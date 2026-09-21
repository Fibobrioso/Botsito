"""El paquete de una sesion (F10, ADR-0011): config del kit, construccion determinista,
escritura sin sobreescribir, `check` puro y validacion para `knowledge validate`."""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from botsito.cases.ambiguedades import (
    FICHERO_AMBIGUEDADES,
    Ambiguedad,
    AmbiguedadError,
    cargar_ambiguedades,
)
from botsito.cases.ambiguedades import validar_contra_contexto as validar_ambiguedades
from botsito.cases.cuestionario import CuestionarioError, EntradaMapa, Pregunta, generar
from botsito.cases.kappa import EtiquetaError
from botsito.cases.particiones import PARTICIONES, ParticionError, asignar
from botsito.cases.ventanas import Anclaje, Caso, Excluido, VentanaError, universo
from botsito.comun import ids
from botsito.comun.documentos import activos
from botsito.comun.historial import (
    blob_en_arbol,
    blob_en_head,
    commit_que_anadio,
    es_ancestro,
    intacto_desde,
)
from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.config.registro import Registro, RegistroError, cargar_registro
from botsito.data.dataset import DatasetError, cargar_manifiesto, manifiestos
from botsito.data.velas import parse_ts
from botsito.domain.valores import HoraLocal
from botsito.domain.velas import VelaInvalidaError
from botsito.evidence import contradicciones
from botsito.evidence.modelo import EvidenceItem, cargar_evidencia
from botsito.evidence.propuestas import FICHERO_TEMAS, cargar_temas
from botsito.feedback.modelo import FeedbackRecord
from botsito.retrieval.indice import Indice, construir_indice

DIRECTORIO_KIT = "knowledge/cases/kit"
FICHERO_CONFIG = "config.yaml"
FICHERO_MAPA = "mapa_parametros.yaml"
FICHERO_VISTOS = "vistos.yaml"
FICHERO_ANCLAS = "anclas.yaml"
# Lo que el ancla ata. `ventanas.yaml` lleva el universo y el config congelados; `particiones.yaml`,
# la asignacion. Son los dos ficheros que la guardia de ancestro ya nombraba.
FICHEROS_ANCLADOS = ("ventanas.yaml", "particiones.yaml")
FICHEROS_PAQUETE = ("cuestionario.yaml", "ventanas.yaml", "particiones.yaml", "hoja_trader.md")
# Lo que una sesion ya celebrada cambia legitimamente: el cuestionario ya no preguntaria lo
# mismo, las ventanas se recortan con lo respondido y la hoja las refleja. `particiones.yaml`
# NO esta aqui a proposito (ver `comprobar`). Y el `datasets:` de `ventanas.yaml` tampoco se exime
# nunca: se compara APARTE, antes del bucle, porque no sale de ninguna respuesta del trader
# (ADR-0035). Si entrara aqui, alterar la lista congelada seria invisible en una sesion celebrada.
DEPENDEN_DE_LAS_RESPUESTAS = ("cuestionario.yaml", "ventanas.yaml", "hoja_trader.md")
SESION = re.compile(r"^\d{4}-\d{2}-\d{2}-sesion-\d{2}$", re.ASCII)
_MES = re.compile(r"^\d{4}-\d{2}$", re.ASCII)
_HORA = re.compile(r"^\d{2}:\d{2}$", re.ASCII)
_SHA_BLOB = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
_DIA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
# Claves de config que un camino puede traer y otro no. La guardia sigue siendo estricta:
# todo lo que no este aqui ni en las obligatorias se rechaza (ADR-0036).
CLAVES_OPCIONALES = ("cobertura_material",)


class KitError(ValueError):
    """Config, mapa, vistos o paquete invalidos."""


@dataclass(frozen=True)
class Sesion:
    nombre: str
    desde: str
    hasta: str


@dataclass(frozen=True)
class Config:
    simbolo: str
    dataset_prefijo: str
    ventana_local: tuple[str, str]
    sesiones: tuple[Sesion, ...]
    anclajes: tuple[Anclaje, ...]
    min_velas_ventana: int
    etiquetas: tuple[str, ...]
    particiones: dict[str, int]
    # Hasta donde llega el MATERIAL ETIQUETADO del trader, por mes: `AAAA-MM` -> tramos
    # `(desde, hasta)` de dias del trader. Vacio = ese mes no se acota (ADR-0036).
    cobertura: dict[str, tuple[tuple[str, str], ...]]
    doc: dict[str, Any]

    @property
    def nombres_sesiones(self) -> tuple[str, ...]:
        return tuple(s.nombre for s in self.sesiones)


def _yaml(ruta: Path) -> Any:
    try:
        return leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise KitError(f"{ruta.name}: {exc}") from exc


def _hora(v: object, que: str) -> str:
    if not isinstance(v, str) or not _HORA.match(v):
        raise KitError(f"{que}: hora invalida {v!r} (HH:MM entre comillas)")
    HoraLocal(v, "UTC")  # valida el rango
    return v


def _cobertura_desde_doc(crudo: Any, nombre: str) -> dict[str, tuple[tuple[str, str], ...]]:
    """`cobertura_material`: hasta donde llega el material ETIQUETADO del trader (ADR-0036).

    SOLO TRAMOS `{desde, hasta}`. NUNCA una lista de dias cubiertos, y se rechaza por la FORMA,
    no por convenio: `docs/validation/SEPTIEMBRE-ENTRA.md` dejo escrito que un dia laborable
    dentro del rango que NO aparezca en la columna de fechas del backtest **es un dia sin
    operaciones, y eso ES su etiqueta**. Declarar la lista de dias cubiertos publicaria esas
    etiquetas por la puerta de atras, sin pasar por la de ADR-0033.

    Es ADITIVO: una entrega nueva del mismo mes ANADE un tramo, no corrige el que hay. Por eso el
    valor es una lista y no un `hasta:` suelto, que ademas no sabria expresar una entrega partida.
    """
    if crudo is None:
        return {}
    if not isinstance(crudo, dict):
        raise KitError(f"{nombre}: cobertura_material es un mapa AAAA-MM -> lista de tramos")
    salida: dict[str, tuple[tuple[str, str], ...]] = {}
    for mes, tramos in crudo.items():
        if not isinstance(mes, str) or not _MES.match(mes):
            raise KitError(f"{nombre}: cobertura_material: {mes!r} no es un mes AAAA-MM")
        if not isinstance(tramos, list) or not tramos:
            raise KitError(f"{nombre}: cobertura_material/{mes}: lista de tramos no vacia")
        pares: list[tuple[str, str]] = []
        for tramo in tramos:
            if not isinstance(tramo, dict):
                raise KitError(
                    f"{nombre}: cobertura_material/{mes}: cada tramo es un mapa con desde y "
                    f"hasta. Una lista de DIAS cubiertos no se admite: un dia laborable del "
                    f"rango que no estuviera en ella seria un dia sin operaciones, y eso es su "
                    f"etiqueta (ADR-0036)"
                )
            sobran = set(tramo) - {"desde", "hasta", "entregado_el", "fuente"}
            if not {"desde", "hasta"} <= set(tramo) or sobran:
                raise KitError(
                    f"{nombre}: cobertura_material/{mes}: tramo con desde, hasta y opcionalmente "
                    f"entregado_el y fuente"
                )
            desde, hasta = str(tramo["desde"]), str(tramo["hasta"])
            for f in (desde, hasta):
                if not _DIA.match(f):
                    raise KitError(f"{nombre}: cobertura_material/{mes}: {f!r} no es AAAA-MM-DD")
                if not f.startswith(f"{mes}-"):
                    raise KitError(f"{nombre}: cobertura_material/{mes}: {f} no es de ese mes")
            if hasta < desde:
                raise KitError(f"{nombre}: cobertura_material/{mes}: {desde}..{hasta} al reves")
            pares.append((desde, hasta))
        # Ordenados y sin solapar: dos tramos que se pisan harian ambiguo que dia esta cubierto.
        if pares != sorted(pares) or any(
            pares[i][1] >= pares[i + 1][0] for i in range(len(pares) - 1)
        ):
            raise KitError(f"{nombre}: cobertura_material/{mes}: tramos sin ordenar o solapados")
        salida[mes] = tuple(pares)
    return salida


def config_desde_doc(
    doc: Any, nombre: str, particiones_validas: Sequence[str] = PARTICIONES
) -> Config:
    """Valida un doc de config ya leido. Lo usa `cargar_config` con el fichero global y
    `comprobar` con el bloque `config:` CONGELADO dentro del paquete (ADR-0035, enmienda del
    2026-09-21): un mecanismo, dos origenes, la misma validacion.

    `particiones_validas` es el juego de nombres del camino que llama; por omision, el del kit.
    El camino de fidelidad (ADR-0036) trae los suyos, porque sus dias no son ciegos.
    """
    esperadas = {
        "simbolo",
        "dataset_prefijo",
        "ventana_local",
        "sesiones",
        "anclajes_candidatos",
        "min_velas_ventana",
        "etiquetas",
        "particiones",
    }
    if not isinstance(doc, dict) or set(doc) - set(CLAVES_OPCIONALES) != esperadas:
        raise KitError(
            f"{nombre}: claves {sorted(esperadas)} exactamente"
            f" (opcionales: {sorted(CLAVES_OPCIONALES)})"
        )
    if not isinstance(doc["simbolo"], str) or not doc["simbolo"].isalnum():
        raise KitError(f"{nombre}: simbolo invalido")
    if not isinstance(doc["dataset_prefijo"], str) or not doc["dataset_prefijo"].strip():
        raise KitError(f"{nombre}: dataset_prefijo vacio")
    ventana = doc["ventana_local"]
    if not isinstance(ventana, dict) or set(ventana) != {"desde", "hasta"}:
        raise KitError(f"{nombre}: ventana_local necesita desde y hasta")
    v_desde, v_hasta = (
        _hora(ventana["desde"], "ventana_local"),
        _hora(ventana["hasta"], "ventana_local"),
    )
    if v_hasta <= v_desde:
        raise KitError(f"{nombre}: ventana_local acaba antes de empezar")
    sesiones: list[Sesion] = []
    for s in doc["sesiones"] if isinstance(doc["sesiones"], list) else []:
        if not isinstance(s, dict) or set(s) != {"nombre", "desde", "hasta"}:
            raise KitError(f"{nombre}: cada sesion tiene nombre, desde y hasta")
        nombre_sesion = str(s["nombre"])
        if not re.match(r"^[a-z0-9-]+$", nombre_sesion):
            raise KitError(f"{nombre}: nombre de sesion {nombre_sesion!r} (solo a-z, 0-9 y guion)")
        d, h = _hora(s["desde"], nombre_sesion), _hora(s["hasta"], nombre_sesion)
        if not (v_desde <= d < h <= v_hasta):
            raise KitError(f"{nombre}: la sesion {nombre_sesion} no cabe en ventana_local")
        sesiones.append(Sesion(nombre_sesion, d, h))
    if not sesiones or len({s.nombre for s in sesiones}) != len(sesiones):
        raise KitError(f"{nombre}: sesiones vacias o con nombres repetidos")
    anclajes: list[Anclaje] = []
    for a in doc["anclajes_candidatos"] if isinstance(doc["anclajes_candidatos"], list) else []:
        if not isinstance(a, dict) or set(a) != {
            "etiqueta",
            "hora",
            "huso",
            "coincide_con_sesiones",
        }:
            raise KitError(
                f"{nombre}: cada anclaje tiene etiqueta, hora, huso y coincide_con_sesiones"
            )
        try:
            HoraLocal(str(a["hora"]), str(a["huso"]))
            ZoneInfo(str(a["huso"]))
        except (ValueError, KeyError, OSError) as exc:
            raise KitError(f"{nombre}: anclaje {a.get('etiqueta')!r}: {exc}") from exc
        if not isinstance(a["coincide_con_sesiones"], bool):
            raise KitError(f"{nombre}: coincide_con_sesiones debe ser true/false")
        anclajes.append(
            Anclaje(str(a["etiqueta"]), str(a["hora"]), str(a["huso"]), a["coincide_con_sesiones"])
        )
    if not anclajes or len({a.etiqueta for a in anclajes}) != len(anclajes):
        raise KitError(f"{nombre}: anclajes vacios o con etiquetas repetidas")
    if sum(1 for a in anclajes if a.coincide_con_sesiones) != 1:
        raise KitError(f"{nombre}: exactamente un anclaje coincide con las sesiones")
    minimo = doc["min_velas_ventana"]
    if isinstance(minimo, bool) or not isinstance(minimo, int) or minimo < 1:
        raise KitError(f"{nombre}: min_velas_ventana debe ser un entero >= 1")
    etiquetas = doc["etiquetas"]
    if (
        not isinstance(etiquetas, list)
        or not etiquetas
        or len(set(etiquetas)) != len(etiquetas)
        or not all(isinstance(e, str) and re.match(r"^[a-z_]+$", e) for e in etiquetas)
    ):
        raise KitError(
            f"{nombre}: etiquetas debe ser una lista de nombres en minusculas sin repetir"
        )
    particiones = doc["particiones"]
    if not isinstance(particiones, dict) or set(particiones) != set(particiones_validas):
        raise KitError(f"{nombre}: particiones debe declarar {tuple(particiones_validas)}")
    for k, v in particiones.items():
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise KitError(f"{nombre}: particion {k}: entero >= 0")
    cobertura = _cobertura_desde_doc(doc.get("cobertura_material"), nombre)
    return Config(
        str(doc["simbolo"]),
        str(doc["dataset_prefijo"]),
        (v_desde, v_hasta),
        tuple(sesiones),
        tuple(anclajes),
        minimo,
        tuple(etiquetas),
        {str(k): int(v) for k, v in particiones.items()},
        cobertura,
        doc,
    )


def cargar_config(ruta: Path) -> Config:
    return config_desde_doc(_yaml(ruta), ruta.name)


def cargar_mapa(
    ruta: Path, registro: Registro, temas_raiz: frozenset[str]
) -> dict[str, EntradaMapa]:
    doc = _yaml(ruta)
    if (
        not isinstance(doc, dict)
        or set(doc) != {"parametros"}
        or not isinstance(doc["parametros"], dict)
    ):
        raise KitError(f"{ruta.name}: solo la clave 'parametros' (mapa)")
    salida: dict[str, EntradaMapa] = {}
    for nombre, e in doc["parametros"].items():
        if nombre not in registro.parametros:
            raise KitError(f"{ruta.name}: {nombre} no esta en el registro")
        if not isinstance(e, dict) or set(e) != {"temas"}:
            raise KitError(
                f"{ruta.name}: {nombre}: la unica clave es `temas` (F13: `opciones` las da el "
                f"registro y `ambiguedad` la da ambiguedades.yaml)"
            )
        temas = e["temas"]
        if not isinstance(temas, list) or not temas or not all(isinstance(t, str) for t in temas):
            raise KitError(f"{ruta.name}: {nombre}: temas debe ser una lista no vacia")
        for t in temas:
            if temas_raiz and t.split(".")[0] not in temas_raiz:
                raise KitError(f"{ruta.name}: {nombre}: tema {t!r} fuera de _temas.yaml")
        # Las respuestas cerradas las sostiene el registro, no el kit: si el parametro es un
        # enum se le preguntan al trader sus opciones, y si no, la pregunta va abierta.
        salida[str(nombre)] = EntradaMapa(
            tuple(temas), tuple(registro.parametros[str(nombre)].opciones or ())
        )
    return salida


def _fecha_vista(ruta: Path, que: str, valor: object) -> str:
    try:
        return date.fromisoformat(str(valor)).isoformat()
    except ValueError as exc:
        raise KitError(f"{ruta.name}: {que}: visto_el {valor!r} no es AAAA-MM-DD") from exc


def cargar_vistos_fechados(ruta: Path) -> tuple[dict[str, str], dict[str, str], dict[str, Any]]:
    """`mes -> visto_el` y `dia -> visto_el`: CUANDO vio el trader cada cosa (2026-09-17).

    Sin la fecha, un mes visto DESPUES de construir un paquete borraba lo que ese paquete pregunto:
    declarar mayo visto hacia que `kit check` de la sesion 1 -construida con mayo ciego- dijera
    "se piden 40 casos y el universo tiene 22". `visto_el` es obligatorio: sin el no se sabe a que
    paquetes afecta, y "desde siempre" es justo la suposicion que rompio la sesion 1.
    """
    doc = _yaml(ruta)
    if not isinstance(doc, dict) or set(doc) != {"meses", "dias"}:
        raise KitError(f"{ruta.name}: claves meses y dias")
    meses: dict[str, str] = {}
    for m in doc["meses"] if isinstance(doc["meses"], list) else []:
        if (
            not isinstance(m, dict)
            or not {"mes", "motivo", "fuente", "visto_el"} <= set(m)
            or not _MES.match(str(m["mes"]))
        ):
            raise KitError(
                f"{ruta.name}: cada mes tiene mes (AAAA-MM), motivo, fuente y visto_el (AAAA-MM-DD)"
            )
        meses[str(m["mes"])] = _fecha_vista(ruta, str(m["mes"]), m["visto_el"])
    dias: dict[str, str] = {}
    for d in doc["dias"] if isinstance(doc["dias"], list) else []:
        if not isinstance(d, dict) or not {"dia", "motivo", "visto_el"} <= set(d):
            raise KitError(f"{ruta.name}: cada dia tiene dia, motivo y visto_el")
        try:
            dia = date.fromisoformat(str(d["dia"])).isoformat()
        except ValueError as exc:
            raise KitError(f"{ruta.name}: dia {d['dia']!r} no es AAAA-MM-DD") from exc
        dias[dia] = _fecha_vista(ruta, dia, d["visto_el"])
    return meses, dias, doc


def fecha_de_sesion(sesion: str) -> str:
    """La fecha de la REUNION en la que el trader etiqueta: la del nombre del paquete.

    Es la que decide si un mes es ciego, porque lo que importa es que el trader no lo haya visto
    cuando etiqueta, no cuando se construyo el paquete. Y es la unica fiable: el commit que anadio
    `particiones.yaml` es el del ultimo `mover_sesion` (git no sigue renombrados ahi), sin commit no
    existe, y una fecha nueva dentro del paquete romperia la reproduccion de la sesion 1.
    """
    if not SESION.match(sesion):
        raise KitError(f"sesion invalida {sesion!r} (AAAA-MM-DD-sesion-NN)")
    return sesion[:10]


def cargar_vistos(
    ruta: Path, hasta: str | None = None
) -> tuple[set[str], set[str], dict[str, Any]]:
    """Meses y dias vistos A MAS TARDAR en `hasta` (la fecha de la sesion). Sin `hasta`, todos."""
    meses, dias, doc = cargar_vistos_fechados(ruta)
    return (
        {m for m, f in meses.items() if hasta is None or f <= hasta},
        {d for d, f in dias.items() if hasta is None or f <= hasta},
        doc,
    )


def vistos_en_el_paquete(repo: Path, sesion: str, dias_del_paquete: list[str]) -> list[str]:
    """Dias de un paquete que el trader ya habia visto el dia de su sesion. Debe salir vacio."""
    meses, dias, _ = cargar_vistos(repo / DIRECTORIO_KIT / FICHERO_VISTOS, fecha_de_sesion(sesion))
    return sorted(d for d in dias_del_paquete if d[:7] in meses or d in dias)


def _dump(doc: Any) -> str:
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=True, width=100)


def _hora_local(iso: str, huso: ZoneInfo) -> str:
    from botsito.data.velas import a_datetime

    return a_datetime(parse_ts(iso)).astimezone(huso).strftime("%H:%M")


def meses_del_paquete(casos: list[Caso]) -> list[str]:
    """Meses (AAAA-MM) de los dias del paquete: lo que el trader debe confirmar que no ha visto."""
    return sorted({c.dia[:7] for c in casos})


def hoja_trader(
    sesion: str,
    config: Config,
    huso_operativa: str,
    preguntas: list[Pregunta],
    casos: list[Caso],
    asignacion: dict[str, str],
    meses: set[str],
) -> str:
    """Lo que el consultor lleva a la sesion: preguntas (bloqueantes primero, sin ids `ev-*`)
    y solo los casos `dev` con las dos rejillas H4 en hora del trader."""
    huso = ZoneInfo(huso_operativa)
    lineas = [
        f"# Sesion {sesion} · hoja del trader",
        "",
        "Condicion previa: el trader confirma por escrito que NO ha operado ni backtesteado los "
        f"meses del paquete ({', '.join(meses_del_paquete(casos)) or 'ninguno'}). Toda "
        "respuesta se anota literal (registro F09).",
        "",
        "## Preguntas",
        "",
    ]
    for p in preguntas:
        marca = " (BLOQUEANTE)" if p.bloqueante else ""
        lineas.append(f"### {p.id} · {p.titulo}{marca}")
        lineas.append(f"Pregunta: {p.enunciado}")
        opciones = p.respuesta_esperada.get("opciones")
        if opciones:
            lineas.append(f"Opciones: {' / '.join(opciones)} (u otra, literal)")
        lineas.append("Casos:")
        for ejemplo in p.casos:
            foto = f" · fotograma {ejemplo['fotograma']}" if ejemplo.get("fotograma") else ""
            lineas.append(f'- {ejemplo["video"]} {ejemplo["t0"]}: "{ejemplo["cita"]}"{foto}')
        lineas.append("Respuesta del trader: ______________________  ¿confirma? [ ]")
        lineas.append("")
    dev = [c for c in casos if asignacion.get(c.id) == "dev"]
    lineas += [
        "## Ventanas de etiquetado (solo `dev`)",
        "",
        f"Dia operativo {config.ventana_local[0]}-{config.ventana_local[1]} ({huso_operativa}). "
        f"Sesiones: {', '.join(f'{s.nombre} ({s.desde}-{s.hasta})' for s in config.sesiones)}. "
        f"Decision por sesion: {' / '.join(config.etiquetas)}. Gramatica: "
        f"`{config.sesiones[0].nombre}: venta@08:37 e=... sl=... tp=...; "
        f"{config.sesiones[-1].nombre}: no_trade`.",
        "",
        "| Caso | Dia | Ventana UTC | "
        + " | ".join(
            f"H4 {a.etiqueta}{' (sesiones)' if a.coincide_con_sesiones else ''}"
            for a in config.anclajes
        )
        + " |",
        "|---|---|---|" + "---|" * len(config.anclajes),
    ]
    for c in dev:
        rejillas = []
        for a in config.anclajes:
            horas = [_hora_local(x, huso) for x in c.limites_h4.get(a.etiqueta, [])]
            rejillas.append(" ".join(horas))
        lineas.append(
            f"| {c.id} | {c.dia} | {c.desde_utc}-{c.hasta_utc} | " + " | ".join(rejillas) + " |"
        )
    lineas += [
        "",
        f"{len(dev)} casos dev de {len(casos)} del paquete (los holdout no se muestran).",
        "",
    ]
    return "\n".join(lineas)


@dataclass
class Paquete:
    sesion: str
    seed: int
    ficheros: dict[str, str]
    casos: list[Caso]
    excluidos: list[Excluido]
    preguntas: list[Pregunta]
    asignacion: dict[str, str]
    universo: int = 0


def _cargar_todo(
    repo: Path,
    sesion: str | None = None,
) -> tuple[
    Config,
    Registro,
    list[Ambiguedad],
    dict[str, EntradaMapa],
    set[str],
    set[str],
    list[EvidenceItem],
]:
    kit = repo / DIRECTORIO_KIT
    config = cargar_config(kit / FICHERO_CONFIG)
    try:
        registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    except RegistroError as exc:
        raise KitError(str(exc)) from exc
    try:
        ambiguedades = cargar_ambiguedades(repo / FICHERO_AMBIGUEDADES)
    except AmbiguedadError as exc:
        raise KitError(str(exc)) from exc
    ruta_temas = repo / FICHERO_TEMAS
    temas_raiz = cargar_temas(ruta_temas).raices if ruta_temas.is_file() else frozenset()
    mapa = cargar_mapa(kit / FICHERO_MAPA, registro, temas_raiz)
    # Solo lo visto a mas tardar el dia de la sesion: un mes visto despues no borra lo que un
    # paquete anterior pregunto (2026-09-17).
    meses, dias, _ = cargar_vistos(
        kit / FICHERO_VISTOS, fecha_de_sesion(sesion) if sesion is not None else None
    )
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    return config, registro, ambiguedades, mapa, meses, dias, items


def manifiestos_del_prefijo(
    repo: Path, config: Config, datasets: Sequence[str] | None = None
) -> list[dict[str, Any]]:
    """Los manifiestos con los que se calcula un universo.

    Con `datasets` -la lista CONGELADA en el paquete- devuelve exactamente esos, y falla si falta
    alguno: un paquete existente se recompone con lo que dice que uso, no con lo que haya hoy en
    disco. Sin `datasets` devuelve todos los del prefijo, que es lo correcto para un paquete NUEVO:
    se construye con lo que hay (ADR-0035).
    """
    del_disco = []
    for ruta in manifiestos(repo):
        m = cargar_manifiesto(ruta)
        if str(m["dataset_id"]).startswith(config.dataset_prefijo):
            del_disco.append(m)
    if datasets is None:
        return del_disco
    por_id = {str(m["dataset_id"]): m for m in del_disco}
    faltan = [d for d in datasets if d not in por_id]
    if faltan:
        raise KitError(
            f"datasets congelados que ya no estan en data/manifests: {', '.join(sorted(faltan))}"
        )
    return [por_id[d] for d in datasets]


def datasets_que_faltan_en_disco(
    repo: Path, carpeta_datos: Path, config: Config, datasets: Sequence[str] | None = None
) -> list[str]:
    """Datasets cuyos ficheros no estan en `carpeta_datos`, por id y ordenados.

    Antes esto era un booleano global (`hay_datos_del_kit`) sobre TODOS los datasets del prefijo, y
    bastaba con que uno solo -aunque fuera ajeno al paquete- no tuviera sus ficheros para que
    `kit check` saliera con 0 sin comprobar nada y sin declarar ninguna lectura. Un exit 0 que no
    comprueba nada es la misma clase de defecto que ADR-0035 arregla, asi que ahora se NOMBRAN.
    """
    return sorted(
        str(m["dataset_id"])
        for m in manifiestos_del_prefijo(repo, config, datasets)
        if not all((carpeta_datos / str(f["ruta"])).is_file() for f in m["ficheros"])
    )


def hay_datos_del_kit(
    repo: Path, carpeta_datos: Path, config: Config, datasets: Sequence[str] | None = None
) -> bool:
    """Si estan en `carpeta_datos` los ficheros de los datasets pedidos (los congelados, o los del
    prefijo si no se pasa lista)."""
    manifiestos_kit = manifiestos_del_prefijo(repo, config, datasets)
    return bool(manifiestos_kit) and not datasets_que_faltan_en_disco(
        repo, carpeta_datos, config, datasets
    )


def lectura_de_velas(
    repo: Path,
    carpeta_datos: Path,
    asignacion: dict[str, str],
    datasets: Sequence[str] | None = None,
    config: Config | None = None,
    reservadas: Sequence[str] | None = None,
) -> list[str]:
    """Lo que `kit build` y `kit check` declaran en su salida ANTES de leer velas (ADR-0033).

    Construir o comprobar un paquete lee las velas M1 de TODOS los dias del universo, reservados
    incluidos: que dias son reservados depende de cuales entran, y eso de sus velas. No es abrir un
    holdout (ADR-0021 §1), pero hasta el 2026-09-17 pasaba en silencio, y el 2026-09-13 paso dos
    veces sin que nadie lo viera en la salida. Sin datos no se lee nada y no se declara nada.

    Dice CUANTOS dias reservados y de que particion, sin fechas, sin cifras de velas y sin precios:
    las fechas estan en `particiones.yaml`, y la salida puede acabar delante del trader.
    """
    config = config or cargar_config(repo / DIRECTORIO_KIT / FICHERO_CONFIG)
    if not hay_datos_del_kit(repo, carpeta_datos, config, datasets):
        return []
    if reservadas is None:
        from botsito.cases.holdout import PARTICIONES_RESERVADAS

        reservadas = PARTICIONES_RESERVADAS

    # Los que se van a leer DE VERDAD: con un paquete existente, su lista congelada; si no, el
    # disco. Declarar de mas es menos peligroso que declarar de menos, pero sigue siendo una
    # declaracion falsa en el unico fichero que existe para ser creible (ADR-0033, ADR-0035).
    leidos = sorted(str(m["dataset_id"]) for m in manifiestos_del_prefijo(repo, config, datasets))
    lineas = [
        f"LECTURA: se leen las velas M1 de {', '.join(leidos)} en {carpeta_datos.name}/ -todos "
        f"los dias del universo, reservados incluidos- para recalcular n_velas, sha256 y limites "
        f"H4 de sus ventanas. Ninguna etiqueta y ningun precio: no es abrir un holdout (ADR-0021 "
        f"§1), y se declara (ADR-0033)"
    ]
    # RECUENTO y no fechas (decision del consultor, 2026-09-17): las fechas ya estan en
    # `particiones.yaml` para quien las quiera, la lectura es siempre la misma, y esta salida puede
    # acabar delante del trader, a quien la hoja le oculta esos dias por contrato.
    por_particion = {p: sum(1 for x in asignacion.values() if x == p) for p in reservadas}
    total = sum(por_particion.values())
    if total:
        detalle = ", ".join(f"{p} {n}" for p, n in por_particion.items() if n)
        lineas.append(f"LECTURA: {total} dias reservados cuyas velas se leen: {detalle}")
    return lineas


def construir(
    repo: Path,
    carpeta_datos: Path,
    sesion: str,
    seed: int,
    indice: Indice | None = None,
    datasets: Sequence[str] | None = None,
    config: Config | None = None,
) -> Paquete:
    """Construye el paquete completo en memoria. Exige los datos de los datasets en `data/`.

    `datasets` y `config` son lo CONGELADO de un paquete existente (ADR-0035 y su enmienda del
    2026-09-21): con ellos el paquete se recompone con lo que uso y no con lo que haya hoy en
    disco -ni los manifiestos de hoy, ni el `config.yaml` de hoy-. Los dos tienen el MISMO
    contrato: por omision -`None`- se lee el disco, que es lo que un paquete NUEVO tiene que
    hacer, porque `kit build` se construye con lo que hay y congelar tambien este camino dejaria
    al proyecto sin poder hacer ningun paquete.
    """
    if not SESION.match(sesion):
        raise KitError(f"sesion invalida {sesion!r} (AAAA-MM-DD-sesion-NN)")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise KitError("el seed debe ser un entero >= 0")
    del_disco, registro, ambiguedades, mapa, meses, dias, items = _cargar_todo(repo, sesion)
    config = del_disco if config is None else config
    huso = registro.texto("huso_operativa")
    try:
        huso_canonico(huso)
    except HusoDesconocidoError as exc:
        raise KitError(f"huso_operativa: {exc}") from exc
    vivos = activos(list(items))
    abiertas = contradicciones.detectar(vivos)
    # TODOS los items para la EXISTENCIA de la cita, y solo los vivos para la contradiccion: una
    # ambiguedad cita la evidencia que ABRIO la pregunta, y esa evidencia existe aunque despues se
    # haya supersedido. Miraba solo los vivos, asi que el 2026-09-12 -al cerrar `stop.nivel` con
    # los primeros `supersede` sobre evidencia del proyecto- `kit check` dijo que A-10, A-11 y
    # A-18 citaban evidencia "que no existe". `validation/knowledge.py` ya lo hacia bien: eran dos
    # llamadas a la misma comprobacion diciendo cosas distintas.
    problemas_amb = validar_ambiguedades(
        ambiguedades, {i.id for i in items}, set(registro.nombres()), {c["tema"] for c in abiertas}
    )
    if problemas_amb:
        raise KitError("ambiguedades: " + "; ".join(problemas_amb))
    indice = indice or construir_indice(repo, carpeta_datos)
    try:
        preguntas = generar(
            registro,
            ambiguedades,
            mapa,
            abiertas,
            vivos,
            indice.fotograma_en,
        )
    except CuestionarioError as exc:
        raise KitError(str(exc)) from exc
    try:
        manif = manifiestos_del_prefijo(repo, config, datasets)
        if not manif:
            raise KitError(
                f"ningun dataset con prefijo {config.dataset_prefijo!r} en data/manifests"
            )
        casos, excluidos = universo(
            manif,
            carpeta_datos,
            config.simbolo,
            huso,
            config.ventana_local,
            list(config.anclajes),
            config.min_velas_ventana,
            meses,
            dias,
        )
        asignacion = asignar([c.id for c in casos], seed, config.particiones)
    except (DatasetError, VentanaError, ParticionError, VelaInvalidaError) as exc:
        raise KitError(str(exc)) from exc
    elegidos = [c for c in casos if c.id in asignacion]
    # La guardia, en el camino de `kit build`, `kit check` y `mover_sesion`: un paquete no puede
    # sortear un dia que el trader ya habia visto el dia de su sesion. El filtro de `_cargar_todo`
    # ya lo impide; esto FALLA si algun dia se colara igual, en vez de dejarlo pasar.
    colados = vistos_en_el_paquete(repo, sesion, [c.dia for c in elegidos])
    if colados:
        raise KitError(
            f"{sesion}: el paquete sortearia dias que el trader ya habia visto el "
            f"{fecha_de_sesion(sesion)}: {', '.join(colados)} (vistos.yaml)"
        )
    ficheros = {
        "cuestionario.yaml": _dump(
            {"sesion": sesion, "preguntas": [p.como_dict() for p in preguntas]}
        ),
        "ventanas.yaml": _dump(
            {
                "sesion": sesion,
                "config": config.doc,
                "huso_operativa": huso,
                "casos": [c.como_dict() for c in elegidos],
                "datasets": sorted(str(m["dataset_id"]) for m in manif),
                "universo": len(casos),
                "excluidos": [{"dia": e.dia, "motivo": e.motivo} for e in excluidos],
            }
        ),
        "particiones.yaml": _dump(
            {
                "sesion": sesion,
                "seed": seed,
                "cupos": config.particiones,
                "asignacion": {c.id: asignacion[c.id] for c in elegidos},
            }
        ),
        "hoja_trader.md": hoja_trader(sesion, config, huso, preguntas, elegidos, asignacion, meses),
    }
    return Paquete(sesion, seed, ficheros, elegidos, excluidos, preguntas, asignacion, len(casos))


def escribir(repo: Path, paquete: Paquete) -> Path:
    carpeta = repo / DIRECTORIO_KIT / paquete.sesion
    if carpeta.exists():
        raise KitError(
            f"ya existe {carpeta.relative_to(repo).as_posix()}: un paquete no se sobreescribe"
        )
    temporal = carpeta.with_name(f"_{carpeta.name}.tmp")
    if temporal.exists():
        raise KitError(f"queda un temporal {temporal.name}: borralo y repite")
    temporal.mkdir(parents=True)
    try:
        for nombre, texto in paquete.ficheros.items():
            (temporal / nombre).write_text(texto, encoding="utf-8", newline="\n")
        temporal.rename(carpeta)
    except OSError:
        for f in temporal.glob("*"):
            f.unlink()
        temporal.rmdir()
        raise
    return carpeta


def _leer(carpeta: Path, nombre: str) -> str:
    try:
        return (carpeta / nombre).read_text(encoding="utf-8").replace("\r\n", "\n")
    except OSError as exc:
        raise KitError(f"{carpeta.name}/{nombre}: {exc}") from exc


def esquema_paquete(
    repo: Path, sesion: str
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Carga estricta de los tres YAML del paquete (sin datos)."""
    carpeta = repo / DIRECTORIO_KIT / sesion
    if not carpeta.is_dir():
        raise KitError(f"no existe el paquete {sesion}")
    faltan = [f for f in FICHEROS_PAQUETE if not (carpeta / f).is_file()]
    if faltan:
        raise KitError(f"{sesion}: faltan {faltan}")
    docs = []
    for nombre in ("cuestionario.yaml", "ventanas.yaml", "particiones.yaml"):
        doc = _yaml(carpeta / nombre)
        if not isinstance(doc, dict) or doc.get("sesion") != sesion:
            raise KitError(f"{sesion}/{nombre}: 'sesion' debe ser {sesion}")
        docs.append(doc)
    cuestionario, ventanas, particiones = docs
    preguntas = cuestionario.get("preguntas")
    if not isinstance(preguntas, list) or not all(isinstance(p, dict) for p in preguntas):
        raise KitError(f"{sesion}/cuestionario.yaml: preguntas debe ser una lista de mapas")
    for p in preguntas:
        if not isinstance(p.get("casos"), list) or not all(isinstance(c, dict) for c in p["casos"]):
            raise KitError(
                f"{sesion}/cuestionario.yaml: {p.get('id')}: casos debe ser una lista de mapas"
            )
    casos = ventanas.get("casos")
    if not isinstance(casos, list) or not all(isinstance(c, dict) for c in casos):
        raise KitError(f"{sesion}/ventanas.yaml: casos debe ser una lista de mapas")
    asignacion = particiones.get("asignacion")
    if not isinstance(asignacion, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in asignacion.items()
    ):
        raise KitError(f"{sesion}/particiones.yaml: asignacion debe ser un mapa caso -> particion")
    seed = particiones.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise KitError(f"{sesion}/particiones.yaml: seed invalido")
    return cuestionario, ventanas, particiones


def _datasets_congelados(
    sesion: str, ventanas: dict[str, Any], problemas: list[str]
) -> list[str] | None:
    """La lista congelada del paquete, validada. `None` si no se puede seguir (ADR-0035)."""
    crudo = ventanas.get("datasets")
    if crudo is None:
        problemas.append(
            f"{sesion}/ventanas.yaml: sin `datasets`: el universo del paquete no esta congelado y "
            f"no hay con que reproducirlo (ADR-0035)"
        )
        return None
    if not isinstance(crudo, list) or not all(isinstance(d, str) and d for d in crudo):
        problemas.append(f"{sesion}/ventanas.yaml: `datasets` debe ser una lista de ids")
        return None
    lista = [str(d) for d in crudo]
    if lista != sorted(set(lista)):
        problemas.append(f"{sesion}/ventanas.yaml: `datasets` con repetidos o sin ordenar")
        return None
    de_casos = {
        str(c.get("dataset_id")) for c in ventanas.get("casos") or [] if isinstance(c, dict)
    }
    huerfanos = sorted(de_casos - set(lista))
    if huerfanos:
        problemas.append(
            f"{sesion}/ventanas.yaml: casos que citan datasets fuera de `datasets`: "
            f"{', '.join(huerfanos)}"
        )
        return None
    return lista


def cargar_anclas(
    repo: Path, directorio: str = DIRECTORIO_KIT, patron: re.Pattern[str] = SESION
) -> dict[str, dict[str, str]]:
    """`<directorio>/anclas.yaml`: id -> fichero -> sha del blob. Vacio si no existe.

    `directorio` y `patron` los trae el camino que llama: el kit usa sesiones con fecha; el de
    fidelidad (ADR-0036), artefactos sin fecha, porque alli no hay reunion que fechar.
    """
    ruta = repo / directorio / FICHERO_ANCLAS
    if not ruta.is_file():
        return {}
    doc = _yaml(ruta)
    if doc is None:
        return {}
    if not isinstance(doc, dict):
        raise KitError(f"{FICHERO_ANCLAS}: se espera un mapa sesion -> fichero -> sha")
    anclas: dict[str, dict[str, str]] = {}
    for sesion, entrada in doc.items():
        if not isinstance(sesion, str) or not patron.match(sesion):
            raise KitError(f"{FICHERO_ANCLAS}: {sesion!r} no es una sesion")
        if not isinstance(entrada, dict) or set(entrada) - set(FICHEROS_ANCLADOS):
            raise KitError(f"{FICHERO_ANCLAS}: {sesion}: ficheros {list(FICHEROS_ANCLADOS)}")
        for nombre, sha in entrada.items():
            if not isinstance(sha, str) or not _SHA_BLOB.match(sha):
                raise KitError(
                    f"{FICHERO_ANCLAS}: {sesion}/{nombre}: {sha!r} no es un sha de blob (40 hex; "
                    f"lo da `git hash-object {DIRECTORIO_KIT}/{sesion}/{nombre}`)"
                )
        anclas[sesion] = {str(k): str(v) for k, v in entrada.items()}
    return anclas


CABECERA_ANCLAS = """\
# Anclas anti-manipulacion de los paquetes del kit (ADR-0035, enmienda del 2026-09-21).
#
# Un paquete congela dentro de si mismo el universo (`datasets:`) y los cupos (el bloque
# `config:`), y se recompone con ellos. Congelar solo es legitimo si editar lo congelado a mano
# se VE, y la comparacion byte a byte no lo ve entero: `anclajes_candidatos`, `sesiones` y
# `etiquetas` solo alimentan ficheros que una sesion celebrada exime. Estas anclas cierran eso.
#
# Es el sha del BLOB de cada fichero -`git hash-object <ruta>`-, no el de un commit: el blob
# cambia con cualquier byte del fichero y con nada mas, y sobrevive a un rebase. Mismo patron que
# `preregistro_blob` (ADR-0033).
#
# GENERADO por `botsito kit anclar --sesion <s>`. Re-anclar un paquete que cambio es un acto
# EXPLICITO (`--reanclar`) y su diff se ve aqui, no como efecto colateral de regenerar nada.
"""


def anclas_del_arbol(repo: Path, sesion: str, directorio: str = DIRECTORIO_KIT) -> dict[str, str]:
    """Los sha de blob de los ficheros anclados de una sesion tal como estan AHORA en el disco."""
    salida: dict[str, str] = {}
    for nombre in FICHEROS_ANCLADOS:
        ruta = f"{directorio}/{sesion}/{nombre}"
        sha = blob_en_arbol(repo, ruta)
        if sha is None:
            raise KitError(f"{ruta}: no existe, o git no puede calcular su blob")
        salida[nombre] = sha
    return salida


def escribir_anclas(
    repo: Path, anclas: dict[str, dict[str, str]], directorio: str = DIRECTORIO_KIT
) -> Path:
    ruta = repo / directorio / FICHERO_ANCLAS
    cuerpo = _dump({s: dict(sorted(v.items())) for s, v in sorted(anclas.items())})
    ruta.write_text(CABECERA_ANCLAS + cuerpo, encoding="utf-8", newline="\n")
    return ruta


def problemas_de_ancla(
    repo: Path,
    sesion: str,
    anclas: dict[str, dict[str, str]],
    directorio: str = DIRECTORIO_KIT,
    comando: str = "kit anclar",
) -> list[str]:
    """El ancla anti-manipulacion de un paquete (ADR-0035, enmienda del 2026-09-21).

    Congelar algo dentro de un fichero solo es legitimo si editarlo a mano se ve. Con `datasets:`
    se ve: cambiarlo cambia el universo y `particiones.yaml` deja de reproducirse. Con el bloque
    `config:` NO se ve entero: `particiones` si -cambia la asignacion-, pero `anclajes_candidatos`,
    `sesiones` y `etiquetas` solo alimentan ficheros que una sesion celebrada exime, y editarlos
    daba exit 0 (medido el 2026-09-21). El ancla cubre el fichero ENTERO y cierra eso.

    El patron es el de `preregistro_blob` (ADR-0033), con sus tres requisitos:

      1. VIVE FUERA del fichero que ata (`anclas.yaml`, no `ventanas.yaml`): un ancla dentro de lo
         que ancla la reescribe quien reescriba el fichero.
      2. Es el sha del BLOB, no el de un commit: el blob cambia con cualquier byte del fichero y
         con nada mas, sobrevive a un rebase o a un merge y no se mueve porque otro commit toque
         otra cosa. `ventanas.yaml` tiene ya dos commits (`6266738` y el de ADR-0035) y un ancla
         de commit lo habria dado por alterado sin que su contenido lo estuviera.
      3. RE-ANCLAR ES EXPLICITO: cambiar el paquete obliga a editar `anclas.yaml`, que es otro
         fichero, en un diff que se ve y con su trailer `Fuente:`. No se cuela como efecto
         colateral de regenerar nada.

    Y NO depende de que existan etiquetas. La guardia de ancestro se desentiende con
    `if not etiquetas: continue`, y hoy no hay ni un `LABEL_CASE` en el repositorio: si el ancla
    heredara ese `continue` no ataria nada justo en el periodo en el que hace falta.
    """
    problemas: list[str] = []
    declaradas = anclas.get(sesion, {})
    for nombre in FICHEROS_ANCLADOS:
        ruta = f"{directorio}/{sesion}/{nombre}"
        en_head = blob_en_head(repo, ruta)
        if en_head is None:
            # Sin commitear -o sin git- no hay nada que anclar todavia: el paquete se ancla en el
            # mismo commit que lo mete. Lo que no esta commiteado lo vigilan las otras guardias.
            continue
        declarado = declaradas.get(nombre)
        if declarado is None:
            problemas.append(
                f"{sesion}/{nombre}: sin ancla en {FICHERO_ANCLAS}: lo congelado dentro del "
                f"paquete no esta atado contra manipulacion (ADR-0035, enmienda del 2026-09-21); "
                f"se declara con `botsito {comando} {sesion}`"
            )
            continue
        if declarado != en_head:
            problemas.append(
                f"{sesion}/{nombre}: su ancla dice {declarado[:12]}… y lo commiteado es "
                f"{en_head[:12]}…: el paquete cambio despues de anclarse. Si el cambio es "
                f"legitimo se re-ancla a proposito (`botsito {comando} {sesion} --reanclar`), "
                f"que deja el diff a la vista"
            )
            continue
        en_arbol = blob_en_arbol(repo, ruta)
        if en_arbol is not None and en_arbol != declarado:
            problemas.append(
                f"{sesion}/{nombre}: editado en el arbol de trabajo ({en_arbol[:12]}…) y no "
                f"coincide con su ancla ({declarado[:12]}…)"
            )
    return problemas


def comprobar(
    repo: Path, carpeta_datos: Path, sesion: str, celebrada: bool = False
) -> tuple[list[str], list[str]]:
    """PURO: recompone el paquete y compara byte a byte (tras normalizar CRLF). Sin datos en
    `data/`, comprueba solo el esquema y avisa."""
    problemas: list[str] = []
    avisos: list[str] = []
    cuestionario, ventanas, particiones = esquema_paquete(repo, sesion)
    seed = int(particiones["seed"])
    # El bloque `config:` del paquete se USA, no se compara contra el `config.yaml` de hoy
    # (ADR-0035, enmienda del 2026-09-21). Comparar hacia el fichero global hacia DOS trabajos en
    # una sola linea y por eso estorbaba: probaba la reproduccion del paquete Y avisaba de que el
    # config global habia derivado. Lo primero se hace ahora con el congelado; lo segundo vive en
    # `validar_paquetes` como AVISO, porque un paquete viejo no tiene por que saber nada del
    # config de hoy y porque editar `config.yaml` para el paquete SIGUIENTE es el camino normal.
    doc_congelado = ventanas.get("config")
    if doc_congelado is None:
        problemas.append(
            f"{sesion}/ventanas.yaml: sin bloque `config`: los cupos del paquete no estan "
            f"congelados y no hay con que reproducirlo (ADR-0035, enmienda del 2026-09-21)"
        )
        return problemas, avisos
    try:
        config = config_desde_doc(doc_congelado, f"{sesion}/ventanas.yaml:config")
    except KitError as exc:
        problemas.append(str(exc))
        return problemas, avisos
    # El universo y los cupos de un paquete se congelan DENTRO del paquete. Ninguno de los dos
    # puede compararse contra nada: el disco crece a proposito -meses nuevos- y el config global
    # evoluciona a proposito -el paquete siguiente quiere otros cupos-, y esas eran justo las dos
    # averias (ADR-0035 y su enmienda). Lo congelado se USA: es con lo que se recompone el
    # paquete, y lo que lo prueba es que el paquete siga reproduciendose byte a byte con ello.
    # Tres condiciones, y ninguna es un permiso:
    #
    #   1. Sin `datasets:` no se comprueba nada: PROBLEMA, no aviso. Un paquete sin universo
    #      congelado no tiene con que reproducirse, y dejarlo pasar seria devolver el defecto.
    #   2. La lista se valida contra los manifiestos, que son inmutables: ids existentes, ordenada
    #      y sin repetidos, y contiene todos los `casos[].dataset_id`. Lo que no necesita velas se
    #      comprueba ademas en `knowledge validate` (`validar_paquetes`), que corre sin `data/`.
    #   3. Se comprueba AQUI, fuera del bucle de comparacion, y NO entra en
    #      DEPENDEN_DE_LAS_RESPUESTAS: una diferencia en `datasets:` no sale de ninguna respuesta
    #      del trader, asi que nunca puede bajar a aviso. Si bajara, alterar la lista congelada
    #      quedaria invisible en una sesion celebrada, que son todas las que importan.
    #
    # Y una cuarta, que es de los CUPOS y hay que decirla porque la falsabilidad del bloque
    # `config:` no es uniforme: editar `particiones` dentro del congelado cambia la asignacion y
    # `particiones.yaml` -que no se exime NUNCA- deja de reproducirse, asi que se ve. Pero
    # `anclajes_candidatos`, `sesiones` y `etiquetas` solo alimentan `ventanas.yaml` y
    # `hoja_trader.md`, que en una sesion celebrada SI se eximen: editarlos ahi no lo ve nadie.
    # Medido el 2026-09-21 (exit 0, "sin diferencias que no explique la sesion celebrada"). Por
    # eso el bloque congelado se ata FUERA, con el ancla de `anclas.yaml` (`problemas_de_ancla`).
    congelados = _datasets_congelados(sesion, ventanas, problemas)
    if congelados is None:
        return problemas, avisos
    faltan = datasets_que_faltan_en_disco(repo, carpeta_datos, config, congelados)
    if faltan:
        avisos.append(
            f"{sesion}: datos ausentes en {carpeta_datos.name}/ de {', '.join(faltan)}: solo "
            f"esquema"
        )
        return problemas, avisos
    nuevo = construir(repo, carpeta_datos, sesion, seed, datasets=congelados, config=config)
    carpeta = repo / DIRECTORIO_KIT / sesion
    for nombre, texto in nuevo.ficheros.items():
        if _leer(carpeta, nombre) == texto:
            continue
        if celebrada and nombre in DEPENDEN_DE_LAS_RESPUESTAS:
            # El paquete de una sesion ya celebrada es historico: dice lo que se le pregunto al
            # trader ese dia. Regenerarlo hoy da otra cosa a proposito, porque el registro ya
            # tiene las respuestas y el cuestionario ya no preguntaria lo mismo. Exigir que se
            # reproduzca seria exigir que el proyecto no aprenda nada.
            #
            # Pero SOLO estos tres. `particiones.yaml` no depende de las respuestas -sale de los
            # hashes de los casos y del seed-, asi que sigue teniendo que reproducirse byte a
            # byte: es la prueba de que las particiones se fijaron antes de etiquetar, y bajarla
            # a AVISO dejaba a `kit check` sin poder denunciar que alguien la reescribiera.
            avisos.append(
                f"{sesion}/{nombre}: ya no se genera igual, y es lo esperado: la sesion se "
                f"celebro y sus respuestas estan en el registro"
            )
            continue
        problemas.append(f"{sesion}/{nombre}: difiere de lo que se genera hoy")
    return problemas, avisos


def sesiones_del_kit(repo: Path) -> list[str]:
    kit = repo / DIRECTORIO_KIT
    if not kit.is_dir():
        return []
    return sorted(p.name for p in kit.iterdir() if p.is_dir() and SESION.match(p.name))


def _problemas_de_vistos(repo: Path, sesion: str, ventanas: dict[str, Any]) -> list[str]:
    """Meses vistos (2026-09-17), para `knowledge validate` y sin datos, asi que corre en CI.

    Un paquete escrito no puede tener dias que el trader ya habia visto el dia de su sesion. Y lo
    que excluyo como visto tiene que seguir fechado a mas tardar ese dia: poner a una entrada ya
    usada una fecha posterior -o borrarla- la saca del paquete y rompe su reproduccion, y eso solo
    lo veria `kit check` con `data/` presente. Sin `vistos.yaml` no hay nada visto que comprobar.
    """
    ruta = repo / DIRECTORIO_KIT / FICHERO_VISTOS
    if not ruta.is_file():
        return []
    try:
        meses_todos, dias_todos, _ = cargar_vistos(ruta)
        meses, dias, _ = cargar_vistos(ruta, fecha_de_sesion(sesion))
    except KitError as exc:
        return [str(exc)]
    casos = [str(c.get("dia")) for c in ventanas.get("casos") or [] if isinstance(c, dict)]
    problemas: list[str] = []
    colados = sorted(d for d in casos if d[:7] in meses or d in dias)
    if colados:
        problemas.append(
            f"{sesion}: tiene dias que el trader ya habia visto el dia de su sesion: "
            f"{', '.join(colados)} (vistos.yaml)"
        )
    for e in ventanas.get("excluidos") or []:
        if not isinstance(e, dict):
            continue
        dia, motivo = str(e.get("dia")), str(e.get("motivo"))
        if motivo == "mes visto por el trader" and dia[:7] not in meses:
            estado = (
                "tiene visto_el posterior a la sesion" if dia[:7] in meses_todos else "ya no esta"
            )
            problemas.append(
                f"{sesion}: excluyo {dia} como mes visto, y en vistos.yaml {dia[:7]} {estado}"
            )
        elif motivo == "dia visto por el trader" and dia not in dias:
            estado = "tiene visto_el posterior a la sesion" if dia in dias_todos else "ya no esta"
            problemas.append(f"{sesion}: excluyo {dia} como dia visto, y en vistos.yaml {estado}")
    return problemas


def validar_paquetes(
    repo: Path,
    registros: list[FeedbackRecord],
    ids_evidencia: set[str],
    ids_datasets: set[str],
) -> tuple[list[str], list[str]]:
    """Para `knowledge validate`: esquema, ids unicos, evidencia y datasets existentes, y la
    guardia de particiones: el commit que anadio `particiones.yaml` es ancestro del commit que
    anadio el primer `LABEL_CASE` de esa sesion (y distinto de el)."""
    problemas: list[str] = []
    avisos: list[str] = []
    try:
        anclas = cargar_anclas(repo)
    except KitError as exc:
        problemas.append(str(exc))
        anclas = {}
    try:
        doc_global = cargar_config(repo / DIRECTORIO_KIT / FICHERO_CONFIG).doc
    except KitError:
        doc_global = None  # lo denuncia `kit check`; aqui solo sirve para el aviso de deriva
    for sesion in sesiones_del_kit(repo):
        try:
            cuestionario, ventanas, particiones = esquema_paquete(repo, sesion)
        except KitError as exc:
            problemas.append(str(exc))
            continue
        pids = [str(p.get("id")) for p in cuestionario.get("preguntas") or []]
        if len(set(pids)) != len(pids) or not pids:
            problemas.append(f"{sesion}: ids de pregunta repetidos o sin preguntas")
        for p in cuestionario.get("preguntas") or []:
            evs = [str(c.get("evidencia")) for c in p.get("casos") or []]
            if not evs:
                problemas.append(f"{sesion}: {p.get('id')} sin casos")
            for e in evs:
                if e not in ids_evidencia:
                    problemas.append(f"{sesion}: {p.get('id')} cita evidencia inexistente {e}")
        # El universo congelado (ADR-0035), con lo que se puede comprobar SIN velas: que la lista
        # exista, que sus ids sigan en data/manifests -si alguien borra un manifiesto, el paquete
        # deja de poder reproducirse y aqui se ve sin datos- y que ningun caso cite uno que no
        # este. Lo demas lo prueba `kit check` reproduciendo el paquete byte a byte.
        congelados = ventanas.get("datasets")
        if congelados is None:
            problemas.append(
                f"{sesion}/ventanas.yaml: sin `datasets`: el universo del paquete no esta "
                f"congelado (ADR-0035)"
            )
        elif not isinstance(congelados, list) or [str(d) for d in congelados] != sorted(
            {str(d) for d in congelados}
        ):
            problemas.append(
                f"{sesion}/ventanas.yaml: `datasets` debe ser una lista ordenada y sin repetidos"
            )
        else:
            for d in congelados:
                if str(d) not in ids_datasets:
                    problemas.append(
                        f"{sesion}/ventanas.yaml: `datasets` cita {d}, que ya no esta en "
                        f"data/manifests: el paquete no se puede reproducir"
                    )
        casos = ventanas.get("casos") or []
        cids = [str(c.get("id")) for c in casos]
        if len(set(cids)) != len(cids):
            problemas.append(f"{sesion}: ids de caso repetidos")
        for c in casos:
            if not ids.es_id_de("caso", str(c.get("id"))):
                problemas.append(f"{sesion}: id de caso invalido {c.get('id')!r}")
            if str(c.get("dataset_id")) not in ids_datasets:
                problemas.append(
                    f"{sesion}: {c.get('id')} cita dataset inexistente {c.get('dataset_id')}"
                )
        problemas += _problemas_de_vistos(repo, sesion, ventanas)
        # El ancla del paquete, ANTES de cualquier `continue` que dependa de las etiquetas: es
        # justo mientras no existe ninguna cuando hace falta (ADR-0035, enmienda del 2026-09-21).
        problemas += problemas_de_ancla(repo, sesion, anclas)
        # (b) del reparto de trabajos de la vieja guardia: avisar de que el config global ha
        # derivado. AVISO y no ERROR, y por dos motivos: un paquete viejo se reproduce con el
        # suyo y no tiene por que saber nada del de hoy, y editar `config.yaml` para el paquete
        # SIGUIENTE -otros cupos, otro mes- es el camino normal, no una averia. Nombra las claves
        # que difieren, no vuelca el diff: quien quiera el detalle tiene `git diff`.
        doc_congelado = ventanas.get("config")
        if doc_global is not None and isinstance(doc_congelado, dict):
            distintas = sorted(
                k
                for k in set(doc_global) | set(doc_congelado)
                if doc_global.get(k) != doc_congelado.get(k)
            )
            if distintas:
                avisos.append(
                    f"{sesion}/ventanas.yaml: su config congelado difiere del {FICHERO_CONFIG} de "
                    f"hoy en {', '.join(distintas)}. Es lo esperado cuando el config global "
                    f"evoluciona: el paquete se reproduce con el suyo (ADR-0035, enmienda del "
                    f"2026-09-21). Si no esperabas esa clave, mira el ancla"
                )
        asignacion = particiones.get("asignacion") or {}
        if set(asignacion) != set(cids):
            problemas.append(
                f"{sesion}: particiones.yaml y ventanas.yaml no tienen los mismos casos"
            )
        if any(v not in PARTICIONES for v in asignacion.values()):
            problemas.append(f"{sesion}: particion desconocida en la asignacion")
        # Guardia: particiones antes del primer LABEL_CASE de la sesion.
        etiquetas = [r for r in registros if r.sesion == sesion and r.accion == "LABEL_CASE"]
        if not etiquetas:
            continue
        ruta_part = f"{DIRECTORIO_KIT}/{sesion}/particiones.yaml"
        alta = commit_que_anadio(repo, ruta_part)
        if alta is None:
            problemas.append(f"{sesion}: hay LABEL_CASE pero particiones.yaml no esta commiteado")
            continue
        for nombre in ("particiones.yaml", "ventanas.yaml"):
            ruta = f"{DIRECTORIO_KIT}/{sesion}/{nombre}"
            origen = commit_que_anadio(repo, ruta)
            if origen is not None and intacto_desde(repo, origen[0], ruta) is not True:
                problemas.append(
                    f"{sesion}: {nombre} cambio despues de su commit {origen[0][:7]} y ya hay "
                    "LABEL_CASE de esa sesion (la asignacion es inmutable tras el etiquetado)"
                )
        for r in etiquetas:
            ruta_fb = f"knowledge/feedback/{r.sesion}/{r.id}.yaml"
            alta_fb = commit_que_anadio(repo, ruta_fb)
            if alta_fb is None:
                continue  # el registro sin commitear lo vigila la guardia de feedback
            if alta_fb[0] == alta[0] or es_ancestro(repo, alta[0], alta_fb[0]) is not True:
                problemas.append(
                    f"{sesion}: particiones.yaml ({alta[0][:7]}, {alta[1]}) no es anterior al "
                    f"LABEL_CASE {r.id} ({alta_fb[0][:7]}, {alta_fb[1]})"
                )
    return problemas, avisos


def kappa_entre_sesiones(
    repo: Path,
    registros: list[FeedbackRecord],
    a: str,
    b: str,
    incluir_holdout: bool = False,
    pregunta: str = "",
) -> Any:
    """Kappa entre dos rondas, SIN leer las etiquetas de los dias reservados (ADR-0033).

    Leer la etiqueta de un caso asignado a `holdout-1/2/3` es abrir ese holdout (ADR-0021 §1), y el
    kappa las leia todas. Ahora se excluyen y se dice cuantas; con `incluir_holdout` se pide
    abrirlas, y la puerta se niega salvo autorizacion del usuario y PREREGISTRO relleno (§3).
    """
    from botsito.cases.holdout import abrir, casos_reservados, gastar_pregunta
    from botsito.cases.kappa import calcular, etiquetas_de_registros

    config = cargar_config(repo / DIRECTORIO_KIT / FICHERO_CONFIG)
    reservados = casos_reservados(repo)
    # Solo el OBJETIVO del registro (el id del caso), nunca su valor: saber que un caso reservado
    # tiene etiqueta no es leerla.
    from botsito.feedback.modelo import activos

    etiquetados = {
        r.objetivo.id
        for r in activos(list(registros))
        if r.accion == "LABEL_CASE" and r.sesion in (a, b) and r.objetivo.id in reservados
    }
    por_particion: dict[str, int] = {}
    for caso in etiquetados:
        por_particion[reservados[caso]] = por_particion.get(reservados[caso], 0) + 1
    if incluir_holdout:
        # El orden manda (ADR-0033, enmienda del 2026-09-21): comprobar la puerta -> GASTAR la
        # pregunta -> leer. Los dos modos de fallo no son simetricos: "gastada y no leida" cuesta
        # volver a pre-registrar; "leida y no gastada" es el defecto que la enmienda cierra.
        for particion in sorted(por_particion):
            abrir(repo, particion, pregunta)
        gastar_pregunta(repo, pregunta)
        excluir: frozenset[str] = frozenset()
    else:
        excluir = frozenset(etiquetados)
    try:
        ra = etiquetas_de_registros(
            registros, a, config.nombres_sesiones, config.etiquetas, excluir=excluir
        )
        rb = etiquetas_de_registros(
            registros, b, config.nombres_sesiones, config.etiquetas, excluir=excluir
        )
        resultado = calcular(ra, rb, config.etiquetas)
    except EtiquetaError as exc:
        pista = (
            " (las etiquetas de los dias reservados no se leen sin abrir su holdout, ADR-0033)"
            if excluir
            else ""
        )
        raise KitError(f"{exc}{pista}") from exc
    # Etiquetado que NO fue ciego (2026-09-17): una unidad de un dia cuyo mes -o el propio dia- el
    # trader ya habia visto el dia de la sesion que la etiqueto. No se excluye -el kappa mide
    # consistencia y sigue sirviendo-, pero F26 tiene que saberlo al leer cualquier kappa que la
    # incluya: lo dice aqui, y no en una nota que nadie mira.
    for sesion_r, ronda in ((a, ra), (b, rb)):
        casos_ronda = sorted({u.split("|", 1)[0] for u in ronda})
        vistos = vistos_en_el_paquete(repo, sesion_r, [c[-10:] for c in casos_ronda])
        if vistos:
            resultado.avisos.append(
                f"{sesion_r}: {len(vistos)} casos etiquetados sobre dias que el trader ya habia "
                f"visto el {fecha_de_sesion(sesion_r)} (vistos.yaml): no fue etiquetado ciego"
            )
    if excluir:
        detalle = ", ".join(f"{p}: {n}" for p, n in sorted(por_particion.items()))
        resultado.avisos.append(
            f"{len(excluir)} casos reservados excluidos sin leer su etiqueta ({detalle}); "
            f"abrirlos exige autorizacion y PREREGISTRO (ADR-0021 §3)"
        )
    return resultado
