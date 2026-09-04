from decimal import Decimal
from pathlib import Path

import pytest

from botsito.config.registro import (
    AmbiguedadNoDeclaradaError,
    Estado,
    ParametroDesconocidoError,
    RegistroError,
    cargar_registro,
)
from botsito.domain.valores import Fraccion, Porcentaje

BASE = """
parametros:
  - nombre: stop_fraccion
    tipo: fraccion
    unidad: fraccion de la distancia completa
    descripcion: donde va el stop
    estado: CONFIRMED
    valor: "0.75"
    fuente: {tipo: evidence, id: ev-1}
    minimo: "0"
    maximo: "1"
  - nombre: riesgo_pct
    tipo: porcentaje
    unidad: porcentaje del balance
    descripcion: riesgo por operacion
    estado: DEFAULT_AMBIGUOUS
    valor: "0.5"
    fuente: {tipo: decision, id: ADR-0015}
    ambiguedad_id: A-9
  - nombre: cartuchos
    tipo: entero
    unidad: intentos por zona
    descripcion: cuantos intentos
    estado: UNKNOWN
  - nombre: inicio
    tipo: hora
    unidad: hora de Espana
    descripcion: inicio de ventana
    estado: CONFIRMED
    valor: "07:00"
    fuente: {tipo: feedback, id: fb-3}
"""


def _escribir(tmp_path: Path, contenido: str) -> Path:
    p = tmp_path / "parametros.yaml"
    p.write_text(contenido, encoding="utf-8")
    return p


def test_carga_valida_y_tipos(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    assert r.obtener("stop_fraccion") == Fraccion("0.75")
    assert isinstance(r.obtener("inicio"), str)
    assert r.parametros["riesgo_pct"].estado is Estado.DEFAULT_AMBIGUOUS
    assert set(r.sin_fuente_confirmada()) == {"riesgo_pct", "cartuchos"}


def test_unknown_falla_siempre(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    with pytest.raises(ParametroDesconocidoError):
        r.obtener("cartuchos")
    with pytest.raises(ParametroDesconocidoError):
        r.obtener("no_existe")


def test_default_ambiguo_se_lee_y_queda_anotado(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    assert r.obtener("riesgo_pct") == Porcentaje("0.5")
    lecturas = r.lecturas_ambiguas()
    assert len(lecturas) == 1 and lecturas[0].ambiguedad_id == "A-9"


def test_default_ambiguo_sin_ambiguedad_id_es_error_de_carga(tmp_path: Path) -> None:
    contenido = BASE.replace("    ambiguedad_id: A-9\n", "")
    with pytest.raises(RegistroError, match="ambiguedad_id"):
        cargar_registro(_escribir(tmp_path, contenido))


def test_ambiguedad_no_declarada_en_lectura() -> None:
    from botsito.config.registro import Parametro, Registro

    p = Parametro(
        nombre="x",
        tipo="fraccion",
        unidad="u",
        estado=Estado.DEFAULT_AMBIGUOUS,
        descripcion="d",
        valor=Fraccion("0.5"),
    )
    with pytest.raises(AmbiguedadNoDeclaradaError):
        Registro({"x": p}).obtener("x")


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ("    fuente: {tipo: evidence, id: ev-1}\n", "exige fuente"),
        ('    valor: "0.75"\n', "exige valor"),
        ('    maximo: "1"\n', None),
    ],
)
def test_confirmed_exige_fuente_y_valor(tmp_path: Path, cambio: str, mensaje: str | None) -> None:
    contenido = BASE.replace(cambio, "", 1)
    if mensaje is None:
        cargar_registro(_escribir(tmp_path, contenido))
    else:
        with pytest.raises(RegistroError, match=mensaje):
            cargar_registro(_escribir(tmp_path, contenido))


def test_fuera_de_rango(tmp_path: Path) -> None:
    contenido = BASE.replace('valor: "0.75"', 'valor: "1.5"')
    with pytest.raises(RegistroError, match="maximo"):
        cargar_registro(_escribir(tmp_path, contenido))


def test_duplicado(tmp_path: Path) -> None:
    dup = BASE + BASE.split("parametros:")[1].split("  - nombre: riesgo_pct")[0]
    with pytest.raises(RegistroError, match="duplicado"):
        cargar_registro(_escribir(tmp_path, dup))


def test_float_en_yaml_rechazado(tmp_path: Path) -> None:
    contenido = BASE.replace('valor: "0.75"', "valor: 0.75")
    with pytest.raises(RegistroError, match="comillas"):
        cargar_registro(_escribir(tmp_path, contenido))


def test_unknown_con_valor_es_error(tmp_path: Path) -> None:
    contenido = BASE.replace("    estado: UNKNOWN\n", "    estado: UNKNOWN\n    valor: 3\n")
    with pytest.raises(RegistroError, match="UNKNOWN"):
        cargar_registro(_escribir(tmp_path, contenido))


def test_hora_invalida(tmp_path: Path) -> None:
    contenido = BASE.replace('valor: "07:00"', 'valor: "7am"')
    with pytest.raises(RegistroError, match="hora"):
        cargar_registro(_escribir(tmp_path, contenido))


def test_fichero_real_vacio_de_valores(repo: Path) -> None:
    r = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    assert r.parametros == {}, "en F02 el registro no puede contener valores"


def test_decimal_no_es_float(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    v = r.obtener("stop_fraccion")
    assert isinstance(v, Fraccion) and isinstance(v.valor, Decimal)
