"""Fase 0.c de trabajo/entrada-enero: el spread supuesto de llenado.yaml en un dia de desfase.

`engine/simulador_config.py` busca el spread por la hora de PARED en `spread.huso` (Europe/Madrid);
la ventana del trader la cuenta la rejilla (ADR-0069). Para un dia sin desfase (2026-10-22) y uno
con desfase (2026-10-27), por cada hora UTC de 04 a 14: la hora de pared, la hora NOMINAL de la
rejilla, y el spread que da la tabla por cada una. Solo lee el registro y llenado.yaml.

  uv run python spread_desfase.py <raiz del repo>
"""

from __future__ import annotations

import sys
from datetime import UTC, date, datetime
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.relojes import reloj_de_las_sesiones  # noqa: E402
from botsito.comun.husos import huso_canonico  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.velas import a_minuto  # noqa: E402
from botsito.engine.simulador_config import cargar_config_llenado  # noqa: E402

registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
reloj = reloj_de_las_sesiones(registro)
cfg = cargar_config_llenado(RAIZ / "knowledge" / "simulador" / "llenado.yaml")
tabla = dict(cfg.spread_por_hora_local)
fuera = cfg.spread_fuera_de_ventana
zona = huso_canonico(cfg.spread_huso)
print(f"llenado.yaml: huso {cfg.spread_huso}; tabla {tabla}; fuera {fuera}")
for dia in (date(2026, 10, 22), date(2026, 10, 27)):
    print(f"\n== {dia}")
    distintas = 0
    for h in range(4, 15):
        t = datetime(dia.year, dia.month, dia.day, h, 30, tzinfo=UTC)
        pared = t.astimezone(zona).hour
        _, minuto = reloj.lectura(int(a_minuto(t)))
        nominal = minuto // 60
        a, b = tabla.get(pared, fuera), tabla.get(nominal, fuera)
        distintas += a != b
        print(f"{h:02d}:30Z pared {pared:02d} -> {a} | rejilla {nominal:02d} -> {b}"
              f"{'  DISTINTO' if a != b else ''}")
    print(f"horas con spread distinto: {distintas}")
