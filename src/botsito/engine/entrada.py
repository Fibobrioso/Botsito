"""El tipo de la orden de entrada (A-47, ADR-0056 §1; rama `trabajo/selector-orden-stop`).

`entrada_tipo_orden` vive en el registro como UNKNOWN hasta que el trader responda A-47, con las dos
lecturas que documenta el material: `stop_en_ruptura`, una orden STOP en el nivel de ruptura que
salta cuando el precio lo rompe, y `limite_en_retroceso`, la LIMITE que espera el retroceso al
bloque y que es lo que RN-011 programa hoy. Sin fijar, el motor cableado se niega; la unica
excepcion es el diagnostico pedido a proposito (`--diagnostico-a47`), ETIQUETADO en cada linea,
fichero y pagina y sin valor para ninguna medida (el patron de ADR-0054). Con el valor fijado, el
diagnostico se rechaza.

Con `stop_en_ruptura`, en esta rama la orden stop se coloca en el MISMO instante que la limite, el
cierre del breaker, y al mismo precio, el 0 de la caja (`Zona.entrada`): el instante propio de la
stop -el posible punto de breaker, antes de la ruptura- es la rama 3 de ADR-0056. Lo decide,
PROVISIONAL, ADR-0058.
"""

from __future__ import annotations

from botsito.config.registro import ParametroDesconocidoError, Registro

PARAMETRO_A47 = "entrada_tipo_orden"
STOP_EN_RUPTURA = "stop_en_ruptura"
LIMITE_EN_RETROCESO = "limite_en_retroceso"
LECTURAS_A47 = (STOP_EN_RUPTURA, LIMITE_EN_RETROCESO)


class SinTipoDeOrdenError(ValueError):
    """A-47 sin responder: el motor cableado se niega a colocar ninguna entrada y dice cual."""


class DiagnosticoDeTipoRechazadoError(ValueError):
    """Se pidio el diagnostico de A-47 con el tipo ya fijado: la corrida cuenta y no lo admite."""


def lectura_tipo_orden(registro: Registro, a47: str | None) -> str:
    """El tipo de orden con el que corre el motor cableado: el del registro si el trader lo fijo;
    si no, el del diagnostico pedido; y sin ninguno de los dos, la negativa que nombra A-47."""
    try:
        fijado: str | None = registro.opcion(PARAMETRO_A47)
    except ParametroDesconocidoError:
        fijado = None
    if fijado is not None:
        if a47 is not None:
            raise DiagnosticoDeTipoRechazadoError(
                f"{PARAMETRO_A47} ya esta fijado en {fijado!r} (A-47 respondida): la corrida "
                "cuenta y no admite --diagnostico-a47"
            )
        return fijado
    if a47 is not None:
        if a47 not in LECTURAS_A47:
            raise ValueError(f"lectura de A-47 {a47!r} no esta en {LECTURAS_A47}")
        return a47
    raise SinTipoDeOrdenError(
        f"A-47 sin fijar: `{PARAMETRO_A47}` es UNKNOWN en knowledge/spec/parametros.yaml y la spec "
        "no sabe si la entrada es una orden stop o una limite; el motor cableado se niega a "
        "colocarla. La responde el trader, grabado. Para ver el resultado en hipotesis, "
        f"--diagnostico-a47 <{'|'.join(LECTURAS_A47)}>: corre ETIQUETADO y sin valor para ninguna "
        "medida"
    )
