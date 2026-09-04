"""FeedbackRecord (F09): cada aportacion del trader como registro trazable y solo-anadir.

Un registro dice que dijo el trader (literal), sobre que objeto (evidencia, regla, parametro,
ambiguedad, caso o contradiccion), con que accion, en que sesion y por que medio, y quien lo
registro. Nunca modifica la evidencia ni otro registro: los supersede. El id incluye un hash del
contenido y el historial de git se vigila igual que el de la evidencia.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.evidence.modelo import _normalizar_texto, parse_tiempo

ACCIONES = (
    "CONFIRM",
    "CORRECT",
    "REJECT",
    "RESOLVE_UNKNOWN",
    "RESOLVE_CONTRADICTION",
    "LABEL_CASE",
    "MARK_FALSE_POSITIVE",
    "MARK_FALSE_NEGATIVE",
    "BORDERLINE",
)
TIPOS_OBJETIVO = ("evidence", "regla", "parametro", "ambiguedad", "caso", "contradiccion")
MEDIOS = ("replay", "audio", "video", "escrito")
OBJETIVOS_POR_ACCION: dict[str, tuple[str, ...]] = {
    "CONFIRM": ("evidence", "regla", "parametro"),
    "CORRECT": ("evidence", "regla", "parametro"),
    "REJECT": ("evidence", "regla", "parametro"),
    "RESOLVE_UNKNOWN": ("parametro", "ambiguedad", "evidence"),
    "RESOLVE_CONTRADICTION": ("contradiccion",),
    "LABEL_CASE": ("caso",),
    "MARK_FALSE_POSITIVE": ("caso",),
    "MARK_FALSE_NEGATIVE": ("caso",),
    "BORDERLINE": ("caso",),
}
EXIGEN_VALOR = ("CORRECT", "RESOLVE_UNKNOWN", "RESOLVE_CONTRADICTION", "LABEL_CASE")
FORMATO_ID_OBJETIVO: dict[str, re.Pattern[str]] = {
    "evidence": re.compile(r"^ev-[a-z0-9]+-\d{6}-[0-9a-f]{8}$"),
    "regla": re.compile(r"^RN-\d{3}$"),
    "parametro": re.compile(r"^[a-z][a-z0-9_]*$"),
    "ambiguedad": re.compile(r"^A-\d+$"),
    "caso": re.compile(r"^caso-[a-z0-9][a-z0-9-]*$"),
    "contradiccion": re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$"),
}
_SESION = re.compile(r"^\d{4}-\d{2}-\d{2}-sesion-\d{2}$")
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_ID = re.compile(r"^fb-[0-9a-z-]+-[0-9a-f]{8}$")
CAMPOS_OBLIGATORIOS = (
    "sesion",
    "fecha",
    "medio",
    "objetivo",
    "accion",
    "respuesta_literal",
    "registrado_por",
)
CAMPOS_OPCIONALES = ("grabacion", "t0", "t1", "valor_resultante", "supersede", "notas")


class FeedbackError(ValueError):
    """Un registro no cumple el esquema o no es coherente."""


@dataclass(frozen=True, slots=True)
class Objetivo:
    tipo: str
    id: str


@dataclass(frozen=True, slots=True)
class FeedbackRecord:
    id: str
    sesion: str
    fecha: str
    medio: str
    objetivo: Objetivo
    accion: str
    respuesta_literal: str
    registrado_por: str
    grabacion: str | None = None
    t0: str | None = None
    t1: str | None = None
    valor_resultante: str | None = None
    supersede: str | None = None
    notas: str | None = None


def contenido_canonico(campos: dict[str, Any]) -> str:
    limpio: dict[str, Any] = {}
    for clave in (*CAMPOS_OBLIGATORIOS, *CAMPOS_OPCIONALES):
        if clave not in campos or campos[clave] is None:
            continue
        v = campos[clave]
        if clave == "objetivo" and isinstance(v, dict):
            limpio[clave] = {str(k): _normalizar_texto(x) for k, x in sorted(v.items())}
        elif isinstance(v, str):
            limpio[clave] = _normalizar_texto(v)
        else:
            limpio[clave] = v
    return json.dumps(limpio, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def calcular_id(campos: dict[str, Any]) -> str:
    h = hashlib.sha256(contenido_canonico(campos).encode("utf-8")).hexdigest()[:8]
    return f"fb-{campos['sesion']}-{h}"


def _validar(campos: dict[str, Any], origen: str) -> None:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if c not in campos or campos[c] in (None, "")]
    if faltan:
        raise FeedbackError(f"{origen}: faltan campos obligatorios {faltan}")
    desconocidos = set(campos) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES) - {"id"}
    if desconocidos:
        raise FeedbackError(f"{origen}: campos desconocidos {sorted(desconocidos)}")
    if not _SESION.match(str(campos["sesion"])):
        raise FeedbackError(f"{origen}: sesion invalida (formato AAAA-MM-DD-sesion-NN)")
    if not _FECHA.match(str(campos["fecha"])):
        raise FeedbackError(f"{origen}: fecha invalida (AAAA-MM-DD)")
    if campos["medio"] not in MEDIOS:
        raise FeedbackError(f"{origen}: medio {campos['medio']!r} no esta en {MEDIOS}")
    if campos["accion"] not in ACCIONES:
        raise FeedbackError(f"{origen}: accion {campos['accion']!r} no esta en {ACCIONES}")
    objetivo = campos["objetivo"]
    if not isinstance(objetivo, dict) or set(objetivo) != {"tipo", "id"}:
        raise FeedbackError(f"{origen}: objetivo debe ser {{tipo, id}}")
    if objetivo["tipo"] not in TIPOS_OBJETIVO:
        raise FeedbackError(f"{origen}: tipo de objetivo {objetivo['tipo']!r} desconocido")
    if not FORMATO_ID_OBJETIVO[objetivo["tipo"]].match(str(objetivo["id"])):
        raise FeedbackError(
            f"{origen}: id de objetivo {objetivo['id']!r} no tiene formato de {objetivo['tipo']}"
        )
    permitidos = OBJETIVOS_POR_ACCION[campos["accion"]]
    if objetivo["tipo"] not in permitidos:
        raise FeedbackError(
            f"{origen}: la accion {campos['accion']} exige objetivo de tipo {permitidos}, "
            f"no {objetivo['tipo']!r}"
        )
    if campos["accion"] in EXIGEN_VALOR and not _normalizar_texto(
        campos.get("valor_resultante") or ""
    ):
        raise FeedbackError(f"{origen}: la accion {campos['accion']} exige valor_resultante")
    if len(_normalizar_texto(campos["respuesta_literal"])) < 5:
        raise FeedbackError(f"{origen}: respuesta_literal es obligatoria y literal")
    if not _normalizar_texto(campos["registrado_por"]):
        raise FeedbackError(f"{origen}: registrado_por es obligatorio")
    if campos["medio"] != "escrito":
        for c in ("grabacion", "t0", "t1"):
            if not campos.get(c):
                raise FeedbackError(
                    f"{origen}: medio {campos['medio']} exige grabacion, t0 y t1 "
                    "(la sesion se graba)"
                )
        if not parse_tiempo(str(campos["t0"])) < parse_tiempo(str(campos["t1"])):
            raise FeedbackError(f"{origen}: t0 debe ser menor que t1")
    if campos.get("supersede") is not None and not _ID.match(str(campos["supersede"])):
        raise FeedbackError(f"{origen}: supersede debe ser un id de feedback")


def registro_desde_dict(campos: dict[str, Any], origen: str = "registro") -> FeedbackRecord:
    _validar(campos, origen)
    esperado = calcular_id(campos)
    if campos.get("id") != esperado:
        raise FeedbackError(
            f"{origen}: id {campos.get('id')!r} no coincide con el contenido "
            f"(esperado {esperado}); un registro no se edita: se anade otro que lo supersede"
        )
    o = campos["objetivo"]

    def txt(clave: str) -> str | None:
        v = campos.get(clave)
        return _normalizar_texto(v) if v not in (None, "") else None

    return FeedbackRecord(
        id=esperado,
        sesion=str(campos["sesion"]),
        fecha=str(campos["fecha"]),
        medio=str(campos["medio"]),
        objetivo=Objetivo(str(o["tipo"]), _normalizar_texto(o["id"])),
        accion=str(campos["accion"]),
        respuesta_literal=_normalizar_texto(campos["respuesta_literal"]),
        registrado_por=_normalizar_texto(campos["registrado_por"]),
        grabacion=txt("grabacion"),
        t0=txt("t0"),
        t1=txt("t1"),
        valor_resultante=txt("valor_resultante"),
        supersede=txt("supersede"),
        notas=txt("notas"),
    )


def cargar_registro(ruta: Path) -> FeedbackRecord:
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    if not isinstance(doc, dict):
        raise FeedbackError(f"{ruta.name}: no es un mapa YAML")
    r = registro_desde_dict(doc, ruta.name)
    if ruta.stem != r.id:
        raise FeedbackError(f"{ruta.name}: el nombre del fichero debe ser {r.id}.yaml")
    if ruta.parent.name != r.sesion:
        raise FeedbackError(f"{ruta.name}: debe estar en la carpeta de su sesion {r.sesion}/")
    return r


def cargar_feedback(directorio: Path) -> list[FeedbackRecord]:
    registros: list[FeedbackRecord] = []
    for ruta in sorted(directorio.rglob("*.yaml")):
        if ruta.name.startswith("_"):
            continue
        registros.append(cargar_registro(ruta))
    ids = [r.id for r in registros]
    repetidos = sorted({i for i in ids if ids.count(i) > 1})
    if repetidos:
        raise FeedbackError(f"ids repetidos: {repetidos}")
    return registros


def validar_contra_contexto(
    registros: list[FeedbackRecord],
    ids_evidencia: set[str],
    nombres_parametros: set[str],
    temas_contradiccion: set[str],
    rutas_corpus: set[str] | None = None,
) -> list[str]:
    """Los objetivos existen donde ya hay contra que comprobar.

    Regla, ambiguedad y caso se comprueban solo por formato hasta F11/F14.
    """
    problemas: list[str] = []
    ids = {r.id for r in registros}
    for r in registros:
        t, i = r.objetivo.tipo, r.objetivo.id
        if t == "evidence" and i not in ids_evidencia:
            problemas.append(f"{r.id}: evidencia objetivo {i} no existe")
        elif t == "parametro" and i not in nombres_parametros:
            problemas.append(f"{r.id}: parametro objetivo {i} no esta en el registro")
        elif t == "contradiccion" and i not in temas_contradiccion:
            problemas.append(f"{r.id}: no hay contradiccion abierta sobre {i}")
        if r.supersede and r.supersede not in ids:
            problemas.append(f"{r.id}: supersede a {r.supersede}, que no existe")
        if r.supersede == r.id:
            problemas.append(f"{r.id}: no puede supersederse a si mismo")
        if rutas_corpus is not None and r.grabacion and r.grabacion not in rutas_corpus:
            problemas.append(f"{r.id}: grabacion {r.grabacion!r} no esta inventariada en el corpus")
    return problemas


def activos(registros: list[FeedbackRecord]) -> list[FeedbackRecord]:
    superseded = {r.supersede for r in registros if r.supersede}
    return [r for r in registros if r.id not in superseded]


def escribir_registro(directorio: Path, campos: dict[str, Any]) -> Path:
    campos = {k: v for k, v in campos.items() if v not in (None, "", [], ())}
    campos["id"] = calcular_id(campos)
    r = registro_desde_dict(campos, "nuevo")
    carpeta = directorio / r.sesion
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{r.id}.yaml"
    if ruta.exists():
        raise FeedbackError(f"ya existe {ruta.name}: mismo contenido")
    doc: dict[str, Any] = {"id": r.id}
    for k, v in asdict(r).items():
        if k == "id" or v in (None, ""):
            continue
        doc[k] = v
    ruta.write_text(
        yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
        newline="\n",
    )
    return ruta


def trazar(identificador: str, registros: list[FeedbackRecord]) -> list[str]:
    """Cadena de un objeto: registros que lo tienen como objetivo y sus supersedes, en orden."""
    por_id = {r.id: r for r in registros}
    lineas: list[str] = []
    relacionados = [r for r in registros if r.objetivo.id == identificador or r.id == identificador]
    if not relacionados:
        return [f"sin registros de feedback para {identificador}"]
    for r in sorted(relacionados, key=lambda r: (r.fecha, r.id)):
        estado = "superseded" if any(x.supersede == r.id for x in registros) else "activo"
        lineas.append(
            f"{r.fecha} {r.id} [{estado}] {r.accion} sobre {r.objetivo.tipo}:{r.objetivo.id}"
            + (f" -> {r.valor_resultante}" if r.valor_resultante else "")
            + (f" (supersede {r.supersede})" if r.supersede else "")
        )
        if r.supersede and r.supersede in por_id:
            lineas.append(f"    corrige a: {por_id[r.supersede].respuesta_literal[:80]}")
    return lineas
