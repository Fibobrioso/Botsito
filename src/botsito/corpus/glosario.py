"""Glosario del ASR (F04, ADR-0007): vocabulario para el motor y correcciones de dos alcances.

`knowledge/corpus/glosario_asr.yaml`:
- `vocabulario`: terminos del dominio que se pasan al motor como `initial_prompt` (mejora la
  jerga) y que ninguna sustitucion global puede tocar.
- `sustituciones`: `alcance: global` solo para "antes" que NO son palabra del dominio
  ("brequiven", "cargo chuto"); `alcance: segmento` (con `transcripcion_id` y `segmento`) para
  ambiguedades reales (M5/M15, FVG/FTMO), con `verificado_por`. Ambas exigen `motivo` y ejemplo.
Patrones Unicode (`\\b` reconoce n con tilde y vocales acentuadas), sin distinguir mayusculas,
con limites en ambos extremos y sin `.*`/`.+`. Texto y patrones se normalizan a NFC.
`aplicar(cruda, glosario)` es determinista; `dudas` lista los segmentos donde aparece un
termino ambiguo sin corregir, para que F07 los mire.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.documentos import hash_corto, sha256_hex
from botsito.comun.yaml_estricto import YamlError, cargar_yaml
from botsito.corpus.transcripcion import Segmento

ALCANCES = ("global", "segmento")
CAMPOS_BASE = ("patron", "reemplazo", "alcance", "motivo", "ejemplo_video", "ejemplo_t0")
CAMPOS_SEGMENTO = ("transcripcion_id", "segmento", "verificado_por")
_LIMITE_INICIO = (r"\b", r"(?<!\w)")
_LIMITE_FIN = (r"\b", r"(?!\w)")
# Comodines o cuantificadores que casarian texto arbitrario aunque lleven \b en los extremos
# (`\b\w+\b`, `\b\d+\b`, `[a-z]+`, `m.`): solo entran literales (con `\.` escapado),
# alternancias, grupos y `?`.
_SIN_LIMITE = re.compile(r"\.\*|\.\+|\[\^|\\[SsWwDd]|\.\{|(?<!\\)[+*{\[.]")


class GlosarioError(ValueError):
    """El glosario no cumple su esquema."""


@dataclass(frozen=True, slots=True)
class Sustitucion:
    patron: re.Pattern[str]
    reemplazo: str
    alcance: str
    motivo: str
    ejemplo_video: str
    ejemplo_t0: str
    transcripcion_id: str | None = None
    segmento: int | None = None
    verificado_por: str | None = None
    texto_patron: str = ""  # el patron tal como lo escribio el usuario (para el registro)


@dataclass(frozen=True, slots=True)
class Glosario:
    version: str  # hash corto del fichero: cambia con cualquier edicion
    sha256: str
    vocabulario: tuple[str, ...]
    sustituciones: tuple[Sustitucion, ...]

    @property
    def prompt_inicial(self) -> str:
        return ", ".join(self.vocabulario)


def _nfc(texto: str) -> str:
    return unicodedata.normalize("NFC", texto)


def cargar_glosario(ruta: Path) -> Glosario:
    if not ruta.exists():
        raise GlosarioError(f"no existe {ruta}")
    texto = ruta.read_text(encoding="utf-8")
    try:
        doc = cargar_yaml(texto) or {}
    except YamlError as exc:
        raise GlosarioError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) - {"vocabulario", "sustituciones"}:
        raise GlosarioError(f"{ruta.name}: solo se admiten 'vocabulario' y 'sustituciones'")
    vocab_bruto = doc.get("vocabulario") or []
    if not isinstance(vocab_bruto, list) or not all(
        isinstance(v, str) and v.strip() for v in vocab_bruto
    ):
        raise GlosarioError(f"{ruta.name}: 'vocabulario' debe ser una lista de textos")
    vocabulario = tuple(_nfc(" ".join(v.split())) for v in vocab_bruto)
    lista = doc.get("sustituciones") or []
    if not isinstance(lista, list):
        raise GlosarioError(f"{ruta.name}: 'sustituciones' debe ser una lista")
    salida: list[Sustitucion] = []
    for n, bruto in enumerate(lista, start=1):
        salida.append(_sustitucion(bruto, f"{ruta.name}: entrada {n}", vocabulario))
    return Glosario(
        hash_corto(texto), sha256_hex(texto.encode("utf-8")), vocabulario, tuple(salida)
    )


def _sustitucion(bruto: object, origen: str, vocabulario: tuple[str, ...]) -> Sustitucion:
    if not isinstance(bruto, dict):
        raise GlosarioError(f"{origen}: debe ser un mapa")
    alcance = bruto.get("alcance")
    if alcance not in ALCANCES:
        raise GlosarioError(f"{origen}: alcance debe ser uno de {ALCANCES}")
    esperados = set(CAMPOS_BASE) | (set(CAMPOS_SEGMENTO) if alcance == "segmento" else set())
    if set(bruto) != esperados:
        raise GlosarioError(f"{origen}: campos esperados {sorted(esperados)}, hay {sorted(bruto)}")
    for c in CAMPOS_BASE:
        if not isinstance(bruto[c], str) or not bruto[c].strip():
            raise GlosarioError(f"{origen}: {c} vacio o no es texto")
    patron = _nfc(bruto["patron"])
    if not patron.startswith(_LIMITE_INICIO) or not patron.endswith(_LIMITE_FIN):
        raise GlosarioError(f"{origen}: el patron debe llevar limites de palabra en ambos extremos")
    if _SIN_LIMITE.search(patron):
        raise GlosarioError(
            f"{origen}: el patron no puede contener comodines ni cuantificadores sin limite "
            "(.* .+ [^ \\w \\d \\s + * { [)"
        )
    try:
        # Envuelto en limites propios: una alternancia (`\bfoo|bar\b`) no puede saltarse la regla
        # de "limites en ambos extremos".
        compilado = re.compile(rf"(?<!\w)(?:{patron})(?!\w)", re.IGNORECASE)
    except re.error as exc:
        raise GlosarioError(f"{origen}: patron invalido ({exc})") from exc
    if alcance == "global":
        for termino in vocabulario:
            if compilado.search(termino):
                raise GlosarioError(
                    f"{origen}: una sustitucion global no puede casar con el termino del "
                    f"vocabulario {termino!r}; usa alcance: segmento"
                )
        return Sustitucion(
            compilado,
            _nfc(bruto["reemplazo"]),
            alcance,
            bruto["motivo"],
            bruto["ejemplo_video"],
            bruto["ejemplo_t0"],
            texto_patron=patron,
        )
    if not ids.es_id_de("transcripcion", bruto["transcripcion_id"]):
        raise GlosarioError(f"{origen}: transcripcion_id invalido")
    seg = bruto["segmento"]
    if isinstance(seg, bool) or not isinstance(seg, int) or seg < 0:
        raise GlosarioError(f"{origen}: segmento debe ser un entero >= 0")
    if not isinstance(bruto["verificado_por"], str) or not bruto["verificado_por"].strip():
        raise GlosarioError(f"{origen}: verificado_por es obligatorio en alcance segmento")
    return Sustitucion(
        compilado,
        _nfc(bruto["reemplazo"]),
        alcance,
        bruto["motivo"],
        bruto["ejemplo_video"],
        bruto["ejemplo_t0"],
        bruto["transcripcion_id"],
        seg,
        bruto["verificado_por"],
        patron,
    )


def _literal(reemplazo: str) -> Callable[[re.Match[str]], str]:
    return lambda _m: reemplazo


@dataclass(frozen=True, slots=True)
class Correccion:
    segmento: int
    patron: str
    alcance: str
    antes: str
    despues: str


def aplicar(
    segmentos: list[Segmento], glosario: Glosario, transcripcion_id: str | None = None
) -> tuple[list[Segmento], list[Correccion], list[int]]:
    """(corregida, correcciones, dudas). Las globales se aplican a todo; las de segmento solo al
    segmento de SU transcripcion. `dudas`: segmentos donde un patron de alcance segmento casa
    sin aplicarse (otra transcripcion u otro segmento): F07 los revisa."""
    corregidos: list[Segmento] = []
    registro: list[Correccion] = []
    dudas: list[int] = []
    for s in segmentos:
        texto = _nfc(s.texto)
        duda = False
        for sub in glosario.sustituciones:
            if sub.alcance == "segmento":
                mia = sub.transcripcion_id == transcripcion_id and sub.segmento == s.n
                if not mia:
                    duda = duda or bool(sub.patron.search(texto))
                    continue
            # Reemplazo LITERAL (no plantilla de re.sub: `\1` o `\b` no se interpretan).
            nuevo = sub.patron.sub(_literal(sub.reemplazo), texto)
            if nuevo != texto:
                registro.append(Correccion(s.n, sub.texto_patron, sub.alcance, texto, nuevo))
                texto = nuevo
        if duda:
            dudas.append(s.n)
        corregidos.append(
            Segmento(
                s.n,
                s.t0_ms,
                s.t1_ms,
                texto,
                s.palabras,
                s.no_speech_prob,
                s.compression_ratio,
                s.avg_logprob,
                s.senales,
            )
        )
    return corregidos, registro, dudas


def correcciones_jsonl(glosario: Glosario, registro: list[Correccion], dudas: list[int]) -> str:
    cabecera = {
        "glosario_version": glosario.version,
        "glosario_sha256": glosario.sha256,
        "dudas": dudas,
    }
    lineas = [json.dumps(cabecera, ensure_ascii=False, sort_keys=True)]
    lineas += [
        json.dumps(
            {
                "segmento": c.segmento,
                "patron": c.patron,
                "alcance": c.alcance,
                "antes": c.antes,
                "despues": c.despues,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
        for c in registro
    ]
    return "\n".join(lineas) + "\n"


def glosario_desde_texto(texto: str) -> Glosario:
    """Para tests: un glosario desde YAML en memoria."""
    import tempfile

    with tempfile.TemporaryDirectory() as d:
        ruta = Path(d) / "glosario_asr.yaml"
        ruta.write_text(texto, encoding="utf-8")
        return cargar_glosario(ruta)


def resumen(glosario: Glosario) -> dict[str, Any]:
    return {
        "version": glosario.version,
        "sha256": glosario.sha256,
        "vocabulario": len(glosario.vocabulario),
        "sustituciones_globales": sum(1 for s in glosario.sustituciones if s.alcance == "global"),
        "sustituciones_segmento": sum(1 for s in glosario.sustituciones if s.alcance == "segmento"),
    }
