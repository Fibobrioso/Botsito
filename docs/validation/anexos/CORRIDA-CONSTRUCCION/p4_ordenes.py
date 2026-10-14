"""Que paso con las ordenes del bot en cada sesion de P4 («sin orden»: operaciones del trader a
favor del sesgo y sin ninguna operacion del bot en la sesion), leido de «### Ordenes» de la misma
salida (respuesta del consultor a la PARADA 2, punto 4: P4 queda PENDIENTE de la lista de ordenes).
Por sesion: cuantas ordenes intento colocar el bot, cuantas se rechazaron y por que, cuantas se
cancelaron (y cuantas de ellas eran reubicaciones: RN-006 con RN-011 y RN-015 en el mismo cierre),
cuantas quedaron vivas al cerrar, y el ultimo campo de la tabla (el primer hecho del camino que
falta). Tambien el recuento de esos casos por mes y en total.

Uso: uv run python docs/validation/anexos/CORRIDA-CONSTRUCCION/p4_ordenes.py <salida>
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from patrones import clasificar, leer  # noqa: E402

REUBICACION = ("RN-006", "RN-011", "RN-015")
# Desde la respuesta del consultor a la PARADA 3 (punto 1), «Por sesion» lleva `bloqueadas`: la
# regla que PEDIA la accion, la accion y `prohibida:<efecto>` (o `gate desconocido:<efecto>`). El
# gate que prohibio no lo guarda la traza: se deduce cruzando las reglas que dispararon en la
# sesion con las que `prohibe` ese efecto en la spec. Y la regla del consultor para las 17
# sesiones sin orden (4.d), que la sesion aplica y el consultor confirma.
FIRMA_O_CUENTA = {"RN-029", "RN-030", "RN-031", "RN-032"}  # el tope diario, el total, el cierre
ESTRATEGIA = {"RN-016", "RN-035", "RN-036"}  # cartuchos, ventana, racha
POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader \d+ \| bot \d+ \| .* \| disparadas (?P<disp>[^|]*)"
    r"(?: \| bloqueadas (?P<bloq>.*))?$"
)


def reglas_que_prohiben(spec: Path) -> dict[str, set[str]]:
    """efecto -> reglas que lo prohiben, leido del texto de strategy_spec.yaml (cada regla
    empieza en `  - id: RN-` y su `prohibe: [...]` va dentro de su bloque)."""
    salida: dict[str, set[str]] = defaultdict(set)
    regla = ""
    for ln in spec.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^  - id: (RN-\d+)", ln)
        if m:
            regla = m.group(1)
        m = re.search(r"prohibe: \[([^\]]*)\]", ln)
        if m and regla:
            for efecto in m.group(1).split(","):
                salida[efecto.strip()].add(regla)
    return salida


def bloqueos_por_sesion(ruta: Path) -> dict[tuple[str, str], tuple[set[str], str]]:
    """(reglas disparadas, texto de bloqueadas) por sesion, de «Por sesion»."""
    salida: dict[tuple[str, str], tuple[set[str], str]] = {}
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        m = POR_SESION.match(ln.split("] ", 1)[-1])
        if m:
            disparadas = {
                r.strip() for r in m.group("disp").split(",") if r.strip().startswith("RN")
            }
            salida[(m.group(1), m.group(2))] = (disparadas, m.group("bloq") or "sin campo")
    return salida


def gate_que_bloqueo(
    bloqueadas: str, disparadas: set[str], prohiben: dict[str, set[str]]
) -> tuple[list[str], str]:
    """Los gates candidatos (dispararon en la sesion y prohiben el efecto bloqueado) y la clase
    provisional por la regla del consultor (4.d)."""
    efectos = set(re.findall(r"prohibida:([a-z_]+)", bloqueadas))
    if not efectos:
        return [], "sin bloqueo registrado"
    candidatos = sorted({g for e in efectos for g in prohiben.get(e, set()) if g in disparadas})
    if not candidatos:
        return [], "PARADA: ningun gate disparado prohibe ese efecto"
    if all(g in FIRMA_O_CUENTA for g in candidatos):
        return candidatos, "firma o cuenta: M o E segun si la regla esta bien aplicada ese dia"
    if all(g in ESTRATEGIA for g in candidatos):
        return candidatos, "estrategia: R, destino V"
    return candidatos, "PARADA: bloquea otra cosa (o varias)"


def ordenes_por_sesion(ruta: Path) -> dict[tuple[str, str], list[list[str]]]:
    salida: dict[tuple[str, str], list[list[str]]] = defaultdict(list)
    dentro = False
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = ln.split("] ", 1)[-1]
        if c.startswith("### Ordenes ("):
            dentro = True
            continue
        if dentro and c.startswith("### "):
            break
        if dentro and c[:4].isdigit() and " | " in c:
            campos = c.split(" | ")
            if len(campos) == 8:
                salida[(campos[0], campos[1])].append(campos)
    return salida


def resumen(ordenes: list[list[str]]) -> str:
    por_resultado: Counter[str] = Counter()
    motivos: Counter[str] = Counter()
    reubicadas = 0
    for _, _, _, _, _, resultado, motivo, _ in ordenes:
        por_resultado[resultado] += 1
        if resultado == "rechazada":
            motivos[motivo] += 1
        if resultado == "cancelada" and all(r in motivo for r in REUBICACION):
            reubicadas += 1
    partes = [f"{k} {v}" for k, v in sorted(por_resultado.items())]
    if motivos:
        partes.append("rechazos: " + ", ".join(f"{k} {v}" for k, v in sorted(motivos.items())))
    if reubicadas:
        partes.append(f"reubicaciones {reubicadas}")
    return f"ordenes {len(ordenes)}: " + "; ".join(partes) if ordenes else "ninguna orden"


def main(ruta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    filas, sesgo = leer(ruta)
    ordenes = ordenes_por_sesion(ruta)
    bloqueos = bloqueos_por_sesion(ruta)
    spec = Path(__file__).resolve().parents[3] / "knowledge" / "spec" / "strategy_spec.yaml"
    prohiben = reglas_que_prohiben(spec) if spec.exists() else {}
    p4 = [f for p, _, _, f in clasificar(filas, sesgo) if p == "P4 sin orden"]
    sesiones = sorted({tuple(f.split(" | ")[1:3]) for f in p4})
    print(f"{ruta.name}: {len(p4)} filas P4 en {len(sesiones)} sesiones")
    clases: Counter[str] = Counter()
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    sin_orden: list[str] = []
    gates: Counter[str] = Counter()
    for dia, ses in sesiones:
        ops = ordenes.get((dia, ses), [])
        n_trader = sum(1 for f in p4 if f.split(" | ")[1:3] == [dia, ses])
        hecho = next(
            f.split("primer hecho que falto: ", 1)[1]
            for f in p4
            if f.split(" | ")[1:3] == [dia, ses]
        )
        if not ops:
            clase = "sin ninguna orden colocada"
        elif all(o[5] == "rechazada" for o in ops):
            clase = "todas rechazadas"
        elif any(o[5] == "llenada" for o in ops):
            clase = "alguna llenada (fuera de la sesion de la tabla?)"
        elif all(o[5] == "cancelada" for o in ops):
            clase = "todas canceladas sin llenarse"
        else:
            clase = "rechazadas y canceladas, ninguna llenada"
        clases[clase] += 1
        por_mes[dia[:7]][clase] += 1
        print(f"{dia} {ses} | trader {n_trader} | {resumen(ops)} | {hecho} | {clase}")
        if not ops:
            disparadas, bloqueadas = bloqueos.get((dia, ses), (set(), "sin linea"))
            candidatos, provisional = gate_que_bloqueo(bloqueadas, disparadas, prohiben)
            gates[", ".join(candidatos) or "-"] += 1
            sin_orden.append(
                f"{dia} {ses} | bloqueadas {bloqueadas} | gates candidatos "
                f"{', '.join(candidatos) or '-'} | {provisional}"
            )
    print("-- sesiones P4 por clase y mes")
    for mes in sorted(por_mes):
        print(f"{mes} | " + "; ".join(f"{k} {v}" for k, v in sorted(por_mes[mes].items())))
    print("total | " + "; ".join(f"{k} {v}" for k, v in sorted(clases.items())))
    print("-- las sesiones sin ninguna orden colocada: que bloqueo (regla que pedia, accion,")
    print("   efecto) y que gates disparados prohiben ese efecto; clase provisional por 4.d")
    for ln in sin_orden:
        print(ln)
    print("gates candidatos por sesion: " + "; ".join(f"{k} {v}" for k, v in sorted(gates.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
