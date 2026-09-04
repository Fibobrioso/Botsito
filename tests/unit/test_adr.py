import re
from pathlib import Path

ADR_SECTIONS = [
    "Decision",
    "Problema que resuelve",
    "Alternativas consideradas",
    "Por que elegimos esta opcion",
    "Por que descartamos las demas",
    "Impacto",
    "Fecha / fase",
    "Estado",
]


def _adrs(repo: Path) -> list[Path]:
    pattern = "[0-9][0-9][0-9][0-9]-*.md"
    return sorted(p for p in (repo / "docs" / "adr").glob(pattern) if not p.name.startswith("0000"))


def test_at_least_one_adr(repo: Path) -> None:
    assert _adrs(repo), "no hay ADR"


def test_every_adr_has_status_and_sections(repo: Path) -> None:
    for adr in _adrs(repo):
        text = adr.read_text(encoding="utf-8")
        assert re.search(r"^status:\s*(ACTIVE|SUPERSEDED)\s*$", text, re.M), (
            f"{adr.name}: sin status"
        )
        heads = [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]
        missing = [s for s in ADR_SECTIONS if s not in heads]
        assert not missing, f"{adr.name}: faltan secciones {missing}"
        estado = text.rsplit("## Estado", 1)[1].strip().split()[0]
        assert estado in {"ACTIVE", "SUPERSEDED"}, f"{adr.name}: estado final invalido"


def test_adr_index_lists_every_adr(repo: Path) -> None:
    index = (repo / "docs" / "adr" / "README.md").read_text(encoding="utf-8")
    for adr in _adrs(repo):
        number = adr.name[:4]
        assert f"| {number} |" in index, f"ADR {number} no esta en docs/adr/README.md"
