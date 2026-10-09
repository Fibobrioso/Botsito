"""El selector del tipo de orden de entrada (A-47, ADR-0056 §1, ADR-0058; rama
`trabajo/selector-orden-stop`): la lectura del registro o del diagnostico, la negativa sin ninguna,
la etiqueta, y la CLI que se niega ANTES de leer una vela. RN-011 con orden stop, de punta a punta,
vive en `test_cableado.py`, junto a su mercado sintetico.

Desde el 2026-09-29 (rama `trabajo/activar-sesion-03`) el trader ha respondido A-47 -«se entra
siempre por stop», fb-2026-09-29-sesion-03-8f091ed8- y el registro REAL dice `stop_en_ruptura`.
Los tests que comprobaban la negativa contra el registro real cambian de sentido a proposito: la
negativa se conserva, con A-47 fijada a UNKNOWN de forma EXPLICITA en una copia del registro."""

from __future__ import annotations

import argparse
import re
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
from botsito.engine.perfil_cuenta import PerfilCuenta, cargar_perfil
from tests.unit.perfil_stops_level_unknown import perfil_con_stops_level_unknown

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO_REAL = RAIZ / "knowledge" / "spec" / "parametros.yaml"
PERFIL_REAL = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"


def _registro_con_a47_unknown(tmp_path: Path) -> Path:
    """Una copia del registro real con `entrada_tipo_orden` devuelto a UNKNOWN y sin valor: la
    forma explicita de seguir probando la negativa cuando el registro real ya esta fijado."""
    texto = REGISTRO_REAL.read_text(encoding="utf-8")
    patron = re.compile(
        r"(  - nombre: entrada_tipo_orden\n(?:    (?!estado:).*\n|      .*\n)*)"
        r"    estado: CONFIRMED\n    valor: stop_en_ruptura\n    fuente:\n      tipo: feedback\n"
        r"      id: fb-[0-9a-z-]+\n"
    )
    nuevo, n = patron.subn(r"\1    estado: UNKNOWN\n", texto)
    assert n == 1, "el bloque de entrada_tipo_orden del registro real ya no tiene la forma esperada"
    copia = tmp_path / "parametros.yaml"
    copia.write_text(nuevo, encoding="utf-8")
    return copia


class _Fijado:
    """Un registro minimo con el tipo de orden ya respondido."""

    def __init__(self, valor: str | None) -> None:
        self.valor = valor

    def opcion(self, nombre: str) -> str:
        assert nombre == PARAMETRO_A47
        if self.valor is None:
            raise ParametroDesconocidoError(nombre)
        return self.valor


def test_el_selector_esta_en_el_registro_fijado_en_stop_y_con_las_dos_lecturas() -> None:
    registro = cargar_registro(REGISTRO_REAL)
    p = registro.parametros[PARAMETRO_A47]
    assert p.estado.name == "CONFIRMED" and p.valor == STOP_EN_RUPTURA
    assert p.opciones == LECTURAS_A47 == (STOP_EN_RUPTURA, LIMITE_EN_RETROCESO)
    # con el registro real, el motor corre con stop y rechaza el diagnostico
    assert lectura_tipo_orden(registro, None) == STOP_EN_RUPTURA
    with pytest.raises(DiagnosticoDeTipoRechazadoError, match="ya esta fijado"):
        lectura_tipo_orden(registro, LIMITE_EN_RETROCESO)


def test_sin_fijar_y_sin_diagnostico_se_niega_nombrando_a47(tmp_path: Path) -> None:
    registro = cargar_registro(_registro_con_a47_unknown(tmp_path))
    assert registro.parametros[PARAMETRO_A47].estado.name == "UNKNOWN"
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
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.config import registro as modulo_registro

    (tmp_path / "registro").mkdir()
    copia = _registro_con_a47_unknown(tmp_path / "registro")
    original = modulo_registro.cargar_registro

    def con_a47_unknown(ruta: Path) -> modulo_registro.Registro:
        return original(copia if Path(ruta) == REGISTRO_REAL else ruta)

    monkeypatch.setattr(modulo_registro, "cargar_registro", con_a47_unknown)
    real = cargar_criterio(RAIZ)
    (tmp_path / "salida").mkdir()
    salida = tmp_path / "salida" / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--simular", "--meses", real.construccion[0],
         "--salida", str(salida), "--diagnostico-a35", "cierre_vela_contraria",
         "--diagnostico-a44", "sin_tope", "--diagnostico-a21", "solo_una_zona_de_control"]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert codigo == 2 and "A-47" in err and PARAMETRO_A47 in err
    assert not list((tmp_path / "salida").iterdir())


def test_la_cli_con_a47_fijada_pasa_a_pedir_a27(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Con el registro real, A-47 ya no para la corrida: la siguiente puerta es la de la orden stop,
    que no se coloca sin stops level (A-27, ADR-0057).

    NO se niega antes de leer velas, como decia el nombre de este test hasta el 2026-09-29: A-27 la
    comprueba el broker al colocar la PRIMERA orden stop (ADR-0057 §5), despues de leer las velas y
    los ticks del mes y de correr el motor hasta esa orden. Por eso necesita `data/`, y sin las
    velas en la maquina (la CI) se salta, como `test_preparar_a35.py`; la CI de e7df30b fallo por
    eso.

    Desde ADR-0071 (2026-10-09) el perfil de FTMO fija el stops level en 0 y la corrida real ya no
    se para ahi: la negativa se prueba con el perfil SINTETICO en UNKNOWN, que la CLI carga en lugar
    del real (como `_registro_con_a47_unknown` hace con el registro)."""
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.engine import cableado

    (tmp_path / "perfil").mkdir()
    copia = perfil_con_stops_level_unknown(tmp_path / "perfil")

    def con_stops_level_unknown(ruta: Path) -> PerfilCuenta:
        return cargar_perfil(copia if Path(ruta) == PERFIL_REAL else ruta)

    monkeypatch.setattr(cableado, "cargar_perfil", con_stops_level_unknown)
    real = cargar_criterio(RAIZ)
    (tmp_path / "salida").mkdir()
    salida = tmp_path / "salida" / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--simular", "--meses", real.construccion[0],
         "--salida", str(salida), "--diagnostico-a35", "cierre_vela_contraria",
         "--diagnostico-a44", "sin_tope", "--diagnostico-a21", "solo_una_zona_de_control"]
    )  # fmt: skip
    err = capsys.readouterr().err
    if codigo == 2 and "falta en disco" in err:
        pytest.skip("sin las velas de construccion en esta maquina")
    assert codigo == 2 and "A-27" in err and "A-47" not in err
    assert not list((tmp_path / "salida").iterdir())
