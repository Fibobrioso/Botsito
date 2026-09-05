"""Fotogramas (F05): indice, huecos, plan de instantes, obligatorios, esquema del manifiesto y
referencias citables. Puros: sin ffmpeg."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from botsito.comun import ids
from botsito.corpus.fotogramas import (
    Fotograma,
    FotogramasError,
    a_jsonl,
    cargar_obligatorios,
    desde_jsonl,
    huecos,
    mas_cercanos,
    nominal_de,
    parsear_showinfo,
    plan_instantes,
    referencia,
    validar_indice,
)
from botsito.corpus.manifiestos_fotogramas import (
    Fotogramas,
    ManifiestoFotogramasError,
    activa_de,
    cargar_todos,
    comprobar,
    comprobar_obligatorios,
    referencias_conocidas,
    validar,
)

SHA = "a" * 64
SHOWINFO = (
    "[Parsed_showinfo_1 @ 0x1] config in time_base: 1/30000, frame_rate: 30/1\n"
    "[Parsed_showinfo_1 @ 0x1] n:   1 pts:  30030 pts_time:1.001   duration: 1001 "
    "fmt:yuv420p sar:1/1 s:1762x884 i:P iskey:0 type:P checksum:1 mean:[1] stdev:[1]\n"
    "ruido\n"
    "[Parsed_showinfo_1 @ 0x1] n:   0 pts:      0 pts_time:0       duration: 1001 "
    "fmt:yuv420p sar:1/1 s:1762x884 i:P iskey:1 type:I checksum:1 mean:[1] stdev:[1]\n"
)


def _f(n: int, t: int, pts: int | None = None, origen: str = "regular") -> Fotograma:
    return Fotograma(n, t, t if pts is None else pts, f"{t:09d}.png", SHA, 10, origen)


def test_parsear_showinfo_ordena_y_da_resolucion() -> None:
    assert parsear_showinfo(SHOWINFO) == ([0, 1001], (1762, 884))
    assert parsear_showinfo("nada") == ([], None)
    with pytest.raises(FotogramasError, match="consecutiva"):
        parsear_showinfo(SHOWINFO.replace("n:   0", "n:   5"))


def test_nominal_y_referencia() -> None:
    assert nominal_de(1001) == 1000 and nominal_de(999) == 0 and nominal_de(1736033) == 1736000
    assert referencia("fr-v3-abcdef01", 1736000) == "fr-v3-abcdef01/1736000"
    assert ids.es_id_de("referencia_fotograma", "fr-v3-abcdef01/1736000")
    assert not ids.es_id_de("referencia_fotograma", "fr-v3-abcdef01/1736000.5")
    assert ids.es_id_de("fotogramas", "fr-v3-abcdef01")
    assert not ids.es_id_de("fotogramas", "tr-v3-a")


def test_plan_instantes_solo_fracciones_y_rechazos() -> None:
    assert plan_instantes([1000, 1250, 0, 999], 2000) == [999, 1250]
    with pytest.raises(FotogramasError, match="fuera del video"):
        plan_instantes([2000], 2000)
    assert plan_instantes([1999], 2000) == [1999]
    with pytest.raises(FotogramasError, match="repetido"):
        plan_instantes([1250, 1250], 2000)
    assert plan_instantes([], 0) == []


def test_huecos_sobre_pts_reales() -> None:
    assert huecos([_f(0, 0), _f(1, 1000), _f(2, 2000)], 2000) == []
    assert huecos([_f(0, 0), _f(1, 2000)], 2000) == []  # falta un segundo: no es hueco
    assert huecos([_f(0, 0), _f(1, 4000, 4033)], 2000) == [
        {"desde_ms": 0, "hasta_ms": 4033, "ms": 4033}
    ]
    assert huecos([_f(0, 3000)], 2000) == [{"desde_ms": 0, "hasta_ms": 3000, "ms": 3000}]
    assert huecos([], 2000) == []


def test_indice_ida_y_vuelta_y_rechazos() -> None:
    fs = [_f(0, 0), _f(1, 1000, 1033), _f(2, 1250, 1300, "obligatorio"), _f(3, 2000)]
    texto = a_jsonl(fs)
    assert desde_jsonl(texto) == fs
    assert texto.endswith("\n") and '"n": 0' in texto.splitlines()[0]
    with pytest.raises(FotogramasError, match="JSON"):
        desde_jsonl("{no json\n")
    with pytest.raises(FotogramasError, match="claves"):
        desde_jsonl('{"n": 0}\n')
    with pytest.raises(FotogramasError, match="entero"):
        desde_jsonl(texto.replace('"n": 0', '"n": true', 1))
    with pytest.raises(FotogramasError, match="vacio"):
        desde_jsonl("")
    with pytest.raises(FotogramasError, match="sha256"):
        _f(0, 0).__class__(0, 0, 0, "000000000.png", "zz", 1, "regular")
    with pytest.raises(FotogramasError, match="negativos"):
        Fotograma(0, -1, 0, "000000000.png", SHA, 1, "regular")
    with pytest.raises(FotogramasError, match="anterior"):
        Fotograma(0, 1000, 999, "000001000.png", SHA, 1, "regular")
    with pytest.raises(FotogramasError, match="fichero debe ser"):
        Fotograma(0, 1000, 1000, "x.png", SHA, 1, "regular")
    with pytest.raises(FotogramasError, match="origen"):
        Fotograma(0, 1000, 1000, "000001000.png", SHA, 1, "otro")


def test_validar_indice() -> None:
    with pytest.raises(FotogramasError, match="consecutivos"):
        validar_indice([_f(1, 0)])
    with pytest.raises(FotogramasError, match="posterior"):
        validar_indice([_f(0, 1000), _f(1, 1000)])
    with pytest.raises(FotogramasError, match="posterior"):
        validar_indice([_f(0, 0, 1500), _f(1, 1000, 1400)])
    with pytest.raises(FotogramasError, match="segundo entero"):
        validar_indice([_f(0, 500)])
    with pytest.raises(FotogramasError, match="deberia ser el regular"):
        validar_indice([_f(0, 1000, origen="obligatorio")])


def test_mas_cercanos() -> None:
    fs = [_f(0, 0), _f(1, 1000, 1033), _f(2, 2000, 2033)]
    assert [f.t_ms for f in mas_cercanos(fs, 1500, 1)] == [1000]  # empate: el anterior
    assert [f.t_ms for f in mas_cercanos(fs, 1900, 2)] == [1000, 2000]
    assert [f.t_ms for f in mas_cercanos(fs, 2900, 1)] == [2000]
    with pytest.raises(FotogramasError, match="fuera"):
        mas_cercanos(fs, 4000)
    with pytest.raises(FotogramasError, match="n debe"):
        mas_cercanos(fs, 0, 0)


def test_cargar_obligatorios(tmp_path: Path) -> None:
    ruta = tmp_path / "ob.yaml"
    assert cargar_obligatorios(ruta) == []
    ruta.write_text(
        "fotogramas:\n"
        "  - {video_id: v3, t: '0:28:56', motivo: excel, marca_heredada: 'V3 0:28:56'}\n"
        "  - {video_id: v4, t: '0:12:30.5', motivo: caja}\n",
        encoding="utf-8",
    )
    ob = cargar_obligatorios(ruta)
    assert [(o.video_id, o.t_ms, o.marca_heredada) for o in ob] == [
        ("v3", 1736000, "V3 0:28:56"),
        ("v4", 750500, None),
    ]
    for malo, msg in (
        ("fotogramas:\n  - {video_id: v3, t: '0:28:56'}\n", "faltan"),
        ("fotogramas:\n  - {video_id: v3, t: 'x', motivo: m}\n", "tiempo invalido"),
        ("fotogramas:\n  - {video_id: v3, t: '0:00:01', motivo: ' '}\n", "vacio"),
        ("fotogramas:\n  - {video_id: v3, t: '0:00:01', motivo: m, otro: 1}\n", "desconocidos"),
        (
            "fotogramas:\n  - {video_id: v3, t: '0:00:01', motivo: m}\n"
            "  - {video_id: v3, t: '0:00:01.000', motivo: m}\n",
            "repetido",
        ),
        ("- 1\n", "se espera"),
    ):
        ruta.write_text(malo, encoding="utf-8")
        with pytest.raises(FotogramasError, match=msg):
            cargar_obligatorios(ruta)


def _doc(**cambios: Any) -> dict[str, Any]:
    doc: dict[str, Any] = {
        "schema_version": 1,
        "fotogramas_id": "fr-v1-" + SHA[:8],
        "video_id": "v1",
        "fichero_video": "clip.mp4",
        "sha256_video": SHA,
        "duracion_video_s": 2.0,
        "resolucion": {"ancho": 320, "alto": 180},
        "ffmpeg": "9.0.1",
        "parametros": {"fps": 1, "formato": "png", "seleccion": "x", "bitexact": True},
        "carpeta": "fotogramas/v1/png-1fps",
        "n_fotogramas": 3,
        "n_regulares": 2,
        "ultimo_pts_ms": 1300,
        "hueco_fotogramas_ms": 2000,
        "huecos": [],
        "extra": [{"t_ms": 1250, "pts_ms": 1300, "sha256": SHA}],
        "sha256_index": SHA,
        "generado_el": "2026-09-05T00:00:00Z",
    }
    doc.update(cambios)
    return doc


def test_esquema_del_manifiesto() -> None:
    t = validar(_doc(), "manifiesto")
    assert t.id == "fr-v1-" + SHA[:8] and t.extra_ms == (1250,) and t.supersede is None
    assert t.referencias() == {f"fr-v1-{SHA[:8]}/{x}" for x in (0, 1000, 1250)}
    validar(_doc(huecos=[{"desde_ms": 0, "hasta_ms": 3000, "ms": 3000}]), "manifiesto")
    validar(_doc(carpeta="fotogramas/v1/png-1fps-deadbeef"), "manifiesto")
    for cambios, msg in (
        ({"fotogramas_id": "fr-v1-00000000"}, "8 primeros"),
        ({"carpeta": "fotogramas/v2/png-1fps"}, "carpeta"),
        ({"n_fotogramas": 5}, "n_regulares"),
        ({"extra": [{"t_ms": 1000, "pts_ms": 1000, "sha256": SHA}]}, "extra invalido"),
        ({"extra": [{"t_ms": 1250, "pts_ms": 1200, "sha256": SHA}]}, "extra invalido"),
        ({"huecos": [{"desde_ms": 5, "hasta_ms": 1, "ms": -4}]}, "hueco invalido"),
        ({"ultimo_pts_ms": 9000}, "supera"),
        ({"resolucion": {"ancho": 0, "alto": 1}}, "resolucion"),
        ({"parametros": {}}, "seleccion"),
        ({"reemplaza_a": "tr-v1-x-00000000"}, "reemplaza_a"),
        ({"otro": 1}, "desconocidos"),
        ({"schema_version": 2}, "schema_version"),
    ):
        with pytest.raises(ManifiestoFotogramasError, match=msg):
            validar(_doc(**cambios), "manifiesto")
    with pytest.raises(ManifiestoFotogramasError, match="faltan"):
        validar({k: v for k, v in _doc().items() if k != "huecos"}, "manifiesto")
    with pytest.raises(ManifiestoFotogramasError, match="llamarse"):
        validar(_doc(), "otro.yaml")


def _escribir(repo: Path, doc: dict[str, Any]) -> None:
    import yaml

    d = repo / "knowledge" / "corpus" / "fotogramas"
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{doc['fotogramas_id']}.yaml").write_text(yaml.safe_dump(doc), encoding="utf-8")


def test_cargar_todos_un_activo_por_video_y_reemplazos(tmp_path: Path) -> None:
    assert cargar_todos(tmp_path) == []
    a = _doc()
    b = _doc(fotogramas_id="fr-v1-" + "b" * 8, sha256_index="b" * 64)
    _escribir(tmp_path, a)
    _escribir(tmp_path, b)
    with pytest.raises(ManifiestoFotogramasError, match="2 extracciones activas"):
        cargar_todos(tmp_path)
    b["reemplaza_a"] = a["fotogramas_id"]
    _escribir(tmp_path, b)
    items = cargar_todos(tmp_path)
    assert activa_de(items, "v1").id == b["fotogramas_id"]
    with pytest.raises(ManifiestoFotogramasError, match="no hay extraccion"):
        activa_de(items, "v2")
    c = _doc(
        fotogramas_id="fr-v2-" + "c" * 8,
        sha256_index="c" * 64,
        video_id="v2",
        carpeta="fotogramas/v2/png-1fps",
        reemplaza_a=a["fotogramas_id"],
    )
    _escribir(tmp_path, c)
    with pytest.raises(ManifiestoFotogramasError, match="otro video"):
        cargar_todos(tmp_path)
    c["reemplaza_a"] = "fr-v2-00000000"
    _escribir(tmp_path, c)
    with pytest.raises(ManifiestoFotogramasError, match="no existe"):
        cargar_todos(tmp_path)


def test_referencias_conocidas_excluye_heredado_y_obligatorios(tmp_path: Path) -> None:
    t = validar(_doc(), "manifiesto")
    viejo = Fotogramas(
        "fr-v1-" + "0" * 8, "v1", "fotogramas/v1/png-1fps", "0" * 64, 1, 0, (), None, {}
    )
    corpus = {
        "ficheros": [
            {"ruta": "_procesado/frames/v1_60.jpg", "papel": "heredado_v2"},
            {"ruta": "Material adicional/x.xlsx", "papel": "material_adicional"},
            {"ruta": "video.mp4", "papel": "video_original"},
        ]
    }
    refs = referencias_conocidas([t, viejo], corpus)
    assert "Material adicional/x.xlsx" in refs and "_procesado/frames/v1_60.jpg" not in refs
    assert "video.mp4" not in refs
    assert f"fr-v1-{'0' * 8}/0" in refs and f"fr-v1-{SHA[:8]}/1250" in refs
    assert referencias_conocidas([], None) == set()
    from botsito.corpus.fotogramas import Obligatorio

    ob = [
        Obligatorio("v1", 1000, "m", None),
        Obligatorio("v1", 1250, "m", None),
        Obligatorio("v1", 1500, "m", None),
        Obligatorio("v2", 0, "m", None),
    ]
    fallos = comprobar_obligatorios([t], ob)
    assert len(fallos) == 2
    assert "v1 0:00:01.500" in fallos[0] and "v2 0:00:00" in fallos[1]


def test_comprobar_sin_datos_avisa(tmp_path: Path) -> None:
    t = validar(_doc(), "manifiesto")
    errores, avisos = comprobar([t], tmp_path)
    assert errores == [] and len(avisos) == 1 and "no esta en esta maquina" in avisos[0]
