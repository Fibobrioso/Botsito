"""La caja de las 77 (docs/validation/CAJA-77.md): R1 a R6 de BLOQUE-DE-LA-CAJA.md §1.4 frente a la
caja del trader reconstruida desde el libro -el 0 en la entrada, el 1 desde el stop leido como el
0,8 o como el 1-, sobre las operaciones de los dias `dev` de abril y agosto de 2026.

MEDICION con el criterio pre-registrado en CAJA-77.md §1 (y su nota §1.8): no cambia el motor, el
productor ni la spec. Las reglas son las funciones `r1` a `r6` de `scripts/bloque_de_la_caja.py`,
importadas sin tocarlas. Solo lee el repositorio y escribe SOLO en --salida.

    uv run python scripts/caja_77.py --salida <fichero> [--raiz <repo>]
"""

from __future__ import annotations

import argparse
import bisect
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))
sys.path.insert(0, str(RAIZ_SCRIPT / "scripts"))

import bloque_de_la_caja as bc  # noqa: E402

from botsito.domain.estructura_m1 import COMPRA, VENTA  # noqa: E402
from botsito.domain.velas import Vela  # noqa: E402

MESES = ("2026-04", "2026-08")
VELAS = {"2026-04": "eurusd-m1-2026-04-990211bd", "2026-08": "eurusd-m1-2026-08-0d42230e"}
TICKS = {"2026-04": "eurusd-ticks-2026-04-1d189bdd", "2026-08": "eurusd-ticks-2026-08-75bd3a08"}
ESPERADAS = 77
ESCALA = 100_000
VENTANA_MIN = 90
TAU = 2
TAUS = (1, 2, 3)
DESFASE = -2  # la mediana +2 de OANDA sobre Dukascopy (BLOQUE-DE-LA-CAJA.md §2.3), restada
UMBRAL = Fraction(40, 100)
LECTURAS = ("L0,8", "L1")
REGLAS: Mapping[str, Callable[[Sequence[Vela], str], tuple[int, int] | None]] = bc.REGLAS
SPREAD_VENTANA_MS = 60_000

# El control (§1.8.2): las cajas de BLOQUE-DE-LA-CAJA con pareja en el libro (SESION-02-VIDEO.md
# §4, ADR-0043), con el dia y el instante UTC del caso emparejado tal como los da esa tabla.
PAREJAS = {
    "v7-2": ("2026-08-03", "06:03:05"),
    "v7-3": ("2026-08-03", "06:07:40"),
    "v7-5": ("2026-08-03", "09:46:15"),
    "v7-11": ("2026-08-04", "11:34:50"),
    "v7-15": ("2026-08-06", "06:07:25"),
}
# v7-2: la caja que el trader dejo (BLOQUE-DE-LA-CAJA.md §5.3); la de §2.2 se da tambien
CAJA_V7_2_BUENA = ("1.15364", "1.15380")


def puntos(precio: object) -> int:
    return int((Decimal(str(precio)) * ESCALA).to_integral_value())


@dataclass(frozen=True)
class Op:
    caso: str
    dia: str
    t: datetime
    lado: str
    entrada: int
    stop: int

    @property
    def mes(self) -> str:
        return self.dia[:7]

    @property
    def minuto(self) -> int:
        return int(self.t.timestamp() // 60)

    def fuera(self) -> str | None:
        if self.lado not in (VENTA, COMPRA):
            return f"direccion {self.lado!r}"
        if self.lado == VENTA and self.stop <= self.entrada:
            return "stop del lado equivocado o en la entrada (venta)"
        if self.lado == COMPRA and self.stop >= self.entrada:
            return "stop del lado equivocado o en la entrada (compra)"
        return None

    def caja(self, lectura: str) -> tuple[Fraction, Fraction]:
        """El 0 y el 1 del trader: el 0 en la entrada; el 1 desde el stop (§1.2)."""
        cero = Fraction(self.entrada)
        if lectura == "L1":
            return cero, Fraction(self.stop)
        return cero, cero + (Fraction(self.stop) - cero) * Fraction(5, 4)


# ----------------------------------------------------------------------------------- lectura


def cargar_operaciones(raiz: Path) -> tuple[list[Op], int]:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.holdout import casos_ocultos, casos_reservados
    from botsito.cases.ingesta import DIRECTORIO_DEV
    from botsito.comun.yaml_estricto import leer_yaml
    from botsito.engine import arnes

    reservados, ocultos = casos_reservados(raiz), casos_ocultos(raiz)
    dias = arnes.dias_de_construccion(raiz, cargar_criterio(raiz), MESES, ocultos=ocultos)
    vetados = sum(1 for d in dias if d.id in reservados or d.id in ocultos)
    if vetados:
        raise SystemExit(f"PARADA: {vetados} dias de construccion reservados u ocultos")
    ops: list[Op] = []
    for d in dias:
        ruta = raiz / DIRECTORIO_DEV / f"{d.id}.yaml"
        if not ruta.exists():
            continue
        for o in leer_yaml(ruta).get("operaciones") or []:
            t = datetime.fromisoformat(str(o["instante_utc"]).replace("Z", "+00:00"))
            ops.append(
                Op(d.id, d.dia, t.astimezone(UTC), str(o["direccion"]), puntos(o["entrada"]),
                   puntos(o["stop"]))
            )  # fmt: skip
    return sorted(ops, key=lambda o: (o.t, o.caso)), len(dias)


def cargar_velas(raiz: Path) -> list[Vela]:
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_ventana

    todas: list[Vela] = []
    for mes in MESES:
        m = cargar_manifiesto(buscar_manifiesto(raiz, VELAS[mes]))
        if int(m["escala"]) != ESCALA:
            raise SystemExit(f"{VELAS[mes]}: escala {m['escala']} != {ESCALA}")
        todas += list(cargar_ventana(m, carpeta_datos(raiz)).velas)
    return sorted(todas, key=lambda v: int(v.inicio))


def spreads(raiz: Path, compras: Sequence[Op]) -> dict[str, int | None]:
    """ask - bid del ultimo tick en [T - 60 s, T] de cada compra (§1.8.3)."""
    from botsito.config.ajustes import carpeta_datos
    from botsito.data.ticks import buscar_manifiesto_ticks, cargar_manifiesto_ticks, cargar_ticks

    salida: dict[str, int | None] = {}
    for o in compras:
        m = cargar_manifiesto_ticks(buscar_manifiesto_ticks(raiz, TICKS[o.mes]))
        ms = int(o.t.timestamp() * 1000)
        serie = cargar_ticks(m, carpeta_datos(raiz), ms - SPREAD_VENTANA_MS, ms + 1)
        salida[clave(o)] = (
            int(serie.ticks[-1].ask) - int(serie.ticks[-1].bid) if serie.ticks else None
        )
    return salida


def clave(o: Op) -> str:
    return f"{o.dia} {o.t:%H:%M:%S} {o.lado}"


def ventana(inicios: list[int], velas: list[Vela], minuto_t: int) -> list[Vela]:
    """Las M1 cerradas en [T - 90 min, minuto de T): la vela en curso en T no entra (§1.3)."""
    a = bisect.bisect_left(inicios, minuto_t - VENTANA_MIN)
    b = bisect.bisect_left(inicios, minuto_t)
    return velas[a:b]


# ------------------------------------------------------------------------------------- medida


@dataclass
class Fila:
    op: Op
    cajas: dict[str, tuple[int, int] | None]  # regla -> (0, 1) o None


def acierta(
    caja: tuple[int, int] | None, t0: Fraction, t1: Fraction, tau: int
) -> tuple[bool, bool] | None:
    if caja is None:
        return None
    return abs(caja[0] - t0) <= tau, abs(caja[1] - t1) <= tau


def niveles(o: Op, lectura: str, desfase: int, spread: int | None) -> tuple[Fraction, Fraction]:
    cero, uno = o.caja(lectura)
    resta = spread if (o.lado == COMPRA and spread is not None) else 0
    ajuste = desfase - resta
    return cero + ajuste, uno + ajuste


def recuento(
    filas: Sequence[Fila], lectura: str, tau: int, desfase: int,
    spread: dict[str, int | None] | None = None,
) -> dict[str, dict[str, int]]:  # fmt: skip
    salida = {r: {"acierta": 0, "solo_0": 0, "solo_1": 0, "sin_caja": 0, "n": 0} for r in REGLAS}
    for f in filas:
        s = None if spread is None else spread.get(clave(f.op))
        t0, t1 = niveles(f.op, lectura, desfase, s)
        for r in REGLAS:
            c = salida[r]
            c["n"] += 1
            a = acierta(f.cajas[r], t0, t1, tau)
            if a is None:
                c["sin_caja"] += 1
            elif a[0] and a[1]:
                c["acierta"] += 1
            elif a[0]:
                c["solo_0"] += 1
            elif a[1]:
                c["solo_1"] += 1
    return salida


def pct(a: int, n: int) -> str:
    return f"{a}/{n} ({100 * a / n:.0f} %)" if n else "0/0"


def tabla(titulo: str, filas: Sequence[Fila], tau: int, desfase: int,
          spread: dict[str, int | None] | None = None) -> list[str]:  # fmt: skip
    salida = [
        f"### {titulo}  (n = {len(filas)}; tau {tau}; desfase {desfase:+d})",
        "| regla | L0,8 acierta | solo 0 | solo 1 | sin caja "
        "| L1 acierta | solo 0 | solo 1 | sin caja |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    por = {lec: recuento(filas, lec, tau, desfase, spread) for lec in LECTURAS}
    for r in REGLAS:
        celdas = []
        for lec in LECTURAS:
            c = por[lec][r]
            celdas += [pct(c["acierta"], c["n"]), str(c["solo_0"]), str(c["solo_1"]),
                       str(c["sin_caja"])]  # fmt: skip
        salida.append(f"| {r} | " + " | ".join(celdas) + " |")
    return [*salida, ""]


def veredicto(filas: Sequence[Fila]) -> list[str]:
    """§1.8.1 sobre la celda principal: tau 2, sin correccion."""
    n = len(filas)
    salida = ["## VEREDICTO (umbral pre-registrado, CAJA-77.md §1.8.1)", ""]
    sostenidas = []
    for r in REGLAS:
        partes = []
        ok = False
        for lec in LECTURAS:
            a = recuento(filas, lec, TAU, 0)[r]["acierta"]
            partes.append(f"{lec} {pct(a, n)}")
            ok = ok or (n > 0 and Fraction(a, n) >= UMBRAL)
        if ok:
            sostenidas.append(r)
        salida.append(f"- {r}: {'; '.join(partes)} -> {'SOSTENIDA' if ok else 'no llega al 40 %'}")
    salida.append("")
    iguales = [f for f in filas if f.cajas["R1"] == f.cajas["R4"]]
    distintas = [f for f in filas if f.cajas["R1"] != f.cajas["R4"]]
    salida.append(
        f"R1 y R4: dan la MISMA caja en {len(iguales)} operaciones y DISTINTA en {len(distintas)}"
    )
    for nombre, grupo in (("misma caja", iguales), ("caja distinta", distintas)):
        for lec in LECTURAS:
            c = recuento(grupo, lec, TAU, 0)
            salida.append(
                f"  {nombre}, {lec}: R1 acierta {pct(c['R1']['acierta'], len(grupo))}; "
                f"R4 acierta {pct(c['R4']['acierta'], len(grupo))}"
            )
    for lec in LECTURAS:
        c = recuento(distintas, lec, TAU, 0)
        a1, a4 = c["R1"]["acierta"], c["R4"]["acierta"]
        if a1 >= 1 and a1 >= 2 * a4:
            quien = "gana R1"
        elif a4 >= 1 and a4 >= 2 * a1:
            quien = "gana R4"
        else:
            quien = "sin decidir (ninguna llega al doble de la otra)"
        salida.append(f"R1 frente a R4 en las distintas, {lec}: {a1} frente a {a4} -> {quien}")
    salida.append("")
    salida.append(
        "RESULTADO: "
        + (
            f"SOSTENIDAS {', '.join(sostenidas)}"
            if sostenidas
            else "NO DECIDE: la pregunta va a la sesion 4"
        )
    )
    return [*salida, ""]


def detalle(filas: Sequence[Fila]) -> list[str]:
    salida = [
        "## DETALLE, operacion a operacion (tau 2, sin correccion). Celda: regla - trader, "
        "en el 0 / en el 1 (L0,8 | L1); «—»: la regla no da caja",
        "| op | dir | 0 | 1 L0,8 | 1 L1 | " + " | ".join(REGLAS) + " |",
        "|---|---|---|---|---|" + "---|" * len(REGLAS),
    ]
    for f in filas:
        t0, u08 = f.op.caja("L0,8")
        _, u1 = f.op.caja("L1")
        celdas = []
        for r in REGLAS:
            c = f.cajas[r]
            if c is None:
                celdas.append("—")
                continue
            celdas.append(
                f"{float(c[0] - t0):+.0f} / {float(c[1] - u08):+.2f} | {float(c[1] - u1):+.0f}"
            )
        salida.append(
            f"| {clave(f.op)} | {f.op.lado} | {f.op.entrada} | {float(u08):.2f} | {f.op.stop} | "
            + " | ".join(celdas)
            + " |"
        )
    return [*salida, ""]


# ------------------------------------------------------------------------------------- control


def _dif(x: tuple[int, int] | None, p0: int, p1: int) -> str:
    return "—" if x is None else f"{x[0] - p0:+d} / {x[1] - p1:+d}"


def control(ops: Sequence[Op], inicios: list[int], velas: list[Vela]) -> list[str]:
    por_clave = {(o.dia, f"{o.t:%H:%M:%S}"): o for o in ops}
    cajas = {c.op: c for c in bc.CAJAS}
    salida = [
        "## CONTROL DE LA RECONSTRUCCION (CAJA-77.md §1.8.2), antes del resultado principal",
        "Cajas de BLOQUE-DE-LA-CAJA.md con pareja en el libro (SESION-02-VIDEO.md §4). Niveles y "
        "hora "
        "de colocacion: los que ese informe ya leyo; ningun fotograma nuevo.",
        "",
        "### (a) La caja reconstruida desde el libro frente a la leida en pantalla "
        "(reconstruida - leida)",
        "| caja | libro: entrada / stop | pantalla: 0 / 1 | L0,8: 0 / 1 | L1: 0 / 1 |",
        "|---|---|---|---|---|",
    ]
    filas_b: list[str] = []
    for op, (dia, hms) in PAREJAS.items():
        o = por_clave.get((dia, hms))
        c = cajas[op]
        if o is None:
            salida.append(f"| {op} | SIN PAREJA en los casos ({dia} {hms}) | | | |")
            continue
        leidas = [(c.puntos(c.cero), c.puntos(c.uno), "")]
        if op == "v7-2":
            leidas = [
                (puntos(CAJA_V7_2_BUENA[0]), puntos(CAJA_V7_2_BUENA[1]), " (la que dejo, §5.3)"),
                (c.puntos(c.cero), c.puntos(c.uno), " (la primera, §2.2)"),
            ]
        for p0, p1, nota in leidas:
            r08, r1 = o.caja("L0,8"), o.caja("L1")
            salida.append(
                f"| {op}{nota} | {o.entrada} / {o.stop} | {p0} / {p1} | "
                f"{float(r08[0] - p0):+.0f} / {float(r08[1] - p1):+.2f} | "
                f"{float(r1[0] - p0):+.0f} / {float(r1[1] - p1):+.0f} |"
            )
        p0, p1 = leidas[0][0], leidas[0][1]
        col = int(c.t_utc.timestamp() // 60)
        v_llenado = ventana(inicios, velas, o.minuto)
        v_colocacion = ventana(inicios, velas, col)
        for r, f in REGLAS.items():
            a, b = f(v_llenado, VENTA), f(v_colocacion, VENTA)
            entre = "—" if a is None or b is None else f"{a[0] - b[0]:+d} / {a[1] - b[1]:+d}"
            filas_b.append(f"| {op} | {r} | {_dif(a, p0, p1)} | {_dif(b, p0, p1)} | {entre} |")
    salida += [
        "",
        "### (b) Las reglas ancladas en el LLENADO del libro frente a la COLOCACION leida",
        "Celdas «regla - caja leida» en el 0 / en el 1, y la diferencia llenado - colocacion.",
        "| caja | regla | anclada en el llenado | anclada en la colocacion "
        "| llenado - colocacion |",
        "|---|---|---|---|---|",
        *filas_b,
        "",
    ]
    return salida


# --------------------------------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--salida", required=True, type=Path)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    args = p.parse_args(argv)
    raiz = args.raiz.resolve()
    ops, n_dias = cargar_operaciones(raiz)
    if len(ops) != ESPERADAS:
        print(f"PARADA: {len(ops)} operaciones en {n_dias} dias, se esperaban {ESPERADAS}")
        return 3
    velas = cargar_velas(raiz)
    inicios = [int(v.inicio) for v in velas]
    fuera: list[str] = []
    filas: list[Fila] = []
    for o in ops:
        motivo = o.fuera()
        v = ventana(inicios, velas, o.minuto)
        if motivo is None and not v:
            motivo = "sin velas M1 en la ventana"
        if motivo is not None:
            fuera.append(f"- {clave(o)}: {motivo}")
            continue
        filas.append(Fila(o, {r: f(v, o.lado) for r, f in REGLAS.items()}))
    compras = [f.op for f in filas if f.op.lado == COMPRA]
    sp = spreads(raiz, compras)
    lineas = [
        "# La caja de las 77 (criterio en docs/validation/CAJA-77.md §1 y §1.8)",
        f"OPERACIONES: {len(ops)} en {n_dias} dias dev de {', '.join(MESES)}; 0 dias reservados u "
        f"ocultos; evaluables {len(filas)}; fuera {len(fuera)}",
        f"VELAS: {', '.join(VELAS.values())} (Dukascopy, BID, UTC); "
        f"ventana [T - {VENTANA_MIN} min, "
        "minuto de T), la vela en curso en T no entra",
        "",
        *(["## FUERA", *fuera, ""] if fuera else []),
        *control(ops, inicios, velas),
        "## RESULTADO PRINCIPAL (tau 2, sin correccion)",
        "",
        *tabla("Todas", filas, TAU, 0),
        *veredicto(filas),
        "## SENSIBILIDADES (no deciden)",
        "",
    ]
    for tau in TAUS:
        if tau != TAU:
            lineas += tabla(f"Todas, tau {tau}", filas, tau, 0)
    for tau in TAUS:
        lineas += tabla(f"Todas, desfase -2, tau {tau}", filas, tau, DESFASE)
    for lado in (VENTA, COMPRA):
        grupo = [f for f in filas if f.op.lado == lado]
        lineas += tabla(f"Solo {lado}s", grupo, TAU, 0)
        lineas += tabla(f"Solo {lado}s, desfase -2", grupo, TAU, DESFASE)
    for mes in MESES:
        grupo = [f for f in filas if f.op.mes == mes]
        lineas += tabla(f"Solo {mes}", grupo, TAU, 0)
        lineas += tabla(f"Solo {mes}, desfase -2", grupo, TAU, DESFASE)
    con_spread = [f for f in filas if f.op.lado == COMPRA and sp.get(clave(f.op)) is not None]
    sin = sum(1 for f in filas if f.op.lado == COMPRA and sp.get(clave(f.op)) is None)
    valores = sorted(v for v in sp.values() if v is not None)
    lineas += [
        f"### Spread de las compras en T (ticks): {len(valores)} con tick, {sin} sin spread; "
        + (
            f"mediana {valores[len(valores) // 2]}, min {valores[0]}, max {valores[-1]} puntos"
            if valores
            else "ninguno"
        ),  # fmt: skip
        "",
        *tabla("Compras con tick, sin restar el spread", con_spread, TAU, 0),
        *tabla("Compras con tick, restando el spread en T", con_spread, TAU, 0, sp),
        *detalle(filas),
    ]
    args.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
