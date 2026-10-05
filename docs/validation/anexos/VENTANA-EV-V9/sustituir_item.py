"""Sustituye ev-v9-003456-9ef48fb5 por un item nuevo que lo supersede, con la ventana corregida, SIN
que el texto del item pase por la sesion (decision del consultor del 2026-10-05, punto 1).

Replica `botsito evidence new --supersede` (`evidence_new`; las lineas son las de `main` en
fffaa03: `src/botsito/cli.py:988-1040`): los mismos `campos` (cli.py:1014-1032), escritos con la
misma funcion,
`escribir_item(entorno.directorio, campos, entorno.comprobar)` (cli.py:1034), y la misma
comprobacion, `_EntornoEvidencia.comprobar` (cli.py:621-662): `tramo_no_citable`, el manifiesto, la
transcripcion activa y `verificar_citas`. Si la comprobacion encuentra algun problema,
`escribir_item` no escribe nada (`evidence/modelo.py:429-435`).

Los campos se copian del item viejo, salvo `t0` (el argumento), `supersede` (el id viejo) y
`notas` (el texto que fijo el consultor). Despues de escribir, comprueba que el item nuevo es igual
campo a campo al viejo salvo `id`, `t0`, `supersede` y `notas`; el modelo no genera campos de fecha
ni de autoria (`EvidenceItem`, `evidence/modelo.py:121-138`).

Solo imprime el id nuevo y el resultado de la comprobacion. Nunca la cita ni la afirmacion.

Uso (desde la raiz del repo):
    uv run python docs/validation/anexos/VENTANA-EV-V9/sustituir_item.py 0:34:56
        (tiene que fallar: la ventana vieja pisa el tramo de margen)
    uv run python docs/validation/anexos/VENTANA-EV-V9/sustituir_item.py 0:34:57
        (escribe el item nuevo)
"""

from __future__ import annotations

import sys
from dataclasses import asdict
from pathlib import Path

from botsito.cli import _EntornoEvidencia
from botsito.evidence.modelo import (
    EvidenciaError,
    calcular_id,
    cargar_item,
    escribir_item,
    limpiar_campos,
)

RAIZ = Path(__file__).resolve().parents[4]
VIEJO = "ev-v9-003456-9ef48fb5"
NOTAS = (
    "ventana corregida por orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó"
)
CAMBIAN = {"id", "t0", "supersede", "notas"}


def main(t0: str) -> int:
    entorno = _EntornoEvidencia(RAIZ)
    viejo = next(i for i in entorno.existentes if i.id == VIEJO)
    campos = {k: v for k, v in asdict(viejo).items() if k != "id"}
    campos["fotogramas"] = list(viejo.fotogramas)
    campos["t0"] = t0
    campos["supersede"] = VIEJO
    campos["notas"] = NOTAS
    print(f"item viejo: {VIEJO} ({viejo.t0_ms}-{viejo.t1_ms} ms); t0 nuevo: {t0}")
    try:
        ruta = escribir_item(entorno.directorio, campos, entorno.comprobar)
    except EvidenciaError as exc:
        # Los mensajes de la comprobacion son de plantilla: ids, tiempos y el motivo del tramo. El
        # id del candidato no se escribe nunca, y `knowledge validate` exige que exista todo id
        # citado en docs/: se nombra sin el.
        candidato = calcular_id(limpiar_campos(dict(campos)))
        mensaje = str(exc).replace(candidato, "<candidato sin escribir>")
        print(f"RECHAZADO por la comprobacion de evidence new: {mensaje}")
        return 1
    nuevo = cargar_item(ruta)
    a, b = asdict(viejo), asdict(nuevo)
    distintos = sorted(k for k in a if a[k] != b[k])
    print(
        f"ESCRITO: {nuevo.id} ({nuevo.t0_ms}-{nuevo.t1_ms} ms), {ruta.relative_to(RAIZ).as_posix()}"
    )
    print(f"campos distintos del viejo: {distintos}")
    print(f"igual campo a campo salvo {sorted(CAMBIAN)}: {set(distintos) <= CAMBIAN}")
    return 0 if set(distintos) <= CAMBIAN else 2


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
