"""Fase 0 de `trabajo/filtradas-escenario-b`: lo que se puede medir SIN ESCRIBIR NADA, sin texto.

Para cada sesion (v7-v10) lee de sus ficheros fuera del repositorio SOLO:
- las marcas `[CUARENTENA mm:ss-mm:ss]` de la filtrada de ANTES (v9, v10) y de la actual (A);
- las lineas de recuento de su registro (`segmentos`, `segmentos en cuarentena`, `motivos`), que no
  traen texto del trader;
y del repositorio, los tramos no citables (el «antes» de v7 y v8) y los intervalos de los items
ev-*. Imprime recuentos, marcas de tiempo, limites en ms e ids. Nunca una linea de texto.

El escenario B NO se mide aqui: para las sesiones, la regla mecanica solo la aplica el guion
revisado (`scripts/transcribir_sesion.py`), que siempre escribe la filtrada; el `Filtro` de la
libreria oculta la sesion entera (motivo a), y leer la cruda con otro codigo lo bloquea la guardia.
Ver el informe.

Caso negativo conocido: v8, que en A da 0 bloques y no tiene tramos.

Uso: uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/medir_fase0.py
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia

RAIZ = Path(__file__).resolve().parents[4]
E = Path(r"C:\Users\USER\Desktop")
# video -> (hoja, filtrada ANTES o None, registro ANTES o None, filtrada A, registro A)
SESIONES = {
    "v7": ("02", None, None, E / "sesion-02-v7-audio" / "sesion-02-v7.filtrada.md",
           E / "sesion-02-v7-audio" / "sesion-02-v7.registro.txt"),
    "v8": ("02", None, None, E / "sesion-02-v8-audio" / "sesion-02-v8.filtrada.md",
           E / "sesion-02-v8-audio" / "sesion-02-v8.registro.txt"),
    "v9": ("03", E / "sesion-03-audio" / "sesion-03.filtrada-ANTES-condicion.md",
           E / "sesion-03-audio" / "sesion-03.registro-ANTES-condicion.txt",
           E / "sesion-03-audio" / "sesion-03.filtrada.md",
           E / "sesion-03-audio" / "sesion-03.registro.txt"),
    "v10": ("04", E / "sesion-04-audio" / "sesion-04.filtrada-ANTES-condicion.md",
            E / "sesion-04-audio" / "sesion-04.registro-ANTES-condicion.txt",
            E / "sesion-04-audio" / "sesion-04.filtrada.md",
            E / "sesion-04-audio" / "sesion-04.registro.txt"),
}  # fmt: skip
_BLOQUE = re.compile(r"^\[CUARENTENA (\d+):(\d\d)–(\d+):(\d\d)\]$")
_CUENTA = re.compile(r"^segmentos en cuarentena: (\d+) en (\d+) bloques$")


def bloques(ruta: Path) -> list[tuple[int, int]]:
    """(t0_ms, t1_ms) de cada marca; t1 un segundo despues, para cubrir el ultimo segmento."""
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _BLOQUE.match(linea):
            a = (int(m.group(1)) * 60 + int(m.group(2))) * 1000
            b = (int(m.group(3)) * 60 + int(m.group(4)) + 1) * 1000
            salida.append((a, b))
    return sorted(salida)


_MARCA = re.compile(r"^\[(\d+):(\d\d)\] ")


def marcas_visibles(ruta: Path) -> list[int]:
    """El instante (ms) de cada linea visible de una filtrada; solo la marca, nunca el texto."""
    salida = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        if m := _MARCA.match(linea):
            salida.append((int(m.group(1)) * 60 + int(m.group(2))) * 1000)
    return salida


def cabe(a: int, b: int, x: int, y: int) -> bool:
    """El bloque [a, b) cabe en el intervalo [x, y), con un segundo de tolerancia en el final: la
    marca de la filtrada trunca al segundo y `bloques` le suma uno, y algunos tramos (los de v9)
    terminan en el segundo exacto. Sin la tolerancia, el control positivo de v9 fallaba (6 de 8)."""
    return x <= a and b <= y + 1000


def cuenta(registro: Path) -> tuple[int, int] | None:
    for linea in registro.read_text(encoding="utf-8").splitlines():
        if m := _CUENTA.match(linea):
            return int(m.group(1)), int(m.group(2))
    return None


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    print(
        "| video | hoja | antes: segmentos/bloques | A: segmentos/bloques | bloques de A que no "
        "estaban antes | items ev-* en ellos |"
    )
    print("|---|---|---|---|---|---|")
    for v, (hoja, f_antes, r_antes, f_a, r_a) in SESIONES.items():
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]
        if f_antes is not None and r_antes is not None:
            antes = bloques(f_antes)
            c = cuenta(r_antes)
            txt_antes = f"{c[0]}/{c[1]}" if c else "?"
        else:
            antes = de_tramos
            txt_antes = f"sin filtrada; {len(de_tramos)} tramos"
        en_a = bloques(f_a)
        ca = cuenta(r_a)
        nuevos_a = [(a, b) for a, b in en_a if not any(cabe(a, b, x, y) for x, y in antes)]
        caen = sorted(
            it.id for it in items
            if it.video_id == v and any(it.t1_ms > a and it.t0_ms < b for a, b in nuevos_a)
        )  # fmt: skip
        print(
            f"| {v} | {hoja} | {txt_antes} | {ca[0]}/{ca[1] if ca else '?'} | {len(nuevos_a)}"
            + (f" ({', '.join(hms(a) for a, _ in nuevos_a)})" if nuevos_a else "")
            + f" | {len(caen)}"
            + (f" ({', '.join(caen)})" if caen else "")
            + " |"
        )
    print()
    print("tramos no citables por sesion (limites en ms):")
    for v in SESIONES:
        print(f"  {v}: {len(tramos.get(v, ()))} tramos")
    print()
    # Las filtradas NO aplican los tramos no citables: el guion solo conoce la regla mecanica.
    # Cuantas lineas VISIBLES empiezan dentro de un tramo, en ANTES y en A. Solo se lee la marca
    # [mm:ss] del principio de cada linea; el texto que la sigue no se guarda ni se imprime.
    print("lineas visibles cuya marca cae dentro de un tramo no citable (sin texto):")
    for v, (_, f_antes, _, f_a, _) in SESIONES.items():
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]
        for nombre, ruta in (("ANTES", f_antes), ("A", f_a)):
            if ruta is None:
                continue
            marcas = marcas_visibles(ruta)
            dentro = [t for t in marcas if any(x <= t < y for x, y in de_tramos)]
            tramos_tocados = sorted(
                {i for t in dentro for i, (x, y) in enumerate(de_tramos) if x <= t < y}
            )
            inicios = ", ".join(hms(de_tramos[i][0]) for i in tramos_tocados)
            print(
                f"  {v} {nombre}: {len(dentro)} lineas en {len(tramos_tocados)} de "
                f"{len(de_tramos)} tramos"
                + (f" (tramos que empiezan en {inicios})" if tramos_tocados else "")
            )
    print()
    v8 = bloques(SESIONES["v8"][3])
    print(
        f"CASO NEGATIVO v8: {len(v8)} bloques en A y {len(tramos.get('v8', ()))} tramos "
        f"(esperado 0 y 0)"
    )
    # Control POSITIVO de la logica de contencion: los bloques de ANTES de v9 y v10 se registraron
    # como tramos no citables en sus ramas (sesion 3 y sesion 4), asi que cada uno tiene que caber
    # en un tramo. Si la comparacion de intervalos estuviera mal, aqui saldrian bloques fuera.
    for v in ("v9", "v10"):
        f_antes = SESIONES[v][1]
        assert f_antes is not None
        de_tramos = [(a, b) for a, b, _ in tramos.get(v, ())]
        fuera = [a for a, b in bloques(f_antes) if not any(cabe(a, b, x, y) for x, y in de_tramos)]
        print(
            f"CONTROL POSITIVO {v}: {len(bloques(f_antes))} bloques de ANTES, {len(fuera)} fuera "
            f"de un tramo (esperado 0)"
        )


if __name__ == "__main__":
    main()
