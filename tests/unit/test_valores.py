from decimal import Decimal

import pytest
from hypothesis import given
from hypothesis import strategies as st

from botsito.config.registro import cargar_registro
from botsito.domain.valores import Fraccion, Porcentaje


def test_fraccion_y_porcentaje_no_se_mezclan() -> None:
    with pytest.raises(TypeError):
        Fraccion("0.5") + Porcentaje("50")  # type: ignore[operator]
    with pytest.raises(TypeError):
        _ = Fraccion("0.5") < Porcentaje("50")  # type: ignore[operator]


def test_conversion_explicita() -> None:
    assert Porcentaje("0.5").como_fraccion() == Fraccion("0.005")
    assert Fraccion("0.75").como_porcentaje() == Porcentaje("75")


def test_float_rechazado() -> None:
    with pytest.raises(TypeError):
        Fraccion(0.75)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Porcentaje(True)


def test_decimal_exacto_no_binario() -> None:
    assert Fraccion("0.1") + Fraccion("0.2") == Fraccion("0.3")


def test_valor_invalido() -> None:
    with pytest.raises(ValueError):
        Fraccion("abc")


def test_inmutable() -> None:
    f = Fraccion("0.5")
    with pytest.raises(AttributeError):
        f.valor = Decimal("1")  # type: ignore[misc]


@given(st.decimals(min_value=Decimal("-1000"), max_value=Decimal("1000"), places=6))
def test_ida_y_vuelta_porcentaje_fraccion(d: Decimal) -> None:
    assert Porcentaje(d).como_fraccion().como_porcentaje() == Porcentaje(d)


@given(d=st.decimals(min_value=Decimal("0"), max_value=Decimal("1"), places=8))
def test_ida_y_vuelta_por_yaml_sin_perdida(
    d: Decimal, tmp_path_factory: pytest.TempPathFactory
) -> None:
    ruta = tmp_path_factory.mktemp("yaml") / "p.yaml"
    ruta.write_text(
        "parametros:\n  - nombre: x\n    tipo: fraccion\n    unidad: u\n    descripcion: d\n"
        f'    estado: CONFIRMED\n    valor: "{d}"\n    fuente: {{tipo: decision, id: t}}\n',
        encoding="utf-8",
    )
    assert cargar_registro(ruta).fraccion("x") == Fraccion(d)
