"""Los graficos de S-7 a S-12 de la sesion 6 (rama `trabajo/barrido-sesion-6`, D6 del encargo y la
respuesta del consultor a la PARADA del 2026-10-28, puntos 3 a 6).

Por cada dia de construccion pedido, un SVG con tres paneles -H4, M15 y M1- cortados en el cierre
de la vela de M1 en que el bot coloca su primera orden de la sesion, y otro igual con una sola
marca: la linea horizontal en el punto de esa orden, que es su precio de entrada. Sin la orden, el
stop, el objetivo, el llenado ni el resultado. Los SVG van FUERA del repositorio, con `clave.txt`
(que dia, sesion y corte es cada grafico; la guarda Aleks y no se ensena).

NEGAR POR DEFECTO (D6 a). Todo minuto con una vela en la imagen, contado a la vez en la hora de
Madrid y en UTC, tiene que caer en un dia de construccion de la regla 2 de
`docs/runbooks/SESION-DE-PREGUNTAS.md` (abril, julio del 1 al 17, agosto y enero del 2 al 30;
ADR-0078 y ADR-0079) y no estar en `casos_ocultos`. La ventana de cada marco se recorta hacia atras
hasta el primer minuto que no cumple; un dia pedido que no cumple, un mes que el guion no sabe
clasificar o una vela fuera de la ventana hacen salir con error SIN ESCRIBIR NADA: todo se calcula
antes de escribir el primer fichero.

LAS VENTANAS (decision 4): H4 desde las 00:00 de Madrid de cuatro dias antes; M15 desde las 00:00 de
Madrid del dia anterior; M1 desde una hora antes del inicio de la sesion; todo hasta el corte. Una
vela de H4 o de M15 que empieza antes del recorte no se dibuja (estaria a medias); la ultima, en
formacion, se dibuja hasta el corte, como la veria el trader en su replay.

LAS VELAS (D6 b): por la API del manifiesto (`buscar_manifiesto`, `cargar_manifiesto`,
`cargar_ventana`, la misma del arnes), que lee el fichero mensual entero y se queda con la ventana.
Solo el mes del dia pedido, sin el calentamiento del mes anterior. El guion no recorre carpetas.
Imprime, por mes leido, cuantos dias tienen velas, cuantos estan en `casos_ocultos` y cuantos caen
fuera de la construccion: recuentos, nunca fechas.

LA ORDEN Y SU PUNTO (D6 c y e): de «### Ordenes» de la salida commiteada de la corrida diaria
(`docs/validation/anexos/RECORRIDA-CONSTRUCCION/diaria.DIAGNOSTICO.cuenta=diaria.txt`), la primera
colocada de la sesion, canceladas incluidas. Sin correr el motor.

SIN FECHAS (D6 d): ni en los SVG -ningun texto, ningun atributo, sin <title>, sin <metadata> y sin
comentarios- ni en sus nombres (`grafico-N-limpio.svg`, `grafico-N-marcado.svg`). Las horas, en la
de Madrid de ese dia (ADR-0069), y el marco escrito en cada panel.

LA RAIZ (D6 f): sale de `--salida`, y el guion se niega a escribir dentro del repositorio.

Uso, desde la raiz del repo:
    uv run python scripts/graficos_sesion.py --dias <fichero> --salida <carpeta fuera del repo>
`--dias`: una linea por grafico, en su orden, con «AAAA-MM-DD HH-HH» (el dia y la sesion).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Callable, Collection, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.data.agregacion import agregar
from botsito.data.velas import a_datetime, a_minuto
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MinutoUtc, Vela

RAIZ = Path(__file__).resolve().parents[1]
MADRID = ZoneInfo("Europe/Madrid")
ANEXO_ORDENES = (
    Path("docs") / "validation" / "anexos" / "RECORRIDA-CONSTRUCCION"
    / "diaria.DIAGNOSTICO.cuenta=diaria.txt"
)  # fmt: skip
# La regla 2 de SESION-DE-PREGUNTAS.md: mes -> (primer dia, ultimo dia) de construccion.
CONSTRUCCION: Mapping[str, tuple[int, int]] = {
    "2026-01": (2, 30),
    "2026-04": (1, 30),
    "2026-07": (1, 17),
    "2026-08": (1, 31),
}
MINUTOS_H4 = 240
MINUTOS_M15 = 15
DIAS_H4 = 4
DIAS_M15 = 1
HORA_ANTES_M1 = timedelta(hours=1)
_LINEA_ORDEN = re.compile(
    r"^(?:\[[^\]]*\] )?(\d{4}-\d\d-\d\d) \| (\d\d-\d\d) \| (\S+) \| (\S+) \| (\d+\.\d+) \| "
)
_PUNTO = re.compile(r"\| (\d+)@\d+ \| [\d.]+$")


class GraficoError(ValueError):
    """Algo no se puede dibujar sin romper D6: no se escribe nada."""


@dataclass(frozen=True)
class Pedido:
    dia: date
    sesion: str  # «07-11» o «11-15», en la hora de Madrid

    @property
    def inicio_sesion(self) -> datetime:
        return datetime.combine(self.dia, time(int(self.sesion[:2])), tzinfo=MADRID)


@dataclass(frozen=True)
class Orden:
    colocada: datetime  # el cierre de la M1 que la coloca (hh:mm:59.999 UTC)
    punto: int  # en puntos, la escala de las velas


@dataclass(frozen=True)
class Grafico:
    pedido: Pedido
    corte: MinutoUtc  # inicio de la ultima M1 dibujada: la que coloca la orden
    punto: int
    escala: int
    h4: tuple[Vela, ...]
    m15: tuple[Vela, ...]
    m1: tuple[Vela, ...]


# ------------------------------------------------------------------------------ lo permitido


def es_de_construccion(d: date, construccion: Mapping[str, tuple[int, int]]) -> bool:
    tramo = construccion.get(f"{d.year:04d}-{d.month:02d}")
    return tramo is not None and tramo[0] <= d.day <= tramo[1]


def permitido(
    minuto: int, construccion: Mapping[str, tuple[int, int]], ocultos: Collection[tuple[int, int]]
) -> bool:
    """El minuto cae, en Madrid y en UTC, en un dia de construccion que no esta en casos_ocultos."""
    instante = a_datetime(minuto)
    for d in (instante.date(), instante.astimezone(MADRID).date()):
        if not es_de_construccion(d, construccion) or (d.month, d.day) in ocultos:
            return False
    return True


def recorte(
    desde: int,
    corte: int,
    construccion: Mapping[str, tuple[int, int]],
    ocultos: Collection[tuple[int, int]],
) -> int:
    """El primer minuto de la ventana [desde, corte] desde el que TODO esta permitido."""
    if not permitido(corte, construccion, ocultos):
        raise GraficoError("el corte no cae en un dia de construccion libre (regla 2)")
    m = corte
    while m - 1 >= desde and permitido(m - 1, construccion, ocultos):
        m -= 1
    return m


# ------------------------------------------------------------------------------ la orden


def primeras_ordenes(texto: str) -> dict[tuple[str, str], Orden]:
    """La primera orden colocada de cada (dia, sesion) de «### Ordenes», canceladas incluidas."""
    salida: dict[tuple[str, str], Orden] = {}
    dentro = False
    for linea in texto.splitlines():
        cuerpo = re.sub(r"^\[[^\]]*\] ", "", linea)
        if cuerpo.startswith("### Ordenes ("):
            dentro = True
            continue
        if dentro and cuerpo.startswith("#"):
            break
        if not dentro:
            continue
        m = _LINEA_ORDEN.match(cuerpo)
        p = _PUNTO.search(cuerpo)
        if m is None or p is None:
            continue
        colocada = datetime.fromisoformat(m.group(4))
        clave = (m.group(1), m.group(2))
        if clave not in salida or colocada < salida[clave].colocada:
            salida[clave] = Orden(colocada, int(p.group(1)))
    return salida


# ------------------------------------------------------------------------------ las velas


def preparar(
    pedido: Pedido,
    orden: Orden,
    cargar: Callable[[int, int], tuple[Sequence[Vela], int]],
    anclaje: HoraLocal,
    construccion: Mapping[str, tuple[int, int]],
    ocultos: Collection[tuple[int, int]],
) -> Grafico:
    """Las velas de un grafico, recortadas y cortadas; `cargar(desde, hasta)` da las M1 de
    [desde, hasta) y la escala. Puro salvo `cargar`."""
    if not es_de_construccion(pedido.dia, construccion) or (
        (pedido.dia.month, pedido.dia.day) in ocultos
    ):
        raise GraficoError("un dia pedido no es de construccion o esta en casos_ocultos")
    colocada = orden.colocada.astimezone(UTC)
    corte = a_minuto(colocada.replace(second=0, microsecond=0))
    if a_datetime(corte).astimezone(MADRID).date() != pedido.dia:
        raise GraficoError("la primera orden no cae en el dia pedido")
    fin = corte + 1
    dia = datetime.combine(pedido.dia, time(), tzinfo=MADRID)
    desde = {
        "h4": recorte(a_minuto(dia - timedelta(days=DIAS_H4)), corte, construccion, ocultos),
        "m15": recorte(a_minuto(dia - timedelta(days=DIAS_M15)), corte, construccion, ocultos),
        "m1": recorte(a_minuto(pedido.inicio_sesion - HORA_ANTES_M1), corte, construccion, ocultos),
    }
    velas, escala = cargar(min(desde.values()), fin)
    m1 = [v for v in velas if min(desde.values()) <= v.inicio < fin]
    if len(m1) != len(velas):
        raise GraficoError("el lector devolvio velas fuera de la ventana")
    if not m1 or m1[-1].inicio != corte:
        raise GraficoError("no hay M1 en el minuto del corte")
    paneles: dict[str, tuple[Vela, ...]] = {}
    for marco, minutos in (("h4", MINUTOS_H4), ("m15", MINUTOS_M15), ("m1", 1)):
        propias = [v for v in m1 if v.inicio >= desde[marco]]
        agregadas = propias if minutos == 1 else agregar(propias, minutos, anclaje)
        paneles[marco] = tuple(v for v in agregadas if v.inicio >= desde[marco])
    g = Grafico(pedido, corte, orden.punto, escala, paneles["h4"], paneles["m15"], paneles["m1"])
    comprobar(g, construccion, ocultos)
    return g


def comprobar(
    g: Grafico,
    construccion: Mapping[str, tuple[int, int]],
    ocultos: Collection[tuple[int, int]],
) -> None:
    """Ultima puerta: ninguna vela pasa del corte ni toca un minuto no permitido."""
    for velas in (g.h4, g.m15, g.m1):
        for v in velas:
            ultimo = min(int(v.fin), g.corte + 1) - 1
            if v.inicio > g.corte or ultimo > g.corte:
                raise GraficoError("una vela pasa del corte")
            for minuto in (int(v.inicio), ultimo):
                if not permitido(minuto, construccion, ocultos):
                    raise GraficoError("una vela toca un minuto fuera de la construccion")


# ------------------------------------------------------------------------------ el SVG

ANCHO = 1600
ALTO_PANEL = 300
MARGEN_IZQ = 20
MARGEN_DER = 110
MARGEN_SUP = 30
MARGEN_INF = 30
VERDE = "#26a69a"
ROJA = "#ef5350"
GRIS = "#9e9e9e"
_RE_FECHA = re.compile(
    r"\d{4}-\d{1,2}-\d{1,2}|\b\d{1,2}/\d{1,2}\b|\b\d{1,2}-\d{1,2}\b|"
    r"enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|"
    r"diciembre|january|february|march|april|june|july|august|september|october|november|december",
    re.IGNORECASE,
)


def lleva_fecha(texto: str) -> bool:
    """Una fecha en cualquiera de las formas de D6 d): AAAA-MM-DD, DD/MM, DD-MM o un mes."""
    return _RE_FECHA.search(texto) is not None


def _precio(puntos: int, escala: int) -> str:
    decimales = len(str(escala)) - 1
    return f"{puntos / escala:.{decimales}f}"


def _panel(
    velas: Sequence[Vela], marco: str, y0: int, escala: int, punto: int | None, extra: Sequence[int]
) -> list[str]:
    if not velas:
        raise GraficoError(f"el panel {marco} se queda sin velas")
    alto = ALTO_PANEL - MARGEN_SUP - MARGEN_INF
    ancho = ANCHO - MARGEN_IZQ - MARGEN_DER
    precios = [int(v.maxima) for v in velas] + [int(v.minima) for v in velas] + list(extra)
    hi, lo = max(precios), min(precios)
    rango = max(hi - lo, 1)
    paso = ancho / len(velas)

    def y(p: int) -> float:
        return y0 + MARGEN_SUP + (hi - p) / rango * alto

    partes = [
        f'<text x="{MARGEN_IZQ}" y="{y0 + 20}" font-size="18" font-weight="bold">{marco}</text>'
    ]
    for k in range(5):
        p = lo + rango * k // 4
        partes.append(
            f'<text x="{ANCHO - MARGEN_DER + 8}" y="{y(p) + 4:.1f}" font-size="12">'
            f"{_precio(p, escala)}</text>"
        )
    cada = max(1, len(velas) // 10)
    anterior: date | None = None
    for i, v in enumerate(velas):
        x = MARGEN_IZQ + (i + 0.5) * paso
        local = a_datetime(v.inicio).astimezone(MADRID)
        if anterior is not None and local.date() != anterior:
            xs = MARGEN_IZQ + i * paso
            partes.append(
                f'<line x1="{xs:.1f}" y1="{y0 + MARGEN_SUP}" x2="{xs:.1f}" '
                f'y2="{y0 + ALTO_PANEL - MARGEN_INF}" stroke="#cccccc" stroke-dasharray="4 4"/>'
            )
        anterior = local.date()
        color = VERDE if v.cierre > v.abierta else ROJA if v.cierre < v.abierta else GRIS
        arriba, abajo = max(int(v.abierta), int(v.cierre)), min(int(v.abierta), int(v.cierre))
        partes.append(
            f'<line x1="{x:.1f}" y1="{y(int(v.maxima)):.1f}" x2="{x:.1f}" '
            f'y2="{y(int(v.minima)):.1f}" stroke="{color}"/>'
        )
        partes.append(
            f'<rect class="vela" x="{x - paso * 0.35:.1f}" y="{y(arriba):.1f}" '
            f'width="{paso * 0.7:.1f}" height="{max(y(abajo) - y(arriba), 1):.1f}" '
            f'fill="{color}"/>'
        )
        if i % cada == 0:
            partes.append(
                f'<text x="{x:.1f}" y="{y0 + ALTO_PANEL - 10}" font-size="11" '
                f'text-anchor="middle">{local:%H:%M}</text>'
            )
    if punto is not None:
        partes.append(
            f'<line class="punto" x1="{MARGEN_IZQ}" y1="{y(punto):.1f}" '
            f'x2="{MARGEN_IZQ + len(velas) * paso:.1f}" y2="{y(punto):.1f}" stroke="#1565c0" '
            f'stroke-width="2"/>'
        )
    return partes


def svg(g: Grafico, marcado: bool) -> str:
    """El SVG de un grafico. La escala de precios del panel de M1 incluye el punto en las dos
    imagenes, para que la marcada sea la limpia mas la linea."""
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO_PANEL * 3}" '
        f'viewBox="0 0 {ANCHO} {ALTO_PANEL * 3}" font-family="sans-serif">',
        f'<rect x="0" y="0" width="{ANCHO}" height="{ALTO_PANEL * 3}" fill="#ffffff"/>',
    ]
    partes += _panel(g.h4, "H4", 0, g.escala, None, ())
    partes += _panel(g.m15, "M15", ALTO_PANEL, g.escala, None, ())
    partes += _panel(g.m1, "M1", ALTO_PANEL * 2, g.escala, g.punto if marcado else None, (g.punto,))
    partes.append("</svg>")
    texto = "\n".join(partes) + "\n"
    if lleva_fecha(texto) or "<!--" in texto or "<title" in texto or "<metadata" in texto:
        raise GraficoError("el SVG llevaria una fecha, un comentario o metadatos")
    return texto


# ------------------------------------------------------------------------------ escribir


def escribir(graficos: Sequence[Grafico], salida: Path, repo: Path) -> list[Path]:
    """Los SVG y clave.txt en `salida`, que no puede estar dentro del repositorio. Todo se genera
    en memoria antes de escribir el primer fichero; no pisa ninguno que ya exista."""
    destino = salida.resolve()
    if destino == repo.resolve() or destino.is_relative_to(repo.resolve()):
        raise GraficoError("la raiz de salida esta dentro del repositorio")
    ficheros: dict[str, str] = {}
    clave = ["# Que es cada grafico. NO SE ENSENA: lo guarda Aleks.", ""]
    for n, g in enumerate(graficos, 1):
        ficheros[f"grafico-{n}-limpio.svg"] = svg(g, marcado=False)
        ficheros[f"grafico-{n}-marcado.svg"] = svg(g, marcado=True)
        corte = a_datetime(g.corte).astimezone(MADRID)
        clave.append(
            f"grafico {n}: {g.pedido.dia.isoformat()}, sesion {g.pedido.sesion}, corte en la M1 de "
            f"las {corte:%H:%M} (Madrid), punto {_precio(g.punto, g.escala)}"
        )
    ficheros["clave.txt"] = "\n".join(clave) + "\n"
    for nombre in ficheros:
        if lleva_fecha(nombre):
            raise GraficoError("un nombre de fichero llevaria una fecha")
        if (destino / nombre).exists():
            raise GraficoError(f"{nombre} ya existe en la salida: no se pisa")
    destino.mkdir(parents=True, exist_ok=True)
    escritos = []
    for nombre, contenido in ficheros.items():
        (destino / nombre).write_text(contenido, encoding="utf-8", newline="\n")
        escritos.append(destino / nombre)
    return escritos


# ------------------------------------------------------------------------------ main


def leer_pedidos(texto: str) -> list[Pedido]:
    pedidos = []
    for linea in texto.splitlines():
        if not linea.strip():
            continue
        m = re.fullmatch(r"\s*(\d{4}-\d\d-\d\d)\s+(07-11|11-15)\s*", linea)
        if m is None:
            raise GraficoError("una linea de --dias no es «AAAA-MM-DD HH-HH»")
        pedidos.append(Pedido(date.fromisoformat(m.group(1)), m.group(2)))
    if not pedidos:
        raise GraficoError("--dias no trae ningun dia")
    return pedidos


def main(argv: Sequence[str] | None = None) -> int:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.holdout import casos_ocultos
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.corpus.cuarentena import dias_de_casos
    from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_ventana

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--dias", required=True, help="fichero con «AAAA-MM-DD HH-HH» por linea")
    p.add_argument("--salida", required=True, help="carpeta FUERA del repositorio")
    a = p.parse_args(argv)
    try:
        if set(cargar_criterio(RAIZ).construccion) != set(CONSTRUCCION):
            raise GraficoError("los meses de construccion del criterio no son los de la regla 2")
        pedidos = leer_pedidos(Path(a.dias).read_text(encoding="utf-8"))
        ocultos = dias_de_casos(casos_ocultos(RAIZ))
        ordenes = primeras_ordenes((RAIZ / ANEXO_ORDENES).read_text(encoding="utf-8"))
        anclaje = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml").hora(
            "anclaje_h4"
        )
        prefijo = cargar_config(
            RAIZ / "knowledge" / "cases" / "kit" / "config.yaml"
        ).dataset_prefijo
        datos = carpeta_datos(RAIZ)
        leidos: dict[str, list[Vela]] = {}
        escalas: dict[str, int] = {}

        def cargar(desde: int, hasta: int) -> tuple[Sequence[Vela], int]:
            mes = a_datetime(desde).strftime("%Y-%m")
            if a_datetime(hasta - 1).strftime("%Y-%m") != mes:
                raise GraficoError("una ventana cruza de mes")
            if mes not in leidos:
                inicio = a_minuto(datetime.strptime(mes, "%Y-%m").replace(tzinfo=UTC))
                manifiesto = cargar_manifiesto(buscar_manifiesto(RAIZ, f"{prefijo}{mes}"))
                serie = cargar_ventana(manifiesto, datos, inicio, None)
                leidos[mes] = [
                    v for v in serie.velas if a_datetime(v.inicio).strftime("%Y-%m") == mes
                ]
                escalas[mes] = serie.escala
            return [v for v in leidos[mes] if desde <= v.inicio < hasta], escalas[mes]

        graficos = []
        for pedido in pedidos:
            orden = ordenes.get((pedido.dia.isoformat(), pedido.sesion))
            if orden is None:
                raise GraficoError("un dia pedido no tiene orden del bot en «### Ordenes»")
            graficos.append(preparar(pedido, orden, cargar, anclaje, CONSTRUCCION, ocultos))
        escritos = escribir(graficos, Path(a.salida), RAIZ)
    except (GraficoError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}. No se ha escrito nada.", file=sys.stderr)
        return 2
    for _mes, velas in sorted(leidos.items()):
        dias = {a_datetime(v.inicio).date() for v in velas}
        print(
            f"LECTURA: un fichero mensual; dias con velas: {len(dias)}; en casos_ocultos: "
            f"{sum(1 for d in dias if (d.month, d.day) in ocultos)}; fuera de la construccion: "
            f"{sum(1 for d in dias if not es_de_construccion(d, CONSTRUCCION))}"
        )
    print(f"OK: {len(escritos)} ficheros ({len(graficos)} graficos y clave.txt) en la salida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
