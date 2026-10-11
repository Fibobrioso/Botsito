"""El hook de arranque `.claude/hooks/estado_sesion.py` (E1, rama `trabajo/entorno-code`): dice el
estado de la rama, solo abre las rutas de su lista cerrada, cada una despues de preguntar a la
guardia, y nunca bloquea la sesion."""

from __future__ import annotations

import ast
import importlib.util
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
HOOK = RAIZ / ".claude" / "hooks" / "estado_sesion.py"


@pytest.fixture(scope="module")
def e() -> ModuleType:
    nombre = "estado_sesion"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, HOOK)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=a@b", "-c", "user.name=x", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def _escribir(repo: Path, rel: str, texto: str) -> None:
    ruta = repo / rel
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(texto, encoding="utf-8")


CONTRATO = (
    "rama: trabajo/x\n"
    "riesgo: medio  # un motivo\n"
    "artefacto: docs/validation/X.md\n"
    "tramo: R0\n"
    "rutas_permitidas: [docs/]\n"
)
PS = (
    "# Estado\n\n## Current Branch\n\nmain\n\n## Next Action\n\n"
    "S. Una cosa.\n\nB. Otra.\n\n### Pendientes heredados (sin verificar)\n\n1. un heredado\n\n"
    "## Known Ambiguities\n\nQ. fuera de la Next Action\n"
)


def _repo(tmp_path: Path, *, rama: str = "trabajo/x", contrato: str | None = CONTRATO) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir(parents=True)
    _git(repo, "init", "-q", "-b", "main")
    _escribir(repo, "PROJECT_STATE.md", PS)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "base")
    if rama != "main":
        _git(repo, "checkout", "-q", "-b", rama)
        if contrato is not None:
            _escribir(repo, "contrato.yaml", contrato)
        _escribir(repo, f"docs/encargos/{rama.replace('/', '-')}.md", "# Encargo\n\n> hazlo\n")
    return repo


def _informe(repo: Path, cuerpo: str, estado: str = "EN CURSO.") -> None:
    _escribir(repo, "docs/validation/X.md", f"# X\n\n{cuerpo}\n## Estado\n\n{estado}\n")


def test_rama_con_contrato(e: ModuleType, tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _informe(repo, "## 0. Fase 0\n\nalgo\n")
    salida = e.estado(repo)
    assert salida[0].startswith("Rama: trabajo/x · ultimo commit: ")
    assert "Contrato: artefacto docs/validation/X.md · riesgo medio · tramo R0" in salida
    assert "Encargo: docs/encargos/trabajo-x.md" in salida
    assert "Estado del informe: EN CURSO." in salida
    assert not [x for x in salida if "ESPERANDO" in x or "AVISO" in x]
    assert salida[-1] == "Para retomar: skill retomar-rama"
    assert len(salida) < 15


def test_main_da_las_letras_vivas_y_sin_rama_abierta(e: ModuleType, tmp_path: Path) -> None:
    salida = e.estado(_repo(tmp_path, rama="main"))
    assert salida[0].startswith("Rama: main · ")
    assert "Next Action: S B" in salida  # solo las de la seccion Next Action
    assert "sin rama abierta" in salida
    _git(tmp_path / "repo", "branch", "trabajo/y")
    assert "Ramas locales: trabajo/y" in e.estado(tmp_path / "repo")


def test_parada_sin_respuesta_espera(e: ModuleType, tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _informe(repo, "## 0. Fase 0\n\n## 1. Lo que necesito que decidas\n\n0. algo\n", "PARADA.")
    assert "ESPERANDO al consultor: la ultima PARADA no tiene respuesta" in e.estado(repo)
    # con la respuesta copiada a los dos sitios, ya no espera
    _informe(
        repo,
        "## 1. Lo que necesito que decidas\n\n## 2. Respuesta del consultor a la PARADA\n\n> si\n",
    )
    encargo = repo / "docs/encargos/trabajo-x.md"
    encargo.write_text(
        encargo.read_text(encoding="utf-8") + "\n## Respuesta del consultor a la PARADA\n",
        encoding="utf-8",
    )
    salida = e.estado(repo)
    assert not [x for x in salida if "ESPERANDO" in x or "AVISO" in x], salida


def test_respuesta_copiada_solo_al_encargo(e: ModuleType, tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _informe(repo, "## 1. Lo que necesito que decidas\n\n0. algo\n")
    encargo = repo / "docs/encargos/trabajo-x.md"
    encargo.write_text(
        encargo.read_text(encoding="utf-8") + "\n## Respuesta del consultor a la PARADA\n\n> si\n",
        encoding="utf-8",
    )
    salida = e.estado(repo)
    assert not [x for x in salida if "ESPERANDO" in x]
    assert (
        "AVISO: respuestas del consultor: 0 en el informe, 1 en el encargo (se copian a los dos)"
        in salida
    )


def test_sin_informe(e: ModuleType, tmp_path: Path) -> None:
    salida = e.estado(_repo(tmp_path))
    assert "Informe: sin informe (docs/validation/X.md no existe)" in salida
    sin_artefacto = e.estado(_repo(tmp_path / "otro", contrato="rama: trabajo/x\nriesgo: bajo\n"))
    assert "Informe: sin informe (no hay `artefacto` en el contrato)" in sin_artefacto


def test_un_fichero_que_la_guardia_bloquea_no_se_lee(
    e: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    protegido = "knowledge/cases/holdout/1/caso.yaml"
    repo = _repo(tmp_path, contrato=CONTRATO.replace("docs/validation/X.md", protegido))
    _escribir(repo, protegido, "SECRETO-123\n")
    leidos: list[Path] = []
    original = Path.read_text

    def read_text(self: Path, *args: object, **kwargs: object) -> str:
        leidos.append(self.resolve())
        return original(self, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.setattr(Path, "read_text", read_text)
    salida = e.estado(repo)
    assert f"Informe: {protegido}: no se lee, la guardia lo bloquea" in salida
    assert "SECRETO" not in "\n".join(salida)
    assert (repo / protegido).resolve() not in leidos


def test_solo_abre_su_lista_cerrada(e: ModuleType, tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    _informe(repo, "## 0. Fase 0\n")
    permitidas = e.lista_cerrada("trabajo/x", "docs/validation/X.md")
    assert permitidas == (
        "contrato.yaml",
        "PROJECT_STATE.md",
        "docs/encargos/trabajo-x.md",
        "docs/validation/X.md",
    )
    with pytest.raises(e.NoSeLeeError, match="fuera de la lista cerrada"):
        e.leer(repo, "data/velas.csv", permitidas)
    with pytest.raises(e.NoSeLeeError, match="fuera de la lista cerrada"):
        e.leer(repo, "docs/validation/OTRO.md", permitidas)


def test_ningun_otro_sitio_del_hook_abre_un_fichero() -> None:
    """Negar por defecto, en el codigo: abrir un fichero (open, read_text, read_bytes, io/os.open)
    solo se puede dentro de `leer`, que exige la lista cerrada y la guardia. Si alguien anade una
    lectura en otro sitio, falla aqui."""
    arbol = ast.parse(HOOK.read_text(encoding="utf-8"))
    abre = {"open", "read_text", "read_bytes", "readlines", "listdir", "scandir", "glob", "rglob"}
    fuera: list[str] = []

    def recorrer(nodo: ast.AST, funcion: str) -> None:
        for hijo in ast.iter_child_nodes(nodo):
            nombre = hijo.name if isinstance(hijo, ast.FunctionDef) else funcion
            if isinstance(hijo, ast.Call):
                f = hijo.func
                n = f.attr if isinstance(f, ast.Attribute) else getattr(f, "id", "")
                if n in abre and nombre != "leer":
                    fuera.append(f"{nombre}:{hijo.lineno} {n}")
            recorrer(hijo, nombre)

    recorrer(arbol, "<modulo>")
    assert fuera == []


def _hook(env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps({"hook_event_name": "SessionStart", "source": "startup"}),
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONUTF8": "1", **env},
        timeout=30,
        check=False,
    )


def test_nunca_bloquea_y_es_rapido(tmp_path: Path) -> None:
    inicio = time.perf_counter()
    r = _hook({"CLAUDE_PROJECT_DIR": str(RAIZ)})
    segundos = time.perf_counter() - inicio
    assert r.returncode == 0, r.stderr
    assert r.stdout.strip().splitlines()[-1] == "Para retomar: skill retomar-rama"
    assert segundos < 2, segundos
    # fuera de un repositorio, o con la raiz rota: una linea, y sale con 0
    for raiz in (tmp_path, tmp_path / "no-existe"):
        r = _hook({"CLAUDE_PROJECT_DIR": str(raiz)})
        assert r.returncode == 0, r.stderr
        assert r.stdout.strip(), r.stderr


def test_si_la_guardia_no_se_puede_importar_no_se_lee_nada(
    e: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repo = _repo(tmp_path)
    _informe(repo, "## 0. Fase 0\n")
    monkeypatch.setitem(sys.modules, "guardia", None)  # `import guardia` da ImportError
    salida = e.estado(repo)
    no_decide = "la guardia no pudo decidir (ModuleNotFoundError)"
    assert f"Encargo: docs/encargos/trabajo-x.md: {no_decide}" in salida
    assert f"Contrato: contrato.yaml: {no_decide}" in salida
    assert not [x for x in salida if x.startswith(("Contrato: artefacto", "Estado del informe"))]
    assert salida[-1] == "Para retomar: skill retomar-rama"


def test_un_error_dentro_es_una_linea_y_sale_con_0(
    e: ModuleType, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def rota(_raiz: Path) -> list[str]:
        raise RuntimeError("rota a proposito")

    monkeypatch.setattr(e, "estado", rota)
    assert e.main() == 0
    assert capsys.readouterr().out.strip() == (
        "estado_sesion: no se pudo leer el estado (RuntimeError: rota a proposito)"
    )


def test_settings_lo_lanza_al_arrancar_retomar_limpiar_y_compactar() -> None:
    ajustes = json.loads((RAIZ / ".claude" / "settings.json").read_text(encoding="utf-8"))
    (entrada,) = ajustes["hooks"]["SessionStart"]
    assert entrada["matcher"] == "startup|resume|clear|compact"
    (orden,) = entrada["hooks"]
    assert orden["type"] == "command"
    assert "estado_sesion.py" in orden["command"] and "PYTHONUTF8=1" in orden["command"]
    assert "PreToolUse" in ajustes["hooks"]  # la guardia sigue
