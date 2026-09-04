import lzma
import struct
from datetime import date
from pathlib import Path

import pytest

from botsito.data.dukascopy import (
    DescargaError,
    FormatoBi5Error,
    decodificar_bi5,
    descarga_http,
    descargar_dia,
    es_plana_sin_volumen,
    url_dia,
)
from botsito.data.velas import formato_ts

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ohlc"
REG = struct.Struct(">iiiiif")


def bi5(*registros: tuple[int, int, int, int, int, float]) -> bytes:
    return lzma.compress(b"".join(REG.pack(*r) for r in registros))


def test_url_con_mes_en_base_cero() -> None:
    assert url_dia("XXXYYY", date(2026, 3, 29)).endswith("/XXXYYY/2026/02/29/BID_candles_min_1.bi5")
    assert "/2026/00/05/" in url_dia("XXXYYY", date(2026, 1, 5), base="http://x")


def test_decodifica_y_descarta_planas() -> None:
    cuerpo = bi5((0, 5, 5, 5, 5, 0.0), (60, 5, 6, 4, 7, 12.5), (120, 6, 6, 6, 6, 0.0))
    velas, n = decodificar_bi5(cuerpo, date(2026, 7, 2))
    assert n == 3 and formato_ts(velas[1].inicio) == "2026-07-02T00:01Z"
    # el proveedor da (t, abierta, cierre, minima, maxima): el orden interno es o/h/l/c
    assert (velas[1].abierta, velas[1].maxima, velas[1].minima, velas[1].cierre) == (5, 7, 4, 6)
    assert velas[1].volumen == 12500  # 12.5 en milesimas (ESCALA_VOLUMEN)
    assert [es_plana_sin_volumen(v) for v in velas] == [True, False, True]
    dia = descargar_dia("XXXYYY", date(2026, 7, 2), lambda _url: cuerpo)  # jueves
    assert dia.presente and dia.registros == 3 and dia.descartadas == 2 and len(dia.velas) == 1
    # Las planas del principio y del final del dia no estan "dentro de sesion".
    assert dia.descartadas_dentro_de_sesion == 0 and dia.volumen_cero_no_planas == 0
    con_hueco = bi5((0, 5, 6, 4, 7, 1.0), (60, 6, 6, 6, 6, 0.0), (120, 6, 6, 5, 7, 1.0))
    dia_hueco = descargar_dia("XXXYYY", date(2026, 7, 2), lambda _url: con_hueco)
    assert dia_hueco.descartadas == 1 and dia_hueco.descartadas_dentro_de_sesion == 1
    dudosa = bi5((0, 5, 6, 4, 7, 0.0))  # precio se movio sin volumen: se conserva y se cuenta
    dia2 = descargar_dia("XXXYYY", date(2026, 7, 5), lambda _url: dudosa)  # domingo
    assert dia2.volumen_cero_no_planas == 1 and dia2.descartadas_dentro_de_sesion == 0


def test_dia_sin_fichero_y_vacio() -> None:
    dia = descargar_dia("XXXYYY", date(2026, 7, 4), lambda _url: None)
    assert not dia.presente and dia.velas == () and dia.registros == 0
    vacio = descargar_dia("XXXYYY", date(2026, 7, 4), lambda _url: b"")
    assert vacio.presente and vacio.registros == 0


@pytest.mark.parametrize(
    ("cuerpo", "mensaje"),
    [
        (b"no es lzma", "LZMA"),
        (lzma.compress(b"\x00" * 23), "multiplo"),
        (bi5((30, 1, 1, 1, 1, 0.0)), "marca de tiempo"),
        (bi5((86400, 1, 1, 1, 1, 0.0)), "marca de tiempo"),
        (bi5((60, 1, 1, 1, 1, 0.0), (60, 1, 1, 1, 1, 0.0)), "duplicados"),
        (bi5((120, 1, 1, 1, 1, 0.0), (60, 1, 1, 1, 1, 0.0)), "desordenados"),
        (bi5((0, 9, 1, 1, 1, 0.0)), "fuera de rango"),
        (bi5((0, 5, 6, 4, 7, float("nan"))), "volumen invalido"),
        (bi5((0, 5, 6, 4, 7, float("inf"))), "volumen invalido"),
        (bi5((0, 5, 6, 4, 7, -1.0)), "volumen invalido"),
        (lzma.compress(b"\x00" * (24 * 1441)), "mas de 1440"),
    ],
)
def test_formato_invalido(cuerpo: bytes, mensaje: str) -> None:
    with pytest.raises(FormatoBi5Error, match=mensaje):
        decodificar_bi5(cuerpo, date(2026, 7, 2))


def test_fixture_real_del_dia_del_caso() -> None:
    dia = descargar_dia(
        "EURUSD_FIXTURE",
        date(2026, 7, 2),
        lambda _url: (FIXTURES / "EURUSD_2026-07-02.bi5").read_bytes(),
    )
    assert dia.registros == 1440 and dia.descartadas == 3 and len(dia.velas) == 1437
    primera, ultima = dia.velas[0], dia.velas[-1]
    assert formato_ts(primera.inicio) == "2026-07-02T00:00Z"
    assert formato_ts(ultima.inicio) == "2026-07-02T23:59Z"
    assert all(v.minima <= v.abierta <= v.maxima for v in dia.velas)


def test_domingo_solo_tiene_la_apertura() -> None:
    dia = descargar_dia(
        "EURUSD_FIXTURE",
        date(2026, 3, 29),
        lambda _url: (FIXTURES / "EURUSD_2026-03-29.bi5").read_bytes(),
    )
    assert dia.registros == 1440 and formato_ts(dia.velas[0].inicio) == "2026-03-29T21:00Z"


def test_descarga_http_reintenta_y_falla_cerrado(monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.request

    llamadas: list[str] = []

    def falla(*_a: object, **_k: object) -> object:
        llamadas.append("x")
        raise TimeoutError("lento")

    monkeypatch.setattr(urllib.request, "urlopen", falla)
    monkeypatch.setattr("botsito.data.dukascopy.time.sleep", lambda _s: None)
    with pytest.raises(DescargaError, match="lento"):
        descarga_http("http://x", intentos=3, espera_s=0)
    assert len(llamadas) == 3


def test_cache_por_dia_reanuda(tmp_path: Path) -> None:
    from botsito.data.dukascopy import con_cache

    llamadas: list[str] = []

    def red(url: str) -> bytes | None:
        llamadas.append(url)
        return None if "/2026/02/01/" in url else b"cuerpo"

    d = con_cache(tmp_path / "raw", red)
    u1, u2 = url_dia("XXXYYY", date(2026, 3, 2)), url_dia("XXXYYY", date(2026, 3, 1))
    assert d(u1) == b"cuerpo" and d(u1) == b"cuerpo" and len(llamadas) == 1
    assert d(u2) is None and d(u2) is None and len(llamadas) == 2
    assert (tmp_path / "raw" / "XXXYYY" / "2026-03-02.bi5").read_bytes() == b"cuerpo"
    assert (tmp_path / "raw" / "XXXYYY" / "2026-03-01.404").exists()
    # Otra instancia sobre el mismo disco no vuelve a la red.
    assert con_cache(tmp_path / "raw", red)(u1) == b"cuerpo" and len(llamadas) == 2


def test_descarga_http_404_y_500(monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.error
    import urllib.request

    def responde(codigo: int) -> object:
        def f(*_a: object, **_k: object) -> object:
            raise urllib.error.HTTPError("http://x", codigo, "msg", {}, None)  # type: ignore[arg-type]

        return f

    esperas: list[float] = []
    monkeypatch.setattr("botsito.data.dukascopy.time.sleep", esperas.append)
    monkeypatch.setattr(urllib.request, "urlopen", responde(404))
    assert descarga_http("http://x", intentos=3, espera_s=1) is None and esperas == []
    monkeypatch.setattr(urllib.request, "urlopen", responde(503))
    with pytest.raises(DescargaError, match="503"):
        descarga_http("http://x", intentos=3, espera_s=1)
    assert esperas == [1, 2]  # no se duerme tras el ultimo intento
