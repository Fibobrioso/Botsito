"""Cada `registro.<accesor>("nombre")` en src/ cita un parametro existente con ese tipo
(ADR-0006): un typo o un tipo cambiado se detecta aqui, no en produccion."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from botsito.config.registro import cargar_registro

ACCESORES = {
    "fraccion": "fraccion",
    "porcentaje": "porcentaje",
    "decimal": "decimal",
    "entero": "entero",
    "hora": "hora",
    "texto": "texto",
    # F11
    "opcion": "enum",
    "booleano": "booleano",
    "puntos": "puntos",
    "minutos": "minutos",
    "lotes": "lotes",
}


def _usos(repo: Path) -> list[tuple[str, str, str]]:
    usos: list[tuple[str, str, str]] = []
    for py in sorted((repo / "src" / "botsito").rglob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in ACCESORES
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in {"registro", "reg", "parametros"}
            ):
                usos.append((f"{py.name}:{node.lineno}", node.func.attr, node.args[0].value))
    return usos


@pytest.mark.contract
def test_accesores_del_registro_citan_parametros_existentes_con_su_tipo(repo: Path) -> None:
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    problemas: list[str] = []
    for donde, accesor, nombre in _usos(repo):
        p = registro.parametros.get(nombre)
        if p is None:
            problemas.append(f"{donde}: parametro {nombre!r} no existe en el registro")
        elif p.tipo != ACCESORES[accesor]:
            problemas.append(f"{donde}: {nombre} es {p.tipo}, se lee con .{accesor}()")
    assert problemas == [], problemas


def test_el_detector_ve_los_usos(tmp_path: Path) -> None:
    (tmp_path / "src" / "botsito").mkdir(parents=True)
    (tmp_path / "src" / "botsito" / "m.py").write_text(
        'x = registro.fraccion("stop_fraccion")\ny = reg.hora("inicio")\n', encoding="utf-8"
    )
    assert _usos(tmp_path) == [
        ("m.py:1", "fraccion", "stop_fraccion"),
        ("m.py:2", "hora", "inicio"),
    ]


def test_las_opciones_del_kit_y_del_registro_no_pueden_separarse(repo: Path) -> None:
    """`mapa_parametros.yaml` (F10) y el registro (F11) declaran las mismas listas cerradas.

    Las `opciones` deberian vivir solo en el registro, pero el paquete de la sesion 1 se genero
    con las del kit y `kit check` exige que ese paquete se reproduzca byte a byte: es la prueba de
    lo que se le pregunto al trader, y no puede cambiar. Asi que conviven, y esto impide lo unico
    que importa: que una de las dos se quede atras y el kit pregunte por una opcion que el
    registro rechaza. Deuda declarada para F13.
    """
    import yaml

    from botsito.config.registro import cargar_registro

    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    mapa = yaml.safe_load(
        (repo / "knowledge" / "cases" / "kit" / "mapa_parametros.yaml").read_text(encoding="utf-8")
    )
    problemas: list[str] = []
    for nombre, datos in (mapa.get("parametros") or {}).items():
        opciones_kit = (datos or {}).get("opciones")
        if opciones_kit is None:
            continue
        p = registro.parametros.get(nombre)
        if p is None:
            problemas.append(f"{nombre}: el kit lo nombra y el registro no lo tiene")
            continue
        if p.opciones is None:
            problemas.append(f"{nombre}: el kit declara opciones y en el registro no es un enum")
            continue
        if list(p.opciones) != list(opciones_kit):
            problemas.append(f"{nombre}: kit {list(opciones_kit)} != registro {list(p.opciones)}")
    assert not problemas, "; ".join(problemas)


def test_el_readme_de_la_spec_no_puede_llevar_cifras_viejas(repo: Path) -> None:
    """Las cifras de la spec se quedaron viejas TRES veces en dos dias.

    P8 las encontro desfasadas tres versiones, P11 vio que dejaron de cuadrar al aparecer el
    primer `DEFAULT_AMBIGUOUS`, y la tercera copia nacio desfasada porque `spec_version` subio dos
    veces mas antes del merge. La leccion no es "revisar mejor": una foto de un estado que cambia
    en cada commit no se pega a mano.

    De los documentos que las llevaban, solo UNO describe el presente sin mezcla: este README, que
    dice que contiene `knowledge/spec/` AHORA. El HANDOFF es una narracion con fechas -su seccion
    de F10 dice "registro con 24 parametros de estrategia en UNKNOWN", que era cierto entonces- asi
    que ahi la cifra se quito y se apunta al comando; los informes de validacion y los ADR son
    artefactos fechados y no se tocan.

    La guardia es pequena a proposito. Una que cazara tambien la narracion historica daria falsos
    positivos, y una guardia con falsos positivos se desactiva sola.
    """
    import re

    from botsito.config.registro import cargar_registro

    ruta = repo / "knowledge" / "spec" / "README.md"
    texto = " ".join(ruta.read_text(encoding="utf-8").split())
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    reales = {
        "": len(registro.parametros),
        "confirmados": sum(
            1 for p in registro.parametros.values() if p.estado.value == "CONFIRMED"
        ),
        "UNKNOWN": sum(1 for p in registro.parametros.values() if p.estado.value == "UNKNOWN"),
    }

    m = re.search(
        r"tiene (\d+) parametros: (\d+) confirmados, \d+ con un default \w+ y (\d+) UNKNOWN", texto
    )
    assert m, "el README dejo de declarar el recuento en la forma que esta guardia sabe leer"
    dichos = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    esperados = (reales[""], reales["confirmados"], reales["UNKNOWN"])
    assert dichos == esperados, f"el README dice {dichos} y el registro tiene {esperados}"


def test_el_handoff_no_pega_un_recuento_que_caduca(repo: Path) -> None:
    """El HANDOFF llevaba la copia que se quedo vieja tres veces; ahora apunta al comando."""
    texto = (repo / "docs" / "HANDOFF.md").read_text(encoding="utf-8")
    assert "`botsito spec status`" in texto
    assert "manifiesto 3.0.0" not in texto and "manifiesto 1.5.0" not in texto
