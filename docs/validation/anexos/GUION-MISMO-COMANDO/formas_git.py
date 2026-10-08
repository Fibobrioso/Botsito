"""trabajo/guion-mismo-comando, respuesta del consultor a §1.27: las formas de `git config`, `git
remote`, `git merge`, los bucles `for` y los builtins que fijan variables, en los 572 comandos
reales, los 32 de `RITUAL` y las lineas de codigo de los runbooks y las skills. De ahi salen las
listas cerradas de `config`/`remote`/`merge -s`, y se comprueba que builtin fija que nombre.

Usa el tokenizador de la propia guardia; no ejecuta nada.

Uso: python formas_git.py <guardia> <transcripcion.jsonl> <N> <raiz>
"""

from __future__ import annotations

import ast
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

BUILTINS_QUE_FIJAN = {
    "read", "declare", "typeset", "local", "readonly", "mapfile", "readarray", "getopts", "let",
    "printf", "export", "set", "eval", "source", "unset", "shift", "trap",
}  # fmt: skip


def cargar(ruta: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location("g_formas_git", ruta)
    assert spec is not None and spec.loader is not None
    m = importlib.util.module_from_spec(spec)
    sys.modules["g_formas_git"] = m
    spec.loader.exec_module(m)
    return m


def reales(tr: Path, n: int) -> list[str]:
    out: list[str] = []
    for linea in tr.open(encoding="utf-8"):
        try:
            d = json.loads(linea)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        for b in d.get("message", {}).get("content", []) or []:
            if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") == "Bash":
                out.append(str(b.get("input", {}).get("command", "")))
    return list(dict.fromkeys(out))[:n]


def ritual(raiz: Path) -> list[str]:
    arbol = ast.parse((raiz / "tests" / "unit" / "test_guardia_claude.py").read_text("utf-8"))
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.Assign) and any(
            getattr(x, "id", "") == "RITUAL" for x in nodo.targets
        ):
            return [str(v) for v in ast.literal_eval(nodo.value)]
    return []


def documentados(raiz: Path) -> list[str]:
    out: list[str] = []
    fs = sorted((raiz / "docs" / "runbooks").glob("*.md"))
    fs += sorted((raiz / ".claude" / "skills").glob("*/SKILL.md"))
    for f in fs:
        dentro = False
        for linea in f.read_text(encoding="utf-8").splitlines():
            if linea.strip().startswith("```"):
                dentro = not dentro
                continue
            if dentro and linea.strip() and not linea.strip().startswith("#"):
                out.append(linea.strip())
    return list(dict.fromkeys(out))


def main() -> int:
    g = cargar(sys.argv[1])
    raiz = Path(sys.argv[4])
    fuentes = reales(Path(sys.argv[2]), int(sys.argv[3])) + ritual(raiz) + documentados(raiz)
    c: dict[str, Counter[str]] = {}

    def apunta(k: str, v: str) -> None:
        c.setdefault(k, Counter())[v] += 1

    def recorrer(texto: str) -> None:
        try:
            lex = g.tokenizar(texto)
        except g.BloqueoError:
            return
        for interior in lex.sustituciones:
            recorrer(interior)
        palabras = [p.texto for p in lex.palabras]
        for i, p in enumerate(palabras):
            if p == "for" and i + 1 < len(palabras):
                apunta("for (variable)", palabras[i + 1])
        for cmd in g.comandos(lex):
            argv = g._quitar_envoltorios(cmd.argv)
            if not argv:
                continue
            prog = g._nombre_de_programa(argv[0].texto)
            textos = [a.texto for a in argv[1:]]
            if prog in {"bash", "sh"} and "-c" in textos and textos.index("-c") + 1 < len(textos):
                recorrer(textos[textos.index("-c") + 1])
            if prog == "git":
                sub = next((t for t in textos if not t.startswith("-")), "")
                if sub in {"config", "remote", "merge"}:
                    apunta(f"git {sub}", " ".join(textos[:4]))
            if prog in BUILTINS_QUE_FIJAN:
                apunta("builtin que fija", prog)

    for texto in fuentes:
        recorrer(texto)
    print(f"comandos: {len(fuentes)}")
    for clase, cuenta in sorted(c.items()):
        print(f"\n== {clase}")
        for v, n in sorted(cuenta.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"{n:5}  {v!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
