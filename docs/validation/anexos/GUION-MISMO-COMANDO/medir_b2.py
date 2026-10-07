"""trabajo/guion-mismo-comando, respuesta del consultor a §1.12: el coste de que «ejecucion» sea
todo lo que no esta en la lista cerrada (a), de negar el fichero que recibe un programa desconocido
(b), y de los nombres de entorno (c), sobre los N primeros comandos reales distintos y los 32 de
`RITUAL` (`tests/unit/test_guardia_claude.py`).

Compara la guardia de la rama ANTES del cambio con la de despues, y con la de despues SIN (b)
(`_ficheros_de_un_programa_desconocido` devuelve nada), para atribuir cada negacion nueva. Solo
llama a `decidir()`; no ejecuta nada. Lista cada negacion nueva con su motivo: un comando que nombra
el material adicional o un backtest se cuenta y no se imprime.

Uso: python medir_b2.py <guardia antes> <guardia despues> <transcripcion.jsonl> <N> <raiz>
"""

from __future__ import annotations

import ast
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

NO_SE_IMPRIME = ("material adicional", "backtest")


def cargar(ruta: str, nombre: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def comandos(transcripcion: Path) -> list[str]:
    salida: list[str] = []
    for linea in transcripcion.open(encoding="utf-8"):
        try:
            d = json.loads(linea)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        for b in d.get("message", {}).get("content", []) or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                salida.append(str(b.get("input", {}).get("command", "")))
    return salida


def ritual(raiz: Path) -> list[str]:
    arbol = ast.parse((raiz / "tests" / "unit" / "test_guardia_claude.py").read_text("utf-8"))
    for n in ast.walk(arbol):
        if isinstance(n, ast.Assign) and any(getattr(x, "id", "") == "RITUAL" for x in n.targets):
            valor = ast.literal_eval(n.value)
            return [str(v) for v in valor]
    raise SystemExit("no hay RITUAL")


def documentados(raiz: Path) -> list[str]:
    """Las lineas de los bloques de codigo de `docs/runbooks/*.md` y `.claude/skills/*/SKILL.md`:
    la practica documentada, mas alla de los comandos de una sesion."""
    salida: list[str] = []
    ficheros = sorted((raiz / "docs" / "runbooks").glob("*.md"))
    ficheros += sorted((raiz / ".claude" / "skills").glob("*/SKILL.md"))
    for f in ficheros:
        dentro = False
        for linea in f.read_text(encoding="utf-8").splitlines():
            if linea.strip().startswith("```"):
                dentro = not dentro
                continue
            if dentro and linea.strip() and not linea.strip().startswith("#"):
                salida.append(linea.strip())
    return list(dict.fromkeys(salida))


def main() -> int:
    de_antes, de_despues, transcripcion, n, raiz_texto = sys.argv[1:6]
    raiz = Path(raiz_texto)
    antes = cargar(de_antes, "guardia_antes")
    despues = cargar(de_despues, "guardia_despues")
    sin_b = cargar(de_despues, "guardia_sin_b")
    sin_b._ficheros_de_un_programa_desconocido = lambda *_a, **_k: ([], False)
    conjuntos = {
        f"los {n} primeros comandos reales distintos": list(
            dict.fromkeys(comandos(Path(transcripcion)))
        )[: int(n)],
        "los 32 de RITUAL": ritual(raiz),
        "las lineas de codigo de los runbooks y las skills": documentados(raiz),
    }
    peor = 0
    for titulo, lista in conjuntos.items():
        nuevos: list[tuple[str, str, bool]] = []
        al_reves = 0
        for c in lista:
            ev = {"tool_name": "Bash", "tool_input": {"command": c}, "cwd": str(raiz)}
            a = antes.decidir(ev, antes.Politica(raiz))
            d = despues.decidir(ev, despues.Politica(raiz))
            s = sin_b.decidir(ev, sin_b.Politica(raiz))
            if a is None and d is not None:
                nuevos.append((c, d.splitlines()[0], s is None))
            elif a is not None and d is None:
                al_reves += 1
                print(f"   !! antes se negaba y ahora pasa: {c[:150]}")
                print(f"       antes: {a.splitlines()[0][:180]}")
        print(f"== {titulo}: {len(lista)}")
        print(f"   antes pasan y ahora se niegan: {len(nuevos)}")
        print(f"     de ellos, solo por (b): {sum(1 for _c, _d, solo_b in nuevos if solo_b)}")
        print(f"   antes se negaban y ahora pasan: {al_reves}")
        for c, motivo, solo_b in nuevos:
            if any(s in c.lower() for s in NO_SE_IMPRIME):
                print("   - [no se imprime: nombra el material adicional o un backtest]")
                continue
            print(f"   - {'(b) ' if solo_b else ''}{c.replace(chr(10), ' \\n ')[:150]}")
            print(f"       {motivo[:180]}")
        peor += al_reves
    return 1 if peor else 0


if __name__ == "__main__":
    raise SystemExit(main())
