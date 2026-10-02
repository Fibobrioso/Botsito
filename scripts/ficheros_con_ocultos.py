"""Escribe (o comprueba) la lista de ficheros que la guardia no deja leer: copian texto oculto.

La lista se CALCULA (ordenes del consultor del 2026-10-01, rama `trabajo/cuarentena-por-defecto`,
tercera, cuarta y quinta), no se escribe a mano:
- las propuestas de `knowledge/_proposals/` con algun segmento oculto
  (`botsito.corpus.cuarentena.propuestas_con_ocultos`);
- las salidas commiteadas de los guiones de medicion (`cuarentena.SALIDAS_DE_MEDICIONES`) que traen
  alguna linea de un segmento que hoy se oculta: la linea `[h:mm:ss-h:mm:ss] #n texto` de un pasaje
  de la transcripcion `tr-…` es oculta si el filtro de esa cruda oculta el segmento `n`;
- los ficheros de `docs/` seguidos por git que COPIAN alguna de esas lineas
  (`cuarentena.copia`: la mitad o mas de sus ventanas de 30 caracteres; quinta orden).
Imprime solo rutas y cuentas, nunca contenido. Sin los datos de las transcripciones en la maquina
(la CI) las dos ultimas partes no se pueden calcular, y lo dice.

Uso:
    uv run python scripts/ficheros_con_ocultos.py            (comprueba; sale con 1 si no cuadra)
    uv run python scripts/ficheros_con_ocultos.py --escribir (la reescribe; exige los datos)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import (
    DIRECTORIO_PROPUESTAS,
    FICHERO_OCULTOS,
    SALIDAS_DE_MEDICIONES,
    Filtro,
    copia,
    filtro_de,
    plano,
    propuestas_con_ocultos,
    texto_de_la_lista,
    ventanas_de_copia,
)
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import FICHERO_CRUDA, cargar_cruda

RAIZ = Path(__file__).resolve().parents[1]
CABECERA = re.compile(r"^=== .*?PASAJE \d+ \| (tr-[^ |]+)")
LINEA = re.compile(r"^\[[\d:]+-[\d:]+\] #(\d+) (.*)$")
EXTENSIONES = {".md", ".txt", ".yaml", ".yml", ".json", ".jsonl"}


def _filtros(raiz: Path) -> dict[str, Filtro] | None:
    """Por transcripcion, el filtro que ya paso por su cruda (anota lo que oculta); None si falta
    alguna cruda en la maquina."""
    datos = _carpeta_datos(raiz)
    salida: dict[str, Filtro] = {}
    for t in cargar_todos(raiz):
        carpeta = carpeta_de(datos, t)
        if not (carpeta / FICHERO_CRUDA).is_file():
            return None
        filtro = filtro_de(raiz, t.video_id)
        cargar_cruda(carpeta, filtro)
        salida[t.id] = filtro
    return salida


def lineas_ocultas(raiz: Path, rel: str, filtros: dict[str, Filtro]) -> list[str]:
    """El texto de las lineas de `rel` cuyo segmento esta oculto hoy (no se imprime)."""
    salida: list[str] = []
    tr = None
    for ln in (raiz / rel).read_text(encoding="utf-8").splitlines():
        if m := CABECERA.match(ln):
            tr = m.group(1)
            continue
        m = LINEA.match(ln)
        if m is not None and tr is not None and int(m.group(1)) in filtros[tr].ocultos:
            salida.append(m.group(2))
    return salida


def _que_copian(raiz: Path, lineas: list[str], excluidos: set[str]) -> list[str]:
    seguidos = subprocess.run(
        ["git", "ls-files", "docs"], cwd=raiz, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    ventanas = [v for v in (ventanas_de_copia(t) for t in lineas) if v]
    salida: list[str] = []
    for rel in seguidos:
        if rel in excluidos or Path(rel).suffix not in EXTENSIONES:
            continue
        try:
            texto = plano((raiz / rel).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
        if any(copia(texto, v) for v in ventanas):
            salida.append(rel)
    return salida


def calcular(raiz: Path) -> tuple[list[str], list[str] | None]:
    """(propuestas, salidas y ficheros de docs/ que copian sus lineas ocultas); la segunda es None
    si no hay datos para calcularla."""
    propuestas = [f"{DIRECTORIO_PROPUESTAS}/{n}" for n in propuestas_con_ocultos(raiz)]
    filtros = _filtros(raiz)
    if filtros is None:
        return propuestas, None
    ocultas = {rel: lineas_ocultas(raiz, rel, filtros) for rel in sorted(SALIDAS_DE_MEDICIONES)}
    salidas = [rel for rel, lineas in ocultas.items() if lineas]
    todas = [t for lineas in ocultas.values() for t in lineas]
    return propuestas, salidas + _que_copian(raiz, todas, set(SALIDAS_DE_MEDICIONES))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--escribir", action="store_true")
    args = ap.parse_args(argv)
    propuestas, otros = calcular(RAIZ)
    print(f"propuestas con segmentos ocultos: {len(propuestas)}")
    if otros is None:
        print("salidas e informes: sin los datos de las transcripciones, no se calculan")
    else:
        print(f"salidas de medicion con lineas ocultas, y ficheros que las copian: {len(otros)}")
        for rel in otros:
            print(f"  {rel}")
    destino = RAIZ / FICHERO_OCULTOS
    if args.escribir:
        if otros is None:
            print("ERROR: --escribir exige los datos de las transcripciones")
            return 1
        destino.write_text(texto_de_la_lista(propuestas + otros), encoding="utf-8", newline="\n")
        print(f"OK: {len(propuestas) + len(otros)} ficheros en {FICHERO_OCULTOS}")
        return 0
    actual = destino.read_text(encoding="utf-8") if destino.is_file() else ""
    if otros is None:
        listadas = [ln for ln in actual.splitlines() if ln and not ln.startswith("#")]
        otros = [r for r in listadas if not r.startswith(f"{DIRECTORIO_PROPUESTAS}/")]
    if actual != texto_de_la_lista(propuestas + otros):
        print(f"ERROR: {FICHERO_OCULTOS} no coincide con lo calculado: --escribir")
        return 1
    print(f"OK: {FICHERO_OCULTOS} coincide")
    return 0


if __name__ == "__main__":
    sys.exit(main())
