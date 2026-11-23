"""Simula las lineas preparadas para el cierre de `trabajo/recorrida-construccion-3`
(RECORRIDA-CONSTRUCCION-3.md §7; encargo, «Las lineas del cierre»), sin aplicarlas: la F reescrita
(sigue viva; ninguna letra sale ni entra; «R5.7 despues de (3)» sale); en la hoja de ruta, R3.10
nueva tras R3.9 y HECHA, R4.3 HECHA y sin `NA:F` (la F sigue viva en R4.2 y R4.6), R4.6 con ADR-0098
en Refs y en su «Hecho cuando», R5.7 sustituida por ADR-0098 y HECHA (sin `NA:F`), R5.2 cita R3.10
y una fila nueva en el Marcador. Como `anexos/RECORRIDA-CONSTRUCCION-2/simular_cierre.py`: contra
`tests/unit/test_hoja_de_ruta.py` (a, b y c) y `tests/unit/test_project_state.py`, cargados por su
ruta LITERAL.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la raiz del repo) y
aplica en memoria sustituciones exactas (cada una casa UNA vez). Las comprobaciones de
PROJECT_STATE corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar.
En el repo no escribe nada. Simula tambien las cabeceras que escribe el ritual y mide los bytes con
y sin la linea de Technical Debt de D7 (la decide el consultor en la PARADA final).

    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/simular_cierre.py
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


sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
thr = _modulo(importlib.util.spec_from_file_location("thr", "tests/unit/test_hoja_de_ruta.py"))
tps = _modulo(importlib.util.spec_from_file_location("tps", "tests/unit/test_project_state.py"))

raiz = Path.cwd()
ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: la F, una frase por cada cosa, sin quitar lo que sigue vivo
F_VIEJA = next(x for x in ps.splitlines() if x.startswith("F. "))
F_NUEVA = (
    "F. La sesión 7, en dos días con el método de ADR-0093 (R4.3), ingerida y ACTIVADA: la 7a (F39e: "
    "ADR-0094, A-58 abierta; break even al cierre, A-13 abierta por el margen) y la 7b (F39k: la stop "
    "cuyo 0 queda del lado malo espera, ADR-0097, A-59 abierta); A-48 y A-58, a la sesión siguiente. "
    "La corrida (3) de ADR-0070 §3 dio «no» (cobertura 15.2 %, precisión 14.4 %; "
    "RECORRIDA-CONSTRUCCION-3.md). La línea base vigente es "
    "anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt. El pivote de ADR-0093 §6, por su "
    "contingencia sobre la diaria (19 parejas de julio y 40 de más): «una sesión más». La meta de "
    "ADR-0098: salida C, el techo no gana, y manda sobre el pivote. El vídeo de mapeo (recibido el "
    "2026-11-18): SIN ABRIR y fuera del repo, no se ingiere; octubre y noviembre de 2026, "
    "reservados. C y R6a en los huecos."
)
ps = cambiar(ps, F_VIEJA + "\n", F_NUEVA + "\n")

# --- La hoja de ruta: R3.10 nueva tras R3.9
R310 = (
    "\n### R3.10 · La corrida (3): la 7b activada, sobre toda la construcción\n"
    "- **Refs:** ID:ADR-0070 · ID:ADR-0092 · ID:ADR-0097 · ID:ADR-0098\n"
    "- **Qué es:** la corrida del arnés que cuenta por ADR-0070 §3 sobre toda la construcción con el\n"
    "  motor de la 7b (F39k) y una cuenta por mes (ADR-0092 §8), con su diagnóstico de cuenta diaria,\n"
    "  los dos `diff` contra la línea base anterior, la lectura del pivote de ADR-0093 §6 y la medida\n"
    "  de la meta de ADR-0098, pre-registrada antes de correr.\n"
    "- **Depende de:** R3.9 y R4.3 (HECHAS).\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** el veredicto literal está en el informe y en ADR-0070 §3 y la línea base\n"
    "  vigente es la suya.\n"
    "- **Estado:** HECHA (`trabajo/recorrida-construccion-3`; RECORRIDA-CONSTRUCCION-3.md): «no»\n"
    "  (cobertura 15,2 %, precisión 14,4 %); línea base vigente\n"
    "  `anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt`.\n"
)
hoja = cambiar(
    hoja,
    "  clase hasta T y 279 sin clase; la caja, dispersa.\n\n## R4 ·",
    "  clase hasta T y 279 sin clase; la caja, dispersa.\n" + R310 + "\n## R4 ·",
)

# --- R4.3: HECHA, sin NA:F (la F sigue viva en R4.2 y R4.6), con el pivote leído y ADR-0098
hoja = cambiar(
    hoja,
    "- **Refs:** NA:F · ID:A-13 · ID:A-35 · ID:A-43 · ID:A-44 · ID:A-46 · ID:A-48 · ID:A-53 · ID:A-20 · ID:ADR-0083 · ID:ADR-0064 · ID:RN-009 · ID:A-58\n",
    "- **Refs:** ID:A-13 · ID:A-35 · ID:A-43 · ID:A-44 · ID:A-46 · ID:A-48 · ID:A-53 · ID:A-20 · ID:ADR-0083 · ID:ADR-0064 · ID:RN-009 · ID:A-58 · ID:ADR-0098\n",
)
hoja = cambiar(
    hoja,
    "- **Estado:** ABIERTA (la 7a, ingerida y activada, ACTIVAR-SESION-07.md; la 7b, ingerida en trabajo/sesion-08 y activada en trabajo/activar-sesion-08, ACTIVAR-SESION-08.md: la stop del lado malo espera, ADR-0097, y S-22 no cambia el motor; falta leer el pivote en (3)).\n",
    "- **Estado:** HECHA (la 7a, ACTIVAR-SESION-07.md; la 7b, ACTIVAR-SESION-08.md; el pivote, leído en la corrida (3), RECORRIDA-CONSTRUCCION-3.md §3: la cuenta por mes de julio deja de llenar por RN-032 desde el 2026-07-10, así que se lee la diaria por la contingencia, con 19 parejas de julio y 40 de más: «una sesión más»; la meta de ADR-0098, en la misma corrida: salida C, que manda sobre el pivote).\n",
)

# --- R4.6: ADR-0098 en Refs y en «Hecho cuando»
hoja = cambiar(
    hoja,
    "- **Refs:** NA:F · ID:ADR-0093\n- **Qué es:** acuerdo de Aleks y el consultor (2026-11-19)",
    "- **Refs:** NA:F · ID:ADR-0093 · ID:ADR-0098\n- **Qué es:** acuerdo de Aleks y el consultor (2026-11-19)",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** julio cumple los dos mínimos del pivote (ADR-0093 §6), o la lectura del pivote cambia el objetivo.\n",
    "- **Hecho cuando:** julio cumple los dos mínimos del pivote (ADR-0093 §6), o la lectura del pivote cambia el objetivo, o la lectura de ADR-0098 cambia el objetivo.\n",
)

# --- R5.7: sustituida por ADR-0098, HECHA, sin NA:F
R57_VIEJA = hoja.split("### R5.7 ", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
R57_NUEVA = (
    "· El techo del trader y el R de las parejas (ADR-0098)\n"
    "- **Refs:** ID:ADR-0092 · ID:ADR-0098\n"
    "- **Qué es:** lo de RUMBO §5, sustituido por la medida de ADR-0098, que la pre-registra con\n"
    "  cuatro salidas antes de correr: el techo del trader (sus operaciones repetidas con el bróker,\n"
    "  la cuenta y la gestión del bot) y el R de las parejas de la corrida (3), sin abrir la columna de\n"
    "  resultado del libro. Decide el método y el objetivo, nunca un parámetro (recuadro de ADR-0092 §6).\n"
    "- **Depende de:** R3.10 (HECHA).\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** la salida de ADR-0098 está en un informe.\n"
    "- **Estado:** HECHA (`trabajo/recorrida-construccion-3`; RECORRIDA-CONSTRUCCION-3.md §4): el\n"
    "  control reproduce 235 de 235 posiciones; el techo no gana (esperanza -0,239 R en 191, percentil\n"
    "  95 -0,026); las parejas, ni una cosa ni otra (29); **salida C**."
)
hoja = cambiar(hoja, "### R5.7 " + R57_VIEJA, "### R5.7 " + R57_NUEVA)

# --- R5.2: la corrida que cuenta es R3.10
hoja = cambiar(
    hoja,
    '- **Depende de:** la corrida que cuenta (R3.9; ADR-0070 §3) con un "sí", y el ADR propio de la\n',
    '- **Depende de:** la corrida que cuenta (R3.10; ADR-0070 §3) con un "sí", y el ADR propio de la\n',
)

# --- El Marcador: la fila de esta rama, con sus columnas de hoy
FILA = "| 2026-11-22 | RECORRIDA-CONSTRUCCION-3.md | 15.2 / 14.4 | 22.7 / 16.3 | -0.429 | 321 |\n"
hoja = cambiar(
    hoja,
    "| 2026-11-08 | RECORRIDA-CONSTRUCCION-2.md | 15.7 / 13.9 | 20.2 / 14.6 | -0.533 | 425 |\n",
    "| 2026-11-08 | RECORRIDA-CONSTRUCCION-2.md | 15.7 / 13.9 | 20.2 / 14.6 | -0.533 | 425 |\n"
    + FILA,
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
vivas = thr.entradas_vivas(ps)


def bloque(texto: str, titulo: str) -> str:
    return texto.split(f"### {titulo} ", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]


print(f"letras vivas en la copia: {' '.join(sorted(vivas))}; F viva? {'F' in vivas}")
for t in ("R3.10", "R4.3", "R5.7"):
    b = bloque(hoja, t)
    print(f"{t}: HECHA? {'- **Estado:** HECHA' in b}; NA:F en el bloque? {'NA:F' in b}")
print(f"R4.6 cita ADR-0098? {'ADR-0098' in bloque(hoja, 'R4.6')}")
print(f"R5.2 cita R3.10? {'(R3.10; ADR-0070 §3)' in bloque(hoja, 'R5.2')}")
print(f"«R5.7 después de (3)» en la F? {'R5.7 después de (3)' in F_NUEVA}")
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))


def _seccion(texto: str, titulo: str, nuevo: str) -> str:
    """Sustituye el cuerpo (una linea) de una seccion `## titulo` de PROJECT_STATE."""
    viejo = texto.split(f"## {titulo}\n", 1)[1].split("\n\n", 1)[0]
    return cambiar(texto, f"## {titulo}\n{viejo}\n", f"## {titulo}\n{nuevo}\n")


# las cabeceras que escribe el ritual, con la forma de las de main y un sha de 8 de relleno
SHA = "xxxxxxxx"
ps_cierre = _seccion(ps, "Current Branch", "main")
ps_cierre = _seccion(
    ps_cierre,
    "Current Feature",
    "Ninguna abierta: trabajo/recorrida-construccion-3 cerrada en main "
    "(stable/F39l-recorrida-construccion-3). Lo siguiente, en la Next Action (F).",
)
ps_cierre = _seccion(
    ps_cierre,
    "Stable Main State",
    f"{SHA} · merge de `trabajo/recorrida-construccion-3` (tag "
    "`stable/F39l-recorrida-construccion-3`), sobre `stable/F39k-activar-sesion-08` (f04868cc). "
    "Informe docs/validation/RECORRIDA-CONSTRUCCION-3.md; el registro del cierre, al final de HISTORIA.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Last Stable Commit",
    f"{SHA} · merge trabajo/recorrida-construccion-3: la corrida (3) de ADR-0070 §3 («no»), el "
    "pivote por la contingencia («una sesión más») y la meta de ADR-0098 (salida C) · tag "
    "stable/F39l-recorrida-construccion-3",
)
DEUDA_D7 = next(x for x in ps_cierre.splitlines() if x.startswith("- Tests que no miran el estado"))
sin_d7 = cambiar(ps_cierre, DEUDA_D7 + "\n", "")
for nombre, texto in (("con la linea de D7", ps_cierre), ("sin la linea de D7", sin_d7)):
    with tempfile.TemporaryDirectory() as tmp:
        copia = Path(tmp)
        (copia / "PROJECT_STATE.md").write_text(texto, encoding="utf-8", newline="\n")
        tps.test_project_state_has_required_sections_in_order(copia)
        tps.test_project_state_declares_a_branch(copia)
        try:
            tps.test_project_state_cabe_en_el_tope(copia)
            tope = "cabe"
        except AssertionError:
            tope = "NO CABE"
    print(
        f"PROJECT_STATE del cierre, {nombre}: {len(texto.encode('utf-8'))} bytes ({tope} en "
        f"{tps.TOPE_BYTES}); la rama hoy: {len(ps.encode('utf-8'))} bytes con la F nueva"
    )
print(
    f"bytes de la F: antes {len(F_VIEJA.encode('utf-8'))}, despues {len(F_NUEVA.encode('utf-8'))}"
)
print(f"bytes de la linea de D7: {len(DEUDA_D7.encode('utf-8')) + 1}")
