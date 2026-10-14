"""Punto 4.b de la respuesta del consultor a la PARADA 3 (trabajo/corrida-construccion,
2026-10-14): sobre las sesiones con operaciones del trader de una salida del arnes, la tabla 2x2
«la H4 que fijo el sesgo rompio el extremo de su anterior SOLO con la mecha (cerro dentro) o con
el cierre fuera» frente a «el trader opero a favor o en contra del sesgo del bot», y aparte las
sesiones cuyo sesgo se decidio por doble ruptura o en la segunda vela o mas atras. Y la lista de
las sesiones de P1 con ruptura solo de mecha (dia, sesion y hora UTC de esa H4).

ES UN DIAGNOSTICO PARA ARMAR LA PREGUNTA DE LA SESION 5, NO UNA MEDIDA QUE DECIDA EL PARAMETRO:
`sesgo_h4_criterio_ruptura` sigue en `mecha` (fb-2026-09-09-sesion-01-8eccf5c0) y los parametros
no se optimizan contra resultados.

Las velas se cargan como el arnes (`arnes.dias_de_mercado`, el mismo calentamiento) y solo se
leen velas de construccion (ADR-0021 §1). «Cierre dentro» = el cierre de la H4 que rompio no pasa
el extremo roto de la anterior (con el criterio `mecha`, el extremo es el maximo o el minimo);
«cierre fuera» = lo pasa. Una sesion es «a favor» si TODAS sus operaciones del trader van con el
sesgo del bot, «en contra» si ninguna, «mixta» si hay de los dos.

Uso: uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/sesgo_2x2.py <raiz> <salida>
"""

from __future__ import annotations

import sys
from collections import Counter
from collections.abc import Sequence
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patrones import A_FAVOR, clasificar, leer  # noqa: E402

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.cli import _carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.velas import a_datetime  # noqa: E402
from botsito.domain.sesgo import _extremos, sesgo_h4  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.relojes import reloj_de_las_sesiones  # noqa: E402

SOLO_MECHA = "ruptura solo con mecha (cierre dentro)"
CIERRE_FUERA = "ruptura con cierre fuera"
DOBLE = "doble ruptura decidida por el color"
SEGUNDA = "decidida en la segunda vela o mas atras"
INSUFICIENTE = "insuficiente"


def como_rompio(
    velas: Sequence[Vela], apertura: MinutoUtc, tope: int, criterio: str
) -> tuple[str, Vela | None]:
    """La clase de la ruptura que fijo el sesgo y la H4 que lo fijo."""
    r = sesgo_h4(velas, apertura, tope, criterio)
    if r.sesgo.value == INSUFICIENTE:
        return INSUFICIENTE, None
    cerradas = sorted((v for v in velas if v.fin <= apertura), key=lambda v: v.inicio)
    vela = cerradas[-r.velas_miradas]
    if r.doble_ruptura:
        return DOBLE, vela
    if r.velas_miradas > 1:
        return SEGUNDA, vela
    ant = cerradas[-2]
    alto_ant, bajo_ant = _extremos(ant, criterio)
    if r.sesgo.value == "alcista":
        return (CIERRE_FUERA if vela.cierre > alto_ant else SOLO_MECHA), vela
    return (CIERRE_FUERA if vela.cierre < bajo_ant else SOLO_MECHA), vela


def main(repo: Path, salida: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    filas, sesgo_motor = leer(salida)
    clasificadas = clasificar(filas, sesgo_motor)
    p1 = {tuple(f.split(" | ")[1:3]) for p, _, _, f in clasificadas if p == "P1 sesgo"}
    # el lado del trader frente al sesgo del bot, por sesion
    lados: dict[tuple[str, str], set[str]] = {}
    for quien, dia, sesion, lado, _, _, _ in filas:
        if quien == "trader":
            s = sesgo_motor.get((dia, sesion), "?")
            lados.setdefault((dia, sesion), set()).add(
                "a favor" if (lado, s) in A_FAVOR else "en contra"
            )
    sesiones = sorted(lados)
    print(f"{salida.name}: {len(sesiones)} sesiones con operaciones del trader; {len(p1)} de P1")
    criterio = cargar_criterio(repo)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    reloj = reloj_de_las_sesiones(registro)
    dias = arnes.dias_de_construccion(repo, criterio, list(criterio.construccion))
    mercado = arnes.dias_de_mercado(repo, _carpeta_datos(repo), config, registro, dias, reloj)
    tope = registro.entero("sesgo_h4_tope_velas")
    crit = registro.opcion("sesgo_h4_criterio_ruptura")
    desde = {s.nombre: s.desde for s in config.sesiones}
    print(f"tope {tope}, criterio {crit}")
    tabla: Counter[tuple[str, str]] = Counter()
    aparte: Counter[tuple[str, str]] = Counter()
    p1_mecha: list[str] = []
    for dia, sesion in sesiones:
        d = date.fromisoformat(dia)
        apertura = reloj.instante(d, desde[sesion])
        velas = mercado[dia].datos.velas_h4_cerradas(int(apertura))
        clase, vela = como_rompio(velas, apertura, tope, crit)
        lado = next(iter(lados[(dia, sesion)])) if len(lados[(dia, sesion)]) == 1 else "mixta"
        if clase in (SOLO_MECHA, CIERRE_FUERA):
            tabla[(clase, lado)] += 1
        else:
            aparte[(clase, lado)] += 1
        if (dia, sesion) in p1 and clase == SOLO_MECHA and vela is not None:
            h4 = f"{a_datetime(vela.inicio):%Y-%m-%dT%H:%MZ}"
            p1_mecha.append(f"{dia} {sesion} | H4 {h4} | {sesgo_motor.get((dia, sesion))}")
    print("-- tabla 2x2 (sesiones con el sesgo fijado por la ultima H4 cerrada, ruptura simple):")
    print("ruptura | a favor | en contra | mixta | total")
    for clase in (SOLO_MECHA, CIERRE_FUERA):
        n = {k: tabla[(clase, k)] for k in ("a favor", "en contra", "mixta")}
        print(f"{clase} | {n['a favor']} | {n['en contra']} | {n['mixta']} | {sum(n.values())}")
    print("-- aparte:")
    for (clase, lado), n in sorted(aparte.items()):
        print(f"{clase} | {lado} | {n}")
    print(f"-- sesiones de P1 con ruptura solo de mecha: {len(p1_mecha)} de {len(p1)}")
    for ln in p1_mecha:
        print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
