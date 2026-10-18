"""Simula las lineas preparadas para el commit del contrato de la orden de cierre de
`trabajo/visor-construccion` (VISOR-CONSTRUCCION.md §4) contra tests/unit/test_hoja_de_ruta.py y
tests/unit/test_project_state.py, como `anexos/SESGO-H4-COLOR/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
propuestos como sustituciones exactas (cada una tiene que casar UNA vez). Corre las funciones a, b
y c de test_hoja_de_ruta.py sobre el texto simulado, y las tres de test_project_state.py (sus
secciones y su orden, `Current Branch` no vacio, menos de 25.000 bytes) sobre una copia del
PROJECT_STATE simulado en una carpeta temporal fuera del repo, que se borra al acabar. En el repo
no escribe nada.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/simular_cierre.py <raiz del repo>
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


# §4.1 Next Action: O sale entera (a HISTORIA, con su texto literal); entra Y; F y V cambian
linea_o = next(x for x in ps.splitlines() if x.startswith("O. "))
ps = cambiar(ps, linea_o + "\n", "")
historia += (
    "\n# Next Action HECHA · O · las comprobaciones en el visor · sale de PROJECT_STATE.md en "
    "trabajo/visor-construccion (2026-10-18)\n\n" + linea_o + "\n\nLa hace "
    "`trabajo/visor-construccion` (docs/validation/VISOR-CONSTRUCCION.md).\n"
)
linea_f = next(x for x in ps.splitlines() if x.startswith("F. "))
F_NUEVA = (
    "F. Y → V. Las re-corridas de R3.1 con el sesgo nuevo (SESGO-H4-COLOR.md §4) y con el límite "
    "del lote (MARGEN-LOTE.md §4) están hechas. Y va antes de V: cambia las reentradas de la "
    "pregunta 3."
)
ps = cambiar(ps, linea_f, F_NUEVA)
Y_NUEVA = (
    "Y. Que el punto de una orden ya llenada no se vuelva a colocar con otra caja (ADR-0064, "
    "decisión 1): hoy se marca la zona y no el punto; en la corrida 2, hasta 47 órdenes en 22 "
    "sesiones van al 0 de una ya llenada (VISOR-CONSTRUCCION.md §2.d.4). Rama de código, con su "
    "test y la corrida 2 repetida."
)
ps = cambiar(ps, F_NUEVA + "\n", F_NUEVA + "\n\n" + Y_NUEVA + "\n")
ps = cambiar(
    ps,
    "en su orden; y A-57 (el lote que no cabe, MARGEN-LOTE.md §5). Depende de R1.1, de R3.1, de O, "
    "de J (kit hoja) y de la copia de seguridad (A.4).",
    "en su orden; A-57 (el lote que no cabe, MARGEN-LOTE.md §5); y las preguntas de "
    "VISOR-CONSTRUCCION.md §3.2. Depende de R1.1, de R3.1, de Y, de J (kit hoja) y de la copia de "
    "seguridad (A.4).",
)

# §4.2 Hoja de ruta: R3.2 HECHA; R3.4 nueva (NA:Y); R4.1 sin NA:O, con las preguntas nuevas
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** cada comprobación tiene su gráfico y su conclusión (E o R) en un informe.\n",
    "- **Hecho cuando:** cada comprobación tiene su gráfico y su conclusión (E o R) en un informe.\n"
    "- **Estado:** HECHA (`trabajo/visor-construccion`; VISOR-CONSTRUCCION.md): los gráficos son\n"
    "  las páginas del visor, regenerables con los comandos del informe (§2.c), fuera de git; 19\n"
    "  días con «no» de `contexto_h4.py`, que se pueden enseñar a V (si el visor o la spec cambian\n"
    "  lo que pintan, se vuelven a comprobar antes), y 2026-07-01 sin página (su contexto pinta un\n"
    "  día oculto). Una E (la reentrada en un punto ya llenado: R3.4) y el resto «correcto», que\n"
    "  aquí quiere decir que la regla se aplica como está escrita y la diferencia con el trader es\n"
    "  de regla: va a V con sus preguntas (§3.2).\n",
)
R34 = (
    "### R3.4 · Un punto ya llenado no se vuelve a colocar\n"
    "- **Refs:** NA:Y · ID:ADR-0064 · ID:ADR-0074\n"
    "- **Qué es:** que el bot no vuelva a colocar, con otra caja, el punto cuya orden ya se llenó\n"
    "  (ADR-0064, decisión 1; VISOR-CONSTRUCCION.md §2.d.4), y la corrida 2 repetida.\n"
    "- **Depende de:** R3.2 (HECHA).\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está repetida\n"
    "  con los tres comandos de R3.1.\n\n"
)
hoja = cambiar(
    hoja, "## R4 · La sesión 5 con el trader y su activación\n", R34 + "## R4 · La sesión 5 con el "
    "trader y su activación\n"
)
hoja = cambiar(
    hoja,
    "ID:A-53 · ID:A-57 · ID:RN-007 · NA:H · NA:J · NA:V · NA:O · HER:25 · HER:30 · HER:35 ·",
    "ID:A-53 · ID:A-57 · ID:RN-007 · NA:H · NA:J · NA:V · NA:Y · HER:25 · HER:30 · HER:35 ·",
)
hoja = cambiar(
    hoja,
    "contradicción con la sesión 1; R1.2); y A-57 (el lote que no cabe, MARGEN-LOTE.md §5). La hoja",
    "contradicción con la sesión 1; R1.2); A-57 (el lote que no cabe, MARGEN-LOTE.md §5); y las\n"
    "  preguntas de VISOR-CONSTRUCCION.md §3.2 (las dos nuevas y los días que ganan la 5, la 8 y la\n"
    "  9; R3.2). La hoja",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (HECHA), R3.2 (NA:O), R3.3 (HECHA) y la copia de",
    "- **Depende de:** R1.1, R3.1 (HECHA), R1.2 (HECHA), R3.2 (HECHA), R3.3 (HECHA), R3.4 (NA:Y) y\n"
    "  la copia de",
)

# §4.3 Technical Debt: las cinco lineas
DEUDAS = [
    "- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2557; el arnés sí, :2437): con "
    "`--todos` arrastra la cuenta (VISOR-CONSTRUCCION.md §4.3).",
    "- VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del "
    "mes anterior (VISOR-CONSTRUCCION.md §4.3).",
    "- El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; "
    "VISOR-CONSTRUCCION.md §4.3).",
    "- `test_visor.py` hace leer al visor el M1 de marzo (calienta abril) en cada make check "
    "(HOLDOUT-EXPOSICIONES, 2026-10-18; VISOR-CONSTRUCCION.md §4.3).",
    "- `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker "
    "(VISOR-CONSTRUCCION.md §4.3).",
    "- El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana: los "
    "ticks empiezan en ventana_inicio y la orden lleva 1 ms antes (VISOR-CONSTRUCCION.md §4.3).",
]
ps = cambiar(
    ps,
    "Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.\n",
    "Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.\n"
    + "\n".join(DEUDAS)
    + "\n",
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
