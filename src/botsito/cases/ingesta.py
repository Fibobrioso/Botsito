"""La ingesta del detalle por operacion (F14a, ADR-0037).

Convierte las filas de un backtest del trader en CASOS, uno por dia, bajo
`knowledge/cases/dev/`. Lo que el trader DICE vive en `knowledge/feedback/` como `LABEL_CASE`; lo
que el trader HIZO vive aqui. No son el mismo objeto: uno es testimonio -solo-anadir, id por hash-
y el otro es derivado -versionado, cita `Fuente:`, se recalcula del material y del reparto-.

**QUE DIAS SE INGIEREN: NO SE ELIGEN, SE DERIVAN.** No hay `--dias`, ni `--mes`, ni `--desde`. El
conjunto es

    dias pedidos  =  (casos en un reparto COMMITEADO)  -  casos_reservados(repo)

y un humano no puede ampliarlo. Tres negativas duras:

- un dia que no este en NINGUN reparto **aborta el comando entero**, no se salta: asi no se puede
  ingerir un mes antes de su sorteo;
- un dia reservado se descarta **sin escribirse en ningun sitio y sin nombrarse en la salida**;
- si un reparto no se puede leer, `casos_reservados` lanza y el comando falla: un mapa a medias es
  indistinguible de uno completo.

**EL OBJETIVO NO ES UN CAMPO.** El objetivo del trader es una REGLA -`objetivo_rr` con su
`base_calculo_objetivo`, 1:3, con cita literal en `ev-v2-001658-d02fb71a`- y el xlsx no registra el
objetivo planeado: `maxTP` solo existe cuando la operacion gano y `idealTP` cae del lado de la
perdida en 4 de 47 filas. Un campo opcional vacio seria una invitacion a que alguien lo rellenara
con `maxTP` dentro de seis meses, asi que **el campo no existe**. Quitar el campo ES el mecanismo
(ADR-0037, decision 7 y su correccion).
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.cases.holdout import casos_reservados, repartos_commiteables
from botsito.comun.historial import commit_que_anadio
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.corpus.libro import PESTANA_OPERACIONES, LibroError, filas_de_los_dias

DIRECTORIO_DEV = "knowledge/cases/dev"
PESTANA = PESTANA_OPERACIONES
# Las CUATRO columnas que entran, y en este orden: la primera es el instante, que es de la unica
# sin la cual nada se puede trocear por dia. Todo lo demas del libro -resultado, PnL, RR, ids,
# `idealTP`- se descarta y no se escribe en ningun sitio.
COLUMNAS = ("dateStart", "side", "entryPrice", "initialSL")
# `dateStart` viene en UTC: medido sobre agosto, convertido a `huso_operativa` las 47 operaciones
# caen dentro de las dos sesiones H4 declaradas; leido como hora local, 16 quedarian fuera.
HUSO_DEL_FICHERO = "UTC"
_DIRECCION = {"buy": "compra", "sell": "venta"}
_CASO = re.compile(r"^caso-[a-z0-9]+-(\d{4}-\d{2}-\d{2})$", re.ASCII)


class IngestaError(ValueError):
    """La ingesta no se puede hacer con lo que hay. Nunca nombra un dia reservado."""


@dataclass(frozen=True)
class Operacion:
    instante_utc: str
    sesion: str
    direccion: str
    entrada: Decimal
    stop: Decimal


@dataclass(frozen=True)
class Resultado:
    casos: dict[str, list[Operacion]]
    sin_stop: int
    filas_leidas: int


def dias_ingeribles(repo: Path) -> dict[str, str]:
    """`dia -> id de caso` de todo caso repartido, commiteado y NO reservado.

    El reparto tiene que estar COMMITEADO: `repartos_commiteables` globea el arbol de trabajo, asi
    que un `particiones.yaml` sin commitear podria marcar un dia como `dev` y hacerlo ingerible.
    Es el mismo criterio que `anterioridad.problemas_de_anterioridad` ya aplica.
    """
    reservados = casos_reservados(repo)  # lanza si un reparto es ilegible: falla cerrado
    salida: dict[str, str] = {}
    for fichero in repartos_commiteables(repo):
        ruta = fichero.relative_to(repo).as_posix()
        if commit_que_anadio(repo, ruta) is None:
            continue  # sin commitear no reparte nada
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError) as exc:  # pragma: no cover - lo cubre casos_reservados
            raise IngestaError(f"{ruta}: {exc}") from exc
        for caso in (doc.get("asignacion") or {}) if isinstance(doc, dict) else {}:
            m = _CASO.match(str(caso))
            if m is not None and str(caso) not in reservados:
                salida[m.group(1)] = str(caso)
    return salida


def _decimal(valor: object, fila: str, columna: str) -> Decimal:
    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise IngestaError(f"fila {fila}: {columna} ilegible") from exc


def _sesion_de(
    instante_utc: str, huso: str, sesiones: Sequence[tuple[str, str, str]]
) -> str | None:
    local = datetime.fromisoformat(instante_utc).astimezone(ZoneInfo(huso))
    hhmm = local.strftime("%H:%M")
    for nombre, desde, hasta in sesiones:
        if desde <= hhmm < hasta:
            return nombre
    return None


def ingerir(
    repo: Path,
    material: Path,
    huso_operativa: str,
    sesiones: Sequence[tuple[str, str, str]],
    dias: Iterable[str] | None = None,
) -> Resultado:
    """Las operaciones de los dias ingeribles, agrupadas por dia. No escribe nada.

    `dias` solo se pasa en tests: en produccion se derivan con `dias_ingeribles`.
    """
    pedidos = dict.fromkeys(dias) if dias is not None else dias_ingeribles(repo)
    if not pedidos:
        raise IngestaError(
            "no hay ningun dia ingerible: o no hay reparto commiteado, o todos sus casos estan "
            "reservados"
        )
    try:
        filas = filas_de_los_dias(material, pedidos, PESTANA, COLUMNAS, HUSO_DEL_FICHERO)
    except LibroError as exc:
        raise IngestaError(str(exc)) from exc

    casos: dict[str, list[Operacion]] = {d: [] for d in pedidos}
    sin_stop = 0
    for fila in filas:
        n = str(fila.get("_fila"))
        lado = str(fila.get("side") or "")
        if lado not in _DIRECCION:
            raise IngestaError(f"fila {n}: `side` no es buy ni sell")
        if not fila.get("initialSL"):
            # Una fila sin stop NO produce caso. Se CUENTA, y quien llama lo dice: un caso que
            # desaparece sin constancia es el defecto que a la sesion 1 le costo dos dias.
            sin_stop += 1
            continue
        entrada = _decimal(fila["entryPrice"], n, "entryPrice")
        stop = _decimal(fila["initialSL"], n, "initialSL")
        # EL INVARIANTE GEOMETRICO, guardia permanente: caza un intercambio de columnas, que es el
        # fallo silencioso que mas caro sale. Y es el que cazo que `idealTP` no era el objetivo.
        bien = stop < entrada if lado == "buy" else stop > entrada
        if not bien:
            raise IngestaError(
                f"fila {n}: con `side` {lado} el stop {stop} esta del lado equivocado de la "
                f"entrada {entrada}. O las columnas estan intercambiadas o el material no es el "
                f"que se cree"
            )
        instante = str(fila["_instante_utc"])
        sesion = _sesion_de(instante, huso_operativa, sesiones)
        if sesion is None:
            raise IngestaError(
                f"fila {n}: su apertura no cae en ninguna sesion declarada. La asignacion a sesion "
                f"H4 depende del huso, y sin ella la unidad de fidelidad no existe"
            )
        dia = datetime.fromisoformat(instante).astimezone(ZoneInfo(huso_operativa)).date()
        casos.setdefault(dia.isoformat(), []).append(
            Operacion(instante, sesion, _DIRECCION[lado], entrada, stop)
        )
    return Resultado(casos, sin_stop, len(filas))
