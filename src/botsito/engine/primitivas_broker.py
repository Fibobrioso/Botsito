"""Las primitivas que leen el broker y la cuenta (ADR-0053 §1-3): fuente `broker`, `bot` y los
acumuladores de la firma, mas las acciones que hablan con el broker.

Se anaden a `primitivas_escritas` (ADR-0048) sin tocarlas. Todas leen un `ContextoDia` que el
bucle de `engine/cableado.py` rellena en cada minuto: el broker, la cuenta viva, los eventos del
broker desde el evento anterior, las zonas ligadas y la orden en preparacion. Lo que la spec no da
sigue NO_IMPLEMENTADA con su nombre (ADR-0053 §3.3): `perdida_dia`, `perdida_semana`, `cartuchos`,
y toda la geometria.

Ninguna cifra vive aqui (ADR-0002): los argumentos de valor son nombres del registro (ADR-0019 §1)
y se leen al evaluar; los tokens que se interpretan son los declarados en la spec.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from decimal import ROUND_DOWN, Decimal
from typing import Any

from botsito.config.registro import Registro
from botsito.domain.valores import CIEN
from botsito.engine.broker import LLENADA, MANUAL, Broker, BrokerError, Rechazo
from botsito.engine.cuenta import CuentaViva
from botsito.engine.interprete import (
    EstadoDia,
    Momento,
    NoImplementada,
    Primitivas,
    Resultado,
    Tri,
)
from botsito.engine.llenado import OBJETIVO, STOP, Lado
from botsito.engine.primitivas import primitivas_escritas
from botsito.engine.tope_trader import (
    ACUMULADOR_DIA,
    ACUMULADOR_SEMANA,
    PORCENTAJE,
    SIN_TOPE,
    TopeTrader,
)

# Tokens de la spec que estas primitivas interpretan (declarados en `tokens` de strategy_spec.yaml)
CUALQUIER_ESQUEMA = "cualquier_esquema"
CUALQUIER_ACTIVACION = "cualquier_activacion"
ESQUEMAS = ("primer_esquema", "segundo_esquema")
SALTO_EL_STOP = "salto_el_stop"
BREAK_EVEN = "break_even"
GANANCIA = "ganancia"
PERDIDA = "perdida"
SI = "si"
PREFIJO_ZONA = "zona:"
# Los acumuladores de la firma que la cuenta viva alimenta (ADR-0053 §3); los demas, hueco.
ACUMULADORES_DE_LA_FIRMA = ("perdida_dia_firma", "perdida_total_firma")
HUECOS = {
    "acumulador:cartuchos": "depende de cartucho_criterio y de un cierre con esquema (geometria)",
}
# Los dos acumuladores del trader (RN-020) los alimenta el tope del trader (A-44,
# engine/tope_trader.py) cuando esta fijado o en diagnostico; sin el, siguen siendo hueco.
ACUMULADORES_DEL_TRADER = (ACUMULADOR_DIA, ACUMULADOR_SEMANA)


class CableadoError(ValueError):
    """Una accion que el cableado no puede ejecutar con lo que tiene: nunca se adivina."""


@dataclass(frozen=True)
class Zona:
    """Una zona de control ligada por una regla: la entrada (nivel 0), el extremo de la caja
    (nivel 1), el lado y como se produjo (`por`, un esquema de la spec)."""

    id: str
    lado: Lado
    entrada: int  # puntos
    extremo: int  # puntos, el nivel 1 de la caja
    por: str

    @property
    def distancia_completa(self) -> int:
        return abs(self.entrada - self.extremo)


@dataclass
class OrdenEnPreparacion:
    zona: Zona
    stop: int | None = None
    objetivo: int | None = None
    lote: Decimal | None = None
    lotaje: tuple[str, Decimal, str] | None = None  # (base del lotaje, riesgo %, base de calculo)


@dataclass
class EventoBroker:
    instante_ms: int
    tipo: str  # LLENADA, STOP, OBJETIVO, MANUAL, EXPIRADA, rechazo
    id: str
    por: str | None = None  # el esquema de la orden (LLENADA / cierres)
    resultado: str | None = None  # el mecanismo del cierre (cierres)


@dataclass
class ContextoDia:
    """Lo que las primitivas del broker ven en el minuto que se evalua."""

    broker: Broker
    cuenta: CuentaViva
    contrato: Decimal
    escala: int
    zonas: dict[str, Zona] = field(default_factory=dict)
    orden: OrdenEnPreparacion | None = None
    eventos: list[EventoBroker] = field(default_factory=list)  # desde el evento anterior
    acumuladores: dict[str, Decimal] = field(default_factory=dict)
    por_de_orden: dict[str, str] = field(default_factory=dict)  # orden_id -> esquema
    instante_ms: int = 0  # el instante del evento del interprete (exclusivo para el broker)
    huecos: set[str] = field(default_factory=set)
    tope: TopeTrader | None = None  # el tope propio del trader (A-44), si esta fijado


def _casa_por(pedido: str, real: str | None) -> bool:
    if pedido == CUALQUIER_ACTIVACION:
        return True
    if pedido == CUALQUIER_ESQUEMA:
        return real in ESQUEMAS
    return real == pedido


def _tri(v: bool) -> Resultado:
    return Resultado(Tri.SI if v else Tri.NO)


def clasificar_cierre(motivo: str, stop_movido: bool, pnl_bruto: Decimal) -> str:
    """El mecanismo del cierre (predicado `se_cierra_operacion`, ADR-0053 §2). Puro."""
    if motivo == STOP:
        return BREAK_EVEN if stop_movido else SALTO_EL_STOP
    return GANANCIA if pnl_bruto > 0 else PERDIDA


def primitivas_cableadas(registro: Registro, ctx: ContextoDia) -> Primitivas:
    """Las primitivas de ADR-0048 mas las del broker, la cuenta y las acciones de la orden."""
    base = primitivas_escritas(registro)

    # ------------------------------------------------------------------ fuente broker

    def operaciones_abiertas_alcanzan(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        vivas = sum(1 for p in ctx.broker.posiciones.values() if p.abierta)
        return _tri(vivas >= registro.entero(str(args["tope"])))

    def se_activa_entrada(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        pedido = str(args["por"])
        return _tri(any(e.tipo == LLENADA and _casa_por(pedido, e.por) for e in ctx.eventos))

    def salta_stop(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        return _tri(any(e.tipo == STOP for e in ctx.eventos))

    def se_cierra_operacion(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        resultado, por = str(args["resultado"]), str(args["por"])
        return _tri(
            any(
                e.tipo in (STOP, OBJETIVO, MANUAL)
                and e.resultado == resultado
                and _casa_por(por, e.por)
                for e in ctx.eventos
            )
        )

    # -------------------------------------------------------------------- fuente bot

    def distancia_menor_que(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        o = ctx.orden
        if o is None or o.stop is None or o.objetivo is None:
            return Resultado(Tri.NO)
        tope = registro.puntos(str(args["tope"]))
        registro.entero(str(args["digitos"]))  # el minimo viene en puntos: la traduccion no cambia
        distancia = min(abs(o.zona.entrada - o.stop), abs(o.zona.entrada - o.objetivo))
        return _tri(distancia < tope)

    def no_es_multiplo_de(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        o = ctx.orden
        if o is None:
            return Resultado(Tri.NO)
        lote = _lote_resuelto(o)
        if lote is None:
            return Resultado(Tri.NO)
        paso = registro.lotes(str(args["paso"]))
        return _tri(lote % paso != 0)

    # ------------------------------------------------------------------ acumuladores

    def acumulador_de_la_firma(nombre: str) -> Any:
        def leer(
            args: Mapping[str, Any], momento: Momento, estado: EstadoDia
        ) -> Resultado | NoImplementada:
            valor = ctx.acumuladores.get(nombre)
            if valor is None:
                return NoImplementada(f"acumulador:{nombre}:sin cuenta")
            capital = ctx.cuenta.reglas.capital_inicial
            tope = capital * registro.porcentaje(str(args["tope"])).valor / CIEN
            umbral = tope
            if "margen" in args:
                umbral = tope - capital * registro.porcentaje(str(args["margen"])).valor / CIEN
            if "riesgo" in args:
                # la lectura PROSPECTIVA (RN-032): sumar el riesgo de la operacion que se abriria
                sobre = registro.opcion(str(args["sobre"]))
                base = ctx.cuenta.saldo if sobre == "saldo_actual" else ctx.cuenta.saldo_corte
                valor = valor + base * registro.porcentaje(str(args["riesgo"])).valor / CIEN
            return _tri(valor >= umbral)

        return leer

    def acumulador_del_trader(nombre: str) -> Any:
        """`perdida_dia` / `perdida_semana` (RN-020) contra el tope propio del trader (A-44):
        sin tope fijado es hueco con nombre; con `sin_tope`, NO siempre; con un alcance que no
        incluye este acumulador, NO; si no, la perdida desde el corte contra el tope, en la unidad
        del tope (el porcentaje lo nombra la forma, ADR-0019 §1; el dinero lo da el registro)."""

        def leer(
            args: Mapping[str, Any], momento: Momento, estado: EstadoDia
        ) -> Resultado | NoImplementada:
            tope = ctx.tope
            if tope is None:
                ctx.huecos.add(f"acumulador:{nombre}")
                return NoImplementada(f"acumulador:{nombre}")
            if tope.alcance == SIN_TOPE:
                return Resultado(Tri.NO)
            aplica = tope.aplica_dia if nombre == ACUMULADOR_DIA else tope.aplica_semana
            if not aplica:
                return Resultado(Tri.NO)
            valor = ctx.acumuladores.get(nombre)
            if valor is None:
                return NoImplementada(f"acumulador:{nombre}:sin cuenta")
            if tope.unidad == PORCENTAJE:
                umbral = registro.porcentaje(str(args["tope"])).valor
            else:
                umbral = ctx.acumuladores[f"{nombre}:tope"]
            return _tri(valor >= umbral)

        return leer

    def hueco(id: str) -> Any:
        def falta(
            args: Mapping[str, Any], momento: Momento, estado: EstadoDia
        ) -> Resultado | NoImplementada:
            ctx.huecos.add(id)
            return NoImplementada(id)

        return falta

    # ---------------------------------------------------------------------- acciones

    def _zona(ligaduras: Mapping[str, str], clave: str, quien: str) -> Zona:
        ref = ligaduras.get(clave)
        z = ctx.zonas.get(str(ref)) if ref is not None else None
        if z is None:
            raise CableadoError(f"{quien}: la ligadura {clave!r} no apunta a una zona ({ref!r})")
        return z

    def _orden(quien: str) -> OrdenEnPreparacion:
        if ctx.orden is None:
            raise CableadoError(f"{quien}: no hay orden en preparacion")
        return ctx.orden

    def _posicion_ligada(ligaduras: Mapping[str, str], clave: str, quien: str) -> str:
        # ADR-0053 §1.2: OP se liga al VALOR del hecho, que es `si`; con una sola posicion viva,
        # es esa; con varias, error nombrado
        vivas = [p for p in ctx.broker.posiciones.values() if p.abierta]
        if ligaduras.get(clave) is None:
            raise CableadoError(f"{quien}: {clave!r} no esta ligada")
        if len(vivas) != 1:
            raise CableadoError(
                f"{quien}: {len(vivas)} posiciones vivas; {clave!r} no identifica una"
            )
        return vivas[0].id

    def dimensionar_lote(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        # ADR-0053 §1.1: se anota y el lote se resuelve al colocar, con el stop ya escrito
        o = ctx.orden
        if o is None:
            z = _zona(ligaduras, "Z", "dimensionar_lote")
            o = ctx.orden = OrdenEnPreparacion(z)
        o.lotaje = (
            registro.opcion(str(args["base"])),
            registro.porcentaje(str(args["riesgo"])).valor,
            registro.opcion(str(args["sobre"])),
        )
        return []

    def escribir_stop_en_la_orden(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        o = _orden("escribir_stop_en_la_orden")
        registro.opcion(str(args["donde"]))  # en_la_orden: el stop viaja en la orden (A-11)
        fraccion = registro.fraccion(str(args["nivel"])).valor
        distancia = int(
            (Decimal(o.zona.distancia_completa) * fraccion).to_integral_value(ROUND_DOWN)
        )
        o.stop = (
            o.zona.entrada - distancia if o.zona.lado == "compra" else o.zona.entrada + distancia
        )
        return []

    def fijar_objetivo(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        o = _orden("fijar_objetivo")
        multiplo = registro.decimal(str(args["multiplo"]))
        sobre = registro.opcion(str(args["sobre"]))
        if sobre == "caja_completa":
            base = o.zona.distancia_completa
        else:
            if o.stop is None:
                raise CableadoError("fijar_objetivo sobre riesgo_real sin stop escrito")
            base = abs(o.zona.entrada - o.stop)
        if (
            registro.booleano(str(args["extension"]))
            or registro.opcion(str(args["parciales"])) == SI
        ):
            ctx.huecos.add("accion:fijar_objetivo:extension_o_parciales")
            raise CableadoError("fijar_objetivo con extension o parciales activos: sin contrato")
        distancia = int((Decimal(base) * multiplo).to_integral_value(ROUND_DOWN))
        o.objetivo = (
            o.zona.entrada + distancia if o.zona.lado == "compra" else o.zona.entrada - distancia
        )
        return []

    def redondear_lote(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        o = _orden("redondear_lote")
        lote = _lote_resuelto(o)
        if lote is None:
            return []
        paso, minimo = registro.lotes(str(args["paso"])), registro.lotes(str(args["minimo"]))
        registro.decimal(str(args["contrato"]))
        o.lote = max((lote / paso).to_integral_value(ROUND_DOWN) * paso, minimo)
        return []

    def _lote_resuelto(o: OrdenEnPreparacion) -> Decimal | None:
        if o.lote is not None:
            return o.lote
        if o.lotaje is None or o.stop is None:
            return None
        base_lotaje, riesgo, sobre = o.lotaje
        distancia = (
            abs(o.zona.entrada - o.stop)
            if base_lotaje == "hasta_stop_fraccion"
            else o.zona.distancia_completa
        )
        if distancia <= 0:
            return None
        saldo = ctx.cuenta.saldo if sobre == "saldo_actual" else ctx.cuenta.saldo_corte
        dinero = saldo * riesgo / CIEN
        o.lote = dinero / (Decimal(distancia) / ctx.escala * ctx.contrato)
        return o.lote

    def colocar_orden_limite(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        o = _orden("colocar_orden_limite")
        z = _zona(
            ligaduras,
            str(args["en"]) if str(args["en"]) in ligaduras else "Z",
            "colocar_orden_limite",
        )
        if z.id != o.zona.id:
            raise CableadoError(
                "colocar_orden_limite: la zona ligada no es la de la orden preparada"
            )
        lote = _lote_resuelto(o)
        if o.stop is None or o.objetivo is None or lote is None or lote <= 0:
            raise CableadoError("colocar_orden_limite: la orden no lleva stop, objetivo y lote")
        id = f"o{len(ctx.broker.ordenes) + 1}"
        r = ctx.broker.colocar_limite(
            id, z.lado, z.entrada, lote, o.stop, o.objetivo, ctx.instante_ms
        )
        ctx.por_de_orden[id] = z.por
        if isinstance(r, Rechazo):
            ctx.eventos.append(EventoBroker(r.instante_ms, "rechazo", r.orden_id, z.por))
        ctx.orden = None
        return []

    def cerrar_a_mercado(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        if registro.opcion(str(args["si"])) != SI:
            return []
        pid = _posicion_ligada(ligaduras, str(args["de"]), "cerrar_a_mercado")
        try:
            ctx.broker.cerrar_a_mercado(pid, ctx.instante_ms)
        except BrokerError as exc:
            raise CableadoError(f"cerrar_a_mercado: {exc}") from exc
        return []

    def retirar_orden_limite(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        pendientes = [
            o for o in ctx.broker.ordenes.values() if o.estado in ("colocada", "modificada")
        ]
        if len(pendientes) != 1:
            raise CableadoError(f"retirar_orden_limite: {len(pendientes)} ordenes pendientes")
        ctx.broker.cancelar(pendientes[0].id, ctx.instante_ms)
        return []

    def reubicar_orden_limite(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        z = _zona(
            ligaduras,
            str(args["a"]) if str(args["a"]) in ligaduras else "Z",
            "reubicar_orden_limite",
        )
        registro.opcion(str(args["cadencia"]))
        pendientes = [
            o for o in ctx.broker.ordenes.values() if o.estado in ("colocada", "modificada")
        ]
        if len(pendientes) != 1:
            raise CableadoError(f"reubicar_orden_limite: {len(pendientes)} ordenes pendientes")
        ctx.broker.modificar(pendientes[0].id, ctx.instante_ms, precio=z.entrada)
        return []

    def mover_stop(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        pid = _posicion_ligada(ligaduras, str(args["de"]), "mover_stop")
        destino = str(args["a"])
        if not destino.endswith(".precio_entrada"):
            ctx.huecos.add(f"accion:mover_stop:{destino}")
            raise CableadoError(f"mover_stop a {destino!r}: sin contrato")
        registro.opcion(str(args["cuando"]))
        p = ctx.broker.posiciones[pid]
        ctx.broker.mover_stop(pid, p.entrada, ctx.instante_ms)
        return []

    predicados = dict(base.predicados)
    predicados.update(
        {
            "operaciones_abiertas_alcanzan": operaciones_abiertas_alcanzan,
            "se_activa_entrada": se_activa_entrada,
            "salta_stop": salta_stop,
            "se_cierra_operacion": se_cierra_operacion,
            "distancia_menor_que": distancia_menor_que,
            "no_es_multiplo_de": no_es_multiplo_de,
        }
    )
    acciones = dict(base.acciones)
    acciones.update(
        {
            "dimensionar_lote": dimensionar_lote,
            "escribir_stop_en_la_orden": escribir_stop_en_la_orden,
            "fijar_objetivo": fijar_objetivo,
            "redondear_lote": redondear_lote,
            "colocar_orden_limite": colocar_orden_limite,
            "cerrar_a_mercado": cerrar_a_mercado,
            "retirar_orden_limite": retirar_orden_limite,
            "reubicar_orden_limite": reubicar_orden_limite,
            "mover_stop": mover_stop,
        }
    )
    acumuladores = dict(base.acumuladores)
    for nombre in ACUMULADORES_DE_LA_FIRMA:
        acumuladores[nombre] = acumulador_de_la_firma(nombre)
    for nombre in ACUMULADORES_DEL_TRADER:
        acumuladores[nombre] = acumulador_del_trader(nombre)
    for id in HUECOS:
        acumuladores[id.split(":", 1)[1]] = hueco(id)
    return Primitivas(predicados=predicados, acciones=acciones, acumuladores=acumuladores)


__all__ = [
    "ACUMULADORES_DEL_TRADER",
    "ACUMULADORES_DE_LA_FIRMA",
    "HUECOS",
    "CableadoError",
    "ContextoDia",
    "EventoBroker",
    "OrdenEnPreparacion",
    "Zona",
    "clasificar_cierre",
    "primitivas_cableadas",
]
