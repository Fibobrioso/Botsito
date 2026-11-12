"""Genera el golden del journal v2 (trabajo/capa-generada, fase 1) a partir del golden v1
(tests/golden/journal/): los mismos casos, linea a linea, con `v` 2 y `capa_hash` igual al hash FIJO
de prueba, y la cadena recalculada (seq y prev). El hash fijo es a proposito: asi el golden no
depende de lo generado (respuesta del consultor a la PARADA, punto 6), y el script de pruebas de
MQL5 (mql5/Scripts/BotsitoPruebasCapa.mq5) lo escribe con el mismo valor.

Uso (las dos carpetas, por argumento: el golden v1 y la salida; nada sale de __file__), desde la
raiz del repositorio:

    uv run python docs/validation/anexos/CAPA-GENERADA/fase1/generar_golden_v2.py A B

Escribe <salida>/continua/... y <salida>/rota/... con los mismos nombres que el v1.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from botsito.mql5bridge.journal import CLAVES, GENESIS, canonica, hash_linea, leer

CAPA_HASH_PRUEBA = "0123456789abcdef" * 4


def main(origen: Path, salida: Path) -> None:
    for cadena in sorted({p.parent for p in origen.rglob("*.jsonl")}):
        nombres = sorted(p.name for p in cadena.glob("*.jsonl"))
        leer([(n, (cadena / n).read_bytes()) for n in nombres])  # el v1 de partida valida
        prev, seq = GENESIS, 0
        destino = salida / cadena.relative_to(origen)
        destino.mkdir(parents=True, exist_ok=True)
        escritos = []
        for n in nombres:
            lineas = []
            for b in (cadena / n).read_bytes()[:-1].split(b"\n"):
                o = json.loads(b)
                if o["prev"] == GENESIS:
                    prev, seq = GENESIS, 0
                seq += 1
                o = {**o, "v": 2, "seq": seq, "capa_hash": CAPA_HASH_PRUEBA, "prev": prev}
                linea = canonica({k: o[k] for k in CLAVES})
                prev = hash_linea(linea)
                lineas.append(linea)
            contenido = b"".join(x + b"\n" for x in lineas)
            (destino / n).write_bytes(contenido)
            escritos.append((n, contenido))
        leer(escritos)
        print(f"{destino}: {len(escritos)} ficheros, hash final {prev}")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
