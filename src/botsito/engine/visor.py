"""El visor de dias de construccion: una pagina por dia para depurar reglas del motor.

Para un dia `dev` de un mes de CONSTRUCCION, muestra de un vistazo que hizo el trader, que hizo el
bot y por que: las M1 de la ventana del dia (y las M15, conmutables), las H4 de contexto -la
previa y las que miro el sesgo-, las operaciones del trader con entrada y stop en su instante de
llenado, las del bot si el arnes las produjo, y por sesion el sesgo, los hechos fijados en su
instante, donde se paro el embudo (primitiva NO_IMPLEMENTADA o gate que prohibio), los avisos de
H3 y las parejas del criterio de fidelidad (ADR-0043).

**SOLO CONSTRUCCION, y POR LA COMPUERTA**, con el mismo mecanismo y los mismos mensajes que el
arnes: los dias salen de `arnes.dias_de_construccion`, que valida el mes contra
`criterio_fidelidad.yaml` y cruza cada caso con `casos_ocultos` ANTES de leerlo. Un dia oculto
detiene todo con `HoldoutCerradoError` y no se lee.

**EL RENDER ES PURO Y DETERMINISTA**: `render_dia` recibe un `DiaVisor` ya preparado y devuelve el
HTML; sin tiempos, sin azar, todo ordenado. Dos ejecuciones dan los mismos bytes. HTML
autocontenido con SVG generado aqui, sin ninguna dependencia nueva ni JavaScript.

**SIN MIRAR AL FUTURO**: cada hecho se pinta en el instante en que el motor lo fijo, y `hasta`
recorta la vista a un instante: velas cerradas hasta el, hechos fijados hasta el, operaciones
llenadas hasta el.

La salida no se versiona: va a una carpeta ignorada por git (`data/visor/` por defecto).
"""

from __future__ import annotations

import html
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from botsito.cases.criterio_fidelidad import Criterio, Operacion, Pareja, medir
from botsito.cases.ingesta import DIRECTORIO_DEV
from botsito.cases.paquete import Config
from botsito.cases.ventanas import MINUTOS_H4
from botsito.comun.husos import huso_canonico
from botsito.comun.yaml_estricto import leer_yaml
from botsito.config.registro import Registro
from botsito.data.agregacion import agregar
from botsito.data.dataset import DatasetError, buscar_manifiesto, cargar_manifiesto, cargar_serie
from botsito.data.velas import a_datetime, a_minuto
from botsito.domain.sesgo import ResultadoSesgo, sesgo_h4
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import arnes
from botsito.engine.arnes import ConjuntoError, DiaTrader
from botsito.engine.interprete import VALOR_APAGADO
from botsito.engine.motor import (
    DatosMercado,
    DiaDeMercado,
    Motor,
    ResultadoDia,
    Sesion,
    TrazaSesion,
)
from botsito.engine.primitivas import ANOTACION_SESGO

MINUTOS_M15 = 15
CARPETA_SALIDA = Path("data") / "visor"  # ignorada por git (`/data/*`)
INDICE = "index.html"
TRADER = "trader"
BOT = "bot"
# Geometria de los graficos, en pixeles. No es negocio: es la pagina.
ANCHO = 1180
ALTO_PRECIO = 420
ALTO_HECHOS = 26  # por hecho de regla
MARGEN_IZQ = 70
MARGEN_DER = 16
MARGEN_SUP = 12
ALTO_EJE = 22
ALTO_H4 = 220
H4_DE_CONTEXTO_MIN = 8  # al menos estas H4 en el grafico de contexto, ademas de las del sesgo


# ------------------------------------------------------------------------------------ datos


@dataclass(frozen=True)
class OperacionVisor:
    origen: str  # TRADER o BOT
    sesion: str
    direccion: str
    instante: datetime  # llenado, con huso
    entrada: Decimal
    stop: Decimal | None = None  # el caso del trader lo trae; el bot, hoy, no

    def como_criterio(self, dia: str) -> Operacion:
        return Operacion(dia, self.sesion, self.direccion, self.instante, self.entrada)


@dataclass(frozen=True)
class SesgoSesion:
    """Lo que dijo `domain/sesgo.py` al abrir la sesion, recalculado para poder senalar la H4."""

    sesion: str
    apertura: MinutoUtc
    resultado: ResultadoSesgo
    decide: Vela | None  # la H4 cuya ruptura fijo el sesgo; None si INSUFICIENTE
    anterior: Vela | None  # la H4 contra la que rompio


@dataclass(frozen=True)
class DiaVisor:
    """Todo lo que la pagina de un dia necesita, ya leido: el render no toca ficheros."""

    caso: str
    dia: date
    huso: str
    sesiones: tuple[Sesion, ...]
    ventana: tuple[str, str]  # HH:MM locales, [desde, hasta]
    escala: int
    m1: tuple[Vela, ...]
    m15: tuple[Vela, ...]
    h4: tuple[Vela, ...]  # las de contexto, cerradas, en orden
    trader: tuple[OperacionVisor, ...]
    bot: tuple[OperacionVisor, ...]
    resultado: ResultadoDia
    parejas: tuple[Pareja, ...]
    hechos: tuple[tuple[str, tuple[str, ...]], ...]  # de origen regla, en el orden de la spec
    sesgos: tuple[SesgoSesion, ...]
    objetivo_rr: Decimal | None  # el objetivo DERIVADO por regla; el caso no trae objetivo
    motor: str

    @property
    def ventana_utc(self) -> tuple[MinutoUtc, MinutoUtc]:
        return _minuto_local(self.dia, self.ventana[0], self.huso), _minuto_local(
            self.dia, self.ventana[1], self.huso
        )


def _minuto_local(dia: date, hhmm: str, huso: str) -> MinutoUtc:
    hh, mm = (int(x) for x in hhmm.split(":"))
    return a_minuto(datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=huso_canonico(huso)))


# --------------------------------------------------------------------------------- compuerta


def caso_de_construccion(
    repo: Path,
    criterio: Criterio,
    caso: str,
    *,
    ocultos: Iterable[str] | None = None,
    asignaciones: Mapping[str, Mapping[str, str]] | None = None,
) -> DiaTrader:
    """UN dia `dev` de construccion, por la compuerta del arnes y con sus mismos mensajes.

    El mes sale del id; `arnes.dias_de_construccion` lo valida contra el criterio y cruza TODOS los
    casos del reparto con los ocultos antes de leer ninguno, asi que un caso oculto -este o
    cualquiera del mes- detiene con `HoldoutCerradoError` sin abrir nada.
    """
    m = arnes._DIA.search(caso)
    if m is None:
        raise ConjuntoError(f"{caso}: el id no acaba en AAAA-MM-DD")
    mes = m.group(1)[:7]
    dias = arnes.dias_de_construccion(
        repo,
        criterio,
        [mes],
        ocultos=None if ocultos is None else set(ocultos),
        asignaciones=asignaciones,
    )
    for d in dias:
        if d.id == caso:
            return d
    raise ConjuntoError(
        f"{caso} no es un dia dev de construccion de {mes}: el visor solo pinta esos "
        f"({len(dias)} en el reparto)"
    )


def _stops(repo: Path, dt: DiaTrader) -> list[Decimal | None]:
    """El stop de cada operacion del caso, en el orden del fichero (el arnes no lo carga)."""
    ruta = repo / DIRECTORIO_DEV / f"{dt.id}.yaml"
    if not ruta.exists():
        return [None] * len(dt.operaciones)
    doc = leer_yaml(ruta)
    stops: list[Decimal | None] = []
    for op in doc.get("operaciones") or []:
        stop = op.get("stop")
        stops.append(Decimal(str(stop)) if stop is not None else None)
    if len(stops) != len(dt.operaciones):
        stops = [None] * len(dt.operaciones)
    return stops


# ------------------------------------------------------------------------------- preparador


@dataclass
class Preparador:
    """Prepara `DiaVisor` con el motor real: carga las velas de cada mes una sola vez."""

    repo: Path
    carpeta_datos: Path
    criterio: Criterio
    registro: Registro
    config: Config
    vocabulario: Mapping[str, Mapping[str, Any]]
    motor: Motor
    nombre_motor: str = "spec vigente"
    _m1_por_mes: dict[str, tuple[tuple[Vela, ...], int]] = field(default_factory=dict)

    @property
    def huso(self) -> str:
        return self.registro.texto("huso_operativa")

    def dias(self, meses: Sequence[str]) -> tuple[DiaTrader, ...]:
        return arnes.dias_de_construccion(self.repo, self.criterio, meses)

    def caso(self, caso: str) -> DiaTrader:
        return caso_de_construccion(self.repo, self.criterio, caso)

    def _m1(self, mes: str) -> tuple[tuple[Vela, ...], int]:
        """Las M1 del mes y del anterior (el calentamiento del sesgo, como el arnes), y la
        escala."""
        if mes not in self._m1_por_mes:
            velas: list[Vela] = []
            escala: int | None = None
            for m in (arnes._mes_anterior(mes), mes):
                try:
                    ruta = buscar_manifiesto(self.repo, f"{self.config.dataset_prefijo}{m}")
                except DatasetError:
                    continue
                serie = cargar_serie(cargar_manifiesto(ruta), self.carpeta_datos)
                if escala is not None and serie.escala != escala:
                    raise ConjuntoError(f"{m}: escala {serie.escala} distinta de {escala}")
                escala = serie.escala
                velas += list(serie.velas)
            if escala is None:
                raise ConjuntoError(f"{mes}: no hay dataset {self.config.dataset_prefijo}{mes}")
            self._m1_por_mes[mes] = (tuple(velas), escala)
        return self._m1_por_mes[mes]

    def preparar(self, dt: DiaTrader) -> DiaVisor:
        dia = date.fromisoformat(dt.dia)
        m1_mes, escala = self._m1(dt.dia[:7])
        anclaje = self.registro.hora("anclaje_h4")
        h4_todas = agregar(list(m1_mes), MINUTOS_H4, anclaje)
        sesiones = tuple(Sesion(s.nombre, s.desde, s.hasta) for s in self.config.sesiones)
        mercado = DiaDeMercado(dia, self.huso, sesiones, DatosMercado(h4_todas))
        resultado = self.motor.correr_dia(mercado)

        desde, hasta = (
            _minuto_local(dia, self.config.ventana_local[0], self.huso),
            _minuto_local(dia, self.config.ventana_local[1], self.huso),
        )
        m1 = tuple(v for v in m1_mes if desde <= v.inicio < hasta)
        m15 = tuple(agregar(list(m1), MINUTOS_M15, anclaje)) if m1 else ()

        tope = self.registro.entero("sesgo_h4_tope_velas")
        criterio_ruptura = self.registro.opcion("sesgo_h4_criterio_ruptura")
        sesgos = tuple(
            _sesgo_de_sesion(h4_todas, s, dia, self.huso, tope, criterio_ruptura) for s in sesiones
        )
        h4 = _h4_de_contexto(h4_todas, sesgos, hasta)

        stops = _stops(self.repo, dt)
        trader = tuple(
            OperacionVisor(TRADER, op.sesion, op.direccion, op.instante, op.entrada, stop)
            for op, stop in zip(dt.operaciones, stops, strict=True)
        )
        bot = tuple(
            OperacionVisor(BOT, op.sesion, op.direccion, op.instante, op.entrada)
            for op in resultado.operaciones
        )
        parejas = medir(
            [o.como_criterio(dt.dia) for o in trader],
            [o.como_criterio(dt.dia) for o in bot],
            self.criterio.tolerancias,
        ).parejas
        return DiaVisor(
            caso=dt.id,
            dia=dia,
            huso=self.huso,
            sesiones=sesiones,
            ventana=self.config.ventana_local,
            escala=escala,
            m1=m1,
            m15=m15,
            h4=h4,
            trader=trader,
            bot=bot,
            resultado=resultado,
            parejas=parejas,
            hechos=tuple((h, tuple(p)) for h, p in arnes.hechos_de_regla(self.vocabulario)),
            sesgos=sesgos,
            objetivo_rr=self.registro.decimal("objetivo_rr"),
            motor=self.nombre_motor,
        )


def _sesgo_de_sesion(
    h4: Sequence[Vela], sesion: Sesion, dia: date, huso: str, tope: int, criterio: str
) -> SesgoSesion:
    apertura = _minuto_local(dia, sesion.desde, huso)
    cerradas = sorted((v for v in h4 if v.fin <= apertura), key=lambda v: v.inicio)
    r = sesgo_h4(cerradas, apertura, tope, criterio)
    decide = anterior = None
    if r.ruptura_puntos is not None and r.velas_miradas <= len(cerradas) - 1:
        i = len(cerradas) - r.velas_miradas
        decide, anterior = cerradas[i], cerradas[i - 1]
    return SesgoSesion(sesion.nombre, apertura, r, decide, anterior)


def _h4_de_contexto(
    h4: Sequence[Vela], sesgos: Sequence[SesgoSesion], hasta: MinutoUtc
) -> tuple[Vela, ...]:
    """Las H4 cerradas antes del fin de la ventana: desde la que rompio el sesgo mas antiguo (y su
    anterior), y al menos las ultimas H4_DE_CONTEXTO_MIN."""
    cerradas = sorted((v for v in h4 if v.fin <= hasta), key=lambda v: v.inicio)
    desde = len(cerradas) - H4_DE_CONTEXTO_MIN
    for s in sesgos:
        if s.anterior is not None:
            indice = next(
                (i for i, v in enumerate(cerradas) if v.inicio == s.anterior.inicio), None
            )
            if indice is not None:
                desde = min(desde, indice)
    return tuple(cerradas[max(desde, 0) :])


# ----------------------------------------------------------------------------------- embudo


def embudo_de_sesion(
    traza: TrazaSesion, hechos: Sequence[tuple[str, Sequence[str]]], hasta: MinutoUtc | None = None
) -> list[tuple[str, str]]:
    """Por hecho de regla, en el orden de la spec: `si`, o `no[primitivas]`, o `no[productoras sin
    cumplirse]`, con la misma lectura que el informe del arnes."""
    producidos = {h for t, _, h, v in traza.fijados if v != VALOR_APAGADO and _visible(t, hasta)}
    salida: list[tuple[str, str]] = []
    for hecho, productoras in hechos:
        if hecho in producidos:
            salida.append((hecho, "si"))
            continue
        prim = sorted({p for r, p in traza.no_implementadas if r in productoras})
        salida.append((hecho, f"no[{', '.join(prim) if prim else 'productoras sin cumplirse'}]"))
    return salida


def donde_se_para(traza: TrazaSesion, hechos: Sequence[tuple[str, Sequence[str]]]) -> str:
    """El primer hecho que falta y en que se paro, mas los gates que prohibieron algo."""
    partes = [f"{h}:{e}" for h, e in embudo_de_sesion(traza, hechos) if e != "si"][:1]
    prohibidas = sorted({m for _, _, m in traza.bloqueadas})
    if prohibidas:
        partes.append("bloqueado por " + ", ".join(prohibidas))
    return "; ".join(partes) or "produce todos los hechos"


def _visible(instante: int, hasta: MinutoUtc | None) -> bool:
    return hasta is None or instante <= hasta


# --------------------------------------------------------------------------------- geometria


@dataclass(frozen=True)
class Lienzo:
    """La transformacion de (minuto UTC, puntos) a pixeles. Publica para que los tests comprueben
    que cada marca cae donde debe."""

    desde: MinutoUtc
    hasta: MinutoUtc
    minimo: int
    maximo: int
    ancho: int = ANCHO
    alto: int = ALTO_PRECIO

    def x(self, minuto: int) -> float:
        rango = max(self.hasta - self.desde, 1)
        return MARGEN_IZQ + (minuto - self.desde) * (self.ancho - MARGEN_IZQ - MARGEN_DER) / rango

    def y(self, puntos: float | Decimal) -> float:
        rango = max(self.maximo - self.minimo, 1)
        util = self.alto - MARGEN_SUP - ALTO_EJE
        return MARGEN_SUP + (self.maximo - float(puntos)) * util / rango


def _px(valor: float) -> str:
    return f"{valor:.1f}"


def _puntos(precio: Decimal, escala: int) -> int:
    return int((precio * escala).to_integral_value())


def _precio(puntos: int | float, escala: int) -> str:
    decimales = len(str(escala)) - 1
    return f"{puntos / escala:.{decimales}f}"


def _hora(minuto: int, huso: ZoneInfo) -> str:
    return a_datetime(minuto).astimezone(huso).strftime("%H:%M")


def _hora_exacta(instante: datetime, huso: ZoneInfo) -> str:
    return instante.astimezone(huso).strftime("%H:%M:%S")


def _minuto_de(instante: datetime) -> int:
    return a_minuto(instante.replace(second=0, microsecond=0))


# ---------------------------------------------------------------------------------- svg


def _velas_svg(velas: Iterable[Vela], lienzo: Lienzo, clase: str, minimo_ancho: float) -> str:
    partes: list[str] = []
    for v in velas:
        x0, x1 = lienzo.x(v.inicio), lienzo.x(v.fin)
        ancho = max(x1 - x0 - 1.0, minimo_ancho)
        xm = (x0 + x1) / 2
        sube = v.cierre >= v.abierta
        ya, yb = lienzo.y(max(v.abierta, v.cierre)), lienzo.y(min(v.abierta, v.cierre))
        partes.append(
            f'<line class="mecha" x1="{_px(xm)}" y1="{_px(lienzo.y(v.maxima))}" '
            f'x2="{_px(xm)}" y2="{_px(lienzo.y(v.minima))}"/>'
            f'<rect class="{"sube" if sube else "baja"}" x="{_px(xm - ancho / 2)}" y="{_px(ya)}" '
            f'width="{_px(ancho)}" height="{_px(max(yb - ya, 1.0))}"/>'
        )
    return f'<g class="{clase}">{"".join(partes)}</g>'


def _eje_tiempo(lienzo: Lienzo, huso: ZoneInfo, paso_min: int) -> str:
    partes: list[str] = []
    primero = lienzo.desde - (lienzo.desde % paso_min)
    y = lienzo.alto - ALTO_EJE
    for m in range(primero, lienzo.hasta + 1, paso_min):
        if m < lienzo.desde:
            continue
        x = lienzo.x(m)
        partes.append(
            f'<line class="rejilla" x1="{_px(x)}" y1="{MARGEN_SUP}" x2="{_px(x)}" y2="{y}"/>'
            f'<text class="eje" x="{_px(x)}" y="{y + 16}" text-anchor="middle">'
            f"{_hora(m, huso)}</text>"
        )
    return "".join(partes)


def _eje_precio(lienzo: Lienzo, escala: int, divisiones: int = 6) -> str:
    partes: list[str] = []
    rango = lienzo.maximo - lienzo.minimo
    for i in range(divisiones + 1):
        p = lienzo.minimo + rango * i / divisiones
        y = lienzo.y(p)
        partes.append(
            f'<line class="rejilla" x1="{MARGEN_IZQ}" y1="{_px(y)}" '
            f'x2="{lienzo.ancho - MARGEN_DER}" y2="{_px(y)}"/>'
            f'<text class="eje" x="{MARGEN_IZQ - 6}" y="{_px(y + 4)}" text-anchor="end">'
            f"{_precio(p, escala)}</text>"
        )
    return "".join(partes)


def _sesiones_svg(d: DiaVisor, lienzo: Lienzo, huso: ZoneInfo) -> str:
    partes: list[str] = []
    for s in d.sesiones:
        a, b = _minuto_local(d.dia, s.desde, d.huso), _minuto_local(d.dia, s.hasta, d.huso)
        x0, x1 = lienzo.x(max(a, lienzo.desde)), lienzo.x(min(b, lienzo.hasta))
        partes.append(
            f'<rect class="sesion" x="{_px(x0)}" y="{MARGEN_SUP}" width="{_px(max(x1 - x0, 0))}" '
            f'height="{lienzo.alto - MARGEN_SUP - ALTO_EJE}"/>'
            f'<text class="etiqueta" x="{_px(x0 + 4)}" y="{MARGEN_SUP + 12}">'
            f"{html.escape(s.nombre)} ({_hora(a, huso)}-{_hora(b, huso)})</text>"
        )
    return "".join(partes)


def _operacion_svg(
    op: OperacionVisor, d: DiaVisor, lienzo: Lienzo, huso: ZoneInfo, indice: int
) -> str:
    x = lienzo.x(_minuto_de(op.instante))
    y = lienzo.y(_puntos(op.entrada, d.escala))
    fin = lienzo.x(lienzo.hasta)
    etiqueta = (
        f"{op.origen} {indice}: {op.direccion} {op.entrada} @ {_hora_exacta(op.instante, huso)}"
    )
    partes = [
        f'<g class="op {op.origen}"><title>{html.escape(etiqueta)}</title>'
        f'<line class="entrada" x1="{_px(x)}" y1="{_px(y)}" x2="{_px(fin)}" y2="{_px(y)}"/>'
        f'<circle class="llenado" cx="{_px(x)}" cy="{_px(y)}" r="5"/>'
        f'<text class="etiqueta" x="{_px(x - 7 if x > fin - 90 else x + 7)}" y="{_px(y - 6)}"'
        f' text-anchor="{"end" if x > fin - 90 else "start"}">'
        f"{html.escape(op.origen[0].upper())}{indice} {html.escape(op.direccion)}</text>"
    ]
    if op.stop is not None:
        ys = lienzo.y(_puntos(op.stop, d.escala))
        partes.append(
            f'<line class="stop" x1="{_px(x)}" y1="{_px(ys)}" x2="{_px(fin)}" y2="{_px(ys)}"/>'
        )
        if d.objetivo_rr is not None:
            distancia = abs(op.entrada - op.stop) * d.objetivo_rr
            objetivo = (
                op.entrada + distancia if op.direccion == "compra" else op.entrada - distancia
            )
            yo = lienzo.y(_puntos(objetivo, d.escala))
            partes.append(
                f'<line class="objetivo" x1="{_px(x)}" y1="{_px(yo)}" x2="{_px(fin)}" '
                f'y2="{_px(yo)}"><title>objetivo DERIVADO por regla (objetivo_rr), no del caso'
                "</title></line>"
            )
    partes.append("</g>")
    return "".join(partes)


def _parejas_svg(d: DiaVisor, lienzo: Lienzo) -> str:
    partes: list[str] = []
    for p in d.parejas:
        x0, y0 = (
            lienzo.x(_minuto_de(p.trader.instante)),
            lienzo.y(_puntos(p.trader.entrada, d.escala)),
        )
        x1, y1 = lienzo.x(_minuto_de(p.bot.instante)), lienzo.y(_puntos(p.bot.entrada, d.escala))
        partes.append(
            f'<line class="pareja" x1="{_px(x0)}" y1="{_px(y0)}" x2="{_px(x1)}" y2="{_px(y1)}">'
            f"<title>pareja: Δ {p.delta_segundos} s, {p.delta_puntos} puntos</title></line>"
        )
    return "".join(partes)


def _hechos_svg(d: DiaVisor, lienzo: Lienzo, huso: ZoneInfo, hasta: MinutoUtc | None) -> str:
    """Una calle por hecho de regla; una marca en el instante EXACTO en que se fijo."""
    nombres = [h for h, _ in d.hechos]
    alto = MARGEN_SUP + ALTO_HECHOS * len(nombres) + ALTO_EJE
    partes = [f'<svg class="hechos" viewBox="0 0 {lienzo.ancho} {alto}" width="{lienzo.ancho}">']
    for i, nombre in enumerate(nombres):
        y = MARGEN_SUP + ALTO_HECHOS * i + ALTO_HECHOS / 2
        partes.append(
            f'<line class="rejilla" x1="{MARGEN_IZQ}" y1="{_px(y)}" '
            f'x2="{lienzo.ancho - MARGEN_DER}" y2="{_px(y)}"/>'
            f'<text class="eje" x="{MARGEN_IZQ + 2}" y="{_px(y - 4)}">'
            f"{html.escape(nombre)}</text>"
        )
    for sesion, traza in sorted(d.resultado.sesiones.items()):
        for instante, regla, hecho, valor in sorted(traza.fijados):
            if hecho not in nombres or not _visible(instante, hasta):
                continue
            y = MARGEN_SUP + ALTO_HECHOS * nombres.index(hecho) + ALTO_HECHOS / 2
            x = lienzo.x(instante)
            clase = "apagado" if valor == VALOR_APAGADO else "fijado"
            titulo = html.escape(f"{sesion} {_hora(instante, huso)} {regla}: {hecho}={valor}")
            partes.append(
                f'<g class="hecho {clase}" data-instante="{instante}"><title>{titulo}</title>'
                f'<circle cx="{_px(x)}" cy="{_px(y)}" r="5"/>'
                f'<text class="valor" x="{_px(x + 7)}" y="{_px(y + 4)}">{html.escape(valor)}'
                "</text></g>"
            )
    partes.append("</svg>")
    return "".join(partes)


def _h4_svg(d: DiaVisor, huso: ZoneInfo) -> str:
    if not d.h4:
        return "<p>Sin H4 de contexto.</p>"
    lienzo = Lienzo(
        d.h4[0].inicio,
        d.h4[-1].fin,
        min(v.minima for v in d.h4),
        max(v.maxima for v in d.h4),
        alto=ALTO_H4,
    )
    marcas: list[str] = []
    for s in d.sesgos:
        if s.decide is not None:
            x0, x1 = lienzo.x(s.decide.inicio), lienzo.x(s.decide.fin)
            marcas.append(
                f'<rect class="decide" x="{_px(x0)}" y="{MARGEN_SUP}" width="{_px(x1 - x0)}" '
                f'height="{ALTO_H4 - MARGEN_SUP - ALTO_EJE}"><title>'
                f"{html.escape(f'{s.sesion}: {s.resultado.sesgo.value}, rompe esta H4')}"
                "</title></rect>"
            )
        xa = lienzo.x(min(max(s.apertura, lienzo.desde), lienzo.hasta))
        marcas.append(
            f'<line class="apertura" x1="{_px(xa)}" y1="{MARGEN_SUP}" x2="{_px(xa)}" '
            f'y2="{ALTO_H4 - ALTO_EJE}"/>'
            f'<text class="etiqueta" x="{_px(xa + 3)}" y="{MARGEN_SUP + 12}">'
            f"{html.escape(s.sesion)}: {html.escape(s.resultado.sesgo.value)}</text>"
        )
    return (
        f'<svg class="h4" viewBox="0 0 {ANCHO} {ALTO_H4}" width="{ANCHO}">'
        f"{_eje_precio(lienzo, d.escala, 4)}{_eje_tiempo(lienzo, huso, MINUTOS_H4 * 2)}"
        f"{_velas_svg(d.h4, lienzo, 'h4', 6.0)}{''.join(marcas)}</svg>"
    )


# --------------------------------------------------------------------------------- pagina


_CSS = (
    "body{font-family:system-ui,sans-serif;margin:16px;color:#222;background:#fff}"
    "h1{font-size:20px;margin:0 0 4px}h2{font-size:16px;margin:18px 0 6px}"
    "h3{font-size:14px;margin:12px 0 4px}p,li,td,th{font-size:13px}"
    "table{border-collapse:collapse}"
    "td,th{border:1px solid #ddd;padding:2px 6px;text-align:left;vertical-align:top}"
    "svg{display:block;max-width:100%;height:auto;background:#fafafa;border:1px solid #ddd}"
    ".rejilla{stroke:#e6e6e6;stroke-width:1}.eje{font-size:10px;fill:#666}"
    ".etiqueta{font-size:10px;fill:#444}.mecha{stroke:#555;stroke-width:1}"
    ".sube{fill:#2e8b57}.baja{fill:#c0392b}.sesion{fill:#3b6fd6;fill-opacity:.06}"
    ".decide{fill:#f39c12;fill-opacity:.25}"
    ".apertura{stroke:#3b6fd6;stroke-width:1;stroke-dasharray:3 3}"
    ".op .entrada{stroke-width:1.5}.op .stop{stroke:#c0392b;stroke-width:1;stroke-dasharray:4 3}"
    ".op .objetivo{stroke:#2e8b57;stroke-width:1;stroke-dasharray:2 4}"
    ".op.trader .entrada,.op.trader .llenado{stroke:#1f4e9c;fill:#1f4e9c}"
    ".op.bot .entrada,.op.bot .llenado{stroke:#8e44ad;fill:#8e44ad}"
    ".pareja{stroke:#f39c12;stroke-width:2}.hecho.fijado circle{fill:#1f4e9c}"
    ".hecho.apagado circle{fill:#999}.valor{font-size:10px;fill:#333}"
    ".m15{display:none}#m15:checked~.grafico .m15{display:inline}"
    "#m15:checked~.grafico .m1{display:none}"
    ".aviso{color:#8a5a00}.leyenda span{display:inline-block;margin-right:14px}"
)


def _fila(*celdas: str) -> str:
    return "<tr>" + "".join(f"<td>{c}</td>" for c in celdas) + "</tr>"


def _tabla(cabecera: Sequence[str], filas: Iterable[str]) -> str:
    cab = "".join(f"<th>{html.escape(c)}</th>" for c in cabecera)
    return f"<table><thead><tr>{cab}</tr></thead><tbody>{''.join(filas)}</tbody></table>"


def _sesion_html(
    d: DiaVisor, s: Sesion, traza: TrazaSesion, huso: ZoneInfo, hasta: MinutoUtc | None
) -> str:
    sesgo = next((x for x in d.sesgos if x.sesion == s.nombre), None)
    anotado = traza.anotaciones.get(ANOTACION_SESGO, arnes.SIN_ANOTACION)
    partes = [
        f"<h3>Sesion {html.escape(s.nombre)} ({html.escape(s.desde)}-{html.escape(s.hasta)})</h3>"
    ]
    detalle = ""
    if sesgo is not None:
        r = sesgo.resultado
        h4 = (
            f", rompe la H4 que abre a las {_hora(sesgo.decide.inicio, huso)} contra la anterior"
            if sesgo.decide is not None
            else ""
        )
        detalle = (
            f" (domain/sesgo.py: {html.escape(r.sesgo.value)}, {r.velas_miradas} H4 miradas"
            f"{', ruptura de ' + str(r.ruptura_puntos) + ' puntos' if r.ruptura_puntos else ''}"
            f"{h4})"
        )
    partes.append(f"<p><b>Sesgo anotado por el motor:</b> {html.escape(anotado)}{detalle}</p>")
    partes.append(
        "<p><b>Embudo:</b> "
        + " · ".join(
            f"{html.escape(h)}:{html.escape(e)}"
            for h, e in embudo_de_sesion(traza, d.hechos, hasta)
        )
        + f"<br><b>Donde se para:</b> {html.escape(donde_se_para(traza, d.hechos))}</p>"
    )
    fijados = [
        _fila(_hora(t, huso), html.escape(r), html.escape(h), html.escape(v))
        for t, r, h, v in sorted(traza.fijados)
        if _visible(t, hasta)
    ]
    partes.append("<p><b>Hechos fijados</b> (en su instante; un valor `no` apaga el hecho):</p>")
    partes.append(
        _tabla(("hora", "regla", "hecho", "valor"), fijados) if fijados else "<p>ninguno</p>"
    )
    listas = (
        ("Primitivas NO_IMPLEMENTADA (regla: primitiva)", sorted(traza.no_implementadas)),
        ("Acciones bloqueadas (regla: accion, motivo)", sorted(traza.bloqueadas)),
    )
    for titulo, elementos in listas:
        cuerpo = ", ".join(html.escape(": ".join(e)) for e in elementos) or "ninguna"
        partes.append(f"<p><b>{titulo}:</b> {cuerpo}</p>")
    partes.append(
        "<p><b>Reglas disparadas:</b> "
        + (html.escape(", ".join(sorted(traza.disparadas))) or "ninguna")
        + "</p>"
    )
    avisos = sorted(traza.empates)
    partes.append(
        '<p class="aviso"><b>Avisos H3 (dos reglas de la misma clase dieron SI a la vez):</b> '
        + (
            "; ".join(html.escape(f"{clase} {', '.join(ids)}") for clase, ids in avisos)
            or "ninguno"
        )
        + "</p>"
    )
    return "".join(partes)


def _operaciones_html(d: DiaVisor, huso: ZoneInfo, ops: Sequence[OperacionVisor]) -> str:
    emparejadas: dict[tuple[str, str, str], str] = {}
    for i, p in enumerate(d.parejas, 1):
        emparejadas[(TRADER, p.trader.sesion, p.trader.instante.isoformat())] = f"pareja {i}"
        emparejadas[(BOT, p.bot.sesion, p.bot.instante.isoformat())] = f"pareja {i}"
    filas = [
        _fila(
            html.escape(op.origen),
            html.escape(op.sesion),
            html.escape(op.direccion),
            _hora_exacta(op.instante, huso),
            html.escape(str(op.entrada)),
            html.escape(str(op.stop)) if op.stop is not None else "-",
            html.escape(emparejadas.get((op.origen, op.sesion, op.instante.isoformat()), "-")),
        )
        for op in ops
    ]
    if not filas:
        return "<p>ninguna</p>"
    return _tabla(
        ("origen", "sesion", "direccion", "llenado", "entrada", "stop", "criterio"), filas
    )


def render_dia(d: DiaVisor, hasta: MinutoUtc | None = None) -> str:
    """La pagina de un dia. Pura y determinista. Con `hasta`, la vista se recorta a ese instante:
    velas cerradas hasta el, hechos fijados hasta el y operaciones llenadas hasta el."""
    huso = huso_canonico(d.huso)
    desde, fin = d.ventana_utc
    m1 = tuple(v for v in d.m1 if _visible(v.fin, hasta))
    m15 = tuple(v for v in d.m15 if _visible(v.fin, hasta))
    trader = tuple(o for o in d.trader if _visible(_minuto_de(o.instante), hasta))
    bot = tuple(o for o in d.bot if _visible(_minuto_de(o.instante), hasta))
    visibles = {(o.origen, o.sesion, o.instante) for o in (*trader, *bot)}
    parejas = tuple(
        p
        for p in d.parejas
        if (TRADER, p.trader.sesion, p.trader.instante) in visibles
        and (BOT, p.bot.sesion, p.bot.instante) in visibles
    )
    recortado = DiaVisor(
        **{**d.__dict__, "m1": m1, "m15": m15, "trader": trader, "bot": bot, "parejas": parejas}
    )

    precios: list[int] = [int(p) for v in m1 for p in (v.minima, v.maxima)]
    for op in (*trader, *bot):
        precios.append(_puntos(op.entrada, d.escala))
        if op.stop is not None:
            precios.append(_puntos(op.stop, d.escala))
    if not precios:
        precios = [0, 1]
    margen = max((max(precios) - min(precios)) // 20, 1)
    lienzo = Lienzo(desde, fin, min(precios) - margen, max(precios) + margen)

    ops_svg = "".join(
        _operacion_svg(op, recortado, lienzo, huso, i)
        for origen in (trader, bot)
        for i, op in enumerate(origen, 1)
    )
    grafico = (
        f'<svg class="precio" viewBox="0 0 {ANCHO} {ALTO_PRECIO}" width="{ANCHO}">'
        f"{_sesiones_svg(d, lienzo, huso)}{_eje_precio(lienzo, d.escala)}"
        f"{_eje_tiempo(lienzo, huso, 60)}{_velas_svg(m1, lienzo, 'm1', 1.0)}"
        f"{_velas_svg(m15, lienzo, 'm15', 4.0)}{ops_svg}{_parejas_svg(recortado, lienzo)}</svg>"
    )
    titulo = f"{d.caso} · {d.dia.isoformat()}"
    vista = f" · vista hasta las {_hora(hasta, huso)}" if hasta is not None else ""
    sesiones_html = "".join(
        _sesion_html(d, s, d.resultado.sesiones.get(s.nombre, TrazaSesion()), huso, hasta)
        for s in d.sesiones
    )
    cuerpo = [
        "<!doctype html>",
        f'<html lang="es"><head><meta charset="utf-8"><title>Visor {html.escape(titulo)}</title>',
        f"<style>{_CSS}</style></head><body>",
        f"<h1>Visor de dia: {html.escape(titulo)}{html.escape(vista)}</h1>",
        f"<p>Motor: {html.escape(d.motor)} · reloj de pared: {html.escape(d.huso)} · ventana "
        f"{html.escape(d.ventana[0])}-{html.escape(d.ventana[1])} · operaciones del trader "
        f"{len(trader)}, del bot {len(bot)}, parejas del criterio {len(parejas)}</p>",
        '<p class="leyenda"><span>■ azul: trader</span><span>■ morado: bot</span>'
        "<span>-- rojo: stop</span><span>·· verde: objetivo DERIVADO por regla (objetivo_rr; "
        "el caso no trae objetivo, ADR-0043)</span><span>— naranja: pareja del criterio</span>"
        "</p>",
        '<input type="checkbox" id="m15"><label for="m15"> ver M15 en vez de M1</label>',
        f'<div class="grafico">{grafico}</div>',
        "<h2>Hechos del motor, en el instante en que se fijaron</h2>",
        _hechos_svg(d, lienzo, huso, hasta),
        "<h2>Contexto H4: la previa y las que miro el sesgo</h2>",
        _h4_svg(d, huso),
        "<h2>Por sesion</h2>",
        sesiones_html,
        "<h2>Operaciones</h2>",
        _operaciones_html(recortado, huso, (*trader, *bot)),
        "</body></html>",
    ]
    return "\n".join(cuerpo) + "\n"


# ---------------------------------------------------------------------------------- indice


@dataclass(frozen=True)
class FilaIndice:
    caso: str
    dia: str
    sesiones_con_trader: int
    operaciones_trader: int
    operaciones_bot: int
    parejas: int
    sesgos: str
    parada: str


def fila_indice(d: DiaVisor) -> FilaIndice:
    con_trader = {op.sesion for op in d.trader}
    trazas = {s.nombre: d.resultado.sesiones.get(s.nombre, TrazaSesion()) for s in d.sesiones}
    sesgos = "; ".join(
        f"{s.nombre} {trazas[s.nombre].anotaciones.get(ANOTACION_SESGO, arnes.SIN_ANOTACION)}"
        for s in d.sesiones
    )
    parada = "; ".join(
        f"{s.nombre}: {donde_se_para(trazas[s.nombre], d.hechos)}" for s in d.sesiones
    )
    return FilaIndice(
        d.caso,
        d.dia.isoformat(),
        len(con_trader),
        len(d.trader),
        len(d.bot),
        len(d.parejas),
        sesgos,
        parada,
    )


def render_indice(filas: Sequence[FilaIndice], motor: str) -> str:
    cuerpo = [
        "<!doctype html>",
        '<html lang="es"><head><meta charset="utf-8"><title>Visor de dias de construccion</title>',
        f"<style>{_CSS}</style></head><body>",
        "<h1>Visor de dias de construccion</h1>",
        f"<p>Motor: {html.escape(motor)} · {len(filas)} dias. Cada fila enlaza a su pagina.</p>",
        _tabla(
            (
                "caso",
                "dia",
                "sesiones con trader",
                "op. trader",
                "op. bot",
                "parejas",
                "sesgo por sesion",
                "donde se para el embudo",
            ),
            (
                _fila(
                    f'<a href="{html.escape(f.caso)}.html">{html.escape(f.caso)}</a>',
                    html.escape(f.dia),
                    str(f.sesiones_con_trader),
                    str(f.operaciones_trader),
                    str(f.operaciones_bot),
                    str(f.parejas),
                    html.escape(f.sesgos),
                    html.escape(f.parada),
                )
                for f in sorted(filas, key=lambda f: (f.dia, f.caso))
            ),
        ),
        "</body></html>",
    ]
    return "\n".join(cuerpo) + "\n"


def generar(dias: Sequence[DiaVisor], salida: Path, motor: str, con_indice: bool) -> list[Path]:
    """Escribe una pagina por dia y, si se pide, el indice. Determinista: mismos bytes siempre."""
    salida.mkdir(parents=True, exist_ok=True)
    escritos: list[Path] = []
    for d in sorted(dias, key=lambda d: (d.dia, d.caso)):
        ruta = salida / f"{d.caso}.html"
        ruta.write_text(render_dia(d), encoding="utf-8", newline="\n")
        escritos.append(ruta)
    if con_indice:
        ruta = salida / INDICE
        ruta.write_text(
            render_indice([fila_indice(d) for d in dias], motor), encoding="utf-8", newline="\n"
        )
        escritos.append(ruta)
    return escritos


__all__ = [
    "BOT",
    "CARPETA_SALIDA",
    "INDICE",
    "TRADER",
    "DiaVisor",
    "FilaIndice",
    "Lienzo",
    "OperacionVisor",
    "Preparador",
    "SesgoSesion",
    "caso_de_construccion",
    "donde_se_para",
    "embudo_de_sesion",
    "fila_indice",
    "generar",
    "render_dia",
    "render_indice",
]
