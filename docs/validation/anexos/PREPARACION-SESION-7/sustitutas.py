"""D3 d) de trabajo/preparacion-sesion-7: las sustitutas de la lista de dias de la sesion 7 de
RECORRIDA-CONSTRUCCION-2 F3.5, sobre anexos/RECORRIDA-CONSTRUCCION-2/caja-stop.txt y
para-clasificar.txt.

Uso (desde la raiz del repo): uv run python sustitutas.py <caja-stop.txt> <para-clasificar.txt>

Por grupo de la caja (stop fuera; P2 a 4-10 puntos), las filas ordenadas por cociente, de mayor a
menor y de menor a mayor, con D3 a) a c) por sesion:
a) dia dev de un mes de construccion (visto: laborables de cobertura_material), fuera de
   casos_ocultos y de casos_reservados;
b) el laborable anterior tambien lo es;
c) ninguna hora perdida dentro de la sesion (las 18 de anexos/RESPALDO-M1/horas_perdidas.py) y
   ninguna operacion del trader de la sesion con «posible M» en la columna «hora perdida» de
   para-clasificar.txt (y ninguna fila «posible M» de patrones-cuenta-por-mes.txt).
No imprime ningun id de casos ocultos: solo recuentos.
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
UTC = ZoneInfo("UTC")
SESIONES = {"07-11": (7, 11), "11-15": (11, 15)}
PATRONES = REPO / "docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/patrones-cuenta-por-mes.txt"
HORAS = REPO / "docs/validation/anexos/RESPALDO-M1/horas_perdidas.py"


def _horas() -> tuple[str, ...]:
    spec = importlib.util.spec_from_file_location("horas_perdidas_anexo", HORAS)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return tuple(mod.HORAS_PERDIDAS)


def _dia(caso: str) -> str | None:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", caso)
    return m.group(1) if m else None


def main(caja: Path, para: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    criterio = cargar_criterio(REPO)
    dev = {
        d
        for mes in criterio.construccion
        for c, p in visto.asignacion(REPO, mes).items()
        if p == "dev" and (d := _dia(c))
    }
    vetados = {d for c in casos_ocultos(REPO) if (d := _dia(c))} | {
        d for c in casos_reservados(REPO) if (d := _dia(c))
    }
    print(f"dias dev de construccion: {len(dev)}; de ellos vetados: {len(dev & vetados)}")
    horas = _horas()

    marcadas: set[tuple[str, str]] = set()
    en_tabla = False
    for ln in para.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            en_tabla = ln.startswith("## Operaciones del trader")
            continue
        if en_tabla and ln.startswith("2026-"):
            cols = [c.strip() for c in ln.split("|")]
            if cols[-1].startswith("posible M"):
                marcadas.add((cols[0], cols[1]))
    fila = re.compile(r"posible M[^\]]*\]: (?:trader|bot) \| (\d{4}-\d{2}-\d{2}) \| (\S+) \|")
    for ln in PATRONES.read_text(encoding="utf-8").splitlines():
        if m := fila.search(ln):
            marcadas.add((m.group(1), m.group(2)))
    print(f"sesiones con alguna fila «posible M»: {len(marcadas)}")

    def bueno(d: str) -> bool:
        return d in dev and d not in vetados

    def anterior(d: str) -> str:
        x = date.fromisoformat(d) - timedelta(days=1)
        while x.weekday() >= 5:
            x -= timedelta(days=1)
        return x.isoformat()

    def motivo(dia: str, ses: str) -> str:
        if not bueno(dia):
            return "NO a)"
        if not bueno(anterior(dia)):
            return "NO b) (el dia de mercado anterior no es de construccion; sin la fecha)"
        a, b = SESIONES[ses]
        d = date.fromisoformat(dia)
        ini = datetime(d.year, d.month, d.day, a, tzinfo=MADRID).astimezone(UTC)
        fin = datetime(d.year, d.month, d.day, b, tzinfo=MADRID).astimezone(UTC)
        dentro = [
            h for h in horas
            if (hi := datetime.strptime(h, "%Y-%m-%dT%HZ").replace(tzinfo=UTC)) < fin
            and hi + timedelta(hours=1) > ini
        ]  # fmt: skip
        if dentro:
            return f"NO c) (hora perdida {', '.join(dentro)})"
        if (dia, ses) in marcadas:
            return "NO c) (posible M)"
        return "cumple"

    grupos: dict[str, list[tuple[float, str, str, str, str]]] = {"stop fuera": [], "P2 4-10": []}
    seccion = ""
    for ln in caja.read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            seccion = ln
            continue
        if not ln.startswith("2026-"):
            continue
        cols = [c.strip() for c in ln.split("|")]
        if seccion.startswith("## 1.") and cols[12] == "stop fuera":
            grupos["stop fuera"].append((float(cols[11]), cols[0], cols[1], cols[2], cols[3]))
        elif seccion.startswith("## 2.") and cols[12] == "4-10 puntos":
            grupos["P2 4-10"].append((float(cols[11]), cols[0], cols[1], cols[2], cols[3]))
    for nombre, filas in grupos.items():
        print(f"\n## {nombre}: {len(filas)} filas")
        for titulo, orden in (("de mayor a menor", True), ("de menor a mayor", False)):
            print(f"### {titulo} (las diez primeras)")
            for coc, dia, ses, lado, inst in sorted(filas, key=lambda f: (f[0], f[4]), reverse=orden)[:10]:
                print(f"{coc:5.2f} | {dia} {ses} | {lado} {inst[11:19]}Z | {motivo(dia, ses)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
