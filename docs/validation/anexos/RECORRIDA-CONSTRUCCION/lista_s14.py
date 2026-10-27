"""La lista «Para S-14» (RECORRIDA-CONSTRUCCION): cada sesion de P6 de la corrida 2 (el bot opera
y el trader no), por dia y sesion, con el camino del bot, su resultado en R, si la cuenta
arrastrada de la corrida 1 llega a esa sesion, y si el dia viene de video. SOLO LEE las salidas
commiteadas de los anexos; no corre nada.

uso: uv run python lista_s14.py <carpeta de anexos RECORRIDA-CONSTRUCCION>
"""

from __future__ import annotations

import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

carpeta = Path(sys.argv[1])
sys.path.insert(0, str(carpeta))
import patrones  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]

DIARIA = carpeta / "diaria.DIAGNOSTICO.cuenta=diaria.txt"
ARRASTRADA = carpeta / "cuenta-arrastrada.txt"
ENTRADAS = carpeta / "entradas-antes-alternancia.txt"
ROTULO = "[DIAGNOSTICO"
# que viene de video (ACTIVAR-SESION-05.md §0.b.7): abril solo el 29 (v5); julio «si, segun el
# trader» (v11-v13, sin comprobar hasta T); enero y agosto no
VIDEO = {"2026-04-29": "si (v5)"}
VIDEO_MES = {"2026-07": "segun el trader (v11-v13; lo comprueba T)"}


# La marca de la respuesta del consultor a la PARADA 3 (punto 1 a): la llenada que el broker hizo
# con el respaldo M1 en la vela cuyo cierre coloco la orden (RECORRIDA-CONSTRUCCION.md §2.8)
MARCA_E = "E: llenada con la vela que la colocó (ADR-0051 §2)"


def sin_rotulo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def llenadas_con_su_vela(ls: list[str]) -> set[tuple[str, str]]:
    """(dia, instante ISO del llenado) de cada orden que el broker lleno con el respaldo M1 en la
    vela cuyo cierre la coloco: «### Eventos del broker» con `llenada` y `respaldo_m1`, y en
    «### Ordenes» la orden colocada 1 ms antes de ese instante (el cierre de la misma vela)."""
    colocada: dict[tuple[str, str], str] = {}
    respaldo: list[tuple[str, str, str]] = []
    seccion = ""
    for ln in ls:
        if ln.startswith("### "):
            seccion = ln
            continue
        if not ln.startswith("20"):
            continue
        p = ln.split(" | ")
        if seccion.startswith("### Ordenes ("):
            colocada[(p[0], p[2])] = p[3]
        elif seccion.startswith("### Eventos del broker") and p[2:] == [
            "llenada",
            p[3],
            "respaldo_m1",
        ]:
            respaldo.append((p[0], p[3], p[1]))
    salida: set[tuple[str, str]] = set()
    for dia, orden, llenada in respaldo:
        ms_col = datetime.fromisoformat(colocada[(dia, orden)]).timestamp() * 1000
        ms_ll = datetime.fromisoformat(llenada).timestamp() * 1000
        if round(ms_ll - ms_col) == 1:
            salida.add((dia, llenada))
    return salida


# 0. las llenadas de la corrida 2 hechas con la vela que coloco la orden
CON_SU_VELA = llenadas_con_su_vela([sin_rotulo(x) for x in DIARIA.read_text("utf-8").splitlines()])

# 1. las filas P6 de la corrida 2, por (dia, sesion)
filas, sesgo = patrones.leer(DIARIA)
p6: dict[tuple[str, str], list[str]] = defaultdict(list)
marcadas_e = 0
for patron, _detalle, marca, fila in patrones.clasificar(filas, sesgo):
    if patron.startswith("P6"):
        p = fila.split(" | ")
        marcas = [marca] if marca else []
        if (p[1], p[4]) in CON_SU_VELA:
            marcas.append(MARCA_E)
            marcadas_e += 1
        p6[(p[1], p[2])].append(f"{p[3]} {p[4]} {p[5]}" + "".join(f" [{m}]" for m in marcas))

# 2. del guion de f): R, sesgo y camino por (dia, sesion), de la tabla «Todas las llenadas»
todas: dict[tuple[str, str], list[list[str]]] = defaultdict(list)
dentro = False
for ln in ENTRADAS.read_text(encoding="utf-8").splitlines():
    if ln.startswith("## Todas las llenadas"):
        dentro = True
        continue
    if dentro and ln.startswith("20"):
        p = ln.split(" | ")
        todas[(p[0], p[1])].append(p)

# 3. la corrida 1: veredicto, instante del corte, y en que sesiones opero (llenadas de «Ordenes»)
arr = [sin_rotulo(ln) for ln in ARRASTRADA.read_text(encoding="utf-8").splitlines()]
estado = next((ln for ln in arr if ln.startswith("estado: ")), "estado: ?")
instante = next((ln for ln in arr if ln.startswith("instante: ")), "instante: ?")
corte = instante.split(": ", 1)[1]
llenadas_arr: dict[tuple[str, str], int] = defaultdict(int)
dentro = False
for ln in arr:
    if ln.startswith("### Ordenes ("):
        dentro = True
        continue
    if dentro and (ln.startswith("### ") or ln.startswith("ordenes: ")):
        break
    if dentro and ln.startswith("20") and ln.split(" | ")[5] == "llenada":
        p = ln.split(" | ")
        llenadas_arr[(p[0], p[1])] += 1

# la ultima sesion en que la corrida 1 lleno una orden: despues de ella la cuenta arrastrada no
# corta el tramo, pero el bot no vuelve a colocar nada (RN-032 prohibe abrir desde ahi; el motivo,
# medido en las lineas «Por sesion» de la corrida 1, va en el informe §2.2)
ultima = max(llenadas_arr) if llenadas_arr else ("", "")
print(f"corrida 1: {estado}; {instante}; ultima sesion con un llenado: {ultima[0]} {ultima[1]}")
print(f"sesiones P6 en la corrida 2: {len(p6)}; filas P6: {sum(len(v) for v in p6.values())}")
marcadas_sesiones = sum(1 for ops in p6.values() if any(MARCA_E in o for o in ops))
print(
    f"llenadas de la corrida 2 con la vela que coloco la orden: {len(CON_SU_VELA)}; de ellas en "
    f"P6: {marcadas_e}, en {marcadas_sesiones} sesiones de esta lista [{MARCA_E}]"
)
print(
    "dia | sesion | mes viene de video | operaciones del bot (lado, llenada, entrada) | sesgo | "
    "camino del bot | R de cada llenada | la cuenta arrastrada (corrida 1) llega a la sesion | "
    "llenadas de la corrida 1 en esa sesion"
)
for (dia, ses), ops in sorted(p6.items()):
    video = VIDEO.get(dia) or VIDEO_MES.get(dia[:7], "no")
    filas_t = todas.get((dia, ses), [])
    sesgo_t = filas_t[0][14] if filas_t and len(filas_t[0]) > 14 else "-"
    camino = filas_t[0][15] if filas_t and len(filas_t[0]) > 15 else "-"
    erres = "; ".join(f"{f[4][11:19]}Z {f[12]}" for f in filas_t) or "-"
    n_arr = llenadas_arr.get((dia, ses), 0)
    if corte != "-" and dia >= corte[:10]:
        llega = "NO: la cuenta corto antes"
    elif (dia, ses) <= ultima:
        llega = "si" + (
            f" (la corrida 1 lleno {n_arr})" if n_arr else " (sin llenado en la corrida 1)"
        )
    else:
        llega = (
            "la cuenta no corta el tramo (EN_CURSO), pero es posterior a la ultima sesion con un "
            f"llenado de la corrida 1 ({ultima[0]} {ultima[1]}): desde ahi el bot no coloca nada"
        )
    print(
        f"{dia} | {ses} | {video} | {'; '.join(ops)} | {sesgo_t} | {camino} | {erres} | {llega} | "
        f"{llenadas_arr.get((dia, ses), 0)}"
    )
