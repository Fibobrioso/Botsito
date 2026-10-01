"""La geometria de la zona de entrada en M1 (RN-008, RN-009, RN-011): el breaker, el bloque de
origen y las zonas de control del retroceso. Puro: velas dentro, esquema fuera.

Lo que esta documentado y de donde sale cada cosa (`docs/validation/PREPARACION-A21.md` §1):

- **La temporalidad es M1**: el flujo de ordenes que da la entrada se desarrolla en M1
  (`ev-v3-001630-a911f624`, `ev-v2-001329-e766675a`, `ev-v3-010431-20bddf07`).
- **El breaker (BOS) marca el bloque de origen** y el trader no usa el CHoCH
  (`ev-v3-011653-38c712f3`); la ruptura vale con mecha (`breaker_m1_criterio_ruptura`, CONFIRMED;
  `ev-v4-010415-6d8b1d02`, `ev-v4-005910-d24c0345`). Aqui el breaker es la primera M1, cerrada
  despues de tomar la liquidez de M15, que pasa el ultimo pivote de M1 contrario al sentido de la
  entrada: en una compra, el ultimo ALTO; en una venta, el ultimo BAJO.
- **El bloque de origen lo marca la vela contraria**: en M1, la vela contraria al flujo marca el
  punto (`ev-v3-010818-010bd2b3`, `ev-v3-011540-5425b533`). Aqui el bloque es la ULTIMA vela del
  color contrario a la entrada antes del impulso que rompe. Que varias velas formen «un order block
  mayor» y se mapeen como una (RN-007, `mapeo_dos_velas = order_block_mayor`,
  `ev-v3-010648-0039e34d`) no tiene criterio escrito: `agrupar_estructura` sigue NO_IMPLEMENTADA y
  la agrupacion es un candidato a ambiguedad, no una lectura.
- **Los extremos son las mechas**: el mapeo considera siempre las mechas
  (`ev-v3-010500-f3a1bebc`, `ev-v3-001827-72bc1e81`) y la orden va «en la mecha»
  (`ev-v4-010605-a11249c0`). La entrada es el borde del bloque mas cercano al precio y el extremo
  de la caja el borde opuesto: el stop sale «del punto mas bajo donde se genera la vela contraria»
  (`ev-v1-001454-69cebe62`) y el lote «desde el punto mas alto hasta el punto mas bajo»
  (`ev-v3-004353-b7661782`). En que punto exacto de la mecha va la orden es A-36.
- **Los dos esquemas** (`ev-v4-000243-5f8875ce`, `ev-v3-004201-bfeb3734`, `ev-v3-004230-ed95f336`):
  el primero rompe directamente, sin retroceso; el segundo hace un pequeno retroceso que deja una
  zona de control y despues rompe. Aqui una zona de control del retroceso es un pivote de M1 en el
  sentido de la entrada -un BAJO en una compra- formado entre la toma de la liquidez y el breaker;
  cero zonas es el primer esquema, una el segundo, y mas de `zonas_control_max_por_esquema`
  invalida (RN-009, `fb-2026-09-09-sesion-01-1b2203b0`, v3 #624).
- **Que hace limpia una zona es A-21, y NADIE lo define** (0 de 14 pasajes,
  `A24-A21-A26-A34-CLASIFICACION.md`). Las dos condiciones de validez que el corpus si enuncia
  son las dos lecturas del selector `zona_control_limpia`: `solo_una_zona_de_control` -la unica
  condicion es la de RN-009 (v3 #624-#627)- y `sin_mecha_mas_alla_del_extremo` -una mecha que
  rompe el nivel deja la entrada sin validez (`ev-v4-005310-ce69f8c6`, v4 0:53:10; que nivel era
  es A-32)-, leida aqui como que ninguna mecha entre el bloque y el breaker puede pasar el extremo
  lejano del bloque.

Sin reloj, sin IO, sin registro (ADR-0002): los criterios y topes llegan como argumentos.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from botsito.domain.pivotes_m15 import (
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    color,
    pivotes_formados,
)
from botsito.domain.velas import MinutoUtc, Vela

COMPRA = "compra"
VENTA = "venta"
LADOS = (COMPRA, VENTA)
MECHA = "mecha"
CUERPO = "cuerpo"
PRIMER_ESQUEMA = "primer_esquema"
SEGUNDO_ESQUEMA = "segundo_esquema"
SOLO_UNA_ZONA_DE_CONTROL = "solo_una_zona_de_control"
SIN_MECHA_MAS_ALLA_DEL_EXTREMO = "sin_mecha_mas_alla_del_extremo"
LECTURAS_LIMPIA = (SOLO_UNA_ZONA_DE_CONTROL, SIN_MECHA_MAS_ALLA_DEL_EXTREMO)
# El bloque de la caja de una orden stop (A-48, `caja_bloque`; ADR-0064): las reglas R6, R4 y R1
# de docs/validation/CAJA-77.md, que dan el 1 de la caja; el 0 es siempre el punto de ruptura.
BLOQUE_R6 = "r6"
BLOQUE_R4 = "r4"
BLOQUE_R1 = "r1"
BLOQUES_CAJA = (BLOQUE_R6, BLOQUE_R4, BLOQUE_R1)


class EstructuraError(ValueError):
    """Argumentos que el modelo no admite: nunca se adivina."""


@dataclass(frozen=True)
class Esquema:
    """Lo que la geometria de M1 da al motor cuando se completa un esquema de entrada."""

    cual: str  # primer_esquema | segundo_esquema
    lado: str  # compra | venta
    entrada: int  # el borde del bloque mas cercano al precio, en puntos
    extremo: int  # el borde opuesto: el nivel 1 de la caja
    bloque_inicio: MinutoUtc  # la primera vela del bloque de origen
    bloque_fin: MinutoUtc  # el fin de la ultima
    breaker_fin: MinutoUtc  # el cierre de la M1 que rompe: desde ahi existe la zona
    referencia: int  # el pivote de M1 que el breaker paso
    zonas_de_control: int  # pivotes del retroceso entre la toma y el breaker

    @property
    def caja(self) -> int:
        return abs(self.entrada - self.extremo)


def _signo(lado: str) -> int:
    if lado not in LADOS:
        raise EstructuraError(f"lado {lado!r} no esta en {LADOS}")
    return 1 if lado == COMPRA else -1


def _pasa(vela: Vela, nivel: int, lado: str, criterio: str) -> bool:
    """La vela pasa el nivel en el sentido de la entrada con el criterio del breaker."""
    if criterio == MECHA:
        precio = int(vela.maxima) if lado == COMPRA else int(vela.minima)
    elif criterio == CUERPO:
        precio = int(vela.cierre)
    else:
        raise EstructuraError(f"criterio de ruptura {criterio!r} desconocido")
    return precio > nivel if lado == COMPRA else precio < nivel


def referencia_del_breaker(m1: Sequence[Vela], hasta: int, lado: str) -> int | None:
    """El ultimo pivote de M1 contrario al sentido de la entrada formado con las velas `m1[:hasta]`
    (la toma de la liquidez incluida): un ALTO para una compra, un BAJO para una venta. Es el nivel
    que el breaker tiene que pasar."""
    contrario = ALTO if lado == COMPRA else BAJO
    if hasta <= 0:
        return None
    instante = int(m1[hasta - 1].fin)
    for p in reversed(pivotes_formados(m1, None, CIERRE_VELA_CONTRARIA, instante, hasta)):
        if p.lado == contrario:
            return p.nivel
    return None


def bloque_de_origen(m1: Sequence[Vela], idx_breaker: int, lado: str) -> tuple[int, int] | None:
    """Los indices [desde, hasta) del bloque de origen: la ULTIMA vela contraria a la entrada antes
    del impulso que rompe (`ev-v3-010818-010bd2b3`); None si no la hay."""
    signo = _signo(lado)
    i = idx_breaker
    # el impulso: velas del color de la entrada (o sin cuerpo) hasta llegar a la primera contraria
    while i >= 0 and color(m1[i]) != -signo:
        i -= 1
    if i < 0:
        return None
    return i, i + 1


def zonas_de_control(m1: Sequence[Vela], desde: int, hasta: int, lado: str) -> int:
    """Cuantas zonas de control deja el retroceso entre la toma (`desde`, exclusivo) y el breaker
    (`hasta`, inclusivo): los pivotes de M1 en el sentido de la entrada -BAJOS en una compra- que se
    forman DESPUES de la primera vela del impulso. El extremo del barrido (el bajo que la toma
    deja) no es una zona de control del retroceso: es la propia toma."""
    signo = _signo(lado)
    sentido = BAJO if lado == COMPRA else ALTO
    if hasta <= desde:
        return 0
    primer_impulso = next((k for k in range(desde + 1, hasta + 1) if color(m1[k]) == signo), None)
    if primer_impulso is None:
        return 0
    instante = int(m1[hasta].fin)
    n = 0
    for p in pivotes_formados(m1, None, CIERRE_VELA_CONTRARIA, instante, hasta + 1):
        if p.lado == sentido and int(p.contraria_inicio) > int(m1[primer_impulso].inicio):
            n += 1
    return n


def mecha_mas_alla_del_extremo(
    m1: Sequence[Vela], desde: int, hasta: int, extremo: int, lado: str
) -> bool:
    """Alguna mecha de `m1[desde:hasta]` pasa el extremo lejano del bloque (la lectura
    `sin_mecha_mas_alla_del_extremo` de A-21 la deja sin validez)."""
    for v in m1[desde:hasta]:
        if lado == COMPRA and int(v.minima) < extremo:
            return True
        if lado == VENTA and int(v.maxima) > extremo:
            return True
    return False


@dataclass(frozen=True)
class PuntoDeRuptura:
    """Un posible punto de breaker (ADR-0056 §7, ADR-0064): el ultimo pivote de M1 contrario al
    sentido de la entrada -un BAJO en una venta, un ALTO en una compra- formado con las velas dadas.
    `marca` es el indice de la vela que marca su nivel, desde la que R6 traza la caja."""

    nivel: int
    contraria_inicio: MinutoUtc  # la vela contraria que lo forma: con el nivel, lo identifica
    marca: int

    @property
    def clave(self) -> tuple[int, int]:
        return self.nivel, int(self.contraria_inicio)


def ultimo_punto_de_ruptura(
    m1: Sequence[Vela], lado: str, hasta: int | None = None
) -> PuntoDeRuptura | None:
    """El ultimo pivote de M1 contrario a la entrada formado con `m1[:hasta]` (todas si `hasta` es
    None), con `CIERRE_VELA_CONTRARIA`: la funcion de R5 de `scripts/bloque_de_la_caja.py`. Con
    `hasta` en la vela de la toma, es el pivote de `referencia_del_breaker`."""
    signo = _signo(lado)
    n = len(m1) if hasta is None else hasta
    if n <= 0:
        return None
    buscado = ALTO if signo == 1 else BAJO
    for p in reversed(pivotes_formados(m1, None, CIERRE_VELA_CONTRARIA, int(m1[n - 1].fin), n)):
        if p.lado != buscado:
            continue
        ic = next((i for i in range(n) if int(m1[i].inicio) == int(p.contraria_inicio)), None)
        if ic is None:
            return None

        def extremo(v: Vela) -> int:
            return int(v.maxima) if signo == 1 else int(v.minima)

        marca = next((i for i in range(ic, -1, -1) if extremo(m1[i]) == p.nivel), ic)
        return PuntoDeRuptura(p.nivel, p.contraria_inicio, marca)
    return None


def extremo_de_la_caja(
    m1: Sequence[Vela], lado: str, punto: PuntoDeRuptura, bloque: str
) -> int | None:
    """El 1 de la caja de una orden stop en `punto`, con las M1 cerradas `m1` (ADR-0064): R6, el
    extremo opuesto de las velas desde la que marca el punto hasta la ultima; R4, el del tramo de
    velas contrarias consecutivas que acaba en la ultima contraria; R1, el de esa ultima contraria.
    El extremo opuesto es la maxima en una venta y la minima en una compra. None si el bloque no
    tiene velas o si su extremo no queda del lado del stop: una caja sin altura no da stop ni
    lote."""
    signo = _signo(lado)
    if bloque not in BLOQUES_CAJA:
        raise EstructuraError(f"bloque {bloque!r} no esta en {BLOQUES_CAJA}")
    if bloque == BLOQUE_R6:
        velas = list(m1[punto.marca :])
    else:
        k = next((i for i in range(len(m1) - 1, -1, -1) if color(m1[i]) == -signo), None)
        if k is None:
            return None
        j = k
        if bloque == BLOQUE_R4:
            while j - 1 >= 0 and color(m1[j - 1]) == -signo:
                j -= 1
        velas = list(m1[j : k + 1])
    if not velas:
        return None
    uno = min(int(v.minima) for v in velas) if signo == 1 else max(int(v.maxima) for v in velas)
    del_lado_del_stop = uno < punto.nivel if signo == 1 else uno > punto.nivel
    return uno if del_lado_del_stop else None


def zona_posterior_completada(m1: Sequence[Vela], lado: str, criterio: str) -> int | None:
    """El indice de la PRIMERA M1 que completa una zona de control posterior a la entrada
    (RN-014), o None si todavia no. `m1` son las M1 cerradas desde la entrada, en orden.

    Tras la entrada, una vela CONTRARIA que sigue a una racha a favor deja el punto extremo
    -el punto alto en una compra- y abre el retroceso, que es la zona de control; la zona se
    completa cuando una M1 posterior PASA ese punto con `criterio` («rompe el punto alto
    anterior con mecha», fb-2026-09-09-sesion-01-a456bc3f). Manda el ULTIMO punto formado, y
    la mecha de la propia vela contraria no cuenta: el punto existe desde su cierre, como en
    `pivotes_m15`. Sin mirar al futuro: solo usa las velas dadas."""
    return _recorrer_zona_posterior(m1, lado, criterio)[0]


def nivel_de_activacion_posterior(m1: Sequence[Vela], lado: str, criterio: str) -> int | None:
    """El nivel que la PROXIMA M1 tendria que pasar para completar la zona de control posterior
    (RN-014), con las M1 cerradas `m1` desde la entrada; None si todavia no hay zona o si ya se
    completo (rama feature/be-al-tick, ADR-0065). Es el MISMO punto que mira
    `zona_posterior_completada`, del mismo recorrido: el break even al tick cambia el instante,
    no el nivel. Sin mirar al futuro."""
    k, extremo = _recorrer_zona_posterior(m1, lado, criterio)
    return extremo if k is None else None


def _recorrer_zona_posterior(
    m1: Sequence[Vela], lado: str, criterio: str
) -> tuple[int | None, int | None]:
    """(indice de la M1 que completa la zona o None, ultimo punto extremo formado o None)."""
    signo = _signo(lado)
    if criterio not in (MECHA, CUERPO):
        raise EstructuraError(f"criterio de ruptura {criterio!r} desconocido")
    extremo: int | None = None
    racha: list[Vela] = []  # las velas a favor consecutivas que preceden a la que se mira
    for k, v in enumerate(m1):
        if extremo is not None and _pasa(v, extremo, lado, criterio):
            return k, extremo
        c = color(v)
        if c == signo:
            racha.append(v)
            continue
        if c == -signo and racha:
            extremo = (
                max(int(x.maxima) for x in racha)
                if lado == COMPRA
                else min(int(x.minima) for x in racha)
            )
        racha = []
    return None, extremo


def detectar_esquema(
    m1: Sequence[Vela],
    idx_toma: int,
    lado: str,
    criterio: str,
    tope_zonas: int,
    limpia: str,
) -> Esquema | None:
    """El primer esquema de entrada que se completa despues de la toma de la liquidez.

    `m1` son las M1 cerradas hasta el instante que se evalua, en orden; `idx_toma` es la M1 que
    tomo la liquidez de M15 (a partir de ahi se busca el breaker). Devuelve el esquema en
    cuanto una M1 cerrada pasa la referencia, o None si todavia no, si el retroceso dejo mas
    zonas de las admitidas, o si la zona no pasa la lectura de «limpia». Sin mirar al futuro: solo
    usa velas anteriores o iguales a la que rompe."""
    if limpia not in LECTURAS_LIMPIA:
        raise EstructuraError(f"lectura de A-21 {limpia!r} no esta en {LECTURAS_LIMPIA}")
    _signo(lado)
    if criterio not in (MECHA, CUERPO):
        raise EstructuraError(f"criterio de ruptura {criterio!r} desconocido")
    if tope_zonas < 0:
        raise EstructuraError("el tope de zonas de control es un entero no negativo")
    if idx_toma < 0 or idx_toma >= len(m1):
        raise EstructuraError("la toma cae fuera de las velas dadas")
    referencia = referencia_del_breaker(m1, idx_toma + 1, lado)
    if referencia is None:
        return None
    for i in range(idx_toma + 1, len(m1)):
        if not _pasa(m1[i], referencia, lado, criterio):
            continue
        n_zonas = zonas_de_control(m1, idx_toma, i, lado)
        if n_zonas > tope_zonas:
            return None
        bloque = bloque_de_origen(m1, i, lado)
        if bloque is None:
            return None
        desde, hasta = bloque
        velas = m1[desde:hasta]
        lo, hi = min(int(v.minima) for v in velas), max(int(v.maxima) for v in velas)
        entrada, extremo = (hi, lo) if lado == COMPRA else (lo, hi)
        if limpia == SIN_MECHA_MAS_ALLA_DEL_EXTREMO and mecha_mas_alla_del_extremo(
            m1, hasta, i + 1, extremo, lado
        ):
            return None
        return Esquema(
            PRIMER_ESQUEMA if n_zonas == 0 else SEGUNDO_ESQUEMA,
            lado,
            entrada,
            extremo,
            m1[desde].inicio,
            m1[hasta - 1].fin,
            m1[i].fin,
            referencia,
            n_zonas,
        )
    return None


__all__ = [
    "BLOQUES_CAJA",
    "BLOQUE_R1",
    "BLOQUE_R4",
    "BLOQUE_R6",
    "COMPRA",
    "CUERPO",
    "LADOS",
    "LECTURAS_LIMPIA",
    "MECHA",
    "PRIMER_ESQUEMA",
    "SEGUNDO_ESQUEMA",
    "SIN_MECHA_MAS_ALLA_DEL_EXTREMO",
    "SOLO_UNA_ZONA_DE_CONTROL",
    "VENTA",
    "Esquema",
    "EstructuraError",
    "PuntoDeRuptura",
    "bloque_de_origen",
    "detectar_esquema",
    "extremo_de_la_caja",
    "mecha_mas_alla_del_extremo",
    "nivel_de_activacion_posterior",
    "referencia_del_breaker",
    "ultimo_punto_de_ruptura",
    "zona_posterior_completada",
    "zonas_de_control",
]
