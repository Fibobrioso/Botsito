"""A-42 RESUELTA (ADR-0069): las dos sesiones son las velas H4 de la rejilla de `anclaje_h4` que
empiezan en ancla + 8 h y ancla + 12 h (H2b), y el bot las fija en instantes UTC con zoneinfo,
nunca con un desfase fijo.

Todo con fechas de calendario y sin leer datos: lo que se comprueba es el reloj. Las fechas son
las del encargo (`docs/encargos/trabajo-activacion-a42.md`, fase 1, paso 5): 2026-10-23 y
2026-10-26 (05:00 UTC), 2026-11-02 (06:00 UTC), un dia de enero de 2026 (06:00 UTC), la semana
2025-03-10/14 (EE. UU. ya cambio y Europa no) y las dos semanas de 2024 de las capturas del trader
(RELOJ-INVIERNO.md §12, ACTIVACION-A42.md §4). H2a es lo que hacia el motor (la ventana en el
reloj civil, `civil_operativa`); H1, la lectura provisional de ADR-0059 (la ventana fija en un
reloj UTC+2: `grafico` con el grafico en Etc/GMT-2). Las dos se calculan por el MISMO camino que
H2b y fallan donde el encargo dice.
"""

from __future__ import annotations

import ast
import re
from dataclasses import replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import limites_del_dia
from botsito.data.velas import a_datetime, a_minuto
from botsito.domain.velas import MinutoUtc
from botsito.engine import relojes
from botsito.engine.cableado import comprobar_reloj_unico
from botsito.engine.cuenta import reglas_de_fase
from botsito.engine.interprete import (
    EstadoDia,
    Interprete,
    Momento,
    Resultado,
    Tri,
    reglas_ejecutables,
)
from botsito.engine.motor import DatosMercado, DiaDeMercado, MotorSpec
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.primitivas import primitivas_escritas
from botsito.engine.relojes import (
    PARAMETRO_RELOJ_SESIONES,
    PARAMETROS_DE_LA_REJILLA,
    REJILLA_H4,
    RelojError,
    RelojSesiones,
    reloj_de_las_sesiones,
)
from botsito.spec.modelo import FICHERO_SPEC, cargar_reglas, cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_huecos_motor as th

RAIZ = Path(__file__).resolve().parents[2]
REAL = RAIZ / "knowledge" / "spec" / "parametros.yaml"
SPEC = RAIZ / FICHERO_SPEC
SESIONES = tuple((s.nombre, s.desde, s.hasta) for s in th.SESIONES)
VENTANA = {"inicio": "ventana_inicio", "fin": "ventana_fin", "reloj": "reloj_sesiones",
           "dias": "dias_operables"}  # fmt: skip
UN_DIA_DE_ENERO = date(2026, 1, 15)
SEMANA = [timedelta(days=k) for k in range(5)]

# (dia, apertura de la primera sesion en UTC) del encargo. La segunda abre 4 h despues y la
# ventana cierra a las 8 h.
ENCARGO: list[tuple[date, str]] = [
    (date(2026, 10, 23), "05:00"),
    (date(2026, 10, 26), "05:00"),
    (date(2026, 11, 2), "06:00"),
    (UN_DIA_DE_ENERO, "06:00"),
    *[(date(2025, 3, 10) + d, "05:00") for d in SEMANA],
    *[(date(2024, 10, 28) + d, "05:00") for d in SEMANA],
    *[(date(2024, 11, 4) + d, "06:00") for d in SEMANA],
]
# Donde cada hipotesis descartada da OTRA hora que H2b (ACTIVACION-A42.md §5.1).
FALLA_H2A = {date(2026, 10, 26), *[date(2025, 3, 10) + d for d in SEMANA],
             *[date(2024, 10, 28) + d for d in SEMANA]}  # fmt: skip
FALLA_H1 = {date(2026, 11, 2), UN_DIA_DE_ENERO, *[date(2024, 11, 4) + d for d in SEMANA]}


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(REAL)


def _cambiar(texto: str, tras: str, viejo: str, nuevo: str) -> str:
    i = texto.index(tras)
    j = texto.index(viejo, i)
    return texto[:j] + nuevo + texto[j + len(viejo) :]


def _registro(tmp_path_factory: pytest.TempPathFactory, nombre: str, texto: str) -> Registro:
    ruta = tmp_path_factory.mktemp(nombre) / "parametros.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return cargar_registro(ruta)


@pytest.fixture(scope="module")
def h2a(tmp_path_factory: pytest.TempPathFactory) -> Registro:
    """Lo que hacia el motor hasta ADR-0069: la ventana en el reloj civil del trader."""
    texto = REAL.read_text(encoding="utf-8")
    texto = _cambiar(
        texto, "  - nombre: reloj_sesiones\n", f'valor: "{REJILLA_H4}"', 'valor: "civil_operativa"'
    )
    return _registro(tmp_path_factory, "h2a", texto)


@pytest.fixture(scope="module")
def h1(tmp_path_factory: pytest.TempPathFactory) -> Registro:
    """La lectura provisional de ADR-0059: la ventana fija en el reloj del grafico, UTC+2 todo el
    ano. El huso fijo es la hipotesis, no un parametro de hoy."""
    texto = REAL.read_text(encoding="utf-8")
    texto = _cambiar(
        texto, "  - nombre: reloj_sesiones\n", f'valor: "{REJILLA_H4}"', 'valor: "grafico"'
    )
    texto = _cambiar(
        texto, "  - nombre: huso_grafico\n", 'valor: "Europe/Madrid"', 'valor: "Etc/GMT-2"'
    )
    for hora in ("ventana_inicio", "ventana_fin"):
        texto = _cambiar(texto, f"  - nombre: {hora}\n", "huso: Europe/Madrid", "huso: Etc/GMT-2")
    return _registro(tmp_path_factory, "h1", texto)


def _utc(dia: date, hhmm: str) -> MinutoUtc:
    hh, mm = (int(x) for x in hhmm.split(":"))
    return MinutoUtc(a_minuto(datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=UTC)))


def _aperturas(reloj: RelojSesiones, dia: date) -> list[MinutoUtc]:
    """Apertura de las dos sesiones y cierre de la ventana, por la puerta."""
    limites = reloj.limites_de_sesiones(dia, SESIONES)
    return [limites[0][1], limites[1][1], limites[1][2]]


# ---------------------------------------------------------------------------------- el registro


def test_el_selector_vale_rejilla_h4_confirmado_y_sin_ambiguedad(registro: Registro) -> None:
    p = registro.parametros[PARAMETRO_RELOJ_SESIONES]
    assert registro.opcion(PARAMETRO_RELOJ_SESIONES) == REJILLA_H4
    assert p.estado.value == "CONFIRMED" and p.ambiguedad_id is None
    assert p.fuente is not None and p.fuente.tipo == "decision" and p.fuente.id == "ADR-0069"
    # las dos opciones de ADR-0063 siguen ahi: H2a y H1 se calculan por el mismo camino
    assert set(p.opciones or ()) == {"civil_operativa", "grafico", REJILLA_H4}
    vela = registro.parametros[PARAMETROS_DE_LA_REJILLA["primera_vela"]]
    assert vela.categoria == "ejecucion" and registro.entero(vela.nombre) == 3
    # las horas nominales se nombran en el reloj del grafico, que es lo que el trader ve
    for hora in ("ventana_inicio", "ventana_fin"):
        assert registro.hora(hora).huso == registro.texto("huso_grafico"), hora


def test_con_la_rejilla_no_hay_huso_de_las_sesiones(registro: Registro) -> None:
    with pytest.raises(RelojError, match="la rejilla no es un huso"):
        relojes.huso_de_las_sesiones(registro)
    assert reloj_de_las_sesiones(registro).huso_visible == registro.texto("huso_grafico")


# --------------------------------------------------------------------- las fechas del encargo


@pytest.mark.parametrize(("dia", "apertura"), ENCARGO, ids=lambda x: str(x))
def test_las_horas_del_encargo_en_utc(registro: Registro, dia: date, apertura: str) -> None:
    reloj = reloj_de_las_sesiones(registro)
    hh = int(apertura[:2])
    esperado = [_utc(dia, apertura), _utc(dia, f"{hh + 4:02d}:00"), _utc(dia, f"{hh + 8:02d}:00")]
    assert _aperturas(reloj, dia) == esperado
    # y las primitivas leen lo mismo: el dia y la hora nominal de la apertura
    assert reloj.lectura(int(esperado[0])) == (dia, registro.hora("ventana_inicio").minutos_del_dia)
    assert reloj.lectura(int(esperado[2]) - 1) == (
        dia,
        registro.hora("ventana_fin").minutos_del_dia - 1,
    )


def test_h2a_da_otra_hora_justo_donde_el_encargo_dice(registro: Registro, h2a: Registro) -> None:
    rejilla, civil = reloj_de_las_sesiones(registro), reloj_de_las_sesiones(h2a)
    distintos = {dia for dia, _ in ENCARGO if _aperturas(civil, dia) != _aperturas(rejilla, dia)}
    assert distintos == FALLA_H2A


def test_h1_da_otra_hora_justo_donde_el_encargo_dice(registro: Registro, h1: Registro) -> None:
    rejilla, fijo = reloj_de_las_sesiones(registro), reloj_de_las_sesiones(h1)
    distintos = {dia for dia, _ in ENCARGO if _aperturas(fijo, dia) != _aperturas(rejilla, dia)}
    assert distintos == FALLA_H1


# ----------------------------------------------------------------- ningun desfase fijo


def _laborables(desde: int, hasta: int) -> list[date]:
    dia, salida = date(desde, 1, 1), []
    while dia.year <= hasta:
        if dia.isoweekday() <= 5:
            salida.append(dia)
        dia += timedelta(days=1)
    return salida


def test_ninguna_hora_de_sesion_sale_de_un_desfase_fijo(registro: Registro) -> None:
    """(a) En todo dia laborable de 2024 a 2027 la apertura es un limite de la rejilla de
    `anclaje_h4`, y la hora UTC toma DOS valores, no uno. (b) Ningun desfase fijo de UTC con la
    hora nominal reproduce esos cuatro anos. (c) Y la guardia de la vela irregular no cae en ningun
    dia laborable (anadido 1 del consultor): solo puede caer en dias de rejilla sin mercado."""
    reloj = reloj_de_las_sesiones(registro)
    ancla = registro.hora(PARAMETROS_DE_LA_REJILLA["anclaje"])
    inicio = registro.hora("ventana_inicio").minutos_del_dia
    horas_utc: set[str] = set()
    desfases: dict[int, int] = {}  # desfase (min) -> dias en que la hora nominal + desfase acierta
    dias = _laborables(2024, 2027)
    for dia in dias:
        abre = reloj.apertura(dia)  # (c): no levanta RelojError en ningun laborable
        limites = {int(x) for x in limites_del_dia(dia - timedelta(days=1), 240, ancla)}
        assert int(abre) in limites, dia
        horas_utc.add(f"{a_datetime(abre):%H:%M}")
        nominal = a_minuto(datetime(dia.year, dia.month, dia.day, tzinfo=UTC)) + inicio
        desfase = int(nominal) - int(abre)
        desfases[desfase] = desfases.get(desfase, 0) + 1
    assert horas_utc == {"05:00", "06:00"}  # (a)
    assert all(n < len(dias) for n in desfases.values()), desfases  # (b)


def test_con_un_ancla_sin_cambio_de_hora_las_fechas_de_verano_fallan(
    registro: Registro, tmp_path_factory: pytest.TempPathFactory
) -> None:
    """Si el huso del ancla no cambiara de hora, el reloj seria un desfase fijo y las fechas de
    verano del encargo saldrian una hora tarde: lo que distingue H2b es zoneinfo."""
    texto = REAL.read_text(encoding="utf-8")
    texto = _cambiar(texto, "  - nombre: anclaje_h4\n", "huso: America/New_York", "huso: Etc/GMT+5")
    fijo = reloj_de_las_sesiones(_registro(tmp_path_factory, "ancla-fija", texto))
    rejilla = reloj_de_las_sesiones(registro)
    verano = [dia for dia, apertura in ENCARGO if apertura == "05:00"]
    invierno = [dia for dia, apertura in ENCARGO if apertura == "06:00"]
    assert all(_aperturas(fijo, d) != _aperturas(rejilla, d) for d in verano)
    assert all(_aperturas(fijo, d) == _aperturas(rejilla, d) for d in invierno)


def test_el_codigo_del_reloj_no_lleva_ningun_desfase() -> None:
    """Ni un huso fijo, ni una suma de horas a UTC, ni una hora escrita: todo sale del registro
    y de `limites_del_dia`."""
    fuente = (RAIZ / "src" / "botsito" / "engine" / "relojes.py").read_text(encoding="utf-8")
    cuerpo = "\n".join(linea for linea in fuente.splitlines() if not linea.lstrip().startswith("#"))
    arbol = ast.parse(fuente)
    docstrings = {
        n.value.value
        for n in ast.walk(arbol)
        if isinstance(n, ast.Expr)
        and isinstance(n.value, ast.Constant)
        and isinstance(n.value.value, str)
    }
    for doc in docstrings:
        cuerpo = cuerpo.replace(doc, "")
    assert not re.search(r"Etc/GMT|(?<!as)timezone\(|timedelta\(hours|\b\d\d:\d\d\b", cuerpo)
    assert "limites_del_dia" in cuerpo


# ----------------------------------------------------------------------- las guardias


def test_una_sesion_que_no_es_una_vela_entera_falla_con_nombre(registro: Registro) -> None:
    reloj = reloj_de_las_sesiones(registro)
    with pytest.raises(RelojError, match="corta no es una vela H4 entera"):
        reloj.limites_de_sesiones(UN_DIA_DE_ENERO, [("corta", "07:00", "09:00")])
    with pytest.raises(RelojError, match="tarde no es una vela H4 entera"):
        reloj.limites_de_sesiones(UN_DIA_DE_ENERO, [("tarde", "08:00", "12:00")])


def test_el_dia_de_rejilla_con_vela_irregular_no_es_operable(registro: Registro) -> None:
    """El domingo del cambio de hora de Nueva York: la vela que abriria la ventana no es entera, y
    la puerta lo dice. Es un dia sin mercado: ningun laborable cae aqui (test de arriba)."""
    reloj = reloj_de_las_sesiones(registro)
    with pytest.raises(RelojError, match="no es entera"):
        reloj.apertura(date(2026, 3, 8))  # domingo: EE. UU. cambia a las 02:00


def test_un_selector_desconocido_se_dice() -> None:
    class Falso:
        def opcion(self, nombre: str) -> str:
            return "servidor"

    with pytest.raises(RelojError, match="servidor"):
        relojes.huso_del_reloj(Falso(), PARAMETRO_RELOJ_SESIONES)  # type: ignore[arg-type]
    with pytest.raises(RelojError, match="servidor"):
        reloj_de_las_sesiones(Falso())  # type: ignore[arg-type]


# -------------------------------------------------------------- el motor y el dia de riesgo


def _en_ventana(reg: Registro, dia: date, hhmm_utc: str) -> Tri:
    predicado = primitivas_escritas(reg).predicados["en_ventana"]
    salida = predicado(VENTANA, Momento(_utc(dia, hhmm_utc), "07-11", False, None), EstadoDia())
    assert isinstance(salida, Resultado)
    return salida.valor


@pytest.mark.parametrize(
    ("dia", "utc", "dentro"),
    [
        (date(2026, 10, 26), "04:59", Tri.NO),
        (date(2026, 10, 26), "05:00", Tri.SI),  # las 06:00 de Madrid esa semana
        (date(2026, 10, 26), "12:59", Tri.SI),
        (date(2026, 10, 26), "13:00", Tri.NO),
        (date(2026, 11, 2), "05:00", Tri.NO),
        (date(2026, 11, 2), "06:00", Tri.SI),  # las 07:00 de Madrid otra vez
        (date(2026, 11, 2), "14:00", Tri.NO),
        (date(2026, 10, 25), "05:00", Tri.NO),  # domingo: fuera de dias_operables
    ],
)
def test_en_ventana_lee_la_rejilla(registro: Registro, dia: date, utc: str, dentro: Tri) -> None:
    assert _en_ventana(registro, dia, utc) is dentro


def test_el_motor_abre_las_sesiones_en_los_limites_de_la_rejilla(registro: Registro) -> None:
    """De punta a punta por el motor de la spec, el lunes 26 de octubre de 2026 (Europa ya cambio,
    EE. UU. no): las sesiones abren a las 05:00 y 09:00 UTC, y RN-001 no prohibe dentro."""
    reglas = reglas_ejecutables(cargar_reglas(SPEC))
    voc = cargar_vocabulario(SPEC)
    motor = MotorSpec(Interprete(voc, primitivas_escritas(registro)), reglas)
    dia = date(2026, 10, 26)
    velas = th._velas("arriba", "arriba")
    # las H4 sinteticas de th son de 2030: se recolocan sobre la rejilla de ese lunes
    corrimiento = int(_utc(dia, "01:00")) - int(velas[1].inicio)
    recolocadas = [replace(v, inicio=MinutoUtc(int(v.inicio) + corrimiento)) for v in velas]
    mercado = DiaDeMercado(dia, "UTC", th.SESIONES, DatosMercado(recolocadas),
                           reloj=reloj_de_las_sesiones(registro))  # fmt: skip
    r = motor.correr_dia(mercado)
    fijan_el_sesgo = sorted(
        t for s in r.sesiones.values() for t, regla, _, _ in s.fijados if regla == "RN-003"
    )
    assert fijan_el_sesgo == [int(_utc(dia, "05:00")), int(_utc(dia, "09:00"))]
    assert "RN-001" not in r.sesiones["07-11"].disparadas


def test_el_dia_de_riesgo_sigue_en_el_reloj_civil(registro: Registro) -> None:
    perfil = cargar_perfil(tc.PERFIL)
    fase = reglas_de_fase(perfil, "reto")
    mercados = {tc.DIA.isoformat(): tc._mercado(tc.RUTA_STOP)}
    comprobar_reloj_unico(registro, fase, mercados)  # no se niega: el dia de riesgo no se movio


# ------------------------------------------------------------------- construccion


def test_fuera_de_las_semanas_del_cambio_la_rejilla_es_la_ventana_civil(
    registro: Registro, h2a: Registro
) -> None:
    """ADR-0069 §1: en 2026 solo difieren del 9 al 27 de marzo y del 26 al 30 de octubre. El
    material de construccion (enero, abril, mayo, agosto y septiembre) no tiene ningun dia ahi."""
    rejilla, civil = reloj_de_las_sesiones(registro), reloj_de_las_sesiones(h2a)
    distintos = [
        d for d in _laborables(2026, 2026) if _aperturas(rejilla, d) != _aperturas(civil, d)
    ]
    assert distintos == [
        *[
            date(2026, 3, 9) + timedelta(days=k)
            for k in range(19)
            if (date(2026, 3, 9) + timedelta(days=k)).isoweekday() <= 5
        ],
        *[date(2026, 10, 26) + d for d in SEMANA],
    ]
    assert {d.month for d in distintos} == {3, 10}
