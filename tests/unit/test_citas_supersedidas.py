"""G1 (trabajo/guardias-citas): un supersedido solo se nombra junto a su sustituto.

Cada test rompe la guardia a proposito en un `knowledge/spec/` TEMPORAL (`tmp_path`), nunca en el
repositorio real. Los cuatro primeros son los que pidio el consultor (respuesta a la fase 0,
punto 2); los demas fijan los bordes de la condicion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

from botsito.validation import citas_supersedidas
from botsito.validation.citas_supersedidas import Excepcion, citas_a_supersedidos, sustitutos

VIEJO = "ev-v4-001207-0c4ffd4b"
NUEVO = "ev-v6-021939-b430a110"
OTRO = "ev-v1-000620-0f7dea14"


@dataclass(frozen=True)
class _Item:
    id: str
    supersede: str | None = None


ITEMS = [_Item(VIEJO), _Item(NUEVO, supersede=VIEJO), _Item(OTRO)]


def _spec(tmp_path: Path, nombre: str, texto: str) -> Path:
    ruta = tmp_path / "knowledge" / "spec" / nombre
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return tmp_path


def _fallos(repo: Path) -> list[str]:
    return citas_a_supersedidos(repo, ITEMS, excepciones=())[0]


def test_un_supersedido_en_el_campo_evidencia_falla(tmp_path: Path) -> None:
    repo = _spec(
        tmp_path,
        "ambiguedades.yaml",
        f"ambiguedades:\n  - id: A-11\n    evidencia:\n      - {VIEJO}\n      - {OTRO}\n",
    )
    assert _fallos(repo) == [
        f"knowledge/spec/ambiguedades.yaml:4: nombra {VIEJO}, supersedido por {NUEVO}; un "
        "supersedido solo aparece en el mismo valor o la misma linea de comentario que su "
        "sustituto"
    ]


def test_el_mismo_id_en_una_nota_sin_su_sustituto_falla(tmp_path: Path) -> None:
    repo = _spec(
        tmp_path,
        "strategy_spec.yaml",
        f"reglas:\n  - id: RN-1\n    notas: >-\n      lo dijo en v4 ({VIEJO}), y nada mas\n",
    )
    assert len(_fallos(repo)) == 1


def test_con_su_sustituto_en_la_misma_nota_pasa(tmp_path: Path) -> None:
    repo = _spec(
        tmp_path,
        "strategy_spec.yaml",
        f"reglas:\n  - id: RN-1\n    notas: >-\n      lo dijo en v4 ({VIEJO}), y lo\n"
        f"      sustituye {NUEVO} en otra linea del mismo valor\n",
    )
    assert _fallos(repo) == []


def test_en_un_fichero_nuevo_bajo_knowledge_spec_falla(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "nuevo_fichero.yaml", f"cosas:\n  cita: {VIEJO}\n")
    assert [f.split(":", 1)[0] for f in _fallos(repo)] == ["knowledge/spec/nuevo_fichero.yaml"]


def test_un_fichero_nuevo_en_una_subcarpeta_tambien_se_vigila(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "sub/otro.yaml", f"cita: {VIEJO}\n")
    assert len(_fallos(repo)) == 1


def test_un_fichero_que_no_es_yaml_no_tiene_valores_y_falla_aunque_nombre_al_sustituto(
    tmp_path: Path,
) -> None:
    repo = _spec(tmp_path, "README.md", f"{VIEJO} lo sustituye {NUEVO}\n")
    assert len(_fallos(repo)) == 1


def test_un_yaml_ilegible_falla_como_si_no_fuera_yaml(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "roto.yaml", f"a: [\n  {VIEJO} {NUEVO}\n")
    assert len(_fallos(repo)) == 1


def test_en_la_misma_linea_de_comentario_que_su_sustituto_pasa(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "a.yaml", f"a: 1  # {VIEJO} esta supersedido por {NUEVO}\n")
    assert _fallos(repo) == []


def test_en_un_comentario_con_el_sustituto_en_la_linea_siguiente_falla(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "a.yaml", f"# {VIEJO} esta\n# supersedido por {NUEVO}\na: 1\n")
    assert len(_fallos(repo)) == 1


def test_el_sustituto_en_otro_valor_no_vale(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "a.yaml", f"evidencia:\n  - {VIEJO}\n  - {NUEVO}\n")
    assert len(_fallos(repo)) == 1


def test_un_id_vigente_o_el_sustituto_solos_pasan(tmp_path: Path) -> None:
    repo = _spec(tmp_path, "a.yaml", f"evidencia:\n  - {NUEVO}\n  - {OTRO}\n# {OTRO}\n")
    assert _fallos(repo) == []


def test_en_una_cadena_vale_cualquier_sustituto_y_el_mensaje_da_el_vigente(tmp_path: Path) -> None:
    tercero = "ev-v9-000001-0000000a"
    items = [*ITEMS, _Item(tercero, supersede=NUEVO)]
    assert sustitutos(items)[VIEJO] == [NUEVO, tercero]
    repo = _spec(tmp_path, "a.yaml", f"notas: {VIEJO} lo sustituye {tercero}\ncita: {VIEJO}\n")
    fallos = citas_a_supersedidos(repo, items, excepciones=())[0]
    assert len(fallos) == 1
    assert f"supersedido por {NUEVO} (vigente: {tercero})" in fallos[0]


def test_la_lista_de_excluidos_esta_vacia() -> None:
    """Excluir un fichero de G1 es una decision que se ve en el diff: hoy no hay ninguno."""
    assert citas_supersedidas.EXCLUIDOS == ()


def test_sin_knowledge_spec_no_hay_nada_que_mirar(tmp_path: Path) -> None:
    assert citas_a_supersedidos(tmp_path, ITEMS, excepciones=()) == ([], 0)


# --- La excepcion de A-11 (respuesta del consultor del 2026-10-06 a la parada de A-11) ---

OTRO_VIEJO = "ev-v4-011351-74b8bb39"
OTRO_NUEVO = "ev-v6-000732-f7189541"
ITEMS_DOS = [*ITEMS, _Item(OTRO_VIEJO), _Item(OTRO_NUEVO, supersede=OTRO_VIEJO)]


def _ambiguedades(tmp_path: Path, a11: list[str], a12: list[str] | None = None) -> Path:
    texto = "ambiguedades:\n  - id: A-11\n    evidencia:\n"
    texto += "".join(f"      - {e}\n" for e in a11)
    if a12 is not None:
        texto += "  - id: A-12\n    evidencia:\n" + "".join(f"      - {e}\n" for e in a12)
    return _spec(tmp_path, "ambiguedades.yaml", texto)


def test_la_excepcion_es_exactamente_un_par() -> None:
    esperada = Excepcion(
        "A-11",
        VIEJO,
        "respaldo de A-11 pendiente de decisión del consultor, GUARDIAS-CITAS.md §8; 2026-10-06",
    )
    excepciones = citas_supersedidas.EXCEPCIONES
    assert excepciones == (esperada,)


def test_la_excepcion_deja_pasar_su_par(tmp_path: Path) -> None:
    repo = _ambiguedades(tmp_path, [VIEJO, OTRO])
    assert citas_a_supersedidos(repo, ITEMS_DOS)[0] == []


def test_la_excepcion_no_cubre_otro_supersedido_de_a11(tmp_path: Path) -> None:
    repo = _ambiguedades(tmp_path, [VIEJO, OTRO_VIEJO])
    fallos = citas_a_supersedidos(repo, ITEMS_DOS)[0]
    assert len(fallos) == 1
    assert f"nombra {OTRO_VIEJO}" in fallos[0]


def test_la_excepcion_no_cubre_el_mismo_id_en_otra_ambiguedad(tmp_path: Path) -> None:
    repo = _ambiguedades(tmp_path, [VIEJO], a12=[VIEJO])
    fallos = citas_a_supersedidos(repo, ITEMS_DOS)[0]
    assert fallos == [
        f"knowledge/spec/ambiguedades.yaml:7: nombra {VIEJO}, supersedido por {NUEVO}; un "
        "supersedido solo aparece en el mismo valor o la misma linea de comentario que su "
        "sustituto"
    ]


def test_la_excepcion_no_cubre_el_par_en_otro_fichero_sin_objeto_a11(tmp_path: Path) -> None:
    _ambiguedades(tmp_path, [VIEJO])
    repo = _spec(tmp_path, "otro.yaml", f"cita: {VIEJO}\n")
    fallos = citas_a_supersedidos(repo, ITEMS_DOS)[0]
    assert [f.split(":", 1)[0] for f in fallos] == ["knowledge/spec/otro.yaml"]


def test_la_excepcion_no_cubre_un_comentario(tmp_path: Path) -> None:
    repo = _spec(
        tmp_path,
        "ambiguedades.yaml",
        f"ambiguedades:\n  - id: A-11\n    # {VIEJO}\n    evidencia:\n      - {VIEJO}\n",
    )
    fallos = citas_a_supersedidos(repo, ITEMS_DOS)[0]
    assert [f.split(":", 2)[1] for f in fallos] == ["3"]


def test_caducidad_la_excepcion_sin_uso_falla(tmp_path: Path) -> None:
    """Si A-11 deja de citar el id, la excepcion ya no hace falta: G1 falla hasta que se quite."""
    repo = _ambiguedades(tmp_path, [OTRO])
    assert citas_a_supersedidos(repo, ITEMS_DOS)[0] == [
        f"excepcion de G1 sin uso: A-11 ya no cita {VIEJO}; se quita de EXCEPCIONES "
        "(src/botsito/validation/citas_supersedidas.py)"
    ]


def test_caducidad_en_el_repositorio_real(repo: Path) -> None:
    """G1 sobre el repositorio real: sin fallos con la excepcion, y la excepcion HACE FALTA. Sin
    ella, la unica aparicion que falla es la de A-11 (`ambiguedades.yaml`); el dia que A-11 deje
    de citar el id, esa asercion falla y la excepcion se quita (hallazgo b2 del revisor)."""
    from botsito.evidence.modelo import cargar_evidencia

    items = cargar_evidencia(repo / "knowledge" / "evidence")
    fallos, vigilados = citas_a_supersedidos(repo, items)
    assert fallos == [], "\n".join(fallos)
    assert vigilados > 0
    sin_excepcion = citas_a_supersedidos(repo, items, excepciones=())[0]
    assert len(sin_excepcion) == 1, sin_excepcion
    assert sin_excepcion[0].startswith("knowledge/spec/ambiguedades.yaml:")
    assert "nombra ev-v4-001207-0c4ffd4b" in sin_excepcion[0]


def test_knowledge_validate_lleva_g1(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """G1 esta conectada: si la guardia da un fallo, `knowledge validate` sale con ERROR."""
    from botsito.validation import knowledge

    def _rota(_repo: Path, _items: object) -> tuple[list[str], int]:
        return ["knowledge/spec/x.yaml:1: fallo de prueba"], 1

    monkeypatch.setattr(citas_supersedidas, "citas_a_supersedidos", _rota)
    codigo, salida = knowledge.validar(repo)
    assert codigo == 1
    assert "ERROR: spec: knowledge/spec/x.yaml:1: fallo de prueba" in salida


def test_sin_el_item_supersedido_la_excepcion_no_tiene_a_que_aplicarse(tmp_path: Path) -> None:
    """Un `knowledge/` minimo (los de los tests de la CLI) no tiene el item: no hay caducidad."""
    repo = _ambiguedades(tmp_path, [OTRO])
    assert citas_a_supersedidos(repo, [_Item(OTRO)])[0] == []
