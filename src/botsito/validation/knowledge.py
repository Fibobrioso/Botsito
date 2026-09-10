"""Validacion de knowledge/ y de los manifiestos de datos (registro, corpus, evidencia,
contradicciones, feedback, historial de git, trailers Fuente). Orquestador movido desde la CLI
(ADR-0006): F12 (spec) y F14 (casos) anaden aqui sus capas; la CLI solo imprime.

Devuelve (codigo, lineas): 0 OK, 1 error de contenido, 2 estructura ausente.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


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


def contexto_feedback(
    repo: Path,
) -> tuple[set[str], set[str], set[str], set[str] | None, dict[str, float]]:
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
    duraciones: dict[str, float] = {}
    if ruta_manifiesto.exists():
        manifiesto = cargar_manifiesto(ruta_manifiesto)
        rutas_corpus, duraciones = rutas_y_duraciones(manifiesto)
    return {i.id for i in items}, set(registro.nombres()), temas, rutas_corpus, duraciones


def rutas_y_duraciones(manifiesto: dict[str, Any]) -> tuple[set[str], dict[str, float]]:
    """Rutas citables como `grabacion` (ficheros del corpus Y videos de fuentes.yaml, F10) y la
    duracion en segundos de cada video."""
    rutas = {str(f.get("ruta")) for f in (manifiesto.get("ficheros") or []) if isinstance(f, dict)}
    duraciones: dict[str, float] = {}
    for v in manifiesto.get("videos") or []:
        if isinstance(v, dict) and v.get("fichero"):
            rutas.add(str(v["fichero"]))
            d = v.get("duracion_s")
            if isinstance(d, int | float) and not isinstance(d, bool):
                duraciones[str(v["fichero"])] = float(d)
    return rutas, duraciones


def ids_ambiguedades(repo: Path) -> set[str] | None:
    """Ids de knowledge/spec/ambiguedades.yaml, o None si el fichero no existe (repos previos
    a F10: la ambiguedad se valida solo por formato)."""
    from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades

    ruta = repo / FICHERO_AMBIGUEDADES
    if not ruta.is_file():
        return None
    return {a.id for a in cargar_ambiguedades(ruta)}


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
    # Contexto de verificacion (F07): crudas, referencias de fotogramas, transcripciones.
    from botsito.corpus.manifiestos_fotogramas import ManifiestoFotogramasError
    from botsito.corpus.manifiestos_transcripcion import ManifiestoTranscripcionError
    from botsito.evidence.modelo import verificar_citas
    from botsito.evidence.propuestas import (
        DIRECTORIO_PROPUESTAS,
        FICHERO_PROMPT,
        PropuestaError,
        cargar_propuestas,
        validar_propuestas,
    )
    from botsito.validation.contexto_evidencia import construir_contexto

    contexto = None
    try:
        contexto, _temas = construir_contexto(repo, _carpeta_datos(repo), manifiesto)
    except (ManifiestoTranscripcionError, ManifiestoFotogramasError, PropuestaError) as exc:
        fallos.append(f"contexto de evidencia: {exc}")
    if manifiesto is not None:
        fallos += validar_contra_manifiesto(items, manifiesto, contexto)
    if contexto is not None:
        problemas_citas, avisos_citas, _loc = verificar_citas(items, contexto)
        fallos += problemas_citas
        for a in avisos_citas:
            salida.append(f"AVISO: {a}")
    fallos += contradicciones.validar_fichero(directorio, items)
    propuestas: list[dict[str, Any]] = []
    try:
        propuestas = cargar_propuestas(repo / DIRECTORIO_PROPUESTAS)
        ruta_prompt = repo / DIRECTORIO_PROPUESTAS / FICHERO_PROMPT
        prompt_sha = None
        if ruta_prompt.is_file():
            from botsito.comun.documentos import sha256_hex

            prompt_sha = sha256_hex(ruta_prompt.read_bytes().replace(b"\r\n", b"\n"))
        problemas_pr, avisos_pr = validar_propuestas(propuestas, items, prompt_sha)
        fallos += problemas_pr
        for a in avisos_pr:
            salida.append(f"AVISO: {a}")
    except PropuestaError as exc:
        fallos.append(f"propuestas: {exc}")
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
    duraciones: dict[str, float] = {}
    if manifiesto is not None:
        rutas_corpus, duraciones = rutas_y_duraciones(manifiesto)
    from botsito.cases.ambiguedades import (
        FICHERO_AMBIGUEDADES,
        AmbiguedadError,
        cargar_ambiguedades,
    )
    from botsito.cases.ambiguedades import validar_contra_contexto as validar_ambiguedades

    ambiguedades = []
    ids_amb: set[str] | None = None
    fallos_amb: list[str] = []
    if (repo / FICHERO_AMBIGUEDADES).is_file():
        try:
            ambiguedades = cargar_ambiguedades(repo / FICHERO_AMBIGUEDADES)
            ids_amb = {a.id for a in ambiguedades}
            fallos_amb = [
                f"ambiguedades: {p}"
                for p in validar_ambiguedades(
                    ambiguedades, {i.id for i in items}, set(registro.nombres()), temas
                )
            ]
        except AmbiguedadError as exc:
            fallos_amb = [f"ambiguedades: {exc}"]
    fallos_fb = fallos_amb + validar_contra_contexto(
        registros_fb,
        {i.id for i in items},
        set(registro.nombres()),
        temas,
        rutas_corpus,
        ids_amb,
        duraciones,
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
    # Alias: `cargar_manifiesto` ya nombra aqui el del corpus, y sombrearlo hace que
    # cualquier linea nueva de mas abajo use el de datos en silencio.
    from botsito.data.dataset import DIRECTORIO_MANIFIESTOS, DatasetError
    from botsito.data.dataset import cargar_manifiesto as cargar_manifiesto_dataset
    from botsito.data.dataset import manifiestos as listar_manifiestos

    fallos_datos: list[str] = []
    try:
        rutas_manifiestos = listar_manifiestos(repo)
        for ruta in rutas_manifiestos:
            cargar_manifiesto_dataset(ruta)
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
    # Un parametro no puede tener dos registros vigentes que FIJEN su valor: no habria forma de
    # saber cual manda. Lo comprobaba `feedback apply`, que solo se ejecuta cuando alguien lo
    # llama; aqui se vigila siempre. Ojo al matiz: dos REJECT vigentes sobre el mismo parametro no
    # son un problema -ninguno fija valor- y ademas no se pueden fusionar, porque un registro
    # supersede a UNO y dos cadenas paralelas no convergen anadiendo registros.
    from botsito.feedback.aplicar import ACCIONES_QUE_FIJAN

    fijan: dict[str, list[str]] = {}
    from botsito.comun.documentos import activos as _activos

    for registro_fb in _activos(list(registros_fb)):
        if registro_fb.objetivo.tipo != "parametro":
            continue
        if registro_fb.accion not in ACCIONES_QUE_FIJAN:
            continue
        if registro_fb.valor_resultante is None and registro_fb.valor_canonico is None:
            continue
        fijan.setdefault(registro_fb.objetivo.id, []).append(registro_fb.id)
    for nombre, ids_fijan in sorted(fijan.items()):
        if len(ids_fijan) > 1:
            salida.append(
                f"ERROR: feedback: {nombre} tiene {len(ids_fijan)} registros vigentes que fijan su "
                f"valor ({', '.join(sorted(ids_fijan))}); uno debe superseder al otro"
            )
            return 1, salida

    # Capa spec (F11, ADR-0013): reglas, glosario y manifiesto.
    from botsito.spec.manifiesto import FICHERO_MANIFIESTO
    from botsito.spec.manifiesto import comprobar as comprobar_manifiesto_spec
    from botsito.spec.modelo import (
        FICHERO_GLOSARIO,
        FICHERO_SPEC,
        SpecError,
        Termino,
        cargar_reglas,
        comprobar_contra,
        comprobar_literales,
    )
    from botsito.spec.modelo import (
        cargar_glosario as cargar_glosario_spec,
    )

    ruta_spec = repo / FICHERO_SPEC
    if ruta_spec.is_file():
        try:
            reglas = cargar_reglas(ruta_spec)
            terminos: list[Termino] = (
                cargar_glosario_spec(repo / FICHERO_GLOSARIO)
                if (repo / FICHERO_GLOSARIO).is_file()
                else []
            )
            citas = {i.id for i in items} | {r.id for r in registros_fb}
            problemas_spec = comprobar_contra(reglas, terminos, set(registro.nombres()), citas)
            # Y que cada regla diga lo que su cita dice: mismo criterio de tokens que ADR-0009
            # usa con la evidencia. Sin esto, una regla podria poner palabras en boca del
            # trader citando un registro que dice otra cosa.
            textos_citados = {i.id: i.cita_literal for i in items}
            textos_citados |= {r.id: r.respuesta_literal for r in registros_fb}
            problemas_spec += comprobar_literales(reglas, textos_citados)
            # Una regla vigente que nombra un parametro UNKNOWN no es un error de formato: es una
            # regla que el motor no podria ejecutar, y conviene verlo aqui y no en F18.
            for r in reglas:
                if not r.vigente:
                    continue
                for nombre in r.parametros:
                    param = registro.parametros.get(nombre)
                    if param is not None and param.estado.value == "UNKNOWN":
                        problemas_spec.append(
                            f"{r.id}: usa {nombre}, que sigue UNKNOWN: la regla esta vigente pero "
                            f"no se puede ejecutar"
                        )
            problemas_spec += comprobar_manifiesto_spec(repo, repo / FICHERO_MANIFIESTO)
        except SpecError as exc:
            problemas_spec = [str(exc)]
        for f in problemas_spec:
            salida.append(f"ERROR: spec: {f}")
        if problemas_spec:
            return 1, salida
        vigentes = sum(1 for r in reglas if r.vigente)
        salida.append(
            f"OK: {len(reglas)} reglas de spec ({vigentes} vigentes), {len(terminos)} terminos de "
            f"glosario, hash del manifiesto al dia"
        )

    # Capa kit (F10, ADR-0011): paquetes de sesion y guardia de particiones.
    from botsito.cases.paquete import KitError, sesiones_del_kit, validar_paquetes

    ids_datasets = {cargar_manifiesto_dataset(r)["dataset_id"] for r in rutas_manifiestos}
    try:
        fallos_kit, avisos_kit = validar_paquetes(
            repo, registros_fb, {i.id for i in items}, {str(d) for d in ids_datasets}
        )
    except KitError as exc:
        fallos_kit, avisos_kit = [str(exc)], []
    for a in avisos_kit:
        salida.append(f"AVISO: {a}")
    for f in fallos_kit:
        salida.append(f"ERROR: kit: {f}")
    if fallos_kit:
        return 1, salida
    n_sesiones = len(sesiones_del_kit(repo))
    if ambiguedades or n_sesiones:
        salida.append(
            f"OK: {len(ambiguedades)} ambiguedades registradas; {n_sesiones} paquetes de sesion "
            "validos, particiones anteriores al etiquetado"
        )
    abiertas = len(contradicciones.detectar(items))
    salida.append(
        f"OK: {len(registros_fb)} registros de feedback, historial intacto, commits con Fuente"
    )
    items_pendientes = sum(
        1
        for p in propuestas
        for it in (p.get("items") or [])
        if isinstance(it, dict) and it.get("decision", "pendiente") == "pendiente"
    )
    salida.append(
        f"OK: {len(items)} items de evidencia, {abiertas} contradicciones abiertas, "
        f"historial intacto; {len(propuestas)} propuestas ({items_pendientes} items pendientes)"
    )
    return 0, salida
