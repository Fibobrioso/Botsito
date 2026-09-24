"""Los fotogramas de A-35, CONGELADOS antes de abrir ninguno.

Documento: `docs/validation/A35-FOTOGRAMAS-CRITERIO.md` (2026-09-24, rama
`trabajo/a35-pivote-formado`). Este script es su implementacion exacta; cambiarlo despues de mirar
es cambiar el criterio.

Para cada pasaje, la ventana es la de su(s) segmento(s) en la transcripcion cruda, a 1 fps: el
fotograma de cada segundo de `t0` a `t1`, los dos incluidos. Cualquier otro nombre se rechaza ANTES
de leer un byte. Cada PNG se comprueba contra la extraccion de F05 (manifiesto commiteado -> sha del
indice -> sha del PNG) antes de decodificarlo, como en `scripts/v5_criterio.py`.

El script no lee el grafico: da, por fotograma, cuantos pixeles cambian respecto al anterior de la
misma ventana. Se abren a mano el primero de cada ventana y todos los que cambian (`> 0`); un
fotograma sin ningun pixel distinto del anterior tiene su mismo contenido.

  `uv run python scripts/a35_fotogramas.py --salida <fichero>`
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType

RAIZ = Path(__file__).resolve().parents[1]
DATOS = RAIZ / "data" / "fotogramas"
MANIFIESTOS = RAIZ / "knowledge" / "corpus" / "fotogramas"
EXTRACCION = {"v3": "fr-v3-982da728", "v4": "fr-v4-9ad0ebb8"}

# pasaje -> (video, segmentos, t0_s, t1_s, fotograma citado en la clasificacion), de la salida
# congelada `docs/validation/A35-PIVOTE-FORMADO-SALIDA.txt`
VENTANAS: dict[str, tuple[str, str, int, int, int]] = {
    "P4": ("v3", "#976", 4540, 4559, 4540),  # [1:15:40-1:15:59]
    "P5": ("v4", "#461-#462", 1681, 1694, 1681),  # [0:28:01-0:28:14]
    "P6": ("v4", "#597-#601", 2107, 2124, 2116),  # [0:35:07-0:35:24]
    "P8": ("v4", "#844-#849", 3044, 3056, 3048),  # [0:50:44-0:50:56]
    "P9": ("v4", "#942", 3486, 3509, 3486),  # [0:58:06-0:58:29]
}
MEDIR: dict[str, tuple[str, ...]] = {
    p: tuple(f"{s * 1000:09d}" for s in range(t0, t1 + 1))
    for p, (_, _, t0, t1, _) in VENTANAS.items()
}


class IntegridadError(RuntimeError):
    """Un fotograma fuera de la lista cerrada, o que no es el que extrajo F05."""


def _png() -> ModuleType:
    nombre = "decodificar_png"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def sha_esperados(video: str) -> dict[str, str]:
    """`fichero -> sha256` del indice de F05, despues de comprobar que el indice es el que fija el
    manifiesto commiteado (`sha256_index`)."""
    manifiesto = MANIFIESTOS / f"{EXTRACCION[video]}.yaml"
    m = re.search(r"^sha256_index: ([0-9a-f]{64})$", manifiesto.read_text(encoding="utf-8"), re.M)
    if m is None:
        raise IntegridadError(f"{manifiesto.name}: sin sha256_index")
    indice = DATOS / video / "png-1fps" / "index.jsonl"
    if hashlib.sha256(indice.read_bytes()).hexdigest() != m.group(1):
        raise IntegridadError(f"{video}: index.jsonl no es el que fija el manifiesto de F05")
    filas = [json.loads(x) for x in indice.read_text(encoding="utf-8").splitlines() if x.strip()]
    return {str(f["fichero"]): str(f["sha256"]) for f in filas}


def verificar(pasaje: str, nombres: tuple[str, ...]) -> list[str]:
    """Todos los nombres estan en la ventana de su pasaje y sus bytes son los que F05 extrajo. Nada
    se decodifica hasta que TODOS pasan. Devuelve el registro de la verificacion."""
    if pasaje not in MEDIR:
        raise IntegridadError(f"pasaje fuera de la lista cerrada: {pasaje}")
    fuera = [n for n in nombres if n not in MEDIR[pasaje]]
    if fuera:
        raise IntegridadError(f"fuera de la lista cerrada de {pasaje}: {fuera}")
    video = VENTANAS[pasaje][0]
    esperados = sha_esperados(video)
    registro: list[str] = []
    for n in nombres:
        real = hashlib.sha256((DATOS / video / "png-1fps" / f"{n}.png").read_bytes()).hexdigest()
        if esperados.get(f"{n}.png") != real:
            raise IntegridadError(f"{video}/{n}.png no es el fotograma que extrajo F05")
        registro.append(f"INTEGRIDAD {EXTRACCION[video]}/{int(n)} sha256 {real} = indice F05: OK")
    return registro


def distintos(a: bytes, b: bytes, canales: int) -> int:
    """Pixeles con algun canal distinto entre dos imagenes del mismo tamano."""
    if len(a) != len(b):
        raise ValueError("tamanos distintos")
    if a == b:
        return 0
    return sum(1 for i in range(0, len(a), canales) if a[i : i + canales] != b[i : i + canales])


def hms(s: int) -> str:
    return f"{s // 3600}:{s // 60 % 60:02d}:{s % 60:02d}"


def registrar() -> list[str]:
    lineas: list[str] = []
    for pasaje, nombres in MEDIR.items():
        video, segmentos, t0, t1, citado = VENTANAS[pasaje]
        lineas.append(
            f"=== {pasaje} | {video} {segmentos} | {hms(t0)}-{hms(t1)} | citado "
            f"{EXTRACCION[video]}/{citado * 1000}"
        )
        lineas += verificar(pasaje, nombres)
        anterior: bytes | None = None
        for n in nombres:
            img = _png().leer(DATOS / video / "png-1fps" / f"{n}.png")
            cambio = "-" if anterior is None else str(distintos(anterior, img.pixeles, img.canales))
            abrir = "ABRIR" if anterior is None or cambio != "0" else "igual al anterior"
            lineas.append(f"{EXTRACCION[video]}/{int(n)} {hms(int(n) // 1000)} {cambio} {abrir}")
            anterior = img.pixeles
    return lineas


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: a35_fotogramas.py --salida <fichero>", file=sys.stderr)
        return 2
    Path(argv[1]).write_text("\n".join(registrar()) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
