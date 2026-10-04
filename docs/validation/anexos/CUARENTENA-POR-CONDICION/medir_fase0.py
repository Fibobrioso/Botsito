"""HISTORICO: se ejecuto en `ad4fd75` (fase 0) y su salida es `medir_fase0-SALIDA.txt`. Desde la
fase 1 NO CORRE: importa `_RE_MES`, que la fase 1 elimino, y sus entradas -las filtradas de v9 y
v10- se rehicieron en la fase 2. Se conserva como la medida que fue (revisor de la rama, A1); la
de despues es `medir_fase2.py`.

Fase 0, punto 4: la regla nueva medida SIN aplicarla. Solo recuentos y marcas de tiempo:
nunca texto, nunca que mes.

Escenarios:
  A: hoy no hay fuente de los meses reservados enteros (b), asi que (c) filtra los 12 meses;
  B: con una fuente de (b) que declare los dos meses reservados enteros sin casos que el repo
     nombra en prosa (los que hoy cubre MESES_FILTRADOS y no tienen casos), el filtro tapa los
     meses con casos ocultos o reservados mas esos dos.
Para cada video: segmentos que pasarian a ocultos (con su vecino anterior y siguiente, como la
regla de hoy) y que hoy se ensenan; e items ev-* cuyo intervalo pisa alguno de ellos.
"""

import re
from pathlib import Path

from botsito.cases.holdout import casos_ocultos, casos_reservados
from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import (
    _RE_MES,
    Filtro,
    cargar_tramos_no_citables,
    normalizar,
    numeros_a_cifras,
)
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(r"C:\Users\USER\Desktop\Bot v3")
FILTRADAS = {
    "v9": Path(r"C:\Users\USER\Desktop\sesion-03-audio\sesion-03.filtrada.md"),
    "v10": Path(r"C:\Users\USER\Desktop\sesion-04-audio\sesion-04.filtrada.md"),
}
# Nombres por mes, normalizados: espanol, ingles y abreviatura de tres letras (y sus variantes).
NOMBRES = {  # (nombres completos en espanol e ingles, abreviatura espanola de tres letras)
    1: (["enero", "january"], ["ene"]),
    2: (["febrero", "february"], ["feb"]),
    3: (["marzo", "march"], ["mar"]),
    4: (["abril", "april"], ["abr"]),
    5: (["mayo", "may"], ["may"]),
    6: (["junio", "june"], ["jun"]),
    7: (["julio", "july"], ["jul"]),
    8: (["agosto", "august"], ["ago"]),
    9: (["septiembre", "setiembre", "september"], ["sep", "sept"]),
    10: (["octubre", "october"], ["oct"]),
    11: (["noviembre", "november"], ["nov"]),
    12: (["diciembre", "december"], ["dic"]),
}


def meses_con_casos() -> set[int]:
    casos = set(casos_ocultos(RAIZ)) | set(casos_reservados(RAIZ))
    return {int(m) for c in casos for m in re.findall(r"\d{4}-(\d{2})-\d{2}$", c)}


def patron(meses: set[int], clase: str = "todo") -> re.Pattern[str]:
    idx = {"nombre": (0,), "abrev": (1,), "todo": (0, 1)}[clase]
    nombres = [n for m in sorted(meses) for k in idx for n in NOMBRES[m][k]]
    return re.compile(r"\b(?:" + "|".join(nombres) + r")\b")


def nuevos(lineas: list[tuple[int, int, int, str]], pat: re.Pattern[str]) -> list[int]:
    """lineas: (posicion, t0_ms, t1_ms, texto) de los segmentos VISIBLES, en orden. Devuelve las
    posiciones que la regla nueva taparia (con vecinos) y la de hoy no."""
    marcados = set()
    for i, (_, _, _, texto) in enumerate(lineas):
        t = numeros_a_cifras(normalizar(texto))
        if pat.search(t) and not _RE_MES.search(t):
            marcados.add(i)
    con_vecinos = set()
    for i in marcados:
        for j in (i - 1, i, i + 1):
            if 0 <= j < len(lineas) and (j == i or lineas[j][0] == lineas[i][0] + (j - i)):
                con_vecinos.add(j)
    return sorted(con_vecinos)


def mmss(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    casos = meses_con_casos()
    sin_casos_cubiertos = {2, 3, 5, 9} - casos  # los que hoy cubre la lista y no tienen casos
    escenarios = {"A": set(range(1, 13)), "B": casos | sin_casos_cubiertos}
    print(
        f"meses con casos: {len(casos)}; escenario A filtra {len(escenarios['A'])} meses; "
        f"escenario B filtra {len(escenarios['B'])}"
    )
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    tramos = cargar_tramos_no_citables(RAIZ)
    datos = _carpeta_datos(RAIZ)
    por_video: dict[str, list[tuple[int, int, int, str]]] = {}
    transcripcion_de: dict[str, str] = {}
    todas = cargar_todos(RAIZ)
    reemplazadas = {t.supersede for t in todas if t.supersede}
    for t in todas:
        carpeta = carpeta_de(datos, t)
        if t.id in reemplazadas:
            continue
        if t.video_id in FILTRADAS or not (carpeta / FICHERO_CRUDA).is_file():
            continue
        filtro = Filtro(t.video_id, tramos.get(t.video_id, ()))
        visibles = cargar_cruda(carpeta, filtro)
        if not visibles:
            print(
                f"{t.video_id} ({t.id}): 0 segmentos visibles (sesion en cuarentena), "
                "no medible aqui"
            )
            continue
        por_video[t.video_id] = [(s.n, s.t0_ms, s.t1_ms, s.texto) for s in visibles]
        transcripcion_de[t.video_id] = t.id
    for v, ruta in FILTRADAS.items():
        filas = []
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\[(\d+):(\d\d)\] (.*)$", linea)
            if m:
                filas.append(((int(m.group(1)) * 60 + int(m.group(2))) * 1000, m.group(3)))
        filas.sort()
        ocultos_tramo = tramos.get(v, ())
        lineas = []
        for k, (t0, texto) in enumerate(filas):
            t1 = filas[k + 1][0] if k + 1 < len(filas) else t0 + 5000
            if any(t1 > a and t0 < b for a, b, _ in ocultos_tramo):
                continue
            lineas.append((k, t0, t1, texto))
        por_video[v] = lineas
    print(
        "activas: "
        + ", ".join(
            f"{v}={transcripcion_de[v]}" for v in sorted(transcripcion_de, key=lambda x: int(x[1:]))
        )
    )
    otras = [
        it.id
        for it in items
        if it.video_id in transcripcion_de and it.transcripcion != transcripcion_de[it.video_id]
    ]
    print(f"items que citan una transcripcion NO activa (no se cruzan): {len(otras)}")
    for v in sorted(por_video, key=lambda x: int(x[1:])):
        lineas = por_video[v]
        for nombre, meses in escenarios.items():
            pos = nuevos(lineas, patron(meses))
            afectados = sorted(
                it.id
                for it in items
                if it.video_id == v
                and (v in FILTRADAS or it.transcripcion == transcripcion_de.get(v))
                and any(it.t1_ms > lineas[p][1] and it.t0_ms < lineas[p][2] for p in pos)
            )
            marcas = ", ".join(mmss(lineas[p][1]) for p in pos)
            solo_nombre = len(nuevos(lineas, patron(meses, "nombre")))
            solo_abrev = len(nuevos(lineas, patron(meses, "abrev")))
            print(
                f"{v} {nombre}: [por nombre {solo_nombre}, por abreviatura {solo_abrev}] "
                f"{len(pos)} segmentos nuevos de {len(lineas)} visibles; "
                f"{len(afectados)} items ev-* dentro"
                + (f"; en {marcas}" if nombre == "B" and pos else "")
            )
            if afectados and nombre == "B":
                print(f"   items B: {', '.join(afectados)}")
            elif afectados:
                print(f"   items A: {len(afectados)}")
    for v in ("v7", "v8"):
        if v not in por_video:
            print(
                f"{v}: sin filtrada en disco y con la cruda en cuarentena: NO MEDIBLE en esta fase"
            )


main()
