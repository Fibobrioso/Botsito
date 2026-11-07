"""SELLO-RESPALDO-M1, fase 0 c), d) y f): el prototipo EN MEMORIA de (e2) y de (c2), y el visor por caso.

No toca `src/`: en este proceso sustituye, con funciones ESCRITAS AQUI (copias literales de las de
`main` con el cambio de cada forma, sin `exec`: la guardia niega ejecutar codigo que no es literal),
lo que cada forma cambia, y despues llama al visor de la CLI por caso, igual que
`uv run botsito motor visor --caso <id> --simular --salida <carpeta>`. Las paginas van a la carpeta
que se le da, fuera del repositorio; lo que se imprime sale del motor cableado que el visor construyo.

Las formas (las del diagnostico `diagH` del 2026-10-31, `forma_e2.diff` y `forma_c2.diff`, vueltas a
escribir aqui sobre el `main` de hoy):
- `main`: nada;
- `e2`: `_peor_del_minuto` acepta la vela solo si EMPIEZA estrictamente antes de `hasta`
  (`broker.py:955`);
- `c2`: (e2); el evento del respaldo sellado en el cierre de su vela MENOS 1 ms en las tres funciones
  del respaldo (`llenado.py:184,193,240,252,327,345,351`: `_fin_ms` devuelve el fin menos 1 ms SOLO
  cuando lo llaman ellas; `Mercado.cotizacion`, que tambien lo usa, sigue igual, como en diagH); y
  los tres lectores del minuto de apertura con `(abierta_ms + 1)`: `_marcar_hasta` (`broker.py:933`),
  la sesion de la posicion (`cableado.py:469`) y el break even por velas
  (`primitivas_broker.py:279`, aqui con la vela del llenado fuera de la lista que reciben
  `zona_posterior_completada` y `nivel_de_activacion_posterior`, que es lo que hace el «+ 1»);
- `rama` (fase 2, la verificacion del punto 8 de la respuesta del consultor): nada parcheado, el
  codigo commiteado de la rama con ADR-0091, y la sesion de cada posicion leida como la lee la rama
  (`minuto_de_apertura`). Las tres de arriba son para el codigo de `main`: sobre el de la rama, `e2`
  y `c2` parchearian dos veces.

Solo dias `dev` de construccion, por la compuerta del visor (un caso oculto se niega sin leerse). Por
dia, nunca agregado: las ordenes (tipo, lado, colocada, resultado e instante), las posiciones
(sesion, lado, vela de entrada, salida y R) y, para cada orden cancelada en el cierre de una M1, si
esa M1 tiene ticks y, si no, si la habria llenado (la funcion del respaldo de `main` sobre esa sola
vela). No imprime precios.

    uv run python -B docs/validation/anexos/SELLO-RESPALDO-M1/prototipo_sello.py <forma> <carpeta> <AAAA-MM-DD> [...]
"""

# ruff: noqa: E501  (la cabecera lleva el comando de uso y rutas literales, como simular_cierre.py)
from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from botsito import cli
from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import arnes, broker, cableado, llenado, primitivas_broker
from botsito.engine.cableado import OperacionCriterio, _precio

REPO = Path.cwd()
FORMAS = ("main", "e2", "c2", "rama")
DEL_RESPALDO = {"primer_llenado_limite", "primer_llenado_stop", "primera_salida"}
ORIGINAL_FIN_MS = llenado._fin_ms
ORIGINAL_ZONA = primitivas_broker.zona_posterior_completada
ORIGINAL_NIVEL = primitivas_broker.nivel_de_activacion_posterior
ORIGINALES = {"limite": llenado.primer_llenado_limite, "stop": llenado.primer_llenado_stop}
ACTUAL: list[broker.Broker] = []  # el broker del dia en curso (para el break even de c2)
FORMA = ""


# ---------------------------------------------------------------------------- (e2)


def peor_del_minuto_e2(
    self: broker.Broker, lado: str, minuto: int, desde_ms: int, hasta_ms: int
) -> int | None:
    """`Broker._peor_del_minuto` de `main` con (e2) en la condicion de la vela."""
    ticks = self.mercado.ticks_del_minuto(minuto)
    if ticks is not None:
        valores = [
            int(t.bid) if lado == "compra" else int(t.ask)
            for t in ticks
            if desde_ms <= t.instante <= hasta_ms
        ]
        if not valores:
            return None
        return min(valores) if lado == "compra" else max(valores)
    vela = self.mercado.m1(minuto)
    if vela is None or int(vela.inicio) * MS_POR_MINUTO >= hasta_ms:  # (e2)
        return None
    spread = self.config.spread_supuesto(MinutoUtc(minuto))
    return int(vela.minima) if lado == "compra" else int(vela.maxima) + spread


# ---------------------------------------------------------------------------- (c2)


def fin_ms_c2(vela: Vela) -> int:
    """`llenado._fin_ms`, menos 1 ms solo para las tres funciones del respaldo (el sello de (c))."""
    if sys._getframe(1).f_code.co_name in DEL_RESPALDO:
        return ORIGINAL_FIN_MS(vela) - 1
    return ORIGINAL_FIN_MS(vela)


def marcar_hasta_c2(self: broker.Broker, hasta_ms: int) -> None:
    """`Broker._marcar_hasta` de `main` con el minuto de apertura leido con `+ 1`."""
    for p in self.posiciones.values():
        if not p.abierta:
            continue
        desde = (
            p.marcas[-1][0] // MS_POR_MINUTO + 1
            if p.marcas
            else (p.abierta_ms + 1) // MS_POR_MINUTO  # (c2)
        )
        for m in range(desde, hasta_ms // MS_POR_MINUTO + 1):
            peor = self._peor_del_minuto(p.lado, m, p.abierta_ms, hasta_ms)
            if peor is None:
                continue
            p.marcas.append((min(m * MS_POR_MINUTO + MS_POR_MINUTO - 1, hasta_ms), peor))
            p.ultimo_precio = peor
        self._swaps(p, hasta_ms)


def operaciones_del_bot_c2(
    self: cableado.MotorCableado,
    b: broker.Broker,
    md: Any,
    dia: Any,
    limites: Sequence[tuple[str, int, int]],
) -> tuple[OperacionCriterio, ...]:
    """`MotorCableado._operaciones_del_bot` de `main` con el minuto de apertura leido con `+ 1`."""
    salida: list[OperacionCriterio] = []
    for p in sorted(b.posiciones.values(), key=lambda x: x.abierta_ms):
        minuto = (p.abierta_ms + 1) // MS_POR_MINUTO  # (c2)
        sesion = next((n for n, d, h in limites if d <= minuto < h), None)
        if sesion is None:
            continue
        salida.append(
            OperacionCriterio(
                dia.dia.isoformat(),
                sesion,
                p.lado,
                datetime.fromtimestamp(p.abierta_ms / 1000, UTC),
                _precio(p.entrada, b.escala),
            )
        )
    return tuple(salida)


def _sin_la_vela_del_llenado(m1: list[Vela]) -> tuple[list[Vela], int]:
    """Lo que el `+ 1` de `primitivas_broker.py:279` deja: si la unica posicion viva se abrio en el
    ultimo milisegundo de un minuto, la vela de ese minuto (la primera de la lista) no entra."""
    vivas = [p for p in ACTUAL[-1].posiciones.values() if p.abierta] if ACTUAL else []
    if len(vivas) != 1 or not m1:
        return m1, 0
    p = vivas[0]
    a, b = p.abierta_ms // MS_POR_MINUTO, (p.abierta_ms + 1) // MS_POR_MINUTO
    if a != b and int(m1[0].inicio) == a:
        return m1[1:], 1
    return m1, 0


def zona_posterior_completada_c2(m1: list[Vela], *a: Any, **k: Any) -> int | None:
    resto, quitadas = _sin_la_vela_del_llenado(m1)
    i = ORIGINAL_ZONA(resto, *a, **k)
    return None if i is None else i + quitadas  # el llamador indexa la lista entera


def nivel_de_activacion_posterior_c2(m1: list[Vela], *a: Any, **k: Any) -> Any:
    resto, _ = _sin_la_vela_del_llenado(m1)
    return ORIGINAL_NIVEL(resto, *a, **k)


def aplicar(forma: str) -> None:
    original_init = broker.Broker.__init__

    def init(self: broker.Broker, *a: Any, **k: Any) -> None:
        original_init(self, *a, **k)
        ACTUAL.append(self)

    broker.Broker.__init__ = init  # type: ignore[method-assign]  # solo registra el broker del dia
    if forma in ("main", "rama"):
        return
    broker.Broker._peor_del_minuto = peor_del_minuto_e2  # type: ignore[assignment,method-assign]
    if forma == "e2":
        return
    llenado._fin_ms = fin_ms_c2
    broker.Broker._marcar_hasta = marcar_hasta_c2  # type: ignore[method-assign]
    cableado.MotorCableado._operaciones_del_bot = operaciones_del_bot_c2  # type: ignore[method-assign]
    primitivas_broker.zona_posterior_completada = zona_posterior_completada_c2
    primitivas_broker.nivel_de_activacion_posterior = nivel_de_activacion_posterior_c2


# ---------------------------------------------------------------------------- informe


def hora(ms: int | None) -> str:
    if ms is None:
        return "-"
    return datetime.fromtimestamp(ms / 1000, UTC).strftime("%H:%M:%S.%f")[:-3] + "Z"


def caso_del_dia(dia: str) -> str:
    criterio = cargar_criterio(REPO)
    for d in arnes.dias_de_construccion(REPO, criterio, [dia[:7]]):
        if d.dia == dia:
            return d.id
    raise SystemExit(f"{dia}: no es un dia de construccion")


def vela_k(b: broker.Broker, o: broker.Orden, k: int) -> str:
    """Lo que la M1 k habria hecho con la orden: la funcion del respaldo de MAIN sobre esa vela."""
    if b.mercado.ticks_del_minuto(k) is not None:
        return "M1 k con ticks"
    if b.mercado.m1(k) is None:
        return "sin M1 k"
    actual = llenado._fin_ms
    llenado._fin_ms = ORIGINAL_FIN_MS  # la regla de main, tambien en c2
    try:
        ev = ORIGINALES[o.tipo](
            o.lado, o.precio, k * MS_POR_MINUTO - 1, (k + 1) * MS_POR_MINUTO, b.mercado, b.config,
            o.colocada_ms,
        )  # fmt: skip
    finally:
        llenado._fin_ms = actual
    return "M1 k sin ticks; la LLENARIA" if ev is not None else "M1 k sin ticks; no la llena"


def informe(motor: cableado.MotorCableado, dia: str) -> None:
    b = motor.brokers[dia]
    limites = motor.trazas_broker[dia].limites
    print(f"## {dia}")
    print("ordenes: id | tipo | lado | colocada | resultado | instante del resultado | M1 k")
    for o in sorted(b.ordenes.values(), key=lambda x: (x.colocada_ms, x.id)):
        fin = o.historial[-1][0] if o.historial else None
        extra = ""
        if o.estado == broker.CANCELADA and fin is not None and (fin + 1) % MS_POR_MINUTO == 0:
            extra = vela_k(b, o, (fin + 1) // MS_POR_MINUTO - 1)
        print(
            f"  {o.id} | {o.tipo} | {o.lado} | {hora(o.colocada_ms)} | {o.estado} | "
            f"{hora(fin)} | {extra}"
        )
    print("posiciones: orden | sesion | lado | abierta | vela de entrada | salida | cerrada | R")
    for p in sorted(b.posiciones.values(), key=lambda x: (x.abierta_ms, x.id)):
        a = p.abierta_ms + 1 if FORMA in ("c2", "rama") else p.abierta_ms
        minuto = a // MS_POR_MINUTO
        sesion = next((n for n, d, h in limites if d <= minuto < h), "fuera")
        stop0 = b.ordenes[p.orden_id].stop if p.orden_id in b.ordenes else p.stop
        signo = 1 if p.lado == "compra" else -1
        r = "-"
        if p.precio_cierre is not None and p.entrada != stop0:
            r = f"{signo * (p.precio_cierre - p.entrada) / abs(p.entrada - stop0):.2f}"
        llenado_en = p.abierta_ms - 1 if (p.abierta_ms % MS_POR_MINUTO == 0) else p.abierta_ms
        vela = hora(llenado_en // MS_POR_MINUTO * MS_POR_MINUTO)[:5]
        print(
            f"  {p.orden_id} | {sesion} | {p.lado} | {hora(p.abierta_ms)} ({p.fuente_apertura}) | "
            f"M1 {vela}Z | {p.motivo_cierre} ({p.fuente_cierre}) | {hora(p.cerrada_ms)} | {r}"
        )


def main(forma: str, carpeta: Path, dias: list[str]) -> int:
    global FORMA
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    if forma not in FORMAS:
        raise SystemExit(f"forma: una de {FORMAS}")
    if carpeta.resolve().is_relative_to(REPO.resolve()):
        raise SystemExit("la carpeta de las paginas va FUERA del repositorio")
    FORMA = forma
    aplicar(forma)
    construidos: list[cableado.MotorCableado] = []
    original = cableado.construir_motor_cableado

    def guardar(*a: Any, **k: Any) -> cableado.MotorCableado:
        m = original(*a, **k)
        construidos.append(m)
        return m

    cableado.construir_motor_cableado = guardar  # type: ignore[assignment]
    print(f"# prototipo_sello.py, forma {forma}")
    for dia in dias:
        caso = caso_del_dia(dia)
        codigo = cli.main(
            ["--repo", str(REPO), "motor", "visor", "--caso", caso, "--simular",
             "--salida", str(carpeta / forma)]
        )  # fmt: skip
        if codigo != 0:
            print(f"## {dia}: el visor salio con {codigo}")
            continue
        informe(construidos[-1], dia)
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    sys.exit(main(sys.argv[1], Path(sys.argv[2]), sys.argv[3:]))
