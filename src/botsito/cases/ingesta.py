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

**EL CERO SIGNIFICA UNA SOLA COSA, Y ESO ES LO QUE LA PUERTA COMPRA** (2026-09-21). Hasta hoy
un dia que no producia filas podia ser dos cosas incompatibles -«el trader miro y no opero», que
es UN DATO SUYO, y «este mes no tiene material», que es AUSENCIA DE CONOCIMIENTO- y las dos daban
exactamente el mismo silencio. El dia que alguien decida que un dia sin filas produce un
`no_trade`, esa decision convertiria la segunda en la primera sin que nadie lo viera: fabricar una
etiqueta del trader donde no hay material. Por eso:

- un dia cuyo mes NO este declarado en `cobertura_material`, o lo este con CERO tramos, **no es
  ingerible**: se descarta nombrando el MES y el motivo, nunca los dias;
- si un mes pedido no tiene NI UNA FILA en el xlsx que se ha pasado, es **error** y se nombra el
  mes: `--material` recibe un libro y la ingesta nunca busca fichero por mes, asi que pasarle el
  de mayo y pedirle dias de septiembre daba ceros en silencio;
- y despues de la puerta, un dia ingerible sin filas significa exactamente UNA cosa -el material
  cubre ese dia y no hay operaciones-, asi que se **cuenta y se dice**, como ya se hacia con las
  filas sin `initialSL`.

Lo que NO se decide aqui: si ese dia produce un caso `no_trade` o no produce nada. Hoy no produce
nada y asi se queda; toca la forma del caso y roza «un dia sin ninguna operacion ES su etiqueta».
Lo que esta rama aporta es que, cuando se tome, se tomara sobre un conjunto donde el cero ya no es
ambiguo.

**EL OBJETIVO NO ES UN CAMPO.** El objetivo del trader es una REGLA -`objetivo_rr` con su
`base_calculo_objetivo`, 1:3, con cita literal en `ev-v2-001658-d02fb71a`- y el xlsx no registra el
objetivo planeado: `maxTP` solo existe cuando la operacion gano y `idealTP` cae del lado de la
perdida en 4 de 47 filas. Un campo opcional vacio seria una invitacion a que alguien lo rellenara
con `maxTP` dentro de seis meses, asi que **el campo no existe**. Quitar el campo ES el mecanismo
(ADR-0037, decision 7 y su correccion).
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
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
class Ingeribles:
    """Lo que la puerta deja pasar, y lo que niega POR MES y nunca por dia."""

    dias: dict[str, str]
    # mes -> (cuantos dias se niegan, motivo). Nunca la lista de dias: un dia laborable que no
    # aparece ES su etiqueta, y publicarlo seria abrir por la puerta de atras (ADR-0036, ADR-0037).
    negados: dict[str, tuple[int, str]]


@dataclass(frozen=True)
class Resultado:
    casos: dict[str, list[Operacion]]
    sin_stop: int
    filas_leidas: int
    # Dias ingeribles que el material cubre y en los que el trader no opero. Despues de la puerta
    # esto significa UNA sola cosa, y por eso se puede contar sin mentir.
    sin_operaciones: int = 0


def dias_ingeribles(
    repo: Path, cobertura: Mapping[str, Sequence[tuple[str, str]]] | None = None
) -> Ingeribles:
    """`dia -> id de caso` de todo caso repartido, commiteado, NO reservado y CON MATERIAL.

    El reparto tiene que estar COMMITEADO: `repartos_commiteables` globea el arbol de trabajo, asi
    que un `particiones.yaml` sin commitear podria marcar un dia como `dev` y hacerlo ingerible.
    Es el mismo criterio que `anterioridad.problemas_de_anterioridad` ya aplica.

    **LA PUERTA DEL MATERIAL** (2026-09-21): `cobertura` es el `cobertura_material` del camino, y
    un dia cuyo mes no este declarado -o lo este con cero tramos- NO es ingerible. No lanza: los
    niega y los DEVUELVE CONTADOS POR MES, porque negarlos lanzando dejaria el comando inservible
    mientras junio siga repartido, y negarlos en silencio es el defecto que esto viene a cerrar.
    Con `cobertura` en None no hay puerta, que es lo que necesitan los tests de lo demas.
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
    if cobertura is None:
        return Ingeribles(salida, {})
    negados: dict[str, tuple[int, str]] = {}
    for dia in sorted(salida):
        mes = dia[:7]
        tramos = cobertura.get(mes)
        if tramos is None:
            motivo = f"{mes} no esta declarado en cobertura_material: no consta que haya material"
        elif not tramos:
            motivo = f"{mes} esta declarado con CERO tramos: no hay material del trader"
        else:
            continue
        n, _ = negados.get(mes, (0, motivo))
        negados[mes] = (n + 1, motivo)
    for dia in [d for d in salida if d[:7] in negados]:
        del salida[dia]
    return Ingeribles(salida, negados)


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
    pedidos = dict.fromkeys(dias) if dias is not None else dias_ingeribles(repo).dias
    if not pedidos:
        raise IngestaError(
            "no hay ningun dia ingerible: o no hay reparto commiteado, o todos sus casos estan "
            "reservados"
        )
    try:
        filas = filas_de_los_dias(material, pedidos, PESTANA, COLUMNAS, HUSO_DEL_FICHERO)
    except LibroError as exc:
        raise IngestaError(str(exc)) from exc

    # LA REGLA POR MES, no por dia: si un mes pedido no tiene NI UNA fila en el libro que se ha
    # pasado, el libro no es el suyo y decirlo cuesta una linea. Habla del FICHERO -"el material
    # que me has dado"- y no de los dias del trader, asi que no publica calendario. Un dia
    # concreto sin filas dentro de un mes que SI tiene es otra cosa, y es la que si tiene sentido.
    meses_pedidos = {d[:7] for d in pedidos}
    meses_con_filas = {str(f["_instante_utc"])[:7] for f in filas}
    vacios = sorted(meses_pedidos - meses_con_filas)
    if vacios:
        raise IngestaError(
            f"el material que se ha pasado no tiene ni una fila de {', '.join(vacios)}: o es el "
            f"libro de otro mes, o falta. No se escribe nada, porque un cero de aqui no se puede "
            f"distinguir de un dia sin operaciones"
        )

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
    # Despues de la puerta y de la regla por mes, esto significa UNA cosa: el material cubre ese
    # dia y el trader no opero. Se cuenta, y quien llama lo dice.
    sin_operaciones = sum(1 for d in pedidos if not casos.get(d))
    return Resultado(casos, sin_stop, len(filas), sin_operaciones)
