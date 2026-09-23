"""La guardia de ids citados en los documentos (2026-09-22, rama `trabajo/guardia-ids-docs`).

Todo id citado en `docs/**`, `CLAUDE.md` o `PROJECT_STATE.md` existe, o esta DECLARADO en su propio
documento con motivo. Un repo minimo de fixture con cada caso; la gramatica es `comun.ids.FUENTE` y
el conjunto de existencia se le pasa, igual que hace `knowledge validate` con el de los trailers.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.validation.ids_citados import problemas_de_ids_citados

EXISTE = "ev-v1-000100-0000aaaa"
NO_EXISTE = "ev-v1-000200-0000bbbb"
ADR_EXISTE = "ADR-0001"
EXISTENTES = {EXISTE, ADR_EXISTE}


def _doc(tmp_path: Path, texto: str, nombre: str = "docs/validation/INFORME.md") -> Path:
    ruta = tmp_path / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return tmp_path


def _bloque(*lineas: str, cita: bool = True) -> str:
    p = "> " if cita else ""
    cuerpo = "".join(f"{p}{linea}\n" for linea in lineas)
    return f"{p}```ids-inexistentes\n{cuerpo}{p}```\n"


@pytest.mark.contract
def test_un_id_que_existe_pasa(tmp_path: Path) -> None:
    repo = _doc(tmp_path, f"Se cita {EXISTE} y {ADR_EXISTE}.\n")
    assert problemas_de_ids_citados(repo, EXISTENTES) == []


@pytest.mark.contract
def test_un_id_inexistente_sin_declarar_falla_nombrando_fichero_linea_e_id(tmp_path: Path) -> None:
    repo = _doc(tmp_path, f"Titulo\n\nSe cita {NO_EXISTE}.\n")
    assert problemas_de_ids_citados(repo, EXISTENTES) == [
        f"docs/validation/INFORME.md:3: {NO_EXISTE}"
    ]


@pytest.mark.contract
def test_un_id_declarado_con_motivo_y_citado_pasa(tmp_path: Path) -> None:
    texto = _bloque(f"{NO_EXISTE} — salida de una copia desechable") + f"\nCuerpo: {NO_EXISTE}.\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == []


@pytest.mark.contract
def test_la_declaracion_solo_exime_en_su_documento(tmp_path: Path) -> None:
    texto = _bloque(f"{NO_EXISTE} — motivo") + f"\n{NO_EXISTE}\n"
    repo = _doc(tmp_path, texto)
    _doc(tmp_path, f"Otro documento que cita {NO_EXISTE}.\n", "docs/OTRO.md")
    assert problemas_de_ids_citados(repo, EXISTENTES) == [f"docs/OTRO.md:1: {NO_EXISTE}"]


@pytest.mark.contract
def test_un_id_declarado_que_si_existe_falla(tmp_path: Path) -> None:
    texto = _bloque(f"{EXISTE} — lo creia inventado") + f"\n{EXISTE}\n"
    problemas = problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)
    assert len(problemas) == 1 and "SI existe" in problemas[0] and EXISTE in problemas[0]


@pytest.mark.contract
def test_un_id_declarado_y_no_citado_falla(tmp_path: Path) -> None:
    texto = _bloque(f"{NO_EXISTE} — motivo") + "\nEl cuerpo no lo cita.\n"
    problemas = problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)
    assert len(problemas) == 1 and "no citado" in problemas[0]


@pytest.mark.contract
def test_un_id_que_aparece_solo_en_su_bloque_de_declaracion_falla(tmp_path: Path) -> None:
    """La mencion dentro del propio bloque NO cuenta como cita: si contara, la regla de la
    declaracion muerta no podria fallar nunca. Con el id repetido dos veces en el bloque."""
    texto = "Titulo\n\n" + _bloque(f"{NO_EXISTE} — motivo que nombra {NO_EXISTE}")
    problemas = problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)
    assert len(problemas) == 1 and "no citado" in problemas[0]


@pytest.mark.contract
@pytest.mark.parametrize("linea", [NO_EXISTE, f"{NO_EXISTE} — ", f"{NO_EXISTE} - motivo con guion"])
def test_un_id_declarado_sin_motivo_falla(tmp_path: Path, linea: str) -> None:
    texto = _bloque(linea) + f"\n{NO_EXISTE}\n"
    problemas = problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)
    assert any("sin motivo" in p for p in problemas), problemas


@pytest.mark.contract
def test_lo_que_parece_un_id_y_no_lo_es_segun_fuente_se_ignora(tmp_path: Path) -> None:
    """Controles: ni `ADR-12345` ni `ADR-0001x` ni `ev-v1-12345-0000aaaa` son ids para FUENTE."""
    texto = "ADR-12345 · ADR-0001x · ev-v1-12345-0000aaaa · fb-X-0000aaaa · ev-*\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == []


@pytest.mark.contract
def test_claude_y_project_state_estan_en_el_alcance(tmp_path: Path) -> None:
    for nombre in ("CLAUDE.md", "PROJECT_STATE.md"):
        _doc(tmp_path, f"cita {NO_EXISTE}\n", nombre)
    assert problemas_de_ids_citados(tmp_path, EXISTENTES) == [
        f"CLAUDE.md:1: {NO_EXISTE}",
        f"PROJECT_STATE.md:1: {NO_EXISTE}",
    ]


@pytest.mark.contract
def test_el_bloque_tambien_vale_fuera_de_un_recuadro(tmp_path: Path) -> None:
    texto = _bloque(f"{NO_EXISTE} — motivo", cita=False) + f"\n{NO_EXISTE}\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto, "PROJECT_STATE.md"), EXISTENTES) == []


@pytest.mark.contract
def test_dos_bloques_en_un_documento_fallan(tmp_path: Path) -> None:
    texto = _bloque(f"{NO_EXISTE} — uno") + _bloque(f"{NO_EXISTE} — otro") + f"\n{NO_EXISTE}\n"
    problemas = problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)
    assert any("segundo bloque" in p for p in problemas)
