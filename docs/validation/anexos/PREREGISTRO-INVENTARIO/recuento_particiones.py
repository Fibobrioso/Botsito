"""Recuento de dias por particion reservada, SIN imprimir ninguna clave (llevan la fecha).

trabajo/preregistro, fase 0, punto 0.3. Solo lee la ASIGNACION, por las funciones del repo:
`casos_reservados`, `casos_retirados`, `casos_medidos` (botsito.cases.holdout), y
`cargar_retirados` para la fecha de cada retirada (`retirado_el`, que es la fecha en que se
retiro, no la del dia). Para partir por reparto, `repartos_commiteables` y los VALORES de su
`asignacion`, que es lo mismo que lee `casos_reservados`.

Imprime solo nombres de particion, rutas de reparto (ids de sesion o de artefacto) y numeros.
Uso: uv run python <este guion> <raiz del repo>
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from botsito.cases.holdout import (
    RESERVADAS,
    cargar_retirados,
    casos_medidos,
    casos_reservados,
    casos_retirados,
    huella_de_caso,
    repartos_commiteables,
)
from botsito.comun.yaml_estricto import leer_yaml

CORTE = "2026-10-17"


def main(repo: Path) -> None:
    reservados = casos_reservados(repo)
    retirados = casos_retirados(repo)
    medidos = casos_medidos(repo)
    entradas = cargar_retirados(repo)

    tot = Counter(reservados.values())
    ret = Counter(retirados.values())
    med = Counter(medidos.values())
    ret_antes = Counter(
        p for c, p in retirados.items() if str(entradas[huella_de_caso(c)]["retirado_el"]) < CORTE
    )
    print("particion | dias | retirados | retirados antes de", CORTE, "| medibles")
    for p in RESERVADAS:
        print(f"{p} | {tot[p]} | {ret[p]} | {ret_antes[p]} | {med[p]}")
    print(f"TOTAL | {sum(tot.values())} | {sum(ret.values())} | {sum(ret_antes.values())} | "
          f"{sum(med.values())}")
    print("fechas de retirada (retirado_el, no son dias de mercado):",
          sorted(Counter(str(e["retirado_el"]) for e in entradas.values()).items()))

    print("\npor reparto (valores de su asignacion):")
    for fichero in repartos_commiteables(repo):
        asignacion = (leer_yaml(fichero) or {}).get("asignacion") or {}
        cuenta = Counter(str(v) for v in asignacion.values())
        print(f"{fichero.relative_to(repo).as_posix()} | {dict(sorted(cuenta.items()))}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
