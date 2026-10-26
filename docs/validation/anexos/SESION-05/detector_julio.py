"""Decision (4) del consultor (trabajo/sesion-05, respuesta a): antes de LEER una filtrada, localiza
las lineas que pueden nombrar un dia de julio, imprimiendo SOLO su marca de tiempo, el tipo de
coincidencia y un booleano «algun numero de dia entre 18 y 31». NUNCA el texto ni el numero.

Uso: python detector_julio.py <filtrada.md>

Tipos:
  julio+num   la linea nombra julio y un entero suelto de 1 a 31
  dia+num     la linea dice «dia/dias» seguido (o precedido) de un entero de 1 a 31
  vecino      entero suelto de 18 a 31 en una linea contigua a una que nombra julio
Las lineas [CUARENTENA ...] no tienen texto y no cuentan.
"""

import re
import sys
from pathlib import Path

from botsito.corpus.cuarentena import normalizar, numeros_a_cifras

LINEA = re.compile(r"^\[(\d+:\d\d)\] (.*)$")
NUM = re.compile(r"(?<![\d.,])(\d{1,2})(?![\d]|[.,]\d)")
JULIO = re.compile(r"\b(julio|july|jul)\b")
DIA_NUM = re.compile(
    r"\bdias?\b\W+(?:\w+\W+)?(\d{1,2})(?!\d)|(?<!\d)(\d{1,2})\W+(?:\w+\W+)?dias?\b"
)


def enteros(t: str) -> list[int]:
    return [int(m.group(1)) for m in NUM.finditer(t) if 1 <= int(m.group(1)) <= 31]


def main() -> int:
    ruta = Path(sys.argv[1])
    lineas: list[tuple[str, str]] = []
    for crudo in ruta.read_text(encoding="utf-8").splitlines():
        m = LINEA.match(crudo)
        if m:
            lineas.append((m.group(1), numeros_a_cifras(normalizar(m.group(2)))))
    con_julio = {i for i, (_, t) in enumerate(lineas) if JULIO.search(t)}
    hallazgos: list[tuple[str, str, bool]] = []
    for i, (marca, t) in enumerate(lineas):
        nums = enteros(t)
        if i in con_julio and nums:
            hallazgos.append((marca, "julio+num", any(n >= 18 for n in nums)))
        dias = [int(g) for m in DIA_NUM.finditer(t) for g in m.groups() if g]
        dias = [d for d in dias if 1 <= d <= 31]
        if dias:
            hallazgos.append((marca, "dia+num", any(d >= 18 for d in dias)))
        if i not in con_julio and ({i - 1, i + 1} & con_julio) and any(n >= 18 for n in nums):
            hallazgos.append((marca, "vecino", True))
    print(f"lineas con texto: {len(lineas)}; lineas que nombran julio: {len(con_julio)}")
    print(f"coincidencias: {len(hallazgos)}; con algun 18-31: {sum(h[2] for h in hallazgos)}")
    for marca, tipo, alto in hallazgos:
        print(f"  [{marca}] {tipo} 18-31={'SI' if alto else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
