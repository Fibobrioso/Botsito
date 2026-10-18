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
from botsito.cases.criterio_fidelidad import (
    Criterio,
    Medida,
    Operacion,
    Simulacion,
    Tolerancias,
    habilita_medir,
    medir,
)
from botsito.cases.holdout import HoldoutCerradoError, casos_ocultos
from botsito.cases.ingesta import DIRECTORIO_DEV
from botsito.cases.paquete import Config
from botsito.cases.ventanas import MINUTOS_H4, MINUTOS_M15
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
from botsito.engine.primitivas import (
    ANOTACION_DOBLE_RUPTURA,
    ANOTACION_SALTADAS_COLOR,
    ANOTACION_SALTADAS_NEUTRA_DOBLE,
    ANOTACION_SALTADAS_NEUTRA_SIMPLE,
    ANOTACION_SESGO,
)
from botsito.engine.relojes import RelojSesiones

PARTICION_DEV = "dev"
_DIA = re.compile(r"(\d{4}-\d{2}-\d{2})$", re.ASCII)
A_FAVOR = frozenset({("compra", "alcista"), ("venta", "bajista")})
SIN_ANOTACION = "sin anotacion"


# ADR-0070 (enmienda del 2026-10-07): las UNICAS opciones de `motor arnes` con las que una corrida
# puede habilitar medir el conjunto de medida, porque no cambian lo que el motor decide ni como se
# llena. Lista CERRADA: cualquier otra opcion presente, conocida o futura, da «no». Unico sitio.
# Las que dicen un valor se comprueban aparte en `habilita_medir`: `--meses` solo si cubre todo
# `construccion`; `--simular` es OBLIGATORIA (sin ella, «sin simulación»), y `--perfil` y `--fase`
# solo valen si el perfil y la fase EFECTIVOS son `perfil_para_medir` y la primera de ese perfil.
OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA = frozenset(
    {"--salida", "--tracemalloc", "--meses", "--simular", "--perfil", "--fase"}
)


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
    reloj: RelojSesiones | str,
    lectura_pivote: str | None = None,
) -> dict[str, DiaDeMercado]:
    """Las H4 de cada mes y del anterior, para el calentamiento del sesgo (como MOTOR-SESGO-H4); y
    las M15 y las M1 del mismo tramo para la liquidez de M15 con la lectura de «formado» que se
    de (A-35). Sin lectura, RN-004 sigue NO_IMPLEMENTADA."""
    anclaje = registro.hora("anclaje_h4")
    if isinstance(reloj, str):  # un huso de pared: los guiones de ramas cerradas (ADR-0063 §5)
        reloj = RelojSesiones.de_pared(reloj)
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
            por_mes[mes] = DatosMercado(
                agregar(m1, MINUTOS_H4, anclaje),
                agregar(m1, MINUTOS_M15, anclaje),
                m1,
                lectura_pivote,
            )
        salida[d.dia] = DiaDeMercado(
            date.fromisoformat(d.dia), reloj.huso_visible, sesiones, por_mes[mes], reloj=reloj
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


def bloqueadas_de(traza: TrazaSesion) -> str:
    """Las acciones que un gate bloqueo en la sesion, con la regla que las pedia y el motivo
    (`Evento.bloqueadas`: regla, accion, motivo), para la linea «Por sesion» (respuesta del
    consultor a la PARADA 3 de trabajo/corrida-construccion, 2026-10-14, punto 1). Solo salida: la
    traza ya lo guardaba. `ninguna` si no hubo."""
    return ", ".join(f"{r}:{a}:{m}" for r, a, m in sorted(traza.bloqueadas)) or "ninguna"


def medida_de(corrida: Corrida, criterio: Criterio) -> Medida:
    trader = [op for d in corrida.dias for op in d.operaciones]
    bot = [op for r in corrida.resultados for op in r.operaciones]
    return medir(trader, bot, criterio.tolerancias)


def informe(
    corrida: Corrida,
    criterio: Criterio,
    vocabulario: Mapping[str, Mapping[str, Any]],
    *,
    opciones: Sequence[str],
    simulacion: Simulacion | None,
) -> str:
    """El informe de una corrida. `opciones` es obligatorio y lo da el comando: las opciones que
    la corrida uso. Cualquiera fuera de `OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA` hace que el
    veredicto de ADR-0070 sea «no», llegue o no a los umbrales."""
    medida = medida_de(corrida, criterio)
    fuera = sorted(set(opciones) - OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA)
    veredicto = habilita_medir(
        medida, criterio, corrida.meses, opciones_fuera=fuera, simulacion=simulacion
    )
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
    dobles = 0  # sesiones cuyo sesgo lo decidio el color, con doble ruptura (ADR-0060)
    # Las H4 que la busqueda salto antes de fijar el sesgo, por motivo (ADR-0080, 4.f del
    # encargo): sesiones con alguna, y velas en total. Ninguna fecha ni precio.
    saltadas: dict[str, list[int]] = {
        ANOTACION_SALTADAS_COLOR: [0, 0],
        ANOTACION_SALTADAS_NEUTRA_SIMPLE: [0, 0],
        ANOTACION_SALTADAS_NEUTRA_DOBLE: [0, 0],
    }
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
        dobles += ANOTACION_DOBLE_RUPTURA in traza.anotaciones
        for anotacion, cuenta in saltadas.items():
            if anotacion in traza.anotaciones:
                cuenta[0] += 1
                cuenta[1] += int(traza.anotaciones[anotacion])
        filas.append(
            f"{clave[0]} {clave[1]} | trader {trader_por_sesion[clave]} | bot "
            f"{bot_por_sesion[clave]} | rn003 {anotado} | {' '.join(partes)} | disparadas "
            f"{', '.join(sorted(traza.disparadas)) or 'ninguna'} | bloqueadas "
            f"{bloqueadas_de(traza)}"
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
        f"habilita medir el conjunto de medida ({', '.join(criterio.medida)}) (ADR-0070): "
        + ("sí" if veredicto.habilita else f"no ({'; '.join(veredicto.motivos)})"),
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
    # H3 (ADR-0049): dos reglas de la misma clase que dieron SI en la misma pasada. Cual disparo
    # primero lo decidio el orden por id, que no tiene semantica: la spec tiene que resolverlo.
    avisos = [
        f"- {dia} {sesion}: {clase} {', '.join(ids)}"
        for (dia, sesion) in corridas
        for clase, ids in sorted(trazas[(dia, sesion)].empates)
    ]
    lineas += [
        "",
        "## Avisos de orden dentro de una clase (ADR-0049, H3)",
        *(
            avisos
            or ["- ninguno: en ninguna sesion dieron SI dos reglas de la misma clase a la vez"]
        ),
        "",
        "## RN-003 al abrir la sesion (domain/sesgo.py, anotacion del motor)",
        "por sesion: " + "; ".join(f"{k} {v}" for k, v in sorted(sesgo_sesion.items())),
        f"de ellas con doble ruptura, que decide el color de la vela (ADR-0060): {dobles}",
        "sesiones con alguna H4 saltada por color contrario (rompio un extremo y cerro del color "
        f"contrario, ADR-0080 D1): {saltadas[ANOTACION_SALTADAS_COLOR][0]} "
        f"({saltadas[ANOTACION_SALTADAS_COLOR][1]} velas)",
        "sesiones con alguna H4 saltada por neutra simple (rompio un extremo y cerro sin cuerpo, "
        f"ADR-0080 D3): {saltadas[ANOTACION_SALTADAS_NEUTRA_SIMPLE][0]} "
        f"({saltadas[ANOTACION_SALTADAS_NEUTRA_SIMPLE][1]} velas)",
        "sesiones con alguna H4 saltada por neutra con doble ruptura (ADR-0075): "
        f"{saltadas[ANOTACION_SALTADAS_NEUTRA_DOBLE][0]} "
        f"({saltadas[ANOTACION_SALTADAS_NEUTRA_DOBLE][1]} velas)",
        "por operacion del trader: "
        + "; ".join(f"{k} {v}" for k, v in sorted(por_operacion.items())),
        "",
        "## Por sesion",
        *filas,
        "",
        *diferencias_por_operacion(corrida, criterio, vocabulario, medida=medida),
    ]
    return "\n".join(lineas) + "\n"


# ------------------------------------------------- diferencias por operacion (R3.1, ADR-0043)
#
# La ultima seccion del informe (rama `trabajo/corrida-construccion`, 2026-10-14): una fila por
# operacion del trader -emparejada o no, y si no, la del bot mas cercana en su sesion y el primer
# hecho del embudo que falto- y una por operacion del bot sin pareja, para que el consultor
# clasifique cada diferencia. Se construye sobre el MISMO emparejamiento del criterio
# (`cases/criterio_fidelidad.medir`), sin repetirlo: la `Medida` global se parte por mes, y la
# particion es identica a medir cada mes aparte porque una pareja exige el mismo dia y el voraz
# solo compite dentro de un dia. No anade ninguna opcion al comando (ADR-0070: la lista cerrada no
# cambia). Determinista: por mes en el orden de `construccion`, por dia y por instante.

PAREJA = "PAREJA"
SIN_PAREJA = "SIN PAREJA"
TODOS_LOS_HECHOS = "todos los hechos del camino producidos"
SIN_PRODUCTORA_PARADA = "productoras sin cumplirse"
# Los hechos de origen `regla` que son FRENOS (un tope, el limite total, los cartuchos, la racha)
# solo se producen cuando algo para al bot: no son el camino hacia la operacion (sesgo,
# orden_dimensionada, liquidez_tomada). El ultimo campo de la tabla mira el camino y nombra un
# freno solo si se produjo (respuesta del consultor a la PARADA 2, 2026-10-14, punto 1.a).
PREFIJO_FRENO = "detenido_por_"


def _meses_en_orden(criterio: Criterio, corrida: Corrida) -> tuple[str, ...]:
    """Los meses de la corrida en el orden de `construccion`; uno que no este alli (no pasa por
    `validar_meses`, pero una corrida sintetica puede traerlo) va al final, por fecha."""
    en_construccion = [m for m in criterio.construccion if m in corrida.meses]
    resto = sorted(set(corrida.meses) - set(criterio.construccion))
    return tuple(en_construccion + resto)


def _delta_con_signo(desde: Operacion, hasta: Operacion, tol: Tolerancias) -> tuple[int, Decimal]:
    """(Δinstante en segundos, Δentrada en puntos), `hasta` menos `desde`, con signo."""
    segundos = int((hasta.instante - desde.instante).total_seconds())
    puntos = (hasta.entrada - desde.entrada) * tol.escala
    return segundos, puntos


def _puntos(d: Decimal) -> str:
    entero = d.to_integral_value()
    if d == entero:
        return f"{int(entero):+d}"
    return f"{d.normalize():+f}"


def _segundos(s: int) -> str:
    signo = "-" if s < 0 else "+"
    return f"{signo}{abs(s) // 60} min {abs(s) % 60} s"


def _fmt_delta(segundos: int, puntos: Decimal) -> str:
    return f"Δentrada {_puntos(puntos)} puntos, Δinstante {_segundos(segundos)}"


def _mas_cercana(
    op: Operacion, candidatas: Sequence[Operacion], tol: Tolerancias
) -> Operacion | None:
    """La mas cercana a `op` en su misma sesion, con el orden del criterio (menor |Δinstante|,
    luego menor |Δentrada|, luego la mas temprana) y SIN exigir el lado: para clasificar, una
    operacion del otro lado a la misma hora es un dato."""
    misma_sesion = [c for c in candidatas if (c.dia, c.sesion) == (op.dia, op.sesion)]
    if not misma_sesion:
        return None

    def clave(c: Operacion) -> tuple[int, Decimal, datetime]:
        segundos, puntos = _delta_con_signo(op, c, tol)
        return abs(segundos), abs(puntos), c.instante

    return min(misma_sesion, key=clave)


def primer_hecho_que_falta(traza: TrazaSesion, hechos: Sequence[tuple[str, list[str]]]) -> str:
    """El primer hecho DEL CAMINO (origen `regla`, sin los frenos `detenido_por_*`), en el orden
    de la spec, que la sesion no produjo, con las primitivas NO_IMPLEMENTADA en que se pararon sus
    productoras (como «Por sesion»); si se produjeron todos, lo dice. Los frenos se nombran aparte
    SOLO si se produjeron: uno que no se produjo no es un hecho que falto."""
    producidos = traza.hechos_producidos
    texto = TODOS_LOS_HECHOS
    for hecho, productoras in hechos:
        if hecho.startswith(PREFIJO_FRENO) or hecho in producidos:
            continue
        prim = sorted({p for r, p in traza.no_implementadas if r in productoras})
        texto = f"{hecho}[{', '.join(prim) if prim else SIN_PRODUCTORA_PARADA}]"
        break
    frenos = [h for h, _ in hechos if h.startswith(PREFIJO_FRENO) and h in producidos]
    if frenos:
        texto += f"; frenos producidos: {', '.join(frenos)}"
    return texto


def _fila(quien: str, op: Operacion, resultado: str) -> str:
    return (
        f"{quien} | {op.dia} | {op.sesion} | {op.direccion} | {op.instante.isoformat()} | "
        f"{op.entrada} | {resultado}"
    )


def diferencias_por_operacion(
    corrida: Corrida,
    criterio: Criterio,
    vocabulario: Mapping[str, Mapping[str, Any]],
    *,
    medida: Medida | None = None,
) -> list[str]:
    """Las lineas de la seccion «## Diferencias por operacion». `medida` es la del informe si ya
    esta calculada; si no, se calcula igual (`medida_de`)."""
    tol = criterio.tolerancias
    if medida is None:
        medida = medida_de(corrida, criterio)
    hechos = hechos_de_regla(vocabulario)
    trazas: dict[tuple[str, str], TrazaSesion] = {
        (r.dia, s): t for r in corrida.resultados for s, t in r.sesiones.items()
    }
    trader_por_dia: dict[str, list[Operacion]] = {}
    for d in corrida.dias:
        trader_por_dia.setdefault(d.dia, []).extend(d.operaciones)
    bot_por_dia: dict[str, list[Operacion]] = {}
    for r in corrida.resultados:
        bot_por_dia.setdefault(r.dia, []).extend(r.operaciones)
    # la pareja de cada operacion, por identidad: `medir` devuelve los MISMOS objetos que recibe
    pareja_del_trader = {id(p.trader): p for p in medida.parejas}
    pareja_del_bot = {id(p.bot): p for p in medida.parejas}
    dias_con_trader = {dia for dia, ops in trader_por_dia.items() if ops}
    meses = _meses_en_orden(criterio, corrida)
    dias_por_mes: dict[str, list[str]] = {m: [] for m in meses}
    for d in corrida.dias:
        dias_por_mes.setdefault(d.dia[:7], []).append(d.dia)
    for mes in dias_por_mes:
        dias_por_mes[mes] = sorted(set(dias_por_mes[mes]))

    lineas = [
        f"## Diferencias por operacion (ADR-0043: {tol.entrada_puntos} puntos, "
        f"{tol.instante_min} min)",
        "### Resumen por mes (en el orden de construccion)",
        "mes | dias | trader | bot puntuables | bot en dias sin trader | parejas | cobertura | "
        "precision",
    ]
    for mes in meses:
        dias = dias_por_mes.get(mes, [])
        n_trader = sum(len(trader_por_dia.get(d, [])) for d in dias)
        n_punt = sum(len(bot_por_dia.get(d, [])) for d in dias if d in dias_con_trader)
        n_fuera = sum(len(bot_por_dia.get(d, [])) for d in dias if d not in dias_con_trader)
        n_parejas = sum(1 for p in medida.parejas if p.trader.dia[:7] == mes)
        cobertura = _fraccion(
            Fraction(n_parejas, n_trader) if n_trader else None, n_parejas, n_trader,
            "cero del trader",
        )  # fmt: skip
        precision = _fraccion(
            Fraction(n_parejas, n_punt) if n_punt else None, n_parejas, n_punt,
            "cero operaciones del bot puntuables",
        )  # fmt: skip
        lineas.append(
            f"{mes} | {len(dias)} | {n_trader} | {n_punt} | {n_fuera} | {n_parejas} | "
            f"{cobertura} | {precision}"
        )

    lineas += [
        "### Embudo por mes: primer hecho del camino que falta en las sesiones con operaciones "
        "del trader y sin operacion del bot (los frenos detenido_por_*, solo si se produjeron)",
        "mes | hecho[primitivas NO_IMPLEMENTADA] | sesiones",
    ]
    for mes in meses:
        paradas: Counter[str] = Counter()
        con_trader = 0
        for dia in dias_por_mes.get(mes, []):
            sesiones_trader = {op.sesion for op in trader_por_dia.get(dia, [])}
            sesiones_bot = {op.sesion for op in bot_por_dia.get(dia, [])}
            con_trader += len(sesiones_trader)
            for sesion in sorted(sesiones_trader - sesiones_bot):
                traza = trazas.get((dia, sesion), TrazaSesion())
                paradas[primer_hecho_que_falta(traza, hechos)] += 1
        lineas.append(
            f"{mes} | sesiones con operaciones del trader {con_trader}; sin operacion del bot "
            f"{sum(paradas.values())}"
        )
        por_frecuencia = sorted(paradas.items(), key=lambda kv: (-kv[1], kv[0]))
        lineas += [f"{mes} | {h} | {n}" for h, n in por_frecuencia]

    lineas += [
        "### Por operacion (por mes de construccion y por dia; en cada dia, el trader primero y "
        "despues el bot sin pareja)",
        "quien | dia | sesion | lado | instante UTC | entrada | resultado",
    ]
    for mes in meses:
        for dia in dias_por_mes.get(mes, []):
            trader = sorted(trader_por_dia.get(dia, []), key=lambda o: (o.instante, o.entrada))
            bot = sorted(bot_por_dia.get(dia, []), key=lambda o: (o.instante, o.entrada))
            for op in trader:
                pareja = pareja_del_trader.get(id(op))
                if pareja is not None:
                    segundos, puntos = _delta_con_signo(op, pareja.bot, tol)
                    resultado = (
                        f"{PAREJA} bot {pareja.bot.instante.isoformat()} {pareja.bot.entrada} "
                        f"({_fmt_delta(segundos, puntos)})"
                    )
                else:
                    cercana = _mas_cercana(op, bot, tol)
                    if cercana is None:
                        resultado = f"{SIN_PAREJA}; ninguna operacion del bot en la sesion"
                    else:
                        segundos, puntos = _delta_con_signo(op, cercana, tol)
                        resultado = (
                            f"{SIN_PAREJA}; bot mas cercano en la sesion: {cercana.direccion} "
                            f"{cercana.instante.isoformat()} {cercana.entrada} "
                            f"({_fmt_delta(segundos, puntos)})"
                        )
                    traza = trazas.get((dia, op.sesion), TrazaSesion())
                    resultado += (
                        f"; primer hecho que falto: {primer_hecho_que_falta(traza, hechos)}"
                    )
                lineas.append(_fila("trader", op, resultado))
            for op in bot:
                if id(op) in pareja_del_bot:
                    continue
                if dia not in dias_con_trader:
                    resultado = f"{SIN_PAREJA}; ninguna operacion del trader en el dia"
                else:
                    cercana = _mas_cercana(op, trader, tol)
                    if cercana is None:
                        resultado = f"{SIN_PAREJA}; ninguna operacion del trader en la sesion"
                    else:
                        segundos, puntos = _delta_con_signo(op, cercana, tol)
                        resultado = (
                            f"{SIN_PAREJA}; trader mas cercano en la sesion: {cercana.direccion} "
                            f"{cercana.instante.isoformat()} {cercana.entrada} "
                            f"({_fmt_delta(segundos, puntos)})"
                        )
                lineas.append(_fila("bot", op, resultado))
    return lineas


__all__ = [
    "OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA",
    "ConjuntoError",
    "Corrida",
    "DiaTrader",
    "bloqueadas_de",
    "correr",
    "dias_de_construccion",
    "dias_de_mercado",
    "diferencias_por_operacion",
    "hechos_de_regla",
    "informe",
    "medida_de",
    "primer_hecho_que_falta",
    "validar_meses",
]
