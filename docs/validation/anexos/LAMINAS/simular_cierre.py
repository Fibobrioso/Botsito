"""Las propuestas para la orden de cierre de trabajo/laminas, comprobadas con las funciones de
tests/unit/test_hoja_de_ruta.py sobre COPIAS en memoria de PROJECT_STATE.md y HOJA-DE-RUTA.md (no
escribe nada)."""
import sys
from pathlib import Path

import importlib.util
_spec = importlib.util.spec_from_file_location("hoja_de_ruta", "C:/Users/USER/Desktop/Bot v3/tests/unit/test_hoja_de_ruta.py")
t = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t)

ps = Path("PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = Path("docs/plan/HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = Path("docs/state/HISTORIA.md").read_text(encoding="utf-8")

VIEJO_F = (
    "Siguiente, en este orden: (1) las láminas del bot (R4.5), con la enmienda de RUMBO §0, §4 y §5 "
    "en un commit propio; (2) J, si la hoja sale de kit hoja; (3) la preparación de la sesión 7"
)
NUEVO_F = (
    "Las láminas del bot están hechas (LAMINAS.md; `motor laminas`; R4.5) y RUMBO §0, §4 y §5, "
    "enmendado. Siguiente, en este orden: (1) J, si la hoja sale de kit hoja; (2) la preparación "
    "de la sesión 7"
)
assert ps.count(VIEJO_F) == 1
ps2 = ps.replace(VIEJO_F, NUEVO_F)

VIEJO_R45 = """- **Refs:** NA:F · ID:ADR-0092
- **Qué es:** lo de RUMBO §3"""
NUEVO_R45 = """- **Refs:** ID:ADR-0092
- **Qué es:** lo de RUMBO §3"""
VIEJO_HECHO = """- **Hecho cuando:** las láminas de los días de la sesión 7a están hechas y revisadas por el consultor.
- **Estado:** ABIERTA."""
NUEVO_HECHO = """- **Hecho cuando:** la herramienta y las láminas de las sesiones candidatas de la 7a, revisadas por el consultor; las de los días que elija la preparación se generan allí con la herramienta.
- **Estado:** HECHA (trabajo/laminas, LAMINAS.md)."""
bloque = hoja.split("### R4.5 · Las láminas del bot", 1)[1].split("\n## ", 1)[0]
assert bloque.count(VIEJO_R45) == 1 and bloque.count(VIEJO_HECHO) == 1
nuevo_bloque = bloque.replace(VIEJO_R45, NUEVO_R45).replace(VIEJO_HECHO, NUEVO_HECHO)
hoja2 = hoja.replace(bloque, nuevo_bloque)

ids = t._ids_existentes()
funcs = t._funcionalidades()
for nombre, (p, h) in {"hoy": (ps, hoja), "con las propuestas": (ps2, hoja2)}.items():
    print(f"== {nombre}")
    print("  a:", t.problemas_a(p, h))
    print("  b:", t.problemas_b(p, h, historia, ids, funcs))
    print("  c:", t.problemas_c(p))
    print("  d:", t.problemas_d(h, t._extracciones(), t._estados_de_ambiguedades(Path("knowledge/spec/ambiguedades.yaml").read_text(encoding="utf-8"))))
print("== R4.5 propuesta")
print(nuevo_bloque.split("\n## ")[0][:1200])
print("== bytes de PROJECT_STATE con la F nueva:", len(ps2.encode("utf-8")))
