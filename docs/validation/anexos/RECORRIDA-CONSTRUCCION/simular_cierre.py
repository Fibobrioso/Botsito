"""Simula las lineas preparadas para el commit del contrato del cierre de
`trabajo/recorrida-construccion` (RECORRIDA-CONSTRUCCION.md §6 y la respuesta del consultor a la
PARADA 3, punto 1 c) contra tests/unit/test_hoja_de_ruta.py (a, b y c) y
tests/unit/test_project_state.py, como `anexos/PUNTO-USADO/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
como sustituciones exactas (cada una tiene que casar UNA vez). La letra de la entrada nueva de la
Next Action llega por argumento, porque la decide el consultor (PARADA 4). Las comprobaciones de
PROJECT_STATE corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar.
En el repo no escribe nada.

    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py <raiz> <letra>
"""

# ruff: noqa: E501  (las sustituciones son literales de la hoja de ruta: tienen que casar tal cual)
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from pathlib import Path
from types import ModuleType

raiz = Path(sys.argv[1])
letra = sys.argv[2]
FECHA = "2026-10-27"


def _cargar(nombre: str, ruta: Path) -> ModuleType:
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


# --- PROJECT_STATE: V sale a HISTORIA; F cambia; la letra nueva entra tras N; sale una deuda
linea_v = next(x for x in ps.splitlines() if x.startswith("V. "))
ps = cambiar(ps, linea_v + "\n\n", "")
historia += (
    f"\n# Next Action HECHA · V · sale de PROJECT_STATE.md en trabajo/recorrida-construccion "
    f"({FECHA})\n\n" + linea_v + "\n\nLa hace `trabajo/recorrida-construccion` "
    "(docs/validation/RECORRIDA-CONSTRUCCION.md: la corrida que cuenta por ADR-0070 §3 dio «no»).\n"
)
linea_f = next(x for x in ps.splitlines() if x.startswith("F. "))
ps = cambiar(
    ps,
    linea_f,
    "F. La rama corta de la cuarentena por condición (Technical Debt, PRIORITARIA) antes de "
    "ingerir la sesión 6; la preparación de la sesión 6 (R4.2); R6a en los huecos.",
)
NUEVA = (
    f"{letra}. El bróker simulado llena con el respaldo M1 una orden en la vela cuyo cierre la "
    "colocó, en todo minuto sin ticks (el borde de la ventana y las horas perdidas), contra "
    "ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8; antes, VISOR-CONSTRUCCION.md §4.3). Rama propia "
    "con su test que rompe en main, una NOTA en ADR-0051 §5 y las corridas repetidas; antes de la "
    "próxima corrida del arnés que cuente (ADR-0070 §3)."
)
linea_n = next(x for x in ps.splitlines() if x.startswith("N. "))
ps = cambiar(ps, linea_n + "\n", linea_n + "\n\n" + NUEVA + "\n")
ps = cambiar(
    ps,
    "- El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana: los "
    "ticks empiezan en ventana_inicio y la orden lleva 1 ms antes (VISOR-CONSTRUCCION.md §4.3).\n",
    "",
)
ps = cambiar(ps, "## Current Branch\ntrabajo/recorrida-construccion\n", "## Current Branch\nmain\n")
cf = next(x for x in ps.splitlines() if x.startswith("trabajo/recorrida-construccion, EN CURSO"))
ps = cambiar(
    ps,
    cf,
    f"Ninguna rama abierta. trabajo/recorrida-construccion cerrada en main el {FECHA} "
    "(stable/F38g-recorrida-construccion): la corrida que cuenta por ADR-0070 §3 dio «no» "
    "(cobertura 3,5 %, precisión 13,2 %); se sigue construyendo (RECORRIDA-CONSTRUCCION.md).",
)

# --- La hoja de ruta: R4.1 HECHA sin NA:V; R4.2 sin NA:V y sin depender de la re-corrida; R5.2;
# R3.5 y G.5 nuevas
hoja = cambiar(
    hoja,
    "  ID:A-53 · ID:A-57 · ID:RN-007 · NA:V · ID:RN-004 · ID:RN-020 ·",
    "  ID:A-53 · ID:A-57 · ID:RN-007 · ID:RN-004 · ID:RN-020 ·",
)
hoja = cambiar(
    hoja,
    "- **Estado:** spec y motor HECHOS (`trabajo/activar-sesion-05`, `stable/F38e-activar-sesion-05`;\n"
    "  `trabajo/activar-sesion-05-motor`, `stable/F38f-activar-sesion-05-motor`;\n"
    "  ACTIVAR-SESION-05-MOTOR.md: ADR-0084 a ADR-0086, RN-037). Queda la re-corrida de ADR-0070 §3\n"
    "  con su `diff` (ACTIVAR-A35-A44.md §5.1), que mire las entradas que nacen en el primer punto tras\n"
    "  la toma y se llenan antes de la alternancia (ACTIVAR-SESION-05-MOTOR.md §0.b.8).\n",
    "- **Estado:** HECHA (`trabajo/activar-sesion-05`, `stable/F38e-activar-sesion-05`;\n"
    "  `trabajo/activar-sesion-05-motor`, `stable/F38f-activar-sesion-05-motor`;\n"
    "  `trabajo/recorrida-construccion`, el tag de su cierre: la corrida que cuenta por ADR-0070 §3\n"
    "  dio «no» -cobertura 3,5 %, precisión 13,2 %- y las dos listas para la sesión 6 están en\n"
    "  RECORRIDA-CONSTRUCCION.md §3 y §4).\n",
)
hoja = cambiar(hoja, "- **Refs:** NA:V · ID:A-35 · ID:A-44 ·", "- **Refs:** ID:A-35 · ID:A-44 ·")
hoja = cambiar(
    hoja,
    "  S-14 con los días de construcción que dé la re-corrida;",
    "  S-14 con las 34 sesiones de P6 de la re-corrida (RECORRIDA-CONSTRUCCION.md §4; 77 llenadas) y\n"
    "  el dibujo 3 de S-15 con las 259 entradas llenadas con menos de dos zonas de control (§3; 149\n"
    "  con cero, 110 con una), sin las marcadas E;",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** la re-corrida del arnés (R4.1, lo que queda).",
    "- **Depende de:** nada (la re-corrida está hecha, R4.1).",
)
hoja = cambiar(
    hoja,
    "- **Depende de:** R3.1, con una corrida que cuente (sin diagnóstico; ADR-0070 §3).",
    '- **Depende de:** la corrida que cuenta (R4.1; ADR-0070 §3) con un "sí", y el ADR propio de la\n'
    f"  rama de medida (ADR-0070 §6); y NA:{letra}, el respaldo M1 corregido (R3.5).",
)
R35 = (
    "### R3.5 · El respaldo M1 no llena con la vela que colocó la orden\n"
    f"- **Refs:** NA:{letra} · ID:ADR-0051\n"
    "- **Qué es:** en todo minuto sin ticks (el borde de la ventana y las horas perdidas) el bróker\n"
    "  simulado llena una orden con la vela M1 cuyo cierre la colocó, con precios anteriores a la\n"
    "  orden, contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8: 2 llenadas en la corrida que\n"
    "  cuenta, 10 en la diaria); se corrige con su test, una NOTA en ADR-0051 §5 y las corridas\n"
    "  repetidas.\n"
    "- **Depende de:** nada.\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** un test que llena con la vela que colocó la orden rompe en `main` y pasa en\n"
    "  la rama, y las dos corridas de `trabajo/recorrida-construccion` están repetidas en la suya.\n"
    "\n"
)
hoja = cambiar(
    hoja,
    "## R4 · La sesión 5 con el trader y su activación\n",
    R35 + "## R4 · La sesión 5 con el trader y su activación\n",
)
G5 = (
    "### G.5 · La cuarentena por condición\n"
    "- **Refs:** —\n"
    "- **Qué es:** la línea PRIORITARIA de Technical Debt: diciembre cuenta como libre en `meses_libres`\n"
    "  con NA:I sin decidir, y la fecha numérica seguida de coma no se tapa (SESION-05-EXTRACCION.md\n"
    "  §2.7 y §11, a4).\n"
    "- **Depende de:** nada.\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** los dos casos tienen su test que rompe en main y pasa en la rama, antes de\n"
    "  ingerir la sesión 6.\n"
    "\n"
)
hoja = cambiar(
    hoja,
    "## Carril: material reservado que no se toca\n",
    G5 + "## Carril: material reservado que no se toca\n",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
print(
    f"letra {letra}: viva en la copia simulada? {letra in thr.entradas_vivas(ps)}; HECHA en HISTORIA? "
    f"{letra in thr.letras_hechas(historia)}; NA:{letra} en la hoja de main? "
    f"{bool(re.search(rf'NA:{letra}(?![\w-])', (raiz / 'docs/plan/HOJA-DE-RUTA.md').read_text(encoding='utf-8')))}"
)
print("a:", thr.problemas_a(ps, hoja))
print("b:", thr.problemas_b(ps, hoja, historia, ids, funciones))
print("c:", thr.problemas_c(ps))
with tempfile.TemporaryDirectory() as tmp:
    copia = Path(tmp)
    (copia / "PROJECT_STATE.md").write_text(ps, encoding="utf-8", newline="\n")
    tps.test_project_state_exists(copia)
    tps.test_project_state_has_required_sections_in_order(copia)
    tps.test_project_state_declares_a_branch(copia)
    tps.test_project_state_cabe_en_el_tope(copia)
    print(
        f"PROJECT_STATE con las lineas del cierre: {len(ps.encode('utf-8'))} bytes (wc -c de la copia: "
        f"{(copia / 'PROJECT_STATE.md').stat().st_size}); los cuatro tests de test_project_state: ok"
    )
