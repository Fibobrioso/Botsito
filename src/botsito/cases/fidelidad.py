"""El camino de fidelidad (ADR-0036): repartir material ETIQUETADO de un mes que el trader ya vio.

El kit (`cases/paquete.py`) es el camino del etiquetado CIEGO: construye un cuestionario, una hoja
para el trader y un paquete de dias que el NO ha visto, y por eso filtra por `vistos.yaml` y aborta
si un dia visto se cuela. Septiembre es lo contrario: material que el trader YA backtesteo y
entrego etiquetado (ADR-0034). Forzarlo por el kit exigiria falsear la fecha de la sesion o
desactivar el filtro de vistos, y las dos corrompen un mecanismo para reaprovechar codigo.

Lo que este camino SI necesita, y es todo lo que hace: un universo, un reparto fijado ANTES de leer
ninguna etiqueta, y un ancla. No necesita cuestionario, ni hoja, ni sesion, ni ceguera del trader
que proteger.

**Lo que aqui se salta A PROPOSITO, dicho para que no parezca un olvido:** el filtro de meses y
dias vistos. `universo()` recibe `meses_vistos=set()` y `dias_vistos=set()`. El kit no se toca: su
guardia sigue entera. Y en cuanto ese filtro se salta, `cobertura_material` -hasta donde llega el
material etiquetado- pasa de adorno a ser el UNICO filtro entre el universo y un dia sin etiquetar.

**Lo que este camino NO puede prometer, y va escrito aqui porque es donde se lee:** una cifra con
potencia estadistica. El minimo para F26 son 36 unidades efectivas independientes
(`docs/validation/AUDITORIA-2026-09-13-ultracode.md` §6.1) y NADA construible hoy lo alcanza: los
14 dias laborables de septiembre dan 28 unidades brutas y ~23 efectivas, y ninguna combinacion de
mayo llega tampoco. Lo que este camino aporta es ANTERIORIDAD DEMOSTRABLE -que el reparto se fijo
antes de leer ninguna etiqueta, comprobado por maquina- mas una cifra DESCRIPTIVA con su intervalo.
Quien cite esa cifra como si midiera fidelidad con potencia estara afirmando lo que no se probo.

Y los NOMBRES DE PARTICION son propios (`PARTICIONES_FIDELIDAD`), no los del kit: los del kit son
globales, un `AUTORIZACION-<nombre>.md` por nombre y un mapa plano que tira el paquete, asi que
mezclar dias no ciegos con los ciegos de mayo daria un cubo cuya cifra no se puede interpretar.
Pasan por la MISMA puerta (`holdout.py`): ADR-0034 separo la ceguera DEL TRADER -que
septiembre ya no tiene- de LA NUESTRA -que sigue intacta-, y es la nuestra la que la puerta
protege.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.cases.paquete import (
    FICHERO_ANCLAS,
    Config,
    KitError,
    _dump,
    _leer,
    _yaml,
    cargar_anclas,
    config_desde_doc,
    datasets_que_faltan_en_disco,
    lectura_de_velas,
    manifiestos_del_prefijo,
    problemas_de_ancla,
)
from botsito.cases.particiones import PARTICIONES_FIDELIDAD, ParticionError, asignar
from botsito.cases.ventanas import Caso, Excluido, VentanaError, universo
from botsito.comun import ids
from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.config.registro import RegistroError, cargar_registro
from botsito.data.dataset import DatasetError
from botsito.domain.velas import VelaInvalidaError

DIRECTORIO_FIDELIDAD = "knowledge/cases/fidelidad"
FICHERO_CONFIG = "config.yaml"
FICHEROS_ARTEFACTO = ("ventanas.yaml", "particiones.yaml")
# Un artefacto NO lleva fecha ni "sesion" en el nombre, y no es un detalle de estilo: no hay
# reunion que fechar. `eurusd-2026-09`, no `2026-09-22-sesion-02`.
ARTEFACTO = re.compile(r"^[a-z0-9][a-z0-9-]*$", re.ASCII)
# El comando que nombra el ancla en los mensajes de la guardia.
COMANDO_ANCLA = "fidelidad anclar --artefacto"


class FidelidadError(ValueError):
    """Config o artefacto de fidelidad invalidos."""


@dataclass(frozen=True)
class Artefacto:
    id: str
    seed: int
    ficheros: dict[str, str]
    casos: list[Caso]
    excluidos: list[Excluido]
    asignacion: dict[str, str]
    universo: int


def cargar_config(repo: Path) -> Config:
    """El config del camino, con sus nombres de particion y su `cobertura_material`."""
    ruta = repo / DIRECTORIO_FIDELIDAD / FICHERO_CONFIG
    try:
        return config_desde_doc(_yaml(ruta), ruta.name, PARTICIONES_FIDELIDAD)
    except KitError as exc:
        raise FidelidadError(str(exc)) from exc


def artefactos(repo: Path) -> list[str]:
    base = repo / DIRECTORIO_FIDELIDAD
    if not base.is_dir():
        return []
    return sorted(d.name for d in base.iterdir() if d.is_dir() and ARTEFACTO.match(d.name))


def construir(
    repo: Path,
    carpeta_datos: Path,
    artefacto: str,
    seed: int,
    datasets: Sequence[str] | None = None,
    config: Config | None = None,
) -> Artefacto:
    """Construye el artefacto en memoria. Exige los datos de sus datasets en `data/`.

    `datasets` y `config` son lo CONGELADO de un artefacto existente, con el mismo contrato que en
    el kit (ADR-0035 y su enmienda): `None` lee el disco -lo que un artefacto NUEVO tiene que
    hacer- y no-`None` usa lo congelado.
    """
    if not ARTEFACTO.match(artefacto):
        raise FidelidadError(f"id de artefacto invalido {artefacto!r} (a-z, 0-9 y guion)")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise FidelidadError("el seed debe ser un entero >= 0")
    config = config or cargar_config(repo)
    try:
        registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    except RegistroError as exc:
        raise FidelidadError(str(exc)) from exc
    huso = registro.texto("huso_operativa")
    try:
        huso_canonico(huso)
    except HusoDesconocidoError as exc:
        raise FidelidadError(f"huso_operativa: {exc}") from exc
    try:
        manif = manifiestos_del_prefijo(repo, config, datasets)
        if not manif:
            raise FidelidadError(
                f"ningun dataset con prefijo {config.dataset_prefijo!r} en data/manifests"
            )
        # AQUI se salta el filtro de vistos, a proposito (ver la cabecera del modulo): estos dias
        # los ha visto el trader, y precisamente por eso estan etiquetados y sirven.
        casos, excluidos = universo(
            manif,
            carpeta_datos,
            config.simbolo,
            huso,
            config.ventana_local,
            list(config.anclajes),
            config.min_velas_ventana,
            set(),
            set(),
            config.cobertura,
            solo_con_cobertura=True,
        )
        asignacion = asignar([c.id for c in casos], seed, config.particiones, PARTICIONES_FIDELIDAD)
    except (DatasetError, VentanaError, ParticionError, VelaInvalidaError, KitError) as exc:
        raise FidelidadError(str(exc)) from exc
    elegidos = [c for c in casos if c.id in asignacion]
    ficheros = {
        "ventanas.yaml": _dump(
            {
                "artefacto": artefacto,
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
                "artefacto": artefacto,
                "seed": seed,
                "cupos": config.particiones,
                "asignacion": {c.id: asignacion[c.id] for c in elegidos},
            }
        ),
    }
    return Artefacto(artefacto, seed, ficheros, elegidos, excluidos, asignacion, len(casos))


def escribir(repo: Path, artefacto: Artefacto) -> Path:
    carpeta = repo / DIRECTORIO_FIDELIDAD / artefacto.id
    if carpeta.exists():
        raise FidelidadError(f"{carpeta.as_posix()} ya existe: no se sobreescribe")
    carpeta.mkdir(parents=True)
    for nombre, texto in artefacto.ficheros.items():
        (carpeta / nombre).write_text(texto, encoding="utf-8", newline="\n")
    return carpeta


def esquema_artefacto(repo: Path, artefacto: str) -> tuple[dict[str, Any], dict[str, Any]]:
    carpeta = repo / DIRECTORIO_FIDELIDAD / artefacto
    docs: list[dict[str, Any]] = []
    for nombre in FICHEROS_ARTEFACTO:
        ruta = carpeta / nombre
        if not ruta.is_file():
            raise FidelidadError(f"falta {artefacto}/{nombre}")
        doc = _yaml(ruta)
        if not isinstance(doc, dict) or doc.get("artefacto") != artefacto:
            raise FidelidadError(f"{artefacto}/{nombre}: clave `artefacto` ausente o distinta")
        docs.append(doc)
    ventanas, particiones = docs
    asignacion = particiones.get("asignacion")
    if not isinstance(asignacion, dict):
        raise FidelidadError(f"{artefacto}/particiones.yaml: asignacion debe ser un mapa")
    seed = particiones.get("seed")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise FidelidadError(f"{artefacto}/particiones.yaml: seed invalido")
    return ventanas, particiones


def comprobar(repo: Path, carpeta_datos: Path, artefacto: str) -> tuple[list[str], list[str]]:
    """PURO: recompone el artefacto con lo CONGELADO y compara byte a byte.

    A diferencia del kit, aqui NINGUN fichero se exime nunca: no hay sesion celebrada cuyas
    respuestas expliquen una diferencia, porque no hubo reunion. Todo tiene que reproducirse.
    """
    problemas: list[str] = []
    avisos: list[str] = []
    ventanas, particiones = esquema_artefacto(repo, artefacto)
    seed = int(particiones["seed"])
    doc_congelado = ventanas.get("config")
    if doc_congelado is None:
        problemas.append(
            f"{artefacto}/ventanas.yaml: sin bloque `config`: el artefacto no esta congelado y no "
            f"hay con que reproducirlo (ADR-0035, enmienda; ADR-0036)"
        )
        return problemas, avisos
    try:
        config = config_desde_doc(
            doc_congelado, f"{artefacto}/ventanas.yaml:config", PARTICIONES_FIDELIDAD
        )
    except KitError as exc:
        problemas.append(str(exc))
        return problemas, avisos
    congelados = ventanas.get("datasets")
    if not isinstance(congelados, list) or not all(isinstance(d, str) and d for d in congelados):
        problemas.append(f"{artefacto}/ventanas.yaml: `datasets` debe ser una lista de ids")
        return problemas, avisos
    faltan = datasets_que_faltan_en_disco(repo, carpeta_datos, config, congelados)
    if faltan:
        avisos.append(
            f"{artefacto}: datos ausentes en {carpeta_datos.name}/ de {', '.join(faltan)}: solo "
            f"esquema"
        )
        return problemas, avisos
    try:
        nuevo = construir(repo, carpeta_datos, artefacto, seed, datasets=congelados, config=config)
    except FidelidadError as exc:
        problemas.append(str(exc))
        return problemas, avisos
    carpeta = repo / DIRECTORIO_FIDELIDAD / artefacto
    for nombre, texto in nuevo.ficheros.items():
        if _leer(carpeta, nombre) != texto:
            problemas.append(f"{artefacto}/{nombre}: difiere de lo que se genera hoy")
    return problemas, avisos


def lectura(
    repo: Path,
    carpeta_datos: Path,
    asignacion: dict[str, str],
    datasets: Sequence[str] | None = None,
) -> list[str]:
    """La declaracion de ADR-0033 para este camino, con SUS particiones reservadas."""
    from botsito.cases.holdout import PARTICIONES_RESERVADAS_FIDELIDAD

    try:
        config = cargar_config(repo)
    except FidelidadError:
        return []
    return lectura_de_velas(
        repo,
        carpeta_datos,
        asignacion,
        datasets,
        config=config,
        reservadas=PARTICIONES_RESERVADAS_FIDELIDAD,
    )


def validar_artefactos(repo: Path, ids_datasets: set[str]) -> tuple[list[str], list[str]]:
    """Para `knowledge validate`: esquema, ancla y deriva del config. SIN `data/`."""
    problemas: list[str] = []
    avisos: list[str] = []
    lista = artefactos(repo)
    if not lista:
        return problemas, avisos
    try:
        anclas = cargar_anclas(repo, DIRECTORIO_FIDELIDAD, ARTEFACTO)
    except KitError as exc:
        problemas.append(str(exc))
        anclas = {}
    try:
        doc_global: dict[str, Any] | None = cargar_config(repo).doc
    except FidelidadError as exc:
        problemas.append(str(exc))
        doc_global = None
    for artefacto in lista:
        try:
            ventanas, particiones = esquema_artefacto(repo, artefacto)
        except (FidelidadError, KitError) as exc:
            problemas.append(str(exc))
            continue
        casos = ventanas.get("casos") or []
        cids = [str(c.get("id")) for c in casos]
        if len(set(cids)) != len(cids):
            problemas.append(f"{artefacto}: ids de caso repetidos")
        for c in casos:
            if not ids.es_id_de("caso", str(c.get("id"))):
                problemas.append(f"{artefacto}: id de caso invalido {c.get('id')!r}")
            if str(c.get("dataset_id")) not in ids_datasets:
                problemas.append(
                    f"{artefacto}: {c.get('id')} cita dataset inexistente {c.get('dataset_id')}"
                )
        congelados = ventanas.get("datasets")
        if not isinstance(congelados, list) or not congelados:
            problemas.append(f"{artefacto}/ventanas.yaml: sin `datasets` congelados (ADR-0035)")
        else:
            for d in congelados:
                if str(d) not in ids_datasets:
                    problemas.append(
                        f"{artefacto}/ventanas.yaml: `datasets` cita {d}, que ya no esta en "
                        f"data/manifests: el artefacto no se puede reproducir"
                    )
        asignacion = particiones.get("asignacion") or {}
        if set(asignacion) != set(cids):
            problemas.append(
                f"{artefacto}: particiones.yaml y ventanas.yaml no tienen los mismos casos"
            )
        if any(v not in PARTICIONES_FIDELIDAD for v in asignacion.values()):
            problemas.append(
                f"{artefacto}: particion fuera de {PARTICIONES_FIDELIDAD} en la asignacion"
            )
        problemas += problemas_de_ancla(
            repo, artefacto, anclas, DIRECTORIO_FIDELIDAD, COMANDO_ANCLA
        )
        doc_congelado = ventanas.get("config")
        if doc_global is not None and isinstance(doc_congelado, dict):
            distintas = sorted(
                k
                for k in set(doc_global) | set(doc_congelado)
                if doc_global.get(k) != doc_congelado.get(k)
            )
            if distintas:
                avisos.append(
                    f"{artefacto}/ventanas.yaml: su config congelado difiere del "
                    f"{FICHERO_CONFIG} de hoy en {', '.join(distintas)}. El artefacto se "
                    f"reproduce con el suyo (ADR-0036)"
                )
    return problemas, avisos


__all__ = [
    "ARTEFACTO",
    "COMANDO_ANCLA",
    "DIRECTORIO_FIDELIDAD",
    "FICHERO_ANCLAS",
    "FICHEROS_ARTEFACTO",
    "Artefacto",
    "FidelidadError",
    "artefactos",
    "cargar_config",
    "comprobar",
    "construir",
    "escribir",
    "esquema_artefacto",
    "lectura",
    "validar_artefactos",
]
