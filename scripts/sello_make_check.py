"""El sello de `make check`: el arbol que se probo en verde es el que se commitea.

`make check` llama a `borrar` al empezar y a `sellar` al terminar. Como `make` para en el primer
objetivo que falla, `sellar` solo llega a ejecutarse con todo en verde. El sello es una linea con
el hash de `git write-tree`, el arbol del INDICE, y vive en `git rev-parse --git-path
botsito-sello`, dentro del directorio de git, asi que git nunca lo sigue.

Se sella solo si lo probado es exactamente lo estadiado: sin cambios sin estadiar y sin ficheros
sin seguir fuera de `.gitignore`. Si los hay, avisa, dice cuales y NO sella. `make check` no
falla por eso: el aviso basta, porque el hook de pre-commit rechazara el commit sin sello.

LA GUARDIA (rama `trabajo/blindar-make-check`, 2026-09-28). `borrar` toma ademas una HUELLA del
arbol de trabajo y la guarda junto al sello (`botsito-huella`): el commit de HEAD y, por cada
fichero seguido, su entrada del indice (modo y blob) y el `mtime` y el tamano del fichero en disco;
por cada fichero sin seguir fuera de `.gitignore`, su `mtime`, su tamano y el hash de su contenido.
`sellar` toma la misma huella al terminar y, si difiere, FALLA (codigo 1, `make check` sale en
rojo), nombra los ficheros que cambiaron y no sella. Asi un cambio hecho DURANTE la comprobacion
no se puede sellar, aunque se estadie, aunque se deshaga antes del final o aunque se haga un
commit a mitad. Lo que `make check` escribe de forma legitima (el log, las caches, los artefactos
de los tests) esta en `.gitignore` y no entra en la huella: la exclusion ES `.gitignore`, sin lista
aparte (medido en `docs/validation/BLINDAR-MAKE-CHECK.md`). Lo que no ve: un fichero sin seguir
que se crea y se borra entre las dos huellas, y lo que se escriba en un fichero ignorado. Sale del
incidente del instalador sobre copias del 2026-09-28 (el mismo informe).

Los hooks `pre-commit` y `pre-merge-commit` (`scripts/git-hooks/`) comparan su propio
`git write-tree` con el sello. Rama `trabajo/blindaje`, 2026-09-25.

Uso:
    uv run python scripts/sello_make_check.py borrar
    uv run python scripts/sello_make_check.py sellar
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

NOMBRE = "botsito-sello"
NOMBRE_HUELLA = "botsito-huella"
MAX_LISTADOS = 10
CLAVE_HEAD = ":HEAD"
ERROR_GUARDIA = "ERROR: el arbol de trabajo cambio mientras corria make check"


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, encoding="utf-8", check=False
    )


def _ruta_git(repo: Path, nombre: str) -> Path | None:
    r = _git(repo, "rev-parse", "--git-path", nombre)
    if r.returncode != 0:
        return None
    return (repo / r.stdout.strip()).resolve()


def ruta_del_sello(repo: Path) -> Path | None:
    return _ruta_git(repo, NOMBRE)


def ruta_de_la_huella(repo: Path) -> Path | None:
    return _ruta_git(repo, NOMBRE_HUELLA)


def _disco(ruta: Path) -> str:
    try:
        st = ruta.stat()
    except OSError:
        return "ausente"
    return f"{st.st_mtime_ns}:{st.st_size}"


def _contenido(ruta: Path) -> str:
    h = hashlib.sha256()
    try:
        with ruta.open("rb") as f:
            for trozo in iter(lambda: f.read(1 << 20), b""):
                h.update(trozo)
    except OSError:
        return "ilegible"
    return h.hexdigest()


def huella(repo: Path) -> dict[str, str]:
    """Ruta -> estado, mas el commit de HEAD. Lectura pura: no escribe nada en el arbol."""
    salida: dict[str, str] = {}
    head = _git(repo, "rev-parse", "-q", "--verify", "HEAD")
    salida[CLAVE_HEAD] = head.stdout.strip() if head.returncode == 0 else "sin HEAD"
    indice = _git(repo, "ls-files", "-s", "-z")
    for registro in indice.stdout.split("\0"):
        if not registro:
            continue
        cabecera, ruta = registro.split("\t", 1)
        modo, blob, etapa = cabecera.split()
        salida[ruta] = f"indice {modo} {blob} {etapa} · disco {_disco(repo / ruta)}"
    otros = _git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    for ruta in otros.stdout.split("\0"):
        if ruta:
            p = repo / ruta
            salida[ruta] = f"sin seguir · disco {_disco(p)} · {_contenido(p)}"
    return salida


def diferencias(antes: dict[str, str], despues: dict[str, str]) -> list[str]:
    """Las rutas cuyo estado cambio, aparecio o desaparecio, con HEAD nombrado aparte."""
    claves = sorted(set(antes) | set(despues))
    cambiadas = [k for k in claves if antes.get(k) != despues.get(k)]
    return [
        "HEAD (se hizo un commit o se cambio de rama)" if k == CLAVE_HEAD else k for k in cambiadas
    ]


def borrar(repo: Path) -> str:
    ruta = ruta_del_sello(repo)
    if ruta is not None and ruta.exists():
        ruta.unlink()
    mensaje = "SELLO: borrado el anterior; solo se vuelve a escribir si make check termina en verde"
    ruta_huella = ruta_de_la_huella(repo)
    if ruta_huella is None:
        return mensaje
    foto = huella(repo)
    ruta_huella.write_text(json.dumps(foto, sort_keys=True), encoding="utf-8", newline="\n")
    return (
        f"{mensaje}\nHUELLA: tomada sobre {len(foto) - 1} ficheros; si cambia alguno antes de "
        "sellar, make check falla y no sella"
    )


def guardia(repo: Path) -> list[str] | None:
    """Lo que cambio desde `borrar`, o None si no hay huella (sellar fuera de make check).
    La huella se consume: se lee una vez y se borra."""
    ruta = ruta_de_la_huella(repo)
    if ruta is None or not ruta.exists():
        return None
    antes = json.loads(ruta.read_text(encoding="utf-8"))
    ruta.unlink()
    return diferencias(antes, huella(repo))


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
    """(sellado, mensaje). No sella si el arbol cambio durante la comprobacion (el mensaje
    empieza por ERROR_GUARDIA) ni si lo probado no es exactamente lo estadiado."""
    ruta = ruta_del_sello(repo)
    if ruta is None:
        return False, "AVISO: no es un repositorio git; no se sella"
    cambiadas = guardia(repo)
    if cambiadas:
        lineas = [f"{ERROR_GUARDIA}; NO se sella: lo probado no es lo que hay ahora."]
        lineas += _lista("cambiaron entre el principio y el final", cambiadas)
        lineas.append(
            "  Mientras corre make check no se escribe nada en el repositorio (CLAUDE.md). "
            "Revisa esos ficheros y repite: make check > make-check.log 2>&1"
        )
        return False, "\n".join(lineas)
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
        return 1 if mensaje.startswith(ERROR_GUARDIA) else 0
    print("uso: sello_make_check.py borrar|sellar", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
