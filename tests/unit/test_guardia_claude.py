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
        # `make` es una ejecucion: su `Makefile` tiene que ser el de `main`
        # (`trabajo/guion-mismo-comando`, decision 3 del consultor).
        "Makefile",
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
    assert p.sesiones_en_cuarentena == {"v7", "v8", "v9", "v10"}
    assert p.meses_legibles == {"2026-01", "2026-04", "2026-08"}
    assert p.meses_reservados >= {"2026-05", "2026-09"}


def test_las_rutas_se_comparan_igual_en_cualquier_sistema(g: ModuleType, repo: Path) -> None:
    """La primera CI de la guardia (run 36889215829, Linux) salio roja con 24 fallos: `relativa`
    comparaba con `\\` y `os.path.normcase` no pasa a minusculas fuera de Windows, asi que ninguna
    ruta se reconocia dentro del repo. `_normcase` da minusculas y `/` en cualquier sistema."""
    p = g.Politica(repo)
    assert "\\" not in g._normcase(str(repo / "Corpus" / "X.txt"))
    assert g._normcase(str(repo / "Corpus" / "X.txt")).endswith("/corpus/x.txt")
    con_barras = str(repo).replace("\\", "/") + "/Knowledge/Cases/holdout/1/x.yaml"
    assert p.relativa(con_barras) == "knowledge/cases/holdout/1/x.yaml"
    assert p.relativa(str(repo)) == ""
    assert p.relativa(str(repo) + "-otro/x") is None
    assert p.motivo_fichero(str(repo / "SONDA.CRUDA-NO-LEER.txt")) == g.R_CUARENTENA
    # La segunda CI (run 36891855700): las zonas se guardan en minusculas y en Linux hay que
    # encontrar la carpeta con su grafia real para recorrerla.
    assert p._ruta_real(g.MATERIAL) == repo / MATERIAL
    assert p._ruta_real("corpus/no-existe") is None


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
        'for d in docs/*.md; do wc -l "$d"; done',  # `d` es una variable de bucle de la lista
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
        # Sin `--video` pasa desde `trabajo/cuarentena-por-defecto` (el indice sale filtrado);
        # con `--video` de una sesion en cuarentena sigue bloqueado (segunda capa).
        ("uv run botsito kb find stop", False),
        ("uv run botsito kb find stop --video v7", True),
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
    """v7 y v9 tienen tramos, pero su cruda ya no se lee entera: solo se vigilan los de v6. Desde
    `trabajo/cuarentena-por-condicion` (revisor, A4), tambien sus dos tramos de precaucion de la
    regla del mes por condicion."""
    assert g.Politica(RAIZ).tramos_vigilados == {
        "v6": [
            (2_460_000, 3_011_000),
            (6_810_000, 7_051_000),
            (60_720, 63_160),
            (8_777_201, 8_778_341),
        ]
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


# ------------------------------------ el corpus sin filtrar (`trabajo/cuarentena-por-defecto`)
OPCION = "--" + "crudo"
LLAMADA = "cru" + "do=True"


@pytest.mark.parametrize(
    "comando",
    [
        f"uv run botsito {OPCION} kb find hola",  # al principio
        f"uv run botsito kb find hola {OPCION}",  # al final
        f"uv run botsito kb at --video v1 --t 0:00:01 {OPCION}=1",  # con =
        f"uv run botsito corpus transcript show --video v1 --t0 0:00:01 --t1 0:00:02 {OPCION} si",
        "uv run botsito corpus frames show --video v1 --t 0:00:01 --cru",  # abreviada
        f"uv run python -c 'from botsito.corpus import x; x.f({LLAMADA})'",  # python -c
        "uv run python - <<'EOF'\nfrom botsito import x\nx.f(" + LLAMADA + ")\nEOF\n",  # heredoc
        "uv run python -c 'f(**{\"cru" + "do\": True})'",  # por diccionario
        f"make check {OPCION} > make-check.log 2>&1",  # make check con argumentos extra
    ],
)
def test_la_guardia_bloquea_el_corpus_sin_filtrar(g: ModuleType, repo: Path, comando: str) -> None:
    motivo = _bash(g, repo, comando)
    assert motivo is not None and g.R_CRUDO in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "uv run botsito kb find hola --video v1",
        "uv run botsito kb find hola --video v1 --contexto",
        "uv run botsito kb at --video v1 --t 0:00:01",
        "uv run botsito corpus transcript show --video v1 --t0 0:00:01 --t1 0:00:02",
        "uv run botsito corpus frames show --video v1 --t 0:00:01",
        "uv run python -c 'from botsito.corpus import x; x.f(cru" + "do=False)'",
        "make check > make-check.log 2>&1",
        "uv run pytest",
    ],
)
def test_sin_la_opcion_los_mismos_comandos_pasan(g: ModuleType, repo: Path, comando: str) -> None:
    assert _bash(g, repo, comando) is None, comando


def test_un_guion_nuevo_con_el_corpus_sin_filtrar_se_bloquea(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    guion = tmp_path / "nuevo.py"
    guion.write_text(f"from botsito import x\nx.f({LLAMADA})\n", encoding="utf-8")
    motivo = _bash(g, repo, f'uv run python "{guion}"')
    assert motivo is not None and g.R_CRUDO in motivo
    motivo = _decide(g, repo, "PowerShell", command=f"uv run botsito kb find hola {OPCION}")
    assert motivo is not None and g.R_CRUDO in motivo


def test_un_fichero_con_texto_oculto_no_se_lee(g: ModuleType, repo: Path) -> None:
    """La lista la calcula `botsito.corpus.cuarentena` y la guardia la lee de su fichero
    (ordenes del consultor del 2026-10-01): propuestas con segmentos ocultos y salidas de medicion
    que ya no se reproducen. Aqui, sintetica."""
    from botsito.corpus.cuarentena import FICHERO_OCULTOS, texto_de_la_lista

    oculta = _escribir(repo, "knowledge/_proposals/pr-v2-000100-000200-aaaaaaaa.yaml")
    libre = _escribir(repo, "knowledge/_proposals/pr-v2-000300-000400-bbbbbbbb.yaml")
    salida = _escribir(repo, "docs/validation/X-SALIDA.txt")
    otra = _escribir(repo, "docs/validation/Y-SALIDA.txt")
    _escribir(
        repo,
        FICHERO_OCULTOS,
        texto_de_la_lista([f"knowledge/_proposals/{oculta.name}", "docs/validation/X-SALIDA.txt"]),
    )
    for ruta in (oculta, salida):
        motivo = _decide(g, repo, "Read", file_path=str(ruta))
        assert motivo is not None and g.R_FICHERO_OCULTO in motivo, ruta
        assert _bash(g, repo, f'cat "{ruta}"') is not None, ruta
        assert _decide(g, repo, "Grep", pattern="x", path=str(ruta)) is not None, ruta
    assert _decide(g, repo, "Read", file_path=str(libre)) is None
    assert _decide(g, repo, "Read", file_path=str(otra)) is None


def _guion_de_la_lista() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "ficheros_con_ocultos", RAIZ / "scripts" / "ficheros_con_ocultos.py"
    )
    assert spec is not None and spec.loader is not None
    guion = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guion)
    return guion


def test_la_lista_de_la_guardia_es_la_que_se_calcula() -> None:
    """El fichero que lee la guardia es exactamente el que sale de
    `scripts/ficheros_con_ocultos.py`: nadie lo escribe a mano. Sin los datos de las
    transcripciones (la CI), las salidas y los ficheros que las copian no se recalculan: se
    comprueba que son de `docs/`."""
    from botsito.corpus.cuarentena import FICHERO_OCULTOS, texto_de_la_lista

    propuestas, otros = _guion_de_la_lista().calcular(RAIZ)
    actual = (RAIZ / FICHERO_OCULTOS).read_text(encoding="utf-8")
    if otros is None:
        listadas = [ln for ln in actual.splitlines() if ln and not ln.startswith("#")]
        otros = [r for r in listadas if not r.startswith("knowledge/_proposals/")]
        assert all(r.startswith("docs/") for r in otros), otros
    assert actual == texto_de_la_lista(propuestas + otros)


def test_una_linea_es_oculta_si_su_segmento_lo_esta(tmp_path: Path) -> None:
    """La definicion EXACTA (quinta orden): cuenta el segmento `n` de la transcripcion del pasaje,
    no que la linea haya dejado de salir. Sintetico."""
    from botsito.corpus.cuarentena import Filtro, Oculto

    salida = tmp_path / "docs" / "X-SALIDA.txt"
    salida.parent.mkdir(parents=True)
    salida.write_text(
        "=== A-1 · PASAJE 1 | tr-v1-falso-00000000 | 0:00:00-0:00:10 | x x1\n"
        "[0:00:00-0:00:05] #0 linea visible\n"
        "[0:00:05-0:00:10] #1 linea del oculto\n"
        "=== PASAJE 2 | tr-v2-falso-00000000 | 0:00:00-0:00:05 | x x1\n"
        "[0:00:00-0:00:05] #1 mismo numero, otra transcripcion\n",
        encoding="utf-8",
    )
    oculto = Filtro("v1", ocultos={1: Oculto("v1", 1, 5000, 10000, "c")})
    filtros = {"tr-v1-falso-00000000": oculto, "tr-v2-falso-00000000": Filtro("v2")}
    lineas = _guion_de_la_lista().lineas_ocultas(tmp_path, "docs/X-SALIDA.txt", filtros)
    assert lineas == ["linea del oculto"]


def test_la_guardia_y_el_modulo_dicen_la_misma_cuarentena(g: ModuleType) -> None:
    """La guardia guarda su copia (la deduce de `fuentes.yaml`: `drive_id: null` menos v6) y el
    modulo tiene la LISTA: tienen que decir lo mismo sobre el repositorio real."""
    from botsito.corpus import cuarentena

    assert g.Politica(RAIZ).sesiones_en_cuarentena == cuarentena.SESIONES_EN_CUARENTENA
    assert frozenset(cuarentena.EXCEPCIONES) == g.SESIONES_SIN_CUARENTENA


# ------------------------------------------------------------- el borrado de ramas remotas
@pytest.mark.parametrize(
    "comando",
    [
        "git push origin --delete fix/x",
        "git push origin :fix/x",
        "git push origin -d fix/dieta-y-skills",
        "git push --delete origin trabajo/x feature/F35-orden-stop-pivote",
        "git push origin :refs/heads/fix/x",
        "git push origin trabajo/x:refs/heads/fix/x",
    ],
)
def test_se_puede_borrar_una_rama_remota_de_trabajo(
    g: ModuleType, repo: Path, comando: str
) -> None:
    """RITUAL.md: la `fix/<rama>` que se empuja para la CI de Linux se borra al cerrar."""
    assert _bash(g, repo, comando) is None, comando


@pytest.mark.parametrize(
    "comando",
    [
        "git push origin --delete main",
        "git push origin :main",
        "git push origin --delete stable/F36j-guardia-linux",
        "git push origin :stable/F36j-guardia-linux",
        "git push origin --delete refs/tags/x",
        "git push origin :refs/tags/x",
        "git push origin --delete fix/x main",
        "git push origin --delete fix/x stable/F36j-guardia-linux",
        "git push origin :fix/x :main",
        "git push origin trabajo/x :refs/tags/x",
        "git push origin --delete 'fix/*'",
        "git push origin --delete fix/x/../../main",
        'git push origin --delete "$RAMA"',
        "git push origin :$RAMA",
        "git push origin --delete",
        "git push --prune origin 'refs/heads/*:refs/heads/*'",
        "git push origin :",
        "git push origin +:main",
        "git push --mirror origin",
    ],
)
def test_no_se_borra_main_ni_un_tag_ni_lo_que_no_se_puede_decidir(
    g: ModuleType, repo: Path, comando: str
) -> None:
    assert _bash(g, repo, comando) is not None, comando


def test_la_decision_de_borrado_sola_tambien_cierra_el_forzado_y_el_espejo(g: ModuleType) -> None:
    """Revisor de `trabajo/dieta-y-skills`, B1 y B2: `+:main` y `--mirror` los paraba ya el push
    forzado en Bash, pero no en PowerShell (`--mirror`) ni la funcion por si sola."""
    for argumentos in (["origin", "+:main"], ["--mirror", "origin"]):
        with pytest.raises(g.BloqueoError):
            g.decidir_borrado_remoto(argumentos)
    g.decidir_borrado_remoto(["origin", "+:fix/x"])


def test_borrar_un_tag_remoto_cita_la_regla_de_los_tags(g: ModuleType, repo: Path) -> None:
    motivo = _bash(g, repo, "git push origin --delete fix/x stable/F36j-guardia-linux")
    assert motivo is not None and g.R_TAG in motivo
    motivo = _bash(g, repo, "git push origin --delete main")
    assert motivo is not None and g.R_BORRAR_REMOTO in motivo


@pytest.mark.parametrize(
    ("comando", "bloquea"),
    [
        ("git push origin --delete fix/x", False),
        ("git push origin :fix/x", False),
        ("git push origin --delete main", True),
        ("git push origin --delete fix/x stable/F36j-guardia-linux", True),
        ("git push origin :refs/tags/x", True),
        ("git push origin --delete $rama", True),
        ("git push origin +:main", True),
        ("git push --mirror origin", True),
    ],
)
def test_powershell_borra_solo_ramas_de_trabajo(
    g: ModuleType, repo: Path, comando: str, bloquea: bool
) -> None:
    motivo = _decide(g, repo, "PowerShell", command=comando)
    assert (motivo is not None) is bloquea, (comando, motivo)


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
    "git push origin trabajo/guardia-linux:refs/heads/fix/guardia-linux",
    "git push origin --delete fix/guardia-linux",
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
        "git push origin --delete main",
        "git push origin --delete refs/tags/x",
        "git push origin --delete refs/heads/main",
        "git push origin :stable/F01",
        "git push origin :refs/heads/main",
        # Lo que cubria `git push * --delete *` antes de partirla (revision del consultor de
        # `trabajo/dieta-y-skills`): el borrado MIXTO, con una rama de trabajo delante.
        "git push origin --delete fix/x main",
        "git push origin --delete fix/x stable/F36j-guardia-linux",
        "git push origin --delete trabajo/x refs/tags/x",
        "git push origin --delete fix/x refs/heads/main",
        "git push origin :fix/x :main",
        "git push origin :fix/x :stable/F01",
        "git push origin -d main",
        "git push origin -d stable/F01",
        "git push origin -d fix/x main",
        "git push origin -d fix/x stable/F01",
        "git push origin --force fix/x",
        "git push --no-verify origin fix/x",
    ):
        assert any(_casa_regla(r, comando) for r in deny), comando
    # El borrado de la `fix/<rama>` del ritual no lo deniega ninguna regla: lo decide la guardia.
    for comando in (
        "git push origin --delete fix/x",
        "git push origin :fix/x",
        "git push origin -d fix/dieta-y-skills",
        "git push origin --delete trabajo/x feature/F35-orden-stop-pivote",
        "git push origin --delete fix/main-nueva",
    ):
        assert not any(_casa_regla(r, comando) for r in deny), comando


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


# ---------------------------- la ejecucion verificable (`trabajo/guion-mismo-comando`, 2026-10-07)
# Una sola condicion, `exigir_ejecucion_verificable`: la guardia solo deja ejecutar codigo si es
# SEGURO que lo que se ejecuta es lo que ella lee al inspeccionar el comando. Los tests la rompen a
# proposito: cada caso de la fase 0 (GUION-MISMO-COMANDO.md §0.b), cada via de §0.a, cada elemento
# de la lista cerrada y lo que queda fuera. El anexo `sin_condicion.py` comprueba que fallan si se
# quita la condicion.
def _ejecucion(repo: Path) -> str:
    """El guion malo `a.py`, NUEVO en la rama (sin seguir): imprime un fichero del holdout del repo
    sintetico. Y `inocuo.py`, tambien nuevo, que no nombra nada."""
    holdout = repo / "knowledge" / "cases" / "holdout" / "1" / "etiquetas.yaml"
    malo = f"print(open(r'{holdout}').read())\n"
    _escribir(repo, "a.py", malo)
    _escribir(repo, "inocuo.py", "print('hola')\n")
    _escribir(repo, "existente.py", "print('inocuo al inspeccionar')\n")
    _escribir(repo, "suelto/test_malo.py", malo)
    _escribir(repo, "malo.sh", f"cat {holdout.as_posix()}\n")
    return malo


@pytest.mark.parametrize(
    "comando",
    [
        "cp a.py b.py && uv run python b.py",  # b1: el guion no existe al inspeccionar
        "cp a.py existente.py && uv run python existente.py",  # b1': existe, inocuo
        "cp a.py scripts/otro.py && uv run python scripts/otro.py",  # b2: el de main
        "cat > x.py <<'EOF'\n{MALO}EOF\npython x.py",  # b3
        "cat > x.py <<'EOF' && python x.py\n{MALO}EOF\n",  # b3'
        "python x.py $(cp a.py x.py)",  # b4
        "echo $(cp a.py x.py); python x.py",  # b4'
        "PYTHONUTF8=$(cp a.py x.py) python x.py",  # b4''
        "cp a.py x.py & python x.py",  # b5
        "cat a.py | tee x.py && python x.py",  # b5'
        "cat a.py | tee x.py | python x.py",  # b5''
        "cp a.py otros/test_nuevo.py && uv run pytest otros/test_nuevo.py",  # b6
        "cp a.py tests/unit/test_nuevo.py && uv run pytest tests/unit/test_nuevo.py",
        "python existente.py <(cp a.py existente.py)",  # sustitucion de proceso
        "python existente.py & cp a.py existente.py",  # en segundo plano, a la vez
        "python existente.py > existente.py",  # la salida, a su propio guion
        "echo hola | python existente.py",  # lo que va antes por la tuberia
        # revisor, B1: el programa, por su NOMBRE y con las opciones globales de `uv`
        "cp a.py b.py && uv -q run python b.py",
        "cp a.py b.py && uv --no-cache run python b.py",
        "cp a.py b.py && /usr/bin/env python b.py",
        "cp a.py b.py && uv run botsito state check",  # botsito es una ejecucion (revisor 2, B8)
        "cp a.py b.py && python --version",  # tambien lo que no corre codigo, por la funcion (A3)
    ],
)
def test_ejecucion_cambiada_en_el_mismo_comando_se_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    malo = _ejecucion(repo)
    motivo = _bash(g, repo, comando.replace("{MALO}", malo))
    assert motivo is not None and g.R_EJECUCION in motivo, (comando, motivo)


@pytest.mark.parametrize(
    ("herramienta", "comando"),
    [
        ("Bash", "bash malo.sh"),  # via 2: el guion de shell, leido como bash
        ("Bash", "python < a.py"),  # via 4: la entrada estandar, leida como guion
        ("Bash", "python -m a"),  # via 5: `-m` solo para pytest
        ("Bash", "uv run pytest suelto"),  # via 6: un directorio fuera de tests/
        ("Bash", "make x"),  # via 7: el Makefile cambiado en la rama (lo cambia el test)
        ("Bash", 'pwsh -c "python inocuo.py"'),  # via 8, desde Bash
        ("PowerShell", "python inocuo.py"),  # via 8
        ("PowerShell", "uv run botsito state check"),  # via 8
        ("PowerShell", "& ./x.ps1"),  # via 8: el operador de llamada
        ("Bash", "./a.py"),  # via 9: un fichero como programa
        ("Bash", "uv run a.py"),  # via 9
        ("Bash", "python3.12 a.py"),  # via 9: el interprete con version
        ("Bash", "nice -n 5 python a.py"),  # via 9: el envoltorio con sus opciones
        ("Bash", "timeout -s KILL 5 python a.py"),  # via 9
        ("Bash", "winpty python inocuo.py"),  # via 9: un lanzador que la guardia no conoce
        ("Bash", "find docs -exec python inocuo.py \\;"),  # via 10
        ("Bash", "git -c alias.x='!python inocuo.py' x"),  # via 11
        ("Bash", "python - <<'EOF'\n{MALO}EOF\n"),  # el heredoc, leido entero
        ("Bash", "/usr/bin/env python a.py"),  # revisor, B1
        ("Bash", "uv --directory . run python a.py"),  # revisor, B1
        ("Bash", "uv tool run python a.py"),  # revisor, B1
        ("Bash", "uvx ./a.py"),  # revisor, B1
        ("Bash", "{python,a.py}"),  # revisor, B1: expansion de llaves
        ("Bash", "xargs python < docs/a.md"),  # via 12, por la funcion (revisor, A1)
        ("Bash", "eval 'python inocuo.py'"),  # via 13
        ("Bash", "cmd /c python inocuo.py"),  # via 14
        ("Bash", "git --config-env=alias.x=CMD x"),  # revisor, B3
    ],
)
def test_ejecucion_cada_via_pasa_por_la_condicion(
    g: ModuleType, repo: Path, herramienta: str, comando: str
) -> None:
    malo = _ejecucion(repo)
    _escribir(repo, "Makefile", "x:\n\tpython inocuo.py\n")  # distinto del de main
    motivo = _decide(g, repo, herramienta, command=comando.replace("{MALO}", malo))
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "uv run python inocuo.py",
        "cd docs && uv run python ../inocuo.py",  # cd
        "S=hola; python inocuo.py",  # asignacion suelta con un nombre de la lista
        "PYTHONUTF8=1 python inocuo.py",  # asignacion literal que precede al comando
        "export PYTHONUTF8=1 && python inocuo.py",  # export literal
        "set -e; python inocuo.py",
        "set -u; python inocuo.py",
        "set -o pipefail; python inocuo.py",
        "set -euo pipefail; python inocuo.py",  # combinacion
        "python inocuo.py 2>&1 | head -3",
        "python inocuo.py | tail -3",
        "python inocuo.py | grep hola",
        "python inocuo.py | wc -l",
        "python inocuo.py | sort",
        "python inocuo.py | uniq -c",
        "python inocuo.py | cut -c1-10",
        "python inocuo.py > salida.txt 2>&1; echo $?",  # lo de despues, en otro comando
        "python -X utf8 inocuo.py",
        "uv run --with pyyaml python inocuo.py",
        "python --version",
        "grep python docs/a.md",  # un lector cuyo patron se llama python
        "command -v python",
        "uv run pytest -p no:cacheprovider tests/unit -q",
        "uv -q run python inocuo.py",  # opcion global de uv
        "timeout 60 python inocuo.py",
        "uv --version",
    ],
)
def test_ejecucion_lo_de_la_lista_cerrada_pasa(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


@pytest.mark.parametrize(
    "comando",
    [
        "inventado && python inocuo.py",  # un programa inventado antes
        "grep hola docs/a.md && python inocuo.py",  # un lector antes: tampoco esta en la lista
        "python inocuo.py && python existente.py",  # una ejecucion antes de otra
        "PYTHONUTF8=$Y python inocuo.py",  # asignacion no literal
        "PYTHONUTF8=$(echo 1) python inocuo.py",
        "export PYTHONUTF8=$Y; python inocuo.py",
        "set -x; python inocuo.py",
        "cd docs > f.txt && python ../inocuo.py",  # una redireccion antes
        "python inocuo.py | tee salida.txt",
        "python inocuo.py | sort -o salida.txt",
        "python inocuo.py | uniq - salida.txt",
        "python inocuo.py | cat",  # un programa conocido que no es un filtro
        "python",  # sin guion ni codigo
        "python -m json.tool docs/a.md",
        "env -S 'python inocuo.py'",
        "uv run --opcion-inventada python inocuo.py",
        "uv run pytest -p mi_plugin tests/unit",
        "cd docs && uv run pytest",  # sin rutas fuera de la raiz
        "python nuevo.py",  # no existe
        "cd && python inocuo.py",  # `cd` a secas va a HOME (revisor, B4)
        "cd - && python inocuo.py",
        "uv run pytest -o addopts=-pmi_plugin tests/unit",  # revisor, B3
        "uv run pytest -c otro.ini tests/unit",  # revisor, B3
        "uv run pytest -n $X tests/unit",  # revisor, A3
        "timeout -n eval python inocuo.py",  # revisor, A3: opcion que no conoce
        "timeout $X python inocuo.py",  # revisor, A3: duracion no literal
    ],
)
def test_ejecucion_lo_de_fuera_de_la_lista_se_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


def test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo(g: ModuleType, repo: Path) -> None:
    motivo = _bash(g, repo, "uv run python nuevo.py")
    assert motivo is not None and "no existe" in motivo
    assert "Write" in motivo and "OTRA llamada" in motivo


def test_ejecucion_make_solo_con_el_makefile_de_main(g: ModuleType, repo: Path) -> None:
    assert _bash(g, repo, "make check > make-check.log 2>&1") is None
    _escribir(repo, "Makefile", "check:\n\tpython inocuo.py\n")
    motivo = _bash(g, repo, "make check > make-check.log 2>&1")
    assert motivo is not None and "no es el de `main`" in motivo and "Aleks" in motivo
    assert _bash(g, repo, "make -f otro.mk check > make-check.log 2>&1") is not None


# --- que activa la condicion y lo que la configura, en listas cerradas (respuesta del consultor a
# §1.12, 2026-10-07): todo programa fuera de `NO_EJECUTAN` es una ejecucion; el fichero que recibe
# un programa desconocido, si no es el de `main`, se niega; y los nombres de entorno, cerrados.
PROHIBIDOS = [
    "PYTHONPATH",
    "PYTHONSTARTUP",
    "PYTHONHOME",
    "BASH_ENV",
    "ENV",
    "NODE_OPTIONS",
    "PERL5OPT",
    "RUBYOPT",
    "LD_PRELOAD",
    "LD_LIBRARY_PATH",
]


@pytest.mark.parametrize(
    "comando",
    [
        "cp a.py b.php && php b.php",  # (a): un programa desconocido, con algo delante
        "cp a.py b.py && setsid ./b.py",
        "php nuevo.php",  # (b): un fichero nuevo que puede ser lo que ejecuta
        "inventado docs/nuevo.md",  # (b): cualquier fichero que no es el de main
        "inventado $X",  # un argumento que se construye al ejecutarse
        "sudo make check > make-check.log 2>&1",  # lanza un programa que ejecuta
        "winpty python inocuo.py",
        "trap 'python inocuo.py' EXIT",  # `trap` sale de los lectores
        "awk -f a.py docs/a.md",  # un fichero de programa: lenguaje desconocido
        "awk -fa.py docs/a.md",
        "gawk --file=a.py docs/a.md",
        "sed -f a.py docs/a.md",
    ],
)
def test_ejecucion_lo_que_no_esta_en_la_lista_es_una_ejecucion(
    g: ModuleType, repo: Path, comando: str
) -> None:
    _ejecucion(repo)
    _escribir(repo, "nuevo.php", "<?php echo 1;")
    _escribir(repo, "docs/nuevo.md", "x\n")
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "inventado --version",  # un programa desconocido sin ficheros ni nada delante
        "php scripts/otro.py",  # el fichero es el de main: codigo revisado
        "awk '{print $1}' docs/a.md",  # el programa va en el comando
        "sed -n 1p docs/a.md",
        "trap",
        "grep -n python docs/a.md",
    ],
)
def test_ejecucion_lo_que_si_se_puede_decidir_pasa(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


@pytest.mark.parametrize("nombre", PROHIBIDOS)
def test_ejecucion_un_nombre_de_entorno_que_carga_codigo_se_niega(
    g: ModuleType, repo: Path, nombre: str
) -> None:
    _ejecucion(repo)
    for comando in (
        f"{nombre}=x python inocuo.py",  # el que precede al comando
        f"export {nombre}=x",
        f"env {nombre}=x python inocuo.py",
        f"declare -x {nombre}=x",
        f"{nombre}=x git commit -m hola",  # tambien sin ejecucion: los hooks de git son codigo
    ):
        motivo = _bash(g, repo, comando)
        assert motivo is not None and "NOMBRES_DE_ENTORNO" in motivo, (comando, motivo)
    assert nombre not in g.NOMBRES_DE_ENTORNO


def test_ejecucion_los_nombres_de_entorno_son_una_lista_cerrada(g: ModuleType, repo: Path) -> None:
    _ejecucion(repo)
    for comando in (
        "PYTHONUTF8=1 python inocuo.py",
        "BOTSITO_ALLOW_MAIN=1 git commit -m hola",
        "S=hola; python inocuo.py",  # una variable del shell de la lista (S, W, R)
        "W=x; R=y; python inocuo.py",
    ):
        assert _bash(g, repo, comando) is None, comando
    # Respuesta del consultor a §1.21, punto 3: TODA asignacion, tambien la suelta a un nombre no
    # exportado, solo admite los nombres de la lista.
    for comando in (
        "MI_NOMBRE_INVENTADO=1 python inocuo.py",  # cualquier nombre fuera de la lista
        "X=hola; python inocuo.py",  # suelta, no exportada: antes pasaba, ahora se niega
        "CDPATH=sub; cd scripts && python de_main.py",  # bash interpreta CDPATH sin exportarla
        "IFS=x python inocuo.py",
        "PATH=.; python x.py",  # con PATH cambiado, `python` podria ser un fichero de la carpeta
        "PATH=. python x.py",
        "export MI_NOMBRE_INVENTADO=1",
        "declare -x BASH_ENV=x.sh",
    ):
        motivo = _bash(g, repo, comando)
        assert motivo is not None and "NOMBRES_DE_ENTORNO" in motivo, (comando, motivo)


def test_ejecucion_las_dos_listas_cerradas_dicen_su_porque(g: ModuleType) -> None:
    for lista in (g.NO_EJECUTAN, g.NOMBRES_DE_ENTORNO):
        assert all(isinstance(v, str) and len(v) > 10 for v in lista.values()), lista
    assert "trap" not in g.NO_EJECUTAN and "trap" not in g.LECTOR_DE_METADATOS
    for programa in ("python", "pytest", "make", "botsito", "bash", "php", "sudo", "awk -f"):
        assert programa not in g.NO_EJECUTAN, programa


# --- segunda pasada del revisor: lo que pasaba sin ser decidido, dentro de lo ya decidido
@pytest.mark.parametrize(
    ("herramienta", "comando"),
    [
        ("Bash", "node -r ./a.py inocuo.py"),  # B1: lo que carga una opcion es codigo
        ("Bash", "node --require=./a.py inocuo.py"),
        ("Bash", "node --import ./a.py inocuo.py"),
        ("Bash", "ruby -r ./a.py inocuo.py"),
        ("Bash", "node -r dotenv/config inocuo.py"),  # un modulo por su nombre: no se resuelve
        ("Bash", "bash --rcfile malo.sh -i -c true"),  # B6 c
        ("PowerShell", "Write-Output ( php x.php )"),  # B2: con espacio tras el parentesis
        ("PowerShell", "Write-Output $( cscript x.js )"),
        ("PowerShell", "Write-Output @( php x.php )"),
        ("PowerShell", "Get-Content docs/a.md; ( php x.php )"),
        ("PowerShell", "git -c alias.x='!python a.py' x"),
        ("Bash", "find docs -exec ls {} \\; -exec python a.py \\;"),  # B3 d: el segundo -exec
        ("Bash", "xargs -a docs/a.md python a.py"),  # B3 e: el valor de -a no es el programa
        ("Bash", "xargs --arg-file=docs/a.md python a.py"),
        ("Bash", "xargs --opcion-inventada python"),
        ("Bash", 'watch "python a.py"'),  # B4: una cadena de comando como argumento
        ("Bash", 'su -c "python a.py"'),
        ("Bash", 'ssh -o ProxyCommand="python a.py" host'),
        ("Bash", "tar --checkpoint=1 --checkpoint-action=exec=./a.py -cf out.tar inocuo.py"),
        ("Bash", "vim -c '!python a.py'"),
        ("Bash", "php {a,b}.py"),
        ("Bash", "./git status"),  # B5: un fichero con nombre de programa
        ("Bash", "sub/git status"),
        ("Bash", "./python inocuo.py"),
        ("Bash", "uv run --directory sub python scripts/otro.py"),  # B6 a
        ("Bash", "env -C sub python scripts/otro.py"),
        ("Bash", "uv run --env-file x.env python inocuo.py"),  # B6 b
        ("Bash", "uv run --with ./paquete python inocuo.py"),
        ("Bash", "sed -nf a.py docs/a.md"),  # B7: banderas agrupadas
        ("Bash", "sed -sf a.py docs/a.md"),
        ("Bash", "gawk -nf a.py docs/a.md"),
    ],
)
def test_ejecucion_lo_que_vio_la_segunda_pasada_se_niega(
    g: ModuleType, repo: Path, herramienta: str, comando: str
) -> None:
    malo = _ejecucion(repo)
    for rel in ("git", "sub/git", "python"):
        _escribir(repo, rel, "#!/usr/bin/env python\n" + malo)
    _escribir(repo, "sub/scripts/otro.py", malo)
    _escribir(repo, "x.env", "PYTHONSTARTUP=a.py\n")
    motivo = _decide(g, repo, herramienta, command=comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    ("herramienta", "comando"),
    [
        ("Bash", "sed -n -e 1p docs/a.md"),
        ("Bash", "sed -i.bak -e 1p docs/a.md"),
        ("Bash", "awk -F: '{print $1}' docs/a.md"),
        ("Bash", "find docs -name x -exec ls {} \\;"),
        ("Bash", "echo docs/a.md | xargs -0 ls"),
        ("Bash", "node --version"),
        ("Bash", "uv run --with pyyaml python inocuo.py"),
        ("PowerShell", "Write-Output (Get-Content docs/a.md)"),
    ],
)
def test_ejecucion_lo_que_la_segunda_pasada_no_toca_pasa(
    g: ModuleType, repo: Path, herramienta: str, comando: str
) -> None:
    _ejecucion(repo)
    motivo = _decide(g, repo, herramienta, command=comando)
    assert motivo is None, (comando, motivo)


# --- respuesta a §1.21, punto 1: un programa de NO_EJECUTAN solo es inocuo en una forma de la lista
@pytest.mark.parametrize(
    "comando",
    [
        "git bisect run python a.py",  # subcomando fuera de la lista: ejecuta
        "git submodule foreach 'python a.py'",
        "git filter-branch --tree-filter 'python a.py'",
        "gh alias set -s x 'python a.py'",  # gh: subcomando fuera de la lista
        "sort --compress-program=./a.py docs/a.md",  # sort: opcion que ejecuta
        "sort --random-source=./a.py docs/a.md",
        "awk 'BEGIN{system(\"python a.py\")}' docs/a.md",  # awk: system()
        "awk '{print > \"out\"}' docs/a.md",  # awk: redirige
        "awk '{while((getline x)>0) y=x}' docs/a.md",  # awk: getline
        "sed 's/x/y/e' docs/a.md",  # sed: s///e ejecuta
        "sed '1e python a.py' docs/a.md",  # sed: comando e
        "sed 'w salida.txt' docs/a.md",  # sed: comando w escribe
        "sed '1r /etc/passwd' docs/a.md",  # sed: comando r lee
    ],
)
def test_ejecucion_un_modo_que_ejecuta_se_niega(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "git status",
        "git log --oneline",
        "git worktree add /tmp/x",  # subcomando de la lista: pasa (lo que escribe no es ejecucion)
        "gh run view 123",
        "gh auth status",
        "sort -rn docs/a.md",
        "sort -k2 -t: docs/a.md",
        "awk '{print $1}' docs/a.md",  # programa inocuo
        "awk 'NR==66{print $5, $8}' docs/a.md",
        "sed -n '1,60p' docs/a.md",  # rango + p
        "sed -n '/inicio/,/fin/p' docs/a.md",  # direcciones regex + p
        "sed 's/\\r$//' docs/a.md",  # s/// sin e ni w
        "sed -i 's#a#b#g' docs/a.md",  # s/// con flag g
    ],
)
def test_ejecucion_una_forma_inocua_pasa(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


# --- respuesta a §1.27: git opcion B, awk/sed como lista admitida, asignaciones por cualquier via
@pytest.mark.parametrize(
    "comando",
    [
        "git -c core.sshCommand=nx fetch",  # clave de -c fuera de la lista (vacia)
        "git -c core.pager=nx log",
        "git -c core.fsmonitor=nx status",
        "git fetch --upload-pack=nx .",  # opciones de transporte
        "git push --receive-pack=nx .",
        "git archive --remote=. --exec=nx HEAD",
        "git config core.sshCommand nx",  # config que fija
        "git config core.pager nx",
        "git remote add x ext::nx",  # remote que no es de lectura
        "git remote set-url x ext::nx",
        "git merge -s nx rama",  # estrategia fuera de la lista (vacia)
        "awk -F , 'BEGIN{system(\"python a.py\")}' docs/a.md",  # system tras -F (B1)
        "awk -v x=1 'BEGIN{system(\"python a.py\")}' docs/a.md",
        "awk '{c=\"python a.py\"; print | c}' docs/a.md",  # tuberia a comando
        "sed -e p -e 'w x.py' docs/a.md",  # -e con w (B1)
        "sed --expression='w x.py' docs/a.md",
        "sed -e 1d -e 'e nx' docs/a.md",  # -e con e
        "sed '1a\\\\ texto' docs/a.md",  # comando a (append), fuera de la lista
        "sed '1r /etc/passwd' docs/a.md",
    ],
)
def test_ejecucion_la_ultima_ronda_niega(g: ModuleType, repo: Path, comando: str) -> None:
    """git/awk/sed, por la condicion (`exigir_ejecucion_verificable`)."""
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "read PATH <<< .",  # builtin que fija un nombre fuera de la lista
        "read ruta <<< x",
        "printf -v PATH .",
        "declare -x BASH_ENV=x.sh",
        "let x=1",  # let: se niega entero
        "getopts o v",
        "mapfile -t lineas < docs/a.md",
        "(( PATH = 1 ))",  # aritmetico
        "i=0; (( i++ )); echo $i",
        "for PATH in .; do ls; done",  # la variable de bucle, fuera de la lista
    ],
)
def test_ejecucion_la_ultima_ronda_fija_variable_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    """Asignaciones por otras vias (builtins, `(( ))`, `for`), por `_niega` directo."""
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "NOMBRES_DE_ENTORNO" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "git config core.autocrlf",  # la forma medida (get)
        "git config --get core.autocrlf",
        "git remote -v",
        "git remote show origin",
        "git merge --no-ff rama -m x",  # merge sin -s, como el ritual
        "git merge --abort",
        "awk -F , '{print $1}' docs/a.md",  # programa inocuo con -F
        "awk -v x=1 '{print x, $1}' docs/a.md",
        "awk '$1 > 5' docs/a.md",  # el > de comparacion
        "awk '{if ($1>5) print $2}' docs/a.md",
        "sed -n -e 1p -e 3p docs/a.md",  # varios -e inocuos
        "sed -ne '1,5p' docs/a.md",  # cluster -ne
        "sed 's/a/b/g; 3d' docs/a.md",
        "read d <<< x",  # un nombre de bucle de la lista
        'for d in docs/*.md; do wc -l "$d"; done',
    ],
)
def test_ejecucion_la_ultima_ronda_admite(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


# --- cuarta pasada del revisor: los huecos del punto 0 (abreviaturas de sort, envoltorios en
# find/xargs, git reset/revert, unset, printf/read que fijan, la redireccion de awk escondida y
# git en PowerShell). Cada uno medido con `decidir()` antes de escribirlo (§1.28).
@pytest.mark.parametrize(
    "comando",
    [
        "sort --compress-pro=scripts/otro.py docs/a.md",  # abreviatura de --compress-program
        "sort --random-s=scripts/otro.py docs/a.md",  # abreviatura de --random-source
        "find src -name '*.py' -exec env python scripts/otro.py {} ;",  # envoltorio env
        "find docs -exec command python scripts/otro.py {} +",  # envoltorio command
        "echo x | xargs env python scripts/otro.py",
        "echo x | xargs command sh -c 'echo hi'",
        "git reset --hard HEAD~1",  # subcomando fuera de la lista cerrada (B5)
        "git revert --no-edit HEAD",
        "awk '{print $1/2 > $3/4}' docs/a.md",  # redireccion escondida entre divisiones (B4)
    ],
)
def test_ejecucion_cuarta_pasada_niega(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "unset PATH",  # quita una variable fuera de la lista cerrada (B2)
        "printf -vPATH '%s' x",  # `-v` pegado al nombre (B3)
        "read 'PATH[0]'",  # nombre con indice de array (B3)
    ],
)
def test_ejecucion_cuarta_pasada_fija_variable_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "NOMBRES_DE_ENTORNO" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "[ -f docs/a.md ]",  # `[`/`test` son lectores, no un comodin (B10)
        "[ -d src ]",
        "test -f docs/a.md",
        "cd -P src",  # `-P`/`-L` son opciones de cd, no el destino
        "cd -L src",
        "unset S",  # un nombre de la lista cerrada
        "sort -S 1M docs/a.md",  # `-S` (buffer) no ejecuta
        "awk '/a|b/{print}' docs/a.md",  # la `|` de una regex, no una tuberia
        "awk '{print $1/2, $3/4}' docs/a.md",  # divisiones sin redireccion
        "find . -exec sha256sum {} +",  # un lector sigue exento
    ],
)
def test_ejecucion_cuarta_pasada_admite(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


@pytest.mark.parametrize(
    "comando",
    [
        "git reset --hard HEAD~1",  # subcomando fuera de la lista cerrada, tambien en PowerShell
        "git revert HEAD",
        "git bisect run ./x.ps1",
    ],
)
def test_ejecucion_cuarta_pasada_powershell_git_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    """git en PowerShell pasaba por `PS_NO_EJECUTAN`: ahora su subcomando pasa por la lista
    cerrada (B1)."""
    motivo = _decide(g, repo, "PowerShell", command=comando)
    assert motivo is not None and "PowerShell" in motivo, (comando, motivo)


# --- quinta pasada del revisor: builtins negados por defecto (§1.27.3), awk entre divisiones con
# espacios, mas vias de fijar una variable, y las perdidas de git frente a main.
@pytest.mark.parametrize(
    "comando",
    [
        "shopt -s extglob",  # un builtin fuera de la lista cerrada (B1)
        "enable -n printf",
        "ulimit -n 10",
        "bind -x ':ls'",
        "complete -A function foo",
        "compgen -A function",
        "caller 0",
        "fc -l",
        "umask 022",
        "pushd .",
        "popd",
        "awk '{ print $1 / 2 > $3 / 4 }' docs/a.md",  # redireccion entre divisiones con espacios
        "awk '{ print (a) / 2 > \"out\" }' docs/a.md",
    ],
)
def test_ejecucion_quinta_pasada_niega(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "Regla:" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "for PATH; do ls; done",  # `for` sin `in` fija la variable igual (B3)
        "declare -n d=PATH",  # un nameref apunta a otra variable (B3)
        "PATH+=:x",  # `NOMBRE+=` suelto, fuera de la lista (B3/B9)
        "read $S <<< .",  # un nombre que se construye al ejecutarse (B3)
    ],
)
def test_ejecucion_quinta_pasada_fija_variable_niega(
    g: ModuleType, repo: Path, comando: str
) -> None:
    _ejecucion(repo)
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "NOMBRES_DE_ENTORNO" in motivo, (comando, motivo)


@pytest.mark.parametrize(
    "comando",
    [
        "git ls-files",  # lectores de git que `main` deja pasar (B5)
        "git ls-tree HEAD",
        "git show-ref",
        "git hash-object docs/a.md",
        "git pull",
        "type ls",  # builtins lectores, admitidos
        "hash -r",
        "shift",
        "awk '/a|b/{print}' docs/a.md",  # la `|` de una regex, no una tuberia (B2, sin regresion)
        "S+=x echo hola",  # `NOMBRE+=` de un nombre de la lista
    ],
)
def test_ejecucion_quinta_pasada_admite(g: ModuleType, repo: Path, comando: str) -> None:
    _ejecucion(repo)
    assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


@pytest.mark.parametrize("opcion", ["-P", "-L"])
def test_cd_fisico_resuelve_el_destino_y_bloquea_la_lectura(
    g: ModuleType, repo: Path, opcion: str
) -> None:
    """`cd -P`/`-L <dir>` resuelve el destino (no toma `-P` como ruta): despues, leer material
    reservado se niega (revisor quinta pasada, A4). Con el bug, `cd -P` dejaba el cwd en `-P` y la
    lectura pasaba."""
    comando = f"cd {opcion} knowledge/cases/holdout/1 && cat etiquetas.yaml"
    assert _bash(g, repo, comando) is not None, comando


def test_lectores_que_nombro_el_revisor_pasan(g: ModuleType, repo: Path) -> None:
    """Los lectores que entraron en `NO_EJECUTAN` por §1.21 punto 2 (revisor quinta pasada, R2)."""
    for comando in (
        "md5sum docs/a.md",
        "chmod +x scripts/otro.py",
        "jq '.x' docs/a.md",
        "tasklist",
        "test -f docs/a.md",
        "[ -f docs/a.md ]",
    ):
        assert _bash(g, repo, comando) is None, (comando, _bash(g, repo, comando))


def test_ejecucion_powershell_sin_ejecuciones_y_lo_demas_igual(g: ModuleType, repo: Path) -> None:
    for comando in (
        "Start-Process python",
        ".\\x.ps1",
        "make check > make-check.log 2>&1",
        # revisor, B2, y respuesta del consultor a §1.12: tambien en PowerShell, lista cerrada
        "[System.Diagnostics.Process]::Start('python','a.py')",
        "Get-ChildItem | ForEach-Object { python $_ }",
        "Write-Output $(python a.py)",
        "cscript x.js",
        ".\\x.exe",
        "Start-Job { .\\x }",
        "New-Object -ComObject WScript.Shell",
    ):
        motivo = _decide(g, repo, "PowerShell", command=comando)
        assert motivo is not None and "PowerShell" in motivo, (comando, motivo)
    for comando in ("git status", "Get-Content docs/a.md -TotalCount 5", "Write-Output hola"):
        assert _decide(g, repo, "PowerShell", command=comando) is None, comando


def test_ejecucion_una_sola_funcion_y_ninguna_via_decide_por_su_cuenta(g: ModuleType) -> None:
    """Toda via de ejecucion llama a `exigir_ejecucion_verificable` (directamente o por
    `_exigir_guion`, `_sin_guion` o `_ejecucion_lanzada`, que vuelve a `analizar_comando`), y la
    regla `R_EJECUCION` solo la escriben la funcion y su `_niega`."""
    import ast

    arbol = ast.parse(GUARDIA.read_text(encoding="utf-8"))
    funciones = {n.name: n for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef)}

    def llama(nombre: str) -> set[str]:
        return {
            n.func.id
            for n in ast.walk(funciones[nombre])
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        }

    puertas = {"exigir_ejecucion_verificable", "_exigir_guion", "_sin_guion"}
    for via in (
        "_analizar_interprete",
        "_analizar_shell",
        "_analizar_pytest",
        "_analizar_make",
        "_analizar_pwsh",
        "analizar_powershell",
        "_exigir_guion",
        "_sin_guion",
    ):
        assert llama(via) & puertas, via
    assert "exigir_ejecucion_verificable" in llama("analizar_comando")  # botsito y los lanzadores
    assert "_exigir_guion" in llama("analizar_comando")  # el fichero como programa
    assert "_ejecucion_lanzada" in llama("_analizar_find")
    assert "_ejecucion_lanzada" in llama("_analizar_git")
    assert "analizar_comando" in llama("_ejecucion_lanzada")
    usan_la_regla = {
        nombre
        for nombre, f in funciones.items()
        if any(isinstance(n, ast.Name) and n.id == "R_EJECUCION" for n in ast.walk(f))
    }
    assert usan_la_regla == {"_niega", "exigir_ejecucion_verificable"}

    def lanza(nombre: str) -> list[str]:
        return [
            ast.unparse(n.exc)
            for n in ast.walk(funciones[nombre])
            if isinstance(n, ast.Raise) and n.exc
        ]

    # Ninguna via de ejecucion niega por su cuenta (revisor, A1): no tienen ningun `raise`; los
    # envoltorios solo dicen que no saben (`IndecidibleError`), y lo decide la funcion; y en
    # `analizar_comando` el unico `raise` que queda es el de leer recursivamente sin ruta.
    for via in (
        "_analizar_interprete",
        "_analizar_shell",
        "_sin_guion",
        "_exigir_guion",
        "_analizar_pwsh",
        "_analizar_pytest",
        "_analizar_xargs",
        "_ejecucion_lanzada",
        "_ejecucion_de_un_programa_desconocido",
        "_exigir_nombres_de_entorno",
    ):
        assert lanza(via) == [], (via, lanza(via))
    assert all(x.startswith("IndecidibleError(") for x in lanza("_envoltorios"))
    assert all(x.startswith("IndecidibleError(") for x in lanza("_opciones_cerradas"))
    assert all("recursivo sin ruta" in x for x in lanza("analizar_comando")), lanza(
        "analizar_comando"
    )
