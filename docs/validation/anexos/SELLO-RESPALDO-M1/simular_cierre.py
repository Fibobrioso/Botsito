"""Simula las lineas preparadas para el commit del contrato del cierre de `trabajo/sello-respaldo-m1`
(SELLO-RESPALDO-M1.md, «Las lineas del cierre»), en el caso que dio D2: (c2), con (e2) aplicado y
la PARADA con el plan. Como `anexos/RESPALDO-M1/simular_cierre.py`, contra
tests/unit/test_hoja_de_ruta.py (a, b y c) y tests/unit/test_project_state.py, pero con los dos
modulos importados por su nombre (la guardia niega cargarlos por una ruta calculada).

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz del repositorio (el directorio de
trabajo) y aplica en memoria los cambios como sustituciones exactas (cada una casa UNA vez). Las
comprobaciones de PROJECT_STATE corren sobre una copia en una carpeta temporal fuera del repo, que
se borra al acabar. En el repo no escribe nada. No simula lo que el ritual de cierre pone en
Current Branch, Current Feature y las secciones de main (RITUAL.md).

    PYTHONPATH=. uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/simular_cierre.py
"""

# ruff: noqa: E501  (las sustituciones son literales de los documentos: tienen que casar tal cual)
from __future__ import annotations

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


# las rutas, LITERALES y relativas a la raiz del repositorio (el directorio de trabajo): la guardia
# solo deja cargar un fichero cuya ruta lee al inspeccionar
thr = _modulo(importlib.util.spec_from_file_location("thr", "tests/unit/test_hoja_de_ruta.py"))
tps = _modulo(importlib.util.spec_from_file_location("tps", "tests/unit/test_project_state.py"))

raiz = Path.cwd()
ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: H se queda, reescrita (no sale HECHA: D2 dio (c2)); F con lo siguiente
linea_h = next(x for x in ps.splitlines() if x.startswith("H. "))
H_NUEVA = (
    "H. El respaldo M1 sella el evento de una vela en su cierre, un milisegundo después de que el "
    "motor decida (ADR-0051 §5, ADR-0057 §1), así que la vela k no se evalúa para la orden que el "
    "motor cancela en su cierre. Medido con el código de main, día a día con el visor: en 11 días de "
    "construcción, 2 de esas cancelaciones en una M1 sin ticks las habría llenado su vela, y con la "
    "forma (c2) (sellar en k fin - 1, con los lectores del minuto de apertura en «+ 1») son 2 "
    "operaciones nuevas del bot (SELLO-RESPALDO-M1.md §0.c). Rama propia con un ADR que enmiende esos "
    "dos ADR (borrador en SELLO-RESPALDO-M1.md §PARADA): 10 tests de main reescritos, los lectores de "
    "§0.e y las NOTAS que pida la decisión del consultor. La marca adelantada de _peor_del_minuto ya "
    "está corregida, (e2) en trabajo/sello-respaldo-m1. Va antes de la re-corrida que cuenta "
    "(ADR-0070 §3)."
)
ps = cambiar(ps, linea_h, H_NUEVA)
ps = cambiar(
    ps,
    "Siguiente: H (fase 0: el diagnóstico de H del scratchpad de Claude Code, fuera del repo, medido con la comisión de 5: se vuelve a medir sobre el main de F38p), R y la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3);",
    "Siguiente: H, la rama de (c2) con su ADR (SELLO-RESPALDO-M1.md, la PARADA), R y la re-corrida que cuenta (ADR-0070 §3), con las dos corridas que pedía R3.6 y la primera con la comisión medida (ADR-0090 §3);",
)

# --- La hoja de ruta: R3.6 con (e2) hecha y su «Hecho cuando» sin las dos corridas
hoja = cambiar(
    hoja,
    "  redondo (RESPALDO-M1.md §0.a y §0.l). Rama propia con un ADR que enmiende ADR-0051 §5 y\n"
    "  ADR-0057 §1.\n",
    "  redondo (RESPALDO-M1.md §0.a y §0.l). Rama propia con un ADR que enmiende ADR-0051 §5 y\n"
    "  ADR-0057 §1. La marca de `_peor_del_minuto` ya está corregida ((e2), `trabajo/sello-respaldo-m1`);\n"
    "  queda el sello, la forma (c2), que cambia operaciones del bot (SELLO-RESPALDO-M1.md §0.c).\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** el ADR está aceptado, un test que rompe en `main` pasa en la rama y las dos\n"
    "  corridas están repetidas.\n",
    "- **Hecho cuando:** el ADR está aceptado y un test que rompe en `main` pasa en la rama. Las dos\n"
    "  corridas pasan a la re-corrida que cuenta, después de R3.7 (regla del consultor del\n"
    "  2026-11-07: los umbrales de R se fijan antes de ver ninguna corrida nueva).\n",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
print(f"H viva en la copia simulada? {'H' in thr.entradas_vivas(ps)}")
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano = (copia / "PROJECT_STATE.md").stat().st_size
    print(
        f"PROJECT_STATE con las lineas del cierre: {tamano} bytes; los cuatro tests de test_project_state: ok"
    )
    if tamano >= 23_000:
        print("POR ENCIMA de la alerta de 23.000 del consultor", file=sys.stderr)
        sys.exit(1)
