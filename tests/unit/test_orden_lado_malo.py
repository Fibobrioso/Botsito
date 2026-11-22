"""La orden stop cuyo 0 queda del lado malo ESPERA (ADR-0097; A-59, lectura del consultor;
`orden_stop_lado_malo` = `espera`, DEFAULT_AMBIGUOUS). Rama `trabajo/activar-sesion-08`, F2.

Cuando la cotizacion del cierre deja el 0 del lado malo (una compra stop por debajo del ask, una
venta stop por encima del bid: la misma `lado_equivocado` con la misma `Mercado.cotizacion` con la
que rechaza el broker, ADR-0057 §4), la orden NO se envia -ninguna peticion-, la caja no queda usada
y el punto no se gasta; RN-011 y RN-015 la vuelven a preparar en el cierre siguiente y se envia en
el primero en que el 0 quede del lado bueno. Con `se_gasta_el_punto` (lo de antes de esta rama), el
broker la rechaza (`precio_invalido`) y el rechazo gasta el punto (ADR-0083 D1).

Por el CABLEADO REAL y la spec real, con dias SINTETICOS de 2030 (la infraestructura de
`test_punto_usado`: el productor real de la zona salvo `zona_del_punto`), en compra y en venta. Y
uno por el camino real, sobre la sesion de 2026-07-08 de 11 a 15 (construccion), que en la corrida
de julio de la base tiene un rechazo por `precio_invalido` al colocar (ACTIVAR-SESION-08.md, 0.5):
necesita las M1 y los ticks de `data/`, fuera de git; sin ellos (la CI), se salta.

En `main` fallan los que esperan: alli la orden se envia, el broker la rechaza y el punto queda
gastado (los recuentos, en el informe de la rama)."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.estructura_m1 import PRIMER_ESQUEMA
from botsito.domain.pivotes_m15 import ALTO, BAJO, Pivote
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import cableado, primitivas_broker, zonas
from botsito.engine.broker import (
    COLOCADA,
    MOTIVO_PRECIO_INVALIDO,
    PETICION_COLOCAR,
    RECHAZADA,
)
from botsito.engine.entrada import STOP_EN_RUPTURA
from botsito.engine.interprete import EstadoDia, Momento, Resultado, Tri
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.zonas import Zona
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_escenarios_por_sesion as te
from tests.unit import test_punto_usado as tp

RAIZ = tc.RAIZ
DIA = tp.DIA
SESION = tp.SESION
Z = tp.Z
E = tp.E
TOMA = tp.TOMA
MS = tp.MS
PARAMETRO = "orden_stop_lado_malo"


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _h4_bajista() -> list[Vela]:
    """Tres H4 rojas cerradas antes de la ventana; la ultima rompe la minima de la anterior y
    cierra roja: bajista (el espejo de `test_cableado._h4_alcista`)."""
    inicio = int(a_minuto(datetime(2030, 1, 14, 10, 0, tzinfo=UTC)))
    base = tc.BASE
    velas = []
    niveles = [(base + 100, base + 300), (base + 50, base + 200), (base - 20, base + 150)]
    for i, (lo, hi) in enumerate(niveles):
        m = inicio + 240 * i
        velas.append(
            Vela(
                MinutoUtc(m), Puntos(hi - 10), Puntos(hi), Puntos(lo), Puntos(lo + 10), 1, 240, 240
            )
        )
    return velas


class _Datos(DatosMercado):
    """Como `test_punto_usado._Datos`, con el lado de la liquidez: un BAJO por debajo del punto
    para una compra, un ALTO por encima para una venta, tomado en TOMA."""

    def __init__(self, h4: Any, m1: Any, lado: str) -> None:
        super().__init__(h4, velas_m1=m1)
        self.lado = lado

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        if self.lado == "compra":
            return te._pivote(tc.BASE - 50, TOMA - 30, BAJO) if lado == BAJO else None
        return te._pivote(tc.BASE + 50, TOMA - 30, ALTO) if lado == ALTO else None


def _geometria(lado: str, extremo: int) -> Callable[..., Zona | None]:
    """`zona_del_punto` sintetico, una sola caja todo el dia desde Z (`test_punto_usado._geometria`
    con el lado)."""
    punto = tp.PUNTO

    def zona_del_punto(registro: Registro, momento: Momento, estado: EstadoDia) -> Zona | None:
        if momento.sesion != SESION:
            return None
        if zonas._anotar_toma(momento.datos, momento, estado) is None:
            return None
        if int(momento.instante) < Z:
            return None
        mem = zonas._de_la_sesion(estado, momento.sesion)
        puntos = mem.setdefault("puntos", {})
        del_dia = zonas._memoria(estado).setdefault("zonas", {})
        clave = f"{punto}#{extremo}"
        id = puntos.get(clave)
        if id is None:
            id = f"{zonas.PREFIJO_ZONA}{len(del_dia) + 1}"
            puntos[clave] = id
            mem.setdefault("punto_de_zona", {})[id] = punto
            zonas._ligar_al_escenario(estado, momento.sesion, id)
            del_dia[id] = Zona(id, lado, E, extremo, PRIMER_ESQUEMA, tp.VELA_CONTRARIA, Z)
        return del_dia[id]  # type: ignore[no-any-return]

    return zona_del_punto


def _correr(
    registro: Registro,
    lado: str,
    ruta: Mapping[int, int],
    monkeypatch: pytest.MonkeyPatch,
) -> Any:
    """Un dia por el cableado real, como `test_punto_usado._correr`, en el lado pedido."""
    vocabulario = cargar_vocabulario(tc.SPEC)
    mercado = tc._mercado(ruta)
    motor = tc._motor(registro, vocabulario, mercado)
    motor.limpia = "solo_una_zona_de_control"
    motor.tipo_orden = STOP_EN_RUPTURA
    motor.zonas_de = None
    predicados, acumuladores = tc._sinteticas()
    for real in ("toca_colocar_orden_limite", "se_completa_zona_de_control"):
        del predicados[real]
    del acumuladores["cartuchos"]

    def toma(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI if int(momento.instante) == TOMA else Tri.NO)

    def si(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.SI)

    predicados.update({"alcanza_nivel": toma, "cruza": toma, "la_toma_es_de_la_sesion": si})
    motor.primitivas_extra = predicados
    motor.acumuladores_extra = acumuladores
    extremo = tp.CAJA if lado == "compra" else E + 20
    geometria = _geometria(lado, extremo)
    monkeypatch.setattr(zonas, "zona_del_punto", geometria)
    monkeypatch.setattr(primitivas_broker, "zona_del_punto", geometria)
    h4 = tc._h4_alcista() if lado == "compra" else _h4_bajista()
    datos = _Datos(h4, list(mercado.m1), lado)
    motor.correr_dia(DiaDeMercado(tc.DIA, tc.HUSO, tc.SESIONES, datos))
    return motor


# El precio (BID de cierre por minuto). COMPRA: por encima del punto desde Z-5 (la compra stop en E
# queda por debajo del ask: del lado malo) y por debajo desde Z+3 (vale). VENTA: el espejo.
COMPRA_VUELVE = {Z - 5: E + 10, Z + 3: E - 10}
COMPRA_NO_VUELVE = {Z - 5: E + 10}
VENTA_VUELVE = {Z - 5: E - 10, Z + 3: E + 10}
VENTA_NO_VUELVE = {Z - 5: E - 10}


def test_el_registro_dice_espera_por_defecto_bajo_a59(registro: Registro) -> None:
    p = registro.parametros[PARAMETRO]
    assert p.valor == "espera" and p.ambiguedad_id == "A-59"
    assert p.estado.name == "DEFAULT_AMBIGUOUS"


@pytest.mark.parametrize(("lado", "ruta"), [("compra", COMPRA_VUELVE), ("venta", VENTA_VUELVE)])
def test_si_el_precio_vuelve_la_orden_se_coloca_en_el_primer_cierre_en_que_vale(
    registro: Registro, lado: str, ruta: Mapping[int, int], monkeypatch: pytest.MonkeyPatch
) -> None:
    """En Z el 0 queda del lado malo: no se envia (ninguna peticion, ningun rechazo), la caja no
    queda usada y el punto no se gasta. Cuando el precio vuelve, la MISMA zona se coloca en el
    primer cierre en que la cotizacion deja el 0 del lado bueno. En `main`, rechazo y punto
    gastado."""
    motor = _correr(registro, lado, ruta, monkeypatch)
    broker = motor.brokers[DIA]
    assert not broker.traza().rechazos, broker.traza().rechazos
    ordenes = list(broker.ordenes.values())
    assert len(ordenes) == 1, ordenes
    o = ordenes[0]
    assert o.lado == lado and o.precio == E and o.historial[0][1] == COLOCADA
    # el precio cambia de lado en la M1 que empieza en Z+3: su ultimo tick (a los 40 s) es lo que
    # ve la cotizacion en el cierre de esa M1, el de Z+4, que es el primero en que vale
    assert o.colocada_ms == tp._cierre(Z + 4)
    assert broker.lado_equivocado_al_colocar("stop", lado, E, tp._cierre(Z + 3))  # aun no
    assert not broker.lado_equivocado_al_colocar("stop", lado, E, o.colocada_ms)  # ya vale
    estado = motor.estados[DIA]
    assert not zonas.punto_rechazado(estado, SESION, "zona:1")
    tb = motor.trazas_broker[DIA]
    (espera,) = tb.esperas
    desde_ms, zona_id, orden_id = espera
    assert (zona_id, orden_id) == ("zona:1", o.id) and desde_ms == tp._cierre(Z)
    assert [p.tipo for p in tb.peticiones][0] == PETICION_COLOCAR


@pytest.mark.parametrize(
    ("lado", "ruta"), [("compra", COMPRA_NO_VUELVE), ("venta", VENTA_NO_VUELVE)]
)
def test_si_el_precio_no_vuelve_no_hay_orden_ni_peticion(
    registro: Registro, lado: str, ruta: Mapping[int, int], monkeypatch: pytest.MonkeyPatch
) -> None:
    motor = _correr(registro, lado, ruta, monkeypatch)
    broker = motor.brokers[DIA]
    assert not broker.ordenes and not broker.traza().rechazos
    tb = motor.trazas_broker[DIA]
    assert not tb.peticiones
    assert [(z, o) for _, z, o in tb.esperas] == [("zona:1", None)]
    assert not zonas.punto_rechazado(motor.estados[DIA], SESION, "zona:1")
    texto = cableado.informe_simulacion(motor)
    assert cableado.CABECERA_ESPERAS in texto and "esperas: 1 (enviadas despues: 0)" in texto


def test_con_se_gasta_el_punto_el_broker_la_rechaza_y_el_punto_queda_gastado(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La otra opcion de A-59, lo de antes de esta rama (ADR-0083 D1; la decision 1 de ADR-0064)."""
    motor = _correr(tc._registro_se_gasta(tmp_path), "compra", COMPRA_VUELVE, monkeypatch)
    broker = motor.brokers[DIA]
    assert [(o.id, o.estado) for o in broker.ordenes.values()] == [("o1", RECHAZADA)]
    assert broker.traza().rechazos[0].motivo == MOTIVO_PRECIO_INVALIDO
    assert zonas.punto_rechazado(motor.estados[DIA], SESION, "zona:1")
    assert not motor.trazas_broker[DIA].esperas


def test_el_broker_y_la_espera_miran_la_misma_cotizacion(
    registro: Registro, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La comprobacion previa es la del broker (`lado_equivocado_al_colocar`, que usa
    `_precio_infringido`), no una copia: con la espera apagada, el broker rechaza justo en el cierre
    en que, con la espera encendida, la orden no se envia."""
    motor = _correr(registro, "compra", COMPRA_VUELVE, monkeypatch)
    broker = motor.brokers[DIA]
    assert broker.lado_equivocado_al_colocar("stop", "compra", E, tp._cierre(Z))
    o = next(iter(broker.ordenes.values()))
    assert not broker.lado_equivocado_al_colocar("stop", "compra", E, o.colocada_ms)


# ------------------------------------------------------------------- por el camino real (julio)


def _motor_julio(dia: str) -> Any:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.dataset import DatasetError
    from botsito.engine import arnes, diagnostico, entrada, tope_trader
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.engine.relojes import reloj_de_las_sesiones
    from botsito.spec.modelo import cargar_reglas

    spec = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    dias = [d for d in arnes.dias_de_construccion(RAIZ, criterio, [dia[:7]]) if d.dia == dia]
    assert len(dias) == 1, f"{dia} no es un dia dev de construccion"
    diag = diagnostico.Diagnostico()
    lectura = diagnostico.lectura_pivote(registro, diag)
    perfil = cableado.perfil_del_repo(RAIZ, None)
    try:
        mercado = arnes.dias_de_mercado(
            RAIZ, carpeta_datos(RAIZ), config, registro, dias,
            reloj_de_las_sesiones(registro), lectura,
        )  # fmt: skip
        motor = cableado.construir_motor_cableado(
            RAIZ, carpeta_datos(RAIZ), criterio, config, registro, cargar_vocabulario(spec),
            reglas_ejecutables(cargar_reglas(spec)), dias, perfil, None, False,
            tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag),
            zonas.lectura_limpia(registro), stops_level_diagnostico=None,
            tipo_orden=entrada.lectura_tipo_orden(registro, None),
        )  # fmt: skip
    except (DatasetError, FileNotFoundError, OSError) as exc:
        pytest.skip(f"sin las M1 o los ticks de data/: {exc}")
    arnes.correr(cableado.NOMBRE_MOTOR, (dia[:7],), dias, mercado, motor)
    return motor


def test_por_el_camino_real_el_8_de_julio_no_hay_rechazo_por_precio_invalido_al_colocar() -> None:
    """2026-07-08 (construccion): en la corrida de julio de la base, la orden o15 de la sesion de 11
    a 15 sale rechazada por `precio_invalido` al colocar (ACTIVAR-SESION-08.md, 0.5). Con la
    espera, ningun rechazo por precio al colocar en el dia, y la espera queda anotada. Rompe en
    `main`."""
    motor = _motor_julio("2026-07-08")
    dia = "2026-07-08"
    rechazos = [
        r for r in motor.brokers[dia].traza().rechazos if r.motivo == MOTIVO_PRECIO_INVALIDO
    ]
    assert not rechazos, rechazos
    assert motor.trazas_broker[dia].esperas
