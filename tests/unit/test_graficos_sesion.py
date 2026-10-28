"""`scripts/graficos_sesion.py` (rama `trabajo/barrido-sesion-6`, D6 g del encargo y decision 5 del
consultor): cada test rompe a proposito una condicion de D6 y llega a la asercion que la fija.

DATOS SINTETICOS: velas inventadas de 2030, con una construccion de prueba de enero y agosto de 2030
(meses libres: ningun dato forma una fecha posible de un mes reservado; leccion B1 de
`trabajo/cuarentena-por-condicion-2`). Ningun test lee velas reales ni el anexo de la corrida."""

from __future__ import annotations

import ast
import importlib.util
import re
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from botsito.data.velas import a_minuto
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import Vela

RAIZ = Path(__file__).resolve().parents[2]
GUION = RAIZ / "scripts" / "graficos_sesion.py"
CONSTRUCCION = {"2030-01": (2, 30), "2030-08": (2, 31)}


@pytest.fixture(scope="module")
def g() -> ModuleType:
    nombre = "graficos_sesion"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, GUION)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _anclaje() -> HoraLocal:
    return HoraLocal("17:00", "America/New_York")


def _velas(desde: datetime, hasta: datetime) -> list[Vela]:
    """M1 sinteticas de [desde, hasta), en zigzag alrededor de 1.10000."""
    salida = []
    t = desde
    i = 0
    while t < hasta:
        base = 110000 + (i % 40) - 20
        cierre = base + (1 if i % 2 else -1)
        salida.append(
            Vela(a_minuto(t), Puntos(base), Puntos(base + 3), Puntos(base - 3), Puntos(cierre), 1)
        )
        t += timedelta(minutes=1)
        i += 1
    return salida


def _cargador(extra_tras_corte: int = 0) -> Callable[[int, int], tuple[Sequence[Vela], int]]:
    """Un lector como el de la API: las M1 sinteticas de [desde, hasta); con `extra_tras_corte`,
    devuelve ademas velas posteriores (lo que el guion tiene que rechazar)."""

    def cargar(desde: int, hasta: int) -> tuple[Sequence[Vela], int]:
        inicio = datetime(1970, 1, 1, tzinfo=UTC) + timedelta(minutes=desde)
        fin = datetime(1970, 1, 1, tzinfo=UTC) + timedelta(minutes=hasta + extra_tras_corte)
        return _velas(inicio, fin), 100000

    return cargar


def _orden(g: ModuleType, dia: date, hh: int, mm: int) -> Any:
    return g.Orden(datetime(dia.year, dia.month, dia.day, hh, mm, 59, 999000, tzinfo=UTC), 110005)


# ------------------------------------------------------------------- a) negar por defecto


def test_un_dia_fuera_de_la_construccion_sale_con_error(g: ModuleType) -> None:
    dia = date(2030, 1, 1)  # fuera: la construccion de prueba de enero empieza el 2
    pedido = g.Pedido(dia, "11-15")
    with pytest.raises(g.GraficoError, match="no es de construccion"):
        g.preparar(pedido, _orden(g, dia, 12, 30), _cargador(), _anclaje(), CONSTRUCCION, set())


def test_un_dia_en_casos_ocultos_sale_con_error(g: ModuleType) -> None:
    dia = date(2030, 8, 14)
    pedido = g.Pedido(dia, "11-15")
    with pytest.raises(g.GraficoError, match="casos_ocultos"):
        g.preparar(pedido, _orden(g, dia, 11, 30), _cargador(), _anclaje(), CONSTRUCCION, {(8, 14)})


def test_la_ventana_se_recorta_antes_de_un_dia_no_permitido(g: ModuleType) -> None:
    """El 2030-08-03: la H4 empezaria el 30 de julio, fuera; y el 1 de agosto tampoco es de la
    construccion de prueba. Ninguna vela dibujada toca un minuto no permitido, en Madrid ni en
    UTC."""
    dia = date(2030, 8, 3)
    graf = g.preparar(
        g.Pedido(dia, "07-11"), _orden(g, dia, 5, 40), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    for velas in (graf.h4, graf.m15, graf.m1):
        for v in velas:
            assert g.permitido(int(v.inicio), CONSTRUCCION, set())
    primera = datetime(1970, 1, 1, tzinfo=UTC) + timedelta(minutes=int(graf.h4[0].inicio))
    assert primera >= datetime(2030, 8, 2, tzinfo=UTC)
    # y la H4 que empezaria antes del recorte, a medias, no se dibuja
    assert all(v.inicio >= graf.h4[0].inicio for v in graf.h4)


def test_el_recorte_empieza_en_el_primer_minuto_permitido_en_los_dos_relojes(
    g: ModuleType,
) -> None:
    """El recorte, solo: la ventana pedida empieza el 1 de agosto (fuera de la construccion de
    prueba); las 00:00 de Madrid del 2 son aun el 1 en UTC, asi que empieza a las 00:00 UTC del 2.
    Rompe por aqui, y no en la ultima puerta de `preparar`, si el recorte deja de recortar."""
    desde = a_minuto(datetime(2030, 8, 1, tzinfo=UTC))
    corte = a_minuto(datetime(2030, 8, 3, 5, 40, tzinfo=UTC))
    assert g.recorte(desde, corte, CONSTRUCCION, set()) == a_minuto(
        datetime(2030, 8, 2, tzinfo=UTC)
    )
    tras_el_oculto = a_minuto(datetime(2030, 8, 3, tzinfo=UTC))
    assert g.recorte(desde, corte, CONSTRUCCION, {(8, 2)}) == tras_el_oculto


def test_un_dia_oculto_dentro_de_la_ventana_la_recorta(g: ModuleType) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION,
        {(8, 18)},
    )  # fmt: skip
    for velas in (graf.h4, graf.m15, graf.m1):
        for v in velas:
            local = datetime(1970, 1, 1, tzinfo=UTC) + timedelta(minutes=int(v.inicio))
            assert local.date() > date(2030, 8, 18)


# ------------------------------------------------------------------- c) el corte


def test_ninguna_vela_pasa_del_corte(g: ModuleType) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    assert graf.m1[-1].inicio == graf.corte
    for velas in (graf.h4, graf.m15, graf.m1):
        assert max(int(v.inicio) for v in velas) <= graf.corte


def test_un_lector_que_devuelve_velas_tras_el_corte_hace_salir_con_error(g: ModuleType) -> None:
    dia = date(2030, 8, 20)
    with pytest.raises(g.GraficoError, match="fuera de la ventana"):
        g.preparar(
            g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(extra_tras_corte=30),
            _anclaje(), CONSTRUCCION, set(),
        )  # fmt: skip


def test_ningun_elemento_del_svg_cae_a_la_derecha_del_corte(g: ModuleType) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    limite = g.ANCHO - g.MARGEN_DER  # el borde derecho de cada panel ES el corte
    for marcado in (False, True):
        texto = g.svg(graf, marcado)
        velas = re.findall(r'<rect class="vela" x="([\d.]+)" [^>]*width="([\d.]+)"', texto)
        assert len(velas) == len(graf.h4) + len(graf.m15) + len(graf.m1)
        assert all(float(x) + float(w) <= limite + 1e-6 for x, w in velas)
        lineas = re.findall(r"<line [^>]*>", texto)
        assert lineas
        for linea in lineas:
            for x in re.findall(r'\bx[12]="([\d.]+)"', linea):
                assert float(x) <= limite + 1e-6, linea
        # a la derecha del corte solo hay etiquetas de precio (texto), ninguna vela ni linea
        fuera = [float(x) for x in re.findall(r'<text x="([\d.]+)"', texto) if float(x) > limite]
        assert len(fuera) == 15  # cinco precios por panel


# ------------------------------------------------------------------- d) sin fechas


@pytest.mark.parametrize("texto", ["2030-08-15", "15/08", "15-08", "en agosto", "January", "Enero"])
def test_la_comprobacion_de_fechas_caza_cada_forma(g: ModuleType, texto: str) -> None:
    assert g.lleva_fecha(texto)


@pytest.mark.parametrize("texto", ["1.10005", "07:00", "14:35", "H4", "M15", "M1"])
def test_las_horas_y_los_precios_no_son_fechas(g: ModuleType, texto: str) -> None:
    assert not g.lleva_fecha(texto)


def test_los_svg_y_sus_nombres_no_llevan_fecha_ni_metadatos(g: ModuleType, tmp_path: Path) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    escritos = g.escribir([graf], tmp_path / "salida", RAIZ)
    svgs = [p for p in escritos if p.suffix == ".svg"]
    assert sorted(p.name for p in svgs) == ["grafico-1-limpio.svg", "grafico-1-marcado.svg"]
    for p in svgs:
        texto = p.read_text(encoding="utf-8")
        assert not g.lleva_fecha(p.name)
        assert not g.lleva_fecha(texto)
        for prohibido in ("<!--", "<title", "<metadata", "2030"):
            assert prohibido not in texto
        assert ">H4<" in texto and ">M15<" in texto and ">M1<" in texto
    # la marcada es la limpia mas UNA linea, en el punto
    limpio = (tmp_path / "salida" / "grafico-1-limpio.svg").read_text(encoding="utf-8")
    marcado = (tmp_path / "salida" / "grafico-1-marcado.svg").read_text(encoding="utf-8")
    sobra = [linea for linea in marcado.splitlines() if linea not in limpio.splitlines()]
    assert len(sobra) == 1 and 'class="punto"' in sobra[0]
    # la clave si lleva el dia: es la clave, no se ensena
    assert "2030-08-20" in (tmp_path / "salida" / "clave.txt").read_text(encoding="utf-8")


def test_un_svg_con_fecha_no_se_escribe(
    g: ModuleType, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    monkeypatch.setattr(g, "_precio", lambda puntos, escala: "2030-08-20")
    with pytest.raises(g.GraficoError, match="fecha"):
        g.escribir([graf], tmp_path / "salida", RAIZ)
    assert not (tmp_path / "salida").exists()


# ------------------------------------------------------------------- f) la raiz


def test_la_raiz_no_puede_estar_dentro_del_repo(g: ModuleType) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    dentro = RAIZ / "docs" / "sesion-6-graficos-no-debe-existir"
    with pytest.raises(g.GraficoError, match="dentro del repositorio"):
        g.escribir([graf], dentro, RAIZ)
    assert not dentro.exists()


def test_no_pisa_una_salida_que_ya_existe(g: ModuleType, tmp_path: Path) -> None:
    dia = date(2030, 8, 20)
    graf = g.preparar(
        g.Pedido(dia, "11-15"), _orden(g, dia, 10, 5), _cargador(), _anclaje(), CONSTRUCCION, set()
    )
    g.escribir([graf], tmp_path, RAIZ)
    with pytest.raises(g.GraficoError, match="ya existe"):
        g.escribir([graf], tmp_path, RAIZ)


# ------------------------------------------------------- b) el guion no recorre carpetas


def test_el_guion_no_recorre_carpetas_ni_usa_la_palabra_vetada() -> None:
    arbol = ast.parse(GUION.read_text(encoding="utf-8"))
    vetadas = {"glob", "rglob", "iterdir", "listdir", "scandir", "walk"}
    usadas = {
        n.attr if isinstance(n, ast.Attribute) else n.id
        for n in ast.walk(arbol)
        if isinstance(n, (ast.Attribute, ast.Name))
    }
    assert not usadas & vetadas
    nombres = {n.id for n in ast.walk(arbol) if isinstance(n, ast.Name)} | {
        a.arg for n in ast.walk(arbol) if isinstance(n, ast.FunctionDef) for a in n.args.args
    }
    assert not any("crudo" in x for x in nombres)


# ------------------------------------------------------------------- la orden del anexo


def test_la_primera_orden_de_la_sesion_con_canceladas(g: ModuleType) -> None:
    resto = "| 1 | 1 | 1 | 1 | 0.5 | 1 | ninguno"
    texto = "\n".join(
        [
            "[X] ### Ordenes (dia | sesion | id | colocada UTC | precio | ... | punto | caja 1)",
            "[X] 2030-08-20 | 11-15 | o2 | 2030-08-20T10:06:59.999000+00:00 | 1.10010 | llenada"
            f" | - | x {resto} | 110010@1 | 1.10040",
            "[X] 2030-08-20 | 11-15 | o1 | 2030-08-20T10:05:59.999000+00:00 | 1.10005 | cancelada"
            f" | x | y {resto} | 110005@1 | 1.10030",
            "[X] ### Ordenes no enviadas por el bot (dia | sesion | instante UTC | zona | motivo)",
            "[X] 2030-08-20 | 11-15 | o0 | 2030-08-20T09:00:59.999000+00:00 | 1.10000 | x"
            " | 110000@1 | 1.1",
        ]
    )
    ordenes = g.primeras_ordenes(texto)
    o = ordenes[("2030-08-20", "11-15")]
    assert o.punto == 110005
    assert o.colocada.minute == 5
