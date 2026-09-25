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


SECCION_INDICE = "## Architectural Decisions (index)"


def _indice_de_project_state(texto: str) -> list[str]:
    """Los numeros de ADR que lista el indice de PROJECT_STATE, en orden y con repeticiones."""
    assert SECCION_INDICE in texto, f"PROJECT_STATE sin la seccion {SECCION_INDICE!r}"
    seccion = texto.split(SECCION_INDICE, 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^- ADR-(\d{4})\b", seccion, re.M)


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


def test_project_state_indexa_exactamente_los_adr_que_existen(repo: Path) -> None:
    """K-01 de la sesion 02: ADR-0045 falto del indice de PROJECT_STATE sin que nada lo viera."""
    existen = {p.name[:4] for p in _adrs(repo)}
    texto = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    problemas = _problemas_del_indice(existen, _indice_de_project_state(texto))
    assert not problemas, "; ".join(problemas)


def test_el_indice_caza_el_que_falta_el_que_sobra_y_el_repetido() -> None:
    texto = (
        "# x\n\n## Architectural Decisions (index)\n"
        "- ADR-0001 uno — ACTIVE\n- ADR-0003 tres — ACTIVE\n- ADR-0003 otra vez — ACTIVE\n"
        "\n## Decisions and Rationale\n- ADR-0002 fuera de la seccion no cuenta\n"
    )
    listados = _indice_de_project_state(texto)
    assert listados == ["0001", "0003", "0003"]
    problemas = " ".join(_problemas_del_indice({"0001", "0002"}, listados))
    assert "repetidos en el indice: ['0003']" in problemas
    assert "faltan en el indice: ['0002']" in problemas
    assert "no existen en docs/adr/: ['0003']" in problemas
    assert _problemas_del_indice({"0001"}, ["0001"]) == []
