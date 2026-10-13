"""Fase 0.e de trabajo/entrada-enero: la ventana de ticks por la rejilla frente a huso_operativa.

Para cada dia laborable de enero de 2026, de julio de 2026 (1-17) y de dos tramos de desfase
(marzo y octubre-noviembre de 2026), la apertura de la ventana y su fin en UTC por
`reloj_de_las_sesiones` (ADR-0069 §5), las horas UTC que cubre, y la hora UTC en que huso_operativa
pone `ventana_inicio`. Solo lee el registro; no toca datos.

  uv run python ventana_rejilla.py <raiz del repo>
"""

from __future__ import annotations

import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.relojes import reloj_de_las_sesiones  # noqa: E402
from botsito.comun.husos import huso_canonico  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402

registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
reloj = reloj_de_las_sesiones(registro)
huso = huso_canonico(registro.texto("huso_operativa"))
ini = registro.hora("ventana_inicio").minutos_del_dia
fin = registro.hora("ventana_fin").minutos_del_dia
epoca = datetime(1970, 1, 1, tzinfo=UTC)
print(f"reloj {reloj.opcion}; ancla {reloj.anclaje}; vela {reloj.primera_vela}; "
      f"ventana nominal {ini // 60:02d}-{fin // 60:02d}; huso_operativa {huso}")


def utc(minuto: int) -> datetime:
    return epoca + timedelta(minutes=minuto)


def tramo(nombre: str, desde: date, hasta: date) -> None:
    print(f"\n== {nombre}")
    horas_union: set[int] = set()
    d = desde
    while d <= hasta:
        if d.weekday() < 5:
            a = int(reloj.instante(d, f"{ini // 60:02d}:{ini % 60:02d}"))
            b = int(reloj.instante(d, f"{fin // 60:02d}:{fin % 60:02d}"))
            horas = sorted({utc(m).hour for m in range(a, b)})
            horas_union |= set(horas)
            pared = datetime(d.year, d.month, d.day, ini // 60, ini % 60, tzinfo=huso)
            pared_utc = pared.astimezone(UTC)
            desfase = utc(a) != pared_utc
            print(f"{d} rejilla {utc(a):%H:%M}-{utc(b):%H:%M}Z horas {horas[0]:02d}-{horas[-1]:02d}"
                  f" | huso_operativa {pared_utc:%H:%M}Z{'  DESFASE' if desfase else ''}")
        d += timedelta(days=1)
    print(f"union de horas UTC: {sorted(horas_union)}")


tramo("enero 2026", date(2026, 1, 1), date(2026, 1, 31))
tramo("julio 2026 (1-17)", date(2026, 7, 1), date(2026, 7, 17))
tramo("marzo 2026 (desfase de primavera)", date(2026, 3, 6), date(2026, 3, 31))
tramo("octubre-noviembre 2026 (desfase de otono)", date(2026, 10, 22), date(2026, 11, 4))
