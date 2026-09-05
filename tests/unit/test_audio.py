"""Corte por muestras con silencios (F04): reglas puras, fixture sintetico y extraccion."""

import shutil
import wave
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from botsito.corpus.audio import (
    MUESTRAS_S,
    AudioError,
    ParametrosCorte,
    Silencio,
    cortar_wav,
    detectar_silencios,
    duracion_wav_s,
    extraer_wav,
    muestras_wav,
    puntos_de_corte,
)

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "audio" / "tono_silencio_tono_10s.wav"
CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"
P = ParametrosCorte(objetivo_s=30.0, min_s=20.0, max_s=40.0)


def _requiere_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg no disponible")


def m(segundos: float) -> int:
    return round(segundos * MUESTRAS_S)


def test_sin_silencios_corta_en_el_objetivo_y_cuenta_forzados() -> None:
    c = puntos_de_corte(m(100), [], P)
    # El resto (40 s) cabe en MAX: no se corta mas (ultimo fragmento <= MAX).
    assert c.puntos_m == [0, m(30), m(60), m(100)]
    assert c.forzados_m == [m(30), m(60)]


def test_elige_el_silencio_mas_cercano_al_objetivo_y_desempata_por_el_mas_temprano() -> None:
    silencios = [Silencio(m(27.5), m(28.5)), Silencio(m(32.5), m(33.5))]
    assert puntos_de_corte(m(100), silencios, P).puntos_m[1] == m(28)  # |28-30| < |33-30|
    empate = [Silencio(m(26.5), m(27.5)), Silencio(m(32.5), m(33.5))]
    assert puntos_de_corte(m(100), empate, P).puntos_m[1] == m(27)
    fuera = [Silencio(m(14.5), m(15.5))]  # fuera de [20, 40]: se ignora y se fuerza en 30
    c = puntos_de_corte(m(100), fuera, P)
    assert c.puntos_m[1] == m(30) and c.forzados_m == [m(30), m(60)]
    cruza = [Silencio(m(29.5), m(31.0))]
    assert puntos_de_corte(m(100), cruza, P).puntos_m[1] == (m(29.5) + m(31.0)) // 2


def test_audio_corto_no_se_corta_y_parametros_invalidos() -> None:
    assert puntos_de_corte(m(40), [], P).puntos_m == [0, m(40)]
    with pytest.raises(AudioError):
        puntos_de_corte(0, [], P)
    with pytest.raises(AudioError, match="min_s <= objetivo_s <= max_s"):
        ParametrosCorte(objetivo_s=10.0, min_s=20.0, max_s=40.0)


@given(
    n=st.integers(min_value=1, max_value=MUESTRAS_S * 400),
    silencios=st.lists(
        st.integers(min_value=0, max_value=MUESTRAS_S * 400), min_size=0, max_size=30
    ),
)
def test_invariantes_del_corte(n: int, silencios: list[int]) -> None:
    lista = [Silencio(x, x + MUESTRAS_S) for x in sorted(set(silencios))]
    c = puntos_de_corte(n, lista, P)
    pts = c.puntos_m
    assert pts[0] == 0 and pts[-1] == n
    assert all(b > a for a, b in zip(pts, pts[1:], strict=False))
    tamanos = [b - a for a, b in zip(pts, pts[1:], strict=False)]
    assert all(t <= m(40) for t in tamanos)
    assert all(t >= m(20) for t in tamanos[:-1])
    assert set(c.forzados_m) <= set(pts)


def test_silencios_y_corte_sobre_el_fixture(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    assert muestras_wav(FIXTURE) == 10 * MUESTRAS_S and duracion_wav_s(FIXTURE) == 10.0
    silencios = detectar_silencios(FIXTURE, umbral_db=-40.0, minimo_s=0.5)
    assert len(silencios) == 1
    assert abs(silencios[0].inicio_m - m(3.0)) <= m(0.05)
    assert abs(silencios[0].fin_m - m(5.0)) <= m(0.05)
    p = ParametrosCorte(objetivo_s=5.0, min_s=3.0, max_s=7.0)
    c = puntos_de_corte(10 * MUESTRAS_S, silencios, p)
    assert c.puntos_m == [0, silencios[0].centro_m, 10 * MUESTRAS_S] and c.forzados_m == []
    assert abs(silencios[0].centro_m - m(4.0)) <= m(0.05)
    fragmentos = cortar_wav(FIXTURE, c.puntos_m, tmp_path / "frag")
    assert [(f.indice, f.inicio_m, f.fin_m) for f in fragmentos] == [
        (0, 0, c.puntos_m[1]),
        (1, c.puntos_m[1], 10 * MUESTRAS_S),
    ]
    assert fragmentos[1].inicio_ms == c.puntos_m[1] * 1000 // MUESTRAS_S
    with wave.open(str(fragmentos[1].ruta), "rb") as w:
        assert w.getframerate() == MUESTRAS_S and w.getnframes() == 10 * MUESTRAS_S - c.puntos_m[1]
    with pytest.raises(AudioError, match="vacio"):
        cortar_wav(FIXTURE, [0, m(4), m(4)], tmp_path / "x")


def test_extraer_wav_es_bit_a_bit_reproducible(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    a, b = tmp_path / "a" / "audio.wav", tmp_path / "b" / "audio.wav"
    extraer_wav(CLIP, a)
    extraer_wav(CLIP, b)
    assert a.read_bytes() == b.read_bytes() and abs(duracion_wav_s(a) - 2.0) < 0.1
    assert not (tmp_path / "a" / "audio.wav.tmp").exists()
    with pytest.raises(AudioError, match="no existe"):
        extraer_wav(tmp_path / "nada.mp4", tmp_path / "x.wav")


def test_wav_con_formato_distinto_rechazado(tmp_path: Path) -> None:
    ruta = tmp_path / "44k.wav"
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(44100)
        w.writeframes(b"\x00\x00" * 4)
    with pytest.raises(AudioError, match="16000 Hz"):
        muestras_wav(ruta)
