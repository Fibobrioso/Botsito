from pathlib import Path

# Desde la dieta (rama `trabajo/dieta-y-skills`, 2026-10-01) PROJECT_STATE lleva solo el presente;
# lo demas -Project Goal, Existing Components, el indice de ADR, Lineamientos...- vive en
# docs/state/HISTORIA.md (docs/state/README.md).
REQUIRED_SECTIONS = [
    "Current Branch",
    "Current Feature",
    "Stable Main State",
    "Last Stable Commit",
    "Tests Currently Passing",
    "Next Action",
    "Known Ambiguities",
    "Technical Debt",
    "Reglas vivas",
    "Completed Features",
    "Change Log",
]
# El encargo de la dieta: «Objetivo: menos de 25 KB». Si una rama lo pasa, lo que dejo de ser
# presente se archiva en docs/state/HISTORIA.md; el tope no se sube.
TOPE_BYTES = 25_000


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
    sobran = [s for s in found if s not in REQUIRED_SECTIONS]
    assert not sobran, f"secciones que no son del presente (van a docs/state/HISTORIA.md): {sobran}"


def test_project_state_declares_a_branch(repo: Path) -> None:
    text = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    start = text.index("## Current Branch")
    body = text[start:].split("\n## ", 1)[0]
    assert any(line.strip() for line in body.splitlines()[1:]), "Current Branch vacio"


def test_project_state_cabe_en_el_tope(repo: Path) -> None:
    tamano = (repo / "PROJECT_STATE.md").stat().st_size
    assert tamano < TOPE_BYTES, (
        f"PROJECT_STATE.md pesa {tamano} bytes (tope {TOPE_BYTES}): archiva en "
        "docs/state/HISTORIA.md lo que ya no es presente (docs/state/README.md)"
    )
