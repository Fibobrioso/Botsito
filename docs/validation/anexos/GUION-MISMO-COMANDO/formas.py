"""trabajo/guion-mismo-comando, respuesta del consultor a §1.21: las FORMAS de git, gh, sort, awk y
sed que aparecen en los comandos reales, en los 32 de `RITUAL` y en las lineas de codigo de los
runbooks y las skills: de ahi salen sus listas cerradas.

Parte cada comando con el tokenizador de la propia guardia (y los `$(...)` y los `bash -c`
anidados), quita los envoltorios y cuenta, por programa: git, sus opciones globales, las claves de
`-c` y el subcomando; gh, sus dos primeras palabras; sort, sus opciones; awk y sed, sus opciones y
su programa. No ejecuta nada.

Uso: python formas.py <guardia> <transcripcion.jsonl> <N> <raiz>
"""

from __future__ import annotations

import ast
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType


def cargar(ruta: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location("guardia_formas", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["guardia_formas"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def reales(transcripcion: Path, n: int) -> list[str]:
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
    return list(dict.fromkeys(salida))[:n]


def ritual(raiz: Path) -> list[str]:
    arbol = ast.parse((raiz / "tests" / "unit" / "test_guardia_claude.py").read_text("utf-8"))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Assign) and any(
            getattr(x, "id", "") == "RITUAL" for x in nodo.targets
        ):
            return [str(v) for v in ast.literal_eval(nodo.value)]
    return []


def documentados(raiz: Path) -> list[str]:
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
    g = cargar(sys.argv[1])
    raiz = Path(sys.argv[4])
    fuentes = {
        "reales": reales(Path(sys.argv[2]), int(sys.argv[3])),
        "ritual": ritual(raiz),
        "runbooks": documentados(raiz),
    }
    cuentas: dict[str, Counter[str]] = {}

    def apunta(clase: str, valor: str) -> None:
        cuentas.setdefault(clase, Counter())[valor] += 1

    def recorrer(texto: str) -> None:
        try:
            lex = g.tokenizar(texto)
        except g.BloqueoError:
            return
        for interior in lex.sustituciones:
            recorrer(interior)
        for cmd in g.comandos(lex):
            argv = g._quitar_envoltorios(cmd.argv)
            if not argv:
                continue
            prog = g._nombre_de_programa(argv[0].texto)
            textos = [a.texto for a in argv[1:]]
            if prog in {"bash", "sh"} and "-c" in textos and textos.index("-c") + 1 < len(textos):
                recorrer(textos[textos.index("-c") + 1])
            if prog == "git":
                i = 0
                while i < len(textos) and textos[i].startswith("-"):
                    apunta("git: opcion global", textos[i])
                    if textos[i] in {"-C", "-c"} and i + 1 < len(textos):
                        if textos[i] == "-c":
                            apunta("git: clave de -c", textos[i + 1].split("=", 1)[0])
                        i += 2
                    else:
                        i += 1
                if i < len(textos):
                    apunta("git: subcomando", textos[i])
            elif prog == "gh":
                palabras = [t for t in textos if not t.startswith("-")][:2]
                apunta("gh: subcomando", " ".join(palabras))
            elif prog == "sort":
                for t in textos:
                    if t.startswith("-"):
                        apunta("sort: opcion", t)
            elif prog in {"awk", "sed"}:
                for t in textos:
                    if t.startswith("-"):
                        apunta(f"{prog}: opcion", t)
                programa = next((t for t in textos if not t.startswith("-")), None)
                if programa is not None:
                    apunta(f"{prog}: programa", programa)

    for nombre, lista in fuentes.items():
        for c in lista:
            recorrer(c)
        print(f"{nombre}: {len(lista)} comandos")
    for clase, cuenta in sorted(cuentas.items()):
        print(f"\n== {clase}")
        for valor, n in sorted(cuenta.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{n:5}  {valor!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
