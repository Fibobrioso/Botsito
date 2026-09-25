"""El camino de fidelidad para un segundo mes (ADR-0046): la regla de cupos desde N, el filtro por
el mes del id y el sorteo que no se repite nunca. Sobre repos SINTETICOS; el unico test que toca el
repo real es el de septiembre, y se salta sin `data/`."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

import pytest

from botsito.cases import fidelidad as fid
from botsito.cases.paquete import KitError, config_desde_doc
from botsito.data.dataset import congelar
from tests.unit.test_kit import CONFIG_FIDELIDAD, HOY, _repo_fidelidad, descarga

REPO = Path(__file__).resolve().parents[2]

REGLA_MARZO = """cupos_por_mes:
  "2026-05":
    - {particion: fidelidad-dev, de: total, fraccion: "1/3"}
    - {particion: fidelidad-2, de: resto, fraccion: "1/2"}
    - {particion: fidelidad-3, de: resto, fraccion: "1/1"}
    - {particion: fidelidad-1, fijo: 0}
"""


def _formula(n: int) -> dict[str, int]:
    """La regla del consultor escrita a mano, independiente del codigo que la aplica."""
    dev = n // 3
    dos = (n - dev) // 2
    return {
        "fidelidad-dev": dev,
        "fidelidad-2": dos,
        "fidelidad-3": n - dev - dos,
        "fidelidad-1": 0,
    }


def _regla(texto: str = REGLA_MARZO, mes: str = "2026-05") -> tuple[fid.Paso, ...]:
    import yaml

    return fid.reglas_de_cupos(yaml.safe_load(texto), "prueba")[mes]


# ---------------------------------------------------------------- la regla de cupos


def test_n_cero_se_niega() -> None:
    with pytest.raises(fid.FidelidadError, match="N = 0"):
        fid.cupos_desde_regla(_regla(), 0)


@pytest.mark.parametrize(
    ("n", "esperado"),
    [
        (1, {"fidelidad-dev": 0, "fidelidad-2": 0, "fidelidad-3": 1, "fidelidad-1": 0}),
        (2, {"fidelidad-dev": 0, "fidelidad-2": 1, "fidelidad-3": 1, "fidelidad-1": 0}),
        (3, {"fidelidad-dev": 1, "fidelidad-2": 1, "fidelidad-3": 1, "fidelidad-1": 0}),
        (20, {"fidelidad-dev": 6, "fidelidad-2": 7, "fidelidad-3": 7, "fidelidad-1": 0}),
    ],
)
def test_cupos_explicitos(n: int, esperado: dict[str, int]) -> None:
    assert fid.cupos_desde_regla(_regla(), n) == esperado


def test_la_regla_real_de_marzo_es_la_del_consultor() -> None:
    """La regla vive en el config del repo (ADR-0002) y dice lo mismo que ADR-0046, N a N."""
    config = fid.cargar_config(REPO)
    regla = fid.reglas_de_cupos(config.doc, "config.yaml")["2026-03"]
    for n in range(1, 41):
        cupos = fid.cupos_desde_regla(regla, n)
        assert cupos == _formula(n), n
        assert sum(cupos.values()) == n
    # Y septiembre sigue con sus cifras, sin regla: 4/10/0/0.
    assert "2026-09" not in fid.reglas_de_cupos(config.doc, "config.yaml")
    assert config.particiones == {
        "fidelidad-dev": 4,
        "fidelidad-1": 10,
        "fidelidad-2": 0,
        "fidelidad-3": 0,
    }


@pytest.mark.parametrize(
    ("viejo", "nuevo", "mensaje"),
    [
        ("    - {particion: fidelidad-1, fijo: 0}\n", "", "exactamente una vez"),
        ('fraccion: "1/3"', 'fraccion: "4/3"', "0 <= a <= b"),
        ('fraccion: "1/3"', 'fraccion: "1/0"', "0 <= a <= b"),
        ("de: total", "de: todo", "de: total|resto"),
        ('"2026-05":', '"2026-5":', "AAAA-MM"),
    ],
)
def test_una_regla_mal_formada_no_carga(viejo: str, nuevo: str, mensaje: str) -> None:
    import yaml

    with pytest.raises(fid.FidelidadError, match=mensaje):
        fid.reglas_de_cupos(yaml.safe_load(REGLA_MARZO.replace(viejo, nuevo)), "prueba")


def test_una_regla_que_no_reparte_los_n_se_niega() -> None:
    """`asignar` dejaria fuera en silencio lo que no quepa: la regla tiene que repartirlo todo."""
    corta = REGLA_MARZO.replace('de: resto, fraccion: "1/1"', 'de: resto, fraccion: "1/2"')
    with pytest.raises(fid.FidelidadError, match="sin particion"):
        fid.cupos_desde_regla(_regla(corta), 9)


def test_el_kit_no_admite_cupos_por_mes() -> None:
    import yaml

    doc = yaml.safe_load(CONFIG_FIDELIDAD.replace("fidelidad-", "p-") + REGLA_MARZO)
    with pytest.raises(KitError, match="exactamente"):
        config_desde_doc(doc, "kit")


# ---------------------------------------------------------------- el mes del artefacto


def test_un_id_sin_mes_no_se_sortea(tmp_path: Path) -> None:
    repo = _repo_fidelidad(tmp_path)
    with pytest.raises(fid.FidelidadError, match="AAAA-MM"):
        fid.construir(repo, repo / "data", "xxxyyy", 3)
    with pytest.raises(fid.FidelidadError, match="AAAA-MM"):
        fid.construir(repo, repo / "data", "xxxyyy-2026-13", 3)


def _dos_meses(tmp_path: Path, regla: str = "") -> Path:
    """Mayo del repo sintetico MAS junio, los dos con cobertura: el caso que hoy rompia."""
    config = CONFIG_FIDELIDAD.replace(
        'cobertura_material:\n  "2026-05":\n'
        '    - {desde: "2026-05-04", hasta: "2026-05-08", entregado_el: "2026-09-20",'
        " fuente: [ADR-0034]}\n",
        'cobertura_material:\n  "2026-05":\n'
        '    - {desde: "2026-05-04", hasta: "2026-05-08", entregado_el: "2026-09-20",'
        " fuente: [ADR-0034]}\n"
        '  "2026-06":\n'
        '    - {desde: "2026-06-01", hasta: "2026-06-05", entregado_el: "2026-09-20",'
        " fuente: [ADR-0034]}\n",
    )
    assert config != CONFIG_FIDELIDAD
    repo = _repo_fidelidad(tmp_path, config + regla)
    congelar(
        repo=repo,
        carpeta_datos=repo / "data",
        nombre="prueba",
        simbolo="XXXYYY",
        escala=100000,
        desde=date(2026, 5, 16),
        hasta=date(2026, 6, 12),
        descarga=descarga,
        hoy=HOY,
    )
    return repo


def test_el_artefacto_de_un_mes_no_contiene_ningun_dia_de_otro_mes(tmp_path: Path) -> None:
    repo = _dos_meses(tmp_path)
    mayo = fid.construir(repo, repo / "data", "xxxyyy-2026-05", 3)
    junio = fid.construir(repo, repo / "data", "xxxyyy-2026-06", 3)
    assert mayo.casos and all(c.dia.startswith("2026-05") for c in mayo.casos)
    assert junio.casos and all(c.dia.startswith("2026-06") for c in junio.casos)
    motivos = {e.dia: e.motivo for e in mayo.excluidos}
    assert motivos["2026-06-01"] == "de otro mes que el del artefacto (2026-05)"
    # Un dia fuera del tramo conserva SU motivo: el filtro del mes va despues del de cobertura.
    assert "fuera de la cobertura del material del trader" in motivos["2026-05-19"]


def test_la_regla_del_mes_decide_los_cupos_y_queda_en_particiones(tmp_path: Path) -> None:
    import yaml

    repo = _dos_meses(tmp_path, REGLA_MARZO)
    a = fid.construir(repo, repo / "data", "xxxyyy-2026-05", 7)
    n = a.universo
    assert n == 5
    assert len(a.casos) == n, "la regla reparte TODOS los casos: ninguno se cae en silencio"
    cupos = yaml.safe_load(a.ficheros["particiones.yaml"])["cupos"]
    assert cupos == _formula(n)
    contados = {p: list(a.asignacion.values()).count(p) for p in _formula(n)}
    assert contados == _formula(n)
    # Junio no tiene regla: usa los cupos fijos del config.
    j = fid.construir(repo, repo / "data", "xxxyyy-2026-06", 7)
    assert yaml.safe_load(j.ficheros["particiones.yaml"])["cupos"]["fidelidad-dev"] == 2
    # Y se reproduce con lo congelado.
    fid.escribir(repo, a)
    assert fid.comprobar(repo, repo / "data", "xxxyyy-2026-05") == ([], [])


# ---------------------------------------------------------------- el sorteo no se repite


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def test_el_sorteo_no_se_repite_nunca(tmp_path: Path) -> None:
    repo = _repo_fidelidad(tmp_path)
    for args in (
        ("init", "-q", "-b", "main"),
        ("config", "user.email", "t@t"),
        ("config", "user.name", "t"),
        ("config", "core.autocrlf", "false"),
    ):
        _git(repo, *args)
    fid.escribir(repo, fid.construir(repo, repo / "data", "xxxyyy-2026-05", 3))
    # 1. Con la carpeta delante, ni con otra semilla.
    with pytest.raises(fid.FidelidadError, match="ya existe"):
        fid.escribir(repo, fid.construir(repo, repo / "data", "xxxyyy-2026-05", 4))
    # 2. Commiteado y BORRADO despues: el historial lo recuerda.
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "sorteo")
    carpeta = repo / fid.DIRECTORIO_FIDELIDAD / "xxxyyy-2026-05"
    for f in carpeta.iterdir():
        f.unlink()
    carpeta.rmdir()
    with pytest.raises(fid.FidelidadError, match="EL SORTEO NO SE REPITE NUNCA"):
        fid.escribir(repo, fid.construir(repo, repo / "data", "xxxyyy-2026-05", 5))
    assert not carpeta.exists()


def test_un_id_con_ancla_no_se_vuelve_a_sortear(tmp_path: Path) -> None:
    """Sin git y sin carpeta, el ancla basta para negarse."""
    repo = _repo_fidelidad(tmp_path)
    (repo / fid.DIRECTORIO_FIDELIDAD / fid.FICHERO_ANCLAS).write_text(
        "xxxyyy-2026-05:\n  particiones.yaml: "
        + "a" * 40
        + "\n  ventanas.yaml: "
        + "b" * 40
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(fid.FidelidadError, match="tiene ancla"):
        fid.escribir(repo, fid.construir(repo, repo / "data", "xxxyyy-2026-05", 3))


# ---------------------------------------------------------------- septiembre, el real


@pytest.mark.skipif(
    not (REPO / "data" / "raw").is_dir(),
    reason="sin data/: septiembre solo se recompone con sus velas",
)
def test_septiembre_se_reconstruye_igual_con_el_filtro_por_mes() -> None:
    assert fid.comprobar(REPO, REPO / "data", "eurusd-2026-09") == ([], [])
