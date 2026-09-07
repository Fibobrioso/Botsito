"""Localizacion de citas por tokens con tiempo por palabras (F07, ADR-0009)."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from botsito.evidence.verificacion import (
    TOLERANCIA_CITA_MS,
    CitaError,
    comprobar_referencias,
    localizar_cita,
    tokens,
    tokens_de_segmento,
    trozos_de_cita,
)


@dataclass(frozen=True)
class P:
    t0_ms: int
    t1_ms: int
    texto: str


@dataclass(frozen=True)
class S:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str
    senales: tuple[str, ...] = ()
    palabras: tuple[P, ...] = ()


def _seg(n: int, t0: int, texto: str, paso: int = 500, senales: tuple[str, ...] = ()) -> S:
    """Segmento con una palabra cada `paso` ms, a partir del texto."""
    palabras = []
    t = t0
    for w in texto.split():
        palabras.append(P(t, t + paso, w))
        t += paso
    return S(n, t0, t, texto, senales, tuple(palabras))


def test_tokens_normaliza_como_el_brief() -> None:
    assert tokens("Break-even 0,75 1:3 M15 ¿vale? se... Ah 1.19537 33 9.65") == [
        "break",
        "even",
        "0,75",
        "1:3",
        "m15",
        "vale",
        "se",
        "ah",
        "1.19537",
        "33",
        "9.65",
    ]
    assert tokens("órdenes") == ["órdenes"]  # acentos conservados
    assert tokens("…") == []


def test_trozos_y_comodines() -> None:
    assert trozos_de_cita("uno dos tres cuatro") == [["uno", "dos", "tres", "cuatro"]]
    assert trozos_de_cita("uno dos tres [...] cuatro cinco seis") == [
        ["uno", "dos", "tres"],
        ["cuatro", "cinco", "seis"],
    ]
    with pytest.raises(CitaError, match="maximo"):
        trozos_de_cita("a b c [...] d e f [...] g h i [...] j k l")
    with pytest.raises(CitaError, match="trozo"):
        trozos_de_cita("a b [...] c d e")
    with pytest.raises(CitaError, match="minimo"):
        trozos_de_cita("solo tres tokens")
    with pytest.raises(CitaError, match="corchetes"):
        trozos_de_cita("uno dos tres [cuatro] cinco")
    with pytest.raises(CitaError, match="vacio"):
        trozos_de_cita("[...] uno dos tres cuatro")


def test_localiza_por_tokens_y_devuelve_tiempo_de_palabra() -> None:
    segs = [_seg(0, 0, "apenas rompe esto o cierra la vela pues ya proteges y")]
    loc = localizar_cita(segs, 0, 5000, "cierra la vela pues ya proteges")
    assert loc.segmentos == (0,) and loc.coincidencias == 1 and loc.trozos == 1
    assert loc.t0_ms == 2000 and loc.t1_ms == 5000  # palabras 5..10
    assert loc.avisos == ()


def test_tres_no_casa_dentro_de_treinta_y_tres_ni_1_3_en_11_3() -> None:
    segs = [_seg(0, 0, "limito a 33 y mi rr es 11.3 vale")]
    with pytest.raises(CitaError, match="no se localiza"):
        localizar_cita(segs, 0, 5000, "limito a 3 y mi")
    with pytest.raises(CitaError, match="no se localiza"):
        localizar_cita(segs, 0, 5000, "mi rr es 1.3 vale")


def test_coma_y_punto_no_son_equivalentes_a_proposito() -> None:
    segs = [_seg(0, 0, "el stop en 0.75 siempre vale")]
    assert localizar_cita(segs, 0, 5000, "el stop en 0.75 siempre").coincidencias == 1
    with pytest.raises(CitaError):
        localizar_cita(segs, 0, 5000, "el stop en 0,75 siempre")


def test_cruza_dos_segmentos_y_borde_de_ventana() -> None:
    a = _seg(0, 0, "tienes un cartucho todavia para")
    b = _seg(1, 2500, "poder seguir operando entonces")
    loc = localizar_cita([a, b], 0, 5000, "cartucho todavia para poder seguir")
    assert loc.segmentos == (0, 1)
    # La ventana solo toca el primer segmento: el segundo trozo no esta.
    with pytest.raises(CitaError):
        localizar_cita([a, b], 0, 200, "cartucho todavia para poder seguir")


def test_fuera_de_la_ventana_en_tiempo_aunque_el_segmento_la_toque() -> None:
    largo = _seg(0, 0, " ".join(f"w{i}" for i in range(100)))  # 50 s, una palabra cada 0,5 s
    with pytest.raises(CitaError, match="ajusta t0/t1"):
        localizar_cita([largo], 0, 1000, "w90 w91 w92 w93")
    loc = localizar_cita([largo], 45000, 47000, "w90 w91 w92 w93")
    assert loc.t0_ms == 45000 and loc.t1_ms == 47000


def test_elipsis_del_asr_y_guiones() -> None:
    segs = [_seg(0, 0, "se... Ah, vale. no, es que la orden break-even")]
    loc = localizar_cita(segs, 0, 9000, "se ah vale no es que la orden break even")
    assert loc.coincidencias == 1
    with pytest.raises(CitaError):
        localizar_cita(segs, 0, 9000, "la orden breakeven vale ok")


def test_orden_estricto_y_coincidencias_multiples() -> None:
    segs = [_seg(0, 0, "vale vale vale vale mira esto vale vale vale vale mira esto")]
    loc = localizar_cita(segs, 0, 9000, "vale vale vale vale [...] mira esto vale")
    assert loc.coincidencias == 2 and loc.trozos == 2
    with pytest.raises(CitaError, match="orden"):
        localizar_cita(segs, 0, 9000, "mira esto vale [...] vale vale vale vale")


def test_sin_palabras_cae_al_segmento_con_aviso_y_senales() -> None:
    s = S(3, 1000, 4000, "uno dos tres cuatro", ("no_habla",), ())
    loc = localizar_cita([s], 1000, 4000, "uno dos tres cuatro")
    assert loc.t0_ms == 1000 and loc.t1_ms == 4000 and loc.senales == ("no_habla",)
    assert loc.avisos and "sin palabras" in loc.avisos[0]
    roto = S(4, 0, 2000, "uno dos tres cuatro", (), (P(0, 1000, "uno"),))
    toks, aviso = tokens_de_segmento(roto)
    assert aviso and "no reproducen" in aviso and all(t.t0_ms == 0 for t in toks)


def test_tolerancia_por_defecto() -> None:
    segs = [_seg(0, 10000, "uno dos tres cuatro")]
    assert localizar_cita(segs, 10000 + TOLERANCIA_CITA_MS, 13000, "uno dos tres cuatro")
    with pytest.raises(CitaError):
        localizar_cita(segs, 10000 + TOLERANCIA_CITA_MS + 1, 13000, "uno dos tres cuatro")


REFS = {"fr-v4-9ad0ebb8/750000", "fr-v4-9ad0ebb8/751000", "Material adicional/a.xlsx"}


@pytest.mark.parametrize(
    ("modalidad", "fotos", "esperado"),
    [
        ("audio", [], []),
        ("audio", ["fr-v4-9ad0ebb8/750000"], ["no admite"]),
        ("pantalla", [], ["exige al menos"]),
        ("pantalla", ["fr-v4-9ad0ebb8/750000"], []),
        ("ambas", ["fr-v4-9ad0ebb8/750000", "Material adicional/a.xlsx"], []),
        ("pantalla", ["Material adicional/a.xlsx"], ["exige al menos"]),
        ("pantalla", ["fr-v4-9ad0ebb8/999000"], ["no conocida"]),
        ("pantalla", ["fr-v1-9ad0ebb8/750000"], ["no conocida"]),
        ("pantalla", ["fr-v4-9ad0ebb8/751000"], []),
    ],
)
def test_comprobar_referencias(modalidad: str, fotos: list[str], esperado: list[str]) -> None:
    problemas = comprobar_referencias("v4", 749000, 750000, modalidad, fotos, REFS)
    assert len(problemas) == len(esperado)
    for e in esperado:
        assert any(e in p for p in problemas)


def test_referencia_de_otro_video_y_fuera_del_tramo() -> None:
    refs = {"fr-v1-5a2a42c3/10000", "fr-v4-9ad0ebb8/750000"}
    p = comprobar_referencias("v4", 749000, 750000, "pantalla", ["fr-v1-5a2a42c3/10000"], refs)
    assert any("es del video 'v1'" in x for x in p)
    p = comprobar_referencias("v4", 700000, 701000, "pantalla", ["fr-v4-9ad0ebb8/750000"], refs)
    assert any("fuera del tramo" in x for x in p)
