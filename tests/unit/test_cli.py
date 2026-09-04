import subprocess
from pathlib import Path

from botsito import __version__, cli

MINIMO = """# PROJECT STATE

## Current Feature
F99

## Current Branch
{branch}

## Completed Features
{completed}

## Tests Currently Passing
{tests}

## Last Stable Commit
{stable}
"""


def _repo_tmp(tmp_path: Path, branch: str = "main") -> Path:
    subprocess.run(["git", "init", "-q", "-b", branch], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text(
        "def test_uno():\n    pass\n\ndef test_dos():\n    pass\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    return tmp_path


def _state(repo: Path, **kw: str) -> None:
    valores = {"branch": "main", "completed": "—", "tests": "2", "stable": "—"}
    valores.update(kw)
    (repo / "PROJECT_STATE.md").write_text(MINIMO.format(**valores), encoding="utf-8")


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_state_check_ok_on_real_repo(repo: Path) -> None:
    branch = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    if not branch:  # HEAD separado (CI de pull request): solo se omite la rama
        return
    assert cli.state_check(repo) == 0


def test_detects_branch_mismatch(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, branch="feature/F99-otra")
    assert cli.state_check(r) == 1


def test_detects_wrong_test_count(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, tests="7 (inventado)")
    assert cli.state_check(r) == 1


def test_detects_stable_commit_mismatch_with_tag(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, stable="deadbee · falso")
    subprocess.run(["git", "add", "-A"], cwd=r, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "x"], cwd=r, check=True)
    subprocess.run(["git", "tag", "-a", "stable/F99", "-m", "t"], cwd=r, check=True)
    assert cli.state_check(r) == 1
    real = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=r, capture_output=True, text=True, check=True
    ).stdout.strip()
    _state(r, stable=f"{real} · merge")
    assert cli.state_check(r) == 0


def test_detects_completed_feature_without_report(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, completed="- F99 · algo")
    assert cli.state_check(r) == 1
    (r / "docs" / "validation" / "F99-algo.md").write_text("ok", encoding="utf-8")
    assert cli.state_check(r) == 0


def test_state_check_missing_file(tmp_path: Path) -> None:
    assert cli.state_check(tmp_path) == 2


def test_contar_tests(tmp_path: Path) -> None:
    assert cli.contar_tests(_repo_tmp(tmp_path)) == 2


def test_knowledge_validate_real_repo(repo: Path) -> None:
    assert cli.knowledge_validate(repo) == 0


def test_knowledge_validate_detecta_registro_roto(tmp_path: Path) -> None:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros:\n  - nombre: x\n", encoding="utf-8"
    )
    assert cli.knowledge_validate(tmp_path) == 1


def test_cli_entrypoint_runs(repo: Path) -> None:
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0


def test_config_validate_real_repo(repo: Path) -> None:
    assert cli.config_validate(repo) == 0


def test_config_validate_detecta_clave_del_registro(tmp_path: Path) -> None:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros:\n  - nombre: stop_fraccion\n    tipo: fraccion\n    unidad: u\n"
        '    descripcion: d\n    estado: CONFIRMED\n    valor: "0.75"\n'
        "    fuente: {tipo: decision, id: x}\n",
        encoding="utf-8",
    )
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\nstop_fraccion = "0.5"\n\n'
        '[rutas]\ncorpus = "c"\ndata = "d"\nknowledge = "k"\n',
        encoding="utf-8",
    )
    assert cli.config_validate(tmp_path) == 1
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n[rutas]\ncorpus = "c"\ndata = "d"\nknowledge = "k"\n',
        encoding="utf-8",
    )
    assert cli.config_validate(tmp_path) == 0
    assert cli.main(["--repo", str(tmp_path), "config", "validate"]) == 0
