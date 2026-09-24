"""El reparto dev-visto (ADR-0042): material ya visto, todo `dev`, sin sorteo y sin holdout.

Se prueba en repositorios temporales con un mes de mentira. Tres cosas que el ADR exige: un dia de
dev-visto es ingerible; un dia OCULTO no lo es aunque este en dev-visto (ADR-0041); y un mes que no
esta en `vistos.yaml` no puede entrar por aqui. Y el regimen del fichero: se recompone y se ancla.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from botsito.cases import visto
from botsito.cases.ingesta import IngestaError, dias_ingeribles

SHA = "a" * 64
LIBRO = "Material/backtesting-analytics PRUEBA.xlsx"
CONFIG = f"""simbolo: XXXYYY
dataset_prefijo: prueba-
ventana_local: {{desde: "00:00", hasta: "15:00"}}
sesiones:
  - {{nombre: "07-11", desde: "07:00", hasta: "11:00"}}
  - {{nombre: "11-15", desde: "11:00", hasta: "15:00"}}
anclajes_candidatos:
  - {{etiqueta: ny-17, hora: "17:00", huso: America/New_York, coincide_con_sesiones: true}}
min_velas_ventana: 850
etiquetas: [compra, venta, no_trade]
particiones: {{dev: 0, holdout-1: 1, holdout-2: 0, holdout-3: 0}}
cobertura_material:
  "2026-08":
    - desde: "2026-08-03"
      hasta: "2026-08-07"
      material_sha256: "{SHA}"
"""
LIBROS = f"""libros:
  "{SHA}":
    fichero: "{LIBRO}"
    lecturas:
      - formato: "AAAA/MM/DD HH:MM:SS"
        huso: UTC
    medida: sintetica
    declarado_el: "2026-09-23"
    fuente: [ADR-0039]
"""
DIAS = {"2026-08-03", "2026-08-04", "2026-08-05", "2026-08-06", "2026-08-07"}


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def _commit(repo: Path, mensaje: str) -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", mensaje)


def _repo(tmp_path: Path, mes_visto: str = "2026-08", expuesto: bool = True) -> Path:
    kit = tmp_path / "knowledge" / "cases" / "kit"
    kit.mkdir(parents=True)
    (kit / "config.yaml").write_text(CONFIG, encoding="utf-8")
    (kit / "vistos.yaml").write_text(f'meses:\n  - mes: "{mes_visto}"\n', encoding="utf-8")
    corpus = tmp_path / "knowledge" / "corpus"
    corpus.mkdir(parents=True)
    (corpus / "libros.yaml").write_text(LIBROS, encoding="utf-8")
    val = tmp_path / "docs" / "validation"
    val.mkdir(parents=True)
    texto = f"| 2026-09-21 | el xlsx `{Path(LIBRO).name}` entero |\n" if expuesto else "nada\n"
    (val / "HOLDOUT-EXPOSICIONES.md").write_text(texto, encoding="utf-8")
    _git(tmp_path, "init", "-q")
    _commit(tmp_path, "base")
    return tmp_path


def _con_reparto(tmp_path: Path) -> Path:
    repo = _repo(tmp_path)
    visto.escribir(repo, "2026-08", visto.construir(repo, "2026-08"))
    _commit(repo, "dev-visto")
    return repo


def test_un_dia_de_dev_visto_es_ingerible(tmp_path: Path) -> None:
    repo = _con_reparto(tmp_path)
    assert set(visto.asignacion(repo, "2026-08").values()) == {"dev"}
    assert set(dias_ingeribles(repo).dias) == DIAS
    assert visto.problemas(repo) == []


def test_un_dia_oculto_no_es_ingerible_aunque_este_en_dev_visto(tmp_path: Path) -> None:
    repo = _con_reparto(tmp_path)
    reparto = repo / "knowledge" / "cases" / "kit" / "s1"
    reparto.mkdir(parents=True)
    (reparto / "particiones.yaml").write_text(
        "asignacion:\n  caso-xxxyyy-2026-08-05: holdout-1\n", encoding="utf-8"
    )
    _commit(repo, "reserva un dia")
    assert set(dias_ingeribles(repo).dias) == DIAS - {"2026-08-05"}


def test_un_mes_que_no_esta_en_vistos_no_entra_por_aqui(tmp_path: Path) -> None:
    repo = _repo(tmp_path, mes_visto="2026-07")
    with pytest.raises(visto.VistoError, match="vistos.yaml"):
        visto.construir(repo, "2026-08")
    # Y si alguien escribe el reparto a mano, la ingesta falla cerrada en vez de aceptarlo.
    a_mano = repo / "knowledge" / "cases" / "visto" / "2026-08"
    a_mano.mkdir(parents=True)
    (a_mano / "particiones.yaml").write_text(
        "asignacion:\n  caso-xxxyyy-2026-08-03: dev\n", encoding="utf-8"
    )
    _commit(repo, "a mano")
    with pytest.raises(IngestaError, match="dev-visto invalido"):
        dias_ingeribles(repo)


def test_sin_la_lectura_completa_declarada_no_entra(tmp_path: Path) -> None:
    repo = _repo(tmp_path, expuesto=False)
    assert any("HOLDOUT-EXPOSICIONES" in p for p in visto.requisitos(repo, "2026-08"))


def test_el_reparto_se_recompone_y_esta_anclado(tmp_path: Path) -> None:
    repo = _con_reparto(tmp_path)
    ruta = repo / "knowledge" / "cases" / "visto" / "2026-08" / "particiones.yaml"
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace("caso-xxxyyy-2026-08-07: dev\n", ""),
        encoding="utf-8",
    )
    assert any("difiere" in p for p in visto.problemas(repo))
    _commit(repo, "manipula")
    assert any("anclas.yaml" in p or "ancla" in p for p in visto.problemas(repo))
    with pytest.raises(visto.VistoError, match="no se sobreescribe"):
        visto.escribir(repo, "2026-08", visto.construir(repo, "2026-08"))
