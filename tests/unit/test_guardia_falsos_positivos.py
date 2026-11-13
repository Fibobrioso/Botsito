"""F2 entra y F1 se aplaza: la guardia deja `cmp` y sigue negando lo que negaba.

Rama `trabajo/guardia-falsos-positivos` (2026-11-12 y 13, GUARDIA-FALSOS-POSITIVOS.md), con las
respuestas del consultor a la PARADA de la fase 0 y a la PARADA 2:

- F1, APLAZADO (respuesta a la PARADA 2, punto 4): la condicion que dejaba pasar los comentarios de
  MQL5 que escribe `generar_capa.py` (:359 y :364) se probo en tres versiones (D1d; con el tramo
  sin blancos a los dos lados; con los sufijos mirados) y la segunda pasada del revisor encontro
  casos que stable/F38z niega y esa condicion dejaba pasar (R1-R4, abajo, medidos). La guardia
  vuelve a la de stable/F38z para esos literales; los tests de F1 que aseguran que pasa quedan como
  `xfail` estricto, documentado.
- F2 (G.6; D2): `cmp` esta en `NO_EJECUTAN` y sus argumentos se miran como una lectura, como los de
  `diff`.
- Lo que tiene que seguir negado (D3, h1-h8 de la fase 0, B1-B2 de la primera pasada del revisor
  y R1-R4 de la segunda), cada caso con su sistema: los casos con `\\` y `//` son de Windows (en
  Linux `\\` es parte del nombre y `// x` es `/ x`: ya pasaban); lo que sigue negado en los dos va
  sin marca. Se quedan aunque F1 se aplace: son la bateria contra la que se medira una condicion
  futura.
- Lo que la guardia de `GUARDIA_DE_REFERENCIA` (`stable/F38z-capa-generada`, en
  `test_guardia_g1.py`) decidia en F1, F2 y esos casos, por su motivo.
- ROTO A PROPOSITO, de F2: sin `cmp` en `NO_EJECUTAN` se niega; con `cmp` sin leer sus argumentos,
  el protegido pasa. (Los de las piezas de F1 salieron con F1.)

Todo EN MEMORIA, con `decidir`, sobre un repo INVENTADO con ficheros FALSOS donde el material
protegido; las rutas protegidas a trozos. La fase 0 (la tabla de cinco variantes de D1) esta en
`anexos/GUARDIA-FALSOS-POSITIVOS/fase0-windows-SALIDA.txt`.
"""

from __future__ import annotations

import ast
import importlib.util
import os
import re
import shutil
import socket
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
GENERAR_CAPA = RAIZ / "src" / "botsito" / "mql5bridge" / "generar_capa.py"
TEST_G1 = RAIZ / "tests" / "unit" / "test_guardia_g1.py"
EN_WINDOWS = os.name == "nt"
SOLO_WINDOWS = pytest.mark.skipif(
    not EN_WINDOWS, reason="F1 y las rutas con \\ solo existen en Windows (D6)"
)

HOL = "hol" + "dout"
KC = "knowledge/cases"
SECRETO = f"{KC}/{HOL}/1/secreto.yaml"
B = "\\"
LIT_364 = "// CAPA_HASH = SHA-256 de este fichero sin su linea (docs/validation/CAPA-GENERADA.md)."
LIT_359 = "//   uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil "


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
def base(g: ModuleType, tmp_path: Path) -> Iterator[Path]:
    """Donde va el repo inventado. El temporal de pytest en Windows lleva `AppData\\`, que casa con
    el fragmento `data\\` de `SENSIBLES`: con el, h7 y h8 se negarian por el fragmento y no por la
    condicion que los niega con la raiz real (fase 0, §a). Si el temporal lleva un fragmento, el
    repo va a una carpeta nueva en la del usuario, que se borra al acabar."""
    if not any(s in str(tmp_path).lower() for s in g.SENSIBLES):
        yield tmp_path
        return
    limpia = Path(tempfile.mkdtemp(prefix="gfp-", dir=Path.home()))
    assert not any(s in str(limpia).lower() for s in g.SENSIBLES), "la carpeta limpia no lo es"
    try:
        yield limpia
    finally:
        _borrar(limpia)


def _borrar(carpeta: Path) -> None:
    """`shutil.rmtree` que quita el «solo lectura» de los objetos de git en Windows (sin eso,
    `ignore_errors` deja la carpeta entera sin decir nada: 130 quedaron en la primera medida)."""

    def quitar_solo_lectura(funcion: Any, ruta: str, _excepcion: BaseException) -> None:
        os.chmod(ruta, stat.S_IWRITE)
        funcion(ruta)

    shutil.rmtree(carpeta, onexc=quitar_solo_lectura)
    assert not carpeta.exists(), carpeta


@pytest.fixture
def repo(base: Path) -> Path:
    """El repo inventado de la fase 0: lo de `main`, y en la rama los ficheros NUEVOS que compara
    `cmp` (dos de `docs/` y el nombre con `=` del origen de G.6, ACTIVAR-SESION-06-MOTOR.md:217)."""
    return _crear_repo(base / "repo")


def _crear_repo(r: Path) -> Path:
    _escribir(
        r, f"{KC}/kit/s1/particiones.yaml", "asignacion:\n  caso-eurusd-2026-05-04: holdout-1\n"
    )
    _escribir(r, "knowledge/corpus/fuentes.yaml", "videos:\n  - video_id: v7\n    drive_id: null\n")
    for rel in (f"{KC}/{HOL}/README.md", f"{KC}/{HOL}/1/README.md", SECRETO, f"{KC}/dev/c.yaml"):
        _escribir(r, rel)
    for rel in ("docs/a.md", "docs/b.md", "PROJECT_STATE.md", "Makefile"):
        _escribir(r, rel)
    _escribir(r, ".gitignore", "/corp" + "us/\n/data/*\n")
    _git(r, "init", "-q", "-b", "main")
    _git(r, "add", "-A")
    _git(r, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "inicio")
    _git(r, "checkout", "-q", "-b", "trabajo/prueba")
    for rel in ("docs/n1.md", "docs/n2.md", "diaria.DIAGNOSTICO.cuenta=diaria.txt", "otra.txt"):
        _escribir(r, rel)
    return r


def _decide(g: ModuleType, repo: Path, comando: str) -> str | None:
    evento: dict[str, Any] = {
        "tool_name": "Bash",
        "tool_input": {"command": comando},
        "cwd": str(repo),
    }
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


def _guion(g: ModuleType, repo: Path, nombre: str, codigo: str) -> str | None:
    """Escribe un guion NUEVO en la rama (no esta en `main`) y decide su ejecucion."""
    _escribir(repo, nombre, codigo)
    return _decide(g, repo, f"uv run python {nombre}")


def _regla(g: ModuleType, motivo: str | None) -> str:
    if motivo is None:
        return "pasa"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    return ",".join(sorted(nombres)) or "niega (sin R_)"


def _lista(literal: str) -> str:
    return f"L = [{literal!r}]\nprint(L)\n"


def _abre(expresion: str) -> str:
    return f"print(open({expresion}).read())\n"


def _recorre(ruta: str) -> str:
    return f"from pathlib import Path\nprint(list(Path({ruta!r}).rglob('*')))\n"


def _unc(repo: Path, blanco: str, equipo: str, cola: str = "") -> str:
    """La raiz del repo como recurso de la propia maquina (`\\\\<blanco><equipo>\\C$\\...`)."""
    rw = str(repo)
    cola = cola.replace("/", B)
    return B * 2 + blanco + equipo + B + rw[0] + "$" + rw[2:] + (B + cola if cola else "")


def _copia_de_generar_capa(repo: Path) -> str:
    """La copia CAMBIADA del guion real (la de `main` pasa por ser identica a la de `main`)."""
    rel = "src/botsito/mql5bridge/generar_capa.py"
    _escribir(repo, rel, GENERAR_CAPA.read_text(encoding="utf-8") + "# cambiado en la rama\n")
    return f"uv run python {rel} --repo . --perfil p"


_F1_APLAZADO = pytest.mark.xfail(
    strict=True,
    reason="F1, aplazado: ninguna condicion medida aguanta (respuesta a la PARADA 2, punto 4;"
    " R1-R4 de la segunda pasada del revisor, GUARDIA-FALSOS-POSITIVOS.md)",
)


# -------------------------------------------------------------- F1 (solo Windows: D1d, punto 0)
def test_el_guion_real_lleva_los_dos_literales() -> None:
    """Los dos literales de F1 son los de `generar_capa.py`, tal cual (fase 0, §a)."""
    texto = GENERAR_CAPA.read_text(encoding="utf-8")
    assert LIT_364 in texto
    assert LIT_359 in texto


@_F1_APLAZADO
@SOLO_WINDOWS
def test_f1_la_copia_cambiada_de_generar_capa_pasa(g: ModuleType, repo: Path) -> None:
    motivo = _decide(g, repo, _copia_de_generar_capa(repo))
    assert motivo is None, motivo


@_F1_APLAZADO
@SOLO_WINDOWS
def test_f1_el_literal_no_llega_a_absoluta_ni_tarda(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """D6: los dos literales de F1 (:364 y el trozo constante de :359) no llegan a `_absoluta` (ni,
    por tanto, a `_canonica` ni a `realpath`), y la decision sobre el guion entero queda muy por
    debajo del tope de 30 s del hook. Los `//+---`, `//| ...` y `// ` de la cabecera SI llegan, como
    con la referencia: no son de F1 (sin blanco en el tramo), ya pasaban, y no tardan."""
    vistos: list[str] = []
    original = g._absoluta

    def absoluta(ruta: str, cwd: str) -> str:
        vistos.append(ruta)
        return str(original(ruta, cwd))

    monkeypatch.setattr(g, "_absoluta", absoluta)
    t = time.perf_counter()
    motivo = _decide(g, repo, _copia_de_generar_capa(repo))
    segundos = time.perf_counter() - t
    print(f"F1 | decidir sobre la copia de generar_capa.py: {segundos:.2f} s")
    assert motivo is None, motivo
    de_f1 = [v for v in vistos if v.startswith("//") and ("CAPA_HASH =" in v or "uv run" in v)]
    assert not de_f1, de_f1
    assert [v for v in vistos if v.startswith("//+")], "la medida no vio la cabecera"
    assert segundos < 5


@_F1_APLAZADO
@SOLO_WINDOWS
@pytest.mark.parametrize(
    "codigo",
    [
        _lista(LIT_364),
        # :359 tal cual: la f-cadena con un parametro que no se calcula; su trozo constante
        # es un literal de `analizar_codigo`
        f"def f(perfil):\n    return [f{LIT_359 + '{perfil}'!r}]\nprint(f('p'))\n",
        _lista("//\tx docs/a/b.md"),
        _lista(B * 2 + " x docs" + B + "a" + B + "b.md"),
    ],
    ids=["364", "359-fcadena", "tabulador", "barras-invertidas"],
)
def test_f1_un_comentario_de_un_guion_nuevo_pasa(g: ModuleType, repo: Path, codigo: str) -> None:
    motivo = _guion(g, repo, "t/f1.py", codigo)
    assert motivo is None, motivo


# -------------------------------------------------------------------------- F2 (G.6, los dos)
@pytest.mark.parametrize(
    "comando",
    [
        "cmp docs/n1.md docs/n2.md",
        "cmp -s docs/n1.md docs/n2.md",
        "cmp diaria.DIAGNOSTICO.cuenta=diaria.txt otra.txt",
    ],
)
def test_f2_cmp_de_dos_ficheros_que_no_son_guiones_pasa(
    g: ModuleType, repo: Path, comando: str
) -> None:
    motivo = _decide(g, repo, comando)
    assert motivo is None, motivo


def test_f2_cmp_con_un_fichero_protegido_se_niega_por_la_lectura(g: ModuleType, repo: Path) -> None:
    """D2 y D3: el fichero protegido, primero, segundo o con la ruta absoluta, se niega por la
    regla del sitio (`R_HOLDOUT`), como el de `diff`."""
    for comando in (
        f"cmp docs/a.md {SECRETO}",
        f"cmp {SECRETO} docs/n1.md",
        f"cmp docs/n1.md '{repo.as_posix()}/{SECRETO}'",
        f"diff docs/a.md {SECRETO}",
    ):
        motivo = _decide(g, repo, comando)
        assert "R_HOLDOUT" in _regla(g, motivo).split(","), (comando, motivo)


# ---------------------------------------------------- D3 y h1-h8: lo que sigue negado (fase 0)
def _h_windows(repo: Path) -> dict[str, str]:
    """h1-h8 de la fase 0 que solo se niegan en Windows (en Linux ya pasaban: `\\` es parte del
    nombre, y `// <ruta>` es `/ <ruta>`, fuera de la raiz)."""
    return {
        "h1-recorte": _abre(repr("// " + SECRETO) + "[3:]"),
        "h1c-recorte-blanco-interior": _abre(repr("// a b/" + SECRETO) + "[6:]"),
        "h2-lstrip": _abre(repr("// " + SECRETO) + ".lstrip('/ ')"),
        "h4-espacio-localhost": _abre(repr(_unc(repo, " ", "localhost", SECRETO))),
        "h5-tab-localhost": _abre(repr(_unc(repo, "\t", "localhost", SECRETO))),
        "h6-espacio-equipo": _abre(repr(_unc(repo, " ", socket.gethostname(), SECRETO))),
        "h7-raiz-recorre": _recorre(_unc(repo, " ", "localhost")),
        "h8-raiz-sin-recorrer": f"import os\nprint(os.stat({_unc(repo, ' ', 'localhost')!r}))\n",
    }


@SOLO_WINDOWS
@pytest.mark.parametrize(
    "caso",
    [
        "h1-recorte",
        "h1c-recorte-blanco-interior",
        "h2-lstrip",
        "h4-espacio-localhost",
        "h5-tab-localhost",
        "h6-espacio-equipo",
        "h7-raiz-recorre",
        "h8-raiz-sin-recorrer",
    ],
)
def test_h_los_casos_de_windows_siguen_negados(g: ModuleType, repo: Path, caso: str) -> None:
    motivo = _guion(g, repo, "t/h.py", _h_windows(repo)[caso])
    assert motivo is not None, caso


# Lo que encontro el revisor (B1 y B2): variantes de h4-h8 y de h1c que stable/F38z niega.
def _revisor(repo: Path) -> dict[str, str]:
    oculto = "docs/oculto-SALIDA.txt"  # en `ficheros_con_ocultos.txt` del repo inventado
    return {
        "b1-h7-blanco-detras": _recorre(_unc(repo, " ", "localhost ")),
        "b1-h8-blanco-detras": f"import os\nprint(os.stat({_unc(repo, ' ', 'localhost ')!r}))\n",
        "b1-h7-tab-detras": _recorre(_unc(repo, "\t", "localhost\t")),
        "b1-h4-blanco-detras": _abre(repr(_unc(repo, " ", "localhost ", SECRETO))),
        "b2-oculto-sin-fragmento": _abre(repr("// a b/" + oculto) + "[7:]"),
        "b2-oculto-invertidas": _abre(repr(B * 2 + " a b" + B + oculto.replace("/", B)) + "[7:]"),
        # una carpeta sin fragmento que CONTIENE el holdout, recortada y recorrida (la politica
        # no para recorrer una carpeta solo por un fichero oculto dentro: `'docs'` y `rglob`
        # ya pasan con stable/F38z, y por eso no es este caso)
        "b2-carpeta-protegida-recorrida": (
            "from pathlib import Path\nprint(list(Path('// a b/knowledge'[7:]).rglob('*')))\n"
        ),
    }


def _con_oculto(repo: Path) -> None:
    _escribir(repo, "docs/oculto-SALIDA.txt", "linea oculta\n")
    _escribir(repo, ".claude/hooks/ficheros_con_ocultos.txt", "docs/oculto-SALIDA.txt\n")


@SOLO_WINDOWS
@pytest.mark.parametrize(
    "caso",
    [
        "b1-h7-blanco-detras",
        "b1-h8-blanco-detras",
        "b1-h7-tab-detras",
        "b1-h4-blanco-detras",
        "b2-oculto-sin-fragmento",
        "b2-oculto-invertidas",
        "b2-carpeta-protegida-recorrida",
    ],
)
def test_revisor_las_variantes_siguen_negadas(g: ModuleType, repo: Path, caso: str) -> None:
    """B1 y B2 del revisor (PARADA 2, puntos 0 y 1): negados en la rama, como en stable/F38z."""
    _con_oculto(repo)
    motivo = _guion(g, repo, "t/rev.py", _revisor(repo)[caso])
    assert motivo is not None, caso


@SOLO_WINDOWS
@pytest.mark.parametrize(
    "caso",
    [
        "b1-h7-blanco-detras",
        "b1-h8-blanco-detras",
        "b1-h7-tab-detras",
        "b1-h4-blanco-detras",
        "b2-oculto-sin-fragmento",
        "b2-oculto-invertidas",
        "b2-carpeta-protegida-recorrida",
    ],
)
def test_revisor_la_referencia_niega_las_variantes(ref: ModuleType, repo: Path, caso: str) -> None:
    _con_oculto(repo)
    motivo = _guion(ref, repo, "t/rev.py", _revisor(repo)[caso])
    assert motivo is not None, caso


@SOLO_WINDOWS
def test_el_residuo_de_f1_es_la_clase_de_h1b(
    g: ModuleType, ref: ModuleType, repo: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """PARADA 2, punto 1: lo que queda de F1, un recorte a mitad de un nombre
    (`"// a b/x<fichero oculto>"[8:]`), es la clase de h1b (`'x' + ruta[1:]`), que la guardia de
    stable/F38z YA deja pasar: medido aqui con las dos guardias, sobre el mismo fichero oculto.
    Limite conocido (GUARDIAS-CLAUDE.md §1.7); no se asegura un hueco, se mide."""
    _con_oculto(repo)
    oculto = "docs/oculto-SALIDA.txt"
    h1b = _abre(repr("x" + oculto) + "[1:]")
    residuo = _abre(repr("// a b/x" + oculto) + "[8:]")
    decisiones = {
        (guardia, caso): _guion(m, repo, "t/r.py", codigo)
        for guardia, m in (("F38z", ref), ("rama", g))
        for caso, codigo in (("h1b", h1b), ("residuo", residuo))
    }
    with capsys.disabled():
        for (guardia, caso), motivo in decisiones.items():
            print(f"\nRESIDUO | {guardia} | {caso} | {'PASA' if motivo is None else 'NIEGA'}")
    assert decisiones[("F38z", "h1b")] is None  # la clase ya pasa con la referencia
    assert decisiones[("rama", "h1b")] is None


# La segunda pasada del revisor (R1-R4): la cabeza de un literal de F1 es una carpeta de verdad, o
# la cola es la raiz por el recurso `C$`, y el directorio de trabajo no es la raiz.
def _r_casos(base: Path, repo: Path) -> dict[str, tuple[str, str]]:
    """(directorio de trabajo, comando) de R1-R4. `repo` no lleva blancos en su ruta; `base/r b`
    es otro repo inventado cuya carpeta si lleva uno (R2)."""

    def py_c(codigo: str) -> str:
        return f'uv run python -c "{codigo}"'

    rglob = "from pathlib import Path; print(list(Path({}).rglob('*')))"
    raiz_c = B * 2 + " local host" + B + str(repo)[0] + "$" + str(repo)[2:]
    corte = repr(f"// a b/x//localhost/{str(repo)[0]}$" + repo.as_posix()[2:]) + "[8:]"
    zona = "estrategia del trader/sesiones/x.txt"
    walk = "import os; print([r for r, _, _ in os.walk('// r b/knowledge'[3:])])"
    return {
        "r1-cd-corpus": (str(repo / ("corp" + "us")), py_c(f"print(open('// {zona}'[3:]).read())")),
        "r2-cd-padre": (str(base), py_c(walk)),
        "r3-blanco-dentro-del-nombre": (
            str(repo),
            py_c(rglob.format(repr(raiz_c) + ".replace(' ', '', 2)")),
        ),
        "r4-recurso-tras-el-corte": (str(repo), py_c(rglob.format(corte))),
    }


@pytest.fixture
def repos_r(base: Path, repo: Path) -> dict[str, tuple[str, str]]:
    _crear_repo(base / "r b")
    _escribir(repo, f"{'corp' + 'us'}/estrategia del trader/sesiones/x.txt", "hoja falsa\n")
    return _r_casos(base, repo)


def _decide_en(g: ModuleType, repo: Path, cwd: str, comando: str) -> str | None:
    evento: dict[str, Any] = {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": cwd}
    motivo: str | None = g.decidir(evento, g.Politica(repo))
    return motivo


R_CASOS = [
    "r1-cd-corpus",
    "r2-cd-padre",
    "r3-blanco-dentro-del-nombre",
    "r4-recurso-tras-el-corte",
]


@SOLO_WINDOWS
@pytest.mark.parametrize("caso", R_CASOS)
def test_r_la_referencia_niega(
    ref: ModuleType, repo: Path, repos_r: dict[str, tuple[str, str]], caso: str
) -> None:
    cwd, comando = repos_r[caso]
    motivo = _decide_en(ref, repo, cwd, comando)
    primera = (motivo or "PASA").splitlines()[0].replace(str(repo.parent), "<tmp>")
    print(f"\nR | F38z | {caso} | {primera.replace(repo.parent.as_posix(), '<tmp>')[:160]}")
    assert motivo is not None, caso


@SOLO_WINDOWS
@pytest.mark.parametrize("caso", R_CASOS)
def test_r_siguen_negados(
    g: ModuleType, repo: Path, repos_r: dict[str, tuple[str, str]], caso: str
) -> None:
    cwd, comando = repos_r[caso]
    assert _decide_en(g, repo, cwd, comando) is not None, caso


def test_h3_el_punto_punto_sigue_negado(g: ModuleType, repo: Path) -> None:
    """h3, en los dos sistemas: `// x/../<raiz>/<protegido>` (en Linux `realpath` lo resuelve a la
    raiz; en Windows es un recurso de otra maquina que no se puede canonizar)."""
    raiz = repo.as_posix().lstrip("/")
    motivo = _guion(g, repo, "t/h3.py", _abre(repr(f"// x/../{raiz}/{SECRETO}")))
    assert motivo is not None


@SOLO_WINDOWS
@pytest.mark.parametrize(
    "literal",
    ["//host/share/x/y.txt", B * 2 + "host" + B + "share" + B + "y.txt"],
    ids=["barras", "invertidas"],
)
def test_d3_un_recurso_de_red_sin_blanco_sigue_negado(
    g: ModuleType, repo: Path, literal: str
) -> None:
    motivo = _guion(g, repo, "t/d3.py", _abre(repr(literal)))
    assert motivo is not None and "no se puede canonizar" in motivo, motivo


def test_d3_un_guion_nuevo_que_nombra_o_recorre_lo_protegido_sigue_negado(
    g: ModuleType, repo: Path
) -> None:
    for codigo in (_recorre(f"{KC}/{HOL}"), _abre(repr(SECRETO))):
        motivo = _guion(g, repo, "t/d3.py", codigo)
        assert motivo is not None and "R_HOLDOUT" in _regla(g, motivo), motivo


@SOLO_WINDOWS
@pytest.mark.parametrize(
    "codigo",
    [
        _lista("//| ver docs/validation/X.md |"),
        f"p = 'x'\nL = [f{LIT_359 + '{p}'!r}]\nprint(L)\n",
    ],
    ids=["barra-vertical", "fcadena-calculable"],
)
def test_lo_que_d1d_no_cubre_sigue_negado(g: ModuleType, repo: Path, codigo: str) -> None:
    """El residuo declarado (respuesta, punto 2): `//| docs/x |` y la f-cadena `// ...{x}/...`
    con una variable calculable (va por las composiciones). Ningun guion real lo pide hoy."""
    assert _guion(g, repo, "t/residuo.py", codigo) is not None


# ------------------------------------ la referencia (stable/F38z) negaba F1 y F2, por su motivo
def _referencia() -> str:
    m = re.search(r'^GUARDIA_DE_REFERENCIA = "([^"]+)"', TEST_G1.read_text(encoding="utf-8"), re.M)
    assert m is not None
    return m.group(1)


@pytest.fixture
def ref(tmp_path: Path) -> ModuleType:
    """La guardia de `GUARDIA_DE_REFERENCIA` (`test_guardia_g1.py`), cargada aparte; sin el tag,
    el test salta con aviso (la CI lo trae con `git fetch --tags --force`)."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    r = subprocess.run(
        ["git", "show", f"{_referencia()}:.claude/hooks/guardia.py"],
        cwd=RAIZ,
        capture_output=True,
        encoding="utf-8",
        check=False,
        env=env,
    )
    if r.returncode != 0:
        pytest.skip(f"sin el tag {_referencia()} en este clon")
    ruta = tmp_path / "referencia" / "guardia.py"
    ruta.parent.mkdir(parents=True)
    ruta.write_text(r.stdout, encoding="utf-8")
    spec = importlib.util.spec_from_file_location("guardia_referencia_gfp", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["guardia_referencia_gfp"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_la_referencia_es_stable_f38z() -> None:
    """D5: la referencia sube al ultimo stable, el de la guardia que esta rama cambia."""
    assert _referencia() == "stable/F38z-capa-generada"


@SOLO_WINDOWS
def test_la_referencia_niega_f1_por_no_canonizar(ref: ModuleType, repo: Path) -> None:
    motivo = _decide(ref, repo, _copia_de_generar_capa(repo))
    assert motivo is not None and "no se puede canonizar" in motivo, motivo
    assert "CAPA_HASH" in motivo  # el literal de :364, el primero que encuentra `ast.walk`


def test_la_referencia_niega_f2_por_ejecutar(ref: ModuleType, repo: Path) -> None:
    motivo = _decide(ref, repo, "cmp docs/n1.md docs/n2.md")
    assert motivo is not None and "ejecutar `cmp`" in motivo and "no sabe con que" in motivo


# --------------------------------------------------------------------------- ROTO A PROPOSITO
def test_b3_cmp_como_diff_en_las_composiciones(g: ModuleType) -> None:
    """B3 del revisor: con `cmp` en `NO_EJECUTAN`, una cadena que empieza por `cmp ` es una ORDEN y
    no una composicion de C, igual que `diff`; un programa fuera de la lista (`xxd`) sigue
    contando como composicion."""
    for programa, composicion in (("cmp", False), ("diff", False), ("xxd", True)):
        for codigo in (f'f"{programa} {{a}}/b/c"', f'"{programa} " + a + "/b/c"'):
            nodo = ast.parse(codigo, mode="eval").body
            assert g._es_composicion(nodo) is composicion, (programa, codigo)


def test_roto_sin_cmp_en_no_ejecutan(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delitem(g.NO_EJECUTAN, "cmp")
    motivo = _decide(g, repo, "cmp docs/n1.md docs/n2.md")
    assert motivo is not None and "ejecutar `cmp`" in motivo


def test_roto_cmp_sin_leer_sus_argumentos(
    g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Si `cmp` no mirara sus argumentos como una lectura, el fichero protegido pasaria."""
    monkeypatch.setattr(g, "SIN_LECTURA_DE_RUTAS", g.SIN_LECTURA_DE_RUTAS | {"cmp"})
    assert _decide(g, repo, f"cmp docs/a.md {SECRETO}") is None
