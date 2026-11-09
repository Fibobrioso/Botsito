"""La caja: el stop del trader frente al del bot (respuesta del consultor a la PARADA 2 de
trabajo/recorrida-construccion-2, punto 2). Lee:

- el STOP de cada operacion del trader de los casos dev de construccion, por la compuerta del arnes
  (`arnes.dias_de_construccion`, la que lee `knowledge/cases/dev/`; comprobado antes con
  `casos_reservados` y declarado en HOLDOUT-EXPOSICIONES, fila de la fase 3);
- de la salida de la corrida 1: «### Ordenes» (precio, distancia al stop, resultado y motivo de cada
  orden), la direccion de cada orden como la lee `para_clasificar.py` y las filas de «Diferencias por
  operacion» clasificadas por `patrones.py` (la copia identica de esta carpeta);
- `para-clasificar.txt`: el escalon de cada operacion del trader y la orden del bot que mira.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/caja_stop.py \\
        <corrida 1> <para-clasificar.txt>

Dos grupos, como los nombra el consultor:
1. Las operaciones con la entrada dentro (`para_clasificar.ENTRADA_DENTRO`) y la orden que mira la
   cascada: por operacion, entrada y stop del trader y del bot, Δentrada y Δstop con signo y el
   cociente de distancias; su escalon por el stop (a 3 puntos) y el llenado se comprueban contra la
   cascada impresa (stop fuera, no llenada y las cuatro piezas). De las «no llenadas», el resultado y
   el motivo literales de su fila de «Ordenes».
2. Las filas P2 de `patrones.py`, con la operacion del bot que las hace P2 (la del mismo lado a 15
   minutos o menos con la entrada mas cercana, como `patrones.clasificar`), con su Δentrada con signo.

LOS SIGNOS (el consultor: «positivo = el del bot mas lejos de la entrada que el del trader, en la
direccion de la operacion»): Δstop > 0 si el stop del bot esta mas alla del stop del trader, del lado
del stop (compra: mas abajo; venta: mas arriba). Para Δentrada se usa la misma orientacion, porque la
frase no la fija para la entrada y aqui se declara: Δentrada > 0 si la entrada del bot esta del lado
del stop respecto de la del trader (compra: mas abajo; venta: mas arriba). La regla de los dos tercios
mira solo si los signos coinciden, asi que la orientacion no cambia la clase. Cociente = distancia
entrada-stop del bot / la del trader.

LA REGLA (fijada por el consultor antes de medir): SISTEMATICA si al menos dos tercios del grupo tienen
el mismo signo; si no, DISPERSA. Antes de la clase: el redondeo del stop al punto mueve 1 punto como
mucho, asi que solo puede explicar las que estan a 4 puntos (3 de tolerancia + 1); la comision no
mueve ningun precio. Se cuentan las primeras y se dice.
"""

# ruff: noqa: E501  (textos y tablas literales: el docstring explica las columnas)

from __future__ import annotations

import re
import sys
from collections import Counter
from datetime import datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patrones  # noqa: E402  (la copia identica de esta carpeta)
from salida_comun import (  # noqa: E402  (sin importar para_clasificar: la guardia, 3 niveles)
    clase,
    cociente,
    hacia_el_stop,
    ordenes_de,
    posiciones_de,
    stop_de,
)

TOLERANCIA = 3  # puntos, la de entrada y la de stop (la salida la imprime en «tolerancias:»)
LLENADO_MIN = 15
DELTA_P2 = re.compile(r"Δentrada minima (\d+) puntos")
ENTRADA_DENTRO = "entrada dentro (el stop del trader no esta en la salida)"  # la de para_clasificar

__all__ = ["cerca_de_p2", "clase", "cociente", "hacia_el_stop", "stop_de"]


def _distribucion(valores: list[int] | list[Fraction], nombre: str) -> str:
    if not valores:
        return f"{nombre}: ninguna"
    ordenados: list[Fraction] = sorted(Fraction(v) for v in valores)
    n = len(ordenados)
    mediana = ordenados[n // 2] if n % 2 else (ordenados[n // 2 - 1] + ordenados[n // 2]) / 2
    enteros = all(isinstance(v, int) for v in valores)

    def f(x: Fraction) -> str:
        return str(x) if enteros and x.denominator == 1 else f"{float(x):.2f}"

    return (
        f"{nombre}: n {n}; minimo {f(ordenados[0])}; mediana {f(mediana)}; maximo "
        f"{f(ordenados[-1])}"
    )


def cerca_de_p2(
    cerca: list[tuple[str, datetime, Decimal]], t: datetime, e_t: Decimal
) -> tuple[str, datetime, Decimal]:
    """La operacion del bot que hace P2 a una del trader: la de entrada mas cercana entre las del
    mismo lado a 15 minutos o menos (y, a igualdad, la mas cercana en el tiempo)."""
    return min(cerca, key=lambda x: (abs(x[2] - e_t), abs((x[1] - t).total_seconds())))


def main(corrida: Path, para_clasificar: Path, repo: Path) -> int:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.engine import arnes

    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    criterio = cargar_criterio(repo)
    dias = arnes.dias_de_construccion(repo, criterio, sorted(criterio.construccion))
    stop_trader = {
        (op.dia, op.sesion, op.direccion, op.instante.isoformat(), str(op.entrada)): op.stop
        for d in dias
        for op in d.operaciones
    }
    texto = corrida.read_text(encoding="utf-8")
    ordenes = ordenes_de(texto)

    # 1. las de la entrada dentro, con la orden que mira la cascada (para-clasificar.txt)
    filas_pc = []
    dentro = False
    for ln in para_clasificar.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## Operaciones del trader"):
            dentro = True
            continue
        if dentro and ln.startswith("## "):
            break
        if dentro and ln.startswith("20"):
            filas_pc.append(ln.split(" | "))
    print(f"# La caja (respuesta a la PARADA 2, punto 2). Corrida 1: {corrida.name}")
    print(
        "# signos: > 0 = el del bot mas alla del del trader, del lado del stop (ver el docstring)"
    )
    print()
    print("## 1. Entrada dentro: el stop")
    print(
        "dia | sesion | lado | instante del trader | entrada T | stop T | orden | entrada B | "
        "stop B | Δentrada | Δstop | cociente | grupo | resultado y motivo de la orden"
    )
    grupos: Counter[str] = Counter()
    delta_stop_fuera: list[int] = []
    cocientes_fuera: list[Fraction] = []
    a_cuatro = 0
    for c in filas_pc:
        if c[5] != ENTRADA_DENTRO:
            continue
        clave = (c[0], c[1], c[2], c[3], c[4])
        st = stop_trader.get(clave)
        oid = c[6].split(" ")[0]
        o = ordenes.get((c[0], oid))
        e_t = Decimal(c[4])
        if st is None or o is None or o.stop is None:
            print(f"{' | '.join(clave)} | - | {oid} | sin stop del caso o sin la orden")
            grupos["sin dato"] += 1
            continue
        de = hacia_el_stop(c[2], o.precio, e_t)
        ds = hacia_el_stop(c[2], o.stop, st)
        q = cociente(o.precio, o.stop, e_t, st)
        if abs(ds) > TOLERANCIA:
            grupo = "stop fuera"
            delta_stop_fuera.append(ds)
            cocientes_fuera.append(q)
            a_cuatro += abs(ds) == TOLERANCIA + 1
        elif o.resultado != "llenada":
            grupo = "en el nivel, no llenada"
        else:
            t = datetime.fromisoformat(c[3])
            fuera = abs((datetime.fromisoformat(o.instante) - t).total_seconds()) > LLENADO_MIN * 60
            grupo = "llenada fuera de 15 min" if fuera else "las cuatro piezas"
        grupos[grupo] += 1
        detalle = (
            f"{o.resultado}: {o.motivo}" if grupo == "en el nivel, no llenada" else o.resultado
        )
        print(
            f"{' | '.join(clave)} | {st} | {oid} | {o.precio} | {o.stop} | {de:+d} | {ds:+d} | "
            f"{float(q):.2f} | {grupo} | {detalle}"
        )
    print()
    print("grupos: " + ", ".join(f"{k} {v}" for k, v in sorted(grupos.items())))
    cl, pos, neg, ceros = clase(delta_stop_fuera)
    print(
        f"stop fuera: {len(delta_stop_fuera)}; Δstop > 0 {pos}, < 0 {neg}, = 0 {ceros}; regla de los "
        f"dos tercios: {cl}"
    )
    print(_distribucion(delta_stop_fuera, "Δstop (puntos) de las de stop fuera"))
    print(_distribucion(cocientes_fuera, "cociente de las de stop fuera"))
    print(
        f"stop fuera a exactamente {TOLERANCIA + 1} puntos (las unicas que el redondeo del stop al "
        f"punto podria explicar): {a_cuatro}; la comision no mueve ningun precio"
    )

    # 2. las P2, con la operacion del bot que las hace P2
    filas, sesgo = patrones.leer(corrida)
    bot = patrones._ops_bot(filas)
    print()
    print("## 2. P2: la entrada")
    print(
        "dia | sesion | lado | instante del trader | entrada T | stop T | Δentrada minima de "
        "patrones | entrada B | stop B | Δentrada | Δstop | cociente | tramo"
    )
    tramos: Counter[str] = Counter()
    delta_p2: list[int] = []
    # (dia, llenada UTC, entrada) -> id de la orden, de «### Posiciones»
    posiciones = {(c[0], c[6], Decimal(c[7])): c[3] for c in posiciones_de(texto)}
    for patron, detalle, _marca, fila in patrones.clasificar(filas, sesgo):
        if patron != "P2 entrada":
            continue
        q_, dia, sesion, lado, instante, entrada, _r = fila.split(" | ", 6)
        t, e_t = datetime.fromisoformat(instante), Decimal(entrada)
        cerca = [
            b for b in bot.get((dia, sesion), [])
            if b[0] == lado and abs((b[1] - t).total_seconds()) <= LLENADO_MIN * 60
        ]  # fmt: skip
        b = cerca_de_p2(cerca, t, e_t)
        de = hacia_el_stop(lado, b[2], e_t)
        m = DELTA_P2.search(detalle)
        minimo = int(m.group(1)) if m else abs(de)
        tramo = "4-10 puntos" if minimo <= 10 else "mas de 10 puntos"
        tramos[tramo] += 1
        if tramo == "4-10 puntos":
            delta_p2.append(de)
        st = stop_trader.get((dia, sesion, lado, instante, entrada))
        orden_p2 = posiciones.get((dia, b[1].isoformat(), b[2]))
        o = ordenes.get((dia, orden_p2)) if orden_p2 is not None else None
        stop_b = o.stop if o is not None else None
        ds_p2: int | None = (
            hacia_el_stop(lado, stop_b, st) if stop_b is not None and st is not None else None
        )
        q_p2 = (
            f"{float(cociente(b[2], stop_b, e_t, st)):.2f}"
            if stop_b is not None and st is not None
            else "-"
        )
        print(
            f"{dia} | {sesion} | {lado} | {instante} | {entrada} | {st} | {minimo} | {b[2]} | "
            f"{stop_b if stop_b is not None else '-'} | {de:+d} | "
            f"{f'{ds_p2:+d}' if ds_p2 is not None else '-'} | {q_p2} | {tramo}"
        )
    print()
    print("tramos de P2: " + ", ".join(f"{k} {v}" for k, v in sorted(tramos.items())))
    cl, pos, neg, ceros = clase(delta_p2)
    print(
        f"P2 a 4-10 puntos: {len(delta_p2)}; Δentrada > 0 {pos}, < 0 {neg}, = 0 {ceros}; regla de los "
        f"dos tercios: {cl}"
    )
    print(_distribucion(delta_p2, "Δentrada (puntos) de las P2 a 4-10 puntos"))
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]), Path.cwd()))
