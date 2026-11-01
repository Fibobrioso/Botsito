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

La 1.2 (rama `trabajo/margen-pendiente`, 2026-10-31) anade el paso 8: cuando comprueba MT5 el margen
de una pendiente stop (ADR-0081 §4). Sus respuestas (M1 a M4), con la regla escrita ANTES de
ejecutarlo (`docs/validation/MARGEN-PENDIENTE.md`, respuesta del consultor a la PARADA), van en una
seccion aparte que solo sale si hay un fichero 1.2; con ficheros 1.0 o 1.1 la salida no cambia. Todo
lo que no prueba la causa sale «no concluyente».

    uv run python scripts/leer_demo_ftmo.py <csv o carpeta>... [--salida <fichero>]
"""

from __future__ import annotations

import argparse
import csv
import re
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
    # 1.2: el paso 8 espera, ademas, el rechazo por margen (10019 NO_MONEY)
    "8_margen": frozenset({10008, 10009, 10019}),
}
# filas que no son una peticion al servidor sino una observacion: su retcode no se juzga
OBSERVACIONES = frozenset({"buy_stop_llenado", "m4_resultado"})
OBSERVACION = "OBSERVACION"
TEXTO_OBSERVACION_1_0 = "SIN_RESPUESTA"  # lo que escribia la 1.0 en una observacion
VERSIONES = ("1.0", "1.1", "1.2")
VERSION_PASO_8 = "1.2"
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


# --- Paso 8 (1.2): cuando comprueba MT5 el margen de una pendiente stop (ADR-0081 §4). La regla es
# la de la respuesta del consultor a la PARADA (MARGEN-PENDIENTE.md, 2026-10-31): cada respuesta es
# «si», «no», «no concluyente» o «no medible», y lo que no prueba la causa es «no concluyente».

# M2: la pendiente carga si el margen libre baja al menos esta fraccion del margen calculado al
# mercado; el precio se decide por la mitad de D = |orden - mercado|, si D llega a este minimo (USD)
CARGA_MIN = 0.10
D_MIN = 10.0
# M4: lo que el comentario del historial tiene que decir para atribuir el rechazo al margen.
# ORDER_REASON no tiene ningun valor para el margen (CLIENT, MOBILE, WEB, EXPERT, SL, TP, SO): solo
# ORDER_COMMENT puede nombrarlo, y la documentacion no dice que lo haga.
COMENTARIO_MARGEN = re.compile(r"no money|not enough money|margin|margen", re.IGNORECASE)
ESTADO_RECHAZADA = "ORDER_STATE_REJECTED"


def _numero(filas: Sequence[Fila], clave: str) -> float | None:
    f = _busca(filas, clave)
    if f is None:
        return None
    try:
        return float(f.valor)
    except ValueError:
        return None


def _no_medible(filas: Sequence[Fila], medida: str) -> str | None:
    f = _busca(filas, f"{medida}_no_medible")
    return None if f is None else f"no medible: {f.nota}"


def respuesta_m1(filas: Sequence[Fila]) -> str:
    """M1: ¿rechaza al COLOCAR una pendiente cuyo margen no cabe en el libre?"""
    if (nm := _no_medible(filas, "m1")) is not None:
        return nm
    f = _busca(filas, "m1_colocar")
    if f is None:
        return "sin medir"
    if f.retcode == 10019 and f.colocada == "no":
        return "si: la rechaza al colocar (10019 NO_MONEY)"
    if f.colocada in ("si", "llenada") and f.retcode in (10008, 10009):
        return f"no: la acepta al colocar ({f.retcode} {f.retcode_texto})"
    return f"no concluyente: {f.colocada} ({f.retcode} {f.retcode_texto})"


def respuesta_m2(filas: Sequence[Fila]) -> str:
    """M2: ¿carga margen una stop viva, y a que precio? Por la bajada del margen LIBRE."""
    if (nm := _no_medible(filas, "m2")) is not None:
        return nm
    col = _busca(filas, "m2_colocar")
    if col is None:
        return "sin medir"
    if col.colocada != "si":
        return f"no concluyente: la pendiente no quedo viva ({col.retcode} {col.retcode_texto})"
    claves = (
        "m2_libre_antes",
        "m2_libre_despues",
        "m2_margen_antes",
        "m2_margen_despues",
        "m2_inicial_antes",
        "m2_inicial_despues",
        "m2_calculado_orden",
        "m2_calculado_mercado",
    )
    valores = [_numero(filas, c) for c in claves]
    if any(v is None for v in valores):
        return "no concluyente: faltan las cifras de la cuenta"
    la, ld, ma, md, ia, idp, co, cm = (v for v in valores if v is not None)
    baja = la - ld
    detalle = (
        f"el libre baja {baja:.2f}; ACCOUNT_MARGIN {md - ma:+.2f}; ACCOUNT_MARGIN_INITIAL "
        f"{idp - ia:+.2f}; calculado a la orden {co:.2f} y al mercado {cm:.2f}"
    )
    umbral = CARGA_MIN * cm
    if abs(baja) < umbral:
        return f"no: la pendiente viva no carga margen ({detalle})"
    if baja < 0:
        return f"no concluyente: el libre sube ({detalle})"
    d = abs(co - cm)
    if d < D_MIN:
        return f"si, carga (el precio no se distingue: D = {d:.2f}) ({detalle})"
    if abs(baja - co) < d / 2:
        return f"si, carga al precio de la orden ({detalle})"
    if abs(baja - cm) < d / 2:
        return f"si, carga al precio de mercado ({detalle})"
    return f"no concluyente: carga, pero ni al precio de la orden ni al de mercado ({detalle})"


def respuesta_m3(filas: Sequence[Fila]) -> str:
    """M3: ¿suma MT5 el margen de las pendientes al colocar otra?"""
    if (nm := _no_medible(filas, "m3")) is not None:
        return nm
    c1 = _busca(filas, "m3_colocar_1")
    if c1 is None:
        return "sin medir"
    if c1.colocada != "si":
        return f"no concluyente: la primera no quedo viva ({c1.retcode} {c1.retcode_texto})"
    c2 = _busca(filas, "m3_colocar_2")
    if c2 is None:
        return "no concluyente: falta la segunda"
    if c2.retcode == 10019 and c2.colocada == "no":
        return "si: suma las pendientes al colocar (10019 NO_MONEY en la segunda)"
    if c2.colocada == "si":
        return f"no: no las suma al colocar ({c2.retcode} {c2.retcode_texto})"
    return f"no concluyente: la segunda {c2.colocada} ({c2.retcode} {c2.retcode_texto})"


def respuesta_m4(filas: Sequence[Fila]) -> str:
    """M4: ¿comprueba MT5 el margen al LLENAR? «si» solo con la causa escrita en el historial."""
    oc = _busca(filas, "m4_ocupacion")
    if oc is not None and oc.valor == "no_medible":
        return f"no medible: {oc.nota}"
    if (nm := _no_medible(filas, "m4")) is not None:
        return nm
    res = _busca(filas, "m4_resultado")
    if res is None:
        return "sin medir" if oc is None else "no concluyente: falta el resultado"
    if res.valor not in ("llenada", "sin_deal"):
        return f"no concluyente: {res.valor} ({res.nota})"
    antes, tras_s, tras_o, margen_s = (
        _numero(filas, c)
        for c in (
            "m4_libre_antes_stop",
            "m4_libre_tras_stop",
            "m4_libre_tras_ocupar",
            "m4_margen_stop",
        )
    )
    if antes is None or tras_s is None or tras_o is None or margen_s is None:
        return "no concluyente: faltan las cifras del margen libre"
    reservado = antes - tras_s
    if not tras_o + reservado < margen_s:
        return (
            f"no concluyente: S cabia al llenar (libre {tras_o:.2f} + reservado {reservado:.2f}"
            f" >= margen de S {margen_s:.2f})"
        )
    viva = _busca(filas, "m4_ocupacion_viva")
    if viva is None or viva.valor != "si":
        return "no concluyente: la ocupacion cayo antes de que se resolviera S"
    # el libre leido justo antes de ver resuelta S: se ensena, no decide (la condicion de arriba)
    al_resolver = _busca(filas, "m4_libre_al_resolver")
    libre_final = "sin dato" if al_resolver is None else al_resolver.valor
    if res.valor == "llenada":
        vd, vs = _numero(filas, "m4_volumen_deal"), _numero(filas, "m4_volumen_stop")
        if vd is None or vs is None or vd + 1e-9 < vs:
            return f"no concluyente: llenado parcial ({res.nota})"
        return (
            f"no: la llena sin margen libre (a {res.precio_resultado}; libre al resolver"
            f" {libre_final})"
        )
    estado = _busca(filas, "m4_estado")
    comentario = _busca(filas, "m4_comentario")
    motivo = _busca(filas, "m4_motivo")
    texto_estado = "sin estado" if estado is None else estado.valor
    texto_comentario = "" if comentario is None else comentario.valor
    texto_motivo = "sin motivo" if motivo is None else motivo.valor
    literal = f"{texto_estado}, «{texto_comentario}», {texto_motivo}"
    limite = _numero(filas, "p8_volumen_limite")
    vs, vo = _numero(filas, "m4_volumen_stop"), _numero(filas, "m4_volumen_ocupacion")
    dentro_del_tope = limite == 0.0 or (
        limite is not None and vs is not None and vo is not None and vs + vo <= limite + 1e-9
    )
    if (
        texto_estado == ESTADO_RECHAZADA
        and COMENTARIO_MARGEN.search(texto_comentario)
        and dentro_del_tope
    ):
        return (
            f"si: la rechaza al llenar por el margen ({literal}; libre al resolver {libre_final})"
        )
    return f"no concluyente: S sin deal ({literal})"


def _contexto_paso_8(filas: Sequence[Fila]) -> str:
    partes = [
        ("modo de margen", "p8_modo_margen"),
        ("SYMBOL_MARGIN_HEDGED", "p8_margen_hedged"),
        ("pierna mayor", "p8_hedged_pierna_mayor"),
        ("margen inicial", "p8_margen_inicial"),
        ("tope agregado de volumen", "p8_volumen_limite"),
        ("tasas de margen buy stop", "p8_tasa_buy_stop"),
        ("buy", "p8_tasa_buy"),
    ]
    return "; ".join(f"{nombre} {_dato(clave)(filas)}" for nombre, clave in partes)


def seccion_paso_8(ficheros: dict[str, list[Fila]], nombres: Sequence[str]) -> list[str]:
    """La seccion aparte del paso 8: solo con ficheros 1.2, uno a uno."""
    lineas = [
        "",
        "## Paso 8: cuando comprueba MT5 el margen de una pendiente stop (ADR-0081 §4)",
        "",
        "La regla se escribio antes de ejecutar (MARGEN-PENDIENTE.md). Lo que no prueba la causa es"
        " «no concluyente».",
    ]
    for n in nombres:
        filas = ficheros[n]
        lineas += ["", f"### {n}", ""]
        fin = _busca(filas, "p8_fin")
        if fin is not None and fin.valor == "desactivado":
            lineas.append("- paso 8 desactivado (InpMedirMargen = false)")
            continue
        if fin is None and not any(f.medicion == "8_margen" for f in filas):
            lineas.append("- el paso 8 no corrio")
            continue
        lineas += [
            f"- contexto: {_contexto_paso_8(filas)}",
            f"- M1 · rechaza al colocar una pendiente sin margen libre: {respuesta_m1(filas)}",
            f"- M2 · una stop viva carga margen, y a que precio: {respuesta_m2(filas)}",
            f"- M3 · suma las pendientes al colocar otra: {respuesta_m3(filas)}",
            f"- M4 · comprueba el margen al llenar: {respuesta_m4(filas)}",
        ]
        for medida in ("m1", "m2", "m3", "m4"):
            f = _busca(filas, f"{medida}_peor_caso")
            if f is not None:
                lineas.append(f"- peor caso {medida.upper()}: {f.valor} USD ({f.nota})")
        if fin is None:
            lineas.append("- SIN LA FILA p8_fin (cortado)")
        elif fin.valor == "detenido":
            lineas.append(f"- PASO 8 DETENIDO: {fin.nota}")
    return lineas


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

    # 1.2: el paso 8, en su seccion; sin ficheros 1.2 no se escribe nada (salida igual que en 1.1)
    con_paso_8 = [n for n in nombres if ficheros[n] and ficheros[n][0].version == VERSION_PASO_8]
    if con_paso_8:
        lineas += seccion_paso_8(ficheros, con_paso_8)

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
