"""El hook no depende de la codificacion de la consola (rama `trabajo/simulador-cuenta`).

Desde una consola de Windows en cp1252, `uv run --no-sync lint-imports` pintaba un emoji, Python
reventaba con `UnicodeEncodeError` y `pre-commit` lo contaba como «contrato de importacion roto».
Medido el 2026-09-25: con `PYTHONUTF8=0` falla y con `PYTHONUTF8=1` pasa. Los hooks versionados
exportan la variable ellos mismos, y aqui se comprueba sobre un repo TEMPORAL:

- la consola se SIMULA -UTF-8 apagado, locale C sin coercion- y un `uv` FALSO en el PATH hace lo
  que hacia el real: pintar un emoji con Python;
- el CONTROL demuestra que la simulacion muerde: la herramienta suelta falla;
- el hook tal como esta versionado pasa; el mismo hook SIN la linea del export -el mutante-
  rechaza el commit con el mensaje de contrato roto, que es lo que pasaba antes.

Nunca se toca el repo real ni se llama al `uv` de verdad.
"""

from __future__ import annotations

import importlib.util
import os
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
EXPORT = "export PYTHONUTF8=1"
EMOJI = "✅"


def _sello() -> ModuleType:
    nombre = "sello_make_check"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _git(repo: Path, env: dict[str, str], *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, encoding="utf-8", check=False, env=env
    )


def _ejecutable(ruta: Path) -> None:
    ruta.chmod(ruta.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _uv_falso(carpeta: Path) -> Path:
    """Un `uv` de mentira delante en el PATH: `lock --check` pasa y `run ...` pinta un emoji con
    el MISMO interprete que corre los tests, que es lo que hacia `lint-imports` de verdad."""
    carpeta.mkdir()
    pinta = carpeta / "pinta_emoji.py"
    pinta.write_text(f'print("{EMOJI} contratos en verde")\n', encoding="utf-8")
    uv = carpeta / "uv"
    uv.write_text(
        "#!/bin/sh\n"
        "# uv FALSO para el test de codificacion: nunca toca el entorno real.\n"
        'case "$1" in\n'
        "  lock) exit 0 ;;\n"
        f'  run) exec "{Path(sys.executable).as_posix()}" "{pinta.as_posix()}" ;;\n'
        "esac\n"
        "exit 3\n",
        encoding="utf-8",
        newline="\n",
    )
    _ejecutable(uv)
    return pinta


def _consola_cp1252(uv_dir: Path) -> dict[str, str]:
    """El entorno de una consola sin UTF-8: Python sin modo UTF-8, locale C y sin coercion, y sin
    ninguna variable que ya lo arreglara desde fuera."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for k in ("BOTSITO_ALLOW_MAIN", "PYTHONIOENCODING", "PYTHONLEGACYWINDOWSSTDIO"):
        env.pop(k, None)
    env.update(
        {
            "PYTHONUTF8": "0",
            "PYTHONCOERCECLOCALE": "0",
            "LC_ALL": "C",
            "LANG": "C",
            "PATH": str(uv_dir) + os.pathsep + env.get("PATH", ""),
        }
    )
    return env


@pytest.fixture
def escenario(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """Un repo en una rama de trabajo con `pyproject.toml` (para que el hook llame a `uv`), los
    hooks versionados instalados y un primer commit sellado. Devuelve el repo y el entorno de la
    consola simulada, tras comprobar que esa simulacion hace fallar a la herramienta suelta."""
    if shutil.which("git") is None or shutil.which("sh") is None:
        pytest.skip("sin git o sin sh en PATH")
    pinta = _uv_falso(tmp_path / "uv-falso")
    env = _consola_cp1252(tmp_path / "uv-falso")
    control = subprocess.run(
        [sys.executable, str(pinta)], capture_output=True, encoding="utf-8", check=False, env=env
    )
    if control.returncode == 0:
        if sys.platform == "win32":
            pytest.fail("la consola simulada no reproduce el fallo cp1252 en Windows")
        pytest.skip("esta plataforma pinta el emoji aunque se apague el modo UTF-8")
    assert "UnicodeEncodeError" in control.stderr, control.stderr

    r = tmp_path / "repo"
    r.mkdir()
    _git(r, env, "init", "-q", "-b", "trabajo/prueba")
    for clave, valor in (
        ("user.email", "t@t"),
        ("user.name", "t"),
        ("core.autocrlf", "false"),
        ("commit.gpgsign", "false"),
    ):
        _git(r, env, "config", clave, valor)
    _instalar_hooks(r, env)
    (r / "pyproject.toml").write_text("[project]\nname = 'prueba'\n", encoding="utf-8")
    (r / "a.txt").write_text("a\n", encoding="utf-8")
    _git(r, env, "add", "pyproject.toml", "a.txt")
    assert _sello().sellar(r)[0]
    return r, env


def _instalar_hooks(r: Path, env: dict[str, str], sin_export: bool = False) -> None:
    destino = Path(_git(r, env, "rev-parse", "--git-path", "hooks").stdout.strip())
    destino = destino if destino.is_absolute() else r / destino
    destino.mkdir(parents=True, exist_ok=True)
    for nombre in ("pre-commit", "pre-merge-commit"):
        texto = (HOOKS / nombre).read_text(encoding="utf-8")
        if sin_export:
            assert EXPORT in texto
            texto = texto.replace(EXPORT + "\n", "")
        objetivo = destino / nombre
        objetivo.write_text(texto, encoding="utf-8", newline="\n")
        _ejecutable(objetivo)


def test_el_hook_pasa_con_la_consola_en_cp1252(escenario: tuple[Path, dict[str, str]]) -> None:
    repo, env = escenario
    c = _git(repo, env, "commit", "-q", "-m", "inicio")
    assert c.returncode == 0, c.stderr
    assert "contrato de importacion roto" not in c.stderr


def test_el_mutante_sin_el_export_reproduce_el_fallo_de_antes(
    escenario: tuple[Path, dict[str, str]],
) -> None:
    """Sin la linea del export, el mismo commit se rechaza como «contrato de importacion roto»:
    es el fallo que se veia desde la consola del usuario, y prueba que este test lo caza."""
    repo, env = escenario
    _instalar_hooks(repo, env, sin_export=True)
    c = _git(repo, env, "commit", "-q", "-m", "inicio")
    assert c.returncode != 0
    assert "contrato de importacion roto" in c.stderr
    assert "UnicodeEncodeError" in c.stderr
    # con el hook versionado, el mismo arbol sellado entra
    _instalar_hooks(repo, env)
    c = _git(repo, env, "commit", "-q", "-m", "inicio")
    assert c.returncode == 0, c.stderr


def test_los_dos_hooks_exportan_utf8_antes_de_lanzar_nada() -> None:
    for nombre in ("pre-commit", "pre-merge-commit"):
        texto = (HOOKS / nombre).read_text(encoding="utf-8")
        assert texto.count(EXPORT) == 1, nombre
        lineas = texto.splitlines()
        export = next(i for i, x in enumerate(lineas) if x.strip() == EXPORT)
        llamadas = [
            i for i, x in enumerate(lineas) if not x.lstrip().startswith("#") and "uv " in x
        ]
        assert all(export < i for i in llamadas), f"{nombre}: el export va antes de llamar a uv"


def test_el_ritual_ya_no_pide_anteponer_la_variable() -> None:
    ritual = (RAIZ / "docs" / "runbooks" / "RITUAL.md").read_text(encoding="utf-8")
    assert "PYTHONUTF8" in ritual
    assert "PYTHONUTF8=1 git commit" not in ritual
    readme = (HOOKS / "README.md").read_text(encoding="utf-8")
    assert "PYTHONUTF8" in readme
