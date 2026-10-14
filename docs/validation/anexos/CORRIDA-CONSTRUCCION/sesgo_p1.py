"""Punto 5 de la respuesta del consultor a la PARADA 2 (trabajo/corrida-construccion, 2026-10-14):
para cada sesion del patron P1 (operaciones del trader contra el sesgo del bot), las dos ultimas
H4 cerradas antes de la apertura -hora UTC de inicio, apertura, maximo, minimo y cierre en
nuestras velas-, el sesgo de la sesion y el de la sesion anterior del mismo dia, y la regla que
decidio cada uno: RN-003 por ruptura simple, la doble ruptura decidida por el color (ADR-0060) o
una vela neutra con doble ruptura saltada (ADR-0075). Lee SOLO velas de construccion (ADR-0021 §1),
con el mismo calentamiento que el arnes (`arnes.dias_de_mercado`), y la salida del arnes para
saber que sesiones son P1 y que sesgo anoto el motor.

Uso: uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/sesgo_p1.py <raiz del repo> <salida>
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from datetime import date
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patrones import clasificar, leer  # noqa: E402

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.cli import _carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.velas import a_datetime  # noqa: E402
from botsito.domain.sesgo import _extremos, sesgo_h4  # noqa: E402
from botsito.domain.velas import MinutoUtc, Vela  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.relojes import reloj_de_las_sesiones  # noqa: E402


def _regla(velas: Sequence[Vela], apertura: MinutoUtc, tope: int, criterio: str) -> str:
    """La regla que decidio el sesgo, mirando lo mismo que `sesgo_h4` mira."""
    r = sesgo_h4(velas, apertura, tope, criterio)
    if r.sesgo.value == "insuficiente":
        return f"insuficiente tras {r.velas_miradas} velas (RN-033)"
    cerradas = sorted((v for v in velas if v.fin <= apertura), key=lambda v: v.inicio)
    saltadas_neutras = 0
    for k in range(1, r.velas_miradas):  # las velas miradas antes de la que decidio
        vela, ant = cerradas[-k], cerradas[-k - 1]
        alto, bajo = _extremos(vela, criterio)
        alto_ant, bajo_ant = _extremos(ant, criterio)
        if alto > alto_ant and bajo < bajo_ant and vela.cierre == vela.abierta:
            saltadas_neutras += 1
    base = (
        f"{r.sesgo.value} por doble ruptura decidida por el color (ADR-0060 §1), "
        f"{r.ruptura_puntos} puntos"
        if r.doble_ruptura
        else f"{r.sesgo.value} por RN-003, ruptura simple de {r.ruptura_puntos} puntos"
    )
    if r.velas_miradas > 1:
        base += f", en la vela {r.velas_miradas}.a hacia atras"
        if saltadas_neutras:
            base += f" ({saltadas_neutras} neutra(s) con doble ruptura saltada(s), ADR-0075)"
    return base


def _ohlc(v: Vela, escala: int) -> str:
    def p(x: int) -> str:
        return str(Decimal(x) / escala)

    return (
        f"{a_datetime(v.inicio):%Y-%m-%dT%H:%MZ} o {p(int(v.abierta))} h {p(int(v.maxima))} "
        f"l {p(int(v.minima))} c {p(int(v.cierre))}"
    )


def main(repo: Path, salida: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    filas, sesgo_motor = leer(salida)
    p1 = sorted(
        {
            tuple(f.split(" | ")[1:3])
            for p, _, _, f in clasificar(filas, sesgo_motor)
            if p == "P1 sesgo"
        }
    )
    print(f"{salida.name}: {len(p1)} sesiones P1")
    criterio = cargar_criterio(repo)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    reloj = reloj_de_las_sesiones(registro)
    dias = arnes.dias_de_construccion(repo, criterio, list(criterio.construccion))
    # sin lectura de A-35: aqui solo se miran las H4, y la liquidez de M15 no se pide
    mercado = arnes.dias_de_mercado(repo, _carpeta_datos(repo), config, registro, dias, reloj)
    tope = registro.entero("sesgo_h4_tope_velas")
    crit = registro.opcion("sesgo_h4_criterio_ruptura")
    escala = 100_000
    sesiones = {s.nombre: s.desde for s in config.sesiones}
    orden = [s.nombre for s in config.sesiones]
    print(f"tope {tope}, criterio {crit}; sesiones {sesiones}")
    for dia, sesion in p1:
        dm = mercado[dia]
        d = date.fromisoformat(dia)
        apertura = reloj.instante(d, sesiones[sesion])
        h4 = dm.datos.velas_h4_cerradas(int(apertura))
        ultimas = h4[-2:]
        anotado = sesgo_motor.get((dia, sesion), "?")
        regla = _regla(h4, apertura, tope, crit)
        abre = f"{a_datetime(apertura):%H:%M}Z"
        print(f"{dia} {sesion} (abre {abre}): sesgo del motor {anotado}; {regla}")
        for v in ultimas:
            print(f"    H4 {_ohlc(v, escala)}")
        i = orden.index(sesion)
        if i > 0:
            previa = orden[i - 1]
            ap = reloj.instante(d, sesiones[previa])
            anotado_previa = sesgo_motor.get((dia, previa), "?")
            regla_previa = _regla(dm.datos.velas_h4_cerradas(int(ap)), ap, tope, crit)
            print(f"    sesion anterior {previa}: sesgo del motor {anotado_previa}; {regla_previa}")
        else:
            print("    sesion anterior del mismo dia: ninguna (es la primera)")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
