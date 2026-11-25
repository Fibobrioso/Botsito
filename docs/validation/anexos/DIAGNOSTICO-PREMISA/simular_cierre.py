"""Simula las lineas preparadas para el cierre de `trabajo/diagnostico-premisa`
(DIAGNOSTICO-PREMISA.md §6; encargo, «Las lineas del cierre»), sin aplicarlas: la F con la frase
del encargo (ninguna letra sale ni entra) y, aparte, la de la decision 0 (con el contraste con el
trader); la linea de Technical Debt del b2 de `puente.py` (decision 1), con y sin ella; en la hoja de
ruta, R4.7 con ADR-0100 en sus Refs y en su «Que es», y R4.9 (HECHA, solo `ID:`) y R4.10 (ABIERTA,
`NA:F`) nuevas tras R4.8. Como `anexos/PUENTE-TECHO/simular_cierre.py`: contra
`tests/unit/test_hoja_de_ruta.py` (a, b y c) y `tests/unit/test_project_state.py`, cargados por su
ruta LITERAL.

Lee PROJECT_STATE.md de `main` de un fichero fuera del repo que se le da como argumento (volcado
antes con `git show main:PROJECT_STATE.md`: el cierre devuelve Current Branch y Current Feature, y
el encargo mide sobre el de main), y HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la
raiz del repo), y aplica en memoria sustituciones exactas (cada una casa UNA vez).
Las comprobaciones de PROJECT_STATE corren sobre copias en una carpeta temporal fuera del repo, que
se borra al acabar. En el repo no escribe nada. Simula tambien las cabeceras que escribe el ritual.

    git show main:PROJECT_STATE.md > <carpeta fuera del repo>/ps-main.md
    uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/simular_cierre.py <carpeta>/ps-main.md
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
if len(sys.argv) != 2:
    raise SystemExit("uso: simular_cierre.py <PROJECT_STATE.md de main, volcado fuera del repo>")
ps_main = Path(sys.argv[1]).read_text(encoding="utf-8")
ps_rama = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


def _seccion(texto: str, titulo: str, nuevo: str) -> str:
    """Sustituye el cuerpo (una linea) de una seccion `## titulo` de PROJECT_STATE."""
    viejo = texto.split(f"## {titulo}\n", 1)[1].split("\n\n", 1)[0]
    return cambiar(texto, f"## {titulo}\n{viejo}\n", f"## {titulo}\n{nuevo}\n")


# --- PROJECT_STATE: el de main, con lo que la rama cambia y el ritual reescribe
TESTS_RAMA = ps_rama.split("## Tests Currently Passing\n", 1)[1].split("\n\n", 1)[0]
F_VIEJA_FRASE = "F17 rediseñado (ADR-0099 §5) y el contraste con el trader, pendientes."
F_ENCARGO = "F17 (ADR-0099 §5) y el backtest del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa, hecho."
F_DECISION_0 = "F17 (ADR-0099 §5), el contraste con el trader (ADR-0099 §6) y el backtest del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa, hecho."
LINEA_B2 = (
    "- El test de humo de `anexos/PUENTE-TECHO/puente.py` no pasa el break even ni el tope por el "
    "bucle de `repetir` (b2 del revisor de F39m, PUENTE-TECHO.md); lo reutiliza "
    "`anexos/DIAGNOSTICO-PREMISA/premisa.py`. Dueño: la rama que vuelva a tocar `puente.py`."
)
ANCLA_B2 = "\n\n## Reglas vivas\n"

SHA = "xxxxxxxx"


def ps_del_cierre(frase: str, con_b2: bool) -> str:
    ps = _seccion(ps_main, "Tests Currently Passing", TESTS_RAMA)
    ps = cambiar(ps, F_VIEJA_FRASE, frase)
    if con_b2:
        ps = cambiar(ps, ANCLA_B2, "\n" + LINEA_B2 + ANCLA_B2)
    ps = _seccion(
        ps,
        "Current Feature",
        "Ninguna abierta: trabajo/diagnostico-premisa cerrada en main "
        "(stable/F39n-diagnostico-premisa). Lo siguiente, en la Next Action (F).",
    )
    ps = _seccion(
        ps,
        "Stable Main State",
        f"{SHA} · merge de `trabajo/diagnostico-premisa` (tag `stable/F39n-diagnostico-premisa`), "
        "sobre `stable/F39m-puente-techo` (7a3087e9). Informe docs/validation/DIAGNOSTICO-PREMISA.md; "
        "el registro del cierre, al final de HISTORIA.",
    )
    return _seccion(
        ps,
        "Last Stable Commit",
        f"{SHA} · merge trabajo/diagnostico-premisa: ADR-0100, la premisa con costes "
        "pre-registrada, y sus dos diagnósticos · tag stable/F39n-diagnostico-premisa",
    )


# --- La hoja de ruta
hoja = cambiar(
    hoja,
    "### R4.7 · La salida C de ADR-0098: los costes y la premisa, antes de seguir\n- **Refs:** NA:F · ID:ADR-0098 · ID:ADR-0099 · ID:A-16 · F:F17\n",
    "### R4.7 · La salida C de ADR-0098: los costes y la premisa, antes de seguir\n- **Refs:** NA:F · ID:ADR-0098 · ID:ADR-0099 · ID:ADR-0100 · ID:A-16 · F:F17\n",
)
hoja = cambiar(
    hoja,
    "y el contraste de la premisa con el trader (ADR-0099 §6). Hasta el ADR no se graba ninguna sesión de fidelidad.",
    "y el contraste de la premisa con el trader (ADR-0099 §6). ADR-0100: la premisa se mide con el backtest del trader con costes y dos diagnósticos, con la lectura escrita antes (R4.9, HECHA; R4.10). Hasta el ADR no se graba ninguna sesión de fidelidad.",
)
R49_R410 = (
    "\n### R4.9 · El diagnóstico de la premisa (ADR-0100 §5-§6)\n"
    "- **Refs:** ID:ADR-0100 · ID:ADR-0099\n"
    "- **Qué es:** sobre los días dev de construcción, el registro del trader frente a la réplica (la variante todo_junto del puente), mes por mes, con el retroceso de sus ganadoras, y el techo con lote fijo (base y todo_junto), con las lecturas pre-registradas en docs/plan/PREMISA-COSTES.yaml. Diagnóstico de construcción: ninguna cifra cambia un valor (ADR-0092 §6, recuadro de ADR-0100).\n"
    "- **Depende de:** nada (el pre-registro de ADR-0100).\n"
    "- **Quién:** la sesión, con el encargo del consultor; lee el consultor.\n"
    "- **Hecho cuando:** las dos medidas, con sus lecturas.\n"
    "- **Estado:** HECHA (trabajo/diagnostico-premisa, DIAGNOSTICO-PREMISA.md): la lectura de §5, «enero_y_julio_peores_tambien_para_el»; todo_junto con lote fijo sobre los cuatro meses, «no_concluyente».\n"
    "\n### R4.10 · El backtest del trader con costes (ADR-0100 §2-§4)\n"
    "- **Refs:** ID:ADR-0100 · NA:F\n"
    "- **Qué es:** dos meses de 2024 que el trader no haya operado nunca en backtest, en su plataforma con spread de 0,2 pips y comisión de 5 USD por lote de ida y vuelta, grabados y con el libro completo; medido por riesgo y con lote fijo, con la lectura de ADR-0100 §4 escrita antes (docs/plan/PREMISA-COSTES.yaml). Material de construcción para la premisa (ADR-0100 §2); entra SIN ABRIR y fuera del repo hasta su rama.\n"
    "- **Depende de:** que el trader lo haga y Aleks lo traiga.\n"
    "- **Quién:** el trader lo hace, Aleks lo trae SIN ABRIR y la sesión lo mide en su propia rama, con el encargo del consultor.\n"
    "- **Hecho cuando:** su lectura de ADR-0100 §4, escrita.\n"
    "- **Estado:** ABIERTA.\n"
)
ANCLA_R48 = "el cierre cierra con V1 y V2.\n"
hoja = cambiar(hoja, ANCLA_R48, ANCLA_R48 + R49_R410)

# --- Las comprobaciones de la hoja de ruta, con la F del encargo y con la de la decision 0
ids = thr._ids_existentes()
funciones = thr._funcionalidades()


def bloque(texto: str, titulo: str) -> str:
    return texto.split(f"### {titulo} ", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]


b49, b410, b47 = bloque(hoja, "R4.9"), bloque(hoja, "R4.10"), bloque(hoja, "R4.7")
print(
    f"R4.9: HECHA? {'- **Estado:** HECHA' in b49}; alguna letra (NA:) en el bloque? {'NA:' in b49}"
)
print(f"R4.10: ABIERTA? {'- **Estado:** ABIERTA' in b410}; NA:F? {'NA:F' in b410}")
print(
    f"R4.7 cita ADR-0100 en Refs y en Qué es? {b47.count('ADR-0100') == 2}; ABIERTA? {'ABIERTA' in b47}"
)
for nombre, frase in (("la del encargo", F_ENCARGO), ("la de la decision 0", F_DECISION_0)):
    for con_b2 in (False, True):
        ps = ps_del_cierre(frase, con_b2)
        vivas = thr.entradas_vivas(ps)
        print()
        print(f"## F {nombre}, {'con' if con_b2 else 'sin'} la linea del b2")
        print(f"letras vivas: {' '.join(sorted(vivas))}; F viva? {'F' in vivas}")
        print("a:", thr.problemas_a(ps, hoja))
        print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
        print("c:", thr.problemas_c(ps))
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp)
            (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
            tps.test_project_state_has_required_sections_in_order(copia)
            tps.test_project_state_declares_a_branch(copia)
            try:
                tps.test_project_state_cabe_en_el_tope(copia)
                tope = "cabe"
            except AssertionError:
                tope = "NO CABE"
        print(
            f"PROJECT_STATE del cierre: {len(ps.encode('utf-8'))} bytes ({tope} en {tps.TOPE_BYTES})"
        )
print()
print(f"PROJECT_STATE de main: {len(ps_main.encode('utf-8'))} bytes")
print(
    f"bytes de la frase de la F: antes {len(F_VIEJA_FRASE.encode('utf-8'))}, la del encargo "
    f"{len(F_ENCARGO.encode('utf-8'))}, la de la decision 0 {len(F_DECISION_0.encode('utf-8'))}; "
    f"la linea del b2, {len(LINEA_B2.encode('utf-8')) + 1}"
)
