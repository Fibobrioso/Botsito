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
    # Solape de milisegundos (Whisper lo hace): se recorta el segundo y se cuenta; palabra con
    # fin < inicio se iguala en vez de abortar.
    tol = fusionar(
        [
            (
                f0,
                [
                    SegmentoRelativo(0.0, 10.005, "a", ((2.0, 1.9, "x", 0.5),)),
                    SegmentoRelativo(10.0, 12.0, "b"),
                    SegmentoRelativo(11.99, 12.0, "c"),
                ],
            )
        ],
        900_000,
    )
    assert [(s.t0_ms, s.t1_ms) for s in tol.segmentos] == [(0, 10005), (10005, 12000)]
    assert tol.recortados == 2 and tol.descartados == 1
    assert tol.segmentos[0].palabras == (Palabra(2000, 2000, "x", 0.5),)
    # Fragmento cuyo fin en ms se trunca (floor) y motor que redondea: 1 ms de mas no es recorte.
    f_imp = Fragmento(0, 0, 9_590_407, tmp_path / "fi.wav")  # 599400.4375 ms -> fin_ms 599400
    borde = fusionar([(f_imp, [SegmentoRelativo(0.0, 599.4009, "a")])], 900_000)
    assert (borde.segmentos[0].t1_ms, borde.recortados) == (599400, 0)
    borde2 = fusionar([(f_imp, [SegmentoRelativo(0.0, 599.402, "a")])], 900_000)
    assert (borde2.segmentos[0].t1_ms, borde2.recortados) == (599400, 1)
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
    for malo in (
        "31:59",
        "0:61:00",
        "0:00:60",
        "x:00:00",
        "-1:00:00",
        "-0:00:01",
        "+0:00:01",
        "1_0:00:00",
        "0:00:01.1234",
        "0: 0:01",
        "0:0:01",
    ):
        with pytest.raises(TranscripcionError):
            parse_ms(malo)
    assert parse_ms(" 0:00:01.25 ") == 1250


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
    # Un parcial corrupto es cache invalida: se retranscribe en vez de abortar.
    (tmp_path / "parciales" / "fragmento_001.json").write_text("{corrupto", encoding="utf-8")
    transcribir_fragmentos(fragmentos, motor, tmp_path / "parciales", "h2")
    assert llamadas[-1:] == ["f1.wav"]
    fusion = fusionar(r2, 10_000).segmentos
    assert texto_entre(fusion, 4900, 5100) == fusion[1:]
    assert texto_entre(fusion, 4900, 5100, margen_ms=5000) == fusion
    assert texto_entre(fusion, 500, 800) == fusion[:1]
    # Cita de un instante en el borde exacto entre dos segmentos: toca a ambos; en 0, al primero.
    contiguos = [Segmento(0, 0, 2000, "a"), Segmento(1, 2000, 4000, "b")]
    assert texto_entre(contiguos, 2000, 2000) == contiguos
    assert texto_entre(contiguos, 0, 0) == contiguos[:1]
    assert texto_entre(contiguos, 4000, 4000) == contiguos[1:]
    assert texto_entre(contiguos, 2000, 2001) == contiguos[1:]


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
        (_entrada(r"\b\w+\b"), "comodines"),
        (_entrada(r"\b\d+\b"), "comodines"),
        (_entrada(r"\b[a-z]+\b"), "comodines"),
        (_entrada(r"\bx{2,}\b"), "comodines"),
        (_entrada(r"\b(\b"), "invalido"),
        (_entrada(r"\bx\b", "segmento"), "campos esperados"),
        (_entrada(r"\bx\b", "otro"), "alcance"),
    ],
)
def test_glosario_rechazos(entrada: str, mensaje: str) -> None:
    with pytest.raises(GlosarioError, match=mensaje):
        glosario_desde_texto(f"vocabulario: [M5]\nsustituciones:\n  - {entrada}\n")


def test_glosario_unicode_respeta_limites() -> None:
    # Con re.ASCII, `\bse\b` casaria dentro de "señal" (la ñ no seria \w); con Unicode no.
    entrada = _entrada(r"\bse\b").replace("reemplazo: y", "reemplazo: SE")
    g = glosario_desde_texto("sustituciones:\n  - " + entrada + "\n")
    corregida, registro, _ = aplicar([Segmento(0, 0, 1000, "la señal se ve")], g)
    assert corregida[0].texto == "la señal SE ve" and len(registro) == 1


def test_glosario_reemplazo_literal_y_alternancia_con_limites() -> None:
    # `\1` y `\b` en el reemplazo son texto, no plantilla de re.sub.
    entrada = _entrada(r"\bfoo\b").replace("reemplazo: y", r"reemplazo: 'x\1\b'")
    g = glosario_desde_texto("sustituciones:\n  - " + entrada + "\n")
    corregida, registro, _ = aplicar([Segmento(0, 0, 1000, "un foo aqui")], g)
    assert corregida[0].texto == "un x\\1\\b aqui" and registro[0].patron == r"\bfoo\b"
    # Una alternancia no se salta los limites de palabra.
    entrada = _entrada(r"\bfoo|bar\b").replace("reemplazo: y", "reemplazo: ZZ")
    g = glosario_desde_texto("sustituciones:\n  - " + entrada + "\n")
    corregida, _, _ = aplicar([Segmento(0, 0, 1000, "embarcar foobar foo bar")], g)
    assert corregida[0].texto == "embarcar foobar ZZ ZZ"
    with pytest.raises(GlosarioError, match="comodines"):
        glosario_desde_texto("sustituciones:\n  - " + _entrada(r"\bx\S+\b") + "\n")


def test_glosario_rechaza_punto_sin_escapar() -> None:
    """Un punto sin escapar casaria `m1` y `m5` a la vez: solo entra escapado."""
    cabecera = "vocabulario: [M5]\nsustituciones:\n"
    resto = (
        ", reemplazo: Z, alcance: global, motivo: m, ejemplo_video: v1, ejemplo_t0: '0:00:01'}\n"
    )
    with pytest.raises(GlosarioError):
        glosario_desde_texto(cabecera + "  - {patron: '\\bm.\\b'" + resto)
    g = glosario_desde_texto(cabecera + "  - {patron: '\\bm\\.5\\b'" + resto)
    assert len(g.sustituciones) == 1
