"""Los manifiestos de la medida de las ordenes stop y del grabador (rama `trabajo/f17-ordenes`, D7):
esquemas `schema_f17_ordenes: 1` y `schema_f17_grabador: 1` de `data/manifests/README.md`, en sus
carpetas propias, `data/manifests/f17-ordenes/` y `data/manifests/f17-grabador/`, NUNCA en `f17/`
(su test valida todo lo de ahi con el esquema del historial, que exige un mes de construccion).

Sobre un manifiesto sintetico en un temporal, cada regla rompe a proposito; y los de verdad, si los
hay, cumplen.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "scripts" / "leer_ordenes_f17.py"
README = RAIZ / "data" / "manifests" / "README.md"


def _modulo() -> ModuleType:
    spec = importlib.util.spec_from_file_location("leer_ordenes_f17", GUION)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["leer_ordenes_f17"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


L = _modulo()


def _fichero(ruta: str, tipo: str) -> dict[str, Any]:
    return {
        "ruta": ruta,
        "tipo": tipo,
        "sha256": hashlib.sha256(ruta.encode()).hexdigest(),
        "bytes": 10,
        "filas": 2,
        "fin_de_linea": "crlf",
    }


def _manifiesto(tipo: str) -> dict[str, Any]:
    if tipo == "ordenes":
        ficheros = [
            _fichero("data/f17-ordenes/2026-12-02/F17M_uno_20261202_100000.csv", "medida"),
            _fichero("data/f17-ordenes/2026-12-02/F17M_ticks_1.csv", "ticks"),
        ]
        cabeza = {"schema_f17_ordenes": 1, "estrato": "uno"}
        nombre = "f17-ordenes-2026-12-02-"
    else:
        ficheros = [
            _fichero("data/f17-grabador/2026-12-02/F17G_2026-12-02_09.csv", "hora"),
            _fichero("data/f17-grabador/2026-12-02/F17G_control_20261202_090000.csv", "control"),
        ]
        cabeza = {"schema_f17_grabador": 1}
        nombre = "f17-grabador-2026-12-02-"
    return {
        **cabeza,
        "dataset_id": nombre + L.H.sufijo_de(ficheros),
        "ficheros": ficheros,
        "dias": 1,
        "script": {"nombre": "x", "version": "1.0"},
        "control": {
            "time_trade_server_s": 1,
            "time_gmt_s": 1,
            "desfase_servidor_gmt_min": 120,
            "cuadra": True,
        },
        "cuenta": "DEMO",
        "declarado_por": "Aleks",
        "congelado_el": "2026-12-02",
        "rama": "trabajo/x",
        "informe": "docs/validation/X.md",
    }


@pytest.mark.parametrize("tipo", ["ordenes", "grabador"])
def test_el_manifiesto_sintetico_cumple(tipo: str, tmp_path: Path) -> None:
    import yaml

    ruta = tmp_path / "m.yaml"
    ruta.write_text(yaml.safe_dump(_manifiesto(tipo), allow_unicode=True), encoding="utf-8")
    assert L.validar_manifiesto(leer_yaml(ruta), tipo) == []


@pytest.mark.parametrize(
    ("tipo", "cambio", "esperado"),
    [
        ("ordenes", lambda d: d.pop("estrato"), "falta estrato"),
        ("ordenes", lambda d: d.update(estrato="bot_reducido"), "estrato 'bot_reducido'"),
        ("ordenes", lambda d: d.update(schema_f17_ordenes=2), "schema_f17_ordenes no es 1"),
        ("ordenes", lambda d: d["ficheros"].pop(), "faltan ficheros de tipo ['ticks']"),
        ("ordenes", lambda d: d["ficheros"][0].update(tipo="m1"), "tipo 'm1'"),
        ("ordenes", lambda d: d["ficheros"][0].update(sha256="x"), "sha256 mal formado"),
        ("ordenes", lambda d: d.update(dataset_id="f17-historial-2026-04-12345678"), "mal formado"),
        ("ordenes", lambda d: d.update(dataset_id="f17-ordenes-2026-12-02-00000000"), "sufijo"),
        ("ordenes", lambda d: d.update(dias=0), "dias"),
        ("grabador", lambda d: d["control"].pop("cuadra"), "control: falta cuadra"),
        ("grabador", lambda d: d.update(extra=1), "campo de mas"),
        ("grabador", lambda d: d["ficheros"][1].pop("fin_de_linea"), "falta fin_de_linea"),
    ],
)
def test_cada_regla_del_esquema_rompe_a_proposito(tipo: str, cambio: Any, esperado: str) -> None:
    d = copy.deepcopy(_manifiesto(tipo))
    cambio(d)
    malos = L.validar_manifiesto(d, tipo)
    assert any(esperado in m for m in malos), malos


def test_un_manifiesto_de_esta_rama_no_cumple_el_esquema_del_historial() -> None:
    """Por eso no va en `f17/`: el esquema del historial lo rechaza (D7)."""
    from botsito.cases.criterio_fidelidad import cargar_criterio

    construccion = list(cargar_criterio(RAIZ).construccion)
    assert L.H.validar_manifiesto(_manifiesto("ordenes"), construccion) != []


def test_los_esquemas_estan_en_el_readme() -> None:
    texto = README.read_text(encoding="utf-8")
    for clave in (
        "schema_f17_ordenes: 1",
        "schema_f17_grabador: 1",
        "f17-ordenes/",
        "f17-grabador/",
    ):
        assert clave in texto
    for tipo in ("ordenes", "grabador"):
        for campo in L.CAMPOS[tipo]:
            assert f"`{campo}" in texto, campo


@pytest.mark.parametrize("tipo", ["ordenes", "grabador"])
def test_los_manifiestos_de_verdad_si_los_hay_cumplen(tipo: str) -> None:
    carpeta = RAIZ / "data" / "manifests" / L.CARPETA_MANIFIESTOS[tipo]
    for ruta in sorted(carpeta.glob("*.yaml")) if carpeta.is_dir() else []:
        assert L.validar_manifiesto(leer_yaml(ruta), tipo) == [], ruta.name
