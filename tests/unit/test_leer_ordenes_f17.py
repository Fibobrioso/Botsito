"""El lector de la medida de las ordenes stop y del grabador (`scripts/leer_ordenes_f17.py`, rama
`trabajo/f17-ordenes`, D5): datos sinteticos, y cada regla de D3 rompe a proposito.

Lo que pide D5, cada uno con su test: el tick que dispara de una compra se busca en el ASK y el de
una venta en el BID (con un caso donde el otro lado daria otro tick); un llenado sin tick sale
`sin_tick` y no entra en la mediana; una clase con mas del 5 % de `sin_tick` no da veredicto; con la
mediana «bot» 1 punto por encima de la «uno» manda «bot» y la clase sale «insuficiente»; el
percentil de la clase es el mayor entre el de «uno» y el maximo de «bot»; una muestra fuera de la
ventana no entra. Y lo de la respuesta a la PARADA: `al_colocar` (punto 8), los bordes `(puesta,
llenado]` (punto 9) y `bot_reducido` (punto 2)."""

from __future__ import annotations

import importlib.util
import sys
from datetime import UTC, date, datetime
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "scripts" / "leer_ordenes_f17.py"


def _modulo() -> ModuleType:
    spec = importlib.util.spec_from_file_location("leer_ordenes_f17", GUION)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["leer_ordenes_f17"] = modulo  # lo pide @dataclass al crear la clase
    spec.loader.exec_module(modulo)
    return modulo


L = _modulo()
C = L.cargar_criterio_ordenes(RAIZ)


class RelojIdentidad:
    """El servidor en UTC: para los tests que no miran el reloj."""

    def a_utc(self, servidor_ms: int) -> int:
        return servidor_ms


def siempre(_: int) -> bool:
    return True


def nunca(_: int) -> bool:
    return False


def T(msc: int, bid: int, ask: int) -> Any:  # noqa: N802
    return L.Tick(msc, bid, ask)


def fila(**k: str) -> dict[str, str]:
    base = {c: "" for c in L.COLUMNAS_MEDIDA}
    base.update({"fila": "1", "estrato": "uno", "lotes": "1.00", "lote_d2": "1.00"})
    base.update(k)
    return base


# ------------------------------------------------------------------ el criterio, leido del yaml


def test_el_criterio_sale_del_yaml_y_de_criterio_fidelidad() -> None:
    assert C.sin_tick_maximo == Fraction(5, 100)
    assert (C.minimo_uno, C.minimo_bot, C.bot_si_el_lote_importa) == (100, 30, 100)
    assert C.diferencia_que_importa == 1
    assert C.fraccion_lote_d2 == Fraction(9, 10)
    assert C.percentil == 90


# ----------------------------------------------------------------------- el tick que dispara


def test_la_compra_se_busca_en_el_ask_y_la_venta_en_el_bid() -> None:
    """Ticks (bid, ask) en los que el otro lado tocaria antes (no son cotizaciones reales: solo
    separan los dos lados)."""
    ticks = [T(20, 100, 99), T(30, 99, 100)]
    # compra con nivel 100: el ASK llega en el 30; por el BID habria sido el 20
    assert L.tick_que_dispara(ticks, "compra", 100, 0, 50) == T(30, 99, 100)
    # venta con nivel 99: el BID llega en el 30; por el ASK habria sido el 20
    assert L.tick_que_dispara(ticks, "venta", 99, 0, 50) == T(30, 99, 100)


def test_un_lado_cambiado_daria_otro_tick(monkeypatch: pytest.MonkeyPatch) -> None:
    """Rompe a proposito: con los lados cambiados (la compra al BID), el tick es el 20."""
    ticks = [T(20, 100, 99), T(30, 99, 100)]
    monkeypatch.setattr(L, "ejecuta_al_ask", lambda lado: lado == "venta")
    assert L.tick_que_dispara(ticks, "compra", 100, 0, 50) == T(20, 100, 99)


def test_los_bordes_son_la_puesta_fuera_y_el_llenado_dentro() -> None:
    ticks = [T(10, 99, 100), T(20, 99, 100)]
    assert L.tick_que_dispara(ticks, "compra", 100, 10, 20) == T(20, 99, 100)  # el 10 es la puesta
    assert L.tick_que_dispara(ticks, "compra", 100, 9, 20) == T(10, 99, 100)
    assert L.tick_que_dispara(ticks, "compra", 100, 10, 19) is None  # el 20 pasa del llenado


def test_el_deslizamiento_es_mas_en_contra() -> None:
    assert L.deslizamiento("compra", 102, 100) == 2  # compro mas caro
    assert L.deslizamiento("venta", 98, 100) == 2  # vendo mas barato
    assert L.deslizamiento("compra", 99, 100) == -1
    with pytest.raises(L.OrdenesError):
        L.deslizamiento("larga", 1, 1)


# ----------------------------------------------------------------------------- las muestras


def _entrada(lado: str = "compra", **k: str) -> dict[str, str]:
    campos = {
        "evento": "llenado",
        "clase": "entrada_stop",
        "lado": lado,
        "nivel": "1.00100",
        "precio": "1.00102",
        "instante_msc": "100",
        "puesta_msc": "50",
        "cot_bid": "1.00090",
        "cot_ask": "1.00095",
        "cot_msc": "40",
    }
    campos.update(k)
    return fila(**campos)


def test_una_entrada_en_puntos() -> None:
    ticks = [T(60, 100090, 100100), T(100, 100095, 100101)]
    m = L.muestra_de(_entrada(), ticks, 5, siempre, RelojIdentidad(), C)
    assert (m.estado, m.valor, m.estrato) == ("ok", 2, "uno")  # 100102 - 100100


def test_sin_tick_no_entra_en_la_mediana() -> None:
    m = L.muestra_de(_entrada(), [T(60, 100090, 100099)], 5, siempre, RelojIdentidad(), C)
    assert (m.estado, m.valor) == ("sin_tick", None)
    r = L.Resumen()
    r.anadir(m)
    r.anadir(L.Muestra("entrada_stop", "uno", 3, "ok", 0))
    assert (r.n, r.sin_tick, r.valores) == (1, 1, [3])


def test_una_entrada_que_llega_ya_pasada_es_al_colocar() -> None:
    """Punto 8: la cotizacion antes de colocar ya tocaba el nivel; o un tick entre esa lectura y la
    puesta. No entra en la mediana ni en sin_tick."""
    pasada = _entrada(cot_ask="1.00100")
    m = L.muestra_de(pasada, [T(100, 100095, 100101)], 5, siempre, RelojIdentidad(), C)
    assert (m.estado, m.valor) == ("al_colocar", None)
    entre = [T(45, 100095, 100100), T(100, 100095, 100101)]
    m = L.muestra_de(_entrada(), entre, 5, siempre, RelojIdentidad(), C)
    assert m.estado == "al_colocar"
    r = L.Resumen()
    r.anadir(m)
    assert (r.n, r.sin_tick, r.al_colocar) == (0, 0, 1)


def test_un_cierre_a_mercado_usa_la_cotizacion_previa() -> None:
    f = fila(
        evento="llenado",
        clase="cierre_mercado",
        lado="venta",
        precio="1.00090",
        instante_msc="100",
        puesta_msc="95",
        cot_bid="1.00092",
        cot_ask="1.00094",
        cot_msc="90",
    )
    m = L.muestra_de(f, [], 5, siempre, RelojIdentidad(), C)
    assert (m.estado, m.valor) == ("ok", 2)  # vende a 90 con el BID en 92


def test_un_cierre_por_stop_de_una_compra_vende_al_bid() -> None:
    f = fila(
        evento="llenado",
        clase="cierre_stop",
        lado="venta",
        nivel="1.00082",
        precio="1.00080",
        instante_msc="200",
        puesta_msc="100",
    )
    ticks = [T(100, 100080, 100082), T(150, 100083, 100081), T(180, 100081, 100083)]
    m = L.muestra_de(f, ticks, 5, siempre, RelojIdentidad(), C)
    # el 100 es la puesta (fuera); el 150 toca por el ASK (81), no por el BID (83); el 180, BID 81
    assert (m.estado, m.valor) == ("ok", 1)


def test_fuera_de_la_ventana_no_entra() -> None:
    m = L.muestra_de(_entrada(), [T(60, 100090, 100100)], 5, nunca, RelojIdentidad(), C)
    assert (m.estado, m.valor) == ("fuera_de_ventana", None)
    r = L.Resumen()
    r.anadir(m)
    assert (r.n, r.fuera_de_ventana) == (0, 1)


def test_bot_reducido_por_debajo_del_90_por_ciento() -> None:
    assert L.estrato_de(fila(estrato="bot", lotes="22.50", lote_d2="25.00"), C) == "bot"
    assert L.estrato_de(fila(estrato="bot", lotes="22.49", lote_d2="25.00"), C) == "bot_reducido"
    assert L.estrato_de(fila(estrato="uno"), C) == "uno"


# ------------------------------------------------------------------------------ el veredicto


def _r(valores: list[int], sin_tick: int = 0) -> Any:
    r = L.Resumen()
    r.valores = list(valores)
    r.sin_tick = sin_tick
    return r


def test_con_lo_minimo_vale_uno_y_el_percentil_es_el_mayor() -> None:
    """El percentil de la clase es el mayor entre el p90 de «uno» y el maximo de «bot»."""
    uno = _r([0] * 90 + [1] * 10)  # p90 0 o 1, mediana 0
    bot = _r([0] * 29 + [5])  # mediana 0, maximo 5
    v = L.veredicto("entrada_stop", uno, bot, C)
    assert (v.estado, v.estrato, v.mediana, v.percentil) == ("valido", "uno", 0, 5)
    bot_bajo = _r([0] * 30)
    v = L.veredicto("entrada_stop", uno, bot_bajo, C)
    assert v.percentil == L.percentil(sorted(uno.valores), 0.9)


def test_con_la_mediana_bot_un_punto_mas_manda_bot_e_insuficiente() -> None:
    uno = _r([0] * 100)
    bot = _r([1] * 30)
    v = L.veredicto("cierre_stop", uno, bot, C)
    assert (v.estado, v.estrato) == ("insuficiente", "bot")
    v = L.veredicto("cierre_stop", uno, _r([1] * 100), C)
    assert (v.estado, v.estrato, v.mediana) == ("valido", "bot", 1)


def test_mas_del_5_por_ciento_sin_tick_no_da_veredicto() -> None:
    uno = _r([0] * 100, sin_tick=6)  # 6 de 106: 5,7 %
    v = L.veredicto("entrada_stop", uno, _r([0] * 30), C)
    assert v.estado == "sin_veredicto"
    uno = _r([0] * 100, sin_tick=5)  # 5 de 105: 4,8 %
    assert L.veredicto("entrada_stop", uno, _r([0] * 30), C).estado == "valido"


def test_con_menos_del_minimo_es_insuficiente() -> None:
    assert L.veredicto("cierre_mercado", _r([0] * 99), _r([0] * 30), C).estado == "insuficiente"
    assert L.veredicto("cierre_mercado", _r([0] * 100), _r([0] * 29), C).estado == "insuficiente"


# --------------------------------------------------------------- de punta a punta, con main()


def _escribir(ruta: Path, cabecera: str, filas: list[str]) -> None:
    ruta.write_bytes(("\r\n".join([cabecera, *filas]) + "\r\n").encode("cp1252"))


def _ms_servidor_en_ventana(hora: str) -> int:
    """El instante del servidor de las `hora` nominales del 2026-12-02 (un miercoles)."""
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.config.registro import cargar_registro
    from botsito.engine.relojes import reloj_de_las_sesiones

    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    minuto = int(reloj_de_las_sesiones(registro).instante(date(2026, 12, 2), hora))
    return int(L.RelojServidor.del_registro(registro).a_servidor(minuto * 60_000))


def test_main_lee_la_medida_y_no_imprime_precios(tmp_path: Path) -> None:
    dentro = _ms_servidor_en_ventana("10:00")
    fuera = _ms_servidor_en_ventana("20:00")
    cab = ",".join(L.COLUMNAS_MEDIDA)

    def linea(**k: str) -> str:
        f = fila(**k)
        return ",".join(f[c] for c in L.COLUMNAS_MEDIDA)

    filas = [
        linea(evento="contexto", clase="digits", motivo="5"),
        linea(
            evento="llenado",
            clase="entrada_stop",
            lado="compra",
            nivel="1.17100",
            precio="1.17102",
            instante_msc=str(dentro),
            puesta_msc=str(dentro - 1000),
            cot_bid="1.17090",
            cot_ask="1.17095",
            cot_msc=str(dentro - 1500),
            ticks_fichero="F17M_ticks_1.csv",
        ),
        linea(
            evento="llenado",
            clase="entrada_stop",
            lado="compra",
            nivel="1.17100",
            precio="1.17101",
            instante_msc=str(fuera),
            puesta_msc=str(fuera - 1000),
            cot_bid="1.17090",
            cot_ask="1.17095",
            cot_msc=str(fuera - 1500),
            ticks_fichero="F17M_ticks_2.csv",
        ),
        linea(evento="tope", clase="b_dia", motivo="salta"),
    ]
    _escribir(tmp_path / "F17M_uno_20261202_100000.csv", cab, filas)
    _escribir(
        tmp_path / "F17M_ticks_1.csv", "time_msc,bid,ask,flags", [f"{dentro},1.17095,1.17100,6"]
    )
    _escribir(
        tmp_path / "F17M_ticks_2.csv", "time_msc,bid,ask,flags", [f"{fuera},1.17095,1.17100,6"]
    )
    salida = tmp_path / "salida.txt"
    assert L.main(["medida", str(tmp_path), "--salida", str(salida)], raiz=RAIZ) == 0
    texto = salida.read_text(encoding="utf-8")
    assert (
        "entrada_stop · uno: n 1; mediana 2, p90 2, max 2; sin_tick 0; al_colocar 0; "
        "fuera de ventana 1" in texto
    )
    assert "VEREDICTO entrada_stop: insuficiente" in texto
    assert "tope 1" in texto
    assert "1.171" not in texto  # ningun precio


def test_main_lee_el_grabador(tmp_path: Path) -> None:
    dentro = _ms_servidor_en_ventana("10:00")
    _escribir(
        tmp_path / "F17G_control_20261202_090000.csv", "clave,valor,nota", ['"digits","5",""']
    )
    _escribir(
        tmp_path / "F17G_2026-12-02_11.csv",
        "time_msc,bid,ask,flags",
        [f"{dentro},1.17095,1.17100,6", f"{dentro + 10},1.17095,1.17097,6"],
    )
    salida = tmp_path / "salida.txt"
    assert L.main(["grabador", str(tmp_path), "--salida", str(salida)], raiz=RAIZ) == 0
    texto = salida.read_text(encoding="utf-8")
    assert "GRABADOR: 2 ticks leidos; 1 dias con ticks en la ventana" in texto
    assert "spread FTMO 10:00: n 2, p50 2, p90 5, p99 5, max 5" in texto
    assert "1.170" not in texto


def test_una_clase_desconocida_no_se_adivina() -> None:
    with pytest.raises(L.OrdenesError):
        L.muestra_de(
            fila(evento="llenado", clase="cierre_tp", lado="venta", precio="1.0", instante_msc="1"),
            [],
            5,
            siempre,
            RelojIdentidad(),
            C,
        )


def test_el_reloj_pasa_a_utc_con_el_registro() -> None:
    """El instante del servidor pasa a UTC con RelojServidor, del registro (sin cifras aqui)."""
    ms = _ms_servidor_en_ventana("10:00")
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.config.registro import cargar_registro

    reloj = L.RelojServidor.del_registro(
        cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    )
    utc = datetime.fromtimestamp(reloj.a_utc(ms) / 1000, tz=UTC)
    assert utc.date() == date(2026, 12, 2)
    assert reloj.a_utc(ms) < ms  # el servidor va por delante de UTC
