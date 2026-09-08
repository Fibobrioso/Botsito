"""Propuestas de evidencia: esqueleto, sello, guardias de calidad, aceptar/rechazar (F07)."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.evidence.modelo import escribir_item, item_desde_dict
from botsito.evidence.propuestas import (
    PropuestaError,
    Temas,
    anotar_decision,
    campos_de_item,
    cargar_propuesta,
    cargar_temas,
    comprobar,
    comprobar_sello,
    escribir_propuesta,
    esqueleto,
    salida_sha256,
    sellar,
    validar_propuestas,
)
from botsito.evidence.verificacion import ContextoEvidencia

REPO = Path(__file__).resolve().parents[2]
TID = "tr-v4-large-v3-int8-float16-a8d1bccc"


@dataclass(frozen=True)
class P:
    t0_ms: int
    t1_ms: int
    texto: str


@dataclass(frozen=True)
class S:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str
    senales: tuple[str, ...] = ()
    palabras: tuple[P, ...] = ()


def _seg(n: int, t0: int, texto: str, senales: tuple[str, ...] = ()) -> S:
    palabras, t = [], t0
    for w in texto.split():
        palabras.append(P(t, t + 500, w))
        t += 500
    return S(n, t0, t, texto, senales, tuple(palabras))


SEGS = [
    _seg(0, 0, "el stop loss como tal es hasta el 0.75 vale"),
    _seg(1, 6000, "yo sinceramente limito a 3 por ejemplo", ("no_habla",)),
]
TEMAS = Temas(frozenset({"stop", "cartuchos", "meta"}), frozenset({"cuerpo", "si", "no"}))


def _contexto(**cambios: Any) -> ContextoEvidencia:
    base: dict[str, Any] = {
        "referencias": {"fr-v4-9ad0ebb8/1000"},
        "crudas": lambda tid: SEGS if tid == TID else None,
        "transcripciones": {TID: "v4"},
        "activas": {"v4": TID},
        "reemplazadas": {},
        "dudas": lambda tid: {1},
        "temas_raiz": TEMAS.raices,
        "valores_cerrados": TEMAS.valores_cerrados,
    }
    base.update(cambios)
    return ContextoEvidencia(**base)


def _doc(generado_el: str = "2026-09-07T00:00:00Z", **cambios: Any) -> dict[str, Any]:
    doc = esqueleto(
        "v4",
        TID,
        "0:00:00",
        "0:00:12",
        SEGS,
        ["fr-v4-9ad0ebb8/1000"],
        "prompt v1",
        "falso",
        "llm",
        ["stop", "cartuchos"],
        generado_el,
    )
    doc["items"] = [
        {
            "n": 1,
            "t0": "0:00:00",
            "t1": "0:00:05",
            "modalidad": "audio",
            "tipo": "PARAMETER",
            "cita_literal": "el stop loss como tal es hasta el 0.75",
            "afirmacion": "el stop va al 0.75",
            "tema": "stop.nivel",
            "valor": "0.75",
            "confianza": "alta",
        },
        {
            "n": 2,
            "t0": "0:00:06",
            "t1": "0:00:10",
            "modalidad": "audio",
            "tipo": "RULE_STATEMENT",
            "cita_literal": "yo sinceramente limito a 3",
            "afirmacion": "limita a tres cartuchos",
            "tema": "cartuchos.maximo",
            "valor": "3",
            "confianza": "media",
        },
    ]
    doc.update(cambios)
    return doc


def test_esqueleto_id_y_sello() -> None:
    doc = _doc()
    assert doc["propuesta_id"].startswith("pr-v4-000000-000012-")
    assert doc["contexto"]["segmentos"][0]["texto"] == SEGS[0].texto
    assert "palabras" not in doc["contexto"]["segmentos"][0]
    assert comprobar_sello(doc) and "sin salida_sha256" in str(comprobar_sello(doc))
    sellar(doc, "2026-09-07T01:00:00Z")
    assert comprobar_sello(doc) is None
    anotar_decision(doc, 1, "rechazado", "t", "2026-09-07T02:00:00Z", None, "m")
    assert comprobar_sello(doc) is None  # la decision no forma parte del sello
    doc["items"][0]["cita_literal"] = "otra"
    assert "cambio despues del check" in str(comprobar_sello(doc))
    with pytest.raises(PropuestaError, match="proponente"):
        esqueleto("v4", TID, "0:00:00", "0:00:01", [], [], "p", "m", "otro", [], "x")
    with pytest.raises(PropuestaError, match="menor"):
        esqueleto("v4", TID, "0:00:02", "0:00:01", [], [], "p", "m", "llm", [], "x")


def test_comprobar_en_verde_y_localizaciones() -> None:
    r = comprobar(_doc(), _contexto(), TEMAS)
    assert r.problemas == []
    assert set(r.localizaciones) == {1, 2}
    assert r.localizaciones[2].senales == ("no_habla",)


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"tema": "fuera.x"}, "fuera de la taxonomia"),
        ({"valor": "0.80"}, "no aparece en la cita"),
        ({"cita_literal": "el stop loss como tal es hasta el 0,75"}, "no se localiza"),
        ({"cita_literal": "el stop loss"}, "menos de 4 tokens"),
        ({"t0": "0:00:20", "t1": "0:00:30"}, "fuera del tramo"),
        ({"fotogramas": ["fr-v4-9ad0ebb8/1000"]}, "no admite fotogramas"),
        ({"modalidad": "ambas"}, "exige al menos una referencia"),
    ],
)
def test_guardias_por_item(cambio: dict[str, Any], mensaje: str) -> None:
    doc = _doc()
    doc["items"][0].update(cambio)
    r = comprobar(doc, _contexto(), TEMAS)
    assert any(mensaje in p for p in r.problemas), r.problemas


def test_confianza_alta_con_senal_o_duda_es_error() -> None:
    doc = _doc()
    doc["items"][1]["confianza"] = "alta"
    r = comprobar(doc, _contexto(), TEMAS)
    assert any("confianza alta con senales no_habla" in p for p in r.problemas)
    doc = _doc()
    doc["items"][0]["confianza"] = "alta"
    r = comprobar(doc, _contexto(dudas=lambda tid: {0}), TEMAS)
    assert any("duda del glosario" in p for p in r.problemas)


def test_duplicados_solapes_y_temas_buscados() -> None:
    doc = _doc()
    doc["items"].append(dict(doc["items"][0], n=3, tema="stop.otro"))
    r = comprobar(doc, _contexto(), TEMAS)
    assert any("misma cita que el item 1" in p for p in r.problemas)
    doc = _doc()
    doc["items"].append(
        dict(doc["items"][0], n=3, cita_literal="stop loss como tal es hasta", t1="0:00:04")
    )
    r = comprobar(doc, _contexto(), TEMAS)
    assert any("mismo tema y localizacion solapada" in p for p in r.problemas)
    doc = _doc(temas_buscados=["stop", "cartuchos", "meta"])
    r = comprobar(doc, _contexto(), TEMAS)
    assert any("tema buscado 'meta'" in p for p in r.problemas)
    doc["no_consta"] = [{"tema": "meta", "motivo": "no habla del metodo en el tramo"}]
    assert comprobar(doc, _contexto(), TEMAS).problemas == []


def test_cita_ya_en_evidencia_o_rechazada(tmp_path: Path) -> None:
    doc = _doc()
    campos = campos_de_item(doc, 1, "t · hoja · cruda leida", "cruda_leida")
    campos["id"] = None
    del campos["id"]
    ruta = escribir_item(tmp_path, campos)
    from botsito.evidence.modelo import cargar_item

    item = cargar_item(ruta)
    r = comprobar(doc, _contexto(), TEMAS, [item])
    assert any(f"misma cita que la evidencia {item.id}" in p for p in r.problemas)
    otra = _doc(generado_el="2026-09-07T09:00:00Z")
    sellar(otra, "x")
    anotar_decision(otra, 2, "rechazado", "t", "x", None, "no es una regla")
    r = comprobar(doc, _contexto(), TEMAS, [], [otra])
    assert any("fue rechazada" in a for a in r.avisos)


def test_campos_de_item_y_metodos() -> None:
    doc = _doc()
    campos = campos_de_item(doc, 1, "t · hoja · cruda leida", "cruda_leida")
    assert campos["transcripcion"] == TID and campos["extractor"] == "llm"
    assert campos["provenance"] == "botsito"
    campos["id"] = "x"
    del campos["id"]
    from botsito.evidence.modelo import calcular_id

    campos["id"] = calcular_id(campos)
    assert item_desde_dict(campos).transcripcion == TID
    doc["items"][0]["marca_heredada"] = "V4 0:12:30"
    assert campos_de_item(doc, 1, "t", "cruda_leida")["provenance"] == "bot-v2"
    doc["items"][0]["modalidad"] = "ambas"
    with pytest.raises(PropuestaError, match="fotograma_visto"):
        campos_de_item(doc, 1, "t", "cruda_leida")
    with pytest.raises(PropuestaError, match="metodo_revision"):
        campos_de_item(doc, 2, "t", "otro")
    with pytest.raises(PropuestaError, match="cruda_leida o audio_oido"):
        campos_de_item(doc, 2, "t", "fotograma_visto")
    anotar_decision(doc, 2, "aceptado", "t", "x", "cruda_leida", None, "ev-v4-000006-deadbeef")
    with pytest.raises(PropuestaError, match="ya esta aceptado"):
        campos_de_item(doc, 2, "t", "cruda_leida")
    with pytest.raises(PropuestaError, match="no tiene el item"):
        campos_de_item(doc, 9, "t", "cruda_leida")


def test_cargar_propuesta_estricta(tmp_path: Path) -> None:
    doc = _doc()
    ruta = tmp_path / f"{doc['propuesta_id']}.yaml"
    escribir_propuesta(ruta, doc)
    assert cargar_propuesta(ruta)["propuesta_id"] == doc["propuesta_id"]
    casos: list[tuple[dict[str, Any], str]] = [
        ({"propuesta_id": "pr-mal"}, "propuesta_id invalido"),
        ({"prompt": "otro"}, "prompt_sha256"),
        ({"modelo": "otro"}, "no coincide con su contenido"),
        ({"extra": 1}, "desconocidos"),
        ({"items": [{"n": 1}]}, "faltan"),
        ({"no_consta": [{"tema": "x"}]}, "tema y motivo"),
    ]
    for cambio, mensaje in casos:
        malo = dict(doc)
        malo.update(cambio)
        r2 = tmp_path / f"{malo['propuesta_id']}.yaml"
        r2.write_text(yaml.safe_dump(malo, allow_unicode=True), encoding="utf-8")
        with pytest.raises(PropuestaError, match=mensaje):
            cargar_propuesta(r2)
    otro_nombre = tmp_path / "pr-v4-000000-000012-00000000.yaml"
    otro_nombre.write_text(ruta.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(PropuestaError, match="nombre del fichero"):
        cargar_propuesta(otro_nombre)
    # Cabecera con un tiempo invalido: error de propuesta, no traceback de EvidenciaError.
    mal = dict(doc, t0="abc")
    r3 = tmp_path / "sub" / f"{doc['propuesta_id']}.yaml"
    escribir_propuesta(r3, mal)
    with pytest.raises(PropuestaError, match="tiempo invalido"):
        cargar_propuesta(r3)
    # El sello cubre la cabecera (transcripcion, proponente): cambiarlas lo rompe.
    sellado = _doc()
    sellar(sellado, "x")
    sellado["proponente"] = "humano"
    assert comprobar_sello(sellado) is not None


def test_validar_propuestas_para_knowledge_validate() -> None:
    doc = _doc()
    sellar(doc, "x")
    anotar_decision(doc, 1, "aceptado", "t", "x", "cruda_leida", None, "ev-v4-000000-deadbeef")
    problemas, avisos = validar_propuestas([doc], [], "otro-prompt")
    assert any("inexistente" in p for p in problemas)
    assert any("prompt distinto" in a for a in avisos)
    # Evidencia coherente con el item aceptado: sin problemas; con un campo distinto, error.
    campos = campos_de_item(_doc(), 1, "t", "cruda_leida")
    from botsito.evidence.modelo import calcular_id

    campos["id"] = calcular_id(campos)
    ev = item_desde_dict(campos)
    doc["items"][0]["evidence_id"] = ev.id
    problemas, avisos = validar_propuestas([doc], [ev], None)
    assert problemas == [] and avisos == []
    doc["items"][0]["metodo_revision"] = "fotograma_visto"
    problemas, _ = validar_propuestas([doc], [ev], None)
    assert any("audio aceptado con fotograma_visto" in p for p in problemas)
    doc["items"][0]["metodo_revision"] = "cruda_leida"
    otro = dict(campos, tema="otro.tema")
    otro["id"] = calcular_id(otro)
    problemas, _ = validar_propuestas([doc], [item_desde_dict(otro)], None)
    assert any("inexistente" in p for p in problemas)
    doc["items"][0]["evidence_id"] = item_desde_dict(otro).id
    problemas, _ = validar_propuestas([doc], [item_desde_dict(otro)], None)
    assert any("no coincide con" in p and "'tema'" in p for p in problemas)
    # Evidencia llm sin propuesta que la respalde: aviso.
    _, avisos = validar_propuestas([], [ev], None)
    assert any("sin propuesta" in a for a in avisos)
    # Un rechazado no puede anotar evidence_id; el mismo id no puede anotarse dos veces.
    doc2 = _doc()
    sellar(doc2, "x")
    anotar_decision(doc2, 1, "rechazado", "t", "x", None, "m", ev.id)
    problemas, _ = validar_propuestas([doc2], [ev], None)
    assert any("rechazado pero anota" in p for p in problemas)
    doc["items"][0]["evidence_id"] = ev.id
    doc["items"][1]["decision"] = "aceptado"
    doc["items"][1]["metodo_revision"] = "cruda_leida"
    doc["items"][1]["evidence_id"] = ev.id
    problemas, _ = validar_propuestas([doc], [ev], None)
    assert any("ya anotado" in p for p in problemas)
    doc["items"][1]["cita_literal"] = "cambiada"
    problemas, _ = validar_propuestas([doc], [ev], None)
    assert any("cambio despues del check" in p for p in problemas)
    sin_sello = _doc()
    anotar_decision(sin_sello, 1, "rechazado", "t", "x", None, "m")
    problemas, _ = validar_propuestas([sin_sello], [], None)
    assert any("sin check" in p for p in problemas)


def test_temas_reales_y_salida_canonica() -> None:
    temas = cargar_temas(REPO / "knowledge" / "evidence" / "_temas.yaml")
    assert {"stop", "no_trade", "meta"} <= temas.raices and "si" in temas.valores_cerrados
    doc = _doc()
    a = salida_sha256(doc)
    anotar_decision(doc, 1, "rechazado", "t", "x", None, "m")
    assert salida_sha256(doc) == a
