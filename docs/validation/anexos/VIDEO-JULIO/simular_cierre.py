"""Simula EN MEMORIA las propuestas de la orden de cierre de trabajo/video-julio (VIDEO-JULIO.md
§10) contra las comprobaciones a, b y c de `tests/unit/test_hoja_de_ruta.py`, sin escribir nada.

Segunda version (2026-11-09, respuesta del consultor a la PARADA final, punto 7): T y U HECHAS
las dos. La primera (commit 8a08da4) solo sacaba T. Cambios simulados:
- PROJECT_STATE: las entradas T y U salen de la Next Action; en F sale el punto (1) y el resto se
  renumera, y la preparacion de la sesion 7 hereda lo de T.
- HOJA-DE-RUTA: R2.4 HECHA (Refs NA:T · NA:U, las dos registradas en HISTORIA).
- HISTORIA: dos registros nuevos, que dicen de que T y de que U son (HISTORIA ya tiene «HECHA · T»
  y «HECHA · U» de octubre, de letras reutilizadas).
- Variante con la entrada del VAD (§10, punto 7): una letra nueva, V (la asigna el consultor), en
  PROJECT_STATE y una entrada R2.5 en la hoja de ruta con NA:V.

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


def sustituir(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, f"no esta una sola vez: {viejo[:60]}"
    return texto.replace(viejo, nuevo)


# ------------------------------------------------------------------------------ PROJECT_STATE
lineas = ps.split("\n")
quitar = ("T. Transcribir v11 a v14", "U. Julio 20-31")
assert all(sum(ln.startswith(q) for ln in lineas) == 1 for q in quitar)
ps2 = "\n".join(ln for ln in lineas if not ln.startswith(quitar))
F_VIEJO = (
    "(1) T, la voz del trader sobre julio; (2) trazas del motor y ablación por regla (RUMBO §2); "
    "(3) láminas del bot a la estética de FX Replay (RUMBO §3); (4) la preparación de la sesión 7 "
    "con el método nuevo y su ADR (RUMBO §1), con los días de §8."
)
F_NUEVO = (
    "(1) trazas del motor y ablación por regla (RUMBO §2), que confirman o reclasifican las 5 filas "
    "de «error nuestro» del vídeo de julio (VIDEO-JULIO.md §4); (2) láminas del bot a la estética "
    "de FX Replay (RUMBO §3); (3) la preparación de la sesión 7 con el método nuevo y su ADR "
    "(RUMBO §1), con los días de §8, la clasificación de las 81 filas del vídeo de julio "
    "(VIDEO-JULIO.md §4), sus dos preguntas técnicas (la tarde del 10 de julio; las entradas válidas "
    "que el trader deja sin tomar en el backtest) y los ítems de evidencia de F7 #1, #2, #3 y #10."
)
ps2 = sustituir(ps2, F_VIEJO, F_NUEVO)

# ------------------------------------------------------------------------------ HOJA-DE-RUTA
R24_HECHA = """### R2.4 · Julio en vídeo
- **Refs:** NA:T · NA:U · ID:ADR-0078
- **Qué es:** transcribir v11 a v14 (el backtest de julio en vídeo), comprobar qué días cubre cada
  uno y compararlos con el xlsx en los días 1 a 17 y con las horas del libro (NA:T); y, tras eso,
  decidir si se extraen casos del vídeo para los días 20 a 31, que solo están en v14 (NA:U;
  ADR-0078 §3).
- **Depende de:** R2.1 (HECHA).
- **Quién:** la transcripción y la comparación, la sesión con encargo del consultor; la decisión
  de los días 20 a 31, el consultor.
- **Hecho cuando:** v11 a v14 están transcritos y comparados con el xlsx, y los días 20 a 31 tienen
  decisión escrita.
- **Estado:** HECHA (`trabajo/video-julio`, `stable/F38u-video-julio`; VIDEO-JULIO.md): v11 a v14
  transcritos y comparados con el libro (67 operaciones, ninguna lo contradice; julio sigue
  provisional en `material_sin_video`); de los días 20 a 31 no se sacan casos del vídeo (decisión
  del consultor del 2026-11-09). Los huecos del ASR, en R2.5.

"""
m = re.search(r"(?ms)^### R2\.4 · Julio en vídeo\n.*?(?=^#{2,3} )", hoja)
assert m is not None, "no encuentro R2.4"
hoja2 = hoja[: m.start()] + R24_HECHA + hoja[m.end() :]

historia2 = historia + (
    "\n# Next Action HECHA · T · el vídeo de julio, v11 a v14 (no la T de trabajo/respuestas-ftmo)"
    " · sale de PROJECT_STATE.md en trabajo/video-julio (<fecha del cierre>)\n"
    "\n# Next Action HECHA · U · julio del 20 al 31, sin casos del vídeo (no la U de "
    "trabajo/respaldo-a11) · sale de PROJECT_STATE.md en trabajo/video-julio (<fecha del cierre>)\n"
)

# ------------------------------------------------------------------- variante con la entrada del VAD
V_PS = (
    "V. Los huecos del ASR en el vídeo de julio (prioridad baja, en los huecos): exponer en corpus "
    "transcribe la configuración del VAD (o su desactivación), con tests; retranscribir v12, v13 y "
    "v14 con --reemplaza-a; volver a medir en los huecos lo de F2, F3, F4 y F6 de VIDEO-JULIO.md y, "
    "con eso, volver a decidir F5 (material_sin_video de julio). No va antes de las trazas, de las "
    "láminas ni de la preparación de la sesión 7."
)
R25 = """### R2.5 · Los huecos del ASR en el vídeo de julio
- **Refs:** NA:V · ID:ADR-0078
- **Qué es:** el VAD de `corpus transcribe` se salta frases cortas del trader (VIDEO-JULIO.md §1.7
  y el minuto de escucha de Aleks). Exponer su configuración, retranscribir v12 a v14 y volver a
  medir en los huecos F2, F3, F4 y F6; con eso se vuelve a decidir F5 (`material_sin_video` de
  julio).
- **Depende de:** R2.4 (HECHA).
- **Quién:** la sesión, con encargo del consultor.
- **Hecho cuando:** los huecos están retranscritos y medidos, y F5 tiene decisión con ellos.
- Prioridad baja, en los huecos: no va antes de R4.4 ni de la preparación de la sesión 7.

"""
psv = sustituir(ps2, "\nG. PREREGISTRO.md", "\n" + V_PS + "\n\nG. PREREGISTRO.md")
hojav = sustituir(hoja2, "## R3 · Una corrida del arnés", R25 + "## R3 · Una corrida del arnés")

for nombre, p, h in (("sin la entrada del VAD", ps2, hoja2), ("con la entrada del VAD (V)", psv, hojav)):
    print(f"## {nombre}")
    print("T y U fuera:", not ({"T", "U"} & set(t.entradas_vivas(p))))
    print("a:", t.problemas_a(p, h))
    print("b:", t.problemas_b(p, h, historia2, t._ids_existentes(), t._funcionalidades()))
    print("c:", t.problemas_c(p))
    print("letras vivas tras el cierre:", "".join(sorted(t.entradas_vivas(p))))
    print("R2.4 HECHA:", bool(t.HECHA.search(R24_HECHA)))
    print("bytes de PROJECT_STATE:", len(p.encode("utf-8")))
