"""Fase 0 a) de trabajo/respuestas-ftmo: stable/F37a-<nombre> frente a cada lector del formato del tag.

Se ejecuta desde la raiz del repo real (uv run python <este fichero> <clon>). El clon es un
`git clone` desechable fuera del repo: el tag de prueba se crea ALLI, nunca en el repo real (un
worktree compartiria los refs)."""

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path.cwd()
CLON = Path(sys.argv[1])
TAG = "stable/F37a-respuestas-ftmo"


def git(repo: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_COMMITTER_DATE="2030-01-01T00:00:00", GIT_AUTHOR_DATE="2030-01-01T00:00:00")
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True, env=env
    ).stdout.strip()


print("== 1. guardia (.claude/hooks/guardia.py, decidir, sobre el repo real)")
spec = importlib.util.spec_from_file_location("guardia_claude", RAIZ / ".claude/hooks/guardia.py")
g = importlib.util.module_from_spec(spec)
sys.modules["guardia_claude"] = g
spec.loader.exec_module(g)
politica = g.Politica(RAIZ)
pasan = [
    f'git tag -a {TAG} -m "resumen"',
    f'git rev-parse --short "{TAG}^{{commit}}"',
    f"git push --atomic origin main {TAG}",
    f"git ls-remote --tags origin {TAG}",
    f'BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): trabajo/x, cerrada en main ({TAG})"',
    'git tag -l "stable/*" --sort=-creatordate',
]
bloquean = [
    f"git tag -d {TAG}",
    f"git tag -f {TAG} HEAD",
    f"git push origin --delete {TAG}",
    f"git push origin :refs/tags/{TAG}",
]
for c in pasan + bloquean:
    motivo = g.decidir({"tool_name": "Bash", "tool_input": {"command": c}, "cwd": str(RAIZ)}, politica)
    esperado = c in pasan
    print(f"  {'pasa' if motivo is None else 'BLOQUEA'} (esperado {'pasa' if esperado else 'BLOQUEA'}): {c}")
    assert (motivo is None) == esperado

print("== 2. state check, regla 4 (cli.py:166, Completed Features)")
for linea in (f"- F37a-respuestas-ftmo", "- F36z-ventana-no-citable", "- F37 algo (control)"):
    mm = re.match(r"-\s*(F\d{2})\b", linea)
    print(f"  {linea!r}: {'casa ' + mm.group(1) if mm else 'no casa'}")

print("== 3. knowledge validate: ids_de_funcionalidad (MASTER_PLAN, no tags)")
from botsito.validation.knowledge import ids_de_funcionalidad  # noqa: E402

ids = ids_de_funcionalidad(RAIZ)
print(f"  {len(ids)} ids; F36 en ellos: {'F36' in ids}; F37 en ellos: {'F37' in ids}")

print("== 4. clon desechable: tag de prueba y state check")
print(f"  HEAD del clon: {git(CLON, 'rev-parse', '--short', 'HEAD')}")
git(CLON, "tag", "-a", TAG, "f8b291c", "-m", "prueba de la fase 0, solo en el clon")
print("  git tag -l 'stable/*' --sort=-creatordate (3 primeros):")
for t in git(CLON, "tag", "-l", "stable/*", "--sort=-creatordate").splitlines()[:3]:
    print(f"    {t}")
from botsito.cli import _ultimo_tag_estable, state_check  # noqa: E402

print(f"  _ultimo_tag_estable(clon): {_ultimo_tag_estable(CLON)}")
codigo = state_check(CLON)
print(f"  state_check(clon) = {codigo}")
assert codigo == 0
print("== todo como se esperaba")
