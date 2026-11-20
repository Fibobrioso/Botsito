"""G2: en una rama `trabajo/*`, `make check` no sella sin la fila de HOLDOUT-EXPOSICIONES del dia
(`scripts/contrato_rama.py`, rama `trabajo/guardias-holdout`; GUARDIAS-HOLDOUT.md, G2).

La funcion pura recibe la rama, el dia y el texto: los tests le inyectan los tres. Los de git van
sobre repos temporales, como los de `test_contrato_rama.py`: nunca se toca el repo real."""

from __future__ import annotations

import datetime as dt
import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "contrato_rama.py"
HOY = dt.date(2026, 11, 19)
AYER = dt.date(2026, 11, 18)
RAMA = "trabajo/prueba"

CABECERA = """\
# Exposiciones de holdout

Texto de antes de la tabla.

| Fecha | Que se vio | Particiones | Quien | ¿Quema? |
|---|---|---|---|---|
| 2026-10-01 | **Rama `trabajo/vieja`**: algo | ninguna | la sesion | No |
"""
COLA = """
## Lo que esto obliga

| Fecha | Otra tabla |
|---|---|
"""


def fila(dia: str, rama: str) -> str:
    return f"| {dia} | **Rama `{rama}` (`PRUEBA.md`): make check** | ninguna | la sesion | No |\n"


def texto(*filas: str, cola: str = COLA) -> str:
    return CABECERA + "".join(filas) + cola


@pytest.fixture(scope="module")
def c() -> ModuleType:
    nombre = "contrato_rama"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _mensaje(dia: str, rama: str) -> str:
    return (
        f"G2: falta la fila de HOLDOUT-EXPOSICIONES del {dia} para {rama}; escríbela y estadíala "
        "antes de este make check (ADR-0021 §4)"
    )


# ------------------------------------------------------------------ la funcion pura, inyectada


def test_pasa_con_la_fila_de_hoy_que_nombra_la_rama(c: ModuleType) -> None:
    assert c.problemas_fila_del_dia(RAMA, HOY, texto(fila("2026-11-19", RAMA))) == []


def test_falla_sin_ninguna_fila_del_dia(c: ModuleType) -> None:
    assert c.problemas_fila_del_dia(RAMA, HOY, texto()) == [_mensaje("2026-11-19", RAMA)]


def test_falla_sin_el_fichero(c: ModuleType) -> None:
    assert c.problemas_fila_del_dia(RAMA, HOY, None) == [_mensaje("2026-11-19", RAMA)]


def test_falla_con_la_fila_de_ayer(c: ModuleType) -> None:
    t = texto(fila("2026-11-18", RAMA))
    assert c.problemas_fila_del_dia(RAMA, HOY, t) == [_mensaje("2026-11-19", RAMA)]
    assert c.problemas_fila_del_dia(RAMA, AYER, t) == []


@pytest.mark.parametrize(
    "otra",
    [
        "trabajo/otra",
        "trabajo/prueba-2",  # empieza igual que la rama: no es ella
        "trabajo/prueb",  # la rama empieza igual que ella
        "fix/prueba",  # el mismo nombre con otro prefijo
        "feature/trabajo/prueba",
    ],
)
def test_falla_con_la_fila_de_hoy_de_otra_rama(c: ModuleType, otra: str) -> None:
    t = texto(fila("2026-11-19", otra))
    assert c.problemas_fila_del_dia(RAMA, HOY, t) == [_mensaje("2026-11-19", RAMA)]


def test_solo_cuenta_la_tabla_de_exposiciones_y_su_primera_columna(c: ModuleType) -> None:
    # una linea de otra tabla, o una que nombra el dia fuera de la primera columna, no es la fila
    otra_tabla = COLA + fila("2026-11-19", RAMA)
    assert c.problemas_fila_del_dia(RAMA, HOY, texto(cola=otra_tabla)) != []
    fuera = (
        f"| 2026-11-18 | **Rama `{RAMA}`**: escrita el 2026-11-19 | ninguna | la sesion | No |\n"
    )
    assert c.problemas_fila_del_dia(RAMA, HOY, texto(fuera)) != []
    prosa = f"El 2026-11-19, la rama `{RAMA}` leyo algo.\n"
    assert c.problemas_fila_del_dia(RAMA, HOY, texto(cola="\n" + prosa)) != []


def test_la_tabla_no_tiene_que_estar_al_final(c: ModuleType) -> None:
    """La tabla de HOLDOUT-EXPOSICIONES.md va seguida de «## Lo que esto obliga» (0.4)."""
    t = texto(fila("2026-11-17", "trabajo/otra"), fila("2026-11-19", RAMA))
    assert "## Lo que esto obliga" in t.split(fila("2026-11-19", RAMA), 1)[1]
    assert c.problemas_fila_del_dia(RAMA, HOY, t) == []


@pytest.mark.parametrize("rama", ["main", "fix/prueba", "feature/F01-prueba", "", "trabajo"])
def test_fuera_de_trabajo_no_actua(c: ModuleType, rama: str) -> None:
    assert c.problemas_fila_del_dia(rama, HOY, None) == []
    assert c.problemas_fila_del_dia(rama, HOY, texto()) == []


# ------------------------------------------------------------------ lo estadiado, en un repo


def git(repo: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    r = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=True,
    )
    return r.stdout


def escribir(repo: Path, rel: str, contenido: str) -> None:
    ruta = repo / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(contenido, encoding="utf-8")


EXPOSICIONES = "docs/validation/HOLDOUT-EXPOSICIONES.md"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    escribir(r, EXPOSICIONES, texto())
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "base")
    git(r, "checkout", "-q", "-b", RAMA)
    return r


def test_cuenta_la_fila_estadiada_y_no_la_del_arbol(c: ModuleType, repo: Path) -> None:
    escribir(repo, EXPOSICIONES, texto(fila("2026-11-19", RAMA)))
    # solo en el arbol de trabajo: no se sella, no cuenta
    assert c.fila_del_dia(repo, HOY) == [_mensaje("2026-11-19", RAMA)]
    git(repo, "add", EXPOSICIONES)
    assert c.fila_del_dia(repo, HOY) == []
    # estadiada y luego borrada del arbol: cuenta lo estadiado
    escribir(repo, EXPOSICIONES, texto())
    assert c.fila_del_dia(repo, HOY) == []


def test_en_un_repo_fuera_de_trabajo_no_actua(c: ModuleType, repo: Path) -> None:
    for rama in ("main", "fix/prueba"):
        git(repo, "checkout", "-q", "-B", rama)
        assert c.fila_del_dia(repo, HOY) == [], rama
    # HEAD separado (la CI puede dejar uno): sin rama, no actua
    git(repo, "checkout", "-q", "--detach")
    assert c.fila_del_dia(repo, HOY) == []


def test_main_del_guion_niega_sin_la_fila_en_trabajo(
    c: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`main()` -lo que lanza `make check`- llama a G2 despues del contrato, con el dia de `_hoy`
    (el reloj local): sin contrato.yaml, sin fila del dia y en trabajo/, sale con 1 y el mensaje
    de G2; con la fila estadiada, con 0."""
    monkeypatch.setattr(c, "RAIZ", repo)
    monkeypatch.setattr(c, "_hoy", lambda: HOY)
    assert c.main() == 1
    assert _mensaje("2026-11-19", RAMA) in capsys.readouterr().err
    escribir(repo, EXPOSICIONES, texto(fila("2026-11-19", RAMA)))
    git(repo, "add", EXPOSICIONES)
    assert c.main() == 0
    assert "G2: fila de HOLDOUT-EXPOSICIONES del 2026-11-19" in capsys.readouterr().out


def test_hoy_es_el_dia_del_reloj_local(c: ModuleType) -> None:
    antes = dt.date.today()
    assert c._hoy() in {antes, dt.date.today()}
