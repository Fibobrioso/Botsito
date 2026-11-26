"""Lee lo que graban `tools/mql5/MedirOrdenesFTMO.mq5` (la medida de las ordenes stop) y
`tools/mql5/GrabarTicksFTMO.mq5` (el grabador) en la demo de FTMO, con el criterio pre-registrado de
`docs/plan/F17-ORDENES.yaml` (ADR-0099 §5; rama `trabajo/f17-ordenes`).

    uv run python scripts/leer_ordenes_f17.py medida <carpeta> --salida <fichero>
    uv run python scripts/leer_ordenes_f17.py grabador <carpeta> --salida <fichero>

**medida.** De cada llenado (fila `llenado` de un `F17M_<estrato>_*.csv`), el tick que dispara se
busca en su `F17M_ticks_<deal>.csv`: el primero en `(puesta, llenado]` cuyo ASK (lo que compra) o
BID (lo que vende) toca o pasa el nivel por el lado que ejecuta, como el simulador; un cierre a
mercado usa la cotizacion leida justo antes de pedirlo. El deslizamiento, en puntos, «+ en contra».
Por clase y estrato da n, mediana, percentil (`percentil_deslizamiento_f17` de
`criterio_fidelidad.yaml`), maximo, `sin_tick`, `al_colocar`, fuera de ventana y `bot_reducido`, y
el veredicto de D3.

**grabador.** El spread de FTMO (ASK − BID, en puntos) por hora nominal de la ventana, en los dias
grabados, con los percentiles de `scripts/ticks_spread.py`; y nada mas (la comparacion con Dukascopy
no la hace esta rama: el yaml, `spread_del_grabador`).

**El reloj del servidor** pasa a UTC con `RelojServidor` de `scripts/leer_historial_f17.py` (del
registro, sin cifras). **No filtra por mes** (D6): lo que lea se declara en HOLDOUT-EXPOSICIONES el
dia que corra, por recuento de dias. Imprime puntos, recuentos y fracciones; ningun precio.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
CRITERIO = Path("docs") / "plan" / "F17-ORDENES.yaml"
MS_POR_MINUTO = 60_000
MINUTOS_POR_HORA = 60
CLASES = ("entrada_stop", "cierre_stop", "cierre_mercado")
ESTRATOS = ("uno", "bot")
COLUMNAS_MEDIDA = (
    "version_script",
    "fila",
    "ciclo",
    "estrato",
    "evento",
    "clase",
    "lado",
    "orden",
    "deal",
    "posicion",
    "nivel",
    "lotes",
    "lote_d2",
    "precio",
    "instante_msc",
    "puesta_msc",
    "cot_bid",
    "cot_ask",
    "cot_msc",
    "motivo",
    "retcode",
    "ticks_fichero",
    "ticks_n",
    "ticks_error",
    "comision",
    "hora_servidor",
    "hora_gmt",
    "nota",
)
COLUMNAS_TICKS = ("time_msc", "bid", "ask", "flags")
PATRON_MEDIDA = re.compile(r"^F17M_(uno|bot)_\d{8}_\d{6}\.csv$")
PATRON_TICKS_MEDIDA = re.compile(r"^F17M_ticks_\d+\.csv$")
PATRON_HORA = re.compile(r"^F17G_(\d{4}-\d{2}-\d{2})_(\d{2})\.csv$")
PATRON_CONTROL_GRABADOR = re.compile(r"^F17G_control_\d{8}_\d{6}\.csv$")


class OrdenesError(ValueError):
    """Algo que impide leer o decidir: el mensaje dice que, y no se adivina."""


def _historial() -> ModuleType:
    """`scripts/leer_historial_f17.py`, importado por su ruta y sin editarlo (como sus tests)."""
    nombre = "leer_historial_f17"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo  # lo pide @dataclass al crear la clase
    spec.loader.exec_module(modulo)
    return modulo


H = _historial()
RelojServidor = H.RelojServidor
percentil = H.percentil
mediana = H.mediana
a_puntos = H.a_puntos
_filas = H._filas


# ------------------------------------------------------------------------------ el criterio


@dataclass(frozen=True)
class Criterio:
    sin_tick_maximo: Fraction
    minimo_uno: int
    minimo_bot: int
    bot_si_el_lote_importa: int
    diferencia_que_importa: int
    fraccion_lote_d2: Fraction
    percentil: int  # el percentil_deslizamiento_f17 de criterio_fidelidad.yaml


def cargar_criterio_ordenes(raiz: Path) -> Criterio:
    sys.path.insert(0, str(raiz / "src"))
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.comun.yaml_estricto import leer_yaml

    c = leer_yaml(raiz / CRITERIO)
    rentabilidad = cargar_criterio(raiz).rentabilidad
    if rentabilidad is None:
        raise OrdenesError("criterio_fidelidad.yaml sin el bloque rentabilidad")
    e = c["estratos"]
    q = c["que_estrato_vale"]
    return Criterio(
        sin_tick_maximo=Fraction(c["sin_tick"]["fraccion_maxima_por_clase"]),
        minimo_uno=int(e["uno"]["minimo_por_clase"]),
        minimo_bot=int(e["bot"]["minimo_por_clase"]),
        bot_si_el_lote_importa=int(q["bot_minimo_si_el_lote_importa"]),
        diferencia_que_importa=int(q["diferencia_que_importa_puntos"]),
        fraccion_lote_d2=Fraction(e["bot_reducido"]["fraccion_minima_del_lote_d2"]),
        percentil=int(rentabilidad.percentil_deslizamiento_f17),
    )


# ------------------------------------------------------------------- el tick que dispara


@dataclass(frozen=True)
class Tick:
    msc: int  # en el reloj del servidor, como en el CSV
    bid: int
    ask: int


def ejecuta_al_ask(lado: str) -> bool:
    """Lo que compra ejecuta al ASK; lo que vende, al BID (el lado de la EJECUCION)."""
    if lado not in ("compra", "venta"):
        raise OrdenesError(f"lado {lado!r}: ni compra ni venta")
    return lado == "compra"


def toca(lado: str, valor: int, nivel: int) -> bool:
    """El valor del lado que ejecuta toca o pasa el nivel: ASK >= nivel al comprar, BID <= nivel
    al vender."""
    return valor >= nivel if ejecuta_al_ask(lado) else valor <= nivel


def tick_que_dispara(
    ticks: Sequence[Tick], lado: str, nivel: int, puesta: int, llenado: int
) -> Tick | None:
    """El primer tick en (puesta, llenado] cuyo lado que ejecuta toca o pasa el nivel; None si no
    lo hay (`sin_tick`)."""
    al_ask = ejecuta_al_ask(lado)
    for t in ticks:
        if t.msc <= puesta or t.msc > llenado:
            continue
        if toca(lado, t.ask if al_ask else t.bid, nivel):
            return t
    return None


def deslizamiento(lado: str, precio: int, referencia: int) -> int:
    """En puntos, «+ en contra»: comprar mas caro o vender mas barato es positivo."""
    return precio - referencia if ejecuta_al_ask(lado) else referencia - precio


def llego_ya_pasada(
    ticks: Sequence[Tick], lado: str, nivel: int, cot: Tick | None, puesta: int
) -> bool:
    """`al_colocar`: la cotizacion leida antes de colocar la entrada, o un tick entre esa lectura y
    la puesta, ya tocaba el nivel."""
    al_ask = ejecuta_al_ask(lado)
    if cot is not None and toca(lado, cot.ask if al_ask else cot.bid, nivel):
        return True
    desde = cot.msc if cot is not None else puesta
    return any(
        desde < t.msc <= puesta and toca(lado, t.ask if al_ask else t.bid, nivel) for t in ticks
    )


# ------------------------------------------------------------------------------ las muestras


@dataclass(frozen=True)
class Muestra:
    clase: str
    estrato: str  # uno, bot o bot_reducido
    valor: int | None  # None: sin_tick o al_colocar
    estado: str  # ok, sin_tick, al_colocar o fuera_de_ventana
    utc_ms: int


def estrato_de(fila: Mapping[str, str], c: Criterio) -> str:
    """«bot» solo si el lote usado es al menos `fraccion_lote_d2` del de ADR-0081 D2 de ese
    momento; si no, `bot_reducido` (respuesta a la PARADA, punto 2)."""
    estrato = fila["estrato"]
    if estrato == "uno":
        return "uno"
    if estrato != "bot":
        raise OrdenesError(f"estrato {estrato!r}")
    usado, d2 = Fraction(fila["lotes"]), Fraction(fila["lote_d2"])
    return "bot" if d2 > 0 and usado >= c.fraccion_lote_d2 * d2 else "bot_reducido"


def _cot(fila: Mapping[str, str], digitos: int) -> Tick | None:
    if not fila.get("cot_bid") or not fila.get("cot_ask"):
        return None
    return Tick(
        int(fila["cot_msc"]), a_puntos(fila["cot_bid"], digitos), a_puntos(fila["cot_ask"], digitos)
    )


def muestra_de(
    fila: Mapping[str, str],
    ticks: Sequence[Tick],
    digitos: int,
    en_ventana: Any,
    reloj: Any,
    c: Criterio,
) -> Muestra:
    """La muestra de una fila `llenado` de una de las tres clases."""
    clase, lado = fila["clase"], fila["lado"]
    if clase not in CLASES:
        raise OrdenesError(f"clase {clase!r}")
    precio = a_puntos(fila["precio"], digitos)
    llenado = int(fila["instante_msc"])
    utc = reloj.a_utc(llenado)
    estrato = estrato_de(fila, c)
    if not en_ventana(utc):
        return Muestra(clase, estrato, None, "fuera_de_ventana", utc)
    cot = _cot(fila, digitos)
    if clase == "cierre_mercado":
        if cot is None:
            raise OrdenesError(f"fila {fila['fila']}: un cierre a mercado sin su cotizacion previa")
        ref = cot.ask if ejecuta_al_ask(lado) else cot.bid
        return Muestra(clase, estrato, deslizamiento(lado, precio, ref), "ok", utc)
    nivel = a_puntos(fila["nivel"], digitos)
    puesta = int(fila["puesta_msc"])
    if clase == "entrada_stop" and llego_ya_pasada(ticks, lado, nivel, cot, puesta):
        return Muestra(clase, estrato, None, "al_colocar", utc)
    t = tick_que_dispara(ticks, lado, nivel, puesta, llenado)
    if t is None:
        return Muestra(clase, estrato, None, "sin_tick", utc)
    ref = t.ask if ejecuta_al_ask(lado) else t.bid
    return Muestra(clase, estrato, deslizamiento(lado, precio, ref), "ok", utc)


# ------------------------------------------------------------------------------ el veredicto


@dataclass
class Resumen:
    valores: list[int] = field(default_factory=list)
    sin_tick: int = 0
    al_colocar: int = 0
    fuera_de_ventana: int = 0

    @property
    def n(self) -> int:
        return len(self.valores)

    def anadir(self, m: Muestra) -> None:
        if m.estado == "ok":
            assert m.valor is not None
            self.valores.append(m.valor)
        elif m.estado == "sin_tick":
            self.sin_tick += 1
        elif m.estado == "al_colocar":
            self.al_colocar += 1
        else:
            self.fuera_de_ventana += 1

    def demasiados_sin_tick(self, c: Criterio) -> bool:
        """Mas del 5 % de `sin_tick` entre las muestras de la ventana que no son `al_colocar`."""
        total = self.n + self.sin_tick
        return total > 0 and Fraction(self.sin_tick, total) > c.sin_tick_maximo


@dataclass(frozen=True)
class Veredicto:
    clase: str
    estado: str  # valido, insuficiente o sin_veredicto
    estrato: str | None  # el que vale
    mediana: int | None
    percentil: int | None
    motivo: str


def veredicto(clase: str, uno: Resumen, bot: Resumen, c: Criterio) -> Veredicto:
    """D3: que estrato vale y con que mediana y percentil."""
    if uno.demasiados_sin_tick(c) or bot.demasiados_sin_tick(c):
        return Veredicto(clase, "sin_veredicto", None, None, None, "mas del 5 % de sin_tick")
    if uno.n < c.minimo_uno or bot.n < c.minimo_bot:
        return Veredicto(
            clase,
            "insuficiente",
            None,
            None,
            None,
            f"uno {uno.n}/{c.minimo_uno}, bot {bot.n}/{c.minimo_bot}",
        )
    m_uno = mediana(uno.valores)
    m_bot = mediana(bot.valores)
    p = c.percentil / 100
    if m_bot - m_uno >= c.diferencia_que_importa:
        if bot.n < c.bot_si_el_lote_importa:
            return Veredicto(
                clase,
                "insuficiente",
                "bot",
                None,
                None,
                f"el lote importa (mediana bot {m_bot} - uno {m_uno} >= "
                f"{c.diferencia_que_importa}); bot {bot.n}/{c.bot_si_el_lote_importa}",
            )
        return Veredicto(
            clase, "valido", "bot", m_bot, percentil(sorted(bot.valores), p), "el lote importa"
        )
    p90 = max(percentil(sorted(uno.valores), p), max(bot.valores))
    return Veredicto(
        clase, "valido", "uno", m_uno, p90, f"percentil: max(p{c.percentil} uno, max bot)"
    )


# --------------------------------------------------------------------------- los ficheros


def leer_ticks_de(ruta: Path, digitos: int) -> list[Tick]:
    return [
        Tick(int(f["time_msc"]), a_puntos(f["bid"], digitos), a_puntos(f["ask"], digitos))
        for f in _filas(ruta, COLUMNAS_TICKS)
    ]


def ventana_de(registro: Any, sesiones: Any) -> Any:
    """`en_ventana(utc_ms)`: el minuto UTC cae en [ventana_inicio, ventana_fin) del dia por
    `reloj_de_las_sesiones` (la rejilla), sin el calendario de cierres."""
    inicio = _minutos(registro.hora("ventana_inicio").hora)
    fin = _minutos(registro.hora("ventana_fin").hora)

    def en_ventana(utc_ms: int) -> bool:
        try:
            _, minuto = sesiones.lectura(utc_ms // MS_POR_MINUTO)
        except ValueError:
            return False
        return bool(inicio <= int(minuto) < fin)

    return en_ventana


def _minutos(hhmm: str) -> int:
    hh, mm = hhmm.split(":")
    return int(hh) * MINUTOS_POR_HORA + int(mm)


def leer_medida(
    carpeta: Path, digitos: int, en_ventana: Any, reloj: Any, c: Criterio
) -> tuple[dict[tuple[str, str], Resumen], dict[str, int]]:
    """Los resumenes por (clase, estrato) y los recuentos de lo demas (otras salidas, filas)."""
    resumenes: dict[tuple[str, str], Resumen] = defaultdict(Resumen)
    otros: dict[str, int] = defaultdict(int)
    for csv_medida in sorted(p for p in carpeta.iterdir() if PATRON_MEDIDA.match(p.name)):
        for fila in _filas(csv_medida, COLUMNAS_MEDIDA):
            if fila["evento"] != "llenado":
                otros[fila["evento"]] += 1
                continue
            if fila["clase"] not in CLASES:
                otros[f"llenado {fila['clase']}"] += 1
                continue
            nombre = fila["ticks_fichero"]
            ticks = leer_ticks_de(carpeta / nombre, digitos) if nombre else []
            m = muestra_de(fila, ticks, digitos, en_ventana, reloj, c)
            resumenes[(m.clase, m.estrato)].anadir(m)
    return resumenes, otros


def lineas_medida(
    resumenes: Mapping[tuple[str, str], Resumen], otros: Mapping[str, int], c: Criterio
) -> list[str]:
    salida: list[str] = []
    for clase in CLASES:
        for estrato in (*ESTRATOS, "bot_reducido"):
            r = resumenes.get((clase, estrato), Resumen())
            v = sorted(r.valores)
            cifras = (
                f"mediana {mediana(v)}, p{c.percentil} {percentil(v, c.percentil / 100)}, "
                f"max {v[-1]}"
                if v
                else "sin muestras"
            )
            salida.append(
                f"{clase} · {estrato}: n {r.n}; {cifras}; sin_tick {r.sin_tick}; al_colocar "
                f"{r.al_colocar}; fuera de ventana {r.fuera_de_ventana}"
            )
        vd = veredicto(
            clase,
            resumenes.get((clase, "uno"), Resumen()),
            resumenes.get((clase, "bot"), Resumen()),
            c,
        )
        salida.append(
            f"VEREDICTO {clase}: {vd.estado}"
            + (
                f" (vale {vd.estrato}: mediana {vd.mediana}, p{c.percentil} {vd.percentil})"
                if vd.mediana is not None
                else ""
            )
            + f"; {vd.motivo}"
        )
    salida.append(
        "OTRAS FILAS: " + (", ".join(f"{k} {n}" for k, n in sorted(otros.items())) or "ninguna")
    )
    salida.append(
        "NO DICE: que la prueba gratuita ejecute como el Challenge y la cuenta real (P4-08); "
        "y cómo entran las medianas en ADR-0092 §4 no lo decide esta medida "
        "(deslizamiento sigue en pendiente_F17)"
    )
    return salida


def spread_por_hora(
    carpeta: Path, digitos: int, reloj: Any, sesiones: Any, inicio: int, fin: int
) -> tuple[dict[int, list[int]], set[date], int]:
    """Los spreads de la ventana por hora nominal, los dias grabados y cuantos ticks se leyeron."""
    por_hora: dict[int, list[int]] = defaultdict(list)
    dias: set[date] = set()
    leidos = 0
    for p in sorted(q for q in carpeta.iterdir() if PATRON_HORA.match(q.name)):
        for t in leer_ticks_de(p, digitos):
            leidos += 1
            utc = reloj.a_utc(t.msc)
            try:
                dia, minuto = sesiones.lectura(utc // MS_POR_MINUTO)
            except ValueError:
                continue
            if inicio <= minuto < fin:
                por_hora[minuto // MINUTOS_POR_HORA].append(t.ask - t.bid)
                dias.add(dia)
    return por_hora, dias, leidos


def lineas_grabador(
    por_hora: Mapping[int, list[int]], dias: Iterable[date], leidos: int
) -> list[str]:
    salida = [f"GRABADOR: {leidos} ticks leidos; {len(set(dias))} dias con ticks en la ventana"]
    for hora in sorted(por_hora):
        v = sorted(por_hora[hora])
        if v:
            salida.append(
                f"  spread FTMO {hora:02d}:00: n {len(v)}, p50 {percentil(v, 0.5)}, "
                f"p90 {percentil(v, 0.9)}, p99 {percentil(v, 0.99)}, max {v[-1]}"
            )
    return salida


# ----------------------------------------------------------------------- los manifiestos (D7)

PATRON_DATASET = {
    "ordenes": re.compile(r"^f17-ordenes-(\d{4}-\d{2}-\d{2})-([0-9a-f]{8})$"),
    "grabador": re.compile(r"^f17-grabador-(\d{4}-\d{2}-\d{2})-([0-9a-f]{8})$"),
}
TIPOS = {"ordenes": frozenset({"medida", "ticks"}), "grabador": frozenset({"hora", "control"})}
CAMPOS = {
    "ordenes": (
        "schema_f17_ordenes",
        "dataset_id",
        "estrato",
        "ficheros",
        "dias",
        "script",
        "control",
        "cuenta",
        "declarado_por",
        "congelado_el",
        "rama",
        "informe",
    ),
    "grabador": (
        "schema_f17_grabador",
        "dataset_id",
        "ficheros",
        "dias",
        "script",
        "control",
        "cuenta",
        "declarado_por",
        "congelado_el",
        "rama",
        "informe",
    ),
}
CARPETA_MANIFIESTOS = {"ordenes": "f17-ordenes", "grabador": "f17-grabador"}


def validar_manifiesto(doc: Mapping[str, Any], tipo: str) -> list[str]:
    """Lo que no cumple el esquema `schema_f17_ordenes: 1` o `schema_f17_grabador: 1` de
    `data/manifests/README.md`."""
    campos = CAMPOS[tipo]
    salida = [f"falta {k}" for k in campos if k not in doc]
    if salida:
        return salida
    salida += [f"campo de mas: {k}" for k in doc if k not in campos]
    if doc[campos[0]] != 1:
        salida.append(f"{campos[0]} no es 1")
    if tipo == "ordenes" and doc["estrato"] not in ESTRATOS:
        salida.append(f"estrato {doc['estrato']!r}")
    ficheros = doc["ficheros"] or []
    tipos = set()
    for f in ficheros:
        if f.get("tipo") not in TIPOS[tipo]:
            salida.append(f"{f.get('ruta')}: tipo {f.get('tipo')!r}")
        tipos.add(f.get("tipo"))
        if not re.fullmatch(r"[0-9a-f]{64}", str(f.get("sha256", ""))):
            salida.append(f"{f.get('ruta')}: sha256 mal formado")
        for k in ("ruta", "bytes", "filas", "fin_de_linea"):
            if k not in f:
                salida.append(f"{f.get('ruta')}: falta {k}")
    if tipos != TIPOS[tipo]:
        salida.append(f"faltan ficheros de tipo {sorted(TIPOS[tipo] - tipos)}")
    m = PATRON_DATASET[tipo].match(str(doc["dataset_id"]))
    if m is None:
        salida.append("dataset_id mal formado")
    elif not salida and m.group(2) != H.sufijo_de(ficheros):
        salida.append("el sufijo del dataset_id no es el de sus ficheros")
    if not isinstance(doc["dias"], int) or doc["dias"] < 1:
        salida.append("dias: un recuento de dias, al menos 1")
    for k in ("time_trade_server_s", "time_gmt_s", "desfase_servidor_gmt_min", "cuadra"):
        if k not in (doc["control"] or {}):
            salida.append(f"control: falta {k}")
    return salida


# ------------------------------------------------------------------------------- la salida


def main(argv: Sequence[str] | None = None, raiz: Path = RAIZ) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("forma", choices=("medida", "grabador"))
    ap.add_argument("carpeta", type=Path)
    ap.add_argument("--salida", type=Path, required=True)
    a = ap.parse_args(argv)
    sys.path.insert(0, str(raiz / "src"))
    from botsito.config.registro import cargar_registro
    from botsito.engine.relojes import reloj_de_las_sesiones

    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    sesiones = reloj_de_las_sesiones(registro)
    reloj = RelojServidor.del_registro(registro)
    c = cargar_criterio_ordenes(raiz)
    digitos = _digitos(a.carpeta, a.forma)
    salida = [
        f"CRITERIO: {CRITERIO.as_posix()} (pre-registrado, ADR-0099 §5)",
        f"RELOJ: servidor = UTC + {reloj.base_minutos} min + verano de {reloj.huso or 'ninguno'} "
        "(broker_offset_base y broker_dst del registro)",
    ]
    if a.forma == "medida":
        resumenes, otros = leer_medida(a.carpeta, digitos, ventana_de(registro, sesiones), reloj, c)
        salida += lineas_medida(resumenes, otros, c)
    else:
        inicio = _minutos(registro.hora("ventana_inicio").hora)
        fin = _minutos(registro.hora("ventana_fin").hora)
        salida += lineas_grabador(
            *spread_por_hora(a.carpeta, digitos, reloj, sesiones, inicio, fin)
        )
    a.salida.write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


def _digitos(carpeta: Path, forma: str) -> int:
    """Los `digits` del simbolo, de la fila de contexto de la medida o del control del grabador."""
    if forma == "medida":
        for p in sorted(q for q in carpeta.iterdir() if PATRON_MEDIDA.match(q.name)):
            for f in _filas(p, COLUMNAS_MEDIDA):
                if f["evento"] == "contexto" and f["clase"] == "digits":
                    return int(f["motivo"])
    else:
        for p in sorted(q for q in carpeta.iterdir() if PATRON_CONTROL_GRABADOR.match(q.name)):
            control = H.leer_control(p)
            if "digits" in control:
                return int(control["digits"])
    raise OrdenesError("no se encuentran los digits del simbolo en ningun CSV")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
