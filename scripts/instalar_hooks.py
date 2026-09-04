"""Copia scripts/git-hooks/* a .git/hooks/ (ADR-0003). Portable: no depende de sh, cp ni chmod.

Uso: `uv run python scripts/instalar_hooks.py` (lo llama `make hooks`). Quita `core.hooksPath` si
alguien lo dejo configurado, porque con una ruta relativa git omite en silencio el hook cuando la
rama no contiene el fichero.
"""

from __future__ import annotations

import shutil
import stat
import subprocess
import sys
from pathlib import Path


def main() -> int:
    raiz = Path(__file__).resolve().parents[1]
    origen = raiz / "scripts" / "git-hooks"
    git_dir = subprocess.run(
        ["git", "rev-parse", "--git-dir"],
        cwd=raiz,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )
    if git_dir.returncode != 0:
        print("ERROR: no es un repositorio git")
        return 1
    destino = (raiz / git_dir.stdout.strip()).resolve() / "hooks"
    destino.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "config", "--unset", "core.hooksPath"], cwd=raiz, capture_output=True, check=False
    )
    instalados: list[str] = []
    for hook in sorted(p for p in origen.iterdir() if p.is_file() and p.suffix == ""):
        objetivo = destino / hook.name
        shutil.copyfile(hook, objetivo)
        objetivo.chmod(objetivo.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        instalados.append(hook.name)
    print(f"OK: hooks instalados en {destino}: {', '.join(instalados)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
