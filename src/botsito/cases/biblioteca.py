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

**PRECIOS BAJO `knowledge/cases/`.** Es la primera vez, y por eso la guardia de ADR-0037 §9: ningun
fichero de aqui puede corresponder a un caso reservado, comprobado por `problemas_de_biblioteca` y
por un test de contrato, no por convenio.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from botsito.cases.holdout import casos_reservados
from botsito.cases.ingesta import DIRECTORIO_DEV, Operacion
from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, leer_yaml

FUENTE_OBJETIVO = "ev-v2-001658-d02fb71a"


class BibliotecaError(ValueError):
    """Un caso de `knowledge/cases/dev/` que no tiene la forma declarada."""


def _dump(doc: Any) -> str:
    return yaml.safe_dump(doc, allow_unicode=True, sort_keys=True, width=100)


def como_documento(
    caso: str, dia: str, simbolo: str, operaciones: list[Operacion], fuente: dict[str, str]
) -> dict[str, Any]:
    return {
        "id": caso,
        "dia": dia,
        "simbolo": simbolo,
        # El objetivo NO es un campo: es `objetivo_rr` (1:3) con su `base_calculo_objetivo`, y el
        # material no registra el planeado. Se deja dicho DENTRO del fichero para que nadie tenga
        # que ir a buscarlo, y para que quede claro que la ausencia es de diseno.
        "objetivo": (
            f"NO ES UN CAMPO: lo fija la regla `objetivo_rr` con `base_calculo_objetivo`, cuyo "
            f"valor vive en el registro de parametros; el material no registra el objetivo "
            f"planeado ({FUENTE_OBJETIVO}, ADR-0037 §7)"
        ),
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
    reservados = casos_reservados(repo)  # lanza si un reparto es ilegible: falla cerrado
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
            if not isinstance(op, dict) or set(op) != {
                "instante_utc",
                "sesion",
                "direccion",
                "entrada",
                "stop",
            }:
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
