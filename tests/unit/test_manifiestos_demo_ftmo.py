"""Los manifiestos de la demo de FTMO (`data/manifests/demo_ftmo/`) se escriben a mano
(`data/manifests/README.md`, «Demo de FTMO»), y nada comprobaba que su `dataset_id` dijera la
verdad: `demo-ftmo-<AAAA-MM-DD del servidor>-<8 hex>`, con el sufijo = los 8 primeros del sha256
del CSV y la fecha = la de `hora_servidor_primera` (rama trabajo/demo-ejecuciones-2-3, encargo del
2026-11-06).

Solo lee los manifiestos commiteados, no los CSV (que viven fuera de git)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

REPO = Path(__file__).resolve().parents[2]
CARPETA = REPO / "data" / "manifests" / "demo_ftmo"


def problemas_del_manifiesto(m: dict[str, Any]) -> list[str]:
    """Lo que no casa entre el `dataset_id` y el resto del manifiesto (vacio si casa)."""
    problemas: list[str] = []
    dataset_id = str(m.get("dataset_id", ""))
    sha = str(m.get("fichero", {}).get("sha256", ""))
    partes = dataset_id.rsplit("-", 1)
    if len(partes) != 2 or not partes[0].startswith("demo-ftmo-"):
        return [f"dataset_id {dataset_id!r} sin la forma demo-ftmo-<fecha>-<8 hex>"]
    prefijo, sufijo = partes
    if len(sha) != 64:
        problemas.append(f"sha256 {sha!r} no tiene 64 hex")
    if sufijo != sha[:8]:
        problemas.append(f"sufijo {sufijo!r} no son los 8 primeros del sha256 ({sha[:8]!r})")
    fecha = prefijo.removeprefix("demo-ftmo-")
    primera = str(m.get("hora_servidor_primera", ""))[:10].replace(".", "-")
    if fecha != primera:
        problemas.append(f"fecha {fecha!r} no es la de hora_servidor_primera ({primera!r})")
    return problemas


def _manifiestos() -> list[tuple[Path, dict[str, Any]]]:
    return [
        (p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in sorted(CARPETA.glob("*.yaml"))
    ]


def test_hay_los_tres_manifiestos_de_la_demo() -> None:
    ejecuciones = sorted(m["ejecucion"] for _, m in _manifiestos())
    assert ejecuciones == [1, 2, 3]


@pytest.mark.parametrize("ruta, manifiesto", _manifiestos(), ids=lambda x: getattr(x, "name", ""))
def test_el_dataset_id_casa_con_el_sha256_y_la_fecha(
    ruta: Path, manifiesto: dict[str, Any]
) -> None:
    assert problemas_del_manifiesto(manifiesto) == []
    assert ruta.stem == manifiesto["dataset_id"]


def test_un_sufijo_que_no_casa_se_caza() -> None:
    _, bueno = _manifiestos()[0]
    malo = {**bueno, "dataset_id": bueno["dataset_id"][:-8] + "00000000"}
    assert any("sufijo" in p for p in problemas_del_manifiesto(malo))
    otra_fecha = {**bueno, "dataset_id": "demo-ftmo-2000-01-01-" + bueno["fichero"]["sha256"][:8]}
    assert any("fecha" in p for p in problemas_del_manifiesto(otra_fecha))
