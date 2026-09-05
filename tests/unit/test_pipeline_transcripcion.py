"""Pipeline completo con motor falso sobre el clip fixture, manifiestos inmutables, CLI (F04)."""

import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.comun.documentos import sha256_hex
from botsito.corpus.glosario import glosario_desde_texto
from botsito.corpus.manifiestos_transcripcion import (
    ManifiestoTranscripcionError,
    activa_de,
    cargar_manifiesto,
    cargar_todos,
    comprobar,
    validar,
)
from botsito.corpus.pipeline_transcripcion import (
    DIRECTORIO_MANIFIESTOS,
    cargar_corregida,
    cargar_cruda,
    transcribir_video,
)
from botsito.corpus.transcripcion import MotorFalso, SegmentoRelativo

CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"


class MotorVacio(MotorFalso):
    @property
    def nombre(self) -> str:
        return "vacio"

    def describir(self) -> dict[str, object]:
        return {"motor": "vacio", "modelo": "vacio"}

    def transcribir(self, wav: Path) -> list[SegmentoRelativo]:
        return []


def _sust(patron: str, reemplazo: str) -> str:
    return (
        f"  - {{patron: '{patron}', reemplazo: {reemplazo}, alcance: global, motivo: m, "
        "ejemplo_video: v1, ejemplo_t0: '0:00:01'}\n"
    )


GLOSARIO = "vocabulario: [otro]\nsustituciones:\n" + _sust(r"\bfalso\b", "FALSO")


def _requiere_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        pytest.skip("ffmpeg no disponible")


def _repo(tmp_path: Path) -> tuple[Path, Path, str]:
    """Repo minimo con un corpus de un video (el clip) inventariado."""
    raiz = tmp_path / "corpus"
    raiz.mkdir()
    shutil.copy(CLIP, raiz / "clip.mp4")
    sha = sha256_hex((raiz / "clip.mp4").read_bytes())
    (tmp_path / "knowledge" / "corpus").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec").mkdir()
    (tmp_path / "knowledge" / "corpus" / "fuentes.yaml").write_text(
        'raiz: "corpus"\nvideos:\n  - video_id: v1\n    fichero: "clip.mp4"\n    drive_id: d1\n'
        f'    bytes: {(raiz / "clip.mp4").stat().st_size}\n    fecha_grabacion: "2026-01-01"\n'
        "    naturaleza: prueba\n",
        encoding="utf-8",
    )
    (tmp_path / "knowledge" / "corpus" / "manifest.yaml").write_text(
        "version: 1\nraiz: corpus\nvideos:\n  - video_id: v1\n    fichero: clip.mp4\n"
        f"    bytes: {(raiz / 'clip.mp4').stat().st_size}\n    sha256: {sha}\n"
        "    duracion_s: 2.0\n    ancho: 1\n    alto: 1\n    audio: true\nficheros: []\n",
        encoding="utf-8",
    )
    (tmp_path / "knowledge" / "corpus" / "glosario_asr.yaml").write_text(GLOSARIO, encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n'
        '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n',
        encoding="utf-8",
    )
    return tmp_path, raiz, sha


def test_pipeline_con_motor_falso_es_determinista_e_inmutable(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    g = glosario_desde_texto(GLOSARIO)
    r = transcribir_video(repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(), g)
    assert r.transcripcion_id.startswith("tr-v1-falso-") and r.manifiesto.exists()
    doc = yaml.safe_load(r.manifiesto.read_text(encoding="utf-8"))
    assert doc["segmentos"] == 1 and doc["carpeta"] == "transcripciones/v1/falso"
    assert doc["fragmentos"] == [{"indice": 0, "inicio_m": 0, "fin_m": doc["muestras"]}]
    cruda = cargar_cruda(r.carpeta)
    assert cruda[0].t0_ms == 0 and cruda[0].t1_ms == doc["muestras"] * 1000 // 16000
    assert cargar_corregida(r.carpeta)[0].texto.startswith("texto FALSO")
    assert (
        (r.carpeta / "cruda.txt")
        .read_text(encoding="utf-8")
        .startswith("[0:00:00.000] texto falso")
    )
    # Segunda ejecucion: mismo id, no reescribe el manifiesto, reutiliza parciales.
    r2 = transcribir_video(repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(), g)
    assert r2.transcripcion_id == r.transcripcion_id
    # Manifiesto valido y coherente con el disco y el glosario.
    items = cargar_todos(repo)
    assert [t.id for t in items] == [r.transcripcion_id]
    assert comprobar(items, repo / "data", g) == ([], [])
    assert activa_de(items, "v1").id == r.transcripcion_id
    # Un motor sin segmentos no registra nada.
    otro = MotorVacio()
    with pytest.raises(Exception, match="ningun segmento"):
        transcribir_video(repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, otro, g)
    # Video con hash distinto del manifiesto del corpus: rechazado.
    with pytest.raises(Exception, match="sha256"):
        transcribir_video(
            repo, repo / "data", raiz, "v1", "clip.mp4", "0" * 64, 2.0, MotorFalso(), g
        )


def test_comprobar_detecta_cruda_alterada_y_corregida_desfasada(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    g = glosario_desde_texto(GLOSARIO)
    r = transcribir_video(repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(), g)
    items = cargar_todos(repo)
    corregida = r.carpeta / "corregida.jsonl"
    corregida.write_text(
        corregida.read_text(encoding="utf-8").replace("FALSO", "editado"), encoding="utf-8"
    )
    errores, _ = comprobar(items, repo / "data", g)
    assert len(errores) == 1 and "no es cruda + glosario" in errores[0]
    g2 = glosario_desde_texto(GLOSARIO + _sust(r"\btexto\b", "TEXTO"))
    assert len(comprobar(items, repo / "data", g2)[0]) == 2  # corregida y correcciones desfasadas
    r.cruda.write_text("x", encoding="utf-8")
    errores, _ = comprobar(items, repo / "data", g)
    assert errores == [
        f"{r.transcripcion_id}: cruda.jsonl alterada (sha256 distinto del manifiesto)"
    ]
    shutil.rmtree(r.carpeta)
    assert comprobar(items, repo / "data", g)[0] == [] and comprobar(items, repo / "data", g)[1]


def test_manifiesto_corrupto_rechazado(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    r = transcribir_video(
        repo,
        repo / "data",
        raiz,
        "v1",
        "clip.mp4",
        sha,
        2.0,
        MotorFalso(),
        glosario_desde_texto(GLOSARIO),
    )
    doc: dict[str, Any] = yaml.safe_load(r.manifiesto.read_text(encoding="utf-8"))
    casos: list[tuple[dict[str, Any], str]] = [
        ({"transcripcion_id": "tr-v1-falso-00000000"}, "sufijo"),
        ({"carpeta": "transcripciones/v2/falso"}, "carpeta"),
        ({"carpeta": "../x/transcripciones/v1/falso"}, "carpeta"),
        ({"transcripcion_id": "tr-v2-falso-" + doc["sha256_cruda"][:8]}, "empieza por"),
        ({"segmentos": 0}, "sin segmentos"),
        ({"extra": 1}, "desconocidos"),
        ({"reemplaza_a": "x"}, "reemplaza_a"),
        ({"motor": {}}, "motor.modelo"),
    ]
    for cambio, mensaje in casos:
        with pytest.raises(ManifiestoTranscripcionError, match=mensaje):
            validar({**doc, **cambio}, "manifiesto")
    (repo / DIRECTORIO_MANIFIESTOS / "otro.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")
    with pytest.raises(ManifiestoTranscripcionError, match="debe llamarse"):
        cargar_manifiesto(repo / DIRECTORIO_MANIFIESTOS / "otro.yaml")


def test_cli_transcribe_glossary_check_show(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _requiere_ffmpeg()
    repo, _raiz, _sha = _repo(tmp_path)
    base = ["--repo", str(repo), "corpus"]
    assert cli.main(base + ["transcribe", "--video", "v1", "--motor", "falso"]) == 0
    assert "OK: tr-v1-falso-" in capsys.readouterr().out
    assert cli.main(base + ["transcript", "check"]) == 0
    assert cli.main(base + ["glossary", "apply", "--video", "v1"]) == 0
    capsys.readouterr()
    assert (
        cli.main(
            base
            + [
                "transcript",
                "show",
                "--video",
                "v1",
                "--t0",
                "0:00:00",
                "--t1",
                "0:00:01",
                "--capa",
                "corregida",
            ]
        )
        == 0
    )
    salida = capsys.readouterr().out
    assert "[0:00:00.000] texto FALSO" in salida and "capa corregida" in salida
    assert (
        cli.main(
            base + ["transcript", "show", "--video", "v9", "--t0", "0:00:00", "--t1", "0:00:01"]
        )
        == 1
    )
    assert (
        cli.main(
            base + ["transcript", "show", "--video", "v1", "--t0", "0:00:05", "--t1", "0:00:01"]
        )
        == 1
    )
    # Un instante (t0 == t1) es una cita valida; --transcripcion de otro video se rechaza.
    assert (
        cli.main(
            base + ["transcript", "show", "--video", "v1", "--t0", "0:00:01", "--t1", "0:00:01"]
        )
        == 0
    )
    tid = next((repo / DIRECTORIO_MANIFIESTOS).glob("tr-*.yaml")).stem
    assert (
        cli.main(
            base
            + ["transcript", "show", "--video", "v2", "--t0", "0:00:01", "--t1", "0:00:01"]
            + ["--transcripcion", tid]
        )
        == 1
    )
    assert cli.main(base + ["transcribe", "--video", "v9", "--motor", "falso"]) == 1
    # knowledge validate incluye la capa de transcripciones (sin git: guardias no evaluadas).
    (repo / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros: []\n", encoding="utf-8"
    )
    (repo / "knowledge" / "evidence").mkdir()
    (repo / "knowledge" / "feedback").mkdir()
    (repo / "docs" / "adr").mkdir(parents=True)
    capsys.readouterr()
    assert cli.main(["--repo", str(repo), "evidence", "contradictions"]) == 0
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0
    assert "1 transcripciones registradas" in capsys.readouterr().out
