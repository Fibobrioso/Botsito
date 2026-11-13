"""FASE 0 de `trabajo/guardia-falsos-positivos` (2026-11-12): lo que decide hoy la guardia.

MEDIDA, no tests de la condicion: la fase 0 no toca la guardia (encargo, punto 5). Como en
`trabajo/guardia-g1` (D4): EN MEMORIA, con `decidir()`, sobre un repo INVENTADO en `tmp_path` con
ficheros FALSOS donde el material protegido; las rutas protegidas a trozos y la salida sin ninguna
entera (`_sin_rutas`). Corre desde `tests/` porque la guardia niega ejecutar suelto un guion que
monta rutas protegidas a trozos (`medir_g1.py`, su cabecera).

Por caso imprime tres decisiones: la de HOY; la de HOY con D1 SIMULADO (`_literales` sin los que
empiezan por dos separadores y un espacio o un tabulador: lo que no llega a `_absoluta`); y con D1
y D2 simulados (`cmp` en `NO_EJECUTAN`). La simulacion no cambia `guardia.py`: es un `monkeypatch`.
Y el tiempo de `decidir()` de cada caso (D6).

Tras la respuesta del consultor este fichero pasa a tener los tests de la rama.
"""

from __future__ import annotations

import importlib.util
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
GENERAR_CAPA = RAIZ / "src" / "botsito" / "mql5bridge" / "generar_capa.py"

HOL = "hol" + "dout"
KC = "knowledge/cases"
SECRETO = f"{KC}/{HOL}/1/secreto.yaml"
B = "\\"


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


def _escribir(repo: Path, rel: str, texto: str = "x\n") -> Path:
    ruta = repo.joinpath(*rel.split("/"))
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")
    return ruta


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    r = tmp_path / "repo"
    _escribir(
        r, f"{KC}/kit/s1/particiones.yaml", "asignacion:\n  caso-eurusd-2026-05-04: holdout-1\n"
    )
    _escribir(r, "knowledge/corpus/fuentes.yaml", "videos:\n  - video_id: v7\n    drive_id: null\n")
    for rel in (f"{KC}/{HOL}/README.md", f"{KC}/{HOL}/1/README.md", SECRETO, f"{KC}/dev/c.yaml",
                "docs/a.md", "docs/b.md", "PROJECT_STATE.md", "Makefile"):  # fmt: skip
        _escribir(r, rel)
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    # Ficheros NUEVOS de la rama (no estan en main): los de docs/ que compara cmp, y el de G.6.
    for rel in ("docs/n1.md", "docs/n2.md", "diaria.DIAGNOSTICO.cuenta=diaria.txt", "otra.txt"):
        _escribir(r, rel)
    return r


def _casos(repo: Path) -> list[tuple[str, str, str, tuple[str, str] | None]]:
    """(id, grupo, comando, guion nuevo a escribir o None). Un caso de guion se lanza con
    `uv run python <guion>`; el guion es nuevo en la rama (no esta en main)."""
    r = repo.as_posix()
    rw = str(repo)
    raiz_unc = rw[0] + "$" + rw[2:]  # `C$\...`: la raiz como recurso de la propia maquina
    sec_inv = SECRETO.replace("/", B)
    capa = GENERAR_CAPA.read_text(encoding="utf-8") + "# cambiado en la rama\n"
    lit364 = (
        "// CAPA_HASH = SHA-256 de este fichero sin su linea (docs/validation/CAPA-GENERADA.md)."
    )
    lit359 = "//   uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil "

    def unc(blanco: str, equipo: str, cola: str = "") -> str:
        return B * 2 + blanco + equipo + B + raiz_unc + (B + cola if cola else "")

    def lista(literal: str) -> str:
        return f"L = [{literal!r}]\nprint(L)\n"

    def abre(expresion: str) -> str:
        return f"print(open({expresion}).read())\n"

    recorre = "from pathlib import Path\nprint(list(Path({!r}).rglob('*')))\n"
    guiones: list[tuple[str, str, str]] = [
        # F1: el literal real y sus hermanos
        ("f1-literal-364", "F1", lista(lit364)),
        ("f1-literal-359-fcadena", "F1", f"p = 'x'\nL = [f{lit359 + '{p}'!r}]\nprint(L)\n"),
        ("f1-tabulador", "F1", lista("//\tx docs/a/b.md")),
        ("f1-barras-invertidas", "F1", lista(B * 2 + " x docs" + B + "a" + B + "b.md")),
        ("f1-mql5-pipe", "F1", lista("//| Generado.mqh - lo que la capa de MT5 recibe (R6a.2, |")),
        ("f1-mql5-pipe-con-barras", "F1", lista("//| ver docs/validation/X.md |")),
        ("f1-mql5-mas", "F1", lista("//+----------+")),
        # D3: lo que hoy se niega y tiene que seguir negado
        ("d3-host-share-barras", "D3", abre(repr("//host/share/x/y.txt"))),
        ("d3-host-share-invertidas", "D3", abre(repr(B * 2 + "host" + B + "share" + B + "y.txt"))),
        ("d3-recorre-protegida", "D3", recorre.format(f"{KC}/{HOL}")),
        ("d3-nombra-protegido", "D3", abre(repr(SECRETO))),
        # Posibles huecos de D1: hoy y con D1 simulado
        ("h1-recorte", "hueco", abre(repr("// " + SECRETO) + "[3:]")),
        ("h1b-recorte-control", "hueco", abre(repr("x" + SECRETO) + "[1:]")),
        ("h1c-recorte-blanco-interior", "hueco", abre(repr("// a b/" + SECRETO) + "[6:]")),
        ("h2-lstrip", "hueco", abre(repr("// " + SECRETO) + ".lstrip('/ ')")),
        ("h3-puntopunto", "hueco", abre(repr(f"// x/../{r.lstrip('/')}/{SECRETO}"))),
        ("h4-espacio-localhost", "hueco", abre(repr(unc(" ", "localhost", sec_inv)))),
        ("h5-tab-localhost", "hueco", abre(repr(unc("\t", "localhost", sec_inv)))),
        ("h6-espacio-equipo", "hueco", abre(repr(unc(" ", socket.gethostname(), sec_inv)))),
        # El residuo de una variante: la raiz entera por un literal de D1, recorrida o no
        ("h7-espacio-localhost-raiz-recorre", "hueco", recorre.format(unc(" ", "localhost"))),
        (
            "h8-espacio-localhost-raiz-sin-recorrer",
            "hueco",
            f"import os\nprint(os.stat({unc(' ', 'localhost')!r}))\n",
        ),
    ]
    capa_rel = "src/botsito/mql5bridge/generar_capa.py"
    c: list[tuple[str, str, str, tuple[str, str] | None]] = [
        (
            "f1-copia-generar-capa",
            "F1",
            f"uv run python {capa_rel} --repo . --perfil p",
            (capa_rel, capa),
        ),
    ]
    c += [(i, gr, f"uv run python t/{i}.py", (f"t/{i}.py", codigo)) for i, gr, codigo in guiones]
    c += [
        # F2: cmp, y diff de control
        ("f2-cmp-docs-nuevos", "F2", "cmp docs/n1.md docs/n2.md", None),
        ("f2-cmp-s-docs-nuevos", "F2", "cmp -s docs/n1.md docs/n2.md", None),
        ("f2-cmp-docs-de-main", "F2", "cmp docs/a.md docs/b.md", None),
        ("f2-cmp-origen-g6", "F2", "cmp diaria.DIAGNOSTICO.cuenta=diaria.txt otra.txt", None),
        ("f2-cmp-protegido-segundo", "F2", f"cmp docs/a.md {SECRETO}", None),
        ("f2-cmp-protegido-primero", "F2", f"cmp {SECRETO} docs/n1.md", None),
        ("f2-cmp-protegido-absoluto", "F2", f"cmp docs/n1.md '{r}/{SECRETO}'", None),
        ("c-diff-docs-nuevos", "diff", "diff docs/n1.md docs/n2.md", None),
        ("c-diff-q-docs-nuevos", "diff", "diff -q docs/n1.md docs/n2.md", None),
        ("c-diff-protegido", "diff", f"diff docs/a.md {SECRETO}", None),
        ("c-diff-protegido-primero", "diff", f"diff {SECRETO} docs/n1.md", None),
    ]
    return c


def _es_d1(lit: str) -> bool:
    return re.match(r"[\\/]{2}[ \t]", lit) is not None


def _con_d1(
    g: ModuleType, monkeypatch: pytest.MonkeyPatch, variante: str = "D1", base: str = ""
) -> None:
    """D1 tal cual (`D1`); con la clausula de SENSIBLES (`D1a`: un literal de D1 que lleva un
    fragmento sensible se sigue mirando como ruta); y ademas sin recorrido (`D1b`); con la del
    blanco interior (`D1c`); y con las dos, la de SENSIBLES y la del blanco (`D1d`). `base` (el
    directorio temporal, sin unidad) se quita ANTES de buscar el fragmento: el de pytest en Windows
    lleva `AppData\\`, que casa con `data\\`, y la raiz del repo real no lleva ninguno."""
    original = g._literales

    def literales(codigo: str, es_python: bool) -> list[str]:
        recorre = g.CODIGO_QUE_RECORRE.search(codigo) is not None
        salida = []
        for lit in original(codigo, es_python):
            fuera = _es_d1(lit)
            if fuera and variante in {"D1a", "D1b", "D1d"}:
                texto = lit.lower().replace(base.lower(), "") if base else lit.lower()
                fuera = not any(s in texto for s in g.SENSIBLES)
            if fuera and variante == "D1b":
                fuera = not recorre
            if fuera and variante in {"D1c", "D1d"}:
                # el tramo hasta el siguiente separador, sin los blancos del principio, lleva un
                # blanco: no puede ser el nombre de una maquina
                tramo = re.split(r"[\\/]", lit[2:], maxsplit=1)[0].lstrip(" \t")
                fuera = re.search(r"[ \t]", tramo) is not None
            if not fuera:
                salida.append(lit)
        return salida

    monkeypatch.setattr(g, "_literales", literales)


def _sin_rutas(texto: str, repo: Path) -> str:
    for base in (str(repo.parent), repo.parent.as_posix(), str(repo.parent)[2:]):
        texto = texto.replace(base, "<tmp>")
    texto = texto.replace(socket.gethostname(), "<equipo>")
    return texto.replace(f"{KC}/{HOL}", "<holdout>").replace(
        f"{KC}{B}{HOL}".replace("/", B), "<holdout>"
    )


def _decide(g: ModuleType, repo: Path, comando: str) -> tuple[str, float]:
    evento: dict[str, Any] = {
        "tool_name": "Bash",
        "tool_input": {"command": comando},
        "cwd": str(repo),
    }
    t = time.perf_counter()
    motivo = g.decidir(evento, g.Politica(repo))
    s = time.perf_counter() - t
    if motivo is None:
        return "PASA", s
    return "NIEGA: " + motivo.splitlines()[0][:150], s


def test_fase0_tabla(g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    casos = _casos(repo)
    for _, _, _, guion in casos:
        if guion:
            _escribir(repo, *guion)
    print(f"\nFASE0 | plataforma: os.name={os.name}")
    filas = []
    for ident, grupo, comando, _ in casos:
        hoy, t0 = _decide(g, repo, comando)
        with monkeypatch.context() as m:
            _con_d1(g, m)
            d1, t1 = _decide(g, repo, comando)
            m.setitem(g.NO_EJECUTAN, "cmp", "fase 0: simulado")
            d12, t2 = _decide(g, repo, comando)
        variantes = {}
        for v in ("D1a", "D1b", "D1c", "D1d"):
            with monkeypatch.context() as m:
                _con_d1(g, m, v, str(repo.parent)[2:])
                m.setitem(g.NO_EJECUTAN, "cmp", "fase 0: simulado")
                variantes[v] = _decide(g, repo, comando)
        filas.append(ident)
        print(f"FASE0 | {grupo} | {ident} | hoy: {_sin_rutas(hoy, repo)} | {t0:.2f}s")
        print(f"FASE0 |   | {ident} | con D1: {_sin_rutas(d1, repo)} | {t1:.2f}s")
        print(f"FASE0 |   | {ident} | con D1+D2: {_sin_rutas(d12, repo)} | {t2:.2f}s")
        for v, (d, t) in variantes.items():
            print(f"FASE0 |   | {ident} | con {v}+D2: {_sin_rutas(d, repo)} | {t:.2f}s")
    assert len(filas) == len(casos)
