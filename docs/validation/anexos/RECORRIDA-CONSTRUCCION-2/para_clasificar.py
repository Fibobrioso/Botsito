"""La lista «Para clasificar» de trabajo/recorrida-construccion-2 (D8 del encargo del consultor del
2026-11-08): la materia de la PARADA 2, sin conclusiones.

Lee SOLO salidas del arnes ya escritas (ninguna vela, ningun tick, ningun caso): la de la corrida 1
(la que cuenta, cuenta por mes) y la de la corrida 2 (la diaria, diagnostico), y clasifica con
`patrones.py`, la copia identica de esta carpeta.

Uso (desde la raiz):
    uv run python docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/para_clasificar.py \
        <corrida 1> <corrida 2>

Dos tablas:
1. Cada operacion del trader: el escalon de la cascada de ADR-0092 §2 en que se queda en la corrida
   1 y en la 2, la orden del bot que mira, su patron (T0, P1 a P7), el primer hecho del camino que
   falta en su sesion (el embudo, el que la salida da en su fila), si el dia viene de video
   (`material_sin_video`, leido de la linea «libros sin video» de la salida) y si toca una hora de
   ticks perdida (la marca «posible M» de `patrones.py`).
2. Cada orden del bot en un (dia, sesion, direccion) sin operacion del trader, en la corrida 1: su
   resultado, su R neto y su desenlace (de «### Posiciones»), si su stop se movio (un evento
   `stop_movido` de su posicion en «### Eventos del broker») y su patron.

Lo que la salida NO trae, y se declara (D8: «si necesita leer algo que no este en la salida, dilo y
deja la columna vacia»):
- **El stop del trader** no esta en ninguna linea de la salida (la fila del trader de «Por
  operacion» lleva lado, instante y entrada). Sin el, la cascada se calcula hasta la entrada:
  «sin orden», «entrada fuera» o ENTRADA_DENTRO, que agrupa los cinco escalones siguientes (stop
  fuera, sin stop, no llenada, llenada fuera, completa). Para que el consultor tenga lo que si se
  sabe de esas, la fila da el resultado de la orden que mira y, si se lleno, cuantos minutos la
  separan del instante del trader.
- **La direccion de una orden NO llenada** tampoco esta escrita: se lee de su «caja 1» (el 1 de la
  caja, el extremo de la zona: por encima del precio, venta; por debajo, compra). En una orden
  llenada se toma el lado de su posicion, y se comprueba que la caja dice lo mismo.
Para que lo deducido no se quede en supuesto, el guion compara, mes a mes, lo que cuenta con la
cascada que la propia salida imprime (los dos primeros escalones, uno a uno; los cinco ultimos,
sumados) y las ordenes sin trader con la linea de la salida; si algo no coincide, lo dice y sale
con 1.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import patrones  # noqa: E402  (la copia identica de esta carpeta)

ESCALA = 100_000
SIN_ORDEN = "sin orden del bot en su (dia, sesion, direccion)"
ENTRADA_FUERA = "orden, con la entrada fuera de tolerancia"
ENTRADA_DENTRO = "entrada dentro (el stop del trader no esta en la salida)"
ESCALONES = (SIN_ORDEN, ENTRADA_FUERA, ENTRADA_DENTRO)
TOLERANCIAS = re.compile(
    r"^tolerancias: entrada (\d+) puntos, stop (\d+) puntos, llenado (\d+) min"
)
SIN_TRADER = re.compile(r"^ordenes del bot en un \(dia, sesion, direccion\) sin ninguna operacion "
                        r"del trader: (\d+)")  # fmt: skip
SIN_VIDEO = re.compile(
    r"^libros sin video: (.*), salvo (.*); cuentan como CON video, provisionales hasta que T lo "
    r"compruebe: (.*) \(fuente"
)
EMBUDO = re.compile(r"primer hecho que falto: (.*)$")
STOP_MOVIDO = "stop_movido"
LLENADA = "llenada"
# (dia, sesion, lado, instante UTC, entrada) de una operacion del trader, como la escribe la salida
Clave = tuple[str, str, str, str, str]


@dataclass(frozen=True)
class Orden:
    dia: str
    sesion: str
    id: str
    colocada: datetime
    precio: Decimal
    resultado: str
    instante: str
    caja: str
    direccion: str | None  # None: no se puede leer


@dataclass(frozen=True)
class Posicion:
    dia: str
    sesion: str
    id: str
    orden: str
    lado: str
    llenada: str
    entrada: Decimal
    desenlace: str
    r_neto: str


@dataclass
class Salida:
    ordenes: list[Orden]
    posiciones: list[Posicion]
    stops_movidos: set[tuple[str, str]]  # (dia, id de posicion)
    cascada: dict[str, list[int]]  # mes -> recuentos por escalon de la salida, y el total al final
    escalones_salida: list[str]
    sin_trader: int | None
    tol_entrada: int
    tol_llenado: int
    sin_video: tuple[set[str], set[str], set[str]]  # meses, dias con video, provisionales
    contradicciones: list[str]  # ordenes llenadas cuya caja dice otro lado que su posicion


def _seccion(lineas: list[str], empieza: str, acaba: str) -> list[str]:
    """Las filas de la tabla cuya cabecera empieza por `empieza`, hasta la linea que empieza por
    `acaba` (sin ella). Vacia si la tabla no esta o dice «ninguna»."""
    for i, ln in enumerate(lineas):
        if ln.startswith(empieza):
            salida = []
            for fila in lineas[i + 1 :]:
                if fila.startswith(acaba):
                    break
                salida.append(fila)
            return [f for f in salida if f and f not in ("ninguna", "ninguno")]
    return []


def _lado_de_caja(precio: Decimal, caja: str) -> str | None:
    if caja == "-":
        return None
    c = Decimal(caja)
    return "venta" if c > precio else "compra" if c < precio else None


def leer_salida(texto: str) -> Salida:
    lineas = [patrones._cuerpo(ln) for ln in texto.splitlines()]
    posiciones = []
    for fila in _seccion(lineas, "### Posiciones (dia", "posiciones: "):
        c = fila.split(" | ")
        posiciones.append(Posicion(c[0], c[1], c[2], c[3], c[4], c[6], Decimal(c[7]), c[11], c[18]))
    lado_de = {(p.dia, p.orden): p.lado for p in posiciones}
    ordenes, contradicciones = [], []
    for fila in _seccion(lineas, "### Ordenes (dia", "ordenes: "):
        c = fila.split(" | ")
        dia, sesion, oid, colocada, precio, resultado, instante, caja = (
            c[0], c[1], c[2], c[3], Decimal(c[4]), c[5], c[7], c[16],
        )  # fmt: skip
        por_caja = _lado_de_caja(precio, caja)
        lado = lado_de.get((dia, oid))
        if lado is not None and por_caja is not None and lado != por_caja:
            contradicciones.append(f"{dia} {oid}: posicion {lado}, caja {por_caja}")
        ordenes.append(
            Orden(
                dia, sesion, oid, datetime.fromisoformat(colocada), precio, resultado, instante,
                caja, lado or por_caja,
            )
        )  # fmt: skip
    movidos = set()
    for fila in _seccion(lineas, "### Eventos del broker", "eventos: "):
        c = fila.split(" | ")
        if len(c) == 5 and c[2] == STOP_MOVIDO:
            movidos.add((c[0], c[3]))
    cascada: dict[str, list[int]] = {}
    escalones: list[str] = []
    sin_trader = None
    tol_entrada = tol_llenado = -1
    sin_video: tuple[set[str], set[str], set[str]] = (set(), set(), set())
    dentro = False
    for ln in lineas:
        if ln.startswith("### Fidelidad por criterios"):
            dentro = True
            continue
        if dentro:
            m = TOLERANCIAS.match(ln)
            if m:
                tol_entrada, tol_llenado = int(m.group(1)), int(m.group(3))
            elif ln.startswith("mes | "):
                escalones = ln.split(" | ")[1:-1]
            elif SIN_TRADER.match(ln):
                sin_trader = int(SIN_TRADER.match(ln).group(1))  # type: ignore[union-attr]
                dentro = False
            elif " | " in ln:
                c = ln.split(" | ")
                cascada[c[0]] = [int(x) for x in c[1:]]
        m = SIN_VIDEO.match(ln)
        if m:

            def _lista(s: str) -> set[str]:
                return {x for x in s.split(", ") if x and x not in ("ningun dia", "ninguno")}

            sin_video = (_lista(m.group(1)), _lista(m.group(2)), _lista(m.group(3)))
    return Salida(
        ordenes, posiciones, movidos, cascada, escalones, sin_trader, tol_entrada, tol_llenado,
        sin_video, contradicciones,
    )  # fmt: skip


def video_de(dia: str, sin_video: tuple[set[str], set[str], set[str]]) -> str:
    meses, dias_con, provisionales = sin_video
    if dia in dias_con:
        return "con video (dia con video de un libro sin video)"
    if dia[:7] in provisionales:
        return "con video, provisional"
    if dia[:7] in meses:
        return "sin video"
    return "con video"


@dataclass(frozen=True)
class Paso:
    escalon: str
    orden: str  # «id resultado [llenada a N min]» o «-»


def cascada_hasta_la_entrada(trader: Clave, salida: Salida) -> Paso:
    """ADR-0092 §2 hasta donde la salida deja: la orden del bot de su (dia, sesion, direccion) mas
    cercana en entrada (a igualdad, la de colocacion mas cercana al instante del trader, y luego la
    mas temprana), como `cascada_por_criterios`."""
    dia, sesion, lado, instante, entrada = trader
    t, e = datetime.fromisoformat(instante), Decimal(entrada)
    candidatas = [
        o for o in salida.ordenes if (o.dia, o.sesion, o.direccion) == (dia, sesion, lado)
    ]
    if not candidatas:
        return Paso(SIN_ORDEN, "-")
    o = min(
        candidatas,
        key=lambda c: (
            abs(c.precio - e) * ESCALA,
            abs((c.colocada - t).total_seconds()),
            c.colocada,
        ),
    )
    detalle = f"{o.id} {o.resultado}"
    if o.resultado == LLENADA:
        minutos = abs((datetime.fromisoformat(o.instante) - t).total_seconds()) / 60
        detalle += f", llenada a {minutos:.1f} min del trader"
    if abs(o.precio - e) * ESCALA > salida.tol_entrada:
        return Paso(ENTRADA_FUERA, detalle)
    return Paso(ENTRADA_DENTRO, detalle)


def _clave_fila(fila: str) -> Clave:
    c = fila.split(" | ")
    return c[1], c[2], c[3], c[4], c[5]


def trader_de(clasificadas: list[tuple[str, str, str, str]]) -> dict[Clave, tuple[str, str, str]]:
    """(dia, sesion, lado, instante, entrada) -> (patron, marca M, embudo) por fila del trader."""
    salida: dict[Clave, tuple[str, str, str]] = {}
    for patron, _detalle, marca, fila in clasificadas:
        if fila.startswith("trader | "):
            m = EMBUDO.search(fila)
            salida[_clave_fila(fila)] = (patron, marca, m.group(1) if m else "-")
    return salida


def comprobar(pasos: dict[Clave, Paso], salida: Salida, nombre: str) -> list[str]:
    """Lo contado frente a la cascada que imprime la salida; cada discrepancia, una linea."""
    problemas = [f"{nombre}: {c}" for c in salida.contradicciones]
    sin = sum(1 for o in salida.ordenes if o.direccion is None)
    if sin:
        problemas.append(f"{nombre}: {sin} ordenes sin direccion legible")
    por_mes: dict[str, Counter[str]] = defaultdict(Counter)
    for clave, p in pasos.items():
        por_mes[clave[0][:7]][p.escalon] += 1
        por_mes["total"][p.escalon] += 1
    for mes, cuenta in sorted(por_mes.items()):
        fila = salida.cascada.get(mes)
        if fila is None:
            problemas.append(f"{nombre}: {mes} no esta en la cascada de la salida")
            continue
        esperado = (fila[0], fila[1], sum(fila[2:-1]))
        contado = (cuenta[SIN_ORDEN], cuenta[ENTRADA_FUERA], cuenta[ENTRADA_DENTRO])
        if esperado != contado:
            problemas.append(f"{nombre}: {mes} contado {contado}, la salida {esperado}")
    claves = {(k[0], k[1], k[2]) for k in pasos}
    sin_trader = sum(1 for o in salida.ordenes if (o.dia, o.sesion, o.direccion) not in claves)
    if salida.sin_trader is not None and sin_trader != salida.sin_trader:
        problemas.append(
            f"{nombre}: ordenes sin trader contadas {sin_trader}, la salida {salida.sin_trader}"
        )
    return problemas


def bot_sin_trader(
    salida: Salida, claves: set[tuple[str, str, str]], clasificadas: list[tuple[str, str, str, str]]
) -> list[str]:
    patron_bot = {}
    for patron, detalle, _marca, fila in clasificadas:
        if fila.startswith("bot | "):
            dia, sesion, lado, instante, entrada = _clave_fila(fila)
            patron_bot[(dia, sesion, lado, instante, Decimal(entrada))] = f"{patron}" + (
                f" [{detalle}]" if detalle else ""
            )
    posicion_de = {(p.dia, p.orden): p for p in salida.posiciones}
    filas = []
    for o in salida.ordenes:
        if (o.dia, o.sesion, o.direccion) in claves:
            continue
        p = posicion_de.get((o.dia, o.id))
        if p is None:
            r, desenlace, movido, patron = "-", "-", "-", "- (no llenada)"
        else:
            r, desenlace = p.r_neto, p.desenlace
            movido = "si" if (o.dia, p.id) in salida.stops_movidos else "no"
            clave = (p.dia, p.sesion, p.lado, p.llenada, p.entrada)
            patron = patron_bot.get(clave, "sin fila del bot sin pareja (emparejada)")
        filas.append(
            f"{o.dia} | {o.sesion} | {o.direccion or '?'} | {o.id} | {o.resultado} | {r} | "
            f"{desenlace} | {movido} | {patron}"
        )
    return filas


def main(ruta1: Path, ruta2: Path) -> int:
    sys.stdout.reconfigure(encoding="utf-8", newline="\n")  # type: ignore[union-attr]
    corridas = []
    for ruta in (ruta1, ruta2):
        salida = leer_salida(ruta.read_text(encoding="utf-8"))
        filas, sesgo = patrones.leer(ruta)
        clasificadas = patrones.clasificar(filas, sesgo)
        corridas.append((ruta.name, salida, clasificadas, trader_de(clasificadas)))
    (n1, s1, c1, t1), (n2, s2, c2, t2) = corridas
    pasos1 = {k: cascada_hasta_la_entrada(k, s1) for k in t1}
    pasos2 = {k: cascada_hasta_la_entrada(k, s2) for k in t2}
    problemas = comprobar(pasos1, s1, n1) + comprobar(pasos2, s2, n2)
    if set(t1) != set(t2):
        problemas.append("las operaciones del trader no son las mismas en las dos salidas")

    print(f"# Para clasificar (D8). Corrida 1: {n1}; corrida 2: {n2}")
    print("# Comprobacion contra la cascada que imprime cada salida (dos primeros escalones uno a")
    print("# uno, los cinco ultimos sumados) y contra sus ordenes sin trader: "
          + ("coincide" if not problemas else "NO COINCIDE"))  # fmt: skip
    for p in problemas:
        print(f"#   {p}")
    print()
    print("## Resumen por mes (operaciones del trader por escalon; ordenes del bot sin trader)")
    print("mes | corrida | " + " | ".join(ESCALONES) + " | ordenes del bot sin trader")
    meses = sorted({k[0][:7] for k in t1})
    for nombre, pasos, salida in (("1", pasos1, s1), ("2", pasos2, s2)):
        claves = {(k[0], k[1], k[2]) for k in pasos}
        for mes in [*meses, "total"]:
            cuenta = Counter(
                p.escalon for k, p in pasos.items() if mes == "total" or k[0][:7] == mes
            )
            sin = sum(
                1
                for o in salida.ordenes
                if (o.dia, o.sesion, o.direccion) not in claves
                and (mes == "total" or o.dia[:7] == mes)
            )
            print(
                f"{mes} | {nombre} | " + " | ".join(str(cuenta[e]) for e in ESCALONES) + f" | {sin}"
            )
    print()
    print("## Operaciones del trader")
    print(
        "dia | sesion | lado | instante UTC | entrada | escalon corrida 1 | orden corrida 1 | "
        "patron corrida 1 | primer hecho que falta (corrida 1) | escalon corrida 2 | patron "
        "corrida 2 | video | hora perdida"
    )
    for k in sorted(t1, key=lambda x: (x[0], x[3], x[4])):
        p1, p2 = pasos1[k], pasos2.get(k)
        patron1, marca, embudo = t1[k]
        patron2 = t2.get(k, ("-", "", "-"))[0]
        print(
            f"{' | '.join(k)} | {p1.escalon} | {p1.orden} | {patron1} | {embudo} | "
            f"{p2.escalon if p2 else '-'} | {patron2} | {video_de(k[0], s1.sin_video)} | "
            f"{marca or 'no'}"
        )
    print()
    print("## Ordenes del bot en un (dia, sesion, direccion) sin operacion del trader (corrida 1)")
    print(
        "dia | sesion | direccion | orden | resultado | R neto | desenlace | stop movido | patron"
    )
    lista = bot_sin_trader(s1, {(k[0], k[1], k[2]) for k in pasos1}, c1)
    for f in lista:
        print(f)
    if not lista:
        print("ninguna")
    print()
    print("## Resumen de la lista anterior, por mes (sin conclusiones)")
    for linea in resumen_sin_trader(lista):
        print(linea)
    return 1 if problemas else 0


def resumen_sin_trader(lista: list[str]) -> list[str]:
    """Por mes: ordenes, llenadas, la suma del R neto de las llenadas, sus desenlaces, cuantas
    movieron el stop y sus patrones."""
    por_mes: dict[str, list[list[str]]] = defaultdict(list)
    for f in lista:
        c = f.split(" | ")
        por_mes[c[0][:7]].append(c)
        por_mes["total"].append(c)
    salida = []
    for mes in [m for m in sorted(por_mes) if m != "total"] + ["total"]:
        filas = por_mes[mes]
        llenadas = [c for c in filas if c[4] == LLENADA]
        suma_r = sum((Decimal(c[5]) for c in llenadas if c[5] != "-"), Decimal(0))
        desenlaces = Counter(c[6] for c in llenadas)
        patrones_ = Counter(c[8].split(" [")[0] for c in llenadas)
        salida.append(
            f"{mes} | ordenes {len(filas)} | llenadas {len(llenadas)} | suma del R neto "
            f"{suma_r:.3f}"
            f" | stop movido {sum(c[7] == 'si' for c in llenadas)} | desenlaces "
            + ", ".join(f"{k} {v}" for k, v in sorted(desenlaces.items()))
            + " | patrones "
            + ", ".join(f"{k} {v}" for k, v in sorted(patrones_.items()))
        )
    return salida


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2])))
