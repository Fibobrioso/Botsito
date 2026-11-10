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
from botsito.engine.laminas import Composicion, Dibujo, LaminaError, hora, precio

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


def _velas(p: _Panel, huso: str, escala: int) -> list[str]:
    tz = ZoneInfo(huso)
    partes = [
        f'<text class="marco" x="{MARGEN_IZQ}" y="{p.y0 + 20}" font-size="18" '
        f'font-weight="bold" fill="{COLOR["texto"]}">{p.marco}</text>',
        f'<line class="corte" x1="{_f(p.derecha)}" y1="{p.y0 + MARGEN_SUP}" x2="{_f(p.derecha)}" '
        f'y2="{p.y0 + ALTO_PANEL - MARGEN_INF}" stroke="{COLOR["ejes"]}"/>',
    ]
    for k in range(5):
        nivel = p.lo + p.rango * k // 4
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


def _lineas_m15(p: _Panel, d: Dibujo) -> list[str]:
    partes = []
    for ln in d.lineas:
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
        x = p.centro(inicio) if p.marco == "M1" else p.x(inicio + 1)
        if x is not None:
            partes.append(
                f'<circle class="toma" cx="{_f(x)}" cy="{_f(p.y(nivel))}" r="5" '
                f'fill="{COLOR["texto"]}"/>'
            )
    return partes


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


def _m1(p: _Panel, d: Dibujo) -> list[str]:
    partes = []
    if d.caja is not None:
        z = d.caja
        color = COLOR["caja_compra"] if z.lado == "compra" else COLOR["caja_venta"]
        x1 = p.x(z.desde if z.desde is not None else int(z.formada or 0))
        y1, y2 = sorted((p.y(z.entrada), p.y(z.extremo)))
        partes.append(
            f'<rect class="caja {z.lado}" x="{_f(x1)}" y="{_f(y1)}" width="{_f(p.derecha - x1)}" '
            f'height="{_f(max(y2 - y1, 1))}" fill="{color}" fill-opacity="{OPACIDAD_CAJA}"/>'
        )
        for rotulo, nivel in d.niveles:
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
            partes.append(
                f'<text class="rotulo" x="{_f(p.derecha - 4)}" y="{_f(p.y(nivel) - 3)}" '
                f'font-size="11" text-anchor="end" fill="{COLOR["nivel"]}">{rotulo}</text>'
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
            partes.append(
                f'<rect class="zona-control" x="{_f(x - 4)}" y="{_f(p.y(nivel) - 4)}" width="8" '
                f'height="8" fill="{COLOR["control"]}"/>'
            )
    for o in d.ordenes:
        desde = (o.colocada_ms + 1) // MS_POR_MINUTO
        for clase, nivel, color, extra in (
            ("orden", o.precio, COLOR["orden"], 'stroke-width="3"'),
            ("stop", o.stop, COLOR["stop"], 'stroke-width="2" stroke-dasharray="6 4"'),
            ("objetivo", o.objetivo, COLOR["objetivo"], 'stroke-width="2" stroke-dasharray="6 4"'),
        ):
            partes.append(_horizontal(p, clase, nivel, desde, d.corte, color, extra))
    return partes


def svg(d: Dibujo) -> str:
    niveles_m15 = [ln.nivel for ln in d.lineas]
    niveles_m1 = list(niveles_m15) + [n for _, n in d.niveles]
    niveles_m1 += [n for _, n in d.control] + ([d.punto[1]] if d.punto else [])
    for o in d.ordenes:
        niveles_m1 += [o.precio, o.stop, o.objetivo]
    h4 = _Panel(d.h4, "H4", 0, ())
    m15 = _Panel(d.m15, "M15", ALTO_PANEL, niveles_m15)
    m1 = _Panel(d.m1, "M1", ALTO_PANEL * 2, niveles_m1)
    partes = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{ANCHO}" height="{ALTO_PANEL * 3}" '
        f'viewBox="0 0 {ANCHO} {ALTO_PANEL * 3}" font-family="sans-serif">',
        f'<rect x="0" y="0" width="{ANCHO}" height="{ALTO_PANEL * 3}" fill="{COLOR["fondo"]}"/>',
    ]
    partes += _h4(h4, d) + _velas(h4, d.huso, d.escala)
    partes += _velas(m15, d.huso, d.escala) + _lineas_m15(m15, d)
    partes += _m1(m1, d) + _velas(m1, d.huso, d.escala) + _lineas_m15(m1, d)
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
