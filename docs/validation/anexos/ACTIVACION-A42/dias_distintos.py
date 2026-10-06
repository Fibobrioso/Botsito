"""Fase 0 e de `trabajo/activacion-a42`: en que dias laborables la ventana de H2b -las velas H4 de
la rejilla de `anclaje_h4` que empiezan en ancla + 8 h y ancla + 12 h- NO es la que el motor
calcula hoy (`reloj_sesiones` = `civil_operativa`: `ventana_inicio`-`ventana_fin` en
`huso_operativa`, que es H2a), ni la de H1 (las mismas horas en Etc/GMT-2). Solo calendario, con
zoneinfo: no lee ningun dato de mercado ni del trader.

La ventana de H2b sale de `limites_del_dia`, la funcion que parte las velas H4 del bot: la tercera
y la cuarta vela del dia de rejilla que abre el ancla de la vispera. Las horas y los husos salen
del registro; Etc/GMT-2 es la hipotesis H1, no un parametro.

    uv run python docs/validation/anexos/ACTIVACION-A42/dias_distintos.py
"""

from __future__ import annotations

import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.agregacion import limites_del_dia  # noqa: E402
from botsito.data.velas import a_datetime  # noqa: E402

MINUTOS_H4 = 240
PRIMERA = 2  # la tercera vela del dia de rejilla: ancla + 8 h
H1 = ZoneInfo("Etc/GMT-2")
ANIOS = (2024, 2025, 2026, 2027)


def tramos(dias: list[date]) -> str:
    """Dias consecutivos (saltando fines de semana) como «AAAA-MM-DD a AAAA-MM-DD (n)»."""
    if not dias:
        return "ninguno"
    grupos: list[list[date]] = [[dias[0]]]
    for d in dias[1:]:
        if (d - grupos[-1][-1]).days <= 3:
            grupos[-1].append(d)
        else:
            grupos.append([d])
    return "; ".join(f"{g[0].isoformat()} a {g[-1].isoformat()} ({len(g)})" for g in grupos)


def main() -> int:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    ancla = registro.hora("anclaje_h4")
    inicio, fin = registro.hora("ventana_inicio"), registro.hora("ventana_fin")
    civil = ZoneInfo(registro.texto("huso_operativa"))
    print(
        f"anclaje_h4 = {ancla}; ventana = {inicio.hora}-{fin.hora}; huso_operativa = {civil.key}; "
        f"reloj_sesiones = {registro.opcion('reloj_sesiones')}"
    )

    def de_pared(dia: date, hora: str, huso: ZoneInfo) -> datetime:
        hh, mm = (int(x) for x in hora.split(":"))
        return datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=huso).astimezone(UTC)

    for anio in ANIOS:
        distintos_h2a: list[date] = []
        distintos_h1: list[date] = []
        horas: set[tuple[str, str]] = set()
        dia = date(anio, 1, 1)
        while dia.year == anio:
            if dia.isoweekday() <= 5:
                limites = limites_del_dia(dia - timedelta(days=1), MINUTOS_H4, ancla)
                h2b = (a_datetime(limites[PRIMERA]), a_datetime(limites[PRIMERA + 2]))
                assert h2b[1] - h2b[0] == timedelta(hours=8), dia
                horas.add((f"{h2b[0]:%H:%M}", f"{h2b[1]:%H:%M}"))
                h2a = (de_pared(dia, inicio.hora, civil), de_pared(dia, fin.hora, civil))
                h1 = (de_pared(dia, inicio.hora, H1), de_pared(dia, fin.hora, H1))
                if h2b != h2a:
                    distintos_h2a.append(dia)
                if h2b != h1:
                    distintos_h1.append(dia)
            dia += timedelta(days=1)
        print()
        print(f"== {anio}: ventanas UTC de H2b que aparecen: {sorted(horas)}")
        print(f"H2b != hoy (civil_operativa, H2a): {len(distintos_h2a)} dias laborables: "
              f"{tramos(distintos_h2a)}")  # fmt: skip
        print(f"H2b != H1 (Etc/GMT-2): {len(distintos_h1)} dias laborables: {tramos(distintos_h1)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
