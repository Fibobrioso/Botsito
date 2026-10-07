"""El umbral de construccion que habilita medir el conjunto de medida (ADR-0070), sin el arnes:
todo sintetico. La carga de los dos campos nuevos de `criterio_fidelidad.yaml` y, desde la fase 3,
la linea de veredicto que el arnes escribe al final de su seccion del criterio."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import FICHERO_CRITERIO, CriterioError, cargar_criterio

REPO = Path(__file__).resolve().parents[2]
CAMPOS = ("umbral_construccion_para_medir_cobertura", "umbral_construccion_para_medir_precision")


def _copia(tmp_path: Path, cambiar: dict[str, str | None]) -> Path:
    """El fichero real, con los campos de `cambiar` sustituidos (o quitados si el valor es None)."""
    lineas = []
    for linea in (REPO / FICHERO_CRITERIO).read_text(encoding="utf-8").splitlines():
        campo = linea.split(":", 1)[0]
        if campo in cambiar:
            if cambiar[campo] is not None:
                lineas.append(f"{campo}: {cambiar[campo]}")
            continue
        lineas.append(linea)
    ruta = tmp_path / FICHERO_CRITERIO
    ruta.parent.mkdir(parents=True)
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return tmp_path


def test_el_fichero_real_lleva_las_cifras_de_adr_0043_tambien_para_construccion() -> None:
    c = cargar_criterio(REPO)
    assert c.umbral_construccion_para_medir_cobertura == Fraction(7, 10)
    assert c.umbral_construccion_para_medir_precision == Fraction(6, 10)
    # las mismas que el umbral de medida (ADR-0070, decision 1)
    assert c.umbral_construccion_para_medir_cobertura == c.umbral_cobertura
    assert c.umbral_construccion_para_medir_precision == c.umbral_precision


@pytest.mark.parametrize("campo", CAMPOS)
def test_sin_el_campo_no_carga(tmp_path: Path, campo: str) -> None:
    with pytest.raises(CriterioError, match=campo):
        cargar_criterio(_copia(tmp_path, {campo: None}))


@pytest.mark.parametrize("campo", CAMPOS)
@pytest.mark.parametrize("valor", ['"1.5"', '"-0.1"', '"setenta"'])
def test_fuera_de_0_a_1_o_no_numerico_no_carga(tmp_path: Path, campo: str, valor: str) -> None:
    with pytest.raises(CriterioError, match=campo):
        cargar_criterio(_copia(tmp_path, {campo: valor}))
