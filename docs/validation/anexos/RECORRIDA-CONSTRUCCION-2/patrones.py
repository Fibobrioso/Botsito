"""La clasificacion PROVISIONAL por patrones del consultor (respuesta a la PARADA 2 de
trabajo/corrida-construccion, 2026-10-14, punto 4), aplicada con sus reglas LITERALES a la tabla
«Diferencias por operacion» de una salida del arnes, y el recuento por mes. Si el recuento no
coincide con el suyo, se dice en la PARADA 3: aqui no se ajusta ni una regla ni una cifra.

COPIA de docs/validation/anexos/CORRIDA-CONSTRUCCION/patrones.py para trabajo/recorrida-construccion
(RECORRIDA-CONSTRUCCION.md §0.e) con UNA sola diferencia: `_cuerpo` corta el rotulo de diagnostico
solo si la linea empieza por `[DIAGNOSTICO`. La copia de R3.1 cortaba por el primer «] », y las
lineas «Por sesion» llevan «] » en su propio cuerpo (arnes.py, `{hecho}:no[...]`): sobre una salida
SIN rotulo, como la corrida que cuenta por ADR-0070 §3, perdia el sesgo de todas las sesiones y
daba un P1 falso a toda fila del trader sin pareja (medido: 0 sesiones con rn003 y 180 P1 frente a
44). Ninguna regla de clasificacion cambia.

Uso: uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/patrones.py <salida> [--filas]

Reglas, para cada fila (el sesgo es el rn003 de la linea «Por sesion» de su sesion; «a favor» =
compra con alcista o venta con bajista):
- T0 pareja: filas del trader con PAREJA.
- P1 sesgo: filas del trader sin pareja y contra el sesgo del bot.
- P7 entradas repetidas (respuesta a la PARADA 3, punto 2; va ANTES de P2): filas del trader sin
  pareja cuya operacion del bot mas cercana esta a 3 puntos o menos y a menos de 15 minutos, pero
  ya emparejada con otra operacion del trader.
- P2 entrada: filas del trader sin pareja, a favor del sesgo, con una operacion del bot del mismo
  lado a menos de 15 minutos y a mas de 3 puntos.
- P3 otra zona: filas del trader sin pareja, a favor del sesgo, con el bot del mismo lado en la
  sesion pero a mas de 15 minutos.
- P4 sin orden: filas del trader sin pareja, a favor del sesgo, sin ninguna operacion del bot en
  la sesion.
- P5 de mas: filas del bot sin pareja en una sesion con operaciones del trader (del mismo lado que
  alguna del trader, o del otro).
- P6 donde el trader no opero: filas del bot en una sesion o un dia sin operaciones del trader.
Ademas, sin cambiar el patron, se marca «posible M» en las filas que tocan una hora de ticks
perdida (las de horas_perdidas.py).

Lo que las reglas no dicen y aqui se decide, y se declara: «a favor» con un sesgo que no es
alcista ni bajista (insuficiente) cuenta como CONTRA (P1); en P2 y P3 «del mismo lado» se mira
sobre TODAS las operaciones del bot de la sesion (las filas del bot y las emparejadas, no solo la
mas cercana de la tabla); una fila va a P2 si alguna del mismo lado esta a <= 15 min (como no es
pareja, esta a > 3 puntos), y a P3 si hay alguna del mismo lado pero ninguna a <= 15 min; si en la
sesion solo hay operaciones del bot del otro lado, no encaja en P2, P3 ni P4 y se cuenta aparte
como «P? solo otro lado».
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from horas_perdidas import HORAS_PERDIDAS, INSTANTE, hora_de  # noqa: E402  (el guion vecino)

ESCALA = 100_000
TOL_PUNTOS = 3
TOL_SEGUNDOS = 15 * 60
A_FAVOR = {("compra", "alcista"), ("venta", "bajista")}
POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader (\d+) \| bot (\d+) \| rn003 (\S+) \|"
)


ROTULO = "[DIAGNOSTICO"


def _cuerpo(ln: str) -> str:
    """La linea sin su rotulo de diagnostico, si lo lleva; una linea sin rotulo, tal cual."""
    if ln.startswith(ROTULO) and "] " in ln:
        return ln.split("] ", 1)[1]
    return ln


def leer(ruta: Path) -> tuple[list[list[str]], dict[tuple[str, str], str]]:
    filas: list[list[str]] = []
    sesgo: dict[tuple[str, str], str] = {}
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = _cuerpo(ln)
        if c.startswith(("trader | ", "bot | ")):
            filas.append(c.split(" | ", 6))
        m = POR_SESION.match(c)
        if m:
            sesgo[(m.group(1), m.group(2))] = m.group(5)
    return filas, sesgo


def _ops_bot(filas: list[list[str]]) -> dict[tuple[str, str], list[tuple[str, datetime, Decimal]]]:
    """TODAS las operaciones del bot por sesion: las filas del bot sin pareja y las emparejadas,
    que no salen aparte y se leen de la fila de su trader."""
    bot: dict[tuple[str, str], list[tuple[str, datetime, Decimal]]] = defaultdict(list)
    for quien, dia, sesion, lado, instante, entrada, resultado in filas:
        if quien == "bot":
            bot[(dia, sesion)].append((lado, datetime.fromisoformat(instante), Decimal(entrada)))
        elif resultado.startswith("PAREJA bot "):
            _, _, b_instante, b_entrada, *_ = resultado.split(" ", 4)
            bot[(dia, sesion)].append(
                (lado, datetime.fromisoformat(b_instante), Decimal(b_entrada))
            )
    return bot


def clasificar(
    filas: list[list[str]], sesgo: dict[tuple[str, str], str]
) -> list[tuple[str, str, str, str]]:
    """(patron, detalle, marca M, fila) por fila."""
    bot = _ops_bot(filas)
    trader_en = {(f[1], f[2]) for f in filas if f[0] == "trader"}
    dias_trader = {f[1] for f in filas if f[0] == "trader"}
    salida = []
    for fila in filas:
        quien, dia, sesion, lado, instante, entrada, resultado = fila
        clave = (dia, sesion)
        horas = sorted(
            {hora_de(i) for i in INSTANTE.findall(" | ".join(fila))} & set(HORAS_PERDIDAS)
        )
        marca = "posible M (hora perdida " + ", ".join(horas) + ")" if horas else ""
        if quien == "trader":
            if resultado.startswith("PAREJA"):
                salida.append(("T0 pareja", "", marca, " | ".join(fila)))
                continue
            s = sesgo.get(clave, "?")
            if (lado, s) not in A_FAVOR:
                salida.append(("P1 sesgo", f"sesgo {s}", marca, " | ".join(fila)))
                continue
            t = datetime.fromisoformat(instante)
            e = Decimal(entrada)
            mismo_lado = [b for b in bot.get(clave, []) if b[0] == lado]
            cerca = [b for b in mismo_lado if abs((b[1] - t).total_seconds()) <= TOL_SEGUNDOS]
            # P7 (respuesta a la PARADA 3, punto 2), ANTES de P2: la del bot mas cercana esta a
            # 3 puntos o menos y a menos de 15 minutos, pero ya emparejada con otra del trader
            repetidas = [b for b in cerca if abs((b[2] - e) * ESCALA) <= TOL_PUNTOS]
            if repetidas:
                deltas = sorted(abs((b[2] - e) * ESCALA) for b in repetidas)
                detalle = f"Δentrada {int(deltas[0])} puntos, bot ya emparejado"
                salida.append(("P7 entradas repetidas", detalle, marca, " | ".join(fila)))
            elif cerca:
                deltas = sorted(abs((b[2] - e) * ESCALA) for b in cerca)
                salida.append(
                    (
                        "P2 entrada",
                        f"Δentrada minima {int(deltas[0])} puntos",
                        marca,
                        " | ".join(fila),
                    )
                )
            elif mismo_lado:
                misma = any(abs((b[2] - e) * ESCALA) <= TOL_PUNTOS for b in mismo_lado)
                salida.append(
                    (
                        "P3 otra zona",
                        "misma entrada, otra hora" if misma else "otra entrada",
                        marca,
                        " | ".join(fila),
                    )
                )
            elif bot.get(clave):
                salida.append(
                    (
                        "P? solo otro lado",
                        "bot solo del otro lado en la sesion",
                        marca,
                        " | ".join(fila),
                    )
                )
            else:
                salida.append(("P4 sin orden", "", marca, " | ".join(fila)))
        else:
            if clave in trader_en:
                trader_lados = {f[3] for f in filas if f[0] == "trader" and (f[1], f[2]) == clave}
                detalle = "mismo lado" if lado in trader_lados else "otro lado"
                salida.append(("P5 de mas", detalle, marca, " | ".join(fila)))
            else:
                detalle = "en sesion" if dia in dias_trader else "en dia"
                salida.append(("P6 donde el trader no opero", detalle, marca, " | ".join(fila)))
    return salida


def main(ruta: Path, con_filas: bool) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    filas, sesgo = leer(ruta)
    clasificadas = clasificar(filas, sesgo)
    print(f"{ruta.name}: {len(filas)} filas, {len(sesgo)} sesiones con rn003")
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    total: Counter[str] = Counter()
    detalles: Counter[tuple[str, str]] = Counter()
    sesiones_p1: set[tuple[str, str]] = set()
    marcadas = 0
    for patron, detalle, marca, fila in clasificadas:
        mes = fila.split(" | ")[1][:7]
        por_mes[mes][patron] += 1
        total[patron] += 1
        if detalle:
            detalles[(patron, detalle.split(" ")[0] if patron == "P2 entrada" else detalle)] += 1
        if patron == "P1 sesgo":
            sesiones_p1.add(tuple(fila.split(" | ")[1:3]))  # type: ignore[arg-type]
        marcadas += bool(marca)
    patrones = sorted(total)
    print("mes | " + " | ".join(patrones))
    for mes in sorted(por_mes):
        print(f"{mes} | " + " | ".join(str(por_mes[mes][p]) for p in patrones))
    print("total | " + " | ".join(str(total[p]) for p in patrones))
    print(f"P1 sesgo: {total['P1 sesgo']} filas en {len(sesiones_p1)} sesiones")
    for (patron, detalle), n in sorted(detalles.items()):
        print(f"  {patron} · {detalle}: {n}")
    print(f"filas marcadas posible M (hora perdida): {marcadas}")
    if con_filas:
        print("-- filas")
        for patron, detalle, marca, fila in clasificadas:
            extra = f" [{detalle}]" if detalle else ""
            extra += f" [{marca}]" if marca else ""
            print(f"{patron}{extra}: {fila}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), "--filas" in sys.argv[2:]))
