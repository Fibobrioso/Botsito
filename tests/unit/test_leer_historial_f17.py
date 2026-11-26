"""El lector del historial de ticks de FTMO (`scripts/leer_historial_f17.py`, rama
`trabajo/f17-historial`): el reloj del servidor a UTC a los dos lados de los cambios de hora de
EE. UU. y de Europa, la negativa a meses que no son de construccion, los dias, y los puntos (a) a
(d2) del criterio, con datos sinteticos. Varios rompen a proposito.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from collections.abc import Set as AbstractSet
from datetime import UTC, date, datetime
from decimal import InvalidOperation
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from botsito.cases.relojes import RelojSesiones

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "scripts" / "leer_historial_f17.py"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("leer_historial_f17", GUION)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["leer_historial_f17"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


L = _cargar()
MS = 60_000


def _ms(texto: str) -> int:
    return int(datetime.fromisoformat(texto).replace(tzinfo=UTC).timestamp() * 1000)


class _Registro:
    def __init__(self, base: int, dst: str) -> None:
        self._base, self._dst = base, dst

    def minutos(self, nombre: str) -> int:
        assert nombre == "broker_offset_base"
        return self._base

    def opcion(self, nombre: str) -> str:
        assert nombre == "broker_dst"
        return self._dst


def _reloj(dst: str) -> Any:
    # la base de las pruebas no es la del registro: el lector la lee, no la lleva dentro
    return L.RelojServidor.del_registro(_Registro(120, dst))


# --- el reloj del servidor -----------------------------------------------------------------


@pytest.mark.parametrize(
    ("dst", "antes", "despues", "d_antes", "d_despues"),
    [
        # Fechas de 2027, un año sin meses reservados (revisor, a4). EE. UU. adelanta el
        # 14-mar-2027 y atrasa el 7-nov-2027
        ("us", "2027-03-12T12:00", "2027-03-15T12:00", 120, 180),
        ("us", "2027-11-05T12:00", "2027-11-08T12:00", 180, 120),
        # Europa adelanta el 28-mar-2027 y atrasa el 31-oct-2027: con `us` no cambia nada
        ("us", "2027-03-26T12:00", "2027-03-29T12:00", 180, 180),
        ("us", "2027-10-29T12:00", "2027-11-01T12:00", 180, 180),
        ("eu", "2027-03-26T12:00", "2027-03-29T12:00", 120, 180),
        ("eu", "2027-10-29T12:00", "2027-11-01T12:00", 180, 120),
        ("eu", "2027-03-12T12:00", "2027-03-15T12:00", 120, 120),
        ("ninguno", "2027-07-15T12:00", "2027-12-15T12:00", 120, 120),
    ],
)
def test_el_reloj_a_los_dos_lados_de_cada_cambio(
    dst: str, antes: str, despues: str, d_antes: int, d_despues: int
) -> None:
    r = _reloj(dst)
    for texto, desfase in ((antes, d_antes), (despues, d_despues)):
        utc = _ms(texto)
        assert r.desfase_minutos(utc) == desfase
        servidor = r.a_servidor(utc)
        assert servidor - utc == desfase * MS
        assert r.a_utc(servidor) == utc


@pytest.mark.parametrize(
    ("dst", "repetida_a", "repetida_b", "salto_antes", "salto_despues", "inexistente"),
    [
        # `us`: el 7-nov-2027 las 01:30 de Nueva York existen dos veces (05:30 y 06:30 UTC) y el
        # servidor marca las 08:30 en los dos; el 14-mar-2027, de las 08:59 a las 10:00 del
        # servidor no hay nada (06:59 y 07:00 UTC)
        (
            "us",
            "2027-11-07T05:30",
            "2027-11-07T06:30",
            "2027-03-14T06:59",
            "2027-03-14T07:00",
            "2027-03-14T09:30",
        ),
        # `eu` (revisor, b7): el 31-oct-2027 las 01:30 de Londres existen dos veces (00:30 y
        # 01:30 UTC), y el servidor marca las 03:30 en los dos; el 28-mar-2027, de las 02:59 a
        # las 04:00 del servidor no hay nada (00:59 y 01:00 UTC)
        (
            "eu",
            "2027-10-31T00:30",
            "2027-10-31T01:30",
            "2027-03-28T00:59",
            "2027-03-28T01:00",
            "2027-03-28T03:30",
        ),
    ],
)
def test_la_hora_repetida_y_la_que_no_existe_fallan_con_nombre(
    dst: str,
    repetida_a: str,
    repetida_b: str,
    salto_antes: str,
    salto_despues: str,
    inexistente: str,
) -> None:
    r = _reloj(dst)
    assert r.a_servidor(_ms(repetida_a)) == r.a_servidor(_ms(repetida_b))
    with pytest.raises(L.HistorialError, match="se repite"):
        r.a_utc(r.a_servidor(_ms(repetida_a)))
    assert r.a_servidor(_ms(salto_despues)) - r.a_servidor(_ms(salto_antes)) == 61 * MS
    with pytest.raises(L.HistorialError, match="no existe"):
        r.a_utc(_ms(inexistente))


def test_un_calendario_desconocido_no_se_adivina() -> None:
    with pytest.raises(L.HistorialError, match="no es un calendario"):
        L.RelojServidor.del_registro(_Registro(120, "asia"))


def test_el_reloj_no_lleva_ninguna_cifra_del_registro() -> None:
    """Rompe si alguien escribe el desfase en el codigo en lugar de leerlo (ADR-0002)."""
    import re

    codigo = GUION.read_text(encoding="utf-8")
    assert not re.search(r"(?<![\w.])(120|180)(?![\w.])", codigo)


def test_el_control_cuadra_o_no_con_el_registro() -> None:
    """Rompe a proposito (revisor, b4): el 3-nov-2027 Europa ya esta en invierno y EE. UU. todavia
    en verano. Un servidor que diga 120 cuadra con `eu` y NO con `us`, y uno que diga 180 al reves:
    la comparacion del lector discrimina el calendario."""
    gmt = str(_ms("2027-11-03T10:00") // 1000)
    con_120 = {"time_gmt_s": gmt, "desfase_servidor_gmt_min": "120"}
    con_180 = {"time_gmt_s": gmt, "desfase_servidor_gmt_min": "180"}
    assert L.control_cuadra(con_180, _reloj("us")) == (180, 180)
    assert L.control_cuadra_con_registro(con_180, _reloj("us"))
    assert not L.control_cuadra_con_registro(con_120, _reloj("us"))
    assert L.control_cuadra_con_registro(con_120, _reloj("eu"))
    assert not L.control_cuadra_con_registro(con_180, _reloj("eu"))


def test_las_filas_de_otro_mes_utc_se_descartan_sin_leer_su_precio(tmp_path: Path) -> None:
    """Respuesta a la PARADA 3, punto 0. Rompe a proposito: en el fichero del 1 de abril, un tick y
    una M1 de la ultima hora UTC del 31 de marzo (el dia del servidor empieza antes que el UTC) no
    entran en ninguna cuenta y si en el recuento de descartes, por su mes. Su precio es ilegible a
    proposito: si el lector lo leyera, fallaria. En 2027, un año sin meses reservados (revisor, a4):
    el borde es el mismo, el servidor va tres horas por delante de UTC."""
    r = _reloj("us")
    borde = r.a_servidor(_ms("2027-03-31T23:30"))  # 02:30 del 1-abr en el servidor
    dentro = r.a_servidor(_ms("2027-04-01T10:00"))
    ticks = tmp_path / "F17_2027-04-01_ticks.csv"
    ticks.write_bytes(
        (
            f"time_msc,bid,ask,flags\r\n{borde},ilegible,ilegible,6\r\n{dentro},1.17000,1.17002,6\r\n"
        ).encode("cp1252")
    )
    m1 = tmp_path / "F17_2027-04-01_m1.csv"
    m1.write_bytes(
        (
            "time,open,high,low,close,tick_volume,spread,real_volume\r\n"
            f"{borde // 1000},x,x,x,x,1,1,0\r\n"
            f"{dentro // 1000},1.17000,1.17001,1.16999,1.17000,4,2,0\r\n"
        ).encode("cp1252")
    )
    destino = L.TicksDelMes()
    descartes: Counter[str] = Counter()
    assert L.leer_ticks(ticks, r, 5, destino, "2027-04", descartes) == 1
    velas = L.leer_m1(m1, r, 5, "2027-04", descartes)
    assert sum(destino.por_minuto.values()) == 1
    assert list(destino.por_minuto) == [_ms("2027-04-01T10:00") // MS]
    assert list(velas) == [_ms("2027-04-01T10:00") // MS]
    assert descartes == Counter({"ticks del 2027-03": 1, "M1 del 2027-03": 1})
    # sin `mes`, el lector leeria el precio ilegible y fallaria: el descarte va antes de leerlo
    with pytest.raises(InvalidOperation):
        L.leer_ticks(ticks, r, 5, L.TicksDelMes())
    # y el recorrido de la carpeta (el que usa leer_historial) pasa el mes y lo dice en su linea
    ftmo, velas_mes, desc_mes = L.leer_mes_ftmo(tmp_path, "2027-04", r, 5)
    assert list(ftmo.por_minuto) == [_ms("2027-04-01T10:00") // MS]
    assert list(velas_mes) == [_ms("2027-04-01T10:00") // MS]
    assert desc_mes == descartes
    assert L.linea_descartes(desc_mes).endswith(
        "1 filas de M1 del 2027-03, 1 filas de ticks del 2027-03"
    )
    assert L.linea_descartes(Counter()).endswith(": ninguna")


def test_los_dias_sin_ticks_o_con_error_se_dicen() -> None:
    """Revisor, b5: un dia a medias (ERR_HISTORY_TIMEOUT) o vacio sale nombrado."""
    control = {
        "dia_2026-04-01_ticks": "1000",
        "dia_2026-04-01_error": "0",
        "dia_2026-04-02_ticks": "500",
        "dia_2026-04-02_error": "4403",
        "dia_2026-04-03_ticks": "0",
        "dia_2026-04-03_error": "0",
    }
    assert L.dias_incompletos(control) == [
        "2026-04-02 (ticks 500, error 4403)",
        "2026-04-03 (ticks 0, error 0)",
    ]


# --- la negativa ---------------------------------------------------------------------------

CONSTRUCCION = ("2026-04", "2026-07", "2026-08", "2026-01")


def test_decide_por_el_nombre_que_meses_lee() -> None:
    assert (
        L.comprobar_meses(
            [
                "F17_2026-04-15_ticks.csv",
                "F17_2026-01-02_m1.csv",
                "F17_control_20261201_101500.csv",
            ],
            CONSTRUCCION,
        )
        == []
    )
    assert L.comprobar_meses(
        ["F17_2026-02-10_ticks.csv", "F17_2026-03-02_m1.csv", "otro.csv"], CONSTRUCCION
    ) == ["F17_2026-02-10_ticks.csv", "F17_2026-03-02_m1.csv", "otro.csv"]


def test_se_niega_a_un_mes_que_no_es_de_construccion_sin_leerlo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Rompe a proposito: un fichero de febrero (heredado 6) con bytes que no se pueden leer; el
    lector sale con 2 antes de abrirlo."""
    carpeta = tmp_path / "historial"
    carpeta.mkdir()
    (carpeta / "F17_2026-04-15_ticks.csv").write_bytes(b"time_msc,bid,ask,flags\r\n")
    (carpeta / "F17_2026-02-10_ticks.csv").write_bytes(b"\xff\xfe no es un csv")
    salida = tmp_path / "salida.txt"
    assert L.main([str(carpeta), "--salida", str(salida)], raiz=RAIZ) == 2
    assert "F17_2026-02-10_ticks.csv" in capsys.readouterr().err
    assert not salida.exists()


# --- los dias ------------------------------------------------------------------------------

UTC_PARED = RelojSesiones.de_pared("UTC")


def _ms_dia(d: date, hhmm: str) -> int:
    return int(UTC_PARED.instante(d, hhmm)) * MS


def test_los_dias_son_los_laborables_menos_los_cierres_que_tocan_la_ventana() -> None:
    cubre = (_ms("2026-03-01T00:00"), _ms("2026-05-01T00:00"))
    # un cierre el miercoles 1-abr dentro de la ventana, y otro el jueves 2 despues de ella
    cierres = [
        (_ms_dia(date(2026, 4, 1), "09:00"), _ms_dia(date(2026, 4, 1), "10:00")),
        (_ms_dia(date(2026, 4, 2), "16:00"), _ms_dia(date(2026, 4, 2), "17:00")),
    ]
    dias = L.dias_del_mes("2026-04", UTC_PARED, "07:00", "15:00", cierres, cubre)
    fechas = [d.dia for d in dias]
    assert date(2026, 4, 1) not in fechas  # el cierre toca la ventana
    assert date(2026, 4, 2) in fechas  # el cierre cae fuera de ella
    assert all(f.weekday() < 5 for f in fechas)
    assert len(fechas) == 22 - 1  # abril de 2026 tiene 22 laborables
    assert all(d.hasta - d.desde == 8 * 60 for d in dias)


def test_un_dia_fuera_del_calendario_para() -> None:
    cubre = (_ms("2026-04-01T00:00"), _ms("2026-04-20T00:00"))
    with pytest.raises(L.HistorialError, match="no cubre"):
        L.dias_del_mes("2026-04", UTC_PARED, "07:00", "15:00", [], cubre)


# --- los puntos ----------------------------------------------------------------------------

CRITERIO = L.Criterio(
    a_minimo=Fraction(99, 100),
    b_umbral=5,
    b_maximo=3,
    b_hueco_maximo=30,
    c_tolerancia=2,
    c_minimo=Fraction(99, 100),
    d1_valores=3,
    d1_minimo=Fraction(95, 100),
    d2_fraccion=Fraction(1, 2),
)
DIA = date(2026, 4, 15)


def _dia() -> Any:
    return L.DiaVentana(
        DIA, int(UTC_PARED.instante(DIA, "07:00")), int(UTC_PARED.instante(DIA, "15:00"))
    )


def _lleno(dia: Any, sin: AbstractSet[int] = frozenset(), por_minuto: int = 4) -> Any:
    """Ticks en cada minuto de la ventana salvo `sin`, con spreads 1, 2, 3 y 4 que rotan."""
    t = L.TicksDelMes()
    for i, m in enumerate(dia.minutos()):
        if m in sin:
            continue
        for k in range(por_minuto):
            bid = 100_000 + i
            t.anadir(m * MS + k, bid, bid + 1 + (k % 4))
    return t


def _m1_de(t: Any) -> dict[int, Any]:
    return dict(t.m1)


def _horas(d: Any) -> frozenset[tuple[date, int]]:
    """Todas las horas UTC de la ventana de `d`, como si Dukascopy las tuviera descargadas."""
    return frozenset(L.hora_utc(m) for m in d.minutos())


def test_un_mes_lleno_cubre() -> None:
    d = _dia()
    t = _lleno(d)
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, _lleno(d), _horas(d))
    assert p.cumple(CRITERIO) == {"a": True, "b": True, "c": True, "d1": True, "d2": True}


def test_cada_punto_rompe_por_separado() -> None:
    """Rompe a proposito: cada punto falla con su causa, y solo el suyo."""
    d = _dia()
    minutos = list(d.minutos())
    # (a) y (b): un hueco de 31 minutos (y con el, menos del 99 % de minutos con tick)
    t = _lleno(d, sin=set(minutos[10:41]))
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, _lleno(d), _horas(d))
    assert p.hueco_maximo == 31 and not p.cumple(CRITERIO)["b"] and not p.cumple(CRITERIO)["a"]
    # (b) solo: cuatro huecos de 6 minutos, el 95 % de los minutos con tick
    sin = {m for i in range(4) for m in minutos[100 * i : 100 * i + 6]}
    t = _lleno(d, sin=sin)
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, _lleno(d), _horas(d))
    assert p.huecos_largos == 4 and not p.cumple(CRITERIO)["b"]
    # (c): la M1 del servidor corrida 3 puntos en todos los minutos
    t = _lleno(d)
    corrida = {
        m: L.Ohlc(o.abierta + 3, o.maxima + 3, o.minima + 3, o.cierre + 3) for m, o in t.m1.items()
    }
    assert not L.puntos_del_mes([d], t, corrida, UTC_PARED, CRITERIO, _lleno(d), _horas(d)).cumple(
        CRITERIO
    )["c"]
    # (d1): el spread siempre igual (como unos ticks fabricados de la M1 con su spread)
    plano = L.TicksDelMes()
    for m in minutos:
        for k in range(4):
            plano.anadir(m * MS + k, 100_000, 100_002)
    p = L.puntos_del_mes([d], plano, _m1_de(plano), UTC_PARED, CRITERIO, _lleno(d), _horas(d))
    assert p.cumple(CRITERIO) == {"a": True, "b": True, "c": True, "d1": False, "d2": True}
    # (d2): un tick por minuto frente a cuatro de Dukascopy
    t = _lleno(d, por_minuto=1)
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, _lleno(d, por_minuto=4), _horas(d))
    assert p.mediana_ticks_minuto == 1 and not p.cumple(CRITERIO)["d2"]


def test_d2_compara_solo_las_horas_que_dukascopy_tiene_descargadas() -> None:
    """PARADA 2, punto 0. Rompe a proposito (punto 1): unas horas con ticks densos en Dukascopy y
    escasos en FTMO dan «no cubre»; y las horas que Dukascopy no tiene descargadas no entran, ni
    como 0 ni comparadas."""
    d = _dia()
    minutos = list(d.minutos())
    primeras = minutos[: 4 * 60]  # Dukascopy solo tiene descargadas las cuatro primeras horas
    horas = frozenset(L.hora_utc(m) for m in primeras)
    duk = L.TicksDelMes()
    for m in primeras:
        for k in range(8):  # densos: 8 por minuto
            duk.anadir(m * MS + k, 100_000, 100_002 + k % 3)
    # FTMO escaso (2 por minuto) en esas horas: no cubre
    escaso = _lleno(d, por_minuto=2)
    p = L.puntos_del_mes([d], escaso, _m1_de(escaso), UTC_PARED, CRITERIO, duk, horas)
    assert (p.minutos_d2, p.mediana_ticks_minuto, p.mediana_ticks_minuto_dukascopy) == (240, 2, 8)
    assert p.cumple(CRITERIO) == {"a": True, "b": True, "c": True, "d1": False, "d2": False}
    # FTMO denso en esas horas y sin nada en las otras cuatro: (a) y (b) fallan, pero d2 cubre,
    # porque las horas sin descarga de Dukascopy no cuentan como 0 ni se comparan
    t = L.TicksDelMes()
    for m in primeras:
        for k in range(8):
            t.anadir(m * MS + k, 100_000, 100_001 + k % 4)
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, duk, horas)
    assert p.cumple(CRITERIO)["d2"] and not p.cumple(CRITERIO)["a"]
    # sin ninguna hora descargada, d2 no se puede evaluar: no cubre
    p = L.puntos_del_mes([d], t, _m1_de(t), UTC_PARED, CRITERIO, duk, frozenset())
    assert p.minutos_d2 == 0 and not p.cumple(CRITERIO)["d2"]


def test_las_horas_descargadas_salen_del_manifiesto() -> None:
    horas = L.horas_descargadas(["2026-07-01", "2026-07-02"], [5, 6], ["2026-07-02T06Z"])
    assert horas == frozenset({(date(2026, 7, 1), 5), (date(2026, 7, 1), 6), (date(2026, 7, 2), 5)})


def test_la_diferencia_mediana_es_la_mediana_de_las_diferencias_por_dia_hora() -> None:
    d = _dia()
    ftmo, duk = L.TicksDelMes(), L.TicksDelMes()
    for m in d.minutos():
        ftmo.anadir(m * MS, 100_000, 100_003)  # 3 puntos
        duk.anadir(m * MS, 100_000, 100_005)  # 5 puntos
    diferencia, global_ = L.diferencias_de_spread([d], ftmo, duk, UTC_PARED)
    assert (diferencia, global_) == (-2, -2)


def test_los_precios_pasan_a_puntos_exactos_y_el_csv_admite_crlf(tmp_path: Path) -> None:
    assert L.a_puntos("1.17345", 5) == 117345
    with pytest.raises(L.HistorialError, match="decimales"):
        L.a_puntos("1.173451", 5)
    ruta = tmp_path / "F17_control_20261201_101500.csv"
    ruta.write_bytes(b"clave,valor,nota\r\ndigits,5,\r\n")
    assert L.leer_control(ruta) == {"digits": "5"}
    ruta.write_bytes(b"clave,valor\r\n")
    with pytest.raises(L.HistorialError, match="columnas"):
        L.leer_control(ruta)
