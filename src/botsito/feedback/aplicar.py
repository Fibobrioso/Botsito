"""Llevar al registro los valores que el trader dio en una sesion (F11, ADR-0002/0011).

Esta es la puerta que F09 dejo diferida a proposito: hasta que hubo sesion no habia valores
que aplicar. La regla de oro es que aqui NO se interpreta nada. Si el valor que trae el
registro de feedback no encaja en el tipo declarado, esto falla y lo dice; la re-expresion se
hace fuera, escribiendo un registro nuevo con `valor_canonico` (que supersede al anterior y
conserva el literal del trader), no con una tabla de traducciones dentro del codigo. Una tabla
asi seria negocio viviendo fuera del registro, que es justo lo que ADR-0002 prohibe.

El fichero se reescribe preservando comentarios: las primeras lineas de `parametros.yaml` son
la documentacion del esquema, citada por ADR-0002 y por el README, y un volcado de ida y
vuelta las borraria.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.config.registro import (
    Estado,
    Parametro,
    Registro,
    RegistroError,
    _convertir,  # noqa: PLC2701  # misma capa: aplicar comprueba con el MISMO conversor que carga
)
from botsito.feedback.modelo import FeedbackRecord, activos

# Un valor solo entra al registro por una de estas: resolver un desconocido, corregir lo que
# habia, o ratificarlo. Un REJECT o un LABEL_CASE no fijan el valor de un parametro.
ACCIONES_QUE_FIJAN = ("RESOLVE_UNKNOWN", "CORRECT", "CONFIRM")


class AplicarError(ValueError):
    """El feedback de la sesion no se puede llevar al registro tal como esta."""


@dataclass(frozen=True, slots=True)
class Cambio:
    """Lo que le pasaria a un parametro. `valor_escrito` es lo que iria al fichero."""

    parametro: str
    registro_id: str
    accion: str
    valor_escrito: Any
    literal: str
    canonico: bool
    estado_anterior: Estado
    valor_anterior: Any | None

    @property
    def es_no_op(self) -> bool:
        return self.valor_anterior is not None and self.valor_anterior == self.valor_escrito


def _valor_bruto(r: FeedbackRecord, p: Parametro) -> Any:
    """Lo que se escribiria en el YAML, en el tipo que el fichero espera.

    `valor_canonico` manda si existe. No se normaliza nada: como mucho, un tipo que en el
    fichero se escribe sin comillas (entero, puntos, minutos, booleano) se convierte desde su
    texto, y si no es exactamente eso, falla.
    """
    bruto = r.valor_canonico if r.valor_canonico is not None else r.valor_resultante
    if bruto is None:
        raise AplicarError(f"{p.nombre}: el registro {r.id} no trae valor")
    if p.tipo in ("entero", "puntos", "minutos"):
        if not re.fullmatch(r"-?\d+", bruto.strip()):
            raise AplicarError(
                f"{p.nombre}: {bruto!r} no es un {p.tipo} (el fichero lo escribe sin comillas); "
                f"anade un registro con --valor-canonico"
            )
        return int(bruto.strip())
    if p.tipo == "booleano":
        if bruto.strip() not in ("true", "false"):
            raise AplicarError(f"{p.nombre}: {bruto!r} no es un booleano; se escribe true o false")
        return bruto.strip() == "true"
    return bruto


def cambios_de_sesion(
    registro: Registro,
    feedback: Sequence[FeedbackRecord],
    sesion: str,
    husos: dict[str, str] | None = None,
) -> list[Cambio]:
    """Los cambios que la sesion propone sobre el registro, o `AplicarError` si no son aplicables.

    No filtra por accion `RESOLVE_UNKNOWN`: cinco parametros de la sesion 1 solo tienen un
    `CORRECT` vigente, y quedarse con el `RESOLVE_UNKNOWN` superseded escribiria el valor viejo
    (en `perdida_maxima_diaria`, "saldo del momento" en vez de "saldo inicial del dia").
    """
    vigentes: list[FeedbackRecord] = activos(list(feedback))
    por_parametro: dict[str, list[FeedbackRecord]] = {}
    for r in vigentes:
        if (
            r.sesion != sesion
            or r.objetivo.tipo != "parametro"
            or r.accion not in ACCIONES_QUE_FIJAN
        ):
            continue
        if r.valor_resultante is None and r.valor_canonico is None:
            continue
        por_parametro.setdefault(r.objetivo.id, []).append(r)

    problemas: list[str] = []
    cambios: list[Cambio] = []
    for nombre in sorted(por_parametro):
        lista = por_parametro[nombre]
        if len(lista) > 1:
            ids = ", ".join(sorted(r.id for r in lista))
            problemas.append(
                f"{nombre}: {len(lista)} registros vigentes a la vez ({ids}); uno debe superseder "
                f"al otro para saber cual manda"
            )
            continue
        r = lista[0]
        if nombre not in registro.nombres():
            problemas.append(f"{nombre}: el registro {r.id} apunta a un parametro que no existe")
            continue
        p = registro.parametros[nombre]
        if p.categoria != "estrategia":
            problemas.append(
                f"{nombre}: es de categoria {p.categoria} y solo se cambia por decision (ADR); "
                f"el registro {r.id} no puede escribirlo (ADR-0004)"
            )
            continue
        try:
            escrito = _valor_bruto(r, p)
            huso = (husos or {}).get(nombre)
            if p.tipo == "hora" and not huso:
                raise AplicarError(
                    f"{nombre}: es de tipo hora y no declara 'huso' en el fichero; sin huso "
                    f"una hora no dice cuando ocurre"
                )
            _convertir(p.tipo, escrito, huso, p.nombre)
            if p.tipo == "enum" and p.opciones is not None and escrito not in p.opciones:
                # Se comprueba aqui y no solo al cargar el fichero: si no, `--check` diria que
                # todo esta bien y el error saldria al escribir, con el registro ya tocado.
                raise AplicarError(
                    f"{nombre}: {escrito!r} no es ninguna de las opciones "
                    f"{list(p.opciones)}; anade un registro con --valor-canonico"
                )
        except (AplicarError, RegistroError) as exc:
            problemas.append(str(exc))
            continue
        cambios.append(
            Cambio(
                parametro=nombre,
                registro_id=r.id,
                accion=r.accion,
                valor_escrito=escrito,
                literal=r.respuesta_literal,
                canonico=r.valor_canonico is not None,
                estado_anterior=p.estado,
                valor_anterior=p.valor,
            )
        )

    if problemas:
        raise AplicarError("; ".join(problemas))
    return cambios


_INICIO_PARAMETRO = re.compile(r"^  - nombre: (\S+)\s*$")


def escribir_cambios(ruta: Path, cambios: Sequence[Cambio]) -> str:
    """Reescribe `parametros.yaml` con los valores, preservando comentarios y orden.

    Edicion por lineas a proposito: un `safe_dump` de ida y vuelta borraria la cabecera que
    documenta el esquema y reordenaria los campos de los 33 parametros, produciendo un diff en
    el que nadie podria ver que ha cambiado de verdad.
    """
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    por_nombre = {c.parametro: c for c in cambios}
    salida: list[str] = []
    actual: str | None = None
    bloque: list[str] = []

    def volcar() -> None:
        if actual is None:
            salida.extend(bloque)
            return
        cambio = por_nombre.get(actual)
        if cambio is None:
            salida.extend(bloque)
            return
        nuevas: list[str] = []
        for linea in bloque:
            if re.match(r"^    (estado|valor|fuente):", linea):
                continue
            if re.match(r"^      (tipo|id): ", linea):  # cuerpo de `fuente`
                continue
            nuevas.append(linea)
        valor = cambio.valor_escrito
        texto = (
            "true"
            if valor is True
            else "false"
            if valor is False
            else str(valor)
            if isinstance(valor, int)
            else f'"{valor}"'
        )
        nuevas.append("    estado: CONFIRMED")
        nuevas.append(f"    valor: {texto}")
        nuevas.append("    fuente:")
        nuevas.append("      tipo: feedback")
        nuevas.append(f"      id: {cambio.registro_id}")
        salida.extend(nuevas)

    for linea in lineas:
        m = _INICIO_PARAMETRO.match(linea)
        if m:
            volcar()
            actual, bloque = m.group(1), [linea]
            continue
        if actual is None:
            salida.append(linea)
        else:
            bloque.append(linea)
    volcar()
    return "\n".join(salida) + "\n"
