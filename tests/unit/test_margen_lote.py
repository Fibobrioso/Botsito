"""El margen y el lote que no cabe (ADR-0081, rama trabajo/margen-lote; fases 2 y 3). Escritos
ANTES del codigo, en rojo sobre el de `main` mas el campo de salida de la fase 1 (el recuento de
FAILED esta en MARGEN-LOTE.md §3). Sobre el broker SINTETICO de `test_broker` (contrato 1, escala 1:
el margen de un lote a 1000 con 1:30 son 33,33) y sobre el dia sintetico de `test_cableado`.

Lo que comprueban, en el orden del encargo (fase 2):
- el broker rechaza por margen al colocar, con el margen libre justo por encima y justo por debajo;
- el margen tiene en cuenta una posicion ya abierta, y una pendiente STOP lo reserva hasta que se
  cancela (la reubicacion de ADR-0074 libera antes de volver a colocar);
- la compra convierte con el ask y la venta con el bid;
- el rechazo al LLENAR, con el precio del llenado y sin contar la reserva de la propia orden; no es
  una peticion al servidor;
- `abrir_conocida` rechaza por margen (tras el volumen);
- el lote se limita por margen, por volumen y por los dos (`limitar_lote`, la funcion pura), el que
  cabe no cambia, y por debajo del minimo no se opera;
- con `lote_si_no_cabe = no_operar` no se coloca, y queda anotado;
- el resultado en R de una operacion limitada es el mismo que sin limite;
- el cableado pasa siempre el saldo al broker, y con apalancamiento el saldo es obligatorio.
"""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine import broker as broker_mod
from botsito.engine import cableado
from botsito.engine.broker import (
    CANCELADA,
    COLOCADA,
    HECHO_ORDEN_PENDIENTE,
    MOTIVO_MARGEN_LIBRE,
    PETICION_COLOCAR,
    RECHAZADA,
    Broker,
    BrokerError,
    Rechazo,
    margen_requerido,
)
from botsito.engine.cuenta import CuentaViva, reglas_de_fase
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.interprete import EstadoDia, Momento
from botsito.engine.llenado import TICKS, TIPO_STOP, Configuracion, Mercado
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.primitivas_broker import (
    ContextoDia,
    OrdenEnPreparacion,
    primitivas_cableadas,
)
from botsito.engine.simulacion import reglas_broker_de
from botsito.engine.zonas import orden_nace_en_el_punto
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_broker as tb
from tests.unit import test_cableado as tc

APAL = 30
CIEN_LOTES = Decimal(100)
DIA = tc.DIA.isoformat()


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(tc.RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


def _saldo(valor: str) -> dict[str, Decimal]:
    return {"v": Decimal(valor)}


def _broker_con_margen(ticks: list[Any], saldo: dict[str, Decimal], **cambios: object) -> Broker:
    return Broker(
        tb._reglas(apalancamiento=APAL, **cambios),
        tb._cfg(),
        Mercado(ticks, []),
        tb.UNO,
        1,
        saldo=lambda: saldo["v"],
    )


def _ticks_planos(bid: int = 1000, minutos: int = 4) -> list[Any]:
    return [tb._tick(tb.M0 + i, 5, bid) for i in range(minutos)]


# -------------------------------------------------------------------- la unica funcion de margen


def test_la_formula_es_lotes_por_contrato_por_precio_entre_apalancamiento() -> None:
    assert margen_requerido(Decimal(3), 1000, 1, tb.UNO, APAL) == Decimal(100)
    assert margen_requerido(Decimal("1.5"), 110000, 100_000, Decimal(100_000), APAL) == Decimal(
        5500
    )


def test_con_apalancamiento_el_saldo_es_obligatorio_y_sin_el_no_hay_margen_que_medir() -> None:
    """Negar por defecto (respuesta a la PARADA, punto 2): el perfil real declara apalancamiento, y
    entonces construir el broker sin el saldo de la cuenta es un error. Un perfil sin
    apalancamiento (los sinteticos) no mide margen, y una orden enorme pasa."""
    with pytest.raises(BrokerError, match="saldo"):
        Broker(tb._reglas(apalancamiento=APAL), tb._cfg(), Mercado(_ticks_planos(), []), tb.UNO, 1)
    sin = tb._broker(_ticks_planos())  # apalancamiento None, sin saldo
    o = sin.colocar_limite("o1", "compra", 990, Decimal(9), 980, 1010, tb._ms(tb.M0, 10))
    assert not isinstance(o, Rechazo)


# ------------------------------------------------------------------------- al colocar


def test_rechaza_al_colocar_justo_por_encima_y_admite_justo_por_debajo() -> None:
    """Saldo 100 y nada vivo: margen libre 100. Una compra convierte con el ASK (1003): 2,99 lotes
    piden 99,97 y pasan; 3,00 piden 100,30 y se rechazan con `margen_libre`, registrado como
    cualquier rechazo del perfil (traza, estado RECHAZADA, peticion no aceptada)."""
    b = _broker_con_margen(_ticks_planos(), _saldo("100"))
    cabe = b.colocar_limite("cabe", "compra", 990, Decimal("2.99"), 980, 1010, tb._ms(tb.M0, 10))
    assert not isinstance(cabe, Rechazo) and cabe.estado == COLOCADA
    b.cancelar("cabe", tb._ms(tb.M0, 11))
    r = b.colocar_limite("grande", "compra", 990, Decimal("3.00"), 980, 1010, tb._ms(tb.M0, 12))
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_MARGEN_LIBRE
    assert b.ordenes["grande"].estado == RECHAZADA
    assert b.traza().rechazos[-1] == r
    assert b.traza().peticiones[-1].tipo == PETICION_COLOCAR
    assert b.traza().peticiones[-1].aceptada is False


def test_la_compra_convierte_con_el_ask_y_la_venta_con_el_bid() -> None:
    """Mismo instante, mismos 3,00 lotes y saldo 100: la compra pide 3 x 1003 / 30 = 100,30 (ask) y
    no cabe; la venta pide 3 x 1000 / 30 = 100,00 (bid) y cabe justo."""
    b = _broker_con_margen(_ticks_planos(), _saldo("100"))
    r = b.colocar_limite("compra", "compra", 990, Decimal("3.00"), 980, 1010, tb._ms(tb.M0, 10))
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_MARGEN_LIBRE
    v = b.colocar_limite("venta", "venta", 1010, Decimal("3.00"), 1020, 990, tb._ms(tb.M0, 11))
    assert not isinstance(v, Rechazo)


def test_una_posicion_abierta_ocupa_margen() -> None:
    """Una posicion de 1 lote abierta a 1000 ocupa 33,33: con saldo 100 quedan 66,67 libres. Una
    compra de 2,00 lotes pide 66,87 (ask 1003) y no cabe; una de 1,99 pide 66,53 y cabe."""
    b = _broker_con_margen(_ticks_planos(), _saldo("100"))
    b.abrir_conocida("real", "compra", 1000, tb.UNO, 990, 1020, tb._ms(tb.M0, 10), "caso")
    assert b.margen_usado() == margen_requerido(tb.UNO, 1000, 1, tb.UNO, APAL)
    r = b.colocar_limite("o2", "compra", 990, Decimal("2.00"), 980, 1010, tb._ms(tb.M0, 11))
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_MARGEN_LIBRE
    o = b.colocar_limite("o3", "compra", 990, Decimal("1.99"), 980, 1010, tb._ms(tb.M0, 12))
    assert not isinstance(o, Rechazo)


def test_una_pendiente_stop_reserva_margen_y_cancelarla_lo_libera() -> None:
    """MT5: «For all other order types (Stop and Stop Limit), the margin is summed up (charged for
    each order)». Una compra STOP de 2,00 lotes en 1010 reserva 67,33 (a su precio); con saldo 100
    la siguiente de 1,00 (33,43 al ask) no cabe. Cancelada la primera, la misma de 1,00 cabe. Es la
    pieza del BROKER; el orden de la reubicacion de ADR-0074 por las primitivas reales, en el mismo
    cierre, lo prueba el test de la reubicacion (`test_en_la_reubicacion_…`)."""
    b = _broker_con_margen(_ticks_planos(), _saldo("100"), stops_level_puntos=0)
    o1 = b.colocar_stop("o1", "compra", 1010, Decimal("2.00"), 1000, 1030, tb._ms(tb.M0, 10))
    assert not isinstance(o1, Rechazo)
    assert b.margen_usado() == margen_requerido(Decimal("2.00"), 1010, 1, tb.UNO, APAL)
    r = b.colocar_stop("o2", "compra", 1010, Decimal("1.00"), 1000, 1030, tb._ms(tb.M0, 11))
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_MARGEN_LIBRE
    b.cancelar("o1", tb._ms(tb.M0, 12))
    assert b.margen_usado() == 0
    o3 = b.colocar_stop("o3", "compra", 1010, Decimal("1.00"), 1000, 1030, tb._ms(tb.M0, 13))
    assert not isinstance(o3, Rechazo)


# -------------------------------------------------------------------------- al llenar


def _ticks_que_disparan_la_stop() -> list[Any]:
    # bid 1000 en M0 (ask 1003 < 1010: no salta), bid 1010 en M0+1 (ask 1013 >= 1010: salta)
    return [tb._tick(tb.M0, 5, 1000), tb._tick(tb.M0 + 1, 5, 1010), tb._tick(tb.M0 + 2, 5, 1010)]


def test_rechaza_al_llenar_si_el_margen_libre_bajo_desde_que_se_coloco() -> None:
    """La stop de 1,00 lote cabe al colocar (33,43 de 100). Antes de que salte, el saldo de la
    cuenta baja a 30: al llenar, al precio del llenado (ask 1013: 33,77), no cabe. La orden pasa a
    RECHAZADA
    con `margen_libre`, no nace posicion, el evento llega a la traza y NO es una peticion (R13)."""
    saldo = _saldo("100")
    b = _broker_con_margen(_ticks_que_disparan_la_stop(), saldo, stops_level_puntos=0)
    o1 = b.colocar_stop("o1", "compra", 1010, Decimal("1.00"), 1000, 1030, tb._ms(tb.M0, 10))
    assert not isinstance(o1, Rechazo)
    peticiones = len(b.traza().peticiones)
    saldo["v"] = Decimal(30)
    eventos = b.avanzar(tb._ms(tb.M0 + 2))
    assert eventos == [(tb._ms(tb.M0 + 1, 5), RECHAZADA, "o1", TICKS)]
    assert b.ordenes["o1"].estado == RECHAZADA and not b.posiciones
    assert b.traza().rechazos[-1].motivo == MOTIVO_MARGEN_LIBRE
    assert b.traza().rechazos[-1].orden_id == "o1"
    assert len(b.traza().peticiones) == peticiones
    assert b.hechos()[broker_mod.HECHO_ORDEN_PENDIENTE] is False
    assert [h for _, h in b.ordenes["o1"].historial] == [COLOCADA, RECHAZADA]


def test_al_llenar_la_reserva_de_la_propia_orden_no_cuenta_contra_ella() -> None:
    """Con saldo 34 la stop de 1,00 lote (33,67 reservados a 1010) cabe al colocar y al llenar
    (33,77 al ask 1013 <= 34): su propia reserva pasa a ser el margen de la posicion, no se suma dos
    veces. Un broker que la contara dos veces la rechazaria aqui."""
    b = _broker_con_margen(_ticks_que_disparan_la_stop(), _saldo("34"), stops_level_puntos=0)
    o1 = b.colocar_stop("o1", "compra", 1010, Decimal("1.00"), 1000, 1030, tb._ms(tb.M0, 10))
    assert not isinstance(o1, Rechazo)
    eventos = b.avanzar(tb._ms(tb.M0 + 2))
    assert [e[1] for e in eventos] == [broker_mod.LLENADA]
    assert b.posiciones["pos-o1"].abierta
    assert b.margen_usado() == margen_requerido(Decimal("1.00"), 1013, 1, tb.UNO, APAL)


def test_abrir_conocida_rechaza_por_margen_despues_del_volumen() -> None:
    b = _broker_con_margen(_ticks_planos(), _saldo("100"))
    with pytest.raises(BrokerError, match="volumen_max_lotes"):
        b.abrir_conocida("v", "compra", 1000, Decimal(11), 990, 1020, tb._ms(tb.M0, 10), "caso")
    with pytest.raises(BrokerError, match=MOTIVO_MARGEN_LIBRE):
        b.abrir_conocida("m", "compra", 1000, Decimal(4), 990, 1020, tb._ms(tb.M0, 11), "caso")
    p = b.abrir_conocida("cabe", "compra", 1000, Decimal(3), 990, 1020, tb._ms(tb.M0, 12), "caso")
    assert p.abierta


# ------------------------------------------------------------------- el limite del bot


def _limitar(lote_riesgo: str, vol_max: str, margen: str, precio: int = 110_000) -> Any:
    return broker_mod.limitar_lote(
        Decimal(lote_riesgo),
        Decimal(vol_max),
        Decimal(margen),
        precio,
        100_000,
        Decimal(100_000),
        APAL,
        Decimal("0.01"),
        Decimal("0.01"),
    )


def test_el_lote_que_cabe_no_cambia() -> None:
    assert _limitar("5", "50", "95000") == (Decimal("5"), ())


def test_el_lote_se_limita_por_margen_por_volumen_y_por_los_dos() -> None:
    """31,25 lotes (0,5 % de 100.000 sobre 1,6 pips) con 95.000 de margen disponible a 1,10 y 1:30:
    caben 25,909 -> 25,90 al paso (margen). Con el tope de volumen en 20, manda el volumen y los dos
    limites muerden. Con el tope en 50 y margen de sobra, solo el volumen."""
    assert _limitar("31.25", "50", "95000") == (Decimal("25.90"), ("margen",))
    assert _limitar("31.25", "20", "95000") == (Decimal("20.00"), ("volumen", "margen"))
    assert _limitar("60", "50", "950000") == (Decimal("50.00"), ("volumen",))


def test_por_debajo_del_minimo_no_se_opera() -> None:
    """ADR-0081 §2 (respuesta a la PARADA, punto 0): por debajo de instrumento_lote_minimo el lote
    es None y el motivo `minimo`; subirlo al minimo arriesgaria mas que riesgo_por_operacion."""
    assert _limitar("0.004", "50", "95000") == (None, ("minimo",))
    assert _limitar("31.25", "50", "30") == (None, ("margen", "minimo"))


def _motor_con_perfil_real(registro: Registro, vocabulario: dict[str, dict[str, Any]]) -> Any:
    return tc._motor(registro, vocabulario, tc._mercado(tc.RUTA_STOP))


def test_en_el_dia_sintetico_el_lote_se_limita_por_margen_y_se_coloca(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El 0,5 % de 100.000 sobre 16 puntos pide 31,25 lotes y mas margen del que hay (fase 1): con
    el
    limite, la orden se coloca con el lote que cabe en el 95 % del margen libre, el broker no la
    rechaza, y la anotacion de la traza dice `margen` y el lote del riesgo."""
    motor = _motor_con_perfil_real(registro, vocabulario)
    motor.correr_dia(tc._dia())
    broker = motor.brokers[DIA]
    o1 = broker.ordenes["o1"]
    assert o1.estado != RECHAZADA and o1.lotes < Decimal("31.25")
    fraccion = registro.decimal("lote_margen_libre_fraccion")
    ask, _ = broker.precio_de_conversion("compra", o1.colocada_ms)
    requerido = margen_requerido(o1.lotes, ask, broker.escala, broker.contrato, APAL)
    assert requerido <= fraccion * Decimal(100_000)
    anotado = motor.trazas_broker[DIA].margen_al_colocar["o1"]
    assert anotado[3:] == (Decimal("31.25"), "margen")
    assert "| 31.25 | margen" in cableado.informe_simulacion(motor)


def test_el_resultado_en_r_de_la_operacion_limitada_es_el_mismo_que_sin_limite(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """La fidelidad mide decisiones: misma entrada, mismo stop, mismo cierre. Sin apalancamiento no
    hay limite (31,25 lotes); con el perfil real el lote baja. El R es el mismo; el dinero, no."""

    def operacion(apalancamiento: int | None) -> Any:
        motor = _motor_con_perfil_real(registro, vocabulario)
        motor.reglas_broker = dataclasses.replace(
            motor.reglas_broker, apalancamiento=apalancamiento
        )
        motor.correr_dia(tc._dia())
        (op,) = motor.brokers[DIA].operaciones_cerradas()
        return op

    con, sin = operacion(APAL), operacion(None)
    assert sin.lotes == Decimal("31.25") and con.lotes < sin.lotes
    assert (con.apertura.precio, con.cierre.precio) == (sin.apertura.precio, sin.cierre.precio)
    assert con.marcas[0].precio == sin.marcas[0].precio  # el stop inicial
    r_con = (con.cierre.precio - con.apertura.precio) / (con.apertura.precio - con.marcas[0].precio)
    r_sin = (sin.cierre.precio - sin.apertura.precio) / (sin.apertura.precio - sin.marcas[0].precio)
    assert r_con == r_sin


def _registro_con_no_operar(tmp_path: Path) -> Registro:
    texto = (tc.RAIZ / "knowledge" / "spec" / "parametros.yaml").read_text(encoding="utf-8")
    viejo = "    valor: limitar\n"
    assert texto.count(viejo) == 1, "lote_si_no_cabe no esta en el registro, o hay otro `limitar`"
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto.replace(viejo, "    valor: no_operar\n"), encoding="utf-8")
    return cargar_registro(ruta)


def test_con_no_operar_la_orden_que_no_cabe_no_se_envia_y_queda_anotada(
    vocabulario: dict[str, dict[str, Any]], tmp_path: Path
) -> None:
    registro = _registro_con_no_operar(tmp_path)
    motor = _motor_con_perfil_real(registro, vocabulario)
    motor.correr_dia(tc._dia())
    broker = motor.brokers[DIA]
    assert not broker.ordenes and not broker.posiciones
    tb_dia = motor.trazas_broker[DIA]
    assert len(tb_dia.no_enviadas) == 1
    _, zona, motivo, lote_riesgo = tb_dia.no_enviadas[0]
    assert (zona, motivo, lote_riesgo) == ("zona:1", "no_operar:margen", Decimal("31.25"))
    texto = cableado.informe_simulacion(motor)
    assert "### Ordenes no enviadas" in texto and "no_operar:margen" in texto


def test_el_cableado_pasa_siempre_el_saldo_de_la_cuenta_al_broker(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor_con_perfil_real(registro, vocabulario)
    motor.correr_dia(tc._dia())
    broker = motor.brokers[DIA]
    assert broker.saldo is not None and broker.saldo() == motor.cuenta.saldo
    assert broker.reglas.apalancamiento == APAL


def test_el_rechazo_al_llenar_sale_en_rechazos_por_motivo_como_llenar() -> None:
    """La salida (`_informe_ordenes`): un rechazo al llenar cuenta con `peticion = llenar`, no como
    `colocar`, y la orden sale `rechazada | margen_libre` en «### Ordenes»."""
    from types import SimpleNamespace

    saldo = _saldo("100")
    b = _broker_con_margen(_ticks_que_disparan_la_stop(), saldo, stops_level_puntos=0)
    b.colocar_stop("o1", "compra", 1010, Decimal("1.00"), 1000, 1030, tb._ms(tb.M0, 10))
    saldo["v"] = Decimal(30)
    b.avanzar(tb._ms(tb.M0 + 2))
    trazas = cableado.TrazaBroker(limites=(("07-11", tb.M0 - 60, tb.M0 + 60),))
    motor = SimpleNamespace(trazas_broker={"2030-01-15": trazas}, brokers={"2030-01-15": b})
    lineas = cableado._informe_ordenes(motor)  # type: ignore[arg-type]
    assert any(f"| rechazada | {MOTIVO_MARGEN_LIBRE} |" in ln for ln in lineas)
    assert f"2030-01 | {MOTIVO_MARGEN_LIBRE} | llenar | 1" in lineas


# ------------------------------------------------------ la reubicacion (ADR-0074), mismo cierre


def _contexto_para_reubicar(registro: Registro) -> tuple[ContextoDia, Broker]:
    """El cableado a mano, con el perfil real: la cuenta, el broker con su saldo y tres zonas de
    compra en la misma entrada, sobre la ruta de `test_cableado` para una compra STOP (el precio
    esta por debajo de la entrada cuando se coloca)."""
    perfil = cargar_perfil(tc.PERFIL)
    md = tc._mercado(tc.RUTA_ORDEN_STOP)
    contrato = registro.decimal("instrumento_contrato")
    cuenta = CuentaViva(reglas_de_fase(perfil, "reto"), contrato, tc.MINUTO_INI * MS_POR_MINUTO - 1)
    broker = Broker(
        reglas_broker_de(perfil, registro),
        Configuracion(False, 0, lambda _m: tc.SPREAD),
        md.mercado(),
        contrato,
        md.escala,
        saldo=lambda: cuenta.saldo,
    )
    ctx = ContextoDia(broker, cuenta, contrato, md.escala)
    for i in (1, 2, 3):
        ctx.zonas[f"zona:{i}"] = cableado.zona_sintetica(
            f"zona:{i}", "compra", tc.ENTRADA, tc.EXTREMO, "primer_esquema"
        )
    ctx.instante_ms = tc.MINUTO_ZONA * MS_POR_MINUTO - 1
    return ctx, broker


def _preparar(ctx: ContextoDia, zona_id: str) -> None:
    """Lo que dejan RN-011 y RN-015 antes de colocar: la base del lotaje, el stop y el objetivo."""
    o = ctx.orden = OrdenEnPreparacion(ctx.zonas[zona_id])
    o.lotaje = ("hasta_stop_fraccion", Decimal("0.5"), "saldo_actual")
    o.stop = tc.ENTRADA - 16
    o.objetivo = tc.ENTRADA + 60


def test_en_la_reubicacion_la_cancelacion_libera_el_margen_antes_del_lote_nuevo_en_el_mismo_cierre(
    registro: Registro,
) -> None:
    """Respuesta del consultor a la PARADA, punto 3: en la reubicacion de ADR-0074 la cancelacion
    de la orden vieja libera su margen ANTES de calcular el lote de la nueva, en el mismo cierre.
    Por las primitivas reales y en el MISMO `instante_ms`: `colocar_orden_limite` coloca una stop
    que reserva margen; `reubicar_orden_limite` (con `orden_limite_nace` en
    `al_aparecer_punto_de_breaker`) la cancela y el margen usado vuelve a cero;
    `colocar_orden_limite` coloca la nueva con el margen libre ENTERO, asi que sale con el mismo
    lote que la primera. De control: una tercera colocada con la segunda viva ve menos margen libre
    y sale con menos lote."""
    assert orden_nace_en_el_punto(registro), "la reubicacion ya no cancela: el test no aplica"
    ctx, broker = _contexto_para_reubicar(registro)
    primitivas = primitivas_cableadas(registro, ctx, None, STOP_EN_RUPTURA)
    colocar = primitivas.acciones["colocar_orden_limite"]
    reubicar = primitivas.acciones["reubicar_orden_limite"]
    momento = Momento(MinutoUtc(tc.MINUTO_ZONA), "07-11", False, None)
    estado = EstadoDia(broker=broker.hechos())

    _preparar(ctx, "zona:1")
    colocar({"en": "Z"}, {"Z": "zona:1"}, momento, estado)
    o1 = broker.ordenes["o1"]
    assert o1.estado == COLOCADA and o1.tipo == TIPO_STOP
    reserva = broker.margen_usado()
    assert reserva > 0
    anotacion_1 = ctx.margen_al_colocar["o1"]
    assert anotacion_1[4] == "margen"  # el 0,5 % sobre 16 puntos no cabe a 1:30

    # el mismo cierre de M1: la caja se recalcula y RN-006 reubica, que con la orden en el punto
    # CANCELA (ADR-0074) y refresca los hechos para que RN-011 y RN-015 vuelvan a colocar
    reubicar({"a": "Z", "cadencia": "reubicacion_cadencia"}, {"Z": "zona:2"}, momento, estado)
    assert broker.ordenes["o1"].estado == CANCELADA
    assert broker.margen_usado() == 0
    assert estado.broker[HECHO_ORDEN_PENDIENTE] is False

    _preparar(ctx, "zona:2")
    colocar({"en": "Z"}, {"Z": "zona:2"}, momento, estado)
    o2 = broker.ordenes["o2"]
    anotacion_2 = ctx.margen_al_colocar["o2"]
    assert o2.estado == COLOCADA
    assert anotacion_2[1] == anotacion_1[1]  # el margen libre entero: la reserva de o1 ya no esta
    assert o2.lotes == o1.lotes

    # de control, sin cancelar: la tercera ve el margen libre menos la reserva de la segunda
    _preparar(ctx, "zona:3")
    colocar({"en": "Z"}, {"Z": "zona:3"}, momento, estado)
    o3 = broker.ordenes["o3"]
    anotacion_3 = ctx.margen_al_colocar["o3"]
    assert anotacion_3[1] is not None and anotacion_2[1] is not None
    assert anotacion_3[1] < anotacion_2[1] and o3.lotes < o2.lotes
