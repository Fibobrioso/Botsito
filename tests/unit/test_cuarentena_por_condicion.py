"""La cuarentena del texto por CONDICION (rama `trabajo/cuarentena-por-condicion`, decision del
consultor del 2026-10-04): se tapa todo mes que no se pueda demostrar libre.

Un mes es libre solo si (a) no tiene ningun dia en `casos_ocultos` ni en `casos_reservados`, en
ningun ano; (b) no esta en `knowledge/cases/meses_reservados.yaml`; y (c) se pudieron comprobar las
dos. `cases.holdout.meses_libres` lo calcula; `corpus.cuarentena` lo recibe (`libres`) y, sin el,
tapa los doce. Los repositorios de prueba son temporales: el real solo se mira en el recuento final
y en el cruce con la lista blanca de la guardia.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest

from botsito.cases import holdout
from botsito.cases.holdout import (
    FICHERO_MESES_RESERVADOS,
    cargar_meses_reservados,
    casos_ocultos,
    casos_reservados,
    meses_libres,
    problemas_de_meses_reservados,
)
from botsito.corpus import cuarentena as cu

RAIZ = Path(__file__).resolve().parents[2]
# El nombre de cada mes en espanol: si la regla tapa un mes, tapa por lo menos su nombre.
NOMBRE = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio", 7: "julio",
    8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}  # fmt: skip
MESES_RESERVADOS = """meses:
  "2026-02":
    motivo: el mes limpio pendiente
    fuente: [ADR-0046]
    declarado_el: "2026-10-04"
  "2026-03":
    motivo: recibido y sin abrir
    fuente: [ADR-0046]
    declarado_el: "2026-10-04"
"""


def _repo(tmp_path: Path, meses: str | None = MESES_RESERVADOS) -> Path:
    """Un repositorio minimo: un ADR que citar, el fichero de (b) y ningun reparto."""
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0046-marzo.md").write_text("# 0046\n", encoding="utf-8")
    (tmp_path / "knowledge" / "cases").mkdir(parents=True)
    if meses is not None:
        (tmp_path / FICHERO_MESES_RESERVADOS).write_text(meses, encoding="utf-8")
    return tmp_path


def _reparto(repo: Path, asignacion: dict[str, str]) -> None:
    sesion = repo / "knowledge" / "cases" / "kit" / "2026-09-15-sesion-01"
    sesion.mkdir(parents=True, exist_ok=True)
    lineas = "".join(f"  {caso}: {p}\n" for caso, p in asignacion.items())
    (sesion / "particiones.yaml").write_text(
        f"sesion: 2026-09-15-sesion-01\nseed: 1\nasignacion:\n{lineas}", encoding="utf-8"
    )


def _tapa(mes: int, libres: frozenset[int] | None) -> bool:
    return cu.MOTIVO_MES in cu.motivos_cuarentena(f"eso fue en {NOMBRE[mes]}", libres)


# ---------------------------------------------------------------- 1: un caso inventado, sin listas


def test_1_un_caso_oculto_inventado_tapa_su_mes_sin_tocar_ninguna_lista(tmp_path: Path) -> None:
    """Noviembre hoy no se tapa. Un caso reservado inventado en noviembre, en un repo temporal, lo
    tapa: sin anadirlo a ninguna lista (GRAFIAS_MES no cambia)."""
    repo = _repo(tmp_path)
    grafias_antes = dict(cu.GRAFIAS_MES)
    libres = meses_libres(repo)
    assert libres is not None and 11 in libres and not _tapa(11, libres)
    _reparto(repo, {"caso-eurusd-2026-11-05": "holdout-1"})
    libres = meses_libres(repo)
    assert libres is not None and 11 not in libres
    assert _tapa(11, libres)
    assert dict(cu.GRAFIAS_MES) == grafias_antes


def test_1b_un_caso_de_otro_ano_tapa_el_mismo_mes(tmp_path: Path) -> None:
    """(a) es en NINGUN ano: el texto dice «noviembre» sin ano."""
    repo = _repo(tmp_path)
    _reparto(repo, {"caso-eurusd-2031-11-05": "fidelidad-2"})
    libres = meses_libres(repo)
    assert libres is not None and 11 not in libres


def test_1c_un_caso_dev_no_tapa_su_mes(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _reparto(repo, {"caso-eurusd-2026-11-05": "dev"})
    libres = meses_libres(repo)
    assert libres is not None and 11 in libres


# ------------------------------------------------------------- 2: sin datos se tapan los doce


@pytest.mark.parametrize("mes", range(1, 13))
def test_2_sin_datos_se_tapan_los_doce(mes: int) -> None:
    assert _tapa(mes, None)
    filtro = cu.Filtro("v1")  # construido sin los datos de (a) y (b)

    class S:
        def __init__(self, n: int, texto: str) -> None:
            self.n, self.t0_ms, self.t1_ms, self.texto = n, n * 1000, n * 1000 + 900, texto

    segmentos = [S(0, "hola"), S(1, "x"), S(2, f"en {NOMBRE[mes]}"), S(3, "y"), S(4, "adios")]
    assert [s.n for s in filtro.aplicar(segmentos)] == [0, 4]


@pytest.mark.parametrize(
    "contenido",
    [
        None,  # el fichero falta
        "meses: [\n",  # no se puede leer
        'meses:\n  "2026-2":\n    motivo: x\n    fuente: [ADR-0046]\n'
        '    declarado_el: "2026-10-04"\n',
        'meses:\n  "2026-02":\n    motivo: x\n    fuente: []\n    declarado_el: "2026-10-04"\n',
        'meses:\n  "2026-02":\n    motivo: x\n    fuente: [ADR-0999]\n'
        '    declarado_el: "2026-10-04"\n',
        'meses:\n  "2026-02":\n    motivo: x\n    fuente: [docs/no-esta.md]\n'
        '    declarado_el: "x"\n',
        "otra: {}\n",
    ],
)
def test_2b_si_la_fuente_de_b_falla_no_hay_ningun_mes_libre(
    tmp_path: Path, contenido: str | None
) -> None:
    """Falta, no se lee o no valida: `meses_libres` da None y la regla tapa los doce."""
    repo = _repo(tmp_path, contenido)
    assert meses_libres(repo) is None
    assert all(_tapa(m, meses_libres(repo)) for m in range(1, 13))


def test_2c_un_reparto_ilegible_no_deja_ningun_mes_libre(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    sesion = repo / "knowledge" / "cases" / "kit" / "s"
    sesion.mkdir(parents=True)
    (sesion / "particiones.yaml").write_text("asignacion: [\n", encoding="utf-8")
    assert meses_libres(repo) is None


def test_2d_un_caso_sin_fecha_no_deja_ningun_mes_libre(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _reparto(repo, {"caso-raro": "holdout-1"})
    assert meses_libres(repo) is None


# ------------------------------------------------------------ 3: un mes reservado entero sin casos


def test_3_un_mes_reservado_entero_sin_casos_se_tapa(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    assert casos_ocultos(repo) == {} and casos_reservados(repo) == {}
    libres = meses_libres(repo)
    assert libres is not None
    assert 2 not in libres and 3 not in libres
    assert _tapa(2, libres) and _tapa(3, libres)


# --------------------------------------------------- 4: la guardia puede dejar pasar algo


def test_4_un_mes_libre_de_verdad_no_se_tapa(tmp_path: Path) -> None:
    """Sin casos ocultos ni reservados y fuera de meses_reservados.yaml: se ve. Demuestra que la
    regla no es «tapar todo»."""
    repo = _repo(tmp_path)
    libres = meses_libres(repo)
    assert libres == frozenset(range(1, 13)) - {2, 3}
    assert not _tapa(11, libres)
    assert cu.motivos_cuarentena("eso fue en noviembre", libres) == []


# -------------------------------------------- 5: el repo real, ningun mes con dias sin cubrir


def test_5_ningun_mes_con_dias_ocultos_o_reservados_queda_sin_cubrir() -> None:
    """Contra el repositorio real. Solo recuento: nunca se dice que mes."""
    libres = meses_libres(RAIZ)
    assert libres is not None, "el repo real no demuestra ningun mes libre: revisar la fuente"
    casos = set(casos_ocultos(RAIZ)) | set(casos_reservados(RAIZ))
    vigilados = {int(c[-5:-3]) for c in casos} | {
        int(m[5:7]) for m in cargar_meses_reservados(RAIZ)
    }
    sin_cubrir = [m for m in vigilados if m in libres or not _tapa(m, libres)]
    assert len(sin_cubrir) == 0, f"{len(sin_cubrir)} sin cubrir"


# ---------------------------------------------------------- 6: las grafias de siempre siguen


@pytest.mark.parametrize(
    "texto",
    [
        "eso lo vi en septiembre",
        "lo de setiembre ya lo hablamos",
        "en Setiembre, no",
        "el sep lo tengo apuntado",
        "eso fue en marzo",
        "lo de marso",
        "cuando lo probaste en mayo",
        "lo de maio",
        "en febrero no operé",
        "lo de febreo",
        "el feb",
        "in September",
        "back in March",
        "the february one",
        "in june",
        "el jun",
    ],
)
def test_6_las_grafias_del_asr_siguen_tapando_los_meses_tapados(texto: str) -> None:
    libres = meses_libres(RAIZ)
    assert cu.MOTIVO_MES in cu.motivos_cuarentena(texto, libres), texto
    assert cu.MOTIVO_MES in cu.motivos_cuarentena(texto, None), texto


@pytest.mark.parametrize(
    "texto",
    [
        "es la mayor de todas",
        "la mayoría de las veces",
        "siempre pongo el stop ahí",
        "dentro de mi marco de operativa",
        "yo lo marco cuando cierra",
        "marco la liquidez de M15",
        "junto a la caja",
        "lo hago así",
        "lo pongo a 35 puntos",
    ],
)
def test_6b_marco_y_los_limites_de_palabra_no_tapan_ni_con_los_doce(texto: str) -> None:
    assert cu.motivos_cuarentena(texto, None) == [], texto


def test_set_suelto_no_es_un_mes_y_con_backtest_si() -> None:
    """Decision 5 del consultor: el primer intento de la medida contaba «set» suelto como mes."""
    for libres in (None, meses_libres(RAIZ)):
        assert cu.motivos_cuarentena("vamos a hacer un set de pruebas", libres) == []
        assert cu.MOTIVO_BACKTEST in cu.motivos_cuarentena("el backtest de set", libres)


def test_ningun_mes_queda_sin_grafias() -> None:
    assert set(cu.GRAFIAS_MES) == set(range(1, 13)) == set(cu.ABREVIATURAS_MES)


# --------------------------------------------- la lista blanca de la guardia, contra la fuente


def _guardia() -> ModuleType:
    nombre = "guardia_para_cruce"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / ".claude" / "hooks" / "guardia.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def test_la_lista_blanca_de_la_guardia_no_se_separa_de_la_fuente() -> None:
    """Decision 3 del consultor: MESES_DE_DESARROLLO (los libros legibles, `guardia.py`) es una
    lista blanca escrita a mano. Falla si algun mes suyo tiene dias en `casos_ocultos` o en
    `casos_reservados`, o esta en `meses_reservados.yaml`."""
    casos = set(casos_ocultos(RAIZ)) | set(casos_reservados(RAIZ))
    reservados_enteros = set(cargar_meses_reservados(RAIZ))
    mal = [
        m
        for m in _guardia().MESES_DE_DESARROLLO
        if m in reservados_enteros
        or any(c.endswith(tuple(f"-{m}-{d:02d}" for d in range(1, 32))) for c in casos)
    ]
    assert mal == [], f"{len(mal)} meses de la lista blanca chocan con la fuente"


def test_el_cruce_de_la_lista_blanca_no_es_decorativo(monkeypatch: pytest.MonkeyPatch) -> None:
    g = _guardia()
    monkeypatch.setattr(g, "MESES_DE_DESARROLLO", ("2026-03",))
    with pytest.raises(AssertionError, match="chocan con la fuente"):
        test_la_lista_blanca_de_la_guardia_no_se_separa_de_la_fuente()


# ------------------------------------------------------------- la fuente de (b): forma e historial


def test_la_fuente_real_valida() -> None:
    assert problemas_de_meses_reservados(RAIZ) == []
    assert {"2026-02", "2026-03"} <= set(cargar_meses_reservados(RAIZ))


def test_sin_la_fuente_validate_lo_dice(tmp_path: Path) -> None:
    repo = _repo(tmp_path, None)
    assert any("no existe" in p for p in problemas_de_meses_reservados(repo))


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def test_la_fuente_es_solo_anadir(tmp_path: Path) -> None:
    """Un mes que entra no sale: sacarlo o cambiarlo, aunque sea sin commitear, es un error."""
    repo = _repo(tmp_path)
    _git(repo, "init", "-q")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "uno")
    assert problemas_de_meses_reservados(repo) == []
    ruta = repo / FICHERO_MESES_RESERVADOS
    original = ruta.read_text(encoding="utf-8")
    ruta.write_text(original.split('  "2026-03"')[0], encoding="utf-8")
    assert any("saca el mes reservado 2026-03" in p for p in problemas_de_meses_reservados(repo))
    ruta.write_text(original.replace("recibido y sin abrir", "otro"), encoding="utf-8")
    assert any(
        "modifica el mes reservado 2026-03" in p for p in problemas_de_meses_reservados(repo)
    )
    ruta.write_text(
        original
        + '  "2026-12":\n    motivo: x\n    fuente: [ADR-0046]\n    declarado_el: "2026-10-04"\n',
        encoding="utf-8",
    )
    assert problemas_de_meses_reservados(repo) == []


def test_la_condicion_vive_en_cases_y_no_en_corpus() -> None:
    """corpus no puede leer cases (capas de import-linter): `cuarentena.py` no importa `cases`; los
    meses libres le llegan por argumento, y `cases.holdout` es quien los calcula."""
    import ast

    fuente = (RAIZ / "src" / "botsito" / "corpus" / "cuarentena.py").read_text(encoding="utf-8")
    importados: set[str] = set()
    for nodo in ast.walk(ast.parse(fuente)):
        if isinstance(nodo, ast.ImportFrom):
            importados.add(nodo.module or "")
        elif isinstance(nodo, ast.Import):
            importados |= {a.name for a in nodo.names}
    assert not any(m.startswith("botsito.cases") for m in importados)
    assert callable(holdout.meses_libres)
