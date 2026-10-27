"""ADR-0084 por el camino que corre de verdad: `DatosMercado.liquidez_m15` (engine/motor.py) con
el selector `liquidez_m15_mecha_que_vuelve` y el criterio de la toma leidos del registro REAL, y
las primitivas de RN-004 (`alcanza_nivel`, `cruza`) sobre ese nivel. La mecha de la contraria
mueve el nivel (caso i), las mechas de las M1 posteriores lo mueven hasta la toma (caso ii) y la
toma lo congela; con `solo_la_contraria` solo el caso i; con `no_mueve` lo de antes. Un valor
fuera del enum falla al leer el registro, y las series de M1 (la referencia del breaker, el punto
de la orden) no se mueven. Todo sintetico; falla con el codigo de `main` (el nivel se quedaba en
el extremo de la racha)."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.config.registro import Registro, RegistroError, cargar_registro
from botsito.domain.estructura_m1 import COMPRA, referencia_del_breaker, ultimo_punto_de_ruptura
from botsito.domain.pivotes_m15 import (
    ALTO,
    CIERRE_VELA_CONTRARIA,
    CUALQUIER_MECHA,
    NO_MUEVE,
    SOLO_LA_CONTRARIA,
)
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.motor import DatosMercado
from botsito.engine.primitivas import primitivas_escritas
from tests.unit.test_estructura_m1 import TOMA, _serie
from tests.unit.test_pivotes_m15 import FLUJO_ALCISTA, ROJA, ROJA_CON_MECHA, _m15

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "knowledge" / "spec" / "parametros.yaml"
FIN_ROJA = int(ROJA.fin)  # T0 + 60: desde aqui, las M1 posteriores


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(PARAMETROS)


def _m1(k: int, a: int, c: int, alto: int | None = None) -> Vela:
    hi = alto if alto is not None else max(a, c) + 1
    return Vela(MinutoUtc(FIN_ROJA + k), Puntos(a), Puntos(hi), Puntos(min(a, c) - 1), Puntos(c), 1)


# tras la roja (ALTO en 134): una mecha a 137 que vuelve, una M1 que cierra sobre 134 pero no sobre
# 137 con mecha 138, y la que cierra sobre 138 (la toma)
M1_POSTERIORES = [
    _m1(0, 118, 125, alto=137),
    _m1(1, 125, 136, alto=138),
    _m1(2, 136, 141, alto=142),
]


def _datos(
    registro: Registro, m15: list[Vela], m1: list[Vela], mecha: str | None = None
) -> DatosMercado:
    return DatosMercado(
        [],
        m15,
        m1,
        registro.opcion("liquidez_m15_pivote_formado"),
        registro.opcion("liquidez_m15_mecha_que_vuelve") if mecha is None else mecha,
        registro.opcion("liquidez_m15_criterio_toma"),
    )


def _momento(datos: DatosMercado, k: int) -> Momento:
    return Momento(MinutoUtc(FIN_ROJA + k + 1), "07-11", False, datos)  # el cierre de la M1 k


def _nivel(datos: DatosMercado, instante: int) -> int:
    p = datos.liquidez_m15(instante, ALTO)
    assert p is not None
    return p.nivel


def _estado() -> EstadoDia:
    e = EstadoDia()
    e.hechos["sesgo"] = "bajista"  # la liquidez de un sesgo bajista es un ALTO
    return e


def test_el_registro_real_trae_el_selector_como_lectura_del_consultor(registro: Registro) -> None:
    p = registro.parametros["liquidez_m15_mecha_que_vuelve"]
    assert p.valor == CUALQUIER_MECHA and p.estado.value == "DEFAULT_AMBIGUOUS"
    assert p.ambiguedad_id == "A-35"
    assert p.fuente is not None and p.fuente.id == "ev-v15-000553-9d95178a"
    assert registro.opcion("liquidez_m15_pivote_formado") == CIERRE_VELA_CONTRARIA
    assert registro.opcion("liquidez_m15_criterio_toma") == "cuerpo"


def test_por_el_camino_real_las_mechas_mueven_el_nivel_y_la_toma_lo_congela(
    registro: Registro,
) -> None:
    """Con el registro vigente (`cualquier_mecha`): en el cierre de cada M1, `liquidez_m15` da el
    nivel movido por las mechas de hasta esa M1; `alcanza_nivel` lo toca y `cruza` NO lo toma
    hasta la M1 que cierra sobre el nivel MOVIDO. En `main` el nivel era 134 en los tres cierres y
    la segunda M1 (cierre 136) ya era la toma."""
    datos = _datos(registro, [*FLUJO_ALCISTA, ROJA], M1_POSTERIORES)
    niveles = [_nivel(datos, FIN_ROJA + k + 1) for k in range(3)]
    assert niveles == [137, 138, 138]
    prim = primitivas_escritas(registro).predicados
    alcanza, cruza = prim["alcanza_nivel"], prim["cruza"]
    args_c = {"que": "liquidez_m15", "criterio": "liquidez_m15_criterio_toma"}
    e = _estado()
    assert alcanza({"que": "liquidez_m15"}, _momento(datos, 0), e) == Resultado(Tri.SI)
    assert cruza(args_c, _momento(datos, 0), e) == Resultado(Tri.NO)
    assert cruza(args_c, _momento(datos, 1), e) == Resultado(Tri.NO)  # 136 no pasa el 137
    assert cruza(args_c, _momento(datos, 2), e) == Resultado(Tri.SI)  # 141 pasa el 138: la toma
    # la huella del selector en la traza lleva el nivel movido
    assert e.anotaciones["07-11"]["liquidez_m15"].startswith("alto 137 formado_en")
    # y despues de la toma, una mecha mas alta ya no mueve nada: el nivel sigue congelado
    con_otra = _datos(
        registro, [*FLUJO_ALCISTA, ROJA], [*M1_POSTERIORES, _m1(3, 141, 130, alto=150)]
    )
    assert _nivel(con_otra, FIN_ROJA + 4) == 138


@pytest.mark.parametrize(
    ("mecha", "nivel_contraria", "nivel_tras_m1"),
    [(NO_MUEVE, 134, 134), (SOLO_LA_CONTRARIA, 140, 140), (CUALQUIER_MECHA, 140, 141)],
)
def test_cada_opcion_del_selector_por_el_camino_real(
    registro: Registro, mecha: str, nivel_contraria: int, nivel_tras_m1: int
) -> None:
    """La contraria con mecha 140 (caso i) y despues una M1 con mecha 141 que vuelve (caso ii):
    `no_mueve` deja 134; `solo_la_contraria` 140 y la M1 no lo mueve; `cualquier_mecha` 141."""
    datos = _datos(registro, [*FLUJO_ALCISTA, ROJA_CON_MECHA], [_m1(0, 118, 125, alto=141)], mecha)
    assert _nivel(datos, FIN_ROJA) == nivel_contraria
    assert _nivel(datos, FIN_ROJA + 1) == nivel_tras_m1


def test_un_valor_fuera_del_enum_falla_al_leer_el_registro(tmp_path: Path) -> None:
    texto = PARAMETROS.read_text(encoding="utf-8")
    linea = "    valor: cualquier_mecha\n"
    assert texto.count(linea) == 1
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto.replace(linea, "    valor: a_ojo\n"), encoding="utf-8")
    with pytest.raises(RegistroError):
        cargar_registro(ruta)
    with pytest.raises(ValueError, match="mecha que vuelve"):
        DatosMercado([], [], [], CIERRE_VELA_CONTRARIA, "a_ojo", "cuerpo")


def test_las_series_de_m1_no_se_mueven() -> None:
    """El otro marco: la contraria de M1 con una mecha que pasa el maximo de la racha (1130 sobre
    1120) deja la referencia del breaker y el punto de la orden en 1120, como antes de ADR-0084:
    `estructura_m1.py` no pide ninguna mecha."""
    m1 = _serie(
        [
            (1000, 1050),
            (1050, 1100),
            (1100, 1119, None, 1120),
            (1119, 1060, None, 1130),
            (1060, 990),
        ]
    )
    assert referencia_del_breaker(m1, TOMA + 1, COMPRA) == 1120
    punto = ultimo_punto_de_ruptura(m1, COMPRA, TOMA + 1)
    assert punto is not None and punto.nivel == 1120
    # y la M15 sin ninguna M1 posterior tampoco cambia con el selector por defecto
    datos = _datos(cargar_registro(PARAMETROS), [*FLUJO_ALCISTA, _m15(3, 130, 118)], [], NO_MUEVE)
    assert _nivel(datos, FIN_ROJA) == 134
