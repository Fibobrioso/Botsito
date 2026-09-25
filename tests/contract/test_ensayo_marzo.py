"""EL ENSAYO DE MARZO, de punta a punta, sobre un repo SINTETICO (ADR-0046 §6, pasos a-e).

Es el runbook `docs/runbooks/ENTRADA-MARZO.md` ejecutado entero sin tocar nada real: la CLI de
verdad -`fidelidad build`, `fidelidad anclar`, `casos ingerir --artefacto`, `fidelidad check`-, la
herramienta del huso (`scripts/huso_por_velas.py`) y un libro sintetico con una CENTINELA en las
filas de los dias reservados. Lo que comprueba, en el orden en que pasa:

  a. el tramo de marzo esta declarado en `cobertura_material`, sin sha: todavia no hay libro;
  b. el sorteo reparte con los CUPOS DE LA REGLA real de 2026-03, solo dias de MARZO -el repo
     tiene tambien mayo cubierto-, y NO SE REPITE: ni con otra semilla ni borrando la carpeta;
  c. el huso sale de las VELAS con la herramienta, solo con filas `dev`, y la centinela no sale;
  d. el libro se declara y su sha se ata al tramo; la herramienta, ya como CONTROL, coincide;
  e. `casos ingerir --artefacto` escribe los `fidelidad-dev` y ni una fila reservada.

Las velas sinteticas cambian de precio CADA MINUTO, a proposito: con un precio plano todo el dia,
leer el instante en UTC o en Madrid daria la misma vela y la prueba del huso no distinguiria nada.
"""

from __future__ import annotations

import importlib.util
import lzma
import shutil
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.cases import fidelidad as fid
from botsito.corpus.libros import sha256_de
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie, congelar
from botsito.data.velas import a_minuto
from tests.contract.test_ingesta import _declarar, _xlsx
from tests.unit.test_kit import CONFIG_FIDELIDAD, HOY, REG, _repo_fidelidad

REAL = Path(__file__).resolve().parents[2]
ART = "xxxyyy-2026-03"
FORMATO = "AAAA-MM-DD HH:MM:SS"
CENTINELA = "CENTINELA-RESERVADA-no-debe-salir"
TRAMO = (
    '    - {desde: "2026-03-02", hasta: "2026-03-13", entregado_el: "2026-09-24",'
    " fuente: [ADR-0046]}"
)
BASE = 100000
PASO = 10  # puntos por minuto: una hora de desfase son 600 puntos, muy lejos del margen


def _precio(minuto_del_dia: int) -> int:
    return BASE + PASO * minuto_del_dia


def _descarga(url: str) -> bytes | None:
    partes = url.split("/")
    d = date(int(partes[-4]), int(partes[-3]) + 1, int(partes[-2]))
    if d.weekday() == 5:
        return None
    regs = [
        REG.pack(m * 60, _precio(m), _precio(m) + 1, _precio(m) - 1, _precio(m) + 2, 1.5)
        for m in range(1440)
    ]
    return lzma.compress(b"".join(regs))


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _cli(repo: Path, *args: str) -> int:
    return cli.main(["--repo", str(repo), *args])


@pytest.fixture(scope="module")
def huso() -> ModuleType:
    nombre = "huso_por_velas"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, REAL / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _regla_real() -> str:
    """La regla de cupos de 2026-03 TAL CUAL esta en el config real: la del consultor."""
    real = yaml.safe_load((REAL / fid.DIRECTORIO_FIDELIDAD / "config.yaml").read_text("utf-8"))
    return yaml.safe_dump({"cupos_por_mes": {"2026-03": real["cupos_por_mes"]["2026-03"]}})


def _formula(n: int) -> dict[str, int]:
    dev = n // 3
    f2 = (n - dev) // 2
    return {"fidelidad-dev": dev, "fidelidad-2": f2, "fidelidad-3": n - dev - f2, "fidelidad-1": 0}


def _montaje(tmp_path: Path) -> Path:
    """Paso a: el tramo de marzo declarado SIN sha -de la columna de fechas, antes del sorteo-."""
    config = CONFIG_FIDELIDAD.replace(
        "cobertura_material:\n", f'cobertura_material:\n  "2026-03":\n{TRAMO}\n'
    )
    assert config != CONFIG_FIDELIDAD
    repo = _repo_fidelidad(tmp_path, config + _regla_real())
    congelar(
        repo=repo,
        carpeta_datos=repo / "data",
        nombre="prueba-2026-03",
        simbolo="XXXYYY",
        escala=BASE,
        desde=date(2026, 3, 1),
        hasta=date(2026, 3, 14),
        descarga=_descarga,
        hoy=HOY,
    )
    corpus = repo / "knowledge" / "corpus"
    shutil.copy(REAL / "knowledge/corpus/criterio_huso.yaml", corpus / "criterio_huso.yaml")
    (corpus / "libros.yaml").write_text("libros: {}\n", encoding="utf-8")
    (corpus / "manifest.yaml").write_text("ficheros: []\n", encoding="utf-8")
    for args in (
        ("init", "-q", "-b", "trabajo"),
        ("config", "user.email", "t@t"),
        ("config", "user.name", "t"),
        ("config", "core.autocrlf", "false"),
        ("add", "-A"),
        ("commit", "-q", "-m", "a: tramo de marzo, sin libro"),
    ):
        _git(repo, *args)
    return repo


def _libro(ruta: Path, asignacion: dict[str, str]) -> None:
    """El libro de marzo: el huso VERDADERO es UTC. Dos operaciones por dia `dev`, con la entrada
    en el precio de la vela de ese minuto UTC; una fila CENTINELA por dia reservado."""
    filas = [["dateStart", "side", "entryPrice", "initialSL"]]
    for caso, particion in sorted(asignacion.items()):
        dia = caso.removeprefix("caso-xxxyyy-")
        if particion != "fidelidad-dev":
            filas.append([f"{dia} 09:00:00", CENTINELA, CENTINELA, CENTINELA])
            continue
        for hh, mm in ((8, 0), (11, 30)):
            p = _precio(60 * hh + mm)
            filas.append([f"{dia} {hh:02d}:{mm:02d}:00", "buy", f"{p / BASE:.5f}", "0.90000"])
    _xlsx(ruta, filas, con_agregado=False)


def _velas(repo: Path, huso: ModuleType) -> Any:
    """Las M1 del dataset sintetico, cargadas como las carga `main` de la herramienta."""
    s = cargar_serie(cargar_manifiesto(buscar_manifiesto(repo, "prueba-2026-03")), repo / "data")
    rangos = {int(v.inicio): huso.Rango(int(v.minima), int(v.maxima), s.escala) for v in s.velas}

    def vela_de(instante: datetime) -> Any:
        return rangos.get(int(a_minuto(instante)))

    return vela_de


def _sin_fuga(salida: str, repo: Path, reservados: list[str]) -> None:
    assert CENTINELA not in salida
    for dia in reservados:
        assert dia not in salida, f"la salida nombra el dia reservado {dia}"
    dev = repo / "knowledge" / "cases" / "dev"
    for f in dev.glob("*.yaml") if dev.is_dir() else []:
        assert CENTINELA not in f.read_text(encoding="utf-8"), f"{f.name} lleva la centinela"


@pytest.mark.contract
def test_ensayo_de_marzo_de_punta_a_punta(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], huso: ModuleType
) -> None:
    repo = _montaje(tmp_path)
    carpeta = repo / fid.DIRECTORIO_FIDELIDAD / ART

    # b. EL SORTEO, con la regla de cupos real y solo dias de marzo.
    assert _cli(repo, "fidelidad", "build", "--artefacto", ART, "--seed", "11") == 0
    particiones = yaml.safe_load((carpeta / "particiones.yaml").read_text(encoding="utf-8"))
    asignacion: dict[str, str] = particiones["asignacion"]
    n = len(asignacion)
    assert n == 10, "los laborables del 2 al 13 de marzo, y ninguno de mayo"
    assert all(c.startswith("caso-xxxyyy-2026-03-") for c in asignacion)
    assert (
        particiones["cupos"]
        == _formula(n)
        == {
            "fidelidad-dev": 3,
            "fidelidad-2": 3,
            "fidelidad-3": 4,
            "fidelidad-1": 0,
        }
    )
    assert _cli(repo, "fidelidad", "anclar", "--artefacto", ART) == 0
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "b: sorteo de marzo, anclado")
    dev = sorted(
        c.removeprefix("caso-xxxyyy-") for c, p in asignacion.items() if p == "fidelidad-dev"
    )
    reservados = sorted(c.removeprefix("caso-xxxyyy-") for c in asignacion if c[-10:] not in dev)
    capsys.readouterr()

    # b'. EL SORTEO NO SE REPITE: ni con otra semilla, ni borrando la carpeta commiteada.
    assert _cli(repo, "fidelidad", "build", "--artefacto", ART, "--seed", "12") == 1
    assert "ya existe" in capsys.readouterr().err
    shutil.rmtree(carpeta)
    assert _cli(repo, "fidelidad", "build", "--artefacto", ART, "--seed", "12") == 1
    assert "EL SORTEO NO SE REPITE NUNCA" in capsys.readouterr().err
    assert not carpeta.exists()
    _git(repo, "checkout", "--", ".")
    assert yaml.safe_load((carpeta / "particiones.yaml").read_text("utf-8")) == particiones

    # c. EL HUSO, por velas, con la herramienta: solo filas `dev`, la centinela no sale.
    libro = tmp_path / "marzo.xlsx"
    _libro(libro, asignacion)
    inf = huso.medir_libro(repo, libro, "2026-03", FORMATO, _velas(repo, huso))
    assert inf.dias == len(dev) == 3
    assert len(inf.comparables.filas) == 2 * len(dev)
    assert inf.cuenta == {"UTC": (6, 6, 0), "Europe/Madrid": (0, 6, 0)}
    assert (inf.veredicto, inf.declarado) == ("UTC", None)
    _sin_fuga("\n".join(huso.lineas(inf, huso.cargar_criterio(repo))), repo, reservados)

    # d. LA DECLARACION: el libro en libros.yaml y su sha atado al tramo de marzo.
    _declarar(repo, libro, formato=FORMATO, huso="UTC")
    sha = sha256_de(libro)
    config = repo / fid.DIRECTORIO_FIDELIDAD / "config.yaml"
    texto = config.read_text(encoding="utf-8")
    config.write_text(
        texto.replace(TRAMO, TRAMO[:-1] + f", material_sha256: {sha}}}"), encoding="utf-8"
    )
    manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
    manifiesto.write_text(
        yaml.safe_dump({"ficheros": [{"ruta": "marzo.xlsx", "sha256": sha}]}), encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "d: libro de marzo declarado")
    control = huso.medir_libro(repo, libro, "2026-03", None, _velas(repo, huso))
    assert (control.declarado, control.veredicto, control.coincide) == ("UTC", "UTC", True)

    # e. LA INGESTA de los `fidelidad-dev`, y ni una fila reservada.
    capsys.readouterr()
    args = ("casos", "ingerir", "--material", str(libro), "--fecha", "2026-09-24")
    assert _cli(repo, *args, "--artefacto", ART) == 0
    cap = capsys.readouterr()
    escritos = sorted(p.stem for p in (repo / "knowledge/cases/dev").glob("*.yaml"))
    assert escritos == [f"caso-xxxyyy-{d}" for d in dev]
    for d in dev:
        caso = yaml.safe_load((repo / f"knowledge/cases/dev/caso-xxxyyy-{d}.yaml").read_text())
        assert [o["sesion"] for o in caso["operaciones"]] == ["07-11", "11-15"]
    assert f"{len(dev)} casos escritos de {len(dev)} dias ingeribles" in cap.out
    _sin_fuga(cap.out + cap.err, repo, reservados)

    # Y el artefacto se sigue reproduciendo con lo que congelo.
    assert _cli(repo, "fidelidad", "check", "--artefacto", ART) == 0
    _sin_fuga(capsys.readouterr().out, repo, reservados)
