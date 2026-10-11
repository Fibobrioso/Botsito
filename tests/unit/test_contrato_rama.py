"""El contrato de rama (`scripts/contrato_rama.py`, rama `trabajo/guardias-claude`).

Sobre repos temporales con `main` y una rama de trabajo: nunca se toca el repo real, salvo para
leer los ejemplos del runbook y, si existe, el contrato de la rama actual."""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "contrato_rama.py"
RUNBOOK = RAIZ / "docs" / "runbooks" / "CONTRATO-DE-RAMA.md"

CONTRATO = """\
rama: trabajo/prueba
riesgo: bajo
artefacto: docs/validation/PRUEBA.md
rutas_permitidas:
  - docs/validation/PRUEBA.md
  - src/botsito/engine/
  - tests/unit/test_*.py
rutas_protegidas:
  - src/botsito/engine/broker.py
comprobaciones:
  - uv run pytest tests/unit -q
"""


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


def escribir(repo: Path, rel: str, texto: str = "x\n") -> None:
    ruta = repo / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    git(r, "init", "-q", "-b", "main")
    escribir(r, "README.md")
    escribir(r, "src/botsito/engine/broker.py")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "base")
    git(r, "checkout", "-q", "-b", "trabajo/prueba")
    escribir(r, "contrato.yaml", CONTRATO)
    escribir(r, "docs/validation/PRUEBA.md")
    git(r, "add", "-A")
    git(r, "commit", "-q", "-m", "contrato e informe")
    return r


def test_pasa_con_un_diff_dentro_de_las_rutas_permitidas(c: ModuleType, repo: Path) -> None:
    escribir(repo, "src/botsito/engine/motor.py")
    escribir(repo, "tests/unit/test_motor.py")
    git(repo, "add", "-A")
    problemas, resumen = c.comprobar(repo)
    assert problemas == []
    assert "4 ficheros" in resumen  # el contrato, el informe y los dos nuevos


def test_falla_con_un_diff_fuera_de_las_rutas_permitidas(c: ModuleType, repo: Path) -> None:
    escribir(repo, "knowledge/spec/strategy_spec.yaml")
    escribir(repo, "tests/unit/sub/test_x.py")  # `*` no cruza carpetas
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "se sale")
    problemas, _ = c.comprobar(repo)
    assert problemas == [
        "knowledge/spec/strategy_spec.yaml: fuera de rutas_permitidas",
        "tests/unit/sub/test_x.py: fuera de rutas_permitidas",
    ]


def test_lo_protegido_manda_sobre_lo_permitido(c: ModuleType, repo: Path) -> None:
    escribir(repo, "src/botsito/engine/broker.py", "cambiado\n")
    git(repo, "add", "-A")
    problemas, _ = c.comprobar(repo)
    assert problemas == [
        "src/botsito/engine/broker.py: dentro de rutas_protegidas (src/botsito/engine/broker.py)"
    ]


def test_cuenta_lo_estadiado_y_no_lo_que_no_lo_esta(c: ModuleType, repo: Path) -> None:
    escribir(repo, "fuera.txt")
    assert c.comprobar(repo)[0] == []  # sin estadiar: no se sella, no se mira
    git(repo, "add", "fuera.txt")
    assert c.comprobar(repo)[0] == ["fuera.txt: fuera de rutas_permitidas"]


def test_falla_si_falta_el_artefacto(c: ModuleType, repo: Path) -> None:
    git(repo, "rm", "-q", "--cached", "docs/validation/PRUEBA.md")
    problemas, _ = c.comprobar(repo)
    assert problemas == ["falta el artefacto docs/validation/PRUEBA.md (no esta estadiado)"]


def test_sin_contrato_no_hay_nada_que_comprobar(c: ModuleType, repo: Path) -> None:
    git(repo, "rm", "-q", "contrato.yaml")
    escribir(repo, "lo/que/sea.txt")
    git(repo, "add", "-A")
    problemas, resumen = c.comprobar(repo)
    assert problemas == [] and "nada que comprobar" in resumen


def test_en_main_no_se_exige(c: ModuleType, repo: Path) -> None:
    git(repo, "checkout", "-q", "main")
    escribir(repo, "contrato.yaml", CONTRATO)
    problemas, resumen = c.comprobar(repo)
    assert problemas == [] and "en main" in resumen


def test_un_contrato_heredado_no_vale_y_el_prefijo_puede_cambiar(c: ModuleType, repo: Path) -> None:
    git(repo, "checkout", "-q", "-b", "trabajo/otra")
    assert any("heredado" in p for p in c.comprobar(repo)[0])
    git(repo, "checkout", "-q", "-b", "feature/prueba")
    assert c.comprobar(repo)[0] == []


@pytest.mark.parametrize(
    ("cambio", "fragmento"),
    [
        ("riesgo: bajo", "riesgo: enorme"),
        ("artefacto: docs/validation/PRUEBA.md", "artefacto: informe.md"),
        ("comprobaciones:\n  - uv run pytest tests/unit -q\n", "comprobaciones: []\n"),
        ("rama: trabajo/prueba", "rama: trabajo/prueba\nnotas: algo"),
    ],
)
def test_un_contrato_mal_escrito_falla(
    c: ModuleType, repo: Path, cambio: str, fragmento: str
) -> None:
    escribir(repo, "contrato.yaml", CONTRATO.replace(cambio, fragmento))
    git(repo, "add", "-A")
    problemas, _ = c.comprobar(repo)
    assert len(problemas) == 1 and problemas[0].startswith("contrato.yaml:"), problemas


HOJA = "# Hoja\n\n## R1 · Activar la sesion 4\n\n### R1.1 · Algo\n\n## Carril: lo de Aleks\n"


def _hoja_en_main(repo: Path) -> None:
    """La hoja de ruta entra en `main` y la rama se rehace sobre ella: el merge-base ya la tiene."""
    git(repo, "checkout", "-q", "main")
    escribir(repo, "docs/plan/HOJA-DE-RUTA.md", HOJA)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", "hoja de ruta")
    git(repo, "checkout", "-q", "trabajo/prueba")
    git(repo, "merge", "-q", "main", "-m", "trae la hoja")


def test_sin_hoja_de_ruta_en_la_base_el_tramo_no_se_exige(c: ModuleType, repo: Path) -> None:
    """La rama que trae la hoja de ruta (`trabajo/hoja-de-ruta`) no lleva tramo: su base no la
    tiene. Un contrato sin `tramo` sigue valiendo ahi."""
    escribir(repo, "docs/plan/HOJA-DE-RUTA.md", HOJA)
    escribir(
        repo, "contrato.yaml", CONTRATO.replace("  - docs/validation/PRUEBA.md\n", "  - docs/\n", 1)
    )
    git(repo, "add", "-A")
    assert c.comprobar(repo)[0] == []


def test_con_hoja_de_ruta_en_la_base_el_tramo_es_obligatorio(c: ModuleType, repo: Path) -> None:
    _hoja_en_main(repo)
    problemas, _ = c.comprobar(repo)
    assert len(problemas) == 1 and problemas[0].startswith("falta `tramo` en contrato.yaml"), (
        problemas
    )
    for tramo in ("R1", "R1 · Activar la sesion 4", "Carril: lo de Aleks"):
        escribir(repo, "contrato.yaml", CONTRATO + f'tramo: "{tramo}"\n')
        git(repo, "add", "-A")
        assert c.comprobar(repo)[0] == [], tramo


def test_un_tramo_que_no_esta_en_la_hoja_falla(c: ModuleType, repo: Path) -> None:
    _hoja_en_main(repo)
    escribir(repo, "contrato.yaml", CONTRATO + "tramo: R9\n")
    git(repo, "add", "-A")
    assert c.comprobar(repo)[0] == [
        "`tramo` 'R9' no es un tramo (`## `) de docs/plan/HOJA-DE-RUTA.md"
    ]
    # y un tramo que nombra una hoja que la rama no tiene, tambien
    assert c.problemas_de_tramo("R1", False, None) == [
        "`tramo` 'R1' nombra docs/plan/HOJA-DE-RUTA.md, que no existe en esta rama"
    ]


@pytest.mark.parametrize(
    ("patron", "ruta", "casa"),
    [
        ("docs/", "docs/a/b.md", True),
        ("docs/*.md", "docs/a/b.md", False),
        ("docs/**/*.md", "docs/a/b.md", True),
        ("docs/**/*.md", "docs/b.md", True),
        ("tests/unit/test_?.py", "tests/unit/test_a.py", True),
        (".claude/", ".claude/hooks/guardia.py", True),
        ("Makefile", "Makefile.bak", False),
    ],
)
def test_los_patrones(c: ModuleType, patron: str, ruta: str, casa: bool) -> None:
    assert (c.casa(ruta, (patron,)) is not None) is casa


def test_los_tres_ejemplos_del_runbook_son_contratos_validos(c: ModuleType, tmp_path: Path) -> None:
    bloques = re.findall(r"```yaml\n(.*?)```", RUNBOOK.read_text(encoding="utf-8"), re.S)
    assert len(bloques) >= 4  # la plantilla y los tres ejemplos
    for i, bloque in enumerate(bloques):
        ruta = tmp_path / f"c{i}.yaml"
        ruta.write_text(bloque, encoding="utf-8")
        assert c.cargar(ruta).riesgo in c.RIESGOS


def test_el_contrato_de_la_rama_actual_si_lo_hay_es_valido(c: ModuleType) -> None:
    if not (RAIZ / "contrato.yaml").is_file():
        pytest.skip("sin contrato.yaml en esta rama (en main sale antes del merge)")
    assert c.cargar(RAIZ / "contrato.yaml").artefacto.startswith("docs/validation/")


def test_make_check_comprueba_el_contrato() -> None:
    texto = (RAIZ / "Makefile").read_text(encoding="utf-8")
    objetivos = next(x for x in texto.splitlines() if x.startswith("check:")).split()[1:]
    assert "contrato" in objetivos
    assert "scripts/contrato_rama.py" in texto
