"""Ventanas de replay para el etiquetado ciego (F10, ADR-0011).

Un caso es el dia operativo del trader (`ventana_local` de `config.yaml` en `huso_operativa`)
sobre un dataset congelado (F15): `dataset_id`, ventana UTC `[desde, hasta)`, velas M1 con su
hash (recomputable con `cargar_ventana`) y los limites de las velas H4 con cada anclaje candidato
(`limites_entre`, ADR-0005). El universo son los dias laborables NO vistos por el trader cuya
ventana completa cae dentro del dataset y tiene suficientes velas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from botsito.comun.documentos import sha256_hex
from botsito.data.agregacion import limites_entre
from botsito.data.dataset import cargar_serie
from botsito.data.velas import a_minuto, escribir_csv, formato_ts
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MinutoUtc, SerieVelas

MINUTOS_H4 = 240


class VentanaError(ValueError):
    """No se puede construir la ventana con lo que hay."""


@dataclass(frozen=True, slots=True)
class Anclaje:
    etiqueta: str
    hora: str
    huso: str
    coincide_con_sesiones: bool

    def hora_local(self) -> HoraLocal:
        return HoraLocal(self.hora, self.huso)


@dataclass(frozen=True, slots=True)
class Caso:
    id: str
    dia: str  # AAAA-MM-DD en el huso del trader
    dataset_id: str
    desde_utc: str  # ISO minuto, sufijo Z
    hasta_utc: str
    n_velas: int
    sha256: str
    limites_h4: dict[str, list[str]]  # etiqueta del anclaje -> limites UTC (ISO)

    def como_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "dia": self.dia,
            "dataset_id": self.dataset_id,
            "desde_utc": self.desde_utc,
            "hasta_utc": self.hasta_utc,
            "n_velas": self.n_velas,
            "sha256": self.sha256,
            "limites_h4": {k: list(v) for k, v in self.limites_h4.items()},
        }


@dataclass(frozen=True, slots=True)
class Excluido:
    dia: str
    motivo: str


def _minuto(dia: date, hora: str, huso: ZoneInfo) -> MinutoUtc:
    hh, mm = (int(x) for x in hora.split(":"))
    local = datetime.combine(dia, time(hh, mm), tzinfo=huso)
    return a_minuto(local.astimezone(UTC))


def id_caso(simbolo: str, dia: date) -> str:
    return f"caso-{simbolo.lower()}-{dia.isoformat()}"


def _iso(minuto: MinutoUtc | int) -> str:
    return formato_ts(minuto)


def dias_laborables(desde: date, hasta: date) -> list[date]:
    salida: list[date] = []
    d = desde
    while d <= hasta:
        if d.weekday() < 5:
            salida.append(d)
        d += timedelta(days=1)
    return salida


def hash_ventana(serie: SerieVelas, desde: MinutoUtc, hasta: MinutoUtc) -> tuple[int, str]:
    """(n_velas, sha256) de las velas M1 de `serie` en `[desde, hasta)`, en el CSV canonico."""
    velas = [v for v in serie.velas if desde <= v.inicio < hasta]
    return len(velas), sha256_hex(escribir_csv(velas).encode("utf-8"))


def construir_caso(
    serie: SerieVelas,
    dia: date,
    simbolo: str,
    huso_operativa: str,
    ventana_local: tuple[str, str],
    anclajes: list[Anclaje],
    min_velas: int,
) -> Caso | Excluido:
    """El caso del dia, o el motivo por el que queda fuera del universo."""
    huso = ZoneInfo(huso_operativa)
    desde = _minuto(dia, ventana_local[0], huso)
    hasta = _minuto(dia, ventana_local[1], huso)
    if hasta <= desde:
        raise VentanaError("la ventana local debe acabar despues de empezar")
    if not serie.velas:
        return Excluido(dia.isoformat(), "dataset sin velas")
    primera, ultima = serie.velas[0].inicio, serie.velas[-1].inicio
    if desde < primera or hasta - 1 > ultima:
        return Excluido(
            dia.isoformat(),
            f"ventana [{_iso(desde)}, {_iso(hasta)}) fuera del dataset "
            f"[{_iso(primera)}, {_iso(ultima)}]",
        )
    n, sha = hash_ventana(serie, desde, hasta)
    if n < min_velas:
        return Excluido(dia.isoformat(), f"{n} velas < {min_velas}")
    limites = {
        a.etiqueta: [_iso(x) for x in limites_entre(desde, hasta, MINUTOS_H4, a.hora_local())]
        for a in anclajes
    }
    return Caso(
        id_caso(simbolo, dia),
        dia.isoformat(),
        serie.origen or "",
        _iso(desde),
        _iso(hasta),
        n,
        sha,
        limites,
    )


def universo(
    manifiestos: list[dict[str, Any]],
    carpeta_datos: Path,
    simbolo: str,
    huso_operativa: str,
    ventana_local: tuple[str, str],
    anclajes: list[Anclaje],
    min_velas: int,
    meses_vistos: set[str],
    dias_vistos: set[str],
) -> tuple[list[Caso], list[Excluido]]:
    """Casos de todos los dias laborables no vistos de los datasets dados (ordenados por dia) y
    los dias excluidos con motivo. Cada dataset se lee UNA vez (hash por fichero)."""
    casos: list[Caso] = []
    excluidos: list[Excluido] = []
    ordenados = sorted(manifiestos, key=lambda x: (str(x["desde"]), str(x["dataset_id"])))
    series = {str(m["dataset_id"]): cargar_serie(m, carpeta_datos) for m in ordenados}
    for k, m in enumerate(ordenados):
        desde = date.fromisoformat(str(m["desde"]))
        hasta = date.fromisoformat(str(m["hasta"]))
        serie = series[str(m["dataset_id"])]
        # El dia operativo empieza la vispera a las 22:00/23:00Z: el mes anterior, si es
        # contiguo, aporta esas velas al primer dia del mes (el caso sigue citando ESTE dataset).
        if k > 0:
            previo = ordenados[k - 1]
            if date.fromisoformat(str(previo["hasta"])) + timedelta(days=1) == desde:
                anterior = series[str(previo["dataset_id"])]
                serie = SerieVelas(
                    serie.simbolo,
                    serie.periodo_min,
                    serie.escala,
                    serie.escala_volumen,
                    tuple(anterior.velas) + tuple(serie.velas),
                    serie.origen,
                )
        for dia in dias_laborables(desde, hasta):
            if dia.isoformat()[:7] in meses_vistos:
                excluidos.append(Excluido(dia.isoformat(), "mes visto por el trader"))
                continue
            if dia.isoformat() in dias_vistos:
                excluidos.append(Excluido(dia.isoformat(), "dia visto por el trader"))
                continue
            resultado = construir_caso(
                serie, dia, simbolo, huso_operativa, ventana_local, anclajes, min_velas
            )
            if isinstance(resultado, Caso):
                casos.append(resultado)
            else:
                excluidos.append(resultado)
    ids_casos = [c.id for c in casos]
    if len(set(ids_casos)) != len(ids_casos):
        raise VentanaError("dos datasets cubren el mismo dia: ids de caso repetidos")
    return casos, excluidos


def recomputar_hash(
    manifiesto: dict[str, Any], carpeta_datos: Path, desde_utc: str, hasta_utc: str
) -> tuple[int, str]:
    """Para `kit check` y F14: (n_velas, sha256) de una ventana ya escrita."""
    from botsito.data.velas import parse_ts

    serie = cargar_serie(manifiesto, carpeta_datos)
    return hash_ventana(serie, parse_ts(desde_utc), parse_ts(hasta_utc))
