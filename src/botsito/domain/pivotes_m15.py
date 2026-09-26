"""El pivote de M15 mas reciente ya formado (ADR-0045), con el momento de «formado» como SELECTOR
y no como decision: A-35 sigue ABIERTA y la responde el trader.

Lo que si esta documentado, y de donde sale cada cosa:

- **El extremo lo marca la vela CONTRARIA al flujo de M15**, no un recuento de velas a cada lado,
  que el trader rehusa (`ev-v3-011540-5425b533`, v3 #975-#976; `ev-v4-005749-1e9325cb`, v4 #942;
  `docs/validation/A35-PIVOTE-FORMADO-CLASIFICACION.md`, dudas 1). En un flujo alcista una vela
  roja marca un ALTO; en un flujo bajista una vela verde marca un BAJO.
- **Cuando esta formado** es lo que A-35 pregunta, y el corpus documenta DOS lecturas, que son las
  dos opciones del selector `liquidez_m15_pivote_formado`:
  - `inicio_vela_contraria`: «apenas se inicia una vela contraria en un flujo de ordenes, yo ya lo
    tomo como un punto en el cual yo ya voy marcando» (v4 #942, `ev-v4-005749-1e9325cb`, P9 de la
    clasificacion). El pivote esta disponible desde el primer cierre de M1 en que la M15 en curso
    va contraria al flujo.
  - `cierre_vela_contraria`: «Uno ya formado», «Por encima de este ya formado» frente a «el punto
    mas alto de las ultimas velas aunque sigan en curso» (v4 #846, #849, `ev-v4-005053-885e2773`,
    P8), leido como que la vela que deja atras el extremo tiene que estar cerrada. El pivote esta
    disponible desde el cierre de esa vela.
  Ninguna otra lectura esta documentada (dudas 1 y 2 de la clasificacion): no se anade ninguna.
- **El mas reciente** de los formados es el que cuenta (ADR-0045, `ev-v1-001334-96e8ca40`).

Lo que NO esta documentado y aqui se deja FIJO Y VISIBLE, sin decidirlo por el trader (candidatos a
ambiguedad en `docs/validation/PREPARACION-A35-A44.md`): el nivel es el extremo de la racha de
velas del mismo color inmediatamente anterior a la contraria, y la mecha de la propia vela
contraria no lo mueve («¿que haces si despues el precio lo supera un poco?» es la segunda pregunta
de A-35); una vela sin cuerpo (cierre igual a la apertura) no es de ningun color, no es contraria
y corta la racha; y con la lectura `inicio_vela_contraria` el pivote es el ESTADO en cada instante:
si la vela en curso vuelve a su color, el pivote desaparece (P9 dice «voy marcando»).

Puro: velas dentro, pivote fuera. Sin reloj, sin IO, sin registro (ADR-0002: el selector lo lee
quien construye los datos del dia, no este modulo).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from botsito.domain.velas import MinutoUtc, Vela

INICIO_VELA_CONTRARIA = "inicio_vela_contraria"
CIERRE_VELA_CONTRARIA = "cierre_vela_contraria"
LECTURAS = (INICIO_VELA_CONTRARIA, CIERRE_VELA_CONTRARIA)
ALTO = "alto"
BAJO = "bajo"
LADOS = (ALTO, BAJO)


class PivoteError(ValueError):
    """Argumentos que el modelo no admite: nunca se adivina."""


@dataclass(frozen=True)
class Pivote:
    """Un pivote de M15 formado: su lado, su nivel en puntos, la vela contraria que lo marco y el
    primer instante (cierre de M1, minuto UTC) en que la lectura lo da por formado."""

    lado: str
    nivel: int
    contraria_inicio: MinutoUtc  # inicio de la vela contraria que lo marca
    contraria_fin: MinutoUtc  # su fin (aunque este en curso): desde ahi cuentan los toques
    formado_en: MinutoUtc


def color(v: Vela) -> int:
    """+1 verde (cierra por encima de su apertura), -1 roja, 0 sin cuerpo."""
    if v.cierre > v.abierta:
        return 1
    if v.cierre < v.abierta:
        return -1
    return 0


def _racha_anterior(velas: Sequence[Vela], hasta: int, signo: int) -> list[Vela]:
    """Las velas consecutivas de color `signo` que terminan justo antes del indice `hasta`."""
    racha: list[Vela] = []
    i = hasta - 1
    while i >= 0 and color(velas[i]) == signo:
        racha.append(velas[i])
        i -= 1
    racha.reverse()
    return racha


def _pivote_de(contraria: Vela, racha: Sequence[Vela], formado_en: MinutoUtc) -> Pivote:
    if color(contraria) < 0:
        return Pivote(
            ALTO,
            int(max(int(v.maxima) for v in racha)),
            contraria.inicio,
            contraria.fin,
            formado_en,
        )
    return Pivote(
        BAJO,
        int(min(int(v.minima) for v in racha)),
        contraria.inicio,
        contraria.fin,
        formado_en,
    )


def pivotes_formados(
    cerradas: Sequence[Vela], en_curso: Vela | None, lectura: str, instante: int
) -> list[Pivote]:
    """Todos los pivotes formados a la vista en `instante` (un cierre de M1), del mas antiguo al
    mas reciente. `cerradas` son las M15 con fin <= instante, en orden; `en_curso`, la M15 que
    contiene `instante` construida SOLO con las M1 cerradas hasta el (None si no hay ninguna)."""
    if lectura not in LECTURAS:
        raise PivoteError(f"lectura {lectura!r} no esta en {LECTURAS}")
    for a, b in zip(cerradas, cerradas[1:], strict=False):
        if b.inicio < a.fin:
            raise PivoteError("las M15 cerradas tienen que ir en orden y sin solapar")
    if cerradas and int(cerradas[-1].fin) > instante:
        raise PivoteError("una M15 'cerrada' termina despues del instante: mira al futuro")
    if en_curso is not None and cerradas and en_curso.inicio < cerradas[-1].fin:
        raise PivoteError("la M15 en curso empieza antes de que cierre la ultima cerrada")
    salida: list[Pivote] = []
    for i in range(1, len(cerradas)):
        c = cerradas[i]
        signo = color(c)
        if signo == 0:
            continue
        racha = _racha_anterior(cerradas, i, -signo)
        if not racha:
            continue
        # con la lectura `inicio` una vela ya cerrada tambien esta formada: el instante en que
        # empezo a contar es su primer cierre de M1, y ya paso
        formado = c.fin if lectura == CIERRE_VELA_CONTRARIA else MinutoUtc(int(c.inicio) + 1)
        salida.append(_pivote_de(c, racha, formado))
    if lectura == INICIO_VELA_CONTRARIA and en_curso is not None and cerradas:
        signo = color(en_curso)
        if signo != 0:
            racha = _racha_anterior(cerradas, len(cerradas), -signo)
            if racha:
                salida.append(_pivote_de(en_curso, racha, MinutoUtc(int(en_curso.inicio) + 1)))
    return salida


def pivote_mas_reciente(
    cerradas: Sequence[Vela], en_curso: Vela | None, lectura: str, instante: int, lado: str
) -> Pivote | None:
    """El pivote formado mas reciente del lado pedido (ADR-0045), o None si no hay ninguno."""
    if lado not in LADOS:
        raise PivoteError(f"lado {lado!r} no esta en {LADOS}")
    for p in reversed(pivotes_formados(cerradas, en_curso, lectura, instante)):
        if p.lado == lado:
            return p
    return None


def toca(vela: Vela, pivote: Pivote) -> bool:
    """La vela llega al nivel del pivote (`alcanza_nivel`): con la mecha basta para LLEGAR."""
    if pivote.lado == BAJO:
        return int(vela.minima) <= pivote.nivel
    return int(vela.maxima) >= pivote.nivel


def cruza(vela: Vela, pivote: Pivote, criterio: str) -> bool:
    """La vela pasa al otro lado del nivel con el criterio declarado (RN-004,
    `liquidez_m15_criterio_toma`): `cuerpo`, el cierre queda al otro lado; `mecha`, basta con que
    la mecha lo perfore. Estrictamente al otro lado: tocar el nivel no es cruzarlo."""
    if criterio == "cuerpo":
        precio = int(vela.cierre)
    elif criterio == "mecha":
        precio = int(vela.minima) if pivote.lado == BAJO else int(vela.maxima)
    else:
        raise PivoteError(f"criterio de toma {criterio!r} desconocido")
    return precio < pivote.nivel if pivote.lado == BAJO else precio > pivote.nivel


__all__ = [
    "ALTO",
    "BAJO",
    "CIERRE_VELA_CONTRARIA",
    "INICIO_VELA_CONTRARIA",
    "LADOS",
    "LECTURAS",
    "Pivote",
    "PivoteError",
    "color",
    "cruza",
    "pivote_mas_reciente",
    "pivotes_formados",
    "toca",
]
