"""D6 de trabajo/recorrida-construccion-3: los frenos de la cuenta, como dato y sin umbral.

Uso (desde la raiz):
    uv run python -B docs/validation/anexos/RECORRIDA-CONSTRUCCION-3/frenos_julio.py \\
        <corrida 1> <delta de julio corrida 1 -> corrida 2>

Lee SOLO salidas: la corrida 1 (cuenta por mes) y el delta de julio entre ella y la diaria
(`anexos/ACTIVAR-SESION-07/delta_julio.py`). Imprime:

1. Por cada sesion de julio de 2026: cuantas filas cambian de la corrida 1 a la 2 (de patron, o
   que aparecen o desaparecen) y que frenos de la cuenta dispararon EN ESA SESION de la corrida 1
   (RN-032 y RN-036 en «disparadas» de «## Por sesion»), con lo que bloquearon («bloqueadas»). La
   linea `prohibida:abrir_operacion` de RN-015 no nombra el gate (ERRORES-RECURRENTES, fila de
   recorrida-construccion-2, leccion 5): el freno se nombra SOLO si dispara en la sesion; si no
   dispara ninguno, «ningun freno dispara en la sesion» y la causa queda sin atribuir.
2. Por cada cuenta mensual de la corrida 1: la primera sesion en que dispara RN-032 o RN-036, y el
   saldo al corte de ese dia, de la curva por dia del bloque de la cuenta (la salida no da el
   saldo por sesion). Las sesiones salen de «## Por sesion» (las que tienen operaciones del
   trader) y de las lineas «gate» de «## Avisos de orden dentro de una clase», que nombran las
   reglas de una sesion aunque no tenga operaciones del trader (hallazgo b1 del revisor); se dice
   de donde sale cada una y, por mes, cuantas sesiones con cada freno se localizan asi.

Las fechas son de dias dev de construccion; no imprime ningun precio.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader (\d+) \| bot (\d+) \| .*\| disparadas (.*?) \| "
    r"bloqueadas (.*)$"
)
FILA_DELTA = re.compile(r"^(?:[+-] )?.*?: (?:trader|bot) \| (\d{4}-\d{2}-\d{2}) \| (\S+) \| ")
AVISO_GATE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) (\S+): gate (.*)$")
CURVA = re.compile(r"^(\d{4}-\d{2}-\d{2}) \| (\S+) \| (\S+) \| (\S+)$")
FRENOS = ("RN-032", "RN-036")


def sesiones(corrida: Path) -> dict[tuple[str, str], tuple[int, int, list[str], str]]:
    salida: dict[tuple[str, str], tuple[int, int, list[str], str]] = {}
    for ln in corrida.read_text(encoding="utf-8").splitlines():
        m = POR_SESION.match(ln)
        if m:
            disparadas = [r.strip() for r in m.group(5).split(",")]
            salida[(m.group(1), m.group(2))] = (
                int(m.group(3)), int(m.group(4)), disparadas, m.group(6)
            )  # fmt: skip
    return salida


def cambios(delta: Path) -> Counter[tuple[str, str]]:
    cuenta: Counter[tuple[str, str]] = Counter()
    seccion = ""
    for ln in delta.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            seccion = ln
            continue
        if not seccion.startswith("## filas que"):
            continue
        m = FILA_DELTA.match(ln)
        if m:
            cuenta[(m.group(1), m.group(2))] += 1
    return cuenta


def curvas(corrida: Path) -> dict[str, dict[str, str]]:
    """Por mes, el saldo al corte de cada dia de la curva de su cuenta."""
    salida: dict[str, dict[str, str]] = {}
    mes = None
    for ln in corrida.read_text(encoding="utf-8").splitlines():
        if ln.startswith("### Cuenta de "):
            mes = ln.removeprefix("### Cuenta de ").strip()
            salida[mes] = {}
            continue
        if ln.startswith("#"):
            mes = None
        if mes is not None:
            m = CURVA.match(ln)
            if m:
                salida[mes][m.group(1)] = m.group(2)
    return salida


def main(corrida: Path, delta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
    por_sesion = sesiones(corrida)
    cambian = cambios(delta)
    print(f"# Los frenos de la cuenta (D6), de {corrida.name} y {delta.name}; sin umbral")
    print()
    print("## 1. Julio de 2026, por sesion: filas que cambian de la corrida 1 a la 2, y frenos")
    print("dia sesion | trader | bot (corrida 1) | filas que cambian | frenos que disparan en la "
          "corrida 1 | bloqueadas (corrida 1)")  # fmt: skip
    total = 0
    for (dia, ses), (trader, bot, disparadas, bloqueadas) in sorted(por_sesion.items()):
        if not dia.startswith("2026-07"):
            continue
        n = cambian.get((dia, ses), 0)
        total += n
        frenos = [f for f in FRENOS if f in disparadas]
        print(
            f"{dia} {ses} | {trader} | {bot} | {n} | "
            f"{', '.join(frenos) or 'ningun freno dispara en la sesion'} | {bloqueadas}"
        )
    fuera = sum(v for k, v in cambian.items() if k not in por_sesion)
    print(
        f"filas que cambian, en total: {total}; en una sesion sin operaciones del trader: {fuera}"
    )
    print()
    print("## 2. Por cuenta mensual de la corrida 1: la primera sesion con un freno y el saldo al")
    print("corte de ese dia (curva por dia del bloque de la cuenta); las sesiones, de «## Por")
    print("sesion» (con operaciones del trader) y de las lineas «gate» de «## Avisos de orden")
    print("dentro de una clase» (con o sin ellas)")
    saldos = curvas(corrida)
    con_freno = frenos_por_sesion(corrida, por_sesion)
    for mes in sorted(saldos):
        del_mes = sorted((k, v) for k, v in con_freno.items() if k[0].startswith(mes))
        cuenta = Counter(f for _, (fs, _) in del_mes for f in fs)
        recuento = ", ".join(f"{f} en {cuenta[f]} sesiones" for f in FRENOS) or "ninguno"
        if not del_mes:
            print(f"{mes}: ningun freno de la cuenta localizado en ninguna sesion ({recuento})")
            continue
        (dia, ses), (frenos, donde) = del_mes[0]
        print(
            f"{mes}: primera sesion con freno {dia} {ses} ({', '.join(frenos)}; {donde}); saldo "
            f"al corte de ese dia {saldos[mes].get(dia, 'sin dia en la curva')}; localizadas: "
            f"{recuento}"
        )
    return 0


def frenos_por_sesion(
    corrida: Path, por_sesion: dict[tuple[str, str], tuple[int, int, list[str], str]]
) -> dict[tuple[str, str], tuple[list[str], str]]:
    """Las sesiones con RN-032 o RN-036, de «Por sesion» y de las lineas «gate» de «Avisos»."""
    vistos: dict[tuple[str, str], set[str]] = {}
    for clave, (_, _, disparadas, _) in por_sesion.items():
        vistos.setdefault(clave, set()).update(f for f in FRENOS if f in disparadas)
    for ln in corrida.read_text(encoding="utf-8").splitlines():
        m = AVISO_GATE.match(ln)
        if m:
            reglas = {r.strip() for r in m.group(3).split(",")}
            vistos.setdefault((m.group(1), m.group(2)), set()).update(
                f for f in FRENOS if f in reglas
            )
    return {
        clave: (
            sorted(fs),
            "con operaciones del trader"
            if clave in por_sesion
            else "sesion sin operaciones del trader, de «Avisos»",
        )
        for clave, fs in vistos.items()
        if fs
    }


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
