"""¿Que vela o velas de M1 elige el trader como bloque de su caja? Rama `trabajo/bloque-de-la-caja`,
2026-09-28. Descriptivo: no cambia el motor, ni el productor, ni la spec.

El criterio esta en docs/validation/BLOQUE-DE-LA-CAJA.md §1, escrito y commiteado antes de medir.
Las CAJAS son lecturas de pantalla (fotogramas de v7 y v8 por instante localizado, ADR-0038): el 0,
el 1, la hora de colocacion en el reloj del grafico (UTC+2 fijo) y la direccion. Las VELAS son las
M1 de Dukascopy del repositorio (BID, UTC). FX Replay dibuja OANDA: 1-2 puntos de diferencia (A-16).

Fase 2: que velas de la ventana [T - 90 min, T) dan el 0 y el 1 a <= tau (tau 1, 2 y 3).
Fase 3: seis reglas candidatas (R1-R6) y la zona del productor en T, frente al 0 y el 1 del trader.

    uv run python scripts/bloque_de_la_caja.py --salida <fichero>
"""

from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.holdout import casos_ocultos, casos_reservados  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_ventana  # noqa: E402
from botsito.domain.estructura_m1 import (  # noqa: E402
    LECTURAS_LIMPIA,
    VENTA,
    Esquema,
    detectar_esquema,
)
from botsito.domain.pivotes_m15 import (  # noqa: E402
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    color,
    pivotes_formados,
)
from botsito.domain.sesgo import sesgo_h4  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico  # noqa: E402
from botsito.engine.interprete import Interprete, reglas_ejecutables  # noqa: E402
from botsito.engine.motor import MotorSpec, _minuto_utc  # noqa: E402
from botsito.engine.perfil_cuenta import cargar_perfil  # noqa: E402
from botsito.engine.primitivas import primitivas_escritas  # noqa: E402
from botsito.engine.tope_trader import tope_del_registro  # noqa: E402
from botsito.engine.zonas import LADO_ENTRADA, LOOKBACK_M1  # noqa: E402
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario  # noqa: E402

ESCALA = 100000
VENTANA_MIN = 90
TAUS = (1, 2, 3)
TAU = 2
PANTALLA = timedelta(hours=2)  # el reloj de FX Replay es UTC+2 fijo (CLAUDE.md)
# la primera toma de liquidez de M15 del dia segun el productor (A-35 en diagnostico), por caja
TOMAS: dict[str, int | None] = {}


@dataclass(frozen=True)
class Caja:
    """Una caja leida en pantalla (docs/validation/BLOQUE-DE-LA-CAJA.md §2)."""

    op: str
    dia: str
    colocacion_pantalla: str  # HH:MM:SS en UTC+2
    direccion: str
    cero: str
    uno: str
    fotograma: str

    @property
    def t_utc(self) -> datetime:
        local = datetime.fromisoformat(f"{self.dia}T{self.colocacion_pantalla}")
        return (local - PANTALLA).replace(tzinfo=UTC)

    def puntos(self, precio: str) -> int:
        return int((Decimal(precio) * ESCALA).to_integral_value())


# Las 12 cajas legibles, leidas el 2026-09-28 (notas en el informe, §2). La hora es la del primer
# fotograma que ensena la etiqueta de la orden, en el reloj del grafico.
CAJAS = (
    Caja("v7-1", "2026-08-03", "07:47:59", VENTA, "1.15358", "1.15370", "v7/000227000"),
    Caja("v7-2", "2026-08-03", "08:00:59", VENTA, "1.15352", "1.15376", "v7/000404000"),
    Caja("v7-3", "2026-08-03", "08:06:59", VENTA, "1.15364", "1.15389", "v7/000510000"),
    Caja("v7-4", "2026-08-03", "09:33:59", VENTA, "1.15306", "1.15322", "v7/000710000"),
    Caja("v7-5", "2026-08-03", "11:46:59", VENTA, "1.15274", "1.15290", "v7/000955000"),
    Caja("v7-7", "2026-08-03", "13:11:59", VENTA, "1.15256", "1.15268", "v7/001210000"),
    Caja("v7-9", "2026-08-03", "14:09:59", VENTA, "1.15338", "1.15352", "v7/001535000"),
    Caja("v7-10", "2026-08-04", "09:44:59", VENTA, "1.15129", "1.15172", "v7/001930000"),
    Caja("v7-11", "2026-08-04", "13:32:59", VENTA, "1.15184", "1.15210", "v7/002110000"),
    Caja("v7-12", "2026-08-04", "13:56:59", VENTA, "1.15174", "1.15234", "v7/002180000"),
    Caja("v7-15", "2026-08-06", "08:01:59", VENTA, "1.15491", "1.15516", "v7/002654000"),
    Caja("v8-1", "2026-08-12", "08:35:59", VENTA, "1.15354", "1.15362", "v8/000200000"),
)


# ------------------------------------------------------------------------------------ utilidades


def hhmm(m: int) -> str:
    return f"{(m // 60) % 24:02d}:{m % 60:02d}"


def contraria(v: Vela, lado: str) -> bool:
    """La vela del color contrario a la entrada: alcista en una venta, bajista en una compra."""
    return color(v) == (1 if lado == VENTA else -1)


def del_color_de_la_entrada(v: Vela, lado: str) -> bool:
    return color(v) == (-1 if lado == VENTA else 1)


def cero_uno(velas: Sequence[Vela], lado: str) -> tuple[int, int]:
    """El 0 y el 1 de una caja trazada sobre `velas`: en una venta el minimo y el maximo."""
    lo, hi = min(int(v.minima) for v in velas), max(int(v.maxima) for v in velas)
    return (lo, hi) if lado == VENTA else (hi, lo)


def describe(v: Vela) -> str:
    c = {1: "verde", -1: "roja", 0: "sin cuerpo"}[color(v)]
    return f"{hhmm(int(v.inicio))} UTC ({hhmm(int(v.inicio) + 120)} UTC+2) {c}"


def que_da(v: Vela, nivel: int, tau: int) -> str | None:
    """Que extremo de la vela da el nivel (mecha si es la maxima o la minima, cuerpo si es la
    apertura o el cierre), o None."""
    partes = []
    if abs(int(v.minima) - nivel) <= tau:
        partes.append(f"minima {int(v.minima) - nivel:+d}")
    if abs(int(v.maxima) - nivel) <= tau:
        partes.append(f"maxima {int(v.maxima) - nivel:+d}")
    cuerpo = [x for x in (int(v.abierta), int(v.cierre)) if abs(x - nivel) <= tau]
    if cuerpo and not partes:
        partes.append(f"cuerpo {cuerpo[0] - nivel:+d}")
    return ", ".join(partes) or None


# ------------------------------------------------------------------------------------ las reglas


def r1(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R1 · la ultima vela contraria antes de T (bloque_de_origen anclado en la colocacion)."""
    k = ultima_contraria(velas, lado)
    return None if k is None else cero_uno([velas[k]], lado)


def ultima_contraria(velas: Sequence[Vela], lado: str) -> int | None:
    for k in range(len(velas) - 1, -1, -1):
        if contraria(velas[k], lado):
            return k
    return None


def r2(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R2 · la vela de R1 y la siguiente, si la siguiente la cubre con la mecha (pasa su extremo
    del lado de la entrada: por debajo en una venta)."""
    k = ultima_contraria(velas, lado)
    if k is None or k + 1 >= len(velas):
        return None
    a, b = velas[k], velas[k + 1]
    cubre = int(b.minima) < int(a.minima) if lado == VENTA else int(b.maxima) > int(a.maxima)
    return cero_uno([a, b], lado) if cubre else None


def r3(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R3 · la ultima envolvente del color de la entrada: maxima >= y minima <= las de la
    anterior."""
    for k in range(len(velas) - 1, 0, -1):
        v, p = velas[k], velas[k - 1]
        envuelve = int(v.maxima) >= int(p.maxima) and int(v.minima) <= int(p.minima)
        if envuelve and del_color_de_la_entrada(v, lado):
            return cero_uno([v], lado)
    return None


def r4(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R4 · la racha de contrarias consecutivas que termina en la vela de R1."""
    k = ultima_contraria(velas, lado)
    if k is None:
        return None
    j = k
    while j - 1 >= 0 and contraria(velas[j - 1], lado):
        j -= 1
    return cero_uno(velas[j : k + 1], lado)


def pivote_de_ruptura(velas: Sequence[Vela], lado: str) -> tuple[int, int, int] | None:
    """El ultimo pivote de M1 contrario a la entrada formado con `velas` (un BAJO en una venta):
    (nivel, indice de la vela que marca el nivel, indice de la contraria que lo forma)."""
    if not velas:
        return None
    buscado = BAJO if lado == VENTA else ALTO
    instante = int(velas[-1].fin)
    for p in reversed(pivotes_formados(velas, None, CIERRE_VELA_CONTRARIA, instante, len(velas))):
        if p.lado != buscado:
            continue
        ic = next(
            (i for i, v in enumerate(velas) if int(v.inicio) == int(p.contraria_inicio)), None
        )
        if ic is None:
            return None
        extremo = (lambda v: int(v.minima)) if lado == VENTA else (lambda v: int(v.maxima))
        il = next((i for i in range(ic, -1, -1) if extremo(velas[i]) == p.nivel), ic)
        return p.nivel, il, ic
    return None


def r5(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R5 · la vela del pivote de M1 cuya ruptura da la entrada: 0 = el nivel del pivote; 1 = el
    extremo opuesto de las velas desde la que marca el nivel hasta la contraria que lo forma."""
    p = pivote_de_ruptura(velas, lado)
    if p is None:
        return None
    nivel, il, ic = p
    _, uno = cero_uno(velas[il : ic + 1], lado)
    return nivel, uno


def r6(velas: Sequence[Vela], lado: str) -> tuple[int, int] | None:
    """R6 · del punto de breaker (el nivel de R5) al punto mas alto (mas bajo en una compra) de
    las velas entre ese pivote y T."""
    p = pivote_de_ruptura(velas, lado)
    if p is None:
        return None
    nivel, il, _ = p
    _, uno = cero_uno(velas[il:], lado)
    return nivel, uno


REGLAS = {"R1": r1, "R2": r2, "R3": r3, "R4": r4, "R5": r5, "R6": r6}


# ------------------------------------------------------------------------------------ productor


def zonas_del_productor(dias_caja: set[str]) -> dict[tuple[str, str], Esquema | str]:
    """La zona que el productor tiene viva en T para cada caja y cada lectura de A-21, con los
    supuestos de scripts/verificacion_a21_entradas.py (DIAGNOSTICO: A-35 cierre_vela_contraria,
    A-44 sin_tope). Devuelve el esquema o el motivo de que no haya zona."""
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    huso = registro.texto("huso_operativa")
    dias = [
        d
        for d in arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
        if d.dia in dias_caja
    ]
    mercado = arnes.dias_de_mercado(
        RAIZ, carpeta_datos(RAIZ), config, registro, dias, huso, CIERRE_VELA_CONTRARIA
    )
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
    salida: dict[tuple[str, str], Esquema | str] = {}
    for limpia in LECTURAS_LIMPIA:
        motor = MotorSpec(Interprete(voc, primitivas_escritas(registro, tope, limpia)), reglas)
        for d in dias:
            dm = mercado[d.dia]
            r = motor.correr_dia(dm)
            aperturas = {s.nombre: int(_minuto_utc(dm.dia, s.desde, huso)) for s in dm.sesiones}
            tomas = sorted(
                (t, n)
                for n, tz in r.sesiones.items()
                for t, _, h, _ in tz.fijados
                if h == "liquidez_tomada"
            )
            for c in CAJAS:
                if c.dia != d.dia:
                    continue
                t_min = int(c.t_utc.timestamp() // 60)
                TOMAS[c.op] = tomas[0][0] if tomas else None
                if not tomas or tomas[0][0] > t_min:
                    salida[(c.op, limpia)] = "sin toma de M15 antes de T"
                    continue
                toma, toma_sesion = tomas[0]
                t_ap = aperturas[toma_sesion]
                sesgo = sesgo_h4(
                    dm.datos.velas_h4_cerradas(t_ap), MinutoUtc(t_ap), tope_sesgo, criterio_ruptura
                ).sesgo.value
                lado = LADO_ENTRADA.get(sesgo)
                if lado is None:
                    salida[(c.op, limpia)] = f"sesgo {sesgo}"
                    continue
                m1 = dm.datos.m1_entre(toma - LOOKBACK_M1, t_min)
                idx = next((k for k, v in enumerate(m1) if int(v.fin) == toma), None)
                e = (
                    detectar_esquema(m1, idx, lado, criterio_breaker, tope_zonas, limpia)
                    if idx is not None
                    else None
                )
                salida[(c.op, limpia)] = (
                    e if e is not None else f"toma {hhmm(toma)} UTC sin esquema antes de T"
                )
                if e is not None and e.lado != c.direccion:
                    salida[(c.op, limpia)] = f"zona de {e.lado}, contraria a la orden"
    return salida


# ------------------------------------------------------------------------------------ informe


# Las leyendas OHLC del grafico en el fotograma de cada caja: la vela en curso en ese instante (el
# fotograma cae en el segundo :59, asi que le falta un segundo para cerrar). Sirven para medir la
# diferencia OANDA - Dukascopy sobre la misma vela (A-16), vela a vela.
LEYENDAS = (
    ("v7-1", "2026-08-03", "07:47", "1.15364", "1.15370", "1.15359", "1.15369"),
    ("v7-2", "2026-08-03", "08:00", "1.15372", "1.15380", "1.15364", "1.15379"),
    ("v7-3", "2026-08-03", "08:06", "1.15384", "1.15384", "1.15371", "1.15374"),
    ("v7-4", "2026-08-03", "09:33", "1.15310", "1.15322", "1.15308", "1.15316"),
    ("v7-5", "2026-08-03", "11:46", "1.15288", "1.15288", "1.15270", "1.15281"),
    ("v7-7", "2026-08-03", "13:11", "1.15265", "1.15268", "1.15260", "1.15262"),
    ("v7-9", "2026-08-03", "14:24", "1.15344", "1.15351", "1.15320", "1.15322"),
    ("v7-10", "2026-08-04", "09:44", "1.15102", "1.15104", "1.15099", "1.15101"),
    ("v7-11", "2026-08-04", "13:39", "1.15188", "1.15200", "1.15188", "1.15198"),
    ("v7-12", "2026-08-04", "13:56", "1.15194", "1.15194", "1.15160", "1.15160"),
    ("v7-15", "2026-08-06", "08:07", "1.15491", "1.15492", "1.15486", "1.15486"),
    ("v8-1", "2026-08-12", "08:37", "1.15351", "1.15360", "1.15350", "1.15350"),
)
VERSIONES = (
    ("v1 · criterio de §1: M1 CERRADAS antes de T", False, False),
    ("v2 · nota del 2026-09-28: incluida la M1 en curso en T (le falta 1 s)", True, False),
    (
        "v3 · nota del 2026-09-28: v2 con los niveles del trader corregidos por el desfase OANDA - "
        "Dukascopy medido en las leyendas",
        True,
        True,
    ),
)
LEYENDA_BAJO_EL_CURSOR = (
    10  # puntos: mas que eso en los cuatro valores no es un desfase de proveedor
)


def minuto_utc(dia: str, hhmm_pantalla: str) -> int:
    local = datetime.fromisoformat(f"{dia}T{hhmm_pantalla}:00")
    return int((local - PANTALLA).replace(tzinfo=UTC).timestamp() // 60)


def control_de_proveedor(todas: Sequence[Vela]) -> tuple[list[str], int]:
    """OANDA (la leyenda del grafico) frente a Dukascopy (el repositorio) en la misma vela."""
    por_minuto = {int(v.inicio): v for v in todas}
    salida = [
        "## CONTROL DE PROVEEDOR · la vela en curso de cada fotograma, OANDA (leyenda) - Dukascopy",
        "| caja | vela (UTC+2 / UTC) | dO | dH | dL | dC |",
        "|---|---|---|---|---|---|",
    ]
    difs: list[int] = []
    excluidas: list[str] = []
    for op, dia, hm, *ohlc in LEYENDAS:
        m = minuto_utc(dia, hm)
        v = por_minuto.get(m)
        if v is None:
            salida.append(f"| {op} | {hm} / {hhmm(m)} | sin vela en el repositorio | | | |")
            continue
        oanda = [int((Decimal(x) * ESCALA).to_integral_value()) for x in ohlc]
        duka = [int(v.abierta), int(v.maxima), int(v.minima), int(v.cierre)]
        d = [a - b for a, b in zip(oanda, duka, strict=True)]
        fila = f"| {op} | {hm} / {hhmm(m)} | " + " | ".join(f"{x:+d}" for x in d) + " |"
        if any(abs(x) > LEYENDA_BAJO_EL_CURSOR for x in d):
            excluidas.append(op)
            salida.append(fila[:-1] + " EXCLUIDA: leyenda de la vela bajo el cursor |")
            continue
        difs += d
        salida.append(fila)
    a = sorted(abs(x) for x in difs)
    salida.append(
        f"excluidas {len(excluidas)} ({', '.join(excluidas)}): algun valor difiere mas de "
        f"{LEYENDA_BAJO_EL_CURSOR} puntos, porque la leyenda de TradingView ensena la vela que "
        "esta bajo el cursor, no la vela en curso"
    )
    salida.append(
        f"{len(difs)} valores: |OANDA - Dukascopy| mediana {a[len(a) // 2]}, maximo {a[-1]}; "
        f"<= 1: {sum(1 for x in a if x <= 1)}; <= 2: {sum(1 for x in a if x <= 2)}; "
        f"> 3: {sum(1 for x in a if x > 3)}; media con signo {sum(difs) / len(difs):+.1f}"
    )
    return [*salida, ""], sorted(difs)[len(difs) // 2]


def fases(
    todas: Sequence[Vela],
    en_curso: bool,
    titulo: str,
    productor: dict[tuple[str, str], Esquema | str],
    desfase: int = 0,
) -> tuple[list[str], dict[str, Counter[str]]]:
    lineas = [f"# {titulo}", "", "## FASE 2 · que velas dan el 0 y el 1 del trader (tau 2)"]
    ventanas: dict[str, list[Vela]] = {}
    for c in CAJAS:
        t_min = int(c.t_utc.timestamp() // 60)
        tope = t_min + 1 if en_curso else t_min
        velas = [v for v in todas if t_min - VENTANA_MIN <= int(v.inicio) and int(v.fin) <= tope]
        ventanas[c.op] = velas
        cero, uno = c.puntos(c.cero) - desfase, c.puntos(c.uno) - desfase
        lineas.append(
            f"### {c.op} · {c.dia} · colocacion {c.colocacion_pantalla} UTC+2 "
            f"({c.t_utc.strftime('%H:%M:%S')} UTC) · {c.direccion} · 0 = {c.cero} · 1 = "
            f"{c.uno} · caja {abs(uno - cero)} puntos · {c.fotograma}"
        )
        toma = TOMAS.get(c.op)
        lineas.append(
            "- primera toma de M15 del dia (productor, A-35 en diagnostico): "
            + (f"{hhmm(toma)} UTC ({hhmm(toma + 120)} UTC+2)" if toma is not None else "ninguna")
        )
        for nombre, nivel in (("0", cero), ("1", uno)):
            dan = [(v, q) for v in velas if (q := que_da(v, nivel, TAU)) is not None]
            if not dan:
                lineas.append(f"- el {nombre}: SIN EXPLICACION (ninguna vela a <= {TAU} puntos)")
                continue
            lineas.append(
                f"- el {nombre}: {len(dan)} velas; "
                + "; ".join(f"{describe(v)}: {q}" for v, q in dan[-6:])
                + (" (se listan las 6 mas recientes)" if len(dan) > 6 else "")
            )
    lineas += ["", "## FASE 3 · que regla da el mismo 0 y el mismo 1 (a <= tau)"]
    aciertos: dict[str, Counter[str]] = {
        r: Counter() for r in (*REGLAS, "productor a", "productor b")
    }
    for c in CAJAS:
        cero, uno = c.puntos(c.cero) - desfase, c.puntos(c.uno) - desfase
        lineas.append(f"### {c.op} (0 = {cero}, 1 = {uno})")
        candidatas: dict[str, tuple[int, int] | None] = {
            r: f(ventanas[c.op], c.direccion) for r, f in REGLAS.items()
        }
        for i, limpia in enumerate(LECTURAS_LIMPIA):
            z = productor[(c.op, limpia)]
            nombre = f"productor {'ab'[i]}"
            candidatas[nombre] = (z.entrada, z.extremo) if isinstance(z, Esquema) else None
            if not isinstance(z, Esquema):
                lineas.append(f"- {nombre}: sin zona ({z})")
        for nombre, caja in candidatas.items():
            if caja is None:
                if not nombre.startswith("productor"):
                    lineas.append(f"- {nombre}: no da caja")
                continue
            d0, d1 = caja[0] - cero, caja[1] - uno
            for tau in TAUS:
                if abs(d0) <= tau and abs(d1) <= tau:
                    aciertos[nombre][f"los dos a {tau}"] += 1
                if abs(d0) <= tau:
                    aciertos[nombre][f"el 0 a {tau}"] += 1
                if abs(d1) <= tau:
                    aciertos[nombre][f"el 1 a {tau}"] += 1
            marca = " · ACIERTA" if abs(d0) <= TAU and abs(d1) <= TAU else ""
            lineas.append(f"- {nombre}: 0 = {caja[0]} ({d0:+d}), 1 = {caja[1]} ({d1:+d}){marca}")
    lineas += [
        "",
        f"## RECUENTO ({titulo.split(' ·')[0]}, sobre las {len(CAJAS)} cajas legibles)",
        "| regla | los dos a 1 | a 2 | a 3 | el 0 a 2 | el 1 a 2 |",
        "|---|---|---|---|---|---|",
    ]
    for nombre, cnt in aciertos.items():
        lineas.append(
            f"| {nombre} | {cnt['los dos a 1']} | {cnt['los dos a 2']} | {cnt['los dos a 3']} | "
            f"{cnt['el 0 a 2']} | {cnt['el 1 a 2']} |"
        )
    return [*lineas, ""], aciertos


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: bloque_de_la_caja.py --salida <fichero>", file=sys.stderr)
        return 2
    reservados, ocultos = casos_reservados(RAIZ), casos_ocultos(RAIZ)
    for c in CAJAS:
        if f"caso-eurusd-{c.dia}" in reservados or f"caso-eurusd-{c.dia}" in ocultos:
            raise ValueError("una caja cae en un dia reservado u oculto: no se mide")
    manifiesto = cargar_manifiesto(buscar_manifiesto(RAIZ, "eurusd-m1-2026-08"))
    if int(manifiesto["escala"]) != ESCALA:
        raise ValueError(f"escala {manifiesto['escala']} != {ESCALA}")
    todas = list(cargar_ventana(manifiesto, carpeta_datos(RAIZ)).velas)
    productor = zonas_del_productor({c.dia for c in CAJAS})
    lineas = [
        "# El bloque de la caja: fases 2 y 3 (criterio en BLOQUE-DE-LA-CAJA.md §1)",
        f"CAJAS: {len(CAJAS)} legibles; velas: {manifiesto['dataset_id']} (Dukascopy, BID, UTC); "
        "pantalla: FX Replay (OANDA, UTC+2 fijo). OANDA y Dukascopy difieren 1-2 puntos (A-16).",
        f"ventana: M1 en [T - {VENTANA_MIN} min, T) (v1) o hasta el cierre de la M1 en curso en T "
        f"(v2); tau {TAU} puntos (sensibilidad {', '.join(map(str, TAUS))})",
        "",
    ]
    control, desfase = control_de_proveedor(todas)
    lineas += control
    for titulo, en_curso, corregida in VERSIONES:
        d = desfase if corregida else 0
        bloque, _ = fases(
            todas, en_curso, f"{titulo} ({d:+d} puntos)" if corregida else titulo, productor, d
        )
        lineas += bloque
    Path(argv[1]).write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
