"""El barrido ancho de dias (`scripts/barrido_dias.py`, rama `trabajo/cuarentena-por-condicion-2`),
sobre una filtrada SINTETICA en una carpeta temporal.

Ningun texto lleva una fecha real: los dias en rango van solos o con meses imposibles («del 13»), y
lo que se comprueba de la salida es que el numero no aparece nunca.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]

FILTRADA = """# Sesion · sintetica · version FILTRADA

## S-1

[01:02] el 25 del 13 entre
[01:10] y el veinticinco tambien
[02:00] el 5 del 13 no es del rango
[02:30] el precio a 1,25 y el stop
[03:00] hoy, 31,
[03:10] pregunta S25 sin dia
## S-25
[04:00] nada que ver
"""


@pytest.fixture(scope="module")
def b() -> ModuleType:
    nombre = "barrido_dias"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _salida(b: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str], *args: str) -> str:
    ruta = tmp_path / "x.filtrada.md"
    ruta.write_text(FILTRADA, encoding="utf-8")
    assert b.main([str(ruta), *args]) == 0
    return capsys.readouterr().out


def test_el_dia_en_digitos_y_en_letra_sale_con_el_numero_enmascarado(
    b: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    salida = _salida(b, tmp_path, capsys)
    lineas = salida.splitlines()
    assert "[01:02] el [N] del 13 entre" in lineas
    assert "[01:10] y el [N] tambien" in lineas  # «veinticinco», en letra
    assert "[03:00] hoy, [N]," in lineas  # pegado a una coma de puntuacion
    assert lineas[-1] == "lineas con un entero suelto de 18 a 31: 3"


def test_fuera_del_rango_un_precio_y_un_codigo_no_salen(
    b: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    salida = _salida(b, tmp_path, capsys)
    assert "[02:00]" not in salida  # el 5: fuera del rango
    assert "[02:30]" not in salida  # «1,25»: un decimal, no un dia
    assert "[03:10]" not in salida  # «S25»: un codigo pegado a una letra
    assert "[04:00]" not in salida and "## S-25" not in salida  # encabezados: no se barren


def test_la_salida_nunca_trae_el_numero(
    b: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    salida = _salida(b, tmp_path, capsys)
    cuerpo = "\n".join(salida.splitlines()[:-1])  # sin la linea del recuento
    assert not re.search(r"(?<!\d)(?:2[0-9]|3[01]|1[89])(?!\d)", cuerpo)
    assert "veinticinco" not in cuerpo


def test_el_rango_se_fija_por_argumento(
    b: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    salida = _salida(b, tmp_path, capsys, "--desde", "1", "--hasta", "9")
    assert "[02:00] el [N] del 13 no es del rango" in salida.splitlines()
    assert "[01:02]" not in salida


def test_roto_a_proposito_en_los_dos_sentidos(
    b: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    # (1) Sin pasar por `numeros_a_cifras` (como barrido_18_31.py), el dia en letra no sale.
    monkeypatch.setattr(b, "numeros_a_cifras", lambda t: t)
    assert "[01:10]" not in _salida(b, tmp_path, capsys)
    monkeypatch.undo()
    # (2) Sin la condicion del digito a cada lado, el precio «1,25» saldria como un dia.
    monkeypatch.setattr(b, "ENTERO", re.compile(r"(?<!\w)(\d{1,2})(?!\d)"))
    assert "[02:30] el precio a 1,[N] y el stop" in _salida(b, tmp_path, capsys).splitlines()
    monkeypatch.undo()
    # (3) Con el lookbehind de barrido_18_31.py (`(?<![\w.,])`), «hoy, 31,» saldria igual (hay
    # un espacio delante), pero «hoy,31» no: el hueco de la coma de puntuacion.
    viejo = re.compile(r"(?<![\w.,])(\d{1,2})(?![\d]|[.,]\d)")
    assert not viejo.search("hoy,31")
    assert b.ENTERO.search("hoy,31")
