"""Linea de comandos minima. Cada funcionalidad anade su subcomando aqui."""

from __future__ import annotations

import argparse
import ast
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from botsito import __version__
from botsito.domain.valores import HoraLocal

if TYPE_CHECKING:
    from botsito.corpus.fotogramas import Obligatorio
    from botsito.corpus.glosario import Glosario
    from botsito.evidence.modelo import EvidenceItem

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
                    f"main tiene cambios sin tag estable desde {tag}: {', '.join(ajenos)} "
                    "(en main, tras el tag, solo puede cambiar PROJECT_STATE.md; el HANDOFF y "
                    "cualquier otro fichero entran por una rama con su tag: MASTER_PLAN §F)"
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


def _glosario(repo: Path) -> Glosario:
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
    if args.video and not any(t.video_id == args.video for t in items):
        print(f"ERROR: no hay ninguna transcripcion registrada del video {args.video!r}")
        return 1
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
        if args.margen_s < 0:
            raise TranscripcionError("--margen-s no puede ser negativo")
        trozo = texto_entre(segmentos, t0, t1, round(args.margen_s * 1000))
    except (ManifiestoTranscripcionError, TranscripcionError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"# {t.id} · capa {args.capa} · {args.t0}-{args.t1} (margen {args.margen_s:g} s)")
    sys.stdout.write(a_texto_legible(trozo))
    return 0


def _obligatorios(repo: Path) -> list[Obligatorio]:
    from botsito.corpus.fotogramas import FICHERO_OBLIGATORIOS, cargar_obligatorios

    return cargar_obligatorios(repo / FICHERO_OBLIGATORIOS)


def corpus_frames_extract(repo: Path, args: argparse.Namespace) -> int:
    """Cobertura completa a 1 fps sin perdida mas los obligatorios (F05, ADR-0008)."""
    from botsito.corpus.fotogramas import FotogramasError, extraer_video
    from botsito.corpus.inventario import InventarioError
    from botsito.corpus.manifiestos_fotogramas import ManifiestoFotogramasError, cargar_todos

    try:
        raiz, fichero, sha, duracion = _video_del_corpus(repo, args.video)
        obligatorios = [o.t_ms for o in _obligatorios(repo) if o.video_id == args.video]
        if args.reemplaza_a:
            previas = {t.id: t for t in cargar_todos(repo)}
            if args.reemplaza_a not in previas:
                raise FotogramasError(f"--reemplaza-a {args.reemplaza_a}: no existe ese manifiesto")
            if previas[args.reemplaza_a].video_id != args.video:
                raise FotogramasError(
                    f"--reemplaza-a {args.reemplaza_a}: es de "
                    f"{previas[args.reemplaza_a].video_id}, no de {args.video}"
                )
        r = extraer_video(
            repo,
            _carpeta_datos(repo),
            raiz,
            args.video,
            fichero,
            sha,
            duracion,
            obligatorios,
            reemplaza_a=args.reemplaza_a,
            progreso=lambda msg: print(f"  {msg}", flush=True),
        )
    except (InventarioError, FotogramasError, ManifiestoFotogramasError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    extra = sum(1 for f in r.fotogramas if f.origen == "obligatorio")
    print(f"OK: {r.fotogramas_id} ({len(r.fotogramas)} fotogramas, {extra} extra)")
    print(f"  indice: {r.indice}")
    print(
        f"  manifiesto: {r.manifiesto.relative_to(repo).as_posix()} (INMUTABLE; commit sin editar)"
    )
    return 0


def corpus_frames_check(repo: Path) -> int:
    from botsito.corpus.fotogramas import FotogramasError
    from botsito.corpus.manifiestos_fotogramas import (
        ManifiestoFotogramasError,
        cargar_todos,
        comprobar,
        comprobar_obligatorios,
    )

    try:
        items = cargar_todos(repo)
        obligatorios = _obligatorios(repo)
    except (FotogramasError, ManifiestoFotogramasError) as exc:
        print(f"ERROR: {exc}")
        return 1
    errores, avisos = comprobar(items, _carpeta_datos(repo))
    errores += comprobar_obligatorios(items, obligatorios)
    for a in avisos:
        print(f"AVISO: {a}")
    for e in errores:
        print(f"ERROR: {e}")
    if not errores:
        print(
            f"OK: {len(items)} extracciones coherentes con el disco; "
            f"{len(obligatorios)} obligatorios presentes"
        )
    return 1 if errores else 0


def corpus_frames_show(repo: Path, args: argparse.Namespace) -> int:
    """Fotogramas mas cercanos a un instante, con la referencia citable `fr-<id>/<t_ms>` y el
    segmento de la transcripcion activa que cubre ese instante (si la hay)."""
    from botsito.corpus.fotogramas import FotogramasError, cargar_indice, mas_cercanos, referencia
    from botsito.corpus.manifiestos_fotogramas import (
        ManifiestoFotogramasError,
        activa_de,
        cargar_todos,
        carpeta_de,
    )
    from botsito.corpus.transcripcion import TranscripcionError, formato_ms, parse_ms

    try:
        t_ms = parse_ms(args.t)
        fr = activa_de(cargar_todos(repo), args.video)
        carpeta = carpeta_de(_carpeta_datos(repo), fr)
        if not (carpeta / "index.jsonl").is_file():
            raise FotogramasError(f"{fr.id}: los fotogramas no estan en esta maquina ({carpeta})")
        fin_ms = round(float(fr.doc["duracion_video_s"]) * 1000)
        elegidos = mas_cercanos(cargar_indice(carpeta), t_ms, args.n, fin_ms)
    except (ManifiestoFotogramasError, FotogramasError, TranscripcionError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"# {fr.id} · {args.t} ({t_ms} ms)")
    for f in elegidos:
        print(
            f"{referencia(fr.id, f.t_ms)}\t{formato_ms(f.pts_ms)}\t{f.origen}\t"
            f"{(carpeta / f.fichero).as_posix()}"
        )
    print(_segmento_en(repo, args.video, t_ms))
    return 0


def _segmento_en(repo: Path, video_id: str, t_ms: int) -> str:
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        activa_de,
        cargar_todos,
        carpeta_de,
    )
    from botsito.corpus.pipeline_transcripcion import cargar_cruda
    from botsito.corpus.transcripcion import a_texto_legible, texto_entre

    try:
        tr = activa_de(cargar_todos(repo), video_id)
        carpeta = carpeta_de(_carpeta_datos(repo), tr)
        if not (carpeta / "cruda.jsonl").is_file():
            return f"# transcripcion {tr.id}: cruda no esta en esta maquina"
        trozo = texto_entre(cargar_cruda(carpeta), t_ms, t_ms, 0)
    except (ManifiestoTranscripcionError, OSError, ValueError):
        return "# sin transcripcion activa para este video"
    if not trozo:
        return f"# transcripcion {tr.id}: ningun segmento cubre este instante"
    return f"# transcripcion {tr.id} (cruda):\n" + a_texto_legible(trozo).rstrip()


class _EntornoEvidencia:
    """Lo que `evidence new|accept|propose` necesitan: fuentes, manifiesto, evidencia existente
    y el contexto de verificacion (crudas, referencias, transcripciones)."""

    def __init__(self, repo: Path) -> None:
        from botsito.corpus.inventario import cargar_fuentes, cargar_manifiesto
        from botsito.evidence.modelo import cargar_evidencia
        from botsito.validation.contexto_evidencia import construir_contexto

        self.repo = repo
        self.videos = {
            v.video_id
            for v in cargar_fuentes(repo / "knowledge" / "corpus" / "fuentes.yaml").videos
        }
        ruta_manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
        self.manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
        self.directorio = repo / "knowledge" / "evidence"
        self.existentes = cargar_evidencia(self.directorio)
        self.contexto, self.temas = construir_contexto(repo, _carpeta_datos(repo), self.manifiesto)

    def comprobar(self, item: EvidenceItem) -> list[str]:
        """Problemas del item nuevo en el contexto real: manifiesto, referencias y cita."""
        from botsito.evidence.modelo import validar_contra_manifiesto, verificar_citas
        from botsito.evidence.verificacion import comprobar_referencias, tramo_no_citable

        todos = [*self.existentes, item]
        problemas: list[str] = []
        fuera = tramo_no_citable(self.contexto, item.video_id, item.t0_ms, item.t1_ms)
        if fuera is not None:
            problemas.append(f"{item.id}: el tramo no es especificacion, {fuera}")
        if self.manifiesto is not None:
            problemas += validar_contra_manifiesto(todos, self.manifiesto, self.contexto)
        elif item.modalidad in ("pantalla", "ambas") or item.fotogramas:
            # Sin manifiesto del corpus, las referencias se comprueban igual.
            if self.contexto.referencias is None:
                problemas.append(f"{item.id}: faltan referencias conocidas para validar fotogramas")
            else:
                problemas += [
                    f"{item.id}: {p}"
                    for p in comprobar_referencias(
                        item.video_id,
                        item.t0_ms,
                        item.t1_ms,
                        item.modalidad,
                        list(item.fotogramas),
                        self.contexto.referencias,
                    )
                ]
        if item.cita_de_audio and item.transcripcion:
            if self.contexto.activas.get(item.video_id) != item.transcripcion:
                problemas.append(
                    f"{item.id}: transcripcion {item.transcripcion} no es la activa de "
                    f"{item.video_id} ({self.contexto.activas.get(item.video_id)})"
                )
            if self.contexto.crudas and self.contexto.crudas(item.transcripcion) is None:
                problemas.append(
                    f"{item.id}: la cruda de {item.transcripcion} no esta en data/: la cita no "
                    "se puede verificar aqui"
                )
        p_citas, _avisos, _loc = verificar_citas([item], self.contexto)
        problemas += p_citas
        return [p for p in problemas if p.startswith(item.id)]


def _errores_evidencia() -> tuple[type[Exception], ...]:
    from botsito.corpus.inventario import InventarioError
    from botsito.corpus.manifiestos_fotogramas import ManifiestoFotogramasError
    from botsito.corpus.manifiestos_transcripcion import ManifiestoTranscripcionError
    from botsito.evidence.modelo import EvidenciaError
    from botsito.evidence.propuestas import PropuestaError

    return (
        InventarioError,
        ManifiestoFotogramasError,
        ManifiestoTranscripcionError,
        EvidenciaError,
        PropuestaError,
    )


def evidence_new(repo: Path, args: argparse.Namespace) -> int:
    """Crea un item de evidencia con su id calculado (nunca sobreescribe).

    Antes de escribir se comprueba contra el manifiesto y el contexto (duracion, referencias de
    fotogramas, transcripcion activa, cita localizada en la cruda): un item es inmutable, asi que
    un error no se corrige, se evita.
    """
    from botsito.evidence.modelo import EvidenciaError, escribir_item

    if not (repo / "knowledge").is_dir():
        print("ERROR: falta knowledge/ (¿--repo apunta a la raiz del proyecto?)")
        return 2
    try:
        entorno = _EntornoEvidencia(repo)
    except _errores_evidencia() as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.video not in entorno.videos:
        print(f"ERROR: video {args.video!r} no esta en fuentes.yaml ({sorted(entorno.videos)})")
        return 1
    transcripcion = args.transcripcion
    if transcripcion is None and args.modalidad in ("audio", "ambas"):
        transcripcion = entorno.contexto.activas.get(args.video)
        if transcripcion is None:
            print(f"ERROR: {args.video} no tiene transcripcion activa; indica --transcripcion")
            return 1
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
        "transcripcion": transcripcion,
    }
    try:
        ruta = escribir_item(entorno.directorio, campos, entorno.comprobar)
    except EvidenciaError as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"OK: {ruta.relative_to(repo).as_posix()}")
    print("Regenera las contradicciones: botsito evidence contradictions")
    return 0


def _ahora() -> str:
    from datetime import UTC, datetime

    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _prompt_canonico(repo: Path) -> str:
    from botsito.evidence.propuestas import DIRECTORIO_PROPUESTAS, FICHERO_PROMPT

    ruta = repo / DIRECTORIO_PROPUESTAS / FICHERO_PROMPT
    return ruta.read_text(encoding="utf-8").replace("\r\n", "\n")


def evidence_propose(repo: Path, args: argparse.Namespace) -> int:
    """Esqueleto de una propuesta (`--video --t0 --t1`) o comprobacion de una rellena
    (`--check <fichero>`). Nunca escribe en knowledge/evidence/."""
    from botsito.corpus.transcripcion import TranscripcionError, parse_ms
    from botsito.evidence.propuestas import (
        DIRECTORIO_PROPUESTAS,
        PropuestaError,
        cargar_propuesta,
        cargar_propuestas,
        comprobar,
        escribir_propuesta,
        esqueleto,
        sellar,
    )
    from botsito.evidence.verificacion import t_ms_de_referencia, video_de_referencia

    try:
        entorno = _EntornoEvidencia(repo)
    except _errores_evidencia() as exc:
        print(f"ERROR: {exc}")
        return 1
    if args.check:
        ruta = Path(args.check)
        try:
            doc = cargar_propuesta(ruta)
            otras = cargar_propuestas(repo / DIRECTORIO_PROPUESTAS)
            r = comprobar(doc, entorno.contexto, entorno.temas, entorno.existentes, otras)
        except (PropuestaError, OSError) as exc:
            print(f"ERROR: {exc}")
            return 1
        for a in r.avisos:
            print(f"AVISO: {a}")
        for p in r.problemas:
            print(f"ERROR: {p}")
        for n, loc in sorted(r.localizaciones.items()):
            print(
                f"  item {n}: localizado en {_fmt_ms(loc.t0_ms)}-{_fmt_ms(loc.t1_ms)} "
                f"(segmentos {list(loc.segmentos)})"
            )
        if r.problemas:
            return 1
        sellar(doc, _ahora())
        escribir_propuesta(ruta, doc)
        print(f"OK: {len(doc['items'])} items, {len(doc['no_consta'])} no_consta; salida sellada")
        return 0
    if not (args.video and args.t0 and args.t1):
        print("ERROR: indica --video, --t0 y --t1 (o --check <fichero>)")
        return 2
    if args.video not in entorno.videos:
        print(f"ERROR: video {args.video!r} no esta en fuentes.yaml")
        return 1
    tid = entorno.contexto.activas.get(args.video)
    if tid is None:
        print(f"ERROR: {args.video} no tiene transcripcion activa")
        return 1
    segmentos = entorno.contexto.crudas(tid) if entorno.contexto.crudas else None
    if segmentos is None:
        print(f"ERROR: la cruda de {tid} no esta en data/")
        return 1
    try:
        t0, t1 = parse_ms(args.t0), parse_ms(args.t1)
    except TranscripcionError as exc:
        print(f"ERROR: {exc}")
        return 1
    tramo = [s for s in segmentos if s.t1_ms > t0 and s.t0_ms < t1]
    # Referencias del tramo, compactas: la cobertura es 1 fps (ADR-0008), asi que se anota el
    # manifiesto y el recuento por segundo, y solo los instantes con fraccion (obligatorios).
    en_tramo = [
        ref
        for ref in (entorno.contexto.referencias or set())
        if video_de_referencia(ref) == args.video and t0 <= t_ms_de_referencia(ref) <= t1
    ]
    por_manifiesto: dict[str, list[int]] = {}
    for ref in en_tramo:
        por_manifiesto.setdefault(ref.rsplit("/", 1)[0], []).append(t_ms_de_referencia(ref))
    referencias: list[str] = []
    for fid, instantes in sorted(por_manifiesto.items()):
        regulares = sorted(t for t in instantes if t % 1000 == 0)
        extras = sorted(t for t in instantes if t % 1000 != 0)
        if regulares:
            referencias.append(
                f"{fid}/<t_ms>: {len(regulares)} fotogramas regulares, uno por segundo, "
                f"de {regulares[0]} a {regulares[-1]} ms"
            )
        referencias += [f"{fid}/{t} (obligatorio)" for t in extras]
    try:
        doc = esqueleto(
            args.video,
            tid,
            args.t0,
            args.t1,
            tramo,
            referencias,
            _prompt_canonico(repo),
            args.modelo,
            args.proponente,
            args.tema_buscado or [],
            _ahora(),
        )
    except (PropuestaError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    salida = (
        Path(args.salida)
        if args.salida
        else repo / DIRECTORIO_PROPUESTAS / (doc["propuesta_id"] + ".yaml")
    )
    if salida.exists():
        print(f"ERROR: ya existe {salida}")
        return 1
    escribir_propuesta(salida, doc)
    print(f"OK: {salida.relative_to(repo).as_posix() if salida.is_relative_to(repo) else salida}")
    print(f"  {len(tramo)} segmentos de {tid}, {len(referencias)} referencias de fotogramas")
    return 0


def _fmt_ms(ms: int) -> str:
    from botsito.evidence.verificacion import formato_ms

    return formato_ms(ms)


def evidence_accept(repo: Path, args: argparse.Namespace) -> int:
    """Acepta un item propuesto: crea la evidencia (con todas las comprobaciones de `new`) y
    anota la decision en la propuesta."""
    from botsito.evidence.modelo import escribir_item
    from botsito.evidence.propuestas import (
        DIRECTORIO_PROPUESTAS,
        anotar_decision,
        campos_de_item,
        cargar_propuesta,
        cargar_propuestas,
        comprobar,
        comprobar_sello,
        escribir_propuesta,
    )

    errores: tuple[type[Exception], ...] = (*_errores_evidencia(), OSError)
    try:
        entorno = _EntornoEvidencia(repo)
        ruta = Path(args.propuesta)
        doc = cargar_propuesta(ruta)
        sello = comprobar_sello(doc)
        if sello:
            print(f"ERROR: {sello}")
            return 1
        otras = cargar_propuestas(repo / DIRECTORIO_PROPUESTAS)
        r = comprobar(doc, entorno.contexto, entorno.temas, entorno.existentes, otras)
        patron = re.compile(rf"\bitem {args.item}\b")
        mios = [p for p in r.problemas if patron.search(p)]
        globales = [p for p in r.problemas if not p.startswith("item ")]
        if mios or globales:
            for p in mios + globales:
                print(f"ERROR: {p}")
            return 1
        campos = campos_de_item(doc, args.item, args.revisado_por, args.metodo)
        if args.notas:
            previas = str(campos.get("notas") or "").strip()
            campos["notas"] = f"{previas} {args.notas}".strip()
        ruta_item = escribir_item(entorno.directorio, campos, entorno.comprobar)
        from botsito.evidence.modelo import cargar_item

        item = cargar_item(ruta_item)
        anotar_decision(
            doc, args.item, "aceptado", args.revisado_por, _ahora(), args.metodo, None, item.id
        )
        try:
            escribir_propuesta(ruta, doc)
        except OSError:
            # Sin decision anotada el item recien creado quedaria huerfano: se retira.
            ruta_item.unlink(missing_ok=True)
            raise
    except errores as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"OK: {ruta_item.relative_to(repo).as_posix()} (item {args.item} aceptado)")
    return 0


def evidence_reject(repo: Path, args: argparse.Namespace) -> int:
    from botsito.evidence.propuestas import (
        PropuestaError,
        anotar_decision,
        cargar_propuesta,
        comprobar_sello,
        escribir_propuesta,
    )

    try:
        ruta = Path(args.propuesta)
        doc = cargar_propuesta(ruta)
        sello = comprobar_sello(doc)
        if sello:
            print(f"ERROR: {sello}")
            return 1
        it = next((i for i in doc["items"] if i["n"] == args.item), None)
        if it is None:
            print(f"ERROR: la propuesta no tiene el item {args.item}")
            return 1
        if it.get("decision", "pendiente") != "pendiente":
            print(f"ERROR: el item {args.item} ya esta {it['decision']}")
            return 1
        anotar_decision(doc, args.item, "rechazado", args.decidido_por, _ahora(), None, args.motivo)
        escribir_propuesta(ruta, doc)
    except (PropuestaError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"OK: item {args.item} rechazado")
    return 0


def evidence_list(repo: Path, args: argparse.Namespace) -> int:
    from botsito.evidence.modelo import EvidenciaError, cargar_evidencia

    try:
        items = cargar_evidencia(repo / "knowledge" / "evidence")
    except EvidenciaError as exc:
        print(f"ERROR: {exc}")
        return 1
    filas = sorted(items, key=lambda i: (i.video_id, i.t0_s, i.id))
    if args.video:
        filas = [i for i in filas if i.video_id == args.video]
    if args.tema:
        filas = [i for i in filas if i.tema == args.tema or i.tema.startswith(args.tema + ".")]
    for i in filas:
        print(f"{i.id}  {i.video_id}  {i.t0}-{i.t1}  {i.modalidad:8s}  {i.tipo:14s}  {i.tema}")
    print(f"{len(filas)} items")
    return 0


def _kb_indice(repo: Path) -> Any:
    from botsito.retrieval.indice import construir_indice

    return construir_indice(repo, _carpeta_datos(repo))


def _kb_errores() -> tuple[type[Exception], ...]:
    from botsito.corpus.inventario import InventarioError
    from botsito.corpus.manifiestos_fotogramas import ManifiestoFotogramasError
    from botsito.corpus.manifiestos_transcripcion import ManifiestoTranscripcionError
    from botsito.corpus.transcripcion import TranscripcionError
    from botsito.evidence.modelo import EvidenciaError
    from botsito.retrieval.indice import RetrievalError

    return (
        RetrievalError,
        InventarioError,
        ManifiestoFotogramasError,
        ManifiestoTranscripcionError,
        TranscripcionError,
        EvidenciaError,
        OSError,
    )


def _kb_imprimir(respuesta: Any, como_json: bool, contexto: bool) -> int:
    from botsito.retrieval.salida import json_, tabla

    for a in respuesta.avisos:
        print(f"AVISO: {a}", file=sys.stderr)
    sys.stdout.write(
        json_(respuesta.resultados) if como_json else tabla(respuesta.resultados, contexto)
    )
    return 0


def kb_find(repo: Path, args: argparse.Namespace) -> int:
    """Busqueda lexica por texto sobre evidencia y crudas activas (F08, ADR-0010)."""
    from botsito.corpus.transcripcion import parse_ms
    from botsito.retrieval.consultas import Opciones, buscar

    try:
        opciones = Opciones(
            video=args.video,
            tema=args.tema,
            desde_ms=parse_ms(args.desde) if args.desde else None,
            hasta_ms=parse_ms(args.hasta) if args.hasta else None,
            solo=args.solo,
            frase=args.frase,
            prefijo=args.prefijo,
            top=args.top,
        )
        respuesta = buscar(_kb_indice(repo), args.texto, opciones)
    except _kb_errores() as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return _kb_imprimir(respuesta, args.json, args.contexto)


def kb_at(repo: Path, args: argparse.Namespace) -> int:
    """Todo lo que ocurre en un instante: evidencia, cruda, fotograma y contradicciones."""
    from botsito.corpus.transcripcion import parse_ms
    from botsito.retrieval.consultas import en_instante

    errores: tuple[type[Exception], ...] = (*_kb_errores(), ValueError)
    try:
        if not math.isfinite(args.margen_s):
            raise ValueError("el margen debe ser un numero finito")
        respuesta = en_instante(
            _kb_indice(repo), args.video, parse_ms(args.t), round(args.margen_s * 1000)
        )
    except errores as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return _kb_imprimir(respuesta, args.json, args.contexto)


def _kit_errores() -> tuple[type[Exception], ...]:
    from botsito.cases.paquete import KitError
    from botsito.config.ajustes import AjustesError
    from botsito.config.registro import RegistroError
    from botsito.corpus.inventario import InventarioError
    from botsito.data.dataset import DatasetError
    from botsito.domain.velas import VelaInvalidaError
    from botsito.evidence.modelo import EvidenciaError
    from botsito.feedback.modelo import FeedbackError
    from botsito.retrieval.indice import RetrievalError

    return (
        KitError,
        AjustesError,
        RegistroError,
        InventarioError,
        DatasetError,
        VelaInvalidaError,
        EvidenciaError,
        FeedbackError,
        RetrievalError,
        OSError,
    )


def kit_build(repo: Path, args: argparse.Namespace) -> int:
    """Genera el paquete de una sesion (F10, ADR-0011). Exige los datos en data/."""
    from botsito.cases.paquete import construir, escribir

    try:
        paquete = construir(repo, _carpeta_datos(repo), args.sesion, args.seed)
        carpeta = escribir(repo, paquete)
    except _kit_errores() as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    dev = sum(1 for v in paquete.asignacion.values() if v == "dev")
    print(
        f"OK: {carpeta.relative_to(repo).as_posix()}: {len(paquete.preguntas)} preguntas, "
        f"{len(paquete.casos)} casos ({dev} dev) de un universo de {paquete.universo} "
        f"(+ {len(paquete.excluidos)} dias excluidos), seed {paquete.seed}"
    )
    return 0


def kit_check(repo: Path, args: argparse.Namespace) -> int:
    from botsito.cases.paquete import comprobar

    try:
        problemas, avisos = comprobar(repo, _carpeta_datos(repo), args.sesion)
    except _kit_errores() as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for a in avisos:
        print(f"AVISO: {a}", file=sys.stderr)
    for p in problemas:
        print(f"ERROR: {p}", file=sys.stderr)
    if problemas:
        return 1
    print(f"OK: {args.sesion} se recompone igual desde el repo y data/")
    return 0


def kit_kappa(repo: Path, args: argparse.Namespace) -> int:
    from botsito.cases.paquete import kappa_entre_sesiones
    from botsito.feedback.modelo import cargar_feedback

    try:
        registros = cargar_feedback(repo / "knowledge" / "feedback")
        r = kappa_entre_sesiones(repo, registros, args.sesion_a, args.sesion_b)
    except _kit_errores() as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    for a in r.avisos:
        print(f"AVISO: {a}", file=sys.stderr)
    kappa = "indefinida" if r.kappa is None else f"{float(r.kappa):.3f}"
    print(f"unidades: {r.unidades}  po: {float(r.po):.3f}  pe: {float(r.pe):.3f}  kappa: {kappa}")
    for x, fila in r.matriz.items():
        print(f"  {x:10s} " + " ".join(f"{fila[y]:4d}" for y in fila))
    for x, v in r.acuerdo_por_categoria.items():
        print(f"  acuerdo {x}: {float(v):.3f}")
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
    from botsito.cases.ambiguedades import AmbiguedadError
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
        ids_ev, nombres, temas, rutas_corpus, duraciones = contexto_feedback(repo)
        from botsito.validation.knowledge import ids_ambiguedades

        ids_amb = ids_ambiguedades(repo)
    except (FeedbackError, EvidenciaError, RegistroError, InventarioError, AmbiguedadError) as exc:
        print(f"ERROR: contexto de knowledge/: {exc}")
        return 1

    def comprobar(r: FeedbackRecord) -> list[str]:
        todos = [*existentes, r]
        problemas = validar_contra_contexto(
            todos, ids_ev, nombres, temas, rutas_corpus, ids_amb, duraciones
        )
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
    """`[rutas].data` (config/ajustes.carpeta_datos); un TOML roto aborta con ERROR."""
    from botsito.config.ajustes import AjustesError, carpeta_datos

    try:
        return carpeta_datos(repo)
    except AjustesError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc


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
    tr.add_argument("--video", required=True, help="video_id de fuentes.yaml (v1..v5)")
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
    fr = corpus_sub.add_parser("frames", help="fotogramas del corpus (F05)")
    fr_sub = fr.add_subparsers(dest="frames_cmd", required=True)
    fre = fr_sub.add_parser("extract", help="cobertura completa a 1 fps sin perdida + obligatorios")
    fre.add_argument("--video", required=True, help="video_id de fuentes.yaml (v1..v5)")
    fre.add_argument("--reemplaza-a", dest="reemplaza_a", help="fotogramas_id que sustituye")
    fr_sub.add_parser("check", help="manifiestos frente al disco y a los obligatorios")
    frs = fr_sub.add_parser("show", help="fotogramas mas cercanos a un instante")
    frs.add_argument("--video", required=True)
    frs.add_argument("--t", required=True, help="h:mm:ss[.mmm]")
    frs.add_argument("--n", type=int, default=1, help="cuantos fotogramas (por cercania)")
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
    nuevo.add_argument(
        "--transcripcion", help="id tr-* de la cruda citada (por defecto la activa del video)"
    )
    ev_sub.add_parser("contradictions", help="regenera knowledge/evidence/_contradicciones.yaml")
    kit = sub.add_parser(
        "kit", help="kit de elicitacion: paquete de una sesion con el trader (F10)"
    )
    kit_sub = kit.add_subparsers(dest="kit_cmd", required=True)
    kb_build = kit_sub.add_parser(
        "build", help="genera knowledge/cases/kit/<sesion>/ (no sobreescribe)"
    )
    kb_build.add_argument("--sesion", required=True, help="AAAA-MM-DD-sesion-NN")
    kb_build.add_argument("--seed", required=True, type=int)
    kb_check = kit_sub.add_parser("check", help="recompone el paquete y compara byte a byte")
    kb_check.add_argument("--sesion", required=True)
    kb_kappa = kit_sub.add_parser(
        "kappa", help="kappa de Cohen entre los LABEL_CASE de dos sesiones"
    )
    kb_kappa.add_argument("--sesion-a", dest="sesion_a", required=True)
    kb_kappa.add_argument("--sesion-b", dest="sesion_b", required=True)
    kb = sub.add_parser("kb", help="busqueda de desarrollo sobre la base de conocimiento (F08)")
    kb_sub = kb.add_subparsers(dest="kb_cmd", required=True)
    find = kb_sub.add_parser("find", help="por texto: AND de tokens, --frase o --prefijo")
    find.add_argument("texto")
    find.add_argument("--video")
    find.add_argument("--tema", help="raiz o tema completo; implica --solo evidencia")
    find.add_argument("--desde", help="h:mm:ss[.d] (exige --video)")
    find.add_argument("--hasta", help="h:mm:ss[.d] (exige --video)")
    find.add_argument("--solo", choices=["evidencia", "cruda"])
    find.add_argument("--frase", action="store_true", help="secuencia exacta con comodin [...]")
    find.add_argument("--prefijo", action="store_true", help="cada termino casa por inicio")
    find.add_argument(
        "--top", type=int, help="corta por el orden temporal (sin limite por defecto)"
    )
    find.add_argument(
        "--contexto", action="store_true", help="texto completo y afirmacion/corregida"
    )
    find.add_argument("--json", action="store_true")
    at = kb_sub.add_parser("at", help="todo lo que ocurre en un instante de un video")
    at.add_argument("--video", required=True)
    at.add_argument("--t", required=True, help="h:mm:ss[.d]")
    at.add_argument("--margen-s", dest="margen_s", type=float, default=10.0, help="0-120")
    at.add_argument("--contexto", action="store_true")
    at.add_argument("--json", action="store_true")
    prop = ev_sub.add_parser("propose", help="esqueleto de propuesta o --check de una rellena")
    prop.add_argument("--video")
    prop.add_argument("--t0")
    prop.add_argument("--t1")
    prop.add_argument("--modelo", default="pendiente", help="quien rellena la propuesta")
    prop.add_argument("--proponente", default="llm", choices=["llm", "humano"])
    prop.add_argument("--tema-buscado", dest="tema_buscado", action="append")
    prop.add_argument("--salida", help="ruta del fichero (por defecto knowledge/_proposals/)")
    prop.add_argument("--check", help="fichero de propuesta rellena a comprobar y sellar")
    acc = ev_sub.add_parser("accept", help="crea la evidencia de un item propuesto")
    acc.add_argument("--propuesta", required=True)
    acc.add_argument("--item", required=True, type=int)
    acc.add_argument("--revisado-por", required=True, dest="revisado_por")
    acc.add_argument(
        "--metodo",
        required=True,
        choices=["cruda_leida", "audio_oido", "fotograma_visto"],
        help="como reviso la persona",
    )
    acc.add_argument("--notas")
    rej = ev_sub.add_parser("reject", help="anota el rechazo de un item propuesto")
    rej.add_argument("--propuesta", required=True)
    rej.add_argument("--item", required=True, type=int)
    rej.add_argument("--motivo", required=True)
    rej.add_argument("--decidido-por", required=True, dest="decidido_por")
    lst = ev_sub.add_parser("list", help="tabla estable de items (id, video, t0, tipo, tema)")
    lst.add_argument("--video")
    lst.add_argument("--tema")
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
    for flujo in (sys.stdout, sys.stderr):  # consolas Windows en cp1252 y con CRLF
        if hasattr(flujo, "reconfigure"):
            flujo.reconfigure(encoding="utf-8", newline="\n")
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
    if args.cmd == "evidence" and args.evidence_cmd == "propose":
        return evidence_propose(args.repo, args)
    if args.cmd == "evidence" and args.evidence_cmd == "accept":
        return evidence_accept(args.repo, args)
    if args.cmd == "evidence" and args.evidence_cmd == "reject":
        return evidence_reject(args.repo, args)
    if args.cmd == "evidence" and args.evidence_cmd == "list":
        return evidence_list(args.repo, args)
    if args.cmd == "kit" and args.kit_cmd == "build":
        return kit_build(args.repo, args)
    if args.cmd == "kit" and args.kit_cmd == "check":
        return kit_check(args.repo, args)
    if args.cmd == "kit" and args.kit_cmd == "kappa":
        return kit_kappa(args.repo, args)
    if args.cmd == "kb" and args.kb_cmd == "find":
        return kb_find(args.repo, args)
    if args.cmd == "kb" and args.kb_cmd == "at":
        return kb_at(args.repo, args)
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
    if args.cmd == "corpus" and args.corpus_cmd == "frames" and args.frames_cmd == "extract":
        return corpus_frames_extract(args.repo, args)
    if args.cmd == "corpus" and args.corpus_cmd == "frames" and args.frames_cmd == "check":
        return corpus_frames_check(args.repo)
    if args.cmd == "corpus" and args.corpus_cmd == "frames" and args.frames_cmd == "show":
        return corpus_frames_show(args.repo, args)
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
