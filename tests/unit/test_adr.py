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


# El indice de ADR vive en docs/adr/README.md. Hasta la dieta de PROJECT_STATE (rama
# `trabajo/dieta-y-skills`, 2026-10-01) habia otro en PROJECT_STATE, y este test -nacido de K-01 de
# la sesion 02: ADR-0045 falto de aquel indice sin que nada lo viera- lo vigilaba; aquel indice paso
# a docs/state/HISTORIA.md y la guardia entera (que falte, que sobre, que se repita) pasa al README.
FILA_INDICE = re.compile(r"^\| (\d{4}) \|", re.M)


def _indice_del_readme(texto: str) -> list[str]:
    """Los numeros de ADR que lista la tabla de docs/adr/README.md, en orden y con repeticiones."""
    return FILA_INDICE.findall(texto)


def _problemas_del_indice(existen: set[str], listados: list[str]) -> list[str]:
    problemas = []
    repetidos = sorted({n for n in listados if listados.count(n) > 1})
    if repetidos:
        problemas.append(f"repetidos en el indice: {repetidos}")
    if faltan := sorted(existen - set(listados)):
        problemas.append(f"existen en docs/adr/ y faltan en el indice: {faltan}")
    if sobran := sorted(set(listados) - existen):
        problemas.append(f"estan en el indice y no existen en docs/adr/: {sobran}")
    return problemas


def test_el_readme_indexa_exactamente_los_adr_que_existen(repo: Path) -> None:
    existen = {p.name[:4] for p in _adrs(repo)}
    texto = (repo / "docs" / "adr" / "README.md").read_text(encoding="utf-8")
    problemas = _problemas_del_indice(existen, _indice_del_readme(texto))
    assert not problemas, "; ".join(problemas)


def test_el_indice_caza_el_que_falta_el_que_sobra_y_el_repetido() -> None:
    texto = (
        "# ADR\n\n| ADR | Titulo | Estado |\n|---|---|---|\n"
        "| 0001 | uno | ACTIVE |\n| 0003 | tres | ACTIVE |\n| 0003 | otra vez | ACTIVE |\n"
        "\nTexto que cita | 0002 | sin ser fila no cuenta\n"
    )
    listados = _indice_del_readme(texto)
    assert listados == ["0001", "0003", "0003"]
    problemas = " ".join(_problemas_del_indice({"0001", "0002"}, listados))
    assert "repetidos en el indice: ['0003']" in problemas
    assert "faltan en el indice: ['0002']" in problemas
    assert "no existen en docs/adr/: ['0003']" in problemas
    assert _problemas_del_indice({"0001"}, ["0001"]) == []
