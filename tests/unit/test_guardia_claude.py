"""La guardia de Claude Code (`.claude/hooks/guardia.py`, rama `trabajo/guardias-claude`).

Casi todo sobre un repo SINTETICO con la forma del real -particiones, fuentes, corpus, data-, para
que ningun test dependa del material que solo esta en la maquina del consultor. Los ficheros
"protegidos" del repo sintetico son de mentira: la guardia decide por la ruta y por los repartos,
no por el contenido (salvo el feedback, que se crea aqui). Y tres comprobaciones contra el repo
REAL: que la guardia ve los mismos reservados que `casos_reservados`, las mismas sesiones en
cuarentena y los mismos meses de desarrollo, y que el ritual y los runbooks pasan.
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

from botsito.cases.holdout import RESERVADAS, casos_reservados

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
AJUSTES = RAIZ / ".claude" / "settings.json"
MATERIAL = "corpus/Estrategia del trader/Material adicional de su operativa"


@pytest.fixture(scope="module")
def g() -> ModuleType:
    nombre = "guardia_claude"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, GUARDIA)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _escribir(raiz: Path, rel: str, texto: str = "x\n") -> Path:
    ruta = raiz / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def _git(repo: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    _escribir(
        r,
        "knowledge/cases/kit/2026-09-09-sesion-01/particiones.yaml",
        "asignacion:\n  caso-eurusd-2026-05-04: holdout-1\n  caso-eurusd-2026-05-06: dev\n"
        "cupos:\n  dev: 1\n",
    )
    _escribir(
        r,
        "knowledge/cases/fidelidad/eurusd-2026-09/particiones.yaml",
        "artefacto: eurusd-2026-09\nasignacion:\n  caso-eurusd-2026-09-01: fidelidad-dev\n"
        "  caso-eurusd-2026-09-02: fidelidad-1\nseed: 1\n",
    )
    _escribir(
        r,
        "knowledge/corpus/fuentes.yaml",
        "videos:\n  - video_id: v1\n    drive_id: abc\n  - video_id: v6\n    drive_id: null\n"
        "  - video_id: v7\n    drive_id: null  # sesion\n  - video_id: v9\n    drive_id: null\n"
        "carpetas:\n  - ruta: Sesiones\n",
    )
    for rel in (
        f"{MATERIAL}/backtesting-analytics ABRIL 2026.xlsx",
        f"{MATERIAL}/backtesting-analytics ENERO 2026.xlsx",
        f"{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx",
        f"{MATERIAL}/Backtest marzo 2026/asdasd.jpeg",
        f"{MATERIAL}/Backtest mayo 2026/backtesting-analytics MAYO 2026.xlsx",
        f"{MATERIAL}/WhatsApp Image 2026-09-03 at 5.55.36 PM.jpeg",
        f"{MATERIAL}/Mensajes del trader/mensaje.txt",
        "corpus/Estrategia del trader/Sesiones/s1/hoja RELLENADA.docx",
        "corpus/Estrategia del trader/_procesado/transcripciones/v1.txt",
        "data/transcripciones/v7/large-v3/cruda.jsonl",
        "data/transcripciones/v6/large-v3/cruda.jsonl",
        "data/transcripciones/v1/large-v3/cruda.txt",
        "data/fotogramas/v4/png-1fps/004800000.png",
        "data/ohlc/m1.parquet",
        "data/visor/caso-eurusd-2026-09-02.html",
        "data/visor/caso-eurusd-2026-04-01.html",
        "knowledge/cases/holdout/README.md",
        "knowledge/cases/holdout/1/README.md",
        "knowledge/cases/dev/caso-eurusd-2026-04-01.yaml",
        "knowledge/feedback/README.md",
        "knowledge/spec/strategy_spec.yaml",
        "src/botsito/x.py",
        "docs/a.md",
        "scripts/huso_por_velas.py",
        "scripts/otro.py",
        ".gitignore",
    ):
        _escribir(r, rel)
    (r / ".gitignore").write_text("/corpus/\n/data/*\n", encoding="utf-8")
    _escribir(
        r,
        "knowledge/corpus/tramos_no_citables.yaml",
        'tramos:\n  - video_id: v6\n    t0: "0:41:00"\n    t1: "0:50:11"\n    motivo: x\n'
        '  - video_id: v6\n    t0: "1:53:30"\n    t1: "1:57:31"\n'
        '  - video_id: v7\n    t0: "0:15:34"\n    t1: "0:15:48"\n',
    )
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    return r


def _decide(g: ModuleType, repo: Path, herramienta: str, **entrada: Any) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(repo)}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _bash(g: ModuleType, repo: Path, comando: str) -> str | None:
    return _decide(g, repo, "Bash", command=comando)


# ------------------------------------------------------------------- lo que la politica ve
def test_la_politica_lee_los_repartos_las_sesiones_y_los_meses(g: ModuleType, repo: Path) -> None:
    p = g.Politica(repo)
    assert p.reservados == {
        "caso-eurusd-2026-05-04": "holdout-1",
        "caso-eurusd-2026-09-02": "fidelidad-1",
    }
    assert p.sesiones_en_cuarentena == {"v7", "v9"}  # v6 queda fuera: leida antes, dia retirado
    assert p.meses_legibles == {"2026-01", "2026-04", "2026-08"}


def test_contra_el_repo_real_ve_lo_mismo_que_el_codigo(g: ModuleType) -> None:
    p = g.Politica(RAIZ)
    assert p.reservados == casos_reservados(RAIZ)
    assert set(g.PARTICIONES_RESERVADAS) == set(RESERVADAS)
    assert p.sesiones_en_cuarentena == {"v7", "v8", "v9"}
    assert p.meses_legibles == {"2026-01", "2026-04", "2026-08"}
    assert p.meses_reservados >= {"2026-05", "2026-09"}


def test_un_mes_de_desarrollo_con_un_dia_reservado_deja_de_ser_legible(
    g: ModuleType, repo: Path
) -> None:
    _escribir(
        repo,
        "knowledge/cases/visto/2026-04/particiones.yaml",
        "asignacion:\n  caso-eurusd-2026-04-07: holdout-2\n",
    )
    libro = f"{MATERIAL}/backtesting-analytics ABRIL 2026.xlsx"
    assert _decide(g, repo, "Read", file_path=str(repo / libro)) is not None


# ------------------------------------------------------------ Fase 4: lo que pide el encargo
@pytest.mark.parametrize(
    "rel",
    [
        f"{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx",
        f"{MATERIAL}/Backtest marzo 2026/asdasd.jpeg",
        f"{MATERIAL}/Backtest mayo 2026/backtesting-analytics MAYO 2026.xlsx",
        f"{MATERIAL}/WhatsApp Image 2026-09-03 at 5.55.36 PM.jpeg",
        "corpus/Estrategia del trader/Sesiones/s1/hoja RELLENADA.docx",
        "data/transcripciones/v7/large-v3/cruda.jsonl",
        "data/visor/caso-eurusd-2026-09-02.html",
        "knowledge/cases/holdout/1/etiquetas.yaml",
    ],
)
def test_bloquea_leer_material_reservado(g: ModuleType, repo: Path, rel: str) -> None:
    motivo = _decide(g, repo, "Read", file_path=str(repo / rel))
    assert motivo is not None and "CLAUDE.md" in motivo, motivo
    assert _bash(g, repo, f'cat "{rel}"') is not None
    assert _bash(g, repo, f'head -c 100 "{repo / rel}"') is not None


@pytest.mark.parametrize(
    "comando",
    [
        f'sha256sum "{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx"',
        f'stat "{MATERIAL}/Backtest marzo 2026/asdasd.jpeg"',
        f'ls -la "{MATERIAL}/Backtest marzo 2026"',
        f'du -sh "{MATERIAL}"',
        f'wc -c "{MATERIAL}/Backtest mayo 2026/backtesting-analytics MAYO 2026.xlsx"',
        f'certutil -hashfile "{MATERIAL}/Backtest marzo 2026/asdasd.jpeg" SHA256',
        f'find "{MATERIAL}" -name "*.xlsx" -exec sha256sum {{}} +',
        "uv run botsito corpus inventory",
        "git check-ignore -v data/transcripciones/v7/large-v3/cruda.jsonl",
    ],
)
def test_deja_pasar_stat_tamano_y_sha256(g: ModuleType, repo: Path, comando: str) -> None:
    assert _bash(g, repo, comando) is None


@pytest.mark.parametrize(
    "comando",
    [
        'cat "$(find corpus -name "*.xlsx" | head -1)"',
        "cat $FICHERO",
        'F="data/transcripciones/v7/large-v3/cruda.jsonl"; head "$F"',
        "find corpus -name '*.xlsx' | xargs cat",
        'eval "cat corpus/x"',
        'while read f; do cat "$f"; done < lista.txt',
        "python -c \"import os; [open(os.path.join(r, f)).read() for r, _, fs in os.walk('corpus') "
        'for f in fs]"',
    ],
)
def test_bloquea_un_bash_indecidible(g: ModuleType, repo: Path, comando: str) -> None:
    motivo = _bash(g, repo, comando)
    assert motivo is not None, comando
    assert "Como reescribirlo" in motivo or "Regla:" in motivo


def test_lo_indecidible_que_no_puede_leer_nada_pasa(g: ModuleType, repo: Path) -> None:
    """`$(...)` y variables en comandos que no leen contenido no son lecturas."""
    for comando in (
        'echo "$HOME" && git log -1 --format=%H',
        'git commit -m "$(printf x)"',
        'for f in docs/*.md; do wc -l "$f"; done',
        'cd src && grep -rn "def " botsito',
    ):
        assert _bash(g, repo, comando) is None, comando


@pytest.mark.parametrize(
    ("rel", "regla"),
    [
        (f"{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx", "R_SIN_ABRIR"),
        (f"{MATERIAL}/Backtest marzo 2026/aaaaa.jpeg", "R_CAPTURA"),
        (f"{MATERIAL}/Backtest mayo 2026/backtesting-analytics MAYO 2026.xlsx", "R_LIBRO"),
        (
            f"{MATERIAL}/Backtest septiembre 2026/backtesting-analytics SEPTIEMBRE 2026.xlsx",
            "R_LIBRO",
        ),
        ("data/transcripciones/v9/large-v3-int8-float16/cruda.txt", "R_CUARENTENA"),
        ("knowledge/cases/holdout/1/etiquetas.yaml", "R_HOLDOUT"),
    ],
)
def test_cada_bloqueo_cita_su_regla_en_el_repo_real(g: ModuleType, rel: str, regla: str) -> None:
    """Por la ruta, sin abrir nada: vale tambien en la CI, donde no hay corpus."""
    motivo = g.Politica(RAIZ).motivo_fichero(str(RAIZ / rel))
    assert motivo == getattr(g, regla)
    assert motivo.startswith("CLAUDE.md")


def test_pytest_sobre_codigo_suelto_se_lee_como_un_guion(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    suelto = tmp_path / "test_suelto.py"
    marzo = repo / MATERIAL / "Backtest marzo 2026" / "backtesting-analytics MARZO 2026.xlsx"
    suelto.write_text(f"def test_x():\n    open(r'{marzo}', 'rb').read()\n", encoding="utf-8")
    assert _bash(g, repo, f'uv run pytest "{suelto}" -q') is not None
    assert _bash(g, repo, f'python -m pytest "{suelto}"') is not None
    assert _bash(g, repo, "uv run pytest tests/unit -q") is None


# ------------------------------------------------------------------ las rutas que si se leen
@pytest.mark.parametrize(
    "rel",
    [
        f"{MATERIAL}/backtesting-analytics ABRIL 2026.xlsx",
        f"{MATERIAL}/backtesting-analytics ENERO 2026.xlsx",
        f"{MATERIAL}/Mensajes del trader/mensaje.txt",
        "data/transcripciones/v1/large-v3/cruda.txt",
        "data/fotogramas/v4/png-1fps/004800000.png",
        "data/visor/caso-eurusd-2026-04-01.html",
        "knowledge/cases/holdout/1/README.md",
        "knowledge/cases/dev/caso-eurusd-2026-04-01.yaml",
        "corpus/Estrategia del trader/_procesado/transcripciones/v1.txt",
    ],
)
def test_lo_que_se_lee_sin_puerta_pasa(g: ModuleType, repo: Path, rel: str) -> None:
    assert _decide(g, repo, "Read", file_path=str(repo / rel)) is None
    assert _bash(g, repo, f'cat "{rel}"') is None


def test_una_cruda_no_leer_fuera_del_repo_y_un_libro_por_su_nombre(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    fuera = tmp_path / "reunion" / "sesion.cruda-NO-LEER.txt"
    assert _decide(g, repo, "Read", file_path=str(fuera)) is not None
    copia = tmp_path / "para-revisar" / "backtesting-analytics MARZO 2026.xlsx"
    assert _decide(g, repo, "Read", file_path=str(copia)) is not None
    assert _bash(g, repo, f"cp '{copia}' /tmp/x.xlsx") is not None


def test_el_feedback_que_etiqueta_un_caso_reservado(g: ModuleType, repo: Path) -> None:
    fb = _escribir(
        repo,
        "knowledge/feedback/s1/fb-1.yaml",
        "accion: LABEL_CASE\nobjetivo:\n  id: caso-eurusd-2026-05-04\n",
    )
    otro = _escribir(repo, "knowledge/feedback/s1/fb-2.yaml", "accion: CONFIRM\n")
    assert _decide(g, repo, "Read", file_path=str(fb)) is not None
    assert _decide(g, repo, "Read", file_path=str(otro)) is None
    assert _decide(g, repo, "Grep", pattern="x", path=str(repo / "knowledge")) is not None


# --------------------------------------------------------------------------- Grep y Glob
def test_grep_desde_la_raiz_respeta_lo_ignorado_y_dentro_no(g: ModuleType, repo: Path) -> None:
    """Medido el 2026-10-01: el Grep de Claude Code no entra en `data/` desde la raiz, pero si
    busca dentro de una carpeta ignorada cuando se le da su ruta."""
    assert _decide(g, repo, "Grep", pattern="x") is None
    assert _decide(g, repo, "Grep", pattern="x", path=str(repo / "src")) is None
    assert (
        _decide(g, repo, "Grep", pattern="x", path=str(repo / "data/transcripciones")) is not None
    )
    assert _decide(g, repo, "Grep", pattern="x", path=str(repo / "data/fotogramas")) is None
    assert _decide(g, repo, "Grep", pattern="x", path=str(repo / MATERIAL)) is not None
    _escribir(repo, "knowledge/cases/holdout/2/etiquetas.yaml")
    assert _decide(g, repo, "Grep", pattern="x") is not None  # ya hay etiquetas seguidas


def test_glob_solo_lista_nombres_y_pasa(g: ModuleType, repo: Path) -> None:
    assert _decide(g, repo, "Glob", pattern="**/*.xlsx", path=str(repo / "corpus")) is None


def test_grep_recursivo_en_bash(g: ModuleType, repo: Path) -> None:
    assert _bash(g, repo, "grep -rn septiembre .") is not None
    assert _bash(g, repo, "grep -rn septiembre data") is not None
    assert _bash(g, repo, "rg septiembre") is None  # rg respeta .gitignore
    assert _bash(g, repo, "rg -uu septiembre") is not None
    assert _bash(g, repo, "grep -rn septiembre docs src") is None


# ------------------------------------------------------------------------ la CLI del proyecto
@pytest.mark.parametrize(
    ("comando", "bloquea"),
    [
        ("uv run botsito corpus frames show --video v9 --t 0:15:29", True),
        ("uv run botsito corpus transcript show --video v7 --desde 0:01:00", True),
        ("uv run botsito kb at --video=v7 --t 0:10:00", True),
        ("uv run botsito kb find stop", True),
        ("uv run botsito kb find stop --video v3", False),
        ("uv run botsito corpus frames show --video v4 --t 1:06:12", False),
        ("uv run botsito motor arnes --salida arnes.txt", False),
        ("uv run botsito casos ingerir --material x.xlsx --fecha 2026-10-01", False),
    ],
)
def test_la_cli_pasa_salvo_lo_que_imprime_una_cruda(
    g: ModuleType, repo: Path, comando: str, bloquea: bool
) -> None:
    assert (_bash(g, repo, comando) is not None) is bloquea, comando


def test_git_con_menos_c_resuelve_las_rutas_desde_su_directorio(g: ModuleType, repo: Path) -> None:
    """Hallazgo A2 del revisor: `-C` cambia la base de las rutas de los argumentos."""
    _escribir(repo, "knowledge/cases/holdout/1/etiquetas.yaml")
    for comando in (
        "git show HEAD:knowledge/cases/holdout/1/etiquetas.yaml",
        "git -C knowledge/cases show HEAD:./holdout/1/etiquetas.yaml",
        "git -C knowledge/cases/holdout/1 diff -- etiquetas.yaml",
        "git -C knowledge/cases log -p -- holdout",
    ):
        assert _bash(g, repo, comando) is not None, comando
    assert _bash(g, repo, "git -C src log --oneline -- botsito") is None


def test_core_hookspath_es_saltarse_los_hooks(g: ModuleType, repo: Path) -> None:
    """Hallazgo A1 del revisor: cambiar `core.hooksPath` equivale a `--no-verify`."""
    for comando in (
        "git -c core.hooksPath=/dev/null commit -m x",
        "git config core.hooksPath /dev/null",
        "git config --local core.hooksPath .vacio",
        "git config --unset core.hooksPath",
    ):
        motivo = _bash(g, repo, comando)
        assert motivo is not None and "--no-verify" in motivo, comando
    assert _bash(g, repo, "git config core.hooksPath") is None  # leerlo no lo cambia
    motivo = _decide(g, repo, "PowerShell", command="git config core.hooksPath NUL")
    assert motivo is not None


def _segmentos_v6(repo: Path) -> Path:
    """Cinco segmentos: el tercero dentro del tramo 0:41:00-0:50:11, los demas fuera."""
    tiempos = [
        (0, 1000),
        (600000, 610000),
        (2470000, 2480000),
        (3100000, 3110000),
        (3200000, 3201000),
    ]
    lineas = [
        json.dumps({"n": i, "t0_ms": a, "t1_ms": b, "texto": "x"})
        for i, (a, b) in enumerate(tiempos)
    ]
    return _escribir(repo, "data/transcripciones/v6/large-v3/cruda.jsonl", "\n".join(lineas) + "\n")


def test_v6_se_lee_salvo_sus_tramos_no_citables(g: ModuleType, repo: Path) -> None:
    """Decision del consultor del 2026-10-01: la exencion de v6 se mantiene solo con sus tramos
    bloqueados."""
    cruda = _segmentos_v6(repo)
    txt = _escribir(
        repo,
        "data/transcripciones/v6/large-v3/cruda.txt",
        "[0:00:00.000] a\n[0:10:00.000] a2\n[0:40:00.000] b\n[0:45:00.000] c\n[0:51:00.000] d\n",
    )
    # Se bloquea tambien la linea vecina de un tramo (margen de una linea, por prudencia), y la
    # ultima, que no tiene fin conocido.
    assert _decide(g, repo, "Read", file_path=str(cruda)) is not None  # entero: toca el tramo
    assert _decide(g, repo, "Read", file_path=str(cruda), offset=1, limit=1) is None
    assert _decide(g, repo, "Read", file_path=str(cruda), offset=5, limit=1) is None
    motivo = _decide(g, repo, "Read", file_path=str(cruda), offset=2, limit=2)
    assert motivo is not None and "Lineas en tramo no citable: 3" in motivo
    assert _decide(g, repo, "Read", file_path=str(txt), offset=1, limit=1) is None
    assert _decide(g, repo, "Read", file_path=str(txt), offset=3, limit=1) is not None  # 0:40-0:45
    assert _bash(g, repo, f'cat "{cruda}"') is not None
    assert _bash(g, repo, f'grep -n stop "{cruda}"') is not None
    assert _bash(g, repo, f'sha256sum "{cruda}"') is None


@pytest.mark.parametrize(
    ("comando", "bloquea"),
    [
        ("uv run botsito corpus frames show --video v6 --t 0:45:00", True),
        ("uv run botsito corpus frames show --video v6 --t 0:30:00", False),
        ("uv run botsito kb at --video v6 --t 1:55:00 --contexto", True),
        ("uv run botsito kb at --video v6 --t 1:58:00", False),
        ("uv run botsito corpus transcript show --video v6 --t0 0:40:00 --t1 0:42:00", True),
        ("uv run botsito corpus transcript show --video v6 --t0 0:10:00 --t1 0:20:00", False),
        ("uv run botsito kb find stop --video v6", True),
        ("uv run botsito kb find stop --video v6 --desde 0:00:00 --hasta 0:30:00", False),
        ("uv run botsito kb find stop --video v6 --desde 0:30:00 --hasta 1:00:00", True),
    ],
)
def test_la_cli_no_imprime_un_tramo_de_v6(
    g: ModuleType, repo: Path, comando: str, bloquea: bool
) -> None:
    assert (_bash(g, repo, comando) is not None) is bloquea, comando


def test_una_propuesta_con_segmentos_de_un_tramo(g: ModuleType, repo: Path) -> None:
    dentro = _escribir(
        repo,
        "knowledge/_proposals/pr-v6-004900-005100-aaaa.yaml",
        "contexto:\n  segmentos:\n  - n: 1\n    t0_ms: 2998843\n    t1_ms: 3001023\n",
    )
    fuera = _escribir(
        repo,
        "knowledge/_proposals/pr-v6-001000-001100-bbbb.yaml",
        "contexto:\n  segmentos:\n  - n: 1\n    t0_ms: 600000\n    t1_ms: 601000\n",
    )
    assert _decide(g, repo, "Read", file_path=str(dentro)) is not None
    assert _decide(g, repo, "Read", file_path=str(fuera)) is None
    assert (
        _decide(g, repo, "Grep", pattern="x", path=str(repo / "knowledge/_proposals")) is not None
    )
    assert _decide(g, repo, "Grep", pattern="x") is None  # limite declarado (§1.7)


def test_los_tramos_del_repo_real(g: ModuleType) -> None:
    """v7 y v9 tienen tramos, pero su cruda ya no se lee entera: solo se vigilan los de v6."""
    assert g.Politica(RAIZ).tramos_vigilados == {
        "v6": [(2_460_000, 3_011_000), (6_810_000, 7_051_000)]
    }


def test_solo_el_guion_de_main_es_codigo_revisado(g: ModuleType, repo: Path) -> None:
    """Decision del consultor del 2026-10-01: un guion nuevo o cambiado en la rama en curso pasa
    por el hook como cualquier otro comando, aunque este commiteado."""
    marzo = f"{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx"
    _escribir(repo, "scripts/nuevo.py", f"print(open(r'{repo / marzo}', 'rb').read())\n")
    _git(repo, "add", "-A")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "nuevo")
    motivo = _bash(g, repo, "uv run python scripts/nuevo.py")
    assert motivo is not None and "MARZO" in motivo.upper()
    assert _bash(g, repo, f'uv run python scripts/huso_por_velas.py --libro "{marzo}"') is None
    _escribir(repo, "scripts/huso_por_velas.py", "print('cambiado en la rama')\n")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-am", "cambia")
    assert _bash(g, repo, f'uv run python scripts/huso_por_velas.py --libro "{marzo}"') is not None


def test_un_guion_seguido_es_codigo_revisado_y_uno_nuevo_se_lee(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    marzo = f"{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx"
    assert _bash(g, repo, f'uv run python scripts/huso_por_velas.py --libro "{marzo}"') is None
    assert _bash(g, repo, f'uv run python scripts/otro.py "{marzo}"') is not None
    nuevo = tmp_path / "scratch.py"
    nuevo.write_text(f"print(open(r'{repo / marzo}', 'rb').read())\n", encoding="utf-8")
    assert _bash(g, repo, f'python "{nuevo}"') is not None
    inocuo = tmp_path / "inocuo.py"
    inocuo.write_text("print(open('docs/a.md').read())\n", encoding="utf-8")
    assert _bash(g, repo, f'python "{inocuo}"') is None


# --------------------------------------------------------------- las operaciones prohibidas
@pytest.mark.parametrize(
    "comando",
    [
        'git commit --no-verify -m "x"',
        'git commit -nm "x"',
        "git merge --no-verify trabajo/x",
        "git push --no-verify origin trabajo/x",
        "git push --force origin trabajo/x",
        "git push origin trabajo/x -f",
        "git push --force-with-lease origin trabajo/x",
        "git push origin +trabajo/x",
        "git -C . push --force",
        "git tag -d stable/F36h-be-al-tick",
        "git tag -f stable/F36h-be-al-tick HEAD",
        "git push origin --delete stable/F36h-be-al-tick",
        "git push origin :refs/tags/stable/F36h-be-al-tick",
        "git cherry-pick abc123",
        "git rebase main",
        "git branch -D trabajo/x",
        "rm -rf data/fotogramas",
        "rm -fr corpus",
        "rm -rf ./knowledge/evidence",
        "make check",
        "make check > /dev/null 2>&1",
        "make check 2>&1 | tail -5",
        "cat > f.py <<EOF\nimport re\nre.compile(r'\\bhola')\nEOF\n",
        "git checkout main && git add -A",
        "git checkout main && git commit -am x",
        "git checkout main && git revert HEAD",
    ],
)
def test_las_operaciones_prohibidas(g: ModuleType, repo: Path, comando: str) -> None:
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, comando


def test_en_una_rama_de_trabajo_add_a_y_un_heredoc_con_comillas_pasan(
    g: ModuleType, repo: Path
) -> None:
    assert _bash(g, repo, "git add -A") is None
    assert _bash(g, repo, "cat > f.py <<'EOF'\nre.compile(r'\\bhola')\nEOF\n") is None
    assert _bash(g, repo, "git rebase --abort") is None
    assert _bash(g, repo, "rm -rf .pytest_cache build") is None


# ---------------------------------------------------- el ritual y los runbooks NO se bloquean
RITUAL = [
    "git checkout main",
    "git status --short",
    "git log --oneline main..trabajo/guardias-claude",
    'git merge --no-ff trabajo/guardias-claude -m "merge: las guardias de Claude Code"',
    "git merge --abort",
    'git tag -a stable/F37-guardias-claude -m "las guardias de Claude Code"',
    "git rev-parse --short HEAD",
    "git branch --show-current",
    'git rev-parse --short "stable/F37-guardias-claude^{commit}"',
    "git add PROJECT_STATE.md",
    "git diff --cached --name-only",
    "uv run botsito state check",
    "make check > make-check.log 2>&1",
    'grep "SELLO: make check en verde" make-check.log',
    "rm make-check.log",
    'BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): trabajo/x, cerrada en main (stable/F37)"',
    "git push --atomic origin main stable/F37-guardias-claude",
    "git ls-remote --tags origin stable/F37-guardias-claude",
    "curl -s --ssl-no-revoke https://api.github.com/repos/Fibobrioso/Botsito/commits/"
    "$(git rev-parse HEAD)/check-runs | grep -o "
    '\'"status": *"[^"]*"\\|"conclusion": *"[^"]*"\'',
    "git push origin main",
    "git branch -d trabajo/guardias-claude",
    "make hooks",
    "uv run botsito knowledge validate > knowledge-validate.log 2>&1",
    "uv run botsito fidelidad build --artefacto eurusd-2026-03 --seed 20261001",
    "uv run python scripts/huso_por_velas.py --libro "
    '"corpus/Estrategia del trader/Material adicional de su operativa/'
    'backtesting-analytics ABRIL 2026.xlsx" --mes 2026-04',
    'uv run python -c "from pathlib import Path; from botsito.cases.holdout import casos_ocultos; '
    "print(any('2026-04-07' in c for c in casos_ocultos(Path('.'))))\"",
    "uv run python scripts/hoja_preguntas.py",
    "uv run botsito motor visor --caso caso-eurusd-2026-04-01",
    "uv run pytest tests/unit/test_guardia_claude.py -q",
    "uv run botsito corpus frames show --video v4 --t 1:06:12 --n 3",
]


@pytest.mark.parametrize("comando", RITUAL)
def test_el_ritual_y_los_runbooks_pasan(g: ModuleType, comando: str) -> None:
    """Contra el repo REAL: lo que hoy ejecuta el ritual (RITUAL.md) y los runbooks."""
    assert _bash(g, RAIZ, comando) is None, comando


# ------------------------------------------------------------------------------- PowerShell
@pytest.mark.parametrize(
    ("comando", "bloquea"),
    [
        (
            f"Get-Content '{MATERIAL}/Backtest marzo 2026/backtesting-analytics MARZO 2026.xlsx'",
            True,
        ),
        (f"Get-FileHash '{MATERIAL}/Backtest marzo 2026/asdasd.jpeg'", False),
        (f"Get-ChildItem '{MATERIAL}/Backtest marzo 2026'", False),
        ("Get-ChildItem -Recurse data | Select-String septiembre", True),
        ("Get-Content docs/a.md -TotalCount 5", False),
        ("git push --force origin trabajo/x", True),
        ("Remove-Item -Recurse -Force data/fotogramas", True),
        ("Invoke-Expression $codigo", True),
        ("git status", False),
    ],
)
def test_powershell(g: ModuleType, repo: Path, comando: str, bloquea: bool) -> None:
    motivo = _decide(g, repo, "PowerShell", command=comando)
    assert (motivo is not None) is bloquea, (comando, motivo)


# ---------------------------------------------------------------- el proceso, de punta a punta
def _ejecutar(evento: dict[str, Any]) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PYTHONUTF8": "1"}
    return subprocess.run(
        [sys.executable, str(GUARDIA)],
        input=json.dumps(evento),
        capture_output=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


def test_el_proceso_sale_con_2_y_el_motivo_o_con_0() -> None:
    marzo = RAIZ / MATERIAL / "Backtest marzo 2026" / "backtesting-analytics MARZO 2026.xlsx"
    bloqueado = _ejecutar(
        {"tool_name": "Read", "tool_input": {"file_path": str(marzo)}, "cwd": str(RAIZ)}
    )
    assert bloqueado.returncode == 2
    assert "GUARDIA" in bloqueado.stderr and "CLAUDE.md" in bloqueado.stderr
    pasa = _ejecutar(
        {"tool_name": "Bash", "tool_input": {"command": "git status"}, "cwd": str(RAIZ)}
    )
    assert pasa.returncode == 0, pasa.stderr
    roto = _ejecutar({"tool_name": "Bash", "tool_input": {"command": 'cat "corpus/sin cerrar'}})
    assert roto.returncode == 2


# ------------------------------------------------------------------- .claude/settings.json
def _casa_regla(regla: str, comando: str) -> bool:
    """La semantica documentada de una regla `Bash(...)`: `*` es cualquier texto, `:*` final
    equivale a ` *`, un ` *` final casa tambien el comando a secas, y las asignaciones del
    principio se saltan (code.claude.com/docs/en/permissions, 2026-10-01)."""
    m = re.fullmatch(r"Bash\((.*)\)", regla)
    assert m, regla
    patron = m.group(1)
    if patron.endswith(":*"):
        patron = patron[:-2] + " *"
    cuerpo = re.escape(patron).replace(r"\*", ".*")
    if patron.endswith(" *") and patron.count("*") == 1:
        cuerpo = re.escape(patron[:-2]) + r"(?: .*)?"
    comando = re.sub(r"^(?:[A-Za-z_][A-Za-z0-9_]*=\S*\s+)+", "", comando)
    partes = re.split(r"\s*(?:&&|\|\||;|\|)\s*", comando)
    return any(re.fullmatch(cuerpo, p.strip(), re.S) for p in partes)


def test_los_ajustes_registran_la_guardia_y_las_denegaciones() -> None:
    ajustes = json.loads(AJUSTES.read_text(encoding="utf-8"))
    entradas = ajustes["hooks"]["PreToolUse"]
    assert len(entradas) == 1
    assert set(entradas[0]["matcher"].split("|")) == {"Read", "Grep", "Glob", "Bash", "PowerShell"}
    orden = entradas[0]["hooks"][0]["command"]
    assert "PYTHONUTF8=1" in orden and ".claude/hooks/guardia.py" in orden
    deny = ajustes["permissions"]["deny"]
    for comando in (
        "git commit --no-verify -m x",
        "git commit -m x --no-verify",
        "git push --no-verify",
        "git push --force origin x",
        "git push origin x --force",
        "git push -f origin x",
        "git tag -d stable/F01",
        "git tag --delete stable/F01",
        "git push origin --delete stable/F01",
        "rm -rf data",
        "rm -rf corpus/x",
        "rm -rf knowledge",
        "BOTSITO_ALLOW_MAIN=1 git commit --no-verify -m x",
    ):
        assert any(_casa_regla(r, comando) for r in deny), comando


def test_el_push_a_main_pide_confirmacion() -> None:
    """Decision del consultor del 2026-10-01: `ask`, no `deny`. El ritual sigue pudiendo empujar,
    pero solo con la confirmacion de Aleks; una tarea nocturna se queda esperando."""
    ask = json.loads(AJUSTES.read_text(encoding="utf-8"))["permissions"]["ask"]
    for comando in (
        "git push --atomic origin main stable/F37-guardias-claude",
        "git push origin main",
        "BOTSITO_ALLOW_MAIN=1 git push origin main",
        "git push origin HEAD:main",
        "git push origin HEAD:refs/heads/main",
    ):
        assert any(_casa_regla(r, comando) for r in ask), comando
    for comando in ("git push origin trabajo/guardias-claude", "git push -u origin feature/x"):
        assert not any(_casa_regla(r, comando) for r in ask), comando


@pytest.mark.parametrize("comando", RITUAL)
def test_ninguna_denegacion_toca_el_ritual(comando: str) -> None:
    deny = json.loads(AJUSTES.read_text(encoding="utf-8"))["permissions"]["deny"]
    assert not [r for r in deny if _casa_regla(r, comando)], comando


def test_los_ajustes_locales_no_se_versionan() -> None:
    r = subprocess.run(
        ["git", "check-ignore", "-q", ".claude/settings.local.json"], cwd=RAIZ, check=False
    )
    assert r.returncode == 0
    r = subprocess.run(
        ["git", "check-ignore", "-q", ".claude/settings.json"], cwd=RAIZ, check=False
    )
    assert r.returncode == 1
