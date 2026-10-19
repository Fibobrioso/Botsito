"""PUNTO-USADO (R3.4), fase 1: cuantas ordenes de una salida del arnes se colocan en el PUNTO EXACTO
(la clave `nivel@inicio` de la vela contraria, que «### Ordenes» lleva al final desde esta rama) de
una orden ya LLENADA de su misma sesion, separando las de la MISMA caja (el mismo 1) y las de OTRA;
y cuantas se colocan en el punto de una orden ya RECHAZADA de su sesion (al colocar o al llenar).

Es el recuento de `anexos/VISOR-CONSTRUCCION/reentradas.py` hecho por el punto y no por el precio:
alli era una cota superior (un pivote nuevo al mismo nivel tambien contaba); aqui el punto lleva el
instante de la vela contraria, asi que dos puntos distintos al mismo nivel no se confunden. «La
misma caja» es el mismo 1 (`caja 1`, la ultima columna): el stop no sirve, porque el redondeo de
`stop_fraccion_redondeo` iguala dos 1 que difieren en un punto (PUNTO-USADO.md §1.d).

Lee SOLO «### Ordenes» de la salida que recibe por argumento, no escribe nada, y no imprime las dos
columnas en USD. Las filas son de dias dev de construccion.

    uv run python docs/validation/anexos/PUNTO-USADO/reentradas_por_punto.py <salida> [--filas]
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

CABECERA = "### Ordenes (dia"
FIN = "### "
COLUMNAS = 17  # las 15 de MARGEN-LOTE mas `punto` y `caja 1` (esta rama)
# posiciones en la fila
DIA, SESION, ID, COLOCADA, PRECIO, RESULTADO, _MOTIVO, CUANDO = range(8)
PUNTO, CAJA_1 = 15, 16
LLENADA, RECHAZADA = "llenada", "rechazada"
SIN = "-"


def _sin_etiquetas(linea: str) -> str:
    texto = linea
    while texto.startswith("["):
        texto = texto.split("] ", 1)[-1]
    return texto


def filas(ruta: Path) -> list[list[str]]:
    dentro = False
    salida: list[list[str]] = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        texto = _sin_etiquetas(linea)
        if texto.startswith(CABECERA):
            if " | punto | caja 1)" not in texto:
                raise SystemExit("la salida no lleva las columnas `punto` y `caja 1` (esta rama)")
            dentro = True
            continue
        if dentro and texto.startswith(FIN):
            break
        if dentro and texto.count(" | ") >= COLUMNAS - 1:
            salida.append([c.strip() for c in texto.split(" | ")])
    return salida


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if not argv or len(argv) > 2:
        print(__doc__)
        return 2
    ruta = Path(argv[0])
    con_filas = len(argv) == 2 and argv[1] == "--filas"
    por_sesion: dict[tuple[str, str], list[list[str]]] = defaultdict(list)
    sin_punto = 0
    for f in filas(ruta):
        if f[PUNTO] == SIN:
            sin_punto += 1
            continue
        por_sesion[(f[DIA], f[SESION])].append(f)
    tras_llenada = {"misma caja": 0, "otra caja": 0}
    llenadas_tras_llenada = {"misma caja": 0, "otra caja": 0}
    tras_rechazo = 0
    sesiones_llenada: set[tuple[str, str]] = set()
    sesiones_rechazo: set[tuple[str, str]] = set()
    if con_filas:
        print(
            "dia | sesion | orden | colocada UTC | punto | caja 1 | resultado | tras | la orden "
            "anterior en ese punto (su resultado, su caja 1, su instante)"
        )
    for clave, ordenes in sorted(por_sesion.items()):
        ordenes.sort(key=lambda f: (f[COLOCADA], f[ID]))
        llenada_en: dict[str, list[str]] = {}  # punto -> la ULTIMA fila llenada en ese punto
        rechazada_en: dict[str, list[str]] = {}
        for f in ordenes:
            punto = f[PUNTO]
            previa_llenada = llenada_en.get(punto)
            previa_rechazada = rechazada_en.get(punto)
            if previa_llenada is not None and f[COLOCADA] > previa_llenada[CUANDO]:
                cual = "misma caja" if f[CAJA_1] == previa_llenada[CAJA_1] else "otra caja"
                tras_llenada[cual] += 1
                llenadas_tras_llenada[cual] += f[RESULTADO] == LLENADA
                sesiones_llenada.add(clave)
                if con_filas:
                    print(
                        f"{f[DIA]} | {f[SESION]} | {f[ID]} | {f[COLOCADA]} | {punto} | {f[CAJA_1]}"
                        f" | {f[RESULTADO]} | llenada, {cual} | {previa_llenada[ID]} "
                        f"({previa_llenada[RESULTADO]}, {previa_llenada[CAJA_1]}, "
                        f"{previa_llenada[CUANDO]})"
                    )
            if previa_rechazada is not None and f[COLOCADA] > previa_rechazada[CUANDO]:
                tras_rechazo += 1
                sesiones_rechazo.add(clave)
                if con_filas:
                    print(
                        f"{f[DIA]} | {f[SESION]} | {f[ID]} | {f[COLOCADA]} | {punto} | {f[CAJA_1]}"
                        f" | {f[RESULTADO]} | rechazo | {previa_rechazada[ID]} "
                        f"({previa_rechazada[RESULTADO]}, {previa_rechazada[CAJA_1]}, "
                        f"{previa_rechazada[CUANDO]})"
                    )
            if f[RESULTADO] == LLENADA:
                llenada_en[punto] = f
            elif f[RESULTADO] == RECHAZADA:
                rechazada_en[punto] = f
    total = sum(tras_llenada.values())
    print(
        f"ordenes colocadas en el punto exacto de una orden ya llenada de su sesion: {total}, en "
        f"{len(sesiones_llenada)} sesiones; con la misma caja: {tras_llenada['misma caja']} "
        f"(llenadas {llenadas_tras_llenada['misma caja']}); con otra caja: "
        f"{tras_llenada['otra caja']} (llenadas {llenadas_tras_llenada['otra caja']})"
    )
    print(
        f"ordenes colocadas en el punto exacto de una orden ya rechazada de su sesion: "
        f"{tras_rechazo}, en {len(sesiones_rechazo)} sesiones"
    )
    print(f"filas sin punto (zona sin productor): {sin_punto}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
