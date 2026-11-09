"""F4 de trabajo/video-julio: las 81 filas de julio «sin clase hasta T» de RECORRIDA-CONSTRUCCION-2.md §8.

Lee SOLO dos salidas ya commiteadas de `docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/`:
- `patrones-cuenta-por-mes.txt` (bloque `-- filas`): patron, quien, dia, sesion, lado, instante UTC,
  entrada, y el bot (o trader) mas cercano con Δentrada y Δinstante, el primer hecho y los frenos;
- `para-clasificar.txt` (tabla «Operaciones del trader»): la orden de la corrida 1, el primer hecho
  que falta con sus frenos y la hora perdida, unidas por (dia, sesion, lado, instante UTC).

Las 81: P1 (20), P2 con |Δentrada| > 10 puntos (7), P3 (15), P5 (37) y P6 (2), todas de 2026-07.
Las filas P5 y P6 son ordenes del bot: para-clasificar no les da primer hecho ni frenos
(respuesta del consultor a la fase 0, punto 3). Sale con codigo 1 si no son 81.

Imprime agrupado por (dia, sesion) y, en cada fila, la hora de Madrid (UTC+2 en julio, ADR-0069)
para buscarla en el video. Ninguna cifra de resultados del bot.

Uso (la raiz del repositorio y el fichero de salida, por argumento: CLAUDE.md, «Ensayos aislados»):
  uv run python docs/validation/anexos/VIDEO-JULIO/filas_hasta_t.py <raiz> <salida>
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit("uso: filas_hasta_t.py <raiz del repositorio> <fichero de salida>")
RAIZ = Path(sys.argv[1]).resolve()
SALIDA = Path(sys.argv[2]).resolve()
ANEXO = RAIZ / "docs" / "validation" / "anexos" / "RECORRIDA-CONSTRUCCION-2"
ESPERADAS = {"P1": 20, "P2": 7, "P3": 15, "P5": 37, "P6": 2}
RE_FILA = re.compile(r"^(P\d) ([^\[]+?) \[([^\]]*)\](?: \[([^\]]*)\])?: (trader|bot) \| (.+)$")
RE_DELTA = re.compile(r"Δentrada ([+-]?\d+) puntos")


def madrid(iso_utc: str) -> str:
    t = datetime.fromisoformat(iso_utc) + timedelta(hours=2)
    return t.strftime("%H:%M:%S")


def filas_patrones() -> list[dict[str, str]]:
    salida = []
    dentro = False
    for linea in (ANEXO / "patrones-cuenta-por-mes.txt").read_text(encoding="utf-8").splitlines():
        if linea.startswith("-- filas"):
            dentro = True
            continue
        if not dentro:
            continue
        m = RE_FILA.match(linea)
        if not m:
            continue
        patron, nombre, subtipo, marca, quien, resto = m.groups()
        campos = resto.split(" | ")
        dia, sesion, lado, instante, entrada = campos[:5]
        if not dia.startswith("2026-07"):
            continue
        detalle = " | ".join(campos[5:])
        if patron == "P2":
            d = RE_DELTA.search(detalle)
            if d is None or abs(int(d.group(1))) <= 10:
                continue
        if patron not in ESPERADAS:
            continue
        salida.append(
            {
                "patron": patron,
                "nombre": nombre,
                "subtipo": subtipo,
                "marca": marca or "",
                "quien": quien,
                "dia": dia,
                "sesion": sesion,
                "lado": lado,
                "instante": instante,
                "entrada": entrada,
                "detalle": detalle,
            }
        )
    return salida


def trader_para_clasificar() -> dict[tuple[str, str, str, str], dict[str, str]]:
    tabla: dict[tuple[str, str, str, str], dict[str, str]] = {}
    dentro = False
    for linea in (ANEXO / "para-clasificar.txt").read_text(encoding="utf-8").splitlines():
        if linea.startswith("## Operaciones del trader"):
            dentro = True
            continue
        if dentro and linea.startswith("## "):
            break
        if not dentro or not linea.startswith("2026-07"):
            continue
        c = linea.split(" | ")
        tabla[(c[0], c[1], c[2], c[3])] = {
            "orden": c[6],
            "primer_hecho": c[8],
            "hora_perdida": c[12],
        }
    return tabla


def main() -> int:
    filas = filas_patrones()
    pc = trader_para_clasificar()
    cuenta = Counter(f["patron"] for f in filas)
    lineas: list[str] = []
    print = lineas.append  # noqa: A001 - se escribe a fichero, en UTF-8 y con \n
    print("# F4 · las filas de julio sin clase hasta T (RECORRIDA-CONSTRUCCION-2.md §8)")
    print(f"# por patron: {dict(sorted(cuenta.items()))}; total {len(filas)}")
    sesiones = defaultdict(list)
    for f in filas:
        sesiones[(f["dia"], f["sesion"])].append(f)
    print(f"# sesiones (dia, sesion): {len(sesiones)}; dias: {len({d for d, _ in sesiones})}")
    for (dia, sesion), grupo in sorted(sesiones.items()):
        print(f"\n## {dia} {sesion} ({len(grupo)} filas)")
        for f in sorted(grupo, key=lambda x: x["instante"]):
            marca = f" [{f['marca']}]" if f["marca"] else ""
            linea = (
                f"{f['patron']} [{f['subtipo']}]{marca} {f['quien']} {f['lado']} "
                f"{madrid(f['instante'])} Madrid ({f['instante']}) entrada {f['entrada']}: "
                f"{f['detalle']}"
            )
            if f["quien"] == "trader":
                extra = pc.get((f["dia"], f["sesion"], f["lado"], f["instante"]))
                if extra is None:
                    sys.stdout.write("ERROR: fila del trader sin su fila en para-clasificar\n")
                    return 1
                linea += (
                    f" || para-clasificar: orden {extra['orden']}; primer hecho que falta: "
                    f"{extra['primer_hecho']}; hora perdida: {extra['hora_perdida']}"
                )
            else:
                linea += " || para-clasificar: orden del bot, sin primer hecho ni frenos"
            print(f"- {linea}")
    SALIDA.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    if dict(cuenta) != ESPERADAS:
        sys.stdout.write(f"ERROR: no son las de 8: {dict(cuenta)} frente a {ESPERADAS}\n")
        return 1
    sys.stdout.write(f"OK: {len(filas)} filas en {len(sesiones)} sesiones -> {SALIDA.name}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
