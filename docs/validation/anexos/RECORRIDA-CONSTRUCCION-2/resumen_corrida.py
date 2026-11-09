"""El resumen de una salida del arnes para D5 y D6 de trabajo/recorrida-construccion-2: lo que la
salida imprime repartido por mes y lo que no imprime y se deriva de ella. Solo LEE la salida que
recibe (ninguna vela, ningun tick, ningun caso) y no imprime ningun precio.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/resumen_corrida.py <salida>

Lo DERIVADO, y como (lo demas es recuento de lineas de la salida):
- la equity minima y la peor perdida diaria de CADA cuenta: de la curva de su bloque «### Cuenta de
  AAAA-MM» (o de la «### Curva de equity» de una salida con una sola cuenta), con las MISMAS
  funciones del criterio (`criterio_fidelidad.equity_minima_del_tramo` y `perdida_diaria_maxima`,
  base `saldo_corte_diario`, capital 100000, los del perfil); la salida solo da la peor cuenta;
- RN-032: la salida no tiene una columna propia; se cuentan, en «## Por sesion» (solo las sesiones
  con operaciones del trader), las que llevan RN-032 entre las disparadas y, de ellas, las que
  bloquean `abrir_operacion` (el `prohibida:abrir_operacion` lo dan tambien otras reglas: no mide
  SOLO RN-032, como dijo RECORRIDA-CONSTRUCCION.md §2.2, a4 del revisor).
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from botsito.cases.criterio_fidelidad import (
    BASE_SALDO_CORTE,
    equity_minima_del_tramo,
    perdida_diaria_maxima,
)

CAPITAL = Decimal(100000)
ROTULO = "[DIAGNOSTICO"
POR_SESION = re.compile(
    r"^(\d{4}-\d{2}-\d{2}) (\S+) \| trader \d+ \| bot \d+ \| rn003 \S+ \| (.*) \| disparadas (.*) "
    r"\| bloqueadas (.*)$"
)
CURVA = re.compile(r"^(\d{4}-\d{2}-\d{2}) \| (\S+) \| (\S+) \| (\S+)$")
FRENOS = ("detenido_por_tope", "detenido_por_tope_total", "detenido_por_cartuchos",
          "detenido_por_racha")  # fmt: skip
REGLAS = ("RN-016", "RN-020", "RN-032", "RN-035", "RN-036", "RN-037")


def _cuerpo(ln: str) -> str:
    return ln.split("] ", 1)[1] if ln.startswith(ROTULO) and "] " in ln else ln


def _pct(f: object) -> str:
    return f"{float(f) * 100:.2f} %"  # type: ignore[arg-type]


def _seccion(lineas: list[str], empieza: str) -> list[str]:
    """Las lineas desde la cabecera que empieza por `empieza` hasta la siguiente `#`."""
    for i, ln in enumerate(lineas):
        if ln.startswith(empieza):
            salida = []
            for fila in lineas[i + 1 :]:
                if fila.startswith("#"):
                    break
                salida.append(fila)
            return salida
    return []


def cuentas(lineas: list[str]) -> list[tuple[str, list[str], list[tuple]]]:  # type: ignore[type-arg]
    """(mes o «tramo», lineas del bloque, curva) de cada cuenta."""
    salida = []
    actual: tuple[str, list[str], list[tuple]] | None = None  # type: ignore[type-arg]
    for ln in lineas:
        if ln.startswith("### Cuenta de ") or ln.startswith("### Veredicto de la cuenta"):
            actual = (ln.removeprefix("### Cuenta de ") if "Cuenta de" in ln else "tramo", [], [])
            salida.append(actual)
            continue
        if ln.startswith("### Eventos del broker"):
            break
        if actual is None or ln.startswith("### Curva"):
            continue
        m = CURVA.match(ln)
        if m:
            corte, final, minima = (Decimal(x) if x != "-" else None for x in m.groups()[1:])
            actual[2].append((m.group(1), corte, final, minima))
        elif ln and not ln.startswith("curva de equity"):
            actual[1].append(ln)
    return salida


def main(ruta: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    lineas = [_cuerpo(ln) for ln in ruta.read_text(encoding="utf-8").splitlines()]
    print(f"# Resumen de {ruta.name} (D5 y D6; solo lee la salida)")

    print("\n## Reglas disparadas por sesion (literal, las que D6 nombra)")
    for ln in _seccion(lineas, "## Reglas disparadas por sesion"):
        if ln.startswith(tuple(f"- {r}:" for r in REGLAS)):
            print(ln)
    nombradas = {ln.split(":")[0][2:] for ln in _seccion(lineas, "## Reglas disparadas por sesion")}
    for r in REGLAS:
        if r not in nombradas:
            print(f"- {r}: no sale en la seccion (0 sesiones)")

    print("\n## Por sesion (las sesiones con operaciones del trader), por mes")
    cols = [
        "sesiones", *(f"{f}:si" for f in FRENOS), "RN-032 disparada",
        "RN-032 y prohibida:abrir_operacion", "RN-020 disparada", "RN-036 disparada",
    ]  # fmt: skip
    print("mes | " + " | ".join(cols))
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    dias_032: list[str] = []
    for ln in lineas:
        m = POR_SESION.match(ln)
        if not m:
            continue
        dia, _sesion, hechos, disparadas, bloqueadas = m.groups()
        c = por_mes[dia[:7]]
        c["sesiones"] += 1
        for f in FRENOS:
            c[f"{f}:si"] += f" {f}:si" in f" {hechos}"
        reglas = set(disparadas.split(", "))
        if "RN-032" in reglas:
            c["RN-032 disparada"] += 1
            dias_032.append(dia)
            c["RN-032 y prohibida:abrir_operacion"] += "prohibida:abrir_operacion" in bloqueadas
        c["RN-020 disparada"] += "RN-020" in reglas
        c["RN-036 disparada"] += "RN-036" in reglas
    for mes in sorted(por_mes):
        print(f"{mes} | " + " | ".join(str(por_mes[mes][k]) for k in cols))
    print("RN-032 disparada, primer y ultimo dia por mes: " + (
        "; ".join(
            f"{mes} {min(d for d in dias_032 if d[:7] == mes)} a "
            f"{max(d for d in dias_032 if d[:7] == mes)}"
            for mes in sorted({d[:7] for d in dias_032})
        ) or "ninguno"
    ))  # fmt: skip

    print("\n## Cuentas: lo literal del bloque y lo derivado de su curva")
    for mes, bloque, curva in cuentas(lineas):
        print(f"### {mes}")
        for ln in bloque:
            print(f"  {ln}")
        if curva:
            peor_eq = min(curva, key=lambda d: d[3] if d[3] is not None else min(d[1], d[2]))
            peor_dia = max(
                curva, key=lambda d: d[1] - (d[3] if d[3] is not None else min(d[1], d[2]))
            )
            print(
                f"  DERIVADO: dias en la curva {len(curva)}; equity minima "
                f"{_pct(equity_minima_del_tramo(curva, CAPITAL))} del capital (el {peor_eq[0]}); "
                "peor perdida diaria "
                f"{_pct(perdida_diaria_maxima(curva, CAPITAL, BASE_SALDO_CORTE))}"
                f" del capital (el {peor_dia[0]})"
            )

    print("\n## Ordenes, por mes: resultado y motivo de la cancelacion (su texto hasta el «:»)")
    resultados: dict[str, Counter[str]] = defaultdict(Counter)
    motivos: dict[str, Counter[str]] = defaultdict(Counter)
    for ln in _seccion(lineas, "### Ordenes (dia"):
        campos = ln.split(" | ")
        if len(campos) < 8:
            continue
        resultados[campos[0][:7]][campos[5]] += 1
        if campos[5] != "llenada":
            motivos[campos[0][:7]][f"{campos[5]}: {campos[6].split(':')[0]}"] += 1
    for mes in sorted(resultados):
        print(f"{mes} | " + ", ".join(f"{k} {v}" for k, v in sorted(resultados[mes].items())))
        for k, v in sorted(motivos[mes].items()):
            print(f"  {mes} | {k} | {v}")

    print("\n## Posiciones, por mes: tipo de orden, desenlace, comision y PnL neto (USD)")
    tipos: dict[str, Counter[str]] = defaultdict(Counter)
    desenlaces: dict[str, Counter[str]] = defaultdict(Counter)
    comision: dict[str, Decimal] = defaultdict(Decimal)
    neto: dict[str, Decimal] = defaultdict(Decimal)
    for ln in _seccion(lineas, "### Posiciones (dia"):
        campos = ln.split(" | ")
        if len(campos) != 19:
            continue
        mes = campos[0][:7]
        tipos[mes][campos[5]] += 1
        desenlaces[mes][campos[11]] += 1
        comision[mes] += Decimal(campos[14])
        neto[mes] += Decimal(campos[16])
    for mes in sorted(tipos):
        print(
            f"{mes} | posiciones {sum(tipos[mes].values())} | tipo "
            + ", ".join(f"{k} {v}" for k, v in sorted(tipos[mes].items()))
            + " | desenlace "
            + ", ".join(f"{k} {v}" for k, v in sorted(desenlaces[mes].items()))
            + f" | comision {comision[mes]:.2f} | PnL neto {neto[mes]:.2f}"
        )

    print("\n## Eventos del broker, por mes: tipo y fuente")
    eventos: dict[str, Counter[str]] = defaultdict(Counter)
    for ln in _seccion(lineas, "### Eventos del broker"):
        campos = ln.split(" | ")
        if len(campos) == 5:
            eventos[campos[0][:7]][f"{campos[2]}/{campos[4]}"] += 1
    for mes in sorted(eventos):
        print(f"{mes} | " + ", ".join(f"{k} {v}" for k, v in sorted(eventos[mes].items())))

    print("\n## Peticiones al servidor, por mes: total y maximo diario")
    pet: dict[str, list[int]] = defaultdict(list)
    for ln in _seccion(lineas, "### Peticiones al servidor"):
        campos = ln.split(" | ")
        if len(campos) == 7 and re.match(r"^\d{4}-\d{2}-\d{2}$", campos[0]):
            pet[campos[0][:7]].append(int(campos[1]))
    for mes in sorted(pet):
        print(f"{mes} | dias {len(pet[mes])} | total {sum(pet[mes])} | maximo {max(pet[mes])}")
    print(f"total | {sum(sum(v) for v in pet.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
