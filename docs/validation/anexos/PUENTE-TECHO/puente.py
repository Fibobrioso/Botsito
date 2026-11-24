"""El puente del techo de ADR-0099: el techo de ADR-0098 §1 con una pieza cambiada cada vez.

Rama `trabajo/puente-techo` (PUENTE-TECHO.md). Pre-registrado en `613aa40c` (ADR-0099 y
`docs/plan/PUENTE-TECHO.yaml`) antes de que este guion existiera.

Uso (desde la raiz):

    uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py control \\
        docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt
    uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py conocida \\
        docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt
    uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py variante <nombre> \\
        docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt
    uv run python -B docs/validation/anexos/PUENTE-TECHO/puente.py todo \\
        docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt

Los cuatro modos corren primero el control de ADR-0098 §1 con el bucle de este guion (D2 a) y
paran con 4 si no pasa. `control` se queda ahi. `conocida` es D2 c sobre los dias dev: cada
posicion del techo llenada al precio de su orden, abierta otra vez con `abrir_conocida` en el
instante y al precio del llenado, con el mismo lote, stop y objetivo, tiene que dar el mismo riesgo,
el mismo R bruto y neto y el mismo cierre. `variante` corre una de las dieciseis del yaml. `todo`
corre las dieciseis en el orden del yaml, con el entorno construido una sola vez, y al final la
lectura del puente. Sale con 0 si todo se hizo, con 4 si el control no pasa, con 5 si D2 c no pasa
(en `conocida`) y con 2 ante un error de entrada.

EL MODELO es el de `techo_parejas.py` (ADR-0098 §1; su docstring), cargado de `main` por su ruta
y sin copiar: el entorno, las piezas puras, el dimensionado, la medida y los formatos. Lo que se
reescribe, con un interruptor por pieza del yaml (`piezas`): el bucle del dia (`repetir`), la
construccion de los pedidos (`techo`, que solo guarda el minuto), el predicado de RN-002 (los dos
por separado) y las filas de las posiciones abiertas con `abrir_conocida`, que
`posiciones_del_bot` salta porque no tienen orden (`cableado.py:1341-1343`): se calculan aqui con
sus mismas formulas.

- `objetivo_sobre_el_stop`: el objetivo, `objetivo_rr` por la distancia de la entrada al stop del
  caso, hacia abajo al punto, en lugar de por la caja derivada.
- `sin_break_even`: RN-014 no mueve el stop.
- `entrada_al_precio_del_caso`: `abrir_conocida` en el instante (al segundo, el de la ingesta) y al
  precio del caso, con el lote del riesgo limitado como en el techo, el mismo stop y el mismo
  objetivo; sin orden stop no hay no colocables ni no llenadas; un rechazo del perfil se cuenta.
- `sin_las_de_mas_de_<N>_lotes`: fuera, y contadas, las de lote por riesgo (antes de limitar)
  mayor que `lotes_fuera_si_el_lote_por_riesgo_pasa_de`.
- `desfase_menos_<N>`: la entrada y el stop del caso, `desfase_puntos` por debajo, en los dos lados.
- `spread_menos_<k>` y `sin_spread`: el ASK de cada tick a max(BID, ASK - k) o al BID; los minutos
  sin ticks (el respaldo M1 con su spread supuesto) no se tocan.
- `sin_cierre_h4`: RN-002 solo por `alcanza_hora`, no por `vence_vela_h4`.
- `stop_en_el_08`: el stop a `stop_fraccion_caja` por la distancia del caso, al punto mas cercano
  (como `niveles()` de `scripts/viabilidad_comision.py`), y el lote sobre esa distancia.

LO QUE IMPRIME (ADR-0099 §2, ADR-0098 §4 c): por variante, sobre los cuatro meses y aparte sobre
abril y agosto juntos, recuentos y agregados, y las lecturas que salen de los yaml. Ninguna
operacion con su R, ningun R por clase de setup, sesion o direccion, ningun precio, ninguna vela,
ningun nivel. Por mes, solo d), e) y f) por cuenta y el subtotal de abril y agosto; el bloque de
julio, solo en `base`, porque es el bloque M1 de `meta.txt` (D2 b).
"""

from __future__ import annotations

import bisect
import dataclasses
import importlib.util
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

# el guion del techo de `main`, por su ruta literal (desde la raiz), sin copiarlo
_ESPEC = importlib.util.spec_from_file_location(
    "techo_parejas", "docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py"
)
if _ESPEC is None or _ESPEC.loader is None:
    raise ImportError("no encuentro techo_parejas.py: el guion se lanza desde la raiz")
tp: Any = importlib.util.module_from_spec(_ESPEC)
sys.modules["techo_parejas"] = tp  # sus dataclasses lo buscan aqui
_ESPEC.loader.exec_module(tp)

RAIZ: Path = tp.RAIZ
MS: int = tp.MS
HORA_MS = 60 * MS
PIEZAS_DEL_GUION = (
    "objetivo_sobre_el_stop",
    "sin_break_even",
    "entrada_al_precio_del_caso",
    "sin_las_de_mas_de_{lotes}_lotes",
    "desfase_menos_{desfase}",
    "spread_menos_{k0}",
    "spread_menos_{k1}",
    "sin_spread",
    "sin_cierre_h4",
    "stop_en_el_08",
)

# ------------------------------------------------------------------------- piezas puras


@dataclass(frozen=True)
class Piezas:
    """Los interruptores de una variante. Todo apagado es el techo de ADR-0098 §1."""

    objetivo_sobre_el_stop: bool = False
    sin_break_even: bool = False
    entrada_al_precio_del_caso: bool = False
    tope_lotes: Decimal | None = None  # sin_las_de_mas_de_N_lotes
    desfase: int = 0  # puntos que se restan a la entrada y al stop del caso
    spread: int | None = 0  # k: el ASK a max(BID, ASK - k); 0 sin cambio; None, igual al BID
    sin_cierre_h4: bool = False
    stop_en_el_08: bool = False
    cambia_spread: bool = False


def nombres_de_las_piezas(propios: Mapping[str, Any]) -> tuple[str, ...]:
    """Los nombres de las piezas del yaml, con sus cifras sacadas de `propios` (no del guion)."""
    k0, k1 = (int(k) for k in propios["spread_menos_puntos"])
    return tuple(
        p.format(
            lotes=propios["lotes_fuera_si_el_lote_por_riesgo_pasa_de"],
            desfase=propios["desfase_puntos"],
            k0=k0,
            k1=k1,
        )
        for p in PIEZAS_DEL_GUION
    )


def piezas_de(nombres: Sequence[str], propios: Mapping[str, Any]) -> Piezas:
    """Los interruptores de una lista de piezas del yaml; una pieza desconocida rompe."""
    conocidas = nombres_de_las_piezas(propios)
    desconocidas = [n for n in nombres if n not in conocidas]
    if desconocidas:
        raise ValueError(f"piezas que el guion no sabe hacer: {desconocidas}")
    (objetivo, sin_be, entrada, tope, desfase, spread0, spread1, sin_spread, sin_h4, st08) = (
        conocidas
    )
    k0, k1 = (int(k) for k in propios["spread_menos_puntos"])
    spreads = [n for n in nombres if n in (spread0, spread1, sin_spread)]
    if len(spreads) > 1:
        raise ValueError(f"dos piezas de spread a la vez: {spreads}")
    k: int | None = 0
    if spread0 in nombres:
        k = k0
    elif spread1 in nombres:
        k = k1
    elif sin_spread in nombres:
        k = None
    return Piezas(
        objetivo_sobre_el_stop=objetivo in nombres,
        sin_break_even=sin_be in nombres,
        entrada_al_precio_del_caso=entrada in nombres,
        tope_lotes=(
            Decimal(propios["lotes_fuera_si_el_lote_por_riesgo_pasa_de"])
            if tope in nombres
            else None
        ),
        desfase=int(propios["desfase_puntos"]) if desfase in nombres else 0,
        spread=k,
        sin_cierre_h4=sin_h4 in nombres,
        stop_en_el_08=st08 in nombres,
        cambia_spread=bool(spreads),
    )


@dataclass(frozen=True)
class Niveles:
    entrada: int
    stop: int
    caja: int  # la distancia del 1 derivada del stop del caso
    base_stop: int  # la distancia de la entrada al stop del caso (la de objetivo_sobre_el_stop)


def niveles_del_caso(
    entrada: int, stop: int, lado: str, piezas: Piezas, fraccion: Decimal, modo: str
) -> Niveles:
    """Entrada, stop, caja y base del objetivo de una operacion del trader con las piezas puestas.
    Puro. El desfase baja la entrada y el stop por igual, asi que la distancia no cambia."""
    entrada, stop = entrada - piezas.desfase, stop - piezas.desfase
    distancia = abs(entrada - stop)
    caja = tp.caja_derivada(distancia, fraccion, modo)
    if piezas.stop_en_el_08:
        d08 = int((Decimal(distancia) * fraccion).to_integral_value())
        stop = entrada - d08 if lado == "compra" else entrada + d08
    return Niveles(entrada, stop, caja, distancia)


def base_del_objetivo(n: Niveles, piezas: Piezas, base_registro: str) -> int:
    """La distancia sobre la que `objetivo_rr` pone el objetivo."""
    if piezas.objetivo_sobre_el_stop:
        return n.base_stop
    return n.caja if base_registro == "caja_completa" else abs(n.entrada - n.stop)


def ask_con_spread(ask: int, bid: int, k: int | None) -> int:
    """El ASK de un tick con la pieza de spread: max(BID, ASK - k), o el BID. Nunca cruza el BID."""
    if k is None:
        return bid
    return max(bid, ask - k)


def ticks_con_spread(ticks: Sequence[Any], k: int | None) -> list[Any]:
    from botsito.domain.ticks import Tick
    from botsito.domain.valores import Puntos

    return [
        dataclasses.replace(t, ask=Puntos(ask_con_spread(int(t.ask), int(t.bid), k)))
        if isinstance(t, Tick)
        else t
        for t in ticks
    ]


def fuera_por_el_tope(lote_riesgo: Decimal, tope: Decimal | None) -> bool:
    return tope is not None and lote_riesgo > tope


def lectura_por_el_r(
    n: int,
    esperanza: Decimal | None,
    bajo: Decimal | None,
    alto: Decimal | None,
    n_minimo: int,
    esperanza_min: Decimal,
    alto_minimo: Decimal,
    orden: Sequence[str],
) -> str:
    """ADR-0099 §3, en el orden del yaml: gana, no_gana, no_concluyente (sin d, e ni f)."""
    cumple = {
        "gana": n >= n_minimo
        and esperanza is not None
        and esperanza >= esperanza_min
        and bajo is not None
        and bajo > 0,
        "no_gana": (esperanza is not None and esperanza < 0)
        or (alto is not None and alto < alto_minimo),
        "no_concluyente": True,
    }
    return next(clave for clave in orden if cumple[clave])


def lectura_del_puente(
    sueltas: Mapping[str, str], todo_junto: str, orden: Sequence[str]
) -> tuple[str, list[str]]:
    """ADR-0099 §3, el puente entero, en el orden del yaml; con las sueltas que no dan no_gana."""
    salen = [nombre for nombre, lectura in sueltas.items() if lectura != "no_gana"]
    cumple = {
        "una_pieza_basta": bool(salen),
        "solo_juntas": not salen and todo_junto != "no_gana",
        "ni_juntas": todo_junto == "no_gana",
    }
    return next(clave for clave in orden if cumple[clave]), salen


def cierre_del_puente(
    n: int,
    neta: Decimal | None,
    bruta: Decimal | None,
    publicada: Mapping[str, Any],
    tol_operaciones: int,
    tol_neta: Decimal,
) -> tuple[bool, str]:
    """ADR-0099 §2: cierra si N queda a `tol_operaciones` o menos y la neta a `tol_neta` o menos."""
    pub_n = int(publicada["operaciones"])
    pub_neta = Decimal(publicada["esperanza_neta_r"])
    pub_bruta = Decimal(publicada["esperanza_bruta_r"])
    cierra = (
        neta is not None and abs(n - pub_n) <= tol_operaciones and abs(neta - pub_neta) <= tol_neta
    )
    dif_neta = "sin definir" if neta is None else f"{neta - pub_neta:+.3f}"
    dif_bruta = "sin definir" if bruta is None else f"{bruta - pub_bruta:+.3f}"
    return cierra, (
        f"N {n} frente a {pub_n} ({n - pub_n:+d}); esperanza neta {tp._r(neta)} frente a "
        f"{pub_neta} ({dif_neta}); antes de comision {tp._r(bruta)} frente a {pub_bruta} "
        f"({dif_bruta})"
    )


# ------------------------------------------------------------------------ la repeticion


@dataclass
class PedidoPuente:
    """Una operacion que la repeticion abre: por orden stop (el techo) o con `abrir_conocida`."""

    id: str
    dia: str
    lado: str
    entrada: int  # puntos
    stop: int
    caja: int
    minuto: int  # la iteracion del bucle en que se coloca (decide en minuto * MS - 1)
    fin_minuto: int | None = None
    cerrar_en_ms: int | None = None  # control: un manual fuera del control, en su instante
    base_stop: int = 0  # la distancia del caso, para objetivo_sobre_el_stop
    instante_ms: int = 0  # el del caso (entrada_al_precio_del_caso)
    conocida: bool = False
    lote_forzado: Decimal | None = None  # D2 c: el mismo lote que la posicion del techo
    objetivo_forzado: int | None = None  # D2 c: el mismo objetivo
    fuente: str = "caso"  # D2 c: la fuente de apertura de la posicion del techo (ADR-0091 §2)


@dataclass
class Recuentos:
    """Por mes: lo que el techo cuenta y lo que el puente anade."""

    por_mes: dict[str, Counter[str]] = field(default_factory=dict)
    rechazadas: dict[str, Counter[str]] = field(default_factory=dict)

    def mas(self, mes: str, que: str, n: int = 1) -> None:
        self.por_mes.setdefault(mes, Counter())[que] += n

    def rechazo(self, mes: str, motivo: str) -> None:
        self.rechazadas.setdefault(mes, Counter())[motivo] += 1

    def total(self, que: str, meses: Sequence[str] | None = None) -> int:
        return sum(c[que] for m, c in self.por_mes.items() if meses is None or m in meses)

    def rechazos(self, meses: Sequence[str] | None = None) -> Counter[str]:
        salida: Counter[str] = Counter()
        for m, c in self.rechazadas.items():
            if meses is None or m in meses:
                salida.update(c)
        return salida


@dataclass
class Repeticion:
    brokers: dict[str, Any]
    trazas: dict[str, Any]
    cuentas: list[tuple[str, Any]]
    recuentos: Recuentos
    contrato: Decimal
    reglas_broker: Any
    reglas_fase: Any
    por_fuente: Counter[str] = field(default_factory=Counter)


def predicado_rn002(registro: Any, solo_ventana: bool) -> Callable[[int], bool]:
    """`_rn002` del techo con los dos predicados por separado: con `solo_ventana`, solo
    `alcanza_hora` (la pieza `sin_cierre_h4`)."""
    from botsito.domain.velas import MinutoUtc
    from botsito.engine.primitivas import primitivas_escritas

    pred = primitivas_escritas(registro).predicados
    vence: Any = pred["vence_vela_h4"]
    alcanza: Any = pred["alcanza_hora"]
    args_vence = {"anclaje": "anclaje_h4", "antelacion": "cierre_h4_antelacion"}
    args_alcanza = {"hora": "ventana_fin", "reloj": "reloj_sesiones"}

    def dispara(instante: int) -> bool:
        m = SimpleNamespace(instante=MinutoUtc(instante))
        b = alcanza(args_alcanza, m, None)
        if solo_ventana:
            return bool(b.valor.name == "SI")
        a = vence(args_vence, m, None)
        return bool(a.valor.name == "SI" or b.valor.name == "SI")

    return dispara


def repetir(
    ent: Any, pedidos: Sequence[PedidoPuente], piezas: Piezas, dias: Sequence[Any] | None = None
) -> Repeticion:
    """El bucle del dia de `techo_parejas.repetir`, con los interruptores de `piezas`."""
    from botsito.domain.estructura_m1 import zona_posterior_completada
    from botsito.engine.broker import Broker, BrokerError, Rechazo, minuto_de_apertura
    from botsito.engine.cableado import MotorCableado
    from botsito.engine.cuenta import CuentaViva
    from botsito.engine.llenado import TIPO_STOP, Mercado
    from botsito.engine.primitivas_broker import ContextoDia

    registro = ent.registro
    if registro.opcion("break_even_condicion") != "cierre":
        raise ValueError("break_even_condicion no es `cierre`: el guion solo reproduce esa")
    criterio_be = registro.opcion("break_even_criterio_ruptura")
    cierre_forzoso = registro.opcion("cierre_forzoso_fin_ventana") == "si"
    base_riesgo = registro.opcion("base_calculo_riesgo")
    lotaje = registro.opcion("lotaje_base")
    riesgo_pct = registro.porcentaje("riesgo_por_operacion").valor
    paso = registro.lotes("instrumento_lote_paso")
    minimo = registro.lotes("instrumento_lote_minimo")
    fraccion_margen = registro.decimal("lote_margen_libre_fraccion")
    multiplo = registro.decimal("objetivo_rr")
    base_objetivo = registro.opcion("base_calculo_objetivo")
    if registro.opcion("lote_si_no_cabe") != "limitar":
        raise ValueError("lote_si_no_cabe no es `limitar`: ADR-0098 §1 lo da por limitar")
    rn002 = predicado_rn002(registro, piezas.sin_cierre_h4)
    por_dia: dict[str, list[PedidoPuente]] = {}
    for p in pedidos:
        por_dia.setdefault(p.dia, []).append(p)
    rec = Recuentos()
    brokers: dict[str, Any] = {}
    trazas: dict[str, Any] = {}
    cuentas: list[tuple[str, Any]] = []
    por_fuente: Counter[str] = Counter()
    rb = ent.reglas_broker
    cuenta: Any = None
    mes_en_curso: str | None = None
    for d in ent.dias if dias is None else dias:
        clave = d.dia
        md = ent.mercados[clave]
        limites = tuple(
            (n, int(a), int(b))
            for n, a, b in ent.reloj.limites_de_sesiones(date.fromisoformat(clave), ent.sesiones)
        )
        primero = min(a for _, a, _ in limites)
        ultimo = max(b for _, _, b in limites)
        mes = clave[:7]
        if cuenta is None or mes != mes_en_curso:
            cuenta = CuentaViva(ent.reglas_fase, ent.contrato, primero * MS - 1)
            cuentas.append((mes, cuenta))
        mes_en_curso = mes
        mercado = (
            Mercado(ticks_con_spread(md.ticks, piezas.spread), md.m1)
            if piezas.cambia_spread
            else md.mercado()
        )
        broker = Broker(
            rb, ent.config_llenado, mercado, ent.contrato, md.escala, saldo=tp._saldo_de(cuenta)
        )
        ctx = ContextoDia(broker, cuenta, ent.contrato, md.escala)
        tb = tp.Traza(limites)
        yo = SimpleNamespace(cuenta=cuenta, reglas_broker=rb, racha=None)
        inicios = [int(v.inicio) for v in md.m1]
        horas_con_ticks = {int(t.instante) // HORA_MS for t in md.ticks}
        pendientes_del_dia = sorted(por_dia.get(clave, []), key=lambda p: (p.minuto, p.id))
        for p in pendientes_del_dia:
            if p.minuto > ultimo:
                rec.mas(mes, "fuera_de_ventana")
            elif p.minuto < primero:
                rec.mas(mes, "fuera_de_ventana")
                p.minuto = primero
        fin_de: dict[str, int | None] = {}
        cerrar_en: dict[str, int] = {}
        vistos = 0
        for instante in range(primero, ultimo + 1):
            hasta_ms = instante * MS - 1
            nuevos = broker.avanzar(hasta_ms)
            vistos = MotorCableado._a_la_cuenta(
                cast(Any, yo), broker, ctx, cast(Any, tb), nuevos, vistos, hasta_ms
            )
            ctx.instante_ms = hasta_ms
            vivas = [pos for pos in broker.posiciones.values() if pos.abierta]
            if len(vivas) > 1:
                rec.mas(mes, "dos_vivas")
            for pos in vivas:  # control: el manual de una regla solo del bot, en su instante
                if cerrar_en.get(pos.orden_id) == hasta_ms:
                    broker.cerrar_a_mercado(pos.id, hasta_ms)
            vivas = [pos for pos in vivas if pos.abierta]
            if vivas and cierre_forzoso and rn002(instante):
                for pos in vivas:
                    broker.cerrar_a_mercado(pos.id, hasta_ms)
                    rec.mas(mes, "rn002")
                vivas = []
            if not piezas.sin_break_even:
                for pos in vivas:  # RN-014, en el cierre de la M1 que pasa el punto
                    a = bisect.bisect_left(inicios, minuto_de_apertura(pos))
                    b = bisect.bisect_left(inicios, instante)
                    m1 = md.m1[a:b]
                    k = zona_posterior_completada(m1, pos.lado, criterio_be)
                    if k is not None and int(m1[k].fin) == instante:
                        broker.mover_stop(pos.id, pos.entrada, hasta_ms)
                        rec.mas(mes, "break_even")
            for oid, fin in list(fin_de.items()):  # no llenada en su sesion
                o = broker.ordenes[oid]
                if fin is not None and instante >= fin and o.estado in ("colocada", "modificada"):
                    broker.cancelar(oid, hasta_ms)
                    rec.mas(mes, "no_llenadas")
                    del fin_de[oid]
            for p in [p for p in pendientes_del_dia if p.minuto == instante]:
                if not p.conocida and broker.lado_equivocado_al_colocar(
                    TIPO_STOP, cast(Any, p.lado), p.entrada, hasta_ms
                ):
                    rec.mas(mes, "no_colocables")
                    if hasta_ms // HORA_MS not in horas_con_ticks:
                        rec.mas(mes, "no_colocables_en_hora_sin_ticks")
                    if broker.mercado.ticks_del_minuto(instante - 1) is None:
                        rec.mas(mes, "no_colocables_en_minuto_sin_ticks")
                    continue
                distancia_stop = abs(p.entrada - p.stop)
                distancia = distancia_stop if lotaje == "hasta_stop_fraccion" else p.caja
                saldo = cuenta.saldo if base_riesgo == "saldo_actual" else cuenta.saldo_corte
                if p.lote_forzado is not None:
                    lote = p.lote_forzado
                else:
                    lote_riesgo = tp.lote_del_riesgo(
                        saldo, riesgo_pct, distancia, md.escala, ent.contrato, paso
                    )
                    if fuera_por_el_tope(lote_riesgo, piezas.tope_lotes):
                        rec.mas(mes, "fuera_por_el_tope")
                        continue
                    instante_lote = p.instante_ms if p.conocida else hasta_ms
                    lote = tp._lote_final(broker, rb, p.lado, lote_riesgo, instante_lote,
                                          fraccion_margen, md.escala, ent.contrato, paso,
                                          minimo)  # fmt: skip
                    if lote is None:
                        rec.mas(mes, "lote_minimo")
                        continue
                if p.objetivo_forzado is not None:
                    objetivo = p.objetivo_forzado
                else:
                    base = base_del_objetivo(
                        Niveles(p.entrada, p.stop, p.caja, p.base_stop), piezas, base_objetivo
                    )
                    objetivo = tp.objetivo_de(p.entrada, p.lado, base, multiplo)
                if p.conocida:
                    try:
                        broker.abrir_conocida(
                            p.id, cast(Any, p.lado), p.entrada, lote, p.stop, objetivo,
                            p.instante_ms, p.fuente,
                        )  # fmt: skip
                    except BrokerError as exc:
                        rec.rechazo(mes, f"al abrir: {str(exc).rsplit('(', 1)[-1].rstrip(')')}")
                    continue
                try:
                    r = broker.colocar_stop(
                        p.id, cast(Any, p.lado), p.entrada, lote, p.stop, objetivo, hasta_ms
                    )
                except BrokerError as exc:
                    raise ValueError(
                        f"{clave} {p.id}: el broker no admite la orden ({exc})"
                    ) from exc
                if isinstance(r, Rechazo):
                    rec.rechazo(mes, f"al colocar: {r.motivo}")
                    continue
                fin_de[p.id] = p.fin_minuto
                if p.cerrar_en_ms is not None:
                    cerrar_en[p.id] = p.cerrar_en_ms
            ctx.eventos = []
        fin_ms = ultimo * MS - 1
        for pos in list(broker.posiciones.values()):
            if pos.abierta:
                broker.cerrar_a_mercado(pos.id, fin_ms)
                rec.mas(mes, "fin_de_dia")
        for o in list(broker.ordenes.values()):
            if o.estado in ("colocada", "modificada"):
                broker.cancelar(o.id, fin_ms)
                rec.mas(mes, "no_llenadas")
        nuevos = broker.avanzar(fin_ms)
        MotorCableado._a_la_cuenta(
            cast(Any, yo), broker, ctx, cast(Any, tb), nuevos, vistos, fin_ms
        )
        for o in broker.ordenes.values():  # el rechazo al llenar: la orden estuvo colocada antes
            if o.estado == "rechazada" and len(o.historial) > 1:
                motivo = next(
                    (r.motivo for r in broker.traza().rechazos if r.orden_id == o.id), "?"
                )
                rec.rechazo(mes, f"al llenar: {motivo}")
        por_fuente.update(tb.por_fuente)
        brokers[clave] = broker
        trazas[clave] = tb
    return Repeticion(brokers, trazas, cuentas, rec, ent.contrato, rb, ent.reglas_fase, por_fuente)


def filas_conocidas(rep: Repeticion) -> list[Any]:
    """Las filas de las posiciones abiertas con `abrir_conocida`, que `posiciones_del_bot` salta
    (no tienen orden): sus mismas formulas, con el riesgo sobre el stop de apertura (lotes x
    distancia de la entrada a ese stop / escala x contrato) y la entrada que no es por stop."""
    from botsito.cases.criterio_fidelidad import PosicionCerrada
    from botsito.engine.broker import minuto_de_apertura
    from botsito.engine.cableado import SIN_MEDIDA, FilaPosicion, _instante, _precio
    from botsito.engine.cuenta import Marca, pnl
    from botsito.engine.cuenta import Operacion as OperacionCuenta
    from botsito.engine.primitivas_broker import clasificar_cierre

    salida: list[Any] = []
    rb = rep.reglas_broker
    for dia in sorted(rep.trazas):
        broker = rep.brokers.get(dia)
        tb = rep.trazas[dia]
        if broker is None:
            continue
        escala = broker.escala
        for p in sorted(broker.posiciones.values(), key=lambda x: (x.abierta_ms, x.id)):
            if p.cerrada_ms is None or p.precio_cierre is None or p.motivo_cierre is None:
                continue
            if p.orden_id in broker.ordenes:
                continue  # la de una orden: la da posiciones_del_bot
            entrada, cierre = _precio(p.entrada, escala), _precio(p.precio_cierre, escala)
            apertura = Marca(_instante(p.abierta_ms), entrada)
            bruto = pnl(OperacionCuenta(p.id, p.lado, p.lotes, apertura, apertura), cierre,
                        rep.contrato)  # fmt: skip
            comision = rb.comision_por_lote * p.lotes * (2 if rb.comision_por_lado else 1)
            swaps = sum((imp for t, imp in p.swaps if t <= p.cerrada_ms), Decimal(0))
            neto = bruto - comision - swaps
            stop_apertura = p.stop_original if p.stop_original is not None else p.stop
            riesgo = p.lotes * Decimal(abs(p.entrada - stop_apertura)) / escala * rep.contrato
            signo = 1 if p.lado == "compra" else -1
            desenlace = clasificar_cierre(
                p.motivo_cierre,
                p.stop_original is not None,
                Decimal(signo * (p.precio_cierre - p.entrada)),
            )
            minuto = minuto_de_apertura(p)
            sesion = next((n for n, a, b in tb.limites if a <= minuto < b), SIN_MEDIDA)
            salida.append(
                FilaPosicion(
                    dia, sesion, p.id, p.orden_id, p.lado, "conocida", _instante(p.abierta_ms),
                    entrada, _instante(p.cerrada_ms), cierre, p.motivo_cierre, desenlace,
                    p.lotes, bruto, comision, swaps, neto, riesgo,
                    PosicionCerrada(
                        dia, neto, riesgo, False, p.motivo_cierre, p.lotes,
                        rep.contrato / escala,
                    ),
                )
            )  # fmt: skip
    return salida


def filas(rep: Repeticion) -> list[Any]:
    """Todas las filas: las de orden por `posiciones_del_bot` (`filas_de` del techo) y las de
    `abrir_conocida` por `filas_conocidas`. Sin conocidas, el orden es el del techo."""
    de_orden = list(tp.filas_de(rep))
    conocidas = filas_conocidas(rep)
    if not conocidas:
        return de_orden
    return sorted([*de_orden, *conocidas], key=lambda f: (f.dia, f.llenada, f.id))


def en_break_even(fila: Any) -> bool:
    """Cerrada por el stop movido a la entrada (`clasificar_cierre`: stop con el stop movido)."""
    from botsito.engine.primitivas_broker import BREAK_EVEN

    return bool(fila.desenlace == BREAK_EVEN)


def esperanza_bruta(posiciones: Sequence[Any]) -> Decimal | None:
    """La media del PnL bruto entre el riesgo: la esperanza antes de comision."""
    validas = [f for f in posiciones if f.riesgo > 0]
    if not validas:
        return None
    return sum((f.bruto / f.riesgo for f in validas), Decimal(0)) / len(validas)


# ----------------------------------------------------------------------------- el control


def control(ent: Any, salida: Path) -> tuple[bool, list[str]]:
    """`techo_parejas.control` con el bucle de este guion (D2 a): las ordenes llenadas del bot,
    repetidas, al centimo."""
    pred_rn002 = predicado_rn002(ent.registro, False)
    ordenes = tp.ordenes_llenadas(salida)
    pedidos: list[PedidoPuente] = []
    esperadas: dict[tuple[str, str], Any] = {}
    fuera: list[str] = []
    for o in ordenes:
        md = ent.mercados[o.dia]
        entrada = tp.a_puntos(o.entrada, md.escala)
        stop = entrada - o.distancia if o.lado == "compra" else entrada + o.distancia
        caja = abs(tp.a_puntos(o.caja1, md.escala) - entrada)
        limites = ent.reloj.limites_de_sesiones(date.fromisoformat(o.dia), ent.sesiones)
        fin_dia = max(int(b) for _, _, b in limites) * MS - 1
        cerrar: int | None = None
        if o.esperada.motivo == "manual":
            alineado = (o.cierre_ms + 1) % MS == 0
            if not (o.cierre_ms == fin_dia or (alineado and pred_rn002((o.cierre_ms + 1) // MS))):
                fuera.append(f"{o.dia} {o.id} manual en {o.esperada.cierre}")
                if not alineado:
                    raise ValueError(f"{o.dia} {o.id}: manual fuera del cierre de una M1")
                cerrar = o.cierre_ms
        if (o.colocada_ms + 1) % MS:
            raise ValueError(f"{o.dia} {o.id}: colocada fuera del cierre de una M1")
        pedidos.append(
            PedidoPuente(
                o.id,
                o.dia,
                o.lado,
                entrada,
                stop,
                caja,
                (o.colocada_ms + 1) // MS,
                None,
                cerrar,
                base_stop=o.distancia,
            )  # fmt: skip
        )
        if cerrar is None:
            esperadas[(o.dia, o.id)] = o.esperada
    rep = repetir(ent, pedidos, Piezas())
    fuera_ids = {(f.split()[0], f.split()[1]) for f in fuera}
    obtenidas = {
        (f.dia, f.orden_id): tp.FilaControl(
            f.orden_id, str(f.lotes), f.cierre, f.cerrada.isoformat(), f"{f.neto:.2f}"
        )
        for f in filas(rep)
        if (f.dia, f.orden_id) not in fuera_ids
    }
    diferencias = tp.comparar_control(esperadas, obtenidas)
    vale = not diferencias and len(fuera) * 20 <= len(ordenes)
    difieren = {tuple(x.split(":")[0].split()[:2]) for x in diferencias}
    lineas = [
        "## El control (ADR-0098 §1), con el bucle de puente.py (D2 a)",
        f"posiciones del bot en la salida: {len(ordenes)}; entran en el control: {len(esperadas)}; "
        f"fuera (manual de una regla solo del bot): {len(fuera)}",
        *[f"  fuera: {f}" for f in fuera],
        "reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): "
        f"{len(esperadas) - len(difieren & set(esperadas))} de {len(esperadas)}",
        *[f"  difiere: {x}" for x in diferencias],
        "control: " + ("PASA" if vale else "NO PASA (PARADA total: no se corre ninguna variante)"),
    ]
    return vale, lineas


# ------------------------------------------------------------------------------ el techo


@dataclass
class Corrida:
    nombre: str
    piezas: Piezas
    rep: Repeticion
    filas: list[Any]
    total: int
    sin_stop: int
    sin_riesgo: int  # filas con riesgo no positivo, que no entran (el techo las filtra igual)


def pedidos_del_techo(
    ent: Any, piezas: Piezas, dias: Sequence[Any] | None = None
) -> tuple[list[PedidoPuente], int, int]:
    """Las operaciones del trader de los dias dev, como `techo_parejas.techo`, con las piezas."""
    from botsito.engine.primitivas_broker import REDONDEO_DEL_STOP

    reg = ent.registro
    fraccion = reg.fraccion("stop_fraccion_caja").valor
    modo = REDONDEO_DEL_STOP[reg.opcion("stop_fraccion_redondeo")]
    pedidos: list[PedidoPuente] = []
    sin_stop = 0
    total = 0
    for d in ent.dias if dias is None else dias:
        md = ent.mercados[d.dia]
        limites = {
            n: int(b)
            for n, _, b in ent.reloj.limites_de_sesiones(date.fromisoformat(d.dia), ent.sesiones)
        }
        for k, op in enumerate(d.operaciones, start=1):
            total += 1
            if op.stop is None:
                sin_stop += 1
                continue
            n = niveles_del_caso(
                tp.a_puntos(op.entrada, md.escala), tp.a_puntos(op.stop, md.escala),
                op.direccion, piezas, fraccion, modo,
            )  # fmt: skip
            segundos = op.instante.timestamp()
            pedidos.append(
                PedidoPuente(
                    f"t{k}",
                    d.dia,
                    op.direccion,
                    n.entrada,
                    n.stop,
                    n.caja,
                    int(segundos) // 60,
                    limites.get(op.sesion),
                    base_stop=n.base_stop,
                    instante_ms=int(round(segundos * 1000)),
                    conocida=piezas.entrada_al_precio_del_caso,
                )  # fmt: skip
            )
    return pedidos, total, sin_stop


def correr(ent: Any, nombre: str, piezas: Piezas, dias: Sequence[Any] | None = None) -> Corrida:
    pedidos, total, sin_stop = pedidos_del_techo(ent, piezas, dias)
    rep = repetir(ent, pedidos, piezas, dias)
    todas = filas(rep)
    validas = [f for f in todas if f.riesgo > 0]
    return Corrida(nombre, piezas, rep, validas, total, sin_stop, len(todas) - len(validas))


@dataclass(frozen=True)
class Lecturas:
    """Lo que las lecturas leen de los tres yaml."""

    n_minimo: int
    esperanza_min: Decimal
    perdida_diaria_max: Fraction
    perdida_total_max: Fraction
    alto_minimo: Decimal
    orden_techo: Sequence[str]
    orden_r: Sequence[str]
    orden_puente: Sequence[str]


def lecturas_de(ent: Any, meta: Mapping[str, Any], puente: Mapping[str, Any]) -> Lecturas:
    r = ent.criterio.rentabilidad
    return Lecturas(
        r.n_minimo,
        r.esperanza_minima_r,
        Fraction(r.perdida_diaria_max),
        Fraction(r.perdida_total_max),
        Decimal(meta["propios"]["techo_no_gana_si_percentil_alto_por_debajo_de_r"]),
        list(meta["lecturas"]["orden_de_lectura_del_techo"]),
        list(puente["lectura_por_el_r"]["orden"]),
        list(puente["lecturas_del_puente"]["orden"]),
    )


def bloque_m1(ent: Any, c: Corrida, lec: Lecturas) -> list[str]:
    """El bloque M1 de `techo_parejas.techo`, linea a linea, para D2 b (solo en `base`)."""
    from botsito.cases.criterio_fidelidad import punto_de_equilibrio

    rep, rec = c.rep, c.rep.recuentos
    dias = [d.dia for d in ent.dias]
    m = tp.medida_de(rep, [f.posicion for f in c.filas], dias, ent.criterio)
    julio = [d for d in dias if d.startswith("2026-07")]
    mj = tp.medida_de(
        rep, [f.posicion for f in c.filas if f.dia.startswith("2026-07")], julio, ent.criterio,
        meses=["2026-07"],
    )  # fmt: skip
    r = ent.criterio.rentabilidad
    lectura = tp.lectura_techo(m, lec.n_minimo, lec.esperanza_min, lec.perdida_diaria_max,
                               lec.perdida_total_max, lec.alto_minimo, lec.orden_techo)  # fmt: skip
    equilibrio = punto_de_equilibrio([f.posicion for f in c.filas], r.esperanza_minima_r)
    rechazadas = rec.rechazos()
    return [
        "## M1 · El techo (ADR-0098 §1)",
        f"operaciones del trader en los dias dev: {c.total}; sin stop: {c.sin_stop}; "
        f"no colocables: "
        f"{rec.total('no_colocables')}; no llenadas: {rec.total('no_llenadas')}; fuera por el lote "
        f"minimo: {rec.total('lote_minimo')}; fuera de la ventana: {rec.total('fuera_de_ventana')}",
        "rechazadas por el broker, por motivo: "
        + (", ".join(f"{k} {v}" for k, v in sorted(rechazadas.items())) or "ninguna"),
        f"llenadas y cerradas: {len(c.filas)}; cierres de M1 con mas de una posicion viva: "
        f"{rec.total('dos_vivas')}; cierres por RN-002: {rec.total('rn002')}; al fin del dia: "
        f"{rec.total('fin_de_dia')}; break even movido: {rec.total('break_even')}",
        *tp._lineas_medida(m, r, "todos los dias dev corridos"),
        "deslizamiento por llenado afectado que lleva la esperanza a "
        f"{r.esperanza_minima_r} R (ADR-0092 §4, sin decidir nada): "
        + ("sin definir" if equilibrio is None else f"{equilibrio:.2f} puntos"),
        f"LECTURA DEL TECHO: {lectura}"
        + (
            " (gana en construccion, con el deslizamiento pendiente de F17)"
            if lectura == "gana"
            else ""
        ),
        "",
        "### Julio de 2026, como diagnostico (sin umbral; el unico mes con video, provisional)",
        *tp._lineas_medida(mj, r, "los dias dev de julio"),
    ]


@dataclass
class Resultado:
    lineas: list[str]
    lectura_r: str | None
    n: int
    neta: Decimal | None
    bruta: Decimal | None


def bloque(
    ent: Any, c: Corrida, lec: Lecturas, meses: Sequence[str] | None, titulo: str, leer: bool
) -> Resultado:
    """Lo de ADR-0099 §2 sobre los meses dados (None: los cuatro): recuentos, esperanzas,
    percentiles, d, e y f y, si `leer`, la lectura por el R y la de ADR-0098 §2."""
    rep, rec = c.rep, c.rep.recuentos
    dias = [d.dia for d in ent.dias if meses is None or d.dia[:7] in meses]
    corridos = set(rep.trazas)
    dias = [x for x in dias if x in corridos]
    posiciones = [f for f in c.filas if meses is None or f.dia[:7] in meses]
    m = tp.medida_de(rep, [f.posicion for f in posiciones], dias, ent.criterio, meses=meses)
    r = ent.criterio.rentabilidad
    bruta = esperanza_bruta(posiciones)
    rechazadas = rec.rechazos(meses)
    lineas = [
        f"### {titulo}",
        f"N (llenadas y cerradas): {m.n}; no colocables: {rec.total('no_colocables', meses)}; no "
        f"llenadas: {rec.total('no_llenadas', meses)}; fuera por el tope de lotes: "
        f"{rec.total('fuera_por_el_tope', meses)}; fuera por el lote minimo: "
        f"{rec.total('lote_minimo', meses)}; fuera de la ventana: "
        f"{rec.total('fuera_de_ventana', meses)}",
        "rechazadas por el broker, por motivo: "
        + (", ".join(f"{k} {v}" for k, v in sorted(rechazadas.items())) or "ninguna"),
        f"break even movido: {rec.total('break_even', meses)}; cerradas en el break even: "
        f"{sum(1 for f in posiciones if en_break_even(f))}; cierres por RN-002: "
        f"{rec.total('rn002', meses)}; al fin del dia: {rec.total('fin_de_dia', meses)}",
        f"esperanza antes de comision y swaps (media del R bruto): {tp._r(bruta)}; neta (media "
        f"del R neto): {tp._r(m.esperanza)}",
        f"percentil {r.percentil_remuestreo} y percentil {tp.PERCENTIL_ALTO} de la media del R "
        f"neto, por remuestreo por dias ({r.replicas_remuestreo} replicas, semilla "
        f"{r.semilla_remuestreo}, {len(dias)} dias): {tp._r(m.percentil_bajo)} y "
        f"{tp._r(m.percentil_alto)}; replicas descartadas: {m.descartadas}",
        *tp._lineas_medida(m, r, "")[3:],
    ]
    if meses is None:
        lineas.insert(2, f"cerradas con riesgo no positivo (no entran): {c.sin_riesgo}")
    lectura_r: str | None = None
    if leer:
        lectura_r = lectura_por_el_r(m.n, m.esperanza, m.percentil_bajo, m.percentil_alto,
                                     lec.n_minimo, lec.esperanza_min, lec.alto_minimo,
                                     lec.orden_r)  # fmt: skip
        lectura_t = tp.lectura_techo(m, lec.n_minimo, lec.esperanza_min, lec.perdida_diaria_max,
                                     lec.perdida_total_max, lec.alto_minimo,
                                     lec.orden_techo)  # fmt: skip
        lineas += [
            f"LECTURA POR EL R (ADR-0099 §3): {lectura_r}",
            f"lectura de ADR-0098 §2 (lectura_techo): {lectura_t}",
        ]
    return Resultado(lineas, lectura_r, m.n, m.esperanza, bruta)


@dataclass(frozen=True)
class Variante:
    nombre: str
    piezas: tuple[str, ...]
    grupo: str  # base, suelta, todo_junto, de_vuelta, cierre


def variantes_del_yaml(puente: Mapping[str, Any]) -> list[Variante]:
    """Las dieciseis, en el orden del yaml, con su nombre."""
    v = puente["variantes"]
    salida = [Variante("base", tuple(v["base"]), "base")]
    salida += [Variante(s[0], tuple(s), "suelta") for s in v["sueltas"]]
    salida.append(Variante("todo_junto", tuple(v["todo_junto"]), "todo_junto"))
    todo = list(v["todo_junto"])
    for lista in v["de_vuelta"]:
        repuesta = [p for p in todo if p not in lista]
        if len(repuesta) != 1:
            raise ValueError(f"una de vuelta que no repone una sola pieza: {lista}")
        salida.append(Variante(f"de_vuelta_{repuesta[0]}", tuple(lista), "de_vuelta"))
    salida += [Variante(n, tuple(lista), "cierre") for n, lista in v["cierre"].items()]
    return salida


def correr_variante(
    ent: Any, var: Variante, puente: Mapping[str, Any], lec: Lecturas
) -> tuple[list[str], Resultado | None, Resultado]:
    """Una variante: sus lineas, el bloque de los cuatro meses (None en las del cierre) y el de
    abril y agosto."""
    propios = puente["propios"]
    piezas = piezas_de(var.piezas, propios)
    meses_cierre = list(puente["cierre"]["meses"])
    dias = [d for d in ent.dias if d.dia[:7] in meses_cierre] if var.grupo == "cierre" else None
    c = correr(ent, var.nombre, piezas, dias)
    lineas = [f"## Variante {var.nombre} ({var.grupo}): [{', '.join(var.piezas)}]"]
    cuatro: Resultado | None = None
    if var.grupo == "base":
        lineas += bloque_m1(ent, c, lec)
        lineas += [
            "",
            "### D8 (sin R): eventos del techo por fuente: "
            + ", ".join(f"{k} {v}" for k, v in sorted(c.rep.por_fuente.items())),
            f"no colocables en una hora UTC sin ticks: "
            f"{c.rep.recuentos.total('no_colocables_en_hora_sin_ticks')} de "
            f"{c.rep.recuentos.total('no_colocables')}; en un minuto sin ticks (el de la "
            f"colocacion): {c.rep.recuentos.total('no_colocables_en_minuto_sin_ticks')}",
            "",
        ]
    if piezas.cambia_spread:  # D3: con el spread cambiado, cuantos eventos salen del respaldo
        lineas += [
            "eventos por fuente (sin R; el respaldo M1 no lleva el spread cambiado): "
            + ", ".join(f"{k} {v}" for k, v in sorted(c.rep.por_fuente.items())),
        ]
    if var.grupo != "cierre":
        cuatro = bloque(ent, c, lec, None, "Los cuatro meses", True)
        lineas += cuatro.lineas
    ay = bloque(ent, c, lec, meses_cierre, "Abril y agosto juntos (sin lectura)", False)
    lineas += ay.lineas
    if var.grupo == "cierre":
        pub = puente["cierre"]["publicadas_con_5_usd"][
            "v1" if var.nombre.startswith("v1") else "v2"
        ]
        cierra, texto = cierre_del_puente(
            ay.n, ay.neta, ay.bruta, pub, int(propios["cierre_tolerancia_operaciones"]),
            Decimal(propios["cierre_tolerancia_esperanza_neta_r"]),
        )  # fmt: skip
        lineas.append(
            f"CIERRE DEL PUENTE (ADR-0099 §2) frente a la publicada: "
            f"{'cierra' if cierra else 'no cierra'}; {texto}"
        )
    return lineas, cuatro, ay


# ----------------------------------------------------------------------------- D2 c


def conocida(ent: Any) -> tuple[bool, list[str]]:
    """D2 c sobre los dias dev: cada posicion del techo llenada al precio de su orden, otra vez con
    `abrir_conocida` en su instante y a su precio, con el mismo lote, stop y objetivo."""
    base = correr(ent, "base", Piezas())
    pedidos: list[PedidoPuente] = []
    esperadas: dict[tuple[str, str], Any] = {}
    for f in base.filas:
        broker = base.rep.brokers[f.dia]
        o = broker.ordenes[f.orden_id]
        p = broker.posiciones[f.id]
        if p.entrada != o.precio:
            continue
        pid = f"c-{f.orden_id}"
        pedidos.append(
            PedidoPuente(
                pid,
                f.dia,
                f.lado,
                p.entrada,
                o.stop,
                0,
                p.abierta_ms // MS,
                None,
                instante_ms=p.abierta_ms,
                conocida=True,
                lote_forzado=f.lotes,
                objetivo_forzado=o.objetivo,
                fuente=p.fuente_apertura,
            )  # fmt: skip
        )
        esperadas[(f.dia, pid)] = f
    rep = repetir(ent, pedidos, Piezas())
    obtenidas = {(f.dia, f.id): f for f in filas_conocidas(rep)}
    difieren: list[str] = []
    for clave, e in sorted(esperadas.items()):
        o = obtenidas.get(clave)
        if o is None:
            difieren.append(f"{clave[0]} {clave[1]}: abrir_conocida no la abre o no la cierra")
            continue
        for campo in ("riesgo", "lotes", "cierre", "cerrada"):
            if getattr(e, campo) != getattr(o, campo):
                difieren.append(f"{clave[0]} {clave[1]}: {campo}")
        if e.bruto / e.riesgo != o.bruto / o.riesgo or e.neto / e.riesgo != o.neto / o.riesgo:
            difieren.append(f"{clave[0]} {clave[1]}: el R")
    vale = not difieren and bool(esperadas)
    rech = rep.recuentos.rechazos()
    return vale, [
        "## D2 c · abrir_conocida frente a la orden stop, sobre los dias dev",
        f"posiciones del techo: {len(base.filas)}; llenadas al precio de su orden (entran): "
        f"{len(esperadas)}; abiertas otra vez con abrir_conocida y cerradas: {len(obtenidas)}",
        "rechazadas al abrir, por motivo: "
        + (", ".join(f"{k} {v}" for k, v in sorted(rech.items())) or "ninguna"),
        f"con el mismo riesgo, lote, motivo e instante del cierre y el mismo R bruto y neto: "
        f"{len(esperadas) - len({x.split(':')[0] for x in difieren})} de {len(esperadas)}",
        *[f"  difiere: {x}" for x in difieren],
        "D2 c: " + ("PASA" if vale else "NO PASA (PARADA en las variantes con esa pieza)"),
    ]


# ---------------------------------------------------------------------------------- main


def cargar_yaml(repo: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    from botsito.comun.yaml_estricto import leer_yaml

    meta, _pivotes = tp._cargar_meta(repo)
    puente = leer_yaml(repo / "docs" / "plan" / "PUENTE-TECHO.yaml")
    if puente.get("decision") != "ADR-0099":
        raise ValueError("PUENTE-TECHO.yaml no es el de ADR-0099")
    if tuple(puente["piezas"]) != nombres_de_las_piezas(puente["propios"]):
        raise ValueError("las piezas del yaml no son las que el guion sabe hacer, en su orden")
    return meta, puente


def main(argv: Sequence[str]) -> int:
    cast(Any, sys.stdout).reconfigure(encoding="utf-8", newline="\n")  # LF tambien en Windows
    modos = ("control", "conocida", "variante", "todo")
    if not argv or argv[0] not in modos or len(argv) != (3 if argv[0] == "variante" else 2):
        print(__doc__)
        return 2
    modo, salida = argv[0], Path(argv[-1])
    meta, puente = cargar_yaml(RAIZ)
    variantes = variantes_del_yaml(puente)
    elegidas = variantes
    if modo == "variante":
        elegidas = [v for v in variantes if v.nombre == argv[1]]
        if not elegidas:
            print(f"variante desconocida: {argv[1]}; las del yaml: {[v.nombre for v in variantes]}")
            return 2
    ent = tp.entorno(RAIZ)
    lec = lecturas_de(ent, meta, puente)
    vale, lineas = control(ent, salida)
    titulo = f"{modo} {argv[1]}" if modo == "variante" else modo
    print(f"# puente.py {titulo}, sobre {salida.name} (ADR-0099; PUENTE-TECHO)")
    print()
    print("\n".join(lineas))
    if not vale:
        return 4
    if modo == "control":
        return 0
    if modo == "conocida":
        vale_c, lineas_c = conocida(ent)
        print()
        print("\n".join(lineas_c))
        return 0 if vale_c else 5
    sueltas: dict[str, str] = {}
    todo_junto: str | None = None
    for var in elegidas:
        lineas_v, cuatro, _ay = correr_variante(ent, var, puente, lec)
        print()
        print("\n".join(lineas_v))
        sys.stdout.flush()
        if cuatro is not None and var.grupo == "suelta":
            sueltas[var.nombre] = str(cuatro.lectura_r)
        if cuatro is not None and var.grupo == "todo_junto":
            todo_junto = cuatro.lectura_r
    if modo == "todo" and todo_junto is not None:
        lectura, salen = lectura_del_puente(sueltas, todo_junto, lec.orden_puente)
        print()
        print("## La lectura del puente (ADR-0099 §3)")
        print(
            "sueltas: "
            + ", ".join(f"{k} {v}" for k, v in sueltas.items())
            + f"; todo_junto: {todo_junto}"
        )
        print(
            f"LECTURA DEL PUENTE: {lectura}"
            + (
                f" (dejan de dar no_gana: {', '.join(salen)})"
                if lectura == "una_pieza_basta"
                else ""
            )
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
