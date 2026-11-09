"""La bitacora de decisiones y la ablacion (`engine/decisiones.py`, rama trabajo/trazas-ablacion)
sobre el dia SINTETICO de 2030 de `test_cableado.py`: ningun test lee velas ni ticks reales
(respuesta del consultor a la fase 0, punto 4). La prueba sobre la construccion entera es la corrida
de F4 (`motor arnes --simular` con un diff de 0 bytes contra la linea base)."""

from __future__ import annotations

import argparse
import re
from collections.abc import Mapping
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.criterio_fidelidad import Operacion
from botsito.cli import build_parser
from botsito.config.registro import Registro, cargar_registro
from botsito.engine import arnes, decisiones, diagnostico
from botsito.engine.cableado import Cierre, MotorCableado
from botsito.engine.interprete import (
    EstadoDia,
    Evento,
    Momento,
    NoImplementada,
    Resultado,
    Tri,
    reglas_ejecutables,
)
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario
from tests.unit.test_cableado import (
    DIA,
    ENTRADA,
    ESCALA,
    MINUTO_ZONA,
    RUTA_HUECO,
    RUTA_STOP,
    RUTA_VIVA,
    SPEC,
    _criterio,
    _dia,
    _mercado,
    _motor,
)

RAIZ = Path(__file__).resolve().parents[2]
PROHIBIDO_EN_LA_SALIDA = re.compile(r"%|PnL|\bR\b|rentab|USD|saldo|equity", re.IGNORECASE)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(SPEC)


def _foto(motor: MotorCableado, r: Any) -> tuple[Any, ...]:
    """Todo lo que el motor decide en el dia: operaciones, trazas por sesion, eventos del broker,
    ordenes y la cuenta."""
    clave = DIA.isoformat()
    trazas = {
        s: (
            sorted(t.fijados), sorted(t.bloqueadas), sorted(t.disparadas),
            sorted(t.no_implementadas), sorted(t.empates), sorted(t.anotaciones.items()),
        )
        for s, t in r.sesiones.items()
    }  # fmt: skip
    broker = motor.brokers[clave]
    ordenes = [
        (o.id, o.estado, o.precio, o.stop, o.objetivo, o.lotes, o.tipo, tuple(o.historial))
        for o in broker.ordenes.values()
    ]
    assert motor.cuenta is not None
    return (
        r.operaciones, trazas, tuple(motor.trazas_broker[clave].eventos), ordenes,
        motor.cuenta.saldo, motor.cuenta.equity,
    )  # fmt: skip


def _correr(motor: MotorCableado) -> tuple[Any, ...]:
    return _foto(motor, motor.correr_dia(_dia()))


def _sin_estado(motor: MotorCableado) -> MotorCableado:
    """El `toca_colocar_orden_limite` sintetico de `test_cableado.py` guarda en una clausura que ya
    dio SI, asi que solo coloca en la PRIMERA corrida del proceso. Para correr el mismo dia dos
    veces, uno sin estado: SI en MINUTO_ZONA y NO en el resto (el interprete no lo vuelve a
    disparar dentro del evento por la refraccion). Las primitivas reales se crean cada dia."""

    def toca(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        if int(momento.instante) == MINUTO_ZONA:
            return Resultado(Tri.SI, {"Z": "zona:1"})
        return Resultado(Tri.NO)

    predicados = dict(motor.primitivas_extra)
    predicados["toca_colocar_orden_limite"] = toca
    motor.primitivas_extra = predicados
    return motor


# ----------------------------------------------------------------- F2 · lo que decide no cambia


@pytest.mark.parametrize("ruta", [RUTA_STOP, RUTA_HUECO, RUTA_VIVA], ids=["stop", "hueco", "viva"])
def test_con_la_bitacora_el_motor_decide_lo_mismo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]], ruta: Mapping[int, int]
) -> None:
    sin = _correr(_motor(registro, vocabulario, _mercado(ruta)))
    con_motor = _motor(registro, vocabulario, _mercado(ruta))
    bitacora = decisiones.Bitacora(con_motor.reglas, {DIA.isoformat()})
    con_motor.observador = bitacora
    assert _correr(con_motor) == sin
    assert bitacora.eventos > 0 and bitacora.texto(DIA.isoformat())


def test_un_observador_que_muta_el_estado_hace_fallar_la_comparacion(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """La mutacion comprobada: un observador que enciende un freno un minuto antes de la zona
    cambia lo que el motor decide, y la foto lo ve."""
    sin = _correr(_motor(registro, vocabulario, _mercado(RUTA_STOP)))

    def muta(c: Cierre) -> None:
        if c.instante == MINUTO_ZONA - 1:
            c.estado.hechos["detenido_por_cartuchos"] = "hasta_cartuchos_reinicio"

    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    motor.observador = muta
    assert _correr(motor) != sin


def _con_dos_gates(motor: MotorCableado) -> None:
    """En MINUTO_ZONA, RN-009 dispara (zonas_desarrolladas_superan da SI) y RN-005 queda
    DESCONOCIDO (se_desarrolla_en_el_lado_de_ruido sin implementar): los dos prohiben
    abrir_operacion."""

    def superan(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        return Resultado(Tri.SI if int(momento.instante) == MINUTO_ZONA else Tri.NO)

    def ruido(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        if int(momento.instante) == MINUTO_ZONA:
            return NoImplementada("predicado:se_desarrolla_en_el_lado_de_ruido")
        return Resultado(Tri.NO)

    predicados = dict(motor.primitivas_extra)
    predicados.update(
        {"zonas_desarrolladas_superan": superan, "se_desarrolla_en_el_lado_de_ruido": ruido}
    )
    motor.primitivas_extra = predicados


def test_el_gate_que_dispara_y_el_desconocido_quedan_apuntados_los_dos(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    _con_dos_gates(motor)
    vistos: dict[int, Evento] = {}

    def ver(c: Cierre) -> None:
        vistos.setdefault(c.instante, c.evento)

    motor.observador = ver
    motor.correr_dia(_dia())
    ev = vistos[MINUTO_ZONA]
    clave = ("RN-015", "accion:colocar_orden_limite", "prohibida:abrir_operacion")
    assert clave in ev.bloqueadas
    assert ev.bloqueada_por[clave] == (("RN-009", "dispara"), ("RN-005", "desconocido"))
    assert ev.prohibido_por["abrir_operacion"] == ["RN-009"]
    assert "RN-005" in ev.quizas_por["abrir_operacion"]
    assert not motor.brokers[DIA.isoformat()].ordenes  # no se coloco nada


def test_la_bitacora_nombra_los_gates_de_cada_prohibicion(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
    _con_dos_gates(motor)
    bitacora = decisiones.Bitacora(motor.reglas, {DIA.isoformat()})
    motor.observador = bitacora
    motor.correr_dia(_dia())
    texto = bitacora.texto(DIA.isoformat())
    assert (
        "RN-015 no ejecuta accion:colocar_orden_limite (prohibida:abrir_operacion): la prohiben "
        "RN-009 [dispara], RN-005 [desconocido]" in texto
    )
    assert "SIN GATE REGISTRADO" not in texto
    assert "prohibido abrir_operacion por: RN-009 [dispara], RN-005 [desconocido]" in texto


def test_la_bitacora_es_determinista_y_va_etiquetada_sin_cifras_de_resultado(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    def texto() -> str:
        motor = _motor(registro, vocabulario, _mercado(RUTA_STOP))
        b = decisiones.Bitacora(motor.reglas, {DIA.isoformat()})
        motor.observador = b
        motor.correr_dia(_dia())
        return b.texto(DIA.isoformat())

    uno = texto()
    assert uno.encode("utf-8") == texto().encode("utf-8")
    lineas = uno.splitlines()
    assert lineas and all(ln.startswith(decisiones.PREFIJO_LINEA) for ln in lineas)
    assert not [ln for ln in lineas if PROHIBIDO_EN_LA_SALIDA.search(ln)]
    # la orden y su llenado salen, con la vela del llenado
    assert any("orden o1 (" in ln for ln in lineas)
    assert any("llenado de o1" in ln for ln in lineas)


def test_la_bitacora_no_mira_al_futuro(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    """Con el mercado cortado un minuto despues del llenado, las lineas hasta ese cierre son las
    mismas: ninguna lleva nada posterior a su instante."""
    corte_min = MINUTO_ZONA + 4
    corte_ms = corte_min * 60_000

    def lineas(hasta_ms: int | None) -> list[tuple[int, str]]:
        motor = _motor(registro, vocabulario, _mercado(RUTA_STOP, hasta_ms=hasta_ms))
        b = decisiones.Bitacora(motor.reglas, {DIA.isoformat()})
        motor.observador = b
        motor.correr_dia(_dia())
        return [x for x in b.lineas(DIA.isoformat()) if x[0] <= corte_min]

    completas = lineas(None)
    assert completas and completas == lineas(corte_ms)


# ------------------------------------------------------------------- F3 · ablacion y salida


def test_nombre_etiquetado_solo_admite_una_ambiguedad_tras_diagnostico_a() -> None:
    """En main, «DIAGNOSTICO-ABLACION-RN-007» salia en silencio como `aBLACION=RN-007`."""
    ruta = Path("x.txt")
    for mala in ("DIAGNOSTICO-ABLACION-RN-007", "DIAGNOSTICO-A-x", "DIAGNOSTICO-Ax-1"):
        with pytest.raises(ValueError, match="sin la forma esperada"):
            diagnostico.nombre_etiquetado(ruta, (mala,))
    assert diagnostico.nombre_etiquetado(
        ruta, ("DIAGNOSTICO-A35-inicio_vela_contraria", "DIAGNOSTICO-CUENTA-diaria")
    ) == Path("x.DIAGNOSTICO.a35=inicio_vela_contraria.cuenta=diaria.txt")


def test_la_carpeta_tiene_que_estar_dentro_de_data(tmp_path: Path) -> None:
    (tmp_path / "data").mkdir()
    assert (
        decisiones.comprobar_carpeta(tmp_path, tmp_path / "data" / "d")
        == (tmp_path / "data" / "d").resolve()
    )
    for mala in (
        tmp_path / "docs",
        tmp_path,
        tmp_path / "data" / "manifests" / "x",
        tmp_path / "data" / ".." / "x",
    ):
        with pytest.raises(decisiones.DecisionesError):
            decisiones.comprobar_carpeta(tmp_path, mala)


def test_los_ficheros_llevan_diagnostico_en_el_nombre() -> None:
    assert (
        decisiones.nombre_fichero("bitacora", "2026-07-03") == "bitacora.DIAGNOSTICO.2026-07-03.txt"
    )
    assert "DIAGNOSTICO" in decisiones.nombre_fichero("ablacion", "vigentes")
    with pytest.raises(decisiones.DecisionesError):
        decisiones.nombre_fichero("ablacion", "../x")


def _hijo(parser: argparse.ArgumentParser, nombre: str) -> argparse.ArgumentParser:
    """El subparser `nombre` de `parser`, leido del propio parser (no de --help)."""
    for accion in parser._actions:
        if isinstance(accion, argparse._SubParsersAction):
            return accion.choices[nombre]  # type: ignore[no-any-return]
    raise AssertionError(f"{parser.prog} sin subcomandos")


def test_el_subcomando_tiene_sus_opciones_y_ninguna_de_diagnostico_ni_de_simulacion() -> None:
    args = build_parser().parse_args(["motor", "decisiones", "--carpeta", "data/d"])
    sub = _hijo(_hijo(build_parser(), "motor"), "decisiones")
    largas = sorted(o for a in sub._actions for o in a.option_strings if o.startswith("--"))
    assert largas == [
        "--ablacion", "--ablacion-vigentes", "--bitacora", "--carpeta", "--help", "--meses",
    ]  # fmt: skip
    assert args.carpeta == "data/d" and not args.ablacion_vigentes
    with pytest.raises(SystemExit):
        build_parser().parse_args(["motor", "decisiones"])  # --carpeta es obligatoria


def test_un_id_que_no_es_vigente_se_nombra() -> None:
    reglas_spec = cargar_reglas(SPEC)
    reglas = reglas_ejecutables(reglas_spec)
    vigentes = decisiones.ids_vigentes(reglas_spec)
    descartada = next(r.id for r in reglas_spec if r.estado == "DESCARTADA")
    for mala in (descartada, "RN-999"):
        with pytest.raises(decisiones.DecisionesError, match=mala):
            decisiones.sin_regla(reglas, mala, vigentes)


def test_sin_ablacion_las_reglas_son_las_de_motor_arnes() -> None:
    reglas_spec = cargar_reglas(SPEC)
    reglas = reglas_ejecutables(reglas_spec)
    vigentes = decisiones.ids_vigentes(reglas_spec)
    assert decisiones.sin_regla(reglas, None, vigentes) == reglas
    assert len(vigentes) == len(reglas) == 32
    quitada = decisiones.sin_regla(reglas, "RN-016", vigentes)
    assert [r.id for r in quitada] == [r.id for r in reglas if r.id != "RN-016"]


def test_motor_nuevo_no_arrastra_nada_de_la_corrida_anterior(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    plantilla = _sin_estado(_motor(registro, vocabulario, _mercado(RUTA_STOP)))
    primera = _correr(plantilla)
    nuevo = decisiones.motor_nuevo(plantilla, plantilla.reglas)
    assert nuevo.cuenta is None and not nuevo.brokers and not nuevo.trazas_broker
    assert nuevo.mercados is plantilla.mercados  # de solo lectura, compartidos
    assert _correr(nuevo) == primera


def _trader() -> list[Operacion]:
    instante = datetime.fromtimestamp((MINUTO_ZONA + 3) * 60, UTC)
    return [Operacion(DIA.isoformat(), "07-11", "compra", instante, Decimal(ENTRADA) / ESCALA)]


def test_la_ablacion_del_control_da_cero_y_la_de_rn015_pierde_la_pareja(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    plantilla = _sin_estado(_motor(registro, vocabulario, _mercado(RUTA_STOP)))
    reglas_spec = cargar_reglas(SPEC)
    vigentes = decisiones.ids_vigentes(reglas_spec)
    dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), tuple(_trader())),)

    def correr(motor: MotorCableado) -> list[Operacion]:
        corrida = arnes.correr("x", ("2030-01",), dias, {DIA.isoformat(): _dia()}, motor)
        return [op for r in corrida.resultados for op in r.operaciones]

    # primero, solo la base: de ahi sale el control
    base = decisiones.correr_diagnostico(
        plantilla, plantilla.reglas, vigentes, correr, _trader(), _criterio().tolerancias,
        {DIA.isoformat()},
    )  # fmt: skip
    texto = base[decisiones.nombre_fichero("ablacion", "base")]
    linea = next(ln for ln in texto.splitlines() if "control (" in ln)
    control = [x for x in linea.split(": ")[-1].split(", ") if x.startswith("RN-")]
    assert control and "RN-015" not in control
    salida = decisiones.correr_diagnostico(
        plantilla, plantilla.reglas, vigentes, correr, _trader(), _criterio().tolerancias,
        (), (control[0], "RN-015"),
    )  # fmt: skip
    (nombre,) = [n for n in salida if n.startswith("ablacion.")]
    assert "DIAGNOSTICO" in nombre
    lineas = salida[nombre].splitlines()
    assert all(ln.startswith(decisiones.PREFIJO_LINEA) for ln in lineas)
    assert not [ln for ln in lineas if PROHIBIDO_EN_LA_SALIDA.search(ln)]
    assert any(f"[control] sin {control[0]} | sin delta" in ln for ln in lineas)
    assert any("[medida] sin RN-015 | pareja que se pierde" in ln for ln in lineas)
    assert any(
        "base repetida en el mismo proceso, sin bitacora" in ln and "igual: si" in ln
        for ln in lineas
    )
