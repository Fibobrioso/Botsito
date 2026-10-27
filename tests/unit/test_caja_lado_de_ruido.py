"""A-50, `caja_lado_de_ruido` (sesion 5, S-12b; trabajo/activar-sesion-05-motor, punto 4): que
parte de la caja de la orden stop mira RN-005 frente al nivel tomado. Por el camino real
(`se_desarrolla_en_el_lado_de_ruido` de engine/zonas.py con el registro y la zona del punto), en
compra y en venta y con los dos valores: la caja con el 0 del lado de ruido y el 1 no (con
`caja_entera` se opera; con `solo_el_0`, no), la caja entera del lado de ruido (no se opera con
ninguno), el 0 justo en la linea (indiferente con los dos); un valor fuera del enum falla al leer el
registro. Todo sintetico; con el codigo de main la caja a caballo era ruido."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.config.registro import Registro, RegistroError, cargar_registro
from botsito.domain.pivotes_m15 import Pivote
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import zonas
from botsito.engine.interprete import EstadoDia, Resultado, Tri
from tests.unit import test_orden_stop_pivote as tosp

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "knowledge" / "spec" / "parametros.yaml"
NIVEL = 1010  # el nivel de M15 tomado, en los dos lados
ARGS = {"que": "liquidez_m15", "sentido": "S", "caja": "caja_lado_de_ruido"}
# compra (el ruido queda POR ENCIMA del nivel): la caja a caballo (el 0, el ALTO en 1031, por
# encima; el 1, el minimo desde la vela que marca el punto, 1004, por debajo) y la caja entera
# por encima (el 1 en 1021)
A_CABALLO = [1000, 1005, 1015, 1020, 1030, 1005, 1008]
ENTERA = [1000, 1005, 1015, 1020, 1030, 1025, 1022]
# y el 0 justo en la linea: el ALTO en 1010 (la verde cierra en 1009, maxima 1010) y el 1 debajo
EN_LA_LINEA = [1000, 1003, 1006, 1009, 1000, 1002]


class _Datos(tosp._Datos):
    def __init__(self, velas: list[Vela], toma: int, lado: str) -> None:
        super().__init__(velas, toma)
        self.lado = lado

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        return Pivote(
            lado, NIVEL, MinutoUtc(tosp.M0), MinutoUtc(tosp.M0 + 1), MinutoUtc(tosp.M0 + 1)
        )


def _espejo(cierres: list[int]) -> list[int]:
    return [2 * NIVEL - c for c in cierres]


def _estado(sesgo: str) -> EstadoDia:
    e = EstadoDia()
    e.hechos.update({"liquidez_tomada": "si", "sesgo": sesgo})
    return e


def _ruido(reg: Registro, cierres: list[int], sesgo: str) -> tuple[Resultado, zonas.Zona]:
    """El veredicto de RN-005 en el ultimo cierre, y la zona del punto que mira."""
    lado = "compra" if sesgo == "alcista" else "venta"
    datos = _Datos(
        tosp._serie(cierres if lado == "compra" else _espejo(cierres)), tosp.M0 + 1, lado
    )
    estado = _estado(sesgo)
    prim = zonas.primitivas_zona(reg, "solo_una_zona_de_control")
    k = len(cierres) - 1
    r = prim["se_desarrolla_en_el_lado_de_ruido"](ARGS, tosp._momento(datos, k), estado)
    z = zonas.zona_del_punto(reg, tosp._momento(datos, k), estado)
    assert isinstance(r, Resultado) and z is not None
    return r, z


@pytest.mark.parametrize("sesgo", ["alcista", "bajista"])
def test_con_caja_entera_la_caja_a_caballo_no_es_ruido_y_con_solo_el_0_si(
    tmp_path: Path, sesgo: str
) -> None:
    """El 0 del lado de ruido y el 1 del lado del trader: con el registro vigente (`caja_entera`)
    RN-005 no prohibe; con `solo_el_0`, lo de antes de la sesion 5 (y de main): prohibe."""
    entera = tosp._registro(tmp_path)
    assert entera.opcion("caja_lado_de_ruido") == "caja_entera"
    r, z = _ruido(entera, A_CABALLO, sesgo)
    if sesgo == "alcista":
        assert z.entrada > NIVEL > z.extremo
    else:
        assert z.entrada < NIVEL < z.extremo
    assert r == Resultado(Tri.NO)
    otra = tmp_path / "solo_el_0"
    otra.mkdir()
    solo = tosp._registro(otra, caja_lado_de_ruido="solo_el_0")
    assert _ruido(solo, A_CABALLO, sesgo)[0] == Resultado(Tri.SI)


@pytest.mark.parametrize("sesgo", ["alcista", "bajista"])
def test_la_caja_entera_del_lado_de_ruido_no_se_opera_con_ninguno(
    tmp_path: Path, sesgo: str
) -> None:
    entera = tosp._registro(tmp_path)
    r, z = _ruido(entera, ENTERA, sesgo)
    if sesgo == "alcista":
        assert z.entrada > NIVEL and z.extremo > NIVEL
    else:
        assert z.entrada < NIVEL and z.extremo < NIVEL
    assert r == Resultado(Tri.SI)
    otra = tmp_path / "solo_el_0"
    otra.mkdir()
    assert _ruido(tosp._registro(otra, caja_lado_de_ruido="solo_el_0"), ENTERA, sesgo)[0] == (
        Resultado(Tri.SI)
    )


@pytest.mark.parametrize("sesgo", ["alcista", "bajista"])
def test_el_0_justo_en_la_linea_es_indiferente_con_los_dos(tmp_path: Path, sesgo: str) -> None:
    """«si el 0 queda justo en la linea … eso es indiferente» (ev-v15-010451-5b123278): el 0 EN el
    nivel no es ruido, con ninguna de las dos lecturas (estrictamente al otro lado)."""
    entera = tosp._registro(tmp_path)
    r, z = _ruido(entera, EN_LA_LINEA, sesgo)
    assert z.entrada == NIVEL
    assert r == Resultado(Tri.NO)
    otra = tmp_path / "solo_el_0"
    otra.mkdir()
    assert _ruido(tosp._registro(otra, caja_lado_de_ruido="solo_el_0"), EN_LA_LINEA, sesgo)[0] == (
        Resultado(Tri.NO)
    )


def test_el_registro_real_y_un_valor_fuera_del_enum(tmp_path: Path) -> None:
    reg = cargar_registro(PARAMETROS)
    p = reg.parametros["caja_lado_de_ruido"]
    assert p.valor == "caja_entera" and p.estado.value == "DEFAULT_AMBIGUOUS"
    assert p.ambiguedad_id == "A-50" and p.categoria == "estrategia"
    assert p.fuente is not None and p.fuente.id == "ev-v15-010451-5b123278"
    texto = PARAMETROS.read_text(encoding="utf-8")
    linea = "    valor: caja_entera\n"
    assert texto.count(linea) == 1
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto.replace(linea, "    valor: a_ojo\n"), encoding="utf-8")
    with pytest.raises(RegistroError):
        cargar_registro(ruta)
