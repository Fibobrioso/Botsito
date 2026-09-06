"""Huella de reanudacion sin GPU/driver y guardia del tamano del `initial_prompt` (previos de F07,
2026-09-06). `motor_whisper` se importa sin cargar faster-whisper (import perezoso)."""

import pytest

from botsito.corpus.motor_whisper import (
    LIMITE_PROMPT_TOKENS,
    ConfiguracionWhisper,
    comprobar_prompt,
)
from botsito.corpus.pipeline_transcripcion import CLAVES_FUERA_DE_HUELLA, huella_de
from botsito.corpus.transcripcion import TranscripcionError

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
    assert huella_de(CORTE, MOTOR) != huella_de(CORTE, dict(MOTOR, initial_prompt_sha256="x"))
    assert huella_de(CORTE, MOTOR) != huella_de(dict(CORTE, max_s=600.0), MOTOR)


class _Tokenizador:
    """Un token por caracter: basta para probar la guardia."""

    class _Codificado:
        def __init__(self, ids: list[int]) -> None:
            self.ids = ids

    def encode(self, texto: str) -> "_Tokenizador._Codificado":
        return self._Codificado(list(range(len(texto))))


def test_prompt_vacio_no_cuenta_tokens() -> None:
    assert comprobar_prompt(_Tokenizador(), "") == 0


def test_prompt_dentro_del_limite_devuelve_su_tamano() -> None:
    # faster-whisper codifica " " + texto.strip(): el espacio inicial cuenta.
    assert comprobar_prompt(_Tokenizador(), "M15, BOS") == len(" M15, BOS")


def test_prompt_que_el_motor_truncaria_es_error_de_dominio() -> None:
    largo = "x" * LIMITE_PROMPT_TOKENS  # + el espacio inicial = LIMITE + 1
    with pytest.raises(TranscripcionError, match="trunca el prompt"):
        comprobar_prompt(_Tokenizador(), largo)


def test_configuracion_lleva_prompt_inicial_no_hotwords() -> None:
    c = ConfiguracionWhisper(prompt_inicial="M15, BOS")
    assert c.prompt_inicial == "M15, BOS"
    assert not hasattr(c, "hotwords")
