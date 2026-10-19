"""El journal de la capa de MT5, formato v1: lector y validador (R6a.1, ADR-0082 D7).

El formato se define una sola vez, en `mql5/JOURNAL.md`; lo escribe
`mql5/Include/Botsito/Capa/Journal.mqh` y lo valida este modulo, que recalcula la cadena de hashes
sobre los mismos bytes:

- un objeto JSON por linea, UTF-8 sin BOM, fin de linea LF (nunca CR), y la ultima linea con su LF
  (sin el, la linea esta truncada);
- cada linea es la forma CANONICA de su objeto: las claves de `CLAVES` en ese orden, sin espacios, y
  sin escapar lo que no es ASCII (`canonica`);
- `h(n)` es el SHA-256 de los bytes de la linea `n` sin el LF, y la linea `n+1` lo lleva en `prev`;
  la primera linea de una cadena lleva `GENESIS`. Una cadena nueva en medio solo la abre un
  `arranque` con `cadena_anterior: rota`;
- `seq` empieza en 1 en cada cadena y sube de uno en uno, entre ficheros y reinicios;
- `desfase_s` es `srv - gmt` en segundos, y las claves reservadas valen `null` en v1;
- los `datos` de cada evento llevan exactamente las claves de `DATOS`: ni login ni dinero (D2f).

Uso, para validar uno o varios ficheros en orden como una sola cadena (por su ruta: la guardia de
Claude Code no ejecuta `python -m` de un modulo que no sea pytest):

    uv run python src/botsito/mql5bridge/journal.py <fichero> [<fichero>...]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

VERSION = 1
CLAVES = (
    "v",
    "seq",
    "srv",
    "gmt",
    "desfase_s",
    "ev",
    "datos",
    "regla",
    "condicion",
    "capa_hash",
    "spec_hash",
    "risk_hash",
    "ambiguas",
    "prev",
)
RESERVADAS = ("regla", "condicion", "capa_hash", "spec_hash", "risk_hash", "ambiguas")
GENESIS = "0" * 64
CADENA_ANTERIOR = ("ninguna", "sigue", "rota")
DIAS = ("SUNDAY", "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY")

# Las claves de `datos` de cada evento, con su tipo. `hora` es una hora ISO 8601 sin huso, `dia` una
# fecha, `semana` el objeto de las sesiones (un dia de `DIAS` -> lista de [desde_s, hasta_s]).
DATOS: dict[str, dict[str, str]] = {
    "arranque": {
        "version_ea": "texto",
        "build": "entero",
        "simbolo": "texto",
        "conectado": "logico",
        "cadena_anterior": "cadena_anterior",
    },
    "cuenta": {
        "trade_mode": "texto",
        "margin_mode": "texto",
        "servidor": "texto",
        "conectado": "logico",
    },
    "negativa": {"trade_mode": "texto", "motivo": "texto"},
    "reloj": {
        "time_current": "hora",
        "time_trade_server": "hora",
        "time_gmt": "hora",
        "time_local": "hora",
        "desfase_servidor_gmt_min": "entero",
        "desfase_local_gmt_min": "entero",
        "time_gmt_offset_seg": "entero",
        "horario_verano_local_seg": "entero",
    },
    "sesiones": {"trade": "semana", "quote": "semana", "tope_alcanzado": "logico"},
    "latido": {"conectado": "logico", "time_current": "hora"},
    "cambio_de_dia": {"dia_anterior": "dia", "dia_nuevo": "dia"},
    "fin": {"motivo": "entero", "motivo_texto": "texto"},
}

_HORA = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")
_DIA = re.compile(r"\d{4}-\d{2}-\d{2}")
_HEX64 = re.compile(r"[0-9a-f]{64}")
_BOM = b"\xef\xbb\xbf"


class JournalError(ValueError):
    """Un journal que no cumple el formato v1; el mensaje dice el fichero, la linea y el motivo."""


@dataclass(frozen=True)
class Linea:
    fichero: str
    numero: int
    objeto: dict[str, Any]
    hash: str


def canonica(objeto: dict[str, Any]) -> bytes:
    """Los bytes de la unica forma admitida de escribir un objeto (sin el LF)."""
    return json.dumps(objeto, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def hash_linea(linea: bytes) -> str:
    """`h(n)`: el SHA-256 de los bytes de la linea sin su LF, en hexadecimal en minusculas."""
    return hashlib.sha256(linea).hexdigest()


def _es_entero(x: object) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


def _hora(texto: object) -> datetime | None:
    if not isinstance(texto, str) or not _HORA.fullmatch(texto):
        return None
    try:
        return datetime.fromisoformat(texto)
    except ValueError:
        return None


def _comprobar_valor(tipo: str, valor: object) -> str | None:
    """None si `valor` es del `tipo`; si no, el motivo."""
    if tipo == "texto":
        return None if isinstance(valor, str) else "no es texto"
    if tipo == "entero":
        return None if _es_entero(valor) else "no es un entero"
    if tipo == "logico":
        return None if isinstance(valor, bool) else "no es true/false"
    if tipo == "hora":
        return None if _hora(valor) is not None else "no es una hora AAAA-MM-DDTHH:MM:SS"
    if tipo == "dia":
        if not isinstance(valor, str) or not _DIA.fullmatch(valor):
            return "no es una fecha AAAA-MM-DD"
        try:
            datetime.fromisoformat(valor)
        except ValueError:
            return "no es una fecha AAAA-MM-DD"
        return None
    if tipo == "cadena_anterior":
        return None if valor in CADENA_ANTERIOR else f"no es una de {CADENA_ANTERIOR}"
    if tipo == "semana":
        if not isinstance(valor, dict) or list(valor) != list(DIAS):
            return f"no lleva los siete dias en orden {DIAS}"
        for dia, sesiones in valor.items():
            if not isinstance(sesiones, list):
                return f"{dia} no es una lista"
            for s in sesiones:
                if not (isinstance(s, list) and len(s) == 2 and all(_es_entero(x) for x in s)):
                    return f"{dia}: cada sesion es [desde_s, hasta_s] en enteros"
        return None
    raise AssertionError(f"tipo desconocido: {tipo}")


def _comprobar_objeto(obj: object) -> str | None:
    """None si el objeto cumple el esquema v1 (sin mirar la cadena); si no, el motivo."""
    if not isinstance(obj, dict):
        return "la linea no es un objeto JSON"
    if tuple(obj) != CLAVES:
        return f"las claves no son las de v1 en su orden: {list(obj)}"
    if obj["v"] != VERSION or not _es_entero(obj["v"]):
        return f"version {obj['v']!r}: este lector es de la v{VERSION}"
    if not _es_entero(obj["seq"]) or obj["seq"] < 1:
        return f"seq {obj['seq']!r} no es un entero positivo"
    srv, gmt = _hora(obj["srv"]), _hora(obj["gmt"])
    if srv is None or gmt is None:
        return "srv y gmt son horas AAAA-MM-DDTHH:MM:SS"
    if not _es_entero(obj["desfase_s"]) or obj["desfase_s"] != int((srv - gmt).total_seconds()):
        return f"desfase_s {obj['desfase_s']!r} no es srv - gmt en segundos"
    for clave in RESERVADAS:
        if obj[clave] is not None:
            return f"{clave} esta reservada y vale null en v{VERSION}"
    if not isinstance(obj["prev"], str) or not _HEX64.fullmatch(obj["prev"]):
        return "prev no son 64 hexadecimales en minusculas"
    esquema = DATOS.get(obj["ev"]) if isinstance(obj["ev"], str) else None
    if esquema is None:
        return f"evento desconocido: {obj['ev']!r}"
    datos = obj["datos"]
    if not isinstance(datos, dict) or list(datos) != list(esquema):
        return f"los datos de {obj['ev']} no son {list(esquema)}"
    for clave, tipo in esquema.items():
        motivo = _comprobar_valor(tipo, datos[clave])
        if motivo is not None:
            return f"datos.{clave}: {motivo}"
    return None


def leer(ficheros: Sequence[tuple[str, bytes]]) -> list[Linea]:
    """Valida uno o varios ficheros, en orden, como una sola cadena. Lanza `JournalError`."""
    lineas: list[Linea] = []
    previa: Linea | None = None
    for nombre, contenido in ficheros:
        if contenido.startswith(_BOM):
            raise JournalError(f"{nombre}: empieza por BOM; el journal es UTF-8 sin BOM")
        if b"\r" in contenido:
            raise JournalError(f"{nombre}: lleva CR; el fin de linea es LF")
        if not contenido:
            raise JournalError(f"{nombre}: vacio")
        if not contenido.endswith(b"\n"):
            raise JournalError(f"{nombre}: la ultima linea no acaba en LF (truncada)")
        for numero, b in enumerate(contenido[:-1].split(b"\n"), start=1):
            donde = f"{nombre}:{numero}"
            try:
                obj = json.loads(b.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                raise JournalError(f"{donde}: no es JSON en UTF-8 ({e})") from None
            motivo = _comprobar_objeto(obj)
            if motivo is not None:
                raise JournalError(f"{donde}: {motivo}")
            if canonica(obj) != b:
                raise JournalError(f"{donde}: no esta en forma canonica")
            if obj["prev"] == GENESIS:
                nueva_por_rota = (
                    obj["ev"] == "arranque" and obj["datos"]["cadena_anterior"] == "rota"
                )
                if previa is not None and not nueva_por_rota:
                    raise JournalError(f"{donde}: cadena nueva sin un arranque con cadena rota")
                if obj["seq"] != 1:
                    raise JournalError(f"{donde}: una cadena empieza en seq 1, no en {obj['seq']}")
            else:
                if previa is None:
                    raise JournalError(f"{donde}: prev sin linea anterior (la primera lleva ceros)")
                if obj["prev"] != previa.hash:
                    raise JournalError(f"{donde}: prev no es el hash de la linea anterior")
                if obj["seq"] != previa.objeto["seq"] + 1:
                    raise JournalError(f"{donde}: seq {obj['seq']} tras {previa.objeto['seq']}")
            previa = Linea(nombre, numero, obj, hash_linea(b))
            lineas.append(previa)
    return lineas


def resumen(lineas: Sequence[Linea]) -> str:
    """Lo que dice el journal, para leerlo sin abrirlo: eventos, desfases, sesiones y cadenas."""
    eventos: dict[str, int] = {}
    desfases: dict[int, int] = {}
    for x in lineas:
        eventos[x.objeto["ev"]] = eventos.get(x.objeto["ev"], 0) + 1
        desfases[x.objeto["desfase_s"]] = desfases.get(x.objeto["desfase_s"], 0) + 1
    cadenas = sum(1 for x in lineas if x.objeto["prev"] == GENESIS)
    ficheros = len({x.fichero for x in lineas})
    salida = [
        f"{len(lineas)} lineas validas en {ficheros} ficheros, {cadenas} cadena(s)",
        f"desde {lineas[0].objeto['srv']} hasta {lineas[-1].objeto['srv']} (hora del servidor)",
        "eventos: " + ", ".join(f"{k} {v}" for k, v in sorted(eventos.items())),
        "desfase_s (srv - gmt): " + ", ".join(f"{k} x{v}" for k, v in sorted(desfases.items())),
        f"hash de la ultima linea: {lineas[-1].hash}",
    ]
    for x in lineas:
        if x.objeto["ev"] in ("cuenta", "negativa", "cambio_de_dia", "sesiones", "fin"):
            datos = json.dumps(x.objeto["datos"], ensure_ascii=False)
            salida.append(f"{x.fichero}:{x.numero} {x.objeto['ev']} {datos}")
    return "\n".join(salida)


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Valida el journal v1 de la capa de MT5 (mql5/JOURNAL.md)."
    )
    p.add_argument(
        "ficheros", nargs="+", type=Path, help="en orden; se validan como una sola cadena"
    )
    a = p.parse_args(argv)
    try:
        lineas = leer([(str(f), f.read_bytes()) for f in a.ficheros])
    except JournalError as e:
        print(f"NO VALIDO: {e}")
        return 1
    if not lineas:
        print("NO VALIDO: sin lineas")
        return 1
    print(resumen(lineas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
