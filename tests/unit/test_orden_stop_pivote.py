"""La vida de la orden stop con la caja por operacion (ADR-0064; ADR-0056 §7, rama
`feature/F35-orden-stop-pivote`) sobre velas SINTETICAS de 2030: el punto de ruptura y la caja
son las funciones de R5 y de R6, R4 y R1 de CAJA-77; el productor liga una zona por punto y no
repite un punto usado; RN-008 no frena la colocacion con la orden en el punto; y por el cableado
real, la cadena colocada, cancelada y recolocada en el punto nuevo, llenada."""

from __future__ import annotations

import importlib.util
import random
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.estructura_m1 import (
    BLOQUE_R1,
    BLOQUE_R4,
    BLOQUE_R6,
    COMPRA,
    VENTA,
    extremo_de_la_caja,
    ultimo_punto_de_ruptura,
)
from botsito.domain.pivotes_m15 import Pivote
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import cableado, zonas
from botsito.engine.broker import CANCELADA, LLENADA, PETICION_CANCELAR, PETICION_COLOCAR
from botsito.engine.interprete import EstadoDia, Momento, NoImplementada, Resultado, Tri
from botsito.engine.llenado import OBJETIVO

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "knowledge" / "spec" / "parametros.yaml"
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))


def _cargar(nombre: str) -> ModuleType:
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _vela(k: int, o: int, h: int, lo: int, c: int) -> Vela:
    return Vela(MinutoUtc(M0 + k), Puntos(o), Puntos(h), Puntos(lo), Puntos(c), 1)


def _serie(cierres: list[int]) -> list[Vela]:
    velas, abre = [], cierres[0]
    for k, c in enumerate(cierres):
        velas.append(_vela(k, abre, max(abre, c) + 1, min(abre, c) - 1, c))
        abre = c
    return velas


def _registro(tmp_path: Path, **valores: str) -> Registro:
    """El registro real con los valores pedidos para los parametros de ADR-0064."""
    texto = PARAMETROS.read_text(encoding="utf-8")
    actuales = {
        "orden_limite_nace": '    valor: "al_aparecer_punto_de_breaker"\n',
        "orden_stop_punto": "    valor: ultimo_pivote_m1\n",
        "caja_bloque": "    valor: r6\n",
    }
    for nombre, valor in valores.items():
        viejo = actuales[nombre]
        assert texto.count(viejo) == 1, nombre
        texto = texto.replace(viejo, f'    valor: "{valor}"\n')
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return cargar_registro(ruta)


# ------------------------------------------------------------------------------ el dominio


# una bajada, un rebote verde (marca un BAJO), otra bajada y otro rebote (marca un BAJO mas bajo)
VENTA_DOS_BAJOS = [1000, 990, 980, 985, 990, 975, 965, 970, 972]


def test_el_punto_es_el_ultimo_bajo_en_una_venta_y_se_actualiza() -> None:
    velas = _serie(VENTA_DOS_BAJOS)
    primero = ultimo_punto_de_ruptura(velas[:5], VENTA)
    ultimo = ultimo_punto_de_ruptura(velas, VENTA)
    assert primero is not None and ultimo is not None
    assert ultimo.nivel < primero.nivel  # el pivote nuevo es mas bajo, y manda el ultimo
    assert int(velas[ultimo.marca].minima) == ultimo.nivel
    # con `hasta`, el de las velas hasta ahi: el de la referencia de la toma
    assert ultimo_punto_de_ruptura(velas, VENTA, hasta=5) == primero
    # en una compra se busca un ALTO: la serie invertida da el simetrico
    espejo = _serie([2000 - c for c in VENTA_DOS_BAJOS])
    alto = ultimo_punto_de_ruptura(espejo, COMPRA)
    assert alto is not None and alto.nivel == 2000 - ultimo.nivel


def test_la_caja_de_r6_r4_y_r1() -> None:
    velas = _serie(VENTA_DOS_BAJOS)
    p = ultimo_punto_de_ruptura(velas, VENTA)
    assert p is not None
    r6 = extremo_de_la_caja(velas, VENTA, p, BLOQUE_R6)
    assert r6 == max(int(v.maxima) for v in velas[p.marca :])
    ultima_verde = max(k for k, v in enumerate(velas) if v.cierre > v.abierta)
    r1 = extremo_de_la_caja(velas, VENTA, p, BLOQUE_R1)
    assert r1 == int(velas[ultima_verde].maxima)
    r4 = extremo_de_la_caja(velas, VENTA, p, BLOQUE_R4)
    assert r4 is not None and r4 >= r1  # el tramo contiene a la ultima contraria
    # una caja sin altura del lado del stop no se traza
    plana = [_vela(0, 100, 100, 100, 100)]
    from botsito.domain.estructura_m1 import PuntoDeRuptura

    assert (
        extremo_de_la_caja(plana, VENTA, PuntoDeRuptura(100, MinutoUtc(M0), 0), BLOQUE_R6) is None
    )


@pytest.mark.parametrize("lado", [VENTA, COMPRA])
def test_son_las_funciones_de_r5_y_r6_de_caja_77(lado: str) -> None:
    """El productor usa lo que CAJA-77 midio: sobre series al azar, el punto y el 0 de R5, y el 1
    de R6, R4 y R1, salen iguales que en scripts/bloque_de_la_caja.py."""
    bc = _cargar("bloque_de_la_caja")
    azar = random.Random(7)
    for _ in range(60):
        cierres = [1000]
        for _ in range(40):
            cierres.append(cierres[-1] + azar.randint(-6, 6))
        velas = _serie(cierres)
        p = ultimo_punto_de_ruptura(velas, lado)
        r5 = bc.r5(velas, lado)
        assert (p is None) == (r5 is None)
        if p is None:
            continue
        assert p.nivel == r5[0]
        for bloque, regla in ((BLOQUE_R6, bc.r6), (BLOQUE_R4, bc.r4), (BLOQUE_R1, bc.r1)):
            uno = extremo_de_la_caja(velas, lado, p, bloque)
            caja = regla(velas, lado)
            del_lado = caja is not None and (
                caja[1] > p.nivel if lado == VENTA else caja[1] < p.nivel
            )
            assert uno == (caja[1] if del_lado else None), (bloque, cierres)


# ---------------------------------------------------------------------------- el productor


class _Datos:
    def __init__(self, velas: list[Vela], toma: int) -> None:
        self.velas, self.toma = velas, toma

    def m1_entre(self, desde: int, hasta: int) -> list[Vela]:
        return [v for v in self.velas if desde <= int(v.inicio) and int(v.fin) <= hasta]

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        return Pivote(lado, 1010, MinutoUtc(M0), MinutoUtc(M0 + 1), MinutoUtc(M0 + 1))


def _momento(datos: _Datos, k: int) -> Momento:
    return Momento(MinutoUtc(M0 + k + 1), "07-11", False, datos)  # el cierre de la M1 k


def _estado() -> EstadoDia:
    e = EstadoDia()
    e.hechos.update({"liquidez_tomada": "si", "sesgo": "bajista"})
    return e


def test_el_productor_liga_una_zona_por_punto_y_no_repite_un_punto_usado(tmp_path: Path) -> None:
    reg = _registro(tmp_path)
    toca = zonas.primitivas_zona(reg, "solo_una_zona_de_control")["toca_colocar_orden_limite"]
    datos = _Datos(_serie(VENTA_DOS_BAJOS), toma=M0 + 1)
    estado = _estado()
    args = {"momento": "orden_limite_nace", "liga": "Z"}
    # la toma es la primera vez que el productor ve el hecho encendido: en el cierre de la M1 0
    assert toca(args, _momento(datos, 0), estado) == Resultado(Tri.NO)  # aun no hay punto
    r = toca(args, _momento(datos, 4), estado)
    assert isinstance(r, Resultado) and r.valor is Tri.SI
    z1 = zonas.zonas_del_dia(estado)[r.ligaduras["Z"]]
    assert z1.lado == VENTA and z1.extremo > z1.entrada and z1.por == "primer_esquema"
    # idempotente en el mismo instante; y una vez usada, no se vuelve a colocar
    assert toca(args, _momento(datos, 4), estado) == r
    zonas.marcar_usada(estado, "07-11", z1.id)
    assert toca(args, _momento(datos, 5), estado) == Resultado(Tri.NO)
    # el punto nuevo liga una zona nueva
    r2 = toca(args, _momento(datos, 8), estado)
    assert isinstance(r2, Resultado) and r2.valor is Tri.SI and r2.ligaduras["Z"] != z1.id
    assert zonas.zonas_del_dia(estado)[r2.ligaduras["Z"]].entrada < z1.entrada


def test_con_la_referencia_de_la_toma_el_punto_no_se_mueve(tmp_path: Path) -> None:
    reg = _registro(tmp_path, orden_stop_punto="referencia_de_la_toma")
    datos = _Datos(_serie(VENTA_DOS_BAJOS), toma=M0 + 5)
    estado = _estado()
    # la toma se anota en el cierre de la M1 4 (instante M0 + 5)
    z_toma = zonas.zona_del_punto(reg, _momento(datos, 4), estado)
    z_despues = zonas.zona_del_punto(reg, _momento(datos, 8), estado)
    assert z_toma is not None and z_despues is not None and z_toma.id == z_despues.id


def test_rn008_no_frena_con_la_orden_en_el_punto(tmp_path: Path) -> None:
    for valor, esperado in (
        ("al_aparecer_punto_de_breaker", Tri.SI),
        ("al_darse_el_esquema", Tri.NO),
    ):
        reg = _registro(tmp_path, orden_limite_nace=valor)
        f = zonas.primitivas_zona(reg, "solo_una_zona_de_control")[
            "la_orden_nace_antes_del_esquema"
        ]
        r = f({"momento": "orden_limite_nace"}, _momento(_Datos([], M0), 0), EstadoDia())
        assert r == Resultado(esperado)


# ------------------------------------------------------------- de punta a punta, por el cableado


def test_la_cadena_colocada_cancelada_recolocada_y_llenada_por_el_cableado(
    tmp_path: Path,
) -> None:
    """ADR-0056 §7 por el cableado real y la spec real (RN-006, RN-008, RN-011, RN-015): la
    orden stop nace en el punto A sin esquema (RN-008 no frena), se forma el punto B, RN-006 la
    cancela y RN-011 y RN-015 la recolocan en B en el MISMO cierre de M1, con su caja; el precio
    rompe B, se llena y llega al objetivo. El contador de peticiones lo ve: colocar, cancelar,
    colocar. La geometria de los puntos es sintetica; la marca de usada es la del productor."""
    tc = _cargar_test_cableado()
    reg = _registro(tmp_path)
    from botsito.spec.modelo import cargar_vocabulario

    vocabulario = cargar_vocabulario(tc.SPEC)
    entrada_a, entrada_b = tc.ENTRADA, tc.ENTRADA - 4
    a = cableado.zona_sintetica("zona:1", "compra", entrada_a, entrada_a - 20, "primer_esquema")
    b = cableado.zona_sintetica("zona:2", "compra", entrada_b, entrada_b - 20, "primer_esquema")
    ruta = {
        tc.MINUTO_ZONA - 5: tc.ENTRADA - 10,
        tc.MINUTO_ZONA + 3: tc.ENTRADA + 5,
        tc.MINUTO_ZONA + 8: tc.ENTRADA + 70,
    }
    motor = tc._motor(reg, vocabulario, tc._mercado(ruta))
    motor.limpia = "solo_una_zona_de_control"
    motor.tipo_orden = "stop_en_ruptura"
    motor.stops_level_diagnostico = 2
    motor.zonas_de = lambda md: {"zona:1": a, "zona:2": b}
    predicados, _ = tc._sinteticas()
    nuevo = tc.MINUTO_ZONA + 1

    def toca(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        if momento.sesion != "07-11":  # la geometria sintetica solo tiene toma en esta sesion
            return Resultado(Tri.NO)
        usadas = zonas.zonas_usadas(estado, momento.sesion)
        t = int(momento.instante)
        z = "zona:1" if tc.MINUTO_ZONA <= t < nuevo else ("zona:2" if t >= nuevo else None)
        if z is None or z in usadas:
            return Resultado(Tri.NO)
        return Resultado(Tri.SI, {"Z": z})

    def completa(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        if "posterior_a" in args:
            return Resultado(Tri.NO)
        usadas = zonas.zonas_usadas(estado, momento.sesion)
        if int(momento.instante) >= nuevo and "zona:1" in usadas and "zona:2" not in usadas:
            return Resultado(Tri.SI, {"Z": "zona:2"})
        return Resultado(Tri.NO)

    def sin_esquema(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        return Resultado(Tri.NO)  # sin ninguno de los esquemas: RN-008 frenaria sin ADR-0064

    predicados.update(
        {
            "toca_colocar_orden_limite": toca,
            "se_completa_zona_de_control": completa,
            "se_da_esquema": sin_esquema,
        }
    )
    motor.primitivas_extra = predicados
    motor.correr_dia(tc._dia())
    broker = motor.brokers[tc.DIA.isoformat()]
    o1, o2 = broker.ordenes["o1"], broker.ordenes["o2"]
    assert (o1.precio, o1.estado) == (entrada_a, CANCELADA)
    assert o2.precio == entrada_b and o2.colocada_ms == o1.ultimo_cambio_ms  # mismo cierre
    assert (o2.stop, o2.objetivo) == (entrada_b - 16, entrada_b + 60)  # su propia caja
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert [t for _, t, _, _ in tb.eventos] == [LLENADA, OBJETIVO], tb.eventos
    assert [(p.tipo, p.id) for p in tb.peticiones] == [
        (PETICION_COLOCAR, "o1"),
        (PETICION_CANCELAR, "o1"),
        (PETICION_COLOCAR, "o2"),
    ], [(o.id, o.precio, o.estado, o.colocada_ms, o.historial) for o in broker.ordenes.values()]
    # con la orden en el esquema, RN-008 frena: sin esquema no se coloca nada
    antes = tc._motor(
        _registro(tmp_path, orden_limite_nace="al_darse_el_esquema"), vocabulario, tc._mercado(ruta)
    )
    antes.limpia, antes.tipo_orden, antes.stops_level_diagnostico = (
        motor.limpia,
        motor.tipo_orden,
        2,
    )
    antes.zonas_de = motor.zonas_de
    antes.primitivas_extra = predicados
    antes.correr_dia(tc._dia())
    assert not antes.brokers[tc.DIA.isoformat()].ordenes


def _cargar_test_cableado() -> ModuleType:
    from tests.unit import test_cableado

    return test_cableado


def test_con_la_orden_en_el_esquema_rn006_sigue_sin_escribirse(tmp_path: Path) -> None:
    """Sin `posterior_a` y con la orden en el esquema, RN-006 sigue sin escribirse."""
    from botsito.engine.primitivas_broker import ContextoDia, primitivas_cableadas

    reg = _registro(tmp_path, orden_limite_nace="al_darse_el_esquema")
    ctx = ContextoDia.__new__(ContextoDia)
    p = primitivas_cableadas(reg, ctx, "solo_una_zona_de_control")
    r = p.predicados["se_completa_zona_de_control"](
        {"criterio": "zona_control_criterio_completada"}, _momento(_Datos([], M0), 0), EstadoDia()
    )
    assert isinstance(r, NoImplementada)
