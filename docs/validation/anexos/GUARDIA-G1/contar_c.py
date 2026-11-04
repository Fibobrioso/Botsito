"""trabajo/guardia-g1, fase 0 h): cuantos guiones .py de `scripts/` y `tests/` de `main` negaria la
condicion C propuesta (nombra un fragmento sensible Y compone rutas), por fichero y en dos variantes:

- ANCHA: el texto del guion contiene un fragmento de `SENSIBLES` (como hoy `analizar_codigo`) y el
  guion compone rutas en cualquier sitio (`joinpath`, `os.path.join`, `/` entre una expresion y un
  texto, un f-string, `+` con un texto);
- ESTRECHA: el fragmento sensible esta en un texto que forma parte de la COMPOSICION misma (un
  argumento de `joinpath`/`os.path.join`, un lado de `/` o de `+`, una parte de un f-string).

Lee los ficheros de `git show main:<ruta>` (no del disco): son los de `main`. Usa `SENSIBLES` de la
guardia que se le pasa. Uso: python contar_c.py <guardia.py>
"""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path


def cargar(ruta: Path):
    spec = importlib.util.spec_from_file_location("guardia_contar_c", ruta)
    assert spec is not None and spec.loader is not None
    m = importlib.util.module_from_spec(spec)
    sys.modules["guardia_contar_c"] = m
    spec.loader.exec_module(m)
    return m


def textos(nodo: ast.AST) -> list[str]:
    return [n.value for n in ast.walk(nodo) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def composiciones(arbol: ast.AST) -> list[ast.AST]:
    salida: list[ast.AST] = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Call):
            f = n.func
            nombre = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else "")
            if nombre in {"joinpath", "join"} and (
                nombre == "joinpath" or (isinstance(f, ast.Attribute) and ast.unparse(f.value) in {"os.path", "path", "posixpath", "ntpath"})
            ):
                salida.append(n)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Div):
            if textos(n.left) or textos(n.right):
                salida.append(n)
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
            if any(isinstance(x, ast.Constant) and isinstance(x.value, str) for x in (n.left, n.right)):
                salida.append(n)
        elif isinstance(n, ast.JoinedStr) and any(isinstance(v, ast.FormattedValue) for v in n.values):
            salida.append(n)
    return salida


def main() -> int:
    g = cargar(Path(sys.argv[1]).resolve())
    sensibles = tuple(g.SENSIBLES)
    ficheros = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "main", "--", "scripts", "tests"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    ficheros = [f for f in ficheros if f.endswith(".py")]
    ancha: list[str] = []
    estrecha: list[str] = []
    sin_parse = 0
    for f in ficheros:
        codigo = subprocess.run(["git", "show", f"main:{f}"], capture_output=True, text=True, check=True).stdout
        try:
            arbol = ast.parse(codigo)
        except SyntaxError:
            sin_parse += 1
            continue
        comps = composiciones(arbol)
        if not comps:
            continue
        if any(s in codigo.lower() for s in sensibles):
            ancha.append(f)
        if any(any(s in t.lower() for s in sensibles) for c in comps for t in textos(c)):
            estrecha.append(f)
    print(f"guiones .py de scripts/ y tests/ en main: {len(ficheros)} (sin poder parsear: {sin_parse})")
    for nombre, lista in (("ANCHA", ancha), ("ESTRECHA", estrecha)):
        en_scripts = sum(f.startswith("scripts/") for f in lista)
        print(f"{nombre}: {len(lista)} negados ({en_scripts} de scripts/, {len(lista) - en_scripts} de tests/)")
        for f in lista:
            print(f"  {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
