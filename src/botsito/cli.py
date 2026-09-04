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
    pendientes = registro.no_confirmados()
    print(
        f"OK: registro con {len(registro.parametros)} parametros ({len(pendientes)} sin confirmar)"
    )
    from botsito.corpus.inventario import (
        InventarioError,
        cargar_fuentes,
        cargar_manifiesto,
        validar_manifiesto,
    )

    try:
        fuentes = cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml")
        ruta_manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
        if ruta_manifiesto.exists():
            problemas = validar_manifiesto(cargar_manifiesto(ruta_manifiesto), fuentes)
            for p in problemas:
                print(f"ERROR: manifiesto: {p}")
            if problemas:
                return 1
            print(f"OK: manifiesto del corpus coherente con {len(fuentes.videos)} videos esperados")
        else:
            print("AVISO: knowledge/corpus/manifest.yaml no existe (botsito corpus inventory)")
    except InventarioError as exc:
        print(f"ERROR: fuentes del corpus: {exc}")
        return 1
    from botsito.evidence import contradicciones
    from botsito.evidence.historial import modificaciones_en_historial
    from botsito.evidence.modelo import EvidenciaError, cargar_evidencia, validar_contra_manifiesto

    directorio = repo / "knowledge" / "evidence"
    try:
        items = cargar_evidencia(directorio)
    except EvidenciaError as exc:
        print(f"ERROR: evidencia: {exc}")
        return 1
    fallos: list[str] = []
    if ruta_manifiesto.exists():
        fallos += validar_contra_manifiesto(items, cargar_manifiesto(ruta_manifiesto))
    fallos += contradicciones.validar_fichero(directorio, items)
    historial = modificaciones_en_historial(repo)
    if historial:
        fallos += [f"evidencia modificada en el historial: {h}" for h in historial]
    for fallo in fallos:
        print(f"ERROR: {fallo}")
    if fallos:
        return 1
    abiertas = len(contradicciones.detectar(items))
    print(
        f"OK: {len(items)} items de evidencia, {abiertas} contradicciones abiertas, "
        "historial intacto"
    )
    return 0


def corpus_inventory(repo: Path, sin_hash: bool) -> int:
    """Genera knowledge/corpus/manifest.yaml desde fuentes.yaml y el disco."""
    from botsito.corpus.inventario import (
        InventarioError,
        cargar_fuentes,
        escribir_manifiesto,
        inventariar,
        validar_manifiesto,
    )

    try:
        fuentes = cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml")
        manifiesto = inventariar(repo, fuentes, hashear=not sin_hash)
    except InventarioError as exc:
        print(f"ERROR: {exc}")
        return 1
    problemas = validar_manifiesto(manifiesto, fuentes)
    escribir_manifiesto(manifiesto, repo / "knowledge" / "corpus" / "manifest.yaml")
    for p in problemas:
        print(f"AVISO: {p}")
    r = manifiesto["resumen"]
    print(
        "OK: manifiesto escrito · "
        + " · ".join(f"{k}: {v['ficheros']} ficheros, {v['bytes']:,} bytes" for k, v in r.items())
    )
    for i in manifiesto["indices_heredados"]:
        print(f"  {i['ruta']}: {i['fotogramas']} fotogramas, {len(i['huecos'])} huecos > umbral")
    return 1 if problemas else 0


def corpus_check(repo: Path, hashes: bool) -> int:
    """Compara el manifiesto con el disco (tamanos; con --hashes tambien SHA-256)."""
    from botsito.corpus.inventario import (
        InventarioError,
        cargar_fuentes,
        cargar_manifiesto,
        comprobar_contra_disco,
        validar_manifiesto,
    )

    try:
        fuentes = cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml")
        manifiesto = cargar_manifiesto(repo / "knowledge" / "corpus" / "manifest.yaml")
    except InventarioError as exc:
        print(f"ERROR: {exc}")
        return 1
    problemas = validar_manifiesto(manifiesto, fuentes) + comprobar_contra_disco(
        manifiesto, repo, hashes=hashes
    )
    for p in problemas:
        print(f"ERROR: {p}")
    if not problemas:
        print(f"OK: el corpus coincide con el manifiesto ({'hashes' if hashes else 'tamanos'})")
    return 1 if problemas else 0


def evidence_new(repo: Path, args: argparse.Namespace) -> int:
    """Crea un item de evidencia con su id calculado (nunca sobreescribe)."""
    from botsito.evidence.modelo import EvidenciaError, escribir_item

    campos = {
        "video_id": args.video,
        "t0": args.t0,
        "t1": args.t1,
        "modalidad": args.modalidad,
        "tipo": args.tipo,
        "cita_literal": args.cita,
        "afirmacion": args.afirmacion,
        "tema": args.tema,
        "valor": args.valor,
        "confianza": args.confianza,
        "extractor": args.extractor,
        "revisado_por": args.revisado_por,
        "provenance": args.provenance,
        "fotogramas": args.fotograma or [],
        "supersede": args.supersede,
        "notas": args.notas,
    }
    try:
        ruta = escribir_item(repo / "knowledge" / "evidence", campos)
    except EvidenciaError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"OK: {ruta.relative_to(repo).as_posix()}")
    print("Regenera las contradicciones: botsito evidence contradictions")
    return 0


def evidence_contradictions(repo: Path) -> int:
    from botsito.evidence import contradicciones
    from botsito.evidence.modelo import EvidenciaError, cargar_evidencia

    directorio = repo / "knowledge" / "evidence"
    try:
        items = cargar_evidencia(directorio)
    except EvidenciaError as exc:
        print(f"ERROR: {exc}")
        return 1
    ruta = contradicciones.escribir(directorio, items)
    n = len(contradicciones.detectar(items))
    print(f"OK: {ruta.relative_to(repo).as_posix()} con {n} contradicciones abiertas")
    return 0


def config_validate(repo: Path) -> int:
    """Los ficheros de ajustes reales no contienen claves del registro ni secciones ajenas."""
    from botsito.config.ajustes import AjustesError, cargar_ajustes
    from botsito.config.registro import RegistroError, cargar_registro

    try:
        nombres = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml").nombres()
    except RegistroError as exc:
        print(f"ERROR: registro de parametros: {exc}")
        return 1
    ficheros = [repo / "config" / "settings.example.toml"]
    ficheros += sorted((repo / "config").glob("settings*.local.toml"))
    errores = 0
    for fichero in ficheros:
        try:
            ajustes = cargar_ajustes(fichero, nombres)
        except AjustesError as exc:
            print(f"ERROR: {fichero.name}: {exc}")
            errores += 1
            continue
        print(f"OK: {fichero.name} (entorno {ajustes.entorno})")
    return 1 if errores else 0


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
    corpus = sub.add_parser("corpus", help="inventario del corpus")
    corpus_sub = corpus.add_subparsers(dest="corpus_cmd", required=True)
    inv = corpus_sub.add_parser("inventory", help="genera knowledge/corpus/manifest.yaml")
    inv.add_argument("--sin-hash", action="store_true", help="no calcular SHA-256 (rapido)")
    chk = corpus_sub.add_parser("check", help="compara el manifiesto con el disco")
    chk.add_argument("--hashes", action="store_true", help="verificar tambien SHA-256")
    ev = sub.add_parser("evidence", help="evidencia del corpus")
    ev_sub = ev.add_subparsers(dest="evidence_cmd", required=True)
    nuevo = ev_sub.add_parser("new", help="crea un item de evidencia con id calculado")
    nuevo.add_argument("--video", required=True)
    nuevo.add_argument("--t0", required=True, help="h:mm:ss[.d]")
    nuevo.add_argument("--t1", required=True, help="h:mm:ss[.d]")
    nuevo.add_argument("--modalidad", required=True, choices=["audio", "pantalla", "ambas"])
    nuevo.add_argument(
        "--tipo",
        required=True,
        choices=[
            "RULE_STATEMENT",
            "PARAMETER",
            "EXAMPLE_TRADE",
            "NO_TRADE",
            "MANAGEMENT",
            "UNKNOWN",
        ],
    )
    nuevo.add_argument("--cita", required=True, help="cita literal")
    nuevo.add_argument("--afirmacion", required=True)
    nuevo.add_argument("--tema", required=True, help="p. ej. stop.nivel")
    nuevo.add_argument("--valor")
    nuevo.add_argument("--confianza", required=True, choices=["alta", "media", "baja"])
    nuevo.add_argument("--extractor", required=True, choices=["humano", "llm"])
    nuevo.add_argument("--revisado-por", required=True, dest="revisado_por")
    nuevo.add_argument("--provenance", default="botsito", choices=["botsito", "bot-v2"])
    nuevo.add_argument("--fotograma", action="append", help="ruta del manifiesto; repetible")
    nuevo.add_argument("--supersede")
    nuevo.add_argument("--notas")
    ev_sub.add_parser("contradictions", help="regenera knowledge/evidence/_contradicciones.yaml")
    conf = sub.add_parser("config", help="ajustes de entorno")
    conf_sub = conf.add_subparsers(dest="config_cmd", required=True)
    conf_sub.add_parser("validate", help="comprueba config/settings*.toml contra el registro")
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
    if args.cmd == "config" and args.config_cmd == "validate":
        return config_validate(args.repo)
    if args.cmd == "evidence" and args.evidence_cmd == "new":
        return evidence_new(args.repo, args)
    if args.cmd == "evidence" and args.evidence_cmd == "contradictions":
        return evidence_contradictions(args.repo)
    if args.cmd == "corpus" and args.corpus_cmd == "inventory":
        return corpus_inventory(args.repo, args.sin_hash)
    if args.cmd == "corpus" and args.corpus_cmd == "check":
        return corpus_check(args.repo, args.hashes)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
