"""El criterio de la medida de las ordenes stop de FTMO, pre-registrado antes de cualquier llenado
(ADR-0099 §5; `docs/plan/F17-ORDENES.yaml`, rama `trabajo/f17-ordenes`, D3 y la respuesta del
consultor a la PARADA del 2026-11-26).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit, como `test_f17_historial_criterio.py`. Ademas se lee con el
lector estricto y se comprueban sus cifras, que «lo visto antes» son los nueve valores de
ADR-0090 §7 (la respuesta, error 1 del consultor) y que el percentil que nombra existe en
`criterio_fidelidad.yaml`; y un test rompe a proposito.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "F17-ORDENES.yaml"
SHA256 = "3d453e901a77ed698e702b4388c189757d09e48f7c4fa91717443a34f8d8ba84"

# (camino de claves, valor): las cifras de D3 y de la respuesta a la PARADA
CIFRAS: dict[tuple[str, ...], Any] = {
    ("sin_tick", "fraccion_maxima_por_clase"): "0.05",
    ("sin_tick", "entra_en_la_mediana"): False,
    ("al_colocar", "entra_en_la_mediana"): False,
    ("al_colocar", "entra_en_sin_tick"): False,
    ("estratos", "uno", "lotes"): "1.00",
    ("estratos", "uno", "minimo_por_clase"): 100,
    ("estratos", "bot", "minimo_por_clase"): 30,
    ("estratos", "bot_reducido", "fraccion_minima_del_lote_d2"): "0.90",
    ("que_estrato_vale", "diferencia_que_importa_puntos"): 1,
    ("que_estrato_vale", "bot_minimo_si_el_lote_importa"): 100,
    ("guion", "stop_puntos"): 18,
    ("guion", "salida_a_mercado_s"): 300,
    ("guion", "espera_llenado_s"): 120,
    ("guion", "distancia_entrada_puntos"): 5,
}
# ADR-0090 §7: tres por ejecucion; la buy stop, llenado menos nivel; a mercado, llenado menos la
# cotizacion leida antes (MedirDemoFTMO.mq5:650-651 y :666-667)
VISTO_BUY_STOP = [1, 0, 0]
VISTO_MERCADO = {
    "ejecucion_1": {"lotes": "0.01", "apertura": 2, "cierre": -2},
    "ejecucion_2": {"lotes": "1.00", "apertura": 2, "cierre": 0},
    "ejecucion_3": {"lotes": "1.00", "apertura": 0, "cierre": 0},
}
CLASES = ["entrada_stop", "cierre_stop", "cierre_mercado"]


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _en(doc: Any, camino: tuple[str, ...]) -> Any:
    for clave in camino:
        if not isinstance(doc, dict) or clave not in doc:
            return None
        doc = doc[clave]
    return doc


def problemas(doc: dict[str, Any]) -> list[str]:
    """Lo que no es lo pre-registrado: la regla, la referencia, las clases, las cifras, lo visto y
    que nada de lo que el lector necesita este vacio."""
    salida: list[str] = []
    if not str(doc.get("regla") or "").startswith("ADR-0092 §4"):
        salida.append("la regla no es ADR-0092 §4")
    if not str(doc.get("referencia") or "").startswith("ADR-0099 §5"):
        salida.append("la referencia no es ADR-0099 §5")
    if doc.get("clases") != CLASES:
        salida.append(f"las clases no son {CLASES}")
    for camino, valor in CIFRAS.items():
        if _en(doc, camino) != valor:
            salida.append(f"{'.'.join(camino)} no es {valor!r}")
    visto = doc.get("lo_visto_antes") or {}
    if _en(visto, ("buy_stop_llenado_menos_nivel", "valores")) != VISTO_BUY_STOP:
        salida.append("lo visto antes: la buy stop no son los tres de ADR-0090 §7")
    if visto.get("mercado_llenado_menos_cotizacion_previa") != VISTO_MERCADO:
        salida.append("lo visto antes: a mercado no son los seis de ADR-0090 §7")
    for camino in (
        ("precisiones_nuevas",),
        ("tick_que_dispara", "regla"),
        ("tick_que_dispara", "bordes"),
        ("cierre_mercado", "referencia"),
        ("al_colocar", "regla"),
        ("estadistico", "percentil"),
        ("que_estrato_vale", "precision"),
        ("ventana", "regla"),
        ("reloj",),
        ("como_entra_en_adr_0092",),
        ("lo_que_no_dice",),
        ("spread_del_grabador",),
        ("no_imprime",),
    ):
        if not str(_en(doc, camino) or "").strip():
            salida.append(f"falta {'.'.join(camino)}")
    if "pendiente_F17" not in str(doc.get("como_entra_en_adr_0092") or ""):
        salida.append("como_entra_en_adr_0092 no dice que deslizamiento sigue en pendiente_F17")
    if "P4-08" not in str(doc.get("lo_que_no_dice") or ""):
        salida.append("lo_que_no_dice no nombra P4-08")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_el_yaml_va_con_saltos_lf() -> None:
    assert b"\r" not in RUTA.read_bytes()


def test_las_cifras_son_las_de_la_respuesta_a_la_parada() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_el_percentil_que_nombra_es_el_de_criterio_fidelidad() -> None:
    """El yaml no copia la cifra del percentil: nombra el campo de `criterio_fidelidad.yaml`."""
    assert "percentil_deslizamiento_f17" in str(leer_yaml(RUTA)["estadistico"]["percentil"])
    rentabilidad = cargar_criterio(RAIZ).rentabilidad
    assert rentabilidad is not None
    assert rentabilidad.percentil_deslizamiento_f17 == 90


def test_una_cifra_cambiada_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: el minimo de «uno» a 50 cambia el sha256 y la rechaza."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = "    minimo_por_clase: 100\n"
    assert texto.count(linea) == 1
    mutado = tmp_path / "F17-ORDENES.yaml"
    mutado.write_bytes(texto.replace(linea, "    minimo_por_clase: 50\n").encode("utf-8"))
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["estratos.uno.minimo_por_clase no es 100"]


def test_siete_en_vez_de_nueve_rompe(tmp_path: Path) -> None:
    """Rompe a proposito con el error 1 del consultor: «lo visto antes» sin la ejecucion 3."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = '    ejecucion_3: {lotes: "1.00", apertura: 0, cierre: 0}\n'
    assert texto.count(linea) == 1
    mutado = tmp_path / "F17-ORDENES.yaml"
    mutado.write_bytes(texto.replace(linea, "").encode("utf-8"))
    assert problemas(leer_yaml(mutado)) == [
        "lo visto antes: a mercado no son los seis de ADR-0090 §7"
    ]
