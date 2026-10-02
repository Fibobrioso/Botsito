"""El productor de la zona de entrada (RN-008, RN-009, RN-011, RN-005) sobre la geometria de M1 de
`domain/estructura_m1.py`, con el selector de A-21 como puerta.

Rama `trabajo/preparar-a21`, 2026-09-27. Mismo patron que A-35 y A-44 (ADR-0054): el selector
`zona_control_limpia` vive en el registro como UNKNOWN hasta que el trader responda A-21; sin fijar
el motor se niega a correr, salvo en modo diagnostico etiquetado `DIAGNOSTICO-A21-<lectura>`, cuyas
salidas no cuentan para nada. Con el valor fijado, el diagnostico se rechaza.

El estado del productor vive en `EstadoDia.memoria` (nace y muere con el dia, ADR-0048 §3).
**Cada sesion es un escenario propio** (A-46 RESUELTA en la sesion 3, «cada uno es un mundo
diferente»; ADR-0055 §4): el hecho `liquidez_tomada` caduca al abrir la sesion y el productor lo
sigue, asi que la toma, el esquema y el id de la zona se guardan SESION A SESION y lo de una no
vale en la siguiente. Por sesion (`memoria_de_sesion`):

- `toma`: el instante en que RN-004 fijo `liquidez_tomada`, el nivel del pivote tomado y el
  lado de la entrada (el del sesgo: alcista compra, bajista vende);
- `esquema`: el `Esquema` detectado despues de la toma, si lo hay;
- `zona_id`: el id con el que `toca_colocar_orden_limite` ligo la zona en el cierre del breaker.

Y del dia entero: `zonas`, las `Zona` ligadas por `toca_colocar_orden_limite`, que las acciones
del cableado leen; sus ids no se repiten entre sesiones.

**Dentro de la sesion, ESCENARIOS** (ADR-0066): un escenario es una liquidez de M15 tomada dentro
de la sesion, con sus zonas -y por ellas, sus intentos-. La sesion guarda la lista
(`escenarios`) y `toma`, `esquema` y `zona_id` son los del vigente. El primero nace con la primera
toma de la sesion; los siguientes los abre `abrir_escenario`, la accion de RN-004, con cada toma
NUEVA -la de otro pivote- cuando el vigente ha terminado, o con el vigente vivo segun
`intentos_tras_toma_nueva` (A-25). Termina con una ganadora (RN-034, `terminar`), y un escenario
terminado no coloca mas. Sin intentos no se marca terminado: RN-016 deja
`detenido_por_cartuchos`, que prohibe abrir (RN-001) hasta que la toma de otra liquidez abre el
escenario siguiente y lo apaga.

`orden_limite_nace` (A-29, RESUELTA en `al_aparecer_punto_de_breaker`): `al_darse_el_esquema` coloca
en el cierre del breaker, en el 0 del bloque de origen, como siempre; `al_tomarse_la_liquidez` queda
NO_IMPLEMENTADA con nombre. `al_aparecer_punto_de_breaker` es LA VIDA DE LA ORDEN STOP (ADR-0056 §7,
ADR-0064): tras la toma de la sesion, la orden nace en el posible punto de breaker que dice
`orden_stop_punto` -`ultimo_pivote_m1`, el ultimo pivote de M1 contrario a la entrada (la funcion de
R5), o `referencia_de_la_toma`, el de `referencia_del_breaker` en la toma- con la caja que dice
`caja_bloque` (R6, R4 o R1 de CAJA-77), y cada punto nuevo liga una zona nueva (`zona_del_punto`),
que RN-006 usa para reubicarla. Un punto ya usado -colocado, aceptado o rechazado- no se vuelve a
colocar (`marcar_usada`), y la sesion guarda sus zonas usadas (`zonas_usadas`). Con `caja_se_fija` =
`en_cada_cierre_m1` (sensibilidad de ADR-0064, decision 5) el 1 de la caja se recalcula en cada
cierre de M1 hasta el llenado: un 1 nuevo es una zona nueva del mismo punto, y RN-006 la reubica; un
punto cuya orden se rechazo no se vuelve a colocar con otra caja (`marcar_rechazada`)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol, cast

from botsito.config.registro import ParametroDesconocidoError, Registro
from botsito.domain.estructura_m1 import (
    COMPRA,
    LECTURAS_LIMPIA,
    PRIMER_ESQUEMA,
    VENTA,
    Esquema,
    detectar_esquema,
    extremo_de_la_caja,
    ultimo_punto_de_ruptura,
)
from botsito.domain.pivotes_m15 import ALTO, BAJO, Pivote
from botsito.domain.velas import Vela
from botsito.engine.interprete import (
    VALOR_APAGADO,
    EstadoDia,
    Momento,
    NoImplementada,
    Resultado,
    Tri,
)

PARAMETRO_A21 = "zona_control_limpia"
ETIQUETA_A21 = "DIAGNOSTICO-A21"
HECHO_LIQUIDEZ_TOMADA = "liquidez_tomada"
HECHO_SESGO = "sesgo"
AL_DARSE_EL_ESQUEMA = "al_darse_el_esquema"
AL_APARECER_PUNTO_DE_BREAKER = "al_aparecer_punto_de_breaker"
PARAMETRO_MOMENTO = "orden_limite_nace"
PARAMETRO_PUNTO = "orden_stop_punto"
PARAMETRO_BLOQUE = "caja_bloque"
ULTIMO_PIVOTE_M1 = "ultimo_pivote_m1"
REFERENCIA_DE_LA_TOMA = "referencia_de_la_toma"
PARAMETRO_CAJA_SE_FIJA = "caja_se_fija"
FIJA_AL_VERSE = "al_verse_el_punto"
EN_CADA_CIERRE_M1 = "en_cada_cierre_m1"
CUALQUIER_ESQUEMA = "cualquier_esquema"
PREFIJO_ZONA = "zona:"
POR_SESION = "por_sesion"
ESCENARIOS = "escenarios"
# Las opciones de `intentos_tras_toma_nueva` (A-25) y la unica de `cartuchos_reinicio` que tiene
# contrato (ADR-0066).
INTENTOS_VUELVEN = "vuelven_a_cartuchos_max"
INTENTOS_SIGUEN = "siguen_los_que_quedan"
REINICIO_SIGUIENTE_LIQUIDEZ = "siguiente_liquidez_m15"
# Las opciones de `max_escenarios_por_sesion` (A-52): sin tope, o un numero, que vive en el
# registro como texto de la opcion; y las de `orden_pendiente_al_abrir_escenario` (A-53).
SIN_LIMITE = "sin_limite"
ORDEN_SE_MUEVE = "se_mueve"
ORDEN_SE_RETIRA = "se_retira"
HECHO_DETENIDO = "detenido_por_cartuchos"
TERMINADO_POR_GANANCIA = "ganancia"
LOOKBACK_M1 = (
    240  # minutos de M1 anteriores a la toma con los que se busca la referencia del breaker
)
# El lado de la entrada y el del pivote de la liquidez, por sesgo (RN-005 y `primitivas.py`).
LADO_ENTRADA = {"alcista": COMPRA, "bajista": VENTA}
LADO_PIVOTE = {"alcista": BAJO, "bajista": ALTO}


class SinLecturaDeZonaError(ValueError):
    """A-21 sin responder: el motor se niega a correr y lo dice."""


class DiagnosticoDeZonaRechazadoError(ValueError):
    """Se pidio el diagnostico de A-21 con el selector fijado: la corrida cuenta, sin etiqueta."""


class DatosDeZona(Protocol):
    def m1_entre(self, desde: int, hasta: int) -> list[Vela]: ...

    def liquidez_m15(self, instante: int, lado: str) -> Pivote | None: ...


@dataclass(frozen=True)
class Zona:
    """Una zona de control ligada por una regla: la entrada (nivel 0), el extremo de la caja
    (nivel 1), el lado y como se produjo (`por`, un esquema de la spec). Vive aqui para que el
    productor no dependa del broker; `primitivas_broker` la reexporta."""

    id: str
    lado: str
    entrada: int  # puntos
    extremo: int  # puntos, el nivel 1 de la caja
    por: str
    desde: int | None = None  # minuto UTC en que empieza el bloque de origen (para el visor)
    formada: int | None = None  # minuto UTC del cierre del breaker: desde cuando existe

    @property
    def distancia_completa(self) -> int:
        return abs(self.entrada - self.extremo)


def lectura_limpia(registro: Registro, a21: str | None) -> str:
    """La lectura de «limpia» con la que corre el motor: la del registro si el trader la fijo; si
    no, la del diagnostico pedido; y sin ninguna, la negativa que nombra A-21."""
    try:
        fijada: str | None = registro.opcion(PARAMETRO_A21)
    except ParametroDesconocidoError:
        fijada = None
    if fijada is not None:
        if a21 is not None:
            raise DiagnosticoDeZonaRechazadoError(
                f"{PARAMETRO_A21} ya esta fijado en {fijada!r} (A-21 respondida): la corrida "
                "cuenta y no admite --diagnostico-a21"
            )
        return fijada
    if a21 is not None:
        if a21 not in LECTURAS_LIMPIA:
            raise ValueError(f"lectura de A-21 {a21!r} no esta en {LECTURAS_LIMPIA}")
        return a21
    raise SinLecturaDeZonaError(
        f"A-21 sin fijar: `{PARAMETRO_A21}` es UNKNOWN en knowledge/spec/parametros.yaml y la spec "
        "no define que hace limpia una zona de control; el motor se niega a correr. La responde el "
        "trader (docs/runbooks/ACTIVAR-A35-A44.md). Para ver el embudo en hipotesis, "
        f"--diagnostico-a21 <{'|'.join(LECTURAS_LIMPIA)}>: corre ETIQUETADO y sin valor para "
        "ninguna medida"
    )


def _memoria(estado: EstadoDia) -> dict[str, Any]:
    return cast(dict[str, Any], estado.memoria.setdefault("zona_de_entrada", {}))


def _de_la_sesion(estado: EstadoDia, sesion: str | None) -> dict[str, Any]:
    """La toma, el esquema y el id de la zona de UNA sesion. No hay nada que borrar al cambiar
    de sesion: cada una escribe en lo suyo, y asi el predicado que lo lee sigue siendo puro
    (ADR-0055 §1)."""
    por_sesion = _memoria(estado).setdefault(POR_SESION, {})
    return cast(dict[str, Any], por_sesion.setdefault(sesion or "", {}))


def memoria_de_sesion(estado: EstadoDia, sesion: str) -> Mapping[str, Any]:
    """Lo que el productor guardo de una sesion (`toma`, `esquema`, `zona_id`), sin crear nada:
    para quien mide despues de correr el dia (`scripts/embudo_77.py`)."""
    mem: Mapping[str, Any] = estado.memoria.get("zona_de_entrada", {})
    return cast(Mapping[str, Any], mem.get(POR_SESION, {}).get(sesion, {}))


def _toma_del_momento(
    datos: DatosDeZona, momento: Momento, estado: EstadoDia
) -> dict[str, Any] | None:
    """La toma que dice el hecho en este instante: el pivote que hoy es la liquidez, del lado del
    sesgo, con su identidad (`pivote`: lado, nivel e instante de formacion) para distinguir una
    toma NUEVA de la misma liquidez vista otra vez (RN-004 la vuelve a fijar en cada M1 que cierra
    pasada la linea)."""
    if estado.hechos.get(HECHO_LIQUIDEZ_TOMADA) != "si":
        return None
    sesgo = str(estado.hechos.get(HECHO_SESGO))
    lado_entrada, lado_pivote = LADO_ENTRADA.get(sesgo), LADO_PIVOTE.get(sesgo)
    if lado_entrada is None or lado_pivote is None:
        return None
    try:
        pivote = datos.liquidez_m15(int(momento.instante), lado_pivote)
    except (AttributeError, LookupError):
        return None
    if pivote is None:
        return None
    return {
        "instante": int(momento.instante),
        "nivel": pivote.nivel,
        "lado": lado_entrada,
        "pivote": (pivote.lado, pivote.nivel, int(pivote.formado_en)),
    }


def _abrir(estado: EstadoDia, sesion: str | None, toma: dict[str, Any]) -> dict[str, Any]:
    """Un escenario nuevo en la sesion (ADR-0066), con la toma que lo abre: lo que el productor
    guardaba de la sesion (la toma, el esquema y la zona del esquema) pasa a ser el de este."""
    mem = _de_la_sesion(estado, sesion)
    escenarios = mem.setdefault(ESCENARIOS, [])
    escenario = {"n": len(escenarios) + 1, "toma": toma, "zonas": set(), "terminado": None}
    escenarios.append(escenario)
    mem["toma"] = toma
    mem.pop("esquema", None)
    mem.pop("zona_id", None)
    return escenario


def escenario_actual(estado: EstadoDia, sesion: str | None) -> dict[str, Any] | None:
    """El ultimo escenario abierto en la sesion, o None si todavia no hay toma (ADR-0066)."""
    escenarios = _de_la_sesion(estado, sesion).get(ESCENARIOS) or []
    return cast(dict[str, Any], escenarios[-1]) if escenarios else None


def escenario_de_zona(estado: EstadoDia, sesion: str | None, zona_id: str) -> dict[str, Any] | None:
    """El escenario de la sesion en el que se ligo esa zona."""
    for escenario in _de_la_sesion(estado, sesion).get(ESCENARIOS) or []:
        if zona_id in escenario["zonas"]:
            return cast(dict[str, Any], escenario)
    return None


def _anotar_toma(datos: DatosDeZona, momento: Momento, estado: EstadoDia) -> dict[str, Any] | None:
    """La toma del escenario vigente de ESTA sesion. Si no hay ninguno y el hecho esta encendido,
    abre el primero con la toma de este instante: es lo que hacia el productor antes de los
    escenarios, y lo que pasa cuando el hecho se fija sin que RN-004 abra el escenario (un estado
    hecho a mano). Las tomas siguientes las abre `abrir_escenario` (ADR-0066)."""
    toma = _de_la_sesion(estado, momento.sesion).get("toma")
    if toma is not None:
        return cast(dict[str, Any], toma)
    nueva = _toma_del_momento(datos, momento, estado)
    if nueva is None:
        return None
    _abrir(estado, momento.sesion, nueva)
    return nueva


def _ligar_al_escenario(estado: EstadoDia, sesion: str | None, zona_id: str) -> None:
    escenario = escenario_actual(estado, sesion)
    if escenario is not None:
        escenario["zonas"].add(zona_id)


def acciones_escenario(registro: Registro) -> dict[str, Any]:
    """La accion de RN-004 que abre un escenario (ADR-0066). Va con las primitivas escritas haya
    geometria o no: el escenario es de la sesion, no del productor de la zona."""

    def abrir_escenario(
        args: Mapping[str, Any], ligaduras: Mapping[str, str], momento: Momento, estado: EstadoDia
    ) -> list[tuple[str, str]]:
        """RN-004 acaba de fijar `liquidez_tomada`. Si la liquidez es la misma que la del
        escenario vigente (RN-004 la vuelve a fijar en cada M1 pasada la linea), no hace nada. Si
        es NUEVA, abre un escenario cuando el vigente ha terminado (ganancia o intentos agotados);
        con el vigente vivo, lo decide `intentos` (A-25, pregunta 18 de la sesion 4). Abrir un
        escenario es el reinicio de los cartuchos (`reinicio`, `siguiente_liquidez_m15`): apaga
        `detenido_por_cartuchos`."""
        intentos = registro.opcion(str(args["intentos"]))
        if intentos not in (INTENTOS_VUELVEN, INTENTOS_SIGUEN):
            raise ValueError(f"{args['intentos']} = {intentos!r}: lectura sin contrato")
        reinicio = registro.opcion(str(args["reinicio"]))
        if reinicio != REINICIO_SIGUIENTE_LIQUIDEZ:
            raise ValueError(f"{args['reinicio']} = {reinicio!r}: lectura sin contrato")
        pendiente = registro.opcion(str(args["orden_pendiente"]))
        if pendiente not in (ORDEN_SE_MUEVE, ORDEN_SE_RETIRA):
            raise ValueError(f"{args['orden_pendiente']} = {pendiente!r}: lectura sin contrato")
        maximo = registro.opcion(str(args["maximo"]))
        tope = None if maximo == SIN_LIMITE else int(maximo)
        toma = _toma_del_momento(momento.datos, momento, estado)
        if toma is None:
            return []
        actual = escenario_actual(estado, momento.sesion)
        if actual is not None and actual["toma"]["pivote"] == toma["pivote"]:
            return []
        vivo = (
            actual is not None
            and actual["terminado"] is None
            and HECHO_DETENIDO not in estado.hechos
        )
        if vivo and intentos == INTENTOS_SIGUEN:
            # la toma nueva sigue el MISMO escenario, con los intentos que le quedaban
            assert actual is not None
            actual["toma"] = toma
            mem = _de_la_sesion(estado, momento.sesion)
            mem["toma"] = toma
            mem.pop("esquema", None)
            mem.pop("zona_id", None)
            return []
        abiertos = len(_de_la_sesion(estado, momento.sesion).get(ESCENARIOS) or [])
        if tope is not None and abiertos >= tope:
            return []  # max_escenarios_por_sesion (A-52): la toma no abre otro
        _abrir(estado, momento.sesion, toma)
        if estado.hechos.pop(HECHO_DETENIDO, None) is not None:
            return [(HECHO_DETENIDO, VALOR_APAGADO)]
        return []

    return {"abrir_escenario": abrir_escenario}


def terminar(estado: EstadoDia, sesion: str | None, escenario: dict[str, Any], motivo: str) -> None:
    """El escenario no da mas entradas: se espera otra liquidez (ADR-0066)."""
    if escenario["terminado"] is None:
        escenario["terminado"] = motivo


def escenario_terminado(estado: EstadoDia, sesion: str | None) -> bool:
    actual = escenario_actual(estado, sesion)
    return actual is not None and actual["terminado"] is not None


def _esquema(
    datos: DatosDeZona,
    momento: Momento,
    estado: EstadoDia,
    criterio: str,
    tope_zonas: int,
    limpia: str,
) -> Esquema | None:
    """El esquema detectado hasta este instante, sin mirar al futuro: solo M1 cerradas."""
    toma = _anotar_toma(datos, momento, estado)
    if toma is None:
        return None
    mem = _de_la_sesion(estado, momento.sesion)
    esquema = mem.get("esquema")
    if esquema is not None:
        return cast(Esquema, esquema)
    instante = int(momento.instante)
    m1 = datos.m1_entre(toma["instante"] - LOOKBACK_M1, instante)
    idx_toma = next((k for k, v in enumerate(m1) if int(v.fin) == toma["instante"]), None)
    if idx_toma is None:
        return None
    esquema = detectar_esquema(m1, idx_toma, toma["lado"], criterio, tope_zonas, limpia)
    if esquema is not None:
        mem["esquema"] = esquema
    return esquema


def orden_nace_en_el_punto(registro: Registro) -> bool:
    """Con `al_aparecer_punto_de_breaker` corre la vida de la orden stop (ADR-0064)."""
    return registro.opcion(PARAMETRO_MOMENTO) == AL_APARECER_PUNTO_DE_BREAKER


def zona_del_punto(registro: Registro, momento: Momento, estado: EstadoDia) -> Zona | None:
    """La zona del posible punto de breaker de ESTA sesion en este instante (ADR-0064), o None si
    todavia no hay toma, ni punto, ni caja con altura. Solo M1 cerradas. La misma para el mismo
    punto: se liga una vez, con la caja del primer instante en que se ve, y el id no se repite en
    el dia; asi es idempotente, como pide el interprete (ADR-0055 §1)."""
    datos = momento.datos
    toma = _anotar_toma(datos, momento, estado)
    if toma is None:
        return None
    instante = int(momento.instante)
    m1 = datos.m1_entre(toma["instante"] - LOOKBACK_M1, instante)
    idx_toma = next((k for k, v in enumerate(m1) if int(v.fin) == toma["instante"]), None)
    if idx_toma is None:
        return None
    lado = str(toma["lado"])
    lectura = registro.opcion(PARAMETRO_PUNTO)
    if lectura not in (ULTIMO_PIVOTE_M1, REFERENCIA_DE_LA_TOMA):
        raise ValueError(f"{PARAMETRO_PUNTO} = {lectura!r}: lectura sin contrato")
    hasta = idx_toma + 1 if lectura == REFERENCIA_DE_LA_TOMA else None
    punto = ultimo_punto_de_ruptura(m1, lado, hasta)
    if punto is None:
        return None
    mem = _de_la_sesion(estado, momento.sesion)
    puntos = mem.setdefault("puntos", {})
    zonas = _memoria(estado).setdefault("zonas", {})
    clave_punto = f"{punto.nivel}@{int(punto.contraria_inicio)}"
    se_fija = registro.opcion(PARAMETRO_CAJA_SE_FIJA)
    if se_fija not in (FIJA_AL_VERSE, EN_CADA_CIERRE_M1):
        raise ValueError(f"{PARAMETRO_CAJA_SE_FIJA} = {se_fija!r}: lectura sin contrato")
    extremo: int | None = None
    clave = clave_punto
    if se_fija == EN_CADA_CIERRE_M1:
        extremo = extremo_de_la_caja(m1, lado, punto, registro.opcion(PARAMETRO_BLOQUE))
        if extremo is None:
            return None
        clave = f"{clave_punto}#{extremo}"
    id = puntos.get(clave)
    if id is None:
        if extremo is None:
            extremo = extremo_de_la_caja(m1, lado, punto, registro.opcion(PARAMETRO_BLOQUE))
        if extremo is None:
            return None
        id = f"{PREFIJO_ZONA}{len(zonas) + 1}"
        puntos[clave] = id
        mem.setdefault("punto_de_zona", {})[id] = clave_punto
        _ligar_al_escenario(estado, momento.sesion, id)
        zonas[id] = Zona(
            id, lado, punto.nivel, extremo, PRIMER_ESQUEMA, int(m1[punto.marca].inicio), instante
        )
    return cast(Zona, zonas[id])


def marcar_rechazada(estado: EstadoDia, sesion: str | None, zona_id: str) -> None:
    """El broker rechazo la orden de esta zona: su PUNTO no se vuelve a colocar, tampoco con
    otra caja (ADR-0064, decision 1)."""
    mem = _de_la_sesion(estado, sesion)
    punto = mem.get("punto_de_zona", {}).get(zona_id)
    if punto is not None:
        mem.setdefault("rechazados", set()).add(punto)


def punto_rechazado(estado: EstadoDia, sesion: str | None, zona_id: str) -> bool:
    mem = _de_la_sesion(estado, sesion)
    return mem.get("punto_de_zona", {}).get(zona_id) in mem.get("rechazados", set())


def marcar_usada(estado: EstadoDia, sesion: str | None, zona_id: str) -> None:
    """La orden de esta zona ya se envio, aceptada o rechazada: su punto no se vuelve a colocar."""
    _de_la_sesion(estado, sesion).setdefault("usadas", set()).add(zona_id)


def zonas_usadas(estado: EstadoDia, sesion: str | None) -> frozenset[str]:
    return frozenset(_de_la_sesion(estado, sesion).get("usadas", set()))


def primitivas_zona(registro: Registro, limpia: str) -> dict[str, Any]:
    """Los predicados de la geometria de la entrada, con la lectura de A-21 dada."""
    if limpia not in LECTURAS_LIMPIA:
        raise ValueError(f"lectura de A-21 {limpia!r} no esta en {LECTURAS_LIMPIA}")

    def se_da_esquema(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        cual = str(args.get("cual"))
        criterio = registro.opcion(str(args["criterio"]))
        tope = registro.entero("zonas_control_max_por_esquema")
        e = _esquema(momento.datos, momento, estado, criterio, tope, limpia)
        if e is None:
            return Resultado(Tri.NO)
        return Resultado(Tri.SI if cual in (e.cual, CUALQUIER_ESQUEMA) else Tri.NO)

    def zonas_desarrolladas_superan(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        from botsito.domain.estructura_m1 import zonas_de_control

        toma = _anotar_toma(momento.datos, momento, estado)
        if toma is None:
            return Resultado(Tri.NO)
        tope = registro.entero(str(args["tope"]))
        m1 = momento.datos.m1_entre(toma["instante"] - LOOKBACK_M1, int(momento.instante))
        idx_toma = next((k for k, v in enumerate(m1) if int(v.fin) == toma["instante"]), None)
        if idx_toma is None or idx_toma >= len(m1) - 1:
            return Resultado(Tri.NO)
        return Resultado(
            Tri.SI if zonas_de_control(m1, idx_toma, len(m1) - 1, toma["lado"]) > tope else Tri.NO
        )

    def toca_colocar_orden_limite(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        momento_orden = registro.opcion(str(args["momento"]))
        # un escenario terminado -con una ganadora, o sin intentos- no coloca mas: se espera
        # otra liquidez de M15 (ADR-0066)
        _anotar_toma(momento.datos, momento, estado)
        if escenario_terminado(estado, momento.sesion):
            return Resultado(Tri.NO)
        if momento_orden == AL_APARECER_PUNTO_DE_BREAKER:
            z = zona_del_punto(registro, momento, estado)
            if (
                z is None
                or z.id in zonas_usadas(estado, momento.sesion)
                or punto_rechazado(estado, momento.sesion, z.id)
            ):
                return Resultado(Tri.NO)
            return Resultado(Tri.SI, {str(args.get("liga", "Z")): z.id})
        if momento_orden != AL_DARSE_EL_ESQUEMA:
            return NoImplementada(f"predicado:toca_colocar_orden_limite:{momento_orden}")
        criterio = registro.opcion("breaker_m1_criterio_ruptura")
        tope = registro.entero("zonas_control_max_por_esquema")
        e = _esquema(momento.datos, momento, estado, criterio, tope, limpia)
        # SI exactamente en el cierre del breaker, y sin efectos: el interprete evalua los `cuando`
        # de las demas reglas para avisar de empates (ADR-0049 H3), asi que una primitiva que se
        # «consumiera» al evaluarse dejaria de dar SI cuando le toca disparar. La zona se registra
        # de forma idempotente, con el mismo id para el mismo esquema.
        if e is None or int(momento.instante) != int(e.breaker_fin):
            return Resultado(Tri.NO)
        zonas = _memoria(estado).setdefault("zonas", {})
        mem = _de_la_sesion(estado, momento.sesion)
        id = mem.setdefault("zona_id", f"{PREFIJO_ZONA}{len(zonas) + 1}")
        if id not in zonas:
            _ligar_al_escenario(estado, momento.sesion, id)
        zonas.setdefault(
            id,
            Zona(
                id, e.lado, e.entrada, e.extremo, e.cual, int(e.bloque_inicio), int(e.breaker_fin)
            ),
        )
        liga = str(args.get("liga", "Z"))
        return Resultado(Tri.SI, {liga: id})

    def se_desarrolla_en_el_lado_de_ruido(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        # Con la vida de la orden stop la zona es la del punto (ADR-0064, DECISION: RN-005 se
        # aplica a ella, la lectura mas conservadora); con el esquema, la del esquema
        e: Esquema | Zona | None
        if orden_nace_en_el_punto(registro):
            e = zona_del_punto(registro, momento, estado)
        else:
            criterio = registro.opcion("breaker_m1_criterio_ruptura")
            tope = registro.entero("zonas_control_max_por_esquema")
            e = _esquema(momento.datos, momento, estado, criterio, tope, limpia)
        toma = _de_la_sesion(estado, momento.sesion).get("toma")
        if e is None or toma is None:
            return Resultado(Tri.NO)
        # RN-005: la operativa alcista va por debajo de la liquidez tomada, la bajista por encima;
        # una zona al otro lado se desarrolla en el ruido
        ruido = e.entrada > toma["nivel"] if e.lado == COMPRA else e.entrada < toma["nivel"]
        return Resultado(Tri.SI if ruido else Tri.NO)

    def la_orden_nace_antes_del_esquema(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        # RN-008 no frena la colocacion de la orden stop en el punto (ADR-0056 §7, ADR-0064)
        nace = registro.opcion(str(args["momento"])) == AL_APARECER_PUNTO_DE_BREAKER
        return Resultado(Tri.SI if nace else Tri.NO)

    return {
        "se_da_esquema": se_da_esquema,
        "la_orden_nace_antes_del_esquema": la_orden_nace_antes_del_esquema,
        "zonas_desarrolladas_superan": zonas_desarrolladas_superan,
        "toca_colocar_orden_limite": toca_colocar_orden_limite,
        "se_desarrolla_en_el_lado_de_ruido": se_desarrolla_en_el_lado_de_ruido,
    }


def zonas_del_dia(estado: EstadoDia) -> dict[str, Zona]:
    """Las zonas que el productor ligo en este dia (para las acciones del cableado)."""
    return _memoria(estado).get("zonas", {})  # type: ignore[no-any-return]


__all__ = [
    "ESCENARIOS",
    "INTENTOS_SIGUEN",
    "INTENTOS_VUELVEN",
    "TERMINADO_POR_GANANCIA",
    "acciones_escenario",
    "escenario_actual",
    "escenario_de_zona",
    "escenario_terminado",
    "terminar",
    "AL_APARECER_PUNTO_DE_BREAKER",
    "AL_DARSE_EL_ESQUEMA",
    "ETIQUETA_A21",
    "LADO_ENTRADA",
    "PARAMETRO_A21",
    "EN_CADA_CIERRE_M1",
    "FIJA_AL_VERSE",
    "PARAMETRO_BLOQUE",
    "PARAMETRO_CAJA_SE_FIJA",
    "PARAMETRO_MOMENTO",
    "PARAMETRO_PUNTO",
    "REFERENCIA_DE_LA_TOMA",
    "ULTIMO_PIVOTE_M1",
    "DiagnosticoDeZonaRechazadoError",
    "SinLecturaDeZonaError",
    "Zona",
    "lectura_limpia",
    "marcar_rechazada",
    "marcar_usada",
    "memoria_de_sesion",
    "orden_nace_en_el_punto",
    "punto_rechazado",
    "primitivas_zona",
    "zona_del_punto",
    "zonas_del_dia",
    "zonas_usadas",
]
