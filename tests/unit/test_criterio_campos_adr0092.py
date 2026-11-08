"""Los campos que ADR-0092 añade a `criterio_fidelidad.yaml` (§13): sin ellos, el yaml NO carga.

Este fichero importa SOLO lo que ya existia en `main` antes de ADR-0092 (`cargar_criterio`,
`CriterioError`, `FICHERO_CRITERIO`), a proposito: en `main` sus tests ROMPEN por lo que miden (un
yaml sin los campos nuevos carga sin error), no por un import que falta. Todo sintetico: copias del
yaml real en una carpeta temporal, con un campo quitado o cambiado."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import FICHERO_CRITERIO, CriterioError, cargar_criterio

REPO = Path(__file__).resolve().parents[2]
CAMPOS_DEL_BLOQUE = (
    "fase",
    "n_minimo",
    "esperanza_minima_r",
    "percentil_remuestreo",
    "replicas_remuestreo",
    "semilla_remuestreo",
    "perdida_diaria_max",
    "perdida_total_max",
    "deslizamiento",
    "percentil_deslizamiento_f17",
    "meses",
    "extension",
    "vistos_rentabilidad",
)


def _copia(
    tmp_path: Path,
    quitar: str | None = None,
    cambiar: dict[str, str] | None = None,
    bloque: str | None = None,
) -> Path:
    """El yaml real con una linea quitada (por su clave, con o sin sangria) o cambiada. Quitar
    `rentabilidad` o `material_sin_video` quita el bloque entero. Con `bloque`, una clave
    sangrada solo se toca dentro de ese bloque (`meses` vive en dos)."""
    cambiar = cambiar or {}
    salida: list[str] = []
    en_bloque_quitado = False
    actual = ""
    for linea in (REPO / FICHERO_CRITERIO).read_text(encoding="utf-8").splitlines():
        clave = linea.split(":", 1)[0].strip()
        sangrada = linea.startswith(" ")
        comentario = linea.lstrip().startswith("#")
        if not sangrada and not comentario and linea.strip():
            actual = clave
        if en_bloque_quitado and sangrada:
            continue
        en_bloque_quitado = False
        aqui = bloque is None or not sangrada or actual == bloque
        if quitar is not None and clave == quitar and not comentario and aqui:
            en_bloque_quitado = not sangrada
            continue
        if clave in cambiar and not comentario and aqui:
            sangria = linea[: len(linea) - len(linea.lstrip())]
            salida.append(f"{sangria}{clave}: {cambiar[clave]}")
            continue
        salida.append(linea)
    ruta = tmp_path / FICHERO_CRITERIO
    ruta.parent.mkdir(parents=True)
    ruta.write_text("\n".join(salida) + "\n", encoding="utf-8")
    return tmp_path


def test_el_yaml_real_carga() -> None:
    cargar_criterio(REPO)


def test_sin_la_tolerancia_del_stop_no_carga(tmp_path: Path) -> None:
    with pytest.raises(CriterioError, match="tolerancia_stop_puntos"):
        cargar_criterio(_copia(tmp_path, quitar="tolerancia_stop_puntos"))


def test_sin_el_bloque_de_rentabilidad_no_carga(tmp_path: Path) -> None:
    with pytest.raises(CriterioError, match="rentabilidad"):
        cargar_criterio(_copia(tmp_path, quitar="rentabilidad"))


@pytest.mark.parametrize("campo", CAMPOS_DEL_BLOQUE)
def test_sin_un_campo_del_bloque_no_carga(tmp_path: Path, campo: str) -> None:
    with pytest.raises(CriterioError, match=campo):
        cargar_criterio(_copia(tmp_path, quitar=campo, bloque="rentabilidad"))


# --------------------------- material_sin_video (respuesta del consultor a la PARADA 2, punto 1)


def test_sin_el_bloque_del_material_sin_video_no_carga(tmp_path: Path) -> None:
    with pytest.raises(CriterioError, match="material_sin_video"):
        cargar_criterio(_copia(tmp_path, quitar="material_sin_video"))


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("meses", '["2026-05"]'),  # un mes que no es de construccion (es de medida)
        ("dias_con_video", '["2026-05-12"]'),  # un dia que no es de construccion
        ("dias_con_video", '["2026-07-01"]'),  # un dia de construccion fuera de `meses`
        ("provisionales_con_video", '["2026-08"]'),  # en `meses` y en provisionales a la vez
        ("provisionales_con_video", '["2026-03"]'),  # un mes que no es de construccion
        ("dias_con_video", '["2026-04-31"]'),  # no es una fecha
    ],
)
def test_el_material_sin_video_mal_formado_no_carga(tmp_path: Path, campo: str, valor: str) -> None:
    with pytest.raises(CriterioError, match="material_sin_video|dias_con_video|provisionales"):
        cargar_criterio(_copia(tmp_path, cambiar={campo: valor}, bloque="material_sin_video"))


@pytest.mark.parametrize(
    ("campo", "valor"),
    [
        ("tolerancia_stop_puntos", '"3"'),  # un texto, no un entero
        ("esperanza_minima_r", "0.10"),  # un numero de coma flotante, no un texto
        ("esperanza_minima_r", '"diez"'),
        ("perdida_diaria_max", '"1.5"'),  # fuera de 0..1
        ("percentil_remuestreo", "100"),
        ("deslizamiento", "medido_a_ojo"),
        ("meses", '["2025-13"]'),
        ("meses", "[]"),
        ("extension", '["2025-06"]'),  # el mismo mes en meses y en extension
        ("meses", '["2026-04"]'),  # un mes de construccion
    ],
)
def test_un_valor_mal_formado_no_carga(tmp_path: Path, campo: str, valor: str) -> None:
    with pytest.raises(CriterioError):
        cargar_criterio(_copia(tmp_path, cambiar={campo: valor}))
