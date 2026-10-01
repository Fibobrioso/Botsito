"""La dieta de PROJECT_STATE.md (rama `trabajo/dieta-y-skills`, 2026-10-01).

Guion de UNA sola ejecucion, guardado como anexo del informe para que se pueda repetir y leer.
No escribe en el repositorio: escribe en la carpeta que se le pasa (`--salida`), y la sesion copia
de ahi lo que va al repositorio.

Hace tres cosas, todas sobre `git show df6aa2c:PROJECT_STATE.md` (el fichero ANTES de la dieta):

1. `original.md`: el fichero ENTERO tal cual, byte a byte, que la sesion pone como «Archivo 1» de
   `docs/state/HISTORIA.md` debajo de su cabecera. Asi la comprobacion de que ningun texto se
   pierde es literal: el original esta dentro de HISTORIA (`tests/unit/test_historia.py`).
2. `deuda.md`: de cada entrada de Technical Debt que su propio texto NO da por cerrada, su ARRANQUE
   LITERAL (un prefijo del texto original, comprobado aqui), para la seccion nueva.
3. `ambiguedades.md`: la tabla de las ABIERTAS, generada de `knowledge/spec/ambiguedades.yaml`.

Uso: uv run python docs/validation/anexos/DIETA-Y-SKILLS/dieta.py --salida <carpeta fuera del repo>
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
ORIGEN = "df6aa2c"

# Entradas de Technical Debt (numeradas desde 1 en el orden del fichero) que su PROPIO TEXTO da
# por cerradas, con la palabra que lo dice. Se quedan solo en HISTORIA.md.
CERRADAS = {
    7: "RESUELTA",
    8: "DECIDIDO",
    10: "RESUELTA",
    11: "CORREGIDA",
    16: "DECIDIDA",
    25: "CERRADA",
    39: "APLICADO",
    40: "REGISTRADOS",
    41: "RESUELTO",
    44: "RESUELTOS",
    45: "REGISTRADO",
    46: "RESUELTA",
    47: "CERRADA",
    50: "CERRADA",
    51: "HECHO",
}
# La entrada de los cinco patrones de defecto es una REGLA viva: va entera, tal cual, a
# docs/runbooks/ERRORES-RECURRENTES.md, y aqui queda su arranque con el puntero.
PATRONES = 20
FECHA_ENTRE_PARENTESIS = re.compile(r"\(\d{4}-\d{2}-\d{2}[^()]*\)")
MAX_ARRANQUE = 420
ENTRADA_CORTA = 300


def _git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=RAIZ,
        capture_output=True,
        check=True,
    )
    return r.stdout.decode("utf-8")


def secciones(texto: str) -> dict[str, str]:
    """`## titulo` -> cuerpo (sin la linea del titulo), en el orden del fichero."""
    salida: dict[str, str] = {}
    actual = None
    trozos: list[str] = []
    for linea in texto.split("\n"):
        if linea.startswith("## "):
            if actual is not None:
                salida[actual] = "\n".join(trozos)
            actual, trozos = linea[3:].strip(), []
        elif actual is not None:
            trozos.append(linea)
    if actual is not None:
        salida[actual] = "\n".join(trozos)
    return salida


def entradas(cuerpo: str) -> list[str]:
    """Las entradas de una lista markdown: cada una empieza por `- ` en la columna 0."""
    salida: list[str] = []
    for linea in cuerpo.split("\n"):
        if linea.startswith("- "):
            salida.append(linea)
        elif salida and linea.strip():
            salida[-1] += "\n" + linea
    return salida


def arranque(entrada: str) -> str:
    """El arranque literal de una entrada: entera si es corta; si no, hasta el primer parentesis
    con fecha, o hasta el primer punto o dos puntos, o la primera linea entera. Siempre un PREFIJO
    del texto original."""
    if len(entrada) <= ENTRADA_CORTA:
        return entrada
    primera = entrada.split("\n", 1)[0]
    m = FECHA_ENTRE_PARENTESIS.search(primera)
    if m and m.end() <= MAX_ARRANQUE:
        corte = m.end()
        if primera[corte : corte + 1] in {".", ":"}:
            corte += 1
        return primera[:corte]
    for sep in (". ", ": "):
        i = primera.find(sep)
        if 0 < i <= MAX_ARRANQUE:
            return primera[: i + 1]
    return primera if len(primera) <= MAX_ARRANQUE else primera[:MAX_ARRANQUE] + "…"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True, type=Path)
    args = ap.parse_args()
    salida: Path = args.salida.resolve()
    if salida == RAIZ or RAIZ in salida.parents:
        print("ERROR: --salida tiene que estar FUERA del repositorio", file=sys.stderr)
        return 2
    salida.mkdir(parents=True, exist_ok=True)

    original = _git("show", f"{ORIGEN}:PROJECT_STATE.md")
    (salida / "original.md").write_text(original, encoding="utf-8", newline="\n")

    deuda = entradas(secciones(original)["Technical Debt"])
    lineas: list[str] = []
    for n, e in enumerate(deuda, start=1):
        if n in CERRADAS:
            assert CERRADAS[n] in e, (n, CERRADAS[n])
            continue
        a = arranque(e)
        assert a.rstrip("…") and e.startswith(a.rstrip("…")), n
        lineas.append(a)
    (salida / "deuda.md").write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    print(f"deuda: {len(deuda)} entradas, {len(CERRADAS)} cerradas, {len(lineas)} con arranque")
    print(f"patrones: {deuda[PATRONES - 1][:60]}")

    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases.ambiguedades import cargar_ambiguedades

    ambs = cargar_ambiguedades(RAIZ / "knowledge" / "spec" / "ambiguedades.yaml")
    filas = [
        "| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |",
        "|---|---|---|---|---|",
    ]
    for a in ambs:
        if a.estado == "ABIERTA":
            filas.append(
                f"| {a.id} | {a.titulo} | {a.clase} | {'si' if a.bloqueante else 'no'} | "
                f"{', '.join(a.resuelve_en)} |"
            )
    (salida / "ambiguedades.md").write_text("\n".join(filas) + "\n", encoding="utf-8", newline="\n")
    print(f"ambiguedades abiertas: {len(filas) - 2}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
