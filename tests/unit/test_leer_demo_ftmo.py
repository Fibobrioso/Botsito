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
           gmt: str = "2030-01-15 08:00:00", nota: str = "",
           version: str = "1.0") -> str:  # fmt: skip
    campos = [
        f'"{version}"', str(n), f'"{medicion}"', '"x"', f'"{clave}"', f'"{valor}"', retcode,
        f'"{texto}"', f'"{colocada}"', f'"{tipo}"', pedido, "1.10000", "1.10002", resultado,
        f'"{distancia}"',
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


def _version_1_1(apertura: str = "-3.00", nota_volumen: str = "") -> list[str]:
    """El CSV de la 1.1 (ADR-0071): el paso 6 escribe sus lotes en `volumen_comision` y la
    observacion del llenado lleva OBSERVACION. Cifras inventadas."""
    ls = [
        ln.replace('"1.0"', '"1.1"', 1)
        for ln in _completo()
        if '"apertura_compra_mercado"' not in ln
        and '"cierre_compra_mercado"' not in ln
        and '"buy_stop_llenado"' not in ln
    ]
    ls.insert(-2, _linea(20, "6_comision", "volumen_comision", "1.00", nota=nota_volumen,
                         version="1.1"))  # fmt: skip
    if apertura == "no_abre":
        ls.insert(-2, _linea(21, "6_comision", "apertura_compra_mercado", "no_abre",
                             nota=nota_volumen, version="1.1"))  # fmt: skip
    else:
        ls.insert(-2, _linea(21, "6_comision", "apertura_compra_mercado", apertura, "10009",
                             "DONE", "llenada", "buy", "1.10002", "1.10003", "1.0",
                             version="1.1"))  # fmt: skip
        ls.insert(-2, _linea(22, "6_comision", "cierre_compra_mercado", "-3.00", "10009", "DONE",
                             "llenada", "sell", "1.10000", "1.10000", "0.0",
                             version="1.1"))  # fmt: skip
    ls.insert(-2, _linea(23, "7_llenado_stop", "buy_stop_llenado", "1.0", "0", "OBSERVACION",
                         "llenada", "buy_stop", "1.10004", "1.10005", "2",
                         version="1.1"))  # fmt: skip
    return ls


def test_un_csv_1_1_da_los_lotes_del_paso_6_y_la_observacion(tmp_path: Path) -> None:
    m = _cargar()
    ruta = _csv(tmp_path / "MedirDemoFTMO_20301027_100000.csv", _version_1_1())
    filas = m.ficheros_de([ruta])
    texto = m.informe(filas)
    assert "- MedirDemoFTMO_20301027_100000.csv: completo (script 1.1)" in texto
    assert "| FTMO-REGLAS R12 | lotes de la compra a mercado | 1.00 |" in texto
    assert (
        "| ADR-0057 d1 · DN-3 | compra a mercado | comision -3.00; deslizamiento 1.0 puntos |"
        in texto
    )
    assert "| ADR-0057 d1 · DN-3 | cierre a mercado | comision -3.00;" in texto
    observacion = next(f for f in filas[ruta.name] if f.clave == "buy_stop_llenado")
    assert observacion.retcode_texto == "OBSERVACION" and not m.es_inesperado(observacion)
    assert "## Retcodes INESPERADOS: esas filas no miden lo que dicen\n\n- ninguno" in texto


def test_un_csv_1_1_sin_margen_no_abre_y_lo_dice(tmp_path: Path) -> None:
    m = _cargar()
    nota = "margen libre insuficiente: margen necesario 3700.00; margen libre 100.00"
    ruta = _csv(
        tmp_path / "MedirDemoFTMO_20301027_100000.csv",
        _version_1_1(apertura="no_abre", nota_volumen=nota),
    )
    texto = m.informe(m.ficheros_de([ruta]))
    assert f"| ADR-0057 d1 · DN-3 | compra a mercado | no abrio: {nota} |" in texto
    assert "| ADR-0057 d1 · DN-3 | cierre a mercado | sin medir |" in texto
    assert "## Retcodes INESPERADOS: esas filas no miden lo que dicen\n\n- ninguno" in texto


def test_la_1_0_se_sigue_leyendo_con_la_etiqueta_nueva(tmp_path: Path) -> None:
    """La 1.0 (la ejecucion 1) escribia SIN_RESPUESTA en la observacion y no escribia sus lotes:
    usaba el volumen minimo del simbolo. El lector da OBSERVACION y el volumen minimo."""
    m = _cargar()
    lineas = [*_completo()]
    lineas.insert(2, _linea(12, "1_especificacion", "volumen_min", "0.01"))
    ruta = _csv(tmp_path / "MedirDemoFTMO_20300115_100000.csv", lineas)
    filas = m.ficheros_de([ruta])
    texto = m.informe(filas)
    assert "completo (script 1.0)" in texto
    assert "| lotes de la compra a mercado | 0.01 (la 1.0 usa el volumen minimo) |" in texto
    observacion = next(f for f in filas[ruta.name] if f.clave == "buy_stop_llenado")
    assert observacion.retcode_texto == "OBSERVACION"


def test_otra_version_o_una_mezcla_se_rechazan(tmp_path: Path) -> None:
    m = _cargar()
    otra = [ln.replace('"1.0"', '"2.0"', 1) for ln in _completo()]
    with pytest.raises(m.LecturaError, match="version_script '2.0'"):
        m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20300115_100000.csv", otra)])
    mezcla = [*_completo()[:-1], _linea(11, "9_fin", "terminado", "completo", version="1.1")]
    with pytest.raises(m.LecturaError, match="mezcla versiones"):
        m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20300115_100001.csv", mezcla)])


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


# --- 1.2 (rama trabajo/margen-pendiente): el paso 8, con la regla de la respuesta del consultor a
# la PARADA (MARGEN-PENDIENTE.md, 2026-10-31). Cifras inventadas, del tamano de las de la prueba.

# La salida del lector de main sobre los CSV sinteticos 1.0 y 1.1 de arriba (y sobre una carpeta con
# los dos), medida con el lector de main antes de cambiarlo (MARGEN-PENDIENTE.md, fase 1): con la
# 1.2 en VERSIONES, un 1.0 o un 1.1 tienen que dar EXACTAMENTE lo mismo.
SALIDA_MAIN_SHA256 = {
    "1_0": "a02029b8a0623907d4f534a5e535781c21e8f48bb3a9a0741257aaed09db114c",
    "1_1": "f61f234c8e916029c3d6e805a17c5b77d9a7cb25dbd7d02b1ec7b772a09cccbb",
    "carpeta": "5f487f6f24777719e4543f92e3473dd7280da2921d52b6b9256bdce1926648ef",
}


def test_un_1_0_y_un_1_1_dan_la_salida_de_main_byte_a_byte(tmp_path: Path) -> None:
    import hashlib

    m = _cargar()
    a = _csv(tmp_path / "MedirDemoFTMO_20300115_100000.csv", _completo())
    b = _csv(tmp_path / "MedirDemoFTMO_20301027_100000.csv", _version_1_1())
    for nombre, rutas in (("1_0", [a]), ("1_1", [b]), ("carpeta", [tmp_path])):
        texto = m.informe(m.ficheros_de(rutas))
        assert "Paso 8" not in texto
        assert hashlib.sha256(texto.encode("utf-8")).hexdigest() == SALIDA_MAIN_SHA256[nombre], (
            nombre
        )


def _p8(n: int, clave: str, valor: str = "", retcode: str = "", texto: str = "",
        colocada: str = "", tipo: str = "", pedido: str = "", resultado: str = "",
        nota: str = "") -> str:  # fmt: skip
    return _linea(n, "8_margen", clave, valor, retcode, texto, colocada, tipo, pedido, resultado,
                  nota=nota, version="1.2")  # fmt: skip


def _m2(libre_despues: str = "97730.00", margen_despues: str = "2270.00",
        orden: str = "2270.00", mercado: str = "2250.00") -> list[str]:  # fmt: skip
    """M2 con 100000 de libre antes: por defecto el libre baja 2270, lo calculado a la orden."""
    return [
        _p8(40, "m2_colocar", "0.61", "10008", "PLACED", "si", "buy_stop", "1.12623", "1.12623"),
        _p8(41, "m2_margen_antes", "0.00"),
        _p8(42, "m2_margen_despues", margen_despues),
        _p8(43, "m2_libre_antes", "100000.00"),
        _p8(44, "m2_libre_despues", libre_despues),
        _p8(45, "m2_inicial_antes", "0.00"),
        _p8(46, "m2_inicial_despues", "2270.00"),
        _p8(47, "m2_calculado_orden", orden),
        _p8(48, "m2_calculado_mercado", mercado),
    ]


def _m4(resultado: str = "llenada", viva: str = "si", deal: str = "21.50",
        estado: str = "ORDER_STATE_REJECTED", comentario: str = "[no money]",
        libre_tras_ocupar: str = "74000.00", limite: str = "0.00") -> list[str]:  # fmt: skip
    """M4 por la via de la posicion: S de 21.50 lotes (margen 80000), ocupacion de 6.72."""
    ls = [
        _p8(60, "p8_volumen_limite", limite),
        _p8(61, "m4_ocupacion", "posicion"),
        _p8(62, "m4_volumen_stop", "21.50"),
        _p8(63, "m4_volumen_ocupacion", "6.72"),
        _p8(64, "m4_libre_antes_stop", "100000.00"),
        _p8(65, "m4_libre_tras_stop", "100000.00"),
        _p8(66, "m4_libre_tras_ocupar", libre_tras_ocupar),
        _p8(67, "m4_margen_stop", "80000.00"),
        _p8(68, "m4_ocupacion_viva", viva, nota="ticket 123"),
        _p8(68, "m4_libre_al_resolver", "73950.00"),
    ]
    if resultado == "llenada":
        ls += [
            _p8(
                69,
                "m4_resultado",
                "llenada",
                "0",
                "OBSERVACION",
                "llenada",
                "buy_stop",
                "1.11633",
                "1.11634",
            ),  # fmt: skip
            _p8(70, "m4_volumen_deal", deal),
        ]
    elif resultado == "sin_deal":
        ls += [
            _p8(69, "m4_resultado", "sin_deal", "0", "OBSERVACION", "no", "buy_stop", "1.11633"),
            _p8(70, "m4_estado", estado),
            _p8(71, "m4_comentario", comentario),
            _p8(72, "m4_motivo", "ORDER_REASON_EXPERT"),
        ]
    else:
        ls.append(
            _p8(69, "m4_resultado", resultado, "0", "OBSERVACION", "no", "buy_stop", "1.11633")
        )
    return ls


def _version_1_2(paso_8: list[str] | None = None) -> list[str]:
    """Un 1.2: lo de la 1.1 con la version nueva y, antes del fin, las filas del paso 8."""
    ls = [ln.replace('"1.1"', '"1.2"', 1) for ln in _version_1_1()]
    filas = paso_8 if paso_8 is not None else [*_m2(), *_m4()]
    ls[-2:-2] = [*filas, _p8(99, "p8_fin", "hecho")]
    return ls


def _paso_8(tmp_path: Path, filas: list[str]) -> str:
    m = _cargar()
    texto: str = m.informe(
        m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", _version_1_2(filas))])
    )
    return texto.split("## Paso 8", 1)[1].split("## Retcodes INESPERADOS", 1)[0]


def _respuesta(seccion: str, medida: str) -> str:
    return next(ln for ln in seccion.splitlines() if ln.startswith(f"- {medida} ·"))


def test_un_1_2_sale_en_su_seccion_y_no_en_la_tabla(tmp_path: Path) -> None:
    m = _cargar()
    ruta = _csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", _version_1_2())
    texto = m.informe(m.ficheros_de([ruta]))
    assert "- MedirDemoFTMO_20301102_100000.csv: completo (script 1.2)" in texto
    tabla = texto.split("## Decision a decision", 1)[1].split("## A-28", 1)[0]
    assert "M1" not in tabla and "margen" not in tabla
    assert "## Paso 8: cuando comprueba MT5 el margen de una pendiente stop" in texto
    assert texto.index("## Paso 8") < texto.index("## Retcodes INESPERADOS")


def test_una_carpeta_con_un_1_1_y_un_1_2_se_lee_y_el_paso_8_solo_nombra_el_1_2(
    tmp_path: Path,
) -> None:
    m = _cargar()
    _csv(tmp_path / "MedirDemoFTMO_20301029_100000.csv", _version_1_1())
    _csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", _version_1_2())
    texto = m.informe(m.ficheros_de([tmp_path]))
    assert "(script 1.1)" in texto and "(script 1.2)" in texto
    seccion = texto.split("## Paso 8", 1)[1]
    assert "### MedirDemoFTMO_20301102_100000.csv" in seccion
    assert "### MedirDemoFTMO_20301029_100000.csv" not in seccion


def test_un_1_2_con_el_paso_8_desactivado_lo_dice(tmp_path: Path) -> None:
    m = _cargar()
    ls = [ln.replace('"1.1"', '"1.2"', 1) for ln in _version_1_1()]
    ls[-2:-2] = [_p8(99, "p8_fin", "desactivado")]
    texto = m.informe(m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", ls)]))
    assert "- paso 8 desactivado (InpMedirMargen = false)" in texto
    assert "M1 ·" not in texto


def test_un_paso_8_detenido_por_un_limpiar_lo_dice(tmp_path: Path) -> None:
    """El script para el paso 8 si un Limpiar no deja la cuenta vacia (revisor, b1)."""
    m = _cargar()
    ls = [ln.replace('"1.1"', '"1.2"', 1) for ln in _version_1_1()]
    nota = "un Limpiar no dejo la cuenta vacia: el paso 8 no siguio"
    ls[-2:-2] = [
        _p8(30, "m1_colocar", "26.88", "10019", "NO_MONEY", "no", "buy_stop", "1.12623"),
        _linea(31, "limpieza", "quedan_abiertas_tras_m1", "1", version="1.2"),
        _p8(99, "p8_fin", "detenido", nota=nota),
    ]
    texto = m.informe(m.ficheros_de([_csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", ls)]))
    assert f"- PASO 8 DETENIDO: {nota}" in texto
    assert "- M2 · una stop viva carga margen, y a que precio: sin medir" in texto
    assert "quedan_abiertas_tras_m1 = 1" in texto  # y el aviso de seguridad de siempre


def test_m1_en_sus_dos_sentidos_y_no_concluyente(tmp_path: Path) -> None:
    def m1(retcode: str, texto: str, colocada: str) -> str:
        fila = _p8(30, "m1_colocar", "26.88", retcode, texto, colocada, "buy_stop", "1.12623")
        return _respuesta(_paso_8(tmp_path, [fila]), "M1")

    assert "si: la rechaza al colocar (10019 NO_MONEY)" in m1("10019", "NO_MONEY", "no")
    assert "no: la acepta al colocar (10008 PLACED)" in m1("10008", "PLACED", "si")
    assert "no concluyente: no (10014 INVALID_VOLUME)" in m1("10014", "INVALID_VOLUME", "no")
    nm = _p8(30, "m1_no_medible", "si", nota="el volumen necesario pasa del maximo por orden")
    assert "no medible: el volumen necesario pasa del maximo" in _respuesta(
        _paso_8(tmp_path, [nm]), "M1"
    )


def test_m2_juzga_por_el_libre_que_baja(tmp_path: Path) -> None:
    def m2(**kw: str) -> str:
        return _respuesta(_paso_8(tmp_path, _m2(**kw)), "M2")

    # el libre baja lo calculado a la orden (2270; al mercado, 2250: D = 20)
    assert "si, carga al precio de la orden" in m2()
    assert "si, carga al precio de mercado" in m2(libre_despues="97750.00")
    # ACCOUNT_MARGIN sube pero el libre no baja: no carga
    r = m2(libre_despues="100000.00", margen_despues="2270.00")
    assert r.split(": ", 1)[1].startswith("no: la pendiente viva no carga margen")
    assert "ACCOUNT_MARGIN +2270.00" in r
    # carga, pero lejos de los dos calculos
    assert "no concluyente: carga, pero ni al precio" in m2(libre_despues="99000.00")
    # D por debajo de 10: el precio no se distingue
    assert "si, carga (el precio no se distingue" in m2(mercado="2265.00")


def test_m2_sin_la_pendiente_viva_no_concluye(tmp_path: Path) -> None:
    filas = _m2()
    filas[0] = _p8(40, "m2_colocar", "0.61", "10019", "NO_MONEY", "no", "buy_stop", "1.12623")
    assert "no concluyente: la pendiente no quedo viva" in _respuesta(
        _paso_8(tmp_path, filas), "M2"
    )


def test_m3_en_sus_dos_sentidos_y_no_concluyente(tmp_path: Path) -> None:
    def m3(retcode: str, texto: str, colocada: str, primera: str = "si") -> str:
        filas = [
            _p8(50, "m3_colocar_1", "14.79", "10008", "PLACED", primera, "buy_stop", "1.12623"),
            _p8(51, "m3_colocar_2", "14.79", retcode, texto, colocada, "buy_stop", "1.12623"),
        ]
        return _respuesta(_paso_8(tmp_path, filas), "M3")

    assert "si: suma las pendientes al colocar" in m3("10019", "NO_MONEY", "no")
    assert "no: no las suma al colocar" in m3("10008", "PLACED", "si")
    assert "no concluyente: la segunda no (10034 LIMIT_VOLUME)" in m3("10034", "LIMIT_VOLUME", "no")
    assert "no concluyente: la primera no quedo viva" in m3("10008", "PLACED", "si", primera="no")


def test_m4_llenada_entera_da_no_y_parcial_no_concluye(tmp_path: Path) -> None:
    no = _respuesta(_paso_8(tmp_path, _m4()), "M4")
    assert "no: la llena sin margen libre (a 1.11634; libre al resolver 73950.00)" in no
    parcial = _respuesta(_paso_8(tmp_path, _m4(deal="10.00")), "M4")
    assert "no concluyente: llenado parcial" in parcial


def test_m4_ocupacion_caida_no_concluye_en_los_dos_sentidos(tmp_path: Path) -> None:
    for filas in (_m4(viva="no"), _m4("sin_deal", viva="no")):
        r = _respuesta(_paso_8(tmp_path, filas), "M4")
        assert "no concluyente: la ocupacion cayo antes de que se resolviera S" in r


def test_m4_si_solo_rechazada_con_el_motivo_del_margen(tmp_path: Path) -> None:
    def m4(**kw: str) -> str:
        return _respuesta(_paso_8(tmp_path, _m4("sin_deal", **kw)), "M4")

    assert "si: la rechaza al llenar por el margen (ORDER_STATE_REJECTED, «[no money]»" in m4()
    assert "no concluyente: S sin deal (ORDER_STATE_REJECTED, «[invalid stops]»" in m4(
        comentario="[invalid stops]"
    )
    # CANCELED nunca da «si», aunque el comentario nombre el margen
    assert "no concluyente: S sin deal (ORDER_STATE_CANCELED, «[no money]»" in m4(
        estado="ORDER_STATE_CANCELED"
    )
    # con un tope agregado de volumen que S y la ocupacion pasan, tampoco
    assert "no concluyente: S sin deal" in m4(limite="20.00")
    assert "si: la rechaza al llenar" in m4(limite="50.00")


def test_m4_sin_la_condicion_de_partida_o_sin_salto_no_concluye(tmp_path: Path) -> None:
    cabia = _respuesta(_paso_8(tmp_path, _m4(libre_tras_ocupar="85000.00")), "M4")
    assert "no concluyente: S cabia al llenar" in cabia
    assert "no concluyente: no_salto" in _respuesta(_paso_8(tmp_path, _m4("no_salto")), "M4")
    no_medible = [
        _p8(61, "m4_ocupacion", "no_medible", nota="las pendientes cargan su margen y MT5 las suma")
    ]
    assert "no medible: las pendientes cargan su margen" in _respuesta(
        _paso_8(tmp_path, no_medible), "M4"
    )


def test_el_retcode_10019_del_paso_8_no_es_inesperado(tmp_path: Path) -> None:
    m = _cargar()
    fila = _p8(30, "m1_colocar", "26.88", "10019", "NO_MONEY", "no", "buy_stop", "1.12623")
    ruta = _csv(tmp_path / "MedirDemoFTMO_20301102_100000.csv", _version_1_2([fila]))
    texto = m.informe(m.ficheros_de([ruta]))
    assert "## Retcodes INESPERADOS: esas filas no miden lo que dicen\n\n- ninguno" in texto
