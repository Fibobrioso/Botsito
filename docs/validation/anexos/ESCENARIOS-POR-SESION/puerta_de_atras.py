"""¿La toma de la manana vale en la tarde por la puerta de atras? Dia SINTETICO de 2030.

Anexo de `docs/validation/ESCENARIOS-POR-SESION.md` §0.2. La secuencia de `test_preparar_a35`
(la toma de un BAJO con cuerpo; sesgo alcista) se desplaza para que la toma caiga en el ultimo cuarto
de hora de la sesion 07-11 (09:45Z-10:00Z: es invierno), y despues el precio sigue bajando con
bloques ROJOS -sin vela contraria que forme otro BAJO- hasta pasadas las 11:00 (10:00Z). Imprime en
que minutos fija RN-004 `liquidez_tomada` en cada sesion, contados desde la apertura de la tarde, y
el pivote que es la liquidez a esa hora. Sin datos reales: no lee nada de `data/`.

    uv run python docs/validation/anexos/ESCENARIOS-POR-SESION/puerta_de_atras.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ))

from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.agregacion import agregar  # noqa: E402
from botsito.domain.pivotes_m15 import BAJO, CIERRE_VELA_CONTRARIA  # noqa: E402
from botsito.engine.interprete import reglas_ejecutables  # noqa: E402
from botsito.engine.motor import DatosMercado  # noqa: E402
from botsito.spec.modelo import cargar_reglas  # noqa: E402
from tests.unit import test_preparar_a35 as ta  # noqa: E402

VERDES_ANTES = 9  # bloques verdes de subida antes del dibujo: no dejan ningun BAJO
ROJOS_DESPUES = 6  # bloques rojos despues de la toma: tampoco
PASO = 20


def m1_del_dia() -> list:  # type: ignore[type-arg]
    bloques: list[tuple[int, int, int | None]] = []
    precio = ta.BASE + 200
    for _ in range(VERDES_ANTES):
        bloques.append((precio, precio + PASO, None))
        precio += PASO
    bloques.append((precio, ta.BLOQUES[0][0], None))  # el puente hasta el arranque del dibujo
    bloques += ta.BLOQUES  # B5, la toma, es el bloque 15: 09:45Z-10:00Z
    ultimo = bloques[-1][1]
    for _ in range(ROJOS_DESPUES):
        bloques.append((ultimo, ultimo - PASO, None))
        ultimo -= PASO
    velas = []
    n, precio = 0, bloques[0][0]
    while ta.INICIO + ta.M15 * n < ta.FIN:
        a, c, lo = bloques[n] if n < len(bloques) else (precio, precio + 5, None)
        velas += ta._bloque(n, a, c, lo)
        precio = c
        n += 1
    return velas


def main() -> int:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    reglas = list(reglas_ejecutables(cargar_reglas(ta.SPEC)))
    m1 = m1_del_dia()
    agregadas = agregar(m1, ta.M15, registro.hora("anclaje_h4"))
    datos = DatosMercado(ta._h4_alcista(), agregadas, m1, CIERRE_VELA_CONTRARIA)
    r = ta._motor(registro, reglas).correr_dia(ta._dia(datos))
    tarde = ta.INICIO + 240
    for nombre, traza in r.sesiones.items():
        tomas = [t - tarde for t, _, h, _ in traza.fijados if h == "liquidez_tomada"]
        print(f"{nombre}: RN-004 fija liquidez_tomada en los minutos {tomas[:3]}... ({len(tomas)})")
    manana, apertura = datos.liquidez_m15(tarde - 10, BAJO), datos.liquidez_m15(tarde, BAJO)
    print(f"la liquidez a las 09:50Z y a las 10:00Z es el mismo pivote: {manana == apertura}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
