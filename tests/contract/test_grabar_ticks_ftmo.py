"""Contrato de `tools/mql5/GrabarTicksFTMO.mq5` (rama `trabajo/f17-ordenes`, D2): un script que SOLO
LEE los ticks del servidor de una cuenta DEMO y los graba, una hora por fichero.

Se comprueba en el texto, como el del exportador (`test_exportar_ticks_ftmo.py`, de donde se toman
`cuerpo_de` y la condicion DEMO; la lista de funciones de trading, de `test_capa_mt5.py`): no llama
a ninguna funcion de trading ni de ordenes; lleva la condicion DEMO literal y `OnStart` la mira
antes de pedir nada; solo EURUSD; todo lo que escribe lleva el prefijo `F17G_`; cada hora se escribe
en `.part` y pasa a `.csv` con `FileMove(..., FILE_REWRITE)`; el bucle mira `IsStopped`; y la
primera vez empieza al inicio de la hora en que se lanza, nunca en «el primer tick disponible» (un
`from` 0). Cada comprobacion rompe a proposito con un fuente mutado."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from tests.contract.test_capa_mt5 import llamadas_de_trading, sin_comentarios, sin_textos
from tests.contract.test_exportar_ticks_ftmo import CONDICION_DEMO, cuerpo_de

RAIZ = Path(__file__).resolve().parents[2]
FUENTE = RAIZ / "tools" / "mql5" / "GrabarTicksFTMO.mq5"
PETICIONES = ("CopyTicksRange", "CopyTicks", "FileOpen", "FileFindFirst", "FileDelete", "FileMove")


def _src() -> str:
    return FUENTE.read_text(encoding="utf-8")


def problemas(src: str) -> list[str]:
    salida: list[str] = []
    codigo = sin_comentarios(src)
    trading = llamadas_de_trading(src)
    if trading:
        salida.append(f"llama a funciones de trading: {sorted(set(trading))}")
    if CONDICION_DEMO not in cuerpo_de(src, "Comprobaciones"):
        salida.append("Comprobaciones no lleva la condicion DEMO de MedirDemoFTMO.mq5:759")
    onstart = sin_textos(cuerpo_de(src, "OnStart"))
    posiciones = [m.start() for p in PETICIONES for m in re.finditer(rf"\b{p}\s*\(", onstart)]
    llamadas = [
        m.start() for m in re.finditer(r"\b(Rehacer\w+|Borrar\w+|Siguiente\w+)\s*\(", onstart)
    ]
    i = onstart.find("Comprobaciones(")
    if i < 0 or i > min([*posiciones, *llamadas], default=len(onstart)):
        salida.append("OnStart no llama a Comprobaciones antes de pedir nada")
    simbolos = set(re.findall(r'"([A-Z]{6})"', codigo))
    if simbolos != {"EURUSD"}:
        salida.append(f"simbolos {sorted(simbolos)}: solo EURUSD")
    if not re.search(r'^#define\s+PREFIJO\s+"F17G_"', codigo, re.MULTILINE):
        salida.append("PREFIJO no es F17G_")
    for m in re.finditer(r"\bFileOpen\s*\(([^,]*),", codigo):
        if "NombreDeLaHora(" not in m.group(1) and m.group(1).strip() != "nombre":
            salida.append(f"FileOpen de {m.group(1).strip()}: no es un nombre con PREFIJO")
    if "PREFIJO" not in cuerpo_de(src, "NombreDeLaHora"):
        salida.append("NombreDeLaHora no lleva el PREFIJO")
    if not re.search(r'StringFormat\("%scontrol_', cuerpo_de(src, "OnStart")):
        salida.append("el control no lleva el PREFIJO")
    cerrar = re.sub(r"\s+", "", cuerpo_de(src, "CerrarHora"))
    if 'FileMove(base+".part",0,base+".csv",FILE_REWRITE)' not in cerrar:
        salida.append("CerrarHora no pasa el .part a .csv con FileMove y FILE_REWRITE")
    if '".part"' not in cuerpo_de(src, "AbrirHora"):
        salida.append("AbrirHora no escribe en .part")
    if "while(!IsStopped())" not in re.sub(r"\s+", "", cuerpo_de(src, "OnStart")):
        salida.append("el bucle no mira IsStopped")
    if re.search(r"\bCopyTicks(?:Range)?\s*\([^;]*,\s*0\s*[,)]", codigo):
        salida.append("una peticion de ticks desde 0: «el primer tick disponible»")
    if "desde = ahora;" not in cuerpo_de(src, "OnStart"):
        salida.append("la primera vez no empieza al inicio de la hora en que se lanza")
    if "g_ultimo = (long)ahora * 1000;" not in cuerpo_de(src, "OnStart"):
        salida.append("la hora en curso no empieza en su inicio")
    return salida


def test_el_grabador_cumple_el_contrato() -> None:
    assert problemas(_src()) == []


def test_el_fuente_es_utf8_sin_bom_y_lf() -> None:
    b = FUENTE.read_bytes()
    assert not b.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in b
    b.decode("utf-8")


@pytest.mark.parametrize(
    ("viejo", "nuevo", "esperado"),
    [
        # una orden, aunque sea en una funcion que no se llama
        (
            "bool Comprobaciones(",
            "void Enviar(){ MqlTradeRequest r; MqlTradeResult s; OrderSend(r, s); }\n"
            "bool Comprobaciones(",
            "llama a funciones de trading",
        ),
        ("bool Comprobaciones(", "#include <Trade\\Trade.mqh>\nbool Comprobaciones(", "trading"),
        # la negativa DEMO quitada
        ("!= ACCOUNT_TRADE_MODE_DEMO)", "== ACCOUNT_TRADE_MODE_REAL)", "condicion DEMO"),
        # una peticion antes de la negativa
        (
            '   string motivo = "";\n   if(!Comprobaciones(motivo))',
            '   string motivo = "";\n   BorrarPartes();\n   if(!Comprobaciones(motivo))',
            "antes de pedir nada",
        ),
        # otro simbolo, otro prefijo
        ('#define SIMBOLO        "EURUSD"', '#define SIMBOLO        "XAUUSD"', "solo EURUSD"),
        ('#define PREFIJO        "F17G_"', '#define PREFIJO        "F17_"', "PREFIJO no es F17G_"),
        # la hora escrita directamente en .csv, o renombrada sin FILE_REWRITE
        (
            '   g_part = FileOpen(NombreDeLaHora(hora) + ".part",',
            '   g_part = FileOpen(NombreDeLaHora(hora) + ".csv",',
            "AbrirHora no escribe en .part",
        ),
        (
            'FileMove(base + ".part", 0, base + ".csv", FILE_REWRITE)',
            'FileMove(base + ".part", 0, base + ".csv", 0)',
            "FileMove y FILE_REWRITE",
        ),
        # un bucle que no mira IsStopped
        (
            "   while(!IsStopped())\n     {\n      MqlTick ticks[];",
            "   while(true)\n     {\n      MqlTick ticks[];",
            "IsStopped",
        ),
        # la primera vez, desde el primer tick disponible
        (
            "      desde = ahora; // la primera vez",
            "      desde = 0; // la primera vez",
            "la primera vez no empieza",
        ),
        (
            "   g_ultimo = (long)ahora * 1000;\n",
            "   g_ultimo = 0;\n",
            "la hora en curso no empieza",
        ),
        # control: un comentario con OrderSend no cuenta
        ("bool Comprobaciones(", "// OrderSend(r, s);\nbool Comprobaciones(", None),
        (
            "int n = CopyTicks(SIMBOLO, ticks, COPY_TICKS_ALL, (ulong)desde_msc, LOTE_TICKS);",
            "int n = CopyTicks(SIMBOLO, ticks, COPY_TICKS_ALL, 0, LOTE_TICKS);",
            "desde 0",
        ),
    ],
)
def test_cada_regla_rompe_a_proposito(viejo: str, nuevo: str, esperado: str | None) -> None:
    src = _src()
    assert src.count(viejo) == 1, viejo
    malos = problemas(src.replace(viejo, nuevo))
    if esperado is None:
        assert malos == []
    else:
        assert any(esperado in m for m in malos), malos
