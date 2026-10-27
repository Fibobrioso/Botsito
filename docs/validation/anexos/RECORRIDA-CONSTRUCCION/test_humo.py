"""Tests de humo de los guiones de esta carpeta, sobre salidas SINTETICAS y en los dos sentidos
(RECORRIDA-CONSTRUCCION, fase 1). No los recoge `make check` (`testpaths = ["tests"]`):

    uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION/test_humo.py -q
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import entradas_antes_alternancia as eaa  # noqa: E402
import patrones  # noqa: E402

PATRONES_VIEJO = AQUI.parent / "CORRIDA-CONSTRUCCION" / "patrones.py"
ROTULO = "[DIAGNOSTICO-CUENTA-diaria] "
POR_SESION = (
    "2026-04-01 07-11 | trader 1 | bot 0 | rn003 alcista | sesgo:si "
    "orden_dimensionada:no[productoras sin cumplirse] | disparadas RN-003 | bloqueadas ninguna"
)
TRADER = (
    "trader | 2026-04-01 | 07-11 | compra | 2026-04-01T08:00:00+00:00 | 1.10000 | SIN PAREJA; "
    "ninguna operacion del bot en la sesion; primer hecho que falto: liquidez_tomada[x]"
)


def _cargar(ruta: Path, nombre: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _llenada(zonas: int, reubicaciones: int = 0, donde: str = eaa.PRIMERO) -> eaa.Llenada:
    return eaa.Llenada(
        "2026-04-01", "07-11", "o-1", "compra", "2026-04-01T08:00:00+00:00", "1.10000",
        zonas, zonas, donde, "110000@29580000", reubicaciones, "n 1", "+3.00 (objetivo)",
        "P6 donde el trader no opero",
    )  # fmt: skip


# ------------------------------------------------------------- la lista, en los dos sentidos


def test_entra_con_cero_o_una_zona_y_no_con_dos_o_mas() -> None:
    assert eaa.en_la_lista(_llenada(0))
    assert eaa.en_la_lista(_llenada(1))
    assert not eaa.en_la_lista(_llenada(2))
    assert not eaa.en_la_lista(_llenada(3))


def test_la_columna_de_zonas_dice_cuantas_habia() -> None:
    assert eaa.fila_texto(_llenada(0)).split(" | ")[6] == "0"
    assert eaa.fila_texto(_llenada(1)).split(" | ")[6] == "1"


def test_una_reubicada_sale_como_reubicada_y_una_no_reubicada_no() -> None:
    assert eaa.fila_texto(_llenada(0, reubicaciones=1)).split(" | ")[10] == "1"
    assert eaa.fila_texto(_llenada(0, reubicaciones=0)).split(" | ")[10] == "0"


def test_donde_esta_referencia_primero_y_posterior() -> None:
    toma = 1000  # el cierre de la toma, en minutos
    assert eaa.donde_esta(990, toma, [1003, 1010]) == eaa.REFERENCIA
    assert eaa.donde_esta(1003, toma, [1003, 1010]) == eaa.PRIMERO
    assert eaa.donde_esta(1010, toma, [1003, 1010]) == eaa.POSTERIOR
    # el cierre de la toma cuenta ya como "tras la toma"
    assert eaa.donde_esta(1000, toma, [1000]) == eaa.PRIMERO


def test_reubicaciones_solo_cuenta_las_anteriores_canceladas_por_rn006() -> None:
    ordenes = {"o-1": 100, "o-2": 200, "o-3": 300}
    cancelaciones = [
        (150, "o-1", "reglas disparadas en ese cierre: RN-006, RN-011, RN-015"),
        (250, "o-2", "en ventana_fin; reglas disparadas en ese cierre: RN-035"),
    ]
    assert eaa.reubicaciones_antes(300, ordenes, cancelaciones) == 1  # o-1 si, o-2 no
    assert eaa.reubicaciones_antes(100, ordenes, cancelaciones) == 0  # ninguna anterior
    cancelaciones.append((350, "o-3", "reglas disparadas en ese cierre: RN-006"))
    assert eaa.reubicaciones_antes(200, ordenes, cancelaciones) == 1  # o-3 es posterior: no


def test_llenadas_de_ordenes_lee_solo_las_llenadas_con_y_sin_rotulo() -> None:
    fila_ll = "2026-04-01 | 07-11 | o-1 | 2026-04-01T07:59:59+00:00 | 1.10000 | llenada | - | x"
    fila_ca = "2026-04-01 | 07-11 | o-2 | 2026-04-01T08:30:59+00:00 | 1.10100 | cancelada | m | x"
    cuerpo = ["### Ordenes (dia | ...)", fila_ll, fila_ca, "ordenes: llenada 1, cancelada 1"]
    assert eaa.llenadas_de_ordenes(cuerpo) == [fila_ll]
    assert eaa.llenadas_de_ordenes([ROTULO + ln for ln in cuerpo]) == [fila_ll]
    assert eaa.llenadas_de_ordenes(["### Ordenes (x)", "ordenes: 0"]) == []


# ---------------------------------------------- patrones.py: con rotulo y sin el, frente al viejo


def _clasifica(modulo: ModuleType, ruta: Path) -> tuple[int, list[str]]:
    filas, sesgo = modulo.leer(ruta)
    return len(sesgo), [p for p, *_ in modulo.clasificar(filas, sesgo)]


def test_la_copia_lee_el_sesgo_con_rotulo_y_sin_el(tmp_path: Path) -> None:
    con = tmp_path / "con.txt"
    sin = tmp_path / "sin.txt"
    con.write_text(f"{ROTULO}{POR_SESION}\n{ROTULO}{TRADER}\n", encoding="utf-8")
    sin.write_text(f"{POR_SESION}\n{TRADER}\n", encoding="utf-8")
    assert _clasifica(patrones, con) == (1, ["P4 sin orden"])
    assert _clasifica(patrones, sin) == (1, ["P4 sin orden"])


def test_la_lectura_vieja_rompe_sin_rotulo(tmp_path: Path) -> None:
    """El guion de R3.1 cortaba por el primer «] »: sin rotulo pierde el sesgo y da un P1 falso."""
    viejo = _cargar(PATRONES_VIEJO, "patrones_viejo")
    con = tmp_path / "con.txt"
    sin = tmp_path / "sin.txt"
    con.write_text(f"{ROTULO}{POR_SESION}\n{ROTULO}{TRADER}\n", encoding="utf-8")
    sin.write_text(f"{POR_SESION}\n{TRADER}\n", encoding="utf-8")
    assert _clasifica(viejo, con) == (1, ["P4 sin orden"])
    assert _clasifica(viejo, sin) == (0, ["P1 sesgo"])


def test_la_copia_solo_corta_el_rotulo_de_diagnostico() -> None:
    assert patrones._cuerpo(ROTULO + POR_SESION) == POR_SESION
    assert patrones._cuerpo(POR_SESION) == POR_SESION
    assert patrones._cuerpo("[otra cosa] texto") == "[otra cosa] texto"
