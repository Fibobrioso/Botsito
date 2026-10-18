"""VISOR-CONSTRUCCION (R3.2), respuesta del consultor a la PARADA, punto 2: de una pagina del visor,
solo lo del dia dev, para que la sesion NO abra el HTML entero.

Imprime los encabezados, los parrafos y las tablas de la pagina en texto, y deja fuera:
- todo `<svg>`: el grafico de precio (M1/M15 desde las 00:00 del trader, el dia UTC anterior),
  la calle de hechos y el grafico de H4 de contexto;
- el parentesis del sesgo de cada sesion («(domain/sesgo.py: …, rompe la H4 que abre a …)»),
  que nombra una H4 que puede ser de un dia anterior;
- lo que sigue a «saldo al cierre» en el resumen del broker (saldo y equity: dinero);
- toda fila de tabla, y toda hora suelta en un parrafo, anterior a las 00:00Z de la fecha del caso:
  las horas de la pagina son del reloj del trader (Europe/Madrid) y se convierten a UTC con el
  desfase de ese dia (respuesta del consultor, punto 5).
No escribe nada: imprime.

    uv run python docs/validation/anexos/VISOR-CONSTRUCCION/extraer_pagina.py <pagina.html>
"""

from __future__ import annotations

import re
import sys
from datetime import UTC, date, datetime, time
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

HUSO_TRADER = ZoneInfo("Europe/Madrid")
HORA = re.compile(r"\b(\d{2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?\b")
FECHA_EN_NOMBRE = re.compile(r"caso-eurusd-(\d{4}-\d{2}-\d{2})")
OCULTO = "(antes del dia)"
SESGO = re.compile(r"\s*\(domain/sesgo\.py:[^)]*\)")
BLOQUES = ("h1", "h2", "h3", "h4", "p", "li", "caption")


class Extractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.dentro_svg = 0
        self.bloque: list[str] | None = None
        self.etiqueta = ""
        self.fila: list[str] | None = None
        self.celda: list[str] | None = None
        self.salida: list[tuple[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "svg":
            self.dentro_svg += 1
            return
        if self.dentro_svg:
            return
        if tag in BLOQUES:
            self.bloque, self.etiqueta = [], tag
        elif tag == "tr":
            self.fila = []
        elif tag in ("td", "th"):
            self.celda = []
        elif tag == "br" and self.bloque is not None:
            self.bloque.append(" | ")

    def handle_endtag(self, tag: str) -> None:
        if tag == "svg":
            self.dentro_svg -= 1
            return
        if self.dentro_svg:
            return
        if tag in BLOQUES and self.bloque is not None:
            texto = " ".join("".join(self.bloque).split())
            if texto:
                self.salida.append((self.etiqueta, texto))
            self.bloque = None
        elif tag in ("td", "th") and self.celda is not None and self.fila is not None:
            self.fila.append(" ".join("".join(self.celda).split()))
            self.celda = None
        elif tag == "tr" and self.fila is not None:
            self.salida.append(("tr", self.fila))
            self.fila = None

    def handle_data(self, data: str) -> None:
        if self.dentro_svg:
            return
        if self.celda is not None:
            self.celda.append(data)
        elif self.bloque is not None:
            self.bloque.append(data)


def _antes_del_dia(hh: int, mm: int, ss: int, fecha: date) -> bool:
    """Una hora del reloj del trader en el dia del caso, ¿es anterior a las 00:00Z de esa fecha?"""
    local = datetime.combine(fecha, time(hh, mm, ss), tzinfo=HUSO_TRADER)
    return local.astimezone(UTC).date() < fecha


def _enmascarar_horas(texto: str, fecha: date) -> str:
    def cambio(m: re.Match[str]) -> str:
        hh, mm, ss = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
        if hh > 23 or mm > 59:
            return m.group(0)
        return OCULTO if _antes_del_dia(hh, mm, ss, fecha) else m.group(0)

    return HORA.sub(cambio, texto)


def main(ruta: Path, sin_hechos: bool = False) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    m = FECHA_EN_NOMBRE.search(ruta.name)
    if m is None:
        print("ERROR: el nombre de la pagina no lleva la fecha del caso")
        return 2
    fecha = date.fromisoformat(m.group(1))
    e = Extractor()
    e.feed(ruta.read_text(encoding="utf-8"))
    print(
        f"PAGINA {ruta.name} · sin graficos, sin el parentesis del sesgo, sin saldo ni equity, sin"
    )
    print("nada anterior a las 00:00Z de la fecha del caso")
    saltando = False
    omitidas = 0
    for etiqueta, contenido in e.salida:
        if etiqueta != "tr" and saltando:
            print(
                f"  | ({omitidas} filas de hechos fijados omitidas: las resume traza_por_cierre.py)"
            )
            saltando, omitidas = False, 0
        if etiqueta == "tr" and saltando:
            omitidas += 1
            continue
        if sin_hechos and etiqueta == "p" and str(contenido).startswith("Hechos fijados"):
            print(str(contenido))
            saltando = True
            continue
        if etiqueta == "tr":
            celdas = [str(c) for c in contenido]  # type: ignore[union-attr]
            horas = [h for c in celdas for h in HORA.finditer(c)]
            if any(
                int(h.group(1)) <= 23
                and _antes_del_dia(int(h.group(1)), int(h.group(2)), int(h.group(3) or 0), fecha)
                for h in horas
            ):
                print(f"  | {OCULTO}")
            else:
                print("  | " + " | ".join(celdas))
            continue
        texto = str(contenido)
        texto = SESGO.sub("", texto)
        if "saldo al cierre" in texto:
            texto = (
                texto.split("· saldo al cierre", 1)[0].rstrip(" ·") + " · (saldo y equity omitidos)"
            )
        texto = _enmascarar_horas(texto, fecha)
        prefijo = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### "}.get(etiqueta, "")
        print(f"{prefijo}{texto}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), sin_hechos="--sin-hechos" in sys.argv[2:]))
