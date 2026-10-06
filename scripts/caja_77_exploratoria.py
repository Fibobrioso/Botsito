"""La parte EXPLORATORIA de CAJA-77 (docs/validation/CAJA-77.md §3), pedida por el consultor DESPUES
de ver el resultado y sin cambiar el veredicto: la tabla de «solo el 0» por direccion, el placebo
del 0 (la entrada desplazada) y, para R5, su pivote frente a la referencia del breaker que el
productor fija en la toma de la liquidez de la sesion.

No toca `caja_77.py` ni su salida, que es la pre-registrada: importa sus piezas. El productor corre
como en `scripts/embudo_77.py`, en DIAGNOSTICO (A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21
`solo_una_zona_de_control`, A-27 a 0). Solo lee; escribe SOLO en --salida.

    uv run python scripts/caja_77_exploratoria.py --salida <fichero> [--raiz <repo>]
"""

from __future__ import annotations

import argparse
import bisect
import sys
from collections import Counter
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

RAIZ_SCRIPT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ_SCRIPT / "src"))
sys.path.insert(0, str(RAIZ_SCRIPT / "scripts"))

import bloque_de_la_caja as bc  # noqa: E402
import caja_77 as c77  # noqa: E402

from botsito.domain.estructura_m1 import COMPRA, VENTA  # noqa: E402
from botsito.domain.pivotes_m15 import (  # noqa: E402
    ALTO,
    BAJO,
    CIERRE_VELA_CONTRARIA,
    Pivote,
    pivotes_formados,
)
from botsito.domain.velas import Vela  # noqa: E402

DESPLAZAMIENTOS = (-10, -5, 0, 5, 10)  # + hacia el stop, - hacia la ruptura
A21 = "solo_una_zona_de_control"


# ----------------------------------------------------------------------- 1. solo el 0 por lado


def solo_el_cero(filas: Sequence[c77.Fila]) -> list[str]:
    salida = [
        "## 1. «Solo el 0» (tau 2, sin correccion), por regla, lectura y direccion",
        "Celda: solo el 0 (el 0 a <= 2 y el 1 no) / el 0 a <= 2 en total (aciertos + solo el 0)",
        "| regla | ventas L0,8 | ventas L1 | compras L0,8 | compras L1 | todas L0,8 | todas L1 |",
        "|---|---|---|---|---|---|---|",
    ]
    grupos = (
        [f for f in filas if f.op.lado == VENTA],
        [f for f in filas if f.op.lado == COMPRA],
        list(filas),
    )
    cuentas = [{lec: c77.recuento(g, lec, c77.TAU, 0) for lec in c77.LECTURAS} for g in grupos]
    for r in c77.REGLAS:
        celdas = []
        for c in cuentas:
            for lec in c77.LECTURAS:
                x = c[lec][r]
                celdas.append(f"{x['solo_0']} / {x['acierta'] + x['solo_0']}")
        salida.append(f"| {r} | " + " | ".join(celdas) + " |")
    n = [len(g) for g in grupos]
    salida.append(f"n: ventas {n[0]}, compras {n[1]}, todas {n[2]}")
    return [*salida, ""]


# ------------------------------------------------------------------------- 2. placebo del 0


def placebo(filas: Sequence[c77.Fila]) -> list[str]:
    salida = [
        "## 2. Placebo del 0: la entrada desplazada, mismo T y mismas velas "
        "(tau 2, sin correccion)",
        "Aciertos del 0 (|0 de la regla - 0 desplazado| <= 2). Desplazamiento + hacia el stop, "
        "- hacia la ruptura (en una venta, + es hacia arriba; en una compra, hacia abajo). "
        "0 = la entrada real.",
        "| regla | " + " | ".join(f"{d:+d}" for d in DESPLAZAMIENTOS) + " |",
        "|---|" + "---|" * len(DESPLAZAMIENTOS),
    ]
    for r in c77.REGLAS:
        celdas = []
        for d in DESPLAZAMIENTOS:
            n = 0
            for f in filas:
                caja = f.cajas[r]
                if caja is None:
                    continue
                signo = 1 if f.op.lado == VENTA else -1
                if abs(caja[0] - (f.op.entrada + signo * d)) <= c77.TAU:
                    n += 1
            celdas.append(str(n))
        salida.append(f"| {r} | " + " | ".join(celdas) + " |")
    salida.append(f"n = {len(filas)}")
    return [*salida, ""]


# ------------------------------------------------- 3. el pivote de R5 frente a la referencia


def tomas_del_productor(raiz: Path) -> dict[tuple[str, str], dict[str, Any]]:
    """La toma de la liquidez que el productor guarda en cada sesion, como en embudo_77.py."""
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.holdout import casos_ocultos
    from botsito.cases.paquete import cargar_config
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import ParametroDesconocidoError, cargar_registro
    from botsito.engine import arnes, cableado, diagnostico, entrada, relojes, tope_trader, zonas
    from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

    criterio = cargar_criterio(raiz)
    registro = cargar_registro(raiz / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(raiz / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = raiz / "knowledge" / "spec" / "strategy_spec.yaml"
    vocabulario = cargar_vocabulario(spec)
    reglas = reglas_ejecutables(cargar_reglas(spec))
    meses = list(criterio.construccion)
    dias = arnes.dias_de_construccion(raiz, criterio, meses, ocultos=casos_ocultos(raiz))
    try:
        fijado: str | None = registro.opcion(entrada.PARAMETRO_A47)
    except ParametroDesconocidoError:
        fijado = None
    a47 = None if fijado is not None else entrada.STOP_EN_RUPTURA
    diag = Diagnostico(CIERRE_VELA_CONTRARIA, A44_SIN_TOPE, A21, 0, a47)
    lectura = diagnostico.lectura_pivote(registro, diag)
    perfil = cableado.perfil_del_repo(raiz, None)
    tope = tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag)
    limpia = zonas.lectura_limpia(registro, diag.a21)
    tipo_orden = entrada.lectura_tipo_orden(registro, diag.a47)
    carpeta = carpeta_datos(raiz)
    mercado = arnes.dias_de_mercado(
        raiz, carpeta, config, registro, dias, relojes.reloj_de_las_sesiones(registro), lectura
    )
    motor = cableado.construir_motor_cableado(
        raiz, carpeta, criterio, config, registro, vocabulario, reglas, dias, perfil, None, False,
        tope, limpia, stops_level_diagnostico=0, tipo_orden=tipo_orden,
    )  # fmt: skip
    arnes.correr(cableado.NOMBRE_MOTOR, tuple(sorted(set(meses))), dias, mercado, motor)
    salida: dict[tuple[str, str], dict[str, Any]] = {}
    for d in dias:
        for s in mercado[d.dia].sesiones:
            mem = zonas.memoria_de_sesion(motor.estados[d.dia], s.nombre)
            if mem.get("toma") is not None:
                salida[(d.dia, s.nombre)] = {
                    "toma": mem["toma"],
                    "esquema": mem.get("esquema"),
                    "lookback": zonas.LOOKBACK_M1,
                }
    return salida


def pivote_de_referencia(
    velas: list[Vela], inicios: list[int], toma: int, lado: str, lookback: int
) -> Pivote | None:
    """El pivote que `referencia_del_breaker` da en la toma: el ultimo contrario a la entrada
    formado con las M1 de [toma - lookback, toma], la de la toma incluida."""
    a = bisect.bisect_left(inicios, toma - lookback)
    b = bisect.bisect_right(inicios, toma - 1)
    m1 = velas[a:b]
    if not m1 or int(m1[-1].fin) != toma:
        return None
    contrario = ALTO if lado == COMPRA else BAJO
    for p in reversed(pivotes_formados(m1, None, CIERRE_VELA_CONTRARIA, toma, len(m1))):
        if p.lado == contrario:
            return p
    return None


def r5_frente_a_la_referencia(
    raiz: Path, filas: Sequence[c77.Fila], velas: list[Vela], inicios: list[int]
) -> list[str]:
    sesiones = tomas_del_productor(raiz)
    clases: Counter[str] = Counter()
    lineas: list[str] = []
    distancias_min: list[int] = []
    for f in filas:
        o = f.op
        sesion = _sesion_de_la_operacion(raiz, o)
        dato = sesiones.get((o.dia, sesion)) if sesion else None
        v = c77.ventana(inicios, velas, o.minuto)
        r5 = bc.pivote_de_ruptura(v, o.lado)
        if r5 is None:
            clases["R5 sin pivote"] += 1
            continue
        nivel, _, ic = r5
        r5_contraria = int(v[ic].inicio)
        if dato is None:
            clases["sin toma del productor en su sesion"] += 1
            continue
        toma = int(dato["toma"]["instante"])
        if toma > o.minuto:
            clases["la toma de su sesion llega despues de T"] += 1
            continue
        if str(dato["toma"]["lado"]) != o.lado:
            clases["la toma es del lado contrario a la operacion"] += 1
            continue
        ref = pivote_de_referencia(velas, inicios, toma, o.lado, int(dato["lookback"]))
        if ref is None:
            clases["sin referencia en la toma"] += 1
            continue
        esquema = dato["esquema"]
        con_esquema = esquema is not None and int(esquema.breaker_fin) <= o.minuto
        mismo = nivel == ref.nivel and r5_contraria == int(ref.contraria_inicio)
        if mismo:
            clase = "el MISMO pivote que la referencia"
        elif r5_contraria > toma:
            clase = "un pivote formado DESPUES de la toma"
        else:
            clase = "otro pivote formado ANTES de la toma"
        clases[clase] += 1
        dmin = r5_contraria - toma
        distancias_min.append(dmin)
        lineas.append(
            f"| {c77.clave(o)} | {clase} | {nivel - ref.nivel:+d} | {dmin:+d} | "
            f"{'si' if con_esquema else 'no'} |"
        )
    total = sum(clases.values())
    salida = [
        "## 3. R5: su pivote frente a la referencia del breaker del productor en la toma",
        "Toma: la de la sesion de la operacion en el productor (diagnostico); referencia: el "
        "ultimo pivote contrario formado hasta la vela de la toma (= Esquema.referencia cuando "
        "hay esquema).",
        "Mismo pivote = mismo nivel y misma vela contraria.",
        *(f"- {k}: {v} de {total}" for k, v in clases.most_common()),
    ]
    if distancias_min:
        s = sorted(distancias_min)
        salida.append(
            f"minutos de la vela contraria del pivote de R5 a la toma (+ despues): mediana "
            f"{s[len(s) // 2]:+d}, de {s[0]:+d} a {s[-1]:+d}"
        )
    salida += [
        "",
        "| op | clase | nivel R5 - referencia | minutos desde la toma | esquema antes de T |",
        "|---|---|---|---|---|",
        *lineas,
        "",
    ]
    return salida


_SESIONES: dict[tuple[str, datetime], str] = {}


def _sesion_de_la_operacion(raiz: Path, o: c77.Op) -> str | None:
    if not _SESIONES:
        from botsito.cases.ingesta import DIRECTORIO_DEV
        from botsito.comun.yaml_estricto import leer_yaml

        for ruta in sorted((raiz / DIRECTORIO_DEV).glob("caso-*.yaml")):
            doc = leer_yaml(ruta)
            dia = str(doc["dia"])
            if dia[:7] not in c77.MESES:
                continue
            for op in doc.get("operaciones") or []:
                t = datetime.fromisoformat(str(op["instante_utc"]).replace("Z", "+00:00"))
                _SESIONES[(dia, t.astimezone(UTC))] = str(op["sesion"])
    return _SESIONES.get((o.dia, o.t))


# --------------------------------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--salida", required=True, type=Path)
    p.add_argument("--raiz", type=Path, default=RAIZ_SCRIPT)
    args = p.parse_args(argv)
    raiz = args.raiz.resolve()
    ops, _ = c77.cargar_operaciones(raiz)
    if len(ops) != c77.ESPERADAS:
        print(f"PARADA: {len(ops)} operaciones, se esperaban {c77.ESPERADAS}")
        return 3
    velas = c77.cargar_velas(raiz)
    inicios = [int(v.inicio) for v in velas]
    filas = []
    for o in ops:
        v = c77.ventana(inicios, velas, o.minuto)
        if o.fuera() is None and v:
            filas.append(c77.Fila(o, {r: f(v, o.lado) for r, f in c77.REGLAS.items()}))
    lineas = [
        "# CAJA-77, parte EXPLORATORIA (posterior a ver el resultado; no cambia el veredicto)",
        f"evaluables: {len(filas)}",
        "",
        *solo_el_cero(filas),
        *placebo(filas),
        *r5_frente_a_la_referencia(raiz, filas, velas, inicios),
    ]
    args.salida.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {args.salida}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
