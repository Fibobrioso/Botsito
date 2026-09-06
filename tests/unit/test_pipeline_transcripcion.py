"""Pipeline completo con motor falso sobre el clip fixture, manifiestos inmutables, CLI (F04)."""

import os
import shutil
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.comun.documentos import sha256_hex
from botsito.corpus.audio import AudioError
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
from botsito.corpus.transcripcion import MotorFalso, SegmentoRelativo, TranscripcionError

CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"


class MotorNombreMalo(MotorFalso):
    @property
    def nombre(self) -> str:
        return "Systran/Falso"


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
        if os.environ.get("CI") or os.environ.get("BOTSITO_EXIGE_FFPROBE"):
            pytest.fail("ffmpeg no esta en PATH y en CI es obligatorio")
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
    # Segunda ejecucion: mismo id, no reescribe el manifiesto, no llama al motor (parciales).
    bytes_manifiesto = r.manifiesto.read_bytes()
    llamadas: list[str] = []

    def espia(wav: Path) -> list[SegmentoRelativo]:
        llamadas.append(wav.name)
        return MotorFalso().transcribir(wav)

    r2 = transcribir_video(
        repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, MotorFalso(espia), g
    )
    assert r2.transcripcion_id == r.transcripcion_id and llamadas == []
    assert r.manifiesto.read_bytes() == bytes_manifiesto
    assert (r.carpeta / "huella.txt").is_file()
    assert (r.carpeta / "video.sha256").read_text(encoding="utf-8").strip() == sha
    assert (r.carpeta.parent / "audio.sha256_video").is_file()
    # Un temporal huerfano del manifiesto (corte a mitad de escritura) no invalida el repo.
    huerfano = r.manifiesto.with_name("_" + r.manifiesto.name + ".tmp")
    huerfano.write_text("a medias", encoding="utf-8")
    assert [t.id for t in cargar_todos(repo)] == [r.transcripcion_id]
    huerfano.unlink()
    # Si el video del corpus cambia (otro sha), la cruda anterior no se pisa: otra carpeta,
    # decidida antes de llamar al motor (la carpeta `<nombre>` sigue siendo del video viejo).
    otro_sha = "f" * 64
    # Un video distinto da otra cruda (aqui se fuerza con un motor que dice otra cosa).
    motor_otro = MotorFalso(lambda wav: [SegmentoRelativo(0.0, 1.0, "otra cruda")])
    # Otra carpeta = otra transcripcion: exige reemplazar a la activa (auditoria 2026-09-05).
    with pytest.raises(TranscripcionError, match="indica --reemplaza-a"):
        transcribir_video(
            repo,
            repo / "data",
            raiz,
            "v1",
            "clip.mp4",
            otro_sha,
            2.0,
            motor_otro,
            g,
            comprobar_hash_video=False,
        )
    r3 = transcribir_video(
        repo,
        repo / "data",
        raiz,
        "v1",
        "clip.mp4",
        otro_sha,
        2.0,
        motor_otro,
        g,
        comprobar_hash_video=False,
        reemplaza_a=r.transcripcion_id,
    )
    assert r3.carpeta != r.carpeta and r3.carpeta.name.startswith("falso-")
    assert (r3.carpeta / "video.sha256").read_text(encoding="utf-8").strip() == otro_sha
    assert (r.carpeta / "video.sha256").read_text(encoding="utf-8").strip() == sha
    assert cargar_cruda(r.carpeta) == cruda  # la cruda vieja sigue intacta
    # Reemplazar a un id que no es la activa: error antes del motor.
    with pytest.raises(TranscripcionError, match="la transcripcion activa de v1 es"):
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
        )
    # El mismo manifiesto (misma cruda, mismo id) con otro reemplaza_a no se reescribe.
    with pytest.raises(TranscripcionError, match="inmutable"):
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
            reemplaza_a=r3.transcripcion_id,
        )
    # En un clon sin data/ (sin marcas), el manifiesto de `r` sigue diciendo de que video salio
    # la carpeta base `falso`: con otro video no se pisa aunque no haya marcas.
    shutil.rmtree(repo / "data")
    r4 = transcribir_video(
        repo,
        repo / "data",
        raiz,
        "v1",
        "clip.mp4",
        otro_sha,
        2.0,
        motor_otro,
        g,
        comprobar_hash_video=False,
    )
    assert r4.carpeta.name.startswith("falso-") and r4.transcripcion_id == r3.transcripcion_id
    # Un motor cuyo nombre no cabe en un id se rechaza antes de trabajar.
    with pytest.raises(TranscripcionError, match="nombre de motor"):
        transcribir_video(
            repo, repo / "data", raiz, "v1", "clip.mp4", sha, 2.0, MotorNombreMalo(), g
        )
    # Manifiesto valido y coherente con el disco y el glosario.
    items = cargar_todos(repo)
    assert sorted(t.id for t in items) == sorted([r.transcripcion_id, r3.transcripcion_id])
    errores, avisos = comprobar(items, repo / "data", g)
    assert errores == [] and len(avisos) == 1 and r.transcripcion_id in avisos[0]
    assert activa_de(items, "v1").id == r3.transcripcion_id
    # Un motor sin segmentos no registra nada.
    otro = MotorVacio()
    with pytest.raises(TranscripcionError, match="ningun segmento"):
        transcribir_video(
            repo,
            repo / "data",
            raiz,
            "v1",
            "clip.mp4",
            sha,
            2.0,
            otro,
            g,
            reemplaza_a=r3.transcripcion_id,
        )
    # Video con hash distinto del manifiesto del corpus: rechazado.
    with pytest.raises(AudioError, match="sha256"):
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
        ({"fragmentos": ["x"]}, "fragmentos"),
        ({"fragmentos": [{"indice": 0, "inicio_m": 0, "fin_m": 5}]}, "no cubren"),
        ({"duracion_wav_s": "abc"}, "duracion_wav_s"),
        ({"duracion_wav_s": 999.0}, "no coincide con muestras"),
        ({"senales": {}}, "senales"),
        ({"huecos": [{"desde_ms": 5, "hasta_ms": 1, "ms": -4}]}, "hueco invalido"),
        ({"cortes_forzados_m": [7]}, "cortes_forzados_m"),
        ({"carpeta": "transcripciones/v1/falso-zz"}, "carpeta"),
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
    (repo / DIRECTORIO_MANIFIESTOS / "otro.yaml").unlink()
    # Con sufijo -<huella8> la carpeta es valida; reemplaza_a a otro video se rechaza.
    validar({**doc, "carpeta": "transcripciones/v1/falso-0123abcd"}, "manifiesto")
    tid2 = "tr-v2-falso-" + doc["sha256_cruda"][:8]
    doc2 = {
        **doc,
        "video_id": "v2",
        "transcripcion_id": tid2,
        "carpeta": "transcripciones/v2/falso",
    }
    doc2["reemplaza_a"] = doc["transcripcion_id"]
    (repo / DIRECTORIO_MANIFIESTOS / f"{tid2}.yaml").write_text(
        yaml.safe_dump(doc2), encoding="utf-8"
    )
    with pytest.raises(ManifiestoTranscripcionError, match="otro video"):
        cargar_todos(repo)


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
    # Parametros de corte invalidos y --reemplaza-a inexistente: error limpio, sin traceback.
    assert (
        cli.main(base + ["transcribe", "--video", "v1", "--motor", "falso", "--min-s", "700"]) == 1
    )
    assert (
        cli.main(
            base
            + [
                "transcribe",
                "--video",
                "v1",
                "--motor",
                "falso",
                "--reemplaza-a",
                "tr-v1-x-00000000",
            ]
        )
        == 1
    )
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
