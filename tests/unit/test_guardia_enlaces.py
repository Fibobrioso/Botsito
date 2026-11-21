"""El material protegido se niega por lo que ES, no solo por donde esta respecto de la raiz.

Rama `trabajo/guardia-enlaces` (2026-11-20, docs/validation/GUARDIA-ENLACES.md; hoja de ruta, G.8).
Con `corpus/` como union a otro disco la ruta canonica quedaba fuera de la raiz y las reglas del
material adicional dejaban de aplicarse (GUARDIAS-HOLDOUT.md §17); una copia del material fuera del
repo, o un clon desechable, tampoco se protegia; y un Read de la carpeta `Backtest <mes>` misma no
se negaba. Las dos decisiones del consultor:

- D1: una ruta se decide por TODAS sus formas y se niega si cualquiera niega: la TEXTUAL relativa a
  la raiz (sin resolver enlaces), la CANONICA relativa a la raiz y, si cae fuera, su ESTRUCTURA (un
  anclaje de una clase protegida en cualquier tramo se lee como si estuviera en la raiz).
- D2: la carpeta `Backtest <mes>` de un mes no legible, como objetivo directo de Read o Grep, se
  niega como su contenido; Glob, `ls` y `Get-ChildItem` la listan (respuesta del consultor a la
  PARADA final, punto 2: listar nombres no es leer contenido, ADR-0021 §1).

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
OCULTO = "knowledge/_proposals/pr-v7-x.yaml"  # en la lista de ficheros con ocultos del inventado

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
    # v6: grabacion de sesion SIN cuarentena (SESIONES_SIN_CUARENTENA) y con tramos no citables.
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
    _escribir(r, ".claude/hooks/ficheros_con_ocultos.txt", f"{OCULTO}\n")
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


def _corta(ruta: str) -> str:
    """El nombre corto 8.3 de `ruta` (metadatos), o `ruta` si el volumen no los tiene."""
    if sys.platform != "win32":  # para mypy en Linux, que no conoce `windll`
        return ruta
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    ctypes.windll.kernel32.GetShortPathNameW(ruta, buffer, 1024)
    return buffer.value or ruta


def test_un_enlace_escrito_con_un_tramo_83_se_niega(g: ModuleType, tmp_path: Path) -> None:
    """Revisor, B1: `holdout/1` como union a una carpeta sin anclaje, y la ruta escrita con el
    nombre corto de `knowledge` (`KNOWLE~1`): la forma textual expande el 8.3 sin seguir la
    union, y casa con la raiz."""
    if not EN_WINDOWS:
        pytest.skip("los nombres cortos 8.3 son de Windows")
    r = _hacer_repo(tmp_path / "Bot v3 corto", material=False)
    _escribir(tmp_path, f"zz/{CASO}.yaml")
    _union(r / HOL / "1", tmp_path / "zz")
    corta = _corta(str(r / "knowledge"))
    if corta.lower() == str(r / "knowledge").lower():
        pytest.skip("este volumen no genera nombres cortos 8.3")
    ruta = corta + "\\cases\\holdout\\1\\" + f"{CASO}.yaml"
    fallos = _fallos(g, r, [(ruta, "R_HOLDOUT")])
    assert not fallos, "\n".join(fallos)


def test_el_recorrido_de_una_carpeta_de_fuera_tiene_tope(
    g: ModuleType, repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Revisor, B3: pasado el tope de entradas, el lector recursivo y el listado recursivo de una
    carpeta de fuera se niegan (negar de mas no abre nada) en vez de arriesgar el plazo del
    hook."""
    monkeypatch.setattr(g, "LIMITE_DEL_RECORRIDO", 5)
    grande = tmp_path / "grande"
    for n in range(10):
        _escribir(grande, f"nota-{n}.txt")
    grep = _decide(g, repo, "Grep", {"pattern": "x", "path": str(grande)})
    assert grep is not None and "R_RECORRIDO" in _regla(g, grep)
    glob = _decide(g, repo, "Glob", {"pattern": "**/*", "path": str(grande)})
    assert glob is not None and "R_LISTADO" in _regla(g, glob)


def test_una_carpeta_de_fuera_con_un_anclaje_por_fichero_se_recorre_entera_y_con_tope(
    g: ModuleType, repo: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Revisor de la segunda pasada, A1: una carpeta de fuera cuya ruta lleva un anclaje por
    fichero (`knowledge/cases/`) y que tiene DEBAJO un clon con `holdout/1`: su listado recursivo
    se niega (ADR-0088), como sin el anclaje; y una carpeta de fuera con anclaje y mas entradas que
    el tope, a un lector recursivo, se niega con el tope."""
    base = tmp_path / "t" / "knowledge" / "cases" / "kit"
    _escribir(base, f"clon/{HOL}/1/caso.yaml")
    posix = base.as_posix()
    for herramienta, entrada in (
        ("Glob", {"pattern": "**/*", "path": str(base)}),
        ("Bash", {"command": f'ls -R "{posix}"'}),
        ("Bash", {"command": f'find "{posix}" -name "*.yaml"'}),
    ):
        motivo = _decide(g, repo, herramienta, entrada)
        assert motivo is not None and "R_LISTADO" in _regla(g, motivo), (herramienta, entrada)
    monkeypatch.setattr(g, "LIMITE_DEL_RECORRIDO", 5)
    grande = tmp_path / "t2" / "knowledge" / "feedback"
    for n in range(10):
        _escribir(grande, f"nota-{n}.txt")
    grep = _decide(g, repo, "Grep", {"pattern": "x", "path": str(grande)})
    assert grep is not None and "R_RECORRIDO" in _regla(g, grep)


def test_un_ancestro_de_la_raiz_se_decide_sin_recorrerlo_fuera(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Revisor, B3: un Glob o un Grep desde una carpeta que CONTIENE la raiz se decide por la raiz,
    como en `main`, sin recorrer el resto del ancestro."""

    def no(*_args: object) -> None:
        raise AssertionError("recorrio el ancestro")

    monkeypatch.setattr(g.Politica, "holdout_debajo", no)
    monkeypatch.setattr(g.Politica, "lo_que_alcanza_fuera", no)
    glob = _decide(g, repo, "Glob", {"pattern": "**/*.yaml", "path": str(repo.parent)})
    assert glob is not None and "R_LISTADO" in _regla(g, glob)
    assert _decide(g, repo, "Grep", {"pattern": "x", "path": str(repo.parent)}) is not None


# ------------------------------------------------------------ (d) D2: la carpeta Backtest misma
def _carpetas_backtest(repo: Path, copia: Path) -> list[str]:
    """La carpeta de un mes no legible VACIA (en `main` el Grep solo la negaba si tenia algun
    fichero protegido dentro), dentro del repo y en la copia; y la de marzo con su imagen."""
    return [str(repo / VACIA), str(copia / VACIA), str(repo / BTM), str(copia / BTM)]


def test_la_carpeta_backtest_como_objetivo_de_read_y_grep_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """D2, tras la respuesta del consultor a la PARADA final (punto 2): Read y Grep."""
    fallos = []
    for carpeta in _carpetas_backtest(repo, copia):
        for herramienta, entrada in (
            ("Read", {"file_path": carpeta}),
            ("Grep", {"pattern": "x", "path": carpeta}),
        ):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"D2 | {herramienta} | {obtenida} | {carpeta[-45:]}")
            if obtenida != "R_SIN_ABRIR":
                fallos.append(f"{herramienta} · {carpeta[-45:]}: {obtenida}")
    assert not fallos, "\n".join(fallos)


def test_listar_la_carpeta_backtest_con_ls_get_childitem_o_glob_pasa(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """D2: `ls`, `dir`, `Get-ChildItem` y, desde la respuesta del consultor a la PARADA final
    (punto 2), Glob listan nombres y pasan: listar nombres no es leer contenido (ADR-0021 §1)."""
    fallos = []
    for carpeta in _carpetas_backtest(repo, copia):
        posix = carpeta.replace("\\", "/")
        for herramienta, entrada in (
            ("Bash", {"command": f'ls "{posix}"'}),
            ("Bash", {"command": f'dir "{posix}"'}),
            ("PowerShell", {"command": f"Get-ChildItem '{carpeta}'"}),
            ("Glob", {"pattern": "*", "path": carpeta}),
            ("Glob", {"pattern": posix + "/*.xlsx"}),
        ):
            if _decide(g, repo, herramienta, entrada) is not None:
                fallos.append(f"{herramienta} · {carpeta[-45:]}")
    # Un libro SUELTO `backtesting-analytics ...` no es una carpeta `Backtest <mes>`: su Glob lista
    # un nombre que ya esta en el patron; leerlo lo niega su propia regla.
    if _decide(g, repo, "Glob", {"pattern": str(repo / LIBRO).replace("\\", "/")}) is not None:
        fallos.append("Glob · el libro suelto")
    assert _decide(g, repo, "Read", {"file_path": str(repo / LIBRO)}) is not None
    assert not fallos, "\n".join(fallos)


# ------------------- respuesta del consultor a la PARADA final, punto 1: las clases por fichero
def _niega_en_la_copia(
    g: ModuleType, repo: Path, copia: Path, rel: str, regla: str, texto: str = "dato falso\n"
) -> None:
    _escribir(copia, rel, texto)
    fallos = _fallos(g, repo, [(str(copia / rel), regla)])
    assert not fallos, "\n".join(fallos)


def test_un_tramo_no_citable_en_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """La cruda de un video con tramos no citables (v6, sin cuarentena), con lineas en el tramo."""
    cruda = "[0:10:00] uno\n[0:20:00] dos\n[0:45:00] tres\n[1:00:00] cuatro\n"
    _niega_en_la_copia(g, repo, copia, f"{TRA}/v6/large-v3/cruda.txt", "R_TRAMO", cruda)


def test_un_caso_reservado_en_cases_de_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    _niega_en_la_copia(g, repo, copia, f"knowledge/cases/kit/s1/{CASO}.yaml", "R_CASO")


def test_un_caso_reservado_en_el_visor_de_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    _niega_en_la_copia(g, repo, copia, f"data/visor/{CASO}.html", "R_CASO")


def test_el_feedback_de_un_reservado_en_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    texto = f"accion: LABEL_CASE\ncaso: {CASO}\n"
    _niega_en_la_copia(g, repo, copia, "knowledge/feedback/s1/fb-1.yaml", "R_CASO", texto)


def test_un_fichero_de_la_lista_con_ocultos_en_una_copia_fuera_se_niega(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    _niega_en_la_copia(g, repo, copia, OCULTO, "R_FICHERO_OCULTO")


def test_lo_que_no_es_reservado_en_esas_clases_de_la_copia_pasa(
    g: ModuleType, repo: Path, copia: Path
) -> None:
    """Que los anclajes nuevos no se pasen de frenada: un caso que no es reservado, un feedback
    que no etiqueta ninguno, una cruda de un video sin cuarentena ni tramos, una propuesta que no
    esta en la lista y la cruda de v6 que no toca el tramo, leida por un trozo fuera de el."""
    for rel, texto in (
        ("knowledge/cases/dev/caso-eurusd-2026-04-01.yaml", "x\n"),
        ("knowledge/feedback/s1/fb-2.yaml", "accion: LABEL_CASE\ncaso: caso-eurusd-2026-04-01\n"),
        ("data/visor/caso-eurusd-2026-04-01.html", "x\n"),
        (f"{TRA}/v1/large-v3/cruda.txt", "[0:10:00] uno\n"),
        ("knowledge/_proposals/pr-v1-y.yaml", "x\n"),
    ):
        _escribir(copia, rel, texto)
        ruta = str(copia / rel)
        for etiqueta, herramienta, entrada in _lecturas(ruta):
            assert _decide(g, repo, herramienta, entrada) is None, (etiqueta, rel)
    # Las lineas 2 y 3 caen en el tramo; la guardia deja una de margen a cada lado (`decidir`).
    cruda = "[0:10:00] uno\n[0:20:00] dos\n[0:45:00] tres\n[1:00:00] cuatro\n[1:10:00] cinco\n"
    _escribir(copia, f"{TRA}/v6/large-v3/cruda.txt", cruda)
    ruta = str(copia / TRA / "v6" / "large-v3" / "cruda.txt")
    assert _decide(g, repo, "Read", {"file_path": ruta, "offset": 5, "limit": 1}) is None
