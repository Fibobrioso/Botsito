"""Transcribe una sesion con el trader y aplica una CUARENTENA MECANICA antes de que nadie lea el
texto. Rama `trabajo/sesion-02`, para la sesion 02 (y las que vengan).

TODO lo que produce va FUERA del repositorio, en la carpeta del audio (por defecto
`C:\\Users\\USER\\Desktop\\reunion-a35-a44\\sesion-02-audio\\`); el script se niega a escribir
dentro del repo. Por cada audio `<nombre>.<ext>`:

    <nombre>.cruda-NO-LEER.jsonl   segmentos del ASR con marcas de tiempo (sin filtrar: NO se lee)
    <nombre>.cruda-NO-LEER.txt     la misma cruda en texto, con [h:mm:ss] (NO se lee)
    <nombre>.filtrada.md           la version FILTRADA, agrupada por pregunta: lo UNICO que se lee
    <nombre>.registro.txt          tiempos, motor, recuentos y codigos; ningun texto del trader
    <nombre>-trabajo/              WAV, fragmentos y parciales (reanudable)

EL ASR ES EL DEL CORPUS (F04, ADR-0007), sin cambiar nada: faster-whisper `large-v3`
`int8_float16` en CUDA, `beam_size=5`, `temperature=0`, `vad_filter`, sin
`condition_on_previous_text`, con el vocabulario de `knowledge/corpus/glosario_asr.yaml` como
`initial_prompt`, el mismo corte por silencios (`corpus/audio.py`) y la misma fusion de fragmentos
(`corpus/transcripcion.py`). Asi se transcribio la sesion 01 (v6). No descarga modelos: corre con
`HF_HUB_OFFLINE=1` y usa el que ya esta en la cache local.

LA CUARENTENA (se aplica a la cruda ANTES de escribir la version filtrada; ninguna persona ni
ningun modelo lee la cruda). Un segmento va a `[CUARENTENA mm:ss–mm:ss]` SIN contenido si:
- nombra un mes que no se puede DEMOSTRAR libre (desde `trabajo/cuarentena-por-condicion`: sin dias
  en `casos_ocultos` ni en `casos_reservados` y fuera de `knowledge/cases/meses_reservados.yaml`;
  si no se puede demostrar, todos), por su nombre en espanol o en ingles, su abreviatura o las
  grafias del ASR (`GRAFIAS_MES`), o «el mes 9» y parecidos;
- trae una fecha numerica: `dd/mm`, `dd-mm`, `dd.mm.aa(aa)` o «N del M» (con cifras o con letras);
- trae un dia de la semana con un numero a dos palabras o menos;
- trae «backtest» (y sus grafias del ASR) con la abreviatura de un mes tapado («set» incluida).
Y tambien el segmento ANTERIOR y el SIGUIENTE. Ante la duda, cuarentena. Un mes demostrado libre
no se filtra. Con punto y DOS partes no es fecha: son precios («1.17»), medido en v1-v6.

LOS TRAMOS NO CITABLES (desde `trabajo/filtradas-con-tramos`, punto Q; FILTRADAS-CON-TRAMOS.md):
ademas, un segmento va a `[NO CITABLE mm:ss–mm:ss]` SIN contenido si se solapa MAS DE 0 ms con algun
tramo de `knowledge/corpus/tramos_no_citables.yaml` de SU video (`--video`, obligatorio): el que
empieza justo donde termina un tramo, o termina justo donde empieza, queda visible. La marca no
dice la clase ni el motivo del tramo. Un segmento que tapan las dos reglas va al bloque
`[NO CITABLE]`, y cuenta en «ambos». Falla cerrado: sin `--video`, con un video que no es una
sesion, con mas de un audio, o si el fichero de tramos falta, no se puede leer o no valida, no
escribe NADA (ni la cruda) y sale con error.

LA SEGMENTACION POR PREGUNTA: SOLO «pregunta» seguida del codigo abre una pregunta («Pregunta A
treinta y cinco», «pregunta a 35», «pregunta A-35»...), hasta la siguiente «pregunta ...» o hasta
«fin de pregunta», que devuelve a SIN PREGUNTA; lo que hay antes de la primera es SIN PREGUNTA.
El «a N» suelto no abre nada. Solo cuentan los codigos que se preguntan (ABIERTA o DECIDIDA).

Uso (un solo comando, desde la raiz del repo; un audio por ejecucion):
    uv run python scripts/transcribir_sesion.py --audio <fichero> --video v10 [--sesion 04]
    uv run python scripts/transcribir_sesion.py --audio <fichero> --video v10 --solo-filtrar
        (rehace la filtrada desde la cruda)
La hoja (orden y codigos de sesion) es la de `--sesion`, por defecto la sesion en curso: cada
sesion tiene la suya, y un mismo codigo puede significar otra cosa en otra sesion (S-1).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.corpus.cuarentena import (
    EXCEPCIONES,
    FICHERO_TRAMOS_NO_CITABLES,
    SESIONES_EN_CUARENTENA,
    TramosNoCitablesError,
    cargar_tramos_no_citables,
    en_cuarentena,
    normalizar,
    numeros_a_cifras,
)

RAIZ = Path(__file__).resolve().parents[1]
CARPETA_AUDIO = Path(r"C:\Users\USER\Desktop\reunion-a35-a44\sesion-02-audio")
EXTENSIONES_AUDIO = (
    ".m4a", ".mp3", ".wav", ".ogg", ".opus", ".aac", ".flac", ".wma", ".mp4", ".webm", ".mkv",
    ".mov", ".3gp", ".amr",
)  # fmt: skip
SIN_PREGUNTA = "SIN PREGUNTA"

# El orden de la hoja de la sesion 02 (`scripts/hoja_preguntas.py`, `ORDEN_SESION_02`, medido
# contra `hoja-sesion-02.docx`) con A-46 justo despues de A-21: en la hoja impresa va a mano.
ORDEN_SESION_02 = (
    "A-35", "A-45", "A-21", "A-46", "A-44", "A-43", "A-24", "A-42",
    "A-26", "A-25", "A-32",
    "A-36", "A-37", "A-29", "A-30", "A-38", "A-47", "A-48", "A-49",
    "A-18", "A-13", "A-31", "A-40", "A-33",
    "A-34", "A-41", "A-39",
)  # fmt: skip

# La hoja de la sesion 03 (2026-09-29, brief del consultor): ademas de las A-xx, codigos de sesion
# que no son ambiguedades del registro -E-x, S-1 (como decide el sesgo del dia), G-1 (cerrar antes
# del stop), G-2 (dejar correr mas alla del objetivo) y G-3 (tamano minimo de caja)-, dichos en voz
# como «pregunta S uno» o «pregunta G dos». Es el orden con el que se agrupa la version filtrada.
ORDEN_SESION_03 = (
    "A-47",
    "S-1", "A-34", "A-26", "A-39",
    "A-46", "A-35", "A-45", "A-43", "A-50",
    "A-13", "A-40", "G-1", "G-2", "A-18", "G-3",
    "A-42", "A-44",
    "A-21", "E-1",
    "A-30", "A-31", "E-2", "E-3", "A-41", "A-38", "A-24", "A-25", "A-37",
)  # fmt: skip
# La hoja de la sesion 04 (2026-10-04, decisiones del consultor de los dias 2026-10-03 y
# 2026-10-04, docs/sesion-4/HOJA-USADA.md): SOLO codigos de sesion, dichos en voz como «pregunta
# ese siete». S-n es la pregunta n de docs/sesion-4/PREGUNTAS.md, mas S-23 (A-32) y S-24 (A-13).
ORDEN_SESION_04 = (
    "S-1", "S-2", "S-3", "S-4", "S-5", "S-6", "S-22",
    "S-7", "S-8", "S-9", "S-10", "S-11", "S-12", "S-13", "S-14", "S-15", "S-16", "S-17",
    "S-18", "S-20", "S-21", "S-23", "S-24", "S-19",
)  # fmt: skip
# Los codigos de sesion con su texto, POR SESION: el mismo codigo vuelve con otro texto (S-1 era en
# la 03 «como decide el sesgo del dia» y en la 04 es la pregunta 1 de PREGUNTAS.md), asi que un
# diccionario comun se pisaria. Los de la 03 se definieron en la revision del consultor del
# 2026-09-29 (hasta entonces E-1, E-2 y E-3 no tenian texto en ningun fichero del repositorio); los
# de la 04 son los titulos de PREGUNTAS.md y del encargo de `trabajo/sesion-04`.
CODIGOS_DE_SESION_TEXTO: dict[str, dict[str, str]] = {
    "02": {},
    "03": {
        "E-1": "tus dos backtests de los mismos días",
        "E-2": "cómo operas los equals",
        "E-3": "cuando la vela cambia de color",
        "S-1": "cómo decide el sesgo del día",
        "G-1": "cerrar antes del stop",
        "G-2": "dejar correr más allá del objetivo",
        "G-3": "tamaño mínimo de caja",
    },
    "04": {
        "S-1": "cuándo pones la orden, una vez formado el mínimo (o máximo) en M1",
        "S-2": "cuándo un mínimo de M1 se convierte en tu punto de breaker",
        "S-3": "el stop al poner la orden: ¿en el 1 o en el 0,8?",
        "S-4": "si el precio sube más antes de llenarse, ¿se mueve el 1 de la caja?",
        "S-5": "la orden sin llenar al acabar la sesión o la ventana",
        "S-6": "«lo mínimo posible» al redondear el stop: ¿un punto o un pip entero?",
        "S-7": "con qué reloj empiezas a las 7 en invierno",
        "S-8": "qué corta la racha de 9 pérdidas y cuándo vuelves a operar",
        "S-9": "el tope de pérdida: ¿porcentaje o 9 seguidas?",
        "S-10": "zona limpia",
        "S-11": "el alto de M15 que el precio supera un poco",
        "S-12": "las salidas por encima de 3 R",
        "S-13": "la vela de 4 horas que rompe por los dos lados y cierra sin cuerpo",
        "S-14": "el umbral de la vela casi plana",
        "S-15": "una liquidez tomada antes de las 7",
        "S-16": "cuál de tus dos backtests de agosto vale",
        "S-17": "si solo el 0 de la caja cuenta frente al nivel tomado",
        "S-18": "los intentos: ¿por marca o por toma?",
        "S-19": "las 7 capturas que venían con el backtest de marzo",
        "S-20": "cuántos escenarios puede haber en una sesión como máximo",
        "S-21": "la orden puesta cuando el precio toma otra liquidez",
        "S-22": "dónde va la orden de entrada frente al 0 de la caja",
        "S-23": "el nivel que, roto con mecha, anula la entrada",
        "S-24": "confirmar el break even tapado por el corte de audio de v9",
    },
}
# La hoja con la que se agrupa la version filtrada de cada sesion (`--sesion`).
HOJAS: dict[str, tuple[str, ...]] = {
    "02": ORDEN_SESION_02,
    "03": ORDEN_SESION_03,
    "04": ORDEN_SESION_04,
}
SESION_EN_CURSO = "04"


# ------------------------------------------------------------------------------ cuarentena

# La regla por segmento vive desde el 2026-10-01 en `botsito.corpus.cuarentena`, que es la UNICA
# fuente para este script y para la CLI (`trabajo/cuarentena-por-defecto`).


# ------------------------------------------------------------------------ codigos de pregunta

_UNIDADES_TRAS = (
    r"puntos?|pips?|pipos?|minutos?|min|horas?|segundos?|dolares?|euros?|por\s*ciento|%|velas?|"
    r"lotes?|veces|operaciones?|dias?|semanas?|meses|anos?|pesos?|usd|k\b|mil"
)
# SOLO «pregunta» seguida del codigo abre una pregunta (protocolo de voz de la sesion 02):
# «Pregunta A treinta y cinco», «pregunta a 35», «pregunta A-35», «pregunta, A35», «pregunta
# numero 35», «pregunta 35». El «a N» suelto ya no abre nada: en la sesion 01 casaba 17 veces
# con conversacion normal («llega a 30»). Desde la sesion 03, la letra puede ser tambien E, S o G,
# con sus nombres y las grafias del ASR: «pregunta E uno», «pregunta ese uno», «pregunta G dos»,
# «pregunta je dos»; sin letra, A. Solo abre si el codigo esta entre los validos.
_LETRAS = {
    "a": "A", "ha": "A", "ah": "A",
    "e": "E", "he": "E",
    "s": "S", "ese": "S", "es": "S",
    "g": "G", "ge": "G", "je": "G",
}  # fmt: skip
_RE_CODIGO = re.compile(
    r"(?<![\w-])preguntas?\W{0,3}(?:numero\W{1,3})?"
    r"(?:(?P<l>" + "|".join(sorted(_LETRAS, key=len, reverse=True)) + r")\W{0,3})?"
    r"(?P<n>\d{1,2})(?!\d|[.,]\d)(?!\s*(?:" + _UNIDADES_TRAS + r"))"
)
_RE_FIN = re.compile(r"\b(?:fin de (?:la )?pregunta|sin pregunta|fuera de pregunta)\b")


def codigo_en(texto: str, validos: Iterable[str]) -> str | None:
    """El ULTIMO codigo de pregunta valido dicho DESPUES DE «pregunta», o None: «pregunta A
    treinta y cinco», «pregunta a 35», «pregunta A-35». «llega a 30» o «A-35» sueltos no
    cuentan."""
    conocidos = set(validos)
    t = numeros_a_cifras(normalizar(texto))
    ultimo: str | None = None
    for m in _RE_CODIGO.finditer(t):
        codigo = f"{_LETRAS.get(m.group('l') or 'a', 'A')}-{int(m.group('n'))}"
        if codigo in conocidos:
            ultimo = codigo
    return ultimo


def fin_de_pregunta(texto: str) -> bool:
    return bool(_RE_FIN.search(normalizar(texto)))


# --------------------------------------------------------------------------- la version filtrada


@dataclass(frozen=True)
class Seg:
    """Lo minimo de un segmento de la cruda: marcas en milisegundos y texto."""

    t0_ms: int
    t1_ms: int
    texto: str


def mmss(ms: int) -> str:
    """Minutos totales y segundos: «103:07» a la hora y 43 minutos."""
    s = max(ms, 0) // 1000
    return f"{s // 60:02d}:{s % 60:02d}"


CUARENTENA = "CUARENTENA"  # la marca de la regla por meses
NO_CITABLE = "NO CITABLE"  # la marca de los tramos no citables, sin su clase ni su motivo

Tramo = tuple[int, int, str]  # (t0_ms, t1_ms, motivo), como los da `cargar_tramos_no_citables`


@dataclass(frozen=True)
class Linea:
    pregunta: str
    t0_ms: int
    t1_ms: int
    texto: str | None  # None: tapada, con la marca de `marca`
    indices: tuple[int, ...]
    marca: str = CUARENTENA


def tapados_por_tramos(segmentos: Sequence[Seg], tramos: Iterable[Tramo]) -> frozenset[int]:
    """Las posiciones de los segmentos que se solapan MAS DE 0 ms con algun tramo: la misma
    condicion que `Filtro.motivos` y `tramo_no_citable` (`s.t1_ms > a and s.t0_ms < b`). Un
    segmento que empieza justo donde termina un tramo, o termina justo donde empieza, no se tapa."""
    tramos = tuple(tramos)
    return frozenset(
        i for i, s in enumerate(segmentos) if any(s.t1_ms > a and s.t0_ms < b for a, b, _ in tramos)
    )


def lineas_filtradas(
    segmentos: Sequence[Seg],
    validos: Iterable[str],
    libres: frozenset[int] | None = None,
    tramos: Iterable[Tramo] = (),
) -> tuple[list[Linea], dict[int, list[str]]]:
    """Cada segmento con su pregunta y, si esta tapado, sin texto; los tapados seguidos de la misma
    pregunta y la misma marca se funden en una sola linea. `libres`: los meses DEMOSTRADOS libres
    (`cases.holdout.meses_libres`); sin ellos la regla del mes tapa los doce. `tramos`: los tramos
    no citables del video de la sesion (`tramos_del_video`); un segmento que tapan las dos reglas
    lleva la marca `[NO CITABLE]`. Devuelve tambien los segmentos de la regla por meses."""
    validos = tuple(validos)
    textos = [s.texto for s in segmentos]
    cuarentena = en_cuarentena(textos, libres)
    no_citables = tapados_por_tramos(segmentos, tramos)
    pregunta = SIN_PREGUNTA
    salida: list[Linea] = []
    for i, s in enumerate(segmentos):
        if fin_de_pregunta(s.texto):
            pregunta = SIN_PREGUNTA
        codigo = codigo_en(s.texto, validos)
        if codigo is not None:
            pregunta = codigo
        if i in cuarentena or i in no_citables:
            marca = NO_CITABLE if i in no_citables else CUARENTENA
            previa = salida[-1] if salida else None
            if (
                previa is not None
                and previa.texto is None
                and previa.pregunta == pregunta
                and previa.marca == marca
            ):
                salida[-1] = Linea(
                    pregunta, previa.t0_ms, s.t1_ms, None, (*previa.indices, i), marca
                )
            else:
                salida.append(Linea(pregunta, s.t0_ms, s.t1_ms, None, (i,), marca))
        else:
            salida.append(Linea(pregunta, s.t0_ms, s.t1_ms, s.texto.strip(), (i,)))
    return salida, cuarentena


def orden_de_preguntas(presentes: Iterable[str], hoja: Sequence[str]) -> list[str]:
    """El orden de la hoja de la sesion, luego las demas por letra y numero, y SIN PREGUNTA al
    final."""
    presentes = set(presentes)
    en_hoja = [p for p in hoja if p in presentes]
    otras = sorted((p for p in presentes if p not in hoja and p != SIN_PREGUNTA),
                   key=lambda p: (p[0], int(p[2:])))  # fmt: skip
    return en_hoja + otras + ([SIN_PREGUNTA] if SIN_PREGUNTA in presentes else [])


def version_filtrada(lineas: Sequence[Linea], titulo: str, hoja: Sequence[str]) -> str:
    """La version que se lee: agrupada por pregunta en el orden de la hoja, cronologica dentro de
    cada pregunta, con «…» donde la conversacion volvio a esa pregunta mas tarde."""
    partes = [
        f"# {titulo} · version FILTRADA",
        "",
        "Cuarentena mecanica aplicada antes de cualquier lectura: los tramos `[CUARENTENA]` no se "
        "reconstruyen ni se escuchan. Los `[NO CITABLE]` son los tramos no citables del video "
        "(`knowledge/corpus/tramos_no_citables.yaml`): tampoco se leen ni se citan. Citas "
        "literales con `mm:ss` desde el inicio del audio.",
        "",
    ]
    for pregunta in orden_de_preguntas((ln.pregunta for ln in lineas), hoja):
        partes += [f"## {pregunta}", ""]
        ultimo_indice: int | None = None
        for ln in (x for x in lineas if x.pregunta == pregunta):
            if ultimo_indice is not None and ln.indices[0] != ultimo_indice + 1:
                partes.append("…")
            if ln.texto is None:
                partes.append(f"[{ln.marca} {mmss(ln.t0_ms)}–{mmss(ln.t1_ms)}]")
            else:
                partes.append(f"[{mmss(ln.t0_ms)}] {ln.texto}")
            ultimo_indice = ln.indices[-1]
        partes.append("")
    return "\n".join(partes).rstrip() + "\n"


def registro_filtro(
    lineas: Sequence[Linea],
    cuarentena: dict[int, list[str]],
    validos: Iterable[str],
    hoja: Sequence[str],
    no_citables: Collection[int] = frozenset(),
) -> list[str]:
    """Lo que el registro puede decir del texto: recuentos y codigos, nunca contenido.
    `no_citables`: los segmentos que tapan los tramos (`tapados_por_tramos`)."""
    motivos: Counter[str] = Counter(m for ms in cuarentena.values() for m in ms)
    bloques = sum(1 for ln in lineas if ln.texto is None and ln.marca == CUARENTENA)
    bloques_nc = sum(1 for ln in lineas if ln.texto is None and ln.marca == NO_CITABLE)
    meses, tramos_nc = set(cuarentena), set(no_citables)
    primeras: dict[str, int] = {}
    tramos: Counter[str] = Counter()
    anterior = None
    for ln in lineas:
        if ln.pregunta != anterior:
            tramos[ln.pregunta] += 1
            primeras.setdefault(ln.pregunta, ln.t0_ms)
        anterior = ln.pregunta
    detectados = [p for p in orden_de_preguntas(primeras, hoja) if p != SIN_PREGUNTA]
    no_detectados = [p for p in hoja if p not in primeras]
    return [
        f"segmentos: {sum(len(ln.indices) for ln in lineas)}",
        f"segmentos en cuarentena: {len(cuarentena)} en {bloques} bloques",
        f"segmentos tapados: solo por meses {len(meses - tramos_nc)}, solo por tramos "
        f"{len(tramos_nc - meses)}, por ambos {len(meses & tramos_nc)}",
        f"bloques [{NO_CITABLE}]: {bloques_nc} (los de «ambos» van aqui)",
        "motivos (un segmento puede tener varios): "
        + ", ".join(f"{m} {n}" for m, n in sorted(motivos.items())),
        "codigos detectados (primera vez, tramos): "
        + (", ".join(f"{p} {mmss(primeras[p])} x{tramos[p]}" for p in detectados) or "ninguno"),
        "preguntas de la hoja SIN codigo detectado: " + (", ".join(no_detectados) or "ninguna"),
        f"codigos validos considerados: {len(tuple(validos))}",
    ]


# ------------------------------------------------------------------------------ transcripcion


class SesionError(RuntimeError):
    """Algo que impide transcribir o escribir fuera del repo: se dice y no se escribe nada."""


def fuera_del_repo(ruta: Path) -> Path:
    """La ruta, o `SesionError` si cae dentro del repositorio: el audio y la cruda nunca entran."""
    absoluta = ruta.resolve()
    if absoluta == RAIZ or RAIZ in absoluta.parents:
        raise SesionError(f"{absoluta} esta dentro del repositorio: la salida va fuera")
    return ruta


def audios_de(ruta: Path) -> list[Path]:
    if ruta.is_file():
        return [ruta]
    if not ruta.is_dir():
        raise SesionError(f"no existe {ruta}")
    encontrados = sorted(p for p in ruta.iterdir() if p.suffix.lower() in EXTENSIONES_AUDIO)
    if not encontrados:
        raise SesionError(f"no hay ningun audio en {ruta} ({', '.join(EXTENSIONES_AUDIO)})")
    return encontrados


def salidas_de(audio: Path) -> dict[str, Path]:
    base = audio.parent
    return {
        "cruda": base / f"{audio.stem}.cruda-NO-LEER.jsonl",
        "cruda_txt": base / f"{audio.stem}.cruda-NO-LEER.txt",
        "filtrada": base / f"{audio.stem}.filtrada.md",
        "registro": base / f"{audio.stem}.registro.txt",
        "trabajo": base / f"{audio.stem}-trabajo",
    }


def _comprobar_rutas(rutas: Iterable[Path]) -> None:
    from botsito.engine.diagnostico import comprobar_ruta

    for r in rutas:
        fuera_del_repo(r)
        comprobar_ruta(r)


def transcribir(
    audio: Path, trabajo: Path, dispositivo: str
) -> tuple[list[Seg], dict[str, Any], float]:
    """El ASR del corpus sobre un audio suelto. Devuelve los segmentos, la descripcion del motor y
    la duracion del audio en segundos."""
    os.environ.setdefault("HF_HUB_OFFLINE", "1")  # no se descarga ningun modelo
    from botsito.corpus.audio import (
        MUESTRAS_S,
        ParametrosCorte,
        cortar_wav,
        detectar_silencios,
        extraer_wav,
        muestras_wav,
        puntos_de_corte,
    )
    from botsito.corpus.glosario import cargar_glosario
    from botsito.corpus.motor_whisper import ConfiguracionWhisper, MotorWhisper
    from botsito.corpus.pipeline_transcripcion import huella_de
    from botsito.corpus.transcripcion import fusionar, transcribir_fragmentos

    glosario = cargar_glosario(RAIZ / "knowledge" / "corpus" / "glosario_asr.yaml")
    motor = MotorWhisper(
        ConfiguracionWhisper("large-v3", dispositivo, "int8_float16", glosario.prompt_inicial)
    )
    wav = trabajo / "audio.wav"
    extraer_wav(audio, wav)
    n = muestras_wav(wav)
    p = ParametrosCorte()
    silencios = detectar_silencios(wav, p.umbral_db, p.silencio_minimo_s)
    cortes = puntos_de_corte(n, silencios, p)
    fragmentos = cortar_wav(wav, cortes.puntos_m, trabajo / "fragmentos")
    descripcion = motor.describir()
    por_fragmento = transcribir_fragmentos(
        fragmentos, motor, trabajo / "parciales", huella_de(p.como_dict(), descripcion)
    )
    fusion = fusionar(por_fragmento, n * 1000 // MUESTRAS_S)
    segs = [Seg(s.t0_ms, s.t1_ms, s.texto) for s in fusion.segmentos]
    return segs, descripcion, n / MUESTRAS_S


def _escribir(ruta: Path, texto: str) -> None:
    fuera_del_repo(ruta)
    ruta.write_text(texto, encoding="utf-8", newline="\n")


def tramos_del_video(video: str | None, repo: Path) -> tuple[Tramo, ...]:
    """Los tramos no citables de `video`, o `SesionError`: FALLA CERRADO. Sin video declarado, con
    un video que no es una sesion (`SESIONES_EN_CUARENTENA` o `EXCEPCIONES`), o si el fichero de
    tramos falta, no se puede leer o no valida, no hay filtrada. `cargar_tramos_no_citables` (la
    funcion de la libreria, la misma de `knowledge validate`) devuelve {} si el fichero falta: aqui
    eso es un error. Un video de sesion sin tramos (v8) da una tupla vacia."""
    if video is None:
        raise SesionError("falta --video: sin el video de la sesion no se aplican sus tramos")
    sesiones = SESIONES_EN_CUARENTENA | frozenset(EXCEPCIONES)
    if video not in sesiones:
        raise SesionError(
            f"--video {video} no es un video de sesion ({', '.join(sorted(sesiones))})"
        )
    if not (repo / FICHERO_TRAMOS_NO_CITABLES).is_file():
        raise SesionError(
            f"no existe {FICHERO_TRAMOS_NO_CITABLES}: sin tramos no se escribe la filtrada"
        )
    try:
        return cargar_tramos_no_citables(repo).get(video, ())
    except TramosNoCitablesError as exc:
        raise SesionError(f"los tramos no citables no se pueden usar: {exc}") from exc


def procesar(
    audio: Path, dispositivo: str, solo_filtrar: bool, sesion: str, video: str | None = None
) -> list[str]:
    # Lo primero, antes de escribir nada (tampoco la cruda): sin tramos validos no hay salida.
    tramos = tramos_del_video(video, RAIZ)
    salidas = salidas_de(audio)
    _comprobar_rutas([*salidas.values(), salidas["trabajo"] / "fragmentos" / "fragmento_000.wav"])
    inicio = time.perf_counter()
    registro = [
        f"# registro de {audio.name} (sin contenido del trader)",
        f"hoja: la de la sesion {sesion}",
        f"video: {video}; tramos no citables del video: {len(tramos)} "
        f"({FICHERO_TRAMOS_NO_CITABLES})",
    ]
    if solo_filtrar:
        if not salidas["cruda"].is_file():
            raise SesionError(f"--solo-filtrar sin cruda: no existe {salidas['cruda']}")
        segmentos = [
            Seg(d["t0_ms"], d["t1_ms"], d["texto"])
            for d in (json.loads(x) for x in salidas["cruda"].read_text("utf-8").splitlines() if x)
        ]
        registro.append("modo: solo filtrar (la cruda ya existia; ASR no ejecutado)")
    else:
        salidas["trabajo"].mkdir(parents=True, exist_ok=True)
        segmentos, motor, duracion_s = transcribir(audio, salidas["trabajo"], dispositivo)
        asr_s = time.perf_counter() - inicio
        _escribir(
            salidas["cruda"],
            "".join(
                json.dumps(
                    {"n": i, "t0_ms": s.t0_ms, "t1_ms": s.t1_ms, "texto": s.texto},
                    ensure_ascii=False,
                )
                + "\n"
                for i, s in enumerate(segmentos)
            ),
        )
        _escribir(
            salidas["cruda_txt"],
            "".join(f"[{mmss(s.t0_ms)}] {s.texto.strip()}\n" for s in segmentos),
        )
        registro += [
            f"duracion del audio: {duracion_s:.1f} s ({duracion_s / 60:.1f} min)",
            f"tiempo de ASR: {asr_s:.1f} s; factor {asr_s / max(duracion_s, 1e-9):.2f} x tiempo "
            f"real; 2 h de audio: ~{asr_s / max(duracion_s, 1e-9) * 7200 / 60:.0f} min",
            f"motor: {motor.get('motor')} {motor.get('modelo')} {motor.get('compute_type')} en "
            f"{motor.get('dispositivo')} ({motor.get('gpu')}), faster-whisper "
            f"{motor.get('faster_whisper')}, prompt de {motor.get('initial_prompt_tokens')} tokens",
        ]
    validos = codigos_validos(sesion)
    hoja = HOJAS[sesion]
    lineas, cuarentena = lineas_filtradas(segmentos, validos, meses_libres_del_repo(), tramos)
    _escribir(salidas["filtrada"], version_filtrada(lineas, f"Sesion · {audio.stem}", hoja))
    registro += registro_filtro(
        lineas, cuarentena, validos, hoja, tapados_por_tramos(segmentos, tramos)
    )
    registro += [
        f"tiempo total: {time.perf_counter() - inicio:.1f} s",
        f"version filtrada (la UNICA que se lee): {salidas['filtrada']}",
        f"cruda (NO se lee): {salidas['cruda']}",
    ]
    _escribir(salidas["registro"], "\n".join(registro) + "\n")
    return registro


def meses_libres_del_repo() -> frozenset[int] | None:
    """Los meses DEMOSTRADOS libres para la regla del mes (rama `trabajo/cuarentena-por-condicion`),
    o None si no se pueden demostrar: entonces se tapan los doce."""
    from botsito.cases.holdout import meses_libres

    return meses_libres(RAIZ)


def codigos_validos(sesion: str) -> tuple[str, ...]:
    """Los ids que se pueden preguntar: ABIERTA o DECIDIDA en `knowledge/spec/ambiguedades.yaml`
    (solo lectura), mas los codigos de sesion de la hoja de ESA sesion. Las RESUELTAS (A-1..A-12 y
    otras) no cuentan: «a dos» no es A-2."""
    from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades

    return tuple(
        a.id
        for a in cargar_ambiguedades(RAIZ / FICHERO_AMBIGUEDADES)
        if a.estado in ("ABIERTA", "DECIDIDA")
    ) + tuple(CODIGOS_DE_SESION_TEXTO[sesion])


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--audio",
        type=Path,
        default=CARPETA_AUDIO,
        help="fichero de audio o carpeta con audios (la salida va a esa carpeta)",
    )
    parser.add_argument("--dispositivo", default="cuda", choices=("cuda", "cpu"))
    parser.add_argument(
        "--sesion",
        default=SESION_EN_CURSO,
        choices=tuple(HOJAS),
        help=f"la hoja con la que se agrupa la filtrada (por defecto, la {SESION_EN_CURSO})",
    )
    parser.add_argument(
        "--solo-filtrar",
        action="store_true",
        help="no transcribe: rehace la version filtrada desde la cruda",
    )
    parser.add_argument(
        "--video",
        default=None,
        help="el video_id de la sesion (v7, v8, v9, v10...): sus tramos no citables se tapan. "
        "Obligatorio: sin el no se escribe nada",
    )
    args = parser.parse_args(argv)
    try:
        audios = audios_de(args.audio)
        if len(audios) != 1:
            raise SesionError(
                f"--audio da {len(audios)} audios: uno por ejecucion, porque cada uno lleva los "
                "tramos de su video (--video)"
            )
        print(
            "\n".join(
                procesar(audios[0], args.dispositivo, args.solo_filtrar, args.sesion, args.video)
            )
        )
    except SesionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (ValueError, RuntimeError) as exc:  # la guarda de 259, ffmpeg, el ASR
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
