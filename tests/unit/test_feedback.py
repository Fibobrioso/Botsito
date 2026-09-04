from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from botsito.feedback.modelo import (
    FeedbackError,
    activos,
    calcular_id,
    cargar_feedback,
    cargar_registro,
    escribir_registro,
    registro_desde_dict,
    trazar,
    validar_contra_contexto,
)

EV = "ev-v4-001533-1a2b3c4d"


def base(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "sesion": "2026-09-20-sesion-01",
        "fecha": "2026-09-20",
        "medio": "replay",
        "grabacion": "Material adicional/sesion-01.mp4",
        "t0": "0:12:10",
        "t1": "0:12:40",
        "objetivo": {"tipo": "evidence", "id": EV},
        "accion": "CONFIRM",
        "respuesta_literal": "si, con cuerpo, siempre con cuerpo en M15",
        "registrado_por": "aleks",
    }
    d.update(cambios)
    return d


def test_crear_cargar_y_nombre(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    r = cargar_registro(ruta)
    assert r.id.startswith("fb-2026-09-20-sesion-01-") and ruta.stem == r.id
    assert ruta.parent.name == "2026-09-20-sesion-01"
    with pytest.raises(FeedbackError, match="ya existe"):
        escribir_registro(tmp_path, base())


def test_editar_rompe_el_id(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    doc["respuesta_literal"] = "otra cosa distinta"
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True), encoding="utf-8")
    with pytest.raises(FeedbackError, match="no coincide"):
        cargar_registro(ruta)


def test_carpeta_de_sesion(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    otra = tmp_path / "otra" / ruta.name
    otra.parent.mkdir()
    ruta.rename(otra)
    with pytest.raises(FeedbackError, match="carpeta de su sesion"):
        cargar_registro(otra)


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"respuesta_literal": ""}, "obligatorios"),
        ({"respuesta_literal": "si"}, "literal"),
        ({"sesion": "sesion1"}, "sesion invalida"),
        ({"fecha": "20/09/2026"}, "fecha invalida"),
        ({"medio": "telepatia"}, "medio"),
        ({"accion": "APROBAR"}, "accion"),
        ({"objetivo": {"tipo": "regla", "id": "RN-01"}}, "formato"),
        ({"objetivo": {"tipo": "caso", "id": "caso-1"}}, "exige objetivo de tipo"),
        ({"accion": "CORRECT"}, "exige valor_resultante"),
        ({"accion": "RESOLVE_CONTRADICTION"}, "exige objetivo de tipo"),
        ({"grabacion": None}, "exige grabacion"),
        ({"t1": "0:12:10"}, "t0 debe ser menor"),
        ({"supersede": "x"}, "supersede"),
        ({"extra": 1}, "desconocidos"),
    ],
)
def test_rechazos(cambio: dict[str, Any], mensaje: str) -> None:
    campos = base(**cambio)
    campos["id"] = "fb-2026-09-20-sesion-01-00000000"
    with pytest.raises(FeedbackError, match=mensaje):
        registro_desde_dict(campos)


def test_medio_escrito_no_exige_grabacion(tmp_path: Path) -> None:
    campos = base(medio="escrito", grabacion=None, t0=None, t1=None)
    r = cargar_registro(escribir_registro(tmp_path, campos))
    assert r.grabacion is None and r.medio == "escrito"


def test_acciones_coherentes(tmp_path: Path) -> None:
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_CONTRADICTION",
            objetivo={"tipo": "contradiccion", "id": "mitigacion.m15.cierre"},
            valor_resultante="cuerpo",
        ),
    )
    escribir_registro(
        tmp_path,
        base(
            accion="LABEL_CASE",
            objetivo={"tipo": "caso", "id": "caso-2026-07-02-a"},
            valor_resultante="opera",
        ),
    )
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_UNKNOWN",
            objetivo={"tipo": "ambiguedad", "id": "A-1"},
            valor_resultante="cierre",
        ),
    )
    assert len(cargar_feedback(tmp_path)) == 3


def test_validacion_contra_contexto(tmp_path: Path) -> None:
    escribir_registro(tmp_path, base())
    escribir_registro(tmp_path, base(objetivo={"tipo": "parametro", "id": "stop_fraccion"}))
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_CONTRADICTION",
            objetivo={"tipo": "contradiccion", "id": "x.y"},
            valor_resultante="a",
        ),
    )
    escribir_registro(tmp_path, base(supersede="fb-2026-09-20-sesion-01-deadbeef", notas="n"))
    problemas = validar_contra_contexto(
        cargar_feedback(tmp_path),
        ids_evidencia=set(),
        nombres_parametros=set(),
        temas_contradiccion=set(),
        rutas_corpus={"otra.mp4"},
    )
    assert any("no existe" in p and "evidencia" in p for p in problemas)
    assert any("no esta en el registro" in p for p in problemas)
    assert any("no hay contradiccion abierta" in p for p in problemas)
    assert any("supersede a" in p for p in problemas)
    assert any("no esta inventariada" in p for p in problemas)
    ok = validar_contra_contexto(
        [cargar_registro(escribir_registro(tmp_path, base(notas="ok")))],
        ids_evidencia={EV},
        nombres_parametros=set(),
        temas_contradiccion=set(),
        rutas_corpus={"Material adicional/sesion-01.mp4"},
    )
    assert ok == []


def test_supersede_y_traza(tmp_path: Path) -> None:
    primero = cargar_registro(escribir_registro(tmp_path, base()))
    segundo = escribir_registro(
        tmp_path,
        base(
            accion="CORRECT",
            valor_resultante="mecha",
            respuesta_literal="perdon, en M1 vale con mecha",
            supersede=primero.id,
            fecha="2026-09-21",
        ),
    )
    registros = cargar_feedback(tmp_path)
    assert [r.id for r in activos(registros)] == [cargar_registro(segundo).id]
    lineas = trazar(EV, registros)
    assert len(lineas) == 3 and "[superseded]" in lineas[0] and "corrige a" in lineas[2]
    assert trazar("nada", registros) == ["sin registros de feedback para nada"]


@given(
    espacios=st.text(alphabet=" \t\n", max_size=3),
    extra=st.text(alphabet="xyz", min_size=1, max_size=4),
)
def test_id_estable_y_sensible(espacios: str, extra: str) -> None:
    ref = calcular_id(base())
    assert (
        calcular_id(base(respuesta_literal=espacios + base()["respuesta_literal"] + espacios))
        == ref
    )
    assert calcular_id(base(respuesta_literal=base()["respuesta_literal"] + " " + extra)) != ref


def test_directorio_real_valida(repo: Path) -> None:
    assert cargar_feedback(repo / "knowledge" / "feedback") == []
