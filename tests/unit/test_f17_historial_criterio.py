"""El criterio del historial de ticks de FTMO, pre-registrado antes de ver un tick (ADR-0099 §5;
`docs/plan/F17-HISTORIAL.yaml`, rama `trabajo/f17-historial`).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit, como `test_premisa_costes.py`. Ademas se lee con el lector
estricto y se comprueban sus cifras, que la tolerancia de (c) es la de `scripts/ticks_integridad.py`
(una sola cifra en dos sitios, comparada aqui), que el calendario de cierres que nombra existe y
cubre los cuatro meses de construccion, y que las filas del puente que nombra existen; y un test
rompe a proposito.
"""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.comun.yaml_estricto import leer_yaml
from botsito.engine.calendario_cierres import cargar_calendario

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "F17-HISTORIAL.yaml"
PUENTE = RAIZ / "docs" / "plan" / "PUENTE-TECHO.yaml"
INTEGRIDAD = RAIZ / "scripts" / "ticks_integridad.py"
# El sha cambio una vez, a la vista: la frase `minutos` del bloque d2 (respuesta del consultor a la
# PARADA 2 del 2026-11-26), antes de ver un tick de FTMO; el primero era 51a8ada2...
SHA256 = "46af1341ded522e945b89eb1bbc099660c72c677d1799d98bb683ed5d69fc552"

CIFRAS = {
    ("a_minutos_con_tick", "minimo"): "0.99",
    ("b_huecos", "umbral_minutos"): 5,
    ("b_huecos", "maximo_huecos_por_mes"): 3,
    ("b_huecos", "hueco_maximo_minutos"): 30,
    ("c_m1_propia", "tolerancia_puntos"): 2,
    ("c_m1_propia", "minimo"): "0.99",
    ("d1_spread_variable", "valores_distintos_minimo"): 3,
    ("d1_spread_variable", "minimo"): "0.95",
    ("d2_ticks_por_minuto", "fraccion_de_dukascopy_minima"): "0.5",
}
CALENDARIO = "knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml"


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def problemas(doc: dict[str, Any]) -> list[str]:
    """Lo que no es lo pre-registrado: la decision, las cifras de cubre_si y que nada este vacio."""
    salida: list[str] = []
    if doc.get("decision") != "ADR-0099 §5":
        salida.append("la decision no es ADR-0099 §5")
    cubre = doc.get("cubre_si") or {}
    for (bloque, clave), valor in CIFRAS.items():
        if (cubre.get(bloque) or {}).get(clave) != valor:
            salida.append(f"{bloque}.{clave} no es {valor!r}")
    if CALENDARIO not in str((doc.get("dias") or {}).get("calendario") or ""):
        salida.append("el calendario de los dias no es el de FTMO")
    for clave in ("meses", "ventana", "reloj", "control_dukascopy", "no_imprime", "no_autoriza"):
        if not str(doc.get(clave) or "").strip():
            salida.append(f"falta {clave}")
    if not str(cubre.get("d_lectura") or "").strip() or not str(cubre.get("veredicto") or ""):
        salida.append("falta la lectura de d o el veredicto")
    if "descargadas" not in str((cubre.get("d2_ticks_por_minuto") or {}).get("minutos") or ""):
        salida.append("d2 no acota sus minutos a las horas que Dukascopy tiene descargadas")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_el_yaml_va_con_saltos_lf() -> None:
    assert b"\r" not in RUTA.read_bytes()


def test_las_cifras_son_las_de_la_respuesta_a_la_parada() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_la_tolerancia_de_c_es_la_de_ticks_integridad() -> None:
    """La misma cifra en dos sitios (auditor, 30): el yaml es la puerta de este criterio, y este
    test falla si alguna de las dos cambia sin la otra."""
    spec = importlib.util.spec_from_file_location("ticks_integridad", INTEGRIDAD)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["ticks_integridad"] = modulo  # lo pide @dataclass al crear la clase
    try:
        spec.loader.exec_module(modulo)
    finally:
        sys.modules.pop("ticks_integridad", None)
    yaml_tol = leer_yaml(RUTA)["cubre_si"]["c_m1_propia"]["tolerancia_puntos"]
    assert yaml_tol == modulo.TOLERANCIA_PUNTOS


def test_el_calendario_cubre_los_meses_de_construccion() -> None:
    """Punto 0 de la respuesta: si el calendario no cubre un dia de un mes de construccion, PARA."""
    cal = cargar_calendario(RAIZ / CALENDARIO).calendario()
    for mes in cargar_criterio(RAIZ).construccion:
        anio, m = int(mes[:4]), int(mes[5:])
        primero = datetime(anio, m, 1, tzinfo=UTC)
        siguiente = datetime(anio + (m == 12), m % 12 + 1, 1, tzinfo=UTC)
        assert cal.cubre_desde_ms <= int(primero.timestamp() * 1000), mes
        assert int(siguiente.timestamp() * 1000) <= cal.cubre_hasta_ms, mes


def test_las_filas_del_puente_que_nombra_existen() -> None:
    piezas = leer_yaml(PUENTE)["piezas"]
    texto = RUTA.read_text(encoding="utf-8")
    for fila in ("spread_menos_1", "spread_menos_2"):
        assert fila in piezas
        assert fila in texto


def test_una_cifra_cambiada_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: el minimo de (d1) a 0,90 cambia el sha256 y la rechaza."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = '    minimo: "0.95"\n'
    assert texto.count(linea) == 1
    mutado = tmp_path / "F17-HISTORIAL.yaml"
    mutado.write_bytes(texto.replace(linea, '    minimo: "0.90"\n').encode("utf-8"))
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["d1_spread_variable.minimo no es '0.95'"]
