"""La meta, pre-registrada antes de la corrida (3) (ADR-0098; `docs/plan/META-TECHO-PAREJAS.yaml`).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit. Ademas se lee con el lector estricto y se comprueban la
decision, las cifras propias, las cuatro salidas en su orden, la precedencia con el pivote, el orden
de lectura del techo, que el minimo de parejas remite a una clave de `PIVOTES-SESION-7.yaml` con el
valor 19 y que el bloque `rentabilidad` de `criterio_fidelidad.yaml` al que remite existe con sus
dos cifras; y un test rompe a proposito con una banda cambiada (rama
`trabajo/recorrida-construccion-3`, fase P).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml"
PIVOTES = RAIZ / "docs" / "plan" / "PIVOTES-SESION-7.yaml"
CRITERIO = RAIZ / "knowledge" / "cases" / "criterio_fidelidad.yaml"
SHA256 = "bb8291df8da8cbc53334f6128348a38e2cf516aef286da4fbeca456ec5b21bcc"

PROPIOS = {
    "percentil_alto": 95,
    "techo_no_gana_si_percentil_alto_por_debajo_de_r": "0.10",
    "parejas_ganan_media_bot_al_menos_r": "0.10",
    "parejas_pierden_media_bot_por_debajo_de_r": "0",
    "parejas_pierden_percentil_alto_de_la_diferencia_por_debajo_de_r": "0",
    "relecturas_de_d_antes_de_decidir": 2,
}
SALIDAS = ("A", "B", "C", "D")
PRECEDENCIA = ("C", "B", "A", "D")
LECTURA_DEL_TECHO = ("gana", "no_gana", "no_concluyente")
LECTURA_DE_LAS_PAREJAS = ("no_concluyente", "ganan", "pierden", "ni_una_cosa_ni_otra")


def _sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def _clave_del_pivote(referencia: str) -> Any:
    """`PIVOTES-SESION-7.yaml, minimos.minimo_1_...` -> el valor de esa clave en su yaml."""
    fichero, _, ruta = referencia.partition(", ")
    if fichero != PIVOTES.name or not ruta:
        return None
    nodo: Any = leer_yaml(PIVOTES)
    for parte in ruta.split("."):
        if not isinstance(nodo, dict) or parte not in nodo:
            return None
        nodo = nodo[parte]
    return nodo


def problemas(doc: Any) -> list[str]:
    """Lo que no casa con el pre-registro de ADR-0098: decision, cifras, salidas y precedencia."""
    if not isinstance(doc, dict):
        return ["el yaml no es un mapa"]
    salida: list[str] = []
    if doc.get("decision") != "ADR-0098":
        salida.append("no cita ADR-0098")
    propios = doc.get("propios") or {}
    for clave, valor in PROPIOS.items():
        if propios.get(clave) != valor:
            salida.append(f"propios.{clave} no es {valor!r}")
    if _clave_del_pivote(str(propios.get("parejas_minimo_desde") or "")) != 19:
        salida.append("parejas_minimo_desde no nombra una clave del pivote con el valor 19")
    if tuple(doc.get("salidas") or {}) != SALIDAS:
        salida.append("las salidas no son A, B, C y D, en su orden")
    if tuple(doc.get("precedencia_con_el_pivote") or {}) != PRECEDENCIA:
        salida.append("la precedencia con el pivote no son sus cuatro claves")
    lecturas = doc.get("lecturas") or {}
    if tuple(lecturas.get("orden_de_lectura_del_techo") or ()) != LECTURA_DEL_TECHO:
        salida.append("el orden de lectura del techo no es gana, no_gana, no_concluyente")
    if tuple(lecturas.get("techo") or {}) != LECTURA_DEL_TECHO:
        salida.append("las lecturas del techo no son las tres, en su orden")
    if tuple(lecturas.get("parejas") or {}) != LECTURA_DE_LAS_PAREJAS:
        salida.append("las lecturas de las parejas no son las cuatro, en su orden")
    for clave in ("pre_registrado_el", "que_se_mide", "umbrales_de_adr_0092", "adr_0092_6"):
        if not str(doc.get(clave) or "").strip():
            salida.append(f"falta {clave}")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_las_cifras_las_salidas_y_la_precedencia_son_las_de_adr_0098() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_el_bloque_rentabilidad_al_que_remite_existe() -> None:
    """Las cifras de ADR-0092 §3 no se copian: se leen de aqui, y tienen que estar."""
    rentabilidad = leer_yaml(CRITERIO)["rentabilidad"]
    assert rentabilidad["n_minimo"] == 100
    assert rentabilidad["esperanza_minima_r"] == "0.10"


def test_una_banda_cambiada_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: la banda de las parejas que ganan a 0.05 cambia el sha256 y la rechaza."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = 'parejas_ganan_media_bot_al_menos_r: "0.10"\n'
    assert texto.count(linea) == 1
    mutado = tmp_path / "META-TECHO-PAREJAS.yaml"
    mutado.write_bytes(
        texto.replace(linea, 'parejas_ganan_media_bot_al_menos_r: "0.05"\n').encode("utf-8")
    )
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == [
        "propios.parejas_ganan_media_bot_al_menos_r no es '0.10'"
    ]


def test_el_minimo_que_no_remite_al_pivote_rompe(tmp_path: Path) -> None:
    texto = RUTA.read_text(encoding="utf-8")
    assert texto.count("minimo_1_parejas_de_julio_al_menos\n") == 1
    mutado = tmp_path / "META-TECHO-PAREJAS.yaml"
    mutado.write_text(
        texto.replace(
            "minimo_1_parejas_de_julio_al_menos\n",
            "minimo_2_operaciones_de_mas_de_julio_como_mucho\n",
        ),
        encoding="utf-8",
        newline="\n",
    )
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == [
        "parejas_minimo_desde no nombra una clave del pivote con el valor 19"
    ]
