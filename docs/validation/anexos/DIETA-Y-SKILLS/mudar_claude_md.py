"""Muda TAL CUAL a docs/runbooks/ los bloques de CLAUDE.md que solo se usan en algunas tareas.

Rama `trabajo/dieta-y-skills` (2026-10-01), punto 2 del encargo. Lee `git show df6aa2c:CLAUDE.md`
(el de antes de la revision) y escribe en `--salida` (fuera del repositorio) los dos runbooks
nuevos; cada bloque se copia con sus lineas exactas y el guion comprueba que esta en el original.

Uso: uv run python docs/validation/anexos/DIETA-Y-SKILLS/mudar_claude_md.py --salida <carpeta>
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]

# (primera, ultima) linea de cada bloque, 1-based e inclusivas, en CLAUDE.md de df6aa2c; el
# texto de la primera linea lo confirma, para que un numero mal puesto no mude otra cosa.
MIRAR = [
    ((96, 103), "Estan infrautilizados, y eso cuesta turnos del trader"),
    ((142, 161), "> **Por que cambio esta regla, TERCERA vez (2026-09-21).**"),
    ((163, 187), "**COMO SE ABRE UN FOTOGRAMA: POR INSTANTE LOCALIZADO, NUNCA POR MUESTREO**"),
    ((230, 243), "## Donde esta el texto de las transcripciones"),
]
AMBIGUEDADES = [
    ((191, 210), "## Abrir una ambiguedad toca dos sitios; cerrarla, cuatro"),
]

CABECERA_MIRAR = """\
# Mirar el material: fotogramas, transcripciones y el reloj de FX Replay

Lo que hace falta SOLO cuando una tarea abre fotogramas, lee transcripciones o compara el video con
las velas. Mudado TAL CUAL desde `CLAUDE.md` («Que se puede mirar y que no» y «Donde esta el texto
de las transcripciones») el 2026-10-01, en `trabajo/dieta-y-skills`; alli queda la regla corta
y el puntero a este fichero. Las fechas y los «hoy» son los de cuando se escribio cada parrafo.
Lo que se puede mirar y lo que no lo sigue diciendo `CLAUDE.md`: esto es el COMO.

"""

CABECERA_AMBIGUEDADES = """\
# Abrir, editar y cerrar una ambiguedad

Lo que hace falta SOLO cuando una tarea toca `knowledge/spec/ambiguedades.yaml`. Mudado TAL CUAL
desde `CLAUDE.md` el 2026-10-01, en `trabajo/dieta-y-skills`; alli queda una linea que apunta aqui.

> **CORRECCION (2026-10-01, `trabajo/dieta-y-skills`).** Desde hoy la tabla «Known Ambiguities» de
> `PROJECT_STATE.md` lleva solo las ABIERTAS, con su titulo, clase, bloqueante y «resuelve en», y
> `tests/unit/test_kit.py` (`test_project_state_refleja_las_ambiguedades_abiertas`) exige que sean
> exactamente las `ABIERTA` del YAML. ABRIR una sigue tocando la tabla (se anade su fila); CERRARLA
> la toca QUITANDO la fila, no cambiando su texto. Lo que dicen los dos apartados de abajo sobre «la
> tabla» se lee asi. Las filas de las cerradas hasta hoy estan en docs/state/HISTORIA.md.

"""


def bloques(lineas: list[str], tramos: list[tuple[tuple[int, int], str]]) -> str:
    trozos = []
    for (a, b), primera in tramos:
        assert lineas[a - 1].startswith(primera), (a, lineas[a - 1][:60])
        trozos.append("\n".join(lineas[a - 1 : b]))
    return "\n\n".join(trozos) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True, type=Path)
    salida: Path = ap.parse_args().salida.resolve()
    if salida == RAIZ or RAIZ in salida.parents:
        print("ERROR: --salida tiene que estar FUERA del repositorio", file=sys.stderr)
        return 2
    salida.mkdir(parents=True, exist_ok=True)
    original = subprocess.run(
        ["git", "show", "df6aa2c:CLAUDE.md"], cwd=RAIZ, capture_output=True, check=True
    ).stdout.decode("utf-8")
    lineas = original.split("\n")
    mirar = CABECERA_MIRAR + bloques(lineas, MIRAR)
    ambs = CABECERA_AMBIGUEDADES + bloques(lineas, AMBIGUEDADES)
    (salida / "MIRAR-EL-MATERIAL.md").write_text(mirar, encoding="utf-8", newline="\n")
    (salida / "AMBIGUEDADES.md").write_text(ambs, encoding="utf-8", newline="\n")
    print(f"MIRAR-EL-MATERIAL.md: {len(mirar.encode())} bytes; AMBIGUEDADES.md: {len(ambs.encode())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
