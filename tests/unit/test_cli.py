import subprocess
from pathlib import Path

from botsito import __version__, cli


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_state_check_matches_real_branch(repo: Path) -> None:
    branch = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    if not branch:  # sin git (por ejemplo, un tarball): la comprobacion se omite
        return
    assert cli.state_check(repo) == 0


def test_state_check_detects_mismatch(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    (tmp_path / "PROJECT_STATE.md").write_text(
        "# PROJECT STATE\n\n## Current Feature\nF99\n\n## Current Branch\nfeature/F99-otra\n",
        encoding="utf-8",
    )
    assert cli.state_check(tmp_path) == 1


def test_state_check_missing_file(tmp_path: Path) -> None:
    assert cli.state_check(tmp_path) == 2


def test_knowledge_validate_noop(repo: Path) -> None:
    assert cli.knowledge_validate(repo) == 0


def test_cli_entrypoint_runs(repo: Path) -> None:
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0
