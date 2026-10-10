"""Ventanas de replay para el etiquetado ciego (F10, ADR-0011).

Un caso es el dia operativo del trader (`ventana_local` de `config.yaml`, en horas NOMINALES
contadas por la puerta del reloj de las sesiones, `cases/relojes.py`; desde ADR-0069, la rejilla
H4) sobre un dataset congelado (F15): `dataset_id`, ventana UTC `[desde, hasta)`, velas M1 con su
hash (recomputable con `cargar_ventana`) y los limites de las velas H4 con cada anclaje candidato
(`limites_entre`, ADR-0005). El universo son los dias laborables NO vistos por el trader cuya
ventana completa cae dentro del dataset, tiene suficientes velas y la puerta sabe decidir.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any, cast

from botsito.cases.relojes import (
    HUSO_DEL_RELOJ,
    PARAMETRO_RELOJ_SESIONES,
    PARAMETROS_DE_LA_REJILLA,
    REJILLA_H4,
    RelojError,
    RelojSesiones,
    reloj_de_las_sesiones,
)
from botsito.comun.documentos import sha256_hex
from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.config.registro import Registro
from botsito.data.agregacion import limites_entre
from botsito.data.dataset import cargar_serie
from botsito.data.velas import a_datetime, escribir_csv, formato_ts, parse_ts
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import MinutoUtc, SerieVelas

MINUTOS_H4 = 240
MINUTOS_M15 = 15


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
    reloj: RelojSesiones,
    ventana_local: tuple[str, str],
    sesiones: Sequence[tuple[str, str, str]],
    anclajes: list[Anclaje],
    min_velas: int,
) -> Caso | Excluido:
    """El caso del dia, o el motivo por el que queda fuera del universo.

    La ventana sale de la PUERTA (`reloj.instante`), nunca de pasar una hora a un huso aqui. Y la
    puerta tiene que poder decidir el dia: si sus guardias saltan -la vela que abre la ventana no
    es una H4 entera, o una sesion no es una vela de la rejilla-, el dia no es operable y sale del
    universo con el motivo que da la puerta, que nombra el dia y la razon (negar por defecto)."""
    try:
        reloj.limites_de_sesiones(dia, sesiones)
        desde = reloj.instante(dia, ventana_local[0])
        hasta = reloj.instante(dia, ventana_local[1])
    except RelojError as exc:
        return Excluido(dia.isoformat(), f"la puerta del reloj no decide el dia: {exc}")
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


def motivo_de_cobertura(dia: str, tramos: Sequence[tuple[str, str]]) -> str:
    """El motivo de excluir un dia por la cobertura del material. Publico a proposito.

    CERO TRAMOS tiene su propia frase: hasta el 2026-09-21 salia `(2026-06 cubre )` con la lista
    vacia detras, que es literalmente falso, y el motivo de una exclusion es lo unico que alguien
    va a leer dentro de un ano. Vive aqui, y no dentro del bucle, para que el test compruebe LA
    FRASE y no una copia suya.
    """
    mes = dia[:7]
    if not tramos:
        return f"{mes}: sin material del trader (declarado con cero tramos en cobertura_material)"
    cubre = ", ".join(f"{d}..{h}" for d, h in tramos)
    return f"fuera de la cobertura del material del trader ({mes} cubre {cubre})"


def universo(
    manifiestos: list[dict[str, Any]],
    carpeta_datos: Path,
    simbolo: str,
    reloj: RelojSesiones,
    ventana_local: tuple[str, str],
    sesiones: Sequence[tuple[str, str, str]],
    anclajes: list[Anclaje],
    min_velas: int,
    meses_vistos: set[str],
    dias_vistos: set[str],
    cobertura: Mapping[str, Sequence[tuple[str, str]]] | None = None,
    solo_con_cobertura: bool = False,
    solo_mes: str | None = None,
) -> tuple[list[Caso], list[Excluido]]:
    """Casos de todos los dias laborables no vistos de los datasets dados (ordenados por dia) y
    los dias excluidos con motivo. Cada dataset se lee UNA vez (hash por fichero).

    `cobertura` acota un mes a lo que cubre el MATERIAL ETIQUETADO del trader (ADR-0036): mes ->
    tramos `(desde, hasta)` de dias del trader. Un mes que no aparece NO se acota, que es lo que
    hace que esto no toque ningun paquete anterior.

    `solo_mes` (ADR-0046) limita el universo a UN mes, el del artefacto de fidelidad: la
    `cobertura_material` es una sola para todos los meses, y sin esto un artefacto de marzo se
    llevaria tambien los dias de septiembre. Va DESPUES del filtro de cobertura y con motivo
    propio, asi que un dia sin cobertura conserva el suyo y un artefacto de un solo mes cubierto
    -septiembre- sale igual byte a byte.

    `solo_con_cobertura` invierte esa regla y es del camino de fidelidad: alli un mes SIN material
    declarado no aporta ningun caso, porque ese camino existe para repartir material etiquetado y
    de un mes sin material no hay nada que medir. Los manifiestos se siguen pasando TODOS aunque
    su mes no aporte casos: el dia 1 de un mes necesita las velas de la vispera, y sin el mes
    anterior en la lista el primer dia se caeria con un motivo que no es el suyo.

    El filtro va con MOTIVO PROPIO y despues de
    los de vistos: si fuera despues de `construir_caso`, el dia saldria como `N velas < min` o
    como `ventana fuera del dataset`, y ninguno de los dos dice la verdad -que el trader no
    etiqueto ese dia-. `excluidos:` es la unica narracion de por que un dia no entro.
    """
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
            tramos = (cobertura or {}).get(dia.isoformat()[:7])
            if tramos is None and solo_con_cobertura:
                excluidos.append(
                    Excluido(
                        dia.isoformat(),
                        f"sin material etiquetado del trader ({dia.isoformat()[:7]} no esta en "
                        f"cobertura_material)",
                    )
                )
                continue
            if solo_mes is not None and dia.isoformat()[:7] != solo_mes:
                excluidos.append(
                    Excluido(dia.isoformat(), f"de otro mes que el del artefacto ({solo_mes})")
                )
                continue
            # Con CERO tramos `any(...)` es False y el mes entero cae por aqui, que es
            # exactamente lo que se quiere: mes declarado, cero dias cubiertos.
            if tramos is not None and not any(d <= dia.isoformat() <= h for d, h in tramos):
                excluidos.append(
                    Excluido(dia.isoformat(), motivo_de_cobertura(dia.isoformat(), tramos))
                )
                continue
            resultado = construir_caso(
                serie, dia, simbolo, reloj, ventana_local, sesiones, anclajes, min_velas
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
    serie = cargar_serie(manifiesto, carpeta_datos)
    return hash_ventana(serie, parse_ts(desde_utc), parse_ts(hasta_utc))


# ------------------------------------------------------------------ el reloj del caso (ADR-0069)
#
# La ventana de un caso se cuenta por la PUERTA del reloj de las sesiones (`cases/relojes.py`), la
# misma que usa el motor: con `rejilla_h4`, las horas nominales del kit (00:00, 07:00, 15:00) caen
# donde abre la vela H4 de la rejilla, y no en la pared de `huso_operativa`. Fuera de los dias de
# desfase las dos dan los mismos instantes; en ellos la rejilla va una hora antes, que es la hora a
# la que opera el trader (ACTIVACION-A42.md §3.6, CASES-REJILLA.md).
#
# EL RELOJ SE CONGELA en el artefacto, en la clave de primer nivel `reloj_sesiones`, igual que ya
# se congelaba `huso_operativa`: el sorteo no se repite (ADR-0046 §5), y el artefacto tiene que
# decir con que reloj se calculo. Se lee NEGANDO POR DEFECTO (respuesta del consultor del
# 2026-10-10, punto 1): con la clave, el reloj congelado y nunca el del registro de hoy; sin ella,
# el artefacto se calculo en la pared de su `huso_operativa`; un valor que la puerta no reconoce,
# o una clave de mas o de menos, es un error con nombre.

CLAVE_RELOJ = PARAMETRO_RELOJ_SESIONES
CLAVE_HUSO = "huso_operativa"


@dataclass(frozen=True)
class RelojDelArtefacto:
    """El reloj con que se calcula un artefacto, y lo que se congela de el en `ventanas.yaml`.

    `congelado` es None en un artefacto de antes de la clave: se recompone en la pared de su
    `huso_operativa` y no se le escribe una clave que no tenia (sus bytes no cambian)."""

    reloj: RelojSesiones
    congelado: dict[str, Any] | None


def _parametros_del_reloj(opcion: str) -> tuple[str, ...]:
    """Los parametros que la puerta lee con cada opcion del selector (su tabla, no una copia)."""
    if opcion == REJILLA_H4:
        return tuple(PARAMETROS_DE_LA_REJILLA.values())
    return (HUSO_DEL_RELOJ[opcion],)


def reloj_del_registro(registro: Registro) -> RelojDelArtefacto:
    """El reloj de un artefacto NUEVO: el del registro, por la puerta, y su forma congelada (el
    valor del selector y los parametros que la puerta lee con el)."""
    reloj = reloj_de_las_sesiones(registro)
    congelado: dict[str, Any] = {PARAMETRO_RELOJ_SESIONES: reloj.opcion}
    for nombre in _parametros_del_reloj(reloj.opcion):
        tipo = registro.parametros[nombre].tipo
        if tipo == "hora":
            h = registro.hora(nombre)
            congelado[nombre] = {"hora": h.hora, "huso": h.huso}
        elif tipo == "entero":
            congelado[nombre] = registro.entero(nombre)
        else:
            congelado[nombre] = registro.texto(nombre)
    return RelojDelArtefacto(reloj, congelado)


class _RegistroCongelado:
    """Lo que `reloj_de_las_sesiones` lee de un registro, servido desde la clave congelada: la
    puerta construye el reloj congelado por el MISMO camino, y con las mismas guardias, que el del
    registro."""

    def __init__(self, doc: Mapping[str, Any], donde: str) -> None:
        self._doc = doc
        self._donde = donde

    def _valor(self, nombre: str, tipo: type) -> Any:
        valor = self._doc.get(nombre)
        if isinstance(valor, bool) or not isinstance(valor, tipo):
            raise RelojError(
                f"{self._donde}: {CLAVE_RELOJ}.{nombre} = {valor!r}: no es un {tipo.__name__}"
            )
        return valor

    def opcion(self, nombre: str) -> str:
        return str(self._valor(nombre, str))

    def texto(self, nombre: str) -> str:
        huso = str(self._valor(nombre, str))
        try:
            huso_canonico(huso)
        except HusoDesconocidoError as exc:
            raise RelojError(f"{self._donde}: {CLAVE_RELOJ}.{nombre}: {exc}") from exc
        return huso

    def entero(self, nombre: str) -> int:
        return int(self._valor(nombre, int))

    def hora(self, nombre: str) -> HoraLocal:
        valor = self._valor(nombre, dict)
        if set(valor) != {"hora", "huso"}:
            raise RelojError(f"{self._donde}: {CLAVE_RELOJ}.{nombre} necesita hora y huso")
        try:
            huso_canonico(valor["huso"])
            return HoraLocal(str(valor["hora"]), str(valor["huso"]))
        except (HusoDesconocidoError, ValueError) as exc:
            raise RelojError(f"{self._donde}: {CLAVE_RELOJ}.{nombre}: {exc}") from exc


def reloj_congelado(doc: object, donde: str) -> RelojSesiones:
    """El reloj de la clave `reloj_sesiones` de un artefacto. Niega por defecto."""
    if not isinstance(doc, dict):
        raise RelojError(f"{donde}: {CLAVE_RELOJ} debe ser un mapa")
    opcion = doc.get(PARAMETRO_RELOJ_SESIONES)
    if not isinstance(opcion, str) or (opcion != REJILLA_H4 and opcion not in HUSO_DEL_RELOJ):
        relojes = ", ".join((*HUSO_DEL_RELOJ, REJILLA_H4))
        raise RelojError(
            f"{donde}: {CLAVE_RELOJ}.{PARAMETRO_RELOJ_SESIONES} = {opcion!r}: no es un reloj que "
            f"la puerta reconozca ({relojes})"
        )
    esperadas = {PARAMETRO_RELOJ_SESIONES, *_parametros_del_reloj(opcion)}
    if set(doc) != esperadas:
        raise RelojError(
            f"{donde}: {CLAVE_RELOJ} con {opcion} lleva exactamente {sorted(esperadas)}, no "
            f"{sorted(doc)}"
        )
    return reloj_de_las_sesiones(cast(Registro, _RegistroCongelado(doc, donde)))


def reloj_de_ventanas(ventanas: Mapping[str, Any], donde: str) -> RelojDelArtefacto:
    """El reloj con que se calculo un artefacto YA CONGELADO. Nunca el del registro de hoy."""
    if CLAVE_RELOJ in ventanas:
        crudo = ventanas[CLAVE_RELOJ]
        return RelojDelArtefacto(reloj_congelado(crudo, donde), dict(crudo))
    huso = ventanas.get(CLAVE_HUSO)
    try:
        huso_canonico(huso)
    except HusoDesconocidoError as exc:
        raise RelojError(
            f"{donde}: sin {CLAVE_RELOJ} y sin un {CLAVE_HUSO} valido: no se sabe con que reloj "
            f"se calculo ({exc})"
        ) from exc
    return RelojDelArtefacto(RelojSesiones.de_pared(str(huso)), None)


# ------------------------------------------------------------------ lo que el trader ve


def _en_pantalla(reloj: RelojSesiones, minuto: MinutoUtc | int) -> tuple[str, str]:
    """(fecha, «HH:MM») que el grafico del trader marca en `minuto`: el `huso_visible` de la
    puerta (`huso_grafico` con la rejilla). Es lo UNICO de cases/, fuera de la puerta, que pasa un
    instante a un huso, y solo para PINTARLO: ninguna ventana se calcula con esto."""
    local = a_datetime(minuto).astimezone(huso_canonico(reloj.huso_visible))
    return local.date().isoformat(), local.strftime("%H:%M")


def hora_en_pantalla(reloj: RelojSesiones, minuto: MinutoUtc | int) -> str:
    return _en_pantalla(reloj, minuto)[1]


@dataclass(frozen=True)
class OtrasHoras:
    """Un dia cuyo grafico no marca las horas nominales del kit (los dias de desfase)."""

    dia: str
    desde: str
    hasta: str
    desde_la_vispera: bool
    sesiones: tuple[tuple[str, str, str], ...]


def dias_con_otras_horas(
    reloj: RelojSesiones,
    casos: Sequence[tuple[str, str, str]],
    ventana_local: tuple[str, str],
    sesiones: Sequence[tuple[str, str, str]],
) -> list[OtrasHoras]:
    """De los casos `(dia, desde_utc, hasta_utc)`, los que en el grafico del trader NO van de
    `ventana_local` con las sesiones en sus horas nominales. Vacio fuera de los dias de desfase,
    asi que la hoja de un paquete sin ellos sale igual byte a byte."""
    nominales = tuple((n, a, b) for n, a, b in sesiones)
    salida: list[OtrasHoras] = []
    for dia, desde_utc, hasta_utc in casos:
        fecha_desde, desde = _en_pantalla(reloj, parse_ts(desde_utc))
        hasta = hora_en_pantalla(reloj, parse_ts(hasta_utc))
        en_pantalla = tuple(
            (n, hora_en_pantalla(reloj, a), hora_en_pantalla(reloj, b))
            for n, a, b in reloj.limites_de_sesiones(date.fromisoformat(dia), sesiones)
        )
        if (desde, hasta) == tuple(ventana_local) and en_pantalla == nominales:
            continue
        salida.append(OtrasHoras(dia, desde, hasta, fecha_desde != dia, en_pantalla))
    return salida
