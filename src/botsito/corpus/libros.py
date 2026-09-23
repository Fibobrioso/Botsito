"""El registro de LIBROS: como se lee cada backtest del trader, atado a su sha (ADR-0039).

**NINGUN LIBRO SE LEE SIN SU FORMATO Y SU HUSO DECLARADOS, atados a su sha y a la medida que los
sostiene.** Nacio el 2026-09-22 en `trabajo/mayo-dev-ingerido`: el lector daba por hecho el
formato de fecha de agosto (`AAAA/MM/DD HH:MM:SS`, UTC) para todos los libros, y el de mayo viene
entero en `AAAA-MM-DD HH:MM:SS`. Aceptar un formato nuevo sin fijar antes su huso es el error del
huso de esos dos dias metido en el codigo, y «probar formatos hasta que uno parsee» es exactamente
eso. Asi que cada libro declara su lista CERRADA de lecturas `{formato, huso}` y el lector acepta
esas y ninguna otra.

**SOLO ANADIR.** El sha fija los bytes, asi que el formato y el huso de un libro no pueden cambiar
nunca: una entrada commiteada no se edita ni se borra. `problemas_de_libros` lo comprueba contra el
historial, version a version del fichero, y contra el arbol de trabajo. Si una declaracion resulta
estar mal, el libro NO se lee hasta que se decida por ADR que hacer; no se corrige encima.

**EL PROCEDIMIENTO PARA DECLARAR UN LIBRO NUEVO** (ADR-0039): el huso se mide por velas -la entrada
dentro de [minima - 2, maxima + 2] puntos de la M1 del minuto- con UTC y con el huso alternativo,
y con un CONTROL sobre un libro de huso ya conocido. Decide si un huso da >= 90 % y el otro
<= 50 %; si no, NO CONCLUYENTE y el libro no se declara.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from botsito.comun import historial
from botsito.comun.yaml_estricto import YamlError, cargar_yaml, leer_yaml

FICHERO_LIBROS = "knowledge/corpus/libros.yaml"
# EL VOCABULARIO CERRADO de formatos: nombre legible -> patron de `strptime`. Un formato nuevo
# entra aqui solo con su medida (ADR-0039), nunca porque un libro no parsee.
FORMATOS = {
    "AAAA/MM/DD HH:MM:SS": "%Y/%m/%d %H:%M:%S",
    "AAAA-MM-DD HH:MM:SS": "%Y-%m-%d %H:%M:%S",
}
CLAVES_ENTRADA = frozenset({"fichero", "lecturas", "medida", "declarado_el", "fuente"})
_SHA256 = re.compile(r"^[0-9a-f]{64}$", re.ASCII)
_DIA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)


class LibrosError(ValueError):
    """El registro no tiene la forma declarada, o un libro no esta en el."""


@dataclass(frozen=True)
class Lectura:
    formato: str
    huso: str

    @property
    def patron(self) -> str:
        return FORMATOS[self.formato]


@dataclass(frozen=True)
class Declaracion:
    sha256: str
    lecturas: tuple[Lectura, ...]


def sha256_de(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def _entradas(doc: Any, nombre: str) -> dict[str, dict[str, Any]]:
    if not isinstance(doc, dict) or set(doc) != {"libros"} or not isinstance(doc["libros"], dict):
        raise LibrosError(f"{nombre}: un mapa con la clave `libros` y nada mas")
    return {str(k): v for k, v in doc["libros"].items()}


def _declaracion(sha: str, entrada: Any, nombre: str) -> Declaracion:
    if not _SHA256.match(sha):
        raise LibrosError(f"{nombre}: {sha[:16]}... no es un sha256 en hexadecimal minuscula")
    if not isinstance(entrada, dict) or set(entrada) != CLAVES_ENTRADA:
        raise LibrosError(f"{nombre}: {sha[:12]}...: claves {sorted(CLAVES_ENTRADA)}, exactamente")
    if not _DIA.match(str(entrada["declarado_el"])):
        raise LibrosError(f"{nombre}: {sha[:12]}...: declarado_el no es AAAA-MM-DD")
    if not str(entrada["medida"]).strip() or not entrada["fuente"]:
        raise LibrosError(
            f"{nombre}: {sha[:12]}...: una declaracion sin la medida que la sostiene y sin su "
            f"fuente no vale (ADR-0039)"
        )
    lecturas: list[Lectura] = []
    for lec in entrada["lecturas"] if isinstance(entrada["lecturas"], list) else []:
        if not isinstance(lec, dict) or set(lec) != {"formato", "huso"}:
            raise LibrosError(f"{nombre}: {sha[:12]}...: cada lectura es {{formato, huso}}")
        if lec["formato"] not in FORMATOS:
            raise LibrosError(
                f"{nombre}: {sha[:12]}...: formato {lec['formato']!r} fuera del vocabulario "
                f"{sorted(FORMATOS)}"
            )
        try:
            ZoneInfo(str(lec["huso"]))
        except (ZoneInfoNotFoundError, ValueError) as exc:
            raise LibrosError(f"{nombre}: {sha[:12]}...: huso {lec['huso']!r}") from exc
        lecturas.append(Lectura(str(lec["formato"]), str(lec["huso"])))
    if not lecturas or len({le.formato for le in lecturas}) != len(lecturas):
        raise LibrosError(f"{nombre}: {sha[:12]}...: lecturas vacias o con formatos repetidos")
    return Declaracion(sha, tuple(lecturas))


def cargar_libros(repo: Path) -> dict[str, Declaracion]:
    ruta = repo / FICHERO_LIBROS
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise LibrosError(f"{FICHERO_LIBROS}: {exc}") from exc
    return {
        sha: _declaracion(sha, e, FICHERO_LIBROS)
        for sha, e in _entradas(doc, FICHERO_LIBROS).items()
    }


def declaracion_de(repo: Path, ruta: Path) -> Declaracion:
    """La declaracion del libro por el sha de SUS BYTES. Sin ella, no se lee."""
    sha = sha256_de(ruta)
    libros = cargar_libros(repo)
    if sha not in libros:
        raise LibrosError(
            f"el libro {sha[:12]}... no esta declarado en {FICHERO_LIBROS}: sin su formato y su "
            f"huso medidos no se lee (ADR-0039)"
        )
    return libros[sha]


def _version(texto: str | None, donde: str) -> dict[str, Any]:
    if texto is None:
        return {}
    try:
        return _entradas(cargar_yaml(texto), f"{FICHERO_LIBROS}@{donde}")
    except YamlError as exc:
        raise LibrosError(f"{FICHERO_LIBROS}@{donde}: {exc}") from exc


def problemas_de_libros(repo: Path, shas_de_cobertura: set[str]) -> list[str]:
    """Para `knowledge validate`: forma, SOLO ANADIR contra el historial y el cruce con
    `cobertura_material`."""
    try:
        libros = cargar_libros(repo)
    except LibrosError as exc:
        return [str(exc)]
    problemas: list[str] = []
    # EL CRUCE: dos registros con la misma llave y nada que los compare es como empieza una
    # deriva. Todo libro que declara su MES tiene que declarar tambien como se LEE.
    for sha in sorted(shas_de_cobertura - set(libros)):
        problemas.append(
            f"cobertura_material declara el material {sha[:12]}... y {FICHERO_LIBROS} no: un libro "
            f"con mes y sin formato ni huso no se puede leer (ADR-0039)"
        )
    # SOLO ANADIR: cada version del fichero contiene, identicas, todas las entradas de la anterior.
    if historial.historial_evaluable(repo) is not None:
        return problemas
    pares = historial.versiones_del_fichero(repo, FICHERO_LIBROS)
    if pares is None:
        return problemas
    actual = (repo / FICHERO_LIBROS).read_text(encoding="utf-8")
    pares = [*pares, ("arbol de trabajo", "HEAD")]
    for hijo, padre in pares:
        texto_hijo = (
            actual
            if hijo == "arbol de trabajo"
            else historial.contenido_en(repo, hijo, FICHERO_LIBROS)
        )
        try:
            antes = _version(historial.contenido_en(repo, padre, FICHERO_LIBROS), padre[:7])
            despues = _version(texto_hijo, hijo[:7])
        except LibrosError as exc:
            problemas.append(str(exc))
            continue
        for sha, entrada in antes.items():
            if sha not in despues:
                problemas.append(f"{hijo[:16]}: borra la declaracion del libro {sha[:12]}...")
            elif despues[sha] != entrada:
                problemas.append(
                    f"{hijo[:16]}: modifica la declaracion del libro {sha[:12]}.... El registro es "
                    f"SOLO ANADIR: el sha fija los bytes y su formato y su huso no cambian"
                )
    return problemas
