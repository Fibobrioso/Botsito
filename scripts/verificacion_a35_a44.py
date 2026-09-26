"""Medicion DESCRIPTIVA de A-35 y A-44 sobre construccion (abril y agosto), por la compuerta del
arnes. Fase 3 de la verificacion de `trabajo/preparar-a35-a44`. No decide nada: cuenta.

(a) operaciones del trader cuyo toque de la liquidez ocurre DENTRO de la vela contraria que marca
    el pivote, despues de que esa vela haya empezado a ir contraria: donde las dos lecturas de A-35
    divergirian si la toma se evaluara dentro de la vela;
(b) operaciones del trader cuya liquidez se toma con cuerpo en una M1 dentro de una M15 todavia
    abierta: cuantos minutos antes del cierre de esa M15 y cuantos antes de la entrada;
(c) las sesiones del trader en las que RN-004 no toma liquidez, clasificadas por causa.

El pivote es el mas reciente ya formado del lado que fija el sesgo de la sesion (RN-005), con la
lectura `cierre_vela_contraria` como referencia y `inicio_vela_contraria` para saber desde cuando
la contraria iba contraria. Imprime dias de CONSTRUCCION, sesiones, minutos y recuentos; ninguna
entrada, ningun stop, ningun resultado del trader.

  `uv run python scripts/verificacion_a35_a44.py --salida <fichero>`
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import UTC
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.domain.pivotes_m15 import (  # noqa: E402
    CIERRE_VELA_CONTRARIA,
    INICIO_VELA_CONTRARIA,
    Pivote,
    cruza,
    toca,
)
from botsito.domain.sesgo import sesgo_h4  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.motor import DatosMercado, _minuto_utc  # noqa: E402
from botsito.engine.primitivas import LADO_DE_LA_LIQUIDEZ  # noqa: E402

M15 = 15


def _hhmm(minuto: int) -> str:
    return f"{(minuto // 60) % 24:02d}:{minuto % 60:02d}"


def _minuto(instante) -> int:  # type: ignore[no-untyped-def]
    return int(instante.astimezone(UTC).timestamp() // 60)


def _primer_minuto_contrario(datos: DatosMercado, p: Pivote, lado: str) -> int | None:
    """Con la lectura `inicio`: el primer cierre de M1 dentro de la contraria en que el pivote
    (esta misma contraria) ya estaba a la vista."""
    for t in range(int(p.contraria_inicio) + 1, int(p.contraria_fin)):
        q = datos.liquidez_m15(t, lado)
        if q is not None and q.contraria_inicio == p.contraria_inicio and q.nivel == p.nivel:
            return t
    return None


def _toque_m1(velas: list[Vela], p: Pivote) -> Vela | None:
    for v in velas:
        if toca(v, p):
            return v
    return None


def _toma_m1(velas: list[Vela], p: Pivote) -> Vela | None:
    for v in velas:
        if cruza(v, p, "cuerpo"):
            return v
    return None


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: verificacion_a35_a44.py --salida <fichero>", file=sys.stderr)
        return 2
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    huso = registro.texto("huso_operativa")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    carpeta = carpeta_datos(RAIZ)
    por_lectura = {
        lectura: arnes.dias_de_mercado(RAIZ, carpeta, config, registro, dias, huso, lectura)
        for lectura in (CIERRE_VELA_CONTRARIA, INICIO_VELA_CONTRARIA)
    }
    tope = registro.entero("sesgo_h4_tope_velas")
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    lineas: list[str] = [
        "# Verificacion A-35 / A-44: medicion descriptiva sobre construccion",
        f"CONJUNTO: construccion ({', '.join(criterio.construccion)}); dias {len(dias)}; "
        f"operaciones del trader {sum(len(d.operaciones) for d in dias)}",
        "REFERENCIA: pivote mas reciente ya formado (ADR-0045) del lado del sesgo (RN-005), "
        "lectura cierre_vela_contraria; `inicio_vela_contraria` dice desde cuando la contraria "
        "iba contraria",
        "",
    ]

    # ---------------------------------------------------------------- (a) y (b), por operacion
    a_casos: list[str] = []
    b_filas: list[tuple[int, int]] = []  # (min antes del cierre de la M15, min antes de la entrada)
    b_casos: list[str] = []
    sin_lado = sin_pivote = 0
    entra_antes_del_cierre_m15 = 0
    for d in dias:
        dm_c = por_lectura[CIERRE_VELA_CONTRARIA][d.dia]
        dm_i = por_lectura[INICIO_VELA_CONTRARIA][d.dia]
        datos_c: DatosMercado = dm_c.datos
        datos_i: DatosMercado = dm_i.datos
        aperturas = {s.nombre: int(_minuto_utc(dm_c.dia, s.desde, huso)) for s in dm_c.sesiones}
        for op in d.operaciones:
            t_ap = aperturas.get(op.sesion)
            if t_ap is None:
                continue
            sesgo = sesgo_h4(
                datos_c.velas_h4_cerradas(t_ap), MinutoUtc(t_ap), tope, criterio_ruptura
            ).sesgo.value
            lado = LADO_DE_LA_LIQUIDEZ.get(sesgo)
            if lado is None:
                sin_lado += 1
                continue
            t_op = _minuto(op.instante)
            p = datos_c.liquidez_m15(t_op, lado)
            if p is None:
                sin_pivote += 1
                continue
            hora = op.instante.astimezone(UTC).strftime("%H:%M")
            etiqueta = f"{d.dia} {op.sesion} {hora}Z ({op.direccion}, sesgo {sesgo}, pivote {lado})"
            # (a) toque dentro de la contraria, despues de que fuera contraria
            t_contrario = _primer_minuto_contrario(datos_i, p, lado)
            if t_contrario is not None:
                dentro = datos_c.m1_entre(t_contrario - 1, int(p.contraria_fin))
                v = _toque_m1(dentro, p)
                if v is not None:
                    a_casos.append(
                        f"- {etiqueta}: la contraria (empieza {_hhmm(int(p.contraria_inicio))}Z) "
                        f"va contraria desde su minuto {t_contrario - int(p.contraria_inicio)} y "
                        f"toca el nivel en su minuto {int(v.inicio) - int(p.contraria_inicio) + 1} "
                        f"(de {M15}, al cierre de la M1 de las {_hhmm(int(v.inicio) + 1)}Z); la "
                        f"entrada es {t_op - int(p.contraria_fin)} min despues del cierre de la "
                        "contraria"
                    )
            # (b) la toma con cuerpo en M1, dentro de una M15 todavia abierta
            despues = datos_c.m1_entre(int(p.contraria_fin), t_op)
            v = _toma_m1(despues, p)
            if v is not None:
                cierre_m1 = int(v.inicio) + 1
                fin_m15 = int(p.contraria_fin) + M15 * (
                    (cierre_m1 - 1 - int(p.contraria_fin)) // M15 + 1
                )
                antes_cierre = fin_m15 - cierre_m1
                antes_entrada = t_op - cierre_m1
                b_filas.append((antes_cierre, antes_entrada))
                if t_op < fin_m15:
                    entra_antes_del_cierre_m15 += 1
                b_casos.append(
                    f"- {etiqueta}: la toma en M1 cierra {antes_cierre} min antes del cierre de su "
                    f"M15 y {antes_entrada} min antes de la entrada"
                    + ("; la entrada es ANTERIOR al cierre de esa M15" if t_op < fin_m15 else "")
                )
    lineas += [
        "## (a) Toque de la liquidez DENTRO de la vela contraria (donde las lecturas divergirian)",
        f"operaciones con sesgo sin lado (ambiguo/insuficiente): {sin_lado}; sin pivote del lado "
        f"formado antes de la entrada: {sin_pivote}",
        f"operaciones cuyo pivote fue tocado dentro de su vela contraria, tras ir contraria: "
        f"{len(a_casos)}",
        *a_casos,
        "",
        "## (b) Toma con cuerpo en M1 dentro de una M15 todavia abierta",
        f"operaciones con una toma en M1 antes de la entrada: {len(b_filas)}",
    ]
    if b_filas:
        antes_c = sorted(x for x, _ in b_filas)
        antes_e = sorted(y for _, y in b_filas)
        lineas += [
            f"minutos antes del cierre de la M15: min {antes_c[0]}, mediana {median(antes_c)}, "
            f"max {antes_c[-1]}",
            f"minutos antes de la entrada: min {antes_e[0]}, mediana {median(antes_e)}, "
            f"max {antes_e[-1]}",
            f"entradas ANTERIORES al cierre de la M15 en la que la M1 tomo el nivel: "
            f"{entra_antes_del_cierre_m15}",
        ]
    lineas += [*b_casos, ""]

    # ---------------------------------------------------------------- (c) sesiones sin toma
    from botsito.engine.diagnostico import A44_SIN_TOPE, Diagnostico
    from botsito.engine.interprete import Interprete, reglas_ejecutables
    from botsito.engine.motor import MotorSpec
    from botsito.engine.perfil_cuenta import cargar_perfil
    from botsito.engine.primitivas import primitivas_escritas
    from botsito.engine.tope_trader import tope_del_registro
    from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

    spec = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
    perfil = next(iter(sorted((RAIZ / "knowledge" / "cuentas").glob("*.yaml"))))
    tope_diag = tope_del_registro(
        registro, cargar_perfil(perfil).huso_corte(), Diagnostico(a44=A44_SIN_TOPE)
    )
    motor = MotorSpec(
        Interprete(cargar_vocabulario(spec), primitivas_escritas(registro, tope_diag)),
        reglas_ejecutables(cargar_reglas(spec)),
    )
    causas: Counter[str] = Counter()
    detalle: list[str] = []
    for d in dias:
        dm = por_lectura[CIERRE_VELA_CONTRARIA][d.dia]
        datos: DatosMercado = dm.datos
        r = motor.correr_dia(dm)
        con_trader = {op.sesion for op in d.operaciones}
        limites = {
            s.nombre: (
                int(_minuto_utc(dm.dia, s.desde, huso)),
                int(_minuto_utc(dm.dia, s.hasta, huso)),
            )
            for s in dm.sesiones
        }
        for nombre in sorted(con_trader):
            traza = r.sesiones[nombre]
            if "liquidez_tomada" in traza.hechos_producidos:
                continue
            desde, hasta = limites[nombre]
            sesgo = sesgo_h4(
                datos.velas_h4_cerradas(desde), MinutoUtc(desde), tope, criterio_ruptura
            ).sesgo.value
            lado = LADO_DE_LA_LIQUIDEZ.get(sesgo)
            if lado is None:
                causa = f"sesgo {sesgo}: sin lado, no hay liquidez marcada (RN-033 prohibe)"
            else:
                pivotes = {
                    (q.contraria_inicio, q.nivel): q
                    for t in range(desde, hasta + 1)
                    if (q := datos.liquidez_m15(t, lado)) is not None
                }
                if not pivotes:
                    causa = "sin pivote del lado del sesgo a la vista en la sesion"
                else:
                    tocado = tomado = False
                    for q in pivotes.values():
                        velas = datos.m1_entre(max(int(q.formado_en) - M15, desde), hasta)
                        m15s = [datos.ultima_m15_cerrada(t) for t in range(desde, hasta + 1)]
                        for m in {v.inicio: v for v in m15s if v is not None}.values():
                            if int(q.formado_en) < int(m.fin) and toca(m, q):
                                tocado = True
                                if cruza(m, q, "cuerpo"):
                                    tomado = True
                        del velas
                    if tomado:
                        causa = (
                            "una M15 cerro con cuerpo al otro lado, pero fuera de la sesion o con "
                            "el hecho ya vivo"
                        )
                    elif tocado:
                        causa = "el pivote se toco (mecha) pero ninguna M15 cerro con cuerpo"
                    else:
                        causa = "hay pivote del lado del sesgo, pero el precio no volvio a su nivel"
            causas[causa] += 1
            detalle.append(f"- {d.dia} {nombre}: {causa}")
    lineas += [
        "## (c) Sesiones del trader en las que RN-004 no toma liquidez, por causa",
        f"sesiones: {sum(causas.values())}",
        *(f"- {n}: {c}" for c, n in causas.most_common()),
        *detalle,
        "",
    ]
    Path(argv[1]).write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {argv[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
