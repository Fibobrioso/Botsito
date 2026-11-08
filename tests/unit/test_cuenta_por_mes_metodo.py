"""Las piezas puras de `criterio_fidelidad.py` que trae `trabajo/cuenta-por-mes` (ADR-0092 §8; D5
del encargo): `medir_por_cuentas` y el motivo de f) con una cuenta o con varias (PARADA condicional
2 de CUENTA-POR-MES.md). Van aparte de `test_cuenta_por_mes.py` para que ese fichero se pueda correr
con el codigo de `main` (respuesta al revisor, a4 y b1): este, en `main`, falla al importar, porque
lo que prueba no existe alli."""

from __future__ import annotations

import dataclasses
from decimal import Decimal
from fractions import Fraction

from botsito.cases.criterio_fidelidad import (
    BASE_SALDO_CORTE,
    NO_PASA,
    CuentaDelTramo,
    MedidaRentabilidad,
    cargar_criterio,
    equity_minima_del_tramo,
    medir_por_cuentas,
    perdida_diaria_maxima,
    veredicto_rentabilidad,
)
from tests.unit import test_cableado as tc

_RENT = cargar_criterio(tc.RAIZ).rentabilidad
assert _RENT is not None
RENT = _RENT
CAPITAL = Decimal(100_000)


def _cuenta(mes: str, minima: str, suspendida: bool = False) -> CuentaDelTramo:
    dia = f"{mes}-15"
    return CuentaDelTramo(mes, ((dia, CAPITAL, Decimal(minima), Decimal(minima)),), suspendida)


def test_medir_por_cuentas_da_la_peor_y_su_mes_y_las_cifras_de_la_curva_seguida() -> None:
    """d) y e) son un maximo y un minimo por dia: por cuenta salen las cifras de la curva de todos
    los dias seguida (lo nuevo es el mes); a igualdad, la primera cuenta."""
    cuentas = [
        _cuenta("2030-01", "97000"),
        _cuenta("2030-02", "95000", True),
        _cuenta("2030-03", "95000"),
    ]
    m = medir_por_cuentas(cuentas, CAPITAL, BASE_SALDO_CORTE)
    seguida = [x for c in cuentas for x in c.curva]
    assert m.perdida_diaria_maxima == perdida_diaria_maxima(seguida, CAPITAL, BASE_SALDO_CORTE)
    assert m.equity_minima == equity_minima_del_tramo(seguida, CAPITAL) == Fraction(95, 100)
    assert (m.mes_perdida_diaria, m.mes_equity_minima) == ("2030-02", "2030-02")
    assert m.meses_suspendidos == ("2030-02",)
    vacia = medir_por_cuentas([], CAPITAL, BASE_SALDO_CORTE)
    assert (vacia.equity_minima, vacia.mes_equity_minima, vacia.meses_suspendidos) == (
        Fraction(1),
        None,
        (),
    )


def test_el_motivo_de_f_con_una_cuenta_es_el_de_siempre_y_con_varias_dice_cuales() -> None:
    """PARADA condicional 2: con una cuenta, el texto de `main`; con varias, «alguna cuenta»."""
    base = MedidaRentabilidad(
        n=RENT.n_minimo,
        esperanza=Decimal(1),
        percentil_remuestreo=Decimal(1),
        perdida_diaria_maxima=Fraction(0),
        equity_minima=Fraction(1),
        suspendida=True,
    )
    una = veredicto_rentabilidad(base, RENT)
    assert una.estado == NO_PASA and una.motivos == ("f) la cuenta entro en SUSPENDIDA",)
    varias = veredicto_rentabilidad(
        dataclasses.replace(base, cuentas=3, meses_suspendidos=("2030-01", "2030-03")), RENT
    )
    assert varias.motivos == ("f) alguna cuenta entro en SUSPENDIDA (2030-01, 2030-03)",)
