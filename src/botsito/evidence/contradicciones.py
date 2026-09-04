"""Contradicciones (F06): dos items activos con el mismo tema y valores distintos.

No se escriben a mano. `_contradicciones.yaml` se regenera desde los items y el validador falla si
el fichero versionado no coincide con la regeneracion. Una contradiccion se cierra cuando un
registro de feedback (F09) supersede a uno de los items, no editandolos.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from itertools import groupby
from pathlib import Path
from typing import Any

import yaml

from botsito.evidence.modelo import FICHERO_CONTRADICCIONES, EvidenceItem, activos

_NUMERO = re.compile(r"^(-?\d+(?:[.,]\d+)?)\s*(%?)$")


def normalizar_valor(valor: str) -> str:
    """'0,75', '0.75' y '0.750' son el mismo valor; '75 %' y '75%' tambien.

    El resto se compara en minusculas y sin espacios sobrantes.
    """
    v = " ".join(valor.split()).lower()
    m = _NUMERO.match(v)
    if not m:
        return v
    try:
        numero = Decimal(m.group(1).replace(",", ".")).normalize()
    except InvalidOperation:
        return v
    texto = format(numero, "f")
    return f"{texto}%" if m.group(2) else texto


CABECERA = (
    "# GENERADO por `botsito evidence contradictions`. No editar a mano.\n"
    "# Se cierra una contradiccion con un registro de feedback que supersede a un item (F09).\n"
)


def detectar(items: list[EvidenceItem]) -> list[dict[str, Any]]:
    con_valor = sorted((i for i in activos(items) if i.valor is not None), key=lambda i: i.tema)
    salida: list[dict[str, Any]] = []
    for tema, grupo in groupby(con_valor, key=lambda i: i.tema):
        lista = sorted(grupo, key=lambda i: i.id)
        valores = sorted({normalizar_valor(i.valor) for i in lista if i.valor is not None})
        if len(valores) < 2:
            continue
        salida.append(
            {
                "tema": tema,
                "estado": "ABIERTA",
                "valores": valores,
                "items": [
                    {"id": i.id, "valor": i.valor, "video_id": i.video_id, "t0": i.t0}
                    for i in lista
                ],
            }
        )
    return salida


def texto(items: list[EvidenceItem]) -> str:
    cuerpo = yaml.safe_dump(
        {"contradicciones": detectar(items)}, allow_unicode=True, sort_keys=True, width=100
    )
    return CABECERA + cuerpo


def escribir(directorio: Path, items: list[EvidenceItem]) -> Path:
    ruta = directorio / FICHERO_CONTRADICCIONES
    ruta.write_text(texto(items), encoding="utf-8", newline="\n")
    return ruta


def validar_fichero(directorio: Path, items: list[EvidenceItem]) -> list[str]:
    ruta = directorio / FICHERO_CONTRADICCIONES
    if not ruta.exists():
        return [f"falta {FICHERO_CONTRADICCIONES}: ejecuta `botsito evidence contradictions`"]
    actual = ruta.read_text(encoding="utf-8").replace("\r\n", "\n")
    if actual != texto(items):
        return [f"{FICHERO_CONTRADICCIONES} no coincide con la regeneracion desde los items"]
    return []
