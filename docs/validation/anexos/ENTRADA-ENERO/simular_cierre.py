"""Simula EN MEMORIA los textos de §8.1 y §8.2 de ENTRADA-ENERO.md contra test_hoja_de_ruta.py.

No escribe nada: lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada, aplica los
cambios propuestos como sustituciones exactas (cada una tiene que casar UNA vez) y corre las
funciones a, b y c del test. Uso: python simular_cierre.py <raiz del repo>
"""

import importlib.util
import sys
from pathlib import Path

raiz = Path(sys.argv[1])
TEST = raiz / "tests" / "unit" / "test_hoja_de_ruta.py"
spec = importlib.util.spec_from_file_location("thr", TEST)
assert spec is not None and spec.loader is not None
thr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(thr)

ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# 8.1 Next Action
linea_x = next(x for x in ps.splitlines() if x.startswith("X. "))
ps = cambiar(ps, linea_x + "\n", "")
linea_f = next(x for x in ps.splitlines() if x.startswith("F. "))
ps = cambiar(
    ps,
    linea_f,
    "F. Orden de trabajo: lo siguiente es T (R2.4: transcribir v11 a v14 y compararlos con el xlsx "
    "de julio). R2.3 (Q, agosto) espera la exportación del trader, y R3.1 depende de R2 entera.",
)
ps = cambiar(
    ps,
    "Entra por su propia rama después de X y de renovar hacia atrás",
    "Entra por su propia rama después de renovar hacia atrás",
)
ps = cambiar(
    ps,
    "- 34. Ticks: la ventana de invierno por la rejilla es X; el deslizamiento y el swap, las "
    "ejecuciones 2 y 3 (A).",
    "- 34. Ticks: el deslizamiento y el swap, las ejecuciones 2 y 3 (A).",
)
historia += "\n# Next Action HECHA · X · simulada\n"

# 8.2 Hoja de ruta
hoja = cambiar(
    hoja,
    "- **Refs:** NA:X · HER:34 · ID:ADR-0069 · ID:ADR-0051\n",
    "- **Refs:** NA:X · ID:ADR-0069 · ID:ADR-0051 · ID:ADR-0079\n",
)
hoja = cambiar(
    hoja,
    "las ejecuciones de la demo (carril de Aleks, NA:A).",
    "las ejecuciones de la demo (carril de Aleks, R7.1).",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** la ventana de ticks sale de la rejilla, con su test.\n",
    "- **Hecho cuando:** la ventana de ticks sale de la rejilla, con su test.\n"
    "- **Estado:** HECHA (`trabajo/entrada-enero`, `stable/F37p-entrada-enero`; "
    "ENTRADA-ENERO.md,\n"
    "  ADR-0079): la ventana de ticks sale de la rejilla, con su test; enero es construcción "
    "del 2 al\n"
    "  30, con sus ticks. Las partes b y c del heredado 34 siguen en R7.1.\n",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R2.2 (NA:X) y R2.1 (HECHA) y R1.1.",
    "- **Depende de:** R2.2 (HECHA) y R2.1 (HECHA) y R1.1.",
)

print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, thr._ids_existentes(), thr._funcionalidades()))
print("c:", thr.problemas_c(ps))
print("PROJECT_STATE simulado:", len(ps.encode("utf-8")), "bytes")
