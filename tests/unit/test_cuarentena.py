"""La cuarentena por defecto (rama `trabajo/cuarentena-por-defecto`, 2026-10-01).

Todo sobre datos SINTETICOS: el repo de `test_retrieval` con una cruda propia en la que un segmento
nombra un mes SIN dia (la regla c), otro cae en un tramo no citable escrito aqui (la b), y la
cuarentena de sesion (la a) se prueba poniendo v1 en la lista con `monkeypatch`. Ningun texto lleva
una fecha real ni un dia reservado. Lo unico real es `fuentes.yaml`, para cruzar la lista.
"""

from __future__ import annotations

import ast
import json
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
    # 4 segmentos; el item que pisa uno de (c) SE VE: la evidencia tiene su criterio (sexta orden)
    ocultos = buscar(filtrado, "calma").ocultos
    assert sorted(o.clase for o in ocultos) == ["segmento"] * 4
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


def test_evidence_propose_oculta_el_vecino_aunque_el_que_dispara_quede_fuera(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Revisor de esta rama, B1: el intervalo 0:00:20-0:00:21 solo trae el segmento 4, vecino
    del 3 (el que nombra el mes), que queda FUERA. Filtrando solo el recorte, el 4 se copiaba."""
    from tests.unit.test_cli import _knowledge_con_cruda

    repo, _tid, _cita = _knowledge_con_cruda(tmp_path)
    carpeta = next((repo / "data" / "transcripciones" / "v1").rglob("cruda.jsonl")).parent
    (carpeta / "cruda.jsonl").write_text(a_jsonl(SEGMENTOS), encoding="utf-8")
    (repo / "knowledge" / "_proposals").mkdir()
    (repo / "knowledge" / "_proposals" / "PROMPT.md").write_text("# prompt\n", encoding="utf-8")
    salida = _cli(
        capsys, repo, "evidence", "propose", "--video", "v1", "--t0", "0:00:20", "--t1", "0:00:21"
    )
    assert "OCULTOS: 1 segmentos: 1 por material reservado o sin sortear (c)" in salida
    (fichero,) = (repo / "knowledge" / "_proposals").glob("pr-*.yaml")
    doc = yaml.safe_load(fichero.read_text(encoding="utf-8"))
    assert doc["contexto"]["segmentos"] == []


# ------------------------------------------------------------ quien puede pedir el crudo

# (fichero, funcion) -> motivo. Negar por defecto (cuarta orden del consultor, 2026-10-01): solo
# funciones concretas, nunca un fichero entero. La verificacion de citas y los tests (segunda
# orden); `corpus glossary apply` (tercera); `corpus transcript check` (cuarta, punto 2); y la
# evidencia de kb que copia un segmento oculto (quinta).
AUTORIZADOS: dict[tuple[str, str], str] = {
    ("src/botsito/validation/contexto_evidencia.py", "crudas"): (
        "la verificacion de citas compara cada cita con la cruda entera y no devuelve su texto"
    ),
    ("src/botsito/cli.py", "corpus_glossary_apply"): (
        "corpus glossary apply recalcula la corregida desde la cruda entera (ADR-0007)"
    ),
    ("src/botsito/corpus/manifiestos_transcripcion.py", "comprobar"): (
        "corpus transcript check recalcula sobre la cruda entera los recuentos del manifiesto"
        " y compara la corregida con cruda + glosario (integridad)"
    ),
    ("src/botsito/retrieval/indice.py", "_evidencia_que_copia"): (
        "kb oculta el item que COPIA el texto de un tramo no citable aunque su cita no lo pise"
        " (quinta y sexta orden): compara con la cruda entera y devuelve solo ids y motivos"
    ),
    # scripts/transcribir_sesion.py NO usa `crudo=True`, y desde la cuarta orden no esta
    # autorizado entero: negar por defecto, una funcion concreta cuando lo necesite. Estas dos
    # son la tuberia de la cuarentena de una sesion nueva, FUERA del repositorio, y las autorizo
    # el consultor en la sexta orden: «La ingesta de una sesión nueva las necesita».
    ("scripts/transcribir_sesion.py", "salidas_de"): (
        "arma las rutas de la cruda de una sesion (`*.cruda-NO-LEER.*`), fuera del repositorio,"
        " que el script escribe y luego filtra"
    ),
    ("scripts/transcribir_sesion.py", "transcribir"): (
        "el ASR de una sesion guarda sus parciales de fragmento antes de fusionarlos"
    ),
}
# El modulo que IMPLEMENTA las funciones que filtran: es el unico que lee el fichero sin pasar
# por ellas.
IMPLEMENTACION = "src/botsito/corpus/pipeline_transcripcion.py"


def _autorizado(rel: str, funcion: str | None) -> bool:
    """Negar por defecto (cuarta orden): solo una funcion concreta, nunca un fichero entero."""
    return (rel, funcion) in AUTORIZADOS


def _con_funcion(arbol: ast.AST) -> list[tuple[ast.AST, str | None, ast.AST | None]]:
    """Cada nodo con la funcion que lo contiene (la mas interior) y su padre."""
    salida: list[tuple[ast.AST, str | None, ast.AST | None]] = []

    def visitar(nodo: ast.AST, funcion: str | None, padre: ast.AST | None) -> None:
        salida.append((nodo, funcion, padre))
        dentro = nodo.name if isinstance(nodo, ast.FunctionDef | ast.AsyncFunctionDef) else funcion
        for hijo in ast.iter_child_nodes(nodo):
            visitar(hijo, dentro, nodo)

    visitar(arbol, None, None)
    return salida


def usos_de_crudo(codigo: str) -> list[tuple[int, str, str | None]]:
    """Cada `crudo=` de una llamada (y cada clave "crudo" de un dict) que NO sea `False`, ni el
    reenvio de un parametro (`crudo=crudo`) o de un atributo (`crudo=args.crudo`): `True` u otra
    cosa, con su linea y la funcion que lo contiene."""
    salida: list[tuple[int, str, str | None]] = []
    for nodo, funcion, _padre in _con_funcion(ast.parse(codigo)):
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
                salida.append((nodo.lineno, "True" if es_true else "otro", funcion))
        elif isinstance(nodo, ast.Dict):
            for clave in nodo.keys:
                if isinstance(clave, ast.Constant) and clave.value == "crudo":
                    salida.append((nodo.lineno, "dict", funcion))
    return salida


# Los nombres de lo que guarda TEXTO de una transcripcion: las constantes del pipeline y cualquier
# literal que nombre la cruda (`cruda.jsonl`, `cruda.txt`, `*.cruda-NO-LEER.*`), la corregida o
# los parciales de un fragmento (revisor de esta rama, B2: la primera version solo veia
# `cruda.jsonl` y `corregida.jsonl` detras de una `/`).
CONSTANTES_DE_TEXTO = {"FICHERO_CRUDA", "FICHERO_CORREGIDA", "CARPETA_PARCIALES"}
TROZOS_DE_TEXTO = ("cruda", "corregida", "parciales")
LLAMADAS_CON_RUTA = {"open", "Path", "joinpath", "glob", "rglob", "iglob", "read_text"}


def _nombra_fichero_de_texto(nodo: ast.AST) -> bool:
    if isinstance(nodo, ast.Name):
        return nodo.id in CONSTANTES_DE_TEXTO
    if isinstance(nodo, ast.Attribute):
        return nodo.attr in CONSTANTES_DE_TEXTO
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        return any(t in nodo.value.lower() for t in TROZOS_DE_TEXTO)
    if isinstance(nodo, ast.JoinedStr):
        return any(_nombra_fichero_de_texto(v) for v in nodo.values)
    return False


def _nombre_de_llamada(nodo: ast.Call) -> str | None:
    if isinstance(nodo.func, ast.Name):
        return nodo.func.id
    if isinstance(nodo.func, ast.Attribute):
        return nodo.func.attr
    return None


def lecturas_en_bruto(codigo: str) -> list[tuple[int, str, str | None]]:
    """Lo que leeria el texto de una transcripcion SIN pasar por `cargar_cruda`/`cargar_corregida`:
    construir su ruta (`carpeta / FICHERO_CRUDA`, `... / "cruda.jsonl"`) para algo que no sea
    preguntar si existe (`.is_file()`, `.exists()`); pasar su nombre a `open`, `Path`,
    `joinpath`, `glob`, `rglob` o `iglob`; o parsear con el `desde_jsonl` de las transcripciones."""
    arbol = ast.parse(codigo)
    nodos = _con_funcion(arbol)
    padres = {id(n): p for n, _f, p in nodos}
    importa_desde_jsonl = any(
        isinstance(n, ast.ImportFrom)
        and n.module == "botsito.corpus.transcripcion"
        and any(a.name == "desde_jsonl" for a in n.names)
        for n, _f, _p in nodos
    )
    salida: list[tuple[int, str, str | None]] = []
    for nodo, funcion, padre in nodos:
        if (
            isinstance(nodo, ast.BinOp)
            and isinstance(nodo.op, ast.Div)
            and _nombra_fichero_de_texto(nodo.right)
        ):
            existe = (
                isinstance(padre, ast.Attribute)
                and padre.attr in {"is_file", "exists"}
                and isinstance(padres.get(id(padre)), ast.Call)
            )
            if not existe:
                salida.append((nodo.lineno, "ruta", funcion))
        if (
            isinstance(nodo, ast.Call)
            and _nombre_de_llamada(nodo) in LLAMADAS_CON_RUTA
            and any(_nombra_fichero_de_texto(a) for a in nodo.args)
        ):
            salida.append((nodo.lineno, "llamada", funcion))
        if (
            importa_desde_jsonl
            and isinstance(nodo, ast.Call)
            and isinstance(nodo.func, ast.Name)
            and nodo.func.id == "desde_jsonl"
        ):
            salida.append((nodo.lineno, "desde_jsonl", funcion))
    return salida


def _codigo_del_proyecto() -> list[tuple[str, str]]:
    return [
        (py.relative_to(RAIZ).as_posix(), py.read_text(encoding="utf-8"))
        for base in ("src", "scripts")
        for py in sorted((RAIZ / base).rglob("*.py"))
    ]


def test_crudo_true_solo_en_los_llamadores_autorizados() -> None:
    """Los tests no se recorren: son llamadores autorizados."""
    problemas = [
        f"{rel}:{linea}: crudo={que} en {funcion}"
        for rel, codigo in _codigo_del_proyecto()
        for linea, que, funcion in usos_de_crudo(codigo)
        if not (que == "True" and _autorizado(rel, funcion))
    ]
    assert problemas == []


def test_nadie_lee_la_cruda_sin_pasar_por_las_funciones_que_filtran() -> None:
    """Orden del consultor del 2026-10-01: ninguna funcion lee la cruda (o la corregida) sin
    pasar por `crudo=True`; solo el modulo que las implementa y los llamadores autorizados."""
    problemas = [
        f"{rel}:{linea}: {que} en {funcion}"
        for rel, codigo in _codigo_del_proyecto()
        if rel != IMPLEMENTACION
        for linea, que, funcion in lecturas_en_bruto(codigo)
        if not _autorizado(rel, funcion)
    ]
    assert problemas == []


def test_los_recorridos_no_son_decorativos() -> None:
    assert usos_de_crudo("f(crudo=True)") == [(1, "True", None)]
    assert usos_de_crudo("def g():\n    f(x, crudo=algo)") == [(2, "otro", "g")]
    assert usos_de_crudo("f(**{'crudo': True})") == [(1, "dict", None)]
    assert usos_de_crudo("f(crudo=False)\ng(crudo=crudo)\nh(crudo=args.crudo)") == []
    assert lecturas_en_bruto("def g(c):\n    return (c / FICHERO_CRUDA).read_bytes()") == [
        (2, "ruta", "g")
    ]
    assert lecturas_en_bruto("x = c / 'corregida.jsonl'") == [(1, "ruta", None)]
    assert lecturas_en_bruto("x = c.joinpath('cruda.jsonl')") == [(1, "llamada", None)]
    assert lecturas_en_bruto("x = open(f'{c}/cruda.txt')") == [(1, "llamada", None)]
    assert lecturas_en_bruto("x = c.glob('parciales/*.json')") == [(1, "llamada", None)]
    assert lecturas_en_bruto("x = c / 'cruda.txt'") == [(1, "ruta", None)]
    assert lecturas_en_bruto("ok = (c / FICHERO_CRUDA).is_file()") == []
    assert lecturas_en_bruto(
        "from botsito.corpus.transcripcion import desde_jsonl\ndesde_jsonl(t)"
    ) == [(2, "desde_jsonl", None)]
    assert (
        lecturas_en_bruto("from botsito.corpus.fotogramas import desde_jsonl\ndesde_jsonl(t)") == []
    )
    assert _autorizado("src/botsito/cli.py", "corpus_glossary_apply")
    assert not _autorizado("src/botsito/cli.py", "kb_find")
    # Negar por defecto (cuarta orden): ninguna autorizacion por fichero entero.
    assert all(funcion is not None for _rel, funcion in AUTORIZADOS)
    assert not _autorizado("scripts/transcribir_sesion.py", "procesar")


# ------------------------------------- la evidencia: su propio criterio (sexta orden del consultor)
# La cruda no esta revisada, y por eso la ocultan la sesion en cuarentena (a) y la regla del mes
# (c). Un item de evidencia es un extracto REVISADO que ademas se lee con Read: solo lo ocultan un
# tramo no citable (b) -su cita cae en el o su texto lo copia- o un dia de `casos_ocultos`.

ITEM_SINTETICO = "ev-v1-000035-"


def _item_en(repo: Path, notas: str, t0: str = "0:00:35", t1: str = "0:00:40") -> None:
    """Un item sintetico de v1 con `notas` y la palabra `espejado` en la afirmacion."""
    from botsito.evidence.modelo import escribir_item
    from tests.unit.test_retrieval import _item

    (manifiesto,) = (repo / "knowledge" / "corpus" / "transcripciones").glob("tr-*.yaml")
    cita = {"0:00:35": "cierre visible final", "0:00:30": "tramo ajeno palabra"}[t0]
    escribir_item(
        repo / "knowledge" / "evidence",
        _item(
            transcripcion=manifiesto.stem,
            t0=t0,
            t1=t1,
            cita_literal=cita,
            afirmacion="un cierre espejado",
            notas=notas,
            tema="salida.cierre",
            valor=None,
        ),
    )


def _args(orden: tuple[str, ...], instante: str) -> tuple[str, ...]:
    return (*orden, "--t", instante, "--margen-s", "0") if orden[1] == "at" else orden


@pytest.mark.parametrize("orden", [("kb", "find", "boss"), ("kb", "at", "--video", "v1")])
def test_kb_ensena_la_evidencia_de_una_sesion_en_cuarentena_sin_dia_reservado(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    sesion_v1: None,
    orden: tuple[str, ...],
) -> None:
    """Sexta orden: «un ítem de v7 sin día reservado se muestra». v1 hace de v7 (la fixture la
    pone en la cuarentena): sus segmentos se ocultan por (a), pero el item del boss, que cita uno
    y tambien pisa un vecino de (c), SALE, y el aviso no cuenta evidencia."""
    repo = _repo(tmp_path)
    # 0:00:15: el final de la cita del boss y el principio del segmento 3 (en `at`, un instante
    # coge el segmento que lo contiene).
    salida = _cli(capsys, repo, *_args(orden, "0:00:15"))
    assert "ev-v1-000010-" in salida
    assert "por sesion en cuarentena (a)" in salida and "items de evidencia" not in salida
    _sin_fuga(salida)


@pytest.mark.parametrize("orden", [("kb", "find", "espejado"), ("kb", "at", "--video", "v1")])
@pytest.mark.parametrize("como", ["copia", "cita"])
def test_kb_oculta_la_evidencia_de_un_tramo_no_citable(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], orden: tuple[str, ...], como: str
) -> None:
    """Sexta orden: «uno que copia un tramo no citable de v6 se oculta» (v1 con un tramo
    sintetico hace de v6). Dos vias: sus notas copian el segmento 6, que cae en el tramo, con la
    cita en un segmento visible (quinta orden); o su cita cae en el tramo. Por defecto no sale y el
    aviso lo cuenta por (b); con la opcion de crudo, sale."""
    repo = _repo(tmp_path)
    if como == "copia":
        _item_en(repo, "contexto: tramo ajeno palabra")
        instante, item = "0:00:36", ITEM_SINTETICO
    else:
        _item_en(repo, "sin copia", t0="0:00:30", t1="0:00:31")
        instante, item = "0:00:30", "ev-v1-000030-"
    salida = _cli(capsys, repo, *_args(orden, instante))
    assert item not in salida
    assert "1 items de evidencia: 1 por tramo no citable (b)" in salida
    _sin_fuga(salida)
    crudo = _cli(capsys, repo, *_args(orden, instante), OPCION)
    assert item in crudo and "OCULTOS" not in crudo


@pytest.mark.parametrize("orden", [("kb", "find", "espejado"), ("kb", "at", "--video", "v1")])
def test_kb_oculta_la_evidencia_con_un_dia_reservado(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    monkeypatch: pytest.MonkeyPatch,
    orden: tuple[str, ...],
) -> None:
    """Sexta orden: «uno con un día reservado se oculta». El dia es sintetico e imposible (31 de
    febrero), puesto como reservado sustituyendo `cli._dias_ocultos`; la misma nota con el dia sin
    reservar no oculta nada."""
    repo = _repo(tmp_path)
    _item_en(repo, "lo cuenta el 31/02 en la revision")
    libre = _cli(capsys, repo, *_args(orden, "0:00:36"))
    assert ITEM_SINTETICO in libre
    monkeypatch.setattr(cli, "_dias_ocultos", lambda _repo: frozenset({(2, 31)}))
    salida = _cli(capsys, repo, *_args(orden, "0:00:36"))
    assert ITEM_SINTETICO not in salida
    assert "1 items de evidencia: 1 por material reservado o sin sortear (c)" in salida
    _sin_fuga(salida)
    assert "31" not in next(ln for ln in salida.splitlines() if ln.startswith("OCULTOS"))
    crudo = _cli(capsys, repo, *_args(orden, "0:00:36"), OPCION)
    assert ITEM_SINTETICO in crudo and "OCULTOS" not in crudo


def test_copia_pide_la_mitad_de_las_ventanas() -> None:
    oculto = cuarentena.ventanas_de_copia("uno dos tres cuatro cinco seis siete ocho nueve diez")
    assert len(oculto) == 3
    assert cuarentena.copia(cuarentena.plano("UNO dos  tres cuatro cinco seis siete ocho"), oculto)
    assert not cuarentena.copia(cuarentena.plano("uno dos tres cuatro cinco seis"), oculto)
    assert cuarentena.ventanas_de_copia("corto") == []
    filtro = Filtro("v1")
    filtro.aplicar(SEGMENTOS)
    items = [("ev-copia", 35000, 40000, "x: lo vi en mayo con calma"), ("ev-no", 0, 1, "zona")]
    copian = cuarentena.items_que_copian(filtro, SEGMENTOS, items)
    assert {i: (o.motivo, o.clase) for i, o in copian.items()} == {"ev-copia": ("c", "evidencia")}
    # Con el alcance de la sexta orden (solo b), copiar un segmento de (c) no oculta.
    assert cuarentena.items_que_copian(filtro, SEGMENTOS, items, motivos={"b"}) == {}


def test_evidencia_a_ocultar_solo_por_tramo_o_dia() -> None:
    """Sexta orden, la funcion pura: (c) y (a) no ocultan evidencia; un tramo, o un dia de los
    vigilados en el texto del item, en un segmento visible que cita o en uno oculto, si."""
    filtro = Filtro("v1", ((30000, 31000, "x"),), dias=frozenset({(2, 31)}))
    visibles = filtro.aplicar([*SEGMENTOS[:7], _seg(7, 35000, "el 31/02 cierre")])
    items = [
        ("ev-pisa-c", 10000, 15000, "nada"),  # pisa segmentos de (c): se ve
        ("ev-tramo", 30000, 30500, "nada"),  # su cita cae en el tramo
        ("ev-dia-propio", 0, 4000, "dice el 31/02"),  # el dia en su propio texto
        ("ev-dia-visible", 35000, 36000, "nada"),  # el dia en el segmento visible que cita
        ("ev-libre", 0, 4000, "dice el 30/02"),  # una fecha que no se vigila
    ]
    ocultos = cuarentena.evidencia_a_ocultar(filtro, items, visibles)
    assert {i: (o.motivo, o.fecha_vigilada) for i, o in ocultos.items()} == {
        "ev-tramo": ("b", False),
        "ev-dia-propio": ("c", True),
        "ev-dia-visible": ("c", True),
    }
    sin_dias = Filtro("v1", ((30000, 31000, "x"),))
    sin_dias.aplicar(SEGMENTOS)
    assert set(cuarentena.evidencia_a_ocultar(sin_dias, items, [])) == {"ev-tramo"}


def test_items_ocultos_toma_el_motivo_de_mas_prioridad() -> None:
    filtro = Filtro("v1", ((30000, 31000, "x"),))
    filtro.aplicar(SEGMENTOS)
    ocultos = cuarentena.items_ocultos(
        filtro, [("ev-uno", 10000, 15000), ("ev-dos", 30000, 30500), ("ev-tres", 0, 4000)]
    )
    assert {i: o.motivo for i, o in ocultos.items()} == {"ev-uno": "c", "ev-dos": "b"}
    assert all(o.clase == "evidencia" for o in ocultos.values())


def test_fechas_en_dice_dia_y_mes_y_nada_mas() -> None:
    """Datos sinteticos: fechas imposibles o de meses sin dias reservados."""
    assert cuarentena.fechas_en("el treinta y uno de febrero") == {(2, 31)}
    assert cuarentena.fechas_en("el 31/02") == {(2, 31)}
    assert cuarentena.fechas_en("agosto 40 no existe") == set()
    assert cuarentena.fechas_en("lo vi en mayo con calma") == set()
    filtro = Filtro("v1", dias=frozenset({(2, 31)}))
    filtro.aplicar([_seg(0, 0, "nada aqui"), _seg(1, 5000, "el 31/02 entre"), _seg(2, 9000, "y")])
    assert {n: o.fecha_vigilada for n, o in filtro.ocultos.items()} == {0: False, 1: True, 2: False}


# --------------------------------------------- corpus transcript check: solo el resultado


def test_transcript_check_no_imprime_contenido(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Cuarta orden, punto 2: autorizado con la cruda entera, con la condicion de imprimir solo
    el resultado (OK o fallo) y el fichero. Ni con la cruda sana ni con una rota sale texto."""
    from dataclasses import replace

    from botsito.comun.documentos import sha256_hex
    from botsito.corpus.glosario import glosario_desde_texto
    from botsito.corpus.manifiestos_transcripcion import cargar_todos, comprobar

    repo = _repo(tmp_path)
    glosario = "vocabulario: [otro]\nsustituciones: []\n"
    (repo / "knowledge" / "corpus" / "glosario_asr.yaml").write_text(glosario, encoding="utf-8")
    # Por la CLI, con la cruda sana (la del manifiesto no casa: da un fallo de integridad).
    cli.main(["--repo", str(repo), "corpus", "transcript", "check"])
    sana = capsys.readouterr()
    assert not any(s.texto in sana.out + sana.err for s in SEGMENTOS)
    # Con una cruda ROTA cuyo sha si casa: el fallo de forma no trae la palabra que lo provoca.
    palabra = {"t0_ms": 0, "t1_ms": 5000, "texto": "PALABRASECRETA", "probabilidad": 0.9}
    fila = {"n": 0, "t0_ms": 0, "t1_ms": 1000, "texto": "texto ajeno", "palabras": [palabra]}
    texto = json.dumps(fila) + "\n"  # la palabra acaba DESPUES del segmento: forma invalida
    (repo / CARPETA_V1 / "cruda.jsonl").write_bytes(texto.encode("utf-8"))
    (t,) = cargar_todos(repo)
    t = replace(t, sha256_cruda=sha256_hex(texto.encode("utf-8")))
    errores, avisos = comprobar([t], repo / "data", glosario_desde_texto(glosario))
    salida = "\n".join(errores + avisos)
    assert "cruda.jsonl no se puede leer" in salida
    assert "PALABRASECRETA" not in salida and "texto ajeno" not in salida
