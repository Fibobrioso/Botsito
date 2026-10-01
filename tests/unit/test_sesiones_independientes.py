"""Cada sesion es un escenario propio (A-46 RESUELTA en la sesion 3; ADR-0055 §4, ADR-0049 H1).

El hecho `liquidez_tomada` caduca al abrir cada sesion, como `sesgo`, y el productor de la zona de
entrada (`engine/zonas.py`) guarda la toma, el esquema y el id de la zona SESION A SESION: una toma
de la primera sesion no vale en la segunda, y una segunda sesion con su propia toma y su propio
esquema liga su propia zona. Sobre un dia SINTETICO de 2030 y la spec REAL."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.domain.estructura_m1 import SOLO_UNA_ZONA_DE_CONTROL
from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import diagnostico, zonas
from botsito.engine.diagnostico import Diagnostico
from botsito.engine.interprete import EstadoDia, Interprete, Momento, ReglaEjecutable
from botsito.engine.motor import DatosMercado, MotorSpec
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.primitivas import primitivas_escritas
from botsito.engine.tope_trader import tope_del_registro
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_preparar_a21 as t21
from tests.unit import test_preparar_a35 as ta

RAIZ = Path(__file__).resolve().parents[2]
SEGUNDA = ta.INICIO + 240  # la apertura de la sesion 11-15 (10:00Z)
BLOQUES_POR_SESION = 240 // ta.M15
BAJA = 100  # la segunda sesion repite el dibujo de la primera, cien puntos mas abajo


@pytest.fixture(scope="module")
def registro(tmp_path_factory: pytest.TempPathFactory) -> Registro:
    # Estos tests prueban la zona que nace AL DARSE EL ESQUEMA. Desde ADR-0064 el valor de
    # `orden_limite_nace` es `al_aparecer_punto_de_breaker` (la vida de la orden stop, que prueba
    # tests/unit/test_orden_stop_pivote.py): aqui se fija la otra lectura, que sigue en pie
    texto = (RAIZ / "knowledge" / "spec" / "parametros.yaml").read_text(encoding="utf-8")
    viejo = '    valor: "al_aparecer_punto_de_breaker"\n'
    assert texto.count(viejo) == 1
    ruta = tmp_path_factory.mktemp("registro") / "parametros.yaml"
    ruta.write_text(texto.replace(viejo, '    valor: "al_darse_el_esquema"\n'), encoding="utf-8")
    return cargar_registro(ruta)


@pytest.fixture(scope="module")
def reglas() -> list[ReglaEjecutable]:
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.spec.modelo import cargar_reglas

    return list(reglas_ejecutables(cargar_reglas(ta.SPEC)))


def _m1_con_dos_tomas() -> list[Vela]:
    """La primera sesion, como en `test_preparar_a21` (toma y primer esquema, LIMPIO). La segunda
    repite el dibujo entero cien puntos mas abajo: seis bloques de M15 que dejan un pivote BAJO
    nuevo y lo toman con cuerpo, y el mismo camino LIMPIO despues de esa toma."""
    primera = [v for v in t21._m1(t21.LIMPIO) if int(v.inicio) < SEGUNDA]
    segunda: list[Vela] = []
    for n, (a, c, lo) in enumerate(ta.BLOQUES):
        segunda += ta._bloque(
            n + BLOQUES_POR_SESION, a - BAJA, c - BAJA, None if lo is None else lo - BAJA
        )
    minuto = SEGUNDA + ta.M15 * len(ta.BLOQUES)
    for a, c, lo, hi in t21.LIMPIO:
        a, c = a - BAJA, c - BAJA
        segunda.append(
            Vela(
                MinutoUtc(minuto),
                Puntos(a),
                Puntos(hi - BAJA if hi is not None else max(a, c) + 1),
                Puntos(lo - BAJA if lo is not None else min(a, c) - 1),
                Puntos(c),
                1,
            )
        )
        minuto += 1
    ultimo = t21.LIMPIO[-1][1] - BAJA
    while minuto < ta.FIN:
        segunda.append(
            Vela(
                MinutoUtc(minuto),
                Puntos(ultimo),
                Puntos(ultimo + 1),
                Puntos(ultimo - 1),
                Puntos(ultimo),
                1,
            )  # fmt: skip
        )
        minuto += 1
    return primera + segunda


def _datos(registro: Registro, m1: list[Vela]) -> DatosMercado:
    anclaje = registro.hora("anclaje_h4")
    return DatosMercado(ta._h4_alcista(), agregar(m1, ta.M15, anclaje), m1, CIERRE_VELA_CONTRARIA)


def _motor(registro: Registro, reglas: list[ReglaEjecutable]) -> MotorSpec:
    tope = tope_del_registro(
        registro,
        cargar_perfil(tc.PERFIL).huso_corte(),
        Diagnostico(a44=diagnostico.A44_SIN_TOPE),
    )
    primitivas = primitivas_escritas(registro, tope, SOLO_UNA_ZONA_DE_CONTROL)
    return MotorSpec(Interprete(cargar_vocabulario(ta.SPEC), primitivas), reglas)


def test_liquidez_tomada_caduca_al_abrir_cada_sesion(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    motor = _motor(registro, reglas)
    assert "liquidez_tomada" in motor.interprete.caducan_al_abrir
    datos = _datos(registro, t21._m1(t21.LIMPIO))
    estado = EstadoDia(hechos={"liquidez_tomada": "si", "sesgo": "alcista"})
    apertura = Momento(MinutoUtc(SEGUNDA), "11-15", True, datos)
    ev = motor.interprete.evento(motor.reglas, apertura, estado)
    assert "liquidez_tomada" in ev.caducados
    assert "liquidez_tomada" not in estado.hechos
    # y solo en la apertura: dentro de la sesion el hecho sigue vivo
    estado = EstadoDia(hechos={"liquidez_tomada": "si", "sesgo": "alcista"})
    dentro = Momento(MinutoUtc(SEGUNDA + 5), "11-15", False, datos)
    ev = motor.interprete.evento(motor.reglas, dentro, estado)
    assert ev.caducados == [] and estado.hechos["liquidez_tomada"] == "si"


def test_la_toma_de_la_primera_sesion_no_vale_en_la_segunda(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """El dia de `test_preparar_a21`: toma y zona en la primera sesion, y despues el precio se
    queda quieto. En la segunda no hay toma nueva, asi que no hay liquidez tomada, RN-008 prohibe
    y el productor no arrastra ni la toma ni el esquema de la manana (ADR-0055 §4)."""
    motor = _motor(registro, reglas)
    datos = _datos(registro, t21._m1(t21.LIMPIO))
    r = motor.correr_dia(ta._dia(datos))
    primera, segunda = r.sesiones["07-11"], r.sesiones["11-15"]
    assert "liquidez_tomada" in primera.hechos_producidos and "RN-011" in primera.disparadas
    assert "liquidez_tomada" not in segunda.hechos_producidos
    assert "RN-008" in segunda.disparadas and "RN-011" not in segunda.disparadas


def test_cada_sesion_con_su_toma_liga_su_propia_zona(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    motor = _motor(registro, reglas)
    r = motor.correr_dia(ta._dia(_datos(registro, _m1_con_dos_tomas())))
    primera, segunda = r.sesiones["07-11"], r.sesiones["11-15"]
    for traza in (primera, segunda):
        assert {"RN-004", "RN-011", "RN-015"} <= traza.disparadas
    breaker_1 = t21.TOMA + len(t21.LIMPIO)
    breaker_2 = SEGUNDA + ta.M15 * len(ta.BLOQUES) + len(t21.LIMPIO)
    ligadas = [
        (t, v) for traza in (primera, segunda) for t, _, h, v in traza.fijados
        if h == "orden_dimensionada" and v != "no"
    ]  # fmt: skip
    assert ligadas == [(breaker_1, "zona:1"), (breaker_2, "zona:2")]


def test_la_memoria_del_productor_es_de_cada_sesion(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Lo que el productor guarda -la toma, el esquema y el id de la zona- se lee por sesion
    (`zonas.memoria_de_sesion`), y las zonas ligadas siguen juntas en la memoria del dia."""
    motor = _motor(registro, reglas)
    datos = _datos(registro, _m1_con_dos_tomas())
    dia = ta._dia(datos)
    estado = EstadoDia()
    limites = {"07-11": (ta.INICIO, SEGUNDA), "11-15": (SEGUNDA, ta.FIN)}
    for nombre, (desde, hasta) in limites.items():
        ultimo = hasta if nombre == "11-15" else hasta - 1
        for t in range(desde, ultimo + 1):
            motor.interprete.evento(
                motor.reglas, Momento(MinutoUtc(t), nombre, t == desde, dia.datos), estado
            )
    una, otra = (zonas.memoria_de_sesion(estado, s) for s in ("07-11", "11-15"))
    # la toma de cada sesion es la de SU primera M1 que cierra con cuerpo bajo SU nivel
    assert una["toma"]["instante"] == ta.TOMA_M1 and una["zona_id"] == "zona:1"
    assert otra["toma"]["instante"] == ta.TOMA_M1 + 240
    assert otra["zona_id"] == "zona:2"
    assert otra["toma"]["nivel"] == una["toma"]["nivel"] - BAJA
    assert otra["esquema"].entrada == una["esquema"].entrada - BAJA
    assert sorted(zonas.zonas_del_dia(estado)) == ["zona:1", "zona:2"]
    assert zonas.memoria_de_sesion(estado, "no-existe") == {}
