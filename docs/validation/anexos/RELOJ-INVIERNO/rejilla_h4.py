"""M4 de RELOJ-INVIERNO.md: la rejilla H4 de anclaje_h4 en cuatro semanas, calculada con zoneinfo.

Para cada dia laborable, la hora de apertura de las dos velas H4 de la manana -las que en verano
caen 07-11 y 11-15 en el grafico, es decir, ancla + 8 h y ancla + 12 h- en UTC, Europe/Madrid y
Etc/GMT-2. El ancla es `anclaje_h4` del registro (hora de reloj de pared en su huso, hoy 17:00
America/New_York) del dia ANTERIOR; las velas avanzan 4 h de tiempo absoluto desde el ancla. En
estas semanas ningun dia laborable tiene cambio de hora entre su ancla y sus velas de la manana
(los cambios son en domingo de madrugada), asi que reloj de pared y tiempo absoluto coinciden.

Y al lado, a que hora EMPEZARIA la primera sesion cada dia con cada hipotesis del consultor, en UTC
y en los dos relojes que el trader podria estar leyendo (su grafico y su reloj civil de Madrid):
- H1: `ventana_inicio` (hoy 07:00) en Etc/GMT-2, fija todo el año; grafico = Etc/GMT-2.
- H2a: `ventana_inicio` en Europe/Madrid; grafico = Europe/Madrid.
- H2b: la apertura de la vela ancla + 8 h; grafico = Europe/Madrid.
La hora (07:00) sale del registro; el huso de cada hipotesis es la hipotesis, no un parametro.

    uv run python docs/validation/anexos/RELOJ-INVIERNO/rejilla_h4.py
"""

from __future__ import annotations

import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.config.registro import cargar_registro  # noqa: E402

UTC = ZoneInfo("UTC")
MADRID = ZoneInfo("Europe/Madrid")
FIJO = ZoneInfo("Etc/GMT-2")
# Las semanas del encargo (lunes); la de enero, la del 12 al 16, una cualquiera sin festivo.
SEMANAS = (date(2025, 10, 20), date(2025, 10, 27), date(2025, 11, 3), date(2026, 1, 12))
# Y, como dato, las mismas tres semanas en 2026, que es el cambio del que habla S-7 («desde el 25
# de octubre»): Europa cambia el domingo 25 de octubre y EE. UU. el domingo 1 de noviembre.
SEMANAS_2026 = (date(2026, 10, 19), date(2026, 10, 26), date(2026, 11, 2))
VELA = timedelta(hours=4)
PRIMERA_DE_LA_MANANA = 2  # ancla + 2 velas = ancla + 8 h


def hhmm(instante: datetime, huso: ZoneInfo) -> str:
    return instante.astimezone(huso).strftime("%H:%M")


def main() -> int:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    ancla = registro.hora("anclaje_h4")
    inicio = registro.hora("ventana_inicio")
    huso_ancla = ZoneInfo(ancla.huso)
    h_a, m_a = (int(x) for x in ancla.hora.split(":"))
    h_i, m_i = (int(x) for x in inicio.hora.split(":"))
    print(f"anclaje_h4 = {ancla.hora} {ancla.huso}; ventana_inicio = {inicio.hora} (registro)")
    for titulo, semanas in (("Semanas del encargo", SEMANAS), ("Las mismas en 2026 (dato)", SEMANAS_2026)):
        print()
        print(f"### {titulo}")
        print()
        tabla(semanas, h_a, m_a, huso_ancla, h_i, m_i)
    return 0


def tabla(semanas, h_a, m_a, huso_ancla, h_i, m_i) -> None:
    print("| Dia | Vela 1 UTC | Vela 1 Madrid | Vela 1 Etc/GMT-2 | Vela 2 UTC | Vela 2 Madrid | "
          "Vela 2 Etc/GMT-2 | H1: UTC · grafico · Madrid | H2a: UTC · grafico · Madrid | "
          "H2b: UTC · grafico · Madrid |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for lunes in semanas:
        for k in range(5):
            dia = lunes + timedelta(days=k)
            vispera = dia - timedelta(days=1)
            a = datetime(vispera.year, vispera.month, vispera.day, h_a, m_a, tzinfo=huso_ancla)
            v1 = a + PRIMERA_DE_LA_MANANA * VELA
            v2 = v1 + VELA
            h1 = datetime(dia.year, dia.month, dia.day, h_i, m_i, tzinfo=FIJO)
            h2a = datetime(dia.year, dia.month, dia.day, h_i, m_i, tzinfo=MADRID)
            h2b = v1
            print(
                f"| {dia:%a %Y-%m-%d} | {hhmm(v1, UTC)} | {hhmm(v1, MADRID)} | {hhmm(v1, FIJO)} | "
                f"{hhmm(v2, UTC)} | {hhmm(v2, MADRID)} | {hhmm(v2, FIJO)} | "
                f"{hhmm(h1, UTC)} · {hhmm(h1, FIJO)} · {hhmm(h1, MADRID)} | "
                f"{hhmm(h2a, UTC)} · {hhmm(h2a, MADRID)} · {hhmm(h2a, MADRID)} | "
                f"{hhmm(h2b, UTC)} · {hhmm(h2b, MADRID)} · {hhmm(h2b, MADRID)} |"
            )


if __name__ == "__main__":
    raise SystemExit(main())
