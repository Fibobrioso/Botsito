"""Fase 0 de trabajo/laminas (0.2): QUE CAMPOS da cada pieza, medido sobre una ejecucion real del
motor cableado (julio de 2026, construccion, por la compuerta del arnes; la misma preparacion que
`motor decisiones`). Imprime NOMBRES de campos, tipos y recuentos, y para 2026-07-03 la forma de la
memoria en los cierres en que cambia algo. Ni R, ni dinero, ni porcentajes, ni lotes.
Uso, desde la raiz del repo: uv run python <este fichero>"""
from __future__ import annotations

import dataclasses
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from botsito.cases.criterio_fidelidad import cargar_criterio, medir
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.engine import arnes, cableado, decisiones, diagnostico, entrada, tope_trader, zonas
from botsito.engine.interprete import reglas_ejecutables
from botsito.engine.relojes import reloj_de_las_sesiones
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

sys.stdout.reconfigure(encoding="utf-8")
repo = Path(".")
spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
reglas = reglas_ejecutables(cargar_reglas(spec))
criterio = cargar_criterio(repo)
meses = ["2026-07"]
registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
vocabulario = cargar_vocabulario(spec)
dias = arnes.dias_de_construccion(repo, criterio, meses)
diag = diagnostico.Diagnostico()
lectura = diagnostico.lectura_pivote(registro, diag)
perfil = cableado.perfil_del_repo(repo, None)
tope = tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag)
limpia = zonas.lectura_limpia(registro)
tipo = entrada.lectura_tipo_orden(registro, None)
datos = carpeta_datos(repo)
mercado = arnes.dias_de_mercado(
    repo, datos, config, registro, dias, reloj_de_las_sesiones(registro), lectura
)
plantilla = cableado.construir_motor_cableado(
    repo, datos, criterio, config, registro, vocabulario, reglas, dias, perfil, None, False,
    tope, limpia, stops_level_diagnostico=None, tipo_orden=tipo,
)
DIA = "2026-07-03"
claves_mem: Counter[str] = Counter()
claves_ses: Counter[str] = Counter()
claves_esc: Counter[str] = Counter()
claves_toma: Counter[str] = Counter()
anot: Counter[str] = Counter()
hechos: Counter[str] = Counter()
broker_h: Counter[str] = Counter()
tipos: dict[str, str] = {}
campos_orden: set[str] = set()
campos_pos: set[str] = set()
campos_ctx: set[str] = set()
ejemplo_punto: list[str] = []
sesiones_vistas: set[str] = set()
cierres = 0


def _nombre(x: Any) -> str:
    return type(x).__name__


def obs(c: Any) -> None:
    global cierres
    cierres += 1
    if not tipos:
        for f in dataclasses.fields(c):
            tipos[f.name] = _nombre(getattr(c, f.name))
        campos_ctx.update(f.name for f in dataclasses.fields(c.ctx))
    if c.dia != DIA:
        return
    sesiones_vistas.add(str(c.sesion))
    mem = c.estado.memoria.get("zona_de_entrada", {})
    claves_mem.update(mem.keys())
    for nombre, m in (mem.get("por_sesion") or {}).items():
        claves_ses.update(f"{k}:{_nombre(v)}" for k, v in m.items())
        for e in m.get("escenarios") or []:
            claves_esc.update(f"{k}:{_nombre(v)}" for k, v in e.items())
            claves_toma.update(f"{k}:{_nombre(v)}" for k, v in e["toma"].items())
        if m.get("punto_de_zona") and not ejemplo_punto:
            ejemplo_punto.append(_nombre(next(iter(m["punto_de_zona"].values()))))
    for z in (mem.get("zonas") or {}).values():
        tipos.setdefault("Zona", ",".join(f.name for f in dataclasses.fields(z)))
    for s in c.estado.anotaciones.values():
        anot.update(s.keys())
    hechos.update(f"{k}={v}" for k, v in c.estado.hechos.items())
    broker_h.update(c.estado.broker.keys())
    for o in c.broker.ordenes.values():
        campos_orden.update(f.name for f in dataclasses.fields(o))
    for p in c.broker.posiciones.values():
        campos_pos.update(f.name for f in dataclasses.fields(p))


motor = decisiones.motor_nuevo(plantilla, reglas, obs)
corrida = arnes.correr(cableado.NOMBRE_MOTOR, tuple(meses), dias, mercado, motor)
bot = [op for r in corrida.resultados for op in r.operaciones]
trader = [op for d in dias for op in d.operaciones]
m = medir(trader, bot, criterio.tolerancias)
print("cierres observados:", cierres, "| dias:", len(dias))
print("Cierre, campos y tipos:", tipos)
print("ContextoDia, campos:", sorted(campos_ctx))
print(f"{DIA}: sesiones vistas:", sorted(sesiones_vistas))
print("memoria zona_de_entrada, claves:", dict(claves_mem))
print("por_sesion, claves:tipo:", dict(claves_ses))
print("escenario, claves:tipo:", dict(claves_esc))
print("toma, claves:tipo:", dict(claves_toma))
print("punto_de_zona, tipo del valor:", ejemplo_punto)
print("anotaciones por sesion, claves:", dict(anot))
print("hechos=valor vistos (cierres):", dict(hechos))
print("hechos del broker, claves:", dict(broker_h))
print("Orden, campos:", sorted(campos_orden))
print("Posicion, campos:", sorted(campos_pos))
print("bot Operacion, campos:", [f.name for f in dataclasses.fields(bot[0])] if bot else "-")
print("parejas de julio (recuento):", len(m.parejas), "| trader:", len(trader), "| bot:", len(bot))
print("ResultadoDia, campos:", [f.name for f in dataclasses.fields(corrida.resultados[0])])
