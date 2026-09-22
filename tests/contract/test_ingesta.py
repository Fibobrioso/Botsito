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
from pathlib import Path

import pytest

from botsito.cases.biblioteca import como_documento, escribir, problemas_de_biblioteca
from botsito.cases.ingesta import IngestaError, dias_ingeribles, ingerir
from botsito.corpus.libro import LibroError, filas_de_los_dias

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

    pedidos = dias_ingeribles(repo).dias
    assert set(pedidos) == {"2026-05-08", "2026-05-12"}, "el dia reservado no se deriva"

    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=list(pedidos))
    assert r.filas_leidas == 2, "solo se leen las filas de los dias pedidos"
    assert sorted(d for d, ops in r.casos.items() if ops) == ["2026-05-08", "2026-05-12"]
    op = r.casos["2026-05-08"][0]
    assert (op.direccion, str(op.entrada), str(op.stop)) == ("compra", "1.1000", "1.0990")
    assert op.sesion == "07-11"

    docs = [
        como_documento(pedidos[d], d, "EURUSD", ops, {"tipo": "prueba"})
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
    r = ingerir(repo2, material, "Europe/Madrid", SESIONES, dias=["2026-05-07"])
    docs = [
        como_documento("caso-eurusd-2026-05-07", "2026-05-07", "EURUSD", ops, {"tipo": "prueba"})
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
        filas_de_los_dias(otro, {"2026-05-08"}, "la-que-no-esta", COLS)


@pytest.mark.contract
def test_el_invariante_geometrico_aborta_nombrando_la_fila(tmp_path: Path) -> None:
    """Un stop del lado equivocado es un intercambio de columnas, el fallo mas caro y mas mudo.

    Lo puso el consultor como higiene, y fue lo que cazo que `idealTP` no era el objetivo.
    """
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, ["2026/05/08 07:30:00", "buy", "1.1000", "1.1010", "", "1.1"]])
    with pytest.raises(IngestaError, match="del lado equivocado"):
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])


@pytest.mark.contract
def test_una_fila_sin_stop_no_produce_caso_y_se_cuenta(tmp_path: Path) -> None:
    """No se cae en silencio: a la sesion 1 un caso sin constancia le costo dos dias."""
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev"})
    material = tmp_path / "libro.xlsx"
    _xlsx(material, [CABECERA, ["2026/05/08 07:30:00", "buy", "1.1000", "", "", "1.1"]])
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert r.sin_stop == 1 and r.casos["2026-05-08"] == []


@pytest.mark.contract
def test_el_lector_no_publica_el_conjunto_de_fechas_ni_de_columnas(tmp_path: Path) -> None:
    """Un "14 dias en el libro" publica que dias reservados NO opero el trader (ADR-0037 §6)."""
    material = tmp_path / "libro.xlsx"
    _xlsx(material, FILAS)
    filas = filas_de_los_dias(material, {"2026-05-08"}, "backtesting-analytics", COLS)
    assert len(filas) == 1
    # Lo devuelto habla SOLO del dia pedido: ninguna otra fecha del libro aparece.
    texto = repr(filas)
    for otra in ("2026/05/07", "2026-05-07", "2026/05/12", "2026-05-12"):
        assert otra not in texto, f"el lector publica {otra}, que no se pidio"

    # Y el error de estructura nombra lo ESPERADO que falta, nunca lo encontrado.
    with pytest.raises(LibroError) as exc:
        filas_de_los_dias(material, {"2026-05-08"}, "backtesting-analytics", ["inventada"])
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
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert (r.filas_leidas, r.sin_stop) == (2, 1), "cuentan las PEDIDAS, no las 17 del libro"

    _xlsx(material, [CABECERA, *[no_pedida] * 10, ["2026/05/08 07:30:00", "hold", "1.1", "1.0"]])
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert "la fila pedida 1 (2026-05-08T07:30:00+00:00)" in str(exc.value)
    assert "12" not in str(exc.value)

    _xlsx(material, [CABECERA, *[no_pedida] * 10, ["ayer", "buy", "1.1", "1.0"]])
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08"])
    assert "ilegible" in str(exc.value) and "12" not in str(exc.value)
