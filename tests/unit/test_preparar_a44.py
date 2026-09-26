"""RN-020 lista para activarse con la respuesta a A-44 (rama trabajo/preparar-a35-a44): el tope
propio del trader con tres estados -SIN FIJAR (se niega nombrando A-44), SIN_TOPE (RN-020 nunca
bloquea) y un valor concreto-, independiente de los limites de la firma; cada alcance y cada
unidad; el reinicio con el huso del parametro (o el del perfil, marcado como SUPUESTO) en el borde
de la medianoche; con los dos limites activos se aplica el que se toque primero y la traza dice
cual; y el motor de la spec sin cuenta."""

from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.config.registro import Registro, cargar_registro
from botsito.engine import cableado, diagnostico, tope_trader
from botsito.engine.cuenta import EstadoCuenta
from botsito.engine.diagnostico import Diagnostico
from botsito.engine.interprete import Interprete, ReglaEjecutable
from botsito.engine.motor import MotorSpec
from botsito.engine.primitivas import primitivas_escritas
from botsito.engine.tope_trader import (
    AMBOS,
    DIA,
    EQUITY,
    ORIGEN_FIRMA,
    ORIGEN_TRADER,
    PORCENTAJE,
    SALDO,
    SEMANA,
    SIN_TOPE,
    SUPUESTO_HUSO,
    USD,
    SeguidorTope,
    TopeRechazadoError,
    TopeSinFijarError,
    TopeTrader,
    tope_del_registro,
)
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_preparar_a35 as ta35

RAIZ = Path(__file__).resolve().parents[2]
HUSO_PERFIL = ZoneInfo("Europe/Prague")  # el del perfil de FTMO (ADR-0050)
CAPITAL = Decimal(100_000)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(tc.SPEC)


@pytest.fixture(scope="module")
def reglas() -> list[ReglaEjecutable]:
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.spec.modelo import cargar_reglas

    return list(reglas_ejecutables(cargar_reglas(tc.SPEC)))


def _registro_sintetico(tmp_path: Path, **valores: str) -> Registro:
    """Un registro con los cuatro CONFIRMED de la sesion 1 y los seis de A-44 con los valores que
    se pidan (los demas, UNKNOWN)."""
    partes = [
        "parametros:",
        "  - nombre: perdida_maxima_diaria\n    categoria: estrategia\n    tipo: porcentaje\n"
        '    unidad: pct\n    descripcion: d\n    estado: CONFIRMED\n    valor: "4.5"\n'
        "    fuente: {tipo: feedback, id: fb-2026-09-09-sesion-01-bff260ea}",
        "  - nombre: perdida_maxima_semanal\n    categoria: estrategia\n    tipo: porcentaje\n"
        '    unidad: pct\n    descripcion: s\n    estado: CONFIRMED\n    valor: "9"\n'
        "    fuente: {tipo: feedback, id: fb-2026-09-09-sesion-01-a85b6bc7}",
        "  - nombre: base_calculo_perdida_diaria\n    categoria: estrategia\n    tipo: enum\n"
        "    unidad: base\n    opciones: [saldo_actual, saldo_inicial_dia]\n    descripcion: b\n"
        "    estado: CONFIRMED\n    valor: saldo_inicial_dia\n"
        "    fuente: {tipo: feedback, id: fb-2026-09-09-sesion-01-bff260ea}",
        "  - nombre: base_calculo_perdida_semanal\n    categoria: estrategia\n    tipo: enum\n"
        "    unidad: base\n    opciones: [saldo_actual, saldo_inicial_semana, saldo_inicial_dia]\n"
        "    descripcion: b\n    estado: CONFIRMED\n    valor: saldo_actual\n"
        "    fuente: {tipo: feedback, id: fb-2026-09-09-sesion-01-a85b6bc7}",
    ]
    fichas = {
        "perdida_trader_alcance": ("enum", "[sin_tope, dia, semana, ambos]"),
        "perdida_trader_magnitud": ("enum", "[saldo, equity]"),
        "perdida_trader_unidad": ("enum", "[porcentaje, usd]"),
        "perdida_trader_dia_usd": ("decimal", None),
        "perdida_trader_semana_usd": ("decimal", None),
        "perdida_trader_reinicio_huso": ("texto", None),
    }
    for nombre, (tipo, opciones) in fichas.items():
        ficha = (
            f"  - nombre: {nombre}\n    categoria: estrategia\n    tipo: {tipo}\n    unidad: u\n"
        )
        if opciones:
            ficha += f"    opciones: {opciones}\n"
        ficha += "    descripcion: x\n"
        if nombre in valores:
            ficha += (
                f'    estado: CONFIRMED\n    valor: "{valores[nombre]}"\n'
                "    fuente: {tipo: feedback, id: fb-2030-01-16-sesion-02-1a2b3c4d}"
            )
        else:
            ficha += "    estado: UNKNOWN"
        partes.append(ficha)
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text("\n".join(partes) + "\n", encoding="utf-8")
    return cargar_registro(ruta)


# ------------------------------------------------------------------------- los tres estados


def test_sin_fijar_se_niega_nombrando_a44_y_el_diagnostico_corre(registro: Registro) -> None:
    with pytest.raises(TopeSinFijarError, match="A-44") as exc:
        tope_del_registro(registro, HUSO_PERFIL)
    assert tope_trader.P_ALCANCE in str(exc.value) and "diagnostico" in str(exc.value)
    sin = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_SIN_TOPE))
    assert sin.alcance == SIN_TOPE and sin.diagnostico == "DIAGNOSTICO-A44-sin_tope"
    assert not sin.aplica_dia and not sin.aplica_semana and "sin_tope" in sin.descripcion()
    marcador = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_MARCADOR))
    assert marcador.alcance == AMBOS and marcador.unidad == USD and marcador.magnitud == EQUITY
    assert marcador.tope_dia == Decimal(1) and marcador.tope_semana == Decimal(1)
    assert marcador.huso_supuesto and marcador.huso_reinicio is HUSO_PERFIL
    assert "DIAGNOSTICO-A44-marcador" in marcador.descripcion()


def test_con_el_tope_fijado_el_diagnostico_se_rechaza_y_sin_tope_es_una_respuesta(
    tmp_path: Path,
) -> None:
    r = _registro_sintetico(tmp_path, perdida_trader_alcance=SIN_TOPE)
    t = tope_del_registro(r, HUSO_PERFIL)
    assert t.alcance == SIN_TOPE and t.diagnostico is None
    with pytest.raises(TopeRechazadoError, match="ya esta fijado"):
        tope_del_registro(r, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_SIN_TOPE))


@pytest.mark.parametrize(
    ("alcance", "unidad", "huso"),
    [
        (DIA, PORCENTAJE, None),
        (SEMANA, USD, "Europe/Madrid"),
        (AMBOS, PORCENTAJE, "America/New_York"),
        (AMBOS, USD, None),
    ],
)
def test_cada_alcance_y_cada_unidad_se_leen_del_registro(
    tmp_path: Path, alcance: str, unidad: str, huso: str | None
) -> None:
    valores = {
        "perdida_trader_alcance": alcance,
        "perdida_trader_magnitud": SALDO,
        "perdida_trader_unidad": unidad,
        "perdida_trader_dia_usd": "1500",
        "perdida_trader_semana_usd": "3000",
    }
    if huso is not None:
        valores["perdida_trader_reinicio_huso"] = huso
    t = tope_del_registro(_registro_sintetico(tmp_path, **valores), HUSO_PERFIL)
    assert (t.alcance, t.unidad, t.magnitud) == (alcance, unidad, SALDO)
    assert t.aplica_dia == (alcance in (DIA, AMBOS)) and t.aplica_semana == (
        alcance in (SEMANA, AMBOS)
    )
    dia = (Decimal("4.5") if unidad == PORCENTAJE else Decimal(1500)) if t.aplica_dia else None
    semana = (Decimal(9) if unidad == PORCENTAJE else Decimal(3000)) if t.aplica_semana else None
    assert (t.tope_dia, t.tope_semana) == (dia, semana)
    assert (t.base_dia, t.base_semana) == ("saldo_inicial_dia", "saldo_actual")
    if huso is None:
        assert t.huso_supuesto and t.huso_reinicio is HUSO_PERFIL
        assert SUPUESTO_HUSO in t.descripcion()
    else:
        assert not t.huso_supuesto and t.huso_reinicio.key == huso
        assert SUPUESTO_HUSO not in t.descripcion()


# ------------------------------------------------------------------------- el seguidor


def _tope(
    alcance: str, unidad: str, magnitud: str = SALDO, huso: ZoneInfo = HUSO_PERFIL
) -> TopeTrader:
    return TopeTrader(
        alcance, magnitud, unidad,
        Decimal("4.5") if unidad == PORCENTAJE else Decimal(1500),
        Decimal(9) if unidad == PORCENTAJE else Decimal(3000),
        "saldo_inicial_dia", "saldo_actual", huso, False,
    )  # fmt: skip


def test_el_reinicio_corta_en_la_medianoche_de_su_huso_y_la_semana_el_lunes() -> None:
    """Praga en invierno es UTC+1: el dia corta a las 23:00Z. Una perdida a las 22:59Z cuenta en
    el dia; a las 23:00Z el conteo vuelve a cero; el domingo a lunes tambien corta la semana."""
    s = SeguidorTope(_tope(AMBOS, USD), datetime(2030, 1, 12, 8, tzinfo=UTC), CAPITAL)  # sabado
    s.avanzar(datetime(2030, 1, 12, 22, 59, tzinfo=UTC), CAPITAL - 700)
    a = s.acumuladores(CAPITAL - 700, CAPITAL - 700)
    assert a["perdida_dia"] == Decimal(700) and a["perdida_semana"] == Decimal(700)
    assert a["perdida_dia:tope"] == Decimal(1500) and a["perdida_semana:tope"] == Decimal(3000)
    s.avanzar(datetime(2030, 1, 12, 23, 0, tzinfo=UTC), CAPITAL - 700)  # medianoche de Praga
    a = s.acumuladores(CAPITAL - 700, CAPITAL - 700)
    assert a["perdida_dia"] == Decimal(0) and a["perdida_semana"] == Decimal(700)
    assert [c for _, c in s.cortes] == [DIA]
    s.avanzar(datetime(2030, 1, 13, 23, 0, tzinfo=UTC), CAPITAL - 900)  # domingo -> lunes
    a = s.acumuladores(CAPITAL - 900, CAPITAL - 900)
    assert a["perdida_dia"] == Decimal(0) and a["perdida_semana"] == Decimal(0)
    assert [c for _, c in s.cortes] == [DIA, DIA, SEMANA]
    # y con el huso de Madrid en verano seria otra hora: el corte es del huso del parametro
    s2 = SeguidorTope(
        _tope(DIA, USD, huso=ZoneInfo("Europe/Madrid")),
        datetime(2030, 7, 10, 8, tzinfo=UTC),
        CAPITAL,
    )
    s2.avanzar(datetime(2030, 7, 10, 21, 59, tzinfo=UTC), CAPITAL - 100)
    assert s2.acumuladores(CAPITAL - 100, CAPITAL - 100)["perdida_dia"] == Decimal(100)
    s2.avanzar(datetime(2030, 7, 10, 22, 0, tzinfo=UTC), CAPITAL - 100)
    assert s2.acumuladores(CAPITAL - 100, CAPITAL - 100)["perdida_dia"] == Decimal(0)


def test_alcances_unidades_y_magnitud_en_el_seguidor() -> None:
    t0 = datetime(2030, 1, 15, 8, tzinfo=UTC)
    solo_dia = SeguidorTope(_tope(DIA, PORCENTAJE), t0, CAPITAL)
    a = solo_dia.acumuladores(CAPITAL - 4500, CAPITAL - 4500)
    assert set(a) == {"perdida_dia", "perdida_dia:tope"} and a["perdida_dia"] == Decimal("4.5")
    solo_semana = SeguidorTope(_tope(SEMANA, PORCENTAJE), t0, CAPITAL)
    a = solo_semana.acumuladores(CAPITAL - 9000, CAPITAL - 9000)
    assert set(a) == {"perdida_semana", "perdida_semana:tope"}
    # base saldo_actual: 9.000 sobre 91.000 de saldo actual, no sobre el corte
    assert a["perdida_semana"] == Decimal(9000) / Decimal(91000) * 100
    assert (
        SeguidorTope(_tope(SIN_TOPE, PORCENTAJE), t0, CAPITAL).acumuladores(CAPITAL, CAPITAL) == {}
    )
    # equity frente a saldo: con una posicion abierta perdiendo, solo `equity` lo ve
    por_saldo = SeguidorTope(_tope(AMBOS, USD, SALDO), t0, CAPITAL).acumuladores(
        CAPITAL, CAPITAL - 2000
    )
    por_equity = SeguidorTope(_tope(AMBOS, USD, EQUITY), t0, CAPITAL).acumuladores(
        CAPITAL, CAPITAL - 2000
    )
    assert por_saldo["perdida_dia"] == Decimal(0) and por_equity["perdida_dia"] == Decimal(2000)
    # una ganancia no es una perdida negativa: recortada en cero
    assert (
        SeguidorTope(_tope(DIA, USD), t0, CAPITAL).acumuladores(CAPITAL + 500, CAPITAL + 500)[
            "perdida_dia"
        ]
        == 0
    )


# ------------------------------------------------------------------------- el motor cableado


# La limite se llena en MINUTO_ZONA+3 (el ask cruza la entrada) y la posicion queda cinco puntos
# en perdida; tres minutos despues, el hueco de 2.000 puntos que suspende la cuenta de la firma.
RUTA_TRADER_PRIMERO = {tc.MINUTO_ZONA + 3: tc.ENTRADA - 5, tc.MINUTO_ZONA + 6: tc.ENTRADA - 2000}


def _motor_con_tope(
    registro: Registro,
    vocabulario: dict[str, dict[str, Any]],
    ruta: dict[int, int],
    tope: TopeTrader,
) -> cableado.MotorCableado:
    motor = tc._motor(registro, vocabulario, tc._mercado(ruta))
    # la estrategia sintetica deja los acumuladores del trader al cableado real: solo cartuchos
    motor.acumuladores_extra = {"cartuchos": motor.acumuladores_extra["cartuchos"]}
    motor.tope = tope
    return motor


def test_sin_tope_rn020_no_bloquea_ni_es_hueco(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    tope = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_SIN_TOPE))
    motor = _motor_con_tope(registro, vocabulario, tc.RUTA_STOP, tope)
    r = motor.correr_dia(tc._dia())
    traza = r.sesiones["07-11"]
    assert "RN-020" not in traza.disparadas
    assert not any(p.startswith("acumulador:perdida_") for _, p in traza.no_implementadas)
    assert not any(
        h.startswith("acumulador:perdida_") for h in motor.trazas_broker[tc.DIA.isoformat()].huecos
    )
    assert r.operaciones and motor.primero_en_tocar is None
    assert (
        "TOPE DEL TRADER (RN-020, A-44): tope del trader: sin_tope"
        in cableado.informe_simulacion(motor)
    )


def test_con_un_valor_concreto_rn020_prohibe_al_cierre_de_m1_siguiente_a_la_perdida(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El marcador (un dolar sobre la equity): la posicion se llena en MINUTO_ZONA+3 y el precio
    la deja en perdida; RN-020 dispara en el primer cierre de M1 que ve la perdida y fija
    `detenido_por_tope`; la traza dice que el primer limite tocado fue el del trader."""
    tope = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_MARCADOR))
    motor = _motor_con_tope(registro, vocabulario, tc.RUTA_STOP, tope)
    r = motor.correr_dia(tc._dia())
    traza = r.sesiones["07-11"]
    assert "RN-020" in traza.disparadas
    hechos = {(t, h, v) for t, _, h, v in traza.fijados if h == "detenido_por_tope"}
    assert hechos and all(v == "hasta_el_corte_siguiente" for _, _, v in hechos)
    assert min(t for t, _, _ in hechos) > tc.MINUTO_ZONA + 3
    assert motor.primero_en_tocar is not None and motor.primero_en_tocar[0] == ORIGEN_TRADER
    assert motor.primero_en_tocar[1] == "perdida_dia"
    informe = cableado.informe_simulacion(motor)
    assert "PRIMERO EN TOCAR UN LIMITE: trader (perdida_dia)" in informe
    assert "DIAGNOSTICO-A44-marcador" in informe


def test_independiente_de_la_firma_se_aplica_el_que_se_toque_primero_y_la_traza_lo_dice(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """El hueco de 2.000 puntos suspende la cuenta de la firma. Con el marcador del trader, el
    tope del trader se toca ANTES (la posicion queda en perdida tres minutos antes del hueco) y la
    traza lo dice, con el instante de la peor marca; con sin_tope, la primera en tocarse es la
    firma, en el instante exacto del tick."""
    marcador = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_MARCADOR))
    motor = _motor_con_tope(registro, vocabulario, RUTA_TRADER_PRIMERO, marcador)
    motor.correr_dia(tc._dia())
    assert motor.cuenta is not None and motor.cuenta.estado is EstadoCuenta.SUSPENDIDA
    assert motor.primero_en_tocar is not None
    origen, cual, ms = motor.primero_en_tocar
    firma_ms = int(motor.cuenta.instante.timestamp() * 1000) if motor.cuenta.instante else None
    assert (
        origen == ORIGEN_TRADER and cual == "perdida_dia" and firma_ms is not None and ms < firma_ms
    )
    sin = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_SIN_TOPE))
    motor2 = _motor_con_tope(registro, vocabulario, RUTA_TRADER_PRIMERO, sin)
    motor2.correr_dia(tc._dia())
    assert motor2.primero_en_tocar is not None and motor2.primero_en_tocar[0] == ORIGEN_FIRMA
    assert motor2.cuenta is not None and motor2.cuenta.instante is not None
    assert motor2.primero_en_tocar[2] == int(motor2.cuenta.instante.timestamp() * 1000)
    assert "PRIMERO EN TOCAR UN LIMITE: firma" in cableado.informe_simulacion(motor2)
    # los limites de la firma no cambian con el tope del trader: mismo instante de suspension
    assert motor.cuenta.instante == motor2.cuenta.instante


def test_sin_tope_fijado_ni_diagnostico_sigue_siendo_hueco_con_nombre(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor_con_tope(registro, vocabulario, tc.RUTA_STOP, None)  # type: ignore[arg-type]
    r = motor.correr_dia(tc._dia())
    assert ("RN-020", "acumulador:perdida_dia") in r.sesiones["07-11"].no_implementadas
    assert "acumulador:perdida_dia" in motor.trazas_broker[tc.DIA.isoformat()].huecos
    assert "sin fijar: hueco con nombre" in cableado.informe_simulacion(motor)


# ------------------------------------------------------------------------- el motor de la spec


def test_el_motor_de_la_spec_sin_cuenta_evalua_rn020_con_tope_y_sin_el_es_hueco(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    voc = cargar_vocabulario(tc.SPEC)
    datos = ta35._datos(registro, "cierre_vela_contraria")
    sin = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_SIN_TOPE))
    r = MotorSpec(Interprete(voc, primitivas_escritas(registro, sin)), reglas).correr_dia(
        ta35._dia(datos)
    )
    faltan = {p for _, p in r.sesiones["07-11"].no_implementadas}
    assert "acumulador:perdida_dia" not in faltan and "RN-020" not in r.sesiones["07-11"].disparadas
    marcador = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_MARCADOR))
    r = MotorSpec(Interprete(voc, primitivas_escritas(registro, marcador)), reglas).correr_dia(
        ta35._dia(datos)
    )
    assert "RN-020" not in r.sesiones["07-11"].disparadas  # sin operaciones no hay perdida
    r = MotorSpec(Interprete(voc, primitivas_escritas(registro)), reglas).correr_dia(
        ta35._dia(datos)
    )
    assert "acumulador:perdida_dia" in {p for _, p in r.sesiones["07-11"].no_implementadas}


def test_el_marcador_cero_se_alcanza_sin_perder_nada_y_rn020_bloquea_de_punta_a_punta(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], reglas: list[ReglaEjecutable]
) -> None:
    """Fase 3d de la verificacion: un marcador que SI se alcanza en construccion aunque el bot no
    opere (tope cero). En el motor de la spec RN-020 dispara en cada sesion y fija
    `detenido_por_tope`; en el motor cableado, ademas, `abrir_operacion` queda prohibido y la
    estrategia sintetica no coloca ninguna orden. No es un valor plausible de nadie."""
    cero = tope_del_registro(registro, HUSO_PERFIL, Diagnostico(a44=diagnostico.A44_MARCADOR_CERO))
    assert cero.tope_dia == Decimal(0) and cero.diagnostico == "DIAGNOSTICO-A44-marcador_cero"
    voc = cargar_vocabulario(tc.SPEC)
    datos = ta35._datos(registro, "cierre_vela_contraria")
    r = MotorSpec(Interprete(voc, primitivas_escritas(registro, cero)), reglas).correr_dia(
        ta35._dia(datos)
    )
    for nombre, traza in r.sesiones.items():
        assert "RN-020" in traza.disparadas, nombre
        assert ("detenido_por_tope", "hasta_el_corte_siguiente") in {
            (h, v) for _, _, h, v in traza.fijados
        }, nombre
    motor = _motor_con_tope(registro, vocabulario, tc.RUTA_STOP, cero)
    r2 = motor.correr_dia(tc._dia())
    traza = r2.sesiones["07-11"]
    assert "RN-020" in traza.disparadas and not r2.operaciones
    assert any(b[1] == "accion:colocar_orden_limite" for b in traza.bloqueadas)
    assert motor.primero_en_tocar is not None and motor.primero_en_tocar[0] == ORIGEN_TRADER


def test_la_cli_se_niega_sin_a44_aunque_a35_vaya_en_diagnostico(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli

    real = cargar_criterio(RAIZ)
    salida = tmp_path / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", real.construccion[0], "--salida",
         str(salida), "--diagnostico-a35", "inicio_vela_contraria"]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert codigo == 2 and "A-44" in err and tope_trader.P_ALCANCE in err
    assert not list(tmp_path.iterdir())
