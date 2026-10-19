"""Simula las lineas preparadas para el commit del contrato de la orden de cierre de
`trabajo/ea-conexion` (EA-CONEXION.md, «Lineas preparadas») contra tests/unit/test_hoja_de_ruta.py y
tests/unit/test_project_state.py, como `anexos/VISOR-CONSTRUCCION/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
propuestos como sustituciones exactas (cada una tiene que casar UNA vez). Corre las funciones a, b
y c de test_hoja_de_ruta.py sobre el texto simulado, y las de test_project_state.py sobre una copia
del PROJECT_STATE simulado en una carpeta temporal fuera del repo, que se borra al acabar. En el
repo no escribe nada.

    uv run python docs/validation/anexos/EA-CONEXION/simular_cierre.py <raiz del repo>
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


# --- la hoja de ruta: R6a.1 HECHA; su «Que es», su «Quien» y su «Hecho cuando»; R6a.2, R6a.7, A.1.
# Una entrada HECHA no nombra una letra viva (test_hoja_de_ruta.py, b): N sigue viva, asi que R6a.1
# pierde su NA:N (en las referencias y en el texto).
hoja = cambiar(
    hoja,
    "- **Refs:** ID:ADR-0082 · F:F31 · F:F33 · F:F17 · ID:A-28 · NA:N\n",
    "- **Refs:** ID:ADR-0082 · F:F31 · F:F33 · F:F17 · ID:A-28\n",
)
hoja = cambiar(
    hoja,
    "  sesiones del símbolo con `SymbolInfoSessionTrade` (condición 2 de NA:N, `RENOVAR-CIERRES.md`);\n"
    "  comprueba `ACCOUNT_MARGIN_MODE` al arrancar (MASTER_PLAN §H); y fija el formato del journal, uno\n",
    "  sesiones del símbolo con `SymbolInfoSessionTrade` (condición 2 de `RENOVAR-CIERRES.md`);\n"
    "  lee y registra `ACCOUNT_MARGIN_MODE` al arrancar, sin abortar, y lo compara R6a.7 (MASTER_PLAN\n"
    "  §H; ADR-0082 §10, recuadro del 2026-10-19); y fija el formato del journal, uno\n",
)
hoja = cambiar(
    hoja,
    "- **Quién:** la sesión, con el encargo del consultor; Aleks compila y ejecuta en su máquina y en\n"
    "  la demo.\n"
    "- **Hecho cuando:** el EA conecta en la demo, escribe el journal con el desfase y las sesiones del\n"
    "  símbolo, y se niega fuera de una demo.\n",
    "- **Quién:** la sesión, con el encargo del consultor: compila y ejecuta las pruebas en la máquina\n"
    "  de Aleks (`src/botsito/mql5bridge/compilar.py`); Aleks pone el EA en la demo.\n"
    "- **Hecho cuando:** el EA conecta en la demo, escribe el journal con el desfase y las sesiones del\n"
    "  símbolo, y se niega fuera de una demo; esto último lo prueban las pruebas estáticas de la CI y\n"
    "  las dinámicas del script de pruebas, porque no se ejecuta en una cuenta real.\n"
    "- **Estado:** HECHA (`trabajo/ea-conexion`, `stable/F37x-ea-conexion`; EA-CONEXION.md): el EA\n"
    "  `mql5/Experts/Botsito.mq5`, el journal v1 (`mql5/JOURNAL.md`) con su validador y su golden, y\n"
    "  la corrida en la demo con el journal congelado en los anexos.\n",
)
hoja = cambiar(
    hoja,
    "  calendario de cierres, generados desde el repo para el EA, con su propio hash en el journal; ni\n"
    "  una cifra a mano (ADR-0082 D5). La parte de estrategia de F28 espera a F26.\n",
    "  calendario de cierres, generados desde el repo para el EA, con su propio hash en el journal; ni\n"
    "  una cifra a mano (ADR-0082 D5). La parte de estrategia de F28 espera a F26. Si se decide, también\n"
    "  `LATIDO_SEG` y `TOPE_SESIONES`, las dos cifras del formato del journal (`mql5/JOURNAL.md`).\n",
)
hoja = cambiar(
    hoja,
    "  si algo no cuadra (MASTER_PLAN §H y §H.2).\n",
    "  si algo no cuadra (MASTER_PLAN §H y §H.2). Antes de comparar `ACCOUNT_MARGIN_MODE`, el parámetro\n"
    "  del modo de margen se crea con su fuente, la respuesta de FTMO sobre la cuenta Swing (A.2).\n",
)
hoja = cambiar(
    hoja,
    "- **Quién:** Aleks ejecuta; la sesión congela cada CSV en su rama.\n",
    "- **Quién:** Aleks ejecuta; los dos CSV los congela una sola rama, tras la ejecución 3, que es la\n"
    "  que decide A-28 con los dos (EA-CONEXION.md, D6).\n",
)

# --- PROJECT_STATE: N y las lineas de Technical Debt
ps = cambiar(
    ps,
    "La condición 2 la cumplirá R6a.1, que trae la lectura de SymbolInfoSessionTrade, y R6a.5 la usa "
    "(ADR-0082 D6).",
    "La condición 2 la cumple la lectura de SymbolInfoSessionTrade de R6a.1 (EA-CONEXION.md, el "
    "journal de la demo en sus anexos), y R6a.5 la usa (ADR-0082 D6).",
)
DEUDAS = [
    "- El validador del journal v1 vive en `botsito.mql5bridge`, que `engine` no puede importar "
    "(import-linter): cuando F23 lo necesite, el esquema baja a una capa que `engine` vea, en su rama "
    "y tocando pyproject.toml (EA-CONEXION.md, respuesta a la PARADA, punto 4).",
    "- El modo texto ANSI de MT5 (build 6230) escribe CRLF y el CSV de la ejecución 1 de "
    "MedirDemoFTMO tiene LF, sin explicación: la rama que congele los CSV de las ejecuciones 2 y 3 "
    "comprueba el CRLF del CSV 2 en `MQL5\\Files` antes de copiarlo (EA-CONEXION.md §0.c).",
    "- La comprobación del LF final en `UltimaLinea` (`mql5/Include/Botsito/Capa/Journal.mqh`) es "
    "redundante con la del formato: ninguna prueba la caza sola (EA-CONEXION.md §6, rotura r3).",
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
