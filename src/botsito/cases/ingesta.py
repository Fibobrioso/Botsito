"""La ingesta del detalle por operacion (F14a, ADR-0037).

Convierte las filas de un backtest del trader en CASOS, uno por dia, bajo
`knowledge/cases/dev/`. Lo que el trader DICE vive en `knowledge/feedback/` como `LABEL_CASE`; lo
que el trader HIZO vive aqui. No son el mismo objeto: uno es testimonio -solo-anadir, id por hash-
y el otro es derivado -versionado, cita `Fuente:`, se recalcula del material y del reparto-.

**QUE DIAS SE INGIEREN: NO SE ELIGEN, SE DERIVAN.** No hay `--dias`, ni `--mes`, ni `--desde`. El
conjunto es

    dias pedidos  =  (casos en un reparto COMMITEADO)  -  casos_ocultos(repo)

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
  cubre ese dia y NO HAY NINGUNA FILA EN EL-, asi que se **cuenta y se dice**, como ya se hacia con
  las filas sin `initialSL`. Se dice SIN sujeto humano: de esa ausencia salen dos cosas -que no
  opero, o que opero y la fila no esta en la exportacion- y quedarse con la primera seria
  atribuirle una decision al trader a partir de lo que falta.

**EL LIBRO DICE DE QUE MES ES, Y SOLO SE PIDEN LOS DIAS DE ESE MES** (2026-09-22, rama
`trabajo/mayo-dev-ingerido`). Hasta hoy el mes del material se DEDUCIA de sus filas -la regla de
arriba- y con dos meses ingeribles a la vez el comando no podia ingerir ninguno: pedia los dias de
los dos y el libro de uno solo "no tenia ni una fila" del otro. Ese «falla cerrada» NO ERA LA
PUERTA: era la regla de cobertura protegiendo por coincidencia. Ahora el mes se DECLARA -el
`material_sha256` de cada tramo de `cobertura_material`, copiado del manifiesto del corpus- y
`dias_del_material` lo compara con el sha del `--material` ANTES de leer una fila. Es la deuda que
`trabajo/cobertura-material-del-kit` dejo nombrada en Technical Debt: «declarar el mes del
material en vez de deducirlo de las filas».

**SOLO EL CAMINO DEL KIT.** Los dias del camino de fidelidad (ADR-0036) no los toma este comando:
el brief que los abra no existe todavia (PROJECT_STATE, Next Action), y hasta hoy esa obligacion
solo estaba ESCRITA. Se cuentan -nunca se nombran- y se dice.

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

from botsito.cases.holdout import (
    DIRECTORIO_KIT,
    DIRECTORIO_VISTO,
    casos_ocultos,
    repartos_commiteables,
)
from botsito.comun.historial import commit_que_anadio
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.corpus.inventario import InventarioError, cargar_manifiesto
from botsito.corpus.libro import PESTANA_OPERACIONES, LibroError, filas_de_los_dias
from botsito.corpus.libros import LibrosError, declaracion_de

DIRECTORIO_DEV = "knowledge/cases/dev"
MANIFIESTO_CORPUS = "knowledge/corpus/manifest.yaml"
PESTANA = PESTANA_OPERACIONES
# Las CUATRO columnas que entran, y en este orden: la primera es el instante, que es de la unica
# sin la cual nada se puede trocear por dia. Todo lo demas del libro -resultado, PnL, RR, ids,
# `idealTP`- se descarta y no se escribe en ningun sitio.
COLUMNAS = ("dateStart", "side", "entryPrice", "initialSL")
# El formato y el huso de `dateStart` NO se fijan aqui: los declara cada libro, atados a su sha,
# en `knowledge/corpus/libros.yaml` (ADR-0039). Hasta el 2026-09-22 aqui habia una constante
# `HUSO_DEL_FICHERO = "UTC"`, medida sobre agosto y aplicada a todos los libros.
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
    # Dias no reservados de repartos de OTRO camino (fidelidad). Este comando no los toma: se
    # cuentan para que no desaparezcan en silencio, y no se nombran.
    de_otro_camino: int = 0


def aviso_de_otro_camino(n: int) -> str:
    """La frase que dice que los dias de fidelidad no entran. Por RECUENTO, sin fechas."""
    return (
        f"INGESTA: {n} dias del camino de FIDELIDAD no los toma este comando: sus dias `dev` no "
        f"se abren sin su propio brief (PROJECT_STATE.md, Next Action: «EL BRIEF PARA ABRIR LOS "
        f"4 `dev` DE SEPTIEMBRE [...] no se abre sin el»). No se han leido ni escrito"
    )


@dataclass(frozen=True)
class Resultado:
    casos: dict[str, list[Operacion]]
    sin_stop: int
    filas_leidas: int
    # Dias ingeribles que el material cubre y en los que NO HAY NINGUNA FILA. Se dice asi, sin
    # sujeto humano: de una ausencia salen DOS cosas -que no opero, o que opero y la fila no esta
    # en la exportacion- y quedarse con la primera es atribuirle una decision a una persona a
    # partir de lo que falta, que es justo lo que esta rama existe para impedir.
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
    # OCULTOS (ADR-0041): un retirado no es ingerible. Lanza si un reparto es ilegible.
    reservados = casos_ocultos(repo)
    salida: dict[str, str] = {}
    de_otro_camino: set[str] = set()
    kit = (repo / DIRECTORIO_KIT).resolve()
    visto = (repo / DIRECTORIO_VISTO).resolve()
    # EL REPARTO DEV-VISTO (ADR-0042) solo cuenta si cumple sus condiciones -mes visto, lectura
    # completa declarada, tramo con su libro- y se reproduce y esta anclado. Si no, FALLA CERRADO:
    # un reparto que no deberia existir no puede hacer ingerible nada.
    from botsito.cases import visto as camino_visto

    fallos_visto = camino_visto.problemas(repo)
    if fallos_visto:
        raise IngestaError("reparto dev-visto invalido: " + "; ".join(fallos_visto))
    for fichero in repartos_commiteables(repo):
        ruta = fichero.relative_to(repo).as_posix()
        if commit_que_anadio(repo, ruta) is None:
            continue  # sin commitear no reparte nada
        # LOS OCULTOS SE LEEN DE TODOS LOS CAMINOS (arriba); LOS INGERIBLES, SOLO DEL KIT Y DEL
        # REPARTO DEV-VISTO (ADR-0042). La fidelidad sigue fuera: su `dev` es de otro camino.
        del_kit = fichero.resolve().is_relative_to(kit) or fichero.resolve().is_relative_to(visto)
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError) as exc:  # pragma: no cover - lo cubre casos_reservados
            raise IngestaError(f"{ruta}: {exc}") from exc
        for caso in (doc.get("asignacion") or {}) if isinstance(doc, dict) else {}:
            m = _CASO.match(str(caso))
            if m is not None and str(caso) not in reservados:
                if del_kit:
                    salida[m.group(1)] = str(caso)
                else:
                    de_otro_camino.add(str(caso))
    if cobertura is None:
        return Ingeribles(salida, {}, len(de_otro_camino))
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
    return Ingeribles(salida, negados, len(de_otro_camino))


def meses_sin_libro(
    cobertura: Mapping[str, Sequence[tuple[str, str]]], materiales: Mapping[str, str]
) -> list[str]:
    """Meses CON material declarado y SIN ningun libro atado por su sha.

    Un tramo sin `material_sha256` significa exactamente esto: «hay material de este mes, y
    `casos ingerir` no lo lee». Ningun libro se resuelve a ese mes, asi que no se pide ninguno de
    sus dias (2026-09-22: septiembre, hasta que tenga su brief y su medida en `libros.yaml`).
    """
    con_libro = set(materiales.values())
    return sorted(m for m, tramos in cobertura.items() if tramos and m not in con_libro)


def aviso_de_meses_sin_libro(meses: Sequence[str]) -> str:
    return (
        f"INGESTA: {', '.join(meses)}: hay material declarado y ningun libro atado por su sha. "
        f"Este comando no lee ningun dia de ese mes, con ningun libro"
    )


def dias_del_material(
    repo: Path, dias: Mapping[str, str], materiales: Mapping[str, str], sha: str
) -> dict[str, str]:
    """De los `dias` ingeribles, SOLO los del mes que el libro DECLARA ser, por su sha.

    `materiales` es `sha256 -> AAAA-MM` de `cobertura_material`. Tres negativas, todas antes de
    leer una fila: un sha que no este en el manifiesto del corpus (el libro no es del corpus), un
    sha que ningun tramo declare (el libro no es material de ningun mes), y un mes sin ningun dia
    ingerible. Ninguna nombra un dia.
    """
    try:
        manifiesto = cargar_manifiesto(repo / MANIFIESTO_CORPUS)
    except InventarioError as exc:
        raise IngestaError(str(exc)) from exc
    del_corpus = {
        str(f.get("sha256")) for f in manifiesto.get("ficheros") or [] if isinstance(f, dict)
    }
    if sha not in del_corpus:
        raise IngestaError(
            f"el material {sha[:12]}... no esta en {MANIFIESTO_CORPUS}: no es un fichero del "
            f"corpus, o ha cambiado. No se lee"
        )
    mes = materiales.get(sha)
    if mes is None:
        raise IngestaError(
            f"el material {sha[:12]}... no lo declara ningun tramo de cobertura_material: no "
            f"consta de que mes es, y no se deduce de sus filas. No se lee"
        )
    salida = {d: c for d, c in dias.items() if d[:7] == mes}
    if not salida:
        raise IngestaError(
            f"el material es de {mes} y ese mes no tiene ningun dia ingerible en el camino del "
            f"kit. No se lee"
        )
    return salida


def _decimal(valor: object, fila: str, columna: str) -> Decimal:
    try:
        return Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise IngestaError(f"{fila}: `{columna}` no es un numero") from exc


def mensaje_mes_sin_filas(meses: Sequence[str]) -> str:
    """El texto de la regla del mes sin filas: solo lo que la regla sabe, sin sujeto humano."""
    mes = ", ".join(meses)
    return (
        f"ninguno de los dias pedidos de {mes} tiene filas en este material: o el libro no es de "
        f"{mes} (revisa a que tramo de cobertura_material esta atado su sha), o esos dias no "
        f"tienen ninguna fila en la exportacion. No se escribe nada"
    )


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
    dias: Mapping[str, str] | Iterable[str] | None = None,
) -> Resultado:
    """Las operaciones de los dias ingeribles, agrupadas por dia. No escribe nada.

    `dias` es `dia -> id de caso` (o solo los dias, en tests); si no se pasa, se derivan con
    `dias_ingeribles`.

    **LOS MENSAJES DE ERROR NOMBRAN EL CASO Y LA COMPROBACION, NUNCA EL INSTANTE NI LOS PRECIOS**
    (2026-09-22). Con el lector filtrando en el huso correcto, lo que se imprimiria seria de un dia
    `dev`; pero una puerta no puede depender de que otra este bien: si el filtro vuelve a fallar,
    el mensaje no puede ser la via por la que salga una fila reservada. Y el caso sale de lo
    PEDIDO, no de la fila: una fila cuyo dia no este pedido aborta sin decir nada de ella.
    """
    if dias is None:
        pedidos: dict[str, str] = dias_ingeribles(repo).dias
    elif isinstance(dias, Mapping):
        pedidos = {str(d): str(c) for d, c in dias.items()}
    else:
        pedidos = {d: f"el caso del dia {d}" for d in dias}
    if not pedidos:
        raise IngestaError(
            "no hay ningun dia ingerible: o no hay reparto commiteado, o todos sus casos estan "
            "reservados"
        )
    try:
        declaracion = declaracion_de(repo, material)
        filas = filas_de_los_dias(
            material, pedidos, PESTANA, COLUMNAS, declaracion, huso_de_los_dias=huso_operativa
        )
    except (LibroError, LibrosError, OSError) as exc:
        raise IngestaError(str(exc)) from exc

    # LA REGLA DEL MES SIN FILAS (se mantiene, 2026-09-23, docs/validation/REGLA-MES-SIN-FILAS.md).
    # Cuenta SOLO las filas de los dias PEDIDOS, nunca las del mes entero: si ninguno de los dias
    # pedidos de un mes tiene fila, el comando para. Es lo unico que detecta un libro cuyo sha esta
    # atado en `cobertura_material` al tramo de OTRO mes. Su coste, aceptado: no distingue ese caso
    # de uno valido -ninguno de esos dias tiene fila en la exportacion-, en el que tampoco habria
    # nada que escribir.
    #
    # EL MENSAJE DICE SOLO LO QUE LA REGLA SABE. Hasta el 2026-09-23 decia «el material no tiene ni
    # una fila de <mes>», afirmando algo del mes entero que la regla no comprueba (patron 5). Y va
    # SIN sujeto humano, por lo mismo que el aviso de dias sin operaciones: de una ausencia salen
    # dos lecturas, y quedarse con «el trader no opero» seria atribuirle una decision.
    meses_pedidos = {d[:7] for d in pedidos}
    meses_con_filas = {str(f["_dia"])[:7] for f in filas}
    vacios = sorted(meses_pedidos - meses_con_filas)
    if vacios:
        raise IngestaError(mensaje_mes_sin_filas(vacios))

    casos: dict[str, list[Operacion]] = {d: [] for d in pedidos}
    sin_stop = 0
    orden: dict[str, int] = {}
    for fila in filas:
        dia = str(fila.get("_dia"))
        if dia not in pedidos:
            # Defensa en profundidad: el lector no deberia devolverla. Si lo hace, NADA de ella
            # sale de aqui -ni su dia, ni su instante, ni sus precios-.
            raise IngestaError(
                "el lector devolvio una fila de un dia que no se pidio. No se dice nada de ella: "
                "es un fallo del filtro por dia, y puede ser de un dia reservado"
            )
        # Se nombra por el CASO -que sale de lo pedido- y su orden dentro de el. Nunca por el
        # instante ni los precios, ni por su fila en el libro.
        orden[dia] = orden.get(dia, 0) + 1
        n = f"{pedidos[dia]}, operacion {orden[dia]}"
        lado = str(fila.get("side") or "")
        if lado not in _DIRECCION:
            raise IngestaError(f"{n}: `side` no es buy ni sell")
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
                f"{n}: falla el invariante geometrico -con `side` {lado} el stop esta del lado "
                f"equivocado de la entrada-. O las columnas estan intercambiadas o el material no "
                f"es el que se cree"
            )
        instante = str(fila["_instante_utc"])
        sesion = _sesion_de(instante, huso_operativa, sesiones)
        if sesion is None:
            raise IngestaError(
                f"{n}: su apertura no cae en ninguna sesion declarada. La asignacion a sesion "
                f"H4 depende del huso, y sin ella la unidad de fidelidad no existe"
            )
        casos[dia].append(Operacion(instante, sesion, _DIRECCION[lado], entrada, stop))
    # Despues de la puerta y de la regla por mes, esto significa UNA cosa: el material cubre ese
    # dia y NO HAY NINGUNA FILA. Se cuenta, y quien llama lo dice SIN sujeto humano.
    sin_operaciones = sum(1 for d in pedidos if not casos.get(d))
    return Resultado(casos, sin_stop, len(filas), sin_operaciones)
