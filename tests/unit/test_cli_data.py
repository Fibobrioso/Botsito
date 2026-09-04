"""CLI `data download|check|aggregate` en un repositorio temporal con descarga simulada."""

import lzma
import struct
from pathlib import Path

import pytest

from botsito import cli
from botsito.data import dukascopy
from botsito.data.velas import leer_csv

REG = struct.Struct(">iiiiif")


def bi5_dia(precio: int) -> bytes:
    regs = [REG.pack(m * 60, precio, precio + 1, precio - 1, precio + 2, 1.5) for m in range(1440)]
    return lzma.compress(b"".join(regs))


def _repo(tmp_path: Path) -> Path:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.example.toml").write_text(
        '[entorno]\nnombre = "backtest"\n\n'
        '[rutas]\ncorpus = "c"\ndata = "datos"\nknowledge = "k"\n',
        encoding="utf-8",
    )
    return tmp_path


def _descarga_falsa(url: str) -> bytes | None:
    dia = int(url.split("/")[-2])
    return None if dia == 4 else bi5_dia(100000 + dia)


def test_download_check_aggregate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    repo = _repo(tmp_path)
    monkeypatch.setattr(dukascopy, "descarga_http", _descarga_falsa)
    base = ["--repo", str(repo), "data"]
    args = base + [
        "download",
        "--dataset",
        "prueba",
        "--simbolo",
        "XXXYYY",
        "--escala",
        "100000",
        "--desde",
        "2026-01-01",
        "--hasta",
        "2026-01-06",
    ]
    assert cli.main(args) == 0
    salida = capsys.readouterr().out
    assert "OK: data/manifests/prueba-" in salida and "Fuente: ADR-0005" in salida
    manifiestos = list((repo / "data" / "manifests").glob("prueba-*.yaml"))
    assert len(manifiestos) == 1
    assert (repo / "datos" / "ohlc" / manifiestos[0].stem / "XXXYYY_M1_2026-01.csv").exists()
    # Mismo contenido: no se congela dos veces.
    assert cli.main(args) == 1
    assert cli.main(base + ["check", "--dataset", "prueba", "--hashes"]) == 0
    assert cli.main(base + ["check", "--dataset", "nada"]) == 1
    salida_csv = repo / "h4.csv"
    assert (
        cli.main(
            base
            + [
                "aggregate",
                "--dataset",
                "prueba",
                "--periodo",
                "240",
                "--anclaje",
                "00:00 UTC",
                "--desde",
                "2026-01-02",
                "--hasta",
                "2026-01-02",
                "--salida",
                str(salida_csv),
            ]
        )
        == 0
    )
    velas = leer_csv(salida_csv.read_text(encoding="utf-8"))
    assert len(velas) == 6 and all(v.duracion_min == 240 and v.completa for v in velas)
    assert velas[0].abierta == 100002 and velas[0].n_m1 == 240
    # Sin --salida escribe CSV en stdout; la ultima vela del rango no esta cerrada y se omite.
    capsys.readouterr()
    assert (
        cli.main(
            base + ["aggregate", "--dataset", "prueba", "--periodo", "60", "--anclaje", "00:30 UTC"]
        )
        == 0
    )
    capturado = capsys.readouterr()
    assert capturado.out.startswith("# dataset=prueba-")
    assert "ts_utc,abierta,maxima,minima,cierre,volumen,duracion_min" in capturado.out
    assert "sin cerrar omitidas" in capturado.err
    # --incluir-incompletas conserva el borde; --salida crea la carpeta; desde > hasta falla.
    destino = repo / "sub" / "dir" / "h1.csv"
    assert (
        cli.main(
            base
            + ["aggregate", "--dataset", "prueba", "--periodo", "60", "--anclaje", "00:30 UTC"]
            + ["--incluir-incompletas", "--salida", str(destino)]
        )
        == 0
    )
    assert not leer_csv(destino.read_bytes().decode("utf-8"))[-1].completa
    assert (
        cli.main(
            base
            + ["aggregate", "--dataset", "prueba", "--periodo", "60", "--anclaje", "00:00 UTC"]
            + ["--desde", "2026-01-03", "--hasta", "2026-01-02"]
        )
        == 1
    )


def test_stdout_redirigido_no_lleva_crlf(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """En Windows `sys.stdout` traduce LF a CRLF: el CSV de `aggregate` debe salir con LF."""
    import subprocess
    import sys

    repo = _repo(tmp_path)
    monkeypatch.setattr(dukascopy, "descarga_http", _descarga_falsa)
    assert (
        cli.main(
            [
                "--repo",
                str(repo),
                "data",
                "download",
                "--dataset",
                "pp",
                "--simbolo",
                "XXXYYY",
                "--escala",
                "1",
                "--desde",
                "2026-01-01",
                "--hasta",
                "2026-01-02",
            ]
        )
        == 0
    )
    salida = tmp_path / "out.csv"
    with salida.open("wb") as f:
        rc = subprocess.run(
            [
                sys.executable,
                "-c",
                "from botsito.cli import main; import sys; sys.exit(main(sys.argv[1:]))",
                "--repo",
                str(repo),
                "data",
                "aggregate",
                "--dataset",
                "pp",
                "--periodo",
                "240",
                "--anclaje",
                "00:00 UTC",
            ],
            stdout=f,
            stderr=subprocess.DEVNULL,
            check=False,
        ).returncode
    assert rc == 0
    assert b"\r" not in salida.read_bytes()
    assert leer_csv(salida.read_bytes().decode("utf-8"))


def test_download_rechaza_fechas_y_repo_malos(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    base = ["--repo", str(repo), "data", "download", "--dataset", "p", "--simbolo", "XXXYYY"]
    assert cli.main(base + ["--escala", "1", "--desde", "2026-13-01", "--hasta", "2026-01-02"]) == 1
    assert cli.main(base + ["--escala", "1", "--desde", "2026-01-01", "--hasta", "2999-01-01"]) == 1
    assert (
        cli.main(
            [
                "--repo",
                str(tmp_path / "nada"),
                "data",
                "download",
                "--dataset",
                "p",
                "--simbolo",
                "X",
                "--escala",
                "1",
                "--desde",
                "2026-01-01",
                "--hasta",
                "2026-01-02",
            ]
        )
        == 2
    )


def test_aggregate_anclaje_invalido(tmp_path: Path) -> None:
    """El formato lo rechaza el CLI (SystemExit); un anclaje bien formado sobre un dataset
    inexistente devuelve 1 por el dataset, no por el anclaje."""
    repo = _repo(tmp_path)
    with pytest.raises(SystemExit, match="anclaje"):
        cli.main(
            [
                "--repo",
                str(repo),
                "data",
                "aggregate",
                "--dataset",
                "p",
                "--periodo",
                "240",
                "--anclaje",
                "mediodia",
            ]
        )
    assert (
        cli.main(
            [
                "--repo",
                str(repo),
                "data",
                "aggregate",
                "--dataset",
                "p",
                "--periodo",
                "240",
                "--anclaje",
                "00:00 UTC",
            ]
        )
        == 1
    )
