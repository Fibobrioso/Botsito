"""El tope de perdida PROPIO del trader (RN-020, A-44), como configuracion explicita y con tres
estados, independiente de los limites de la firma del perfil de cuenta (ADR-0050).

Lo que el trader ya dijo en la sesion 1 y esta CONFIRMED en el registro: la cifra del dia
(`perdida_maxima_diaria`, sobre `base_calculo_perdida_diaria`) y la de la semana
(`perdida_maxima_semanal`, sobre `base_calculo_perdida_semanal`), y que el dia corta con
`reloj_dia_riesgo`. Lo que NO dijo, y es A-44 (ADR-0053 §3.3 y §9): sobre que MAGNITUD se mide
(saldo o equity), a que ALCANCE aplica (dia, semana, los dos, o ningun tope), en que UNIDAD esta
la cifra (porcentaje o dinero de la cuenta) y con que reloj se REINICIA el conteo. Cada una es un
parametro UNKNOWN del registro hasta que el trader responda:

- SIN FIJAR (`perdida_trader_alcance` UNKNOWN): el motor se niega a correr nombrando A-44, salvo
  en modo diagnostico etiquetado (`--diagnostico-a44 sin_tope|marcador`).
- SIN_TOPE (`perdida_trader_alcance: sin_tope`): respuesta valida; RN-020 nunca bloquea.
- Un valor concreto: alcance, magnitud, unidad (y las cifras en dinero si la unidad es `usd`), y el
  huso del reinicio, que si el trader no dice otra cosa es el corte del perfil y la traza lo marca
  como SUPUESTO.

Los acumuladores `perdida_dia` y `perdida_semana` se miden desde el ultimo corte: el diario, cada
medianoche del huso de reinicio; el semanal, la medianoche del lunes. La base del porcentaje es la
que declara la spec para cada uno (`saldo_inicial_dia` = el saldo al corte del dia;
`saldo_inicial_semana` = el saldo al corte de la semana; `saldo_actual` = el saldo en el instante
de la lectura). Ningun campo de la firma (`firma_*`) se reutiliza.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

from botsito.comun.husos import huso_canonico
from botsito.config.registro import ParametroDesconocidoError, Registro
from botsito.domain.valores import CIEN
from botsito.engine.diagnostico import A44_MARCADOR, A44_SIN_TOPE, NINGUNO, Diagnostico

# Los nombres del registro que este modulo lee (ADR-0002: una sola puerta).
P_ALCANCE = "perdida_trader_alcance"
P_MAGNITUD = "perdida_trader_magnitud"
P_UNIDAD = "perdida_trader_unidad"
P_DIA_USD = "perdida_trader_dia_usd"
P_SEMANA_USD = "perdida_trader_semana_usd"
P_REINICIO_HUSO = "perdida_trader_reinicio_huso"
P_DIA_PCT = "perdida_maxima_diaria"
P_SEMANA_PCT = "perdida_maxima_semanal"
P_BASE_DIA = "base_calculo_perdida_diaria"
P_BASE_SEMANA = "base_calculo_perdida_semanal"

SIN_TOPE = "sin_tope"
DIA = "dia"
SEMANA = "semana"
AMBOS = "ambos"
ALCANCES = (SIN_TOPE, DIA, SEMANA, AMBOS)
SALDO = "saldo"
EQUITY = "equity"
MAGNITUDES = (SALDO, EQUITY)
PORCENTAJE = "porcentaje"
USD = "usd"
UNIDADES = (PORCENTAJE, USD)
BASE_SALDO_ACTUAL = "saldo_actual"
BASE_INICIAL_DIA = "saldo_inicial_dia"
BASE_INICIAL_SEMANA = "saldo_inicial_semana"

ACUMULADOR_DIA = "perdida_dia"
ACUMULADOR_SEMANA = "perdida_semana"
ORIGEN_TRADER = "trader"
ORIGEN_FIRMA = "firma"
SUPUESTO_HUSO = "SUPUESTO: reinicio con el huso de corte del perfil (el trader no dijo otro)"


class TopeSinFijarError(ValueError):
    """A-44 sin responder: el motor se niega a correr y lo dice."""


class TopeRechazadoError(ValueError):
    """Se pidio el diagnostico de A-44 con el tope ya fijado: la corrida cuenta, sin etiqueta."""


@dataclass(frozen=True)
class TopeTrader:
    """El tope del trader, ya leido: lo que el motor necesita para RN-020 y nada mas."""

    alcance: str  # sin_tope | dia | semana | ambos
    magnitud: str  # saldo | equity (que se mide)
    unidad: str  # porcentaje | usd (en que esta la cifra)
    tope_dia: Decimal | None  # % o dinero segun `unidad`; None si el alcance no lo incluye
    tope_semana: Decimal | None
    base_dia: str  # saldo_inicial_dia | saldo_actual
    base_semana: str  # saldo_inicial_semana | saldo_actual | saldo_inicial_dia
    huso_reinicio: ZoneInfo
    huso_supuesto: bool  # el huso vino del perfil, no del trader
    diagnostico: str | None = None  # el modo hipotetico, si lo hay

    @property
    def aplica_dia(self) -> bool:
        return self.alcance in (DIA, AMBOS)

    @property
    def aplica_semana(self) -> bool:
        return self.alcance in (SEMANA, AMBOS)

    def descripcion(self) -> str:
        if self.alcance == SIN_TOPE:
            marca = f" [{self.diagnostico}]" if self.diagnostico else ""
            return f"tope del trader: {SIN_TOPE}{marca}"
        partes = [f"tope del trader: {self.alcance}, sobre {self.magnitud}, en {self.unidad}"]
        if self.aplica_dia:
            partes.append(f"dia {self.tope_dia} sobre {self.base_dia}")
        if self.aplica_semana:
            partes.append(f"semana {self.tope_semana} sobre {self.base_semana}")
        partes.append(f"reinicio en {self.huso_reinicio.key}")
        if self.huso_supuesto:
            partes.append(SUPUESTO_HUSO)
        if self.diagnostico:
            partes.append(f"[{self.diagnostico}]")
        return "; ".join(partes)


def _leer_opcion(registro: Registro, nombre: str) -> str | None:
    try:
        return registro.opcion(nombre)
    except ParametroDesconocidoError:
        return None


def tope_del_registro(
    registro: Registro, huso_perfil: ZoneInfo, diagnostico: Diagnostico = NINGUNO
) -> TopeTrader:
    """El tope del trader con el que corre el motor: el del registro si el trader lo fijo; si no,
    el del diagnostico pedido; y sin ninguno, la negativa que nombra A-44."""
    alcance = _leer_opcion(registro, P_ALCANCE)
    if alcance is not None and diagnostico.a44 is not None:
        raise TopeRechazadoError(
            f"{P_ALCANCE} ya esta fijado en {alcance!r} (A-44 respondida): la corrida cuenta y "
            "no admite --diagnostico-a44"
        )
    if alcance is None:
        if diagnostico.a44 is None:
            raise TopeSinFijarError(
                f"A-44 sin fijar: `{P_ALCANCE}` es UNKNOWN en knowledge/spec/parametros.yaml y la "
                "spec no declara la magnitud ni el corte del tope propio del trader; el motor se "
                "niega a correr. La responde el trader (docs/runbooks/ACTIVAR-A35-A44.md). Para "
                f"ver el embudo en hipotesis, --diagnostico-a44 <{A44_SIN_TOPE}|{A44_MARCADOR}>: "
                "corre ETIQUETADO y sin valor para ninguna medida"
            )
        if diagnostico.a44 == A44_SIN_TOPE:
            return TopeTrader(
                SIN_TOPE, SALDO, PORCENTAJE, None, None, BASE_INICIAL_DIA, BASE_SALDO_ACTUAL,
                huso_perfil, True, f"DIAGNOSTICO-A44-{A44_SIN_TOPE}",
            )  # fmt: skip
        # el MARCADOR: un tope de un punto porcentual de nada, que no es un valor plausible del
        # trader; se toca con cualquier perdida y sirve para ver el embudo, no para simular
        return TopeTrader(
            AMBOS, EQUITY, USD, Decimal(1), Decimal(1), BASE_INICIAL_DIA, BASE_SALDO_ACTUAL,
            huso_perfil, True, f"DIAGNOSTICO-A44-{A44_MARCADOR}",
        )  # fmt: skip
    if alcance == SIN_TOPE:
        return TopeTrader(
            SIN_TOPE, SALDO, PORCENTAJE, None, None, BASE_INICIAL_DIA, BASE_SALDO_ACTUAL,
            huso_perfil, True,
        )  # fmt: skip
    magnitud = registro.opcion(P_MAGNITUD)
    unidad = registro.opcion(P_UNIDAD)
    tope_dia = tope_semana = None
    if alcance in (DIA, AMBOS):
        tope_dia = (
            registro.porcentaje(P_DIA_PCT).valor
            if unidad == PORCENTAJE
            else registro.decimal(P_DIA_USD)
        )
    if alcance in (SEMANA, AMBOS):
        tope_semana = (
            registro.porcentaje(P_SEMANA_PCT).valor
            if unidad == PORCENTAJE
            else registro.decimal(P_SEMANA_USD)
        )
    try:
        huso, supuesto = huso_canonico(registro.texto(P_REINICIO_HUSO)), False
    except ParametroDesconocidoError:
        huso, supuesto = huso_perfil, True
    return TopeTrader(
        alcance,
        magnitud,
        unidad,
        tope_dia,
        tope_semana,
        registro.opcion(P_BASE_DIA),
        registro.opcion(P_BASE_SEMANA),
        huso,
        supuesto,
    )


# ------------------------------------------------------------------------------ el seguidor


def _medianoche(dia: date, huso: ZoneInfo) -> datetime:
    return datetime.combine(dia, time(0), tzinfo=huso).astimezone(UTC)


def _lunes(dia: date) -> date:
    return dia - timedelta(days=dia.weekday())


class SeguidorTope:
    """Lleva los cortes del tope del trader con su propio reloj y da los acumuladores de RN-020.
    Recibe el saldo y la equity de la cuenta en cada instante; no toca la cuenta."""

    def __init__(self, tope: TopeTrader, primer_instante: datetime, saldo: Decimal) -> None:
        self.tope = tope
        self.dia = primer_instante.astimezone(tope.huso_reinicio).date()
        self.saldo_corte_dia = saldo
        self.saldo_corte_semana = saldo
        self.cortes: list[tuple[datetime, str]] = []  # (instante UTC, "dia" | "semana")

    def avanzar(self, instante: datetime, saldo: Decimal) -> None:
        """Corta los dias (y las semanas) que `instante` cruce, con el saldo de ese momento."""
        siguiente = self.dia + timedelta(days=1)
        while _medianoche(siguiente, self.tope.huso_reinicio) <= instante:
            self.dia = siguiente
            self.saldo_corte_dia = saldo
            self.cortes.append((_medianoche(siguiente, self.tope.huso_reinicio), DIA))
            if _lunes(siguiente) == siguiente:
                self.saldo_corte_semana = saldo
                self.cortes.append((_medianoche(siguiente, self.tope.huso_reinicio), SEMANA))
            siguiente = self.dia + timedelta(days=1)

    def _base(self, cual: str, saldo: Decimal) -> Decimal:
        if cual == BASE_SALDO_ACTUAL:
            return saldo
        if cual == BASE_INICIAL_SEMANA:
            return self.saldo_corte_semana
        return self.saldo_corte_dia

    def acumuladores(self, saldo: Decimal, equity: Decimal) -> dict[str, Decimal]:
        """`perdida_dia` y `perdida_semana` en la unidad del tope (recortados en cero), y los
        topes con los que se comparan, en esa misma unidad. Sin tope, vacio: RN-020 no lee nada."""
        t = self.tope
        if t.alcance == SIN_TOPE:
            return {}
        vigilada = equity if t.magnitud == EQUITY else saldo
        salida: dict[str, Decimal] = {}
        filas = (
            (ACUMULADOR_DIA, t.aplica_dia, self.saldo_corte_dia, t.base_dia, t.tope_dia),
            (
                ACUMULADOR_SEMANA,
                t.aplica_semana,
                self.saldo_corte_semana,
                t.base_semana,
                t.tope_semana,
            ),
        )
        for cual, aplica, corte, base_nombre, tope in filas:
            if not aplica or tope is None:
                continue
            perdida = max(Decimal(0), corte - vigilada)
            if t.unidad == PORCENTAJE:
                base = self._base(base_nombre, saldo)
                perdida = perdida / base * CIEN if base > 0 else Decimal(0)
            salida[cual] = perdida
            salida[f"{cual}:tope"] = tope
        return salida


__all__ = [
    "ACUMULADOR_DIA",
    "ACUMULADOR_SEMANA",
    "ALCANCES",
    "AMBOS",
    "DIA",
    "EQUITY",
    "MAGNITUDES",
    "ORIGEN_FIRMA",
    "ORIGEN_TRADER",
    "PORCENTAJE",
    "SALDO",
    "SEMANA",
    "SIN_TOPE",
    "SUPUESTO_HUSO",
    "UNIDADES",
    "USD",
    "SeguidorTope",
    "TopeRechazadoError",
    "TopeSinFijarError",
    "TopeTrader",
    "tope_del_registro",
]
