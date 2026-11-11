"""Las laminas del bot (rama `trabajo/laminas`, R4.5; RUMBO-2026-11.md §3): lo que hizo el bot y
por que, en el idioma del trader, recortado al instante de decidir. DIAGNOSTICO DE CONSTRUCCION.

**Una sola fuente.** Todo lo que la lamina atribuye al bot sale de la corrida del motor por su
observador pasivo (`MotorCableado.observador`), como la bitacora de `engine/decisiones.py`: el
`Recolector` recibe cada cierre de M1 ya decidido y, en los cierres que pueden ser un corte, saca
una FOTO, un dataclass congelado con COPIAS de lo que el motor tenia en ese instante (las velas de
la ventana, los hechos, las anotaciones, la memoria de la sesion, las ordenes y posiciones, las
prohibiciones del evento). Nada guarda una referencia a `estado`, `broker`, `ctx` ni a la memoria, y
el dibujo (`engine/laminas_svg.py`) solo recibe fotos: no recalcula ninguna decision. Lo que el
observador no veia antes de esta rama -que H4 fija el sesgo y cuales salta, que zonas de control
cuenta RN-009- lo anotan el dominio y las primitivas como REGISTRO: nada lo lee para decidir.

**Que laminas** (encargo, punto 2): (a) por cada orden del bot que se lleno en la sesion, la foto
del ultimo cierre en que se coloco o se movio al precio al que se lleno; (b) por cada operacion del
trader de la sesion que el criterio (ADR-0043) no empareja, la foto del cierre `t` mas tardio con
`t * 60 000 < su entrada en ms`, sin la operacion del trader. El emparejamiento es el de
`decisiones.resumir` sobre la corrida entera.

**Negar por defecto** (punto 6): todo minuto con una vela, en el huso de las sesiones y en UTC, cae
en un tramo de construccion de `cobertura_material` y fuera de `casos_ocultos` (`Puerta`); la
ventana se recorta hacia atras hasta el primer minuto que no cumple. Lo que no es vela se dibuja o
se nombra con su precio solo si nace dentro de la ventana de su panel mas ancho. Un dia, una sesion,
un corte o una causa que no cumple: `LaminaError`, y no se escribe nada.

**Las cifras:** el 0,8 es `stop_fraccion_caja` del registro, el huso el de las sesiones, el anclaje
`anclaje_h4`; las ventanas (cuatro dias de H4, uno de M15, una hora de M1) son constantes de dibujo
que no deciden nada (respuesta del consultor a la fase 0, punto 7)."""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from botsito.cases.criterio_fidelidad import Operacion, Tolerancias
from botsito.domain.pivotes_m15 import ALTO, BAJO
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import Vela
from botsito.engine.cableado import Cierre, MotorCableado

# ---------------------------------------------------------------- constantes de dibujo (punto 7)

DIAS_H4 = 4  # el panel de H4 empieza a las 00:00 (huso de las sesiones) de cuatro dias antes
DIAS_M15 = 1  # el de M15, a las 00:00 del dia anterior
MINUTOS_ANTES_M1 = 60  # el de M1, una hora antes de la sesion
PREFIJO_DETENIDO = "detenido_por_"
ESTADOS_VIVOS = ("colocada", "modificada")


class LaminaError(ValueError):
    """La lamina no se puede hacer sin romper una de sus reglas: no se escribe nada."""


# ------------------------------------------------------------------------------------ la puerta


@dataclass(frozen=True)
class Puerta:
    """Lo que se puede ensenar (punto 6): los tramos de construccion de `cobertura_material`, los
    dias de `casos_ocultos` (mes, dia) y el huso de las sesiones."""

    tramos: tuple[tuple[date, date], ...]
    ocultos: frozenset[tuple[int, int]]
    huso: str

    def dia_permitido(self, d: date) -> bool:
        return any(a <= d <= b for a, b in self.tramos) and (d.month, d.day) not in self.ocultos

    def permitido(self, minuto: int) -> bool:
        """El minuto cae, en el huso de las sesiones y en UTC, en un dia permitido."""
        t = datetime.fromtimestamp(minuto * 60, UTC)
        local = t.astimezone(ZoneInfo(self.huso))
        return self.dia_permitido(t.date()) and self.dia_permitido(local.date())

    def recorte(self, desde: int, ultimo: int) -> int:
        """El primer minuto de [desde, ultimo] desde el que TODO esta permitido; si `ultimo` no lo
        esta, `LaminaError`."""
        if not self.permitido(ultimo):
            raise LaminaError("el corte no cae en un tramo de construccion libre")
        m = ultimo
        while m - 1 >= desde and self.permitido(m - 1):
            m -= 1
        return m


def puerta_de(
    cobertura: Mapping[str, Sequence[tuple[str, str]]],
    meses: Iterable[str],
    ocultos: Iterable[tuple[int, int]],
    huso: str,
) -> Puerta:
    """La puerta con los tramos de `cobertura_material` de los meses de construccion (respuesta
    del consultor a la fase 0, punto 3: el 30 de abril queda fuera, el libro no lo cubre)."""
    tramos: list[tuple[date, date]] = []
    for mes in meses:
        if mes not in cobertura:
            raise LaminaError(f"{mes}: mes de construccion sin cobertura_material")
        tramos += [(date.fromisoformat(a), date.fromisoformat(b)) for a, b in cobertura[mes]]
    return Puerta(tuple(sorted(tramos)), frozenset(ocultos), huso)


# -------------------------------------------------------------------------------------- la foto


@dataclass(frozen=True)
class OrdenFoto:
    id: str
    lado: str
    precio: int
    stop: int
    objetivo: int
    colocada_ms: int
    estado: str
    sesion: str | None  # la sesion del cierre en que se coloco (`ContextoDia.sesion_de_orden`)
    zona: str | None


@dataclass(frozen=True)
class PosicionFoto:
    orden_id: str
    abierta_ms: int
    cerrada_ms: int | None
    motivo_cierre: str | None


@dataclass(frozen=True)
class ZonaFoto:
    id: str
    lado: str
    entrada: int  # el 0
    extremo: int  # el 1
    por: str
    desde: int | None
    formada: int | None


@dataclass(frozen=True)
class TomaFoto:
    instante: int  # el cierre de la M1 que toma
    lado: str  # compra | venta
    pivote_lado: str  # alto | bajo
    pivote_nivel: int
    pivote_formado: int


@dataclass(frozen=True)
class EscenarioFoto:
    n: int
    toma: TomaFoto
    zonas: tuple[str, ...]
    terminado: str | None


@dataclass(frozen=True)
class LineaM15:
    """Un pivote de M15 que el motor tuvo como liquidez en algun cierre de la sesion hasta el
    corte (`DatosMercado.liquidez_m15`, de los dos lados)."""

    lado: str  # alto | bajo
    nivel: int
    contraria_inicio: int  # su nacimiento: la vela contraria que lo marca
    formado_en: int
    primera: int  # primer cierre en que era la liquidez
    ultima: int  # ultimo cierre (hasta el corte) en que lo era


@dataclass(frozen=True)
class Foto:
    """Lo que el motor tenia en el cierre `corte` (minuto UTC del cierre de la ultima M1), en
    copias. Las velas de M1 van de `desde_h4` (el panel mas ancho, ya recortado) al corte."""

    dia: str
    sesion: str | None
    corte: int
    huso: str
    escala: int
    limites: tuple[tuple[str, int, int], ...]  # (sesion, desde, hasta) del dia, por la puerta
    desde_h4: int
    desde_m15: int
    desde_m1: int
    m1: tuple[Vela, ...]
    hechos: tuple[tuple[str, str], ...]
    origen: tuple[tuple[str, tuple[str, ...]], ...]  # hecho -> reglas que lo encendieron
    broker: tuple[tuple[str, str], ...]
    anotaciones: tuple[tuple[str, str], ...]
    escenarios: tuple[EscenarioFoto, ...]
    zonas: tuple[ZonaFoto, ...]
    puntos: tuple[tuple[str, str], ...]  # zona -> "nivel@inicio"
    usadas: frozenset[str]
    rechazados: frozenset[str]
    ordenes: tuple[OrdenFoto, ...]
    colocadas: frozenset[str]  # ordenes que nacen en este cierre
    movidas: frozenset[str]  # ordenes que cambian de precio en este cierre
    posiciones: tuple[PosicionFoto, ...]
    lineas: tuple[LineaM15, ...]
    prohibido: tuple[tuple[str, tuple[str, ...]], ...]  # efecto -> gates que disparan
    quizas: tuple[tuple[str, tuple[str, ...]], ...]  # efecto -> gates desconocidos
    bloqueos: tuple[tuple[str, str, str, tuple[tuple[str, str], ...]], ...]
    disparadas: tuple[str, ...]
    no_enviadas: tuple[tuple[int, str, str], ...]  # (ms, zona, motivo) de este cierre

    def hecho(self, nombre: str) -> str | None:
        return dict(self.hechos).get(nombre)

    def anotacion(self, nombre: str) -> str | None:
        return dict(self.anotaciones).get(nombre)

    def zona(self, zid: str | None) -> ZonaFoto | None:
        return next((z for z in self.zonas if z.id == zid), None)

    def orden(self, oid: str) -> OrdenFoto | None:
        return next((o for o in self.ordenes if o.id == oid), None)


@dataclass(frozen=True)
class Lectura:
    """Lo que la lamina lee del registro para decir y dibujar: la opcion de la toma que nombra la
    forma de RN-004, el 0,8, el tope de zonas de control de RN-009, el anclaje de las H4 y cuando
    vuelve a contar el trader su perdida (la frase de RN-020 lo da por cierto)."""

    criterio_toma: str
    stop_fraccion: Decimal
    zonas_max: int
    anclaje: Any  # HoraLocal
    reinicio_trader: str
    alcance_trader: str  # perdida_trader_alcance: con semana o ambos, RN-020 no es solo «del dia»


# ---------------------------------------------------------------------------------- el recolector


@dataclass(frozen=True)
class Pedida:
    n: int  # el orden en --sesiones, desde 1
    dia: str
    sesion: str


@dataclass
class _DiaRec:
    precios: dict[str, int] = field(default_factory=dict)
    hechos: dict[str, str] = field(default_factory=dict)
    origen: dict[str, tuple[str, ...]] = field(default_factory=dict)
    lineas: dict[str, dict[tuple[str, int, int, int], list[int]]] = field(default_factory=dict)
    no_enviadas: int = 0


def ventanas(dia: date, desde_sesion: int, huso: str) -> tuple[int, int, int]:
    """El primer minuto (UTC) de cada panel SIN recortar: H4, M15 y M1."""
    tz = ZoneInfo(huso)

    def minuto(d: date) -> int:
        return int(datetime.combine(d, time(), tzinfo=tz).timestamp()) // 60

    return (
        minuto(dia - timedelta(days=DIAS_H4)),
        minuto(dia - timedelta(days=DIAS_M15)),
        desde_sesion - MINUTOS_ANTES_M1,
    )


class Recolector:
    """El observador de `MotorCableado` para las laminas. En los dias pedidos acumula las lineas de
    M15 de cada sesion y el origen de cada freno, y saca una `Foto` en cada cierre en que una orden
    nace o cambia de precio y en cada corte de tipo b. Solo LEE el cierre y solo guarda copias."""

    def __init__(
        self,
        dias: Mapping[str, tuple[tuple[str, int, int], ...]],
        cortes_b: Mapping[str, frozenset[int]],
        puerta: Puerta,
    ) -> None:
        self.dias = dict(dias)  # dia -> limites de sus sesiones
        self.cortes_b = dict(cortes_b)
        self.puerta = puerta
        self.fotos_a: dict[tuple[str, str], Foto] = {}  # (dia, orden) -> la ultima
        self.fotos_b: dict[tuple[str, int], Foto] = {}  # (dia, corte)
        self._dias: dict[str, _DiaRec] = {}

    def __call__(self, c: Cierre) -> None:
        if c.dia not in self.dias:
            return
        d = self._dias.setdefault(c.dia, _DiaRec())
        self._origen(d, c)
        if c.sesion is not None:
            self._lineas(d, c)
        colocadas, movidas = set(), set()
        for oid, o in c.broker.ordenes.items():
            antes = d.precios.get(oid)
            if antes is None:
                colocadas.add(oid)
            elif antes != int(o.precio):
                movidas.add(oid)
            d.precios[oid] = int(o.precio)
        nuevas = tuple(
            (int(ms), str(z), str(m)) for ms, z, m, _ in c.ctx.no_enviadas[d.no_enviadas :]
        )
        d.no_enviadas = len(c.ctx.no_enviadas)
        de_b = c.instante in self.cortes_b.get(c.dia, frozenset())
        if not (colocadas or movidas or de_b):
            return
        foto = self._foto(d, c, frozenset(colocadas), frozenset(movidas), nuevas)
        for oid in colocadas | movidas:
            self.fotos_a[(c.dia, oid)] = foto
        if de_b:
            self.fotos_b[(c.dia, c.instante)] = foto

    def _origen(self, d: _DiaRec, c: Cierre) -> None:
        """Quien encendio cada freno: las reglas que lo fijan en el cierre en que se enciende
        (`Evento.fijados`), nunca por el hecho solo."""
        fijan: dict[str, set[str]] = {}
        for regla, hecho, _ in c.evento.fijados:
            fijan.setdefault(str(hecho), set()).add(str(regla))
        ahora = {str(h): str(v) for h, v in c.estado.hechos.items()}
        for h, v in ahora.items():
            if h.startswith(PREFIJO_DETENIDO) and d.hechos.get(h) != v:
                d.origen[h] = tuple(sorted(fijan.get(h, set())))
        for h in set(d.hechos) - set(ahora):
            d.origen.pop(h, None)
        d.hechos = ahora

    def _lineas(self, d: _DiaRec, c: Cierre) -> None:
        sesion = str(c.sesion)
        lineas = d.lineas.setdefault(sesion, {})
        for lado in (ALTO, BAJO):
            p = c.datos.liquidez_m15(c.instante, lado)
            if p is None:
                continue
            clave = (str(p.lado), int(p.nivel), int(p.contraria_inicio), int(p.formado_en))
            vista = lineas.setdefault(clave, [c.instante, c.instante])
            vista[1] = c.instante

    def _foto(
        self,
        d: _DiaRec,
        c: Cierre,
        colocadas: frozenset[str],
        movidas: frozenset[str],
        no_enviadas: tuple[tuple[int, str, str], ...],
    ) -> Foto:
        limites = self.dias[c.dia]
        sesion = c.sesion
        desde_sesion = next(
            (a for n, a, _ in limites if n == sesion), min(a for _, a, _ in limites)
        )
        sin_recortar = ventanas(date.fromisoformat(c.dia), desde_sesion, c.huso)
        ultimo = c.instante - 1  # el inicio de la ultima M1, la del corte
        h4, m15, m1 = (self.puerta.recorte(x, ultimo) for x in sin_recortar)
        mem_dia: Mapping[str, Any] = c.estado.memoria.get("zona_de_entrada", {})
        por_sesion: Mapping[str, Any] = mem_dia.get("por_sesion", {})
        mem: Mapping[str, Any] = por_sesion.get(sesion, {}) if sesion is not None else {}
        escenarios = tuple(
            EscenarioFoto(
                int(e["n"]),
                _toma(e["toma"]),
                tuple(sorted(str(z) for z in e["zonas"])),
                None if e["terminado"] is None else str(e["terminado"]),
            )
            for e in mem.get("escenarios", []) or []
        )
        zonas = tuple(
            ZonaFoto(
                str(z.id), str(z.lado), int(z.entrada), int(z.extremo), str(z.por),
                None if z.desde is None else int(z.desde),
                None if z.formada is None else int(z.formada),
            )
            for z in (mem_dia.get("zonas", {}) or {}).values()
        )  # fmt: skip
        puntos: dict[str, str] = {}
        for m in por_sesion.values():
            puntos.update({str(k): str(v) for k, v in (m.get("punto_de_zona") or {}).items()})
        ordenes = tuple(
            OrdenFoto(
                str(o.id), str(o.lado), int(o.precio), int(o.stop), int(o.objetivo),
                int(o.colocada_ms), str(o.estado), c.ctx.sesion_de_orden.get(o.id),
                c.ctx.zona_de_orden.get(o.id),
            )
            for o in c.broker.ordenes.values()
        )  # fmt: skip
        posiciones = tuple(
            PosicionFoto(
                str(p.orden_id), int(p.abierta_ms),
                None if p.cerrada_ms is None else int(p.cerrada_ms),
                None if p.motivo_cierre is None else str(p.motivo_cierre),
            )
            for p in c.broker.posiciones.values()
        )  # fmt: skip
        lineas = tuple(
            LineaM15(lado, nivel, inicio, formado, vista[0], vista[1])
            for (lado, nivel, inicio, formado), vista in sorted(
                d.lineas.get(str(sesion), {}).items()
            )
        )
        ev = c.evento
        return Foto(
            dia=c.dia,
            sesion=sesion,
            corte=c.instante,
            huso=c.huso,
            escala=c.escala,
            limites=tuple(limites),
            desde_h4=h4,
            desde_m15=m15,
            desde_m1=m1,
            m1=tuple(c.datos.m1_entre(min(h4, m15, m1), c.instante)),
            hechos=tuple(sorted((str(k), str(v)) for k, v in c.estado.hechos.items())),
            origen=tuple(sorted(d.origen.items())),
            broker=tuple(sorted((str(k), str(v)) for k, v in c.estado.broker.items())),
            anotaciones=tuple(
                sorted(
                    (str(k), str(v)) for k, v in c.estado.anotaciones.get(str(sesion), {}).items()
                )
            ),
            escenarios=escenarios,
            zonas=zonas,
            puntos=tuple(sorted(puntos.items())),
            usadas=frozenset(str(z) for z in mem.get("usadas", set()) or set()),
            rechazados=frozenset(str(p) for p in mem.get("rechazados", set()) or set()),
            ordenes=ordenes,
            colocadas=colocadas,
            movidas=movidas,
            posiciones=posiciones,
            lineas=lineas,
            prohibido=tuple(
                sorted((str(e), tuple(map(str, g))) for e, g in ev.prohibido_por.items())
            ),
            quizas=tuple(sorted((str(e), tuple(map(str, g))) for e, g in ev.quizas_por.items())),
            bloqueos=tuple(
                sorted(
                    (
                        str(r),
                        str(a),
                        str(m),
                        tuple((str(g), str(t)) for g, t in ev.bloqueada_por.get((r, a, m), ())),
                    )
                    for r, a, m in ev.bloqueadas
                )
            ),
            disparadas=tuple(sorted(str(r) for r in ev.disparadas)),
            no_enviadas=no_enviadas,
        )


def _toma(t: Mapping[str, Any]) -> TomaFoto:
    lado_p, nivel_p, formado_p = t["pivote"]
    return TomaFoto(int(t["instante"]), str(t["lado"]), str(lado_p), int(nivel_p), int(formado_p))


# ------------------------------------------------------------------------- la tabla de frases

# La tabla cerrada de la fase 0 (§0.3), aprobada con los cambios de la respuesta del consultor
# (punto 12). La clave la usa el codigo; la salida solo lleva la frase. Sin ids, lote, R, dinero
# ni porcentajes: lo comprueba `comprobar_texto` en cada byte de cada lamina.
SESGO_ALCISTA = "alcista"
SESGO_BAJISTA = "bajista"
FRASE_SESGO = {
    (SESGO_ALCISTA, False): "Sesgo de H4 alcista: la vela H4 que lo fija rompió el alto de la "
    "anterior y cerró verde.",
    (SESGO_ALCISTA, True): "Sesgo de H4 alcista: la vela H4 que lo fija rompió los dos extremos "
    "de la anterior y cerró verde.",
    (SESGO_BAJISTA, False): "Sesgo de H4 bajista: la vela H4 que lo fija rompió el bajo de la "
    "anterior y cerró roja.",
    (SESGO_BAJISTA, True): "Sesgo de H4 bajista: la vela H4 que lo fija rompió los dos extremos "
    "de la anterior y cerró roja.",
    ("insuficiente", False): "Sin sesgo de H4: ninguna de las velas H4 que mira hacia atrás rompe "
    "un extremo de la anterior cerrando de ese color.",
    ("ambiguo", False): "Sesgo de H4 ambiguo.",
}
# por motivo de la saltada (`domain.sesgo`): (una, varias)
FRASE_SALTADAS = {
    "color_contrario": (
        "Antes de esa vela, el bot se saltó una vela H4 que rompió un extremo y cerró del color "
        "contrario.",
        "Antes de esa vela, el bot se saltó {n} velas H4 que rompieron un extremo y cerraron del "
        "color "
        "contrario.",
    ),
    "neutra_simple": (
        "Antes de esa vela, el bot se saltó una vela H4 que rompió un extremo y cerró sin cuerpo.",
        "Antes de esa vela, el bot se saltó {n} velas H4 que rompieron un extremo y cerraron sin "
        "cuerpo.",
    ),
    "neutra_doble": (
        "Antes de esa vela, el bot se saltó una vela H4 que rompió los dos extremos y cerró sin "
        "cuerpo.",
        "Antes de esa vela, el bot se saltó {n} velas H4 que rompieron los dos extremos y cerraron "
        "sin "
        "cuerpo.",
    ),
}
FRASE_FIJA_FUERA = "La vela H4 que fija el sesgo viene de antes de la ventana."
FRASE_DETENIDO = {
    "detenido_por_cartuchos": "Ya ha gastado sus intentos en esta liquidez: espera otra liquidez "
    "de M15.",
    "detenido_por_tope_total": "La cuenta ha llegado a su freno total: no opera más.",
    "detenido_por_racha": "Tras la racha de pérdidas seguidas del trader, no opera más hoy.",
}
# detenido_por_tope lo fijan dos reglas: la frase sale de la que lo encendio (respuesta, punto 12)
FRASE_TOPE_POR_REGLA = {
    "RN-020": "Ha llegado a la pérdida máxima del día del trader: no abre más hasta la primera "
    "sesión del día siguiente.",
    "RN-029": "Ha saltado el freno diario de la cuenta: no abre más hasta el cambio de día de la "
    "cuenta.",
}
HECHO_TOPE = "detenido_por_tope"
REINICIO_TRADER = "primera_sesion_dia_siguiente"  # el valor que la frase de RN-020 da por cierto
# Con estos alcances la rama semanal de RN-020 no dispara (`acumulador_del_trader` da NO a
# `perdida_semana`, primitivas_broker.py:360-362), y la frase y el motivo dicen «del dia» con
# verdad; con `semana` o `ambos`, error que lo nombra (respuesta a la PARADA final, punto 2)
ALCANCES_SOLO_DIA = ("dia", "sin_tope")
HECHOS_SIN_FRASE = ("orden_dimensionada",)  # la marca interna de la orden preparada
# Toda hora que nombra una vela es la de su APERTURA, como la rotula FX Replay (respuesta del
# consultor tras revisar la v3, punto 2); la cabecera nombra el corte y la vela, cada uno el suyo
FRASE_TOMA = "La vela de M1 de las {hora} cerró con {criterio} por {lado} de M15 en {precio}."
CRITERIO_TOMA = {"cuerpo": "cuerpo", "mecha": "mecha"}
LADO_TOMA = {BAJO: "debajo del bajo", ALTO: "encima del alto"}
FRASE_TOMA_LINEA_FUERA = (
    "La vela de M1 de las {hora} tomó la liquidez de M15: la línea que toma viene de antes de la "
    "ventana."
)
FRASE_TOMA_FUERA = "La toma de la liquidez de M15 viene de antes de la ventana."
FRASE_SIN_TOMA = "Todavía no ha tomado la liquidez de M15 en esta sesión."
FRASE_ESCENARIO = "Sigue la liquidez de M15 número {n} de esta sesión."
FRASE_LINEAS_FUERA = (
    "Una línea de M15 de esta sesión viene de antes de la ventana.",
    "{n} líneas de M15 de esta sesión vienen de antes de la ventana.",
)
# Sin frase del esquema (respuesta del consultor a la PARADA final, punto 1): con la orden en el
# punto, `zona_del_punto` crea toda zona con `por = primer_esquema` (zonas.py:414-416), asi que
# decirlo seria afirmar un esquema que el motor no ha distinguido. Vuelve cuando lo distinga.
FRASE_CAJA = "La caja va de {cero} (el 0) a {uno} (el 1)."
FRASE_CAJA_FUERA = "La caja viene de antes de la ventana."
FRASE_PUNTO = "El punto de breaker está en {precio}, de la vela de las {hora}."
FRASE_PUNTO_FUERA = "El punto de breaker viene de antes de la ventana."
LADO_ORDEN = {"compra": "compra", "venta": "venta"}
FRASE_ORDEN = {
    "colocada": "Coloca la orden de {lado} en {precio}, el 0 de la caja, con el stop en {stop} "
    "(el {fraccion} redondeado) y el objetivo en {objetivo}.",
    "movida": "Mueve la orden de {lado} a {precio}, el 0 de la caja, con el stop en {stop} (el "
    "{fraccion} redondeado) y el objetivo en {objetivo}.",
    "viva": "Tiene una orden de {lado} pendiente en {precio}, el 0 de la caja, con el stop en "
    "{stop} (el {fraccion} redondeado) y el objetivo en {objetivo}.",
}
CIERRE_ANTES = {"stop": "en el stop", "objetivo": "en el objetivo", "manual": "a mercado"}
FRASE_CERRADAS = "Antes, en esta sesión: {partes}."
FRASE_RETIRADAS = (
    "Una orden anterior se retiró sin llenarse.",
    "{n} órdenes anteriores se retiraron sin llenarse.",
)
FRASE_RECHAZADAS = (
    "El bróker rechazó una orden anterior.",
    "El bróker rechazó {n} órdenes anteriores.",
)
FRASE_STOPS_LIQUIDEZ = (
    "En esta liquidez ya lleva un stop.",
    "En esta liquidez ya lleva {n} stops.",
)
ESTADOS_RETIRADA = ("cancelada", "expirada")
ESTADO_RECHAZADA = "rechazada"
MOTIVO_STOP = "stop"
# El motivo de cada gate VIGENTE que puede prohibir (los 15 de la spec con `prohibe`)
MOTIVO_GATE = {
    "RN-001": "está fuera de la ventana de la sesión",
    "RN-037": "es el último minuto antes de que cierre la vela H4 de la sesión",
    "RN-033": "no hay sesgo de H4 claro",
    "RN-005": "lo que se forma queda en la zona de ruido de la liquidez de M15, donde no se busca "
    "entrada",
    "RN-008": "no se da ninguno de los dos esquemas de entrada",
    "RN-009": "el esquema tiene más zonas de control de las que admite ({n}, y admite {m})",
    "RN-016": "ya ha gastado sus intentos en esta liquidez",
    "RN-018": "ya tiene una operación abierta, y no opera en paralelo",
    "RN-020": "ha llegado a la pérdida máxima del día del trader",
    "RN-036": "viene de la racha de pérdidas seguidas del trader",
    "RN-022": "la situación no encaja en lo que sabe hacer",
    "RN-026": "el bróker no admite el stop donde toca",
    "RN-029": "ha saltado el freno diario de la cuenta",
    "RN-031": "ha saltado el freno total de la cuenta",
    "RN-032": "el riesgo de la operación no cabe antes del límite de la cuenta",
}
GATE_ZONAS_CONTROL = "RN-009"
EFECTOS = ("abrir_operacion", "buscar_entradas")
ACCION_COLOCAR = "accion:colocar_orden_limite"
FRASE_PROHIBE = {
    "dispara": "No abre: {motivo}.",
    "desconocido": "No abre porque no puede descartar que {motivo}.",
}
FRASE_BLOQUEO = "Iba a colocar la orden y no la coloca: {motivo}."
LIMITE_NO_ENVIO = {
    "volumen": "por el volumen máximo",
    "margen": "por el margen",
    "minimo": "por debajo del mínimo",
}
PREFIJO_NO_OPERAR = "no_operar:"
FRASE_NO_ENVIADA = "Iba a colocar la orden y no la envía: no cabe en la cuenta ({limites})."
FRASE_OPERACION_ABIERTA = "Tiene una operación abierta."
FRASE_TERMINADO = {
    "ganancia": "Este escenario ya terminó con una ganadora: espera otra liquidez de M15.",
}
FRASE_SIN_CAJA = (
    "Ha tomado la liquidez, pero aún no se ha formado ninguna caja con su breaker en este "
    "escenario."
)
FRASE_SIN_PUNTO = "La caja no tiene punto de breaker."
FRASE_USADA = "Esa caja ya tuvo su orden."
FRASE_PUNTO_GASTADO = "Ese punto ya se gastó: el bróker rechazó la orden."
FRASE_NO_TOCABA = "Con la caja formada, todavía no le toca colocar la orden."
REGLAS_QUE_COLOCAN = ("RN-011", "RN-015")
HECHO_LIQUIDEZ = "liquidez_tomada"
HECHO_SESGO = "sesgo"
SI = "si"
BROKER_OPERACION = "operacion_abierta"
BROKER_PENDIENTE = "orden_limite_pendiente"
VERDADERO = ("True", "si")


def _plural(par: tuple[str, str], n: int) -> str:
    return par[0] if n == 1 else par[1].format(n=n)


def precio(puntos: int, escala: int) -> str:
    decimales = len(str(escala)) - 1
    return f"{Decimal(puntos) / Decimal(escala):.{decimales}f}"


def hora(minuto: int, huso: str) -> str:
    """HH:MM en el huso de las sesiones."""
    return f"{datetime.fromtimestamp(minuto * 60, UTC).astimezone(ZoneInfo(huso)):%H:%M}"


def fraccion(valor: Decimal) -> str:
    """El 0,8 como lo escribe el trader."""
    return format(valor.normalize(), "f").replace(".", ",")


# ----------------------------------------------------------------------- de la foto al dibujo

TIPO_A = "a"  # una orden del bot que se lleno
TIPO_B = "b"  # una operacion del trader sin pareja


@dataclass(frozen=True)
class Lamina:
    pedida: Pedida
    tipo: str
    foto: Foto
    orden: str | None = None  # la orden de la lamina (tipo a)


@dataclass(frozen=True)
class LineaDibujada:
    lado: str
    nivel: int
    desde: int  # minuto de nacimiento (la vela contraria)
    hasta: int  # minuto UTC del cierre en que acaba
    tomada: bool
    dejo: bool  # dejo de ser la liquidez antes del corte, sin tomarse


@dataclass(frozen=True)
class Dibujo:
    """Lo que pinta `laminas_svg`, ya cortado y pasado por la puerta: solo sale de la foto."""

    corte: int
    huso: str
    escala: int
    h4: tuple[Vela, ...]
    m15: tuple[Vela, ...]
    m1: tuple[Vela, ...]
    h4_fija: int | None  # inicio de la H4 que fija el sesgo, si esta dentro
    h4_saltadas: tuple[int, ...]
    lineas: tuple[LineaDibujada, ...]
    toma: tuple[int, int] | None  # (inicio de la M1 que toma, nivel)
    caja: ZonaFoto | None
    niveles: tuple[tuple[str, int], ...]  # rotulo -> nivel, de la caja
    punto: tuple[int, int] | None  # (inicio de su vela, nivel)
    control: tuple[tuple[int, int], ...]  # (inicio de la vela contraria, nivel) de RN-009
    ordenes: tuple[OrdenFoto, ...]


@dataclass(frozen=True)
class Composicion:
    dibujo: Dibujo
    frases: tuple[str, ...]
    fija_dentro: bool | None  # la H4 que fija el sesgo, dentro de la ventana (decision 9)


def _paneles(foto: Foto, lectura: Lectura) -> tuple[tuple[Vela, ...], ...]:
    from botsito.cases.ventanas import MINUTOS_H4, MINUTOS_M15
    from botsito.data.agregacion import agregar

    salida = []
    for desde, minutos in (
        (foto.desde_h4, MINUTOS_H4),
        (foto.desde_m15, MINUTOS_M15),
        (foto.desde_m1, 1),
    ):
        # solo lo de la ventana y ANTES del corte, aunque la foto trajera mas
        propias = [v for v in foto.m1 if desde <= int(v.inicio) < foto.corte]
        velas = propias if minutos == 1 else agregar(propias, minutos, lectura.anclaje)
        salida.append(tuple(v for v in velas if int(v.inicio) >= desde))
    return tuple(salida)


def _lista(texto: str | None) -> list[tuple[int, str]]:
    """`inicio:motivo,...` (o `nivel@inicio,...`) de una anotacion de registro."""
    if not texto:
        return []
    salida = []
    for parte in texto.split(","):
        a, b = parte.split(":") if ":" in parte else parte.split("@")
        salida.append((int(a), b))
    return salida


def componer(lam: Lamina, lectura: Lectura) -> Composicion:
    """El dibujo y la sustentacion de una lamina, solo desde su foto. Una causa o un valor sin
    frase: `LaminaError` con su nombre (negar por defecto)."""
    from botsito.engine.primitivas import (
        ANOTACION_DOBLE_RUPTURA,
        ANOTACION_SALTADAS_COLOR,
        ANOTACION_SALTADAS_NEUTRA_DOBLE,
        ANOTACION_SALTADAS_NEUTRA_SIMPLE,
        ANOTACION_SESGO,
        ANOTACION_SESGO_SALTADAS,
        ANOTACION_SESGO_VELA,
    )
    from botsito.engine.zonas import ANOTACION_ZONAS_CONTROL

    f = lam.foto
    h4, m15, m1 = _paneles(f, lectura)
    frases: list[str] = []

    def dentro(nacimiento: int | None, desde: int) -> bool:
        """`nacimiento` es el INICIO de la vela en que nace (no un cierre)."""
        return nacimiento is not None and desde <= nacimiento < f.corte

    def linea_dentro(ln: LineaM15) -> bool:
        """Una linea de M15 nace con su vela contraria, pero su nivel es el extremo de la racha
        de antes (el pivote de origen, punto 6 del encargo): sale solo si las dos cosas estan en
        la ventana de M15, la contraria y una M1 que marque ese nivel antes de que se forme
        (revisor, b-I3). Si una M1 de la ventana lo marca, el precio ya se ve en una vela."""
        if not dentro(ln.contraria_inicio, f.desde_m15):
            return False
        return any(
            f.desde_m15 <= int(v.inicio) < ln.formado_en
            and int(v.maxima if ln.lado == ALTO else v.minima) == ln.nivel
            for v in f.m1
        )

    # el sesgo y sus H4
    sesgo = f.hecho(HECHO_SESGO)
    anotado = f.anotacion(ANOTACION_SESGO)
    if sesgo is None or anotado != sesgo:
        raise LaminaError(f"el sesgo del hecho ({sesgo}) y el anotado ({anotado}) no casan")
    doble = f.anotacion(ANOTACION_DOBLE_RUPTURA) == SI
    if (sesgo, doble) not in FRASE_SESGO:
        raise LaminaError(f"sesgo {sesgo!r} sin frase")
    frases.append(FRASE_SESGO[(sesgo, doble)])
    vela = f.anotacion(ANOTACION_SESGO_VELA)
    fija = None if vela is None else int(vela)
    inicios_h4 = {int(v.inicio) for v in h4}
    fija_dentro: bool | None = None
    if sesgo in (SESGO_ALCISTA, SESGO_BAJISTA):
        if fija is None:
            raise LaminaError("sesgo con lado sin la H4 que lo fija anotada")
        fija_dentro = fija in inicios_h4
        if not fija_dentro:
            frases.append(FRASE_FIJA_FUERA)
    saltadas = _lista(f.anotacion(ANOTACION_SESGO_SALTADAS))
    for motivo, anotacion in (
        ("color_contrario", ANOTACION_SALTADAS_COLOR),
        ("neutra_simple", ANOTACION_SALTADAS_NEUTRA_SIMPLE),
        ("neutra_doble", ANOTACION_SALTADAS_NEUTRA_DOBLE),
    ):
        n = sum(1 for _, m in saltadas if m == motivo)
        if n != int(f.anotacion(anotacion) or 0):
            raise LaminaError(f"las H4 saltadas por {motivo} no casan con su recuento")
        if n and fija is not None:
            frases.append(_plural(FRASE_SALTADAS[motivo], n))
    if any(m not in FRASE_SALTADAS for _, m in saltadas):
        raise LaminaError("una H4 saltada con un motivo sin frase")
    h4_saltadas = tuple(i for i, _ in saltadas if i in inicios_h4) if fija is not None else ()

    # los frenos
    origen = dict(f.origen)
    for h, v in f.hechos:
        if h in (HECHO_SESGO, HECHO_LIQUIDEZ) or h in HECHOS_SIN_FRASE:
            continue
        if h == HECHO_TOPE:
            reglas = origen.get(h, ())
            if len(reglas) != 1 or reglas[0] not in FRASE_TOPE_POR_REGLA:
                raise LaminaError(f"{h}: no se sabe que regla lo encendio ({', '.join(reglas)})")
            if reglas[0] == "RN-020" and lectura.reinicio_trader != REINICIO_TRADER:
                raise LaminaError(f"perdida_trader_reinicio = {lectura.reinicio_trader}: sin frase")
            if reglas[0] == "RN-020" and lectura.alcance_trader not in ALCANCES_SOLO_DIA:
                raise LaminaError(f"perdida_trader_alcance = {lectura.alcance_trader}: sin frase")
            frases.append(FRASE_TOPE_POR_REGLA[reglas[0]])
        elif h in FRASE_DETENIDO:
            frases.append(FRASE_DETENIDO[h])
        else:
            raise LaminaError(f"hecho {h}={v} sin frase")
    if f.hecho(HECHO_LIQUIDEZ) not in (None, SI):
        raise LaminaError(f"{HECHO_LIQUIDEZ}={f.hecho(HECHO_LIQUIDEZ)} sin frase")

    # la toma y las lineas de M15
    escenario = f.escenarios[-1] if f.escenarios else None
    tomas = {
        (e.toma.pivote_lado, e.toma.pivote_nivel, e.toma.pivote_formado): e.toma
        for e in f.escenarios
    }
    lineas: list[LineaDibujada] = []
    fuera = 0
    for ln in f.lineas:
        if not linea_dentro(ln):
            fuera += 1
            continue
        t = tomas.get((ln.lado, ln.nivel, ln.formado_en))
        if t is not None and t.instante <= f.corte:
            lineas.append(
                LineaDibujada(ln.lado, ln.nivel, ln.contraria_inicio, t.instante, True, False)
            )
        elif ln.ultima < f.corte:
            lineas.append(
                LineaDibujada(ln.lado, ln.nivel, ln.contraria_inicio, ln.ultima, False, True)
            )
        else:
            lineas.append(
                LineaDibujada(ln.lado, ln.nivel, ln.contraria_inicio, f.corte, False, False)
            )
    toma: tuple[int, int] | None = None
    if escenario is None:
        frases.append(FRASE_SIN_TOMA)
    else:
        t = escenario.toma
        if lectura.criterio_toma not in CRITERIO_TOMA or t.pivote_lado not in LADO_TOMA:
            raise LaminaError(f"toma con {lectura.criterio_toma}/{t.pivote_lado}: sin frase")
        toma_con_linea = any(
            (ln.lado, ln.nivel, ln.formado_en)
            == (t.pivote_lado, t.pivote_nivel, t.pivote_formado)
            and linea_dentro(ln)
            for ln in f.lineas
        )  # fmt: skip
        if not dentro(t.instante - 1, f.desde_m15):
            frases.append(FRASE_TOMA_FUERA)
        elif not toma_con_linea:
            frases.append(FRASE_TOMA_LINEA_FUERA.format(hora=hora(t.instante - 1, f.huso)))
        else:
            toma = (t.instante - 1, t.pivote_nivel)
            frases.append(
                FRASE_TOMA.format(
                    criterio=CRITERIO_TOMA[lectura.criterio_toma], lado=LADO_TOMA[t.pivote_lado],
                    precio=precio(t.pivote_nivel, f.escala), hora=hora(t.instante - 1, f.huso),
                )
            )  # fmt: skip
        frases.append(FRASE_ESCENARIO.format(n=escenario.n))
    if fuera:
        frases.append(_plural(FRASE_LINEAS_FUERA, fuera))

    # la orden de la lamina, o las vivas, y la caja que se ensena
    vivas = [o for o in f.ordenes if o.estado in ESTADOS_VIVOS]
    if lam.tipo == TIPO_A:
        o = f.orden(str(lam.orden))
        if o is None:
            raise LaminaError("la orden de la lamina no esta en su foto")
        ordenes = [o]
        clase = "colocada" if o.id in f.colocadas else "movida" if o.id in f.movidas else None
        if clase is None:
            raise LaminaError("la foto de la lamina no es la de una colocacion ni un movimiento")
        clases = {o.id: clase}
    else:
        ordenes = vivas
        clases = {o.id: "viva" for o in vivas}
    zona: ZonaFoto | None = None
    if ordenes:
        zona = f.zona(ordenes[0].zona)
    elif escenario is not None and escenario.zonas:
        candidatas = [z for z in (f.zona(zid) for zid in escenario.zonas) if z is not None]
        zona = max(
            candidatas, key=lambda z: (z.formada or 0, int(z.id.split(":")[-1])), default=None
        )
    caja: ZonaFoto | None = None
    niveles: tuple[tuple[str, int], ...] = ()
    punto: tuple[int, int] | None = None
    if zona is not None:
        # `formada` es el cierre del breaker: nace en la M1 que empieza un minuto antes
        if zona.formada is not None and dentro(zona.formada - 1, f.desde_m1):
            caja = zona
            niveles = _niveles(zona, lectura)
            frases.append(
                FRASE_CAJA.format(
                    cero=precio(zona.entrada, f.escala), uno=precio(zona.extremo, f.escala)
                )
            )
        else:
            frases.append(FRASE_CAJA_FUERA)
        clave_punto = dict(f.puntos).get(zona.id)
        if clave_punto is not None:
            nivel_s, inicio_s = clave_punto.split("@")
            if dentro(int(inicio_s), f.desde_m1):
                punto = (int(inicio_s), int(nivel_s))
                frases.append(
                    FRASE_PUNTO.format(
                        precio=precio(int(nivel_s), f.escala), hora=hora(int(inicio_s), f.huso)
                    )
                )
            else:
                frases.append(FRASE_PUNTO_FUERA)
    for o in ordenes:
        z = f.zona(o.zona)
        if z is None or z.entrada != o.precio or o.lado not in LADO_ORDEN:
            raise LaminaError("una orden sin su caja, fuera del 0 o con un lado sin frase")
        frases.append(
            FRASE_ORDEN[clases[o.id]].format(
                lado=LADO_ORDEN[o.lado], precio=precio(o.precio, f.escala),
                stop=precio(o.stop, f.escala), fraccion=fraccion(lectura.stop_fraccion),
                objetivo=precio(o.objetivo, f.escala),
            )
        )  # fmt: skip

    # lo de antes del corte, en esta sesion
    frases += _antes(f, {o.id for o in ordenes}, escenario)

    # las zonas de control de RN-009 que se evaluaron en este cierre
    control: tuple[tuple[int, int], ...] = ()
    anot = f.anotacion(ANOTACION_ZONAS_CONTROL)
    contadas: int | None = None
    if anot is not None:
        instante_s, _, resto = anot.partition("|")
        if int(instante_s) == f.corte:
            pivotes = [(int(i), int(n)) for n, i in (p.split("@") for p in resto.split(",") if p)]
            contadas = len(pivotes)
            control = tuple((i, n) for i, n in pivotes if dentro(i, f.desde_m1))

    # por que no hay orden (tipo b sin orden viva)
    if lam.tipo == TIPO_B and not vivas:
        frases += _sin_orden(f, escenario, zona, contadas, lectura)

    salida = tuple(dict.fromkeys(frases))  # sin repetir, en su orden
    dibujo = Dibujo(
        f.corte, f.huso, f.escala, h4, m15, m1,
        fija if fija_dentro else None, h4_saltadas, tuple(lineas), toma, caja, niveles, punto,
        control, tuple(ordenes),
    )  # fmt: skip
    return Composicion(dibujo, salida, fija_dentro)


def _niveles(zona: ZonaFoto, lectura: Lectura) -> tuple[tuple[str, int], ...]:
    """Los niveles de la caja como en su Fibonacci: 0, 0,25, 0,5, el 0,8 del registro y 1. Solo
    dibujo: la orden, el stop y el objetivo salen de la foto."""
    fracciones = (
        Decimal(0),
        Decimal("0.25"),  # no-negocio: rotulo del Fibonacci de la caja, solo dibujo
        Decimal("0.5"),  # no-negocio: rotulo del Fibonacci de la caja, solo dibujo
        lectura.stop_fraccion,
        Decimal(1),
    )
    altura = zona.extremo - zona.entrada
    return tuple((fraccion(x), zona.entrada + int(x * altura)) for x in fracciones)


def _antes(f: Foto, propias: set[str], escenario: EscenarioFoto | None) -> list[str]:
    corte_ms = f.corte * MS_POR_MINUTO
    de_la_sesion = {o.id for o in f.ordenes if o.sesion == f.sesion and o.id not in propias}
    frases: list[str] = []
    cerradas: dict[str, int] = {}
    for p in f.posiciones:
        if p.orden_id in de_la_sesion and p.cerrada_ms is not None and p.cerrada_ms < corte_ms:
            if p.motivo_cierre not in CIERRE_ANTES:
                raise LaminaError(f"cierre {p.motivo_cierre!r} sin frase")
            cerradas[str(p.motivo_cierre)] = cerradas.get(str(p.motivo_cierre), 0) + 1
    if cerradas:
        partes: list[str] = []
        for motivo, texto in CIERRE_ANTES.items():
            n = cerradas.get(motivo, 0)
            if n:
                cuantas = f"{n} cerrada{'s' if n != 1 else ''} " if not partes else f"{n} "
                partes.append(cuantas + texto)
        unidas = partes[0] if len(partes) == 1 else ", ".join(partes[:-1]) + " y " + partes[-1]
        frases.append(FRASE_CERRADAS.format(partes=unidas))
    llenadas = {p.orden_id for p in f.posiciones}
    retiradas = sum(
        1
        for o in f.ordenes
        if o.id in de_la_sesion and o.estado in ESTADOS_RETIRADA and o.id not in llenadas
    )
    rechazadas = sum(1 for o in f.ordenes if o.id in de_la_sesion and o.estado == ESTADO_RECHAZADA)
    if retiradas:
        frases.append(_plural(FRASE_RETIRADAS, retiradas))
    if rechazadas:
        frases.append(_plural(FRASE_RECHAZADAS, rechazadas))
    if escenario is not None:
        zonas = set(escenario.zonas)
        stops = sum(
            1 for p in f.posiciones
            if p.motivo_cierre == MOTIVO_STOP
            and p.cerrada_ms is not None and p.cerrada_ms < corte_ms
            and (o := f.orden(p.orden_id)) is not None and o.zona in zonas
        )  # fmt: skip
        if stops:
            frases.append(_plural(FRASE_STOPS_LIQUIDEZ, stops))
    return frases


def _motivo(gate: str, contadas: int | None, lectura: Lectura) -> str:
    if gate not in MOTIVO_GATE:
        raise LaminaError(f"el gate {gate} no tiene frase")
    if gate == "RN-020" and lectura.alcance_trader not in ALCANCES_SOLO_DIA:
        raise LaminaError(f"perdida_trader_alcance = {lectura.alcance_trader}: RN-020 sin frase")
    if gate == GATE_ZONAS_CONTROL:
        if contadas is None:
            raise LaminaError(f"{gate} sin las zonas de control anotadas en el corte")
        return MOTIVO_GATE[gate].format(n=contadas, m=lectura.zonas_max)
    return MOTIVO_GATE[gate]


def _sin_orden(
    f: Foto,
    escenario: EscenarioFoto | None,
    zona: ZonaFoto | None,
    contadas: int | None,
    lectura: Lectura,
) -> list[str]:
    """Por que no hay orden: una lista cerrada de causas, cada una de un campo de la foto."""
    causas: list[str] = []
    sesgo = f.hecho(HECHO_SESGO)
    hay = sesgo not in (SESGO_ALCISTA, SESGO_BAJISTA) or any(
        h.startswith(PREFIJO_DETENIDO) for h, _ in f.hechos
    )
    if str(dict(f.broker).get(BROKER_OPERACION)) == "True":
        causas.append(FRASE_OPERACION_ABIERTA)
    if escenario is None:
        hay = True  # la frase de la toma ya lo dice
    else:
        if escenario.terminado is not None:
            if escenario.terminado not in FRASE_TERMINADO:
                raise LaminaError(f"escenario terminado por {escenario.terminado!r}: sin frase")
            causas.append(FRASE_TERMINADO[escenario.terminado])
        if not escenario.zonas:
            causas.append(FRASE_SIN_CAJA)
        elif zona is not None:
            punto = dict(f.puntos).get(zona.id)
            if punto is None:
                causas.append(FRASE_SIN_PUNTO)
            if zona.id in f.usadas:
                causas.append(FRASE_USADA)
            if punto is not None and punto in f.rechazados:
                causas.append(FRASE_PUNTO_GASTADO)
    bloquean: set[str] = set()  # los gates que bloquean la colocacion en este cierre
    for _, accion, _, gates in f.bloqueos:
        if accion == ACCION_COLOCAR:
            causas += [FRASE_BLOQUEO.format(motivo=_motivo(g, contadas, lectura)) for g, _ in gates]
            bloquean |= {g for g, _ in gates}
    for _, _, motivo in f.no_enviadas:
        partes = motivo.removeprefix(PREFIJO_NO_OPERAR).split("+")
        if not partes or any(p not in LIMITE_NO_ENVIO for p in partes):
            raise LaminaError(f"orden no enviada por {motivo!r}: sin frase")
        causas.append(
            FRASE_NO_ENVIADA.format(limites=" y ".join(LIMITE_NO_ENVIO[p] for p in partes))
        )
    for efectos, tipo in ((f.prohibido, "dispara"), (f.quizas, "desconocido")):
        for efecto, prohiben in efectos:
            if efecto in EFECTOS:
                # el que ya bloqueo la colocacion no se repite (respuesta a la PARADA final, 3)
                causas += [
                    FRASE_PROHIBE[tipo].format(motivo=_motivo(g, contadas, lectura))
                    for g in prohiben
                    if g not in bloquean
                ]
    if not causas and not hay:
        if zona is None or any(r in f.disparadas for r in REGLAS_QUE_COLOCAN):
            raise LaminaError("sin orden y sin ninguna causa de la lista cerrada")
        causas.append(FRASE_NO_TOCABA)
    return causas


# ------------------------------------------------------------------------- fechas, ids y dinero

# Sin fechas (punto 5): AAAA-MM-DD, DD/MM, DD-MM y los meses CON limite de palabra («3 de mayo»
# casa y «otro rango mayor» no), en castellano y en ingles.
RE_FECHA = re.compile(
    r"\d{4}-\d{1,2}-\d{1,2}|\b\d{1,2}/\d{1,2}\b|\b\d{1,2}-\d{1,2}\b|"
    r"\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|"
    r"noviembre|diciembre|january|february|march|april|may|june|july|august|september|october|"
    r"november|december)\b",
    re.IGNORECASE,
)
# Ni ids (RN-, A- con cifras, ADR-, S- con cifras, zona:, o con cifras, pos-, ev-, fb-), ni lote,
# ni R, ni dinero, ni porcentajes (punto 4)
RE_PROHIBIDO = re.compile(
    r"\bRN-|\bA-\d|\bADR-|\bS-\d|zona:|\bo\d+\b|\bpos-|\bev-|\bfb-|\blote|(?-i:\bR\b)|%|\bUSD\b|"
    r"\bEUR\b|\$|€|\bdinero\b|\bganancia\b|\bp[eé]rdida de \d",
    re.IGNORECASE,
)
RE_MARCADO = re.compile(r"<!--|<title|<metadata|<script|javascript:|\son[a-z]+\s*=", re.IGNORECASE)


def comprobar_texto(nombre: str, texto: str) -> None:
    """La ultima puerta de cada fichero que se ensena: sin fechas, sin ids ni dinero, sin
    comentarios, metadatos ni JavaScript."""
    for patron, que in (
        (RE_FECHA, "una fecha"),
        (RE_PROHIBIDO, "un id, el lote, R o dinero"),
        (RE_MARCADO, "un comentario, metadatos o JavaScript"),
    ):
        if patron.search(nombre) or patron.search(texto):
            raise LaminaError(f"{nombre} llevaria {que}")


# ---------------------------------------------------------------------------------- la eleccion


def corte_b(op: Operacion) -> int:
    """El cierre `t` mas tardio con `t * 60 000 < entrada en ms`: la ultima M1 cerrada
    ESTRICTAMENTE antes de la entrada (respuesta del consultor a la fase 0, punto 8)."""
    ms = (op.instante - datetime(1970, 1, 1, tzinfo=UTC)) // timedelta(milliseconds=1)
    return (int(ms) - 1) // MS_POR_MINUTO


def elegir(
    rec: Recolector,
    motor: MotorCableado,
    pedidas: Sequence[Pedida],
    ops_bot: Sequence[Operacion],
    ops_trader: Sequence[Operacion],
    tol: Tolerancias,
) -> dict[Pedida, tuple[Lamina, ...]]:
    """Las laminas de cada sesion pedida, en orden de hora: (a) las ordenes del bot llenadas en la
    sesion; (b) las operaciones del trader de la sesion sin pareja, con las parejas de
    `decisiones.resumir` sobre la corrida entera (ADR-0043)."""
    from botsito.engine.broker import minuto_de_apertura
    from botsito.engine.decisiones import clave_op, resumir

    resumen = resumir("laminas", motor, ops_bot, ops_trader, tol)
    con_pareja = {t for t, _ in resumen.parejas}
    salida: dict[Pedida, tuple[Lamina, ...]] = {}
    for p in pedidas:
        limites = rec.dias[p.dia]
        laminas: list[tuple[int, str, str, Lamina]] = []
        broker = motor.brokers.get(p.dia)
        if broker is None:
            raise LaminaError(f"sesion {p.n}: el dia no se corrio")
        for pos in broker.posiciones.values():
            minuto = minuto_de_apertura(pos)
            sesion = next((n for n, d, h in limites if d <= minuto < h), None)
            if sesion != p.sesion:
                continue
            foto = rec.fotos_a.get((p.dia, pos.orden_id))
            if foto is None:
                raise LaminaError(f"sesion {p.n}: una orden llenada sin foto de su colocacion")
            o = foto.orden(pos.orden_id)
            if o is None or o.precio != int(broker.ordenes[pos.orden_id].precio):
                raise LaminaError(f"sesion {p.n}: la foto no es la del precio al que se lleno")
            laminas.append(
                (foto.corte, TIPO_A, pos.orden_id, Lamina(p, TIPO_A, foto, pos.orden_id))
            )
        for op in ops_trader:
            if op.dia != p.dia or op.sesion != p.sesion or clave_op(op) in con_pareja:
                continue
            t = corte_b(op)
            foto = rec.fotos_b.get((p.dia, t))
            if foto is None:
                raise LaminaError(f"sesion {p.n}: un corte de tipo b sin cierre observado")
            laminas.append((t, TIPO_B, "", Lamina(p, TIPO_B, foto)))
        salida[p] = tuple(x[-1] for x in sorted(laminas, key=lambda x: x[:3]))
    return salida


# ----------------------------------------------------------------------------- la corrida entera


def generar(
    plantilla: MotorCableado,
    reglas: Sequence[Any],
    correr: Callable[[MotorCableado], Sequence[Operacion]],
    pedidas: Sequence[Pedida],
    limites: Mapping[str, tuple[tuple[str, int, int], ...]],
    ops_trader: Sequence[Operacion],
    tol: Tolerancias,
    puerta: Puerta,
    lectura: Lectura,
    avisar: Callable[[str], None] = lambda _t: None,
) -> tuple[dict[str, str], list[str]]:
    """La base con el recolector y la base otra vez sin el (tienen que dar lo mismo, respuesta del
    consultor a la fase 0, punto 10); despues, las laminas. Devuelve los ficheros (ruta relativa ->
    texto) y el resumen por sesion para la consola. Todo en memoria: si algo falla, `LaminaError`
    y no se ha escrito nada."""
    from botsito.engine.decisiones import motor_nuevo, resumir, sin_delta
    from botsito.engine.laminas_svg import indice, pagina

    cortes: dict[str, set[int]] = {}
    for op in ops_trader:
        if any(op.dia == p.dia and op.sesion == p.sesion for p in pedidas):
            cortes.setdefault(op.dia, set()).add(corte_b(op))
    rec = Recolector(
        {p.dia: limites[p.dia] for p in pedidas},
        {d: frozenset(c) for d, c in cortes.items()},
        puerta,
    )
    motor = motor_nuevo(plantilla, reglas, rec)
    ops = list(correr(motor))
    base = resumir("base", motor, ops, ops_trader, tol)
    avisar(f"base con el recolector: {base.recuentos()}")
    # se eligen antes de la segunda corrida para soltar el primer motor (las fotos son copias)
    elegidas = elegir(rec, motor, pedidas, ops, ops_trader, tol)
    del motor, rec
    otra = motor_nuevo(plantilla, reglas)
    repetida = resumir("base", otra, list(correr(otra)), ops_trader, tol)
    avisar(f"base sin el recolector: {repetida.recuentos()}")
    del otra
    if not sin_delta(base, repetida):
        raise LaminaError(
            f"la base con el recolector {base.recuentos()} y sin el {repetida.recuentos()} no "
            "cuadran: no se escribe nada"
        )
    ficheros: dict[str, str] = {}
    clave = ["# Que es cada lamina. NO SE ENSENA: lo guarda Aleks.", ""]
    resumen: list[str] = []
    for p in pedidas:
        carpeta = f"sesion-{p.n:02d}"
        desde, hasta = next((a, b) for n, a, b in limites[p.dia] if n == p.sesion)
        cabecera = f"La sesión de las {hora(desde, puerta.huso)} a las {hora(hasta, puerta.huso)}"
        entradas = []
        dentro = fuera = 0
        for k, lam in enumerate(elegidas[p], 1):
            comp = componer(lam, lectura)
            nombre = f"lamina-{k:02d}.html"
            texto = pagina(comp, k, cabecera)
            comprobar_texto(nombre, texto)
            ficheros[f"{carpeta}/{nombre}"] = texto
            entradas.append((nombre, k, hora(lam.foto.corte, puerta.huso)))
            dentro += comp.fija_dentro is True
            fuera += comp.fija_dentro is False
            que = (
                "orden del bot llenada" if lam.tipo == TIPO_A else "operacion del trader sin pareja"
            )
            fija = {True: "dentro", False: "FUERA", None: "sin sesgo con lado"}[comp.fija_dentro]
            clave.append(
                f"{carpeta}/{nombre}: {p.dia}, sesion {p.sesion}, corte en el cierre de M1 de las "
                f"{hora(lam.foto.corte, puerta.huso)} ({puerta.huso}), tipo {lam.tipo} ({que}); la "
                f"H4 que fija el sesgo, {fija} de la ventana"
            )
        texto = indice(cabecera, entradas)
        comprobar_texto("indice.html", texto)
        ficheros[f"{carpeta}/indice.html"] = texto
        de_a = sum(1 for lam in elegidas[p] if lam.tipo == TIPO_A)
        resumen.append(
            f"{carpeta}: {len(elegidas[p])} laminas ({de_a} de tipo a y {len(elegidas[p]) - de_a} "
            f"de tipo b); la H4 que fija el sesgo, dentro en {dentro} y fuera en {fuera}"
        )
    ficheros["clave.txt"] = "\n".join(clave) + "\n"
    for nombre in ficheros:
        if nombre != "clave.txt":
            comprobar_texto(nombre, "")
    return ficheros, resumen


def comprobar_salida(salida: Path, repo: Path) -> Path:
    """La raiz de salida, ABSOLUTA, fuera del repositorio y vacia o inexistente (no pisa nada).
    Lo contrario de `decisiones.comprobar_carpeta`, que exige data/ (encargo, punto 7)."""
    destino = (salida if salida.is_absolute() else Path.cwd() / salida).resolve()
    raiz = repo.resolve()
    if destino == raiz or raiz in destino.parents:
        raise LaminaError(f"--salida {salida} esta dentro del repositorio: las laminas van fuera")
    if destino.exists() and (not destino.is_dir() or any(destino.iterdir())):
        raise LaminaError(f"--salida {salida} ya existe y no esta vacia: no se pisa")
    return destino


def escribir(ficheros: Mapping[str, str], destino: Path) -> list[Path]:
    escritos = []
    for nombre, texto in sorted(ficheros.items()):
        ruta = destino / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8", newline="\n")
        escritos.append(ruta)
    return escritos


def pedidas_de(texto: str) -> tuple[Pedida, ...]:
    """`dia:sesion,dia:sesion,...` en el orden dado; repetidas o mal formadas, `LaminaError`."""
    salida: list[Pedida] = []
    for k, parte in enumerate((x.strip() for x in texto.split(",") if x.strip()), 1):
        dia, _, sesion = parte.partition(":")
        try:
            date.fromisoformat(dia)
        except ValueError as exc:
            raise LaminaError(f"--sesiones: {parte!r} no es dia:sesion") from exc
        if not sesion:
            raise LaminaError(f"--sesiones: {parte!r} no es dia:sesion")
        salida.append(Pedida(k, dia, sesion))
    if not salida:
        raise LaminaError("--sesiones vacia")
    if len({(p.dia, p.sesion) for p in salida}) != len(salida):
        raise LaminaError("--sesiones lleva una sesion repetida")
    return tuple(salida)


def comprobar_pedidas(
    pedidas: Sequence[Pedida],
    dias_dev: Iterable[str],
    puerta: Puerta,
    limites: Mapping[str, tuple[tuple[str, int, int], ...]],
    horas_perdidas: Mapping[str, Sequence[str]],
) -> None:
    """Antes de correr nada: cada dia pedido es dev de construccion y no esta oculto, la sesion
    existe y no tiene ninguna hora perdida dentro (punto 6)."""
    dev = set(dias_dev)
    for p in pedidas:
        if p.dia not in dev or not puerta.dia_permitido(date.fromisoformat(p.dia)):
            raise LaminaError(f"sesion {p.n}: el dia no es dev de construccion o esta oculto")
        sesion = next(((a, b) for n, a, b in limites.get(p.dia, ()) if n == p.sesion), None)
        if sesion is None:
            raise LaminaError(f"sesion {p.n}: {p.sesion!r} no es una sesion de ese dia")
        for h in horas_perdidas.get(p.dia, ()):
            inicio = int(datetime.strptime(h, "%Y-%m-%dT%HZ").replace(tzinfo=UTC).timestamp()) // 60
            if inicio < sesion[1] and inicio + 60 > sesion[0]:
                raise LaminaError(f"sesion {p.n}: tiene una hora perdida dentro (sin ticks)")


__all__ = [
    "Dibujo",
    "Foto",
    "Lamina",
    "LaminaError",
    "Lectura",
    "Pedida",
    "Puerta",
    "Recolector",
    "comprobar_pedidas",
    "comprobar_salida",
    "comprobar_texto",
    "componer",
    "corte_b",
    "elegir",
    "escribir",
    "generar",
    "pedidas_de",
    "puerta_de",
]
