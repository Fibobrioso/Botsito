"""Las primitivas escritas a mano que el interprete despacha por nombre (ADR-0030 §1).

Hoy son pocas, y todo lo demas es NO_IMPLEMENTADA (ADR-0048 §2):

- de reloj: `abre_sesion_operativa`, `en_ventana` y `alcanza_hora`;
- de mercado: `rompe`, SOLO con `que: vela_h4_previa` y `contra: extremo_de_la_h4_anterior`, que es
  RN-003 y usa `domain/sesgo.py` tal cual (ADR-0044, ADR-0048 §8 y H1). Con cualquier otro sujeto
  `rompe` no esta escrito, y lo dice;
- la accion `fijar`.

Ninguna cifra vive aqui (ADR-0002): los argumentos de valor son NOMBRES del registro (ADR-0019 §1)
y se leen en el momento de evaluar. Las opciones de enum que se interpretan (`dias_operables`) son
las del propio registro.
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any, Protocol
from zoneinfo import ZoneInfo

from botsito.comun.husos import huso_canonico
from botsito.config.registro import Registro
from botsito.data.velas import a_datetime
from botsito.domain.sesgo import Sesgo, sesgo_h4
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

# RN-003: el unico sujeto de `rompe` que hay escrito (ADR-0044).
SUJETO_SESGO = ("vela_h4_previa", "extremo_de_la_h4_anterior")
TOKEN_SENTIDO = "sentido_de_la_ruptura"
PARAMETRO_TOPE_SESGO = "sesgo_h4_tope_velas"  # lo pide ADR-0044 y no va en los argumentos
ANOTACION_SESGO = "sesgo_h4"  # lo que dijo `sesgo_h4` al abrir la sesion (H1)
# Las opciones de `dias_operables` en parametros.yaml, con los dias ISO que abarca cada una.
DIAS_OPERABLES = {
    "lunes_a_viernes": frozenset(range(1, 6)),
    "todos_los_dias": frozenset(range(1, 8)),
}


class DatosDelDia(Protocol):
    """Lo que el motor da a las primitivas: solo lo cerrado hasta el instante del evento."""

    def velas_h4_cerradas(self, instante: int) -> list[Vela]: ...


def _local(instante: int, huso: str) -> datetime:
    zona: ZoneInfo = huso_canonico(huso)
    return a_datetime(instante).astimezone(zona)


def primitivas_escritas(registro: Registro) -> Primitivas:
    """Las primitivas de hoy, con el registro del que leen sus argumentos."""

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

    def rompe(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        if (str(args.get("que")), str(args.get("contra"))) != SUJETO_SESGO:
            return NoImplementada(f"predicado:rompe:{args.get('que')}")
        datos: DatosDelDia = momento.datos
        r = sesgo_h4(
            datos.velas_h4_cerradas(momento.instante),
            momento.instante,
            registro.entero(PARAMETRO_TOPE_SESGO),
            registro.opcion(str(args["criterio"])),
        )
        if momento.sesion is not None:
            estado.anotaciones.setdefault(momento.sesion, {})[ANOTACION_SESGO] = r.sesgo.value
        if r.sesgo in (Sesgo.ALCISTA, Sesgo.BAJISTA):
            return Resultado(Tri.SI, {TOKEN_SENTIDO: r.sesgo.value})
        return Resultado(Tri.NO)  # AMBIGUO o INSUFICIENTE: la forma no fija nada (H1)

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

    return Primitivas(
        predicados={
            "abre_sesion_operativa": abre_sesion_operativa,
            "en_ventana": en_ventana,
            "alcanza_hora": alcanza_hora,
            "rompe": rompe,
        },
        acciones={"fijar": fijar},
        acumuladores={},
    )


__all__ = ["ANOTACION_SESGO", "DatosDelDia", "primitivas_escritas"]
