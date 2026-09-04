"""Linea de comandos minima. Cada funcionalidad anade su subcomando aqui."""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

from botsito import __version__

STATE_FILE = "PROJECT_STATE.md"


def _read_section(text: str, title: str) -> str:
    """Devuelve el cuerpo de la seccion `## title` sin lineas vacias, o cadena vacia."""
    out: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip() == title
            continue
        if inside and line.strip():
            out.append(line.strip())
    return "\n".join(out)


def _git(repo: Path, *args: str) -> str | None:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def _current_branch(repo: Path) -> str:
    # symbolic-ref funciona tambien en una rama sin commits; rev-parse no.
    return _git(repo, "symbolic-ref", "--short", "HEAD") or ""


def contar_tests(repo: Path) -> int:
    """Funciones `test_*` bajo tests/, contadas por AST (sin ejecutar nada)."""
    total = 0
    for py in (repo / "tests").rglob("test_*.py"):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        total += sum(
            1
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef)
            and node.name.startswith("test_")
        )
    return total


def _ultimo_tag_estable(repo: Path) -> tuple[str, str] | None:
    tags = _git(repo, "tag", "-l", "stable/*", "--sort=-creatordate")
    if not tags:
        return None
    tag = tags.splitlines()[0].strip()
    commit = _git(repo, "rev-parse", "--short", f"{tag}^{{commit}}")
    return (tag, commit) if commit else None


def state_check(repo: Path) -> int:
    """Comprueba que PROJECT_STATE.md dice la verdad sobre el repositorio.

    1. `Current Branch` coincide con la rama real (se omite con HEAD separado).
    2. `Tests Currently Passing` empieza por el recuento real de funciones de test.
    3. `Last Stable Commit` empieza por el commit del ultimo tag `stable/*` (si hay tags).
    4. Toda funcionalidad en `Completed Features` tiene su informe en docs/validation/.
    """
    state_path = repo / STATE_FILE
    if not state_path.exists():
        print(f"ERROR: falta {STATE_FILE}")
        return 2
    text = state_path.read_text(encoding="utf-8")
    errores: list[str] = []

    declared = _read_section(text, "Current Branch")
    actual = _current_branch(repo)
    if not actual:
        print("AVISO: sin rama activa (HEAD separado o sin git); se omite la comprobacion de rama")
    elif declared != actual:
        errores.append(f"PROJECT_STATE declara la rama '{declared}'; la rama actual es '{actual}'")

    tests_line = _read_section(text, "Tests Currently Passing").splitlines()[:1]
    m = re.match(r"\s*(\d+)", tests_line[0]) if tests_line else None
    reales = contar_tests(repo)
    if m is None:
        errores.append("'Tests Currently Passing' debe empezar por el numero de tests")
    elif int(m.group(1)) != reales:
        errores.append(
            f"'Tests Currently Passing' dice {m.group(1)}; hay {reales} funciones de test"
        )

    estable = _ultimo_tag_estable(repo)
    if estable is not None:
        tag, commit = estable
        declarado = _read_section(text, "Last Stable Commit").split("·")[0].strip()
        if not declarado or not (declarado.startswith(commit) or commit.startswith(declarado)):
            errores.append(
                f"'Last Stable Commit' dice '{declarado}'; el tag {tag} apunta a {commit}"
            )

    for line in _read_section(text, "Completed Features").splitlines():
        mm = re.match(r"-\s*(F\d{2})\b", line)
        if mm and not list((repo / "docs" / "validation").glob(f"{mm.group(1)}-*.md")):
            errores.append(f"{mm.group(1)} figura como completada sin informe en docs/validation/")

    if errores:
        for e in errores:
            print(f"ERROR: {e}")
        return 1
    feature = _read_section(text, "Current Feature")
    print(f"OK: rama '{actual or '(sin rama)'}' - funcionalidad actual: {feature or '-'}")
    return 0


def knowledge_validate(repo: Path) -> int:
    """Valida lo que ya existe en knowledge/: en F02, el registro de parametros."""
    if not (repo / "knowledge").is_dir():
        print("ERROR: falta knowledge/")
        return 2
    from botsito.config.registro import RegistroError, cargar_registro

    try:
        registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    except RegistroError as exc:
        print(f"ERROR: registro de parametros: {exc}")
        return 1
    pendientes = registro.sin_fuente_confirmada()
    print(
        f"OK: registro con {len(registro.parametros)} parametros"
        f" ({len(pendientes)} sin confirmar) (validadores de evidencia desde F06)"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="botsito")
    parser.add_argument("--version", action="version", version=f"botsito {__version__}")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="raiz del repositorio")
    sub = parser.add_subparsers(dest="cmd")
    state = sub.add_parser("state", help="memoria operativa del proyecto")
    state_sub = state.add_subparsers(dest="state_cmd", required=True)
    state_sub.add_parser("check", help="comprueba PROJECT_STATE.md contra el repositorio")
    know = sub.add_parser("knowledge", help="base de conocimiento")
    know_sub = know.add_subparsers(dest="knowledge_cmd", required=True)
    know_sub.add_parser("validate", help="valida knowledge/ (registro de parametros en F02)")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):  # consolas Windows en cp1252
        sys.stdout.reconfigure(encoding="utf-8")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "state" and args.state_cmd == "check":
        return state_check(args.repo)
    if args.cmd == "knowledge" and args.knowledge_cmd == "validate":
        return knowledge_validate(args.repo)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
