"""Las nueve sesiones del visor (respuesta del consultor a la PARADA 2 de
trabajo/recorrida-construccion-2, punto 3): lo que las paginas de `data/visor/` (ignoradas por git;
las escriben los nueve `motor visor --simular --caso` del punto 3) dicen de cada sesion, contado, y
comparado con la corrida 1 (`cuenta-por-mes.txt`). Solo LEE esas paginas y la salida; no corre nada.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/visor_sesiones.py \\
        data/visor docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt

Por sesion:
- (a) las ordenes del visor frente a las de la corrida 1 de ese dia: id, colocacion (la del visor va
  en hora de pared, Europe/Madrid; la de la salida, en UTC, y se convierte), precio, stop (el de la
  salida, desde su precio y su distancia) y estado;
- (b) el sesgo que anota el motor (su linea literal: lado, H4 miradas, ruptura y la H4 que abre la
  decision, por su hora de apertura) y el color de esa H4 en el grafico (clase `sube`/`baja` del
  rectangulo marcado «rompe esta H4»), sin precios;
- la primera `liquidez_tomada=si` de RN-004 en la sesion, y si vuelve a `no` dentro de ella;
- (d) S-10: cada orden con la zona de la que nace (la zona del mismo lado y la misma entrada cuyo
  cierre de formacion es el de la colocacion: la orden se coloca en el cierre en que la zona se
  forma, 1 ms antes de su minuto) y si esa zona es la PRIMERA formada en la sesion desde la primera
  toma. LIMITE, declarado: el visor no nombra las tomas ni los escenarios (RN-004 se fija «si» en
  cada cierre), asi que «la toma» es aqui la primera de la sesion; una toma nueva dentro de ella no
  se ve;
- (c) por cada operacion del trader de la sesion: la zona del bot del mismo lado mas cercana en
  entrada formada antes de su instante, a cuantos puntos, y si alguna orden nacio de ella y que fue.

Lo que imprime son horas de pared del dia del caso, ids, recuentos y distancias en puntos: ningun
precio, nivel ni instante de un dia anterior.
"""

# ruff: noqa: E501  (textos y tablas literales: el docstring explica las columnas)

from __future__ import annotations

import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
from salida_comun import cierre as _cierre  # noqa: E402  (sin para_clasificar: la guardia)
from salida_comun import ordenes_de  # noqa: E402

PARED = ZoneInfo("Europe/Madrid")
ESCALA = 100_000
SESIONES = {
    "2026-07-06": ("07-11",),
    "2026-07-07": ("07-11", "11-15"),
    "2026-07-15": ("11-15",),
    "2026-01-22": ("11-15",),
    "2026-07-02": ("11-15",),
    "2026-04-13": ("07-11",),
    "2026-01-13": ("07-11",),
    "2026-04-15": ("11-15",),
    "2026-07-14": ("11-15",),
}
PATRON = {
    ("2026-07-06", "07-11"): "P1",
    ("2026-07-07", "07-11"): "P1",
    ("2026-07-07", "11-15"): "P1",
    ("2026-07-15", "11-15"): "P1",
    ("2026-01-22", "11-15"): "P1",
    ("2026-07-02", "11-15"): "P3",
    ("2026-04-13", "07-11"): "P3",
    ("2026-01-13", "07-11"): "P5",
    ("2026-04-15", "11-15"): "P6",
    ("2026-07-14", "11-15"): "P2 (la caja)",
}
SESION = re.compile(r"^Sesion (\d\d-\d\d) \((\d\d:\d\d)-(\d\d:\d\d)\)$")


class _Texto(HTMLParser):
    """El texto de la pagina (sin SVG ni scripts), una linea por fila o parrafo, y del SVG de H4
    solo los rectangulos: su clase y su x, y los marcados «decide» con su titulo."""

    def __init__(self) -> None:
        super().__init__()
        self.lineas: list[str] = []
        self.actual: list[str] = []
        self.fuera = 0
        self.en_h4 = False
        self.velas_h4: list[tuple[float, str]] = []
        self.decide: list[tuple[float, float, str]] = []
        self._decide: tuple[float, float] | None = None
        self._titulo = False

    def handle_starttag(self, tag, attrs):  # type: ignore[no-untyped-def]
        a = dict(attrs)
        if tag == "svg" and a.get("class") == "h4":
            self.en_h4 = True
        if self.en_h4 and tag == "rect":
            if a.get("class") in ("sube", "baja", "neutra"):
                self.velas_h4.append((float(a["x"]), a["class"]))
            elif a.get("class") == "decide":
                self._decide = (float(a["x"]), float(a["width"]))
        if self.en_h4 and tag == "title" and self._decide is not None:
            self._titulo = True
        if tag in ("svg", "script", "style"):
            self.fuera += 1
        if tag in ("tr", "p", "li", "h1", "h2", "h3", "div", "br"):
            self._cerrar()
        if tag in ("td", "th"):
            self.actual.append(" | ")

    def handle_endtag(self, tag):  # type: ignore[no-untyped-def]
        if tag == "svg" and self.en_h4:
            self.en_h4 = False
        if tag in ("svg", "script", "style"):
            self.fuera -= 1
        if tag in ("tr", "p", "li", "h1", "h2", "h3"):
            self._cerrar()
        if tag == "title":
            self._titulo = False

    def handle_data(self, data):  # type: ignore[no-untyped-def]
        if self._titulo and self._decide is not None:
            self.decide.append((*self._decide, data))
            self._decide = None
        if not self.fuera:
            self.actual.append(data)

    def _cerrar(self) -> None:
        t = " ".join("".join(self.actual).split())
        if t:
            self.lineas.append(t)
        self.actual = []


@dataclass(frozen=True)
class OrdenVisor:
    id: str
    lado: str
    precio: Decimal
    stop: Decimal
    estado: str
    colocada: str  # hh:mm:ss de pared


@dataclass(frozen=True)
class Zona:
    id: str
    lado: str
    entrada: Decimal
    desde: str
    formada: str  # hh:mm:ss de pared, el cierre en que se forma


def _celdas(ln: str) -> list[str]:
    return [c.strip() for c in ln.strip("| ").split(" | ")]


def _tabla(lineas: list[str], titulo: str) -> list[list[str]]:
    try:
        i = lineas.index(titulo)
    except ValueError:
        return []
    filas = []
    for ln in lineas[i + 2 :]:
        if not ln.startswith("| "):
            break
        filas.append(_celdas(ln))
    return filas


def leer_pagina(ruta: Path) -> tuple[list[str], _Texto]:
    p = _Texto()
    p.feed(ruta.read_text(encoding="utf-8"))
    p._cerrar()
    return p.lineas, p


def bloques_de_sesion(lineas: list[str]) -> dict[str, list[str]]:
    salida: dict[str, list[str]] = {}
    actual: str | None = None
    for ln in lineas:
        m = SESION.match(ln)
        if m:
            actual = m.group(1)
            salida[actual] = []
            continue
        if ln == "Operaciones":
            actual = None
        if actual is not None:
            salida[actual].append(ln)
    return salida


def pared(iso_utc: str) -> str:
    return datetime.fromisoformat(iso_utc).astimezone(PARED).strftime("%H:%M:%S")


def color_de_la_h4(p: _Texto, sesion: str) -> str:
    for x, ancho, titulo in p.decide:
        if titulo.startswith(f"{sesion}:"):
            dentro = [c for vx, c in p.velas_h4 if x - 1 <= vx <= x + ancho]
            return dentro[0] if dentro else "sin vela en el grafico"
    return "sin marca en el grafico"


ABRE = re.compile(r"abre a las (\d\d:\d\d)")


def antes_del_dia(linea: str, inicio_sesion: str) -> str:
    """La regla «(antes del dia)» de `anexos/VISOR-CONSTRUCCION/comun_visor.py`: la H4 que el motor
    nombra por su hora de apertura es de un dia anterior si abre a la hora de inicio de la sesion o
    despues (una H4 cerrada antes de abrir la sesion que abre mas tarde en el reloj es de la
    vispera); entonces la hora no se escribe."""

    def tapa(m: re.Match[str]) -> str:
        return "abre un dia anterior" if f"{m.group(1)}:00" >= inicio_sesion else m.group(0)

    return ABRE.sub(tapa, linea)


def _segundos(hhmmss: str) -> int:
    h, m, s = (int(x) for x in hhmmss.split(":"))
    return h * 3600 + m * 60 + s


def main(visor: Path, corrida: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    texto = corrida.read_text(encoding="utf-8")
    todas = ordenes_de(texto)
    print("# Las nueve sesiones del visor (respuesta a la PARADA 2, punto 3); horas de pared")
    for dia, sesiones in SESIONES.items():
        lineas, p = leer_pagina(visor / f"caso-eurusd-{dia}.html")
        bloques = bloques_de_sesion(lineas)
        ordenes_v = [
            OrdenVisor(c[0], c[1], Decimal(c[2]), Decimal(c[4]), c[6], c[7])
            for c in _tabla(lineas, "Ordenes")
        ]
        zonas = [
            Zona(c[0], c[1], Decimal(c[3]), c[5], c[6])
            for c in _tabla(lineas, "Zonas de entrada ligadas por el motor")
        ]
        trader = [c for c in _tabla(lineas, "Operaciones") if c[0] == "trader"]
        ordenes_c = [o for o in todas.values() if o.dia == dia]
        # (a) visor frente a corrida 1, el dia entero
        print(f"\n## {dia}")
        dif = []
        por_id_c = {o.id: o for o in ordenes_c}
        for ov in ordenes_v:
            oc = por_id_c.get(ov.id)
            if oc is None:
                dif.append(f"{ov.id}: en el visor y no en la corrida 1")
                continue
            stop_c = oc.stop
            estado_c = {"llenada": "llenada", "rechazada": "rechazada"}.get(
                oc.resultado, "cancelada"
            )
            campos = []
            if pared(oc.colocada) != ov.colocada:
                campos.append("colocacion")
            if oc.precio != ov.precio:
                campos.append(f"precio ({int((ov.precio - oc.precio) * ESCALA):+d} puntos)")
            if stop_c is None:
                campos.append("stop (la orden de la corrida sin direccion legible)")
            elif stop_c != ov.stop:
                campos.append(f"stop ({int((ov.stop - stop_c) * ESCALA):+d} puntos)")
            if estado_c != ov.estado:
                campos.append(f"estado (visor {ov.estado}, corrida {oc.resultado})")
            if campos:
                dif.append(f"{ov.id}: {', '.join(campos)}")
        for oc in ordenes_c:
            if oc.id not in {o.id for o in ordenes_v}:
                dif.append(f"{oc.id}: en la corrida 1 y no en el visor")
        print(
            f"(a) ordenes del dia: visor {len(ordenes_v)}, corrida 1 {len(ordenes_c)}; "
            + ("IGUALES en id, colocacion, precio, stop y estado" if not dif else "DIFERENCIAS:")
        )
        for d in dif[:12]:
            print(f"    {d}")
        if len(dif) > 12:
            print(f"    ... y {len(dif) - 12} mas")
        for sesion in sesiones:
            bloque = bloques.get(sesion, [])
            ini_s, fin_s = {
                "07-11": ("07:00:00", "11:00:00"),
                "11-15": ("11:00:00", "15:00:00"),
            }[sesion]
            sesgo = antes_del_dia(
                next((ln for ln in bloque if ln.startswith("Sesgo anotado")), "-"), ini_s
            )
            tomas = [
                _celdas(ln)[0] for ln in bloque
                if ln.startswith("| ") and "| RN-004 | liquidez_tomada |" in ln
            ]  # fmt: skip
            valores = [
                _celdas(ln)[3] for ln in bloque
                if ln.startswith("| ") and "| RN-004 | liquidez_tomada |" in ln
            ]  # fmt: skip
            primera = next((t for t, v in zip(tomas, valores, strict=True) if v == "si"), None)
            vuelve_a_no = primera is not None and "no" in valores[valores.index("si") :]
            bloqueadas = next((ln for ln in bloque if ln.startswith("Acciones bloqueadas")), "-")
            print(f"\n### {dia} {sesion} · {PATRON[(dia, sesion)]}")
            print(f"(b) {sesgo}")
            print(f"    color de la H4 que decide, en el grafico: {color_de_la_h4(p, sesion)}")
            print(
                f"    primera liquidez_tomada=si (RN-004): {primera or 'ninguna'}; vuelve a «no» "
                f"dentro de la sesion: {'si' if vuelve_a_no else 'no'}; {bloqueadas}"
            )
            zs = sorted((z for z in zonas if ini_s <= z.formada < fin_s), key=lambda z: z.formada)
            desde_toma = [z for z in zs if primera is not None and z.formada >= primera + ":00"]
            # la orden es de la sesion por el CIERRE en que se coloca (1 s despues de su hora,
            # que acaba en :59), como `cableado._sesion_de`
            os_ = [o for o in ordenes_v if ini_s <= _cierre(o.colocada) < fin_s]
            print(
                f"    zonas formadas en la sesion: {len(zs)} ("
                + ", ".join(f"{k} {v}" for k, v in sorted(Counter(z.lado for z in zs).items()))
                + f"); ordenes: {len(os_)} ("
                + ", ".join(f"{k} {v}" for k, v in sorted(Counter(o.estado for o in os_).items()))
                + ")"
            )
            # (d) S-10
            print("(d) S-10, orden por orden: zona de la que nace · ¿la primera desde la toma?")
            for o in os_:
                cierre = _cierre(o.colocada)
                z = next(
                    (z for z in zs if z.lado == o.lado and z.entrada == o.precio and z.formada == cierre),
                    None,
                )  # fmt: skip
                if z is None:
                    nace = "sin zona formada en su cierre (recolocada sobre una zona anterior)"
                    primera_z = "-"
                else:
                    nace = f"{z.id} (bloque desde {z.desde}, formada {z.formada})"
                    primera_z = "si" if desde_toma and desde_toma[0].id == z.id else "no"
                print(
                    f"    {o.id} {o.lado} {o.estado} colocada {o.colocada}: {nace} · primera: {primera_z}"
                )
            # (c) por operacion del trader
            ts = [t for t in trader if t[1] == sesion]
            print(f"(c) operaciones del trader en la sesion: {len(ts)}")
            for t in ts:
                lado, llenado, entrada = t[2], t[3], Decimal(t[4])
                # solo las zonas de la sesion: la memoria de zonas es por sesion (zonas.py)
                antes = [z for z in zs if z.lado == lado and z.formada <= llenado]
                if not antes:
                    print(
                        f"    trader {lado} {llenado}: ninguna zona del bot de su lado formada "
                        "antes en la sesion"
                    )
                    continue
                z = min(antes, key=lambda z: (abs(z.entrada - entrada), -_segundos(z.formada)))
                nacidas = [
                    o for o in ordenes_v
                    if o.lado == lado and o.precio == z.entrada and o.colocada < llenado
                ]  # fmt: skip
                print(
                    f"    trader {lado} {llenado}: zona mas cercana {z.id} formada {z.formada}, a "
                    f"{int(abs(z.entrada - entrada) * ESCALA)} puntos; ordenes en esa entrada antes: "
                    + (", ".join(f"{o.id} {o.estado} {o.colocada}" for o in nacidas) or "ninguna")
                )
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
