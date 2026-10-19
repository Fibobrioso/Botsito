"""Que gasta un punto (ADR-0083, rama `trabajo/punto-usado`; enmienda la decision 1 de ADR-0064),
por el CABLEADO REAL y la spec real, con dias y velas SINTETICOS de 2030 (`test_cableado`).

Lo que decide es el productor real (`toca_colocar_orden_limite` de `primitivas_zona`, con sus marcas
`usadas` y `rechazados`; RN-011, RN-015, RN-006, RN-016, RN-034, RN-018 reales): lo unico sintetico
de la geometria es `zona_del_punto`, sustituido por un plan «desde este cierre se ve el punto con
este 1», que registra la zona EXACTAMENTE como la real (`puntos`, `punto_de_zona`, el escenario y
`zonas` del dia) para que la misma caja sea la misma zona y otro 1 sea otra zona del mismo punto.
Cada test dice que caja construye a proposito.

Fase 1 (el campo): «### Ordenes» lleva al final el punto y el 1 de la caja, solo salida.
Fase 2 (D1-D4): los tests que en `main` fallan por la razon que dicen son los dos de D3, el de
`_punto_nuevo` tras una perdida y el del break even (la misma caja no vuelve en `main`).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.estructura_m1 import PRIMER_ESQUEMA
from botsito.domain.pivotes_m15 import BAJO, Pivote
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import cableado, primitivas_broker, zonas
from botsito.engine.broker import (
    CANCELADA,
    LLENADA,
    MOTIVO_MARGEN_LIBRE,
    MOTIVO_PRECIO_INVALIDO,
    PETICION_CANCELAR,
    PETICION_COLOCAR,
    RECHAZADA,
    STOP_MOVIDO,
)
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.llenado import OBJETIVO, STOP
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.primitivas_broker import BREAK_EVEN, GANANCIA, SALTO_EL_STOP
from botsito.engine.zonas import Zona
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_escenarios_por_sesion as te
from tests.unit import test_margen_lote as tm

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


def _ordenes(motor: Any) -> Any:
    return motor.brokers[DIA].ordenes


def _eventos(motor: Any) -> list[str]:
    return [t for _, t, _, _ in motor.trazas_broker[DIA].eventos]


def _peticiones(motor: Any) -> list[tuple[str, str]]:
    return [(p.tipo, p.id) for p in motor.trazas_broker[DIA].peticiones]


def _resultados(motor: Any) -> list[str]:
    """El resultado clasificado de cada cierre, en su orden (lo que ven RN-016 y RN-034)."""
    broker = motor.brokers[DIA]
    salida = []
    for p in sorted(broker.posiciones.values(), key=lambda p: p.abierta_ms):
        assert p.precio_cierre is not None and p.motivo_cierre is not None
        signo = 1 if p.lado == "compra" else -1
        bruto = Decimal(signo * (p.precio_cierre - p.entrada))
        salida.append(
            primitivas_broker.clasificar_cierre(p.motivo_cierre, p.stop_original is not None, bruto)
        )
    return salida


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


# el precio, por minuto (BID de cierre): por debajo del punto antes de Z (la stop de compra queda
# por encima del ask: valida), rompe el punto en Z+3 (se llena), y lo que diga cada test
ANTES = {Z - 5: E - 10}
ROMPE = E + 5
PIERDE = E - 17  # bid por debajo del stop de -16: salta el stop; y el ask (E - 14) vuelve a estar
# por debajo del punto: la stop de compra se puede volver a colocar en el cierre siguiente
GANA = E + 70  # por encima del objetivo de +60


# ------------------------------------------------------------------------- D3a: tras una perdida


def test_tras_una_perdida_el_mismo_punto_se_vuelve_a_colocar_con_la_misma_caja(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D3a (ADR-0083). La caja: la MISMA todo el dia (el 1 en CAJA, una sola zona del punto). o1 se
    llena en Z+3 y salta su stop en Z+6 (perdida); en el cierre siguiente (Z+7) RN-011 y RN-015
    vuelven a colocar o2 en el mismo punto, con la misma caja (mismo stop y mismo objetivo); o2 se
    llena y llega al objetivo, y RN-034 termina el escenario: nada mas se coloca. En `main` falla:
    la zona sigue en `usadas` tras el stop y o2 no existe (VISOR-CONSTRUCCION.md §2.d.4, al reves:
    `main` solo vuelve con OTRA caja)."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: PIERDE, Z + 9: ROMPE, Z + 12: GANA}
    motor, r = _correr(registro, ruta, {Z: CAJA}, monkeypatch)
    ordenes = _ordenes(motor)
    assert list(ordenes) == ["o1", "o2"], list(ordenes)
    o1, o2 = ordenes["o1"], ordenes["o2"]
    assert (o1.precio, o1.stop, o1.objetivo, o1.estado) == (E, E - 16, E + 60, LLENADA)
    assert (o2.precio, o2.stop, o2.objetivo, o2.estado) == (E, E - 16, E + 60, LLENADA)
    assert o2.colocada_ms == _cierre(Z + 7)  # el cierre siguiente al stop
    assert _eventos(motor) == [LLENADA, STOP, LLENADA, OBJETIVO]
    assert _resultados(motor) == [SALTO_EL_STOP, GANANCIA]
    assert _peticiones(motor) == [(PETICION_COLOCAR, "o1"), (PETICION_COLOCAR, "o2")]
    estado = motor.estados[DIA]
    # la misma zona las dos veces, y tras la ganadora el escenario esta terminado (RN-034)
    assert zonas.zonas_del_dia(estado).keys() == {"zona:1"}
    assert zonas.escenario_terminado(estado, SESION)
    assert "RN-034" in r.sesiones[SESION].disparadas


def test_tras_una_perdida_un_1_nuevo_coloca_otra_zona_del_mismo_punto(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: CAJA hasta el stop y OTRA_CAJA desde el cierre que lo sigue (Z+7): otra zona del
    mismo punto. o2 se coloca con el stop y el objetivo de la caja nueva. Pasa en `main` y en la
    rama: es lo que `main` ya hacia (la E de VISOR §2.d.4 leida como reentrada con otra caja)."""
    # el objetivo de la otra caja esta en +75: el precio sube mas que en D3a
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: PIERDE, Z + 9: ROMPE, Z + 12: E + 85}
    motor, _ = _correr(registro, ruta, {Z: CAJA, Z + 7: OTRA_CAJA}, monkeypatch)
    ordenes = _ordenes(motor)
    assert list(ordenes) == ["o1", "o2"]
    o2 = ordenes["o2"]
    assert (o2.precio, o2.stop, o2.objetivo, o2.colocada_ms) == (E, E - 20, E + 75, _cierre(Z + 7))
    assert _eventos(motor) == [LLENADA, STOP, LLENADA, OBJETIVO]
    assert set(zonas.zonas_del_dia(motor.estados[DIA])) == {"zona:1", "zona:2"}


# ------------------------------------------------------------------------- tras un break even


# tras el llenado en Z+3, el dibujo de RUTA_BREAK_EVEN de `test_cableado`: sube, retrocede con una
# roja y la M1 siguiente pasa el punto alto (RN-014 mueve el stop a la entrada al tick), y el
# precio vuelve: sale por break even, por debajo del punto (el ask queda por debajo de E)
VUELVE = {Z + 4: E + 10, Z + 5: E + 20, Z + 6: E + 14, Z + 7: E + 25, Z + 12: E - 8}


def test_tras_un_break_even_el_mismo_punto_se_vuelve_a_colocar_igual_que_tras_la_perdida(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: la MISMA (CAJA). o1 se llena, RN-014 pone el stop en la entrada y el precio vuelve:
    cierre `break_even` (no gasta cartucho, RN-016). En el cierre siguiente o2 vuelve al mismo punto
    con la misma caja (D1: «una perdida, un break even o un equal»). En `main` falla como D3a."""
    ruta = {**ANTES, Z + 3: ROMPE, **VUELVE, Z + 15: ROMPE, Z + 18: GANA}
    motor, r = _correr(registro, ruta, {Z: CAJA}, monkeypatch)
    assert "RN-014" in r.sesiones[SESION].disparadas
    ordenes = _ordenes(motor)
    assert list(ordenes) == ["o1", "o2"], list(ordenes)
    p1 = motor.brokers[DIA].posiciones["pos-o1"]
    assert p1.stop_original == E - 16 and p1.stop == E  # el break even de RN-014
    assert _eventos(motor) == [LLENADA, STOP_MOVIDO, STOP, LLENADA, OBJETIVO]
    assert _resultados(motor) == [BREAK_EVEN, GANANCIA]
    o2 = ordenes["o2"]
    assert (o2.precio, o2.stop, o2.objetivo) == (E, E - 16, E + 60)
    assert o2.colocada_ms == _cierre(Z + 13)


# ---------------------------------------------------------------- tras una ganadora: nada (RN-034)


def test_tras_una_ganadora_nada_se_vuelve_a_colocar(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: CAJA, y OTRA_CAJA desde Z+10 (otra zona del mismo punto, que en `main` se
    colocaria si el escenario siguiera). o1 llega al objetivo en Z+6: RN-034 termina el escenario y
    `toca_colocar_orden_limite` niega aunque el precio vuelva por debajo del punto. Pasa en los
    dos."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: GANA, Z + 9: E - 10}
    motor, r = _correr(registro, ruta, {Z: CAJA, Z + 10: OTRA_CAJA}, monkeypatch)
    assert list(_ordenes(motor)) == ["o1"]
    assert _eventos(motor) == [LLENADA, OBJETIVO]
    assert zonas.escenario_terminado(motor.estados[DIA], SESION)
    assert "RN-034" in r.sesiones[SESION].disparadas


# --------------------------------------------------------------------- los cartuchos (RN-016)


def test_los_cartuchos_cortan_la_reentrada_al_agotarse(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: un 1 nuevo en cada reentrada (CAJA, luego -25, -30 y -35), para que `main` tambien
    reentre y el test pase en los dos. Tres perdidas seguidas en el mismo punto gastan los tres
    cartuchos (`cartuchos_max`): RN-016 fija `detenido_por_cartuchos` y la cuarta zona, visible, no
    se coloca."""
    assert registro.entero("cartuchos_max") == 3
    ruta = {**ANTES}
    for k in range(3):
        ruta[Z + 3 + 6 * k] = ROMPE
        ruta[Z + 6 + 6 * k] = E - 45  # por debajo de los tres stops (-16, -20 y -24)
    plan = {Z: CAJA, Z + 7: E - 25, Z + 13: E - 30, Z + 19: E - 35}
    motor, r = _correr(registro, ruta, plan, monkeypatch)
    assert list(_ordenes(motor)) == ["o1", "o2", "o3"]
    assert _eventos(motor) == [LLENADA, STOP] * 3
    assert _resultados(motor) == [SALTO_EL_STOP] * 3
    assert ("RN-016", "detenido_por_cartuchos", "hasta_cartuchos_reinicio") in [
        (regla, hecho, valor) for _, regla, hecho, valor in r.sesiones[SESION].fijados
    ]
    assert "zona:4" in zonas.zonas_del_dia(motor.estados[DIA])  # vista, y no colocada


# ------------------------------------------------------------- D3b: el rechazo al llenar gasta


# el salto que hace que el margen al precio del llenado no quepa (ADR-0081 §4): el lote se limito
# al 95 % del margen libre al colocar, y un llenado un 9 % mas caro pide mas del 100 %
SALTO = E + 20_000


def test_tras_un_rechazo_al_llenar_el_punto_no_se_vuelve_a_colocar_con_ninguna_caja(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D3b (ADR-0083). La caja: CAJA, y OTRA_CAJA desde Z+6 (otra zona del mismo punto: en `main`
    se colocaria, porque solo la ZONA quedaba usada). o1 se coloca con el lote que cabe en el 95 %
    del margen libre; el precio salta y el llenado pide mas margen del que hay: el broker la
    rechaza AL LLENAR (`margen_libre`, peticion `llenar`). El precio vuelve por debajo del punto y
    el punto esta gastado: ni la misma caja ni otra. En `main` falla: o2 existe."""
    ruta = {**ANTES, Z + 3: SALTO, Z + 5: E - 10}
    motor, _ = _correr(registro, ruta, {Z: CAJA, Z + 6: OTRA_CAJA}, monkeypatch)
    broker = motor.brokers[DIA]
    o1 = broker.ordenes["o1"]
    assert o1.estado == RECHAZADA and not broker.posiciones
    (rechazo,) = broker.traza().rechazos
    assert (rechazo.orden_id, rechazo.motivo) == ("o1", MOTIVO_MARGEN_LIBRE)
    assert _eventos(motor) == [RECHAZADA]
    estado = motor.estados[DIA]
    assert zonas.punto_rechazado(estado, SESION, "zona:1")  # el punto, gastado
    assert "zona:2" in zonas.zonas_del_dia(estado)  # la otra caja se vio...
    assert list(broker.ordenes) == ["o1"]  # ...y no se coloco
    texto = cableado.informe_simulacion(motor)
    assert f"2030-01 | {MOTIVO_MARGEN_LIBRE} | llenar | 1" in texto


# ------------------------------------- el rechazo al colocar y el no envio siguen gastando


def test_el_rechazo_al_colocar_sigue_gastando_el_punto(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: CAJA, y OTRA_CAJA desde Z+4. En Z el precio ya esta por encima del punto: la stop
    de compra queda del lado equivocado y el broker la rechaza al colocar (`precio_invalido`,
    ADR-0057). Despues el precio baja y la otra caja se ve: el punto esta gastado (ADR-0064,
    decision 1, que ADR-0083 conserva para el rechazo). Pasa en los dos."""
    ruta = {Z - 5: E + 10, Z + 3: E - 10}
    motor, _ = _correr(registro, ruta, {Z: CAJA, Z + 4: OTRA_CAJA}, monkeypatch)
    broker = motor.brokers[DIA]
    assert [(o.id, o.estado) for o in broker.ordenes.values()] == [("o1", RECHAZADA)]
    assert broker.traza().rechazos[0].motivo == MOTIVO_PRECIO_INVALIDO
    estado = motor.estados[DIA]
    assert zonas.punto_rechazado(estado, SESION, "zona:1")
    assert "zona:2" in zonas.zonas_del_dia(estado)


def test_el_no_envio_sigue_gastando_el_punto(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: CAJA, y OTRA_CAJA desde Z+4. Con `lote_si_no_cabe = no_operar` el lote del riesgo
    no cabe en el margen y la orden no se envia (ADR-0081 §2 y §3): queda en «no enviadas», el
    punto gastado, y la otra caja no se coloca. Pasa en los dos."""
    registro = tm._registro_con_no_operar(tmp_path)
    ruta = {**ANTES, Z + 3: E - 12}
    motor, _ = _correr(registro, ruta, {Z: CAJA, Z + 4: OTRA_CAJA}, monkeypatch)
    broker = motor.brokers[DIA]
    assert not broker.ordenes
    tb = motor.trazas_broker[DIA]
    assert [(zona, motivo) for _, zona, motivo, _ in tb.no_enviadas] == [
        ("zona:1", "no_operar:margen")
    ]
    estado = motor.estados[DIA]
    assert zonas.punto_rechazado(estado, SESION, "zona:1")
    assert "zona:2" in zonas.zonas_del_dia(estado)


# ------------------------------------------------- D4: con la posicion abierta no se coloca otra


def test_con_la_posicion_abierta_no_se_coloca_otra_orden(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D4. La caja: CAJA, y OTRA_CAJA desde Z+5, con la posicion de o1 ABIERTA de Z+3 a Z+9 (el
    precio se queda entre la entrada y el stop). RN-011 exige `ninguno_de operacion_abierta` y
    RN-018 prohibe abrir con una viva: la otra zona, visible, no se coloca hasta el cierre siguiente
    al stop. Pasa en los dos."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 9: PIERDE}
    motor, _ = _correr(registro, ruta, {Z: CAJA, Z + 5: OTRA_CAJA}, monkeypatch)
    ordenes = _ordenes(motor)
    assert list(ordenes) == ["o1", "o2"]
    p1 = motor.brokers[DIA].posiciones["pos-o1"]
    assert p1.cerrada_ms is not None and _cierre(Z + 9) < p1.cerrada_ms < _cierre(Z + 10)
    assert ordenes["o2"].colocada_ms == _cierre(Z + 10)  # ni un cierre antes
    assert ordenes["o2"].stop == E - 20  # la otra caja


# ------------------------------------------- la reubicacion (RN-006, ADR-0074) y `_punto_nuevo`


def test_con_la_orden_sin_llenar_el_1_nuevo_la_reubica_como_hoy(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La caja: CAJA en Z y OTRA_CAJA desde Z+2, con o1 SIN llenar (el precio no rompe). RN-006
    cancela o1 y RN-011 y RN-015 colocan o2 en el mismo cierre con la caja nueva (ADR-0074, ADR-0056
    §7). Pasa en los dos."""
    motor, r = _correr(registro, {**ANTES}, {Z: CAJA, Z + 2: OTRA_CAJA}, monkeypatch)
    ordenes = _ordenes(motor)
    o1, o2 = ordenes["o1"], ordenes["o2"]
    assert (o1.estado, o1.stop) == (CANCELADA, E - 16)
    assert (o2.stop, o2.objetivo, o2.colocada_ms) == (E - 20, E + 75, o1.ultimo_cambio_ms)
    assert o2.colocada_ms == _cierre(Z + 2)
    assert "RN-006" in r.sesiones[SESION].disparadas
    assert _peticiones(motor)[:3] == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_CANCELAR, "o1"),
        (PETICION_COLOCAR, "o2"),
    ]


def test_punto_nuevo_sigue_reconociendo_la_orden_de_la_sesion_tras_una_perdida(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`_punto_nuevo` (RN-006) lee `usadas` para saber que la pendiente es de esta sesion. La
    caja: CAJA; tras la perdida de o1, o2 vuelve con la misma caja (D3a) y en Z+9 aparece
    OTRA_CAJA con o2 sin llenar: RN-006 la reubica (cancelar o2, colocar o3 en el mismo cierre).
    `usadas` sigue conteniendo la zona de una orden pendiente, asi que la reubicacion ve a o2 como
    propia. En `main` falla: o2 no existe."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: PIERDE}
    motor, r = _correr(registro, ruta, {Z: CAJA, Z + 9: OTRA_CAJA}, monkeypatch)
    # la quinta peticion es RN-035 retirando o3, sin llenar, al abrir la tarde (`se_retira`)
    assert _peticiones(motor) == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_COLOCAR, "o2"),
        (PETICION_CANCELAR, "o2"),
        (PETICION_COLOCAR, "o3"),
        (PETICION_CANCELAR, "o3"),
    ]
    ordenes = _ordenes(motor)
    assert ordenes["o2"].colocada_ms == _cierre(Z + 7)
    assert ordenes["o3"].colocada_ms == ordenes["o2"].ultimo_cambio_ms == _cierre(Z + 9)
    assert ordenes["o3"].stop == E - 20
    assert "RN-006" in r.sesiones[SESION].disparadas
    estado = motor.estados[DIA]
    assert zonas.zonas_usadas(estado, SESION) == frozenset({"zona:1", "zona:2"})


# ------------------------------------------------------------ fase 1: el campo de «### Ordenes»


def test_la_fila_de_ordenes_lleva_al_final_el_punto_y_el_1_de_la_caja(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Solo salida (regimen de `bloqueadas`, R3.1): las dos ultimas columnas son el punto de la
    orden (`nivel@inicio`) y el 1 de su caja, en precio; las quince de antes no se mueven."""
    ruta = {**ANTES, Z + 3: ROMPE, Z + 6: GANA}
    motor, _ = _correr(registro, ruta, {Z: CAJA}, monkeypatch)
    texto = cableado.informe_simulacion(motor)
    assert cableado.CABECERA_ORDENES.endswith(" | limite | punto | caja 1)")
    seccion = texto.split("### Ordenes", 1)[1].split("### Ordenes no enviadas", 1)[0]
    (fila,) = [ln for ln in seccion.splitlines() if ln.startswith(f"{DIA} | ")]
    campos = fila.split(" | ")
    assert len(campos) == 17
    assert campos[:3] == [DIA, SESION, "o1"] and campos[5] == "llenada"
    assert campos[15:] == [PUNTO, str(Decimal(CAJA) / tc.ESCALA)]


def test_sin_productor_el_punto_y_la_caja_dicen_sin_medida(
    registro: Registro,
) -> None:
    """El otro sentido: una zona sintetica del contexto (`test_cableado`) no tiene punto ni caja
    del productor, y las dos columnas salen `-`. Nada mas cambia en la fila."""
    vocabulario = cargar_vocabulario(tc.SPEC)
    motor = tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))
    motor.correr_dia(tc._dia())
    texto = cableado.informe_simulacion(motor)
    seccion = texto.split("### Ordenes", 1)[1].split("### Ordenes no enviadas", 1)[0]
    (fila,) = [ln for ln in seccion.splitlines() if ln.startswith(f"{DIA} | ")]
    assert fila.endswith(f" | 31.25 | margen | {cableado.SIN_MEDIDA} | {cableado.SIN_MEDIDA}")
