from pathlib import Path

REQUIRED_SECTIONS = [
    "Project Goal",
    "Approved Architecture",
    "Development Strategy",
    "How to Start a Session",
    "Change Regimes (must be respected)",
    "Current Phase",
    "Current Feature",
    "Current Branch",
    "Stable Main State",
    "Completed Phases",
    "Completed Features",
    "Features Waiting for Validation",
    "Existing Components",
    "Important Files",
    "Tests Currently Passing",
    "Architectural Decisions (index)",
    "Decisions and Rationale",
    "Expert Entry Points",
    "Expert Validations",
    "Known Ambiguities",
    "Known Contradictions",
    "Known Issues",
    "Technical Debt",
    "Open Questions",
    "Things That Must Not Be Changed",
    "Next Feature",
    "Next Action",
    "Last Stable Commit",
    "Change Log",
]


def _sections(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def test_project_state_exists(repo: Path) -> None:
    assert (repo / "PROJECT_STATE.md").exists()


def test_project_state_has_required_sections_in_order(repo: Path) -> None:
    text = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    found = _sections(text)
    missing = [s for s in REQUIRED_SECTIONS if s not in found]
    assert not missing, f"faltan secciones: {missing}"
    positions = [found.index(s) for s in REQUIRED_SECTIONS]
    assert positions == sorted(positions), "las secciones no estan en el orden del plan"


def test_project_state_declares_a_branch(repo: Path) -> None:
    text = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    start = text.index("## Current Branch")
    body = text[start:].split("\n## ", 1)[0]
    assert any(line.strip() for line in body.splitlines()[1:]), "Current Branch vacio"
