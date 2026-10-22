"""La capa de MT5 que nunca decide una operacion (ADR-0082; trabajo/ea-conexion, R6a.1), leida por
su texto: las pruebas estaticas de D4 (1), que corren en `make check` y en la CI de Linux sin
MetaTrader.

- D2e: ningun `.mq5` ni `.mqh` de la capa llama a una funcion del grupo de funciones de trading de
  la documentacion oficial de MQL5 (<https://www.mql5.com/en/docs/trading>, consultada el
  2026-10-19: las 33 de `FUNCIONES_DE_TRADING`), ni usa la clase `CTrade` ni incluye la carpeta
  `Trade\\` de la biblioteca estandar, salvo las de `LECTURA_PERMITIDA`, que en R6a.1 esta vacia.
  Niega por defecto: tambien las de lectura (PositionsTotal, HistorySelect...).
- D2a: la condicion de `NegarFueraDeDemo(modo)` es la de `tools/mql5/MedirDemoFTMO.mq5:759`, con el
  modo como argumento, y la funcion no hace nada mas.
- D2a y respuesta a la PARADA, punto 1: `OnInit` la llama lo primero, y si niega devuelve
  `INIT_FAILED`; y hay exactamente otra llamada, con el modo leido al conectar, cuyo bloque hace
  `ExpertRemove()`.
- D2g: en el codigo de la capa no hay cifras con decimales, ni nombres de instrumento ni de firma, y
  los `#define` son solo los del formato y la version (`DEFINES_PERMITIDOS`, mql5/JOURNAL.md).
- D2b y D2c tras un cambio de simbolo: cada global del EA y de sus includes se pone a su valor
  inicial en `OnInit` o en una funcion a la que `OnInit` llame (`globales_sin_reiniciar`; el defecto
  medido en la demo del 2026-10-20, EA-CONEXION.md fase 3).

Cada comprobacion se rompe a proposito en los dos sentidos sobre fuentes de ejemplo; las mismas
comprobaciones se aplican a los ficheros reales de la capa (los tests `test_la_capa_*`).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
# La capa: las grafias exactas, porque la CI es Linux (ERRORES-RECURRENTES.md).
CARPETAS_DE_LA_CAPA = ("mql5/Experts", "mql5/Include/Botsito", "mql5/Scripts")
MEDIR = RAIZ / "tools" / "mql5" / "MedirDemoFTMO.mq5"

FUNCIONES_DE_TRADING = (
    "OrderCalcMargin",
    "OrderCalcProfit",
    "OrderCheck",
    "OrderSend",
    "OrderSendAsync",
    "PositionsTotal",
    "PositionGetSymbol",
    "PositionSelect",
    "PositionSelectByTicket",
    "PositionGetDouble",
    "PositionGetInteger",
    "PositionGetString",
    "PositionGetTicket",
    "OrdersTotal",
    "OrderGetTicket",
    "OrderSelect",
    "OrderGetDouble",
    "OrderGetInteger",
    "OrderGetString",
    "HistorySelect",
    "HistorySelectByPosition",
    "HistoryOrderSelect",
    "HistoryOrdersTotal",
    "HistoryOrderGetTicket",
    "HistoryOrderGetDouble",
    "HistoryOrderGetInteger",
    "HistoryOrderGetString",
    "HistoryDealSelect",
    "HistoryDealsTotal",
    "HistoryDealGetTicket",
    "HistoryDealGetDouble",
    "HistoryDealGetInteger",
    "HistoryDealGetString",
)
LECTURA_PERMITIDA: frozenset[str] = frozenset()  # vacia en R6a.1 (D2e)
DEFINES_PERMITIDOS = frozenset({"VERSION_EA", "JOURNAL_VERSION", "LATIDO_SEG", "TOPE_SESIONES"})
TEXTOS_PROHIBIDOS = re.compile(r"\b(EURUSD|XAUUSD|NASDAQ|FTMO|FundedNext)\b")
LLAMADA = "NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE))"


# --- leer MQL5 sin compilarlo -------------------------------------------------------------------


def sin_comentarios(src: str) -> str:
    """Quita `// ...` y `/* ... */` sin tocar los textos entre comillas."""
    salida, i, n = [], 0, len(src)
    while i < n:
        c = src[i]
        if c == '"':
            j = i + 1
            while j < n and src[j] != '"':
                j += 2 if src[j] == "\\" else 1
            salida.append(src[i : j + 1])
            i = j + 1
        elif src.startswith("//", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif src.startswith("/*", i):
            j = src.find("*/", i + 2)
            i = n if j < 0 else j + 2
            salida.append(" ")
        else:
            salida.append(c)
            i += 1
    return "".join(salida)


def sin_textos(src: str) -> str:
    """Cada texto entre comillas (ya sin comentarios) pasa a `""`: lo que queda es codigo."""
    return re.sub(r'"(?:\\.|[^"\\])*"', '""', src)


def compacto(src: str) -> str:
    """El codigo sin comentarios, sin textos y sin espacios en blanco."""
    return re.sub(r"\s+", "", sin_textos(sin_comentarios(src)))


def bloque(texto: str, inicio: int) -> str:
    """El contenido entre la primera `{` desde `inicio` y su `}`."""
    a = texto.index("{", inicio)
    nivel = 0
    for j in range(a, len(texto)):
        if texto[j] == "{":
            nivel += 1
        elif texto[j] == "}":
            nivel -= 1
            if nivel == 0:
                return texto[a + 1 : j]
    raise ValueError("llave sin cerrar")


# --- las comprobaciones ------------------------------------------------------------------------


def llamadas_de_trading(src: str) -> list[str]:
    """Las funciones de trading que llama `src`, `CTrade` y los `#include <Trade\\...>`."""
    codigo = sin_textos(sin_comentarios(src))
    prohibidas = [f for f in FUNCIONES_DE_TRADING if f not in LECTURA_PERMITIDA]
    halladas = re.findall(r"\b(" + "|".join(prohibidas) + r")\s*\(", codigo)
    halladas += re.findall(r"\bCTrade\b", codigo)
    halladas += re.findall(r"#include\s*[<\"]\s*Trade[\\/]", sin_comentarios(src))
    return halladas


def condicion_de_medir(src: str) -> str:
    """La condicion de la negativa de MedirDemoFTMO, con la lectura del modo como `<MODO>`."""
    linea = next(x for x in sin_comentarios(src).splitlines() if "ACCOUNT_TRADE_MODE_DEMO" in x)
    m = re.fullmatch(r"\s*if\((.*)\)\s*", linea)
    assert m is not None, linea
    return re.sub(r"\s+", "", m.group(1)).replace(
        "AccountInfoInteger(ACCOUNT_TRADE_MODE)", "<MODO>"
    )


def condicion_de_la_capa(src: str) -> str:
    """La condicion de `NegarFueraDeDemo(modo)`, con el parametro como `<MODO>`. La funcion tiene
    que ser exactamente `if(<condicion>) return true; return false;`."""
    c = compacto(src)
    m = re.search(r"boolNegarFueraDeDemo\((?:const)?long(\w+)\)\{", c)
    assert m is not None, "no hay bool NegarFueraDeDemo(const long modo)"
    cuerpo = bloque(c, m.start())
    f = re.fullmatch(r"if\((.*)\)(?:\{returntrue;\}|returntrue;)returnfalse;", cuerpo)
    assert f is not None, f"NegarFueraDeDemo hace algo mas que la condicion: {cuerpo}"
    return re.sub(rf"\b{m.group(1)}\b", "<MODO>", f.group(1))


def primera_de_oninit(src: str) -> str:
    """El bloque del `if` que abre `OnInit`, que tiene que ser la llamada a la negativa."""
    c = compacto(src)
    m = re.search(r"intOnInit\(\)\{", c)
    assert m is not None, "no hay int OnInit()"
    cuerpo = bloque(c, m.start())
    assert cuerpo.startswith(f"if({LLAMADA})"), f"OnInit no empieza por la negativa: {cuerpo[:80]}"
    return bloque(cuerpo, 0)


def bloques_de_la_negativa(src: str) -> list[str]:
    """El bloque de cada `if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))`, y falla si
    la funcion se llama de otra forma."""
    c = compacto(src)
    todas = [m.start() for m in re.finditer(r"(?<!bool)NegarFueraDeDemo\(", c)]
    con_if = [m.start() + 3 for m in re.finditer(re.escape(f"if({LLAMADA})"), c)]
    assert todas == con_if, f"NegarFueraDeDemo se llama fuera de if({LLAMADA})"
    return [bloque(c, p) for p in con_if]


def comprobar_negativa(src_ea: str, src_includes: str, src_medir: str) -> None:
    """D2a y el punto 1 de la respuesta: la condicion, lo primero de OnInit y la segunda llamada."""
    assert condicion_de_la_capa(src_includes) == condicion_de_medir(src_medir)
    primera = primera_de_oninit(src_ea)
    assert re.search(r"return\(?INIT_FAILED\)?;", primera), (
        "la negativa de OnInit no devuelve INIT_FAILED"
    )
    bloques = bloques_de_la_negativa(src_ea + "\n" + src_includes)
    assert len(bloques) == 2, f"{len(bloques)} llamadas a la negativa: tienen que ser dos"
    assert primera in bloques
    otra = bloques[1] if bloques[0] == primera else bloques[0]
    assert "ExpertRemove();" in otra, "la segunda llamada no hace ExpertRemove()"


TIPOS = r"(?:int|long|ulong|uint|short|ushort|char|uchar|bool|string|datetime|double|float|color)"


def globales(src: str) -> list[str]:
    """Las variables declaradas al principio de una linea (las globales, por el estilo de la
    capa)."""
    codigo = sin_textos(sin_comentarios(src))
    return re.findall(
        rf"^(?:static\s+)?{TIPOS}\s+(\w+)\s*(?:\[\w*\])?\s*(?:=[^;]*)?;", codigo, re.MULTILINE
    )


def cuerpo_de(src: str, funcion: str) -> str | None:
    """El cuerpo de la funcion `funcion` definida en `src` (su tipo en la columna 0, como en la
    capa), o None si no esta."""
    codigo = sin_textos(sin_comentarios(src))
    m = re.search(rf"^\w[\w ]*?\s+{funcion}\s*\([^;{{]*\)\s*\{{", codigo, re.MULTILINE)
    return None if m is None else bloque(codigo, m.start())


def sin_la_negativa(cuerpo: str) -> str:
    """El cuerpo de `OnInit` sin el `if` de la negativa con que empieza (con bloque o sin el)."""
    c = cuerpo.lstrip()
    if not c.startswith("if"):
        return cuerpo
    a = c.index("(")
    nivel = 0
    for j in range(a, len(c)):
        nivel += {"(": 1, ")": -1}.get(c[j], 0)
        if nivel == 0:
            break
    resto = c[j + 1 :].lstrip()
    if resto.startswith("{"):
        return resto[len(bloque(resto, 0)) + 2 :]
    return resto[resto.index(";") + 1 :]


def tramo_recto(cuerpo: str) -> str:
    """Lo que se ejecuta siempre: el cuerpo hasta el primer `if`, `else`, `return` o bucle."""
    m = re.search(r"\b(?:if|else|return|while|for|do|switch)\b", cuerpo)
    return cuerpo if m is None else cuerpo[: m.start()]


def globales_sin_reiniciar(src_ea: str, src_includes: str) -> list[str]:
    """Al cambiar el simbolo o el marco del grafico el EA no se recarga: el terminal llama a
    `OnDeinit` y a `OnInit`, pero «values of global variables and static variables are not reset»
    (<https://www.mql5.com/en/docs/runtime/running>, consultada el 2026-10-20). Medido en la demo
    del 2026-10-20 (EA-CONEXION.md, fase 3): una global que se quedo en `true` dejo dos arranques
    sin cuenta, reloj ni sesiones. Cada global tiene que asignarse en `OnInit` o en una funcion a
    la que `OnInit` llame directamente, y SIN CONDICION: solo cuenta el tramo recto de cada
    cuerpo, antes del primer `if`, `return` o bucle (en `OnInit`, despues de la negativa). La
    primera version
    contaba cualquier asignacion y no cazaba el defecto: el `g_cuenta_leida = true;` de
    `AlConectar`, detras de su `if`, pasaba por reinicio."""
    oninit = cuerpo_de(src_ea, "OnInit")
    assert oninit is not None, "no hay OnInit"
    cuerpos = [tramo_recto(sin_la_negativa(oninit))]
    for llamada in set(re.findall(r"\b(\w+)\s*\(", cuerpos[0])):
        for src in (src_ea, src_includes):
            cuerpo = cuerpo_de(src, llamada)
            if cuerpo is not None:
                cuerpos.append(tramo_recto(cuerpo))
    texto = "\n".join(cuerpos)
    asignadas = set(re.findall(r"\b(\w+)\s*=(?!=)", texto))
    asignadas |= set(re.findall(r"\bArray(?:Free|Resize)\(\s*(\w+)", texto))
    return [g for g in globales(src_ea) + globales(src_includes) if g not in asignadas]


def cifras_y_nombres(src: str) -> list[str]:
    """D2g: decimales, instrumentos o firmas en el codigo, y `#define` fuera de la lista."""
    codigo = sin_comentarios(src)
    malos = re.findall(r"(?<![\w.])\d+\.\d*(?:[eE][-+]?\d+)?|(?<![\w.])\.\d+", sin_textos(codigo))
    malos += TEXTOS_PROHIBIDOS.findall(codigo)
    malos += [d for d in re.findall(r"#define\s+(\w+)", codigo) if d not in DEFINES_PERMITIDOS]
    return malos


# --- fuentes de ejemplo -------------------------------------------------------------------------

INCLUDE_BUENO = """
// la negativa: misma condicion que MedirDemoFTMO.mq5:759
bool NegarFueraDeDemo(const long modo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)modo != ACCOUNT_TRADE_MODE_DEMO)
      return true;
   return false;
  }
"""
EA_BUENO = """
#define VERSION_EA "1.0"
#define LATIDO_SEG 60
int OnInit()
  {
   if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))
     {
      Print("no es DEMO"); // OrderSend( en un comentario no cuenta
      return(INIT_FAILED);
     }
   EventSetTimer(LATIDO_SEG);
   Print("OrderSend(\\"texto\\")");
   return(INIT_SUCCEEDED);
  }
void AlConectar()
  {
   if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))
     {
      Escribir("negativa");
      ExpertRemove();
      return;
     }
  }
"""
MEDIR_EJEMPLO = """
bool Comprobaciones(string &motivo)
  {
   if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)
     {
      motivo = "la cuenta NO es DEMO";
      return false;
     }
   return true;
  }
"""


def test_la_lista_de_trading_es_la_de_la_documentacion() -> None:
    assert len(FUNCIONES_DE_TRADING) == len(set(FUNCIONES_DE_TRADING)) == 33
    assert not LECTURA_PERMITIDA


def test_trading_en_los_dos_sentidos() -> None:
    assert llamadas_de_trading(EA_BUENO + INCLUDE_BUENO) == []
    for malo in (
        "void F(){ MqlTradeRequest r; MqlTradeResult s; OrderSend(r, s); }",
        "void F(){ OrderSendAsync (r, s); }",
        "void F(){ int n = PositionsTotal(); }",
        "void F(){ HistorySelect(0, 1); }",
        "CTrade t;",
        "#include <Trade\\Trade.mqh>",
        '#include "Trade/Trade.mqh"',
    ):
        assert llamadas_de_trading(malo), malo
    for bueno in (
        "// OrderSend(r, s);",
        "/* CTrade t; */",
        'Print("OrderSend(");',
        "void MiOrderSendX(){}",
    ):
        assert llamadas_de_trading(bueno) == [], bueno


def test_la_condicion_de_medir_se_lee_del_fichero_real() -> None:
    real = condicion_de_medir(MEDIR.read_text(encoding="utf-8"))
    assert real == "(ENUM_ACCOUNT_TRADE_MODE)<MODO>!=ACCOUNT_TRADE_MODE_DEMO"
    assert real == condicion_de_medir(MEDIR_EJEMPLO)


def test_la_negativa_en_los_dos_sentidos() -> None:
    comprobar_negativa(EA_BUENO, INCLUDE_BUENO, MEDIR_EJEMPLO)
    rotos = {
        "otra condicion": (EA_BUENO, INCLUDE_BUENO.replace("!=", "=="), MEDIR_EJEMPLO),
        "sin el cast": (
            EA_BUENO,
            INCLUDE_BUENO.replace("(ENUM_ACCOUNT_TRADE_MODE)modo", "modo"),
            MEDIR_EJEMPLO,
        ),
        "otra cuenta": (EA_BUENO, INCLUDE_BUENO.replace("_DEMO", "_CONTEST"), MEDIR_EJEMPLO),
        "hace algo mas": (
            EA_BUENO,
            INCLUDE_BUENO.replace("return true;", "Print(1); return true;"),
            MEDIR_EJEMPLO,
        ),
        "no es lo primero": (
            EA_BUENO.replace("int OnInit()\n  {\n", "int OnInit()\n  {\n   Print(0);\n"),
            INCLUDE_BUENO,
            MEDIR_EJEMPLO,
        ),
        "no devuelve INIT_FAILED": (
            EA_BUENO.replace("return(INIT_FAILED);", "return(INIT_SUCCEEDED);", 1),
            INCLUDE_BUENO,
            MEDIR_EJEMPLO,
        ),
        "sin ExpertRemove": (EA_BUENO.replace("ExpertRemove();", ""), INCLUDE_BUENO, MEDIR_EJEMPLO),
        "sin la segunda": (EA_BUENO.split("void AlConectar()")[0], INCLUDE_BUENO, MEDIR_EJEMPLO),
        "una tercera": (
            EA_BUENO + f"void G(){{ if({LLAMADA}) {{ ExpertRemove(); }} }}",
            INCLUDE_BUENO,
            MEDIR_EJEMPLO,
        ),
        "con otro modo": (
            EA_BUENO.replace(LLAMADA, "NegarFueraDeDemo(ACCOUNT_TRADE_MODE_DEMO)", 1),
            INCLUDE_BUENO,
            MEDIR_EJEMPLO,
        ),
        "medir cambia": (EA_BUENO, INCLUDE_BUENO, MEDIR_EJEMPLO.replace("!=", ">")),
    }
    for motivo, (ea, inc, medir) in rotos.items():
        with pytest.raises(AssertionError):
            comprobar_negativa(ea, inc, medir)
            pytest.fail(f"no lo caza: {motivo}")  # pragma: no cover


def test_cifras_y_nombres_en_los_dos_sentidos() -> None:
    assert cifras_y_nombres(EA_BUENO + INCLUDE_BUENO) == []
    for malo in (
        "double lote = 0.01;",
        "double m = .5;",
        'string s = "EURUSD";',
        "#define MAGICO 57057000",
        '// nada\nstring f = "FTMO";',
    ):
        assert cifras_y_nombres(malo), malo
    for bueno in ("// EURUSD y 0.8 en un comentario", 'string v = "1.0";', "int n = 32;"):
        assert cifras_y_nombres(bueno) == [], bueno


EA_CON_GLOBALES = """
datetime g_ultimo = 0;
bool     g_leida = false;
int OnInit()
  {
   if(NegarFueraDeDemo(AccountInfoInteger(ACCOUNT_TRADE_MODE)))
      return(INIT_FAILED);
   g_leida = false;
   g_ultimo = 0;
   string c = Abrir("x");
   Conectar();
   return(INIT_SUCCEEDED);
  }
void Conectar()
  {
   if(g_leida)
      return;
   g_leida = true;
  }
void Otra()
  {
   g_dia = "";
  }
"""
INCLUDE_CON_GLOBALES = """
string g_dia = "";
long   g_seq = 0;
uchar  g_buf[];
string Abrir(const string carpeta)
  {
   g_dia = "";
   g_seq = 0;
   ArrayFree(g_buf);
   g_buf[0] = 0;
   return "ninguna";
  }
"""


def test_las_globales_se_reinician_en_los_dos_sentidos() -> None:
    assert globales(EA_CON_GLOBALES) == ["g_ultimo", "g_leida"]
    assert globales(INCLUDE_CON_GLOBALES) == ["g_dia", "g_seq", "g_buf"]
    assert globales_sin_reiniciar(EA_CON_GLOBALES, INCLUDE_CON_GLOBALES) == []
    rotos = {
        "la del EA, sin reiniciar (el defecto del 2026-10-20)": (
            EA_CON_GLOBALES.replace("\n   g_leida = false;\n", "\n"),
            INCLUDE_CON_GLOBALES,
            ["g_leida"],
        ),
        "solo comparada, no asignada": (
            EA_CON_GLOBALES.replace(
                "\n   g_leida = false;\n", "\n   bool b = (g_leida == false);\n"
            ),
            INCLUDE_CON_GLOBALES,
            ["g_leida"],
        ),
        "OnInit no llama a la funcion que reinicia": (
            EA_CON_GLOBALES.replace('string c = Abrir("x");', ""),
            INCLUDE_CON_GLOBALES,
            ["g_dia", "g_seq", "g_buf"],
        ),
        "reiniciada solo en otra funcion": (
            EA_CON_GLOBALES,
            INCLUDE_CON_GLOBALES.replace('   g_dia = "";\n', ""),
            ["g_dia"],
        ),
        "reiniciada detras de un if": (
            EA_CON_GLOBALES.replace("int OnInit()", "void Q()\n  {\n  }\nint OnInit()").replace(
                "\n   g_leida = false;\n   g_ultimo = 0;\n",
                "\n   g_ultimo = 0;\n   if(Q())\n      g_leida = false;\n",
            ),
            INCLUDE_CON_GLOBALES,
            ["g_leida", "g_dia", "g_seq", "g_buf"],
        ),
        "una global nueva": (
            EA_CON_GLOBALES.replace("int OnInit()", "int g_nueva = 0;\nint OnInit()"),
            INCLUDE_CON_GLOBALES,
            ["g_nueva"],
        ),
    }
    for motivo, (ea, inc, esperadas) in rotos.items():
        assert globales_sin_reiniciar(ea, inc) == esperadas, motivo


def test_la_segunda_llamada_puede_ir_antes_en_el_fichero() -> None:
    oninit, resto = EA_BUENO.split("void AlConectar()")
    comprobar_negativa("void AlConectar()" + resto + oninit, INCLUDE_BUENO, MEDIR_EJEMPLO)


# --- la capa de verdad ---------------------------------------------------------------------------

EA = "mql5/Experts/Botsito.mq5"
LA_CAPA = {
    EA,
    "mql5/Include/Botsito/Capa/Cuenta.mqh",
    "mql5/Include/Botsito/Capa/Journal.mqh",
    "mql5/Include/Botsito/Capa/Reloj.mqh",
    "mql5/Include/Botsito/Capa/Sesiones.mqh",
    "mql5/Scripts/BotsitoPruebasCapa.mq5",
}


def _capa() -> dict[str, str]:
    ficheros = sorted(
        p
        for c in CARPETAS_DE_LA_CAPA
        for p in (RAIZ / c).rglob("*")
        if p.suffix.lower() in (".mq5", ".mqh")
    )
    return {p.relative_to(RAIZ).as_posix(): p.read_bytes().decode("utf-8") for p in ficheros}


def test_la_capa_son_los_ficheros_de_r6a1() -> None:
    """Si aparece otro fichero, este test lo nombra: las comprobaciones de abajo lo cubren igual,
    pero la lista se amplia a mano, para que nadie anada capa sin mirarla."""
    assert set(_capa()) == LA_CAPA


def test_la_capa_no_llama_a_ninguna_funcion_de_trading() -> None:
    for nombre, texto in _capa().items():
        assert llamadas_de_trading(texto) == [], nombre


def test_la_negativa_de_la_capa_es_la_de_medir_y_va_lo_primero() -> None:
    capa = _capa()
    includes = "\n".join(t for n, t in capa.items() if n.startswith("mql5/Include/"))
    comprobar_negativa(capa[EA], includes, MEDIR.read_text(encoding="utf-8"))


def test_el_ea_reinicia_sus_globales_en_oninit() -> None:
    capa = _capa()
    includes = "\n".join(t for n, t in capa.items() if n.startswith("mql5/Include/"))
    assert globales(capa[EA]), "el EA no declara globales: la comprobacion no comprobaria nada"
    assert globales_sin_reiniciar(capa[EA], includes) == []


def test_la_capa_no_lleva_cifras_ni_nombres_a_mano() -> None:
    for nombre, texto in _capa().items():
        assert cifras_y_nombres(texto) == [], nombre


def test_la_capa_es_utf8_sin_bom_y_lf() -> None:
    """MetaEditor lee UTF-8 sin BOM (medido, EA-CONEXION.md §0.a)."""
    for nombre in LA_CAPA:
        b = (RAIZ / nombre).read_bytes()
        assert not b.startswith(b"\xef\xbb\xbf") and b"\r" not in b, nombre
