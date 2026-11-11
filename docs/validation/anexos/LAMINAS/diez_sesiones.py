"""Fase 0 de trabajo/laminas (0.1): las diez sesiones y los dias que tocan sus ventanas frente a
casos_reservados, casos_ocultos y la construccion. SOLO recuentos y si/no; ningun id de caso."""
from datetime import date, timedelta
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.holdout import casos_ocultos, casos_reservados
from botsito.corpus.cuarentena import dias_de_casos
from botsito.engine.arnes import dias_de_construccion

repo = Path(".")
SESIONES = (
    ("2026-07-06", "07-11"), ("2026-07-06", "11-15"), ("2026-07-07", "07-11"),
    ("2026-07-07", "11-15"), ("2026-07-15", "11-15"), ("2026-07-17", "11-15"),
    ("2026-04-13", "07-11"), ("2026-07-02", "11-15"), ("2026-07-03", "11-15"),
    ("2026-07-03", "07-11"),
)
res = casos_reservados(repo)
ocu = casos_ocultos(repo)
print("casos_reservados:", len(res), "claves; casos_ocultos:", len(ocu), "claves")
dias_ocultos = dias_de_casos(ocu)
dias_reservados = dias_de_casos(res)
print("dias (mes, dia) ocultos:", len(dias_ocultos), "; reservados:", len(dias_reservados))
criterio = cargar_criterio(repo)
print("meses de construccion:", list(criterio.construccion))
dev = {d.dia for d in dias_de_construccion(repo, criterio, list(criterio.construccion))}
print("dias dev de construccion:", len(dev))
for dia, sesion in SESIONES:
    d = date.fromisoformat(dia)
    ventana = [d - timedelta(days=k) for k in range(5, -1, -1)]  # 4 dias antes y el UTC anterior
    print(
        dia, sesion,
        "| dev:", dia in dev,
        "| oculto:", (d.month, d.day) in dias_ocultos,
        "| reservado:", (d.month, d.day) in dias_reservados,
        "| dias de la ventana ocultos:", sum((x.month, x.day) in dias_ocultos for x in ventana),
        "| reservados:", sum((x.month, x.day) in dias_reservados for x in ventana),
    )
