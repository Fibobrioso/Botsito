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

**Y NO SE DIO POR HECHO: MAYO LO ROMPIO** (2026-09-22, `trabajo/mayo-dev-ingerido`). El libro de
mayo viene entero en `AAAA-MM-DD HH:MM:SS`, no en el formato de agosto. Medido por velas sobre sus
filas `dev`, con control en agosto y abril: UTC. Desde entonces el formato y el huso NO los fija
este modulo: los DECLARA cada libro, atados a su sha, en `knowledge/corpus/libros.yaml`
(`corpus.libros`, ADR-0039), y aqui se acepta exactamente lo declarado. Formatos por libro, medidos:
agosto y abril `AAAA/MM/DD HH:MM:SS` UTC; mayo `AAAA-MM-DD HH:MM:SS` UTC.
"""

from __future__ import annotations

import hashlib
import io
import zipfile
from collections.abc import Iterable, Sequence
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree
from zoneinfo import ZoneInfo

from botsito.corpus.libros import Declaracion

# La pestana de operaciones del export de FX Replay. Vive AQUI y no en la ingesta: es
# conocimiento de como esta hecho el libro, y el contrato de importacion exige que solo este
# modulo lo nombre.
PESTANA_OPERACIONES = "backtesting-analytics"
_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


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


def _instante(texto: str, declaracion: Declaracion) -> datetime | None:
    """El instante UTC con la PRIMERA lectura declarada que case; None si ninguna. Los formatos
    del vocabulario son disjuntos, asi que como mucho casa uno."""
    for lectura in declaracion.lecturas:
        try:
            ingenuo = datetime.strptime(texto, lectura.patron)
        except ValueError:
            continue
        return ingenuo.replace(tzinfo=ZoneInfo(lectura.huso)).astimezone(UTC)
    return None


def filas_de_los_dias(
    ruta: Path,
    dias: Iterable[str],
    pestana: str,
    cabeceras: Sequence[str],
    declaracion: Declaracion,
    *,
    huso_de_los_dias: str,
) -> list[dict[str, str | None]]:
    """Las filas del libro cuyo dia -EN `huso_de_los_dias`- esta en `dias`. Nada mas.

    `pestana` y `cabeceras` son lo ESPERADO, escrito antes de abrir: si no cuadran, el error
    nombra lo que falta de esa lista y NUNCA lo que se ha encontrado.

    `dias` son dias ISO ya filtrados por quien llama: este modulo no sabe cuales estan reservados.

    **EL DIA SE CALCULA EN EL HUSO DE LOS DIAS PEDIDOS, no en el del fichero** (2026-09-22, rama
    `trabajo/mayo-dev-ingerido`). Hasta hoy se comparaba la fecha UTC con dias que son de
    `huso_operativa`, y una fila de las 22:00-24:00 UTC de un dia pedido -que en Madrid es el dia
    SIGUIENTE, y puede estar reservado- entraba como pedida: su instante, su entrada y su stop
    podian salir en un mensaje de error. Y al reves, la madrugada de un dia pedido se perdia. Es
    la regla de `CLAUDE.md` -fijar el huso de las dos fuentes antes de compararlas- con el libro y
    el reparto como las dos fuentes. Por eso `huso_de_los_dias` es obligatorio y no tiene default:
    uno en UTC reproduciria el defecto en silencio. Cada fila devuelta lleva `_dia` en ese huso.

    **Y SOLO CON LA DECLARACION DEL LIBRO** (ADR-0039): los bytes tienen que dar el sha declarado,
    y cada fecha se parsea con las lecturas `{formato, huso}` declaradas y con ninguna otra. Una
    fecha que no casa con ninguna es error: nunca se prueba otro formato hasta que uno parsee.
    """
    pedidos = set(dias)
    if not pedidos:
        return []
    try:
        contenido = ruta.read_bytes()
    except OSError as exc:
        raise LibroError(f"{ruta.name}: {exc}") from exc
    if hashlib.sha256(contenido).hexdigest() != declaracion.sha256:
        raise LibroError(
            f"{ruta.name}: sus bytes no son los del libro declarado {declaracion.sha256[:12]}...: "
            f"no se lee con una declaracion ajena (ADR-0039)"
        )
    try:
        with zipfile.ZipFile(io.BytesIO(contenido)) as libro:
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
    except ElementTree.ParseError:
        # SIN el texto del parser: trae «line X, column Y», y esa columna es una POSICION dentro
        # de la hoja entera, que crece con las filas de antes -reservadas incluidas- (medido el
        # 2026-09-22: «column 4913»). `from None` para que tampoco salga encadenada.
        raise LibroError(
            f"{ruta.name}: XML mal formado dentro del libro. No se da la posicion: contaria el "
            f"contenido de antes, reservado incluido"
        ) from None
    except (OSError, zipfile.BadZipFile) as exc:
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
    for fila in filas[1:]:
        celdas = _fila_como_dict(fila)
        crudo = celdas.get(donde[cabeceras[0]])
        if not crudo:
            continue
        instante = _instante(str(crudo), declaracion)
        if instante is None:
            # SIN su numero de fila ni su valor: la posicion en el libro cuenta TODAS las filas de
            # antes, reservadas incluidas (ADR-0037), y de una fila sin fecha legible no se sabe de
            # que dia es: puede ser reservada.
            raise LibroError(
                f"{ruta.name}/{pestana}: una fila tiene {cabeceras[0]} que no casa con ningun "
                f"formato declarado para este libro. No se da ni su valor ni su posicion"
            )
        dia = instante.astimezone(ZoneInfo(huso_de_los_dias)).date().isoformat()
        if dia not in pedidos:
            continue  # NO se cuenta, NO se acumula: el conjunto de dias del libro no sale de aqui
        # `_orden` es la posicion ENTRE LAS FILAS PEDIDAS, no en el libro: el numero de fila del
        # libro contaria las de los dias no pedidos que van delante (2026-09-22, MAYO-DEV).
        fila_util: dict[str, str | None] = {
            "_orden": str(len(salida) + 1),
            "_instante_utc": instante.isoformat(),
            "_dia": dia,
        }
        for c in cabeceras:
            fila_util[c] = celdas.get(donde[c])
        salida.append(fila_util)
    return salida
