"""Propuestas de evidencia (F07, ADR-0009): prompt, modelo, salida y decision humana.

`knowledge/_proposals/<propuesta_id>.yaml` es el registro de lo que un proponente (un LLM o una
persona) propuso sobre un tramo de la cruda. Regimen: manual y versionado; tras `--check` la
salida queda sellada con `salida_sha256` y solo los campos de decision pueden cambiar. El
proponente nunca escribe en `knowledge/evidence/`: solo `aceptar` crea un item, con todas las
comprobaciones de `evidence new`.
"""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from botsito.comun import ids
from botsito.comun.documentos import hash_corto, normalizar_texto, sha256_hex, vacio
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.evidence.modelo import (
    CONFIANZAS,
    MODALIDADES,
    TIPOS,
    EvidenceItem,
    EvidenciaError,
    formato_hhmmss,
    parse_tiempo,
)
from botsito.evidence.verificacion import (
    CitaError,
    ContextoEvidencia,
    Localizacion,
    SegmentoCitable,
    comprobar_referencias,
    localizar_cita,
    tokens,
)

DIRECTORIO_PROPUESTAS = "knowledge/_proposals"
FICHERO_PROMPT = "PROMPT.md"
FICHERO_TEMAS = "knowledge/evidence/_temas.yaml"
PROPONENTES = ("llm", "humano")
DECISIONES = ("pendiente", "aceptado", "rechazado")
METODOS_REVISION = ("cruda_leida", "audio_oido", "fotograma_visto")
CAMPOS_PROPUESTA = (
    "propuesta_id",
    "video_id",
    "transcripcion",
    "t0",
    "t1",
    "prompt",
    "prompt_sha256",
    "modelo",
    "proponente",
    "generado_el",
    "contexto",
    "temas_buscados",
    "items",
    "no_consta",
)
CAMPOS_OPCIONALES_PROPUESTA = ("salida_sha256", "comprobado_el", "notas")
CAMPOS_ITEM = (
    "n",
    "t0",
    "t1",
    "modalidad",
    "tipo",
    "cita_literal",
    "afirmacion",
    "tema",
    "confianza",
)
CAMPOS_ITEM_OPCIONALES = ("valor", "fotogramas", "notas", "marca_heredada")
CAMPOS_DECISION = (
    "decision",
    "decidido_por",
    "decidido_el",
    "metodo_revision",
    "motivo",
    "evidence_id",
)


class PropuestaError(ValueError):
    """La propuesta no cumple su esquema o su sello."""


@dataclass(frozen=True, slots=True)
class Temas:
    raices: frozenset[str]
    valores_cerrados: frozenset[str]


def cargar_temas(ruta: Path) -> Temas:
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except (OSError, YamlError) as exc:
        raise PropuestaError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"raices", "valores_cerrados"}:
        raise PropuestaError(f"{ruta.name}: se esperan 'raices' y 'valores_cerrados'")
    raices, valores = doc["raices"], doc["valores_cerrados"]
    for nombre, lista in (("raices", raices), ("valores_cerrados", valores)):
        if not isinstance(lista, list) or not all(
            isinstance(x, str) and ids.es_id_de("parametro", x) for x in lista
        ):
            raise PropuestaError(f"{ruta.name}: {nombre} debe ser una lista de nombres simples")
    return Temas(frozenset(raices), frozenset(valores))


def id_propuesta(
    video_id: str, t0: str, t1: str, prompt_sha256: str, modelo: str, generado_el: str
) -> str:
    huella = hash_corto(f"{prompt_sha256}|{modelo}|{generado_el}")
    return (
        f"pr-{video_id}-{formato_hhmmss(parse_tiempo(t0))}-{formato_hhmmss(parse_tiempo(t1))}-"
        f"{huella}"
    )


def esqueleto(
    video_id: str,
    transcripcion: str,
    t0: str,
    t1: str,
    segmentos: Sequence[SegmentoCitable],
    referencias_tramo: Sequence[str],
    prompt: str,
    modelo: str,
    proponente: str,
    temas_buscados: Sequence[str],
    generado_el: str,
) -> dict[str, Any]:
    """La propuesta vacia: contexto de la cruda (sin `palabras`), referencias del tramo, prompt
    y `temas_buscados`. Quien propone rellena `items` y `no_consta`."""
    if proponente not in PROPONENTES:
        raise PropuestaError(f"proponente debe ser uno de {PROPONENTES}")
    if parse_tiempo(t0) >= parse_tiempo(t1):
        raise PropuestaError("t0 debe ser menor que t1")
    prompt_sha = sha256_hex(prompt.encode("utf-8"))
    contexto = {
        "segmentos": [
            {
                "n": s.n,
                "t0_ms": s.t0_ms,
                "t1_ms": s.t1_ms,
                "texto": s.texto,
                "senales": list(s.senales),
            }
            for s in segmentos
        ],
        "referencias": sorted(referencias_tramo),
    }
    return {
        "propuesta_id": id_propuesta(video_id, t0, t1, prompt_sha, modelo, generado_el),
        "video_id": video_id,
        "transcripcion": transcripcion,
        "t0": t0,
        "t1": t1,
        "prompt": prompt,
        "prompt_sha256": prompt_sha,
        "modelo": modelo,
        "proponente": proponente,
        "generado_el": generado_el,
        "contexto": contexto,
        "temas_buscados": sorted(temas_buscados),
        "items": [],
        "no_consta": [],
    }


def _canonico_salida(doc: dict[str, Any]) -> str:
    """Lo que sella `salida_sha256`: prompt, modelo, contexto, temas y la salida del proponente,
    SIN los campos de decision."""
    items = []
    for it in doc.get("items") or []:
        items.append({k: it[k] for k in sorted(it) if k not in CAMPOS_DECISION})
    cuerpo = {
        "prompt_sha256": doc.get("prompt_sha256"),
        "modelo": doc.get("modelo"),
        "contexto": doc.get("contexto"),
        "temas_buscados": doc.get("temas_buscados"),
        "items": items,
        "no_consta": doc.get("no_consta"),
    }
    return json.dumps(cuerpo, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def salida_sha256(doc: dict[str, Any]) -> str:
    return sha256_hex(_canonico_salida(doc).encode("utf-8"))


def cargar_propuesta(ruta: Path) -> dict[str, Any]:
    """Carga estricta: esquema del fichero, no de las citas (eso es `comprobar`)."""
    try:
        doc = cargar_yaml(ruta.read_text(encoding="utf-8"))
    except (OSError, YamlError) as exc:
        raise PropuestaError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict):
        raise PropuestaError(f"{ruta.name}: no es un mapa")
    faltan = [c for c in CAMPOS_PROPUESTA if c not in doc]
    if faltan:
        raise PropuestaError(f"{ruta.name}: faltan campos {faltan}")
    extra = set(doc) - set(CAMPOS_PROPUESTA) - set(CAMPOS_OPCIONALES_PROPUESTA)
    if extra:
        raise PropuestaError(f"{ruta.name}: campos desconocidos {sorted(extra)}")
    if not ids.es_id_de("propuesta", doc["propuesta_id"]):
        raise PropuestaError(f"{ruta.name}: propuesta_id invalido")
    if ruta.stem != doc["propuesta_id"]:
        raise PropuestaError(
            f"{ruta.name}: el nombre del fichero debe ser {doc['propuesta_id']}.yaml"
        )
    if not ids.es_id_de("transcripcion", doc["transcripcion"]):
        raise PropuestaError(f"{ruta.name}: transcripcion invalida")
    if doc["proponente"] not in PROPONENTES:
        raise PropuestaError(f"{ruta.name}: proponente debe ser uno de {PROPONENTES}")
    for clave in ("prompt", "prompt_sha256", "modelo", "generado_el", "video_id", "t0", "t1"):
        if not isinstance(doc[clave], str) or not doc[clave].strip():
            raise PropuestaError(f"{ruta.name}: {clave} vacio o no es texto")
    if sha256_hex(doc["prompt"].encode("utf-8")) != doc["prompt_sha256"]:
        raise PropuestaError(f"{ruta.name}: prompt_sha256 no coincide con el prompt")
    esperado = id_propuesta(
        doc["video_id"],
        doc["t0"],
        doc["t1"],
        doc["prompt_sha256"],
        doc["modelo"],
        doc["generado_el"],
    )
    if esperado != doc["propuesta_id"]:
        raise PropuestaError(f"{ruta.name}: propuesta_id no coincide con su contenido ({esperado})")
    for clave in ("items", "no_consta", "temas_buscados"):
        if not isinstance(doc[clave], list):
            raise PropuestaError(f"{ruta.name}: {clave} debe ser una lista")
    ctx = doc["contexto"]
    if not isinstance(ctx, dict) or set(ctx) != {"segmentos", "referencias"}:
        raise PropuestaError(f"{ruta.name}: contexto debe tener segmentos y referencias")
    for k, it in enumerate(doc["items"], start=1):
        _validar_item_propuesto(it, f"{ruta.name}: item {k}")
    for k, nc in enumerate(doc["no_consta"], start=1):
        if not isinstance(nc, dict) or set(nc) != {"tema", "motivo"}:
            raise PropuestaError(f"{ruta.name}: no_consta {k} debe tener tema y motivo")
        if not ids.es_id_de("contradiccion", str(nc["tema"])):
            raise PropuestaError(f"{ruta.name}: no_consta {k}: tema invalido")
    return doc


def _validar_item_propuesto(it: object, origen: str) -> None:
    if not isinstance(it, dict):
        raise PropuestaError(f"{origen}: debe ser un mapa")
    faltan = [c for c in CAMPOS_ITEM if vacio(it.get(c))]
    if faltan:
        raise PropuestaError(f"{origen}: faltan {faltan}")
    extra = set(it) - set(CAMPOS_ITEM) - set(CAMPOS_ITEM_OPCIONALES) - set(CAMPOS_DECISION)
    if extra:
        raise PropuestaError(f"{origen}: campos desconocidos {sorted(extra)}")
    if isinstance(it["n"], bool) or not isinstance(it["n"], int) or it["n"] < 1:
        raise PropuestaError(f"{origen}: n debe ser un entero >= 1")
    for clave, permitidos in (
        ("modalidad", MODALIDADES),
        ("tipo", TIPOS),
        ("confianza", CONFIANZAS),
    ):
        if it[clave] not in permitidos:
            raise PropuestaError(f"{origen}: {clave} {it[clave]!r} no esta en {permitidos}")
    for clave in ("t0", "t1", "cita_literal", "afirmacion", "tema"):
        if not isinstance(it[clave], str):
            raise PropuestaError(f"{origen}: {clave} debe ser texto entre comillas")
    try:
        if parse_tiempo(it["t0"]) >= parse_tiempo(it["t1"]):
            raise PropuestaError(f"{origen}: t0 debe ser menor que t1")
    except EvidenciaError as exc:
        raise PropuestaError(f"{origen}: {exc}") from exc
    if not ids.es_id_de("contradiccion", it["tema"]):
        raise PropuestaError(f"{origen}: tema invalido {it['tema']!r}")
    fotos = it.get("fotogramas")
    if fotos is not None and (
        not isinstance(fotos, list) or not all(isinstance(x, str) and x for x in fotos)
    ):
        raise PropuestaError(f"{origen}: fotogramas debe ser una lista de referencias")
    decision = it.get("decision", "pendiente")
    if decision not in DECISIONES:
        raise PropuestaError(f"{origen}: decision {decision!r} no esta en {DECISIONES}")
    if decision == "aceptado" and not ids.es_id_de("evidence", it.get("evidence_id")):
        raise PropuestaError(f"{origen}: un item aceptado lleva evidence_id")
    if decision == "rechazado" and vacio(it.get("motivo")):
        raise PropuestaError(f"{origen}: un item rechazado lleva motivo")
    if decision != "pendiente" and vacio(it.get("decidido_por")):
        raise PropuestaError(f"{origen}: una decision lleva decidido_por")
    metodo = it.get("metodo_revision")
    if metodo is not None and metodo not in METODOS_REVISION:
        raise PropuestaError(f"{origen}: metodo_revision {metodo!r} no esta en {METODOS_REVISION}")


def cargar_propuestas(directorio: Path) -> list[dict[str, Any]]:
    if not directorio.is_dir():
        return []
    docs = [cargar_propuesta(r) for r in sorted(directorio.glob("pr-*.yaml"))]
    vistos = [d["propuesta_id"] for d in docs]
    repetidos = sorted({i for i in vistos if vistos.count(i) > 1})
    if repetidos:
        raise PropuestaError(f"propuestas con id repetido: {repetidos}")
    return docs


def escribir_propuesta(ruta: Path, doc: dict[str, Any]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(
        "# Propuesta de evidencia (F07, ADR-0009). Editable SOLO en los campos de decision\n"
        "# (decision, decidido_por, decidido_el, metodo_revision, motivo, evidence_id): la salida\n"
        "# queda sellada por salida_sha256 tras `botsito evidence propose --check`.\n"
        + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=100),
        encoding="utf-8",
        newline="\n",
    )


def _ms(t: str) -> int:
    return round(parse_tiempo(t) * 1000)


def cita_normalizada(cita: str) -> str:
    return " ".join(tokens(cita.replace("[...]", " ")))


@dataclass(frozen=True, slots=True)
class ResultadoCheck:
    problemas: list[str]
    avisos: list[str]
    localizaciones: dict[int, Localizacion]


def comprobar(
    doc: dict[str, Any],
    contexto: ContextoEvidencia,
    temas: Temas,
    evidencia: Sequence[EvidenceItem] = (),
    otras_propuestas: Sequence[dict[str, Any]] = (),
) -> ResultadoCheck:
    """Las guardias del brief F07 (decisiones 2-4 y 7) item a item. No escribe nada."""
    problemas: list[str] = []
    avisos: list[str] = []
    localizaciones: dict[int, Localizacion] = {}
    tid = doc["transcripcion"]
    video = doc["video_id"]
    if contexto.transcripciones and contexto.transcripciones.get(tid) != video:
        problemas.append(f"transcripcion {tid} no existe o no es de {video}")
    if contexto.activas and contexto.activas.get(video) != tid:
        avisos.append(f"la transcripcion {tid} no es la activa de {video}")
    segmentos = contexto.crudas(tid) if contexto.crudas else None
    if segmentos is None:
        avisos.append(f"cruda de {tid} ausente en data/: citas de audio no verificables aqui")
    dudas = contexto.dudas(tid) if contexto.dudas else set()
    citas_previas: dict[str, str] = {}
    for ev in evidencia:
        citas_previas[cita_normalizada(ev.cita_literal)] = ev.id
    rechazadas: dict[str, str] = {}
    for otra in otras_propuestas:
        if otra.get("propuesta_id") == doc.get("propuesta_id"):
            continue
        for it in otra.get("items") or []:
            clave = cita_normalizada(str(it.get("cita_literal", "")))
            if it.get("decision") == "rechazado":
                rechazadas[clave] = str(otra["propuesta_id"])
            elif it.get("decision") == "aceptado":
                citas_previas[clave] = str(it.get("evidence_id"))
    vistas: dict[str, int] = {}
    por_tema: list[tuple[str, str, int, int, int]] = []
    numeros = [it["n"] for it in doc["items"]]
    if len(set(numeros)) != len(numeros):
        problemas.append("numeros de item repetidos")
    for it in doc["items"]:
        n = it["n"]
        pref = f"item {n}"
        cita = str(it["cita_literal"])
        clave = cita_normalizada(cita)
        if clave in vistas:
            problemas.append(f"{pref}: misma cita que el item {vistas[clave]}")
        vistas[clave] = n
        if clave in citas_previas:
            problemas.append(f"{pref}: misma cita que la evidencia {citas_previas[clave]}")
        if clave in rechazadas:
            avisos.append(f"{pref}: una cita igual fue rechazada en {rechazadas[clave]}")
        raiz = str(it["tema"]).split(".")[0]
        if raiz not in temas.raices:
            problemas.append(f"{pref}: tema {it['tema']!r} fuera de la taxonomia (raiz {raiz!r})")
        if parse_tiempo(it["t0"]) < parse_tiempo(doc["t0"]) or parse_tiempo(
            it["t1"]
        ) > parse_tiempo(doc["t1"]):
            problemas.append(f"{pref}: fuera del tramo de la propuesta")
        modalidad = it["modalidad"]
        fotos = list(it.get("fotogramas") or [])
        if modalidad == "audio" and fotos:
            problemas.append(f"{pref}: modalidad audio no admite fotogramas")
        if modalidad in ("pantalla", "ambas"):
            if contexto.referencias is None:
                problemas.append(f"{pref}: faltan referencias conocidas para validar fotogramas")
            else:
                problemas += [
                    f"{pref}: {p}"
                    for p in comprobar_referencias(
                        video, _ms(it["t0"]), _ms(it["t1"]), modalidad, fotos, contexto.referencias
                    )
                ]
        if modalidad in ("audio", "ambas"):
            try:
                if len(tokens(cita.replace("[...]", " "))) < 4:  # no-negocio: minimo de tokens
                    raise CitaError("la cita tiene menos de 4 tokens")
                if segmentos is not None:
                    loc = localizar_cita(segmentos, _ms(it["t0"]), _ms(it["t1"]), cita)
                    localizaciones[n] = loc
                    por_tema.append((str(it["tema"]), modalidad, loc.t0_ms, loc.t1_ms, n))
                    con_duda = bool(set(loc.segmentos) & dudas)
                    if (loc.senales or con_duda) and it["confianza"] == "alta":
                        motivo = (
                            "senales " + ",".join(loc.senales)
                            if loc.senales
                            else "duda del glosario"
                        )
                        problemas.append(f"{pref}: confianza alta con {motivo} en la cruda")
                    if loc.coincidencias > 1:
                        avisos.append(
                            f"{pref}: la cita casa {loc.coincidencias} veces en la ventana"
                        )
                    avisos += [f"{pref}: {a}" for a in loc.avisos]
            except CitaError as exc:
                problemas.append(f"{pref}: {exc}")
        else:
            if len(tokens(cita)) < 1:
                problemas.append(f"{pref}: cita de pantalla vacia")
        valor = it.get("valor")
        if valor is not None:
            v = normalizar_texto(str(valor)).casefold()
            en_cita = v in tokens(cita.replace("[...]", " ")) or v in temas.valores_cerrados
            if not en_cita:
                problemas.append(
                    f"{pref}: valor {valor!r} no aparece en la cita ni en los valores cerrados"
                )
    for i, (tema_a, mod_a, a0, a1, na) in enumerate(por_tema):
        for tema_b, mod_b, b0, b1, nb in por_tema[i + 1 :]:
            if tema_a == tema_b and mod_a == mod_b and a0 < b1 and b0 < a1:
                problemas.append(f"item {na} e item {nb}: mismo tema y localizacion solapada")
    temas_cubiertos = {str(it["tema"]) for it in doc["items"]} | {
        str(nc["tema"]) for nc in doc["no_consta"]
    }
    for tema in doc["temas_buscados"]:
        if not any(t == tema or t.startswith(tema + ".") for t in temas_cubiertos):
            problemas.append(f"tema buscado {tema!r} sin item ni no_consta")
    return ResultadoCheck(problemas, avisos, localizaciones)


def sellar(doc: dict[str, Any], comprobado_el: str) -> None:
    doc["salida_sha256"] = salida_sha256(doc)
    doc["comprobado_el"] = comprobado_el


def comprobar_sello(doc: dict[str, Any]) -> str | None:
    sello = doc.get("salida_sha256")
    if not sello:
        return "la propuesta no ha pasado por `propose --check` (sin salida_sha256)"
    if sello != salida_sha256(doc):
        return "la salida cambio despues del check: crea otra propuesta"
    return None


def _item(doc: dict[str, Any], n: int) -> dict[str, Any]:
    for it in doc["items"]:
        if isinstance(it, dict) and it.get("n") == n:
            return it
    raise PropuestaError(f"la propuesta no tiene el item {n}")


def campos_de_item(doc: dict[str, Any], n: int, revisado_por: str, metodo: str) -> dict[str, Any]:
    """Los campos de `EvidenceItem` que se crean al aceptar el item `n`."""
    if metodo not in METODOS_REVISION:
        raise PropuestaError(f"metodo_revision debe ser uno de {METODOS_REVISION}")
    it = _item(doc, n)
    if it.get("decision", "pendiente") != "pendiente":
        raise PropuestaError(f"el item {n} ya esta {it['decision']}")
    if it["modalidad"] in ("pantalla", "ambas") and metodo != "fotograma_visto":
        raise PropuestaError(f"el item {n} es de pantalla: exige metodo_revision fotograma_visto")
    provenance = "bot-v2" if not vacio(it.get("marca_heredada")) else "botsito"
    campos: dict[str, Any] = {
        "video_id": doc["video_id"],
        "t0": it["t0"],
        "t1": it["t1"],
        "modalidad": it["modalidad"],
        "tipo": it["tipo"],
        "cita_literal": it["cita_literal"],
        "afirmacion": it["afirmacion"],
        "tema": it["tema"],
        "valor": it.get("valor"),
        "confianza": it["confianza"],
        "extractor": doc["proponente"],
        "revisado_por": revisado_por,
        "provenance": provenance,
        "fotogramas": list(it.get("fotogramas") or []),
        "notas": it.get("notas"),
    }
    if it["modalidad"] != "pantalla":
        campos["transcripcion"] = doc["transcripcion"]
    return campos


def anotar_decision(
    doc: dict[str, Any],
    n: int,
    decision: str,
    decidido_por: str,
    decidido_el: str,
    metodo: str | None = None,
    motivo: str | None = None,
    evidence_id: str | None = None,
) -> None:
    it = _item(doc, n)
    it["decision"] = decision
    it["decidido_por"] = decidido_por
    it["decidido_el"] = decidido_el
    if metodo:
        it["metodo_revision"] = metodo
    if motivo:
        it["motivo"] = motivo
    if evidence_id:
        it["evidence_id"] = evidence_id


def validar_propuestas(
    docs: Sequence[dict[str, Any]], ids_evidencia: set[str], prompt_actual_sha: str | None
) -> tuple[list[str], list[str]]:
    """Para `knowledge validate`: sello intacto, evidence_id existentes, prompt vigente."""
    problemas: list[str] = []
    avisos: list[str] = []
    for doc in docs:
        pid = doc["propuesta_id"]
        sello = doc.get("salida_sha256")
        if sello and sello != salida_sha256(doc):
            problemas.append(f"{pid}: la salida cambio despues del check")
        if not sello and any(it.get("decision", "pendiente") != "pendiente" for it in doc["items"]):
            problemas.append(f"{pid}: decisiones sobre una propuesta sin check")
        for it in doc["items"]:
            eid = it.get("evidence_id")
            if eid and eid not in ids_evidencia:
                problemas.append(f"{pid}: item {it['n']} anota evidence_id {eid} inexistente")
        if prompt_actual_sha and doc["prompt_sha256"] != prompt_actual_sha:
            avisos.append(f"{pid}: prompt distinto del PROMPT.md actual")
    return problemas, avisos
