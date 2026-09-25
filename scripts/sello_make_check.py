"""El sello de `make check`: el arbol que se probo en verde es el que se commitea.

`make check` llama a `borrar` al empezar y a `sellar` al terminar. Como `make` para en el primer
objetivo que falla, `sellar` solo llega a ejecutarse con todo en verde. El sello es una linea con
el hash de `git write-tree`, el arbol del INDICE, y vive en `git rev-parse --git-path
botsito-sello`, dentro del directorio de git, asi que git nunca lo sigue.

Se sella solo si lo probado es exactamente lo estadiado: sin cambios sin estadiar y sin ficheros
sin seguir fuera de `.gitignore`. Si los hay, avisa, dice cuales y NO sella. `make check` no
falla por eso: el aviso basta, porque el hook de pre-commit rechazara el commit sin sello.

Los hooks `pre-commit` y `pre-merge-commit` (`scripts/git-hooks/`) comparan su propio
`git write-tree` con el sello. Rama `trabajo/blindaje`, 2026-09-25.

Uso:
    uv run python scripts/sello_make_check.py borrar
    uv run python scripts/sello_make_check.py sellar
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

NOMBRE = "botsito-sello"
MAX_LISTADOS = 10


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, encoding="utf-8", check=False
    )


def ruta_del_sello(repo: Path) -> Path | None:
    r = _git(repo, "rev-parse", "--git-path", NOMBRE)
    if r.returncode != 0:
        return None
    return (repo / r.stdout.strip()).resolve()


def borrar(repo: Path) -> str:
    ruta = ruta_del_sello(repo)
    if ruta is not None and ruta.exists():
        ruta.unlink()
    return "SELLO: borrado el anterior; solo se vuelve a escribir si make check termina en verde"


def sin_estadiar(repo: Path) -> list[str]:
    r = _git(repo, "-c", "core.quotepath=false", "diff", "--name-only")
    return [x for x in r.stdout.splitlines() if x]


def sin_seguir(repo: Path) -> list[str]:
    r = _git(repo, "-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard")
    return [x for x in r.stdout.splitlines() if x]


def _lista(titulo: str, rutas: list[str]) -> list[str]:
    lineas = [f"  {titulo} ({len(rutas)}):"]
    lineas += [f"    {x}" for x in rutas[:MAX_LISTADOS]]
    if len(rutas) > MAX_LISTADOS:
        lineas.append(f"    ... y {len(rutas) - MAX_LISTADOS} mas")
    return lineas


def sellar(repo: Path) -> tuple[bool, str]:
    """(sellado, mensaje). No sella si lo probado no es exactamente lo estadiado."""
    ruta = ruta_del_sello(repo)
    if ruta is None:
        return False, "AVISO: no es un repositorio git; no se sella"
    cambios, nuevos = sin_estadiar(repo), sin_seguir(repo)
    if cambios or nuevos:
        lineas = [
            "AVISO: make check esta en verde, pero NO se sella: lo probado no es lo estadiado."
        ]
        if cambios:
            lineas += _lista("cambios sin estadiar", cambios)
        if nuevos:
            lineas += _lista("ficheros sin seguir fuera de .gitignore", nuevos)
        lineas.append(
            "  Estadia lo que vas a commitear (git add <fichero>), quita lo que sobre y repite: "
            "make check > make-check.log 2>&1"
        )
        return False, "\n".join(lineas)
    arbol = _git(repo, "write-tree")
    if arbol.returncode != 0 or not arbol.stdout.strip():
        return False, f"AVISO: git write-tree fallo; no se sella: {arbol.stderr.strip()}"
    hash_arbol = arbol.stdout.strip()
    ruta.write_text(hash_arbol + "\n", encoding="utf-8", newline="\n")
    return True, f"SELLO: make check en verde sobre el arbol {hash_arbol}"


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    repo = Path.cwd()
    if args == ["borrar"]:
        print(borrar(repo))
        return 0
    if args == ["sellar"]:
        _, mensaje = sellar(repo)
        print(mensaje)
        return 0
    print("uso: sello_make_check.py borrar|sellar", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
