"""Las filtradas de sesion con los tramos no citables (`trabajo/filtradas-con-tramos`, punto Q;
docs/validation/FILTRADAS-CON-TRAMOS.md).

Todo es sintetico: ningun test lee una cruda ni una filtrada real. Los segmentos los escribe el
test, y el fichero de tramos es el de un repo de juguete en `tmp_path`. Cada regla va con el caso
negativo que demuestra que la comprobacion puede fallar.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[2]
VALIDOS = ("A-35", "A-21")


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "transcribir_sesion"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _segs(m: ModuleType, tiempos: list[tuple[int, int, str]]) -> list[Any]:
    return [m.Seg(a, b, t) for a, b, t in tiempos]


def _tramo(a: int, b: int) -> tuple[int, int, str]:
    return (a, b, "MOTIVO-SINTETICO")


# --------------------------------------------------------------------------- la regla de > 0 ms


def test_un_solape_de_1_ms_tapa(m: ModuleType) -> None:
    segs = _segs(m, [(1000, 2000, "uno")])
    assert m.tapados_por_tramos(segs, [_tramo(1999, 5000)]) == {0}  # se mete 1 ms por el final
    assert m.tapados_por_tramos(segs, [_tramo(0, 1001)]) == {0}  # 1 ms por el principio
    assert m.tapados_por_tramos(segs, [_tramo(1500, 1600)]) == {0}  # dentro


def test_termina_justo_en_el_inicio_del_tramo_queda_visible(m: ModuleType) -> None:
    segs = _segs(m, [(1000, 2000, "uno")])
    assert m.tapados_por_tramos(segs, [_tramo(2000, 5000)]) == frozenset()
    assert m.tapados_por_tramos(segs, [_tramo(1999, 5000)]) == {0}  # el negativo: 1 ms antes


def test_empieza_justo_en_el_fin_del_tramo_queda_visible(m: ModuleType) -> None:
    segs = _segs(m, [(3000, 4000, "tres")])
    assert m.tapados_por_tramos(segs, [_tramo(0, 3000)]) == frozenset()
    assert m.tapados_por_tramos(segs, [_tramo(0, 3001)]) == {0}  # el negativo: 1 ms despues


def test_el_caso_de_borde_de_v9_0_34_56(m: ModuleType) -> None:
    """FILTRADAS-ESCENARIO-B.md §4.1: el ultimo segmento oculto termina en 2.096.900 y el
    siguiente, el del item, empieza en 2.098.060; el tramo original termina en 2.096.000. Con
    tiempos sinteticos: el segmento del item queda visible y el oculto, tapado."""
    segs = _segs(m, [(2_090_000, 2_096_900, "oculto"), (2_098_060, 2_100_240, "del item")])
    tramo = [_tramo(2_084_000, 2_096_000)]
    assert m.tapados_por_tramos(segs, tramo) == {0}
    lineas, _ = m.lineas_filtradas(segs, VALIDOS, frozenset(range(1, 13)), tramo)
    texto = m.version_filtrada(lineas, "prueba", ())
    assert "[NO CITABLE 34:50–34:56]" in texto and "oculto" not in texto
    assert "[34:58] del item" in texto
    # El negativo: un segmento que empieza justo en el fin del tramo tampoco se tapa.
    borde = _segs(m, [(2_096_000, 2_100_000, "en el borde")])
    assert m.tapados_por_tramos(borde, tramo) == frozenset()


# --------------------------------------------------------------------------- la marca y los bloques


def test_la_marca_no_lleva_texto_ni_clase_ni_motivo_y_los_contiguos_se_funden(
    m: ModuleType,
) -> None:
    segs = _segs(
        m,
        [(0, 1000, "antes"), (1000, 2000, "SECRETO uno"), (2000, 3000, "SECRETO dos"),
         (3000, 4000, "despues")],
    )  # fmt: skip
    tramos = [(1500, 2500, "precaucion: MOTIVO-QUE-NO-SALE")]
    lineas, _ = m.lineas_filtradas(segs, VALIDOS, frozenset(range(1, 13)), tramos)
    texto = m.version_filtrada(lineas, "prueba", ())
    # «[NO CITABLE 0» y «[CUARENTENA 0» son marcas; la cabecera solo nombra «[NO CITABLE]».
    assert texto.count("[NO CITABLE 0") == 1 and "[NO CITABLE 00:01–00:03]" in texto
    assert "SECRETO" not in texto and "MOTIVO" not in texto and "precaucion" not in texto
    assert "[CUARENTENA 0" not in texto
    assert "[00:00] antes" in texto and "[00:03] despues" in texto
    # El negativo: sin tramos, el texto sale.
    sin, _ = m.lineas_filtradas(segs, VALIDOS, frozenset(range(1, 13)))
    assert "SECRETO uno" in m.version_filtrada(sin, "prueba", ())


def test_un_segmento_de_las_dos_reglas_cuenta_en_ambos_y_sale_una_vez(m: ModuleType) -> None:
    textos = [
        (0, 1000, "hola"),
        (1000, 2000, "otra cosa"),  # vecino del mes: meses
        (2000, 3000, "fue en septiembre"),  # mes y tramo: ambos
        (3000, 4000, "y luego"),  # vecino del mes: meses
        (4000, 5000, "fin"),
    ]
    segs = _segs(m, textos)
    tramos = [_tramo(2000, 3000)]
    lineas, cuarentena = m.lineas_filtradas(segs, VALIDOS, None, tramos)
    assert set(cuarentena) == {1, 2, 3}
    tapados = m.tapados_por_tramos(segs, tramos)
    assert tapados == {2}
    registro = "\n".join(m.registro_filtro(lineas, cuarentena, VALIDOS, (), tapados))
    assert "solo por meses 2, solo por tramos 0, por ambos 1" in registro
    assert "bloques [NO CITABLE]: 1" in registro
    assert "segmentos en cuarentena: 3 en 2 bloques" in registro
    texto = m.version_filtrada(lineas, "prueba", ())
    assert "septiembre" not in texto and "otra cosa" not in texto and "y luego" not in texto
    # El segmento de las dos reglas sale en UN bloque, el [NO CITABLE], y no en uno de cada.
    assert texto.count("00:02–00:03") == 1 and "[NO CITABLE 00:02–00:03]" in texto
    assert sum(len(ln.indices) for ln in lineas) == len(segs)
    # El negativo: con el tramo lejos del mes, «ambos» es 0.
    lejos = [_tramo(4000, 5000)]
    l2, c2 = m.lineas_filtradas(segs, VALIDOS, None, lejos)
    r2 = "\n".join(m.registro_filtro(l2, c2, VALIDOS, (), m.tapados_por_tramos(segs, lejos)))
    assert "solo por meses 3, solo por tramos 1, por ambos 0" in r2


def test_el_registro_no_trae_texto_ni_motivo(m: ModuleType) -> None:
    segs = _segs(m, [(0, 1000, "pregunta A-35"), (1000, 2000, "SECRETO"), (2000, 3000, "otra")])
    tramos = [(1000, 2000, "MOTIVO-SECRETO")]
    lineas, cuarentena = m.lineas_filtradas(segs, VALIDOS, frozenset(range(1, 13)), tramos)
    registro = "\n".join(
        m.registro_filtro(lineas, cuarentena, VALIDOS, (), m.tapados_por_tramos(segs, tramos))
    )
    assert "SECRETO" not in registro and "MOTIVO" not in registro
    assert "solo por tramos 1" in registro


# ------------------------------------------------------------------ el video y los tramos

_TRAMOS_YAML = """tramos:
  - video_id: v8
    t0: "0:00:01"
    t1: "0:00:03"
    motivo: sintetico
    acordado: sintetico
"""


def _repo(tmp_path: Path, contenido: str | None = _TRAMOS_YAML) -> Path:
    repo = tmp_path / "repo"
    (repo / "knowledge" / "corpus").mkdir(parents=True)
    if contenido is not None:
        (repo / "knowledge" / "corpus" / "tramos_no_citables.yaml").write_text(
            contenido, encoding="utf-8"
        )
    return repo


def test_un_tramo_de_otro_video_no_tapa_nada(m: ModuleType, tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    segs = _segs(m, [(0, 1000, "a"), (1000, 2000, "b"), (2000, 3000, "c")])
    assert m.tramos_del_video("v9", repo) == ()
    assert m.tapados_por_tramos(segs, m.tramos_del_video("v9", repo)) == frozenset()
    # El negativo: el mismo tramo, en su video, si tapa.
    assert m.tapados_por_tramos(segs, m.tramos_del_video("v8", repo)) == {1, 2}


@pytest.mark.parametrize(
    ("contenido", "video", "error"),
    [
        (None, "v9", "no existe knowledge/corpus/tramos_no_citables.yaml"),
        ("tramos: [\n", "v9", "no se pueden usar"),
        ("otra: 1\n", "v9", "no se pueden usar"),
        (_TRAMOS_YAML.replace('t1: "0:00:03"', 't1: "0:00:01"'), "v8", "no se pueden usar"),
        (_TRAMOS_YAML, None, "falta --video"),
        (_TRAMOS_YAML, "v99", "no es un video de sesion"),
        (_TRAMOS_YAML, "v1", "no es un video de sesion"),
    ],
    ids=["sin_fichero", "corrupto", "otra_clave", "t1_no_posterior", "sin_video", "v99", "v1"],
)
def test_tramos_del_video_falla_cerrado(
    m: ModuleType, tmp_path: Path, contenido: str | None, video: str | None, error: str
) -> None:
    repo = _repo(tmp_path, contenido)
    with pytest.raises(m.SesionError, match=error):
        m.tramos_del_video(video, repo)


def test_un_video_de_sesion_sin_tramos_da_una_tupla_vacia(m: ModuleType, tmp_path: Path) -> None:
    assert m.tramos_del_video("v10", _repo(tmp_path)) == ()


def test_el_repo_real_da_los_tramos_de_sus_sesiones(m: ModuleType) -> None:
    """Solo comprueba que el guion carga el fichero de tramos del repositorio con la libreria y que
    hay tramos de v9 y de v10: no lee ninguna cruda ni ninguna filtrada."""
    from botsito.corpus.cuarentena import cargar_tramos_no_citables

    for video in ("v9", "v10"):
        assert m.tramos_del_video(video, RAIZ) == cargar_tramos_no_citables(RAIZ)[video]
        assert m.tramos_del_video(video, RAIZ)


# ---------------------------------------------------------------- de punta a punta, con `main`


@pytest.fixture
def sesion(m: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Un repo de juguete con su fichero de tramos (v8: 1-3 s) y una carpeta de audio FUERA de el,
    con un audio vacio y una cruda SINTETICA; `main` lee los tramos del repo de juguete."""
    repo = _repo(tmp_path)
    monkeypatch.setattr(m, "RAIZ", repo)
    monkeypatch.setattr(m, "codigos_validos", lambda sesion: VALIDOS)
    monkeypatch.setattr(m, "meses_libres_del_repo", lambda: frozenset(range(1, 13)))
    carpeta = tmp_path / "audio"
    carpeta.mkdir()
    audio = carpeta / "s.m4a"
    audio.write_bytes(b"")
    segmentos = [(0, 1000, "hola"), (1000, 2000, "SECRETO uno"), (2000, 3000, "SECRETO dos"),
                 (3000, 4000, "adios")]  # fmt: skip
    m.salidas_de(audio)["cruda"].write_text(
        "".join(
            json.dumps({"n": i, "t0_ms": a, "t1_ms": b, "texto": t}, ensure_ascii=False) + "\n"
            for i, (a, b, t) in enumerate(segmentos)
        ),
        encoding="utf-8",
    )
    return audio


def _ficheros(carpeta: Path) -> set[str]:
    return {p.name for p in carpeta.iterdir()}


def test_main_aplica_los_tramos_del_video(m: ModuleType, sesion: Path) -> None:
    antes = _ficheros(sesion.parent)
    codigo = m.main(["--audio", str(sesion), "--solo-filtrar", "--sesion", "02", "--video", "v8"])
    assert codigo == 0
    salidas = m.salidas_de(sesion)
    texto = salidas["filtrada"].read_text(encoding="utf-8")
    assert "SECRETO" not in texto and "[NO CITABLE 00:01–00:03]" in texto
    assert "[00:00] hola" in texto and "[00:03] adios" in texto
    registro = salidas["registro"].read_text(encoding="utf-8")
    assert "video: v8; tramos no citables del video: 1" in registro
    assert "solo por meses 0, solo por tramos 2, por ambos 0" in registro
    assert "SECRETO" not in registro
    assert _ficheros(sesion.parent) == antes | {salidas["filtrada"].name, salidas["registro"].name}


def test_main_con_el_video_equivocado_no_tapa_el_tramo_ajeno(m: ModuleType, sesion: Path) -> None:
    """El tramo es de v8: con --video v9 no se aplica (y el texto sale). Es el riesgo declarado de
    la identificacion por declaracion (FILTRADAS-CON-TRAMOS.md §0.3)."""
    assert (
        m.main(["--audio", str(sesion), "--solo-filtrar", "--sesion", "03", "--video", "v9"]) == 0
    )
    assert "SECRETO uno" in m.salidas_de(sesion)["filtrada"].read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("preparar", "argumentos", "error"),
    [
        ("sin_fichero", ["--video", "v8"], "no existe"),
        ("corrupto", ["--video", "v8"], "no se pueden usar"),
        ("no_valida", ["--video", "v8"], "no se pueden usar"),
        ("nada", [], "falta --video"),
        ("nada", ["--video", "v99"], "no es un video de sesion"),
    ],
    ids=["sin_fichero", "corrupto", "no_valida", "sin_video", "v99"],
)
def test_main_falla_cerrado_y_no_escribe_nada(
    m: ModuleType,
    sesion: Path,
    capsys: pytest.CaptureFixture[str],
    preparar: str,
    argumentos: list[str],
    error: str,
) -> None:
    fichero = m.RAIZ / "knowledge" / "corpus" / "tramos_no_citables.yaml"
    if preparar == "sin_fichero":
        fichero.unlink()
    elif preparar == "corrupto":
        fichero.write_text("tramos: [\n", encoding="utf-8")
    elif preparar == "no_valida":
        fichero.write_text(_TRAMOS_YAML.replace('t1: "0:00:03"', 't1: "0:00:00"'), encoding="utf-8")
    antes = _ficheros(sesion.parent)
    codigo = m.main(["--audio", str(sesion), "--solo-filtrar", "--sesion", "02", *argumentos])
    assert codigo != 0
    assert error in capsys.readouterr().err
    assert _ficheros(sesion.parent) == antes  # ni filtrada ni registro
    assert not m.salidas_de(sesion)["filtrada"].exists()


def test_main_sin_tramos_no_transcribe_ni_escribe_la_cruda(
    m: ModuleType, sesion: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """En el modo con ASR, los tramos se cargan ANTES de transcribir: sin ellos no se escribe ni la
    cruda."""
    llamadas: list[Path] = []

    def transcribir(audio: Path, *_: Any) -> tuple[list[Any], dict[str, Any], float]:
        llamadas.append(audio)
        return [], {}, 0.0

    monkeypatch.setattr(m, "transcribir", transcribir)
    (m.RAIZ / "knowledge" / "corpus" / "tramos_no_citables.yaml").unlink()
    m.salidas_de(sesion)["cruda"].unlink()
    antes = _ficheros(sesion.parent)
    assert m.main(["--audio", str(sesion), "--sesion", "02", "--video", "v8"]) != 0
    assert llamadas == []
    assert _ficheros(sesion.parent) == antes


def test_main_se_niega_con_varios_audios(
    m: ModuleType, sesion: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (sesion.parent / "otro.mp4").write_bytes(b"")
    antes = _ficheros(sesion.parent)
    codigo = m.main(["--audio", str(sesion.parent), "--solo-filtrar", "--video", "v8"])
    assert codigo != 0 and "uno por ejecucion" in capsys.readouterr().err
    assert _ficheros(sesion.parent) == antes


def test_procesar_sin_video_falla_cerrado(m: ModuleType, sesion: Path) -> None:
    """La unica funcion que escribe la filtrada no tiene un camino sin tramos: su `video` por
    defecto es None, y None falla."""
    with pytest.raises(m.SesionError, match="falta --video"):
        m.procesar(sesion, "cpu", True, "02")
    assert not m.salidas_de(sesion)["filtrada"].exists()
