"""Simula las lineas preparadas para el commit del contrato del cierre de `trabajo/sello-respaldo-m1`
(SELLO-RESPALDO-M1.md §0.g, reescrito tras la respuesta del consultor del 2026-11-07, punto 10): H
sale HECHA con su registro en HISTORIA, F se reescribe, R3.6 pasa a HECHA con su «Hecho cuando»
corregido y sin `NA:H`, las dos corridas pasan a R3.7 y a la re-corrida que cuenta, y R5.2 deja de
depender de `NA:H`. Como `anexos/RESPALDO-M1/simular_cierre.py`, contra
tests/unit/test_hoja_de_ruta.py (a, b y c) y tests/unit/test_project_state.py, con los dos modulos
cargados por su ruta LITERAL (la guardia niega cargarlos por una ruta calculada).

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz del repositorio (el directorio de
trabajo) y aplica en memoria los cambios como sustituciones exactas (cada una casa UNA vez). Las
comprobaciones de PROJECT_STATE corren sobre una copia en una carpeta temporal fuera del repo, que
se borra al acabar. En el repo no escribe nada. Ademas simula el Current Feature que escribe el
ritual (con la forma del de `main`), para medir los bytes de despues del cierre.

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/simular_cierre.py
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


# las rutas, LITERALES y relativas a la raiz del repositorio (el directorio de trabajo): la guardia
# solo deja cargar un fichero cuya ruta lee al inspeccionar
thr = _modulo(importlib.util.spec_from_file_location("thr", "tests/unit/test_hoja_de_ruta.py"))
tps = _modulo(importlib.util.spec_from_file_location("tps", "tests/unit/test_project_state.py"))

FECHA = "2026-11-07"
raiz = Path.cwd()
ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: H sale HECHA (a HISTORIA, con su registro); F se reescribe
linea_h = next(x for x in ps.splitlines() if x.startswith("H. "))
ps = cambiar(ps, linea_h + "\n\n", "")
historia += (
    f"\n# Next Action HECHA · H · el sello del respaldo M1 · sale de PROJECT_STATE.md en "
    f"trabajo/sello-respaldo-m1 ({FECHA})\n\n"
    "Su texto literal (la letra ya tenía un registro HECHA, el de RN-007, del 2026-10-26; este lleva "
    "su fecha, DECISIONES-DE-PROCESO.md:29):\n\n"
    + linea_h
    + "\n\nHECHA en `trabajo/sello-respaldo-m1` (docs/validation/SELLO-RESPALDO-M1.md): ADR-0091 sella "
    "el evento del respaldo M1 en el último milisegundo de su vela (enmienda ADR-0051 §5, ADR-0057 §1, "
    "ADR-0068 §2 y ADR-0083 D2), con los lectores del minuto de apertura neutros, y (e2) corrige la "
    "marca de `_peor_del_minuto`. En once días de desarrollo, 27 cancelaciones en el cierre de una M1 "
    "sin ticks, 2 que su vela llenaba: 2 operaciones nuevas del bot, verificadas con el visor por "
    "caso. Las dos corridas que pedía R3.6 pasan a la re-corrida que cuenta, después de R3.7.\n"
)
ps = cambiar(
    ps,
    "Siguiente: H (fase 0: el diagnóstico de H del scratchpad de Claude Code, fuera del repo, medido con la comisión de 5: se vuelve a medir sobre el main de F38p), R y la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3);",
    "Siguiente: R y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3) y con el sello del respaldo de ADR-0091;",
)

# --- La hoja de ruta: R3.6 HECHA, sin NA:H; las dos corridas, a R3.7; R5.2 sin NA:H
hoja = cambiar(
    hoja,
    "### R3.6 · El respaldo M1 sella en el cierre, después de que el motor decida\n- **Refs:** NA:H · ID:ADR-0051 · ID:ADR-0057\n",
    "### R3.6 · El respaldo M1 sella en el cierre, después de que el motor decida\n- **Refs:** ID:ADR-0091 · ID:ADR-0051 · ID:ADR-0057\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** el ADR está aceptado, un test que rompe en `main` pasa en la rama y las dos\n"
    "  corridas están repetidas.\n",
    "- **Hecho cuando:** el ADR está aceptado, los tests que rompen en `main` pasan en la rama y los\n"
    "  once días del censo, verificados con el visor por caso, dan lo que dio el prototipo. Las dos\n"
    "  corridas que pedía pasan a R3.7 y a la re-corrida que cuenta (ADR-0070 §3).\n"
    "- **Estado:** HECHA (`trabajo/sello-respaldo-m1`; SELLO-RESPALDO-M1.md): ADR-0091 sella el\n"
    "  evento del respaldo en el último milisegundo de su vela, con los lectores del minuto de\n"
    "  apertura neutros, y (e2) corrige la marca de `_peor_del_minuto`; en once días de desarrollo,\n"
    "  2 operaciones nuevas del bot y las demás idénticas.\n",
)
hoja = cambiar(
    hoja,
    "  de esa rama, antes de ver ninguna corrida nueva.\n",
    "  de esa rama, antes de ver ninguna corrida nueva. Después, la re-corrida que cuenta (ADR-0070\n"
    "  §3) repite las dos corridas que pedía R3.6, ya con el sello de ADR-0091.\n",
)
hoja = cambiar(
    hoja,
    "  rama de medida (ADR-0070 §6); NA:H, el sello del respaldo M1 (R3.6); y NA:R, el\n  método (R3.7).\n",
    "  rama de medida (ADR-0070 §6); y NA:R, el método (R3.7). El sello del respaldo M1 (R3.6)\n  está HECHO (ADR-0091).\n",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
print(
    f"H viva en la copia? {'H' in thr.entradas_vivas(ps)}; H HECHA en HISTORIA? "
    f"{'H' in thr.letras_hechas(historia)}; NA:H en la hoja simulada? {'NA:H' in hoja}"
)
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
# el Current Feature que escribe el ritual, con la forma del de main (unos 263 bytes)
cf_actual = ps.split("## Current Feature\n", 1)[1].split("\n\n", 1)[0]
cf_cierre = (
    "Ninguna rama abierta. trabajo/sello-respaldo-m1 cerrada en main el 2026-11-0X "
    "(stable/F38q-sello-respaldo-m1): (e2) y el sello del respaldo M1 en el último milisegundo de "
    "su vela (ADR-0091); en once días de desarrollo, 2 operaciones nuevas del bot."
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
