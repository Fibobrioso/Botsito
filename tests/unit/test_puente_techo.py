"""El puente del techo, pre-registrado antes de correr ninguna variante (ADR-0099;
`docs/plan/PUENTE-TECHO.yaml`).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit. Ademas se lee con el lector estricto y se comprueban la
decision, las cifras propias, que cada pieza que nombra una variante existe y que no sobra ninguna,
las variantes en su orden, los dos ordenes de lectura, las cifras publicadas del cierre y que las
claves a las que remite existen en `criterio_fidelidad.yaml` y en `META-TECHO-PAREJAS.yaml`; y un
test rompe a proposito con una cifra cambiada (rama `trabajo/puente-techo`, fase P).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "PUENTE-TECHO.yaml"
META = RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml"
CRITERIO = RAIZ / "knowledge" / "cases" / "criterio_fidelidad.yaml"
SHA256 = "31e70e0a89db3f5b7c1500d7698f450f6d7d3f3659972ef5443ad383b524cfbf"

PROPIOS = {
    "lotes_fuera_si_el_lote_por_riesgo_pasa_de": 100,
    "desfase_puntos": 2,
    "spread_menos_puntos": [1, 2],
    "cierre_tolerancia_operaciones": 3,
    "cierre_tolerancia_esperanza_neta_r": "0.10",
}
PIEZAS = (
    "objetivo_sobre_el_stop",
    "sin_break_even",
    "entrada_al_precio_del_caso",
    "sin_las_de_mas_de_100_lotes",
    "desfase_menos_2",
    "spread_menos_1",
    "spread_menos_2",
    "sin_spread",
    "sin_cierre_h4",
    "stop_en_el_08",
)
SUELTAS = [[p] for p in PIEZAS[:8]]
TODO_JUNTO = list(PIEZAS[:4])
DE_VUELTA = [[p for p in TODO_JUNTO if p != repuesta] for repuesta in TODO_JUNTO]
CIERRE = {
    "v1_de_hoy": [*TODO_JUNTO, "sin_cierre_h4", "desfase_menos_2"],
    "v2_de_hoy": [*TODO_JUNTO, "sin_cierre_h4", "desfase_menos_2", "stop_en_el_08"],
}
MESES_DEL_CIERRE = ["2026-04", "2026-08"]
PUBLICADAS = {
    "v1": {"operaciones": 70, "esperanza_bruta_r": "0.70", "esperanza_neta_r": "0.34"},
    "v2": {"operaciones": 67, "esperanza_bruta_r": "0.88", "esperanza_neta_r": "0.47"},
}
LECTURA_POR_EL_R = ("gana", "no_gana", "no_concluyente")
LECTURAS_DEL_PUENTE = ("una_pieza_basta", "solo_juntas", "ni_juntas")


def _sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def _nombradas(variantes: dict[str, Any]) -> list[str]:
    """Todas las piezas que nombra alguna variante, con repeticiones."""
    salida: list[str] = list(variantes.get("base") or [])
    for grupo in ("sueltas", "de_vuelta"):
        for lista in variantes.get(grupo) or []:
            salida.extend(lista)
    salida.extend(variantes.get("todo_junto") or [])
    for lista in (variantes.get("cierre") or {}).values():
        salida.extend(lista)
    return salida


def problemas(doc: Any) -> list[str]:
    """Lo que no casa con el pre-registro de ADR-0099: cifras, piezas, variantes y orden."""
    if not isinstance(doc, dict):
        return ["el yaml no es un mapa"]
    salida: list[str] = []
    if doc.get("decision") != "ADR-0099":
        salida.append("no cita ADR-0099")
    propios = doc.get("propios") or {}
    for clave, valor in PROPIOS.items():
        if propios.get(clave) != valor:
            salida.append(f"propios.{clave} no es {valor!r}")
    piezas = doc.get("piezas") or {}
    if tuple(piezas) != PIEZAS:
        salida.append("las piezas no son las diez, en su orden")
    variantes = doc.get("variantes") or {}
    nombradas = _nombradas(variantes)
    if sorted(set(nombradas) - set(piezas)):
        salida.append(
            f"variantes con piezas que no existen: {sorted(set(nombradas) - set(piezas))}"
        )
    if sorted(set(piezas) - set(nombradas)):
        salida.append(f"piezas que ninguna variante nombra: {sorted(set(piezas) - set(nombradas))}")
    if variantes.get("base") != []:
        salida.append("base no es la lista vacia")
    if variantes.get("sueltas") != SUELTAS:
        salida.append("las sueltas no son las ocho, en su orden")
    if variantes.get("todo_junto") != TODO_JUNTO:
        salida.append("todo_junto no son las cuatro primeras piezas")
    if variantes.get("de_vuelta") != DE_VUELTA:
        salida.append("las de vuelta no son las cuatro, en su orden")
    if variantes.get("cierre") != CIERRE:
        salida.append("las del cierre no son v1_de_hoy y v2_de_hoy, en su orden")
    elif tuple(variantes["cierre"]) != tuple(CIERRE):
        salida.append("las del cierre no van en su orden")
    cierre = doc.get("cierre") or {}
    if cierre.get("meses") != MESES_DEL_CIERRE:
        salida.append("el cierre no se lee sobre abril y agosto")
    publicadas = cierre.get("publicadas_con_5_usd") or {}
    for nombre, cifras in PUBLICADAS.items():
        if publicadas.get(nombre) != cifras:
            salida.append(f"las publicadas de {nombre} no son {cifras!r}")
    if tuple((doc.get("lectura_por_el_r") or {}).get("orden") or ()) != LECTURA_POR_EL_R:
        salida.append("el orden de la lectura por el R no es gana, no_gana, no_concluyente")
    if tuple((doc.get("lecturas_del_puente") or {}).get("orden") or ()) != LECTURAS_DEL_PUENTE:
        salida.append("el orden del puente no es una_pieza_basta, solo_juntas, ni_juntas")
    for clave in (
        "decidido_el",
        "modelo_de_partida",
        "que_imprime",
        "que_no_imprime",
        "adr_0092_6",
    ):
        if not str(doc.get(clave) or "").strip():
            salida.append(f"falta {clave}")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_el_yaml_va_con_saltos_lf() -> None:
    assert b"\r" not in RUTA.read_bytes()


def test_las_cifras_las_piezas_y_las_variantes_son_las_de_adr_0099() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_las_claves_a_las_que_remite_existen() -> None:
    """Las cifras de ADR-0092 §3 y ADR-0098 §2 no se copian: se leen de alli, y tienen que estar."""
    rentabilidad = leer_yaml(CRITERIO)["rentabilidad"]
    assert rentabilidad["n_minimo"] == 100
    assert rentabilidad["esperanza_minima_r"] == "0.10"
    propios_meta = leer_yaml(META)["propios"]
    assert propios_meta["percentil_alto"] == 95
    assert propios_meta["techo_no_gana_si_percentil_alto_por_debajo_de_r"] == "0.10"


def test_una_cifra_cambiada_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: el desfase a 3 puntos cambia el sha256 y la rechaza."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = "  desfase_puntos: 2\n"
    assert texto.count(linea) == 1
    mutado = tmp_path / "PUENTE-TECHO.yaml"
    mutado.write_bytes(texto.replace(linea, "  desfase_puntos: 3\n").encode("utf-8"))
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["propios.desfase_puntos no es 2"]


def test_una_variante_con_otra_pieza_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: una suelta que nombra una pieza que no existe."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = "    - [sin_spread]\n"
    assert texto.count(linea) == 1
    mutado = tmp_path / "PUENTE-TECHO.yaml"
    mutado.write_bytes(texto.replace(linea, "    - [sin_comision]\n").encode("utf-8"))
    assert problemas(leer_yaml(mutado)) == [
        "variantes con piezas que no existen: ['sin_comision']",
        "piezas que ninguna variante nombra: ['sin_spread']",
        "las sueltas no son las ocho, en su orden",
    ]
