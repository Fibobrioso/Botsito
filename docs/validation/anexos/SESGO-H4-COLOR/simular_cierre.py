"""Simula EN MEMORIA las lineas preparadas para el commit del contrato de la orden de cierre de
`trabajo/sesgo-h4-color` (SESGO-H4-COLOR.md §5) contra tests/unit/test_hoja_de_ruta.py, como hizo
`anexos/ENTRADA-ENERO/simular_cierre.py`.

No escribe nada: lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada, aplica los
cambios propuestos como sustituciones exactas (cada una tiene que casar UNA vez) y corre las
funciones a, b y c del test; imprime tambien el tamano que resulta de PROJECT_STATE.md.
Uso: uv run python docs/validation/anexos/SESGO-H4-COLOR/simular_cierre.py <raiz del repo>
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


# §5.1 Next Action: W sale entera (a HISTORIA, con su texto literal); F y V se reescriben
linea_w = next(x for x in ps.splitlines() if x.startswith("W. "))
ps = cambiar(ps, linea_w + "\n", "")
linea_f = next(x for x in ps.splitlines() if x.startswith("F. "))
F_NUEVA = (
    "F. E → O → V. La re-corrida de R3.1 con el sesgo nuevo ya está hecha (SESGO-H4-COLOR.md §4); "
    "si E cambia lo que simula, su encargo decide si hace falta otra."
)
ps = cambiar(ps, linea_f, F_NUEVA)
ps = cambiar(
    ps,
    "de CORRIDA-CONSTRUCCION.md §4.5 sin la pregunta 1 (el sesgo, respondida: pasa a W), en su "
    "orden. Depende de R1.1, de R3.1, de W, E y O, de J (kit hoja) y de la copia de seguridad "
    "(A.4).",
    "de CORRIDA-CONSTRUCCION.md §4.5 con su pregunta 1 sustituida por las dos de "
    "SESGO-H4-COLOR.md §4.4 (la ruptura simple sin cuerpo, D3 de ADR-0080, y la contradicción con "
    "la sesión 1, con un esquema dibujado), en su orden. Depende de R1.1, de R3.1, de E y O, de J "
    "(kit hoja) y de la copia de seguridad (A.4).",
)
historia += (
    "\n# Next Action HECHA · W · el sesgo de H4 por el color · sale de PROJECT_STATE.md en "
    "trabajo/sesgo-h4-color (2026-10-17)\n\n" + linea_w + "\n\nLa hace `trabajo/sesgo-h4-color` "
    "(docs/validation/SESGO-H4-COLOR.md, ADR-0080).\n"
)

# §5.2 Hoja de ruta: R1.2 HECHA con ADR-0080; R4.1 deja de esperar a NA:W y a R1.2
hoja = cambiar(
    hoja,
    "- **Refs:** NA:W · ID:ADR-0060 · ID:RN-003\n",
    "- **Refs:** NA:W · ID:ADR-0060 · ID:RN-003 · ID:ADR-0080\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** la regla está en la spec y en el motor, con su feedback y su ADR, y el "
    "arnés\n  se ha vuelto a correr con los tres comandos de R3.1.\n",
    "- **Hecho cuando:** la regla está en la spec y en el motor, con su feedback y su ADR, y el "
    "arnés\n  se ha vuelto a correr con los tres comandos de R3.1.\n"
    "- **Estado:** HECHA (`trabajo/sesgo-h4-color`, `stable/F37r-sesgo-h4-color`; "
    "SESGO-H4-COLOR.md,\n"
    "  ADR-0080): la regla del color en la spec y en el motor, dos registros de feedback, el arnés\n"
    "  vuelto a correr con los tres comandos de R3.1 (§4). La contradicción con la sesión 1 y la\n"
    "  ruptura simple sin cuerpo van a la sesión 5 (R4.1).\n",
)
hoja = cambiar(
    hoja,
    "ID:A-53 · ID:RN-007 · NA:H · NA:J · NA:V · NA:W · NA:E · NA:O · HER:25 · HER:30 · HER:35 ·",
    "ID:A-53 · ID:RN-007 · NA:H · NA:J · NA:V · NA:E · NA:O · HER:25 · HER:30 · HER:35 ·",
)
hoja = cambiar(
    hoja,
    "«Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5, sin su pregunta 1 "
    "(el\n  sesgo, respondida: R1.2).",
    "«Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5, con su pregunta 1\n"
    "  sustituida por las dos de SESGO-H4-COLOR.md §4.4 (la ruptura simple sin cuerpo y la\n"
    "  contradicción con la sesión 1; R1.2).",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (NA:W), R3.2 (NA:O), R3.3 (NA:E) y la copia de",
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (HECHA), R3.2 (NA:O), R3.3 (NA:E) y la copia de",
)

print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, thr._ids_existentes(), thr._funcionalidades()))
print("c:", thr.problemas_c(ps))
print("PROJECT_STATE hoy:", len((raiz / "PROJECT_STATE.md").read_bytes()), "bytes")
print("PROJECT_STATE simulado:", len(ps.encode("utf-8")), "bytes")
