"""El alias de la raiz: la guardia niega el material protegido escriba como se escriba la ruta.

Rama `trabajo/guardia-alias` (2026-10-24, docs/validation/GUARDIA-ALIAS.md). La fase 0 midio 123
lecturas protegidas que pasaban (`docs/validation/anexos/GUARDIA-ALIAS/diagnostico/`): la raiz
escrita con `\\\\?\\`, `//?/`, un UNC a la propia maquina, `\\\\?\\UNC\\`, su nombre corto 8.3 o
un punto final; un lector recursivo sobre una carpeta que CONTIENE la raiz; y variables con un
alias o `$env:` en PowerShell. La condicion (respuesta del consultor a la PARADA 1): toda ruta se
compara en su forma CANONICA (`_canonica`, dentro de `_absoluta`), lo que no se puede canonizar
se niega, un ancestro de la raiz se decide como la raiz, y PowerShell resuelve `$env:`, `$HOME`,
`$PWD` y `~` y niega delante de un lector la variable que no resuelve.

Todo EN MEMORIA, con `decidir`, sobre un repo INVENTADO en `tmp_path` (con un espacio en el nombre,
para que tenga 8.3) y ficheros FALSOS en tres sitios protegidos: nada se ejecuta ni se abre del
repo real. Las formas de prefijo, UNC y 8.3 son de Windows: fuera de Windows van con `skip`
(punto 6 de la respuesta; en Linux esos textos son nombres de fichero raros y no llegan a nada).

ROTO A PROPOSITO, en los dos sentidos: `test_roto_a_proposito` cambia una pieza de la guardia
(`_romper`: sin canonizar, canonizando de mas, sin el contenedor, sin las variables de PowerShell,
sin negar lo no canonizable) y exige que los tests que esa pieza sostiene FALLEN; imprime su
fallo, que va al anexo de la rama. (Primero con una variable de entorno; la guardia la nego por
no estar en `NOMBRES_DE_ENTORNO`, y se siguio su forma, «sin esa variable»: GUARDIA-ALIAS.md §3.)
"""

from __future__ import annotations

import importlib.util
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
EN_WINDOWS = sys.platform == "win32"
SOLO_WINDOWS = pytest.mark.skipif(
    not EN_WINDOWS, reason="prefijos de dispositivo, UNC y 8.3 son de Windows (punto 6)"
)

# Las tres rutas protegidas, a trozos (no se escriben enteras), y la buena.
MARZO = (
    "corp" + "us/Estrategia del trader/Material adicional de su operativa/Back" + "test marzo 2026"
) + "/x.xlsx"
HOLD = "knowledge/cases/hol" + "dout/1/caso.yaml"
CRUDA = "data/transcrip" + "ciones/v7/large-v3/cru" + "da.jsonl"
BUENO = "src/botsito/cli.py"
PROTEGIDOS = {
    "marzo": (MARZO, "R_SIN_ABRIR"),
    "holdout": (HOLD, "R_HOLDOUT"),
    "cruda": (CRUDA, "R_CUARENTENA"),
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


def _romper(cual: str, g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Rompe a proposito una pieza de la guardia (los tests `test_roto_a_proposito_*`)."""
    if cual == "identidad":  # sin canonizar: vuelven a pasar las formas de la raiz
        monkeypatch.setattr(g, "_canonica", lambda ruta: os.path.normpath(ruta))
    elif cual == "todo_es_la_raiz":  # canoniza de mas: todo cae en el holdout, lo bueno se niega
        original = g._canonica

        def de_mas(ruta: str) -> str:
            if g._normcase(ruta) == g._normcase(str(repo)):
                return str(original(ruta))
            return os.path.join(str(repo), *HOLD.split("/"))

        monkeypatch.setattr(g, "_canonica", de_mas)
    elif cual == "sin_contenedor":
        monkeypatch.setattr(g.Politica, "contiene_la_raiz", lambda self, ruta: False)
    elif cual == "sin_variables_ps":
        monkeypatch.setattr(g, "_variables_powershell", lambda texto, ctx: (texto, []))
    elif cual == "sin_no_canonizable":
        monkeypatch.setattr(g, "_no_canonizable", lambda ruta: ruta)
    elif cual == "una_lectura":  # PARADA 2, punto 0: sin la lectura con un nivel de `\\` menos
        monkeypatch.setattr(g, "_lecturas_de_la_herramienta", lambda texto: [texto])
    elif cual == "sin_tilde_de_pila":
        monkeypatch.setattr(g, "_tilde_de_bash", lambda ruta, cwd: os.path.expanduser(ruta))
    elif cual == "sin_proc_cygdrive":
        monkeypatch.setattr(g, "_UNIDAD_MSYS", re.compile(r"^/(?:cygdrive/)?([a-zA-Z])(/.*)?$"))
    elif cual == "sin_unidad_sin_barra":
        monkeypatch.setattr(g, "_relativa_a_unidad", lambda ruta, cwd: ruta)
    elif cual == "sin_disfraz_posix":  # pasada corta del revisor: sin normalizar `/proc/...`
        monkeypatch.setattr(g, "_sin_disfraz_posix", lambda ruta, cwd: ruta)
    elif cual == "sin_prefijos_tras_realpath":  # m1: lo que da realpath, sin quitar prefijos
        monkeypatch.setattr(g, "_tras_realpath", lambda real: os.path.normpath(real))
    elif cual == "sin_proveedor":
        monkeypatch.setattr(g, "_sin_proveedor", lambda ruta: ruta)
    else:
        raise AssertionError(cual)


def _git(repo: Path, *args: str) -> None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, env=env)


def _escribir(repo: Path, rel: str, texto: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """El repo inventado de la fase 0 (`medir_k.py`): la estructura del real, con ficheros falsos
    SIN SEGUIR donde el material protegido. Su nombre lleva un espacio, para que tenga 8.3."""
    r = tmp_path / "Bot v3 prueba"
    r.mkdir()
    _escribir(r, "Makefile", "x\n")
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _escribir(r, "knowledge/corpus/fuentes.yaml", "videos:\n  - video_id: v7\n    drive_id: null\n")
    _escribir(
        r,
        "knowledge/cases/kit/s1/particiones.yaml",
        "asignacion:\n  caso-eurusd-2026-05-04: holdout-1\ncupos:\n  dev: 0\n",
    )
    _escribir(r, BUENO, "x = 1\n")
    _escribir(r, "docs/a.md", "x\n")
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    for rel, _ in PROTEGIDOS.values():
        _escribir(r, rel, "dato falso\n")
    (tmp_path / "hermana").mkdir()
    _escribir(tmp_path / "hermana", "nota.txt", "x\n")
    (tmp_path / "fuera").mkdir()
    return r


def _decide(g: ModuleType, repo: Path, herramienta: str, entrada: dict[str, Any]) -> str | None:
    evento = {"tool_name": herramienta, "tool_input": entrada, "cwd": str(repo)}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _regla(g: ModuleType, motivo: str | None) -> str:
    if motivo is None:
        return "pasa"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    return ",".join(sorted(nombres)) or "niega (sin R_)"


def _corta(ruta: str) -> str:
    """El nombre corto 8.3 de `ruta` (metadatos), o `ruta` si el volumen no los tiene."""
    if sys.platform != "win32":  # para mypy en Linux, que no conoce `windll`
        return ruta
    import ctypes

    buffer = ctypes.create_unicode_buffer(1024)
    ctypes.windll.kernel32.GetShortPathNameW(ruta, buffer, 1024)
    return buffer.value or ruta


def _formas(repo: Path, rel: str) -> list[tuple[str, str]]:
    """Las formas de Windows de `<raiz>\\<rel>` que hoy en `main` pasan (fase 0, §0.a), y sus
    disfraces: mayusculas cambiadas, barras mezcladas, `.` y `..` intercalados, el punto final."""
    r = str(repo)
    rw = rel.replace("/", "\\")
    unidad, sin_unidad = r[0], r[2:]
    import socket

    equipo = socket.gethostname()
    corta = _corta(r)
    formas = [
        ("\\\\?\\", f"\\\\?\\{r}\\{rw}"),
        ("//?/", f"//?/{r.replace(chr(92), '/')}/{rel}"),
        ("UNC localhost", f"\\\\localhost\\{unidad}${sin_unidad}\\{rw}"),
        ("UNC 127.0.0.1", f"\\\\127.0.0.1\\{unidad}${sin_unidad}\\{rw}"),
        ("UNC con /", f"//localhost/{unidad}${sin_unidad.replace(chr(92), '/')}/{rel}"),
        ("UNC el equipo", f"\\\\{equipo}\\{unidad}${sin_unidad}\\{rw}"),
        ("\\\\?\\UNC\\localhost", f"\\\\?\\UNC\\localhost\\{unidad}${sin_unidad}\\{rw}"),
        ("punto final", f"{r}.\\{rw}"),
        ("\\\\.\\ unidad", f"\\\\.\\{r}\\{rw}"),
        # Disfraces de la misma familia
        ("\\\\?\\ en MAYUSCULAS", f"\\\\?\\{r.upper()}\\{rw.upper()}"),
        ("//?/ con barras mezcladas", f"//?/{r}\\{rel}"),
        ("\\\\?\\ con . y ..", f"\\\\?\\{r}\\.\\docs\\..\\{rw}"),
        ("UNC con la unidad en minuscula", f"\\\\LOCALHOST\\{unidad.lower()}${sin_unidad}\\{rw}"),
        ("punto final y \\\\?\\", f"\\\\?\\{r}.\\{rw}"),
    ]
    if corta.lower() != r.lower():
        formas += [("8.3", f"{corta}\\{rw}"), ("8.3 con //?/", f"//?/{corta}\\{rw}")]
    return formas


def _herramientas(ruta: str, fuera: Path) -> list[tuple[str, str, dict[str, Any]]]:
    """La misma lectura por cada herramienta que la guardia decide."""
    guion = fuera / "guion.py"
    guion.write_text(f"print(open(r'{ruta}', encoding='utf-8').read())\n", encoding="utf-8")
    # Entre comillas simples, la guardia ve la ruta tal cual. (La herramienta Bash de Claude Code
    # quita un nivel de `\` ANTES de bash, tambien entre simples: revisor, a1 y b1; GUARDIA-ALIAS.md
    # §8. Ese hueco, con las barras dobladas, queda para el consultor.)
    cat = f"cat '{ruta}'"
    return [
        ("Bash cat", "Bash", {"command": cat}),
        ("Read", "Read", {"file_path": ruta}),
        ("Grep", "Grep", {"pattern": "x", "path": ruta}),
        ("PowerShell Get-Content", "PowerShell", {"command": f"Get-Content '{ruta}'"}),
        ("Monitor cat", "Monitor", {"command": cat, "description": "x", "timeout_ms": 1000}),
        ("python guion", "Bash", {"command": f'python "{guion.as_posix()}"'}),
    ]


# ------------------------------------------------------------------ a) las formas de la raiz
@SOLO_WINDOWS
@pytest.mark.parametrize("sitio", sorted(PROTEGIDOS))
def test_cada_forma_de_la_raiz_se_niega_con_la_regla_del_sitio(
    g: ModuleType, repo: Path, sitio: str
) -> None:
    rel, esperada = PROTEGIDOS[sitio]
    fallos = []
    for forma, ruta in _formas(repo, rel):
        for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera"):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"{sitio} | {forma} | {etiqueta} | {obtenida}")
            if esperada not in obtenida.split(","):
                fallos.append(f"{forma} · {etiqueta}: {obtenida}")
    assert not fallos, "\n".join(fallos)


@SOLO_WINDOWS
def test_lo_bueno_pasa_con_cada_forma_de_la_raiz(g: ModuleType, repo: Path) -> None:
    fallos = []
    for forma, ruta in _formas(repo, BUENO):
        for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera"):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"bueno | {forma} | {etiqueta} | {obtenida}")
            if obtenida != "pasa":
                fallos.append(f"{forma} · {etiqueta}: {obtenida}")
    assert not fallos, "\n".join(fallos)


def test_lo_bueno_pasa_en_las_formas_de_siempre(g: ModuleType, repo: Path) -> None:
    """En los dos sistemas: relativa, absoluta con las dos barras, `.` y `..`, y los programas de
    datos que pasaban en `main` (lecciones de `trabajo/guardia-ci`, ERRORES-RECURRENTES.md)."""
    r = str(repo)
    rutas = [BUENO, f"{r}{os.sep}{BUENO}", f"{r}/{BUENO}", f"{r}/./docs/../{BUENO}"]
    comandos = [
        "grep -rn x docs/",
        "grep -r x docs",
        "rg x docs",
        f"wc -c '{MARZO}'",
        f"sha256sum '{repo / MARZO}'",
        f"stat '{repo / HOLD}'",
        f'grep -rn x "{repo / "docs"}"',
        "ls -la",
        f"ls '{repo.parent}'",
    ]
    fallos = []
    for ruta in rutas:
        for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera"):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            if obtenida != "pasa":
                fallos.append(f"ruta {rutas.index(ruta)} · {etiqueta}: {obtenida}")
    for comando in comandos:
        obtenida = _regla(g, _decide(g, repo, "Bash", {"command": comando}))
        print(f"bueno | comando {comandos.index(comando)} | {obtenida}")
        if obtenida != "pasa":
            fallos.append(f"comando {comandos.index(comando)}: {obtenida}")
    assert not fallos, "\n".join(fallos)


# ------------------------------------------------- b) una carpeta que CONTIENE la raiz
def _contenedores(repo: Path) -> list[tuple[str, str]]:
    salida = [("la carpeta del repo", str(repo.parent)), ("la de encima", str(repo.parent.parent))]
    if EN_WINDOWS:
        salida.append(("la carpeta del repo con \\\\?\\", "\\\\?\\" + str(repo.parent)))
        salida.append(("la carpeta del repo con //?/", "//?/" + repo.parent.as_posix()))
        # Disfraces de la familia (revisor, b10): mayusculas, barras mezcladas, `.` y `..`
        salida.append(("en MAYUSCULAS", str(repo.parent).upper()))
        salida.append(("con barras mezcladas y ..", f"{repo.parent}/x\\..\\."))
    salida.append(("con /./ al final", f"{repo.parent.as_posix()}/./"))
    return salida


def _lecturas_recursivas(d: str) -> list[tuple[str, str, dict[str, Any]]]:
    df = d.replace("\\", "/")
    return [
        ("grep -r", "Bash", {"command": f'grep -r x "{df}"'}),
        ("grep -R con mayuscula", "Bash", {"command": f'grep -R x "{df}"'}),
        ("find -exec cat", "Bash", {"command": f'find "{df}" -name "*.yaml" -exec cat {{}} \\;'}),
        ("cp -r", "Bash", {"command": f'cp -r "{df}" /tmp/copia'}),
        ("rg --no-ignore", "Bash", {"command": f'rg --no-ignore x "{df}"'}),
        ("Grep", "Grep", {"pattern": "x", "path": d}),
        ("Monitor grep -r", "Monitor", {"command": f'grep -r x "{df}"', "description": "x"}),
    ]


def test_un_lector_recursivo_sobre_una_carpeta_que_contiene_la_raiz_se_niega(
    g: ModuleType, repo: Path
) -> None:
    fallos = []
    for nombre, d in _contenedores(repo):
        for etiqueta, herramienta, entrada in _lecturas_recursivas(d):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"contenedor | {nombre} | {etiqueta} | {obtenida}")
            if obtenida == "pasa" or obtenida.startswith("niega"):
                fallos.append(f"{nombre} · {etiqueta}: {obtenida}")
    assert not fallos, "\n".join(fallos)


def test_rg_desde_fuera_respeta_lo_ignorado_como_desde_la_raiz(g: ModuleType, repo: Path) -> None:
    """Punto 4: el contenedor se decide como la raiz CON su `respeta_ignore`: `rg` sin
    `--no-ignore` no entra en `corpus/` ni `data/` (ignorados), pero si en el holdout."""
    obtenida = _regla(g, _decide(g, repo, "Bash", {"command": f'rg x "{repo.parent.as_posix()}"'}))
    assert obtenida == "R_HOLDOUT"


def test_una_carpeta_hermana_sin_el_repo_pasa(g: ModuleType, repo: Path) -> None:
    hermana = repo.parent / "hermana"
    fallos = []
    for etiqueta, herramienta, entrada in _lecturas_recursivas(str(hermana)):
        if etiqueta == "cp -r":
            continue  # escribe en /tmp: no es lo que se mide
        obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
        if obtenida != "pasa":
            fallos.append(f"{etiqueta}: {obtenida}")
    assert not fallos, "\n".join(fallos)


# ------------------------------------------------------------------------- c) las variables
@SOLO_WINDOWS
def test_una_variable_de_bash_con_un_alias_se_niega(g: ModuleType, repo: Path) -> None:
    r = repo.as_posix()
    casos = [
        f'S="//?/{r}"; cat "$S/{MARZO}"',
        f"S='\\\\?\\{repo}'; cat \"$S/{MARZO}\"",
        f"S='//localhost/{r[0]}${r[2:]}'; cat \"$S/{MARZO}\"",
    ]
    corta = _corta(str(repo))
    if corta.lower() != str(repo).lower():
        casos.append(f'S="{corta}"; cat "$S/{MARZO}"')
    fallos = []
    for comando in casos:
        obtenida = _regla(g, _decide(g, repo, "Bash", {"command": comando}))
        print(f"variable bash | caso {casos.index(comando)} | {obtenida}")
        if obtenida != "R_SIN_ABRIR":
            fallos.append(f"caso {casos.index(comando)}: {obtenida}")
    # `export S=...` no fija una variable que la guardia siga: el lector se niega por no saber
    # la ruta, como en `main` (no es la regla del sitio, pero tampoco pasa).
    exportada = f'export S="//?/{r}"; cat "$S/{MARZO}"'
    assert _decide(g, repo, "Bash", {"command": exportada}) is not None
    assert not fallos, "\n".join(fallos)


def test_powershell_resuelve_env_home_pwd_y_tilde(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    casa = repo.parent
    monkeypatch.setenv("USERPROFILE", str(casa))
    monkeypatch.setenv("HOME", str(casa))
    monkeypatch.setenv("GUARDIA_ALIAS_PRUEBA", str(repo))
    # Con `\` en Windows (lo que se escribe alli) y con `/` fuera, donde `\` es parte del nombre.
    s = "\\" if EN_WINDOWS else "/"
    m = MARZO.replace("/", s)
    nombre = repo.name
    casos = [
        f'Get-Content "$env:USERPROFILE{s}{nombre}{s}{m}"',
        f'Get-Content "$env:GUARDIA_ALIAS_PRUEBA{s}{m}"',
        f'Get-Content "$env:CLAUDE_PROJECT_DIR{s}{m}"',
        f'Get-Content "$HOME{s}{nombre}{s}{m}"',
        f'Get-Content "$PWD{s}{m}"',
        f'Get-Content "~{s}{nombre}{s}{m}"',
        f'Get-Content "$env:GUARDIA_ALIAS_PRUEBA/./docs/../{MARZO}"',  # disfraz: barras y ..
    ]
    # Disfraz: mayusculas cambiadas. En Windows el entorno no distingue mayusculas y se resuelve;
    # en Linux si las distingue, no se resuelve y se niega (`R_ALIAS`): CI run 40132371656.
    cambiada = f'Get-Content "$ENV:userprofile{s}{nombre}{s}{m}"'
    if EN_WINDOWS:
        casos.append(cambiada)
    else:
        assert "R_ALIAS" in _regla(g, _decide(g, repo, "PowerShell", {"command": cambiada}))
    fallos = []
    for comando in casos:
        obtenida = _regla(g, _decide(g, repo, "PowerShell", {"command": comando}))
        print(f"powershell | caso {casos.index(comando)} | {obtenida}")
        if obtenida != "R_SIN_ABRIR":
            fallos.append(f"caso {casos.index(comando)}: {obtenida}")
    # `${env:X}` (un bloque) y `gc` (fuera de la lista cerrada) ya se niegan como ejecucion.
    for comando in (
        f'Get-Content "${{env:USERPROFILE}}\\{nombre}\\{m}"',
        f'gc "$env:USERPROFILE\\{nombre}\\{m}"',
    ):
        assert _decide(g, repo, "PowerShell", {"command": comando}) is not None, comando
    assert not fallos, "\n".join(fallos)


def test_powershell_niega_una_variable_que_no_resuelve_delante_de_un_lector(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("GUARDIA_ALIAS_NO_EXISTE", raising=False)
    for comando in (
        'Get-Content "$env:GUARDIA_ALIAS_NO_EXISTE\\a.txt"',
        'Get-Content "$algo\\a.txt"',
        "Get-Content $env:GUARDIA_ALIAS_NO_EXISTE",
    ):
        motivo = _decide(g, repo, "PowerShell", {"command": comando})
        assert motivo is not None and "R_ALIAS" in _regla(g, motivo), (comando, motivo)


def test_powershell_lo_bueno_y_lo_literal_pasan(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GUARDIA_ALIAS_PRUEBA", str(repo))
    casos = [
        'Get-Content "$env:GUARDIA_ALIAS_PRUEBA\\src\\botsito\\cli.py"',
        'Get-Content "$PWD\\src\\botsito\\cli.py"',
        'Get-Content "%USERPROFILE%\\x.txt"',  # PowerShell no lo expande: es un nombre
        "Get-ChildItem $env:GUARDIA_ALIAS_PRUEBA",  # sin lector
        "Write-Output $algo",
    ]
    if EN_WINDOWS:  # el `?` del prefijo no es un comodin (fase 0, §0.g)
        casos += [f"Get-Content '\\\\?\\{repo}\\src\\botsito\\cli.py'"]
    fallos = []
    for comando in casos:
        obtenida = _regla(g, _decide(g, repo, "PowerShell", {"command": comando}))
        if obtenida != "pasa":
            fallos.append(f"{comando}: {obtenida}")
    assert not fallos, "\n".join(fallos)


# --------------------------------------------------------------- lo que no se puede canonizar
@SOLO_WINDOWS
@pytest.mark.parametrize(
    "ruta",
    [
        "\\\\otra-maquina\\C$\\x\\y.txt",
        "//otra-maquina/C$/x/y.txt",
        "\\\\localhost\\compartida\\x\\y.txt",
        "\\\\.\\pipe\\x",
        "\\\\?\\GLOBALROOT\\Device\\HarddiskVolume1\\x\\y.txt",
        "\\\\?\\Volume{00000000-0000-0000-0000-000000000000}\\x\\y.txt",
        "\\\\?\\UNC\\otra-maquina\\C$\\x\\y.txt",
    ],
)
def test_lo_que_no_se_puede_canonizar_se_niega_con_la_forma_buena(
    g: ModuleType, repo: Path, ruta: str
) -> None:
    for herramienta, entrada in (
        ("Bash", {"command": f"cat '{ruta}'"}),
        ("Read", {"file_path": ruta}),
        ("Grep", {"pattern": "x", "path": ruta}),
    ):
        motivo = _decide(g, repo, herramienta, entrada)
        assert motivo is not None and "R_ALIAS" in _regla(g, motivo), (herramienta, motivo)
        assert "no se puede canonizar" in motivo and "desde la raiz" in motivo


def test_fuera_de_windows_los_prefijos_no_se_tocan(g: ModuleType) -> None:
    """Punto 6: en Linux `\\\\?\\C:\\x` es un nombre de fichero; la canonizacion no lo inventa."""
    if EN_WINDOWS:
        assert g._canonica("\\\\?\\C:\\x\\y") == "C:\\x\\y"
    else:
        assert "?" in g._canonica("/tmp/\\\\?\\C:\\x")


# ------------------------------------------------------------- d) enlaces y uniones (punto 1)
def _enlace(enlace: Path, destino: Path) -> None:
    if EN_WINDOWS:
        subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(enlace), str(destino)],
            check=True,
            capture_output=True,
        )
    else:
        enlace.symlink_to(destino, target_is_directory=True)


def test_leer_por_una_union_o_un_enlace_hacia_lo_protegido_se_niega(
    g: ModuleType, repo: Path
) -> None:
    _enlace(repo / "docs" / "atajo", (repo / HOLD).parent)
    _enlace(repo / "docs" / "atajo_src", repo / "src")
    malo = str(repo / "docs" / "atajo" / "caso.yaml")
    bueno = str(repo / "docs" / "atajo_src" / "botsito" / "cli.py")
    fallos = []
    for ruta, esperada in ((malo, "R_HOLDOUT"), (bueno, "pasa")):
        for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera"):
            obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
            print(f"enlace | {esperada} | {etiqueta} | {obtenida}")
            if obtenida != esperada:
                fallos.append(f"{ruta[-30:]} · {etiqueta}: {obtenida}")
    assert not fallos, "\n".join(fallos)


# ---------------------------- respuesta a la PARADA 2: lo que el revisor encontro abierto (§9)
def _bash_y_monitor(comando: str) -> list[tuple[str, str, dict[str, Any]]]:
    return [
        ("Bash", "Bash", {"command": comando}),
        ("Monitor", "Monitor", {"command": comando, "description": "x", "timeout_ms": 1000}),
    ]


def _dobladas(repo: Path, rel: str) -> list[tuple[str, str]]:
    """Las 18 filas de b1: `\\\\?\\`, UNC a `localhost` y `\\\\?\\UNC\\`, con cada `\\` DOBLADA,
    como hay que escribirlas para que la herramienta Bash le entregue a bash la buena."""
    r = str(repo)
    rw = rel.replace("/", "\\")
    unidad, sin_unidad = r[0], r[2:]
    formas = [
        ("\\\\?\\", f"\\\\?\\{r}\\{rw}"),
        ("UNC localhost", f"\\\\localhost\\{unidad}${sin_unidad}\\{rw}"),
        ("\\\\?\\UNC\\localhost", f"\\\\?\\UNC\\localhost\\{unidad}${sin_unidad}\\{rw}"),
    ]
    return [(f, ruta.replace("\\", "\\\\")) for f, ruta in formas]


def _fallos_dobladas(g: ModuleType, repo: Path, rel: str, esperada: str) -> list[str]:
    fallos = []
    for forma, doblada in _dobladas(repo, rel):
        for comillas in ("'", '"'):
            for etiqueta, herramienta, entrada in _bash_y_monitor(
                f"cat {comillas}{doblada}{comillas}"
            ):
                obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
                destino = "src" if rel == BUENO else "protegido"  # pasada minima, c4
                print(f"dobladas | {destino} | {forma} | {comillas} | {etiqueta} | {obtenida}")
                if (esperada == "pasa") != (obtenida == "pasa") or (
                    esperada != "pasa" and esperada not in obtenida.split(",")
                ):
                    fallos.append(f"{forma} · {comillas} · {etiqueta}: {obtenida}")
    return fallos


@SOLO_WINDOWS
def test_las_barras_dobladas_de_la_herramienta_se_niegan(g: ModuleType, repo: Path) -> None:
    """Punto 0: la guardia decide el texto tal como llega y con un nivel de `\\` menos."""
    fallos = []
    for rel, esperada in PROTEGIDOS.values():
        fallos += _fallos_dobladas(g, repo, rel, esperada)
    fallos += _fallos_dobladas(g, repo, BUENO, "pasa")
    assert not fallos, "\n".join(fallos)


def _fallos_de(
    g: ModuleType, repo: Path, casos: list[tuple[str, str, dict[str, Any], str]]
) -> list[str]:
    fallos = []
    for n, (etiqueta, herramienta, entrada, esperada) in enumerate(casos):
        obtenida = _regla(g, _decide(g, repo, herramienta, entrada))
        print(f"caso {n} | {etiqueta} | {obtenida}")
        if obtenida != esperada:
            fallos.append(f"caso {n} ({etiqueta}): {obtenida}, se esperaba {esperada}")
    return fallos


def test_tilde_mas_y_tilde_menos_de_bash(g: ModuleType, repo: Path) -> None:
    """Punto 1: `~+` es el directorio de trabajo; `~-` y `~+N` no se saben: `R_ALIAS`."""
    casos = []
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat ~+/'{HOLD}'"):
        casos.append((f"~+ hacia el holdout, {etiqueta}", herramienta, entrada, "R_HOLDOUT"))
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat ~+/{BUENO}"):
        casos.append((f"~+ hacia src, {etiqueta}", herramienta, entrada, "pasa"))
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat ~-/'{HOLD}'"):
        casos.append((f"~- hacia el holdout, {etiqueta}", herramienta, entrada, "R_ALIAS"))
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat ~+1/{BUENO}"):
        casos.append((f"~+1, {etiqueta}", herramienta, entrada, "R_ALIAS"))
    casos.append(("~ sigue siendo la casa", "Bash", {"command": "cat ~/x.txt"}, "pasa"))
    fallos = _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


def _regla_de_la_raiz(g: ModuleType, repo: Path) -> str:
    """La regla con que se niega `grep -r` sobre la raiz escrita normal: la misma que tiene que
    salir por cualquier alias de la raiz."""
    return _regla(g, _decide(g, repo, "Bash", {"command": "cd src && grep -r x .."}))


def test_proc_self_cwd_es_el_directorio_de_trabajo(g: ModuleType, repo: Path) -> None:
    """Pasada corta del revisor, b2: `/proc/self/cwd/` es el directorio de trabajo (como `~+`);
    el de otro proceso o `/proc/self/root/` no se saben: `R_ALIAS`."""
    casos = []
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat '/proc/self/cwd/{HOLD}'"):
        casos.append((f"/proc/self/cwd al holdout, {etiqueta}", herramienta, entrada, "R_HOLDOUT"))
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat '/proc//self/./cwd/{HOLD}'"):
        casos.append((f"/proc/self/cwd con disfraz, {etiqueta}", herramienta, entrada, "R_HOLDOUT"))
    for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat /proc/self/cwd/{BUENO}"):
        casos.append((f"/proc/self/cwd a src, {etiqueta}", herramienta, entrada, "pasa"))
    casos += [
        ("/proc/1/cwd", "Bash", {"command": f"cat '/proc/1/cwd/{BUENO}'"}, "R_ALIAS"),
        ("/proc/self/root", "Bash", {"command": f"cat '/proc/self/root/{BUENO}'"}, "R_ALIAS"),
        # `..` DESPUES de traducir `cwd` (pasada minima, c1): desde `src/`, la raiz del repo.
        ("cwd/.. desde src", "Bash", {"command": "cd src && grep -r x /proc/self/cwd/.."}, "?"),
        (
            "cwd/../src desde src",
            "Bash",
            {"command": f"cd src && cat /proc/self/cwd/../{BUENO}"},
            "pasa",
        ),
        # Lo que no es un enlace de /proc no lleva a ningun fichero (c2): como en `main`.
        ("/proc/self/status", "Bash", {"command": "cat /proc/self/status"}, "pasa"),
    ]
    obtenida = _regla(g, _decide(g, repo, "Grep", {"pattern": "x", "path": "/proc/self/cwd/.."}))
    print(f"Grep /proc/self/cwd/.. desde la raiz (su padre contiene el repo) | {obtenida}")
    assert obtenida not in {"pasa"} and not obtenida.startswith("niega"), obtenida
    casos = [c if c[3] != "?" else (*c[:3], _regla_de_la_raiz(g, repo)) for c in casos]
    fallos = _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


@SOLO_WINDOWS
def test_proc_cygdrive_es_la_unidad(g: ModuleType, repo: Path) -> None:
    """Punto 1: `/proc/cygdrive/c/...` de MSYS es `C:/...`, como `/c/` y `/cygdrive/c/`."""
    r = repo.as_posix()
    u, resto = r[0].lower(), r[2:]
    # La forma y sus disfraces que abren en Git Bash (revisor, pasada corta, b1).
    formas = {
        "/proc/cygdrive": f"/proc/cygdrive/{u}{resto}",
        "/proc//cygdrive": f"/proc//cygdrive/{u}{resto}",
        "/proc/cygdrive//": f"/proc/cygdrive//{u}{resto}",
        "/proc/./cygdrive": f"/proc/./cygdrive/{u}{resto}",
        "/proc/x/../cygdrive": f"/proc/x/../cygdrive/{u}{resto}",
    }
    casos = []
    for nombre, msys in formas.items():
        for sitio, (rel, esperada) in PROTEGIDOS.items():
            for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat '{msys}/{rel}'"):
                casos.append((f"{sitio} por {nombre}, {etiqueta}", herramienta, entrada, esperada))
        for etiqueta, herramienta, entrada in _bash_y_monitor(f"cat '{msys}/{BUENO}'"):
            casos.append((f"src por {nombre}, {etiqueta}", herramienta, entrada, "pasa"))
    fallos = _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


@SOLO_WINDOWS
def test_la_unidad_sin_barra_es_relativa_al_directorio_de_esa_unidad(
    g: ModuleType, repo: Path
) -> None:
    """Punto 1: `C:x`, con la unidad del directorio de trabajo, cuelga de el; otra unidad que la
    del repositorio no puede caer bajo la raiz y se deja."""
    unidad = str(repo)[0]
    otra = next(u for u in "ZYXWV" if u != unidad.upper())
    # Cada grupo se decide nada mas crearlo: `_herramientas` reescribe el guion de Python.
    fallos = []
    grupos = [
        (sitio, f"{unidad}:{rel.replace('/', chr(92))}", e)
        for sitio, (rel, e) in PROTEGIDOS.items()
    ]
    grupos.append(("src", f"{unidad}:src\\botsito\\cli.py", "pasa"))
    for sitio, ruta, esperada in grupos:
        casos = [
            (f"{sitio} · {etiqueta}", herramienta, entrada, esperada)
            for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera")
        ]
        fallos += _fallos_de(g, repo, casos)
    otra_unidad = ("otra unidad", "Read", {"file_path": f"{otra}:x\\y.txt"}, "pasa")
    fallos += _fallos_de(g, repo, [otra_unidad])
    # La unidad del repo con el directorio de trabajo en OTRA unidad: el de la del repo no se sabe
    # (revisor, pasada corta, b3), hacia lo protegido y hacia lo bueno.
    for rel in (HOLD, BUENO):
        entrada = {"file_path": f"{unidad}:{rel.replace('/', chr(92))}"}
        evento = {"tool_name": "Read", "tool_input": entrada, "cwd": f"{otra}:\\x"}
        obtenida = _regla(g, g.decidir(evento, g.Politica(repo)))
        print(f"cwd en otra unidad | {rel == BUENO and 'src' or 'holdout'} | {obtenida}")
        if obtenida != "R_ALIAS":
            fallos.append(f"cwd en otra unidad ({rel == BUENO and 'src' or 'holdout'}): {obtenida}")
    assert not fallos, "\n".join(fallos)


@SOLO_WINDOWS
def test_otra_unidad_se_canoniza_y_se_niega_si_cae_bajo_la_raiz(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Orden de cierre, punto 1: `D:x` de otra unidad no pasa por ser otra unidad. Con `subst` o
    una unidad de red puede apuntar a una carpeta que contiene el repo: se canoniza y se compara.
    La unidad se SIMULA (monkeypatch de `_unidad_completa`, sin tocar el sistema): una apunta al
    ancestro de la raiz y otra a una carpeta ajena."""
    unidad = str(repo)[0].upper()
    subst = next(u for u in "QRSTU" if u != unidad)
    ajena = next(u for u in "VWXYZ" if u != unidad)
    destinos = {subst: repo.parent, ajena: repo.parent / "hermana"}
    original = g._unidad_completa

    def simulada(ruta: str) -> str:
        letra = ruta[0].upper()
        if letra in destinos:
            return str(destinos[letra] / ruta[2:])
        return str(original(ruta))

    monkeypatch.setattr(g, "_unidad_completa", simulada)
    grupos = [
        (sitio, f"{subst}:{repo.name}\\{rel.replace('/', chr(92))}", esperada)
        for sitio, (rel, esperada) in PROTEGIDOS.items()
    ]
    grupos.append(
        ("src por la unidad simulada", f"{subst}:{repo.name}\\src\\botsito\\cli.py", "pasa")
    )
    grupos.append(("la unidad ajena", f"{ajena}:nota.txt", "pasa"))
    fallos = []
    for sitio, ruta, esperada in grupos:  # cada grupo, nada mas crearlo (el guion se reescribe)
        casos = [
            (f"{sitio} · {etiqueta}", herramienta, entrada, esperada)
            for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera")
        ]
        fallos += _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


@SOLO_WINDOWS
def test_una_unidad_mapeada_a_la_propia_maquina_se_compara_como_la_unidad(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Revisor, pasada minima previa al cierre, m1: `realpath` sobre una unidad de red mapeada a
    la propia maquina da `\\\\localhost\\C$\\...`, y eso se compara como `C:\\...`. La unidad se
    SIMULA (monkeypatch de `_realpath`, sin `net use`): `Q:\\` es el padre del repo visto por la
    red; `V:\\` es una unidad de OTRA maquina, que no se puede canonizar."""
    r = str(repo.parent)
    por_la_red = f"\\\\localhost\\{r[0]}${r[2:]}"
    original = g._realpath

    def simulada(ruta: str) -> str:
        if ruta[:2].upper() == "Q:":
            return por_la_red + ruta[2:]
        if ruta[:2].upper() == "V:":
            return "\\\\otra-maquina\\datos" + ruta[2:]
        return str(original(ruta))

    monkeypatch.setattr(g, "_realpath", simulada)
    grupos = [
        (sitio, f"Q:\\{repo.name}\\{rel.replace('/', chr(92))}", esperada)
        for sitio, (rel, esperada) in PROTEGIDOS.items()
    ]
    grupos.append(("src por la unidad mapeada", f"Q:\\{repo.name}\\src\\botsito\\cli.py", "pasa"))
    grupos.append(("una unidad de otra maquina", "V:\\x\\y.txt", "R_ALIAS"))
    fallos = []
    for sitio, ruta, esperada in grupos:
        casos = [
            (f"{sitio} · {etiqueta}", herramienta, entrada, esperada)
            for etiqueta, herramienta, entrada in _herramientas(ruta, repo.parent / "fuera")
            if etiqueta in {"Read", "Bash cat", "Grep"}
        ]
        fallos += _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


def test_el_proveedor_filesystem_de_powershell(g: ModuleType, repo: Path) -> None:
    """Punto 1: `FileSystem::<ruta>` y `Microsoft.PowerShell.Core\\FileSystem::<ruta>`."""
    r = repo.as_posix()
    casos = []
    for prefijo in ("FileSystem::", "Microsoft.PowerShell.Core\\FileSystem::", "filesystem::"):
        for sitio, (rel, esperada) in PROTEGIDOS.items():
            comando = f"Get-Content '{prefijo}{r}/{rel}'"
            casos.append((f"{prefijo} {sitio}", "PowerShell", {"command": comando}, esperada))
        bueno = f"Get-Content '{prefijo}{r}/{BUENO}'"
        casos.append((f"{prefijo} src", "PowerShell", {"command": bueno}, "pasa"))
    fallos = _fallos_de(g, repo, casos)
    assert not fallos, "\n".join(fallos)


# ------------------------------------------------------------ roto a proposito (los dos sentidos)
# Cada pieza, con los tests que sostiene: con la pieza rota, cada uno de ellos tiene que FALLAR.
def _w(rotura: str, nombre: str) -> Any:
    return pytest.param(rotura, nombre, marks=SOLO_WINDOWS)


ROTURAS = [
    _w("identidad", "test_cada_forma_de_la_raiz_se_niega_con_la_regla_del_sitio"),
    _w("identidad", "test_una_variable_de_bash_con_un_alias_se_niega"),
    _w("identidad", "test_lo_que_no_se_puede_canonizar_se_niega_con_la_forma_buena"),
    ("identidad", "test_leer_por_una_union_o_un_enlace_hacia_lo_protegido_se_niega"),
    _w("todo_es_la_raiz", "test_lo_bueno_pasa_con_cada_forma_de_la_raiz"),
    ("todo_es_la_raiz", "test_lo_bueno_pasa_en_las_formas_de_siempre"),
    ("todo_es_la_raiz", "test_una_carpeta_hermana_sin_el_repo_pasa"),
    ("sin_contenedor", "test_un_lector_recursivo_sobre_una_carpeta_que_contiene_la_raiz_se_niega"),
    ("sin_contenedor", "test_rg_desde_fuera_respeta_lo_ignorado_como_desde_la_raiz"),
    ("sin_variables_ps", "test_powershell_resuelve_env_home_pwd_y_tilde"),
    ("sin_variables_ps", "test_powershell_niega_una_variable_que_no_resuelve_delante_de_un_lector"),
    _w("sin_no_canonizable", "test_lo_que_no_se_puede_canonizar_se_niega_con_la_forma_buena"),
    # Revisor, b9: los dos que no se rompian nunca.
    ("todo_es_la_raiz", "test_powershell_lo_bueno_y_lo_literal_pasan"),
    _w("identidad", "test_fuera_de_windows_los_prefijos_no_se_tocan"),
    # Respuesta a la PARADA 2: cada condicion nueva, rota; y el otro sentido, canonizando de mas.
    _w("una_lectura", "test_las_barras_dobladas_de_la_herramienta_se_niegan"),
    _w("todo_es_la_raiz", "test_las_barras_dobladas_de_la_herramienta_se_niegan"),
    ("sin_tilde_de_pila", "test_tilde_mas_y_tilde_menos_de_bash"),
    ("todo_es_la_raiz", "test_tilde_mas_y_tilde_menos_de_bash"),
    _w("sin_proc_cygdrive", "test_proc_cygdrive_es_la_unidad"),
    _w("todo_es_la_raiz", "test_proc_cygdrive_es_la_unidad"),
    _w("sin_unidad_sin_barra", "test_la_unidad_sin_barra_es_relativa_al_directorio_de_esa_unidad"),
    # Orden de cierre, punto 1: otra unidad que apunta a un ancestro de la raiz.
    _w("sin_unidad_sin_barra", "test_otra_unidad_se_canoniza_y_se_niega_si_cae_bajo_la_raiz"),
    _w("todo_es_la_raiz", "test_otra_unidad_se_canoniza_y_se_niega_si_cae_bajo_la_raiz"),
    # m1: una unidad mapeada a la propia maquina.
    _w(
        "sin_prefijos_tras_realpath",
        "test_una_unidad_mapeada_a_la_propia_maquina_se_compara_como_la_unidad",
    ),
    _w("todo_es_la_raiz", "test_una_unidad_mapeada_a_la_propia_maquina_se_compara_como_la_unidad"),
    _w("todo_es_la_raiz", "test_la_unidad_sin_barra_es_relativa_al_directorio_de_esa_unidad"),
    _w("sin_disfraz_posix", "test_proc_cygdrive_es_la_unidad"),
    ("sin_disfraz_posix", "test_proc_self_cwd_es_el_directorio_de_trabajo"),
    # Pasada minima, c3: la rama `_no_canonizable` de la unidad sin barra.
    _w("sin_no_canonizable", "test_la_unidad_sin_barra_es_relativa_al_directorio_de_esa_unidad"),
    ("todo_es_la_raiz", "test_proc_self_cwd_es_el_directorio_de_trabajo"),
    ("sin_proveedor", "test_el_proveedor_filesystem_de_powershell"),
    ("todo_es_la_raiz", "test_el_proveedor_filesystem_de_powershell"),
]


@pytest.mark.parametrize(("rotura", "nombre"), ROTURAS)
def test_roto_a_proposito(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch, rotura: str, nombre: str
) -> None:
    _romper(rotura, g, repo, monkeypatch)
    test = globals()[nombre]
    argumentos: dict[str, Any] = {"g": g, "repo": repo, "monkeypatch": monkeypatch}
    argumentos |= {"sitio": "marzo", "ruta": "\\\\otra-maquina\\C$\\x\\y.txt"}
    nombres = test.__code__.co_varnames[: test.__code__.co_argcount]
    with pytest.raises(AssertionError) as fallo:
        test(**{n: argumentos[n] for n in nombres})
    primera = str(fallo.value).splitlines()[0] if str(fallo.value) else "AssertionError"
    print(f"ROTO | {rotura} | {nombre} | falla: {primera[:160]}")
