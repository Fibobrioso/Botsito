"""Simula las lineas preparadas para el commit del contrato de la orden de cierre de
`trabajo/previa-sesion-5` (PREVIA-SESION-5.md, «Lineas preparadas») contra
tests/unit/test_hoja_de_ruta.py y tests/unit/test_project_state.py, como
`anexos/VISOR-CONSTRUCCION/simular_cierre.py` y `anexos/EA-CONEXION/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
propuestos como sustituciones exactas (cada una tiene que casar UNA vez). Corre las funciones a, b
y c de test_hoja_de_ruta.py sobre el texto simulado, y las de test_project_state.py sobre una copia
del PROJECT_STATE simulado en una carpeta temporal fuera del repo, que se borra al acabar. En el
repo no escribe nada.

    uv run python docs/validation/anexos/PREVIA-SESION-5/simular_cierre.py <raiz del repo>
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

raiz = Path(sys.argv[1])


def _cargar(nombre: str, ruta: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


thr = _cargar("thr", raiz / "tests" / "unit" / "test_hoja_de_ruta.py")
tps = _cargar("tps", raiz / "tests" / "unit" / "test_project_state.py")

ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE, V: la hoja lleva los recuadros de esta rama, y S-12 decide si RN-005 sigue.
ps = cambiar(
    ps,
    "Hoja de preguntas: docs/sesion-5/PREGUNTAS.md (trabajo/barrido-sesion-5).",
    "Hoja de preguntas: docs/sesion-5/PREGUNTAS.md (trabajo/barrido-sesion-5), con los recuadros de "
    "corrección de S-7, S-12, S-13 y S-15 (trabajo/previa-sesion-5): la primera parte de S-12 decide "
    "si RN-005 sigue o se reabre (PREVIA-SESION-5.md §1).",
)

# --- PROJECT_STATE, Technical Debt: el docstring que apunta a una seccion que ya no esta en PS.
DEUDA = (
    "- El docstring de `tests/contract/test_tramos_fuente.py:5` cita «PROJECT_STATE, Decisions and "
    "Rationale, 2026-09-04», que vive desde trabajo/previa-sesion-5 en "
    "`docs/runbooks/DECISIONES-DE-PROCESO.md`: lo corrige la próxima rama que toque `tests/` "
    "(PREVIA-SESION-5.md §5)."
)
ps = cambiar(
    ps,
    "- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, "
    "INCOMPLETA desde el 2026-09-09.\n",
    "- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, "
    "INCOMPLETA desde el 2026-09-09.\n" + DEUDA + "\n",
)

print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, thr._ids_existentes(), thr._funcionalidades()))
print("c:", thr.problemas_c(ps))
with tempfile.TemporaryDirectory() as tmp:
    # con newline="\n": en Windows, sin el, cada linea gana un byte (CRLF) y el tope miente
    (Path(tmp) / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    for prueba in (
        tps.test_project_state_exists,
        tps.test_project_state_has_required_sections_in_order,
        tps.test_project_state_declares_a_branch,
        tps.test_project_state_cabe_en_el_tope,
    ):
        prueba(Path(tmp))
        print(f"{prueba.__name__}: pasa")
print("PROJECT_STATE hoy:", len((raiz / "PROJECT_STATE.md").read_bytes()), "bytes")
print("PROJECT_STATE simulado:", len(ps.encode("utf-8")), "bytes")
