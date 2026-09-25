"""Los huecos del arnes (ADR-0049) sobre H4 SINTETICAS y la spec real.

H1: una sesion ambigua fija `sesgo` a `ambiguo` y RN-033 prohibe; una segunda sesion ambigua no
hereda el sesgo de la primera, ni una no ambigua la prohibicion de una ambigua -el hecho caduca al
abrir-; insuficiente prohibe; y, cuando `data/` esta en la maquina, la forma y la primitiva
coinciden en todas las sesiones de construccion. Mas las guardias nuevas: `vale`, `caduca`, los
`valores` de un hecho como tokens y `sentido` como ligadura. Ninguna fecha real: el dia sintetico
es de 2030.
"""

from __future__ import annotations

import copy
import dataclasses
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.dataset import DatasetError, buscar_manifiesto
from botsito.data.velas import a_minuto
from botsito.domain.sesgo import sesgo_h4
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine.interprete import (
    EstadoDia,
    Interprete,
    Momento,
    Primitivas,
    Tri,
    reglas_ejecutables,
)
from botsito.engine.motor import DatosMercado, DiaDeMercado, MotorSpec, Sesion, TrazaSesion
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import (
    FICHERO_SPEC,
    Regla,
    _nodos_hecho,
    cargar_reglas,
    cargar_vocabulario,
    comprobar_forma,
)

RAIZ = Path(__file__).resolve().parents[2]
SPEC = RAIZ / FICHERO_SPEC
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
# Martes de enero de 2030: Madrid es UTC+1, asi que las sesiones abren a las 06:00 y a las 10:00
# UTC, y la rejilla H4 (17:00 Nueva York) abre a las 22:00 UTC: velas 22-02, 02-06, 06-10...
DIA = date(2030, 1, 15)
APERTURA = {
    "07-11": datetime(2030, 1, 15, 6, tzinfo=UTC),
    "11-15": datetime(2030, 1, 15, 10, tzinfo=UTC),
}
PROHIBE_RN033 = frozenset({"buscar_entradas", "abrir_operacion"})
SIN_LADO = ("ambiguo", "insuficiente")


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def motor(registro: Registro) -> MotorSpec:
    reglas = reglas_ejecutables(cargar_reglas(SPEC))
    return MotorSpec(Interprete(cargar_vocabulario(SPEC), primitivas_escritas(registro)), reglas)


@pytest.fixture(scope="module")
def spec_real(
    registro: Registro,
) -> tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]]:
    tipos = {n: str(getattr(p.tipo, "value", p.tipo)) for n, p in registro.parametros.items()}
    return cargar_reglas(SPEC), cargar_vocabulario(SPEC), set(registro.nombres()), tipos


# ------------------------------------------------------------------------------- velas H4


def _h4(inicio: datetime, maxima: int, minima: int) -> Vela:
    return Vela(
        a_minuto(inicio),
        Puntos(minima + 20),
        Puntos(maxima),
        Puntos(minima),
        Puntos(maxima - 20),
        1,
        duracion_min=240,
        n_m1=240,
    )


def _velas(*pasos: str) -> list[Vela]:
    """H4 desde las 22:00 UTC de la vispera; cada paso dice que hace la vela respecto a la previa.

    `arriba` rompe solo el maximo, `abajo` solo el minimo, `ambos` los dos y `dentro` ninguno. La
    sesion 07-11 mira el primer paso (02-06 contra 22-02) y la 11-15 el segundo (06-10 contra
    02-06).
    """
    inicio = datetime(2030, 1, 14, 22, tzinfo=UTC)
    maxima, minima = 100_100, 99_900
    velas = [_h4(inicio, maxima, minima)]
    for i, paso in enumerate(pasos, start=1):
        if paso == "arriba":
            maxima, minima = maxima + 50, minima + 10
        elif paso == "abajo":
            maxima, minima = maxima - 10, minima - 50
        elif paso == "ambos":
            maxima, minima = maxima + 50, minima - 50
        elif paso == "dentro":
            maxima, minima = maxima - 10, minima + 10
        else:
            raise ValueError(paso)
        velas.append(_h4(inicio + timedelta(hours=4 * i), maxima, minima))
    return velas


def _dia(velas: list[Vela]) -> DiaDeMercado:
    return DiaDeMercado(DIA, HUSO, SESIONES, DatosMercado(velas))


def _apertura(sesion: str, velas: list[Vela]) -> Momento:
    return Momento(MinutoUtc(a_minuto(APERTURA[sesion])), sesion, True, DatosMercado(velas))


def _sesgo_de(traza: TrazaSesion) -> list[str]:
    return [v for _, r, h, v in traza.fijados if h == "sesgo" and r == "RN-003"]


# ------------------------------------------------------------------------------------- H1


def test_una_sesion_ambigua_fija_sesgo_ambiguo_y_rn033_prohibe(motor: MotorSpec) -> None:
    velas = _velas("ambos", "arriba")
    estado = EstadoDia()
    ev = motor.interprete.evento(motor.reglas, _apertura("07-11", velas), estado)
    assert ("RN-003", "sesgo", "ambiguo") in ev.fijados
    assert estado.hechos["sesgo"] == "ambiguo"
    assert "RN-033" in ev.disparadas and ev.prohibidos >= PROHIBE_RN033
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["07-11"]) == ["ambiguo"]
    assert "RN-033" in r.sesiones["07-11"].disparadas
    assert r.sesiones["07-11"].anotaciones["sesgo_h4"] == "ambiguo"


def test_una_segunda_sesion_ambigua_no_hereda_el_sesgo_de_la_primera(motor: MotorSpec) -> None:
    velas = _velas("arriba", "ambos")
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["07-11"]) == ["alcista"]
    assert _sesgo_de(r.sesiones["11-15"]) == ["ambiguo"]
    assert "RN-033" not in r.sesiones["07-11"].disparadas
    assert "RN-033" in r.sesiones["11-15"].disparadas
    # Con el sesgo de la primera sesion en pie, la apertura de la segunda lo caduca ANTES de la
    # primera pasada y fija el suyo: el estado acaba en `ambiguo`, no en `alcista`.
    estado = EstadoDia(hechos={"sesgo": "alcista"})
    ev = motor.interprete.evento(motor.reglas, _apertura("11-15", velas), estado)
    assert ev.caducados == ["sesgo"]
    assert estado.hechos["sesgo"] == "ambiguo" and "RN-033" in ev.disparadas


def test_una_sesion_no_ambigua_tras_una_ambigua_no_hereda_la_prohibicion(motor: MotorSpec) -> None:
    """Medido el 2026-09-25 antes de la caducidad: RN-033 disparaba en la apertura de la segunda
    sesion sobre el sesgo de la primera (24 sesiones de 84 en construccion, y solo 15 ambiguas)."""
    velas = _velas("ambos", "arriba")
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["11-15"]) == ["alcista"]
    assert "RN-033" not in r.sesiones["11-15"].disparadas
    estado = EstadoDia(hechos={"sesgo": "ambiguo"})
    ev = motor.interprete.evento(motor.reglas, _apertura("11-15", velas), estado)
    assert ev.caducados == ["sesgo"]
    assert "RN-033" not in ev.disparadas and not (PROHIBE_RN033 & ev.prohibidos)
    assert estado.hechos["sesgo"] == "alcista"


def test_insuficiente_prohibe(motor: MotorSpec) -> None:
    velas = _velas("dentro", "dentro")
    r = motor.correr_dia(_dia(velas))
    for sesion in ("07-11", "11-15"):
        assert _sesgo_de(r.sesiones[sesion]) == ["insuficiente"]
        assert "RN-033" in r.sesiones[sesion].disparadas
    ev = motor.interprete.evento(motor.reglas, _apertura("07-11", velas), EstadoDia())
    assert ev.prohibidos >= PROHIBE_RN033


def test_el_hecho_solo_caduca_en_la_apertura(motor: MotorSpec) -> None:
    velas = _velas("arriba", "arriba")
    estado = EstadoDia(hechos={"sesgo": "bajista"})
    dentro = Momento(
        MinutoUtc(a_minuto(APERTURA["07-11"]) + 5), "07-11", False, DatosMercado(velas)
    )
    ev = motor.interprete.evento(motor.reglas, dentro, estado)
    assert ev.caducados == [] and estado.hechos["sesgo"] == "bajista"
    assert motor.interprete.caducan_al_abrir == ("sesgo",)


def test_vale_en_el_nodo_hecho() -> None:
    vocab: dict[str, dict[str, Any]] = {
        "predicados": {},
        "acciones": {},
        "hechos": {"h": {"origen": "regla", "valores": ["x", "y"]}},
        "acumuladores": {},
        "efectos": {},
        "tokens": {},
    }
    it = Interprete(vocab, Primitivas({}, {}, {}))
    momento = Momento(MinutoUtc(0), "s", False, None)
    estado = EstadoDia(hechos={"h": "x"})
    assert it.evaluar({"hecho": "h", "vale": "x"}, momento, estado, set()).valor is Tri.SI
    assert it.evaluar({"hecho": "h", "vale": "y"}, momento, estado, set()).valor is Tri.NO
    assert it.evaluar({"hecho": "h"}, momento, estado, set()).valor is Tri.SI
    assert it.evaluar({"hecho": "h", "vale": "x"}, momento, EstadoDia(), set()).valor is Tri.NO


def test_la_forma_y_la_primitiva_coinciden_en_todas_las_sesiones_de_construccion(
    registro: Registro, motor: MotorSpec
) -> None:
    """Sobre las velas de `data/` (fuera de git): por la compuerta y leyendo solo velas, que no es
    abrir (ADR-0021 §1). Sin las velas en la maquina se salta, no se finge."""
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.engine import arnes

    criterio = cargar_criterio(RAIZ)
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        carpeta = cli._carpeta_datos(RAIZ)
        for mes in criterio.construccion:
            buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{mes}")
    except (SystemExit, DatasetError) as exc:
        pytest.skip(f"sin las velas de construccion: {exc}")
    if not carpeta.is_dir():
        pytest.skip(f"sin carpeta de datos: {carpeta}")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    try:
        mercado = arnes.dias_de_mercado(
            RAIZ, carpeta, config, registro, dias, registro.texto("huso_operativa")
        )
    except (OSError, DatasetError) as exc:
        pytest.skip(f"sin las velas de construccion: {exc}")
    tope = registro.entero("sesgo_h4_tope_velas")
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    salidas: Counter[str] = Counter()
    for d in dias:
        dm = mercado[d.dia]
        r = motor.correr_dia(dm)
        for s in dm.sesiones:
            local = datetime.fromisoformat(f"{d.dia}T{s.desde}:00").replace(
                tzinfo=ZoneInfo(dm.huso)
            )
            t = MinutoUtc(a_minuto(local))
            esperado = sesgo_h4(
                dm.datos.velas_h4_cerradas(t), t, tope, criterio_ruptura
            ).sesgo.value
            assert _sesgo_de(r.sesiones[s.nombre]) == [esperado], (d.dia, s.nombre)
            assert ("RN-033" in r.sesiones[s.nombre].disparadas) == (esperado in SIN_LADO), (
                d.dia,
                s.nombre,
            )
            salidas[esperado] += 1
    assert sum(salidas.values()) == 2 * len(dias)
    assert salidas["alcista"] + salidas["bajista"] > 0, "sin velas de verdad no se compara nada"


# ------------------------------------------------------------------------- las guardias


def _fallos(
    spec: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> list[str]:
    reglas, voc, parametros, tipos = spec
    return comprobar_forma(reglas, voc, parametros, tipos=tipos)


def _con_forma(reglas: list[Regla], rid: str, forma: dict[str, Any]) -> list[Regla]:
    return [dataclasses.replace(r, forma=forma) if r.id == rid else r for r in reglas]


def _forma_de(reglas: list[Regla], rid: str) -> dict[str, Any]:
    forma = next(r for r in reglas if r.id == rid).forma
    assert isinstance(forma, dict), rid
    return copy.deepcopy(forma)


def test_la_spec_real_pasa_y_rn033_pregunta_por_sesgo_con_vale(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, _, _ = spec_real
    assert _fallos(spec_real) == []
    rn033 = next(r for r in reglas if r.id == "RN-033")
    assert rn033.clase == "gate" and rn033.vigente and isinstance(rn033.forma, dict)
    assert {n["vale"] for n in _nodos_hecho(rn033.forma["cuando"])} == set(SIN_LADO)
    assert voc["hechos"]["sesgo"]["caduca"] == "al_abrir_sesion"
    assert voc["hechos"]["sesgo"]["consume"] == ["RN-005", "RN-033"]
    assert "rompe" in voc["predicados"]  # declarado, sin ninguna regla que lo invoque


def test_vale_fuera_de_los_valores_o_sobre_un_hecho_sin_valores_falla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    forma = _forma_de(reglas, "RN-033")
    forma["cuando"]["cualquiera_de"][0]["vale"] = "permanente"  # token, pero no de `sesgo`
    fallos = comprobar_forma(_con_forma(reglas, "RN-033", forma), voc, parametros, tipos=tipos)
    assert any("RN-033" in f and "vale='permanente'" in f for f in fallos), fallos
    forma = _forma_de(reglas, "RN-033")
    forma["cuando"]["cualquiera_de"][0] = {"hecho": "orden_dimensionada", "vale": "ambiguo"}
    fallos = comprobar_forma(_con_forma(reglas, "RN-033", forma), voc, parametros, tipos=tipos)
    assert any("orden_dimensionada" in f and "no declara `valores`" in f for f in fallos), fallos


def test_un_valor_de_hecho_que_no_es_token_falla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["sesgo"]["valores"].append("raro")
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("hechos 'sesgo'" in f and "'raro'" in f for f in fallos), fallos


def test_sentido_como_token_no_pasa_en_un_predicado_con_lado_de_ruido(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    forma = _forma_de(reglas, "RN-005")
    forma["cuando"]["todos_de"][1]["se_desarrolla_en_el_lado_de_ruido"]["sentido"] = "ambiguo"
    fallos = comprobar_forma(_con_forma(reglas, "RN-005", forma), voc, parametros, tipos=tipos)
    assert any("RN-005" in f and "LIGADURA" in f for f in fallos), fallos


def test_caduca_exige_un_token_de_caducidad_y_solo_en_hechos_de_regla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["sesgo"]["caduca"] = "permanente"  # token de clase duracion, no caducidad
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("hechos 'sesgo'" in f and "caducidad" in f for f in fallos), fallos
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["operacion_abierta"]["caduca"] = "al_abrir_sesion"
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("operacion_abierta" in f and "origen broker" in f for f in fallos), fallos
