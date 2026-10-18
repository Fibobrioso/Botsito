"""Medida 1 de MARGEN-LOTE.md (fase 1): que parte de las operaciones del trader de los dias dev de
construccion tiene un stop tan corto que el lote del riesgo no cabe en el margen (1:30) ni en el
volumen maximo de la firma; y, si se da un calendario, cuantas caen a +-N minutos de una noticia.
Hermano de anexos/ENTRADA-JULIO/margen_p_d1.py: lee el registro y el perfil y no lleva ninguna
cifra dentro; los precios de referencia y la ventana de minutos llegan por argumento. Solo mide.

Uso: uv run python docs/validation/anexos/MARGEN-LOTE/stops_cortos.py --precios 1.10 1.20
         [--noticias <csv> --ventana-min 2]

Las operaciones se leen POR LA MISMA VIA QUE EL ARNES: `arnes.dias_de_construccion` (la compuerta:
veta cualquier caso oculto) sobre los meses de `construccion` del criterio, y el stop de cada
operacion por `visor._stops`, como `simulacion._del_trader`. Antes de leer, `casos_reservados`
cuenta por mes y se niega a seguir si un mes de construccion tiene un caso reservado.

El caso trae ENTRADA y STOP, no la caja. D = |entrada - stop| en pips (10 puntos de 0,00001,
ADR-0071 §2). Donde puso el trader el stop de su libro es lo que mide A-56 (ABIERTA), asi que se
cuentan las DOS lecturas, con el supuesto delante de cada tabla:
- lectura «stop del libro = el 1 de la caja» (la de VIABILIDAD-COMISION.md): distancia 0->1 = D,
  distancia del lote (0->0,8) = stop_fraccion_caja x D;
- lectura «stop del libro = el 0,8»: distancia del lote = D, distancia 0->1 = D /
  stop_fraccion_caja.
Los umbrales salen del registro y del perfil: el stop minimo que admite el tope de volumen
(riesgo / (valor del pip x firma_volumen_max_lotes)) y el stop minimo que admite el margen con todo
el saldo inicial como margen a cada precio de referencia (riesgo / (valor del pip x lote maximo)),
ademas del precio de la propia entrada de cada operacion (lo exacto). Se imprimen solo recuentos y
agregados por mes: ninguna fecha de operacion, ningun precio de una operacion.

El calendario de noticias (opcional): CSV con cabecera y columnas `fecha_utc,hora_utc,divisa,evento`
(hora HH:MM); solo se cuenta cuantas operaciones tienen su instante a +-ventana minutos de alguna
fila. Su sha256 se imprime para el informe.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from datetime import UTC, datetime, timedelta
from decimal import ROUND_DOWN, Decimal
from pathlib import Path
from statistics import median

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.holdout import casos_reservados  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.engine import arnes  # noqa: E402
from botsito.engine.visor import _stops  # noqa: E402

PIP = Decimal("0.0001")  # 10 puntos de 0,00001 (ADR-0071 §2)
PERFIL = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"


def _noticias(ruta: Path) -> list[datetime]:
    instantes: list[datetime] = []
    with ruta.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f):
            instantes.append(
                datetime.fromisoformat(f"{fila['fecha_utc']}T{fila['hora_utc']}").replace(
                    tzinfo=UTC
                )
            )
    return instantes


def main(precios: list[Decimal], noticias: Path | None, ventana_min: int) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    spec = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    perfil = cargar_registro(PERFIL)
    criterio = cargar_criterio(RAIZ)
    riesgo_pct = spec.porcentaje("riesgo_por_operacion").valor
    fraccion = spec.fraccion("stop_fraccion_caja").valor
    contrato = spec.decimal("instrumento_contrato")
    paso = spec.lotes("instrumento_lote_paso")
    saldo = perfil.decimal("saldo_inicial_cuenta")
    apalancamiento = perfil.entero("firma_apalancamiento")
    vol_max = perfil.lotes("firma_volumen_max_lotes")
    riesgo_usd = saldo * riesgo_pct / 100
    valor_pip = contrato * PIP
    meses = tuple(criterio.construccion)

    # la puerta, antes de leer: ningun caso reservado en los meses de construccion
    reservados = Counter(c[-10:-3] for c in casos_reservados(RAIZ))
    for mes in meses:
        if reservados.get(mes, 0):
            print(f"PARADA: {mes} tiene {reservados[mes]} casos reservados; no se lee")
            return 2
    print(
        f"PARAMETROS: saldo {saldo} USD; riesgo_por_operacion {riesgo_pct} % = {riesgo_usd} USD; "
        f"stop_fraccion_caja {fraccion}; instrumento_contrato {contrato}; paso {paso}; "
        f"firma_apalancamiento 1:{apalancamiento}; firma_volumen_max_lotes {vol_max}; "
        f"valor del pip "
        f"{valor_pip} USD por lote; meses de construccion {', '.join(meses)}; casos reservados en "
        f"ellos: 0 (reservados en total {sum(reservados.values())})"
    )
    stop_vol = riesgo_usd / (valor_pip * vol_max)
    umbrales: dict[str, Decimal] = {f"volumen ({vol_max} lotes): {stop_vol:.2f} pips": stop_vol}
    for precio in precios:
        lote_max = (saldo * apalancamiento / (contrato * precio)).quantize(paso, ROUND_DOWN)
        stop_min = riesgo_usd / (valor_pip * lote_max)
        umbrales[f"margen a {precio} ({lote_max} lotes): {stop_min:.2f} pips"] = stop_min
    print(
        "UMBRALES (stop minimo con el que el lote del riesgo todavia cabe): " + "; ".join(umbrales)
    )

    dias = arnes.dias_de_construccion(RAIZ, criterio, meses)
    instantes_noticias = _noticias(noticias) if noticias is not None else None
    if noticias is not None:
        print(
            f"NOTICIAS: {noticias.name} sha256 "
            f"{hashlib.sha256(noticias.read_bytes()).hexdigest()}; "
            f"{len(instantes_noticias or [])} filas; ventana +-{ventana_min} min"
        )
    por_mes_d: dict[str, list[Decimal]] = defaultdict(list)  # D en pips
    por_mes_precio: dict[str, list[Decimal]] = defaultdict(list)
    por_mes_noticia: Counter[str] = Counter()
    for dt in dias:
        for op, stop in zip(dt.operaciones, _stops(RAIZ, dt), strict=True):
            if stop is None:
                continue
            d_pips = abs(op.entrada - stop) / PIP
            por_mes_d[dt.dia[:7]].append(d_pips)
            por_mes_precio[dt.dia[:7]].append(op.entrada)
            if instantes_noticias is not None:
                ventana = timedelta(minutes=ventana_min)
                if any(abs(op.instante - n) <= ventana for n in instantes_noticias):
                    por_mes_noticia[dt.dia[:7]] += 1
    total_d = [d for mes in meses for d in por_mes_d[mes]]
    print(
        f"OPERACIONES con stop en el caso: {len(total_d)} ("
        + ", ".join(f"{mes} {len(por_mes_d[mes])}" for mes in meses)
        + ")"
    )

    lecturas = {
        "A: el stop del libro es el 1 de la caja (VIABILIDAD-COMISION): lote sobre fraccion x D": (
            lambda d: d * fraccion,
            lambda d: d,
        ),
        "B: el stop del libro es el 0,8: lote sobre D": (lambda d: d, lambda d: d / fraccion),
    }
    for titulo, (del_lote, del_uno) in lecturas.items():
        print(f"LECTURA {titulo}")
        print(
            "  mes | n | mediana lote (pips) | mediana 0->1 (pips) | "
            + " | ".join(f"lote < {u}" for u in umbrales)
            + " | lote < margen al precio de la entrada | "
            + " | ".join(f"0->1 < {u}" for u in umbrales)
        )
        acumulado: Counter[str] = Counter()
        n_total = 0
        for mes in meses:
            ds = por_mes_d[mes]
            if not ds:
                continue
            lotes_d = [del_lote(d) for d in ds]
            unos_d = [del_uno(d) for d in ds]
            fila = [mes, str(len(ds)), f"{median(lotes_d):.2f}", f"{median(unos_d):.2f}"]
            for clave, u in umbrales.items():
                n = sum(1 for x in lotes_d if x < u)
                acumulado[f"lote<{clave}"] += n
                fila.append(f"{n} ({100 * n / len(ds):.0f} %)")
            # el margen al precio de la propia entrada: lote_max(P) con todo el saldo como margen
            n_exacto = 0
            for x, precio in zip(lotes_d, por_mes_precio[mes], strict=True):
                lote_max = (saldo * apalancamiento / (contrato * precio)).quantize(paso, ROUND_DOWN)
                if x < riesgo_usd / (valor_pip * lote_max):
                    n_exacto += 1
            acumulado["exacto"] += n_exacto
            fila.append(f"{n_exacto} ({100 * n_exacto / len(ds):.0f} %)")
            for clave, u in umbrales.items():
                n = sum(1 for x in unos_d if x < u)
                acumulado[f"uno<{clave}"] += n
                fila.append(f"{n} ({100 * n / len(ds):.0f} %)")
            n_total += len(ds)
            print("  " + " | ".join(fila))
        if n_total:
            fila = [
                "total",
                str(n_total),
                f"{median([del_lote(d) for d in total_d]):.2f}",
                f"{median([del_uno(d) for d in total_d]):.2f}",
            ]
            for clave in umbrales:
                n = acumulado[f"lote<{clave}"]
                fila.append(f"{n} ({100 * n / n_total:.0f} %)")
            fila.append(f"{acumulado['exacto']} ({100 * acumulado['exacto'] / n_total:.0f} %)")
            for clave in umbrales:
                n = acumulado[f"uno<{clave}"]
                fila.append(f"{n} ({100 * n / n_total:.0f} %)")
            print("  " + " | ".join(fila))
    if instantes_noticias is not None:
        print(
            f"NOTICIAS a +-{ventana_min} min: "
            + ", ".join(f"{mes} {por_mes_noticia[mes]}" for mes in meses)
            + f"; total {sum(por_mes_noticia.values())}"
        )
    else:
        print("NOTICIAS: sin calendario (no se da --noticias); la medida queda sin fuente")
    return 0


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--precios", type=Decimal, nargs="+", required=True)
    p.add_argument("--noticias", type=Path)
    p.add_argument("--ventana-min", type=int, default=None)
    p.add_argument(
        "--escribir", type=Path, help="ademas de la pantalla, el mismo texto a este fichero"
    )
    a = p.parse_args()
    if (a.noticias is None) != (a.ventana_min is None):
        p.error("--noticias y --ventana-min van juntos")
    if a.escribir is not None:
        import io

        buffer = io.StringIO()
        real = sys.stdout
        sys.stdout = buffer  # type: ignore[assignment]
        codigo = main(a.precios, a.noticias, a.ventana_min or 0)
        sys.stdout = real
        a.escribir.write_text(buffer.getvalue(), encoding="utf-8")
        print(buffer.getvalue(), end="")
        raise SystemExit(codigo)
    raise SystemExit(main(a.precios, a.noticias, a.ventana_min or 0))
