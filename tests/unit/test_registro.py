from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.config.registro import (
    AmbiguedadNoDeclaradaError,
    Estado,
    ParametroDesconocidoError,
    Registro,
    RegistroError,
    TipoDeParametroError,
    _convertir,
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


def test_fichero_real_cada_valor_de_estrategia_cita_al_trader(repo: Path) -> None:
    """Desde F11 los parametros de estrategia SI tienen valor, y por eso lo que hay que vigilar
    cambia: ninguno puede tenerlo sin citar al trader.

    Antes de la sesion 1 este test afirmaba lo contrario -que todos seguian UNKNOWN-, que era la
    guardia util mientras no habia respuestas. Ahora la guardia util es que nadie escriba un valor
    de estrategia por decision propia: un numero de la operativa sale del trader (feedback) o de
    una cita suya (evidence), nunca de un ADR nuestro.
    """
    r = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    for nombre in r.por_categoria("estrategia"):
        p = r.parametros[nombre]
        if p.estado is Estado.UNKNOWN:
            continue  # sin valor no hay nada que citar
        assert p.fuente is not None, f"{nombre} tiene valor y no dice de donde sale"
        assert p.fuente.tipo in ("feedback", "evidence"), (
            f"{nombre} es de estrategia y su valor viene de {p.fuente.tipo}: "
            f"un numero de la operativa lo dice el trader, no lo decidimos nosotros"
        )
    for nombre, p in r.parametros.items():
        # Un parametro de entorno sin valor todavia (UNKNOWN) no tiene nada que citar; la regla
        # es que su VALOR venga de una decision, no de la evidencia ni del feedback.
        if p.categoria != "estrategia" and p.estado is not Estado.UNKNOWN:
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
        # NaN e Infinity los para ya el formato, antes de construir el Decimal.
        ('valor: "0.75"', 'valor: "NaN"', "numero invalido"),
        ('valor: "0.75"', 'valor: "Infinity"', "numero invalido"),
        ('valor: "0.75"', 'valor: "abc"', "numero invalido"),
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


@pytest.mark.parametrize(
    ("bruto", "pista"),
    [
        ("0,75", "el separador decimal es el punto"),
        ("1%", "el porcentaje se escribe sin el signo"),
        ("1_000", "numero invalido"),
        ("1E+999999999", "numero invalido"),
        ("dos", "numero invalido"),
    ],
)
def test_numeros_escritos_como_los_dice_una_persona(bruto: str, pista: str) -> None:
    """La respuesta del trader se copia a mano al registro, y `0,75` o `1%` es como se dice.
    El mensaje tiene que explicar como escribirlo, no ensenar las internals de `decimal`."""
    with pytest.raises(RegistroError, match=pista):
        _convertir("decimal", bruto, None, "p")


def test_los_numeros_validos_siguen_valiendo() -> None:
    assert _convertir("decimal", "0.75", None, "p") == Decimal("0.75")
    assert _convertir("decimal", " 3 ", None, "p") == Decimal("3")
    assert _convertir("decimal", 3, None, "p") == Decimal("3")


# --- tipos que entran con F11: enum, booleano, puntos, minutos, lotes ---


def _param(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "nombre": "ejemplo",
        "categoria": "estrategia",
        "tipo": "enum",
        "unidad": "eleccion",
        "descripcion": "un parametro de prueba",
        "estado": "CONFIRMED",
        "valor": "a",
        "opciones": ["a", "b"],
        "fuente": {"tipo": "feedback", "id": "fb-2026-09-09-sesion-01-846fb0d7"},
    }
    d.update(cambios)
    return {k: v for k, v in d.items() if v is not _QUITAR}


_QUITAR = object()


def _cargar(tmp_path: Path, param: dict[str, Any]) -> Registro:
    ruta = tmp_path / "p.yaml"
    ruta.write_text(yaml.safe_dump({"parametros": [param]}), encoding="utf-8", newline="\n")
    return cargar_registro(ruta)


def test_enum_exige_opciones_y_el_valor_debe_estar_en_ellas(tmp_path: Path) -> None:
    r = _cargar(tmp_path, _param())
    assert r.opcion("ejemplo") == "a"
    with pytest.raises(TipoDeParametroError):
        r.texto("ejemplo")  # un enum no se lee como texto: el tipo declarado manda
    with pytest.raises(RegistroError, match="no esta en las opciones"):
        _cargar(tmp_path, _param(valor="c"))
    with pytest.raises(RegistroError, match="al menos dos valores"):
        _cargar(tmp_path, _param(opciones=["a"]))
    with pytest.raises(RegistroError, match="opcion repetida"):
        _cargar(tmp_path, _param(opciones=["a", "a"]))


def test_solo_un_enum_lleva_opciones(tmp_path: Path) -> None:
    with pytest.raises(RegistroError, match="solo un parametro de tipo enum"):
        _cargar(tmp_path, _param(tipo="texto", valor="a", opciones=["a", "b"]))


def test_booleano_no_admite_comillas(tmp_path: Path) -> None:
    """`false` entre comillas es la cadena 'false', que es verdadera: por eso se rechaza."""
    r = _cargar(tmp_path, _param(tipo="booleano", valor=False, opciones=_QUITAR))
    assert r.booleano("ejemplo") is False
    with pytest.raises(RegistroError, match="se escribe true o false"):
        _cargar(tmp_path, _param(tipo="booleano", valor="false", opciones=_QUITAR))


@pytest.mark.parametrize("tipo", ["puntos", "minutos"])
def test_puntos_y_minutos_son_enteros_no_negativos(tmp_path: Path, tipo: str) -> None:
    assert _cargar(tmp_path, _param(tipo=tipo, valor=20, opciones=_QUITAR)) is not None
    with pytest.raises(RegistroError, match="exige un entero"):
        _cargar(tmp_path, _param(tipo=tipo, valor="20", opciones=_QUITAR))
    with pytest.raises(RegistroError, match="no puede ser negativo"):
        _cargar(tmp_path, _param(tipo=tipo, valor=-1, opciones=_QUITAR))


def test_lotes_admite_decimales_entre_comillas(tmp_path: Path) -> None:
    r = _cargar(tmp_path, _param(tipo="lotes", valor="0.01", opciones=_QUITAR))
    assert str(r.obtener("ejemplo")) == "0.01"


@pytest.mark.parametrize("tipo", ["enum", "booleano"])
def test_ni_enum_ni_booleano_admiten_minimo_o_maximo(tmp_path: Path, tipo: str) -> None:
    valor = "a" if tipo == "enum" else True
    ops = ["a", "b"] if tipo == "enum" else _QUITAR
    with pytest.raises(RegistroError, match="minimo/maximo no se aplican"):
        _cargar(tmp_path, _param(tipo=tipo, valor=valor, opciones=ops, minimo="0"))


def test_el_huso_del_grafico_es_utc_mas_dos_todo_el_ano(repo: Path) -> None:
    """`Etc/GMT-2` significa UTC+2: el signo va invertido en la nomenclatura IANA.

    Es el error que este test existe para impedir. Si alguien "corrige" `Etc/GMT-2` por
    `Etc/GMT+2` porque le parece mas natural, todas las horas de la operativa se desplazan cuatro
    horas y el bot opera en otro momento del dia sin que nada mas falle.

    Y se comprueba en enero y en julio a proposito: el trader dijo que NO se ajusta al cambio de
    horario, asi que el desplazamiento tiene que ser el mismo en invierno y en verano -que es lo
    que distingue `Etc/GMT-2` de `Europe/Madrid`-.
    """
    from datetime import datetime
    from zoneinfo import ZoneInfo

    r = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    huso = ZoneInfo(r.texto("huso_grafico"))
    for mes in (1, 7):
        desfase = datetime(2026, mes, 15, 12, tzinfo=huso).utcoffset()
        assert desfase is not None
        assert desfase.total_seconds() == 2 * 3600, f"mes {mes}: {desfase}"
    madrid = ZoneInfo("Europe/Madrid")
    enero = datetime(2026, 1, 15, 12, tzinfo=madrid).utcoffset()
    assert enero is not None and enero.total_seconds() == 3600, (
        "Europe/Madrid da +1 en enero: por eso el reloj del trader no es Madrid"
    )


def test_las_horas_de_la_operativa_cuelgan_del_huso_del_grafico(repo: Path) -> None:
    """Las tres horas declaran el mismo huso que `huso_grafico`, o dirian cosas distintas."""
    r = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    esperado = r.texto("huso_grafico")
    for nombre in ("anclaje_h4", "ventana_inicio", "ventana_fin"):
        assert r.hora(nombre).huso == esperado, nombre
