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
from decimal import ROUND_DOWN, ROUND_UP, Decimal
from typing import Any, cast

from botsito.config.registro import Registro
from botsito.domain.estructura_m1 import zona_posterior_completada
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.valores import CIEN
from botsito.engine.broker import LLENADA, MANUAL, Broker, BrokerError, Rechazo
from botsito.engine.cuenta import CuentaViva
from botsito.engine.entrada import STOP_EN_RUPTURA
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
from botsito.engine.zonas import (
    Zona,
    marcar_rechazada,
    marcar_usada,
    orden_nace_en_el_punto,
    punto_rechazado,
    zona_del_punto,
    zonas_del_dia,
    zonas_usadas,
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
# Las opciones de `stop_fraccion_redondeo`: hacia donde va el stop cuando el nivel de la caja
# no cae en un punto exacto. Se redondea la DISTANCIA de la entrada al stop: hacia abajo lo
# acerca a la entrada y hacia arriba lo aleja, y el lote sale de esa distancia (RN-011).
REDONDEO_DEL_STOP = {"hacia_la_entrada": ROUND_DOWN, "alejandose_de_la_entrada": ROUND_UP}
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
    zona_de_orden: dict[str, str] = field(default_factory=dict)  # orden_id -> zona_id
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


def primitivas_cableadas(
    registro: Registro,
    ctx: ContextoDia,
    limpia: str | None = None,
    tipo_orden: str | None = None,
) -> Primitivas:
    """Las primitivas de ADR-0048 mas las del broker, la cuenta y las acciones de la orden. Con
    `limpia` (A-21), la geometria de la zona de entrada produce las zonas que las acciones leen.
    Con `tipo_orden` (A-47, ADR-0056 §1) `stop_en_ruptura`, la entrada va al broker como orden
    STOP, al mismo precio y en el mismo instante que la limite (ADR-0058, PROVISIONAL); sin el, o
    con `limite_en_retroceso`, como LIMITE, que es lo de siempre."""
    base = primitivas_escritas(registro, None, limpia)

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

    def _pendientes() -> list[Any]:
        return [o for o in ctx.broker.ordenes.values() if o.estado in ("colocada", "modificada")]

    def _punto_nuevo(momento: Momento, estado: EstadoDia) -> Zona | None:
        """RN-006 en la vida de la orden stop (ADR-0064): la zona de un punto de breaker NUEVO de
        esta sesion, distinto del de la orden pendiente, que es de esta misma sesion; o None."""
        pendientes = _pendientes()
        if len(pendientes) != 1:
            return None
        de_la_orden = ctx.zona_de_orden.get(pendientes[0].id)
        usadas = zonas_usadas(estado, momento.sesion)
        if de_la_orden is None or de_la_orden not in usadas:
            return None  # la orden no es de esta sesion: cada sesion es un escenario (A-46)
        z = zona_del_punto(registro, momento, estado)
        if (
            z is None
            or z.id == de_la_orden
            or z.id in usadas
            or punto_rechazado(estado, momento.sesion, z.id)
        ):
            return None
        return z

    def toca_colocar_orden_limite(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        # DECISION de ADR-0064 (la lectura mas conservadora): con la vida de la orden stop, una
        # sesion en la que ya se lleno una orden no coloca otra, como la zona de un solo uso
        if orden_nace_en_el_punto(registro):
            usadas = zonas_usadas(estado, momento.sesion)
            ordenes = {o for o, z in ctx.zona_de_orden.items() if z in usadas}
            if any(p.orden_id in ordenes for p in ctx.broker.posiciones.values()):
                return Resultado(Tri.NO)
        return base.predicados["toca_colocar_orden_limite"](args, momento, estado)

    def se_completa_zona_de_control(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        # Con `posterior_a`, el break even de RN-014 (ADR-0061). Sin el, la reubicacion de la orden
        # pendiente (RN-006): con la vida de la orden stop (ADR-0064), la zona se completa cuando
        # se forma un punto de breaker nuevo; con la orden en el esquema, sigue sin escribirse.
        if "posterior_a" not in args:
            if not orden_nace_en_el_punto(registro):
                return NoImplementada("predicado:se_completa_zona_de_control")
            registro.opcion(str(args["criterio"]))  # lo nombra la forma
            z = _punto_nuevo(momento, estado)
            if z is None:
                return Resultado(Tri.NO)
            return Resultado(Tri.SI, {str(args.get("liga", "Z")): z.id})
        criterio = registro.opcion(str(args["criterio"]))  # lo nombra la forma
        vivas = [p for p in ctx.broker.posiciones.values() if p.abierta]
        if len(vivas) != 1:
            return Resultado(Tri.NO)
        p = vivas[0]
        try:
            # las M1 cerradas desde la que contiene el llenado: solo lo de despues de la entrada
            m1 = momento.datos.m1_entre(p.abierta_ms // MS_POR_MINUTO, int(momento.instante))
        except AttributeError:
            return NoImplementada("predicado:se_completa_zona_de_control:sin M1")
        k = zona_posterior_completada(m1, p.lado, criterio)
        # SI exactamente en el cierre de la M1 que pasa el punto, y sin efectos (ADR-0055 §1)
        if k is None or int(m1[k].fin) != int(momento.instante):
            return Resultado(Tri.NO)
        liga = str(args.get("liga", "Z"))
        return Resultado(Tri.SI, {liga: f"zona_posterior:{int(momento.instante)}"})

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

    def _zona(ligaduras: Mapping[str, str], clave: str, quien: str, estado: EstadoDia) -> Zona:
        ref = ligaduras.get(clave)
        z = None
        if ref is not None:
            # las zonas del contexto (sinteticas, tests) y las que el productor ligo en el dia
            z = ctx.zonas.get(str(ref)) or zonas_del_dia(estado).get(str(ref))
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
        # ADR-0053 §1.1: se anota y el lote se resuelve al colocar, con el stop ya escrito.
        # RN-011 PREPARA la orden de la zona que liga, y siempre de cero: una preparacion
        # anterior que un gate no dejo enviar (RN-015 apaga `orden_dimensionada`, ADR-0032) no
        # se arrastra a la zona siguiente. Con una zona por dia no podia pasar; desde A-46
        # cada sesion liga la suya.
        o = ctx.orden = OrdenEnPreparacion(_zona(ligaduras, "Z", "dimensionar_lote", estado))
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
        hacia = registro.opcion(str(args["redondeo"]))  # lo nombra la forma (ADR-0019 §1)
        modo = REDONDEO_DEL_STOP.get(hacia)
        if modo is None:
            raise CableadoError(f"escribir_stop_en_la_orden: redondeo {hacia!r} sin contrato")
        distancia = int((Decimal(o.zona.distancia_completa) * fraccion).to_integral_value(modo))
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
            estado,
        )
        if z.id != o.zona.id:
            raise CableadoError(
                "colocar_orden_limite: la zona ligada no es la de la orden preparada"
            )
        lote = _lote_resuelto(o)
        if o.stop is None or o.objetivo is None or lote is None or lote <= 0:
            raise CableadoError("colocar_orden_limite: la orden no lleva stop, objetivo y lote")
        id = f"o{len(ctx.broker.ordenes) + 1}"
        colocar = (
            ctx.broker.colocar_stop if tipo_orden == STOP_EN_RUPTURA else ctx.broker.colocar_limite
        )
        r = colocar(id, cast(Lado, z.lado), z.entrada, lote, o.stop, o.objetivo, ctx.instante_ms)
        ctx.por_de_orden[id] = z.por
        ctx.zona_de_orden[id] = z.id
        marcar_usada(estado, momento.sesion, z.id)
        if isinstance(r, Rechazo):
            ctx.eventos.append(EventoBroker(r.instante_ms, "rechazo", r.orden_id, z.por))
            marcar_rechazada(estado, momento.sesion, z.id)
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
            estado,
        )
        registro.opcion(str(args["cadencia"]))
        pendientes = _pendientes()
        if len(pendientes) != 1:
            raise CableadoError(f"reubicar_orden_limite: {len(pendientes)} ordenes pendientes")
        if orden_nace_en_el_punto(registro):
            # ADR-0056 §7: se cancela y RN-011 y RN-015 la vuelven a colocar en el punto nuevo,
            # con la caja, el stop y el lote recalculados. Los hechos del broker se refrescan para
            # que lo hagan en este mismo cierre de M1 y no en el siguiente
            ctx.broker.cancelar(pendientes[0].id, ctx.instante_ms)
            estado.broker = ctx.broker.hechos()
            return []
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
            "se_completa_zona_de_control": se_completa_zona_de_control,
            "distancia_menor_que": distancia_menor_que,
            "no_es_multiplo_de": no_es_multiplo_de,
        }
    )
    if "toca_colocar_orden_limite" in base.predicados:  # solo con la geometria de A-21
        predicados["toca_colocar_orden_limite"] = toca_colocar_orden_limite
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
