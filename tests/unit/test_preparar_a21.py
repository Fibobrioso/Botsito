"""RN-008, RN-009 y RN-011 listas para activarse con la respuesta a A-21 (rama
trabajo/preparar-a21): el selector `zona_control_limpia` SIN FIJAR hace que el motor se niegue
nombrando A-21; el modo diagnostico corre con una lectura hipotetica y lo etiqueta todo; sobre un
dia SINTETICO con la spec REAL, tras la toma de la liquidez de M15 el breaker de M1 forma la zona,
RN-008 deja de prohibir y RN-011 liga la zona; sin mirar al futuro con cada lectura; por el arnes
real las dos lecturas dejan trazas DISTINTAS cuando una mecha pasa el extremo del bloque; y por el
cableado la zona llega al broker como una orden limite con su stop y su objetivo."""

from __future__ import annotations

from datetime import UTC, date
from decimal import ROUND_UP, Decimal
from pathlib import Path

import pytest

from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.domain.estructura_m1 import (
    LECTURAS_LIMPIA,
    PRIMER_ESQUEMA,
    SEGUNDO_ESQUEMA,
    SIN_MECHA_MAS_ALLA_DEL_EXTREMO,
    SOLO_UNA_ZONA_DE_CONTROL,
)
from botsito.domain.pivotes_m15 import CIERRE_VELA_CONTRARIA
from botsito.domain.ticks import MS_POR_MINUTO, MilisegundoUtc, Tick
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import arnes, cableado, diagnostico, visor, zonas
from botsito.engine.cuenta import reglas_de_fase
from botsito.engine.diagnostico import Diagnostico
from botsito.engine.interprete import Interprete, ReglaEjecutable
from botsito.engine.llenado import Configuracion
from botsito.engine.motor import DatosMercado, DiaDeMercado, MotorSpec, ResultadoDia
from botsito.engine.perfil_cuenta import cargar_perfil
from botsito.engine.primitivas import primitivas_escritas
from botsito.engine.simulacion import MercadoDia, reglas_broker_de
from botsito.engine.tope_trader import tope_del_registro
from botsito.engine.zonas import (
    PARAMETRO_A21,
    DiagnosticoDeZonaRechazadoError,
    SinLecturaDeZonaError,
    lectura_limpia,
)
from botsito.spec.modelo import cargar_vocabulario
from tests.unit import test_cableado as tc
from tests.unit import test_preparar_a35 as ta

RAIZ = Path(__file__).resolve().parents[2]
BASE = ta.BASE
TOMA = ta.INICIO + ta.M15 * (ta.CRUZA + 1)  # el cierre de B5: RN-004 fija liquidez_tomada
REFERENCIA = BASE - 99  # el ALTO de M1 que deja la racha verde de B3 (max(a, c) + 1)
SPREAD = 3
Paso = tuple[int, int, int | None, int | None]  # apertura, cierre, minimo, maximo


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def reglas() -> list[ReglaEjecutable]:
    from botsito.engine.interprete import reglas_ejecutables
    from botsito.spec.modelo import cargar_reglas

    return list(reglas_ejecutables(cargar_reglas(ta.SPEC)))


# Tras la toma, el precio esta en BASE-300. Los caminos, vela a vela (M1):
#   LIMPIO (primer esquema): dos rojas -la segunda es el bloque-, tres verdes y la tercera pasa la
#     referencia con la mecha; ninguna mecha del impulso baja del extremo del bloque.
#   SUCIO: igual, pero la primera verde del impulso baja con la mecha por debajo del bloque: la
#     lectura `sin_mecha_mas_alla_del_extremo` no da la zona, `solo_una_zona_de_control` si.
#   RETROCESO (segundo esquema): roja, verde, dos rojas de retroceso, verde (una zona de control),
#     y el breaker.
#   DOS_ZONAS: dos retrocesos antes del breaker: RN-009 prohibe.
LIMPIO: list[Paso] = [
    (BASE - 300, BASE - 310, None, None),
    (BASE - 310, BASE - 322, BASE - 324, BASE - 308),  # el bloque: [BASE-324, BASE-308]
    (BASE - 322, BASE - 250, None, None),
    (BASE - 250, BASE - 170, None, None),
    (BASE - 170, BASE - 100, None, BASE - 94),  # el breaker: la mecha pasa BASE-99
]
SUCIO: list[Paso] = [*LIMPIO[:2], (BASE - 322, BASE - 250, BASE - 330, None), *LIMPIO[3:]]
RETROCESO: list[Paso] = [
    (BASE - 300, BASE - 310, None, None),
    (BASE - 310, BASE - 240, None, None),
    (BASE - 240, BASE - 260, None, None),
    (BASE - 260, BASE - 270, BASE - 274, BASE - 258),  # el bloque del segundo esquema
    (BASE - 270, BASE - 180, None, None),
    (BASE - 180, BASE - 100, None, BASE - 94),
]
DOS_ZONAS: list[Paso] = [
    (BASE - 300, BASE - 240, None, None),
    (BASE - 240, BASE - 260, None, None),
    (BASE - 260, BASE - 200, None, None),
    (BASE - 200, BASE - 230, None, None),
    (BASE - 230, BASE - 100, None, BASE - 94),
]


def _m1(camino: list[Paso], hasta: int | None = None) -> list[Vela]:
    """Los seis bloques de la liquidez (tests de A-35), el camino dado desde la toma y despues velas
    sin cuerpo hasta el fin de la ventana. Con `hasta`, solo las M1 con inicio < hasta."""
    velas: list[Vela] = []
    for n, (a, c, lo) in enumerate(ta.BLOQUES):
        velas += ta._bloque(n, a, c, lo)
    minuto = TOMA
    for a, c, lo, hi in camino:
        velas.append(
            Vela(
                MinutoUtc(minuto),
                Puntos(a),
                Puntos(hi if hi is not None else max(a, c) + 1),
                Puntos(lo if lo is not None else min(a, c) - 1),
                Puntos(c),
                1,
            )
        )
        minuto += 1
    ultimo = camino[-1][1]
    while minuto < ta.FIN:
        velas.append(
            Vela(
                MinutoUtc(minuto),
                Puntos(ultimo),
                Puntos(ultimo + 1),
                Puntos(ultimo - 1),
                Puntos(ultimo),
                1,
            )
        )
        minuto += 1
    return [v for v in velas if hasta is None or int(v.inicio) < hasta]


def _datos(registro: Registro, camino: list[Paso], hasta: int | None = None) -> DatosMercado:
    m1 = _m1(camino, hasta)
    anclaje = registro.hora("anclaje_h4")
    return DatosMercado(ta._h4_alcista(), agregar(m1, ta.M15, anclaje), m1, CIERRE_VELA_CONTRARIA)


def _motor(registro: Registro, reglas: list[ReglaEjecutable], limpia: str) -> MotorSpec:
    tope = tope_del_registro(
        registro,
        cargar_perfil(tc.PERFIL).huso_corte(),
        Diagnostico(a44=diagnostico.A44_SIN_TOPE),
    )
    return MotorSpec(
        Interprete(cargar_vocabulario(ta.SPEC), primitivas_escritas(registro, tope, limpia)), reglas
    )


def _correr(
    registro: Registro, reglas: list[ReglaEjecutable], camino: list[Paso], limpia: str
) -> ResultadoDia:
    return _motor(registro, reglas, limpia).correr_dia(ta._dia(_datos(registro, camino)))


def _breaker_fin(camino: list[Paso]) -> int:
    return TOMA + len(camino)


# ------------------------------------------------------------------------- el motor de la spec


def test_el_primer_esquema_forma_la_zona_y_rn011_la_liga_en_el_cierre_del_breaker(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    r = _correr(registro, reglas, LIMPIO, SOLO_UNA_ZONA_DE_CONTROL)
    traza = r.sesiones["07-11"]
    assert {"RN-004", "RN-011", "RN-015"} <= traza.disparadas
    fijados = [(t, h, v) for t, _, h, v in traza.fijados if h == "orden_dimensionada"]
    assert fijados and fijados[0] == (_breaker_fin(LIMPIO), "orden_dimensionada", "zona:1")
    # RN-008 y RN-009 ya no estan en DESCONOCIDO: sus primitivas se evaluaron
    faltan = {p for _, p in traza.no_implementadas}
    evaluadas = {
        "predicado:se_da_esquema",
        "predicado:zonas_desarrolladas_superan",
        "predicado:toca_colocar_orden_limite",
        "predicado:se_desarrolla_en_el_lado_de_ruido",
    }
    assert not faltan & evaluadas
    # las acciones del broker no estan en el motor de la spec: huecos con nombre, no fallos
    assert ("RN-011", "accion:dimensionar_lote") in traza.no_implementadas
    # antes del breaker, RN-008 prohibia abrir: la zona no existe hasta que la M1 rompe
    for t in range(TOMA, _breaker_fin(LIMPIO)):
        assert t not in {x for x, _, _ in fijados}


def test_el_segundo_esquema_y_las_dos_zonas(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    r = _correr(registro, reglas, RETROCESO, SOLO_UNA_ZONA_DE_CONTROL)
    traza = r.sesiones["07-11"]
    assert "RN-011" in traza.disparadas and "RN-009" not in traza.disparadas
    zona = zonas.zonas_del_dia  # el productor deja la zona en la memoria del dia
    dos = _correr(registro, reglas, DOS_ZONAS, SOLO_UNA_ZONA_DE_CONTROL)
    t2 = dos.sesiones["07-11"]
    assert "RN-009" in t2.disparadas and "RN-011" not in t2.disparadas
    assert ("detenido", "x") not in {(h, v) for _, _, h, v in t2.fijados}
    assert zona is not None


def test_las_dos_lecturas_de_a21_dejan_trazas_distintas_por_el_arnes_real(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Fase 2.3: la sesion completa pasa por `arnes.correr` con el motor real. En el camino SUCIO la
    primera verde del impulso baja con la mecha por debajo del bloque: con
    `solo_una_zona_de_control` la zona se forma y RN-011 liga `zona:1`; con
    `sin_mecha_mas_alla_del_extremo` no hay zona, RN-008 sigue prohibiendo y RN-011 no dispara."""
    trazas = {}
    for lectura in LECTURAS_LIMPIA:
        dias = (arnes.DiaTrader("caso-x-2030-01-15", ta.DIA.isoformat(), ()),)
        corrida = arnes.correr(
            "x", ("2030-01",), dias, {ta.DIA.isoformat(): ta._dia(_datos(registro, SUCIO))},
            _motor(registro, reglas, lectura),
        )  # fmt: skip
        trazas[lectura] = corrida.resultados[0].sesiones["07-11"]
    solo, sin = trazas[SOLO_UNA_ZONA_DE_CONTROL], trazas[SIN_MECHA_MAS_ALLA_DEL_EXTREMO]
    assert "RN-011" in solo.disparadas and "RN-011" not in sin.disparadas
    assert ("orden_dimensionada", "zona:1") in {(h, v) for _, _, h, v in solo.fijados}
    assert not any(h == "orden_dimensionada" for _, _, h, _ in sin.fijados)
    assert solo.fijados != sin.fijados and solo.disparadas != sin.disparadas
    # y en el camino LIMPIO las dos coinciden: es la mecha lo que el selector separa
    iguales = [
        _correr(registro, reglas, LIMPIO, lectura).sesiones["07-11"] for lectura in LECTURAS_LIMPIA
    ]
    assert (
        iguales[0].fijados == iguales[1].fijados and iguales[0].disparadas == iguales[1].disparadas
    )


def test_sin_mirar_al_futuro_la_zona_existe_desde_el_cierre_del_breaker_con_cada_lectura(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Recortar las M1 en `t` no cambia lo fijado hasta `t` con ninguna lectura; y con las M1 hasta
    un minuto antes del breaker, la zona no existe."""
    for lectura in LECTURAS_LIMPIA:
        completo = _correr(registro, reglas, LIMPIO, lectura).sesiones["07-11"]
        breaker = _breaker_fin(LIMPIO)
        for corte in (breaker - 1, breaker, breaker + 3):
            recortado = (
                _motor(registro, reglas, lectura)
                .correr_dia(ta._dia(_datos(registro, LIMPIO, hasta=corte)))
                .sesiones["07-11"]
            )
            assert [f for f in completo.fijados if f[0] < corte] == [
                f for f in recortado.fijados if f[0] < corte
            ], (lectura, corte)
        antes = (
            _motor(registro, reglas, lectura)
            .correr_dia(ta._dia(_datos(registro, LIMPIO, hasta=breaker - 1)))
            .sesiones["07-11"]
        )
        assert not any(h == "orden_dimensionada" for _, _, h, _ in antes.fijados), lectura


# ------------------------------------------------------------------------- el cableado


def _mercado_de(m1: list[Vela]) -> MercadoDia:
    ticks: list[Tick] = []
    for v in m1:
        o, c = int(v.abierta), int(v.cierre)
        for seg, b in ((0, o), (20, (o + c) // 2), (40, c)):
            ms = int(v.inicio) * MS_POR_MINUTO + seg * 1000
            ticks.append(Tick(MilisegundoUtc(ms), Puntos(b + SPREAD), Puntos(b), 0, 0))
    return MercadoDia(
        "caso-x-2030-01-15", ta.DIA, MinutoUtc(ta.INICIO), MinutoUtc(ta.FIN), tc.ESCALA,
        tuple(m1), tuple(ticks), ("sintetico",), (),
    )  # fmt: skip


def test_por_el_cableado_la_zona_llega_al_broker_como_una_orden_limite(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Con el broker y la cuenta cableados (ADR-0053) y los tres selectores en diagnostico, la
    zona del primer esquema se convierte en una orden limite en la entrada del bloque, con el stop
    a stop_fraccion_caja de la caja y el objetivo a objetivo_rr sobre la caja completa."""
    m1 = _m1(LIMPIO)
    perfil = cargar_perfil(tc.PERFIL)
    tope = tope_del_registro(
        registro, perfil.huso_corte(), Diagnostico(a44=diagnostico.A44_SIN_TOPE)
    )
    motor = cableado.MotorCableado(
        vocabulario=cargar_vocabulario(ta.SPEC),
        reglas=reglas,
        registro=registro,
        mercados={ta.DIA.isoformat(): _mercado_de(m1)},
        reglas_broker=reglas_broker_de(perfil),
        reglas_fase=reglas_de_fase(perfil, "reto"),
        config_llenado=Configuracion(False, 0, lambda _m: SPREAD),
        contrato=registro.decimal("instrumento_contrato"),
        tope=tope,
        limpia=SOLO_UNA_ZONA_DE_CONTROL,
    )
    dia = DiaDeMercado(ta.DIA, ta.HUSO, ta.SESIONES, _datos(registro, LIMPIO))
    r = motor.correr_dia(dia)
    traza = r.sesiones["07-11"]
    assert {"RN-004", "RN-011", "RN-015"} <= traza.disparadas
    broker = motor.brokers[ta.DIA.isoformat()]
    tb = motor.trazas_broker[ta.DIA.isoformat()]
    assert broker.ordenes or tb.rechazos, "ni orden ni rechazo: la zona no llego al broker"
    if broker.ordenes:
        (o,) = broker.ordenes.values()
        entrada, extremo = BASE - 308, BASE - 324  # el bloque LIMPIO: entrada arriba, extremo abajo
        caja = entrada - extremo
        assert o.lado == "compra" and o.precio == entrada
        # caja de 16 puntos: el nivel de stop_fraccion_caja cae entre dos puntos y, desde la
        # sesion 3, el stop va al siguiente ALEJANDOSE de la entrada (stop_fraccion_redondeo)
        assert registro.opcion("stop_fraccion_redondeo") == "alejandose_de_la_entrada"
        exacta = Decimal(caja) * registro.fraccion("stop_fraccion_caja").valor
        assert exacta != int(exacta) and o.stop == entrada - int(exacta.to_integral_value(ROUND_UP))
        assert o.objetivo == entrada + int(Decimal(caja) * registro.decimal("objetivo_rr"))
        assert o.colocada_ms == (_breaker_fin(LIMPIO) * MS_POR_MINUTO - 1)
    # y la zona llega al detalle del visor, que la pinta desde el cierre del breaker y no antes
    detalle = cableado.detalle_para_visor(motor, ta.DIA.isoformat())
    assert detalle is not None and len(detalle.zonas) == 1
    (z,) = detalle.zonas
    escala = broker.escala
    assert (z.lado, z.por) == ("compra", PRIMER_ESQUEMA)
    assert (int(z.entrada * escala), int(z.extremo * escala)) == (BASE - 308, BASE - 324)
    assert z.formada is not None and int(z.formada.timestamp() // 60) == _breaker_fin(LIMPIO)
    d = visor.DiaVisor(
        caso="caso-sintetico",
        dia=ta.DIA,
        huso=ta.HUSO,
        sesiones=ta.SESIONES,
        ventana=("07:00", "15:00"),
        escala=escala,
        m1=tuple(m1),
        m15=(),
        h4=(),
        trader=(),
        bot=(),
        resultado=r,
        parejas=(),
        hechos=(),
        sesgos=(),
        objetivo_rr=None,
        motor="spec",
        broker=detalle,
    )
    con = visor.render_dia(d)
    assert 'class="zona compra"' in con and "Zonas de entrada ligadas por el motor" in con
    sin = visor.render_dia(d, MinutoUtc(_breaker_fin(LIMPIO) - 1))
    assert 'class="zona' not in sin and "<p>ninguna</p>" in sin


# ------------------------------------------------------------------------- el diagnostico


def test_sin_fijar_el_motor_se_niega_nombrando_a21_y_el_diagnostico_corre(
    registro: Registro,
) -> None:
    with pytest.raises(SinLecturaDeZonaError, match="A-21") as exc:
        lectura_limpia(registro, None)
    assert PARAMETRO_A21 in str(exc.value) and "diagnostico" in str(exc.value)
    assert (
        lectura_limpia(registro, SIN_MECHA_MAS_ALLA_DEL_EXTREMO) == SIN_MECHA_MAS_ALLA_DEL_EXTREMO
    )
    with pytest.raises(ValueError, match="A-21"):
        lectura_limpia(registro, "al_ojo")
    d = Diagnostico(a21=SOLO_UNA_ZONA_DE_CONTROL)
    assert d.etiquetas == ("DIAGNOSTICO-A21-solo_una_zona_de_control",)
    with pytest.raises(ValueError, match="A-21"):
        Diagnostico(a21="limpia_a_ojo")


def test_con_el_valor_fijado_el_diagnostico_se_rechaza(tmp_path: Path) -> None:
    contenido = f"""
parametros:
  - nombre: {PARAMETRO_A21}
    categoria: estrategia
    tipo: enum
    unidad: que la hace limpia
    opciones: [solo_una_zona_de_control, sin_mecha_mas_alla_del_extremo]
    descripcion: el selector, ya respondido en este registro de prueba
    estado: CONFIRMED
    valor: solo_una_zona_de_control
    fuente: {{tipo: feedback, id: fb-2030-01-16-sesion-02-1a2b3c4d}}
"""
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(contenido, encoding="utf-8")
    fijado = cargar_registro(ruta)
    assert lectura_limpia(fijado, None) == SOLO_UNA_ZONA_DE_CONTROL
    with pytest.raises(DiagnosticoDeZonaRechazadoError, match="ya esta fijado"):
        lectura_limpia(fijado, SIN_MECHA_MAS_ALLA_DEL_EXTREMO)


def test_la_cli_se_niega_sin_a21_aunque_a35_y_a44_vayan_en_diagnostico(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio

    real = cargar_criterio(RAIZ)
    salida = tmp_path / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", real.construccion[0], "--salida",
         str(salida), "--diagnostico-a35", "inicio_vela_contraria", "--diagnostico-a44", "sin_tope"]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert codigo == 2 and "A-21" in err and PARAMETRO_A21 in err
    assert not list(tmp_path.iterdir())
    # y la compuerta de construccion sigue mandando primero
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", real.medida[0], "--salida", str(salida),
         "--diagnostico-a35", "inicio_vela_contraria", "--diagnostico-a44", "sin_tope",
         "--diagnostico-a21", SOLO_UNA_ZONA_DE_CONTROL]
    )  # fmt: skip
    assert codigo == 2 and "MEDIDA" in capsys.readouterr().err and not list(tmp_path.iterdir())


def test_los_esquemas_se_nombran_como_la_spec() -> None:
    assert (PRIMER_ESQUEMA, SEGUNDO_ESQUEMA) == ("primer_esquema", "segundo_esquema")
    assert date(2030, 1, 15).weekday() == 1  # martes: el dia sintetico esta dentro de la semana
    assert UTC is not None
