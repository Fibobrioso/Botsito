"""DIAGNOSTICO del sesgo H4 (RN-003, ADR-0044) sobre los casos de CONSTRUCCION: abril y agosto.

Documento: `docs/validation/MOTOR-SESGO-H4.md`. NO es una medida de fidelidad (ADR-0043): no hay
umbral y no se cambia la regla por lo que salga. Por cada operacion del trader, el sesgo del bot AL
ABRIR SU SESION frente a la direccion de la operacion: a favor, en contra, ambiguo o insuficiente;
y aparte, cuantas de las rupturas que fijaron el sesgo son de 1-2 puntos, la zona de A-16.

**MAYO NO SE TOCA**: es el conjunto de MEDIDA (ADR-0043). La lista de meses es cerrada y el script
se niega a cualquier otro.

  `uv run python scripts/sesgo_h4_diagnostico.py --salida <fichero>`

Lee los `caso-*.yaml` de esos dos meses y las velas M1 del mes y del anterior, cuando existe, para
el calentamiento del sesgo (ADR-0043: leer velas no es abrir casos). Imprime SOLO recuentos.
"""

from __future__ import annotations

import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[1]
CONSTRUCCION = ("2026-04", "2026-08")
ZONA_A16 = (1, 2)
A_FAVOR = {("compra", "alcista"), ("venta", "bajista")}


def mes_anterior(mes: str) -> str:
    anio, m = int(mes[:4]), int(mes[5:])
    return f"{anio - 1}-12" if m == 1 else f"{anio}-{m - 1:02d}"


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--salida":
        print("uso: sesgo_h4_diagnostico.py --salida <fichero>", file=sys.stderr)
        return 2
    sys.path.insert(0, str(RAIZ / "src"))
    from botsito.cases.paquete import cargar_config
    from botsito.comun.yaml_estricto import leer_yaml
    from botsito.config.ajustes import carpeta_datos
    from botsito.config.registro import cargar_registro
    from botsito.data.agregacion import agregar
    from botsito.data.dataset import (
        DatasetError,
        buscar_manifiesto,
        cargar_manifiesto,
        cargar_serie,
    )
    from botsito.data.velas import a_minuto
    from botsito.domain.sesgo import Sesgo, sesgo_h4

    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    anclaje = registro.hora("anclaje_h4")
    tope = registro.entero("sesgo_h4_tope_velas")
    criterio = registro.opcion("sesgo_h4_criterio_ruptura")
    huso = ZoneInfo(registro.texto("huso_operativa"))
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    apertura_de = {s.nombre: s.desde for s in config.sesiones}
    datos = carpeta_datos(RAIZ)

    lineas: list[str] = []
    total: Counter[str] = Counter()
    for mes in CONSTRUCCION:
        leidos, m1 = [], []
        for m in (mes_anterior(mes), mes):
            try:
                ruta = buscar_manifiesto(RAIZ, f"eurusd-m1-{m}")
            except DatasetError:
                continue  # sin dataset del mes anterior, el calentamiento empieza en el mes
            m1 += list(cargar_serie(cargar_manifiesto(ruta), datos).velas)
            leidos.append(ruta.stem)
        velas_h4 = agregar(m1, 240, anclaje)
        cuenta: Counter[str] = Counter()
        for f in sorted((RAIZ / "knowledge" / "cases" / "dev").glob(f"caso-*-{mes}-*.yaml")):
            caso = leer_yaml(f)
            if str(caso["dia"])[:7] not in CONSTRUCCION:
                raise SystemExit("un caso fuera de construccion: este diagnostico no lo lee")
            for op in caso["operaciones"]:
                local = datetime.fromisoformat(f"{caso['dia']}T{apertura_de[op['sesion']]}:00")
                apertura = a_minuto(local.replace(tzinfo=huso).astimezone(ZoneInfo("UTC")))
                r = sesgo_h4(velas_h4, apertura, tope, criterio)
                if r.sesgo in (Sesgo.AMBIGUO, Sesgo.INSUFICIENTE):
                    clase = r.sesgo.value
                elif (op["direccion"], r.sesgo.value) in A_FAVOR:
                    clase = "a favor"
                else:
                    clase = "en contra"
                cuenta[clase] += 1
                cuenta["operaciones"] += 1
                if r.ruptura_puntos in ZONA_A16:
                    cuenta["ruptura de 1-2 puntos (zona A-16)"] += 1
        total.update(cuenta)
        lineas.append(f"{mes} (velas: {', '.join(leidos)}): {_formato(cuenta)}")
    lineas.append(f"total: {_formato(total)}")
    cabecera = [
        f"PARAMETROS: anclaje_h4 {anclaje.hora} {anclaje.huso}; sesgo_h4_tope_velas {tope}; "
        f"sesgo_h4_criterio_ruptura {criterio}",
        "CONJUNTO: construccion (abril y agosto). Mayo no se lee.",
    ]
    Path(argv[1]).write_text("\n".join([*cabecera, *lineas]) + "\n", encoding="utf-8", newline="\n")
    return 0


def _formato(c: Counter[str]) -> str:
    orden = ["operaciones", "a favor", "en contra", "ambiguo", "insuficiente"]
    partes = [f"{k} {c[k]}" for k in orden]
    partes.append(
        f"de ellas con ruptura de 1-2 puntos (zona A-16) {c['ruptura de 1-2 puntos (zona A-16)']}"
    )
    return "; ".join(partes)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
