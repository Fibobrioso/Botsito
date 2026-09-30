"""Con que reloj se cuentan la ventana operativa y sus sesiones (ADR-0063).

Hasta la rama `trabajo/nocturno-01oct` el motor leia `huso_operativa` para DOS cosas: el reloj de
las SESIONES -a que hora abre y cierra la ventana, y donde caen sus sesiones- y el reloj del DIA DE
RIESGO -la medianoche que corta el tope diario, que tiene que ser la de la firma (ADR-0027,
ADR-0053 §4)-. En verano coinciden; en invierno, si el trader cuenta sus sesiones con el reloj de
su grafico (A-42, lectura PROVISIONAL de ADR-0059), se separan una hora, y no se podia mover uno
sin romper el otro.

Aqui se separan. El selector `reloj_sesiones` dice CUAL de los relojes del registro cuenta las
sesiones, y el huso de cada reloj sigue viviendo en SU parametro, una sola vez (ADR-0002): el
reloj civil del trader en `huso_operativa` y el de su grafico en `huso_grafico`. El dia de riesgo
no pasa por aqui: sigue en `huso_operativa`, que es lo que `reloj_dia_riesgo` declara.
"""

from __future__ import annotations

from botsito.config.registro import Registro

PARAMETRO_RELOJ_SESIONES = "reloj_sesiones"
# Cada opcion del selector y el parametro del registro que lleva el huso de ese reloj.
HUSO_DEL_RELOJ = {"civil_operativa": "huso_operativa", "grafico": "huso_grafico"}


class RelojError(ValueError):
    """El selector nombra un reloj que el motor no sabe leer: nunca se adivina."""


def huso_del_reloj(registro: Registro, selector: str) -> str:
    """El huso IANA del reloj que dice `selector`, un parametro enum del registro."""
    opcion = registro.opcion(selector)
    parametro = HUSO_DEL_RELOJ.get(opcion)
    if parametro is None:
        raise RelojError(
            f"{selector} = {opcion!r}: no es un reloj del registro ({', '.join(HUSO_DEL_RELOJ)})"
        )
    return registro.texto(parametro)


def huso_de_las_sesiones(registro: Registro) -> str:
    """El huso en el que el motor abre y cierra las sesiones: el del reloj de `reloj_sesiones`."""
    return huso_del_reloj(registro, PARAMETRO_RELOJ_SESIONES)


__all__ = [
    "HUSO_DEL_RELOJ",
    "PARAMETRO_RELOJ_SESIONES",
    "RelojError",
    "huso_de_las_sesiones",
    "huso_del_reloj",
]
