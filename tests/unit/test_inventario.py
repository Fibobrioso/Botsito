import hashlib
import shutil
import warnings
from pathlib import Path

import pytest

from botsito.corpus.inventario import (
    InventarioError,
    cargar_fuentes,
    cargar_manifiesto,
    clasificar,
    comprobar_contra_disco,
    escribir_manifiesto,
    ffprobe_disponible,
    ffprobe_info,
    huecos_en_indice,
    inventariar,
    sha256_fichero,
    validar_manifiesto,
)

CLIP = Path(__file__).resolve().parents[1] / "fixtures" / "clip_2s.mp4"

FUENTES = """
raiz: "corpus"
videos:
  - video_id: v1
    fichero: "clip.mp4"
    drive_id: d1
    bytes: {bytes}
    fecha_grabacion: "2026-01-01"
    naturaleza: prueba
carpetas:
  - ruta: "_procesado"
    papel: heredado_v2
    descripcion: heredado
  - ruta: "Material adicional"
    papel: material_adicional
    descripcion: adicional
umbral_hueco_segundos: 1
"""


def _requiere_ffprobe() -> None:
    if ffprobe_disponible() is None:
        warnings.warn("ffprobe no esta en PATH: test de video omitido", stacklevel=2)
        pytest.skip("ffprobe no disponible")


def _corpus_tmp(tmp_path: Path) -> tuple[Path, Path]:
    raiz = tmp_path / "corpus"
    (raiz / "_procesado" / "v1" / "fr").mkdir(parents=True)
    (raiz / "Material adicional").mkdir()
    shutil.copy(CLIP, raiz / "clip.mp4")
    (raiz / "_procesado" / "v1" / "fr" / "index.txt").write_text(
        "c0_001.jpg 0:00:00 0.2\nc0_002.jpg 0:00:00 0.5\nc0_003.jpg 0:00:01 1.9\n",
        encoding="utf-8",
    )
    (raiz / "_procesado" / "nota.md").write_text("x", encoding="utf-8")
    (raiz / "Material adicional" / "balance.jpeg").write_bytes(b"\xff\xd8\xff")
    fuentes = tmp_path / "fuentes.yaml"
    fuentes.write_text(FUENTES.format(bytes=CLIP.stat().st_size), encoding="utf-8")
    return tmp_path, fuentes


def test_huecos_en_indice() -> None:
    texto = "a.jpg 0:00:10 10\nb.jpg 0:00:20 20\nc.jpg 0:05:00 300\n"
    huecos = huecos_en_indice(texto, 180, duracion_s=600)
    assert [(h["desde_s"], h["hasta_s"]) for h in huecos] == [(20.0, 300.0), (300.0, 600.0)]
    assert huecos_en_indice(texto, 1000) == []
    assert huecos_en_indice("basura\n", 5, duracion_s=10) == [
        {"desde_s": 0.0, "hasta_s": 10.0, "segundos": 10.0}
    ]


def test_sha256_igual_a_hashlib(tmp_path: Path) -> None:
    f = tmp_path / "f.bin"
    f.write_bytes(b"abc" * 10_000)
    assert sha256_fichero(f, bloque=7) == hashlib.sha256(b"abc" * 10_000).hexdigest()


def test_cargar_fuentes_y_clasificar(tmp_path: Path) -> None:
    _, ruta = _corpus_tmp(tmp_path)
    fuentes = cargar_fuentes(ruta)
    assert clasificar("clip.mp4", fuentes) == "video_original"
    assert clasificar("_procesado/v1/fr/index.txt", fuentes) == "heredado_v2"
    assert clasificar("Material adicional/balance.jpeg", fuentes) == "material_adicional"
    assert clasificar("otro.txt", fuentes) == "sin_clasificar"


def test_fuentes_invalidas(tmp_path: Path) -> None:
    ruta = tmp_path / "f.yaml"
    ruta.write_text("raiz: c\nvideos:\n  - video_id: v1\n", encoding="utf-8")
    with pytest.raises(InventarioError, match="esquema"):
        cargar_fuentes(ruta)
    ruta.write_text(
        FUENTES.format(bytes=1).replace("papel: heredado_v2", "papel: otro"), encoding="utf-8"
    )
    with pytest.raises(InventarioError, match="papel"):
        cargar_fuentes(ruta)


def test_ffprobe_sobre_fixture() -> None:
    _requiere_ffprobe()
    info = ffprobe_info(CLIP)
    assert abs(info.duracion_s - 2.0) < 0.2
    assert (info.ancho, info.alto) == (320, 180)
    assert info.audio is True


def test_inventario_completo_y_determinista(tmp_path: Path) -> None:
    _requiere_ffprobe()
    repo, ruta_fuentes = _corpus_tmp(tmp_path)
    fuentes = cargar_fuentes(ruta_fuentes)
    m1 = inventariar(repo, fuentes)
    m2 = inventariar(repo, fuentes)
    assert m1 == m2
    assert m1["videos"][0]["sha256"] == sha256_fichero(CLIP)
    assert m1["resumen"]["video_original"]["ficheros"] == 1
    assert m1["resumen"]["heredado_v2"]["ficheros"] == 2
    assert m1["resumen"]["material_adicional"]["ficheros"] == 1
    indice = m1["indices_heredados"][0]
    assert indice["video_id"] == "v1" and indice["fotogramas"] == 3
    assert indice["huecos"][0]["desde_s"] == 0.5  # 0.5 -> 1.9 supera el umbral de 1 s
    assert validar_manifiesto(m1, fuentes) == []
    salida = tmp_path / "manifest.yaml"
    escribir_manifiesto(m1, salida)
    assert cargar_manifiesto(salida) == m1
    assert comprobar_contra_disco(m1, repo, hashes=True) == []


def test_video_ausente_o_con_tamano_distinto(tmp_path: Path) -> None:
    _requiere_ffprobe()
    repo, ruta_fuentes = _corpus_tmp(tmp_path)
    fuentes = cargar_fuentes(ruta_fuentes)
    (repo / "corpus" / "clip.mp4").write_bytes(b"corto")
    with pytest.raises(InventarioError, match="esperados"):
        inventariar(repo, fuentes)
    (repo / "corpus" / "clip.mp4").unlink()
    with pytest.raises(InventarioError, match="falta el video"):
        inventariar(repo, fuentes)


def test_validar_y_comprobar_detectan(tmp_path: Path) -> None:
    _requiere_ffprobe()
    repo, ruta_fuentes = _corpus_tmp(tmp_path)
    fuentes = cargar_fuentes(ruta_fuentes)
    m = inventariar(repo, fuentes, hashear=False)
    assert any("sha256" in p for p in validar_manifiesto(m, fuentes))
    m["videos"][0]["sha256"] = "x"
    m["ficheros"].append({"ruta": "nuevo.txt", "papel": "sin_clasificar", "bytes": 1})
    assert any("sin clasificar" in p for p in validar_manifiesto(m, fuentes))
    assert any("falta en disco" in p for p in comprobar_contra_disco(m, repo))


def test_fuentes_y_manifiesto_reales_coherentes(repo: Path) -> None:
    fuentes = cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml")
    assert [v.video_id for v in fuentes.videos] == ["v1", "v2", "v3", "v4"]
    ruta = repo / "knowledge" / "corpus" / "manifest.yaml"
    if not ruta.exists():
        pytest.skip("manifiesto real todavia no generado")
    assert validar_manifiesto(cargar_manifiesto(ruta), fuentes) == []
