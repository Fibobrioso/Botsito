"""Escenarios dentro de la sesion (ADR-0066, rama `feature/escenarios-por-sesion`), sobre dias y
velas SINTETICOS de 2030 y la spec REAL.

Los cuatro del encargo: dos sesiones independientes; una toma nueva tras una operacion cerrada abre
un escenario nuevo; la liquidez de la manana no vale para la tarde; y la orden viva al cambiar de
sesion, segun `orden_pendiente_al_abrir_sesion`. Y las piezas: la toma antes de la ventana (A-43),
los intentos con una toma nueva (A-25), los cartuchos del escenario y su reinicio."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
from botsito.domain.pivotes_m15 import ALTO, BAJO, CIERRE_VELA_CONTRARIA, Pivote
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import zonas
from botsito.engine.broker import CANCELADA
from botsito.engine.interprete import (
    EstadoDia,
    Momento,
    NoImplementada,
    ReglaEjecutable,
    Resultado,
    Tri,
    reglas_ejecutables,
)
from botsito.engine.llenado import OBJETIVO, STOP
from botsito.engine.motor import DatosMercado
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_orden_stop_pivote as tsp
from tests.unit import test_preparar_a35 as ta

RAIZ = Path(__file__).resolve().parents[2]
PARAMETROS = RAIZ / "knowledge" / "spec" / "parametros.yaml"
M0 = int(a_minuto(datetime(2030, 1, 15, 6, 0, tzinfo=UTC)))  # 07:00 Madrid en invierno
TARDE = M0 + 240  # 11:00 Madrid


def _registro(tmp_path: Path, **valores: str) -> Registro:
    """El registro real con los valores pedidos (en la linea `valor:` de cada parametro)."""
    actuales = {
        "toma_antes_de_la_ventana": "    valor: no_cuenta\n",
        "intentos_tras_toma_nueva": "    valor: vuelven_a_cartuchos_max\n",
        "orden_pendiente_al_abrir_sesion": "    valor: se_retira\n",
        "cartuchos_max": "    valor: 3\n",
        "orden_limite_nace": '    valor: "al_aparecer_punto_de_breaker"\n',
    }
    texto = PARAMETROS.read_text(encoding="utf-8")
    for nombre, valor in valores.items():
        bloque = texto.split(f"  - nombre: {nombre}\n", 1)
        assert len(bloque) == 2, nombre
        cabeza, cola = bloque[1].split("  - nombre: ", 1)
        assert cabeza.count(actuales[nombre]) == 1, nombre
        cabeza = cabeza.replace(actuales[nombre], f"    valor: {valor}\n")
        texto = f"{bloque[0]}  - nombre: {nombre}\n{cabeza}  - nombre: {cola}"
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(texto, encoding="utf-8")
    return cargar_registro(ruta)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(PARAMETROS)


@pytest.fixture(scope="module")
def reglas() -> list[ReglaEjecutable]:
    return list(reglas_ejecutables(cargar_reglas(ta.SPEC)))


# ------------------------------------------------------- la liquidez de la manana, en la tarde


def _m1_toma_al_final_de_la_manana() -> list[Vela]:
    """El dibujo de `test_preparar_a35` desplazado: la toma (B5) cae en el ultimo cuarto de hora de
    la manana (09:45Z-10:00Z) y despues el precio sigue bajando, sin vela contraria que forme otro
    BAJO, hasta pasadas las 11:00 (10:00Z). Es `anexos/ESCENARIOS-POR-SESION/puerta_de_atras.py`."""
    bloques: list[tuple[int, int, int | None]] = []
    precio = ta.BASE + 200
    for _ in range(9):
        bloques.append((precio, precio + 20, None))
        precio += 20
    bloques.append((precio, ta.BLOQUES[0][0], None))
    bloques += ta.BLOQUES
    ultimo = bloques[-1][1]
    for _ in range(6):
        bloques.append((ultimo, ultimo - 20, None))
        ultimo -= 20
    velas: list[Vela] = []
    n, precio = 0, bloques[0][0]
    while ta.INICIO + ta.M15 * n < ta.FIN:
        a, c, lo = bloques[n] if n < len(bloques) else (precio, precio + 5, None)
        velas += ta._bloque(n, a, c, lo)
        precio = c
        n += 1
    return velas


def _tomas(r: Any, sesion: str) -> list[int]:
    return [t for t, _, h, _ in r.sesiones[sesion].fijados if h == "liquidez_tomada"]


def test_la_liquidez_de_la_manana_no_vale_para_la_tarde(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """La toma de la manana y el precio todavia pasado a las 11:00, sobre el MISMO pivote: hasta
    ADR-0066 RN-004 la volvia a fijar en el primer minuto de la tarde (`cruza` mira donde cierra la
    ultima M1, no si cruza). Ahora la tarde no tiene toma: el pivote ya estaba tomado al abrirla."""
    m1 = _m1_toma_al_final_de_la_manana()
    datos = DatosMercado(
        ta._h4_alcista(),
        agregar(m1, ta.M15, registro.hora("anclaje_h4")),
        m1,
        CIERRE_VELA_CONTRARIA,
    )
    assert datos.liquidez_m15(TARDE - 10, BAJO) == datos.liquidez_m15(TARDE, BAJO)
    r = ta._motor(registro, reglas).correr_dia(ta._dia(datos))
    manana = _tomas(r, "07-11")
    assert manana and TARDE - 15 < min(manana) < TARDE
    assert _tomas(r, "11-15") == []
    assert "RN-004" not in r.sesiones["11-15"].disparadas


# --------------------------------------------------------- la toma antes de la ventana (A-43)


class _Datos:
    """Un pivote BAJO formado en `formado`, al nivel 1000, y M1 a medida: (inicio, cierre)."""

    def __init__(self, cierres: Mapping[int, int], formado: int) -> None:
        self.velas = [
            Vela(MinutoUtc(t), Puntos(c), Puntos(c + 1), Puntos(c - 1), Puntos(c), 1)
            for t, c in sorted(cierres.items())
        ]
        self.formado = formado

    def m1_entre(self, desde: int, hasta: int) -> list[Vela]:
        return [v for v in self.velas if desde <= int(v.inicio) < hasta]

    def ultima_m1_cerrada(self, instante: int) -> Vela | None:
        cerradas = [v for v in self.velas if int(v.fin) <= instante]
        return cerradas[-1] if cerradas else None

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        if lado != BAJO or instante < self.formado:
            return None
        return Pivote(BAJO, 1000, MinutoUtc(self.formado - 1), MinutoUtc(self.formado),
                      MinutoUtc(self.formado))  # fmt: skip


ARGS_DE_LA_SESION = {
    "que": "liquidez_m15",
    "criterio": "liquidez_m15_criterio_toma",
    "antes_de_la_ventana": "toma_antes_de_la_ventana",
}


def _de_la_sesion(registro: Registro, datos: _Datos, instante: int, desde: int) -> Any:
    f = primitivas_escritas(registro).predicados["la_toma_es_de_la_sesion"]
    estado = EstadoDia(hechos={"sesgo": "alcista"})
    sesion = "07-11" if desde == M0 else "11-15"
    return f(
        ARGS_DE_LA_SESION, Momento(MinutoUtc(instante), sesion, False, datos, desde, M0), estado
    )


def test_la_toma_antes_de_la_ventana_la_decide_el_parametro(tmp_path: Path) -> None:
    """Pivote formado a las 06:30 Madrid; el precio lo toma a las 06:45 y sigue debajo a las 07:05
    (A-43, pregunta 15 de la sesion 4). Con `no_cuenta` (el valor PROVISIONAL) no es toma de la
    sesion; con `cuenta`, si. Una toma DENTRO de la sesion vale con los dos."""
    antes = _Datos({M0 - 15: 990, M0 + 4: 985}, formado=M0 - 30)
    dentro = _Datos({M0 - 15: 1010, M0 + 4: 985}, formado=M0 - 30)
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    no_cuenta = _registro(tmp_path / "a")
    cuenta = _registro(tmp_path / "b", toma_antes_de_la_ventana="cuenta")
    assert _de_la_sesion(no_cuenta, antes, M0 + 5, M0) == Resultado(Tri.NO)
    assert _de_la_sesion(cuenta, antes, M0 + 5, M0) == Resultado(Tri.SI)
    for r in (no_cuenta, cuenta):
        assert _de_la_sesion(r, dentro, M0 + 5, M0) == Resultado(Tri.SI)
    # la M1 que cierra justo en la apertura (06:59-07:00) tambien es de antes
    en_la_apertura = _Datos({M0 - 1: 990, M0 + 4: 985}, formado=M0 - 30)
    assert _de_la_sesion(no_cuenta, en_la_apertura, M0 + 5, M0) == Resultado(Tri.NO)


def test_una_toma_de_la_sesion_anterior_no_cuenta_nunca(tmp_path: Path) -> None:
    """Tomada a las 10:30 y todavia debajo a las 11:05: no es de la tarde, con cualquier valor de
    `toma_antes_de_la_ventana` (A-46 RESUELTA, no una pregunta abierta)."""
    datos = _Datos({TARDE - 30: 990, TARDE + 4: 985}, formado=TARDE - 60)
    for r in (_registro(tmp_path), cargar_registro(PARAMETROS)):
        assert _de_la_sesion(r, datos, TARDE + 5, TARDE) == Resultado(Tri.NO)
    # sin los limites de la sesion en el Momento no hay nada que mirar
    f = primitivas_escritas(cargar_registro(PARAMETROS)).predicados["la_toma_es_de_la_sesion"]
    hecho_a_mano = Momento(MinutoUtc(TARDE + 5), "11-15", False, datos)
    estado = EstadoDia(hechos={"sesgo": "alcista"})
    assert f(ARGS_DE_LA_SESION, hecho_a_mano, estado) == Resultado(Tri.SI)


# ----------------------------------------------------------------------------- los escenarios


class _Liquidez:
    """La liquidez que se va tomando: `pivotes` dice, por instante, que pivote es la liquidez."""

    def __init__(self, pivotes: Mapping[int, Pivote]) -> None:
        self.pivotes = dict(sorted(pivotes.items()))

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None:
        vigente = None
        for t, p in self.pivotes.items():
            if t <= instante and p.lado == lado:
                vigente = p
        return vigente


def _pivote(nivel: int, formado: int, lado: str = ALTO) -> Pivote:
    return Pivote(lado, nivel, MinutoUtc(formado - 1), MinutoUtc(formado), MinutoUtc(formado))


ARGS_ESCENARIO = {"intentos": "intentos_tras_toma_nueva", "reinicio": "cartuchos_reinicio"}


def _abrir(registro: Registro, datos: Any, estado: EstadoDia, t: int, sesion: str) -> list[Any]:
    abrir = primitivas_escritas(registro).acciones["abrir_escenario"]
    return list(abrir(ARGS_ESCENARIO, {}, Momento(MinutoUtc(t), sesion, False, datos), estado))


def _estado_bajista() -> EstadoDia:
    return EstadoDia(hechos={"liquidez_tomada": "si", "sesgo": "bajista"})


def test_dos_sesiones_independientes_cada_una_con_sus_escenarios(registro: Registro) -> None:
    """La manana y la tarde llevan su propia lista de escenarios, aunque la liquidez sea la
    misma: lo de una no se arrastra a la otra (A-46)."""
    p = _pivote(1100, M0)
    datos = _Liquidez({M0: p})
    estado = _estado_bajista()
    _abrir(registro, datos, estado, M0 + 5, "07-11")
    _abrir(registro, datos, estado, TARDE + 5, "11-15")
    manana, tarde = (zonas.escenario_actual(estado, s) for s in ("07-11", "11-15"))
    assert manana is not None and tarde is not None and manana is not tarde
    assert manana["n"] == tarde["n"] == 1
    zonas.terminar(estado, "07-11", manana, zonas.TERMINADO_POR_GANANCIA)
    assert zonas.escenario_terminado(estado, "07-11")
    assert not zonas.escenario_terminado(estado, "11-15")


def test_una_toma_nueva_tras_una_ganadora_abre_un_escenario_nuevo(registro: Registro) -> None:
    """RN-034 termina el escenario de la ganadora; la MISMA liquidez, que RN-004 vuelve a fijar en
    cada M1 pasada la linea, no abre nada; una liquidez NUEVA abre el segundo, vivo."""
    p1, p2 = _pivote(1100, M0), _pivote(1150, M0 + 40)
    datos = _Liquidez({M0: p1, M0 + 40: p2})
    estado = _estado_bajista()
    _abrir(registro, datos, estado, M0 + 5, "07-11")
    primero = zonas.escenario_actual(estado, "07-11")
    assert primero is not None
    zonas.terminar(estado, "07-11", primero, zonas.TERMINADO_POR_GANANCIA)
    _abrir(registro, datos, estado, M0 + 20, "07-11")  # la misma liquidez, otra M1
    assert zonas.escenario_actual(estado, "07-11") is primero
    _abrir(registro, datos, estado, M0 + 45, "07-11")  # la toma de la liquidez nueva
    segundo = zonas.escenario_actual(estado, "07-11")
    assert segundo is not None and segundo is not primero and segundo["n"] == 2
    assert segundo["terminado"] is None and segundo["toma"]["nivel"] == 1150


@pytest.mark.parametrize(
    ("valor", "escenarios"), [("vuelven_a_cartuchos_max", 2), ("siguen_los_que_quedan", 1)]
)
def test_una_toma_nueva_con_el_escenario_vivo_la_decide_el_parametro(
    tmp_path: Path, valor: str, escenarios: int
) -> None:
    """A-25, pregunta 18: con el escenario vivo, una liquidez nueva abre otro (los intentos
    vuelven a `cartuchos_max`) o sigue el mismo sobre la toma nueva (siguen los que quedaban)."""
    reg = _registro(tmp_path, intentos_tras_toma_nueva=valor)
    datos = _Liquidez({M0: _pivote(1100, M0), M0 + 40: _pivote(1150, M0 + 40)})
    estado = _estado_bajista()
    _abrir(reg, datos, estado, M0 + 5, "07-11")
    zonas.escenario_actual(estado, "07-11")["zonas"].add("zona:1")  # type: ignore[index]
    _abrir(reg, datos, estado, M0 + 45, "07-11")
    todos = zonas.memoria_de_sesion(estado, "07-11")[zonas.ESCENARIOS]
    assert len(todos) == escenarios
    vigente = zonas.escenario_actual(estado, "07-11")
    assert vigente is not None and vigente["toma"]["nivel"] == 1150
    assert ("zona:1" in vigente["zonas"]) is (valor == "siguen_los_que_quedan")


def test_abrir_un_escenario_es_el_reinicio_de_los_cartuchos(registro: Registro) -> None:
    """`detenido_por_cartuchos` (RN-016) lo apaga la siguiente liquidez de M15, que es
    `cartuchos_reinicio`; con la misma liquidez sigue detenido."""
    datos = _Liquidez({M0: _pivote(1100, M0), M0 + 40: _pivote(1150, M0 + 40)})
    estado = _estado_bajista()
    _abrir(registro, datos, estado, M0 + 5, "07-11")
    estado.hechos["detenido_por_cartuchos"] = "hasta_cartuchos_reinicio"
    assert _abrir(registro, datos, estado, M0 + 20, "07-11") == []
    assert "detenido_por_cartuchos" in estado.hechos
    fijados = _abrir(registro, datos, estado, M0 + 45, "07-11")
    assert fijados == [("detenido_por_cartuchos", "no")]
    assert "detenido_por_cartuchos" not in estado.hechos


class _ConVelas(_Liquidez):
    """Las M1 de `test_orden_stop_pivote` (una venta con dos BAJOS) y la liquidez a medida."""

    def __init__(self, pivotes: Mapping[int, Pivote]) -> None:
        super().__init__(pivotes)
        self.velas = tsp._serie(tsp.VENTA_DOS_BAJOS)

    def m1_entre(self, desde: int, hasta: int) -> list[Vela]:
        return [v for v in self.velas if desde <= int(v.inicio) and int(v.fin) <= hasta]


def test_un_escenario_terminado_no_coloca_mas(registro: Registro) -> None:
    """El productor no liga zona en un escenario terminado, y si en el siguiente: con la orden en
    el punto (el valor del registro), sobre las M1 de `test_orden_stop_pivote`."""
    toca = zonas.primitivas_zona(registro, "solo_una_zona_de_control")["toca_colocar_orden_limite"]
    m0 = tsp.M0
    datos = _ConVelas({m0: _pivote(1100, m0), m0 + 4: _pivote(1150, m0 + 4)})
    estado = _estado_bajista()
    _abrir(registro, datos, estado, m0 + 1, "07-11")  # la toma en el cierre de la M1 0
    escenario = zonas.escenario_actual(estado, "07-11")
    assert escenario is not None
    zonas.terminar(estado, "07-11", escenario, zonas.TERMINADO_POR_GANANCIA)
    args = {"momento": "orden_limite_nace", "liga": "Z"}
    r = toca(args, Momento(MinutoUtc(m0 + 5), "07-11", False, datos), estado)  # ya hay punto
    assert r == Resultado(Tri.NO) and not isinstance(r, NoImplementada)
    # la toma de una liquidez nueva abre el siguiente, y ese si liga zona en cuanto hay punto
    _abrir(registro, datos, estado, m0 + 5, "07-11")
    r2 = toca(args, Momento(MinutoUtc(m0 + 9), "07-11", False, datos), estado)
    assert isinstance(r2, Resultado) and r2.valor is Tri.SI
    siguiente = zonas.escenario_actual(estado, "07-11")
    assert siguiente is not None and r2.ligaduras["Z"] in siguiente["zonas"]


def test_con_la_orden_en_el_esquema_el_escenario_tambien_manda(tmp_path: Path) -> None:
    """Revisor, a2: el escenario es de la sesion, no del productor de la orden, asi que con
    `orden_limite_nace` = `al_darse_el_esquema` un escenario terminado tampoco liga zona."""
    reg = _registro(tmp_path, orden_limite_nace='"al_darse_el_esquema"')
    toca = zonas.primitivas_zona(reg, "solo_una_zona_de_control")["toca_colocar_orden_limite"]
    datos = _ConVelas({tsp.M0: _pivote(1100, tsp.M0)})
    estado = _estado_bajista()
    _abrir(reg, datos, estado, tsp.M0 + 1, "07-11")
    escenario = zonas.escenario_actual(estado, "07-11")
    assert escenario is not None
    zonas.terminar(estado, "07-11", escenario, zonas.TERMINADO_POR_GANANCIA)
    args = {"momento": "orden_limite_nace", "liga": "Z"}
    r = toca(args, Momento(MinutoUtc(tsp.M0 + 9), "07-11", False, datos), estado)
    assert r == Resultado(Tri.NO)


# ------------------------------------------------------------ por el cableado: RN-034, RN-016


def _motor_con_escenario(
    registro: Registro, ruta: Mapping[int, int], con_cartuchos: bool = True
) -> Any:
    """El motor cableado de `test_cableado`, con la zona sintetica ligada a un escenario de la
    manana que la toca sintetica abre al colocar (el productor real necesita geometria)."""
    vocabulario = cargar_vocabulario(tc.SPEC)
    motor = tc._motor(registro, vocabulario, tc._mercado(ruta))
    predicados, acumuladores = tc._sinteticas()
    toca_sintetica = predicados["toca_colocar_orden_limite"]

    def toca(args: Mapping[str, Any], momento: Momento, estado: EstadoDia) -> Any:
        r = toca_sintetica(args, momento, estado)
        if isinstance(r, Resultado) and r.valor is Tri.SI:
            toma = {"instante": int(momento.instante), "nivel": tc.EXTREMO, "lado": "compra",
                    "pivote": (BAJO, tc.EXTREMO, int(momento.instante))}  # fmt: skip
            zonas._abrir(estado, momento.sesion, toma)["zonas"].add(r.ligaduras["Z"])
        return r

    predicados["toca_colocar_orden_limite"] = toca
    motor.primitivas_extra = predicados
    if con_cartuchos:
        acumuladores = {k: v for k, v in acumuladores.items() if k != "cartuchos"}
    motor.acumuladores_extra = acumuladores
    return motor


# la limite de compra se llena por el ASK (BID + spread): el BID baja a la entrada - 6, como en
# RUTA_VIVA de test_cableado, y despues sube hasta pasar el objetivo (+60)
RUTA_GANADORA = {tc.MINUTO_ZONA + 3: tc.ENTRADA - 6, tc.MINUTO_ZONA + 8: tc.ENTRADA + 70}


def test_por_el_cableado_la_ganadora_termina_su_escenario(registro: Registro) -> None:
    """RN-034 con la spec real: la orden se llena, llega al objetivo y el escenario de su zona
    termina; RN-017 dispara con ella (complementa)."""
    motor = _motor_con_escenario(registro, RUTA_GANADORA)
    r = motor.correr_dia(tc._dia())
    tb = motor.trazas_broker[tc.DIA.isoformat()]
    assert [t for _, t, _, _ in tb.eventos][-1] == OBJETIVO, tb.eventos
    assert {"RN-034", "RN-017"} <= r.sesiones["07-11"].disparadas
    escenario = zonas.escenario_actual(motor.estados[tc.DIA.isoformat()], "07-11")
    assert escenario is not None and escenario["terminado"] == zonas.TERMINADO_POR_GANANCIA


def test_por_el_cableado_tras_una_perdida_el_escenario_sigue_y_cuenta_el_intento(
    registro: Registro, tmp_path: Path
) -> None:
    """Con `cartuchos_max` = 3 el stop gasta un intento y el escenario sigue vivo; con 1, RN-016
    dispara por primera vez y deja `detenido_por_cartuchos` hasta la siguiente liquidez."""
    motor = _motor_con_escenario(registro, tc.RUTA_STOP)
    r = motor.correr_dia(tc._dia())
    assert [t for _, t, _, _ in motor.trazas_broker[tc.DIA.isoformat()].eventos][-1] == STOP
    estado = motor.estados[tc.DIA.isoformat()]
    escenario = zonas.escenario_actual(estado, "07-11")
    assert escenario is not None and escenario["terminado"] is None
    assert "RN-016" not in r.sesiones["07-11"].disparadas
    assert ("RN-016", "acumulador:cartuchos") not in r.sesiones["07-11"].no_implementadas
    uno = _motor_con_escenario(_registro(tmp_path, cartuchos_max="1"), tc.RUTA_STOP)
    r1 = uno.correr_dia(tc._dia())
    assert "RN-016" in r1.sesiones["07-11"].disparadas
    assert uno.estados[tc.DIA.isoformat()].hechos.get("detenido_por_cartuchos")


# ------------------------------------------------------------ la orden viva al cambiar de sesion


@pytest.mark.parametrize(
    ("valor", "retirada_en"),
    [
        ("se_retira", tc.FIN_H4 * 60_000 - 1),  # la apertura de la tarde, 11:00 Madrid
        ("sigue_hasta_ventana_fin", tc.MINUTO_FIN * 60_000 - 1),  # el fin del dia
    ],
)
def test_la_orden_viva_al_cambiar_de_sesion_segun_el_parametro(
    tmp_path: Path, valor: str, retirada_en: int
) -> None:
    """La orden de la manana no se llena (el precio no baja a la entrada). Con `se_retira`
    (PROVISIONAL, pregunta 5) RN-035 la retira en la apertura de la tarde; con
    `sigue_hasta_ventana_fin`, lo de antes, sigue viva hasta que el cableado la cancela al final
    del dia."""
    reg = _registro(tmp_path, orden_pendiente_al_abrir_sesion=valor)
    motor = tc._motor(reg, cargar_vocabulario(tc.SPEC), tc._mercado({}))
    r = motor.correr_dia(tc._dia())
    o1 = motor.brokers[tc.DIA.isoformat()].ordenes["o1"]
    assert o1.estado == CANCELADA and o1.ultimo_cambio_ms == retirada_en
    assert ("RN-035" in r.sesiones["11-15"].disparadas) is True
