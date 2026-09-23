"""El criterio de lectura de los instantes de v5, CONGELADO antes de abrir ningun fotograma nuevo.

Documento: `docs/validation/V5-INSTANTES-CRITERIO.md` (2026-09-23, rama `trabajo/v5-instantes`).
Este script es su implementacion exacta; cambiarlo despues de mirar es cambiar el criterio.

Dos modos:
  `uv run python scripts/v5_criterio.py --calibrar`  -> solo los CUATRO fotogramas ya abiertos.
  `uv run python scripts/v5_criterio.py --medir`     -> los 36 de la ventana fija. NO se ejecuta
                                                        sin luz verde del consultor.

Usa el decodificador de `scripts/decodificar_png.py`. Todo numerico: colores por tono, umbrales en
pixeles, y ningun OCR.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType

RAIZ = Path(__file__).resolve().parents[1]
FOTOGRAMAS = RAIZ / "data" / "fotogramas" / "v5" / "png-1fps"
ABIERTOS = ("000216000", "000225000", "000292000", "000293000")
# Los SEIS instantes pendientes (decision del consultor, 2026-09-23) y la ventana FIJA: t..t+5 s.
INSTANTES = {
    "1 (0:01:46)": 106,
    "2 (0:02:33)": 153,
    "3 (0:03:21)": 201,
    "4 (0:03:29)": 209,
    "6 (0:04:44)": 284,
    "7 (0:04:58)": 298,
}
VENTANA_S = 6
# LA LISTA CERRADA de los 36, escrita aqui y comprobada contra su derivacion (t..t+5 s de los seis).
# Cualquier otro nombre se rechaza ANTES de leer ni un byte del fichero.
MEDIR = (
    "000106000", "000107000", "000108000", "000109000", "000110000", "000111000",
    "000153000", "000154000", "000155000", "000156000", "000157000", "000158000",
    "000201000", "000202000", "000203000", "000204000", "000205000", "000206000",
    "000209000", "000210000", "000211000", "000212000", "000213000", "000214000",
    "000284000", "000285000", "000286000", "000287000", "000288000", "000289000",
    "000298000", "000299000", "000300000", "000301000", "000302000", "000303000",
)  # fmt: skip
assert (
    tuple(f"{(t + k) * 1000:09d}" for t in INSTANTES.values() for k in range(VENTANA_S)) == MEDIR
), "la lista cerrada no es la ventana t..t+5 s de los seis instantes"
# La extraccion de F05: el manifiesto commiteado fija el sha del indice, y el indice el de cada PNG.
MANIFIESTO_F05 = RAIZ / "knowledge" / "corpus" / "fotogramas" / "fr-v5-718ecabb.yaml"

# Region del grafico y umbrales, calibrados con los cuatro abiertos (documento, seccion 3).
Y_MIN, Y_MAX = 80, 640
X_MIN, X_MAX = 75, 1250
LARGO_MIN = 40  # px seguidos de una linea de nivel coloreada
TOL_NIVEL = 3  # px: donde se busca el borde gris del nivel 0 o 1, desde 0,8 y 0,5
FRACCION_GRIS = 0.5  # el borde gris cubre al menos la mitad del ancho de la caja
ZONA_MIN = 20  # px que ABARCA cada zona de la herramienta en una columna
VISIBLES_MIN = 6  # px de relleno visibles de cada zona en esa columna
UNION_MAX = 6  # px entre las dos zonas (la arista de entrada)
ANCHO_ZONA_MIN = 30  # columnas seguidas con las dos zonas
ANCLA_MAX = 2  # px entre el nivel 0 de la caja y la arista de entrada (LA-CAJA-DEL-29-DE-ABRIL:180)
DENTRO = 2  # px: un superviviente "cae dentro"
FUERA = 4  # px: "queda fuera por mas de 4"

Pixel = tuple[int, ...]


def _png() -> ModuleType:
    if "decodificar_png" in sys.modules:
        return sys.modules["decodificar_png"]
    spec = importlib.util.spec_from_file_location(
        "decodificar_png", RAIZ / "scripts" / "decodificar_png.py"
    )
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["decodificar_png"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def azul(p: Pixel) -> bool:
    return p[2] >= p[0] + 60 and p[2] >= p[1] + 60


def verde(p: Pixel) -> bool:
    return p[1] >= p[0] + 20 and p[1] >= p[2] + 40


def gris(p: Pixel) -> bool:
    return max(p) - min(p) <= 16 and 95 <= p[0] <= 175


def rojo_zona(p: Pixel) -> bool:
    return all(abs(a - b) <= 8 for a, b in zip(p, (59, 22, 26), strict=True))


def teal_zona(p: Pixel) -> bool:
    return all(abs(a - b) <= 8 for a, b in zip(p, (12, 41, 38), strict=True))


def rojizo(p: Pixel) -> bool:
    return p[0] >= p[1] + 25 and p[0] >= p[2] + 20


def _rgb(img: object, x: int, y: int) -> Pixel:
    return img.pixel(x, y)[:3]  # type: ignore[attr-defined, no-any-return]


def tramos(img: object, y: int, clase, x0: int = X_MIN, x1: int = X_MAX) -> list[tuple[int, int]]:  # type: ignore[no-untyped-def]
    salida: list[tuple[int, int]] = []
    ini: int | None = None
    for x in range(x0, x1):
        if clase(_rgb(img, x, y)):
            ini = x if ini is None else ini
        elif ini is not None:
            salida.append((ini, x - 1))
            ini = None
    if ini is not None:
        salida.append((ini, x1 - 1))
    return salida


@dataclass(frozen=True)
class Caja:
    y08: int
    y05: int
    x_izq: int
    x_der: int

    @property
    def delta(self) -> float:
        return (self.y05 - self.y08) / 0.3

    @property
    def y1(self) -> float:
        return self.y08 - 0.2 * self.delta

    @property
    def y0(self) -> float:
        return self.y05 + 0.5 * self.delta


def caja(img: object) -> Caja | None:
    """Linea azul (0,8) y verde (0,5) que ACABAN en la misma x (+-3), la verde 5..400 px debajo."""
    filas = range(Y_MIN, Y_MAX)
    azules = [(y, a, b) for y in filas for a, b in tramos(img, y, azul) if b - a + 1 >= LARGO_MIN]
    verdes = [(y, a, b) for y in filas for a, b in tramos(img, y, verde) if b - a + 1 >= LARGO_MIN]
    mejor: tuple[int, Caja] | None = None
    for ya, aa, ba in azules:
        for yv, av, bv in verdes:
            if abs(ba - bv) <= 3 and 5 <= yv - ya <= 400:
                largo = (ba - aa) + (bv - av)
                if mejor is None or largo > mejor[0]:
                    mejor = (largo, Caja(ya, yv, min(aa, av), max(ba, bv)))
    return mejor[1] if mejor else None


def borde_gris(img: object, c: Caja, y_pred: float) -> int | None:
    ancho = c.x_der - c.x_izq + 1
    for y in range(round(y_pred) - TOL_NIVEL, round(y_pred) + TOL_NIVEL + 1):
        if Y_MIN <= y < Y_MAX:
            for a, b in tramos(img, y, gris, c.x_izq, c.x_der + 1):
                if b - a + 1 >= FRACCION_GRIS * ancho:
                    return y
    return None


def detector_a(img: object) -> tuple[bool, Caja | None, int | None, int | None]:
    """SI solo si hay caja y SUS DOS bordes grises -nivel 1 y nivel 0- estan donde los ponen 0,8 y
    0,5 (+-TOL_NIVEL)."""
    c = caja(img)
    if c is None:
        return False, None, None, None
    y1, y0 = borde_gris(img, c, c.y1), borde_gris(img, c, c.y0)
    return (y1 is not None and y0 is not None), c, y1, y0


@dataclass(frozen=True)
class Herramienta:
    x_izq: int
    x_der: int
    y_stop: float
    y_entrada: float
    y_tp: float
    lado: str


def detector_b(img: object) -> tuple[bool, Herramienta | None]:
    """VALIDA si en >= ANCHO_ZONA_MIN columnas seguidas hay relleno rojo y teal que ABARCAN cada
    uno >= ZONA_MIN px, con >= VISIBLES_MIN visibles, sin solaparse y a <= UNION_MAX px. En estado
    de error ("Order Error") la herramienta no pinta zonas. Medida: mediana por columna."""
    filas: dict[int, tuple[int, float, int, str]] = {}
    buenas: list[bool] = []
    for x in range(X_MIN, X_MAX):
        r = [y for y in range(Y_MIN, Y_MAX) if rojo_zona(_rgb(img, x, y))]
        t = [y for y in range(Y_MIN, Y_MAX) if teal_zona(_rgb(img, x, y))]
        ok = False
        lado = ""
        visibles = len(r) >= VISIBLES_MIN and len(t) >= VISIBLES_MIN
        if visibles and max(r) - min(r) + 1 >= ZONA_MIN and max(t) - min(t) + 1 >= ZONA_MIN:
            if max(r) < min(t) and min(t) - max(r) - 1 <= UNION_MAX:
                lado, ok = "venta", True
            elif max(t) < min(r) and min(r) - max(t) - 1 <= UNION_MAX:
                lado, ok = "compra", True
        if ok and lado == "venta":
            stop = min(r)
            while stop - 1 >= Y_MIN and rojizo(_rgb(img, x, stop - 1)):
                stop -= 1
            filas[x] = (stop, (max(r) + min(t)) / 2, max(t), lado)
        elif ok:
            stop = max(r)
            while stop + 1 < Y_MAX and rojizo(_rgb(img, x, stop + 1)):
                stop += 1
            filas[x] = (stop, (max(t) + min(r)) / 2, min(t), lado)
        buenas.append(ok)
    mejor, act = (0, -1), None
    for x, ok in zip(range(X_MIN, X_MAX), buenas, strict=True):
        if ok:
            act = (act[0], x) if act else (x, x)
            if act[1] - act[0] > mejor[1] - mejor[0]:
                mejor = act
        else:
            act = None
    if mejor[1] - mejor[0] + 1 < ANCHO_ZONA_MIN:
        return False, None
    xs = list(range(mejor[0], mejor[1] + 1))

    def med(k: int) -> float:
        return float(sorted(filas[x][k] for x in xs)[len(xs) // 2])  # type: ignore[type-var]

    return True, Herramienta(mejor[0], mejor[1], med(0), med(1), med(2), filas[xs[0]][3])


@dataclass(frozen=True)
class Lectura:
    fotograma: str
    a: bool
    b: bool
    valido: bool
    motivo: str
    error_riesgo_real: float | None = None
    error_caja_completa: float | None = None
    veredicto: str = "no valido"
    y_stop: float | None = None
    y_entrada: float | None = None
    y_tp: float | None = None
    y_nivel_0: float | None = None
    y_nivel_1: float | None = None


class IntegridadError(ValueError):
    """Un fotograma fuera de la lista cerrada, o que no es el que F05 extrajo."""


def leer(nombre: str) -> Lectura:
    return evaluar(nombre, _png().leer(FOTOGRAMAS / f"{nombre}.png"))


def sha_esperados() -> dict[str, str]:
    """`fichero -> sha256` del indice de F05, despues de comprobar que el indice es el que fija el
    manifiesto commiteado (`sha256_index`)."""
    m = re.search(
        r"^sha256_index: ([0-9a-f]{64})$", MANIFIESTO_F05.read_text(encoding="utf-8"), re.M
    )
    if m is None:
        raise IntegridadError(f"{MANIFIESTO_F05.name}: sin sha256_index")
    indice = FOTOGRAMAS / "index.jsonl"
    if hashlib.sha256(indice.read_bytes()).hexdigest() != m.group(1):
        raise IntegridadError("index.jsonl no es el que fija el manifiesto de F05")
    filas = [json.loads(x) for x in indice.read_text(encoding="utf-8").splitlines() if x.strip()]
    return {str(f["fichero"]): str(f["sha256"]) for f in filas}


def verificar(nombres: tuple[str, ...]) -> None:
    """Todos los nombres estan en la lista cerrada y sus bytes son los que F05 extrajo. Nada se
    decodifica hasta que TODOS pasan."""
    fuera = [n for n in nombres if n not in MEDIR]
    if fuera:
        raise IntegridadError(f"fuera de la lista cerrada: {fuera}")
    esperados = sha_esperados()
    for n in nombres:
        real = hashlib.sha256((FOTOGRAMAS / f"{n}.png").read_bytes()).hexdigest()
        if esperados.get(f"{n}.png") != real:
            raise IntegridadError(f"{n}.png no es el fotograma que extrajo F05")


def leer_para_medir(nombre: str) -> Lectura:
    """Solo un nombre de la lista cerrada, y solo verificado contra F05."""
    verificar((nombre,))
    return leer(nombre)


def evaluar(nombre: str, img: object) -> Lectura:
    """El veredicto de UN fotograma ya decodificado: valido o no, y si valido, que superviviente
    cae dentro (+-DENTRO px) y cual fuera (> FUERA px), en stop y TP a la vez."""
    a, c, y1, y0 = detector_a(img)
    b, h = detector_b(img)
    pos = {
        "y_stop": h.y_stop if h else None,
        "y_entrada": h.y_entrada if h else None,
        "y_tp": h.y_tp if h else None,
        "y_nivel_0": y0,
        "y_nivel_1": y1,
    }
    if not (a and b) or c is None or h is None or y1 is None or y0 is None:
        falla = " y ".join(k for k, ok in (("a)", a), ("b)", b)) if not ok) or "a)"
        return Lectura(nombre, a, b, False, f"no cumple {falla}", **pos)
    if abs(y0 - h.y_entrada) > ANCLA_MAX:
        return Lectura(
            nombre, a, b, False, f"ancla: |nivel 0 - entrada| = {abs(y0 - h.y_entrada)}", **pos
        )
    if (y1 - y0) * (h.y_stop - h.y_entrada) <= 0:
        return Lectura(nombre, a, b, False, "el nivel 1 y el stop no estan del mismo lado", **pos)
    d = y1 - y0  # con signo: hacia el lado del stop
    pred = {
        "riesgo_real": (y0 + 0.8 * d, y0 - 3 * 0.8 * d),  # stop en 0,8; TP a 3 x (entrada-stop)
        "caja_completa": (y0 + 1.0 * d, y0 - 3 * 1.0 * d),  # stop en 1,0; TP a 3 x caja
    }
    err = {k: max(abs(h.y_stop - s), abs(h.y_tp - tp)) for k, (s, tp) in pred.items()}
    rr, cc = err["riesgo_real"], err["caja_completa"]
    if rr <= DENTRO and cc > FUERA:
        veredicto = "separa: riesgo_real"
    elif cc <= DENTRO and rr > FUERA:
        veredicto = "separa: caja_completa"
    else:
        veredicto = "no separa"
    return Lectura(nombre, a, b, True, "valido", rr, cc, veredicto, **pos)


def resultado_instante(lecturas: list[Lectura]) -> str:
    """Separa hacia X si al menos UNO de sus fotogramas validos separa hacia X y NINGUNO separa en
    sentido contrario: los «no separa» no vetan. Los dos sentidos dentro del instante son
    contradiccion, y cuenta como contradiccion global."""
    validas = [x for x in lecturas if x.valido]
    if not validas:
        return "sin fotograma valido"
    sentidos = {x.veredicto for x in validas if x.veredicto.startswith("separa")}
    if len(sentidos) == 2:
        return "contradictorio"
    return sentidos.pop() if sentidos else "no separa"


def resultado_global(por_instante: dict[str, str]) -> str:
    validos = {k: v for k, v in por_instante.items() if v != "sin fotograma valido"}
    if not validos:
        return "la medida NO ESTA en v5"
    sentidos = {v for v in validos.values() if v.startswith("separa")}
    if "contradictorio" in validos.values() or len(sentidos) == 2:
        return "contradictorio: A-18 sube a bloqueante, no se elige superviviente"
    return f"separacion hacia {sentidos.pop().split(': ')[1]}" if sentidos else "no separa"


def _px(v: float | None) -> str:
    return "-" if v is None else f"{v:g}"


def formato(lec: Lectura) -> str:
    """Una linea por fotograma, sirva o no: que falla, posiciones en px, errores y veredicto."""
    sirve = "SIRVE" if lec.valido else f"NO SIRVE ({lec.motivo})"
    return (
        f"{lec.fotograma}: {sirve} | stop {_px(lec.y_stop)} entrada {_px(lec.y_entrada)} "
        f"TP {_px(lec.y_tp)} nivel_0 {_px(lec.y_nivel_0)} nivel_1 {_px(lec.y_nivel_1)} | "
        f"error riesgo_real {_px(lec.error_riesgo_real)} caja_completa "
        f"{_px(lec.error_caja_completa)} | {lec.veredicto}"
    )


def main(argv: list[str]) -> int:
    if argv[1:] == ["--calibrar"]:
        for nombre in ABIERTOS:
            print(formato(leer(nombre)))
        return 0
    if argv[1:] == ["--medir"]:
        verificar(MEDIR)  # los 36, contra F05, ANTES de decodificar ninguno
        por_instante: dict[str, str] = {}
        for instante, t in INSTANTES.items():
            lecturas = [leer_para_medir(f"{(t + k) * 1000:09d}") for k in range(VENTANA_S)]
            for lec in lecturas:
                print(f"{instante} {formato(lec)}")
            por_instante[instante] = resultado_instante(lecturas)
            print(f"== {instante}: {por_instante[instante]}")
        print(f"== GLOBAL: {resultado_global(por_instante)}")
        return 0
    print("uso: v5_criterio.py --calibrar | --medir", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
