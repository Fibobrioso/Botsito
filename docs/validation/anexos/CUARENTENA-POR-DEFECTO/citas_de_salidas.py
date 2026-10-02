"""Que lineas de las salidas de medicion son de segmentos que hoy se ocultan, y quien las copia.

Anexo de `docs/validation/CUARENTENA-POR-DEFECTO.md` (cuarta orden del consultor, 2026-10-01,
punto 3, y quinta orden). Cada salida de `cuarentena.SALIDAS_DE_MEDICIONES` trae pasajes
(`=== ... PASAJE k | <transcripcion> | ...`) con una linea por segmento
(`[h:mm:ss-h:mm:ss] #n texto`). Una linea es OCULTA si el segmento `n` de esa transcripcion esta
hoy en lo que oculta el filtro (`cuarentena.filtro_de` sobre su cruda): es la definicion EXACTA.

La primera version de este anexo usaba otra -«la linea esta en la salida commiteada y no en la de
hoy»- y CONTABA DE MAS: cuando el termino de un pasaje cae en un segmento oculto, el pasaje
entero deja de salir, con sus vecinos VISIBLES. Se dejan las dos cuentas lado a lado.

Para las lineas ocultas, se buscan copias (`cuarentena.copia`: la mitad o mas de sus ventanas de 30
caracteres) en todos los ficheros de texto seguidos por git, menos las propias salidas y las
propuestas (ya en la lista). Imprime SOLO rutas y cuentas: ni una linea, ni un trozo, ni una fecha.

    uv run python docs/validation/anexos/CUARENTENA-POR-DEFECTO/citas_de_salidas.py
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from botsito.cli import _carpeta_datos
from botsito.corpus.cuarentena import (
    SALIDAS_DE_MEDICIONES,
    Filtro,
    copia,
    filtro_de,
    plano,
    ventanas_de_copia,
)
from botsito.corpus.manifiestos_transcripcion import cargar_todos, carpeta_de
from botsito.corpus.pipeline_transcripcion import cargar_cruda

RAIZ = Path(__file__).resolve().parents[4]
CABECERA = re.compile(r"^=== .*?PASAJE \d+ \| (tr-[^ |]+)")
LINEA = re.compile(r"^\[[\d:]+-[\d:]+\] #(\d+) (.*)$")
EXTENSIONES = {".md", ".txt", ".yaml", ".yml", ".py", ".json", ".jsonl"}


def _guion(nombre: str):  # type: ignore[no-untyped-def]
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def filtros_por_transcripcion() -> dict[str, Filtro]:
    datos = _carpeta_datos(RAIZ)
    salida: dict[str, Filtro] = {}
    for t in cargar_todos(RAIZ):
        filtro = filtro_de(RAIZ, t.video_id)
        try:
            cargar_cruda(carpeta_de(datos, t), filtro)  # anota lo que oculta
        except OSError:
            continue
        salida[t.id] = filtro
    return salida


def lineas(rel: str, filtros: dict[str, Filtro]) -> tuple[list[str], list[str]]:
    """(ocultas: su segmento esta oculto hoy, visibles), por la definicion exacta."""
    ocultas: list[str] = []
    visibles: list[str] = []
    tr = None
    for ln in (RAIZ / rel).read_text(encoding="utf-8").splitlines():
        if m := CABECERA.match(ln):
            tr = m.group(1)
            continue
        m = LINEA.match(ln)
        if m is None or tr is None:
            continue
        oculta = int(m.group(1)) in filtros[tr].ocultos
        (ocultas if oculta else visibles).append(m.group(2))
    return ocultas, visibles


def ya_no_salen(rel: str, nombre: str, conjunto: str | None) -> int:
    """La cuenta VIEJA: lineas de segmento commiteadas que hoy no salen."""
    guion = _guion(nombre)
    hoy = set(guion.buscar() if conjunto is None else guion.buscar(guion.CONJUNTOS[conjunto]))
    return sum(
        1
        for ln in (RAIZ / rel).read_text(encoding="utf-8").splitlines()
        if LINEA.match(ln) and ln not in hoy
    )


def citadas(textos_lineas: list[str], textos: dict[str, str]) -> Counter[str]:
    por_fichero = Counter[str]()
    for texto in textos_lineas:
        ventanas = ventanas_de_copia(texto)
        for r, contenido in textos.items():
            if copia(contenido, ventanas):
                por_fichero[r] += 1
    return por_fichero


def main() -> int:
    filtros = filtros_por_transcripcion()
    seguidos = subprocess.run(
        ["git", "ls-files"], cwd=RAIZ, capture_output=True, text=True, check=True
    ).stdout.splitlines()
    textos: dict[str, str] = {}
    for r in seguidos:
        if (
            Path(r).suffix not in EXTENSIONES
            or r in SALIDAS_DE_MEDICIONES
            or r.startswith("knowledge/_proposals/")
        ):
            continue
        try:
            textos[r] = plano((RAIZ / r).read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            continue
    total = Counter[str]()
    for rel, (nombre, conjunto) in sorted(SALIDAS_DE_MEDICIONES.items()):
        ocultas, visibles = lineas(rel, filtros)
        print(
            f"{rel}: {len(ocultas)} lineas de segmentos ocultos hoy "
            f"(la cuenta vieja, «ya no salen»: {ya_no_salen(rel, nombre, conjunto)})"
        )
        por_fichero = citadas(ocultas, textos)
        for r, n in sorted(por_fichero.items()):
            print(f"  la copia {r}: {n}")
        control = citadas(visibles, textos)
        print(
            f"  CONTROL: de {len(visibles)} lineas visibles, {sum(control.values())} copias "
            f"en {len(control)} ficheros"
        )
        total.update(por_fichero)
    print(f"TOTAL ficheros que copian alguna linea oculta: {len(total)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
