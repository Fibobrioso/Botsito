"""La memoria sin `tracemalloc` (rama `trabajo/memoria-suite`): el pico del proceso que da el
sistema, `motor arnes` que solo rastrea con `--tracemalloc`, y el medidor de `make check`
(`scripts/pico_memoria.py`), que se prueba en subprocesos: en Windows mete en un Job Object al
proceso que lo llama, y ese no puede ser el de pytest."""

from __future__ import annotations

import re
import subprocess
import sys
import tracemalloc
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "pico_memoria.py"
MIB = 2**20
# un hijo que toca cada pagina de 64 MiB, para que cuenten como residentes y comprometidas
RESERVA = "b = bytearray(64 * 2**20); b[::4096] = b'x' * len(b[::4096])"


def test_el_pico_del_proceso_sube_con_una_reserva_y_no_baja_al_soltarla() -> None:
    # en un proceso nuevo: el de pytest ya puede haber tenido un pico mayor que la reserva
    codigo = (
        "from botsito.comun.memoria import pico_del_proceso as p\n"
        f"antes = p()\n{RESERVA}\ndel b\ndespues = p()\nprint(antes, despues, p())\n"
    )
    r = subprocess.run(
        [sys.executable, "-c", codigo], capture_output=True, encoding="utf-8", check=True
    )
    antes, despues, final = (int(x) for x in r.stdout.split())
    assert antes > 0 and despues - antes >= 60 * MIB, r.stdout
    assert final >= despues


def _arnes_que_se_niega(tmp_path: Path, *extra: str) -> list[str]:
    # mayo no es de construccion: la compuerta para la corrida antes de leer nada
    return ["--repo", str(RAIZ), "motor", "arnes", "--meses", "2026-05",
            "--salida", str(tmp_path / "informe.txt"), *extra]  # fmt: skip


@pytest.mark.parametrize(("extra", "rastrea"), [((), False), (("--tracemalloc",), True)])
def test_motor_arnes_solo_rastrea_con_tracemalloc_si_se_pide(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, extra: tuple[str, ...], rastrea: bool
) -> None:
    from botsito import cli

    llamadas: list[str] = []
    original = tracemalloc.start

    def start(nframe: int = 1) -> None:
        llamadas.append("start")
        original(nframe)

    monkeypatch.setattr(tracemalloc, "start", start)
    assert cli.main(_arnes_que_se_niega(tmp_path, *extra)) == 2
    assert (llamadas == ["start"]) is rastrea
    assert not tracemalloc.is_tracing()


def _script(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=cwd,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )


def _mib(texto: str) -> int:
    m = re.search(r"(\d+) MiB", texto)
    assert m is not None, texto
    return int(m.group(1))


def test_ejecutar_mide_el_pico_de_un_hijo_y_devuelve_su_codigo(tmp_path: Path) -> None:
    hijo = [sys.executable, "-c", RESERVA + "; raise SystemExit(3)"]
    r = _script("ejecutar", "--", *hijo, cwd=tmp_path)
    assert r.returncode == 3, r.stderr
    assert _mib(r.stdout) >= 64, r.stdout


def test_medir_apunta_cada_paso_y_el_informe_da_el_mayor_y_limpia(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    assert _script("empezar", cwd=tmp_path).returncode == 0
    ligero = _script("medir", "ligero", "--", sys.executable, "-c", "pass", cwd=tmp_path)
    pesado = _script("medir", "pesado", "--", sys.executable, "-c", RESERVA, cwd=tmp_path)
    assert ligero.returncode == 0 and pesado.returncode == 0, ligero.stderr + pesado.stderr
    informe = _script("informe", cwd=tmp_path)
    linea = informe.stdout.strip()
    assert linea.startswith("PICO DE MEMORIA de make check: ") and "en `pesado`" in linea, linea
    assert _mib(linea) >= 64
    # el acumulador se consume: un segundo informe no tiene medidas
    assert "sin medida" in _script("informe", cwd=tmp_path).stdout


def test_medir_devuelve_el_codigo_del_paso(tmp_path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    r = _script("medir", "rojo", "--", sys.executable, "-c", "raise SystemExit(2)", cwd=tmp_path)
    assert r.returncode == 2


def test_make_check_mide_cada_paso_e_informa_al_final() -> None:
    real = (RAIZ / "Makefile").read_text(encoding="utf-8")
    recetas = re.findall(r"^(\w+):[^\n]*\n((?:\t[^\n]*\n)+)", real, re.M)
    por_objetivo = dict(recetas)
    linea = next(x for x in real.splitlines() if x.startswith("check:"))
    for paso in linea.split(":", 1)[1].split():
        ordenes = [x for x in por_objetivo[paso].splitlines() if "$(PICO) empezar" not in x]
        assert ordenes and all(x.startswith("\t$(MEDIR) ") for x in ordenes), (paso, ordenes)
    # el acumulador se vacia al empezar, y el informe es la receta de `check`: corre tras `sellar`
    assert por_objetivo["desellar"].startswith("\t$(PICO) empezar\n")
    assert por_objetivo["check"] == "\t@$(PICO) informe\n"
