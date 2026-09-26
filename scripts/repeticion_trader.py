"""Repeticion DESCRIPTIVA de las operaciones reales del trader por el broker y la cuenta FTMO.

Fase 6 de `trabajo/ticks-llenado` (ADR-0051, ADR-0052, ADR-0050). SOLO construccion (abril y
agosto), por la compuerta del arnes. Solo descriptivo: no cambia ningun ADR, parametro ni spec.

LO QUE EL CASO TRAE Y LO QUE NO. Cada operacion dev trae instante de llenado, direccion, entrada y
stop (`initialSL`); NO trae salida, resultado ni lote (ADR-0037 §7, ADR-0043). Aqui NO se inventa
la salida real: cada operacion se REPITE por el broker con la regla de salida de la spec -stop del
caso, objetivo DERIVADO por `objetivo_rr` (registro), cierre forzoso a `ventana_fin` (RN-002)- y
el lote sale de una REJILLA EXPLICITA de riesgo por operacion, declarada como escenarios
hipoteticos y no como parametros del bot. Lo que se reporta es «que habria pasado en la cuenta si
el trader hubiera salido por la regla de la spec», no lo que le paso al trader.

Por escenario y por mes: el veredicto FTMO (fase `reto`), la perdida diaria maxima y la total
maxima (sobre el capital inicial), los dias operados y, si suspende, en que instante. Y el
contraste ticks frente a respaldo M1: en cuantas operaciones cambia el desenlace (motivo o
precio de cierre). Imprime solo recuentos, porcentajes e instantes de suspension; ni una entrada
ni un stop.

  `uv run python scripts/repeticion_trader.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from decimal import ROUND_DOWN, Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
# La rejilla de riesgo por operacion, en porcentaje del capital inicial: escenarios HIPOTETICOS.
REJILLA_RIESGO = (Decimal("0.25"), Decimal("0.5"), Decimal("1"), Decimal("2"))
LOTE_PASO = Decimal("0.01")


@dataclass(frozen=True)
class Desenlace:
    motivo: str
    precio_cierre: int
    fuente: str


def lote_por_riesgo(
    riesgo_dinero: Decimal, entrada: int, stop: int, contrato: Decimal, escala: int
) -> Decimal:
    """Lotes para arriesgar `riesgo_dinero` entre la entrada y el stop, redondeado hacia abajo al
    paso de 0,01. Puro."""
    distancia = Decimal(abs(entrada - stop)) / escala
    if distancia == 0:
        return Decimal(0)
    lotes = riesgo_dinero / (distancia * contrato)
    return lotes.quantize(LOTE_PASO, rounding=ROUND_DOWN)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: repeticion_trader.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases import visto
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.velas import a_minuto
    from botsito.domain.ticks import MS_POR_MINUTO
    from botsito.engine import simulacion
    from botsito.engine.broker import Broker, BrokerError
    from botsito.engine.cuenta import EstadoCuenta, evaluar_fase, reglas_de_fase
    from botsito.engine.llenado import Mercado
    from botsito.engine.perfil_cuenta import cargar_perfil
    from botsito.engine.simulador_config import FICHERO_LLENADO, cargar_config_llenado
    from botsito.engine.visor import caso_de_construccion

    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    perfil = cargar_perfil(RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    reglas_fase = reglas_de_fase(perfil, "reto")
    reglas_broker = simulacion.reglas_broker_de(perfil)
    llenado = cargar_config_llenado(RAIZ / FICHERO_LLENADO)
    cfg = llenado.configuracion()
    contrato = registro.decimal("instrumento_contrato")
    objetivo_rr = registro.decimal("objetivo_rr")

    salida = [
        "REPETICION DESCRIPTIVA de las operaciones del trader por el broker y la cuenta FTMO",
        "SALIDA: la del caso NO existe; se repite con la regla de la spec (stop del caso, objetivo "
        f"= entrada +/- objetivo_rr x |entrada - stop| con objetivo_rr = {objetivo_rr}, cierre "
        f"forzoso a {config.ventana_local[1]} del trader). Escenarios HIPOTETICOS de riesgo por "
        "operacion: "
        + ", ".join(f"{r} %" for r in REJILLA_RIESGO)
        + " del capital inicial; lote redondeado hacia abajo a 0,01",
        f"PERFIL: {perfil.nombre}, fase reto; MESES: construccion "
        + ", ".join(criterio.construccion),
        f"LLENADO: limite al toque {llenado.limite_llena_al_toque}; spread supuesto de "
        f"{llenado.spread_fuente}",
    ]
    mercados: dict[str, list[simulacion.MercadoDia]] = {}
    for mes in criterio.construccion:
        casos = sorted(c for c, p in visto.asignacion(RAIZ, mes).items() if p == "dev")
        mercados[mes] = []
        for caso in casos:
            caso_de_construccion(RAIZ, criterio, caso)  # la compuerta, antes de leer nada
            mercados[mes].append(
                simulacion.mercado_de_construccion(
                    RAIZ,
                    carpeta_datos(RAIZ),
                    criterio,
                    config,
                    registro,
                    caso,
                    con_operaciones_del_trader=True,
                )
            )
    salida.append(
        "TICKS: "
        + "; ".join(
            f"{mes} {sum(1 for m in ms if m.origen_ticks)} de {len(ms)} dias con ticks"
            for mes, ms in mercados.items()
        )
    )

    def repetir(
        md: simulacion.MercadoDia, riesgo_pct: Decimal, con_ticks: bool
    ) -> tuple[list[object], list[Desenlace], list[str]]:
        """Las operaciones del caso por el broker, en orden: las cerradas y sus desenlaces."""
        mercado = md.mercado() if con_ticks else Mercado((), md.m1)
        b = Broker(reglas_broker, cfg, mercado, contrato, md.escala)
        desenlaces: list[Desenlace] = []
        rechazadas: list[str] = []
        assert md.operaciones_trader is not None
        for i, op in enumerate(md.operaciones_trader, 1):
            entrada = int((op.apertura.precio * md.escala).to_integral_value())
            stop = int((op.marcas[0].precio * md.escala).to_integral_value()) if op.marcas else None
            if stop is None:
                continue
            distancia = abs(entrada - stop)
            objetivo = (
                entrada + int(distancia * objetivo_rr)
                if op.direccion == "compra"
                else entrada - int(distancia * objetivo_rr)
            )
            lotes = lote_por_riesgo(
                reglas_fase.capital_inicial * riesgo_pct / 100, entrada, stop, contrato, md.escala
            )
            if lotes <= 0:
                continue
            llenado_ms = (
                int(a_minuto(op.apertura.instante.replace(second=0, microsecond=0))) * MS_POR_MINUTO
                + op.apertura.instante.second * 1000
            )
            # el instante del caso ES el llenado (medido, ADR-0043): la posicion se abre ahi, al
            # precio del caso, sin pasar por el modelo de llenado; el stop, el objetivo y el cierre
            # forzoso si se deciden con el modelo
            try:
                b.abrir_conocida(
                    f"pos-t{i}",
                    op.direccion,
                    entrada,
                    lotes,
                    stop,
                    objetivo,
                    llenado_ms,
                    "caso",  # type: ignore[arg-type]
                )
            except BrokerError as exc:
                # un limite del perfil (p. ej. mas lotes que firma_volumen_max_lotes con un stop
                # muy corto): la operacion no entra y se cuenta
                rechazadas.append(str(exc).rsplit("(", 1)[-1].rstrip(")"))
        # el cierre forzoso, en el ultimo milisegundo de la ventana (el minuto de `hasta` ya no
        # pertenece al dia del trader y no tiene M1 cargada)
        b.avanzar(md.hasta_ms - 1)
        for p in list(b.posiciones.values()):
            if p.abierta:
                b.cerrar_a_mercado(p.id, md.hasta_ms - 1)
        for p in sorted(b.posiciones.values(), key=lambda x: x.id):
            desenlaces.append(
                Desenlace(str(p.motivo_cierre), int(p.precio_cierre or 0), str(p.fuente_cierre))
            )
        return list(b.operaciones_cerradas()), desenlaces, rechazadas

    for riesgo in REJILLA_RIESGO:
        salida.append(f"== ESCENARIO riesgo {riesgo} % por operacion")
        for mes, ms in mercados.items():
            ops: list[object] = []
            cambian = 0
            total_ops = 0
            rechazos = 0
            for md in ms:
                cerradas, con_t, rech = repetir(md, riesgo, True)
                _, sin_t, _ = repetir(md, riesgo, False)
                rechazos += len(rech)
                ops.extend(replace(o, id=f"{md.caso}/{o.id}") for o in cerradas)  # type: ignore[arg-type]
                for a, c in zip(con_t, sin_t, strict=False):
                    total_ops += 1
                    if (a.motivo, a.precio_cierre) != (c.motivo, c.precio_cierre):
                        cambian += 1
            r = evaluar_fase(ops, reglas_fase, contrato)  # type: ignore[arg-type]
            capital = reglas_fase.capital_inicial
            peor_dia = (
                max(
                    (
                        d.saldo_corte
                        - (d.equity_minima if d.equity_minima is not None else d.saldo_corte)
                    )
                    for d in r.dias
                )
                if r.dias
                else Decimal(0)
            )
            peor_total = (
                max(
                    (capital - (d.equity_minima if d.equity_minima is not None else capital))
                    for d in r.dias
                )
                if r.dias
                else Decimal(0)
            )
            suspension = (
                r.instante.isoformat()
                if r.estado is EstadoCuenta.SUSPENDIDA and r.instante
                else "-"
            )
            salida.append(
                f"{mes}: operaciones {len(ops)}; veredicto {r.estado.value}; perdida diaria maxima "
                f"{100 * peor_dia / capital:.2f} %; perdida total maxima "
                f"{100 * peor_total / capital:.2f} %; dias operados {r.dias_de_trading}; "
                f"saldo final {r.saldo_final:.2f}; suspende en {suspension}; "
                f"desenlace cambia entre ticks y respaldo en {cambian} de {total_ops}; "
                f"rechazadas por limite del perfil {rechazos}"
            )
    Path(argv[1]).write_text("\n".join(salida) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(salida))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
