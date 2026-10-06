"""G1 (trabajo/guardias-citas): un supersedido solo se nombra junto a su sustituto.

Cada test rompe la guardia a proposito en un `knowledge/spec/` TEMPORAL (`tmp_path`), nunca en el
repositorio real. Los cuatro primeros son los que pidio el consultor (respuesta a la fase 0,
punto 2); los demas fijan los bordes de la condicion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from botsito.validation import citas_supersedidas
from botsito.validation.citas_supersedidas import citas_a_supersedidos, sustitutos

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
    return citas_a_supersedidos(repo, ITEMS)[0]


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
    fallos = citas_a_supersedidos(repo, items)[0]
    assert len(fallos) == 1
    assert f"supersedido por {NUEVO} (vigente: {tercero})" in fallos[0]


def test_la_lista_de_excluidos_esta_vacia() -> None:
    """Excluir un fichero de G1 es una decision que se ve en el diff: hoy no hay ninguno."""
    assert citas_supersedidas.EXCLUIDOS == ()


def test_sin_knowledge_spec_no_hay_nada_que_mirar(tmp_path: Path) -> None:
    assert citas_a_supersedidos(tmp_path, ITEMS) == ([], 0)
