"""F08: indice en memoria, consultas por texto e instante, salida determinista y CLI `kb`.

Repo temporal construido A MANO (sin ffmpeg ni GPU): dos videos, una cruda con corregida y dudas,
un manifiesto de fotogramas con ficheros vacios, items de evidencia con una contradiccion.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.comun.documentos import sha256_hex
from botsito.corpus.transcripcion import Palabra, Segmento, a_jsonl
from botsito.evidence.modelo import escribir_item
from botsito.retrieval.consultas import Opciones, buscar, en_instante
from botsito.retrieval.indice import RetrievalError, construir_indice, token_de_busqueda
from botsito.retrieval.salida import json_, tabla

SHA = "a" * 64
FUENTES = (
    'raiz: "corpus"\nvideos:\n'
    '  - video_id: v1\n    fichero: "clip.mp4"\n    drive_id: d1\n    bytes: 1\n'
    '    fecha_grabacion: "2026-01-01"\n    naturaleza: prueba\n'
    '  - video_id: v2\n    fichero: "clip2.mp4"\n    drive_id: d2\n    bytes: 1\n'
    '    fecha_grabacion: "2026-01-02"\n    naturaleza: prueba\n'
)
AJUSTES = (
    '[entorno]\nnombre = "backtest"\n\n'
    '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n'
)


def _seg(n: int, t0: int, texto: str, paso: int = 500, senales: tuple[str, ...] = ()) -> Segmento:
    palabras = []
    t = t0
    for w in texto.split():
        palabras.append(Palabra(t, t + paso, w, 0.9))
        t += paso
    return Segmento(n, t0, t, texto, tuple(palabras), senales=senales)


CRUDA = [
    _seg(0, 0, "hola pongo el break even en el 0.75 vale"),
    _seg(1, 5000, "mi orden límite se va bajando con el precio"),
    _seg(2, 10000, "el boss rompe la liquidez", senales=("no_habla",)),
    _seg(3, 15000, "y aquí no hay entrada vale"),
    _seg(4, 20000, "no hay entrada vale porque cae"),
]


def _manifiesto_tr(tid: str, sha_cruda: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "transcripcion_id": tid,
        "video_id": "v1",
        "fichero_video": "clip.mp4",
        "sha256_video": SHA,
        "sha256_wav": "b" * 64,
        "duracion_video_s": 30.0,
        "duracion_wav_s": 30.0,
        "muestras": 480000,
        "carpeta": "transcripciones/v1/falso",
        "motor": {"modelo": "falso"},
        "ffmpeg": "x",
        "corte": {},
        "silencios_detectados": 0,
        "fragmentos": [{"indice": 0, "inicio_m": 0, "fin_m": 480000}],
        "cortes_forzados_m": [],
        "segmentos": len(CRUDA),
        "recortados": 0,
        "descartados": 0,
        "ms_con_habla": 0,
        "senales": {"repeticion": 0, "baja_prob": 0, "compresion": 0, "no_habla": 1},
        "hueco_transcripcion_s": 0,
        "huecos": [],
        "sha256_cruda": sha_cruda,
        "glosario_sha256_inicial": "c" * 64,
        "generado_el": "2026-09-08T00:00:00Z",
    }


def _manifiesto_fr() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "fotogramas_id": "fr-v1-" + SHA[:8],
        "video_id": "v1",
        "fichero_video": "clip.mp4",
        "sha256_video": SHA,
        "duracion_video_s": 30.0,
        "resolucion": {"ancho": 320, "alto": 180},
        "ffmpeg": "9.0.1",
        "parametros": {"fps": 1, "formato": "png", "seleccion": "x", "bitexact": True},
        "carpeta": "fotogramas/v1/png-1fps",
        "n_fotogramas": 29,
        "n_regulares": 29,
        "ultimo_pts_ms": 29000,
        "hueco_fotogramas_ms": 2000,
        "huecos": [],
        "extra": [],
        "sha256_index": SHA,
        "generado_el": "2026-09-05T00:00:00Z",
        "segundos_ausentes_ms": [7000],
    }


def _item(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "video_id": "v1",
        "t0": "0:00:00",
        "t1": "0:00:05",
        "modalidad": "audio",
        "tipo": "RULE_STATEMENT",
        "cita_literal": "pongo el break even en el 0.75",
        "afirmacion": "el break even va en 0,75",
        "tema": "stop.nivel",
        "valor": "0.75",
        "confianza": "alta",
        "extractor": "llm",
        "revisado_por": "t · hoja · cruda leida",
        "provenance": "botsito",
    }
    d.update(cambios)
    return d


def construir_repo(tmp_path: Path, con_datos: bool = True) -> tuple[Path, str]:
    """Devuelve (repo, transcripcion_id)."""
    repo = tmp_path
    (repo / "knowledge" / "corpus" / "transcripciones").mkdir(parents=True)
    (repo / "knowledge" / "corpus" / "fotogramas").mkdir(parents=True)
    (repo / "knowledge" / "evidence").mkdir(parents=True)
    (repo / "knowledge" / "corpus" / "fuentes.yaml").write_text(FUENTES, encoding="utf-8")
    (repo / "config").mkdir()
    (repo / "config" / "settings.example.toml").write_text(AJUSTES, encoding="utf-8")
    cruda = a_jsonl(CRUDA)
    sha_cruda = sha256_hex(cruda.encode("utf-8"))
    tid = "tr-v1-falso-" + sha_cruda[:8]
    (repo / "knowledge" / "corpus" / "transcripciones" / f"{tid}.yaml").write_text(
        yaml.safe_dump(_manifiesto_tr(tid, sha_cruda), sort_keys=True), encoding="utf-8"
    )
    fr = _manifiesto_fr()
    (repo / "knowledge" / "corpus" / "fotogramas" / f"{fr['fotogramas_id']}.yaml").write_text(
        yaml.safe_dump(fr, sort_keys=True), encoding="utf-8"
    )
    if con_datos:
        carpeta = repo / "data" / "transcripciones" / "v1" / "falso"
        carpeta.mkdir(parents=True)
        (carpeta / "cruda.jsonl").write_text(cruda, encoding="utf-8")
        corregida = [
            Segmento(
                s.n, s.t0_ms, s.t1_ms, s.texto.replace("boss", "BOS"), s.palabras, senales=s.senales
            )
            for s in CRUDA
        ]
        (carpeta / "corregida.jsonl").write_text(a_jsonl(corregida), encoding="utf-8")
        (carpeta / "correcciones.jsonl").write_text(
            json.dumps({"dudas": [3], "glosario_sha256": "x", "glosario_version": "x"}) + "\n",
            encoding="utf-8",
        )
        fotos = repo / "data" / "fotogramas" / "v1" / "png-1fps"
        fotos.mkdir(parents=True)
        for s in (0, 5, 10, 15, 20):
            (fotos / f"{s * 1000:09d}.png").write_bytes(b"png")
    directorio = repo / "knowledge" / "evidence"
    escribir_item(directorio, _item(transcripcion=tid))
    escribir_item(
        directorio,
        _item(
            t0="0:00:05",
            t1="0:00:10",
            cita_literal="mi orden límite se va bajando con el precio",
            afirmacion="la orden limite se reubica",
            tema="entrada.orden_limite",
            valor=None,
            transcripcion=tid,
            notas="cadencia sin definir",
        ),
    )
    escribir_item(
        directorio,
        _item(
            t0="0:00:10",
            t1="0:00:15",
            cita_literal="el boss rompe la liquidez",
            afirmacion="con el stop en 0,80 protege",
            tema="stop.nivel",
            valor="0,80",
            confianza="media",
            transcripcion=tid,
        ),
    )
    escribir_item(
        directorio,
        _item(
            video_id="v2",
            t0="0:01:00",
            t1="0:01:05",
            modalidad="pantalla",
            cita_literal="ratio 4,08",
            afirmacion="en pantalla el ratio es 4,08",
            tema="herramientas.ratio",
            valor="4,08",
            fotogramas=["fr-v2-00000000/60000"],
            transcripcion=None,
        ),
    )
    return repo, tid


def _indice(tmp_path: Path, con_datos: bool = True) -> Any:
    repo, _tid = construir_repo(tmp_path, con_datos)
    return construir_indice(repo, repo / "data")


def test_token_de_busqueda_pliega_acentos_y_numeros() -> None:
    assert token_de_busqueda("orden límite 0,75 0.750 Ñu M15 1:3") == [
        "orden",
        "limite",
        "0.75",
        "0.75",
        "nu",
        "m15",
        "1:3",  # un solo token (F07): no casa con el 1.3 que escribe el ASR (fallo lexico)
    ]


def test_indice_determinista_y_con_fuentes(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    assert ind.avisos == ["v2 sin transcripcion activa: solo por evidencia"]
    assert len(ind.documentos) == 4 + len(CRUDA)
    assert ind.transcripciones == {"v1": ind.documentos[-1].fuente.rsplit("/", 1)[0]}
    assert len(ind.contradicciones) == 1 and ind.contradicciones[0]["tema"] == "stop.nivel"
    r1 = tabla(buscar(ind, "break even").resultados, contexto=True)
    r2 = tabla(buscar(construir_indice(ind.repo, ind.carpeta_datos), "break even").resultados, True)
    assert r1 == r2


def test_and_prefijo_y_frase(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    r = buscar(ind, "0,75")
    assert [x.tipo for x in r.resultados] == ["evidencia", "segmento"]
    assert buscar(ind, "orden limite").resultados[0].fuente.startswith("ev-v1-000005")
    assert buscar(ind, "break vale").resultados[0].tipo == "segmento"  # AND por segmento
    assert buscar(ind, "breakev", Opciones(prefijo=True)).resultados == []
    assert len(buscar(ind, "bre", Opciones(prefijo=True)).resultados) == 2
    assert buscar(ind, "0.80").resultados[0].extra["valor"] == "0,80"
    # frase con comodin, por campo en los items y cruzando segmentos en la cruda
    frase = buscar(ind, "no hay entrada [...] porque cae", Opciones(frase=True)).resultados
    # dos apariciones: "no hay entrada" del segmento 3 con "porque cae" del 4, y la del 4 entera
    assert [x.fuente.rsplit("/", 1)[1] for x in frase] == ["3-4", "4"]
    dos = buscar(ind, "no hay entrada vale", Opciones(frase=True)).resultados
    assert [x.fuente.rsplit("/", 1)[1] for x in dos] == ["3", "4"]
    cruzada = buscar(ind, "en el 0.75 el break even", Opciones(frase=True))
    assert cruzada.resultados == []  # no cruza cita -> afirmacion
    with pytest.raises(RetrievalError, match="corchetes"):
        buscar(ind, "a [b", Opciones(frase=True))
    with pytest.raises(RetrievalError, match="vacio"):
        buscar(ind, "[...] hola", Opciones(frase=True))
    with pytest.raises(RetrievalError, match="tokens"):
        buscar(ind, "...")


def test_filtros_orden_top_y_errores(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    todos = buscar(ind, "vale").resultados
    assert [x.fuente.rsplit("/", 1)[1] for x in todos] == ["0", "3", "4"]
    assert len(buscar(ind, "vale", Opciones(top=2)).resultados) == 2
    assert (
        buscar(ind, "vale", Opciones(desde_ms=14000, hasta_ms=16000, video="v1"))
        .resultados[0]
        .extra["n"]
        == 3
    )
    assert buscar(ind, "stop", Opciones(tema="stop")).resultados[0].tipo == "evidencia"
    assert all(x.tipo == "evidencia" for x in buscar(ind, "vale", Opciones(tema="stop")).resultados)
    assert buscar(ind, "ratio", Opciones(video="v2")).resultados[0].fotograma is None
    assert buscar(ind, "liquidez", Opciones(solo="evidencia")).resultados[0].tipo == "evidencia"
    assert buscar(ind, "liquidez", Opciones(solo="cruda")).resultados[0].extra["senales"] == [
        "no_habla"
    ]
    for opciones, msg in (
        (Opciones(video="v9"), "desconocido"),
        (Opciones(desde_ms=1), "exigen --video"),
        (Opciones(video="v1", desde_ms=5, hasta_ms=1), "posterior"),
        (Opciones(top=0), "top"),
        (Opciones(solo="x"), "solo"),
    ):
        with pytest.raises(RetrievalError, match=msg):
            buscar(ind, "vale", opciones)


def test_corregida_dudas_y_fotograma(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    r = buscar(ind, "bos").resultados  # solo en la corregida
    assert len(r) == 1 and r[0].extra["texto_corregido"] == "el BOS rompe la liquidez"
    assert r[0].fotograma == {
        "referencia": "fr-v1-" + SHA[:8] + "/10000",
        "ruta": "data/fotogramas/v1/png-1fps/000010000.png",
    }
    duda = buscar(ind, "aqui").resultados[0]
    assert duda.extra["duda_glosario"] is True and duda.extra["texto_corregido"] is None
    # fotograma de referencia: floor, saltando ausentes (7 s) y sin fichero -> ruta None
    assert ind.fotograma_en("v1", 7900) == {
        "referencia": "fr-v1-" + SHA[:8] + "/6000",
        "ruta": None,
    }
    assert ind.fotograma_en("v1", 29999)["referencia"].endswith("/29000")
    assert ind.fotograma_en("v1", 31000) is None and ind.fotograma_en("v2", 0) is None
    salida = tabla(buscar(ind, "bos").resultados, contexto=True)
    assert "<no_habla>" in salida and "[corregida] el BOS rompe la liquidez" in salida
    assert "<duda glosario>" in tabla(buscar(ind, "aqui").resultados)


def test_en_instante(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    r = en_instante(ind, "v1", 12000, 3000).resultados
    tipos = [x.tipo for x in r]
    esperado = ["evidencia", "evidencia", "segmento", "segmento", "fotograma", "contradiccion"]
    assert tipos == esperado  # por bloques; dentro de cada bloque por tiempo
    assert r[0].fuente.startswith("ev-v1-000005") and r[1].fuente.startswith("ev-v1-000010")
    assert [r[2].extra["n"], r[3].extra["n"]] == [1, 2] and r[4].fuente.endswith("/12000")
    assert r[5].extra["items"][0].startswith("ev-v1-") and "0.75" in r[5].texto
    sin_margen = [x.tipo for x in en_instante(ind, "v1", 12000, 0).resultados]
    assert sin_margen == ["evidencia", "segmento", "fotograma", "contradiccion"]
    amplio = en_instante(ind, "v1", 12000, 60000).resultados
    assert sum(1 for x in amplio if x.tipo == "segmento") == len(CRUDA)
    for args, msg in (
        (("v9", 0, 0), "desconocido"),
        (("v1", -1, 0), ">= 0"),
        (("v1", 0, 121000), "margen"),
    ):
        with pytest.raises(RetrievalError, match=msg):
            en_instante(ind, *args)


def test_sin_datos_solo_evidencia_con_avisos(tmp_path: Path) -> None:
    ind = _indice(tmp_path, con_datos=False)
    assert any("ausente" in a for a in ind.avisos) and any(
        "v2 sin transcripcion" in a for a in ind.avisos
    )
    r = buscar(ind, "break even")
    assert [x.tipo for x in r.resultados] == ["evidencia"]
    foto = r.resultados[0].fotograma
    assert foto is not None and foto["ruta"] is None
    assert buscar(ind, "vale", Opciones(solo="cruda")).resultados == []
    assert [x.tipo for x in en_instante(ind, "v1", 1000, 0).resultados] == [
        "evidencia",
        "fotograma",
        "contradiccion",
    ]


def test_salida_con_fuente_sin_rutas_absolutas_y_json(tmp_path: Path) -> None:
    ind = _indice(tmp_path)
    resultados = buscar(ind, "vale").resultados + en_instante(ind, "v1", 12000, 3000).resultados
    texto = tabla(resultados, contexto=True)
    fuente = re.compile(r"^(ev-|tr-[a-z0-9-]+/\d|fr-[a-z0-9-]+/\d|contradiccion )")
    for linea in texto.splitlines():
        if linea.startswith("#") or linea.startswith("    ") or linea.endswith(" resultados"):
            continue
        assert fuente.match(linea), linea
    assert not re.search(r"^[A-Za-z]:/|/home/|/Users/", texto, re.M)
    doc = json.loads(json_(resultados))
    assert doc[0]["fuente"].startswith("tr-") and list(doc[0]) == sorted(doc[0])
    assert json.loads(json_([])) == []


def test_cli_kb(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo, tid = construir_repo(tmp_path)
    base = ["--repo", str(repo), "kb"]
    assert cli.main([*base, "find", "orden limite", "--top", "1"]) == 0
    out = capsys.readouterr()
    assert out.out.startswith("# tiempos") and "ev-v1-000005" in out.out
    assert out.err == "AVISO: v2 sin transcripcion activa: solo por evidencia\n"
    assert cli.main([*base, "find", "nada de nada", "--json"]) == 0
    out = capsys.readouterr()
    assert out.out == "[]\n"
    assert (
        cli.main([*base, "at", "--video", "v1", "--t", "0:00:12", "--margen-s", "3", "--json"]) == 0
    )
    doc = json.loads(capsys.readouterr().out)
    assert [d["tipo"] for d in doc] == [
        "evidencia",
        "evidencia",
        "segmento",
        "segmento",
        "fotograma",
        "contradiccion",
    ]
    for argv, msg in (
        (["find", "vale", "--video", "v9"], "desconocido"),
        (["find", "vale", "--top", "0"], "top"),
        (["find", "vale", "--desde", "0:00:01"], "exigen"),
        (["find", "a [b", "--frase"], "corchetes"),
        (["at", "--video", "v1", "--t", "0:99:99"], "ERROR"),
        (["at", "--video", "v1", "--t", "0:00:01", "--margen-s", "121"], "margen"),
    ):
        assert cli.main([*base, *argv]) == 1
        assert msg in capsys.readouterr().err
    # sin data/: aviso en stderr, resultados de evidencia, codigo 0
    repo2, _ = construir_repo(tmp_path / "sin", con_datos=False)
    assert cli.main(["--repo", str(repo2), "kb", "find", "break even"]) == 0
    out = capsys.readouterr()
    assert "AVISO" in out.err and "ev-v1-000000" in out.out and "AVISO" not in out.out
