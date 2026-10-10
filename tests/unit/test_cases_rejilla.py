"""cases/ cuenta la ventana de cada caso por la rejilla H4 (ADR-0069), por la puerta del reloj de
las sesiones, y no en la pared de `huso_operativa` (`trabajo/cases-rejilla`, CASES-REJILLA.md).

Fechas: solo semanas de 2024 (ACTIVACION-A42.md §4). La del 27 al 31 de octubre de 2024 es de
desfase -Europa ya cambio la hora y EE. UU. no-; la del 3 al 7 de noviembre es la de control. El
DIA DE DESFASE se calcula aqui con zoneinfo a partir de esa condicion, nunca con una lista.

Cada test de los que rompen a proposito dice como falla con el codigo de `main`.
"""

from __future__ import annotations

import ast
import inspect
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.cases import ventanas
from botsito.cases.relojes import RelojSesiones, reloj_de_las_sesiones
from botsito.cases.ventanas import (
    Anclaje,
    Caso,
    Excluido,
    RelojDelArtefacto,
    construir_caso,
    reloj_congelado,
    reloj_de_ventanas,
    reloj_del_registro,
)
from botsito.config.registro import Registro, cargar_registro
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import MinutoUtc, SerieVelas, Vela
from botsito.engine import relojes as relojes_del_motor

RAIZ = Path(__file__).resolve().parents[2]
CASES = RAIZ / "src" / "botsito" / "cases"
SESIONES = (("07-11", "07:00", "11:00"), ("11-15", "11:00", "15:00"))
VENTANA = ("00:00", "15:00")
ANCLAJES = [Anclaje("ny-17", "17:00", "America/New_York", True)]
DESFASE = date(2024, 10, 28)  # lunes
CONTROL = date(2024, 11, 4)  # lunes


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def es_desfase(dia: date, registro: Registro) -> bool:
    """Solo uno de los dos -EE. UU., el huso del ancla, o Europa- ha cambiado la hora."""
    t = datetime(dia.year, dia.month, dia.day, 12, tzinfo=UTC)
    eeuu = ZoneInfo(registro.hora("anclaje_h4").huso)
    europa = ZoneInfo(registro.texto("huso_operativa"))
    return bool(t.astimezone(eeuu).dst()) != bool(t.astimezone(europa).dst())


def _serie(desde: datetime, horas: int) -> SerieVelas:
    inicio = int(desde.timestamp() // 60)
    p = Puntos(100000)
    velas = tuple(
        Vela(MinutoUtc(inicio + k), p, Puntos(100002), Puntos(99998), Puntos(100001), 1)
        for k in range(60 * horas)
    )
    return SerieVelas("XXXYYY", 1, 100000, 1000, velas, "prueba-1")


def _caso(
    dia: date,
    reloj: RelojSesiones,
    sesiones: tuple[tuple[str, str, str], ...] = SESIONES,
    ventana: tuple[str, str] = VENTANA,
    min_velas: int = 850,
) -> Caso | Excluido:
    inicio = datetime(dia.year, dia.month, dia.day, tzinfo=UTC) - timedelta(days=2)
    serie = _serie(inicio, 96)
    return construir_caso(serie, dia, "xxxyyy", reloj, ventana, sesiones, ANCLAJES, min_velas)


# ------------------------------------------------------------------------ las dos semanas de 2024


def test_las_semanas_de_2024_son_lo_que_dice_el_encargo(registro: Registro) -> None:
    assert es_desfase(DESFASE, registro) and not es_desfase(CONTROL, registro)


def test_un_dia_de_desfase_abre_una_hora_antes_que_la_pared(registro: Registro) -> None:
    """Con `main` falla: `construir_caso` recibe el huso y cuenta la ventana en la pared de Madrid,
    00:00-15:00 (23:00Z-14:00Z). Por la rejilla, el trader opera ese dia de 06:00 a 14:00 de
    Madrid, y la ventana del caso es 23:00 de la vispera - 14:00 de Madrid: 22:00Z-13:00Z."""
    caso = _caso(DESFASE, reloj_de_las_sesiones(registro))
    pared = _caso(DESFASE, RelojSesiones.de_pared(registro.texto("huso_operativa")))
    assert isinstance(caso, Caso) and isinstance(pared, Caso)
    assert (caso.desde_utc, caso.hasta_utc) == ("2024-10-27T22:00Z", "2024-10-28T13:00Z")
    assert (pared.desde_utc, pared.hasta_utc) == ("2024-10-27T23:00Z", "2024-10-28T14:00Z")
    # las dos sesiones del trader son las velas H4 de la rejilla que abren a las 05:00Z y 09:00Z
    assert caso.limites_h4["ny-17"][-3:] == [
        "2024-10-28T05:00Z",
        "2024-10-28T09:00Z",
        "2024-10-28T13:00Z",
    ]


def test_un_dia_de_control_sale_identico_al_de_main(registro: Registro) -> None:
    """Fuera de desfase la rejilla y la pared de `huso_operativa` dan los mismos instantes: el caso
    es el mismo byte a byte que el que calculaba `main` (la pared), con sus velas y su hash."""
    caso = _caso(CONTROL, reloj_de_las_sesiones(registro))
    pared = _caso(CONTROL, RelojSesiones.de_pared(registro.texto("huso_operativa")))
    assert isinstance(caso, Caso)
    assert caso == pared
    assert (caso.desde_utc, caso.hasta_utc) == ("2024-11-03T23:00Z", "2024-11-04T14:00Z")
    assert caso.n_velas == 900


# --------------------------------------------------------------------- el dia que no se decide


def test_un_dia_de_rejilla_con_vela_irregular_no_entra_en_el_universo() -> None:
    """Con el ancla del registro esto NUNCA le pasa a un laborable (de 2000 a 2035 la puerta no
    decide 72 dias, todos domingos: CASES-REJILLA.md §0.e). Se fuerza con un ancla SINTETICA en un
    huso que cambia de hora en viernes -Israel, el viernes 29 de marzo de 2024-, que vive solo
    aqui y nunca en el registro. Con `main` falla: el viernes entra como `Caso` (medido con un
    minimo de 150 velas; con 200 lo excluia, pero por tener 180, no por la puerta)."""
    reloj = RelojSesiones(
        "rejilla_h4",
        "Asia/Jerusalem",
        anclaje=HoraLocal("00:00", "Asia/Jerusalem"),
        primera_vela=1,
        inicio_nominal=0,
    )
    sesiones = (("s1", "00:00", "04:00"),)
    viernes = _caso(date(2024, 3, 29), reloj, sesiones, ("00:00", "04:00"), 150)
    jueves = _caso(date(2024, 3, 28), reloj, sesiones, ("00:00", "04:00"), 150)
    assert isinstance(jueves, Caso)
    assert isinstance(viernes, Excluido)
    assert viernes.motivo.startswith("la puerta del reloj no decide el dia: 2024-03-29")
    assert "no es entera" in viernes.motivo


# ------------------------------------------------------------------- un solo camino de calculo


_CONVERSIONES = {"astimezone", "ZoneInfo", "combine", "localize", "fromtimestamp"}
# Las UNICAS llamadas de cases/ (fuera de la puerta) que tocan un huso, cada una con su motivo.
_PERMITIDAS = {
    # pintar una hora en el grafico del trader; ninguna ventana se calcula con esto
    ("ventanas.py", "_en_pantalla", "astimezone"),
    # validar que el huso de un anclaje candidato existe al leer el config
    ("paquete.py", "config_desde_doc", "ZoneInfo"),
}


def _conversiones(fichero: Path) -> set[tuple[str, str, str]]:
    arbol = ast.parse(fichero.read_text(encoding="utf-8"))
    salida: set[tuple[str, str, str]] = set()

    def visitar(nodo: ast.AST, funcion: str) -> None:
        for hijo in ast.iter_child_nodes(nodo):
            nombre = (
                hijo.name if isinstance(hijo, ast.FunctionDef | ast.AsyncFunctionDef) else funcion
            )
            if isinstance(hijo, ast.Call):
                f = hijo.func
                llamada = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
                if llamada in _CONVERSIONES:
                    salida.add((fichero.name, nombre, llamada))
                if any(k.arg == "tzinfo" for k in hijo.keywords):
                    salida.add((fichero.name, nombre, "tzinfo="))
            visitar(hijo, nombre)

    visitar(arbol, "<modulo>")
    return salida


def test_un_solo_camino_ningun_sitio_de_cases_convierte_horas_con_un_huso() -> None:
    """Toda ventana se calcula por la puerta (`cases/relojes.py`). Con `main` falla: la ventana
    del caso (`ventanas._minuto`), la sesion de la ingesta y las horas de las dos hojas pasaban
    un instante a `huso_operativa` cada una por su cuenta."""
    encontradas: set[tuple[str, str, str]] = set()
    for fichero in sorted(CASES.glob("*.py")):
        if fichero.name != "relojes.py":
            encontradas |= _conversiones(fichero)
    assert encontradas == _PERMITIDAS


def test_la_ventana_y_la_ingesta_piden_el_reloj_y_no_un_huso() -> None:
    from botsito.cases.ingesta import ingerir

    for funcion in (ventanas.construir_caso, ventanas.universo):
        parametros = inspect.signature(funcion).parameters
        assert "reloj" in parametros, funcion.__name__
        assert not [p for p in parametros if "huso" in p], funcion.__name__
    assert "reloj" in inspect.signature(ingerir).parameters


def test_engine_relojes_no_define_nada_propio() -> None:
    """La puerta vive en `cases/relojes.py` (contrato de capas: `cases` no importa de `engine`) y
    `engine/relojes.py` la REEXPORTA: ni una funcion ni una clase propias, o habria dos puertas."""
    fuente = inspect.getsource(relojes_del_motor)
    arbol = ast.parse(fuente)
    propias = [
        n.name
        for n in ast.walk(arbol)
        if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef | ast.Lambda)
        and not isinstance(n, ast.Lambda)
    ]
    assert propias == []
    from botsito.cases import relojes

    for nombre in relojes.__all__:
        assert getattr(relojes_del_motor, nombre) is getattr(relojes, nombre), nombre


# ---------------------------------------------------- el reloj congelado, negando por defecto


def test_un_artefacto_nuevo_congela_el_reloj_del_registro(registro: Registro) -> None:
    elegido = reloj_del_registro(registro)
    assert elegido.congelado == {
        "reloj_sesiones": "rejilla_h4",
        "anclaje_h4": {"hora": "17:00", "huso": "America/New_York"},
        "sesiones_primera_vela_h4": 3,
        "ventana_inicio": {"hora": "07:00", "huso": "Europe/Madrid"},
        "huso_grafico": "Europe/Madrid",
    }
    assert reloj_congelado(elegido.congelado, "x") == elegido.reloj


def test_con_la_clave_manda_el_reloj_congelado_y_no_el_del_registro(registro: Registro) -> None:
    congelado = dict(reloj_del_registro(registro).congelado or {})
    congelado["sesiones_primera_vela_h4"] = 2
    leido = reloj_de_ventanas({"huso_operativa": "Europe/Madrid", "reloj_sesiones": congelado}, "x")
    assert leido.reloj.primera_vela == 2 and leido.congelado == congelado


def test_sin_la_clave_el_artefacto_se_calculo_en_su_huso_operativa() -> None:
    leido = reloj_de_ventanas({"huso_operativa": "Europe/Madrid"}, "x")
    assert leido == RelojDelArtefacto(RelojSesiones.de_pared("Europe/Madrid"), None)


@pytest.mark.parametrize(
    "ventanas_doc, mensaje",
    [
        ({}, "sin reloj_sesiones y sin un huso_operativa valido"),
        ({"huso_operativa": "Marte/Olimpo"}, "sin reloj_sesiones y sin un huso_operativa valido"),
        ({"reloj_sesiones": "rejilla_h4"}, "reloj_sesiones debe ser un mapa"),
        ({"reloj_sesiones": {"reloj_sesiones": "servidor"}}, "no es un reloj que la puerta"),
        (
            {"reloj_sesiones": {"reloj_sesiones": "civil_operativa"}},
            "lleva exactamente",
        ),
        (
            {
                "reloj_sesiones": {
                    "reloj_sesiones": "civil_operativa",
                    "huso_operativa": "Europe/Madrid",
                    "de_mas": 1,
                }
            },
            "lleva exactamente",
        ),
        (
            {"reloj_sesiones": {"reloj_sesiones": "civil_operativa", "huso_operativa": "Nada"}},
            "huso desconocido",
        ),
    ],
)
def test_la_clave_se_lee_negando_por_defecto(ventanas_doc: dict[str, Any], mensaje: str) -> None:
    from botsito.cases.relojes import RelojError

    with pytest.raises(RelojError, match=mensaje):
        reloj_de_ventanas(ventanas_doc, "x/ventanas.yaml")


def test_una_vela_fuera_de_la_rejilla_en_la_clave_es_un_error_con_nombre(
    registro: Registro,
) -> None:
    from botsito.cases.relojes import RelojError

    congelado = dict(reloj_del_registro(registro).congelado or {})
    congelado["sesiones_primera_vela_h4"] = 9
    with pytest.raises(RelojError, match="sesiones_primera_vela_h4 = 9"):
        reloj_congelado(congelado, "x")


# ------------------------------------------------------------------------------- las hojas


def _hojas(caso: Caso, reloj: RelojSesiones) -> tuple[str, str]:
    from botsito.cases import hoja_docx
    from botsito.cases.paquete import cargar_config, hoja_trader

    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    asignacion = {caso.id: "dev"}
    md = hoja_trader(
        "2024-01-01-sesion-99", config, "Europe/Madrid", [], [caso], asignacion, set(), reloj
    )
    docx = hoja_docx.bloque_etiquetado(
        [caso.como_dict()], asignacion, config, reloj, "P-01", "EURUSD"
    )
    return md, docx


def test_la_hoja_de_un_dia_normal_es_la_de_main_byte_a_byte(registro: Registro) -> None:
    """Fuera de desfase la hoja con la rejilla es la que daba `main` (la pared de Madrid)."""
    rejilla = reloj_de_las_sesiones(registro)
    caso = _caso(CONTROL, rejilla)
    assert isinstance(caso, Caso)
    md, docx = _hojas(caso, rejilla)
    md_main, docx_main = _hojas(caso, RelojSesiones.de_pared("Europe/Madrid"))
    assert (md, docx) == (md_main, docx_main)
    assert "otras horas" not in md and "es distinto" not in docx


def test_la_hoja_de_un_dia_de_desfase_dice_las_horas_que_vera_el_trader(
    registro: Registro,
) -> None:
    """Con `main` falla: la hoja decia 00:00-15:00 y sesiones 07:00-11:00 y 11:00-15:00 tambien
    ese dia, y su grafico marca 23:00 de la vispera - 14:00, con las sesiones una hora antes."""
    rejilla = reloj_de_las_sesiones(registro)
    caso = _caso(DESFASE, rejilla)
    assert isinstance(caso, Caso)
    md, docx = _hojas(caso, rejilla)
    assert (
        "- 2024-10-28: dia operativo de 23:00 de la vispera a 14:00; sesiones: 07-11 de 06:00 a "
        "10:00, 11-15 de 10:00 a 14:00." in md
    )
    assert "El 2024-10-28 es distinto" in docx
    assert "de 23:00 de la víspera a 14:00" in docx
    assert "07-11 de 06:00 a 10:00, 11-15 de 10:00 a 14:00" in docx
