"""Por que decide el motor: la bitacora de decisiones y la ablacion por regla (rama
`trabajo/trazas-ablacion`, R4.4; RUMBO-2026-11.md §2). DIAGNOSTICO DE CONSTRUCCION.

**Lo que es y lo que no.** Todo lo de este modulo es diagnostico sobre los meses de construccion,
por la compuerta del arnes, como la seccion de rentabilidad sobre construccion (ADR-0092 §6, y su
NOTA para la ablacion): sus recuentos no son una medida, ninguna rama de spec ni de motor se
justifica con ellos, y las ramas de spec citan al trader (`ev-*`, `fb-*`). Como se convierte una
respuesta del trader en regla lo fijara el ADR del metodo (RUMBO §1); esto no lo adelanta. Una
operacion de mas del bot no se llama error (VIDEO-JULIO.md §10, punto 4).

**La bitacora** es un observador pasivo (`MotorCableado.observador`): recibe cada cierre de M1
DESPUES de que el motor lo haya decidido, solo LEE, y escribe cada linea con el instante del cierre
en que el motor lo supo. Lo que dice: la toma de M15 y su vela, los escenarios (ADR-0066), las zonas
y sus puntos, cada orden y su vida, por que una zona no tuvo orden, los hechos que cambian y, en
cada prohibicion, los gates que la fijan (`Evento.prohibido_por`, `Evento.bloqueada_por`: los apunta
el interprete donde prohibe, sin que nada los lea para decidir).

**La ablacion** quita UNA regla VIGENTE de la lista que recibe el interprete -la spec y su sha no
cambian- y compara la corrida con la base del MISMO proceso: parejas trader-bot del criterio
(ADR-0043) que se ganan y se pierden, operaciones del bot sin pareja que aparecen y desaparecen, y
el delta de ordenes. Cada corrida lleva un motor y un estado nuevos (`motor_nuevo`); las velas y los
ticks, de solo lectura, se comparten.

**La salida** solo lleva recuentos, dias, sesiones, horas y precios de entrada: ni R, ni dinero, ni
porcentajes. Cada linea empieza por `DIAGNOSTICO-DECISIONES | ` y cada fichero lleva `DIAGNOSTICO`
en el nombre, en una carpeta dentro de `data/` que da quien llama (`comprobar_carpeta`)."""

from __future__ import annotations

import dataclasses
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from botsito.cases.criterio_fidelidad import Operacion, Tolerancias, emparejar
from botsito.domain.pivotes_m15 import ALTO, BAJO
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.cableado import Cierre, MotorCableado
from botsito.engine.interprete import ReglaEjecutable

ETIQUETA = "DIAGNOSTICO-DECISIONES"
PREFIJO_LINEA = f"{ETIQUETA} | "
MARCA_FICHERO = "DIAGNOSTICO"
CARPETA_DATOS = "data"
CARPETA_VETADA = "manifests"  # data/manifests/ es inmutable y va en git
VIGENTE = "VIGENTE"
COMPRA = "compra"


class DecisionesError(ValueError):
    """El diagnostico no corre asi: nunca se adivina."""


# ------------------------------------------------------------------------ carpeta y nombres


def comprobar_carpeta(repo: Path, carpeta: Path) -> Path:
    """La carpeta de salida, ABSOLUTA, si esta dentro de `<repo>/data/` (ignorada por git) y fuera
    de `data/manifests/`; si no, `DecisionesError`. La raiz sale del argumento, nunca de una ruta
    fija (CLAUDE.md, «Ensayos aislados», punto 2)."""
    datos = (repo / CARPETA_DATOS).resolve()
    absoluta = (carpeta if carpeta.is_absolute() else Path.cwd() / carpeta).resolve()
    if absoluta != datos and datos not in absoluta.parents:
        raise DecisionesError(
            f"--carpeta {carpeta} esta fuera de {datos}: la salida del diagnostico solo va a una "
            "carpeta ignorada de data/ (no se ha leido ni escrito nada)"
        )
    vetada = datos / CARPETA_VETADA
    if absoluta == vetada or vetada in absoluta.parents:
        raise DecisionesError(f"--carpeta {carpeta}: data/manifests/ va en git y es inmutable")
    return absoluta


def nombre_fichero(clase: str, cual: str) -> str:
    """`bitacora.DIAGNOSTICO.2026-07-03.txt`, `ablacion.DIAGNOSTICO.vigentes.txt`."""
    if not clase or not cual or "/" in cual or "\\" in cual:
        raise DecisionesError(f"nombre de fichero sin la forma esperada: {clase!r}, {cual!r}")
    return f"{clase}.{MARCA_FICHERO}.{cual}.txt"


def etiquetar(lineas: Iterable[str]) -> str:
    """Cada linea con la etiqueta delante; el texto acaba en un salto de linea."""
    return "".join(f"{PREFIJO_LINEA}{ln}\n" for ln in lineas)


# ------------------------------------------------------------------------------- ablacion


def ids_vigentes(reglas_spec: Sequence[Any]) -> tuple[str, ...]:
    """Los ids VIGENTE de la spec, en su orden."""
    return tuple(r.id for r in reglas_spec if getattr(r, "estado", None) == VIGENTE)


def sin_regla(
    reglas: Sequence[ReglaEjecutable], quitar: str | None, vigentes: Sequence[str]
) -> list[ReglaEjecutable]:
    """La lista que recibe el interprete sin la regla `quitar`, por su id y sin ningun caso
    especial; sin `quitar`, la misma lista. Un id que no sea VIGENTE da `DecisionesError` con su
    nombre."""
    if quitar is None:
        return list(reglas)
    if quitar not in vigentes:
        raise DecisionesError(
            f"{quitar} no es una regla VIGENTE de knowledge/spec/strategy_spec.yaml: la ablacion "
            "solo quita reglas vigentes"
        )
    salida = [r for r in reglas if r.id != quitar]
    if len(salida) != len(reglas) - 1:
        raise DecisionesError(f"{quitar}: VIGENTE pero no llega al interprete (sin `forma`)")
    return salida


# Los campos de `MotorCableado`: la configuracion se copia de la plantilla; el estado de la corrida
# nace de nuevo en cada motor. Un campo nuevo que no este en ninguna de las dos listas hace fallar
# `motor_nuevo` (y su test): hay que decidir de cual es.
CAMPOS_DE_CONFIGURACION = frozenset(
    {
        "vocabulario", "registro", "mercados", "reglas_broker", "reglas_fase", "config_llenado",
        "contrato", "depuracion", "perfil", "fase", "primitivas_extra", "acumuladores_extra",
        "zonas_de", "tope", "limpia", "stops_level_diagnostico", "tipo_orden", "cuenta_diaria",
        "operaciones_trader", "criterio",
    }
)  # fmt: skip
CAMPOS_DE_ESTADO = frozenset(
    {
        "reglas", "observador", "cuenta", "seguidor", "racha", "primero_en_tocar",
        "mes_en_curso", "cuentas_cerradas", "trazas_broker", "brokers", "estados",
    }
)  # fmt: skip


def motor_nuevo(
    plantilla: MotorCableado,
    reglas: Sequence[ReglaEjecutable],
    observador: Callable[[Cierre], None] | None = None,
) -> MotorCableado:
    """Un `MotorCableado` con la configuracion de `plantilla`, `reglas` y el estado de una corrida
    que empieza: sin cuenta, sin brokers ni trazas. Los mercados (velas y ticks, inmutables) se
    comparten; nada mutable de la plantilla pasa al motor nuevo."""
    campos = {f.name for f in dataclasses.fields(MotorCableado)}
    sin_clase = campos - CAMPOS_DE_CONFIGURACION - CAMPOS_DE_ESTADO
    if sin_clase:
        raise DecisionesError(f"campos de MotorCableado sin clasificar: {sorted(sin_clase)}")
    copia = {n: getattr(plantilla, n) for n in CAMPOS_DE_CONFIGURACION}
    return MotorCableado(**copia, reglas=list(reglas), observador=observador)


# --------------------------------------------------------------------------------- resumen

ClaveOp = tuple[str, str, str, str, str]  # dia, sesion, direccion, instante ISO, entrada


def clave_op(op: Operacion) -> ClaveOp:
    return (op.dia, op.sesion, op.direccion, op.instante.isoformat(), str(op.entrada))


@dataclass(frozen=True)
class Resumen:
    """Lo que una corrida deja para compararla: sin R, sin dinero, sin porcentajes."""

    nombre: str
    parejas: frozenset[tuple[ClaveOp, ClaveOp]] = frozenset()
    de_mas: frozenset[ClaveOp] = frozenset()  # del bot, sin pareja, en dias con trader
    fuera: frozenset[ClaveOp] = frozenset()  # del bot, en dias sin ninguna del trader
    ordenes: int = 0
    no_enviadas: int = 0
    rechazos: int = 0
    suspendidas: tuple[str, ...] = ()  # meses cuya cuenta acabo SUSPENDIDA
    error: str | None = None

    def recuentos(self) -> tuple[int, ...]:
        return (
            len(self.parejas), len(self.de_mas), len(self.fuera), self.ordenes,
            self.no_enviadas, self.rechazos, len(self.suspendidas),
        )  # fmt: skip


def resumir(
    nombre: str,
    motor: MotorCableado,
    operaciones_bot: Sequence[Operacion],
    operaciones_trader: Sequence[Operacion],
    tol: Tolerancias,
) -> Resumen:
    """Las parejas por el emparejamiento del criterio (ADR-0043), como `medir`: solo puntuan las
    del bot en dias con alguna del trader."""
    dias_trader = {t.dia for t in operaciones_trader}
    puntuables = [b for b in operaciones_bot if b.dia in dias_trader]
    parejas = emparejar(operaciones_trader, puntuables, tol)
    con_pareja = {clave_op(p.bot) for p in parejas}
    from botsito.engine.cableado import cuentas_del_tramo
    from botsito.engine.cuenta import EstadoCuenta

    suspendidas = tuple(
        c.mes for c in cuentas_del_tramo(motor) if c.estado is EstadoCuenta.SUSPENDIDA
    )
    return Resumen(
        nombre=nombre,
        parejas=frozenset((clave_op(p.trader), clave_op(p.bot)) for p in parejas),
        de_mas=frozenset(clave_op(b) for b in puntuables if clave_op(b) not in con_pareja),
        fuera=frozenset(clave_op(b) for b in operaciones_bot if b.dia not in dias_trader),
        ordenes=sum(len(b.ordenes) for b in motor.brokers.values()),
        no_enviadas=sum(len(t.no_enviadas) for t in motor.trazas_broker.values()),
        rechazos=sum(t.rechazos for t in motor.trazas_broker.values()),
        suspendidas=suspendidas,
    )


def _op(c: ClaveOp) -> str:
    dia, sesion, direccion, instante, entrada = c
    return f"{dia} {sesion} {direccion} {instante[11:19]} {entrada}"


def comparar(base: Resumen, otra: Resumen) -> list[str]:
    """Lo que cambia de `base` a `otra`, en lineas: recuentos y que operaciones."""
    if otra.error is not None:
        return [f"{otra.nombre} | la corrida fallo: {otra.error}"]
    nb, no = base.recuentos(), otra.recuentos()
    nombres = ("parejas", "de mas", "fuera", "ordenes", "no enviadas", "rechazos", "suspendidas")
    cab = "; ".join(f"{n} {a} -> {b}" for n, a, b in zip(nombres, nb, no, strict=True) if a != b)
    if sin_delta(base, otra):
        cab = "sin delta"
    elif not cab:
        cab = "mismos recuentos, distintas operaciones"
    lineas = [f"{otra.nombre} | {cab}"]
    for t, b in sorted(otra.parejas - base.parejas):
        lineas.append(f"{otra.nombre} | pareja que se gana: trader {_op(t)} con bot {_op(b)}")
    for t, b in sorted(base.parejas - otra.parejas):
        lineas.append(f"{otra.nombre} | pareja que se pierde: trader {_op(t)} con bot {_op(b)}")
    for c in sorted(otra.de_mas - base.de_mas):
        lineas.append(f"{otra.nombre} | de mas que aparece: {_op(c)}")
    for c in sorted(base.de_mas - otra.de_mas):
        lineas.append(f"{otra.nombre} | de mas que desaparece: {_op(c)}")
    for c in sorted(otra.fuera - base.fuera):
        lineas.append(f"{otra.nombre} | en dia sin trader, aparece: {_op(c)}")
    for c in sorted(base.fuera - otra.fuera):
        lineas.append(f"{otra.nombre} | en dia sin trader, desaparece: {_op(c)}")
    if otra.suspendidas != base.suspendidas:
        lineas.append(
            f"{otra.nombre} | cuentas suspendidas: {list(base.suspendidas)} -> "
            f"{list(otra.suspendidas)}"
        )
    return lineas


def sin_delta(base: Resumen, otra: Resumen) -> bool:
    return otra.error is None and dataclasses.replace(otra, nombre=base.nombre) == base


# -------------------------------------------------------------------------------- bitacora


def _vela(v: Any, escala: int) -> str:
    if v is None:
        return "sin vela"
    return "/".join(_precio(int(x), escala) for x in (v.abierta, v.maxima, v.minima, v.cierre))


def _precio(puntos: int, escala: int) -> str:
    return f"{Decimal(puntos) / Decimal(escala):.5f}"


@dataclass
class _Sesion:
    toma: tuple[Any, ...] | None = None
    escenarios: list[tuple[int, str | None]] = field(default_factory=list)  # (n, terminado)
    prohibido: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass
class _Dia:
    lineas: list[tuple[int, str]] = field(default_factory=list)  # (instante del cierre, texto)
    sesiones: dict[str, _Sesion] = field(default_factory=dict)
    zonas: set[str] = field(default_factory=set)
    ordenes: dict[str, str] = field(default_factory=dict)  # id -> estado visto
    posiciones: dict[str, bool] = field(default_factory=dict)  # id -> abierta vista
    no_enviadas: int = 0
    hechos: dict[str, str] = field(default_factory=dict)


class Bitacora:
    """El observador de `MotorCableado`: por cada cierre, lo que cambio. Escribe el detalle solo de
    los dias de `detalle`; de todos, los recuentos por regla (cuantos eventos disparo, en cuantos
    quedo desconocida, cuantas acciones bloqueo) que dan el conjunto de control."""

    def __init__(self, reglas: Sequence[ReglaEjecutable], detalle: Iterable[str] = ()) -> None:
        self.detalle = frozenset(detalle)
        self.prohibe = {
            r.id: tuple(str(e) for e in r.entonces.get("prohibe", []) or []) for r in reglas
        }
        self.disparos: Counter[str] = Counter()
        self.desconocidas: Counter[str] = Counter()
        self.bloqueos: Counter[str] = Counter()  # por gate que bloquea
        self.eventos = 0
        self._dias: dict[str, _Dia] = {}

    # el resultado ---------------------------------------------------------------------------

    def dias(self) -> tuple[str, ...]:
        return tuple(sorted(self._dias))

    def lineas(self, dia: str) -> list[tuple[int, str]]:
        """(minuto UTC del cierre en que el motor lo supo, texto), en orden."""
        return list(self._dias[dia].lineas)

    def texto(self, dia: str) -> str:
        return etiquetar(t for _, t in self._dias[dia].lineas)

    def control(self, vigentes: Sequence[str]) -> tuple[str, ...]:
        """Las VIGENTE que en toda la corrida ni dispararon ni quedaron desconocidas."""
        return tuple(r for r in vigentes if not self.disparos[r] and not self.desconocidas[r])

    def recuento(self, vigentes: Sequence[str]) -> list[str]:
        lineas = [f"eventos observados: {self.eventos}"]
        for r in vigentes:
            lineas.append(
                f"{r}: dispara en {self.disparos[r]} eventos; desconocida en "
                f"{self.desconocidas[r]}; bloquea {self.bloqueos[r]} acciones"
            )
        return lineas

    # el observador --------------------------------------------------------------------------

    def __call__(self, c: Cierre) -> None:
        ev = c.evento
        self.eventos += 1
        for r in ev.disparadas:
            self.disparos[r] += 1
        for r in {r for r, _ in ev.no_implementadas}:
            self.desconocidas[r] += 1
        for gates in ev.bloqueada_por.values():
            for g, _ in gates:
                self.bloqueos[g] += 1
        if c.dia not in self.detalle:
            return
        d = self._dias.setdefault(c.dia, _Dia())
        self._cierre(d, c)

    def _hora(self, c: Cierre, minuto: int) -> str:
        t = datetime.fromtimestamp(minuto * 60, UTC)
        return f"{t.astimezone(ZoneInfo(c.huso)):%H:%M} ({t:%H:%M}Z)"

    def _hora_ms(self, c: Cierre, ms: int) -> str:
        t = datetime.fromtimestamp(ms / 1000, UTC)
        return f"{t.astimezone(ZoneInfo(c.huso)):%H:%M:%S} ({t:%H:%M:%S}Z)"

    def _cierre(self, d: _Dia, c: Cierre) -> None:
        sesion = c.sesion or "-"
        pre = f"{c.dia} {sesion} {self._hora(c, c.instante)} | "
        salida: list[str] = []
        mem_dia: Mapping[str, Any] = c.estado.memoria.get("zona_de_entrada", {})
        por_sesion: Mapping[str, Any] = mem_dia.get("por_sesion", {})
        mem = por_sesion.get(sesion, {}) if c.sesion else {}
        s = d.sesiones.setdefault(sesion, _Sesion())
        self._tomas(c, s, mem, salida)
        self._escenarios(c, s, mem, salida)
        self._zonas(c, d, mem_dia, por_sesion, salida)
        self._hechos(c, d, salida)
        self._prohibiciones(c, s, salida)
        self._bloqueos(c, salida)
        self._ordenes(c, d, salida)
        d.lineas += [(c.instante, pre + x) for x in salida]

    def _tomas(self, c: Cierre, s: _Sesion, mem: Mapping[str, Any], salida: list[str]) -> None:
        toma = mem.get("toma")
        if toma is None:
            return
        clave = (toma["instante"], tuple(toma["pivote"]))
        if clave == s.toma:
            return
        s.toma = clave
        lado_pivote, nivel, formado = toma["pivote"]
        m1 = c.datos.ultima_m1_cerrada(int(toma["instante"]))
        cuerpo = "sin vela"
        if m1 is not None:
            pasada = int(m1.cierre) < nivel if lado_pivote == BAJO else int(m1.cierre) > nivel
            cuerpo = "CIERRA pasada la linea (cuerpo)" if pasada else "NO cierra pasada la linea"
        salida.append(
            f"toma de M15: el {lado_pivote} de M15 en {_precio(nivel, c.escala)} (formado "
            f"{self._hora(c, int(formado))}), para {toma['lado']}; M1 de la toma (cierra "
            f"{self._hora(c, int(toma['instante']))}) o/h/l/c {_vela(m1, c.escala)}: {cuerpo}"
        )

    def _escenarios(self, c: Cierre, s: _Sesion, mem: Mapping[str, Any], salida: list[str]) -> None:
        vistos = [(int(e["n"]), e["terminado"]) for e in mem.get("escenarios", []) or []]
        previos = dict(s.escenarios)
        for n, terminado in vistos:
            if n not in previos:
                e = mem["escenarios"][n - 1]
                hora = self._hora(c, int(e["toma"]["instante"]))
                salida.append(f"escenario {n} abierto, con la toma de {hora}")
            if terminado is not None and previos.get(n) is None:
                salida.append(f"escenario {n} terminado: {terminado}")
        s.escenarios = vistos

    def _linea_m15(self, c: Cierre, nivel: int, toma: Mapping[str, Any] | None) -> str:
        if toma is not None and int(toma["nivel"]) == nivel:
            return "SI: es el nivel de la toma de M15"
        for lado in (ALTO, BAJO):
            try:
                p = c.datos.liquidez_m15(c.instante, lado)
            except (AttributeError, LookupError):
                return "sin lectura de M15"
            if p is not None and int(p.nivel) == nivel:
                return f"SI: es la liquidez de M15 {lado} de ese instante"
        return "no: ningun nivel de M15 de ese instante"

    def _zonas(
        self,
        c: Cierre,
        d: _Dia,
        mem_dia: Mapping[str, Any],
        por_sesion: Mapping[str, Any],
        salida: list[str],
    ) -> None:
        zonas: Mapping[str, Any] = mem_dia.get("zonas", {})
        for zid in sorted(set(zonas) - d.zonas, key=lambda z: int(z.split(":")[-1])):
            d.zonas.add(zid)
            z = zonas[zid]
            ses, n, punto, toma = "-", "-", None, None
            for nombre, m in por_sesion.items():
                for e in m.get("escenarios", []) or []:
                    if zid in e["zonas"]:
                        ses, n, toma = nombre, str(e["n"]), e["toma"]
                punto = punto or (m.get("punto_de_zona", {}) or {}).get(zid)
            texto_punto = "sin punto"
            if punto is not None:
                nivel_s, inicio_s = str(punto).split("@")
                texto_punto = (
                    f"punto {_precio(int(nivel_s), c.escala)}, vela contraria que lo forma: la "
                    f"que abre a las {self._hora(c, int(inicio_s))}"
                )
            cero, uno = _precio(z.entrada, c.escala), _precio(z.extremo, c.escala)
            salida.append(
                f"{zid} ({z.lado}) ligada en la sesion {ses}, escenario {n}: 0 = {cero}, 1 = "
                f"{uno}; {texto_punto}; linea de M15: {self._linea_m15(c, int(z.entrada), toma)}"
            )
            if zid not in set(c.ctx.zona_de_orden.values()):
                salida.append(f"{zid} sin orden en este cierre: {self._sin_orden(c, zid, ses)}")

    def _sin_orden(self, c: Cierre, zid: str, ses: str) -> str:
        motivos = []
        m = c.estado.memoria.get("zona_de_entrada", {}).get("por_sesion", {}).get(ses, {})
        if zid in (m.get("usadas") or set()):
            motivos.append("zona usada")
        punto = (m.get("punto_de_zona") or {}).get(zid)
        if punto is not None and punto in (m.get("rechazados") or set()):
            motivos.append("punto gastado (rechazo)")
        escenarios = m.get("escenarios") or []
        if escenarios and escenarios[-1]["terminado"] is not None:
            motivos.append(f"escenario terminado ({escenarios[-1]['terminado']})")
        if c.estado.broker.get("orden_limite_pendiente"):
            motivos.append("hay una orden pendiente")
        if c.estado.broker.get("operacion_abierta"):
            motivos.append("hay una posicion abierta")
        if any(m_ == "accion:colocar_orden_limite" for _, m_, _ in c.evento.bloqueadas):
            motivos.append("la colocacion se bloqueo (abajo)")
        disp = [r for r in ("RN-011", "RN-015") if r in c.evento.disparadas]
        motivos.append(f"disparan {', '.join(disp) or 'ni RN-011 ni RN-015'}")
        return "; ".join(motivos)

    def _hechos(self, c: Cierre, d: _Dia, salida: list[str]) -> None:
        quien = {h: r for r, h, _ in c.evento.fijados}
        ahora = dict(c.estado.hechos)
        for h in sorted(set(ahora) | set(d.hechos)):
            a, b = d.hechos.get(h), ahora.get(h)
            if a != b:
                por = quien.get(h, "sin regla en este cierre")
                salida.append(f"hecho {h}: {a or '-'} -> {b or '-'} ({por})")
        d.hechos = ahora

    def _prohibiciones(self, c: Cierre, s: _Sesion, salida: list[str]) -> None:
        ahora: dict[str, tuple[str, ...]] = {}
        for efecto, gates in c.evento.prohibido_por.items():
            ahora[efecto] = tuple(f"{g} [dispara]" for g in gates)
        for efecto, gates in c.evento.quizas_por.items():
            ahora[efecto] = ahora.get(efecto, ()) + tuple(f"{g} [desconocido]" for g in gates)
        for efecto in sorted(set(ahora) | set(s.prohibido)):
            if ahora.get(efecto) != s.prohibido.get(efecto):
                if efecto in ahora:
                    salida.append(f"prohibido {efecto} por: {', '.join(ahora[efecto])}")
                else:
                    salida.append(f"deja de estar prohibido {efecto}")
        s.prohibido = ahora

    def _bloqueos(self, c: Cierre, salida: list[str]) -> None:
        for clave in sorted(c.evento.bloqueadas):
            regla, accion, motivo = clave
            gates = c.evento.bloqueada_por.get(clave, ())
            quien = ", ".join(f"{g} [{t}]" for g, t in gates) or "SIN GATE REGISTRADO"
            salida.append(f"{regla} no ejecuta {accion} ({motivo}): la prohiben {quien}")

    def _ordenes(self, c: Cierre, d: _Dia, salida: list[str]) -> None:
        for zona_id_t in c.ctx.no_enviadas[d.no_enviadas :]:
            ms, zid, motivo, _ = zona_id_t
            salida.append(f"orden NO enviada en {zid} a las {self._hora_ms(c, ms)}: {motivo}")
        d.no_enviadas = len(c.ctx.no_enviadas)
        for oid in sorted(c.broker.ordenes, key=lambda x: int(x[1:])):
            o = c.broker.ordenes[oid]
            if d.ordenes.get(oid) == o.estado:
                continue
            zid = c.ctx.zona_de_orden.get(oid, "-")
            if oid not in d.ordenes:
                precio, stop = _precio(o.precio, c.escala), _precio(o.stop, c.escala)
                salida.append(
                    f"orden {oid} ({o.tipo}, {o.lado}) en {zid}: precio {precio}, stop {stop}, "
                    f"objetivo {_precio(o.objetivo, c.escala)}, lote {o.lotes}; estado {o.estado}"
                )
            else:
                salida.append(
                    f"orden {oid}: {d.ordenes[oid]} -> {o.estado} a las "
                    f"{self._hora_ms(c, o.ultimo_cambio_ms)}"
                )
                if o.estado == "llenada":
                    salida.append(self._llenado(c, oid, o, zid))
            d.ordenes[oid] = o.estado
        for pid, p in sorted(c.broker.posiciones.items()):
            if d.posiciones.get(pid) is False or (d.posiciones.get(pid) and p.abierta):
                continue
            if not p.abierta:
                salida.append(
                    f"posicion {pid} cerrada por {p.motivo_cierre} a las "
                    f"{self._hora_ms(c, int(p.cerrada_ms or 0))}"
                )
            d.posiciones[pid] = p.abierta

    def _llenado(self, c: Cierre, oid: str, o: Any, zid: str) -> str:
        """(a) del punto 2 de la respuesta a la fase 0: el llenado frente a la primera M1 que
        cierra mas alla del precio de la orden, y si la M1 del llenado cierra mas alla (cuerpo).
        Solo velas ya cerradas en este instante."""
        minuto = o.ultimo_cambio_ms // MS_POR_MINUTO

        precio = int(o.precio)

        def mas_alla(v: Any) -> bool:
            return int(v.cierre) > precio if o.lado == COMPRA else int(v.cierre) < precio

        desde = o.colocada_ms // MS_POR_MINUTO
        antes = [v for v in c.datos.m1_entre(desde, minuto) if mas_alla(v)]
        vela = next(iter(c.datos.m1_entre(minuto, minuto + 1)), None)
        if minuto + 1 > c.instante:
            de_la_vela = "su M1 aun no ha cerrado"
        elif vela is None:
            de_la_vela = "sin M1"
        else:
            de_la_vela = (
                "la M1 del llenado CIERRA mas alla (cuerpo)"
                if mas_alla(vela)
                else ("la M1 del llenado NO cierra mas alla (mecha)")
            )
        if antes:
            orden = (
                f"DESPUES de la primera M1 que cierra mas alla ({self._hora(c, int(antes[0].fin))})"
            )
        else:
            orden = "ANTES de que ninguna M1 cierre mas alla del precio desde que se coloco"
        return f"llenado de {oid} ({zid}) a {_precio(o.precio, c.escala)}: {orden}; {de_la_vela}"


# ---------------------------------------------------------------------------- las corridas


class ParadaError(DecisionesError):
    """Una condicion de PARADA medida; lleva los ficheros ya calculados para escribirlos igual."""

    def __init__(self, motivo: str, salida: Mapping[str, str]) -> None:
        super().__init__(motivo)
        self.salida = dict(salida)


class BaseQueNoCuadraError(ParadaError):
    """La base corrida dos veces en el mismo proceso no da lo mismo: PARADA (respuesta del
    consultor a la fase 0, punto 6)."""


class ControlConDeltaError(ParadaError):
    """Una regla del conjunto de control da delta: PARADA (respuesta a la fase 0, punto 7)."""


def correr_diagnostico(
    plantilla: MotorCableado,
    reglas: Sequence[ReglaEjecutable],
    vigentes: Sequence[str],
    correr: Callable[[MotorCableado], Sequence[Operacion]],
    operaciones_trader: Sequence[Operacion],
    tol: Tolerancias,
    detalle: Iterable[str] = (),
    ablaciones: Sequence[str] = (),
    avisar: Callable[[str], None] = lambda _t: None,
) -> dict[str, str]:
    """La base con la bitacora, la base otra vez sin ella (tiene que dar lo mismo), el conjunto de
    control y cada ablacion pedida, en ese orden. `correr` corre un motor sobre los dias y devuelve
    las operaciones del bot. Devuelve los ficheros a escribir (nombre -> texto etiquetado).

    Los ids pedidos se comprueban ANTES de correr nada. Si la base repetida no cuadra, o si una
    regla del control (las VIGENTE que en la base ni disparan ni quedan desconocidas) da delta, se
    levanta el error de PARADA despues de escribir lo que haya."""
    for quitar in ablaciones:
        sin_regla(reglas, quitar, vigentes)
    bitacora = Bitacora(reglas, detalle)

    def una(nombre: str, lista: Sequence[ReglaEjecutable], obs: Any = None) -> Resumen:
        motor = motor_nuevo(plantilla, lista, obs)
        try:
            ops = correr(motor)
        except Exception as exc:  # una ablacion puede romper el motor: se dice y se sigue
            avisar(f"{nombre}: fallo ({type(exc).__name__})")
            return Resumen(nombre, error=f"{type(exc).__name__}: {exc}")
        r = resumir(nombre, motor, ops, operaciones_trader, tol)
        avisar(f"{nombre}: {r.recuentos()}")
        return r

    base = una("base", reglas, bitacora)
    if base.error is not None:
        raise DecisionesError(f"la base fallo: {base.error}")
    repetida = una("base repetida", reglas)
    control = bitacora.control(vigentes)
    lineas = [
        "base: parejas, de mas, fuera, ordenes, no enviadas, rechazos, cuentas suspendidas = "
        f"{base.recuentos()}",
        f"base repetida en el mismo proceso, sin bitacora: {repetida.recuentos()}; "
        f"igual: {'si' if sin_delta(base, repetida) else 'NO'}",
        f"control (VIGENTE que ni disparan ni quedan desconocidas en la base): "
        f"{', '.join(control) or 'ninguna'}",
        *bitacora.recuento(vigentes),
    ]
    salida = {nombre_fichero("bitacora", d): bitacora.texto(d) for d in bitacora.dias()}
    fallos: list[str] = []
    if not sin_delta(base, repetida):
        fallos.append("la base repetida no cuadra")
    else:
        for quitar in ablaciones:
            r = una(f"sin {quitar}", sin_regla(reglas, quitar, vigentes))
            en_control = quitar in control
            lineas += [f"[{'control' if en_control else 'medida'}] {x}" for x in comparar(base, r)]
            if en_control and not sin_delta(base, r):
                fallos.append(f"{quitar} esta en el control y da delta")
    cual = (
        "vigentes"
        if list(ablaciones) == list(vigentes)
        else ("base" if not ablaciones else "-".join(ablaciones))
    )
    salida[nombre_fichero("ablacion", cual)] = etiquetar(lineas)
    if fallos:
        error = BaseQueNoCuadraError if "base" in fallos[0] else ControlConDeltaError
        raise error("; ".join(fallos), salida)
    return salida


__all__ = [
    "BaseQueNoCuadraError",
    "ControlConDeltaError",
    "ParadaError",
    "correr_diagnostico",
    "CAMPOS_DE_CONFIGURACION",
    "CAMPOS_DE_ESTADO",
    "ETIQUETA",
    "PREFIJO_LINEA",
    "Bitacora",
    "DecisionesError",
    "Resumen",
    "comparar",
    "comprobar_carpeta",
    "etiquetar",
    "ids_vigentes",
    "motor_nuevo",
    "nombre_fichero",
    "resumir",
    "sin_delta",
    "sin_regla",
]
