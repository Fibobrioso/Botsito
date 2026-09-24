"""El mes del material se DECLARA, y `casos ingerir` solo toma dias del camino del kit.

Rama `trabajo/mayo-dev-ingerido`, 2026-09-22. La revision de diseno midio sobre el repo real que
`dias_ingeribles` devolvia 10 dias y no 6 -los 6 `dev` de mayo mas los 4 `fidelidad-dev` de
septiembre-, y que con el libro de mayo el comando fallaba con «no tiene ni una fila de 2026-09».
Ese «falla cerrada» NO ERA LA PUERTA: era la regla de cobertura protegiendo por coincidencia. Los
tests de F14a no lo vieron porque montan UN SOLO REPARTO -el patron 3 en los tests: enumerar el
caso que se penso en vez de la condicion-. Por eso aqui hay SIEMPRE DOS: el del kit, con dos
meses, y el de fidelidad.

Todo por la CLI y con libros sinteticos: lo que se prueba es el comando que se ejecuta.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

from botsito import cli
from botsito.cases.paquete import KitError, config_desde_doc

from .test_ingesta import _declarar, _xlsx

REAL = Path(__file__).resolve().parents[2]
KIT = "knowledge/cases/kit"
CAB = ["dateStart", "side", "entryPrice", "initialSL", "maxTP", "idealTP"]

# Mayo trae una fila de JULIO a proposito: el libro no decide que dias se piden, la declaracion si.
MAYO = [
    CAB,
    ["2026/05/08 07:30:00", "buy", "1.1000", "1.0990", "1.1030", "1.1005"],
    ["2026/05/12 12:00:00", "sell", "1.3000", "1.3010", "", "1.2990"],
    ["2026/05/13 08:00:00", "buy", "1.2000", "1.1990", "", "1.2005"],  # RESERVADO
    ["2026/07/06 08:00:00", "buy", "1.5000", "1.4990", "", "1.5005"],  # otro mes
]
JULIO = [CAB, ["2026/07/06 08:00:00", "buy", "1.5000", "1.4990", "", "1.5005"]]
SEPTIEMBRE = [
    CAB,
    ["2026/09/01 08:00:00", "buy", "1.6000", "1.5990", "", "1.6005"],
    ["2026/09/04 08:00:00", "sell", "1.7000", "1.7010", "", "1.6990"],
]
KIT_ASIGNACION = {
    "caso-eurusd-2026-05-08": "dev",
    "caso-eurusd-2026-05-12": "dev",
    "caso-eurusd-2026-05-13": "holdout-1",
    "caso-eurusd-2026-07-06": "dev",
    "caso-eurusd-2026-07-07": "dev",
}
FIDELIDAD_ASIGNACION = {
    "caso-eurusd-2026-09-01": "fidelidad-dev",
    "caso-eurusd-2026-09-04": "fidelidad-dev",
    "caso-eurusd-2026-09-02": "fidelidad-1",
}


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _libros(tmp: Path) -> dict[str, Path]:
    libros = {"mayo": MAYO, "julio": JULIO, "septiembre": SEPTIEMBRE, "ajeno": MAYO[:2]}
    salida: dict[str, Path] = {}
    for nombre, filas in libros.items():
        ruta = tmp / f"{nombre}.xlsx"
        _xlsx(ruta, filas)
        salida[nombre] = ruta
    # El «ajeno» cambia un byte del contenido para no compartir sha con ninguno.
    _xlsx(salida["ajeno"], [*MAYO[:2], ["2026/05/08 09:00:00", "buy", "1.1", "1.0", "", ""]])
    return salida


def _repo(
    tmp: Path,
    libros: dict[str, Path],
    en_manifiesto: tuple[str, ...],
    sin_sha: tuple[str, ...] = (),
) -> Path:
    repo = tmp / "repo"
    (repo / KIT / "2026-09-09-sesion-01").mkdir(parents=True)
    (repo / "knowledge/cases/fidelidad/eurusd-2026-09").mkdir(parents=True)
    (repo / "knowledge/spec").mkdir(parents=True)
    (repo / "knowledge/corpus").mkdir(parents=True)
    shutil.copy(REAL / "knowledge/spec/parametros.yaml", repo / "knowledge/spec/parametros.yaml")

    config = yaml.safe_load((REAL / KIT / "config.yaml").read_text(encoding="utf-8"))
    config["cobertura_material"] = {
        mes: [
            {"desde": f"{mes}-01", "hasta": f"{mes}-28"}
            if mes in sin_sha
            else {"desde": f"{mes}-01", "hasta": f"{mes}-28", "material_sha256": _sha(libros[n])}
        ]
        for mes, n in (("2026-05", "mayo"), ("2026-07", "julio"), ("2026-09", "septiembre"))
    }
    (repo / KIT / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    for ruta, asignacion in (
        (repo / KIT / "2026-09-09-sesion-01/particiones.yaml", KIT_ASIGNACION),
        (repo / "knowledge/cases/fidelidad/eurusd-2026-09/particiones.yaml", FIDELIDAD_ASIGNACION),
    ):
        ruta.write_text(yaml.safe_dump({"asignacion": asignacion}), encoding="utf-8")
    ficheros = [{"ruta": f"{n}.xlsx", "sha256": _sha(libros[n])} for n in en_manifiesto]
    (repo / "knowledge/corpus/manifest.yaml").write_text(
        yaml.safe_dump({"ficheros": ficheros}), encoding="utf-8"
    )
    # Los libros del corpus de prueba, declarados (ADR-0039): lo que aqui se prueba es el MES.
    _declarar(repo, *(libros[n] for n in en_manifiesto))
    for args in (("init", "-q"), ("add", "-A"), ("commit", "-q", "-m", "repartos")):
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True,
            capture_output=True,
        )
    return repo


def _ingerir(repo: Path, libro: Path) -> int:
    return cli.main(
        ["--repo", str(repo), "casos", "ingerir", "--material", str(libro), "--fecha", "2026-09-22"]
    )


def _escritos(repo: Path) -> list[str]:
    dev = repo / "knowledge/cases/dev"
    return sorted(p.stem for p in dev.glob("caso-*.yaml")) if dev.is_dir() else []


@pytest.fixture
def montaje(tmp_path: Path) -> tuple[Path, dict[str, Path]]:
    libros = _libros(tmp_path)
    return _repo(tmp_path, libros, ("mayo", "julio", "septiembre", "ajeno")), libros


@pytest.mark.contract
def test_a_dos_meses_en_el_kit_el_libro_de_uno_ingiere_solo_ese_mes(
    montaje: tuple[Path, dict[str, Path]], capsys: pytest.CaptureFixture[str]
) -> None:
    """(a) Mayo y julio son ingeribles a la vez: el libro de mayo ingiere mayo, ni un dia de julio.

    Hasta hoy esto fallaba entero -«no tiene ni una fila de 2026-07»-, y la fila de julio que el
    libro trae a proposito tampoco entra: los dias salen de la declaracion, no de las filas.
    """
    repo, libros = montaje
    assert _ingerir(repo, libros["mayo"]) == 0
    assert _escritos(repo) == ["caso-eurusd-2026-05-08", "caso-eurusd-2026-05-12"]
    salida = capsys.readouterr().out
    assert "2 casos escritos de 2 dias ingeribles; 2 filas leidas" in salida
    assert "2026-05-13" not in salida and "2026-07" not in salida


@pytest.mark.contract
def test_a_y_el_otro_mes_con_su_libro_ingiere_el_suyo(
    montaje: tuple[Path, dict[str, Path]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Simetrico: la condicion es «el mes que el libro declara», no «mayo»."""
    repo, libros = montaje
    assert _ingerir(repo, libros["julio"]) == 0
    assert _escritos(repo) == ["caso-eurusd-2026-07-06"]
    assert "1 dias ingeribles sin ninguna operacion" in capsys.readouterr().err


@pytest.mark.contract
def test_b_un_sha_que_no_declara_ningun_tramo_es_error_y_no_escribe(
    montaje: tuple[Path, dict[str, Path]], capsys: pytest.CaptureFixture[str]
) -> None:
    """(b) El libro esta en el corpus pero ningun tramo dice de que mes es: no se deduce."""
    repo, libros = montaje
    assert _ingerir(repo, libros["ajeno"]) == 1
    assert _escritos(repo) == []
    assert "no lo declara ningun tramo de cobertura_material" in capsys.readouterr().err


@pytest.mark.contract
def test_b_un_libro_fuera_del_manifiesto_es_error_y_no_escribe(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Y si el sha no esta en el manifiesto del corpus, ni se mira la cobertura."""
    libros = _libros(tmp_path)
    repo = _repo(tmp_path, libros, ("julio", "septiembre"))
    assert _ingerir(repo, libros["mayo"]) == 1
    assert _escritos(repo) == []
    assert "no esta en knowledge/corpus/manifest.yaml" in capsys.readouterr().err


@pytest.mark.contract
def test_c_el_libro_correcto_de_septiembre_no_mete_ni_un_dia_de_fidelidad(
    montaje: tuple[Path, dict[str, Path]], capsys: pytest.CaptureFixture[str]
) -> None:
    """(c) LA OBLIGACION CONVERTIDA EN MECANISMO. El reparto de fidelidad esta, sus dos `dev` no
    estan reservados, y el libro que se pasa es EL CORRECTO de septiembre. Aun asi: cero dias de
    fidelidad ingeridos, y el mensaje lo dice citando la obligacion. Contados, no nombrados."""
    repo, libros = montaje
    assert _ingerir(repo, libros["septiembre"]) == 1
    assert _escritos(repo) == []
    err = capsys.readouterr().err
    assert "2 dias del camino de FIDELIDAD no los toma este comando" in err
    assert "Next Action" in err
    assert "2026-09-01" not in err and "2026-09-04" not in err


@pytest.mark.contract
def test_c_el_aviso_de_fidelidad_sale_tambien_cuando_se_ingiere_otro_mes(
    montaje: tuple[Path, dict[str, Path]], capsys: pytest.CaptureFixture[str]
) -> None:
    """Que no entran se dice siempre, no solo cuando se intenta meterlos."""
    repo, libros = montaje
    assert _ingerir(repo, libros["mayo"]) == 0
    assert "2 dias del camino de FIDELIDAD" in capsys.readouterr().err


@pytest.mark.contract
def test_un_libro_no_puede_declararse_de_dos_meses() -> None:
    """Un mismo sha en dos meses devolveria a deducir el mes de las filas."""
    doc = yaml.safe_load((REAL / KIT / "config.yaml").read_text(encoding="utf-8"))
    sha = "a" * 64
    doc["cobertura_material"] = {
        "2026-05": [{"desde": "2026-05-01", "hasta": "2026-05-31", "material_sha256": sha}],
        "2026-07": [{"desde": "2026-07-01", "hasta": "2026-07-31", "material_sha256": sha}],
    }
    with pytest.raises(KitError, match="Un libro es de UN mes"):
        config_desde_doc(doc, "c.yaml")
    doc["cobertura_material"] = {
        "2026-05": [{"desde": "2026-05-01", "hasta": "2026-05-31", "material_sha256": "XYZ"}]
    }
    with pytest.raises(KitError, match="no es un sha256"):
        config_desde_doc(doc, "c.yaml")


@pytest.mark.contract
def test_el_config_real_ata_mayo_por_su_sha_y_septiembre_no() -> None:
    """Los sha del config real son los del manifiesto del corpus, no unos copiados a mano.

    Septiembre llevo su sha desde el paso 1 de esta rama -lo pidio un brief escrito sin anticipar
    ADR-0039- y la guardia del cruce con `libros.yaml` lo cazo el mismo dia: su tramo se queda,
    sin sha, hasta que tenga su brief y su medida, los dos a la vez.

    Desde ADR-0042 (2026-09-23) abril y agosto llevan tambien el suyo: son material ya visto que
    entra por el reparto dev-visto, con su libro medido en `libros.yaml`. Septiembre sigue sin."""
    doc = yaml.safe_load((REAL / KIT / "config.yaml").read_text(encoding="utf-8"))
    config = config_desde_doc(doc, "config.yaml")
    materiales = config.materiales
    assert config.cobertura["2026-09"], "el tramo de septiembre se queda"
    manifiesto = yaml.safe_load(
        (REAL / "knowledge/corpus/manifest.yaml").read_text(encoding="utf-8")
    )
    por_sha = {f["sha256"]: f["ruta"] for f in manifiesto["ficheros"]}
    assert sorted(materiales.values()) == ["2026-04", "2026-05", "2026-08"]
    assert "2026-09" not in materiales.values(), "septiembre sin sha hasta su brief y su medida"
    for sha, mes in materiales.items():
        assert sha in por_sha, f"{mes}: su sha no esta en el manifiesto del corpus"
        assert por_sha[sha].endswith(".xlsx")


@pytest.mark.contract
def test_un_tramo_sin_sha_es_material_que_este_comando_no_lee(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Un tramo SIN `material_sha256` significa: «hay material de este mes, y `casos ingerir` no
    lo lee». Julio tiene dias `dev` en el kit y su libro esta en el corpus y DECLARADO en
    `libros.yaml`; aun asi, sin sha en su tramo, no se pide ni un dia suyo con ningun libro, y el
    mensaje lo dice nombrando el MES y sin fechas."""
    libros = _libros(tmp_path)
    repo = _repo(tmp_path, libros, ("mayo", "julio", "septiembre", "ajeno"), sin_sha=("2026-07",))
    assert _ingerir(repo, libros["julio"]) == 1
    assert _escritos(repo) == []
    err = capsys.readouterr().err
    assert "2026-07: hay material declarado y ningun libro atado por su sha" in err
    assert "2026-07-06" not in err and "2026-07-07" not in err
    # Con otro libro tampoco entra julio: mayo ingiere solo mayo, y el aviso se repite.
    assert _ingerir(repo, libros["mayo"]) == 0
    assert _escritos(repo) == ["caso-eurusd-2026-05-08", "caso-eurusd-2026-05-12"]
    assert "2026-07: hay material declarado" in capsys.readouterr().err
