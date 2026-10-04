"""La cuarentena mecanica (desde el 2026-10-01 en `botsito.corpus.cuarentena`) y la segmentacion
por pregunta de `scripts/transcribir_sesion.py`, sobre
texto SINTETICO y sin audio.

Ningun dato de prueba lleva una fecha real de un dia reservado: los meses filtrados van sin dia;
los patrones numericos usan fechas IMPOSIBLES («31/02», «45 del 13», «el jueves 40»); y las fechas
con dia son de abril y agosto, en los casos que NO deben filtrarse."""

from __future__ import annotations

import importlib.util
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
    S-1..S-24 y cada uno con su texto."""
    assert list(m.ORDEN_SESION_04) == ORDEN_04
    assert m.HOJAS["04"] is m.ORDEN_SESION_04
    assert m.SESION_EN_CURSO == "04"
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
