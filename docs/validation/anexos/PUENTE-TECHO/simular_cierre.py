"""Simula las lineas preparadas para el cierre de `trabajo/puente-techo` (PUENTE-TECHO.md §5;
encargo, «Las lineas del cierre»), sin aplicarlas: la F con una frase mas (ninguna letra sale ni
entra); en la hoja de ruta, R4.7 con ADR-0099, sus tres medidas, la auditoria profunda y su «Hecho
cuando» en el ADR de ADR-0099 §7; R4.8 nueva tras R4.7, para el puente, HECHA con su lectura y sin
ninguna letra en su bloque; A.5 con F17 rediseñado; R6.0 con la razon retirada; y la linea de Metas
con ADR-0098 §6. Como `anexos/RECORRIDA-CONSTRUCCION-3/simular_cierre.py`: contra
`tests/unit/test_hoja_de_ruta.py` (a, b y c) y `tests/unit/test_project_state.py`, cargados por su
ruta LITERAL.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la raiz del repo) y
aplica en memoria sustituciones exactas (cada una casa UNA vez). Las comprobaciones de
PROJECT_STATE corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar.
En el repo no escribe nada. Simula tambien las cabeceras que escribe el ritual.

    uv run python -B docs/validation/anexos/PUENTE-TECHO/simular_cierre.py
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


# --- PROJECT_STATE: la F, con una frase mas, sin quitar nada de lo que sigue vivo
F_VIEJA = next(x for x in ps.splitlines() if x.startswith("F. "))
ANCLA_F = "y la siguiente (R4.6) se prepara."
FRASE_F = (
    " ADR-0099: se mide primero; el puente del techo, hecho (PUENTE-TECHO.md, lectura «solo_juntas»); "
    "F17 rediseñado (ADR-0099 §5) y el contraste con el trader, pendientes."
)
F_NUEVA = cambiar(F_VIEJA, ANCLA_F, ANCLA_F + FRASE_F)
ps = cambiar(ps, F_VIEJA + "\n", F_NUEVA + "\n")

# --- La hoja de ruta
hoja = cambiar(
    hoja,
    "Metas (Aleks): firme, el bot testeado y funcional para marzo de 2027;",
    "Metas (Aleks): firme, el bot testeado y funcional para marzo de 2027, que no cabe con ninguna vía (ADR-0098 §6);",
)
hoja = cambiar(
    hoja,
    "### R4.7 · La salida C de ADR-0098: los costes y la premisa, antes de seguir\n- **Refs:** NA:F · ID:ADR-0098 · ID:A-16 · F:F17\n",
    "### R4.7 · La salida C de ADR-0098: los costes y la premisa, antes de seguir\n- **Refs:** NA:F · ID:ADR-0098 · ID:ADR-0099 · ID:A-16 · F:F17\n",
)
hoja = cambiar(
    hoja,
    "La auditoría profunda del consultor (solo lectura, sin rama, desde AUDITORIA-2026-11-21.md) se centra en la premisa: de dónde sale la diferencia entre el techo y lo que el trader dice ganar. Hasta el ADR no se graba ninguna sesión de fidelidad.",
    "La auditoría profunda (solo lectura, sin rama; AUDITORIA-PROFUNDA-2026-11.md, que partió de AUDITORIA-2026-11-21.md) se centró en la premisa: de dónde sale la diferencia entre el techo y lo que el trader dice ganar. ADR-0099 decide medir primero tres cosas: el puente del techo pieza a pieza (R4.8, HECHA), F17 rediseñado (ADR-0099 §5; A.5) y el contraste de la premisa con el trader (ADR-0099 §6). Hasta el ADR no se graba ninguna sesión de fidelidad.",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** un ADR de Aleks decide, con lo que salga, si se sigue y cómo (ADR-0098 §3 C).\n- **Estado:** ABIERTA.\n",
    "- **Hecho cuando:** el ADR de Aleks que acota ADR-0099 §7 decide, con lo que salga, si se sigue y cómo (ADR-0098 §3 C).\n- **Estado:** ABIERTA.\n"
    "\n### R4.8 · El puente del techo pieza a pieza (ADR-0099)\n"
    "- **Refs:** ID:ADR-0099 · ID:ADR-0098\n"
    "- **Qué es:** el techo de ADR-0098 §1 con una pieza cambiada cada vez, sobre los días dev de construcción, con la lista cerrada de dieciséis variantes y las lecturas pre-registradas en docs/plan/PUENTE-TECHO.yaml (ADR-0099 §2-§3). Diagnóstico de construcción: ninguna cifra cambia un valor (ADR-0092 §6, recuadro de ADR-0099).\n"
    "- **Depende de:** nada (el pre-registro de ADR-0099).\n"
    "- **Quién:** la sesión, con el encargo del consultor; lee el consultor.\n"
    "- **Hecho cuando:** las dieciséis variantes medidas, con su lectura y el cierre del puente.\n"
    "- **Estado:** HECHA (trabajo/puente-techo, PUENTE-TECHO.md): lectura del puente «solo_juntas» (ninguna suelta deja de dar no_gana; todo_junto, no_concluyente); el cierre cierra con V1 y V2.\n",
)
hoja = cambiar(
    hoja,
    "- **Refs:** NA:A · NA:M · HER:10 · F:F17\n",
    "- **Refs:** NA:A · NA:M · HER:10 · F:F17 · ID:ADR-0099\n",
)
hoja = cambiar(
    hoja,
    "y el grabador de spread y ticks de F17 (heredado 10), que también mide el\n  deslizamiento (ADR-0090 §7).",
    "y F17 rediseñado (heredado 10; ADR-0099 §5): el historial de ticks del servidor\n  de la demo, el grabador de ticks y spread y la medida de las órdenes stop.",
)
hoja = cambiar(
    hoja,
    "se descarta que Python decida en vivo, por el tope de peticiones.",
    "se descarta que Python decida en vivo, por el tope de peticiones (razón retirada por el recuadro del 2026-11-22 de ADR-0082; la decisión sigue).",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
vivas = thr.entradas_vivas(ps)


def bloque(texto: str, titulo: str) -> str:
    return texto.split(f"### {titulo} ", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]


print(f"letras vivas en la copia: {' '.join(sorted(vivas))}; F viva? {'F' in vivas}")
b48 = bloque(hoja, "R4.8")
print(
    f"R4.8: HECHA? {'- **Estado:** HECHA' in b48}; alguna letra (NA:) en el bloque? {'NA:' in b48}"
)
print(
    f"R4.7 cita ADR-0099? {'ADR-0099' in bloque(hoja, 'R4.7')}; ABIERTA? {'ABIERTA' in bloque(hoja, 'R4.7')}"
)
print(
    f"A.5 cita ADR-0099 §5? {'ADR-0099 §5' in bloque(hoja, 'A.5')}; «que también mide» sigue? {'que también mide' in bloque(hoja, 'A.5')}"
)
print(f"R6.0 lleva la razón retirada? {'razón retirada' in bloque(hoja, 'R6.0')}")
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
    "Ninguna abierta: trabajo/puente-techo cerrada en main (stable/F39m-puente-techo). Lo "
    "siguiente, en la Next Action (F).",
)
ps_cierre = _seccion(
    ps_cierre,
    "Stable Main State",
    f"{SHA} · merge de `trabajo/puente-techo` (tag `stable/F39m-puente-techo`), sobre "
    "`stable/F39l-recorrida-construccion-3` (88f678f7). Informe docs/validation/PUENTE-TECHO.md; el "
    "registro del cierre, al final de HISTORIA.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Last Stable Commit",
    f"{SHA} · merge trabajo/puente-techo: las dos auditorías de noviembre, ADR-0099 y el puente del "
    "techo pieza a pieza (solo_juntas) · tag stable/F39m-puente-techo",
)
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps_cierre, encoding="utf-8", newline="\n")
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    try:
        tps.test_project_state_cabe_en_el_tope(copia)
        tope = "cabe"
    except AssertionError:
        tope = "NO CABE"
print(
    f"PROJECT_STATE del cierre: {len(ps_cierre.encode('utf-8'))} bytes ({tope} en "
    f"{tps.TOPE_BYTES}); la rama hoy, con la F nueva: {len(ps.encode('utf-8'))} bytes"
)
print(
    f"bytes de la F: antes {len(F_VIEJA.encode('utf-8'))}, despues {len(F_NUEVA.encode('utf-8'))}"
)
