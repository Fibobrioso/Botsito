"""SELLO-RESPALDO-M1, fase 0 b): las cancelaciones que el bot pide en el cierre de una M1 sin ticks.

Reconstruye el recuento de `censo_cierre.py` de RESPALDO-M1 (§0.l, :351), que no esta en el repo,
desde su descripcion: «de las ordenes canceladas, ... se cancelaron en el cierre de una M1 sin
ticks (las 22, en horas perdidas)». Solo LEE la salida del arnes que recibe por argumento (ya
commiteada; no corre el motor, no lee velas ni manifiestos) y no imprime precios ni R.

Una cancelacion del bot (tabla «### Ordenes», resultado `cancelada`) se pide en el cierre de la M1
k menos 1 ms: su instante acaba en `:59.999`, y la M1 k es la que empieza un minuto antes de
`instante + 1 ms`. Las cancelaciones de una ventana de cierre de mercado (ADR-0068) van en un
instante redondo y se cuentan aparte. «Sin ticks» se lee aqui por la HORA, como `censo_respaldo.donde`
de RESPALDO-M1: una de las 18 horas perdidas de `horas_perdidas.py` o una hora fuera de las que
bajan los manifiestos. El guion del prototipo (`prototipo_sello.py`) lo comprueba minuto a minuto
contra el mercado del dia.

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/censo_cierre.py <salida del arnes>
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from horas_perdidas import HORAS_PERDIDAS  # noqa: E402  (copia identica de la de RESPALDO-M1)

MS_MIN = 60_000
ROTULO = "[DIAGNOSTICO"
HORAS_DE_TICKS = {"2026-01": range(6, 15)}  # el resto de meses de construccion: 05-13 UTC
HORAS_DE_TICKS_RESTO = range(5, 14)


def sin_rotulo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def ms_de(iso: str) -> int:
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


def hora(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).strftime("%H:%M:%S.%f")[:-3] + "Z"


def donde(dia: str, inicio_ms: int) -> str:
    h = datetime.fromtimestamp(inicio_ms / 1000, UTC).hour
    if f"{dia}T{h:02d}Z" in HORAS_PERDIDAS:
        return "hora perdida"
    if h not in HORAS_DE_TICKS.get(dia[:7], HORAS_DE_TICKS_RESTO):
        return "borde de la cobertura de ticks"
    return "con ticks"


def main(ruta: Path) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    seccion = ""
    clases: Counter[str] = Counter()
    filas: list[str] = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        ln = sin_rotulo(linea)
        if ln.startswith("### "):
            seccion = ln
            continue
        if not seccion.startswith("### Ordenes (") or not ln.startswith("20"):
            continue
        p = ln.split(" | ")
        dia, sesion, id_, colocada, resultado, instante = p[0], p[1], p[2], p[3], p[5], p[7]
        if resultado != "cancelada":
            continue
        ms = ms_de(instante)
        if (ms + 1) % MS_MIN != 0:
            clases["cancelada en un instante redondo (ventana de cierre, ADR-0068)"] += 1
            continue
        inicio_k = ms + 1 - MS_MIN  # la M1 k, en cuyo cierre (menos 1 ms) se cancela
        lugar = donde(dia, inicio_k)
        clases[f"cancelada en el cierre de una M1 · {lugar}"] += 1
        if lugar != "con ticks":
            filas.append(
                f"  {dia} | {sesion} | {id_} | colocada {hora(ms_de(colocada))} | "
                f"cancelada {hora(ms)} | M1 k {hora(inicio_k)[:5]}Z | {lugar}"
            )
    # SOLO la lista de los eventos: ningun recuento nuevo sobre la construccion (regla del
    # consultor para esta rama); el numero de filas es el recuento que el encargo pide rehacer
    del clases
    print(
        f"# {ruta.parent.name}/{ruta.name}: cancelaciones del bot en el cierre de una M1 sin ticks"
    )
    print(f"## filas: {len(filas)}")
    print("  dia | sesion | orden | colocada UTC | cancelada UTC | M1 k | donde")
    print("\n".join(filas))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    sys.exit(main(Path(sys.argv[1])))
