"""La busqueda de A-24, A-21, A-26 y A-34 en las transcripciones, CONGELADA antes de ejecutarla.

Documento: `docs/validation/A24-A21-A26-A34-CRITERIO.md` (2026-09-24, rama
`trabajo/a24-a21-a26-a34`). Reutiliza `scripts/a18_buscar.py` -mismo alcance, misma integridad,
misma normalizacion y la misma ventana de +-45 s con union de solapes- con dos diferencias:

- una lista CERRADA de terminos POR AMBIGUEDAD, solo frases o combinaciones especificas: ningun
  termino de una sola palabra de uso constante (liquidez, zona, M15, H4, sesgo, vela, pivote);
- un pasaje mide como mucho 180 s; una union mas larga se corta en pasajes consecutivos, y cada
  uno lista sus propias coincidencias.

Se busca por separado para cada ambiguedad, asi que un mismo tramo puede salir en mas de una.

  `uv run python scripts/buscar_ambiguedades.py --salida <fichero>`

A-35 (cuando un pivote de M15 esta formado) tiene su PROPIA lista cerrada, congelada en
`docs/validation/A35-PIVOTE-FORMADO-CRITERIO.md` (2026-09-24, rama `trabajo/a35-pivote-formado`),
con el mismo metodo. Va en un conjunto aparte para que la salida de A-24, A-21, A-26 y A-34 se siga
reproduciendo byte a byte:

  `uv run python scripts/buscar_ambiguedades.py --conjunto a35 --salida <fichero>`

Los candidatos C-01, C-02, C-04, C-05, C-06 y C-07 de la sesion 02 (huecos del motor sin
ambiguedad ni regla, `docs/validation/SESION-02-INVENTARIO.md` §4.3) van en el conjunto
`sesion02`, congelado en `docs/validation/SESION-02-BUSQUEDA-CRITERIO.md`:

  `uv run python scripts/buscar_ambiguedades.py --conjunto sesion02 --salida <fichero>`
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

RAIZ = Path(__file__).resolve().parent
MAXIMO_MS = 180_000
# LOS TERMINOS, lista cerrada por ambiguedad y en los dos sentidos. No se anade ni se quita ninguno
# despues de ver resultados.
TERMINOS: dict[str, tuple[str, ...]] = {
    "A-24": (
        "más reciente", "más recientes", "estructura más reciente", "más próximo", "más cercano",
        "más extremo", "alto más alto", "bajo más bajo", "el más alto", "el más bajo",
        "punto más alto", "punto más bajo", "que tú consideres", "que yo considere",
        "yo considero", "invadiría", "no se toma en cuenta", "velas atrás",
    ),
    "A-21": (
        "zona limpia", "zona de control limpia", "sea limpia", "mucho ruido", "sin ruido",
        "sin mucho ruido", "haga ruido", "hace ruido", "ruidoso", "ruidosa", "cuántas velas",
        "número de velas", "retroceso complejo", "complex pullback", "ningún retroceso",
        "segunda zona de control", "otra zona de control",
    ),
    "A-26": (
        "contra el sesgo", "contra la tendencia", "contra tendencia", "a favor de la tendencia",
        "a favor del sesgo", "sentido del sesgo", "flujo de 15", "flujo de m15", "flujo de m 15",
        "flujo en m15", "flujo en m 15", "vela contraria", "velas contrarias",
        "contraria al flujo", "envuelve", "envolvente",
    ),
    "A-34": (
        "por arriba y por abajo", "por abajo y por arriba", "los dos extremos", "ambos extremos",
        "los dos lados", "ambos lados", "las dos direcciones", "rompe los dos", "envolvente",
        "outside", "vela de 4 previa", "previa cerrada", "vela previa", "vela de 4 horas",
    ),
}  # fmt: skip
# A-35, lista cerrada propia (mismo criterio: solo frases, ninguna palabra suelta de uso constante).
# No se anade ni se quita ninguno despues de ver resultados.
TERMINOS_A35: dict[str, tuple[str, ...]] = {
    "A-35": (
        "ya formado", "ya formada", "ya formados", "ya se formó", "ya se ha formado",
        "se ha formado", "se formó", "se forme", "está formado", "esté formado",
        "formado del todo", "se termine de formar", "termina de formarse",
        "en curso", "vela cerrada", "velas cerradas", "cierre de la vela", "cierra la vela",
        "la vela cierra", "esperar el cierre", "espero el cierre", "ya cerró",
        "vela contraria", "velas contrarias", "marca un mínimo", "marca un máximo",
        "marca un alto", "marca un bajo", "máximo estructural", "mínimo estructural",
        "a cada lado", "cuántas velas",
    ),
}  # fmt: skip
# Los candidatos C-xx de la sesion 02, lista cerrada propia, congelada en
# `docs/validation/SESION-02-BUSQUEDA-CRITERIO.md` (2026-09-25, rama `trabajo/sesion-02`). Mismo
# criterio: solo frases, ninguna palabra suelta. No se anade ni se quita ninguno despues de ver
# resultados.
TERMINOS_SESION02: dict[str, tuple[str, ...]] = {
    "C-01": (
        "orden limit", "orden límite", "mi orden", "la orden limit", "pongo la orden",
        "coloco la orden", "marco mi orden", "poner la orden", "colocar la orden",
        "precio de entrada", "punto de entrada", "bloque de origen", "origen del breaker",
        "order block", "mitad de la zona", "cincuenta por ciento", "50 por ciento",
    ),
    "C-02": (
        "punto más abajo", "punto más bajo", "punto más arriba", "punto más alto",
        "caja de gann", "cuadro de gann", "nivel cero", "nivel uno", "nivel 0", "nivel 1",
        "desde aquí hasta", "de aquí hasta aquí", "de aquí a aquí", "extremo de la caja",
        "mi stop", "el stop va", "pongo el stop", "defino el stop", "definir el stop",
    ),
    "C-04": (
        "no se llenó", "no se llena", "no me llenó", "no se activó", "no se activa",
        "no me activó", "no me activa", "se fue sin", "se va sin", "se me fue", "sin activar",
        "sin activarse", "no entró", "no me entró", "cancelo la orden", "cancelar la orden",
        "quito la orden", "quitar la orden", "borro la orden", "elimino la orden",
    ),
    "C-05": (
        "siguiente sesión", "otra sesión", "nueva sesión", "cambio de sesión",
        "segunda sesión", "a las once", "de 11 a 15", "de once a", "nueva vela de 4",
        "nueva vela de cuatro", "cambia el sesgo", "cambió el sesgo", "sigue abierta",
        "sigo dentro", "la dejo abierta", "queda abierta",
    ),
    "C-06": (
        "muevo el stop", "mover el stop", "subo el stop", "bajo el stop", "subir el stop",
        "bajar el stop", "trailing stop", "arrastrar el stop", "arrastro el stop",
        "voy moviendo el stop", "asegurar ganancias", "asegurar beneficio",
        "después del break even", "luego del break even", "ya en break even",
    ),
    "C-07": (
        "dos entradas", "tres entradas", "dos operaciones", "tres operaciones",
        "una operación al día", "una entrada al día", "máximo de operaciones",
        "máximo de entradas", "como máximo", "ya no opero", "dejo de operar",
        "cierro el día", "se acabó el día", "por día", "al día",
    ),
}  # fmt: skip
CONJUNTOS = {"a24": TERMINOS, "a35": TERMINOS_A35, "sesion02": TERMINOS_SESION02}
PROHIBIDOS = {"liquidez", "zona", "m15", "h4", "sesgo", "vela", "pivote"}


def base() -> ModuleType:
    nombre = "a18_buscar"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def patrones(ambiguedad: str) -> tuple[tuple[str, object], ...]:
    b = base()
    todos = {**TERMINOS, **TERMINOS_A35, **TERMINOS_SESION02}
    return tuple((t, b.patron(t)) for t in todos[ambiguedad])


def buscar(terminos: dict[str, tuple[str, ...]] = TERMINOS) -> list[str]:
    b = base()
    lineas: list[str] = []
    segmentos: dict[str, list[object]] = {}
    for tr in b.ALCANCE:
        segs, sha = b.leer(tr)
        segmentos[tr] = segs
        lineas.append(f"INTEGRIDAD {tr} cruda.jsonl sha256 {sha} = manifiesto: OK")
    resumen: list[str] = ["== PASAJES POR AMBIGUEDAD Y TRANSCRIPCION"]
    for amb in terminos:
        lineas.append(f"== {amb}: {len(terminos[amb])} terminos")
        todos = []
        for tr in b.ALCANCE:
            todos += b.pasajes(tr, segmentos[tr], patrones(amb), MAXIMO_MS)
        for i, p in enumerate(todos, 1):
            bloque = b.formato(p, i)
            lineas.append(bloque[0].replace("=== PASAJE", f"=== {amb} · PASAJE", 1))
            lineas += bloque[1:]
        for tr in b.ALCANCE:
            resumen.append(f"{amb} {tr}: {sum(1 for p in todos if p.transcripcion == tr)}")
        resumen.append(f"{amb} TOTAL: {len(todos)}")
    return [*lineas, *resumen]


def main(argv: list[str]) -> int:
    conjunto = "a24"
    if len(argv) == 4 and argv[0] == "--conjunto" and argv[1] in CONJUNTOS:
        conjunto, argv = argv[1], argv[2:]
    if len(argv) != 2 or argv[0] != "--salida":
        print(
            "uso: buscar_ambiguedades.py [--conjunto a35|sesion02] --salida <fichero>",
            file=sys.stderr,
        )
        return 2
    salida = "\n".join(buscar(CONJUNTOS[conjunto])) + "\n"
    Path(argv[1]).write_text(salida, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
