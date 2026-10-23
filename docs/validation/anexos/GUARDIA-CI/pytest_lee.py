"""Fase 0 b): la guardia lee o no el fichero que se le pasa a pytest. Un repo inventado en un
directorio temporal, con el MISMO fichero (un literal de la carpeta de marzo, montado a trozos)
dentro y fuera de `tests/`; solo se llama a `decidir`, no se ejecuta nada."""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("guardia_f0", RAIZ / ".claude" / "hooks" / "guardia.py")
g = importlib.util.module_from_spec(spec)
sys.modules["guardia_f0"] = g
spec.loader.exec_module(g)

CARPETA = "corp" + "us/Estrategia del trader/Material adicional de su operativa/Back" + "test marzo 2026"
CUERPO = f'RUTA = "{CARPETA}/v.mp4"\n\ndef test_x():\n    assert RUTA\n'

with tempfile.TemporaryDirectory() as tmp:
    r = Path(tmp) / "repo"
    (r / "tests" / "unit").mkdir(parents=True)
    (r / "otra").mkdir()
    (r / "Makefile").write_text("x\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=r, check=True)
    subprocess.run(["git", "add", "-A"], cwd=r, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "i"], cwd=r, check=True)
    subprocess.run(["git", "checkout", "-q", "-b", "trabajo/p"], cwd=r, check=True)
    (r / "tests" / "unit" / "test_t.py").write_text(CUERPO, encoding="utf-8")
    (r / "otra" / "test_t.py").write_text(CUERPO, encoding="utf-8")
    politica = g.Politica(r)
    for comando in (
        "uv run pytest -q tests/unit/test_t.py",
        "uv run python -m pytest -q tests/unit/test_t.py",
        "uv run pytest -q otra/test_t.py",
        "uv run python tests/unit/test_t.py",
    ):
        ev = {"tool_name": "Bash", "tool_input": {"command": comando}, "cwd": str(r)}
        m = g.decidir(ev, politica)
        print(f"{comando}\t{'pasa' if m is None else 'NIEGA: ' + m.splitlines()[0][:120]}")
