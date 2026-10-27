"""RECORRIDA-CONSTRUCCION §2.8 (respuesta del consultor a la PARADA 2, punto 1): las llenadas de la
corrida 2 cuyo R se aparta mas de 0,25 del que da su motivo sin costes, las sesiones con mas de 4
llenadas, y el censo de los eventos del respaldo M1 de las dos corridas.

Solo LEE las salidas commiteadas de esta carpeta y los TICKS de los dias dev de construccion, en
ventanas de un minuto alrededor de cada evento, por los cargadores del repositorio
(`data.ticks.cargar_ticks`). No corre el motor, no lee el calentamiento ni ninguna vela anterior al
dia dev, y no imprime nada anterior a las 00:00Z del dia al que pertenece.

R esperado sin costes (el del consultor): stop -1; stop tras moverlo a break even 0; objetivo
+3,75 (3 veces la caja del 0 al 1 sobre el riesgo del 0 al 0,8); manual, ninguno (se listan aparte).
El R de las salidas es por PRECIO, sobre el riesgo con el que nacio la posicion (su stop original)
y desde el precio de llenado: no lleva la comision; la comision va en su propia columna, en R.

    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/costes_y_sesiones.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import ROUND_DOWN, ROUND_UP, Decimal
from pathlib import Path
from typing import Any

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[3]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(AQUI))

from horas_perdidas import HORAS_PERDIDAS  # noqa: E402  (la copia de esta carpeta)

from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.data.ticks import (  # noqa: E402
    buscar_manifiesto_ticks,
    cargar_manifiesto_ticks,
    cargar_ticks,
)

DIARIA = AQUI / "diaria.DIAGNOSTICO.cuenta=diaria.txt"
ARRASTRADA = AQUI / "cuenta-arrastrada.txt"
ENTRADAS = AQUI / "entradas-antes-alternancia.txt"
ROTULO = "[DIAGNOSTICO"
ESCALA = 100_000
MS_MIN = 60_000
UMBRAL = Decimal("0.25")
R_STOP, R_BE, R_OBJ = Decimal(-1), Decimal(0), Decimal("3.75")
# los parametros con los que corrio la rama (parametros.yaml y el perfil), escritos aqui solo para
# explicar el redondeo y la comision; ninguno decide nada en este guion
FRACCION_STOP = Decimal("0.8")  # stop_fraccion_caja
MULTIPLO_OBJ = Decimal(3)  # objetivo_rr, sobre la caja completa (base_calculo_objetivo)
COMISION_REDONDA_POR_LOTE = Decimal(10)  # firma_comision_usd_por_lote 5, por lado (los dos)
USD_POR_PUNTO_Y_LOTE = Decimal(1)  # instrumento_contrato 100000 / escala 100000
SESIONES_LLENAS = 4  # «mas de 4 llenadas»


def sin_rotulo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def lineas(ruta: Path) -> list[str]:
    return [sin_rotulo(ln) for ln in ruta.read_text(encoding="utf-8").splitlines()]


def ms_de(iso: str) -> int:
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


def precio(p: int) -> str:
    return f"{Decimal(p) / ESCALA:.5f}"


def puntos(texto: str) -> int:
    return int((Decimal(texto) * ESCALA).to_integral_value())


def hora(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, UTC).strftime("%H:%M:%S.%f")[:-3] + "Z"


@dataclass
class Orden:
    dia: str
    sesion: str
    id: str
    colocada_ms: int
    precio: int
    resultado: str
    lote: Decimal
    distancia: int
    riesgo: Decimal | None
    limite: str
    punto: str
    caja1: int | None


@dataclass
class Evento:
    ms: int
    tipo: str
    id: str
    fuente: str


def leer_salida(ls: list[str]) -> tuple[dict[tuple[str, str], Orden], dict[str, list[Evento]]]:
    """«### Ordenes» por (dia, id) y «### Eventos del broker» por dia."""
    ordenes: dict[tuple[str, str], Orden] = {}
    eventos: dict[str, list[Evento]] = defaultdict(list)
    seccion = ""
    for ln in ls:
        if ln.startswith("### "):
            seccion = ln
            continue
        if not ln.startswith("20"):
            continue
        p = ln.split(" | ")
        if seccion.startswith("### Ordenes ("):
            ordenes[(p[0], p[2])] = Orden(
                p[0], p[1], p[2], ms_de(p[3]), puntos(p[4]), p[5], Decimal(p[8]), int(p[9]),
                None if p[12] == "-" else Decimal(p[12]), p[14], p[15],
                None if p[16] == "-" else puntos(p[16]),
            )  # fmt: skip
        elif seccion.startswith("### Eventos del broker"):
            eventos[p[0]].append(Evento(ms_de(p[1]), p[2], p[3], p[4]))
    return ordenes, eventos


@dataclass
class Llenada:
    dia: str
    sesion: str
    orden: str
    lado: str
    llenada_ms: int
    entrada: int
    donde: str
    punto: str
    escenario: str
    r: Decimal
    motivo: str
    pareja: str


def leer_entradas() -> list[Llenada]:
    salida: list[Llenada] = []
    dentro = False
    for ln in ENTRADAS.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## Todas las llenadas"):
            dentro = True
            continue
        if dentro and ln.startswith("20"):
            p = ln.split(" | ")
            r_txt, _, motivo = p[12].partition(" (")
            salida.append(
                Llenada(
                    p[0],
                    p[1],
                    p[2],
                    p[3],
                    ms_de(p[4]),
                    puntos(p[5]),
                    p[8],
                    p[9],
                    p[11],
                    Decimal(r_txt),
                    motivo.rstrip(")"),
                    p[13],
                )  # fmt: skip
            )
    return salida


class Ticks:
    """Los ticks de un instante, por los cargadores del repo, en ventanas de un minuto del dia."""

    def __init__(self) -> None:
        self.carpeta = carpeta_datos(RAIZ)
        self.manifiestos: dict[str, dict[str, Any]] = {}

    def _manifiesto(self, mes: str) -> dict[str, Any]:
        if mes not in self.manifiestos:
            ruta = buscar_manifiesto_ticks(RAIZ, f"eurusd-ticks-{mes}")
            self.manifiestos[mes] = cargar_manifiesto_ticks(ruta)
        return self.manifiestos[mes]

    def horas(self, mes: str) -> tuple[int, ...]:
        return tuple(int(h) for h in self._manifiesto(mes)["seleccion"]["horas_utc"])

    def en(self, dia: str, ms: int) -> Any | None:
        """El tick de `ms` exacto, o el ultimo anterior dentro del mismo minuto; None si no hay."""
        serie = cargar_ticks(self._manifiesto(dia[:7]), self.carpeta, ms - MS_MIN, ms + 1)
        previos = [t for t in serie.ticks if int(t.instante) <= ms]
        return previos[-1] if previos else None


def r_teorico_objetivo(caja: int) -> Decimal:
    """El R del objetivo con el llenado en el 0 y el objetivo exacto: el stop se redondea alejandose
    (`stop_fraccion_redondeo`) y el objetivo hacia abajo (`fijar_objetivo`)."""
    d = int((Decimal(caja) * FRACCION_STOP).to_integral_value(ROUND_UP))
    o = int((Decimal(caja) * MULTIPLO_OBJ).to_integral_value(ROUND_DOWN))
    return (Decimal(o) / Decimal(d)).quantize(Decimal("0.01"))


def clasificar_respaldo(dia: str, ms: int, horas_mes: tuple[int, ...]) -> str:
    """El evento del respaldo sella en el CIERRE de su vela: la vela es el minuto anterior."""
    vela = datetime.fromtimestamp((ms - 1) / 1000, UTC)
    clave = f"{dia}T{vela.hour:02d}Z"
    if clave in HORAS_PERDIDAS:
        return "hora perdida"
    if vela.hour not in horas_mes:
        return "fuera de la cobertura de ticks (el minuto antes de la ventana)"
    return "otro"


def parte_a(
    llenadas: list[Llenada],
    ordenes: dict[tuple[str, str], Orden],
    eventos: dict[str, list[Evento]],
    ticks: Ticks,
) -> list[str]:
    salida = [
        "## a) Llenadas de la corrida 2 con |R - R esperado| > 0,25",
        "dia | sesion | orden | lado | motivo | R | R esperado | desviacion | caja (pt) | "
        "stop (pt) | R teorico (llenado en el 0) | llenado: fuente, deslizamiento (pt), spread "
        "(pt) | salida: fuente, precio, salto sobre su nivel (pt) | limite del lote | comision "
        "en R | causa | comprobacion del R | regla aplicada como esta escrita",
    ]
    manuales: list[str] = []
    resumen: Counter[str] = Counter()
    for ll in llenadas:
        o = ordenes[(ll.dia, ll.orden)]
        evs = eventos[ll.dia]
        pos = f"pos-{ll.orden}"
        llen = next(e for e in evs if e.tipo == "llenada" and e.id == ll.orden)
        movido = [e for e in evs if e.tipo == "stop_movido" and e.id == pos]
        sal = next(e for e in evs if e.id == pos and e.tipo in ("stop", "objetivo", "manual"))
        compra = ll.lado == "compra"
        sentido = 1 if compra else -1
        if ll.motivo == "manual":
            manuales.append(f"{ll.dia} | {ll.sesion} | {ll.orden} | {ll.lado} | R {ll.r:+.2f}")
            continue
        esperado = R_OBJ if ll.motivo == "objetivo" else (R_BE if movido else R_STOP)
        desviacion = ll.r - esperado
        if abs(desviacion) <= UMBRAL:
            continue
        caja = abs(o.precio - o.caja1) if o.caja1 is not None else 0
        stop0 = o.precio - sentido * o.distancia
        objetivo = o.precio + sentido * int(
            (Decimal(caja) * MULTIPLO_OBJ).to_integral_value(ROUND_DOWN)
        )
        nivel = {"objetivo": objetivo, "stop": ll.entrada if movido else stop0}[ll.motivo]
        desliz = sentido * (ll.entrada - o.precio)
        t_ll = ticks.en(ll.dia, llen.ms) if llen.fuente == "ticks" else None
        spread = f"{int(t_ll.ask) - int(t_ll.bid)}" if t_ll is not None else "-"
        if sal.fuente == "ticks":
            t_sal = ticks.en(ll.dia, sal.ms)
            assert t_sal is not None
            px_sal = int(t_sal.bid) if compra else int(t_sal.ask)
            if ll.motivo == "objetivo":
                px_sal = objetivo  # el objetivo se llena a su precio (llenado.primera_salida)
        else:
            riesgo = abs(ll.entrada - stop0)
            px_sal = ll.entrada + int((ll.r * riesgo).to_integral_value()) * sentido
        salto = sentido * (nivel - px_sal)  # puntos peor que el nivel (positivo = peor)
        teor = r_teorico_objetivo(caja) if ll.motivo == "objetivo" else esperado
        com_r = (
            COMISION_REDONDA_POR_LOTE / (Decimal(o.distancia) * USD_POR_PUNTO_Y_LOTE)
        ).quantize(Decimal("0.01"))
        horas_mes = ticks.horas(ll.dia[:7])
        causas: list[str] = []
        tipos: set[str] = set()
        aplicada = "si"
        evidencia = ""
        if llen.fuente == "respaldo_m1":
            donde = clasificar_respaldo(ll.dia, llen.ms, horas_mes)
            misma_vela = o.colocada_ms == llen.ms - 1
            causas.append(
                f"llenado con el respaldo M1 ({donde}"
                + ("; con la M1 cuyo cierre coloco la orden" if misma_vela else "")
                + ")"
            )
            if misma_vela:
                aplicada = "NO"
                evidencia = (
                    "la orden se evalua contra la M1 cuyo cierre la coloco, cuyos precios son "
                    "todos anteriores a la orden; ADR-0051 §2 dice que una orden no se evalua "
                    "contra el tick en que se decidio, solo contra los posteriores, y el respaldo "
                    "de §5 no lo excluye por escrito"
                )
                if donde.startswith("fuera"):
                    evidencia += (
                        "; y no es una hora perdida: es el borde de la cobertura de ticks, y §8 "
                        "deja el respaldo para depurar y para las horas perdidas"
                    )
                tipos.add("respaldo M1 con la vela que decidio la orden")
            else:
                tipos.add("respaldo M1")
        if sal.fuente == "respaldo_m1":
            causas.append(
                f"salida con el respaldo M1 ({clasificar_respaldo(ll.dia, sal.ms, horas_mes)})"
            )
            tipos.add("respaldo M1")
        if ll.motivo == "objetivo" and abs(teor - R_OBJ) > Decimal("0.05"):
            causas.append(f"redondeo de una caja de {caja} pt (stop alejandose, objetivo abajo)")
            tipos.add("redondeo de una caja pequena")
        if desliz > 0:
            causas.append(f"el tick que llena la orden stop llega {desliz} pt pasado el 0")
            tipos.add("deslizamiento de la entrada")
        if salto > 0 and ll.motivo != "objetivo":
            causas.append(f"el tick que salta el stop llega {salto} pt pasado su nivel")
            tipos.add("salto del stop")
        causa = "; ".join(causas) or "otra (ver columnas)"
        for t in tipos:
            resumen[t] += 1
        # el R recalculado desde el precio de salida, para comprobar que se lee lo que la salida
        # dice: R = sentido * (salida - llenado) / (llenado - stop original), por precio
        riesgo0 = abs(ll.entrada - stop0)
        r_calc = (Decimal(sentido * (px_sal - ll.entrada)) / Decimal(riesgo0)).quantize(
            Decimal("0.01")
        )
        cuadra = "cuadra" if abs(r_calc - ll.r) <= Decimal("0.01") else f"NO cuadra ({r_calc})"
        if aplicada == "si":
            evidencia = (
                "ADR-0051 §1-§5 y ADR-0057: la orden stop y el stop se llenan al tick que los "
                "dispara, el objetivo a su precio; el redondeo es el de stop_fraccion_redondeo y "
                "fijar_objetivo"
            )
        salida.append(
            f"{ll.dia} | {ll.sesion} | {ll.orden} | {ll.lado} | {ll.motivo}"
            + (" (tras mover a break even)" if movido and ll.motivo == "stop" else "")
            + f" | {ll.r:+.2f} | {esperado:+.2f} | {desviacion:+.2f} | {caja} | {o.distancia} | "
            f"{teor:+.2f} | {llen.fuente} {hora(llen.ms)}, {desliz:+d}, {spread} | {sal.fuente} "
            f"{hora(sal.ms)}, {precio(px_sal)}, {salto:+d} | {o.limite} (riesgo {o.riesgo}%) | "
            f"{com_r} | {causa} | R desde el precio de salida: {cuadra} | {aplicada}: {evidencia}"
        )
    n = len(salida) - 2
    salida += [
        f"casos: {n}; por tipo de causa (un caso puede tener varias): "
        + ", ".join(f"{k} {v}" for k, v in sorted(resumen.items())),
        "",
        f"cerradas a mercado (manual, sin R esperado): {len(manuales)}",
        *manuales,
    ]
    return salida


def parte_b(
    llenadas: list[Llenada],
    ordenes: dict[tuple[str, str], Orden],
    eventos: dict[str, list[Evento]],
    por_sesion: dict[tuple[str, str], str],
) -> list[str]:
    salida = ["", f"## b) Sesiones de la corrida 2 con mas de {SESIONES_LLENAS} llenadas"]
    por_ses: dict[tuple[str, str], list[Llenada]] = defaultdict(list)
    for ll in llenadas:
        por_ses[(ll.dia, ll.sesion)].append(ll)
    por_dia: dict[str, list[Llenada]] = defaultdict(list)
    for ll in llenadas:
        por_dia[ll.dia].append(ll)
    for (dia, ses), lls in sorted(por_ses.items()):
        if len(lls) <= SESIONES_LLENAS:
            continue
        evs = eventos[dia]
        salida.append(f"### {dia} {ses}: {len(lls)} llenadas")
        escenarios: dict[str, list[Llenada]] = defaultdict(list)
        for ll in lls:
            escenarios[ll.escenario.split(" (")[0]].append(ll)
        salida.append(
            f"escenarios con llenadas: {len(escenarios)} ("
            + ", ".join(f"{k}: {len(v)}" for k, v in sorted(escenarios.items()))
            + "); la toma de cada escenario no esta en ninguna salida commiteada"
        )
        puntos_c = Counter(ll.punto for ll in lls)
        salida.append("llenadas por punto: " + ", ".join(f"{k} {v}" for k, v in puntos_c.items()))
        # cartuchos por escenario (RN-016, cartuchos_max 3, solo_perdida: salta el stop sin mover)
        for esc, ls in sorted(escenarios.items()):
            filas = []
            perdidas = 0
            for ll in sorted(ls, key=lambda x: x.llenada_ms):
                movido = any(e.tipo == "stop_movido" and e.id == f"pos-{ll.orden}" for e in evs)
                gasta = ll.motivo == "stop" and not movido
                filas.append(
                    f"{ll.orden} {hora(ll.llenada_ms)} {ll.punto} {ll.r:+.2f} ({ll.motivo}"
                    + (", break even" if movido else "")
                    + f"; cartuchos gastados antes de llenar: {perdidas})"
                )
                perdidas += gasta
            salida.append(f"  {esc}: " + " · ".join(filas))
        # racha del dia (RN-036; la cuenta diaria la pone a cero cada dia; el break even no corta)
        racha = maxima = 0
        for ll in sorted(por_dia[dia], key=lambda x: x.llenada_ms):
            movido = any(e.tipo == "stop_movido" and e.id == f"pos-{ll.orden}" for e in evs)
            if ll.motivo == "stop" and not movido:
                racha += 1
            elif ll.r > 0:
                racha = 0
            maxima = max(maxima, racha)
        # la perdida del dia en % del saldo: R por el riesgo de cada orden, mas la comision
        perdida = Decimal(0)
        for ll in por_dia[dia]:
            o = ordenes[(dia, ll.orden)]
            if o.riesgo is not None:
                perdida += ll.r * o.riesgo
            perdida -= COMISION_REDONDA_POR_LOTE * o.lote / Decimal(1000)
        salida.append(
            f"racha de perdidas maxima del dia (RN-036, tope 9): {maxima}; resultado del dia en % "
            f"del saldo (R x riesgo de cada orden, menos la comision): {perdida:+.2f} "
            f"(RN-020: tope 4,5 de perdida)"
        )
        salida.append(f"linea «Por sesion» de la salida: {por_sesion.get((dia, ses), 'no hay')}")
    return salida


def parte_c(ticks: Ticks) -> list[str]:
    salida = ["", "## c) Censo de los eventos del respaldo M1, en las dos corridas"]
    for nombre, ruta in (("corrida 1", ARRASTRADA), ("corrida 2", DIARIA)):
        ordenes, eventos = leer_salida(lineas(ruta))
        cuenta: Counter[tuple[str, str]] = Counter()
        filas = []
        for dia, evs in sorted(eventos.items()):
            for e in evs:
                if e.fuente != "respaldo_m1":
                    continue
                donde = clasificar_respaldo(dia, e.ms, ticks.horas(dia[:7]))
                extra = ""
                if e.tipo == "llenada":
                    o = ordenes[(dia, e.id)]
                    if o.colocada_ms == e.ms - 1:
                        extra = "; llenada con la M1 cuyo cierre coloco la orden"
                cuenta[(e.tipo, donde + extra)] += 1
                filas.append(f"  {dia} | {hora(e.ms)} | {e.tipo} | {e.id} | {donde}{extra}")
        salida.append(f"### {nombre}: {sum(cuenta.values())} eventos del respaldo")
        salida += [f"  {t} · {d}: {n}" for (t, d), n in sorted(cuenta.items())]
        salida += filas
    return salida


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    ls = lineas(DIARIA)
    ordenes, eventos = leer_salida(ls)
    por_sesion = {}
    for ln in ls:
        partes = ln.split(" | ")
        if len(partes) > 4 and partes[2].startswith("bot ") and partes[3].startswith("rn003 "):
            dia, ses = partes[0].split(" ")
            por_sesion[(dia, ses)] = (
                partes[0]
                + " | "
                + " | ".join(x for x in partes[1:] if x.startswith(("bot", "disparadas")))
            )
    llenadas = leer_entradas()
    ticks = Ticks()
    print("# RECORRIDA-CONSTRUCCION §2.8: costes, sesiones cargadas y el respaldo M1")
    print(f"llenadas leidas de entradas-antes-alternancia.txt: {len(llenadas)}")
    for linea in (
        parte_a(llenadas, ordenes, eventos, ticks)
        + parte_b(llenadas, ordenes, eventos, por_sesion)
        + parte_c(ticks)
    ):
        print(linea)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
