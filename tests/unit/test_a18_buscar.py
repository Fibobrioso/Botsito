"""La busqueda de A-18 (`scripts/a18_buscar.py`), sobre una transcripcion SINTETICA.

Ninguna transcripcion real se lee aqui: el criterio se prueba antes de ejecutarlo, con segmentos
escritos a mano que ejercitan los terminos, los limites de palabra, las tildes, la frase partida
entre segmentos, la ventana de 45 s y la integridad contra el manifiesto.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]


def _cargar() -> ModuleType:
    nombre = "a18_buscar"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def b() -> ModuleType:
    return _cargar()


def _seg(b: ModuleType, n: int, t0_s: int, texto: str) -> object:
    return b.Segmento(n, t0_s * 1000, t0_s * 1000 + 4000, texto)


def _terminos(b: ModuleType, texto: str) -> list[str]:
    return [t for t, _, _ in b.coincidencias([_seg(b, 0, 0, texto)])]


def test_la_lista_cerrada_de_terminos_y_de_transcripciones(b: ModuleType) -> None:
    assert len(b.TERMINOS) == 36 == len(set(b.TERMINOS))
    assert len(b.ALCANCE) == 5
    assert not any(t.startswith("tr-v6-") for t in b.ALCANCE)
    assert b.VENTANA_MS == 45_000


def test_sin_distinguir_mayusculas_ni_tildes(b: ModuleType) -> None:
    assert _terminos(b, "La PROTECCIÓN") == ["protección"]
    assert _terminos(b, "la proteccion") == ["protección"]
    assert _terminos(b, "Relación") == ["relación"]
    assert _terminos(b, "el Take Profit") == ["take profit"]


def test_por_palabra_no_dentro_de_otra(b: ModuleType) -> None:
    assert _terminos(b, "una isla y un stopper, cajas y riesgos") == []
    assert _terminos(b, "el stop.") == ["stop"]
    assert _terminos(b, "el SL y el TP") == ["SL", "TP"]


def test_las_cifras_no_casan_dentro_de_otra_cifra(b: ModuleType) -> None:
    assert _terminos(b, "a 0.80") == ["0.80"]
    assert _terminos(b, "a 0.8") == ["0.8"]
    assert _terminos(b, "el 11% o el 100%") == ["100%"]
    assert _terminos(b, "el 1%") == ["1%"]
    assert _terminos(b, "el 80%") == ["80%"]
    assert _terminos(b, "1:3 y 1:30") == ["1:3"]


def test_una_frase_y_sus_palabras_casan_las_dos(b: ModuleType) -> None:
    assert _terminos(b, "stop loss") == ["stop", "stop loss"]
    assert _terminos(b, "toda la caja") == ["caja", "toda la caja"]


def test_una_frase_partida_entre_dos_segmentos_casa(b: ModuleType) -> None:
    segs = [_seg(b, 0, 10, "pongo toda la"), _seg(b, 1, 20, "caja entera")]
    encontradas = b.coincidencias(segs)
    assert ("toda la caja", 10_000, 24_000) in encontradas


def test_ventanas_de_45_s_se_unen_si_se_solapan(b: ModuleType) -> None:
    segs = [
        _seg(b, 0, 0, "hola"),
        _seg(b, 1, 100, "el stop"),
        _seg(b, 2, 150, "nada"),
        _seg(b, 3, 180, "el riesgo"),
        _seg(b, 4, 400, "el objetivo"),
        _seg(b, 5, 1000, "adios"),
    ]
    ps = b.pasajes("tr-x", segs)
    assert [(p.t0_ms, p.t1_ms) for p in ps] == [(55_000, 229_000), (355_000, 449_000)]
    assert ps[0].terminos == {"stop": 1, "riesgo": 1}
    assert [s.n for s in ps[0].segmentos] == [1, 2, 3]
    assert [s.n for s in ps[1].segmentos] == [4]


def test_el_formato_trae_el_texto_entero(b: ModuleType) -> None:
    p = b.pasajes("tr-x", [_seg(b, 7, 3600, "  pongo el SL por defecto  ")])[0]
    assert b.formato(p, 1) == [
        "=== PASAJE 1 | tr-x | 0:59:15-1:00:49 | SL x1",
        "[1:00:00-1:00:04] #7 pongo el SL por defecto",
    ]


def test_integridad_contra_el_manifiesto(
    b: ModuleType, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    tr = b.ALCANCE[0]
    cruda = tmp_path / "datos" / "transcripciones" / "vx" / "cruda.jsonl"
    cruda.parent.mkdir(parents=True)
    fila = {"n": 0, "t0_ms": 0, "t1_ms": 1000, "texto": "el stop"}
    cruda.write_text(json.dumps(fila) + "\n", encoding="utf-8")
    sha = hashlib.sha256(cruda.read_bytes()).hexdigest()
    manifiestos = tmp_path / "manifiestos"
    manifiestos.mkdir()
    (manifiestos / f"{tr}.yaml").write_text(
        f"carpeta: transcripciones/vx\nsha256_cruda: {sha}\n", encoding="utf-8"
    )
    monkeypatch.setattr(b, "MANIFIESTOS", manifiestos)
    monkeypatch.setattr(b, "DATOS", tmp_path / "datos")

    segmentos, real = b.leer(tr)
    assert real == sha and segmentos[0].texto == "el stop"
    cruda.write_text(json.dumps(fila | {"texto": "otro"}) + "\n", encoding="utf-8")
    with pytest.raises(b.IntegridadError, match="no es la que fija"):
        b.leer(tr)
    with pytest.raises(b.IntegridadError, match="fuera de la lista cerrada"):
        b.leer("tr-v6-large-v3-int8-float16-7718b3f4")
