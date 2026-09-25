"""La hoja de la sesion 02 (`scripts/hoja_preguntas.py`): el orden que fijo el consultor, las
tres reglas de arriba, cada pregunta tal como esta en `ambiguedades.yaml` y que una pregunta
cerrada no llega a la hoja."""

from __future__ import annotations

import importlib.util
import sys
import zipfile
from pathlib import Path
from types import ModuleType

import pytest

from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades
from botsito.cases.hoja_docx import HojaError, x

RAIZ = Path(__file__).resolve().parents[2]
# Decision del consultor, 2026-09-25: lo que bloquea el motor; RN-005 y A-32; la orden y la caja;
# la gestion; y al final lo demas. A-43 (ADR-0049, H2) justo despues de A-35: las dos tocan RN-004.
ORDEN = [
    "A-35", "A-43", "A-21", "A-24", "A-42",
    "A-26", "A-25", "A-32",
    "A-36", "A-37", "A-29", "A-30", "A-38",
    "A-18", "A-13", "A-31", "A-40", "A-33",
    "A-34", "A-41", "A-39",
]  # fmt: skip


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "hoja_preguntas"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_el_orden_es_el_del_consultor(m: ModuleType) -> None:
    assert m.ids_en_orden() == ORDEN


def test_cada_pregunta_sale_tal_cual_y_en_su_orden(m: ModuleType) -> None:
    doc = m.documento(RAIZ)
    todas = {a.id: a for a in cargar_ambiguedades(RAIZ / FICHERO_AMBIGUEDADES)}
    posiciones = []
    for aid in ORDEN:
        texto = x(" ".join(todas[aid].pregunta.split()))
        assert texto in doc, aid
        posiciones.append(doc.index(texto))
    assert posiciones == sorted(posiciones)
    for regla in m.REGLAS:
        assert x(regla) in doc
    assert doc.index(x(m.REGLAS[-1])) < posiciones[0]


def test_una_pregunta_cerrada_no_llega_a_la_hoja(
    m: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(m, "ORDEN_SESION_02", (("Cerrada", ("A-1",)),))
    with pytest.raises(HojaError, match="ya no se preguntan"):
        m.documento(RAIZ)


def test_una_pregunta_repetida_o_inexistente_para_la_hoja(
    m: ModuleType, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(m, "ORDEN_SESION_02", (("Doble", ("A-35", "A-35")),))
    with pytest.raises(HojaError, match="dos veces"):
        m.documento(RAIZ)
    monkeypatch.setattr(m, "ORDEN_SESION_02", (("Nada", ("A-999",)),))
    with pytest.raises(HojaError, match="no existen"):
        m.documento(RAIZ)


def test_escribe_un_docx_que_se_abre(m: ModuleType, tmp_path: Path) -> None:
    salida = tmp_path / "hoja.docx"
    assert m.main(["--salida", str(salida)]) == 0
    with zipfile.ZipFile(salida) as z:
        assert "word/document.xml" in z.namelist()
