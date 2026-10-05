"""Fase 2: antes y despues de la regla por condicion, SIN texto: solo recuentos, marcas de tiempo e
ids de evidencia.

- v1-v6 (no son sesiones en cuarentena): el `Filtro` REAL de la libreria sobre la transcripcion
  activa, con los meses libres de HOY (`cases.holdout.meses_libres`, escenario B) frente a los
  libres que equivalen a la lista vieja (todos menos septiembre, marzo, mayo y febrero: sus
  grafias y abreviaturas no cambiaron, asi que la regla vieja ES la nueva con esos libres).
  Cuenta los segmentos ocultos por la regla (c) en cada caso.
- v7-v10 (sesiones): sus versiones filtradas, rehechas con el guion de `main` (el revisado), que
  no pasa `libres` y por eso sale en el escenario A (los doce meses). Compara las marcas
  `[CUARENTENA mm:ss-mm:ss]` con las de la filtrada de antes, si la hay, y cruza los items ev-*
  con los bloques que antes no estaban.

Uso: uv run python docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase2.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.cases.holdout import meses_libres
from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import MOTIVO_RESERVADO, Filtro, cargar_tramos_no_citables
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
ESCRITORIO = Path(r"C:\Users\USER\Desktop")
# video -> (filtrada de antes o None, filtrada de despues)
SESIONES = {
    "v7": (None, ESCRITORIO / "sesion-02-v7-audio" / "sesion-02-v7.filtrada.md"),
    "v8": (None, ESCRITORIO / "sesion-02-v8-audio" / "sesion-02-v8.filtrada.md"),
    "v9": (
        ESCRITORIO / "sesion-03-audio" / "sesion-03.filtrada-ANTES-condicion.md",
        ESCRITORIO / "sesion-03-audio" / "sesion-03.filtrada.md",
    ),
    "v10": (
        ESCRITORIO / "sesion-04-audio" / "sesion-04.filtrada-ANTES-condicion.md",
        ESCRITORIO / "sesion-04-audio" / "sesion-04.filtrada.md",
    ),
}
LIBRES_DE_LA_LISTA_VIEJA = frozenset(range(1, 13)) - {2, 3, 5, 9}
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")


def _bloques(ruta: Path) -> list[tuple[int, int]]:
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _BLOQUE.match(linea):
            a = (int(m.group(1)) * 60 + int(m.group(2))) * 1000
            b = (int(m.group(3)) * 60 + int(m.group(4)) + 1) * 1000
            salida.append((a, b))
    return sorted(salida)


def _hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    libres = meses_libres(RAIZ)
    print(f"meses libres hoy: {len(libres) if libres is not None else 'None (se tapan los doce)'}")
    tramos = cargar_tramos_no_citables(RAIZ)
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    datos = _carpeta_datos(RAIZ)
    todas = cargar_todos(RAIZ)
    reemplazadas = {t.supersede for t in todas if t.supersede}
    print("| video | antes (c) | despues (c) | nuevos | items ev-* en los nuevos |")
    print("|---|---|---|---|---|")
    for t in todas:
        if t.id in reemplazadas or t.video_id in SESIONES:
            continue
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            print(f"| {t.video_id} | cruda ausente | | | |")
            continue
        cuentas = {}
        ocultos = {}
        for nombre, lib in (("antes", LIBRES_DE_LA_LISTA_VIEJA), ("despues", libres)):
            filtro = Filtro(t.video_id, tramos.get(t.video_id, ()), libres=lib)
            cargar_cruda(carpeta, filtro)
            ocultos[nombre] = {
                n: o for n, o in filtro.ocultos.items() if o.motivo == MOTIVO_RESERVADO
            }
            cuentas[nombre] = len(ocultos[nombre])
        nuevos = sorted(set(ocultos["despues"]) - set(ocultos["antes"]))
        quitados = set(ocultos["antes"]) - set(ocultos["despues"])
        afectados = sorted(
            it.id
            for it in items
            if it.transcripcion == t.id
            and any(
                it.t1_ms > ocultos["despues"][n].t0_ms and it.t0_ms < ocultos["despues"][n].t1_ms
                for n in nuevos
            )
        )
        marcas = ", ".join(_hms(ocultos["despues"][n].t0_ms) for n in nuevos)
        print(
            f"| {t.video_id} | {cuentas['antes']} | {cuentas['despues']} | {len(nuevos)}"
            + (f" ({marcas})" if nuevos else "")
            + (f"; {len(quitados)} dejan de ocultarse" if quitados else "")
            + f" | {len(afectados)}"
            + (f" ({', '.join(afectados)})" if afectados else "")
            + " |"
        )
    print()
    print("| sesion | bloques antes | despues (A) | bloques nuevos | items ev-* en los nuevos |")
    print("|---|---|---|---|---|")
    for v, (antes, despues) in SESIONES.items():
        if not despues.is_file():
            print(f"| {v} | | filtrada todavia no rehecha | | |")
            continue
        nuevos_b = _bloques(despues)
        # Antes: los bloques de la filtrada vieja; si no queda en la maquina (v7, v8), los tramos
        # no citables del video, que es donde se registraron sus bloques de cuarentena.
        if antes is not None:
            viejos_b = _bloques(antes)
        else:
            viejos_b = [(a, b) for a, b, _ in tramos.get(v, ())]
        # Un bloque es nuevo si no cabe entero dentro de uno de antes.
        candidatos = [
            (a, b) for a, b in nuevos_b if not any(x <= a and b <= y for x, y in viejos_b)
        ]
        afectados = sorted(
            it.id
            for it in items
            if it.video_id == v and any(it.t1_ms > a and it.t0_ms < b for a, b in candidatos)
        )
        origen = "" if antes is not None else " (sus tramos no citables)"
        print(
            f"| {v} | {len(viejos_b)}{origen} "
            f"| {len(nuevos_b)} | "
            + (f"{len(candidatos)} ({', '.join(_hms(a) for a, _ in candidatos)})")
            + f" | {len(afectados)}"
            + (f" ({', '.join(afectados)})" if afectados else "")
            + " |"
        )


if __name__ == "__main__":
    main()
