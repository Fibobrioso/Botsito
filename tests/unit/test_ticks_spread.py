"""La ventana de `scripts/ticks_spread.py` por la rejilla (ADR-0069 §5; `trabajo/entrada-enero`, X).

Hasta esa rama el guion leia cada tick en la hora de pared de `huso_operativa`. La rejilla H4 y
Madrid solo difieren los dias en que Europa y EE. UU. no han cambiado la hora a la vez (en 2026, del
9 al 27 de marzo y del 26 al 30 de octubre). Estos tests ROMPEN A PROPOSITO con uno de esos dias
(2026-10-27): el reloj de pared de antes da la hora corrida y el de la rejilla no; y comprueban que
en un dia sin desfase, de invierno y de verano, los dos dan lo mismo minuto a minuto. Con el
registro real: si un dia cambia `reloj_sesiones`, `anclaje_h4` o la ventana, estos tests lo dicen.
"""

from __future__ import annotations

import importlib.util
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.engine.relojes import RelojSesiones, reloj_de_las_sesiones

RAIZ = Path(__file__).resolve().parents[2]
SCRIPT = RAIZ / "scripts" / "ticks_spread.py"
MS_POR_MINUTO = 60_000


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "ticks_spread"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, SCRIPT)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _ventana(registro: Registro) -> tuple[int, int]:
    return (
        registro.hora("ventana_inicio").minutos_del_dia // 60,
        registro.hora("ventana_fin").minutos_del_dia // 60,
    )


def _ms(instante: datetime) -> int:
    return int(a_minuto(instante)) * MS_POR_MINUTO + 1_234  # un tick dentro del minuto


def _claves(m: ModuleType, reloj: RelojSesiones, registro: Registro, dia: datetime) -> list[str]:
    """La clave de un tick en cada hora UTC de 04:30 a 14:30 de `dia`."""
    inicio, fin = _ventana(registro)
    clave = m.clave_de_hora(reloj, inicio, fin)
    return [clave(_ms(dia.replace(hour=h, minute=30))) for h in range(4, 15)]


def test_el_registro_es_el_que_estos_tests_suponen(registro: Registro) -> None:
    """Si esto cae, los dias de abajo ya no son los que dicen ser: se rehacen, no se ajustan."""
    assert registro.opcion("reloj_sesiones") == "rejilla_h4"
    assert registro.texto("huso_operativa") == "Europe/Madrid"
    assert _ventana(registro) == (7, 15)


def test_un_dia_de_desfase_rompe_la_hora_de_pared_y_no_la_rejilla(
    m: ModuleType, registro: Registro
) -> None:
    """2026-10-27: Madrid ya esta en CET y Nueva York sigue en EDT. La rejilla abre la ventana a las
    05:00Z (las 07:00 nominales, ADR-0069 §1); la pared de Madrid marca a esa hora las 06:00."""
    dia = datetime(2026, 10, 27, tzinfo=UTC)
    rejilla = _claves(m, reloj_de_las_sesiones(registro), registro, dia)
    pared = _claves(m, RelojSesiones.de_pared(registro.texto("huso_operativa")), registro, dia)
    # de 04:30Z a 14:30Z, hora a hora
    assert rejilla == ["fuera", "07", "08", "09", "10", "11", "12", "13", "14", "fuera", "fuera"]
    assert pared == ["fuera", "fuera", "07", "08", "09", "10", "11", "12", "13", "14", "fuera"]
    assert rejilla != pared, "con huso_operativa la hora sale corrida una hora el dia de desfase"


def test_la_primera_hora_de_la_ventana_del_dia_de_desfase(
    m: ModuleType, registro: Registro
) -> None:
    """El mismo tick de las 05:30Z del 27 de octubre: dentro (07) por la rejilla, FUERA por la
    pared. Es la primera hora de la sesion, la que el trader opera."""
    inicio, fin = _ventana(registro)
    tick = _ms(datetime(2026, 10, 27, 5, 30, tzinfo=UTC))
    assert m.clave_de_hora(reloj_de_las_sesiones(registro), inicio, fin)(tick) == "07"
    pared = RelojSesiones.de_pared(registro.texto("huso_operativa"))
    assert m.clave_de_hora(pared, inicio, fin)(tick) == m.FUERA


@pytest.mark.parametrize(
    "dia",
    [datetime(2026, 1, 15, tzinfo=UTC), datetime(2026, 7, 15, tzinfo=UTC)],
    ids=["invierno", "verano"],
)
def test_sin_desfase_la_rejilla_y_la_pared_dan_lo_mismo_minuto_a_minuto(
    m: ModuleType, registro: Registro, dia: datetime
) -> None:
    """Enero (06:00-14:00Z) y julio (05:00-13:00Z): los meses de construccion no tienen ningun dia
    de desfase, asi que la cifra de los meses ya medidos no cambia por contar por la rejilla."""
    inicio, fin = _ventana(registro)
    rejilla = m.clave_de_hora(reloj_de_las_sesiones(registro), inicio, fin)
    pared = m.clave_de_hora(RelojSesiones.de_pared(registro.texto("huso_operativa")), inicio, fin)
    base = int(a_minuto(dia.replace(hour=3)))
    for minuto in range(base, base + 13 * 60):
        assert rejilla(minuto * MS_POR_MINUTO) == pared(minuto * MS_POR_MINUTO), minuto
    abre = m.clave_de_hora(reloj_de_las_sesiones(registro), inicio, fin)
    primera = 6 if dia.month == 1 else 5
    assert abre(_ms(dia.replace(hour=primera, minute=0))) == "07"
    assert abre(_ms(dia.replace(hour=primera - 1, minute=59))) == m.FUERA


def test_un_mes_de_construccion_sin_ticks_se_niega_nombrandolo(
    m: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Recorre `construccion` y EXIGE los ticks de cada mes: sin manifiesto, sale con 2 y nombra el
    mes, sin escribir la salida."""
    for rel in ("knowledge/cases/criterio_fidelidad.yaml", "knowledge/spec/parametros.yaml"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RAIZ / rel, tmp_path / rel)
    salida = tmp_path / "salida.txt"
    assert m.main(["--salida", str(salida)], raiz=tmp_path) == 2
    err = capsys.readouterr().err
    assert "2026-04 es de construccion y no tiene ticks" in err
    assert not salida.exists()


def test_el_guion_entero_cuenta_el_dia_de_desfase_por_la_rejilla(
    m: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`main` de punta a punta con tres ticks sinteticos del 2026-10-27: protege el RELOJ que elige
    el guion, no solo `clave_de_hora` (hallazgo b2 del revisor). Si `main` volviera a la pared de
    `huso_operativa`, el tick de las 05:30Z caeria fuera, el de las 12:30Z en la hora 13 y el de las
    13:30Z en la 14, y esto cae. Los manifiestos son ficheros vacios y la carga de ticks se
    sustituye: no se lee ningun dato."""
    import botsito.data.ticks as ticks

    for rel in ("knowledge/cases/criterio_fidelidad.yaml", "knowledge/spec/parametros.yaml"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RAIZ / rel, tmp_path / rel)
    carpeta = tmp_path / ticks.DIRECTORIO_MANIFIESTOS_TICKS
    carpeta.mkdir(parents=True)
    for mes in ("2026-04", "2026-07", "2026-08", "2026-01"):
        (carpeta / f"eurusd-ticks-{mes}-sintetico.yaml").write_text("", encoding="utf-8")
    dia = datetime(2026, 10, 27, tzinfo=UTC)
    del_dia = [
        SimpleNamespace(instante=_ms(dia.replace(hour=h, minute=30)), spread=s)
        for h, s in ((5, 9), (12, 2), (13, 1))
    ]

    def cargar(ruta: Path, _datos: Path) -> SimpleNamespace:
        uno = ruta.stem == "eurusd-ticks-2026-04-sintetico"
        return SimpleNamespace(origen=ruta.stem, ticks=del_dia if uno else [])

    monkeypatch.setattr(ticks, "cargar_manifiesto_ticks", lambda ruta: ruta)
    monkeypatch.setattr(ticks, "cargar_ticks", cargar)
    salida = tmp_path / "salida.txt"
    assert m.main(["--salida", str(salida)], raiz=tmp_path) == 0
    lineas = salida.read_text(encoding="utf-8").splitlines()
    del_mes = [x for x in lineas if x.startswith("2026-04 ")]
    assert del_mes == [
        "2026-04 07:00: n 1, media 9.00, p50 9, p90 9, p99 9, max 9",
        "2026-04 14:00: n 1, media 2.00, p50 2, p90 2, p99 2, max 2",
        "2026-04 fuera: n 1, media 1.00, p50 1, p90 1, p99 1, max 1",
    ]
    assert "(rejilla_h4, ADR-0069 §5)" in lineas[0]
