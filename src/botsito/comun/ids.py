"""Formatos de identificador del proyecto, en un solo sitio (ASCII estricto).

Quien define un objeto define su id aqui; las capas que lo citan importan el patron en vez de
copiarlo. Los formatos de `regla` (`RN-NNN`, F11), `ambiguedad` (`A-N`) y `caso` (`caso-…`, F14)
estan reservados aqui aunque el objeto llegue mas tarde.
"""

from __future__ import annotations

import re

EVIDENCIA = re.compile(r"^ev-[a-z0-9]+-\d{6}-[0-9a-f]{8}$", re.ASCII)
FEEDBACK = re.compile(r"^fb-[0-9a-z-]+-[0-9a-f]{8}$", re.ASCII)
ADR = re.compile(r"^ADR-\d{4}$", re.ASCII)
REGLA = re.compile(r"^RN-\d{3}$", re.ASCII)
AMBIGUEDAD = re.compile(r"^A-\d+$", re.ASCII)
CASO = re.compile(r"^caso-[a-z0-9][a-z0-9-]*$", re.ASCII)
PARAMETRO = re.compile(r"^[a-z][a-z0-9_]*$", re.ASCII)
TEMA = re.compile(r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$", re.ASCII)
DATASET = re.compile(r"^[a-z0-9][a-z0-9-]{1,47}-[0-9a-f]{8}$", re.ASCII)
TRANSCRIPCION = re.compile(r"^tr-[a-z0-9]+-[a-z0-9][a-z0-9._-]{0,39}-[0-9a-f]{8}$", re.ASCII)
FOTOGRAMAS = re.compile(r"^fr-[a-z0-9]+-[0-9a-f]{8}$", re.ASCII)
# Referencia citable a un fotograma: `<fotogramas_id>/<t_ms nominal>` (F05; la usa F07).
REFERENCIA_FOTOGRAMA = re.compile(r"^fr-[a-z0-9]+-[0-9a-f]{8}/\d+$", re.ASCII)
FUENTE = re.compile(
    r"^(ev-[a-z0-9]+-\d{6}-[0-9a-f]{8}|fb-[0-9a-z-]+-[0-9a-f]{8}|ADR-\d{4})$", re.ASCII
)

POR_TIPO: dict[str, re.Pattern[str]] = {
    "evidence": EVIDENCIA,
    "feedback": FEEDBACK,
    "decision": ADR,
    "regla": REGLA,
    "ambiguedad": AMBIGUEDAD,
    "caso": CASO,
    "parametro": PARAMETRO,
    "contradiccion": TEMA,
    "dataset": DATASET,
    "transcripcion": TRANSCRIPCION,
    "fotogramas": FOTOGRAMAS,
    "referencia_fotograma": REFERENCIA_FOTOGRAMA,
}


def es_id_de(tipo: str, texto: object) -> bool:
    patron = POR_TIPO.get(tipo)
    return patron is not None and isinstance(texto, str) and patron.match(texto) is not None
