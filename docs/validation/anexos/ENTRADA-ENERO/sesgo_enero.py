"""Fase 0.f de trabajo/entrada-enero: el sesgo H4 de enero de 2026 sin diciembre de 2025.

Como `engine/arnes.py:dias_de_mercado`: las M1 del mes anterior si hay dataset (no lo hay: se dice)
y las del mes, agregadas a H4 con `anclaje_h4`; la apertura de cada sesion del kit por la puerta
`reloj_de_las_sesiones` (ADR-0069 §5), y `domain.sesgo.sesgo_h4` con el tope y el criterio del
registro. Por cada laborable del 2 al 30 de enero y cada sesion: el sesgo, las velas miradas y
cuantas H4 cerradas hay antes de la apertura. Solo VELAS (ADR-0021 §1): ningun caso, ningun libro.

  uv run python sesgo_enero.py <raiz del repo>
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.cases.relojes import MINUTOS_H4, reloj_de_las_sesiones  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.agregacion import agregar  # noqa: E402
from botsito.data.dataset import (  # noqa: E402
    DatasetError,
    buscar_manifiesto,
    cargar_manifiesto,
    cargar_serie,
)
from botsito.data.velas import a_datetime  # noqa: E402
from botsito.domain.sesgo import Sesgo, sesgo_h4  # noqa: E402

registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
anclaje = registro.hora("anclaje_h4")
tope = registro.entero("sesgo_h4_tope_velas")
criterio = registro.opcion("sesgo_h4_criterio_ruptura")
reloj = reloj_de_las_sesiones(registro)
config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
datos = carpeta_datos(RAIZ)

m1 = []
for m in ("2025-12", "2026-01"):
    try:
        ruta = buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{m}")
    except DatasetError:
        print(f"{m}: sin dataset M1 (el calentamiento empieza en el mes)")
        continue
    serie = cargar_serie(cargar_manifiesto(ruta), datos)
    m1 += list(serie.velas)
    print(f"{m}: {ruta.stem}, {len(serie.velas)} velas M1, primera "
          f"{a_datetime(serie.velas[0].inicio):%Y-%m-%dT%H:%MZ}")
h4 = agregar(m1, MINUTOS_H4, anclaje)
print(f"H4: {len(h4)} velas; primera {a_datetime(h4[0].inicio):%Y-%m-%dT%H:%MZ}")
sesiones = [(s.nombre, s.desde) for s in config.sesiones]
print(f"tope {tope}, criterio {criterio}, sesiones {sesiones}")

cuenta: Counter[str] = Counter()
d = date(2026, 1, 2)
while d <= date(2026, 1, 30):
    if d.weekday() < 5:
        partes = []
        for s in config.sesiones:
            apertura = reloj.instante(d, s.desde)
            cerradas = sum(1 for v in h4 if v.fin <= apertura)
            r = sesgo_h4(h4, apertura, tope, criterio)
            cuenta[r.sesgo.value] += 1
            partes.append(f"{s.nombre} {a_datetime(apertura):%H:%M}Z: {r.sesgo.value} "
                          f"(miradas {r.velas_miradas}, H4 cerradas antes {cerradas})")
        marca = " <- INSUFICIENTE" if any("insuficiente" in p for p in partes) else ""
        print(f"{d}: " + "; ".join(partes) + marca)
    d += timedelta(days=1)
print(f"recuento por sesgo (laborables x sesiones): {dict(cuenta)}")
print(f"INSUFICIENTE: {cuenta[Sesgo.INSUFICIENTE.value]}")
