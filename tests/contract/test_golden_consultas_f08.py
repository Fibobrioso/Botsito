"""Golden de F08: las 15 consultas de referencia devuelven su item de evidencia (siempre) y sus
segmentos (cuando las crudas estan en la maquina). Ver tests/golden/f08_consultas_referencia.yaml.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.config.ajustes import carpeta_datos
from botsito.retrieval.consultas import buscar
from botsito.retrieval.indice import TIPO_EVIDENCIA, TIPO_SEGMENTO, construir_indice

REPO = Path(__file__).resolve().parents[2]
FIXTURE = REPO / "tests" / "golden" / "f08_consultas_referencia.yaml"


def _consultas() -> list[dict[str, Any]]:
    doc = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    return list(doc["consultas"])


@pytest.mark.contract
def test_golden_bien_formado() -> None:
    consultas = _consultas()
    assert len(consultas) == 15
    for c in consultas:
        assert set(c) <= {"consulta", "esperado", "ambiguedad", "segmentos_min", "nota"}
        assert str(c["consulta"]).strip() and c["esperado"].startswith("ev-")
        assert isinstance(c["segmentos_min"], int) and c["segmentos_min"] >= 0


@pytest.mark.contract
def test_las_consultas_de_referencia_devuelven_su_item() -> None:
    indice = construir_indice(REPO, carpeta_datos(REPO))
    con_crudas = bool(indice.segmentos)
    existentes = {it.id for it in indice.items}
    fallos: list[str] = []
    for c in _consultas():
        if c["esperado"] not in existentes:
            fallos.append(f"{c['consulta']!r}: {c['esperado']} no existe")
            continue
        r = buscar(indice, str(c["consulta"]))
        fuentes = {x.fuente for x in r.resultados if x.tipo == TIPO_EVIDENCIA}
        if c["esperado"] not in fuentes:
            fallos.append(f"{c['consulta']!r}: no devuelve {c['esperado']}")
        if con_crudas:
            segmentos = sum(1 for x in r.resultados if x.tipo == TIPO_SEGMENTO)
            if segmentos < c["segmentos_min"]:
                fallos.append(f"{c['consulta']!r}: {segmentos} segmentos < {c['segmentos_min']}")
        for x in r.resultados:
            assert x.fuente.startswith(("ev-", "tr-", "fr-")), x.fuente
    assert fallos == [], fallos
