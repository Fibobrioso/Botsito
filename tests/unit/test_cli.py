import os
import shutil
import subprocess
from pathlib import Path

import pytest

from botsito import __version__, cli

CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"
TEMAS = Path(__file__).resolve().parents[2] / "knowledge" / "evidence" / "_temas.yaml"

MINIMO = """# PROJECT STATE

## Current Feature
F99

## Current Branch
{branch}

## Completed Features
{completed}

## Tests Currently Passing
{tests}

## Last Stable Commit
{stable}
"""


def _repo_tmp(tmp_path: Path, branch: str = "main") -> Path:
    subprocess.run(["git", "init", "-q", "-b", branch], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_a.py").write_text(
        "def test_uno():\n    pass\n\ndef test_dos():\n    pass\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    return tmp_path


def _state(repo: Path, **kw: str) -> None:
    valores = {"branch": "main", "completed": "—", "tests": "2", "stable": "—"}
    valores.update(kw)
    (repo / "PROJECT_STATE.md").write_text(MINIMO.format(**valores), encoding="utf-8")


def test_version() -> None:
    assert __version__ == "0.1.0"


def test_state_check_ok_on_real_repo(repo: Path) -> None:
    branch = subprocess.run(
        ["git", "symbolic-ref", "--short", "HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.strip()
    if not branch:  # HEAD separado (CI de pull request): solo se omite la rama
        pytest.skip("HEAD separado: no hay rama que comprobar")
    assert cli.state_check(repo) == 0


def test_detects_branch_mismatch(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, branch="feature/F99-otra")
    assert cli.state_check(r) == 1


def test_detects_wrong_test_count(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, tests="7 (inventado)")
    assert cli.state_check(r) == 1


def test_detects_stable_commit_mismatch_with_tag(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, stable="deadbee · falso")
    subprocess.run(["git", "add", "-A"], cwd=r, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "x"], cwd=r, check=True)
    subprocess.run(["git", "tag", "-a", "stable/F99", "-m", "t"], cwd=r, check=True)
    assert cli.state_check(r) == 1
    real = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=r, capture_output=True, text=True, check=True
    ).stdout.strip()
    _state(r, stable=f"{real} · merge")
    assert cli.state_check(r) == 0


def test_detects_completed_feature_without_report(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r, completed="- F99 · algo")
    assert cli.state_check(r) == 1
    (r / "docs" / "validation" / "F99-algo.md").write_text("ok", encoding="utf-8")
    assert cli.state_check(r) == 0


def test_state_check_missing_file(tmp_path: Path) -> None:
    assert cli.state_check(tmp_path) == 2


def test_contar_tests(tmp_path: Path) -> None:
    assert cli.contar_tests(_repo_tmp(tmp_path)) == 2


def test_knowledge_validate_real_repo(repo: Path) -> None:
    assert cli.knowledge_validate(repo) == 0


def test_knowledge_validate_detecta_registro_roto(tmp_path: Path) -> None:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros:\n  - nombre: x\n", encoding="utf-8"
    )
    assert cli.knowledge_validate(tmp_path) == 1


def test_cli_entrypoint_runs(repo: Path) -> None:
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0


def test_config_validate_real_repo(repo: Path) -> None:
    assert cli.config_validate(repo) == 0


def test_config_validate_detecta_clave_del_registro(tmp_path: Path) -> None:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    (tmp_path / "knowledge" / "spec" / "parametros.yaml").write_text(
        "parametros:\n  - nombre: stop_fraccion\n    categoria: estrategia\n    tipo: fraccion\n"
        '    unidad: u\n    descripcion: d\n    estado: CONFIRMED\n    valor: "0.75"\n'
        "    fuente: {tipo: decision, id: ADR-0001}\n",
        encoding="utf-8",
    )
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\nstop_fraccion = "0.5"\n\n'
        '[rutas]\ncorpus = "c"\ndata = "d"\nknowledge = "k"\n',
        encoding="utf-8",
    )
    assert cli.config_validate(tmp_path) == 1
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n[rutas]\ncorpus = "c"\ndata = "d"\nknowledge = "k"\n',
        encoding="utf-8",
    )
    assert cli.config_validate(tmp_path) == 0
    assert cli.main(["--repo", str(tmp_path), "config", "validate"]) == 0


def test_main_no_admite_cambios_sin_tag_salvo_el_estado(tmp_path: Path) -> None:
    r = _repo_tmp(tmp_path)
    _state(r)
    subprocess.run(["git", "add", "-A"], cwd=r, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "x"], cwd=r, check=True)
    subprocess.run(["git", "tag", "-a", "stable/F99", "-m", "t"], cwd=r, check=True)
    real = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], cwd=r, capture_output=True, text=True, check=True
    ).stdout.strip()
    _state(r, stable=f"{real} · merge")
    subprocess.run(["git", "commit", "-q", "-am", "docs(state)"], cwd=r, check=True)
    assert cli.state_check(r) == 0
    (r / "src.py").write_text("x = 1\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=r, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "colado en main"], cwd=r, check=True)
    assert cli.state_check(r) == 1


FUENTES_MIN = (
    'raiz: "corpus"\nvideos:\n  - video_id: v1\n    fichero: "clip.mp4"\n    drive_id: d1\n'
    '    bytes: 1\n    fecha_grabacion: "2026-01-01"\n    naturaleza: prueba\n'
)
MANIFIESTO_MIN = (
    "version: 1\nraiz: corpus\nvideos:\n  - video_id: v1\n    fichero: clip.mp4\n    bytes: 1\n"
    "    sha256: " + "a" * 64 + "\n    duracion_s: 120.0\n    ancho: 1\n    alto: 1\n"
    "    audio: true\nficheros:\n  - ruta: Material adicional/sesion-01.mp4\n"
    "    papel: material_adicional\n    bytes: 1\n"
)
PARAMETROS_MIN = (
    "parametros:\n"
    "  - nombre: stop_fraccion\n    categoria: estrategia\n    tipo: fraccion\n"
    "    unidad: u\n    descripcion: d\n    estado: UNKNOWN\n"
    "  - nombre: spread_max\n    categoria: broker\n    tipo: decimal\n"
    "    unidad: u\n    descripcion: d\n    estado: UNKNOWN\n"
)


def _knowledge_tmp(tmp_path: Path) -> Path:
    """knowledge/ minimo con fuentes, manifiesto, registro con dos parametros y evidencia vacia."""
    for d in ("corpus", "spec", "evidence", "feedback"):
        (tmp_path / "knowledge" / d).mkdir(parents=True)
    (tmp_path / "knowledge" / "corpus" / "fuentes.yaml").write_text(FUENTES_MIN, encoding="utf-8")
    (tmp_path / "knowledge" / "corpus" / "manifest.yaml").write_text(
        MANIFIESTO_MIN, encoding="utf-8"
    )
    (tmp_path / "knowledge" / "spec" / "parametros.yaml").write_text(
        PARAMETROS_MIN, encoding="utf-8"
    )
    shutil.copy(TEMAS, tmp_path / "knowledge" / "evidence" / "_temas.yaml")
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0001-x.md").write_text("# 1", encoding="utf-8")
    (tmp_path / "docs" / "adr" / "0000-template.md").write_text("# t", encoding="utf-8")
    return tmp_path


def _knowledge_con_cruda(tmp_path: Path) -> tuple[Path, str, str]:
    """knowledge/ minimo mas una transcripcion real del clip con el motor falso: devuelve
    (repo, transcripcion_id, cita localizable en la cruda)."""
    if shutil.which("ffmpeg") is None:
        if os.environ.get("CI"):
            pytest.fail("ffmpeg no esta en PATH y en CI es obligatorio")
        pytest.skip("ffmpeg no disponible")
    from botsito.comun.documentos import sha256_hex
    from botsito.corpus.glosario import glosario_desde_texto
    from botsito.corpus.pipeline_transcripcion import cargar_cruda, transcribir_video
    from botsito.corpus.transcripcion import MotorFalso

    repo = _knowledge_tmp(tmp_path)
    raiz = repo / "corpus"
    raiz.mkdir()
    shutil.copy(CLIP, raiz / "clip.mp4")
    sha = sha256_hex((raiz / "clip.mp4").read_bytes())
    (repo / "knowledge" / "corpus" / "fuentes.yaml").write_text(
        FUENTES_MIN.replace("bytes: 1", f"bytes: {(raiz / 'clip.mp4').stat().st_size}"),
        encoding="utf-8",
    )
    (repo / "knowledge" / "corpus" / "manifest.yaml").write_text(
        "version: 1\nraiz: corpus\nvideos:\n  - video_id: v1\n    fichero: clip.mp4\n"
        f"    bytes: {(raiz / 'clip.mp4').stat().st_size}\n    sha256: {sha}\n"
        "    duracion_s: 2.0\n    ancho: 1\n    alto: 1\n    audio: true\nficheros: []\n",
        encoding="utf-8",
    )
    glosario = "vocabulario: [otro]\nsustituciones: []\n"
    (repo / "knowledge" / "corpus" / "glosario_asr.yaml").write_text(glosario, encoding="utf-8")
    (repo / "config").mkdir()
    (repo / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n'
        '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n',
        encoding="utf-8",
    )
    r = transcribir_video(
        repo,
        repo / "data",
        raiz,
        "v1",
        "clip.mp4",
        sha,
        2.0,
        MotorFalso(),
        glosario_desde_texto(glosario),
    )
    cita = cargar_cruda(r.carpeta)[0].texto
    return repo, r.transcripcion_id, cita


def _ev_args(repo: Path, **extra: str) -> list[str]:
    campos = {
        "video": "v1",
        "t0": "0:00:01",
        "t1": "0:00:02",
        "modalidad": "pantalla",
        "tipo": "UNKNOWN",
        "cita": "cita de prueba larga",
        "afirmacion": "x",
        "tema": "meta.prueba",
        "confianza": "baja",
        "extractor": "humano",
        "revisado-por": "t",
        "fotograma": "fr-v1-0123abcd/1000",
    }
    campos.update(extra)
    args = ["--repo", str(repo), "evidence", "new"]
    for k, v in campos.items():
        args += [f"--{k}", v]
    return args


def _fb_args(repo: Path, **extra: str) -> list[str]:
    campos = {
        "sesion": "2026-09-20-sesion-01",
        "fecha": "2026-09-20",
        "medio": "escrito",
        "objetivo-tipo": "parametro",
        "objetivo-id": "stop_fraccion",
        "accion": "CONFIRM",
        "respuesta": "si, el stop va al 0,75 siempre",
        "registrado-por": "aleks",
    }
    campos.update(extra)
    args = ["--repo", str(repo), "feedback", "new"]
    for k, v in campos.items():
        args += [f"--{k}", v]
    return args


def test_ids_de_adr(tmp_path: Path) -> None:
    _knowledge_tmp(tmp_path)
    from botsito.validation.knowledge import ids_de_adr

    assert ids_de_adr(tmp_path) == {"ADR-0001"}


def test_evidence_new_valida_contra_el_manifiesto_antes_de_escribir(tmp_path: Path) -> None:
    repo = _knowledge_tmp(tmp_path)
    # Sin fotogramas registrados, ninguna referencia es conocida: el item de pantalla no entra.
    assert cli.main(_ev_args(repo, t1="0:05:00")) == 1  # supera la duracion (120 s)
    assert cli.main(_ev_args(repo, fotograma="no/existe.jpg")) == 1
    assert cli.main(_ev_args(repo, afirmacion="   ")) == 1
    assert cli.main(_ev_args(repo)) == 1  # referencia no conocida
    assert not list((repo / "knowledge" / "evidence").rglob("ev-*.yaml"))


def test_evidence_new_de_audio_exige_cita_localizada_en_la_cruda(tmp_path: Path) -> None:
    repo, tid, cita = _knowledge_con_cruda(tmp_path)
    audio = {
        "modalidad": "audio",
        "fotograma": None,
        "t0": "0:00:00",
        "t1": "0:00:02",
        "cita": cita,
    }
    args = {k: v for k, v in audio.items() if v is not None}
    # Parafrasis: no se localiza; transcripcion que no es la activa: error. Todo antes de
    # escribir.
    assert cli.main(_ev_args_sin(repo, **dict(args, cita="esto no lo dice la cruda"))) == 1
    assert cli.main(_ev_args_sin(repo, **args, transcripcion="tr-v1-falso-00000000")) == 1
    assert not list((repo / "knowledge" / "evidence").rglob("ev-*.yaml"))
    assert cli.main(_ev_args_sin(repo, **args)) == 0
    ficheros = list((repo / "knowledge" / "evidence").rglob("ev-*.yaml"))
    assert len(ficheros) == 1 and tid in ficheros[0].read_text(encoding="utf-8")
    assert cli.main(_ev_args_sin(repo, **args)) == 1  # mismo contenido: ya existe
    assert cli.main(["--repo", str(repo), "evidence", "list"]) == 0


def _ev_args_sin(repo: Path, **extra: str) -> list[str]:
    """Como `_ev_args` pero sin el fotograma por defecto (items de audio)."""
    campos = {
        "video": "v1",
        "t0": "0:00:01",
        "t1": "0:00:02",
        "modalidad": "audio",
        "tipo": "UNKNOWN",
        "cita": "cita de prueba larga",
        "afirmacion": "x",
        "tema": "meta.prueba",
        "confianza": "baja",
        "extractor": "humano",
        "revisado-por": "t",
    }
    campos.update(extra)
    args = ["--repo", str(repo), "evidence", "new"]
    for k, v in campos.items():
        args += [f"--{k}", v]
    return args


def test_propose_check_accept_reject(tmp_path: Path) -> None:
    import yaml

    repo, tid, cita = _knowledge_con_cruda(tmp_path)
    (repo / "knowledge" / "_proposals").mkdir()
    (repo / "knowledge" / "_proposals" / "PROMPT.md").write_text("# prompt v1\n", encoding="utf-8")
    base = ["--repo", str(repo), "evidence", "propose", "--video", "v1", "--t0", "0:00:00"]
    assert cli.main([*base, "--t1", "0:00:02", "--modelo", "falso", "--tema-buscado", "meta"]) == 0
    ficheros = list((repo / "knowledge" / "_proposals").glob("pr-*.yaml"))
    assert len(ficheros) == 1
    ruta = ficheros[0]
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    assert doc["items"] == [] and doc["temas_buscados"] == ["meta"]
    assert doc["contexto"]["segmentos"][0]["texto"] == cita
    check = ["--repo", str(repo), "evidence", "propose", "--check", str(ruta)]
    assert cli.main(check) == 1  # tema buscado sin item ni no_consta
    item = {
        "n": 1,
        "t0": "0:00:00",
        "t1": "0:00:02",
        "modalidad": "audio",
        "tipo": "UNKNOWN",
        "cita_literal": cita,
        "afirmacion": "texto falso",
        "tema": "meta.prueba",
        "confianza": "baja",
    }
    doc["items"] = [item, dict(item, n=2, tema="fuera.taxonomia")]
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    assert cli.main(check) == 1  # misma cita dos veces y tema fuera de la taxonomia
    doc["items"] = [item]
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")
    assert cli.main(check) == 0
    sellada = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    assert sellada["salida_sha256"]
    acc = [
        "--repo",
        str(repo),
        "evidence",
        "accept",
        "--propuesta",
        str(ruta),
        "--item",
        "1",
        "--revisado-por",
        "t · hoja · cruda leida",
    ]
    assert cli.main([*acc, "--metodo", "cruda_leida"]) == 0
    assert len(list((repo / "knowledge" / "evidence").rglob("ev-*.yaml"))) == 1
    assert cli.main([*acc, "--metodo", "cruda_leida"]) == 1  # ya aceptado
    anotada = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    assert anotada["items"][0]["decision"] == "aceptado"
    assert anotada["items"][0]["evidence_id"].startswith("ev-v1-")
    # La salida esta sellada: cambiar la cita despues del check se detecta.
    anotada["items"][0]["cita_literal"] = "otra cosa distinta ahora"
    ruta.write_text(yaml.safe_dump(anotada, allow_unicode=True, sort_keys=False), encoding="utf-8")
    rej = [
        "--repo",
        str(repo),
        "evidence",
        "reject",
        "--propuesta",
        str(ruta),
        "--item",
        "1",
        "--motivo",
        "m",
        "--decidido-por",
        "t",
    ]
    assert cli.main(rej) == 1
    from botsito.validation.knowledge import validar

    codigo, lineas = validar(repo)
    assert codigo == 1 and any("cambio despues del check" in x for x in lineas)


def test_feedback_new_valida_contra_el_contexto_antes_de_escribir(tmp_path: Path) -> None:
    repo = _knowledge_tmp(tmp_path)
    fb = repo / "knowledge" / "feedback"
    assert cli.main(_fb_args(repo, **{"objetivo-id": "no_existe"})) == 1
    assert (
        cli.main(
            _fb_args(repo, **{"objetivo-tipo": "evidence", "objetivo-id": "ev-v1-000001-deadbeef"})
        )
        == 1
    )
    assert (
        cli.main(_fb_args(repo, medio="replay", grabacion="otra.mp4", t0="0:00:01", t1="0:00:02"))
        == 1
    )
    assert cli.main(_fb_args(repo, sesion="")) == 1  # error de dominio, no KeyError
    assert cli.main(_fb_args(repo, valor="   ")) == 0  # el blanco no rompe el id
    assert len(list(fb.rglob("*.yaml"))) == 1
    assert cli.main(["--repo", str(repo), "evidence", "contradictions"]) == 0
    assert cli.main(["--repo", str(repo), "knowledge", "validate"]) == 0
    assert cli.main(_fb_args(repo)) == 1  # mismo contenido: ya existe
    assert (
        cli.main(_fb_args(repo, **{"objetivo-id": "spread_max"}, respuesta="otra respuesta larga"))
        == 0
    )
    assert cli.main(["--repo", str(repo), "feedback", "trace", "stop_fraccion"]) == 0
    assert cli.main(["--repo", str(repo), "feedback", "pending"]) == 0
    assert cli.main(["--repo", str(tmp_path / "nada"), "feedback", "new"] + _fb_args(repo)[4:]) == 2
    assert not (tmp_path / "nada").exists()


def test_feedback_pending_omite_parametros_que_no_son_de_estrategia(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _knowledge_tmp(tmp_path)
    assert cli.main(_fb_args(repo)) == 0
    assert cli.main(_fb_args(repo, **{"objetivo-id": "spread_max"})) == 0
    capsys.readouterr()
    assert cli.feedback_pending(repo) == 0
    salida = capsys.readouterr().out
    assert "stop_fraccion" in salida and "spread_max" not in salida
    assert "1 registros activos" in salida


def test_evidence_new_rechaza_video_fuera_de_fuentes(tmp_path: Path) -> None:
    repo = _knowledge_tmp(tmp_path)
    args = [
        "--repo",
        str(repo),
        "evidence",
        "new",
        "--video",
        "V1",
        "--t0",
        "0:00:01",
        "--t1",
        "0:00:02",
        "--modalidad",
        "audio",
        "--tipo",
        "UNKNOWN",
        "--cita",
        "cita de prueba",
        "--afirmacion",
        "x",
        "--tema",
        "x",
        "--confianza",
        "baja",
        "--extractor",
        "humano",
        "--revisado-por",
        "t",
    ]
    assert cli.main(args) == 1
    assert not (repo / "knowledge" / "evidence" / "V1").exists()
