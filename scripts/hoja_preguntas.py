"""La hoja de una sesion SOLO DE PREGUNTAS, en Word, desde `knowledge/spec/ambiguedades.yaml`.

Es la hoja que Aleks lleva a la sesion 02 (`docs/runbooks/SESION-DE-PREGUNTAS.md`): arriba las
tres reglas de la sesion, y despues cada pregunta con su id pequeno, su texto tal como esta en el
campo `pregunta` y un recuadro para notas. El texto no se reescribe aqui: si una pregunta tiene
que cambiar, cambia en `ambiguedades.yaml` y la hoja se regenera.

El orden es el que fijo el consultor el 2026-09-25 (`ORDEN_SESION_02`): primero lo que bloquea el
motor, despues RN-005, la orden y la caja, la gestion y al final lo demas. Una ambiguedad que ya
no este ABIERTA ni DECIDIDA hace fallar la hoja: no se lleva al trader una pregunta cerrada.

No se versiona el .docx (`/*.docx` en `.gitignore`): se regenera, lo ultimo antes de imprimir.

Uso:
    uv run python scripts/hoja_preguntas.py [--salida hoja-sesion-02.docx]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, Ambiguedad, cargar_ambiguedades
from botsito.cases.hoja_docx import (
    GRIS,
    HojaError,
    caja,
    escribir_docx,
    parrafo,
    run,
    titulo,
)

RAIZ = Path(__file__).resolve().parents[1]
SALIDA = "hoja-sesion-02.docx"

ENCABEZADO = "Sesión 2 · preguntas pendientes"
REGLAS = (
    "Antes de empezar, pedirle permiso para grabar, y que su sí quede en la grabación.",
    "No enseñar ningún gráfico, de ningún día.",
    "Si empieza a comentar operaciones concretas de septiembre, reconducir la conversación.",
)

# (titulo del bloque, ids en orden). Decision del consultor, 2026-09-25.
ORDEN_SESION_02: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Lo primero", ("A-35", "A-21", "A-24")),
    ("La liquidez de M15", ("A-26", "A-25", "A-32")),
    ("La orden y el stop", ("A-36", "A-37", "A-29", "A-30", "A-38")),
    ("La gestión de la operación", ("A-18", "A-13", "A-31", "A-40", "A-33")),
    ("Para terminar", ("A-34", "A-41", "A-39")),
)
ESTADOS_QUE_SE_PREGUNTAN = ("ABIERTA", "DECIDIDA")


def ids_en_orden() -> list[str]:
    return [aid for _, ids in ORDEN_SESION_02 for aid in ids]


def preguntas(repo: Path) -> dict[str, Ambiguedad]:
    todas = {a.id: a for a in cargar_ambiguedades(repo / FICHERO_AMBIGUEDADES)}
    orden = ids_en_orden()
    if len(orden) != len(set(orden)):
        raise HojaError("una ambiguedad sale dos veces en el orden de la hoja")
    faltan = [aid for aid in orden if aid not in todas]
    if faltan:
        raise HojaError(f"no existen en {FICHERO_AMBIGUEDADES}: {', '.join(faltan)}")
    cerradas = [aid for aid in orden if todas[aid].estado not in ESTADOS_QUE_SE_PREGUNTAN]
    if cerradas:
        raise HojaError(
            f"ya no se preguntan (estan {todas[cerradas[0]].estado}): {', '.join(cerradas)}"
        )
    return {aid: todas[aid] for aid in orden}


def documento(repo: Path) -> str:
    amb = preguntas(repo)
    partes = [titulo(ENCABEZADO, 1)]
    partes += [parrafo(run(r)) for r in REGLAS]
    for bloque, ids in ORDEN_SESION_02:
        partes.append(titulo(bloque, 2))
        for aid in ids:
            partes.append(
                parrafo(run(aid, sz=16, color=GRIS), espacio_antes=200, espacio_despues=40)
            )
            partes.append(parrafo(run(" ".join(amb[aid].pregunta.split()))))
            partes.append(caja(lineas=4, etiqueta="Notas"))
    cuerpo = "".join(partes)
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f"<w:body>{cuerpo}"
        '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134" '
        'w:header="709" w:footer="709" w:gutter="0"/></w:sectPr></w:body></w:document>'
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--salida", default=str(RAIZ / SALIDA))
    args = ap.parse_args(argv)
    try:
        escribir_docx(Path(args.salida), documento(RAIZ))
    except HojaError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {args.salida}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
