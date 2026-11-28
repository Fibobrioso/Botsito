"""El VAD de `corpus transcribe`, configurable por transcripcion (trabajo/vad-julio, D1 y D2;
ADR-0007, enmienda del 2026-11-27). Todo con el motor `falso`: la CI no tiene GPU.

Rompen a proposito con un cambio deliberado:
- (i) con la configuracion por defecto, la huella de cada manifiesto commiteado en `main` sigue
  siendo la de `main` (la lista se calculo en un clon de `main`, skill `comparar-con-main`), y la
  descripcion del VAD de esos manifiestos es la de hoy, sin claves nuevas;
- (ii) una configuracion distinta cambia la huella y queda anotada en el manifiesto;
- (iii) la CLI rechaza los valores fuera de rango con un mensaje claro;
- y el ensayo (D2) no registra nada: ni manifiesto ni carpeta activa.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.comun.documentos import sha256_hex
from botsito.corpus.glosario import glosario_desde_texto
from botsito.corpus.motor_whisper import (
    VAD_PARAMETROS,
    ConfiguracionVad,
    ConfiguracionWhisper,
    MotorWhisper,
    argumentos_vad,
    describir_vad,
)
from botsito.corpus.pipeline_transcripcion import (
    DIRECTORIO_MANIFIESTOS,
    FICHERO_ENSAYO,
    PREFIJO_ENSAYO,
    huella_de,
    transcribir_video,
)
from botsito.corpus.transcripcion import MotorFalso, SegmentoRelativo, TranscripcionError

RAIZ = Path(__file__).resolve().parents[2]
CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"

# transcripcion_id -> huella_de(corte, motor), calculadas con el codigo de `main` (139800f5) en un
# clon desechable (`git worktree add --detach`), sobre los 28 manifiestos de `main`
# (docs/validation/VAD-JULIO.md, D1). Un manifiesto que salga de aqui o cambie de huella rompe.
HUELLAS_MAIN: dict[str, str] = {
    "tr-v1-large-v3-int8-float16-00fcaf53": "2a933202",
    "tr-v1-large-v3-int8-float16-bbd8a931": "f52f6bc9",
    "tr-v10-large-v3-int8-float16-85e8af79": "f52f6bc9",
    "tr-v11-large-v3-int8-float16-d5da10be": "f52f6bc9",
    "tr-v12-large-v3-int8-float16-cb502503": "f52f6bc9",
    "tr-v13-large-v3-int8-float16-1aeb45d5": "f52f6bc9",
    "tr-v13-large-v3-int8-float16-7f5333a0": "d38e6b96",
    "tr-v14-large-v3-int8-float16-1d289df6": "d38e6b96",
    "tr-v14-large-v3-int8-float16-2253ec10": "f52f6bc9",
    "tr-v15-large-v3-int8-float16-2ec65e67": "f52f6bc9",
    "tr-v16-large-v3-int8-float16-dc91b386": "f52f6bc9",
    "tr-v17-large-v3-int8-float16-9d44007a": "f52f6bc9",
    "tr-v18-large-v3-int8-float16-ba2d4fca": "f52f6bc9",
    "tr-v19-large-v3-int8-float16-d6b9cc45": "f52f6bc9",
    "tr-v2-large-v3-int8-float16-28391c2c": "f52f6bc9",
    "tr-v2-large-v3-int8-float16-ac6b337b": "2a933202",
    "tr-v20-large-v3-int8-float16-2d93201d": "f52f6bc9",
    "tr-v21-large-v3-int8-float16-9a52aac1": "f52f6bc9",
    "tr-v3-large-v3-int8-float16-270a4851": "f52f6bc9",
    "tr-v3-large-v3-int8-float16-570a315f": "2a933202",
    "tr-v4-large-v3-int8-float16-3f8c826e": "2a933202",
    "tr-v4-large-v3-int8-float16-a8d1bccc": "f52f6bc9",
    "tr-v5-large-v3-int8-float16-01a1ae03": "2a933202",
    "tr-v5-large-v3-int8-float16-3c6fbb57": "f52f6bc9",
    "tr-v6-large-v3-int8-float16-7718b3f4": "f52f6bc9",
    "tr-v7-large-v3-int8-float16-87297562": "f52f6bc9",
    "tr-v8-large-v3-int8-float16-34b7e90f": "f52f6bc9",
    "tr-v9-large-v3-int8-float16-dcd6e5bd": "f52f6bc9",
}


# --- la descripcion del VAD, pura --------------------------------------------------------------


def test_los_nombres_son_los_de_la_faster_whisper_instalada() -> None:
    """Fijados a mano (la CI no instala el grupo `asr`); donde este instalado, se comparan con los
    campos de `VadOptions` del paquete. Si una version nueva cambia uno, este test lo dice."""
    vad = pytest.importorskip("faster_whisper.vad")
    from dataclasses import fields

    assert tuple(f.name for f in fields(vad.VadOptions)) == VAD_PARAMETROS


def test_por_defecto_la_descripcion_es_la_de_hoy() -> None:
    assert describir_vad(ConfiguracionVad()) == {"vad_filter": True}
    assert argumentos_vad(ConfiguracionVad()) == {"vad_filter": True, "vad_parameters": None}
    assert ConfiguracionVad().por_defecto
    assert ConfiguracionWhisper().vad == ConfiguracionVad()


def test_un_parametro_no_dado_no_se_anota_y_uno_dado_si() -> None:
    """Los valores por defecto no se copian al codigo: lo que no se da lo pone el paquete, y lo
    que se da se anota aunque coincida con el de defecto (cambia la huella, no el resultado)."""
    assert ConfiguracionVad.desde() == ConfiguracionVad()
    assert ConfiguracionVad.desde(threshold=None, speech_pad_ms=None) == ConfiguracionVad()
    c = ConfiguracionVad.desde(speech_pad_ms=400)
    assert describir_vad(c) == {"vad_filter": True, "vad_parameters": {"speech_pad_ms": 400}}


def test_otros_valores_quedan_anotados_y_ordenados() -> None:
    c = ConfiguracionVad.desde(speech_pad_ms=800, threshold=0.25)
    assert not c.por_defecto
    assert describir_vad(c) == {
        "vad_filter": True,
        "vad_parameters": {"speech_pad_ms": 800, "threshold": 0.25},
    }
    assert argumentos_vad(c) == {
        "vad_filter": True,
        "vad_parameters": {"speech_pad_ms": 800, "threshold": 0.25},
    }
    sin = ConfiguracionVad.desde(activo=False)
    assert describir_vad(sin) == {"vad_filter": False}
    assert argumentos_vad(sin) == {"vad_filter": False, "vad_parameters": None}


@pytest.mark.parametrize(
    ("valores", "mensaje"),
    [
        ({"threshold": 0.0}, "threshold"),
        ({"threshold": 1.0}, "threshold"),
        ({"threshold": 0.3, "neg_threshold": 0.3}, "neg_threshold"),
        ({"neg_threshold": 0.0}, "neg_threshold"),
        ({"min_speech_duration_ms": -1}, "min_speech_duration_ms"),
        ({"max_speech_duration_s": 0.0}, "max_speech_duration_s"),
        ({"min_silence_duration_ms": -5}, "min_silence_duration_ms"),
        ({"speech_pad_ms": -1}, "speech_pad_ms"),
        ({"activo": False, "threshold": 0.3}, "sin VAD"),
    ],
)
def test_fuera_de_rango_es_un_error_de_dominio(valores: dict[str, object], mensaje: str) -> None:
    with pytest.raises(TranscripcionError, match=mensaje):
        ConfiguracionVad.desde(**valores)  # type: ignore[arg-type]


def test_un_parametro_desconocido_es_un_error() -> None:
    with pytest.raises(TranscripcionError, match="desconocido"):
        ConfiguracionVad.desde(umbral=0.3)


# --- (i) lo registrado no se mueve -------------------------------------------------------------


def _manifiestos() -> dict[str, dict[str, Any]]:
    return {
        p.stem: yaml.safe_load(p.read_text(encoding="utf-8"))
        for p in sorted((RAIZ / DIRECTORIO_MANIFIESTOS).glob("tr-*.yaml"))
    }


def test_i_las_huellas_de_main_no_cambian() -> None:
    assert len(HUELLAS_MAIN) == 28
    docs = _manifiestos()
    for tid, huella in HUELLAS_MAIN.items():
        doc = docs[tid]
        assert huella_de(doc["corte"], doc["motor"]) == huella, tid


def test_i_la_descripcion_por_defecto_reproduce_la_de_cada_manifiesto_de_main() -> None:
    """La parte del VAD de la descripcion de hoy, puesta en lugar de la registrada, da la MISMA
    huella: ninguna clave nueva, ningun valor cambiado."""
    docs = _manifiestos()
    for tid, huella in HUELLAS_MAIN.items():
        motor = dict(docs[tid]["motor"])
        if motor.get("motor") != "faster-whisper":
            continue
        assert {k: motor[k] for k in motor if k.startswith("vad")} == {"vad_filter": True}, tid
        motor.pop("vad_filter")
        motor.update(describir_vad(ConfiguracionVad()))
        assert huella_de(docs[tid]["corte"], motor) == huella, tid


def test_i_el_motor_falso_por_defecto_describe_lo_de_siempre() -> None:
    assert MotorFalso().describir() == {"motor": "falso", "modelo": "falso"}


# --- el adaptador real, sin GPU: describir() y transcribir() usan la configuracion ---------------


class _ModeloQueApunta:
    """Lo minimo de `WhisperModel` para ver con que argumentos se le llama."""

    def __init__(self) -> None:
        self.llamadas: list[dict[str, object]] = []

    def transcribe(self, wav: str, **kwargs: object) -> tuple[list[object], None]:
        self.llamadas.append(kwargs)
        return [], None


def _motor_sin_gpu(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, vad: ConfiguracionVad
) -> tuple[MotorWhisper, _ModeloQueApunta]:
    motor = MotorWhisper(ConfiguracionWhisper(vad=vad))
    modelo = _ModeloQueApunta()

    def cargar() -> _ModeloQueApunta:
        motor._ruta_modelo = tmp_path  # sin model.bin: modelo_sha256 = "?"
        return modelo

    monkeypatch.setattr(motor, "_cargar", cargar)
    return motor, modelo


@pytest.mark.parametrize(
    ("vad", "descrito", "argumentos"),
    [
        (ConfiguracionVad(), {"vad_filter": True}, {"vad_filter": True, "vad_parameters": None}),
        (
            ConfiguracionVad.desde(activo=False),
            {"vad_filter": False},
            {"vad_filter": False, "vad_parameters": None},
        ),
        (
            ConfiguracionVad.desde(threshold=0.25, speech_pad_ms=800),
            {"vad_filter": True, "vad_parameters": {"speech_pad_ms": 800, "threshold": 0.25}},
            {"vad_filter": True, "vad_parameters": {"speech_pad_ms": 800, "threshold": 0.25}},
        ),
    ],
)
def test_motor_whisper_describe_y_transcribe_con_su_vad(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    vad: ConfiguracionVad,
    descrito: dict[str, object],
    argumentos: dict[str, object],
) -> None:
    motor, modelo = _motor_sin_gpu(tmp_path, monkeypatch, vad)
    d = motor.describir()
    assert {k: v for k, v in d.items() if k.startswith("vad")} == descrito
    assert motor.transcribir(tmp_path / "x.wav") == []
    (llamada,) = modelo.llamadas
    assert {k: llamada.get(k) for k in ("vad_filter", "vad_parameters")} == argumentos


# --- (ii) y D2, sobre el clip con el motor falso -----------------------------------------------

GLOSARIO = "vocabulario: [otro]\nsustituciones: []\n"


def _requiere_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        if os.environ.get("CI") or os.environ.get("BOTSITO_EXIGE_FFPROBE"):
            pytest.fail("ffmpeg no esta en PATH y en CI es obligatorio")
        pytest.skip("ffmpeg no disponible")


def _repo(tmp_path: Path) -> tuple[Path, Path, str]:
    raiz = tmp_path / "corpus"
    raiz.mkdir()
    shutil.copy(CLIP, raiz / "clip.mp4")
    sha = sha256_hex((raiz / "clip.mp4").read_bytes())
    k = tmp_path / "knowledge" / "corpus"
    k.mkdir(parents=True)
    (tmp_path / "knowledge" / "spec").mkdir()
    (k / "fuentes.yaml").write_text(
        'raiz: "corpus"\nvideos:\n  - video_id: v1\n    fichero: "clip.mp4"\n    drive_id: d1\n'
        f'    bytes: {(raiz / "clip.mp4").stat().st_size}\n    fecha_grabacion: "2026-01-01"\n'
        "    naturaleza: prueba\n",
        encoding="utf-8",
    )
    (k / "manifest.yaml").write_text(
        "version: 1\nraiz: corpus\nvideos:\n  - video_id: v1\n    fichero: clip.mp4\n"
        f"    bytes: {(raiz / 'clip.mp4').stat().st_size}\n    sha256: {sha}\n"
        "    duracion_s: 2.0\n    ancho: 1\n    alto: 1\n    audio: true\nficheros: []\n",
        encoding="utf-8",
    )
    (k / "glosario_asr.yaml").write_text(GLOSARIO, encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n'
        '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n',
        encoding="utf-8",
    )
    return tmp_path, raiz, sha


def _vad(c: ConfiguracionVad) -> dict[str, object] | None:
    return None if c.por_defecto else describir_vad(c)


def test_ii_otra_configuracion_cambia_la_huella_y_queda_anotada(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    g = glosario_desde_texto(GLOSARIO)
    datos = repo / "data"
    r0 = transcribir_video(repo, datos, raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(), g)
    assert r0.registrado
    doc0 = yaml.safe_load(r0.manifiesto.read_text(encoding="utf-8"))
    assert doc0["motor"] == {"motor": "falso", "modelo": "falso"}

    k2 = ConfiguracionVad.desde(threshold=0.25, speech_pad_ms=800)

    def otro_vad(wav: Path) -> list[SegmentoRelativo]:
        # Otro VAD deja pasar otra voz: otra cruda, y con ella otro transcripcion_id.
        return [SegmentoRelativo(0.0, 1.0, "bias bajista")]

    r2 = transcribir_video(
        repo,
        datos,
        raiz,
        "v1",
        "clip.mp4",
        sha,
        2.0,
        MotorFalso(otro_vad, vad=_vad(k2)),
        g,
        reemplaza_a=r0.transcripcion_id,
    )
    assert r2.registrado
    doc2 = yaml.safe_load(r2.manifiesto.read_text(encoding="utf-8"))
    assert doc2["motor"]["vad_parameters"] == {"speech_pad_ms": 800, "threshold": 0.25}
    assert doc2["reemplaza_a"] == r0.transcripcion_id
    h0 = huella_de(doc0["corte"], doc0["motor"])
    h2 = huella_de(doc2["corte"], doc2["motor"])
    assert h0 != h2
    # La huella distinta abre otra carpeta (la base es de la primera), con su marca.
    assert doc2["carpeta"] != doc0["carpeta"]
    assert (datos / doc2["carpeta"] / "huella.txt").read_text(encoding="utf-8").strip() == h2

    sin = ConfiguracionVad.desde(activo=False)
    assert huella_de(doc0["corte"], {**doc0["motor"], **describir_vad(sin)}) not in {h0, h2}


def test_d2_el_ensayo_no_registra_nada(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    g = glosario_desde_texto(GLOSARIO)
    datos = repo / "data"
    activa = transcribir_video(repo, datos, raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(), g)
    antes = sorted(p.name for p in (repo / DIRECTORIO_MANIFIESTOS).iterdir())
    k1 = ConfiguracionVad.desde(activo=False)
    r = transcribir_video(
        repo, datos, raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(vad=_vad(k1)), g, ensayo=True
    )
    # Ningun manifiesto nuevo, y la activa sigue siendo la misma (sin --reemplaza-a no hubo error).
    assert not r.registrado and r.manifiesto.name == FICHERO_ENSAYO
    assert sorted(p.name for p in (repo / DIRECTORIO_MANIFIESTOS).iterdir()) == antes
    # La cruda, bajo data/transcripciones/<video>/, fuera de la carpeta activa, con su descripcion.
    assert r.carpeta.parent == datos / "transcripciones" / "v1"
    assert r.carpeta.name.startswith(PREFIJO_ENSAYO)
    assert r.carpeta != activa.carpeta and r.cruda.is_file()
    desc = json.loads((r.carpeta / FICHERO_ENSAYO).read_text(encoding="utf-8"))
    assert desc["motor"]["vad_filter"] is False and desc["transcripcion_id"] == r.transcripcion_id
    assert desc["huella"] == huella_de(desc["corte"], desc["motor"])
    # Repetirlo es idempotente (misma cruda) y sigue sin registrar.
    r_bis = transcribir_video(
        repo, datos, raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(vad=_vad(k1)), g, ensayo=True
    )
    assert r_bis.cruda == r.cruda and not r_bis.registrado


def test_d2_ensayo_y_reemplaza_a_no_van_juntos(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    g = glosario_desde_texto(GLOSARIO)
    with pytest.raises(TranscripcionError, match="ensayo"):
        transcribir_video(
            repo,
            repo / "data",
            raiz,
            "v1",
            "clip.mp4",
            sha,
            2.0,
            MotorFalso(),
            g,
            reemplaza_a="tr-v1-falso-00000000",
            ensayo=True,
        )


# --- (iii) la CLI --------------------------------------------------------------------------------


def test_iii_la_cli_rechaza_lo_fuera_de_rango(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo, _raiz, _sha = _repo(tmp_path)
    base = ["--repo", str(repo), "corpus", "transcribe", "--video", "v1", "--motor", "falso"]
    casos = [
        (["--vad-threshold", "1.5"], "threshold"),
        (["--vad-threshold", "0"], "threshold"),
        (["--vad-speech-pad-ms", "-10"], "speech_pad_ms"),
        (["--vad-min-silence-duration-ms", "-1"], "min_silence_duration_ms"),
        (["--vad-min-speech-duration-ms", "-1"], "min_speech_duration_ms"),
        (["--vad-max-speech-duration-s", "0"], "max_speech_duration_s"),
        (["--vad-threshold", "0.3", "--vad-neg-threshold", "0.4"], "neg_threshold"),
        (["--sin-vad", "--vad-threshold", "0.3"], "sin VAD"),
        (["--ensayo", "--reemplaza-a", "tr-v1-falso-00000000"], "ensayo"),
    ]
    for extra, mensaje in casos:
        capsys.readouterr()
        assert cli.main(base + extra) == 1, extra
        salida = capsys.readouterr().out
        assert salida.startswith("ERROR:") and mensaje in salida, (extra, salida)
    # Nada llego a escribirse: ni manifiestos ni datos.
    assert not (repo / DIRECTORIO_MANIFIESTOS).exists() or not any(
        (repo / DIRECTORIO_MANIFIESTOS).glob("tr-*.yaml")
    )
    assert not (repo / "data").exists()


def test_iii_la_cli_anota_la_configuracion_en_un_ensayo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _requiere_ffmpeg()
    repo, _raiz, _sha = _repo(tmp_path)
    base = ["--repo", str(repo), "corpus", "transcribe", "--video", "v1", "--motor", "falso"]
    assert (
        cli.main(base + ["--ensayo", "--vad-threshold", "0.25", "--vad-speech-pad-ms", "800"]) == 0
    )
    salida = capsys.readouterr().out
    assert "ENSAYO:" in salida and "sin manifiesto" in salida
    assert not any((repo / DIRECTORIO_MANIFIESTOS).glob("tr-*.yaml"))
    (carpeta,) = (repo / "data" / "transcripciones" / "v1").glob(PREFIJO_ENSAYO + "*")
    desc = json.loads((carpeta / FICHERO_ENSAYO).read_text(encoding="utf-8"))
    assert desc["motor"]["vad_parameters"] == {"speech_pad_ms": 800, "threshold": 0.25}
