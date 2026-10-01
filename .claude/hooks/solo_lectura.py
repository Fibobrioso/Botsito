"""Bash SIN ESCRITURA para el subagente revisor (`.claude/agents/revisor.md`).

Rama `trabajo/guardias-claude` (2026-10-01). El revisor solo tiene Read, Grep, Glob y Bash; este
hook, declarado en su frontmatter, le quita a Bash lo que escribe: redirecciones a fichero, `tee`,
los comandos que crean, mueven o borran, los `git` que cambian el repo o sus referencias, `make`,
`sed -i`, y los `botsito` que escriben. La guardia del proyecto (`guardia.py`) sigue corriendo
ademas para todo, tambien para el revisor.

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
R_SOLO_LECTURA = (
    ".claude/agents/revisor.md: el revisor «No arregla nada» y su Bash es «sin escritura» "
    "(encargo de trabajo/guardias-claude, fase 3)"
)


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
            sub = next((t for t in textos if not t.startswith("-")), "")
            ramas_que_leen = {"--show-current", "--list", "-a", "-r", "-v", "-vv", "--contains"}
            if sub == "branch" and set(textos[1:]) <= ramas_que_leen:
                continue
            if sub == "stash" and textos[1:2] == ["list"]:
                continue
            if sub not in GIT_LEE:
                return f"`git {sub}` cambia el repositorio o sus referencias"
            if sub == "diff" and "--output" in " ".join(textos):
                return "`git diff --output` escribe un fichero"
        en_seco = "--check" in textos or "--dry-run" in textos
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
