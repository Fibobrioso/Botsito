"""Esperar a la CI con una consulta repetida, en la guardia de Claude Code (`trabajo/guardia-ci`,
docs/validation/GUARDIA-CI.md): se niega una consulta de CI con una espera en el mismo comando,
`gh run watch` siempre y toda consulta desde codigo; la consulta suelta pasa. Y `Monitor` en el
matcher, y las herramientas que este repo no usa, en `permissions.deny` (respuestas del consultor
del 2026-10-23).

Todo se decide en memoria, con `decidir` sobre un repo de `tmp_path`: ningun comando se ejecuta y
ninguno consulta la CI. La guardia no lee este fichero cuando se le pasa a pytest (`guardia.py`,
`_analizar_pytest`: lo que esta bajo `tests/` es codigo revisado), asi que sus literales van
enteros; solo la ruta del material protegido se monta a trozos, por costumbre (respuesta del
consultor a la fase 0, punto 6).
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
AJUSTES = RAIZ / ".claude" / "settings.json"
MARZO = (
    "corp" + "us/Estrategia del trader/Material adicional de su operativa/Back" + "test marzo 2026"
) + "/v.mp4"

# Las herramientas que este repo no usa y que leerian un fichero local o una pagina `file://` fuera
# del matcher: se cierran por permisos (respuesta del consultor a la PARADA 2, puntos 0 y 1). Los
# nombres, EXACTOS, como los da la lista de herramientas de la sesion.
DENEGADAS = (
    "Artifact",
    "ArtifactData",
    "DesignSync",
    "mcp__claude-in-chrome__file_upload",
    "mcp__claude-in-chrome__navigate",
    "mcp__claude-in-chrome__get_page_text",
    "mcp__claude-in-chrome__read_page",
)

# Los guiones de espera del incidente (EA-CONEXION.md §13), copiados del scratchpad de aquella
# sesion al anexo de esta rama: el de Python lo lanzo la sesion; el de shell lo nego la guardia,
# pero por la asignacion `run=` y no por el bucle (GUARDIA-CI.md §0.a, N8c y N8d).
ANEXO = RAIZ / "docs" / "validation" / "anexos" / "GUARDIA-CI"
PY_INCIDENTE = (ANEXO / "esperar_run_original.py").read_text(encoding="utf-8")
SH_INCIDENTE = (ANEXO / "esperar_run_original.sh").read_text(encoding="utf-8")

RUN = "39893825671"
SHA = "2a99e64fa00d1ff4b0c45ee659614f1a21e2d110"
API = "https://api.github.com/repos/Fibobrioso/Botsito"
CR = f"{API}/commits/{SHA}/check-runs"
VER = f"gh run view {RUN}"
GREP = 'grep -o \'"status": *"[^"]*"\\|"conclusion": *"[^"]*"\''
PY_BUCLE = (
    'python -c "import subprocess, time\n'
    "while True:\n"
    f"    subprocess.run(['gh', 'run', 'view', '{RUN}'])\n"
    '    time.sleep(30)"'
)
PY_COMPRENSION = (
    f"python -c \"import subprocess,time; [(subprocess.run(['gh','run','view','{RUN}']), "
    'time.sleep(30)) for _ in range(20)]"'
)
PY_CURL = (
    'python -c "import subprocess,time\nwhile True:\n'
    f"    subprocess.run(['curl','-s','{CR}'])\n    time.sleep(30)\""
)
PY_UNA = f"python -c \"import subprocess; subprocess.run(['gh','run','view','{RUN}'])\""
PY_HEREDOC = f"python - <<'EOF'\nimport urllib.request\nurllib.request.urlopen('{CR}')\nEOF"
GH_WIN = '"C:\\Program Files\\GitHub CLI\\gh.exe"'
GH_BASH = '"/c/Program Files/GitHub CLI/GH.EXE"'
PS_FOR = f"for ($i = 0; $i -lt 20; $i++) {{ {VER}; Start-Sleep -Seconds 30 }}"
RITUAL_CI = f"curl -s --ssl-no-revoke {API}/commits/$(git rev-parse HEAD)/check-runs | {GREP}"
E = "R_ESPERA_CI"
X = "R_EJECUCION"
P = "pasa"


def _bucle(cuerpo: str) -> str:
    return f"while true; do {cuerpo}; sleep 30; done"


# (id, herramienta, comando, decision ANTES del cambio, decision DESPUES). Los ids N* y B1-B13 son
# los de la tabla de la fase 0 (GUARDIA-CI.md §0.a); R*, C*, D* y B14-B19, de la fase 1. `{FUERA}`
# es un directorio fuera del repo, como el scratchpad de una sesion.
TABLA: list[tuple[str, str, str, str, str]] = [
    # --- la fase 0: lo que tiene que negarse
    ("N1", "Bash", f"while true; do {VER} --json status; sleep 30; done", P, E),
    ("N2", "Bash", f"until {VER} --exit-status; do sleep 30; done", P, E),
    ("N3", "Bash", f"for i in 1 2 3; do {VER}; sleep 30; done", X, E),
    ("N3b", "Bash", f"for n in 1 2 3; do {VER}; sleep 30; done", P, E),
    ("N4", "Bash", f"{VER} && sleep 30 && {VER}", P, E),
    ("N5", "Bash", f"gh run watch {RUN}", P, E),
    ("N5b", "Bash", f"gh run watch {RUN} --exit-status", P, E),
    ("N6", "Bash", f"watch -n 30 {VER}", P, E),
    ("N7", "Bash", PY_BUCLE, P, E),
    ("N7b", "Bash", PY_COMPRENSION, P, E),
    ("N8c", "Bash", f'python "{{FUERA}}/esperar_run_original.py" {RUN}', P, E),
    ("N8b", "Bash", f'uv run python "{{FUERA}}/esperar_run_original.py" {RUN}', P, E),
    ("N8d", "Bash", f'sh "{{FUERA}}/esperar_run_original.sh" {RUN}', X, E),
    ("N9", "PowerShell", PS_FOR, X, E),
    ("N9b", "PowerShell", f"while ($true) {{ {VER}; Start-Sleep 30 }}", X, E),
    ("N9c", "PowerShell", f"{VER}; Start-Sleep 30; {VER}", X, E),
    ("N10", "Bash", _bucle(f"curl -s {CR} | {GREP}"), P, E),
    ("N11", "Bash", _bucle(f"gh api repos/Fibobrioso/Botsito/actions/runs/{RUN} --jq .s"), P, E),
    ("N12", "Bash", f"timeout 600 gh run watch {RUN}", P, E),
    ("N13", "Bash", f"{VER}; sleep 30; {VER}", P, E),
    ("N14", "Bash", "gh pr checks 12 --watch", P, E),
    ("N15", "Bash", f"sleep 300 && {VER} --json status,conclusion", P, E),
    ("N16", "Bash", f"sleep 300; {VER}", P, E),
    ("N17", "Bash", f"until curl -s {CR} | grep -q completed; do sleep 30; done", P, E),
    ("N18", "Bash", f"while sleep 30; do {VER}; done", P, E),
    ("N19", "Bash", PY_CURL, P, E),
    # --- las rutas nuevas (respuesta a la fase 0, punto 1)
    ("R1", "Bash", _bucle(f"curl -s {API}/actions/jobs/1"), P, E),
    ("R2", "Bash", _bucle(f"curl -s {API}/commits/{SHA}/status"), P, E),
    ("R3", "Bash", _bucle(f"gh api repos/x/y/commits/{SHA}/statuses"), P, E),
    ("R4", "Bash", _bucle(f"curl -s {API}/commits/{SHA}/check-suites"), P, E),
    # --- un guion o codigo con UNA consulta, sin bucle (respuesta a la fase 0, punto 3)
    ("C1", "Bash", 'python "{FUERA}/una_consulta.py"', P, E),
    ("C2", "Bash", 'sh "{FUERA}/una_consulta.sh"', P, E),
    ("C3", "Bash", f"bash -c '{VER}'", P, E),
    ("C4", "Bash", PY_UNA, P, E),
    ("C5", "Bash", PY_HEREDOC, P, E),
    # --- los disfraces de la fila de `trabajo/guardia-ffmpeg` en ERRORES-RECURRENTES.md: comillas
    # y escapes, un espacio final, otra forma de escribir lo mismo (la ruta del programa, un
    # `%XX`) y lo de antes y a la vez (`find -exec`, `cd -`, `| tee`, `&`, `1<>`)
    ("D1", "Bash", _bucle(f"$'gh' run view {RUN}"), P, E),
    ("D2", "Bash", _bucle(f"$'\\x67h' run view {RUN}"), X, E),
    ("D3", "Bash", _bucle(f'$"gh" run view {RUN}'), P, E),
    ("D4", "Bash", _bucle(f'"gh " run view {RUN}'), X, E),
    ("D5", "Bash", _bucle(f"{GH_WIN} run view {RUN}"), P, E),
    ("D6", "Bash", _bucle(f"{GH_BASH} run view {RUN}"), P, E),
    ("D7", "Bash", _bucle(f"curl -s {API}/commits/{SHA}/check%2Druns"), P, E),
    ("D8", "Bash", _bucle(f"find Makefile -maxdepth 0 -exec gh run view {RUN} \\;"), P, E),
    ("D9", "Bash", f"cd - && while true; do {VER}; sleep 30; done", X, E),
    ("D10", "Bash", f"{VER} | tee run.log; sleep 30; {VER} | tee -a run.log", P, E),
    ("D11", "Bash", f"{VER} & sleep 30", P, E),
    ("D12", "Bash", f"{VER} 1<>run.log; sleep 30", P, E),
    # y los del encargo: la consulta en una variable, un alias, una funcion, `xargs sh -c`, `$(...)`
    ("D13", "Bash", f'S="{VER}"; while true; do $S; sleep 30; done', X, E),
    ("D14", "Bash", f"alias c='{VER}'; while true; do c; sleep 30; done", X, E),
    ("D15", "Bash", f"f() {{ {VER}; sleep 30; f; }}; f", X, E),
    ("D16", "Bash", f"f() {{ {VER}; f; }}; f", X, E),
    ("D17", "Bash", f"seq 20 | xargs -I{{}} sh -c '{VER}; sleep 30'", X, E),
    ("D18", "Bash", _bucle(f"$(echo gh) run view {RUN}"), X, E),
    # --- lo que tiene que pasar
    ("B1", "Bash", f"{VER} --json status,conclusion,headSha", P, P),
    ("B2", "Bash", f"{VER} --log-failed", P, P),
    ("B3", "Bash", f"{VER} --exit-status", P, P),
    ("B4", "Bash", "gh run list --branch fix/x", P, P),
    ("B5", "Bash", f"gh run rerun {RUN}", P, P),
    ("B6", "Bash", "sleep 120", P, P),
    ("B7", "Bash", RITUAL_CI, P, P),
    ("B8", "Bash", f"curl -s {CR} | grep -E '\"(name|status|conclusion|html_url)\"'", P, P),
    ("B9", "Bash", "gh run list --branch fix/guardia-ci --limit 3", P, P),
    ("B10", "Bash", f"gh api repos/Fibobrioso/Botsito/actions/runs/{RUN} --jq .status", P, P),
    ("B11", "Bash", f"{VER} --log-failed | tail -50", P, P),
    ("B12", "Bash", f"{VER} --json jobs --jq '.jobs[].conclusion'", P, P),
    ("B13", "Bash", f"curl -s {CR}", P, P),
    ("B14", "Bash", f"timeout 60 {VER}", P, P),
    ("B15", "Bash", f"curl -s {API}/commits/{SHA}/status", P, P),
    ("B16", "Bash", "for n in a b; do echo $n; done", P, P),
    ("B17", "Bash", "until test -f listo; do sleep 1; done", P, P),
    ("B18", "Bash", 'python "{FUERA}/inocuo.py"', P, P),
    ("B19", "Bash", "wc -l Makefile", P, P),
]


@pytest.fixture(scope="module")
def g() -> ModuleType:
    nombre = "guardia_claude"  # el mismo que los otros tests de la guardia: un solo modulo
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
    # La cuarentena de la guardia lee las sesiones de aqui (`Politica.sesiones_en_cuarentena`).
    (r / "knowledge" / "corpus").mkdir(parents=True)
    (r / "knowledge" / "corpus" / "fuentes.yaml").write_text(
        "videos:\n  - video_id: v1\n    drive_id: abc\n", encoding="utf-8"
    )
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    (r / MARZO).parent.mkdir(parents=True)
    (r / MARZO).write_bytes(b"\x00" * 32)
    fuera = tmp_path / "scratchpad"
    fuera.mkdir()
    (fuera / "esperar_run_original.py").write_text(PY_INCIDENTE, encoding="utf-8")
    (fuera / "esperar_run_original.sh").write_text(SH_INCIDENTE, encoding="utf-8")
    (fuera / "una_consulta.py").write_text(
        "import subprocess\nsubprocess.run(['gh', 'run', 'view', '1'])\n", encoding="utf-8"
    )
    (fuera / "una_consulta.sh").write_text("#!/bin/sh\ngh run view 1\n", encoding="utf-8")
    (fuera / "inocuo.py").write_text("print('hola')\n", encoding="utf-8")
    return r


def _comando(plantilla: str, repo: Path) -> str:
    return plantilla.replace("{FUERA}", (repo.parent / "scratchpad").as_posix())


def _decide(
    g: ModuleType, repo: Path, entrada: dict[str, Any], herramienta: str = "Bash", **extra: str
) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(repo), **extra}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _regla(g: ModuleType, motivo: str | None) -> str:
    """`pasa`, o el nombre de la constante de regla que cita el motivo."""
    if motivo is None:
        return "pasa"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    assert len(nombres) == 1, motivo
    return str(nombres[0])


def _de_la_tabla(g: ModuleType, repo: Path, herramienta: str, comando: str) -> str:
    return _regla(g, _decide(g, repo, {"command": _comando(comando, repo)}, herramienta))


@pytest.mark.parametrize(("ident", "herramienta", "comando", "antes", "despues"), TABLA)
def test_la_tabla(
    g: ModuleType, repo: Path, ident: str, herramienta: str, comando: str, antes: str, despues: str
) -> None:
    """Cada forma con su decision, y la negada con el MOTIVO de esta regla: las que hoy niega otra
    regla (N3, N8d, N9...) tienen que negarse por esta, no por aquella."""
    motivo = _decide(g, repo, {"command": _comando(comando, repo)}, herramienta)
    print(f"{ident}\t{herramienta}\t{_regla(g, motivo)}")
    assert _regla(g, motivo) == despues, motivo
    if despues == E:
        assert g.COMO_ESPERAR_CI in str(motivo)


def test_el_mensaje_dice_que_hacer(g: ModuleType) -> None:
    """El texto del encargo: la consulta suelta y la espera sin consulta."""
    assert "una consulta suelta con `gh run view <run>`" in g.COMO_ESPERAR_CI
    assert "una espera sin consulta (`sleep` solo, o en segundo plano)" in g.COMO_ESPERAR_CI
    assert "despues otra consulta suelta" in g.COMO_ESPERAR_CI


def test_sin_la_regla_vuelve_lo_de_antes(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito: sin la condicion, cada forma vuelve a la decision de `main` (la columna
    `antes`, la de la fase 0): las que pasaban pasan, y las que negaba otra regla, con esa regla."""
    monkeypatch.setattr(g, "exigir_sin_espera_a_la_ci", lambda texto, ctx: None)
    monkeypatch.setattr(g, "_exigir_codigo_sin_ci", lambda codigo, es_python: None)
    monkeypatch.setattr(g, "_ESPERA_EN_POWERSHELL", re.compile(r"(?!)"))
    distintas = {}
    for ident, herramienta, comando, antes, _despues in TABLA:
        decision = _de_la_tabla(g, repo, herramienta, comando)
        print(f"sin la regla | {ident} | {decision}")
        if decision != antes:
            distintas[ident] = decision
    assert distintas == {}


def test_con_la_consulta_suelta_como_espera_las_buenas_se_niegan(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito en el otro sentido: si `gh` contara como una espera, la consulta suelta se
    negaria; las buenas que consultan son las que lo cazan."""
    monkeypatch.setattr(g, "PROGRAMAS_QUE_ESPERAN", g.PROGRAMAS_QUE_ESPERAN | {"gh"})
    for ident in ("B1", "B2", "B3", "B4", "B9", "B11", "B12", "B14"):
        _i, herramienta, comando, _a, _d = next(t for t in TABLA if t[0] == ident)
        decision = _de_la_tabla(g, repo, herramienta, comando)
        print(f"gh como espera | {ident} | {decision}")
        assert decision == E, ident


# --------------------------------------------- en codigo: mencion Y via de salida (PARADA 3)
TABLA_FASE0 = (ANEXO / "tabla_fase0.py").read_text(encoding="utf-8")
CARGA_ANEXO = 'RAIZ / ".claude" / "hooks" / "guardia.py"'
CARGA_REVISOR = (
    'python -c "import importlib.util, sys; '
    "spec = importlib.util.spec_from_file_location('g', '.claude/hooks/guardia.py'); "
    "g = importlib.util.module_from_spec(spec); sys.modules['g'] = g; spec.loader.exec_module(g); "
    "print(g.decidir({'tool_name': 'Bash', 'tool_input': {'command': 'gh run watch 1'}}, "
    'g.Politica(g.RAIZ)))"'
)


def _guion(repo: Path, nombre: str, texto: str) -> str:
    (repo.parent / "scratchpad" / nombre).write_text(texto, encoding="utf-8")
    return f'python "{(repo.parent / "scratchpad" / nombre).as_posix()}" .'


def test_el_guion_de_la_fase_0_pasa_y_sus_variantes_no(g: ModuleType, repo: Path) -> None:
    """Respuesta a la PARADA 3, punto 0, la excepcion en los dos sentidos: `tabla_fase0.py` carga
    la guardia por su ruta y solo lleva `gh` como dato, y pasa; con `import subprocess`, con
    `importlib` sobre otra ruta o con la ruta de la guardia montada a trozos, se niega."""
    assert CARGA_ANEXO in TABLA_FASE0
    casos = {
        "tal cual": (TABLA_FASE0, P),
        "con subprocess": ("import subprocess\n" + TABLA_FASE0, E),
        "otra ruta": (TABLA_FASE0.replace(CARGA_ANEXO, 'RAIZ / "otro" / "modulo.py"'), E),
        "a trozos": (
            TABLA_FASE0.replace(CARGA_ANEXO, 'RAIZ / ".claude" / "hooks" / ("guar" + "dia.py")'),
            E,
        ),
        "literal a trozos": (
            TABLA_FASE0.replace(CARGA_ANEXO, '".claude/hooks/" + "guardia.py"'),
            E,
        ),
        "literal": (TABLA_FASE0.replace(CARGA_ANEXO, '".claude/hooks/guardia.py"'), P),
    }
    for nombre, (texto, esperado) in casos.items():
        decision = _de_la_tabla(g, repo, "Bash", _guion(repo, "t.py", texto))
        print(f"tabla_fase0 | {nombre} | {decision}")
        assert decision == esperado, nombre


@pytest.mark.parametrize(
    ("comando", "esperado"),
    [
        (CARGA_REVISOR, P),  # la forma del revisor (punto 1)
        ("python -c \"print('gh run view 1')\"", P),  # la mencion sola es un dato
        ("python -c \"print('" + CR + "')\"", P),
        ("python -c \"__import__('subprocess'); print('gh run view 1')\"", E),
        ("python -c \"exec('x = 1'); print('gh run view 1')\"", E),
        ("python -c \"eval('1'); print('gh run view 1')\"", E),
        ("python -c \"compile('1', 'x', 'eval'); print('gh run view 1')\"", E),
        ("python -c \"import runpy; print('gh run view 1')\"", E),
        ("python -c \"import importlib; importlib.import_module('os'); print('gh run')\"", E),
        ("python -c \"from importlib import import_module; print('gh run view 1')\"", E),
        ("python -c \"import os; os.system('gh run view 1')\"", E),
        ("python -c \"import requests; requests.get('" + CR + "')\"", E),
        ("python -c \"import socket; print('gh run view 1')\"", E),
        ("python -c \"import re; re.compile('x'); print('gh run view 1')\"", P),
    ],
)
def test_en_codigo_la_mencion_cuenta_con_una_via_de_salida(
    g: ModuleType, repo: Path, comando: str, esperado: str
) -> None:
    """Respuesta a la PARADA 3, punto 0: en codigo cuenta la mencion de la CI con una via de salir
    del proceso, o con algo que no deja decidir que se importa (`__import__`, `importlib`, `exec`,
    `eval`, `compile`, `runpy`); `re.compile` no es el `compile` de Python."""
    assert _de_la_tabla(g, repo, "Bash", comando) == esperado


def test_riesgo_residual_la_mencion_a_trozos_no_se_ve(g: ModuleType, repo: Path) -> None:
    """RIESGO RESIDUAL DECLARADO (respuesta a la PARADA 3, punto 0; GUARDIA-CI.md y la linea de
    Technical Debt del cierre): con una via de salida, `"g" + "h"` esconde la mencion y pasa;
    `analizar_codigo` solo mira rutas compuestas con literales del material, no esto. Si un dia
    se cierra, este test cambia de sentido."""
    comando = "python -c \"import subprocess; subprocess.run(['g' + 'h', 'run', 'view', '1'])\""
    assert _de_la_tabla(g, repo, "Bash", comando) == P


def test_sin_la_excepcion_el_guion_de_la_fase_0_se_niega(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito en los dos sentidos: sin la excepcion, `tabla_fase0.py` se niega; con una
    excepcion que aceptara cualquier ruta, el guion con `importlib` sobre otra ruta pasaria."""
    otra = TABLA_FASE0.replace(CARGA_ANEXO, 'RAIZ / "otro" / "modulo.py"')
    monkeypatch.setattr(g, "_carga_solo_la_guardia", lambda codigo: False)
    assert _de_la_tabla(g, repo, "Bash", _guion(repo, "t.py", TABLA_FASE0)) == E
    monkeypatch.undo()
    monkeypatch.setattr(g, "_es_ruta_de_la_guardia", lambda nodo, asignaciones: True)
    assert _de_la_tabla(g, repo, "Bash", _guion(repo, "t.py", otra)) == P


# ------------------------------------------------------------------------------------- Monitor
def test_monitor_se_decide_como_bash(g: ModuleType, repo: Path) -> None:
    """Respuesta a la fase 0, punto 0: un Monitor que espera a la CI se niega, uno que lee material
    protegido se niega, y uno inocuo (esperar a que exista un fichero sin leerlo) pasa."""
    base = {"description": "x", "timeout_ms": 60000}
    espera = {"command": f"while true; do {VER}; sleep 30; done", **base}
    assert _regla(g, _decide(g, repo, espera, "Monitor")) == E
    lee = {"command": f'cat "{MARZO}"', **base}
    assert _regla(g, _decide(g, repo, lee, "Monitor")) == "R_SIN_ABRIR"
    inocuo = {"command": "until test -f listo; do sleep 1; done; echo listo", **base}
    assert _decide(g, repo, inocuo, "Monitor") is None


@pytest.mark.parametrize(
    "entrada",
    [
        {"ws": {"url": "wss://x"}, "description": "x", "timeout_ms": 1000},
        {"description": "x", "timeout_ms": 1000},
        {"command": ["ls"], "description": "x", "timeout_ms": 1000},
        {"command": "ls", "description": "x", "timeout_ms": 1000, "otra": 1},
    ],
)
def test_monitor_con_una_entrada_que_no_se_reconoce_se_niega(
    g: ModuleType, repo: Path, entrada: dict[str, Any]
) -> None:
    assert _regla(g, _decide(g, repo, entrada, "Monitor")) == "R_MONITOR"


def test_sin_monitor_en_decidir_el_que_lee_pasaria(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Roto a proposito: sin Monitor entre las herramientas de comando de `decidir`, el Monitor que
    lee material protegido pasa, porque la guardia no lo mira."""
    monkeypatch.setattr(g, "HERRAMIENTAS_DE_COMANDO", frozenset({"Bash", "PowerShell"}))
    lee = {"command": f'cat "{MARZO}"', "description": "x", "timeout_ms": 60000}
    assert _decide(g, repo, lee, "Monitor") is None


# ---------------------------------------------------------------------- los subagentes (punto 8)
def test_un_subagente_se_decide_igual(g: ModuleType, repo: Path) -> None:
    """Respuesta a la fase 0, punto 8: la guardia no mira quien llama. Un evento con los campos de
    un subagente (`agent_id`, `agent_type`) se decide igual que el de la sesion. Que Claude Code
    llama al hook del proyecto para los subagentes se probo de verdad (GUARDIA-CI.md §1)."""
    entrada = {"command": f"while true; do {VER}; sleep 30; done"}
    assert _regla(g, _decide(g, repo, entrada)) == E
    assert _regla(g, _decide(g, repo, entrada, agent_id="a1", agent_type="revisor")) == E


# ---------------------------------------------------------------------------- .claude/settings.json
def _faltan_en_deny(ajustes: dict[str, Any]) -> list[str]:
    deny = ajustes.get("permissions", {}).get("deny", [])
    return [n for n in DENEGADAS if n not in deny]


def test_las_herramientas_que_el_repo_no_usa_estan_denegadas() -> None:
    """Respuesta a la PARADA 2, puntos 0 y 1: cada nombre, exacto, en `permissions.deny`; y
    `Monitor` en el matcher de la guardia (respuesta a la fase 0, punto 0)."""
    ajustes = json.loads(AJUSTES.read_text(encoding="utf-8"))
    assert _faltan_en_deny(ajustes) == []
    assert "Monitor" in ajustes["hooks"]["PreToolUse"][0]["matcher"].split("|")


def test_si_falta_un_nombre_o_esta_mal_escrito_se_ve() -> None:
    """Roto a proposito en los dos sentidos: quitar un nombre de `deny` lo caza, y escribirlo mal
    (`claude_in_chrome` en vez de `claude-in-chrome`) tambien; con todos, no caza nada."""
    ajustes = json.loads(AJUSTES.read_text(encoding="utf-8"))
    assert _faltan_en_deny(ajustes) == []
    for nombre in DENEGADAS:
        sin = json.loads(json.dumps(ajustes))
        sin["permissions"]["deny"].remove(nombre)
        assert _faltan_en_deny(sin) == [nombre]
        if "-" in nombre:
            mal = json.loads(json.dumps(ajustes))
            mal["permissions"]["deny"] = [
                x.replace("-", "_") if x == nombre else x for x in mal["permissions"]["deny"]
            ]
            assert _faltan_en_deny(mal) == [nombre]
