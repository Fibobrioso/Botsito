from pathlib import Path

# Arbol de MASTER_PLAN seccion B. Cada carpeta debe existir y tener un README de
# responsabilidad (o ser un paquete Python con docstring en __init__.py).
DOC_DIRS = [
    "docs/plan",
    "docs/plan/features",
    "docs/adr",
    "docs/validation",
    "docs/spec",
    "docs/runbooks",
    "knowledge",
    "knowledge/corpus",
    "knowledge/evidence",
    "knowledge/feedback",
    "knowledge/spec",
    "knowledge/cases",
    "knowledge/cases/dev",
    "knowledge/cases/holdout",
    "knowledge/cases/holdout/1",
    "knowledge/cases/holdout/2",
    "knowledge/cases/holdout/3",
    "knowledge/cases/fixtures",
    "mql5",
    "mql5/Experts",
    "mql5/Include/Botsito",
    "mql5/Scripts",
    "mql5/tester",
    "scripts",
    "data/manifests",
]
# Ninguna carpeta queda exenta: toda carpeta declara su responsabilidad.
README_EXEMPT: set[str] = set()
PACKAGES = [
    "corpus",
    "evidence",
    "feedback",
    "spec",
    "cases",
    "data",
    "domain",
    "engine",
    "validation",
    "viewer",
    "mql5bridge",
]
TEST_DIRS = ["unit", "contract", "integration", "golden", "regression", "differential"]
ROOT_FILES = [
    "PROJECT_STATE.md",
    "README.md",
    "pyproject.toml",
    "Makefile",
    ".gitignore",
    ".pre-commit-config.yaml",
    ".github/workflows/ci.yml",
    "config/settings.example.toml",
    "docs/plan/MASTER_PLAN.md",
    "docs/adr/0000-template.md",
    "docs/plan/features/_template.md",
    "docs/validation/_template.md",
]


def test_root_files(repo: Path) -> None:
    missing = [f for f in ROOT_FILES if not (repo / f).exists()]
    assert not missing, missing


def test_doc_dirs_exist_with_readme(repo: Path) -> None:
    missing = [d for d in DOC_DIRS if not (repo / d).is_dir()]
    assert not missing, f"carpetas ausentes: {missing}"
    no_readme = [
        d for d in DOC_DIRS if d not in README_EXEMPT and not (repo / d / "README.md").exists()
    ]
    assert not no_readme, f"sin README: {no_readme}"


def test_packages_have_docstring(repo: Path) -> None:
    for p in PACKAGES:
        init = repo / "src" / "botsito" / p / "__init__.py"
        assert init.exists(), f"falta paquete {p}"
        assert init.read_text(encoding="utf-8").lstrip().startswith('"""'), f"{p}: sin docstring"


def test_test_dirs(repo: Path) -> None:
    missing = [d for d in TEST_DIRS if not (repo / "tests" / d).is_dir()]
    assert not missing, missing
