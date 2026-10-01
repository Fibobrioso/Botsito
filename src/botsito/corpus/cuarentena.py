"""La cuarentena del corpus: UNA sola fuente para lo que no se ensena (rama
`trabajo/cuarentena-por-defecto`, 2026-10-01, docs/validation/CUARENTENA-POR-DEFECTO.md).

Tres cosas, con su motivo y en este orden de prioridad:

- (a) **las sesiones en cuarentena**: la transcripcion entera de una sesion con el trader que nadie
  lee (`SESIONES_EN_CUARENTENA`, LISTA EXPLICITA por decision del consultor);
- (b) **los tramos no citables** de `knowledge/corpus/tramos_no_citables.yaml`;
- (c) **el material reservado o sin sortear dentro del texto**: un segmento que nombra un mes con
  dias reservados o sin sortear, una fecha o un dia con numero, con la MISMA regla que aplica
  `scripts/transcribir_sesion.py` a la cruda de una sesion antes de escribir su version filtrada
  (`en_cuarentena`, movida aqui desde el script para que la CLI y el script usen la misma).

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
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
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
SESIONES_EN_CUARENTENA: frozenset[str] = frozenset({"v7", "v8", "v9"})
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

# Grafias de los cuatro meses. Medido en las crudas de v1-v6: el ASR escribe «mayo»,
# «septiembre» y «marzo» bien; «mayo» es PREFIJO de «mayor» y «mayoria», y «siempre» se parece a
# «setiempre», asi que todo va por palabra entera. Los errores tipicos se anaden por si acaso.
MESES_FILTRADOS = (
    r"se[cpt]{0,2}i?e?m[bp]re?s?",  # septiembre, setiembre, setiempre, sectiembre, setembre...
    r"sept?",  # sep, sept (abreviatura)
    r"septem[bp]er",
    r"mar[sz]os?|mar",  # marzo, marso, mar (NO «marco»: ver abajo)
    r"march",
    r"ma[yi]o|mallo",  # mayo, maio, mallo (no «malo»)
    r"may",
    r"fe[bv]r?e?r?o?s?",  # febrero, febreo, febrer, feb, fevrero
    r"february",
)
# «marco» NO se filtra: es el verbo del trader («lo marco», «marco la liquidez») y el sustantivo
# de «marco de operativa»; en las crudas de v1-v6 no hay ni un «marco» por «marzo» (medido el
# 2026-09-27: «marzo» sale bien escrito la unica vez que aparece).
_RE_MES = re.compile(r"\b(?:" + "|".join(MESES_FILTRADOS) + r")\b")
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
_RE_ABREV = re.compile(r"\b(?:sep|sept|set|mar|may|feb)\b")

MOTIVO_MES = "mes"
MOTIVO_FECHA = "fecha numerica"
MOTIVO_DIA = "dia de la semana con numero"
MOTIVO_BACKTEST = "backtest con mes"
MOTIVO_VECINO = "vecino"


def motivos_cuarentena(texto: str) -> list[str]:
    """Por que un texto va a cuarentena (lista vacia si no va). Sin tildes, sin mayusculas, y con
    los numeros escritos en letras pasados a cifras."""
    t = numeros_a_cifras(normalizar(texto))
    motivos: list[str] = []
    if _RE_MES.search(t):
        motivos.append(MOTIVO_MES)
    if _RE_FECHA.search(t):
        motivos.append(MOTIVO_FECHA)
    if _RE_DIA_NUMERO.search(t):
        motivos.append(MOTIVO_DIA)
    if _RE_BACKTEST.search(t) and _RE_ABREV.search(t):
        motivos.append(MOTIVO_BACKTEST)
    return motivos


def en_cuarentena(textos: Sequence[str]) -> dict[int, list[str]]:
    """Indice -> motivos. Cada segmento con motivo arrastra al anterior y al siguiente."""
    propios = {i: m for i, t in enumerate(textos) if (m := motivos_cuarentena(t))}
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
    """Un segmento que no se ensena: donde esta y por que, SIN su texto."""

    video_id: str
    n: int
    t0_ms: int
    t1_ms: int
    motivo: str  # MOTIVO_SESION | MOTIVO_TRAMO | MOTIVO_RESERVADO


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

    def motivos(self, segmentos: Sequence[SegmentoFiltrable]) -> dict[int, str]:
        """Posicion en `segmentos` -> motivo, con prioridad a > b > c."""
        if self.video_id in SESIONES_EN_CUARENTENA:
            return dict.fromkeys(range(len(segmentos)), MOTIVO_SESION)
        salida: dict[int, str] = {}
        for i, s in enumerate(segmentos):
            if any(s.t1_ms > a and s.t0_ms < b for a, b, _ in self.tramos):
                salida[i] = MOTIVO_TRAMO
        for i in en_cuarentena([s.texto for s in segmentos]):
            salida.setdefault(i, MOTIVO_RESERVADO)
        return salida

    def aplicar(self, segmentos: Sequence[S]) -> list[S]:
        """Los segmentos que se pueden ensenar; los demas quedan anotados en `ocultos`."""
        motivos = self.motivos(segmentos)
        for i, motivo in motivos.items():
            s = segmentos[i]
            self.ocultos.setdefault(s.n, Oculto(self.video_id, s.n, s.t0_ms, s.t1_ms, motivo))
        return [s for i, s in enumerate(segmentos) if i not in motivos]

    def ocultos_entre(self, a_ms: int, b_ms: int) -> list[Oculto]:
        return [o for o in self.ocultos.values() if _toca(o.t0_ms, o.t1_ms, a_ms, b_ms)]


def filtros(repo: Path) -> dict[str, Filtro]:
    """Un `Filtro` por video con los tramos del repositorio; el de un video sin tramos se crea al
    pedirlo con `filtro_de`."""
    return {v: Filtro(v, ts) for v, ts in cargar_tramos_no_citables(repo).items()}


def filtro_de(repo: Path, video_id: str) -> Filtro:
    return Filtro(video_id, cargar_tramos_no_citables(repo).get(video_id, ()))


DIRECTORIO_PROPUESTAS = "knowledge/_proposals"
# La lista que lee la guardia de Claude Code: CALCULADA por `propuestas_con_ocultos`, escrita por
# `scripts/propuestas_con_ocultos.py --escribir` y vigilada por `tests/unit/test_cuarentena.py`,
# que falla si no coincide con lo que se calcula hoy (orden del consultor del 2026-10-01).
FICHERO_PROPUESTAS_OCULTAS = ".claude/hooks/propuestas_con_ocultos.txt"


@dataclass(frozen=True, slots=True)
class _SegmentoDePropuesta:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str


def propuestas_con_ocultos(repo: Path) -> dict[str, Counter[str]]:
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
        cuenta = Counter(Filtro(video, tramos.get(video, ())).motivos(segmentos).values())
        if cuenta:
            salida[ruta.name] = cuenta
    return salida


def texto_de_la_lista(propuestas: Iterable[str]) -> str:
    """El fichero que lee la guardia: una cabecera que dice de donde sale, y un nombre por linea."""
    cabecera = (
        "# GENERADO por `uv run python scripts/propuestas_con_ocultos.py --escribir` desde\n"
        "# `botsito.corpus.cuarentena.propuestas_con_ocultos`: las propuestas de\n"
        "# knowledge/_proposals/ con algun segmento oculto (sesion en cuarentena, tramo no\n"
        "# citable o material reservado o sin sortear). No se edita a mano:\n"
        "# tests/unit/test_cuarentena.py falla si no coincide con lo que se calcula. La guardia\n"
        "# de Claude Code no deja leerlas.\n"
    )
    return cabecera + "".join(f"{p}\n" for p in sorted(propuestas))


def resumen(ocultos: Iterable[Oculto]) -> str:
    """Cuantos se ocultaron y por que, en una linea; vacio si ninguno. Solo numeros y motivos:
    nunca un texto, una fecha ni el mes o el dia que disparo la regla."""
    cuenta = Counter(o.motivo for o in ocultos)
    if not cuenta:
        return ""
    partes = [f"{cuenta[m]} por {MOTIVOS[m]} ({m})" for m in sorted(cuenta)]
    return (
        f"OCULTOS: {sum(cuenta.values())} segmentos: {', '.join(partes)}. Su contenido no se "
        "ensena; con --crudo, solo Aleks en su propia terminal."
    )
