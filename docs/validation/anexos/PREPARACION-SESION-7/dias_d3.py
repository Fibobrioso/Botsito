"""0.4 de trabajo/preparacion-sesion-7: D3 a) a c) sesion a sesion, por la compuerta.

Uso (desde la raiz del repo): uv run python dias_d3.py
a) el dia es dev de un mes de construccion (criterio_fidelidad.yaml `construccion`; visto: los
   laborables de los tramos de `cobertura_material`) y no esta en casos_ocultos ni en
   casos_reservados (se cuenta, no se imprime ningun id);
b) el dia de mercado anterior (el laborable anterior, el mismo calendario que visto._laborables)
   tambien es dev de construccion y no oculto;
c) ninguna hora perdida dentro de la sesion (las 18 de anexos/RESPALDO-M1/horas_perdidas.py, con
   la ventana de la sesion en Europe/Madrid) y ninguna fila «posible M» de la sesion en
   patrones-cuenta-por-mes.txt.
Ademas, la condicion b) sobre TODOS los dias dev de construccion: que dias excluye.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.cases import visto
from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.holdout import casos_ocultos, casos_reservados

REPO = Path(".")
MADRID = ZoneInfo("Europe/Madrid")
SESIONES = {"07-11": (7, 11), "11-15": (11, 15)}
PATRONES = REPO / "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt"

CANDIDATAS = {
    "rango H4": ["2026-07-06 07-11", "2026-07-06 11-15", "2026-07-07 07-11", "2026-07-07 11-15",
                 "2026-07-15 11-15", "2026-07-17 11-15"],
    "zonas de control": ["2026-04-13 07-11", "2026-07-02 11-15", "2026-07-03 11-15"],
    "colocacion": ["2026-07-03 07-11"],
    "7b F3.5": ["2026-07-02 11-15", "2026-01-02 11-15", "2026-07-10 07-11", "2026-01-22 11-15",
                "2026-01-13 07-11", "2026-04-15 11-15"],
    "excluidas por el encargo (control)": ["2026-07-14 11-15", "2026-07-17 07-11",
                                           "2026-07-01 07-11", "2026-04-01 11-15"],
}  # fmt: skip


def horas_perdidas() -> tuple[str, ...]:
    ruta = REPO / "docs/validation/anexos/RESPALDO-M1/horas_perdidas.py"
    spec = importlib.util.spec_from_file_location("horas_perdidas_anexo", ruta)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.HORAS_PERDIDAS)


def ventana_utc(dia: str, sesion: str) -> tuple[datetime, datetime]:
    a, b = SESIONES[sesion]
    d = date.fromisoformat(dia)
    ini = datetime(d.year, d.month, d.day, a, tzinfo=MADRID).astimezone(ZoneInfo("UTC"))
    fin = datetime(d.year, d.month, d.day, b, tzinfo=MADRID).astimezone(ZoneInfo("UTC"))
    return ini, fin


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    criterio = cargar_criterio(REPO)
    ocultos = casos_ocultos(REPO)
    reservados = casos_reservados(REPO)
    dev: set[str] = set()
    for mes in criterio.construccion:
        for caso, part in visto.asignacion(REPO, mes).items():
            if part == "dev":
                m = re.search(r"(\d{4}-\d{2}-\d{2})$", caso)
                assert m
                dev.add(m.group(1))
    oc_dias = {m.group(1) for c in ocultos if (m := re.search(r"(\d{4}-\d{2}-\d{2})", c))}
    re_dias = {m.group(1) for c in reservados if (m := re.search(r"(\d{4}-\d{2}-\d{2})", c))}
    print(f"construccion: {criterio.construccion}; dias dev: {len(dev)}")
    print(f"casos_ocultos: {len(ocultos)}; casos_reservados: {len(reservados)}")
    print(f"dias dev que estan en ocultos: {len(dev & oc_dias)}; en reservados: {len(dev & re_dias)}")
    por_mes: dict[str, list[str]] = {}
    for d in sorted(dev):
        por_mes.setdefault(d[:7], []).append(d)
    for mes, ds in por_mes.items():
        print(f"  {mes}: {len(ds)} dias dev, del {ds[0]} al {ds[-1]}")

    def bueno(d: str) -> bool:
        return d in dev and d not in oc_dias and d not in re_dias

    def anterior(d: str) -> str:
        x = date.fromisoformat(d) - timedelta(days=1)
        while x.weekday() >= 5:
            x -= timedelta(days=1)
        return x.isoformat()

    excl_b = [d for d in sorted(dev) if not bueno(anterior(d))]
    print(f"condicion b) sobre los {len(dev)} dias dev: excluye {excl_b}")

    hp = horas_perdidas()
    posible_m: dict[tuple[str, str], int] = {}
    fila = re.compile(r"posible M[^\]]*\]: (?:trader|bot) \| (\d{4}-\d{2}-\d{2}) \| (\S+) \|")
    for ln in PATRONES.read_text(encoding="utf-8").splitlines():
        m = fila.search(ln)
        if m:
            posible_m[(m.group(1), m.group(2))] = posible_m.get((m.group(1), m.group(2)), 0) + 1
    print(f"filas posible M: {sum(posible_m.values())} en {len(posible_m)} sesiones")

    for grupo, sesiones in CANDIDATAS.items():
        print(f"\n## {grupo}")
        pasan = 0
        for s in sesiones:
            dia, ses = s.split()
            a = bueno(dia)
            ant = anterior(dia)
            b = bueno(ant)
            ini, fin = ventana_utc(dia, ses)
            dentro = []
            for h in hp:
                hi = datetime.strptime(h, "%Y-%m-%dT%HZ").replace(tzinfo=ZoneInfo("UTC"))
                if hi < fin and hi + timedelta(hours=1) > ini:
                    dentro.append(h)
            pm = posible_m.get((dia, ses), 0)
            c = not dentro and pm == 0
            ok = a and b and c
            pasan += ok
            print(
                f"{s}: a) {'si' if a else 'NO'}; b) anterior "
                f"{ant + ' si' if b else 'NO (no es de construccion; sin la fecha)'}; "
                f"c) horas perdidas dentro {dentro or 'ninguna'}, posible M {pm} -> "
                f"{'PASA' if ok else 'NO PASA'}"
            )
        print(f"pasan {pasan} de {len(sesiones)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
