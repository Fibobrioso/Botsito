"""F1, punto 6, de trabajo/activar-sesion-07: la estabilidad del arranque de la regla del rango
vigente (ADR-0094, e). Solo recuentos por mes, y una a una las sesiones que nombra el encargo.

Uso: uv run python docs/validation/anexos/ACTIVAR-SESION-07/arranque.py <tope corto> <tope largo>

Carga las velas como el arnes (`arnes.dias_de_mercado`: el mes y el anterior si hay dataset; enero
solo el suyo), por la compuerta de construccion (`arnes.dias_de_construccion`), y para cada sesion
de cada dia `dev` calcula `domain.sesgo.sesgo_h4` con los dos topes y el criterio del registro.
Imprime, por mes: sesiones, cuantas cambian de lado entre los dos topes, cuantas tienen cargadas
menos H4 cerradas que cada tope, y cuantas quedan INSUFICIENTE con cada tope. Y una linea por cada
sesion nombrada (las siete declaradas de F1 y las siete del bloque de la 7b), con lo mismo. No
imprime precios, ni operaciones, ni nada de un dia que no sea de construccion.
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.domain.sesgo import Sesgo, sesgo_h4
from botsito.engine import arnes
from botsito.engine.relojes import reloj_de_las_sesiones

REPO = Path(__file__).resolve().parents[4]
NOMBRADAS = (
    # las siete del rango de H4 declaradas en F1 (VIDEO-JULIO.md §4.1 y §4.2)
    ("2026-07-01", "07-11"),
    ("2026-07-06", "07-11"),
    ("2026-07-06", "11-15"),
    ("2026-07-07", "07-11"),
    ("2026-07-07", "11-15"),
    ("2026-07-15", "11-15"),
    ("2026-07-17", "11-15"),
    # las siete del bloque de la 7b (docs/sesion-7/PREGUNTAS-7B.md §1)
    ("2026-01-13", "07-11"),
    ("2026-04-15", "11-15"),
    ("2026-01-07", "07-11"),
    ("2026-01-19", "11-15"),
    ("2026-01-21", "07-11"),
    ("2026-01-22", "11-15"),
    ("2026-07-16", "07-11"),
)


def main(corto: int, largo: int) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    criterio = cargar_criterio(REPO)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(REPO / "knowledge" / "cases" / "kit" / "config.yaml")
    reloj = reloj_de_las_sesiones(registro)
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    rango_nuevo = registro.opcion("sesgo_h4_rango_nuevo")
    meses = list(criterio.construccion)
    dias = arnes.dias_de_construccion(REPO, criterio, meses)
    nombradas = set(NOMBRADAS)
    dias_nombrados = {d for d, _ in NOMBRADAS}
    vistos = {d.dia for d in dias}
    faltan = sorted(dias_nombrados - vistos)
    if faltan:
        print(f"ERROR: {len(faltan)} dias nombrados no son dias dev de construccion")
        return 1
    mercado = arnes.dias_de_mercado(REPO, carpeta_datos(REPO), config, registro, dias, reloj)
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    lineas: dict[tuple[str, str], str] = {}
    for d in dias:
        dm = mercado[d.dia]
        for s in config.sesiones:
            apertura = reloj.instante(date.fromisoformat(d.dia), s.desde)
            cerradas = dm.datos.velas_h4_cerradas(int(apertura))
            r_c = sesgo_h4(cerradas, apertura, corto, criterio_ruptura, rango_nuevo)
            r_l = sesgo_h4(cerradas, apertura, largo, criterio_ruptura, rango_nuevo)
            c = por_mes[d.dia[:7]]
            c["sesiones"] += 1
            c["cambian de lado"] += r_c.sesgo is not r_l.sesgo
            c[f"menos de {corto} H4 cargadas"] += len(cerradas) < corto
            c[f"menos de {largo} H4 cargadas"] += len(cerradas) < largo
            c[f"INSUFICIENTE con {corto}"] += r_c.sesgo is Sesgo.INSUFICIENTE
            c[f"INSUFICIENTE con {largo}"] += r_l.sesgo is Sesgo.INSUFICIENTE
            if (d.dia, s.nombre) in nombradas:
                lineas[(d.dia, s.nombre)] = (
                    f"{d.dia} {s.nombre}: {len(cerradas)} H4 cerradas cargadas; con {corto}: "
                    f"{r_c.sesgo.value}; con {largo}: {r_l.sesgo.value}"
                    f"{'   <- depende del arranque' if r_c.sesgo is not r_l.sesgo else ''}"
                )
    claves = (
        "sesiones",
        "cambian de lado",
        f"menos de {corto} H4 cargadas",
        f"menos de {largo} H4 cargadas",
        f"INSUFICIENTE con {corto}",
        f"INSUFICIENTE con {largo}",
    )
    print(f"arranque de la regla del rango: tope {corto} frente a {largo}; criterio {criterio_ruptura}")
    print("mes | " + " | ".join(claves))
    total: Counter[str] = Counter()
    for mes in sorted(por_mes):
        total.update(por_mes[mes])
        print(f"{mes} | " + " | ".join(str(por_mes[mes][k]) for k in claves))
    print("total | " + " | ".join(str(total[k]) for k in claves))
    print("-- sesiones nombradas (orden del encargo)")
    for clave in NOMBRADAS:
        print(lineas.get(clave, f"{clave[0]} {clave[1]}: no es una sesion de la configuracion"))
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]), int(sys.argv[2])))
