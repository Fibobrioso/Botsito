"""Decision del consultor del 2026-10-05 sobre ev-v10-010438-0d4e6798, punto 4, SOLO MEDIDA (no se
arregla aqui): los segmentos VISIBLES que el filtro de Q taparia solo porque un tramo no citable,
registrado con el inicio o el fin redondeado al segundo, les pisa un trozo. Para la fase 0 de la
activacion de E.

Criterio, sin texto: un segmento que se solapa mas de 0 ms con la UNION de los tramos de su video
pero no cabe entero en ella.
- Si sobresale por el INICIO del tramo, es visible: un tramo de cuarentena empieza en el segundo
  truncado de su primer segmento oculto, asi que el segmento que asoma por delante es el anterior.
- Si sobresale por el FIN, es visible cuando el tramo lleva el segundo de margen (los de v9, desde
  sus companeros, y los de v10), porque el ultimo oculto acaba antes del fin del tramo.
- Los tramos de precaucion y de conversacion cubren lineas visibles; uno que les asoma por un borde
  tambien sale aqui, con la clase del tramo.

Los segmentos salen por `contexto.crudas` (el llamador autorizado); solo `n`, `t0_ms` y `t1_ms`.

Uso: uv run python docs/validation/anexos/VENTANA-EV-V9/medir_recortados.py
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from botsito.corpus.inventario import cargar_manifiesto
from botsito.validation.contexto_evidencia import construir_contexto
from botsito.validation.knowledge import _carpeta_datos

RAIZ = Path(__file__).resolve().parents[4]


def union(tramos: list[tuple[int, int]]) -> list[tuple[int, int]]:
    salida: list[tuple[int, int]] = []
    for a, b in sorted(tramos):
        if salida and a <= salida[-1][1]:
            salida[-1] = (salida[-1][0], max(salida[-1][1], b))
        else:
            salida.append((a, b))
    return salida


def clase(motivo: str) -> str:
    m = motivo.lower()
    for prefijo in ("cuarentena mecanica", "completa el tramo", "precauci", "sin audio"):
        if m.startswith(prefijo):
            return prefijo
    return " ".join(m.split()[:3])


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}.{ms % 1000:03d}"


def main() -> None:
    ruta = RAIZ / "knowledge" / "corpus" / "manifest.yaml"
    contexto, _ = construir_contexto(
        RAIZ, _carpeta_datos(RAIZ), cargar_manifiesto(ruta) if ruta.exists() else None
    )
    print("| video | segmento | t0-t1 (ms) | lado | tramo que lo pisa | clase | solape (ms) |")
    print("|---|---|---|---|---|---|---|")
    total = 0
    for video in sorted(contexto.tramos_no_citables, key=lambda v: int(v[1:])):
        tramos = contexto.tramos_no_citables[video]
        tid = contexto.activas.get(video)
        segmentos = contexto.crudas(tid) if tid and contexto.crudas else None
        if segmentos is None:
            print(f"| {video} | cruda ausente: no se mide | | | | | |")
            continue
        bloques = union([(a, b) for a, b, _ in tramos])
        n_video = 0
        for s in segmentos:
            for a, b in bloques:
                if not (s.t1_ms > a and s.t0_ms < b) or (a <= s.t0_ms and s.t1_ms <= b):
                    continue
                lado = "inicio" if s.t0_ms < a else "fin"
                borde = a if lado == "inicio" else b
                (x, y, motivo) = next(
                    t for t in tramos if (t[0] == borde if lado == "inicio" else t[1] == borde)
                )
                solape = min(s.t1_ms, b) - max(s.t0_ms, a)
                print(
                    f"| {video} | {s.n} | {s.t0_ms}-{s.t1_ms} | {lado} | "
                    f"{hms(x)}-{hms(y)} | {clase(motivo)} | {solape} |"
                )
                n_video += 1
        print(f"| {video} | total: {n_video} | | | | | |")
        total += n_video
    print(f"TOTAL (asoman por un borde): {total}")
    print()
    dentro(contexto)


_RANGO = re.compile(r"segmentos (\d+)-(\d+)")


def dentro(contexto: Any) -> None:
    """Los segmentos visibles que caben ENTEROS dentro de un tramo de cuarentena mecanica, en su
    segundo redondeado (v9 1:07:45, v10 0:00:58). En v7 y v9 el motivo del tramo dice que segmentos
    oculto el filtro («segmentos 609-612»): lo demas que haya dentro es visible SEGURO. En v10 el
    motivo no lo dice: un segmento dentro del primer o del ultimo segundo del tramo es POSIBLE, y
    distinguirlo de uno oculto exige la filtrada (la fase 0 de la activacion de E)."""
    print("| video | segmento | t0-t1 (ms) | tramo | dentro del borde | visible |")
    print("|---|---|---|---|---|---|")
    seguros = posibles = 0
    for video in sorted(contexto.tramos_no_citables, key=lambda v: int(v[1:])):
        tramos = contexto.tramos_no_citables[video]
        tid = contexto.activas.get(video)
        segmentos = contexto.crudas(tid) if tid and contexto.crudas else None
        if segmentos is None:
            continue
        ocultos: set[int] = set()
        for _a, _b, motivo in tramos:
            if (m := _RANGO.search(motivo)) is not None:
                ocultos |= set(range(int(m.group(1)), int(m.group(2)) + 1))
        vistos: set[int] = set()
        for a, b, motivo in tramos:
            if clase(motivo) not in ("cuarentena mecanica", "completa el tramo"):
                continue
            for s in segmentos:
                if s.n in vistos or not (a <= s.t0_ms and s.t1_ms <= b):
                    continue
                if ocultos and s.n in ocultos:
                    continue
                borde = s.t1_ms <= a + 1000 or s.t0_ms >= b - 1000
                if ocultos:
                    veredicto = "seguro"
                    seguros += 1
                elif borde:
                    veredicto = "posible"
                    posibles += 1
                else:
                    continue
                vistos.add(s.n)
                print(
                    f"| {video} | {s.n} | {s.t0_ms}-{s.t1_ms} | {hms(a)}-{hms(b)} | "
                    f"{'si' if borde else 'no'} | {veredicto} |"
                )
    print(f"TOTAL dentro: {seguros} seguros, {posibles} posibles")


if __name__ == "__main__":
    main()
