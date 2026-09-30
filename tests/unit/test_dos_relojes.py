"""Dos relojes (ADR-0063): el de las SESIONES lo elige `reloj_sesiones`; el del DIA DE RIESGO sigue
en `huso_operativa`.

Hoy el selector vale `civil_operativa` y nada cambia. Lo que se prueba es el mecanismo que ADR-0059
pedia: con el selector en `grafico` -la lectura PROVISIONAL de A-42: las sesiones fijas en el reloj
del grafico, UTC+2 todo el ano-, en invierno la ventana abre una hora antes en el reloj del trader,
y el cableado NO se niega, porque el dia de riesgo sigue en el reloj civil, que es el de la firma.
El 2026-09-29 se intento lo mismo cambiando `huso_operativa` y el motor dejaba de correr en
invierno. Ninguna fecha real: los dias son de 2030."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.velas import MinutoUtc
from botsito.engine.cableado import CableadoError, comprobar_reloj_unico
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
    HUSO_DEL_RELOJ,
    PARAMETRO_RELOJ_SESIONES,
    RelojError,
    huso_de_las_sesiones,
    huso_del_reloj,
)
from botsito.spec.modelo import (
    FICHERO_SPEC,
    _invocaciones,
    cargar_reglas,
    cargar_vocabulario,
    parametros_leidos_por_las_formas,
)
from tests.unit import test_cableado as tc
from tests.unit import test_huecos_motor as th

RAIZ = Path(__file__).resolve().parents[2]
REAL = RAIZ / "knowledge" / "spec" / "parametros.yaml"
SPEC = RAIZ / FICHERO_SPEC
VENTANA = {"inicio": "ventana_inicio", "fin": "ventana_fin", "reloj": "reloj_sesiones",
           "dias": "dias_operables"}  # fmt: skip
INVIERNO, VERANO = "2030-01-15", "2030-07-16"  # martes los dos


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(REAL)


def _cambiar(texto: str, tras: str, viejo: str, nuevo: str) -> str:
    """Sustituye la primera aparicion de `viejo` DESPUES de `tras`: dentro de ese parametro."""
    i = texto.index(tras)
    j = texto.index(viejo, i)
    return texto[:j] + nuevo + texto[j + len(viejo) :]


@pytest.fixture(scope="module")
def en_el_grafico(tmp_path_factory: pytest.TempPathFactory) -> Registro:
    """El registro real con las sesiones en el reloj del grafico: el selector en `grafico` y las
    dos horas de la ventana declarando el huso de ese reloj. Nada mas cambia."""
    texto = REAL.read_text(encoding="utf-8")
    grafico = cargar_registro(REAL).texto("huso_grafico")
    texto = _cambiar(
        texto, "  - nombre: reloj_sesiones\n", 'valor: "civil_operativa"', 'valor: "grafico"'
    )
    for hora in ("ventana_inicio", "ventana_fin"):
        texto = _cambiar(texto, f"  - nombre: {hora}\n", "huso: Europe/Madrid", f"huso: {grafico}")
    ruta = tmp_path_factory.mktemp("registro") / "parametros.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return cargar_registro(ruta)


def _minuto(utc: str) -> MinutoUtc:
    return MinutoUtc(a_minuto(datetime.fromisoformat(f"{utc}+00:00")))


def _en_ventana(reg: Registro, utc: str) -> Tri:
    predicado = primitivas_escritas(reg).predicados["en_ventana"]
    salida = predicado(VENTANA, Momento(_minuto(utc), "07-11", False, None), EstadoDia())
    assert isinstance(salida, Resultado)
    return salida.valor


# ---------------------------------------------------------------------------- el registro


def test_el_selector_nace_en_el_reloj_civil_y_bajo_a42(registro: Registro) -> None:
    p = registro.parametros[PARAMETRO_RELOJ_SESIONES]
    assert p.categoria == "ejecucion" and p.estado.value == "DEFAULT_AMBIGUOUS"
    assert p.ambiguedad_id == "A-42" and p.opciones == tuple(HUSO_DEL_RELOJ)
    assert registro.opcion(PARAMETRO_RELOJ_SESIONES) == "civil_operativa"
    # nace apuntando al reloj que el motor ya usaba: nada cambia todavia
    assert huso_de_las_sesiones(registro) == registro.texto("huso_operativa")
    # y el huso de cada reloj vive en su parametro, no en el selector
    for parametro in HUSO_DEL_RELOJ.values():
        assert registro.texto(parametro)


def test_las_horas_de_la_ventana_declaran_el_huso_del_reloj_de_las_sesiones(
    registro: Registro, en_el_grafico: Registro
) -> None:
    for reg in (registro, en_el_grafico):
        for hora in ("ventana_inicio", "ventana_fin"):
            assert reg.hora(hora).huso == huso_de_las_sesiones(reg), hora
    assert huso_de_las_sesiones(en_el_grafico) == registro.texto("huso_grafico")


def test_las_formas_de_la_ventana_nombran_el_selector_y_ninguna_lee_huso_operativa(
    registro: Registro,
) -> None:
    reglas = cargar_reglas(SPEC)
    rn001 = next(r for r in reglas if r.id == "RN-001")
    rn002 = next(r for r in reglas if r.id == "RN-002")
    assert isinstance(rn001.forma, dict) and isinstance(rn002.forma, dict)
    assert dict(_invocaciones(rn001.forma["cuando"]))["en_ventana"] == VENTANA
    assert dict(_invocaciones(rn002.forma["cuando"]))["alcanza_hora"] == {
        "hora": "ventana_fin",
        "reloj": "reloj_sesiones",
    }
    leidos = parametros_leidos_por_las_formas(
        reglas, set(registro.nombres()), cargar_vocabulario(SPEC)
    )
    assert "reloj_sesiones" in leidos and "huso_operativa" not in leidos


def test_un_selector_con_un_reloj_desconocido_se_dice() -> None:
    class Falso:
        def opcion(self, nombre: str) -> str:
            return "servidor"

    with pytest.raises(RelojError, match="servidor"):
        huso_del_reloj(Falso(), "reloj_sesiones")  # type: ignore[arg-type]


# ------------------------------------------------------------------------------ la ventana


@pytest.mark.parametrize(
    ("utc", "civil", "grafico"),
    [
        # invierno: las 07:00 del grafico (UTC+2) son las 05:00 UTC y las 06:00 de Madrid
        (f"{INVIERNO}T04:59", Tri.NO, Tri.NO),
        (f"{INVIERNO}T05:00", Tri.NO, Tri.SI),
        (f"{INVIERNO}T06:00", Tri.SI, Tri.SI),
        (f"{INVIERNO}T12:59", Tri.SI, Tri.SI),
        (f"{INVIERNO}T13:00", Tri.SI, Tri.NO),  # las 15:00 del grafico: ya fuera
        (f"{INVIERNO}T14:00", Tri.NO, Tri.NO),
        # verano: los dos relojes dan la misma hora
        (f"{VERANO}T04:59", Tri.NO, Tri.NO),
        (f"{VERANO}T05:00", Tri.SI, Tri.SI),
        (f"{VERANO}T12:59", Tri.SI, Tri.SI),
        (f"{VERANO}T13:00", Tri.NO, Tri.NO),
    ],
)
def test_la_ventana_se_cuenta_con_el_reloj_que_dice_el_selector(
    registro: Registro, en_el_grafico: Registro, utc: str, civil: Tri, grafico: Tri
) -> None:
    assert _en_ventana(registro, utc) is civil
    assert _en_ventana(en_el_grafico, utc) is grafico


def test_el_motor_abre_las_sesiones_con_el_reloj_del_selector(
    registro: Registro, en_el_grafico: Registro
) -> None:
    """De punta a punta por el motor de la spec, un dia de invierno: las sesiones abren a las 07:00
    y a las 11:00 del reloj que diga el selector, y RN-001 no prohibe dentro de ellas: el limite
    de la sesion y `en_ventana` leen el MISMO reloj."""
    reglas = reglas_ejecutables(cargar_reglas(SPEC))
    voc = cargar_vocabulario(SPEC)
    esperado = {
        "civil": (registro, [_minuto(f"{INVIERNO}T06:00"), _minuto(f"{INVIERNO}T10:00")]),
        "grafico": (en_el_grafico, [_minuto(f"{INVIERNO}T05:00"), _minuto(f"{INVIERNO}T09:00")]),
    }
    for nombre, (reg, aperturas) in esperado.items():
        motor = MotorSpec(Interprete(voc, primitivas_escritas(reg)), reglas)
        dia = DiaDeMercado(
            th.DIA,
            huso_de_las_sesiones(reg),
            th.SESIONES,
            DatosMercado(th._velas("arriba", "arriba")),
        )
        r = motor.correr_dia(dia)
        fijan_el_sesgo = sorted(
            t for s in r.sesiones.values() for t, regla, _, _ in s.fijados if regla == "RN-003"
        )
        assert fijan_el_sesgo == aperturas, nombre
        assert "RN-001" not in r.sesiones["07-11"].disparadas, nombre


# ---------------------------------------------------------------------- el dia de riesgo


def test_el_dia_de_riesgo_sigue_en_el_reloj_civil_y_el_cableado_no_se_niega_en_invierno(
    en_el_grafico: Registro, tmp_path: Path
) -> None:
    perfil = cargar_perfil(tc.PERFIL)
    fase = reglas_de_fase(perfil, "reto")
    mercados = {tc.DIA.isoformat(): tc._mercado(tc.RUTA_STOP)}  # un martes de enero
    # con las sesiones en el grafico, el reloj del dia de riesgo no se ha movido
    assert en_el_grafico.texto("huso_operativa") != huso_de_las_sesiones(en_el_grafico)
    comprobar_reloj_unico(en_el_grafico, fase, mercados)
    # lo que se probo el 2026-09-29 (ADR-0059): mover `huso_operativa` al reloj del grafico rompe
    # la medianoche de la firma, y el cableado se niega
    texto = REAL.read_text(encoding="utf-8")
    texto = _cambiar(
        texto,
        "  - nombre: huso_operativa\n",
        'valor: "Europe/Madrid"',
        f'valor: "{en_el_grafico.texto("huso_grafico")}"',
    )
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto, encoding="utf-8")
    with pytest.raises(CableadoError, match="no hay un solo reloj"):
        comprobar_reloj_unico(cargar_registro(ruta), fase, mercados)
