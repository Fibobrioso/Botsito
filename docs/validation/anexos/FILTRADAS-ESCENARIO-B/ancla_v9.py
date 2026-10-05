"""Tercera respuesta del consultor, punto 1, SOLO CON MARCAS: el bloque que completa el tramo de v9
0:34:44-0:34:56 y la linea que le sigue, en la filtrada ANTES de v9 y en la A. No imprime texto: de
cada linea, solo su clase (BLOQUE, VISIBLE, «…», SECCION, vacia) y su marca.

- (a) el bloque `[CUARENTENA 34:44–34:56]` existe y termina en la marca 34:56;
- (b) la linea siguiente del fichero es VISIBLE, lleva la marca 34:56 y esta en la misma seccion
  (la filtrada va agrupada por pregunta: solo dentro de una seccion y sin «…» entre medias la linea
  siguiente del fichero es el segmento siguiente de la cruda);
- (c) lo que las marcas pueden decir del ancla de ev-v9-003456-9ef48fb5 (t0 0:34:56, t1 0:35:00):
  que lineas y bloques hay en su ventana de localizacion, con la tolerancia de 2 s de
  `TOLERANCIA_CITA_MS` (0:34:54-0:35:02).

Cuarta respuesta del consultor, punto 1 (`ancla_validate`): el ancla del item medida con la MISMA
localizacion de citas que `uv run botsito knowledge validate`, llamada como la llama validate
(`src/botsito/validation/knowledge.py`: `cargar_evidencia`, `cargar_manifiesto`,
`construir_contexto(repo, _carpeta_datos(repo), manifiesto)` y `verificar_citas(items, contexto)`
con TODOS los items). De los segmentos solo se leen `n`, `t0_ms` y `t1_ms`, por el mismo
`contexto.crudas` que usa `verificar_citas`. No imprime texto, ni palabras, ni longitudes de cita.

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/ancla_v9.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.corpus.inventario import cargar_manifiesto
from botsito.evidence.modelo import cargar_evidencia, verificar_citas
from botsito.validation.contexto_evidencia import construir_contexto
from botsito.validation.knowledge import _carpeta_datos

RAIZ = Path(__file__).resolve().parents[4]
ITEM = "ev-v9-003456-9ef48fb5"
# El bloque [CUARENTENA 34:44–34:56] por sus marcas (segundos truncados) y el segmento que le sigue
# en la filtrada (34:58): asi se encuentra en la lista de segmentos que usa validate.
BLOQUE_T0_S, BLOQUE_T1_S, SIGUIENTE_T0_S = 34 * 60 + 44, 34 * 60 + 56, 34 * 60 + 58

D = Path(r"C:\Users\USER\Desktop\sesion-03-audio")
FICHEROS = {"ANTES": D / "sesion-03.filtrada-ANTES-condicion.md", "A": D / "sesion-03.filtrada.md"}
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")
VENTANA = (34 * 60 + 54, 35 * 60 + 2)  # segundos: [t0 - 2 s, t1 + 2 s] del item


def clase(linea: str) -> tuple[str, str]:
    """(clase, marca) de una linea, sin su texto."""
    if m := _BLOQUE.match(linea):
        return "BLOQUE", f"{m.group(1)}:{m.group(2)}–{m.group(3)}:{m.group(4)}"
    if m := _MARCA.match(linea):
        return "VISIBLE", f"{m.group(1)}:{m.group(2)}"
    if linea == "…":
        return "…", ""
    if linea.startswith("## "):
        return "SECCION", ""
    if not linea.strip():
        return "vacia", ""
    return "otra", ""


def segundos(marca: str) -> int:
    m, s = marca.split(":")
    return int(m) * 60 + int(s)


def main() -> None:
    for nombre, ruta in FICHEROS.items():
        lineas = ruta.read_text(encoding="utf-8").splitlines()
        print(f"== {nombre}")
        donde = [i for i, ln in enumerate(lineas) if clase(ln) == ("BLOQUE", "34:44–34:56")]
        print(f"(a) bloques [CUARENTENA 34:44–34:56]: {len(donde)}")
        for i in donde:
            print(f"    linea {i + 1}: BLOQUE 34:44–34:56")
            for k in range(i + 1, min(i + 4, len(lineas))):
                c, mm = clase(lineas[k])
                print(f"    linea {k + 1}: {c} {mm}".rstrip())
        print("(c) en la ventana 34:54-35:02 (por marca de inicio; bloques por solape):")
        seccion = 0
        for i, ln in enumerate(lineas):
            c, mm = clase(ln)
            if c == "SECCION":
                seccion += 1
            if c == "VISIBLE" and VENTANA[0] <= segundos(mm) <= VENTANA[1]:
                print(f"    linea {i + 1} (seccion {seccion}): VISIBLE {mm}")
            if c == "BLOQUE":
                a, b = (segundos(x) for x in mm.split("–"))
                if a <= VENTANA[1] and b >= VENTANA[0]:
                    print(f"    linea {i + 1} (seccion {seccion}): BLOQUE {mm}")


def ancla_validate() -> None:
    """La localizacion de validate para ITEM: solo indices y milisegundos."""
    repo = RAIZ
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    ruta_manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
    manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
    contexto, _temas = construir_contexto(repo, _carpeta_datos(repo), manifiesto)
    problemas, _avisos, localizaciones = verificar_citas(items, contexto)
    item = next(i for i in items if i.id == ITEM)
    print(f"== ancla de {ITEM} con verificar_citas (la de knowledge validate)")
    print(f"ventana declarada: {item.t0_ms}-{item.t1_ms} ms")
    propios = [p for p in problemas if p.startswith(ITEM)]
    print(f"problemas de cita de este item: {len(propios)}")
    for p in propios:  # mensajes de plantilla de verificacion.py: tiempos, sin texto
        print(f"    {p}")
    loc = localizaciones.get(ITEM)
    if loc is None or item.transcripcion is None or contexto.crudas is None:
        print("SIN LOCALIZACION: caso (c)")
        return
    segmentos = list(contexto.crudas(item.transcripcion) or [])
    por_n = {s.n: s for s in segmentos}
    print(f"apariciones de la cita en la ventana (coincidencias): {loc.coincidencias}")
    print(f"avisos de tiempos parciales o de segmento: {len(loc.avisos)}")
    print("segmentos en que caen las palabras citadas (n, t0_ms, t1_ms):")
    for n in loc.segmentos:
        print(f"    {n} {por_n[n].t0_ms} {por_n[n].t1_ms}")
    candidatos = [
        k
        for k in range(len(segmentos) - 1)
        if segmentos[k].t1_ms // 1000 == BLOQUE_T1_S
        and segmentos[k + 1].t0_ms // 1000 == SIGUIENTE_T0_S
    ]
    print(f"segmentos con fin en 34:56 seguidos de uno que empieza en 34:58: {len(candidatos)}")
    if len(candidatos) != 1:
        print("BLOQUE NO IDENTIFICADO: caso (c)")
        return
    k = candidatos[0]
    primero = k
    while primero > 0 and segmentos[primero - 1].t0_ms // 1000 >= BLOQUE_T0_S:
        primero -= 1
    ultimo = segmentos[k]
    print(
        f"bloque en la lista de validate: posiciones {primero}-{k}, n {segmentos[primero].n}-"
        f"{ultimo.n}; el primero empieza en el segundo {segmentos[primero].t0_ms // 1000} "
        f"(34:44 = {BLOQUE_T0_S})"
    )
    print(f"ultimo segmento del bloque: n {ultimo.n}, t1_ms {ultimo.t1_ms}")
    dentro = [n for n in loc.segmentos if segmentos[primero].n <= n <= ultimo.n]
    despues = [n for n in loc.segmentos if n > ultimo.n]
    if loc.coincidencias != 1:
        veredicto = "(c) ambigua: la cita aparece mas de una vez en la ventana"
    elif dentro:
        veredicto = f"(b) {len(dentro)} segmento(s) de la cita dentro del bloque"
    elif len(despues) == len(loc.segmentos):
        veredicto = "(a) todas las palabras citadas caen despues del bloque"
    else:
        veredicto = "(c) palabras antes del bloque"
    print(f"VEREDICTO: {veredicto}")


if __name__ == "__main__":
    main()
    ancla_validate()
