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
`PREREGISTRO.md` tiene que estar commiteado y RELLENO.
"""

from __future__ import annotations

import re
from pathlib import Path

from botsito.comun.historial import contenido_en_head
from botsito.comun.yaml_estricto import YamlError, leer_yaml

PARTICIONES_RESERVADAS = ("holdout-1", "holdout-2", "holdout-3")
DIRECTORIO_HOLDOUT = "knowledge/cases/holdout"
DIRECTORIO_KIT = "knowledge/cases/kit"
FICHERO_PREREGISTRO = "docs/validation/PREREGISTRO.md"
# El PREREGISTRO nacio vacio el 2026-09-12 con esta marca en su cabecera. Mientras siga, no se abre.
MARCA_SIN_RELLENAR = "SIN RELLENAR"
_CAMPOS_AUTORIZACION = ("particion", "autorizado_por", "fecha", "adr")
_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)
_ADR = re.compile(r"^ADR-(\d{4})$", re.ASCII)


class HoldoutCerradoError(PermissionError):
    """Se intento abrir material de holdout sin lo que exige ADR-0021 §3."""


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


def motivos_de_cierre(repo: Path, particion: str) -> list[str]:
    """Por que `particion` NO se puede abrir hoy. Lista vacia: se puede."""
    if particion not in PARTICIONES_RESERVADAS:
        return [f"{particion!r} no es una particion reservada {PARTICIONES_RESERVADAS}"]
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
    return motivos


def abrir(repo: Path, particion: str, para_que: str) -> None:
    """Deja pasar o se niega. Todo acceso a material reservado llama aqui antes."""
    motivos = motivos_de_cierre(repo, particion)
    if motivos:
        raise HoldoutCerradoError(
            f"no se abre {particion} ({para_que}): ADR-0021 §3 exige autorizacion del usuario y "
            f"PREREGISTRO.md commiteado y relleno ANTES de abrir. " + "; ".join(motivos)
        )


def leer_fichero(repo: Path, ruta: str) -> str:
    """El unico lector de `knowledge/cases/holdout/`. El README de cada particion es libre."""
    partes = Path(ruta).parts
    base = Path(DIRECTORIO_HOLDOUT).parts
    if partes[: len(base)] != base:
        raise ValueError(f"{ruta} no esta en {DIRECTORIO_HOLDOUT}")
    resto = partes[len(base) :]
    if len(resto) >= 2 and resto[0] in {"1", "2", "3"} and resto[1:] != ("README.md",):
        abrir(repo, f"holdout-{resto[0]}", f"leer {ruta}")
    return (repo / ruta).read_text(encoding="utf-8")


def casos_reservados(repo: Path) -> dict[str, str]:
    """`caso -> particion` de todos los casos asignados a una particion reservada, en todos los
    paquetes del kit. Leer la ASIGNACION no es abrir: es lo que dice que no se puede leer."""
    salida: dict[str, str] = {}
    kit = repo / DIRECTORIO_KIT
    if not kit.is_dir():
        return salida
    for fichero in sorted(kit.glob("*/particiones.yaml")):
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError):
            continue  # el esquema del paquete lo denuncia `knowledge validate`, no esta puerta
        asignacion = doc.get("asignacion") if isinstance(doc, dict) else None
        if not isinstance(asignacion, dict):
            continue
        for caso, particion in asignacion.items():
            if particion in PARTICIONES_RESERVADAS:
                salida[str(caso)] = str(particion)
    return salida
