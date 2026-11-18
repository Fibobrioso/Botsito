"""El sesgo H4 (RN-003, ADR-0044, ADR-0094): la primera regla del motor. Puro, sobre velas ya
agregadas.

RN-003 DESDE ADR-0094 (sesion 7a, S-1): el sesgo es el del RANGO VIGENTE de H4. Se recorren HACIA
DELANTE las H4 cerradas a la apertura de la sesion -las de fin no posterior a la apertura, por su
hora de fin y no por su marca `completa` (ADR-0044)- con un estado: el rango (su alto, su bajo y la
vela que lo fijo) y el lado.

a) una H4 que no supera ni el alto ni el bajo del rango -con `criterio`; igual es un equal y no
   rompe- no cambia nada: «El rango es la vela verde grande y sigo buscando compras»
   (ev-v18-000249-bb7b1c07);
b) una H4 que supera el alto del rango y cierra verde fija el lado alcista; la que supera el bajo y
   cierra roja, bajista (el lado: ADR-0080). El rango pasa a ser esa vela, su alto y su bajo con el
   mismo criterio: LECTURA DEL CONSULTOR (`sesgo_h4_rango_nuevo`, DEFAULT_AMBIGUOUS, A-58);
c) una H4 que supera los dos extremos: decide el color (ADR-0060) y el rango pasa a ser esa vela;
   sin cuerpo no decide (ADR-0075) y el rango no cambia;
d) una H4 que supera un extremo y cierra del color contrario, o sin cuerpo, no decide (ADR-0080,
   D1 y D3) y el rango NO cambia: LECTURA DEL CONSULTOR (A-58), apoyada en ev-v11-000038-fef9789d;
e) el arranque: el rango inicial es la H4 situada `tope` velas antes de la ultima cerrada, sin lado
   (con menos velas, la primera que haya); si al llegar a la apertura ninguna vela decidio,
   INSUFICIENTE. Decision del proyecto, como el tope (ADR-0044); ADR-0094 mide cuanto depende el
   resultado de cuantas velas hay cargadas.

Con INSUFICIENTE no se opera (RN-033). AMBIGUO sigue declarado porque la forma de RN-033, los
scripts de diagnostico y el visor lo nombran, pero ninguna vela lo produce desde ADR-0075. Las
cifras no viven aqui (ADR-0002): el tope, el criterio y la lectura del rango nuevo los pasa quien
llama, leidos del registro. La rejilla H4 la construye `data.agregacion`; el dominio no sabe de
husos.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum

from botsito.domain.velas import MinutoUtc, Vela

# Las opciones de `sesgo_h4_criterio_ruptura` (parametros.yaml): que extremos de la vela cuentan.
MECHA, CUERPO = "mecha", "cuerpo"
# La opcion de `sesgo_h4_rango_nuevo` que el motor sabe hacer (b y d de arriba, ADR-0094).
VELA_QUE_ROMPE = "vela_que_rompe_con_su_color"
RANGOS_NUEVOS = (VELA_QUE_ROMPE,)
# Por que no decidio una H4 que rompio el rango, en `ResultadoSesgo.h4_saltadas` (SOLO REGISTRO):
# rompio un extremo y cerro del color contrario (ADR-0080, D1); rompio un extremo y cerro sin
# cuerpo (D3); rompio los dos y cerro sin cuerpo (ADR-0075).
SALTADA_COLOR_CONTRARIO = "color_contrario"
SALTADA_NEUTRA_SIMPLE = "neutra_simple"
SALTADA_NEUTRA_DOBLE = "neutra_doble"


class SesgoError(ValueError):
    """Argumentos que el sesgo no admite."""


class Sesgo(Enum):
    ALCISTA = "alcista"
    BAJISTA = "bajista"
    # Declarado y SIN PRODUCTOR desde ADR-0075. Se queda por la forma de RN-033 (`vale: ambiguo`),
    # los scripts y el visor; retirarlo es deuda.
    AMBIGUO = "ambiguo"
    INSUFICIENTE = "insuficiente"


@dataclass(frozen=True, slots=True)
class ResultadoSesgo:
    sesgo: Sesgo
    # Cuanto supero la vela que fija el lado el extremo del rango que rompio, en puntos: con doble
    # ruptura decidida por el color, la del lado del color. None si ninguna fijo lado.
    ruptura_puntos: int | None
    # Cuantas H4 se compararon con el rango en el recorrido (sin la del arranque).
    velas_miradas: int
    # La vela que fija el lado rompio LOS DOS extremos del rango y el lado lo dio su color.
    doble_ruptura: bool = False
    # Las H4 que rompieron el rango DESPUES de la que lo fijo (o desde el arranque, si ninguna lo
    # fijo) sin decidir, por que no decidieron; el rango no cambio con ellas (d y c sin cuerpo):
    saltadas_color_contrario: int = 0  # rompio UN extremo y cerro del color contrario (D1)
    saltadas_neutras_simples: int = 0  # rompio UN extremo y cerro sin cuerpo (D3)
    saltadas_neutras_dobles: int = 0  # rompio LOS DOS extremos y cerro sin cuerpo (ADR-0075)
    # SOLO REGISTRO: el inicio de la H4 que fija el lado (None si ninguna lo fija) y, por cada
    # saltada, de la mas reciente a la mas antigua, su inicio y su motivo (`SALTADA_*`).
    vela_que_fija: MinutoUtc | None = None
    h4_saltadas: tuple[tuple[MinutoUtc, str], ...] = ()
    # SOLO REGISTRO (ADR-0094): el rango vigente a la apertura -su alto y su bajo con `criterio`, y
    # el inicio de la H4 que lo fijo-. Con lado, esa H4 es `vela_que_fija`; sin lado, la del
    # arranque. None si no hay ninguna H4 cerrada. Nada los lee para decidir.
    rango_alto: int | None = None
    rango_bajo: int | None = None
    rango_vela: MinutoUtc | None = None


def _extremos(vela: Vela, criterio: str) -> tuple[int, int]:
    if criterio == MECHA:
        return vela.maxima, vela.minima
    if criterio == CUERPO:
        return max(vela.abierta, vela.cierre), min(vela.abierta, vela.cierre)
    raise SesgoError(f"criterio de ruptura {criterio!r} fuera de ({MECHA!r}, {CUERPO!r})")


def sesgo_h4(
    velas_h4: Sequence[Vela],
    apertura_sesion: MinutoUtc,
    tope: int,
    criterio: str,
    rango_nuevo: str = VELA_QUE_ROMPE,
) -> ResultadoSesgo:
    """El sesgo al abrir la sesion que empieza en `apertura_sesion` (minuto UTC)."""
    if tope <= 0:
        raise SesgoError("el tope de velas hacia atras es un entero positivo")
    if rango_nuevo not in RANGOS_NUEVOS:
        raise SesgoError(f"rango nuevo {rango_nuevo!r} fuera de {RANGOS_NUEVOS}")
    if criterio not in (MECHA, CUERPO):
        raise SesgoError(f"criterio de ruptura {criterio!r} fuera de ({MECHA!r}, {CUERPO!r})")
    cerradas = sorted((v for v in velas_h4 if v.fin <= apertura_sesion), key=lambda v: v.inicio)
    if not cerradas:
        return ResultadoSesgo(Sesgo.INSUFICIENTE, None, 0)
    inicio = max(0, len(cerradas) - 1 - tope)
    rango = cerradas[inicio]
    alto, bajo = _extremos(rango, criterio)
    sesgo, puntos, doble, fija = Sesgo.INSUFICIENTE, None, False, None
    saltadas = [0, 0, 0]  # color contrario (D1), neutra simple (D3), neutra doble (ADR-0075)
    registro: list[tuple[MinutoUtc, str]] = []
    miradas = 0
    for vela in cerradas[inicio + 1 :]:
        miradas += 1
        v_alto, v_bajo = _extremos(vela, criterio)
        arriba, abajo = v_alto - alto, bajo - v_bajo
        # El color es el del cuerpo, cierre contra apertura, sea cual sea el criterio de ruptura.
        verde, roja = vela.cierre > vela.abierta, vela.cierre < vela.abierta
        decide: tuple[Sesgo, int, bool] | None = None
        motivo: str | None = None
        if arriba > 0 and abajo > 0:
            # c) doble ruptura del rango: «importa el color de la vela» (ADR-0060 §1)
            if verde:
                decide = (Sesgo.ALCISTA, arriba, True)
            elif roja:
                decide = (Sesgo.BAJISTA, abajo, True)
            else:
                motivo = SALTADA_NEUTRA_DOBLE  # sin cuerpo no decide (ADR-0075)
        elif arriba > 0 or abajo > 0:
            # b) y d): decide solo si cierra del color de su ruptura (ADR-0080)
            if arriba > 0 and verde:
                decide = (Sesgo.ALCISTA, arriba, False)
            elif abajo > 0 and roja:
                decide = (Sesgo.BAJISTA, abajo, False)
            else:
                motivo = SALTADA_COLOR_CONTRARIO if (verde or roja) else SALTADA_NEUTRA_SIMPLE
        # a) dentro del rango: nada cambia
        if decide is not None:
            sesgo, puntos, doble = decide
            fija = vela.inicio
            rango = vela  # b) y c): el rango pasa a ser esa vela (A-58, lectura del consultor)
            alto, bajo = v_alto, v_bajo
            saltadas = [0, 0, 0]
            registro = []
        elif motivo is not None:
            # d) y c) sin cuerpo: no decide y el rango NO cambia (A-58, lectura del consultor)
            saltadas[
                {SALTADA_COLOR_CONTRARIO: 0, SALTADA_NEUTRA_SIMPLE: 1, SALTADA_NEUTRA_DOBLE: 2}[
                    motivo
                ]
            ] += 1
            registro.insert(0, (vela.inicio, motivo))
    return ResultadoSesgo(
        sesgo, puntos, miradas, doble, saltadas[0], saltadas[1], saltadas[2], fija,
        tuple(registro), alto, bajo, rango.inicio,
    )  # fmt: skip


__all__ = [
    "CUERPO",
    "MECHA",
    "RANGOS_NUEVOS",
    "SALTADA_COLOR_CONTRARIO",
    "SALTADA_NEUTRA_DOBLE",
    "SALTADA_NEUTRA_SIMPLE",
    "VELA_QUE_ROMPE",
    "ResultadoSesgo",
    "Sesgo",
    "SesgoError",
    "sesgo_h4",
]
