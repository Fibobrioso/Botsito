"""Medida de la fase 0.2 de `trabajo/guardia-enlaces` (TEMPORAL).

Corre como test TEMPORAL en `tests/unit/` (la guardia no lee `tests/`), se saca de alli antes del
commit y queda como anexo en `docs/validation/anexos/GUARDIA-ENLACES/`, con su salida. Precedente:
`docs/validation/anexos/GUARDIA-FALSOS-POSITIVOS/medida_parada2.py`.

Dos partes, y ninguna lee contenido protegido:

1. EN MEMORIA, con `decidir` (la funcion que llama `main`), sobre un repo INVENTADO en `tmp_path`
   con la estructura del real y ficheros FALSOS en cada clase protegida de la familia 1, en las
   cuatro formas del encargo: (a) dentro del repo, (b) por un enlace de dentro que apunta fuera
   -simulado con `_realpath` (b-sim) y con una union real (b-real)-, (c) una copia con la misma
   estructura fuera del repo, (d) la carpeta en si.
2. POR STDIN, con el JSON de PreToolUse simulado y la raiz REAL: las mismas clases en las formas
   (a), (c) y (d), y las rutas de `D:\\BotsitoCorpus` (solo la decision; nada se abre ni se lista
   desde la sesion: la guardia mira lo que mira en cada evento).

Las rutas protegidas van a trozos, como en `test_guardia_alias.py`. Imprime una linea por caso:
`parte | forma | clase | herramienta | decision`.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
EN_WINDOWS = sys.platform == "win32"

ETD = "Estrategia del trader"
MAT = "corp" + "us/" + ETD + "/Material adicional de su operativa"
SES = "corp" + "us/" + ETD + "/Ses" + "iones"
BTM = MAT + "/Back" + "test marzo 2026"
HOL = "knowledge/cases/hol" + "dout"
TRA = "data/transcrip" + "ciones"
CASO = "caso-eurusd-2026-05-04"  # el reservado del repo INVENTADO (no es uno real)

# clase -> ruta relativa (ficheros)
FICHEROS = {
    "holdout-1": f"{HOL}/1/{CASO}.yaml",
    "holdout-2": f"{HOL}/2/{CASO}.yaml",
    "holdout-3": f"{HOL}/3/{CASO}.yaml",
    "libro por nombre (backtesting-analytics de marzo)": f"{MAT}/backtesting-analytics MARZO 2026.xlsx",
    "libro de un mes reservado (mayo) en el material": f"{MAT}/resumen mayo 2026.xlsx",
    "imagen del material adicional": f"{MAT}/Capturas/foto.png",
    "imagen de Backtest marzo": f"{BTM}/x.png",
    "otro fichero de Backtest marzo": f"{BTM}/notas.txt",
    "hoja de Sesiones": f"{SES}/hoja-05.xlsx",
    "cruda en cuarentena (v7)": f"{TRA}/v7/large-v3/cruda.jsonl",
    "*cruda-NO-LEER*": "docs/x.cruda-NO-LEER.jsonl",
    "tramo no citable (v6)": f"{TRA}/v6/large-v3/cruda.txt",
    "id de caso reservado en knowledge/cases": f"knowledge/cases/kit/s1/{CASO}.yaml",
    "id de caso reservado en data/visor": f"data/visor/{CASO}.html",
    "feedback que etiqueta un reservado": "knowledge/feedback/fb-x.yaml",
    "fichero con ocultos (lista calculada)": "knowledge/_proposals/pr-v7-x.yaml",
}
CARPETAS = {
    "carpeta holdout/1": f"{HOL}/1",
    "carpeta Backtest marzo": BTM,
    "carpeta Sesiones": SES,
    "carpeta de la cruda v7": f"{TRA}/v7",
}
CONTENIDO = {
    "tramo no citable (v6)": "[0:45:00] uno\n[0:46:00] dos\n",
    "feedback que etiqueta un reservado": f"accion: LABEL_CASE\ncaso: {CASO}\n",
}


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


def _escribir(base: Path, rel: str, texto: str = "dato falso\n") -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def _git(repo: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def _estructura(base: Path) -> None:
    """Los ficheros falsos de cada clase y las carpetas, en `base`."""
    for clase, rel in FICHEROS.items():
        _escribir(base, rel, CONTENIDO.get(clase, "dato falso\n"))
    for rel in CARPETAS.values():
        (base / rel).mkdir(parents=True, exist_ok=True)


def _repo(tmp: Path) -> Path:
    r = tmp / "Bot v3 prueba"
    r.mkdir(parents=True)
    _escribir(r, "Makefile", "x\n")
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _escribir(
        r,
        "knowledge/corpus/fuentes.yaml",
        "videos:\n  - video_id: v6\n    drive_id: null\n  - video_id: v7\n    drive_id: null\n",
    )
    _escribir(
        r,
        "knowledge/corpus/tramos_no_citables.yaml",
        "tramos:\n  - video_id: v6\n    t0: '0:41:00'\n    t1: '0:50:11'\n",
    )
    _escribir(
        r,
        "knowledge/cases/kit/s1/particiones.yaml",
        f"asignacion:\n  {CASO}: holdout-1\ncupos:\n  dev: 0\n",
    )
    _escribir(r, ".claude/hooks/ficheros_con_ocultos.txt", "knowledge/_proposals/pr-v7-x.yaml\n")
    _escribir(r, "src/botsito/cli.py", "x = 1\n")
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    _estructura(r)
    return r


def _union(enlace: Path, destino: Path) -> bool:
    try:
        if EN_WINDOWS:
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(enlace), str(destino)],
                check=True,
                capture_output=True,
            )
        else:
            enlace.symlink_to(destino, target_is_directory=True)
    except (OSError, subprocess.CalledProcessError):
        return False
    return True


def _regla(g: ModuleType, motivo: str | None) -> str:
    if motivo is None:
        return "PERMITIDA"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    return "negada " + (",".join(sorted(nombres)) or "(sin R_)")


def _herramientas(ruta: str, carpeta: bool) -> Iterator[tuple[str, str, dict[str, Any]]]:
    posix = ruta.replace("\\", "/")
    yield "Read", "Read", {"file_path": ruta}
    yield "Grep", "Grep", {"pattern": "x", "path": ruta}
    if carpeta:
        yield "Glob path=carpeta", "Glob", {"pattern": "*", "path": ruta}
        yield "Bash ls", "Bash", {"command": f'ls "{posix}"'}
        yield "PowerShell Get-ChildItem", "PowerShell", {"command": f"Get-ChildItem '{ruta}'"}
        yield "Bash grep -r", "Bash", {"command": f'grep -r x "{posix}"'}
    else:
        yield "Glob patron absoluto", "Glob", {"pattern": posix}
        yield "Bash cat", "Bash", {"command": f'cat "{posix}"'}
        yield "PowerShell Get-Content", "PowerShell", {"command": f"Get-Content '{ruta}'"}


def _decide(g: ModuleType, raiz: Path, herramienta: str, entrada: dict[str, Any]) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(raiz)}
    motivo: str | None = g.decidir(evento, g.Politica(raiz))
    return motivo


def _casos(base: Path) -> Iterator[tuple[str, str, bool]]:
    for clase, rel in FICHEROS.items():
        yield clase, str(base / rel), False
    for clase, rel in CARPETAS.items():
        yield clase, str(base / rel), True


def _medir(g: ModuleType, raiz: Path, forma: str, base: Path) -> None:
    for clase, ruta, carpeta in _casos(base):
        for etiqueta, herramienta, entrada in _herramientas(ruta, carpeta):
            print(f"memoria | {forma} | {clase} | {etiqueta} | {_regla(g, _decide(g, raiz, herramienta, entrada))}")


def test_medida_en_memoria(g: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    repo = _repo(tmp_path)
    # (a) dentro del repo, y (d) las carpetas (en _casos)
    _medir(g, repo, "a/d dentro", repo)
    # (c) una copia con la misma estructura fuera del repo
    copia = tmp_path / "copia de respaldo"
    _estructura(copia)
    _medir(g, repo, "c copia fuera", copia)
    # (c') un clon desechable: la copia lleva tambien el nombre de un repo
    clon = tmp_path / "clon" / "Bot v3"
    _estructura(clon)
    _medir(g, repo, "c clon fuera", clon)
    # (b-sim) corpus/, knowledge/ y data/ como enlaces que apuntan fuera, CON la estructura detras
    fuera = tmp_path / "otro disco"
    real = g._realpath
    mapas = {
        g._normcase(str(repo / "corp" "us")): str(fuera / "corp" "us"),
        g._normcase(str(repo / "knowledge")): str(fuera / "knowledge"),
        g._normcase(str(repo / "data")): str(fuera / "data"),
    }

    def simulado(ruta: str) -> str:
        n = g._normcase(ruta)
        for pre, destino in mapas.items():
            if n == pre or n.startswith(pre + "/"):
                return os.path.normpath(destino + ruta[len(pre) :])
        return str(real(ruta))

    with monkeypatch.context() as m:
        m.setattr(g, "_realpath", simulado)
        _medir(g, repo, "b-sim enlace con estructura", repo)
    # (b-sim2) la carpeta de cada zona como enlace a un nombre SIN la estructura
    mapas2 = {
        g._normcase(str(repo / HOL / "1")): str(fuera / "zz1"),
        g._normcase(str(repo / BTM)): str(fuera / "bm"),
        g._normcase(str(repo / SES)): str(fuera / "ss"),
        g._normcase(str(repo / MAT)): str(fuera / "mat"),
        g._normcase(str(repo / TRA)): str(fuera / "tt"),
    }

    def simulado2(ruta: str) -> str:
        n = g._normcase(ruta)
        for pre, destino in sorted(mapas2.items(), key=lambda kv: -len(kv[0])):
            if n == pre or n.startswith(pre + "/"):
                return os.path.normpath(destino + ruta[len(pre) :])
        return str(real(ruta))

    with monkeypatch.context() as m:
        m.setattr(g, "_realpath", simulado2)
        _medir(g, repo, "b-sim enlace sin estructura", repo)
    # (b-real) una union real: corpus/ del repo -> una copia fuera (como D:\BotsitoCorpus\corpus)
    repo2 = _repo(tmp_path / "r2")
    destino = tmp_path / "r2" / "disco" / "corp" "us"
    destino.parent.mkdir(parents=True)
    os.replace(repo2 / "corp" "us", destino)
    if _union(repo2 / "corp" "us", destino):
        _medir(g, repo2, "b-real union corpus", repo2)
    else:
        print("memoria | b-real union corpus | (no se pudo crear la union)")
    # (b-real2) union de la carpeta holdout/1 y de Backtest marzo a nombres sin estructura
    repo3 = _repo(tmp_path / "r3")
    for rel, nombre in ((f"{HOL}/1", "zz1"), (BTM, "bm")):
        dst = tmp_path / "r3" / "disco" / nombre
        dst.parent.mkdir(parents=True, exist_ok=True)
        os.replace(repo3 / rel, dst)
        if not _union(repo3 / rel, dst):
            print(f"memoria | b-real union sin estructura | (no se pudo crear la union de {nombre})")
    _medir(g, repo3, "b-real union sin estructura", repo3)
    # Lo bueno, fuera: un fichero cualquiera de una carpeta temporal y la carpeta misma
    _escribir(tmp_path, "suelta/nota.txt")
    for etiqueta, herramienta, entrada in _herramientas(str(tmp_path / "suelta" / "nota.txt"), False):
        print(f"memoria | fuera sin anclaje | fichero suelto | {etiqueta} | {_regla(g, _decide(g, repo, herramienta, entrada))}")
    for etiqueta, herramienta, entrada in _herramientas(str(tmp_path / "suelta"), True):
        print(f"memoria | fuera sin anclaje | carpeta suelta | {etiqueta} | {_regla(g, _decide(g, repo, herramienta, entrada))}")
    # Un lector recursivo sobre la carpeta que CONTIENE la copia (no tiene anclaje en su ruta)
    for etiqueta, herramienta, entrada in _herramientas(str(copia), True):
        print(f"memoria | c ancestro de la copia | carpeta de la copia | {etiqueta} | {_regla(g, _decide(g, repo, herramienta, entrada))}")


# ------------------------------------------------------------------------- por stdin, raiz real
def _stdin(herramienta: str, entrada: dict[str, Any]) -> tuple[int, str]:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(RAIZ)}
    p = subprocess.run(
        [sys.executable, str(GUARDIA)],
        input=json.dumps(evento).encode("utf-8"),
        capture_output=True,
        env={**os.environ, "PYTHONUTF8": "1"},
    )
    return p.returncode, p.stderr.decode("utf-8", "replace")


STDIN_FICHEROS = {
    "holdout-1 (la sonda)": f"{HOL}/1/caso-eurusd-2000-01-01.yaml",
    "libro por nombre (backtesting-analytics de marzo)": f"{MAT}/backtesting-analytics MARZO 2026.xlsx",
    "imagen de Backtest marzo (inventada)": f"{BTM}/x.png",
    "otro fichero de Backtest marzo (inventado)": f"{BTM}/notas.txt",
    "hoja de Sesiones (inventada)": f"{SES}/hoja-xx.xlsx",
    "cruda en cuarentena (v7)": f"{TRA}/v7/large-v3/cruda.jsonl",
}
STDIN_CARPETAS = {
    "carpeta holdout/1": f"{HOL}/1",
    "carpeta Backtest marzo": BTM,
    "carpeta Sesiones": SES,
}


def test_medida_por_stdin(g: ModuleType, tmp_path: Path) -> None:
    formas = [("a/d dentro", RAIZ), ("c copia fuera", tmp_path / "copia")]
    _estructura(tmp_path / "copia")
    if EN_WINDOWS:
        formas.append(("D:\\BotsitoCorpus (solo la decision)", Path("D:/BotsitoCorpus")))
    for forma, base in formas:
        for clase, rel, carpeta in [(c, r, False) for c, r in STDIN_FICHEROS.items()] + [
            (c, r, True) for c, r in STDIN_CARPETAS.items()
        ]:
            if forma.startswith("D:") and not rel.startswith("corp"):
                continue
            ruta = str(base / rel)
            for etiqueta, herramienta, entrada in _herramientas(ruta, carpeta):
                if forma.startswith("D:") and herramienta in {"Bash", "PowerShell"} and carpeta:
                    continue  # ls, grep -r y Get-ChildItem de D:, ni simulados
                codigo, err = _stdin(herramienta, entrada)
                decision = "PERMITIDA" if codigo == 0 else _regla(g, err)
                print(f"stdin | {forma} | {clase} | {etiqueta} | {decision}")
    if EN_WINDOWS:  # un lector recursivo sobre la copia de D: entera, solo la decision
        for herramienta, entrada in (("Grep", {"pattern": "x", "path": "D:\\BotsitoCorpus"}),):
            codigo, err = _stdin(herramienta, entrada)
            print(f"stdin | D:\\BotsitoCorpus (solo la decision) | la copia entera | Grep | {'PERMITIDA' if codigo == 0 else _regla(g, err)}")
