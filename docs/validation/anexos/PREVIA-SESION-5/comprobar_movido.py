"""Cada linea que sale de PROJECT_STATE.md (main frente a la rama) esta literal en un runbook y en HISTORIA.

Uso: python comprobar_movido.py <raiz>. Solo lee: git show main:PROJECT_STATE.md y los ficheros.
"""
import subprocess
import sys
from pathlib import Path

raiz = Path(sys.argv[1])
antes = subprocess.run(
    ["git", "show", "main:PROJECT_STATE.md"], cwd=raiz, capture_output=True, check=True
).stdout.decode("utf-8").splitlines()
ahora = set((raiz / "PROJECT_STATE.md").read_text(encoding="utf-8").splitlines())
runbooks = "\n".join(
    (raiz / "docs/runbooks" / n).read_text(encoding="utf-8")
    for n in ("MIRAR-EL-MATERIAL.md", "RITUAL.md", "DECISIONES-DE-PROCESO.md")
)
historia = (raiz / "docs/state/HISTORIA.md").read_text(encoding="utf-8")
cola = historia[historia.index("# Technical Debt RECLASIFICADA · sale de PROJECT_STATE.md en trabajo/previa-sesion-5"):]
salen = [l for l in antes if l not in ahora and l.strip()]
mal = 0
for l in salen:
    en_rb = l.strip() in runbooks
    en_hi = l.strip() in cola
    print(("OK " if en_rb and en_hi else "FALTA ") + f"runbook={en_rb} historia={en_hi} | {l[:90]}")
    mal += not (en_rb and en_hi)
print(f"{len(salen)} lineas salen; {mal} sin destino completo")
