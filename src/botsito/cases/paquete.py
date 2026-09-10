"""El paquete de una sesion (F10, ADR-0011): config del kit, construccion determinista,
escritura sin sobreescribir, `check` puro y validacion para `knowledge validate`."""

from __future__ import annotations

import re
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
from botsito.comun.historial import commit_que_anadio, es_ancestro, intacto_desde
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
FICHEROS_PAQUETE = ("cuestionario.yaml", "ventanas.yaml", "particiones.yaml", "hoja_trader.md")
SESION = re.compile(r"^\d{4}-\d{2}-\d{2}-sesion-\d{2}$", re.ASCII)
_MES = re.compile(r"^\d{4}-\d{2}$", re.ASCII)
_HORA = re.compile(r"^\d{2}:\d{2}$", re.ASCII)


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


def cargar_config(ruta: Path) -> Config:
    doc = _yaml(ruta)
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
    if not isinstance(doc, dict) or set(doc) != esperadas:
        raise KitError(f"{ruta.name}: claves {sorted(esperadas)} exactamente")
    if not isinstance(doc["simbolo"], str) or not doc["simbolo"].isalnum():
        raise KitError(f"{ruta.name}: simbolo invalido")
    if not isinstance(doc["dataset_prefijo"], str) or not doc["dataset_prefijo"].strip():
        raise KitError(f"{ruta.name}: dataset_prefijo vacio")
    ventana = doc["ventana_local"]
    if not isinstance(ventana, dict) or set(ventana) != {"desde", "hasta"}:
        raise KitError(f"{ruta.name}: ventana_local necesita desde y hasta")
    v_desde, v_hasta = (
        _hora(ventana["desde"], "ventana_local"),
        _hora(ventana["hasta"], "ventana_local"),
    )
    if v_hasta <= v_desde:
        raise KitError(f"{ruta.name}: ventana_local acaba antes de empezar")
    sesiones: list[Sesion] = []
    for s in doc["sesiones"] if isinstance(doc["sesiones"], list) else []:
        if not isinstance(s, dict) or set(s) != {"nombre", "desde", "hasta"}:
            raise KitError(f"{ruta.name}: cada sesion tiene nombre, desde y hasta")
        nombre = str(s["nombre"])
        if not re.match(r"^[a-z0-9-]+$", nombre):
            raise KitError(f"{ruta.name}: nombre de sesion {nombre!r} (solo a-z, 0-9 y guion)")
        d, h = _hora(s["desde"], nombre), _hora(s["hasta"], nombre)
        if not (v_desde <= d < h <= v_hasta):
            raise KitError(f"{ruta.name}: la sesion {nombre} no cabe en ventana_local")
        sesiones.append(Sesion(nombre, d, h))
    if not sesiones or len({s.nombre for s in sesiones}) != len(sesiones):
        raise KitError(f"{ruta.name}: sesiones vacias o con nombres repetidos")
    anclajes: list[Anclaje] = []
    for a in doc["anclajes_candidatos"] if isinstance(doc["anclajes_candidatos"], list) else []:
        if not isinstance(a, dict) or set(a) != {
            "etiqueta",
            "hora",
            "huso",
            "coincide_con_sesiones",
        }:
            raise KitError(
                f"{ruta.name}: cada anclaje tiene etiqueta, hora, huso y coincide_con_sesiones"
            )
        try:
            HoraLocal(str(a["hora"]), str(a["huso"]))
            ZoneInfo(str(a["huso"]))
        except (ValueError, KeyError, OSError) as exc:
            raise KitError(f"{ruta.name}: anclaje {a.get('etiqueta')!r}: {exc}") from exc
        if not isinstance(a["coincide_con_sesiones"], bool):
            raise KitError(f"{ruta.name}: coincide_con_sesiones debe ser true/false")
        anclajes.append(
            Anclaje(str(a["etiqueta"]), str(a["hora"]), str(a["huso"]), a["coincide_con_sesiones"])
        )
    if not anclajes or len({a.etiqueta for a in anclajes}) != len(anclajes):
        raise KitError(f"{ruta.name}: anclajes vacios o con etiquetas repetidas")
    if sum(1 for a in anclajes if a.coincide_con_sesiones) != 1:
        raise KitError(f"{ruta.name}: exactamente un anclaje coincide con las sesiones")
    minimo = doc["min_velas_ventana"]
    if isinstance(minimo, bool) or not isinstance(minimo, int) or minimo < 1:
        raise KitError(f"{ruta.name}: min_velas_ventana debe ser un entero >= 1")
    etiquetas = doc["etiquetas"]
    if (
        not isinstance(etiquetas, list)
        or not etiquetas
        or len(set(etiquetas)) != len(etiquetas)
        or not all(isinstance(e, str) and re.match(r"^[a-z_]+$", e) for e in etiquetas)
    ):
        raise KitError(
            f"{ruta.name}: etiquetas debe ser una lista de nombres en minusculas sin repetir"
        )
    particiones = doc["particiones"]
    if not isinstance(particiones, dict) or set(particiones) != set(PARTICIONES):
        raise KitError(f"{ruta.name}: particiones debe declarar {PARTICIONES}")
    for k, v in particiones.items():
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise KitError(f"{ruta.name}: particion {k}: entero >= 0")
    return Config(
        str(doc["simbolo"]),
        str(doc["dataset_prefijo"]),
        (v_desde, v_hasta),
        tuple(sesiones),
        tuple(anclajes),
        minimo,
        tuple(etiquetas),
        {str(k): int(v) for k, v in particiones.items()},
        doc,
    )


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
        if (
            not isinstance(e, dict)
            or not {"temas", "ambiguedad"} <= set(e)
            or set(e) - {"temas", "ambiguedad", "opciones"}
        ):
            raise KitError(f"{ruta.name}: {nombre}: claves temas, ambiguedad [, opciones]")
        temas = e["temas"]
        if not isinstance(temas, list) or not temas or not all(isinstance(t, str) for t in temas):
            raise KitError(f"{ruta.name}: {nombre}: temas debe ser una lista no vacia")
        for t in temas:
            if temas_raiz and t.split(".")[0] not in temas_raiz:
                raise KitError(f"{ruta.name}: {nombre}: tema {t!r} fuera de _temas.yaml")
        amb = e["ambiguedad"]
        if amb is not None and not ids.es_id_de("ambiguedad", str(amb)):
            raise KitError(f"{ruta.name}: {nombre}: ambiguedad {amb!r} invalida (A-N o null)")
        opciones = e.get("opciones") or []
        if not isinstance(opciones, list) or not all(isinstance(o, str) and o for o in opciones):
            raise KitError(f"{ruta.name}: {nombre}: opciones debe ser una lista de textos")
        salida[str(nombre)] = EntradaMapa(
            tuple(temas), None if amb is None else str(amb), tuple(opciones)
        )
    return salida


def cargar_vistos(ruta: Path) -> tuple[set[str], set[str], dict[str, Any]]:
    doc = _yaml(ruta)
    if not isinstance(doc, dict) or set(doc) != {"meses", "dias"}:
        raise KitError(f"{ruta.name}: claves meses y dias")
    meses: set[str] = set()
    for m in doc["meses"] if isinstance(doc["meses"], list) else []:
        if (
            not isinstance(m, dict)
            or not {"mes", "motivo", "fuente"} <= set(m)
            or not _MES.match(str(m["mes"]))
        ):
            raise KitError(f"{ruta.name}: cada mes tiene mes (AAAA-MM), motivo y fuente")
        meses.add(str(m["mes"]))
    dias: set[str] = set()
    for d in doc["dias"] if isinstance(doc["dias"], list) else []:
        if not isinstance(d, dict) or not {"dia", "motivo"} <= set(d):
            raise KitError(f"{ruta.name}: cada dia tiene dia y motivo")
        try:
            dias.add(date.fromisoformat(str(d["dia"])).isoformat())
        except ValueError as exc:
            raise KitError(f"{ruta.name}: dia {d['dia']!r} no es AAAA-MM-DD") from exc
    return meses, dias, doc


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
    meses, dias, _ = cargar_vistos(kit / FICHERO_VISTOS)
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    return config, registro, ambiguedades, mapa, meses, dias, items


def _manifiestos_del_kit(repo: Path, config: Config) -> list[dict[str, Any]]:
    salida = []
    for ruta in manifiestos(repo):
        m = cargar_manifiesto(ruta)
        if str(m["dataset_id"]).startswith(config.dataset_prefijo):
            salida.append(m)
    return salida


def construir(
    repo: Path, carpeta_datos: Path, sesion: str, seed: int, indice: Indice | None = None
) -> Paquete:
    """Construye el paquete completo en memoria. Exige los datos de los datasets en `data/`."""
    if not SESION.match(sesion):
        raise KitError(f"sesion invalida {sesion!r} (AAAA-MM-DD-sesion-NN)")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise KitError("el seed debe ser un entero >= 0")
    config, registro, ambiguedades, mapa, meses, dias, items = _cargar_todo(repo)
    huso = registro.texto("huso_operativa")
    try:
        huso_canonico(huso)
    except HusoDesconocidoError as exc:
        raise KitError(f"huso_operativa: {exc}") from exc
    vivos = activos(list(items))
    abiertas = contradicciones.detectar(vivos)
    problemas_amb = validar_ambiguedades(
        ambiguedades, {i.id for i in vivos}, set(registro.nombres()), {c["tema"] for c in abiertas}
    )
    if problemas_amb:
        raise KitError("ambiguedades: " + "; ".join(problemas_amb))
    ids_amb = {a.id for a in ambiguedades}
    for nombre, e in mapa.items():
        if e.ambiguedad is not None and e.ambiguedad not in ids_amb:
            raise KitError(
                f"mapa_parametros: {nombre} cita la ambiguedad {e.ambiguedad}, que no existe"
            )
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
        manif = _manifiestos_del_kit(repo, config)
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


def comprobar(
    repo: Path, carpeta_datos: Path, sesion: str, celebrada: bool = False
) -> tuple[list[str], list[str]]:
    """PURO: recompone el paquete y compara byte a byte (tras normalizar CRLF). Sin datos en
    `data/`, comprueba solo el esquema y avisa."""
    problemas: list[str] = []
    avisos: list[str] = []
    cuestionario, ventanas, particiones = esquema_paquete(repo, sesion)
    seed = int(particiones["seed"])
    config = cargar_config(repo / DIRECTORIO_KIT / FICHERO_CONFIG)
    if ventanas.get("config") != config.doc:
        problemas.append(f"{sesion}: config.yaml cambio despues de generar el paquete")
    datasets = {str(m["dataset_id"]) for m in _manifiestos_del_kit(repo, config)}
    hay_datos = all(
        (carpeta_datos / str(f["ruta"])).is_file()
        for m in _manifiestos_del_kit(repo, config)
        for f in m["ficheros"]
    ) and bool(datasets)
    if not hay_datos:
        avisos.append(
            f"{sesion}: datos de los datasets ausentes en {carpeta_datos.name}/: solo esquema"
        )
        return problemas, avisos
    nuevo = construir(repo, carpeta_datos, sesion, seed)
    carpeta = repo / DIRECTORIO_KIT / sesion
    for nombre, texto in nuevo.ficheros.items():
        if _leer(carpeta, nombre) == texto:
            continue
        if celebrada:
            # El paquete de una sesion ya celebrada es historico: dice lo que se le pregunto al
            # trader ese dia. Regenerarlo hoy da otra cosa a proposito, porque el registro ya
            # tiene las respuestas y el cuestionario ya no preguntaria lo mismo. Exigir que se
            # reproduzca seria exigir que el proyecto no aprenda nada.
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


def kappa_entre_sesiones(repo: Path, registros: list[FeedbackRecord], a: str, b: str) -> Any:
    from botsito.cases.kappa import calcular, etiquetas_de_registros

    config = cargar_config(repo / DIRECTORIO_KIT / FICHERO_CONFIG)
    try:
        ra = etiquetas_de_registros(registros, a, config.nombres_sesiones, config.etiquetas)
        rb = etiquetas_de_registros(registros, b, config.nombres_sesiones, config.etiquetas)
        return calcular(ra, rb, config.etiquetas)
    except EtiquetaError as exc:
        raise KitError(str(exc)) from exc
