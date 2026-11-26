"""El manifiesto del historial de ticks de FTMO (`data/manifests/f17/`, esquema
`schema_f17_historial: 1` de `data/manifests/README.md`; rama `trabajo/f17-historial`, D4).

Esta rama solo lo define: se prueba con un manifiesto sintetico en un temporal, que pasa, y con
mutaciones que rompen a proposito. Si algun dia hay manifiestos de verdad en `data/manifests/f17/`,
el ultimo test los valida todos.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "scripts" / "leer_historial_f17.py"
CARPETA = RAIZ / "data" / "manifests" / "f17"


def _cargar() -> ModuleType:
    spec = importlib.util.spec_from_file_location("leer_historial_f17_m", GUION)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["leer_historial_f17_m"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


L = _cargar()
CONSTRUCCION = list(cargar_criterio(RAIZ).construccion)


def _manifiesto() -> dict[str, Any]:
    ficheros = [
        {
            "ruta": "f17/2026-04/F17_2026-04-15_ticks.csv",
            "tipo": "ticks",
            "bytes": 10,
            "sha256": "a" * 64,
            "filas": 2,
            "fin_de_linea": "CRLF",
        },
        {
            "ruta": "f17/2026-04/F17_2026-04-15_m1.csv",
            "tipo": "m1",
            "bytes": 10,
            "sha256": "b" * 64,
            "filas": 2,
            "fin_de_linea": "CRLF",
        },
        {
            "ruta": "f17/2026-04/F17_control_20261201_101500.csv",
            "tipo": "control",
            "bytes": 10,
            "sha256": "c" * 64,
            "filas": 20,
            "fin_de_linea": "CRLF",
        },
    ]
    return {
        "schema_f17_historial": 1,
        "dataset_id": f"f17-historial-2026-04-{L.sufijo_de(ficheros)}",
        "mes": "2026-04",
        "ficheros": ficheros,
        "dias": {"pedidos": 22, "con_ticks": 22, "sin_ticks": []},
        "primer_tick_msc_servidor": 1,
        "primera_m1_servidor_s": 1,
        "control": {
            "time_trade_server_s": 1,
            "time_gmt_s": 1,
            "desfase_servidor_gmt_min": 180,
            "cuadra": True,
        },
        "script": {
            "ruta": "tools/mql5/ExportarTicksFTMO.mq5",
            "version": "1.0",
            "sha256": "d" * 64,
            "commit": "0" * 8,
        },
        "cuenta": {"servidor": "x", "empresa": "y", "build": 1},
        "declarado_por": "Aleks",
        "congelado_el": "2026-12-01",
        "rama": "trabajo/f17-corrida",
        "informe": "docs/validation/F17-CORRIDA.md",
    }


def test_un_manifiesto_sintetico_bien_formado_pasa(tmp_path: Path) -> None:
    ruta = tmp_path / "f17-historial-2026-04.yaml"
    ruta.write_text(yaml.safe_dump(_manifiesto(), allow_unicode=True), encoding="utf-8")
    assert L.validar_manifiesto(leer_yaml(ruta), CONSTRUCCION) == []


@pytest.mark.parametrize(
    ("cambio", "esperado"),
    [
        (lambda d: d.pop("control"), "falta control"),
        (lambda d: d.update(mes="2026-02"), "no es de construccion"),
        (lambda d: d.update(dataset_id="f17-historial-2026-04-00000000"), "sufijo"),
        (lambda d: d["ficheros"].pop(), "faltan ficheros de tipo ['control']"),
        (lambda d: d["ficheros"][0].update(tipo="otro"), "tipo 'otro'"),
        (lambda d: d["ficheros"][0].update(sha256="xyz"), "sha256 mal formado"),
        (
            lambda d: d["ficheros"][0].update(ruta="f17/2026-07/F17_2026-07-01_ticks.csv"),
            "no es del mes",
        ),
        (lambda d: d.update(extra=1), "campo de mas"),
        (lambda d: d["control"].pop("cuadra"), "control: falta cuadra"),
    ],
)
def test_cada_regla_del_esquema_rompe_a_proposito(cambio: Any, esperado: str) -> None:
    d = _manifiesto()
    cambio(d)
    malos = L.validar_manifiesto(d, CONSTRUCCION)
    assert any(esperado in m for m in malos), malos


def test_los_manifiestos_de_verdad_si_los_hay_cumplen_el_esquema() -> None:
    for ruta in sorted(CARPETA.glob("*.yaml")) if CARPETA.is_dir() else []:
        assert L.validar_manifiesto(leer_yaml(ruta), CONSTRUCCION) == [], ruta.name
