"""El selector del tipo de orden de entrada (A-47, ADR-0056 §1, ADR-0058; rama
`trabajo/selector-orden-stop`): la lectura del registro o del diagnostico, la negativa sin ninguna,
la etiqueta, y la CLI que se niega ANTES de leer una vela. RN-011 con orden stop, de punta a punta,
vive en `test_cableado.py`, junto a su mercado sintetico."""

from __future__ import annotations

import argparse
from pathlib import Path

import pytest

from botsito.config.registro import ParametroDesconocidoError, cargar_registro
from botsito.engine.diagnostico import Diagnostico, nombre_etiquetado
from botsito.engine.entrada import (
    LECTURAS_A47,
    LIMITE_EN_RETROCESO,
    PARAMETRO_A47,
    STOP_EN_RUPTURA,
    DiagnosticoDeTipoRechazadoError,
    SinTipoDeOrdenError,
    lectura_tipo_orden,
)

RAIZ = Path(__file__).resolve().parents[2]


class _Fijado:
    """Un registro minimo con el tipo de orden ya respondido."""

    def __init__(self, valor: str | None) -> None:
        self.valor = valor

    def opcion(self, nombre: str) -> str:
        assert nombre == PARAMETRO_A47
        if self.valor is None:
            raise ParametroDesconocidoError(nombre)
        return self.valor


def test_el_selector_esta_en_el_registro_sin_valor_y_con_las_dos_lecturas() -> None:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    p = registro.parametros[PARAMETRO_A47]
    assert p.estado.name == "UNKNOWN" and p.valor is None
    assert p.opciones == LECTURAS_A47 == (STOP_EN_RUPTURA, LIMITE_EN_RETROCESO)


def test_sin_fijar_y_sin_diagnostico_se_niega_nombrando_a47() -> None:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    with pytest.raises(SinTipoDeOrdenError) as exc:
        lectura_tipo_orden(registro, None)
    assert "A-47" in str(exc.value) and "--diagnostico-a47" in str(exc.value)
    for lectura in LECTURAS_A47:
        assert lectura_tipo_orden(registro, lectura) == lectura
    with pytest.raises(ValueError, match="no esta en"):
        lectura_tipo_orden(registro, "mercado")


def test_con_el_tipo_fijado_el_diagnostico_se_rechaza() -> None:
    fijado = _Fijado(STOP_EN_RUPTURA)
    assert lectura_tipo_orden(fijado, None) == STOP_EN_RUPTURA  # type: ignore[arg-type]
    with pytest.raises(DiagnosticoDeTipoRechazadoError, match="ya esta fijado"):
        lectura_tipo_orden(fijado, LIMITE_EN_RETROCESO)  # type: ignore[arg-type]


def test_la_etiqueta_de_a47() -> None:
    diag = Diagnostico(a47=STOP_EN_RUPTURA)
    assert diag.etiquetas == ("DIAGNOSTICO-A47-stop_en_ruptura",)
    assert nombre_etiquetado(Path("x.txt"), diag.etiquetas) == Path(
        "x.DIAGNOSTICO.a47=stop_en_ruptura.txt"
    )
    with pytest.raises(ValueError, match="A-47"):
        Diagnostico(a47="mercado")
    # detras de A-21 y delante de A-27, siempre en el mismo orden
    todo = Diagnostico(None, None, "solo_una_zona_de_control", 0, LIMITE_EN_RETROCESO)
    assert todo.etiquetas == (
        "DIAGNOSTICO-A21-solo_una_zona_de_control",
        "DIAGNOSTICO-A47-limite_en_retroceso",
        "DIAGNOSTICO-A27-0",
    )


def test_la_cli_exige_simular_para_a47() -> None:
    from botsito.cli import _diagnostico_de

    with pytest.raises(ValueError, match="--simular"):
        _diagnostico_de(argparse.Namespace(diagnostico_a47=STOP_EN_RUPTURA, simular=False))
    assert (
        _diagnostico_de(argparse.Namespace(diagnostico_a47=STOP_EN_RUPTURA, simular=True)).a47
        == STOP_EN_RUPTURA
    )


def test_la_cli_con_simular_se_niega_sin_a47_antes_de_leer_velas(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio

    real = cargar_criterio(RAIZ)
    salida = tmp_path / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--simular", "--meses", real.construccion[0],
         "--salida", str(salida), "--diagnostico-a35", "cierre_vela_contraria",
         "--diagnostico-a44", "sin_tope", "--diagnostico-a21", "solo_una_zona_de_control"]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert codigo == 2 and "A-47" in err and PARAMETRO_A47 in err
    assert not list(tmp_path.iterdir())
