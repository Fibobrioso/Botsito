"""VISOR-CONSTRUCCION (R3.2): la comprobacion de UN dia, en el orden que manda la respuesta del
consultor a la PARADA 2 (punto 1: `contexto_h4.py` ANTES de generar CADA pagina).

1. `contexto_h4.py <caso>`: si la pagina pintaria una vela de un dia oculto o de un mes reservado,
   NO se genera la pagina y el dia se mira solo con la traza («sin pagina: su contexto pintaria un
   dia oculto (contexto_h4.py)»; punto 0 de esa respuesta).
2. La pagina del visor, con el comando de la corrida 2 (`botsito motor visor --simular
   --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria
   --caso <caso> --salida <paginas>`), a la carpeta `--paginas`: `data/visor/visor-construccion`
   (ignorada por git) o una carpeta temporal fuera del repo.
3. `extraer_pagina.py <pagina> --sin-hechos`: lo del dia dev de la pagina.
4. `traza_por_cierre.py <caso> [--sesion S] --rn004 --gates`: la traza por cierre, que PARA
   (codigo 3) si sus ordenes no son las de main.
5. `ticks_del_rechazo.py <caso>`: los rechazos por `precio_invalido`, frente al bid y el ask.
Cada salida va a `<dias>/<fecha>.<paso>.txt`. Codigo 3 si la traza no reproduce main (PARADA).

Las dos carpetas en que escribe llegan por argumento, no de la ruta del guion (CLAUDE.md, «Ensayos
aislados», punto 2; hallazgo a1 del revisor). Los anexos de la rama se escribieron con
`--dias docs/validation/anexos/VISOR-CONSTRUCCION/dias --paginas data/visor/visor-construccion`.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/revisar_dia.py <caso>...
        --dias <carpeta> --paginas <carpeta> [--sesion S]
"""

from __future__ import annotations

import argparse
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import contexto_h4  # noqa: E402
import extraer_pagina  # noqa: E402
import ticks_del_rechazo  # noqa: E402
import traza_por_cierre  # noqa: E402

from botsito import cli  # noqa: E402

OPCIONES_CORRIDA_2 = [
    "--simular",
    "--diagnostico-a35",
    "cierre_vela_contraria",
    "--diagnostico-a44",
    "sin_tope",
    "--diagnostico-cuenta-diaria",
]
ROTULO = ".DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria"


def _paso(nombre: str, funcion: Any, *args: Any) -> tuple[int, str]:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        codigo = funcion(*args)
    return int(codigo or 0), buffer.getvalue()


def _escribir(dias: Path, fecha: str, paso: str, texto: str) -> None:
    dias.mkdir(parents=True, exist_ok=True)
    (dias / f"{fecha}.{paso}.txt").write_text(texto, encoding="utf-8", newline="\n")


def main(caso: str, sesion: str | None, dias: Path, paginas: Path) -> int:
    fecha = caso.removeprefix("caso-eurusd-")
    codigo, texto = _paso("contexto", contexto_h4.main, [caso])
    _escribir(dias, fecha, "contexto", texto)
    print(texto, end="")
    if codigo == 0:
        codigo_v, texto_v = _paso(
            "visor",
            cli.main,
            ["motor", "visor", *OPCIONES_CORRIDA_2, "--caso", caso, "--salida", str(paginas)],
        )
        if codigo_v != 0:
            print(texto_v)
            return codigo_v
        pagina = paginas / f"{caso}{ROTULO}.html"
        _, texto_p = _paso("pagina", extraer_pagina.main, pagina, True)
        _escribir(dias, fecha, "pagina", texto_p)
        print(f"pagina generada y extraida: dias/{fecha}.pagina.txt")
    else:
        aviso = "sin pagina: su contexto pintaria un dia oculto (contexto_h4.py)\n"
        _escribir(dias, fecha, "pagina", aviso)
        print(aviso, end="")
    # RN-004 y los gates van siempre (las dos sesiones sin camino y las 14 sin orden)
    codigo_t, texto_t = _paso(
        "traza", traza_por_cierre.main, caso, sesion, True, False, None, True
    )
    _escribir(dias, fecha, "traza" if sesion is None else f"traza.{sesion}", texto_t)
    print(texto_t.splitlines()[1] if len(texto_t.splitlines()) > 1 else texto_t)
    if codigo_t != 0:
        return codigo_t
    _, texto_k = _paso("ticks", ticks_del_rechazo.main, caso)
    _escribir(dias, fecha, "ticks", texto_k)
    print(texto_k.splitlines()[-1] if texto_k else "")
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("casos", nargs="+")
    p.add_argument("--dias", required=True, type=Path, help="carpeta de las salidas por dia")
    p.add_argument("--paginas", required=True, type=Path, help="carpeta de las paginas del visor")
    p.add_argument("--sesion")
    a = p.parse_args()
    peor = 0
    for c in a.casos:
        print(f"== {c}")
        peor = max(peor, main(c, a.sesion, a.dias.resolve(), a.paginas.resolve()))
        if peor == 3:
            break  # la traza no reproduce main: PARADA
    raise SystemExit(peor)
