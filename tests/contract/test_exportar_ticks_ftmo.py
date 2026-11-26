"""Contrato de `tools/mql5/ExportarTicksFTMO.mq5` (rama `trabajo/f17-historial`, D1): un script que
SOLO LEE el historial de ticks del servidor de una cuenta DEMO.

Se comprueba en el texto, como la capa (`test_capa_mt5.py`, de donde se toma la lista de funciones
de trading y como se quitan comentarios y textos): no llama a ninguna funcion de trading ni de
ordenes; lleva la condicion DEMO de `MedirDemoFTMO.mq5`:759, literal; su lista de meses es la
`construccion` de `criterio_fidelidad.yaml`; y en `OnStart` la negativa y la comprobacion del rango
van ANTES de la primera peticion de series (`CopyTicksRange`, `CopyRates`, `SeriesInfoInteger`).
Cada comprobacion rompe a proposito con un fuente mutado.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from tests.contract.test_capa_mt5 import llamadas_de_trading, sin_comentarios, sin_textos

RAIZ = Path(__file__).resolve().parents[2]
FUENTE = RAIZ / "tools" / "mql5" / "ExportarTicksFTMO.mq5"
MEDIR = RAIZ / "tools" / "mql5" / "MedirDemoFTMO.mq5"
LINEA_DEMO = 759
CONDICION_DEMO = (
    "if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)"
)
PETICIONES = ("CopyTicksRange", "CopyTicks", "CopyRates", "SeriesInfoInteger")


def _src() -> str:
    return FUENTE.read_text(encoding="utf-8")


def meses_del_fuente(src: str) -> list[str]:
    m = re.search(r"string\s+MESES_CONSTRUCCION\[\]\s*=\s*\{([^}]*)\}", sin_comentarios(src))
    if m is None:
        return []
    return re.findall(r'"(\d{4}-\d{2})"', m.group(1))


def cuerpo_de(src: str, nombre: str) -> str:
    """El cuerpo de la funcion `nombre` (sin comentarios), entre su `{` y la `}` que la cierra."""
    codigo = sin_comentarios(src)
    m = re.search(rf"\b{nombre}\s*\([^)]*\)\s*\{{", codigo)
    if m is None:
        return ""
    nivel, i = 0, m.end() - 1
    for j in range(i, len(codigo)):
        if codigo[j] == "{":
            nivel += 1
        elif codigo[j] == "}":
            nivel -= 1
            if nivel == 0:
                return codigo[i + 1 : j]
    return ""


def problemas(src: str, construccion: list[str]) -> list[str]:
    salida: list[str] = []
    trading = llamadas_de_trading(src)
    if trading:
        salida.append(f"llama a funciones de trading: {sorted(set(trading))}")
    if CONDICION_DEMO not in sin_comentarios(src):
        salida.append("no lleva la condicion DEMO de MedirDemoFTMO.mq5:759")
    if sorted(meses_del_fuente(src)) != sorted(construccion):
        salida.append(f"MESES_CONSTRUCCION no es {sorted(construccion)}")
    comprobaciones = cuerpo_de(src, "Comprobaciones")
    if CONDICION_DEMO not in comprobaciones:
        salida.append("Comprobaciones no empieza por la negativa DEMO")
    if "EsDeConstruccion" not in cuerpo_de(src, "RangoDeConstruccion"):
        salida.append("RangoDeConstruccion no comprueba los meses")
    onstart = sin_textos(cuerpo_de(src, "OnStart"))
    posiciones = [m.start() for p in PETICIONES for m in re.finditer(rf"\b{p}\s*\(", onstart)]
    llamadas = [m.start() for m in re.finditer(r"\b(Exportar\w+)\s*\(", onstart)]
    primera = min([*posiciones, *llamadas], default=len(onstart))
    for paso in ("Comprobaciones", "RangoDeConstruccion"):
        i = onstart.find(paso + "(")
        if i < 0 or i > primera:
            salida.append(f"OnStart no llama a {paso} antes de pedir nada")
    # el rango se cuenta por dias enteros: una entrada con hora no puede llegar al mes siguiente
    # (revisor de trabajo/f17-historial, b1)
    for entrada in ("InpDesde", "InpHasta"):
        if not re.search(rf"InicioDelDia\(\s*StringToTime\(\s*{entrada}\s*\)\s*\)", onstart):
            salida.append(f"OnStart no lleva {entrada} al inicio del dia")
    if "t-t%86400" not in re.sub(r"\s+", "", cuerpo_de(src, "InicioDelDia")):
        salida.append("InicioDelDia no corta a las 00:00 del dia")
    simbolos = set(re.findall(r'"([A-Z]{6})"', sin_comentarios(src)))
    if simbolos != {"EURUSD"}:
        salida.append(f"simbolos {sorted(simbolos)}: solo EURUSD")
    return salida


def test_la_condicion_demo_es_la_de_medir_demo_ftmo() -> None:
    assert MEDIR.read_text(encoding="utf-8").splitlines()[LINEA_DEMO - 1].strip() == CONDICION_DEMO


def test_el_exportador_cumple_el_contrato() -> None:
    assert problemas(_src(), list(cargar_criterio(RAIZ).construccion)) == []


def test_el_fuente_es_utf8_sin_bom_y_lf() -> None:
    b = FUENTE.read_bytes()
    assert not b.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in b
    b.decode("utf-8")


@pytest.mark.parametrize(
    ("viejo", "nuevo", "esperado"),
    [
        # una orden, aunque sea dentro de una funcion que no se llama
        (
            "bool EsDeConstruccion(",
            "void Enviar(){ MqlTradeRequest r; MqlTradeResult s; OrderSend(r, s); }\n"
            "bool EsDeConstruccion(",
            "llama a funciones de trading",
        ),
        (
            "bool EsDeConstruccion(",
            "#include <Trade\\Trade.mqh>\nbool EsDeConstruccion(",
            "trading",
        ),
        # febrero en la lista (heredado 6)
        ('"2026-08"};', '"2026-08", "2026-02"};', "MESES_CONSTRUCCION no es"),
        # la negativa DEMO quitada
        ("!= ACCOUNT_TRADE_MODE_DEMO)", "== ACCOUNT_TRADE_MODE_REAL)", "condicion DEMO"),
        # el rango sin comprobar los meses
        ("if(!EsDeConstruccion(d))", "if(false)", "no comprueba los meses"),
        # una peticion de series antes de la negativa
        (
            '   string motivo = "";\n   if(!Comprobaciones(motivo))',
            '   string motivo = "";\n'
            "   SeriesInfoInteger(SIMBOLO, PERIOD_M1, SERIES_SERVER_FIRSTDATE);\n"
            "   if(!Comprobaciones(motivo))",
            "antes de pedir nada",
        ),
        # una entrada con hora sin llevarla al inicio del dia (b1: «2026.08.31 06:00» llegaba al
        # 1-sep)
        (
            "datetime hasta = InicioDelDia(StringToTime(InpHasta));",
            "datetime hasta = StringToTime(InpHasta);",
            "InpHasta al inicio del dia",
        ),
        ("   return t - t % 86400;", "   return t;", "no corta a las 00:00"),
        # otro simbolo
        ('#define SIMBOLO        "EURUSD"', '#define SIMBOLO        "XAUUSD"', "solo EURUSD"),
    ],
)
def test_cada_regla_rompe_a_proposito(viejo: str, nuevo: str, esperado: str) -> None:
    src = _src()
    assert src.count(viejo) == 1, viejo
    malos = problemas(src.replace(viejo, nuevo), list(cargar_criterio(RAIZ).construccion))
    assert any(esperado in m for m in malos), malos
