"""El interprete del arbol generico de `forma` (ADR-0030), con el arnes de ADR-0048.

Recorre la `forma` de las reglas VIGENTES y despacha por nombre a primitivas escritas a mano: una
por predicado, una por accion y una por acumulador (ADR-0030 §1). No sabe nada de ninguna regla en
concreto: lo que una regla hace lo dice su arbol.

- **Un evento se evalua a punto fijo con refraccion** (ADR-0028 §4): cada regla dispara como mucho
  una vez por evento y, tras cada disparo, se vuelve a empezar por los `gate`. La precedencia es la
  de ADR-0018: `gate` > `terminal` > `disparador` > `fallback`. Dentro de una misma clase se recorre
  por id solo para ser determinista (ADR-0048, H3): la spec no depende de ese orden.
- **Una accion con `efecto` se ejecuta solo si, en ese instante, ningun `gate` prohibe ese efecto**
  (ADR-0032 §3).
- **Una primitiva que no esta implementada vale DESCONOCIDO** (ADR-0048 §2), y los nodos lo
  propagan con la logica de Kleene. Una regla cuyo `cuando` es DESCONOCIDO no ejecuta su
  `entonces`, y una accion con efecto que un `gate` DESCONOCIDO podria prohibir no se ejecuta. Cada
  caso queda registrado en `Evento.no_implementadas` y `Evento.bloqueadas`.
- **Un nodo `hecho` con `vale`** es verdadero solo si el hecho esta fijado a ese valor, y **un hecho
  que declara `caduca: al_abrir_sesion`** se apaga al empezar el evento de apertura de cada sesion,
  antes de la primera pasada (ADR-0049, H1). `permite` se registra y no cambia nada (H5).

Es puro: recibe el estado, el momento y las primitivas, y devuelve lo que paso. No lee ficheros.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from botsito.domain.velas import MinutoUtc

CLASES_EN_ORDEN = ("gate", "terminal", "disparador", "fallback")  # ADR-0018
NODOS_LOGICOS = ("todos_de", "cualquiera_de", "ninguno_de")
ORIGEN_BROKER = "broker"
FUENTE_ACUMULADOR = "acumulador"
VALOR_APAGADO = "no"  # `fijar: {hecho: X, a: no}` apaga el hecho (RN-015, ADR-0032 §4)
# `caduca: al_abrir_sesion` (ADR-0049): el hecho se apaga al empezar el evento de apertura de cada
# sesion, ANTES de la primera pasada. Sin esto los gates leian en esa pasada el `sesgo` de la
# sesion anterior, y RN-033 disparaba una vez sobre el.
CADUCA_AL_ABRIR = "al_abrir_sesion"


class InterpreteError(ValueError):
    """Una forma que el interprete no sabe recorrer: nunca se adivina."""


class Tri(Enum):
    SI = "si"
    NO = "no"
    DESCONOCIDO = "desconocido"


@dataclass(frozen=True, slots=True)
class NoImplementada:
    """Una primitiva sin escribir, con su id: `predicado:x`, `accion:x` o `acumulador:x`."""

    id: str


@dataclass(frozen=True, slots=True)
class Resultado:
    valor: Tri
    ligaduras: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Momento:
    """Lo que una primitiva puede ver: el instante del evento y lo cerrado hasta el."""

    instante: MinutoUtc  # cierre de la M1 que dispara el evento
    sesion: str | None  # la sesion a la que pertenece el evento
    abre_sesion: bool  # el evento es la apertura de `sesion`
    datos: Any  # acceso a lo cerrado hasta `instante`; lo define el motor


@dataclass
class EstadoDia:
    """El estado que cruza las sesiones de un dia (ADR-0048 §3)."""

    hechos: dict[str, str] = field(default_factory=dict)  # hechos de origen `regla` encendidos
    broker: dict[str, bool] = field(default_factory=dict)  # hechos de origen `broker` (H4)
    anotaciones: dict[str, dict[str, str]] = field(default_factory=dict)  # por sesion


Predicado = Callable[[Mapping[str, Any], Momento, EstadoDia], "Resultado | NoImplementada"]
# Una accion devuelve los hechos que fija, (hecho, valor), CAMBIE O NO su valor: una regla que
# vuelve a fijar el mismo sesgo en la segunda sesion tambien lo produce en esa sesion.
Accion = Callable[
    [Mapping[str, Any], Mapping[str, str], Momento, EstadoDia], Sequence[tuple[str, str]]
]


@dataclass(frozen=True)
class Primitivas:
    predicados: Mapping[str, Predicado]
    acciones: Mapping[str, Accion]
    acumuladores: Mapping[str, Predicado]  # por nombre de acumulador (ADR-0030 §1)


@dataclass(frozen=True)
class ReglaEjecutable:
    id: str
    clase: str
    cuando: Any
    entonces: Mapping[str, Any]


@dataclass
class Evento:
    """Lo que paso en un evento: que disparo, que se fijo y que no se pudo evaluar."""

    disparadas: list[str] = field(default_factory=list)
    caducados: list[str] = field(default_factory=list)  # hechos apagados al abrir (ADR-0049)
    fijados: list[tuple[str, str, str]] = field(default_factory=list)  # (regla, hecho, valor)
    no_implementadas: set[tuple[str, str]] = field(default_factory=set)  # (regla, primitiva)
    bloqueadas: set[tuple[str, str, str]] = field(default_factory=set)  # (regla, accion, motivo)
    prohibidos: set[str] = field(default_factory=set)
    permitidos: set[str] = field(default_factory=set)  # se registra y no cambia nada (H5)


# --------------------------------------------------------------------------------- logica


def _y(valores: Sequence[Tri]) -> Tri:
    if Tri.NO in valores:
        return Tri.NO
    return Tri.DESCONOCIDO if Tri.DESCONOCIDO in valores else Tri.SI


def _o(valores: Sequence[Tri]) -> Tri:
    if Tri.SI in valores:
        return Tri.SI
    return Tri.DESCONOCIDO if Tri.DESCONOCIDO in valores else Tri.NO


def _no(valor: Tri) -> Tri:
    return {Tri.SI: Tri.NO, Tri.NO: Tri.SI, Tri.DESCONOCIDO: Tri.DESCONOCIDO}[valor]


@dataclass
class Interprete:
    """Evalua reglas contra el vocabulario de la spec y un juego de primitivas."""

    vocabulario: Mapping[str, Mapping[str, Any]]
    primitivas: Primitivas
    caducan_al_abrir: tuple[str, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.caducan_al_abrir = tuple(
            sorted(
                nombre
                for nombre, h in (self.vocabulario.get("hechos") or {}).items()
                if isinstance(h, Mapping) and h.get("caduca") == CADUCA_AL_ABRIR
            )
        )

    def _hecho(self, nodo: Mapping[str, Any], estado: EstadoDia) -> Resultado:
        nombre = str(nodo["hecho"])
        declarado = self.vocabulario["hechos"].get(nombre)
        if declarado is None:
            raise InterpreteError(f"hecho {nombre!r} no declarado en la spec")
        if declarado.get("origen") == ORIGEN_BROKER:
            encendido = estado.broker.get(nombre, False)
            valor = "si" if encendido else None
        else:
            valor = estado.hechos.get(nombre)
        if valor is None:
            return Resultado(Tri.NO)
        # `vale` (ADR-0049): el nodo es verdadero solo si el hecho esta fijado A ESE valor. Es lo
        # que hace expresable "con sesgo ambiguo" (RN-033) en un arbol que solo sabia preguntar si
        # un hecho esta encendido.
        vale = nodo.get("vale")
        if vale is not None and valor != str(vale):
            return Resultado(Tri.NO)
        liga = nodo.get("liga")
        return Resultado(Tri.SI, {str(liga): valor} if liga else {})

    def _invocacion(
        self, nombre: str, args: Any, momento: Momento, estado: EstadoDia, faltan: set[str]
    ) -> Resultado:
        declarado = self.vocabulario["predicados"].get(nombre)
        if declarado is None:
            raise InterpreteError(f"predicado {nombre!r} no declarado en la spec")
        argumentos: Mapping[str, Any] = args if isinstance(args, Mapping) else {}
        if declarado.get("fuente") == FUENTE_ACUMULADOR:
            acumulador = str(argumentos.get("acumulador"))
            primitiva = self.primitivas.acumuladores.get(acumulador)
            id_falta = f"acumulador:{acumulador}"
        else:
            primitiva = self.primitivas.predicados.get(nombre)
            id_falta = f"predicado:{nombre}"
        if primitiva is None:
            faltan.add(id_falta)
            return Resultado(Tri.DESCONOCIDO)
        salida = primitiva(argumentos, momento, estado)
        if isinstance(salida, NoImplementada):
            faltan.add(salida.id)
            return Resultado(Tri.DESCONOCIDO)
        return salida

    def evaluar(
        self, nodo: Any, momento: Momento, estado: EstadoDia, faltan: set[str]
    ) -> Resultado:
        """Kleene, de izquierda a derecha y cortando en cuanto el resultado ya no puede cambiar."""
        if not isinstance(nodo, Mapping) or len(nodo) == 0:
            raise InterpreteError(f"nodo de forma invalido: {nodo!r}")
        if "hecho" in nodo:
            return self._hecho(nodo, estado)
        if len(nodo) != 1:
            raise InterpreteError(f"un nodo de forma tiene una sola clave: {sorted(nodo)}")
        clave, valor = next(iter(nodo.items()))
        if clave in NODOS_LOGICOS:
            if not isinstance(valor, list):
                raise InterpreteError(f"{clave} lleva una lista")
            valores: list[Tri] = []
            ligaduras: dict[str, str] = {}
            corte = Tri.NO if clave == "todos_de" else Tri.SI
            for hijo in valor:
                r = self.evaluar(hijo, momento, estado, faltan)
                valores.append(r.valor)
                if r.valor is Tri.SI:
                    ligaduras.update(r.ligaduras)
                if r.valor is corte:
                    break
            if clave == "todos_de":
                total = _y(valores)
                return Resultado(total, ligaduras if total is Tri.SI else {})
            alguno = _o(valores)
            if clave == "cualquiera_de":
                return Resultado(alguno, ligaduras if alguno is Tri.SI else {})
            return Resultado(_no(alguno))
        return self._invocacion(str(clave), valor, momento, estado, faltan)

    def _ejecutar(
        self,
        regla: ReglaEjecutable,
        ligaduras: Mapping[str, str],
        momento: Momento,
        estado: EstadoDia,
        evento: Evento,
        quizas_prohibidos: set[str],
    ) -> None:
        entonces = regla.entonces
        evento.prohibidos.update(str(e) for e in entonces.get("prohibe", []) or [])
        evento.permitidos.update(str(e) for e in entonces.get("permite", []) or [])
        for paso in entonces.get("hace", []) or []:
            if not isinstance(paso, Mapping) or len(paso) != 1:
                raise InterpreteError(f"{regla.id}: accion invalida {paso!r}")
            nombre, args = next(iter(paso.items()))
            declarada = self.vocabulario["acciones"].get(nombre)
            if declarada is None:
                raise InterpreteError(f"{regla.id}: accion {nombre!r} no declarada en la spec")
            efecto = declarada.get("efecto")
            if efecto and efecto in evento.prohibidos:
                evento.bloqueadas.add((regla.id, f"accion:{nombre}", f"prohibida:{efecto}"))
                continue
            if efecto and efecto in quizas_prohibidos:
                evento.bloqueadas.add((regla.id, f"accion:{nombre}", f"gate desconocido:{efecto}"))
                continue
            primitiva = self.primitivas.acciones.get(str(nombre))
            if primitiva is None:
                evento.no_implementadas.add((regla.id, f"accion:{nombre}"))
                continue
            fijados = primitiva(
                args if isinstance(args, Mapping) else {}, ligaduras, momento, estado
            )
            evento.fijados += [(regla.id, hecho, valor) for hecho, valor in fijados]

    def evento(
        self, reglas: Sequence[ReglaEjecutable], momento: Momento, estado: EstadoDia
    ) -> Evento:
        """Un evento a punto fijo con refraccion (ADR-0028 §4)."""
        orden = sorted(reglas, key=lambda r: (CLASES_EN_ORDEN.index(r.clase), r.id))
        evento = Evento()
        if momento.abre_sesion:
            for nombre in self.caducan_al_abrir:
                if estado.hechos.pop(nombre, None) is not None:
                    evento.caducados.append(nombre)
        disparadas: set[str] = set()
        while True:
            quizas_prohibidos: set[str] = set()
            disparo = False
            for regla in orden:
                if regla.id in disparadas:
                    continue
                faltan: set[str] = set()
                r = self.evaluar(regla.cuando, momento, estado, faltan)
                if r.valor is Tri.DESCONOCIDO:
                    evento.no_implementadas.update((regla.id, f) for f in faltan)
                    if regla.clase == "gate":
                        quizas_prohibidos.update(
                            str(e) for e in regla.entonces.get("prohibe", []) or []
                        )
                    continue
                if r.valor is Tri.SI:
                    self._ejecutar(regla, r.ligaduras, momento, estado, evento, quizas_prohibidos)
                    disparadas.add(regla.id)
                    evento.disparadas.append(regla.id)
                    disparo = True
                    break
            if not disparo:
                return evento


def reglas_ejecutables(reglas: Sequence[Any]) -> list[ReglaEjecutable]:
    """Las reglas VIGENTES con `forma`, tal como las carga `spec.modelo.cargar_reglas`."""
    salida: list[ReglaEjecutable] = []
    for r in reglas:
        if not getattr(r, "vigente", False) or r.forma is None:
            continue
        forma = r.forma
        if not isinstance(forma, Mapping) or "cuando" not in forma or "entonces" not in forma:
            raise InterpreteError(f"{r.id}: la forma lleva `cuando` y `entonces`")
        if r.clase not in CLASES_EN_ORDEN:
            raise InterpreteError(f"{r.id}: clase {r.clase!r} fuera de {CLASES_EN_ORDEN}")
        salida.append(ReglaEjecutable(r.id, r.clase, forma["cuando"], forma["entonces"]))
    return salida


__all__ = [
    "CADUCA_AL_ABRIR",
    "CLASES_EN_ORDEN",
    "Accion",
    "EstadoDia",
    "Evento",
    "Interprete",
    "InterpreteError",
    "Momento",
    "NoImplementada",
    "Predicado",
    "Primitivas",
    "ReglaEjecutable",
    "Resultado",
    "Tri",
    "reglas_ejecutables",
]
