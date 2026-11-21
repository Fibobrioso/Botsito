"""El material protegido se niega por lo que ES, no solo por donde esta respecto de la raiz.

Rama `trabajo/guardia-enlaces` (2026-11-20, docs/validation/GUARDIA-ENLACES.md; hoja de ruta, G.8).
Con `corpus/` como union a otro disco la ruta canonica quedaba fuera de la raiz y las reglas del
material adicional dejaban de aplicarse (GUARDIAS-HOLDOUT.md §17); una copia del material fuera del
repo, o un clon desechable, tampoco se protegia; y un Read de la carpeta `Backtest <mes>` misma no
se negaba. Las dos decisiones del consultor:

- D1: una ruta se decide por TODAS sus formas y se niega si cualquiera niega: la TEXTUAL relativa a
  la raiz (sin resolver enlaces), la CANONICA relativa a la raiz y, si cae fuera, su ESTRUCTURA (un
  anclaje de una clase protegida en cualquier tramo se lee como si estuviera en la raiz).
- D2: la carpeta `Backtest <mes>` de un mes no legible, como objetivo directo de Read, Grep o Glob,
  se niega como su contenido; `ls` y `Get-ChildItem` se quedan como estaban.

Todo EN MEMORIA, con `decidir`, sobre un repo INVENTADO en `tmp_path` y copias INVENTADAS fuera de
el, con ficheros falsos: nada del repo real se abre. Las rutas protegidas van a trozos, como en
`test_guardia_alias.py`. Los enlaces reales: una union (`mklink /J`, sin administrador) en Windows y
`symlink_to` fuera; si no se puede crear, el test se salta con su motivo.

Cada forma de D1 la sostiene al menos un test (los mutantes a mano de GUARDIA-ENLACES.md §3):
la CANONICA, `test_un_enlace_de_fuera_hacia_el_holdout_se_niega`; la TEXTUAL,
`test_un_enlace_de_dentro_a_un_nombre_sin_estructura_se_niega`; la ESTRUCTURA, los de las copias.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
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
CASO = "caso-eurusd-2026-05-04"  # el reservado del repo INVENTADO

IMAGEN = f"{BTM}/x.png"
LIBRO = f"{MAT}/backtesting-analytics MARZO 2026.xlsx"
LIBRO_MES = f"{MAT}/resumen mayo 2026.xlsx"  # mayo: un mes con dias reservados en el repo inventado
CASO_1 = f"{HOL}/1/{CASO}.yaml"
HOJA = f"{SES}/hoja-05.xlsx"
CRUDA = f"{TRA}/v7/large-v3/cruda.jsonl"
FOTO = f"{MAT}/Capturas/foto.png"
PROTEGIDOS = {
    "imagen de Backtest marzo": (IMAGEN, "R_CAPTURA"),
    "libro por su nombre": (LIBRO, "R_SIN_ABRIR"),
    "libro de un mes reservado": (LIBRO_MES, "R_LIBRO"),
    "imagen del material": (FOTO, "R_CAPTURA"),
    "caso de holdout/1": (CASO_1, "R_HOLDOUT"),
    "caso de holdout/3": (f"{HOL}/3/{CASO}.yaml", "R_HOLDOUT"),
    "hoja de Sesiones": (HOJA, "R_HOJA"),
    "cruda en cuarentena": (CRUDA, "R_CUARENTENA"),
}


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


def _escribir(base: Path, rel: str, texto: str = "dato falso\n") -> None:
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


def _material(base: Path) -> None:
    """Los ficheros falsos de cada clase, y la carpeta de Backtest marzo VACIA aparte."""
    for rel, _ in PROTEGIDOS.values():
        _escribir(base, rel)
    _escribir(base, f"{HOL}/1/README.md", "# particion 1\n")
    (base / VACIA).mkdir(parents=True, exist_ok=True)


VACIA = MAT + "/Back" + "test junio 2026"  # junio: ni de desarrollo ni reservado en el inventado


def _hacer_repo(r: Path, material: bool = True) -> Path:
    """Un repo inventado, con la estructura del real (como el de `test_guardia_alias.py`)."""
    _escribir(r, "Makefile", "x\n")
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _escribir(r, "knowledge/corpus/fuentes.yaml", "videos:\n  - video_id: v7\n    drive_id: null\n")
    _escribir(
        r,
        "knowledge/cases/kit/s1/particiones.yaml",
        f"asignacion:\n  {CASO}: holdout-1\ncupos:\n  dev: 0\n",
    )
    _escribir(r, "src/botsito/cli.py", "x = 1\n")
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    for args in (
        ["init", "-q", "-b", "main"],
        ["add", "-A"],
        ["-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio"],
        ["checkout", "-q", "-b", "trabajo/prueba"],
    ):
        subprocess.run(["git", *args], cwd=r, check=True, capture_output=True, env=env)
    if material:
        _material(r)
    return r


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return _hacer_repo(tmp_path / "Bot v3 prueba")


@pytest.fixture
def copia(tmp_path: Path) -> Path:
    """Una copia con la misma estructura FUERA del repo (`D:\\BotsitoCorpus`, un clon)."""
    c = tmp_path / "Copia de respaldo"
    _material(c)
    return c


def _decide(g: ModuleType, repo: Path, herramienta: str, entrada: dict[str, Any]) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(repo)}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _regla(g: ModuleType, motivo: str | None) -> str:
    if motivo is None:
        return "pasa"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    return ",".join(sorted(nombres)) or "niega (sin R_)"


def _lecturas(ruta: str) -> list[tuple[str, str, dict[str, Any]]]:
    posix = ruta.replace("\\", "/")
    return [
        ("Read", "Read", {"file_path": ruta}),
        ("Grep", "Grep", {"pattern": "x", "path": ruta}),
        ("Bash cat", "Bash", {"command": f'cat "{posix}"'}),
        ("PowerShell Get-Content", "PowerShell", {"command": f"Get-Content '{ruta}'"}),
    ]


def _fallos(g: ModuleType, repo: Path, casos: list[tuple[str, str]]) -> list[str]:
    """`casos`: (ruta, regla esperada). Cada ruta, por cada lectura."""
    fallos = []
    for ruta, esperada in casos:
        for etiqueta, herramienta, entrada in _lecturas(ruta):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"{esperada} | {etiqueta} | {obtenida} | {ruta[-60:]}")
            if esperada not in obtenida.split(","):
                fallos.append(f"{etiqueta} · {ruta[-60:]}: {obtenida} (se esperaba {esperada})")
    return fallos


def _union(enlace: Path, destino: Path) -> None:
    enlace.parent.mkdir(parents=True, exist_ok=True)
    try:
        if EN_WINDOWS:
            subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(enlace), str(destino)],
                check=True,
                capture_output=True,
            )
        else:
            enlace.symlink_to(destino, target_is_directory=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        pytest.skip(f"no se pudo crear el enlace en esta plataforma: {exc}")


def _simular_enlace(
    g: ModuleType, monkeypatch: pytest.MonkeyPatch, enlace: Path, destino: Path
) -> None:
    """`enlace` (que no existe en disco) como un enlace a `destino`, por `_realpath`."""
    real = g._realpath
    pre = g._normcase(str(enlace))

    def simulado(ruta: str) -> str:
        n = g._normcase(ruta)
        if n == pre or n.startswith(pre + "/"):
            return os.path.normpath(str(destino) + ruta[len(pre) :])
        return str(real(ruta))

    monkeypatch.setattr(g, "_realpath", simulado)


# ------------------------------------------------------------------ (c) una copia fuera del repo
def test_la_imagen_de_backtest_marzo_en_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    assert not _fallos(g, repo, [(str(copia / IMAGEN), "R_CAPTURA")])


def test_cada_clase_en_una_copia_fuera_se_niega_con_su_regla(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """Las clases de D1 (material, Sesiones, holdout 1-3, la cruda en cuarentena) y el libro."""
    fallos = _fallos(g, repo, [(str(copia / rel), regla) for rel, regla in PROTEGIDOS.values()])
    assert not fallos, "\n".join(fallos)


def test_el_libro_y_el_holdout_de_una_copia_se_niegan_tambien_en_mayusculas_y_con_barras(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    casos = []
    for rel, regla in ((LIBRO_MES, "R_LIBRO"), (CASO_1, "R_HOLDOUT")):
        ruta = str(copia / rel)
        casos += [(ruta, regla), (ruta.upper(), regla), (ruta.replace("\\", "/"), regla)]
        if EN_WINDOWS:  # en Linux `\` es parte del nombre: no separa tramos
            casos.append((ruta.replace("/", "\\"), regla))
    fallos = _fallos(g, repo, casos)
    assert not fallos, "\n".join(fallos)


def test_el_anclaje_minimo_del_material_y_de_sesiones_no_exige_corpus(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    """D1: «estrategia del trader/material adicional de su operativa/» y
    «estrategia del trader/sesiones/», sin `corpus/` delante (una copia de la carpeta del
    trader)."""
    sin_corpus = tmp_path / "solo el trader"
    _escribir(sin_corpus, IMAGEN.split("/", 1)[1])
    _escribir(sin_corpus, HOJA.split("/", 1)[1])
    fallos = _fallos(
        g,
        repo,
        [
            (str(sin_corpus / IMAGEN.split("/", 1)[1]), "R_CAPTURA"),
            (str(sin_corpus / HOJA.split("/", 1)[1]), "R_HOJA"),
        ],
    )
    assert not fallos, "\n".join(fallos)


def test_el_readme_de_una_particion_de_la_copia_se_sigue_leyendo(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """La exencion del README de `holdout/{1,2,3}` se cuenta desde el anclaje (auditor, punto 10:
    un clon de comparar-con-main lleva los tres)."""
    leeme = str(copia / HOL / "1" / "README.md")
    assert _decide(g, repo, "Read", {"file_path": leeme}) is None


def test_listar_el_holdout_de_una_copia_se_niega(g: ModuleType, repo: Path, copia: Path) -> None:
    """ADR-0088 por estructura: los nombres de dentro de `holdout/1` de una copia, ni por Glob ni
    por `ls`; y un listado recursivo de la carpeta que contiene la copia, tampoco."""
    particion = (copia / HOL / "1").as_posix()
    for herramienta, entrada in (
        ("Glob", {"pattern": "*", "path": particion}),
        ("Glob", {"pattern": f"{particion}/*.yaml"}),
        ("Bash", {"command": f'ls "{particion}"'}),
        ("Bash", {"command": f'find "{copia.as_posix()}" -name "*.yaml"'}),
    ):
        motivo = _decide(g, repo, herramienta, entrada)
        assert motivo is not None and "R_LISTADO" in _regla(g, motivo), (herramienta, entrada)


def test_un_lector_recursivo_sobre_la_carpeta_de_la_copia_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """La carpeta que contiene la copia no lleva anclaje en su ruta; lo que alcanzaria, si."""
    for herramienta, entrada in (
        ("Grep", {"pattern": "x", "path": str(copia)}),
        ("Bash", {"command": f'grep -r x "{copia.as_posix()}"'}),
    ):
        assert _decide(g, repo, herramienta, entrada) is not None, (herramienta, entrada)


def test_fuera_sin_ningun_anclaje_pasa(g: ModuleType, repo: Path, tmp_path: Path) -> None:
    """Que la regla no se pase de frenada: un fichero cualquiera de una carpeta temporal, la
    carpeta misma, y una ruta que solo PARECE un anclaje (un tramo que no empieza en un limite)."""
    suelta = tmp_path / "suelta"
    _escribir(suelta, "nota.txt")
    _escribir(suelta, "otraestrategia del trader/material adicional de su operativa/x.png")
    _escribir(suelta, "knowledge/cases/holdout/4/caso.yaml")
    fallos = []
    for ruta in (
        str(suelta / "nota.txt"),
        str(suelta / "otraestrategia del trader/material adicional de su operativa/x.png"),
        str(suelta / "knowledge/cases/holdout/4/caso.yaml"),
    ):
        for etiqueta, herramienta, entrada in _lecturas(ruta):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            if obtenida != "pasa":
                fallos.append(f"{etiqueta} · {ruta[-50:]}: {obtenida}")
    for herramienta, entrada in (
        ("Grep", {"pattern": "x", "path": str(suelta)}),
        ("Glob", {"pattern": "**/*", "path": str(suelta)}),
        ("Bash", {"command": f'ls "{suelta.as_posix()}"'}),
    ):
        if _decide(g, repo, herramienta, entrada) is not None:
            fallos.append(f"{herramienta} · la carpeta suelta")
    assert not fallos, "\n".join(fallos)


# --------------------------------------------------------- (b) un enlace de dentro hacia fuera
def test_la_imagen_de_backtest_marzo_por_un_enlace_simulado_se_niega(
    g: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Lo de §17: `corpus/` del repo como union a otro disco (aqui, por `_realpath`), con la
    estructura detras (`D:\\BotsitoCorpus\\corpus`)."""
    r = _hacer_repo(tmp_path / "Bot v3 sin corpus", material=False)
    disco = tmp_path / "BotsitoCorpus"
    _material(disco)
    _simular_enlace(g, monkeypatch, r / ("corp" + "us"), disco / ("corp" + "us"))
    fallos = _fallos(g, r, [(str(r / IMAGEN), "R_CAPTURA"), (str(r / HOJA), "R_HOJA")])
    assert not fallos, "\n".join(fallos)


def test_un_enlace_de_dentro_a_un_nombre_sin_estructura_se_niega(
    g: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La forma TEXTUAL: `holdout/1` y `Backtest marzo 2026` como enlaces (por `_realpath`) a
    carpetas cuyo nombre no lleva ningun anclaje: la canonica cae fuera y sin estructura."""
    r = _hacer_repo(tmp_path / "Bot v3 enlazado", material=False)
    fuera = tmp_path / "otro disco"
    _escribir(fuera, f"zz/{CASO}.yaml")
    _escribir(fuera, "bm/x.png")
    real = g._realpath
    mapas = {
        g._normcase(str(r / HOL / "1")): str(fuera / "zz"),
        g._normcase(str(r / BTM)): str(fuera / "bm"),
    }

    def simulado(ruta: str) -> str:
        n = g._normcase(ruta)
        for pre, destino in mapas.items():
            if n == pre or n.startswith(pre + "/"):
                return os.path.normpath(destino + ruta[len(pre) :])
        return str(real(ruta))

    monkeypatch.setattr(g, "_realpath", simulado)
    casos = [
        (str(r / HOL / "1" / f"{CASO}.yaml"), "R_HOLDOUT"),
        (str(r / BTM / "x.png"), "R_CAPTURA"),
    ]
    fallos = _fallos(g, r, casos)
    assert not fallos, "\n".join(fallos)


def test_un_enlace_real_de_dentro_hacia_fuera_se_niega(g: ModuleType, tmp_path: Path) -> None:
    """Un enlace REAL -una union en Windows, sin administrador; un enlace simbolico fuera-:
    `corpus/` del repo -> otro disco con la estructura detras, y `holdout/1` -> una carpeta sin
    ella."""
    r = _hacer_repo(tmp_path / "Bot v3 con enlace", material=False)
    disco = tmp_path / "disco D"
    _material(disco)
    _union(r / ("corp" + "us"), disco / ("corp" + "us"))
    _escribir(tmp_path, f"zz/{CASO}.yaml")
    _union(r / HOL / "1", tmp_path / "zz")
    fallos = _fallos(
        g,
        r,
        [
            (str(r / IMAGEN), "R_CAPTURA"),
            (str(r / LIBRO_MES), "R_LIBRO"),
            (str(r / HOJA), "R_HOJA"),
            (str(r / HOL / "1" / f"{CASO}.yaml"), "R_HOLDOUT"),
        ],
    )
    # La carpeta enlazada misma: al recorrerla, cada fichero se decide tambien por la forma
    # textual de la carpeta, que su ruta en disco ya no lleva (medida «despues» de la fase 0).
    particion = str(r / HOL / "1")
    for herramienta, entrada, esperada in (
        ("Grep", {"pattern": "x", "path": particion}, "R_HOLDOUT"),
        ("Bash", {"command": f'grep -r x "{particion.replace(chr(92), "/")}"'}, "R_HOLDOUT"),
        ("Glob", {"pattern": "*", "path": particion}, "R_LISTADO"),
    ):
        obtenida = _regla(g, _decide(g, r, herramienta, entrada))
        if esperada not in obtenida.split(","):
            fallos.append(f"{herramienta} · la carpeta enlazada: {obtenida}")
    assert not fallos, "\n".join(fallos)


def test_un_enlace_de_fuera_hacia_el_holdout_se_niega(
    g: ModuleType, repo: Path, tmp_path: Path
) -> None:
    """La forma CANONICA: un enlace FUERA del repo, de nombre sin anclaje, que apunta a
    `holdout/1`; la textual cae fuera y sin estructura."""
    _union(tmp_path / "atajo", repo / HOL / "1")
    fallos = _fallos(g, repo, [(str(tmp_path / "atajo" / f"{CASO}.yaml"), "R_HOLDOUT")])
    assert not fallos, "\n".join(fallos)


# ------------------------------------------------------------ (d) D2: la carpeta Backtest misma
def _carpetas_backtest(repo: Path, copia: Path) -> list[str]:
    """La carpeta de un mes no legible VACIA (en `main` el Grep solo la negaba si tenia algun
    fichero protegido dentro), dentro del repo y en la copia; y la de marzo con su imagen."""
    return [str(repo / VACIA), str(copia / VACIA), str(repo / BTM), str(copia / BTM)]


def test_la_carpeta_backtest_como_objetivo_de_read_grep_y_glob_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    fallos = []
    for carpeta in _carpetas_backtest(repo, copia):
        for herramienta, entrada in (
            ("Read", {"file_path": carpeta}),
            ("Grep", {"pattern": "x", "path": carpeta}),
            ("Glob", {"pattern": "*", "path": carpeta}),
            ("Glob", {"pattern": carpeta.replace("\\", "/") + "/*.xlsx"}),
        ):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"D2 | {herramienta} | {obtenida} | {carpeta[-45:]}")
            if obtenida != "R_SIN_ABRIR":
                fallos.append(f"{herramienta} · {carpeta[-45:]}: {obtenida}")
    assert not fallos, "\n".join(fallos)


def test_listar_la_carpeta_backtest_con_ls_o_get_childitem_sigue_como_estaba(
    g: ModuleType, repo: Path
) -> None:
    """D2: `ls`, `dir` y `Get-ChildItem` listan nombres y se quedan como estaban (pasan)."""
    carpeta = str(repo / BTM)
    for herramienta, entrada in (
        ("Bash", {"command": f'ls "{carpeta.replace(chr(92), "/")}"'}),
        ("Bash", {"command": f'dir "{carpeta.replace(chr(92), "/")}"'}),
        ("PowerShell", {"command": f"Get-ChildItem '{carpeta}'"}),
        # Un libro SUELTO `backtesting-analytics ...` no es una carpeta `Backtest <mes>`: su Glob
        # lista un nombre que ya esta en el patron (leerlo lo niega su propia regla).
        ("Glob", {"pattern": str(repo / LIBRO).replace("\\", "/")}),
    ):
        assert _decide(g, repo, herramienta, entrada) is None, (herramienta, entrada)
    assert _decide(g, repo, "Read", {"file_path": str(repo / LIBRO)}) is not None
