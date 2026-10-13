"""Fase 6 de ENTRADA-JULIO.md (FTMO-P-D1.md): el lote maximo que cabe en el margen y el stop minimo
con el que el riesgo por operacion todavia se cumple. Solo aritmetica; no cambia nada.

La formula de margen de forex de MetaTrader 5 («Volume in lots * Contract size / Leverage», en la
divisa de margen, que para EURUSD es el EUR, convertida a USD con el precio: el Ask en una compra y
el Bid en una venta; documentacion de MT5, «Margin Calculation for Retail Forex, Futures»):

    margen_USD = lotes * instrumento_contrato * precio / firma_apalancamiento

Con TODO el saldo como margen, lote_max = saldo * apalancamiento / (contrato * precio). Y el lote
que pide el riesgo es riesgo_USD / (stop_pips * valor_pip_por_lote), asi que el stop minimo con el
que ese lote cabe es riesgo_USD / (valor_pip_por_lote * lote_max).

Las cifras salen del registro (`knowledge/spec/parametros.yaml`: riesgo_por_operacion,
instrumento_contrato) y del perfil de la cuenta (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`:
saldo_inicial_cuenta, firma_apalancamiento, firma_volumen_max_lotes). Un pip de EURUSD son 10
puntos de 0,00001 (ADR-0071 §2), y el lote se redondea hacia abajo al paso del instrumento.
Los precios, 1,10 y 1,20, son los del encargo.

    uv run python docs/validation/anexos/ENTRADA-JULIO/margen_p_d1.py
"""

from __future__ import annotations

import sys
from decimal import ROUND_DOWN, Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.config.registro import cargar_registro  # noqa: E402

PRECIOS = (Decimal("1.10"), Decimal("1.20"))
PIP = Decimal("0.0001")  # 10 puntos de 0,00001 (ADR-0071 §2)


def main() -> int:
    spec = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    perfil = cargar_registro(RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml")
    riesgo_pct = spec.porcentaje("riesgo_por_operacion").valor
    contrato = spec.decimal("instrumento_contrato")
    paso = spec.lotes("instrumento_lote_paso")
    saldo = perfil.decimal("saldo_inicial_cuenta")
    apalancamiento = perfil.entero("firma_apalancamiento")
    vol_max = perfil.lotes("firma_volumen_max_lotes")
    riesgo_usd = saldo * riesgo_pct / 100
    valor_pip = contrato * PIP  # USD por lote y pip: EURUSD cotiza en USD
    print(
        f"PARAMETROS: saldo {saldo} USD; riesgo_por_operacion {riesgo_pct} % = {riesgo_usd} USD; "
        f"instrumento_contrato {contrato}; paso {paso}; firma_apalancamiento 1:{apalancamiento}; "
        f"firma_volumen_max_lotes {vol_max}; valor del pip {valor_pip} USD por lote"
    )
    stop_vol = riesgo_usd / (valor_pip * vol_max)
    print(f"TOPE DE VOLUMEN ({vol_max} lotes): stop minimo {stop_vol:.2f} pips")
    for precio in PRECIOS:
        lote_max = (saldo * apalancamiento / (contrato * precio)).quantize(paso, ROUND_DOWN)
        margen_1 = contrato * precio / apalancamiento
        stop_min = riesgo_usd / (valor_pip * lote_max)
        print(
            f"PRECIO {precio}: margen de 1,00 lote {margen_1:.2f} USD; lote maximo con todo el "
            f"saldo como margen {lote_max}; stop minimo para el {riesgo_pct} % {stop_min:.2f} pips"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
