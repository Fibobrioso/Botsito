"""Medicion DESCRIPTIVA de A-21 sobre construccion (abril y agosto), por la compuerta del arnes.
Fase 3 de `trabajo/preparar-a21`. No decide nada: cuenta.

Por cada lectura de `zona_control_limpia` (A-21), con A-35 (`cierre_vela_contraria`) y A-44
(`sin_tope`) tambien en hipotesis: en cuantas sesiones del trader se forma una zona de entrada, en
cuantas operaciones del trader la ENTRADA cae dentro de la zona vigente segun esa lectura, en
cuantas la direccion coincide con el lado de la zona, y cuantas operaciones ocurren antes de que
exista ninguna zona. La zona vigente es la que el productor del motor tendria en ese instante: el
esquema detectado desde la PRIMERA toma del dia (`liquidez_tomada` no caduca al abrir la sesion).
Imprime dias de CONSTRUCCION, sesiones, horas y recuentos; ninguna entrada, ningun stop, ningun
resultado del trader.

  `uv run python scripts/verificacion_a21.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import UTC
from decimal import Decimal
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie  # noqa: E402
from botsito.domain.estructura_m1 import LECTURAS_LIMPIA, detectar_esquema  # noqa: E402
from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA  # noqa: E402
from botsito.domain.sesgo import sesgo_h4  # noqa: E402
from botsito.domain.velas import MinutoUtc  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico  # noqa: E402
from botsito.engine.interprete import Interprete, reglas_ejecutables  # noqa: E402
from botsito.engine.motor import DatosMercado, MotorSpec, _minuto_utc  # noqa: E402
from botsito.engine.perfil_cuenta import cargar_perfil  # noqa: E402
from botsito.engine.primitivas import primitivas_escritas  # noqa: E402
from botsito.engine.tope_trader import tope_del_registro  # noqa: E402
from botsito.engine.visor import _stops  # noqa: E402
from botsito.engine.zonas import LADO_ENTRADA, LOOKBACK_M1  # noqa: E402
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario  # noqa: E402


def _minuto(instante) -> int:  # type: ignore[no-untyped-def]
    return int(instante.astimezone(UTC).timestamp() // 60)


def _hhmm(minuto: int) -> str:
    return f"{(minuto // 60) % 24:02d}:{minuto % 60:02d}"


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: verificacion_a21.py --salida <fichero>", file=sys.stderr)
        return 2
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    huso = registro.texto("huso_operativa")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    carpeta = carpeta_datos(RAIZ)
    mercado = arnes.dias_de_mercado(
        RAIZ, carpeta, config, registro, dias, huso, CIERRE_VELA_CONTRARIA
    )
    ruta = buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{criterio.construccion[0]}")
    escala = cargar_serie(cargar_manifiesto(ruta), carpeta).escala
    spec = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
    voc, reglas = cargar_vocabulario(spec), reglas_ejecutables(cargar_reglas(spec))
    perfil = next(iter(sorted((RAIZ / "knowledge" / "cuentas").glob("*.yaml"))))
    tope = tope_del_registro(
        registro, cargar_perfil(perfil).huso_corte(), Diagnostico(a44=A44_SIN_TOPE)
    )
    tope_zonas = registro.entero("zonas_control_max_por_esquema")
    criterio_breaker = registro.opcion("breaker_m1_criterio_ruptura")
    tope_sesgo = registro.entero("sesgo_h4_tope_velas")
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    lineas = [
        "# Verificacion A-21: medicion descriptiva sobre construccion (DIAGNOSTICO)",
        f"CONJUNTO: construccion ({', '.join(criterio.construccion)}); dias {len(dias)}; "
        f"operaciones del trader {sum(len(d.operaciones) for d in dias)}",
        "HIPOTESIS: A-35 cierre_vela_contraria; A-44 sin_tope; A-21 cada lectura. Nada de esto "
        "vale para elegir una lectura: la elige el trader, no el ajuste.",
        "",
    ]
    for limpia in LECTURAS_LIMPIA:
        motor = MotorSpec(Interprete(voc, primitivas_escritas(registro, tope, limpia)), reglas)
        sesiones_con_zona = 0
        sesiones_trader = 0
        dentro = fuera = sin_zona = misma_dir = 0
        detalle: list[str] = []
        esquemas: Counter[str] = Counter()
        minutos_rn004: list[int] = []
        coincide_rn011 = no_coincide_rn011 = 0
        cajas: dict[tuple[str, int], int] = {}  # (dia, breaker_fin) -> caja en puntos
        stops_trader: list[int] = []  # |entrada - stop| del trader, en puntos
        for d in dias:
            dm = mercado[d.dia]
            datos: DatosMercado = dm.datos
            r = motor.correr_dia(dm)
            aperturas = {s.nombre: int(_minuto_utc(dm.dia, s.desde, huso)) for s in dm.sesiones}
            con_trader = {op.sesion for op in d.operaciones}
            for nombre in sorted(con_trader):
                sesiones_trader += 1
                tz = r.sesiones[nombre]
                if "RN-011" in tz.disparadas:
                    sesiones_con_zona += 1
                # H3: cuantos minutos fija RN-004 `liquidez_tomada`, y si RN-011 cae en uno de ellos
                t_rn004 = {
                    t for t, rg, h, _ in tz.fijados if rg == "RN-004" and h == "liquidez_tomada"
                }
                t_rn011 = {t for t, rg, h, _ in tz.fijados if rg == "RN-011"}
                if t_rn004:
                    minutos_rn004.append(len(t_rn004))
                if t_rn011 & t_rn004:
                    coincide_rn011 += 1
                elif t_rn011:
                    no_coincide_rn011 += 1
            stops = _stops(RAIZ, d)  # el stop del trader vive en el caso, como lo lee el visor
            for op, stop in zip(d.operaciones, stops, strict=True):
                t_ap = aperturas.get(op.sesion)
                if t_ap is None:
                    continue
                sesgo = sesgo_h4(
                    datos.velas_h4_cerradas(t_ap), MinutoUtc(t_ap), tope_sesgo, criterio_ruptura
                ).sesgo.value
                lado = LADO_ENTRADA.get(sesgo)
                t_op = _minuto(op.instante)
                # la toma: el primer instante DEL DIA en que RN-004 fijo el hecho, como el productor
                # (`liquidez_tomada` no caduca al abrir la sesion: solo `sesgo` lo hace)
                tomas = sorted(
                    t
                    for tz in r.sesiones.values()
                    for t, _, h, _ in tz.fijados
                    if h == "liquidez_tomada" and t <= t_op
                )
                esquema = None
                if lado is not None and tomas:
                    toma = tomas[0]
                    m1 = datos.m1_entre(toma - LOOKBACK_M1, t_op)
                    idx = next((k for k, v in enumerate(m1) if int(v.fin) == toma), None)
                    if idx is not None:
                        esquema = detectar_esquema(
                            m1, idx, lado, criterio_breaker, tope_zonas, limpia
                        )
                hora = op.instante.astimezone(UTC).strftime("%H:%M")
                if stop is not None:
                    stops_trader.append(
                        abs(int(((Decimal(op.entrada) - stop) * escala).to_integral_value()))
                    )
                if esquema is None:
                    sin_zona += 1
                    continue
                esquemas[esquema.cual] += 1
                cajas[(d.dia, int(esquema.breaker_fin))] = abs(esquema.entrada - esquema.extremo)
                entrada = int((Decimal(op.entrada) * escala).to_integral_value())
                lo, hi = sorted((esquema.entrada, esquema.extremo))
                cae = lo <= entrada <= hi
                dentro += cae
                fuera += not cae
                misma_dir += op.direccion == esquema.lado
                detalle.append(
                    f"- {d.dia} {op.sesion} {hora}Z ({op.direccion}): zona {esquema.lado} del "
                    f"{esquema.cual}, formada {_hhmm(int(esquema.breaker_fin))}Z, "
                    f"{'DENTRO' if cae else 'fuera'} de la zona"
                    f"{'' if op.direccion == esquema.lado else '; direccion contraria a la zona'}"
                )
        lineas += [
            f"## A-21 = {limpia} (DIAGNOSTICO-A21-{limpia})",
            f"sesiones del trader en las que RN-011 liga una zona: {sesiones_con_zona} de "
            f"{sesiones_trader}",
            f"operaciones del trader con una zona vigente antes de su entrada: {dentro + fuera}; "
            f"sin zona todavia (o sin lado, o sin toma): {sin_zona}",
            f"  la entrada cae DENTRO de la zona: {dentro}; fuera: {fuera}",
            f"  la direccion coincide con el lado de la zona: {misma_dir}",
            f"  por esquema: {dict(esquemas)}",
            "  caja de las zonas vigentes (puntos, una por zona): "
            + (
                f"min {min(cajas.values())}, mediana {median(cajas.values())}, "
                f"max {max(cajas.values())}, n {len(cajas)}"
                if cajas
                else "ninguna"
            ),
            "  distancia entrada-stop del trader en sus operaciones (puntos): "
            + (
                f"min {min(stops_trader)}, mediana {median(stops_trader)}, "
                f"max {max(stops_trader)}, "
                f"n {len(stops_trader)}"
                if stops_trader
                else "sin stop en el caso"
            ),
            "H3 (aviso «disparador RN-004, RN-011»): minutos por sesion del trader en que RN-004 "
            f"vuelve a fijar liquidez_tomada: min {min(minutos_rn004) if minutos_rn004 else '-'}, "
            f"max {max(minutos_rn004) if minutos_rn004 else '-'}; sesiones en las que RN-011 "
            f"dispara en un minuto en que RN-004 tambien fija: {coincide_rn011}; en otro minuto: "
            f"{no_coincide_rn011}",
            *detalle,
            "",
        ]
    Path(argv[1]).write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
