"""Simula las lineas preparadas para el commit del contrato del cierre de `trabajo/respaldo-m1`
(RESPALDO-M1.md §6; respuestas del consultor a la PARADA, puntos 0, 2, 3 y 8, y al encargo, 5)
contra tests/unit/test_hoja_de_ruta.py (a, b y c) y tests/unit/test_project_state.py, como
`anexos/RECORRIDA-CONSTRUCCION/simular_cierre.py`.

Lee PROJECT_STATE.md, HOJA-DE-RUTA.md y HISTORIA.md de la raiz dada y aplica en memoria los cambios
como sustituciones exactas (cada una tiene que casar UNA vez). Las comprobaciones de PROJECT_STATE
corren sobre una copia en una carpeta temporal fuera del repo, que se borra al acabar. En el repo no
escribe nada. No simula lo que el ritual de cierre pone en Current Branch, Current Feature y las
secciones de main (RITUAL.md): solo las lineas que prepara la rama.

    uv run python docs/validation/anexos/RESPALDO-M1/simular_cierre.py <raiz>
"""

# ruff: noqa: E501  (las sustituciones son literales de los documentos: tienen que casar tal cual)
from __future__ import annotations

import importlib.util
import re
import sys
import tempfile
from pathlib import Path
from types import ModuleType

raiz = Path(sys.argv[1])
FECHA = "2026-10-29"
LETRA = "H"  # respuesta del consultor a la PARADA, punto 8, y a la PARADA 2, punto 2


def _cargar(nombre: str, ruta: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


thr = _cargar("thr", raiz / "tests" / "unit" / "test_hoja_de_ruta.py")
tps = _cargar("tps", raiz / "tests" / "unit" / "test_project_state.py")

ps = (raiz / "PROJECT_STATE.md").read_text(encoding="utf-8")
hoja_main = (raiz / "docs" / "plan" / "HOJA-DE-RUTA.md").read_text(encoding="utf-8")
hoja = hoja_main
historia = (raiz / "docs" / "state" / "HISTORIA.md").read_text(encoding="utf-8")


def cambiar(texto: str, viejo: str, nuevo: str) -> str:
    assert texto.count(viejo) == 1, viejo[:80]
    return texto.replace(viejo, nuevo)


# --- PROJECT_STATE: Z sale a HISTORIA y H entra en su sitio; F sin «y Z»; la deuda de cotizar
linea_z = next(x for x in ps.splitlines() if x.startswith("Z. "))
NUEVA = (
    f"{LETRA}. En el respaldo M1 el evento de una vela se sella en su cierre, un milisegundo después "
    "de que el motor decida (ADR-0051 §5, ADR-0057 §1). Por eso la vela k no se evalúa para lo que "
    "vivía en ella cuando el motor actúa en su cierre (22 de 1002 cancelaciones en la corrida diaria "
    "de recorrida-construccion, RESPALDO-M1.md §0.l), y _peor_del_minuto marca entera la vela "
    "siguiente cuando se avanza hasta un instante redondo. Rama propia con un ADR que enmiende esos "
    "dos ADR. Antes de decidir, se mide lo que el auditor de RESPALDO-M1 encontró en la forma "
    "«sellar en k fin - 1»: las marcas y m1_entre del break even empiezan a contar la vela del "
    "llenado, cambia la sesión de un llenado en la última vela de 07-11, cambian el fin de la "
    "ventana y el borde de ADR-0068, y rompen 5 tests de main por el milisegundo. Va antes de la "
    "próxima corrida del arnés que cuente (ADR-0070 §3)."
)
ps = cambiar(ps, linea_z, NUEVA)
historia += (
    f"\n# Next Action HECHA · Z · sale de PROJECT_STATE.md en trabajo/respaldo-m1 ({FECHA})\n\n"
    + linea_z
    + "\n\nLa hace `trabajo/respaldo-m1` (docs/validation/RESPALDO-M1.md): una vela del respaldo M1 "
    "solo evalúa lo decidido antes de que empezara (ADR-0051 §5, NOTA del 2026-10-29); 2 llenadas y "
    "0 stops en la corrida que cuenta y 10 llenadas y 2 stops en la diaria de recorrida-construccion "
    "dejan de evaluarse con la vela de su decisión, y las dos corridas repetidas dan Z = 0; el "
    "veredicto de ADR-0070 §3 sigue «no».\n"
)
ps = cambiar(ps, " R6a y Z en los huecos.", " R6a en los huecos.")
DEUDA = (
    "- Las cotizaciones sin tick del bróker no usan la misma vela. En el cierre de la M1 k, "
    "Mercado.cotizacion (precio_invalido y stops_level, ADR-0057 §4) usa lo último cerrado antes del "
    "instante, que sin ticks es la M1 k-1 o el último tick anterior, y _precio_de_mercado y "
    "precio_de_conversion (cierre a mercado y margen) usan la k. Y en un minuto con ticks sin ninguno "
    "anterior al instante, estas dos toman el cierre de su vela; el motor no llega a ese caso "
    "(RESPALDO-M1.md §0.a y §0.b). Decidirlo es una NOTA o un ADR sobre ADR-0057 §4.\n"
)
ps = cambiar(ps, "\n## Reglas vivas\n", DEUDA + "\n## Reglas vivas\n")

# --- La hoja de ruta: R3.5 HECHA sin NA:Z; R3.6 nueva con la letra; R5.2 nombra la letra nueva
hoja = cambiar(
    hoja,
    "### R3.5 · El respaldo M1 no llena con la vela que colocó la orden\n- **Refs:** NA:Z · ID:ADR-0051\n",
    "### R3.5 · El respaldo M1 no llena con la vela que colocó la orden\n- **Refs:** ID:ADR-0051\n",
)
R36 = (
    "### R3.6 · El respaldo M1 sella en el cierre, después de que el motor decida\n"
    f"- **Refs:** NA:{LETRA} · ID:ADR-0051 · ID:ADR-0057\n"
    "- **Qué es:** el evento de una vela del respaldo se sella en su cierre, un milisegundo después\n"
    "  de que el motor decida: la vela no se evalúa para lo que vivía en ella cuando el motor actúa\n"
    "  en su cierre, y `_peor_del_minuto` marca entera la vela siguiente al avanzar hasta un instante\n"
    "  redondo (RESPALDO-M1.md §0.a y §0.l). Rama propia con un ADR que enmiende ADR-0051 §5 y\n"
    "  ADR-0057 §1.\n"
    "- **Depende de:** R3.5.\n"
    "- **Quién:** la sesión, con el encargo del consultor.\n"
    "- **Hecho cuando:** el ADR está aceptado, un test que rompe en `main` pasa en la rama y las dos\n"
    "  corridas están repetidas.\n"
    "\n"
)
hoja = cambiar(
    hoja,
    "  la rama, y las dos corridas de `trabajo/recorrida-construccion` están repetidas en la suya.\n\n",
    "  la rama, y las dos corridas de `trabajo/recorrida-construccion` están repetidas en la suya.\n"
    "- **Estado:** HECHA (`trabajo/respaldo-m1`, `stable/F38j-respaldo-m1`; RESPALDO-M1.md): una vela del\n"
    "  respaldo solo evalúa lo decidido antes de que empezara (ADR-0051 §5, NOTA); 8 tests rompen en\n"
    "  `main` y pasan en la rama; las dos corridas repetidas dan cero eventos con la vela de su\n"
    "  decisión, y la que cuenta sigue en «no».\n\n" + R36,
)
hoja = cambiar(
    hoja,
    "  rama de medida (ADR-0070 §6); y NA:Z, el respaldo M1 corregido (R3.5).",
    f"  rama de medida (ADR-0070 §6); y NA:{LETRA}, el sello del respaldo M1 (R3.6).",
)

# --- Las comprobaciones
ids = thr._ids_existentes()
funciones = thr._funcionalidades()
print(
    f"letra {LETRA}: viva en la copia simulada? {LETRA in thr.entradas_vivas(ps)}; HECHA en HISTORIA? "
    f"{LETRA in thr.letras_hechas(historia)}; NA:{LETRA} en la hoja de main? "
    f"{bool(re.search(rf'NA:{LETRA}(?![\w-])', hoja_main))}; Z viva en la copia? "
    f"{'Z' in thr.entradas_vivas(ps)}; NA:Z en la hoja simulada? "
    f"{bool(re.search(r'NA:Z(?![\w-])', hoja))}"
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
