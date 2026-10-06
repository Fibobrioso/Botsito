"""M1 de RELOJ-INVIERNO.md: el huso del libro de ENERO de 2026, medido por velas (ADR-0039 §5).

Es el procedimiento de `knowledge/corpus/libros.yaml` tal cual, con las funciones de
`scripts/huso_por_velas.py` (codigo de `main`) y sus cifras de `knowledge/corpus/criterio_huso.yaml`:
entrada dentro de [minima - 2, maxima + 2] puntos de la M1 de Dukascopy del minuto, UTC frente a
Europe/Madrid, decide un huso si da >= 0.90 y el otro <= 0.50.

Lo UNICO que cambia respecto de la herramienta, y por que:

- **Los dias.** La herramienta mide los dias `dev` de los repartos commiteados, y enero no tiene
  NINGUNO (no esta en ningun reparto: es material de desarrollo sin sortear), asi que con ella no
  hay nada que medir. Aqui se piden TODOS los dias del mes, despues de comprobar con
  `casos_ocultos` y `casos_reservados` que ninguno de ese mes esta en una particion, y con
  `meses_reservados.yaml` que el mes no esta reservado entero. Si alguno lo esta, sale con error
  sin leer el libro.
- **Un tercer candidato, Etc/GMT-2, SOLO como dato** (encargo): se cuenta igual, con el mismo
  margen, sobre las filas comparables entre UTC y Etc/GMT-2, y NO entra en el veredicto, que es el
  de §5 entre los dos husos del criterio.
- **El control** se hace dos veces: con la herramienta de `main` tal cual (dias `dev`), fuera de
  este guion, y aqui con el MISMO metodo que enero (todos los dias del mes) sobre ABRIL y AGOSTO,
  ya declarados en UTC. Si aqui el veredicto de un control no coincide con su huso declarado, el
  metodo no sirve y sale con codigo 3.

Lee del libro SOLO `dateStart` y `entryPrice`, por el lector unico (`corpus.libro`), con una
declaracion EN MEMORIA por huso. Imprime SOLO recuentos y tasas: ni fechas, ni instantes, ni precios.

    uv run python docs/validation/anexos/RELOJ-INVIERNO/huso_enero.py
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))
sys.path.insert(0, str(RAIZ / "scripts"))

import huso_por_velas as hpv  # noqa: E402
from botsito.cases.fidelidad import cargar_config  # noqa: E402
from botsito.cases.holdout import (  # noqa: E402
    cargar_meses_reservados,
    casos_ocultos,
    casos_reservados,
)
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.corpus.libro import PESTANA_OPERACIONES, LibroError, filas_de_los_dias  # noqa: E402
from botsito.corpus.libros import FORMATOS, Declaracion, Lectura, cargar_libros, sha256_de  # noqa: E402
from botsito.data.dataset import buscar_manifiesto, cargar_manifiesto, cargar_serie  # noqa: E402
from botsito.data.velas import a_minuto  # noqa: E402

# Rutas LITERALES y enteras, una por libro: la guardia de Claude Code no deja ejecutar un guion que
# nombre la carpeta del material adicional sin decir que fichero abre dentro.
LIBROS = {
    "2026-01": "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ENERO 2026.xlsx",  # noqa: E501
    "2026-04": "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ABRIL 2026.xlsx",  # noqa: E501
    "2026-08": "corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics AGOSTO 2026.xlsx",  # noqa: E501
}
# El tercer candidato, solo como dato (encargo de trabajo/reloj-invierno, M1).
TERCERO = "Etc/GMT-2"


def dias_del_mes(mes: str) -> set[str]:
    """Todos los dias del mes, si NINGUNO esta en una particion y el mes no esta reservado."""
    ocupados = [c for c in set(casos_ocultos(RAIZ)) | set(casos_reservados(RAIZ)) if f"-{mes}-" in c]
    if ocupados:
        raise SystemExit(f"ERROR: {mes} tiene {len(ocupados)} casos en particiones: no se lee")
    if mes in cargar_meses_reservados(RAIZ):
        raise SystemExit(f"ERROR: {mes} esta en meses_reservados.yaml: no se lee")
    anio, m = (int(x) for x in mes.split("-"))
    d = date(anio, m, 1)
    dias: set[str] = set()
    while d.month == m:
        dias.add(d.isoformat())
        d += timedelta(days=1)
    return dias


def leer(libro: Path, dias: set[str], formato: str, huso: str, huso_dias: str) -> list[dict]:
    hipotesis = Declaracion(sha256_de(libro), (Lectura(formato, huso),))
    return filas_de_los_dias(
        libro, dias, PESTANA_OPERACIONES, hpv.COLUMNAS, hipotesis, huso_de_los_dias=huso_dias
    )


def formato_de(libro: Path, dias: set[str], huso_dias: str) -> str:
    """El formato que casa con TODAS las filas: se prueba cada uno del vocabulario. Un error del
    lector no dice ni valor ni posicion, asi que de aqui sale solo el nombre del formato."""
    validos = []
    for formato in FORMATOS:
        try:
            leer(libro, dias, formato, "UTC", huso_dias)
        except LibroError:
            continue
        validos.append(formato)
    if len(validos) != 1:
        raise SystemExit(f"ERROR: formatos que casan con todas las filas: {len(validos)}")
    return validos[0]


def main() -> int:
    criterio = hpv.cargar_criterio(RAIZ)
    huso_dias = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml").texto(
        "huso_operativa"
    )
    declarados = cargar_libros(RAIZ)
    datos = carpeta_datos(RAIZ)
    prefijo = cargar_config(RAIZ).dataset_prefijo
    series: dict[str, tuple[dict[int, hpv.Rango], str]] = {}

    def vela_de(instante):
        mes = instante.strftime("%Y-%m")
        if mes not in series:
            ruta = buscar_manifiesto(RAIZ, f"{prefijo}{mes}")
            s = cargar_serie(cargar_manifiesto(ruta), datos)
            series[mes] = (
                {int(v.inicio): hpv.Rango(int(v.minima), int(v.maxima), s.escala) for v in s.velas},
                ruta.stem,
            )
        return series[mes][0].get(int(a_minuto(instante)))

    print(
        f"CRITERIO: {hpv.FICHERO_CRITERIO} (margen {criterio.margen_puntos} puntos; decide >= "
        f"{criterio.umbral_decide} y el otro <= {criterio.umbral_otro}; husos "
        f"{list(criterio.husos)}); tercero, solo dato: {TERCERO}"
    )
    print(f"DIAS: todos los del mes, en {huso_dias} (huso_operativa)")
    codigo = 0
    for mes, rel in LIBROS.items():
        libro = RAIZ / rel
        sha = sha256_de(libro)
        dias = dias_del_mes(mes)
        decl = declarados.get(sha)
        if decl is None:
            formato, declarado = formato_de(libro, dias, huso_dias), None
        else:
            (formato,) = {lec.formato for lec in decl.lecturas}
            (declarado,) = {lec.huso for lec in decl.lecturas}
        husos = (*criterio.husos, TERCERO)
        lecturas = {h: leer(libro, dias, formato, h, huso_dias) for h in husos}
        comp = hpv.comparables(lecturas, criterio.husos)
        cuenta = hpv.medir(comp.filas, vela_de, criterio)
        veredicto = hpv.decidir(cuenta, criterio)
        # El tercero: las filas comparables entre UTC y el tercero, contadas igual.
        par = hpv.Criterio(criterio.margen_puntos, ("UTC", TERCERO), criterio.umbral_decide,
                           criterio.umbral_otro)
        comp3 = hpv.comparables(lecturas, par.husos)
        cuenta3 = hpv.medir(comp3.filas, vela_de, par)
        print(f"\n== {mes}: libro {sha[:12]}... formato {formato!r}; "
              f"declarado: {declarado or 'NO (sin entrada en libros.yaml)'}")
        print(f"FILAS comparables: {len(comp.filas)}; sin entrada numerica: {comp.sin_entrada}; "
              f"descartadas por frontera de dia: {'si' if comp.frontera else 'no'}")
        for h in criterio.husos:
            d, n, s = cuenta[h]
            tasa = f"{Decimal(100 * d) / Decimal(n):.1f} %" if n else "-"
            print(f"{h}: {d}/{n} = {tasa}" + (f" ({s} sin vela)" if s else ""))
        d, n, s = cuenta3[TERCERO]
        tasa = f"{Decimal(100 * d) / Decimal(n):.1f} %" if n else "-"
        print(f"{TERCERO} (solo dato; {len(comp3.filas)} filas comparables con UTC): {d}/{n} = "
              f"{tasa}" + (f" ({s} sin vela)" if s else ""))
        print(f"VEREDICTO (ADR-0039 §5, entre {criterio.husos[0]} y {criterio.husos[1]}): {veredicto}")
        if declarado is not None:
            coincide = veredicto == declarado
            print(f"CONTROL: declarado {declarado} -> "
                  f"{'COINCIDE' if coincide else 'NO COINCIDE: el metodo no sirve'}")
            if not coincide:
                codigo = hpv.CONTROL_FALLA
    print(f"\nDATASETS: {', '.join(series[m][1] for m in sorted(series))}")
    return codigo


if __name__ == "__main__":
    raise SystemExit(main())
