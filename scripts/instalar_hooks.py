"""Copia scripts/git-hooks/* al directorio de hooks del repositorio (ADR-0003).

Portable: no depende de sh, cp ni chmod. Uso: `uv run python scripts/instalar_hooks.py` (lo
llama `make hooks`).

- El destino es `git rev-parse --git-path hooks`, no `--git-dir/hooks`: en un worktree el
  primero es el directorio comun que git lee de verdad y el segundo no.
- Quita `core.hooksPath` local (con una ruta relativa git omite en silencio el hook cuando la rama
  no contiene el fichero) y ABORTA si queda configurado en el ambito global o de sistema, porque
  entonces git ignoraria lo que aqui se instala.
- Un hook ajeno previo se conserva como `<nombre>.bak` para que nadie pierda trabajo.
"""

from __future__ import annotations

import shutil
import stat
import subprocess
import sys
from pathlib import Path


def _git(raiz: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=raiz, capture_output=True, encoding="utf-8", check=False
    )


def main() -> int:
    raiz = Path(__file__).resolve().parents[1]
    origen = raiz / "scripts" / "git-hooks"
    try:
        hooks_path = _git(raiz, "rev-parse", "--git-path", "hooks")
    except FileNotFoundError:
        print("ERROR: git no esta en PATH")
        return 1
    if hooks_path.returncode != 0:
        print("ERROR: no es un repositorio git")
        return 1
    destino = (raiz / hooks_path.stdout.strip()).resolve()
    destino.mkdir(parents=True, exist_ok=True)
    _git(raiz, "config", "--unset", "core.hooksPath")
    restante = _git(raiz, "config", "--show-origin", "core.hooksPath")
    if restante.returncode == 0 and restante.stdout.strip():
        print(
            "ERROR: core.hooksPath sigue configurado fuera del repositorio y git ignoraria "
            f"estos hooks: {restante.stdout.strip()}\n"
            "       Quitalo (git config --global --unset core.hooksPath) y repite make hooks."
        )
        return 1
    instalados: list[str] = []
    for hook in sorted(p for p in origen.iterdir() if p.is_file() and p.suffix == ""):
        objetivo = destino / hook.name
        if objetivo.exists() and objetivo.read_bytes() != hook.read_bytes():
            copia = objetivo.with_name(objetivo.name + ".bak")
            shutil.copyfile(objetivo, copia)
            print(f"AVISO: {objetivo.name} previo distinto conservado en {copia.name}")
        shutil.copyfile(hook, objetivo)
        objetivo.chmod(objetivo.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        instalados.append(hook.name)
    print(f"OK: hooks instalados en {destino}: {', '.join(instalados)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
