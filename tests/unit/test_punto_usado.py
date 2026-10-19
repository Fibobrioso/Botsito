"""Que gasta un punto (ADR-0083, rama `trabajo/punto-usado`; enmienda la decision 1 de ADR-0064),
por el CABLEADO REAL y la spec real, con dias y velas SINTETICOS de 2030 (`test_cableado`).

Lo que decide es el productor real (`toca_colocar_orden_limite` de `primitivas_zona`, con sus marcas
`usadas` y `rechazados`; RN-011, RN-015, RN-006, RN-016, RN-034, RN-018 reales): lo unico sintetico
de la geometria es `zona_del_punto`, sustituido por un plan «desde este cierre se ve el punto con
este 1», que registra la zona EXACTAMENTE como la real (`puntos`, `punto_de_zona`, el escenario y
`zonas` del dia) para que la misma caja sea la misma zona y otro 1 sea otra zona del mismo punto.
Cada test dice que caja construye a proposito.

Fase 1 (el campo): «### Ordenes» lleva al final el punto y el 1 de la caja, solo salida.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from decimal import Decimal
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.estructura_m1 import PRIMER_ESQUEMA
from botsito.domain.pivotes_m15 import BAJO, Pivote
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import cableado, primitivas_broker, zonas
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.zonas import Zona
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_escenarios_por_sesion as te

DIA = tc.DIA.isoformat()
SESION = "07-11"
Z = tc.MINUTO_ZONA  # el primer cierre en que se ve el punto
E = tc.ENTRADA  # el 0 del punto (el nivel del pivote)
TOMA = Z - 2  # la toma de la liquidez de M15, antes del punto
VELA_CONTRARIA = Z - 3  # el minuto en que empieza la vela contraria del punto
PUNTO = f"{E}@{VELA_CONTRARIA}"  # la clave `nivel@inicio` (zonas.py, `clave_punto`)
CAJA = E - 20  # el 1 de la caja de siempre: stop a -16 (0,8), objetivo a +60 (1:3)
OTRA_CAJA = E - 25  # otro 1 del mismo punto: otra zona (stop a -20, objetivo a +75)
MS = MS_POR_MINUTO


def _cierre(instante: int) -> int:
    """El instante ms en que el cableado coloca en el cierre `instante` (`instante * MS - 1`)."""
    return instante * MS - 1


class _Datos(DatosMercado):
    """Las H4 alcistas de `test_cableado`, las M1 del mercado sintetico (RN-014 las lee) y una
    liquidez de M15: un BAJO por debajo del punto, tomado en TOMA."""

    def __init__(self, h4: Any, m1: Any) -> None:
        super().__init__(h4, velas_m1=m1)

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        return te._pivote(tc.BASE - 50, TOMA - 30, BAJO) if lado == BAJO else None


def _geometria(plan: Mapping[int, int]) -> Callable[..., Zona | None]:
    """`zona_del_punto` sintetico: `plan` dice desde que cierre se ve el punto y con que 1; el
    ultimo tramo del plan manda. Registra la zona como la real (zonas.py, `zona_del_punto`): una
    zona por `punto#extremo`, el id `zona:N`, `punto_de_zona`, ligada al escenario vigente."""

    def zona_del_punto(registro: Registro, momento: Momento, estado: EstadoDia) -> Zona | None:
        if momento.sesion != SESION:
            return None
        if zonas._anotar_toma(momento.datos, momento, estado) is None:
            return None
        t = int(momento.instante)
        vistos = [desde for desde in plan if desde <= t]
        if not vistos:
            return None
        extremo = plan[max(vistos)]
        mem = zonas._de_la_sesion(estado, momento.sesion)
        puntos = mem.setdefault("puntos", {})
        del_dia = zonas._memoria(estado).setdefault("zonas", {})
        clave = f"{PUNTO}#{extremo}"
        id = puntos.get(clave)
        if id is None:
            id = f"{zonas.PREFIJO_ZONA}{len(del_dia) + 1}"
            puntos[clave] = id
            mem.setdefault("punto_de_zona", {})[id] = PUNTO
            zonas._ligar_al_escenario(estado, momento.sesion, id)
            del_dia[id] = Zona(id, "compra", E, extremo, PRIMER_ESQUEMA, VELA_CONTRARIA, t)
        return del_dia[id]  # type: ignore[no-any-return]

    return zona_del_punto


def _correr(
    registro: Registro,
    ruta: Mapping[int, int],
    plan: Mapping[int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> tuple[Any, Any]:
    """Un dia por el cableado real: la spec real con el productor real de la zona (`limpia`
    fijada), RN-004 disparada en TOMA por una geometria de toma sintetica, los gates de geometria
    que no se prueban (RN-005, RN-009, el esquema) sinteticos como en `test_cableado`, y el
    acumulador `cartuchos` REAL. La orden es STOP en la ruptura (A-47)."""
    vocabulario = cargar_vocabulario(tc.SPEC)
    mercado = tc._mercado(ruta)
    motor = tc._motor(registro, vocabulario, mercado)
    motor.limpia = "solo_una_zona_de_control"
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.zonas_de = None  # las zonas son del productor, no del contexto
    predicados, acumuladores = tc._sinteticas()
    for real in ("toca_colocar_orden_limite", "se_completa_zona_de_control"):
        del predicados[real]
    del acumuladores["cartuchos"]

    def toma(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI if int(momento.instante) == TOMA else Tri.NO)

    def si(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI)

    predicados.update({"alcanza_nivel": toma, "cruza": toma, "la_toma_es_de_la_sesion": si})
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    geometria = _geometria(plan)
    monkeypatch.setattr(zonas, "zona_del_punto", geometria)  # el predicado del productor
    monkeypatch.setattr(primitivas_broker, "zona_del_punto", geometria)  # `_punto_nuevo`
    datos = _Datos(tc._h4_alcista(), list(mercado.m1))
    r = motor.correr_dia(DiaDeMercado(tc.DIA, tc.HUSO, tc.SESIONES, datos))
    return motor, r


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


# el precio, por minuto (BID de cierre): por debajo del punto antes de Z (la stop de compra queda
# por encima del ask: valida), rompe el punto en Z+3 (se llena), y lo que diga cada test
ANTES = {Z - 5: E - 10}
ROMPE = E + 5
GANA = E + 70  # por encima del objetivo de +60


def _fila_de_ordenes(motor: Any) -> str:
    texto = cableado.informe_simulacion(motor)
    seccion = texto.split("### Ordenes", 1)[1].split("### Ordenes no enviadas", 1)[0]
    (fila,) = [ln for ln in seccion.splitlines() if ln.startswith(f"{DIA} | ")]
    return fila


# ------------------------------------------------------------ fase 1: el campo de «### Ordenes»


def test_la_fila_de_ordenes_lleva_al_final_el_punto_y_el_1_de_la_caja(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Solo salida (regimen de `bloqueadas`, R3.1): las dos ultimas columnas son el punto de la
    orden (`nivel@inicio`) y el 1 de su caja, en precio; las quince de antes no se mueven. La
    caja: CAJA (una sola zona del punto); o1 se llena y llega al objetivo."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: GANA}
    motor, _ = _correr(registro, ruta, {Z: CAJA}, monkeypatch)
    assert cableado.CABECERA_ORDENES.endswith(" | limite | punto | caja 1)")
    campos = _fila_de_ordenes(motor).split(" | ")
    assert len(campos) == 17
    assert campos[:3] == [DIA, SESION, "o1"] and campos[5] == "llenada"
    assert campos[15:] == [PUNTO, str(Decimal(CAJA) / tc.ESCALA)]


def test_sin_productor_el_punto_y_la_caja_dicen_sin_medida(registro: Registro) -> None:
    """El otro sentido: una zona sintetica del contexto (`test_cableado`) no tiene punto ni caja
    del productor, y las dos columnas salen `-`. Nada mas cambia en la fila."""
    motor = tc._motor(registro, cargar_vocabulario(tc.SPEC), tc._mercado(tc.RUTA_STOP))
    motor.correr_dia(tc._dia())
    fila = _fila_de_ordenes(motor)
    assert fila.endswith(f" | 31.25 | margen | {cableado.SIN_MEDIDA} | {cableado.SIN_MEDIDA}")
    assert " | llenada | - | " in fila
