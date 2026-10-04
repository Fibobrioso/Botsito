"""La cuarentena del corpus: UNA sola fuente para lo que no se ensena (rama
`trabajo/cuarentena-por-defecto`, 2026-10-01, docs/validation/CUARENTENA-POR-DEFECTO.md).

Tres cosas, con su motivo y en este orden de prioridad:

- (a) **las sesiones en cuarentena**: la transcripcion entera de una sesion con el trader que nadie
  lee (`SESIONES_EN_CUARENTENA`, LISTA EXPLICITA por decision del consultor);
- (b) **los tramos no citables** de `knowledge/corpus/tramos_no_citables.yaml`;
- (c) **el material reservado o sin sortear dentro del texto**: un segmento que nombra un mes que
  no se puede demostrar libre (`cases.holdout.meses_libres`; desde la rama
  `trabajo/cuarentena-por-condicion`, 2026-10-04), una fecha o un dia con numero, con la MISMA
  regla que aplica `scripts/transcribir_sesion.py` a la cruda de una sesion antes de escribir su
  version filtrada (`en_cuarentena`, movida aqui desde el script para que la CLI y el script usen
  la misma).

`Filtro` aplica las tres a los segmentos de UN video y anota lo que oculta -video, numero de
segmento, tiempos y motivo, NUNCA el texto ni que mes o dia disparo la regla-, para que quien lo
use diga cuantos oculto y por que. Las funciones que devuelven segmentos de una transcripcion
(`corpus.pipeline_transcripcion.cargar_cruda`, `cargar_corregida` y `cargar_capas`,
`corpus.transcripcion.texto_entre`, `retrieval.consultas.buscar` y `en_instante`) filtran por
defecto, y el contenido sin filtrar se pide con `crudo=True`, que solo usan los llamadores
autorizados de `tests/unit/test_cuarentena.py` (`AUTORIZADOS`, cada uno con su motivo: la
verificacion de citas, `corpus glossary apply`, `corpus transcript check`,
`scripts/transcribir_sesion.py`) y los tests; el mismo test falla si alguien mas lo pide o lee la
cruda sin pasar por estas funciones.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from types import MappingProxyType
from typing import Protocol, TypeVar

from botsito.comun.yaml_estricto import YamlError, leer_yaml

# ------------------------------------------------------------------- (a) los videos en cuarentena

# LISTA EXPLICITA (decision del consultor del 2026-10-01): las sesiones con el trader cuya
# transcripcion no lee nadie, de v7 en adelante. Un video de sesion se ANADE aqui al ingerirlo
# (skill `ingerir-sesion`). `tests/unit/test_cuarentena.py` la cruza con `fuentes.yaml` y falla si
# un video con `drive_id: null` -una grabacion de sesion- no esta en ella ni en las EXCEPCIONES, o
# si uno de la lista tiene `drive_id`: asi un video nuevo sin listar rompe `make check` en vez de
# quedar visible. La guardia de Claude Code guarda su copia (`.claude/hooks/guardia.py`) y
# `tests/unit/test_guardia_claude.py` comprueba que dice lo mismo.
SESIONES_EN_CUARENTENA: frozenset[str] = frozenset({"v7", "v8", "v9", "v10"})
# Sesiones con `drive_id: null` que NO estan en cuarentena, cada una con su motivo.
EXCEPCIONES: Mapping[str, str] = MappingProxyType(
    {
        "v6": (
            "la sesion 01 se transcribio y se leyo antes de que existiera la cuarentena, y su dia "
            "reservado esta RETIRADO del holdout (ADR-0041, "
            "docs/validation/V6-FUERA-DEL-HOLDOUT.md); sus tramos no citables siguen ocultos "
            "(decision del consultor del 2026-10-01, "
            "docs/validation/GUARDIAS-CLAUDE.md)"
        ),
    }
)


def problemas_de_la_lista(drive_ids: Mapping[str, str | None]) -> list[str]:
    """La lista frente a `fuentes.yaml` (`video_id -> drive_id`): una grabacion de sesion
    (`drive_id: null`) que no este en la lista ni en las EXCEPCIONES, o un video de la lista que no
    exista o que tenga `drive_id`. Vacio si cuadran."""
    problemas = [
        f"{v}: es una sesion (drive_id null) y no esta en SESIONES_EN_CUARENTENA ni en EXCEPCIONES"
        for v, d in sorted(drive_ids.items())
        if d is None and v not in SESIONES_EN_CUARENTENA and v not in EXCEPCIONES
    ]
    for v in sorted(SESIONES_EN_CUARENTENA):
        if v not in drive_ids:
            problemas.append(f"{v}: esta en SESIONES_EN_CUARENTENA y no en fuentes.yaml")
        elif drive_ids[v] is not None:
            problemas.append(f"{v}: esta en SESIONES_EN_CUARENTENA y tiene drive_id")
    problemas += [
        f"{v}: esta a la vez en SESIONES_EN_CUARENTENA y en EXCEPCIONES"
        for v in sorted(SESIONES_EN_CUARENTENA & set(EXCEPCIONES))
    ]
    return problemas


MOTIVO_SESION = "a"
MOTIVO_TRAMO = "b"
MOTIVO_RESERVADO = "c"
MOTIVOS: Mapping[str, str] = MappingProxyType(
    {
        MOTIVO_SESION: "sesion en cuarentena",
        MOTIVO_TRAMO: "tramo no citable",
        MOTIVO_RESERVADO: "material reservado o sin sortear",
    }
)


class CuarentenaError(ValueError):
    """Una funcion que filtra por defecto se llamo sin filtro y sin `crudo=True`."""


SIN_FILTRO = (
    "filtra por defecto: pasa un `Filtro` (`botsito.corpus.cuarentena`) o `crudo=True`, que solo "
    "usan los llamadores autorizados (`AUTORIZADOS` en tests/unit/test_cuarentena.py) y los tests"
)

# --------------------------------------------------------------- (b) los tramos no citables

FICHERO_TRAMOS_NO_CITABLES = "knowledge/corpus/tramos_no_citables.yaml"
Tramos = dict[str, tuple[tuple[int, int, str], ...]]


class TramosNoCitablesError(ValueError):
    """El fichero de tramos no citables existe pero no se puede leer."""


def cargar_tramos_no_citables(repo: Path) -> Tramos:
    """Tramos de video que no son especificacion, por video_id (F07).

    Sin fichero no hay tramos: un repo anterior a esto sigue funcionando igual. Hasta el 2026-10-01
    vivia en `validation/contexto_evidencia.py`, que lo sigue exportando; bajo aqui para que
    `retrieval` y la CLI lo lean de la misma fuente, y lee los tiempos con `parse_ms` (el formato
    estricto de la evidencia, hasta tres decimales) porque `corpus` no importa `evidence`.
    """
    from botsito.corpus.transcripcion import TranscripcionError, parse_ms

    ruta = repo / FICHERO_TRAMOS_NO_CITABLES
    if not ruta.is_file():
        return {}
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise TramosNoCitablesError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"tramos"}:
        raise TramosNoCitablesError(f"{ruta.name}: se espera una unica clave 'tramos'")
    bruto = doc["tramos"]
    if not isinstance(bruto, list):
        raise TramosNoCitablesError(f"{ruta.name}: 'tramos' debe ser una lista")
    por_video: dict[str, list[tuple[int, int, str]]] = {}
    for i, tramo in enumerate(bruto, start=1):
        campos = {"video_id", "t0", "t1", "motivo", "acordado"}
        if not isinstance(tramo, dict) or set(tramo) != campos:
            raise TramosNoCitablesError(
                f"{ruta.name}: tramo {i} necesita video_id, t0, t1, motivo y acordado"
            )
        try:
            t0_ms = parse_ms(str(tramo["t0"]))
            t1_ms = parse_ms(str(tramo["t1"]))
        except TranscripcionError as exc:
            raise TramosNoCitablesError(f"{ruta.name}: tramo {i}: {exc}") from exc
        if t1_ms <= t0_ms:
            raise TramosNoCitablesError(f"{ruta.name}: tramo {i}: t1 debe ser posterior a t0")
        motivo = " ".join(str(tramo["motivo"]).split())
        if not motivo:
            raise TramosNoCitablesError(f"{ruta.name}: tramo {i}: motivo vacio")
        por_video.setdefault(str(tramo["video_id"]), []).append((t0_ms, t1_ms, motivo))
    return {v: tuple(sorted(ts)) for v, ts in por_video.items()}


# --------------------------------------------- (c) la regla por segmento, desde el script

# ------------------------------------------------------------------------------ normalizar


def normalizar(texto: str) -> str:
    """Minusculas y sin tildes; los guiones, barras y puntos se conservan (las fechas los usan)."""
    plano = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in plano if unicodedata.category(c) != "Mn")


_UNIDADES = {
    "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12,
    "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiun": 21, "veintiuno": 21,
    "veintiuna": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25,
    "veintiseis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29,
}  # fmt: skip
_DECENAS = {
    "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70,
    "ochenta": 80, "noventa": 90,
}  # fmt: skip


def numeros_a_cifras(texto: str) -> str:
    """«treinta y cinco» -> «35», «veinticinco» -> «25», «trece» -> «13» (de 0 a 99), sobre texto
    ya normalizado. «un» y «una» NO se convierten: «voy a una zona» no es el codigo A-1."""
    tokens = re.findall(r"\w+|[^\w\s]|\s+", texto)
    salida: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in _DECENAS:
            valor = _DECENAS[t]
            # «treinta y cinco»: decena, espacio, «y», espacio, unidad 1-9
            if (
                i + 4 < len(tokens)
                and tokens[i + 1].isspace()
                and tokens[i + 2] == "y"
                and tokens[i + 3].isspace()
                and 1 <= _UNIDADES.get(tokens[i + 4], 0) <= 9
            ):
                salida.append(str(valor + _UNIDADES[tokens[i + 4]]))
                i += 5
                continue
            salida.append(str(valor))
        elif t in _UNIDADES:
            salida.append(str(_UNIDADES[t]))
        else:
            salida.append(t)
        i += 1
    return "".join(salida)


# ------------------------------------------------------------------------------ cuarentena

# LA REGLA DEL MES (rama `trabajo/cuarentena-por-condicion`, decision del consultor del
# 2026-10-04): se tapa TODO mes que no se pueda demostrar libre. Que meses son libres no lo decide
# este modulo -`corpus` no puede leer `cases`-: lo calcula `botsito.cases.holdout.meses_libres`
# (sin dias en `casos_ocultos` ni en `casos_reservados`, y fuera de `meses_reservados.yaml`) y se lo
# pasa quien construye el filtro, como los `dias`. Sin ese dato (`libres=None`) se tapan los doce:
# ningun valor por defecto deja un mes a la vista. Hasta esta rama la regla era una LISTA FIJA de
# cuatro meses (`MESES_FILTRADOS`), y junio, con dias ocultos, no estaba
# (docs/validation/SESION-04-EXTRACCION.md §2.4).
#
# GRAFIAS_MES es un diccionario de grafias POR MES, no una lista de meses vigilados: para cada mes,
# su nombre en espanol, en ingles y su abreviatura; y para septiembre, marzo, mayo y febrero ademas
# las grafias del ASR medidas en las crudas de v1-v6. Todo va por palabra entera: «mayo» es PREFIJO
# de «mayor» y «mayoria», y «siempre» se parece a «setiempre».
GRAFIAS_MES: Mapping[int, tuple[str, ...]] = MappingProxyType(
    {
        1: ("enero", "january", "ene"),
        2: (r"fe[bv]r?e?r?o?s?", "february"),  # febrero, febreo, febrer, feb, fevrero
        3: (r"mar[sz]os?|mar", "march"),  # marzo, marso, mar (NO «marco»: ver abajo)
        4: ("abril", "april", "abr"),
        5: (r"ma[yi]o|mallo", "may"),  # mayo, maio, mallo (no «malo»)
        6: ("junio", "june", "jun"),
        7: ("julio", "july", "jul"),
        8: ("agosto", "august", "ago"),
        # septiembre, setiembre, setiempre, sectiembre, setembre...; sep y sept (abreviatura)
        9: (r"se[cpt]{0,2}i?e?m[bp]re?s?", r"sept?", r"septem[bp]er"),
        10: ("octubre", "october", "oct"),
        11: ("noviembre", "november", "nov"),
        12: ("diciembre", "december", "dic"),
    }
)
# Las abreviaturas que solo cuentan junto a «backtest» (motivo «backtest con mes»): «set» no se
# tapa suelta -es una palabra corriente-, pero «el backtest de set» si.
ABREVIATURAS_MES: Mapping[int, tuple[str, ...]] = MappingProxyType(
    {
        1: ("ene",), 2: ("feb",), 3: ("mar",), 4: ("abr",), 5: ("may",), 6: ("jun",),
        7: ("jul",), 8: ("ago",), 9: ("sep", "sept", "set"), 10: ("oct",), 11: ("nov",),
        12: ("dic",),
    }
)  # fmt: skip
TODOS_LOS_MESES = frozenset(range(1, 13))
# «marco» NO se filtra: es el verbo del trader («lo marco», «marco la liquidez») y el sustantivo
# de «marco de operativa»; en las crudas de v1-v6 no hay ni un «marco» por «marzo» (medido el
# 2026-09-27: «marzo» sale bien escrito la unica vez que aparece).


def meses_tapados(libres: Collection[int] | None) -> frozenset[int]:
    """Los meses que tapa la regla: todos menos los DEMOSTRADOS libres; los doce si no hay dato."""
    if libres is None:
        return TODOS_LOS_MESES
    return TODOS_LOS_MESES - frozenset(libres)


@cache
def _patrones(tapados: frozenset[int]) -> tuple[re.Pattern[str] | None, re.Pattern[str] | None]:
    """(nombres, abreviaturas) de los meses tapados, cada uno None si no hay ninguno."""
    if not tapados:
        return None, None
    nombres = [g for m in sorted(tapados) for g in GRAFIAS_MES[m]]
    abrev = [a for m in sorted(tapados) for a in ABREVIATURAS_MES[m]]
    return (
        re.compile(r"\b(?:" + "|".join(nombres) + r")\b"),
        re.compile(r"\b(?:" + "|".join(abrev) + r")\b"),
    )


_NUM = r"(?:\d{1,2})"
_RE_FECHA = re.compile(
    rf"(?<![\d.,]){_NUM}\s*[/-]\s*{_NUM}(?:\s*[/-]\s*\d{{2,4}})?(?![\d.,])"  # 31/02, 31-02-26
    rf"|(?<![\d.,]){_NUM}\.{_NUM}\.\d{{2,4}}(?![\d.,])"  # 31.02.26 (dos partes: precio)
    rf"|(?<![\d.,]){_NUM}\s+del?\s+{_NUM}(?![\d.,])"  # «45 del 13», «3 de 9»
    rf"|\bmes\s+{_NUM}\b"  # «el mes 9»
)
_DIAS = r"(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo)"
_RE_DIA_NUMERO = re.compile(rf"\b{_DIAS}\b(?:\W+\w+)?\W+{_NUM}\b|\b{_NUM}\b(?:\W+\w+)?\W+{_DIAS}\b")
_RE_BACKTEST = re.compile(r"\b(?:back\s*-?\s*tests?|bac?k?test\w*|vac?k?test\w*)\b")

MOTIVO_MES = "mes"
MOTIVO_FECHA = "fecha numerica"
MOTIVO_DIA = "dia de la semana con numero"
MOTIVO_BACKTEST = "backtest con mes"
MOTIVO_VECINO = "vecino"


def motivos_cuarentena(texto: str, libres: Collection[int] | None = None) -> list[str]:
    """Por que un texto va a cuarentena (lista vacia si no va). Sin tildes, sin mayusculas, y con
    los numeros escritos en letras pasados a cifras. `libres`: los meses DEMOSTRADOS libres
    (`cases.holdout.meses_libres`); sin ellos se tapan los doce."""
    t = numeros_a_cifras(normalizar(texto))
    re_mes, re_abrev = _patrones(meses_tapados(libres))
    motivos: list[str] = []
    if re_mes is not None and re_mes.search(t):
        motivos.append(MOTIVO_MES)
    if _RE_FECHA.search(t):
        motivos.append(MOTIVO_FECHA)
    if _RE_DIA_NUMERO.search(t):
        motivos.append(MOTIVO_DIA)
    if re_abrev is not None and _RE_BACKTEST.search(t) and re_abrev.search(t):
        motivos.append(MOTIVO_BACKTEST)
    return motivos


def en_cuarentena(
    textos: Sequence[str], libres: Collection[int] | None = None
) -> dict[int, list[str]]:
    """Indice -> motivos. Cada segmento con motivo arrastra al anterior y al siguiente. `libres`,
    como en `motivos_cuarentena`: sin ellos se tapan los doce meses."""
    propios = {i: m for i, t in enumerate(textos) if (m := motivos_cuarentena(t, libres))}
    salida: dict[int, list[str]] = {i: list(m) for i, m in propios.items()}
    for i in propios:
        for j in (i - 1, i + 1):
            if 0 <= j < len(textos) and j not in propios:
                salida.setdefault(j, [MOTIVO_VECINO])
    return salida


# ------------------------------------------------------------------------------------- el filtro


class SegmentoFiltrable(Protocol):
    """Lo que el filtro mira de un segmento: `corpus.transcripcion.Segmento` y el
    `evidence.verificacion.SegmentoCitable` de las propuestas lo cumplen."""

    @property
    def n(self) -> int: ...
    @property
    def t0_ms(self) -> int: ...
    @property
    def t1_ms(self) -> int: ...
    @property
    def texto(self) -> str: ...


S = TypeVar("S", bound=SegmentoFiltrable)


@dataclass(frozen=True, slots=True)
class Oculto:
    """Un segmento (o un item de evidencia) que no se ensena: donde esta y por que, SIN su texto.
    `fecha_vigilada` dice si su texto trae una fecha que es uno de los `dias` del filtro (los de
    `casos_ocultos`, si quien construye el filtro se los pasa): un booleano, nunca la fecha."""

    video_id: str
    n: int
    t0_ms: int
    t1_ms: int
    motivo: str  # MOTIVO_SESION | MOTIVO_TRAMO | MOTIVO_RESERVADO
    fecha_vigilada: bool = False
    clase: str = "segmento"  # segmento | evidencia


# ---------------------------------------------------------- las fechas de un texto (dia y mes)

_MESES_NUM = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
    "agosto": 8, "septiembre": 9, "setiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}  # fmt: skip
_RE_NOMBRE_MES = "|".join(_MESES_NUM)
_RE_DIA_DE_MES = re.compile(rf"\b(\d{{1,2}})\s+(?:de\s+)?({_RE_NOMBRE_MES})\b")
_RE_MES_DIA = re.compile(rf"\b({_RE_NOMBRE_MES})\s+(\d{{1,2}})\b")
_RE_DIA_BARRA_MES = re.compile(r"(?<![\d.,])(\d{1,2})\s*[/-]\s*(\d{1,2})(?![\d.,])")


def fechas_en(texto: str) -> set[tuple[int, int]]:
    """Las fechas (mes, dia) que un texto dice con dia Y mes: «4 de mayo», «mayo 4», «4/5»,
    tambien con el numero en letras. Un mes sin dia, o un dia sin mes, no es una fecha."""
    t = numeros_a_cifras(normalizar(texto))
    salida: set[tuple[int, int]] = set()
    for d, m in _RE_DIA_DE_MES.findall(t):
        salida.add((_MESES_NUM[m], int(d)))
    for m, d in _RE_MES_DIA.findall(t):
        salida.add((_MESES_NUM[m], int(d)))
    for d, m in _RE_DIA_BARRA_MES.findall(t):
        salida.add((int(m), int(d)))
    return {(m, d) for m, d in salida if 1 <= m <= 12 and 1 <= d <= 31}


def dias_de_casos(casos: Iterable[str]) -> frozenset[tuple[int, int]]:
    """(mes, dia) de cada id de caso `caso-<simbolo>-AAAA-MM-DD` (los de `casos_ocultos`)."""
    salida: set[tuple[int, int]] = set()
    for c in casos:
        if m := re.search(r"-\d{4}-(\d{2})-(\d{2})$", c):
            salida.add((int(m.group(1)), int(m.group(2))))
    return frozenset(salida)


def _toca(t0_ms: int, t1_ms: int, a_ms: int, b_ms: int) -> bool:
    """La misma seleccion que `texto_entre`: un instante coge el segmento que lo contiene, y un
    intervalo, los que lo pisan."""
    if a_ms == b_ms:
        return t0_ms <= a_ms <= t1_ms
    return t1_ms > a_ms and t0_ms < b_ms


@dataclass
class Filtro:
    """Las tres reglas sobre los segmentos de UN video, con lo que van ocultando (por numero de
    segmento: aplicar dos veces el mismo filtro no cuenta dos veces)."""

    video_id: str
    tramos: tuple[tuple[int, int, str], ...] = ()
    ocultos: dict[int, Oculto] = field(default_factory=dict)
    # Los dias (mes, dia) que se vigilan en el texto de lo oculto: los de `casos_ocultos`, que
    # `corpus` no puede leer (es la capa `cases`) y le pasa quien construye el filtro.
    dias: frozenset[tuple[int, int]] = frozenset()
    # Los meses DEMOSTRADOS libres para la regla del mes (`cases.holdout.meses_libres`), que le pasa
    # quien construye el filtro como los `dias`. None: no se demostro ninguno y se tapan los doce.
    libres: frozenset[int] | None = None

    def motivos(self, segmentos: Sequence[SegmentoFiltrable]) -> dict[int, str]:
        """Posicion en `segmentos` -> motivo, con prioridad a > b > c."""
        if self.video_id in SESIONES_EN_CUARENTENA:
            return dict.fromkeys(range(len(segmentos)), MOTIVO_SESION)
        salida: dict[int, str] = {}
        for i, s in enumerate(segmentos):
            if any(s.t1_ms > a and s.t0_ms < b for a, b, _ in self.tramos):
                salida[i] = MOTIVO_TRAMO
        for i in en_cuarentena([s.texto for s in segmentos], self.libres):
            salida.setdefault(i, MOTIVO_RESERVADO)
        return salida

    def aplicar(self, segmentos: Sequence[S]) -> list[S]:
        """Los segmentos que se pueden ensenar; los demas quedan anotados en `ocultos`."""
        motivos = self.motivos(segmentos)
        for i, motivo in motivos.items():
            s = segmentos[i]
            vigilada = bool(self.dias) and bool(fechas_en(s.texto) & self.dias)
            self.ocultos.setdefault(
                s.n, Oculto(self.video_id, s.n, s.t0_ms, s.t1_ms, motivo, vigilada)
            )
        return [s for i, s in enumerate(segmentos) if i not in motivos]

    def ocultos_entre(self, a_ms: int, b_ms: int) -> list[Oculto]:
        return [o for o in self.ocultos.values() if _toca(o.t0_ms, o.t1_ms, a_ms, b_ms)]


def filtros(repo: Path, libres: frozenset[int] | None = None) -> dict[str, Filtro]:
    """Un `Filtro` por video con los tramos del repositorio; el de un video sin tramos se crea al
    pedirlo con `filtro_de`. `libres` lo calcula `cases.holdout.meses_libres`, que esta capa no
    puede leer; sin el se tapan los doce meses."""
    return {v: Filtro(v, ts, libres=libres) for v, ts in cargar_tramos_no_citables(repo).items()}


def filtro_de(repo: Path, video_id: str, libres: frozenset[int] | None = None) -> Filtro:
    return Filtro(video_id, cargar_tramos_no_citables(repo).get(video_id, ()), libres=libres)


DIRECTORIO_PROPUESTAS = "knowledge/_proposals"
# La lista que lee la guardia de Claude Code: los ficheros del repositorio que copian texto que hoy
# se oculta. CALCULADA -las propuestas por `propuestas_con_ocultos`; las salidas de medicion que
# traen alguna linea de un segmento oculto, y los ficheros de docs/ que copian esas lineas, por
# `scripts/ficheros_con_ocultos.py`-, escrita por ese guion con `--escribir` y vigilada por
# `tests/unit/test_guardia_claude.py` (ordenes del consultor del 2026-10-01, tercera a quinta).
FICHERO_OCULTOS = ".claude/hooks/ficheros_con_ocultos.txt"
# Las salidas commiteadas de los guiones de medicion que leen transcripciones, con el guion y el
# conjunto que las regeneraban. Son los CANDIDATOS; cuales entran en la lista lo dice el calculo.
SALIDAS_DE_MEDICIONES: Mapping[str, tuple[str, str | None]] = MappingProxyType(
    {
        "docs/validation/A18-TRANSCRIPCIONES-SALIDA.txt": ("a18_buscar", None),
        "docs/validation/A24-A21-A26-A34-SALIDA.txt": ("buscar_ambiguedades", "a24"),
        "docs/validation/A35-PIVOTE-FORMADO-SALIDA.txt": ("buscar_ambiguedades", "a35"),
        "docs/validation/SESION-02-BUSQUEDA-SALIDA.txt": ("buscar_ambiguedades", "sesion02"),
    }
)


@dataclass(frozen=True, slots=True)
class _SegmentoDePropuesta:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str


def propuestas_con_ocultos(
    repo: Path, libres: frozenset[int] | None = None
) -> dict[str, Counter[str]]:
    """Fichero de `knowledge/_proposals/` -> cuantos de sus segmentos copiados caen en cada regla,
    solo los que tienen alguno. Lee el YAML de la propuesta (los segmentos estan copiados en
    `contexto.segmentos`) y aplica `Filtro.motivos`, que solo devuelve posiciones y motivos."""
    tramos = cargar_tramos_no_citables(repo)
    salida: dict[str, Counter[str]] = {}
    for ruta in sorted((repo / DIRECTORIO_PROPUESTAS).glob("pr-*.yaml")):
        try:
            doc = leer_yaml(ruta)
        except (OSError, YamlError) as exc:
            raise CuarentenaError(f"{ruta.name}: {exc}") from exc
        if not isinstance(doc, dict) or not isinstance(doc.get("contexto"), dict):
            raise CuarentenaError(f"{ruta.name}: sin contexto")
        video = str(doc.get("video_id"))
        segmentos = [
            _SegmentoDePropuesta(int(s["n"]), int(s["t0_ms"]), int(s["t1_ms"]), str(s["texto"]))
            for s in doc["contexto"].get("segmentos") or []
        ]
        filtro = Filtro(video, tramos.get(video, ()), libres=libres)
        cuenta = Counter(filtro.motivos(segmentos).values())
        if cuenta:
            salida[ruta.name] = cuenta
    return salida


def texto_de_la_lista(rutas: Iterable[str]) -> str:
    """El fichero que lee la guardia: una cabecera que dice de donde sale, y una ruta relativa
    al repositorio por linea."""
    cabecera = (
        "# GENERADO por `uv run python scripts/ficheros_con_ocultos.py --escribir` desde\n"
        "# `botsito.corpus.cuarentena`: los ficheros del repositorio que copian texto que hoy se\n"
        "# oculta (sesion en cuarentena, tramo no citable o material reservado o sin sortear):\n"
        "# las propuestas de knowledge/_proposals/ con algun segmento oculto, las salidas de\n"
        "# medicion con alguna linea de un segmento oculto y los ficheros de docs/ que copian\n"
        "# esas lineas. No se edita a mano: tests/unit/test_guardia_claude.py falla si no\n"
        "# coincide con lo que se calcula. La guardia de Claude Code no deja leerlos.\n"
    )
    return cabecera + "".join(f"{p}\n" for p in sorted(rutas))


def resumen(ocultos: Iterable[Oculto]) -> str:
    """Cuantos se ocultaron y por que, en una linea; vacio si ninguno. Solo numeros y motivos:
    nunca un texto, una fecha ni el mes o el dia que disparo la regla."""
    lista = list(ocultos)
    if not lista:
        return ""
    trozos = []
    for clase, nombre in (("segmento", "segmentos"), ("evidencia", "items de evidencia")):
        cuenta = Counter(o.motivo for o in lista if o.clase == clase)
        if cuenta:
            partes = [f"{cuenta[m]} por {MOTIVOS[m]} ({m})" for m in sorted(cuenta)]
            trozos.append(f"{sum(cuenta.values())} {nombre}: {', '.join(partes)}")
    return (
        f"OCULTOS: {'; y '.join(trozos)}. Su contenido no se ensena; con --crudo, solo Aleks en "
        "su propia terminal."
    )


def items_ocultos(filtro: Filtro, items: Iterable[tuple[str, int, int]]) -> dict[str, Oculto]:
    """Los items de evidencia `(id, t0_ms, t1_ms)` de `filtro.video_id` cuya cita pisa un
    segmento que el filtro oculto, con el motivo de mas prioridad de los que pisa (a > b > c).
    Cuarta orden del consultor del 2026-10-01: la evidencia cuya cita cae en un segmento oculto se
    oculta como el segmento."""
    salida: dict[str, Oculto] = {}
    for iid, t0_ms, t1_ms in items:
        pisa = filtro.ocultos_entre(t0_ms, t1_ms)
        if pisa:
            motivo = min(o.motivo for o in pisa)
            vigilada = any(o.fecha_vigilada for o in pisa)
            salida[iid] = Oculto(
                filtro.video_id, -1, t0_ms, t1_ms, motivo, vigilada, clase="evidencia"
            )
    return salida


def evidencia_a_ocultar(
    filtro: Filtro,
    items: Iterable[tuple[str, int, int, str]],
    visibles: Sequence[SegmentoFiltrable],
) -> dict[str, Oculto]:
    """Sexta orden del consultor (2026-10-01): el criterio de la EVIDENCIA, que no es el de la
    cruda. Un item `(id, t0_ms, t1_ms, texto)` es un extracto REVISADO, y sus ficheros se leen
    con Read: la sesion en cuarentena (a) y la regla del mes (c), que existen porque la cruda no
    esta revisada, no lo ocultan. Se oculta SOLO si:
    - (b) su cita cae en un tramo no citable (pisa el tramo o un segmento que el filtro oculto por
      el); la copia del texto de un tramo la anade `items_que_copian` con `motivos={"b"}`;
    - o trae una fecha que es uno de `filtro.dias` (los de `casos_ocultos`): en su propio texto,
      en un segmento VISIBLE que su cita pisa (`visibles`, la cruda filtrada) o en uno OCULTO que
      pisa (`Oculto.fecha_vigilada`, que anota el filtro). Ese motivo cuenta como (c), material
      reservado.
    Devuelve ids, motivos y el booleano de la fecha; nunca texto ni la fecha."""
    salida: dict[str, Oculto] = {}
    for iid, t0_ms, t1_ms, texto in items:
        pisa = filtro.ocultos_entre(t0_ms, t1_ms)
        motivos: set[str] = set()
        if any(o.motivo == MOTIVO_TRAMO for o in pisa) or any(
            _toca(a, b, t0_ms, t1_ms) for a, b, _ in filtro.tramos
        ):
            motivos.add(MOTIVO_TRAMO)
        fecha = bool(filtro.dias) and (
            bool(fechas_en(texto) & filtro.dias)
            or any(o.fecha_vigilada for o in pisa)
            or any(
                fechas_en(s.texto) & filtro.dias
                for s in visibles
                if _toca(s.t0_ms, s.t1_ms, t0_ms, t1_ms)
            )
        )
        if fecha:
            motivos.add(MOTIVO_RESERVADO)
        if motivos:
            salida[iid] = Oculto(
                filtro.video_id, -1, t0_ms, t1_ms, min(motivos), fecha, clase="evidencia"
            )
    return salida


# ------------------------------------------ lo que COPIA el texto de un segmento oculto (quinta)
# Quinta orden del consultor (2026-10-01): un texto copia un segmento oculto si contiene la mitad
# o mas de las ventanas de 30 caracteres (cada 10) de su texto, con el espacio normalizado y en
# minusculas. Es el metodo con el que se midio
# (`docs/validation/anexos/CUARENTENA-POR-DEFECTO/citas_de_salidas.py`), y lo usan la evidencia
# de `kb` y la lista de la guardia.
VENTANA_COPIA = 30
PASO_COPIA = 10
_MINIMO_COPIA = 15  # un segmento mas corto no se busca: casaria con cualquier cosa


def plano(texto: str) -> str:
    return " ".join(texto.split()).lower()


def ventanas_de_copia(texto: str) -> list[str]:
    t = plano(texto)
    if len(t) <= VENTANA_COPIA:
        return [t] if len(t) >= _MINIMO_COPIA else []
    return [t[i : i + VENTANA_COPIA] for i in range(0, len(t) - VENTANA_COPIA + 1, PASO_COPIA)]


def copia(texto_plano: str, ventanas: Sequence[str]) -> bool:
    """`texto_plano` (ya pasado por `plano`) trae la mitad o mas de `ventanas`."""
    if not ventanas:
        return False
    dentro = sum(1 for v in ventanas if v in texto_plano)
    # La mitad o mas, en enteros: el umbral es la definicion de la quinta orden, no un parametro.
    return dentro > 0 and 2 * dentro >= len(ventanas)


def items_que_copian(
    filtro: Filtro,
    segmentos: Sequence[SegmentoFiltrable],
    items: Iterable[tuple[str, int, int, str]],
    motivos: Collection[str] = MOTIVOS,
) -> dict[str, Oculto]:
    """Los items `(id, t0_ms, t1_ms, texto)` cuyo texto COPIA un segmento que `filtro` ya oculto
    por alguno de `motivos`, aunque su cita no lo pise (quinta orden). `segmentos` es la cruda
    ENTERA del video: solo se miran los que estan en `filtro.ocultos`. Devuelve ids y motivos,
    nunca texto."""
    ocultos = [
        (ventanas_de_copia(s.texto), filtro.ocultos[s.n])
        for s in segmentos
        if s.n in filtro.ocultos and filtro.ocultos[s.n].motivo in motivos
    ]
    salida: dict[str, Oculto] = {}
    for iid, t0_ms, t1_ms, texto in items:
        t = plano(texto)
        copiados = [o for ventanas, o in ocultos if copia(t, ventanas)]
        if copiados:
            motivo = min(o.motivo for o in copiados)
            vigilada = any(o.fecha_vigilada for o in copiados)
            salida[iid] = Oculto(
                filtro.video_id, -1, t0_ms, t1_ms, motivo, vigilada, clase="evidencia"
            )
    return salida
