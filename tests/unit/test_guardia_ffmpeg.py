"""ffprobe y ffmpeg en la guardia de Claude Code: cuatro formas de LISTA CERRADA sobre un video que
no se protege, y todo lo demas negado (`trabajo/guardia-ffmpeg`, docs/validation/GUARDIA-FFMPEG.md).

La matriz se decide con el texto de cada comando sobre videos inventados en un repo de `tmp_path`,
SIN SEGUIR como el video real de una sesion (que vive en `corpus/`, fuera de git); nunca se ejecuta
ffmpeg. Las rutas del material protegido se montan a trozos: este fichero lo lee la guardia como
codigo cuando se le pasa a pytest, y un literal con la ruta entera la haria negarlo.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
ESTRATEGIA = "corp" + "us/Estrategia del trader"
MATERIAL = ESTRATEGIA + "/Material adicional de su operativa"
VIDEO = ESTRATEGIA + "/sesion-05.mp4"
MARZO = MATERIAL + "/Back" + "test marzo 2026/v.mp4"
IMAGEN = MATERIAL + "/WhatsApp Image.jpeg"


@pytest.fixture(scope="module")
def g() -> ModuleType:
    nombre = "guardia_claude"  # el mismo que `test_guardia_claude.py`: un solo modulo cargado
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, GUARDIA)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _git(repo: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    r.mkdir()
    (r / "Makefile").write_text("x\n", encoding="utf-8")
    (r / ".gitignore").write_text("/corp" + "us/\n/data/*\n", encoding="utf-8")
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    # Despues del commit: sin seguir, como el video real; binarios, como un video (el principio de
    # un mp4), porque la regla niega una entrada de texto (puede ser una lista `ffconcat`).
    for rel in (VIDEO, MARZO, IMAGEN, "otro.wav"):
        ruta = r / rel
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_bytes(b"\x00\x00\x00\x20ftypisom\x00\x00\x02\x00")
    (r / "lista.txt").write_text("ffconcat version 1.0\nfile 'otro.wav'\n", encoding="utf-8")
    (r / "lista.mp4").write_text("ffconcat version 1.0\nfile 'otro.wav'\n", encoding="utf-8")
    (r / "docs").mkdir()
    (tmp_path / "fuera").mkdir()
    return r


def _decide(modulo: ModuleType, repo: Path, comando: str) -> str | None:
    evento = {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(repo)}
    motivo: str | None = modulo.decidir(evento, modulo.Politica(repo))
    return motivo


def _regla(modulo: ModuleType, motivo: str | None) -> str:
    """`pasa`, o el nombre de la constante de regla que cita el motivo."""
    if motivo is None:
        return "pasa"
    nombres = [
        n for n in dir(modulo) if n.startswith("R_") and f"Regla: {getattr(modulo, n)}" in motivo
    ]
    assert len(nombres) == 1, motivo
    return nombres[0]


V = f'"{VIDEO}"'
SIL = "-vn -sn -dn -af silencedetect=noise=-50dB:d=30 -f null"
VOL = "-vn -sn -dn -af volumedetect -f null"
EXT = "-vn -sn -dn -ac 1 -ar 16000"

# (nombre, comando con {VA} = el video absoluto, {FUERA} = un directorio fuera del repo y {REPO} =
# la raiz, y la decision esperada).
PERMITIDAS = [
    ("ffprobe, relativa", f"ffprobe -v error -show_format -show_streams {V}"),
    (
        "ffprobe, absoluta con -i",
        "ffprobe -hide_banner -loglevel error -select_streams a:0 "
        '-show_entries stream=codec_name,channels -of json -i "{VA}"',
    ),
    ("ffprobe, -print_format", f"ffprobe -v quiet -print_format json -show_format {V}"),
    (
        "silencios, relativa",
        f"ffmpeg -hide_banner -nostdin -nostats -i {V} {SIL} - 2>&1 | grep silence_",
    ),
    (
        "silencios, absoluta a NUL",
        'ffmpeg -nostdin -i "{VA}" -vn -sn -dn -af silencedetect=noise=-30.5dB:d=0.5 -f null NUL',
    ),
    ("volumen, relativa a /dev/null", f"ffmpeg -v info -i {V} {VOL} /dev/null"),
    ("volumen, absoluta", 'ffmpeg -hide_banner -i "{VA}" ' + VOL + " -"),
    ("volumen, stderr fuera del repo", f'ffmpeg -i {V} {VOL} - 2> "{{FUERA}}/volumen.txt"'),
    (
        "extraccion, salida absoluta",
        f'ffmpeg -hide_banner -nostdin -y -i {V} {EXT} -c:a pcm_s16le "{{FUERA}}/sesion-05.wav"',
    ),
    (
        "extraccion, salida relativa",
        'ffmpeg -n -i "{VA}" -vn -sn -dn -acodec flac ../fuera/sesion-05.flac',
    ),
    ("extraccion, mp3", f'ffmpeg -i {V} -vn -sn -dn "{{FUERA}}/sesion-05.mp3"'),
    (
        "extraccion, m4a tras cd",
        f'cd "{{REPO}}" && ffmpeg -i {V} -vn -sn -dn -ar 44100 "{{FUERA}}/s.m4a"',
    ),
    # Las formas exactas de la skill ingerir-sesion, paso 2 (copiadas de alli).
    (
        "skill: silencios",
        f"ffmpeg -hide_banner -nostdin -i {V} -vn -sn -dn "
        "-af silencedetect=noise=-50dB:d=30 -f null - 2>&1 | grep silence_",
    ),
    (
        "skill: volumen",
        f"ffmpeg -hide_banner -nostdin -i {V} -vn -sn -dn -af volumedetect -f null - 2>&1 "
        '| grep -E "mean_volume|max_volume"',
    ),
    ("skill: metadatos", f"ffprobe -v error -show_format -show_streams {V}"),
    (
        "skill: audio fuera del repo",
        f"ffmpeg -hide_banner -nostdin -i {V} -vn -sn -dn -ac 1 -ar 16000 "
        '"{FUERA}/sesion-05.wav"',
    ),
]
NEGADAS = [
    ("entrada protegida, ffprobe", f'ffprobe -v error -show_format "{MARZO}"', "R_SIN_ABRIR"),
    ("entrada protegida, medida", f'ffmpeg -i "{MARZO}" {VOL} -', "R_SIN_ABRIR"),
    (
        "entrada protegida, extraccion",
        f'ffmpeg -i "{MARZO}" {EXT} "{{FUERA}}/a.wav"',
        "R_SIN_ABRIR",
    ),
    ("entrada protegida, imagen", f'ffprobe -show_streams "{IMAGEN}"', "R_CAPTURA"),
    ("dos -i", f"ffmpeg -i {V} -i otro.wav {VOL} -", "R_FFMPEG"),
    ("ffprobe con dos entradas", f"ffprobe -show_format {V} otro.wav", "R_FFMPEG"),
    ("salida en el repo, relativa", f"ffmpeg -i {V} {EXT} audio.wav", "R_FFMPEG"),
    ("salida en el repo, absoluta", f'ffmpeg -i {V} {EXT} "{{REPO}}/data/audio.wav"', "R_FFMPEG"),
    ("salida a la salida estandar", f"ffmpeg -i {V} {EXT} -", "R_FFMPEG"),
    ("salida pipe:", f"ffmpeg -i {V} {EXT} pipe:1", "R_FFMPEG"),
    ("salida que no es audio", f'ffmpeg -i {V} {EXT} "{{FUERA}}/a.mp4"', "R_FFMPEG"),
    ("medida a un fichero", f'ffmpeg -i {V} {SIL} "{{FUERA}}/x.txt"', "R_FFMPEG"),
    ("-f distinto de null", f"ffmpeg -i {V} -vn -sn -dn -af volumedetect -f wav -", "R_FFMPEG"),
    ("-f en la extraccion", f'ffmpeg -i {V} {EXT} -f wav "{{FUERA}}/a.wav"', "R_FFMPEG"),
    ("-map", f'ffmpeg -i {V} {EXT} -map 0:a "{{FUERA}}/a.wav"', "R_FFMPEG"),
    ("-filter_complex", f'ffmpeg -i {V} {EXT} -filter_complex anull "{{FUERA}}/a.wav"', "R_FFMPEG"),
    ("-af en la extraccion", f'ffmpeg -i {V} {EXT} -af volumedetect "{{FUERA}}/a.wav"', "R_FFMPEG"),
    (
        "-af con amovie=",
        f"ffmpeg -i {V} -vn -sn -dn -af amovie=otro.wav,volumedetect -f null -",
        "R_FFMPEG",
    ),
    ("-af con otro filtro", f"ffmpeg -i {V} -vn -sn -dn -af loudnorm -f null -", "R_FFMPEG"),
    (
        "-af con dos filtros",
        f"ffmpeg -i {V} -vn -sn -dn -af volumedetect,silencedetect -f null -",
        "R_FFMPEG",
    ),
    ("-report", f"ffmpeg -report -i {V} {VOL} -", "R_FFMPEG"),
    ("-vstats_file", f'ffmpeg -i {V} {VOL} -vstats_file "{{FUERA}}/v.txt" -', "R_FFMPEG"),
    ("-progress", f'ffmpeg -progress "{{FUERA}}/p.txt" -i {V} {VOL} -', "R_FFMPEG"),
    ("-dump_attachment", f'ffmpeg -dump_attachment:t "" -i {V} {VOL} -', "R_FFMPEG"),
    ("-f concat antes de -i", f"ffmpeg -f concat -safe 0 -i lista.txt {VOL} -", "R_FFMPEG"),
    ("-af antes de -i", f"ffmpeg -af volumedetect -i {V} -vn -sn -dn -f null -", "R_FFMPEG"),
    ("protocolo concat:", f'ffmpeg -i "concat:{VIDEO}|otro.wav" {VOL} -', "R_FFMPEG"),
    ("protocolo subfile", f'ffmpeg -i "subfile,,start,0,end,99,,:{VIDEO}" {VOL} -', "R_FFMPEG"),
    ("protocolo file:", f'ffmpeg -i "file:{VIDEO}" {EXT} "{{FUERA}}/a.wav"', "R_FFMPEG"),
    ("protocolo en ffprobe", f'ffprobe -show_format "file:{VIDEO}"', "R_FFMPEG"),
    ("protocolo sobre marzo", f'ffprobe -show_format "file:{MARZO}"', "R_FFMPEG"),
    ("letra de unidad sin barra", 'ffprobe -show_format "C:x.mp4"', "R_FFMPEG"),
    ("ffprobe -show_data", f"ffprobe -show_data {V}", "R_FFMPEG"),
    ("ffprobe -o", f'ffprobe -show_format -o "{{FUERA}}/f.txt" {V}', "R_FFMPEG"),
    ("ffprobe -report", f"ffprobe -report -show_format {V}", "R_FFMPEG"),
    ("FFREPORT en el entorno", f"FFREPORT=file=x.log ffmpeg -i {V} {VOL} -", "R_EJECUCION"),
    ("redireccion 2> dentro del repo", f"ffmpeg -i {V} {VOL} - 2> volumen.txt", "R_FFMPEG"),
    ("redireccion > dentro del repo", f"ffprobe -show_format {V} > meta.json", "R_FFMPEG"),
    ("ffmpeg dentro de una sustitucion", f'echo "$(ffmpeg -i {V} {VOL} - 2>&1)"', "R_FFMPEG"),
    ("una entrada dinamica", f'ffmpeg -i "$VIDEO_X" {VOL} -', "R_FFMPEG"),
    (
        "una entrada con glob",
        f"ffprobe -show_format {ESTRATEGIA.replace(' ', '?')}/*.mp4",
        "R_FFMPEG",
    ),
    ("una entrada con %d", f'ffprobe -show_format "{ESTRATEGIA}/img%03d.png"', "R_FFMPEG"),
    ("sin -sn", f"ffmpeg -i {V} -vn -dn -af volumedetect -f null -", "R_FFMPEG"),
    ("opcion repetida", f"ffmpeg -i {V} -vn -vn -sn -dn -af volumedetect -f null -", "R_FFMPEG"),
    ("opcion tras la salida", f'ffmpeg -i {V} {EXT} "{{FUERA}}/a.wav" -y', "R_FFMPEG"),
    (
        "-c:a y -acodec",
        f'ffmpeg -i {V} {EXT} -c:a flac -acodec flac "{{FUERA}}/a.flac"',
        "R_FFMPEG",
    ),
    ("ffmpeg -version", "ffmpeg -version", "R_FFMPEG"),
    # Los del revisor de la rama (b1, b2, b4 y a4): lo que va antes y a la vez, las redirecciones
    # de entrada, el directorio y la entrada de texto.
    (
        "find -exec ffprobe {}",
        'find "{REPO}/.." -name "*.mp4" -exec ffprobe -show_format {} \\;',
        "R_EJECUCION",
    ),
    ("cd - delante", f'cd "{{FUERA}}" && cd - && ffprobe -show_format {V}', "R_EJECUCION"),
    ("cd dinamico delante", f'cd "$DIR_X" && ffprobe -show_format {V}', "R_EJECUCION"),
    ("cp delante", f"cp otro.wav b.wav && ffprobe -show_format {V}", "R_EJECUCION"),
    ("cd o true delante", f'cd "{{FUERA}}" || true; ffprobe -show_format {V}', "R_EJECUCION"),
    ("| tee detras", f"ffprobe -show_format {V} | tee meta.json", "R_EJECUCION"),
    ("en segundo plano", f"ffprobe -show_format {V} & cat otro.wav", "R_EJECUCION"),
    (
        "sustitucion en el mismo comando",
        f"ffprobe -show_format {V} && echo $(git rev-parse HEAD)",
        "R_FFMPEG",
    ),
    ("redireccion 1<> dentro del repo", f"ffprobe -show_format {V} 1<>meta.json", "R_FFMPEG"),
    ("redireccion de entrada", f"ffmpeg -i {V} {VOL} - < otro.wav", "R_FFMPEG"),
    ("entrada que es un directorio", "ffprobe -show_format docs", "R_FFMPEG"),
    ("entrada de texto (ffconcat)", f"ffmpeg -i lista.mp4 {VOL} -", "R_FFMPEG"),
]
MATRIZ = [(n, c, "pasa") for n, c in PERMITIDAS] + NEGADAS


def _comando(plantilla: str, repo: Path) -> str:
    return (
        plantilla.replace("{VA}", (repo / VIDEO).as_posix())
        .replace("{FUERA}", (repo.parent / "fuera").as_posix())
        .replace("{REPO}", repo.as_posix())
    )


def _matriz(modulo: ModuleType, repo: Path) -> list[tuple[str, str]]:
    return [(n, _regla(modulo, _decide(modulo, repo, _comando(c, repo)))) for n, c, _e in MATRIZ]


def test_la_matriz_de_ffmpeg(g: ModuleType, repo: Path) -> None:
    obtenido = _matriz(g, repo)
    for (nombre, decision), (_n, comando, esperado) in zip(obtenido, MATRIZ, strict=True):
        print(f"| {nombre} | `{comando}` | {decision} | {esperado} |")  # la tabla del informe
    assert obtenido == [(n, e) for n, _c, e in MATRIZ]


def test_sin_la_regla_las_permitidas_vuelven_a_negarse(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito: sin ffmpeg ni ffprobe en la regla, la guardia vuelve a la de `main`."""
    monkeypatch.setattr(g, "PROGRAMAS_FFMPEG", frozenset())
    for nombre, comando in PERMITIDAS:
        motivo = _decide(g, repo, _comando(comando, repo))
        print(f"sin la regla | {nombre} | {_regla(g, motivo)}")
        assert _regla(g, motivo) == "R_EJECUCION", nombre


def test_con_una_opcion_de_mas_un_negado_pasa(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito en el otro sentido: con `-map` en la extraccion o `-report` en ffprobe, el
    negado correspondiente pasa; la lista cerrada es lo que lo niega."""
    casos = dict((n, c) for n, c, _e in NEGADAS)
    monkeypatch.setattr(
        g, "FFMPEG_EXTRACCION_CON_VALOR", {**g.FFMPEG_EXTRACCION_CON_VALOR, "-map": r"\S+"}
    )
    monkeypatch.setattr(g, "FFPROBE_SIN_VALOR", g.FFPROBE_SIN_VALOR | {"-report"})
    for nombre in ("-map", "ffprobe -report"):
        motivo = _decide(g, repo, _comando(casos[nombre], repo))
        print(f"con una opcion de mas | {nombre} | {_regla(g, motivo)}")
        assert motivo is None, nombre


@pytest.mark.skipif(sys.platform != "win32", reason="los alias de ruta son de Windows")
def test_un_alias_de_la_raiz_no_saca_la_salida_ni_abre_la_entrada(
    g: ModuleType, repo: Path
) -> None:
    """Revisor de la rama, b3: la raiz escrita con `\\\\?\\` o con su nombre corto 8.3 no es
    «fuera del repo», y una entrada protegida escrita asi sigue negada con su motivo."""
    import ctypes

    largo = str(repo)
    casos = [(f"ffmpeg -i {V} {EXT} '\\\\?\\{largo}\\a.wav'", "R_FFMPEG")]
    corto = largo
    if sys.platform == "win32":  # para mypy en Linux, que no conoce `windll`
        buffer = ctypes.create_unicode_buffer(1024)
        ctypes.windll.kernel32.GetShortPathNameW(largo, buffer, 1024)
        corto = buffer.value or largo
    if corto.lower() != largo.lower():
        casos += [
            (f"ffmpeg -i {V} {EXT} '{corto}\\a.wav'", "R_FFMPEG"),
            (f"ffprobe -show_format '{corto}\\{MARZO}'", "R_SIN_ABRIR"),
        ]
    print(f"nombre corto de la raiz: {'sin 8.3 en este volumen' if len(casos) == 1 else corto}")
    for comando, esperado in casos:
        assert _regla(g, _decide(g, repo, comando)) == esperado, comando


def _guardia_de_main(tmp_path: Path) -> ModuleType:
    for ref in ("main", "origin/main"):
        proc = subprocess.run(
            ["git", "show", f"{ref}:.claude/hooks/guardia.py"],
            cwd=RAIZ,
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )
        if proc.returncode == 0:
            break
    else:
        pytest.skip("sin main ni origin/main en este clon")
    fichero = tmp_path / "guardia_de_main_ffmpeg.py"
    fichero.write_text(proc.stdout, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("guardia_de_main_ffmpeg", fichero)
    assert spec is not None and spec.loader is not None
    de_main = importlib.util.module_from_spec(spec)
    sys.modules["guardia_de_main_ffmpeg"] = de_main
    try:
        spec.loader.exec_module(de_main)
    finally:
        del sys.modules["guardia_de_main_ffmpeg"]
    return de_main


def test_la_matriz_frente_a_la_guardia_de_main(g: ModuleType, repo: Path, tmp_path: Path) -> None:
    """La misma matriz con la guardia de `main`: los casos que cambian de decision. Ninguno pasa a
    PASAR fuera de las cuatro formas permitidas; los que pasan a NEGARSE se declaran en el
    informe. Ya en `main`, las dos guardias son la misma y no cambia ninguno."""
    de_main = _guardia_de_main(tmp_path)
    rama, antes = _matriz(g, repo), _matriz(de_main, repo)
    permitidas = {n for n, _c in PERMITIDAS}
    abiertos: list[str] = []
    cerrados: list[str] = []
    for (nombre, r_rama), (_n, r_main) in zip(rama, antes, strict=True):
        if r_rama == r_main:
            continue
        print(f"| {nombre} | main {r_main} | rama {r_rama} |")  # la tabla del informe, con -s
        (abiertos if r_rama == "pasa" else cerrados).append(nombre)
    assert set(abiertos) <= permitidas
    assert not set(cerrados) & permitidas
