"""Bash SIN ESCRITURA para los agentes que solo leen: el revisor (`.claude/agents/revisor.md`) y,
desde `trabajo/entorno-code`, el auditor de encargos (`.claude/agents/auditor-encargo.md`).

Rama `trabajo/guardias-claude` (2026-10-01). Esos agentes solo tienen Read, Grep, Glob y Bash;
este hook, declarado en su frontmatter, le quita a Bash lo que escribe: redirecciones a fichero,
`tee`, los comandos que crean, mueven o borran, los `git` que cambian el repo o sus referencias,
`make`, `sed -i`, y los `botsito` que escriben. Desde `trabajo/entorno-code` (E7, respuesta del
consultor del 2026-10-11, punto 2) tambien los que escriben por un camino que la lista no veia
-`--salida`, `motor arnes`, `motor visor`, `kit hoja`, `casos visto`, `data download` y
`download-ticks`, `evidence contradictions` y `evidence reject`- y `--incluir-holdout`, que no
escribe pero ABRE el holdout. La guardia del proyecto (`guardia.py`) sigue corriendo ademas para
todo, tambien para estos agentes.

Es una lista de lo que escribe, no de lo que lee: lo que no esta aqui pasa. No ve lo que escribe un
guion de Python por dentro; por eso `python` solo pasa con `-c` sin `open(..., "w")` o con un guion
seguido del repositorio. Contrato con Claude Code: 0 deja pasar, 2 bloquea con el motivo por stderr.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import guardia  # noqa: E402  # el tokenizador de bash, el mismo de la guardia

ESCRIBEN = {
    "rm", "rmdir", "mv", "cp", "mkdir", "touch", "tee", "dd", "truncate", "ln", "chmod",
    "chown", "install", "rsync", "scp", "make", "patch", "unzip", "tar", "zip", "7z", "curl",
    "wget", "pip", "npm", "kill",
}  # fmt: skip
GIT_LEE = {
    "status", "log", "diff", "show", "rev-parse", "rev-list", "merge-base", "ls-files",
    "ls-tree", "cat-file", "blame", "grep", "describe", "shortlog", "for-each-ref",
    "name-rev", "check-ignore", "symbolic-ref", "ls-remote", "whatchanged", "count-objects",
    "var", "help", "version",
}  # fmt: skip
BOTSITO_ESCRIBE = re.compile(
    r"--escribir|\b(new|apply|ingerir|build|anclar|inventory|transcribe|extract|propose|accept"
    r"|sellar|desellar)\b"
)
# Escriben siempre, tambien con `--check` (ninguno de estos subcomandos lo tiene): medido en
# `src/botsito/cli.py` en la fase 0 de `trabajo/entorno-code` (ENTORNO-CODE.md §0.a, E7).
BOTSITO_ESCRIBE_SIEMPRE = re.compile(
    r"--salida|\b(arnes|visor|hoja|visto|download|contradictions|reject)\b"
)
BOTSITO_ABRE_HOLDOUT = "--incluir-holdout"
R_SOLO_LECTURA = (
    ".claude/agents/revisor.md y .claude/agents/auditor-encargo.md: «Solo lees: no arreglas, no "
    "editas, no commiteas», y su Bash es «sin escritura» (encargo de trabajo/guardias-claude, "
    "fase 3; E7 de trabajo/entorno-code)"
)


def _subcomando_git(textos: list[str]) -> tuple[str, list[str]]:
    """El subcomando de git y lo que va detras, saltando las opciones globales (`-C <dir>`,
    `-c k=v`, `--git-dir ...`: las de `GIT_CON_VALOR` de la guardia, con su valor).

    Por que (`trabajo/guardia-g1`, respuesta del consultor a la PARADA, punto 8): el primer token
    sin guion era la ruta de `-C` o el `k=v` de `-c`, y se negaba `git -C <clon> rev-parse`, la via
    de comparar-con-main (ACTIVAR-SESION-05-MOTOR.md, revisor). Niega lo mismo que escribe."""
    i = 0
    while i < len(textos) and textos[i].startswith("-"):
        i += 2 if textos[i] in guardia.GIT_CON_VALOR else 1
    if i >= len(textos):
        return "", []
    return textos[i], textos[i + 1 :]


# `git tag` solo lista sin argumentos o con `-l`/`--list`, y sin ninguna opcion que cree, borre,
# firme o mueva (`trabajo/guardia-g1`, punto 8; GUARDIA-CI.md H11).
TAG_QUE_ESCRIBE = re.compile(
    r"-[a-zA-Z]*[dfasmFu][a-zA-Z]*|--(delete|force|annotate|sign|message|file|local-user|edit)\b.*"
)


def _tag_que_lista(resto: list[str]) -> bool:
    if any(TAG_QUE_ESCRIBE.fullmatch(t) for t in resto if t not in {"-l", "--list"}):
        return False
    return not resto or "-l" in resto or "--list" in resto


def motivo(comando: str) -> str | None:
    try:
        lex = guardia.tokenizar(comando)
    except guardia.BloqueoError as exc:
        return str(exc)
    for cmd in guardia.comandos(lex):
        for op, destino in cmd.salidas:
            if op == ">&" or destino.texto.lower() in {"/dev/null", "nul", "&1", "&2", "1", "2"}:
                continue
            return f"redireccion `{op} {destino.texto}`: escribe un fichero"
        argv = guardia._quitar_envoltorios(cmd.argv)
        if not argv:
            continue
        prog = os.path.basename(argv[0].texto).lower().removesuffix(".exe")
        textos = [a.texto for a in argv[1:]]
        if prog in ESCRIBEN:
            return f"`{prog}` escribe"
        if prog in {"sed", "perl"} and any(re.fullmatch(r"-[a-zA-Z]*i\S*", t) for t in textos):
            return f"`{prog} -i` reescribe el fichero"
        if prog == "git":
            sub, resto = _subcomando_git(textos)
            ramas_que_leen = {"--show-current", "--list", "-a", "-r", "-v", "-vv", "--contains"}
            if sub == "branch" and set(resto) <= ramas_que_leen:
                continue
            if sub == "stash" and resto[:1] == ["list"]:
                continue
            if sub == "worktree" and resto[:1] == ["list"]:
                continue
            if sub == "tag" and _tag_que_lista(resto):
                continue
            if sub not in GIT_LEE:
                return f"`git {sub}` cambia el repositorio o sus referencias"
            if sub == "diff" and "--output" in " ".join(textos):
                return "`git diff --output` escribe un fichero"
        en_seco = "--check" in textos or "--dry-run" in textos
        if prog == "botsito" and any(t.startswith(BOTSITO_ABRE_HOLDOUT) for t in textos):
            return f"`{BOTSITO_ABRE_HOLDOUT}` abre el holdout (ADR-0021 §3, ADR-0033)"
        if prog == "botsito" and BOTSITO_ESCRIBE_SIEMPRE.search(" ".join(textos)):
            return "ese subcomando u opcion de `botsito` escribe"
        if prog == "botsito" and BOTSITO_ESCRIBE.search(" ".join(textos)) and not en_seco:
            return "ese subcomando de `botsito` escribe"
        if prog == "uv" and textos[:1] != ["run"]:
            return "`uv` fuera de `uv run` cambia el entorno"
        if prog.startswith("python") or prog == "py":
            codigo = " ".join(textos)
            if re.search(
                r"open\([^)]*['\"][wax]\+?b?['\"]|write_text|write_bytes|unlink|rmtree", codigo
            ):
                return "el codigo de python escribe ficheros"
    return None


def main() -> int:
    for flujo in (sys.stdout, sys.stderr):
        reconfigurar = getattr(flujo, "reconfigure", None)
        if reconfigurar:
            reconfigurar(encoding="utf-8")
    try:
        evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        print("solo_lectura: el evento no es JSON; se bloquea", file=sys.stderr)
        return 2
    entrada = evento.get("tool_input") or {}
    if evento.get("tool_name") != "Bash" or not isinstance(entrada, dict):
        return 0
    razon = motivo(str(entrada.get("command", "")))
    if razon:
        print(f"SOLO LECTURA bloquea: {razon}.\nRegla: {R_SOLO_LECTURA}.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
