"""La lista «Entradas antes de la alternancia» (RECORRIDA-CONSTRUCCION, decision 5 del encargo y
respuesta del consultor a la PARADA, puntos 0, 1 y 2): cada orden LLENADA del bot cuyo llenado
ocurrio con menos de dos zonas de control formadas desde la toma de su escenario, que es donde
muerde RN-009 (ADR-0076 §2 y su NOTA; ADR-0085 §4).

Solo LEE. Construye el motor EXACTAMENTE como `cli.motor_arnes` (las mismas llamadas, en el mismo
orden), con la cuenta reiniciada cada dia: REPRODUCE LA CORRIDA 2 (`--diagnostico-cuenta-diaria`),
no la 1. Corre los cuatro meses de construccion y despues lee la memoria del motor; no cambia
ninguna decision. Antes de escribir nada comprueba que sus ordenes llenadas coinciden una a una,
linea a linea, con las `llenada` de «### Ordenes» de la salida de la corrida 2 (`--diaria`); si
difieren, sale con 3 (PARADA) y no se ajusta nada.

Por cada orden llenada:
- zonas al llenar: `estructura_m1.zonas_de_control` desde la toma de su escenario con las M1
  cerradas hasta el ultimo cierre anterior al instante del llenado (lo que RN-009 ve en ese
  cierre); y zonas al colocar, lo mismo en el cierre que coloco la orden;
- donde estaba: la posicion del punto de su zona frente a la toma, por `contraria_inicio`
  (`referencia`: formado antes del cierre de la toma; `primer punto tras la toma`; `posterior`);
- reubicaciones: cuantas ordenes anteriores del mismo escenario cancelo RN-006 antes de ella;
- escenario: el de su zona y, si es otro, el vigente al llenar (la zona reutilizada en un
  escenario nuevo, PUNTO-USADO.md §1.c);
- su resultado en R (sobre el riesgo con el que nacio) y si la empareja el trader (la medida del
  criterio) o su patron (P5 o P6, con la copia de `patrones.py` de esta carpeta).

Lo que imprime cumple la regla de la rama: nada anterior a las 00:00Z del dia dev (se escribe
«(antes del dia)»); ninguna H4, ningun pivote de M15, ninguna vela.

    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION/entradas_antes_alternancia.py
        --diaria <salida de la corrida 2> --salida <fichero>
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import patrones  # noqa: E402  (la copia de esta carpeta)

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.cases.relojes import reloj_de_las_sesiones  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.domain.estructura_m1 import zonas_de_control  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO  # noqa: E402
from botsito.engine import arnes, cableado, diagnostico, entrada, tope_trader, zonas  # noqa: E402
from botsito.engine.interprete import reglas_ejecutables  # noqa: E402
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario  # noqa: E402

REFERENCIA = "referencia"
PRIMERO = "primer punto tras la toma"
POSTERIOR = "posterior"
OCULTO = "(antes del dia)"
REGLA_REUBICA = "RN-006"
# menos de dos zonas de control: donde muerde RN-009 (zonas_control_max_por_esquema = 1)
TOPE_LISTA = 2
MARCA_ROTULO = "[DIAGNOSTICO"
CABECERA = (
    "dia | sesion | orden | lado | llenada UTC | entrada | zonas al llenar | zonas al colocar | "
    "donde | punto | reubicaciones | escenario | R | pareja o patron"
)


@dataclass(frozen=True)
class Llenada:
    """Una orden llenada, ya leida: lo que la lista imprime."""

    dia: str
    sesion: str
    orden: str
    lado: str
    llenada: str
    entrada: str
    zonas_llenar: int
    zonas_colocar: int
    donde: str
    punto: str
    reubicaciones: int
    escenario: str
    r: str
    pareja: str


# ------------------------------------------------------------------ las reglas puras de la lista


def donde_esta(punto_inicio: int, toma_instante: int, inicios_tras_toma: Sequence[int]) -> str:
    """La posicion del punto de la orden frente a la toma: la referencia se forma con las M1 hasta
    la de la toma incluida, asi que su vela contraria empieza ANTES del cierre de la toma; los
    puntos de despues empiezan en el cierre de la toma o mas tarde, y el primero de ellos es el
    primer punto tras la toma."""
    if punto_inicio < toma_instante:
        return REFERENCIA
    if inicios_tras_toma and punto_inicio == min(inicios_tras_toma):
        return PRIMERO
    return POSTERIOR


def reubicaciones_antes(
    colocada_ms: int,
    ordenes_del_escenario: Mapping[str, int],
    cancelaciones: Sequence[tuple[int, str, str]],
) -> int:
    """Cuantas ordenes del mismo escenario, colocadas antes que esta, se cancelaron con RN-006
    entre las reglas disparadas en el cierre que las cancelo (`cableado._motivo_de_cancelacion`):
    RN-006 reubica cancelando, y RN-011 y RN-015 colocan otra en el punto nuevo."""
    motivo_de = {id: motivo for _, id, motivo in cancelaciones}
    return sum(
        1
        for id, ms in ordenes_del_escenario.items()
        if ms < colocada_ms and REGLA_REUBICA in motivo_de.get(id, "")
    )


def en_la_lista(fila: Llenada) -> bool:
    """Entra en la lista la llenada con menos de dos zonas de control al llenar."""
    return fila.zonas_llenar < TOPE_LISTA


def fila_texto(f: Llenada) -> str:
    return (
        f"{f.dia} | {f.sesion} | {f.orden} | {f.lado} | {f.llenada} | {f.entrada} | "
        f"{f.zonas_llenar} | {f.zonas_colocar} | {f.donde} | {f.punto} | {f.reubicaciones} | "
        f"{f.escenario} | {f.r} | {f.pareja}"
    )


def sin_rotulo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(MARCA_ROTULO) and "] " in ln else ln


def llenadas_de_ordenes(lineas: Sequence[str]) -> list[str]:
    """Las filas `llenada` de la seccion «### Ordenes (...)» de una salida del arnes, sin rotulo
    y tal cual (la comparacion es linea a linea)."""
    salida: list[str] = []
    dentro = False
    for ln in lineas:
        c = sin_rotulo(ln)
        if c.startswith("### Ordenes ("):
            dentro = True
            continue
        if dentro and (c.startswith("### ") or c.startswith("ordenes: ")):
            break
        if dentro and c.split(" | ")[5:6] == [cableado.RESULTADO_LLENADA]:
            salida.append(c)
    return salida


# ------------------------------------------------------------------------- el motor y la lectura


def construir_y_correr() -> tuple[Any, Mapping[str, Any], Any, Any]:
    """El motor como `cli.motor_arnes` (cli.py, `motor_arnes`), con la cuenta reiniciada cada dia.
    Devuelve (motor, mercado, corrida, criterio)."""
    repo = RAIZ
    criterio = cargar_criterio(repo)
    meses = list(criterio.construccion)
    arnes.validar_meses(criterio, meses)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    vocabulario = cargar_vocabulario(spec)
    dias = arnes.dias_de_construccion(repo, criterio, meses)
    lectura = diagnostico.lectura_pivote(registro)
    perfil = cableado.perfil_del_repo(repo, None)
    tope = tope_trader.tope_del_registro(registro, perfil.huso_corte())
    limpia = zonas.lectura_limpia(registro)
    tipo_orden = entrada.lectura_tipo_orden(registro, None)
    datos = carpeta_datos(repo)
    mercado = arnes.dias_de_mercado(
        repo, datos, config, registro, dias, reloj_de_las_sesiones(registro), lectura
    )
    reglas = reglas_ejecutables(cargar_reglas(spec))
    motor = cableado.construir_motor_cableado(
        repo,
        datos,
        criterio,
        config,
        registro,
        vocabulario,
        reglas,
        dias,
        perfil,
        None,
        False,
        tope,
        limpia,
        stops_level_diagnostico=None,
        tipo_orden=tipo_orden,
    )
    motor.cuenta_diaria = True  # la corrida 2: la cuenta, el seguidor y la racha, de cero cada dia
    corrida = arnes.correr(cableado.NOMBRE_MOTOR, tuple(sorted(set(meses))), dias, mercado, motor)
    return motor, mercado, corrida, criterio


def _zonas_hasta(datos: Any, toma_instante: int, lado: str, hasta_minuto: int) -> int | None:
    """`zonas_de_control` desde la toma con las M1 cerradas hasta `hasta_minuto` incluido (las
    que `m1_entre` da con inicio anterior a el), como `zonas_desarrolladas_superan`."""
    m1 = datos.m1_entre(toma_instante - zonas.LOOKBACK_M1, hasta_minuto)
    idx = next((k for k, v in enumerate(m1) if int(v.fin) == toma_instante), None)
    if idx is None:
        return None
    if idx >= len(m1) - 1:
        return 0
    return int(zonas_de_control(m1, idx, len(m1) - 1, lado))


def _r_de(p: Any, escala: int) -> str:
    """El resultado en R sobre el riesgo con el que nacio la posicion (su stop original)."""
    stop0 = p.stop_original if p.stop_original is not None else p.stop
    riesgo = abs(int(p.entrada) - int(stop0))
    if p.precio_cierre is None:
        return "abierta"
    if riesgo == 0:
        return f"sin riesgo ({p.motivo_cierre})"
    signo = 1 if p.lado == "compra" else -1
    r = Decimal(signo * (int(p.precio_cierre) - int(p.entrada))) / Decimal(riesgo)
    return f"{r:+.2f} ({p.motivo_cierre})"


def _inicio_del_dia(dia: str) -> int:
    d = date.fromisoformat(dia)
    return int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp() // 60)


def _punto_texto(clave: str, inicio_dia: int) -> str:
    nivel, _, inicio = clave.partition("@")
    return OCULTO if int(inicio) < inicio_dia else clave


def leer_llenadas(
    motor: Any, mercado: Mapping[str, Any], corrida: Any, criterio: Any, diaria: Path
) -> list[Llenada]:
    """Una fila por orden llenada, leyendo la memoria del motor despues de correr."""
    medida = arnes.medida_de(corrida, criterio)
    parejas = {
        (p.bot.dia, p.bot.sesion, p.bot.instante.isoformat(), str(p.bot.entrada))
        for p in medida.parejas
    }
    filas_p, sesgo = patrones.leer(diaria)
    patron_bot = {
        tuple(fila.split(" | ")[1:6]): patron
        for patron, _, _, fila in patrones.clasificar(filas_p, sesgo)
        if fila.startswith("bot | ")
    }
    salida: list[Llenada] = []
    for dia in sorted(motor.trazas_broker):
        broker = motor.brokers[dia]
        tb = motor.trazas_broker[dia]
        estado = motor.estados[dia]
        datos = mercado[dia].datos
        escala = broker.escala
        inicio_dia = _inicio_del_dia(dia)
        pos_de_orden = {p.orden_id: p for p in broker.posiciones.values()}
        for o in sorted(broker.ordenes.values(), key=lambda o: (o.colocada_ms, o.id)):
            p = pos_de_orden.get(o.id)
            if p is None:
                continue
            sesion = cableado._sesion_de(o.colocada_ms, tb.limites)
            mem = zonas.memoria_de_sesion(estado, sesion)
            punto_de_zona = mem.get("punto_de_zona", {})
            zona_id = tb.zona_de_orden.get(o.id)
            esc = zonas.escenario_de_zona(estado, sesion, zona_id) if zona_id else None
            cierre_llenado = p.abierta_ms // MS_POR_MINUTO
            cierre_colocado = (o.colocada_ms + 1) // MS_POR_MINUTO
            if esc is None or zona_id is None:
                z_ll = z_co = -1
                donde, punto, reub, texto_esc = "sin escenario", "-", 0, "-"
            else:
                toma = esc["toma"]
                toma_inst, lado = int(toma["instante"]), str(toma["lado"])
                z_ll = _zonas_hasta(datos, toma_inst, lado, cierre_llenado) or 0
                z_co = _zonas_hasta(datos, toma_inst, lado, cierre_colocado) or 0
                clave = str(punto_de_zona.get(zona_id, "-"))
                inicios = [
                    int(str(punto_de_zona[z]).partition("@")[2])
                    for z in esc["zonas"]
                    if z in punto_de_zona
                ]
                tras = [i for i in inicios if i >= toma_inst]
                donde = (
                    donde_esta(int(clave.partition("@")[2]), toma_inst, tras)
                    if "@" in clave
                    else "sin punto"
                )
                punto = _punto_texto(clave, inicio_dia) if "@" in clave else clave
                del_escenario = {
                    oid: broker.ordenes[oid].colocada_ms
                    for oid, zid in tb.zona_de_orden.items()
                    if zid in esc["zonas"] and oid in broker.ordenes
                }
                reub = reubicaciones_antes(o.colocada_ms, del_escenario, tb.cancelaciones)
                escenarios = list(mem.get("escenarios") or [])
                vigentes = [e for e in escenarios if int(e["toma"]["instante"]) <= cierre_llenado]
                vigente = vigentes[-1] if vigentes else None
                texto_esc = f"n {esc['n']}"
                if vigente is not None and vigente is not esc:
                    texto_esc += f" (vigente al llenar: n {vigente['n']})"
            llenada = datetime.fromtimestamp(p.abierta_ms / 1000, UTC).isoformat()
            entrada_txt = str(Decimal(int(p.entrada)) / escala)
            clave_bot = (dia, sesion, str(p.lado), llenada, entrada_txt)
            pareja = (
                "T0 pareja"
                if (dia, sesion, llenada, entrada_txt) in parejas
                else patron_bot.get(clave_bot, "sin fila en «Diferencias»")
            )
            salida.append(
                Llenada(
                    dia,
                    sesion,
                    o.id,
                    str(p.lado),
                    llenada,
                    entrada_txt,
                    z_ll,
                    z_co,
                    donde,
                    punto,
                    reub,
                    texto_esc,
                    _r_de(p, escala),
                    pareja,
                )
            )
    return salida


def resumen(filas: Sequence[Llenada]) -> list[str]:
    lista = [f for f in filas if en_la_lista(f)]
    lineas = [
        f"llenadas: {len(filas)}; en la lista (zonas al llenar < {TOPE_LISTA}): {len(lista)}; "
        f"fuera (2 o mas zonas): {len(filas) - len(lista)}",
    ]
    for titulo, clave in (
        ("por mes", lambda f: f.dia[:7]),
        ("por zonas al llenar", lambda f: str(f.zonas_llenar)),
        ("por donde", lambda f: f.donde),
        ("por reubicaciones", lambda f: str(f.reubicaciones)),
        ("por pareja o patron", lambda f: f.pareja),
    ):
        c: Counter[str] = Counter(clave(f) for f in lista)
        lineas.append(f"  {titulo}: " + ", ".join(f"{k} {v}" for k, v in sorted(c.items())))
    return lineas


def main(diaria: Path, salida: Path) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    motor, mercado, corrida, criterio = construir_y_correr()
    propias = llenadas_de_ordenes(cableado._informe_ordenes(motor))
    de_la_diaria = llenadas_de_ordenes(diaria.read_text(encoding="utf-8").splitlines())
    if propias != de_la_diaria:
        print("ORDENES llenadas frente a «### Ordenes» de la corrida 2: DISTINTAS -> PARADA")
        for i in range(max(len(propias), len(de_la_diaria))):
            a = propias[i] if i < len(propias) else None
            b = de_la_diaria[i] if i < len(de_la_diaria) else None
            if a != b:
                print(f"  fila {i + 1}: aqui {a} | corrida 2 {b}")
        return 3
    filas = leer_llenadas(motor, mercado, corrida, criterio, diaria)
    lineas = [
        "# Entradas antes de la alternancia (RECORRIDA-CONSTRUCCION, decision 5)",
        f"MOTOR: {cableado.NOMBRE_MOTOR}; cuenta reiniciada cada dia (reproduce la corrida 2)",
        f"ORDENES llenadas frente a «### Ordenes» de la corrida 2: iguales ({len(propias)})",
        "zonas al llenar: zonas_de_control desde la toma del escenario de la zona de la orden, "
        "con las M1 cerradas hasta el ultimo cierre anterior al llenado (lo que RN-009 ve); "
        "zonas al colocar: lo mismo en el cierre que coloco la orden",
        "donde: la posicion del punto de la orden frente a la toma, por contraria_inicio; "
        "reubicaciones: ordenes anteriores del mismo escenario canceladas por RN-006; "
        "escenario: el de la zona y, si es otro, el vigente al llenar; R: sobre el riesgo con "
        "el que nacio la posicion; pareja o patron: T0 si la empareja el trader (criterio), "
        "si no el patron de patrones.py sobre la corrida 2",
        "",
        f"## En la lista (zonas al llenar < {TOPE_LISTA})",
        CABECERA,
        *[fila_texto(f) for f in filas if en_la_lista(f)],
        "",
        "## Resumen",
        *resumen(filas),
        "",
        "## Todas las llenadas (contexto)",
        CABECERA,
        *[fila_texto(f) for f in filas],
    ]
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {salida} ({len(filas)} llenadas, {sum(en_la_lista(f) for f in filas)} en la lista)")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--diaria", required=True, type=Path, help="la salida de la corrida 2")
    p.add_argument("--salida", required=True, type=Path, help="el fichero que se escribe")
    a = p.parse_args()
    raise SystemExit(main(a.diaria, a.salida))
