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
- nombra septiembre, marzo, mayo o febrero, con las grafias y errores del ASR (`MESES_FILTRADOS`),
  o sus abreviaturas, o su nombre en ingles, o «el mes 9» y parecidos;
- trae una fecha numerica: `dd/mm`, `dd-mm`, `dd.mm.aa(aa)` o «N del M» (con cifras o con letras);
- trae un dia de la semana con un numero a dos palabras o menos;
- trae «backtest» (y sus grafias del ASR) con una abreviatura de mes.
Y tambien el segmento ANTERIOR y el SIGUIENTE. Ante la duda, cuarentena. Abril, agosto y enero
no se filtran. Con punto y DOS partes no es fecha: son precios («1.17»), medido en v1-v6.

LA SEGMENTACION POR PREGUNTA: SOLO «pregunta» seguida del codigo abre una pregunta («Pregunta A
treinta y cinco», «pregunta a 35», «pregunta A-35»...), hasta la siguiente «pregunta ...» o hasta
«fin de pregunta», que devuelve a SIN PREGUNTA; lo que hay antes de la primera es SIN PREGUNTA.
El «a N» suelto no abre nada. Solo cuentan los codigos que se preguntan (ABIERTA o DECIDIDA).

Uso (un solo comando, desde la raiz del repo):
    uv run python scripts/transcribir_sesion.py [--audio <fichero o carpeta>]
    uv run python scripts/transcribir_sesion.py --solo-filtrar   (rehace la filtrada desde la cruda)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

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
    "A-36", "A-37", "A-29", "A-30", "A-38",
    "A-18", "A-13", "A-31", "A-40", "A-33",
    "A-34", "A-41", "A-39",
)  # fmt: skip


# ------------------------------------------------------------------------------ normalizar


def normalizar(texto: str) -> str:
    """Minusculas y sin tildes; los guiones, barras y puntos se conservan (las fechas los usan)."""
    plano = unicodedata.normalize("NFD", texto.lower())
    return "".join(c for c in plano if unicodedata.category(c) != "Mn")


_UNIDADES = {
    "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
    "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10, "once": 11, "doce": 12,
    "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16, "diecisiete": 17,
    "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiun": 21, "veintiuno": 21,
    "veintiuna": 21, "veintidos": 22, "veintitres": 23, "veinticuatro": 24, "veinticinco": 25,
    "veintiseis": 26, "veintisiete": 27, "veintiocho": 28, "veintinueve": 29,
}  # fmt: skip
_DECENAS = {
    "treinta": 30, "cuarenta": 40, "cincuenta": 50, "sesenta": 60, "setenta": 70,
    "ochenta": 80, "noventa": 90,
}  # fmt: skip


def numeros_a_cifras(texto: str) -> str:
    """«treinta y cinco» -> «35», «veinticinco» -> «25», «trece» -> «13» (de 0 a 99), sobre texto
    ya normalizado. «un» y «una» NO se convierten: «voy a una zona» no es el codigo A-1."""
    tokens = re.findall(r"\w+|[^\w\s]|\s+", texto)
    salida: list[str] = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t in _DECENAS:
            valor = _DECENAS[t]
            # «treinta y cinco»: decena, espacio, «y», espacio, unidad 1-9
            if (
                i + 4 < len(tokens)
                and tokens[i + 1].isspace()
                and tokens[i + 2] == "y"
                and tokens[i + 3].isspace()
                and 1 <= _UNIDADES.get(tokens[i + 4], 0) <= 9
            ):
                salida.append(str(valor + _UNIDADES[tokens[i + 4]]))
                i += 5
                continue
            salida.append(str(valor))
        elif t in _UNIDADES:
            salida.append(str(_UNIDADES[t]))
        else:
            salida.append(t)
        i += 1
    return "".join(salida)


# ------------------------------------------------------------------------------ cuarentena

# Grafias de los cuatro meses. Medido en las crudas de v1-v6: el ASR escribe «mayo»,
# «septiembre» y «marzo» bien; «mayo» es PREFIJO de «mayor» y «mayoria», y «siempre» se parece a
# «setiempre», asi que todo va por palabra entera. Los errores tipicos se anaden por si acaso.
MESES_FILTRADOS = (
    r"se[cpt]{0,2}i?e?m[bp]re?s?",  # septiembre, setiembre, setiempre, sectiembre, setembre...
    r"sept?",  # sep, sept (abreviatura)
    r"septem[bp]er",
    r"mar[sz]os?|mar",  # marzo, marso, mar (NO «marco»: ver abajo)
    r"march",
    r"ma[yi]o|mallo",  # mayo, maio, mallo (no «malo»)
    r"may",
    r"fe[bv]r?e?r?o?s?",  # febrero, febreo, febrer, feb, fevrero
    r"february",
)
# «marco» NO se filtra: es el verbo del trader («lo marco», «marco la liquidez») y el sustantivo
# de «marco de operativa»; en las crudas de v1-v6 no hay ni un «marco» por «marzo» (medido el
# 2026-09-27: «marzo» sale bien escrito la unica vez que aparece).
_RE_MES = re.compile(r"\b(?:" + "|".join(MESES_FILTRADOS) + r")\b")
_NUM = r"(?:\d{1,2})"
_RE_FECHA = re.compile(
    rf"(?<![\d.,]){_NUM}\s*[/-]\s*{_NUM}(?:\s*[/-]\s*\d{{2,4}})?(?![\d.,])"  # 31/02, 31-02-26
    rf"|(?<![\d.,]){_NUM}\.{_NUM}\.\d{{2,4}}(?![\d.,])"  # 31.02.26 (dos partes: precio)
    rf"|(?<![\d.,]){_NUM}\s+del?\s+{_NUM}(?![\d.,])"  # «45 del 13», «3 de 9»
    rf"|\bmes\s+{_NUM}\b"  # «el mes 9»
)
_DIAS = r"(?:lunes|martes|miercoles|jueves|viernes|sabado|domingo)"
_RE_DIA_NUMERO = re.compile(rf"\b{_DIAS}\b(?:\W+\w+)?\W+{_NUM}\b|\b{_NUM}\b(?:\W+\w+)?\W+{_DIAS}\b")
_RE_BACKTEST = re.compile(r"\b(?:back\s*-?\s*tests?|bac?k?test\w*|vac?k?test\w*)\b")
_RE_ABREV = re.compile(r"\b(?:sep|sept|set|mar|may|feb)\b")

MOTIVO_MES = "mes"
MOTIVO_FECHA = "fecha numerica"
MOTIVO_DIA = "dia de la semana con numero"
MOTIVO_BACKTEST = "backtest con mes"
MOTIVO_VECINO = "vecino"


def motivos_cuarentena(texto: str) -> list[str]:
    """Por que un texto va a cuarentena (lista vacia si no va). Sin tildes, sin mayusculas, y con
    los numeros escritos en letras pasados a cifras."""
    t = numeros_a_cifras(normalizar(texto))
    motivos: list[str] = []
    if _RE_MES.search(t):
        motivos.append(MOTIVO_MES)
    if _RE_FECHA.search(t):
        motivos.append(MOTIVO_FECHA)
    if _RE_DIA_NUMERO.search(t):
        motivos.append(MOTIVO_DIA)
    if _RE_BACKTEST.search(t) and _RE_ABREV.search(t):
        motivos.append(MOTIVO_BACKTEST)
    return motivos


def en_cuarentena(textos: Sequence[str]) -> dict[int, list[str]]:
    """Indice -> motivos. Cada segmento con motivo arrastra al anterior y al siguiente."""
    propios = {i: m for i, t in enumerate(textos) if (m := motivos_cuarentena(t))}
    salida: dict[int, list[str]] = {i: list(m) for i, m in propios.items()}
    for i in propios:
        for j in (i - 1, i + 1):
            if 0 <= j < len(textos) and j not in propios:
                salida.setdefault(j, [MOTIVO_VECINO])
    return salida


# ------------------------------------------------------------------------ codigos de pregunta

_UNIDADES_TRAS = (
    r"puntos?|pips?|pipos?|minutos?|min|horas?|segundos?|dolares?|euros?|por\s*ciento|%|velas?|"
    r"lotes?|veces|operaciones?|dias?|semanas?|meses|anos?|pesos?|usd|k\b|mil"
)
# SOLO «pregunta» seguida del codigo abre una pregunta (protocolo de voz de la sesion 02):
# «Pregunta A treinta y cinco», «pregunta a 35», «pregunta A-35», «pregunta, A35», «pregunta
# numero 35», «pregunta 35». El «a N» suelto ya no abre nada: en la sesion 01 casaba 17 veces
# con conversacion normal («llega a 30»).
_RE_CODIGO = re.compile(
    r"(?<![\w-])preguntas?\W{0,3}(?:numero\W{1,3})?(?:(?:a|ha|ah)\W{0,3})?"
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
        codigo = f"A-{int(m.group('n'))}"
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


@dataclass(frozen=True)
class Linea:
    pregunta: str
    t0_ms: int
    t1_ms: int
    texto: str | None  # None: cuarentena
    indices: tuple[int, ...]


def lineas_filtradas(
    segmentos: Sequence[Seg], validos: Iterable[str]
) -> tuple[list[Linea], dict[int, list[str]]]:
    """Cada segmento con su pregunta y, si esta en cuarentena, sin texto; los tramos seguidos de
    cuarentena de la misma pregunta se funden en una sola linea."""
    validos = tuple(validos)
    textos = [s.texto for s in segmentos]
    cuarentena = en_cuarentena(textos)
    pregunta = SIN_PREGUNTA
    salida: list[Linea] = []
    for i, s in enumerate(segmentos):
        if fin_de_pregunta(s.texto):
            pregunta = SIN_PREGUNTA
        codigo = codigo_en(s.texto, validos)
        if codigo is not None:
            pregunta = codigo
        if i in cuarentena:
            previa = salida[-1] if salida else None
            if previa is not None and previa.texto is None and previa.pregunta == pregunta:
                salida[-1] = Linea(pregunta, previa.t0_ms, s.t1_ms, None, (*previa.indices, i))
            else:
                salida.append(Linea(pregunta, s.t0_ms, s.t1_ms, None, (i,)))
        else:
            salida.append(Linea(pregunta, s.t0_ms, s.t1_ms, s.texto.strip(), (i,)))
    return salida, cuarentena


def orden_de_preguntas(presentes: Iterable[str]) -> list[str]:
    """El orden de la hoja (con A-46), luego las demas por numero, y SIN PREGUNTA al final."""
    presentes = set(presentes)
    en_hoja = [p for p in ORDEN_SESION_02 if p in presentes]
    otras = sorted((p for p in presentes if p not in ORDEN_SESION_02 and p != SIN_PREGUNTA),
                   key=lambda p: int(p[2:]))  # fmt: skip
    return en_hoja + otras + ([SIN_PREGUNTA] if SIN_PREGUNTA in presentes else [])


def version_filtrada(lineas: Sequence[Linea], titulo: str) -> str:
    """La version que se lee: agrupada por pregunta en el orden de la hoja, cronologica dentro de
    cada pregunta, con «…» donde la conversacion volvio a esa pregunta mas tarde."""
    partes = [
        f"# {titulo} · version FILTRADA",
        "",
        "Cuarentena mecanica aplicada antes de cualquier lectura: los tramos `[CUARENTENA]` no se "
        "reconstruyen ni se escuchan. Citas literales con `mm:ss` desde el inicio del audio.",
        "",
    ]
    for pregunta in orden_de_preguntas(ln.pregunta for ln in lineas):
        partes += [f"## {pregunta}", ""]
        ultimo_indice: int | None = None
        for ln in (x for x in lineas if x.pregunta == pregunta):
            if ultimo_indice is not None and ln.indices[0] != ultimo_indice + 1:
                partes.append("…")
            if ln.texto is None:
                partes.append(f"[CUARENTENA {mmss(ln.t0_ms)}–{mmss(ln.t1_ms)}]")
            else:
                partes.append(f"[{mmss(ln.t0_ms)}] {ln.texto}")
            ultimo_indice = ln.indices[-1]
        partes.append("")
    return "\n".join(partes).rstrip() + "\n"


def registro_filtro(
    lineas: Sequence[Linea], cuarentena: dict[int, list[str]], validos: Iterable[str]
) -> list[str]:
    """Lo que el registro puede decir del texto: recuentos y codigos, nunca contenido."""
    motivos: Counter[str] = Counter(m for ms in cuarentena.values() for m in ms)
    bloques = sum(1 for ln in lineas if ln.texto is None)
    primeras: dict[str, int] = {}
    tramos: Counter[str] = Counter()
    anterior = None
    for ln in lineas:
        if ln.pregunta != anterior:
            tramos[ln.pregunta] += 1
            primeras.setdefault(ln.pregunta, ln.t0_ms)
        anterior = ln.pregunta
    detectados = [p for p in orden_de_preguntas(primeras) if p != SIN_PREGUNTA]
    no_detectados = [p for p in ORDEN_SESION_02 if p not in primeras]
    return [
        f"segmentos: {sum(len(ln.indices) for ln in lineas)}",
        f"segmentos en cuarentena: {len(cuarentena)} en {bloques} bloques",
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


def procesar(audio: Path, dispositivo: str, solo_filtrar: bool) -> list[str]:
    salidas = salidas_de(audio)
    _comprobar_rutas([*salidas.values(), salidas["trabajo"] / "fragmentos" / "fragmento_000.wav"])
    inicio = time.perf_counter()
    registro = [f"# registro de {audio.name} (sin contenido del trader)"]
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
    validos = codigos_validos()
    lineas, cuarentena = lineas_filtradas(segmentos, validos)
    _escribir(salidas["filtrada"], version_filtrada(lineas, f"Sesion · {audio.stem}"))
    registro += registro_filtro(lineas, cuarentena, validos)
    registro += [
        f"tiempo total: {time.perf_counter() - inicio:.1f} s",
        f"version filtrada (la UNICA que se lee): {salidas['filtrada']}",
        f"cruda (NO se lee): {salidas['cruda']}",
    ]
    _escribir(salidas["registro"], "\n".join(registro) + "\n")
    return registro


def codigos_validos() -> tuple[str, ...]:
    """Los ids que se pueden preguntar: ABIERTA o DECIDIDA en `knowledge/spec/ambiguedades.yaml`
    (solo lectura). Las RESUELTAS (A-1..A-12 y otras) no cuentan: «a dos» no es A-2."""
    from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades

    return tuple(
        a.id
        for a in cargar_ambiguedades(RAIZ / FICHERO_AMBIGUEDADES)
        if a.estado in ("ABIERTA", "DECIDIDA")
    )


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
        "--solo-filtrar",
        action="store_true",
        help="no transcribe: rehace la version filtrada desde la cruda",
    )
    args = parser.parse_args(argv)
    try:
        for audio in audios_de(args.audio):
            print("\n".join(procesar(audio, args.dispositivo, args.solo_filtrar)))
    except SesionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except (ValueError, RuntimeError) as exc:  # la guarda de 259, ffmpeg, el ASR
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
