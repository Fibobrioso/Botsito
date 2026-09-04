from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from botsito.evidence import contradicciones
from botsito.evidence.modelo import (
    EvidenciaError,
    calcular_id,
    cargar_evidencia,
    cargar_item,
    escribir_item,
    formato_hhmmss,
    item_desde_dict,
    parse_tiempo,
    validar_contra_manifiesto,
)

MANIFIESTO: dict[str, Any] = {
    "videos": [{"video_id": "v4", "duracion_s": 5616.7}, {"video_id": "v1", "duracion_s": 1752.3}],
    "ficheros": [{"ruta": "_procesado/v4/fr/c0_013.jpg"}],
}


def base(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "video_id": "v4",
        "t0": "0:15:33",
        "t1": "0:16:10",
        "modalidad": "audio",
        "tipo": "RULE_STATEMENT",
        "cita_literal": "es muy importante que lo rompa con cuerpo y que cierre con cuerpo",
        "afirmacion": "la mitigacion en M15 exige cierre con cuerpo",
        "tema": "mitigacion.m15.cierre",
        "valor": "cuerpo",
        "confianza": "alta",
        "extractor": "humano",
        "revisado_por": "aleks",
        "provenance": "botsito",
    }
    d.update(cambios)
    return d


def test_tiempos() -> None:
    assert parse_tiempo("1:02:03.5") == 3723.5
    assert formato_hhmmss(3723.5) == "010203"
    with pytest.raises(EvidenciaError):
        parse_tiempo("15:33")
    with pytest.raises(EvidenciaError):
        parse_tiempo("0:61:00")


def test_id_calculado_y_nombre_de_fichero(tmp_path: Path) -> None:
    ruta = escribir_item(tmp_path, base())
    item = cargar_item(ruta)
    assert item.id.startswith("ev-v4-001533-") and ruta.stem == item.id
    assert ruta.parent.name == "v4"
    with pytest.raises(EvidenciaError, match="ya existe"):
        escribir_item(tmp_path, base())


def test_editar_rompe_el_id(tmp_path: Path) -> None:
    ruta = escribir_item(tmp_path, base())
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    doc["valor"] = "mecha"
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True), encoding="utf-8")
    with pytest.raises(EvidenciaError, match="no coincide con el contenido"):
        cargar_item(ruta)


def test_nombre_de_fichero_distinto_del_id(tmp_path: Path) -> None:
    ruta = escribir_item(tmp_path, base())
    otra = ruta.with_name("otro.yaml")
    ruta.rename(otra)
    with pytest.raises(EvidenciaError, match="nombre del fichero"):
        cargar_item(otra)


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"cita_literal": ""}, "obligatorios"),
        ({"cita_literal": "ok"}, "placeholder"),
        ({"revisado_por": " "}, "obligatorio"),
        ({"tipo": "CONTRADICTION"}, "tipo"),
        ({"tema": "Stop Nivel"}, "tema"),
        ({"t1": "0:15:33"}, "t0 debe ser menor"),
        ({"afirmacion": "x" * 400}, "mucho mas larga"),
        ({"valor": 0.75}, "valor debe ser texto"),
        ({"supersede": "abc"}, "supersede"),
        ({"inventado": 1}, "desconocidos"),
        ({"provenance": "otro"}, "provenance"),
    ],
)
def test_rechazos(cambio: dict[str, Any], mensaje: str) -> None:
    campos = base(**cambio)
    campos["id"] = "ev-v4-001533-00000000"
    with pytest.raises(EvidenciaError, match=mensaje):
        item_desde_dict(campos)


def test_validacion_contra_manifiesto(tmp_path: Path) -> None:
    escribir_item(tmp_path, base())
    escribir_item(tmp_path, base(video_id="v9", tema="a.b"))
    escribir_item(tmp_path, base(t0="1:33:00", t1="1:34:30", tema="a.c"))
    escribir_item(tmp_path, base(fotogramas=["_procesado/v4/fr/no_existe.jpg"], tema="a.d"))
    escribir_item(tmp_path, base(supersede="ev-v4-000000-deadbeef", tema="a.e"))
    problemas = validar_contra_manifiesto(cargar_evidencia(tmp_path), MANIFIESTO)
    assert len(problemas) == 4
    assert any("v9" in p for p in problemas)
    assert any("supera la duracion" in p for p in problemas)
    assert any("no inventariado" in p for p in problemas)
    assert any("no existe" in p for p in problemas)


def test_contradicciones_y_supersede(tmp_path: Path) -> None:
    a = escribir_item(tmp_path, base(valor="cuerpo"))
    b = escribir_item(tmp_path, base(valor="mecha", t0="0:38:53", t1="0:39:10", video_id="v4"))
    items = cargar_evidencia(tmp_path)
    detectadas = contradicciones.detectar(items)
    assert len(detectadas) == 1 and detectadas[0]["valores"] == ["cuerpo", "mecha"]
    assert contradicciones.validar_fichero(tmp_path, items)  # falta el fichero
    contradicciones.escribir(tmp_path, items)
    assert contradicciones.validar_fichero(tmp_path, items) == []
    # un item nuevo que supersede al de "mecha" cierra la contradiccion
    id_b = cargar_item(b).id
    escribir_item(
        tmp_path,
        base(
            valor="cuerpo", t0="0:59:03", t1="0:59:20", supersede=id_b, tema="mitigacion.m15.cierre"
        ),
    )
    items = cargar_evidencia(tmp_path)
    assert contradicciones.detectar(items) == []
    assert "no coincide" in contradicciones.validar_fichero(tmp_path, items)[0]
    assert cargar_item(a).id in {i.id for i in items}


def test_fichero_de_contradicciones_determinista(tmp_path: Path) -> None:
    escribir_item(tmp_path, base(valor="cuerpo"))
    escribir_item(tmp_path, base(valor="mecha", t0="0:38:53", t1="0:39:10"))
    items = cargar_evidencia(tmp_path)
    assert contradicciones.texto(items) == contradicciones.texto(list(reversed(items)))


@given(
    espacios=st.text(alphabet=" \t\n", min_size=0, max_size=4),
    extra=st.text(alphabet="abc", min_size=1, max_size=5),
)
def test_id_estable_ante_espacios_y_cambia_con_contenido(espacios: str, extra: str) -> None:
    ref = calcular_id(base())
    assert calcular_id(base(cita_literal=espacios + base()["cita_literal"] + espacios)) == ref
    reordenado = dict(reversed(list(base().items())))
    assert calcular_id(reordenado) == ref
    assert calcular_id(base(afirmacion=base()["afirmacion"] + " " + extra)) != ref


def test_directorio_real_valida(repo: Path) -> None:
    from botsito.corpus.inventario import cargar_manifiesto

    items = cargar_evidencia(repo / "knowledge" / "evidence")
    manifiesto = cargar_manifiesto(repo / "knowledge" / "corpus" / "manifest.yaml")
    assert validar_contra_manifiesto(items, manifiesto) == []
    assert contradicciones.validar_fichero(repo / "knowledge" / "evidence", items) == []


def test_coma_decimal_no_es_contradiccion(tmp_path: Path) -> None:
    escribir_item(tmp_path, base(valor="0,75", tema="stop.nivel"))
    escribir_item(tmp_path, base(valor="0.75", tema="stop.nivel", t0="0:20:00", t1="0:20:10"))
    escribir_item(tmp_path, base(valor="Cuerpo", tema="x.y", t0="0:21:00", t1="0:21:10"))
    escribir_item(tmp_path, base(valor="cuerpo", tema="x.y", t0="0:22:00", t1="0:22:10"))
    assert contradicciones.detectar(cargar_evidencia(tmp_path)) == []
