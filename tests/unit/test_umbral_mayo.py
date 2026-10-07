"""El umbral de construccion que habilita medir el conjunto de medida (ADR-0070), sin el arnes:
todo sintetico. La carga de los dos campos nuevos de `criterio_fidelidad.yaml` y, desde la fase 3,
la linea de veredicto que el arnes escribe al final de su seccion del criterio."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import (
    FICHERO_CRITERIO,
    Criterio,
    CriterioError,
    Operacion,
    Tolerancias,
    cargar_criterio,
    habilita_medir,
    medir,
)
from botsito.engine import arnes
from botsito.engine.motor import ResultadoDia

REPO = Path(__file__).resolve().parents[2]
CAMPOS = ("umbral_construccion_para_medir_cobertura", "umbral_construccion_para_medir_precision")


def _copia(tmp_path: Path, cambiar: dict[str, str | None]) -> Path:
    """El fichero real, con los campos de `cambiar` sustituidos (o quitados si el valor es None)."""
    lineas = []
    for linea in (REPO / FICHERO_CRITERIO).read_text(encoding="utf-8").splitlines():
        campo = linea.split(":", 1)[0]
        if campo in cambiar:
            if cambiar[campo] is not None:
                lineas.append(f"{campo}: {cambiar[campo]}")
            continue
        lineas.append(linea)
    ruta = tmp_path / FICHERO_CRITERIO
    ruta.parent.mkdir(parents=True)
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return tmp_path


def test_el_fichero_real_lleva_las_cifras_de_adr_0043_tambien_para_construccion() -> None:
    c = cargar_criterio(REPO)
    assert c.umbral_construccion_para_medir_cobertura == Fraction(7, 10)
    assert c.umbral_construccion_para_medir_precision == Fraction(6, 10)
    # las mismas que el umbral de medida (ADR-0070, decision 1)
    assert c.umbral_construccion_para_medir_cobertura == c.umbral_cobertura
    assert c.umbral_construccion_para_medir_precision == c.umbral_precision


@pytest.mark.parametrize("campo", CAMPOS)
def test_sin_el_campo_no_carga(tmp_path: Path, campo: str) -> None:
    with pytest.raises(CriterioError, match=campo):
        cargar_criterio(_copia(tmp_path, {campo: None}))


@pytest.mark.parametrize("campo", CAMPOS)
@pytest.mark.parametrize("valor", ['"1.5"', '"-0.1"', '"setenta"'])
def test_fuera_de_0_a_1_o_no_numerico_no_carga(tmp_path: Path, campo: str, valor: str) -> None:
    with pytest.raises(CriterioError, match=campo):
        cargar_criterio(_copia(tmp_path, {campo: valor}))


# --------------------------------------------------- fase 3: la linea de veredicto (ADR-0070)
# Corridas SINTETICAS: dias, operaciones del trader y del bot escritas a mano, sin motor ni velas.
# Cada test rompe una condicion a proposito y mira la linea que el arnes escribe.

CONSTRUCCION = ("2030-01", "2030-03")
CRITERIO = Criterio(
    Tolerancias(3, 15, 100_000),
    Fraction(7, 10),
    Fraction(6, 10),
    CONSTRUCCION,
    ("2030-02",),
    Fraction(7, 10),
    Fraction(6, 10),
)
VOCABULARIO: dict[str, dict[str, object]] = {"hechos": {}}
T0 = datetime(2030, 1, 7, 7, 30, tzinfo=UTC)


def _op(dia: str, k: int, desfase_min: int = 0) -> Operacion:
    return Operacion(
        dia, "07-11", "venta", T0 + timedelta(minutes=k * 60 + desfase_min), Decimal("1.10000")
    )


def _corrida(
    n_trader: int, n_iguales: int, n_bot_de_mas: int, meses: tuple[str, ...] = CONSTRUCCION
) -> arnes.Corrida:
    """Un dia con `n_trader` operaciones del trader; el bot repite `n_iguales` de ellas y pone
    `n_bot_de_mas` que no emparejan (dos horas despues de cualquiera del trader)."""
    dia = "2030-01-07"
    trader = tuple(_op(dia, k) for k in range(n_trader))
    bot = tuple(_op(dia, k) for k in range(n_iguales)) + tuple(
        _op(dia, k, desfase_min=120) for k in range(n_trader, n_trader + n_bot_de_mas)
    )
    return arnes.Corrida(
        "sintetico",
        meses,
        (arnes.DiaTrader("caso-sintetico", dia, trader),),
        (ResultadoDia(dia, bot, {}),),
    )


def _linea(corrida: arnes.Corrida, *, con_diagnostico: bool) -> str:
    texto = arnes.informe(corrida, CRITERIO, VOCABULARIO, con_diagnostico=con_diagnostico)
    lineas = [ln for ln in texto.splitlines() if ln.startswith("habilita medir")]
    assert len(lineas) == 1, lineas
    # al final de la seccion del criterio: la linea siguiente es la vacia que la cierra
    seccion = texto.split("## Criterio de fidelidad (ADR-0043)\n", 1)[1].split("\n\n", 1)[0]
    assert seccion.splitlines()[-1] == lineas[0]
    return lineas[0]


def test_llega_a_las_dos_sin_diagnostico_y_sobre_todo_el_conjunto_habilita() -> None:
    # 7/10 de cobertura y 7/11 de precision: justo en los umbrales o por encima
    linea = _linea(_corrida(10, 7, 4), con_diagnostico=False)
    assert linea == "habilita medir el conjunto de medida (2030-02) (ADR-0070): sí"


def test_falla_por_cobertura() -> None:
    linea = _linea(_corrida(10, 6, 0), con_diagnostico=False)  # 6/10 y 6/6
    assert linea.endswith(": no (cobertura 60.0 % por debajo de 70.0 %)")


def test_falla_por_precision() -> None:
    linea = _linea(_corrida(10, 8, 6), con_diagnostico=False)  # 8/10 y 8/14
    assert linea.endswith(": no (precision 57.1 % por debajo de 60.0 %)")


def test_una_metrica_sin_definir_no_llega() -> None:
    # el bot no pone ninguna: cobertura 0/3 y precision sin denominador
    linea = _linea(_corrida(3, 0, 0), con_diagnostico=False)
    assert "precision sin definir" in linea and linea.split(": ", 1)[1].startswith("no (")
    # y sin operaciones del trader, la cobertura tampoco esta definida
    sin_trader = arnes.Corrida("sintetico", CONSTRUCCION, (), ())
    assert "cobertura sin definir" in _linea(sin_trader, con_diagnostico=False)


def test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no() -> None:
    """D2 (ADR-0070): la misma corrida que habilita sin diagnostico, con diagnostico sale «no», y
    el unico motivo es el diagnostico. Si se quitara esa condicion, este test fallaria."""
    corrida = _corrida(10, 7, 4)
    assert _linea(corrida, con_diagnostico=False).endswith(": sí")
    linea = _linea(corrida, con_diagnostico=True)
    assert linea.endswith(
        ": no (corrida con diagnostico: solo cuenta una corrida sin --diagnostico-*)"
    )


def test_una_corrida_sobre_parte_de_construccion_no_habilita() -> None:
    linea = _linea(_corrida(10, 7, 4, meses=("2030-01",)), con_diagnostico=False)
    assert linea.endswith(
        ": no (la corrida no cubre todo el conjunto de construccion (falta 2030-03))"
    )


def test_los_motivos_se_suman() -> None:
    v = habilita_medir(
        medir([], [], CRITERIO.tolerancias), CRITERIO, ("2030-01",), con_diagnostico=True
    )
    assert not v.habilita
    assert len(v.motivos) == 4  # diagnostico, conjunto incompleto, cobertura y precision


def test_el_informe_exige_decir_si_hay_diagnostico() -> None:
    """Sin el argumento, `informe` no se puede llamar: ningun llamador puede olvidarlo y dejar el
    veredicto en «sin diagnostico» por defecto."""
    with pytest.raises(TypeError, match="con_diagnostico"):
        arnes.informe(_corrida(1, 1, 0), CRITERIO, VOCABULARIO)  # type: ignore[call-arg]


def test_el_comando_pasa_al_informe_si_la_corrida_lleva_diagnostico() -> None:
    """El comando `motor arnes` le pasa a `informe` `diag.activo`, no una constante: si alguien lo
    cambiara a `False`, toda corrida con diagnostico diria «sí» (revisor de esta rama, a2).
    Se lee el codigo, sin ejecutar el comando: en esta rama el arnes no se corre."""
    import ast

    fuente = (REPO / "src" / "botsito" / "cli.py").read_text(encoding="utf-8")
    llamadas = [
        n
        for n in ast.walk(ast.parse(fuente))
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "informe"
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == "arnes"
    ]
    assert len(llamadas) == 1, "el comando llama a arnes.informe una sola vez"
    argumento = next(k.value for k in llamadas[0].keywords if k.arg == "con_diagnostico")
    assert ast.unparse(argumento) == "diag.activo"
