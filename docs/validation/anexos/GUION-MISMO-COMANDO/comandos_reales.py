"""trabajo/guion-mismo-comando, fase 1: la guardia de `main` y la de la rama sobre los comandos
REALES de Bash de una sesion de Claude Code (su transcripcion `.jsonl`), contra el repositorio real.

Solo llama a `decidir()` de las dos guardias con el texto de cada comando; no ejecuta ninguno. Dice
cuantos cambian de decision y, uno a uno, los que pasan a negarse (lo que cuesta la regla). Sale con
1 si alguno que `main` niega pasa en la rama. Un comando que nombra el material adicional o un
backtest no se imprime: solo se cuenta.

Uso: python comandos_reales.py <transcripcion.jsonl> <guardia de main> <guardia de la rama> <raiz>
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

NO_SE_IMPRIME = ("material adicional", "backtest")


def cargar(ruta: str, nombre: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def comandos(transcripcion: Path) -> list[str]:
    salida: list[str] = []
    for linea in transcripcion.open(encoding="utf-8"):
        try:
            d = json.loads(linea)
        except ValueError:
            continue
        if d.get("type") != "assistant":
            continue
        for bloque in d.get("message", {}).get("content", []) or []:
            if isinstance(bloque, dict) and bloque.get("type") == "tool_use":
                if bloque.get("name") == "Bash":
                    salida.append(str(bloque.get("input", {}).get("command", "")))
    return salida


def main() -> int:
    transcripcion, de_main, de_rama, raiz = sys.argv[1:5]
    g_main, g_rama = cargar(de_main, "guardia_main"), cargar(de_rama, "guardia_rama")
    todos = comandos(Path(transcripcion))
    distintos = list(dict.fromkeys(todos))
    nuevos_niega: list[tuple[str, str]] = []
    malos: list[str] = []
    iguales = 0
    for comando in distintos:
        evento = {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": raiz}
        antes = g_main.decidir(evento, g_main.Politica(Path(raiz)))
        ahora = g_rama.decidir(evento, g_rama.Politica(Path(raiz)))
        if (antes is None) == (ahora is None):
            iguales += 1
        elif ahora is not None:
            nuevos_niega.append((comando, ahora.splitlines()[0]))
        else:
            malos.append(comando)
    print(f"Comandos de Bash en la transcripcion: {len(todos)}; distintos: {len(distintos)}")
    print(f"Misma decision en main y en la rama: {iguales}")
    print(f"main los deja pasar y la rama los niega: {len(nuevos_niega)}")
    print(f"main los niega y la rama los deja pasar: {len(malos)}")
    # El desglose, sobre el motivo ENTERO (no el recortado que se imprime abajo): revisor, A5.
    motivos: dict[str, int] = {}
    delante: dict[str, int] = {}
    for _comando, motivo in nuevos_niega:
        cuerpo = motivo.split("`: ", 1)[-1]
        if cuerpo.startswith("antes, en el mismo comando, va `"):
            clave = "algo delante que no esta en la lista cerrada"
            programa = cuerpo.split("`", 2)[1].split(" ", 1)[0]
            programa = "una asignacion" if "=" in programa else programa.rsplit("/", 1)[-1]
            delante[programa] = delante.get(programa, 0) + 1
        elif cuerpo.startswith("detras, en la misma tuberia"):
            clave = "algo detras, en la tuberia, que no es un filtro"
        elif "sustitucion" in cuerpo:
            clave = "una sustitucion en el comando"
        else:
            clave = cuerpo[:70]
        motivos[clave] = motivos.get(clave, 0) + 1
    print("\n== Por motivo")
    for clave, n in sorted(motivos.items(), key=lambda kv: -kv[1]):
        print(f"{n:5}  {clave}")
    print("\n== Lo que va delante (primer programa)")
    for clave, n in sorted(delante.items(), key=lambda kv: -kv[1]):
        print(f"{n:5}  {clave}")
    print("\n== Los que pasan a negarse (comando, 120 caracteres; y el motivo de la rama)")
    for comando, motivo in nuevos_niega:
        if any(s in comando.lower() for s in NO_SE_IMPRIME):
            print("- [no se imprime: nombra el material adicional o un backtest]")
            continue
        print(f"- {comando.replace(chr(10), ' \\n ')[:120]}")
        print(f"    {motivo[:160]}")
    if malos:
        print("\n== main los niega y la rama los deja pasar")
        for comando in malos:
            print(f"- {comando[:120]}")
    return 1 if malos else 0


if __name__ == "__main__":
    raise SystemExit(main())
