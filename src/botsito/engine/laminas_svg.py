"""El dibujo de las laminas (rama `trabajo/laminas`): un HTML autocontenido por lamina con un SVG
escrito aqui, sin JavaScript ni dependencias, determinista (orden fijo, numeros con formato fijo,
sin reloj). Solo recibe una `Composicion` -el dibujo y las frases que `engine/laminas.py` saca de
una foto-: no ve el `Cierre`, ni el motor, ni nada posterior al corte, que es su borde derecho.

A la estetica de FX Replay es la disposicion (encargo, punto 8): tres paneles, H4, M15 y M1, uno
sobre otro; los precios en el eje derecho; las horas del huso de las sesiones abajo; los niveles de
la caja rotulados; y el corte en el borde derecho, la ultima vela la del corte, como su replay. Los
colores, en la tabla unica de abajo (la primera; la ajustan Aleks y el consultor al revisar)."""

from __future__ import annotations

import bisect
import html
from collections.abc import Sequence
from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from botsito.domain.pivotes_m15 import ALTO
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import Vela
from botsito.engine.laminas import (
    Composicion,
    Dibujo,
    LaminaError,
    LineaDibujada,
    hora,
    precio,
)

# ---------------------------------------------------------------------- la tabla de colores

COLOR = {
    "fondo": "#ffffff",
    "rejilla": "#eeeeee",
    "separador": "#cccccc",
    "verde": "#26a69a",
    "roja": "#ef5350",
    "sin_cuerpo": "#9e9e9e",
    "h4_fija": "#f39c12",
    "h4_saltada": "#7f8c8d",
    "m15_alto": "#3b6fd6",
    "m15_bajo": "#8e44ad",
    "caja_compra": "#2e8b57",
    "caja_venta": "#c0392b",
    "nivel": "#888888",
    "orden": "#1f4e9c",
    "stop": "#c0392b",
    "objetivo": "#2e8b57",
    "punto": "#1565c0",
    "control": "#e67e22",
    "texto": "#444444",
    "ejes": "#666666",
}
OPACIDAD_H4_FIJA = "0.25"  # no-negocio: relleno de la vela H4 que fija el sesgo, solo dibujo
OPACIDAD_CAJA = "0.16"

ANCHO = 1600
ALTO_PANEL = 300
MARGEN_IZQ = 20
MARGEN_DER = 110
MARGEN_SUP = 30
MARGEN_INF = 30
TAMANO_ROTULO = 11  # la altura de la letra de los rotulos de la caja
ALTO_ETIQUETA = 16  # la de las etiquetas de la orden en el eje derecho
TAMANO_MARCA = 10  # la de las marcas de las lineas de M15 que quedan fuera del M1
# El panel «M1 de cerca» (respuesta del consultor tras revisar la v3, punto 1): constantes de dibujo
VELAS_CERCA_MAX = 60  # como mucho, las ultimas 60 velas hasta el corte
VELAS_CERCA_SIN_TOMA = 30  # sin toma, las 30 ultimas
VELAS_ANTES_DEL_CONTROL = 15  # desde 15 velas antes de la primera zona de control, si es anterior
PANELES = 4  # H4, M15, M1 y M1 de cerca
MARCO_CERCA = "M1 de cerca"
ANCHO_MARCA = 90  # dos marcas de borde a menos de esto en x, en el mismo borde, se apilan

EtiquetaEje = tuple[str, int, str]  # una etiqueta del eje: su clase, su nivel y su color
Marca = tuple[str, int, float, str]  # una marca de borde: su clase, su nivel, su x y su color
# un borde del color del fondo alrededor de las letras de los rotulos y de las marcas de borde, que
# se dibujan encima de las velas: asi se leen aunque caigan sobre una (capturas de la v4)
HALO = f'stroke="{COLOR["fondo"]}" stroke-width="3" paint-order="stroke"'


def _f(x: float) -> str:
    return f"{x:.1f}"


class _Panel:
    """Un panel: sus velas, su escala de precios y de tiempo, y lo que se dibuja encima."""

    def __init__(self, velas: Sequence[Vela], marco: str, y0: int, niveles: Sequence[int]) -> None:
        if not velas:
            raise LaminaError(f"el panel {marco} se queda sin velas")
        self.velas = tuple(velas)
        self.marco = marco
        self.y0 = y0
        self.inicios = [int(v.inicio) for v in self.velas]
        precios = [int(v.maxima) for v in velas] + [int(v.minima) for v in velas] + list(niveles)
        self.hi, self.lo = max(precios), min(precios)
        self.rango = max(self.hi - self.lo, 1)
        self.paso = (ANCHO - MARGEN_IZQ - MARGEN_DER) / len(self.velas)
        self.derecha = MARGEN_IZQ + len(self.velas) * self.paso

    def y(self, p: int) -> float:
        alto = ALTO_PANEL - MARGEN_SUP - MARGEN_INF
        return self.y0 + MARGEN_SUP + (self.hi - p) / self.rango * alto

    def x(self, minuto: int) -> float:
        """La x de un minuto UTC: dentro de su vela, en proporcion; antes de la primera, el borde
        izquierdo; desde el fin de la ultima (el corte), el derecho."""
        i = bisect.bisect_right(self.inicios, minuto) - 1
        if i < 0:
            return float(MARGEN_IZQ)
        v = self.velas[i]
        fraccion = min((minuto - int(v.inicio)) / max(v.duracion_min, 1), 1)
        return min(MARGEN_IZQ + (i + fraccion) * self.paso, self.derecha)

    def centro(self, minuto: int) -> float | None:
        """El centro de la vela que empieza en `minuto`, o None si no esta en el panel."""
        i = bisect.bisect_left(self.inicios, minuto)
        if i < len(self.inicios) and self.inicios[i] == minuto:
            return MARGEN_IZQ + (2 * i + 1) * self.paso / 2
        return None


def _velas(p: _Panel, huso: str, escala: int, ocupadas: Sequence[float] = ()) -> list[str]:
    """Las velas, la rejilla de precios del eje derecho y las horas. Un precio de la rejilla que
    caeria bajo una etiqueta de la orden (`ocupadas`, sus y) no se escribe (respuesta del consultor
    a la PARADA final de la ronda, punto 3)."""
    tz = ZoneInfo(huso)
    partes = [
        f'<text class="marco" x="{MARGEN_IZQ}" y="{p.y0 + 20}" font-size="18" '
        f'font-weight="bold" fill="{COLOR["texto"]}">{p.marco}</text>',
        f'<line class="corte" x1="{_f(p.derecha)}" y1="{p.y0 + MARGEN_SUP}" x2="{_f(p.derecha)}" '
        f'y2="{p.y0 + ALTO_PANEL - MARGEN_INF}" stroke="{COLOR["ejes"]}"/>',
    ]
    for k in range(5):
        nivel = p.lo + p.rango * k // 4
        if any(abs(p.y(nivel) - y) < ALTO_ETIQUETA for y in ocupadas):
            continue
        partes.append(
            f'<text class="precio" x="{ANCHO - MARGEN_DER + 8}" y="{_f(p.y(nivel) + 4)}" '
            f'font-size="12" fill="{COLOR["ejes"]}">{precio(nivel, escala)}</text>'
        )
    cada = max(1, len(p.velas) // 10)
    anterior: date | None = None
    for i, v in enumerate(p.velas):
        x = MARGEN_IZQ + (2 * i + 1) * p.paso / 2
        local = datetime.fromtimestamp(int(v.inicio) * 60, UTC).astimezone(tz)
        if anterior is not None and local.date() != anterior:
            xs = MARGEN_IZQ + i * p.paso
            partes.append(
                f'<line class="dia" x1="{_f(xs)}" y1="{p.y0 + MARGEN_SUP}" x2="{_f(xs)}" '
                f'y2="{p.y0 + ALTO_PANEL - MARGEN_INF}" stroke="{COLOR["separador"]}" '
                f'stroke-dasharray="4 4"/>'
            )
        anterior = local.date()
        color = (
            COLOR["verde"] if v.cierre > v.abierta
            else COLOR["roja"] if v.cierre < v.abierta else COLOR["sin_cuerpo"]
        )  # fmt: skip
        arriba, abajo = max(int(v.abierta), int(v.cierre)), min(int(v.abierta), int(v.cierre))
        partes.append(
            f'<line x1="{_f(x)}" y1="{_f(p.y(int(v.maxima)))}" x2="{_f(x)}" '
            f'y2="{_f(p.y(int(v.minima)))}" stroke="{color}"/>'
        )
        partes.append(
            f'<rect class="vela" x="{_f(x - p.paso * 7 / 20)}" y="{_f(p.y(arriba))}" '
            f'width="{_f(p.paso * 7 / 10)}" height="{_f(max(p.y(abajo) - p.y(arriba), 1))}" '
            f'fill="{color}"/>'
        )
        if i % cada == 0:
            partes.append(
                f'<text class="hora" x="{_f(x)}" y="{p.y0 + ALTO_PANEL - 10}" font-size="11" '
                f'text-anchor="middle" fill="{COLOR["ejes"]}">{local:%H:%M}</text>'
            )
    return partes


def _horizontal(
    p: _Panel, clase: str, nivel: int, desde: int, hasta: int, color: str, extra: str
) -> str:
    return (
        f'<line class="{clase}" x1="{_f(p.x(desde))}" y1="{_f(p.y(nivel))}" x2="{_f(p.x(hasta))}" '
        f'y2="{_f(p.y(nivel))}" stroke="{color}" {extra}/>'
    )


def _lineas_m15(p: _Panel, d: Dibujo, lineas: Sequence[LineaDibujada]) -> list[str]:
    partes = []
    for ln in lineas:
        color = COLOR["m15_alto"] if ln.lado == ALTO else COLOR["m15_bajo"]
        estado = "tomada" if ln.tomada else "dejo" if ln.dejo else "viva"
        extra = (
            'stroke-width="3"'
            if ln.tomada
            else 'stroke-width="1.5" stroke-dasharray="6 4"'
            if ln.dejo
            else 'stroke-width="1.5"'
        )
        partes.append(
            _horizontal(
                p, f"linea-m15 {ln.lado} {estado}", ln.nivel, ln.desde, ln.hasta, color, extra
            )
        )
    if d.toma is not None:
        inicio, nivel = d.toma
        x = p.centro(inicio) if p.marco.startswith("M1") else p.x(inicio + 1)
        # en el M1 de cerca la linea tomada puede quedar fuera de la escala (va como marca de
        # borde): el punto no se dibuja fuera del panel (captura de la v4)
        if x is not None and p.lo <= nivel <= p.hi:
            partes.append(
                f'<circle class="toma" cx="{_f(x)}" cy="{_f(p.y(nivel))}" r="5" '
                f'fill="{COLOR["texto"]}"/>'
            )
    return partes


def lineas_del_m1(d: Dibujo) -> tuple[tuple[LineaDibujada, ...], tuple[LineaDibujada, ...]]:
    """Las lineas de M15 que se dibujan en el M1 y las que quedan fuera (respuesta del consultor a
    la PARADA final de la ronda, punto 2): dentro, las que caen en el rango de precios de las velas
    del M1, de la caja y de la orden, ampliado por arriba y por abajo una altura de caja (sin caja,
    un decimo del rango); y la que el motor tomo, siempre."""
    precios = [int(v.maxima) for v in d.m1] + [int(v.minima) for v in d.m1]
    if d.caja is not None:
        precios += [d.caja.entrada, d.caja.extremo]
    for o in d.ordenes:
        precios += [o.precio, o.stop, o.objetivo]
    hi, lo = max(precios), min(precios)
    margen = abs(d.caja.entrada - d.caja.extremo) if d.caja is not None else (hi - lo) // 10
    dentro = tuple(ln for ln in d.lineas if ln.tomada or lo - margen <= ln.nivel <= hi + margen)
    return dentro, tuple(ln for ln in d.lineas if ln not in dentro)


def _marca(
    p: _Panel, clase: str, nivel: int, x: float, color: str, escala: int, fila: int = 0
) -> str:
    """Una marca pequena en el borde de arriba o de abajo de un panel para un nivel que no cabe en
    su escala: su precio y una flecha hacia donde esta. `fila` la aparta del borde cuando otra
    marca cae en el mismo sitio."""
    arriba = nivel > p.hi
    apartada = fila * (TAMANO_MARCA + 2)
    y = (
        p.y0 + MARGEN_SUP + TAMANO_MARCA + apartada
        if arriba
        else p.y0 + ALTO_PANEL - MARGEN_INF - 3 - apartada
    )
    x = max(x, float(MARGEN_IZQ))
    ancla = "end" if x > p.derecha - 80 else "start"
    x = min(x, p.derecha)
    flecha = "▲" if arriba else "▼"
    return (
        f'<text class="{clase}" x="{_f(x)}" y="{_f(y)}" font-size="{TAMANO_MARCA}" '
        f'text-anchor="{ancla}" fill="{color}" {HALO}>{flecha} {precio(nivel, escala)}</text>'
    )


def _fuera(
    p: _Panel, lineas: Sequence[LineaDibujada], escala: int, otras: Sequence[Marca] = ()
) -> list[str]:
    """Una marca de borde por cada linea de M15 que no cabe en el panel, del color de su lado, y las
    `otras` del panel (la del objetivo, de `_m1`). Dos en el mismo borde y casi en la misma x se
    apilan, sean de la clase que sean, para que no se monten (capturas y revisor de la v4)."""
    marcas: list[Marca] = [
        (
            f"m15-fuera {ln.lado}", ln.nivel, p.x(ln.desde),
            COLOR["m15_alto"] if ln.lado == ALTO else COLOR["m15_bajo"],
        )
        for ln in lineas
    ] + list(otras)  # fmt: skip
    partes: list[str] = []
    puestas: list[tuple[bool, float]] = []
    for clase, nivel, x, color in sorted(marcas, key=lambda m: (m[2], m[1], m[0])):
        arriba = nivel > p.hi
        fila = sum(1 for a, xp in puestas if a == arriba and abs(xp - x) < ANCHO_MARCA)
        puestas.append((arriba, x))
        partes.append(_marca(p, clase, nivel, x, color, escala, fila))
    return partes


def tramo_de_cerca(d: Dibujo) -> tuple[Vela, ...]:
    """Las velas del panel «M1 de cerca» (respuesta del consultor tras revisar la v3, punto 1): de
    la M1 de la toma -o de 15 velas antes de la primera zona de control que se dibuja, si es
    anterior- hasta el corte, como mucho 60 (si no, las 60 ultimas); sin toma, las 30 ultimas. Un
    subconjunto de las velas del M1, que ya pasaron la puerta."""
    velas = d.m1
    inicios = [int(v.inicio) for v in velas]
    if d.toma is None:
        return tuple(velas[-VELAS_CERCA_SIN_TOMA:])
    desde = bisect.bisect_left(inicios, d.toma[0])
    controles = [bisect.bisect_left(inicios, i) for i, _ in d.control if i in inicios]
    if controles:
        desde = min(desde, min(controles) - VELAS_ANTES_DEL_CONTROL)
    desde = max(desde, 0, len(velas) - VELAS_CERCA_MAX)
    return tuple(velas[desde:])


def rotulos_visibles(p: _Panel, niveles: Sequence[tuple[str, int]]) -> tuple[tuple[str, int], ...]:
    """Los rotulos de la caja que se escriben (respuesta del consultor a la PARADA final de la
    ronda, punto 1): los cinco; si dos quedan a menos de la altura de su letra, el 0, el del stop y
    el 1; si aun asi se montan, el 0 y el 1. `niveles` va en el orden de `laminas._niveles`: 0,
    0,25, 0,5, el del stop y 1."""
    for elegidos in (tuple(niveles), (niveles[0], niveles[-2], niveles[-1])):
        ys = sorted(p.y(n) for _, n in elegidos)
        if all(b - a >= TAMANO_ROTULO for a, b in zip(ys, ys[1:], strict=False)):
            return elegidos
    return (niveles[0], niveles[-1])


def _h4(p: _Panel, d: Dibujo) -> list[str]:
    partes = []
    for inicio, clase in [(i, "h4-saltada") for i in d.h4_saltadas] + (
        [(d.h4_fija, "h4-fija")] if d.h4_fija is not None else []
    ):
        x = p.centro(inicio)
        if x is None:
            continue
        v = p.velas[p.inicios.index(inicio)]
        y1, y2 = p.y(int(v.maxima)) - 4, p.y(int(v.minima)) + 4
        if clase == "h4-fija":
            estilo = (
                f'fill="{COLOR["h4_fija"]}" fill-opacity="{OPACIDAD_H4_FIJA}" '
                f'stroke="{COLOR["h4_fija"]}"'
            )
        else:
            estilo = f'fill="none" stroke="{COLOR["h4_saltada"]}" stroke-dasharray="4 3"'
        partes.append(
            f'<rect class="{clase}" x="{_f(x - p.paso / 2)}" y="{_f(y1)}" width="{_f(p.paso)}" '
            f'height="{_f(y2 - y1)}" {estilo}/>'
        )
    return partes


def _m1(p: _Panel, d: Dibujo) -> tuple[list[str], list[str], list[Marca]]:
    """Lo del M1 que va detras de las velas (la caja, sus niveles, el punto, las zonas de control y
    las lineas de la orden), lo que va delante, para que ninguna vela lo tape (los rotulos de la
    caja), y las marcas de borde de la orden, que dibuja `_fuera` junto a las de M15 para que se
    apilen con ellas (capturas y revisor de la v4)."""
    partes: list[str] = []
    delante: list[str] = []
    marcas: list[Marca] = []
    if d.caja is not None:
        z = d.caja
        color = COLOR["caja_compra"] if z.lado == "compra" else COLOR["caja_venta"]
        x1 = p.x(z.desde if z.desde is not None else int(z.formada or 0))
        y1, y2 = sorted((p.y(z.entrada), p.y(z.extremo)))
        partes.append(
            f'<rect class="caja {z.lado}" x="{_f(x1)}" y="{_f(y1)}" width="{_f(p.derecha - x1)}" '
            f'height="{_f(max(y2 - y1, 1))}" fill="{color}" fill-opacity="{OPACIDAD_CAJA}"/>'
        )
        for _, nivel in d.niveles:
            partes.append(
                _horizontal(
                    p,
                    "nivel",
                    nivel,
                    z.desde or int(z.formada or 0),
                    d.corte,
                    COLOR["nivel"],
                    'stroke-width="1"',
                )
            )
        for rotulo, nivel in rotulos_visibles(p, d.niveles):
            delante.append(
                f'<text class="rotulo" x="{_f(p.derecha - 4)}" y="{_f(p.y(nivel) - 3)}" '
                f'font-size="{TAMANO_ROTULO}" text-anchor="end" fill="{COLOR["nivel"]}" {HALO}>'
                f"{rotulo}</text>"
            )
    if d.punto is not None:
        inicio, nivel = d.punto
        x = p.centro(inicio)
        if x is not None:
            partes.append(
                f'<circle class="punto" cx="{_f(x)}" cy="{_f(p.y(nivel))}" r="5" fill="none" '
                f'stroke="{COLOR["punto"]}" stroke-width="2"/>'
            )
    for inicio, nivel in d.control:
        x = p.centro(inicio)
        if x is not None:
            partes.append(  # sin pasar del borde del corte (revisor, b-m3)
                f'<rect class="zona-control" x="{_f(min(x - 4, p.derecha - 8))}" '
                f'y="{_f(p.y(nivel) - 4)}" width="8" '
                f'height="8" fill="{COLOR["control"]}"/>'
            )
    for o in d.ordenes:
        # desde el INICIO de la M1 que la coloca: en una lamina de tipo a la orden nace en el
        # mismo cierre del corte, y desde su cierre la linea no tendria largo (lo enseno la
        # captura de la respuesta a la PARADA final, punto 5); y su precio, en el eje derecho
        desde = (o.colocada_ms + 1) // MS_POR_MINUTO - 1
        for clase, nivel, color, extra in (
            ("orden", o.precio, COLOR["orden"], 'stroke-width="3"'),
            ("stop", o.stop, COLOR["stop"], 'stroke-width="2" stroke-dasharray="6 4"'),
            ("objetivo", o.objetivo, COLOR["objetivo"], 'stroke-width="2" stroke-dasharray="6 4"'),
        ):
            if p.lo <= nivel <= p.hi:  # su precio en el eje lo pone `_etiquetas`
                partes.append(_horizontal(p, clase, nivel, desde, d.corte, color, extra))
            else:  # en el M1 de cerca, el objetivo suele quedar fuera de su escala
                marcas.append((f"{clase}-fuera", nivel, p.x(desde), color))
    return partes, delante, marcas


def _etiqueta(p: _Panel, clase: str, nivel: int, color: str, escala: int, y: float) -> str:
    """El precio de una linea en el eje derecho, sobre su color (como el replay), en la `y`."""
    return (
        f'<rect class="eje-{clase}" x="{_f(p.derecha + 2)}" y="{_f(y - ALTO_ETIQUETA / 2)}" '
        f'width="78" height="{ALTO_ETIQUETA}" fill="{color}"/>'
        f'<text class="eje-{clase}" x="{_f(p.derecha + 6)}" y="{_f(y + 4)}" font-size="12" '
        f'fill="{COLOR["fondo"]}">{precio(nivel, escala)}</text>'
    )


def _pedidas(p: _Panel, d: Dibujo, tomadas: Sequence[LineaDibujada] = ()) -> list[EtiquetaEje]:
    """Las etiquetas del eje de un panel: la orden, el stop y el objetivo que caben en su escala, y
    las lineas de M15 tomadas que se le pasen (en el M1 de cerca, para leer separados la liquidez y
    el 0: captura de la v4)."""
    pedidas: list[EtiquetaEje] = []
    for o in d.ordenes:
        for clase, nivel in (("orden", o.precio), ("stop", o.stop), ("objetivo", o.objetivo)):
            if p.lo <= nivel <= p.hi:
                pedidas.append((clase, nivel, COLOR[clase]))
    for ln in tomadas:
        color = COLOR["m15_alto"] if ln.lado == ALTO else COLOR["m15_bajo"]
        pedidas.append(("linea-tomada", ln.nivel, color))
    return pedidas


def _etiquetas(
    p: _Panel, pedidas: Sequence[EtiquetaEje], escala: int
) -> tuple[list[str], list[float]]:
    """Las etiquetas del eje, cada una con su precio, sin montarse: de arriba abajo, la que caeria
    a menos de ALTO_ETIQUETA de la anterior baja lo que haga falta; si la ultima se sale por abajo,
    se suben desde el borde (captura de la v4: dos etiquetas una encima de otra). Devuelve lo que
    se dibuja y las y donde quedan, que la rejilla no escribe."""
    orden = sorted(pedidas, key=lambda x: (p.y(x[1]), x[0]))
    ys: list[float] = []
    for _, nivel, _ in orden:
        y = p.y(nivel)
        ys.append(max(y, ys[-1] + ALTO_ETIQUETA) if ys else y)
    fondo = p.y0 + ALTO_PANEL - ALTO_ETIQUETA / 2
    for i in range(len(ys) - 1, -1, -1):
        tope = fondo if i == len(ys) - 1 else ys[i + 1] - ALTO_ETIQUETA
        ys[i] = min(ys[i], tope)
    partes = [
        _etiqueta(p, clase, nivel, color, escala, y)
        for (clase, nivel, color), y in zip(orden, ys, strict=True)
    ]
    return partes, ys


def svg(d: Dibujo) -> str:
    niveles_m15 = [ln.nivel for ln in d.lineas]
    en_m1, fuera_m1 = lineas_del_m1(d)
    niveles_m1 = [ln.nivel for ln in en_m1] + [n for _, n in d.niveles]
    niveles_m1 += [n for _, n in d.control] + ([d.punto[1]] if d.punto else [])
    for o in d.ordenes:
        niveles_m1 += [o.precio, o.stop, o.objetivo]
    h4 = _Panel(d.h4, "H4", 0, ())
    m15 = _Panel(d.m15, "M15", ALTO_PANEL, niveles_m15)
    m1 = _Panel(d.m1, "M1", ALTO_PANEL * 2, niveles_m1)
    # el M1 de cerca: su escala, las velas del tramo, la caja, la orden y el stop
    niveles_cerca = [d.caja.entrada, d.caja.extremo] if d.caja is not None else []
    for o in d.ordenes:
        niveles_cerca += [o.precio, o.stop]
    cerca = _Panel(tramo_de_cerca(d), MARCO_CERCA, ALTO_PANEL * 3, niveles_cerca)
    # en el M1 de cerca, solo las lineas que llegan al tramo: una que acabo antes no se ve, y ni su
    # precio en el eje ni su marca de borde tienen a que referirse (captura de la v4)
    vistas = tuple(ln for ln in d.lineas if ln.hasta > cerca.inicios[0])
    en_cerca = tuple(ln for ln in vistas if cerca.lo <= ln.nivel <= cerca.hi)
    fuera_cerca = tuple(ln for ln in vistas if ln not in en_cerca)
    alto = ALTO_PANEL * PANELES
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{alto}" '
        f'viewBox="0 0 {ANCHO} {alto}" font-family="sans-serif">',
        f'<rect x="0" y="0" width="{ANCHO}" height="{alto}" fill="{COLOR["fondo"]}"/>',
    ]
    partes += _h4(h4, d) + _velas(h4, d.huso, d.escala)
    partes += _velas(m15, d.huso, d.escala) + _lineas_m15(m15, d, d.lineas)
    # en el M1 y en el M1 de cerca: detras, las velas, las lineas; y delante, lo que no se tapa
    etiquetas, ocupadas = _etiquetas(m1, _pedidas(m1, d), d.escala)
    detras, delante, marcas = _m1(m1, d)
    partes += detras + _velas(m1, d.huso, d.escala, ocupadas) + _lineas_m15(m1, d, en_m1)
    partes += delante + _fuera(m1, fuera_m1, d.escala, marcas) + etiquetas
    tomadas = [ln for ln in en_cerca if ln.tomada]
    etiquetas, ocupadas = _etiquetas(cerca, _pedidas(cerca, d, tomadas), d.escala)
    detras, delante, marcas = _m1(cerca, d)
    partes += detras + _velas(cerca, d.huso, d.escala, ocupadas) + _lineas_m15(cerca, d, en_cerca)
    partes += delante + _fuera(cerca, fuera_cerca, d.escala, marcas) + etiquetas
    partes.append("</svg>")
    return "\n".join(partes)


ESTILO = (
    f"body{{font-family:sans-serif;color:{COLOR['texto']};margin:24px;}}"
    "h1{font-size:22px;}li{margin:4px 0;font-size:16px;}"
)


def pagina(comp: Composicion, k: int, cabecera: str) -> str:
    d = comp.dibujo
    frases = "\n".join(f"<li>{html.escape(f)}</li>" for f in comp.frases)
    return (
        '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        f"<style>{ESTILO}</style>\n</head>\n<body>\n"
        f"<h1>Lámina {k}</h1>\n"
        f"<p>{html.escape(cabecera)}. Corte: a las {hora(d.corte, d.huso)}, al cierre de la vela "
        f"de M1 de las {hora(d.corte - 1, d.huso)}.</p>\n"
        f"{svg(d)}\n"
        f"<h2>Lo que tenía el bot en ese instante</h2>\n<ul>\n{frases}\n</ul>\n"
        "</body>\n</html>\n"
    )


def indice(cabecera: str, entradas: Sequence[tuple[str, int, str]]) -> str:
    filas = (
        "\n".join(
            f'<li><a href="{nombre}">Lámina {k}</a>: corte a las {corte}</li>'
            for nombre, k, corte in entradas
        )
        or "<li>Esta sesión no tiene láminas.</li>"
    )
    return (
        '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        f"<style>{ESTILO}</style>\n</head>\n<body>\n<h1>Láminas</h1>\n"
        f"<p>{html.escape(cabecera)}.</p>\n<ul>\n{filas}\n</ul>\n</body>\n</html>\n"
    )


__all__ = ["COLOR", "indice", "pagina", "svg"]
