"""Fase 0 de trabajo/laminas (0.3): las listas cerradas de donde sale la tabla de frases, leidas de
la spec y del codigo. Solo nombres y titulos."""
import sys
from pathlib import Path

from botsito.engine import broker, zonas
from botsito.engine.arnes import hechos_de_regla
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

sys.stdout.reconfigure(encoding="utf-8")
spec = Path("knowledge/spec/strategy_spec.yaml")
voc = cargar_vocabulario(spec)
print("== hechos (origen, valores, productoras)")
for nombre, h in voc["hechos"].items():
    print(nombre, "|", h.get("origen"), "|", h.get("valores"), "|", h.get("produce"))
print("== hechos de regla en orden (el camino):", [h for h, _ in hechos_de_regla(voc)])
print("== VIGENTE que prohiben")
for r in cargar_reglas(spec):
    if getattr(r, "estado", None) != "VIGENTE":
        continue
    forma = getattr(r, "forma", None) or {}
    ent = (forma.get("entonces") or {}) if isinstance(forma, dict) else {}
    pro = ent.get("prohibe") if isinstance(ent, dict) else None
    if pro:
        print(r.id, "|", getattr(r, "clase", None), "|", pro, "|", r.titulo)
print("== VIGENTE que no prohiben (id, clase)")
for r in cargar_reglas(spec):
    if getattr(r, "estado", None) != "VIGENTE":
        continue
    forma = getattr(r, "forma", None) or {}
    ent = (forma.get("entonces") or {}) if isinstance(forma, dict) else {}
    if not (isinstance(ent, dict) and ent.get("prohibe")):
        print(r.id, "|", getattr(r, "clase", None), "|", r.titulo)
print("== limites del lote:", broker.LIMITE_VOLUMEN, broker.LIMITE_MARGEN, broker.LIMITE_MINIMO)
print("== terminado:", zonas.TERMINADO_POR_GANANCIA)
