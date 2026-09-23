"""La regla del mes sin filas, por la CLI (2026-09-23, rama `trabajo/regla-mes-sin-filas`).

Se MANTIENE, aplicando el criterio fijado antes de medir: detecta un libro cuyo sha esta atado en
`cobertura_material` al tramo de OTRO mes, que ningun otro mecanismo detecta, y cuenta solo sobre
los dias pedidos. Estos son los casos que hasta hoy no tenian test por el camino de verdad -`botsito
casos ingerir`-, no llamando a `ingerir` a mano.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from botsito import cli
from botsito.cases.ingesta import mensaje_mes_sin_filas
from botsito.corpus.libros import sha256_de

from .test_ingesta import _declarar, _xlsx

REAL = Path(__file__).resolve().parents[2]
KIT = "knowledge/cases/kit"
CAB = ["dateStart", "side", "entryPrice", "initialSL"]
MAYO = [
    CAB,
    ["2026/05/08 07:30:00", "buy", "1.1000", "1.0990"],
    ["2026/05/12 08:00:00", "sell", "1.2", "1.21"],
]
JULIO = [CAB, ["2026/07/06 08:00:00", "buy", "1.5000", "1.4990"]]
DEV_MAYO_Y_JULIO = {
    "caso-eurusd-2026-05-08": "dev",
    "caso-eurusd-2026-05-12": "dev",
    "caso-eurusd-2026-05-13": "holdout-1",
    "caso-eurusd-2026-07-06": "dev",
}


def _montar(
    tmp: Path,
    asignacion: dict[str, str],
    libros: dict[str, list[list[str]]],
    atados: dict[str, str],
    husos: dict[str, str] | None = None,
) -> tuple[Path, dict[str, Path]]:
    """Repo minimo: reparto del kit, `cobertura_material` con cada sha atado al mes que se diga,
    manifiesto del corpus y `libros.yaml` (formato AAAA/MM/DD; huso UTC salvo que se diga otro)."""
    repo = tmp / "repo"
    (repo / KIT / "2026-09-09-sesion-01").mkdir(parents=True)
    (repo / "knowledge/spec").mkdir(parents=True)
    (repo / "knowledge/corpus").mkdir(parents=True)
    shutil.copy(REAL / "knowledge/spec/parametros.yaml", repo / "knowledge/spec/parametros.yaml")
    rutas: dict[str, Path] = {}
    for nombre, filas in libros.items():
        rutas[nombre] = tmp / f"{nombre}.xlsx"
        _xlsx(rutas[nombre], filas)
    config = yaml.safe_load((REAL / KIT / "config.yaml").read_text(encoding="utf-8"))
    config["cobertura_material"] = {
        mes: [{"desde": f"{mes}-01", "hasta": f"{mes}-28", "material_sha256": sha256_de(rutas[n])}]
        for mes, n in atados.items()
    }
    (repo / KIT / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    (repo / KIT / "2026-09-09-sesion-01/particiones.yaml").write_text(
        yaml.safe_dump({"asignacion": asignacion}), encoding="utf-8"
    )
    (repo / "knowledge/corpus/manifest.yaml").write_text(
        yaml.safe_dump(
            {"ficheros": [{"ruta": p.name, "sha256": sha256_de(p)} for p in rutas.values()]}
        ),
        encoding="utf-8",
    )
    for nombre, ruta in rutas.items():
        _declarar(repo, ruta, huso=(husos or {}).get(nombre, "UTC"))
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "repartos")):
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True,
            capture_output=True,
        )
    return repo, rutas


def _ingerir(repo: Path, libro: Path) -> int:
    return cli.main(
        ["--repo", str(repo), "casos", "ingerir", "--material", str(libro), "--fecha", "2026-09-23"]
    )


def _escritos(repo: Path) -> list[str]:
    dev = repo / "knowledge/cases/dev"
    return sorted(p.name for p in dev.glob("*.yaml")) if dev.is_dir() else []


@pytest.mark.contract
def test_a2_un_libro_atado_al_tramo_de_otro_mes_lo_para_la_regla(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """(a2) El sha del libro de JULIO esta atado al tramo de MAYO. La puerta pide los dias `dev` de
    mayo, el libro no tiene ninguno, y la regla lo para: es lo UNICO que lo detecta."""
    repo, libros = _montar(
        tmp_path,
        DEV_MAYO_Y_JULIO,
        {"mayo": MAYO, "julio": JULIO},
        {"2026-05": "julio", "2026-07": "mayo"},
    )
    assert _ingerir(repo, libros["julio"]) == 1
    assert _escritos(repo) == []
    assert f"ERROR: {mensaje_mes_sin_filas(['2026-05'])}" in capsys.readouterr().err


@pytest.mark.contract
def test_d_dias_pedidos_sin_ninguna_fila_en_un_libro_correcto_dan_el_mismo_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """(d) COSTE ACEPTADO. El libro ES el de mayo, pero ninguno de los dias pedidos tiene fila -solo
    tiene una del dia reservado, que no se pide-. La regla no puede distinguir esto de (a2): las dos
    cosas dan exactamente el mismo cero sobre los dias pedidos. Y aqui no hay nada que escribir, asi
    que parar no pierde ningun caso: solo obliga a mirar. Por eso se acepta, y el mensaje nombra las
    dos lecturas en vez de elegir una. Tampoco nombra el dia reservado cuya fila si existe."""
    vacio = [CAB, ["2026/05/13 08:00:00", "buy", "1.2000", "1.1990"]]
    repo, libros = _montar(
        tmp_path, DEV_MAYO_Y_JULIO, {"mayo_vacio": vacio}, {"2026-05": "mayo_vacio"}
    )
    assert _ingerir(repo, libros["mayo_vacio"]) == 1
    assert _escritos(repo) == []
    err = capsys.readouterr().err
    assert f"ERROR: {mensaje_mes_sin_filas(['2026-05'])}" in err
    assert "2026-05-13" not in err


@pytest.mark.contract
def test_f_si_todos_los_dias_pedidos_son_reservados_no_hay_nada_que_leer_y_no_se_nombra_ninguno(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """(f) Los dos dias de mayo estan reservados: la puerta los quita antes de leer, y la regla ni
    se alcanza."""
    asignacion = {
        "caso-eurusd-2026-05-08": "holdout-1",
        "caso-eurusd-2026-05-12": "holdout-2",
        "caso-eurusd-2026-07-06": "dev",
    }
    repo, libros = _montar(
        tmp_path,
        asignacion,
        {"mayo": MAYO, "julio": JULIO},
        {"2026-05": "mayo", "2026-07": "julio"},
    )
    assert _ingerir(repo, libros["mayo"]) == 1
    assert _escritos(repo) == []
    err = capsys.readouterr().err
    esperado = (
        "ERROR: el material es de 2026-05 y ese mes no tiene ningun dia ingerible en el camino "
        "del kit"
    )
    assert esperado in err
    assert "2026-05-08" not in err and "2026-05-12" not in err


@pytest.mark.contract
def test_b_extremo_un_huso_mal_declarado_que_saca_todas_las_filas_del_mes_lo_para_la_regla(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """(b), el caso EXTREMO: la fila del 1 de mayo esta en UTC, pero el libro se declara en
    `Pacific/Kiritimati` (UTC+14), asi que su instante cae el 30 de abril y ninguno de los dias
    pedidos de mayo tiene fila. La regla lo caza. El caso NORMAL de (b) -filas que se van a otro dia
    DENTRO del mes, no pedido- NO se testea aqui: hoy no lo detecta nada (Technical Debt).
    El control: el mismo libro declarado en UTC si se ingiere."""
    asignacion = {"caso-eurusd-2026-05-01": "dev"}
    filas = [CAB, ["2026/05/01 07:30:00", "buy", "1.1000", "1.0990"]]
    repo, libros = _montar(
        tmp_path,
        asignacion,
        {"mayo": filas},
        {"2026-05": "mayo"},
        husos={"mayo": "Pacific/Kiritimati"},
    )
    assert _ingerir(repo, libros["mayo"]) == 1
    assert _escritos(repo) == []
    assert f"ERROR: {mensaje_mes_sin_filas(['2026-05'])}" in capsys.readouterr().err

    control, libros_c = _montar(
        tmp_path / "control", asignacion, {"mayo": filas}, {"2026-05": "mayo"}
    )
    assert _ingerir(control, libros_c["mayo"]) == 0
    assert _escritos(control) == ["caso-eurusd-2026-05-01.yaml"]
