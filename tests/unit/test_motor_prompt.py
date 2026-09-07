"""Huella de reanudacion sin GPU/driver y guardia del tamano del `initial_prompt` (previos de F07,
2026-09-06). `motor_whisper` se importa sin cargar faster-whisper (import perezoso)."""

from pathlib import Path

import pytest

from botsito.corpus.glosario import cargar_glosario
from botsito.corpus.motor_whisper import (
    LIMITE_PROMPT_TOKENS,
    ConfiguracionWhisper,
    comprobar_prompt,
)
from botsito.corpus.pipeline_transcripcion import (
    CLAVES_FUERA_DE_HUELLA,
    _carpeta_base_registrada_ajena,
    huella_de,
)
from botsito.corpus.transcripcion import TranscripcionError

REPO = Path(__file__).resolve().parents[2]
CORTE = {"objetivo_s": 600.0, "min_s": 420.0, "max_s": 780.0}
MOTOR = {
    "motor": "faster-whisper",
    "modelo": "large-v3",
    "ctranslate2": "4.8.2",
    "gpu": "GTX 1650, 610.62",
}


def test_huella_ignora_gpu_y_driver() -> None:
    assert "gpu" in CLAVES_FUERA_DE_HUELLA
    otra_gpu = dict(MOTOR, gpu="RTX 4090, 999.99")
    assert huella_de(CORTE, MOTOR) == huella_de(CORTE, otra_gpu)


def test_huella_cambia_con_lo_que_si_afecta_a_la_salida() -> None:
    assert huella_de(CORTE, MOTOR) != huella_de(CORTE, dict(MOTOR, ctranslate2="4.9.0"))
    assert huella_de(CORTE, MOTOR) != huella_de(CORTE, dict(MOTOR, nvidia_cudnn_cu12="9.26"))
    assert huella_de(CORTE, MOTOR) != huella_de(CORTE, dict(MOTOR, modelo_sha256="otro"))
    assert huella_de(CORTE, MOTOR) != huella_de(CORTE, dict(MOTOR, initial_prompt_sha256="x"))
    assert huella_de(CORTE, MOTOR) != huella_de(dict(CORTE, max_s=600.0), MOTOR)


def test_huella_ignora_el_recuento_de_tokens_del_prompt() -> None:
    assert "initial_prompt_tokens" in CLAVES_FUERA_DE_HUELLA
    assert huella_de(CORTE, dict(MOTOR, initial_prompt_tokens=99)) == huella_de(
        CORTE, dict(MOTOR, initial_prompt_tokens=96)
    )


VIDEO = "a" * 64


def _registrado(**cambios: object) -> dict[str, object]:
    doc: dict[str, object] = {
        "carpeta": "transcripciones/v1/large-v3-int8-float16",
        "corte": dict(CORTE),
        "motor": dict(MOTOR),
        "sha256_video": VIDEO,
    }
    doc.update(cambios)
    return doc


def test_carpeta_base_registrada_con_otra_gpu_no_es_ajena() -> None:
    huella = huella_de(CORTE, MOTOR)
    doc = _registrado(motor=dict(MOTOR, gpu="RTX 4090, 999.99"))
    assert not _carpeta_base_registrada_ajena([doc], "v1", "large-v3-int8-float16", huella, VIDEO)


@pytest.mark.parametrize(
    "cambio",
    [
        {"motor": dict(MOTOR, ctranslate2="4.9.0")},
        {"motor": dict(MOTOR, modelo_sha256="otro")},
        {"motor": dict(MOTOR, initial_prompt_sha256="otro")},
        {"corte": dict(CORTE, max_s=600.0)},
        {"sha256_video": "b" * 64},
    ],
)
def test_carpeta_base_registrada_con_otra_huella_o_video_es_ajena(
    cambio: dict[str, object],
) -> None:
    huella = huella_de(CORTE, MOTOR)
    doc = _registrado(**cambio)
    assert _carpeta_base_registrada_ajena([doc], "v1", "large-v3-int8-float16", huella, VIDEO)


def test_carpeta_base_registrada_sin_corte_es_ajena_y_otra_carpeta_no_cuenta() -> None:
    huella = huella_de(CORTE, MOTOR)
    roto = _registrado()
    del roto["corte"]
    assert _carpeta_base_registrada_ajena([roto], "v1", "large-v3-int8-float16", huella, VIDEO)
    otra = _registrado(carpeta="transcripciones/v1/large-v3-int8-float16-12345678")
    assert not _carpeta_base_registrada_ajena([otra], "v1", "large-v3-int8-float16", huella, VIDEO)


class _Tokenizador:
    """Un token por caracter; con `add_special_tokens` (el valor por defecto de `tokenizers`)
    anade 3 tokens especiales, como el tokenizer.json de large-v3. faster-whisper codifica el
    prompt SIN especiales: la guardia debe contar como el motor."""

    class _Codificado:
        def __init__(self, ids: list[int]) -> None:
            self.ids = ids

    def encode(self, texto: str, add_special_tokens: bool = True) -> "_Tokenizador._Codificado":
        extra = 3 if add_special_tokens else 0
        return self._Codificado(list(range(len(texto) + extra)))


def test_prompt_vacio_no_cuenta_tokens() -> None:
    assert comprobar_prompt(_Tokenizador(), "") == 0


def test_prompt_dentro_del_limite_devuelve_su_tamano() -> None:
    # faster-whisper codifica " " + texto.strip(): el espacio inicial cuenta.
    assert comprobar_prompt(_Tokenizador(), "M15, BOS") == len(" M15, BOS")


def test_prompt_en_el_limite_exacto_cabe() -> None:
    # previous_tokens[-(448 // 2 - 1):] conserva 223 tokens enteros: 223 cabe, 224 no.
    justo = "x" * (LIMITE_PROMPT_TOKENS - 1)  # + el espacio inicial = LIMITE
    assert comprobar_prompt(_Tokenizador(), justo) == LIMITE_PROMPT_TOKENS


def test_prompt_que_el_motor_truncaria_es_error_de_dominio() -> None:
    largo = "x" * LIMITE_PROMPT_TOKENS  # + el espacio inicial = LIMITE + 1
    with pytest.raises(TranscripcionError, match="trunca el prompt"):
        comprobar_prompt(_Tokenizador(), largo)


def test_prompt_con_el_tokenizador_real_si_el_modelo_esta_en_cache() -> None:
    tokenizers = pytest.importorskip("tokenizers")
    cache = (
        Path.home() / ".cache" / "huggingface" / "hub" / "models--Systran--faster-whisper-large-v3"
    )
    ficheros = list(cache.glob("snapshots/*/tokenizer.json"))
    if not ficheros:
        pytest.skip("large-v3 no esta en la cache local")
    tokenizador = tokenizers.Tokenizer.from_file(str(ficheros[0]))
    glosario = cargar_glosario(REPO / "knowledge" / "corpus" / "glosario_asr.yaml")
    n = comprobar_prompt(tokenizador, glosario.prompt_inicial)
    assert 0 < n <= LIMITE_PROMPT_TOKENS
    # Sin `add_special_tokens=False` el recuento incluiria los 3 tokens especiales.
    assert n + 3 == len(tokenizador.encode(" " + glosario.prompt_inicial).ids)


def test_configuracion_lleva_prompt_inicial_no_hotwords() -> None:
    c = ConfiguracionWhisper(prompt_inicial="M15, BOS")
    assert c.prompt_inicial == "M15, BOS"
    assert not hasattr(c, "hotwords")
