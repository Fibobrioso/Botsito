"""Simula las lineas preparadas para el commit del contrato del cierre de
`trabajo/metodo-fidelidad-rentabilidad` (METODO-FIDELIDAD-RENTABILIDAD.md §1.4; respuesta del
consultor a la PARADA, «En las lineas del cierre»): R sale HECHA con su registro en HISTORIA (la
letra ya tenia uno, del 2026-10-05; este lleva su fecha), F se reescribe con el texto de la
respuesta, G nombra lo que ADR-0092 le deja, la segunda Regla viva se sustituye con la redaccion
del punto 5; en la hoja de ruta, R3.7 HECHA sin `NA:R`, una entrada nueva R3.8 (la cuenta por mes,
antes de la re-corrida), R5.1 con A-16 medida, R5.2 sin `NA:R` y una entrada nueva R5.6 (la medida
de rentabilidad sobre junio-noviembre de 2025 con las condiciones del punto 4). Como
`anexos/SELLO-RESPALDO-M1/simular_cierre.py`: contra tests/unit/test_hoja_de_ruta.py (a, b y c) y
tests/unit/test_project_state.py, cargados por su ruta LITERAL.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la raiz del repo) y
aplica en memoria sustituciones exactas (cada una casa UNA vez). Las comprobaciones de PROJECT_STATE
corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar. En el repo no
escribe nada. Ademas simula el Current Feature que escribe el ritual, para medir los bytes.

    uv run python -B docs/validation/anexos/METODO-FIDELIDAD-RENTABILIDAD/simular_cierre.py
"""

# ruff: noqa: E501  (las sustituciones son literales de los documentos: tienen que casar tal cual)
from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import tempfile
from pathlib import Path
from types import ModuleType


def _modulo(spec: importlib.machinery.ModuleSpec | None) -> ModuleType:
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


thr = _modulo(importlib.util.spec_from_file_location("thr", "tests/unit/test_hoja_de_ruta.py"))
tps = _modulo(importlib.util.spec_from_file_location("tps", "tests/unit/test_project_state.py"))

FECHA = "2026-11-0X"  # la del cierre
raiz = Path.cwd()
ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: R sale HECHA (a HISTORIA, con su registro)
linea_r = next(x for x in ps.splitlines() if x.startswith("R. "))
ps = cambiar(ps, "\n\n" + linea_r + "\n", "\n")
historia += (
    f"\n# Next Action HECHA · R · el método de juicio del bot · sale de PROJECT_STATE.md en "
    f"trabajo/metodo-fidelidad-rentabilidad ({FECHA})\n\n"
    "Su texto literal (la letra ya tenía un registro HECHA, el de trabajo/ventana-ev-v9-003456, del "
    "2026-10-05; este lleva su fecha, DECISIONES-DE-PROCESO.md:29):\n\n"
    + linea_r
    + "\n\nHECHA en `trabajo/metodo-fidelidad-rentabilidad` (docs/validation/METODO-FIDELIDAD-RENTABILIDAD.md): "
    "ADR-0092 (enmienda ADR-0043, ADR-0070 y ADR-0053 §6) fija la fidelidad por criterios (en cascada "
    "contra las órdenes del bot, sin umbral) como herramienta de construcción y la rentabilidad como "
    "puerta para operar en vivo, pre-registrada por el consultor antes de ninguna corrida nueva: N ≥ 100, "
    "esperanza ≥ +0,10 R neta, percentil 5 del remuestreo por días > 0, pérdida diaria < 3 %, equity "
    "≥ 94 %, sin suspensión, en la fase fondeada, sobre junio-noviembre de 2025 una sola vez y con el "
    "deslizamiento pendiente de F17; una cuenta por mes en construcción (trabajo/cuenta-por-mes). "
    "A-16 medida en construcción (mediana 0 puntos, el 92,4 % dentro de la M1 de Dukascopy): la regla "
    "del punto 7 no se dispara y A-16 sigue ABIERTA.\n"
)
# F: el texto de la respuesta; el resto de F, igual
ps = cambiar(
    ps,
    "Siguiente: R y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3) y con el sello del respaldo de ADR-0091;",
    "Siguiente: la rama de la cuenta por mes (ADR-0092, trabajo/cuenta-por-mes) y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091 y el método de ADR-0092;",
)
# G: lo que ADR-0092 le deja
ps = cambiar(
    ps,
    "la regla del objetivo frente al material, ADR-0073) y A-16.",
    "la regla del objetivo frente al material, ADR-0073) y A-16 (medida en R3.7, sigue ABIERTA). Y lo de ADR-0092: PREREGISTRO §«Que tiene que llevar» y MASTER_PLAN §H (y la fila de F30) con la rentabilidad (ADR-0092 §13).",
)
# la segunda Regla viva, con la redaccion del punto 5
ps = cambiar(
    ps,
    "- La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.",
    "- La rentabilidad pre-registrada de ADR-0092, medida una vez sobre meses que el bot no ha visto, precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos), y la fidelidad sigue siendo la herramienta de construcción; la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.",
)

# --- La hoja de ruta
hoja = cambiar(
    hoja,
    "- **Refs:** NA:R · ID:ADR-0043 · ID:ADR-0070 · ID:A-16 · F:F27\n",
    "- **Refs:** ID:ADR-0092 · ID:ADR-0043 · ID:ADR-0070 · ID:A-16 · F:F27\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** el ADR está aceptado con los umbrales pre-registrados y la medida de los\n"
    "  cuatro sesgos tiene su informe.\n",
    "- **Hecho cuando:** el ADR está aceptado con los umbrales pre-registrados y la medida de los\n"
    "  cuatro sesgos tiene su informe.\n"
    "- **Estado:** HECHA (`trabajo/metodo-fidelidad-rentabilidad`; METODO-FIDELIDAD-RENTABILIDAD.md):\n"
    "  ADR-0092 fija la fidelidad por criterios para construir y la rentabilidad como puerta para\n"
    "  operar en vivo, con sus umbrales; A-16 medida (mediana 0 puntos, 92,4 % dentro de la M1).\n"
    "\n"
    "### R3.8 · Una cuenta por mes en la corrida que cuenta\n"
    "- **Refs:** NA:F · ID:ADR-0092 · ID:ADR-0053 · ID:ADR-0070\n"
    "- **Qué es:** en construcción (y en mayo cuando se mida) la cuenta es una por mes, no\n"
    "  arrastrada entre meses no contiguos (ADR-0092 §8, que enmienda ADR-0053 §6 y la condición\n"
    "  de la corrida que cuenta de ADR-0070); una condición del recorrido, no una opción:\n"
    "  `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` no cambia. Rama de motor corta, `trabajo/cuenta-por-mes`,\n"
    "  ANTES de la re-corrida que cuenta, con un test que rompe en `main`.\n"
    "- **Depende de:** R3.7.\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** la cuenta empieza de nuevo en cada mes de construcción, con su test, y la\n"
    "  re-corrida que cuenta puede correr.\n",
)
hoja = cambiar(
    hoja,
    "  objetivo; A-16 (Oanda frente a Dukascopy), que se mide antes, en R3.7; y, al elegir los\n",
    "  objetivo; A-16 (Oanda frente a Dukascopy), medida en R3.7 (METODO-FIDELIDAD-RENTABILIDAD.md\n"
    "  §1.3) y ABIERTA; y, al elegir los\n",
)
hoja = cambiar(
    hoja,
    "  rama de medida (ADR-0070 §6); y NA:R, el método (R3.7). El sello del respaldo M1 (R3.6)\n  está HECHO (ADR-0091).\n",
    "  rama de medida (ADR-0070 §6); y la cuenta por mes (R3.8). El sello del respaldo M1 (R3.6)\n  y el método (R3.7, ADR-0092) están HECHOS.\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** F26 y F27 tienen informe con su cifra contra el umbral pre-registrado.\n",
    "- **Hecho cuando:** F26 y F27 tienen informe con su cifra contra el umbral pre-registrado.\n"
    "\n"
    "### R5.6 · La rentabilidad, la puerta para operar en vivo\n"
    "- **Refs:** NA:G · NA:N · HER:7 · HER:9 · HER:10 · ID:ADR-0092 · F:F27\n"
    "- **Qué es:** la medida de rentabilidad de ADR-0092 §3, UNA vez, sobre junio a noviembre de\n"
    "  2025 (y su extensión, de uno en uno y solo si N no llega), en la fase fondeada y con la cuenta\n"
    "  arrastrada, por su propia rama con su ADR y su comando (ADR-0070 punto 6: hoy no existe).\n"
    "  Antes: la spec sellada en PREREGISTRO (G); el calendario de cierres renovado hacia atrás hasta\n"
    "  enero de 2025 (NA:N, condición 1); las velas M1 y los ticks de esos meses, bajados y declarados\n"
    "  según los heredados 7 y 9; el riesgo del spread supuesto por la hora de pared (Technical Debt)\n"
    "  en noviembre y en la extensión de invierno; y la construcción en el umbral de ADR-0070. La\n"
    "  puerta no da «pasa» antes de F17 (el deslizamiento, heredado 10).\n"
    "- **Depende de:** R5.1 (G) y la re-corrida que cuenta en el umbral de ADR-0070 (R3.8 y R5.2).\n"
    "- **Quién:** la sesión, con el encargo del consultor; la decisión de operar, Aleks (F35).\n"
    "- **Hecho cuando:** la medida está en su informe con el veredicto de ADR-0092 §3 y §4.\n",
)

# --- Las comprobaciones (ADR-0092 ya existe)
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
print(
    f"R viva en la copia? {'R' in thr.entradas_vivas(ps)}; R HECHA en HISTORIA? "
    f"{'R' in thr.letras_hechas(historia)}; NA:R en la hoja simulada? {'NA:R' in hoja}"
)
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
cf_actual = ps.split("## Current Feature\n", 1)[1].split("\n\n", 1)[0]
cf_cierre = (
    "Ninguna rama abierta. trabajo/metodo-fidelidad-rentabilidad cerrada en main el 2026-11-0X "
    "(stable/F38r-metodo-fidelidad-rentabilidad): el método con el que se juzga al bot (ADR-0092), "
    "fidelidad por criterios para construir y rentabilidad pre-registrada como puerta para operar en "
    "vivo; A-16 medida."
)
ps_cierre = ps.replace(cf_actual, cf_cierre, 1)
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano = (copia / "PROJECT_STATE.md").stat().st_size
    (copia / "PROJECT_STATE.md").write_text(ps_cierre, encoding="utf-8", newline="\n")
    tamano_cierre = (copia / "PROJECT_STATE.md").stat().st_size
    print(
        f"PROJECT_STATE con las lineas del cierre: {tamano} bytes (wc -c de la copia); con el "
        f"Current Feature del cierre: {tamano_cierre}; los cuatro tests de test_project_state: ok"
    )
    if max(tamano, tamano_cierre) >= 23_000:
        print("POR ENCIMA de la alerta de 23.000 del consultor", file=sys.stderr)
        sys.exit(1)
