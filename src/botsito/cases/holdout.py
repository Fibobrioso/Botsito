"""La puerta del holdout (ADR-0033): el unico sitio por el que se ABRE material reservado.

ADR-0021 §1 define abrir un holdout como leer sus etiquetas -los `LABEL_CASE` de sus dias, o el
detalle por operacion del backtest- o medir una cifra del bot sobre ellos. Y §3 dice quien lo
autoriza y con que: el usuario, con `docs/validation/PREREGISTRO.md` commiteado ANTES y un ADR que
diga que se mide y contra que umbral. Hasta esta rama eso era solo texto: nada en el codigo lo
comprobaba, y la guarda de `tests/conftest.py` era un stub.

LO QUE PASA POR ESTA PUERTA, y lo que no (se comprueba con un grep, `test_import_contracts`):
  - Pasa: cualquier lectura de `knowledge/cases/holdout/{1,2,3}/**` que no sea su `README.md`
    (`leer_fichero`), y el VALOR de un `LABEL_CASE` cuyo caso esta asignado a una particion
    reservada (`kappa_entre_sesiones`, via `casos_reservados`). Ningun modulo de `src/` fuera de
    este nombra la carpeta del holdout.
  - NO pasa: las velas de mercado. Construir o comprobar un paquete exige leer las de todos los dias
    del universo, reservados incluidos -que dias son reservados depende de cuales entran, y eso de
    sus velas-, y leer velas para recalcular una ventana no es abrir (ADR-0021 §1). Tampoco pasan
    `knowledge validate`, `feedback pending` ni la guardia de ancestro: CARGAN los registros, pero
    no usan el valor de la etiqueta. La frontera es usar el valor, no cargar el fichero.

LA AUTORIZACION es un fichero COMMITEADO por particion,
`docs/validation/AUTORIZACION-<particion>.md`, y no una variable de entorno: una variable se deja
puesta sin querer y no queda en ningun sitio; un fichero commiteado con fecha, autor y ADR es
dificil de crear por accidente y trivial de auditar con `git log`. Y no basta con el: el
`PREREGISTRO.md` tiene que estar commiteado y RELLENO, y ser EXACTAMENTE el que se aprobo.

QUE VERSION SE APROBO lo fija `preregistro_blob`: el sha del BLOB de `PREREGISTRO.md`, no el de un
commit. Sin este campo se podia rellenar, autorizar, abrir y despues cambiar los umbrales: la
autorizacion seguia valiendo y el fichero seguia commiteado y relleno, que es justo lo que un
pre-registro existe para impedir. El blob y no el commit porque lo que se aprueba es un CONTENIDO:
el sha del blob cambia con cualquier byte del fichero y con nada mas -otro commit que no toque el
PREREGISTRO no lo mueve-, sobrevive a un rebase o a un merge, y se compara directamente con
`git rev-parse HEAD:docs/validation/PREREGISTRO.md`. El sha de un commit fija un instante: habria
que ir a buscar el fichero dentro de el, y un rebase lo deja apuntando a nada. Consecuencia
declarada: si los umbrales se cambian y despues se devuelven byte a byte a lo aprobado, la puerta
vuelve a abrir, porque el contenido vuelve a ser el aprobado.
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.comun.historial import blob_en_head, contenido_en_head
from botsito.comun.yaml_estricto import YamlError, leer_yaml

PARTICIONES_RESERVADAS = ("holdout-1", "holdout-2", "holdout-3")
# Las del camino de fidelidad (ADR-0036). ADR-0034 separo DOS cegueras: la DEL TRADER, que
# septiembre ya no tiene, y LA NUESTRA, que sigue intacta. Es la nuestra la que esta puerta
# protege, asi que el material etiquetado no ciego pasa por ella igual. Dejar estos nombres fuera
# seria material reservado POR INTENCION y desprotegido POR MECANISMO, que es la forma de defecto
# que llevan cerrando las tres ultimas ramas; a sabiendas seria peor que las anteriores.
PARTICIONES_RESERVADAS_FIDELIDAD = ("fidelidad-1", "fidelidad-2", "fidelidad-3")
RESERVADAS = PARTICIONES_RESERVADAS + PARTICIONES_RESERVADAS_FIDELIDAD
DIRECTORIO_HOLDOUT = "knowledge/cases/holdout"
DIRECTORIO_KIT = "knowledge/cases/kit"
DIRECTORIO_FIDELIDAD = "knowledge/cases/fidelidad"
# Subcarpeta de material reservado -> particion que la guarda. Explicita en vez de construida
# con f-strings: una particion nueva que no este aqui se ve en el diff. `DIRECTORIO_FIDELIDAD`
# NO tiene entrada: hoy sus carpetas solo llevan ASIGNACION -`ventanas.yaml`,
# `particiones.yaml`, `anclas.yaml`, `config.yaml`-, y leer asignacion no es abrir. El
# disparador para que la necesite esta escrito en la enmienda de ADR-0033 y en Technical Debt.
CARPETAS_RESERVADAS = {"1": "holdout-1", "2": "holdout-2", "3": "holdout-3"}
FICHERO_PREREGISTRO = "docs/validation/PREREGISTRO.md"
# El PREREGISTRO nacio vacio el 2026-09-12 con esta marca en su cabecera. Mientras siga, no se abre.
MARCA_SIN_RELLENAR = "SIN RELLENAR"
_CAMPOS_AUTORIZACION = (
    "particion",
    "autorizado_por",
    "fecha",
    "adr",
    "pregunta",
    "preregistro_blob",
)
# Las preguntas del pre-registro, una por linea, con su estado en la misma linea. Una sola
# fuente de verdad: una seccion aparte de `gastadas` se desincroniza y ademas invita a
# borrarla entera.
_PREGUNTA = re.compile(
    r"^-\s*pregunta:\s*(?P<id>[A-Za-z0-9][\w-]*)\s*\|\s*estado:\s*(?P<estado>\S+)",
    re.MULTILINE,
)
ABIERTA, GASTADA = "ABIERTA", "GASTADA"
_SHA = re.compile(r"^[0-9a-f]{40}$", re.ASCII)
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
_ADR = re.compile(r"^ADR-(\d{4})$", re.ASCII)


class HoldoutCerradoError(PermissionError):
    """Se intento abrir material de holdout sin lo que exige ADR-0021 §3."""


class RepartoIlegibleError(ValueError):
    """Un `particiones.yaml` que la puerta no puede leer.

    La puerta no puede responder a medias: si no puede leer la asignacion, NO SABE que hay que
    ocultar, y un mapa incompleto es indistinguible de uno completo. Hasta el 2026-09-21 esto
    era un `continue` en silencio, con un comentario que delegaba en `knowledge validate`; el
    comentario era FALSO para toda carpeta que el glob ve y el validador de su camino no
    reconoce -medido: un `BORRADOR_2026-09/` daba exit 0 en todas partes con sus reservados
    invisibles-. Ningun comando que deba sobrevivir a un paquete a medio escribir pasa por
    aqui: ni `kit build`, ni `kit check`, ni `knowledge validate`, ni un clon sin `data/`.
    """


def fichero_autorizacion(particion: str) -> str:
    return f"docs/validation/AUTORIZACION-{particion}.md"


def _commiteado_y_sin_cambios(repo: Path, ruta: str) -> str | None:
    """El texto del fichero si esta en HEAD y el arbol no lo ha cambiado; si no, None."""
    try:
        en_head = contenido_en_head(repo, ruta)
    except OSError:
        return None  # sin `git` en el PATH no hay forma de saber que esta commiteado: cerrado
    fichero = repo / ruta
    if en_head is None or not fichero.is_file():
        return None
    actual = fichero.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    return actual if actual == en_head.lstrip("\ufeff").replace("\r\n", "\n") else None


def preguntas_del_preregistro(texto: str) -> dict[str, str]:
    """`id -> estado` de las preguntas declaradas en el pre-registro.

    La forma es una linea por pregunta dentro de `## Preguntas`:

        - pregunta: P1 | estado: ABIERTA | de que va, en una frase

    Empieza por `- ` a proposito: el parser de la AUTORIZACION parte por el primer `:` de cada
    linea, asi que una linea que empezara por `pregunta:` en columna cero seria una clave si
    alguien reusara ese parser aqui.
    """
    return {m.group("id"): m.group("estado") for m in _PREGUNTA.finditer(texto)}


def motivos_de_cierre(repo: Path, particion: str) -> list[str]:
    """Por que `particion` NO se puede abrir hoy. Lista vacia: se puede."""
    if particion not in RESERVADAS:
        return [f"{particion!r} no es una particion reservada {RESERVADAS}"]
    motivos: list[str] = []
    preregistro = _commiteado_y_sin_cambios(repo, FICHERO_PREREGISTRO)
    if preregistro is None:
        motivos.append(f"{FICHERO_PREREGISTRO} no esta commiteado tal como esta en el arbol")
    elif MARCA_SIN_RELLENAR in preregistro:
        # Por subcadena en TODO el fichero, a proposito: falla del lado seguro. Quien lo rellene
        # tiene que quitar la marca tambien de cualquier comentario.
        motivos.append(
            f"{FICHERO_PREREGISTRO} sigue vacio (lleva la marca {MARCA_SIN_RELLENAR!r} en alguna "
            f"parte; al rellenarlo se quita de todo el fichero)"
        )
    ruta = fichero_autorizacion(particion)
    autorizacion = _commiteado_y_sin_cambios(repo, ruta)
    if autorizacion is None:
        motivos.append(f"no hay autorizacion del usuario commiteada en {ruta}")
        return motivos
    campos: dict[str, str] = {}
    repetidas: set[str] = set()
    for linea in autorizacion.splitlines():
        clave, sep, valor = linea.partition(":")
        if sep and clave.strip() in _CAMPOS_AUTORIZACION:
            if clave.strip() in campos:
                repetidas.add(clave.strip())
            campos[clave.strip()] = valor.strip()
    if repetidas:
        # Con una clave repetida, cual vale lo decidiria el orden de las lineas: una autorizacion
        # para holdout-2 con una segunda linea `particion: holdout-1` abria holdout-1 (auditoria de
        # cierre de la rama de la guarda). Se rechaza entera.
        motivos.append(
            f"{ruta}: claves repetidas {sorted(repetidas)}; una autorizacion no es ambigua"
        )
        return motivos
    faltan = [c for c in _CAMPOS_AUTORIZACION if not campos.get(c)]
    if faltan:
        motivos.append(f"{ruta}: faltan {faltan}")
        return motivos
    if campos["particion"] != particion:
        motivos.append(f"{ruta}: autoriza {campos['particion']!r}, no {particion!r}")
    if not _FECHA.match(campos["fecha"]):
        motivos.append(f"{ruta}: fecha {campos['fecha']!r} no es AAAA-MM-DD")
    adr = _ADR.match(campos["adr"])
    if adr is None or not list((repo / "docs" / "adr").glob(f"{adr.group(1)}-*.md")):
        motivos.append(f"{ruta}: adr {campos['adr']!r} no es un ADR que exista")
    aprobado = campos["preregistro_blob"]
    if not _SHA.match(aprobado):
        motivos.append(
            f"{ruta}: preregistro_blob {aprobado!r} no es un sha de blob (40 hex; lo da "
            f"`git rev-parse HEAD:{FICHERO_PREREGISTRO}`)"
        )
    else:
        try:
            vigente = blob_en_head(repo, FICHERO_PREREGISTRO)
        except OSError:
            vigente = None
        if vigente != aprobado:
            motivos.append(
                f"{ruta}: aprueba el {FICHERO_PREREGISTRO} con blob {aprobado[:12]}…, y el "
                f"commiteado es {vigente[:12] + '…' if vigente else 'ninguno'}: el pre-registro "
                f"cambio despues de autorizar, y hace falta una autorizacion nueva"
            )
    # La PREGUNTA que esta autorizacion abre (ADR-0033, enmienda del 2026-09-21). Sin esto, una
    # autorizacion es de un solo uso POR VERSION DEL PRE-REGISTRO y no por pregunta: si el
    # pre-registro lleva tres preguntas en el blob B1, una autorizacion anclada a B1 abre para las
    # tres y para una cuarta que nadie escribio. Se comprueba contra el `preregistro` que ya
    # tenemos en la mano: ni una llamada mas a git.
    if preregistro is not None:
        estado = preguntas_del_preregistro(preregistro).get(campos["pregunta"])
        if estado is None:
            motivos.append(
                f"{ruta}: cita la pregunta {campos['pregunta']!r} y el {FICHERO_PREREGISTRO} "
                f"commiteado no la tiene"
            )
        elif estado != ABIERTA:
            motivos.append(
                f"{ruta}: la pregunta {campos['pregunta']!r} ya se gasto (estado {estado}): una "
                f"autorizacion abre UNA pregunta, y esa ya esta contestada"
            )
    return motivos


def abrir(repo: Path, particion: str, pregunta: str) -> None:
    """Deja pasar o se niega. Todo acceso a material reservado llama aqui antes.

    `pregunta` es el ID de la pregunta pre-registrada que se esta abriendo, y es LOAD-BEARING: la
    autorizacion cita una, y si no coinciden la puerta se niega nombrando las dos. Hasta el
    2026-09-21 este parametro se llamaba `para_que`, era una frase y solo aparecia en el mensaje
    de error: cuando la puerta ABRIA -que es cuando importa- esa cadena no dejaba rastro en
    ningun sitio, porque `abrir` es pura y no escribe. Con el id, el acto de abrir DECLARA para
    que se abre, y esa declaracion se compara.

    Sigue siendo PURA: comprueba y vuelve. Quien gasta la pregunta es el COMANDO, y la gasta
    ANTES de leer (ADR-0033, enmienda del 2026-09-21).
    """
    motivos = motivos_de_cierre(repo, particion)
    if not motivos:
        ruta = fichero_autorizacion(particion)
        texto = _commiteado_y_sin_cambios(repo, ruta) or ""
        citada = next(
            (
                linea.partition(":")[2].strip()
                for linea in texto.splitlines()
                if linea.partition(":")[0].strip() == "pregunta"
            ),
            None,
        )
        if citada != pregunta:
            motivos = [f"{ruta}: autoriza la pregunta {citada!r} y se esta abriendo {pregunta!r}"]
    if motivos:
        raise HoldoutCerradoError(
            f"no se abre {particion} ({pregunta}): ADR-0021 §3 exige autorizacion del usuario y "
            f"PREREGISTRO.md commiteado y relleno ANTES de abrir. " + "; ".join(motivos)
        )


def gastar_pregunta(repo: Path, pregunta: str) -> Path:
    """Marca una pregunta como GASTADA en el pre-registro. LO LLAMA EL COMANDO, nunca `abrir`.

    Se gasta ANTES de leer, no despues, y los dos modos de fallo no son simetricos: "gastada y no
    leida" cuesta volver a pre-registrar; "leida y no gastada" es exactamente el defecto que esta
    enmienda cierra.

    Escribe y no commitea, como `kit anclar`. Y en cuanto escribe, la puerta YA esta cerrada
    aunque nadie haya commiteado: `_commiteado_y_sin_cambios` exige que el arbol coincida con HEAD.
    """
    ruta = repo / FICHERO_PREREGISTRO
    try:
        texto = ruta.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    except OSError as exc:
        raise HoldoutCerradoError(f"{FICHERO_PREREGISTRO}: {exc}") from exc
    estados = preguntas_del_preregistro(texto)
    if pregunta not in estados:
        raise HoldoutCerradoError(
            f"{FICHERO_PREREGISTRO} no declara la pregunta {pregunta!r}: "
            f"{sorted(estados) or 'ninguna'}"
        )
    if estados[pregunta] != ABIERTA:
        raise HoldoutCerradoError(
            f"la pregunta {pregunta!r} ya estaba {estados[pregunta]}: no se gasta dos veces"
        )
    lineas = texto.splitlines(keepends=True)
    for i, linea in enumerate(lineas):
        m = _PREGUNTA.match(linea)
        if m is not None and m.group("id") == pregunta:
            lineas[i] = linea.replace(f"estado: {ABIERTA}", f"estado: {GASTADA}", 1)
            break
    ruta.write_text("".join(lineas), encoding="utf-8", newline="\n")
    return ruta


def leer_fichero(repo: Path, ruta: str, pregunta: str = "") -> str:
    """El unico lector de `knowledge/cases/holdout/`. El README de cada particion es libre.

    DECIDE SOBRE LA RUTA RESUELTA, no sobre el texto que le pasan. Hasta el 2026-09-21 comparaba
    `Path(ruta).parts` sin resolver, y eso dejaba pasar esto -medido-:

        knowledge/cases/holdout/../holdout/2/caso-secreto.yaml  ->  LEE, sin llamar a `abrir`

    porque el `..` hacia que `resto[0]` no fuera `1|2|3`, mientras que `read_text` si resolvia el
    `..` y leia el fichero reservado. Tres puntos y una barra saltaban la puerta. No se arregla
    buscando `".."` por subcadena -eso es jugar al gato y al raton con la sintaxis-: se resuelve
    la ruta y se decide sobre lo resuelto.

    Y NIEGA POR DEFECTO dentro del directorio guardado: todo lo que no sea exactamente el
    `README.md` de una particion conocida pasa por `abrir`, incluidas las subcarpetas que no
    existen -una `4/` que aparezca manana cae del lado seguro- y los ficheros sueltos en la raiz.
    """
    raiz = repo.resolve()
    destino = (repo / ruta).resolve()
    base = (raiz / DIRECTORIO_HOLDOUT).resolve()
    try:
        resto = destino.relative_to(base).parts
    except ValueError:
        raise ValueError(f"{ruta} no esta en {DIRECTORIO_HOLDOUT}") from None
    if resto[1:] != ("README.md",) or resto[0] not in CARPETAS_RESERVADAS:
        abrir(repo, CARPETAS_RESERVADAS.get(resto[0], RESERVADAS[0]), pregunta)
    return destino.read_text(encoding="utf-8")


def repartos_commiteables(repo: Path) -> list[Path]:
    """Todos los `particiones.yaml` que existen, de los dos caminos, en orden estable.

    Los dos, y por eso esta funcion existe en vez de un glob suelto: un camino que se anada y no
    se agregue aqui deja sus dias reservados invisibles para la puerta, que es un exit 0 que no
    comprueba nada. `tests/unit/test_puerta_holdout.py` lo vigila comparando la union.
    """
    ficheros: list[Path] = []
    for directorio in (DIRECTORIO_KIT, DIRECTORIO_FIDELIDAD):
        base = repo / directorio
        if base.is_dir():
            ficheros += sorted(base.glob("*/particiones.yaml"))
    return ficheros


def casos_reservados(repo: Path) -> dict[str, str]:
    """`caso -> particion` de todos los casos asignados a una particion reservada, en todos los
    repartos commiteados de los DOS caminos. Leer la ASIGNACION no es abrir: es lo que dice que
    no se puede leer."""
    salida: dict[str, str] = {}
    for fichero in repartos_commiteables(repo):
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError) as exc:
            raise RepartoIlegibleError(
                f"{fichero.relative_to(repo).as_posix()}: {exc}. La puerta no sabe que casos "
                f"reservados hay en este reparto, asi que no puede decir que ocultar"
            ) from exc
        asignacion = doc.get("asignacion") if isinstance(doc, dict) else None
        if not isinstance(asignacion, dict):
            continue
        for caso, particion in asignacion.items():
            if particion in RESERVADAS:
                salida[str(caso)] = str(particion)
    return salida
