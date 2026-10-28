"""La cuarentena mecanica (desde el 2026-10-01 en `botsito.corpus.cuarentena`) y la segmentacion
por pregunta de `scripts/transcribir_sesion.py`, sobre
texto SINTETICO y sin audio.

Ningun dato de prueba lleva una fecha real de un dia reservado: los meses filtrados van sin dia;
los patrones numericos usan fechas IMPOSIBLES («31/02», «45 del 13», «el jueves 40»); y las fechas
con dia son de abril y agosto, en los casos que NO deben filtrarse."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from types import ModuleType

import pytest

from botsito.cases.holdout import meses_libres
from botsito.corpus import cuarentena as cu

RAIZ = Path(__file__).resolve().parents[2]
VALIDOS = ("A-21", "A-24", "A-25", "A-30", "A-35", "A-44", "A-45", "A-46")


@pytest.fixture(scope="module")
def m() -> ModuleType:
    nombre = "transcribir_sesion"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


# -------------------------------------------------------------------------------- los meses


@pytest.mark.parametrize(
    "texto",
    [
        "eso lo vi en septiembre",
        "lo de setiembre ya lo hablamos",
        "SEPTIEMBRE fue raro",
        "en Setiembre, no",
        "el sep lo tengo apuntado",
        "eso fue en marzo",
        "Marzo.",
        "lo de marso",
        "cuando lo probaste en mayo",
        "en Mayo, bueno",
        "lo de maio",
        "en febrero no operé",
        "lo de febreo",
        "el feb",
        "in September",
        "back in March",
        "the february one",
    ],
)
def test_cada_mes_filtrado_y_sus_grafias_van_a_cuarentena(m: ModuleType, texto: str) -> None:
    assert cu.MOTIVO_MES in cu.motivos_cuarentena(texto), texto


@pytest.mark.parametrize(
    "texto",
    [
        "eso fue en abril",
        "el 14 de abril entré dos veces",
        "en agosto, el 20 de agosto",
        "en enero no había backtest",
        "el backtest de abril",
        "es la mayor de todas",
        "la mayoría de las veces",
        "siempre pongo el stop ahí",
        "dentro de mi marco de operativa",
        "yo lo marco cuando cierra",
        "marco la liquidez de M15",
        "en el marco temporal de un minuto",
        "el precio estaba en 1.17 y bajó a 1.08",
        "a 35 puntos del nivel",
        "entre las 7 y las 11",
    ],
)
def test_abril_agosto_enero_y_el_lenguaje_normal_no_se_filtran(m: ModuleType, texto: str) -> None:
    """Desde `trabajo/cuarentena-por-condicion` un mes solo se deja ver si esta DEMOSTRADO libre:
    abril, agosto y enero lo estan en el repositorio real (`meses_libres`), y sin ese dato la
    regla los taparia (`test_cuarentena_por_condicion.py`)."""
    libres = meses_libres(RAIZ)
    assert libres is not None and {1, 4, 8} <= libres
    assert cu.motivos_cuarentena(texto, libres) == [], texto


# -------------------------------------------------------------------- fechas y dias de la semana


@pytest.mark.parametrize(
    "texto",
    [
        "el 31/02 entré",
        "fue el 31-02",
        "el 31.02.99",
        "el 45 del 13",
        "el treinta y dos del trece",
        "el mes 13 fue otro",
    ],
)
def test_una_fecha_numerica_va_a_cuarentena(m: ModuleType, texto: str) -> None:
    assert cu.MOTIVO_FECHA in cu.motivos_cuarentena(texto), texto


# Rama `trabajo/cuarentena-por-condicion-2`: una coma o un punto forman parte de un numero solo con
# un digito a cada lado. Fechas imposibles (mes 13, 31 de febrero), como el resto del fichero. El
# literal del encargo era una fecha real (la de una grabacion): se cambio por «hoy, 45 del 13,»
# (respuesta del consultor a la PARADA de la fase 0, punto 3).
PEGADAS_NUEVAS = ("hoy, 45 del 13,", "el 31/02,", "el 31.02.99.")  # en main: []
PEGADA_DE_CONTROL = ", 31-02 ,"  # ya se tapaba en main
NO_SON_FECHAS = ("cuesta 10,5 pips", "son 1,5 pips", "1.0850 del 2", "2.000 mensajes")
# Los que SOLO la condicion del digito a cada lado deja fuera: con un borde que no mire la coma ni
# el punto, serian fechas.
DECIMALES_QUE_NO_SON_FECHAS = ("1,5 del 13", "entre 1.45/1.46", "de 10,5-13,5")

# `_RE_FECHA` y `_RE_DIA_BARRA_MES` de `main`, copiadas tal cual de src/botsito/corpus/cuarentena.py
# en 0fa9c81 (`:283-289` y `:377`), antes de esta rama: el borde excluia TODA coma o punto. Son la
# GUARDIA DE REGRESION del superconjunto (`test_la_rama_no_tapa_menos_que_main`); que los textos
# nuevos rompen en main lo prueba la sonda sobre el codigo real de main (informe de la rama).
_NUM_MAIN = r"(?:\d{1,2})"
RE_FECHA_MAIN = re.compile(
    rf"(?<![\d.,]){_NUM_MAIN}\s*[/-]\s*{_NUM_MAIN}(?:\s*[/-]\s*\d{{2,4}})?(?![\d.,])"
    rf"|(?<![\d.,]){_NUM_MAIN}\.{_NUM_MAIN}\.\d{{2,4}}(?![\d.,])"
    rf"|(?<![\d.,]){_NUM_MAIN}\s+del?\s+{_NUM_MAIN}(?![\d.,])"
    rf"|\bmes\s+{_NUM_MAIN}\b"
)
RE_DIA_BARRA_MES_MAIN = re.compile(r"(?<![\d.,])(\d{1,2})\s*[/-]\s*(\d{1,2})(?![\d.,])")


@pytest.mark.parametrize("texto", [*PEGADAS_NUEVAS, PEGADA_DE_CONTROL])
def test_una_fecha_pegada_a_una_coma_o_un_punto_va_a_cuarentena(m: ModuleType, texto: str) -> None:
    assert cu.MOTIVO_FECHA in cu.motivos_cuarentena(texto), texto


@pytest.mark.parametrize("texto", [*NO_SON_FECHAS, *DECIMALES_QUE_NO_SON_FECHAS])
def test_un_numero_con_decimales_no_es_una_fecha(m: ModuleType, texto: str) -> None:
    assert cu.motivos_cuarentena(texto) == [], texto


def test_fechas_en_ve_la_fecha_pegada_a_una_coma_o_un_punto(m: ModuleType) -> None:
    """La misma condicion en `_RE_DIA_BARRA_MES`, que usa la evidencia (`fechas_en`)."""
    assert cu.fechas_en("el 31/02,") == {(2, 31)}
    assert cu.fechas_en("el 31/02.") == {(2, 31)}
    assert cu.fechas_en("entre 1.45/1.46") == set()


def test_la_coma_y_el_punto_rotos_a_proposito_en_los_dos_sentidos(m: ModuleType) -> None:
    def tapa(regex: re.Pattern[str], texto: str) -> bool:
        return bool(regex.search(cu.numeros_a_cifras(cu.normalizar(texto))))

    # (1) Con el borde de main, las nuevas no se tapan (y la de control si): son nuevas de verdad.
    assert not any(tapa(RE_FECHA_MAIN, t) for t in PEGADAS_NUEVAS)
    assert tapa(RE_FECHA_MAIN, PEGADA_DE_CONTROL)
    assert RE_DIA_BARRA_MES_MAIN.findall("el 31/02,") == []
    # (2) Con un borde que solo mire el digito, sin la coma ni el punto, los decimales serian
    # fechas.
    solo_digito = re.compile(
        cu._RE_FECHA.pattern.replace(cu._ANTES, r"(?<!\d)").replace(cu._DESPUES, r"(?!\d)")
    )
    assert solo_digito.pattern != cu._RE_FECHA.pattern
    assert all(tapa(solo_digito, t) for t in DECIMALES_QUE_NO_SON_FECHAS)
    assert not any(tapa(cu._RE_FECHA, t) for t in DECIMALES_QUE_NO_SON_FECHAS)


DIAS_DEL_MES = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
# Dos numeros sueltos de una o dos cifras unidos por cualquier separador que una fecha pueda usar
# (de mas: tambien la coma y el espacio), solapados. Las dos regex solo sacan numeros sueltos.
_PAR = re.compile(r"(?=(?<!\d)(\d{1,2})\s*(?:[/.,-]|\s+del?\s+|\s+)\s*(\d{1,2})(?!\d))")


def _sin_fechas_posibles(texto: str) -> bool:
    """Ningun par dia/mes del texto es una fecha que exista (revisor de la rama, B1): o el mes no
    esta entre 1 y 12, o el dia pasa de los del mes («31/2», «31/4», «45 del 13»)."""
    pares = [(int(d), int(m)) for d, m in _PAR.findall(texto)]
    return not any(1 <= m <= 12 and 1 <= d <= DIAS_DEL_MES[m - 1] for d, m in pares)


def _bateria() -> list[str]:
    """Textos sinteticos: numeros, decimales, precios y fechas con signos alrededor, y de ellos
    solo los que no traen ninguna fecha posible (ningun dato de prueba es una fecha real)."""
    numeros = ("1", "9", "12", "31", "45", "0", "10,5", "1,5", "1.0850", "2.000", "1.08", "30", "2")
    separadores = ("/", "-", " / ", " del ", " de ", ".", ",", " ")
    antes = ("", "hoy, ", "el ", "1", "1,", "1.", ",", ".", "a,", "x.", "(", "mes ")
    despues = ("", ",", ".", " ", "1", ",5", ".5", "x", ".99", ".99.", "-26", "-2", ")")
    return [
        texto
        for a in numeros
        for s in separadores
        for b in numeros
        for pre in antes
        for post in despues
        if _sin_fechas_posibles(texto := f"{pre}{a}{s}{b}{post}")
    ]


def _fechas_en_main(texto: str) -> set[tuple[int, int]]:
    """`fechas_en` de `main` (src/botsito/corpus/cuarentena.py en 0fa9c81, `:380-391`) con su
    `_RE_DIA_BARRA_MES`; las otras dos regex no cambian en la rama."""
    t = cu.numeros_a_cifras(cu.normalizar(texto))
    salida = {(cu._MESES_NUM[m], int(d)) for d, m in cu._RE_DIA_DE_MES.findall(t)}
    salida |= {(cu._MESES_NUM[m], int(d)) for m, d in cu._RE_MES_DIA.findall(t)}
    salida |= {(int(m), int(d)) for d, m in RE_DIA_BARRA_MES_MAIN.findall(t)}
    return {(m, d) for m, d in salida if 1 <= m <= 12 and 1 <= d <= 31}


def test_la_rama_no_tapa_menos_que_main(m: ModuleType) -> None:
    """GUARDIA DE REGRESION del superconjunto, no la prueba de que los tests nuevos rompen en main:
    esa es la sonda de la fase 0 repetida sobre el codigo real de main en un clon
    (CUARENTENA-POR-CONDICION-2.md, respuesta del consultor a la PARADA 2, punto 1). Aqui, con las
    regex de main copiadas arriba: todo texto que main tapa lo tapa la rama, y todo par (mes, dia)
    que `fechas_en` sacaba con main lo saca la rama. Y la rama tapa alguno que main no. Si falla,
    solo da recuentos: ningun texto de la bateria se imprime."""
    textos = _bateria()
    n = len(textos)
    assert n > 10_000
    menos = sum(1 for t in textos if RE_FECHA_MAIN.search(t) and not cu._RE_FECHA.search(t))
    assert menos == 0, f"{menos} textos que main tapa y la rama no"
    perdidas = sum(1 for t in textos if _fechas_en_main(t) - cu.fechas_en(t))
    assert perdidas == 0, f"{perdidas} textos en que la rama pierde una fecha de main"
    nuevas = sum(1 for t in textos if cu._RE_FECHA.search(t) and not RE_FECHA_MAIN.search(t))
    assert nuevas > 0
    mas_fechas = sum(1 for t in textos if cu.fechas_en(t) - _fechas_en_main(t))
    assert mas_fechas > 0
    # El solape que obliga al lookahead de `_RE_DIA_BARRA_MES`, con una fecha imposible (el 31 de
    # febrero): sin el, «1/31» se comeria a «31-2», que main si sacaba.
    assert _sin_fechas_posibles(",1/31-2")
    assert _fechas_en_main(",1/31-2") == {(2, 31)} <= cu.fechas_en(",1/31-2")
    assert cu.fechas_en(",1/31-2") - {(2, 31)} == set()  # «1/31»: el mes 31 no es una fecha


@pytest.mark.parametrize("texto", ["el jueves 40 entré", "el lunes, 40", "el 40, domingo"])
def test_un_dia_de_la_semana_con_un_numero_va_a_cuarentena(m: ModuleType, texto: str) -> None:
    assert cu.MOTIVO_DIA in cu.motivos_cuarentena(texto), texto
    assert cu.motivos_cuarentena("el lunes entro poco") == []


def test_backtest_con_una_abreviatura_de_mes(m: ModuleType) -> None:
    assert cu.MOTIVO_BACKTEST in cu.motivos_cuarentena("el backtest de set")
    assert cu.MOTIVO_BACKTEST in cu.motivos_cuarentena("el back test de sep")
    assert cu.motivos_cuarentena("el backtest que hiciste") == []


def test_los_vecinos_van_tambien_a_cuarentena(m: ModuleType) -> None:
    textos = ["uno", "dos", "eso fue en mayo", "tres", "cuatro", "cinco"]
    c = cu.en_cuarentena(textos)
    assert set(c) == {1, 2, 3}
    assert c[2] == [cu.MOTIVO_MES] and c[1] == c[3] == [cu.MOTIVO_VECINO]
    # en los bordes no se sale del rango, y dos seguidos no se pisan los motivos
    assert set(cu.en_cuarentena(["en marzo", "hola"])) == {0, 1}
    assert cu.en_cuarentena(["en marzo", "el 31/02"]) == {0: [cu.MOTIVO_MES], 1: [cu.MOTIVO_FECHA]}


# ----------------------------------------------------------------------------- los codigos


@pytest.mark.parametrize(
    ("texto", "codigo"),
    [
        ("Pregunta A treinta y cinco", "A-35"),
        ("pregunta a 35", "A-35"),
        ("pregunta A-35", "A-35"),
        ("pregunta, A35, la del pivote", "A-35"),
        ("pregunta 35", "A-35"),
        ("pregunta numero 35", "A-35"),
        ("pregunta treinta y cinco", "A-35"),
        ("Pregunta A-46", "A-46"),
        ("pregunta A cuarenta y seis", "A-46"),
        ("pregunta ha veintiuno", "A-21"),
        ("pregunta A treinta", "A-30"),
        ("pregunta A-35 y luego pregunta A-45", "A-45"),  # el ultimo manda
    ],
)
def test_una_pregunta_se_abre_solo_con_pregunta_y_el_codigo(
    m: ModuleType, texto: str, codigo: str
) -> None:
    assert m.codigo_en(texto, VALIDOS) == codigo, texto


@pytest.mark.parametrize(
    "texto",
    [
        "el precio llega a 30",
        "llega a treinta",
        "vamos con la A-35",  # sin «pregunta» delante ya no abre
        "A treinta y cinco",
        "ahora a 35",
        "la a35",
        "lo pongo a 35 puntos",
        "de 20 a 25",
        "voy a una zona",
        "pregunta A-12",  # no esta entre los validos (resuelta)
        "pregunta a 99",
        "pregunta a 35 puntos",
        "el precio a 1.21",
    ],
)
def test_lo_que_no_abre_pregunta(m: ModuleType, texto: str) -> None:
    assert m.codigo_en(texto, VALIDOS) is None, texto


def test_la_trampa_llega_a_30_no_abre_a30_y_fin_de_pregunta_cierra(m: ModuleType) -> None:
    textos = [
        "pregunta A treinta y cinco",  # 0 abre A-35
        "el precio llega a treinta",  # 1 sigue en A-35: la trampa no abre A-30
        "fin de pregunta",  # 2 cierra
        "charla suelta",  # 3 SIN PREGUNTA
        "pregunta A treinta",  # 4 abre A-30
    ]
    lineas, _ = m.lineas_filtradas(_segs(m, textos), VALIDOS)
    assert [ln.pregunta for ln in lineas] == [
        "A-35",
        "A-35",
        m.SIN_PREGUNTA,
        m.SIN_PREGUNTA,
        "A-30",
    ]


def test_la_marco_no_va_a_cuarentena(m: ModuleType) -> None:
    assert cu.motivos_cuarentena("la marco en el alto") == []
    assert cu.en_cuarentena(["pregunta A-35", "la marco en el alto", "y sigo"]) == {}


def test_numeros_a_cifras(m: ModuleType) -> None:
    assert cu.numeros_a_cifras("treinta y cinco") == "35"
    assert cu.numeros_a_cifras("veinticinco y trece") == "25 y 13"
    assert cu.numeros_a_cifras("una zona y un stop") == "una zona y un stop"


# ------------------------------------------------------------------ la version filtrada


def _segs(m: ModuleType, textos: list[str]) -> list[object]:
    return [m.Seg(i * 10_000, i * 10_000 + 9_000, t) for i, t in enumerate(textos)]


def test_la_filtrada_agrupa_por_pregunta_y_no_trae_nada_en_cuarentena(m: ModuleType) -> None:
    textos = [
        "buenas, empezamos",  # 0 SIN PREGUNTA
        "pregunta A-35",  # 1
        "yo lo marco cuando cierra",  # 2
        "respuesta uno sin mes",  # 3 vecino
        "SECRETO eso lo vi en septiembre",  # 4 cuarentena
        "otra cosa inocua",  # 5 vecino
        "sigo con la zona",  # 6
        "pregunta A-21",  # 7
        "limpia es sin mechas",  # 8
        "fin de pregunta",  # 9 SIN PREGUNTA
        "charla final",  # 10
        "pregunta A-35 otra vez",  # 11
        "y otra cosa de la 35",  # 12
    ]
    lineas, cuarentena = m.lineas_filtradas(_segs(m, textos), VALIDOS)
    assert set(cuarentena) == {3, 4, 5}
    texto = m.version_filtrada(lineas, "prueba", m.ORDEN_SESION_03)
    assert "SECRETO" not in texto and "septiembre" not in texto
    assert "respuesta uno" not in texto and "otra cosa inocua" not in texto
    assert "[CUARENTENA 00:30–00:59]" in texto  # los tres segmentos, en un solo bloque
    # orden de la hoja: A-35 antes que A-21, y SIN PREGUNTA al final
    assert texto.index("## A-35") < texto.index("## A-21") < texto.index(f"## {m.SIN_PREGUNTA}")
    bloque_35 = texto.split("## A-35")[1].split("## ")[0]
    assert "[00:20] yo lo marco cuando cierra" in bloque_35
    assert "…" in bloque_35 and "[02:00] y otra cosa de la 35" in bloque_35  # volvio a la A-35
    sin = texto.split(f"## {m.SIN_PREGUNTA}")[1]
    assert "buenas, empezamos" in sin and "charla final" in sin


def test_un_tramo_sin_codigo_es_sin_pregunta(m: ModuleType) -> None:
    lineas, _ = m.lineas_filtradas(_segs(m, ["hola", "que tal", "bien"]), VALIDOS)
    assert {ln.pregunta for ln in lineas} == {m.SIN_PREGUNTA}


def test_el_registro_no_trae_contenido(m: ModuleType) -> None:
    textos = ["pregunta A-35", "SECRETO en mayo", "algo", "pregunta A-46", "otra"]
    lineas, cuarentena = m.lineas_filtradas(_segs(m, textos), VALIDOS)
    registro = "\n".join(m.registro_filtro(lineas, cuarentena, VALIDOS, m.ORDEN_SESION_02))
    assert "SECRETO" not in registro and "mayo" not in registro
    assert "A-35 00:00" in registro and "A-46 00:30" in registro
    assert "A-21" in registro.split("SIN codigo detectado:")[1]


def test_mmss(m: ModuleType) -> None:
    assert m.mmss(0) == "00:00" and m.mmss(61_500) == "01:01" and m.mmss(6_187_000) == "103:07"


# ----------------------------------------------------------------- fuera del repo y rutas


def test_la_salida_nunca_va_dentro_del_repo(m: ModuleType, tmp_path: Path) -> None:
    with pytest.raises(m.SesionError, match="dentro del repositorio"):
        m.fuera_del_repo(RAIZ / "data" / "x.filtrada.md")
    assert m.fuera_del_repo(tmp_path / "x.md") == tmp_path / "x.md"


def test_sin_audio_se_dice(m: ModuleType, tmp_path: Path) -> None:
    (tmp_path / "notas.txt").write_text("x", encoding="utf-8")
    with pytest.raises(m.SesionError, match="no hay ningun audio"):
        m.audios_de(tmp_path)
    with pytest.raises(m.SesionError, match="no existe"):
        m.audios_de(tmp_path / "no-esta")
    audio = tmp_path / "prueba.m4a"
    audio.write_bytes(b"")
    assert m.audios_de(tmp_path) == [audio]


def test_la_cli_se_niega_sin_audio_y_no_escribe(
    m: ModuleType, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert m.main(["--audio", str(tmp_path)]) == 2
    assert "no hay ningun audio" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_la_guarda_de_rutas_es_la_de_siempre(m: ModuleType, tmp_path: Path) -> None:
    from botsito.engine.diagnostico import LIMITE_RUTA_WINDOWS, RutaDemasiadoLargaError

    larga = tmp_path / ("c" * max(1, LIMITE_RUTA_WINDOWS - len(str(tmp_path))))
    with pytest.raises(RutaDemasiadoLargaError):
        m._comprobar_rutas(m.salidas_de(larga / "prueba.m4a").values())


def test_el_orden_es_el_de_la_hoja_con_a46_tras_a21(m: ModuleType) -> None:
    """El orden de la hoja de la sesion 02 TAL COMO SE LLEVO (hoja_preguntas.py, 2026-09-25), con
    A-46 tras A-21. Hasta el 2026-09-29 se comparaba con la hoja viva; desde que la sesion 3 deja
    nueve RESUELTAS (rama trabajo/activar-sesion-03), la hoja viva ya no las lleva, y este orden,
    que agrupa la grabacion de la sesion 02, es historia: se fija aqui, explicito."""
    esperado = [
        "A-35", "A-45", "A-21", "A-46", "A-44", "A-43", "A-24", "A-42",
        "A-26", "A-25", "A-32",
        "A-36", "A-37", "A-29", "A-30", "A-38", "A-47", "A-48", "A-49",
        "A-18", "A-13", "A-31", "A-40", "A-33",
        "A-34", "A-41", "A-39",
    ]  # fmt: skip
    assert list(m.ORDEN_SESION_02) == esperado


# ----------------------------------------------- los codigos de sesion de la hoja 03 (E, S y G)

VALIDOS_03 = (*VALIDOS, "E-1", "E-2", "E-3", "S-1", "G-1", "G-2", "G-3")


@pytest.mark.parametrize(
    ("texto", "codigo"),
    [
        ("Pregunta S uno", "S-1"),
        ("pregunta ese uno", "S-1"),
        ("pregunta es 1", "S-1"),
        ("pregunta G dos", "G-2"),
        ("pregunta ge dos", "G-2"),
        ("pregunta je tres", "G-3"),
        ("pregunta G2", "G-2"),
        ("pregunta E uno", "E-1"),
        ("pregunta, e 3", "E-3"),
        ("pregunta A treinta y cinco", "A-35"),  # sin cambios para las A
        ("pregunta 35", "A-35"),
    ],
)
def test_la_sesion_03_abre_tambien_con_e_s_y_g(m: ModuleType, texto: str, codigo: str) -> None:
    assert m.codigo_en(texto, VALIDOS_03) == codigo, texto


@pytest.mark.parametrize(
    "texto",
    [
        "la pregunta es 1 punto",  # «es» seguido de algo que no es el codigo
        "pregunta es la uno",
        "pregunta g 2 puntos",  # una unidad detras: no es un codigo
        "pregunta s 7",  # no esta en la hoja
        "vamos con la G dos",  # sin «pregunta» delante
    ],
)
def test_lo_que_no_abre_en_la_sesion_03(m: ModuleType, texto: str) -> None:
    assert m.codigo_en(texto, VALIDOS_03) is None, texto


def test_el_orden_es_el_de_la_hoja_de_la_sesion_03(m: ModuleType) -> None:
    """El orden del brief del consultor del 2026-09-29, que agrupa la version filtrada."""
    assert list(m.ORDEN_SESION_03) == [
        "A-47",
        "S-1", "A-34", "A-26", "A-39",
        "A-46", "A-35", "A-45", "A-43", "A-50",
        "A-13", "A-40", "G-1", "G-2", "A-18", "G-3",
        "A-42", "A-44",
        "A-21", "E-1",
        "A-30", "A-31", "E-2", "E-3", "A-41", "A-38", "A-24", "A-25", "A-37",
    ]  # fmt: skip
    assert m.HOJAS["03"] is m.ORDEN_SESION_03
    assert set(m.CODIGOS_DE_SESION_TEXTO["03"]) == {"E-1", "E-2", "E-3", "S-1", "G-1", "G-2", "G-3"}
    presentes = ["A-99", "G-3", m.SIN_PREGUNTA, "S-1", "A-47", "E-9"]
    assert m.orden_de_preguntas(presentes, m.ORDEN_SESION_03) == [
        "A-47", "S-1", "G-3", "A-99", "E-9", m.SIN_PREGUNTA,
    ]  # fmt: skip


def test_los_codigos_de_sesion_llevan_el_texto_de_la_hoja(m: ModuleType) -> None:
    """E-1, E-2 y E-3 no tenian texto en ningun fichero hasta la revision del consultor del
    2026-09-29; aqui se fija el de la hoja de la sesion 03, y que todo codigo tiene uno."""
    textos = m.CODIGOS_DE_SESION_TEXTO["03"]
    assert textos["E-1"] == "tus dos backtests de los mismos días"
    assert textos["E-2"] == "cómo operas los equals"
    assert textos["E-3"] == "cuando la vela cambia de color"
    for sesion, por_codigo in m.CODIGOS_DE_SESION_TEXTO.items():
        assert all(texto.strip() for texto in por_codigo.values()), sesion


# ------------------------------------------------- la hoja de la sesion 04 (S-1 a S-24, por sesion)

ORDEN_04 = [
    "S-1", "S-2", "S-3", "S-4", "S-5", "S-6", "S-22",
    "S-7", "S-8", "S-9", "S-10", "S-11", "S-12", "S-13", "S-14", "S-15", "S-16", "S-17",
    "S-18", "S-20", "S-21", "S-23", "S-24", "S-19",
]  # fmt: skip


def test_el_orden_es_el_de_la_hoja_de_la_sesion_04(m: ModuleType) -> None:
    """El orden del encargo de `trabajo/sesion-04` (docs/sesion-4/HOJA-USADA.md), con todos los
    S-1..S-24 y cada uno con su texto. La sesion en curso ya no es la 04: la fija el test de la
    sesion 05 (`trabajo/hoja-sesion-05`)."""
    assert list(m.ORDEN_SESION_04) == ORDEN_04
    assert m.HOJAS["04"] is m.ORDEN_SESION_04
    assert sorted(m.ORDEN_SESION_04, key=lambda c: int(c[2:])) == [f"S-{n}" for n in range(1, 25)]
    assert set(m.CODIGOS_DE_SESION_TEXTO["04"]) == set(m.ORDEN_SESION_04)


def test_s1_tiene_un_texto_por_sesion_y_la_hoja_03_no_cambia(m: ModuleType) -> None:
    """S-1 existe en la 03 y en la 04 con textos distintos: si los textos fueran un unico
    diccionario, uno pisaria al otro. Y la hoja de la 03 sigue validando y agrupando como antes."""
    assert m.CODIGOS_DE_SESION_TEXTO["03"]["S-1"] == "cómo decide el sesgo del día"
    assert m.CODIGOS_DE_SESION_TEXTO["04"]["S-1"] == (
        "cuándo pones la orden, una vez formado el mínimo (o máximo) en M1"
    )
    assert set(m.CODIGOS_DE_SESION_TEXTO["03"]).isdisjoint({"S-2", "S-7", "S-24"})
    assert set(m.CODIGOS_DE_SESION_TEXTO["04"]).isdisjoint({"E-1", "G-1", "G-3"})


def test_los_codigos_validos_son_los_de_la_hoja_de_cada_sesion(m: ModuleType) -> None:
    v03, v04 = set(m.codigos_validos("03")), set(m.codigos_validos("04"))
    assert {"E-1", "E-2", "E-3", "S-1", "G-1", "G-2", "G-3"} <= v03
    assert not {f"S-{n}" for n in range(2, 25)} & v03
    assert {f"S-{n}" for n in range(1, 25)} <= v04
    assert not {"E-1", "E-2", "E-3", "G-1", "G-2", "G-3"} & v04
    assert v03 - {"E-1", "E-2", "E-3", "S-1", "G-1", "G-2", "G-3"} == v04 - set(ORDEN_04)


@pytest.mark.parametrize(
    ("texto", "codigo"),
    [
        ("pregunta ese siete", "S-7"),
        ("Pregunta S veintidós", "S-22"),
        ("pregunta es 24", "S-24"),
        ("pregunta S diez", "S-10"),
        ("pregunta ese diecinueve", "S-19"),
    ],
)
def test_la_sesion_04_abre_con_ese_y_el_numero(m: ModuleType, texto: str, codigo: str) -> None:
    assert m.codigo_en(texto, (*VALIDOS, *ORDEN_04)) == codigo, texto


def test_la_filtrada_de_la_04_agrupa_con_su_hoja(m: ModuleType) -> None:
    textos = ["pregunta ese uno", "uno", "pregunta ese veintidós", "dos", "pregunta ese siete", "x"]
    lineas, _ = m.lineas_filtradas(_segs(m, textos), m.codigos_validos("04"))
    texto = m.version_filtrada(lineas, "prueba", m.HOJAS["04"])
    assert texto.index("## S-1\n") < texto.index("## S-22") < texto.index("## S-7")
    registro = "\n".join(m.registro_filtro(lineas, {}, m.codigos_validos("04"), m.HOJAS["04"]))
    assert "S-24" in registro.split("SIN codigo detectado:")[1]


# ------------------------------------------------- la hoja de la sesion 05 (S-1 a S-25, por sesion)

PREGUNTAS_05 = RAIZ / "docs" / "sesion-5" / "PREGUNTAS.md"
# El titulo de cada pregunta: la negrita «**S-n. ...**», que en S-1 ocupa dos lineas.
_RE_TITULO = re.compile(r"^\*\*S-(\d+)\. (.+?)\*\*", re.MULTILINE | re.DOTALL)
# El «Titulo» de un recuadro de correccion del 2026-10-21 (S-7 y S-12).
_RE_TITULO_RECUADRO = re.compile(r"^> - \*\*Título:\*\* «(.+?)»", re.MULTILINE)


def _titulos_05() -> dict[str, str]:
    """Los textos que la hoja 05 tiene que llevar, leidos de docs/sesion-5/PREGUNTAS.md: el titulo
    de cada pregunta con la primera letra en minuscula, y el del recuadro en S-7 y S-12."""
    texto = PREGUNTAS_05.read_text(encoding="utf-8")
    titulos = {f"S-{n}": " ".join(t.split()) for n, t in _RE_TITULO.findall(texto)}
    recuadros = _RE_TITULO_RECUADRO.findall(texto)
    assert len(recuadros) == 2, recuadros
    titulos["S-7"], titulos["S-12"] = recuadros
    return {codigo: t[0].lower() + t[1:] for codigo, t in titulos.items()}


def test_la_hoja_05_tiene_los_25_codigos_con_su_texto(m: ModuleType) -> None:
    """S-1 a S-25 en el orden de la hoja, que es el numerico, y cada uno con el titulo de su
    pregunta en docs/sesion-5/PREGUNTAS.md (S-7 y S-12, el de su recuadro de correccion)."""
    assert list(m.ORDEN_SESION_05) == [f"S-{n}" for n in range(1, 26)]
    titulos = _titulos_05()
    assert list(titulos) == list(m.ORDEN_SESION_05)
    assert m.CODIGOS_DE_SESION_TEXTO["05"] == titulos


def test_la_hoja_05_sigue_en_su_sitio(m: ModuleType) -> None:
    """La sesion 5 ya no es la sesion en curso (lo es la 06), y su hoja no cambia."""
    assert m.HOJAS["05"] is m.ORDEN_SESION_05
    assert m.CODIGOS_DE_SESION_TEXTO["05"]["S-14"] == "qué te hace no operar un día o una sesión"


def test_s25_vale_en_la_05_y_no_en_la_04(m: ModuleType) -> None:
    v04, v05 = m.codigos_validos("04"), m.codigos_validos("05")
    assert "S-25" in v05
    assert "S-25" not in v04
    assert m.codigo_en("pregunta ese veinticinco", v05) == "S-25"
    assert m.codigo_en("pregunta ese veinticinco", v04) is None


def test_la_03_y_la_04_no_cambian(m: ModuleType) -> None:
    """Las hojas de las sesiones anteriores agrupan igual que antes de la 05."""
    assert m.HOJAS["03"] is m.ORDEN_SESION_03
    assert m.HOJAS["04"] is m.ORDEN_SESION_04
    assert list(m.ORDEN_SESION_04) == ORDEN_04
    assert m.CODIGOS_DE_SESION_TEXTO["04"]["S-7"] == "con qué reloj empiezas a las 7 en invierno"
    assert m.CODIGOS_DE_SESION_TEXTO["03"]["S-1"] == "cómo decide el sesgo del día"
    textos = ["pregunta ese uno", "uno", "pregunta ese veintidós", "dos", "pregunta ese siete", "x"]
    lineas, _ = m.lineas_filtradas(_segs(m, textos), m.codigos_validos("04"))
    texto = m.version_filtrada(lineas, "prueba", m.HOJAS["04"])
    assert texto.index("## S-1\n") < texto.index("## S-22") < texto.index("## S-7")


def test_la_filtrada_de_la_05_agrupa_con_su_hoja(m: ModuleType) -> None:
    """Con la hoja 05, S-7 va antes que S-22 (en la 04 iba despues) y S-25 abre su pregunta."""
    textos = [
        "pregunta ese veintidós", "a", "pregunta ese siete", "b", "pregunta ese veinticinco", "c",
    ]  # fmt: skip
    lineas, _ = m.lineas_filtradas(_segs(m, textos), m.codigos_validos("05"))
    texto = m.version_filtrada(lineas, "prueba", m.HOJAS["05"])
    assert texto.index("## S-7\n") < texto.index("## S-22") < texto.index("## S-25")


# ------------------------------------------------- la hoja de la sesion 06 (S-1 a S-23, por sesion)

PREGUNTAS_06 = RAIZ / "docs" / "sesion-6" / "PREGUNTAS.md"


def _titulos_06() -> dict[str, str]:
    """Los textos que la hoja 06 tiene que llevar, leidos de docs/sesion-6/PREGUNTAS.md: el titulo
    de cada pregunta (la negrita «**S-n. ...**») con la primera letra en minuscula."""
    texto = PREGUNTAS_06.read_text(encoding="utf-8")
    titulos = {f"S-{n}": " ".join(t.split()) for n, t in _RE_TITULO.findall(texto)}
    return {codigo: t[0].lower() + t[1:] for codigo, t in titulos.items()}


def test_la_hoja_06_tiene_los_23_codigos_con_su_texto(m: ModuleType) -> None:
    """S-1 a S-23 en el orden de la hoja, que es el numerico, y cada uno con el titulo de su
    pregunta en docs/sesion-6/PREGUNTAS.md (S-7 a S-12, «gráfico 1» a «gráfico 6»)."""
    assert list(m.ORDEN_SESION_06) == [f"S-{n}" for n in range(1, 24)]
    titulos = _titulos_06()
    assert list(titulos) == list(m.ORDEN_SESION_06)
    assert m.CODIGOS_DE_SESION_TEXTO["06"] == titulos


def test_la_sesion_en_curso_es_la_06(m: ModuleType) -> None:
    """La hoja por defecto de `--sesion`: la de la sesion 6 (2026-10-28, antes de grabar)."""
    assert m.SESION_EN_CURSO == "06"
    assert m.HOJAS["06"] is m.ORDEN_SESION_06


def test_s24_y_s25_valen_en_la_05_y_no_en_la_06(m: ModuleType) -> None:
    v05, v06 = m.codigos_validos("05"), m.codigos_validos("06")
    assert {"S-24", "S-25"} <= set(v05)
    assert not {"S-24", "S-25"} & set(v06)
    assert m.codigo_en("pregunta ese veintitrés", v06) == "S-23"
    assert m.codigo_en("pregunta ese veinticuatro", v06) is None


def test_la_filtrada_de_la_06_agrupa_con_su_hoja(m: ModuleType) -> None:
    """Con la hoja 06, S-7 (el gráfico 1) va antes que S-13 y S-23 abre su pregunta."""
    textos = [
        "pregunta ese trece", "a", "pregunta ese siete", "b", "pregunta ese veintitrés", "c",
    ]  # fmt: skip
    lineas, _ = m.lineas_filtradas(_segs(m, textos), m.codigos_validos("06"))
    texto = m.version_filtrada(lineas, "prueba", m.HOJAS["06"])
    assert texto.index("## S-7\n") < texto.index("## S-13") < texto.index("## S-23")
