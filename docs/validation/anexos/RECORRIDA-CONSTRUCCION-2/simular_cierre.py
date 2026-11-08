"""Simula las lineas preparadas para el commit del contrato del cierre de
`trabajo/recorrida-construccion-2` (RECORRIDA-CONSTRUCCION-2.md §6; encargo, «Las lineas del
cierre»): F se reescribe con el texto del encargo, con el veredicto literal resumido en una linea
(F sigue viva: no sale a HISTORIA; ninguna letra sale ni entra); en la hoja de ruta, R3.9 nueva tras
R3.8, HECHA y sin `NA:F` (F sigue viva, tests/unit/test_hoja_de_ruta.py), y R5.2 cita R3.9 en lugar de
R4.1 como la corrida que cuenta; R5.6 no cambia (la corrida dio «no»). Como
`anexos/CUENTA-POR-MES/simular_cierre.py`: contra tests/unit/test_hoja_de_ruta.py (a, b y c) y
tests/unit/test_project_state.py, cargados por su ruta LITERAL.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la raiz del repo) y
aplica en memoria sustituciones exactas (cada una casa UNA vez). Las comprobaciones de PROJECT_STATE
corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar. En el repo no
escribe nada. Ademas simula las cuatro lineas de cabecera que escribe el ritual, para medir los bytes.

    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/simular_cierre.py
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


# --- PROJECT_STATE: F, con el texto del encargo y el veredicto literal resumido en una linea
F_VIEJA = next(x for x in ps.splitlines() if x.startswith("F. "))
F_NUEVA = (
    "F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7 (§d de "
    "ACTIVAR-SESION-06-MOTOR.md). La re-corrida que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md; "
    "veredicto «no» (cobertura 15.7 % por debajo de 70.0 %; precision 13.9 % por debajo de 60.0 %); "
    "línea base vigente anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Siguiente: la "
    "preparación de la sesión 7 (hoja + gráficos 2 a 6 con contexto; lista en ACTIVAR-SESION-06.md "
    "§«Para la sesión 7», más S-22 y S-19 con sus esquemas y el 52 %, más lo que la clasificación de "
    "la re-corrida añada, RECORRIDA-CONSTRUCCION-2.md §5); J antes si la hoja sale de kit hoja. El "
    "vídeo de mapeo, si llega, SIN ABRIR y fuera del repo. R6a en los huecos."
)
ps = cambiar(ps, F_VIEJA + "\n", F_NUEVA + "\n")

# --- La hoja de ruta: R3.9 nueva tras R3.8
R39 = (
    "\n### R3.9 · La re-corrida que cuenta: comisión medida, sello, sesión 6, método y cuenta por mes\n"
    "- **Refs:** ID:ADR-0070 · ID:ADR-0090 · ID:ADR-0091 · ID:ADR-0092\n"
    "- **Qué es:** la corrida del arnés que cuenta por ADR-0070 §3 sobre toda la construcción, la\n"
    "  primera con la comisión medida (ADR-0090 §3), el sello del respaldo M1 (ADR-0091), el motor\n"
    "  de la sesión 6, la salida del método de ADR-0092 y una cuenta por mes (ADR-0092 §8), con su\n"
    "  diagnóstico de cuenta diaria y los dos `diff` contra la línea base anterior; la materia que\n"
    "  el consultor clasifica (error nuestro o regla desconocida).\n"
    "- **Depende de:** R3.7 y R3.8 (HECHAS).\n"
    "- **Quién:** la sesión, con el encargo del consultor; la clasificación, el consultor.\n"
    "- **Hecho cuando:** el veredicto literal está en el informe y en ADR-0070 §3, la línea base\n"
    "  vigente es la suya y cada diferencia tiene su clase.\n"
    "- **Estado:** HECHA (`trabajo/recorrida-construccion-2`; RECORRIDA-CONSTRUCCION-2.md): «no»\n"
    "  (cobertura 15,7 %, precisión 13,9 %); línea base vigente\n"
    "  `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt`.\n"
)
hoja = cambiar(
    hoja,
    "  toque (NOTA de ADR-0092 §8), con sus tests sintéticos; la diaria, intacta.\n\n## R4 ·",
    "  toque (NOTA de ADR-0092 §8), con sus tests sintéticos; la diaria, intacta.\n"
    + R39
    + "\n## R4 ·",
)
# R5.2: la corrida que cuenta es R3.9
hoja = cambiar(
    hoja,
    '- **Depende de:** la corrida que cuenta (R4.1; ADR-0070 §3) con un "sí", y el ADR propio de la\n',
    '- **Depende de:** la corrida que cuenta (R3.9; ADR-0070 §3) con un "sí", y el ADR propio de la\n',
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
r39 = hoja.split("### R3.9 ", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
vivas = thr.entradas_vivas(ps)
print(
    f"letras vivas en la copia: {' '.join(sorted(vivas))}; F viva? {'F' in vivas}; "
    f"NA:F en R3.9? {'NA:F' in r39}; R3.9 HECHA? {'- **Estado:** HECHA' in r39}"
)
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
r52 = hoja.split("### R5.2 ", 1)[1].split("\n### ", 1)[0]
r56 = hoja.split("### R5.6 ", 1)[1].split("\n### ", 1)[0]
print(f"R5.2 cita R3.9? {'(R3.9; ADR-0070 §3)' in r52}; R4.1 en su «Depende de»? {'R4.1' in r52}")
print(
    "R5.6 «Depende de» sin cambiar? "
    + str(
        "- **Depende de:** R5.1 (G) y la re-corrida que cuenta, con su línea «habilita medir» en sí (ADR-0070 punto 5; ADR-0092 §5).\n"
        in r56 + "\n"
    )
)


def _seccion(texto: str, titulo: str, nuevo: str) -> str:
    """Sustituye el cuerpo (una linea) de una seccion `## titulo` de PROJECT_STATE."""
    viejo = texto.split(f"## {titulo}\n", 1)[1].split("\n\n", 1)[0]
    return cambiar(texto, f"## {titulo}\n{viejo}\n", f"## {titulo}\n{nuevo}\n")


# las CUATRO lineas de cabecera que escribe el ritual, con la forma de las de main y un sha de 7
# caracteres de relleno; el tag, el siguiente libre (F38t)
SHA = "xxxxxxx"
# la forma corta, como las cabeceras de los cierres anteriores (la primera de este guion, con la
# lista entera de lo que entra en la corrida, daba 23.053 bytes: RECORRIDA-CONSTRUCCION-2.md §6)
RESUMEN = "la re-corrida que cuenta (ADR-0070 §3): «no» (cobertura 15,7 %, precisión 13,9 %)"
ps_cierre = _seccion(ps, "Current Branch", "main")
ps_cierre = _seccion(
    ps_cierre,
    "Current Feature",
    "Ninguna rama abierta. trabajo/recorrida-construccion-2 cerrada en main el 2026-11-0X "
    f"(stable/F38t-recorrida-construccion-2): {RESUMEN}.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Stable Main State",
    f"{SHA} · merge de `trabajo/recorrida-construccion-2` (tag `stable/F38t-recorrida-construccion-2`), "
    "sobre `stable/F38s-cuenta-por-mes` (41d47b3). Informe docs/validation/RECORRIDA-CONSTRUCCION-2.md; "
    "el registro del cierre, al final de HISTORIA.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Last Stable Commit",
    f"{SHA} · merge: trabajo/recorrida-construccion-2, {RESUMEN} · tag "
    "stable/F38t-recorrida-construccion-2",
)
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano = (copia / "PROJECT_STATE.md").stat().st_size
    (copia / "PROJECT_STATE.md").write_text(ps_cierre, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano_cierre = (copia / "PROJECT_STATE.md").stat().st_size
    print(
        f"PROJECT_STATE con las lineas del cierre: {tamano} bytes (st_size de la copia, los mismos "
        f"que wc -c); con las cuatro lineas de cabecera del cierre: {tamano_cierre}; los cuatro "
        "tests de test_project_state, sobre las dos: ok"
    )
    if max(tamano, tamano_cierre) >= 23_000:
        print("POR ENCIMA de la alerta de 23.000 del consultor", file=sys.stderr)
        sys.exit(1)
