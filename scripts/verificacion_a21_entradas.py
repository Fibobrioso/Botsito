"""Verificacion de la medida «entrada dentro de la zona» (A-21) sobre construccion, operacion por
operacion, en DIAGNOSTICO (A-35 cierre_vela_contraria, A-44 sin_tope, A-21 cada lectura). Segunda
tarea de `trabajo/preparar-a21`. Descriptivo: no cambia la geometria ni elige lectura.

Supuestos de la medida, escritos aqui porque son la medida:
- LA ZONA: la que el productor del motor tiene VIVA en el instante del llenado del trader: el
  esquema detectado desde la PRIMERA toma del dia (`liquidez_tomada` no caduca al abrir la sesion),
  con las M1 anteriores al llenado, con la lectura de A-21 dada. El lado de la zona lo fija el
  sesgo de H4 de la sesion (RN-005), NO la direccion del trader: si el trader va al reves, se dice.
- EL PRECIO: `entrada` del caso (`entryPrice` del backtest, F14a), que en un backtest de ordenes
  limite es el precio LIMITE de la orden y su llenado a la vez; el instante del caso es el llenado
  (INSTANTE-LLENADO-SALIDA.txt). No hay otro precio de ejecucion en el material.
- LA TOLERANCIA: `tolerancia_entrada_puntos` del criterio de fidelidad (ADR-0043), leida del
  fichero, no escrita aqui. «Dentro» es d <= 0 (sin tolerancia); «en el borde» es 0 < d <= tol.
- LA DISTANCIA FIRMADA d: entrada del trader menos el borde CERCANO de la zona, con el signo puesto
  de modo que d > 0 es «fuera, del lado del precio», d en [-caja, 0] es dentro, y d < -caja es
  «mas alla del extremo». Para una compra d = entrada_trader - borde; para una venta al reves.

  `uv run python scripts/verificacion_a21_entradas.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import UTC
from decimal import Decimal
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.cases.ventanas import MINUTOS_M15  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.agregacion import agregar  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie  # noqa: E402
from botsito.domain.estructura_m1 import (  # noqa: E402
    COMPRA,
    LECTURAS_LIMPIA,
    Esquema,
    detectar_esquema,
)
from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA  # noqa: E402
from botsito.domain.sesgo import sesgo_h4  # noqa: E402
from botsito.domain.valores import HoraLocal  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico  # noqa: E402
from botsito.engine.interprete import Interprete, reglas_ejecutables  # noqa: E402
from botsito.engine.motor import DatosMercado, MotorSpec, _minuto_utc  # noqa: E402
from botsito.engine.perfil_cuenta import cargar_perfil  # noqa: E402
from botsito.engine.primitivas import primitivas_escritas  # noqa: E402
from botsito.engine.tope_trader import tope_del_registro  # noqa: E402
from botsito.engine.visor import _stops  # noqa: E402
from botsito.engine.zonas import LADO_ENTRADA, LOOKBACK_M1  # noqa: E402
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario  # noqa: E402

# Las categorias de la fase 2, en el orden en que se prueban; la primera que casa manda, y se
# listan todas las que casan. Descriptivo: ninguna cambia la geometria.
DENTRO = "dentro"
BORDE = "en el borde (<= tolerancia)"
MAS_ALLA = "mas alla del extremo"
CUERPO = "el cuerpo y no la mecha"
LEJANO_O_MEDIO = "el borde lejano o el medio"
GRUPO = "un grupo de velas contrarias (bloque mayor)"
OTRA_VELA = "otra vela contraria entre la toma y el breaker"
M15_BLOQUE = "desfase de temporalidad (la M15 del bloque)"
ANTERIOR = "otra zona anterior a la toma"
NO_SE_SABE = "no se sabe"


def _minuto(instante) -> int:  # type: ignore[no-untyped-def]
    return int(instante.astimezone(UTC).timestamp() // 60)


def _hhmm(minuto: int) -> str:
    return f"{(minuto // 60) % 24:02d}:{minuto % 60:02d}"


def _contraria(v: Vela, lado: str) -> bool:
    return int(v.cierre) < int(v.abierta) if lado == COMPRA else int(v.cierre) > int(v.abierta)


def _en(rango: tuple[int, int], precio: int, tol: int) -> bool:
    lo, hi = min(rango), max(rango)
    return lo - tol <= precio <= hi + tol


def _rango(velas: list[Vela]) -> tuple[int, int]:
    return min(int(v.minima) for v in velas), max(int(v.maxima) for v in velas)


def _distancia(e: Esquema, precio: int) -> int:
    """d > 0: fuera, del lado del precio; -caja <= d <= 0: dentro; d < -caja: mas alla del
    extremo."""
    return precio - e.entrada if e.lado == COMPRA else e.entrada - precio


def _clasificar(
    e: Esquema, m1: list[Vela], idx_toma: int, precio: int, tol: int, anclaje: HoraLocal
) -> list[str]:
    d = _distancia(e, precio)
    caja = e.caja
    if -caja <= d <= 0:
        return [DENTRO]
    if 0 < d <= tol:
        return [BORDE]
    causas: list[str] = []
    if d < -caja:
        causas.append(MAS_ALLA)
    idx_b0 = next(k for k, v in enumerate(m1) if v.inicio == e.bloque_inicio)
    idx_b1 = next(k for k, v in enumerate(m1) if v.fin == e.bloque_fin)  # inclusive
    idx_br = next(k for k, v in enumerate(m1) if v.fin == e.breaker_fin)
    bloque = m1[idx_b0 : idx_b1 + 1]
    # el cuerpo del bloque (sin mechas)
    cuerpo = (
        min(min(int(v.abierta), int(v.cierre)) for v in bloque),
        max(max(int(v.abierta), int(v.cierre)) for v in bloque),
    )
    borde_cuerpo = cuerpo[1] if e.lado == COMPRA else cuerpo[0]
    if abs(precio - borde_cuerpo) <= tol:
        causas.append(CUERPO)
    medio = (e.entrada + e.extremo) // 2
    if abs(precio - e.extremo) <= tol or abs(precio - medio) <= tol:
        causas.append(LEJANO_O_MEDIO)
    # el grupo: las contrarias consecutivas que acaban en el bloque
    k = idx_b0 - 1
    while k > idx_toma and _contraria(m1[k], e.lado):
        k -= 1
    grupo = m1[k + 1 : idx_b1 + 1]
    if len(grupo) > len(bloque) and _en(_rango(grupo), precio, tol):
        causas.append(GRUPO)
    otras = [
        v
        for j, v in enumerate(m1)
        if idx_toma < j < idx_br and not (idx_b0 <= j <= idx_b1) and _contraria(v, e.lado)
    ]
    if any(_en((int(v.minima), int(v.maxima)), precio, tol) for v in otras):
        causas.append(OTRA_VELA)
    m15 = agregar(list(m1), MINUTOS_M15, anclaje)
    del_bloque = [v for v in m15 if v.inicio <= e.bloque_inicio < v.fin]
    if del_bloque and _en(_rango(del_bloque), precio, tol):
        causas.append(M15_BLOQUE)
    previas = [v for j, v in enumerate(m1) if j <= idx_toma and _contraria(v, e.lado)]
    if any(_en((int(v.minima), int(v.maxima)), precio, tol) for v in previas):
        causas.append(ANTERIOR)
    return causas or [NO_SE_SABE]


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: verificacion_a21_entradas.py --salida <fichero>", file=sys.stderr)
        return 2
    criterio = cargar_criterio(RAIZ)
    tol = criterio.tolerancias.entrada_puntos
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    huso = registro.texto("huso_operativa")
    anclaje = registro.hora("anclaje_h4")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    carpeta = carpeta_datos(RAIZ)
    mercado = arnes.dias_de_mercado(
        RAIZ, carpeta, config, registro, dias, huso, CIERRE_VELA_CONTRARIA
    )
    ruta = buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{criterio.construccion[0]}")
    escala = cargar_serie(cargar_manifiesto(ruta), carpeta).escala
    spec = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
    voc, reglas = cargar_vocabulario(spec), reglas_ejecutables(cargar_reglas(spec))
    perfil = next(iter(sorted((RAIZ / "knowledge" / "cuentas").glob("*.yaml"))))
    tope = tope_del_registro(
        registro, cargar_perfil(perfil).huso_corte(), Diagnostico(a44=A44_SIN_TOPE)
    )
    tope_zonas = registro.entero("zonas_control_max_por_esquema")
    criterio_breaker = registro.opcion("breaker_m1_criterio_ruptura")
    tope_sesgo = registro.entero("sesgo_h4_tope_velas")
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    n_ops = sum(len(d.operaciones) for d in dias)
    lineas = [
        "# Verificacion A-21, entradas: distancia firmada al borde cercano de la zona viva, y "
        "causa",
        f"CONJUNTO: construccion ({', '.join(criterio.construccion)}); dias {len(dias)}; "
        f"operaciones del trader {n_ops}",
        f"TOLERANCIA (ADR-0043, criterio_fidelidad.yaml): {tol} puntos; escala {escala}",
        "HIPOTESIS: A-35 cierre_vela_contraria; A-44 sin_tope; A-21 cada lectura. Descriptivo: "
        "no elige lectura ni cambia la geometria.",
        "d = entrada del trader - borde cercano (compra) o al reves (venta): d > 0 fuera del lado "
        "del precio; -caja <= d <= 0 dentro; d < -caja mas alla del extremo.",
        "",
    ]
    for limpia in LECTURAS_LIMPIA:
        motor = MotorSpec(Interprete(voc, primitivas_escritas(registro, tope, limpia)), reglas)
        distancias: list[int] = []
        causas_primeras: Counter[str] = Counter()
        causas_todas: Counter[str] = Counter()
        sin_zona: Counter[str] = Counter()
        contrarias = 0
        toma_otra_sesion_ops = 0
        filas: list[str] = []
        geometria: list[str] = []
        stop_mayor_que_caja = con_stop = 0
        # fase 3: sesiones que usan una toma de una sesion ANTERIOR del dia
        ses_posteriores = ses_rn011_toma_ajena = ses_rn008_o_9_toma_ajena = 0
        ops_en_ses_posteriores = 0
        for d in dias:
            dm = mercado[d.dia]
            datos: DatosMercado = dm.datos
            r = motor.correr_dia(dm)
            aperturas = {s.nombre: int(_minuto_utc(dm.dia, s.desde, huso)) for s in dm.sesiones}
            tomas = sorted(
                (t, nombre)
                for nombre, tz in r.sesiones.items()
                for t, _, h, _ in tz.fijados
                if h == "liquidez_tomada"
            )
            toma_dia = tomas[0] if tomas else None
            if toma_dia is not None:
                for nombre in sorted(aperturas, key=aperturas.get):  # type: ignore[arg-type]
                    if aperturas[nombre] > toma_dia[0] and nombre != toma_dia[1]:
                        ses_posteriores += 1
                        tz = r.sesiones[nombre]
                        if "RN-011" in tz.disparadas:
                            ses_rn011_toma_ajena += 1
                        if tz.disparadas & {"RN-008", "RN-009"}:
                            ses_rn008_o_9_toma_ajena += 1
                        ops_en_ses_posteriores += sum(
                            1 for op in d.operaciones if op.sesion == nombre
                        )
            stops = _stops(RAIZ, d)
            for op, stop in zip(d.operaciones, stops, strict=True):
                t_ap = aperturas.get(op.sesion)
                t_op = _minuto(op.instante)
                hora = op.instante.astimezone(UTC).strftime("%H:%M")
                etiqueta = f"{d.dia} {op.sesion} {hora}Z {op.direccion}"
                precio = int((Decimal(op.entrada) * escala).to_integral_value())
                d_stop = (
                    abs(int(((Decimal(op.entrada) - stop) * escala).to_integral_value()))
                    if stop is not None
                    else None
                )
                if t_ap is None:
                    sin_zona["sesion fuera de la ventana"] += 1
                    filas.append(f"- {etiqueta}: SIN ZONA (sesion fuera de la ventana)")
                    continue
                if toma_dia is None or toma_dia[0] > t_op:
                    sin_zona["sin toma antes del llenado"] += 1
                    filas.append(f"- {etiqueta}: SIN ZONA (RN-004 no habia tomado liquidez)")
                    continue
                toma, toma_sesion = toma_dia
                # el lado de la zona: el sesgo de la sesion de la TOMA, como lo anota el productor
                t_toma_ap = aperturas[toma_sesion]
                sesgo = sesgo_h4(
                    datos.velas_h4_cerradas(t_toma_ap),
                    MinutoUtc(t_toma_ap),
                    tope_sesgo,
                    criterio_ruptura,
                ).sesgo.value
                lado = LADO_ENTRADA.get(sesgo)
                if lado is None:
                    sin_zona[f"sin lado: sesgo {sesgo} en la sesion de la toma"] += 1
                    filas.append(f"- {etiqueta}: SIN ZONA (sesgo {sesgo} en la sesion de la toma)")
                    continue
                m1 = datos.m1_entre(toma - LOOKBACK_M1, t_op)
                idx = next((k for k, v in enumerate(m1) if int(v.fin) == toma), None)
                e = (
                    detectar_esquema(m1, idx, lado, criterio_breaker, tope_zonas, limpia)
                    if idx is not None
                    else None
                )
                if e is None:
                    sin_zona["toma sin esquema antes del llenado (o rechazado por la lectura)"] += 1
                    filas.append(
                        f"- {etiqueta}: SIN ZONA (toma a las {_hhmm(toma)}Z en {toma_sesion}, sin "
                        "esquema valido antes del llenado)"
                    )
                    continue
                dist = _distancia(e, precio)
                distancias.append(dist)
                causas = _clasificar(e, m1, idx, precio, tol, anclaje)  # type: ignore[arg-type]
                causas_primeras[causas[0]] += 1
                for c in causas:
                    causas_todas[c] += 1
                contraria = op.direccion != e.lado
                contrarias += contraria
                ajena = toma_sesion != op.sesion
                toma_otra_sesion_ops += ajena
                if d_stop is not None:
                    geometria.append(f"{e.caja}:{d_stop}")
                    con_stop += 1
                    stop_mayor_que_caja += d_stop > e.caja
                filas.append(
                    f"- {etiqueta}: zona {e.lado} {e.cual} caja {e.caja} formada "
                    f"{_hhmm(int(e.breaker_fin))}Z; d = {dist:+d}; stop del trader "
                    f"{d_stop if d_stop is not None else '-'}; causa: {' | '.join(causas)}"
                    f"{'; DIRECCION CONTRARIA a la zona' if contraria else ''}"
                    f"{'; toma de la sesion ' + toma_sesion if ajena else ''}"
                )
        n_zona = len(distancias)
        dentro = sum(1 for x in distancias if x <= 0)
        borde = sum(1 for x in distancias if 0 < x <= tol)
        lineas += [
            f"## A-21 = {limpia} (DIAGNOSTICO-A21-{limpia})",
            f"operaciones con zona viva en el llenado: {n_zona} de {n_ops}; sin zona: "
            f"{n_ops - n_zona} -> {dict(sin_zona)}",
            f"  d <= 0 (dentro, incluye mas alla del extremo): {dentro}; 0 < d <= {tol} (borde): "
            f"{borde}; d > {tol}: {n_zona - dentro - borde}",
            "  distribucion de d (puntos): "
            + (
                f"min {min(distancias)}, p25 {sorted(distancias)[len(distancias) // 4]}, mediana "
                f"{median(distancias)}, p75 {sorted(distancias)[3 * len(distancias) // 4]}, max "
                f"{max(distancias)}"
                if distancias
                else "ninguna"
            ),
            f"  en direccion contraria a la zona: {contrarias}; con la toma hecha en otra sesion "
            f"del dia: {toma_otra_sesion_ops}",
            f"  causa mas probable (la primera que casa): {dict(causas_primeras)}",
            "  todas las causas que casan (una operacion puede sumar en varias): "
            f"{dict(causas_todas)}",
            "  geometria caja_motor:distancia_entrada_stop_trader por operacion: "
            + " ".join(geometria),
            f"  el stop del trader esta MAS LEJOS que la caja entera del motor en "
            f"{stop_mayor_que_caja} de {con_stop} (el motor pondria el suyo a stop_fraccion_caja "
            "de la caja, mas cerca)",
            f"FASE 3: sesiones posteriores a la primera toma del dia: {ses_posteriores}; de ellas, "
            f"RN-011 dispara con esa toma ajena en {ses_rn011_toma_ajena} y RN-008 o RN-009 en "
            f"{ses_rn008_o_9_toma_ajena}; operaciones del trader en esas sesiones: "
            f"{ops_en_ses_posteriores}",
            *filas,
            "",
        ]
    Path(argv[1]).write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
