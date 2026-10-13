"""Fase 0.a de trabajo/entrada-enero: las tres medidas de la decision 1, por RECUENTO.

Imprime, sin ningun id de caso ni fecha reservada: cuantos casos de casos_reservados y de
casos_ocultos caen en 2026-01; si 2026-01 esta en meses_reservados.yaml; su entrada de vistos.yaml;
si el libro de enero esta en libros.yaml y con que huso; y el estado de la lista construccion.

  uv run python medidas_enero.py <raiz del repo>
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.holdout import casos_ocultos, casos_reservados  # noqa: E402
from botsito.comun.yaml_estricto import leer_yaml  # noqa: E402

MES = "2026-01"
SHA = "ee4ade46094c73c1f1de0043acc5345cf7fa42c729b71a4b57d781002554ab86"

reservados = casos_reservados(RAIZ)
ocultos = casos_ocultos(RAIZ)
print(f"casos_reservados: {len(reservados)} en total; en {MES}: "
      f"{sum(1 for c in reservados if MES in c)}")
print(f"casos_ocultos: {len(ocultos)} en total; en {MES}: {sum(1 for c in ocultos if MES in c)}")
print(f"casos_reservados por particion (todas, recuento): {dict(Counter(reservados.values()))}")

meses_res = leer_yaml(RAIZ / "knowledge" / "cases" / "meses_reservados.yaml")
texto = (RAIZ / "knowledge" / "cases" / "meses_reservados.yaml").read_text(encoding="utf-8")
print(f"meses_reservados.yaml: '{MES}' aparece {texto.count(MES)} veces")

vistos = leer_yaml(RAIZ / "knowledge" / "cases" / "kit" / "vistos.yaml")
for m in vistos["meses"]:
    if m["mes"] == MES:
        print(f"vistos.yaml: {MES} visto_el {m['visto_el']}, fuente {m['fuente']}")

criterio = cargar_criterio(RAIZ)
print(f"criterio_fidelidad construccion: {list(criterio.construccion)}")

dev = RAIZ / "knowledge" / "cases" / "dev"
print(f"knowledge/cases/dev: casos de {MES}: {len(list(dev.glob(f'caso-eurusd-{MES}-*.yaml')))}")
visto = RAIZ / "knowledge" / "cases" / "visto" / MES
print(f"knowledge/cases/visto/{MES}: {'existe' if visto.exists() else 'no existe'}")
