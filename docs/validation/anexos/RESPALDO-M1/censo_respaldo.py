"""RESPALDO-M1 (respuesta del consultor a la PARADA, punto 5): el censo de los eventos del respaldo
M1 de una o varias salidas del arnes, y el criterio de hecho de la rama: CERO eventos evaluados con
una vela que empieza antes del instante en que se decidio lo evaluado.

Solo LEE las salidas que recibe por argumento. No corre el motor, no lee ningun manifiesto ni
ninguna vela, y no imprime precios ni R: tipos, instantes del dia dev e ids.

Por cada evento del respaldo (`### Eventos del broker`, fuente `respaldo_m1`), su vela es la que
CIERRA en el instante del evento (ADR-0051 §5): empieza en `((ms - 1) // 60000) * 60000`. Lo que
evalua y cuando se decidio:
- `llenada` o `rechazada` de una orden: la orden, decidida al colocarla (`### Ordenes`, «colocada»).
  Las modificaciones de orden no se fechan en la salida; si las hubiera (peticiones `modificar`
  distintas de los eventos `stop_movido`), el guion sale con 3 en vez de dar un censo incompleto.
- `stop` u `objetivo` de una posicion: el stop vigente, decidido en su ultimo `stop_movido` anterior
  al evento o, si no se movio, al llenarse la orden. Si la vela empieza antes de esa decision pero
  despues de la del stop anterior, la evaluo el stop ANTERIOR (ADR-0065 §4; ADR-0051 §5, NOTA del
  2026-10-29): se cuenta aparte, porque la salida no dice con que stop salto.
- `stop_movido`: una decision del motor, no una evaluacion; se cuenta y no entra en el criterio.

Donde: «hora perdida» si la hora UTC de la vela es una de las 18 de `horas_perdidas.py`; «borde de
la cobertura de ticks» si la hora no es de las que bajan los manifiestos (06-14 UTC en enero, 05-13
en abril, julio y agosto: RECORRIDA-CONSTRUCCION.md §0.b, escritas aqui a mano para no leer ningun
manifiesto); si no, «otro».

    uv run python docs/validation/anexos/RESPALDO-M1/censo_respaldo.py <salida> [<salida> ...]
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from horas_perdidas import HORAS_PERDIDAS  # noqa: E402  (la copia de esta carpeta)

MS_MIN = 60_000
ROTULO = "[DIAGNOSTICO"
HORAS_DE_TICKS = {"2026-01": range(6, 15)}  # el resto de meses de construccion: 05-13 UTC
HORAS_DE_TICKS_RESTO = range(5, 14)
# con el codigo de esta rama la evalua el stop anterior; con el de main (las salidas de
# RECORRIDA-CONSTRUCCION) la evaluaba el nuevo, y era Z (RESPALDO-M1.md §0.e)
VELA_DEL_CAMBIO = "vela del stop movido (rama: el stop anterior, ADR-0065 §4; main: el nuevo, Z)"


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
    return "otro"


def censo(ruta: Path) -> tuple[list[str], int]:
    seccion = ""
    eventos: list[tuple[str, int, str, str, str]] = []
    colocada: dict[tuple[str, str], int] = {}
    modificar = 0
    for crudo in ruta.read_text(encoding="utf-8").splitlines():
        ln = sin_rotulo(crudo)
        if ln.startswith("### "):
            seccion = ln
            continue
        if not ln.startswith("20"):
            continue
        p = ln.split(" | ")
        if seccion.startswith("### Eventos del broker"):
            eventos.append((p[0], ms_de(p[1]), p[2], p[3], p[4]))
        elif seccion.startswith("### Ordenes ("):
            colocada[(p[0], p[2])] = ms_de(p[3])
        elif seccion.startswith("### Peticiones al servidor") and len(p) == 7:
            modificar += int(p[3])
    movidos: dict[tuple[str, str], list[int]] = defaultdict(list)
    llenada: dict[tuple[str, str], int] = {}
    for dia, ms, tipo, id_, _ in eventos:
        if tipo == "stop_movido":
            movidos[(dia, id_)].append(ms)
        elif tipo == "llenada":
            llenada[(dia, f"pos-{id_}")] = ms
    n_movidos = sum(len(v) for v in movidos.values())
    if modificar != n_movidos:
        print(
            f"{ruta.name}: {modificar} peticiones modificar y {n_movidos} stops movidos: hay "
            "modificaciones de orden que la salida no fecha; el censo quedaria incompleto",
            file=sys.stderr,
        )
        raise SystemExit(3)
    cuenta: Counter[str] = Counter()
    filas = []
    z = 0
    for dia, ms, tipo, id_, fuente in eventos:
        if fuente != "respaldo_m1":
            continue
        inicio = ((ms - 1) // MS_MIN) * MS_MIN
        lugar = donde(dia, inicio)
        if tipo == "stop_movido":
            clase = "decision del motor (no se evalua)"
        elif tipo in ("llenada", "rechazada"):
            decidida = colocada[(dia, id_)]
            clase = "Z" if inicio < decidida else "vela posterior a la decision"
        elif tipo in ("stop", "objetivo"):
            abierta = llenada[(dia, id_)]
            previos = sorted(m for m in movidos.get((dia, id_), []) if m < ms)
            versiones = [abierta, *previos]  # el instante en que se decidio cada stop
            if inicio >= versiones[-1]:
                clase = "vela posterior a la decision"
            elif len(versiones) > 1 and inicio >= versiones[-2]:
                clase = VELA_DEL_CAMBIO
            else:
                clase = "Z"
        else:
            clase = f"tipo {tipo} sin regla"
        z += clase == "Z"
        cuenta[f"{tipo} · {lugar} · {clase}"] += 1
        filas.append(f"  {dia} | {hora(ms)} | {tipo} | {id_} | {lugar} | {clase}")
    salida = [
        f"### {ruta.parent.name}/{ruta.name}: {sum(cuenta.values())} eventos del respaldo; "
        f"peticiones modificar {modificar} = stops movidos {n_movidos}; Z: {z}"
    ]
    salida += [f"  {k}: {n}" for k, n in sorted(cuenta.items())]
    return salida + filas, z


def main(rutas: list[Path]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    print("# RESPALDO-M1: el censo de los eventos del respaldo M1 (criterio de hecho: Z = 0)")
    total = 0
    for ruta in rutas:
        lineas, z = censo(ruta)
        total += z
        print("\n".join(lineas))
    print(f"Z en total: {total}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    sys.exit(main([Path(a) for a in sys.argv[1:]]))
