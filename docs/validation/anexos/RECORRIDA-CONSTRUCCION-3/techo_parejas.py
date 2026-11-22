"""La meta de ADR-0098 sobre la corrida (3): el techo del trader (M1) y el R de las parejas (M2).

Rama `trabajo/recorrida-construccion-3` (RECORRIDA-CONSTRUCCION-3.md, fase 4). Pre-registrado en
`539f7983` (ADR-0098 y `docs/plan/META-TECHO-PAREJAS.yaml`) antes de correr nada.

Uso (desde la raiz; los tres modos corren primero el control y paran si no pasa):

    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py control \\
        <salida de la corrida 1>
    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py techo \\
        <salida de la corrida 1>
    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/techo_parejas.py parejas \\
        <salida de la corrida 1> <patrones de la corrida 1> <pivote-julio.txt>

Sale con 0 si el control pasa (y, en `techo` y `parejas`, si la medida se hizo); con 4 si el control
no pasa (PARADA 4 del encargo: no se calcula ningun R del trader); con 2 ante un error de entrada.

EL MODELO (ADR-0098 §1), pieza a pieza:
- Entrada: una orden STOP en la entrada del caso, colocada al cierre de la M1 anterior al minuto de
  su llenado (en el bucle del dia, la iteracion `instante` = el minuto del llenado, que decide en
  `instante * 60000 - 1`, como el motor). Si en ese cierre la orden queda del lado malo
  (`Broker.lado_equivocado_al_colocar`, la comprobacion del broker), «no colocable», sin enviar
  nada; si se coloca y no se llena antes de que acabe su sesion, «no llenada» (se cancela en el
  cierre de la M1 del fin de la sesion). Ninguna de las dos entra en el R.
- Stop y objetivo: el stop del caso es su 0,8. El 1 se deriva con la misma regla del 0,8 que usa el
  bot: caja = |entrada - stop| / `stop_fraccion_caja`, redondeada al punto alejandose de la entrada
  (`REDONDEO_DEL_STOP[stop_fraccion_redondeo]`). El objetivo, por `objetivo_rr` sobre la
  distancia de `base_calculo_objetivo`, hacia abajo al punto (`fijar_objetivo`). Sin stop, no entra.
- Sin desfase de serie: ninguna correccion (A-16 ABIERTA).
- Gestion: el break even de RN-014 (`zona_posterior_completada` con `break_even_criterio_ruptura`,
  y el stop a la entrada en el cierre de la M1 que pasa el punto, como `se_completa_zona_de_control`
  con `break_even_condicion` = `cierre`), el objetivo, el cierre forzoso de RN-002 (los predicados
  `vence_vela_h4` y `alcanza_hora` de `primitivas_escritas`, con `cierre_forzoso_fin_ventana`) y el
  cierre de fin de dia del cableado (`cableado.py`, fin de `correr_dia`). Con dos posiciones del
  trader vivas, el break even se mira en cada una (el bot no puede tener dos) y se cuenta.
- Lote: el de la cuenta para el bot (`_lote_resuelto`, `redondear_lote` y `_lote_final` de
  `primitivas_broker.py`): saldo (`base_calculo_riesgo`) x `riesgo_por_operacion` / la distancia de
  `lotaje_base`, hacia abajo al paso, y `limitar_lote` (tope de volumen y margen libre x
  `lote_margen_libre_fraccion` al precio de conversion del instante). Por debajo del minimo, «fuera
  por el lote minimo».
- Costes: ticks de Dukascopy, comision del perfil por lado y swaps (el broker y
  `MotorCableado._a_la_cuenta`, llamado tal cual), deslizamiento 0 (`llenado.yaml` sin tocar).
- Cuenta: `CuentaViva`, una por mes, en la fase de la corrida (la primera del perfil), por el camino
  del motor y no por `evaluar_fase`. Sigue tras SUSPENDIDA (es una marca) y la salida lo dice.
- Ninguna otra regla abre o cierra (ni RN-020, RN-036, RN-029, RN-030, RN-031, RN-032, RN-035).
- Rechazos del broker al colocar o al llenar (por otra causa que el lado): «rechazada por el
  broker», con su motivo; no entran en el R.

LO QUE SE LLAMA SUELTO (sin reescribirlo): `construir_motor_cableado` (mercados de los dias dev,
reglas del broker con el calendario de cierres, reglas de la fase, llenado y contrato; sin
calentamiento), `Broker`, `CuentaViva`, `ContextoDia`, `MotorCableado._a_la_cuenta`,
`posiciones_del_bot` (PnL bruto, comision, swaps, neto y riesgo, como «### Posiciones»),
`limitar_lote`, `zona_posterior_completada`, `minuto_de_apertura`, los predicados de RN-002,
`REDONDEO_DEL_STOP` y, para las cifras, `r_neto`, `esperanza_r`, `remuestreo_por_dias`,
`perdida_diaria_maxima`, `equity_minima_del_tramo`, `medir_por_cuentas` y `punto_de_equilibrio`.
LO QUE SE REPRODUCE (vale solo si pasa el control): el dimensionado, el objetivo, el break even de
la posicion viva, el cierre forzoso y el bucle del dia.

EL CONTROL: las ordenes LLENADAS del bot en la corrida 1 («### Ordenes» y «### Posiciones»), en
su orden y con una cuenta por mes, cada una colocada en su instante real («colocada UTC», porque el
lote del bot depende del precio de conversion de ese instante) con su entrada, su stop (la
distancia de la orden) y su caja 1 real. Tiene que dar, posicion a posicion, el lote, el motivo y
el instante del cierre y el PnL neto al centimo. Un `manual` que no cae en el cierre de una M1 en
que RN-002 dispara ni en el fin del dia queda FUERA, contado con su instante, y se cierra a
mercado en ese instante para que la cuenta siga igual; si queda fuera mas de una de cada veinte,
el control no vale.

LO QUE IMPRIME (ADR-0098 §1 y §4 c): recuentos y agregados. Ninguna operacion del trader con su R,
ningun R por clase de setup, sesion o direccion; por mes, solo la cuenta (d, e y f, que ya son por
cuenta) y julio entero como diagnostico. Ningun precio, ninguna vela, ningun nivel; los dias y los
instantes que salen son de dias dev de construccion.
"""

from __future__ import annotations

import bisect
import re
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import ROUND_DOWN, Decimal
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

# la raiz del repositorio: la de esta carpeta si el guion esta en su sitio; si no (un ensayo desde
# otra carpeta), el directorio desde el que se lanza, que tiene que ser la raiz
_AQUI = Path(__file__).resolve().parents
RAIZ = _AQUI[4] if len(_AQUI) > 4 and (_AQUI[4] / "docs" / "plan").is_dir() else Path.cwd()
MS = 60_000
CIEN = Decimal(100)

# ------------------------------------------------------------------------- piezas puras


def a_puntos(precio: Decimal, escala: int) -> int:
    """Un precio del caso o de la salida, en puntos enteros; falla si no cae en un punto."""
    valor = precio * escala
    if valor != valor.to_integral_value():
        raise ValueError(f"{precio} no cae en un punto de escala {escala}")
    return int(valor)


def caja_derivada(distancia_stop: int, fraccion: Decimal, modo: str) -> int:
    """El 1 del trader: su 0,8 entre la fraccion, al punto con el redondeo del bot."""
    if distancia_stop <= 0:
        raise ValueError("distancia al stop no positiva")
    return int((Decimal(distancia_stop) / fraccion).to_integral_value(modo))


def objetivo_de(entrada: int, lado: str, base: int, multiplo: Decimal) -> int:
    """`fijar_objetivo`: entrada +/- base x multiplo, hacia abajo al punto."""
    distancia = int((Decimal(base) * multiplo).to_integral_value(ROUND_DOWN))
    return entrada + distancia if lado == "compra" else entrada - distancia


def lote_del_riesgo(
    saldo: Decimal,
    riesgo_pct: Decimal,
    distancia: int,
    escala: int,
    contrato: Decimal,
    paso: Decimal,
) -> Decimal:
    """`_lote_resuelto` y `redondear_lote`: saldo x riesgo / (distancia en precio x contrato),
    hacia abajo al paso."""
    dinero = saldo * riesgo_pct / CIEN
    lote = dinero / (Decimal(distancia) / escala * contrato)
    return (lote / paso).to_integral_value(ROUND_DOWN) * paso


@dataclass(frozen=True)
class Medida:
    """Lo de ADR-0092 §3 sobre unas operaciones: N, esperanza, percentiles, d, e y f."""

    n: int
    esperanza: Decimal | None
    percentil_bajo: Decimal | None
    percentil_alto: Decimal | None
    descartadas: int
    perdida_diaria: Fraction
    mes_perdida_diaria: str | None
    equity_minima: Fraction
    mes_equity_minima: str | None
    suspendidas: tuple[str, ...]


def lectura_techo(
    m: Medida,
    n_minimo: int,
    esperanza_min: Decimal,
    perdida_diaria_max: Fraction,
    perdida_total_max: Fraction,
    alto_minimo: Decimal,
    orden: Sequence[str],
) -> str:
    """ADR-0098 §2, el techo, leido en el orden del yaml (gana, no_gana, no_concluyente)."""
    d_ok = m.perdida_diaria < perdida_diaria_max
    e_ok = m.equity_minima >= 1 - perdida_total_max
    f_ok = not m.suspendidas
    gana = (
        m.n >= n_minimo
        and m.esperanza is not None
        and m.esperanza >= esperanza_min
        and m.percentil_bajo is not None
        and m.percentil_bajo > 0
        and d_ok
        and e_ok
        and f_ok
    )
    no_gana = (
        not (d_ok and e_ok and f_ok)
        or (m.esperanza is not None and m.esperanza < 0)
        or (m.percentil_alto is not None and m.percentil_alto < alto_minimo)
    )
    cumple = {"gana": gana, "no_gana": no_gana, "no_concluyente": True}
    return next(clave for clave in orden if cumple[clave])


def lectura_parejas(
    n: int,
    minimo: int,
    media_bot: Decimal | None,
    bajo_bot: Decimal | None,
    alto_diferencia: Decimal | None,
    ganan_min: Decimal,
    pierden_bajo: Decimal,
    pierden_alto: Decimal,
    orden: Sequence[str],
) -> str:
    """ADR-0098 §2, las parejas, en el orden del yaml (no_concluyente, ganan, pierden, ni...)."""
    cumple = {
        "no_concluyente": n < minimo,
        "ganan": media_bot is not None
        and media_bot >= ganan_min
        and bajo_bot is not None
        and bajo_bot > 0,
        "pierden": media_bot is not None
        and media_bot < pierden_bajo
        and alto_diferencia is not None
        and alto_diferencia < pierden_alto,
        "ni_una_cosa_ni_otra": True,
    }
    return next(clave for clave in orden if cumple[clave])


def salida_de(techo: str, parejas: str) -> str:
    """ADR-0098 §3: A, B, C o D (las del yaml: A gana y ganan, B gana y pierden, C no gana, D el
    resto)."""
    if techo == "gana" and parejas == "ganan":
        return "A"
    if techo == "gana" and parejas == "pierden":
        return "B"
    if techo == "no_gana":
        return "C"
    return "D"


def salida_del_pivote(parejas: int, de_mas: int, minimo_parejas: int, maximo_de_mas: int) -> str:
    """ADR-0093 §6 con los minimos de `PIVOTES-SESION-7.yaml`: las claves de sus `salidas`."""
    cumplidos = (parejas >= minimo_parejas) + (de_mas <= maximo_de_mas)
    return {2: "se_cumplen_los_dos", 1: "se_cumple_uno", 0: "no_se_cumple_ninguno"}[cumplidos]


def percentil_de_diferencias(
    diferencias: Sequence[tuple[str, Decimal]],
    dias: Sequence[str],
    *,
    replicas: int,
    semilla: int,
    percentil: int,
) -> tuple[Decimal | None, int]:
    """La diferencia emparejada por `remuestreo_por_dias`: cada pareja, una posicion con PnL igual a
    la diferencia y riesgo 1 (ADR-0098 §1, M2)."""
    from botsito.cases.criterio_fidelidad import PosicionCerrada, remuestreo_por_dias

    posiciones = [
        PosicionCerrada(dia, d, Decimal(1), False, "", Decimal(0), Decimal(0))
        for dia, d in diferencias
    ]
    return remuestreo_por_dias(
        posiciones, dias, replicas=replicas, semilla=semilla, percentil=percentil
    )


@dataclass(frozen=True)
class FilaControl:
    """Lo que el control compara de una posicion: lote, motivo, instante del cierre y PnL neto."""

    orden: str
    lote: str
    motivo: str
    cierre: str
    neto: str


def comparar_control(
    esperadas: Mapping[tuple[str, str], FilaControl],
    obtenidas: Mapping[tuple[str, str], FilaControl],
) -> list[str]:
    """Las diferencias, posicion a posicion (clave: dia y orden)."""
    salida: list[str] = []
    for clave, e in sorted(esperadas.items()):
        o = obtenidas.get(clave)
        if o is None:
            salida.append(f"{clave[0]} {clave[1]}: la repeticion no la llena")
            continue
        for campo in ("lote", "motivo", "cierre", "neto"):
            esperado, obtenido = getattr(e, campo), getattr(o, campo)
            if esperado != obtenido:
                salida.append(f"{clave[0]} {clave[1]}: {campo} {esperado} frente a {obtenido}")
    for clave in sorted(set(obtenidas) - set(esperadas)):
        salida.append(f"{clave[0]} {clave[1]}: la repeticion llena una que el motor no")
    return salida


# --------------------------------------------------------------------- lectura de salidas


def _seccion(lineas: Sequence[str], cabecera: str) -> list[list[str]]:
    i = next((k for k, ln in enumerate(lineas) if ln.startswith(cabecera)), None)
    if i is None:
        raise ValueError(f"la salida no trae «{cabecera}»")
    filas: list[list[str]] = []
    for ln in lineas[i + 1 :]:
        # la seccion acaba en la primera linea sin columnas: la vacia, la cabecera siguiente, su
        # resumen («ordenes: ...», «posiciones: ...») o «ninguna»
        if " | " not in ln or ln.startswith("#"):
            break
        filas.append([c.strip() for c in ln.split(" | ")])
    return filas


@dataclass(frozen=True)
class OrdenDelBot:
    dia: str
    id: str
    lado: str
    colocada_ms: int
    entrada: Decimal
    distancia: int
    caja1: Decimal
    esperada: FilaControl
    cierre_ms: int


def _ms(iso: str) -> int:
    return int(datetime.fromisoformat(iso).timestamp() * 1000)


def ordenes_llenadas(salida: Path) -> list[OrdenDelBot]:
    """Las ordenes del bot que se llenaron, con su posicion de «### Posiciones»."""
    lineas = salida.read_text(encoding="utf-8").splitlines()
    ordenes = {(f[0], f[2]): f for f in _seccion(lineas, "### Ordenes (")}
    resultado: list[OrdenDelBot] = []
    for p in _seccion(lineas, "### Posiciones ("):
        if len(p) != 19:
            raise ValueError(f"fila de «### Posiciones» con {len(p)} columnas")
        o = ordenes.get((p[0], p[3]))
        if o is None or len(o) != 17:
            raise ValueError(f"{p[0]} {p[3]}: posicion sin su orden en «### Ordenes»")
        resultado.append(
            OrdenDelBot(
                dia=p[0], id=p[3], lado=p[4], colocada_ms=_ms(o[3]), entrada=Decimal(o[4]),
                distancia=int(o[9]), caja1=Decimal(o[16]),
                esperada=FilaControl(p[3], p[12], p[10], p[8], p[16]),
                cierre_ms=_ms(p[8]),
            )
        )  # fmt: skip
    return resultado


# ----------------------------------------------------------------------- la repeticion


@dataclass
class Pedido:
    """Una orden que la repeticion coloca."""

    id: str
    dia: str
    lado: str
    entrada: int  # puntos
    stop: int
    caja: int  # distancia del 1, en puntos
    minuto: int  # la iteracion del bucle en que se coloca (decide en minuto * MS - 1)
    fin_minuto: int | None = None  # si sigue sin llenar en esta iteracion, se cancela
    cerrar_en_ms: int | None = None  # control: un manual fuera del control, en su instante


@dataclass
class Traza:
    """Lo que `_a_la_cuenta` y `posiciones_del_bot` leen de la traza del dia."""

    limites: tuple[tuple[str, int, int], ...]
    eventos: list[tuple[int, str, str, str]] = field(default_factory=list)
    por_fuente: dict[str, int] = field(default_factory=dict)


@dataclass
class Recuentos:
    no_colocables: int = 0
    no_llenadas: int = 0
    rechazadas: Counter[str] = field(default_factory=Counter)
    lote_minimo: int = 0
    fuera_de_ventana: int = 0
    dos_vivas: int = 0  # cierres de M1 con mas de una posicion viva
    rn002: int = 0
    fin_de_dia: int = 0
    break_even: int = 0


@dataclass
class Repeticion:
    brokers: dict[str, Any]
    trazas: dict[str, Traza]
    cuentas: list[tuple[str, Any]]  # (mes, CuentaViva), en orden
    recuentos: Recuentos
    contrato: Decimal
    reglas_broker: Any
    reglas_fase: Any


@dataclass
class Entorno:
    """Lo que la corrida usa, construido por las funciones del motor (sin correr nada)."""

    registro: Any
    mercados: Mapping[str, Any]
    reglas_broker: Any
    reglas_fase: Any
    config_llenado: Any
    contrato: Decimal
    reloj: Any
    sesiones: list[tuple[str, str, str]]
    dias: Sequence[Any]  # DiaTrader de los dias dev, en orden
    criterio: Any


def entorno(repo: Path) -> Entorno:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.config.registro import cargar_registro
    from botsito.engine import arnes, cableado
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.engine.relojes import reloj_de_las_sesiones
    from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

    criterio = cargar_criterio(repo)
    meses = list(criterio.construccion)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    dias = arnes.dias_de_construccion(repo, criterio, meses)
    perfil = cableado.perfil_del_repo(repo, None)
    motor = cableado.construir_motor_cableado(
        repo, repo / "data", criterio, config, registro, cargar_vocabulario(spec),
        reglas_ejecutables(cargar_reglas(spec)), dias, perfil, None, False,
    )  # fmt: skip
    return Entorno(
        registro=registro,
        mercados=motor.mercados,
        reglas_broker=motor.reglas_broker,
        reglas_fase=motor.reglas_fase,
        config_llenado=motor.config_llenado,
        contrato=motor.contrato,
        reloj=reloj_de_las_sesiones(registro),
        sesiones=[(s.nombre, s.desde, s.hasta) for s in config.sesiones],
        dias=dias,
        criterio=criterio,
    )


def repetir(ent: Entorno, pedidos: Sequence[Pedido]) -> Repeticion:
    """El bucle del dia del cableado, sin interprete: los pedidos, la gestion y la cuenta."""
    from botsito.domain.estructura_m1 import zona_posterior_completada
    from botsito.engine.broker import Broker, BrokerError, Rechazo, minuto_de_apertura
    from botsito.engine.cableado import MotorCableado
    from botsito.engine.cuenta import CuentaViva
    from botsito.engine.llenado import TIPO_STOP
    from botsito.engine.primitivas_broker import ContextoDia

    registro = ent.registro
    if registro.opcion("break_even_condicion") != "cierre":
        raise ValueError("break_even_condicion no es `cierre`: el guion solo reproduce esa")
    criterio_be = registro.opcion("break_even_criterio_ruptura")
    cierre_forzoso = registro.opcion("cierre_forzoso_fin_ventana") == "si"
    base_riesgo = registro.opcion("base_calculo_riesgo")
    lotaje = registro.opcion("lotaje_base")
    riesgo_pct = registro.porcentaje("riesgo_por_operacion").valor
    paso = registro.lotes("instrumento_lote_paso")
    minimo = registro.lotes("instrumento_lote_minimo")
    fraccion_margen = registro.decimal("lote_margen_libre_fraccion")
    multiplo = registro.decimal("objetivo_rr")
    base_objetivo = registro.opcion("base_calculo_objetivo")
    if registro.opcion("lote_si_no_cabe") != "limitar":
        raise ValueError("lote_si_no_cabe no es `limitar`: ADR-0098 §1 lo da por limitar")
    rn002 = _rn002(registro)
    por_dia: dict[str, list[Pedido]] = {}
    for p in pedidos:
        por_dia.setdefault(p.dia, []).append(p)
    rec = Recuentos()
    brokers: dict[str, Any] = {}
    trazas: dict[str, Traza] = {}
    cuentas: list[tuple[str, Any]] = []
    rb = ent.reglas_broker
    cuenta: Any = None
    mes_en_curso: str | None = None
    for d in ent.dias:
        clave = d.dia
        md = ent.mercados[clave]
        limites = tuple(
            (n, int(a), int(b))
            for n, a, b in ent.reloj.limites_de_sesiones(date.fromisoformat(clave), ent.sesiones)
        )
        primero = min(a for _, a, _ in limites)
        ultimo = max(b for _, _, b in limites)
        mes = clave[:7]
        if cuenta is None or mes != mes_en_curso:
            cuenta = CuentaViva(ent.reglas_fase, ent.contrato, primero * MS - 1)
            cuentas.append((mes, cuenta))
        mes_en_curso = mes
        broker = Broker(
            rb, ent.config_llenado, md.mercado(), ent.contrato, md.escala,
            saldo=_saldo_de(cuenta),
        )  # fmt: skip
        ctx = ContextoDia(broker, cuenta, ent.contrato, md.escala)
        tb = Traza(limites)
        yo = SimpleNamespace(cuenta=cuenta, reglas_broker=rb, racha=None)
        inicios = [int(v.inicio) for v in md.m1]
        pendientes_del_dia = sorted(por_dia.get(clave, []), key=lambda p: (p.minuto, p.id))
        for p in pendientes_del_dia:
            if p.minuto > ultimo:
                rec.fuera_de_ventana += 1
            elif p.minuto < primero:
                rec.fuera_de_ventana += 1
                p.minuto = primero
        fin_de: dict[str, int | None] = {}
        cerrar_en: dict[str, int] = {}
        vistos = 0
        for instante in range(primero, ultimo + 1):
            hasta_ms = instante * MS - 1
            nuevos = broker.avanzar(hasta_ms)
            vistos = MotorCableado._a_la_cuenta(
                cast(Any, yo), broker, ctx, cast(Any, tb), nuevos, vistos, hasta_ms
            )
            ctx.instante_ms = hasta_ms
            vivas = [pos for pos in broker.posiciones.values() if pos.abierta]
            if len(vivas) > 1:
                rec.dos_vivas += 1
            for pos in vivas:  # control: el manual de una regla solo del bot, en su instante
                if cerrar_en.get(pos.orden_id) == hasta_ms:
                    broker.cerrar_a_mercado(pos.id, hasta_ms)
            vivas = [pos for pos in vivas if pos.abierta]
            if vivas and cierre_forzoso and rn002(instante):
                for pos in vivas:
                    broker.cerrar_a_mercado(pos.id, hasta_ms)
                    rec.rn002 += 1
                vivas = []
            for pos in vivas:  # RN-014, en el cierre de la M1 que pasa el punto
                a = bisect.bisect_left(inicios, minuto_de_apertura(pos))
                b = bisect.bisect_left(inicios, instante)
                m1 = md.m1[a:b]
                k = zona_posterior_completada(m1, pos.lado, criterio_be)
                if k is not None and int(m1[k].fin) == instante:
                    broker.mover_stop(pos.id, pos.entrada, hasta_ms)
                    rec.break_even += 1
            for oid, fin in list(fin_de.items()):  # no llenada en su sesion
                o = broker.ordenes[oid]
                if fin is not None and instante >= fin and o.estado in ("colocada", "modificada"):
                    broker.cancelar(oid, hasta_ms)
                    rec.no_llenadas += 1
                    del fin_de[oid]
            for p in [p for p in pendientes_del_dia if p.minuto == instante]:
                if broker.lado_equivocado_al_colocar(
                    TIPO_STOP, cast(Any, p.lado), p.entrada, hasta_ms
                ):
                    rec.no_colocables += 1
                    continue
                distancia_stop = abs(p.entrada - p.stop)
                distancia = distancia_stop if lotaje == "hasta_stop_fraccion" else p.caja
                saldo = cuenta.saldo if base_riesgo == "saldo_actual" else cuenta.saldo_corte
                lote_riesgo = lote_del_riesgo(
                    saldo, riesgo_pct, distancia, md.escala, ent.contrato, paso
                )
                lote = _lote_final(broker, rb, p.lado, lote_riesgo, hasta_ms, fraccion_margen,
                                   md.escala, ent.contrato, paso, minimo)  # fmt: skip
                if lote is None:
                    rec.lote_minimo += 1
                    continue
                base = p.caja if base_objetivo == "caja_completa" else distancia_stop
                objetivo = objetivo_de(p.entrada, p.lado, base, multiplo)
                try:
                    r = broker.colocar_stop(
                        p.id, cast(Any, p.lado), p.entrada, lote, p.stop, objetivo, hasta_ms
                    )
                except BrokerError as exc:
                    raise ValueError(
                        f"{clave} {p.id}: el broker no admite la orden ({exc})"
                    ) from exc
                if isinstance(r, Rechazo):
                    rec.rechazadas[f"al colocar: {r.motivo}"] += 1
                    continue
                fin_de[p.id] = p.fin_minuto
                if p.cerrar_en_ms is not None:
                    cerrar_en[p.id] = p.cerrar_en_ms
            ctx.eventos = []
        fin_ms = ultimo * MS - 1
        for pos in list(broker.posiciones.values()):
            if pos.abierta:
                broker.cerrar_a_mercado(pos.id, fin_ms)
                rec.fin_de_dia += 1
        for o in list(broker.ordenes.values()):
            if o.estado in ("colocada", "modificada"):
                broker.cancelar(o.id, fin_ms)
                rec.no_llenadas += 1
        nuevos = broker.avanzar(fin_ms)
        MotorCableado._a_la_cuenta(
            cast(Any, yo), broker, ctx, cast(Any, tb), nuevos, vistos, fin_ms
        )
        for o in broker.ordenes.values():  # el rechazo al llenar: la orden estuvo colocada antes
            if o.estado == "rechazada" and len(o.historial) > 1:
                motivo = next(
                    (r.motivo for r in broker.traza().rechazos if r.orden_id == o.id), "?"
                )
                rec.rechazadas[f"al llenar: {motivo}"] += 1
        brokers[clave] = broker
        trazas[clave] = tb
    return Repeticion(brokers, trazas, cuentas, rec, ent.contrato, rb, ent.reglas_fase)


def _saldo_de(cuenta: Any) -> Callable[[], Decimal]:
    """El saldo realizado de la cuenta, para el margen libre del broker (como el cableado)."""
    return lambda: Decimal(cuenta.saldo)


def _lote_final(
    broker: Any,
    rb: Any,
    lado: str,
    lote_riesgo: Decimal,
    instante_ms: int,
    fraccion: Decimal,
    escala: int,
    contrato: Decimal,
    paso: Decimal,
    minimo: Decimal,
) -> Decimal | None:
    """`_lote_final` de `primitivas_broker.py`: `limitar_lote` con el margen libre del broker."""
    from botsito.engine.broker import limitar_lote

    disponible: Decimal | None = None
    precio = 0
    if rb.apalancamiento is not None:
        precio, _ = broker.precio_de_conversion(lado, instante_ms)
        disponible = broker.margen_libre() * fraccion
    lote, _ = limitar_lote(
        lote_riesgo, rb.volumen_max_lotes, disponible, precio, escala, contrato,
        rb.apalancamiento, paso, minimo,
    )  # fmt: skip
    return lote


def filas_de(rep: Repeticion) -> list[Any]:
    """`posiciones_del_bot` sobre la repeticion: el mismo calculo que «### Posiciones»."""
    from botsito.engine.cableado import posiciones_del_bot

    motor = SimpleNamespace(
        reglas_broker=rep.reglas_broker, trazas_broker=rep.trazas, brokers=rep.brokers,
        contrato=rep.contrato,
    )  # fmt: skip
    return posiciones_del_bot(cast(Any, motor))


def medida_de(
    rep: Repeticion,
    posiciones: Sequence[Any],
    dias: Sequence[str],
    criterio: Any,
    meses: Sequence[str] | None = None,
) -> Medida:
    """ADR-0092 §3 con las funciones del criterio, sobre `dias` y las cuentas de `meses`."""
    from botsito.cases.criterio_fidelidad import (
        CuentaDelTramo,
        esperanza_r,
        medir_por_cuentas,
        remuestreo_por_dias,
    )
    from botsito.engine.cuenta import EstadoCuenta

    r = criterio.rentabilidad
    corridos = set(rep.trazas)
    tramo = [
        CuentaDelTramo(
            mes,
            tuple(
                (x.dia.isoformat(), x.saldo_corte, x.saldo_final, x.equity_minima)
                for x in c.cerrar_dia_en_curso()
                if x.dia.isoformat() in corridos
            ),
            c.estado is EstadoCuenta.SUSPENDIDA,
        )
        for mes, c in rep.cuentas
        if meses is None or mes in meses
    ]
    por = medir_por_cuentas(tramo, rep.reglas_fase.capital_inicial,
                            rep.reglas_fase.base_perdida_diaria)  # fmt: skip
    bajo, descartadas = remuestreo_por_dias(
        posiciones, dias, replicas=r.replicas_remuestreo, semilla=r.semilla_remuestreo,
        percentil=r.percentil_remuestreo,
    )  # fmt: skip
    alto, _ = remuestreo_por_dias(
        posiciones, dias, replicas=r.replicas_remuestreo, semilla=r.semilla_remuestreo,
        percentil=PERCENTIL_ALTO,
    )  # fmt: skip
    return Medida(
        len(posiciones), esperanza_r(posiciones), bajo, alto, descartadas,
        por.perdida_diaria_maxima, por.mes_perdida_diaria, por.equity_minima,
        por.mes_equity_minima, por.meses_suspendidos,
    )  # fmt: skip


PERCENTIL_ALTO = 95  # se comprueba contra el yaml al cargarlo (`propios.percentil_alto`)


# ----------------------------------------------------------------------------- el control


def control(
    ent: Entorno, salida: Path
) -> tuple[bool, list[str], Repeticion, dict[tuple[str, str], Any]]:
    """Las ordenes llenadas del bot, repetidas; True si cada posicion que entra se reproduce y
    queda fuera como mucho una de cada veinte."""
    pred_rn002 = _rn002(ent.registro)
    ordenes = ordenes_llenadas(salida)
    pedidos: list[Pedido] = []
    esperadas: dict[tuple[str, str], FilaControl] = {}
    fuera: list[str] = []
    for o in ordenes:
        md = ent.mercados[o.dia]
        entrada = a_puntos(o.entrada, md.escala)
        stop = entrada - o.distancia if o.lado == "compra" else entrada + o.distancia
        caja = abs(a_puntos(o.caja1, md.escala) - entrada)
        limites = ent.reloj.limites_de_sesiones(date.fromisoformat(o.dia), ent.sesiones)
        fin_dia = max(int(b) for _, _, b in limites) * MS - 1
        cerrar: int | None = None
        if o.esperada.motivo == "manual":
            alineado = (o.cierre_ms + 1) % MS == 0
            if not (o.cierre_ms == fin_dia or (alineado and pred_rn002((o.cierre_ms + 1) // MS))):
                fuera.append(f"{o.dia} {o.id} manual en {o.esperada.cierre}")
                if not alineado:
                    raise ValueError(f"{o.dia} {o.id}: manual fuera del cierre de una M1")
                cerrar = o.cierre_ms
        if (o.colocada_ms + 1) % MS:
            raise ValueError(f"{o.dia} {o.id}: colocada fuera del cierre de una M1")
        pedidos.append(
            Pedido(
                o.id, o.dia, o.lado, entrada, stop, caja, (o.colocada_ms + 1) // MS, None, cerrar
            )  # fmt: skip
        )
        if cerrar is None:
            esperadas[(o.dia, o.id)] = o.esperada
    rep = repetir(ent, pedidos)
    fuera_ids = {(f.split()[0], f.split()[1]) for f in fuera}
    obtenidas = {
        (f.dia, f.orden_id): FilaControl(
            f.orden_id, str(f.lotes), f.cierre, f.cerrada.isoformat(), f"{f.neto:.2f}"
        )
        for f in filas_de(rep)
        if (f.dia, f.orden_id) not in fuera_ids
    }
    diferencias = comparar_control(esperadas, obtenidas)
    vale = not diferencias and len(fuera) * 20 <= len(ordenes)
    exactas = {(f.dia, f.orden_id): f for f in filas_de(rep)}
    difieren = {tuple(x.split(":")[0].split()[:2]) for x in diferencias}
    lineas = [
        "## El control (ADR-0098 §1)",
        f"posiciones del bot en la salida: {len(ordenes)}; entran en el control: {len(esperadas)}; "
        f"fuera (manual de una regla solo del bot): {len(fuera)}",
        *[f"  fuera: {f}" for f in fuera],
        "reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): "
        f"{len(esperadas) - len(difieren & set(esperadas))} de {len(esperadas)}",
        *[f"  difiere: {x}" for x in diferencias],
        "control: " + ("PASA" if vale else "NO PASA (PARADA 4: no se calcula ningun R del trader)"),
    ]
    return vale, lineas, rep, exactas


def _rn002(registro: Any) -> Callable[[int], bool]:
    from botsito.domain.velas import MinutoUtc
    from botsito.engine.primitivas import primitivas_escritas

    pred = primitivas_escritas(registro).predicados
    vence: Any = pred["vence_vela_h4"]
    alcanza: Any = pred["alcanza_hora"]
    args_vence = {"anclaje": "anclaje_h4", "antelacion": "cierre_h4_antelacion"}
    args_alcanza = {"hora": "ventana_fin", "reloj": "reloj_sesiones"}

    def dispara(instante: int) -> bool:
        # los dos predicados solo leen el instante del momento y el registro
        m = SimpleNamespace(instante=MinutoUtc(instante))
        a, b = vence(args_vence, m, None), alcanza(args_alcanza, m, None)
        return bool(a.valor.name == "SI" or b.valor.name == "SI")

    return dispara


# ------------------------------------------------------------------------------- el techo


@dataclass
class Techo:
    lineas: list[str]
    lectura: str
    rep: Repeticion
    pedidos: dict[tuple[str, str, Decimal], str]  # (dia, instante iso, entrada) -> id
    exactas: dict[tuple[str, str], Any]


def techo(ent: Entorno, meta: Mapping[str, Any]) -> Techo:
    from botsito.engine.primitivas_broker import REDONDEO_DEL_STOP

    reg = ent.registro
    fraccion = reg.fraccion("stop_fraccion_caja").valor
    modo = REDONDEO_DEL_STOP[reg.opcion("stop_fraccion_redondeo")]
    pedidos: list[Pedido] = []
    claves: dict[tuple[str, str, Decimal], str] = {}
    sin_stop = 0
    total = 0
    for d in ent.dias:
        md = ent.mercados[d.dia]
        limites = {
            n: int(b)
            for n, _, b in ent.reloj.limites_de_sesiones(date.fromisoformat(d.dia), ent.sesiones)
        }
        for k, op in enumerate(d.operaciones, start=1):
            total += 1
            if op.stop is None:
                sin_stop += 1
                continue
            entrada = a_puntos(op.entrada, md.escala)
            stop = a_puntos(op.stop, md.escala)
            caja = caja_derivada(abs(entrada - stop), fraccion, modo)
            minuto = int(op.instante.timestamp()) // 60
            pid = f"t{k}"
            pedidos.append(
                Pedido(
                    pid, d.dia, op.direccion, entrada, stop, caja, minuto, limites.get(op.sesion)
                )  # fmt: skip
            )
            claves[(d.dia, op.instante.isoformat(), op.entrada)] = pid
    rep = repetir(ent, pedidos)
    filas = [f for f in filas_de(rep) if f.riesgo > 0]
    exactas = {(f.dia, f.orden_id): f for f in filas}
    dias = [d.dia for d in ent.dias]
    m = medida_de(rep, [f.posicion for f in filas], dias, ent.criterio)
    julio = [d for d in dias if d.startswith("2026-07")]
    mj = medida_de(
        rep, [f.posicion for f in filas if f.dia.startswith("2026-07")], julio, ent.criterio,
        meses=["2026-07"],
    )  # fmt: skip
    r = ent.criterio.rentabilidad
    propios = meta["propios"]
    alto_minimo = Decimal(propios["techo_no_gana_si_percentil_alto_por_debajo_de_r"])
    lectura = lectura_techo(
        m, r.n_minimo, r.esperanza_minima_r, Fraction(r.perdida_diaria_max),
        Fraction(r.perdida_total_max), alto_minimo, meta["lecturas"]["orden_de_lectura_del_techo"],
    )  # fmt: skip
    from botsito.cases.criterio_fidelidad import punto_de_equilibrio

    equilibrio = punto_de_equilibrio([f.posicion for f in filas], r.esperanza_minima_r)
    rec = rep.recuentos
    lineas = [
        "## M1 · El techo (ADR-0098 §1)",
        f"operaciones del trader en los dias dev: {total}; sin stop: {sin_stop}; no colocables: "
        f"{rec.no_colocables}; no llenadas: {rec.no_llenadas}; fuera por el lote minimo: "
        f"{rec.lote_minimo}; fuera de la ventana: {rec.fuera_de_ventana}",
        "rechazadas por el broker, por motivo: "
        + (", ".join(f"{k} {v}" for k, v in sorted(rec.rechazadas.items())) or "ninguna"),
        f"llenadas y cerradas: {len(filas)}; cierres de M1 con mas de una posicion viva: "
        f"{rec.dos_vivas}; cierres por RN-002: {rec.rn002}; al fin del dia: {rec.fin_de_dia}; "
        f"break even movido: {rec.break_even}",
        *_lineas_medida(m, r, "todos los dias dev corridos"),
        "deslizamiento por llenado afectado que lleva la esperanza a "
        f"{r.esperanza_minima_r} R (ADR-0092 §4, sin decidir nada): "
        + ("sin definir" if equilibrio is None else f"{equilibrio:.2f} puntos"),
        f"LECTURA DEL TECHO: {lectura}"
        + (
            " (gana en construccion, con el deslizamiento pendiente de F17)"
            if lectura == "gana"
            else ""
        ),
        "",
        "### Julio de 2026, como diagnostico (sin umbral; el unico mes con video, provisional)",
        *_lineas_medida(mj, r, "los dias dev de julio"),
    ]
    return Techo(lineas, lectura, rep, claves, exactas)


def _r(x: Decimal | None) -> str:
    return "sin definir" if x is None else f"{x:.3f}"


def _pct(f: Fraction) -> str:
    return f"{float(f) * 100:.2f} %"


def _lineas_medida(m: Medida, r: Any, sobre: str) -> list[str]:
    return [
        f"a) N (llenadas y cerradas): {m.n}",
        f"b) esperanza (media del R neto): {_r(m.esperanza)}",
        f"c) percentil {r.percentil_remuestreo} y percentil {PERCENTIL_ALTO} de la media del R "
        f"neto, por remuestreo por dias ({r.replicas_remuestreo} replicas, semilla "
        f"{r.semilla_remuestreo}, {sobre}): {_r(m.percentil_bajo)} y {_r(m.percentil_alto)}; "
        f"replicas descartadas: {m.descartadas}",
        f"d) perdida diaria maxima, por cuenta: {_pct(m.perdida_diaria)} del capital inicial; la "
        f"peor, la cuenta de {m.mes_perdida_diaria}",
        f"e) equity minima, por cuenta: {_pct(m.equity_minima)} del capital inicial; la peor, la "
        f"cuenta de {m.mes_equity_minima}",
        "f) alguna cuenta entro en SUSPENDIDA: "
        + (f"si ({', '.join(m.suspendidas)})" if m.suspendidas else "no"),
    ]


# ----------------------------------------------------------------------------- las parejas

T0 = re.compile(
    r"^T0 [^:]*: trader \| (\d{4}-\d{2}-\d{2}) \| [^|]+ \| [^|]+ \| (\S+) \| (\S+) \| "
    r"PAREJA bot (\S+) (\S+) \("
)
PIVOTE_T0 = re.compile(r"^T0 \(parejas\): (\d+)$")
PIVOTE_DE_MAS = re.compile(r"^operaciones de mas \(P5 \+ P6 en sesion\): (\d+)$")


def parejas(
    ent: Entorno,
    meta: Mapping[str, Any],
    pivotes: Mapping[str, Any],
    t: Techo,
    exactas_bot: Mapping[tuple[str, str], Any],
    patrones: Path,
    pivote: Path,
) -> list[str]:
    from botsito.cases.criterio_fidelidad import r_neto, remuestreo_por_dias

    r = ent.criterio.rentabilidad
    propios = meta["propios"]
    minimo = _clave(pivotes, propios["parejas_minimo_desde"])
    pos_bot = {(f.dia, f.llenada.isoformat(), f.entrada): f for f in exactas_bot.values()}
    pares: list[tuple[str, Decimal, Decimal]] = []
    sin_trader: Counter[str] = Counter()
    sin_bot = 0
    t0_mes: Counter[str] = Counter()
    for ln in patrones.read_text(encoding="utf-8").splitlines():
        m = T0.match(ln)
        if not m:
            continue
        dia, inst_t, ent_t, inst_b, ent_b = m.groups()
        t0_mes[dia[:7]] += 1
        fb = pos_bot.get((dia, inst_b, Decimal(ent_b)))
        if fb is None:
            sin_bot += 1
            continue
        pid = t.pedidos.get((dia, inst_t, Decimal(ent_t)))
        ft = None if pid is None else t.exactas.get((dia, pid))
        if ft is None:
            sin_trader[
                "sin pata del trader (no colocable, no llenada, rechazada o lote minimo)"
                if pid is not None
                else "la operacion del trader no esta en los casos"
            ] += 1
            continue
        pares.append((dia, r_neto(fb.posicion), r_neto(ft.posicion)))
    dias = [d.dia for d in ent.dias]
    n = len(pares)
    media_bot = sum((b for _, b, _ in pares), Decimal(0)) / n if n else None
    media_trader = sum((x for _, _, x in pares), Decimal(0)) / n if n else None
    diferencias = [(dia, b - x) for dia, b, x in pares]
    media_dif = sum((d for _, d in diferencias), Decimal(0)) / n if n else None
    from botsito.cases.criterio_fidelidad import PosicionCerrada

    bot_pos = [
        PosicionCerrada(dia, b, Decimal(1), False, "", Decimal(0), Decimal(0))
        for dia, b, _ in pares
    ]
    kw = {"replicas": r.replicas_remuestreo, "semilla": r.semilla_remuestreo}
    bajo_bot, _ = remuestreo_por_dias(bot_pos, dias, percentil=r.percentil_remuestreo, **kw)
    alto_bot, _ = remuestreo_por_dias(bot_pos, dias, percentil=PERCENTIL_ALTO, **kw)
    bajo_dif, _ = percentil_de_diferencias(diferencias, dias, percentil=r.percentil_remuestreo,
                                           **kw)  # fmt: skip
    alto_dif, _ = percentil_de_diferencias(diferencias, dias, percentil=PERCENTIL_ALTO, **kw)
    lectura = lectura_parejas(
        n, minimo, media_bot, bajo_bot, alto_dif,
        Decimal(propios["parejas_ganan_media_bot_al_menos_r"]),
        Decimal(propios["parejas_pierden_media_bot_por_debajo_de_r"]),
        Decimal(propios["parejas_pierden_percentil_alto_de_la_diferencia_por_debajo_de_r"]),
        list(meta["lecturas"]["parejas"]),
    )  # fmt: skip
    salida = salida_de(t.lectura, lectura)
    texto_pivote = pivote.read_text(encoding="utf-8").splitlines()
    p_t0 = next(int(mm.group(1)) for ln in texto_pivote if (mm := PIVOTE_T0.match(ln)))
    p_mas = next(int(mm.group(1)) for ln in texto_pivote if (mm := PIVOTE_DE_MAS.match(ln)))
    minimos = pivotes["minimos"]
    s_pivote = salida_del_pivote(
        p_t0, p_mas, minimos["minimo_1_parejas_de_julio_al_menos"],
        minimos["minimo_2_operaciones_de_mas_de_julio_como_mucho"],
    )  # fmt: skip
    return [
        "## M2 · Las parejas (ADR-0098 §1)",
        "filas T0 de la corrida 1, por mes: "
        + ", ".join(f"{k} {v}" for k, v in sorted(t0_mes.items())),
        f"parejas con las dos patas: {n}; sin pata del trader: {sum(sin_trader.values())}"
        + "".join(f"; {k}: {v}" for k, v in sorted(sin_trader.items()))
        + f"; sin la posicion del bot: {sin_bot}",
        f"media del R neto del bot en sus parejas: {_r(media_bot)}; del trader en las mismas "
        f"operaciones: {_r(media_trader)}; diferencia emparejada media (bot - trader): "
        f"{_r(media_dif)}",
        f"percentiles {r.percentil_remuestreo} y {PERCENTIL_ALTO} por remuestreo por dias "
        f"({r.replicas_remuestreo} replicas, semilla {r.semilla_remuestreo}, {len(dias)} dias): "
        f"del bot {_r(bajo_bot)} y {_r(alto_bot)}; de la diferencia {_r(bajo_dif)} y "
        f"{_r(alto_dif)}",
        f"minimo de parejas ({propios['parejas_minimo_desde']}): {minimo}",
        f"LECTURA DE LAS PAREJAS: {lectura}",
        "",
        "## La salida (ADR-0098 §3)",
        f"techo: {t.lectura}; parejas: {lectura}",
        f"SALIDA: {salida} ({meta['salidas'][salida]})",
        f"pivote de ADR-0093 §6 (de {pivote.name}): parejas de julio {p_t0}, operaciones de mas "
        f"{p_mas}, minimos {minimos['minimo_1_parejas_de_julio_al_menos']} y "
        f"{minimos['minimo_2_operaciones_de_mas_de_julio_como_mucho']}: {s_pivote} "
        f"({' '.join(str(pivotes['salidas'][s_pivote]).split())})",
        f"PRECEDENCIA CON EL PIVOTE ({salida}): {meta['precedencia_con_el_pivote'][salida]}",
    ]


def _clave(doc: Mapping[str, Any], referencia: str) -> int:
    _, _, ruta = str(referencia).partition(", ")
    nodo: Any = doc
    for parte in ruta.split("."):
        nodo = nodo[parte]
    return int(nodo)


# ---------------------------------------------------------------------------------- main


def _cargar_meta(repo: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    from botsito.comun.yaml_estricto import leer_yaml

    meta = leer_yaml(repo / "docs" / "plan" / "META-TECHO-PAREJAS.yaml")
    pivotes = leer_yaml(repo / "docs" / "plan" / "PIVOTES-SESION-7.yaml")
    if meta.get("decision") != "ADR-0098":
        raise ValueError("META-TECHO-PAREJAS.yaml no es el de ADR-0098")
    if int(meta["propios"]["percentil_alto"]) != PERCENTIL_ALTO:
        raise ValueError("el percentil alto del yaml no es el del guion")
    return meta, pivotes


def main(argv: Sequence[str]) -> int:
    cast(Any, sys.stdout).reconfigure(encoding="utf-8")
    if len(argv) < 2 or argv[0] not in ("control", "techo", "parejas"):
        print(__doc__)
        return 2
    modo, salida = argv[0], Path(argv[1])
    if modo == "parejas" and len(argv) != 4:
        print("parejas pide <salida> <patrones> <pivote-julio.txt>")
        return 2
    meta, pivotes = _cargar_meta(RAIZ)
    ent = entorno(RAIZ)
    vale, lineas, _rep_bot, exactas_bot = control(ent, salida)
    print(f"# techo_parejas.py {modo}, sobre {salida.name} (ADR-0098; RECORRIDA-CONSTRUCCION-3)")
    print()
    print("\n".join(lineas))
    if not vale:
        return 4
    if modo == "control":
        return 0
    t = techo(ent, meta)
    print()
    print("\n".join(t.lineas))
    if modo == "techo":
        return 0
    print()
    print("\n".join(parejas(ent, meta, pivotes, t, exactas_bot, Path(argv[2]), Path(argv[3]))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
