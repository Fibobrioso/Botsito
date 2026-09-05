"""Fusion en milisegundos, senales, JSONL, reanudacion y glosario (F04)."""

from pathlib import Path

import pytest

from botsito.corpus.audio import MUESTRAS_S, Fragmento
from botsito.corpus.glosario import (
    GlosarioError,
    aplicar,
    correcciones_jsonl,
    glosario_desde_texto,
)
from botsito.corpus.transcripcion import (
    MotorFalso,
    Palabra,
    Segmento,
    SegmentoRelativo,
    TranscripcionError,
    a_jsonl,
    a_texto_legible,
    desde_jsonl,
    formato_ms,
    fusionar,
    huecos,
    parse_ms,
    texto_entre,
    transcribir_fragmentos,
)


def frag(i: int, a_s: float, b_s: float, tmp_path: Path) -> Fragmento:
    return Fragmento(i, round(a_s * MUESTRAS_S), round(b_s * MUESTRAS_S), tmp_path / f"f{i}.wav")


def test_segmento_invariantes() -> None:
    with pytest.raises(TranscripcionError, match="tiempos"):
        Segmento(0, 5000, 5000, "x")
    with pytest.raises(TranscripcionError, match="vacio"):
        Segmento(0, 0, 1000, "   ")
    with pytest.raises(TranscripcionError, match="enteros"):
        Segmento(0, 0.5, 1000, "x")  # type: ignore[arg-type]
    with pytest.raises(TranscripcionError, match="fuera de rango"):
        Segmento(0, 1000, 2000, "hola", (Palabra(500, 900, "hola", 0.9),))
    with pytest.raises(TranscripcionError, match="senal desconocida"):
        Segmento(0, 0, 1000, "x", senales=("rara",))


def test_fusionar_aritmetica_exacta_recorte_y_descarte(tmp_path: Path) -> None:
    f0 = Fragmento(0, 0, 9_590_400, tmp_path / "f0.wav")  # termina en 599.4 s
    f1 = Fragmento(1, 9_590_400, 14_400_000, tmp_path / "f1.wav")  # empieza en 599.4 s
    r = fusionar(
        [
            (f0, [SegmentoRelativo(0.0, 10.0, "a"), SegmentoRelativo(598.9, 601.2, "cruza")]),
            (
                f1,
                [
                    SegmentoRelativo(0.52, 3.10, "hola", ((0.52, 0.9, " hola", 0.99),)),
                    SegmentoRelativo(400.0, 401.0, "fuera"),
                ],
            ),
        ],
        fin_wav_ms=900_000,
    )
    assert [(s.n, s.t0_ms, s.t1_ms, s.texto) for s in r.segmentos] == [
        (0, 0, 10000, "a"),
        (1, 598900, 599400, "cruza"),
        (2, 599920, 602500, "hola"),
    ]
    assert r.segmentos[2].palabras == (Palabra(599920, 600300, "hola", 0.99),)
    assert r.recortados == 1 and r.descartados == 1
    with pytest.raises(TranscripcionError, match="solapados"):
        fusionar(
            [(f0, [SegmentoRelativo(0.0, 10.0, "a"), SegmentoRelativo(5.0, 12.0, "b")])], 900_000
        )
    with pytest.raises(TranscripcionError, match="supera el fin"):
        fusionar([(frag(0, 0.0, 950.0, tmp_path), [SegmentoRelativo(0.0, 940.0, "a")])], 900_000)


def test_senales_por_segmento(tmp_path: Path) -> None:
    f0 = frag(0, 0.0, 100.0, tmp_path)
    r = fusionar(
        [
            (
                f0,
                [
                    SegmentoRelativo(0.0, 1.0, "vale, vale", compression_ratio=2.6),
                    SegmentoRelativo(1.0, 2.0, "Vale,  vale", avg_logprob=-1.5),
                    SegmentoRelativo(2.0, 3.0, "otra", no_speech_prob=0.9),
                ],
            )
        ],
        100_000,
    )
    assert [s.senales for s in r.segmentos] == [
        ("compresion",),
        ("repeticion", "baja_prob"),
        ("no_habla",),
    ]
    assert "<repeticion,baja_prob>" in a_texto_legible(r.segmentos)


def test_huecos_incluye_inicio_y_final() -> None:
    segs = [
        Segmento(0, 40000, 50000, "a"),
        Segmento(1, 50000, 60000, "b"),
        Segmento(2, 100000, 110000, "c"),
    ]
    assert huecos(segs, 200000, minimo_s=30.0) == [
        {"desde_ms": 0, "hasta_ms": 40000, "ms": 40000},
        {"desde_ms": 60000, "hasta_ms": 100000, "ms": 40000},
        {"desde_ms": 110000, "hasta_ms": 200000, "ms": 90000},
    ]
    assert huecos([], 10000, minimo_s=30.0) == []


def test_jsonl_ida_y_vuelta_y_rechazos() -> None:
    segs = [
        Segmento(
            0,
            0,
            1500,
            "hola, ¿qué tal?",
            (Palabra(0, 400, "hola,", 0.99),),
            0.1,
            1.2,
            -0.3,
            ("compresion",),
        ),
        Segmento(1, 1500, 3000, "bien"),
    ]
    texto = a_jsonl(segs)
    assert texto.count("\n") == 2 and '"n":0' in texto and "¿" in texto
    assert desde_jsonl(texto) == segs and a_jsonl([]) == "" and desde_jsonl("") == []
    with pytest.raises(TranscripcionError, match="fuera de orden"):
        desde_jsonl(texto.replace('"n":1', '"n":7'))
    with pytest.raises(TranscripcionError, match="linea 1"):
        desde_jsonl("{")
    with pytest.raises(TranscripcionError, match="solapados"):
        desde_jsonl(a_jsonl([Segmento(0, 0, 5000, "a")]) + a_jsonl([Segmento(1, 3000, 6000, "b")]))


def test_tiempos_h_mm_ss() -> None:
    assert formato_ms(3723456) == "1:02:03.456" and parse_ms("1:02:03.456") == 3723456
    assert parse_ms("0:31:59") == 1919000 and parse_ms("0:00:01.5") == 1500
    for malo in ("31:59", "0:61:00", "0:00:60", "x:00:00"):
        with pytest.raises(TranscripcionError):
            parse_ms(malo)


def test_transcribir_fragmentos_es_reanudable_y_sensible_a_parametros(tmp_path: Path) -> None:
    llamadas: list[str] = []
    for i in range(2):
        (tmp_path / f"f{i}.wav").write_bytes(b"RIFF" + bytes([i]))

    def generar(wav: Path) -> list[SegmentoRelativo]:
        llamadas.append(wav.name)
        return [SegmentoRelativo(0.0, 1.0, f"de {wav.name}", ((0.0, 0.5, "de", 0.5),))]

    fragmentos = [frag(0, 0.0, 5.0, tmp_path), frag(1, 5.0, 10.0, tmp_path)]
    motor = MotorFalso(generar)
    r1 = transcribir_fragmentos(fragmentos, motor, tmp_path / "parciales", "h1")
    r2 = transcribir_fragmentos(fragmentos, motor, tmp_path / "parciales", "h1")
    assert llamadas == ["f0.wav", "f1.wav"] and r1 == r2
    transcribir_fragmentos(fragmentos, motor, tmp_path / "parciales", "h2")  # otros parametros
    assert llamadas == ["f0.wav", "f1.wav", "f0.wav", "f1.wav"]
    (tmp_path / "f0.wav").write_bytes(b"RIFF cambiado")  # otro WAV: se retranscribe
    transcribir_fragmentos(fragmentos, motor, tmp_path / "parciales", "h2")
    assert llamadas[-1:] == ["f0.wav"] and llamadas.count("f1.wav") == 2
    fusion = fusionar(r2, 10_000).segmentos
    assert texto_entre(fusion, 4900, 5100) == fusion[1:]
    assert texto_entre(fusion, 4900, 5100, margen_ms=5000) == fusion
    assert texto_entre(fusion, 500, 800) == fusion[:1]


GLOSARIO = r"""
vocabulario: [M15, M5, FTMO, FVG, cartucho, break even]
sustituciones:
  - patron: '\bbrequiven\b'
    reemplazo: 'break even'
    alcance: global
    motivo: 'break even fonetico'
    ejemplo_video: v4
    ejemplo_t0: '0:44:56'
  - patron: '\bcargo chuto\b'
    reemplazo: cartucho
    alcance: global
    motivo: 'jerga'
    ejemplo_video: v4
    ejemplo_t0: '0:48:41'
  - patron: '\bM5\b'
    reemplazo: M15
    alcance: segmento
    motivo: 'en pantalla se ve M15'
    ejemplo_video: v3
    ejemplo_t0: '0:16:05'
    transcripcion_id: tr-v3-large-v3-int8-float16-deadbeef
    segmento: 1
    verificado_por: aleks
"""


def test_glosario_dos_alcances_y_dudas() -> None:
    g = glosario_desde_texto(GLOSARIO)
    assert g.prompt_inicial == "M15, M5, FTMO, FVG, cartucho, break even"
    cruda = [
        Segmento(0, 0, 1000, "hago Brequiven en M5 y otro cargo chuto"),
        Segmento(1, 1000, 2000, "en M5 miro la mitigación"),
        Segmento(2, 2000, 3000, "año sin brequivenes"),
    ]
    corregida, registro, dudas = aplicar(cruda, g, "tr-v3-large-v3-int8-float16-deadbeef")
    assert [s.texto for s in corregida] == [
        "hago break even en M5 y otro cartucho",
        "en M15 miro la mitigación",
        "año sin brequivenes",
    ]
    assert [(c.segmento, c.alcance) for c in registro] == [
        (0, "global"),
        (0, "global"),
        (1, "segmento"),
    ]
    assert dudas == [0]  # M5 aparece en el segmento 0 sin corregir: F07 lo revisa
    otra, registro2, dudas2 = aplicar(cruda, g, "tr-v3-large-v3-int8-float16-00000000")
    assert otra[1].texto == "en M5 miro la mitigación" and dudas2 == [0, 1]
    assert aplicar(cruda, g, "tr-v3-large-v3-int8-float16-deadbeef")[0] == corregida
    texto = correcciones_jsonl(g, registro, dudas)
    assert texto.startswith('{"dudas": [0], "glosario_sha256": "') and texto.count("\n") == 4


def _entrada(patron: str, alcance: str = "global", **extra: str) -> str:
    base = (
        f"patron: '{patron}', reemplazo: y, alcance: {alcance}, motivo: m, "
        "ejemplo_video: v1, ejemplo_t0: '0:00:01'"
    )
    resto = "".join(f", {k}: {v}" for k, v in extra.items())
    return "{" + base + resto + "}"


@pytest.mark.parametrize(
    ("entrada", "mensaje"),
    [
        (_entrada("M5"), "limites"),
        (_entrada(r"\bM5\b"), "vocabulario"),
        (_entrada(r"\b.*\b"), "comodines"),
        (_entrada(r"\b(\b"), "invalido"),
        (_entrada(r"\bx\b", "segmento"), "campos esperados"),
        (_entrada(r"\bx\b", "otro"), "alcance"),
    ],
)
def test_glosario_rechazos(entrada: str, mensaje: str) -> None:
    with pytest.raises(GlosarioError, match=mensaje):
        glosario_desde_texto(f"vocabulario: [M5]\nsustituciones:\n  - {entrada}\n")


def test_glosario_unicode_respeta_limites() -> None:
    entrada = _entrada(r"\ban\b").replace("reemplazo: y", "reemplazo: en")
    g = glosario_desde_texto("sustituciones:\n  - " + entrada + "\n")
    corregida, registro, _ = aplicar([Segmento(0, 0, 1000, "cada año AN tal")], g)
    assert corregida[0].texto == "cada año en tal" and len(registro) == 1
