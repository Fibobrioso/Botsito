"""¿Habrían cumplido las reglas de FTMO 2-Step Swing 100k las operaciones del PROPIO trader en
construcción? Rama `trabajo/viabilidad-trader`, 2026-09-28 (docs/validation/VIABILIDAD-TRADER.md).

Es una MEDICIÓN: no cambia la estrategia, el bot ni el bróker, y no se ajusta nada para mejorar la
cifra. Estos resultados NO se enseñan al trader ni entran en material para él.

Dos series de las mismas 77 operaciones (abril y agosto, los casos `dev` con stop):

- SIMULADA: cada operación se abre en su instante y a su precio de entrada (el caso es el llenado,
  ADR-0043) y se repite por el bróker simulado sobre los ticks de Dukascopy, con el spread real, la
  comisión del perfil (5 USD por lote en cada lado, R12) y el cierre forzoso al final de la ventana
  (RN-002). Stop: el inicial del libro (`initialSL`); el único movimiento documentado con instante
  y caso inequívoco es el de v7-3 (BLOQUE-DE-LA-CAJA.md §5.1), y se reproduce. Objetivo: la regla de
  la spec, `objetivo_rr` x la distancia al stop inicial (el libro no registra el objetivo planeado,
  ADR-0037 §7). Precios del trader (OANDA) desplazados -2 puntos a la escala de Dukascopy
  (BLOQUE-DE-LA-CAJA.md §2.3).
- ANOTADA: la salida real que anotó el trader (`avgClosePrice` en `dateEnd`), con el mismo lote y la
  misma comisión. No ve la equity dentro de la operación: solo abre y cierra.

El lote sale del riesgo por operación sobre el saldo realizado (`base_calculo_riesgo: saldo_actual`)
y la distancia al stop inicial, redondeado hacia abajo a 0,01. Las reglas de la fase 1 salen del
perfil (`evaluar_fase`, ADR-0050). Lee el repositorio en --raiz; escribe solo en --salida.

    uv run python scripts/viabilidad_trader.py --salida <fichero> [--raiz <repo>]
"""

from __future__ import annotations

import argparse
import json
import random
import statistics
import sys
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import datetime
from decimal import ROUND_DOWN, Decimal
from pathlib import Path
from typing import Any

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))

# Escenarios de riesgo por operación, en % del saldo. 0,5 es `riesgo_por_operacion` (CONFIRMED);
# la spec lo mide en el 0,8 de la caja (`lotaje_base: hasta_stop_fraccion`), así que si el stop
# inicial está en el 1 un stop completo cuesta 0,5 / 0,8 = 0,625: los dos extremos de la spec. 1 y 2
# son sensibilidad, FUERA de la spec.
ESCENARIOS = (Decimal("0.5"), Decimal("0.625"), Decimal("1"), Decimal("2"))
DE_LA_SPEC = frozenset({Decimal("0.5"), Decimal("0.625")})
DESFASE_PUNTOS = 2  # OANDA - Dukascopy, mediana medida en las leyendas (BLOQUE-DE-LA-CAJA §2.3)
LOTE_PASO = Decimal("0.01")
UMBRAL_CERO_R = 0.1  # |R| por debajo: cerrada «a cero» (break even o casi)
UMBRAL_DIFERENCIA_R = 1.0  # |R simulada - R anotada| desde aquí: diferencia grande
BOOTSTRAP_N = 10_000
SEMILLA = 20260928
# El único movimiento de stop documentado con instante y caso inequívoco (BLOQUE-DE-LA-CAJA.md §5.1,
# v7-3): la venta del 3 de agosto llenada a las 06:07:40 UTC, con la orden 2 puntos bajo el 0 y el
# stop en el 1 (1.15389, el caso dice 1.15388); en el fotograma de las 08:11:59 del gráfico
# (06:11:59 UTC) el stop ya está en 1.15383, el 0,8. Se mueve ahí, el primer instante en que se ve.
MOVIMIENTOS = {("2026-08-03T06:07:40+00:00", "1.15362"): ("2026-08-03T06:11:59+00:00", "1.15383")}


# ------------------------------------------------------------------------------------ puras


def r_de(direccion: str, entrada: float, stop: float, cierre: float) -> float:
    """El resultado en R: lo ganado o perdido en unidades de la distancia al stop inicial."""
    signo = 1 if direccion == "compra" else -1
    distancia = abs(entrada - stop)
    if distancia == 0:
        raise ValueError("stop en la entrada: sin R")
    return signo * (cierre - entrada) / distancia


def clase(r: float) -> str:
    if r >= UMBRAL_CERO_R:
        return "gana"
    if r <= -UMBRAL_CERO_R:
        return "pierde"
    return "cero"


def diferencia_grande(r_simulada: float, r_anotada: float) -> bool:
    return (
        clase(r_simulada) != clase(r_anotada) or abs(r_simulada - r_anotada) >= UMBRAL_DIFERENCIA_R
    )


def bootstrap(
    rs: Sequence[float], n: int = BOOTSTRAP_N, semilla: int = SEMILLA
) -> tuple[float, float, float]:
    """La media y su intervalo del 95 % por bootstrap de percentiles, con semilla fija."""
    if not rs:
        raise ValueError("sin operaciones")
    azar = random.Random(semilla)
    k = len(rs)
    medias = sorted(sum(azar.choices(rs, k=k)) / k for _ in range(n))
    return statistics.fmean(rs), medias[int(0.025 * n)], medias[int(0.975 * n) - 1]


@dataclass(frozen=True)
class Estadisticas:
    n: int
    ganan: int
    pierden: int
    cero: int
    r_medio_ganadoras: float | None
    r_medio_perdedoras: float | None
    esperanza: float
    ic_bajo: float
    ic_alto: float

    @property
    def tasa_acierto(self) -> float:
        return self.ganan / self.n


def estadisticas(rs: Sequence[float]) -> Estadisticas:
    g = [r for r in rs if clase(r) == "gana"]
    p = [r for r in rs if clase(r) == "pierde"]
    media, lo, hi = bootstrap(rs)
    return Estadisticas(
        n=len(rs),
        ganan=len(g),
        pierden=len(p),
        cero=len(rs) - len(g) - len(p),
        r_medio_ganadoras=statistics.fmean(g) if g else None,
        r_medio_perdedoras=statistics.fmean(p) if p else None,
        esperanza=media,
        ic_bajo=lo,
        ic_alto=hi,
    )


def veredicto(estado: str, motivo: str, ic_bajo: float, ic_alto: float) -> tuple[str, str]:
    """Pasa / no pasa / no concluyente, con la razón. Regla escrita ANTES de correr: manda lo que
    dice la cuenta sobre la muestra (SUPERADA o SUSPENDIDA); si la cuenta no llega a ninguna de las
    dos, no concluyente. Y si la esperanza neta tiene un intervalo que cruza el cero, se dice: la
    muestra no sostiene que se repita."""
    cruza = ic_bajo <= 0 <= ic_alto
    nota = "; la esperanza en R tiene un intervalo que cruza el 0" if cruza else ""
    if estado == "SUPERADA":
        return "pasa", f"alcanza el objetivo con los días mínimos y sin romper un límite{nota}"
    if estado == "SUSPENDIDA":
        return "no pasa", f"rompe un límite: {motivo}{nota}"
    return "no concluyente", f"ni alcanza el objetivo ni rompe un límite en la muestra{nota}"


def comision_en_r(
    comision_por_lote: Decimal, lados: int, distancia_puntos: int, contrato: Decimal, escala: int
) -> float:
    """Lo que cuesta la comision en R: por lote, la comision de los lados cobrados entre lo que se
    pierde por lote hasta el stop inicial. No depende del lote: con EURUSD y cuenta en USD, un
    punto por lote vale un dolar, asi que 5 USD por lado cuestan 10 / distancia R."""
    riesgo_por_lote = Decimal(distancia_puntos) / escala * contrato
    return float(comision_por_lote * lados / riesgo_por_lote)


def marcas_antes_del_cierre(op: Any) -> Any:
    """La operacion sin las marcas en o despues de su cierre: el cierre ya dice ese precio."""
    return replace(op, marcas=tuple(m for m in op.marcas if m.instante < op.cierre.instante))


def marcas_en_el_cierre(cerradas: Sequence[Any]) -> int:
    """Cuantas operaciones traen una marca en o despues de su propio cierre."""
    return sum(1 for op in cerradas if any(m.instante >= op.cierre.instante for m in op.marcas))


def lote_por_riesgo(
    riesgo: Decimal, distancia_puntos: int, contrato: Decimal, escala: int
) -> Decimal:
    """Lotes que arriesgan `riesgo` (dinero) hasta el stop inicial, hacia abajo a 0,01."""
    if distancia_puntos <= 0:
        return Decimal(0)
    lotes = riesgo / (Decimal(distancia_puntos) / escala * contrato)
    return lotes.quantize(LOTE_PASO, rounding=ROUND_DOWN)


# ------------------------------------------------------------------------------- medición


@dataclass(frozen=True)
class OpTrader:
    id: str
    caso: str
    dia: str
    sesion: str
    direccion: str
    instante: datetime  # llenado
    entrada: Decimal  # OANDA
    stop: Decimal  # initialSL, OANDA
    cierre_anotado: Decimal  # avgClosePrice
    instante_cierre: datetime  # dateEnd
    rpnl_signo: int
    status: str


def _pnl(op: Any, contrato: Decimal) -> Decimal:
    signo = 1 if op.direccion == "compra" else -1
    bruto = signo * (op.cierre.precio - op.apertura.precio) * op.lotes * contrato
    return bruto - sum((c.importe for c in op.cargos), Decimal(0))


def medir(raiz: Path) -> dict[str, Any]:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.holdout import casos_ocultos, casos_reservados
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.corpus.libro import PESTANA_OPERACIONES, filas_de_los_dias
    from botsito.corpus.libros import declaracion_de
    from botsito.data.velas import a_minuto
    from botsito.domain.ticks import MS_POR_MINUTO
    from botsito.engine import arnes, simulacion
    from botsito.engine.broker import Broker, BrokerError
    from botsito.engine.cuenta import Cargo, Marca, Operacion, evaluar_fase, reglas_de_fase
    from botsito.engine.perfil_cuenta import cargar_perfil
    from botsito.engine.simulador_config import FICHERO_LLENADO, cargar_config_llenado

    criterio = cargar_criterio(raiz)
    meses = tuple(criterio.construccion)
    if set(meses) != {"2026-04", "2026-08"}:
        raise SystemExit(f"construccion no es abril y agosto: {meses}")
    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(raiz / "knowledge" / "cases" / "kit" / "config.yaml")
    perfil = cargar_perfil(raiz / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    reglas_fase = reglas_de_fase(perfil, "reto")
    reglas_broker = simulacion.reglas_broker_de(perfil)
    cfg = cargar_config_llenado(raiz / FICHERO_LLENADO).configuracion()
    contrato = registro.decimal("instrumento_contrato")
    objetivo_rr = registro.decimal("objetivo_rr")
    huso = registro.texto("huso_operativa")
    ocultos = set(casos_ocultos(raiz)) | set(casos_reservados(raiz))
    dias = arnes.dias_de_construccion(raiz, criterio, list(meses), ocultos=casos_ocultos(raiz))
    if any(d.id in ocultos for d in dias):
        raise SystemExit("un caso de construccion esta reservado")

    # --- el libro: SOLO las filas de los dias dev pedidos (corpus.libro no enumera nada)
    libros = {
        "2026-04": "backtesting-analytics ABRIL 2026.xlsx",
        "2026-08": "backtesting-analytics AGOSTO 2026.xlsx",
    }
    columnas = (
        "dateStart", "side", "entryPrice", "initialSL", "avgClosePrice", "rPnL", "status",
        "dateEnd",
    )  # fmt: skip
    material = raiz / "corpus" / "Estrategia del trader" / "Material adicional de su operativa"
    filas: list[dict[str, str | None]] = []
    for mes, nombre in libros.items():
        ruta = material / nombre
        decl = declaracion_de(raiz, ruta)
        pedidos = [d.dia for d in dias if d.dia.startswith(mes)]
        for f in filas_de_los_dias(
            ruta, pedidos, PESTANA_OPERACIONES, columnas, decl, huso_de_los_dias=huso
        ):
            f["_decl"] = nombre
            filas.append(f)
    decls = {n: declaracion_de(raiz, material / n) for n in libros.values()}
    from botsito.corpus.libro import _instante  # la misma lectura declarada que dateStart

    sin_stop = [f for f in filas if not f.get("initialSL")]
    por_clave = {
        (str(f["_instante_utc"]), str(f["entryPrice"])): f for f in filas if f.get("initialSL")
    }

    # --- las operaciones: el caso manda, el libro añade la salida anotada
    mercados: dict[str, simulacion.MercadoDia] = {}
    ops: list[OpTrader] = []
    for d in dias:
        md = simulacion.mercado_de_construccion(
            raiz,
            carpeta_datos(raiz),
            criterio,
            config,
            registro,
            d.id,
            con_operaciones_del_trader=True,
        )
        mercados[d.dia] = md
        assert md.operaciones_trader is not None
        for op_caso, o in zip(d.operaciones, md.operaciones_trader, strict=True):
            clave = (op_caso.instante.isoformat(), str(Decimal(str(op_caso.entrada))))
            f = por_clave.get(clave)
            if f is None:  # el libro escribe la entrada sin normalizar: se busca por valor
                f = next(
                    (
                        v
                        for (t, e), v in por_clave.items()
                        if t == clave[0] and Decimal(e) == Decimal(str(op_caso.entrada))
                    ),
                    None,
                )
            if f is None:
                raise SystemExit(f"{d.id}: una operacion del caso sin fila en el libro")
            fin = _instante(str(f["dateEnd"]), decls[str(f["_decl"])])
            if fin is None:
                raise SystemExit(f"{d.id}: dateEnd sin el formato declarado")
            stop = o.marcas[0].precio
            if Decimal(str(f["initialSL"])) != stop:
                raise SystemExit(f"{d.id}: el stop del caso no es el initialSL del libro")
            ops.append(
                OpTrader(
                    id=o.id,
                    caso=d.id,
                    dia=d.dia,
                    sesion=op_caso.sesion,
                    direccion=op_caso.direccion,
                    instante=op_caso.instante,
                    entrada=Decimal(str(op_caso.entrada)),
                    stop=stop,
                    cierre_anotado=Decimal(str(f["avgClosePrice"])),
                    instante_cierre=fin,
                    rpnl_signo=(Decimal(str(f["rPnL"])) > 0) - (Decimal(str(f["rPnL"])) < 0),
                    status=str(f.get("status") or ""),
                )
            )
    if len(ops) != 77:
        raise SystemExit(f"se esperaban 77 operaciones y hay {len(ops)}")

    def pts(precio: Decimal, escala: int) -> int:
        return int((precio * escala).to_integral_value())

    def simular(
        tramo: Sequence[OpTrader], riesgo_pct: Decimal
    ) -> tuple[list[Any], dict[str, dict[str, Any]]]:
        """Las del tramo por el broker, dia a dia, con el lote sobre el saldo realizado."""
        cerradas: list[Any] = []
        detalle: dict[str, dict[str, Any]] = {}
        saldo = reglas_fase.capital_inicial
        for dia in sorted({o.dia for o in tramo}):
            md = mercados[dia]
            b = Broker(reglas_broker, cfg, md.mercado(), contrato, md.escala)
            vistas = 0
            for o in sorted((x for x in tramo if x.dia == dia), key=lambda x: x.instante):
                ms = (
                    int(a_minuto(o.instante.replace(second=0, microsecond=0))) * MS_POR_MINUTO
                    + o.instante.second * 1000
                )
                b.avanzar(ms - 1)
                nuevas = b.operaciones_cerradas()[vistas:]
                saldo += sum((_pnl(c, contrato) for c in nuevas), Decimal(0))
                vistas += len(nuevas)
                entrada = pts(o.entrada, md.escala) - DESFASE_PUNTOS
                stop = pts(o.stop, md.escala) - DESFASE_PUNTOS
                dist = abs(entrada - stop)
                objetivo = entrada + int(dist * objetivo_rr) * (
                    1 if o.direccion == "compra" else -1
                )
                lotes = lote_por_riesgo(saldo * riesgo_pct / 100, dist, contrato, md.escala)
                detalle[o.id] = {
                    "lotes": str(lotes),
                    "entrada": entrada,
                    "stop": stop,
                    "objetivo": objetivo,
                }
                if lotes <= 0:
                    detalle[o.id]["rechazo"] = "lote 0"
                    continue
                try:
                    b.abrir_conocida(
                        f"p-{o.id}", o.direccion, entrada, lotes, stop, objetivo, ms, "caso"
                    )  # type: ignore[arg-type]
                except BrokerError as exc:
                    detalle[o.id]["rechazo"] = str(exc)
                    continue
                mov = MOVIMIENTOS.get((o.instante.isoformat(), str(o.entrada)))
                if mov is not None:
                    t_mov = datetime.fromisoformat(mov[0])
                    ms_mov = (
                        int(a_minuto(t_mov.replace(second=0))) * MS_POR_MINUTO + t_mov.second * 1000
                    )
                    b.avanzar(ms_mov - 1)
                    if b.posiciones[f"p-{o.id}"].abierta:
                        b.mover_stop(
                            f"p-{o.id}", pts(Decimal(mov[1]), md.escala) - DESFASE_PUNTOS, ms_mov
                        )
                        detalle[o.id]["stop_movido"] = mov
            b.avanzar(md.hasta_ms - 1)
            for p in list(b.posiciones.values()):
                if p.abierta:
                    b.cerrar_a_mercado(p.id, md.hasta_ms - 1)
            nuevas = b.operaciones_cerradas()[vistas:]
            saldo += sum((_pnl(c, contrato) for c in nuevas), Decimal(0))
            for p in b.posiciones.values():
                oid = p.id.removeprefix("p-")
                detalle[oid]["cierre"] = p.precio_cierre
                detalle[oid]["motivo"] = p.motivo_cierre
                detalle[oid]["fuente"] = p.fuente_cierre
                detalle[oid]["deslizamiento"] = p.deslizamiento_entrada
            cerradas.extend(replace(c, id=f"{dia}/{c.id}") for c in b.operaciones_cerradas())
        return cerradas, detalle

    def anotadas(tramo: Sequence[OpTrader], riesgo_pct: Decimal) -> list[Any]:
        """Las mismas operaciones con la salida que anotó el trader: sin equity intermedia."""
        salida: list[Any] = []
        saldo = reglas_fase.capital_inicial
        pendientes: list[tuple[datetime, Decimal]] = []
        comision = reglas_broker.comision_por_lote
        escala = 100_000
        for o in sorted(tramo, key=lambda x: x.instante):
            # el saldo realizado al abrir: las cerradas antes de este instante
            saldo += sum((p for t, p in pendientes if t <= o.instante), Decimal(0))
            pendientes = [(t, p) for t, p in pendientes if t > o.instante]
            dist = abs(pts(o.entrada, escala) - pts(o.stop, escala))
            lotes = lote_por_riesgo(saldo * riesgo_pct / 100, dist, contrato, escala)
            if lotes <= 0 or lotes > reglas_broker.volumen_max_lotes:
                continue  # como en la simulada: el perfil no admite esa posicion
            cargos: tuple[Any, ...] = (Cargo(o.instante, comision * lotes, "comision"),)
            if (
                reglas_broker.comision_por_lado
            ):  # como el broker: en cada lado, si el perfil lo dice
                cargos += (Cargo(o.instante_cierre, comision * lotes, "comision"),)
            op = Operacion(
                id=o.id,
                direccion=o.direccion,  # type: ignore[arg-type]
                lotes=lotes,
                apertura=Marca(o.instante, o.entrada),
                cierre=Marca(o.instante_cierre, o.cierre_anotado),
                cargos=cargos,
            )
            salida.append(op)
            pendientes.append((o.instante_cierre, _pnl(op, contrato)))
        return salida

    def curva(cerradas: Sequence[Any]) -> dict[str, Any]:
        """Saldo tras cada cierre, su maximo, la caida maxima de pico a valle y el saldo final."""
        saldo = reglas_fase.capital_inicial
        pico = saldo
        caida = Decimal(0)
        puntos: list[tuple[str, str]] = []
        for c in sorted(cerradas, key=lambda x: (x.cierre.instante, x.id)):
            saldo += _pnl(c, contrato)
            pico = max(pico, saldo)
            caida = max(caida, pico - saldo)
            puntos.append((c.cierre.instante.isoformat(), f"{saldo:.2f}"))
        return {
            "saldo_final": f"{saldo:.2f}",
            "caida_max_pct": f"{100 * caida / reglas_fase.capital_inicial:.2f}",
            "puntos": puntos,
        }

    def cuenta(cerradas: Sequence[Any], sanear: bool = True) -> dict[str, Any]:
        """El veredicto de la fase. SANEADO: sin las marcas en o despues del cierre. El broker deja
        una marca en el mismo instante del tick que cierra, y `cuenta._eventos` ordena a igual
        instante el cierre ANTES que la marca, asi que la marca vuelve a meter la posicion cerrada
        en la equity como abierta y ahi se queda: un error de codigo de `evaluar_fase`, que esta
        rama NO corrige (VIABILIDAD-TRADER.md §6). Con `sanear=False`, el motor tal cual."""
        if sanear:
            cerradas = [marcas_antes_del_cierre(x) for x in cerradas]
        r = evaluar_fase(cerradas, reglas_fase, contrato)
        capital = reglas_fase.capital_inicial
        peor_dia = max(
            (
                (
                    d.saldo_corte
                    - (d.equity_minima if d.equity_minima is not None else d.saldo_corte)
                )
                for d in r.dias
            ),
            default=Decimal(0),
        )
        peor_total = max(
            (
                (capital - (d.equity_minima if d.equity_minima is not None else capital))
                for d in r.dias
            ),
            default=Decimal(0),
        )
        return {
            "estado": r.estado.value,
            "motivo": r.motivo,
            "instante": r.instante.isoformat() if r.instante else None,
            "dias_de_trading": r.dias_de_trading,
            "peor_dia_pct": f"{100 * peor_dia / capital:.2f}",
            "peor_total_pct": f"{100 * peor_total / capital:.2f}",
            "saldo_final_cuenta": f"{r.saldo_final:.2f}",
            "operaciones_tras_el_final": r.operaciones_tras_el_final,
        }

    tramos = {
        "abril": [o for o in ops if o.dia.startswith("2026-04")],
        "agosto": [o for o in ops if o.dia.startswith("2026-08")],
        "abril+agosto": ops,
    }
    resultado: dict[str, Any] = {
        "operaciones": len(ops),
        "filas_sin_stop": {
            "2026-04": sum(1 for f in sin_stop if str(f["_dia"]).startswith("2026-04")),
            "2026-08": sum(1 for f in sin_stop if str(f["_dia"]).startswith("2026-08")),
        },
        "ticks": {dia: bool(md.origen_ticks) for dia, md in mercados.items()},
        "horas_perdidas": {
            dia: list(md.horas_perdidas) for dia, md in mercados.items() if md.horas_perdidas
        },
        "escenarios": {},
        "marcas_en_el_cierre": marcas_en_el_cierre(simular(ops, ESCENARIOS[0])[0]),
        "por_operacion": [],
    }
    # R: no depende del riesgo; la simulada con el escenario de la spec
    _, det = simular(ops, ESCENARIOS[0])
    r_sim: dict[str, float] = {}
    r_ano: dict[str, float] = {}
    lados = 2 if reglas_broker.comision_por_lado else 1
    coste: dict[str, float] = {}
    for o in ops:
        dd = det[o.id]
        coste[o.id] = comision_en_r(
            reglas_broker.comision_por_lote,
            lados,
            abs(dd["entrada"] - dd["stop"]),
            contrato,
            100_000,
        )
        r_ano[o.id] = r_de(o.direccion, float(o.entrada), float(o.stop), float(o.cierre_anotado))
        if "cierre" in dd:
            r_sim[o.id] = r_de(o.direccion, dd["entrada"], dd["stop"], dd["cierre"])
        resultado["por_operacion"].append(
            {
                "id": o.id,
                "dia": o.dia,
                "sesion": o.sesion,
                "instante": o.instante.isoformat(),
                "direccion": o.direccion,
                "entrada": str(o.entrada),
                "stop": str(o.stop),
                "distancia_puntos": abs(dd["entrada"] - dd["stop"]),
                "cierre_anotado": str(o.cierre_anotado),
                "cierre_anotado_instante": o.instante_cierre.isoformat(),
                "status": o.status,
                "rpnl_signo": o.rpnl_signo,
                "comision_r": round(coste[o.id], 3),
                "r_anotada": round(r_ano[o.id], 3),
                "r_simulada": None if o.id not in r_sim else round(r_sim[o.id], 3),
                "motivo_simulado": dd.get("motivo"),
                "fuente_simulada": dd.get("fuente"),
                "stop_movido": dd.get("stop_movido"),
                "rechazo": dd.get("rechazo"),
                "grande": o.id in r_sim and diferencia_grande(r_sim[o.id], r_ano[o.id]),
            }
        )
    for nombre, tramo in tramos.items():
        ids = {o.id for o in tramo}
        netas = {
            "simulada_neta": {i: r - coste[i] for i, r in r_sim.items()},
            "anotada_neta": {i: r - coste[i] for i, r in r_ano.items()},
        }
        for fuente, rs in (("simulada", r_sim), ("anotada", r_ano), *netas.items()):
            e = estadisticas([rs[i] for i in sorted(ids) if i in rs])
            resultado.setdefault("estadisticas", {})[f"{nombre}/{fuente}"] = e.__dict__ | {
                "tasa_acierto": round(e.tasa_acierto, 3)
            }
    for riesgo in ESCENARIOS:
        for nombre, tramo in tramos.items():
            sim, det_r = simular(tramo, riesgo)
            rechazos = sorted(
                {
                    str(v.get("rechazo")).split("(")[-1].rstrip(")")
                    for v in det_r.values()
                    if v.get("rechazo")
                }
            )
            n_rech = sum(1 for v in det_r.values() if v.get("rechazo"))
            ano = anotadas(tramo, riesgo)
            for fuente, cerradas in (("simulada", sim), ("anotada", ano)):
                est = resultado["estadisticas"][f"{nombre}/{fuente}_neta"]
                c = cuenta(cerradas)
                tal_cual = cuenta(cerradas, sanear=False)
                v, razon = veredicto(c["estado"], c["motivo"], est["ic_bajo"], est["ic_alto"])
                resultado["escenarios"][f"{riesgo}/{nombre}/{fuente}"] = (
                    c
                    | curva(cerradas)
                    | {"veredicto": v, "razon": razon, "n": len(cerradas)}
                    | {
                        "motor_tal_cual": {
                            k: tal_cual[k] for k in ("estado", "peor_dia_pct", "peor_total_pct")
                        }
                    }
                    | (
                        {"rechazadas": n_rech, "motivos_rechazo": rechazos}
                        if fuente == "simulada"
                        else {}
                    )
                )
    return resultado


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    p.add_argument("--salida", type=Path, required=True)
    args = p.parse_args(argv)
    resultado = medir(args.raiz)
    args.salida.write_text(
        json.dumps(resultado, indent=1, ensure_ascii=False, default=str), encoding="utf-8"
    )
    print(json.dumps({k: v["veredicto"] for k, v in resultado["escenarios"].items()}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
