"""Simula EN MEMORIA las propuestas de la orden de cierre de trabajo/video-julio (VIDEO-JULIO.md
§10) contra las comprobaciones a, b y c de `tests/unit/test_hoja_de_ruta.py`, sin escribir nada.

Cambios simulados:
- PROJECT_STATE: la entrada T sale de la Next Action; U pierde «Depende de T.»; en F sale el
  punto (1) y el resto se renumera.
- HOJA-DE-RUTA: R2.4 con el texto propuesto (sin NA:T en ningun sitio del bloque).
- HISTORIA: el registro nuevo «# Next Action HECHA · T · el video de julio · ...».

Uso: uv run python docs/validation/anexos/VIDEO-JULIO/simular_cierre.py <raiz del repositorio>
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("uso: simular_cierre.py <raiz del repositorio>")
RAIZ = Path(sys.argv[1]).resolve()
# Ruta LITERAL (la guardia de Claude Code solo deja cargar un modulo por una ruta que lee al
# inspeccionar): se ejecuta desde la raiz del repositorio, como el simular_cierre.py de
# anexos/RECORRIDA-CONSTRUCCION-2/.
spec = importlib.util.spec_from_file_location("test_hoja_de_ruta", "tests/unit/test_hoja_de_ruta.py")
assert spec is not None and spec.loader is not None
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

ps = (RAIZ / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (RAIZ / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (RAIZ / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")

# PROJECT_STATE
lineas = ps.split("\n")
lineas = [ln for ln in lineas if not ln.startswith("T. Transcribir v11 a v14")]
ps2 = "\n".join(lineas)
ps2 = ps2.replace(" Depende de T.", "")
ps2 = ps2.replace("(1) T, la voz del trader sobre julio; (2)", "(1)")
ps2 = ps2.replace("; (3) láminas", "; (2) láminas").replace("; (4) la preparación", "; (3) la preparación")

# HOJA-DE-RUTA: R2.4 nueva
R24_NUEVA = """### R2.4 · Julio en vídeo
- **Refs:** NA:U · ID:ADR-0078
- **Qué es:** transcribir v11 a v14 (el backtest de julio en vídeo), comprobar qué días cubre cada
  uno y compararlos con el xlsx en los días 1 a 17 y con las horas del libro; y, tras eso,
  decidir si se extraen casos del vídeo para los días 20 a 31, que solo están en v14 (NA:U;
  ADR-0078 §3).
- **Estado:** la transcripción y la comparación están hechas en trabajo/video-julio
  (VIDEO-JULIO.md); falta la decisión de los días 20 a 31 (NA:U).
- **Depende de:** R2.1 (HECHA).
- **Quién:** la decisión de los días 20 a 31, el consultor.
- **Hecho cuando:** los días 20 a 31 tienen decisión escrita.
- Va antes de la preparación de la sesión 7 (RECORRIDA-CONSTRUCCION-2.md §8 y RUMBO-2026-11.md).

"""
m = re.search(r"(?ms)^### R2\.4 · Julio en vídeo\n.*?(?=^#{2,3} )", hoja)
assert m is not None, "no encuentro R2.4"
hoja2 = hoja[: m.start()] + R24_NUEVA + hoja[m.end():]

historia2 = historia + (
    "\n# Next Action HECHA · T · el vídeo de julio · sale de PROJECT_STATE.md en "
    "trabajo/video-julio (2026-11-09)\n"
)

assert "T. Transcribir" not in ps2 and "Depende de T" not in ps2
print("cambios en PROJECT_STATE:", "T fuera" if "T" not in t.entradas_vivas(ps2) else "T SIGUE")
print("a:", t.problemas_a(ps2, hoja2))
print("b:", t.problemas_b(ps2, hoja2, historia2, t._ids_existentes(), t._funcionalidades()))
print("c:", t.problemas_c(ps2))
print("letras vivas tras el cierre:", "".join(sorted(t.entradas_vivas(ps2))))
