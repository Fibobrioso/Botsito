"""La ventana que FTMO prohibe antes de un cierre de mercado largo (rama
`feature/cierres-de-mercado`, ADR-0068), rompiendo la guardia a proposito: el viernes con el
calendario real de FTMO, un festivo con cierre anticipado SINTETICO, el cambio de hora del ultimo
domingo de octubre, el dia normal, y el predicado desactivado. Sin cobertura agregada: nada aqui
mira un caso ni una operacion del trader."""

from __future__ import annotations

import logging
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import cargar_registro
from botsito.domain.cierres import (
    MOTIVO_CIERRE,
    MOTIVO_SIN_CALENDARIO,
    CalendarioCierres,
    Cierre,
    CierresError,
    FuenteCierres,
    ReglasCierres,
    cierres_desde_sesiones,
    juntar_cierres,
    proxima_prohibicion,
    unir_cierres,
    ventana_prohibida_por_cierre,
)
from botsito.domain.ticks import MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.engine import broker as modulo_broker
from botsito.engine.broker import (
    CANCELADA,
    LLENADA,
    PETICION_CANCELAR,
    PETICION_COLOCAR,
    Broker,
    Orden,
    Rechazo,
    ReglasBroker,
)
from botsito.engine.calendario_cierres import (
    CalendarioError,
    cargar_calendario,
    ruta_calendario,
)
from botsito.engine.llenado import Configuracion, Mercado
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.simulacion import reglas_broker_de

RAIZ = Path(__file__).resolve().parents[2]
PERFIL = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
REGISTRO = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
FTMO = cargar_calendario(ruta_calendario(RAIZ, "ftmo-2step-swing-100k")).calendario()
PERFIL_FTMO = cargar_perfil(PERFIL)
MARGEN = PERFIL_FTMO.minutos("firma_gap_margen_minutos") * 60_000
MINIMO = PERFIL_FTMO.minutos("firma_gap_cierre_minimo_minutos") * 60_000
MADRID = ZoneInfo("Europe/Madrid")
SPREAD = 3
UNO = Decimal(1)
BID = 1_000_000
UN_MS = 1


def _ms(
    anio: int, mes: int, dia: int, hora: int = 0, minuto: int = 0, segundo: int = 0,
    huso: ZoneInfo | None = None,
) -> int:  # fmt: skip
    instante = datetime(anio, mes, dia, hora, minuto, segundo, tzinfo=huso or UTC)
    return int(instante.timestamp() * 1000)


def _tick(ms: int, bid: int = BID) -> Tick:
    return Tick(MilisegundoUtc(ms), Puntos(bid + SPREAD), Puntos(bid), 0, 0)


def _broker(
    calendario: CalendarioCierres | None,
    ticks: list[Tick],
    cancelar_pendientes: bool = True,
) -> Broker:
    cierres = (
        ReglasCierres(calendario, MARGEN, MINIMO, cancelar_pendientes)
        if calendario is not None
        else None
    )
    reglas = ReglasBroker(
        volumen_max_lotes=Decimal(10),
        ordenes_simultaneas_max=10_000,
        posiciones_dia_max=10_000,
        huso_corte=ZoneInfo("Europe/Prague"),
        comision_por_lote=Decimal(0),
        comision_por_lado=False,
        swap_largo_puntos=Decimal(0),
        swap_corto_puntos=Decimal(0),
        mensajes_dia_max=2000,
        cierres=cierres,
    )
    return Broker(reglas, Configuracion(False, 0, lambda _m: SPREAD), Mercado(ticks, []), UNO, 1)


def _compra(b: Broker, id: str, instante_ms: int, precio: int = BID - 1000) -> Orden | Rechazo:
    return b.colocar_limite(id, "compra", precio, UNO, precio - 100, precio + 300, instante_ms)


def _calendario(*cierres: Cierre, desde: int, hasta: int) -> CalendarioCierres:
    return CalendarioCierres(juntar_cierres(cierres), desde, hasta)


# ------------------------------------------------------------- el viernes, con el calendario real

# el viernes 25-9-2026: EURUSD cierra en FTMO a las 20:55 UTC (16:55 de Nueva York, API de simbolos)
CIERRE_VIERNES = _ms(2026, 9, 25, 20, 55)
VENTANA_VIERNES = CIERRE_VIERNES - MARGEN  # 18:55 UTC, las 20:55 de Madrid


def test_el_margen_y_el_minimo_son_las_dos_horas_de_r15() -> None:
    """R15: «two hours or less before a relevant financial market is closed for at least two
    hours». El perfil y el registro dicen lo mismo."""
    assert MARGEN == MINIMO == 2 * 3_600_000
    for nombre in ("firma_gap_margen_minutos", "firma_gap_cierre_minimo_minutos"):
        assert REGISTRO.minutos(nombre) == PERFIL_FTMO.minutos(nombre)


def test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_justo_antes() -> None:
    b = _broker(FTMO, [_tick(VENTANA_VIERNES - 60_000)])
    antes = _compra(b, "o1", VENTANA_VIERNES - UN_MS)
    dentro = _compra(b, "o2", VENTANA_VIERNES)
    al_final = _compra(b, "o3", CIERRE_VIERNES - UN_MS, precio=BID - 2000)
    assert isinstance(antes, Orden)
    assert isinstance(dentro, Rechazo) and dentro.motivo == MOTIVO_CIERRE
    assert isinstance(al_final, Rechazo) and al_final.motivo == MOTIVO_CIERRE
    # lo negado no existe, no llega al servidor y no se cuenta
    assert "o2" not in b.ordenes and "o3" not in b.ordenes
    assert [p.id for p in b.traza().peticiones if p.tipo == PETICION_COLOCAR] == ["o1"]
    assert [(c.id, c.motivo) for c in b.traza().cierres if c.tipo == PETICION_COLOCAR] == [
        ("o2", MOTIVO_CIERRE),
        ("o3", MOTIVO_CIERRE),
    ]


def test_en_madrid_la_ventana_del_viernes_cae_lejos_de_la_operativa() -> None:
    """De las 20:55 a las 22:55 de Madrid: la operativa (07:00-15:00) no la toca."""
    assert datetime.fromtimestamp(VENTANA_VIERNES / 1000, MADRID).strftime("%H:%M") == "20:55"
    for minuto in range(
        _ms(2026, 9, 25, 7, 0, huso=MADRID), _ms(2026, 9, 25, 15, 0, huso=MADRID), 60_000
    ):
        assert ventana_prohibida_por_cierre(minuto, FTMO, MARGEN, MINIMO) is None


def test_con_el_mercado_cerrado_tampoco_se_coloca_y_al_abrir_si() -> None:
    abre = _ms(2026, 9, 27, 21, 5)
    p = ventana_prohibida_por_cierre(abre - UN_MS, FTMO, MARGEN, MINIMO)
    assert p is not None and p.motivo == MOTIVO_CIERRE and p.ventana_desde_ms == VENTANA_VIERNES
    assert ventana_prohibida_por_cierre(abre, FTMO, MARGEN, MINIMO) is None


def test_la_pendiente_puesta_antes_se_cancela_al_empezar_la_ventana() -> None:
    """`cierre_pendientes` = cancelar (PROVISIONAL bajo A-55): al empezar la ventana el broker la
    cancela, y es una peticion que protege la cuenta. Aunque el precio la toque en ese mismo
    instante, la cancelacion va primero."""
    ticks = [_tick(VENTANA_VIERNES - 60_000), _tick(VENTANA_VIERNES, BID - 1500)]
    b = _broker(FTMO, ticks)
    orden = _compra(b, "o1", VENTANA_VIERNES - 30_000)
    assert isinstance(orden, Orden)
    b.avanzar(VENTANA_VIERNES + 60_000)
    assert orden.estado == CANCELADA and not b.posiciones
    assert (VENTANA_VIERNES, CANCELADA, "o1") in [(m, t, i) for m, t, i, _ in b.traza().eventos]
    assert [p.tipo for p in b.traza().peticiones] == [PETICION_COLOCAR, PETICION_CANCELAR]
    assert [(c.tipo, c.motivo) for c in b.traza().cierres] == [(PETICION_CANCELAR, MOTIVO_CIERRE)]


def test_con_mantener_la_pendiente_sigue_y_se_llena_dentro() -> None:
    ticks = [_tick(VENTANA_VIERNES - 60_000), _tick(VENTANA_VIERNES + 60_000, BID - 1500)]
    b = _broker(FTMO, ticks, cancelar_pendientes=False)
    orden = _compra(b, "o1", VENTANA_VIERNES - 30_000)
    b.avanzar(VENTANA_VIERNES + 120_000)
    assert isinstance(orden, Orden) and orden.estado == LLENADA


def test_modificar_una_pendiente_dentro_se_niega_y_la_deja_como_estaba() -> None:
    b = _broker(FTMO, [_tick(VENTANA_VIERNES - 60_000)], cancelar_pendientes=False)
    orden = _compra(b, "o1", VENTANA_VIERNES - 30_000)
    assert isinstance(orden, Orden)
    r = b.modificar("o1", VENTANA_VIERNES + 1000, precio=BID - 1500)
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_CIERRE
    assert orden.precio == BID - 1000


def test_una_posicion_abierta_sigue_y_su_stop_se_mueve() -> None:
    """R7: Swing permite mantener posiciones el fin de semana. El predicado no cierra nada."""
    b = _broker(FTMO, [_tick(VENTANA_VIERNES - 60_000)])
    p = b.abrir_conocida("p1", "compra", BID, UNO, BID - 200, BID + 600, VENTANA_VIERNES - 1000)
    b.mover_stop("p1", BID, VENTANA_VIERNES + 1000)
    b.avanzar(CIERRE_VIERNES)
    assert p.abierta and p.stop == BID


def test_cada_bloqueo_va_al_log_con_su_motivo(caplog: pytest.LogCaptureFixture) -> None:
    b = _broker(FTMO, [_tick(VENTANA_VIERNES - 60_000)])
    with caplog.at_level(logging.INFO, logger="botsito.engine.broker"):
        _compra(b, "o1", VENTANA_VIERNES + 1000)
    mensajes = [r.getMessage() for r in caplog.records]
    assert len(mensajes) == 1
    assert "colocar o1" in mensajes[0] and MOTIVO_CIERRE in mensajes[0]


# ------------------------------------------------------- un festivo con cierre anticipado sintetico

# miercoles 17-7-2030, verano: un cierre anticipado inventado a las 14:00 de Madrid (12:00 UTC)
DESDE_2030, HASTA_2030 = _ms(2030, 7, 1), _ms(2030, 8, 1)
ANTICIPADO = Cierre(_ms(2030, 7, 17, 12, 0), _ms(2030, 7, 18, 21, 5), "sintetico")
DIARIO = Cierre(_ms(2030, 7, 16, 20, 55), _ms(2030, 7, 16, 21, 5), "diario")
FESTIVO = _calendario(ANTICIPADO, DIARIO, desde=DESDE_2030, hasta=HASTA_2030)


def test_un_cierre_anticipado_mete_la_ventana_en_la_operativa() -> None:
    """Cierra a las 14:00 de Madrid: de 12:00 a 14:00 no se coloca, y a las 11:59:59.999 si."""
    ventana = ANTICIPADO.inicio_ms - MARGEN
    b = _broker(FESTIVO, [_tick(ventana - 60_000)])
    assert isinstance(_compra(b, "o1", ventana - UN_MS), Orden)
    r = _compra(b, "o2", ventana)
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_CIERRE
    assert datetime.fromtimestamp(ventana / 1000, MADRID).strftime("%H:%M") == "12:00"


def test_un_cierre_corto_no_bloquea_nada() -> None:
    """El corte diario de 10 minutos no es largo: ni antes ni durante."""
    for t in range(DIARIO.inicio_ms - MARGEN, DIARIO.fin_ms + 60_000, 60_000):
        assert ventana_prohibida_por_cierre(t, FESTIVO, MARGEN, MINIMO) is None


def test_los_bordes_de_r15_van_dentro() -> None:
    """«two hours or less» y «at least two hours»: un cierre de exactamente 2 h cuenta, y su
    ventana empieza exactamente 2 h antes; uno de 2 h menos un milisegundo no cuenta."""
    justo = Cierre(_ms(2030, 7, 10, 12), _ms(2030, 7, 10, 14), "justo")
    corto = Cierre(_ms(2030, 7, 11, 12), _ms(2030, 7, 11, 14) - UN_MS, "corto")
    cal = _calendario(justo, corto, desde=DESDE_2030, hasta=HASTA_2030)
    assert ventana_prohibida_por_cierre(justo.inicio_ms - MARGEN, cal, MARGEN, MINIMO) is not None
    assert (
        ventana_prohibida_por_cierre(justo.inicio_ms - MARGEN - UN_MS, cal, MARGEN, MINIMO) is None
    )
    assert ventana_prohibida_por_cierre(corto.inicio_ms - 1000, cal, MARGEN, MINIMO) is None


# ---------------------------------------------------------- el cambio de hora de octubre


def _calendario_con_octubre(tmp_path: Path) -> CalendarioCierres:
    """El calendario de FTMO con `cubre` alargado hasta noviembre de 2026, sintetico, para ver el
    cambio de hora; y un cierre inventado el domingo 25-10 a las 04:00 de Madrid."""
    texto = ruta_calendario(RAIZ, "ftmo-2step-swing-100k").read_text(encoding="utf-8")
    texto = texto.replace('hasta: "2026-10-07"', 'hasta: "2026-11-30"')
    texto = texto.replace(
        "extraordinarios:\n",
        "extraordinarios:\n"
        '  - inicio: {fecha: "2026-10-25", hora: "04:00", huso: Europe/Madrid}\n'
        '    fin: {fecha: "2026-10-25", hora: "09:00", huso: Europe/Madrid}\n'
        "    fuente: sintetico, para el test del cambio de hora\n",
    )
    carpeta = tmp_path / "cierres"
    carpeta.mkdir()
    ruta = carpeta / "ftmo-2step-swing-100k.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return cargar_calendario(ruta).calendario()


def _ventana_del_viernes(cal: CalendarioCierres, viernes: int) -> int:
    p = proxima_prohibicion(viernes, viernes + 86_400_000, cal, MARGEN, MINIMO)
    assert p is not None
    return p


def test_el_cambio_de_hora_de_octubre_no_mueve_la_ventana_de_mas(tmp_path: Path) -> None:
    """El 25-10-2026 Europa pasa a invierno y Nueva York no hasta el 1-11. El cierre del servidor
    es 16:55 de Nueva York: en UTC, 20:55 hasta el 30-10 y 21:55 desde el 6-11. En Madrid la
    ventana va de 20:55 (23-10), a 19:55 (30-10), a 20:55 (6-11). Siempre 2 h de reloj absoluto."""
    cal = _calendario_con_octubre(tmp_path)
    esperadas = {
        (2026, 10, 23): (_ms(2026, 10, 23, 18, 55), "20:55"),
        (2026, 10, 30): (_ms(2026, 10, 30, 18, 55), "19:55"),
        (2026, 11, 6): (_ms(2026, 11, 6, 19, 55), "20:55"),
    }
    for (a, m, d), (inicio, en_madrid) in esperadas.items():
        ventana = _ventana_del_viernes(cal, _ms(a, m, d))
        assert ventana == inicio
        assert datetime.fromtimestamp(ventana / 1000, MADRID).strftime("%H:%M") == en_madrid
        p = ventana_prohibida_por_cierre(ventana, cal, MARGEN, MINIMO)
        assert p is not None and p.cierre is not None
        assert p.cierre.inicio_ms - ventana == 2 * 3_600_000


def test_un_cierre_justo_despues_del_cambio_tiene_dos_horas_absolutas(tmp_path: Path) -> None:
    """El 25-10-2026 a la 01:00 UTC Madrid vuelve de las 03:00 a las 02:00. Un cierre a las 03:30
    de Madrid (ya en invierno, 02:30 UTC) abre su ventana a las 00:30 UTC, que en la pared de
    Madrid son las 02:30 de VERANO (la primera vez que se marcan). Restar dos horas en la pared
    -03:30 menos dos, la 01:30- la pondria una hora antes: eso es lo que no puede pasar."""
    cal = _calendario_con_octubre(tmp_path)
    inicio_cierre = _ms(2026, 10, 25, 3, 30, huso=MADRID)
    assert inicio_cierre == _ms(2026, 10, 25, 2, 30)
    # el fin de semana ya esta cerrado: se mira en un calendario solo con ese cierre
    solo = _calendario(
        Cierre(inicio_cierre, inicio_cierre + 5 * 3_600_000, "sintetico"),
        desde=cal.cubre_desde_ms,
        hasta=cal.cubre_hasta_ms,
    )
    ventana = inicio_cierre - MARGEN
    assert ventana == _ms(2026, 10, 25, 0, 30)
    assert ventana_prohibida_por_cierre(ventana - UN_MS, solo, MARGEN, MINIMO) is None
    assert ventana_prohibida_por_cierre(ventana, solo, MARGEN, MINIMO) is not None
    pared = datetime.fromtimestamp(ventana / 1000, MADRID)
    assert (pared.strftime("%H:%M"), pared.utcoffset()) == ("02:30", timedelta(hours=2))
    en_la_pared = _ms(2026, 10, 25, 1, 30, huso=MADRID)  # 03:30 menos dos horas de pared
    assert en_la_pared == ventana - 3_600_000
    assert ventana_prohibida_por_cierre(en_la_pared, solo, MARGEN, MINIMO) is None
    # el sintetico del YAML se une al fin de semana, y la union dice de donde sale cada trozo
    assert any("extraordinario 2026-10-25" in c.fuente.split(" + ") for c in cal.cierres)


# --------------------------------------------------------------------------- un dia normal


def test_un_dia_normal_no_bloquea_nada() -> None:
    """Miercoles 23-9-2026, con el calendario real: ni la operativa ni el corte diario bloquean."""
    for t in range(_ms(2026, 9, 23, 0, 0), _ms(2026, 9, 24, 0, 0), 60_000):
        assert ventana_prohibida_por_cierre(t, FTMO, MARGEN, MINIMO) is None
    b = _broker(FTMO, [_tick(_ms(2026, 9, 23, 4, 59))])
    for i, t in enumerate(range(_ms(2026, 9, 23, 5), _ms(2026, 9, 23, 13), 3_600_000)):
        assert isinstance(_compra(b, f"o{i}", t, precio=BID - 1000 - i), Orden)
    assert b.traza().cierres == ()


# --------------------------------------------------------------- el calendario y sus fuentes


def test_fuera_de_lo_que_cubre_el_calendario_no_se_coloca() -> None:
    despues = FTMO.cubre_hasta_ms
    b = _broker(FTMO, [_tick(despues - 60_000)])
    r = _compra(b, "o1", despues)
    assert isinstance(r, Rechazo) and r.motivo == MOTIVO_SIN_CALENDARIO
    p = ventana_prohibida_por_cierre(FTMO.cubre_desde_ms - UN_MS, FTMO, MARGEN, MINIMO)
    assert p is not None and p.motivo == MOTIVO_SIN_CALENDARIO


def test_el_calendario_de_ftmo_trae_navidad_y_ano_nuevo_y_cubre_la_construccion() -> None:
    largos = [c for c in FTMO.cierres if c.duracion_ms >= MINIMO]
    inicios = {datetime.fromtimestamp(c.inicio_ms / 1000, UTC).date().isoformat() for c in largos}
    assert {"2025-12-24", "2025-12-31"} <= inicios  # miercoles, por el 25 y el 1
    assert FTMO.cubre_desde_ms <= _ms(2026, 4, 1) and _ms(2026, 9, 1) <= FTMO.cubre_hasta_ms
    # ningun cierre largo empieza antes de las 17:00 de Madrid en dia laborable
    for c in largos:
        local = datetime.fromtimestamp(c.inicio_ms / 1000, MADRID)
        assert local.weekday() >= 5 or local.hour >= 17, local


def test_gana_la_mas_restrictiva_y_la_discrepancia_se_dice() -> None:
    """Las sesiones de la plataforma (sinteticas) traen un cierre anticipado que el calendario no
    tiene: la union lo toma, y sale como discrepancia."""
    s1 = (_ms(2026, 9, 27, 21, 5), _ms(2026, 9, 28, 13, 0))
    s2 = (_ms(2026, 9, 28, 21, 5), _ms(2026, 9, 29, 20, 55))
    vivos = cierres_desde_sesiones([s2, s1], "plataforma")
    assert vivos == (Cierre(s1[1], s2[0], "plataforma"),)
    unidos, discrepancias = unir_cierres(
        [
            FuenteCierres("calendario", FTMO.cierres, FTMO.cubre_desde_ms, FTMO.cubre_hasta_ms),
            FuenteCierres("plataforma", vivos, s1[0], s2[1]),
        ],
        MINIMO,
    )
    cal = CalendarioCierres(unidos, FTMO.cubre_desde_ms, FTMO.cubre_hasta_ms)
    p = ventana_prohibida_por_cierre(s1[1] - MARGEN, cal, MARGEN, MINIMO)
    assert p is not None and p.motivo == MOTIVO_CIERRE
    assert ventana_prohibida_por_cierre(s1[1] - MARGEN, FTMO, MARGEN, MINIMO) is None
    assert [(d.de, d.falta_en) for d in discrepancias] == [("plataforma", "calendario")]


@pytest.mark.parametrize(
    ("viejo", "nuevo", "dice"),
    [
        ("perfil: ftmo-2step-swing-100k", "perfil: otro", "perfil"),
        ("huso: America/New_York}", "huso: Nueva_York}", "huso"),
        ('hasta: "2026-10-07"', 'hasta: "2025-01-01"', "hasta"),
        (
            "    fuente: >-\n      Trading Update del 18-dic",
            "    nota: >-\n      Trading Update del 18-dic",
            "fuente",
        ),
    ],
)
def test_un_calendario_mal_escrito_no_se_carga(
    tmp_path: Path, viejo: str, nuevo: str, dice: str
) -> None:
    texto = ruta_calendario(RAIZ, "ftmo-2step-swing-100k").read_text(encoding="utf-8")
    assert viejo in texto
    ruta = tmp_path / "ftmo-2step-swing-100k.yaml"
    ruta.write_text(texto.replace(viejo, nuevo, 1), encoding="utf-8")
    with pytest.raises(CalendarioError, match=dice):
        cargar_calendario(ruta)


def test_un_calendario_con_cierres_sin_unir_no_se_arma() -> None:
    a = Cierre(_ms(2030, 7, 1, 10), _ms(2030, 7, 1, 12), "a")
    b = Cierre(_ms(2030, 7, 1, 11), _ms(2030, 7, 1, 13), "b")
    with pytest.raises(CierresError):
        CalendarioCierres((a, b), DESDE_2030, HASTA_2030)


def test_las_reglas_salen_del_perfil_del_registro_y_del_calendario() -> None:
    reglas = reglas_broker_de(PERFIL_FTMO, REGISTRO, FTMO)
    assert reglas.cierres == ReglasCierres(FTMO, MARGEN, MINIMO, True)
    assert REGISTRO.opcion("cierre_pendientes") == "cancelar"
    assert reglas_broker_de(PERFIL_FTMO, REGISTRO).cierres is None


# ------------------------------------------------- con el predicado desactivado, los tests fallan


def test_sin_el_predicado_el_viernes_se_coloca_dentro(monkeypatch: pytest.MonkeyPatch) -> None:
    """La guardia rota a proposito: si el predicado no prohibe nada, la compra dentro de la ventana
    del viernes SALE. Es lo que hace fallar `test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_
    justo_antes`: el unico que la niega es el predicado."""
    monkeypatch.setattr(modulo_broker, "ventana_prohibida_por_cierre", lambda *_a, **_k: None)
    b = _broker(FTMO, [_tick(VENTANA_VIERNES - 60_000)])
    assert isinstance(_compra(b, "o2", VENTANA_VIERNES), Orden)
    with pytest.raises(AssertionError):
        test_un_viernes_no_se_coloca_dentro_de_la_ventana_y_si_justo_antes()
    with pytest.raises(AssertionError):
        test_un_cierre_anticipado_mete_la_ventana_en_la_operativa()
