"""`knowledge/simulador/llenado.yaml` (ADR-0051 §6): lectura estricta sobre ficheros SINTETICOS
en `tmp_path`, el spread supuesto resuelto por hora local, y el fichero real si existe."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from botsito.data.velas import a_minuto
from botsito.engine.simulador_config import (
    FICHERO_LLENADO,
    ConfigSimuladorError,
    cargar_config_llenado,
)

RAIZ = Path(__file__).resolve().parents[2]
BASE = """
adr: ADR-0051
limite_llena_al_toque: false
deslizamiento_fijo_puntos: 0
deslizamiento_motivo: no hay medida; solo el de hueco de los ticks
spread:
  fuente: prueba sintetica
  huso: America/New_York
  por_hora_local: {8: 7, 9: 6}
  fuera_de_ventana: 20
"""


def _escribir(tmp_path: Path, texto: str) -> Path:
    ruta = tmp_path / "llenado.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def test_carga_y_resuelve_el_spread_por_hora_local(tmp_path: Path) -> None:
    c = cargar_config_llenado(_escribir(tmp_path, BASE))
    assert c.limite_llena_al_toque is False and c.deslizamiento_fijo_puntos == 0
    cfg = c.configuracion()
    # 13:30Z es 08:30 en Nueva York en enero (UTC-5): hora 8 -> 7 puntos; 20:00Z es 15:00 -> fuera
    assert cfg.spread_supuesto(a_minuto(datetime(2030, 1, 15, 13, 30, tzinfo=UTC))) == 7
    assert cfg.spread_supuesto(a_minuto(datetime(2030, 1, 15, 20, 0, tzinfo=UTC))) == 20


@pytest.mark.parametrize(
    ("viejo", "nuevo", "mensaje"),
    [
        ("limite_llena_al_toque: false", 'limite_llena_al_toque: "no"', "sin comillas"),
        ("deslizamiento_fijo_puntos: 0", "deslizamiento_fijo_puntos: -1", "no negativo"),
        (
            "deslizamiento_motivo: no hay medida; solo el de hueco de los ticks",
            "deslizamiento_motivo: ''",
            "motivo",
        ),
        ("  fuente: prueba sintetica\n", "  fuente: ''\n", "fuente"),
        ("  huso: America/New_York", "  huso: Marte/Olympus", "huso desconocido"),
        ("{8: 7, 9: 6}", "{24: 7}", "hora local invalida"),
        ("{8: 7, 9: 6}", "{8: -1}", "no negativo"),
        ("adr: ADR-0051", "adr: nota", "ADR-NNNN"),
        ("  fuera_de_ventana: 20\n", "", "exactamente"),
    ],
)
def test_lectura_estricta(tmp_path: Path, viejo: str, nuevo: str, mensaje: str) -> None:
    assert BASE.count(viejo) == 1
    with pytest.raises(ConfigSimuladorError, match=mensaje):
        cargar_config_llenado(_escribir(tmp_path, BASE.replace(viejo, nuevo)))


def test_sin_fichero_no_corre(tmp_path: Path) -> None:
    with pytest.raises(ConfigSimuladorError, match="no existe"):
        cargar_config_llenado(tmp_path / "no.yaml")


def test_el_fichero_real_carga_si_existe() -> None:
    ruta = RAIZ / FICHERO_LLENADO
    if not ruta.exists():
        pytest.skip("todavia no hay llenado.yaml en el repositorio")
    c = cargar_config_llenado(ruta)
    assert c.adr == "ADR-0051" and "ticks" in c.spread_fuente
    assert set(c.spread_por_hora_local) >= {7, 8, 9, 10, 11, 12, 13, 14}
