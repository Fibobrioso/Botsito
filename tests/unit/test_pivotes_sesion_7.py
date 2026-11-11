"""El pivote de la sesion 7, pre-registrado (ADR-0093 §6; `docs/plan/PIVOTES-SESION-7.yaml`).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit. Ademas se lee con el lector estricto y se comprueban las
cifras de la linea base, los dos minimos, las tres salidas y la contingencia, y un test rompe a
proposito con un minimo cambiado (rama `trabajo/preparacion-sesion-7`, F2).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "PIVOTES-SESION-7.yaml"
SHA256 = "cef25e632b8edb529968a2036b5b43c91e0138e57650bcf3d97f3e5776797eef"

SALIDAS = ("se_cumplen_los_dos", "se_cumple_uno", "no_se_cumple_ninguno")


def _sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def problemas(doc: Any) -> list[str]:
    """Lo que no casa con el pre-registro de D5: las cifras, el mes y las tres salidas."""
    if not isinstance(doc, dict):
        return ["el yaml no es un mapa"]
    salida: list[str] = []
    if doc.get("mes") != "2026-07":
        salida.append("el mes no es 2026-07")
    if doc.get("decision") != "ADR-0093":
        salida.append("no cita ADR-0093")
    base = doc.get("linea_base") or {}
    esperadas = {
        "parejas_de_julio": 14,
        "operaciones_de_mas_de_julio": 39,
        "operaciones_de_mas_de_julio_p5": 37,
        "operaciones_de_mas_de_julio_p6": 2,
    }
    for clave, valor in esperadas.items():
        if base.get(clave) != valor:
            salida.append(f"linea_base.{clave} no es {valor}")
    if base.get("operaciones_de_mas_de_julio_p5", 0) + base.get(
        "operaciones_de_mas_de_julio_p6", 0
    ) != base.get("operaciones_de_mas_de_julio"):
        salida.append("P5 + P6 no da las operaciones de mas")
    minimos = doc.get("minimos") or {}
    if minimos.get("minimo_1_parejas_de_julio_al_menos") != 19:
        salida.append("el minimo 1 no es 19")
    if minimos.get("minimo_2_operaciones_de_mas_de_julio_como_mucho") != 33:
        salida.append("el minimo 2 no es 33")
    if tuple(doc.get("salidas") or {}) != SALIDAS:
        salida.append("las salidas no son las tres de D5, en su orden")
    for clave in ("que_se_mide", "contingencia", "por_que", "lo_visto", "adr_0092_6"):
        if not str(doc.get(clave) or "").strip():
            salida.append(f"falta {clave}")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_las_cifras_y_las_salidas_son_las_de_d5() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_un_minimo_cambiado_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: el minimo 1 a 18 cambia el sha256 y lo rechaza la comprobacion."""
    original = RUTA.read_bytes()
    texto = original.decode("utf-8")
    assert texto.count("minimo_1_parejas_de_julio_al_menos: 19\n") == 1
    mutado = tmp_path / "PIVOTES-SESION-7.yaml"
    mutado.write_bytes(
        texto.replace(
            "minimo_1_parejas_de_julio_al_menos: 19\n", "minimo_1_parejas_de_julio_al_menos: 18\n"
        ).encode("utf-8")
    )
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["el minimo 1 no es 19"]


def test_el_otro_minimo_cambiado_tambien_rompe(tmp_path: Path) -> None:
    texto = RUTA.read_text(encoding="utf-8")
    mutado = tmp_path / "PIVOTES-SESION-7.yaml"
    mutado.write_text(
        texto.replace("_como_mucho: 33\n", "_como_mucho: 34\n"), encoding="utf-8", newline="\n"
    )
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["el minimo 2 no es 33"]
