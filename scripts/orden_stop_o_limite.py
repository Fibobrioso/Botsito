"""¿Entra el trader con ordenes STOP a favor de la ruptura o con ordenes LIMITE en el retroceso?
Rama `trabajo/orden-stop-o-limite`, 2026-09-27. Es una HIPOTESIS que se mide, no se adopta: A-47
sigue abierta y nada de esto toca el motor, el productor ni la spec.

Fase 2, el criterio (escrito ANTES de correrlo, en docs/validation/ORDEN-STOP-O-LIMITE.md §1):
para cada operacion de construccion, desde que lado llego el precio al nivel de entrada L en el
instante de llenado t del caso. Con TICKS (obligatorios si existen, ADR-0051; precio bid para una
venta, ask para una compra): en la ventana [t-60 s, t] el ultimo tick que NO esta en el nivel
(|p-L| > tol, con tol = `margen_puntos` de criterio_huso.yaml) fija el lado de llegada; si hay
ticks por encima Y por debajo, «ambiguo»; si ningun tick esta fuera del nivel, se amplia a
[t-300 s, t]. Sin ticks en [t-300 s, t+60 s], M1: el cierre (o la apertura) de la vela anterior.
Venta que llega de ARRIBA -> STOP; de ABAJO -> LIMITE. Compra al reves.

Ademas, ANADIDOS despues de ver el resultado y sin cambiar el criterio: un diagnostico (donde
esta el precio en t, cuando toca el nivel por primera vez, y a que lado esta 60 s antes, por
direccion), una robustez (precio, tolerancia y ventana) y dos trazas de ticks.

Fase 4: para las operaciones con zona viva en el llenado (los mismos supuestos que
scripts/verificacion_a21_entradas.py), la distancia firmada de la entrada al nivel de referencia
del breaker del productor (`Esquema.referencia`), frente a la distancia al borde de la zona.

    uv run python scripts/orden_stop_o_limite.py --salida <fichero>
"""

from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Callable, Sequence
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))

from verificacion_a21_entradas import _distancia, _minuto  # noqa: E402

from botsito.cases.criterio_fidelidad import Criterio, cargar_criterio  # noqa: E402
from botsito.cases.holdout import casos_ocultos  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.comun.yaml_estricto import leer_yaml  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_ventana  # noqa: E402
from botsito.data.ticks import (  # noqa: E402
    buscar_manifiesto_ticks,
    cargar_manifiesto_ticks,
    cargar_ticks,
)
from botsito.domain.estructura_m1 import COMPRA, LECTURAS_LIMPIA, detectar_esquema  # noqa: E402
from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA  # noqa: E402
from botsito.domain.sesgo import sesgo_h4  # noqa: E402
from botsito.domain.ticks import Tick  # noqa: E402
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

W1_S, W2_S, POST_S = 60, 300, 60
STOP, LIMITE, AMBIGUO, SIN_DATOS = "STOP", "LIMITE", "ambiguo", "sin datos"
ARRIBA, ABAJO = "arriba", "abajo"
ESCALA = 100000
MS_DIA = 86_400_000

Precio = Callable[[Tick, str], int]


def bid_ask(k: Tick, direccion: str) -> int:
    """El lado con el que un broker llena cada orden: bid para una venta, ask para una compra."""
    return int(k.bid) if direccion == "venta" else int(k.ask)


def mid(k: Tick, direccion: str) -> int:
    return (int(k.bid) + int(k.ask)) // 2


def ask_bid(k: Tick, direccion: str) -> int:
    return int(k.ask) if direccion == "venta" else int(k.bid)


def lado_llegada(precios: Sequence[int], nivel: int, tol: int) -> str | None:
    """`arriba`, `abajo`, `ambiguo`, o None si ningun tick esta fuera del nivel."""
    fuera = [p for p in precios if abs(p - nivel) > tol]
    if not fuera:
        return None
    hay_arriba = any(p > nivel + tol for p in fuera)
    hay_abajo = any(p < nivel - tol for p in fuera)
    if hay_arriba and hay_abajo:
        return AMBIGUO
    return ARRIBA if fuera[-1] > nivel + tol else ABAJO


def tipo_de(direccion: str, lado: str | None) -> str:
    if lado is None:
        return SIN_DATOS
    if lado == AMBIGUO:
        return AMBIGUO
    if direccion == "venta":
        return STOP if lado == ARRIBA else LIMITE
    return STOP if lado == ABAJO else LIMITE


def posicion(p: int, nivel: int, tol: int) -> str:
    if p > nivel + tol:
        return "encima"
    if p < nivel - tol:
        return "debajo"
    return "en"


def distribucion(xs: Sequence[int]) -> str:
    if not xs:
        return "ninguna"
    s = sorted(xs)
    return (
        f"min {s[0]} · p25 {s[len(s) // 4]} · mediana {median(s)} · p75 {s[3 * len(s) // 4]} · "
        f"max {s[-1]}"
    )


def ms_de(instante: datetime) -> int:
    return int(instante.astimezone(UTC).timestamp() * 1000)


class Op:
    """Una operacion del trader con lo que las fases necesitan de ella."""

    def __init__(self, dia: str, sesion: str, direccion: str, entrada: str, instante: datetime):
        self.dia, self.sesion, self.direccion, self.entrada = dia, sesion, direccion, entrada
        self.instante = instante.astimezone(UTC)
        self.t_ms = ms_de(instante)
        self.nivel = int((Decimal(entrada) * ESCALA).to_integral_value())
        self.tipo = "?"
        self.lado = "-"
        self.fuente = "-"
        self.ventana = "-"
        self.n_ticks = 0

    @property
    def etiqueta(self) -> str:
        return f"{self.dia} {self.sesion} {self.instante.strftime('%H:%M:%S')}Z {self.direccion}"


def _ticks_por_dia(criterio: Criterio, carpeta: Path) -> Callable[[str], list[Tick]]:
    manifiestos = {
        mes: cargar_manifiesto_ticks(buscar_manifiesto_ticks(RAIZ, f"eurusd-ticks-{mes}"))
        for mes in criterio.construccion
    }
    for m in manifiestos.values():
        if int(m["escala"]) != ESCALA:
            raise ValueError(f"escala de ticks {m['escala']} != {ESCALA}")
    cache: dict[str, list[Tick]] = {}

    def ticks(dia: str) -> list[Tick]:
        if dia not in cache:
            d0 = ms_de(datetime.fromisoformat(dia + "T00:00:00+00:00"))
            cache[dia] = list(cargar_ticks(manifiestos[dia[:7]], carpeta, d0, d0 + MS_DIA).ticks)
        return cache[dia]

    return ticks


def _m1_por_mes(criterio: Criterio, carpeta: Path) -> dict[str, list[Vela]]:
    salida: dict[str, list[Vela]] = {}
    for mes in criterio.construccion:
        mm = cargar_manifiesto(buscar_manifiesto(RAIZ, f"eurusd-m1-{mes}"))
        if int(mm["escala"]) != ESCALA:
            raise ValueError(f"escala de M1 {mm['escala']} != {ESCALA}")
        salida[mes] = list(cargar_ventana(mm, carpeta).velas)
    return salida


def fase2(
    ops: list[Op], ticks: Callable[[str], list[Tick]], m1: dict[str, list[Vela]], tol: int
) -> None:
    """Clasifica cada operacion en su sitio (op.tipo, op.lado, op.fuente, op.ventana)."""
    for op in ops:
        serie = ticks(op.dia)
        t = op.t_ms
        rango = [k for k in serie if t - W2_S * 1000 <= k.instante <= t + POST_S * 1000]
        if rango:
            w1 = [bid_ask(k, op.direccion) for k in serie if t - W1_S * 1000 <= k.instante <= t]
            op.n_ticks = len(w1)
            lado = lado_llegada(w1, op.nivel, tol)
            op.ventana = f"{W1_S} s"
            if lado is None:
                w2 = [bid_ask(k, op.direccion) for k in serie if t - W2_S * 1000 <= k.instante <= t]
                lado = lado_llegada(w2, op.nivel, tol)
                op.ventana = f"{W2_S} s" if lado is not None else f"{W2_S} s (sin tick fuera)"
            op.fuente = "ticks"
            op.lado = lado or "-"
            op.tipo = tipo_de(op.direccion, lado)
            continue
        velas = m1[op.dia[:7]]
        minuto = t // 60000
        idx = next((i for i, v in enumerate(velas) if int(v.inicio) == minuto), None)
        op.fuente = "M1"
        if idx is None or idx == 0:
            op.tipo = SIN_DATOS
            continue
        prev = velas[idx - 1]
        ref = int(prev.cierre)
        if abs(ref - op.nivel) <= tol:
            ref = int(prev.abierta)
        lado = AMBIGUO if abs(ref - op.nivel) <= tol else (ARRIBA if ref > op.nivel else ABAJO)
        op.ventana = "vela anterior"
        op.lado = lado
        op.tipo = tipo_de(op.direccion, lado)


def tabla_fase2(ops: list[Op], criterio: Criterio, tol: int) -> list[str]:
    out = [
        "# FASE 2 · lado de llegada del precio al nivel de entrada en el llenado",
        f"CONJUNTO: construccion ({', '.join(criterio.construccion)}); operaciones {len(ops)}; "
        f"tolerancia {tol} puntos (criterio_huso.yaml); ventanas {W1_S} s y {W2_S} s antes del "
        "llenado; precio bid (venta) / ask (compra)",
        "",
        "| dia | sesion | hora UTC | dir. | entrada | tipo | llega de | fuente | ventana | "
        "ticks en 60 s |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for o in ops:
        out.append(
            f"| {o.dia} | {o.sesion} | {o.instante.strftime('%H:%M:%S')} | {o.direccion} | "
            f"{o.entrada} | {o.tipo} | {o.lado} | {o.fuente} | {o.ventana} | {o.n_ticks} |"
        )
    out += [
        "",
        "| mes | fuente | STOP | LIMITE | ambiguo | sin datos | total |",
        "|---|---|---|---|---|---|---|",
    ]
    for mes in (*criterio.construccion, "total"):
        for fuente in ("ticks", "M1"):
            sub = [
                o for o in ops if (mes == "total" or o.dia.startswith(mes)) and o.fuente == fuente
            ]
            if not sub:
                continue
            c = Counter(o.tipo for o in sub)
            out.append(
                f"| {mes} | {fuente} | {c[STOP]} | {c[LIMITE]} | {c[AMBIGUO]} | {c[SIN_DATOS]} | "
                f"{len(sub)} |"
            )
    for direccion in ("compra", "venta"):
        c = Counter(o.tipo for o in ops if o.direccion == direccion)
        out.append(
            f"| {direccion} | todas | {c[STOP]} | {c[LIMITE]} | {c[AMBIGUO]} | {c[SIN_DATOS]} | "
            f"{sum(c.values())} |"
        )
    return out + [""]


def diagnostico(ops: list[Op], ticks: Callable[[str], list[Tick]], tol: int) -> list[str]:
    """Anadido tras ver la fase 2: donde esta el precio en t, cuando toca el nivel, y a que lado
    esta 60 s antes, por direccion."""
    out = ["# DIAGNOSTICO (anadido despues de ver la fase 2; no cambia el criterio)"]
    dif_pt: list[int] = []
    desfases: list[float] = []
    antes: dict[str, Counter[str]] = {"venta": Counter(), "compra": Counter()}
    for o in ops:
        if o.fuente != "ticks":
            continue
        serie = ticks(o.dia)
        hasta_t = [k for k in serie if k.instante <= o.t_ms]
        if hasta_t:
            dif_pt.append(bid_ask(hasta_t[-1], o.direccion) - o.nivel)
        rango = [k for k in serie if o.t_ms - W2_S * 1000 <= k.instante <= o.t_ms + POST_S * 1000]
        toque = next((k for k in rango if abs(bid_ask(k, o.direccion) - o.nivel) <= tol), None)
        if toque is not None:
            desfases.append((toque.instante - o.t_ms) / 1000)
        previos = [k for k in serie if k.instante <= o.t_ms - 60_000]
        if previos:
            antes[o.direccion][posicion(bid_ask(previos[-1], o.direccion), o.nivel, tol)] += 1
    a = sorted(abs(x) for x in dif_pt)
    out += [
        f"p(t) - L en puntos ({len(dif_pt)} operaciones con ticks): {distribucion(dif_pt)}; "
        f"|p(t)-L| <= {tol}: {sum(1 for x in a if x <= tol)}; <= 5: {sum(1 for x in a if x <= 5)}",
        "primer tick en el nivel dentro de [t-300 s, t+60 s], desfase respecto a t (s): "
        + (
            f"min {min(desfases):.0f}, mediana {median(desfases):.0f}, max {max(desfases):.0f}; "
            f"|desfase| <= 5 s: {sum(1 for x in desfases if abs(x) <= 5)}; sin toque: "
            f"{len(dif_pt) - len(desfases)}"
            if desfases
            else "ninguno"
        ),
        "| dir. | precio 60 s ANTES: encima de L | en L | debajo de L |",
        "|---|---|---|---|",
    ]
    for d, c in antes.items():
        out.append(f"| {d} | {c['encima']} | {c['en']} | {c['debajo']} |")
    return out + [""]


def robustez(ops: list[Op], ticks: Callable[[str], list[Tick]]) -> list[str]:
    """Anadida tras ver la fase 2: el mismo recuento con otro precio, otra tolerancia y otra
    ventana, y dos trazas de ticks para leerlas a mano."""
    con_ticks = [o for o in ops if o.fuente == "ticks"]
    out = [
        "# ROBUSTEZ (anadida despues de ver la fase 2; el criterio es la fila bid/ask · 2 · 60 s)",
        "| precio | tol | ventana | STOP | LIMITE | ambiguo | sin dato |",
        "|---|---|---|---|---|---|---|",
    ]
    precios: dict[str, Precio] = {"bid/ask": bid_ask, "mid": mid, "ask/bid (al reves)": ask_bid}
    for nombre, pf in precios.items():
        for tol in (0, 2, 5):
            for w in (10, 60, 300):
                c: Counter[str] = Counter()
                for o in con_ticks:
                    ps = [
                        pf(k, o.direccion)
                        for k in ticks(o.dia)
                        if o.t_ms - w * 1000 <= k.instante <= o.t_ms
                    ]
                    c[tipo_de(o.direccion, lado_llegada(ps, o.nivel, tol))] += 1
                out.append(
                    f"| {nombre} | {tol} | {w} s | {c[STOP]} | {c[LIMITE]} | {c[AMBIGUO]} | "
                    f"{c[SIN_DATOS]} |"
                )
    for d in ("venta", "compra"):
        o = next(x for x in con_ticks if x.direccion == d and x.dia.startswith("2026-08"))
        tr = [k for k in ticks(o.dia) if o.t_ms - 90_000 <= k.instante <= o.t_ms + 30_000]
        paso = max(1, len(tr) // 40)
        out += [
            "",
            f"traza {o.etiqueta} L={o.nivel} (segundos respecto a t : bid/ask - L):",
            "  "
            + " ".join(
                f"{(k.instante - o.t_ms) / 1000:+.0f}s:{bid_ask(k, d) - o.nivel:+d}"
                for k in tr[::paso]
            ),
        ]
    return out + [""]


def fase4(ops: list[Op], criterio: Criterio, tol_adr: int) -> list[str]:
    """Distancia firmada al nivel de referencia del breaker del productor, en las operaciones con
    zona viva en el llenado (mismos supuestos que verificacion_a21_entradas.py)."""
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    huso = registro.texto("huso_operativa")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    carpeta = carpeta_datos(RAIZ)
    mercado = arnes.dias_de_mercado(
        RAIZ, carpeta, config, registro, dias, huso, CIERRE_VELA_CONTRARIA
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
    tipos = {(o.dia, o.instante.isoformat()): o.tipo for o in ops}
    out = [
        "# FASE 4 · la entrada frente al nivel de referencia del breaker del productor "
        "(Esquema.referencia)",
        "d_ref = entrada - referencia (compra) / referencia - entrada (venta): > 0 mas alla del "
        "nivel en la direccion de la ruptura. d_zona como en VERIFICACION-A21 (borde cercano de "
        "la zona).",
        f"tolerancia de ADR-0043: {tol_adr} puntos",
    ]
    for limpia in LECTURAS_LIMPIA:
        motor = MotorSpec(Interprete(voc, primitivas_escritas(registro, tope, limpia)), reglas)
        filas: list[str] = []
        d_refs: list[int] = []
        d_zonas: list[int] = []
        sin_zona = 0
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
            toma_dia = tomas[0] if tomas else None
            for op in d.operaciones:
                tipo = tipos.get((d.dia, op.instante.astimezone(UTC).isoformat()), "?")
                t_op = _minuto(op.instante)
                etiqueta = (
                    f"{d.dia} {op.sesion} {op.instante.astimezone(UTC).strftime('%H:%M')}Z "
                    f"{op.direccion} [{tipo}]"
                )
                precio = int((Decimal(op.entrada) * ESCALA).to_integral_value())
                if op.sesion not in aperturas or toma_dia is None or toma_dia[0] > t_op:
                    sin_zona += 1
                    filas.append(f"- {etiqueta}: SIN ZONA")
                    continue
                toma, toma_sesion = toma_dia
                t_ap = aperturas[toma_sesion]
                sesgo = sesgo_h4(
                    dm.datos.velas_h4_cerradas(t_ap), MinutoUtc(t_ap), tope_sesgo, criterio_ruptura
                ).sesgo.value
                lado = LADO_ENTRADA.get(sesgo)
                if lado is None:
                    sin_zona += 1
                    filas.append(f"- {etiqueta}: SIN ZONA (sesgo {sesgo})")
                    continue
                m1 = dm.datos.m1_entre(toma - LOOKBACK_M1, t_op)
                idx = next((k for k, v in enumerate(m1) if int(v.fin) == toma), None)
                e = (
                    detectar_esquema(m1, idx, lado, criterio_breaker, tope_zonas, limpia)
                    if idx is not None
                    else None
                )
                if e is None:
                    sin_zona += 1
                    filas.append(f"- {etiqueta}: SIN ZONA (sin esquema antes del llenado)")
                    continue
                d_ref = precio - e.referencia if op.direccion == COMPRA else e.referencia - precio
                d_zona = _distancia(e, precio)
                d_refs.append(d_ref)
                d_zonas.append(d_zona)
                contraria = "; DIRECCION CONTRARIA a la zona" if op.direccion != e.lado else ""
                filas.append(
                    f"- {etiqueta}: zona {e.lado} {e.cual}; d_ref = {d_ref:+d}; d_zona = "
                    f"{d_zona:+d}{contraria}"
                )
        n = len(d_refs)
        out += [
            f"## A-21 = {limpia}: con zona viva {n}; sin zona {sin_zona}",
            f"d_ref: {distribucion(d_refs)}; |d_ref| <= {tol_adr}: "
            f"{sum(1 for x in d_refs if abs(x) <= tol_adr)} de {n}; |d_ref| <= 10: "
            f"{sum(1 for x in d_refs if abs(x) <= 10)}",
            f"d_zona (mismas operaciones): {distribucion(d_zonas)}; |d_zona| <= {tol_adr}: "
            f"{sum(1 for x in d_zonas if abs(x) <= tol_adr)}; d_zona <= {tol_adr} (dentro, borde o "
            f"mas alla del extremo): {sum(1 for x in d_zonas if x <= tol_adr)}",
            *filas,
            "",
        ]
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: orden_stop_o_limite.py --salida <fichero>", file=sys.stderr)
        return 2
    criterio = cargar_criterio(RAIZ)
    tol = int(leer_yaml(RAIZ / "knowledge" / "corpus" / "criterio_huso.yaml")["margen_puntos"])
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    ocultos = casos_ocultos(RAIZ)
    for d in dias:
        if f"caso-eurusd-{d.dia}" in ocultos:
            raise ValueError("un dia de construccion esta oculto: no se mide")
    ops = [
        Op(d.dia, op.sesion, op.direccion, str(op.entrada), op.instante)
        for d in dias
        for op in d.operaciones
    ]
    carpeta = carpeta_datos(RAIZ)
    ticks = _ticks_por_dia(criterio, carpeta)
    m1 = _m1_por_mes(criterio, carpeta)
    fase2(ops, ticks, m1, tol)
    lineas = [
        "# Orden STOP o LIMITE: como se lleno cada entrada del trader en construccion",
        "Rama trabajo/orden-stop-o-limite, 2026-09-27. Descriptivo: no elige nada ni toca el "
        "motor.",
        "",
        *tabla_fase2(ops, criterio, tol),
        *diagnostico(ops, ticks, tol),
        *robustez(ops, ticks),
        *fase4(ops, criterio, criterio.tolerancias.entrada_puntos),
    ]
    Path(argv[1]).write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
