"""La puerta automatica del commit (rama `trabajo/blindaje`): `make check` en verde sella el arbol
estadiado y los hooks `pre-commit` y `pre-merge-commit` rechazan un arbol sin ese sello.

Todo sobre repos temporales con los hooks versionados copiados: nunca se toca el repo real."""

from __future__ import annotations

import importlib.util
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
HOOKS = RAIZ / "scripts" / "git-hooks"
SCRIPT = RAIZ / "scripts" / "sello_make_check.py"
INICIO = "# --- sello de make check (inicio)"
FIN = "# --- sello de make check (fin) ---"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "sello_make_check"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _entorno() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.pop("BOTSITO_ALLOW_MAIN", None)
    return env


def git(
    repo: Path, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=False,
        env=env or _entorno(),
    )


@pytest.fixture
def repo(tmp_path: Path, m: ModuleType) -> Path:
    """Un repo en una rama de trabajo, con los hooks versionados y un primer commit sellado."""
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "trabajo/prueba")
    for clave, valor in (
        ("user.email", "t@t"),
        ("user.name", "t"),
        ("core.autocrlf", "false"),
        ("commit.gpgsign", "false"),
    ):
        git(r, "config", clave, valor)
    destino = Path(git(r, "rev-parse", "--git-path", "hooks").stdout.strip())
    destino = destino if destino.is_absolute() else r / destino
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ("pre-commit", "pre-merge-commit"):
        objetivo = destino / nombre
        shutil.copyfile(HOOKS / nombre, objetivo)
        objetivo.chmod(objetivo.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    (r / ".gitignore").write_text("ignorado.txt\n", encoding="utf-8")
    (r / "a.txt").write_text("a\n", encoding="utf-8")
    git(r, "add", ".gitignore", "a.txt")
    assert m.sellar(r)[0]
    c = git(r, "commit", "-q", "-m", "inicio")
    assert c.returncode == 0, c.stderr
    return r


def _sello(r: Path) -> str | None:
    ruta = Path(git(r, "rev-parse", "--git-path", "botsito-sello").stdout.strip())
    ruta = ruta if ruta.is_absolute() else r / ruta
    return ruta.read_text(encoding="utf-8").strip() if ruta.exists() else None


def _escribir(r: Path, nombre: str, texto: str) -> None:
    (r / nombre).write_text(texto, encoding="utf-8")


# ------------------------------------------------------------------------ lo que pide el consultor


def test_sello_correcto_commit_permitido(repo: Path, m: ModuleType) -> None:
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    sellado, mensaje = m.sellar(repo)
    assert sellado, mensaje
    assert _sello(repo) == git(repo, "write-tree").stdout.strip()
    c = git(repo, "commit", "-q", "-m", "b")
    assert c.returncode == 0, c.stderr


def test_arbol_cambiado_despues_del_sello_rechazado(repo: Path, m: ModuleType) -> None:
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    assert m.sellar(repo)[0]
    _escribir(repo, "c.txt", "c\n")
    git(repo, "add", "c.txt")
    c = git(repo, "commit", "-q", "-m", "b y c")
    assert c.returncode != 0
    assert "pre-commit: rechazado" in c.stderr
    assert "make check > make-check.log 2>&1" in c.stderr
    assert "otro arbol" in c.stderr
    assert git(repo, "rev-list", "--count", "HEAD").stdout.strip() == "1"


def test_sin_sello_rechazado_y_dice_que_hacer(repo: Path, m: ModuleType) -> None:
    m.borrar(repo)
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    c = git(repo, "commit", "-q", "-m", "b")
    assert c.returncode != 0
    assert "No hay sello" in c.stderr
    assert "--no-verify esta prohibido" in c.stderr


def _makefile_de_prueba(tmp_path: Path, falla: bool) -> Path:
    """La linea `check:` REAL del Makefile, con los objetivos que no son del sello simulados."""
    real = (RAIZ / "Makefile").read_text(encoding="utf-8")
    linea = next(x for x in real.splitlines() if x.startswith("check:"))
    objetivos = linea.split(":", 1)[1].split()
    otros = [o for o in objetivos if o not in {"desellar", "sellar"}]
    py = Path(sys.executable).as_posix()
    script = SCRIPT.as_posix()
    cuerpo = [
        "SHELL := sh",
        ".NOTPARALLEL:",
        linea,
        "desellar:",
        f'\t"{py}" "{script}" borrar',
        "sellar:",
        f'\t"{py}" "{script}" sellar',
    ]
    for o in otros:
        cuerpo += [f"{o}:", "\t@exit 1" if (falla and o == "test") else "\t@echo ok"]
    fichero = tmp_path / "Makefile.prueba"
    fichero.write_text("\n".join(cuerpo) + "\n", encoding="utf-8", newline="\n")
    return fichero


def _make(repo: Path, makefile: Path) -> subprocess.CompletedProcess[str]:
    if shutil.which("make") is None or shutil.which("sh") is None:
        pytest.skip("sin make o sin sh en PATH")
    return subprocess.run(
        ["make", "-f", str(makefile), "check"],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=False,
        env=_entorno(),
    )


def test_make_check_en_rojo_no_sella_y_borra_el_sello_viejo(
    repo: Path, tmp_path: Path, m: ModuleType
) -> None:
    assert m.sellar(repo)[0]  # un sello viejo del mismo arbol
    rojo = _make(repo, _makefile_de_prueba(tmp_path, falla=True))
    assert rojo.returncode != 0
    assert _sello(repo) is None, "make check en rojo dejo un sello"
    verde = _make(repo, _makefile_de_prueba(tmp_path, falla=False))
    assert verde.returncode == 0, verde.stdout + verde.stderr
    assert _sello(repo) == git(repo, "write-tree").stdout.strip()


def test_el_makefile_real_desella_primero_sella_al_final_y_sin_paralelo() -> None:
    real = (RAIZ / "Makefile").read_text(encoding="utf-8")
    objetivos = (
        next(x for x in real.splitlines() if x.startswith("check:")).split(":", 1)[1].split()
    )
    assert objetivos[0] == "desellar" and objetivos[-1] == "sellar"
    assert objetivos.count("sellar") == 1 and objetivos.count("desellar") == 1
    assert re.search(r"^\.NOTPARALLEL:", real, re.M)
    assert "sello_make_check.py borrar" in real and "sello_make_check.py sellar" in real


def test_cambios_sin_estadiar_no_sella(repo: Path, m: ModuleType) -> None:
    m.borrar(repo)
    _escribir(repo, "a.txt", "a cambiado\n")
    sellado, mensaje = m.sellar(repo)
    assert not sellado
    assert "cambios sin estadiar" in mensaje and "a.txt" in mensaje
    assert _sello(repo) is None


def test_fichero_sin_seguir_no_sella_pero_uno_ignorado_si(repo: Path, m: ModuleType) -> None:
    m.borrar(repo)
    _escribir(repo, "nuevo.txt", "n\n")
    sellado, mensaje = m.sellar(repo)
    assert not sellado and "nuevo.txt" in mensaje
    (repo / "nuevo.txt").unlink()
    _escribir(repo, "ignorado.txt", "x\n")
    assert m.sellar(repo)[0]


# ------------------------------------------------------------------------ merge, amend y el resto


def test_amend_necesita_el_sello_del_arbol_enmendado(repo: Path, m: ModuleType) -> None:
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    assert m.sellar(repo)[0]
    assert git(repo, "commit", "-q", "-m", "b").returncode == 0
    _escribir(repo, "c.txt", "c\n")
    git(repo, "add", "c.txt")
    rechazado = git(repo, "commit", "-q", "--amend", "-m", "b y c")
    assert rechazado.returncode != 0 and "pre-commit: rechazado" in rechazado.stderr
    assert m.sellar(repo)[0]
    assert git(repo, "commit", "-q", "--amend", "-m", "b y c").returncode == 0


def test_commit_a_usa_el_arbol_que_se_escribe_de_verdad(repo: Path, m: ModuleType) -> None:
    # `git commit -a` estadia en un indice temporal: el sello del indice de antes no vale
    assert m.sellar(repo)[0]
    _escribir(repo, "a.txt", "a cambiado\n")
    c = git(repo, "commit", "-q", "-a", "-m", "a")
    assert c.returncode != 0 and "pre-commit: rechazado" in c.stderr


def _rama_con_un_commit(repo: Path, m: ModuleType) -> str:
    git(repo, "checkout", "-q", "-b", "trabajo/otra")
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    assert m.sellar(repo)[0]
    assert git(repo, "commit", "-q", "-m", "b").returncode == 0
    return git(repo, "rev-parse", "HEAD^{tree}").stdout.strip()


def test_merge_no_ff_pasa_con_el_sello_del_arbol_fusionado(repo: Path, m: ModuleType) -> None:
    arbol_rama = _rama_con_un_commit(repo, m)
    git(repo, "checkout", "-q", "trabajo/prueba")
    c = git(repo, "merge", "--no-ff", "trabajo/otra", "-m", "merge")
    assert c.returncode == 0, c.stderr
    assert git(repo, "rev-parse", "HEAD^{tree}").stdout.strip() == arbol_rama


def test_merge_no_ff_sin_sello_rechazado_y_queda_a_medias(repo: Path, m: ModuleType) -> None:
    _rama_con_un_commit(repo, m)
    git(repo, "checkout", "-q", "trabajo/prueba")
    m.borrar(repo)
    c = git(repo, "merge", "--no-ff", "trabajo/otra", "-m", "merge")
    assert c.returncode != 0
    assert "pre-merge-commit: rechazado" in c.stderr and "git merge --abort" in c.stderr
    assert git(repo, "rev-parse", "-q", "--verify", "MERGE_HEAD").returncode == 0
    # la salida documentada: sellar el arbol fusionado y cerrar con git commit (pasa por pre-commit)
    assert m.sellar(repo)[0]
    assert git(repo, "commit", "-q", "--no-edit").returncode == 0


def test_main_sigue_exigiendo_botsito_allow_main_aunque_haya_sello(
    repo: Path, m: ModuleType
) -> None:
    git(repo, "branch", "-q", "-m", "main")
    _escribir(repo, "b.txt", "b\n")
    git(repo, "add", "b.txt")
    assert m.sellar(repo)[0]
    sin = git(repo, "commit", "-q", "-m", "b")
    assert sin.returncode != 0 and "commit directo en main rechazado" in sin.stderr
    env = _entorno() | {"BOTSITO_ALLOW_MAIN": "1"}
    assert git(repo, "commit", "-q", "-m", "b", env=env).returncode == 0


def test_el_bloque_del_sello_es_el_mismo_en_los_dos_hooks() -> None:
    def bloque(nombre: str) -> str:
        texto = (HOOKS / nombre).read_text(encoding="utf-8")
        assert texto.count(INICIO) == 1 and texto.count(FIN) == 1, nombre
        return texto[texto.index(INICIO) : texto.index(FIN)]

    assert bloque("pre-commit") == bloque("pre-merge-commit")
    precommit = (HOOKS / "pre-commit").read_text(encoding="utf-8")
    assert precommit.index("BOTSITO_ALLOW_MAIN") < precommit.index(INICIO)


def test_ninguna_via_de_escape_nueva() -> None:
    for nombre in ("pre-commit", "pre-merge-commit"):
        texto = (HOOKS / nombre).read_text(encoding="utf-8")
        variables = set(re.findall(r'"\$(BOTSITO_[A-Z_]+)"', texto))
        assert variables <= {"BOTSITO_ALLOW_MAIN"}, (nombre, variables)
    assert "--no-verify" in (RAIZ / "CLAUDE.md").read_text(encoding="utf-8")
