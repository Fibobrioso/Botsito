"""El sesgo de H4 por el rango vigente (ADR-0094) POR EL CAMINO REAL: las H4 que el motor recibe
(`arnes.dias_de_mercado`, el mes y el anterior, por la compuerta de construccion) y los
parametros del registro, en dos sesiones de construccion en que el trader corrige al bot en la
sesion 7a (bloque de dias):

- 2026-07-07 de 11 a 15: «lo está definiendo bajista y aquí está mal nuestro sesgo no bajista
  porque tenemos que tener en cuenta que todavía no ha sido mitigado un sesgo que llevamos ya desde
  hace algunos días atrás» (ev-v18-004639-96f84da4; ev-v18-004718-01861c91);
- 2026-07-15 de 11 a 15: «… es considerable por eso ver si tienes un rango mayor y tratar de
  corregir eso antes de meterte a operar confirmar el rango» (ev-v19-004104-6d9d48cc).

Con la regla de antes (la H4 previa contra su anterior, ADR-0080) el bot daba BAJISTA en las dos
(rn003 de la corrida de julio, ACTIVAR-SESION-07.md, 0.2); el trader, ALCISTA. Rompen en `main`.

Necesita las M1 de `data/`, fuera de git: sin ellas (la CI), se salta."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.config.ajustes import carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.data.dataset import DatasetError
from botsito.domain.sesgo import Sesgo, sesgo_h4
from botsito.engine import arnes
from botsito.engine.relojes import reloj_de_las_sesiones

RAIZ = Path(__file__).resolve().parents[2]


def _sesgo(dia: str, sesion: str) -> Sesgo:
    criterio = cargar_criterio(RAIZ)
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    reloj = reloj_de_las_sesiones(registro)
    dias = [d for d in arnes.dias_de_construccion(RAIZ, criterio, [dia[:7]]) if d.dia == dia]
    assert len(dias) == 1, f"{dia} no es un dia dev de construccion"
    try:
        mercado = arnes.dias_de_mercado(RAIZ, carpeta_datos(RAIZ), config, registro, dias, reloj)
    except (DatasetError, FileNotFoundError, OSError) as exc:
        pytest.skip(f"sin las M1 de data/: {exc}")
    desde = next(s.desde for s in config.sesiones if s.nombre == sesion)
    apertura = reloj.instante(date.fromisoformat(dia), desde)
    cerradas = mercado[dia].datos.velas_h4_cerradas(int(apertura))
    if not cerradas:
        pytest.skip("sin las M1 de data/")
    return sesgo_h4(
        cerradas,
        apertura,
        registro.entero("sesgo_h4_tope_velas"),
        registro.opcion("sesgo_h4_criterio_ruptura"),
        registro.opcion("sesgo_h4_rango_nuevo"),
    ).sesgo


@pytest.mark.parametrize("dia", ["2026-07-07", "2026-07-15"])
def test_el_rango_mayor_sin_mitigar_da_alcista_donde_el_trader_corrige_al_bot(dia: str) -> None:
    assert _sesgo(dia, "11-15") is Sesgo.ALCISTA
