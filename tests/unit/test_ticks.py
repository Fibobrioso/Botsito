"""Ticks congelados (ADR-0051, Fase 2 de `trabajo/ticks-llenado`), sin tocar la red: la URL por
horas, el decodificador `>IIIff`, la cache por hora, una hora perdida tras los reintentos que no
aborta y queda en el manifiesto, el CSV por dia que se relee igual, el manifiesto validado con su
id atado a los hashes, la carga por ventana con el hash comprobado, y la compuerta de la CLI que
se niega a un mes que no sea de construccion sin descargar nada."""

from __future__ import annotations

import lzma
import struct
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.data.dukascopy import DescargaError, FormatoBi5Error
from botsito.data.ticks import (
    CABECERA_CSV,
    CongeladoTicks,
    TicksError,
    buscar_manifiesto_ticks,
    cargar_manifiesto_ticks,
    cargar_ticks,
    comprobar_ticks,
    con_cache_horas,
    congelar_ticks,
    decodificar_ticks,
    descargar_hora,
    escribir_csv_ticks,
    formato_ts_ms,
    leer_csv_ticks,
    minutos_con_ticks,
    parse_ts_ms,
    url_hora,
)
from botsito.domain.ticks import Tick, TickInvalidoError

RAIZ = Path(__file__).resolve().parents[2]
REG = struct.Struct(">IIIff")
HOY = date(2030, 3, 1)


def bi5(*registros: tuple[int, int, int, float, float]) -> bytes:
    return lzma.compress(b"".join(REG.pack(*r) for r in registros))


def test_url_por_hora_con_mes_en_base_cero() -> None:
    assert url_hora("XXXYYY", date(2030, 1, 5), 7).endswith("/XXXYYY/2030/00/05/07h_ticks.bi5")
    assert "/2030/11/31/23h_ticks.bi5" in url_hora("XXXYYY", date(2030, 12, 31), 23)


def test_decodifica_una_hora_con_milisegundos_y_volumenes_en_milesimas() -> None:
    cuerpo = bi5((71, 115957, 115953, 1.8, 2.7), (124, 115957, 115955, 0.9, 1.8))
    ticks = decodificar_ticks(cuerpo, date(2030, 1, 7), 10)
    assert len(ticks) == 2
    assert formato_ts_ms(ticks[0].instante) == "2030-01-07T10:00:00.071Z"
    assert (ticks[0].ask, ticks[0].bid, ticks[0].spread) == (115957, 115953, 4)
    assert (ticks[0].volumen_ask, ticks[0].volumen_bid) == (1800, 2700)
    assert ticks[1].minuto == ticks[0].minuto
    assert decodificar_ticks(b"", date(2030, 1, 7), 10) == []


@pytest.mark.parametrize(
    ("cuerpo", "mensaje"),
    [
        (b"no es lzma", "no es LZMA"),
        (lzma.compress(b"\x00" * 21), "multiplo"),
        (bi5((3_600_000, 1, 1, 0.0, 0.0)), "fuera de la hora"),
        (bi5((5, 1, 1, 0.0, 0.0), (4, 1, 1, 0.0, 0.0)), "desordenados"),
        (bi5((5, 0, 1, 0.0, 0.0)), "no positivo"),
        (bi5((5, 1, 1, -1.0, 0.0)), "volumen invalido"),
    ],
)
def test_formato_invalido(cuerpo: bytes, mensaje: str) -> None:
    with pytest.raises(FormatoBi5Error, match=mensaje):
        decodificar_ticks(cuerpo, date(2030, 1, 7), 10)


def test_un_tick_no_admite_precios_ni_volumenes_invalidos() -> None:
    with pytest.raises(TickInvalidoError):
        Tick(1, 0, 1, 0, 0)  # type: ignore[arg-type]
    with pytest.raises(TickInvalidoError):
        Tick(-1, 1, 1, 0, 0)  # type: ignore[arg-type]


def test_una_hora_perdida_tras_los_reintentos_no_aborta(tmp_path: Path) -> None:
    def falla(url: str) -> bytes | None:
        raise DescargaError(url)

    h = descargar_hora("XXXYYY", date(2030, 1, 7), 10, falla)
    assert h.estado == "perdida" and h.ticks == ()
    assert descargar_hora("XXXYYY", date(2030, 1, 7), 10, lambda _u: None).estado == "ausente"
    assert descargar_hora("XXXYYY", date(2030, 1, 7), 10, lambda _u: b"").estado == "vacia"


def test_cache_por_hora(tmp_path: Path) -> None:
    llamadas: list[str] = []

    def descarga(url: str) -> bytes | None:
        llamadas.append(url)
        return None if url.endswith("/03h_ticks.bi5") else bi5((1, 2, 1, 0.0, 0.0))

    cacheada = con_cache_horas(tmp_path / "raw", descarga)
    u1, u3 = url_hora("XXXYYY", date(2030, 1, 7), 1), url_hora("XXXYYY", date(2030, 1, 7), 3)
    assert cacheada(u1) is not None and cacheada(u3) is None
    assert cacheada(u1) is not None and cacheada(u3) is None
    assert llamadas == [u1, u3]
    assert (tmp_path / "raw" / "XXXYYY" / "ticks" / "2030-01-07" / "01.bi5").exists()
    assert (tmp_path / "raw" / "XXXYYY" / "ticks" / "2030-01-07" / "03.404").exists()


def test_csv_de_ticks_ida_y_vuelta() -> None:
    ticks = decodificar_ticks(
        bi5((71, 115957, 115953, 1.8, 2.7), (999, 115958, 115954, 0.0, 0.1)), date(2030, 1, 7), 10
    )
    texto = escribir_csv_ticks(ticks)
    assert texto.startswith(CABECERA_CSV + "\n") and texto.endswith("\n")
    assert leer_csv_ticks(texto) == ticks
    assert parse_ts_ms("2030-01-07T10:00:00.071Z") == ticks[0].instante
    with pytest.raises(TicksError, match="cabecera"):
        leer_csv_ticks("x\n")
    with pytest.raises(TicksError, match="desordenados"):
        leer_csv_ticks(
            texto.split("\n")[0] + "\n" + texto.split("\n")[2] + "\n" + texto.split("\n")[1] + "\n"
        )
    with pytest.raises(TicksError, match="ts_utc invalido"):
        parse_ts_ms("2030-01-07T10:00Z")


def _descarga_falsa(url: str) -> bytes | None:
    """Dia 7: horas 10 y 11 con ticks, la 12 falla siempre (perdida), el resto 404. Dia 8: solo la
    hora 9. Dia 9: nada."""
    partes = url.split("/")
    dia, hora = int(partes[-2]), int(partes[-1][:2])
    if dia == 7 and hora in (10, 11):
        return bi5((5, 100_005, 100_001, 1.0, 1.0), (60_000, 100_010, 100_007, 1.0, 1.0))
    if dia == 7 and hora == 12:
        raise DescargaError(url)
    if dia == 8 and hora == 9:
        return bi5((0, 100_020, 100_015, 1.0, 1.0))
    return None


def _congelar(repo: Path, nombre: str = "prueba-ticks") -> CongeladoTicks:
    return congelar_ticks(
        repo,
        repo / "data",
        nombre,
        "XXXYYY",
        100_000,
        date(2030, 1, 7),
        date(2030, 1, 9),
        _descarga_falsa,
        hoy=HOY,
        generado_por="abc1234",
    )


def test_congelar_escribe_un_csv_por_dia_y_el_manifiesto_con_las_horas_perdidas(
    tmp_path: Path,
) -> None:
    c = _congelar(tmp_path)
    m = c.manifiesto
    assert m["dataset_id"].startswith("prueba-ticks-")
    assert [f.name for f in c.ficheros] == [
        "XXXYYY_TICKS_2030-01-07.csv",
        "XXXYYY_TICKS_2030-01-08.csv",
    ]
    assert m["horas"] == {
        "presentes": 3,
        "ausentes_404": 68,
        "vacias": 0,
        "perdidas": ["2030-01-07T12Z"],
    }
    assert m["ticks"] == {"total": 5, "cruzados_ask_menor_que_bid": 0}
    assert (
        m["ficheros"][0]["filas"] == 4 and m["ficheros"][0]["primera"] == "2030-01-07T10:00:00.005Z"
    )
    doc = cargar_manifiesto_ticks(c.ruta_manifiesto)
    assert comprobar_ticks(doc, tmp_path / "data", hashes=True) == []
    assert buscar_manifiesto_ticks(tmp_path, "prueba-ticks") == c.ruta_manifiesto
    assert not (tmp_path / "data" / "ticks" / "prueba-ticks.parcial").exists()
    # determinista e inmutable: el mismo contenido da el mismo id y no se sobreescribe
    otro = tmp_path / "otro"
    otro.mkdir()
    assert _congelar(otro).manifiesto["dataset_id"] == m["dataset_id"]
    with pytest.raises(TicksError, match="ya existe"):
        _congelar(tmp_path)


def test_cargar_por_ventana_comprueba_el_hash_y_lista_las_horas_perdidas(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    doc = cargar_manifiesto_ticks(c.ruta_manifiesto)
    desde = int(
        (datetime(2030, 1, 7, 11, tzinfo=UTC) - datetime(1970, 1, 1, tzinfo=UTC)).total_seconds()
        * 1000
    )
    serie = cargar_ticks(doc, tmp_path / "data", desde, desde + 3_600_000)
    assert len(serie.ticks) == 2 and serie.horas_perdidas == ("2030-01-07T12Z",)
    assert minutos_con_ticks(serie.ticks) == {desde // 60_000, desde // 60_000 + 1}
    todo = cargar_ticks(doc, tmp_path / "data")
    assert len(todo.ticks) == 5 and todo.escala == 100_000
    fichero = c.ficheros[0]
    fichero.write_bytes(fichero.read_bytes().replace(b"100005", b"100006"))
    with pytest.raises(TicksError, match="alterado"):
        cargar_ticks(doc, tmp_path / "data")
    assert comprobar_ticks(doc, tmp_path / "data", hashes=True) == [
        f"hash distinto: {doc['ficheros'][0]['ruta']}"
    ]


def test_manifiesto_editado_no_carga(tmp_path: Path) -> None:
    c = _congelar(tmp_path)
    ruta = c.ruta_manifiesto
    texto = ruta.read_text(encoding="utf-8")
    ruta.write_text(texto.replace("escala: 100000", "escala: 10"), encoding="utf-8")
    cargar_manifiesto_ticks(ruta)  # la escala no entra en el id: se acepta (como en las M1)
    ruta.write_text(texto.replace("filas: 4", "filas: 5"), encoding="utf-8")
    doc = cargar_manifiesto_ticks(ruta)
    with pytest.raises(TicksError, match="filas"):
        cargar_ticks(doc, tmp_path / "data")
    ruta.write_text(texto.replace(c.manifiesto["dataset_id"][-8:], "00000000"), encoding="utf-8")
    with pytest.raises(TicksError, match="no coincide con los hashes|debe llamarse"):
        cargar_manifiesto_ticks(ruta)


def test_la_cli_se_niega_a_un_mes_que_no_es_de_construccion(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli

    real = cargar_criterio(RAIZ)
    for mes in (*real.medida, "2026-02", "2026-03", "2026-09"):
        codigo = cli.main(
            [
                "--repo",
                str(RAIZ),
                "data",
                "download-ticks",
                "--dataset",
                "prueba-nunca",
                "--simbolo",
                "XXXYYY",
                "--escala",
                "100000",
                "--desde",
                f"{mes}-01",
                "--hasta",
                f"{mes}-02",
            ]
        )
        assert codigo == 2, mes
    salida = capsys.readouterr().out
    assert "no es de construccion" in salida and "ni se descarga" in salida
    assert (
        not list((RAIZ / "data" / "manifests" / "ticks").glob("prueba-nunca*"))
        if (RAIZ / "data" / "manifests" / "ticks").exists()
        else True
    )
    # un rango que cruza de construccion a otro mes tambien se niega entero
    assert cli.meses_fuera_de_construccion(RAIZ, date(2026, 4, 30), date(2026, 5, 1)) == ["2026-05"]
    assert cli.meses_fuera_de_construccion(RAIZ, date(2026, 8, 3), date(2026, 8, 4)) == []
