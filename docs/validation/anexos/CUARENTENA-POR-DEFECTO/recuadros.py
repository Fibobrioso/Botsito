"""Pone el recuadro de correccion en los informes cerrados que nombran una salida de medicion.

Cuarta orden del consultor (2026-10-01), punto 3: «Si esas salidas viven en informes ya cerrados,
pon un recuadro de corrección; no edites el cuerpo». El recuadro va justo debajo del titulo y el
cuerpo queda intacto (CLAUDE.md, «Regimenes de cambio», `docs/validation/`). Las cuentas de lineas
ocultas son las de `citas_de_salidas.py` (definicion exacta). Idempotente: si ya lo tiene, no lo
vuelve a poner. Se ejecuto una vez, en la rama, fuera de `make check`.

    uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/recuadros.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
MARCA = "RECUADRO DE CORRECCIÓN (2026-10-01, rama `trabajo/cuarentena-por-defecto`)"
# salida -> (guion, lineas de segmentos ocultos hoy, informes que la nombran)
SALIDAS = {
    "A18-TRANSCRIPCIONES-SALIDA.txt": (
        "a18_buscar.py",
        27,
        (
            "A18-TRANSCRIPCIONES",
            "A18-TRANSCRIPCIONES-CRITERIO",
            "A18-TRANSCRIPCIONES-CLASIFICACION",
        ),
    ),
    "A24-A21-A26-A34-SALIDA.txt": (
        "buscar_ambiguedades.py",
        9,
        ("A24-A21-A26-A34-CRITERIO", "A24-A21-A26-A34-CLASIFICACION"),
    ),
    "A35-PIVOTE-FORMADO-SALIDA.txt": (
        "buscar_ambiguedades.py",
        9,
        ("A35-PIVOTE-FORMADO-CRITERIO", "A35-PIVOTE-FORMADO-CLASIFICACION"),
    ),
    "SESION-02-BUSQUEDA-SALIDA.txt": (
        "buscar_ambiguedades.py",
        11,
        ("SESION-02-BUSQUEDA-CRITERIO", "SESION-02-BUSQUEDA-CLASIFICACION"),
    ),
}


def recuadro(salida: str, guion: str, n: int) -> str:
    return (
        f"> **{MARCA}.** La salida congelada de esta medición, `{salida}`, trae {n} líneas de\n"
        "> segmentos que hoy se ocultan por defecto (sesión en cuarentena, tramo no citable o\n"
        "> material reservado o sin sortear: `botsito.corpus.cuarentena`). Desde esa rama,\n"
        f"> `scripts/{guion}` lee la cruda FILTRADA, así que volver a ejecutarlo "
        "ya no reproduce la\n"
        "> salida commiteada, y la guardia de Claude Code no deja leerla\n"
        "> (`.claude/hooks/ficheros_con_ocultos.txt`). El cuerpo de este informe "
        "no se toca: lo que\n"
        "> dice se hizo sobre la salida commiteada. Detalle y cuentas:\n"
        "> `docs/validation/CUARENTENA-POR-DEFECTO.md`.\n\n"
    )


def main() -> int:
    for salida, (guion, n, informes) in SALIDAS.items():
        for nombre in informes:
            ruta = RAIZ / "docs" / "validation" / f"{nombre}.md"
            texto = ruta.read_text(encoding="utf-8")
            if MARCA in texto:
                print(f"{ruta.name}: ya lo tiene")
                continue
            titulo, resto = texto.split("\n\n", 1)
            assert titulo.startswith("# ") and "\n" not in titulo, ruta.name
            nuevo = f"{titulo}\n\n{recuadro(salida, guion, n)}{resto}"
            ruta.write_text(nuevo, encoding="utf-8", newline="\n")
            print(f"{ruta.name}: recuadro puesto")
    return 0


if __name__ == "__main__":
    sys.exit(main())
