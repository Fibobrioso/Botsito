"""Validacion de knowledge/ y de los manifiestos de datos (registro, corpus, evidencia,
contradicciones, feedback, historial de git, trailers Fuente). Orquestador movido desde la CLI
(ADR-0006): F12 (spec) y F14 (casos) anaden aqui sus capas; la CLI solo imprime.

Devuelve (codigo, lineas): 0 OK, 1 error de contenido, 2 estructura ausente.
"""

from __future__ import annotations

from pathlib import Path


def _carpeta_datos(repo: Path) -> Path:
    from botsito.config.ajustes import carpeta_datos

    return carpeta_datos(repo)


def ids_de_adr(repo: Path) -> set[str]:
    """`ADR-NNNN` por cada docs/adr/NNNN-*.md real (la plantilla 0000 no es una decision)."""
    return {
        f"ADR-{p.name[:4]}"
        for p in (repo / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")
        if p.name[:4] != "0000"
    }


def contexto_feedback(repo: Path) -> tuple[set[str], set[str], set[str], set[str] | None]:
    """Lo que un registro de feedback puede citar: evidencia, parametros, contradicciones, corpus.

    Lanza el error de dominio del componente que falle; el llamador lo convierte en ERROR.
    """
    from botsito.config.registro import cargar_registro
    from botsito.corpus.inventario import cargar_manifiesto
    from botsito.evidence import contradicciones
    from botsito.evidence.modelo import cargar_evidencia

    items = cargar_evidencia(repo / "knowledge" / "evidence")
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    temas = {c["tema"] for c in contradicciones.detectar(items)}
    ruta_manifiesto = repo / "knowledge" / "corpus" / "manifest.yaml"
    rutas_corpus: set[str] | None = None
    if ruta_manifiesto.exists():
        manifiesto = cargar_manifiesto(ruta_manifiesto)
        rutas_corpus = {
            str(f.get("ruta")) for f in (manifiesto.get("ficheros") or []) if isinstance(f, dict)
        }
    return {i.id for i in items}, set(registro.nombres()), temas, rutas_corpus


def validar(repo: Path) -> tuple[int, list[str]]:
    """Valida todo lo que existe en knowledge/: registro, manifiesto, evidencia, feedback,
    historial de git y trailers `Fuente:` de spec/cases."""
    salida: list[str] = []
    if not (repo / "knowledge").is_dir():
        salida.append("ERROR: falta knowledge/")
        return 2, salida
    from botsito.config.ajustes import AjustesError
    from botsito.config.registro import RegistroError, cargar_registro

    try:
        _carpeta_datos(repo)
    except AjustesError as exc:
        salida.append(f"ERROR: ajustes: {exc}")
        return 1, salida
    try:
        registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    except RegistroError as exc:
        salida.append(f"ERROR: registro de parametros: {exc}")
        return 1, salida
    pendientes = registro.no_confirmados()
    salida.append(
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
                salida.append(f"ERROR: manifiesto: {p}")
            if problemas:
                return 1, salida
            salida.append(
                f"OK: manifiesto del corpus coherente con {len(fuentes.videos)} videos esperados"
            )
        else:
            salida.append(
                "AVISO: knowledge/corpus/manifest.yaml no existe (botsito corpus inventory)"
            )
    except InventarioError as exc:
        salida.append(f"ERROR: fuentes del corpus: {exc}")
        return 1, salida
    from botsito.comun.historial import (
        hay_git,
        historial_evaluable,
        modificaciones_en_historial,
    )
    from botsito.evidence import contradicciones
    from botsito.evidence.modelo import EvidenciaError, cargar_evidencia, validar_contra_manifiesto

    directorio = repo / "knowledge" / "evidence"
    try:
        items = cargar_evidencia(directorio)
    except EvidenciaError as exc:
        salida.append(f"ERROR: evidencia: {exc}")
        return 1, salida
    fallos: list[str] = []
    manifiesto = cargar_manifiesto(ruta_manifiesto) if ruta_manifiesto.exists() else None
    if manifiesto is not None:
        fallos += validar_contra_manifiesto(items, manifiesto)
    fallos += contradicciones.validar_fichero(directorio, items)
    con_git = hay_git(repo)
    no_evaluable = historial_evaluable(repo) if con_git else None
    historial = modificaciones_en_historial(repo)
    if historial is None and con_git:
        motivo = no_evaluable or "git fallo"
        fallos.append(f"la guardia de historial de evidencia no se pudo evaluar ({motivo})")
    elif historial:
        fallos += [f"evidencia modificada en el historial: {h}" for h in historial]
    for fallo in fallos:
        salida.append(f"ERROR: {fallo}")
    if fallos:
        return 1, salida
    from botsito.comun.historial import (
        ANCLA_FUENTE,
        DIRECTORIO_FEEDBACK,
        ancla_desviada,
        commits_sin_fuente,
        resolver,
    )
    from botsito.feedback.modelo import FeedbackError, cargar_feedback, validar_contra_contexto

    try:
        registros_fb = cargar_feedback(repo / "knowledge" / "feedback")
    except FeedbackError as exc:
        salida.append(f"ERROR: feedback: {exc}")
        return 1, salida
    temas = {c["tema"] for c in contradicciones.detectar(items)}
    rutas_corpus: set[str] | None = None
    if manifiesto is not None:
        rutas_corpus = {
            str(f.get("ruta")) for f in (manifiesto.get("ficheros") or []) if isinstance(f, dict)
        }
    fallos_fb = validar_contra_contexto(
        registros_fb, {i.id for i in items}, set(registro.nombres()), temas, rutas_corpus
    )
    historial_fb = modificaciones_en_historial(repo, DIRECTORIO_FEEDBACK)
    if historial_fb is None and con_git:
        motivo = no_evaluable or "git fallo"
        fallos_fb.append(f"la guardia de historial de feedback no se pudo evaluar ({motivo})")
    fallos_fb += [f"feedback modificado en el historial: {h}" for h in historial_fb or []]
    ids_validos = {i.id for i in items} | {r.id for r in registros_fb} | ids_de_adr(repo)
    # El ancla es el SHA: un tag se puede mover; si el tag existe y no coincide, es un error.
    tag, sha = ANCLA_FUENTE
    ancla = resolver(repo, sha) if con_git else None
    if con_git and ancla is None:
        fallos_fb.append(
            f"no se resuelve el ancla de trazabilidad {tag} ({sha[:7]}): "
            "clon superficial o sin historial; haz git fetch --unshallow --tags"
        )
    desviado = ancla_desviada(repo, tag, sha) if con_git else None
    if desviado:
        fallos_fb.append(desviado)
    sin_fuente = commits_sin_fuente(repo, ancla, ids_validos=ids_validos) if ancla else None
    if sin_fuente is None and con_git and ancla is not None:
        motivo = no_evaluable or "git fallo"
        fallos_fb.append(f"la comprobacion de trailers Fuente: no se pudo evaluar ({motivo})")
    fallos_fb += sin_fuente or []
    for fallo in fallos_fb:
        salida.append(f"ERROR: {fallo}")
    if fallos_fb:
        return 1, salida
    from botsito.data.dataset import DIRECTORIO_MANIFIESTOS, DatasetError, cargar_manifiesto
    from botsito.data.dataset import manifiestos as listar_manifiestos

    fallos_datos: list[str] = []
    try:
        rutas_manifiestos = listar_manifiestos(repo)
        for ruta in rutas_manifiestos:
            cargar_manifiesto(ruta)
    except DatasetError as exc:
        fallos_datos.append(f"manifiesto de datos: {exc}")
    historial_datos = modificaciones_en_historial(repo, DIRECTORIO_MANIFIESTOS)
    if historial_datos is None and con_git:
        motivo = no_evaluable or "git fallo"
        fallos_datos.append(f"la guardia de historial de manifiestos no se pudo evaluar ({motivo})")
    fallos_datos += [
        f"manifiesto de datos modificado en el historial: {h}" for h in historial_datos or []
    ]
    from botsito.comun.historial import DIRECTORIO_TRANSCRIPCIONES
    from botsito.corpus.glosario import GlosarioError, cargar_glosario
    from botsito.corpus.manifiestos_transcripcion import (
        ManifiestoTranscripcionError,
        cargar_todos,
    )
    from botsito.corpus.manifiestos_transcripcion import comprobar as comprobar_transcripciones
    from botsito.corpus.transcripcion import TranscripcionError

    try:
        ruta_glosario = repo / "knowledge" / "corpus" / "glosario_asr.yaml"
        glosario = cargar_glosario(ruta_glosario) if ruta_glosario.exists() else None
        transcripciones = cargar_todos(repo)
        errores_tr, avisos_tr = comprobar_transcripciones(
            transcripciones, _carpeta_datos(repo), glosario
        )
        if transcripciones and glosario is None:
            errores_tr.append("hay transcripciones registradas pero falta glosario_asr.yaml")
    except (GlosarioError, ManifiestoTranscripcionError, TranscripcionError) as exc:
        errores_tr, avisos_tr, transcripciones = [f"transcripciones: {exc}"], [], []
    historial_tr = modificaciones_en_historial(repo, DIRECTORIO_TRANSCRIPCIONES)
    if historial_tr is None and con_git:
        motivo = no_evaluable or "git fallo"
        errores_tr.append(
            f"la guardia de historial de transcripciones no se pudo evaluar ({motivo})"
        )
    errores_tr += [
        f"manifiesto de transcripcion modificado en el historial: {h}" for h in historial_tr or []
    ]
    for a in avisos_tr:
        salida.append(f"AVISO: {a}")
    fallos_datos += errores_tr
    from botsito.comun.historial import DIRECTORIO_FOTOGRAMAS
    from botsito.corpus.fotogramas import FICHERO_OBLIGATORIOS, FotogramasError, cargar_obligatorios
    from botsito.corpus.manifiestos_fotogramas import (
        ManifiestoFotogramasError,
        comprobar_obligatorios,
    )
    from botsito.corpus.manifiestos_fotogramas import cargar_todos as cargar_fotogramas
    from botsito.corpus.manifiestos_fotogramas import comprobar as comprobar_fotogramas

    try:
        fotogramas = cargar_fotogramas(repo)
        errores_fr, avisos_fr = comprobar_fotogramas(fotogramas, _carpeta_datos(repo))
        errores_fr += comprobar_obligatorios(
            fotogramas, cargar_obligatorios(repo / FICHERO_OBLIGATORIOS)
        )
    except (FotogramasError, ManifiestoFotogramasError) as exc:
        errores_fr, avisos_fr, fotogramas = [f"fotogramas: {exc}"], [], []
    historial_fr = modificaciones_en_historial(repo, DIRECTORIO_FOTOGRAMAS)
    if historial_fr is None and con_git:
        motivo = no_evaluable or "git fallo"
        errores_fr.append(f"la guardia de historial de fotogramas no se pudo evaluar ({motivo})")
    errores_fr += [
        f"manifiesto de fotogramas modificado en el historial: {h}" for h in historial_fr or []
    ]
    for a in avisos_fr:
        salida.append(f"AVISO: {a}")
    fallos_datos += errores_fr
    for fallo in fallos_datos:
        salida.append(f"ERROR: {fallo}")
    if fallos_datos:
        return 1, salida
    salida.append(f"OK: {len(transcripciones)} transcripciones registradas, historial intacto")
    salida.append(
        f"OK: {len(fotogramas)} extracciones de fotogramas registradas, obligatorios presentes, "
        "historial intacto"
    )
    salida.append(f"OK: {len(rutas_manifiestos)} manifiestos de datos validos, historial intacto")
    abiertas = len(contradicciones.detectar(items))
    salida.append(
        f"OK: {len(registros_fb)} registros de feedback, historial intacto, commits con Fuente"
    )
    salida.append(
        f"OK: {len(items)} items de evidencia, {abiertas} contradicciones abiertas, "
        "historial intacto"
    )
    return 0, salida
