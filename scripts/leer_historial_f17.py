"""Lee el historial de ticks que exporta `tools/mql5/ExportarTicksFTMO.mq5` desde la demo de FTMO y
dice, por mes de construccion, si CUBRE segun el criterio pre-registrado de
`docs/plan/F17-HISTORIAL.yaml` (ADR-0099 §5; rama `trabajo/f17-historial`).

SOLO LEE y SOLO MESES DE CONSTRUCCION: decide por el NOMBRE de cada CSV, antes de abrirlo, y se
niega (sale con 2) a cualquier fichero de un dia que no sea de `construccion` de
`criterio_fidelidad.yaml`. Imprime recuentos, fracciones, puntos de spread y percentiles; ningun
precio.

**El reloj del servidor.** Los instantes del CSV van en el reloj del servidor (que lo vayan es lo
que el control confirma; la documentacion de MQL5 no lo dice, ADR-0082 D7). Pasan a UTC con
`broker_offset_base` y `broker_dst` del registro: el servidor va `broker_offset_base` minutos por
delante de UTC, mas el horario de verano del calendario de `broker_dst`, que sale de zoneinfo (el
`dst()` del huso de ese calendario), sin ninguna cifra aqui. Un instante del servidor que caiga en
la hora repetida o en la que se salta en un cambio de hora (domingos, con el mercado cerrado) no se
adivina: falla nombrandolo.

**Los dias, la ventana y los puntos (a) a (d2)**, como los define el yaml: los laborables del mes
menos los dias con un cierre del calendario de FTMO que toque la ventana; la ventana, los minutos
de cada dia de `ventana_inicio` a `ventana_fin` por `reloj_de_las_sesiones`; y, solo para los meses
que cubren, el spread por hora y la diferencia mediana con Dukascopy, como diagnostico.

    uv run python scripts/leer_historial_f17.py <carpeta> --salida <fichero>
    uv run python scripts/leer_historial_f17.py --control-dukascopy --salida <fichero>

La segunda forma es el control del punto 2 de la respuesta a la PARADA: (d1) sobre los ticks de
Dukascopy de los meses de construccion, que tienen que pasarlo todos.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import defaultdict
from collections.abc import Iterable, Mapping, Sequence
from collections.abc import Set as AbstractSet
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[1]
CRITERIO = Path("docs") / "plan" / "F17-HISTORIAL.yaml"
PERFIL = "ftmo-2step-swing-100k"
MS_POR_MINUTO = 60_000
MINUTOS_POR_HORA = 60
# El calendario de cambio de hora de cada opcion de `broker_dst`, por el nombre de un huso que lo
# sigue: es una tabla de nombres, no de cifras (el `dst()` de zoneinfo da cuanto se adelanta).
HUSO_DEL_CALENDARIO: Mapping[str, str | None] = {
    "us": "America/New_York",
    "eu": "Europe/London",
    "ninguno": None,
}
LABORABLES = frozenset({0, 1, 2, 3, 4})  # lunes a viernes, `date.weekday()`
COLUMNAS_TICKS = ("time_msc", "bid", "ask", "flags")
COLUMNAS_M1 = ("time", "open", "high", "low", "close", "tick_volume", "spread", "real_volume")
COLUMNAS_CONTROL = ("clave", "valor", "nota")
PATRON_TICKS = re.compile(r"^F17_(\d{4}-\d{2})-\d{2}_ticks\.csv$")
PATRON_M1 = re.compile(r"^F17_(\d{4}-\d{2})-\d{2}_m1\.csv$")
PATRON_CONTROL = re.compile(r"^F17_control_\d{8}_\d{6}\.csv$")


class HistorialError(ValueError):
    """Algo que impide leer o decidir: el mensaje dice que, y no se adivina."""


# --------------------------------------------------------------------- el reloj del servidor


@dataclass(frozen=True)
class RelojServidor:
    """El reloj del servidor: `base` minutos por delante de UTC mas el horario de verano de `huso`
    (ninguno si `huso` es None)."""

    base_minutos: int
    huso: str | None

    @classmethod
    def del_registro(cls, registro: Any) -> RelojServidor:
        opcion = registro.opcion("broker_dst")
        if opcion not in HUSO_DEL_CALENDARIO:
            raise HistorialError(f"broker_dst = {opcion!r}: no es un calendario conocido")
        return cls(registro.minutos("broker_offset_base"), HUSO_DEL_CALENDARIO[opcion])

    def verano_minutos(self, utc_ms: int) -> int:
        """Cuantos minutos adelanta el horario de verano en el instante UTC `utc_ms`."""
        if self.huso is None:
            return 0
        local = datetime.fromtimestamp(utc_ms / 1000, tz=UTC).astimezone(ZoneInfo(self.huso))
        dst = local.dst()
        return 0 if dst is None else int(dst.total_seconds()) // 60

    def desfase_minutos(self, utc_ms: int) -> int:
        """Minutos que el servidor va por delante de UTC en `utc_ms`."""
        return self.base_minutos + self.verano_minutos(utc_ms)

    def a_servidor(self, utc_ms: int) -> int:
        return utc_ms + self.desfase_minutos(utc_ms) * MS_POR_MINUTO

    def a_utc(self, servidor_ms: int) -> int:
        """El instante UTC que el servidor marca como `servidor_ms`. Prueba los candidatos que da
        cada horario de verano posible y exige uno solo: dos es la hora repetida, ninguno la que se
        salta."""
        base = servidor_ms - self.base_minutos * MS_POR_MINUTO
        # los horarios de verano posibles cerca del instante: un cambio de hora no cae dos veces en
        # dos dias, asi que el de la vispera, el del dia y el del siguiente los dan todos
        dia = int(timedelta(days=1).total_seconds() * 1000)
        valores = {0, *(self.verano_minutos(base + k * dia) for k in (-1, 0, 1))}
        candidatos = {base - v * MS_POR_MINUTO for v in valores}
        validos = sorted(u for u in candidatos if self.a_servidor(u) == servidor_ms)
        if len(validos) != 1:
            hora = datetime.fromtimestamp(servidor_ms / 1000, tz=UTC).strftime("%Y-%m-%d %H:%M")
            que = "se repite" if validos else "no existe"
            raise HistorialError(
                f"el instante del servidor {hora} {que} en un cambio de hora: no se adivina"
            )
        return validos[0]


# ----------------------------------------------------------------------------- los dias


@dataclass(frozen=True)
class DiaVentana:
    dia: date
    desde: int  # minuto UTC, incluido
    hasta: int  # minuto UTC, excluido

    def minutos(self) -> range:
        return range(self.desde, self.hasta)


def _dias_del_mes(mes: str) -> list[date]:
    anio, m = int(mes[:4]), int(mes[5:])
    d = date(anio, m, 1)
    salida = []
    while d.month == m:
        salida.append(d)
        d += timedelta(days=1)
    return salida


def dias_del_mes(
    mes: str,
    reloj_sesiones: Any,
    inicio: str,
    fin: str,
    cierres: Sequence[tuple[int, int]],
    cubre: tuple[int, int],
) -> list[DiaVentana]:
    """Los laborables de `mes` menos los que tienen un cierre (`[inicio_ms, fin_ms)`) que toca su
    ventana. `cubre` es el tramo `[desde_ms, hasta_ms)` que el calendario conoce: un dia fuera, para
    (punto 0 de la respuesta a la PARADA)."""
    salida: list[DiaVentana] = []
    for d in _dias_del_mes(mes):
        if d.weekday() not in LABORABLES:
            continue
        desde = int(reloj_sesiones.instante(d, inicio))
        hasta = int(reloj_sesiones.instante(d, fin))
        a, b = desde * MS_POR_MINUTO, hasta * MS_POR_MINUTO
        if not (cubre[0] <= a and b <= cubre[1]):
            raise HistorialError(
                f"{d}: el calendario de cierres no cubre su ventana; no se adivina"
            )
        if any(ci < b and a < cf for ci, cf in cierres):
            continue
        salida.append(DiaVentana(d, desde, hasta))
    return salida


# ------------------------------------------------------------------------------- medidas


def percentil(valores: Sequence[int], p: float) -> int:
    """Percentil por rango mas cercano sobre la lista ORDENADA (el de `scripts/ticks_spread.py`)."""
    if not valores:
        raise HistorialError("sin valores")
    i = max(0, min(len(valores) - 1, round(p * (len(valores) - 1))))
    return valores[i]


def mediana(valores: Iterable[int]) -> int:
    return percentil(sorted(valores), 0.5)


@dataclass(frozen=True)
class Ohlc:
    abierta: int
    maxima: int
    minima: int
    cierre: int


@dataclass
class TicksDelMes:
    """Los ticks de un mes por minuto UTC: cuantos, sus spreads y la M1 BID rehecha."""

    por_minuto: dict[int, int] = field(default_factory=lambda: defaultdict(int))
    spreads: dict[int, list[int]] = field(default_factory=lambda: defaultdict(list))
    m1: dict[int, Ohlc] = field(default_factory=dict)

    def anadir(self, utc_ms: int, bid: int, ask: int) -> None:
        minuto = utc_ms // MS_POR_MINUTO
        self.por_minuto[minuto] += 1
        self.spreads[minuto].append(ask - bid)
        o = self.m1.get(minuto)
        self.m1[minuto] = (
            Ohlc(bid, bid, bid, bid)
            if o is None
            else Ohlc(o.abierta, max(o.maxima, bid), min(o.minima, bid), bid)
        )


@dataclass(frozen=True)
class Criterio:
    a_minimo: Fraction
    b_umbral: int
    b_maximo: int
    b_hueco_maximo: int
    c_tolerancia: int
    c_minimo: Fraction
    d1_valores: int
    d1_minimo: Fraction
    d2_fraccion: Fraction


def cargar_criterio_f17(raiz: Path) -> Criterio:
    from botsito.comun.yaml_estricto import leer_yaml

    c = leer_yaml(raiz / CRITERIO)["cubre_si"]
    return Criterio(
        Fraction(c["a_minutos_con_tick"]["minimo"]),
        int(c["b_huecos"]["umbral_minutos"]),
        int(c["b_huecos"]["maximo_huecos_por_mes"]),
        int(c["b_huecos"]["hueco_maximo_minutos"]),
        int(c["c_m1_propia"]["tolerancia_puntos"]),
        Fraction(c["c_m1_propia"]["minimo"]),
        int(c["d1_spread_variable"]["valores_distintos_minimo"]),
        Fraction(c["d1_spread_variable"]["minimo"]),
        Fraction(c["d2_ticks_por_minuto"]["fraccion_de_dukascopy_minima"]),
    )


def huecos(dias: Sequence[DiaVentana], ticks: TicksDelMes) -> list[int]:
    """La longitud de cada racha de minutos seguidos sin ticks dentro de la ventana de un dia."""
    salida = []
    for d in dias:
        racha = 0
        for minuto in d.minutos():
            if ticks.por_minuto.get(minuto, 0) == 0:
                racha += 1
            else:
                if racha:
                    salida.append(racha)
                racha = 0
        if racha:
            salida.append(racha)
    return salida


def horas_dia(dias: Sequence[DiaVentana], reloj_sesiones: Any) -> dict[tuple[date, int], list[int]]:
    """Los minutos de la ventana de cada par (dia, hora nominal)."""
    salida: dict[tuple[date, int], list[int]] = defaultdict(list)
    for d in dias:
        for minuto in d.minutos():
            _, nominal = reloj_sesiones.lectura(minuto)
            salida[(d.dia, nominal // MINUTOS_POR_HORA)].append(minuto)
    return salida


@dataclass(frozen=True)
class Puntos:
    minutos: int
    con_tick: int
    huecos_largos: int
    hueco_maximo: int
    m1_con_tick: int
    m1_cuadran: int
    horas_con_tick: int
    horas_spread_variable: int
    mediana_ticks_minuto: int  # la de FTMO sobre los minutos de d2
    mediana_ticks_minuto_dukascopy: int | None
    minutos_d2: int = 0  # los de las horas que Dukascopy tiene descargadas (PARADA 2, punto 0)

    def cumple(self, c: Criterio) -> dict[str, bool]:
        return {
            "a": self.minutos > 0 and Fraction(self.con_tick, self.minutos) >= c.a_minimo,
            "b": self.huecos_largos <= c.b_maximo and self.hueco_maximo <= c.b_hueco_maximo,
            "c": self.m1_con_tick > 0 and Fraction(self.m1_cuadran, self.m1_con_tick) >= c.c_minimo,
            "d1": self.horas_con_tick > 0
            and Fraction(self.horas_spread_variable, self.horas_con_tick) >= c.d1_minimo,
            "d2": self.minutos_d2 > 0
            and self.mediana_ticks_minuto_dukascopy is not None
            and Fraction(self.mediana_ticks_minuto)
            >= c.d2_fraccion * self.mediana_ticks_minuto_dukascopy,
        }


def d1(
    dias: Sequence[DiaVentana], ticks: TicksDelMes, reloj_sesiones: Any, c: Criterio
) -> tuple[int, int]:
    """(horas dia-hora con algun tick, de ellas con al menos `d1_valores` spreads distintos)."""
    con, variables = 0, 0
    for minutos in horas_dia(dias, reloj_sesiones).values():
        valores = {s for m in minutos for s in ticks.spreads.get(m, ())}
        if any(ticks.por_minuto.get(m, 0) for m in minutos):
            con += 1
            variables += len(valores) >= c.d1_valores
    return con, variables


def hora_utc(minuto: int) -> tuple[date, int]:
    """El dia y la hora UTC de un minuto UTC."""
    t = datetime.fromtimestamp(minuto * MS_POR_MINUTO / 1000, tz=UTC)
    return t.date(), t.hour


def horas_descargadas(
    dias: Iterable[str], horas_utc: Iterable[int], perdidas: Iterable[str]
) -> frozenset[tuple[date, int]]:
    """Las horas que un dataset de ticks de Dukascopy tiene descargadas, de su manifiesto:
    `seleccion.dias` por `seleccion.horas_utc`, menos `horas.perdidas` (`AAAA-MM-DDTHHZ`)."""
    fuera = {(date.fromisoformat(p[:10]), int(p[11:13])) for p in perdidas}
    horas = list(horas_utc)
    return frozenset(
        (date.fromisoformat(d), h)
        for d in dias
        for h in horas
        if (date.fromisoformat(d), h) not in fuera
    )


def puntos_del_mes(
    dias: Sequence[DiaVentana],
    ticks: TicksDelMes,
    m1_servidor: Mapping[int, Ohlc],
    reloj_sesiones: Any,
    c: Criterio,
    dukascopy: TicksDelMes | None,
    horas_dukascopy: AbstractSet[tuple[date, int]] = frozenset(),
) -> Puntos:
    """Los puntos (a) a (d2) del mes. (a), (b), (c) y (d1), sobre todos los minutos de la ventana de
    `dias`; (d2), solo sobre los de las horas que Dukascopy tiene descargadas (`horas_dukascopy`,
    respuesta a la PARADA 2, punto 0), donde un minuto sin ticks cuenta 0 en cada fuente."""
    minutos = [m for d in dias for m in d.minutos()]
    con_tick = [m for m in minutos if ticks.por_minuto.get(m, 0)]
    largos = [h for h in huecos(dias, ticks) if h > c.b_umbral]
    todos = huecos(dias, ticks)
    cuadran = 0
    for m in con_tick:
        s, t = m1_servidor.get(m), ticks.m1[m]
        if (
            s is not None
            and max(
                abs(s.abierta - t.abierta),
                abs(s.maxima - t.maxima),
                abs(s.minima - t.minima),
                abs(s.cierre - t.cierre),
            )
            <= c.c_tolerancia
        ):
            cuadran += 1
    horas, variables = d1(dias, ticks, reloj_sesiones, c)
    de_d2 = [m for m in minutos if hora_utc(m) in horas_dukascopy]
    duk = None
    if dukascopy is not None and de_d2:
        duk = mediana(dukascopy.por_minuto.get(m, 0) for m in de_d2)
    return Puntos(
        minutos=len(minutos),
        con_tick=len(con_tick),
        huecos_largos=len(largos),
        hueco_maximo=max(todos, default=0),
        m1_con_tick=len(con_tick),
        m1_cuadran=cuadran,
        horas_con_tick=horas,
        horas_spread_variable=variables,
        mediana_ticks_minuto=mediana(ticks.por_minuto.get(m, 0) for m in de_d2) if de_d2 else 0,
        mediana_ticks_minuto_dukascopy=duk,
        minutos_d2=len(de_d2),
    )


def diferencias_de_spread(
    dias: Sequence[DiaVentana], ftmo: TicksDelMes, duk: TicksDelMes, reloj_sesiones: Any
) -> tuple[int | None, int | None]:
    """(la diferencia mediana, la de las medianas globales): por cada par dia-hora con ticks de
    las dos fuentes, mediana de FTMO menos mediana de Dukascopy, y la mediana de esas; al lado, la
    mediana de todos los spreads de FTMO menos la de todos los de Dukascopy (`solo_si_cubre`)."""
    difs: list[int] = []
    todos_f: list[int] = []
    todos_d: list[int] = []
    for minutos in horas_dia(dias, reloj_sesiones).values():
        f = [s for m in minutos for s in ftmo.spreads.get(m, ())]
        d = [s for m in minutos for s in duk.spreads.get(m, ())]
        todos_f += f
        todos_d += d
        if f and d:
            difs.append(mediana(f) - mediana(d))
    diferencia = mediana(difs) if difs else None
    global_ = mediana(todos_f) - mediana(todos_d) if todos_f and todos_d else None
    return diferencia, global_


# --------------------------------------------------------------------------- los ficheros


def mes_de_fichero(nombre: str) -> str | None:
    """El AAAA-MM de un CSV de ticks o de M1 por su nombre; None si no es de esos."""
    for patron in (PATRON_TICKS, PATRON_M1):
        m = patron.match(nombre)
        if m:
            return m.group(1)
    return None


def comprobar_meses(nombres: Iterable[str], construccion: Sequence[str]) -> list[str]:
    """Los ficheros cuyo dia no es de construccion. Decide por el NOMBRE, sin abrir nada."""
    malos = []
    for n in nombres:
        mes = mes_de_fichero(n)
        if (mes is None and not PATRON_CONTROL.match(n)) or (
            mes is not None and mes not in construccion
        ):
            malos.append(n)
    return malos


def _filas(ruta: Path, columnas: Sequence[str]) -> list[dict[str, str]]:
    # el CSV de MQL5 sale en ANSI y con CRLF (FILE_ANSI; H10 del auditor): se acepta tal cual
    texto = ruta.read_bytes().decode("cp1252")
    lector = csv.DictReader(texto.splitlines())
    if tuple(lector.fieldnames or ()) != tuple(columnas):
        raise HistorialError(f"{ruta.name}: columnas {lector.fieldnames}, se esperaban {columnas}")
    return list(lector)


def a_puntos(texto: str, digitos: int) -> int:
    """Un precio con `digitos` decimales, en puntos, exacto."""
    valor = Decimal(texto).scaleb(digitos)
    if valor != valor.to_integral_value():
        raise HistorialError(f"precio {texto!r} con mas de {digitos} decimales")
    return int(valor)


def leer_control(ruta: Path) -> dict[str, str]:
    return {f["clave"]: f["valor"] for f in _filas(ruta, COLUMNAS_CONTROL)}


def leer_ticks(ruta: Path, reloj: RelojServidor, digitos: int, destino: TicksDelMes) -> int:
    n = 0
    for f in _filas(ruta, COLUMNAS_TICKS):
        destino.anadir(
            reloj.a_utc(int(f["time_msc"])),
            a_puntos(f["bid"], digitos),
            a_puntos(f["ask"], digitos),
        )
        n += 1
    return n


def leer_m1(ruta: Path, reloj: RelojServidor, digitos: int) -> dict[int, Ohlc]:
    salida = {}
    for f in _filas(ruta, COLUMNAS_M1):
        utc = reloj.a_utc(int(f["time"]) * 1000)
        salida[utc // MS_POR_MINUTO] = Ohlc(
            a_puntos(f["open"], digitos),
            a_puntos(f["high"], digitos),
            a_puntos(f["low"], digitos),
            a_puntos(f["close"], digitos),
        )
    return salida


def control_cuadra(control: Mapping[str, str], reloj: RelojServidor) -> tuple[int, int]:
    """(desfase servidor - GMT del CSV, el que da el registro en ese instante), en minutos. El
    instante es `time_gmt_s` del control, en segundos UTC; el desfase del CSV, su fila."""
    gmt_s = int(control["time_gmt_s"])
    return int(control["desfase_servidor_gmt_min"]), reloj.desfase_minutos(gmt_s * 1000)


def control_cuadra_con_registro(control: Mapping[str, str], reloj: RelojServidor) -> bool:
    """Si el desfase servidor - GMT del control es el que da el registro en su instante."""
    csv_d, reg_d = control_cuadra(control, reloj)
    return csv_d == reg_d


def dias_incompletos(control: Mapping[str, str]) -> list[str]:
    """Los dias del control sin ticks o con un error al pedirlos (`dia_<AAAA-MM-DD>_ticks` de 0 o
    menos, o `dia_<AAAA-MM-DD>_error` distinto de 0), para que un mes que no cubre diga por que
    (revisor de trabajo/f17-historial, b5; `ERR_HISTORY_TIMEOUT` deja un dia a medias)."""
    salida = []
    for clave, valor in control.items():
        m = re.fullmatch(r"dia_(\d{4}-\d{2}-\d{2})_ticks", clave)
        if m is None:
            continue
        error = control.get(f"dia_{m.group(1)}_error", "0")
        if int(valor) <= 0 or int(error) != 0:
            salida.append(f"{m.group(1)} (ticks {valor}, error {error})")
    return sorted(salida)


# ----------------------------------------------------------------------- el manifiesto (D4)

ESQUEMA_MANIFIESTO = "schema_f17_historial"
TIPOS_DE_FICHERO = frozenset({"ticks", "m1", "control"})
CAMPOS_MANIFIESTO = (
    ESQUEMA_MANIFIESTO,
    "dataset_id",
    "mes",
    "ficheros",
    "dias",
    "primer_tick_msc_servidor",
    "primera_m1_servidor_s",
    "control",
    "script",
    "cuenta",
    "declarado_por",
    "congelado_el",
    "rama",
    "informe",
)
PATRON_DATASET = re.compile(r"^f17-historial-(\d{4}-\d{2})-([0-9a-f]{8})$")


def sufijo_de(ficheros: Sequence[Mapping[str, Any]]) -> str:
    """Los 8 primeros del sha256 de los sha256 de los ficheros, ordenados por su ruta."""
    import hashlib

    unidos = "".join(f["sha256"] for f in sorted(ficheros, key=lambda f: str(f["ruta"])))
    return hashlib.sha256(unidos.encode("ascii")).hexdigest()[:8]


def validar_manifiesto(doc: Mapping[str, Any], construccion: Sequence[str]) -> list[str]:
    """Lo que no cumple el esquema `schema_f17_historial: 1` de `data/manifests/README.md`."""
    salida = [f"falta {c}" for c in CAMPOS_MANIFIESTO if c not in doc]
    if salida:
        return salida
    salida += [f"campo de mas: {c}" for c in doc if c not in CAMPOS_MANIFIESTO]
    if doc[ESQUEMA_MANIFIESTO] != 1:
        salida.append(f"{ESQUEMA_MANIFIESTO} no es 1")
    mes = str(doc["mes"])
    if mes not in construccion:
        salida.append(f"el mes {mes} no es de construccion")
    ficheros = doc["ficheros"]
    tipos = set()
    for f in ficheros:
        if f.get("tipo") not in TIPOS_DE_FICHERO:
            salida.append(f"{f.get('ruta')}: tipo {f.get('tipo')!r}")
        tipos.add(f.get("tipo"))
        if not re.fullmatch(r"[0-9a-f]{64}", str(f.get("sha256", ""))):
            salida.append(f"{f.get('ruta')}: sha256 mal formado")
        for c in ("ruta", "bytes", "filas", "fin_de_linea"):
            if c not in f:
                salida.append(f"{f.get('ruta')}: falta {c}")
        if f.get("tipo") in ("ticks", "m1") and mes_de_fichero(Path(str(f["ruta"])).name) != mes:
            salida.append(f"{f.get('ruta')}: no es del mes {mes}")
    if tipos != TIPOS_DE_FICHERO:
        salida.append(f"faltan ficheros de tipo {sorted(TIPOS_DE_FICHERO - tipos)}")
    m = PATRON_DATASET.match(str(doc["dataset_id"]))
    if m is None:
        salida.append("dataset_id mal formado")
    else:
        if m.group(1) != mes:
            salida.append("el dataset_id no es del mes")
        if not salida and m.group(2) != sufijo_de(ficheros):
            salida.append("el sufijo del dataset_id no es el de sus ficheros")
    for c in ("time_trade_server_s", "time_gmt_s", "desfase_servidor_gmt_min", "cuadra"):
        if c not in doc["control"]:
            salida.append(f"control: falta {c}")
    return salida


# ------------------------------------------------------------------------------- la salida


def _fr(a: int, b: int) -> str:
    return f"{a}/{b} ({(100 * a / b) if b else 0:.2f} %)"


def lineas_del_mes(mes: str, dias: int, p: Puntos, c: Criterio) -> list[str]:
    cumple = p.cumple(c)
    veredicto = "CUBRE" if all(cumple.values()) else "NO CUBRE"
    return [
        f"MES {mes}: {dias} dias, {p.minutos} minutos de ventana -> {veredicto}",
        f"  (a) minutos con tick {_fr(p.con_tick, p.minutos)}: {'si' if cumple['a'] else 'no'}",
        f"  (b) huecos de mas de {c.b_umbral} min: {p.huecos_largos}; el mayor: {p.hueco_maximo} "
        f"min: {'si' if cumple['b'] else 'no'}",
        f"  (c) M1 que cuadran {_fr(p.m1_cuadran, p.m1_con_tick)}: {'si' if cumple['c'] else 'no'}",
        f"  (d1) horas con spread variable {_fr(p.horas_spread_variable, p.horas_con_tick)}: "
        f"{'si' if cumple['d1'] else 'no'}",
        f"  (d2) sobre {p.minutos_d2} minutos de horas que Dukascopy tiene descargadas: mediana "
        f"de ticks por minuto {p.mediana_ticks_minuto}, Dukascopy "
        f"{p.mediana_ticks_minuto_dukascopy}: {'si' if cumple['d2'] else 'no'}",
    ]


def main(argv: Sequence[str] | None = None, raiz: Path = RAIZ) -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("carpeta", type=Path, nargs="?")
    ap.add_argument("--control-dukascopy", action="store_true")
    ap.add_argument("--salida", type=Path, required=True)
    a = ap.parse_args(argv)
    sys.path.insert(0, str(raiz / "src"))
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.config.registro import cargar_registro
    from botsito.engine.calendario_cierres import cargar_calendario, ruta_calendario
    from botsito.engine.relojes import reloj_de_las_sesiones

    construccion = tuple(cargar_criterio(raiz).construccion)
    if not a.control_dukascopy:
        if a.carpeta is None:
            print("falta la carpeta del historial", file=sys.stderr)
            return 2
        malos = comprobar_meses((p.name for p in a.carpeta.iterdir() if p.is_file()), construccion)
        if malos:
            print(
                f"ERROR: ficheros que no son de un dia de construccion ({', '.join(construccion)}):"
                f" {', '.join(sorted(malos))}; no se lee nada",
                file=sys.stderr,
            )
            return 2
    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    sesiones = reloj_de_las_sesiones(registro)
    inicio = registro.hora("ventana_inicio").hora
    fin = registro.hora("ventana_fin").hora
    cal = cargar_calendario(ruta_calendario(raiz, PERFIL)).calendario()
    cierres = [(x.inicio_ms, x.fin_ms) for x in cal.cierres]
    cubre = (cal.cubre_desde_ms, cal.cubre_hasta_ms)
    criterio = cargar_criterio_f17(raiz)
    salida: list[str] = [f"CRITERIO: {CRITERIO.as_posix()} (pre-registrado, ADR-0099 §5)"]
    if a.control_dukascopy:
        salida += control_dukascopy(
            raiz, construccion, sesiones, inicio, fin, cierres, cubre, criterio
        )
    else:
        salida += leer_historial(
            raiz, a.carpeta, construccion, registro, sesiones, inicio, fin, cierres, cubre, criterio
        )
    a.salida.write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


def _dukascopy_del_mes(
    raiz: Path, mes: str, dias: Sequence[DiaVentana]
) -> tuple[TicksDelMes, frozenset[tuple[date, int]]]:
    """Los ticks de Dukascopy de la ventana de `dias` y las horas que su dataset tiene
    descargadas."""
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.ticks import buscar_manifiesto_ticks, cargar_manifiesto_ticks, cargar_ticks

    ticks = TicksDelMes()
    manifiesto = cargar_manifiesto_ticks(buscar_manifiesto_ticks(raiz, f"eurusd-ticks-{mes}"))
    datos = carpeta_datos(raiz)
    horas: frozenset[tuple[date, int]] = frozenset()
    for d in dias:
        serie = cargar_ticks(manifiesto, datos, d.desde * MS_POR_MINUTO, d.hasta * MS_POR_MINUTO)
        horas = horas_descargadas(serie.dias_seleccion, serie.horas_seleccion, serie.horas_perdidas)
        for t in serie.ticks:
            ticks.anadir(int(t.instante), int(t.bid), int(t.ask))
    return ticks, horas


def control_dukascopy(
    raiz: Path,
    construccion: Sequence[str],
    sesiones: Any,
    inicio: str,
    fin: str,
    cierres: Sequence[tuple[int, int]],
    cubre: tuple[int, int],
    c: Criterio,
) -> list[str]:
    """Punto 2 de la respuesta a la PARADA: (d1) sobre los ticks de Dukascopy de construccion."""
    salida = [f"CONTROL (d1) sobre Dukascopy, meses {', '.join(construccion)}"]
    for mes in construccion:
        dias = dias_del_mes(mes, sesiones, inicio, fin, cierres, cubre)
        ticks, _ = _dukascopy_del_mes(raiz, mes, dias)
        horas, variables = d1(dias, ticks, sesiones, c)
        pasa = horas > 0 and Fraction(variables, horas) >= c.d1_minimo
        salida.append(
            f"MES {mes}: {len(dias)} dias; horas dia-hora con tick {horas}; con al menos "
            f"{c.d1_valores} spreads distintos {_fr(variables, horas)}: "
            f"{'PASA' if pasa else 'NO PASA'}"
        )
    return salida


def leer_historial(
    raiz: Path,
    carpeta: Path,
    construccion: Sequence[str],
    registro: Any,
    sesiones: Any,
    inicio: str,
    fin: str,
    cierres: Sequence[tuple[int, int]],
    cubre: tuple[int, int],
    c: Criterio,
) -> list[str]:
    reloj = RelojServidor.del_registro(registro)
    controles = sorted(p for p in carpeta.iterdir() if PATRON_CONTROL.match(p.name))
    if len(controles) != 1:
        raise HistorialError(f"se espera un CSV de control y hay {len(controles)}")
    control = leer_control(controles[0])
    digitos = int(control["digits"])
    csv_d, reg_d = control_cuadra(control, reloj)
    incompletos = dias_incompletos(control)
    salida = [
        f"RELOJ: servidor = UTC + {reloj.base_minutos} min + verano de {reloj.huso or 'ninguno'} "
        "(broker_offset_base y broker_dst del registro)",
        f"CONTROL: desfase servidor-GMT del CSV {csv_d} min; el registro da {reg_d} min: "
        f"{'cuadra' if control_cuadra_con_registro(control, reloj) else 'NO CUADRA'}",
        f"DIAS sin ticks o con error al pedirlos: {len(incompletos)}"
        + (f" ({'; '.join(incompletos)})" if incompletos else ""),
    ]
    meses = sorted({m for p in carpeta.iterdir() if (m := mes_de_fichero(p.name)) is not None})
    for mes in meses:
        dias = dias_del_mes(mes, sesiones, inicio, fin, cierres, cubre)
        ftmo = TicksDelMes()
        m1: dict[int, Ohlc] = {}
        for p in sorted(carpeta.glob(f"F17_{mes}-*_ticks.csv")):
            leer_ticks(p, reloj, digitos, ftmo)
        for p in sorted(carpeta.glob(f"F17_{mes}-*_m1.csv")):
            m1.update(leer_m1(p, reloj, digitos))
        duk, horas_duk = _dukascopy_del_mes(raiz, mes, dias)
        p_mes = puntos_del_mes(dias, ftmo, m1, sesiones, c, duk, horas_duk)
        salida += lineas_del_mes(mes, len(dias), p_mes, c)
        if all(p_mes.cumple(c).values()):
            diferencia, global_ = diferencias_de_spread(dias, ftmo, duk, sesiones)
            salida.append(
                f"  diferencia mediana del spread (FTMO - Dukascopy, por dia-hora): {diferencia} "
                f"puntos; la de las medianas globales, sin uso: {global_} puntos"
            )
            por_hora: dict[int, list[int]] = defaultdict(list)
            for (_, hora), minutos in horas_dia(dias, sesiones).items():
                por_hora[hora] += [s for m in minutos for s in ftmo.spreads.get(m, ())]
            for hora in sorted(por_hora):
                v = sorted(por_hora[hora])
                if v:
                    salida.append(
                        f"  spread FTMO {hora:02d}:00: n {len(v)}, p50 {percentil(v, 0.5)}, "
                        f"p90 {percentil(v, 0.9)}, p99 {percentil(v, 0.99)}, max {v[-1]}"
                    )
    return salida


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
