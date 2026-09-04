from decimal import Decimal
from pathlib import Path

import pytest

from botsito.config.registro import (
    AmbiguedadNoDeclaradaError,
    Estado,
    ParametroDesconocidoError,
    RegistroError,
    TipoDeParametroError,
    cargar_registro,
)
from botsito.domain.valores import Fraccion, HoraLocal, Porcentaje

BASE = """
parametros:
  - nombre: stop_fraccion
    categoria: estrategia
    tipo: fraccion
    unidad: fraccion de la distancia completa
    descripcion: donde va el stop
    estado: CONFIRMED
    valor: "0.75"
    fuente: {tipo: evidence, id: ev-v4-001230-1a2b3c4d}
    minimo: "0"
    maximo: "1"
  - nombre: riesgo_pct
    categoria: estrategia
    tipo: porcentaje
    unidad: porcentaje del balance
    descripcion: riesgo por operacion
    estado: DEFAULT_AMBIGUOUS
    valor: "0.5"
    fuente: {tipo: decision, id: ADR-0015}
    ambiguedad_id: A-9
  - nombre: cartuchos
    categoria: estrategia
    tipo: entero
    unidad: intentos por zona
    descripcion: cuantos intentos
    estado: UNKNOWN
  - nombre: inicio
    categoria: estrategia
    tipo: hora
    huso: Europe/Madrid
    unidad: hora de Espana
    descripcion: inicio de ventana
    estado: CONFIRMED
    valor: "07:00"
    fuente: {tipo: feedback, id: fb-2026-09-20-sesion-01-1a2b3c4d}
"""


def _escribir(tmp_path: Path, contenido: str) -> Path:
    p = tmp_path / "parametros.yaml"
    p.write_text(contenido, encoding="utf-8")
    return p


def test_carga_valida_y_tipos(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    assert r.obtener("stop_fraccion") == Fraccion("0.75")
    assert r.obtener("inicio") == HoraLocal("07:00", "Europe/Madrid")
    assert r.parametros["riesgo_pct"].estado is Estado.DEFAULT_AMBIGUOUS
    assert set(r.no_confirmados()) == {"riesgo_pct", "cartuchos"}


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
        categoria="estrategia",
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
        ("    fuente: {tipo: evidence, id: ev-v4-001230-1a2b3c4d}\n", "exige fuente"),
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


def test_fichero_real_sin_valores_de_estrategia(repo: Path) -> None:
    """Hasta F11 ningun parametro de estrategia tiene valor: todo lo que el trader debe confirmar
    sigue UNKNOWN. Los de entorno (F15: husos) se citan por ADR."""
    r = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    for nombre in r.por_categoria("estrategia"):
        assert r.parametros[nombre].estado is Estado.UNKNOWN, f"{nombre} tiene valor antes de F11"
    for nombre, p in r.parametros.items():
        if p.categoria != "estrategia":
            assert p.fuente is not None and p.fuente.tipo == "decision", nombre


def test_decimal_no_es_float(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    v = r.obtener("stop_fraccion")
    assert isinstance(v, Fraccion) and isinstance(v.valor, Decimal)


def test_accesores_tipados(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    assert r.fraccion("stop_fraccion") == Fraccion("0.75")
    assert r.porcentaje("riesgo_pct") == Porcentaje("0.5")
    assert r.hora("inicio") == HoraLocal("07:00", "Europe/Madrid")
    assert r.hora("inicio").minutos_del_dia == 420
    with pytest.raises(TipoDeParametroError):
        r.porcentaje("stop_fraccion")
    with pytest.raises(TipoDeParametroError):
        r.texto("inicio")
    with pytest.raises(TipoDeParametroError):
        r.decimal("stop_fraccion")
    with pytest.raises(ParametroDesconocidoError):
        r.entero("cartuchos")


def test_mensaje_de_error_sin_prefijo_duplicado(tmp_path: Path) -> None:
    contenido = BASE.replace(
        "    estado: UNKNOWN\n",
        '    estado: CONFIRMED\n    valor: "3"\n    fuente: {tipo: decision, id: ADR-0001}\n',
    )
    with pytest.raises(RegistroError) as exc:
        cargar_registro(_escribir(tmp_path, contenido))
    assert str(exc.value).count("cartuchos:") == 1


def test_limites_no_admiten_float(tmp_path: Path) -> None:
    contenido = BASE.replace('minimo: "0"', "minimo: 0.1")
    with pytest.raises(RegistroError, match="minimo"):
        cargar_registro(_escribir(tmp_path, contenido))


@pytest.mark.parametrize(
    ("antes", "despues", "mensaje"),
    [
        ('valor: "07:00"', 'valor: "25:99"', "hora invalida"),
        ("    huso: Europe/Madrid\n", "", "exige 'huso'"),
        ("huso: Europe/Madrid", "huso: Marte/Olympus", "huso desconocido"),
        ('valor: "0.75"', 'valor: "NaN"', "no finito"),
        ('valor: "0.75"', 'valor: "Infinity"', "no finito"),
        ('valor: "0.75"', 'valor: "abc"', "valor invalido"),
        (
            "categoria: estrategia\n    tipo: fraccion",
            "categoria: instrumento\n    tipo: fraccion",
            "por decision",
        ),
        (
            "categoria: estrategia\n    tipo: fraccion",
            "categoria: otra\n    tipo: fraccion",
            "categoria",
        ),
        ("id: ev-v4-001230-1a2b3c4d", "id: ev-1", "formato de evidence"),
        ("ambiguedad_id: A-9", "ambiguedad_id: nueve", "formato A-N"),
        ('minimo: "0"', 'minimo: "2"', "mayor que maximo"),
        (
            "    descripcion: donde va el stop\n",
            "    descripcion: donde va el stop\n    extra: 1\n",
            "desconocidos",
        ),
        (
            "  - nombre: stop_fraccion\n",
            "  - nombre: stop_fraccion\n    nombre: stop_fraccion\n",
            "clave duplicada",
        ),
    ],
)
def test_rechazos_de_esquema(tmp_path: Path, antes: str, despues: str, mensaje: str) -> None:
    contenido = BASE.replace(antes, despues, 1)
    assert contenido != BASE
    with pytest.raises(RegistroError, match=mensaje):
        cargar_registro(_escribir(tmp_path, contenido))


def test_categoria_de_entorno_se_cita_por_adr_y_no_se_pregunta_al_trader(tmp_path: Path) -> None:
    contenido = (
        BASE
        + """  - nombre: digitos
    categoria: instrumento
    tipo: entero
    unidad: decimales del precio
    descripcion: digitos del simbolo en el broker
    estado: CONFIRMED
    valor: 5
    fuente: {tipo: decision, id: ADR-0004}
  - nombre: lote_maximo
    categoria: prop_firm
    tipo: decimal
    unidad: lotes
    descripcion: lote maximo permitido
    estado: UNKNOWN
"""
    )
    r = cargar_registro(_escribir(tmp_path, contenido))
    assert r.entero("digitos") == 5
    assert r.por_categoria("instrumento") == ("digitos",)
    assert "lote_maximo" not in r.no_confirmados()
    assert set(r.no_confirmados()) == {"riesgo_pct", "cartuchos"}


def test_lecturas_ambiguas_no_crecen_por_tick(tmp_path: Path) -> None:
    r = cargar_registro(_escribir(tmp_path, BASE))
    for _ in range(1000):
        r.obtener("riesgo_pct")
    assert len(r.lecturas_ambiguas()) == 1


def test_hora_unknown_puede_declarar_huso(tmp_path: Path) -> None:
    contenido = BASE.replace(
        '    estado: CONFIRMED\n    valor: "07:00"\n'
        "    fuente: {tipo: feedback, id: fb-2026-09-20-sesion-01-1a2b3c4d}\n",
        "    estado: UNKNOWN\n",
    )
    assert contenido != BASE
    r = cargar_registro(_escribir(tmp_path, contenido))
    assert r.parametros["inicio"].estado is Estado.UNKNOWN


def test_texto_vacio_y_claves_ajenas_y_limites_en_hora(tmp_path: Path) -> None:
    texto = BASE.replace(
        "    estado: UNKNOWN\n",
        '    estado: CONFIRMED\n    valor: ""\n    fuente: {tipo: decision, id: ADR-0001}\n',
    ).replace("tipo: entero", "tipo: texto")
    with pytest.raises(RegistroError, match="vacio"):
        cargar_registro(_escribir(tmp_path, texto))
    with pytest.raises(RegistroError, match="nivel superior"):
        cargar_registro(_escribir(tmp_path, BASE + "otra_clave: 1\n"))
    con_limite = BASE.replace(
        "    huso: Europe/Madrid\n", '    huso: Europe/Madrid\n    minimo: "0"\n'
    )
    with pytest.raises(RegistroError, match="no se aplican"):
        cargar_registro(_escribir(tmp_path, con_limite))
