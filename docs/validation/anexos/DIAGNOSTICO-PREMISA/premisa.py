"""Los dos diagnosticos de construccion de ADR-0100: el registro del trader frente a la replica, mes
por mes (§5), y el techo con lote fijo (§6).

Rama `trabajo/diagnostico-premisa` (DIAGNOSTICO-PREMISA.md). Pre-registrado en el commit del ADR de
la premisa (ADR-0100 y `docs/plan/PREMISA-COSTES.yaml`) antes de que este guion existiera.

Uso (desde la raiz; la carpeta de salida es un argumento):

    uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py control \\
        docs/validation/anexos/DIAGNOSTICO-PREMISA
    uv run python -B docs/validation/anexos/DIAGNOSTICO-PREMISA/premisa.py todo \\
        docs/validation/anexos/DIAGNOSTICO-PREMISA

`control` escribe en la carpeta `control.txt` (D2 a y b) y los bloques de `base` y `todo_junto`
regenerados (`base-repetida.txt`, `todo_junto-repetida.txt`), para el `diff` contra los de
`anexos/PUENTE-TECHO/`. `todo` escribe `premisa.txt` (las tres medidas) y `lectura.txt` (las dos
lecturas, literales), con el entorno construido una sola vez. Sale con 0 si todo se hizo, con 4 si
D2 a no pasa, con 5 si D2 b no pasa y con 2 ante un error de entrada.

EL MODELO es el de `anexos/PUENTE-TECHO/puente.py` de `main`, cargado por su ruta y sin copiar (que
a su vez carga `techo_parejas.py`): el entorno, las piezas, la repeticion, las filas y las medidas.
Las variantes `base` y `todo_junto` salen de `PUENTE-TECHO.yaml` con `piezas_de`, sin cambiar
ninguna pieza (D1). Lo nuevo de este guion:

- EL REGISTRO (D3): por cada operacion del trader con stop de los casos dev de construccion, su fila
  del libro de su mes, leida por `corpus.libro.filas_de_los_dias` (que solo devuelve las filas de
  los dias pedidos) y unida con el criterio de `scripts/viabilidad_trader.py` (`cargar`): la clave
  es el instante UTC del llenado y la entrada, y el `initialSL` del libro tiene que ser el stop del
  caso. Su R = (avgClosePrice - entrada) x direccion / D, con D la distancia de la entrada al stop
  del caso, sin costes.
- LA REPLICA (D4): la variante `todo_junto`, su R antes de comision por posicion (bruto / riesgo),
  sobre las mismas operaciones que el registro: las que `todo_junto` abre (por su id `t<k>`, la
  k-esima operacion del dia en el caso).
- EL TECHO CON LOTE FIJO (D5): por posicion, R neto x D / mediana de D, con D la distancia del
  riesgo de su fila (riesgo x escala / (lotes x contrato)), y sus percentiles por
  `remuestreo_por_dias` con una posicion de riesgo 1 y PnL igual a ese R, como
  `techo_parejas.percentil_de_diferencias`.
- EL RETROCESO (D6): de las ganadoras del registro, entre el llenado del caso y `dateEnd`, el BID
  minimo (compra) o el ASK maximo (venta) de los ticks; en los minutos sin ticks, la M1 de bid del
  respaldo (compra: su minima; venta: su maxima mas `spread_supuesto` de la configuracion del
  llenado, como el broker), contra la entrada menos `desfase_puntos`, en fracciones de D.

LO QUE IMPRIME (D7; `que_no_imprime` del yaml): por mes y por bloque, recuentos y medias; por
bloque,
los recuentos del retroceso; por variante, la esperanza con lote fijo y sus percentiles; y los
recuentos de lo que queda fuera. Ninguna operacion con su R, sus precios ni su fecha; ningun R por
clase de setup, por sesion ni por direccion; ninguna vela ni ningun nivel; nada de un dia que no sea
dev (los dias son los de `arnes.dias_de_construccion`).
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

# el guion del puente de `main`, por su ruta literal (desde la raiz), sin copiarlo
_ESPEC = importlib.util.spec_from_file_location(
    "puente", "docs/validation/anexos/PUENTE-TECHO/puente.py"
)
if _ESPEC is None or _ESPEC.loader is None:
    raise ImportError("no encuentro puente.py: el guion se lanza desde la raiz")
pt: Any = importlib.util.module_from_spec(_ESPEC)
sys.modules["puente"] = pt  # sus dataclasses lo buscan aqui
_ESPEC.loader.exec_module(pt)
tp: Any = pt.tp

RAIZ: Path = pt.RAIZ
MS: int = pt.MS

# Los cuatro libros, por su ruta LITERAL desde la raiz: el campo `fichero` de su entrada en
# `knowledge/corpus/libros.yaml`, bajo `corpus/Estrategia del trader/` (D3). Se verifican por su sha
# con `declaracion_de` y contra ese `fichero` antes de leer nada.
LIBROS: dict[str, Path] = {
    "2026-01": Path(
        "corpus/Estrategia del trader/Material adicional de su operativa/"
        "backtesting-analytics ENERO 2026.xlsx"
    ),
    "2026-04": Path(
        "corpus/Estrategia del trader/Material adicional de su operativa/"
        "backtesting-analytics ABRIL 2026.xlsx"
    ),
    "2026-07": Path(
        "corpus/Estrategia del trader/Material adicional de su operativa/"
        "Backtest Julio 2026/backtesting-analytics_JULIO_2026.xlsx"
    ),
    "2026-08": Path(
        "corpus/Estrategia del trader/Material adicional de su operativa/"
        "backtesting-analytics AGOSTO 2026.xlsx"
    ),
}
PREFIJO_DE_LIBROS = "corpus/Estrategia del trader/"
# las columnas de la union (dateStart la primera: es la del dia) y la salida con su instante
COLUMNAS = ("dateStart", "side", "entryPrice", "initialSL", "avgClosePrice", "dateEnd")

# Las salidas de `main` contra las que se repite D2 a, por variante, con su ruta literal.
PUBLICADAS_DEL_PUENTE: dict[str, Path] = {
    "base": Path("docs/validation/anexos/PUENTE-TECHO/base.txt"),
    "todo_junto": Path("docs/validation/anexos/PUENTE-TECHO/todo_junto.txt"),
}
# D2 b: la serie anotada de abril y agosto de VIABILIDAD-COMISION.md §3 (77 operaciones y +0,98 R
# de esperanza bruta), con la tolerancia del encargo; son cifras de un control, no de una lectura.
CONTROL_ANOTADA_N = 77
CONTROL_ANOTADA_MEDIA = Decimal("0.98")
CONTROL_ANOTADA_TOLERANCIA = Decimal("0.02")
MESES_DEL_CONTROL_ANOTADA = ("2026-04", "2026-08")

GANADORA, PERDEDORA, BREAK_EVEN = "ganadoras", "perdedoras", "break_even"

# --------------------------------------------------------------------------- piezas puras


def r_registro(direccion: str, entrada: Decimal, stop: Decimal, salida: Decimal) -> Decimal:
    """R = (salida - entrada) x direccion / D, con D la distancia de la entrada al stop, sin
    costes (ADR-0100 §5)."""
    d = abs(entrada - stop)
    if d == 0:
        raise ValueError("stop en la entrada: D es cero")
    signo = 1 if direccion == "compra" else -1
    return (salida - entrada) * signo / d


def tramo_r(r: Decimal, gana_si_mas_de: Decimal, pierde_si_menos_de: Decimal) -> str:
    """Ganadora si R > +0,2; perdedora si R < -0,2; el resto, break even (`tramos_r`)."""
    if r > gana_si_mas_de:
        return GANADORA
    if r < pierde_si_menos_de:
        return PERDEDORA
    return BREAK_EVEN


def media(valores: Sequence[Decimal]) -> Decimal | None:
    return sum(valores, Decimal(0)) / len(valores) if valores else None


def brecha(media_registro: Decimal | None, media_replica: Decimal | None) -> Decimal | None:
    """La media del R del registro menos la de la replica (`brecha`)."""
    if media_registro is None or media_replica is None:
        return None
    return media_registro - media_replica


def lectura_de_5(
    brecha_enero_y_julio: Decimal | None,
    brecha_abril_y_agosto: Decimal | None,
    margen: Decimal,
    orden: Sequence[str],
) -> str:
    """ADR-0100 §5, en el orden del yaml: la replica pierde mas en enero y julio si su brecha supera
    a la de abril y agosto en MAS de `margen_r`; si no, enero y julio peores tambien para el."""
    if brecha_enero_y_julio is None or brecha_abril_y_agosto is None:
        raise ValueError("una brecha sin definir: la lectura de §5 no se puede escribir")
    cumple = {
        "la_replica_pierde_mas_en_enero_y_julio": (
            brecha_enero_y_julio - brecha_abril_y_agosto > margen
        ),
        "enero_y_julio_peores_tambien_para_el": True,
    }
    return next(clave for clave in orden if cumple[clave])


def mediana_de(distancias: Sequence[int]) -> Decimal:
    """La mediana de D en Decimal: el central, o la media de los dos centrales si son pares (la de
    `statistics.median`, sin pasar por float)."""
    orden = sorted(distancias)
    n = len(orden)
    if n == 0:
        raise ValueError("mediana de nada")
    if n % 2:
        return Decimal(orden[n // 2])
    return (Decimal(orden[n // 2 - 1]) + Decimal(orden[n // 2])) / 2


def r_con_lote_fijo(rs_netos: Sequence[Decimal], distancias: Sequence[int]) -> list[Decimal]:
    """ADR-0100 §6: el R neto de cada posicion por su D, entre la mediana de D del conjunto."""
    if len(rs_netos) != len(distancias):
        raise ValueError("un R sin su D")
    if not distancias:
        return []
    mediana = mediana_de(distancias)
    return [r * Decimal(d) / mediana for r, d in zip(rs_netos, distancias, strict=True)]


def lectura_de_4(
    n: int,
    esperanza: Decimal | None,
    bajo: Decimal | None,
    alto: Decimal | None,
    n_minimo: int,
    esperanza_min: Decimal,
    alto_minimo: Decimal,
    orden: Sequence[str],
) -> str:
    """ADR-0100 §4, en el orden del yaml (sin no_valida ni insuficiente): gana si N >= n_minimo,
    esperanza >= esperanza_minima_r y percentil bajo > 0; no_gana si la esperanza < 0 o el
    percentil alto < el umbral; el resto, no_concluyente."""
    cumple = {
        "gana": n >= n_minimo
        and esperanza is not None
        and esperanza >= esperanza_min
        and bajo is not None
        and bajo > 0,
        "no_gana": (esperanza is not None and esperanza < 0)
        or (alto is not None and alto < alto_minimo),
        "no_concluyente": True,
    }
    return next(clave for clave in orden if cumple[clave])


@dataclass(frozen=True)
class Extremo:
    """El peor precio para la posicion entre dos instantes, y de donde salio."""

    precio: int | None  # puntos; None si no hay ni ticks ni M1 en todo el tramo
    minutos_con_respaldo: int
    del_respaldo: bool  # el extremo salio de una M1 del respaldo
    minutos_sin_datos: int


def extremo_en_contra(
    direccion: str,
    desde_ms: int,
    hasta_ms: int,
    ticks_del_minuto: Callable[[int], Sequence[Any] | None],
    m1_del_minuto: Callable[[int], Any | None],
    spread_supuesto: Callable[[int], int],
) -> Extremo:
    """En una compra, el BID minimo; en una venta, el ASK maximo, de los ticks de [desde, hasta];
    en un minuto sin ticks, la M1 de bid del respaldo (compra: su minima; venta: su maxima mas el
    spread supuesto de ese minuto), como el broker simulado. Puro: el mercado entra por
    funciones."""
    compra = direccion == "compra"
    mejor: int | None = None
    de_respaldo = False
    con_respaldo = 0
    sin_datos = 0
    for minuto in range(desde_ms // MS, hasta_ms // MS + 1):
        ticks = ticks_del_minuto(minuto)
        candidato: int | None = None
        respaldo = False
        if ticks:
            dentro = [t for t in ticks if desde_ms <= int(t.instante) <= hasta_ms]
            if dentro:
                candidato = (
                    min(int(t.bid) for t in dentro) if compra else max(int(t.ask) for t in dentro)
                )
        else:
            vela = m1_del_minuto(minuto)
            if vela is None:
                sin_datos += 1
            else:
                con_respaldo += 1
                respaldo = True
                candidato = (
                    int(vela.minima) if compra else int(vela.maxima) + spread_supuesto(minuto)
                )
        if candidato is None:
            continue
        if mejor is None or (candidato < mejor if compra else candidato > mejor):
            mejor, de_respaldo = candidato, respaldo
    return Extremo(mejor, con_respaldo, de_respaldo, sin_datos)


def retroceso(direccion: str, entrada: int, desfase: int, extremo: int, d: int) -> Fraction:
    """Cuanto fue en contra el precio, en fracciones de D, desde la entrada menos `desfase_puntos`
    (las dos series de precios, ADR-0099): en una compra, (entrada - desfase - BID minimo) / D; en
    una venta, (ASK maximo - (entrada - desfase)) / D. Negativo si nunca llego a la entrada."""
    if d <= 0:
        raise ValueError("D no positiva")
    referencia = entrada - desfase
    en_contra = referencia - extremo if direccion == "compra" else extremo - referencia
    return Fraction(en_contra, d)


def tramo_de_retroceso(x: Fraction, tramos: Sequence[Fraction]) -> str:
    """El tramo [a; b) de `tramos` (el ultimo, a o mas); por debajo del primero, `por_debajo`."""
    if x < tramos[0]:
        return "por_debajo"
    for a, b in zip(tramos, tramos[1:], strict=False):
        if a <= x < b:
            return _nombre_tramo(a, b)
    return _nombre_tramo(tramos[-1], None)


def _nombre_tramo(a: Fraction, b: Fraction | None) -> str:
    def f(x: Fraction) -> str:
        return str(float(x)).replace(".", ",")

    return f"[{f(a)}; {f(b)})" if b is not None else f"{f(a)} o mas"


def nombres_de_tramos(tramos: Sequence[Fraction]) -> list[str]:
    salida = [_nombre_tramo(a, b) for a, b in zip(tramos, tramos[1:], strict=False)]
    return [*salida, _nombre_tramo(tramos[-1], None)]


def _r(x: Decimal | None) -> str:
    return "sin definir" if x is None else f"{x:+.3f}"


# --------------------------------------------------------------------------- el registro


@dataclass
class OpRegistro:
    """Una operacion del trader con stop, unida a su fila. Nunca se imprime."""

    dia: str
    k: int  # la posicion en el caso (1..n): el id `t<k>` de la repeticion del puente
    direccion: str
    entrada: Decimal
    stop: Decimal
    instante_ms: int
    salida: Decimal
    salida_ms: int
    r: Decimal


@dataclass
class Registro:
    ops: dict[tuple[str, int], OpRegistro]
    fuera: dict[str, Counter[str]] = field(default_factory=dict)  # por mes

    def mas(self, mes: str, que: str, n: int = 1) -> None:
        self.fuera.setdefault(mes, Counter())[que] += n


def _instante_ms(instante: Any) -> int:
    return int(round(instante.timestamp() * 1000))


def verificar_libros(repo: Path) -> dict[str, Any]:
    """Cada ruta literal, contra `libros.yaml` por su sha (`declaracion_de`) y contra el `fichero`
    de su entrada, antes de leer ninguna fila. Devuelve las declaraciones por mes."""
    from botsito.comun.yaml_estricto import leer_yaml
    from botsito.corpus.libros import FICHERO_LIBROS, declaracion_de, sha256_de

    entradas = leer_yaml(repo / FICHERO_LIBROS)["libros"]
    salida: dict[str, Any] = {}
    for mes, ruta in LIBROS.items():
        decl = declaracion_de(repo, ruta)
        fichero = str(entradas[sha256_de(ruta)]["fichero"])
        literal = ruta.as_posix()  # se compara por trozos: ninguna ruta se compone con `fichero`
        if (
            not literal.startswith(PREFIJO_DE_LIBROS)
            or literal[len(PREFIJO_DE_LIBROS) :] != fichero
        ):
            raise ValueError(f"{mes}: la ruta del guion no es el `fichero` de libros.yaml")
        salida[mes] = decl
    return salida


def cargar_registro_del_trader(ent: Any) -> Registro:
    """D3: por cada operacion con stop de los casos dev, su fila del libro de su mes, por el lector
    y SOLO de los dias dev pedidos; la union de `viabilidad_trader.cargar`, para los cuatro
    meses."""
    from botsito.corpus.libro import PESTANA_OPERACIONES, _instante, filas_de_los_dias

    decls = verificar_libros(RAIZ)
    huso = ent.registro.texto("huso_operativa")
    reg = Registro({})
    for mes, ruta in LIBROS.items():
        dias = [d for d in ent.dias if d.dia.startswith(mes)]
        filas = filas_de_los_dias(
            ruta, [d.dia for d in dias], PESTANA_OPERACIONES, COLUMNAS, decls[mes],
            huso_de_los_dias=huso,
        )  # fmt: skip
        reg.mas(mes, "filas_sin_initialSL", sum(1 for f in filas if not f.get("initialSL")))
        con_stop = [f for f in filas if f.get("initialSL")]
        por_clave: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for f in con_stop:
            por_clave.setdefault((str(f["_instante_utc"]), str(f["entryPrice"])), []).append(f)
        reg.mas(
            mes, "claves_repetidas_en_el_libro", sum(1 for v in por_clave.values() if len(v) > 1)
        )
        usadas: set[int] = set()
        for d in dias:
            for k, op in enumerate(d.operaciones, start=1):
                if op.stop is None:
                    reg.mas(mes, "operaciones_sin_stop_en_el_caso")
                    continue
                entrada = Decimal(str(op.entrada))
                clave = (op.instante.isoformat(), str(entrada))
                candidatas = por_clave.get(clave)
                if candidatas is None:  # el libro escribe la entrada sin normalizar: por valor
                    candidatas = next(
                        (
                            v
                            for (t, e), v in por_clave.items()
                            if t == clave[0] and Decimal(e) == entrada
                        ),
                        None,
                    )
                if not candidatas:
                    reg.mas(mes, "sin_fila_en_el_libro")
                    continue
                libre = next((c for c in candidatas if id(c) not in usadas), None)
                if libre is None:
                    reg.mas(mes, "fila_ya_usada")
                    continue
                f = libre
                if Decimal(str(f["initialSL"])) != Decimal(str(op.stop)):
                    reg.mas(mes, "stop_del_caso_distinto_del_initialSL")
                    continue
                fin = _instante(str(f["dateEnd"]), decls[mes])
                if fin is None or not f.get("avgClosePrice"):
                    reg.mas(mes, "sin_salida_legible")
                    continue
                usadas.add(id(f))
                salida = Decimal(str(f["avgClosePrice"]))
                stop = Decimal(str(op.stop))
                reg.ops[(d.dia, k)] = OpRegistro(
                    d.dia, k, op.direccion, entrada, stop, _instante_ms(op.instante), salida,
                    _instante_ms(fin), r_registro(op.direccion, entrada, stop, salida),
                )  # fmt: skip
    return reg


# --------------------------------------------------------------------------- las corridas


def corrida(ent: Any, puente: Mapping[str, Any], nombre: str) -> Any:
    """Una variante del puente con `pt.correr`, sus piezas por `pt.piezas_de` del yaml."""
    lista = puente["variantes"][nombre]
    return pt.correr(ent, nombre, pt.piezas_de(lista, puente["propios"]))


def distancia_del_riesgo(ent: Any, fila: Any) -> int:
    """D en puntos: la del riesgo de la fila (riesgo = lotes x D / escala x contrato), que es la
    distancia de la entrada a su stop inicial (`posiciones_del_bot`, `pt.filas_conocidas`)."""
    escala = ent.mercados[fila.dia].escala
    d = fila.riesgo * escala / (fila.lotes * ent.contrato)
    if d != d.to_integral_value() or d <= 0:
        raise ValueError(f"{fila.dia} {fila.orden_id}: la D del riesgo no es un entero positivo")
    return int(d)


def k_de(fila: Any) -> int:
    """La k de `t<k>`: la operacion del caso que la repeticion abrio (`pt.pedidos_del_techo`)."""
    oid = str(fila.orden_id)
    if not oid.startswith("t") or not oid[1:].isdigit():
        raise ValueError(f"{fila.dia}: id de posicion inesperado")
    return int(oid[1:])


# --------------------------------------------------------------------------- el informe


@dataclass(frozen=True)
class Yamls:
    premisa: dict[str, Any]
    puente: dict[str, Any]
    meta: dict[str, Any]


def cargar_los_yaml(repo: Path) -> Yamls:
    from botsito.comun.yaml_estricto import leer_yaml

    meta, puente = pt.cargar_yaml(repo)
    premisa = leer_yaml(repo / "docs" / "plan" / "PREMISA-COSTES.yaml")
    if premisa.get("decision") != "ADR-0100":
        raise ValueError("PREMISA-COSTES.yaml no es el de ADR-0100")
    for v in premisa["techo_con_lote_fijo"]["variantes"]:
        if v not in puente["variantes"] or v not in PUBLICADAS_DEL_PUENTE:
            raise ValueError(f"la variante {v} no esta en PUENTE-TECHO.yaml o no tiene su salida")
    return Yamls(premisa, puente, meta)


def _bloques(y: Yamls) -> dict[str, list[str]]:
    return {k: list(v) for k, v in y.premisa["registro_frente_a_replica"]["bloques"].items()}


def _tramos_r(y: Yamls) -> tuple[Decimal, Decimal]:
    t = y.premisa["registro_frente_a_replica"]["tramos_r"]
    return Decimal(t["gana_si_mas_de"]), Decimal(t["pierde_si_menos_de"])


def _fila_de_serie(nombre: str, rs: Sequence[Decimal], tramos: tuple[Decimal, Decimal]) -> str:
    c = Counter(tramo_r(r, *tramos) for r in rs)
    return (
        f"{nombre}: N {len(rs)}; ganadoras {c[GANADORA]}; perdedoras {c[PERDEDORA]}; break even "
        f"{c[BREAK_EVEN]}; media del R {_r(media(rs))}"
    )


def control_anotada(reg: Registro) -> tuple[bool, list[str]]:
    """D2 b: el registro de abril y agosto, sobre TODAS sus operaciones con stop y antes de
    restringirlo a las de `todo_junto`, contra la serie anotada publicada."""
    rs = [o.r for o in reg.ops.values() if o.dia[:7] in MESES_DEL_CONTROL_ANOTADA]
    m = media(rs)
    vale = (
        len(rs) == CONTROL_ANOTADA_N
        and m is not None
        and abs(m - CONTROL_ANOTADA_MEDIA) <= CONTROL_ANOTADA_TOLERANCIA
    )
    return vale, [
        "## D2 b · El registro de abril y agosto frente a la serie anotada "
        "(VIABILIDAD-COMISION.md §3)",
        f"operaciones con stop unidas a su fila: {len(rs)} (publicadas: {CONTROL_ANOTADA_N}); "
        "media "
        f"del R bruto: {_r(m)} (publicada: +{CONTROL_ANOTADA_MEDIA}; tolerancia "
        f"{CONTROL_ANOTADA_TOLERANCIA})",
        "D2 b: " + ("PASA" if vale else "NO PASA (PARADA en el registro de §5)"),
    ]


def lineas_de_fuera(reg: Registro, meses: Sequence[str]) -> list[str]:
    salida = []
    for mes in meses:
        c = reg.fuera.get(mes, Counter())
        salida.append(
            f"{mes}: " + (", ".join(f"{k} {v}" for k, v in sorted(c.items()) if v) or "ninguna")
        )
    return salida


def medida_5(
    ent: Any, y: Yamls, reg: Registro, replica: Any
) -> tuple[list[str], str, list[tuple[OpRegistro, Decimal]]]:
    """§5: el registro y la replica sobre las mismas operaciones, por mes y por bloque, y su
    lectura. Devuelve tambien las parejas, para el retroceso."""
    tramos = _tramos_r(y)
    bloques = _bloques(y)
    meses = [m for b in bloques.values() for m in b]
    parejas: list[tuple[OpRegistro, Decimal]] = []
    sin_registro: Counter[str] = Counter()
    for f in replica.filas:
        op = reg.ops.get((f.dia, k_de(f)))
        if op is None:
            sin_registro[f.dia[:7]] += 1
            continue
        parejas.append((op, f.bruto / f.riesgo))
    abiertas = {(f.dia, k_de(f)) for f in replica.filas}
    registro_sin_replica: Counter[str] = Counter(
        dia[:7] for (dia, k) in reg.ops if (dia, k) not in abiertas
    )
    rec = replica.rep.recuentos
    lineas = [
        "## §5 · El registro del trader frente a la replica (todo_junto), sobre las mismas "
        "operaciones",
        "",
        "### Lo que queda fuera, por mes",
        "del registro (operaciones del caso o filas del libro que no entran):",
        *[f"  {x}" for x in lineas_de_fuera(reg, sorted(meses))],
    ]
    for mes in sorted(meses):
        rech = rec.rechazos([mes])
        lineas.append(
            f"  {mes}: la replica las deja fuera por el tope de lotes: "
            f"{rec.total('fuera_por_el_tope', [mes])}; por el lote minimo: "
            f"{rec.total('lote_minimo', [mes])}; rechazadas por el broker: "
            + (", ".join(f"{k} {v}" for k, v in sorted(rech.items())) or "ninguna")
            + f"; abiertas por la replica sin fila en el registro: {sin_registro[mes]}; con fila en"
            f" el registro y sin posicion de la replica: {registro_sin_replica[mes]}"
        )
    lineas += ["", "### Por mes"]
    for mes in sorted(meses):
        de_mes = [(o, r) for o, r in parejas if o.dia[:7] == mes]
        lineas += [
            f"#### {mes}",
            _fila_de_serie("registro", [o.r for o, _ in de_mes], tramos),
            _fila_de_serie("replica", [r for _, r in de_mes], tramos),
        ]
    lineas += ["", "### Por bloque"]
    brechas: dict[str, Decimal | None] = {}
    for nombre, meses_b in bloques.items():
        de_b = [(o, r) for o, r in parejas if o.dia[:7] in meses_b]
        b = brecha(media([o.r for o, _ in de_b]), media([r for _, r in de_b]))
        brechas[nombre] = b
        lineas += [
            f"#### {nombre} ({', '.join(meses_b)})",
            _fila_de_serie("registro", [o.r for o, _ in de_b], tramos),
            _fila_de_serie("replica", [r for _, r in de_b], tramos),
            f"brecha (media del registro menos media de la replica): {_r(b)}",
        ]
    rfr = y.premisa["registro_frente_a_replica"]
    margen = Decimal(rfr["margen_r"])
    diferencia = (
        None
        if brechas["enero_y_julio"] is None or brechas["abril_y_agosto"] is None
        else brechas["enero_y_julio"] - brechas["abril_y_agosto"]
    )
    lectura = lectura_de_5(
        brechas["enero_y_julio"], brechas["abril_y_agosto"], margen, rfr["lectura"]["orden"]
    )
    lineas += [
        "",
        f"brecha de enero_y_julio menos brecha de abril_y_agosto: {_r(diferencia)}; margen_r: "
        f"{margen}",
        f"LECTURA DE §5 (ADR-0100): {lectura}",
    ]
    return lineas, lectura, parejas


def medida_retroceso(
    ent: Any, y: Yamls, parejas: Sequence[tuple[OpRegistro, Decimal]]
) -> list[str]:
    """D6: el retroceso de las ganadoras del registro, por tramo y por bloque; solo recuentos."""
    from botsito.domain.velas import MinutoUtc

    tramos_r = _tramos_r(y)
    rg = y.premisa["registro_frente_a_replica"]["retroceso_de_las_ganadoras"]
    tramos = [Fraction(Decimal(t)) for t in rg["tramos"]]
    desfase = int(y.puente["propios"]["desfase_puntos"])
    spread = ent.config_llenado.spread_supuesto
    nombres = ["por_debajo", *nombres_de_tramos(tramos)]
    lineas = [
        "## §5 · El retroceso de las ganadoras del registro (sin lectura; solo recuentos)",
        f"entre el llenado del caso y dateEnd; ticks de Dukascopy (compra: BID minimo; venta: ASK "
        f"maximo) y, en los minutos sin ticks, la M1 de bid del respaldo; contra la entrada menos "
        f"desfase_puntos ({desfase}); en fracciones de D. «por_debajo»: no llego a la entrada.",
    ]
    for nombre, meses_b in _bloques(y).items():
        cuenta: Counter[str] = Counter()
        con_respaldo = extremo_respaldo = sin_datos = sin_nada = al_reves = 0
        ganadoras = [o for o, _ in parejas if o.dia[:7] in meses_b]
        ganadoras = [o for o in ganadoras if tramo_r(o.r, *tramos_r) == GANADORA]
        for o in ganadoras:
            md = ent.mercados[o.dia]
            mercado = md.mercado()
            if o.salida_ms < o.instante_ms:
                al_reves += 1
                continue
            ex = extremo_en_contra(
                o.direccion, o.instante_ms, o.salida_ms, mercado.ticks_del_minuto, mercado.m1,
                lambda m: int(spread(MinutoUtc(m))),
            )  # fmt: skip
            sin_datos += ex.minutos_sin_datos > 0
            if ex.precio is None:
                sin_nada += 1
                continue
            con_respaldo += ex.minutos_con_respaldo > 0
            extremo_respaldo += ex.del_respaldo
            entrada = tp.a_puntos(o.entrada, md.escala)
            d = abs(entrada - tp.a_puntos(o.stop, md.escala))
            cuenta[
                tramo_de_retroceso(retroceso(o.direccion, entrada, desfase, ex.precio, d), tramos)
            ] += 1
        lineas += [
            f"### {nombre} ({', '.join(meses_b)})",
            f"ganadoras del registro (R > {tramos_r[0]}): {len(ganadoras)}",
            "por tramo de retroceso: " + "; ".join(f"{n} {cuenta[n]}" for n in nombres),
            f"con algun minuto por el respaldo M1: {con_respaldo}; con el extremo en una M1 del "
            f"respaldo: {extremo_respaldo}; con algun minuto sin ticks ni M1: {sin_datos}; sin "
            f"ningun precio en el tramo: {sin_nada}; con dateEnd antes del llenado: {al_reves}",
        ]
    return lineas


def medida_lote_fijo(ent: Any, y: Yamls, corridas: Mapping[str, Any]) -> tuple[list[str], str]:
    """§6: el techo con lote fijo, base y todo_junto, sobre los cuatro meses y sobre abril y agosto
    con su propia mediana; la lectura de §4 solo para todo_junto sobre los cuatro meses."""
    from botsito.cases.criterio_fidelidad import PosicionCerrada, remuestreo_por_dias

    r = ent.criterio.rentabilidad
    alto_pct = int(y.meta["propios"]["percentil_alto"])
    alto_minimo = Decimal(y.meta["propios"]["techo_no_gana_si_percentil_alto_por_debajo_de_r"])
    orden = list(y.premisa["backtest_del_trader"]["lectura"]["orden"])
    meses_ay = _bloques(y)["abril_y_agosto"]
    lineas = [
        "## §6 · El techo con lote fijo (R neto x D / mediana de D, por posicion)",
        f"percentiles {r.percentil_remuestreo} y {alto_pct} por remuestreo por dias "
        f"({r.replicas_remuestreo} replicas, semilla {r.semilla_remuestreo}), con "
        "remuestreo_por_dias sobre posiciones de riesgo 1",
    ]
    lectura = ""
    for nombre, c in corridas.items():
        lineas += ["", f"### {nombre}"]
        for titulo, meses in (("los cuatro meses", None), ("abril y agosto", meses_ay)):
            filas = [f for f in c.filas if meses is None or f.dia[:7] in meses]
            dias = [d.dia for d in ent.dias if meses is None or d.dia[:7] in meses]
            dias = [x for x in dias if x in set(c.rep.trazas)]
            ds = [distancia_del_riesgo(ent, f) for f in filas]
            rs = r_con_lote_fijo([f.neto / f.riesgo for f in filas], ds)
            pos = [
                PosicionCerrada(f.dia, x, Decimal(1), False, "", Decimal(0), Decimal(0))
                for f, x in zip(filas, rs, strict=True)
            ]
            kw = {"replicas": r.replicas_remuestreo, "semilla": r.semilla_remuestreo}
            bajo, desc = remuestreo_por_dias(pos, dias, percentil=r.percentil_remuestreo, **kw)
            alto, _ = remuestreo_por_dias(pos, dias, percentil=alto_pct, **kw)
            esp = media(rs)
            mediana = mediana_de(ds) if ds else None
            lineas += [
                f"#### {titulo}",
                f"N {len(rs)}; mediana de D: {mediana} puntos; esperanza con lote fijo: {_r(esp)}; "
                f"media del R neto (por riesgo): {_r(media([f.neto / f.riesgo for f in filas]))}",
                f"percentil {r.percentil_remuestreo} y percentil {alto_pct} de la media, por "
                f"remuestreo por dias ({len(dias)} dias): {_r(bajo)} y {_r(alto)}; replicas "
                f"descartadas: {desc}",
            ]
            if nombre == "todo_junto" and meses is None:
                lectura = lectura_de_4(len(rs), esp, bajo, alto, r.n_minimo,
                                       r.esperanza_minima_r, alto_minimo, orden)  # fmt: skip
                lineas.append(f"LECTURA DE §4 CON LOTE FIJO (ADR-0100 §6): {lectura}")
            else:
                lineas.append("sin lectura (dato)")
    return lineas, lectura


# --------------------------------------------------------------------------- los modos


def _publicadas(nombre: str) -> list[str]:
    texto = PUBLICADAS_DEL_PUENTE[nombre].read_text(encoding="utf-8").splitlines()
    i = next(i for i, x in enumerate(texto) if x.startswith("## Variante "))
    return texto[i:]


def _escribir(ruta: Path, lineas: Sequence[str]) -> None:
    with ruta.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lineas).rstrip("\n") + "\n")


def modo_control(ent: Any, y: Yamls, carpeta: Path) -> int:
    lec = pt.lecturas_de(ent, y.meta, y.puente)
    variantes = {v.nombre: v for v in pt.variantes_del_yaml(y.puente)}
    lineas = ["# premisa.py control (ADR-0100; DIAGNOSTICO-PREMISA)", ""]
    vale_a = True
    for nombre in y.premisa["techo_con_lote_fijo"]["variantes"]:
        lineas_v, _cuatro, _ay = pt.correr_variante(ent, variantes[nombre], y.puente, lec)
        _escribir(carpeta / f"{nombre}-repetida.txt", lineas_v)
        publicadas = _publicadas(nombre)
        iguales = [x.rstrip() for x in lineas_v] == [x.rstrip() for x in publicadas]
        vale_a = vale_a and iguales
        lineas.append(
            f"D2 a · {nombre}: {len(lineas_v)} lineas regeneradas frente a {len(publicadas)} de "
            f"{PUBLICADAS_DEL_PUENTE[nombre].as_posix()} (desde «## Variante»): "
            + ("iguales" if iguales else "DIFIEREN")
        )
    lineas.append("D2 a: " + ("PASA" if vale_a else "NO PASA (PARADA en §6 y en la replica de §5)"))
    lineas.append("")
    reg = cargar_registro_del_trader(ent)
    vale_b, lineas_b = control_anotada(reg)
    lineas += lineas_b
    _escribir(carpeta / "control.txt", lineas)
    if not vale_a:
        return 4
    return 0 if vale_b else 5


def _contiene(publicadas: Sequence[str], propias: Sequence[str]) -> bool:
    """Las lineas propias estan, seguidas y tal cual, dentro de las publicadas."""
    a = [x.rstrip() for x in publicadas]
    b = [x.rstrip() for x in propias]
    return any(a[i : i + len(b)] == b for i in range(len(a) - len(b) + 1))


def modo_todo(ent: Any, y: Yamls, carpeta: Path) -> int:
    reg = cargar_registro_del_trader(ent)
    vale_b, lineas_b = control_anotada(reg)
    corridas = {n: corrida(ent, y.puente, n) for n in y.premisa["techo_con_lote_fijo"]["variantes"]}
    # D2 a otra vez, sobre ESTAS corridas: sus bloques de los cuatro meses y de abril y agosto,
    # con `pt.bloque`, tienen que estar tal cual en la salida de `main` de su variante
    lec = pt.lecturas_de(ent, y.meta, y.puente)
    meses_cierre = list(y.puente["cierre"]["meses"])
    lineas = ["# premisa.py todo (ADR-0100; DIAGNOSTICO-PREMISA)", ""]
    vale_a = True
    for nombre, c in corridas.items():
        propias = [
            *pt.bloque(ent, c, lec, None, "Los cuatro meses", True).lineas,
            *pt.bloque(
                ent, c, lec, meses_cierre, "Abril y agosto juntos (sin lectura)", False
            ).lineas,
        ]
        iguales = _contiene(_publicadas(nombre), propias)
        vale_a = vale_a and iguales
        lineas.append(
            f"D2 a · {nombre}: sus bloques de los cuatro meses y de abril y agosto ({len(propias)} "
            f"lineas), tal cual en {PUBLICADAS_DEL_PUENTE[nombre].as_posix()}: "
            + ("si" if iguales else "NO")
        )
    lineas += [
        "D2 a: " + ("PASA" if vale_a else "NO PASA (PARADA en §6 y en la replica de §5)"),
        "",
    ]
    lineas += [*lineas_b, ""]
    if not vale_a:
        _escribir(carpeta / "premisa.txt", lineas)
        return 4
    lectura_5 = "no se escribe: D2 b no pasa"
    if vale_b:
        l5, lectura_5, parejas = medida_5(ent, y, reg, corridas["todo_junto"])
        lineas += [*l5, "", *medida_retroceso(ent, y, parejas), ""]
    l6, lectura_6 = medida_lote_fijo(ent, y, corridas)
    lineas += l6
    _escribir(carpeta / "premisa.txt", lineas)
    _escribir(
        carpeta / "lectura.txt",
        [
            "# Las lecturas de ADR-0100, literales (premisa.py todo)",
            f"LECTURA DE §5 (ADR-0100): {lectura_5}",
            f"LECTURA DE §4 CON LOTE FIJO, todo_junto sobre los cuatro meses (ADR-0100 §6): "
            f"{lectura_6}",
        ],
    )
    return 0 if vale_b else 5


def main(argv: Sequence[str]) -> int:
    cast(Any, sys.stdout).reconfigure(encoding="utf-8", newline="\n")
    if len(argv) != 2 or argv[0] not in ("control", "todo"):
        print(__doc__)
        return 2
    carpeta = Path(argv[1])
    if not carpeta.is_dir():
        print(f"la carpeta de salida no existe: {carpeta}")
        return 2
    if Path.cwd().resolve() != RAIZ.resolve():
        print("el guion se lanza desde la raiz del repositorio")
        return 2
    y = cargar_los_yaml(RAIZ)
    ent = tp.entorno(RAIZ)
    return modo_control(ent, y, carpeta) if argv[0] == "control" else modo_todo(ent, y, carpeta)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
