"""La premisa con costes, pre-registrada antes de correr nada y antes de que el backtest del trader
llegue a nadie del proyecto (ADR-0100; `docs/plan/PREMISA-COSTES.yaml`).

El yaml se fija por su sha256, escrito aqui: cambiar una cifra (o cualquier byte) exige cambiar este
test a la vista en el mismo commit. Ademas se lee con el lector estricto y se comprueban la
decision, los meses propuestos y su regla, las condiciones del backtest, la comision en pips,
los ordenes de lectura (los del backtest y el de §5), las cinco combinaciones con sus claves y
valores en su orden, que ningun valor es nulo, los dos bloques de meses, los tramos de R, el
margen y los tramos de retroceso, las variantes del techo con lote fijo, y que las claves a las
que remite existen en `criterio_fidelidad.yaml`, en `META-TECHO-PAREJAS.yaml` y en
`PUENTE-TECHO.yaml`; y dos tests rompen a proposito (rama `trabajo/diagnostico-premisa`, fase P).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from botsito.comun.yaml_estricto import leer_yaml

RAIZ = Path(__file__).resolve().parents[2]
RUTA = RAIZ / "docs" / "plan" / "PREMISA-COSTES.yaml"
PUENTE = RAIZ / "docs" / "plan" / "PUENTE-TECHO.yaml"
META = RAIZ / "docs" / "plan" / "META-TECHO-PAREJAS.yaml"
CRITERIO = RAIZ / "knowledge" / "cases" / "criterio_fidelidad.yaml"
SHA256 = "1294bdb1b7dfd992dd87e14ccb0f9d1d6b2bc6e45168bd19ed64a719f68f3b33"

MESES_PROPUESTOS = ["2024-01", "2024-07"]
MAXIMO_DE_MESES = 4
CONDICIONES = {
    "spread_pips": "0.2",
    "comision_usd_por_lote_ida_y_vuelta": 5,
    "riesgo_por_operacion_pct": "0.5",
}
C_PIPS = "0.5"
LECTURA_ANTES = ["no_valida", "insuficiente"]
LECTURA_ORDEN = ["gana", "no_gana", "no_concluyente"]
COMBINACIONES = [
    ("gana", "cualquiera"),
    (["no_gana", "no_concluyente"], "gana"),
    ("no_concluyente", ["no_concluyente", "no_gana"]),
    ("no_gana", "no_concluyente"),
    ("no_gana", "no_gana"),
]
CLAVES_DE_COMBINACION = {"por_riesgo", "con_lote_fijo", "propone"}
BLOQUES = {"abril_y_agosto": ["2026-04", "2026-08"], "enero_y_julio": ["2026-01", "2026-07"]}
TRAMOS_R = {"gana_si_mas_de": "0.2", "pierde_si_menos_de": "-0.2"}
MARGEN_R = "0.20"
LECTURA_DE_5 = ["la_replica_pierde_mas_en_enero_y_julio", "enero_y_julio_peores_tambien_para_el"]
TRAMOS_RETROCESO = ["0", "0.5", "0.8", "1.0"]
VARIANTES_LOTE_FIJO = ["base", "todo_junto"]


def _sha256(datos: bytes) -> str:
    return hashlib.sha256(datos).hexdigest()


def _nulos(nodo: Any, donde: str = "") -> list[str]:
    """Las rutas de los valores nulos y de las claves nulas o vacias, en todo el arbol.

    Un texto con comas dentro de un mapa en linea (`{a: uno, dos}`) se parte en claves nulas sin
    error del lector: aqui se caza.
    """
    salida: list[str] = []
    if nodo is None:
        return [donde or "(raiz)"]
    if isinstance(nodo, dict):
        for clave, valor in nodo.items():
            sitio = f"{donde}.{clave}" if donde else str(clave)
            if clave is None or not str(clave).strip():
                salida.append(f"{sitio} (clave nula)")
            salida.extend(_nulos(valor, sitio))
    elif isinstance(nodo, list):
        for i, valor in enumerate(nodo):
            salida.extend(_nulos(valor, f"{donde}[{i}]"))
    elif isinstance(nodo, str) and not nodo.strip():
        salida.append(f"{donde} (texto vacio)")
    return salida


def problemas(doc: Any) -> list[str]:
    """Lo que no casa con el pre-registro de ADR-0100: cifras, ordenes, combinaciones y bloques."""
    if not isinstance(doc, dict):
        return ["el yaml no es un mapa"]
    salida: list[str] = [f"valor nulo en {r}" for r in _nulos(doc)]
    if doc.get("decision") != "ADR-0100":
        salida.append("no cita ADR-0100")
    if doc.get("decidido_el") != "2026-11-24":
        salida.append("decidido_el no es 2026-11-24")
    backtest = doc.get("backtest_del_trader") or {}
    meses = backtest.get("meses") or {}
    if meses.get("propuestos") != MESES_PROPUESTOS:
        salida.append(f"los meses propuestos no son {MESES_PROPUESTOS!r}")
    for clave in ("regla", "regimen", "extension"):
        if not str(meses.get(clave) or "").strip():
            salida.append(f"falta meses.{clave}")
    if meses.get("maximo_de_meses") != MAXIMO_DE_MESES:
        salida.append(f"maximo_de_meses no es {MAXIMO_DE_MESES}")
    condiciones = backtest.get("condiciones") or {}
    for clave, valor in CONDICIONES.items():
        if condiciones.get(clave) != valor:
            salida.append(f"condiciones.{clave} no es {valor!r}")
    medidas = backtest.get("medidas") or {}
    if medidas.get("c_pips") != C_PIPS:
        salida.append(f"medidas.c_pips no es {C_PIPS!r}")
    lectura = backtest.get("lectura") or {}
    if lectura.get("antes") != LECTURA_ANTES:
        salida.append("la lectura previa no es no_valida, insuficiente")
    if lectura.get("orden") != LECTURA_ORDEN:
        salida.append("el orden de la lectura no es gana, no_gana, no_concluyente")
    for clave in (*LECTURA_ANTES, *LECTURA_ORDEN):
        if not str(lectura.get(clave) or "").strip():
            salida.append(f"falta la lectura {clave}")
    combinaciones = backtest.get("combinaciones") or []
    if len(combinaciones) != len(COMBINACIONES):
        salida.append(f"no son {len(COMBINACIONES)} combinaciones")
    for i, (combinacion, (por_riesgo, con_lote_fijo)) in enumerate(
        zip(combinaciones, COMBINACIONES, strict=False)
    ):
        if not isinstance(combinacion, dict) or set(combinacion) != CLAVES_DE_COMBINACION:
            salida.append(
                f"la combinacion {i} no tiene exactamente {sorted(CLAVES_DE_COMBINACION)}"
            )
            continue
        if combinacion["por_riesgo"] != por_riesgo or combinacion["con_lote_fijo"] != con_lote_fijo:
            salida.append(f"la combinacion {i} no es {por_riesgo!r} con {con_lote_fijo!r}")
    registro = doc.get("registro_frente_a_replica") or {}
    if registro.get("bloques") != BLOQUES:
        salida.append("los bloques no son abril_y_agosto y enero_y_julio con sus meses")
    elif list(registro["bloques"]) != list(BLOQUES):
        salida.append("los bloques no van en su orden")
    if registro.get("tramos_r") != TRAMOS_R:
        salida.append(f"tramos_r no es {TRAMOS_R!r}")
    if registro.get("margen_r") != MARGEN_R:
        salida.append(f"margen_r no es {MARGEN_R!r}")
    if (registro.get("lectura") or {}).get("orden") != LECTURA_DE_5:
        salida.append("el orden de la lectura de §5 no es el pre-registrado")
    retroceso = registro.get("retroceso_de_las_ganadoras") or {}
    if retroceso.get("tramos") != TRAMOS_RETROCESO:
        salida.append(f"los tramos de retroceso no son {TRAMOS_RETROCESO!r}")
    techo = doc.get("techo_con_lote_fijo") or {}
    if techo.get("variantes") != VARIANTES_LOTE_FIJO:
        salida.append(f"las variantes del techo con lote fijo no son {VARIANTES_LOTE_FIJO!r}")
    for clave in ("que_no_imprime", "adr_0092_6"):
        if not str(doc.get(clave) or "").strip():
            salida.append(f"falta {clave}")
    return salida


def test_el_yaml_es_el_pre_registrado() -> None:
    """Cualquier byte cambiado cambia el sha256: el test se cambia a la vista con el yaml."""
    assert _sha256(RUTA.read_bytes()) == SHA256


def test_el_yaml_va_con_saltos_lf() -> None:
    assert b"\r" not in RUTA.read_bytes()


def test_las_cifras_los_ordenes_y_las_combinaciones_son_las_de_adr_0100() -> None:
    assert problemas(leer_yaml(RUTA)) == []


def test_las_claves_a_las_que_remite_existen() -> None:
    """Las cifras del bloque rentabilidad, de META-TECHO-PAREJAS y de PUENTE-TECHO no se copian:
    se leen de alli, y tienen que estar."""
    rentabilidad = leer_yaml(CRITERIO)["rentabilidad"]
    assert rentabilidad["n_minimo"] == 100
    assert rentabilidad["esperanza_minima_r"] == "0.10"
    assert isinstance(rentabilidad["percentil_remuestreo"], int)
    assert isinstance(rentabilidad["replicas_remuestreo"], int)
    assert isinstance(rentabilidad["semilla_remuestreo"], int)
    propios_meta = leer_yaml(META)["propios"]
    assert propios_meta["percentil_alto"] == 95
    assert propios_meta["techo_no_gana_si_percentil_alto_por_debajo_de_r"] == "0.10"
    puente = leer_yaml(PUENTE)
    assert puente["propios"]["desfase_puntos"] == 2
    for variante in VARIANTES_LOTE_FIJO:
        assert variante in puente["variantes"]


def test_una_cifra_cambiada_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: el margen de §5 a 0,25 cambia el sha256 y la rechaza."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = '  margen_r: "0.20"\n'
    assert texto.count(linea) == 1
    mutado = tmp_path / "PREMISA-COSTES.yaml"
    mutado.write_bytes(texto.replace(linea, '  margen_r: "0.25"\n').encode("utf-8"))
    assert _sha256(mutado.read_bytes()) != SHA256
    assert problemas(leer_yaml(mutado)) == ["margen_r no es '0.20'"]


def test_un_texto_con_comas_en_un_mapa_en_linea_rompe(tmp_path: Path) -> None:
    """Rompe a proposito: un texto con comas en un mapa en linea se parte en una clave nula."""
    texto = RUTA.read_bytes().decode("utf-8")
    linea = '  tramos_r: {gana_si_mas_de: "0.2", pierde_si_menos_de: "-0.2"}\n'
    assert texto.count(linea) == 1
    mutado = tmp_path / "PREMISA-COSTES.yaml"
    roto = '  tramos_r: {gana_si_mas_de: "0.2", pierde_si_menos_de: "-0.2", y el resto}\n'
    mutado.write_bytes(texto.replace(linea, roto).encode("utf-8"))
    assert problemas(leer_yaml(mutado)) == [
        "valor nulo en registro_frente_a_replica.tramos_r.y el resto",
        f"tramos_r no es {TRAMOS_R!r}",
    ]
