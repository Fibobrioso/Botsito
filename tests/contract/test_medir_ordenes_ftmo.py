"""Contrato de `tools/mql5/MedirOrdenesFTMO.mq5` (rama `trabajo/f17-ordenes`, D1 y D4, y la
respuesta del consultor a la PARADA del 2026-11-26): el guion que coloca ordenes stop en una cuenta
DEMO.

Se comprueba en el texto, como `test_medir_demo_ftmo.py` (de donde se toman `funciones` y
`peticiones`):

- la condicion DEMO de `MedirDemoFTMO.mq5`:759, literal y la PRIMERA de `Comprobaciones`, y
  `OnStart` la llama antes de cualquier peticion;
- toda funcion que abre o coloca lleva el numero magico, stop distinto de 0 y, si es pendiente, la
  caducidad; solo `CerrarPosicion` va sin stop (cierra, no abre); toda `OrderSend` pasa por `Pedir`,
  que duerme `PAUSA_MS` tras cada una;
- un numero magico propio, distinto del de `MedirDemoFTMO`; solo EURUSD; la limpieza solo toca lo de
  su numero y su simbolo;
- las constantes: las del criterio (el bloque `guion` de `docs/plan/F17-ORDENES.yaml`), las del lote
  (`riesgo_por_operacion` y `lote_margen_libre_fraccion` del registro) y los topes (la tabla de
  `docs/runbooks/F17-ORDENES.md`); ninguna es un `input`;
- cada tope de D4 se lee de la cuenta y de su historial (`HistorySelect`, la terminal), no de una
  variable, y `PuedeEmpezarCiclo` los mira todos antes de colocar;
- (a) `PeorCaso` cuenta compras y ventas; el margen del lote se pide a mercado, nunca con el tipo
  stop (punto 2 de la respuesta);
- la ventana muerta: nada se coloca si el ciclo puede llegar a `HORA_MUERTA_DESDE`, y en las esperas
  se cierra al entrar en ella (punto 3).

Cada regla rompe a proposito con el fuente mutado.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.comun.yaml_estricto import leer_yaml
from botsito.config.registro import cargar_registro
from tests.contract.test_capa_mt5 import sin_comentarios
from tests.contract.test_medir_demo_ftmo import funciones

RAIZ = Path(__file__).resolve().parents[2]
FUENTE = RAIZ / "tools" / "mql5" / "MedirOrdenesFTMO.mq5"
MEDIR = RAIZ / "tools" / "mql5" / "MedirDemoFTMO.mq5"
CRITERIO = RAIZ / "docs" / "plan" / "F17-ORDENES.yaml"
RUNBOOK = RAIZ / "docs" / "runbooks" / "F17-ORDENES.md"
LINEA_DEMO = 759
CONDICION_DEMO = (
    "if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)"
)
SIN_STOP = {"CerrarPosicion": "cierra una posicion existente (`req.position`), no abre nada"}
QUE_ABREN = {"TRADE_ACTION_DEAL": "DEAL", "TRADE_ACTION_PENDING": "PENDING"}
SIN_COMPROBAR = frozenset({"TRADE_ACTION_REMOVE", "TRADE_ACTION_MODIFY"})
# las del criterio: constante del .mq5 -> clave del bloque `guion` del yaml
DEL_CRITERIO = {
    "STOP_PUNTOS": "stop_puntos",
    "SALIDA_A_MERCADO_S": "salida_a_mercado_s",
    "ESPERA_LLENADO_S": "espera_llenado_s",
    "DISTANCIA_ENTRADA_PUNTOS": "distancia_entrada_puntos",
}
# los topes: constante -> lo que dice la tabla del runbook
DEL_RUNBOOK = {
    "TOPE_PEOR_CASO_USD": ("1000.0", "| 1.000 USD |"),
    "TOPE_DIA_USD": ("3000.0", "| 3.000 USD |"),
    "TOPE_TOTAL_USD": ("8000.0", "| 8.000 USD |"),
    "TOPE_PETICIONES": ("500", "| 500 |"),
    "PAUSA_MS": ("1500", "| 1.500 ms |"),
    "MARGEN_CIERRE_MIN": ("150", "| 150 min |"),
    "HORA_MUERTA_DESDE": ("22", "| de 22 a 3 h del servidor |"),
    "HORA_MUERTA_HASTA": ("3", "| de 22 a 3 h del servidor |"),
}
MAGICO_DE_MEDIR = "57057000"
# cada tope de D4: la funcion que lo calcula y lo que tiene que leer (de la cuenta o su historial)
TOPES_LEIDOS = {
    "SaldoAlEmpezarElDia": ("HistorySelect", "ACCOUNT_BALANCE"),
    "CapitalDelHistorial": ("HistorySelect", "DEAL_TYPE_BALANCE"),
    "PeticionesDelDia": ("HistorySelect", "OrdersTotal"),
    "PeorCaso": ("OrdersTotal", "PositionsTotal"),
    "CercaDelCierre": ("SymbolInfoSessionTrade",),
}
EN_PUEDE_EMPEZAR = (
    "EnHoraMuerta(ahora + DURACION_MAXIMA_CICLO_S)",
    "CercaDelCierre(",
    "SaldoAlEmpezarElDia()",
    "CapitalDelHistorial()",
    "PeticionesDelDia()",
    "PeorCaso(",
)


def _src() -> str:
    return FUENTE.read_text(encoding="utf-8")


def cuerpo_de(src: str, nombre: str) -> str:
    """El cuerpo (con su cabecera) de la UNICA funcion `nombre`; vacio si no esta."""
    cuerpos = [c for n, c in funciones(src) if n == nombre]
    return cuerpos[0] if len(cuerpos) == 1 else ""


def define(src: str, nombre: str) -> str | None:
    m = re.search(rf"^#define\s+{nombre}\s+(\S+)", src, re.MULTILINE)
    return m.group(1) if m else None


def problemas(
    src: str, guion: dict[str, int], registro: dict[str, Decimal], runbook: str
) -> list[str]:
    salida: list[str] = []
    codigo = sin_comentarios(src)
    # la negativa DEMO: literal, la primera de Comprobaciones, y OnStart la llama antes de pedir
    comprobaciones = cuerpo_de(codigo, "Comprobaciones")
    if CONDICION_DEMO not in comprobaciones:
        salida.append("Comprobaciones no lleva la condicion DEMO de MedirDemoFTMO.mq5:759")
    elif comprobaciones.index(CONDICION_DEMO) > comprobaciones.index("{") + 8:
        salida.append("la condicion DEMO no es lo primero de Comprobaciones")
    onstart = cuerpo_de(codigo, "OnStart")
    i = onstart.find("Comprobaciones(motivo)")
    envia = [m.start() for m in re.finditer(r"\b(Ciclo|Limpiar|Pedir|OrderSend)\s*\(", onstart)]
    if i < 0 or (envia and min(envia) < i):
        salida.append("OnStart no llama a Comprobaciones antes de pedir nada")
    # lo que abre o coloca: magico, stop y caducidad; y toda OrderSend dentro de Pedir
    for nombre, cuerpo in funciones(codigo):
        if re.search(r"\bOrderSend(?:Async)?\s*\(", cuerpo) and nombre != "Pedir":
            salida.append(f"{nombre}: OrderSend fuera de Pedir")
        for var in sorted(set(re.findall(r"\b(\w+)\.action\s*=", cuerpo))):
            acciones = re.findall(rf"\b{var}\.action\s*=\s*([^;]+);", cuerpo)
            for accion in (a.strip() for a in acciones):
                if accion in SIN_COMPROBAR:
                    continue
                tipo = QUE_ABREN.get(accion)
                if tipo is None:
                    salida.append(f"{nombre}: {var}.action = {accion}: no se puede leer")
                    continue
                if not re.search(rf"\b{var}\.magic\s*=\s*MAGICO\s*;", cuerpo):
                    salida.append(f"{nombre}: {tipo} sin {var}.magic = MAGICO")
                if tipo == "PENDING" and f"PonerCaducidad({var})" not in cuerpo:
                    salida.append(f"{nombre}: PENDING sin PonerCaducidad({var})")
                if nombre in SIN_STOP:
                    continue
                if not re.search(rf"\b{var}\.sl\s*=", cuerpo) or re.search(
                    rf"\b{var}\.sl\s*=\s*0(?:\.0*)?\s*;", cuerpo
                ):
                    salida.append(f"{nombre}: {tipo} sin {var}.sl (stop de proteccion)")
    pedir = cuerpo_de(codigo, "Pedir")
    if "Sleep(PAUSA_MS)" not in pedir:
        salida.append("Pedir no duerme PAUSA_MS tras cada peticion")
    # numero magico propio, solo EURUSD, limpieza del numero y del simbolo
    magico = define(codigo, "MAGICO")
    if magico is None or magico == MAGICO_DE_MEDIR or not magico.isdigit():
        salida.append(f"MAGICO {magico}: tiene que ser propio, distinto del de MedirDemoFTMO")
    # los nombres de DEAL_REASON de NombreMotivo («CLIENT», «EXPERT»...) no son simbolos
    sin_motivos = codigo.replace(cuerpo_de(codigo, "NombreMotivo"), "")
    simbolos = set(re.findall(r'"([A-Z]{6})"', sin_motivos))
    if simbolos != {"EURUSD"}:
        salida.append(f"simbolos {sorted(simbolos)}: solo EURUSD")
    for nombre, cuerpo in funciones(codigo):
        for valor in re.findall(r"\.symbol\s*=\s*([^;]+);", cuerpo):
            if valor.strip() != "SIMBOLO":
                salida.append(f"{nombre}: .symbol = {valor.strip()}, no SIMBOLO")
    for f in ("QuedanAbiertas", "Limpiar"):
        c = cuerpo_de(codigo, f)
        if c.count("== MAGICO") < 2 or c.count("== SIMBOLO") < 2:
            salida.append(f"{f} no filtra por MAGICO y SIMBOLO")
    # las constantes
    for constante, clave in DEL_CRITERIO.items():
        if define(codigo, constante) != str(guion.get(clave)):
            salida.append(f"{constante} no es el {clave} del criterio ({guion.get(clave)})")
    for constante, valor in registro.items():
        if define(codigo, constante) is None or Decimal(str(define(codigo, constante))) != valor:
            salida.append(f"{constante} no es la del registro ({valor})")
    for constante, (valor, en_runbook) in DEL_RUNBOOK.items():
        if define(codigo, constante) != valor:
            salida.append(f"{constante} no es {valor}")
        if en_runbook not in runbook:
            salida.append(f"el runbook no dice {en_runbook!r} ({constante})")
    entradas = re.findall(r"^input\s+\w+\s+(\w+)", codigo, re.MULTILINE)
    if sorted(entradas) != ["InpCiclos", "InpEstrato"]:
        salida.append(f"entradas {entradas}: solo InpEstrato e InpCiclos")
    # cada tope, de la cuenta y de su historial
    for f, lecturas in TOPES_LEIDOS.items():
        c = cuerpo_de(codigo, f)
        for lectura in lecturas:
            if lectura not in c:
                salida.append(f"{f} no lee {lectura}")
    puede = cuerpo_de(codigo, "PuedeEmpezarCiclo")
    for llamada in EN_PUEDE_EMPEZAR:
        if llamada not in puede:
            salida.append(f"PuedeEmpezarCiclo no mira {llamada}")
    ciclo = cuerpo_de(codigo, "Ciclo")
    if ciclo.find("PuedeEmpezarCiclo(") < 0 or ciclo.find("PuedeEmpezarCiclo(") > ciclo.find(
        "ColocarStop("
    ):
        salida.append("Ciclo no comprueba los topes antes de colocar")
    if ciclo.count("HayQueCortar(") < 2:
        salida.append("Ciclo no corta en las dos esperas (llenado y salida)")
    if "EnHoraMuerta(TimeCurrent())" not in cuerpo_de(codigo, "HayQueCortar"):
        salida.append("HayQueCortar no cierra al entrar en la ventana muerta")
    muerta = re.sub(r"\s+", "", cuerpo_de(codigo, "EnHoraMuerta"))
    if "s.hour>=HORA_MUERTA_DESDE||s.hour<HORA_MUERTA_HASTA" not in muerta:
        salida.append("EnHoraMuerta no es de HORA_MUERTA_DESDE a HORA_MUERTA_HASTA")
    # (a) compras y ventas; el margen a mercado
    perdida = cuerpo_de(codigo, "PerdidaHastaElStop")
    if "ORDER_TYPE_SELL" not in perdida or "ORDER_TYPE_BUY" not in perdida:
        salida.append("PerdidaHastaElStop no calcula compras y ventas")
    if "PerdidaHastaElStop(" not in cuerpo_de(codigo, "PeorCaso"):
        salida.append("PeorCaso no usa PerdidaHastaElStop")
    for m in re.finditer(r"OrderCalcMargin\s*\(([^;]*)\)", codigo):
        if "_STOP" in m.group(1) or "_LIMIT" in m.group(1):
            salida.append("OrderCalcMargin con un tipo pendiente: la tasa de la stop es 0;0")
        elif "ORDER_TYPE_BUY" not in m.group(1) or "ORDER_TYPE_SELL" not in m.group(1):
            salida.append("OrderCalcMargin sin ORDER_TYPE_BUY u ORDER_TYPE_SELL a mercado")
    # revision del consultor, arreglo 1: el saldo del dia solo resta los deals de trading (el
    # deposito del primer dia de la cuenta es un DEAL_TYPE_BALANCE de hoy)
    saldo = re.sub(r"\s+", "", cuerpo_de(codigo, "SaldoAlEmpezarElDia"))
    filtro = "if(tipo!=DEAL_TYPE_BUY&&tipo!=DEAL_TYPE_SELL)continue;"
    if "longtipo=HistoryDealGetInteger(d,DEAL_TYPE);" not in saldo or filtro not in saldo:
        salida.append("SaldoAlEmpezarElDia no filtra los deals de trading (DEAL_TYPE_BUY y SELL)")
    elif saldo.index(filtro) > saldo.index("movido+="):
        salida.append("SaldoAlEmpezarElDia suma antes de filtrar")
    # arreglo 3: se niega si el stops level pasa de la distancia de la entrada
    comprobaciones_s = re.sub(r"\s+", "", comprobaciones)
    if (
        "SymbolInfoInteger(SIMBOLO,SYMBOL_TRADE_STOPS_LEVEL)" not in comprobaciones_s
        or "if(stops>DISTANCIA_ENTRADA_PUNTOS)" not in comprobaciones_s
    ):
        salida.append("Comprobaciones no se niega con un stops level mayor que la distancia")
    # arreglo 4: una salida que falta porque se paro el guion lo dice
    if not re.search(r'IsStopped\(\)\s*\?\s*"parado por el usuario', cuerpo_de(codigo, "Ciclo")):
        salida.append("Ciclo no dice «parado por el usuario» cuando se paro el guion")
    return salida


def _guion() -> dict[str, int]:
    return dict(leer_yaml(CRITERIO)["guion"])


def _registro() -> dict[str, Decimal]:
    """Las del lote, en fraccion: `riesgo_por_operacion` es un porcentaje (0,5 = 0,005) y
    `lote_margen_libre_fraccion` un decimal (0,95)."""
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    return {
        "RIESGO_FRACCION": registro.porcentaje("riesgo_por_operacion").valor / 100,
        "MARGEN_LIBRE_FRACCION": registro.decimal("lote_margen_libre_fraccion"),
    }


def _problemas(src: str) -> list[str]:
    return problemas(src, _guion(), _registro(), RUNBOOK.read_text(encoding="utf-8"))


def test_la_condicion_demo_es_la_de_medir_demo_ftmo() -> None:
    assert MEDIR.read_text(encoding="utf-8").splitlines()[LINEA_DEMO - 1].strip() == CONDICION_DEMO


def test_el_guion_cumple_el_contrato() -> None:
    assert _problemas(_src()) == []


def test_el_fuente_es_utf8_sin_bom_y_lf() -> None:
    b = FUENTE.read_bytes()
    assert not b.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in b
    b.decode("utf-8")


@pytest.mark.parametrize(
    ("viejo", "nuevo", "esperado"),
    [
        # la negativa DEMO quitada o al reves
        ("!= ACCOUNT_TRADE_MODE_DEMO)", "== ACCOUNT_TRADE_MODE_REAL)", "condicion DEMO"),
        # una peticion antes de la negativa
        (
            '   string motivo = "";\n   if(!Comprobaciones(motivo))',
            '   string motivo = "";\n   Limpiar("antes");\n   if(!Comprobaciones(motivo))',
            "antes de pedir nada",
        ),
        # una pendiente sin stop, sin caducidad o sin magico
        (
            "   req.sl = NormalizeDouble(compra ? nivel - STOP_PUNTOS * g_point : "
            "nivel + STOP_PUNTOS * g_point, g_digits);\n",
            "",
            "ColocarStop: PENDING sin req.sl",
        ),
        (
            '   req.comment = "MedirOrdenesFTMO";\n   PonerCaducidad(req);\n',
            '   req.comment = "MedirOrdenesFTMO";\n',
            "ColocarStop: PENDING sin PonerCaducidad",
        ),
        (
            "   req.magic = MAGICO;\n   req.volume = volumen;\n",
            "   req.volume = volumen;\n",
            "ColocarStop: PENDING sin req.magic",
        ),
        # una OrderSend fuera de Pedir, y Pedir sin pausa
        (
            "   PonerCaducidad(req);\n   return Pedir(req, res, ciclo, compra ? "
            '"colocar_buy_stop" : "colocar_sell_stop");',
            "   PonerCaducidad(req);\n   return OrderSend(req, res);",
            "ColocarStop: OrderSend fuera de Pedir",
        ),
        ("   Sleep(PAUSA_MS);\n   return aceptada;", "   return aceptada;", "no duerme PAUSA_MS"),
        # el magico de MedirDemoFTMO, otro simbolo
        ("#define MAGICO         57057100", "#define MAGICO         57057000", "MAGICO 57057000"),
        ('#define SIMBOLO        "EURUSD"', '#define SIMBOLO        "XAUUSD"', "solo EURUSD"),
        # la limpieza sin el filtro del numero magico: borraria pendientes de otro
        (
            "         if(tk != 0 && OrderGetInteger(ORDER_MAGIC) == MAGICO && "
            "OrderGetString(ORDER_SYMBOL) == SIMBOLO)\n            BorrarPendiente(tk, 0);",
            "         if(tk != 0)\n            BorrarPendiente(tk, 0);",
            "Limpiar no filtra por MAGICO y SIMBOLO",
        ),
        # control: un comentario con OrderSend no cuenta
        (
            "bool Pedir(MqlTradeRequest",
            "// OrderSend(x) en un comentario\nbool Pedir(MqlTradeRequest",
            None,
        ),
        # una constante distinta del criterio, del registro o del runbook
        (
            "#define STOP_PUNTOS              18",
            "#define STOP_PUNTOS              15",
            "STOP_PUNTOS no es",
        ),
        (
            "#define DISTANCIA_ENTRADA_PUNTOS 5",
            "#define DISTANCIA_ENTRADA_PUNTOS 2",
            "DISTANCIA_ENTRADA_PUNTOS no es",
        ),
        (
            "#define RIESGO_FRACCION       0.005",
            "#define RIESGO_FRACCION       0.01",
            "RIESGO_FRACCION no es",
        ),
        (
            "#define MARGEN_LIBRE_FRACCION 0.95",
            "#define MARGEN_LIBRE_FRACCION 1.00",
            "MARGEN_LIBRE_FRACCION no es",
        ),
        (
            "#define TOPE_PEOR_CASO_USD 1000.0",
            "#define TOPE_PEOR_CASO_USD 2000.0",
            "TOPE_PEOR_CASO_USD no es",
        ),
        (
            "#define TOPE_DIA_USD       3000.0",
            "#define TOPE_DIA_USD       4500.0",
            "TOPE_DIA_USD no es",
        ),
        (
            "#define TOPE_TOTAL_USD     8000.0",
            "#define TOPE_TOTAL_USD     9500.0",
            "TOPE_TOTAL_USD no es",
        ),
        (
            "#define TOPE_PETICIONES    500",
            "#define TOPE_PETICIONES    1500",
            "TOPE_PETICIONES no es",
        ),
        ("#define PAUSA_MS           1500", "#define PAUSA_MS           500", "PAUSA_MS no es"),
        (
            "#define HORA_MUERTA_DESDE  22",
            "#define HORA_MUERTA_DESDE  23",
            "HORA_MUERTA_DESDE no es",
        ),
        # un tope como entrada
        (
            "input int    InpCiclos  = 50;",
            "input int    InpCiclos  = 50;\ninput int    InpPausa = 1500;",
            "solo InpEstrato e InpCiclos",
        ),
        # un tope que no lee el historial (recordado en una variable)
        (
            "   if(!HistorySelect(desde, TimeCurrent() + 3600))\n      return -1.0;\n"
            "   double movido",
            "   double movido",
            "SaldoAlEmpezarElDia no lee HistorySelect",
        ),
        (
            "      if(d != 0 && HistoryDealGetInteger(d, DEAL_TYPE) == DEAL_TYPE_BALANCE)",
            "      if(d != 0)",
            "CapitalDelHistorial no lee DEAL_TYPE_BALANCE",
        ),
        # arreglo 1: el saldo del dia restando tambien el deposito (el primer dia, el tope no salta)
        (
            "      if(tipo != DEAL_TYPE_BUY && tipo != DEAL_TYPE_SELL)\n         continue;\n",
            "",
            "SaldoAlEmpezarElDia no filtra los deals de trading",
        ),
        (
            "      if(tipo != DEAL_TYPE_BUY && tipo != DEAL_TYPE_SELL)\n",
            "      if(tipo == DEAL_TYPE_BALANCE && false)\n",
            "SaldoAlEmpezarElDia no filtra los deals de trading",
        ),
        # arreglo 3: sin la negativa por el stops level
        (
            "   if(stops > DISTANCIA_ENTRADA_PUNTOS)\n",
            "   if(false)\n",
            "Comprobaciones no se niega con un stops level mayor",
        ),
        # arreglo 4: la fila de un guion parado dice que no se pudo cerrar
        (
            '           IsStopped() ? "parado por el usuario: Limpiar" : '
            '"la posicion no se pudo cerrar: Limpiar");',
            '           "la posicion no se pudo cerrar: Limpiar");',
            "parado por el usuario",
        ),
        # un tope que PuedeEmpezarCiclo no mira
        (
            "      int peticiones = PeticionesDelDia();",
            "      int peticiones = g_rechazadas;",
            "PuedeEmpezarCiclo no mira PeticionesDelDia()",
        ),
        (
            "   else if(CercaDelCierre(ahora, nota))",
            "   else if(false)",
            "PuedeEmpezarCiclo no mira CercaDelCierre(",
        ),
        # la ventana muerta: sin mirar el fin del ciclo, o sin cortar en las esperas
        (
            "   if(EnHoraMuerta(ahora) || EnHoraMuerta(ahora + DURACION_MAXIMA_CICLO_S))",
            "   if(EnHoraMuerta(ahora))",
            "EnHoraMuerta(ahora + DURACION_MAXIMA_CICLO_S)",
        ),
        (
            '   if(EnHoraMuerta(TimeCurrent()))\n      tope = "hora_muerta";\n   else if(saldo_dia',
            '   if(false)\n      tope = "hora_muerta";\n   else if(saldo_dia',
            "HayQueCortar no cierra al entrar en la ventana muerta",
        ),
        (
            "   return (s.hour >= HORA_MUERTA_DESDE || s.hour < HORA_MUERTA_HASTA);",
            "   return (s.hour >= HORA_MUERTA_DESDE);",
            "EnHoraMuerta no es de",
        ),
        # (a) solo compras, como el paso 8 de MedirDemoFTMO
        (
            "OrderCalcProfit(compra ? ORDER_TYPE_BUY : ORDER_TYPE_SELL, SIMBOLO, vol, precio, "
            "cierre, p)",
            "OrderCalcProfit(ORDER_TYPE_BUY, SIMBOLO, vol, precio, cierre, p)",
            "PerdidaHastaElStop no calcula compras y ventas",
        ),
        # el margen con el tipo stop
        (
            "OrderCalcMargin(compra ? ORDER_TYPE_BUY : ORDER_TYPE_SELL, SIMBOLO, 1.0,",
            "OrderCalcMargin(compra ? ORDER_TYPE_BUY_STOP : ORDER_TYPE_SELL_STOP, SIMBOLO, 1.0,",
            "OrderCalcMargin con un tipo pendiente",
        ),
    ],
)
def test_cada_regla_rompe_a_proposito(viejo: str, nuevo: str, esperado: str | None) -> None:
    src = _src()
    assert src.count(viejo) == 1, viejo
    malos = _problemas(src.replace(viejo, nuevo))
    if esperado is None:
        assert malos == []
    else:
        assert any(esperado in m for m in malos), malos


def test_una_constante_del_runbook_cambiada_rompe() -> None:
    runbook = RUNBOOK.read_text(encoding="utf-8")
    assert runbook.count("| 3.000 USD |") == 1
    malos = problemas(
        _src(), _guion(), _registro(), runbook.replace("| 3.000 USD |", "| 4.000 USD |")
    )
    assert any("el runbook no dice '| 3.000 USD |'" in m for m in malos), malos


def test_una_cifra_del_criterio_cambiada_rompe() -> None:
    guion = {**_guion(), "salida_a_mercado_s": 600}
    malos = problemas(_src(), guion, _registro(), RUNBOOK.read_text(encoding="utf-8"))
    assert any("SALIDA_A_MERCADO_S no es" in m for m in malos), malos


# --- el dia de riesgo (respuesta a la PARADA, punto 3): la ventana muerta contiene la medianoche
# de Espana, y la ventana del bot queda fuera de ella, con zoneinfo de 2026 a 2030


def _reloj_servidor() -> Any:
    """`RelojServidor` de `scripts/leer_historial_f17.py`, del registro, sin cifras."""
    spec = importlib.util.spec_from_file_location(
        "leer_historial_f17", RAIZ / "scripts" / "leer_historial_f17.py"
    )
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["leer_historial_f17"] = modulo  # lo pide @dataclass al crear la clase
    spec.loader.exec_module(modulo)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    return modulo.RelojServidor.del_registro(registro)


def _en_el_servidor(reloj: Any, d: date, hh: int, zona: ZoneInfo) -> datetime:
    """Las `hh`:00 del dia `d` en `zona`, en el reloj del servidor (escrito como si fuera UTC)."""
    utc = datetime(d.year, d.month, d.day, hh, tzinfo=zona).astimezone(UTC)
    return datetime.fromtimestamp(reloj.a_servidor(int(utc.timestamp() * 1000)) / 1000, tz=UTC)


def fallos_del_dia_de_riesgo(desde_h: int, hasta_h: int, reloj: Any, huso: str) -> list[str]:
    """Cada dia de 2026 a 2030 en que la medianoche de `huso` no cae en [00:00, hasta_h) del MISMO
    dia del servidor, o en que la ventana del bot (07:00 a 15:00 de `huso`) toca la ventana
    muerta."""
    zona = ZoneInfo(huso)
    salida: list[str] = []
    d = date(2026, 1, 1)
    while d < date(2031, 1, 1):
        s = _en_el_servidor(reloj, d, 0, zona)
        if not (s.date() == d and s.hour < hasta_h):
            salida.append(f"{d}: la medianoche de {huso} cae a las {s:%H:%M} del servidor")
        for hh in (7, 15):
            s = _en_el_servidor(reloj, d, hh, zona)
            if s.hour >= desde_h or s.hour < hasta_h:
                salida.append(f"{d}: las {hh}:00 de {huso} caen en la ventana muerta ({s:%H:%M})")
        d += timedelta(days=1)
    return salida


def test_la_ventana_muerta_contiene_la_medianoche_de_espana() -> None:
    src = _src()
    desde, hasta = define(src, "HORA_MUERTA_DESDE"), define(src, "HORA_MUERTA_HASTA")
    assert desde is not None and hasta is not None
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    huso = registro.texto("huso_operativa")
    assert registro.opcion("reloj_dia_riesgo") == "civil_operativa"
    assert fallos_del_dia_de_riesgo(int(desde), int(hasta), _reloj_servidor(), huso) == []


def test_la_medida_tiene_los_dos_lados_de_cada_cambio_de_hora() -> None:
    """Las semanas en que EE. UU. y la UE no han cambiado a la vez dan las 02:00; el resto, la 01:00
    (medido en la fase 0: 1.707 y 119 dias). Si faltara un lado, el test de arriba no lo
    probaria."""
    reloj = _reloj_servidor()
    zona = ZoneInfo("Europe/Madrid")
    horas = set()
    d = date(2026, 1, 1)
    while d < date(2031, 1, 1):
        horas.add(_en_el_servidor(reloj, d, 0, zona).hour)
        d += timedelta(days=1)
    assert horas == {1, 2}


def test_una_ventana_muerta_mas_corta_rompe() -> None:
    """Rompe a proposito: hasta las 02:00 deja fuera las medianoches de las semanas desparejas, y
    desde las 06:00 la ventana del bot cae dentro."""
    reloj = _reloj_servidor()
    corta = fallos_del_dia_de_riesgo(22, 2, reloj, "Europe/Madrid")
    assert corta and all("medianoche" in f for f in corta)
    assert any(
        "ventana muerta" in f for f in fallos_del_dia_de_riesgo(6, 3, reloj, "Europe/Madrid")
    )
