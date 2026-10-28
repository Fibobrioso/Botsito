"""El barrido ancho de dias, ANTES de leer o releer una filtrada (rama
`trabajo/cuarentena-por-condicion-2`; regla del consultor del 2026-10-25,
docs/validation/SESION-05-EXTRACCION.md §2.7, punto 3; skill `ingerir-sesion`).

Toda linea `[mm:ss] texto` de la filtrada con un entero suelto dentro del rango de dias (por
defecto 18 a 31) se imprime con su marca de tiempo y esos numeros sustituidos por [N]: un numero
DEL RANGO no se imprime nunca. El resto de la linea sale tal cual, normalizada, con los demas
numeros (un mes en cifras, un dia por debajo de `--desde`) a la vista: por eso el rango tiene que
cubrir todos los dias que no son de construccion del mes que se barre. Antes de buscar, la linea
pasa por `normalizar` y `numeros_a_cifras` de `botsito.corpus.cuarentena`, asi que el dia escrito
en letra («el veinticinco») sale igual que en digitos. Sucesor de
`docs/validation/anexos/SESION-05/barrido_18_31.py`, que solo veia digitos
(SESION-05-EXTRACCION.md §11, a7).

Un entero suelto: no pegado a una letra (el codigo S25 no es un dia; como en `barrido_18_31.py`)
ni a otro digito, y con el MISMO borde que la regla de fecha (`cuarentena._ANTES` y
`cuarentena._DESPUES`, importados, no copiados): una coma o un punto forman parte de un numero solo
cuando tienen un digito a cada lado. Por eso «1,25» no es un dia y «hoy, 25,» si.

Uso:
    uv run python scripts/barrido_dias.py <filtrada.md> [--desde 18] [--hasta 31]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# `_ANTES` y `_DESPUES` son el borde de la regla de fecha: se importan para que la condicion viva en
# un solo sitio (revisor de `trabajo/cuarentena-por-condicion-2`, A2).
from botsito.corpus.cuarentena import _ANTES, _DESPUES, normalizar, numeros_a_cifras

LINEA = re.compile(r"^\[(\d+:\d\d)\] (.*)$")
ENTERO = re.compile(rf"(?<!\w){_ANTES}(\d{{1,2}}){_DESPUES}")
DESDE = 18
HASTA = 31


def barrer(texto: str, desde: int = DESDE, hasta: int = HASTA) -> list[str]:
    """Las lineas con un entero suelto en [desde, hasta], con esos numeros cambiados por [N]."""
    salida: list[str] = []
    for crudo in texto.splitlines():
        m = LINEA.match(crudo)
        if m is None:
            continue
        linea = numeros_a_cifras(normalizar(m.group(2)))
        if not any(desde <= int(x.group(1)) <= hasta for x in ENTERO.finditer(linea)):
            continue
        mascara = ENTERO.sub(
            lambda x: "[N]" if desde <= int(x.group(1)) <= hasta else x.group(0), linea
        )
        salida.append(f"[{m.group(1)}] {mascara}")
    return salida


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("filtrada", type=Path)
    ap.add_argument("--desde", type=int, default=DESDE)
    ap.add_argument("--hasta", type=int, default=HASTA)
    args = ap.parse_args(argv)
    lineas = barrer(args.filtrada.read_text(encoding="utf-8"), args.desde, args.hasta)
    for ln in lineas:
        print(ln)
    print(f"lineas con un entero suelto de {args.desde} a {args.hasta}: {len(lineas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
