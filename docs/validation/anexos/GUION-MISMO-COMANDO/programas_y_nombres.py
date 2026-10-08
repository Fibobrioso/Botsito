"""trabajo/guion-mismo-comando, respuesta del consultor a §1.12: de que programas y de que nombres de
entorno salen las dos listas cerradas.

Lee los N primeros comandos de Bash DISTINTOS de la transcripcion de una sesion (N = 503, los que
midio el consultor), los parte con el tokenizador de la propia guardia y cuenta: (1) el programa de
cada comando simple, tras quitar los envoltorios; (2) los nombres de las asignaciones, por forma (la
que precede a un comando, la suelta, `export`, `env`). No ejecuta nada.

Uso: python programas_y_nombres.py <guardia> <transcripcion.jsonl> <N>
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from collections import Counter
from pathlib import Path


def cargar(ruta: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location("guardia_listas", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["guardia_listas"] = modulo
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


def main() -> int:
    g = cargar(sys.argv[1])
    distintos = list(dict.fromkeys(comandos(Path(sys.argv[2]))))[: int(sys.argv[3])]
    programas: Counter[str] = Counter()
    nombres: dict[str, Counter[str]] = {}
    no_partidos = 0

    def nombre(forma: str, n: str) -> None:
        nombres.setdefault(forma, Counter())[n] += 1

    def recorrer(texto: str) -> None:
        nonlocal no_partidos
        try:
            lex = g.tokenizar(texto)
        except g.BloqueoError:
            no_partidos += 1
            return
        for interior in lex.sustituciones:
            recorrer(interior)
        for cmd in g.comandos(lex):
            forma = "precede a un comando" if cmd.argv else "suelta"
            for n in cmd.asignaciones:
                nombre(forma, n)
            argv = cmd.argv
            while argv and g._nombre_de_programa(argv[0].texto) == "env":
                argv = argv[1:]
                while argv and (argv[0].texto.startswith("-") or "=" in argv[0].texto):
                    if "=" in argv[0].texto and not argv[0].texto.startswith("-"):
                        nombre("env", argv[0].texto.split("=", 1)[0])
                    argv = argv[1:]
            argv = g._quitar_envoltorios(argv)
            if not argv:
                continue
            prog = g._nombre_de_programa(argv[0].texto) if "\x00" not in argv[0].texto else "$..."
            if prog in {"export", "declare", "typeset", "readonly", "local"}:
                for a in argv[1:]:
                    if not a.texto.startswith("-"):
                        nombre(prog, a.texto.split("=", 1)[0])
            if g._es_fichero_programa(argv[0].texto, g.Contexto(g.Politica(Path(".")), ".")):
                prog = "(un fichero como programa)"
            programas[prog] += 1

    for c in distintos:
        recorrer(c)
    print(f"comandos distintos: {len(distintos)}; sin partir (tokenizador): {no_partidos}")
    print("\n== Programas (nombre, veces)")
    for p, n in sorted(programas.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:5}  {p}")
    print("\n== Nombres de las asignaciones, por forma")
    for forma, cuenta in sorted(nombres.items()):
        print(f"-- {forma}")
        for n, k in sorted(cuenta.items(), key=lambda kv: (-kv[1], kv[0])):
            exportada = " (exportada en el entorno de la guardia)" if n in os.environ else ""
            print(f"{k:5}  {n}{exportada}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
