"""El cableado del simulador (ADR-0053) sobre un dia SINTETICO de 2030 y la spec REAL: una
estrategia sintetica -primitivas de geometria que viven AQUI, fuera de src- coloca una limite a
traves del motor de reglas (RN-011 y RN-015), se llena con ticks, cierra por stop y la cuenta da
el veredicto; un gate de la firma que antes quedaba en DESCONOCIDO (RN-029) prohibe cuando la
cuenta cruza su limite; reloj unico; sin mirar al futuro; determinismo byte a byte; ticks
obligatorios; y las negativas del arnes por la CLI."""

from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.cases.criterio_fidelidad import Criterio, Tolerancias, cargar_criterio
from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import arnes, cableado
from botsito.engine.broker import (
    LLENADA,
    MANUAL,
    MOTIVO_PRECIO_INVALIDO,
    Broker,
    BrokerError,
)
from botsito.engine.cableado import CableadoError, MotorCableado, comprobar_reloj_unico
from botsito.engine.cuenta import EstadoCuenta, ReglasFase, reglas_de_fase
from botsito.engine.entrada import LIMITE_EN_RETROCESO, STOP_EN_RUPTURA
from botsito.engine.interprete import (
    EstadoDia,
    Momento,
    NoImplementada,
    Resultado,
    Tri,
    reglas_ejecutables,
)
from botsito.engine.llenado import OBJETIVO, RESPALDO_M1, STOP, TICKS, TIPO_STOP, Configuracion
from botsito.engine.motor import DatosMercado, DiaDeMercado, Sesion
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulacion import MercadoDia, reglas_broker_de
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

RAIZ = Path(__file__).resolve().parents[2]
SPEC = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
PERFIL = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
DIA = date(2030, 1, 15)  # martes, invierno: 07:00 Madrid = 06:00Z
SPREAD = 3
ESCALA = 100_000
BASE = 110_000  # 1.10000
ENTRADA = BASE - 5
EXTREMO = ENTRADA - 20  # caja de 20 puntos: stop a 16 (0,8), objetivo a +60 (1:3 sobre la caja)
MINUTO_ZONA = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))  # 09:00 Madrid
MINUTO_INI = int(a_minuto(datetime(2030, 1, 15, 6, 0, tzinfo=UTC)))
MINUTO_FIN = int(a_minuto(datetime(2030, 1, 15, 14, 0, tzinfo=UTC)))


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(SPEC)


def _h4_alcista() -> list[Vela]:
    """Tres H4 cerradas antes de la ventana, la ultima rompe la maxima de la anterior: alcista."""
    inicio = int(a_minuto(datetime(2030, 1, 14, 10, 0, tzinfo=UTC)))
    velas = []
    niveles = [(BASE - 300, BASE - 100), (BASE - 200, BASE - 50), (BASE - 150, BASE + 20)]
    for i, (lo, hi) in enumerate(niveles):
        m = inicio + 240 * i
        velas.append(
            Vela(
                MinutoUtc(m), Puntos(lo + 10), Puntos(hi), Puntos(lo), Puntos(hi - 10), 1, 240, 240
            )
        )
    return velas


def _mercado(
    ruta_bid: Mapping[int, int], hasta_ms: int | None = None, con_ticks: bool = True
) -> MercadoDia:
    """M1 y ticks de la ventana. `ruta_bid`: minuto -> BID de cierre; entre puntos, plano. Ticks
    a los 0, 20 y 40 s con el BID del minuto (el ultimo minuto de una bajada baja en el de 40 s)."""
    m1: list[Vela] = []
    ticks: list[Tick] = []
    bid = BASE
    for m in range(MINUTO_INI, MINUTO_FIN):
        objetivo = ruta_bid.get(m, bid)
        o, c = bid, objetivo
        m1.append(
            Vela(
                MinutoUtc(m), Puntos(o), Puntos(max(o, c) + 1), Puntos(min(o, c) - 1), Puntos(c), 1
            )
        )
        for seg, b in ((0, o), (20, (o + c) // 2), (40, c)):
            ms = m * MS_POR_MINUTO + seg * 1000
            if hasta_ms is None or ms <= hasta_ms:
                ticks.append(Tick(MilisegundoUtc(ms), Puntos(b + SPREAD), Puntos(b), 0, 0))
        bid = objetivo
    return MercadoDia(
        "caso-x-2030-01-15", DIA, MinutoUtc(MINUTO_INI), MinutoUtc(MINUTO_FIN), ESCALA,
        tuple(m1), tuple(ticks) if con_ticks else (), ("sintetico",) if con_ticks else (), (),
    )  # fmt: skip


RUTA_STOP = {MINUTO_ZONA + 3: ENTRADA - 2, MINUTO_ZONA + 6: ENTRADA - 17}  # llena y salta el stop
RUTA_HUECO = {MINUTO_ZONA + 3: ENTRADA - 2, MINUTO_ZONA + 6: ENTRADA - 2000}  # salto de 2.000
# para una COMPRA STOP en la entrada (rama trabajo/broker-ordenes-stop): el precio baja por debajo
# de la entrada antes de la zona (la stop queda por encima del ASK, bien colocada), la cruza hacia
# arriba despues y llega al objetivo (+60)
RUTA_ORDEN_STOP = {
    MINUTO_ZONA - 5: ENTRADA - 10,
    MINUTO_ZONA + 3: ENTRADA + 5,
    MINUTO_ZONA + 8: ENTRADA + 70,
}


# llena la limite y el precio se queda quieto: ni stop ni objetivo, asi que la posicion llega
# viva al fin de su vela H4 (06:00-10:00 UTC, la sesion 07-11 de Madrid en invierno)
RUTA_VIVA = {MINUTO_ZONA + 3: ENTRADA - 6}
FIN_H4 = int(a_minuto(datetime(2030, 1, 15, 10, 0, tzinfo=UTC)))


def _sinteticas(minuto_zona: int = MINUTO_ZONA) -> tuple[dict[str, Any], dict[str, Any]]:
    """La estrategia SINTETICA: la geometria que la spec deja NO_IMPLEMENTADA, resuelta a mano.
    En MINUTO_ZONA liga Z a una zona de compra; los demas gates de geometria dan NO; los
    acumuladores del trader (hueco de ADR-0053 §3.3) dan NO."""
    zona_puesta = {"hecho": False}

    def toca(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        if int(momento.instante) == minuto_zona and not zona_puesta["hecho"]:
            zona_puesta["hecho"] = True
            return Resultado(Tri.SI, {"Z": "zona:1"})
        return Resultado(Tri.NO)

    def no(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        return Resultado(Tri.NO)

    def esquema(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        return Resultado(Tri.SI if args.get("cual") == "primer_esquema" else Tri.NO)

    predicados = {
        "toca_colocar_orden_limite": toca,
        "se_desarrolla_en_el_lado_de_ruido": no,
        "se_da_esquema": esquema,
        "zonas_desarrolladas_superan": no,
        "se_completa_zona_de_control": no,
        "alcanza_nivel": no,
        "cruza": no,
        "contexto_filtrable": no,
        "ninguna_regla_de_entrada_aplica": no,
    }
    acumuladores = {"perdida_dia": no, "perdida_semana": no, "cartuchos": no}
    return predicados, acumuladores


def _motor(
    registro: Registro,
    vocabulario: dict[str, dict[str, Any]],
    mercado: MercadoDia,
    reglas_fase: ReglasFase | None = None,
    depuracion: bool = False,
) -> MotorCableado:
    perfil = cargar_perfil(PERFIL)
    predicados, acumuladores = _sinteticas()
    motor = MotorCableado(
        vocabulario=vocabulario,
        reglas=reglas_ejecutables(cargar_reglas(SPEC)),
        registro=registro,
        mercados={DIA.isoformat(): mercado},
        reglas_broker=reglas_broker_de(perfil),
        reglas_fase=reglas_fase or reglas_de_fase(perfil, "reto"),
        config_llenado=Configuracion(False, 0, lambda _m: SPREAD),
        contrato=registro.decimal("instrumento_contrato"),
        depuracion=depuracion,
        primitivas_extra=predicados,
        acumuladores_extra=acumuladores,
    )
    zona = cableado.zona_sintetica("zona:1", "compra", ENTRADA, EXTREMO, "primer_esquema")
    # la zona se inyecta en el contexto del dia a traves del broker: el motor la registra al crear
    # el contexto (ver `MotorCableado.zonas_de`)
    motor.zonas_de = lambda md: {"zona:1": zona}
    return motor


def _dia() -> DiaDeMercado:
    return DiaDeMercado(DIA, HUSO, SESIONES, DatosMercado(_h4_alcista()))


def _criterio() -> Criterio:
    from fractions import Fraction

    return Criterio(
        Tolerancias(3, 15, ESCALA), Fraction(7, 10), Fraction(6, 10), ("2030-01",), ("2030-02",)
    )


# ---------------------------------------------------------------------- punta a punta


def test_una_estrategia_sintetica_coloca_una_limite_por_el_motor_se_llena_y_cierra_por_stop(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    r = motor.correr_dia(_dia())
    traza = r.sesiones["07-11"]
    assert "RN-011" in traza.disparadas and "RN-015" in traza.disparadas
    assert ("orden_dimensionada", "zona:1") in {(h, v) for _, _, h, v in traza.fijados}
    tb = motor.trazas_broker[DIA.isoformat()]
    tipos = [t for _, t, _, _ in tb.eventos]
    assert tipos == [LLENADA, STOP], tb.eventos
    broker = motor.brokers[DIA.isoformat()]
    p = next(iter(broker.posiciones.values()))
    assert (p.entrada, p.stop, p.objetivo) == (ENTRADA, ENTRADA - 16, ENTRADA + 60)
    # 0,5 % de 100.000 sobre 16 puntos: 500 / 16 = 31,25 lotes, ya multiplo de 0,01 (RN-027 no toca)
    assert p.lotes == Decimal("31.25")
    assert (
        r.operaciones
        and r.operaciones[0].sesion == "07-11"
        and r.operaciones[0].direccion == "compra"
    )
    estado, motivo, _ = motor.veredicto()
    assert estado is EstadoCuenta.EN_CURSO
    comision = (
        motor.reglas_broker.comision_por_lote
        * Decimal("31.25")
        * (2 if motor.reglas_broker.comision_por_lado else 1)
    )
    # el stop se llena al precio del tick que lo cruza (ADR-0051, DN-3): un punto bajo el stop
    assert p.precio_cierre == ENTRADA - 17
    perdida = (
        Decimal(ENTRADA - p.precio_cierre) * p.lotes
    )  # 17 puntos x 31,25 lotes, contrato 100.000/escala 100.000
    assert (
        motor.cuenta is not None
        and motor.cuenta.saldo == motor.reglas_fase.capital_inicial - perdida - comision
    )
    assert tb.por_fuente[TICKS] == 2 and tb.por_fuente[RESPALDO_M1] == 0 and not tb.depuracion
    # RN-012 dispara con el stop (salta_stop es de fuente broker y ya se lee)
    assert "RN-012" in traza.disparadas
    # los gates de la firma ya no estan en DESCONOCIDO: ningun acumulador de la firma falta
    faltan = {p for _, p in traza.no_implementadas}
    assert not any(
        p.startswith("acumulador:perdida_dia_firma")
        or p.startswith("acumulador:perdida_total_firma")
        for p in faltan
    )


def test_rn002_cierra_la_posicion_viva_antes_del_fin_de_su_vela_h4(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Sesion 3, S-1 (ADR-0060): «siempre menos un minuto, antes de que cierre [...] la sesion
    de cuatro horas». Una posicion que llega viva al final de su H4 se cierra a mercado en el
    evento anterior al limite de la rejilla de anclaje_h4 -la antelacion la da el registro-,
    y no a las 15:00 de la ventana."""
    motor = _motor(registro, vocabulario, _mercado(RUTA_VIVA))
    r = motor.correr_dia(_dia())
    tb = motor.trazas_broker[DIA.isoformat()]
    assert [t for _, t, _, _ in tb.eventos] == [LLENADA, MANUAL], tb.eventos
    p = next(iter(motor.brokers[DIA.isoformat()].posiciones.values()))
    antelacion = registro.minutos("cierre_h4_antelacion")
    assert p.motivo_cierre == MANUAL
    assert p.cerrada_ms == (FIN_H4 - antelacion) * MS_POR_MINUTO - 1
    assert "RN-002" in r.sesiones["07-11"].disparadas
    assert "RN-002" not in r.sesiones["11-15"].disparadas
    # sin posicion viva la regla no dispara: en la ruta del stop ya esta cerrada
    otro = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    assert "RN-002" not in otro.correr_dia(_dia()).sesiones["07-11"].disparadas


def test_un_gate_de_la_firma_prohibe_cuando_la_cuenta_cruza_su_limite(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Un hueco de 2.000 puntos por debajo del stop: el stop se llena al precio del tick (DN-3 de
    ADR-0051) y la cuenta pierde 62.500 sobre 100.000. RN-029 y RN-031, que antes quedaban en
    DESCONOCIDO, disparan en el cierre de M1 siguiente, prohiben y fijan sus hechos; la cuenta
    queda SUSPENDIDA en el instante del tick."""
    motor = _motor(registro, vocabulario, _mercado(RUTA_HUECO))
    r = motor.correr_dia(_dia())
    traza = r.sesiones["07-11"]
    assert {"RN-029", "RN-031"} <= traza.disparadas
    hechos = {(h, v) for _, _, h, v in traza.fijados}
    assert ("detenido_por_tope", "hasta_el_corte_siguiente") in hechos
    assert ("detenido_por_tope_total", "permanente") in hechos
    estado, motivo, instante = motor.veredicto()
    assert estado is EstadoCuenta.SUSPENDIDA and "perdida" in motivo
    tb = motor.trazas_broker[DIA.isoformat()]
    stop_ms = next(ms for ms, t, _, _ in tb.eventos if t == STOP)
    assert instante == datetime.fromtimestamp(stop_ms / 1000, UTC)
    # reloj unico: la regla ve el evento en el primer cierre de M1 posterior al tick, nunca antes
    minuto_regla = min(m for m, r_, h, _ in traza.fijados if h == "detenido_por_tope")
    assert minuto_regla == stop_ms // MS_POR_MINUTO + 1


def test_reloj_unico_se_comprueba_al_arrancar(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    perfil = cargar_perfil(PERFIL)
    reglas = dataclasses.replace(
        reglas_de_fase(perfil, "reto"), huso_corte=ZoneInfo("America/New_York")
    )
    with pytest.raises(CableadoError, match="no hay un solo reloj"):
        _motor(registro, vocabulario, _mercado(RUTA_STOP), reglas_fase=reglas)
    comprobar_reloj_unico(
        registro, reglas_de_fase(perfil, "reto"), {DIA.isoformat(): _mercado(RUTA_STOP)}
    )


def test_sin_mirar_al_futuro_de_punta_a_punta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    completo = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    rc = completo.correr_dia(_dia())
    tb = completo.trazas_broker[DIA.isoformat()]
    stop_ms = next(ms for ms, t, _, _ in tb.eventos if t == STOP)
    corte = stop_ms + MS_POR_MINUTO  # un minuto despues del stop
    recortado = _motor(registro, vocabulario, _mercado(RUTA_STOP, hasta_ms=corte))
    rr = recortado.correr_dia(_dia())
    limite = corte // MS_POR_MINUTO + 1

    def hasta(r: Any) -> list[tuple[str, tuple[int, str, str, str]]]:
        return sorted((s, f) for s, tr in r.sesiones.items() for f in tr.fijados if f[0] <= limite)

    assert hasta(rc) == hasta(rr) and hasta(rc)
    assert [e for e in tb.eventos if e[0] <= corte] == [
        e for e in recortado.trazas_broker[DIA.isoformat()].eventos if e[0] <= corte
    ]


def test_determinismo_byte_a_byte_del_informe(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    def informe() -> str:
        motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
        dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), ()),)
        corrida = arnes.correr("cableado", ("2030-01",), dias, {DIA.isoformat(): _dia()}, motor)
        return arnes.informe(corrida, _criterio(), vocabulario) + cableado.informe_simulacion(motor)

    assert informe().encode("utf-8") == informe().encode("utf-8")


def test_una_orden_stop_por_el_arnes_real_salta_al_romper_y_cierra_por_objetivo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    """ADR-0056 §8, rama 1: una operacion completa con orden STOP de punta a punta, por
    `arnes.correr` con la spec real (RN-011 y RN-015). La estrategia sigue colocando limites (el
    selector de A-47 no existe todavia): aqui la accion que coloca se desvia a la orden stop del
    broker, que es lo unico que esta rama le da. El stops level va en diagnostico (A-27)."""
    monkeypatch.setattr(Broker, "colocar_limite", Broker.colocar_stop)
    motor = _motor(registro, vocabulario, _mercado(RUTA_ORDEN_STOP))
    motor.stops_level_diagnostico = 2
    dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), ()),)
    corrida = arnes.correr("cableado", ("2030-01",), dias, {DIA.isoformat(): _dia()}, motor)
    informe = arnes.informe(corrida, _criterio(), vocabulario) + cableado.informe_simulacion(motor)
    broker = motor.brokers[DIA.isoformat()]
    orden = next(iter(broker.ordenes.values()))
    assert orden.tipo == TIPO_STOP and orden.precio == ENTRADA
    tb = motor.trazas_broker[DIA.isoformat()]
    assert [t for _, t, _, _ in tb.eventos] == [LLENADA, OBJETIVO], tb.eventos
    p = next(iter(broker.posiciones.values()))
    # el ASK toca la entrada en el tick de los 20 s del minuto que sube: sin hueco, al nivel
    assert (p.entrada, p.deslizamiento_entrada, p.stop, p.objetivo) == (
        ENTRADA,
        0,
        ENTRADA - 16,
        ENTRADA + 60,
    )
    assert p.abierta_ms == (MINUTO_ZONA + 3) * MS_POR_MINUTO + 20_000
    assert (p.motivo_cierre, p.precio_cierre) == (OBJETIVO, ENTRADA + 60)
    assert corrida.dias and informe
    assert motor.cuenta is not None and motor.cuenta.saldo > motor.reglas_fase.capital_inicial


def test_rn011_con_el_selector_en_stop_de_punta_a_punta_por_el_arnes(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """ADR-0056 §8, rama 2, y ADR-0058: con `entrada_tipo_orden` en `stop_en_ruptura` (aqui por el
    campo del motor, como lo pone la CLI con --diagnostico-a47), RN-011 y RN-015 dimensionan y la
    entrada va al broker como COMPRA STOP en el 0 de la caja, en el cierre del breaker. Sin
    desviar nada: es la via real. Sale una operacion completa, llenada al romper y cerrada por
    objetivo."""
    motor = _motor(registro, vocabulario, _mercado(RUTA_ORDEN_STOP))
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.stops_level_diagnostico = 2
    dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), ()),)
    arnes.correr("cableado", ("2030-01",), dias, {DIA.isoformat(): _dia()}, motor)
    broker = motor.brokers[DIA.isoformat()]
    orden = next(iter(broker.ordenes.values()))
    assert (orden.tipo, orden.lado, orden.precio) == (TIPO_STOP, "compra", ENTRADA)
    assert orden.colocada_ms == MINUTO_ZONA * MS_POR_MINUTO - 1
    tb = motor.trazas_broker[DIA.isoformat()]
    assert [t for _, t, _, _ in tb.eventos] == [LLENADA, OBJETIVO], tb.eventos
    p = next(iter(broker.posiciones.values()))
    assert (p.entrada, p.stop, p.objetivo, p.motivo_cierre) == (
        ENTRADA,
        ENTRADA - 16,
        ENTRADA + 60,
        OBJETIVO,
    )


def test_con_el_selector_en_limite_sale_lo_mismo_que_sin_selector(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """La linea base de las limites no cambia: `limite_en_retroceso` es lo de siempre, byte a
    byte, en el informe del arnes y en el de la simulacion."""

    def informe(tipo: str | None) -> str:
        motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
        motor.tipo_orden = tipo
        dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), ()),)
        corrida = arnes.correr("cableado", ("2030-01",), dias, {DIA.isoformat(): _dia()}, motor)
        return arnes.informe(corrida, _criterio(), vocabulario) + cableado.informe_simulacion(motor)

    assert informe(LIMITE_EN_RETROCESO).encode("utf-8") == informe(None).encode("utf-8")


def test_con_el_selector_en_stop_y_el_precio_ya_roto_la_orden_se_rechaza(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El caso que ADR-0056 §1.3 anticipa y ADR-0058 mide: en RUTA_STOP el precio esta POR ENCIMA
    de la entrada en el cierre del breaker, asi que una compra stop alli queda del lado
    equivocado, y el broker la rechaza (ADR-0057); la limite, en cambio, espera y se llena."""
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.stops_level_diagnostico = 0
    motor.correr_dia(_dia())
    tb = motor.trazas_broker[DIA.isoformat()]
    broker = motor.brokers[DIA.isoformat()]
    assert not broker.posiciones and not [e for e in tb.eventos if e[1] == LLENADA]
    assert [r.motivo for r in broker.traza().rechazos] == [MOTIVO_PRECIO_INVALIDO]


def test_sin_stops_level_la_orden_stop_no_se_coloca_y_lo_dice(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(Broker, "colocar_limite", Broker.colocar_stop)
    motor = _motor(registro, vocabulario, _mercado(RUTA_ORDEN_STOP))
    with pytest.raises(BrokerError, match="A-27"):
        motor.correr_dia(_dia())


def test_los_ticks_son_obligatorios_y_la_depuracion_lo_marca(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    sin_ticks = _mercado(RUTA_STOP, con_ticks=False)
    with pytest.raises(CableadoError, match="ticks son obligatorios"):
        _motor(registro, vocabulario, sin_ticks).correr_dia(_dia())
    motor = _motor(registro, vocabulario, sin_ticks, depuracion=True)
    motor.correr_dia(_dia())
    tb = motor.trazas_broker[DIA.isoformat()]
    assert tb.depuracion and tb.por_fuente[RESPALDO_M1] >= 2 and tb.por_fuente[TICKS] == 0
    assert cableado.DEPURACION in cableado.informe_simulacion(motor)


def test_la_cuenta_persiste_entre_dias_y_la_estrategia_empieza_de_cero(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """ADR-0053 §6: el mismo mercado dos dias seguidos por el MISMO motor. La zona sintetica se
    liga otra vez (la estrategia y el broker empiezan de cero) y la cuenta arrastra el saldo: la
    segunda perdida sale del saldo ya mermado, asi que el lote es menor."""
    dia2 = date(2030, 1, 21)  # el lunes siguiente: cinco dias de calendario sin correr
    salto = 6 * 1440  # minutos entre el martes 15 y el lunes 21
    m2 = dataclasses.replace(_mercado(RUTA_STOP), caso="caso-x-2030-01-21", dia=dia2)
    m2 = dataclasses.replace(
        m2,
        desde=MinutoUtc(MINUTO_INI + salto),
        hasta=MinutoUtc(MINUTO_FIN + salto),
        m1=tuple(dataclasses.replace(v, inicio=MinutoUtc(int(v.inicio) + salto)) for v in m2.m1),
        ticks=tuple(
            Tick(
                MilisegundoUtc(int(k.instante) + salto * MS_POR_MINUTO),
                k.ask,
                k.bid,
                k.volumen_ask,
                k.volumen_bid,
            )
            for k in m2.ticks
        ),
    )
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    motor.mercados = {**motor.mercados, dia2.isoformat(): m2}
    r1 = motor.correr_dia(_dia())
    assert motor.cuenta is not None
    saldo_1 = motor.cuenta.saldo
    lote_1 = next(iter(motor.brokers[DIA.isoformat()].posiciones.values())).lotes
    # el dia 2: la zona sintetica se vuelve a activar en su minuto, seis dias despues
    predicados, acumuladores = _sinteticas(minuto_zona=MINUTO_ZONA + salto)
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    r2 = motor.correr_dia(DiaDeMercado(dia2, HUSO, SESIONES, DatosMercado(_h4_alcista())))
    assert (
        "RN-015" in r1.sesiones["07-11"].disparadas and "RN-015" in r2.sesiones["07-11"].disparadas
    )
    assert len(r1.operaciones) == 1 and len(r2.operaciones) == 1
    lote_2 = next(iter(motor.brokers[dia2.isoformat()].posiciones.values())).lotes
    assert saldo_1 < motor.reglas_fase.capital_inicial and motor.cuenta.saldo < saldo_1
    assert lote_2 < lote_1  # el 0,5 % del saldo mermado
    assert motor.cuenta.dias_de_trading == 2
    assert [d for d, *_ in cableado.curva_de_equity(motor)] == [DIA.isoformat(), dia2.isoformat()]
    # la cuenta corto los cinco dias de calendario intermedios, y la curva no los nombra
    assert len(motor.cuenta.dias()) >= 6
    # y el broker del dia 1 no arrastra nada al dia 2
    assert set(motor.brokers[dia2.isoformat()].posiciones) == set(
        motor.brokers[DIA.isoformat()].posiciones
    )


def test_las_negativas_por_la_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """`--simular` pasa por la MISMA compuerta que el arnes y el visor (ADR-0053 §8): un mes de
    medida o uno que no es de construccion se niega ANTES de construir el motor y no escribe nada.
    El centinela de un dia oculto vive en `dias_de_construccion` y `caso_de_construccion`, que son
    las dos puertas que el cableado llama (tests de arnes y visor)."""
    from botsito import cli

    real = cargar_criterio(RAIZ)
    informe = tmp_path / "sim.txt"
    carpeta = tmp_path / "visor"
    for mes in (*real.medida, "2026-03"):
        codigo = cli.main(
            [
                "--repo",
                str(RAIZ),
                "motor",
                "arnes",
                "--simular",
                "--meses",
                mes,
                "--salida",
                str(informe),
            ]
        )
        assert codigo == 2 and not informe.exists(), mes
        codigo = cli.main(
            [
                "--repo",
                str(RAIZ),
                "motor",
                "visor",
                "--simular",
                "--caso",
                f"caso-x-{mes}-00",
                "--salida",
                str(carpeta),
            ]
        )
        assert codigo == 2 and not carpeta.exists(), mes
    err = capsys.readouterr().err
    assert "MEDIDA" in err and "construccion" in err


def test_el_visor_ensena_las_ordenes_y_los_llenados_del_bot(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    motor.correr_dia(_dia())
    detalle = cableado.detalle_para_visor(motor, DIA.isoformat())
    assert detalle is not None and detalle.depuracion is None
    assert [o.estado for o in detalle.ordenes] == [LLENADA]
    assert [p.estado for p in detalle.posiciones] == [STOP]
    assert [e.tipo for e in detalle.eventos] == [LLENADA, STOP]
    assert detalle.posiciones[0].stop == Decimal(ENTRADA - 16) / ESCALA
    assert detalle.posiciones[0].objetivo == Decimal(ENTRADA + 60) / ESCALA
    assert cableado.detalle_para_visor(motor, "2030-01-16") is None
