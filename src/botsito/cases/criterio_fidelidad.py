"""El criterio de fidelidad en desarrollo (ADR-0043): emparejar y medir, SIN motor.

Compara operaciones del trader -las de los `caso-*.yaml` `dev`- con operaciones del bot, cuando
exista. Este modulo NO produce ninguna decision del bot: recibe las dos listas y las compara. Es
puro -sin IO salvo `cargar_criterio`-, y sus cifras no viven aqui sino en
`knowledge/cases/criterio_fidelidad.yaml` (ADR-0002: ninguna cifra de negocio en `src/`).

**LA UNIDAD es la operacion, dentro de su dia y su sesion.** Una operacion del bot empareja con una
del trader si coinciden el dia, la sesion y la direccion, `|Δentrada|` no pasa de la tolerancia en
puntos y `|Δinstante de llenado|` no pasa de la tolerancia en minutos. El instante del caso ES el
llenado (medido: `docs/validation/INSTANTE-LLENADO-SALIDA.txt`).

**UNO A UNO Y DETERMINISTA.** Entre todas las parejas compatibles se toman, en este orden, la de
menor `|Δinstante|`, luego la de menor `|Δentrada|`, luego la mas temprana; y ninguna
operacion se usa dos veces. Es un emparejamiento voraz global: el primer criterio de desempate
manda sobre todo el dia, no solo sobre una operacion.

**LO QUE NO PUNTUA.** Las operaciones del bot en dias sin ninguna del trader se cuentan aparte y no
entran en la precision: leer esa ausencia como decision del trader es una inferencia nuestra
(ADR-0016). Y fuera del criterio quedan stop, TP, resultado y gestion hasta que se resuelvan sus
ambiguedades (ADR-0043).
"""

from __future__ import annotations

import random
import re
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from pathlib import Path

from botsito.comun.yaml_estricto import YamlError, leer_yaml

FICHERO_CRITERIO = "knowledge/cases/criterio_fidelidad.yaml"
_SEGUNDOS_POR_MINUTO = 60


class CriterioError(ValueError):
    """El fichero del criterio no tiene la forma declarada."""


@dataclass(frozen=True)
class Operacion:
    dia: str
    sesion: str
    direccion: str
    instante: datetime  # el LLENADO, con huso
    entrada: Decimal
    # el stop del caso del trader, para la fidelidad por criterios (ADR-0092 §2); el emparejamiento
    # por operacion de ADR-0043 no lo mira. None en las operaciones del bot y en un caso sin stop
    stop: Decimal | None = None


@dataclass(frozen=True)
class Tolerancias:
    entrada_puntos: int
    instante_min: int
    escala: int  # puntos por unidad de precio del instrumento


@dataclass(frozen=True)
class Criterio:
    tolerancias: Tolerancias
    umbral_cobertura: Fraction
    umbral_precision: Fraction
    construccion: tuple[str, ...]
    medida: tuple[str, ...]
    # El umbral de CONSTRUCCION que habilita medir (ADR-0070): sobre una corrida del arnes en
    # todo `construccion`, sin diagnostico.
    umbral_construccion_para_medir_cobertura: Fraction
    umbral_construccion_para_medir_precision: Fraction
    # El perfil de cuenta con el que la corrida simulada tiene que correr para habilitar
    # (ADR-0070, enmienda del 2026-10-07); la fase es la primera de ese perfil.
    perfil_para_medir: str
    # ADR-0092: la tolerancia del stop de la fidelidad por criterios y el criterio de rentabilidad.
    # `cargar_criterio` los exige; el None es solo para los criterios sinteticos de los tests de
    # antes, que no los usan.
    tolerancia_stop_puntos: int | None = None
    rentabilidad: CriterioRentabilidad | None = None
    # ADR-0092 §11 (PARADA 2, punto 1): los libros de construccion sin video, para el sesgo 3
    material_sin_video: MaterialSinVideo | None = None


@dataclass(frozen=True)
class Pareja:
    trader: Operacion
    bot: Operacion
    delta_segundos: int
    delta_puntos: Decimal


@dataclass(frozen=True)
class Medida:
    parejas: tuple[Pareja, ...]
    n_trader: int
    n_bot_puntuables: int
    n_bot_fuera: int  # del bot en dias sin ninguna operacion del trader: no puntuan (ADR-0016)
    cobertura: Fraction | None  # None = sin definir (cero operaciones del trader)
    precision: Fraction | None  # None = sin definir (cero operaciones del bot puntuables)
    mismo_minuto: int
    delta_instante_min: dict[int, int]  # |Δinstante| en minutos enteros -> cuantas
    delta_entrada_puntos: dict[Decimal, int]  # |Δentrada| en puntos -> cuantas


def _deltas(trader: Operacion, bot: Operacion, tol: Tolerancias) -> tuple[int, Decimal]:
    segundos = abs(int((bot.instante - trader.instante).total_seconds()))
    puntos = abs(bot.entrada - trader.entrada) * tol.escala
    return segundos, puntos


def compatibles(trader: Operacion, bot: Operacion, tol: Tolerancias) -> bool:
    if (trader.dia, trader.sesion, trader.direccion) != (bot.dia, bot.sesion, bot.direccion):
        return False
    segundos, puntos = _deltas(trader, bot, tol)
    return puntos <= tol.entrada_puntos and segundos <= tol.instante_min * _SEGUNDOS_POR_MINUTO


def emparejar(
    trader: Sequence[Operacion], bot: Sequence[Operacion], tol: Tolerancias
) -> tuple[Pareja, ...]:
    """Uno a uno y determinista.

    Menor |Δinstante|, luego menor |Δentrada|, luego la mas temprana."""
    candidatas: list[tuple[int, Decimal, datetime, datetime, int, int]] = []
    for i, t in enumerate(trader):
        for j, b in enumerate(bot):
            if compatibles(t, b, tol):
                segundos, puntos = _deltas(t, b, tol)
                candidatas.append((segundos, puntos, min(t.instante, b.instante), b.instante, i, j))
    candidatas.sort()
    usados_t: set[int] = set()
    usados_b: set[int] = set()
    parejas: list[Pareja] = []
    for segundos, puntos, _, _, i, j in candidatas:
        if i in usados_t or j in usados_b:
            continue
        usados_t.add(i)
        usados_b.add(j)
        parejas.append(Pareja(trader[i], bot[j], segundos, puntos))
    return tuple(sorted(parejas, key=lambda p: (p.trader.instante, p.bot.instante)))


def _minuto(instante: datetime) -> datetime:
    return instante.replace(second=0, microsecond=0)


def medir(trader: Sequence[Operacion], bot: Sequence[Operacion], tol: Tolerancias) -> Medida:
    """Cobertura, precision y distribuciones. Nunca divide por cero: sin denominador, `None`."""
    dias_trader = {t.dia for t in trader}
    puntuables = [b for b in bot if b.dia in dias_trader]
    parejas = emparejar(trader, puntuables, tol)
    return Medida(
        parejas=parejas,
        n_trader=len(trader),
        n_bot_puntuables=len(puntuables),
        n_bot_fuera=len(bot) - len(puntuables),
        cobertura=Fraction(len(parejas), len(trader)) if trader else None,
        precision=Fraction(len(parejas), len(puntuables)) if puntuables else None,
        mismo_minuto=sum(
            1 for p in parejas if _minuto(p.trader.instante) == _minuto(p.bot.instante)
        ),
        delta_instante_min=dict(Counter(p.delta_segundos // _SEGUNDOS_POR_MINUTO for p in parejas)),
        delta_entrada_puntos=dict(Counter(p.delta_puntos for p in parejas)),
    )


@dataclass(frozen=True)
class Simulacion:
    """Con que corrio el broker simulado: el perfil y la fase EFECTIVOS (dados o por defecto) y la
    primera fase que declara ese perfil. Sin simulacion, la corrida no lleva este objeto."""

    perfil: str
    fase: str
    primera_fase: str


@dataclass(frozen=True)
class Veredicto:
    """Si una corrida de construccion habilita medir el conjunto de medida (ADR-0070), y por que
    no: un motivo por cada condicion que falta. Sin motivos, habilita."""

    habilita: bool
    motivos: tuple[str, ...]


def _por_ciento(f: Fraction) -> str:
    return f"{float(f) * 100:.1f} %"


def habilita_medir(
    medida: Medida,
    criterio: Criterio,
    meses: Sequence[str],
    *,
    opciones_fuera: Sequence[str],
    simulacion: Simulacion | None,
) -> Veredicto:
    """ADR-0070, con su enmienda del 2026-10-07. Habilita solo si la corrida (1) no uso ninguna
    opcion fuera de la lista CERRADA de las que no cambian lo que el motor decide ni como se llena
    (`opciones_fuera` vacia: la lista y el calculo viven en `engine/arnes.py`), (2) cubre TODO el
    conjunto de construccion y (3) llega, en esa misma corrida, a los dos umbrales de construccion
    para medir. Una metrica sin definir no llega. Y (enmienda del 2026-10-07) la corrida tiene que
    estar SIMULADA con `perfil_para_medir` y la primera fase de ese perfil."""
    motivos: list[str] = [f"opción fuera de la lista: {o}" for o in opciones_fuera]
    if simulacion is None:
        motivos.append("sin simulación")
    else:
        if simulacion.perfil != criterio.perfil_para_medir:
            motivos.append(f"perfil {simulacion.perfil}: solo cuenta {criterio.perfil_para_medir}")
        if simulacion.fase != simulacion.primera_fase:
            motivos.append(
                f"fase {simulacion.fase}: solo cuenta la primera del perfil, "
                f"{simulacion.primera_fase}"
            )
    faltan = sorted(set(criterio.construccion) - set(meses))
    if faltan:
        motivos.append(
            f"la corrida no cubre todo el conjunto de construccion (falta {', '.join(faltan)})"
        )
    for nombre, valor, umbral in (
        ("cobertura", medida.cobertura, criterio.umbral_construccion_para_medir_cobertura),
        ("precision", medida.precision, criterio.umbral_construccion_para_medir_precision),
    ):
        if valor is None:
            motivos.append(f"{nombre} sin definir")
        elif valor < umbral:
            motivos.append(f"{nombre} {_por_ciento(valor)} por debajo de {_por_ciento(umbral)}")
    return Veredicto(not motivos, tuple(motivos))


def _fraccion(valor: object, campo: str) -> Fraction:
    try:
        f = Fraction(str(valor))
    except (ValueError, ZeroDivisionError) as exc:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} no es un numero") from exc
    if not 0 <= f <= 1:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} va entre 0 y 1")
    return f


def _entero(doc: dict[str, object], campo: str) -> int:
    valor = doc.get(campo)
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es un entero positivo")
    return valor


def _texto(doc: dict[str, object], campo: str) -> str:
    valor = doc.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es un texto no vacio")
    return valor


def _meses(doc: dict[str, object], campo: str) -> tuple[str, ...]:
    valor = doc.get(campo)
    if not isinstance(valor, list) or not all(isinstance(m, str) for m in valor):
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es una lista de meses AAAA-MM")
    return tuple(valor)


_MES = re.compile(r"\d{4}-(0[1-9]|1[0-2])", re.ASCII)


def _decimal(doc: dict[str, object], campo: str) -> Decimal:
    """Un numero escrito como TEXTO (como los umbrales): un numero del yaml se rechaza, para que
    nadie lea 0.1 de coma flotante."""
    valor = doc.get(campo)
    if not isinstance(valor, str):
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es un numero escrito como texto")
    try:
        d = Decimal(valor)
    except InvalidOperation as exc:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} no es un numero") from exc
    if not d.is_finite():
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} no es un numero finito")
    return d


def _percentil(doc: dict[str, object], campo: str) -> int:
    valor = _entero(doc, campo)
    if not valor < _POR_CIEN:
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} es un percentil entre 1 y 99")
    return valor


def _meses_validos(doc: dict[str, object], campo: str) -> tuple[str, ...]:
    meses = _meses(doc, campo)
    for mes in meses:
        if not _MES.fullmatch(mes):
            raise CriterioError(f"{FICHERO_CRITERIO}: {campo}: {mes!r} no es un mes AAAA-MM")
    if len(set(meses)) != len(meses):
        raise CriterioError(f"{FICHERO_CRITERIO}: {campo} repite un mes")
    return meses


def _rentabilidad(doc: dict[str, object]) -> CriterioRentabilidad:
    """El bloque `rentabilidad` (ADR-0092 §13): obligatorio y entero."""
    bloque = doc.get("rentabilidad")
    if not isinstance(bloque, dict):
        raise CriterioError(f"{FICHERO_CRITERIO}: falta el bloque rentabilidad (ADR-0092)")
    deslizamiento = _texto(bloque, "deslizamiento")
    if deslizamiento not in DESLIZAMIENTOS:
        raise CriterioError(
            f"{FICHERO_CRITERIO}: rentabilidad.deslizamiento {deslizamiento!r} no es una de "
            f"{sorted(DESLIZAMIENTOS)}"
        )
    r = CriterioRentabilidad(
        fase=_texto(bloque, "fase"),
        n_minimo=_entero(bloque, "n_minimo"),
        esperanza_minima_r=_decimal(bloque, "esperanza_minima_r"),
        percentil_remuestreo=_percentil(bloque, "percentil_remuestreo"),
        replicas_remuestreo=_entero(bloque, "replicas_remuestreo"),
        semilla_remuestreo=_entero(bloque, "semilla_remuestreo"),
        perdida_diaria_max=_fraccion(bloque.get("perdida_diaria_max"), "perdida_diaria_max"),
        perdida_total_max=_fraccion(bloque.get("perdida_total_max"), "perdida_total_max"),
        deslizamiento=deslizamiento,
        percentil_deslizamiento_f17=_percentil(bloque, "percentil_deslizamiento_f17"),
        meses=_meses_validos(bloque, "meses"),
        extension=_meses_validos(bloque, "extension"),
        vistos_rentabilidad=_meses_validos(bloque, "vistos_rentabilidad"),
    )
    if not r.meses:
        raise CriterioError(f"{FICHERO_CRITERIO}: rentabilidad.meses no puede ir vacio")
    if set(r.meses) & set(r.extension):
        raise CriterioError(f"{FICHERO_CRITERIO}: un mes no puede estar en meses y en extension")
    return r


_DIA = re.compile(r"\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])", re.ASCII)


@dataclass(frozen=True)
class MaterialSinVideo:
    """El bloque `material_sin_video` (ADR-0092 §11): los meses de construccion cuyo libro NO esta
    grabado en video, los dias de esos meses que SI lo estan, y los meses que cuentan como grabados
    mientras sea provisional (julio, hasta que T lo compruebe)."""

    meses: tuple[str, ...]
    dias_con_video: tuple[str, ...]
    provisionales_con_video: tuple[str, ...]
    fuente: str

    def sin_video(self, dia: str) -> bool:
        """Si el dia es de un libro sin video: su mes lo esta y el no esta grabado. Un mes
        provisional cuenta como CON video."""
        return dia[:7] in self.meses and dia not in self.dias_con_video


def _material_sin_video(doc: dict[str, object], construccion: Sequence[str]) -> MaterialSinVideo:
    """Las cuatro comprobaciones de la PARADA 2, punto 1: el bloque existe; los meses y los dias son
    de construccion; ningun dia con video cae fuera de `meses`; ningun mes esta a la vez en `meses`
    y en `provisionales_con_video`."""
    bloque = doc.get("material_sin_video")
    if not isinstance(bloque, dict):
        raise CriterioError(f"{FICHERO_CRITERIO}: falta el bloque material_sin_video (ADR-0092)")
    meses = _meses_validos(bloque, "meses")
    provisionales = _meses_validos(bloque, "provisionales_con_video")
    valor = bloque.get("dias_con_video")
    if not isinstance(valor, list) or not all(isinstance(d, str) for d in valor):
        raise CriterioError(f"{FICHERO_CRITERIO}: dias_con_video es una lista de dias AAAA-MM-DD")
    dias = tuple(valor)
    for dia in dias:
        try:
            valida = _DIA.fullmatch(dia) is not None and date.fromisoformat(dia).isoformat() == dia
        except ValueError:
            valida = False
        if not valida:
            raise CriterioError(f"{FICHERO_CRITERIO}: dias_con_video: {dia!r} no es AAAA-MM-DD")
    for mes in (*meses, *provisionales, *(d[:7] for d in dias)):
        if mes not in construccion:
            raise CriterioError(
                f"{FICHERO_CRITERIO}: material_sin_video: {mes} no es un mes de construccion"
            )
    for dia in dias:
        if dia[:7] not in meses:
            raise CriterioError(
                f"{FICHERO_CRITERIO}: dias_con_video: {dia} no cae en material_sin_video.meses"
            )
    if set(meses) & set(provisionales):
        raise CriterioError(
            f"{FICHERO_CRITERIO}: un mes no puede estar en meses y en provisionales_con_video"
        )
    return MaterialSinVideo(meses, dias, provisionales, _texto(bloque, "fuente"))


def cargar_criterio(repo: Path) -> Criterio:
    try:
        doc = leer_yaml(repo / FICHERO_CRITERIO)
    except (OSError, YamlError) as exc:
        raise CriterioError(f"{FICHERO_CRITERIO}: {exc}") from exc
    if not isinstance(doc, dict):
        raise CriterioError(f"{FICHERO_CRITERIO}: se espera un mapa")
    construccion, medida = _meses(doc, "construccion"), _meses(doc, "medida")
    if set(construccion) & set(medida):
        raise CriterioError(f"{FICHERO_CRITERIO}: un mes no puede construir y medir a la vez")
    rentabilidad = _rentabilidad(doc)
    ajenos = set(rentabilidad.meses) | set(rentabilidad.extension)
    if ajenos & (set(construccion) | set(medida)):
        raise CriterioError(
            f"{FICHERO_CRITERIO}: un mes de rentabilidad no puede ser de construccion ni de medida"
        )
    return Criterio(
        tolerancias=Tolerancias(
            entrada_puntos=_entero(doc, "tolerancia_entrada_puntos"),
            instante_min=_entero(doc, "tolerancia_instante_min"),
            escala=_entero(doc, "escala_puntos"),
        ),
        umbral_cobertura=_fraccion(doc.get("umbral_cobertura"), "umbral_cobertura"),
        umbral_precision=_fraccion(doc.get("umbral_precision"), "umbral_precision"),
        construccion=construccion,
        medida=medida,
        umbral_construccion_para_medir_cobertura=_fraccion(
            doc.get("umbral_construccion_para_medir_cobertura"),
            "umbral_construccion_para_medir_cobertura",
        ),
        umbral_construccion_para_medir_precision=_fraccion(
            doc.get("umbral_construccion_para_medir_precision"),
            "umbral_construccion_para_medir_precision",
        ),
        perfil_para_medir=_texto(doc, "perfil_para_medir"),
        tolerancia_stop_puntos=_entero(doc, "tolerancia_stop_puntos"),
        rentabilidad=rentabilidad,
        material_sin_video=_material_sin_video(doc, construccion),
    )


# ======================================================================= ADR-0092: el metodo
#
# Todo lo de abajo es PURO (sin IO): recibe lo que el simulador ya produjo y lo mide. Ninguna
# decision del bot lo lee. Las cifras, en el yaml (ADR-0002).

DESLIZAMIENTO_PENDIENTE_F17 = "pendiente_F17"
DESLIZAMIENTOS = frozenset({DESLIZAMIENTO_PENDIENTE_F17})
_POR_CIEN = 100


@dataclass(frozen=True)
class CriterioRentabilidad:
    """El bloque `rentabilidad` de `criterio_fidelidad.yaml` (ADR-0092 §3, §4 y §5)."""

    fase: str
    n_minimo: int
    esperanza_minima_r: Decimal
    percentil_remuestreo: int
    replicas_remuestreo: int
    semilla_remuestreo: int
    perdida_diaria_max: Fraction  # fraccion del capital inicial
    perdida_total_max: Fraction  # fraccion del capital inicial
    deslizamiento: str
    percentil_deslizamiento_f17: int
    meses: tuple[str, ...]
    extension: tuple[str, ...]
    vistos_rentabilidad: tuple[str, ...]


# ------------------------------------------------------------- la cascada (ADR-0092 §1 y §2)

SIN_ORDEN = "sin orden del bot en su (dia, sesion, direccion)"
ENTRADA_FUERA = "orden, con la entrada fuera de tolerancia"
STOP_FUERA = "entrada, con el stop fuera de tolerancia"
SIN_STOP = "entrada; el caso no trae stop"
NO_LLENADA = "en el nivel, no llenada"
LLENADA_FUERA = "en el nivel, llenada fuera de tolerancia de instante"
COMPLETA = "las cuatro piezas"
ESCALONES = (SIN_ORDEN, ENTRADA_FUERA, STOP_FUERA, SIN_STOP, NO_LLENADA, LLENADA_FUERA, COMPLETA)


@dataclass(frozen=True)
class OrdenCriterio:
    """Una orden que el bot coloco, llenada o no, en la forma de la cascada."""

    dia: str
    sesion: str
    direccion: str
    colocada: datetime
    entrada: Decimal
    stop: Decimal
    llenado: datetime | None  # None: no se lleno


@dataclass(frozen=True)
class PasoCascada:
    trader: Operacion
    orden: OrdenCriterio | None
    escalon: str


@dataclass(frozen=True)
class Cascada:
    pasos: tuple[PasoCascada, ...]
    ordenes_sin_trader: (
        int  # ordenes del bot en un (dia, sesion, direccion) sin operacion del trader
    )


def _clave(x: Operacion | OrdenCriterio) -> tuple[str, str, str]:
    return x.dia, x.sesion, x.direccion


def _puntos_entre(a: Decimal, b: Decimal, escala: int) -> Decimal:
    return abs(a - b) * escala


def cascada_por_criterios(
    trader: Sequence[Operacion],
    ordenes: Sequence[OrdenCriterio],
    tol: Tolerancias,
    tolerancia_stop_puntos: int,
) -> Cascada:
    """ADR-0092 §2. Para cada operacion del trader, la orden del bot de su (dia, sesion, direccion)
    mas cercana en ENTRADA (a igualdad, la de colocacion mas cercana a su llenado, y luego la mas
    temprana), y el ULTIMO escalon que alcanza: hay orden; entrada a <= tolerancia; stop a <=
    tolerancia; llenada a <= la tolerancia de instante. No es uno a uno: dos operaciones del trader
    pueden mirar la misma orden."""
    por_clave: dict[tuple[str, str, str], list[OrdenCriterio]] = {}
    for o in ordenes:
        por_clave.setdefault(_clave(o), []).append(o)
    pasos: list[PasoCascada] = []
    for t in trader:
        candidatas = por_clave.get(_clave(t), [])
        if not candidatas:
            pasos.append(PasoCascada(t, None, SIN_ORDEN))
            continue
        o = min(
            candidatas,
            key=lambda c: (
                _puntos_entre(c.entrada, t.entrada, tol.escala),
                abs((c.colocada - t.instante).total_seconds()),
                c.colocada,
            ),
        )
        if _puntos_entre(o.entrada, t.entrada, tol.escala) > tol.entrada_puntos:
            escalon = ENTRADA_FUERA
        elif t.stop is None:
            escalon = SIN_STOP
        elif _puntos_entre(o.stop, t.stop, tol.escala) > tolerancia_stop_puntos:
            escalon = STOP_FUERA
        elif o.llenado is None:
            escalon = NO_LLENADA
        elif (
            abs((o.llenado - t.instante).total_seconds()) > tol.instante_min * _SEGUNDOS_POR_MINUTO
        ):
            escalon = LLENADA_FUERA
        else:
            escalon = COMPLETA
        pasos.append(PasoCascada(t, o, escalon))
    claves_trader = {_clave(t) for t in trader}
    sin_trader = sum(1 for o in ordenes if _clave(o) not in claves_trader)
    return Cascada(tuple(pasos), sin_trader)


def cascada_por_mes(cascada: Cascada) -> dict[str, Counter[str]]:
    """El recuento de escalones por mes (AAAA-MM del dia), mas «total»."""
    salida: dict[str, Counter[str]] = {}
    for p in cascada.pasos:
        salida.setdefault(p.trader.dia[:7], Counter())[p.escalon] += 1
        salida.setdefault("total", Counter())[p.escalon] += 1
    return salida


# ------------------------------------------------------------- la rentabilidad (ADR-0092 §3)


@dataclass(frozen=True)
class PosicionCerrada:
    """Una operacion llenada y cerrada del bot, con lo que la cuenta ya cobro (ADR-0092 §3)."""

    dia: str
    pnl_neto: Decimal  # USD, con comision y swaps
    riesgo: Decimal  # USD al colocar, como dimensiona la cuenta
    entrada_por_stop: bool  # la entrada fue una orden stop (ADR-0092 §4)
    cierre: str  # el motivo del cierre del broker: stop, objetivo o manual
    lotes: Decimal
    valor_punto_por_lote: Decimal  # USD por punto y por lote: contrato / escala


def r_neto(p: PosicionCerrada) -> Decimal:
    if p.riesgo <= 0:
        raise CriterioError(f"{p.dia}: riesgo al colocar no positivo ({p.riesgo})")
    return p.pnl_neto / p.riesgo


def esperanza_r(posiciones: Sequence[PosicionCerrada]) -> Decimal | None:
    """La media del R neto; sin operaciones, sin definir."""
    if not posiciones:
        return None
    return sum((r_neto(p) for p in posiciones), Decimal(0)) / len(posiciones)


def percentil_por_dias(
    posiciones: Sequence[PosicionCerrada],
    dias: Sequence[str],
    *,
    replicas: int,
    semilla: int,
    percentil: int,
) -> Decimal | None:
    """ADR-0092 §3 c): el percentil de la media del R neto por remuestreo POR DIAS de mercado (la
    forma la fijo el consultor en la PARADA 2 de trabajo/metodo-fidelidad-rentabilidad). Ver
    `remuestreo_por_dias`, que dice ademas cuantas replicas se descartaron."""
    return remuestreo_por_dias(
        posiciones, dias, replicas=replicas, semilla=semilla, percentil=percentil
    )[0]


def remuestreo_por_dias(
    posiciones: Sequence[PosicionCerrada],
    dias: Sequence[str],
    *,
    replicas: int,
    semilla: int,
    percentil: int,
) -> tuple[Decimal | None, int]:
    """(percentil, replicas descartadas). Cada replica sortea con reemplazo tantos dias como
    `dias` (todos los dias de mercado corridos, con o sin operaciones) y toma la media AGRUPADA del
    R neto de todas las operaciones de los dias sorteados; una replica sin ninguna operacion no
    cuenta y se cuenta como descartada. El percentil es el de rango inferior sobre las medias
    ordenadas: el indice floor(percentil * (n - 1) / 100). `random.Random` con la semilla."""
    if not posiciones or not dias:
        return None, 0
    por_dia: dict[str, list[Decimal]] = {d: [] for d in dias}
    for p in posiciones:
        if p.dia not in por_dia:
            raise CriterioError(f"{p.dia}: una operacion en un dia que no esta entre los corridos")
        por_dia[p.dia].append(r_neto(p))
    sumas = [(sum(v, Decimal(0)), len(v)) for v in (por_dia[d] for d in dias)]
    azar = random.Random(semilla)
    medias: list[Decimal] = []
    for _ in range(replicas):
        total, n = Decimal(0), 0
        for _ in dias:
            s, k = sumas[azar.randrange(len(sumas))]
            total += s
            n += k
        if n:
            medias.append(total / n)
    descartadas = replicas - len(medias)
    if not medias:
        return None, descartadas
    medias.sort()
    return medias[(percentil * (len(medias) - 1)) // _POR_CIEN], descartadas


DiaCurva = tuple[str, Decimal, Decimal, Decimal | None]  # dia, saldo al corte, final, equity minima


def _peor_del_dia(corte: Decimal, final: Decimal, minima: Decimal | None) -> Decimal:
    # sin equity minima, el dia no tuvo posicion viva: la equity fue el saldo
    return minima if minima is not None else min(corte, final)


def perdida_diaria_maxima(curva: Sequence[DiaCurva], capital: Decimal, base: str) -> Fraction:
    """ADR-0092 §3 d): la mayor perdida de un dia, en fraccion del capital inicial, sobre la equity
    minima del dia (la magnitud que vigila la firma) y desde la base de la firma: el saldo al corte
    (`saldo_corte_diario`) o el capital (`saldo_inicial_cuenta`)."""
    if base not in BASES_PERDIDA_DIARIA:
        raise CriterioError(f"base de la perdida diaria desconocida: {base!r}")
    peor = Decimal(0)
    for _, corte, final, minima in curva:
        desde = corte if base == BASE_SALDO_CORTE else capital
        peor = max(peor, desde - _peor_del_dia(corte, final, minima))
    return Fraction(peor) / Fraction(capital)


def equity_minima_del_tramo(curva: Sequence[DiaCurva], capital: Decimal) -> Fraction:
    """ADR-0092 §3 e): la menor equity del tramo, en fraccion del capital inicial."""
    if not curva:
        return Fraction(1)
    peor = min(_peor_del_dia(c, f, m) for _, c, f, m in curva)
    return Fraction(min(peor, capital)) / Fraction(capital)


@dataclass(frozen=True)
class CuentaDelTramo:
    """Una cuenta mensual (ADR-0092 §8): su mes, su curva y si entro en SUSPENDIDA."""

    mes: str
    curva: tuple[DiaCurva, ...]
    suspendida: bool


@dataclass(frozen=True)
class MedidaPorCuentas:
    perdida_diaria_maxima: Fraction
    mes_perdida_diaria: str | None  # el de la peor cuenta; None sin cuentas
    equity_minima: Fraction
    mes_equity_minima: str | None
    meses_suspendidos: tuple[str, ...]


def medir_por_cuentas(
    cuentas: Sequence[CuentaDelTramo], capital: Decimal, base: str
) -> MedidaPorCuentas:
    """ADR-0092 §3 d), e) y f) con una cuenta por mes (§8): d) y e) de cada cuenta contra el capital
    inicial del perfil, el mismo para todas, y la peor con su mes (a igualdad, la primera); f), los
    meses de las que entraron en SUSPENDIDA. Como d) y e) son un maximo y un minimo por dia, la peor
    cuenta da la misma cifra que la curva de todos los dias seguida: lo nuevo es el mes."""
    if not cuentas:
        return MedidaPorCuentas(Fraction(0), None, Fraction(1), None, ())
    d = [(perdida_diaria_maxima(c.curva, capital, base), c.mes) for c in cuentas]
    e = [(equity_minima_del_tramo(c.curva, capital), c.mes) for c in cuentas]
    peor_d = max(d, key=lambda x: x[0])
    peor_e = min(e, key=lambda x: x[0])
    return MedidaPorCuentas(
        peor_d[0], peor_d[1], peor_e[0], peor_e[1], tuple(c.mes for c in cuentas if c.suspendida)
    )


BASE_SALDO_CORTE = "saldo_corte_diario"
BASE_CAPITAL = "saldo_inicial_cuenta"
BASES_PERDIDA_DIARIA = frozenset({BASE_SALDO_CORTE, BASE_CAPITAL})

PASA = "pasa"
NO_PASA = "no pasa"
INSUFICIENTE = "insuficiente"
PENDIENTE_F17 = "pendiente de F17"


@dataclass(frozen=True)
class MedidaRentabilidad:
    n: int
    esperanza: Decimal | None
    percentil_remuestreo: Decimal | None
    perdida_diaria_maxima: Fraction
    equity_minima: Fraction
    suspendida: bool
    replicas_descartadas: int = 0  # replicas sin ninguna operacion (PARADA 2, punto 2)
    # una cuenta por mes (ADR-0092 §8): cuantas cuentas mide y los meses de las que entraron en
    # SUSPENDIDA, para el motivo de f); con una, el de siempre
    cuentas: int = 1
    meses_suspendidos: tuple[str, ...] = ()


@dataclass(frozen=True)
class VeredictoRentabilidad:
    estado: str  # PASA, NO_PASA, INSUFICIENTE o PENDIENTE_F17
    motivos: tuple[str, ...]


def medir_rentabilidad(
    posiciones: Sequence[PosicionCerrada],
    dias: Sequence[str],
    curva: Sequence[DiaCurva],
    capital: Decimal,
    base: str,
    suspendida: bool,
    criterio: CriterioRentabilidad,
) -> MedidaRentabilidad:
    percentil, descartadas = remuestreo_por_dias(
        posiciones,
        dias,
        replicas=criterio.replicas_remuestreo,
        semilla=criterio.semilla_remuestreo,
        percentil=criterio.percentil_remuestreo,
    )
    return MedidaRentabilidad(
        n=len(posiciones),
        esperanza=esperanza_r(posiciones),
        percentil_remuestreo=percentil,
        perdida_diaria_maxima=perdida_diaria_maxima(curva, capital, base),
        equity_minima=equity_minima_del_tramo(curva, capital),
        suspendida=suspendida,
        replicas_descartadas=descartadas,
    )


def veredicto_rentabilidad(
    medida: MedidaRentabilidad,
    criterio: CriterioRentabilidad,
    *,
    deslizamiento_medido: bool = False,
) -> VeredictoRentabilidad:
    """ADR-0092 §3 y §4: sin N, «insuficiente»; con N, «no pasa» con un motivo por cada criterio
    que falte; con todos, «pendiente de F17» mientras el deslizamiento lo este (la puerta no puede
    dar «pasa» antes de F17); y «pasa» solo con el deslizamiento ya medido (`veredicto_con_f17`)."""
    if medida.n < criterio.n_minimo:
        return VeredictoRentabilidad(
            INSUFICIENTE, (f"a) N = {medida.n}, por debajo de {criterio.n_minimo}",)
        )
    motivos: list[str] = []
    if medida.esperanza is None or medida.esperanza < criterio.esperanza_minima_r:
        motivos.append(
            f"b) esperanza {_r(medida.esperanza)} por debajo de {criterio.esperanza_minima_r} R"
        )
    if medida.percentil_remuestreo is None or medida.percentil_remuestreo <= 0:
        motivos.append(
            f"c) percentil {criterio.percentil_remuestreo} del remuestreo "
            f"{_r(medida.percentil_remuestreo)}, no mayor que 0"
        )
    if medida.perdida_diaria_maxima >= criterio.perdida_diaria_max:
        motivos.append(
            f"d) perdida diaria maxima {_por_ciento(medida.perdida_diaria_maxima)}, en o por "
            f"encima de {_por_ciento(criterio.perdida_diaria_max)}"
        )
    if medida.equity_minima < 1 - criterio.perdida_total_max:
        motivos.append(
            f"e) equity minima {_por_ciento(medida.equity_minima)}, por debajo de "
            f"{_por_ciento(1 - criterio.perdida_total_max)}"
        )
    if medida.suspendida:
        motivos.append(
            "f) la cuenta entro en SUSPENDIDA"
            if medida.cuentas == 1
            else f"f) alguna cuenta entro en SUSPENDIDA ({', '.join(medida.meses_suspendidos)})"
        )
    if motivos:
        return VeredictoRentabilidad(NO_PASA, tuple(motivos))
    if criterio.deslizamiento == DESLIZAMIENTO_PENDIENTE_F17 and not deslizamiento_medido:
        return VeredictoRentabilidad(
            PENDIENTE_F17, ("deslizamiento pendiente de F17: la puerta no da «pasa» antes",)
        )
    return VeredictoRentabilidad(PASA, ())


def _r(valor: Decimal | None) -> str:
    return "sin definir" if valor is None else f"{valor:.3f}"


def _fills_afectados(p: PosicionCerrada) -> int:
    """ADR-0092 §4: cuantos llenados de la operacion pagan deslizamiento: la entrada si fue una
    orden stop, y el cierre si fue por stop o a mercado (los cierres por objetivo no se tocan)."""
    return int(p.entrada_por_stop) + int(p.cierre in CIERRES_CON_DESLIZAMIENTO)


CIERRE_STOP = "stop"
CIERRE_MANUAL = "manual"
CIERRES_CON_DESLIZAMIENTO = frozenset({CIERRE_STOP, CIERRE_MANUAL})


def con_deslizamiento(p: PosicionCerrada, puntos: Decimal) -> PosicionCerrada:
    """ADR-0092 §4: la operacion con `puntos` restados a cada llenado afectado, sin volver a correr
    el bot: los lotes no cambian."""
    ajuste = puntos * _fills_afectados(p) * p.lotes * p.valor_punto_por_lote
    return replace(p, pnl_neto=p.pnl_neto - ajuste)


def curva_con_deslizamiento(
    curva: Sequence[DiaCurva], posiciones: Sequence[PosicionCerrada], puntos: Decimal
) -> list[DiaCurva]:
    """ADR-0092 §4: la curva recompuesta operacion a operacion, sumando el ajuste al dia de cada
    cierre: el ajuste de un dia baja su equity minima y su saldo final, y el acumulado de los dias
    anteriores baja tambien su saldo al corte. Los bloqueos de RN-032 no se recalculan."""
    por_dia: dict[str, Decimal] = {}
    for p in posiciones:
        por_dia[p.dia] = por_dia.get(p.dia, Decimal(0)) + (
            p.pnl_neto - con_deslizamiento(p, puntos).pnl_neto
        )
    salida: list[DiaCurva] = []
    previo = Decimal(0)
    for dia, corte, final, minima in curva:
        del_dia = por_dia.get(dia, Decimal(0))
        salida.append(
            (
                dia,
                corte - previo,
                final - previo - del_dia,
                None if minima is None else minima - previo - del_dia,
            )
        )
        previo += del_dia
    return salida


def punto_de_equilibrio(posiciones: Sequence[PosicionCerrada], objetivo: Decimal) -> Decimal | None:
    """ADR-0092 §4: el deslizamiento por llenado afectado, en puntos, que lleva la esperanza del R
    neto a `objetivo`. La esperanza baja en linea recta con el deslizamiento; sin ninguna operacion
    con un llenado afectado, sin definir. Negativo: la esperanza ya esta por debajo."""
    base = esperanza_r(posiciones)
    if base is None:
        return None
    pendiente = sum(
        (_fills_afectados(p) * p.lotes * p.valor_punto_por_lote / p.riesgo for p in posiciones),
        Decimal(0),
    ) / len(posiciones)
    if pendiente == 0:
        return None
    return (base - objetivo) / pendiente


def veredicto_con_f17(
    posiciones: Sequence[PosicionCerrada],
    dias: Sequence[str],
    curva: Sequence[DiaCurva],
    capital: Decimal,
    base: str,
    suspendida: bool,
    criterio: CriterioRentabilidad,
    *,
    mediana: Decimal,
    percentil_f17: Decimal,
) -> VeredictoRentabilidad:
    """ADR-0092 §4, cuando F17 mida el deslizamiento de las ordenes stop: SIN volver a correr el
    bot, se resta la MEDIANA a cada llenado afectado y se vuelven a evaluar b), c), d) y e) (d y e
    sobre la curva recompuesta); y la esperanza con el percentil `percentil_deslizamiento_f17` de
    F17 tiene que ser > 0. Los lotes y los bloqueos de RN-032 no se recalculan."""
    con_mediana = [con_deslizamiento(p, mediana) for p in posiciones]
    medida = medir_rentabilidad(
        con_mediana,
        dias,
        curva_con_deslizamiento(curva, posiciones, mediana),
        capital,
        base,
        suspendida,
        criterio,
    )
    veredicto = veredicto_rentabilidad(medida, criterio, deslizamiento_medido=True)
    if veredicto.estado == INSUFICIENTE:
        return veredicto
    con_percentil = esperanza_r([con_deslizamiento(p, percentil_f17) for p in posiciones])
    motivos = list(veredicto.motivos)
    if con_percentil is None or con_percentil <= 0:
        motivos.append(
            f"la esperanza con el percentil {criterio.percentil_deslizamiento_f17} de F17 es "
            f"{_r(con_percentil)}, no mayor que 0"
        )
    return VeredictoRentabilidad(NO_PASA if motivos else PASA, tuple(motivos))


__all__ = [
    "BASE_CAPITAL",
    "BASE_SALDO_CORTE",
    "cargar_criterio",
    "Cascada",
    "cascada_por_criterios",
    "cascada_por_mes",
    "compatibles",
    "COMPLETA",
    "con_deslizamiento",
    "Criterio",
    "CriterioError",
    "CriterioRentabilidad",
    "CuentaDelTramo",
    "curva_con_deslizamiento",
    "DESLIZAMIENTO_PENDIENTE_F17",
    "emparejar",
    "ENTRADA_FUERA",
    "equity_minima_del_tramo",
    "ESCALONES",
    "esperanza_r",
    "FICHERO_CRITERIO",
    "habilita_medir",
    "INSUFICIENTE",
    "LLENADA_FUERA",
    "MaterialSinVideo",
    "Medida",
    "MedidaPorCuentas",
    "MedidaRentabilidad",
    "medir",
    "medir_por_cuentas",
    "medir_rentabilidad",
    "NO_LLENADA",
    "NO_PASA",
    "Operacion",
    "OrdenCriterio",
    "Pareja",
    "PASA",
    "PasoCascada",
    "PENDIENTE_F17",
    "percentil_por_dias",
    "perdida_diaria_maxima",
    "PosicionCerrada",
    "punto_de_equilibrio",
    "r_neto",
    "remuestreo_por_dias",
    "Simulacion",
    "SIN_ORDEN",
    "SIN_STOP",
    "STOP_FUERA",
    "Tolerancias",
    "Veredicto",
    "veredicto_con_f17",
    "veredicto_rentabilidad",
    "VeredictoRentabilidad",
]
