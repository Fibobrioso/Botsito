"""EL UNICO modulo que abre un libro de backtest del trader (ADR-0037).

Un contrato de importacion lo vigila: ningun otro modulo de `src/` puede nombrar un `.xlsx` ni
importar `zipfile` para leerlo. Es el mismo patron que `corpus.motor_whisper` con `faster-whisper`
y que `cases.holdout` con la carpeta del holdout: si la lectura vive en un solo sitio, se sabe
donde mirar.

**LO QUE ESTE MODULO NO HACE, Y ES SU RAZON DE SER:**

1. **No enumera.** No devuelve, no imprime y no registra la lista de pestanas, ni la de cabeceras,
   ni la de FECHAS que hay en el libro. Recibe lo que espera y lo VERIFICA; recibe los dias que
   quiere y devuelve sus filas. Un `"14 dias en el libro"` publicaria que dias reservados NO opero
   el trader, y un dia laborable sin ninguna operacion ES su etiqueta -por eso `2026-05-14` quedo
   quemado el 2026-09-12-.
2. **No lee agregados.** Selecciona la pestana por la lista pre-declarada; no recorre las demas.
   Un agregado sobre un rango que incluya dias reservados no se abre NUNCA, y ninguna autorizacion
   lo abre, porque no se puede trocear por dia (ADR-0037 §1 y §3).
3. **No decide que dias puede leer.** Eso lo hace quien llama, contra `casos_reservados`. Este
   modulo es el lector; la puerta esta antes.

**EL FORMATO, medido sobre `backtesting-analytics AGOSTO 2026.xlsx` el 2026-09-21** (material de
desarrollo, cero dias reservados, declarado en `HOLDOUT-EXPOSICIONES.md`):

- Sin `xl/sharedStrings.xml`: el texto va `inlineStr`, celda a celda.
- Una sola pestana, `backtesting-analytics`, y ningun agregado dentro del libro.
- Las fechas son TEXTO, no serial de Excel: `2026/08/03 06:03:05`, y vienen en **UTC** -convertidas
  a `huso_operativa` las 47 operaciones caen dentro de las dos sesiones H4 declaradas; leidas como
  hora local, 16 quedarian fuera-.

Nada de eso se da por hecho para el mes siguiente: la estructura se VERIFICA contra la lista
escrita antes, asi que un cambio de serializacion sale como fallo limpio y no como dato mal leido.
"""

from __future__ import annotations

import zipfile
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree

# La pestana de operaciones del export de FX Replay. Vive AQUI y no en la ingesta: es
# conocimiento de como esta hecho el libro, y el contrato de importacion exige que solo este
# modulo lo nombre.
PESTANA_OPERACIONES = "backtesting-analytics"
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
# El formato de `dateStart`/`dateEnd` tal como lo escribe el exportador de FX Replay.
_FORMATO = "%Y/%m/%d %H:%M:%S"


class LibroError(ValueError):
    """El libro no tiene la forma declarada. Nombra SOLO lo esperado que falta."""


def _texto(celda: ElementTree.Element) -> str | None:
    if celda.get("t") == "inlineStr":
        return "".join(t.text or "" for t in celda.iter(f"{_NS}t"))
    v = celda.find(f"{_NS}v")
    return v.text if v is not None else None


def _columna(referencia: str) -> str:
    return "".join(c for c in referencia if c.isalpha())


def _fila_como_dict(fila: ElementTree.Element) -> dict[str, str | None]:
    return {_columna(c.get("r") or ""): _texto(c) for c in fila.iter(f"{_NS}c")}


def filas_de_los_dias(
    ruta: Path,
    dias: Iterable[str],
    pestana: str,
    cabeceras: Sequence[str],
    huso_del_fichero: str = "UTC",
) -> list[dict[str, str | None]]:
    """Las filas del libro cuyo dia -en `huso_del_fichero`- esta en `dias`. Nada mas.

    `pestana` y `cabeceras` son lo ESPERADO, escrito antes de abrir: si no cuadran, el error
    nombra lo que falta de esa lista y NUNCA lo que se ha encontrado.

    `dias` son dias ISO ya filtrados por quien llama: este modulo no sabe cuales estan reservados.
    El dia de una fila se calcula del instante en `huso_del_fichero`, sin convertir de huso: la
    conversion a `huso_operativa` la hace la ingesta, que es quien sabe de sesiones H4.
    """
    pedidos = set(dias)
    if not pedidos:
        return []
    try:
        with zipfile.ZipFile(ruta) as libro:
            miembros = set(libro.namelist())
            if "xl/workbook.xml" not in miembros:
                raise LibroError(f"{ruta.name}: no es un libro xlsx (falta xl/workbook.xml)")
            cuaderno = ElementTree.fromstring(libro.read("xl/workbook.xml"))
            # SELECCION, no enumeracion: se busca la esperada y no se listan las demas.
            indice = next(
                (
                    i
                    for i, hoja in enumerate(cuaderno.iter(f"{_NS}sheet"), start=1)
                    if hoja.get("name") == pestana
                ),
                None,
            )
            if indice is None:
                raise LibroError(
                    f"{ruta.name}: no tiene la pestana esperada {pestana!r} (no se nombran las "
                    f"que si tiene: enumerarlas seria leer estructura, ADR-0037 §5)"
                )
            destino = f"xl/worksheets/sheet{indice}.xml"
            if destino not in miembros:
                raise LibroError(f"{ruta.name}: falta {destino}")
            hoja = ElementTree.fromstring(libro.read(destino))
    except (OSError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        raise LibroError(f"{ruta.name}: {exc}") from exc

    filas = list(hoja.iter(f"{_NS}row"))
    if not filas:
        raise LibroError(f"{ruta.name}/{pestana}: sin filas")
    cabecera = _fila_como_dict(filas[0])
    donde = {nombre: letra for letra, nombre in cabecera.items() if nombre}
    faltan = [c for c in cabeceras if c not in donde]
    if faltan:
        # SOLO las esperadas que faltan. El conjunto encontrado no sale de aqui.
        raise LibroError(f"{ruta.name}/{pestana}: faltan las columnas {faltan}")

    salida: list[dict[str, str | None]] = []
    for n, fila in enumerate(filas[1:], start=2):
        celdas = _fila_como_dict(fila)
        crudo = celdas.get(donde[cabeceras[0]])
        if not crudo:
            continue
        try:
            instante = datetime.strptime(str(crudo), _FORMATO)
        except ValueError as exc:
            raise LibroError(f"{ruta.name}/{pestana}: fila {n}: {cabeceras[0]} ilegible") from exc
        instante = instante.replace(tzinfo=UTC if huso_del_fichero == "UTC" else None)
        if instante.date().isoformat() not in pedidos:
            continue  # NO se cuenta, NO se acumula: el conjunto de dias del libro no sale de aqui
        fila_util: dict[str, str | None] = {
            "_fila": str(n),
            "_instante_utc": instante.isoformat(),
        }
        for c in cabeceras:
            fila_util[c] = celdas.get(donde[c])
        salida.append(fila_util)
    return salida
