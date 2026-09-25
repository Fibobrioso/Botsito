"""El push del ritual es UNO y atomico (rama `trabajo/arreglo-ci`, 2026-09-25).

El run 36174003223 de la CI salio rojo porque `main` y el tag se empujaron en dos lineas: la CI
hizo `git fetch --tags` cinco segundos despues del push de `main` y antes de que llegara el tag, y
`state check` vio el merge como cambios sin tag estable. Aqui se reproduce eso en un repo temporal,
y se fija que el ritual empuja los dos refs en el mismo `git push --atomic`."""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import pytest

from botsito.cli import state_check

RAIZ = Path(__file__).resolve().parents[2]
RUNBOOKS = RAIZ / "docs" / "runbooks"


def _entorno(fecha: str | None = None) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    if fecha:
        env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"] = fecha
    return env


def git(repo: Path, *args: str, fecha: str | None = None) -> str:
    r = subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        check=False,
        env=_entorno(fecha),
    )
    assert r.returncode == 0, (args, r.stderr)
    return r.stdout.strip()


ESTADO = """# Project State

## Current Branch
main

## Tests Currently Passing
0 funciones de test

## Last Stable Commit
{sha} · el ultimo merge

## Completed Features
- nada
"""


def _estado(repo: Path, sha: str) -> None:
    (repo / "PROJECT_STATE.md").write_text(ESTADO.format(sha=sha), encoding="utf-8")


@pytest.fixture
def repo_tras_el_merge(tmp_path: Path) -> tuple[Path, str]:
    """main con un tag viejo, un merge de una rama y el docs(state) que declara ese merge, SIN el
    tag nuevo: es lo que vio la CI en el run 36174003223."""
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    for clave, valor in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
        git(r, "config", clave, valor)
    (r / "a.txt").write_text("a\n", encoding="utf-8")
    _estado(r, "0000000")
    git(r, "add", ".")
    git(r, "commit", "-q", "-m", "inicio", fecha="2026-09-20T10:00:00")
    viejo = git(r, "rev-parse", "--short", "HEAD")
    _estado(r, viejo)
    git(r, "commit", "-q", "-am", "docs(state) viejo", fecha="2026-09-20T10:01:00")
    git(r, "tag", "-a", "stable/viejo", viejo, "-m", "viejo", fecha="2026-09-20T10:02:00")
    git(r, "checkout", "-q", "-b", "trabajo/rama")
    (r / "b.txt").write_text("b\n", encoding="utf-8")
    git(r, "add", "b.txt")
    git(r, "commit", "-q", "-m", "b", fecha="2026-09-21T10:00:00")
    git(r, "checkout", "-q", "main")
    git(r, "merge", "-q", "--no-ff", "trabajo/rama", "-m", "merge", fecha="2026-09-22T10:00:00")
    merge = git(r, "rev-parse", "--short", "HEAD")
    _estado(r, merge)
    git(r, "commit", "-q", "-am", "docs(state) nuevo", fecha="2026-09-22T10:01:00")
    return r, merge


def test_sin_su_tag_el_merge_son_cambios_sin_tag_estable(
    repo_tras_el_merge: tuple[Path, str], capsys: pytest.CaptureFixture[str]
) -> None:
    repo, _ = repo_tras_el_merge
    assert state_check(repo) == 1
    salida = capsys.readouterr().out
    assert "main tiene cambios sin tag estable desde stable/viejo: b.txt" in salida


def test_con_su_tag_el_mismo_arbol_pasa(
    repo_tras_el_merge: tuple[Path, str], capsys: pytest.CaptureFixture[str]
) -> None:
    repo, merge = repo_tras_el_merge
    git(repo, "tag", "-a", "stable/nuevo", merge, "-m", "nuevo", fecha="2026-09-22T10:02:00")
    assert state_check(repo) == 0, capsys.readouterr().out
    assert "OK: rama 'main'" in capsys.readouterr().out


def _lineas_de_codigo(texto: str) -> list[str]:
    """Las lineas de los bloques ``` del runbook: lo que se ejecuta, no la prosa."""
    lineas, dentro = [], False
    for linea in texto.splitlines():
        if linea.strip().startswith("```"):
            dentro = not dentro
            continue
        if dentro:
            lineas.append(linea.strip())
    return lineas


def _pushes(texto: str) -> list[str]:
    return [x for x in _lineas_de_codigo(texto) if re.match(r"git\s+push\b", x)]


def test_el_ritual_empuja_main_y_el_tag_en_un_solo_push_atomico() -> None:
    pushes = _pushes((RUNBOOKS / "RITUAL.md").read_text(encoding="utf-8"))
    assert "git push --atomic origin main stable/<tag>" in pushes, pushes
    assert len(pushes) == 1, f"el ritual tiene que empujar una sola vez: {pushes}"


def test_ningun_runbook_empuja_main_o_un_tag_por_separado() -> None:
    for runbook in sorted(RUNBOOKS.glob("*.md")):
        for push in _pushes(runbook.read_text(encoding="utf-8")):
            refs = push.split()
            lleva_main = "main" in refs
            lleva_tag = any(r.startswith("stable/") for r in refs)
            if lleva_main or lleva_tag:
                assert "--atomic" in refs and lleva_main and lleva_tag, (
                    f"{runbook.name}: '{push}' empuja main o un tag suelto; van juntos y --atomic"
                )


def test_el_detector_caza_el_push_suelto() -> None:
    viejo = "texto\n```\ngit push origin main\ngit push origin stable/<tag>\n```\n"
    assert _pushes(viejo) == ["git push origin main", "git push origin stable/<tag>"]
    assert _pushes("prosa con `git push origin main` fuera de un bloque\n") == []
