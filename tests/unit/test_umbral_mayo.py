"""El umbral de construccion que habilita medir el conjunto de medida (ADR-0070), sin el arnes:
todo sintetico. La carga de los dos campos nuevos de `criterio_fidelidad.yaml` y, desde la fase 3,
la linea de veredicto que el arnes escribe al final de su seccion del criterio."""

from __future__ import annotations

import argparse
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
from botsito.cli import build_parser, opciones_de_la_corrida
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
# Cada test rompe una condicion a proposito y mira la linea que el arnes escribe. Las opciones de
# una corrida se obtienen PARSEANDO los argumentos con el parser real: el comando no se ejecuta.

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


def _parsear(*argv: str, parser: argparse.ArgumentParser | None = None) -> tuple[str, ...]:
    """Las opciones que una corrida de `motor arnes` con estos argumentos daria al informe: solo
    se PARSEAN, el comando no se ejecuta. Con `parser`, el de `build_parser()` ya modificado."""
    p = parser or build_parser()
    args = p.parse_args(["motor", "arnes", "--salida", "x.txt", *argv])
    return opciones_de_la_corrida((args.parser_raiz, args.parser_de_la_corrida), args)


def _linea(corrida: arnes.Corrida, opciones: tuple[str, ...] = ("--salida",)) -> str:
    texto = arnes.informe(corrida, CRITERIO, VOCABULARIO, opciones=opciones)
    lineas = [ln for ln in texto.splitlines() if ln.startswith("habilita medir")]
    assert len(lineas) == 1, lineas
    # al final de la seccion del criterio: la linea siguiente es la vacia que la cierra
    seccion = texto.split("## Criterio de fidelidad (ADR-0043)\n", 1)[1].split("\n\n", 1)[0]
    assert seccion.splitlines()[-1] == lineas[0]
    return lineas[0]


def test_llega_a_las_dos_sin_diagnostico_y_sobre_todo_el_conjunto_habilita() -> None:
    # 7/10 de cobertura y 7/11 de precision: justo en los umbrales o por encima
    linea = _linea(_corrida(10, 7, 4))
    assert linea == "habilita medir el conjunto de medida (2030-02) (ADR-0070): sí"


def test_falla_por_cobertura() -> None:
    linea = _linea(_corrida(10, 6, 0))  # 6/10 y 6/6
    assert linea.endswith(": no (cobertura 60.0 % por debajo de 70.0 %)")


def test_falla_por_precision() -> None:
    linea = _linea(_corrida(10, 8, 6))  # 8/10 y 8/14
    assert linea.endswith(": no (precision 57.1 % por debajo de 60.0 %)")


def test_una_metrica_sin_definir_no_llega() -> None:
    # el bot no pone ninguna: cobertura 0/3 y precision sin denominador
    linea = _linea(_corrida(3, 0, 0))
    assert "precision sin definir" in linea and linea.split(": ", 1)[1].startswith("no (")
    # y sin operaciones del trader, la cobertura tampoco esta definida
    sin_trader = arnes.Corrida("sintetico", CONSTRUCCION, (), ())
    assert "cobertura sin definir" in _linea(sin_trader)


def test_una_corrida_con_diagnostico_que_llega_a_las_dos_sale_no() -> None:
    """D2 (ADR-0070): la misma corrida que habilita con las opciones de la lista, con una opcion de
    diagnostico sale «no», y el unico motivo es esa opcion. Si se quitara la condicion, este test
    fallaria (anexo sin_d2.py)."""
    corrida = _corrida(10, 7, 4)
    assert _linea(corrida, _parsear()).endswith(": sí")
    linea = _linea(corrida, _parsear("--diagnostico-a35", "cierre_vela_contraria"))
    assert linea.endswith(": no (opción fuera de la lista: --diagnostico-a35)")


def test_depuracion_da_no() -> None:
    """--depuracion (y el --simular que exige) estan fuera de la lista: «no», con los dos."""
    opciones = _parsear("--simular", "--depuracion")
    assert opciones == ("--depuracion", "--salida", "--simular")
    linea = _linea(_corrida(10, 7, 4), opciones)
    assert linea.endswith(
        ": no (opción fuera de la lista: --depuracion; opción fuera de la lista: --simular)"
    )


def test_una_opcion_nueva_del_parser_da_no_sin_tocar_la_lista() -> None:
    """Una opcion inventada, anadida al parser en el test: sale de `opciones_de_la_corrida` sin
    tocar nada y da «no». La lista no se toca."""
    lista_antes = arnes.OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA
    parser = build_parser()
    probe = parser.parse_args(["motor", "arnes", "--salida", "x.txt"])
    probe.parser_de_la_corrida.add_argument("--opcion-inventada", action="store_true")
    opciones = _parsear("--opcion-inventada", parser=parser)
    assert "--opcion-inventada" in opciones
    linea = _linea(_corrida(10, 7, 4), opciones)
    assert linea.endswith(": no (opción fuera de la lista: --opcion-inventada)")
    assert arnes.OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA is lista_antes


def test_una_opcion_del_parser_raiz_tambien_cuenta() -> None:
    """`--repo` es del parser raiz y cambia el repositorio entero: tambien esta fuera de la lista
    (revisor de esta rama, segunda pasada, a1)."""
    args = build_parser().parse_args(["--repo", "X:/otro", "motor", "arnes", "--salida", "x.txt"])
    opciones = opciones_de_la_corrida((args.parser_raiz, args.parser_de_la_corrida), args)
    assert opciones == ("--repo", "--salida")
    linea = _linea(_corrida(10, 7, 4), opciones)
    assert linea.endswith(": no (opción fuera de la lista: --repo)")


def test_solo_las_de_la_lista_y_que_llega_da_si() -> None:
    opciones = _parsear("--tracemalloc", "--meses", "2030-01,2030-03")
    assert opciones == ("--meses", "--salida", "--tracemalloc")
    assert _linea(_corrida(10, 7, 4), opciones).endswith(": sí")


def test_la_lista_es_exactamente_la_de_la_enmienda() -> None:
    lista = arnes.OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA
    assert lista == {"--salida", "--tracemalloc", "--meses"}


def test_una_corrida_sobre_parte_de_construccion_no_habilita() -> None:
    linea = _linea(_corrida(10, 7, 4, meses=("2030-01",)))
    assert linea.endswith(
        ": no (la corrida no cubre todo el conjunto de construccion (falta 2030-03))"
    )


def test_los_motivos_se_suman() -> None:
    v = habilita_medir(
        medir([], [], CRITERIO.tolerancias),
        CRITERIO,
        ("2030-01",),
        opciones_fuera=("--simular",),
    )
    assert not v.habilita
    assert len(v.motivos) == 4  # la opcion, conjunto incompleto, cobertura y precision


def test_el_informe_exige_decir_que_opciones_uso_la_corrida() -> None:
    """Sin el argumento, `informe` no se puede llamar: ningun llamador puede olvidarlo y dejar el
    veredicto sin mirar las opciones."""
    with pytest.raises(TypeError, match="opciones"):
        arnes.informe(_corrida(1, 1, 0), CRITERIO, VOCABULARIO)  # type: ignore[call-arg]


def test_el_comando_pasa_al_informe_las_opciones_leidas_del_parser() -> None:
    """El comando `motor arnes` le pasa a `informe` las opciones que calcula
    `opciones_de_la_corrida` sobre su propio parser, no una constante (revisor de esta rama, a2).
    Se lee el codigo, sin ejecutar el comando: en esta rama el arnes no se corre."""
    import ast

    fuente = (REPO / "src" / "botsito" / "cli.py").read_text(encoding="utf-8")
    arbol = ast.parse(fuente)
    llamadas = [
        n
        for n in ast.walk(arbol)
        if isinstance(n, ast.Call)
        and isinstance(n.func, ast.Attribute)
        and n.func.attr == "informe"
        and isinstance(n.func.value, ast.Name)
        and n.func.value.id == "arnes"
    ]
    assert len(llamadas) == 1, "el comando llama a arnes.informe una sola vez"
    argumento = next(k.value for k in llamadas[0].keywords if k.arg == "opciones")
    assert ast.unparse(argumento) == "opciones"
    asignaciones = [
        ast.unparse(n.value)
        for n in ast.walk(arbol)
        if isinstance(n, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "opciones" for t in n.targets)
    ]
    assert (
        "opciones_de_la_corrida((args.parser_raiz, args.parser_de_la_corrida), args)"
        in asignaciones
    )
