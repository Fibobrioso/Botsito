"""K, el resto de G.1, B y C: la guardia deja lo legitimo y niega lo que se le escapaba.

Rama `trabajo/guardia-g1` (2026-11-04, docs/validation/GUARDIA-G1.md), con la respuesta del
consultor a la PARADA de la fase 0. Un test por punto de la fase 1, en el orden del encargo:

- e) listar los nombres de dentro de `knowledge/cases/holdout/{1,2,3}` se niega; se cuenta, no se
  imprime (ADR-0088);
- a) la opcion que pide el corpus sin filtrar se reconoce por su FORMA en el arbol de Python, no
  por la palabra: una variable con ese nombre pasa (K1);
- b) un test de un clon `git worktree add --detach` de ESTE repo (comparar-con-main, `C:/cm/`) que
  es el de `main` o el del arbol del repo real cuenta como el test del repo (K2);
- c) la constante `\\.` de un test del clon, que en Windows es la raiz de la unidad, pasa por b
  (K3);
- d) lo que sale de partir un argumento por `=` no es una ruta si queda en blanco (K4);
- f) `solo_lectura.py` salta las opciones globales de git; `which`, `rmdir` y `PYTHONIOENCODING`
  entran en sus listas cerradas; lo encadenado y `git -c` siguen como estaban (decididos);
- g) fase 2, B: lo que un guion de Python importa o ejecuta se resuelve y se lee (hasta 3
  niveles), y lo que no se resuelve se niega;
- h) fase 2, C: una ruta compuesta se calcula y se mira como un literal, y la que no se calcula se
  niega si nombra un fragmento sensible; las llaves de bash se expanden y `file:` es su ruta;
- y la comparacion caso a caso con la guardia de `main` (`anexos/GUARDIA-G1/medir_g1.py`).

Todo EN MEMORIA, con `decidir`, sobre un repo INVENTADO en `tmp_path` con ficheros FALSOS donde el
material protegido: nada se ejecuta ni se abre del repo real. Lo que es de Windows (`\\.` como la
raiz de la unidad) se SIMULA cambiando `_absoluta`, como `_romper` de `test_guardia_alias.py`
cambia `_canonica` (fase 0, §1.c).

ROTO A PROPOSITO, en los dos sentidos: `test_roto_a_proposito` cambia una pieza de la guardia
(`_romper`: quitandola, o haciendola negar o aceptar de mas) y exige que los tests que esa pieza
sostiene FALLEN; imprime su fallo, que va al anexo de la rama.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
SOLO_LECTURA = RAIZ / ".claude" / "hooks" / "solo_lectura.py"

# Las rutas protegidas, a trozos (no se escriben enteras), como en los otros tests de la guardia.
HOL = "hol" + "dout"
KC = "knowledge/cases"
CASO_RESERVADO = "caso-eurusd-2026-05-04"
SECRETO = f"{KC}/{HOL}/1/secreto.yaml"
MAT = "corp" + "us/Estrategia del trader/Material adicional de su operativa"
OPC = "cru" + "do"  # el nombre de la opcion
RECORRE = "gl" + "ob("

TEST_RECORRE = (
    "from pathlib import Path\n"
    "def test_x():\n"
    f"    assert 'caso-{HOL}' not in [p.name for p in Path(__file__).parent.{RECORRE}'*.py')]\n"
)
TEST_BARRA = (
    "from pathlib import Path\n"
    f"def test_x():\n    assert Path('/').is_dir() and list(Path(__file__).parent.{RECORRE}'*'))\n"
)
TEST_REGEX = (
    "import re\nfrom pathlib import Path\nSEP = '\\\\.'\n"
    "def test_x():\n"
    f"    assert re.compile(f'a{{SEP}}b') and list(Path(__file__).parent.{RECORRE}'*'))\n"
)
TEST_OPCION = f"def test_x():\n    assert dict({OPC}=True)\n"


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


@pytest.fixture(scope="module")
def s() -> ModuleType:
    nombre = "solo_lectura"  # el mismo que `test_revisor.py`
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SOLO_LECTURA)
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
    """El repo inventado de la fase 0 (`anexos/GUARDIA-G1/medir_g1.py`), y el clon de
    comparar-con-main en `tmp_path/cm/main`, fuera de el."""
    r = tmp_path / "repo"
    _escribir(
        r,
        f"{KC}/kit/s1/particiones.yaml",
        f"asignacion:\n  {CASO_RESERVADO}: holdout-1\n  caso-eurusd-2026-05-06: dev\n",
    )
    _escribir(
        r,
        "knowledge/corpus/fuentes.yaml",
        "videos:\n  - video_id: v1\n    drive_id: abc\n  - video_id: v7\n    drive_id: null\n",
    )
    for rel in (
        f"{MAT}/backtesting-analytics ABRIL 2026.xlsx",
        f"{MAT}/WhatsApp Image 2026-09-03.jpeg",
        f"{KC}/{HOL}/README.md",
        f"{KC}/{HOL}/1/README.md",
        SECRETO,
        f"{KC}/dev/caso-eurusd-2026-04-01.yaml",
        "knowledge/cuentas/ftmo.yaml",
        "src/botsito/x.py",
        "src/botsito/engine/perfil_cuenta.py",
        "scripts/de_main.py",
        "docs/a.md",
        "PROJECT_STATE.md",
        "Makefile",
    ):
        _escribir(r, rel)
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _escribir(r, "tests/unit/test_recorre.py", TEST_RECORRE)
    _escribir(r, "tests/unit/test_barra.py", TEST_BARRA)
    _escribir(r, "tests/unit/test_regex.py", TEST_REGEX)
    _escribir(r, "tests/unit/test_opcion.py", TEST_OPCION)
    _escribir(r, "herramientas/test_fuera.py", TEST_RECORRE)  # igual que en main, fuera de tests/
    _escribir(
        r, "scripts/leer_demo.py", "def leer(ruta):\n    x = ruta.read_bytes()\n    return x\n"
    )
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    clon = tmp_path / "cm" / "main"
    clon.parent.mkdir(parents=True)
    _git(r, "worktree", "add", "-q", "--detach", str(clon), "main")
    # El test NUEVO de la rama, copiado al clon (el uso de comparar-con-main), y uno CAMBIADO.
    nuevo = TEST_RECORRE.replace("test_x", "test_y")
    _escribir(r, "tests/unit/test_nuevo.py", nuevo)
    _escribir(clon, "tests/unit/test_nuevo.py", nuevo)
    _escribir(clon, "tests/unit/test_cambiado.py", TEST_RECORRE + "# cambiado\n")
    _escribir(clon, "tests/unit/test_regex_cambiado.py", TEST_REGEX + "# cambiado\n")
    # Otro repositorio con el mismo test, que NO es un worktree de este.
    otro = tmp_path / "otro"
    _escribir(otro, "tests/unit/test_recorre.py", TEST_RECORRE)
    _git(otro, "init", "-q", "-b", "main")
    return r


def _clon(repo: Path) -> str:
    return (repo.parent / "cm" / "main").as_posix()


def _otro(repo: Path) -> str:
    return (repo.parent / "otro").as_posix()


def _decide(g: ModuleType, repo: Path, herramienta: str, **entrada: Any) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(repo)}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _bash(g: ModuleType, repo: Path, comando: str) -> str | None:
    return _decide(g, repo, "Bash", command=comando)


def _escribe_guion(repo: Path, nombre: str, codigo: str) -> str:
    _escribir(repo, nombre, codigo)
    return f"uv run python {nombre}"


# --------------------------------------------------------------------- e) listar el holdout
LISTADOS_DEL_HOLDOUT = [
    f"git ls-files {KC} | grep -v {HOL}",  # el de las cuatro ramas (ERRORES-RECURRENTES)
    f"git ls-files {KC}",
    "git ls-files | grep caso",  # sin rutas: todo el repo
    "git ls-files '*.yaml'",  # una ruta de git con comodin alcanza cualquier carpeta
    "git -C knowledge ls-files cases",
    f"git ls-files {KC} > lista.txt",  # a un fichero: los nombres siguen saliendo
    f"ls -R {KC}",
    "ls -laR knowledge",
    f"ls {KC}/{HOL}/1",
    f"ls {KC}/{HOL}/1/",
    f"find {KC} -name '*.yaml'",
    "find . -name '*.py'",
    "find knowledge",
    f"git ls-tree -r --name-only HEAD {KC}",
    "git ls-tree -r HEAD",
    f"git ls-tree --name-only HEAD {KC}/{HOL}/1/",
    f"git ls-tree -r HEAD:{KC}",
    "tree knowledge",
    "tree",
    f"du -a {KC}",
    f"du {KC}",
    f"sha256sum {KC}/{HOL}/1/*",  # el glob imprime los nombres
    f"echo {KC}/{HOL}/*/*",
    f"cd {KC} && ls -R",
]


@pytest.mark.parametrize("comando", LISTADOS_DEL_HOLDOUT)
def test_e_los_listados_del_holdout_se_niegan(g: ModuleType, repo: Path, comando: str) -> None:
    motivo = _bash(g, repo, comando)
    assert motivo is not None, comando
    assert "ADR-0088" in motivo, motivo


def test_e_el_glob_que_alcanza_el_holdout_se_niega(g: ModuleType, repo: Path) -> None:
    for entrada in (
        {"pattern": f"{KC}/**/*.yaml"},
        {"pattern": "**/*.yaml", "path": KC},
        {"pattern": "**/*"},
        {"pattern": "*", "path": f"{KC}/{HOL}/1"},
        {"pattern": f"{KC}/{HOL}/*/*"},
        {"pattern": f"{KC}/{{{HOL},dev}}/**"},
    ):
        motivo = _decide(g, repo, "Glob", **entrada)
        assert motivo is not None and "ADR-0088" in motivo, entrada


def test_e_powershell_que_lista_el_holdout_se_niega(g: ModuleType, repo: Path) -> None:
    for comando in (
        f"Get-ChildItem -Recurse {KC}",
        f"Get-ChildItem {KC}/{HOL}/1",
        f"Get-ChildItem -r {KC}",  # la abreviatura (`gci -r` ya lo niega main como ejecucion)
        "Get-ChildItem -Recurse knowledge",  # `dir -Recurse` ya lo niega main como ejecucion
        f"Get-ChildItem -Path {KC}/{HOL}/1 -Name",  # `ls`, `dir` y `gci` ya los niega main
    ):
        motivo = _decide(g, repo, "PowerShell", command=comando)
        assert motivo is not None and "ADR-0088" in motivo, comando


RECUENTOS_Y_LITERALES = [
    f"git ls-files {KC}/{HOL} | wc -l",  # el recuento
    f"git ls-files {KC} | grep -v {HOL} | wc -l",
    f"git ls-files {KC} | grep -c caso",
    f"find {KC} -name '*.yaml' | wc -l",
    f"git ls-files {KC}/dev {KC}/kit",  # rutas literales que no lo contienen
    f"ls {KC}",  # no recursivos: nombran `holdout`, no lo de dentro
    f"ls -la {KC}/{HOL}",
    f"git ls-tree --name-only HEAD {KC}/{HOL}/",
    "git ls-tree HEAD",
    "git ls-files src docs",
    "find src -name '*.py'",
    "ls -R docs",
    f"du -sh {KC}",
    f"stat {KC}/{HOL}/1/README.md",  # medir un fichero NOMBRADO
    f"sha256sum {SECRETO}",
    "tree docs",
    "uv run botsito corpus inventory",
]


@pytest.mark.parametrize("comando", RECUENTOS_Y_LITERALES)
def test_e_el_recuento_y_lo_literal_pasan(g: ModuleType, repo: Path, comando: str) -> None:
    assert _bash(g, repo, comando) is None, comando


def test_e_glob_y_powershell_que_no_alcanzan_el_holdout_pasan(g: ModuleType, repo: Path) -> None:
    for entrada in ({"pattern": "**/*.py"}, {"pattern": "docs/*.md"}, {"pattern": f"{KC}/dev/*"}):
        assert _decide(g, repo, "Glob", **entrada) is None, entrada
    for comando in ("Get-ChildItem docs", f"Get-ChildItem {KC}", "Get-ChildItem -Recurse src"):
        assert _decide(g, repo, "PowerShell", command=comando) is None, comando


# -------------------------------------------------------------- a) la forma de la opcion (K1)
FORMAS_DE_LA_OPCION = {
    "dict": f"d = {{'{OPC}': 1}}\nprint(d)\n",
    "argumento": f"def f(**k):\n    return k\nprint(f({OPC}=True))\n",
    "argumento_none": f"def f(**k):\n    return k\nprint(f({OPC}=None))\n",
    "atributo": f"class A:\n    pass\na = A()\na.{OPC} = True\n",
    "expandido": f"def f(**k):\n    return k\nprint(f(**{{'{OPC}': True}}))\n",
    "subindice": f"k = {{}}\nk['{OPC}'] = True\n",
    "setattr": f"class A:\n    pass\nsetattr(A(), '{OPC}', 1)\n",
    "sin_parsear": f"def f(:\n    {OPC} = 1\n",  # no se parsea: el regex de antes
}


@pytest.mark.parametrize("forma", sorted(FORMAS_DE_LA_OPCION))
def test_a_la_forma_de_la_opcion_en_python_se_niega(g: ModuleType, repo: Path, forma: str) -> None:
    motivo = _bash(g, repo, _escribe_guion(repo, f"k1_{forma}.py", FORMAS_DE_LA_OPCION[forma]))
    assert motivo is not None and "SIN FILTRAR" in motivo, forma


def test_a_la_opcion_en_codigo_en_linea_y_en_la_cli_se_niega(g: ModuleType, repo: Path) -> None:
    for comando in (
        f'python -c "print(dict({OPC}=True))"',
        f"uv run botsito kb find x --{OPC}",
        f"uv run botsito kb find x --{OPC[:2]}",  # la abreviatura que argparse acepta
        f"python - <<'EOF'\nprint(dict({OPC}=1))\nEOF\n",
    ):
        motivo = _bash(g, repo, comando)
        assert motivo is not None and "SIN FILTRAR" in motivo, comando


def test_a_una_variable_con_ese_nombre_y_los_grep_pasan(g: ModuleType, repo: Path) -> None:
    # El lector de la rama (DEMO-EJECUCION-1.md §3.3) y la prevision de MARGEN-PENDIENTE.md :421.
    lector = f"def leer(ruta):\n    {OPC} = ruta.read_bytes()\n    return {OPC}.decode()\n"
    prevision = f"from pathlib import Path\n{OPC} = Path('docs/a.md').read_text()\nprint({OPC})\n"
    falso = f"def f(**k):\n    return k\nprint(f({OPC}=False))\n"
    for nombre, codigo in (("leer.py", lector), ("prevision.py", prevision), ("falso.py", falso)):
        assert _bash(g, repo, _escribe_guion(repo, nombre, codigo)) is None, nombre
    for comando in (
        f'grep -n "{OPC} = " src/botsito/x.py',
        f'grep -rn -E "def |{OPC}=" src/botsito',
        f"grep -rn '{OPC}: bool' src/botsito",
    ):
        assert _bash(g, repo, comando) is None, comando


# ------------------------------------------------------- b) los tests de un clon (K2)
def test_b_los_tests_del_clon_iguales_al_de_main_o_al_del_repo_pasan(
    g: ModuleType, repo: Path
) -> None:
    clon = _clon(repo)
    for comando in (
        f"cd {clon} && uv run pytest tests/unit/test_recorre.py -q",
        f"uv run pytest {clon}/tests/unit/test_recorre.py -q",
        f"cd {clon} && uv run pytest tests/unit/test_nuevo.py -q",  # el de la rama, copiado
        f"cd {clon} && uv run pytest tests/unit/test_barra.py -q",  # ACTIVAR-SESION-05.md §0.f
        f"cd {clon} && uv run pytest tests/unit/test_opcion.py -q",  # ENTORNO-CODE.md, G.1
        f"cd {clon} && uv run pytest tests/unit/test_recorre.py::test_x -q",
    ):
        assert _bash(g, repo, comando) is None, comando


def test_b_lo_que_no_es_el_test_del_repo_se_sigue_negando(g: ModuleType, repo: Path) -> None:
    clon, otro = _clon(repo), _otro(repo)
    for comando in (
        f"cd {clon} && uv run pytest tests/unit/test_cambiado.py -q",  # cambiado en el clon
        f"cd {clon} && uv run pytest -q",  # sin rutas fuera de la raiz (sin cambio)
        f"cd {clon} && uv run pytest tests/unit/test_recorre.py && uv run pytest tests/unit",
        f"cd {otro} && uv run pytest tests/unit/test_recorre.py -q",  # otro repositorio
        f"cd {clon} && uv run pytest herramientas/test_fuera.py -q",  # el de main, fuera de tests/
    ):
        assert _bash(g, repo, comando) is not None, comando


# ------------------------------------------------- c) `\.`, la raiz de la unidad (K3)
def _windows(g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Simula Windows para `\\.`: es la raiz de la unidad, que CONTIENE el repo y el clon."""
    original: Callable[[str, str], str] = g._absoluta

    def absoluta(ruta: str, cwd: str) -> str:
        if ruta.strip() in {"\\.", "\\"}:
            return str(repo.parent)
        return original(ruta, cwd)

    monkeypatch.setattr(g, "_absoluta", absoluta)


def test_c_la_raiz_de_la_unidad_en_un_test_del_clon_igual_pasa(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _windows(g, repo, monkeypatch)
    comando = f"cd {_clon(repo)} && uv run pytest tests/unit/test_regex.py -q"
    assert _bash(g, repo, comando) is None


def test_c_la_raiz_de_la_unidad_en_un_test_cambiado_se_niega(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _windows(g, repo, monkeypatch)
    comando = f"cd {_clon(repo)} && uv run pytest tests/unit/test_regex_cambiado.py -q"
    motivo = _bash(g, repo, comando)
    assert motivo is not None and "\\." in motivo, motivo


# ----------------------------------------------------------- d) el candidato vacio (K4)
def test_d_un_patron_con_igual_no_es_una_ruta(g: ModuleType, repo: Path) -> None:
    for comando in (
        'grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py',
        'grep -rn "HUSO_CORTE =" src/botsito/engine/perfil_cuenta.py; '
        'grep -rln "huso_corte" knowledge/cuentas | head -3',  # BARRIDO-SESION-6.md :540
        'grep -rn "^Puntos\\|Puntos = " src/botsito/*.py | head -3',  # BARRIDO-SESION-6.md :612
        'grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" '
        '-e "DIAGNOSTICO-A21" -e "a21=" src/ tests/ scripts/',  # ACTIVAR-SESION-04-MOTOR.md
        'grep -rn "HUSO_CORTE =" src/',
        "grep -rn --exclude= x src",
    ):
        assert _bash(g, repo, comando) is None, comando


def test_d_lo_que_sigue_siendo_una_ruta_se_mira(g: ModuleType, repo: Path) -> None:
    for comando in (
        'grep -rn " " src/',  # el argumento entero en blanco: sigue como hoy (decision 4)
        f"grep -rn --exclude-dir={KC}/{HOL} x src",
        f"cat --x={SECRETO}",
        f"cat ruta={SECRETO}",
    ):
        assert _bash(g, repo, comando) is not None, comando


# ---------------------------------------------------------------- f) el resto de G.1
def test_f_solo_lectura_deja_leer_git_con_opciones_globales(s: ModuleType, repo: Path) -> None:
    clon = _clon(repo)
    for comando in (
        "git worktree list",
        "git worktree list --porcelain",
        f"git -C {clon} rev-parse HEAD",
        f"git -C {clon} status --short",
        "git -c core.quotepath=false log -1",
        "git --git-dir=.git log -1",
        "git tag -l 'stable/F38*'",
        "git tag --list",
        "git tag",
        "git --no-pager log -1",
        "git branch --show-current",
        "git stash list",
    ):
        assert s.motivo(comando) is None, comando


def test_f_solo_lectura_sigue_negando_lo_que_escribe(s: ModuleType, repo: Path) -> None:
    clon = _clon(repo)
    for comando in (
        "git tag stable/x",
        "git tag -d stable/x",
        "git tag -l x -d y",
        f"git -C {clon} commit -m x",
        f"git -C {clon} tag stable/y",
        "git -c user.name=x commit -m x",
        "git worktree add ../x",
        "git worktree remove x",
        "git -C",
        "git branch nueva",
    ):
        assert s.motivo(comando) is not None, comando


def test_f_which_rmdir_y_pythonioencoding_pasan(g: ModuleType, repo: Path) -> None:
    for comando in (
        "which python python3",  # n1 de la fase 0
        "rm x.txt && rmdir vacio",  # la negativa de H
        "PYTHONIOENCODING=utf-8 python scripts/de_main.py",  # BARRIDO-SESION-6.md §4
    ):
        assert _bash(g, repo, comando) is None, comando


def test_f_lo_decidido_en_guion_mismo_comando_sigue_negado(g: ModuleType, repo: Path) -> None:
    for comando in (
        "grep -n x PROJECT_STATE.md; uv run botsito state check",  # f9, decision 6
        "uv run botsito state check | tail -8; uv run python scripts/de_main.py",  # f9b
        "git -c core.quotepath=false log -1",  # GIT_C_CLAVES vacia, decision 6
        "PYTHONPATH=x python scripts/de_main.py",  # fuera de NOMBRES_DE_ENTORNO
        "rm x.txt && desconocido vacio",  # un programa fuera de NO_EJECUTAN
    ):
        assert _bash(g, repo, comando) is not None, comando


# ------------------------------------------- g) B: lo que el guion importa o ejecuta (fase 2)
def _malo(repo: Path) -> str:
    """Un modulo local que imprime el fichero FALSO del holdout del repo inventado."""
    secreto = (repo / SECRETO).as_posix()
    _escribir(repo, "trabajo/mod_malo.py", f"print(open({secreto!r}).read())\n")
    _escribir(repo, "trabajo/mod_bueno.py", "X = 1\n")
    return secreto


CARGAS_MALAS = {
    "import_sys_path": "import sys\nsys.path.insert(0, 'trabajo')\nimport mod_malo\n",
    "import_local": "import mod_malo\n",  # en la carpeta del guion
    "from_local": "from mod_malo import x\n",
    "runpy": "import runpy\nrunpy.run_path('trabajo/mod_malo.py')\n",
    "runpy_alias": "from runpy import run_path as rp\nrp('trabajo/mod_malo.py')\n",
    "exec_open": "exec(open('trabajo/mod_malo.py').read())\n",
    "exec_read_text": "from pathlib import Path\nexec(Path('trabajo/mod_malo.py').read_text())\n",
    "subprocess": "import subprocess\nsubprocess.run(['python', 'trabajo/mod_malo.py'])\n",
    "subprocess_alias": "import subprocess as sp\nsp.call(['python', 'trabajo/mod_malo.py'])\n",
    "os_system": "import os\nos.system('python trabajo/mod_malo.py')\n",
    "importlib": "import importlib, sys\nsys.path.insert(0, 'trabajo')\n"
    "importlib.import_module('mod_malo')\n",
    "import_dinamico": "import importlib, sys\nimportlib.import_module(sys.argv[1])\n",
    "exec_dinamico": "import sys\nexec(sys.argv[1])\n",
    "subprocess_dinamico": "import subprocess, sys\nsubprocess.run([sys.argv[1], 'x'])\n",
    "sys_path_dinamico": "import sys\nsys.path.insert(0, sys.argv[1])\nimport json\n",
    "no_existe": "import zzz_modulo_que_no_existe_en_ninguna_parte\n",
    "git_show_dinamico": "import subprocess, sys\nsubprocess.run(['git', 'show', sys.argv[1]])\n",
}


@pytest.mark.parametrize("forma", sorted(CARGAS_MALAS))
def test_g_lo_que_el_guion_carga_sin_resolver_o_protegido_se_niega(
    g: ModuleType, repo: Path, forma: str
) -> None:
    _malo(repo)
    motivo = _bash(g, repo, _escribe_guion(repo, f"trabajo/b_{forma}.py", CARGAS_MALAS[forma]))
    assert motivo is not None, forma


def test_g_el_codigo_en_linea_tambien(g: ModuleType, repo: Path) -> None:
    _malo(repo)
    for comando in (
        'cd trabajo && python -c "import mod_malo"',
        "python -c \"import runpy; runpy.run_path('trabajo/mod_malo.py')\"",
    ):
        assert _bash(g, repo, comando) is not None, comando


def test_g_lo_que_se_resuelve_y_es_inocuo_pasa(g: ModuleType, repo: Path) -> None:
    _malo(repo)
    _escribir(repo, "trabajo/n1.py", "import n2\n")
    _escribir(repo, "trabajo/n2.py", "import n3\n")
    _escribir(repo, "trabajo/n3.py", "X = 3\n")
    for nombre, codigo in (
        ("local", "import mod_bueno\nprint(mod_bueno.X)\n"),
        ("estandar", "import json\nimport os.path\nfrom pathlib import Path\n"),
        ("entorno", "import yaml\nimport pytest\n"),  # paquetes del .venv del repo
        ("botsito", "from botsito.cases.holdout import casos_reservados\n"),
        ("de_main", "import sys\nsys.path.insert(0, 'scripts')\nimport de_main\n"),
        ("git", "import subprocess\nsubprocess.run(['git', 'status', '--short'])\n"),
        ("exec_literal", "exec('x = 1')\n"),
        ("runpy_inocuo", "import runpy\nrunpy.run_path('trabajo/mod_bueno.py')\n"),
        ("importlib", "import importlib\nimportlib.import_module('json')\n"),
        ("tres_niveles", "import n1\n"),  # n1 -> n2 -> n3
        ("propia_run", "def run(x):\n    return x\nrun('python trabajo/mod_malo.py')\n"),
    ):
        guion = _escribe_guion(repo, f"trabajo/ok_{nombre}.py", codigo)
        assert _bash(g, repo, guion) is None, (nombre, _bash(g, repo, guion))


def test_g_mas_de_tres_niveles_se_niega(g: ModuleType, repo: Path) -> None:
    for i in range(1, 5):
        _escribir(repo, f"trabajo/m{i}.py", f"import m{i + 1}\n" if i < 4 else "X = 4\n")
    _escribir(repo, "trabajo/m5.py", "X = 5\n")
    motivo = _bash(g, repo, _escribe_guion(repo, "trabajo/cuatro.py", "import m1\n"))
    assert motivo is not None and "niveles" in motivo, motivo


# ---------------------------------------------------------- h) C: las rutas compuestas (fase 2)
PARTES = f"'knowledge', 'cases', '{HOL}', '1', 'secreto.yaml'"
COMPUESTAS = {
    "joinpath": f"from pathlib import Path\nprint(Path('.').joinpath({PARTES}).read_text())\n",
    "os_path_join": f"import os\nprint(open(os.path.join({PARTES})).read())\n",
    "barra": "from pathlib import Path\n"
    f"print((Path('knowledge') / 'cases' / '{HOL}' / '1' / 'secreto.yaml').read_text())\n",
    "fstring": f"zona = '{HOL}'\nprint(open(f'knowledge/cases/{{zona}}/1/secreto.yaml').read())\n",
    "fstring_partes": "a, b = 'knowledge', 'cases'\n"
    f"print(open(f'{{a}}/{{b}}/{HOL}/1/secreto.yaml').read())\n",
    "concatenacion": f"print(open('knowledge' + '/' + 'cases' + '/{HOL}/1/secreto.yaml').read())\n",
    "sin_calcular": "import sys\nfrom pathlib import Path\n"
    f"print((Path(sys.argv[1]) / '{HOL}' / '1' / 'secreto.yaml').read_text())\n",
    "url": "from urllib.request import urlopen\nprint(urlopen('file://REPO/"
    + SECRETO
    + "').read())\n",
    "ci_a_trozos": "import subprocess\nsubprocess.run(['g' + 'h', 'run', 'view', '1'])\n",
}


@pytest.mark.parametrize("forma", sorted(COMPUESTAS))
def test_h_las_rutas_compuestas_al_material_se_niegan(
    g: ModuleType, repo: Path, forma: str
) -> None:
    codigo = COMPUESTAS[forma].replace("REPO", repo.as_posix())
    motivo = _bash(g, repo, _escribe_guion(repo, f"c_{forma}.py", codigo))
    assert motivo is not None, forma


def test_h_las_llaves_y_las_url_en_bash_se_niegan(g: ModuleType, repo: Path) -> None:
    for comando in (
        f"cat '{KC}/'{{{HOL},dev}}'/1/secreto.yaml'",  # GUARDIA-ALIAS.md §9, b6
        f"curl file://{(repo / SECRETO).as_posix()}",  # b7
        f"curl --url=file://{(repo / SECRETO).as_posix()}",
    ):
        assert _bash(g, repo, comando) is not None, comando


def test_h_las_composiciones_inocuas_pasan(g: ModuleType, repo: Path) -> None:
    for nombre, codigo in (
        ("barra", "from pathlib import Path\nprint((Path('docs') / 'a.md').read_text())\n"),
        ("join", "import os\nprint(open(os.path.join('src', 'botsito', 'x.py')).read())\n"),
        ("sin_calcular", "import sys\nprint(open(f'{sys.argv[1]}/salida.txt').read())\n"),
        ("mensaje", f"import sys\nprint('no se lee el {HOL}: ' + sys.argv[1])\n"),
        ("file", "from pathlib import Path\nprint((Path(__file__).parent / 'docs').exists())\n"),
        (
            "raiz",
            "from pathlib import Path\nRAIZ = Path(__file__).resolve().parent\n"
            "print((RAIZ / 'docs' / 'a.md').read_text())\n",
        ),
    ):
        guion = _escribe_guion(repo, f"ok_c_{nombre}.py", codigo)
        assert _bash(g, repo, guion) is None, (nombre, _bash(g, repo, guion))
    for comando in ("cat '{docs,src}/a.md'", f"curl file://{(repo / 'docs/a.md').as_posix()}"):
        assert _bash(g, repo, comando) is None, comando


# --------------------------------------------------------------- roto a proposito
def _romper(cual: str, g: ModuleType, s: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    """Rompe a proposito una pieza de esta rama (los dos sentidos de cada una)."""
    if cual == "sin_listado":  # e) la condicion quitada: vuelven a pasar los listados
        monkeypatch.setattr(g.Politica, "lista_dentro_del_holdout", lambda self, r, rec: False)
    elif cual == "listado_de_mas":  # e) todo listado alcanza el holdout: lo literal se niega
        monkeypatch.setattr(g.Politica, "lista_dentro_del_holdout", lambda self, r, rec: True)
    elif cual == "sin_forma":  # a) el arbol no ve la forma: la opcion vuelve a pasar
        monkeypatch.setattr(g, "_pide_la_opcion", lambda arbol: False)
    elif cual == "regex_de_antes":  # a) el texto de Bash otra vez con el regex de la palabra
        monkeypatch.setattr(
            g,
            "_opcion_en_el_texto",
            lambda t: bool(g.CRUDO_OPCION.search(t) or g.CRUDO_PYTHON.search(t)),
        )
        monkeypatch.setattr(g, "_pide_la_opcion", lambda arbol: True)
    elif cual == "sin_clon":  # b) un test del clon vuelve a ser codigo sin revisar
        monkeypatch.setattr(g, "_test_de_un_clon", lambda ruta, raiz, con_el_arbol: False)
    elif cual == "clon_de_mas":  # b) cualquier fichero de fuera cuenta como test del repo
        monkeypatch.setattr(g, "_test_de_un_clon", lambda ruta, raiz, con_el_arbol: True)
    elif cual == "candidato_de_antes":  # d) lo de detras del `=` otra vez, aunque este en blanco
        original = g.candidatos_de_ruta

        def de_antes(valor: str) -> Any:
            yield from original(valor)
            if "=" in valor and not valor.split("=", 1)[1].strip():
                yield valor.split("=", 1)[1]

        monkeypatch.setattr(g, "candidatos_de_ruta", de_antes)
    elif cual == "sin_candidato_igual":  # d) nunca se parte por `=`: `--x=<ruta>` se escapa
        monkeypatch.setattr(g, "candidatos_de_ruta", lambda valor: iter([valor]))
    elif cual == "subcomando_de_antes":  # f) el primer token sin guion, como hacia main
        monkeypatch.setattr(
            s,
            "_subcomando_git",
            lambda textos: (
                next((t for t in textos if not t.startswith("-")), ""),
                textos[1:],
            ),
        )
    elif cual == "subcomando_de_mas":  # f) todo es `status`: lo que escribe pasa
        monkeypatch.setattr(s, "_subcomando_git", lambda textos: ("status", []))
    elif cual == "sin_listas_nuevas":  # f) which, rmdir y PYTHONIOENCODING fuera
        for nombre in ("which", "rmdir"):
            monkeypatch.delitem(g.NO_EJECUTAN, nombre)
        monkeypatch.delitem(g.NOMBRES_DE_ENTORNO, "PYTHONIOENCODING")
    elif cual == "lo_decidido_abierto":  # f) lo decidido se abre: tiene que seguir negado
        monkeypatch.setattr(g, "_es_preparacion", lambda cmd: True)
        monkeypatch.setattr(g, "_nombre_admitido", lambda nombre: True)
        monkeypatch.setattr(g, "_no_ejecuta", lambda prog: True)
        monkeypatch.setattr(g, "GIT_C_CLAVES", {"core.quotepath"})
    elif cual == "sin_carga":  # g) B quitada: lo que el guion carga vuelve a pasar sin leerse
        monkeypatch.setattr(g, "_exigir_lo_que_carga", lambda arbol, ctx, guion, vistos: None)
    elif cual == "carga_de_mas":  # g) nada esta instalado: la biblioteca estandar se niega
        monkeypatch.setattr(g, "_instalado", lambda nombre, raiz: False)
    elif cual == "sin_composicion":  # h) C quitada: las rutas a trozos vuelven a pasar
        monkeypatch.setattr(g, "_compone_ruta_sensible", lambda arbol, ctx, recorre, guion: None)
    elif cual == "composicion_de_mas":  # h) ninguna composicion se calcula y todas son sensibles
        monkeypatch.setattr(g, "_calcular", lambda nodo, asig, guion, prof=0: "\x00/" + HOL)
    elif cual == "sin_llaves_ni_url":  # h) bash sin expandir llaves y sin leer `file:`
        monkeypatch.setattr(g, "_llaves", lambda patron, limite=256: [patron])
        monkeypatch.setattr(g, "_ruta_de_url", lambda url: url)
    else:
        raise AssertionError(cual)


ROTURAS = [
    ("sin_listado", "test_e_los_listados_del_holdout_se_niegan"),
    ("sin_listado", "test_e_el_glob_que_alcanza_el_holdout_se_niega"),
    ("sin_listado", "test_e_powershell_que_lista_el_holdout_se_niega"),
    ("listado_de_mas", "test_e_el_recuento_y_lo_literal_pasan"),
    ("listado_de_mas", "test_e_glob_y_powershell_que_no_alcanzan_el_holdout_pasan"),
    ("sin_forma", "test_a_la_forma_de_la_opcion_en_python_se_niega"),
    ("sin_forma", "test_a_la_opcion_en_codigo_en_linea_y_en_la_cli_se_niega"),
    ("regex_de_antes", "test_a_una_variable_con_ese_nombre_y_los_grep_pasan"),
    ("sin_clon", "test_b_los_tests_del_clon_iguales_al_de_main_o_al_del_repo_pasan"),
    ("clon_de_mas", "test_b_lo_que_no_es_el_test_del_repo_se_sigue_negando"),
    ("sin_clon", "test_c_la_raiz_de_la_unidad_en_un_test_del_clon_igual_pasa"),
    ("clon_de_mas", "test_c_la_raiz_de_la_unidad_en_un_test_cambiado_se_niega"),
    ("candidato_de_antes", "test_d_un_patron_con_igual_no_es_una_ruta"),
    ("sin_candidato_igual", "test_d_lo_que_sigue_siendo_una_ruta_se_mira"),
    ("subcomando_de_antes", "test_f_solo_lectura_deja_leer_git_con_opciones_globales"),
    ("subcomando_de_mas", "test_f_solo_lectura_sigue_negando_lo_que_escribe"),
    ("sin_listas_nuevas", "test_f_which_rmdir_y_pythonioencoding_pasan"),
    ("lo_decidido_abierto", "test_f_lo_decidido_en_guion_mismo_comando_sigue_negado"),
    ("sin_carga", "test_g_lo_que_el_guion_carga_sin_resolver_o_protegido_se_niega"),
    ("sin_carga", "test_g_el_codigo_en_linea_tambien"),
    ("sin_carga", "test_g_mas_de_tres_niveles_se_niega"),
    ("carga_de_mas", "test_g_lo_que_se_resuelve_y_es_inocuo_pasa"),
    ("sin_composicion", "test_h_las_rutas_compuestas_al_material_se_niegan"),
    ("composicion_de_mas", "test_h_las_composiciones_inocuas_pasan"),
    ("sin_llaves_ni_url", "test_h_las_llaves_y_las_url_en_bash_se_niegan"),
]

# Los parametrizados se rompen con su caso mas representativo.
PARAMETROS: dict[str, dict[str, Any]] = {
    "test_e_los_listados_del_holdout_se_niegan": {"comando": LISTADOS_DEL_HOLDOUT[0]},
    "test_e_el_recuento_y_lo_literal_pasan": {"comando": RECUENTOS_Y_LITERALES[4]},
    "test_a_la_forma_de_la_opcion_en_python_se_niega": {"forma": "argumento"},
    "test_g_lo_que_el_guion_carga_sin_resolver_o_protegido_se_niega": {"forma": "import_local"},
    "test_h_las_rutas_compuestas_al_material_se_niegan": {"forma": "joinpath"},
}


@pytest.mark.parametrize(("rotura", "nombre"), ROTURAS)
def test_roto_a_proposito(
    g: ModuleType,
    s: ModuleType,
    repo: Path,
    monkeypatch: pytest.MonkeyPatch,
    rotura: str,
    nombre: str,
) -> None:
    _romper(rotura, g, s, monkeypatch)
    test = globals()[nombre]
    argumentos: dict[str, Any] = {"g": g, "s": s, "repo": repo, "monkeypatch": monkeypatch}
    argumentos |= PARAMETROS.get(nombre, {})
    nombres = test.__code__.co_varnames[: test.__code__.co_argcount]
    with pytest.raises(AssertionError) as fallo:
        test(**{n: argumentos[n] for n in nombres})
    primera = str(fallo.value).splitlines()[0] if str(fallo.value) else "AssertionError"
    print(f"ROTO | {rotura} | {nombre} | falla: {primera[:160]}")


# ------------------------------------- la comparacion caso a caso con la guardia de `main`
MEDIR_G1 = RAIZ / "docs" / "validation" / "anexos" / "GUARDIA-G1" / "medir_g1.py"


def _de_main(rel: str) -> str | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for ref in ("main", "origin/main"):
        r = subprocess.run(
            ["git", "show", f"{ref}:{rel}"],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            check=False,
            env=env,
        )
        if r.returncode == 0:
            return r.stdout
    return None


def test_la_comparacion_caso_a_caso_con_la_guardia_de_main(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    """El metodo de GUION-MISMO-COMANDO.md §1.4 (`anexos/GUARDIA-G1/medir_g1.py`): la guardia de
    `main` y la de la rama sobre los mismos casos; ningun caso que `main` niega pasa en la rama sin
    estar en `CAMBIOS_DECLARADOS`. Corre desde `tests/` porque desde la fase 2 (C) la guardia niega
    ejecutar como guion suelto un fichero que monta rutas protegidas a trozos, que es lo que
    `medir_g1.py` hace con su repo inventado (GUARDIA-G1.md §5)."""
    hooks = tmp_path / "main" / ".claude" / "hooks"
    hooks.mkdir(parents=True)
    for nombre in ("guardia.py", "solo_lectura.py"):
        texto = _de_main(f".claude/hooks/{nombre}")
        if texto is None:
            pytest.skip("sin `main` ni `origin/main` no hay guardia de main con que comparar")
        (hooks / nombre).write_text(texto, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("medir_g1_anexo", MEDIR_G1)
    assert spec is not None and spec.loader is not None
    medir = importlib.util.module_from_spec(spec)
    sys.modules["medir_g1_anexo"] = medir
    spec.loader.exec_module(medir)
    monkeypatch.setattr(sys, "argv", ["medir_g1.py", str(hooks / "guardia.py"), str(GUARDIA)])
    salida = medir.main()
    impreso = capsys.readouterr().out
    print(impreso)
    assert salida == 0, [x for x in impreso.splitlines() if "SIN DECLARARLO" in x]
