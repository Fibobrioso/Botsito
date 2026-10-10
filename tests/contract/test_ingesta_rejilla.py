"""La ingesta asigna cada operacion a su sesion por la puerta del reloj (`trabajo/cases-rejilla`).

Semanas de 2024 (ACTIVACION-A42.md §4): el lunes 28 de octubre es de desfase -Europa ya cambio la
hora y EE. UU. no- y el lunes 4 de noviembre es de control. El libro es sintetico, en UTC.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.cases.ingesta import IngestaError, Resultado, ingerir
from botsito.cases.relojes import RelojSesiones

from .test_ingesta import RELOJ, SESIONES, _declarar, _repo, _xlsx

CABECERA = ["dateStart", "side", "entryPrice", "initialSL"]


def _ingerir(tmp_path: Path, fila: list[str], dia: str, reloj: RelojSesiones = RELOJ) -> Resultado:
    repo = _repo(tmp_path, {f"caso-eurusd-{dia}": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, fila])
    _declarar(repo, material)
    return ingerir(repo, material, "Europe/Madrid", SESIONES, dias=[dia], reloj=reloj)


@pytest.mark.contract
def test_una_entrada_a_las_0630_de_un_dia_de_desfase_es_de_la_sesion_07_11(tmp_path: Path) -> None:
    """05:30 UTC = 06:30 de Madrid: la vela H4 de la rejilla que el trader opera ese dia como su
    sesion 07-11 abre a las 06:00. Con `main` falla: en la pared de Madrid las 06:30 no caen en
    ninguna sesion y la ingesta aborta."""
    r = _ingerir(tmp_path, ["2024/10/28 05:30:00", "buy", "1.1000", "1.0990"], "2024-10-28")
    assert [op.sesion for op in r.casos["2024-10-28"]] == ["07-11"]


@pytest.mark.contract
def test_en_la_semana_de_control_la_sesion_es_la_de_main(tmp_path: Path) -> None:
    """06:30 UTC = 07:30 de Madrid: 07-11 con la rejilla y con la pared de Madrid (`main`)."""
    fila = ["2024/11/04 06:30:00", "buy", "1.1000", "1.0990"]
    r = _ingerir(tmp_path / "rejilla", fila, "2024-11-04")
    pared = _ingerir(
        tmp_path / "pared", fila, "2024-11-04", RelojSesiones.de_pared("Europe/Madrid")
    )
    assert r.casos == pared.casos
    assert [op.sesion for op in r.casos["2024-11-04"]] == ["07-11"]


@pytest.mark.contract
def test_si_el_dia_de_la_fila_no_es_el_dia_operativo_la_ingesta_para(tmp_path: Path) -> None:
    """La guardia, rota a proposito. 22:30 UTC del domingo 27 = 23:30 de Madrid del 27: el
    lector la lee como del 27, pero en la rejilla de ese lunes de desfase ya es el dia operativo
    del 28 (que empieza a las 23:00 de la vispera). La ingesta para, nombrando el caso y sin el
    instante ni los precios. Con `main` falla con otro mensaje: no cae en ninguna sesion."""
    with pytest.raises(IngestaError) as exc:
        _ingerir(tmp_path, ["2024/10/27 22:30:00", "buy", "1.1000", "1.0990"], "2024-10-27")
    mensaje = str(exc.value)
    assert "no es el dia operativo de su apertura" in mensaje
    assert mensaje.startswith("el caso del dia 2024-10-27, operacion 1: ")
    assert "22:30" not in mensaje and "23:30" not in mensaje and "1.10" not in mensaje
