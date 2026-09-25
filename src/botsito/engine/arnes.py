"""El arnes del motor (ADR-0048): dia -> motor -> operaciones del bot -> criterio de fidelidad.

**SOLO CONSTRUCCION** (ADR-0048 §7). Los meses salen de `criterio_fidelidad.yaml`: cualquier mes que
no este en `construccion` se rechaza ANTES de leer nada, y si esta en `medida` se dice. La medida
tendra su propia rama y su propio ADR.

**POR LA COMPUERTA.** Los dias son los `dev` del reparto dev-visto de cada mes (ADR-0042). Cada caso
se cruza con `casos_ocultos` ANTES de abrir su fichero, y un oculto detiene todo con
`HoldoutCerradoError`: no se lee, no se salta en silencio. Las velas no pasan por la compuerta
(ADR-0021 §1: leer velas no es abrir).

**LA MEDIDA** es `cases/criterio_fidelidad.medir`, sin tocarla (ADR-0043). **EL EMBUDO** va sobre el
grafo de hechos (ADR-0048 §5): por (dia, sesion) con operaciones del trader, que hechos de origen
`regla` se produjeron y, para cada uno que falto, en que primitivas NO_IMPLEMENTADA se pararon las
reglas que lo producen.

**LA SALIDA ES DETERMINISTA**: todo ordenado y sin tiempos, para poder compararla con `diff`. El
tiempo y la memoria los mide el comando y no entran aqui.
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from botsito.cases import visto
from botsito.cases.criterio_fidelidad import Criterio, Medida, Operacion, medir
from botsito.cases.holdout import HoldoutCerradoError, casos_ocultos
from botsito.cases.ingesta import DIRECTORIO_DEV
from botsito.cases.paquete import Config
from botsito.cases.ventanas import MINUTOS_H4
from botsito.comun.yaml_estricto import leer_yaml
from botsito.config.registro import Registro
from botsito.data.agregacion import agregar
from botsito.data.dataset import DatasetError, buscar_manifiesto, cargar_manifiesto, cargar_serie
from botsito.engine.motor import (
    DatosMercado,
    DiaDeMercado,
    Motor,
    ResultadoDia,
    Sesion,
    TrazaSesion,
)
from botsito.engine.primitivas import ANOTACION_SESGO

PARTICION_DEV = "dev"
_DIA = re.compile(r"(\d{4}-\d{2}-\d{2})$", re.ASCII)
A_FAVOR = frozenset({("compra", "alcista"), ("venta", "bajista")})
SIN_ANOTACION = "sin anotacion"


class ConjuntoError(ValueError):
    """El arnes no corre sobre ese conjunto."""


@dataclass(frozen=True)
class DiaTrader:
    id: str
    dia: str
    operaciones: tuple[Operacion, ...]


@dataclass(frozen=True)
class Corrida:
    motor: str
    meses: tuple[str, ...]
    dias: tuple[DiaTrader, ...]
    resultados: tuple[ResultadoDia, ...]


# ----------------------------------------------------------------------------------- compuerta


def validar_meses(criterio: Criterio, meses: Sequence[str]) -> tuple[str, ...]:
    if not meses:
        raise ConjuntoError("sin meses: el arnes corre sobre construccion")
    for mes in meses:
        if mes in criterio.medida:
            raise ConjuntoError(
                f"{mes} es un mes de MEDIDA (criterio_fidelidad.yaml): el arnes no lo toca. La "
                f"medida tiene su propia rama y su propio ADR (ADR-0048 §7)"
            )
        if mes not in criterio.construccion:
            raise ConjuntoError(
                f"{mes} no es un mes de construccion ({', '.join(criterio.construccion)}): el "
                f"arnes solo corre sobre construccion (ADR-0048 §7)"
            )
    return tuple(sorted(set(meses)))


def _operacion(dia: str, op: Mapping[str, Any]) -> Operacion:
    return Operacion(
        dia=dia,
        sesion=str(op["sesion"]),
        direccion=str(op["direccion"]),
        instante=datetime.fromisoformat(str(op["instante_utc"])),
        entrada=Decimal(str(op["entrada"])),
    )


def dias_de_construccion(
    repo: Path,
    criterio: Criterio,
    meses: Sequence[str],
    *,
    ocultos: Collection[str] | None = None,
    asignaciones: Mapping[str, Mapping[str, str]] | None = None,
) -> tuple[DiaTrader, ...]:
    """Los dias `dev` de los meses de construccion, por la compuerta y en orden."""
    meses = validar_meses(criterio, meses)
    vetados = set(casos_ocultos(repo) if ocultos is None else ocultos)
    salida: list[DiaTrader] = []
    for mes in meses:
        if asignaciones is not None:
            asignacion = asignaciones.get(mes, {})
        elif mes in visto.artefactos(repo):
            asignacion = visto.asignacion(repo, mes)
        else:
            raise ConjuntoError(f"{mes}: no hay reparto dev-visto; el arnes no sabe que dias leer")
        for caso in sorted(c for c, p in asignacion.items() if p == PARTICION_DEV):
            if caso in vetados:
                raise HoldoutCerradoError(
                    f"un caso de {mes} esta oculto (reservado o retirado): el arnes no lo lee"
                )
            m = _DIA.search(caso)
            if m is None:
                raise ConjuntoError(f"{caso}: el id no acaba en AAAA-MM-DD")
            dia = m.group(1)
            ruta = repo / DIRECTORIO_DEV / f"{caso}.yaml"
            ops: tuple[Operacion, ...] = ()
            if ruta.exists():
                doc = leer_yaml(ruta)
                ops = tuple(_operacion(dia, op) for op in doc.get("operaciones") or [])
            salida.append(DiaTrader(caso, dia, ops))
    return tuple(salida)


# ---------------------------------------------------------------------------------- mercado


def _mes_anterior(mes: str) -> str:
    anio, m = int(mes[:4]), int(mes[5:])
    return f"{anio - 1}-12" if m == 1 else f"{anio}-{m - 1:02d}"


def dias_de_mercado(
    repo: Path,
    carpeta_datos: Path,
    config: Config,
    registro: Registro,
    dias: Sequence[DiaTrader],
    huso_sesiones: str,
) -> dict[str, DiaDeMercado]:
    """Las H4 de cada mes y del anterior, para el calentamiento del sesgo (como MOTOR-SESGO-H4)."""
    anclaje = registro.hora("anclaje_h4")
    sesiones = tuple(Sesion(s.nombre, s.desde, s.hasta) for s in config.sesiones)
    por_mes: dict[str, DatosMercado] = {}
    salida: dict[str, DiaDeMercado] = {}
    for d in dias:
        mes = d.dia[:7]
        if mes not in por_mes:
            m1 = []
            for m in (_mes_anterior(mes), mes):
                try:
                    ruta = buscar_manifiesto(repo, f"{config.dataset_prefijo}{m}")
                except DatasetError:
                    continue  # sin el mes anterior, el calentamiento empieza en el mes
                m1 += list(cargar_serie(cargar_manifiesto(ruta), carpeta_datos).velas)
            por_mes[mes] = DatosMercado(agregar(m1, MINUTOS_H4, anclaje))
        salida[d.dia] = DiaDeMercado(
            date.fromisoformat(d.dia), huso_sesiones, sesiones, por_mes[mes]
        )
    return salida


# ------------------------------------------------------------------------------------ correr


def correr(
    nombre_motor: str,
    meses: Sequence[str],
    dias: Sequence[DiaTrader],
    mercado: Mapping[str, DiaDeMercado],
    motor: Motor,
) -> Corrida:
    resultados = tuple(motor.correr_dia(mercado[d.dia]) for d in dias)
    return Corrida(nombre_motor, tuple(meses), tuple(dias), resultados)


# ----------------------------------------------------------------------------------- informe


def _fraccion(f: Fraction | None, n: int, d: int, por_que: str) -> str:
    if f is None:
        return f"sin definir ({por_que})"
    return f"{n}/{d} ({float(f) * 100:.1f} %)"


def hechos_de_regla(vocabulario: Mapping[str, Mapping[str, Any]]) -> list[tuple[str, list[str]]]:
    """Los hechos de origen `regla`, en el orden en que la spec los declara, con sus productoras."""
    return [
        (nombre, [str(r) for r in (h.get("produce") or [])])
        for nombre, h in vocabulario["hechos"].items()
        if h.get("origen") != "broker"
    ]


def medida_de(corrida: Corrida, criterio: Criterio) -> Medida:
    trader = [op for d in corrida.dias for op in d.operaciones]
    bot = [op for r in corrida.resultados for op in r.operaciones]
    return medir(trader, bot, criterio.tolerancias)


def informe(
    corrida: Corrida, criterio: Criterio, vocabulario: Mapping[str, Mapping[str, Any]]
) -> str:
    medida = medida_de(corrida, criterio)
    hechos = hechos_de_regla(vocabulario)
    trazas: dict[tuple[str, str], TrazaSesion] = {
        (r.dia, s): t for r in corrida.resultados for s, t in r.sesiones.items()
    }
    bot_por_sesion = Counter(
        (op.dia, op.sesion) for r in corrida.resultados for op in r.operaciones
    )
    trader_por_sesion = Counter((op.dia, op.sesion) for d in corrida.dias for op in d.operaciones)
    sesiones = sorted(trader_por_sesion)
    n = len(sesiones)

    producen: Counter[str] = Counter()
    paradas: Counter[str] = Counter()
    sesgo_sesion: Counter[str] = Counter()
    filas: list[str] = []
    for clave in sesiones:
        traza = trazas.get(clave, TrazaSesion())
        partes: list[str] = []
        paradas_sesion: set[str] = set()
        for hecho, productoras in hechos:
            if hecho in traza.hechos_producidos:
                producen[hecho] += 1
                partes.append(f"{hecho}:si")
                continue
            prim = sorted({p for r, p in traza.no_implementadas if r in productoras})
            paradas_sesion.update(prim)
            partes.append(f"{hecho}:no[{', '.join(prim) if prim else 'productoras sin cumplirse'}]")
        if bot_por_sesion[clave]:
            producen["operacion del bot"] += 1
        paradas.update(paradas_sesion)
        anotado = traza.anotaciones.get(ANOTACION_SESGO, SIN_ANOTACION)
        sesgo_sesion[anotado] += 1
        filas.append(
            f"{clave[0]} {clave[1]} | trader {trader_por_sesion[clave]} | bot "
            f"{bot_por_sesion[clave]} | rn003 {anotado} | {' '.join(partes)} | disparadas "
            f"{', '.join(sorted(traza.disparadas)) or 'ninguna'}"
        )

    # Que reglas dispararon, sobre TODAS las sesiones corridas y sobre las del trader (ADR-0049,
    # H1): es donde se ve RN-033 en cada sesion ambigua, tenga o no operaciones del trader.
    corridas = sorted(trazas)
    disparadas_todas: Counter[str] = Counter()
    disparadas_trader: Counter[str] = Counter()
    for clave, traza in trazas.items():
        disparadas_todas.update(traza.disparadas)
        if clave in trader_por_sesion:
            disparadas_trader.update(traza.disparadas)

    por_operacion: Counter[str] = Counter()
    for d in corrida.dias:
        for op in d.operaciones:
            anotado = trazas.get((op.dia, op.sesion), TrazaSesion()).anotaciones.get(
                ANOTACION_SESGO, SIN_ANOTACION
            )
            if anotado in ("alcista", "bajista"):
                por_operacion["a favor" if (op.direccion, anotado) in A_FAVOR else "en contra"] += 1
            else:
                por_operacion[anotado] += 1

    lineas = [
        "# Arnes del motor",
        "",
        f"MOTOR: {corrida.motor}",
        f"CONJUNTO: construccion ({', '.join(corrida.meses)}); dias {len(corrida.dias)}; "
        f"sesiones con operaciones del trader {n}",
        "",
        "## Criterio de fidelidad (ADR-0043)",
        f"operaciones del trader: {medida.n_trader}",
        f"operaciones del bot puntuables: {medida.n_bot_puntuables}",
        f"operaciones del bot en dias sin operaciones del trader: {medida.n_bot_fuera}",
        "cobertura: "
        + _fraccion(medida.cobertura, len(medida.parejas), medida.n_trader, "cero del trader"),
        "precision: "
        + _fraccion(
            medida.precision,
            len(medida.parejas),
            medida.n_bot_puntuables,
            "cero operaciones del bot puntuables",
        ),
        f"parejas en el mismo minuto: {medida.mismo_minuto}",
        "",
        "## Embudo sobre el grafo de hechos (ADR-0048 §5)",
        "cuantas sesiones con operaciones del trader producen cada hecho:",
    ]
    lineas += [f"- {hecho}: {producen[hecho]} de {n}" for hecho, _ in hechos]
    lineas.append(f"- operacion del bot: {producen['operacion del bot']} de {n}")
    lineas += ["", "cuantas se paran en cada primitiva NO_IMPLEMENTADA:"]
    lineas += [f"- {p}: {c} de {n}" for p, c in sorted(paradas.items())] or ["- ninguna"]
    lineas += [
        "",
        "## Reglas disparadas por sesion (ADR-0049)",
        f"sobre las {len(corridas)} sesiones corridas, y sobre las {n} con operaciones del trader:",
    ]
    lineas += [
        f"- {rid}: {disparadas_todas[rid]} de {len(corridas)}; {disparadas_trader[rid]} de {n}"
        for rid in sorted(disparadas_todas)
    ] or ["- ninguna"]
    lineas += [
        "",
        "## RN-003 al abrir la sesion (domain/sesgo.py, anotacion del motor)",
        "por sesion: " + "; ".join(f"{k} {v}" for k, v in sorted(sesgo_sesion.items())),
        "por operacion del trader: "
        + "; ".join(f"{k} {v}" for k, v in sorted(por_operacion.items())),
        "",
        "## Por sesion",
        *filas,
    ]
    return "\n".join(lineas) + "\n"


__all__ = [
    "ConjuntoError",
    "Corrida",
    "DiaTrader",
    "correr",
    "dias_de_construccion",
    "dias_de_mercado",
    "hechos_de_regla",
    "informe",
    "medida_de",
    "validar_meses",
]
