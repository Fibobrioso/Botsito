"""StrategySpec, glosario y manifiesto (F11, ADR-0013)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.spec.manifiesto import (
    ManifiestoSpecError,
    cargar_manifiesto,
    estructura_para_hash,
    hash_de,
)
from botsito.spec.modelo import SpecError, cargar_glosario, cargar_reglas, comprobar_contra

REPO = Path(__file__).resolve().parents[2]
FB = "fb-2026-09-09-sesion-01-846fb0d7"


def _regla(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "id": "RN-001",
        "titulo": "una regla",
        "cuando": "el precio alcanza la liquidez de M15",
        "entonces": "se opera segun stop_fraccion_caja",
        "parametros": ["stop_fraccion_caja"],
        "cita": FB,
        "literal": "lo dijo asi",
        "estado": "VIGENTE",
    }
    d.update(cambios)
    return d


def _escribir(tmp_path: Path, reglas: list[dict[str, Any]]) -> Path:
    ruta = tmp_path / "strategy_spec.yaml"
    ruta.write_text(
        yaml.safe_dump({"version_esquema": 1, "reglas": reglas}, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )
    return ruta


def test_una_regla_no_puede_llevar_un_valor_de_negocio(tmp_path: Path) -> None:
    """El valor vive en el registro: aqui solo va el nombre del parametro."""
    with pytest.raises(SpecError, match="contiene la cifra"):
        cargar_reglas(_escribir(tmp_path, [_regla(entonces="el stop va al 0,8 de la caja")]))
    with pytest.raises(SpecError, match="contiene la cifra"):
        cargar_reglas(_escribir(tmp_path, [_regla(cuando="son las 15:00")]))


def test_los_nombres_con_digitos_si_pasan(tmp_path: Path) -> None:
    """`M15`, `H4` y `liquidez_m15_criterio_toma` son nombres, no valores."""
    reglas = cargar_reglas(
        _escribir(
            tmp_path,
            [
                _regla(
                    cuando="el precio toma la liquidez de M15 dentro de la vela H4",
                    entonces="se aplica liquidez_m15_criterio_toma",
                )
            ],
        )
    )
    assert len(reglas) == 1


def test_el_literal_si_puede_llevar_cifras(tmp_path: Path) -> None:
    """Son las palabras del trader; prohibirselas seria censurar la cita."""
    reglas = cargar_reglas(_escribir(tmp_path, [_regla(literal="se reduce al 0.80")]))
    assert reglas[0].literal == "se reduce al 0.80"


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"id": "R-1"}, "formato RN-NNN"),
        ({"estado": "PROVISIONAL"}, "estado"),
        ({"cita": "no-es-un-id"}, "no es un id"),
        ({"parametros": "stop_fraccion_caja"}, "lista de nombres"),
        ({"titulo": "  "}, "falta 'titulo'"),
    ],
)
def test_esquema_estricto(tmp_path: Path, cambio: dict[str, Any], mensaje: str) -> None:
    with pytest.raises(SpecError, match=mensaje):
        cargar_reglas(_escribir(tmp_path, [_regla(**cambio)]))


def test_ids_repetidos(tmp_path: Path) -> None:
    with pytest.raises(SpecError, match="id repetido"):
        cargar_reglas(_escribir(tmp_path, [_regla(), _regla()]))


def test_campos_desconocidos(tmp_path: Path) -> None:
    with pytest.raises(SpecError, match="campos desconocidos"):
        cargar_reglas(_escribir(tmp_path, [{**_regla(), "prioridad": 3}]))


def test_comprobar_contra_el_registro_y_las_citas(tmp_path: Path) -> None:
    reglas = cargar_reglas(_escribir(tmp_path, [_regla()]))
    assert comprobar_contra(reglas, [], {"stop_fraccion_caja"}, {FB}) == []
    problemas = comprobar_contra(reglas, [], set(), set())
    assert any("no esta en el registro" in p for p in problemas)
    assert any("no existe" in p for p in problemas)


# --- la spec real ---


def test_la_spec_real_carga_y_cita_lo_que_existe() -> None:
    from botsito.config.registro import cargar_registro
    from botsito.evidence.modelo import cargar_evidencia
    from botsito.feedback.modelo import cargar_feedback
    from botsito.spec.modelo import FICHERO_GLOSARIO, FICHERO_SPEC

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    terminos = cargar_glosario(REPO / FICHERO_GLOSARIO)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    citas = {i.id for i in cargar_evidencia(REPO / "knowledge" / "evidence")} | {
        r.id for r in cargar_feedback(REPO / "knowledge" / "feedback")
    }
    assert comprobar_contra(reglas, terminos, set(registro.nombres()), citas) == []
    assert any(r.vigente for r in reglas) and any(not r.vigente for r in reglas)


def test_toda_regla_vigente_usa_parametros_con_valor() -> None:
    """Una regla vigente que nombra un UNKNOWN no se podria ejecutar."""
    from botsito.config.registro import Estado, cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC

    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    for r in cargar_reglas(REPO / FICHERO_SPEC):
        if not r.vigente:
            continue
        for nombre in r.parametros:
            p = registro.parametros[nombre]
            assert p.estado is not Estado.UNKNOWN, f"{r.id} usa {nombre}, que sigue UNKNOWN"


# --- manifiesto ---


def _copia_de_la_spec(tmp_path: Path) -> Path:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    for nombre in ("parametros.yaml", "strategy_spec.yaml", "glossary.yaml"):
        origen = REPO / "knowledge" / "spec" / nombre
        (tmp_path / "knowledge" / "spec" / nombre).write_text(
            origen.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
        )
    return tmp_path


def test_el_hash_es_reproducible() -> None:
    assert hash_de(REPO) == hash_de(REPO)
    estructura = estructura_para_hash(REPO)
    assert {p["nombre"] for p in estructura["parametros"]}
    assert all(isinstance(p.get("estado"), str) for p in estructura["parametros"])


def test_el_hash_cubre_el_registro_no_solo_las_reglas(tmp_path: Path) -> None:
    """Si el registro quedara fuera, cambiar el stop no cambiaria la version de la spec y el
    pre-vuelo de la demo daria verde con otra estrategia (MASTER_PLAN H.2)."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "parametros.yaml"
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace('valor: "0.8"', 'valor: "0.75"', 1),
        encoding="utf-8",
        newline="\n",
    )
    assert hash_de(repo) != antes


def test_el_hash_cubre_el_estado_y_la_fuente(tmp_path: Path) -> None:
    """Pasar de CONFIRMED a DEFAULT_AMBIGUOUS no cambia el valor, pero si lo que la spec afirma."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "parametros.yaml"
    # Linea a linea y no con `replace`: las primeras coincidencias de "estado: CONFIRMED" estan
    # dentro del ejemplo COMENTADO de la cabecera, y el hash ignora los comentarios a proposito.
    # Un replace ciego cambiaria el comentario y el test afirmaria lo contrario de lo que cree.
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    for i, linea in enumerate(lineas):
        if linea == "    estado: CONFIRMED":
            lineas[i] = "    estado: DEFAULT_AMBIGUOUS"
            break
    else:  # pragma: no cover
        pytest.fail("el registro real no tiene ningun parametro CONFIRMED")
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    assert hash_de(repo) != antes


def test_un_comentario_no_cambia_el_hash(tmp_path: Path) -> None:
    """Se hashea la estructura, no los bytes: reordenar un comentario no es cambiar la spec."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    ruta.write_text(
        "# comentario nuevo\n" + ruta.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    assert hash_de(repo) == antes


def test_el_manifiesto_real_esta_al_dia() -> None:
    from botsito.spec.manifiesto import FICHERO_MANIFIESTO
    from botsito.spec.manifiesto import comprobar as comprobar_manifiesto

    assert comprobar_manifiesto(REPO, REPO / FICHERO_MANIFIESTO) == []
    doc = cargar_manifiesto(REPO / FICHERO_MANIFIESTO)
    assert len(doc["cubre"]) == 3
    # la version sube con cada cambio de la spec: se comprueba el formato, no el numero
    assert re.fullmatch(r"\d+\.\d+\.\d+", str(doc["spec_version"]))


def test_manifiesto_mal_escrito(tmp_path: Path) -> None:
    ruta = tmp_path / "spec_manifest.yaml"
    ruta.write_text(
        'spec_version: "1"\nhash: abc\ngenerado_el: "x"\ncubre: [a, b, c]\n',
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ManifiestoSpecError, match="semver"):
        cargar_manifiesto(ruta)
