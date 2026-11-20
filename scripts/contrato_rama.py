"""El contrato de una rama de trabajo: lo que puede tocar, lo que no, y el informe que debe dejar.

Rama `trabajo/guardias-claude` (2026-10-01; formato y ejemplos en
`docs/runbooks/CONTRATO-DE-RAMA.md`). Si en la raiz hay un `contrato.yaml`, `make check` compara
contra el merge-base con `main` todo lo que la rama cambia -lo commiteado y lo ESTADIADO, que es
lo que se va a sellar- y falla nombrando:

- cada fichero que no case con ninguna de `rutas_permitidas`;
- cada fichero que case con alguna de `rutas_protegidas` (mandan sobre las permitidas);
- el `artefacto` (el informe de `docs/validation/`) si no esta estadiado;
- el `tramo` (la entrada de `docs/plan/HOJA-DE-RUTA.md` a la que pertenece la rama) si falta o no
  es un tramo de la hoja. Es obligatorio solo si la hoja de ruta existe en el merge-base con `main`
  (`trabajo/hoja-de-ruta`, 2026-10-10): rige desde la rama siguiente a la que la trajo, sin tocar
  ningun contrato anterior.

Y, aparte del contrato, G2 (`trabajo/guardias-holdout`, 2026-11-19; GUARDIAS-HOLDOUT.md): en una
rama `trabajo/*`, `docs/validation/HOLDOUT-EXPOSICIONES.md` TAL COMO ESTA ESTADIADO tiene que
tener una fila de su tabla con la fecha de hoy (reloj local) en la primera columna y que nombre la
rama; si no, no se sella. En `main`, en `fix/` (la CI) y en `feature/` no actua.

`contrato.yaml` se permite siempre a si mismo. Sin contrato no hay nada que comprobar. En `main`
no se exige: el contrato sale de la rama ANTES del merge (RITUAL.md), y si una rama hereda el de
otra, su campo `rama` no casa con la rama actual y falla.

Las `comprobaciones` (comandos obligatorios) NO las ejecuta `make check`: podrian escribir en el
repositorio mientras corre (CLAUDE.md, «nada escribe mientras corre make check») y alargarlo. Las
ejecuta el revisor (`.claude/agents/revisor.md`) y su salida va al informe.

Patrones: `*` no cruza `/`, `**` si, y un patron que acaba en `/` es todo lo que cuelga de esa
carpeta. Las rutas se comparan tal como las da git, con `/`.

Uso (lo llama `make check`):
    uv run python scripts/contrato_rama.py
"""

from __future__ import annotations

import datetime as dt
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RAIZ = Path(__file__).resolve().parents[1]
# `make check` lo lanza dentro de `pico_memoria medir`, donde `python` puede no ser el del entorno
# del proyecto (medido el 2026-10-01: `No module named 'botsito'`); lo mismo que huso_por_velas.py.
sys.path.insert(0, str(RAIZ / "src"))

from botsito.comun.yaml_estricto import YamlError, leer_yaml  # noqa: E402

FICHERO = "contrato.yaml"
CLAVES = {
    "rama",
    "riesgo",
    "artefacto",
    "tramo",
    "rutas_permitidas",
    "rutas_protegidas",
    "comprobaciones",
}
# Las que pueden faltar: `rutas_protegidas` siempre; `tramo`, mientras la hoja de ruta no este en el
# merge-base (lo decide `problemas_de_tramo`, no la carga).
OPCIONALES = {"rutas_protegidas", "tramo"}
HOJA_DE_RUTA = "docs/plan/HOJA-DE-RUTA.md"
RIESGOS = ("bajo", "medio", "alto")


class ContratoError(Exception):
    """Un contrato mal escrito: no se puede comprobar nada con el."""


@dataclass(frozen=True)
class Contrato:
    rama: str
    riesgo: str
    artefacto: str
    rutas_permitidas: tuple[str, ...]
    rutas_protegidas: tuple[str, ...]
    comprobaciones: tuple[str, ...]
    tramo: str | None = None


def _lista(doc: dict[str, Any], clave: str, vacia: bool) -> tuple[str, ...]:
    valor = doc.get(clave)
    if valor is None and vacia:
        return ()
    if not isinstance(valor, list) or not all(isinstance(x, str) and x.strip() for x in valor):
        raise ContratoError(f"{FICHERO}: `{clave}` es una lista de textos no vacios")
    if not valor and not vacia:
        raise ContratoError(f"{FICHERO}: `{clave}` no puede estar vacia")
    return tuple(x.strip() for x in valor)


def cargar(ruta: Path) -> Contrato:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise ContratoError(f"{FICHERO}: {exc}") from exc
    if not isinstance(doc, dict):
        raise ContratoError(f"{FICHERO}: tiene que ser un mapa")
    sobran, faltan = set(doc) - CLAVES, CLAVES - set(doc) - OPCIONALES
    if sobran or faltan:
        raise ContratoError(
            f"{FICHERO}: claves {sorted(CLAVES)}; sobran {sorted(sobran)}, faltan {sorted(faltan)}"
        )
    rama, riesgo, artefacto = doc["rama"], doc["riesgo"], doc["artefacto"]
    if not isinstance(rama, str) or "/" not in rama:
        raise ContratoError(f"{FICHERO}: `rama` es el nombre de la rama, p. ej. trabajo/<nombre>")
    if riesgo not in RIESGOS:
        raise ContratoError(f"{FICHERO}: `riesgo` es uno de {', '.join(RIESGOS)}")
    if not isinstance(artefacto, str) or not re.fullmatch(r"docs/validation/[^/]+\.md", artefacto):
        raise ContratoError(f"{FICHERO}: `artefacto` es el informe, docs/validation/<NOMBRE>.md")
    tramo = doc.get("tramo")
    if tramo is not None and (not isinstance(tramo, str) or not tramo.strip()):
        raise ContratoError(f"{FICHERO}: `tramo` es el titulo de un tramo de {HOJA_DE_RUTA}")
    return Contrato(
        rama=rama,
        riesgo=riesgo,
        artefacto=artefacto,
        rutas_permitidas=_lista(doc, "rutas_permitidas", vacia=False),
        rutas_protegidas=_lista(doc, "rutas_protegidas", vacia=True),
        comprobaciones=_lista(doc, "comprobaciones", vacia=False),
        tramo=tramo.strip() if isinstance(tramo, str) else None,
    )


def tramos_de_la_hoja(texto: str) -> set[str]:
    """Los tramos de la hoja de ruta: cada `## ` por su titulo entero y por su id (lo que va antes
    de « · »): `R1` y `R1 · Activar la sesion 4`, o `Carril: lo de Aleks`."""
    salida: set[str] = set()
    for linea in texto.splitlines():
        if linea.startswith("## "):
            titulo = linea[3:].strip()
            salida |= {titulo, titulo.split(" · ", 1)[0].strip()}
    return salida


def problemas_de_tramo(tramo: str | None, hoja_en_la_base: bool, hoja: str | None) -> list[str]:
    """Niega por defecto: sin hoja en la base el tramo no se exige, pero si se da, existe."""
    if tramo is None:
        if hoja_en_la_base:
            return [
                f"falta `tramo` en {FICHERO}: la entrada de {HOJA_DE_RUTA} a la que pertenece esta "
                "rama (obligatorio desde que la hoja de ruta esta en main)"
            ]
        return []
    if hoja is None:
        return [f"`tramo` {tramo!r} nombra {HOJA_DE_RUTA}, que no existe en esta rama"]
    if tramo not in tramos_de_la_hoja(hoja):
        return [f"`tramo` {tramo!r} no es un tramo (`## `) de {HOJA_DE_RUTA}"]
    return []


def patron_a_regex(patron: str) -> re.Pattern[str]:
    if patron.endswith("/"):
        patron += "**"
    partes: list[str] = []
    i = 0
    while i < len(patron):
        if patron.startswith("**/", i):
            partes.append("(?:.*/)?")
            i += 3
        elif patron.startswith("**", i):
            partes.append(".*")
            i += 2
        elif patron[i] == "*":
            partes.append("[^/]*")
            i += 1
        elif patron[i] == "?":
            partes.append("[^/]")
            i += 1
        else:
            partes.append(re.escape(patron[i]))
            i += 1
    return re.compile("".join(partes))


def casa(ruta: str, patrones: tuple[str, ...]) -> str | None:
    """El primer patron que casa con `ruta`, o None."""
    return next((p for p in patrones if patron_a_regex(p).fullmatch(ruta)), None)


def _git(raiz: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=raiz,
        capture_output=True,
        encoding="utf-8",
        check=False,
    )


def rama_actual(raiz: Path) -> str:
    return _git(raiz, "symbolic-ref", "--short", "-q", "HEAD").stdout.strip()


def base_de_comparacion(raiz: Path) -> str:
    for ref in ("main", "origin/main"):
        r = _git(raiz, "merge-base", ref, "HEAD")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
    raise ContratoError("no hay `main` ni `origin/main` contra los que comparar la rama")


def ficheros_cambiados(raiz: Path, base: str) -> list[str]:
    """Lo commiteado en la rama y lo estadiado, contra el merge-base: el arbol que se sella."""
    r = _git(raiz, "diff", "--cached", "--name-only", "--no-renames", "-z", base)
    if r.returncode != 0:
        raise ContratoError(f"git diff contra {base[:7]} fallo: {r.stderr.strip()}")
    return sorted(x for x in r.stdout.split("\0") if x)


def esta_estadiado(raiz: Path, ruta: str) -> bool:
    return _git(raiz, "cat-file", "-e", f":{ruta}").returncode == 0


def _sin_prefijo(rama: str) -> str:
    """`trabajo/x` y `feature/x` son la misma rama: el cierre puede cambiarle el prefijo."""
    return rama.split("/", 1)[-1]


def comprobar(raiz: Path) -> tuple[list[str], str]:
    """(problemas, resumen). Sin problemas, la rama cumple su contrato."""
    ruta = raiz / FICHERO
    if not ruta.is_file():
        return [], f"sin {FICHERO}: nada que comprobar"
    rama = rama_actual(raiz)
    if rama == "main":
        return [], f"en main el contrato no se exige ({FICHERO} sale de la rama antes del merge)"
    try:
        contrato = cargar(ruta)
    except ContratoError as exc:
        return [str(exc)], ""
    problemas: list[str] = []
    if rama and _sin_prefijo(rama) != _sin_prefijo(contrato.rama):
        problemas.append(
            f"{FICHERO} es de la rama {contrato.rama!r} y esta es {rama!r}: un contrato heredado "
            "no vale; escribe el de esta rama"
        )
    if not casa(contrato.artefacto, contrato.rutas_permitidas):
        problemas.append(f"el artefacto {contrato.artefacto} no esta en rutas_permitidas")
    try:
        base = base_de_comparacion(raiz)
        cambiados = ficheros_cambiados(raiz, base)
    except ContratoError as exc:
        return [*problemas, str(exc)], ""
    hoja_en_la_base = _git(raiz, "cat-file", "-e", f"{base}:{HOJA_DE_RUTA}").returncode == 0
    ruta_hoja = raiz / HOJA_DE_RUTA
    hoja = ruta_hoja.read_text(encoding="utf-8") if ruta_hoja.is_file() else None
    problemas += problemas_de_tramo(contrato.tramo, hoja_en_la_base, hoja)
    for f in cambiados:
        if f == FICHERO:
            continue
        protegido = casa(f, contrato.rutas_protegidas)
        if protegido:
            problemas.append(f"{f}: dentro de rutas_protegidas ({protegido})")
        elif not casa(f, contrato.rutas_permitidas):
            problemas.append(f"{f}: fuera de rutas_permitidas")
    if not esta_estadiado(raiz, contrato.artefacto):
        problemas.append(f"falta el artefacto {contrato.artefacto} (no esta estadiado)")
    resumen = (
        f"{len(cambiados)} ficheros dentro del contrato de {contrato.rama} "
        f"(riesgo {contrato.riesgo}, artefacto {contrato.artefacto}, "
        f"{'tramo ' + repr(contrato.tramo) + ', ' if contrato.tramo else ''}"
        f"{len(contrato.comprobaciones)} comprobaciones para el revisor)"
    )
    return problemas, resumen


# ----------------------------------------------------------------------------------------- G2
# La fila de HOLDOUT-EXPOSICIONES del dia (rama `trabajo/guardias-holdout`, 2026-11-19;
# docs/validation/GUARDIAS-HOLDOUT.md, G2; Technical Debt de PROJECT_STATE desde
# trabajo/cuenta-por-mes). Cada `make check` lee el M1 de marzo y calienta con el de junio
# (RESPALDO-M1.md), y ADR-0021 §4 pide declarar toda exposicion el mismo dia; la fila se escribio
# tarde a mano varias veces (ERRORES-RECURRENTES.md). Actua SOLO en una rama local `trabajo/*`, por
# un `startswith` explicito y no por `_sin_prefijo`: en `main`, en `fix/` y `feature/` (las de la
# CI) y con HEAD separado, no. Lee UN fichero, del indice de git (lo que se sella), y no recorre
# directorios. Va aparte de `comprobar` (la llama `main`): los tests del contrato corren en una
# rama `trabajo/prueba` sin fila.
EXPOSICIONES = "docs/validation/HOLDOUT-EXPOSICIONES.md"
PREFIJO_G2 = "trabajo/"


def _hoy() -> dt.date:
    """El dia del reloj LOCAL de la maquina (en la laptop de Aleks, Lima): limite declarado."""
    return dt.date.today()


def filas_de_exposiciones(texto: str) -> list[str]:
    """Las filas de la tabla de exposiciones: la primera tabla cuya cabecera empieza por
    `| Fecha |`, hasta su primera linea que no es de tabla. No tiene que estar al final."""
    filas: list[str] = []
    dentro = False
    for linea in texto.splitlines():
        if not dentro:
            dentro = re.match(r"\|\s*Fecha\s*\|", linea) is not None
        elif not linea.startswith("|"):
            break
        elif not set(linea.strip()) <= set("|-: "):
            filas.append(linea)
    return filas


def problemas_fila_del_dia(rama: str, hoy: dt.date, texto: str | None) -> list[str]:
    """G2. `texto` es HOLDOUT-EXPOSICIONES.md como esta estadiado (None si no lo esta). Pasa si
    alguna fila de la tabla tiene `hoy` (AAAA-MM-DD) como primera columna y nombra la rama entera
    (no otra que empiece igual). Fuera de `trabajo/*`, no actua."""
    if not rama.startswith(PREFIJO_G2):
        return []
    dia = hoy.isoformat()
    nombra = re.compile(rf"(?<![\w/.-]){re.escape(rama)}(?![\w/-])")
    for fila in filas_de_exposiciones(texto or ""):
        if fila.split("|")[1].strip() == dia and nombra.search(fila):
            return []
    return [
        f"G2: falta la fila de HOLDOUT-EXPOSICIONES del {dia} para {rama}; escríbela y estadíala "
        "antes de este make check (ADR-0021 §4)"
    ]


def texto_estadiado(raiz: Path, ruta: str) -> str | None:
    """El fichero tal como esta en el indice (`git show :ruta`), o None si no esta."""
    r = _git(raiz, "show", f":{ruta}")
    return r.stdout if r.returncode == 0 else None


def fila_del_dia(raiz: Path, hoy: dt.date) -> list[str]:
    rama = rama_actual(raiz)
    if not rama.startswith(PREFIJO_G2):
        return []
    return problemas_fila_del_dia(rama, hoy, texto_estadiado(raiz, EXPOSICIONES))


def main() -> int:
    problemas, resumen = comprobar(RAIZ)
    if problemas:
        print(f"CONTRATO: la rama no cumple {FICHERO}:", file=sys.stderr)
        for p in problemas:
            print(f"  - {p}", file=sys.stderr)
    else:
        print(f"CONTRATO: {resumen}")
    hoy, rama = _hoy(), rama_actual(RAIZ)
    g2 = fila_del_dia(RAIZ, hoy)
    for p in g2:
        print(p, file=sys.stderr)
    if not g2 and rama.startswith(PREFIJO_G2):
        print(f"G2: fila de HOLDOUT-EXPOSICIONES del {hoy.isoformat()} para {rama}, estadiada")
    return 1 if problemas or g2 else 0


if __name__ == "__main__":
    sys.exit(main())
