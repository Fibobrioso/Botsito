"""Simula EN MEMORIA las lineas propuestas para la orden de cierre de trabajo/vad-julio
(VAD-JULIO.md, «Para la orden de cierre») contra las comprobaciones a, b y c de
`tests/unit/test_hoja_de_ruta.py`, sin escribir nada. Respuesta del consultor a la PARADA (b),
punto 7:
- PROJECT_STATE: la letra C sale de la Next Action; en F, «La letra C y R6a, en los huecos.» pasa
  a «R6a, en los huecos.»; una linea nueva de Technical Debt (punto 2).
- HOJA-DE-RUTA: R2.5 HECHA (sin cumplir su «Hecho cuando» original, por el punto 1); R4.7 dice que
  la parte de julio de S-14 no la resuelve el ASR y la decide el ADR de la salida C; R2.4 no cambia.
- HISTORIA: el registro «# Next Action HECHA · C ·» con el texto literal de C.

Uso, desde la raiz del repositorio: uv run python docs/validation/anexos/VAD-JULIO/simular_cierre.py <raiz>
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    sys.exit("uso: simular_cierre.py <raiz del repositorio>")
RAIZ = Path(sys.argv[1]).resolve()
# Ruta LITERAL (la guardia solo deja cargar un modulo por una ruta que lee al inspeccionar).
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
(linea_c,) = [ln for ln in lineas if ln.startswith("C. La voz que el ASR se salta")]
i = lineas.index(linea_c)
# La C y la linea en blanco que la sigue.
assert lineas[i + 1] == ""
ps2 = "\n".join(lineas[:i] + lineas[i + 2 :])
ps2 = sustituir(ps2, " La letra C y R6a, en los huecos.", " R6a, en los huecos.")
DEUDA = (
    "- El texto de julio provisional cita a T, que ya no existe («hasta que T lo compruebe»: "
    "`criterio_fidelidad.yaml`, `cableado.py:1467`, `criterio_fidelidad.py:341`, ADR-0092 §11); "
    "se reescribe cuando el ADR de la salida C de ADR-0098 decida S-14 (VAD-JULIO.md, respuesta "
    "del consultor a la PARADA (b), punto 2)."
)
m = re.search(r"(?m)^## Technical Debt\n.*\n", ps2)
assert m is not None
ps2 = ps2[: m.end()] + DEUDA + "\n" + ps2[m.end() :]

# ------------------------------------------------------------------------------ HOJA-DE-RUTA
R25_HECHA = """### R2.5 · La voz que el ASR se salta (v12 a v14)
- **Refs:** NA:C · ID:ADR-0078 · ID:ADR-0007
- **Qué es:** el VAD de `corpus transcribe` se salta frases cortas del trader (VIDEO-JULIO.md §1.7
  y el minuto de escucha de Aleks). Exponer su configuración, retranscribir v12 a v14 y volver a
  medir en los huecos F2, F3, F4 y F6; con eso se vuelve a decidir F5 (`material_sin_video` de
  julio).
- **Depende de:** R2.4 (HECHA).
- **Quién:** la sesión, con encargo del consultor.
- **Hecho cuando:** los huecos están retranscritos y medidos, y F5 tiene decisión con ellos.
- **Estado:** HECHA sin cumplir su «Hecho cuando» original (`trabajo/vad-julio`, VAD-JULIO.md):
  el VAD es configurable por transcripción y hay `--ensayo` (ADR-0007, enmienda 2026-11-27), pero
  ninguna candidata cumplió el criterio escrito antes de medir (solo se midió en v14). El consultor
  la cierra sin retranscribir y sin tocar el criterio (respuesta a la PARADA (b), punto 1): v12 a
  v14 siguen con sus activas y F5 no cambia (julio sigue provisional); las 24 operaciones sin
  comprobar pasan al ADR de la salida C (S-14, R4.7).

"""
m = re.search(r"(?ms)^### R2\.5 · La voz que el ASR se salta \(v12 a v14\)\n.*?(?=^#{2,3} )", hoja)
assert m is not None, "no encuentro R2.5"
hoja2 = hoja[: m.start()] + R25_HECHA + hoja[m.end() :]
hoja2 = sustituir(
    hoja2,
    "revisar el sesgo del material sin vídeo (S-14) y la otra serie de precios (A-16);",
    "revisar el sesgo del material sin vídeo (S-14; la parte de julio no la resuelve el ASR, "
    "VAD-JULIO.md, y la decide este ADR) y la otra serie de precios (A-16);",
)

historia2 = historia + (
    "\n# Next Action HECHA · C · sale de PROJECT_STATE.md en trabajo/vad-julio (<fecha del cierre>)\n"
    "\nSu texto literal en la Next Action (respuesta del consultor a la PARADA (b) de "
    "trabajo/vad-julio, punto 7; VAD-JULIO.md):\n\n" + linea_c + "\n"
)

print("C fuera:", "C" not in t.entradas_vivas(ps2))
print("a:", t.problemas_a(ps2, hoja2))
print("b:", t.problemas_b(ps2, hoja2, historia2, t._ids_existentes(), t._funcionalidades()))
print("c:", t.problemas_c(ps2))
print("letras vivas tras el cierre:", "".join(sorted(t.entradas_vivas(ps2))))
print("R2.5 HECHA:", bool(t.HECHA.search(R25_HECHA)))
print("bytes de PROJECT_STATE: hoy", len(ps.encode("utf-8")), "-> tras el cierre", len(ps2.encode("utf-8")), "(tope 25000)")
print("control: sin el registro de HISTORIA, b da:", t.problemas_b(ps2, hoja2, historia, t._ids_existentes(), t._funcionalidades()))
