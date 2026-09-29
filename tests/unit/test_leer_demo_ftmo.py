"""El lector de la demo de FTMO (`scripts/leer_demo_ftmo.py`) sobre CSV SINTETICOS con el formato de
`tools/mql5/MedirDemoFTMO.mq5`: la tabla por decision, el desfase por fecha, y que un retcode
inesperado se marca y no se oculta. Ninguna cifra de aqui es de FTMO: son inventadas."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

import pytest

RAIZ = Path(__file__).resolve().parents[2]
CABECERA = (
    "version_script,fila,medicion,responde,clave,valor,retcode,retcode_texto,colocada,tipo_orden,"
    "precio_pedido,bid,ask,precio_resultado,distancia_puntos,hora_servidor,hora_gmt,nota"
)


def _cargar() -> ModuleType:
    nombre = "leer_demo_ftmo"
    if nombre in sys.modules:
        return sys.modules[nombre]
    spec = importlib.util.spec_from_file_location(nombre, RAIZ / "scripts" / f"{nombre}.py")
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def _linea(n: int, medicion: str, clave: str, valor: str = "", retcode: str = "",
           texto: str = "", colocada: str = "", tipo: str = "", pedido: str = "",
           resultado: str = "", distancia: str = "", servidor: str = "2030-01-15 10:00:00",
           gmt: str = "2030-01-15 08:00:00", nota: str = "") -> str:  # fmt: skip
    campos = [
        '"1.0"', str(n), f'"{medicion}"', '"x"', f'"{clave}"', f'"{valor}"', retcode, f'"{texto}"',
        f'"{colocada}"', f'"{tipo}"', pedido, "1.10000", "1.10002", resultado, f'"{distancia}"',
        f'"{servidor}"', f'"{gmt}"', f'"{nota}"',
    ]  # fmt: skip
    return ",".join(campos)


def _csv(ruta: Path, lineas: list[str]) -> Path:
    ruta.write_text(CABECERA + "\r\n" + "\r\n".join(lineas) + "\r\n", encoding="ascii")
    return ruta


def _completo(retcode_lado: str = "10015", texto_lado: str = "INVALID_PRICE",
              servidor: str = "2030-01-15 10:00:00", gmt: str = "2030-01-15 08:00:00",
              desfase: str = "120") -> list[str]:  # fmt: skip
    ls = [
        _linea(1, "1_especificacion", "stops_level_puntos", "0"),
        _linea(2, "1_especificacion", "digits", "5"),
        _linea(3, "2_reloj", "desfase_servidor_gmt_min", desfase, servidor=servidor, gmt=gmt),
        _linea(
            4,
            "3_lado_equivocado",
            "sell_stop_por_encima_del_bid",
            "",
            retcode_lado,
            texto_lado,
            "no",
            "sell_stop",
            "1.10020",
        ),  # fmt: skip
        _linea(
            5,
            "4_distancias",
            "nivel_exacto_sell_stop",
            "",
            "10009",
            "DONE",
            "si",
            "sell_stop",
            "1.10000",
            "1.10000",
            "0",
        ),  # fmt: skip
        _linea(
            6,
            "5_modificacion",
            "modificar_al_lado_equivocado_sell_stop",
            "",
            "10015",
            "INVALID_PRICE",
            "si_sin_cambios",
            "sell_stop",
            "1.10020",
        ),  # fmt: skip
        _linea(
            7,
            "6_comision",
            "apertura_compra_mercado",
            "0.00",
            "10009",
            "DONE",
            "llenada",
            "buy",
            "1.10002",
            "1.10003",
            "1.0",
        ),  # fmt: skip
        _linea(
            8,
            "6_comision",
            "cierre_compra_mercado",
            "-5.00",
            "10009",
            "DONE",
            "llenada",
            "sell",
            "1.10000",
            "1.10000",
            "0.0",
        ),  # fmt: skip
        _linea(
            9,
            "7_llenado_stop",
            "buy_stop_llenado",
            "1.0",
            "0",
            "SIN_RESPUESTA",
            "llenada",
            "buy_stop",
            "1.10004",
            "1.10005",
            "2",
        ),  # fmt: skip
        _linea(10, "limpieza", "quedan_abiertas_al_terminar", "0"),
        _linea(11, "9_fin", "terminado", "completo"),
    ]
    return ls


def test_la_tabla_de_un_fichero_completo(tmp_path: Path) -> None:
    m = _cargar()
    texto = m.informe(
        m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20300115_100000.csv", _completo())])
    )
    assert "| ADR-0057 d5 · A-27 | stops level (puntos) | 0 |" in texto
    assert "| ADR-0057 d2 · d3 | sell stop por encima del bid | no (10015 INVALID_PRICE) |" in texto
    assert "sell_stop si (10009 DONE)" in texto  # el nivel exacto, aceptado
    assert (
        "| ADR-0057 d3 | modificar una sell stop al lado equivocado | si_sin_cambios (10015 "
        in texto
    )
    assert (
        "| ADR-0057 d1 · DN-3 | cierre a mercado | comision -5.00; deslizamiento 0.0 puntos |"
        in texto
    )
    assert (
        "| ADR-0057 d1 | llenado de una buy stop: precio - nivel | 1.0 puntos (nivel 1.10004, "
        in texto
    )
    assert "| 2030-01-15 | 120 | 2030-01-15 10:00:00 | 2030-01-15 08:00:00 |" in texto
    assert "## Retcodes INESPERADOS: esas filas no miden lo que dicen\n\n- ninguno" in texto
    assert "- ninguno: el script no dejo nada abierto" in texto


def test_un_retcode_inesperado_se_marca_y_no_se_oculta(tmp_path: Path) -> None:
    """CLIENT_DISABLES_AT (10027: el trading algoritmico apagado) no dice nada del lado
    equivocado: la celda lo marca y la lista de inesperados lo nombra."""
    m = _cargar()
    ruta = _csv(
        tmp_path / "MedirDemoFTMO_20300115_100000.csv", _completo("10027", "CLIENT_DISABLES_AT")
    )
    texto = m.informe(m.ficheros_de([ruta]))
    assert "| sell stop por encima del bid | INESPERADO: no (10027 CLIENT_DISABLES_AT) |" in texto
    assert (
        "- MedirDemoFTMO_20300115_100000.csv · 3_lado_equivocado · sell_stop_por_encima_del_bid: "
        "10027 CLIENT_DISABLES_AT"
    ) in texto
    assert "- ninguno\n" not in texto.split("## Retcodes INESPERADOS")[1].split("## Avisos")[0]


def test_varios_ficheros_dan_el_desfase_por_fecha(tmp_path: Path) -> None:
    m = _cargar()
    verano = _completo(servidor="2030-10-21 11:00:00", gmt="2030-10-21 08:00:00", desfase="180")
    invierno = _completo(servidor="2030-11-04 10:00:00", gmt="2030-11-04 08:00:00", desfase="120")
    a = _csv(tmp_path / "MedirDemoFTMO_20301021_100000.csv", verano)
    b = _csv(tmp_path / "MedirDemoFTMO_20301104_100000.csv", invierno)
    texto = m.informe(m.ficheros_de([tmp_path]))  # una carpeta: todos sus CSV del script
    assert "| 2030-10-21 | 180 |" in texto
    assert "| 2030-11-04 | 120 |" in texto
    assert "| stops level (puntos) | 0 | 0 |" in texto
    assert texto.index(a.name) < texto.index(b.name)


def test_lo_que_queda_abierto_y_un_corte_se_avisan(tmp_path: Path) -> None:
    m = _cargar()
    lineas = [ln for ln in _completo() if '"terminado"' not in ln]
    lineas = [ln.replace('"quedan_abiertas_al_terminar","0"', '"quedan_abiertas_al_terminar","1"')
              for ln in lineas]  # fmt: skip
    texto = m.informe(m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20300115_100000.csv", lineas)]))
    assert "SIN LA FILA DE FIN (cortado)" in texto
    assert "quedan_abiertas_al_terminar = 1" in texto


def test_un_csv_que_no_es_del_script_se_rechaza(tmp_path: Path) -> None:
    m = _cargar()
    ruta = tmp_path / "MedirDemoFTMO_20300115_100000.csv"
    ruta.write_text("a,b,c\n1,2,3\n", encoding="ascii")
    with pytest.raises(m.LecturaError, match="cabecera"):
        m.ficheros_de([ruta])
    (tmp_path / "vacia").mkdir()
    with pytest.raises(m.LecturaError, match="ningun"):
        m.ficheros_de([tmp_path / "vacia"])
    with pytest.raises(m.LecturaError, match="no existe"):
        m.ficheros_de([tmp_path / "no_esta.csv"])
