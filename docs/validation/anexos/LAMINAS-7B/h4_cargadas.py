"""0.2 de trabajo/laminas-sesion-7b: las H4 cerradas cargadas al abrir cada sesion del bloque de la
7b (las cuatro y las tres reservas de F1). Parte de `anexos/ACTIVAR-SESION-07/arranque.py`.

Uso (desde la raiz del repo):
    uv run python docs/validation/anexos/LAMINAS-7B/h4_cargadas.py

Carga las velas como el arnes (`arnes.dias_de_mercado`: el mes y el anterior si hay dataset; enero
solo el suyo), por la compuerta de construccion (`arnes.dias_de_construccion`), SOLO para los dias
del bloque (lo que se carga para un dia depende solo de su mes, `arnes.dias_de_mercado`), y para
cada sesion del bloque cuenta las H4 cerradas antes de su apertura. Imprime solo ese recuento y si
llega al minimo de 60 (F1 del encargo). Ningun sesgo, precio ni operacion.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.engine import arnes
from botsito.engine.relojes import reloj_de_las_sesiones

REPO = Path(__file__).resolve().parents[4]
MINIMO = 60  # F1 del encargo: sale toda sesion que abra con menos de 60 H4 cargadas
BLOQUE = (
    # las cuatro (F1, puntos 2 y 3)
    ("2026-04-24", "07-11"),
    ("2026-04-15", "11-15"),
    ("2026-04-27", "11-15"),
    ("2026-01-19", "11-15"),
    # las tres reservas (F1, punto 2)
    ("2026-01-21", "07-11"),
    ("2026-01-22", "11-15"),
    ("2026-07-16", "07-11"),
)


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    criterio = cargar_criterio(REPO)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(REPO / "knowledge" / "cases" / "kit" / "config.yaml")
    reloj = reloj_de_las_sesiones(registro)
    meses = sorted({d[:7] for d, _ in BLOQUE})
    pedidos = {d for d, _ in BLOQUE}
    dias = [d for d in arnes.dias_de_construccion(REPO, criterio, meses) if d.dia in pedidos]
    faltan = sorted(pedidos - {d.dia for d in dias})
    if faltan:
        print(f"ERROR: {len(faltan)} dias del bloque no son dias dev de construccion")
        return 1
    mercado = arnes.dias_de_mercado(REPO, carpeta_datos(REPO), config, registro, dias, reloj)
    sesiones = {s.nombre: s for s in config.sesiones}
    print(f"H4 cerradas cargadas al abrir cada sesion del bloque (minimo {MINIMO})")
    for dia, nombre in BLOQUE:
        s = sesiones.get(nombre)
        if s is None:
            print(f"{dia} {nombre}: no es una sesion de la configuracion")
            continue
        apertura = reloj.instante(date.fromisoformat(dia), s.desde)
        n = len(mercado[dia].datos.velas_h4_cerradas(int(apertura)))
        print(f"{dia} {nombre}: {n} H4 cerradas cargadas -> {'CUMPLE' if n >= MINIMO else 'NO CUMPLE'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
