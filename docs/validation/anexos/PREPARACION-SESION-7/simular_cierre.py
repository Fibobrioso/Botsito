"""Las propuestas para la orden de cierre de trabajo/preparacion-sesion-7, comprobadas con las
funciones de tests/unit/test_hoja_de_ruta.py (problemas_a a problemas_d) sobre COPIAS en memoria de
PROJECT_STATE.md y HOJA-DE-RUTA.md (no escribe nada), con un mutante que tiene que fallar.

Uso (desde la raiz): uv run python simular_cierre.py
"""

import importlib.util
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
_spec = importlib.util.spec_from_file_location("hoja_de_ruta", "tests/unit/test_hoja_de_ruta.py")
t = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(t)

ps = Path("PROJECT_STATE.md").read_text(encoding="utf-8")
hoja = Path("docs/plan/HOJA-DE-RUTA.md").read_text(encoding="utf-8")
historia = Path("docs/state/HISTORIA.md").read_text(encoding="utf-8")

# --- F, entera
lineas = ps.split("\n")
(i_f,) = [i for i, ln in enumerate(lineas) if ln.startswith("F. Sesión 6 ACTIVADA")]
NUEVO_F = (
    "F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7. La re-corrida "
    "que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; "
    "línea base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Las trazas del motor y la "
    "ablación por regla (TRAZAS-ABLACION.md; `motor decisiones`) y las láminas del bot (LAMINAS.md; "
    "`motor laminas`; R4.5) están hechas. La sesión 7 está preparada en dos días, 7a (sesion-07) y "
    "7b (sesion-08) (PREPARACION-SESION-7.md; R4.3): el método en ADR-0093, que cambia la regla 2 "
    "de SESION-DE-PREGUNTAS.md (el bloque de días enseña las láminas); el pivote pre-registrado en "
    "docs/plan/PIVOTES-SESION-7.yaml; las preguntas en docs/sesion-7/; las láminas de la 7a fuera "
    "del repo. Siguiente, en este orden: (1) grabar, ingerir y activar la 7a; su activación genera "
    "las láminas de la 7b con su motor, revisa PREGUNTAS-7B.md y pasa SESION_EN_CURSO a \"08\"; (2) "
    "grabar, ingerir y activar la 7b, con la rama de S-22 y S-19; (3) la corrida de ADR-0070 §3 y "
    "la lectura del pivote (ADR-0093 §6). El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo, "
    "por su propia rama. C, R5.7 y R6a en los huecos."
)
lineas[i_f] = NUEVO_F
ps2 = "\n".join(lineas)

# --- Technical Debt: una linea nueva y la de ingerir-sesion ampliada
VIEJA_SKILL = (
    "SESION-06-EXTRACCION.md §7, puntos 1 y 3; segunda vez): rama corta de skills."
)
assert ps2.count(VIEJA_SKILL) == 1
ps2 = ps2.replace(
    VIEJA_SKILL,
    VIEJA_SKILL[:-1] + "; y no dice que ningún fotograma se abre antes de que la voz o uno ya "
    "abierto sitúen el tramo, ADR-0093 §2.",
)
ULTIMA_TD = "- `motor laminas`: la CLI solo se prueba entera con las velas reales"
assert ps2.count(ULTIMA_TD) == 1
NUEVA_TD = (
    "- Dos textos que ADR-0093 deja viejos y que trabajo/preparacion-sesion-7 no podía tocar: "
    "scripts/graficos_sesion.py:66-71, con su test (su constante ya no es la regla 2), y "
    "engine/decisiones.py:7-8 (el ADR del método ya existe) (PREPARACION-SESION-7.md §0.2, H8 y "
    "H19).\n"
)
ps2 = ps2.replace(ULTIMA_TD, NUEVA_TD + ULTIMA_TD)

# --- R0.3 HECHA, sin NA:F en su bloque
b03 = hoja.split("### R0.3 · ", 1)[1].split("\n### ", 1)[0]
n03 = b03.replace(
    "- **Refs:** ID:ADR-0092 · ID:ADR-0070 · NA:F", "- **Refs:** ID:ADR-0092 · ID:ADR-0070 · ID:ADR-0093"
).replace("- **Estado:** ABIERTA.", "- **Estado:** HECHA (trabajo/preparacion-sesion-7, ADR-0093).")
assert n03 != b03 and "NA:F" not in n03
hoja2 = hoja.replace(b03, n03)

# --- R4.3: el reparto definitivo y sin J
b43 = hoja2.split("### R4.3 · ", 1)[1].split("\n### ", 1)[0]
QUE_ES_VIEJO = [ln for ln in b43.split("\n") if ln.startswith("- **Qué es:**")][0]
QUE_ES_NUEVO = (
    "- **Qué es:** con el método de ADR-0093 (RUMBO §1): como mucho seis preguntas técnicas por día "
    "y un bloque de días con las láminas de R4.5. Preparada en `trabajo/preparacion-sesion-7` "
    "(PREPARACION-SESION-7.md), con el reparto que aprobó el consultor el 2026-11-11: 7a "
    "(sesion-07), el rango de H4, el break even (A-13), las zonas de control del esquema (RN-009), "
    "A-35, cuándo se coloca la orden (ADR-0064) y las entradas válidas que deja sin tomar (F7 #10), "
    "más el bloque de días (docs/sesion-7/PREGUNTAS-7A.md); 7b (sesion-08), dónde pone el 0 de la caja "
    "(A-48), S-22, S-19, el «igual» y la caja de la reentrada (ADR-0083 D1), A-53 y A-43, más el "
    "bloque de días y, al final, la tarde del 10 de julio (docs/sesion-7/PREGUNTAS-7B.md, con los "
    "cuatro que no caben). Las láminas de la 7b las genera la activación de la 7a. El pivote, "
    "pre-registrado en docs/plan/PIVOTES-SESION-7.yaml (ADR-0093 §6)."
)
DEPENDE_VIEJO = "- **Depende de:** R4.4 y R4.5; J, si la hoja sale de `kit hoja`; el vídeo de mapeo del trader, si llega antes."
DEPENDE_NUEVO = "- **Depende de:** R4.4 y R4.5; el vídeo de mapeo del trader, si llega antes."
assert b43.count(DEPENDE_VIEJO) == 1
n43 = b43.replace(QUE_ES_VIEJO, QUE_ES_NUEVO).replace(DEPENDE_VIEJO, DEPENDE_NUEVO)
hoja2 = hoja2.replace(b43, n43)

# --- un mutante: R0.3 HECHA dejando NA:F en su bloque
hoja_mut = hoja.replace(
    b03, b03.replace("- **Estado:** ABIERTA.", "- **Estado:** HECHA (trabajo/preparacion-sesion-7, ADR-0093).")
)

ids = t._ids_existentes()
funcs = t._funcionalidades()
amb = t._estados_de_ambiguedades(Path("knowledge/spec/ambiguedades.yaml").read_text(encoding="utf-8"))
for nombre, (p, h) in {
    "hoy": (ps, hoja),
    "con las propuestas": (ps2, hoja2),
    "mutante (R0.3 HECHA con NA:F)": (ps2, hoja_mut),
}.items():
    print(f"== {nombre}")
    print("  a:", t.problemas_a(p, h))
    print("  b:", t.problemas_b(p, h, historia, ids, funcs))
    print("  c:", t.problemas_c(p))
    print("  d:", t.problemas_d(h, t._extracciones(), amb))
print("== bytes de PROJECT_STATE: hoy", len(ps.encode("utf-8")), "; con las propuestas", len(ps2.encode("utf-8")))
print("== bytes de la línea nueva de Technical Debt:", len(NUEVA_TD.encode("utf-8")))
print("== F nueva:", len(NUEVO_F.encode("utf-8")), "bytes; F de hoy:", len(ps.split(chr(10))[i_f].encode("utf-8")))
