"""Las primitivas escritas a mano que el interprete despacha por nombre (ADR-0030 §1).

Hoy son pocas, y todo lo demas es NO_IMPLEMENTADA (ADR-0048 §2):

- de reloj: `abre_sesion_operativa`, `en_ventana` y `alcanza_hora`;
- de mercado: `sesgo_h4_al_abrir`, SOLO con `que: vela_h4_previa` y `contra:
  extremo_de_la_h4_anterior`, que es RN-003 y usa `domain/sesgo.py` tal cual (ADR-0044, ADR-0048
  §8, ADR-0049 H1). Siempre tiene respuesta -alcista, bajista, ambiguo o insuficiente- y la ata en
  `sentido_de_la_ruptura`, asi que RN-003 fija `sesgo` en cada apertura. Con cualquier otro sujeto
  no esta escrito, y lo dice. `rompe` no esta escrito: ninguna regla lo invoca desde ADR-0049;
- la accion `fijar`.

Ninguna cifra vive aqui (ADR-0002): los argumentos de valor son NOMBRES del registro (ADR-0019 §1)
y se leen en el momento de evaluar. Las opciones de enum que se interpretan (`dias_operables`) son
las del propio registro.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from decimal import Decimal
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from botsito.comun.husos import huso_canonico
from botsito.config.registro import Registro
from botsito.data.velas import a_datetime
from botsito.domain.pivotes_m15 import ALTO, BAJO, Pivote, cruza, toca
from botsito.domain.sesgo import sesgo_h4
from botsito.domain.velas import Vela
from botsito.engine.interprete import (
    VALOR_APAGADO,
    EstadoDia,
    Momento,
    NoImplementada,
    Primitivas,
    Resultado,
    Tri,
)
from botsito.engine.tope_trader import (
    ACUMULADOR_DIA,
    ACUMULADOR_SEMANA,
    PORCENTAJE,
    SIN_TOPE,
    TopeTrader,
)

# RN-003: el unico sujeto de `sesgo_h4_al_abrir` que hay escrito (ADR-0044).
SUJETO_SESGO = ("vela_h4_previa", "extremo_de_la_h4_anterior")
TOKEN_SENTIDO = "sentido_de_la_ruptura"
ANOTACION_SESGO = "sesgo_h4"  # lo que dijo `sesgo_h4` al abrir la sesion (H1)
# Las opciones de `dias_operables` en parametros.yaml, con los dias ISO que abarca cada una.
DIAS_OPERABLES = {
    "lunes_a_viernes": frozenset(range(1, 6)),
    "todos_los_dias": frozenset(range(1, 8)),
}


class DatosDelDia(Protocol):
    """Lo que el motor da a las primitivas: solo lo cerrado hasta el instante del evento."""

    def velas_h4_cerradas(self, instante: int) -> list[Vela]: ...

    def ultima_m15_cerrada(self, instante: int) -> Vela | None: ...

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None: ...


# RN-004 y RN-005 leen `que: liquidez_m15`: el unico nivel que estas primitivas saben producir.
TOKEN_LIQUIDEZ_M15 = "liquidez_m15"
HECHO_SESGO = "sesgo"
# El lado del pivote que es la liquidez segun el sesgo (RN-005: «lo que se desarrolla por encima de
# la liquidez de M15 en sesgo alcista, o por debajo de ella en sesgo bajista, es ruido»: la
# operativa alcista va por debajo de un BAJO tomado; la bajista, por encima de un ALTO tomado).
LADO_DE_LA_LIQUIDEZ = {"alcista": BAJO, "bajista": ALTO}


def _local(instante: int, huso: str) -> datetime:
    zona: ZoneInfo = huso_canonico(huso)
    return a_datetime(instante).astimezone(zona)


def primitivas_escritas(registro: Registro, tope: TopeTrader | None = None) -> Primitivas:
    """Las primitivas de hoy, con el registro del que leen sus argumentos. Con `tope` (el tope
    propio del trader, A-44) los acumuladores de RN-020 se evaluan tambien sin cuenta: el motor de
    la spec no coloca ninguna orden, asi que su perdida acumulada es cero; sin `tope`, siguen
    siendo hueco con nombre."""

    def abre_sesion_operativa(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        return Resultado(Tri.SI if momento.abre_sesion else Tri.NO)

    def en_ventana(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        inicio = registro.hora(str(args["inicio"])).minutos_del_dia
        fin = registro.hora(str(args["fin"])).minutos_del_dia
        dias = DIAS_OPERABLES.get(registro.opcion(str(args["dias"])))
        if dias is None:
            return NoImplementada(f"predicado:en_ventana:{args['dias']}")
        local = _local(momento.instante, registro.texto(str(args["huso"])))
        minuto = local.hour * 60 + local.minute
        dentro = inicio <= minuto < fin and local.isoweekday() in dias  # [inicio, fin)
        return Resultado(Tri.SI if dentro else Tri.NO)

    def alcanza_hora(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        hora = registro.hora(str(args["hora"])).minutos_del_dia
        local = _local(momento.instante, registro.texto(str(args["huso"])))
        return Resultado(Tri.SI if local.hour * 60 + local.minute >= hora else Tri.NO)

    def sesgo_h4_al_abrir(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        if (str(args.get("que")), str(args.get("contra"))) != SUJETO_SESGO:
            return NoImplementada(f"predicado:sesgo_h4_al_abrir:{args.get('que')}")
        datos: DatosDelDia = momento.datos
        r = sesgo_h4(
            datos.velas_h4_cerradas(momento.instante),
            momento.instante,
            registro.entero(str(args["tope"])),  # el tope lo nombra la forma (ADR-0019 §1)
            registro.opcion(str(args["criterio"])),
        )
        if momento.sesion is not None:
            estado.anotaciones.setdefault(momento.sesion, {})[ANOTACION_SESGO] = r.sesgo.value
        # Siempre SI: alcista, bajista, ambiguo o insuficiente son los cuatro valores del hecho
        # `sesgo` (ADR-0049, H1), y la forma los fija todos con el mismo `fijar`.
        return Resultado(Tri.SI, {TOKEN_SENTIDO: r.sesgo.value})

    def _liquidez(
        nombre: str, args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> tuple[Pivote, Vela] | Resultado | NoImplementada:
        """El pivote de M15 que hoy es la liquidez y la ultima M15 cerrada que puede tomarlo; NO
        si no hay liquidez marcada (sin sesgo con lado, sin pivote, o sin vela posterior a la
        contraria); NO_IMPLEMENTADA si los datos no tienen lectura de «formado» (A-35)."""
        if str(args.get("que")) != TOKEN_LIQUIDEZ_M15:
            return NoImplementada(f"predicado:{nombre}:{args.get('que')}")
        datos: DatosDelDia = momento.datos
        lado = LADO_DE_LA_LIQUIDEZ.get(str(estado.hechos.get(HECHO_SESGO)))
        if lado is None:
            return Resultado(Tri.NO)  # sin sesgo con lado no hay liquidez marcada (RN-033 manda)
        try:
            pivote = datos.liquidez_m15(momento.instante, lado)
        except (AttributeError, LookupError):
            return NoImplementada(f"predicado:{nombre}")
        ultima = datos.ultima_m15_cerrada(momento.instante)
        if pivote is None or ultima is None or ultima.inicio < pivote.contraria_fin:
            return Resultado(Tri.NO)
        return pivote, ultima

    def alcanza_nivel(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        r = _liquidez("alcanza_nivel", args, momento, estado)
        if not isinstance(r, tuple):
            return r
        pivote, ultima = r
        return Resultado(Tri.SI if toca(ultima, pivote) else Tri.NO)

    def cruza_nivel(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        r = _liquidez("cruza", args, momento, estado)
        if not isinstance(r, tuple):
            return r
        pivote, ultima = r
        criterio = registro.opcion(str(args["criterio"]))  # lo nombra la forma (ADR-0019 §1)
        return Resultado(Tri.SI if cruza(ultima, pivote, criterio) else Tri.NO)

    def fijar(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        hecho, a = str(args["hecho"]), str(args["a"])
        valor = ligaduras.get(a, a)
        if valor == VALOR_APAGADO:
            estado.hechos.pop(hecho, None)
        else:
            estado.hechos[hecho] = valor
        return [(hecho, valor)]

    def acumulador_sin_cuenta(nombre: str) -> Any:
        def leer(
            args: Mapping[str, Any], momento: Momento, estado: EstadoDia
        ) -> Resultado | NoImplementada:
            assert tope is not None
            if tope.alcance == SIN_TOPE:
                return Resultado(Tri.NO)
            aplica = tope.aplica_dia if nombre == ACUMULADOR_DIA else tope.aplica_semana
            if not aplica:
                return Resultado(Tri.NO)
            umbral = (
                registro.porcentaje(str(args["tope"])).valor
                if tope.unidad == PORCENTAJE
                else (tope.tope_dia if nombre == ACUMULADOR_DIA else tope.tope_semana)
            )
            perdida = Decimal(0)  # el motor de la spec no opera: no pierde nada
            return Resultado(Tri.SI if umbral is not None and perdida >= umbral else Tri.NO)

        return leer

    acumuladores: dict[str, Any] = {}
    if tope is not None:
        for nombre in (ACUMULADOR_DIA, ACUMULADOR_SEMANA):
            acumuladores[nombre] = acumulador_sin_cuenta(nombre)

    return Primitivas(
        predicados={
            "abre_sesion_operativa": abre_sesion_operativa,
            "en_ventana": en_ventana,
            "alcanza_hora": alcanza_hora,
            "sesgo_h4_al_abrir": sesgo_h4_al_abrir,
            "alcanza_nivel": alcanza_nivel,
            "cruza": cruza_nivel,
        },
        acciones={"fijar": fijar},
        acumuladores=acumuladores,
    )


__all__ = [
    "ANOTACION_SESGO",
    "LADO_DE_LA_LIQUIDEZ",
    "TOKEN_LIQUIDEZ_M15",
    "DatosDelDia",
    "primitivas_escritas",
]
