"""Extraccion real con ffmpeg sobre el clip fixture (10 fps, 2 s): pts exactos, obligatorio en
segundo entero = regular, determinismo, idempotencia, inmutabilidad, huecos de la fuente, CLI y
`knowledge validate` (F05, ADR-0008)."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from botsito import cli
from botsito.comun.documentos import sha256_hex
from botsito.corpus.fotogramas import (
    FICHERO_INDICE,
    FotogramasError,
    cargar_indice,
    extraer_instante,
    extraer_regulares,
    extraer_video,
)
from botsito.corpus.manifiestos_fotogramas import cargar_todos, comprobar

CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"
NOMBRE_ACENTUADO = "Grabación de pantalla ñ.mp4"


def _requiere_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        if os.environ.get("CI") or os.environ.get("BOTSITO_EXIGE_FFPROBE"):
            pytest.fail("ffmpeg no esta en PATH y en CI es obligatorio")
        pytest.skip("ffmpeg no disponible")


def _repo(tmp_path: Path, obligatorios: str = "") -> tuple[Path, Path, str]:
    """Repo minimo con un corpus de un video (el clip, con nombre acentuado) inventariado."""
    raiz = tmp_path / "corpus"
    raiz.mkdir()
    video = raiz / NOMBRE_ACENTUADO
    shutil.copy(CLIP, video)
    sha = sha256_hex(video.read_bytes())
    (tmp_path / "knowledge" / "corpus").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec").mkdir()
    (tmp_path / "knowledge" / "corpus" / "fuentes.yaml").write_text(
        f'raiz: "corpus"\nvideos:\n  - video_id: v1\n    fichero: "{NOMBRE_ACENTUADO}"\n'
        f"    drive_id: d1\n    bytes: {video.stat().st_size}\n"
        '    fecha_grabacion: "2026-01-01"\n    naturaleza: prueba\n',
        encoding="utf-8",
    )
    (tmp_path / "knowledge" / "corpus" / "manifest.yaml").write_text(
        f'version: 1\nraiz: corpus\nvideos:\n  - video_id: v1\n    fichero: "{NOMBRE_ACENTUADO}"\n'
        f"    bytes: {video.stat().st_size}\n    sha256: {sha}\n"
        "    duracion_s: 2.0\n    ancho: 320\n    alto: 180\n    audio: true\nficheros: []\n",
        encoding="utf-8",
    )
    (tmp_path / "knowledge" / "corpus" / "glosario_asr.yaml").write_text(
        "vocabulario: [otro]\nsustituciones: []\n", encoding="utf-8"
    )
    if obligatorios:
        (tmp_path / "knowledge" / "corpus" / "fotogramas_obligatorios.yaml").write_text(
            obligatorios, encoding="utf-8"
        )
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n'
        '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n',
        encoding="utf-8",
    )
    return tmp_path, raiz, sha


def test_regla_de_seleccion_pts_exactos_y_bitexact(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    _, raiz, _ = _repo(tmp_path)
    video = raiz / NOMBRE_ACENTUADO
    fs, resolucion = extraer_regulares(video, tmp_path / "fr")
    assert resolucion == (320, 180)
    assert [(f.t_ms, f.pts_ms, f.origen) for f in fs] == [
        (0, 0, "regular"),
        (1000, 1000, "regular"),
    ]
    assert sorted(p.name for p in (tmp_path / "fr").glob("*.png")) == [
        "000000000.png",
        "000001000.png",
    ]
    pts, datos = extraer_instante(video, 1250, tmp_path / "fr")
    assert pts == 1300 and b"Lavc" not in datos
    pts1, datos1 = extraer_instante(video, 1000, tmp_path / "fr")
    assert pts1 == 1000 and datos1 == (tmp_path / "fr" / fs[1].fichero).read_bytes()
    assert b"Lavc" not in (tmp_path / "fr" / fs[0].fichero).read_bytes()
    with pytest.raises(FotogramasError, match="fin del video"):
        extraer_instante(video, 5000, tmp_path / "fr")
    with pytest.raises(FotogramasError, match="no existe"):
        extraer_regulares(tmp_path / "nada.mp4", tmp_path / "fr")


def test_ffmpeg_ausente_es_error_explicito(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PATH", str(tmp_path))
    monkeypatch.setattr(shutil, "which", lambda *_: None)
    shutil.copy(CLIP, tmp_path / "c.mp4")
    with pytest.raises(FotogramasError, match="ffmpeg"):
        extraer_regulares(tmp_path / "c.mp4", tmp_path / "fr")


OBLIGATORIOS = (
    "fotogramas:\n"
    "  - {video_id: v1, t: '0:00:01', motivo: entero}\n"
    "  - {video_id: v1, t: '0:00:01.250', motivo: fraccion}\n"
)


def test_extraccion_completa_determinista_idempotente_e_inmutable(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path, OBLIGATORIOS)
    datos = repo / "data"
    r = extraer_video(repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0, [1000, 1250])
    assert r.fotogramas_id.startswith("fr-v1-") and r.manifiesto.exists()
    assert [(f.t_ms, f.pts_ms, f.origen) for f in r.fotogramas] == [
        (0, 0, "regular"),
        (1000, 1000, "regular"),
        (1250, 1300, "obligatorio"),
    ]
    doc = yaml.safe_load(r.manifiesto.read_text(encoding="utf-8"))
    assert doc["carpeta"] == "fotogramas/v1/png-1fps" and doc["huecos"] == []
    assert doc["n_fotogramas"] == 3 and doc["n_regulares"] == 2 and doc["ultimo_pts_ms"] == 1300
    assert doc["extra"] == [{"t_ms": 1250, "pts_ms": 1300, "sha256": r.fotogramas[2].sha256}]
    assert doc["resolucion"] == {"ancho": 320, "alto": 180}
    assert doc["sha256_index"] == sha256_hex(r.indice.read_bytes())
    assert (r.carpeta / "video.sha256").read_text(encoding="utf-8").strip() == sha
    # Determinismo: dos extracciones dan los mismos bytes.
    hashes = {f.t_ms: f.sha256 for f in r.fotogramas}
    otra = tmp_path / "otra"
    fs2, _ = extraer_regulares(raiz / NOMBRE_ACENTUADO, otra)
    assert {f.t_ms: f.sha256 for f in fs2} == {k: v for k, v in hashes.items() if k % 1000 == 0}
    # Idempotente: segunda ejecucion no decodifica (mtime intacto) ni reescribe el manifiesto.
    mtimes = {p.name: p.stat().st_mtime_ns for p in r.carpeta.glob("*.png")}
    bytes_manifiesto = r.manifiesto.read_bytes()
    mensajes: list[str] = []
    r2 = extraer_video(
        repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0, [1000, 1250], progreso=mensajes.append
    )
    assert r2.fotogramas_id == r.fotogramas_id
    assert {p.name: p.stat().st_mtime_ns for p in r.carpeta.glob("*.png")} == mtimes
    assert r.manifiesto.read_bytes() == bytes_manifiesto and "no se decodifica" in mensajes[0]
    # Un obligatorio nuevo con fraccion es otra carpeta y otro manifiesto: exige reemplaza_a.
    args = (repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0)
    with pytest.raises(FotogramasError, match="indica --reemplaza-a"):
        extraer_video(*args, [1250, 1500])
    with pytest.raises(FotogramasError, match="no hay nada que reemplazar"):
        extraer_video(*args, [1250], reemplaza_a=r.fotogramas_id)
    with pytest.raises(FotogramasError, match="la extraccion activa"):
        extraer_video(*args, [1500], reemplaza_a="fr-v1-00000000")
    r3 = extraer_video(*args, [1250, 1500], reemplaza_a=r.fotogramas_id)
    assert r3.fotogramas_id != r.fotogramas_id and r3.carpeta != r.carpeta
    assert r3.carpeta.name.startswith("png-1fps-") and (r.carpeta / FICHERO_INDICE).is_file()
    assert [f.t_ms for f in r3.fotogramas] == [0, 1000, 1250, 1500]
    doc3 = yaml.safe_load(r3.manifiesto.read_text(encoding="utf-8"))
    assert doc3["reemplaza_a"] == r.fotogramas_id
    # Manifiesto que registra la carpeta con OTRO indice (otra build de ffmpeg): inmutabilidad.
    texto = r3.manifiesto.read_text(encoding="utf-8")
    r3.manifiesto.write_text(texto.replace(doc3["sha256_index"], "0" * 64), encoding="utf-8")
    (r3.carpeta / FICHERO_INDICE).unlink()
    with pytest.raises(FotogramasError, match="inmutables"):
        extraer_video(*args, [1250, 1500])


def test_otra_build_exige_reemplaza_a_y_abre_otra_carpeta(tmp_path: Path) -> None:
    """Otra maquina u otra build de ffmpeg: sin `data/` ni marcas locales, solo el manifiesto
    sabe de que build salio la carpeta base `png-1fps`. La salida documentada (`--reemplaza-a`
    la activa) debe abrir OTRA carpeta y no un callejon sin salida (auditoria de cierre, A1)."""
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    datos = repo / "data"
    args = (repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0)
    r = extraer_video(*args, [])
    doc = yaml.safe_load(r.manifiesto.read_text(encoding="utf-8"))
    # Simular "otra build": el manifiesto de `r` registra la carpeta base con otro ffmpeg.
    shutil.rmtree(datos)
    texto = r.manifiesto.read_text(encoding="utf-8")
    r.manifiesto.write_text(
        texto.replace(f"ffmpeg: {doc['ffmpeg']}", "ffmpeg: otra-build"), encoding="utf-8"
    )
    with pytest.raises(FotogramasError, match="indica --reemplaza-a"):
        extraer_video(*args, [])
    with pytest.raises(FotogramasError, match="la extraccion activa"):
        extraer_video(*args, [], reemplaza_a="fr-v1-00000000")
    # Con la build de verdad el indice seria distinto; aqui se fuerza con un extra.
    r2 = extraer_video(*args, [1250], reemplaza_a=r.fotogramas_id)
    assert r2.carpeta.name.startswith("png-1fps-") and r2.fotogramas_id != r.fotogramas_id
    assert not (datos / "fotogramas" / "v1" / "png-1fps").exists()
    doc2 = yaml.safe_load(r2.manifiesto.read_text(encoding="utf-8"))
    assert doc2["reemplaza_a"] == r.fotogramas_id
    assert [t.id for t in cargar_todos(repo) if t.supersede is None] == [r.fotogramas_id]
    # Repetir la activa sin `reemplaza_a`: idempotente (ni error ni manifiesto nuevo).
    r3 = extraer_video(*args, [1250])
    assert r3.fotogramas_id == r2.fotogramas_id
    assert len(list((repo / "knowledge" / "corpus" / "fotogramas").glob("*.yaml"))) == 2
    # Video cambiado: sha256 distinto del manifiesto del corpus.
    with pytest.raises(FotogramasError, match="sha256"):
        extraer_video(repo, datos, raiz, "v1", NOMBRE_ACENTUADO, "0" * 64, 2.0, [])
    # Obligatorio fuera del video.
    with pytest.raises(FotogramasError, match="fuera del video"):
        extraer_video(repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0, [9000])


def test_start_time_distinto_de_cero_se_rechaza(tmp_path: Path) -> None:
    """Con `start_time` != 0 el `pts` de `-ss -copyts` (absoluto) y el `t` de `select`
    (relativo) no comparten reloj: extraer_video lo rechaza antes de decodificar."""
    _requiere_ffmpeg()
    repo, raiz, _ = _repo(tmp_path)
    desplazado = raiz / "offset.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-v",
            "error",
            "-y",
            "-i",
            str(CLIP),
            "-output_ts_offset",
            "0.5",
            "-c",
            "copy",
            str(desplazado),
        ],
        check=True,
    )
    from botsito.corpus.fotogramas import inicio_video_ms

    assert inicio_video_ms(CLIP) == 0 and 400 <= inicio_video_ms(desplazado) <= 500
    sha = sha256_hex(desplazado.read_bytes())
    with pytest.raises(FotogramasError, match=r"start_time \d+ ms"):
        extraer_video(repo, repo / "data", raiz, "v1", "offset.mp4", sha, 2.0, [])


def test_fuente_con_segundo_ausente_lo_declara(tmp_path: Path) -> None:
    """Un salto de la fuente que se lleva un segundo entero (< 2 s, sin hueco) queda declarado
    en `segundos_ausentes_ms`: `referencias()` no lo ofrece y un obligatorio ahi se reclama."""
    _requiere_ffmpeg()
    repo, raiz, _ = _repo(tmp_path)
    video = raiz / "salto.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-v",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=4:size=64x64:rate=10",
            "-vf",
            "select='lt(t,0.95)+gt(t,1.95)'",
            "-fps_mode",
            "passthrough",
            "-c:v",
            "mpeg4",
            "-q:v",
            "2",
            str(video),
        ],
        check=True,
    )
    sha = sha256_hex(video.read_bytes())
    r = extraer_video(repo, repo / "data", raiz, "v1", "salto.mp4", sha, 4.0, [])
    assert [f.t_ms for f in r.fotogramas] == [0, 2000, 3000]
    doc = yaml.safe_load(r.manifiesto.read_text(encoding="utf-8"))
    assert doc["segundos_ausentes_ms"] == [1000] and doc["huecos"] == []
    from botsito.corpus.fotogramas import Obligatorio
    from botsito.corpus.manifiestos_fotogramas import comprobar_obligatorios

    items = cargar_todos(repo)
    assert f"{r.fotogramas_id}/1000" not in items[0].referencias()
    assert f"{r.fotogramas_id}/2000" in items[0].referencias()
    assert len(comprobar_obligatorios(items, [Obligatorio("v1", 1000, "m", None)])) == 1
    assert comprobar(items, repo / "data") == ([], [])


def test_manifiesto_roto_es_error_de_cli(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _requiere_ffmpeg()
    repo, _, _ = _repo(tmp_path)
    d = repo / "knowledge" / "corpus" / "fotogramas"
    d.mkdir()
    (d / "fr-v1-deadbeef.yaml").write_text("fotogramas_id: [\n", encoding="utf-8")
    assert cli.main(["--repo", str(repo), "corpus", "frames", "extract", "--video", "v1"]) == 1
    assert "ERROR: fr-v1-deadbeef.yaml" in capsys.readouterr().out


def test_comprobar_detecta_alteraciones(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    repo, raiz, sha = _repo(tmp_path)
    datos = repo / "data"
    r = extraer_video(repo, datos, raiz, "v1", NOMBRE_ACENTUADO, sha, 2.0, [1250])
    items = cargar_todos(repo)
    assert comprobar(items, datos) == ([], [])
    extra = r.carpeta / "000001250.png"
    original = extra.read_bytes()
    extra.write_bytes(original[:-1] + b"\0")  # mismo tamano, otro hash
    errores, _ = comprobar(items, datos)
    assert len(errores) == 1 and "alterado (sha256 distinto del indice)" in errores[0]
    extra.write_bytes(original)
    regular = r.carpeta / "000001000.png"
    regular.write_bytes(b"x")
    errores, _ = comprobar(items, datos)
    assert any("otro tamano" in e for e in errores)
    regular.unlink()
    errores, _ = comprobar(items, datos)
    assert any("falta 000001000.png" in e for e in errores)
    indice = r.carpeta / FICHERO_INDICE
    indice.write_text(indice.read_text(encoding="utf-8").replace('"n": 0', '"n": 9'), "utf-8")
    errores, _ = comprobar(items, datos)
    assert errores == [f"{r.fotogramas_id}: index.jsonl alterado (sha256 distinto del manifiesto)"]
    shutil.rmtree(r.carpeta)
    errores, avisos = comprobar(items, datos)
    assert errores == [] and "no esta en esta maquina" in avisos[0]


def _clip_con_salto(destino: Path) -> None:
    """6 s a 10 fps sin los fotogramas entre 1 s y 4 s (hueco real de 3 s en la fuente)."""
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-v",
            "error",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "testsrc=duration=6:size=64x64:rate=10",
            "-vf",
            "select='lt(t,1)+gt(t,4)'",
            "-fps_mode",
            "passthrough",
            "-c:v",
            "mpeg4",
            "-q:v",
            "2",
            str(destino),
        ],
        check=True,
    )


def test_huecos_de_la_fuente_se_registran(tmp_path: Path) -> None:
    _requiere_ffmpeg()
    video = tmp_path / "salto.mp4"
    _clip_con_salto(video)
    fs, _ = extraer_regulares(video, tmp_path / "fr")
    segundos = [f.t_ms // 1000 for f in fs]
    assert 0 in segundos and 5 in segundos and 2 not in segundos and 3 not in segundos
    from botsito.corpus.fotogramas import huecos

    h = huecos(fs)
    assert len(h) == 1 and h[0]["ms"] > 2000


def test_cli_extract_check_show_y_knowledge_validate(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _requiere_ffmpeg()
    repo, _, _ = _repo(tmp_path, OBLIGATORIOS)
    base = ["--repo", str(repo), "corpus", "frames"]
    assert cli.main(base + ["extract", "--video", "v1"]) == 0
    salida = capsys.readouterr().out
    assert "OK: fr-v1-" in salida and "3 fotogramas, 1 extra" in salida
    assert cli.main(base + ["check"]) == 0
    assert "2 obligatorios presentes" in capsys.readouterr().out
    assert cli.main(base + ["show", "--video", "v1", "--t", "0:00:01.2", "--n", "2"]) == 0
    salida = capsys.readouterr().out
    fid = salida.splitlines()[0].split()[1]
    assert f"{fid}/1000\t0:00:01.000\tregular" in salida
    assert f"{fid}/1250\t0:00:01.300\tobligatorio" in salida
    assert "sin transcripcion activa" in salida
    assert cli.main(base + ["show", "--video", "v1", "--t", "0:00:09"]) == 1
    assert "fuera del video" in capsys.readouterr().out
    assert cli.main(base + ["show", "--video", "v9", "--t", "0:00:00"]) == 1
    assert cli.main(base + ["extract", "--video", "v9"]) == 1
    assert cli.main(base + ["extract", "--video", "v1", "--reemplaza-a", "fr-v1-00000000"]) == 1
    assert "no existe ese manifiesto" in capsys.readouterr().out
    # Un obligatorio nuevo con fraccion que aun no esta extraido: check y validate lo reclaman.
    (repo / "knowledge" / "corpus" / "fotogramas_obligatorios.yaml").write_text(
        OBLIGATORIOS + "  - {video_id: v1, t: '0:00:01.5', motivo: nuevo}\n", encoding="utf-8"
    )
    assert cli.main(base + ["check"]) == 1
    assert "v1 0:00:01.500: no esta en" in capsys.readouterr().out
    (repo / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros: []\n", encoding="utf-8"
    )
    (repo / "knowledge" / "evidence").mkdir()
    (repo / "knowledge" / "feedback").mkdir()
    (repo / "docs" / "adr").mkdir(parents=True)
    assert cli.main(["--repo", str(repo), "evidence", "contradictions"]) == 0
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 1
    assert "0:00:01.500" in capsys.readouterr().out
    (repo / "knowledge" / "corpus" / "fotogramas_obligatorios.yaml").write_text(
        OBLIGATORIOS, encoding="utf-8"
    )
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0
    assert "1 extracciones de fotogramas registradas" in capsys.readouterr().out
    # Sin data/: aviso, no error.
    shutil.rmtree(repo / "data")
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0
    assert "AVISO" in capsys.readouterr().out
    assert cli.main(base + ["show", "--video", "v1", "--t", "0:00:01"]) == 1
    assert "no estan en esta maquina" in capsys.readouterr().out


def test_show_con_transcripcion_activa(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _requiere_ffmpeg()
    repo, _, _ = _repo(tmp_path)
    base = ["--repo", str(repo), "corpus"]
    assert cli.main(base + ["transcribe", "--video", "v1", "--motor", "falso"]) == 0
    assert cli.main(base + ["frames", "extract", "--video", "v1"]) == 0
    capsys.readouterr()
    assert cli.main(base + ["frames", "show", "--video", "v1", "--t", "0:00:01"]) == 0
    salida = capsys.readouterr().out
    assert "(cruda):" in salida and "[0:00:00.000] texto falso" in salida
    # Borde exacto del segmento falso (0-2 s): un instante en t1 tambien lo cita.
    assert cli.main(base + ["frames", "show", "--video", "v1", "--t", "0:00:02"]) == 0
    assert "[0:00:00.000] texto falso" in capsys.readouterr().out
    indice = cargar_indice(repo / "data" / "fotogramas" / "v1" / "png-1fps")
    assert len(indice) == 2
