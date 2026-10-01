"""docs/state/HISTORIA.md solo se amplia, y su Archivo 1 es PROJECT_STATE.md antes de la dieta.

Rama `trabajo/dieta-y-skills` (2026-10-01). El encargo pedia dos cosas que aqui se vuelven tests:
que HISTORIA «solo se amplía y nunca se reescribe», y comprobar «que ningún texto se pierde: todo
lo anterior está en HISTORIA.md o en PROJECT_STATE.md». La segunda es literal: el Archivo 1 es el
fichero entero de `df6aa2c`, byte a byte, asi que todo lo que habia esta en HISTORIA.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

from botsito.comun import historial

HISTORIA = "docs/state/HISTORIA.md"
ANTES_DE_LA_DIETA = "df6aa2c"
ARCHIVO_1 = "# Archivo 1 "


def problemas_de_solo_ampliar(repo: Path, ruta: str) -> list[str]:
    """Cada version commiteada de `ruta` empieza por la de su padre, y el disco por la de HEAD."""
    problemas: list[str] = []
    for commit, padre in historial.versiones_del_fichero(repo, ruta) or []:
        antes = historial.contenido_en(repo, padre, ruta)
        despues = historial.contenido_en(repo, commit, ruta)
        if antes is None:
            continue  # el commit que lo anadio
        if despues is None or not despues.startswith(antes):
            problemas.append(f"{commit[:7]} reescribe o borra {ruta} (no empieza por {padre[:7]})")
    en_head = historial.contenido_en_head(repo, ruta)
    disco = repo / ruta
    if en_head is not None and (
        not disco.exists() or not disco.read_text(encoding="utf-8").startswith(en_head)
    ):
        problemas.append(f"el {ruta} del disco no empieza por el de HEAD")
    return problemas


def test_historia_solo_se_amplia(repo: Path) -> None:
    if motivo := historial.historial_evaluable(repo):
        pytest.skip(motivo)
    assert problemas_de_solo_ampliar(repo, HISTORIA) == []


def test_el_archivo_1_es_project_state_entero_antes_de_la_dieta(repo: Path) -> None:
    if motivo := historial.historial_evaluable(repo):
        pytest.skip(motivo)
    original = historial.contenido_en(repo, ANTES_DE_LA_DIETA, "PROJECT_STATE.md")
    assert original, f"no se lee PROJECT_STATE.md en {ANTES_DE_LA_DIETA}"
    texto = (repo / HISTORIA).read_text(encoding="utf-8")
    assert ARCHIVO_1 in texto, "HISTORIA sin su Archivo 1"
    tras_el_encabezado = texto.split(ARCHIVO_1, 1)[1].split("\n", 1)[1].lstrip("\n")
    assert tras_el_encabezado.startswith(original), (
        "el Archivo 1 no es, byte a byte, el PROJECT_STATE.md de antes de la dieta"
    )


def _git(repo: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def test_la_guardia_caza_una_reescritura_y_deja_pasar_lo_anadido(tmp_path: Path) -> None:
    """Que no sea decorativa: anadir pasa; cambiar una linea vieja, commiteada o en disco, no."""
    r = tmp_path / "repo"
    (r / "docs" / "state").mkdir(parents=True)
    _git(r, "init", "-q", "-b", "trabajo/x")
    for clave, valor in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
        _git(r, "config", clave, valor)
    fichero = r / HISTORIA
    fichero.write_text("# Archivo 1\nuno\n", encoding="utf-8", newline="\n")
    _git(r, "add", ".")
    _git(r, "commit", "-q", "-m", "uno")
    fichero.write_text("# Archivo 1\nuno\n# Archivo 2\ndos\n", encoding="utf-8", newline="\n")
    _git(r, "commit", "-q", "-am", "dos")
    assert problemas_de_solo_ampliar(r, HISTORIA) == []
    fichero.write_text("# Archivo 1\nUNO\n# Archivo 2\ndos\n", encoding="utf-8", newline="\n")
    assert problemas_de_solo_ampliar(r, HISTORIA) == [
        f"el {HISTORIA} del disco no empieza por el de HEAD"
    ]
    _git(r, "commit", "-q", "-am", "reescribe")
    assert any("reescribe o borra" in p for p in problemas_de_solo_ampliar(r, HISTORIA))
