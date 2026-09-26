"""El modo DIAGNOSTICO de A-35 y A-44: correr el motor con un valor HIPOTETICO y etiquetado para
lo que el trader todavia no ha respondido, sin que esa salida pueda contar para nada.

La regla (rama `trabajo/preparar-a35-a44`, 2026-09-26): el selector de A-35
(`liquidez_m15_pivote_formado`) y el tope propio del trader de A-44 viven en el registro como
UNKNOWN hasta que el trader responda. Sin fijar NO es un valor valido: el motor se niega a correr
y lo dice nombrando la ambiguedad. La UNICA excepcion es pedir el modo diagnostico a proposito, con
la lectura o el tope hipoteticos por nombre; entonces corre, y cada linea de cada salida y el
nombre de cada fichero llevan la etiqueta `DIAGNOSTICO-A35-<lectura>` o `DIAGNOSTICO-A44-<modo>`,
para que nada de eso pueda alimentar una medida de fidelidad ni un conjunto de medicion. Con el
parametro ya fijado, pedir el diagnostico se rechaza: la corrida cuenta y no lleva etiqueta.

Es una regla del proyecto, no del trader: la lectura la elige el trader, no el ajuste.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from botsito.config.registro import ParametroDesconocidoError, Registro
from botsito.domain.pivotes_m15 import LECTURAS

PARAMETRO_A35 = "liquidez_m15_pivote_formado"
ETIQUETA_A35 = "DIAGNOSTICO-A35"
ETIQUETA_A44 = "DIAGNOSTICO-A44"
# Los modos hipoteticos de A-44: sin tope (el trader dice que no tiene) o un MARCADOR que no es un
# valor plausible del trader (un tope de un punto porcentual de nada: se toca con cualquier
# perdida; vale para ver el embudo, no para simular una operativa).
A44_SIN_TOPE = "sin_tope"
A44_MARCADOR = "marcador"
# El marcador CERO: un tope de cero, que se alcanza con cualquier perdida, incluida ninguna. Solo
# sirve para demostrar de punta a punta que RN-020 bloquea cuando el tope se alcanza; no es un
# valor plausible de nadie y no se registra en ningun sitio.
A44_MARCADOR_CERO = "marcador_cero"
MODOS_A44 = (A44_SIN_TOPE, A44_MARCADOR, A44_MARCADOR_CERO)


class SinFijarError(ValueError):
    """Una ambiguedad bloqueante sin responder: el motor se niega a correr y dice cual."""


class DiagnosticoRechazadoError(ValueError):
    """Se pidio el diagnostico de algo que ya esta fijado: la corrida cuenta y no lleva etiqueta."""


@dataclass(frozen=True)
class Diagnostico:
    """Lo que se pidio correr en hipotesis: la lectura de A-35 y el modo de A-44, o nada."""

    a35: str | None = None
    a44: str | None = None

    def __post_init__(self) -> None:
        if self.a35 is not None and self.a35 not in LECTURAS:
            raise ValueError(f"lectura de A-35 {self.a35!r} no esta en {LECTURAS}")
        if self.a44 is not None and self.a44 not in MODOS_A44:
            raise ValueError(f"modo de A-44 {self.a44!r} no esta en {MODOS_A44}")

    @property
    def etiquetas(self) -> tuple[str, ...]:
        salida: list[str] = []
        if self.a35 is not None:
            salida.append(f"{ETIQUETA_A35}-{self.a35}")
        if self.a44 is not None:
            salida.append(f"{ETIQUETA_A44}-{self.a44}")
        return tuple(salida)

    @property
    def activo(self) -> bool:
        return bool(self.etiquetas)


NINGUNO = Diagnostico()


def lectura_pivote(registro: Registro, diagnostico: Diagnostico = NINGUNO) -> str:
    """La lectura de «formado» con la que corre el motor: la del registro si el trader la fijo;
    si no, la del diagnostico pedido; y sin ninguna de las dos, la negativa que nombra A-35."""
    try:
        fijada = registro.opcion(PARAMETRO_A35)
    except ParametroDesconocidoError:
        fijada = None
    if fijada is not None:
        if diagnostico.a35 is not None:
            raise DiagnosticoRechazadoError(
                f"{PARAMETRO_A35} ya esta fijado en {fijada!r} (A-35 respondida): la corrida "
                "cuenta y no admite --diagnostico-a35"
            )
        return fijada
    if diagnostico.a35 is not None:
        return diagnostico.a35
    raise SinFijarError(
        f"A-35 sin fijar: `{PARAMETRO_A35}` es UNKNOWN en knowledge/spec/parametros.yaml y la "
        "spec no define cuando un pivote de M15 esta formado; el motor se niega a correr. La "
        "responde el trader (docs/runbooks/ACTIVAR-A35-A44.md). Para ver el embudo en hipotesis, "
        f"--diagnostico-a35 <{'|'.join(LECTURAS)}>: corre ETIQUETADO y sin valor para ninguna "
        "medida"
    )


def etiquetar(texto: str, etiquetas: tuple[str, ...]) -> str:
    """Cada linea de una salida de texto empieza por sus etiquetas. Sin etiquetas, el texto tal
    cual. Determinista."""
    if not etiquetas:
        return texto
    prefijo = "".join(f"[{e}]" for e in etiquetas) + " "
    lineas = texto.split("\n")
    cola = ""
    if lineas and lineas[-1] == "":
        lineas = lineas[:-1]
        cola = "\n"
    return "\n".join(prefijo + ln for ln in lineas) + cola


def etiquetar_html(html: str, etiquetas: tuple[str, ...]) -> str:
    """Una pagina lleva la etiqueta en el titulo y en un aviso al principio del cuerpo."""
    if not etiquetas:
        return html
    marca = " ".join(etiquetas)
    salida = html.replace("<title>", f"<title>[{marca}] ", 1)
    aviso = (
        f'<p class="aviso diagnostico"><strong>{marca}</strong>: corrida en hipotesis, sin valor '
        "para ninguna medida</p>"
    )
    return salida.replace("<body>", f"<body>{aviso}", 1)


def nombre_etiquetado(ruta: Path, etiquetas: tuple[str, ...]) -> Path:
    """`informe.txt` -> `informe.DIAGNOSTICO-A35-inicio_vela_contraria.txt`. Un fichero de
    diagnostico nunca puede llevar el nombre de una linea base."""
    if not etiquetas:
        return ruta
    return ruta.with_name(f"{ruta.stem}.{'.'.join(etiquetas)}{ruta.suffix}")


__all__ = [
    "A44_MARCADOR",
    "A44_MARCADOR_CERO",
    "A44_SIN_TOPE",
    "ETIQUETA_A35",
    "ETIQUETA_A44",
    "MODOS_A44",
    "NINGUNO",
    "PARAMETRO_A35",
    "Diagnostico",
    "DiagnosticoRechazadoError",
    "SinFijarError",
    "etiquetar",
    "etiquetar_html",
    "lectura_pivote",
    "nombre_etiquetado",
]
