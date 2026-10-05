"""La sección del hueco (segunda respuesta del consultor, punto 3), SIN TEXTO: cada tramo no
citable de v7-v10, con su clase (por el comienzo de su motivo), el commit y la fecha en que entro
(el primer commit de `knowledge/corpus/tramos_no_citables.yaml` en que aparece, por video, t0 y t1)
y las lineas visibles cuya marca cae dentro, en la filtrada A (la instalada) y en la B (apartada),
con el criterio de `medir_fase1.py` (t0 <= marca < t1).

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/hueco.py
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import yaml

from botsito.corpus.transcripcion import parse_ms

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
FICHERO = "knowledge/corpus/tramos_no_citables.yaml"
SESIONES = {
    "v7": (E / "sesion-02-v7-audio", "sesion-02-v7"),
    "v8": (E / "sesion-02-v8-audio", "sesion-02-v8"),
    "v9": (E / "sesion-03-audio", "sesion-03"),
    "v10": (E / "sesion-04-audio", "sesion-04"),
}
_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")


def clase(motivo: str) -> str:
    m = " ".join(motivo.split()).lower()
    for prefijo, nombre in (
        ("cuarentena mecanica", "cuarentena mecanica"),
        ("completa el tramo", "completa (margen)"),
        ("precaucion", "precaucion"),
        ("precaución", "precaucion"),
    ):
        if m.startswith(prefijo):
            return nombre
    return "otra: " + " ".join(m.split()[:4])


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=RAIZ, capture_output=True, text=True, encoding="utf-8", check=True
    ).stdout


def entradas() -> dict[tuple[str, int, int], str]:
    """(video, t0_ms, t1_ms) -> «commit fecha» del primer commit en que aparece."""
    salida: dict[tuple[str, int, int], str] = {}
    log = _git("log", "--reverse", "--format=%h %ad", "--date=short", "--", FICHERO)
    for linea in log.splitlines():
        commit, fecha = linea.split()
        doc = yaml.safe_load(_git("show", f"{commit}:{FICHERO}"))
        for t in doc["tramos"]:
            clave = (str(t["video_id"]), parse_ms(str(t["t0"])), parse_ms(str(t["t1"])))
            salida.setdefault(clave, f"{commit} {fecha}")
    return salida


def marcas_visibles(ruta: Path) -> list[int]:
    return [
        (int(m.group(1)) * 60 + int(m.group(2))) * 1000
        for linea in ruta.read_text(encoding="utf-8").splitlines()
        if (m := _MARCA.match(linea))
    ]


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    doc = yaml.safe_load((RAIZ / FICHERO).read_text(encoding="utf-8"))
    entrada = entradas()
    print(
        "| video | tramo | clase | entro | lineas en A | lineas en B | marcas en B "
        "(«ultimo s» = en el ultimo segundo del tramo) |"
    )
    print("|---|---|---|---|---|---|---|")
    total = 0
    for v, (carpeta, base) in SESIONES.items():
        marcas_a = marcas_visibles(carpeta / f"{base}.filtrada.md")
        marcas_b = marcas_visibles(carpeta / f"{base}.filtrada-B-condicion.md")
        tramos = sorted(
            (parse_ms(str(t["t0"])), parse_ms(str(t["t1"])), str(t["motivo"]))
            for t in doc["tramos"]
            if t["video_id"] == v
        )
        for x, y, motivo in tramos:
            total += 1
            na = sum(1 for t in marcas_a if x <= t < y)
            nb = sum(1 for t in marcas_b if x <= t < y)
            quien = entrada.get((v, x, y), "esta rama")
            dentro = [t for t in marcas_b if x <= t < y]
            if not dentro:
                detalle = "-"
            elif len(dentro) <= 3:
                detalle = ", ".join(
                    hms(t) + (" (ultimo s)" if t >= y - 1000 else "") for t in dentro
                )
            else:
                detalle = f"{len(dentro)} de {hms(dentro[0])} a {hms(dentro[-1])}"
            print(
                f"| {v} | {hms(x)}-{hms(y)} | {clase(motivo)} | {quien} | {na} | {nb} | {detalle} |"
            )
    print(f"tramos de v7-v10: {total}")


if __name__ == "__main__":
    main()
