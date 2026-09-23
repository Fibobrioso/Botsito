"""La guardia de ids citados en los documentos (2026-09-22, rama `trabajo/guardia-ids-docs`).

Todo id citado en `docs/**`, `CLAUDE.md` o `PROJECT_STATE.md` existe, o esta DECLARADO en su propio
documento con motivo. Un repo minimo de fixture con cada caso; la gramatica es `comun.ids.FUENTE` y
el conjunto de existencia se le pasa, igual que hace `knowledge validate` con el de los trailers.

Cada caso comprueba el MENSAJE EXACTO, con el prefijo de su tipo: hasta el 2026-09-23 los cuatro
tipos de fallo compartian «id citado que no existe», y un «sin motivo» se leia como si faltara un
id.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.validation.ids_citados import (
    DECLARADO_Y_EXISTE,
    DECLARADO_Y_NO_CITADO,
    MAL_FORMADA,
    NO_EXISTE,
    problemas_de_ids_citados,
)

EXISTE = "ev-v1-000100-0000aaaa"
INEXISTENTE = "ev-v1-000200-0000bbbb"
ADR_EXISTE = "ADR-0001"
EXISTENTES = {EXISTE, ADR_EXISTE}
DOC = "docs/validation/INFORME.md"


def _doc(tmp_path: Path, texto: str, nombre: str = DOC) -> Path:
    ruta = tmp_path / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return tmp_path


def _bloque(*lineas: str, cita: bool = True) -> str:
    p = "> " if cita else ""
    cuerpo = "".join(f"{p}{linea}\n" for linea in lineas)
    return f"{p}```ids-inexistentes\n{cuerpo}{p}```\n"


@pytest.mark.contract
def test_los_cuatro_prefijos_son_distintos() -> None:
    assert len({NO_EXISTE, MAL_FORMADA, DECLARADO_Y_EXISTE, DECLARADO_Y_NO_CITADO}) == 4


@pytest.mark.contract
def test_un_id_que_existe_pasa(tmp_path: Path) -> None:
    repo = _doc(tmp_path, f"Se cita {EXISTE} y {ADR_EXISTE}.\n")
    assert problemas_de_ids_citados(repo, EXISTENTES) == []


@pytest.mark.contract
def test_un_id_inexistente_sin_declarar_falla_nombrando_fichero_linea_e_id(tmp_path: Path) -> None:
    repo = _doc(tmp_path, f"Titulo\n\nSe cita {INEXISTENTE}.\n")
    assert problemas_de_ids_citados(repo, EXISTENTES) == [f"{NO_EXISTE}: {DOC}:3: {INEXISTENTE}"]


@pytest.mark.contract
def test_un_id_declarado_con_motivo_y_citado_pasa(tmp_path: Path) -> None:
    texto = (
        _bloque(f"{INEXISTENTE} — salida de una copia desechable") + f"\nCuerpo: {INEXISTENTE}.\n"
    )
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == []


@pytest.mark.contract
def test_la_declaracion_solo_exime_en_su_documento(tmp_path: Path) -> None:
    texto = _bloque(f"{INEXISTENTE} — motivo") + f"\n{INEXISTENTE}\n"
    repo = _doc(tmp_path, texto)
    _doc(tmp_path, f"Otro documento que cita {INEXISTENTE}.\n", "docs/OTRO.md")
    assert problemas_de_ids_citados(repo, EXISTENTES) == [
        f"{NO_EXISTE}: docs/OTRO.md:1: {INEXISTENTE}"
    ]


@pytest.mark.contract
def test_un_id_declarado_que_si_existe_falla(tmp_path: Path) -> None:
    texto = _bloque(f"{EXISTE} — lo creia inventado") + f"\n{EXISTE}\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{DECLARADO_Y_EXISTE}: {DOC}:2: {EXISTE}"
    ]


@pytest.mark.contract
def test_un_id_declarado_y_no_citado_falla(tmp_path: Path) -> None:
    texto = _bloque(f"{INEXISTENTE} — motivo") + "\nEl cuerpo no lo cita.\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{DECLARADO_Y_NO_CITADO}: {DOC}:2: {INEXISTENTE}"
    ]


@pytest.mark.contract
def test_un_id_que_aparece_solo_en_su_bloque_de_declaracion_falla(tmp_path: Path) -> None:
    """La mencion dentro del propio bloque NO cuenta como cita: si contara, la regla de la
    declaracion muerta no podria fallar nunca. Con el id repetido dos veces en el bloque."""
    texto = "Titulo\n\n" + _bloque(f"{INEXISTENTE} — motivo que nombra {INEXISTENTE}")
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{DECLARADO_Y_NO_CITADO}: {DOC}:4: {INEXISTENTE}"
    ]


@pytest.mark.contract
@pytest.mark.parametrize(
    "linea", [INEXISTENTE, f"{INEXISTENTE} — ", f"{INEXISTENTE} - motivo con guion"]
)
def test_un_id_declarado_sin_motivo_falla(tmp_path: Path, linea: str) -> None:
    """Sin motivo la declaracion no vale: sale mal formada Y el id queda sin declarar."""
    texto = _bloque(linea) + f"\n{INEXISTENTE}\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{MAL_FORMADA}: {DOC}:2: {INEXISTENTE} sin motivo (`id — motivo`)",
        f"{NO_EXISTE}: {DOC}:5: {INEXISTENTE}",
    ]


@pytest.mark.contract
def test_una_linea_de_declaracion_sin_id_falla(tmp_path: Path) -> None:
    texto = _bloque("no-es-un-id — motivo")
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{MAL_FORMADA}: {DOC}:2: linea sin un id al principio"
    ]


@pytest.mark.contract
def test_un_bloque_sin_cerrar_falla(tmp_path: Path) -> None:
    texto = f"> ```ids-inexistentes\n> {INEXISTENTE} — motivo\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES)[0] == (
        f"{MAL_FORMADA}: {DOC}: bloque sin cerrar"
    )


@pytest.mark.contract
def test_lo_que_parece_un_id_y_no_lo_es_segun_fuente_se_ignora(tmp_path: Path) -> None:
    """Controles: ni `ADR-12345` ni `ADR-0001x` ni `ev-v1-12345-0000aaaa` son ids para FUENTE."""
    texto = "ADR-12345 · ADR-0001x · ev-v1-12345-0000aaaa · fb-X-0000aaaa · ev-*\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == []


@pytest.mark.contract
def test_claude_y_project_state_estan_en_el_alcance(tmp_path: Path) -> None:
    for nombre in ("CLAUDE.md", "PROJECT_STATE.md"):
        _doc(tmp_path, f"cita {INEXISTENTE}\n", nombre)
    assert problemas_de_ids_citados(tmp_path, EXISTENTES) == [
        f"{NO_EXISTE}: CLAUDE.md:1: {INEXISTENTE}",
        f"{NO_EXISTE}: PROJECT_STATE.md:1: {INEXISTENTE}",
    ]


@pytest.mark.contract
def test_el_bloque_tambien_vale_fuera_de_un_recuadro(tmp_path: Path) -> None:
    texto = _bloque(f"{INEXISTENTE} — motivo", cita=False) + f"\n{INEXISTENTE}\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto, "PROJECT_STATE.md"), EXISTENTES) == []


@pytest.mark.contract
def test_dos_bloques_en_un_documento_fallan(tmp_path: Path) -> None:
    texto = (
        _bloque(f"{INEXISTENTE} — uno") + _bloque(f"{INEXISTENTE} — otro") + f"\n{INEXISTENTE}\n"
    )
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == [
        f"{MAL_FORMADA}: {DOC}:4: segundo bloque (uno por documento)"
    ]


@pytest.mark.contract
def test_un_ejemplo_indentado_como_codigo_no_abre_un_bloque(tmp_path: Path) -> None:
    """Con 4 espacios o mas la linea es CODIGO (CommonMark): un documento puede ensenar la
    sintaxis sin declarar nada. El informe de esta rama lo hace, y la primera version del parser
    lo leia como un segundo bloque."""
    ejemplo = "\n".join(
        ["Asi se escribe:", "", "    ```ids-inexistentes", "    <id> — <motivo>", "    ```"]
    )
    texto = _bloque(f"{INEXISTENTE} — motivo") + f"\n{INEXISTENTE}\n\n" + ejemplo + "\n"
    assert problemas_de_ids_citados(_doc(tmp_path, texto), EXISTENTES) == []
