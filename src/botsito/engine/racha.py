"""La racha de perdidas seguidas del trader (RN-036, A-51; ADR-0077): el acumulador
`racha_perdidas`, que PERSISTE entre dias como la cuenta (ADR-0053 §6) y vive junto al
`SeguidorTope`, nunca en `EstadoDia`.

Lo que dijo el trader en la sesion 4 (S-8), ya en el registro:

- `racha_perdidas_max`: tras esa racha de perdidas seguidas no se opera mas ese dia
  (`ev-v10-010653-81316808`; ya en v9, `ev-v9-011128-a267338b`);
- `racha_perdidas_corte`: solo una ganadora la pone a cero; un break even no la corta
  (`ev-v10-010715-fae17215`: «luego nos sigue un break even no corta la racha como tal»);
- `racha_perdidas_reinicio`: nunca por calendario, «la racha sigue de un día a otro y una semana
  otra» (`ev-v10-010804-5b6ad1a3`);
- `racha_perdidas_reanudacion`: tras la racha, «sería el día siguiente» (el mismo item).

Lo que cuenta como PERDIDA es lo mismo que gasta un cartucho en RN-016 (`cartucho_criterio`,
`cuenta_como_perdida`): no se inventa otra definicion. El «dia» es el dia OPERATIVO del reloj de
las sesiones (`reloj_sesiones`, ADR-0063; `rejilla_h4`, ADR-0069), porque la ventana entera cae
dentro de un dia civil: tras la racha no se opera mas en ese dia operativo y se vuelve en la
primera sesion del siguiente. LECTURA DE LA SESION, escrita en ADR-0077: la detencion es del dia
en que cayo la perdida que alcanza el tope; la racha sigue contando (reinicio `nunca`), asi que
al dia siguiente vale lo mismo pero la detencion ha caducado, y la siguiente perdida -la decima-
vuelve a detener el dia en que caiga.

Ninguna cifra vive aqui (ADR-0002): el tope lo nombra la forma de RN-036 y lo lee el acumulador
del registro; las opciones de los tres enums se leen por su nombre.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

from botsito.config.registro import Registro
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine.relojes import RelojSesiones, reloj_de_las_sesiones

# Los nombres del registro que este modulo lee (ADR-0002: una sola puerta).
P_MAX = "racha_perdidas_max"
P_CORTE = "racha_perdidas_corte"
P_REINICIO = "racha_perdidas_reinicio"
P_REANUDACION = "racha_perdidas_reanudacion"
P_CRITERIO = "cartucho_criterio"
ACUMULADOR_RACHA = "racha_perdidas"
HECHO_DETENIDO = "detenido_por_racha"
# Las opciones con contrato: las del trader. Las demas estan declaradas en el registro y NO
# implementadas: con ellas el seguidor se niega, nunca adivina.
CORTE_GANADORA = "ganadora"
CORTE_GANADORA_O_BREAK_EVEN = "ganadora_o_break_even"
REINICIO_NUNCA = "nunca"
REANUDACION_DIA_SIGUIENTE = "dia_siguiente"
# Lo que el broker dice de cada cierre (`clasificar_cierre`, `primitivas_broker`): el mecanismo y
# como se activo la operacion. Son los mismos tokens que la spec declara.
SALTO_EL_STOP = "salto_el_stop"
PERDIDA = "perdida"
BREAK_EVEN = "break_even"
GANANCIA = "ganancia"
ESQUEMAS = ("primer_esquema", "segundo_esquema")
SOLO_PERDIDA = "solo_perdida"
TODO_INTENTO = "todo_intento"


class RachaError(ValueError):
    """Una lectura del registro sin contrato: el seguidor no adivina."""


def cuenta_como_perdida(criterio: str, resultado: str | None, por: str | None) -> bool:
    """Lo mismo que nombran las dos ramas de RN-016: un cierre en que salto el stop, se activara
    como se activara, o una perdida de una operacion que vino de un esquema
    (`cartucho_criterio` = `solo_perdida`); con `todo_intento`, cualquier cierre. Es LA definicion
    del cartucho gastado, y `primitivas_broker` la usa para `cartuchos`: una sola. Puro."""
    if criterio == TODO_INTENTO:
        return True
    if criterio != SOLO_PERDIDA:
        raise RachaError(f"{P_CRITERIO} = {criterio!r}: sin contrato")
    return resultado == SALTO_EL_STOP or (resultado == PERDIDA and por in ESQUEMAS)


@dataclass
class SeguidorRacha:
    """Cuenta las perdidas seguidas del trader y dice si hoy ya no se opera (RN-036)."""

    reloj: RelojSesiones
    criterio: str
    corte: str
    reinicio: str
    reanudacion: str
    racha: int = 0
    # el dia operativo de la ultima perdida contada: si la racha esta en el tope o por encima, ese
    # dia no se opera mas y al siguiente se vuelve (`detenido`)
    ultima_perdida_dia: date | None = None
    cierres: list[tuple[int, str | None, str | None]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.corte not in (CORTE_GANADORA, CORTE_GANADORA_O_BREAK_EVEN):
            raise RachaError(f"{P_CORTE} = {self.corte!r}: sin contrato")
        if self.reinicio != REINICIO_NUNCA:
            raise RachaError(f"{P_REINICIO} = {self.reinicio!r}: solo `nunca` tiene contrato")
        if self.reanudacion != REANUDACION_DIA_SIGUIENTE:
            raise RachaError(
                f"{P_REANUDACION} = {self.reanudacion!r}: solo `dia_siguiente` tiene contrato"
            )
        cuenta_como_perdida(self.criterio, None, None)  # el criterio, con contrato

    def dia_operativo(self, instante_ms: int) -> date:
        return self.reloj.lectura(instante_ms // MS_POR_MINUTO)[0]

    def registrar(self, instante_ms: int, resultado: str | None, por: str | None) -> None:
        """Un cierre del broker, en orden de instante: una perdida suma; una ganadora pone la racha
        a cero (y un break even tambien, solo con `ganadora_o_break_even`); lo demas no la toca.
        El tope no entra aqui: lo nombra la forma de RN-036 y lo aplica `detenido`."""
        self.cierres.append((instante_ms, resultado, por))
        if resultado == GANANCIA or (
            resultado == BREAK_EVEN and self.corte == CORTE_GANADORA_O_BREAK_EVEN
        ):
            self.racha = 0
            return
        if not cuenta_como_perdida(self.criterio, resultado, por):
            return
        self.racha += 1
        self.ultima_perdida_dia = self.dia_operativo(instante_ms)

    def detenido(self, instante_ms: int, tope: int) -> bool:
        """Si en este instante no se opera por la racha (`racha_perdidas` contra
        `racha_perdidas_max`): la racha esta en el tope o por encima Y la perdida que la dejo ahi
        cayo en el dia operativo de `instante_ms`. Al dia siguiente la racha sigue (`reinicio` =
        `nunca`) pero la detencion ha caducado (`reanudacion` = `dia_siguiente`); la siguiente
        perdida vuelve a detener su dia (ADR-0077 §5)."""
        if tope <= 0:
            raise RachaError(f"{P_MAX} = {tope}: es un entero positivo")
        if self.racha < tope or self.ultima_perdida_dia is None:
            return False
        return self.dia_operativo(instante_ms) == self.ultima_perdida_dia

    def descripcion(self) -> str:
        ultima = (
            "" if self.ultima_perdida_dia is None else f"; la ultima el {self.ultima_perdida_dia}"
        )
        return f"{self.racha} seguidas{ultima}"


def seguidor_del_registro(registro: Registro) -> SeguidorRacha:
    """El seguidor con las opciones del trader leidas del registro (una sola puerta, ADR-0002)."""
    return SeguidorRacha(
        reloj_de_las_sesiones(registro),
        registro.opcion(P_CRITERIO),
        registro.opcion(P_CORTE),
        registro.opcion(P_REINICIO),
        registro.opcion(P_REANUDACION),
    )


__all__ = [
    "ACUMULADOR_RACHA",
    "HECHO_DETENIDO",
    "P_CORTE",
    "P_MAX",
    "P_REANUDACION",
    "P_REINICIO",
    "RachaError",
    "SeguidorRacha",
    "cuenta_como_perdida",
    "seguidor_del_registro",
]
