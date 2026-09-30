"""RN-002 desde la sesion 3 (ADR-0060): toda operacion se cierra antes de que termine su vela H4.

El predicado `vence_vela_h4` sobre la rejilla de `anclaje_h4` -la del sesgo, no la ventana-, con la
antelacion leida del registro; la forma de RN-002 que lo nombra; y el parametro nuevo. El cierre de
punta a punta por el cableado vive en `test_cableado.py`, junto a su mercado sintetico. Ninguna
fecha real: los dias son de 2030."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, cast

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MinutoUtc
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import FICHERO_SPEC, _invocaciones, cargar_reglas, cargar_vocabulario

RAIZ = Path(__file__).resolve().parents[2]
ARGS = {"anclaje": "anclaje_h4", "antelacion": "cierre_h4_antelacion"}
PARAMETRO = "cierre_h4_antelacion"


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _vence(registro: Registro, utc: str) -> Tri:
    instante = MinutoUtc(a_minuto(datetime.fromisoformat(f"{utc}+00:00")))
    predicado = primitivas_escritas(registro).predicados["vence_vela_h4"]
    salida = predicado(ARGS, Momento(instante, "07-11", False, None), EstadoDia())
    assert isinstance(salida, Resultado)
    return salida.valor


# Martes 15 de enero de 2030, invierno a los dos lados: el ancla (17:00 Nueva York) cae a las
# 22:00 UTC y la rejilla corta a las 22, 02, 06, 10 y 14 UTC. El evento del minuto t es el cierre
# de la M1 [t - 1, t).
@pytest.mark.parametrize(
    ("utc", "esperado"),
    [
        ("2030-01-15T09:58", Tri.NO),  # quedan dos minutos
        ("2030-01-15T09:59", Tri.SI),  # queda uno: «siempre menos un minuto»
        ("2030-01-15T10:00", Tri.SI),  # el propio limite: lo llenado en el ultimo minuto
        ("2030-01-15T10:01", Tri.NO),  # ya es la vela siguiente
        ("2030-01-15T12:00", Tri.NO),
        ("2030-01-15T13:59", Tri.SI),
        ("2030-01-15T14:00", Tri.SI),
        ("2030-01-15T06:00", Tri.SI),  # la apertura de la ventana es el limite de la H4 anterior
        ("2030-01-15T06:01", Tri.NO),
    ],
)
def test_vence_un_minuto_antes_del_fin_de_la_h4_y_en_el_propio_limite(
    registro: Registro, utc: str, esperado: Tri
) -> None:
    assert _vence(registro, utc) is esperado


# Martes 12 de marzo de 2030: EE. UU. ya cambio la hora (el 10) y la UE todavia no (el 31). El
# ancla cae a las 21:00 UTC y la rejilla corta a las 21, 01, 05, 09 y 13 UTC: a mitad de las
# sesiones del trader (10:00 y 14:00 de Madrid). El cierre sigue a la REJILLA, no a la ventana.
@pytest.mark.parametrize(
    ("utc", "esperado"),
    [
        ("2030-03-12T08:59", Tri.SI),
        ("2030-03-12T09:00", Tri.SI),
        ("2030-03-12T09:01", Tri.NO),
        ("2030-03-12T09:59", Tri.NO),  # las 10:59 de Madrid: en esta semana no vence ninguna H4
        ("2030-03-12T10:00", Tri.NO),
        ("2030-03-12T12:59", Tri.SI),
        ("2030-03-12T13:00", Tri.SI),
    ],
)
def test_en_las_semanas_de_desfase_el_cierre_sigue_a_la_rejilla_y_no_a_la_ventana(
    registro: Registro, utc: str, esperado: Tri
) -> None:
    assert _vence(registro, utc) is esperado


class _RegistroFalso:
    """Un registro minimo: el ancla real y una antelacion que el test elige."""

    def __init__(self, antelacion: int) -> None:
        self.antelacion = antelacion
        self.leidos: list[str] = []

    def hora(self, nombre: str) -> HoraLocal:
        self.leidos.append(nombre)
        return HoraLocal("17:00", "America/New_York")

    def minutos(self, nombre: str) -> int:
        self.leidos.append(nombre)
        return self.antelacion


def test_la_antelacion_y_el_ancla_salen_del_registro_por_su_nombre() -> None:
    """Ninguna cifra en el codigo (ADR-0002): con otra antelacion, otro instante."""
    falso = _RegistroFalso(5)
    predicado = primitivas_escritas(cast(Registro, falso)).predicados["vence_vela_h4"]

    def vence(utc: str) -> Tri:
        instante = MinutoUtc(a_minuto(datetime.fromisoformat(f"{utc}+00:00")))
        salida = predicado(ARGS, Momento(instante, "07-11", False, None), EstadoDia())
        assert isinstance(salida, Resultado)
        return salida.valor

    assert vence("2030-01-15T09:54") is Tri.NO
    assert vence("2030-01-15T09:55") is Tri.SI
    assert vence("2030-01-15T10:00") is Tri.SI
    assert vence("2030-01-15T10:01") is Tri.NO
    assert set(falso.leidos) == {"anclaje_h4", "cierre_h4_antelacion"}


def test_el_parametro_nace_con_la_cifra_y_la_fuente_del_trader(registro: Registro) -> None:
    p = registro.parametros[PARAMETRO]
    assert registro.minutos(PARAMETRO) == 1
    assert p.categoria == "estrategia" and p.estado.value == "CONFIRMED"
    # el item de evidencia con la frase; el registro de feedback es un CORRECT sobre la REGLA
    assert p.fuente is not None and p.fuente.id == "ev-v9-002735-472432b8"


def test_la_forma_de_rn002_nombra_la_rejilla_y_conserva_el_fin_de_la_ventana() -> None:
    spec = RAIZ / FICHERO_SPEC
    rn002 = next(r for r in cargar_reglas(spec) if r.id == "RN-002")
    assert rn002.clase == "terminal" and rn002.vigente and isinstance(rn002.forma, dict)
    llamadas: dict[str, dict[str, Any]] = dict(_invocaciones(rn002.forma["cuando"]))
    assert llamadas["vence_vela_h4"] == ARGS
    assert llamadas["alcanza_hora"] == {"hora": "ventana_fin", "huso": "huso_operativa"}
    assert {"anclaje_h4", PARAMETRO, "ventana_fin"} <= set(rn002.parametros)
    # el cierre depende de la posicion viva, que sigue ligada en el `todos_de` de la raiz
    assert {"hecho": "operacion_abierta", "liga": "OP"} in rn002.forma["cuando"]["todos_de"]
    declarado = cargar_vocabulario(spec)["predicados"]["vence_vela_h4"]
    assert declarado["fuente"] == "reloj" and declarado["argumentos"] == ["anclaje", "antelacion"]
