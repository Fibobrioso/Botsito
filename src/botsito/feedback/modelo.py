"""FeedbackRecord (F09): cada aportacion del trader como registro trazable y solo-anadir.

Un registro dice que dijo el trader (literal), sobre que objeto (evidencia, regla, parametro,
ambiguedad, caso o contradiccion), con que accion, en que sesion y por que medio, y quien lo
registro. Nunca modifica la evidencia ni otro registro: los supersede. El id incluye un hash del
contenido y el historial de git se vigila igual que el de la evidencia.
"""

from __future__ import annotations

import datetime
import json
import re
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.comun import ids
from botsito.comun.documentos import (
    activos,
    cargar_directorio,
    ciclos_de_supersede,
    hash_corto,
    normalizar_texto,
    vacio,
)
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.evidence.modelo import EvidenciaError, parse_tiempo

__all__ = ["activos", "ciclos_de_supersede"]
_normalizar_texto = normalizar_texto
_vacio = vacio

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
TIPOS_OBJETIVO = (
    "evidence",
    "regla",
    "parametro",
    "ambiguedad",
    "caso",
    "contradiccion",
    "paquete",
)
MEDIOS = ("replay", "audio", "video", "escrito")
OBJETIVOS_POR_ACCION: dict[str, tuple[str, ...]] = {
    # `paquete` en CONFIRM/REJECT: la precondicion de ceguera de una sesion (F10). El trader
    # confirma que no ha visto los meses de las ventanas, o la rechaza y hay que regenerar.
    "CONFIRM": ("evidence", "regla", "parametro", "paquete"),
    "CORRECT": ("evidence", "regla", "parametro"),
    "REJECT": ("evidence", "regla", "parametro", "paquete"),
    "RESOLVE_UNKNOWN": ("parametro", "ambiguedad", "evidence"),
    "RESOLVE_CONTRADICTION": ("contradiccion",),
    "LABEL_CASE": ("caso",),
    "MARK_FALSE_POSITIVE": ("caso",),
    "MARK_FALSE_NEGATIVE": ("caso",),
    "BORDERLINE": ("caso",),
}
EXIGEN_VALOR = ("CORRECT", "RESOLVE_UNKNOWN", "RESOLVE_CONTRADICTION", "LABEL_CASE")
# re.ASCII: sin el, `\d` acepta digitos arabigos u otros Unicode, y un id con ellos no se puede
# citar desde el registro ni supersederse.
FORMATO_ID_OBJETIVO: dict[str, re.Pattern[str]] = {t: ids.POR_TIPO[t] for t in TIPOS_OBJETIVO}
_SESION = ids.PAQUETE
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
_ID = ids.FEEDBACK
CAMPOS_OBLIGATORIOS = (
    "sesion",
    "fecha",
    "medio",
    "objetivo",
    "accion",
    "respuesta_literal",
    "registrado_por",
)
CAMPOS_OPCIONALES = (
    "grabacion",
    "t0",
    "t1",
    "valor_resultante",
    "valor_canonico",
    "supersede",
    "notas",
)
CAMPOS_TEXTO = (
    "sesion",
    "fecha",
    "medio",
    "accion",
    "respuesta_literal",
    "registrado_por",
    "grabacion",
    "t0",
    "t1",
    "valor_resultante",
    "valor_canonico",
    "supersede",
    "notas",
)


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
    # Re-expresion del valor en el tipo que espera el registro (F11): '0,8' -> '0.8'. La
    # escribe el consultor en un registro que supersede, con el literal del trader intacto;
    # `feedback apply` la usa tal cual y no interpreta nada.
    valor_canonico: str | None = None
    supersede: str | None = None
    notas: str | None = None


def contenido_canonico(campos: dict[str, Any]) -> str:
    limpio: dict[str, Any] = {}
    for clave in (*CAMPOS_OBLIGATORIOS, *CAMPOS_OPCIONALES):
        if clave not in campos or _vacio(campos[clave]):
            continue  # un campo en blanco no forma parte del contenido (ni del id)
        v = campos[clave]
        if clave == "objetivo" and isinstance(v, dict):
            limpio[clave] = {str(k): _normalizar_texto(x) for k, x in sorted(v.items())}
        elif isinstance(v, str):
            limpio[clave] = _normalizar_texto(v)
        else:
            limpio[clave] = v
    return json.dumps(limpio, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def limpiar_campos(campos: dict[str, Any]) -> dict[str, Any]:
    """Textos normalizados y campos vacios fuera, ANTES de calcular el id.

    Si el id se calculara con un campo en blanco que luego no se escribe, el fichero naceria con
    un id que no coincide con su contenido y nadie podria cargarlo.
    """
    limpio: dict[str, Any] = {}
    for k, v in campos.items():
        if k == "objetivo" and isinstance(v, dict):
            v = {str(a): _normalizar_texto(b) for a, b in v.items() if not _vacio(b)}
        elif isinstance(v, str):
            v = _normalizar_texto(v)
        if not _vacio(v):
            limpio[k] = v
    return limpio


def calcular_id(campos: dict[str, Any]) -> str:
    if _vacio(campos.get("sesion")):
        raise FeedbackError("sesion es obligatoria para calcular el id")
    esperado = f"fb-{campos['sesion']}-{hash_corto(contenido_canonico(campos))}"
    if not _ID.match(esperado):
        raise FeedbackError(f"id calculado {esperado!r} fuera de formato")
    return esperado


def _fecha_real(texto: str) -> bool:
    try:
        datetime.date.fromisoformat(texto)
    except ValueError:
        return False
    return True


def _validar(campos: dict[str, Any], origen: str) -> None:
    faltan = [c for c in CAMPOS_OBLIGATORIOS if _vacio(campos.get(c))]
    if faltan:
        raise FeedbackError(f"{origen}: faltan campos obligatorios {faltan}")
    desconocidos = set(campos) - set(CAMPOS_OBLIGATORIOS) - set(CAMPOS_OPCIONALES) - {"id"}
    if desconocidos:
        raise FeedbackError(f"{origen}: campos desconocidos {sorted(desconocidos)}")
    for clave in CAMPOS_TEXTO:
        if campos.get(clave) is not None and not isinstance(campos[clave], str):
            tipo_real = type(campos[clave]).__name__
            raise FeedbackError(f"{origen}: {clave} debe ser texto entre comillas, no {tipo_real}")
    if not _SESION.match(str(campos["sesion"])):
        raise FeedbackError(f"{origen}: sesion invalida (formato AAAA-MM-DD-sesion-NN)")
    if not _FECHA.match(str(campos["fecha"])) or not _fecha_real(str(campos["fecha"])):
        raise FeedbackError(f"{origen}: fecha invalida (AAAA-MM-DD)")
    if not str(campos["sesion"]).startswith(str(campos["fecha"])):
        raise FeedbackError(f"{origen}: la fecha debe ser la de la sesion {campos['sesion']}")
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
    tiempos: dict[str, float] = {}
    for c in ("t0", "t1"):
        if campos.get(c) is not None:
            try:
                tiempos[c] = parse_tiempo(str(campos[c]))
            except EvidenciaError as exc:
                raise FeedbackError(f"{origen}: {c}: {exc}") from exc
    if len(tiempos) == 2 and not tiempos["t0"] < tiempos["t1"]:
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
        valor_canonico=txt("valor_canonico"),
        supersede=txt("supersede"),
        notas=txt("notas"),
    )


def cargar_registro(ruta: Path) -> FeedbackRecord:
    try:
        doc = leer_yaml(ruta)
    except YamlError as exc:
        raise FeedbackError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise FeedbackError(f"{ruta.name}: no es un mapa YAML")
    r = registro_desde_dict(doc, ruta.name)
    if ruta.stem != r.id:
        raise FeedbackError(f"{ruta.name}: el nombre del fichero debe ser {r.id}.yaml")
    if ruta.parent.name != r.sesion:
        raise FeedbackError(f"{ruta.name}: debe estar en la carpeta de su sesion {r.sesion}/")
    return r


def cargar_feedback(directorio: Path) -> list[FeedbackRecord]:
    """Todos los registros bajo `directorio`; un fichero que no sea `*.yaml` (salvo README y
    `_*`) es error."""
    return cargar_directorio(directorio, cargar_registro, FeedbackError, "feedback", lambda r: r.id)


def validar_contra_contexto(
    registros: list[FeedbackRecord],
    ids_evidencia: set[str],
    nombres_parametros: set[str],
    temas_contradiccion: set[str],
    rutas_corpus: set[str] | None = None,
    ids_ambiguedades: set[str] | None = None,
    duraciones: dict[str, float] | None = None,
) -> list[str]:
    """Los objetivos existen donde ya hay contra que comprobar.

    `ambiguedad` se comprueba contra `knowledge/spec/ambiguedades.yaml` (F10) cuando se pasa el
    conjunto; `caso` y `regla` solo por formato hasta F14/F11. `duraciones` (ruta de grabacion ->
    segundos, F10) rechaza un `t1` mas alla del final de la grabacion.
    """
    problemas: list[str] = []
    por_id = {r.id: r for r in registros}
    ids = set(por_id)
    for r in registros:
        t, i = r.objetivo.tipo, r.objetivo.id
        if t == "evidence" and i not in ids_evidencia:
            problemas.append(f"{r.id}: evidencia objetivo {i} no existe")
        elif t == "parametro" and i not in nombres_parametros:
            problemas.append(f"{r.id}: parametro objetivo {i} no esta en el registro")
        elif t == "contradiccion" and i not in temas_contradiccion:
            problemas.append(f"{r.id}: no hay contradiccion abierta sobre {i}")
        elif t == "ambiguedad" and ids_ambiguedades is not None and i not in ids_ambiguedades:
            problemas.append(f"{r.id}: ambiguedad objetivo {i} no esta en ambiguedades.yaml")
        elif t == "paquete" and i != r.sesion:
            # Un paquete solo se confirma dentro de su propia sesion: si no, la precondicion de
            # ceguera quedaria fechada en un dia que no es aquel en que se pregunto.
            problemas.append(f"{r.id}: el paquete objetivo {i} no es la sesion {r.sesion}")
        if (
            duraciones
            and r.grabacion in duraciones
            and r.t1
            and parse_tiempo(r.t1) > duraciones[r.grabacion]
        ):
            problemas.append(
                f"{r.id}: t1 {r.t1} supera la duracion de {r.grabacion} "
                f"({duraciones[r.grabacion]:.3f} s)"
            )
        if r.supersede and r.supersede not in ids:
            problemas.append(f"{r.id}: supersede a {r.supersede}, que no existe")
        if r.supersede == r.id:
            problemas.append(f"{r.id}: no puede supersederse a si mismo")
        elif r.supersede in por_id and por_id[r.supersede].objetivo != r.objetivo:
            anterior = por_id[r.supersede].objetivo
            problemas.append(
                f"{r.id}: supersede a {r.supersede}, que trata de {anterior.tipo}:{anterior.id}, "
                f"no de {t}:{i}; una correccion habla del mismo objetivo"
            )
        if rutas_corpus is not None and r.grabacion and r.grabacion not in rutas_corpus:
            problemas.append(f"{r.id}: grabacion {r.grabacion!r} no esta inventariada en el corpus")
    # Dos registros que superseden al MISMO: el error natural de una ronda intensiva, cuando se
    # corrige una respuesta y luego se vuelve a corregir apuntando por inercia al original. Sin
    # esto quedan dos registros activos y contradictorios, y el fallo solo asoma mucho despues,
    # al calcular el kappa. El mensaje empieza por el id del registro nuevo para que la CLI lo
    # reconozca como suyo y `feedback new` lo rechace en el momento.
    quien_supersede: dict[str, list[str]] = {}
    for r in registros:
        if r.supersede:
            quien_supersede.setdefault(r.supersede, []).append(r.id)
    for anulado, autores in sorted(quien_supersede.items()):
        if len(autores) > 1:
            for a in sorted(autores):
                otros = ", ".join(x for x in sorted(autores) if x != a)
                problemas.append(
                    f"{a}: {anulado} ya esta superseded por {otros}; una correccion supersede al "
                    "ultimo registro del objetivo, no al original"
                )
    problemas += ciclos_de_supersede({r.id: r.supersede for r in registros})
    return problemas


def escribir_registro(
    directorio: Path,
    campos: dict[str, Any],
    comprobar: Callable[[FeedbackRecord], list[str]] | None = None,
) -> Path:
    """Crea el fichero de un registro nuevo. Nunca sobreescribe.

    `comprobar` recibe el registro ya validado y devuelve problemas de contexto (objetivo
    inexistente, grabacion no inventariada...). Si hay alguno, no se escribe nada: un registro
    es inmutable y un error solo se arreglaria con otro registro que lo supersede.
    """
    campos = limpiar_campos(campos)
    _validar(campos, "nuevo")
    campos["id"] = calcular_id(campos)
    r = registro_desde_dict(campos, "nuevo")
    problemas = comprobar(r) if comprobar else []
    if problemas:
        raise FeedbackError("; ".join(problemas))
    carpeta = directorio / r.sesion
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"{r.id}.yaml"
    doc: dict[str, Any] = {"id": r.id}
    for k, v in asdict(r).items():
        if k == "id" or v in (None, ""):
            continue
        doc[k] = v
    texto = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100)
    if ruta.exists():
        # El id sale del contenido, asi que lo normal es que sea el mismo registro repetido; que
        # NO lo sea significa que el fichero se edito a mano, y eso hay que mirarlo, no pisarlo.
        que = "mismo contenido" if ruta.read_text(encoding="utf-8") == texto else "OTRO contenido"
        raise FeedbackError(f"ya existe {ruta.name}: {que}")
    ruta.write_text(texto, encoding="utf-8", newline="\n")
    try:
        cargar_registro(ruta)  # invariante: lo escrito se puede volver a cargar
    except FeedbackError:
        ruta.unlink()
        raise
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
