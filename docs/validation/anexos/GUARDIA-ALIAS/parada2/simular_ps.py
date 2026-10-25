"""Simula EN MEMORIA el PROJECT_STATE del commit del contrato del cierre con la respuesta a la
PARADA 2, punto 3: K pierde su parte PRIORITARIA; sale la linea del docstring (punto 7); entran la
de los riesgos residuales y la de las llaves y file:///. Solo mide bytes; no escribe nada."""

import sys
from pathlib import Path

ps = Path(sys.argv[1]).read_text(encoding="utf-8")
lineas = ps.split("\n")
k = [i for i, l in enumerate(lineas) if l.startswith("K. PRIORITARIA")]
td = [i for i, l in enumerate(lineas) if l.startswith("- El docstring de `tests/contract/test_tramos_fuente.py:5`")]
assert len(k) == 1 and len(td) == 1, (k, td)
NUEVA_K = (
    "K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada "
    "crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que "
    "la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos. Y "
    "en la misma rama, el arreglo que queda de ENTRADA-JULIO.md §8: que reconozca como tests los de "
    "un clon `git worktree add --detach` de comparar-con-main (`C:/cm/`), con su test de los dos "
    "sentidos."
)
RESIDUALES = (
    "- Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza "
    "OSError la guardia compara la forma sin prefijos; Grep y `rg` sobre una carpeta que contiene "
    "la raíz se deciden como sobre la raíz, suponiendo, sin medirlo, que respetan su `.gitignore`."
)
LLAVES = (
    "- La guardia no expande las llaves de bash que componen una ruta (`'<raíz>/'{a,b}`) ni mira "
    "las URL `file:///` (urllib, curl), que leen material protegido en `main` y en la rama "
    "(GUARDIA-ALIAS.md §9, b6 y b7): van con la deuda C de la Next Action (rutas compuestas)."
)
antes = len(ps.encode("utf-8"))
lineas[k[0]] = NUEVA_K
lineas[td[0]] = RESIDUALES + "\n" + LLAVES
despues = len("\n".join(lineas).encode("utf-8"))
print(f"antes={antes} despues={despues} margen={25000 - despues}")
print("K:", len(ps.split("\n")[k[0]].encode()), "->", len(NUEVA_K.encode()))
print("TD:", len(ps.split("\n")[td[0]].encode()), "->", len(RESIDUALES.encode()) + 1 + len(LLAVES.encode()))
