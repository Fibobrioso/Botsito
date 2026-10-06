"""M2 de RELOJ-INVIERNO.md: a que horas UTC entra el trader en ENERO, con control en abril y agosto.

La regla, escrita en el encargo ANTES de medir (docs/encargos/trabajo-reloj-invierno.md, M2):
  - H2 si hay >= 3 en [13:00, 14:00) y 0 en [05:00, 06:00);
  - H1 si hay >= 3 en [05:00, 06:00) y 0 en [13:00, 14:00);
  - cualquier otra cosa, NO CONCLUYENTE.
Se aplica SOLO a enero. Abril y agosto son el control: en verano H1 y H2 predicen las dos
[05:00, 13:00) UTC, y si el control tiene entradas en [13:00, 14:00) se dice ANTES del veredicto
de enero, porque la regla dejaria de discriminar.

Las cifras de la regla son del encargo, no parametros del registro: son el criterio de UNA medida,
congelado antes de medirla, y no se reutilizan (como los umbrales pre-registrados de los informes).

El huso de cada libro: abril y agosto, el DECLARADO en `knowledge/corpus/libros.yaml`; enero, el
que dio M1, que se pasa con --huso-enero y tiene que estar declarado YA en libros.yaml para ese sha
(M1 solo lo declara si sale concluyente; si no, M2 no se ejecuta y este guion se niega).

Lee del libro SOLO `dateStart`, de todos los dias del mes, tras comprobar que ninguno esta en una
particion. Imprime SOLO horas y recuentos: ni entradas, ni stops, ni resultados, ni R, ni PnL.

    uv run python docs/validation/anexos/RELOJ-INVIERNO/horas_enero.py
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from huso_enero import LIBROS, dias_del_mes  # noqa: E402  (mismo directorio)

from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.corpus.libro import PESTANA_OPERACIONES, filas_de_los_dias  # noqa: E402
from botsito.corpus.libros import cargar_libros, sha256_de  # noqa: E402

MES_REGLA = "2026-01"
TEMPRANA = (time(5, 0), time(6, 0))  # [05:00, 06:00) UTC
TARDIA = (time(13, 0), time(14, 0))  # [13:00, 14:00) UTC
DENTRO = (time(5, 0), time(14, 0))  # [05:00, 14:00) UTC
MINIMO = 3


def en(t: time, franja: tuple[time, time]) -> bool:
    return franja[0] <= t < franja[1]


def veredicto(tempranas: int, tardias: int) -> str:
    if tardias >= MINIMO and tempranas == 0:
        return "H2"
    if tempranas >= MINIMO and tardias == 0:
        return "H1"
    return "NO CONCLUYENTE"


def main() -> int:
    huso_dias = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml").texto(
        "huso_operativa"
    )
    declarados = cargar_libros(RAIZ)
    resultado: dict[str, tuple[int, int]] = {}
    orden = [m for m in LIBROS if m != MES_REGLA] + [MES_REGLA]  # el control, ANTES que enero
    for mes in orden:
        libro = RAIZ / LIBROS[mes]
        sha = sha256_de(libro)
        decl = declarados.get(sha)
        if decl is None:
            raise SystemExit(
                f"ERROR: el libro de {mes} no esta declarado en libros.yaml: M1 no salio "
                f"concluyente o no se declaro, y M2 no se ejecuta"
            )
        filas = filas_de_los_dias(
            libro, dias_del_mes(mes), PESTANA_OPERACIONES, ("dateStart",), decl,
            huso_de_los_dias=huso_dias,
        )
        instantes = sorted(datetime.fromisoformat(str(f["_instante_utc"])) for f in filas)
        horas = [i.time() for i in instantes]
        tempranas = sum(en(t, TEMPRANA) for t in horas)
        tardias = sum(en(t, TARDIA) for t in horas)
        fuera = [i for i in instantes if not en(i.time(), DENTRO)]
        husos = sorted({lec.huso for lec in decl.lecturas})
        papel = "REGLA" if mes == MES_REGLA else "CONTROL"
        print(f"\n== {mes} ({papel}): libro {sha[:12]}..., leido en {', '.join(husos)} "
              f"(libros.yaml); entradas: {len(instantes)}")
        por_hora = Counter(i.hour for i in instantes)
        print("por hora UTC [h, h+1): " + ", ".join(f"{h:02d}h {por_hora[h]}" for h in sorted(por_hora)))
        print(f"en [05:00, 06:00) UTC: {tempranas}")
        print(f"en [13:00, 14:00) UTC: {tardias}")
        print(f"fuera de [05:00, 14:00) UTC: {len(fuera)}"
              + "".join(f"\n  {i:%Y-%m-%d %H:%M:%S} UTC" for i in fuera))
        resultado[mes] = (tempranas, tardias)
    print()
    controles_tardios = [m for m in resultado if m != MES_REGLA and resultado[m][1] > 0]
    if controles_tardios:
        print(f"AVISO ANTES DEL VEREDICTO: el control tiene entradas en [13:00, 14:00) UTC en "
              f"{', '.join(controles_tardios)}: la regla deja de discriminar")
    else:
        print("CONTROL: ninguna entrada en [13:00, 14:00) UTC en abril ni en agosto")
    t, d = resultado[MES_REGLA]
    print(f"== VEREDICTO M2 (regla del encargo, enero): {veredicto(t, d)} "
          f"([05,06): {t}; [13,14): {d}; minimo {MINIMO})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
