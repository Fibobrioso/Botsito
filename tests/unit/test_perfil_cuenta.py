"""El perfil de cuenta (ADR-0050): el fichero de FTMO carga por la puerta del registro, cada
cifra cita una regla de FTMO-REGLAS.md que existe, lo que coincide con parametros.yaml lleva el
mismo valor, lo que la fuente no dice no tiene valor y leerlo se niega nombrando el parametro, y
las guardias de `cargar_perfil` sobre perfiles SINTETICOS en `tmp_path`. Lo que el perfil le da al
motor de cuenta -las reglas de una fase, el contrato de accesores, que todo parametro tenga lector-
se prueba en `test_cuenta.py`."""

from __future__ import annotations

import re
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

import pytest

from botsito.comun.husos import huso_canonico
from botsito.config.registro import cargar_registro
from botsito.engine.perfil_cuenta import (
    FASES,
    HUSO_CORTE,
    ParametroSinValorError,
    PerfilCuenta,
    PerfilError,
    cargar_perfil,
)

RAIZ = Path(__file__).resolve().parents[2]
FTMO = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
SINTETICO = RAIZ / "tests" / "fixtures" / "cuentas" / "sintetica-una-fase-50k.yaml"
REGLAS_FTMO = RAIZ / "docs" / "validation" / "FTMO-REGLAS.md"
REGISTRO = RAIZ / "knowledge" / "spec" / "parametros.yaml"


@pytest.fixture(scope="module")
def ftmo() -> PerfilCuenta:
    return cargar_perfil(FTMO)


def _perfil_sintetico(tmp_path: Path, *cambios: tuple[str, str], nombre: str = "p.yaml") -> Path:
    """El fixture sintetico con sustituciones EXACTAS (cada una tiene que casar una vez)."""
    texto = SINTETICO.read_text(encoding="utf-8")
    for viejo, nuevo in cambios:
        assert texto.count(viejo) == 1, viejo
        texto = texto.replace(viejo, nuevo)
    ruta = tmp_path / nombre
    ruta.write_text(texto, encoding="utf-8")
    return ruta


# --------------------------------------------------------------------------- el perfil de FTMO


def test_el_perfil_de_ftmo_carga_con_sus_tres_fases_y_su_reloj(ftmo: PerfilCuenta) -> None:
    assert ftmo.fases() == ("reto", "verificacion", "fondeada")
    assert ftmo.huso_corte().key == "Europe/Prague"
    assert all(p.categoria == "prop_firm" for p in ftmo.registro.parametros.values())


def test_cada_cifra_del_perfil_cita_una_regla_de_ftmo_reglas_que_existe(
    ftmo: PerfilCuenta,
) -> None:
    """R1..R20 son las filas de la tabla de FTMO-REGLAS.md §2; una cita a una regla que no esta
    en la tabla es una cita rota."""
    tabla = REGLAS_FTMO.read_text(encoding="utf-8")
    existen = set(re.findall(r"^\| (R\d+) \|", tabla, re.M))
    assert len(existen) >= 20
    sin_cita: list[str] = []
    rotas: list[str] = []
    for nombre, p in ftmo.registro.parametros.items():
        citadas = set(re.findall(r"\bR\d+\b", p.descripcion))
        if not citadas:
            sin_cita.append(nombre)
        rotas += [f"{nombre}: {r}" for r in sorted(citadas - existen)]
    assert sin_cita == [], f"parametros del perfil sin regla de FTMO-REGLAS citada: {sin_cita}"
    assert rotas == [], f"citas a reglas que no existen: {rotas}"


def test_lo_que_no_esta_en_la_fuente_no_tiene_valor(ftmo: PerfilCuenta) -> None:
    """Los NO ENCONTRADA de FTMO-REGLAS y lo que no aplica a la fondeada (ADR-0012 §2)."""
    assert ftmo.sin_valor() == (
        "firma_fondeada_dias_minimos",
        "firma_fondeada_objetivo",
        "firma_tamano_posicion_ratio_aviso",
    )
    with pytest.raises(ParametroSinValorError) as exc:
        ftmo.decimal("firma_tamano_posicion_ratio_aviso")
    assert "firma_tamano_posicion_ratio_aviso" in str(exc.value)
    assert "ftmo-2step-swing-100k" in str(exc.value)
    assert "no puede correr" in str(exc.value)


def test_un_nombre_que_coincide_con_parametros_yaml_lleva_el_mismo_valor(
    ftmo: PerfilCuenta,
) -> None:
    """Precedente ADR-0012 §1: dos listas con lo mismo se cruzan para que no se separen."""
    registro = cargar_registro(REGISTRO)
    comunes = sorted(set(ftmo.registro.parametros) & set(registro.parametros))
    assert len(comunes) >= 8, comunes
    distintos = []
    for n in comunes:
        a, b = ftmo.registro.parametros[n], registro.parametros[n]
        if (a.tipo, a.valor, a.opciones) != (b.tipo, b.valor, b.opciones):
            distintos.append(
                f"{n}: perfil {a.valor!r}/{a.tipo} frente a registro {b.valor!r}/{b.tipo}"
            )
    assert distintos == [], distintos


def test_el_reloj_de_corte_de_ftmo_coincide_hoy_con_el_del_trader(ftmo: PerfilCuenta) -> None:
    """ADR-0027 §3: CE(S)T y huso_operativa dan hoy los mismos instantes; si algun dia divergen,
    esto lo vera. Medido a medianoche de cada dia de un ano entero, incluidos los dos cambios."""
    registro = cargar_registro(REGISTRO)
    trader = huso_canonico(registro.texto("huso_operativa"))
    firma = ftmo.huso_corte()
    dia = date(2030, 1, 1)
    while dia.year == 2030:
        a = datetime.combine(dia, time(0), tzinfo=firma).astimezone(UTC)
        b = datetime.combine(dia, time(0), tzinfo=trader).astimezone(UTC)
        assert a == b, dia
        dia += timedelta(days=1)


# ------------------------------------------------------------------- las guardias del cargador


def test_el_perfil_sintetico_carga_y_es_otra_firma(ftmo: PerfilCuenta) -> None:
    s = cargar_perfil(SINTETICO)
    assert s.fases() == ("unica",)
    assert s.huso_corte().key != ftmo.huso_corte().key
    assert s.decimal("saldo_inicial_cuenta") != ftmo.decimal("saldo_inicial_cuenta")
    assert s.registro.parametros["firma"].valor == "sintetica"


def test_un_parametro_que_no_es_prop_firm_no_es_de_un_perfil(tmp_path: Path) -> None:
    ruta = _perfil_sintetico(
        tmp_path,
        (
            "  - nombre: firma_unica_objetivo\n    categoria: prop_firm",
            "  - nombre: firma_unica_objetivo\n    categoria: estrategia",
        ),
    )
    with pytest.raises(PerfilError, match="sobran \\['firma_unica_objetivo'\\]"):
        cargar_perfil(ruta)


def test_sin_reloj_de_corte_o_con_uno_que_no_existe_no_carga(tmp_path: Path) -> None:
    sin = _perfil_sintetico(
        tmp_path, ("  - nombre: firma_huso_corte", "  - nombre: firma_huso_cort")
    )
    with pytest.raises(PerfilError, match=f"falta {HUSO_CORTE}"):
        cargar_perfil(sin)
    malo = _perfil_sintetico(tmp_path, ('valor: "America/New_York"', 'valor: "Marte/Olympus"'))
    with pytest.raises(PerfilError, match="huso desconocido"):
        cargar_perfil(malo)
    vacio = _perfil_sintetico(
        tmp_path,
        (
            '    estado: CONFIRMED\n    valor: "America/New_York"\n'
            "    fuente: {tipo: decision, id: ADR-0050}\n",
            "    estado: UNKNOWN\n",
        ),
    )
    with pytest.raises(PerfilError, match=f"{HUSO_CORTE} sin valor"):
        cargar_perfil(vacio)


def test_las_fases_se_declaran_enteras(tmp_path: Path) -> None:
    sin_fases = _perfil_sintetico(tmp_path, ("  - nombre: firma_fases", "  - nombre: firma_fase"))
    with pytest.raises(PerfilError, match=f"falta {FASES}"):
        cargar_perfil(sin_fases)
    repetida = _perfil_sintetico(tmp_path, ('valor: "unica"', 'valor: "unica unica"'))
    with pytest.raises(PerfilError, match="repite una fase"):
        cargar_perfil(repetida)
    incompleta = _perfil_sintetico(tmp_path, ('valor: "unica"', 'valor: "unica segunda"'))
    with pytest.raises(PerfilError) as exc:
        cargar_perfil(incompleta)
    assert "'segunda' no declara" in str(exc.value)
    assert "firma_segunda_objetivo_aplica" in str(exc.value)
    mal_nombrada = _perfil_sintetico(tmp_path, ('valor: "unica"', 'valor: "Unica"'))
    with pytest.raises(PerfilError, match="nombre de fase invalido"):
        cargar_perfil(mal_nombrada)


def test_un_fichero_que_no_pasa_el_registro_no_es_un_perfil(tmp_path: Path) -> None:
    ruta = tmp_path / "roto.yaml"
    ruta.write_text("parametros:\n  - nombre: x\n", encoding="utf-8")
    with pytest.raises(PerfilError, match="categoria"):
        cargar_perfil(ruta)


def test_la_comision_por_lado_toma_el_supuesto_conservador(ftmo: PerfilCuenta) -> None:
    """Decision del consultor (2026-09-25): se cobra en CADA lado hasta que FTMO lo confirme. El
    simulador ya no se niega a correr por ella; la descripcion sigue citando R12 NO ENCONTRADA."""
    assert ftmo.booleano("firma_comision_por_lado") is True
    p = ftmo.registro.parametros["firma_comision_por_lado"]
    assert "NO ENCONTRADA" in " ".join(p.descripcion.split())
    assert "CONSERVADOR" in p.descripcion and "confirme" in p.descripcion
