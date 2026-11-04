"""trabajo/guardia-g1, fase 2 (respuesta del consultor a la PARADA, punto 10): el coste REAL de C.

Para cada guion `.py` de `scripts/` y `tests/` de `main`, que composiciones de una ruta tiene, si la
guardia de la rama las CALCULA, y si la condicion C (`_compone_ruta_sensible`) lo negaria cambiado en
una rama (es decir, analizado como codigo sin revisar en su propia ruta). Y, aparte, si `main` no
pasaria igual por el analisis entero de la rama (`analizar_codigo`, que incluye B).

Lee los ficheros de `main` con `git cat-file --batch` (no del disco) y llama a la guardia en memoria;
no ejecuta ninguno. En la nube no hay `corpus/` ni `data/`: lo que dependa de que una carpeta
calculada exista en disco sale aqui mas barato que en el portatil de Aleks (GUARDIA-G1.md §5).

Uso: python costo_c.py (desde la raiz del repo; carga `.claude/hooks/guardia.py`)
"""

from __future__ import annotations

import ast
import importlib.util
import subprocess
import sys
from pathlib import Path


# La guardia de la rama por su ruta, con la forma de la excepcion cerrada (respuesta del consultor a
# la PARADA 2 de `trabajo/guardia-g1`, punto 1): antes se cargaba por una ruta de `sys.argv`, que la
# guardia de la fase 2 niega por no poder calcularla.
RAIZ = Path(__file__).resolve().parents[4]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"


def cargar():
    spec = importlib.util.spec_from_file_location("guardia_costo_c", GUARDIA)
    assert spec is not None and spec.loader is not None
    m = importlib.util.module_from_spec(spec)
    sys.modules["guardia_costo_c"] = m
    spec.loader.exec_module(m)
    return m


def blobs(nombres: list[str]) -> dict[str, str]:
    """El texto de cada fichero en `main`, de una sola vez."""
    entrada = "".join(f"main:{n}\n" for n in nombres)
    salida = subprocess.run(["git", "cat-file", "--batch"], input=entrada.encode(), capture_output=True, check=True).stdout
    textos: dict[str, str] = {}
    i = 0
    for n in nombres:
        cabecera_fin = salida.index(b"\n", i)
        tam = int(salida[i:cabecera_fin].split()[2])
        inicio = cabecera_fin + 1
        textos[n] = salida[inicio : inicio + tam].decode("utf-8", errors="replace")
        i = inicio + tam + 1
    return textos


def main() -> int:
    g = cargar()
    raiz = Path.cwd()
    lista = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "main", "--", "scripts", "tests"],
        capture_output=True, text=True, check=True,
    ).stdout.split()
    lista = [f for f in lista if f.endswith(".py")]
    textos = blobs(lista)
    politica = g.Politica(raiz)
    negados_c: list[tuple[str, str]] = []
    negados_todo: list[tuple[str, str]] = []
    detalle: list[str] = []
    for f in lista:
        texto = textos[f]
        try:
            arbol = ast.parse(texto)
        except SyntaxError:
            continue
        guion = str(raiz / f)
        asign = g._asignaciones_unicas(arbol)
        padres = {id(h): p for p in ast.walk(arbol) for h in ast.iter_child_nodes(p)}
        comps = [
            n for n in ast.walk(arbol)
            if g._es_composicion(n) and not g._es_composicion(padres.get(id(n), ast.Pass()))
        ]
        calculadas = sum(g._DESCONOCIDO not in g._calcular(n, asign, guion) for n in comps)
        ctx = g.Contexto(politica, str(raiz))
        recorre = g.CODIGO_QUE_RECORRE.search(texto) is not None
        try:
            g._compone_ruta_sensible(arbol, ctx, recorre, guion)
            c = "PASA"
        except g.BloqueoError as exc:
            c = "NIEGA: " + str(exc).splitlines()[0][:150]
            negados_c.append((f, c))
        try:
            g.analizar_codigo(texto, g.Contexto(politica, str(raiz)), True, guion)
            todo = "PASA"
        except g.BloqueoError as exc:
            todo = "NIEGA: " + str(exc).splitlines()[0][:150]
            negados_todo.append((f, todo))
        if f.startswith("scripts/"):
            detalle.append(f"{f}: {len(comps)} composiciones, {calculadas} calculadas; C {c}; entero {todo}")
    print(f"guiones .py de scripts/ y tests/ en main: {len(lista)}")
    print("\n# scripts/, uno por uno (C sola, y el analisis entero de la rama)")
    print("\n".join(detalle))
    for titulo, negados in (("C sola", negados_c), ("el analisis entero (B y C)", negados_todo)):
        en_scripts = sum(f.startswith("scripts/") for f, _ in negados)
        print(f"\n# {titulo}: {len(negados)} negados ({en_scripts} de scripts/, {len(negados) - en_scripts} de tests/)")
        for f, m in negados:
            print(f"  {f}: {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
