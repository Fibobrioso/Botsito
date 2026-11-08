"""La regla «(antes del dia)» sobre los ficheros de esta carpeta (encargo de
trabajo/recorrida-construccion-2, «Lo que se puede mirar», y alcance 4 del revisor): en cada linea
que empieza por un dia (o por `trader | <dia>` / `bot | <dia>`), ninguna fecha ISO ni ningun
`nivel@minuto` anterior a ese dia; y en ningun sitio una fecha de un mes que no sea de construccion
(salvo las de la linea de la rentabilidad, que nombra la ventana pre-registrada de ADR-0092 §5, y la
del calendario de cierres, que nombra lo que cubre). Solo LEE; imprime recuentos y, si hay alguna,
el numero de linea y que falla, sin el contenido.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/antes_del_dia.py <fichero>...
"""

from __future__ import annotations

import re
import sys
from datetime import UTC, date, datetime
from pathlib import Path

ROTULO = "[DIAGNOSTICO"
CONSTRUCCION = {"2026-01", "2026-04", "2026-07", "2026-08"}
DIA_DE_LA_FILA = re.compile(r"^(?:(?:trader|bot) \| |  )?(\d{4}-\d{2}-\d{2})\b")
FECHA = re.compile(r"(?<!\d)(\d{4})-(\d{2})-(\d{2})(?!\d)")
MINUTO = re.compile(r"@(\d{8})\b")
PATRON = re.compile(r"^(?:T0|P\d|P\?) ")
# las dos lineas que nombran fechas fuera de la construccion por diseno, sin ser datos
EXENTAS = ("### Rentabilidad (ADR-0092", "calendario: cubre ")
# los dias en que trabajo la rama (los nombra el README al fechar lo que se corrio): no son datos
FECHAS_DE_TRABAJO = {date(2026, 11, 8), date(2026, 11, 9)}


def _cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def main(rutas: list[Path]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    total = 0
    for ruta in rutas:
        malas = []
        filas = 0
        for n, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            # un diff lleva «< » o «> » delante del rotulo; una fila de patrones, «<patron>: »
            ln = _cuerpo(linea.lstrip("<> "))
            if PATRON.match(ln) and ": " in ln:
                ln = ln.split(": ", 1)[1]
            if any(e in ln for e in EXENTAS):
                continue
            fechas = [date(int(a), int(m), int(d)) for a, m, d in FECHA.findall(ln)]
            for f in fechas:
                if f"{f:%Y-%m}" not in CONSTRUCCION and f not in FECHAS_DE_TRABAJO:
                    malas.append(f"{n}: fecha fuera de la construccion")
            m = DIA_DE_LA_FILA.match(ln)
            if not m:
                continue
            filas += 1
            dia = date.fromisoformat(m.group(1))
            if any(f < dia for f in fechas):
                malas.append(f"{n}: fecha anterior al dia de la fila")
            for minuto in MINUTO.findall(ln):
                if datetime.fromtimestamp(int(minuto) * 60, UTC).date() < dia:
                    malas.append(f"{n}: nivel@minuto anterior al dia de la fila")
        total += len(malas)
        print(f"{ruta.name}: {filas} filas con dia; {len(malas)} lineas con algo antes del dia o "
              "fuera de la construccion")  # fmt: skip
        for x in malas[:20]:
            print(f"  linea {x}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main([Path(a) for a in sys.argv[1:]]))
