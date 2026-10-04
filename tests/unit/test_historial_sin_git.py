"""Sin historial evaluado, `knowledge validate` no dice «intacto» (trabajo/historial-sin-git).

Encargo del consultor del 2026-10-03 (docs/encargos/trabajo-historial-sin-git.md): toda
comprobacion cuyo resultado depende del historial de git, cuando ese historial no se evaluo -sin
git, o con git y `historial_evaluable` diciendo que no se puede-, no afirma nada: dice que NO se
comprobo y por que. El inventario de las nueve, en docs/validation/HISTORIAL-SIN-GIT.md §0.2.
"""

from __future__ import annotations

import ast
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from botsito.validation import knowledge
from botsito.validation.knowledge import Historial, afirmaciones_sueltas, validar
from tests.unit.test_kit import _sin_holdout

REPO = Path(__file__).resolve().parents[2]

# Las nueve comprobaciones del inventario (HISTORIAL-SIN-GIT.md §0.2), por el ambito de su aviso.
AMBITOS = (
    "libros",
    "retirados",
    "evidencia",
    "feedback",
    "trailers Fuente",
    "manifiestos de datos",
    "transcripciones",
    "fotogramas",
    "ambiguedades",
)

# Las lineas OK de `validar` sobre el repositorio real, con git, tal como salen en `main`
# (48ccbd2): en orden, y con los recuentos como \d+.
OK_CON_GIT = (
    r"OK: registro con \d+ parametros \(\d+ sin confirmar\)",
    r"OK: manifiesto del corpus coherente con \d+ videos esperados",
    r"OK: \d+ libros declarados con formato y huso, solo-anadir intacto, cruzados con "
    r"cobertura_material",
    r"OK: \d+ dias retirados del holdout, cada uno de un reservado, solo-anadir intacto",
    r"OK: \d+ documentos: todo id citado existe o esta declarado con motivo",
    r"OK: \d+ transcripciones registradas, historial intacto",
    r"OK: \d+ extracciones de fotogramas registradas, obligatorios presentes, historial intacto",
    r"OK: \d+ manifiestos de datos validos, historial intacto",
    r"OK: \d+ reglas de spec \(\d+ vigentes, \d+ con forma ejecutable\), \d+ terminos de "
    r"glosario, hash del manifiesto al dia",
    r"OK: \d+ ambiguedades registradas; \d+ paquetes de sesion validos, particiones anteriores al "
    r"etiquetado; \d+ artefactos de fidelidad; \d+ repartos dev-visto",
    r"OK: \d+ registros de feedback, historial intacto, commits con Fuente",
    r"OK: \d+ items de evidencia, \d+ contradicciones abiertas, historial intacto; \d+ propuestas "
    r"\(\d+ items pendientes\)",
)


def _copia(destino: Path) -> Path:
    """La copia sin `.git` de `test_kit.py` -knowledge, docs y config, sin el holdout- mas
    `data/manifests/`: sin ellos el kit sale con 1 antes de feedback y evidencia (§0.1)."""
    destino.mkdir(parents=True)
    for carpeta in ("knowledge", "docs", "config"):
        shutil.copytree(REPO / carpeta, destino / carpeta, ignore=_sin_holdout)
    shutil.copytree(REPO / "data" / "manifests", destino / "data" / "manifests")
    return destino


def _avisos(salida: list[str]) -> dict[str, list[str]]:
    return {
        a: [x for x in salida if x.startswith(f"AVISO: {a}: ") and ", NO se comprobo " in x]
        for a in AMBITOS
    }


# ------------------------------------------------------------------------- 1. sin git


def test_sin_git_ninguna_linea_dice_intacto_y_cada_comprobacion_avisa(tmp_path: Path) -> None:
    codigo, salida = validar(_copia(tmp_path / "copia"))
    assert not [x for x in salida if "intacto" in x], salida
    assert not [x for x in salida if "commits con Fuente" in x], salida
    avisos = _avisos(salida)
    assert {a: len(v) for a, v in avisos.items()} == dict.fromkeys(AMBITOS, 1), avisos
    assert all("sin git, NO se comprobo" in v[0] for v in avisos.values()), avisos
    # y lo que si comprobo, lo sigue diciendo
    assert any(re.fullmatch(r"OK: \d+ transcripciones registradas", x) for x in salida), salida
    assert codigo == 0, salida  # el de main sobre esta copia (§0.1): lo nuevo son avisos


# ------------------------------------------------- 2. el mecanismo comun, negar por defecto


def test_una_afirmacion_de_historial_que_no_pasa_por_historial_hace_fallar_validar(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Una comprobacion de historial falsa que imprime «intacto» sin pasar por `Historial`."""
    original = knowledge._validar

    def con_una_falsa(repo: Path, puerta: Historial) -> tuple[int, list[str]]:
        codigo, salida = original(repo, puerta)
        return codigo, [*salida, "OK: 3 ficheros nuevos, historial intacto"]

    monkeypatch.setattr(knowledge, "_validar", con_una_falsa)
    codigo, salida = validar(_copia(tmp_path / "copia"))
    assert codigo == 1
    assert salida[-1].startswith("ERROR: validar: ") and "historial intacto" in salida[-1]


def test_afirmaciones_sueltas() -> None:
    con = "OK: 3 libros, solo-anadir intacto"
    assert afirmaciones_sueltas([con, "OK: 2 cosas"], [con]) == []
    assert afirmaciones_sueltas(["OK: 3 libros, solo-anadir intacto"], []) == [con]
    assert afirmaciones_sueltas(["OK: 4 registros, commits con Fuente"], []) != []
    # un AVISO o un ERROR no afirman nada
    assert afirmaciones_sueltas(["AVISO: x intacto", "ERROR: y intacto"], []) == []


def _literales_sueltos(fuente: str) -> list[str]:
    """Los literales de `fuente` con una afirmacion de historial que no van dentro de una
    llamada a `.ok(...)` ni son un docstring ni la propia tupla `AFIRMACIONES_DE_HISTORIAL`."""
    arbol = ast.parse(fuente)
    permitidos: set[int] = set()
    for nodo in ast.walk(arbol):
        dentro = (
            isinstance(nodo, ast.Call)
            and isinstance(nodo.func, ast.Attribute)
            and nodo.func.attr == "ok"
        ) or (
            isinstance(nodo, ast.Assign)
            and any(
                isinstance(t, ast.Name) and t.id == "AFIRMACIONES_DE_HISTORIAL"
                for t in nodo.targets
            )
        )
        dentro = dentro or (isinstance(nodo, ast.Expr) and isinstance(nodo.value, ast.Constant))
        if dentro:
            permitidos |= {id(n) for n in ast.walk(nodo)}
    sueltos = []
    for nodo in ast.walk(arbol):
        if id(nodo) in permitidos:
            continue
        if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
            texto = nodo.value
            if any(a in texto for a in knowledge.AFIRMACIONES_DE_HISTORIAL):
                sueltos.append(f"l. {nodo.lineno}: {texto!r}")
    return sueltos


def test_ningun_literal_de_src_afirma_historial_fuera_de_historial_ok() -> None:
    sueltos = {
        str(f.relative_to(REPO)): s
        for f in sorted((REPO / "src" / "botsito").rglob("*.py"))
        if (s := _literales_sueltos(f.read_text(encoding="utf-8")))
    }
    assert sueltos == {}
    # y el detector no es mudo: una comprobacion falsa que lo escribe a mano, la ve
    falsa = 'def f(salida):\n    salida.append(f"OK: {3} ficheros, historial intacto")\n'
    assert _literales_sueltos(falsa) != []
    pasa = 'def f(h, salida):\n    salida += h.ok(f"OK: {3}, historial intacto", "OK: 3")\n'
    assert _literales_sueltos(pasa) == []


# ----------------------------------------------------------------- 3. con git, como en main


@pytest.mark.skipif(not (REPO / ".git").exists(), reason="sin el .git del repositorio")
def test_con_git_las_lineas_ok_son_las_de_main() -> None:
    codigo, salida = validar(REPO)
    assert codigo == 0, [x for x in salida if x.startswith("ERROR")]
    oks = [x for x in salida if x.startswith("OK:")]
    assert len(oks) == len(OK_CON_GIT), oks
    for linea, patron in zip(oks, OK_CON_GIT, strict=True):
        assert re.fullmatch(patron, linea), (linea, patron)
    assert not [x for x in salida if "NO se comprobo" in x], salida


# ------------------------------------------ 4. con git y el historial no evaluable


def test_con_git_y_el_proyecto_fuera_de_la_raiz_tampoco_dice_intacto(tmp_path: Path) -> None:
    raiz = tmp_path / "raiz"
    proyecto = _copia(raiz / "proyecto")
    (raiz / "LEEME").write_text("x\n", encoding="utf-8")
    for args in (
        ["init", "-q"],
        ["add", "LEEME"],
        ["-c", "user.email=a@b", "-c", "user.name=x", "commit", "-qm", "x"],
    ):
        subprocess.run(["git", *args], cwd=raiz, check=True, capture_output=True)
    codigo, salida = validar(proyecto)
    assert codigo == 1  # como en main: la guardia de evidencia da ERROR
    assert any("la guardia de historial de evidencia no se pudo evaluar" in x for x in salida)
    assert not [x for x in salida if "intacto" in x], salida
    avisos = _avisos(salida)
    for a in ("libros", "retirados"):
        assert len(avisos[a]) == 1, avisos
        assert "el proyecto no es la raiz del repositorio git" in avisos[a][0], avisos[a]


# ------------------ 5. la condicion, no las palabras: quien lee git (segunda orden)

VALIDATION = REPO / "src" / "botsito" / "validation"
PRIMITIVAS = "botsito.comun.historial"
# Lo que puede leer git en validation/ fuera de `Historial`, cada cosa con su porque en un
# comentario: `(fichero, nombre importado)`. Ninguna hoy (HISTORIAL-SIN-GIT.md §6.1).
EXCEPCIONES: dict[tuple[str, str], str] = {}


def _lecturas_de_git_fuera_de_historial(fuente: str, fichero: str) -> list[str]:
    """Lo que `fuente` importa para leer git fuera de la clase `Historial`: una funcion de
    `botsito.comun.historial` (sus CONSTANTES si se pueden importar fuera), el modulo entero, o
    `subprocess` (git a mano)."""
    arbol = ast.parse(fuente)
    dentro: set[int] = set()
    for nodo in ast.walk(arbol):
        if isinstance(nodo, ast.ClassDef) and nodo.name == "Historial":
            dentro |= {id(n) for n in ast.walk(nodo)}
    fuera: list[str] = []
    for nodo in ast.walk(arbol):
        if not isinstance(nodo, (ast.Import, ast.ImportFrom)) or id(nodo) in dentro:
            continue
        nombres: list[str] = []
        if isinstance(nodo, ast.ImportFrom) and nodo.module == PRIMITIVAS:
            nombres = [a.name for a in nodo.names if not a.name.isupper()]
        elif isinstance(nodo, ast.ImportFrom) and nodo.module == "botsito.comun":
            nombres = [a.name for a in nodo.names if a.name == "historial"]
        elif isinstance(nodo, ast.ImportFrom) and nodo.module == "subprocess":
            nombres = ["subprocess"]
        elif isinstance(nodo, ast.Import):
            nombres = [a.name for a in nodo.names if a.name in (PRIMITIVAS, "subprocess")]
        fuera += [
            f"{fichero}:{nodo.lineno}: {n}" for n in nombres if (fichero, n) not in EXCEPCIONES
        ]
    return fuera


def test_en_validation_solo_historial_lee_git() -> None:
    fuera = [
        x
        for f in sorted(VALIDATION.glob("*.py"))
        for x in _lecturas_de_git_fuera_de_historial(f.read_text(encoding="utf-8"), f.name)
    ]
    assert fuera == []
    # y el detector no es mudo: una comprobacion falsa que llama a una primitiva directamente
    falsa = (
        "def comprobar(repo):\n"
        "    from botsito.comun.historial import DIRECTORIO_FEEDBACK, modificaciones_en_historial\n"
        "    return modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK)\n"
    )
    assert _lecturas_de_git_fuera_de_historial(falsa, "f.py") == [
        "f.py:2: modificaciones_en_historial"
    ]
    assert _lecturas_de_git_fuera_de_historial("import subprocess\n", "f.py") != []
    dentro = (
        "class Historial:\n"
        "    def lee(self, repo):\n"
        "        from botsito.comun.historial import resolver\n"
        "        return resolver(repo, 'HEAD')\n"
    )
    assert _lecturas_de_git_fuera_de_historial(dentro, "f.py") == []
