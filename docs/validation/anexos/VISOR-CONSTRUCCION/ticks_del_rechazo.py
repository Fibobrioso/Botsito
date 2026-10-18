"""VISOR-CONSTRUCCION (R3.2), comprobacion de los rechazos por `precio_invalido` (ADR-0057): para
cada orden del dia rechazada por ese motivo, donde la coloco el bot frente al bid o el ask de ese
instante.

Corre el dia como `motor visor --simular --caso` (comun_visor.py) y, para cada orden rechazada, lee
la cotizacion con LA MISMA funcion que uso el broker al rechazarla (`Mercado.cotizacion`, el ultimo
tick anterior o igual al instante; donde no hay ticks, la ultima M1 cerrada mas el spread supuesto:
`fuente` lo dice) y la regla del lado equivocado (`llenado.lado_equivocado`). No lee ningun fichero
por su ruta: los ticks llegan por la compuerta del arnes (`mercado_de_construccion`). Solo imprime
el dia dev (nada anterior a las 00:00Z de su fecha) y nada en dinero.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/ticks_del_rechazo.py <caso>
"""

from __future__ import annotations

import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun_visor as cv  # noqa: E402

from botsito.engine import cableado  # noqa: E402
from botsito.engine.broker import MOTIVO_PRECIO_INVALIDO, RECHAZADA  # noqa: E402
from botsito.engine.llenado import lado_equivocado  # noqa: E402


def _precio(puntos: int, escala: int) -> str:
    return str(Decimal(puntos) / escala)


def main(caso: str) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    d = cv.construir(caso)
    iguales, diferencias = cv.ordenes_coinciden(d)
    print(f"CASO {d.caso}")
    if not iguales:
        print("ORDENES frente a «### Ordenes» de main: DISTINTAS -> PARADA")
        for linea in diferencias:
            print(f"  {linea}")
        return 3
    print("ORDENES frente a «### Ordenes» de main: iguales")
    broker = d.broker
    escala = broker.escala
    rechazos = {r.orden_id: r for r in broker.traza().rechazos}
    n = 0
    for f in cableado.vida_de_las_ordenes(d.motor):
        o = broker.ordenes[f[2]]
        r = rechazos.get(o.id)
        if o.estado != RECHAZADA or r is None or r.motivo != MOTIVO_PRECIO_INVALIDO:
            continue
        n += 1
        if r.instante_ms < d.inicio_utc_ms():
            print(f"  {o.id}: {cv.OCULTO}")
            continue
        q = broker.mercado.cotizacion(r.instante_ms, broker.config.spread_supuesto)
        if q is None:
            print(f"  {o.id}: sin cotizacion en ese instante")
            continue
        bid, ask, fuente = q
        referencia = ask if o.lado == "compra" else bid
        equivocado = lado_equivocado(o.tipo, o.lado, o.precio, bid, ask)
        ya_paso = (o.precio < ask) if o.lado == "compra" else (o.precio > bid)
        nombre_ref = "ask" if o.lado == "compra" else "bid"
        print(
            f"  {o.id} {o.tipo} {o.lado} | sesion {f[1]} | colocada "
            f"{cv.hora(r.instante_ms, es_ms=True)} | precio de la orden (el 0) "
            f"{_precio(o.precio, escala)} | bid {_precio(bid, escala)} ask {_precio(ask, escala)} "
            f"({fuente}) | el precio de referencia ({nombre_ref}) ya paso el 0: "
            f"{'si' if ya_paso else 'no'}, por {abs(referencia - o.precio)} puntos | "
            f"lado equivocado segun el broker: {'si' if equivocado else 'no'}"
        )
    print(f"rechazos por {MOTIVO_PRECIO_INVALIDO} del dia: {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
