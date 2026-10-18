"""VISOR-CONSTRUCCION (R3.2), respuesta del consultor a la PARADA, punto 1: la traza por cierre
de M1 de UN dia, con el mismo motor que `motor visor --simular --caso` y las opciones de la
corrida 2.

Solo LEE. Envuelve, dentro de este proceso y sin tocar `src/`, tres cosas para mirar lo que pasa:
- `Interprete.evento`: el `Evento` de cada cierre (reglas disparadas en orden, efectos prohibidos,
  acciones bloqueadas con su regla), que la salida del arnes solo da por sesion;
- `Interprete.evaluar`, solo para los tres predicados de RN-004 (`alcanza_nivel`, `cruza`,
  `la_toma_es_de_la_sesion`): su resultado en cada cierre, y el pivote de M15 que es la liquidez;
- `cableado.primitivas_cableadas`: para quedarse con el contexto del dia (la zona de cada orden).
Cada envoltura llama al original y devuelve lo mismo: ninguna decision cambia. Al final compara
sus ordenes con las de «### Ordenes» de la salida de main para ese dia; si difieren, sale con 3
(PARADA).

Lo que imprime cumple la regla de la rama (comun_visor.py): nada anterior a las 00:00Z de la fecha
del caso (se escribe «(antes del dia)») y nada en dinero.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/traza_por_cierre.py <caso>
        [--sesion 07-11|11-15] [--rn004] [--todos-los-cierres] [--velas HH:MM-HH:MM] [--gates]
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping
from decimal import Decimal
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comun_visor as cv  # noqa: E402

from botsito.domain.estructura_m1 import zonas_de_control  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO  # noqa: E402
from botsito.engine import cableado, zonas  # noqa: E402
from botsito.engine import primitivas as prim  # noqa: E402
from botsito.engine.interprete import Interprete  # noqa: E402

PREDICADOS_RN004 = ("alcanza_nivel", "cruza", "la_toma_es_de_la_sesion")
RESUMIDO = "orden_dimensionada"  # cambia en cada cierre: se resume en una linea
# los predicados de los gates de las sesiones sin orden: RN-005, RN-009 y la ventana de RN-001
RUIDO, SUPERAN, VENTANA = (
    "se_desarrolla_en_el_lado_de_ruido",
    "zonas_desarrolladas_superan",
    "en_ventana",
)
DETENIDOS = ("detenido_por_tope", "detenido_por_tope_total", "detenido_por_cartuchos")


class Lector:
    """Lo que las envolturas apuntan; nada de esto vuelve al motor."""

    def __init__(self) -> None:
        self.cierres: list[
            tuple[int, str | None, list[str], list[str], list[tuple[str, str, str]]]
        ] = []
        self.rn004: dict[int, dict[str, str]] = {}
        self.pivote: dict[int, Any] = {}
        self.ctx: Any = None
        # por cierre: el valor de cada predicado de gate y lo que lo decide
        self.gates: dict[int, dict[str, tuple[str, Any]]] = {}
        self.ultima_zona: dict[int, Any] = {}

    def instalar(self, motor: Any) -> None:
        lector = self
        evento_original = Interprete.evento
        evaluar_original = Interprete.evaluar
        primitivas_original = cableado.primitivas_cableadas
        zona_original = zonas.zona_del_punto

        def zona_del_punto(registro: Any, momento: Any, estado: Any) -> Any:
            # la zona que RN-005 y RN-011 ven en este cierre (idempotente, ADR-0055 §1)
            z = zona_original(registro, momento, estado)
            lector.ultima_zona[int(momento.instante)] = z
            return z

        def _gate(clave: str, valor: str, momento: Any, estado: Any) -> None:
            instante = int(momento.instante)
            toma = zonas._de_la_sesion(estado, momento.sesion).get("toma")
            extra: Any = None
            if clave == RUIDO:
                z = lector.ultima_zona.get(instante)
                if z is not None and toma is not None:
                    extra = (z.lado, int(z.entrada), int(toma["nivel"]))
            elif clave == SUPERAN and toma is not None:
                m1 = momento.datos.m1_entre(toma["instante"] - zonas.LOOKBACK_M1, instante)
                i = next((k for k, v in enumerate(m1) if int(v.fin) == toma["instante"]), None)
                if i is not None and i < len(m1) - 1:
                    extra = zonas_de_control(m1, i, len(m1) - 1, toma["lado"])
            elif clave == VENTANA:
                # un `hecho:` de la forma es SI con cualquier valor fijado (`interprete._hecho`):
                # RN-016 fija `detenido_por_cartuchos=hasta_cartuchos_reinicio`
                extra = tuple(
                    f"{h}={estado.hechos[h]}" for h in DETENIDOS if estado.hechos.get(h) is not None
                )
            lector.gates.setdefault(instante, {})[clave] = (valor, extra)

        def evento(self: Any, reglas: Any, momento: Any, estado: Any) -> Any:
            ev = evento_original(self, reglas, momento, estado)
            lector.cierres.append(
                (
                    int(momento.instante),
                    momento.sesion,
                    list(ev.disparadas),
                    sorted(ev.prohibidos),
                    sorted(ev.bloqueadas),
                )
            )
            return ev

        def evaluar(self: Any, nodo: Any, momento: Any, estado: Any, faltan: Any) -> Any:
            r = evaluar_original(self, nodo, momento, estado, faltan)
            if isinstance(nodo, Mapping) and len(nodo) == 1:
                clave = next(iter(nodo))
                if clave in (RUIDO, SUPERAN, VENTANA):
                    _gate(clave, r.valor.name, momento, estado)
                if clave in PREDICADOS_RN004:
                    instante = int(momento.instante)
                    lector.rn004.setdefault(instante, {})[clave] = r.valor.name
                    # el ultimo de cada cierre, como el valor: en el cierre que abre la sesion,
                    # RN-004 se evalua antes y despues de que RN-003 fije el sesgo
                    lado = prim.LADO_DE_LA_LIQUIDEZ.get(str(estado.hechos.get(prim.HECHO_SESGO)))
                    try:
                        lector.pivote[instante] = (
                            momento.datos.liquidez_m15(instante, lado) if lado else None
                        )
                    except (AttributeError, LookupError):
                        lector.pivote[instante] = None
            return r

        def primitivas_cableadas(registro: Any, ctx: Any, *args: Any, **kwargs: Any) -> Any:
            lector.ctx = ctx
            return primitivas_original(registro, ctx, *args, **kwargs)

        Interprete.evento = evento  # type: ignore[method-assign]
        Interprete.evaluar = evaluar  # type: ignore[method-assign]
        cableado.primitivas_cableadas = primitivas_cableadas  # type: ignore[assignment]
        zonas.zona_del_punto = zona_del_punto  # type: ignore[assignment]


def _precio(puntos: int, escala: int) -> str:
    return str(Decimal(puntos) / escala)


def _instante(d: cv.Dia, minuto: int) -> str:
    return cv.OCULTO if d.antes_del_dia(minuto) else cv.hora(minuto)


def _instante_ms(d: cv.Dia, ms: int) -> str:
    return cv.OCULTO if ms < d.inicio_utc_ms() else cv.hora(ms, es_ms=True)


def _vela(d: cv.Dia, v: Any, escala: int) -> str:
    if d.antes_del_dia(int(v.inicio)):
        return cv.OCULTO
    return (
        f"{cv.hora(int(v.inicio))} O {_precio(int(v.abierta), escala)} H "
        f"{_precio(int(v.maxima), escala)} L {_precio(int(v.minima), escala)} C "
        f"{_precio(int(v.cierre), escala)}"
    )


def main(
    caso: str,
    sesion: str | None,
    con_rn004: bool,
    todos: bool,
    velas_utc: str | None = None,
    con_gates: bool = False,
) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    lector = Lector()
    d = cv.construir(caso, antes_de_correr=lector.instalar)
    iguales, diferencias = cv.ordenes_coinciden(d)
    print(f"CASO {d.caso} · motor visor --simular --caso con las opciones de la corrida 2")
    if not iguales:
        print("ORDENES frente a «### Ordenes» de main: DISTINTAS -> PARADA")
        for linea in diferencias:
            print(f"  {linea}")
        return 3
    n = len(cableado.vida_de_las_ordenes(d.motor))
    print(f"ORDENES frente a «### Ordenes» de main: iguales ({n} ordenes del dia)")
    broker = d.broker
    escala = broker.escala
    limites = d.traza_broker.limites
    for nombre, desde, hasta in limites:
        if sesion is not None and nombre != sesion:
            continue
        print(f"== Sesion {nombre}: de {_instante(d, desde)} a {_instante(d, hasta)} ==")
        traza = d.pagina.resultado.sesiones.get(nombre)
        if traza is not None:
            print(f"  disparadas en la sesion: {', '.join(sorted(traza.disparadas)) or 'ninguna'}")
            print(
                f"  hechos fijados: {len(traza.fijados)}; solo los cambios de valor de cada hecho:"
            )
            ultimo: dict[str, str] = {}
            dimensionada = [(t, v) for t, _, h, v in sorted(traza.fijados) if h == RESUMIDO]
            for t, r, h, v in sorted(traza.fijados):
                if h != RESUMIDO and ultimo.get(h) != v:
                    print(f"    {_instante(d, t)} {r} {h}={v}")
                    ultimo[h] = v
            if dimensionada:
                zonas_ligadas = {v for _, v in dimensionada if v.startswith("zona:")}
                print(
                    f"    {RESUMIDO}: fijado {len(dimensionada)} veces (RN-011 liga una zona, "
                    f"RN-015 lo apaga), de {_instante(d, dimensionada[0][0])} a "
                    f"{_instante(d, dimensionada[-1][0])}; zonas distintas {len(zonas_ligadas)}"
                )
        print(
            "  cierres, en tramos de cierres seguidos iguales (desde - hasta, n | reglas "
            "disparadas | efectos prohibidos | acciones bloqueadas):"
        )
        tramos: list[list[Any]] = []
        for instante, ses, disparadas, prohibidos, bloqueadas in lector.cierres:
            if ses != nombre:
                continue
            if not todos and not (prohibidos or bloqueadas or set(disparadas) - {"RN-003"}):
                continue
            firma = (
                ", ".join(sorted(disparadas)) or "-",
                ", ".join(prohibidos) or "-",
                "; ".join(f"{r}:{a}:{m}" for r, a, m in bloqueadas) or "-",
            )
            if tramos and tramos[-1][2] == firma and tramos[-1][1] == instante - 1:
                tramos[-1][1] = instante
                tramos[-1][3] += 1
            else:
                tramos.append([instante, instante, firma, 1])
        for desde_t, hasta_t, firma, n_t in tramos:
            print(
                f"    {_instante(d, desde_t)} - {_instante(d, hasta_t)}, {n_t} | {firma[0]} | "
                f"{firma[1]} | {firma[2]}"
            )
        if con_rn004:
            print(
                "  RN-004, en tramos de cierres seguidos iguales (desde - hasta, n | alcanza_nivel"
                " / cruza / la_toma_es_de_la_sesion | pivote | extremo de las M1 del tramo"
                " en el lado del pivote: el minimo si es un bajo, el maximo si es un alto):"
            )
            velas = {int(v.inicio): v for v in d.pagina.m1}
            filas_rn004: list[list[Any]] = []
            for instante in sorted(lector.rn004):
                if not (desde <= instante <= hasta):
                    continue
                r = lector.rn004[instante]
                p = lector.pivote.get(instante)
                if p is None:
                    piv = "sin pivote"
                elif d.antes_del_dia(int(p.formado_en)):
                    piv = f"{p.lado}, formado {cv.OCULTO}"
                else:
                    piv = (
                        f"{p.lado} {_precio(int(p.nivel), escala)}, formado "
                        f"{_instante(d, int(p.formado_en))}"
                    )
                firma = (" / ".join(r.get(k, "-") for k in PREDICADOS_RN004), piv)
                ultima = filas_rn004[-1] if filas_rn004 else None
                if ultima is not None and ultima[2] == firma and ultima[1] == instante - 1:
                    filas_rn004[-1][1] = instante
                    filas_rn004[-1][3] += 1
                else:
                    filas_rn004.append([instante, instante, firma, 1, p])
            for desde_t, hasta_t, firma, n_t, p in filas_rn004:
                # la M1 que cierra en el instante t empieza en t - 1
                tramo = [velas[t - 1] for t in range(desde_t, hasta_t + 1) if t - 1 in velas]
                extremo = "-"
                if p is not None and tramo:
                    if p.lado == "bajo":
                        v = min(tramo, key=lambda x: int(x.minima))
                        valor, nombre_e = int(v.minima), "minimo"
                    else:
                        v = max(tramo, key=lambda x: int(x.maxima))
                        valor, nombre_e = int(v.maxima), "maximo"
                    if d.antes_del_dia(int(v.inicio)):
                        extremo = cv.OCULTO
                    else:
                        extremo = (
                            f"{nombre_e} {_precio(valor, escala)} en la M1 de "
                            f"{_instante(d, int(v.inicio))}"
                        )
                print(
                    f"    {_instante(d, desde_t)} - {_instante(d, hasta_t)}, {n_t} | {firma[0]} | "
                    f"{firma[1]} | {extremo}"
                )
        if con_gates:
            tope = d.registro.entero("zonas_control_max_por_esquema")
            print(
                "  gates, en tramos de cierres seguidos iguales (desde - hasta, n | RN-005 "
                "se_desarrolla_en_el_lado_de_ruido: valor, lado y 0 de la zona frente al nivel de "
                "la toma | RN-009 zonas_desarrolladas_superan: valor, zonas de control "
                f"(tope {tope}) | RN-001 en_ventana: valor, hechos detenido_por_* fijados):"
            )
            filas_g: list[list[Any]] = []
            for instante in sorted(lector.gates):
                if not (desde <= instante <= hasta):
                    continue
                g = lector.gates[instante]
                ruido = g.get(RUIDO)
                if ruido is None:
                    t_ruido = "-"
                elif ruido[1] is None:
                    t_ruido = f"{ruido[0]}, sin zona o sin toma"
                else:
                    lado, entrada, nivel = ruido[1]
                    rel = ">" if entrada > nivel else ("<" if entrada < nivel else "=")
                    t_ruido = (
                        f"{ruido[0]}, {lado} 0 {_precio(entrada, escala)} {rel} toma "
                        f"{_precio(nivel, escala)}"
                    )
                sup = g.get(SUPERAN)
                n_zc = "-" if sup is None or sup[1] is None else sup[1]
                t_sup = "-" if sup is None else f"{sup[0]}, {n_zc}"
                ven = g.get(VENTANA)
                t_ven = "-" if ven is None else f"{ven[0]}, {', '.join(ven[1]) or 'ninguno'}"
                firma = (t_ruido, t_sup, t_ven)
                ultima = filas_g[-1] if filas_g else None
                if ultima is not None and ultima[2] == firma and ultima[1] == instante - 1:
                    ultima[1] = instante
                    ultima[3] += 1
                else:
                    filas_g.append([instante, instante, firma, 1])
            for desde_t, hasta_t, firma, n_t in filas_g:
                print(
                    f"    {_instante(d, desde_t)} - {_instante(d, hasta_t)}, {n_t} | "
                    + " | ".join(firma)
                )
        # las ordenes de la sesion, con su zona y el punto
        ctx = lector.ctx
        mem = zonas._de_la_sesion(d.estado, nombre)
        punto_de_zona = mem.get("punto_de_zona", {})
        rechazados = mem.get("rechazados", set())
        zonas_dia = zonas.zonas_del_dia(d.estado)
        filas = [
            f for f in cableado.vida_de_las_ordenes(d.motor) if f[1] == nombre and f[0] == d.clave
        ]
        print("  ordenes de la sesion:")
        if not filas:
            print("    ninguna")
        for f in filas:
            o = broker.ordenes[f[2]]
            zid = ctx.zona_de_orden.get(o.id) if ctx is not None else None
            z = zonas_dia.get(zid) if zid else None
            zona = "-"
            if z is not None:
                zona = (
                    f"{zid} (0 {_precio(z.entrada, escala)}, 1 {_precio(z.extremo, escala)}, "
                    f"bloque desde {_instante(d, z.desde) if z.desde is not None else '-'}, "
                    f"formada {_instante(d, z.formada) if z.formada is not None else '-'}, "
                    f"punto {punto_de_zona.get(zid, '-')})"
                )
            print(
                f"    {o.id} {o.tipo} {o.lado} | colocada {_instante_ms(d, o.colocada_ms)} | "
                f"0 {_precio(o.precio, escala)} stop {_precio(o.stop, escala)} objetivo "
                f"{_precio(o.objetivo, escala)} | {f[5]} {f[6]} | zona {zona}"
            )
        if rechazados:
            print(f"  puntos rechazados en la sesion (ADR-0064, decision 1): {sorted(rechazados)}")
            for f in filas:
                o = broker.ordenes[f[2]]
                zid = ctx.zona_de_orden.get(o.id) if ctx is not None else None
                if zid and punto_de_zona.get(zid) in rechazados and f[5] != "rechazada":
                    print(f"    {o.id} se coloco con un punto ya rechazado: SI")
        # el pivote del 0: la vela que marca el nivel y sus vecinas, para ver que es un pivote
        vistas: set[str] = set()
        for f in filas:
            o = broker.ordenes[f[2]]
            zid = ctx.zona_de_orden.get(o.id) if ctx is not None else None
            z = zonas_dia.get(zid) if zid else None
            if z is None or z.desde is None or zid in vistas:
                continue
            vistas.add(zid)
            m1 = d.pagina.m1
            idx = next((i for i, v in enumerate(m1) if int(v.inicio) == z.desde), None)
            if idx is None:
                continue
            print(f"  la vela que marca el 0 de {zid} y sus vecinas (dos a cada lado):")
            for v in m1[max(idx - 2, 0) : idx + 3]:
                marca = " <- marca" if int(v.inicio) == z.desde else ""
                print(f"    {_vela(d, v, escala)}{marca}")
    if velas_utc:
        # `--velas HH:MM-HH:MM`: las M1 del dia dev que EMPIEZAN en ese tramo UTC, ambos incluidos
        a_txt, b_txt = velas_utc.split("-")
        base = d.inicio_utc_ms() // MS_POR_MINUTO
        a_min = base + int(a_txt[:2]) * 60 + int(a_txt[3:5])
        b_min = base + int(b_txt[:2]) * 60 + int(b_txt[3:5])
        print(f"== M1 del dia dev que empiezan de {a_txt}Z a {b_txt}Z ==")
        for v in d.pagina.m1:
            if a_min <= int(v.inicio) <= b_min:
                print(f"    {_vela(d, v, escala)}")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("caso")
    p.add_argument("--sesion")
    p.add_argument("--rn004", action="store_true")
    p.add_argument("--todos-los-cierres", action="store_true")
    p.add_argument("--velas", help="HH:MM-HH:MM en UTC del dia dev")
    p.add_argument("--gates", action="store_true")
    a = p.parse_args()
    raise SystemExit(main(a.caso, a.sesion, a.rn004, a.todos_los_cierres, a.velas, a.gates))
