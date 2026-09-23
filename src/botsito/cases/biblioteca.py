"""Los casos de `knowledge/cases/dev/` (F14a, ADR-0037): escritura y validacion.

Un caso es un DIA. Su id ya existe y es global -`ventanas.id_caso` da `caso-<simbolo>-<dia>`-, asi
que esto no inventa identidad: le pone CUERPO a un caso que hasta hoy solo tenia esqueleto en el
reparto.

**LO QUE EL CASO LLEVA, Y LO QUE NO.**

Lleva las operaciones del dia, cada una con cuatro cosas: instante de apertura, sesion H4,
direccion, entrada y stop. **No lleva objetivo**, y no es que lo lleve vacio: el objetivo del
trader es una REGLA -`objetivo_rr`, 1:3, `ev-v2-001658-d02fb71a`- y el xlsx no registra el
planeado. Un campo opcional vacio seria una invitacion a rellenarlo con `maxTP`, que es un
resultado (ADR-0037 §7 y su correccion).

**Y NO LLEVA DECISION POR SESION.** Convertir "no hay operacion en la sesion 11-15" en
`no_trade` es una INFERENCIA NUESTRA, no un dato del trader, y ADR-0016 exige que una inferencia
declare el ADR que la decide. Esa decision no esta tomada (F14 D1), asi que aqui NO se toma: el
caso guarda lo que el material dice -las operaciones- y la derivacion a decision por sesion es de
F14b, que es quien construye la biblioteca. Escribir hoy un `no_trade` derivado seria exactamente
"llamar lo que hizo el trader a algo que dedujimos nosotros".

**LA FORMA ES UNA LISTA CERRADA EN LOS TRES NIVELES** (2026-09-22, rama
`trabajo/mayo-dev-ingerido`). Hasta hoy `como_documento` escribia una clave `objetivo` con un
texto que decia «NO ES UN CAMPO», y la guardia no cerraba el primer nivel: el campo que ADR-0037 §7
dice que no existe EXISTIA, y nada impedia cambiar ese texto por un precio. Un comentario no es el
mecanismo; la lista cerrada si, porque caza tambien lo que nadie penso. Cada clave, por lo que la
forma NECESITA:

- caso: `id` (la identidad, global, la del reparto: sin ella la guardia de reservados no puede
  cruzar nada), `dia` y `simbolo` (lo que el id codifica, explicito para quien lo lea; la guardia
  exige que casen con el id, asi que no pueden derivar), `operaciones` (lo que el trader HIZO, que
  es el contenido) y `fuente` (de que libro sale y cuando: `knowledge/cases/` es versionado y cada
  valor cita su origen).
- operacion: `instante_utc` (el momento de la decision, en el huso del fichero), `sesion` (la
  unidad de fidelidad; depende de `huso_operativa`, que es un parametro, asi que se fija al
  ingerir y no se recalcula en silencio), `direccion`, `entrada` y `stop` (la decision completa:
  una fila sin stop no produce caso). NADA de resultado: ni cierre, ni PnL, ni RR.
- fuente: `tipo`, `fichero`, `sha256` (identifica el libro exacto; es el que declara el mes en
  `cobertura_material`) e `ingerido_el`.

**PRECIOS BAJO `knowledge/cases/`.** Es la primera vez, y por eso la guardia de ADR-0037 §9: ningun
fichero de aqui puede corresponder a un caso reservado, comprobado por `problemas_de_biblioteca` y
por un test de contrato, no por convenio.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from botsito.cases.holdout import casos_ocultos
from botsito.cases.ingesta import DIRECTORIO_DEV, Operacion
from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, leer_yaml

FUENTE_OBJETIVO = "ev-v2-001658-d02fb71a"
CLAVES_CASO = frozenset({"id", "dia", "simbolo", "operaciones", "fuente"})
CLAVES_OPERACION = frozenset({"instante_utc", "sesion", "direccion", "entrada", "stop"})
CLAVES_FUENTE = frozenset({"tipo", "fichero", "sha256", "ingerido_el"})


class BibliotecaError(ValueError):
    """Un caso de `knowledge/cases/dev/` que no tiene la forma declarada."""


def _dump(doc: Any) -> str:
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=True, width=100)


def como_documento(
    caso: str, dia: str, simbolo: str, operaciones: list[Operacion], fuente: dict[str, str]
) -> dict[str, Any]:
    # SIN `objetivo`: lo fija la regla `objetivo_rr` con su `base_calculo_objetivo`
    # (FUENTE_OBJETIVO) y el material no registra el planeado (ADR-0037 §7). Hasta el 2026-09-22
    # aqui se escribia una clave `objetivo` con esa explicacion: un comentario hecho campo.
    return {
        "id": caso,
        "dia": dia,
        "simbolo": simbolo,
        "operaciones": [
            {
                "instante_utc": o.instante_utc,
                "sesion": o.sesion,
                "direccion": o.direccion,
                "entrada": str(o.entrada),
                "stop": str(o.stop),
            }
            for o in operaciones
        ],
        "fuente": dict(fuente),
    }


def escribir(repo: Path, documentos: list[dict[str, Any]]) -> list[Path]:
    carpeta = repo / DIRECTORIO_DEV
    carpeta.mkdir(parents=True, exist_ok=True)
    escritos: list[Path] = []
    for doc in documentos:
        ruta = carpeta / f"{doc['id']}.yaml"
        ruta.write_text(_dump(doc), encoding="utf-8", newline="\n")
        escritos.append(ruta)
    return escritos


def problemas_de_biblioteca(repo: Path) -> list[str]:
    """Para `knowledge validate`: forma del caso y, sobre todo, que NINGUNO este reservado."""
    carpeta = repo / DIRECTORIO_DEV
    if not carpeta.is_dir():
        return []
    problemas: list[str] = []
    # OCULTOS (ADR-0041): un retirado tampoco puede tener caso en `dev`. Lanza si un reparto es
    # ilegible: falla cerrado.
    reservados = casos_ocultos(repo)
    for ruta in sorted(carpeta.glob("caso-*.yaml")):
        nombre = ruta.name
        try:
            doc = leer_yaml(ruta)
        except (OSError, YamlError) as exc:
            problemas.append(f"{nombre}: {exc}")
            continue
        if not isinstance(doc, dict):
            problemas.append(f"{nombre}: se espera un mapa")
            continue
        caso = str(doc.get("id"))
        if ruta.stem != caso or not ids.es_id_de("caso", caso):
            problemas.append(f"{nombre}: el nombre del fichero y el `id` no son el mismo caso")
            continue
        if set(doc) != CLAVES_CASO:
            problemas.append(
                f"{nombre}: claves {sorted(CLAVES_CASO)}, exactamente; sobran "
                f"{sorted(set(doc) - CLAVES_CASO)} y faltan {sorted(CLAVES_CASO - set(doc))}. "
                f"Un caso no lleva objetivo ni resultado (ADR-0037 §7)"
            )
        if not caso.endswith(f"-{doc.get('dia')}") or caso != (
            f"caso-{str(doc.get('simbolo')).lower()}-{doc.get('dia')}"
        ):
            problemas.append(f"{nombre}: `dia` y `simbolo` no casan con el id {caso}")
        fuente = doc.get("fuente")
        if not isinstance(fuente, dict) or set(fuente) != CLAVES_FUENTE:
            problemas.append(f"{nombre}: `fuente` con {sorted(CLAVES_FUENTE)}, exactamente")
        # LA GUARDIA DE ADR-0037 §9: aqui hay PRECIOS, asi que un caso reservado no puede estar.
        if caso in reservados:
            problemas.append(
                f"{nombre}: {caso} esta asignado a {reservados[caso]}, que es una particion "
                f"RESERVADA. Un fichero con precios de un dia reservado bajo "
                f"{DIRECTORIO_DEV}/ es material abierto sin puerta (ADR-0037 §9)"
            )
        ops = doc.get("operaciones")
        if not isinstance(ops, list):
            problemas.append(f"{nombre}: `operaciones` debe ser una lista")
            continue
        for i, op in enumerate(ops, start=1):
            if not isinstance(op, dict) or set(op) != CLAVES_OPERACION:
                problemas.append(
                    f"{nombre}: operacion {i}: claves instante_utc, sesion, "
                    f"direccion, entrada y stop, exactamente"
                )
                continue
            if op["direccion"] not in ("compra", "venta"):
                problemas.append(f"{nombre}: operacion {i}: direccion {op['direccion']!r}")
        if "maxTP" in _dump(doc) or "idealTP" in _dump(doc):
            problemas.append(
                f"{nombre}: nombra una columna de objetivo del material. El objetivo no es un "
                f"campo del caso (ADR-0037 §7)"
            )
    return problemas
