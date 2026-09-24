"""La busqueda de A-18 en las transcripciones, CONGELADA antes de ejecutarla.

Documento: `docs/validation/A18-TRANSCRIPCIONES-CRITERIO.md` (2026-09-23, rama
`trabajo/a18-transcripciones`). Este script es su implementacion exacta; cambiarlo despues de ver la
salida es cambiar el criterio.

  `uv run python scripts/a18_buscar.py --salida <fichero>`  -> una sola ejecucion, salida tal cual.

Lee solo la transcripcion CRUDA (`cruda.jsonl`) de las cinco vigentes de la lista cerrada, despues
de comprobar que sus bytes son los que fija su manifiesto commiteado (`sha256_cruda`). No clasifica:
extrae pasajes.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MANIFIESTOS = RAIZ / "knowledge" / "corpus" / "transcripciones"
DATOS = RAIZ / "data"
# EL ALCANCE, lista cerrada (decision del consultor, 2026-09-23): las vigentes de v1 a v5. Fuera la
# de v6 (grabada en un dia reservado, ADR-0037), las heredadas y las sustituidas.
ALCANCE = (
    "tr-v1-large-v3-int8-float16-bbd8a931",
    "tr-v2-large-v3-int8-float16-28391c2c",
    "tr-v3-large-v3-int8-float16-270a4851",
    "tr-v4-large-v3-int8-float16-a8d1bccc",
    "tr-v5-large-v3-int8-float16-3c6fbb57",
)
# LOS TERMINOS, lista cerrada y en el orden del brief. No se anade ni se quita ninguno despues.
TERMINOS = (
    "stop", "stop loss", "SL", "protejo", "proteger", "protección", "protegido",
    "0.8", "0,8", "0.80", "0,80", "punto ocho", "ochenta por ciento", "80%",
    "caja", "caja completa", "toda la caja", "nivel uno", "nivel 1", "cien por ciento", "100%",
    "take profit", "TP", "objetivo", "uno a tres", "1 a 3", "1:3", "tres R", "3R",
    "relación", "ratio", "RR", "riesgo", "uno por ciento", "1%", "beneficio",
)  # fmt: skip
VENTANA_MS = 45_000


class IntegridadError(ValueError):
    """Una transcripcion fuera de la lista cerrada, o cuyos bytes no son los del manifiesto."""


def normalizar(texto: str) -> str:
    """Minusculas, sin tildes (NFD sin marcas combinantes) y con los espacios reducidos a uno."""
    sin_marcas = "".join(
        c for c in unicodedata.normalize("NFD", texto) if not unicodedata.combining(c)
    )
    return " ".join(sin_marcas.lower().split())


def patron(termino: str) -> re.Pattern[str]:
    """Coincidencia por palabra o frase: a ningun lado puede haber una letra o una cifra pegada, ni
    una cifra al otro lado de un separador decimal (`0.8` no casa en `0.80`, ni `1%` en `11%`)."""
    cuerpo = r"\s+".join(re.escape(p) for p in normalizar(termino).split())
    return re.compile(r"(?<![a-z0-9])(?<![0-9][.,:])" + cuerpo + r"(?![a-z0-9%])(?![.,:][0-9])")


PATRONES = tuple((t, patron(t)) for t in TERMINOS)


@dataclass(frozen=True)
class Segmento:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str


@dataclass(frozen=True)
class Pasaje:
    transcripcion: str
    t0_ms: int
    t1_ms: int
    terminos: dict[str, int]
    segmentos: tuple[Segmento, ...]


def coincidencias(
    segmentos: list[Segmento], patrones: tuple[tuple[str, re.Pattern[str]], ...] | None = None
) -> list[tuple[str, int, int]]:
    """`(termino, t0_ms, t1_ms)` de cada coincidencia, buscando sobre el texto de TODA la
    transcripcion unido con un espacio, para que una frase partida entre dos segmentos tambien
    case. El intervalo va del inicio del segmento donde empieza al final del segmento donde
    acaba. `patrones` son los de A-18 si no se pasan otros."""
    inicios: list[int] = []
    partes: list[str] = []
    pos = 0
    for s in segmentos:
        inicios.append(pos)
        norm = normalizar(s.texto)
        partes.append(norm)
        pos += len(norm) + 1
    texto = " ".join(partes)

    def indice(car: int) -> int:
        i = 0
        while i + 1 < len(inicios) and inicios[i + 1] <= car:
            i += 1
        return i

    salida: list[tuple[str, int, int]] = []
    for termino, pat in PATRONES if patrones is None else patrones:
        for m in pat.finditer(texto):
            a, b = indice(m.start()), indice(m.end() - 1)
            salida.append((termino, segmentos[a].t0_ms, segmentos[b].t1_ms))
    return salida


def pasajes(
    transcripcion: str,
    segmentos: list[Segmento],
    patrones: tuple[tuple[str, re.Pattern[str]], ...] | None = None,
    maximo_ms: int | None = None,
) -> list[Pasaje]:
    """Ventana de +-45 s alrededor de cada coincidencia; las que se solapan se unen en una. El
    pasaje trae todos los segmentos que tocan su ventana, sin recortar.

    Para A-18 (`patrones` y `maximo_ms` en None) el comportamiento es el de siempre. Con
    `maximo_ms`, una union mas larga se CORTA en pasajes consecutivos de como mucho `maximo_ms`
    desde su inicio; cada trozo lista SUS coincidencias -las que empiezan dentro de el- y trae los
    segmentos que lo tocan. Un trozo sin ninguna coincidencia propia no se emite."""
    usados = PATRONES if patrones is None else patrones
    orden_terminos = [t for t, _ in usados]
    ventanas = sorted(
        (max(0, t0 - VENTANA_MS), t1 + VENTANA_MS, termino, t0)
        for termino, t0, t1 in coincidencias(segmentos, usados)
    )
    unidas: list[tuple[int, int, list[tuple[str, int]]]] = []
    for a, b, termino, t0 in ventanas:
        if unidas and a <= unidas[-1][1]:
            ua, ub, lista = unidas[-1]
            lista.append((termino, t0))
            unidas[-1] = (ua, max(ub, b), lista)
        else:
            unidas.append((a, b, [(termino, t0)]))
    trozos: list[tuple[int, int, list[tuple[str, int]]]] = []
    for a, b, lista in unidas:
        if maximo_ms is None or b - a <= maximo_ms:
            trozos.append((a, b, lista))
            continue
        inicio = a
        while inicio < b:
            fin = min(inicio + maximo_ms, b)
            propias = [(tm, t0) for tm, t0 in lista if inicio <= t0 < fin or (fin == b and t0 == b)]
            if propias:
                trozos.append((inicio, fin, propias))
            inicio = fin
    salida = []
    for a, b, lista in trozos:
        dentro = tuple(s for s in segmentos if s.t1_ms >= a and s.t0_ms <= b)
        cuenta: dict[str, int] = {}
        for termino, _ in lista:
            cuenta[termino] = cuenta.get(termino, 0) + 1
        orden = {t: cuenta[t] for t in orden_terminos if t in cuenta}
        salida.append(Pasaje(transcripcion, a, b, orden, dentro))
    return salida


def leer_manifiesto(transcripcion: str) -> tuple[Path, str]:
    texto = (MANIFIESTOS / f"{transcripcion}.yaml").read_text(encoding="utf-8")
    carpeta = re.search(r"^carpeta: (.+)$", texto, re.M)
    sha = re.search(r"^sha256_cruda: ([0-9a-f]{64})$", texto, re.M)
    if carpeta is None or sha is None:
        raise IntegridadError(f"{transcripcion}: el manifiesto no fija carpeta y sha256_cruda")
    return DATOS / carpeta.group(1).strip() / "cruda.jsonl", sha.group(1)


def leer(transcripcion: str) -> tuple[list[Segmento], str]:
    """Solo una de la lista cerrada, y solo si sus bytes son los del manifiesto."""
    if transcripcion not in ALCANCE:
        raise IntegridadError(f"fuera de la lista cerrada: {transcripcion}")
    ruta, esperado = leer_manifiesto(transcripcion)
    datos = ruta.read_bytes()
    real = hashlib.sha256(datos).hexdigest()
    if real != esperado:
        raise IntegridadError(f"{transcripcion}: cruda.jsonl no es la que fija su manifiesto")
    filas = [json.loads(x) for x in datos.decode("utf-8").splitlines() if x.strip()]
    segmentos = [
        Segmento(int(f["n"]), int(f["t0_ms"]), int(f["t1_ms"]), str(f["texto"])) for f in filas
    ]
    return segmentos, real


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def formato(p: Pasaje, numero: int) -> list[str]:
    terminos = ", ".join(f"{t} x{n}" for t, n in p.terminos.items())
    lineas = [
        f"=== PASAJE {numero} | {p.transcripcion} | {hms(p.t0_ms)}-{hms(p.t1_ms)} | {terminos}",
    ]
    lineas += [f"[{hms(s.t0_ms)}-{hms(s.t1_ms)}] #{s.n} {s.texto.strip()}" for s in p.segmentos]
    return lineas


def buscar() -> list[str]:
    lineas: list[str] = []
    todos: list[Pasaje] = []
    for tr in ALCANCE:
        segmentos, sha = leer(tr)
        lineas.append(f"INTEGRIDAD {tr} cruda.jsonl sha256 {sha} = manifiesto: OK")
        todos += pasajes(tr, segmentos)
    for i, p in enumerate(todos, 1):
        lineas += formato(p, i)
    lineas.append("== PASAJES POR TRANSCRIPCION")
    for tr in ALCANCE:
        lineas.append(f"{tr}: {sum(1 for p in todos if p.transcripcion == tr)}")
    lineas.append(f"== TOTAL: {len(todos)}")
    return lineas


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: a18_buscar.py --salida <fichero>", file=sys.stderr)
        return 2
    Path(argv[1]).write_text("\n".join(buscar()) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
