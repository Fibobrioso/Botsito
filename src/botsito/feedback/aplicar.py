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

import yaml

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
    # el id de feedback que el registro cita HOY, para no dejarlo apuntando a un registro muerto
    fuente_anterior: str | None = None
    # el mismo `valor_escrito` pasado por el conversor del registro, para poder compararlo
    # con lo que el registro ya tiene sin repetir la conversion
    valor_convertido: Any | None = None

    @property
    def es_no_op(self) -> bool:
        """Si el registro ya tiene ese valor escrito.

        Se comparan los valores YA CONVERTIDOS, no el texto contra el objeto: `valor_anterior` es
        lo que el registro devuelve (`Fraccion(Decimal("0.8"))`, `HoraLocal("07:00", ...)`) y
        `valor_escrito` es el texto que iria al fichero (`"0.8"`). Compararlos crudos hacia que
        todo parametro numerico o de hora pareciera cambiar siempre, y un segundo `apply`
        reescribia el fichero sin que nada hubiera cambiado.
        """
        if self.valor_anterior is None:
            return False
        # Y la FUENTE tambien. Comparando solo el valor, un parametro podia quedarse citando un
        # registro ya superseded para siempre: `apply` lo veia igual y no lo tocaba. Paso de
        # verdad con `cartuchos_reinicio`, que cito durante toda F11 un registro revocado por
        # llevar una parafrasis del consultor donde iba la voz del trader -y que ademas decia
        # "dos perdidas" donde el trader remata "serian 3 perdidas"-. El hash cubre la fuente
        # justo para que quien mida fidelidad la distinga, asi que una fuente muerta lo falsea.
        if self.fuente_anterior is not None and self.fuente_anterior != self.registro_id:
            return False
        if self.valor_anterior == self.valor_escrito:
            return True
        return self.valor_convertido is not None and self.valor_anterior == self.valor_convertido


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
        # re.ASCII: sin el, `٣` (tres arabigo) pasaria como 3. El mismo motivo por el que
        # `feedback/modelo.py` lo usa en sus ids.
        if not re.fullmatch(r"-?[0-9]+", bruto.strip(), re.ASCII):
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
    # Un ciclo de supersede (o un registro que se supersede a si mismo) hace que `activos`
    # descarte los dos extremos y el parametro desaparezca sin que nadie diga nada.
    for r_ciclo in feedback:
        if r_ciclo.supersede == r_ciclo.id:
            raise AplicarError(f"{r_ciclo.id} se supersede a si mismo")
    por_id = {r_x.id: r_x for r_x in feedback}
    for r_ciclo in feedback:
        visto, actual_id = {r_ciclo.id}, r_ciclo.supersede
        while actual_id is not None:
            if actual_id in visto:
                raise AplicarError(f"ciclo de supersede que pasa por {r_ciclo.id}")
            visto.add(actual_id)
            siguiente = por_id.get(actual_id)
            actual_id = siguiente.supersede if siguiente else None
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
            convertido = _convertir(p.tipo, escrito, huso, p.nombre)
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
                fuente_anterior=(
                    p.fuente.id if p.fuente is not None and p.fuente.tipo == "feedback" else None
                ),
                valor_convertido=convertido,
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
        saltando = False
        for linea in bloque:
            if re.match(r"^    (estado|valor|fuente):", linea):
                # Se descarta la clave Y su continuacion: un `valor: >-` de dos lineas dejaba
                # las lineas sueltas, que se pegaban a la `descripcion` anterior y producian un
                # fichero que cargaba bien diciendo otra cosa.
                saltando = True
                continue
            if saltando and re.match(r"^      ", linea):
                continue
            saltando = False
            if re.match(r"^    ambiguedad_id:", linea):
                # Un valor que llega del trader deja de ser un default nuestro, y el registro
                # rechaza `ambiguedad_id` fuera de DEFAULT_AMBIGUOUS. Que la ambiguedad siga
                # abierta se ve cruzando con ambiguedades.yaml (`spec status`), no aqui.
                continue
            nuevas.append(linea)
        # El escalar lo serializa YAML, no una f-string: un valor con comillas rompia el fichero
        # y uno con una barra invertida producia OTRO valor que cargaba igual de bien
        # ("C:\\nuevo" se leia como "C: uevo").
        texto = yaml.safe_dump(
            cambio.valor_escrito, default_flow_style=True, allow_unicode=True, width=10**6
        ).strip()
        if texto.endswith("\n..."):
            texto = texto[: -len("\n...")].strip()
        # El bloque de un parametro llega hasta el `- nombre:` siguiente, asi que arrastra las
        # lineas en blanco y los COMENTARIOS DE CABECERA de la seccion que viene detras. Anadir
        # las claves al final metia esos comentarios DENTRO del parametro: el fichero seguia
        # cargando -YAML los ignora- y el hash no podia verlo -se hashea la estructura-, pero el
        # comentario pasaba a decir lo contrario del parametro que lo contenia. Paso de verdad
        # dos veces, con anclaje_h4 y lotaje_base. Se insertan tras la ultima clave real.
        corte = len(nuevas)
        while corte > 0 and (
            not nuevas[corte - 1].strip() or nuevas[corte - 1].lstrip().startswith("#")
        ):
            corte -= 1
        nuevas[corte:corte] = [
            "    estado: CONFIRMED",
            f"    valor: {texto}",
            "    fuente:",
            "      tipo: feedback",
            f"      id: {cambio.registro_id}",
        ]
        salida.extend(nuevas)
        escritos.add(actual)

    escritos: set[str] = set()

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
    faltan = sorted({c.parametro for c in cambios} - escritos)
    if faltan:
        # Sin esto, un fichero con otro formato -el nombre entrecomillado, otra indentacion, un
        # comentario al final de la linea- devolvia el fichero INTACTO, la validacion del temporal
        # pasaba (es el mismo fichero) y la CLI decia "OK: escrito" saliendo con 0.
        raise AplicarError(
            "no se encontro el bloque de "
            + ", ".join(faltan)
            + " en el fichero: su formato no es el que `apply` sabe editar y no se ha escrito nada"
        )
    return "\n".join(salida) + "\n"
