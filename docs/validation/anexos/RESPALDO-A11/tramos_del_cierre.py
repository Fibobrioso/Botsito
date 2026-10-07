"""Respuesta del consultor del 2026-10-07 a la fase 0 de `trabajo/respaldo-a11`, punto 1: medir que
los instantes del registro que cierra A-11 (`fb-2026-09-09-sesion-01-69711f67`: v6, 1:43:51-1:44:36,
confirmado en 2:00:01) no caen en ningun tramo de `knowledge/corpus/tramos_no_citables.yaml`.

Solo lee el YAML de tramos (por el lector unico de `botsito.corpus.cuarentena`) y el del registro de
feedback; no abre ninguna transcripcion. Comprueba tambien que la grabacion del registro es v6
(`knowledge/corpus/fuentes.yaml`).

Uso: uv run python docs/validation/anexos/RESPALDO-A11/tramos_del_cierre.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

from botsito.corpus.cuarentena import cargar_tramos_no_citables

RAIZ = Path(__file__).resolve().parents[4]
REGISTRO = RAIZ / "knowledge/feedback/2026-09-09-sesion-01/fb-2026-09-09-sesion-01-69711f67.yaml"
# El instante de la confirmacion, de las `notas` del registro («Confirmado en 2:00:01»): un segundo.
CONFIRMACION = ("2:00:01", "2:00:02")


def ms(hms: str) -> int:
    h, m, s = (int(x) for x in hms.split(":"))
    return ((h * 60 + m) * 60 + s) * 1000


def hms(valor: int) -> str:
    s = valor // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> int:
    registro = yaml.safe_load(REGISTRO.read_text(encoding="utf-8"))
    fuentes = yaml.safe_load((RAIZ / "knowledge/corpus/fuentes.yaml").read_text(encoding="utf-8"))
    video = next(
        v["video_id"] for v in fuentes["videos"] if v.get("fichero") == registro["grabacion"]
    )
    print(f"registro: {registro['id']} ({registro['accion']} sobre {registro['objetivo']})")
    print(f"grabacion: {registro['grabacion']} -> {video}")
    assert "2:00:01" in registro["notas"], "la nota del registro ya no nombra 2:00:01"
    instantes = {
        "respuesta (t0-t1)": (str(registro["t0"]), str(registro["t1"])),
        "confirmacion (notas)": CONFIRMACION,
    }
    tramos = cargar_tramos_no_citables(RAIZ).get(video, ())
    print(f"tramos no citables de {video}: {len(tramos)}")
    for a, b, _ in tramos:
        print(f"  {hms(a)}-{hms(b)}")
    dentro = 0
    for nombre, (t0, t1) in instantes.items():
        a, b = ms(t0), ms(t1)
        pisa = [(x, y) for x, y, _ in tramos if a < y and b > x]
        dentro += len(pisa)
        donde = ", ".join(f"{hms(x)}-{hms(y)}" for x, y in pisa) or "ninguno"
        print(f"{nombre} {t0}-{t1}: tramos que pisa: {donde}")
    print("VEREDICTO: " + ("CAE EN UN TRAMO: PARA" if dentro else "ninguno cae en un tramo"))
    return 1 if dentro else 0


if __name__ == "__main__":
    raise SystemExit(main())
