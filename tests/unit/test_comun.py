from pathlib import Path

import pytest

from botsito.comun import ids
from botsito.comun.documentos import (
    activos,
    cargar_directorio,
    ciclos_de_supersede,
    ficheros_de,
    hash_corto,
    normalizar_texto,
    vacio,
)
from botsito.comun.husos import HusoDesconocidoError, huso_canonico


def test_ids() -> None:
    assert ids.es_id_de("evidence", "ev-v4-001533-1a2b3c4d")
    assert not ids.es_id_de("evidence", "ev-v4-\u0660\u0660\u0661533-1a2b3c4d")
    assert ids.es_id_de("dataset", "eurusd-m1-2026-01-e37291d4")
    assert ids.es_id_de("decision", "ADR-0006") and not ids.es_id_de("decision", "ADR-6")
    assert not ids.es_id_de("inexistente", "x") and not ids.es_id_de("caso", 3)


def test_documentos() -> None:
    assert normalizar_texto("  a \t b\n") == "a b"
    assert vacio("  ") and vacio([]) and vacio(None) and not vacio(0) and not vacio("x")
    assert hash_corto("a") == hash_corto("a") and len(hash_corto("a")) == 8
    assert ciclos_de_supersede({"a": "b", "b": "a"}) == ["ciclo de supersede: a -> b -> a"]
    assert ciclos_de_supersede({"a": "b", "b": None}) == []

    class R:
        def __init__(self, i: str, s: str | None) -> None:
            self.id, self.supersede = i, s

    assert [r.id for r in activos([R("a", None), R("b", "a")])] == ["b"]


def test_ficheros_de_y_cargar_directorio(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    (tmp_path / "_gen.yaml").write_text("x", encoding="utf-8")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.yaml").write_text("b", encoding="utf-8")
    (tmp_path / "a.yaml").write_text("a", encoding="utf-8")
    assert [p.name for p in ficheros_de(tmp_path, ValueError, "x")] == ["a.yaml", "b.yaml"]
    (tmp_path / "roto.yml").write_text("x", encoding="utf-8")
    with pytest.raises(ValueError, match="inesperado"):
        ficheros_de(tmp_path, ValueError, "x")
    (tmp_path / "roto.yml").unlink()
    with pytest.raises(ValueError, match="repetidos"):
        cargar_directorio(tmp_path, lambda p: "mismo", ValueError, "x", lambda i: i)
    with pytest.raises(ValueError, match="no existe"):
        ficheros_de(tmp_path / "nada", ValueError, "x")


def test_husos() -> None:
    assert str(huso_canonico("Europe/Madrid")) == "Europe/Madrid"
    for malo in ("Europe/madrid", "utc", "Marte/Olympus", "", None):
        with pytest.raises(HusoDesconocidoError):
            huso_canonico(malo)
