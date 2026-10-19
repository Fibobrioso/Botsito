"""Simula las lineas preparadas para el commit del contrato de la orden de cierre de
`trabajo/punto-usado` (PUNTO-USADO.md §6) contra tests/unit/test_hoja_de_ruta.py y
tests/unit/test_project_state.py, como `anexos/VISOR-CONSTRUCCION/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
propuestos como sustituciones exactas (cada una tiene que casar UNA vez). Corre las funciones a, b
y c de test_hoja_de_ruta.py sobre el texto simulado, y las cuatro de test_project_state.py sobre
una copia del PROJECT_STATE simulado en una carpeta temporal fuera del repo, que se borra al
acabar. En el repo no escribe nada.

    uv run python docs/validation/anexos/PUNTO-USADO/simular_cierre.py <raiz del repo>
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


# §6 Next Action: Y sale entera (a HISTORIA, con su texto literal); F y V cambian
linea_y = next(x for x in ps.splitlines() if x.startswith("Y. "))
ps = cambiar(ps, linea_y + "\n\n", "")
historia += (
    "\n# Next Action HECHA · Y · qué gasta un punto · sale de PROJECT_STATE.md en "
    "trabajo/punto-usado (2026-10-18)\n\n" + linea_y + "\n\nLa hace `trabajo/punto-usado` "
    "(docs/validation/PUNTO-USADO.md; ADR-0083, que la rehizo en el sentido contrario al de esta "
    "línea: el llenado no gasta el punto).\n"
)
linea_f = next(x for x in ps.splitlines() if x.startswith("F. "))
F_NUEVA = (
    "F. J → V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno ni a J "
    "ni a V."
)
ps = cambiar(ps, linea_f, F_NUEVA)
ps = cambiar(
    ps,
    "y las preguntas de VISOR-CONSTRUCCION.md §3.2. Depende de R1.1, de R3.1, de Y, de J (kit "
    "hoja) y de la copia de seguridad (A.4).",
    "las preguntas de VISOR-CONSTRUCCION.md §3.2; y la pregunta 3 con el ejemplo del 29 de abril y "
    "la caja de la reentrada (PUNTO-USADO.md). Depende de R1.1, de R3.1, de J (kit hoja) y de la "
    "copia de seguridad (A.4).",
)

# §6 Technical Debt: las dos lineas del auditor
DEUDAS = [
    "- RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden "
    "stop lleva `por = primer_esquema` (zonas.py); nada produce ese `por`, y la acción `reentrar` "
    "no está escrita (PUNTO-USADO.md §1.h).",
    "- La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta, y A-31 está "
    "RESUELTA desde el 2026-09-29 (PUNTO-USADO.md §1.h).",
    "- Una zona del productor reutilizada en un escenario nuevo (misma caja del mismo punto tras "
    "una toma nueva) sigue ligada al escenario en que nació y sus cierres cuentan en los cartuchos "
    "de aquel (zonas.py, `zona_del_punto` liga solo al crearla); ADR-0083 lo hace alcanzable y la "
    "fase 4 no lo midió: hace falta la traza por cierre (PUNTO-USADO.md §1.c y §4.f).",
]
ps = cambiar(
    ps,
    "Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.\n",
    "Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.\n"
    + "\n".join(DEUDAS)
    + "\n",
)

# §6 Hoja de ruta: R3.4 cambia de titulo y de «Qué es», gana ID:ADR-0083 y pasa a HECHA; R4.1 sin
# NA:Y y con R3.4 (HECHA); el Estado de R3.2 deja de dar la E por buena
R34_VIEJA = (
    "### R3.4 · Un punto ya llenado no se vuelve a colocar\n"
    "- **Refs:** NA:Y · ID:ADR-0064 · ID:ADR-0074\n"
    "- **Qué es:** que el bot no vuelva a colocar, con otra caja, el punto cuya orden ya se llenó\n"
    "  (ADR-0064, decisión 1; VISOR-CONSTRUCCION.md §2.d.4), y la corrida 2 repetida.\n"
    "- **Depende de:** R3.2 (HECHA).\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está "
    "repetida\n"
    "  con los tres comandos de R3.1.\n"
)
R34_NUEVA = (
    "### R3.4 · Qué gasta un punto: el rechazo y el no envío, no el llenado\n"
    "- **Refs:** NA:Y · ID:ADR-0083 · ID:ADR-0064 · ID:ADR-0074\n"
    "- **Qué es:** fijar por ADR qué gasta un punto (ADR-0083, que enmienda la decisión 1 de\n"
    "  ADR-0064): el rechazo del bróker -al colocar o al llenar- y el no envío lo gastan; el\n"
    "  llenado no, y tras una pérdida o un break even el mismo punto se vuelve a colocar, con la\n"
    "  misma caja o con otra; el código lo cumple, con tests que rompen en `main`, y la corrida 2\n"
    "  repetida.\n"
    "- **Depende de:** R3.2 (HECHA).\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está "
    "repetida\n"
    "  con los tres comandos de R3.1.\n"
    "- **Estado:** HECHA (`trabajo/punto-usado`; PUNTO-USADO.md): ADR-0083; `liberar_usada` y el\n"
    "  rechazo al llenar gasta el punto, por el cableado; 13 tests por el cableado real (4 rompen\n"
    "  en `main` por D1); la corrida 2 repetida con los tres comandos de R3.1 (§4). PROVISIONAL "
    "en\n"
    "  D1 hasta la pregunta 3 de la sesión 5 (R4.1).\n"
)
hoja = cambiar(hoja, R34_VIEJA, R34_NUEVA)
hoja = cambiar(
    hoja,
    "  ID:A-53 · ID:A-57 · ID:RN-007 · NA:H · NA:J · NA:V · NA:Y · ID:RN-004 · ID:RN-020 ·",
    "  ID:A-53 · ID:A-57 · ID:RN-007 · NA:H · NA:J · NA:V · ID:RN-004 · ID:RN-020 ·",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (HECHA), R3.2 (HECHA), R3.3 (HECHA), R3.4 (NA:Y) y",
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (HECHA), R3.2 (HECHA), R3.3 (HECHA), R3.4 (HECHA)"
    " y",
)
hoja = cambiar(
    hoja,
    "  día oculto). Una E (la reentrada en un punto ya llenado: R3.4) y el resto «correcto», que\n",
    "  día oculto). Una E (la reentrada en un punto ya llenado: R3.4, que ADR-0083 rehízo en el\n"
    "  sentido contrario: el llenado no gasta el punto) y el resto «correcto», que\n",
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
