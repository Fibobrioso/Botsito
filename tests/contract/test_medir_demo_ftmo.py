"""El script de la demo de FTMO (`tools/mql5/MedirDemoFTMO.mq5`) envia ordenes a una cuenta de
prueba: lo que cada funcion que abre o coloca tiene que llevar, leido en el fuente (rama
`trabajo/margen-pendiente`, 2026-10-31; respuesta del consultor a la PARADA, MARGEN-PENDIENTE.md).

Niega por defecto: toda funcion que rellena una peticion `TRADE_ACTION_DEAL` o
`TRADE_ACTION_PENDING` lleva el numero magico; lleva stop de proteccion (`.sl`) y, si es pendiente,
la caducidad (`PonerCaducidad`), salvo las de la lista cerrada `SIN_STOP`, cada una con su motivo.
Una funcion nueva fuera de la lista tiene que cumplir. Y la condicion DEMO sigue en la linea 759,
que citan ADR-0082 y `mql5/Include/Botsito/Capa/Cuenta.mqh`, con el paso 8 detras de ella."""

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
ACCION = re.compile(r"\b(\w+)\.action\s*=\s*TRADE_ACTION_(DEAL|PENDING)\b")


def funciones(texto: str) -> dict[str, str]:
    """Cada funcion del fuente con su cuerpo: de su cabecera a la siguiente."""
    salida: dict[str, str] = {}
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
                salida[nombre] = "\n".join(cuerpo)
            nombre, cuerpo = m.group(1), [linea]
        elif nombre is not None:
            cuerpo.append(linea)
    if nombre is not None:
        salida[nombre] = "\n".join(cuerpo)
    return salida


def problemas(texto: str) -> list[str]:
    """Lo que falta en cada funcion que abre o coloca; vacio si todo cumple."""
    salida = []
    for nombre, cuerpo in funciones(texto).items():
        for var, accion in sorted(set(ACCION.findall(cuerpo))):
            if not re.search(rf"\b{var}\.magic\s*=", cuerpo):
                salida.append(f"{nombre}: {accion} sin {var}.magic")
            if nombre in SIN_STOP:
                if accion == "PENDING" and f"PonerCaducidad({var})" not in cuerpo:
                    salida.append(f"{nombre}: PENDING sin PonerCaducidad({var})")
                continue
            if not re.search(rf"\b{var}\.sl\s*=", cuerpo):
                salida.append(f"{nombre}: {accion} sin {var}.sl (stop de proteccion)")
            if accion == "PENDING" and f"PonerCaducidad({var})" not in cuerpo:
                salida.append(f"{nombre}: PENDING sin PonerCaducidad({var})")
    return salida


def _texto() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_toda_funcion_que_abre_o_coloca_lleva_magico_stop_y_caducidad() -> None:
    assert problemas(_texto()) == []


def test_las_que_envian_son_las_conocidas_y_la_lista_sin_stop_es_cerrada() -> None:
    """Si nace otra funcion que envia, este test la nombra: que cumpla (o se discuta su motivo)."""
    envian = sorted(n for n, c in funciones(_texto()).items() if ACCION.search(c))
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


def _sin(texto: str, funcion: str, quitar: str) -> str:
    cuerpo = funciones(texto)[funcion]
    assert quitar in cuerpo, (funcion, quitar)
    return texto.replace(cuerpo, cuerpo.replace(quitar, "", 1), 1)


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
