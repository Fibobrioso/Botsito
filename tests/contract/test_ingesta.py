"""F14a (ADR-0037): la ingesta abre por dia, niega por particion y NUNCA toca un agregado.

El xlsx se fabrica aqui con `zipfile` + XML de la stdlib. No se usa `openpyxl` -no esta, y anadirlo
metia una dependencia capaz de abrir un libro por accidente- ni `pandas`, que dos contratos de
importacion prohiben.

El fixture imita lo MEDIDO sobre el material real el 2026-09-21: texto `inlineStr` sin
`sharedStrings`, fechas como texto `AAAA/MM/DD HH:MM:SS` en UTC, y la pestana
`backtesting-analytics`. Lo que NO imita, a proposito, son los agregados: el material real no
tiene ninguno, asi que el riesgo es FUTURO y no presente, y la unica forma de probar la regla hoy
es fabricarlos.
"""

from __future__ import annotations

import subprocess
import zipfile
from decimal import Decimal
from pathlib import Path

import pytest
import yaml

from botsito.cases.biblioteca import como_documento, escribir, problemas_de_biblioteca
from botsito.cases.ingesta import (
    IngestaError,
    Operacion,
    Resultado,
    dias_ingeribles,
    ingerir,
)
from botsito.corpus.libro import LibroError, filas_de_los_dias
from botsito.corpus.libros import FICHERO_LIBROS, Declaracion, Lectura, sha256_de

SESIONES = [("07-11", "07:00", "11:00"), ("11-15", "11:00", "15:00")]
COLS = ["dateStart", "side", "entryPrice", "initialSL"]
# El agregado: una pestana de totales del mes. Se escribe con bytes que NO son XML valido, asi que
# si la ingesta la tocara REVENTARIA SOLA. El cinturon es no leerla; esto son los tirantes.
BASURA = b"ESTO NO ES XML: si alguien lee esta pestana, el parser muere aqui."


def _xlsx(ruta: Path, filas: list[list[str]], con_agregado: bool = True) -> None:
    def celda(ref: str, valor: str) -> str:
        return f'<c r="{ref}" t="inlineStr"><is><t>{valor}</t></is></c>'

    letras = "ABCDEFGH"
    xml = [
        '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
    ]
    for n, fila in enumerate(filas, start=1):
        celdas = "".join(celda(f"{letras[i]}{n}", v) for i, v in enumerate(fila))
        xml.append(f'<row r="{n}">{celdas}</row>')
    xml.append("</sheetData></worksheet>")

    hojas = '<sheet name="backtesting-analytics" sheetId="1" r:id="rId1"/>'
    if con_agregado:
        hojas += '<sheet name="Resumen" sheetId="2" r:id="rId2"/>'
    with zipfile.ZipFile(ruta, "w") as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("_rels/.rels", "<Relationships/>")
        z.writestr(
            "xl/workbook.xml",
            '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f"<sheets>{hojas}</sheets></workbook>",
        )
        z.writestr("xl/worksheets/sheet1.xml", "".join(xml))
        if con_agregado:
            z.writestr("xl/worksheets/sheet2.xml", BASURA)


VIEJO = "AAAA/MM/DD HH:MM:SS"


def _decl(ruta: Path, formato: str = VIEJO, huso: str = "UTC") -> Declaracion:
    """La declaracion de un libro sintetico: sin ella el lector no lo abre (ADR-0039)."""
    return Declaracion(sha256_de(ruta), (Lectura(formato, huso),))


def _declarar(repo: Path, *libros: Path, formato: str = VIEJO, huso: str = "UTC") -> None:
    """Anade los libros al `libros.yaml` del repo de prueba, como lo haria una rama que los mide."""
    ruta = repo / FICHERO_LIBROS
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8")) if ruta.exists() else {"libros": {}}
    for libro in libros:
        doc["libros"].setdefault(
            sha256_de(libro),
            {
                "fichero": libro.name,
                "lecturas": [{"formato": formato, "huso": huso}],
                "medida": "sintetico",
                "declarado_el": "2026-09-22",
                "fuente": ["ADR-0039"],
            },
        )
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True), encoding="utf-8")


def _repo(tmp_path: Path, asignacion: dict[str, str]) -> Path:
    d = tmp_path / "knowledge" / "cases" / "kit" / "2026-09-09-sesion-01"
    d.mkdir(parents=True)
    lineas = "\n".join(f"  {caso}: {part}" for caso, part in asignacion.items())
    (d / "particiones.yaml").write_text(f"asignacion:\n{lineas}\n", encoding="utf-8")
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "reparto")):
        subprocess.run(
            ["git", "-C", str(tmp_path), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True,
            capture_output=True,
        )
    return tmp_path


# La fuente COMPLETA: desde el 2026-09-22 la forma es una lista cerrada tambien en `fuente`, y el
# `{"tipo": "prueba"}` que se usaba aqui ya no la cumple.
FUENTE = {
    "tipo": "prueba",
    "fichero": "libro.xlsx",
    "sha256": "0" * 64,
    "ingerido_el": "2026-09-22",
}
CABECERA = ["dateStart", "side", "entryPrice", "initialSL", "maxTP", "idealTP"]
FILAS = [
    CABECERA,
    ["2026-05-08 07:30:00".replace("-", "/"), "buy", "1.1000", "1.0990", "1.1030", "1.1005"],
    ["2026/05/07 08:00:00", "sell", "1.2000", "1.2010", "", "1.1970"],  # RESERVADO
    ["2026/05/12 12:00:00", "sell", "1.3000", "1.3010", "1.2970", "1.2990"],
    ["2026/05/07 11:00:00", "buy", "1.4000", "1.3990", "1.4030", "1.4005"],  # RESERVADO
]


@pytest.mark.contract
def test_la_ingesta_abre_de_verdad_y_produce_casos(tmp_path: Path) -> None:
    """El test que ABRE. Sin uno que pase, una guarda nueva solo demuestra que sabe decir que no.

    Van cinco veces esta semana que una prohibicion nueva bloqueo un paso que el proceso exige.
    """
    repo = _repo(
        tmp_path,
        {
            "caso-eurusd-2026-05-08": "dev",
            "caso-eurusd-2026-05-12": "dev",
            "caso-eurusd-2026-05-07": "holdout-2",
        },
    )
    material = tmp_path / "libro.xlsx"
    _xlsx(material, FILAS)
    _declarar(repo, material)

    pedidos = dias_ingeribles(repo).dias
    assert set(pedidos) == {"2026-05-08", "2026-05-12"}, "el dia reservado no se deriva"

    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=list(pedidos))
    assert r.filas_leidas == 2, "solo se leen las filas de los dias pedidos"
    assert sorted(d for d, ops in r.casos.items() if ops) == ["2026-05-08", "2026-05-12"]
    op = r.casos["2026-05-08"][0]
    assert (op.direccion, str(op.entrada), str(op.stop)) == ("compra", "1.1000", "1.0990")
    assert op.sesion == "07-11"

    docs = [
        como_documento(pedidos[d], d, "EURUSD", ops, FUENTE)
        for d, ops in sorted(r.casos.items())
        if ops
    ]
    assert escribir(repo, docs) and problemas_de_biblioteca(repo) == []


@pytest.mark.contract
def test_un_dia_reservado_no_se_ingiere_ni_se_nombra(tmp_path: Path) -> None:
    """Y no por una excepcion: por DERIVACION. Pedirlo no es posible desde el comando."""
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-07": "holdout-2"})
    with pytest.raises(IngestaError, match="no hay ningun dia ingerible"):
        ingerir(repo, tmp_path / "no-hace-falta.xlsx", "Europe/Madrid", SESIONES)

    # Y si alguien fuerza el dia por la via interna, la escritura lo rechaza: aqui hay PRECIOS.
    repo2 = _repo(tmp_path / "dos", {"caso-eurusd-2026-05-07": "holdout-2"})
    material = tmp_path / "dos" / "libro.xlsx"
    _xlsx(material, FILAS)
    _declarar(repo2, material)
    r = ingerir(repo2, material, "Europe/Madrid", SESIONES, dias=["2026-05-07"])
    docs = [
        como_documento("caso-eurusd-2026-05-07", "2026-05-07", "EURUSD", ops, FUENTE)
        for d, ops in r.casos.items()
        if ops
    ]
    escribir(repo2, docs)
    problemas = problemas_de_biblioteca(repo2)
    assert any("holdout-2" in p and "RESERVADA" in p for p in problemas), problemas


@pytest.mark.contract
def test_el_agregado_no_se_lee_aunque_viva_en_el_mismo_fichero(tmp_path: Path) -> None:
    """La mitad NUEVA del principio, y la que nadie habia probado nunca (ADR-0037 §1).

    La pestana `Resumen` del fixture son bytes que no son XML: si la ingesta la tocara, reventaria.
    Que la ingesta funcione ES la prueba de que no la toco.
    """
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, FILAS, con_agregado=True)
    _declarar(repo, material)
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert len(r.casos["2026-05-08"]) == 1

    # Y el agregado no es alcanzable desde el camino soportado: `ingerir` NO tiene con que
    # pedir otra pestana. La constante es fija, y esto se rompe si alguien la hace parametro.
    from botsito.cases import ingesta

    assert ingesta.PESTANA == "backtesting-analytics"
    assert "pestana" not in ingerir.__code__.co_varnames, (
        "si `ingerir` acepta la pestana por argumento, existe un camino que abre el agregado"
    )

    # Y cuando la esperada NO esta, el error no nombra las que si estan.
    otro = tmp_path / "otro.xlsx"
    _xlsx(otro, FILAS, con_agregado=True)
    with pytest.raises(LibroError, match="no tiene la pestana esperada"):
        filas_de_los_dias(
            otro,
            {"2026-05-08"},
            "la-que-no-esta",
            COLS,
            _decl(otro),
            huso_de_los_dias="Europe/Madrid",
        )


@pytest.mark.contract
def test_el_invariante_geometrico_aborta_nombrando_la_fila(tmp_path: Path) -> None:
    """Un stop del lado equivocado es un intercambio de columnas, el fallo mas caro y mas mudo.

    Lo puso el consultor como higiene, y fue lo que cazo que `idealTP` no era el objetivo.
    """
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, ["2026/05/08 07:30:00", "buy", "1.1000", "1.1010", "", "1.1"]])
    _declarar(repo, material)
    with pytest.raises(IngestaError, match="del lado equivocado"):
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])


@pytest.mark.contract
def test_una_fila_sin_stop_no_produce_caso_y_se_cuenta(tmp_path: Path) -> None:
    """No se cae en silencio: a la sesion 1 un caso sin constancia le costo dos dias."""
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, ["2026/05/08 07:30:00", "buy", "1.1000", "", "", "1.1"]])
    _declarar(repo, material)
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert r.sin_stop == 1 and r.casos["2026-05-08"] == []


@pytest.mark.contract
def test_el_lector_no_publica_el_conjunto_de_fechas_ni_de_columnas(tmp_path: Path) -> None:
    """Un "14 dias en el libro" publica que dias reservados NO opero el trader (ADR-0037 §6)."""
    material = tmp_path / "libro.xlsx"
    _xlsx(material, FILAS)
    filas = filas_de_los_dias(
        material,
        {"2026-05-08"},
        "backtesting-analytics",
        COLS,
        _decl(material),
        huso_de_los_dias="Europe/Madrid",
    )
    assert len(filas) == 1
    # Lo devuelto habla SOLO del dia pedido: ninguna otra fecha del libro aparece.
    texto = repr(filas)
    for otra in ("2026/05/07", "2026-05-07", "2026/05/12", "2026-05-12"):
        assert otra not in texto, f"el lector publica {otra}, que no se pidio"

    # Y el error de estructura nombra lo ESPERADO que falta, nunca lo encontrado.
    with pytest.raises(LibroError) as exc:
        filas_de_los_dias(
            material,
            {"2026-05-08"},
            "backtesting-analytics",
            ["inventada"],
            _decl(material),
            huso_de_los_dias="Europe/Madrid",
        )
    assert "inventada" in str(exc.value)
    for encontrada in ("dateStart", "entryPrice", "maxTP", "idealTP"):
        assert encontrada not in str(exc.value), "el error publica las columnas encontradas"


@pytest.mark.contract
def test_ningun_numero_de_la_salida_cuenta_el_libro_entero(tmp_path: Path) -> None:
    """Medido el 2026-09-22 (MAYO-DEV) antes de leer el libro real de mayo, que es el PRIMERO con
    dias reservados cuyas filas se leen. Los contadores ya contaban solo las pedidas, pero los
    errores nombraban la fila por su POSICION EN EL LIBRO -«fila 12»-, y esa posicion cuenta las
    filas de los dias no pedidos que van delante: un recuento sobre el libro entero, el agregado
    de ADR-0037. Aqui van 10 filas NO pedidas -y sin stop- delante de las pedidas."""
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    no_pedida = ["2026/05/07 08:00:00", "buy", "1.2000", "", "", ""]
    material = tmp_path / "libro.xlsx"
    _xlsx(
        material,
        [
            CABECERA,
            *[no_pedida] * 10,
            ["2026/05/08 07:30:00", "buy", "1.1000", "1.0990", "", ""],
            ["2026/05/08 08:30:00", "sell", "1.1000", "", "", ""],
            *[no_pedida] * 5,
        ],
    )
    _declarar(repo, material)
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert (r.filas_leidas, r.sin_stop) == (2, 1), "cuentan las PEDIDAS, no las 17 del libro"

    _xlsx(material, [CABECERA, *[no_pedida] * 10, ["2026/05/08 07:30:00", "hold", "1.1", "1.0"]])
    _declarar(repo, material)
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert "el caso del dia 2026-05-08, operacion 1: `side`" in str(exc.value)
    assert "12" not in str(exc.value) and "07:30" not in str(exc.value)

    _xlsx(material, [CABECERA, *[no_pedida] * 10, ["ayer", "buy", "1.1", "1.0"]])
    _declarar(repo, material)
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert "no casa con ningun formato declarado" in str(exc.value)
    assert "12" not in str(exc.value) and "ayer" not in str(exc.value)


def _un_caso_valido(tmp_path: Path) -> tuple[Path, dict[str, object]]:
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    op = Operacion("2026-05-08T07:30:00+00:00", "07-11", "compra", Decimal("1.1"), Decimal("1.0"))
    doc = como_documento("caso-eurusd-2026-05-08", "2026-05-08", "EURUSD", [op], FUENTE)
    escribir(repo, [doc])
    assert problemas_de_biblioteca(repo) == [], "el caso bien formado pasa"
    return repo, doc


@pytest.mark.contract
def test_el_caso_no_lleva_objetivo_y_la_guardia_lo_caza_arriba(tmp_path: Path) -> None:
    """ADR-0037 §7 decia que el campo no existia y `como_documento` lo escribia, con un texto
    que decia «NO ES UN CAMPO». Medido el 2026-09-22 antes de commitear los primeros casos."""
    repo, doc = _un_caso_valido(tmp_path)
    assert "objetivo" not in doc
    escribir(repo, [{**doc, "objetivo": "1.1030"}])
    assert any("sobran ['objetivo']" in p for p in problemas_de_biblioteca(repo))


@pytest.mark.contract
def test_la_guardia_caza_maxtp_dentro_de_una_operacion(tmp_path: Path) -> None:
    """`maxTP` e `idealTP` viven a nivel de OPERACION: la lista cerrada va tambien ahi."""
    repo, doc = _un_caso_valido(tmp_path)
    ops = doc["operaciones"]
    assert isinstance(ops, list)
    escribir(repo, [{**doc, "operaciones": [{**ops[0], "maxTP": "1.1030"}]}])
    problemas = problemas_de_biblioteca(repo)
    assert any("exactamente" in p and "operacion 1" in p for p in problemas)


@pytest.mark.contract
def test_la_lista_cerrada_caza_una_clave_que_nadie_penso(tmp_path: Path) -> None:
    """El valor de una lista cerrada es que caza lo que no se enumero: en los tres niveles."""
    repo, doc = _un_caso_valido(tmp_path)
    ops = doc["operaciones"]
    fuente = doc["fuente"]
    assert isinstance(ops, list) and isinstance(fuente, dict)
    for roto in (
        {**doc, "nota_del_analista": "cerro en 3R"},
        {**doc, "operaciones": [{**ops[0], "cierre": "1.1030"}]},
        {**doc, "fuente": {**fuente, "rpnl": "300"}},
        {**doc, "dia": "2026-05-09"},
    ):
        escribir(repo, [roto])
        assert problemas_de_biblioteca(repo), f"no la caza: {sorted(roto)}"


# LA FRONTERA DE DIA ENTRE UTC Y MADRID (2026-09-22, MAYO-DEV). El libro viene en UTC y los dias
# del reparto son de `huso_operativa`: el lector comparaba la fecha UTC. Es el huso OTRA VEZ.
MADRID = "Europe/Madrid"


def _ingerir_filas(
    tmp_path: Path, filas: list[list[str]], dias: dict[str, str]
) -> tuple[Resultado | None, str]:
    repo = _repo(tmp_path, {c: "dev" for c in dias.values()})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, *filas])
    _declarar(repo, material)
    try:
        return ingerir(repo, material, MADRID, SESIONES, dias=dias), ""
    except IngestaError as exc:
        return None, str(exc)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("utc", "madrid"),
    [
        ("2026/05/08 23:00:00", "verano, UTC+2: el 09 a la 01:00"),
        ("2026/01/08 23:30:00", "invierno, UTC+1: el 09 a las 00:30"),
    ],
)
def test_a_una_fila_del_dia_pedido_en_utc_que_en_madrid_es_otro_dia_no_se_lee(
    tmp_path: Path, utc: str, madrid: str
) -> None:
    """(a) La fila es del dia pedido EN UTC pero del SIGUIENTE en Madrid -que puede estar
    reservado-. Antes pasaba el filtro y su instante salia en el error de sesion. Ahora no se
    lee: no cuenta en ningun contador y no aparece en ningun mensaje."""
    dia = utc[:10].replace("/", "-")
    buena = [f"{utc[:10]} 07:30:00", "buy", "1.1000", "1.0990", "", ""]
    fuera = [utc, "sell", "1.2345", "1.2400", "", ""]
    r, err = _ingerir_filas(tmp_path, [buena, fuera], {dia: f"caso-eurusd-{dia}"})
    assert err == "", f"{madrid}: la fila de otro dia no puede llegar a la ingesta: {err}"
    assert r is not None
    assert (r.filas_leidas, r.sin_stop) == (1, 0), madrid
    ops = r.casos[dia]
    assert [str(o.entrada) for o in ops] == ["1.1000"]


@pytest.mark.contract
@pytest.mark.parametrize(
    ("utc", "dia_madrid"),
    [
        ("2026/05/07 22:30:00", "2026-05-08"),  # verano: 00:30 del 08 en Madrid
        ("2026/01/07 23:30:00", "2026-01-08"),  # invierno: 00:30 del 08 en Madrid
    ],
)
def test_b_c_la_madrugada_de_un_dia_pedido_si_entra_en_verano_y_en_invierno(
    tmp_path: Path, utc: str, dia_madrid: str
) -> None:
    """(b) y (c) La fila es del dia pedido EN MADRID y del anterior en UTC: antes se perdia. El
    desfase no es el mismo en verano que en invierno, y por eso van los dos."""
    fila = [utc, "buy", "1.1000", "1.0990", "", ""]
    repo = _repo(tmp_path, {f"caso-eurusd-{dia_madrid}": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, fila])
    _declarar(repo, material)
    filas = filas_de_los_dias(
        material,
        {dia_madrid},
        "backtesting-analytics",
        COLS,
        _decl(material),
        huso_de_los_dias=MADRID,
    )
    assert [f["_dia"] for f in filas] == [dia_madrid]
    # Y la ingesta la ve como del dia pedido: la rechaza por SESION (00:30 no cae en ninguna),
    # nombrando el caso y no el instante ni los precios.
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, MADRID, SESIONES, dias={dia_madrid: f"caso-eurusd-{dia_madrid}"})
    msg = str(exc.value)
    assert msg.startswith(f"caso-eurusd-{dia_madrid}, operacion 1: su apertura no cae")
    assert "1.1000" not in msg and "1.0990" not in msg and ":30" not in msg


@pytest.mark.contract
def test_los_mensajes_nombran_el_caso_y_la_comprobacion_no_el_instante_ni_los_precios(
    tmp_path: Path,
) -> None:
    """Una puerta no puede depender de que otra este bien: aunque el filtro fallara, el mensaje
    no puede ser la via por la que salga una fila."""
    mala = ["2026/05/08 07:30:00", "buy", "1.1000", "1.1010", "", ""]  # stop del lado malo
    _, err = _ingerir_filas(tmp_path, [mala], {"2026-05-08": "caso-eurusd-2026-05-08"})
    assert err.startswith("caso-eurusd-2026-05-08, operacion 1: falla el invariante geometrico")
    assert "1.1000" not in err and "1.1010" not in err and "07:30" not in err
