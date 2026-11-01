"""El script de la demo de FTMO (`tools/mql5/MedirDemoFTMO.mq5`) envia ordenes a una cuenta de
prueba: lo que cada funcion que abre o coloca tiene que llevar, leido en el fuente (rama
`trabajo/margen-pendiente`, 2026-10-31; respuesta del consultor a la PARADA, MARGEN-PENDIENTE.md).

Niega por defecto: toda funcion que llama a `OrderSend` con una peticion `TRADE_ACTION_DEAL` o
`TRADE_ACTION_PENDING` lleva el numero magico; lleva stop de proteccion (`.sl`, y no a 0) y, si es
pendiente, la caducidad (`PonerCaducidad`), salvo el stop las de la lista cerrada `SIN_STOP`, cada
una con su motivo. Una peticion cuya accion no se lee escrita tal cual en la funcion (una variable,
o ninguna) es un problema; una sobrecarga se mira aparte. Una funcion nueva fuera de la lista tiene
que cumplir. Y la condicion DEMO sigue en la linea 759, que citan ADR-0082 y
`mql5/Include/Botsito/Capa/Cuenta.mqh`, con el paso 8 detras de ella. (Endurecido tras el revisor,
hallazgo b2: el stop a 0, la sobrecarga y la accion por variable pasaban.)"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "tools" / "mql5" / "MedirDemoFTMO.mq5"

# Las unicas que envian sin stop de proteccion, y por que. Lista cerrada: no se amplia sin motivo.
SIN_STOP = {
    "EnviarPendiente": "los pasos 3, 4 y 5 miden pendientes sin stop a proposito, para que solo se"
    " juzgue su precio; si una se llena, ProbarPendiente o ModificarCruzando la cierran al leerla",
    "CerrarPosicion": "es un cierre de una posicion existente (`req.position`), no abre nada",
}
LINEA_DEMO = 759
CONDICION_DEMO = (
    "if((ENUM_ACCOUNT_TRADE_MODE)AccountInfoInteger(ACCOUNT_TRADE_MODE) != ACCOUNT_TRADE_MODE_DEMO)"
)
# una cabecera de funcion: empieza en la columna 0 con un tipo y un nombre seguido de «(», y no
# acaba en «;» (eso seria una global o un prototipo)
CABECERA = re.compile(r"^[A-Za-z_]\w*(?:\s+[A-Za-z_]\w*)*\s+([A-Za-z_]\w*)\s*\(")
# lo que envia al servidor: OrderSend con la peticion que se le pasa
ENVIA = re.compile(r"\bOrderSend\s*\(\s*(\w+)")
# las acciones que no abren ni colocan nada: quitar una pendiente y moverla
SIN_COMPROBAR = frozenset({"TRADE_ACTION_REMOVE", "TRADE_ACTION_MODIFY"})
QUE_ABREN = {"TRADE_ACTION_DEAL": "DEAL", "TRADE_ACTION_PENDING": "PENDING"}


def funciones(texto: str) -> list[tuple[str, str]]:
    """Cada funcion del fuente con su cuerpo, de su cabecera a la siguiente; una sobrecarga (el
    mismo nombre dos veces) sale dos veces, no pisa a la otra."""
    salida: list[tuple[str, str]] = []
    nombre: str | None = None
    cuerpo: list[str] = []
    for linea in texto.split("\n"):
        m = CABECERA.match(linea)
        es_cabecera = (
            m is not None
            and not linea.startswith(("input ", "#"))
            and not linea.rstrip().endswith(";")
        )
        if es_cabecera and m is not None:
            if nombre is not None:
                salida.append((nombre, "\n".join(cuerpo)))
            nombre, cuerpo = m.group(1), [linea]
        elif nombre is not None:
            cuerpo.append(linea)
    if nombre is not None:
        salida.append((nombre, "\n".join(cuerpo)))
    return salida


def peticiones(cuerpo: str) -> list[tuple[str, str]]:
    """(variable, accion) de cada OrderSend del cuerpo: la accion es lo que se asigna a su
    `.action`, tal cual; sin asignacion, «(sin .action)»."""
    salida = []
    for var in sorted(set(ENVIA.findall(cuerpo))):
        acciones = re.findall(rf"\b{var}\.action\s*=\s*([^;]+);", cuerpo)
        salida += [(var, a.strip()) for a in acciones] or [(var, "(sin .action)")]
    return salida


def problemas(texto: str) -> list[str]:
    """Lo que falta en cada funcion que envia; vacio si todo cumple. Niega por defecto: una
    peticion cuya accion no es una de las conocidas, escrita tal cual, es un problema."""
    salida = []
    for nombre, cuerpo in funciones(texto):
        for var, accion in peticiones(cuerpo):
            if accion in SIN_COMPROBAR:
                continue
            if accion not in QUE_ABREN:
                salida.append(
                    f"{nombre}: OrderSend({var}) con una accion que no se puede leer: {accion}"
                )
                continue
            tipo = QUE_ABREN[accion]
            if not re.search(rf"\b{var}\.magic\s*=", cuerpo):
                salida.append(f"{nombre}: {tipo} sin {var}.magic")
            if tipo == "PENDING" and f"PonerCaducidad({var})" not in cuerpo:
                salida.append(f"{nombre}: PENDING sin PonerCaducidad({var})")
            if nombre in SIN_STOP:
                continue
            con_stop = re.search(rf"\b{var}\.sl\s*=", cuerpo)
            stop_cero = re.search(rf"\b{var}\.sl\s*=\s*0(?:\.0*)?\s*;", cuerpo)
            if not con_stop or stop_cero:
                salida.append(f"{nombre}: {tipo} sin {var}.sl (stop de proteccion)")
    return salida


def que_envian(texto: str) -> list[str]:
    """Las funciones con una peticion que abre o coloca (o que no se puede leer)."""
    return sorted(
        {
            nombre
            for nombre, cuerpo in funciones(texto)
            for _, accion in peticiones(cuerpo)
            if accion not in SIN_COMPROBAR
        }
    )


def _texto() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_toda_funcion_que_abre_o_coloca_lleva_magico_stop_y_caducidad() -> None:
    assert problemas(_texto()) == []


def test_las_que_envian_son_las_conocidas_y_la_lista_sin_stop_es_cerrada() -> None:
    """Si nace otra funcion que envia, este test la nombra: que cumpla (o se discuta su motivo)."""
    envian = que_envian(_texto())
    assert envian == [
        "AbrirCompra",
        "CerrarPosicion",
        "ColocarBuyStop",
        "EnviarPendiente",
        "MedirComision",
        "MedirLlenadoStop",
    ]
    assert set(SIN_STOP) <= set(envian)


def test_la_condicion_demo_sigue_en_la_759_y_el_paso_8_va_detras() -> None:
    lineas = _texto().split("\n")
    assert lineas[LINEA_DEMO - 1].strip() == CONDICION_DEMO
    texto = "\n".join(lineas)
    assert texto.index("bool Comprobaciones(") < texto.index("bool MedirMargen(")
    inicio = texto[texto.index("void OnStart()") :]
    assert inicio.index("Comprobaciones(motivo)") < inicio.index("MedirMargen()")


# --- que el test rompe de verdad: el fuente real, estropeado a proposito en memoria


def _cuerpo(texto: str, funcion: str) -> str:
    return next(c for n, c in funciones(texto) if n == funcion)


def _sin(texto: str, funcion: str, quitar: str, poner: str = "") -> str:
    cuerpo = _cuerpo(texto, funcion)
    assert quitar in cuerpo, (funcion, quitar)
    return texto.replace(cuerpo, cuerpo.replace(quitar, poner, 1), 1)


@pytest.mark.parametrize(
    ("funcion", "quitar", "esperado"),
    [
        ("ColocarBuyStop", "   req.sl = NormalizeDouble(precio - stop * g_point, g_digits);\n",
         "ColocarBuyStop: PENDING sin req.sl"),
        ("AbrirCompra", "   req.sl = NormalizeDouble(t.ask - stop * g_point, g_digits);\n",
         "AbrirCompra: DEAL sin req.sl"),
        ("ColocarBuyStop", "   PonerCaducidad(req);\n",
         "ColocarBuyStop: PENDING sin PonerCaducidad"),
        ("AbrirCompra", "   req.magic = MAGICO;\n", "AbrirCompra: DEAL sin req.magic"),
        ("EnviarPendiente", "   PonerCaducidad(req);\n",
         "EnviarPendiente: PENDING sin PonerCaducidad"),
    ],
)  # fmt: skip
def test_rompe_si_falta_el_stop_la_caducidad_o_el_magico(
    funcion: str, quitar: str, esperado: str
) -> None:
    rotos = problemas(_sin(_texto(), funcion, quitar))
    assert any(p.startswith(esperado) for p in rotos), rotos


def test_rompe_con_una_funcion_nueva_que_envia_sin_stop() -> None:
    nueva = (
        "\nbool AbrirSinStop(const double volumen)\n  {\n   MqlTradeRequest r;\n"
        "   MqlTradeResult s;\n   ZeroMemory(r);\n   r.action = TRADE_ACTION_DEAL;\n"
        "   r.magic = MAGICO;\n"
        "   r.volume = volumen;\n   return OrderSend(r, s);\n  }\n"
    )
    texto = _texto().replace("void OnStart()", nueva + "\nvoid OnStart()", 1)
    assert problemas(texto) == ["AbrirSinStop: DEAL sin r.sl (stop de proteccion)"]


# --- las tres roturas que encontro el revisor (MARGEN-PENDIENTE.md, b2): ninguna pasa ya


def test_rompe_con_un_stop_a_cero() -> None:
    sl = "   req.sl = NormalizeDouble(t.ask - stop * g_point, g_digits);\n"
    texto = _sin(_texto(), "AbrirCompra", sl, "   req.sl = 0.0;\n")
    assert problemas(texto) == ["AbrirCompra: DEAL sin req.sl (stop de proteccion)"]


def test_rompe_con_una_sobrecarga_del_mismo_nombre_sin_stop() -> None:
    sobrecarga = (
        "\nbool ColocarBuyStop(const double volumen)\n  {\n   MqlTradeRequest r;\n"
        "   MqlTradeResult s;\n   ZeroMemory(r);\n   r.action = TRADE_ACTION_PENDING;\n"
        "   r.magic = MAGICO;\n   PonerCaducidad(r);\n   return OrderSend(r, s);\n  }\n"
    )
    texto = _texto().replace("void OnStart()", sobrecarga + "\nvoid OnStart()", 1)
    assert problemas(texto) == ["ColocarBuyStop: PENDING sin r.sl (stop de proteccion)"]


def test_rompe_con_una_accion_puesta_por_variable() -> None:
    nueva = (
        "\nbool EnviarCualquiera(const ENUM_TRADE_REQUEST_ACTIONS acc)\n  {\n"
        "   MqlTradeRequest r;\n   MqlTradeResult s;\n   ZeroMemory(r);\n"
        "   r.action = acc;\n   r.magic = MAGICO;\n"
        "   return OrderSend(r, s);\n  }\n"
    )
    texto = _texto().replace("void OnStart()", nueva + "\nvoid OnStart()", 1)
    assert problemas(texto) == [
        "EnviarCualquiera: OrderSend(r) con una accion que no se puede leer: acc"
    ]
    assert "EnviarCualquiera" in que_envian(texto)


def test_rompe_con_un_ordersend_sin_accion_en_la_funcion() -> None:
    nueva = (
        "\nbool ReenviarPeticion(MqlTradeRequest &r)\n  {\n   MqlTradeResult s;\n"
        "   return OrderSend(r, s);\n  }\n"
    )
    texto = _texto().replace("void OnStart()", nueva + "\nvoid OnStart()", 1)
    assert problemas(texto) == [
        "ReenviarPeticion: OrderSend(r) con una accion que no se puede leer: (sin .action)"
    ]
