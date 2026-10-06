"""Fase 0 d de `trabajo/activacion-a42`: el guion de M4 (`anexos/RELOJ-INVIERNO/rejilla_h4.py`, tal
cual, sin tocarlo) repetido sobre las dos semanas de 2024 de las capturas b y c del trader
(RELOJ-INVIERNO.md §12): anclas del domingo 27 al jueves 31 de octubre y del domingo 3 al jueves 7
de noviembre de 2024. En 2024 Europa cambio la hora el domingo 27 de octubre y EE. UU. el domingo 3
de noviembre.

Dos tablas por semana, las dos con zoneinfo y con `anclaje_h4` leido del registro:

1. LO QUE ENSENA EL EJE: a que hora de reloj cae el ancla de cada dia -el limite de la vela diaria
   y de la primera H4- y los seis limites H4 de ese dia de rejilla, en Europe/Madrid y en
   Etc/GMT-2. Los limites salen de `limites_del_dia`, la funcion que parte las velas del bot.
2. La tabla de M4 (`tabla`, importada del anexo de RELOJ-INVIERNO) para las sesiones de los cinco
   dias que abren esas anclas (lunes a viernes).

    uv run python docs/validation/anexos/ACTIVACION-A42/rejilla_h4_2024.py
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import date, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.data.agregacion import limites_del_dia  # noqa: E402
from botsito.data.velas import a_datetime  # noqa: E402

M4 = RAIZ / "docs/validation/anexos/RELOJ-INVIERNO/rejilla_h4.py"
MADRID = ZoneInfo("Europe/Madrid")
FIJO = ZoneInfo("Etc/GMT-2")
# El domingo que abre cada semana de las capturas (el eje de b va de «dom 27 Oct '24» a «jue 31
# Oct '24»; el de c, de «dom 03 Nov '24» a «jue 07 Nov '24»: lectura del consultor, §12).
DOMINGOS = (date(2024, 10, 27), date(2024, 11, 3))
MINUTOS_H4 = 240
DIAS = ("lun", "mar", "mie", "jue", "vie", "sab", "dom")


def cargar_m4():
    spec = importlib.util.spec_from_file_location("rejilla_h4_m4", M4)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main() -> int:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    ancla = registro.hora("anclaje_h4")
    inicio = registro.hora("ventana_inicio")
    m4 = cargar_m4()
    h_a, m_a = (int(x) for x in ancla.hora.split(":"))
    h_i, m_i = (int(x) for x in inicio.hora.split(":"))
    print(f"anclaje_h4 = {ancla.hora} {ancla.huso}; ventana_inicio = {inicio.hora} (registro)")
    for domingo in DOMINGOS:
        print()
        print(f"### Semana del ancla del domingo {domingo.isoformat()}")
        print()
        print("| Ancla (dia de rejilla) | UTC | en un eje Europe/Madrid | en un eje Etc/GMT-2 | "
              "limites H4 del dia, Europe/Madrid | limites H4 del dia, Etc/GMT-2 |")  # fmt: skip
        print("|---|---|---|---|---|---|")
        for k in range(5):
            dia = domingo + timedelta(days=k)
            limites = [a_datetime(x) for x in limites_del_dia(dia, MINUTOS_H4, ancla)]
            a = limites[0]

            def eje(huso: ZoneInfo, a=a) -> str:
                local = a.astimezone(huso)
                return f"{DIAS[local.weekday()]} {local:%d-%m} {local:%H:%M}"

            def horas(huso: ZoneInfo, limites=limites) -> str:
                return " ".join(f"{x.astimezone(huso):%H:%M}" for x in limites)

            print(
                f"| {DIAS[dia.weekday()]} {dia.isoformat()} | {a:%Y-%m-%d %H:%M} | {eje(MADRID)} "
                f"| {eje(FIJO)} | {horas(MADRID)} | {horas(FIJO)} |"
            )
        print()
        print("La tabla de M4 para las sesiones que abren esas anclas (lunes a viernes):")
        print()
        m4.tabla((domingo + timedelta(days=1),), h_a, m_a, ZoneInfo(ancla.huso), h_i, m_i)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
