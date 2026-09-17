"""La guarda del holdout en los tests (F14 D4, extraida a la rama de la guarda; ADR-0033).

Un hook de auditoria de Python (`sys.addaudithook`) mira CADA apertura de fichero del proceso de
pytest, venga de donde venga: `open`, `Path.read_text`, `os.open`, `io.FileIO`, numpy, y las
copias de `shutil`, que en Windows no emiten `open` sino `_winapi.CopyFile2` o `shutil.copyfile`.
Si la ruta cae dentro de `knowledge/cases/holdout/{1,2,3}/` y no es el `README.md` de la
carpeta, lanza `LecturaDeHoldout`.

Tres decisiones que valen mas que el codigo:

1. **Cualquier llamante, no solo `spec` y `domain`.** La promesa del stub hablaba de esos dos
   paquetes, y la revision de diseno midio sobre la suite entera que ninguna lectura tiene a
   `botsito.spec` ni a `botsito.domain` en la pila: `domain` no hace E/S y quien abre fisicamente
   es casi siempre `comun.yaml_estricto`. Los que leeran el holdout son `cases`, el motor, la
   validacion y la CLI.
2. **`BaseException`, no `Exception`.** `cases/paquete.py` y la CLI convierten `OSError` en errores
   del kit; una guarda que se pudiera tragar con `except Exception` se apagaria en silencio. Y
   aunque un test la tragara con `except BaseException`, la fixture falla igual al terminar,
   porque anota cada violacion antes de lanzar.
3. **El hook no se puede quitar** (no existe `sys.removeaudithook`). Se instala una vez por
   proceso y consulta un estado que la fixture enciende y apaga en cada test.

Listar nombres (`os.listdir`, `os.scandir`) NO cuenta: no es abrir (ADR-0021 §1). Copiar SI cuenta:
una copia lee el contenido.

Lo que esto NO ve, y queda declarado en ADR-0033: lo que lee un subproceso (`git show`, la CLI en
otro proceso), y las etiquetas del holdout que NO viven en esta carpeta -los `LABEL_CASE` de dias
reservados, en `knowledge/feedback/`, y el detalle por operacion del backtest-. Eso lo cubre la
puerta de `botsito.cases.holdout`, no esta guarda.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

CARPETAS_RESERVADAS = frozenset({"1", "2", "3"})
PERMITIDOS = frozenset({"README.md"})
# Los eventos que abren contenido. `os.listdir` y `os.scandir` se ignoran a proposito.
EVENTOS = frozenset({"open", "shutil.copyfile", "_winapi.CopyFile2"})


class LecturaDeHoldout(BaseException):  # noqa: N818 - el nombre dice lo que paso, no "Error"
    """Un test ha abierto material reservado. BaseException para que nadie la trague."""


class Estado:
    raiz: Path | None = None
    violaciones: list[str] = []  # noqa: RUF012 - estado de proceso, a proposito


def _normal(ruta: str) -> str:
    return os.path.normcase(os.path.abspath(ruta))


def violacion(evento: str, args: tuple[Any, ...], raiz: Path | None) -> str | None:
    """La violacion que supone este evento, o None. Pura: se prueba sin instalar el hook."""
    if raiz is None or evento not in EVENTOS or not args:
        return None
    try:
        ruta = os.fsdecode(args[0])
    except TypeError:
        return None  # un descriptor entero: ya se abrio antes, y entonces se vio
    base = _normal(str(raiz))
    candidata = _normal(ruta)
    if candidata != base and not candidata.startswith(base + os.sep):
        return None
    partes = Path(os.path.relpath(candidata, base)).parts
    if not partes or partes[0] not in CARPETAS_RESERVADAS:
        return None  # el README de holdout/ y la propia carpeta
    # `normcase` baja a minusculas en Windows: se compara igual de normalizado
    if len(partes) == 2 and partes[1] in {os.path.normcase(x) for x in PERMITIDOS}:
        return None
    return f"{evento}: {Path(*partes).as_posix()}"


def _hook(evento: str, args: tuple[Any, ...]) -> None:
    v = violacion(evento, args, Estado.raiz)
    if v is not None:
        Estado.violaciones.append(v)
        raise LecturaDeHoldout(
            f"{v}: un test ha abierto material de holdout (ADR-0021 §1, ADR-0033). Abrir un "
            f"holdout exige autorizacion del usuario y PREREGISTRO.md (ADR-0021 §3)"
        )


_INSTALADO = False


def instalar() -> None:
    """Una vez por proceso: el hook no se puede quitar."""
    global _INSTALADO
    if not _INSTALADO:
        sys.addaudithook(_hook)
        _INSTALADO = True


def esta_instalado() -> bool:
    return _INSTALADO
