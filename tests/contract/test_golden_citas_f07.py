"""Golden de F07: las citas de referencia (informe de investigacion + marcas de F04) existen como
evidencia activa (tabla A del plan). Se salta mientras no haya items (ronda 1)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.evidence.modelo import activos, cargar_evidencia, parse_tiempo
from botsito.evidence.verificacion import tokens

REPO = Path(__file__).resolve().parents[2]
GOLDEN = REPO / "tests" / "golden" / "f07_citas_referencia.yaml"
TOLERANCIA_S = 30.0


def _entradas() -> list[dict[str, Any]]:
    doc = yaml.safe_load(GOLDEN.read_text(encoding="utf-8"))
    return [e for e in doc["referencias"] if not e.get("descartada")]


def _contiene(cita: str, fragmento: str) -> bool:
    a, b = tokens(cita.replace("[...]", " ")), tokens(fragmento)
    return any(a[i : i + len(b)] == b for i in range(len(a) - len(b) + 1))


def test_golden_bien_formado() -> None:
    entradas = _entradas()
    assert len(entradas) >= 30
    for e in entradas:
        assert e["modalidad"] in ("audio", "pantalla")
        assert ("fragmento" in e) == (e["modalidad"] == "audio")
        assert ("referencia" in e) == (e["modalidad"] == "pantalla")
        parse_tiempo(e["t0"])


def test_las_citas_de_referencia_existen_como_evidencia() -> None:
    items = activos(cargar_evidencia(REPO / "knowledge" / "evidence"))
    if not items:
        pytest.skip("sin evidencia todavia (ronda 1 de F07)")
    faltan: list[str] = []
    for e in _entradas():
        t0 = parse_tiempo(e["t0"])
        candidatos = [
            i for i in items if i.video_id == e["video_id"] and abs(i.t0_s - t0) <= TOLERANCIA_S
        ]
        if e["modalidad"] == "audio":
            ok = any(_contiene(i.cita_literal, e["fragmento"]) for i in candidatos)
        else:
            ok = any(e["referencia"] in i.fotogramas for i in candidatos)
        if not ok:
            faltan.append(e["marca"])
    assert not faltan, f"citas de referencia sin evidencia: {faltan}"
