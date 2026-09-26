"""La capa de cuenta del simulador (ADR-0050) sobre secuencias SINTETICAS de operaciones y el
perfil real de FTMO (fase `reto`): suspension en el instante EXACTO que cruza el limite diario y
no uno antes; el reinicio del dia en los dos cambios de hora europeos; perdida diaria por equity
flotante aunque el saldo no cruce; objetivo alcanzado sin los dias minimos, que no supera;
comision y swaps que convierten una fase superada en no superada; persistencia entre dias -la
total se arrastra, la diaria se reinicia-; la negativa a correr con un parametro sin valor; un
segundo perfil INVENTADO que demuestra que cambiar de firma es solo configuracion; y determinismo.

El contrato vale 1 y los lotes 1: el P/L es la diferencia de precios, en dinero. Los instantes
son de 2030, ningun dia real del material.
"""

from __future__ import annotations

import ast
import dataclasses
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from botsito.config.registro import Estado
from botsito.engine import cuenta, perfil_cuenta
from botsito.engine.cuenta import (
    Cargo,
    EstadoCuenta,
    Marca,
    Operacion,
    OperacionError,
    ReglasFase,
    ResultadoFase,
    evaluar_fase,
    reglas_de_fase,
)
from botsito.engine.perfil_cuenta import (
    SUFIJOS_DE_FASE,
    ParametroSinValorError,
    PerfilCuenta,
    cargar_perfil,
    nombre_de_fase,
)

RAIZ = Path(__file__).resolve().parents[2]
FTMO = RAIZ / "knowledge" / "cuentas" / "ftmo-2step-swing-100k.yaml"
SINTETICO = RAIZ / "tests" / "fixtures" / "cuentas" / "sintetica-una-fase-50k.yaml"
CONTRATO = Decimal(1)
ACCESORES = {
    "porcentaje": "porcentaje",
    "decimal": "decimal",
    "entero": "entero",
    "booleano": "booleano",
    "opcion": "enum",
    "texto": "texto",
    "lotes": "lotes",
}
UNO = Decimal(1)
PRECIO = Decimal(1000)
D = Decimal


def _t(mes: int, dia: int, hora: int, minuto: int = 0, segundo: int = 0) -> datetime:
    return datetime(2030, mes, dia, hora, minuto, segundo, tzinfo=UTC)


def _op(
    id: str,
    abre: datetime,
    cierra: datetime,
    resultado: Decimal | int,
    *,
    lotes: Decimal = UNO,
    marcas: tuple[tuple[datetime, Decimal | int], ...] = (),
    cargos: tuple[Cargo, ...] = (),
) -> Operacion:
    """Una compra que abre en PRECIO y cierra en PRECIO + resultado; cada marca es (instante,
    P/L flotante en ese instante)."""
    return Operacion(
        id=id,
        direccion="compra",
        lotes=lotes,
        apertura=Marca(abre, PRECIO),
        cierre=Marca(cierra, PRECIO + D(resultado)),
        cargos=cargos,
        marcas=tuple(Marca(t, PRECIO + D(v)) for t, v in marcas),
    )


@pytest.fixture(scope="module")
def ftmo() -> PerfilCuenta:
    return cargar_perfil(FTMO)


@pytest.fixture(scope="module")
def reto() -> ReglasFase:
    return reglas_de_fase(cargar_perfil(FTMO), "reto")


@pytest.fixture(scope="module")
def sintetica() -> ReglasFase:
    return reglas_de_fase(cargar_perfil(SINTETICO), "unica")


def _correr(ops: list[Operacion], reglas: ReglasFase) -> ResultadoFase:
    return evaluar_fase(ops, reglas, CONTRATO)


# ------------------------------------------------------------------------- lo que pide el brief


def test_suspension_exacta_en_el_instante_que_cruza_el_limite_diario(reto: ReglasFase) -> None:
    """Limite del dia: 100.000 - 5 % de 100.000 = 95.000. Caer HASTA el limite no infringe (R18,
    «drops below»); caer por debajo, si, y en ese instante y no antes."""
    hasta_el_limite = ((_t(1, 7, 10), -4999), (_t(1, 7, 10, 30), -5000))
    op = _op("a", _t(1, 7, 9), _t(1, 7, 12), 0, marcas=hasta_el_limite)
    r = _correr([op], reto)
    assert r.estado is EstadoCuenta.EN_CURSO, r.motivo
    assert r.dias[0].equity_minima == D(95000)

    op = _op("a", _t(1, 7, 9), _t(1, 7, 12), 0, marcas=(*hasta_el_limite, (_t(1, 7, 11), -5001)))
    r = _correr([op], reto)
    assert r.estado is EstadoCuenta.SUSPENDIDA
    assert r.instante == _t(1, 7, 11)
    assert "perdida diaria" in r.motivo and "94999" in r.motivo and "95000" in r.motivo
    assert "[marca de a]" in r.motivo
    assert r.saldo_final == D(100000), "el cierre posterior ya no se evalua: la cuenta esta parada"


@pytest.mark.parametrize(
    ("dia_antes", "medianoche_1", "dia_1", "medianoche_2", "dia_2"),
    [
        # marzo: el 31 empieza en CET (23:00Z del 30) y el 1 de abril ya en CEST (22:00Z del 31)
        (date(2030, 3, 30), _t(3, 30, 23), date(2030, 3, 31), _t(3, 31, 22), date(2030, 4, 1)),
        # octubre: el 27 empieza en CEST (22:00Z del 26) y el 28 ya en CET (23:00Z del 27)
        (
            date(2030, 10, 26),
            _t(10, 26, 22),
            date(2030, 10, 27),
            _t(10, 27, 23),
            date(2030, 10, 28),
        ),
    ],
)
def test_reinicio_del_dia_en_los_dos_cambios_de_hora_europeos(
    reto: ReglasFase,
    dia_antes: date,
    medianoche_1: datetime,
    dia_1: date,
    medianoche_2: datetime,
    dia_2: date,
) -> None:
    """Las medianoches medidas con zoneinfo, afirmadas en UTC para que un tzdata distinto se vea.
    Una perdida de 3.000 el dia anterior baja el limite del dia siguiente a 92.000: una marca a
    -4.999 justo despues de la medianoche vive, y habria suspendido con el limite viejo. El dia
    entero de 23 h o 25 h se cierra en su ultimo segundo, y el siguiente empieza en el primero
    con su propio limite (95.000 - 5.000 = 90.000, que es tambien el total: la marca a -4.999
    deja la equity en 90.001)."""
    prague = ZoneInfo("Europe/Prague")
    assert datetime.combine(dia_1, time(0), tzinfo=prague).astimezone(UTC) == medianoche_1
    assert datetime.combine(dia_2, time(0), tzinfo=prague).astimezone(UTC) == medianoche_2
    un_segundo_antes = medianoche_1 - _s(1)
    ops = [
        _op("antes", medianoche_1 - _s(3600), un_segundo_antes, -3000),
        _op(
            "dia1",
            medianoche_1,
            medianoche_2 - _s(1),
            -2000,
            marcas=((medianoche_1 + _s(1800), -4999),),
        ),
        _op(
            "dia2",
            medianoche_2,
            medianoche_2 + _s(3600),
            0,
            marcas=((medianoche_2 + _s(60), -4999),),
        ),
    ]
    r = _correr(ops, reto)
    assert r.estado is EstadoCuenta.EN_CURSO, r.motivo
    assert [(d.dia, d.saldo_corte, d.limite_dia, d.con_apertura) for d in r.dias] == [
        (dia_antes, D(100000), D(95000), True),
        (dia_1, D(97000), D(92000), True),
        (dia_2, D(95000), D(90000), True),
    ]
    assert r.dias[1].equity_minima == D(97000 - 4999)
    assert r.dias_de_trading == 3
    # sin el reinicio, la misma marca del dia 1 habria caido bajo el limite viejo
    sin_reinicio = _op(
        "x", medianoche_1, medianoche_1 + _s(3600), 0, marcas=((medianoche_1 + _s(1800), -7999),)
    )
    assert _correr([sin_reinicio], reto).estado is EstadoCuenta.SUSPENDIDA


def _s(segundos: int) -> timedelta:
    return timedelta(seconds=segundos)


def test_perdida_diaria_por_equity_flotante_aunque_el_saldo_no_cruce(reto: ReglasFase) -> None:
    """La posicion baja 5.001 a media manana y cierra ganando: el saldo nunca baja de 100.000 y
    la cuenta esta SUSPENDIDA desde la marca, porque la firma vigila la equity (R2)."""
    op = _op("a", _t(1, 7, 9), _t(1, 7, 12), +100, marcas=((_t(1, 7, 10), -5001),))
    r = _correr([op], reto)
    assert r.estado is EstadoCuenta.SUSPENDIDA
    assert r.instante == _t(1, 7, 10)
    assert "equity 94999" in r.motivo
    assert all(d.saldo_final >= d.limite_dia for d in r.dias)
    # la misma secuencia vigilando el SALDO -otra firma- no suspende: solo cambia la regla
    sobre_saldo = dataclasses.replace(reto, magnitud_vigilada="saldo")
    r2 = _correr([op], sobre_saldo)
    assert r2.estado is EstadoCuenta.EN_CURSO and r2.saldo_final == D(100100)


def test_objetivo_alcanzado_sin_los_dias_minimos_no_supera(reto: ReglasFase) -> None:
    """110.000 en dos dias es EN_CURSO (R4: 4 dias de trading); con dos dias mas de apertura,
    SUPERADA en el cierre que completa el cuarto dia, aunque ese cierre no gane nada."""
    dos_dias = [
        _op("a", _t(1, 7, 9), _t(1, 7, 10), +6000),
        _op("b", _t(1, 8, 9), _t(1, 8, 10), +4000),
    ]
    r = _correr(dos_dias, reto)
    assert r.estado is EstadoCuenta.EN_CURSO and r.saldo_final == D(110000)
    assert r.dias_de_trading == 2
    cuatro_dias = [
        *dos_dias,
        _op("c", _t(1, 9, 9), _t(1, 9, 10), 0),
        _op("d", _t(1, 10, 9), _t(1, 10, 10), 0),
    ]
    r = _correr(cuatro_dias, reto)
    assert r.estado is EstadoCuenta.SUPERADA
    assert r.instante == _t(1, 10, 10)
    assert "4 dias de trading (minimo 4)" in r.motivo and "[cierre de d]" in r.motivo
    # cuatro dias sin llegar al objetivo: EN_CURSO
    r = _correr([*dos_dias[:1], *cuatro_dias[2:]], reto)
    assert r.estado is EstadoCuenta.EN_CURSO and r.saldo_final == D(106000)


def test_el_objetivo_exige_todas_las_posiciones_cerradas(reto: ReglasFase) -> None:
    """R1: «with all positions closed». El cierre que llega al objetivo con otra posicion viva no
    supera; supera el cierre de la ultima."""
    ops = [
        _op("d1", _t(1, 7, 9), _t(1, 7, 10), 0),
        _op("d2", _t(1, 8, 9), _t(1, 8, 10), 0),
        _op("d3", _t(1, 9, 9), _t(1, 9, 10), 0),
        _op("larga", _t(1, 10, 9), _t(1, 10, 12), 0),
        _op("gana", _t(1, 10, 9, 30), _t(1, 10, 11), +10000),
    ]
    r = _correr(ops, reto)
    assert r.estado is EstadoCuenta.SUPERADA
    assert r.instante == _t(1, 10, 12) and "[cierre de larga]" in r.motivo


def test_comision_y_swaps_convierten_una_fase_superada_en_no_superada(reto: ReglasFase) -> None:
    """Cuatro dias que suman justo 10.000 brutos superan; los mismos con 5 de comision por
    operacion y un swap de 30 dejan el saldo en 109.950 y la fase EN_CURSO (R2: comision y swaps
    dentro de la equity, decision (b))."""

    def ops(con_cargos: bool) -> list[Operacion]:
        salida = []
        for i, gana in enumerate((2500, 2500, 2500, 2500)):
            abre, cierra = _t(1, 7 + i, 9), _t(1, 7 + i, 10)
            cargos: tuple[Cargo, ...] = ()
            if con_cargos:
                cargos = (Cargo(abre, D(5), "comision"),)
                if i == 3:
                    cargos += (Cargo(_t(1, 10, 9, 30), D(30), "swap"),)
            salida.append(_op(f"op{i}", abre, cierra, gana, cargos=cargos))
        return salida

    assert _correr(ops(False), reto).estado is EstadoCuenta.SUPERADA
    r = _correr(ops(True), reto)
    assert r.estado is EstadoCuenta.EN_CURSO
    assert r.saldo_final == D(110000 - 4 * 5 - 30) == r.equity_final


def test_persistencia_entre_dias_la_total_se_arrastra_y_la_diaria_se_reinicia(
    reto: ReglasFase,
) -> None:
    """Tres dias perdiendo 4.500, 4.500 y 1.500: ningun dia cruza su limite diario, porque cada
    dia se reinicia sobre el saldo del corte (H6: la cuenta persiste), y el tercero cruza el
    limite TOTAL estatico de 90.000, que no se reinicia nunca (R3)."""
    ops = [
        _op("d1", _t(1, 7, 9), _t(1, 7, 10), -4500),
        _op("d2", _t(1, 8, 9), _t(1, 8, 10), -4500),
        _op("d3", _t(1, 9, 9), _t(1, 9, 10), -1500),
    ]
    r = _correr(ops, reto)
    assert r.estado is EstadoCuenta.SUSPENDIDA
    assert r.instante == _t(1, 9, 10)
    assert "perdida total" in r.motivo and "perdida diaria" not in r.motivo
    assert [(d.saldo_corte, d.limite_dia) for d in r.dias] == [
        (D(100000), D(95000)),
        (D(95500), D(90500)),
        (D(91000), D(86000)),
    ]
    assert r.limite_total_final == D(90000)
    # dos dias solos: EN_CURSO, con 9.000 perdidos y ningun limite tocado
    r2 = _correr(ops[:2], reto)
    assert r2.estado is EstadoCuenta.EN_CURSO and r2.saldo_final == D(91000)


def test_negativa_a_correr_con_un_parametro_sin_valor(tmp_path: Path) -> None:
    """Un perfil cuya fase declara objetivo y no da la cifra: `reglas_de_fase` se niega nombrando
    el parametro. La fondeada de FTMO, sin objetivo ni dias por regla, corre."""
    texto = SINTETICO.read_text(encoding="utf-8")
    viejo = (
        '    estado: CONFIRMED\n    valor: "8"\n    minimo: "0"\n'
        "    fuente: {tipo: decision, id: ADR-0050}\n"
    )
    assert texto.count(viejo) == 1
    ruta = tmp_path / "sin-cifra.yaml"
    ruta.write_text(texto.replace(viejo, "    estado: UNKNOWN\n"), encoding="utf-8")
    perfil = cargar_perfil(ruta)
    with pytest.raises(ParametroSinValorError) as exc:
        reglas_de_fase(perfil, "unica")
    assert "firma_unica_objetivo no tiene valor" in str(exc.value)
    assert "sin-cifra" in str(exc.value)

    fondeada = reglas_de_fase(cargar_perfil(FTMO), "fondeada")
    r = _correr([_op("a", _t(1, 7, 9), _t(1, 7, 10), +20000)], fondeada)
    assert r.estado is EstadoCuenta.EN_CURSO, "sin objetivo por regla, nunca se supera"
    assert r.guardia_tamano.estado == "no_evaluable"
    assert "firma_tamano_posicion_ratio_aviso" in r.guardia_tamano.motivo


def test_un_segundo_perfil_sintetico_solo_cambia_la_configuracion(
    reto: ReglasFase, sintetica: ReglasFase
) -> None:
    """La misma secuencia bajo dos perfiles: con FTMO sigue EN_CURSO; con la firma inventada
    -3 % diario sobre 50.000, corte en Nueva York, vigila el saldo, el total arrastra el saldo
    maximo y la guardia tiene cifra- se SUSPENDE, y por el TOTAL arrastrado. Ni una linea de
    codigo distinta: solo el fichero."""
    ops = [
        _op("gana", _t(1, 7, 3, 30), _t(1, 7, 4), +400, lotes=D(5)),  # P/L 2.000
        _op("pierde", _t(1, 7, 13), _t(1, 7, 14), -3100),
        _op("otra", _t(1, 8, 13), _t(1, 8, 14), 0),
    ]
    con_ftmo = _correr(ops, reto)
    assert con_ftmo.estado is EstadoCuenta.EN_CURSO and con_ftmo.saldo_final == D(98900)
    assert con_ftmo.guardia_tamano.estado == "no_evaluable"
    assert con_ftmo.dias[0].dia == date(2030, 1, 7), "en Praga las 03:30Z son el dia 7"

    con_sintetica = _correr(ops, sintetica)
    assert con_sintetica.estado is EstadoCuenta.SUSPENDIDA
    assert con_sintetica.instante == _t(1, 7, 14)
    assert "perdida total" in con_sintetica.motivo and "49000" in con_sintetica.motivo
    assert con_sintetica.dias[0].dia == date(2030, 1, 6), "en Nueva York las 03:30Z son el dia 6"
    assert con_sintetica.limite_total_final == D(52000 - 3000)
    assert con_sintetica.guardia_tamano.estado == "evaluada"
    assert con_sintetica.guardia_tamano.avisos == (
        "gana: 5 lotes supera 2 veces la mediana 1 de las demas",
    )
    # y con el total ESTATICO de la misma firma inventada, 48.900 no cruza 47.000: EN_CURSO
    estatica = dataclasses.replace(sintetica, perdida_total_arrastra=False)
    assert _correr(ops, estatica).estado is EstadoCuenta.EN_CURSO


def test_determinismo(reto: ReglasFase) -> None:
    ops = [
        _op("b", _t(1, 8, 9), _t(1, 8, 10), -4500, marcas=((_t(1, 8, 9, 30), -100),)),
        _op("a", _t(1, 7, 9), _t(1, 7, 10), +300, cargos=(Cargo(_t(1, 7, 9), D(5), "comision"),)),
        _op("c", _t(1, 9, 9), _t(1, 9, 10), -6000),
    ]
    primero = _correr(ops, reto)
    assert primero == _correr(ops, reto)
    assert primero == _correr(list(reversed(ops)), reto)
    assert primero.estado is EstadoCuenta.SUSPENDIDA and primero.instante == _t(1, 9, 10)


# ------------------------------------------------------------------------------- lo demas


def test_el_primer_dia_usa_el_capital_inicial_y_sin_operaciones_no_pasa_nada(
    reto: ReglasFase,
) -> None:
    r = _correr([], reto)
    assert r.estado is EstadoCuenta.EN_CURSO and r.dias == () and r.motivo == "sin operaciones"
    r = _correr([_op("a", _t(1, 7, 9), _t(1, 7, 10), 0)], reto)
    assert r.dias[0].saldo_corte == D(100000) and r.dias[0].limite_dia == D(95000)


def test_el_dia_de_trading_es_el_de_la_apertura_y_la_diaria_y_la_total_a_la_vez_se_nombran(
    reto: ReglasFase,
) -> None:
    """Una posicion abierta el dia 7 que vive hasta el 9 cuenta un solo dia de trading. Y una
    caida que cruza los dos limites en el mismo instante nombra los dos."""
    larga = _op("larga", _t(1, 7, 9), _t(1, 9, 10), 0)
    r = _correr([larga], reto)
    assert r.dias_de_trading == 1 and [d.con_apertura for d in r.dias] == [True, False, False]
    hundida = _op("h", _t(1, 7, 9), _t(1, 7, 10), -10001)
    r = _correr([hundida], reto)
    assert r.estado is EstadoCuenta.SUSPENDIDA
    assert "perdida diaria" in r.motivo and "perdida total" in r.motivo


def test_tras_el_final_no_se_evalua_nada_y_se_cuenta(reto: ReglasFase) -> None:
    ops = [
        _op("a", _t(1, 7, 9), _t(1, 7, 10), -6000),
        _op("b", _t(1, 8, 9), _t(1, 8, 10), +50000),
    ]
    r = _correr(ops, reto)
    assert r.estado is EstadoCuenta.SUSPENDIDA and r.instante == _t(1, 7, 10)
    assert r.operaciones_evaluadas == 1 and r.operaciones_tras_el_final == 1
    assert r.saldo_final == D(94000)


def test_a_igual_instante_el_cierre_va_antes_que_la_apertura(reto: ReglasFase) -> None:
    """Un cierre y una apertura en el mismo segundo: el objetivo se evalua con la posicion
    anterior ya cerrada y la nueva todavia sin abrir."""
    t = _t(1, 10, 10)
    ops = [
        _op("d1", _t(1, 7, 9), _t(1, 7, 10), 0),
        _op("d2", _t(1, 8, 9), _t(1, 8, 10), 0),
        _op("d3", _t(1, 9, 9), _t(1, 9, 10), 0),
        _op("gana", _t(1, 10, 9), t, +10000),
        _op("nueva", t, _t(1, 10, 12), -500),
    ]
    r = _correr(ops, reto)
    assert r.estado is EstadoCuenta.SUPERADA and r.instante == t
    assert r.operaciones_tras_el_final == 1


def test_una_operacion_mal_formada_no_se_adivina(reto: ReglasFase) -> None:
    sin_huso = Operacion(
        "x", "compra", UNO, Marca(datetime(2030, 1, 7, 9), PRECIO), Marca(_t(1, 7, 10), PRECIO)
    )
    with pytest.raises(OperacionError, match="no lleva huso"):
        _correr([sin_huso], reto)
    with pytest.raises(OperacionError, match="cierra antes de abrir"):
        _correr([_op("x", _t(1, 7, 10), _t(1, 7, 9), 0)], reto)
    with pytest.raises(OperacionError, match="marca fuera"):
        _correr([_op("x", _t(1, 7, 9), _t(1, 7, 10), 0, marcas=((_t(1, 7, 11), 0),))], reto)
    with pytest.raises(OperacionError, match="cargo fuera"):
        _correr(
            [_op("x", _t(1, 7, 9), _t(1, 7, 10), 0, cargos=(Cargo(_t(1, 7, 8), D(1), "swap"),))],
            reto,
        )
    with pytest.raises(OperacionError, match="repetidos"):
        _correr([_op("x", _t(1, 7, 9), _t(1, 7, 10), 0)] * 2, reto)
    with pytest.raises(OperacionError, match="lotes no positivos"):
        _correr([_op("x", _t(1, 7, 9), _t(1, 7, 10), 0, lotes=D(0))], reto)
    with pytest.raises(OperacionError, match="contrato no positivo"):
        evaluar_fase([_op("x", _t(1, 7, 9), _t(1, 7, 10), 0)], reto, D(0))


def test_una_venta_gana_cuando_el_precio_baja(reto: ReglasFase) -> None:
    venta = Operacion(
        "v", "venta", D(2), Marca(_t(1, 7, 9), PRECIO), Marca(_t(1, 7, 10), PRECIO - D(300))
    )
    r = _correr([venta], reto)
    assert r.saldo_final == D(100000 + 2 * 300)


# ------------------------------------------------------------- lo que el perfil le da al motor


def test_todo_parametro_del_perfil_tiene_lector(ftmo: PerfilCuenta) -> None:
    """F12: un parametro con valor y sin lector es un valor que nadie usa y nadie vigila. Lo lee
    el motor de cuenta -por su nombre o por el convenio de fase-, o declara `consumido_por`."""
    fuentes = "".join(
        (RAIZ / "src" / "botsito" / "engine" / m).read_text(encoding="utf-8")
        for m in ("cuenta.py", "perfil_cuenta.py")
    )
    por_convenio = {nombre_de_fase(f, s) for f in ftmo.fases() for s in SUFIJOS_DE_FASE}
    huerfanos = [
        n
        for n, p in ftmo.registro.parametros.items()
        if p.valor is not None
        and n not in por_convenio
        and f'"{n}"' not in fuentes
        and not p.consumido_por
    ]
    assert huerfanos == [], f"parametros del perfil que nadie lee ni declara lector: {huerfanos}"


def test_cada_accesor_del_perfil_en_src_nombra_un_parametro_de_ftmo_con_su_tipo(
    ftmo: PerfilCuenta,
) -> None:
    """El contrato de `test_registro_accessors`, para `perfil.<accesor>("nombre")`."""
    usos: list[tuple[str, str, str]] = []
    for py in sorted((RAIZ / "src" / "botsito").rglob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in ACCESORES
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "perfil"
            ):
                usos.append((f"{py.name}:{node.lineno}", node.func.attr, node.args[0].value))
    assert usos, "ningun uso: el detector no ve nada"
    problemas = []
    for donde, accesor, nombre in usos:
        p = ftmo.registro.parametros.get(nombre)
        if p is None:
            problemas.append(f"{donde}: {nombre!r} no esta en el perfil de FTMO")
        elif p.tipo != ACCESORES[accesor]:
            problemas.append(f"{donde}: {nombre} es {p.tipo}, se lee con .{accesor}()")
    assert problemas == [], problemas


def test_las_reglas_de_una_fase_se_leen_del_perfil_y_lo_que_no_aplica_queda_en_none(
    ftmo: PerfilCuenta,
) -> None:
    reto = cuenta.reglas_de_fase(ftmo, "reto")
    assert reto.objetivo is not None and reto.dias_minimos == 4
    assert reto.ratio_aviso_tamano is None and reto.guardia_tamano_aplica
    fondeada = cuenta.reglas_de_fase(ftmo, "fondeada")
    assert fondeada.objetivo is None and fondeada.dias_minimos is None
    with pytest.raises(ValueError, match="no tiene la fase 'otra'"):
        cuenta.reglas_de_fase(ftmo, "otra")
    assert ftmo.registro.parametros["firma_fondeada_objetivo"].estado is Estado.UNKNOWN
    assert perfil_cuenta.CATEGORIA_PERFIL == "prop_firm"
