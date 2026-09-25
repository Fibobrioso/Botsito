"""La medida del huso por velas (`scripts/huso_por_velas.py`, ADR-0039 §5) sobre datos SINTETICOS.

Escritos y en verde ANTES de ejecutar el control sobre un libro real: la herramienta se fija con
esto, y el control solo puede confirmarla o pararla, nunca ajustarla.
"""

from __future__ import annotations

import ast
import importlib.util
import shutil
import subprocess
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

from tests.contract.test_ingesta import _declarar, _xlsx

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "huso_por_velas.py"
CRITERIO_REAL = RAIZ / "knowledge" / "corpus" / "criterio_huso.yaml"
CENTINELA = "CENTINELA-RESERVADA-no-debe-salir"


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "huso_por_velas"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _doc() -> dict[str, Any]:
    doc = yaml.safe_load(CRITERIO_REAL.read_text(encoding="utf-8"))
    assert isinstance(doc, dict)
    return doc


# --- el criterio: de la configuracion, estricto, y las cifras de §5 ---------------------------


def test_el_criterio_real_son_las_cifras_de_adr_0039(m: ModuleType) -> None:
    c = m.criterio_desde_doc(_doc(), "criterio_huso.yaml")
    assert c.margen_puntos == 2  # A-16
    assert c.husos == ("UTC", "Europe/Madrid")
    assert c.umbral_decide == Decimal("0.90")
    assert c.umbral_otro == Decimal("0.50")


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"sobra": 1}, "exactamente"),
        ({"margen_puntos": True}, "margen_puntos"),
        ({"margen_puntos": -1}, "margen_puntos"),
        ({"husos": ["UTC"]}, "dos husos"),
        ({"husos": ["UTC", "UTC"]}, "dos husos"),
        ({"husos": "UTC"}, "dos husos"),
        ({"husos": ["UTC", "Marte/Olimpo"]}, "desconocido"),
        ({"umbral_decide": 0.9}, "texto decimal"),
        ({"umbral_decide": "1.5"}, "entre 0 y 1"),
        ({"umbral_otro": "0.95"}, "por debajo"),
    ],
)
def test_un_criterio_mal_formado_no_carga(
    m: ModuleType, cambio: dict[str, Any], mensaje: str
) -> None:
    doc = {**_doc(), **cambio}
    with pytest.raises(m.HusoError, match=mensaje):
        m.criterio_desde_doc(doc, "x")


def test_falta_una_clave_y_no_hay_cifra_por_defecto(m: ModuleType) -> None:
    doc = _doc()
    del doc["umbral_otro"]
    with pytest.raises(m.HusoError, match="exactamente"):
        m.criterio_desde_doc(doc, "x")


def test_el_script_no_lleva_ninguna_cifra_ni_huso_de_la_regla(m: ModuleType) -> None:
    """Las cifras se leen de la configuracion: ni el margen, ni los umbrales, ni los husos estan
    escritos en el script fuera de sus docstrings."""
    arbol = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    docstrings = {
        id(n.body[0].value)
        for n in ast.walk(arbol)
        if isinstance(n, ast.Module | ast.FunctionDef | ast.ClassDef)
        and n.body
        and isinstance(n.body[0], ast.Expr)
        and isinstance(n.body[0].value, ast.Constant)
    }
    constantes = [
        n.value for n in ast.walk(arbol) if isinstance(n, ast.Constant) and id(n) not in docstrings
    ]
    numeros = {c for c in constantes if isinstance(c, int | float) and not isinstance(c, bool)}
    assert m.criterio_desde_doc(_doc(), "x").margen_puntos not in numeros
    assert not numeros & {0.9, 0.5}
    textos = [c for c in constantes if isinstance(c, str)]
    for prohibido in ("0.90", "0.50", "0.9", "0.5", "UTC", "Europe/Madrid"):
        assert prohibido not in textos, f"el script lleva {prohibido!r} escrito"


# --- medir: el margen, el minuto, la vela ausente --------------------------------------------

T = datetime(2030, 1, 7, 9, 15, 42, tzinfo=UTC)
ESCALA = 100000


def _fila(m: ModuleType, entrada: str, a: datetime = T, b: datetime = T) -> Any:
    return m.Fila({"UTC": a, "Europe/Madrid": b}, Decimal(entrada))


def _criterio(m: ModuleType, **cambio: Any) -> Any:
    return m.criterio_desde_doc({**_doc(), **cambio}, "x")


def test_dentro_con_el_margen_de_la_configuracion_y_el_minuto_hacia_abajo(m: ModuleType) -> None:
    vela = {T.replace(second=0): m.Rango(110000, 110010, ESCALA)}
    filas = [
        _fila(m, "1.09998"),  # minima - 2: dentro
        _fila(m, "1.09997"),  # minima - 3: fuera
        _fila(m, "1.10012"),  # maxima + 2: dentro
        _fila(m, "1.10013"),  # maxima + 3: fuera
    ]
    cuenta = m.medir(filas, vela.get, _criterio(m))
    assert cuenta["UTC"] == (2, 4, 0)
    # Con margen 0 en la configuracion, los dos bordes quedan fuera: el margen no vive en src.
    assert m.medir(filas, vela.get, _criterio(m, margen_puntos=0))["UTC"] == (0, 4, 0)


def test_sin_vela_cuenta_en_el_total_y_no_dentro(m: ModuleType) -> None:
    cuenta = m.medir([_fila(m, "1.1")], {}.get, _criterio(m))
    assert cuenta["UTC"] == (0, 1, 1)


# --- decidir: §5 literal ---------------------------------------------------------------------


@pytest.mark.parametrize(
    ("utc", "madrid", "veredicto"),
    [
        ((95, 100), (10, 100), "UTC"),
        ((10, 100), (95, 100), "Europe/Madrid"),
        ((90, 100), (50, 100), "UTC"),  # los dos umbrales son inclusivos
        ((89, 100), (0, 100), "NO CONCLUYENTE"),
        ((95, 100), (51, 100), "NO CONCLUYENTE"),  # los dos altos: no distingue husos
        ((100, 100), (100, 100), "NO CONCLUYENTE"),
        ((0, 0), (0, 0), "NO CONCLUYENTE"),
    ],
)
def test_decide_solo_con_los_dos_umbrales(
    m: ModuleType, utc: tuple[int, int], madrid: tuple[int, int], veredicto: str
) -> None:
    cuenta = {"UTC": (*utc, 0), "Europe/Madrid": (*madrid, 0)}
    assert m.decidir(cuenta, _criterio(m)) == veredicto


# --- comparables: solo el mismo dia con los dos husos ----------------------------------------


def _leida(dia: str, texto: str, entrada: str, instante: datetime) -> dict[str, str | None]:
    return {
        "_dia": dia,
        "_instante_utc": instante.isoformat(),
        "dateStart": texto,
        "entryPrice": entrada,
    }


def test_la_fila_de_frontera_se_descarta_y_solo_sale_un_booleano(m: ModuleType) -> None:
    husos = ("UTC", "Europe/Madrid")
    lecturas = {
        "UTC": [
            _leida("2026-03-02", "2026/03/02 08:00:00", "1.1", T),
            _leida("2026-03-03", "2026/03/02 23:30:00", "1.2", T),  # dia distinto
            _leida("2026-03-02", "2026/03/02 09:00:00", "abc", T),  # entrada ilegible
        ],
        "Europe/Madrid": [
            _leida("2026-03-02", "2026/03/02 08:00:00", "1.1", T - timedelta(hours=1)),
            _leida("2026-03-02", "2026/03/02 23:30:00", "1.2", T),
            _leida("2026-03-02", "2026/03/02 09:00:00", "abc", T),
            _leida("2026-03-02", "2026/03/02 00:30:00", "1.3", T),  # solo con un huso
        ],
    }
    comp = m.comparables(lecturas, husos)
    assert len(comp.filas) == 1
    assert comp.frontera is True
    assert comp.sin_entrada == 1
    (fila,) = comp.filas
    assert fila.instantes["UTC"] - fila.instantes["Europe/Madrid"] == timedelta(hours=1)


# --- el libro entero: repo sintetico, lector real, velas sinteticas ---------------------------

FID = "knowledge/cases/fidelidad"
ART = "eurusd-2026-03"
CAB = ["dateStart", "side", "entryPrice", "initialSL"]
DEV = ["2026-03-02", "2026-03-05", "2026-03-09", "2026-03-10", "2026-03-12"]
RESERVADOS = ["2026-03-03", "2026-03-04", "2026-03-06", "2026-03-11"]


def _libro(ruta: Path) -> list[tuple[datetime, str]]:
    """Dos filas por dia `dev` a las 08:00:30 y 11:40:10 del texto, y una CENTINELA por dia
    reservado. Devuelve `(instante del texto leido como UTC, entrada)` de las filas `dev`."""
    filas = [CAB]
    dev: list[tuple[datetime, str]] = []
    for n, dia in enumerate(DEV):
        for hora, extra in (("08:00:30", 0), ("11:40:10", 5)):
            entrada = f"1.{10000 + 100 * n + extra}"
            filas.append([f"{dia.replace('-', '/')} {hora}", "buy", entrada, "1.0"])
            dev.append((datetime.fromisoformat(f"{dia}T{hora}+00:00"), entrada))
    for dia in RESERVADOS:
        filas.append([f"{dia.replace('-', '/')} 09:00:00", CENTINELA, CENTINELA, CENTINELA])
    _xlsx(ruta, filas, con_agregado=False)
    return dev


def _repo(tmp: Path) -> tuple[Path, Path, list[tuple[datetime, str]]]:
    repo = tmp / "repo"
    (repo / FID / ART).mkdir(parents=True)
    (repo / "knowledge/spec").mkdir(parents=True)
    (repo / "knowledge/corpus").mkdir(parents=True)
    shutil.copy(CRITERIO_REAL, repo / "knowledge/corpus/criterio_huso.yaml")
    shutil.copy(RAIZ / "knowledge/spec/parametros.yaml", repo / "knowledge/spec/parametros.yaml")
    (repo / "knowledge/corpus/libros.yaml").write_text("libros: {}\n", encoding="utf-8")
    asignacion = {f"caso-eurusd-{d}": "fidelidad-dev" for d in DEV}
    asignacion |= {f"caso-eurusd-{d}": "fidelidad-2" for d in RESERVADOS}
    (repo / FID / ART / "particiones.yaml").write_text(
        yaml.safe_dump({"asignacion": asignacion}), encoding="utf-8"
    )
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "reparto")):
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True,
            capture_output=True,
        )
    libro = tmp / "marzo.xlsx"
    return repo, libro, _libro(libro)


def _velas(m: ModuleType, dev: list[tuple[datetime, str]], desfase: timedelta) -> Any:
    """Velas que contienen la entrada en el minuto del texto + `desfase`, y lejos en el resto."""
    velas = {}
    for instante, entrada in dev:
        puntos = int(Decimal(entrada) * ESCALA)
        velas[(instante + desfase).replace(second=0)] = m.Rango(puntos - 1, puntos + 1, ESCALA)

    def vela_de(minuto: datetime) -> Any:
        return velas.get(minuto, m.Rango(1, 1, ESCALA))

    return vela_de


@pytest.mark.parametrize(
    ("desfase", "veredicto"),
    [
        (timedelta(0), "UTC"),  # las velas casan con el texto leido como UTC
        (timedelta(hours=-1), "Europe/Madrid"),  # marzo antes del cambio: Madrid es UTC+1
    ],
)
def test_el_libro_sintetico_da_el_huso_de_sus_velas(
    m: ModuleType, tmp_path: Path, desfase: timedelta, veredicto: str
) -> None:
    repo, libro, dev = _repo(tmp_path)
    inf = m.medir_libro(repo, libro, "2026-03", "AAAA/MM/DD HH:MM:SS", _velas(m, dev, desfase))
    assert inf.veredicto == veredicto
    assert inf.dias == len(DEV)
    assert len(inf.comparables.filas) == 2 * len(DEV)
    assert inf.comparables.frontera is False
    assert inf.declarado is None and inf.coincide is None
    texto = "\n".join(m.lineas(inf, m.cargar_criterio(repo)))
    assert CENTINELA not in texto
    for dia in DEV + RESERVADOS:
        assert dia not in texto, "la salida nombra un dia"


def test_el_control_coincide_o_para(m: ModuleType, tmp_path: Path) -> None:
    """Un libro declarado se mide igual; si su veredicto no es el declarado, `coincide` es False
    y `main` saldria con el codigo de control fallido."""
    repo, libro, dev = _repo(tmp_path)
    _declarar(repo, libro, huso="UTC")
    inf = m.medir_libro(repo, libro, "2026-03", None, _velas(m, dev, timedelta(0)))
    assert (inf.declarado, inf.veredicto, inf.coincide) == ("UTC", "UTC", True)
    inf = m.medir_libro(repo, libro, "2026-03", None, _velas(m, dev, timedelta(hours=-1)))
    assert (inf.declarado, inf.veredicto, inf.coincide) == ("UTC", "Europe/Madrid", False)
    assert "NO COINCIDE" in "\n".join(m.lineas(inf, m.cargar_criterio(repo)))


def test_sin_formato_un_libro_no_declarado_no_se_mide(m: ModuleType, tmp_path: Path) -> None:
    repo, libro, dev = _repo(tmp_path)
    with pytest.raises(m.HusoError, match="--formato es obligatorio"):
        m.medir_libro(repo, libro, "2026-03", None, _velas(m, dev, timedelta(0)))


def test_un_mes_sin_dias_dev_no_se_mide(m: ModuleType, tmp_path: Path) -> None:
    repo, libro, dev = _repo(tmp_path)
    with pytest.raises(m.HusoError, match="ningun dia `dev`"):
        m.medir_libro(repo, libro, "2026-04", "AAAA/MM/DD HH:MM:SS", _velas(m, dev, timedelta(0)))
