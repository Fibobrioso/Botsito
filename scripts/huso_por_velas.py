"""El huso de un libro del trader, MEDIDO POR VELAS (ADR-0039 §5). Herramienta, no medida a mano.

Hasta el 2026-09-24 el procedimiento de §5 se ejecutaba a mano (mayo, con agosto y abril de
control: docs/validation/MAYO-DEV.md). Marzo lo necesita en el paso c del orden de ADR-0046 §6, y
una medida que decide como se lee un libro para siempre -libros.yaml es solo anadir- no puede
depender de repetir a mano lo que se hizo una vez. Esto es §5, sin interpretarlo:

- la entrada de cada fila esta DENTRO si cae en [minima - margen, maxima + margen] puntos de la
  vela M1 de Dukascopy del minuto de su instante (hacia abajo: el libro trae segundos);
- el instante se lee con los DOS husos de la configuracion (UTC y el alternativo);
- SOLO filas legibles -fecha que casa con el formato, entrada que es un numero-, y SOLO de dias
  `dev` cuyo dia sale IGUAL con los dos husos. De las demas sale un booleano y nada mas;
- decide un huso si da >= `umbral_decide` Y el otro <= `umbral_otro`; si no, NO CONCLUYENTE.

TODAS las cifras y los husos se leen de `knowledge/corpus/criterio_huso.yaml` (ADR-0002). Los dias
`dev` salen de los repartos COMMITEADOS -`dev` y `fidelidad-dev`, menos `casos_ocultos`-, nunca de
la linea de comandos. El libro se abre SOLO con el lector unico (`corpus.libro`), con una
declaracion en memoria por huso: la hipotesis que se mide, no una declaracion.

CONTROL (§5, «si el control no sale, el metodo no sirve»): con un libro ya declarado, la
herramienta lo mide igual y dice si su veredicto COINCIDE con el huso declarado; si no, sale con
codigo 3 y no se sigue.

    uv run python scripts/huso_por_velas.py --libro <xlsx> --mes AAAA-MM --salida <fichero>
        [--formato "AAAA-MM-DD HH:MM:SS"]   # obligatorio si el libro no esta declarado

Imprime SOLO recuentos y tasas: ni fechas, ni instantes, ni precios.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

RAIZ = Path(__file__).resolve().parents[1]
FICHERO_CRITERIO = "knowledge/corpus/criterio_huso.yaml"
# Las particiones cuyas filas se pueden leer para medir: las de DESARROLLO de los dos caminos. Lista
# cerrada: una particion nueva no entra por no estar en la lista de reservadas.
PARTICIONES_DEV = ("dev", "fidelidad-dev")
# Solo las dos columnas que la medida necesita: el instante y la entrada.
COLUMNAS = ("dateStart", "entryPrice")
NO_CONCLUYENTE = "NO CONCLUYENTE"
CONTROL_FALLA = 3
_CASO = re.compile(r"^caso-[a-z0-9]+-(\d{4}-\d{2}-\d{2})$", re.ASCII)
_MES = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$", re.ASCII)


class HusoError(ValueError):
    """La medida no se puede hacer con lo que hay. Nunca nombra un dia ni una fila."""


@dataclass(frozen=True)
class Criterio:
    margen_puntos: int
    husos: tuple[str, str]
    umbral_decide: Decimal
    umbral_otro: Decimal


@dataclass(frozen=True)
class Fila:
    """Una fila comparable: su instante UTC leido con cada huso, y su entrada."""

    instantes: Mapping[str, datetime]
    entrada: Decimal


@dataclass(frozen=True)
class Rango:
    minima: int
    maxima: int
    escala: int  # puntos por unidad de precio: del dataset, no de aqui


@dataclass(frozen=True)
class Comparables:
    filas: list[Fila]
    # Hubo filas de dias `dev` que con un huso caen en un dia y con el otro en otro -o fuera de los
    # pedidos-. De ellas sale SOLO esto: un booleano (ADR-0039 §5).
    frontera: bool
    # Filas comparables cuya entrada no es un numero: no se pueden medir.
    sin_entrada: int


def _umbral(valor: Any, clave: str, nombre: str) -> Decimal:
    if not isinstance(valor, str):
        raise HusoError(f'{nombre}: `{clave}` va como texto decimal, p. ej. "0.90"')
    try:
        d = Decimal(valor)
    except InvalidOperation as exc:
        raise HusoError(f"{nombre}: `{clave}` no es un decimal") from exc
    if not d.is_finite() or d < 0 or d > 1:
        raise HusoError(f"{nombre}: `{clave}` es una fraccion entre 0 y 1")
    return d


def criterio_desde_doc(doc: Any, nombre: str) -> Criterio:
    """Lectura ESTRICTA: las cinco claves exactas, y ninguna cifra por defecto."""
    claves = {"adr", "margen_puntos", "husos", "umbral_decide", "umbral_otro"}
    if not isinstance(doc, dict) or set(doc) != claves:
        raise HusoError(f"{nombre}: claves {sorted(claves)}, exactamente")
    margen = doc["margen_puntos"]
    if isinstance(margen, bool) or not isinstance(margen, int) or margen < 0:
        raise HusoError(f"{nombre}: `margen_puntos` es un entero >= 0")
    husos = doc["husos"]
    if not isinstance(husos, list):
        raise HusoError(f"{nombre}: `husos` son exactamente dos husos distintos")
    try:
        # Desempaquetar en dos nombres ES la regla: exactamente dos husos.
        primero, segundo = (str(h) for h in husos)
    except (TypeError, ValueError) as exc:
        raise HusoError(f"{nombre}: `husos` son exactamente dos husos distintos") from exc
    if primero == segundo:
        raise HusoError(f"{nombre}: `husos` son exactamente dos husos distintos")
    for h in (primero, segundo):
        try:
            ZoneInfo(h)
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise HusoError(f"{nombre}: huso {h!r} desconocido") from exc
    decide = _umbral(doc["umbral_decide"], "umbral_decide", nombre)
    otro = _umbral(doc["umbral_otro"], "umbral_otro", nombre)
    if otro >= decide:
        raise HusoError(f"{nombre}: `umbral_otro` tiene que quedar por debajo de `umbral_decide`")
    return Criterio(margen, (primero, segundo), decide, otro)


def cargar_criterio(repo: Path) -> Criterio:
    sys.path.insert(0, str(repo / "src"))
    from botsito.comun.yaml_estricto import YamlError, leer_yaml

    ruta = repo / FICHERO_CRITERIO
    try:
        return criterio_desde_doc(leer_yaml(ruta), FICHERO_CRITERIO)
    except (OSError, YamlError) as exc:
        raise HusoError(f"{FICHERO_CRITERIO}: {exc}") from exc


def comparables(
    lecturas: Mapping[str, Sequence[Mapping[str, str | None]]], husos: tuple[str, str]
) -> Comparables:
    """Las filas que el lector devuelve con LOS DOS husos y con el MISMO `_dia` en los dos.

    Una fila se reconoce por su texto crudo -`dateStart` y `entryPrice`-, que no depende del huso:
    su dia con cada huso depende solo de ese texto. Una fila que solo sale con un huso, o con dias
    distintos, es de frontera y se descarta: puede ser, con el otro huso, de un dia reservado.
    """
    a, b = husos
    por_huso: dict[str, dict[tuple[str, str], list[Mapping[str, str | None]]]] = {
        h: defaultdict(list) for h in husos
    }
    for h in husos:
        for fila in lecturas[h]:
            clave = (str(fila.get("dateStart")), str(fila.get("entryPrice")))
            por_huso[h][clave].append(fila)
    frontera = False
    sin_entrada = 0
    filas: list[Fila] = []
    for clave in sorted(set(por_huso[a]) | set(por_huso[b])):
        fa, fb = por_huso[a].get(clave, []), por_huso[b].get(clave, [])
        dias_a = {str(f.get("_dia")) for f in fa}
        dias_b = {str(f.get("_dia")) for f in fb}
        if not fa or len(fa) != len(fb) or dias_a != dias_b:
            frontera = True
            continue
        for x, y in zip(fa, fb, strict=True):
            try:
                entrada = Decimal(str(x.get("entryPrice")))
            except InvalidOperation:
                sin_entrada += 1
                continue
            if not entrada.is_finite():
                sin_entrada += 1
                continue
            filas.append(
                Fila(
                    {
                        a: datetime.fromisoformat(str(x["_instante_utc"])),
                        b: datetime.fromisoformat(str(y["_instante_utc"])),
                    },
                    entrada,
                )
            )
    return Comparables(filas, frontera, sin_entrada)


def minuto(instante: datetime) -> datetime:
    return instante.replace(second=0, microsecond=0)


def medir(
    filas: Sequence[Fila],
    vela_de: Callable[[datetime], Rango | None],
    criterio: Criterio,
) -> dict[str, tuple[int, int, int]]:
    """`huso -> (dentro, total, sin vela)`. Puro: la vela la da quien llama. Una fila sin vela
    cuenta en el total y no dentro, como en la medida a mano."""
    cuenta: dict[str, tuple[int, int, int]] = {}
    for h in criterio.husos:
        dentro = total = sin_vela = 0
        for fila in filas:
            total += 1
            vela = vela_de(minuto(fila.instantes[h]))
            if vela is None:
                sin_vela += 1
                continue
            puntos = int(fila.entrada * vela.escala)
            m = criterio.margen_puntos
            if vela.minima - m <= puntos <= vela.maxima + m:
                dentro += 1
        cuenta[h] = (dentro, total, sin_vela)
    return cuenta


def decidir(cuenta: Mapping[str, tuple[int, int, int]], criterio: Criterio) -> str:
    """§5 literal: un huso >= umbral_decide Y el otro <= umbral_otro. Si no, NO CONCLUYENTE."""
    a, b = criterio.husos
    if cuenta[a][1] == 0:
        return NO_CONCLUYENTE
    tasa = {h: Decimal(cuenta[h][0]) / Decimal(cuenta[h][1]) for h in (a, b)}
    for uno, otro in ((a, b), (b, a)):
        if tasa[uno] >= criterio.umbral_decide and tasa[otro] <= criterio.umbral_otro:
            return uno
    return NO_CONCLUYENTE


def dias_dev(repo: Path, mes: str) -> set[str]:
    """Los dias `dev` y `fidelidad-dev` de `mes` en repartos COMMITEADOS, menos los ocultos."""
    sys.path.insert(0, str(repo / "src"))
    from botsito.cases.holdout import casos_ocultos, repartos_commiteables
    from botsito.comun.historial import commit_que_anadio
    from botsito.comun.yaml_estricto import YamlError, leer_yaml

    ocultos = casos_ocultos(repo)
    dias: set[str] = set()
    for fichero in repartos_commiteables(repo):
        if commit_que_anadio(repo, fichero.relative_to(repo).as_posix()) is None:
            continue
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError) as exc:
            raise HusoError(f"{fichero.relative_to(repo).as_posix()}: {exc}") from exc
        asignacion = doc.get("asignacion") if isinstance(doc, dict) else None
        for caso, particion in (asignacion or {}).items():
            m = _CASO.match(str(caso))
            if m is None or particion not in PARTICIONES_DEV or str(caso) in ocultos:
                continue
            if m.group(1)[:7] == mes:
                dias.add(m.group(1))
    return dias


@dataclass(frozen=True)
class Informe:
    sha: str
    formato: str
    declarado: str | None  # el huso declarado en libros.yaml, si el libro es un control
    dias: int
    comparables: Comparables
    cuenta: dict[str, tuple[int, int, int]]
    veredicto: str

    @property
    def coincide(self) -> bool | None:
        return None if self.declarado is None else self.veredicto == self.declarado


def medir_libro(
    repo: Path,
    libro: Path,
    mes: str,
    formato: str | None,
    vela_de: Callable[[datetime], Rango | None],
) -> Informe:
    """Todo menos las series: las pone quien llama (las reales, o sinteticas en los tests)."""
    sys.path.insert(0, str(repo / "src"))
    from botsito.config.registro import cargar_registro
    from botsito.corpus.libro import PESTANA_OPERACIONES, LibroError, filas_de_los_dias
    from botsito.corpus.libros import (
        FORMATOS,
        Declaracion,
        Lectura,
        LibrosError,
        cargar_libros,
        sha256_de,
    )

    if not _MES.match(mes):
        raise HusoError(f"--mes {mes!r} no es AAAA-MM")
    criterio = cargar_criterio(repo)
    try:
        sha = sha256_de(libro)
        declaracion = cargar_libros(repo).get(sha)
    except (OSError, LibrosError) as exc:
        raise HusoError(str(exc)) from exc
    declarado: str | None = None
    if declaracion is not None:
        formatos = {lec.formato for lec in declaracion.lecturas}
        husos = {lec.huso for lec in declaracion.lecturas}
        if len(formatos) != 1 or len(husos) != 1:
            raise HusoError("el libro declarado tiene mas de una lectura: no es un control simple")
        (declarado_formato,) = formatos
        (declarado,) = husos
        if formato is not None and formato != declarado_formato:
            raise HusoError(
                f"--formato {formato!r} no es el declarado para este libro ({declarado_formato!r})"
            )
        formato = declarado_formato
    if formato is None:
        raise HusoError("el libro no esta declarado: --formato es obligatorio")
    if formato not in FORMATOS:
        raise HusoError(f"--formato {formato!r} fuera del vocabulario {sorted(FORMATOS)}")
    dias = dias_dev(repo, mes)
    if not dias:
        raise HusoError(f"{mes} no tiene ningun dia `dev` en un reparto commiteado: nada que medir")
    huso_de_los_dias = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml").texto(
        "huso_operativa"
    )
    lecturas: dict[str, list[dict[str, str | None]]] = {}
    for huso in criterio.husos:
        hipotesis = Declaracion(sha, (Lectura(formato, huso),))
        try:
            lecturas[huso] = filas_de_los_dias(
                libro,
                dias,
                PESTANA_OPERACIONES,
                COLUMNAS,
                hipotesis,
                huso_de_los_dias=huso_de_los_dias,
            )
        except LibroError as exc:
            raise HusoError(str(exc)) from exc
    comp = comparables(lecturas, criterio.husos)
    cuenta = medir(comp.filas, vela_de, criterio)
    return Informe(sha, formato, declarado, len(dias), comp, cuenta, decidir(cuenta, criterio))


def lineas(informe: Informe, criterio: Criterio, datasets: Sequence[str] = ()) -> list[str]:
    salida = [
        f"LIBRO: {informe.sha[:12]}... formato {informe.formato!r}",
        f"CRITERIO: {FICHERO_CRITERIO} (margen {criterio.margen_puntos} puntos; decide >= "
        f"{criterio.umbral_decide} y el otro <= {criterio.umbral_otro})",
    ]
    if datasets:
        salida.append(f"DATASETS: {', '.join(datasets)}")
    comp = informe.comparables
    salida += [
        f"DIAS dev: {informe.dias}",
        f"FILAS comparables: {len(comp.filas)}; sin entrada numerica: {comp.sin_entrada}; "
        f"descartadas por frontera de dia: {'si' if comp.frontera else 'no'}",
    ]
    for huso in criterio.husos:
        d, n, s = informe.cuenta[huso]
        tasa = f"{Decimal(100 * d) / Decimal(n):.1f} %" if n else "-"
        sin = f" ({s} sin vela)" if s else ""
        salida.append(f"{huso}: {d}/{n} = {tasa}{sin}")
    salida.append(f"== VEREDICTO (ADR-0039 §5): {informe.veredicto}")
    if informe.declarado is not None:
        que = "COINCIDE" if informe.coincide else "NO COINCIDE: el metodo no sirve, se para"
        salida.append(f"== CONTROL: declarado {informe.declarado} -> {que}")
    return salida


def main(argv: Sequence[str]) -> int:
    p = argparse.ArgumentParser(prog="huso_por_velas.py", description=__doc__.splitlines()[0])
    p.add_argument("--libro", required=True)
    p.add_argument("--mes", required=True)
    p.add_argument("--salida", required=True)
    p.add_argument("--formato")
    args = p.parse_args(list(argv))
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases.fidelidad import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie
    from botsito.data.velas import a_minuto

    datos = carpeta_datos(RAIZ)
    prefijo = cargar_config(RAIZ).dataset_prefijo
    series: dict[str, tuple[dict[int, Rango], str]] = {}

    def vela_de(instante: datetime) -> Rango | None:
        mes = instante.strftime("%Y-%m")
        if mes not in series:
            ruta = buscar_manifiesto(RAIZ, f"{prefijo}{mes}")
            s = cargar_serie(cargar_manifiesto(ruta), datos)
            series[mes] = (
                {int(v.inicio): Rango(int(v.minima), int(v.maxima), s.escala) for v in s.velas},
                ruta.stem,
            )
        return series[mes][0].get(int(a_minuto(instante)))

    try:
        criterio = cargar_criterio(RAIZ)
        informe = medir_libro(RAIZ, Path(args.libro), args.mes, args.formato, vela_de)
    except HusoError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    datasets = [series[m][1] for m in sorted(series)]
    texto = "\n".join(lineas(informe, criterio, datasets)) + "\n"
    Path(args.salida).write_text(texto, encoding="utf-8", newline="\n")
    print(texto, end="")
    return CONTROL_FALLA if informe.coincide is False else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
