"""El embudo de las 77: en que paso del pipeline deja el bot de acompanar a cada operacion.

Rama `trabajo/embudo-77`, 2026-09-28. Es una MEDICION: no cambia la estrategia, el productor ni el
broker, y no corrige nada de lo que encuentre. Corre el motor cableado igual que
`motor arnes --simular`, en DIAGNOSTICO (A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-47
`stop_en_ruptura`, A-27 el stops level pedido) con la lectura de A-21 pedida, y para cada operacion
del trader anota el PRIMER paso en el que el bot deja de acompanarla. La clasificacion es una
funcion pura (`clasificar`) sobre lo medido (`Hechos`); todo lo demas solo mide.

Los pasos, en el orden del pipeline real (docs/validation/EMBUDO-77.md §1):

1. sesion: el instante del trader cae fuera de la ventana de su sesion;
2. sesgo: la sesion no tiene sesgo H4 (RN-003, RN-033) o lo tiene contrario a la operacion;
3. liquidez: el productor no tiene, EN LA SESION DE LA OPERACION, toma de M15 (RN-004) antes del
   trader + la tolerancia. Desde la rama trabajo/nocturno-01oct cada sesion tiene su toma y su
   zona (A-46 RESUELTA): la rama «toma de otra sesion» de `clasificar` ya no puede darse con el
   motor real, y se conserva para leer las salidas de antes;
4. breaker: tras la toma, el productor no detecta esquema (RN-008, RN-009, A-21);
5. caja: el 0 de la zona del bot queda a mas de la tolerancia de puntos de la entrada del trader;
6. momento: el breaker cierra despues del instante del trader + la tolerancia de minutos;
7. reglas: con la zona formada, no sale orden (RN-011 no dispara o una gate prohibe);
8. broker: la orden se rechaza (lado equivocado, volumen, stops level);
9. llenado: la orden no se llena, o se llena fuera de la tolerancia, o su operacion ya casa con
   otra del trader;
y `coincide` si el criterio de fidelidad (ADR-0043) la empareja.

CON LA VIDA DE LA ORDEN STOP (ADR-0064: `orden_limite_nace` = `al_aparecer_punto_de_breaker`) los
pasos 4 en adelante describen esa vida y no el esquema, que el motor ya no usa para colocar
(`PASOS_VIDA`, `clasificar_vida`): 4. nace: ninguna orden de la sesion antes del trader + la
tolerancia; 5. punto: hay ordenes, pero ninguna en el precio del trader; 6. broker: la del precio
se rechazo; 7. reubica: la del precio se cancelo al reubicarse y no se lleno; 8. llenado: no se
lleno, o fuera de tolerancia, o casa con otra; y `coincide`. Anade, por sesion, la vida de sus
ordenes (colocadas, canceladas, rechazadas, llenadas y como se cerraron) y el DIAGNOSTICO DEL STOP:
la distancia entrada-stop y la caja del bot en sus llenados frente a las del trader en el libro, y
por llenado la caja, los minutos desde que se fijo la caja, hasta el cierre y el spread en el
llenado y en el cierre, medido en los ticks.

Solo construccion (abril y agosto), por la compuerta del arnes. Lee el repositorio en --raiz (por
defecto, el de este script) y escribe SOLO en --salida (.txt y .json).

    uv run python scripts/embudo_77.py --a21 <lectura> --salida <fichero> [--a27 0] [--raiz <repo>]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))

PASOS = (
    "sesion",
    "sesgo",
    "liquidez",
    "breaker",
    "caja",
    "momento",
    "reglas",
    "broker",
    "llenado",
    "coincide",
)
PASOS_VIDA = (
    "sesion",
    "sesgo",
    "liquidez",
    "nace",
    "punto",
    "broker",
    "reubica",
    "llenado",
    "coincide",
)
A_FAVOR = {"compra": "alcista", "venta": "bajista"}


@dataclass(frozen=True)
class Hechos:
    """Lo medido para UNA operacion del trader: instantes en segundos UTC, precios en puntos."""

    sesion: str
    direccion: str
    instante_s: int
    entrada: int
    en_sesion: bool
    sesgo: str | None  # el que fijo RN-003 al abrir la sesion de la operacion
    # las tomas DISTINTAS de RN-004 en la sesion de la operacion: el cierre de la M15 que toma; el
    # hecho se vuelve a fijar en cada M1 mientras esa M15 sea la ultima cerrada, y eso no son
    # tomas nuevas
    tomas_rn004_s: tuple[int, ...]
    toma_s: int | None  # la del productor: la unica del dia (memoria de un solo uso)
    toma_sesion: str | None
    zona_lado: str | None  # el esquema del productor, si lo hay
    zona_entrada: int | None
    zona_formada_s: int | None  # el cierre del breaker
    sin_esquema: str | None  # sin esquema: por que, medido en el trader + la tolerancia
    sin_orden: str | None  # con zona y sin orden: por que (reglas); None si hubo orden
    rechazo: str | None  # el motivo del broker, si la rechazo
    llenada: bool
    pos_sesion: str | None
    pos_abierta_s: int | None
    pos_entrada: int | None
    emparejada: bool
    bot_casa_con_otra: bool


def _zona_casa(h: Hechos, tol_puntos: int, tol_s: int) -> bool:
    return (
        h.zona_lado == h.direccion
        and h.zona_entrada is not None
        and abs(h.zona_entrada - h.entrada) <= tol_puntos
        and h.zona_formada_s is not None
        and h.zona_formada_s <= h.instante_s + tol_s
    )


def clasificar(h: Hechos, tol_puntos: int, tol_s: int) -> tuple[str, str, str]:
    """El primer paso en el que el bot deja de acompanar a la operacion: (paso, motivo, detalle).
    El motivo agrupa; el detalle lleva las cifras. Pura."""
    if h.emparejada:
        return "coincide", "coincide", ""
    if not h.en_sesion:
        return "sesion", "fuera de la ventana de su sesion", ""
    if h.sesgo not in A_FAVOR.values():
        return "sesgo", "sin sesgo", h.sesgo or "ninguno"
    if h.sesgo != A_FAVOR[h.direccion]:
        return "sesgo", "sesgo contrario", h.sesgo
    limite = h.instante_s + tol_s
    if h.toma_s is None or h.toma_s > limite:
        if any(t <= limite for t in h.tomas_rn004_s):
            return "liquidez", "RN-004 la fija y el productor no la registra", ""
        return "liquidez", "ninguna toma de M15 antes del trader", ""
    if h.toma_sesion != h.sesion and not _zona_casa(h, tol_puntos, tol_s):
        otras = sum(1 for t in h.tomas_rn004_s if t <= limite)
        if otras:
            return (
                "liquidez",
                "la del productor es de una sesion anterior y no usa las nuevas",
                f"{otras} toma(s) nueva(s) en la sesion antes del trader",
            )
        return (
            "liquidez",
            "la del productor es de una sesion anterior y en la sesion no hay otra",
            "",
        )
    if h.zona_entrada is None or h.zona_formada_s is None:
        motivo, _, detalle = (h.sin_esquema or "sin medir").partition(": ")
        return "breaker", f"sin esquema: {motivo}", detalle
    if h.zona_lado != h.direccion:
        return "caja", "zona del lado contrario", ""
    d = abs(h.zona_entrada - h.entrada)
    if d > tol_puntos:
        return "caja", "0 fuera de tolerancia", f"{d} puntos"
    if h.zona_formada_s > limite:
        return (
            "momento",
            "el breaker cierra tarde",
            f"{(h.zona_formada_s - h.instante_s) // 60} min",
        )
    if h.sin_orden is not None:
        return "reglas", h.sin_orden, ""
    if h.rechazo is not None:
        return "broker", f"rechazo: {h.rechazo}", ""
    if not h.llenada or h.pos_abierta_s is None or h.pos_entrada is None:
        return "llenado", "la orden no se llena", ""
    if h.pos_sesion != h.sesion:
        return "llenado", "se llena en otra sesion", h.pos_sesion or "fuera de sesion"
    dt, dp = abs(h.pos_abierta_s - h.instante_s), abs(h.pos_entrada - h.entrada)
    if dt > tol_s:
        return "llenado", "se llena fuera de la tolerancia de minutos", f"{dt // 60} min"
    if dp > tol_puntos:
        return "llenado", "se llena fuera de la tolerancia de puntos", f"{dp} puntos"
    if h.bot_casa_con_otra:
        return "llenado", "su operacion casa con otra del trader", ""
    return "llenado", "compatible y sin pareja", ""  # no deberia darse: el criterio la emparejaria


@dataclass(frozen=True)
class HechosVida:
    """Lo medido para UNA operacion del trader con la vida de la orden stop (ADR-0064)."""

    en_sesion: bool
    direccion: str
    sesgo: str | None
    toma_s: int | None  # la toma de la sesion en el productor
    instante_s: int
    entrada: int
    # las ordenes de la sesion colocadas hasta el trader + la tolerancia: (precio, estado,
    # colocada_s,
    # lado, llenada_s o None, entrada del llenado o None)
    ordenes: tuple[tuple[int, str, int, str, int | None, int | None], ...]
    sin_orden: str | None  # por que no nacio ninguna, si no nacio
    emparejada: bool
    bot_casa_con_otra: bool


def clasificar_vida(h: HechosVida, tol_puntos: int, tol_s: int) -> tuple[str, str, str]:
    """El primer paso de la vida de la orden stop en el que el bot deja de acompanar a la
    operacion: (paso, motivo, detalle). Pura."""
    if h.emparejada:
        return "coincide", "coincide", ""
    if not h.en_sesion:
        return "sesion", "fuera de la ventana de su sesion", ""
    if h.sesgo not in A_FAVOR.values():
        return "sesgo", "sin sesgo", h.sesgo or "ninguno"
    if h.sesgo != A_FAVOR[h.direccion]:
        return "sesgo", "sesgo contrario", h.sesgo or ""
    limite = h.instante_s + tol_s
    if h.toma_s is None or h.toma_s > limite:
        return "liquidez", "ninguna toma de M15 en la sesion antes del trader", ""
    if not h.ordenes:
        return "nace", h.sin_orden or "ninguna orden de la sesion antes del trader", ""
    del_lado = [o for o in h.ordenes if o[3] == h.direccion]
    if not del_lado:
        return "punto", "ninguna orden del lado del trader", ""
    cerca = [o for o in del_lado if abs(o[0] - h.entrada) <= tol_puntos]
    if not cerca:
        d = min(abs(o[0] - h.entrada) for o in del_lado)
        return "punto", "el punto del bot no es el del trader", f"el mas cercano a {d} puntos"
    if all(o[1] == "rechazada" for o in cerca):
        return "broker", "la orden en su precio se rechaza", ""
    llenas = [o for o in cerca if o[4] is not None]
    if not llenas:
        if any(o[1] == "cancelada" for o in cerca):
            return "reubica", "la orden en su precio se cancela antes de llenarse", ""
        return "llenado", "la orden en su precio no se llena", ""
    o = min(llenas, key=lambda x: abs((x[4] or 0) - h.instante_s))
    dt, dp = abs((o[4] or 0) - h.instante_s), abs((o[5] or 0) - h.entrada)
    if dt > tol_s:
        return "llenado", "se llena fuera de la tolerancia de minutos", f"{dt // 60} min"
    if dp > tol_puntos:
        return "llenado", "se llena fuera de la tolerancia de puntos", f"{dp} puntos"
    if h.bot_casa_con_otra:
        return "llenado", "su operacion casa con otra del trader", ""
    return "llenado", "compatible y sin pareja", ""


def tabla(clases: Mapping[str, Sequence[str]], pasos: Sequence[str] = PASOS) -> list[str]:
    """La tabla del embudo: cuantas operaciones mueren en cada paso, por lectura."""
    lecturas = list(clases)
    cuentas = {lec: Counter(clases[lec]) for lec in lecturas}
    lineas = [
        "| paso | " + " | ".join(lecturas) + " |",
        "|---|" + "---|" * len(lecturas),
    ]
    for n, paso in enumerate(pasos, 1):
        nombre = paso if paso == "coincide" else f"{n}. {paso}"
        lineas.append(
            f"| {nombre} | " + " | ".join(str(cuentas[lec][paso]) for lec in lecturas) + " |"
        )
    lineas.append("| total | " + " | ".join(str(len(clases[lec])) for lec in lecturas) + " |")
    return lineas


# --------------------------------------------------------------------------------- medicion


def _limites(dia: date, sesiones: Iterable[Any], huso: ZoneInfo) -> list[tuple[str, int, int]]:
    """Las ventanas de sesion en segundos UTC (como `cableado._minuto_local`, en segundos)."""
    salida = []
    for s in sesiones:
        par = []
        for hhmm in (s.desde, s.hasta):
            hh, mm = (int(x) for x in hhmm.split(":"))
            local = datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=huso)
            par.append(int(local.astimezone(UTC).timestamp()))
        salida.append((s.nombre, par[0], par[1]))
    return salida


def _sesion_de(limites: Sequence[tuple[str, int, int]], s: int) -> str | None:
    return next((n for n, d, h in limites if d <= s < h), None)


def _ruido(lado: str, entrada: int, extremo: int, nivel: int) -> str:
    """Donde queda la caja respecto al nivel de la liquidez tomada, en el sentido de RN-005:
    una compra opera por debajo, una venta por encima. El productor mira solo el 0 (la
    entrada)."""
    s = 1 if lado == "compra" else -1
    fuera_0 = s * (entrada - nivel) > 0
    fuera_1 = s * (extremo - nivel) > 0
    donde = (
        "entera en el lado de ruido" if fuera_1 else ("cruza el nivel" if fuera_0 else "en su lado")
    )
    return f"{donde} (nivel {nivel}, 0 {entrada}, 1 {extremo})"


def _hhmm(s: int | None) -> str:
    return "-" if s is None else datetime.fromtimestamp(s, UTC).strftime("%H:%MZ")


class Grabadora:
    """Envuelve `Interprete.evento` para guardar, por dia y minuto, lo que disparo, lo que se
    prohibio y lo que quedo bloqueado: la traza por sesion lo junta todo y pierde el minuto. Solo
    lee; el evento sale igual."""

    def __init__(self) -> None:
        self.eventos: dict[tuple[int, int], Any] = {}

    def instalar(self) -> None:
        from botsito.engine.interprete import Interprete

        original = Interprete.evento
        grabadora = self

        def evento(self: Any, reglas: Any, momento: Any, estado: Any) -> Any:
            ev = original(self, reglas, momento, estado)
            grabadora.eventos[(id(estado), int(momento.instante))] = ev
            return ev

        Interprete.evento = evento  # type: ignore[method-assign]


def por_que_sin_esquema(
    m1: Sequence[Any], idx_toma: int, lado: str, criterio: str, tope: int, limpia: str
) -> str:
    """Por que `detectar_esquema` no da esquema con estas M1: los mismos pasos, en su orden, con
    las mismas funciones del dominio. Solo lee."""
    from botsito.domain import estructura_m1 as e1

    referencia = e1.referencia_del_breaker(m1, idx_toma + 1, lado)
    if referencia is None:
        return "sin referencia (ningun pivote de M1 contrario hasta la toma)"
    for i in range(idx_toma + 1, len(m1)):
        if not e1._pasa(m1[i], referencia, lado, criterio):
            continue
        n = e1.zonas_de_control(m1, idx_toma, i, lado)
        if n > tope:
            return f"la primera ruptura deja mas zonas de control que el tope (RN-009): {n}"
        bloque = e1.bloque_de_origen(m1, i, lado)
        if bloque is None:
            return "la primera ruptura no tiene bloque de origen"
        desde, hasta = bloque
        velas = m1[desde:hasta]
        lo, hi = min(int(v.minima) for v in velas), max(int(v.maxima) for v in velas)
        extremo = lo if lado == e1.COMPRA else hi
        if limpia == e1.SIN_MECHA_MAS_ALLA_DEL_EXTREMO and e1.mecha_mas_alla_del_extremo(
            m1, hasta, i + 1, extremo, lado
        ):
            return "la lectura de A-21 rechaza la primera ruptura (mecha mas alla del extremo)"
        return "hay esquema"
    return "ninguna M1 pasa la referencia"


def _sin_orden(ev: Any, prohiben: Mapping[str, frozenset[str]], en_sesion: bool) -> str:
    """Por que, con la zona formada en ese minuto, no salio orden."""
    if not en_sesion:
        return "el breaker cierra fuera de sesion"
    if ev is None:
        return "sin evento del interprete en el cierre del breaker"
    bloqueadas = [(a, m) for r, a, m in ev.bloqueadas if r in ("RN-011", "RN-015")]
    bloqueos = sorted({a for a, _ in bloqueadas})
    if bloqueos:
        efectos = {m.split(":", 1)[1] for _, m in bloqueadas}
        gates = sorted(r for r in ev.disparadas if prohiben.get(r, frozenset()) & efectos)
        return f"prohibida por {', '.join(gates) or 'gate desconocido'}: {', '.join(bloqueos)}"
    if "RN-011" not in ev.disparadas:
        falta = sorted({p for r, p in ev.no_implementadas if r == "RN-011"})
        return "RN-011 no dispara" + (f" (no implementado: {', '.join(falta)})" if falta else "")
    if "RN-015" not in ev.disparadas:
        return "RN-011 dispara y RN-015 no coloca"
    return "RN-015 dispara y no hay orden en el broker"


def medir(
    raiz: Path, a21: str, a27: int, cuenta_diaria: bool = False
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from botsito.cases.criterio_fidelidad import cargar_criterio, compatibles, emparejar
    from botsito.cases.holdout import casos_ocultos
    from botsito.cases.paquete import cargar_config
    from botsito.comun.husos import huso_canonico
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import ParametroDesconocidoError, cargar_registro
    from botsito.domain.estructura_m1 import detectar_esquema
    from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA
    from botsito.engine import (
        arnes,
        cableado,
        diagnostico,
        entrada,
        relojes,
        tope_trader,
        zonas,
    )
    from botsito.engine.broker import RECHAZADA
    from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

    grabadora = Grabadora()
    grabadora.instalar()
    criterio = cargar_criterio(raiz)
    tol = criterio.tolerancias
    tol_s = tol.instante_min * 60
    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(raiz / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = raiz / "knowledge" / "spec" / "strategy_spec.yaml"
    vocabulario = cargar_vocabulario(spec)
    reglas_spec = cargar_reglas(spec)
    reglas = reglas_ejecutables(reglas_spec)
    prohiben = {
        r.id: frozenset(str(e) for e in r.entonces.get("prohibe", []) or [])
        for r in reglas
        if r.clase == "gate"
    }
    meses = list(criterio.construccion)
    if not set(meses) <= {"2026-04", "2026-08"}:
        raise SystemExit(f"construccion no es abril y agosto: {meses}")
    dias = arnes.dias_de_construccion(raiz, criterio, meses, ocultos=casos_ocultos(raiz))
    # A-47 esta RESUELTA desde la sesion 3 (`entrada_tipo_orden` = stop_en_ruptura): pedirla en
    # diagnostico se rechaza, y este script dejo de correr. Solo se pide si sigue sin fijar; y
    # si el registro dijera otra cosa, el embudo mediria lo que no es
    try:
        fijado: str | None = registro.opcion(entrada.PARAMETRO_A47)
    except ParametroDesconocidoError:
        fijado = None
    if fijado not in (None, entrada.STOP_EN_RUPTURA):
        raise SystemExit(f"{entrada.PARAMETRO_A47} = {fijado}: el embudo mide la orden stop")
    a47 = None if fijado is not None else entrada.STOP_EN_RUPTURA
    diag = Diagnostico(CIERRE_VELA_CONTRARIA, A44_SIN_TOPE, a21, a27, a47)
    lectura = diagnostico.lectura_pivote(registro, diag)
    perfil = cableado.perfil_del_repo(raiz, None)
    tope = tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag)
    limpia = zonas.lectura_limpia(registro, diag.a21)
    tipo_orden = entrada.lectura_tipo_orden(registro, diag.a47)
    carpeta = carpeta_datos(raiz)
    mercado = arnes.dias_de_mercado(
        raiz, carpeta, config, registro, dias, relojes.reloj_de_las_sesiones(registro), lectura
    )
    motor = cableado.construir_motor_cableado(
        raiz, carpeta, criterio, config, registro, vocabulario, reglas, dias, perfil, None, False,
        tope, limpia, stops_level_diagnostico=a27, tipo_orden=tipo_orden,
    )  # fmt: skip
    motor.cuenta_diaria = cuenta_diaria  # DIAGNOSTICO: la cuenta empieza de cero cada dia
    corrida = arnes.correr(cableado.NOMBRE_MOTOR, tuple(sorted(set(meses))), dias, mercado, motor)

    trader = [op for d in corrida.dias for op in d.operaciones]
    bot = [op for r in corrida.resultados for op in r.operaciones]
    parejas = emparejar(trader, bot, tol)
    t_pareja = {id(p.trader) for p in parejas}
    b_pareja = {id(p.bot) for p in parejas}
    trazas = {(r.dia, s): t for r in corrida.resultados for s, t in r.sesiones.items()}
    if zonas.orden_nace_en_el_punto(registro):
        return medir_vida(
            raiz, corrida, mercado, motor, grabadora, prohiben, tol, bot, t_pareja, b_pareja,
            trazas, a21, a27, cuenta_diaria,
        )  # fmt: skip
    criterio_ruptura = registro.opcion("breaker_m1_criterio_ruptura")
    tope_zonas = registro.entero("zonas_control_max_por_esquema")

    filas: list[dict[str, Any]] = []
    por_dia: list[dict[str, Any]] = []
    for d in corrida.dias:
        dm = mercado[d.dia]
        huso = huso_canonico(dm.huso)
        limites = _limites(dm.dia, dm.sesiones, huso)
        estado = motor.estados[d.dia]
        broker = motor.brokers[d.dia]
        md = motor.mercados[d.dia]
        escala = md.escala
        if escala != tol.escala:
            raise SystemExit(f"{d.dia}: escala del broker {escala} y del criterio {tol.escala}")
        # Cada sesion es un escenario propio (A-46 RESUELTA; el productor guarda la toma y el
        # esquema por sesion desde la rama trabajo/nocturno-01oct): lo del bot se mira SESION A
        # SESION, y cada operacion del trader se compara con lo de la suya
        del_bot: dict[str, tuple[Any, ...]] = {}
        for s in dm.sesiones:
            mem = zonas.memoria_de_sesion(estado, s.nombre)
            toma = mem.get("toma")
            esquema = mem.get("esquema")
            toma_s = None if toma is None else int(toma["instante"]) * 60
            formada_s = None if esquema is None else int(esquema.breaker_fin) * 60
            orden = None
            if esquema is not None:
                colocada_ms = int(esquema.breaker_fin) * 60_000 - 1
                orden = next(
                    (o for o in broker.ordenes.values() if o.colocada_ms == colocada_ms), None
                )
            sin_orden = None
            if esquema is not None and orden is None:
                ev = grabadora.eventos.get((id(estado), int(esquema.breaker_fin)))
                sin_orden = _sin_orden(ev, prohiben, _sesion_de(limites, formada_s) is not None)
            rechazo = None
            if orden is not None and orden.estado == RECHAZADA:
                rechazo = next(r.motivo for r in broker.traza().rechazos if r.orden_id == orden.id)
            pos = None
            if orden is not None:
                pos = next((p for p in broker.posiciones.values() if p.orden_id == orden.id), None)
            por_dia.append(
                {
                    "dia": d.dia,
                    "sesion": s.nombre,
                    "operaciones_trader": sum(1 for op in d.operaciones if op.sesion == s.nombre),
                    "toma": _hhmm(toma_s),
                    "toma_sesion": None if toma_s is None else _sesion_de(limites, toma_s),
                    "zona": None
                    if esquema is None
                    else f"{esquema.lado} {esquema.cual} 0={int(esquema.entrada)} "
                    f"caja {int(esquema.caja)} formada {_hhmm(formada_s)}",
                    "orden": None if orden is None else orden.estado,
                    "rechazo": rechazo,
                    "sin_orden": sin_orden,
                    "ruido": None
                    if esquema is None or toma is None
                    else _ruido(
                        esquema.lado, int(esquema.entrada), int(esquema.extremo), int(toma["nivel"])
                    ),
                    "posicion": None
                    if pos is None
                    else f"{pos.motivo_cierre} ({pos.fuente_apertura})",
                }
            )
            del_bot[s.nombre] = (
                toma, esquema, toma_s, formada_s, orden, sin_orden, rechazo, pos
            )  # fmt: skip
        for op in d.operaciones:
            toma, esquema, toma_s, formada_s, orden, sin_orden, rechazo, pos = del_bot.get(
                op.sesion, (None,) * 8
            )
            t_s = int(op.instante.timestamp())
            traza = trazas.get((d.dia, op.sesion))
            fijados = traza.fijados if traza is not None else []
            sesgo = next((v for _, r, h, v in fijados if h == "sesgo"), None)
            tomas = tuple(
                sorted(
                    {
                        i * 60  # el cierre de la M1 que toma (A-45 RESUELTA)
                        for i, r, h, v in fijados
                        if h == "liquidez_tomada" and v == "si" and r == "RN-004"
                    }
                )
            )
            ventana = next(((a, b) for n, a, b in limites if n == op.sesion), None)
            ent = int((op.entrada * escala).to_integral_value())
            b_op = next((b for b in bot if compatibles(op, b, tol) and id(b) in b_pareja), None)
            sin_esquema = None
            if esquema is None and toma is not None:
                lim_min = (t_s + tol_s) // 60
                m1 = dm.datos.m1_entre(int(toma["instante"]) - zonas.LOOKBACK_M1, lim_min)
                idx = next(
                    (k for k, v in enumerate(m1) if int(v.fin) == int(toma["instante"])), None
                )
                if idx is not None:
                    sin_esquema = por_que_sin_esquema(
                        m1, idx, str(toma["lado"]), criterio_ruptura, tope_zonas, limpia
                    )
            h = Hechos(
                sesion=op.sesion,
                direccion=op.direccion,
                instante_s=t_s,
                entrada=ent,
                en_sesion=ventana is not None and ventana[0] <= t_s < ventana[1],
                sesgo=sesgo,
                tomas_rn004_s=tomas,
                toma_s=toma_s,
                toma_sesion=None if toma_s is None else _sesion_de(limites, toma_s),
                zona_lado=None if esquema is None else esquema.lado,
                zona_entrada=None if esquema is None else int(esquema.entrada),
                zona_formada_s=formada_s,
                sin_esquema=sin_esquema,
                sin_orden=sin_orden,
                rechazo=rechazo,
                llenada=pos is not None,
                pos_sesion=None if pos is None else _sesion_de(limites, pos.abierta_ms // 1000),
                pos_abierta_s=None if pos is None else pos.abierta_ms // 1000,
                pos_entrada=None if pos is None else pos.entrada,
                emparejada=id(op) in t_pareja,
                bot_casa_con_otra=b_op is not None and id(op) not in t_pareja,
            )
            paso, motivo, detalle = clasificar(h, tol.entrada_puntos, tol_s)
            # Anotacion, no clasificacion: con la ULTIMA toma de RN-004 anterior al trader, y la
            # misma deteccion del productor (minuto a minuto, solo M1 cerradas), que esquema saldria
            alternativa = None
            previas = [t for t in tomas if t <= t_s]
            if (
                paso in ("liquidez", "breaker", "caja", "momento")
                and previas
                and sesgo in (A_FAVOR[op.direccion],)
            ):
                ultima = previas[-1] // 60  # el cierre de la M1 que toma
                alternativa = {"toma": _hhmm(ultima * 60), "esquema": None}
                fin = t_s // 60 + tol.instante_min + 1
                for minuto in range(ultima + 1, fin + 1):
                    m1 = dm.datos.m1_entre(ultima - zonas.LOOKBACK_M1, minuto)
                    idx = next((k for k, v in enumerate(m1) if int(v.fin) == ultima), None)
                    if idx is None:
                        break
                    e = detectar_esquema(
                        m1, idx, op.direccion, criterio_ruptura, tope_zonas, limpia
                    )
                    if e is not None:
                        alternativa["esquema"] = {
                            "puntos": abs(int(e.entrada) - ent),
                            "min": (int(e.breaker_fin) * 60 - t_s) // 60,
                            "casa": abs(int(e.entrada) - ent) <= tol.entrada_puntos
                            and int(e.breaker_fin) * 60 <= t_s + tol_s,
                        }
                        break
            filas.append(
                {
                    "dia": d.dia,
                    "sesion": op.sesion,
                    "instante": _hhmm(t_s),
                    "direccion": op.direccion,
                    "entrada": ent,
                    "paso": paso,
                    "motivo": motivo,
                    "detalle": detalle,
                    "bot": {
                        "sesgo": sesgo,
                        "toma": _hhmm(toma_s),
                        "toma_sesion": h.toma_sesion,
                        "tomas_rn004_sesion": [_hhmm(t) for t in tomas],
                        "zona": None
                        if esquema is None
                        else {
                            "lado": esquema.lado,
                            "cero": int(esquema.entrada),
                            "caja": int(esquema.caja),
                            "cual": esquema.cual,
                            "formada": _hhmm(formada_s),
                        },
                        "sin_orden": sin_orden,
                        "orden": None if orden is None else orden.estado,
                        "rechazo": rechazo,
                        "posicion": None
                        if pos is None
                        else {
                            "abierta": _hhmm(pos.abierta_ms // 1000),
                            "entrada": pos.entrada,
                            "cierre": pos.motivo_cierre,
                            "fuente": pos.fuente_apertura,
                        },
                    },
                    "alternativa": alternativa,
                    "hechos": asdict(h),
                }
            )
    resumen = {
        "a21": a21,
        "a27": a27,
        "a47": entrada.STOP_EN_RUPTURA,
        "operaciones_trader": len(trader),
        "operaciones_bot": len(bot),
        "parejas": len(parejas),
        "tolerancia_puntos": tol.entrada_puntos,
        "tolerancia_min": tol.instante_min,
    }
    resumen["por_dia"] = por_dia
    return filas, resumen


def _spread(ticks: Sequence[Any], ms: int) -> int | None:
    """ask - bid del ultimo tick anterior o igual a `ms`, o None."""
    import bisect

    k = bisect.bisect_right([int(x.instante) for x in ticks], ms)
    return None if k == 0 else int(ticks[k - 1].ask) - int(ticks[k - 1].bid)


def _cuartiles(xs: Sequence[float]) -> str:
    if not xs:
        return "sin datos"
    s = sorted(xs)

    def q(f: float) -> float:
        return s[min(len(s) - 1, int(f * (len(s) - 1) + 0.5))]

    return (
        f"n {len(s)}; minimo {s[0]:g}; Q1 {q(0.25):g}; mediana {q(0.5):g}; Q3 {q(0.75):g}; "
        f"maximo {s[-1]:g}"
    )


def medir_vida(
    raiz: Path, corrida: Any, mercado: Any, motor: Any, grabadora: Any, prohiben: Any, tol: Any,
    bot: Any, t_pareja: Any, b_pareja: Any, trazas: Any, a21: str, a27: int,
    cuenta_diaria: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:  # fmt: skip
    """El embudo y el diagnostico del stop con la vida de la orden stop (ADR-0064)."""
    from botsito.cases.criterio_fidelidad import compatibles
    from botsito.cases.ingesta import DIRECTORIO_DEV
    from botsito.comun.husos import huso_canonico
    from botsito.comun.yaml_estricto import leer_yaml
    from botsito.domain.estructura_m1 import ultimo_punto_de_ruptura
    from botsito.engine import entrada, zonas

    def min_desde_el_pivote(datos: Any, lado: str, instante_s: int) -> float | None:
        """Minutos desde que se formo el ultimo pivote de M1 contrario a la entrada (el 0 de R5,
        con `CIERRE_VELA_CONTRARIA`: al cierre de su vela contraria) hasta `instante_s`, con las M1
        cerradas antes del minuto de ese instante."""
        m = instante_s // 60
        pivote = ultimo_punto_de_ruptura(datos.m1_entre(m - zonas.LOOKBACK_M1, m), lado)
        if pivote is None:
            return None
        return round((instante_s - (int(pivote.contraria_inicio) + 1) * 60) / 60, 1)

    def con_mid(ticks: Sequence[Any], p: Any, fin_ms: int) -> str:
        """Con el precio MEDIO (bid + ask) / 2 en vez de bid y ask, que salta primero desde el
        llenado hasta el fin de la ventana: `stop`, `objetivo` o `ninguno`."""
        compra = p.lado == "compra"
        for k in ticks:
            if int(k.instante) <= p.abierta_ms or int(k.instante) > fin_ms:
                continue
            mid = (int(k.ask) + int(k.bid)) / 2
            if (mid <= p.stop) if compra else (mid >= p.stop):
                return "stop"
            if (mid >= p.objetivo) if compra else (mid <= p.objetivo):
                return "objetivo"
        return "ninguno"

    tol_s = tol.instante_min * 60
    filas: list[dict[str, Any]] = []
    por_dia: list[dict[str, Any]] = []
    llenados: list[dict[str, Any]] = []
    for d in corrida.dias:
        dm = mercado[d.dia]
        limites = _limites(dm.dia, dm.sesiones, huso_canonico(dm.huso))
        estado = motor.estados[d.dia]
        broker = motor.brokers[d.dia]
        md = motor.mercados[d.dia]
        ticks = md.ticks
        zonas_dia = zonas.zonas_del_dia(estado)
        pos_de_orden = {p.orden_id: p for p in broker.posiciones.values()}
        for s in dm.sesiones:
            desde, hasta = next((a, b) for n, a, b in limites if n == s.nombre)
            del_dia = [o for o in broker.ordenes.values() if desde <= o.colocada_ms // 1000 < hasta]
            cierres = Counter(
                pos_de_orden[o.id].motivo_cierre for o in del_dia if o.id in pos_de_orden
            )
            toma = zonas.memoria_de_sesion(estado, s.nombre).get("toma")
            por_dia.append(
                {
                    "dia": d.dia,
                    "sesion": s.nombre,
                    "operaciones_trader": sum(1 for op in d.operaciones if op.sesion == s.nombre),
                    "toma": _hhmm(None if toma is None else int(toma["instante"]) * 60),
                    "colocadas": len(del_dia),
                    "canceladas": sum(1 for o in del_dia if o.estado == "cancelada"),
                    "rechazadas": sum(1 for o in del_dia if o.estado == "rechazada"),
                    "llenadas": sum(1 for o in del_dia if o.id in pos_de_orden),
                    "cierres": dict(sorted(cierres.items())),
                }
            )
        for o in broker.ordenes.values():
            p = pos_de_orden.get(o.id)
            if p is None:
                continue
            z = max(
                (
                    z
                    for z in zonas_dia.values()
                    if z.entrada == o.precio and z.lado == o.lado and z.formada is not None
                    and z.formada * 60 <= o.colocada_ms // 1000 + 60
                ),
                key=lambda z: z.formada or 0,
                default=None,
            )  # fmt: skip
            abierta_s, cerrada_ms = p.abierta_ms // 1000, p.cerrada_ms
            riesgo = abs(p.entrada - (p.stop_original or p.stop))
            signo = 1 if p.lado == "compra" else -1
            fin_ventana_ms = max(b for _, _, b in limites) * 1000
            llenados.append(
                {
                    "dia": d.dia,
                    "orden": o.id,
                    "lado": o.lado,
                    "entrada": p.entrada,
                    "caja": None if z is None else z.distancia_completa,
                    "distancia_stop": abs(o.precio - (p.stop_original or p.stop)),
                    "min_caja_a_llenado": None
                    if z is None or z.formada is None
                    else round((abierta_s - z.formada * 60) / 60, 1),
                    "min_a_cierre": None
                    if cerrada_ms is None
                    else round((cerrada_ms - p.abierta_ms) / 60000, 1),
                    "cierre": p.motivo_cierre,
                    "spread_llenado": _spread(ticks, p.abierta_ms),
                    "spread_cierre": None if cerrada_ms is None else _spread(ticks, cerrada_ms),
                    "r": None
                    if p.precio_cierre is None or riesgo == 0
                    else round(signo * (p.precio_cierre - p.entrada) / riesgo, 3),
                    "min_pivote_a_llenado": min_desde_el_pivote(dm.datos, p.lado, abierta_s),
                    "con_mid": con_mid(ticks, p, fin_ventana_ms)
                    if p.motivo_cierre == "stop"
                    else None,
                }
            )
        for op in d.operaciones:
            t_s = int(op.instante.timestamp())
            sesion_lim = next(((a, b) for n, a, b in limites if n == op.sesion), None)
            en_sesion = sesion_lim is not None and sesion_lim[0] <= t_s < sesion_lim[1]
            fijados = trazas.get((d.dia, op.sesion)).fijados if (d.dia, op.sesion) in trazas else []
            sesgo = next((v for _, r, h, v in fijados if h == "sesgo"), None)
            toma = zonas.memoria_de_sesion(estado, op.sesion).get("toma")
            toma_s = None if toma is None else int(toma["instante"]) * 60
            ent = int((op.entrada * md.escala).to_integral_value())
            ordenes = []
            if sesion_lim is not None:
                for o in broker.ordenes.values():
                    c = o.colocada_ms // 1000
                    if sesion_lim[0] <= c <= t_s + tol_s and c < sesion_lim[1]:
                        p = pos_de_orden.get(o.id)
                        ordenes.append(
                            (
                                o.precio, o.estado, c, o.lado,
                                None if p is None else p.abierta_ms // 1000,
                                None if p is None else p.entrada,
                            )
                        )  # fmt: skip
            sin_orden = None
            if not ordenes and sesion_lim is not None:
                vistas = len(zonas.memoria_de_sesion(estado, op.sesion).get("puntos", {}))
                if vistas == 0:
                    sin_orden = "sin punto con caja en la sesion antes del trader"
                else:
                    for minuto in range(sesion_lim[0] // 60, min(t_s + tol_s, sesion_lim[1]) // 60):
                        ev = grabadora.eventos.get((id(estado), minuto))
                        if ev is not None and any(
                            r in ("RN-011", "RN-015") for r, _, _ in ev.bloqueadas
                        ):
                            sin_orden = _sin_orden(ev, prohiben, True)
                            break
                    else:
                        sin_orden = f"{vistas} punto(s) con caja y ninguna orden"
            b_op = next((b for b in bot if compatibles(op, b, tol) and id(b) in b_pareja), None)
            h = HechosVida(
                en_sesion=en_sesion,
                direccion=op.direccion,
                sesgo=sesgo,
                toma_s=toma_s,
                instante_s=t_s,
                entrada=ent,
                ordenes=tuple(ordenes),
                sin_orden=sin_orden,
                emparejada=id(op) in t_pareja,
                bot_casa_con_otra=b_op is not None and id(op) not in t_pareja,
            )
            paso, motivo, detalle = clasificar_vida(h, tol.entrada_puntos, tol_s)
            filas.append(
                {
                    "dia": d.dia,
                    "sesion": op.sesion,
                    "instante": _hhmm(t_s),
                    "direccion": op.direccion,
                    "entrada": ent,
                    "paso": paso,
                    "motivo": motivo,
                    "detalle": detalle,
                    "ordenes": len(ordenes),
                    "min_pivote_a_llenado": min_desde_el_pivote(dm.datos, op.direccion, t_s),
                }
            )
    # el libro: entrada menos stop inicial de cada operacion (su caja con el stop en el 1, CAJA-77)
    distancias_trader: list[float] = []
    for d in corrida.dias:
        ruta = raiz / DIRECTORIO_DEV / f"{d.id}.yaml"
        if ruta.exists():
            for op in leer_yaml(ruta).get("operaciones") or []:
                e = int(round(float(op["entrada"]) * 100_000))
                st = int(round(float(op["stop"]) * 100_000))
                distancias_trader.append(abs(e - st))
    resumen = {
        "modo": "vida",
        "cuenta_diaria": cuenta_diaria,
        "a21": a21,
        "a27": a27,
        "a47": entrada.STOP_EN_RUPTURA,
        "operaciones_trader": sum(len(d.operaciones) for d in corrida.dias),
        "operaciones_bot": len(bot),
        "parejas": len(t_pareja),
        "tolerancia_puntos": tol.entrada_puntos,
        "tolerancia_min": tol.instante_min,
        "por_dia": por_dia,
        "llenados": llenados,
        "distancias_trader": distancias_trader,
    }
    return filas, resumen


def informe_vida(filas: Sequence[Mapping[str, Any]], resumen: Mapping[str, Any]) -> str:
    ll = resumen["llenados"]
    cuenta = (
        "CUENTA REINICIADA CADA DIA (diagnostico)"
        if resumen.get("cuenta_diaria")
        else "cuenta arrastrada entre dias (ADR-0053 §6)"
    )
    lineas = [
        f"# Embudo de las 77 con la VIDA DE LA ORDEN STOP (ADR-0064), A-21 = {resumen['a21']} "
        f"(DIAGNOSTICO: A-35 cierre_vela_contraria, A-44 sin_tope, A-47 {resumen['a47']}, "
        f"A-27 {resumen['a27']}; {cuenta})",
        f"operaciones del trader: {resumen['operaciones_trader']}; del bot: "
        f"{resumen['operaciones_bot']}; parejas: {resumen['parejas']}; tolerancia "
        f"{resumen['tolerancia_puntos']} puntos y {resumen['tolerancia_min']} min",
        "",
        *tabla(
            {
                "todas": [f["paso"] for f in filas],
                **{
                    mes: [f["paso"] for f in filas if f["dia"].startswith(mes)]
                    for mes in sorted({f["dia"][:7] for f in filas})
                },
            },
            PASOS_VIDA,
        ),
        "",
        "## Por motivo",
    ]
    motivos = Counter((f["paso"], f["motivo"]) for f in filas)
    for paso in PASOS_VIDA:
        for (p, m), n in sorted(motivos.items()):
            if p == paso:
                lineas.append(f"- {p}: {m}: {n}")
    cierres = Counter(x["cierre"] for x in ll)
    lineas += [
        "",
        "## Diagnostico del stop",
        "distancia entrada-stop del BOT (en sus llenados, el stop con el que nace): "
        + _cuartiles([x["distancia_stop"] for x in ll]),
        "distancia entrada-stop del TRADER (las operaciones del libro, stop inicial): "
        + _cuartiles(resumen["distancias_trader"]),
        "caja del BOT (en sus llenados): "
        + _cuartiles([x["caja"] for x in ll if x["caja"] is not None]),
        "caja del TRADER reconstruida con el stop en el 1 (CAJA-77): la misma distancia: "
        + _cuartiles(resumen["distancias_trader"]),
        f"llenados: {len(ll)}; cierres: "
        + ", ".join(f"{k} {v}" for k, v in sorted(cierres.items())),
        "",
        "| dia | orden | lado | caja | stop | min caja->llenado | min llenado->cierre | cierre "
        "| spread llenado | spread cierre |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for x in ll:
        lineas.append(
            f"| {x['dia']} | {x['orden']} | {x['lado']} | {x['caja']} | {x['distancia_stop']} | "
            f"{x['min_caja_a_llenado']} | {x['min_a_cierre']} | {x['cierre']} | "
            f"{x['spread_llenado']} | {x['spread_cierre']} |"
        )
    rs = [x["r"] for x in ll if x["r"] is not None]
    lados_bot = Counter(x["lado"] for x in ll)
    lados_trader = Counter(f["direccion"] for f in filas)
    mid = Counter(x["con_mid"] for x in ll if x["con_mid"] is not None)
    mid_lado = Counter((x["lado"], x["con_mid"]) for x in ll if x["con_mid"] is not None)
    lineas += [
        "",
        "## Momento, resultado y spread",
        "minutos desde que se forma el ultimo pivote de M1 (el 0 de R5) hasta el llenado, BOT: "
        + _cuartiles(
            [x["min_pivote_a_llenado"] for x in ll if x["min_pivote_a_llenado"] is not None]
        ),
        "los mismos minutos, TRADER (sus operaciones, en su llenado): "
        + _cuartiles(
            [f["min_pivote_a_llenado"] for f in filas if f["min_pivote_a_llenado"] is not None]
        ),
        "resultado del BOT en R (sobre su stop inicial): "
        + _cuartiles(rs)
        + f"; ganadoras {sum(1 for r in rs if r > 0)} de {len(rs)}",
        "compras / ventas: BOT "
        + f"{lados_bot['compra']} / {lados_bot['venta']}; TRADER "
        + f"{lados_trader['compra']} / {lados_trader['venta']}",
        "stops del bot con el precio MEDIO en vez de bid y ask (desde el llenado hasta el fin "
        "de la ventana, que salta primero): "
        + ", ".join(f"{k} {v}" for k, v in sorted(mid.items()))
        + "; por lado: "
        + ", ".join(f"{a} {b} {v}" for (a, b), v in sorted(mid_lado.items())),
    ]
    lineas += ["", "## Por dia y sesion: la vida de sus ordenes"]
    for x in resumen["por_dia"]:
        lineas.append(
            f"- {x['dia']} {x['sesion']} (trader {x['operaciones_trader']}) | toma {x['toma']} | "
            f"colocadas {x['colocadas']}, canceladas {x['canceladas']}, rechazadas "
            f"{x['rechazadas']}, llenadas {x['llenadas']} | cierres {x['cierres'] or '-'}"
        )
    lineas += ["", "## Por operacion"]
    for f in filas:
        lineas.append(
            f"- {f['dia']} {f['sesion']} {f['instante']} {f['direccion']} {f['entrada']} | "
            f"{f['paso']}: {f['motivo']}{(' (' + f['detalle'] + ')') if f['detalle'] else ''} | "
            f"ordenes de la sesion hasta ahi: {f['ordenes']}"
        )
    return "\n".join(lineas) + "\n"


def informe(filas: Sequence[Mapping[str, Any]], resumen: Mapping[str, Any]) -> str:
    if resumen.get("modo") == "vida":
        return informe_vida(filas, resumen)
    lineas = [
        f"# Embudo de las 77, A-21 = {resumen['a21']} (DIAGNOSTICO: A-35 cierre_vela_contraria, "
        f"A-44 sin_tope, A-47 {resumen['a47']}, A-27 {resumen['a27']})",
        f"operaciones del trader: {resumen['operaciones_trader']}; del bot: "
        f"{resumen['operaciones_bot']}; parejas: {resumen['parejas']}; tolerancia "
        f"{resumen['tolerancia_puntos']} puntos y {resumen['tolerancia_min']} min",
        "",
        *tabla({str(resumen["a21"]): [f["paso"] for f in filas]}),
        "",
        "## Por motivo",
    ]
    motivos = Counter((f["paso"], f["motivo"]) for f in filas)
    for paso in PASOS:
        for (p, m), n in sorted(motivos.items()):
            if p == paso:
                lineas.append(f"- {p}: {m}: {n}")
    alternativas = [f for f in filas if f["alternativa"] is not None]
    casan = sum(1 for f in alternativas if (f["alternativa"]["esquema"] or {}).get("casa"))
    lineas += [
        "",
        f"## Anotacion: con la ULTIMA toma de RN-004 anterior al trader ({len(alternativas)} "
        f"operaciones muertas en liquidez, breaker, caja o momento con sesgo a favor y alguna toma "
        f"previa): el esquema casaria (<= tolerancia) en {casan}",
        "",
        "## Por dia y sesion: la zona del productor, la orden y por que no la hay",
    ]
    for x in resumen["por_dia"]:
        lineas.append(
            f"- {x['dia']} {x['sesion']} (trader {x['operaciones_trader']}) | toma {x['toma']} "
            f"({x['toma_sesion']}) | zona {x['zona']} | orden {x['orden']}"
            f"{' ' + x['rechazo'] if x['rechazo'] else ''}"
            f"{' | sin orden: ' + x['sin_orden'] if x['sin_orden'] else ''}"
            f"{' | RN-005: ' + x['ruido'] if x['sin_orden'] and x['ruido'] else ''}"
            f"{' | posicion ' + x['posicion'] if x['posicion'] else ''}"
        )
    lineas += ["", "## Por operacion"]
    for f in filas:
        b = f["bot"]
        z = b["zona"]
        zona = (
            "sin zona"
            if z is None
            else f"zona {z['lado']} 0={z['cero']} caja {z['caja']} {z['formada']}"
        )
        alt = f["alternativa"]
        alt_txt = ""
        if alt is not None:
            e = alt["esquema"]
            alt_txt = f" | alternativa toma {alt['toma']}: " + (
                "sin esquema" if e is None else f"{e['puntos']} pts, {e['min']} min"
            )
        lineas.append(
            f"- {f['dia']} {f['sesion']} {f['instante']} {f['direccion']} {f['entrada']} | "
            f"{f['paso']}: {f['motivo']}{(' (' + f['detalle'] + ')') if f['detalle'] else ''} | "
            f"sesgo {b['sesgo']} toma {b['toma']} ({b['toma_sesion']}) {zona} orden {b['orden']}"
            f"{alt_txt}"
        )
    return "\n".join(lineas) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--a21", required=True)
    p.add_argument("--a27", type=int, default=0)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    p.add_argument("--salida", type=Path, required=True)
    p.add_argument(
        "--cuenta-diaria",
        action="store_true",
        help="DIAGNOSTICO: la cuenta simulada empieza de cero cada dia (sin arrastrar frenos)",
    )
    args = p.parse_args(argv)
    filas, resumen = medir(args.raiz, args.a21, args.a27, args.cuenta_diaria)
    args.salida.with_suffix(".txt").write_text(
        informe(filas, resumen), encoding="utf-8", newline="\n"
    )
    args.salida.with_suffix(".json").write_text(
        json.dumps({"resumen": resumen, "filas": filas}, indent=1, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(json.dumps(Counter(f["paso"] for f in filas)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
