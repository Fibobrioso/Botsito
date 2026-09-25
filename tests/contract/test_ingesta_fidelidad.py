"""`casos ingerir --artefacto` (ADR-0046 §7): los `fidelidad-dev` de un artefacto, y nada mas.

LA CENTINELA. Las filas de los dias RESERVADOS del libro sintetico llevan en `side`, `entryPrice`
e `initialSL` una cadena que no es un precio ni una direccion. Si una fila reservada llegara a la
ingesta, pasarian dos cosas a la vez: el comando reventaria en `side` -la centinela esta viva, y
un test lo comprueba pidiendo ese dia a proposito- y su texto podria salir por algun sitio. Por eso
cada test que abre mira las TRES salidas -stdout, stderr y los ficheros escritos- y exige que la
centinela no este en ninguna. El cinturon es no pedir el dia; esto son los tirantes.

Las fechas de las filas reservadas SI son legibles, a proposito: una fecha ilegible hace fallar
el libro entero antes de saber de que dia es la fila, y entonces la centinela no probaria nada.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from botsito import cli
from botsito.cases.ingesta import IngestaError, ingerir

from .test_ingesta import SESIONES, _declarar, _xlsx

REAL = Path(__file__).resolve().parents[2]
FID = "knowledge/cases/fidelidad"
ART = "eurusd-2026-03"
CENTINELA = "CENTINELA-RESERVADA-no-debe-salir"
CAB = ["dateStart", "side", "entryPrice", "initialSL", "maxTP", "idealTP"]
# Marzo de 2026 antes del cambio de hora: Madrid es UTC+1, y las 08:00 y 12:00 UTC caen en las
# sesiones 07-11 y 11-15.
MARZO = [
    CAB,
    ["2026/03/02 08:00:00", "buy", "1.1000", "1.0990", "", "1.1005"],  # dev
    ["2026/03/03 08:00:00", CENTINELA, CENTINELA, CENTINELA, CENTINELA, CENTINELA],  # f-2
    ["2026/03/04 12:00:00", CENTINELA, CENTINELA, CENTINELA, CENTINELA, CENTINELA],  # f-3
    ["2026/03/05 12:00:00", "sell", "1.3000", "1.3010", "1.2970", "1.2990"],  # dev
    ["2026/03/06 08:00:00", CENTINELA, CENTINELA, CENTINELA, CENTINELA, CENTINELA],  # f-2
]
ABRIL = [CAB, ["2026/04/01 08:00:00", "buy", "1.2000", "1.1990", "", "1.2005"]]
ASIGNACION = {
    "caso-eurusd-2026-03-02": "fidelidad-dev",
    "caso-eurusd-2026-03-03": "fidelidad-2",
    "caso-eurusd-2026-03-04": "fidelidad-3",
    "caso-eurusd-2026-03-05": "fidelidad-dev",
    "caso-eurusd-2026-03-06": "fidelidad-2",
}
RESERVADOS = ("2026-03-03", "2026-03-04", "2026-03-06")


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _repo(
    tmp: Path,
    *,
    sorteado: bool = True,
    anclado: bool = True,
    commiteado: bool = True,
    asignacion: dict[str, str] | None = None,
) -> tuple[Path, dict[str, Path]]:
    libros = {"marzo": tmp / "marzo.xlsx", "abril": tmp / "abril.xlsx"}
    _xlsx(libros["marzo"], MARZO)
    _xlsx(libros["abril"], ABRIL)
    repo = tmp / "repo"
    (repo / FID).mkdir(parents=True)
    (repo / "knowledge/spec").mkdir(parents=True)
    (repo / "knowledge/corpus").mkdir(parents=True)
    shutil.copy(REAL / "knowledge/spec/parametros.yaml", repo / "knowledge/spec/parametros.yaml")
    # El config del kit, tal cual: es el que lee el comando SIN `--artefacto`.
    (repo / "knowledge/cases/kit").mkdir(parents=True)
    shutil.copy(REAL / "knowledge/cases/kit/config.yaml", repo / "knowledge/cases/kit/config.yaml")
    config = yaml.safe_load((REAL / FID / "config.yaml").read_text(encoding="utf-8"))
    config["cobertura_material"] = {
        "2026-03": [
            {"desde": "2026-03-02", "hasta": "2026-03-31", "material_sha256": _sha(libros["marzo"])}
        ],
        "2026-04": [
            {"desde": "2026-04-01", "hasta": "2026-04-30", "material_sha256": _sha(libros["abril"])}
        ],
    }
    (repo / FID / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    ficheros = [{"ruta": f"{n}.xlsx", "sha256": _sha(p)} for n, p in libros.items()]
    (repo / "knowledge/corpus/manifest.yaml").write_text(
        yaml.safe_dump({"ficheros": ficheros}), encoding="utf-8"
    )
    _declarar(repo, *libros.values())
    _git(repo, "init", "-q")
    if sorteado:
        carpeta = repo / FID / ART
        carpeta.mkdir()
        (carpeta / "particiones.yaml").write_text(
            yaml.safe_dump({"artefacto": ART, "asignacion": asignacion or ASIGNACION}),
            encoding="utf-8",
        )
        (carpeta / "ventanas.yaml").write_text("artefacto: eurusd-2026-03\n", encoding="utf-8")
        if anclado:
            anclas = {
                ART: {
                    n: _git(repo, "hash-object", "--", f"{FID}/{ART}/{n}")
                    for n in ("particiones.yaml", "ventanas.yaml")
                }
            }
            (repo / FID / "anclas.yaml").write_text(yaml.safe_dump(anclas), encoding="utf-8")
    if commiteado:
        _git(repo, "add", "-A")
        _git(repo, "commit", "-q", "-m", "reparto")
    else:
        # Todo menos el artefacto: el reparto queda sin commitear.
        _git(repo, "add", "knowledge/spec", "knowledge/corpus", "knowledge/cases/kit")
        _git(repo, "add", f"{FID}/config.yaml")
        _git(repo, "commit", "-q", "-m", "sin el reparto")
    return repo, libros


def _ingerir(repo: Path, libro: Path, *extra: str) -> int:
    return cli.main(
        [
            "--repo",
            str(repo),
            "casos",
            "ingerir",
            "--material",
            str(libro),
            "--fecha",
            "2026-09-24",
            *extra,
        ]
    )


def _escritos(repo: Path) -> dict[str, str]:
    dev = repo / "knowledge/cases/dev"
    if not dev.is_dir():
        return {}
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(dev.glob("*.yaml"))}


def _sin_centinela(repo: Path, salida: str) -> None:
    """Las TRES salidas: la de consola y cada fichero escrito bajo `knowledge/cases/dev/`."""
    assert CENTINELA not in salida
    for nombre, texto in _escritos(repo).items():
        assert CENTINELA not in texto, f"{nombre} lleva la centinela de una fila reservada"
    for dia in RESERVADOS:
        assert dia not in salida, f"la salida nombra el dia reservado {dia}"


@pytest.mark.contract
def test_abre_los_fidelidad_dev_y_ninguna_fila_reservada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """El test que ABRE: sin uno que pase, la guarda solo demostraria que sabe decir que no."""
    repo, libros = _repo(tmp_path)
    assert _ingerir(repo, libros["marzo"], "--artefacto", ART) == 0
    cap = capsys.readouterr()
    escritos = _escritos(repo)
    assert sorted(escritos) == ["caso-eurusd-2026-03-02", "caso-eurusd-2026-03-05"]
    compra = yaml.safe_load(escritos["caso-eurusd-2026-03-02"])
    assert compra["operaciones"] == [
        {
            "instante_utc": "2026-03-02T08:00:00+00:00",
            "sesion": "07-11",
            "direccion": "compra",
            "entrada": "1.1000",
            "stop": "1.0990",
        }
    ]
    venta = yaml.safe_load(escritos["caso-eurusd-2026-03-05"])
    assert [o["sesion"] for o in venta["operaciones"]] == ["11-15"]
    assert "2 casos escritos de 2 dias ingeribles; 2 filas leidas" in cap.out
    _sin_centinela(repo, cap.out + cap.err)


@pytest.mark.contract
def test_la_centinela_esta_viva(tmp_path: Path) -> None:
    """Si se pidiera un dia reservado, su fila rompe la ingesta y el error no la reproduce. Sin
    esto, que la centinela no salga no probaria nada: podria no salir porque nunca se leyo."""
    repo, libros = _repo(tmp_path)
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, libros["marzo"], "Europe/Madrid", SESIONES, dias=["2026-03-03"])
    assert "`side` no es buy ni sell" in str(exc.value)
    assert CENTINELA not in str(exc.value)


@pytest.mark.contract
def test_sin_artefacto_el_comando_hace_lo_de_antes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Sin `--artefacto`, los `fidelidad-dev` se cuentan y no se toman, con el libro correcto."""
    repo, libros = _repo(tmp_path)
    assert _ingerir(repo, libros["marzo"]) == 1
    cap = capsys.readouterr()
    assert _escritos(repo) == {}
    assert "2 dias del camino de FIDELIDAD no los toma este comando sin `--artefacto`" in cap.err
    assert "2026-03-02" not in cap.err and "2026-03-05" not in cap.err
    _sin_centinela(repo, cap.out + cap.err)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("sorteado", "anclado", "commiteado", "mensaje"),
    [
        (False, True, True, "no esta sorteado"),
        (True, False, True, "no esta anclado"),
        (True, True, False, "no esta commiteado"),
    ],
)
def test_sin_sorteo_sin_ancla_o_sin_commit_se_niega(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    sorteado: bool,
    anclado: bool,
    commiteado: bool,
    mensaje: str,
) -> None:
    repo, libros = _repo(tmp_path, sorteado=sorteado, anclado=anclado, commiteado=commiteado)
    assert _ingerir(repo, libros["marzo"], "--artefacto", ART) == 1
    cap = capsys.readouterr()
    assert mensaje in cap.err
    assert _escritos(repo) == {}
    _sin_centinela(repo, cap.out + cap.err)


@pytest.mark.contract
def test_un_reparto_que_cambio_despues_del_ancla_se_niega(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """El mutante: un reservado pasado a `fidelidad-dev` y commiteado. El ancla lo caza."""
    repo, libros = _repo(tmp_path)
    ruta = repo / FID / ART / "particiones.yaml"
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace(
            "2026-03-03: fidelidad-2", "2026-03-03: fidelidad-dev"
        ),
        encoding="utf-8",
    )
    _git(repo, "commit", "-q", "-am", "mutante")
    assert _ingerir(repo, libros["marzo"], "--artefacto", ART) == 1
    cap = capsys.readouterr()
    assert "no es el que ancla" in cap.err
    assert _escritos(repo) == {}
    _sin_centinela(repo, cap.out + cap.err)


@pytest.mark.contract
def test_el_libro_de_otro_mes_no_se_lee(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """El libro de abril esta declarado y en el corpus, pero su sha es de 2026-04: no se lee."""
    repo, libros = _repo(tmp_path)
    assert _ingerir(repo, libros["abril"], "--artefacto", ART) == 1
    cap = capsys.readouterr()
    assert "ese mes no tiene ningun dia ingerible en el camino de fidelidad" in cap.err
    assert _escritos(repo) == {}


@pytest.mark.contract
def test_un_id_sin_mes_se_niega(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo, libros = _repo(tmp_path)
    assert _ingerir(repo, libros["marzo"], "--artefacto", "eurusd-marzo") == 1
    assert "tiene que ser <simbolo>-AAAA-MM" in capsys.readouterr().err
    assert _escritos(repo) == {}


@pytest.mark.contract
def test_todos_los_dev_ocultos_no_escribe_nada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Un artefacto sin ningun `fidelidad-dev` no ingiere nada y no nombra ningun dia."""
    solo_reservados = {c: "fidelidad-2" for c in ASIGNACION}
    repo, libros = _repo(tmp_path, asignacion=solo_reservados)
    assert _ingerir(repo, libros["marzo"], "--artefacto", ART) == 1
    cap = capsys.readouterr()
    assert "no tiene ningun dia `fidelidad-dev` ingerible" in cap.err
    assert "2026-03-0" not in cap.err
    assert _escritos(repo) == {}
