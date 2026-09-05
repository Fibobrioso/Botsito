"""Linea de comandos minima. Cada funcionalidad anade su subcomando aqui."""

from __future__ import annotations

import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from botsito import __version__
from botsito.domain.valores import HoraLocal

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
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=repo,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
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
    5. En `main`, lo commiteado despues del ultimo tag estable solo puede tocar PROJECT_STATE.md
       (el ritual de merge deja un commit docs(state) tras el tag; nada mas entra sin tag).
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

        if actual == "main":
            tocados = _git(repo, "diff", "--name-only", f"{tag}..HEAD") or ""
            ajenos = sorted(f for f in tocados.splitlines() if f.strip() and f != STATE_FILE)
            if ajenos:
                errores.append(
                    f"main tiene cambios sin tag estable desde {tag}: {', '.join(ajenos)}"
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
    """Imprime `validation.knowledge.validar` (el orquestador vive alli, ADR-0006)."""
    from botsito.validation.knowledge import validar

    codigo, lineas = validar(repo)
    for linea in lineas:
        print(linea)
    return codigo


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
    problemas = validar_manifiesto(manifiesto, fuentes)
    if not problemas:
        problemas = comprobar_contra_disco(manifiesto, repo, hashes=hashes)
    for p in problemas:
        print(f"ERROR: {p}")
    if not problemas:
        print(f"OK: el corpus coincide con el manifiesto ({'hashes' if hashes else 'tamanos'})")
    return 1 if problemas else 0


def _video_del_corpus(repo: Path, video_id: str) -> tuple[Path, str, str, float]:
    """(raiz del corpus, fichero, sha256, duracion) del video segun fuentes y manifiesto."""
    from botsito.corpus.inventario import cargar_fuentes, cargar_manifiesto

    fuentes = cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml")
    manifiesto = cargar_manifiesto(repo / "knowledge" / "corpus" / "manifest.yaml")
    videos = {v["video_id"]: v for v in manifiesto.get("videos") or []}
    if video_id not in videos:
        from botsito.corpus.inventario import InventarioError

        raise InventarioError(f"video {video_id!r} no esta en el manifiesto del corpus")
    v = videos[video_id]
    return repo / fuentes.raiz, str(v["fichero"]), str(v["sha256"]), float(v["duracion_s"])


def _glosario(repo: Path) -> Any:
    from botsito.corpus.glosario import cargar_glosario

    return cargar_glosario(repo / "knowledge" / "corpus" / "glosario_asr.yaml")


def corpus_transcribe(repo: Path, args: argparse.Namespace) -> int:
    """Transcribe un video del corpus por fragmentos con desfase absoluto (F04, ADR-0007)."""
    from botsito.corpus.audio import AudioError, ParametrosCorte
    from botsito.corpus.glosario import GlosarioError
    from botsito.corpus.inventario import InventarioError
    from botsito.corpus.pipeline_transcripcion import transcribir_video
    from botsito.corpus.transcripcion import MotorAsr, MotorFalso, TranscripcionError

    try:
        raiz, fichero, sha, duracion = _video_del_corpus(repo, args.video)
        glosario = _glosario(repo)
    except (InventarioError, GlosarioError) as exc:
        print(f"ERROR: {exc}")
        return 1
    motor: MotorAsr
    if args.motor == "falso":
        motor = MotorFalso()
    else:
        from botsito.corpus.motor_whisper import ConfiguracionWhisper, MotorWhisper

        motor = MotorWhisper(
            ConfiguracionWhisper(
                args.modelo, args.dispositivo, args.compute_type, glosario.prompt_inicial
            )
        )
    try:
        parametros = ParametrosCorte(objetivo_s=args.objetivo_s, min_s=args.min_s, max_s=args.max_s)
        if args.reemplaza_a:
            _comprobar_reemplaza_a(repo, args.video, args.reemplaza_a)
    except (AudioError, TranscripcionError) as exc:
        print(f"ERROR: {exc}")
        return 1

    def progreso(fragmento: object, n: int) -> None:
        print(f"  fragmento {getattr(fragmento, 'indice', '?')}: {n} segmentos", flush=True)

    try:
        r = transcribir_video(
            repo,
            _carpeta_datos(repo),
            raiz,
            args.video,
            fichero,
            sha,
            duracion,
            motor,
            glosario,
            parametros,
            progreso,
            reemplaza_a=args.reemplaza_a,
        )
    except (AudioError, TranscripcionError, ImportError, OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")  # RuntimeError/ValueError: faster-whisper, ctranslate2 y CUDA
        return 1
    print(f"OK: {r.transcripcion_id} ({len(r.segmentos)} segmentos)")
    print(f"  cruda: {r.cruda}")
    print(
        f"  manifiesto: {r.manifiesto.relative_to(repo).as_posix()} (INMUTABLE; commit sin editar)"
    )
    return 0


def _comprobar_reemplaza_a(repo: Path, video_id: str, tid: str) -> None:
    """Antes de gastar GPU: la transcripcion reemplazada existe y es del mismo video."""
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        cargar_todos,
    )
    from botsito.corpus.transcripcion import TranscripcionError

    try:
        previas = {t.id: t for t in cargar_todos(repo)}
    except ManifiestoTranscripcionError as exc:
        raise TranscripcionError(str(exc)) from exc
    if tid not in previas:
        raise TranscripcionError(f"--reemplaza-a {tid}: no existe ese manifiesto")
    if previas[tid].video_id != video_id:
        raise TranscripcionError(
            f"--reemplaza-a {tid}: es de {previas[tid].video_id}, no de {video_id}"
        )


def corpus_glossary_apply(repo: Path, args: argparse.Namespace) -> int:
    """Regenera corregida.jsonl y correcciones.jsonl de una o todas las transcripciones."""
    from botsito.corpus.glosario import GlosarioError
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        cargar_todos,
        carpeta_de,
    )
    from botsito.corpus.pipeline_transcripcion import cargar_cruda, corregir
    from botsito.corpus.transcripcion import TranscripcionError

    try:
        glosario = _glosario(repo)
        items = cargar_todos(repo)
    except (GlosarioError, ManifiestoTranscripcionError) as exc:
        print(f"ERROR: {exc}")
        return 1
    datos = _carpeta_datos(repo)
    n = 0
    for t in items:
        if args.video and t.video_id != args.video:
            continue
        carpeta = carpeta_de(datos, t)
        if not (carpeta / "cruda.jsonl").is_file():
            print(f"AVISO: {t.id}: cruda no esta en esta maquina")
            continue
        try:
            cambios = corregir(carpeta, cargar_cruda(carpeta), glosario, t.id)
        except TranscripcionError as exc:
            print(f"ERROR: {t.id}: {exc}")
            return 1
        print(f"OK: {t.id}: {cambios} sustituciones (glosario {glosario.version})")
        n += 1
    print(f"{n} transcripciones corregidas")
    return 0


def corpus_transcript_check(repo: Path) -> int:
    from botsito.corpus.glosario import GlosarioError
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        cargar_todos,
        comprobar,
    )

    try:
        items = cargar_todos(repo)
        glosario = _glosario(repo)
    except (GlosarioError, ManifiestoTranscripcionError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errores, avisos = comprobar(items, _carpeta_datos(repo), glosario)
    for a in avisos:
        print(f"AVISO: {a}")
    for e in errores:
        print(f"ERROR: {e}")
    if not errores:
        print(f"OK: {len(items)} transcripciones coherentes con el disco y el glosario")
    return 1 if errores else 0


def corpus_transcript_show(repo: Path, args: argparse.Namespace) -> int:
    """Cita literal con marcas: lo que F07 copia en `cita_literal`."""
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        activa_de,
        cargar_todos,
        carpeta_de,
    )
    from botsito.corpus.pipeline_transcripcion import cargar_corregida, cargar_cruda
    from botsito.corpus.transcripcion import (
        TranscripcionError,
        a_texto_legible,
        parse_ms,
        texto_entre,
    )

    try:
        t = activa_de(cargar_todos(repo), args.video, args.transcripcion)
        carpeta = carpeta_de(_carpeta_datos(repo), t)
        segmentos = cargar_cruda(carpeta) if args.capa == "cruda" else cargar_corregida(carpeta)
        t0, t1 = parse_ms(args.t0), parse_ms(args.t1)
        if t1 < t0:
            raise TranscripcionError("--t1 no puede ser anterior a --t0")
        trozo = texto_entre(segmentos, t0, t1, round(args.margen_s * 1000))
    except (ManifiestoTranscripcionError, TranscripcionError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"# {t.id} · capa {args.capa} · {args.t0}-{args.t1} (margen {args.margen_s:g} s)")
    sys.stdout.write(a_texto_legible(trozo))
    return 0


def evidence_new(repo: Path, args: argparse.Namespace) -> int:
    """Crea un item de evidencia con su id calculado (nunca sobreescribe).

    Antes de escribir se comprueba contra el manifiesto (duracion, fotogramas, supersede): un
    item es inmutable, asi que un error no se corrige, se evita.
    """
    from botsito.corpus.inventario import InventarioError, cargar_fuentes, cargar_manifiesto
    from botsito.evidence.modelo import (
        EvidenceItem,
        EvidenciaError,
        cargar_evidencia,
        escribir_item,
        validar_contra_manifiesto,
    )

    if not (repo / "knowledge").is_dir():
        print("ERROR: falta knowledge/ (¿--repo apunta a la raiz del proyecto?)")
        return 2
    try:
        conocidos = {
            v.video_id
            for v in cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml").videos
        }
        ruta_manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
        manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
    except InventarioError as exc:
        print(f"ERROR: fuentes del corpus: {exc}")
        return 1
    if args.video not in conocidos:
        print(f"ERROR: video {args.video!r} no esta en fuentes.yaml ({sorted(conocidos)})")
        return 1
    directorio = repo / "knowledge" / "evidence"
    try:
        existentes = cargar_evidencia(directorio)
    except EvidenciaError as exc:
        print(f"ERROR: evidencia existente: {exc}")
        return 1

    def comprobar(item: EvidenceItem) -> list[str]:
        if manifiesto is None:
            return []
        todos = [*existentes, item]
        return [p for p in validar_contra_manifiesto(todos, manifiesto) if p.startswith(item.id)]

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
        ruta = escribir_item(directorio, campos, comprobar)
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


def feedback_new(repo: Path, args: argparse.Namespace) -> int:
    """Crea un registro de feedback. Se valida contra el contexto (evidencia, registro,
    contradicciones, corpus) ANTES de escribir: un registro es inmutable."""
    from botsito.config.registro import RegistroError
    from botsito.corpus.inventario import InventarioError
    from botsito.evidence.modelo import EvidenciaError
    from botsito.feedback.modelo import (
        FeedbackError,
        FeedbackRecord,
        cargar_feedback,
        escribir_registro,
        validar_contra_contexto,
    )
    from botsito.validation.knowledge import contexto_feedback

    if not (repo / "knowledge").is_dir():
        print("ERROR: falta knowledge/ (¿--repo apunta a la raiz del proyecto?)")
        return 2
    directorio = repo / "knowledge" / "feedback"
    try:
        existentes = cargar_feedback(directorio)
        ids_ev, nombres, temas, rutas_corpus = contexto_feedback(repo)
    except (FeedbackError, EvidenciaError, RegistroError, InventarioError) as exc:
        print(f"ERROR: contexto de knowledge/: {exc}")
        return 1

    def comprobar(r: FeedbackRecord) -> list[str]:
        todos = [*existentes, r]
        problemas = validar_contra_contexto(todos, ids_ev, nombres, temas, rutas_corpus)
        return [p for p in problemas if p.startswith(r.id) or p.startswith("ciclo")]

    campos = {
        "sesion": args.sesion,
        "fecha": args.fecha,
        "medio": args.medio,
        "grabacion": args.grabacion,
        "t0": args.t0,
        "t1": args.t1,
        "objetivo": {"tipo": args.objetivo_tipo, "id": args.objetivo_id},
        "accion": args.accion,
        "respuesta_literal": args.respuesta,
        "valor_resultante": args.valor,
        "registrado_por": args.registrado_por,
        "supersede": args.supersede,
        "notas": args.notas,
    }
    try:
        ruta = escribir_registro(directorio, campos, comprobar)
    except FeedbackError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"OK: {ruta.relative_to(repo).as_posix()}")
    return 0


def feedback_trace(repo: Path, identificador: str) -> int:
    """Cadena de un objeto: el item de evidencia (si lo es) y los registros de feedback."""
    from botsito.evidence.modelo import EvidenciaError, cargar_evidencia
    from botsito.feedback.modelo import FeedbackError, cargar_feedback, trazar

    try:
        registros = cargar_feedback(repo / "knowledge" / "feedback")
        items = cargar_evidencia(repo / "knowledge" / "evidence")
    except (FeedbackError, EvidenciaError) as exc:
        print(f"ERROR: {exc}")
        return 1
    for it in items:
        if it.id == identificador:
            print(f"evidencia {it.id} [{it.video_id} {it.t0}-{it.t1}] {it.tema}: {it.cita_literal}")
    for linea in trazar(identificador, registros):
        print(linea)
    return 0


def feedback_pending(repo: Path) -> int:
    """Registros activos cuyo objetivo todavia no esta reflejado en la spec (todos, hasta F11).

    Un parametro que no sea de categoria `estrategia` no se le pregunta al trader (ADR-0004):
    un registro sobre el no aparece como pendiente.
    """
    from botsito.config.registro import RegistroError, cargar_registro
    from botsito.feedback.modelo import FeedbackError, activos, cargar_feedback

    try:
        registros = activos(cargar_feedback(repo / "knowledge" / "feedback"))
        parametros = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml").parametros
    except (FeedbackError, RegistroError) as exc:
        print(f"ERROR: {exc}")
        return 1
    registros = [
        r
        for r in registros
        if r.objetivo.tipo != "parametro"
        or r.objetivo.id not in parametros
        or parametros[r.objetivo.id].categoria == "estrategia"
    ]
    for r in sorted(registros, key=lambda r: (r.fecha, r.id)):
        print(f"{r.fecha} {r.id} {r.accion} {r.objetivo.tipo}:{r.objetivo.id}")
    print(f"{len(registros)} registros activos pendientes de reflejar en la spec (F11)")
    return 0


def _carpeta_datos(repo: Path) -> Path:
    """`[rutas].data` de settings.local.toml si existe; si no, la del ejemplo."""
    from botsito.config.ajustes import AjustesError, cargar_ajustes

    for nombre in ("settings.local.toml", "settings.example.toml"):
        ruta = repo / "config" / nombre
        if ruta.exists():
            try:
                return repo / cargar_ajustes(ruta).data
            except AjustesError as exc:
                raise SystemExit(f"ERROR: {nombre}: {exc}") from exc
    return repo / "data"


def _parse_anclaje(texto: str) -> HoraLocal:
    """`HH:MM Zona/IANA` -> HoraLocal. La zona la valida la agregacion."""
    m = re.fullmatch(r"\s*([01]\d|2[0-3]):([0-5]\d)\s+(\S+)\s*", texto, re.ASCII)
    if not m:
        raise SystemExit(f"ERROR: --anclaje debe ser 'HH:MM Zona/IANA', no {texto!r}")
    return HoraLocal(f"{m.group(1)}:{m.group(2)}", m.group(3))


def data_download(repo: Path, args: argparse.Namespace) -> int:
    """Congela un dataset M1 (descarga por dias, CSV por mes, manifiesto inmutable)."""
    from datetime import UTC, date, datetime

    from botsito.data.dataset import DatasetError, congelar
    from botsito.data.dukascopy import DescargaError, FormatoBi5Error, con_cache, descarga_http

    if not (repo / "knowledge").is_dir():
        print("ERROR: falta knowledge/ (¿--repo apunta a la raiz del proyecto?)")
        return 2
    try:
        desde, hasta = date.fromisoformat(args.desde), date.fromisoformat(args.hasta)
    except ValueError as exc:
        print(f"ERROR: fechas AAAA-MM-DD: {exc}")
        return 1
    commit = _git(repo, "rev-parse", "--short", "HEAD")
    carpeta_datos = _carpeta_datos(repo)
    try:
        congelado = congelar(
            repo,
            carpeta_datos,
            args.dataset,
            args.simbolo,
            args.escala,
            desde,
            hasta,
            con_cache(carpeta_datos / "raw", descarga_http),
            hoy=datetime.now(UTC).date(),
            reemplaza_a=args.reemplaza_a,
            generado_por=commit,
        )
    except (DatasetError, DescargaError, FormatoBi5Error) as exc:
        print(f"ERROR: {exc}")
        return 1
    m = congelado.manifiesto
    print(f"OK: {congelado.ruta_manifiesto.relative_to(repo).as_posix()} ({m['dataset_id']})")
    d = m["dias"]
    print(
        f"  {d['velas']} velas M1 en {len(m['ficheros'])} ficheros; dias presentes "
        f"{d['presentes']}, ausentes {len(d['ausentes'])}, sin datos {len(d['sin_datos'])}; "
        f"planas descartadas "
        f"{d['descartadas_planas_sin_volumen']} ({d['descartadas_dentro_de_sesion']} dentro de "
        f"sesion); "
        f"huecos >= 60 min: {len(m['huecos']['mayores'])}"
    )
    print("Commit del manifiesto con Fuente: ADR-0005 (es inmutable: no se edita)")
    return 0


def data_check(repo: Path, args: argparse.Namespace) -> int:
    from botsito.data.dataset import DatasetError, buscar_manifiesto, cargar_manifiesto, comprobar

    try:
        manifiesto = cargar_manifiesto(buscar_manifiesto(repo, args.dataset))
    except DatasetError as exc:
        print(f"ERROR: {exc}")
        return 1
    carpeta = _carpeta_datos(repo)
    problemas = comprobar(manifiesto, carpeta, hashes=args.hashes)
    for p in problemas:
        print(f"ERROR: {p} (carpeta de datos: {carpeta})")
    if not problemas:
        modo = "hashes" if args.hashes else "tamanos"
        print(f"OK: {manifiesto['dataset_id']} coincide con el disco ({modo})")
    return 1 if problemas else 0


def data_aggregate(repo: Path, args: argparse.Namespace) -> int:
    """Agrega M1 de un dataset a `--periodo` minutos con `--anclaje` explicito.

    El anclaje va por argumento y no del registro: `anclaje_h4` sigue UNKNOWN (A-9). Las velas
    de borde no cerradas se omiten salvo `--incluir-incompletas`.
    """
    from datetime import date

    from botsito.data.agregacion import AnclajeError, agregar
    from botsito.data.dataset import (
        DatasetError,
        buscar_manifiesto,
        cargar_manifiesto,
        cargar_serie,
    )
    from botsito.data.velas import VelasCsvError, escribir_csv

    anclaje = _parse_anclaje(args.anclaje)
    try:
        desde = date.fromisoformat(args.desde) if args.desde else None
        hasta = date.fromisoformat(args.hasta) if args.hasta else None
        if desde and hasta and hasta < desde:
            raise ValueError(f"--hasta {hasta} anterior a --desde {desde}")
        manifiesto = cargar_manifiesto(buscar_manifiesto(repo, args.dataset))
        serie = cargar_serie(manifiesto, _carpeta_datos(repo), desde, hasta)
        velas = agregar(list(serie.velas), args.periodo, anclaje)
    except (DatasetError, VelasCsvError, AnclajeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    if not serie.velas:
        print("AVISO: la ventana no contiene ninguna M1 del dataset", file=sys.stderr)
    omitidas = [v for v in velas if not v.completa]
    if not args.incluir_incompletas:
        velas = [v for v in velas if v.completa]
    comentario = (
        f"dataset={manifiesto['dataset_id']} periodo_min={args.periodo} "
        f"anclaje={anclaje.hora} {anclaje.huso} escala={manifiesto['escala']}"
    )
    texto = escribir_csv(velas, agregadas=True, comentario=comentario)
    if args.salida:
        try:
            destino = Path(args.salida)
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(texto, encoding="utf-8", newline="\n")
        except OSError as exc:
            print(f"ERROR: no se pudo escribir {args.salida}: {exc}")
            return 1
        print(f"OK: {len(velas)} velas de {args.periodo} min en {args.salida}")
    else:
        sys.stdout.write(texto)
    if omitidas and not args.incluir_incompletas:
        print(f"AVISO: {len(omitidas)} velas de borde sin cerrar omitidas", file=sys.stderr)
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
    know_sub.add_parser(
        "validate", help="valida knowledge/: registro, manifiesto, evidencia, feedback, historial"
    )
    corpus = sub.add_parser("corpus", help="inventario del corpus")
    corpus_sub = corpus.add_subparsers(dest="corpus_cmd", required=True)
    inv = corpus_sub.add_parser("inventory", help="genera knowledge/corpus/manifest.yaml")
    inv.add_argument(
        "--sin-hash",
        action="store_true",
        help="no calcular SHA-256 (rapido; el manifiesto resultante NO pasa knowledge validate)",
    )
    chk = corpus_sub.add_parser("check", help="compara el manifiesto con el disco")
    chk.add_argument("--hashes", action="store_true", help="verificar tambien SHA-256")
    tr = corpus_sub.add_parser("transcribe", help="transcribe un video por fragmentos (F04)")
    tr.add_argument("--video", required=True, help="video_id de fuentes.yaml (v1..v4)")
    tr.add_argument("--motor", choices=["faster-whisper", "falso"], default="faster-whisper")
    tr.add_argument("--modelo", default="large-v3")
    tr.add_argument("--dispositivo", default="cuda", choices=["cuda", "cpu"])
    tr.add_argument("--compute-type", dest="compute_type", default="int8_float16")
    tr.add_argument("--objetivo-s", dest="objetivo_s", type=float, default=600.0)
    tr.add_argument("--min-s", dest="min_s", type=float, default=420.0)
    tr.add_argument("--max-s", dest="max_s", type=float, default=780.0)
    tr.add_argument("--reemplaza-a", dest="reemplaza_a", help="transcripcion_id que sustituye")
    ga = corpus_sub.add_parser("glossary", help="glosario de correcciones del ASR")
    ga_sub = ga.add_subparsers(dest="glossary_cmd", required=True)
    gap = ga_sub.add_parser("apply", help="regenera corregida.jsonl = cruda + glosario")
    gap.add_argument("--video", help="solo este video_id")
    ts = corpus_sub.add_parser("transcript", help="transcripciones registradas")
    ts_sub = ts.add_subparsers(dest="transcript_cmd", required=True)
    ts_sub.add_parser("check", help="manifiestos frente al disco y al glosario")
    tss = ts_sub.add_parser("show", help="cita literal con marcas h:mm:ss.mmm")
    tss.add_argument("--video", required=True)
    tss.add_argument("--t0", required=True, help="h:mm:ss[.mmm]")
    tss.add_argument("--t1", required=True, help="h:mm:ss[.mmm]")
    tss.add_argument("--margen-s", dest="margen_s", type=float, default=0.0)
    tss.add_argument("--capa", choices=["cruda", "corregida"], default="corregida")
    tss.add_argument("--transcripcion", help="transcripcion_id (por defecto, la activa)")
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
    fb = sub.add_parser("feedback", help="registros del trader")
    fb_sub = fb.add_subparsers(dest="feedback_cmd", required=True)
    fbn = fb_sub.add_parser("new", help="crea un registro de feedback con id calculado")
    fbn.add_argument("--sesion", required=True, help="AAAA-MM-DD-sesion-NN")
    fbn.add_argument("--fecha", required=True)
    fbn.add_argument("--medio", required=True, choices=["replay", "audio", "video", "escrito"])
    fbn.add_argument("--grabacion", help="ruta en el corpus (obligatoria salvo escrito)")
    fbn.add_argument("--t0")
    fbn.add_argument("--t1")
    fbn.add_argument("--objetivo-tipo", required=True, dest="objetivo_tipo")
    fbn.add_argument("--objetivo-id", required=True, dest="objetivo_id")
    fbn.add_argument("--accion", required=True)
    fbn.add_argument("--respuesta", required=True, help="respuesta literal del trader")
    fbn.add_argument("--valor", help="valor resultante")
    fbn.add_argument("--registrado-por", required=True, dest="registrado_por")
    fbn.add_argument("--supersede")
    fbn.add_argument("--notas")
    fbt = fb_sub.add_parser("trace", help="cadena de feedback de un objeto")
    fbt.add_argument("identificador")
    fb_sub.add_parser("pending", help="registros activos pendientes de reflejar en la spec")
    datos = sub.add_parser("data", help="datasets de velas congelados (F15)")
    datos_sub = datos.add_subparsers(dest="data_cmd", required=True)
    dl = datos_sub.add_parser("download", help="descarga M1 por dias y congela un dataset")
    dl.add_argument("--dataset", required=True, help="nombre (el id anade -hash8)")
    dl.add_argument("--simbolo", required=True, help="simbolo del proveedor (mayusculas)")
    dl.add_argument("--escala", required=True, type=int, help="puntos por unidad de precio")
    dl.add_argument("--desde", required=True, help="AAAA-MM-DD")
    dl.add_argument("--hasta", required=True, help="AAAA-MM-DD (anterior a hoy)")
    dl.add_argument("--reemplaza-a", dest="reemplaza_a", help="dataset_id que este sustituye")
    dc = datos_sub.add_parser("check", help="compara un dataset con el disco")
    dc.add_argument("--dataset", required=True, help="dataset_id o nombre")
    dc.add_argument("--hashes", action="store_true", help="verificar tambien SHA-256")
    da = datos_sub.add_parser("aggregate", help="agrega M1 con anclaje de reloj de pared")
    da.add_argument("--dataset", required=True, help="dataset_id o nombre")
    da.add_argument("--periodo", required=True, type=int, help="minutos (divisor de 1440)")
    da.add_argument("--anclaje", required=True, help="'HH:MM Zona/IANA' (A-9 sigue abierta)")
    da.add_argument("--desde", help="AAAA-MM-DD (dia UTC inclusive)")
    da.add_argument("--hasta", help="AAAA-MM-DD (dia UTC inclusive)")
    da.add_argument("--salida", help="fichero CSV; sin el, escribe en la salida estandar")
    da.add_argument(
        "--incluir-incompletas",
        dest="incluir_incompletas",
        action="store_true",
        help="no omitir las velas de borde sin cerrar",
    )
    conf = sub.add_parser("config", help="ajustes de entorno")
    conf_sub = conf.add_subparsers(dest="config_cmd", required=True)
    conf_sub.add_parser("validate", help="comprueba config/settings*.toml contra el registro")
    return parser


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):  # consolas Windows en cp1252 y con CRLF
        sys.stdout.reconfigure(encoding="utf-8", newline="\n")
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.cmd == "state" and args.state_cmd == "check":
        return state_check(args.repo)
    if args.cmd == "knowledge" and args.knowledge_cmd == "validate":
        return knowledge_validate(args.repo)
    if args.cmd == "config" and args.config_cmd == "validate":
        return config_validate(args.repo)
    if args.cmd == "feedback" and args.feedback_cmd == "new":
        return feedback_new(args.repo, args)
    if args.cmd == "feedback" and args.feedback_cmd == "trace":
        return feedback_trace(args.repo, args.identificador)
    if args.cmd == "feedback" and args.feedback_cmd == "pending":
        return feedback_pending(args.repo)
    if args.cmd == "evidence" and args.evidence_cmd == "new":
        return evidence_new(args.repo, args)
    if args.cmd == "evidence" and args.evidence_cmd == "contradictions":
        return evidence_contradictions(args.repo)
    if args.cmd == "corpus" and args.corpus_cmd == "inventory":
        return corpus_inventory(args.repo, args.sin_hash)
    if args.cmd == "corpus" and args.corpus_cmd == "check":
        return corpus_check(args.repo, args.hashes)
    if args.cmd == "corpus" and args.corpus_cmd == "transcribe":
        return corpus_transcribe(args.repo, args)
    if args.cmd == "corpus" and args.corpus_cmd == "glossary" and args.glossary_cmd == "apply":
        return corpus_glossary_apply(args.repo, args)
    if args.cmd == "corpus" and args.corpus_cmd == "transcript" and args.transcript_cmd == "check":
        return corpus_transcript_check(args.repo)
    if args.cmd == "corpus" and args.corpus_cmd == "transcript" and args.transcript_cmd == "show":
        return corpus_transcript_show(args.repo, args)
    if args.cmd == "data" and args.data_cmd == "download":
        return data_download(args.repo, args)
    if args.cmd == "data" and args.data_cmd == "check":
        return data_check(args.repo, args)
    if args.cmd == "data" and args.data_cmd == "aggregate":
        return data_aggregate(args.repo, args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
