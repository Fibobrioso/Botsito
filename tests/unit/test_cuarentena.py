"""La cuarentena por defecto (rama `trabajo/cuarentena-por-defecto`, 2026-10-01).

Todo sobre datos SINTETICOS: el repo de `test_retrieval` con una cruda propia en la que un segmento
nombra un mes SIN dia (la regla c), otro cae en un tramo no citable escrito aqui (la b), y la
cuarentena de sesion (la a) se prueba poniendo v1 en la lista con `monkeypatch`. Ningun texto lleva
una fecha real ni un dia reservado. Lo unico real es `fuentes.yaml`, para cruzar la lista.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
import yaml

from botsito import cli
from botsito.corpus import cuarentena
from botsito.corpus.cuarentena import (
    CuarentenaError,
    Filtro,
    motivos_cuarentena,
    problemas_de_la_lista,
    resumen,
)
from botsito.corpus.inventario import cargar_fuentes
from botsito.corpus.pipeline_transcripcion import cargar_cruda
from botsito.corpus.transcripcion import a_jsonl, texto_entre
from botsito.retrieval.consultas import buscar
from botsito.retrieval.indice import RetrievalError, construir_indice
from tests.unit.test_retrieval import _seg, construir_repo

RAIZ = Path(__file__).resolve().parents[2]
CARPETA_V1 = Path("data") / "transcripciones" / "v1" / "falso"

SEGMENTOS = [
    _seg(0, 0, "hola pongo el break even vale"),
    _seg(1, 5000, "texto normal sin nada"),
    _seg(2, 10000, "otra frase tranquila"),  # vecino de la 3: tambien (c)
    _seg(3, 15000, "lo vi en mayo con calma"),  # (c): un mes sin dia
    _seg(4, 20000, "despues sigue la explicacion"),  # vecino de la 3: tambien (c)
    _seg(5, 25000, "zona visible aqui"),
    _seg(6, 30000, "tramo ajeno palabra"),  # (b): el tramo 0:00:30-0:00:31
    _seg(7, 35000, "cierre visible final"),
]
TRAMOS = (
    "tramos:\n"
    '  - video_id: v1\n    t0: "0:00:30"\n    t1: "0:00:31"\n'
    "    motivo: tramo sintetico\n    acordado: en este test\n"
)
# Una palabra que solo esta en el segmento que oculta cada regla.
PALABRA = {"a": "visible", "b": "ajeno", "c": "calma"}
INSTANTE = {"a": "0:00:25", "b": "0:00:30", "c": "0:00:16"}
OPCION = "--" + "crudo"


def _repo(tmp_path: Path) -> Path:
    repo, _tid = construir_repo(tmp_path)
    carpeta = repo / CARPETA_V1
    (carpeta / "cruda.jsonl").write_text(a_jsonl(SEGMENTOS), encoding="utf-8")
    (carpeta / "corregida.jsonl").write_text(a_jsonl(SEGMENTOS), encoding="utf-8")
    (carpeta / "correcciones.jsonl").write_text('{"dudas": []}\n', encoding="utf-8")
    (repo / "knowledge" / "corpus" / "tramos_no_citables.yaml").write_text(TRAMOS, encoding="utf-8")
    return repo


@pytest.fixture
def sesion_v1(monkeypatch: pytest.MonkeyPatch) -> None:
    """La regla (a) sobre el repo sintetico: v1 pasa a estar en la lista de cuarentena."""
    monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))


def _cli(capsys: pytest.CaptureFixture[str], repo: Path, *args: str) -> str:
    assert cli.main(["--repo", str(repo), *args]) == 0
    salida = capsys.readouterr()
    return salida.out + salida.err


def _sin_fuga(salida: str) -> None:
    """El aviso de ocultos solo dice cuantos y por que: ni texto, ni un mes, ni una fecha."""
    linea = next(ln for ln in salida.splitlines() if ln.startswith(("OCULTOS", "# transcr")))
    assert motivos_cuarentena(linea) == [], linea
    for texto in ("mayo", "calma", "ajeno"):
        assert texto not in linea


# ------------------------------------------------------------------------------- la lista


def test_la_lista_cuadra_con_fuentes() -> None:
    """Cruzada con el `fuentes.yaml` real: una sesion sin listar, o un video listado con
    `drive_id`, rompe `make check` en vez de quedar visible (decision del consultor)."""
    fuentes = cargar_fuentes(RAIZ / "knowledge" / "corpus" / "fuentes.yaml")
    drive_ids = {v.video_id: (v.drive_id or None) for v in fuentes.videos}
    assert problemas_de_la_lista(drive_ids) == []


def test_la_comprobacion_de_la_lista_no_es_decorativa() -> None:
    reales = {"v1": "d1", "v6": None, "v7": None, "v8": None, "v9": None}
    assert problemas_de_la_lista(reales) == []
    assert any("v10: es una sesion" in p for p in problemas_de_la_lista({**reales, "v10": None}))
    assert any(
        "v7: esta en" in p and "drive_id" in p
        for p in problemas_de_la_lista({**reales, "v7": "abc"})
    )
    sin_v8 = {k: v for k, v in reales.items() if k != "v8"}
    assert any("v8: esta en" in p for p in problemas_de_la_lista(sin_v8))


# -------------------------------------------------------------------------------- el filtro


def test_el_filtro_aplica_las_tres_reglas_con_prioridad(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    filtro = Filtro("v1", ((30000, 31000, "x"),))
    visibles = filtro.aplicar(SEGMENTOS)
    assert [s.n for s in visibles] == [0, 1, 5, 7]
    assert {n: o.motivo for n, o in filtro.ocultos.items()} == {2: "c", 3: "c", 4: "c", 6: "b"}
    assert filtro.aplicar(visibles) == visibles  # dos veces el mismo filtro no oculta mas
    assert len(filtro.ocultos) == 4
    assert [o.n for o in filtro.ocultos_entre(16000, 16000)] == [3]
    monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    sesion = Filtro("v1", ((30000, 31000, "x"),))
    assert sesion.aplicar(SEGMENTOS) == []
    assert {o.motivo for o in sesion.ocultos.values()} == {"a"}  # la (a) manda sobre b y c


def test_el_aviso_dice_cuantos_y_por_que_sin_contenido() -> None:
    filtro = Filtro("v1", ((30000, 31000, "x"),))
    filtro.aplicar(SEGMENTOS)
    aviso = resumen(filtro.ocultos.values())
    assert aviso.startswith("OCULTOS: 4 segmentos: 1 por tramo no citable (b), 3 por material")
    assert motivos_cuarentena(aviso) == []  # el aviso mismo no dispara la regla (c)
    assert resumen([]) == ""


def test_las_funciones_filtran_por_defecto_y_sin_filtro_fallan(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    carpeta = repo / CARPETA_V1
    with pytest.raises(CuarentenaError, match="filtra por defecto"):
        cargar_cruda(carpeta)
    with pytest.raises(CuarentenaError, match="filtra por defecto"):
        texto_entre(SEGMENTOS, 0, 40000)
    filtro = cuarentena.filtro_de(repo, "v1")
    assert [s.n for s in cargar_cruda(carpeta, filtro)] == [0, 1, 5, 7]
    assert len(cargar_cruda(carpeta, crudo=True)) == len(SEGMENTOS)
    filtrado = construir_indice(repo, repo / "data")
    with pytest.raises(RetrievalError, match="filtrado"):
        buscar(filtrado, "calma", crudo=True)
    assert buscar(filtrado, "calma").resultados == []
    assert len(buscar(filtrado, "calma").ocultos) == 4
    entero = construir_indice(repo, repo / "data", crudo=True)
    assert len(buscar(entero, "calma", crudo=True).resultados) == 1
    with pytest.raises(RetrievalError, match="crudo"):
        buscar(entero, "calma")


# ---------------------------------------------------------- los comandos, regla por regla


@pytest.mark.parametrize("regla", ["a", "b", "c"])
def test_kb_find_oculta_por_defecto_y_crudo_lo_muestra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch, regla: str
) -> None:
    repo = _repo(tmp_path)
    if regla == "a":
        monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    salida = _cli(capsys, repo, "kb", "find", PALABRA[regla], "--video", "v1", "--solo", "cruda")
    assert PALABRA[regla] not in salida.replace("OCULTOS", "")
    assert f"({regla})" in salida
    _sin_fuga(salida)
    crudo = _cli(
        capsys, repo, "kb", "find", PALABRA[regla], "--video", "v1", "--solo", "cruda", OPCION
    )
    assert PALABRA[regla] in crudo and "OCULTOS" not in crudo


@pytest.mark.parametrize("regla", ["a", "b", "c"])
def test_kb_at_oculta_por_defecto_y_crudo_lo_muestra(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch, regla: str
) -> None:
    repo = _repo(tmp_path)
    if regla == "a":
        monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    base = ("kb", "at", "--video", "v1", "--t", INSTANTE[regla], "--margen-s", "0")
    salida = _cli(capsys, repo, *base)
    assert PALABRA[regla] not in salida and f"({regla})" in salida
    _sin_fuga(salida)
    crudo = _cli(capsys, repo, *base, OPCION)
    assert PALABRA[regla] in crudo and "OCULTOS" not in crudo


@pytest.mark.parametrize("regla", ["a", "b", "c"])
@pytest.mark.parametrize("capa", ["cruda", "corregida"])
def test_transcript_show_oculta_por_defecto_y_crudo_lo_muestra(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    regla: str,
    capa: str,
) -> None:
    repo = _repo(tmp_path)
    if regla == "a":
        monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    t = INSTANTE[regla]
    base = ("corpus", "transcript", "show", "--video", "v1", "--t0", t, "--t1", t, "--capa", capa)
    salida = _cli(capsys, repo, *base)
    assert PALABRA[regla] not in salida and f"({regla})" in salida
    _sin_fuga(salida)
    crudo = _cli(capsys, repo, *base, OPCION)
    assert PALABRA[regla] in crudo and "OCULTOS" not in crudo


@pytest.mark.parametrize("regla", ["a", "b", "c"])
def test_frames_show_oculta_el_segmento_por_defecto_y_crudo_lo_muestra(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, regla: str
) -> None:
    """`corpus frames show` imprime las rutas de los PNG y el segmento que cubre el instante; lo
    segundo es `_segmento_en`, que es lo que se prueba (el repo sintetico no trae el indice de
    fotogramas que la primera parte necesita)."""
    repo = _repo(tmp_path)
    if regla == "a":
        monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    t_ms = {"a": 25000, "b": 30500, "c": 16000}[regla]
    salida = cli._segmento_en(repo, "v1", t_ms)
    assert PALABRA[regla] not in salida and f"({regla})" in salida
    _sin_fuga(salida)
    assert PALABRA[regla] in cli._segmento_en(repo, "v1", t_ms, crudo=True)


@pytest.mark.parametrize("regla", ["a", "b", "c"])
def test_evidence_propose_copia_solo_lo_que_se_puede_ensenar(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch, regla: str
) -> None:
    """La propuesta copia los segmentos del tramo en un fichero del repositorio: siempre
    filtrados, sin opcion de crudo."""
    from tests.unit.test_cli import _knowledge_con_cruda

    repo, _tid, _cita = _knowledge_con_cruda(tmp_path)
    carpeta = next((repo / "data" / "transcripciones" / "v1").rglob("cruda.jsonl")).parent
    (carpeta / "cruda.jsonl").write_text(a_jsonl(SEGMENTOS), encoding="utf-8")
    (repo / "knowledge" / "corpus" / "tramos_no_citables.yaml").write_text(TRAMOS, encoding="utf-8")
    (repo / "knowledge" / "_proposals").mkdir()
    (repo / "knowledge" / "_proposals" / "PROMPT.md").write_text("# prompt\n", encoding="utf-8")
    if regla == "a":
        monkeypatch.setattr(cuarentena, "SESIONES_EN_CUARENTENA", frozenset({"v1"}))
    salida = _cli(
        capsys, repo, "evidence", "propose", "--video", "v1", "--t0", "0:00:00", "--t1", "0:00:40"
    )
    assert f"({regla})" in salida
    _sin_fuga(salida)
    (fichero,) = (repo / "knowledge" / "_proposals").glob("pr-*.yaml")
    textos = [
        s["texto"]
        for s in yaml.safe_load(fichero.read_text(encoding="utf-8"))["contexto"]["segmentos"]
    ]
    assert not any(PALABRA[regla] in t for t in textos)


# ------------------------------------------------------------ quien puede pedir el crudo

AUTORIZADOS = {
    "src/botsito/validation/contexto_evidencia.py",  # la verificacion de citas
    "scripts/transcribir_sesion.py",
}


def usos_de_crudo(codigo: str) -> list[tuple[int, str]]:
    """Cada `crudo=` de una llamada (y cada clave "crudo" de un dict) que NO sea `False`, ni el
    reenvio de un parametro (`crudo=crudo`) o de un atributo (`crudo=args.crudo`): `True` u otra
    cosa, con su linea."""
    salida: list[tuple[int, str]] = []
    for nodo in ast.walk(ast.parse(codigo)):
        if isinstance(nodo, ast.Call):
            for k in nodo.keywords:
                if k.arg != "crudo":
                    continue
                v = k.value
                if isinstance(v, ast.Constant) and v.value is False:
                    continue
                if isinstance(v, ast.Name) and v.id == "crudo":
                    continue
                if isinstance(v, ast.Attribute) and v.attr == "crudo":
                    continue
                es_true = isinstance(v, ast.Constant) and v.value is True
                salida.append((nodo.lineno, "True" if es_true else "otro"))
        elif isinstance(nodo, ast.Dict):
            for clave in nodo.keys:
                if isinstance(clave, ast.Constant) and clave.value == "crudo":
                    salida.append((nodo.lineno, "dict"))
    return salida


def test_crudo_true_solo_en_los_llamadores_autorizados() -> None:
    """Decision del consultor: la verificacion de citas, transcribir_sesion.py y los tests. Los
    tests no se recorren: son llamadores autorizados."""
    problemas = []
    for base in ("src", "scripts"):
        for py in sorted((RAIZ / base).rglob("*.py")):
            rel = py.relative_to(RAIZ).as_posix()
            for linea, que in usos_de_crudo(py.read_text(encoding="utf-8")):
                if que == "True" and rel in AUTORIZADOS:
                    continue
                problemas.append(f"{rel}:{linea}: crudo={que}")
    assert problemas == []


def test_el_recorrido_de_crudo_no_es_decorativo() -> None:
    assert usos_de_crudo("f(crudo=True)") == [(1, "True")]
    assert usos_de_crudo("f(x, crudo=algo)") == [(1, "otro")]
    assert usos_de_crudo("f(**{'crudo': True})") == [(1, "dict")]
    assert usos_de_crudo("f(crudo=False)\ng(crudo=crudo)\nh(crudo=args.crudo)") == []
