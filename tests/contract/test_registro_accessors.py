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
