"""Lee los CSV de `tools/mql5/MedirDemoFTMO.mq5` y los pone en una tabla: cada decisión de ADR-0057,
A-27 y las reglas de FTMO con su valor medido, fichero a fichero, y el desfase del reloj del
servidor frente a GMT por fecha (A-28).

Rama `trabajo/demo-ftmo-script`, 2026-09-28. SOLO LEE: no escribe ningún parámetro ni cierra ninguna
decisión; eso se hace en otra rama, con los CSV reales delante. Un retcode fuera de lo que cada
medición puede devolver se MARCA como inesperado en su celda y en una lista aparte, y nunca se
oculta: esa fila no mide lo que dice. El runbook es `docs/runbooks/DEMO-FTMO.md`.

Lee las dos versiones del script (rama `trabajo/demo-ejecucion-1`, 2026-10-09, ADR-0071): la 1.0, la
de la ejecucion 1, y la 1.1, que abre el paso 6 con `InpVolumenComision` lotes y escribe ese volumen
en la fila `volumen_comision` (o `no_abre` en la apertura si el volumen no se admite o no hay
margen). En la 1.0 una fila de observacion llevaba el texto SIN_RESPUESTA; desde la 1.1 lleva
OBSERVACION, y el lector da OBSERVACION en las dos. Otra version se rechaza.

    uv run python scripts/leer_demo_ftmo.py <csv o carpeta>... [--salida <fichero>]
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

COLUMNAS = (
    "version_script",
    "fila",
    "medicion",
    "responde",
    "clave",
    "valor",
    "retcode",
    "retcode_texto",
    "colocada",
    "tipo_orden",
    "precio_pedido",
    "bid",
    "ask",
    "precio_resultado",
    "distancia_puntos",
    "hora_servidor",
    "hora_gmt",
    "nota",
)
PATRON = "MedirDemoFTMO_*.csv"
# Lo que cada medicion puede devolver al enviar una peticion: aceptada (PLACED, DONE) o rechazada
# por el precio o por los stops (INVALID_PRICE, INVALID_STOPS). Cualquier otro -mercado cerrado,
# trading algoritmico desactivado, volumen, llenado- dice que la fila no mide lo que pretende.
ESPERADOS = {
    "3_lado_equivocado": frozenset({10008, 10009, 10015, 10016}),
    "4_distancias": frozenset({10008, 10009, 10015, 10016}),
    "5_modificacion": frozenset({10008, 10009, 10015, 10016}),
    "6_comision": frozenset({10008, 10009}),
    "7_llenado_stop": frozenset({10008, 10009, 10015, 10016}),
}
# filas que no son una peticion al servidor sino una observacion: su retcode no se juzga
OBSERVACIONES = frozenset({"buy_stop_llenado"})
OBSERVACION = "OBSERVACION"
TEXTO_OBSERVACION_1_0 = "SIN_RESPUESTA"  # lo que escribia la 1.0 en una observacion
VERSIONES = ("1.0", "1.1")
# la 1.0 abria el paso 6 con el volumen minimo del simbolo; la 1.1 escribe el suyo
VOLUMEN_1_0 = "volumen_min"
NO_ABRE = "no_abre"
TIPOS = ("sell_stop", "buy_stop", "sell_limit", "buy_limit")


class LecturaError(ValueError):
    """Un CSV que no es del script: se dice y no se adivina."""


@dataclass(frozen=True)
class Fila:
    fichero: str
    version: str
    medicion: str
    responde: str
    clave: str
    valor: str
    retcode: int | None
    retcode_texto: str
    colocada: str
    tipo_orden: str
    precio_pedido: str
    bid: str
    ask: str
    precio_resultado: str
    distancia_puntos: str
    hora_servidor: str
    hora_gmt: str
    nota: str


def leer_csv(ruta: Path) -> list[Fila]:
    crudo = ruta.read_bytes()
    try:  # el script escribe ANSI; hoy todo es ASCII, pero el nombre del servidor puede no serlo
        texto = crudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = crudo.decode("cp1252")
    lector = csv.reader(texto.splitlines())
    cabecera = next(lector, None)
    if cabecera is None or tuple(cabecera) != COLUMNAS:
        raise LecturaError(f"{ruta.name}: la cabecera no es la de MedirDemoFTMO.mq5")
    filas: list[Fila] = []
    for n, campos in enumerate(lector, 2):
        if not campos:
            continue
        if len(campos) != len(COLUMNAS):
            raise LecturaError(
                f"{ruta.name}, linea {n}: {len(campos)} columnas, no {len(COLUMNAS)}"
            )
        d = dict(zip(COLUMNAS, campos, strict=True))
        version = d["version_script"]
        if version not in VERSIONES:
            raise LecturaError(
                f"{ruta.name}, linea {n}: version_script {version!r}; este lector lee "
                + " y ".join(VERSIONES)
            )
        texto_retcode = d["retcode_texto"]
        if d["clave"] in OBSERVACIONES and texto_retcode == TEXTO_OBSERVACION_1_0:
            texto_retcode = OBSERVACION  # la etiqueta de la 1.0, con el nombre de la 1.1
        filas.append(
            Fila(
                fichero=ruta.name,
                version=version,
                medicion=d["medicion"],
                responde=d["responde"],
                clave=d["clave"],
                valor=d["valor"],
                retcode=int(d["retcode"]) if d["retcode"].strip() else None,
                retcode_texto=texto_retcode,
                colocada=d["colocada"],
                tipo_orden=d["tipo_orden"],
                precio_pedido=d["precio_pedido"],
                bid=d["bid"],
                ask=d["ask"],
                precio_resultado=d["precio_resultado"],
                distancia_puntos=d["distancia_puntos"],
                hora_servidor=d["hora_servidor"],
                hora_gmt=d["hora_gmt"],
                nota=d["nota"],
            )
        )
    if len({f.version for f in filas}) > 1:
        raise LecturaError(f"{ruta.name}: mezcla versiones del script")
    return filas


def es_inesperado(f: Fila) -> bool:
    esperados = ESPERADOS.get(f.medicion)
    if esperados is None or f.retcode is None or f.clave in OBSERVACIONES:
        return False
    return f.retcode not in esperados


def _busca(filas: Sequence[Fila], clave: str) -> Fila | None:
    return next((f for f in filas if f.clave == clave), None)


def _dato(clave: str) -> Callable[[Sequence[Fila]], str]:
    def celda(filas: Sequence[Fila]) -> str:
        f = _busca(filas, clave)
        return "sin medir" if f is None else f.valor

    return celda


def _peticion(clave: str) -> Callable[[Sequence[Fila]], str]:
    """Lo que paso con una peticion: colocada, llenada (y a que precio) o no, con su retcode."""

    def celda(filas: Sequence[Fila]) -> str:
        f = _busca(filas, clave)
        if f is None:
            return "sin medir"
        texto = f"{f.colocada} ({f.retcode} {f.retcode_texto})"
        if f.colocada == "llenada" and f.precio_resultado:
            texto += f" a {f.precio_resultado}"
        if es_inesperado(f):
            texto = f"INESPERADO: {texto}"
        return texto

    return celda


def _varias(prefijo: str) -> Callable[[Sequence[Fila]], str]:
    def celda(filas: Sequence[Fila]) -> str:
        partes = [f"{t} {_peticion(prefijo + t)(filas)}" for t in TIPOS]
        if all(p.endswith("sin medir") for p in partes):
            return "sin medir"
        return "; ".join(partes)

    return celda


def _llenado_stop(filas: Sequence[Fila]) -> str:
    f = _busca(filas, "buy_stop_llenado")
    if f is None:
        return "sin medir"
    if f.valor == "no_salto":
        return "no salto en la espera"
    return f"{f.valor} puntos (nivel {f.precio_pedido}, llenado {f.precio_resultado})"


def _mercado(clave: str) -> Callable[[Sequence[Fila]], str]:
    def celda(filas: Sequence[Fila]) -> str:
        f = _busca(filas, clave)
        if f is None:
            return "sin medir"
        if f.valor == NO_ABRE:  # 1.1: volumen no admitido o sin margen
            return f"no abrio: {f.nota}"
        texto = f"comision {f.valor}; deslizamiento {f.distancia_puntos} puntos"
        return f"INESPERADO: {texto} ({f.retcode} {f.retcode_texto})" if es_inesperado(f) else texto

    return celda


def _volumen_comision(filas: Sequence[Fila]) -> str:
    """Los lotes de la compra del paso 6: los escribe la 1.1; la 1.0 usaba el minimo del simbolo."""
    f = _busca(filas, "volumen_comision")
    if f is not None:
        return f.valor
    minimo = _busca(filas, VOLUMEN_1_0)
    if filas and filas[0].version == "1.0" and minimo is not None:
        return f"{minimo.valor} (la 1.0 usa el volumen minimo)"
    return "sin medir"


# (decision, que se mide, como se lee de las filas de un fichero)
TABLA: tuple[tuple[str, str, Callable[[Sequence[Fila]], str]], ...] = (
    ("ADR-0057 d1", "llenado de una buy stop: precio - nivel", _llenado_stop),
    ("FTMO-REGLAS R12", "lotes de la compra a mercado", _volumen_comision),
    ("ADR-0057 d1 · DN-3", "compra a mercado", _mercado("apertura_compra_mercado")),
    ("ADR-0057 d1 · DN-3", "cierre a mercado", _mercado("cierre_compra_mercado")),
    ("ADR-0057 d2", "pendiente en el nivel exacto", _varias("nivel_exacto_")),
    ("ADR-0057 d2 · d3", "sell stop por encima del bid", _peticion("sell_stop_por_encima_del_bid")),
    ("ADR-0057 d2 · d3", "buy stop por debajo del ask", _peticion("buy_stop_por_debajo_del_ask")),
    (
        "ADR-0057 d2 · d3",
        "sell limit por debajo del bid",
        _peticion("sell_limit_por_debajo_del_bid"),
    ),
    ("ADR-0057 d2 · d3", "buy limit por encima del ask", _peticion("buy_limit_por_encima_del_ask")),
    (
        "ADR-0057 d3",
        "modificar una sell stop al lado equivocado",
        _peticion("modificar_al_lado_equivocado_sell_stop"),
    ),
    (
        "ADR-0057 d3",
        "modificar una buy limit al lado equivocado",
        _peticion("modificar_al_lado_equivocado_buy_limit"),
    ),
    (
        "ADR-0057 d4",
        "cotizacion al enviar (bid/ask en cada fila del CSV)",
        lambda filas: "en el CSV, fila a fila" if filas else "sin medir",
    ),
    ("ADR-0057 d5 · A-27", "stops level (puntos)", _dato("stops_level_puntos")),
    ("ADR-0057 d5 · A-27", "a la distancia del stops level", _varias("a_distancia_stops_level_")),
    ("ADR-0057 d5 · A-27", "un punto dentro del stops level", _varias("un_punto_dentro_")),
    ("ADR-0057 d5", "freeze level (puntos)", _dato("freeze_level_puntos")),
    ("A-27", "digits", _dato("digits")),
    ("A-27", "point", _dato("point")),
    ("A-27", "contrato", _dato("contrato")),
    ("A-27", "volumen minimo", _dato("volumen_min")),
    ("A-27", "paso de volumen", _dato("volumen_paso")),
    ("A-27", "modos de llenado", _dato("modos_llenado")),
    ("A-27", "modo de ejecucion", _dato("modo_ejecucion")),
    ("FTMO-REGLAS R11", "volumen maximo", _dato("volumen_max")),
    ("FTMO-REGLAS R12", "swap largo", _dato("swap_largo")),
    ("FTMO-REGLAS R12", "swap corto", _dato("swap_corto")),
    ("FTMO-REGLAS R12", "modo de swap", _dato("swap_modo")),
    ("FTMO-REGLAS R12", "dia del triple swap", _dato("swap_triple_dia")),
)


def _escapa(texto: str) -> str:
    return texto.replace("|", "/")


def informe(ficheros: dict[str, list[Fila]]) -> str:
    nombres = sorted(ficheros)
    lineas = [
        f"# Demo de FTMO: lo medido ({len(nombres)} fichero(s))",
        "",
        "Solo lee: ningun valor pasa a los parametros ni cierra ninguna decision desde aqui.",
        "",
    ]
    for n in nombres:
        fin = _busca(ficheros[n], "terminado")
        version = ficheros[n][0].version if ficheros[n] else "?"
        lineas.append(
            f"- {n}: {fin.valor if fin else 'SIN LA FILA DE FIN (cortado)'} (script {version})"
        )
    lineas += [
        "",
        "## Decision a decision",
        "",
        "| decision | que se mide | " + " | ".join(nombres) + " |",
        "|---|---|" + "---|" * len(nombres),
    ]
    for decision, que, leer in TABLA:
        celdas = [_escapa(leer(ficheros[n])) for n in nombres]
        lineas.append(f"| {decision} | {que} | " + " | ".join(celdas) + " |")

    lineas += ["", "## A-28: desfase del servidor frente a GMT, por fecha", ""]
    lineas += ["| fecha (servidor) | desfase (min) | hora del servidor | hora GMT | fichero |"]
    lineas += ["|---|---|---|---|---|"]
    for n in nombres:
        f = _busca(ficheros[n], "desfase_servidor_gmt_min")
        if f is None:
            lineas.append(f"| - | sin medir | - | - | {n} |")
            continue
        fecha = f.hora_servidor.split(" ")[0]
        lineas.append(f"| {fecha} | {f.valor} | {f.hora_servidor} | {f.hora_gmt} | {n} |")

    raros = [f for n in nombres for f in ficheros[n] if es_inesperado(f)]
    lineas += ["", "## Retcodes INESPERADOS: esas filas no miden lo que dicen", ""]
    if raros:
        for f in raros:
            lineas.append(
                f"- {f.fichero} · {f.medicion} · {f.clave}: {f.retcode} {f.retcode_texto}"
                + (f" ({f.nota})" if f.nota else "")
            )
    else:
        lineas.append("- ninguno")

    avisos = [
        f"- {f.fichero}: {f.clave} = {f.valor}"
        for n in nombres
        for f in ficheros[n]
        if f.medicion == "limpieza" and f.valor != "0"
    ]
    avisos += [
        f"- {f.fichero}: {f.clave} ({f.nota})"
        for n in nombres
        for f in ficheros[n]
        if f.medicion == "error"
    ]
    lineas += ["", "## Avisos de seguridad", ""]
    lineas += avisos or ["- ninguno: el script no dejo nada abierto"]
    return "\n".join(lineas) + "\n"


def ficheros_de(rutas: Sequence[Path]) -> dict[str, list[Fila]]:
    salida: dict[str, list[Fila]] = {}
    for ruta in rutas:
        if not ruta.exists():
            raise LecturaError(f"{ruta}: no existe")
        candidatos = sorted(ruta.glob(PATRON)) if ruta.is_dir() else [ruta]
        for c in candidatos:
            salida[c.name] = leer_csv(c)
    if not salida:
        raise LecturaError(f"ningun {PATRON} en {', '.join(str(r) for r in rutas)}")
    return salida


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument(
        "rutas", nargs="+", type=Path, help="CSV del script o carpetas que los contienen"
    )
    p.add_argument("--salida", type=Path, help="fichero donde escribir la tabla (si no, pantalla)")
    args = p.parse_args(argv)
    try:
        texto = informe(ficheros_de(args.rutas))
    except LecturaError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.salida is None:
        sys.stdout.write(texto)
    else:
        args.salida.write_text(texto, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
