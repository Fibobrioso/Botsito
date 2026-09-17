"""La guarda del holdout se ve saltar (F14 criterio 3, extraido; ADR-0033).

Una guarda que nunca ha fallado no es una guarda: las tres de `DECIDIDA` corrieron sobre el
repositorio real sin que nadie comprobara que saltaban, y `comprobar_citas_revocadas` nacio corta
cuatro veces. Aqui se provoca cada lectura prohibida -contra un holdout SINTETICO en `tmp_path`,
o contra una ruta que no existe en el real- y se comprueba que falla; y cada lectura legitima,
que pasa.
Nunca se crea ni se lee un fichero de verdad dentro de `knowledge/cases/holdout/{1,2,3}/`.
"""

from __future__ import annotations

import contextlib
import io
import os
import shutil
from collections.abc import Callable, Iterator
from pathlib import Path

import pytest

from tests import guarda_holdout
from tests.conftest import RAIZ_HOLDOUT


def test_la_guarda_esta_instalada_y_encendida_sobre_el_holdout_real() -> None:
    assert guarda_holdout.esta_instalado()
    assert guarda_holdout.Estado.raiz == RAIZ_HOLDOUT


@pytest.mark.provoca_holdout
def test_salta_con_una_ruta_del_holdout_real_antes_de_abrir_nada() -> None:
    """El evento `open` se audita ANTES de abrir: la guarda salta aunque el fichero no exista, asi
    que se comprueba sobre el holdout real sin crear nada en el."""
    falso = RAIZ_HOLDOUT / "1" / "caso-que-no-existe.yaml"
    assert not falso.exists()
    with pytest.raises(guarda_holdout.LecturaDeHoldout, match="1/caso-que-no-existe.yaml"):
        falso.read_text(encoding="utf-8")
    assert guarda_holdout.Estado.violaciones


def test_las_lecturas_legitimas_pasan() -> None:
    # el README de cada particion y el de la carpeta
    for carpeta in ("1", "2", "3"):
        assert (RAIZ_HOLDOUT / carpeta / "README.md").read_text(encoding="utf-8")
        # listar nombres no es abrir
        assert "README.md" in os.listdir(RAIZ_HOLDOUT / carpeta)
    assert (RAIZ_HOLDOUT / "README.md").read_text(encoding="utf-8")
    # la ASIGNACION de dias a particion no es material de holdout
    kit = RAIZ_HOLDOUT.parent / "kit" / "2026-09-09-sesion-01" / "particiones.yaml"
    assert "holdout-1" in kit.read_text(encoding="utf-8")
    assert guarda_holdout.Estado.violaciones == []


@pytest.fixture
def holdout_sintetico(tmp_path: Path) -> Iterator[Path]:
    raiz = tmp_path / "knowledge" / "cases" / "holdout"
    (raiz / "2").mkdir(parents=True)
    caso = raiz / "2" / "caso-xxxyyy-2026-05-07.yaml"
    caso.write_text("etiqueta: secreta\n", encoding="utf-8")  # escrito ANTES de encender
    (raiz / "2" / "README.md").write_text("# 2\n", encoding="utf-8")
    real = guarda_holdout.Estado.raiz
    guarda_holdout.Estado.raiz = raiz
    try:
        yield caso
    finally:
        guarda_holdout.Estado.raiz = real


_LECTURAS: dict[str, Callable[[Path, Path], object]] = {
    "read_text": lambda f, _t: f.read_text(encoding="utf-8"),
    "read_bytes": lambda f, _t: f.read_bytes(),
    "open": lambda f, _t: open(f, encoding="utf-8").read(),  # noqa: SIM115
    "os.open": lambda f, _t: os.open(f, os.O_RDONLY),
    "io.FileIO": lambda f, _t: io.FileIO(f).read(),
    "shutil.copy2": lambda f, t: shutil.copy2(f, t / "copia.yaml"),
    "shutil.copyfile": lambda f, t: shutil.copyfile(f, t / "copia.yaml"),
}


@pytest.mark.provoca_holdout
@pytest.mark.parametrize("via", sorted(_LECTURAS))
def test_salta_por_cada_via_de_lectura(via: str, holdout_sintetico: Path, tmp_path: Path) -> None:
    with pytest.raises(guarda_holdout.LecturaDeHoldout):
        _LECTURAS[via](holdout_sintetico, tmp_path)
    assert any("2/caso-xxxyyy-2026-05-07.yaml" in v for v in guarda_holdout.Estado.violaciones)


@pytest.mark.provoca_holdout
def test_tragarse_la_excepcion_no_la_apaga(holdout_sintetico: Path) -> None:
    """Es `BaseException`: `except Exception` y `except OSError` no la tocan, y aunque un test la
    trague a proposito queda anotada, y la fixture falla al terminar si el test no esta marcado."""
    with pytest.raises(guarda_holdout.LecturaDeHoldout):
        try:
            holdout_sintetico.read_text(encoding="utf-8")
        except Exception:  # noqa: BLE001 - es justo lo que se prueba que NO la traga
            pytest.fail("la guarda se trago con except Exception")
    guarda_holdout.Estado.violaciones.clear()
    with contextlib.suppress(BaseException):
        holdout_sintetico.read_text(encoding="utf-8")
    assert guarda_holdout.Estado.violaciones, "la violacion tiene que quedar anotada"


def test_en_el_sintetico_tambien_pasan_el_readme_y_listar(holdout_sintetico: Path) -> None:
    carpeta = holdout_sintetico.parent
    assert (carpeta / "README.md").read_text(encoding="utf-8") == "# 2\n"
    assert holdout_sintetico.name in os.listdir(carpeta)
    assert guarda_holdout.Estado.violaciones == []


@pytest.mark.parametrize(
    ("ruta", "salta"),
    [
        ("1/caso.yaml", True),
        ("3/sub/dir/caso.json", True),
        ("2/README.md", False),
        ("README.md", False),
        ("4/caso.yaml", False),
        ("../kit/particiones.yaml", False),
    ],
)
def test_la_regla_pura(ruta: str, salta: bool, tmp_path: Path) -> None:
    raiz = tmp_path / "holdout"
    v = guarda_holdout.violacion("open", (str(raiz / ruta), "r", 0), raiz)
    assert (v is not None) is salta, (ruta, v)
    assert guarda_holdout.violacion("os.listdir", (str(raiz / "1"),), raiz) is None
