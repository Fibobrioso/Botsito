"""Simula las lineas preparadas para el commit del contrato del cierre de `trabajo/cuenta-por-mes`
(CUENTA-POR-MES.md, fase 1, punto 4; encargo, punto 4): F se reescribe con el texto del encargo y
el resto de F igual (F sigue viva: no sale a HISTORIA); la linea del visor de Technical Debt queda
solo con lo de la diaria; en la hoja de ruta, R3.8 HECHA sin `NA:F` (F sigue viva,
tests/unit/test_hoja_de_ruta.py:144-145) y R5.2 y R5.6 sin la dependencia de R3.8. Como
`anexos/METODO-FIDELIDAD-RENTABILIDAD/simular_cierre.py`: contra tests/unit/test_hoja_de_ruta.py
(a, b y c) y tests/unit/test_project_state.py, cargados por su ruta LITERAL.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md del directorio de trabajo (la raiz del repo) y
aplica en memoria sustituciones exactas (cada una casa UNA vez). Las comprobaciones de PROJECT_STATE
corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar. En el repo no
escribe nada. Ademas simula las cuatro lineas de cabecera que escribe el ritual, para medir los bytes.

    uv run python -B docs/validation/anexos/CUENTA-POR-MES/simular_cierre.py
"""

# ruff: noqa: E501  (las sustituciones son literales de los documentos: tienen que casar tal cual)
from __future__ import annotations

import importlib.machinery
import importlib.util
import sys
import tempfile
from pathlib import Path
from types import ModuleType


def _modulo(spec: importlib.machinery.ModuleSpec | None) -> ModuleType:
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


thr = _modulo(importlib.util.spec_from_file_location("thr", "tests/unit/test_hoja_de_ruta.py"))
tps = _modulo(importlib.util.spec_from_file_location("tps", "tests/unit/test_project_state.py"))

raiz = Path.cwd()
ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: F, con el texto del encargo; el resto de F, igual
ps = cambiar(
    ps,
    "Siguiente: la rama de la cuenta por mes (ADR-0092, trabajo/cuenta-por-mes) y después la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091 y el método de ADR-0092;",
    "Siguiente: la re-corrida que cuenta (ADR-0070 §3), la primera con la comisión medida (ADR-0090 §3), el sello del respaldo de ADR-0091, el método de ADR-0092 y la cuenta por mes;",
)
# Technical Debt: la linea del visor, solo con lo de la diaria (lineas de cli.py medidas en la rama)
ps = cambiar(
    ps,
    "- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2557; el arnés sí, :2437): con `--todos` arrastra la cuenta (VISOR-CONSTRUCCION.md §4.3).\n",
    "- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2558; el arnés sí, :2438): con `--todos --simular` corre una cuenta por mes como el arnés (ADR-0092 §8), nunca la diaria (VISOR-CONSTRUCCION.md §4.3).\n",
)
# Technical Debt: una linea nueva, tras la del visor (revisor, a6)
ps = cambiar(
    ps,
    "nunca la diaria (VISOR-CONSTRUCCION.md §4.3).\n",
    "nunca la diaria (VISOR-CONSTRUCCION.md §4.3).\n"
    "- `curva_con_deslizamiento` y `veredicto_con_f17` (criterio_fidelidad.py) toman una sola curva y arrastran `previo` entre cuentas: cuando F17 los use, por cuenta (CUENTA-POR-MES.md, fase 0 e) 8).\n",
)

# --- La hoja de ruta
hoja = cambiar(
    hoja,
    "- **Refs:** NA:F · ID:ADR-0092 · ID:ADR-0053 · ID:ADR-0070\n",
    "- **Refs:** ID:ADR-0092 · ID:ADR-0053 · ID:ADR-0070\n",
)
hoja = cambiar(
    hoja,
    "- **Hecho cuando:** la cuenta empieza de nuevo en cada mes de construcción, con su test, y la\n"
    "  re-corrida que cuenta puede correr.\n",
    "- **Hecho cuando:** la cuenta empieza de nuevo en cada mes de construcción, con su test, y la\n"
    "  re-corrida que cuenta puede correr.\n"
    "- **Estado:** HECHA (`trabajo/cuenta-por-mes`; CUENTA-POR-MES.md): en `MotorCableado.correr_dia`,\n"
    "  al cambiar de mes empiezan de nuevo la cuenta, el seguidor del tope y el primer toque (NOTA de\n"
    "  ADR-0092 §8), con sus tests sintéticos; la diaria, intacta.\n",
)
hoja = cambiar(
    hoja,
    "  rama de medida (ADR-0070 §6); y la cuenta por mes (R3.8). El sello del respaldo M1 (R3.6)\n"
    "  y el método (R3.7, ADR-0092) están HECHOS.\n",
    "  rama de medida (ADR-0070 §6). El sello del respaldo M1 (R3.6), el método (R3.7, ADR-0092)\n"
    "  y la cuenta por mes (R3.8) están HECHOS.\n",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R5.1 (G) y la re-corrida que cuenta, después de R3.8, con su línea «habilita medir» en sí (ADR-0070 punto 5; ADR-0092 §5).\n",
    "- **Depende de:** R5.1 (G) y la re-corrida que cuenta, con su línea «habilita medir» en sí (ADR-0070 punto 5; ADR-0092 §5).\n",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
r38 = hoja.split("### R3.8 ", 1)[1].split("\n### ", 1)[0]
print(
    f"F viva en la copia? {'F' in thr.entradas_vivas(ps)}; NA:F en R3.8? {'NA:F' in r38}; "
    f"R3.8 HECHA? {'- **Estado:** HECHA' in r38}"
)
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
r52 = hoja.split("### R5.2 ", 1)[1].split("\n### ", 1)[0]
r56 = hoja.split("### R5.6 ", 1)[1].split("\n### ", 1)[0]
depende_r52 = r52.split("- **Depende de:**", 1)[1].split("- **Quién:**", 1)[0]
depende_r56 = next(x for x in r56.splitlines() if x.startswith("- **Depende de:**"))
print(
    f"«la rama de la cuenta por mes» en la copia? {'la rama de la cuenta por mes' in ps}; "
    f"R3.8 como dependencia pendiente de R5.2? {'y la cuenta por mes (R3.8).' in depende_r52}; "
    f"R3.8 en el «Depende de» de R5.6? {'R3.8' in depende_r56}"
)


def _seccion(texto: str, titulo: str, nuevo: str) -> str:
    """Sustituye el cuerpo (una linea) de una seccion `## titulo` de PROJECT_STATE."""
    viejo = texto.split(f"## {titulo}\n", 1)[1].split("\n\n", 1)[0]
    return cambiar(texto, f"## {titulo}\n{viejo}\n", f"## {titulo}\n{nuevo}\n")


# las CUATRO lineas de cabecera que escribe el ritual, con la forma de las de main y un sha de 7
# caracteres de relleno; el tag, el siguiente libre (F38s)
SHA = "xxxxxxx"
ps_cierre = _seccion(ps, "Current Branch", "main")
ps_cierre = _seccion(
    ps_cierre,
    "Current Feature",
    "Ninguna rama abierta. trabajo/cuenta-por-mes cerrada en main el 2026-11-0X "
    "(stable/F38s-cuenta-por-mes): una cuenta por mes en el motor (ADR-0092 §8): la cuenta, el "
    "seguidor del tope y el primer toque empiezan de nuevo al cambiar de mes.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Stable Main State",
    f"{SHA} · merge de `trabajo/cuenta-por-mes` (tag `stable/F38s-cuenta-por-mes`), sobre "
    "`stable/F38r-metodo-fidelidad-rentabilidad` (a1907fa). Informe docs/validation/CUENTA-POR-MES.md; "
    "el registro del cierre, al final de HISTORIA.",
)
ps_cierre = _seccion(
    ps_cierre,
    "Last Stable Commit",
    f"{SHA} · merge: trabajo/cuenta-por-mes, una cuenta por mes en el motor (ADR-0092 §8): la "
    "cuenta, el seguidor del tope y el primer toque empiezan de nuevo al cambiar de mes · tag "
    "stable/F38s-cuenta-por-mes",
)
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano = (copia / "PROJECT_STATE.md").stat().st_size
    (copia / "PROJECT_STATE.md").write_text(ps_cierre, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    tamano_cierre = (copia / "PROJECT_STATE.md").stat().st_size
    print(
        f"PROJECT_STATE con las lineas del cierre: {tamano} bytes (st_size de la copia, los mismos "
        f"que wc -c); con las cuatro lineas de cabecera del cierre: {tamano_cierre}; los cuatro "
        "tests de test_project_state, sobre las dos: ok"
    )
    if max(tamano, tamano_cierre) >= 23_000:
        print("POR ENCIMA de la alerta de 23.000 del consultor", file=sys.stderr)
        sys.exit(1)
