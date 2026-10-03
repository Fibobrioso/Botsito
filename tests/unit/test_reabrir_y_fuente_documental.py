"""Reabrir una ambiguedad (REOPEN) y la fuente documental (rama trabajo/reabrir-y-fuente-documental,
decisiones del consultor del 2026-10-03). Cada guardia nueva tiene aqui su caso que la rompe a
proposito; el informe (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md) mide que cada test falla con
su guardia rota y pasa sin ella."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.cases.ambiguedades import (
    FICHERO_AMBIGUEDADES,
    AmbiguedadError,
    cargar_ambiguedades,
)
from botsito.cli import ContextoPendiente, situacion_de
from botsito.feedback.modelo import (
    FeedbackError,
    FeedbackRecord,
    cargar_feedback,
    cargar_registro,
    escribir_registro,
    validar_contra_contexto,
)
from botsito.validation.knowledge import (
    plano,
    problemas_de_cierre,
    problemas_fuentes_documentales,
    seccion_de,
)

REPO = Path(__file__).resolve().parents[2]
AMB = "A-7"


def _fb(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "sesion": "2026-09-20-sesion-01",
        "fecha": "2026-09-20",
        "medio": "escrito",
        "objetivo": {"tipo": "ambiguedad", "id": AMB},
        "accion": "RESOLVE_UNKNOWN",
        "respuesta_literal": "con cuerpo, siempre con cuerpo",
        "valor_resultante": "cuerpo",
        "registrado_por": "aleks",
        "recibido_el": "2026-09-20",
        "procedencia": "trader_escrito",
    }
    d.update(cambios)
    return d


def _reopen(supersede: str, **cambios: Any) -> dict[str, Any]:
    d = _fb(
        accion="REOPEN",
        respuesta_literal="no se cierra: la pregunta era otra",
        valor_resultante=None,
        procedencia="correccion_consultor",
        supersede=supersede,
        recibido_el="2026-09-21",
    )
    d.update(cambios)
    return {k: v for k, v in d.items() if v is not None}


def _amb(estado: str, aid: str = AMB, **cambios: Any) -> dict[str, Any]:
    bruto: dict[str, Any] = {
        "id": aid,
        "titulo": "t",
        "pregunta": "p",
        "resuelve_en": ["F11"],
        "evidencia": ["ev-v4-001533-1a2b3c4d"],
        "parametros": [],
        "contradiccion": None,
        "estado": estado,
        "decision": "ADR-0022" if estado == "DECIDIDA" else None,
        "decidida_el": "2026-09-12" if estado == "DECIDIDA" else None,
        "bloqueante": False,
        "clase": "pregunta",
    }
    bruto.update(cambios)
    return bruto


def _cargar_ambs(tmp_path: Path, *brutas: dict[str, Any]) -> list[Any]:
    # con `_` delante: el cargador de feedback, que lee la misma carpeta, salta esos ficheros
    ruta = tmp_path / "_ambiguedades.yaml"
    ruta.write_text(yaml.safe_dump({"ambiguedades": list(brutas)}), encoding="utf-8")
    return cargar_ambiguedades(ruta)


def _contexto(registros: list[FeedbackRecord]) -> list[str]:
    return validar_contra_contexto(registros, set(), set(), set(), ids_ambiguedades={AMB, "A-8"})


# ----------------------------------------------------------------------------------- REOPEN


def test_el_ciclo_cerrar_reabrir_volver_a_cerrar_funciona(tmp_path: Path) -> None:
    cierre = cargar_registro(escribir_registro(tmp_path, _fb()))
    assert problemas_de_cierre(_cargar_ambs(tmp_path, _amb("RESUELTA")), [cierre]) == []
    reapertura = cargar_registro(escribir_registro(tmp_path, _reopen(cierre.id)))
    regs = cargar_feedback(tmp_path)
    assert _contexto(regs) == []
    abierta = _cargar_ambs(tmp_path, _amb("ABIERTA"))
    assert problemas_de_cierre(abierta, regs) == []
    ctx = ContextoPendiente({}, {AMB: "ABIERTA"}, {}, frozenset(), "")
    assert situacion_de(ctx, reapertura)[0] == "reflejado"
    escribir_registro(
        tmp_path,
        _fb(
            respuesta_literal="ahora si: con mecha",
            valor_resultante="mecha",
            supersede=reapertura.id,
            recibido_el="2026-09-22",
        ),
    )
    regs = cargar_feedback(tmp_path)
    assert _contexto(regs) == []
    assert problemas_de_cierre(_cargar_ambs(tmp_path, _amb("RESUELTA")), regs) == []


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        # con `trader_escrito`, que por si sola no exige supersede: asi solo la guardia de REOPEN
        # puede pararlo (con `correccion_consultor` lo paraba la de la procedencia, medido)
        ({"supersede": None, "procedencia": "trader_escrito"}, "REOPEN exige `supersede`"),
        ({"valor_resultante": "abierta"}, "no fija ningun valor"),
        ({"respuesta_literal": "no"}, "respuesta_literal"),
        ({"objetivo": {"tipo": "parametro", "id": "stop_fraccion"}}, "exige objetivo de tipo"),
    ],
)
def test_un_reopen_mal_formado_no_se_escribe(
    tmp_path: Path, cambio: dict[str, Any], mensaje: str
) -> None:
    campos = _reopen("fb-2026-09-20-sesion-01-deadbeef")
    campos.update(cambio)
    campos = {k: v for k, v in campos.items() if v is not None}
    with pytest.raises(FeedbackError, match=mensaje):
        escribir_registro(tmp_path, campos)


def test_un_reopen_sobre_una_ambiguedad_que_nunca_se_cerro_falla(tmp_path: Path) -> None:
    escribir_registro(tmp_path, _reopen("fb-2026-09-20-sesion-01-deadbeef"))
    problemas = _contexto(cargar_feedback(tmp_path))
    assert any("no hay nada que reabrir" in p for p in problemas), problemas


def test_un_reopen_sobre_una_decidida_falla(tmp_path: Path) -> None:
    cierre = cargar_registro(escribir_registro(tmp_path, _fb()))
    escribir_registro(tmp_path, _reopen(cierre.id))
    ambs = _cargar_ambs(tmp_path, _amb("DECIDIDA", clase=None))
    problemas = problemas_de_cierre(ambs, cargar_feedback(tmp_path))
    assert any("solo la reabre otro ADR" in p for p in problemas), problemas


def test_un_reopen_activo_exige_que_este_abierta(tmp_path: Path) -> None:
    cierre = cargar_registro(escribir_registro(tmp_path, _fb()))
    escribir_registro(tmp_path, _reopen(cierre.id))
    problemas = problemas_de_cierre(
        _cargar_ambs(tmp_path, _amb("RESUELTA")), cargar_feedback(tmp_path)
    )
    assert any("el YAML tiene que decir ABIERTA" in p for p in problemas), problemas


def test_una_resuelta_cuyo_unico_cierre_esta_superseded_falla(tmp_path: Path) -> None:
    """La guardia nueva de RESUELTA: el cierre tiene que estar ACTIVO. Con la de antes (todos los
    registros, tambien los superseded), esta RESUELTA pasaba."""
    cierre = cargar_registro(escribir_registro(tmp_path, _fb()))
    escribir_registro(tmp_path, _reopen(cierre.id))
    problemas = problemas_de_cierre(
        _cargar_ambs(tmp_path, _amb("RESUELTA")), cargar_feedback(tmp_path)
    )
    assert any("ningun registro de feedback ACTIVO la cierra" in p for p in problemas), problemas


def test_pending_ve_un_reopen_sobre_una_cerrada_como_pendiente(tmp_path: Path) -> None:
    cierre = cargar_registro(escribir_registro(tmp_path, _fb()))
    reapertura = cargar_registro(escribir_registro(tmp_path, _reopen(cierre.id)))
    ctx = ContextoPendiente({}, {AMB: "RESUELTA"}, {}, frozenset(), "")
    assert situacion_de(ctx, reapertura)[0] == "pendiente"


def test_a36_esta_migrada_y_pending_ya_no_la_cuenta() -> None:
    regs = cargar_feedback(REPO / "knowledge" / "feedback")
    por_id = {r.id: r for r in regs}
    reapertura = por_id["fb-2026-09-29-sesion-03-f3caeb2d"]
    assert (reapertura.accion, reapertura.supersede) == (
        "REOPEN",
        "fb-2026-09-29-sesion-03-a0b61bc9",
    )
    assert reapertura.procedencia == "reexpresion_consultor"
    assert (reapertura.fecha, reapertura.recibido_el) == ("2026-09-29", "2026-10-02")
    ambs = cargar_ambiguedades(REPO / FICHERO_AMBIGUEDADES)
    estados = {a.id: a.estado for a in ambs}
    assert estados["A-36"] == "ABIERTA"
    ctx = ContextoPendiente({}, estados, {}, frozenset(), "")
    assert situacion_de(ctx, reapertura)[0] == "reflejado"
    assert problemas_de_cierre(ambs, regs) == []


# ----------------------------------------------------------------------- fuente documental

DOC = "docs/validation/REGLAS.md"
TEXTO = """# Reglas

## 1. Lo de antes

Fuera de la seccion: el literal de prueba esta aqui.

## 2. Las reglas

| R1 | el literal de prueba | fuente |

> Recuadro que parte
> > el literal en
> > varias lineas.

### 2.1 Una subseccion

dentro de la 2 todavia.

## 3. Lo de despues

otra cosa.
"""


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True)


def _repo(tmp_path: Path, commitear: bool = True) -> Path:
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / DOC).write_text(TEXTO, encoding="utf-8")
    _git(tmp_path, "init", "-q")
    if commitear:
        _git(tmp_path, "add", DOC)
        _git(tmp_path, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "doc")
    return tmp_path


def _medicion(**fuente: str) -> dict[str, Any]:
    f = {"documento": DOC, "ancla": "2. Las reglas", "literal": "el literal de prueba"}
    f.update(fuente)
    return _amb("ABIERTA", clase="medicion", evidencia=[], fuentes_documentales=[f])


def test_una_fuente_documental_valida_pasa(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    ambs = _cargar_ambs(tmp_path, _medicion())
    assert problemas_fuentes_documentales(repo, ambs, con_git=True) == []
    # el literal partido en lineas de una cita, y la subseccion, cuentan como de la seccion
    partido = _cargar_ambs(tmp_path, _medicion(literal="el literal en varias lineas."))
    assert problemas_fuentes_documentales(repo, partido, con_git=True) == []
    sub = _cargar_ambs(tmp_path, _medicion(literal="dentro de la 2 todavia."))
    assert problemas_fuentes_documentales(repo, sub, con_git=True) == []


@pytest.mark.parametrize(
    ("documento", "mensaje"),
    [
        ("docs/../knowledge/x.md", "lleva `..`"),
        ("docs/validation/../../x.md", "lleva `..`"),
        ("knowledge/spec/x.md", "fuera de `docs/`"),
        ("/etc/passwd", "no es una ruta relativa"),
        ("C:/x/docs/a.md", "no es una ruta relativa"),
        ("docs\\validation\\REGLAS.md", "no es una ruta relativa"),
        ("docs", "fuera de `docs/`"),
    ],
)
def test_una_ruta_que_sale_de_docs_se_niega_antes_de_leer(
    tmp_path: Path, documento: str, mensaje: str
) -> None:
    with pytest.raises(AmbiguedadError, match=mensaje):
        _cargar_ambs(tmp_path, _medicion(documento=documento))


def test_un_enlace_que_sale_de_docs_se_niega(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    fuera = tmp_path / "fuera.md"
    fuera.write_text(TEXTO, encoding="utf-8")
    enlace = tmp_path / "docs" / "enlace.md"
    try:
        os.symlink(fuera, enlace)
    except OSError:
        pytest.skip("este sistema no deja crear enlaces simbolicos (Windows sin permiso)")
    ambs = _cargar_ambs(tmp_path, _medicion(documento="docs/enlace.md"))
    problemas = problemas_fuentes_documentales(repo, ambs, con_git=True)
    assert any("sale de docs/" in p for p in problemas), problemas


def test_un_documento_sin_commitear_se_niega(tmp_path: Path) -> None:
    repo = _repo(tmp_path, commitear=False)
    problemas = problemas_fuentes_documentales(
        repo, _cargar_ambs(tmp_path, _medicion()), con_git=True
    )
    assert any("no esta commiteado" in p for p in problemas), problemas
    # sin git, «commiteado» no se evalua (como el resto del historial en `validar`), pero la
    # ruta, el encabezado y el literal se siguen comprobando
    sin_git = problemas_fuentes_documentales(
        repo, _cargar_ambs(tmp_path, _medicion()), con_git=False
    )
    assert sin_git == [], sin_git
    roto = problemas_fuentes_documentales(
        repo, _cargar_ambs(tmp_path, _medicion(literal="no esta en el documento")), con_git=False
    )
    assert any("el literal no esta" in p for p in roto), roto


def test_un_documento_que_no_existe_se_niega(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    ambs = _cargar_ambs(tmp_path, _medicion(documento="docs/validation/OTRO.md"))
    assert any("no existe" in p for p in problemas_fuentes_documentales(repo, ambs, True))


def test_un_ancla_que_no_es_un_encabezado_se_niega(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    # el texto existe en el documento, pero no como encabezado
    ambs = _cargar_ambs(tmp_path, _medicion(ancla="R1"))
    problemas = problemas_fuentes_documentales(repo, ambs, con_git=True)
    assert any("no tiene el encabezado" in p for p in problemas), problemas


def test_un_literal_fuera_de_su_seccion_se_niega(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    # «otra cosa.» esta en el fichero, pero en la seccion 3
    ambs = _cargar_ambs(tmp_path, _medicion(literal="otra cosa."))
    problemas = problemas_fuentes_documentales(repo, ambs, con_git=True)
    assert any("no esta dentro de la seccion" in p for p in problemas), problemas


@pytest.mark.parametrize("clase", ["pregunta", None])
def test_una_fuente_documental_en_una_pregunta_se_niega(tmp_path: Path, clase: str | None) -> None:
    bruto = _medicion()
    bruto["clase"] = clase
    if clase is None:
        del bruto["clase"]
    with pytest.raises(AmbiguedadError, match="solo en clase `medicion`"):
        _cargar_ambs(tmp_path, bruto)


def test_la_evidencia_vacia_solo_con_una_fuente_documental(tmp_path: Path) -> None:
    with pytest.raises(AmbiguedadError, match="al menos un item de evidencia"):
        _cargar_ambs(tmp_path, _amb("ABIERTA", clase="medicion", evidencia=[]))


def test_la_seccion_acaba_en_el_siguiente_encabezado_de_su_nivel() -> None:
    seccion = seccion_de(TEXTO, "2. Las reglas")
    assert seccion is not None
    assert "dentro de la 2 todavia." in seccion and "otra cosa." not in seccion
    assert seccion_de(TEXTO, "no existe") is None
    assert plano("> a\n> > b  c") == "a b c"


def test_las_cuatro_migradas_citan_su_regla_y_el_relleno_solo_queda_en_a44() -> None:
    ambs = {a.id: a for a in cargar_ambiguedades(REPO / FICHERO_AMBIGUEDADES)}
    assert problemas_fuentes_documentales(REPO, ambs.values(), con_git=True) == []
    for aid in ("A-27", "A-28", "A-54", "A-55"):
        assert ambs[aid].fuentes_documentales, aid
        assert "ev-v4-012524-0ef85a89" not in ambs[aid].evidencia, aid
    assert ambs["A-54"].evidencia == () and ambs["A-55"].evidencia == ()
    con_relleno = sorted(a for a, x in ambs.items() if "ev-v4-012524-0ef85a89" in x.evidencia)
    assert con_relleno == ["A-44"]  # una pregunta: su evidencia es del trader (decision 4)
