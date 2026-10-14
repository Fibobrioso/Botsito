"""La seccion «## Diferencias por operacion» del informe del arnes (rama
`trabajo/corrida-construccion`, R3.1): todo SINTETICO, sin motor, sin velas y sin correr el arnes.
Cada test rompe un caso a proposito en los dos sentidos: lo que empareja sale emparejado y lo que
queda a 4 puntos o a 16 minutos sale sin pareja con su Δ; una sesion sin operacion del bot dice
«ninguna» y el hecho que falto; una operacion del bot en un dia sin trader sale sin pareja; y la
seccion no anade ninguna opcion al comando (la lista cerrada de ADR-0070 sigue igual)."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from fractions import Fraction

from botsito.cases.criterio_fidelidad import Criterio, Operacion, Tolerancias
from botsito.cli import build_parser
from botsito.engine import arnes
from botsito.engine.motor import ResultadoDia, TrazaSesion

CONSTRUCCION = ("2030-03", "2030-01")  # a proposito, NO cronologico: el orden de la lista manda
CRITERIO = Criterio(
    Tolerancias(3, 15, 100_000),
    Fraction(7, 10),
    Fraction(6, 10),
    CONSTRUCCION,
    ("2030-02",),
    Fraction(7, 10),
    Fraction(6, 10),
    "perfil-de-prueba",
)
# dos hechos de origen regla, en el orden de la spec, y uno del broker que el embudo no mira
VOCABULARIO: dict[str, dict[str, object]] = {
    "hechos": {
        "sesgo": {"produce": ["RN-A"]},
        "liquidez": {"produce": ["RN-B"]},
        "llenada": {"origen": "broker"},
    }
}
SESION = "07-11"
ENTRADA = Decimal("1.10000")


def _t(dia: str, h: int, m: int, s: int = 0) -> datetime:
    return datetime.fromisoformat(f"{dia}T00:00:00+00:00") + timedelta(
        hours=h, minutes=m, seconds=s
    )


def _op(
    dia: str, h: int, m: int, lado: str = "venta", entrada: Decimal = ENTRADA, s: int = 0
) -> Operacion:
    return Operacion(dia, SESION, lado, _t(dia, h, m, s), entrada)


def _traza(*producidos: str, paradas: set[tuple[str, str]] | None = None) -> TrazaSesion:
    t = TrazaSesion()
    t.fijados = [(0, "sintetico", h, "si") for h in producidos]
    t.no_implementadas = set(paradas or set())
    return t


def _corrida(
    dias: dict[str, tuple[Operacion, ...]],
    bot: dict[str, tuple[Operacion, ...]],
    trazas: dict[str, TrazaSesion] | None = None,
    meses: tuple[str, ...] = CONSTRUCCION,
) -> arnes.Corrida:
    """`dias`: operaciones del trader por dia (un caso por dia); `bot`: las del bot por dia."""
    return arnes.Corrida(
        "sintetico",
        meses,
        tuple(arnes.DiaTrader(f"caso-{d}", d, ops) for d, ops in dias.items()),
        tuple(
            ResultadoDia(d, bot.get(d, ()), {SESION: (trazas or {}).get(d, TrazaSesion())})
            for d in dias
        ),
    )


def _seccion(corrida: arnes.Corrida) -> str:
    texto = arnes.informe(corrida, CRITERIO, VOCABULARIO, opciones=(), simulacion=None)
    assert texto.count("## Diferencias por operacion") == 1
    return texto.split("## Diferencias por operacion", 1)[1]


def _filas(seccion: str, quien: str) -> list[str]:
    return [ln for ln in seccion.splitlines() if ln.startswith(f"{quien} | ")]


# ------------------------------------------------------------------ emparejada / sin pareja


def test_una_operacion_emparejada_sale_como_pareja_con_su_delta() -> None:
    trader = _op("2030-01-07", 7, 30)
    bot = _op("2030-01-07", 7, 30, s=30, entrada=Decimal("1.10001"))  # +1 punto, +30 s
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {"2030-01-07": (bot,)}))
    (fila,) = _filas(seccion, "trader")
    assert fila == (
        "trader | 2030-01-07 | 07-11 | venta | 2030-01-07T07:30:00+00:00 | 1.10000 | PAREJA bot "
        "2030-01-07T07:30:30+00:00 1.10001 (Δentrada +1 puntos, Δinstante +0 min 30 s)"
    )
    assert _filas(seccion, "bot") == []  # la del bot tiene pareja: no sale aparte
    assert "2030-01 | 1 | 1 | 1 | 0 | 1 | 1/1 (100.0 %) | 1/1 (100.0 %)" in seccion


def test_a_cuatro_puntos_sale_sin_pareja_y_a_tres_con_pareja() -> None:
    trader = _op("2030-01-07", 7, 30)
    lejos = _op("2030-01-07", 7, 30, entrada=Decimal("1.10004"))  # 4 puntos: fuera
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {"2030-01-07": (lejos,)}))
    (fila,) = _filas(seccion, "trader")
    assert (
        "SIN PAREJA; bot mas cercano en la sesion: venta 2030-01-07T07:30:00+00:00 1.10004 " in fila
    )
    assert "(Δentrada +4 puntos, Δinstante +0 min 0 s)" in fila
    (fila_bot,) = _filas(seccion, "bot")
    assert fila_bot.endswith(
        "SIN PAREJA; trader mas cercano en la sesion: venta 2030-01-07T07:30:00+00:00 1.10000 "
        "(Δentrada -4 puntos, Δinstante +0 min 0 s)"
    )
    assert "2030-01 | 1 | 1 | 1 | 0 | 0 | 0/1 (0.0 %) | 0/1 (0.0 %)" in seccion
    # el mismo caso a 3 puntos, el limite del criterio (`compatibles` usa <=): pareja
    justo = _op("2030-01-07", 7, 30, entrada=Decimal("1.10003"))
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {"2030-01-07": (justo,)}))
    assert "PAREJA bot 2030-01-07T07:30:00+00:00 1.10003 (Δentrada +3 puntos" in seccion


def test_a_dieciseis_minutos_sale_sin_pareja_y_a_quince_con_pareja() -> None:
    trader = _op("2030-01-07", 7, 30)
    tarde = _op("2030-01-07", 7, 46)  # 16 min: fuera
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {"2030-01-07": (tarde,)}))
    (fila,) = _filas(seccion, "trader")
    assert (
        "SIN PAREJA; bot mas cercano en la sesion: venta 2030-01-07T07:46:00+00:00 1.10000 " in fila
    )
    assert "(Δentrada +0 puntos, Δinstante +16 min 0 s)" in fila
    (fila_bot,) = _filas(seccion, "bot")
    assert "(Δentrada +0 puntos, Δinstante -16 min 0 s)" in fila_bot
    justo = _op("2030-01-07", 7, 45)
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {"2030-01-07": (justo,)}))
    assert (
        "PAREJA bot 2030-01-07T07:45:00+00:00 1.10000 (Δentrada +0 puntos, Δinstante +15 min 0 s)"
        in (seccion)
    )


def test_el_mas_cercano_sigue_el_orden_del_criterio_y_no_exige_el_lado() -> None:
    """Menor |Δinstante| primero, aunque sea del otro lado y a mas puntos."""
    trader = _op("2030-01-07", 7, 30)
    compra_cerca = _op("2030-01-07", 7, 31, lado="compra", entrada=Decimal("1.10050"))
    venta_lejos = _op("2030-01-07", 7, 50)  # 20 min: tampoco empareja
    seccion = _seccion(
        _corrida({"2030-01-07": (trader,)}, {"2030-01-07": (venta_lejos, compra_cerca)})
    )
    (fila,) = _filas(seccion, "trader")
    assert "bot mas cercano en la sesion: compra 2030-01-07T07:31:00+00:00 1.10050 " in fila
    assert "(Δentrada +50 puntos, Δinstante +1 min 0 s)" in fila
    assert len(_filas(seccion, "bot")) == 2


# ------------------------------------------------------------------------- el embudo que falto


def test_una_sesion_sin_operacion_del_bot_dice_ninguna_y_el_hecho_que_falto() -> None:
    trader = _op("2030-01-07", 7, 30)
    traza = _traza("sesgo", paradas={("RN-B", "predicado:alcanza_nivel"), ("RN-Z", "otra")})
    seccion = _seccion(_corrida({"2030-01-07": (trader,)}, {}, {"2030-01-07": traza}))
    (fila,) = _filas(seccion, "trader")
    assert fila.endswith(
        "SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: "
        "liquidez[predicado:alcanza_nivel]"
    )
    # y el embudo por mes lo cuenta
    assert "2030-01 | sesiones con operaciones del trader 1; sin operacion del bot 1" in seccion
    assert "2030-01 | liquidez[predicado:alcanza_nivel] | 1" in seccion
    assert "2030-01 | 1 | 1 | 0 | 0 | 0 | 0/1 (0.0 %) | sin definir (cero operaciones del bot" in (
        seccion
    )


def test_el_primer_hecho_que_falta_sigue_el_orden_de_la_spec() -> None:
    hechos = arnes.hechos_de_regla(VOCABULARIO)
    assert [h for h, _ in hechos] == ["sesgo", "liquidez"]
    assert arnes.primer_hecho_que_falta(_traza(), hechos) == "sesgo[productoras sin cumplirse]"
    assert arnes.primer_hecho_que_falta(_traza("sesgo"), hechos) == (
        "liquidez[productoras sin cumplirse]"
    )
    assert arnes.primer_hecho_que_falta(_traza("sesgo", "liquidez"), hechos) == (
        "todos los hechos del camino producidos"
    )
    with_parada = _traza(paradas={("RN-A", "predicado:x"), ("RN-A", "accion:y")})
    assert arnes.primer_hecho_que_falta(with_parada, hechos) == "sesgo[accion:y, predicado:x]"


def test_un_freno_detenido_por_no_se_nombra_si_no_se_produjo_y_si_cuando_se_produjo() -> None:
    """Respuesta del consultor a la PARADA 2, punto 1.a: el ultimo campo mira el CAMINO (sin los
    detenido_por_*) y nombra un freno solo si se produjo. Con la spec real, el freno iba antes que
    liquidez_tomada y salia como «primer hecho que falta» en 47 de 53 sesiones (§3.5)."""
    vocabulario: dict[str, dict[str, object]] = {
        "hechos": {
            "sesgo": {"produce": ["RN-A"]},
            "detenido_por_tope": {"produce": ["RN-T"]},
            "detenido_por_racha": {"produce": ["RN-R"]},
            "liquidez": {"produce": ["RN-B"]},
        }
    }
    hechos = arnes.hechos_de_regla(vocabulario)
    # el freno no se produjo: ni se nombra, y el primer hecho que falta es el del camino
    assert arnes.primer_hecho_que_falta(_traza("sesgo"), hechos) == (
        "liquidez[productoras sin cumplirse]"
    )
    assert arnes.primer_hecho_que_falta(_traza("sesgo", "liquidez"), hechos) == (
        "todos los hechos del camino producidos"
    )
    # el freno se produjo: se nombra aparte, y el camino se sigue mirando igual
    assert arnes.primer_hecho_que_falta(_traza("sesgo", "detenido_por_racha"), hechos) == (
        "liquidez[productoras sin cumplirse]; frenos producidos: detenido_por_racha"
    )
    assert arnes.primer_hecho_que_falta(
        _traza("sesgo", "liquidez", "detenido_por_tope", "detenido_por_racha"), hechos
    ) == ("todos los hechos del camino producidos; frenos producidos: detenido_por_tope, "
          "detenido_por_racha")  # fmt: skip
    # y en la tabla: una sesion con sesgo y sin bot nunca dice detenido_por_tope
    trader = _op("2030-01-07", 7, 30)
    corrida = _corrida({"2030-01-07": (trader,)}, {}, {"2030-01-07": _traza("sesgo")})
    texto = arnes.informe(corrida, CRITERIO, vocabulario, opciones=(), simulacion=None)
    seccion = texto.split("## Diferencias por operacion", 1)[1]
    assert "detenido_por" not in seccion.split("### Por operacion", 1)[1]
    assert "primer hecho que falto: liquidez[productoras sin cumplirse]" in seccion
    assert "2030-01 | liquidez[productoras sin cumplirse] | 1" in seccion


def test_una_sesion_con_pareja_y_otra_sin_bot_en_el_mismo_dia() -> None:
    """Dos operaciones del trader el mismo dia: una emparejada y otra sin bot en su sesion (la
    sesion 11-15 no tiene traza: TrazaSesion vacia)."""
    dia = "2030-01-07"
    a = _op(dia, 7, 30)
    b = Operacion(dia, "11-15", "compra", _t(dia, 12, 0), ENTRADA)
    bot = _op(dia, 7, 31)
    seccion = _seccion(_corrida({dia: (a, b)}, {dia: (bot,)}, {dia: _traza("sesgo", "liquidez")}))
    fa, fb = _filas(seccion, "trader")
    assert "PAREJA bot" in fa
    assert fb.endswith(
        "SIN PAREJA; ninguna operacion del bot en la sesion; primer hecho que falto: "
        "sesgo[productoras sin cumplirse]"
    )
    assert "2030-01 | 1 | 2 | 1 | 0 | 1 | 1/2 (50.0 %) | 1/1 (100.0 %)" in seccion
    assert "2030-01 | sesiones con operaciones del trader 2; sin operacion del bot 1" in seccion


# ---------------------------------------------------------------- el bot en un dia sin trader


def test_una_operacion_del_bot_en_un_dia_sin_trader_sale_sin_pareja_y_no_puntua() -> None:
    bot = _op("2030-01-08", 8, 0, lado="compra")
    seccion = _seccion(
        _corrida(
            {"2030-01-07": (_op("2030-01-07", 7, 30),), "2030-01-08": ()}, {"2030-01-08": (bot,)}
        )
    )
    (fila_bot,) = _filas(seccion, "bot")
    assert fila_bot == (
        "bot | 2030-01-08 | 07-11 | compra | 2030-01-08T08:00:00+00:00 | 1.10000 | SIN PAREJA; "
        "ninguna operacion del trader en el dia"
    )
    # resumen: 2 dias, 1 del trader, 0 puntuables, 1 fuera, 0 parejas
    assert "2030-01 | 2 | 1 | 0 | 1 | 0 | 0/1 (0.0 %) | sin definir (cero operaciones del bot" in (
        seccion
    )


def test_una_operacion_del_bot_en_otra_sesion_del_dia_del_trader_dice_ninguna_en_la_sesion() -> (
    None
):
    dia = "2030-01-07"
    trader = _op(dia, 7, 30)
    bot = Operacion(dia, "11-15", "venta", _t(dia, 12, 0), ENTRADA)  # puntua, no empareja
    seccion = _seccion(_corrida({dia: (trader,)}, {dia: (bot,)}))
    (fila_bot,) = _filas(seccion, "bot")
    assert fila_bot.endswith("SIN PAREJA; ninguna operacion del trader en la sesion")
    assert "2030-01 | 1 | 1 | 1 | 0 | 0 | 0/1 (0.0 %) | 0/1 (0.0 %)" in seccion


# ------------------------------------------------------------- orden, sitio y determinismo


def test_las_filas_van_por_mes_en_el_orden_de_construccion_y_por_dia() -> None:
    dias: dict[str, tuple[Operacion, ...]] = {
        "2030-01-07": (_op("2030-01-07", 7, 30),),
        "2030-01-06": (_op("2030-01-06", 7, 30),),
        "2030-03-05": (_op("2030-03-05", 7, 30),),
    }
    seccion = _seccion(_corrida(dias, {}))
    assert [f.split(" | ")[1] for f in _filas(seccion, "trader")] == [
        "2030-03-05",
        "2030-01-06",
        "2030-01-07",
    ]
    resumen = [ln for ln in seccion.splitlines() if ln.startswith("2030-0") and " | " in ln]
    assert resumen[0].startswith("2030-03 | 1 | 1 |") and resumen[1].startswith("2030-01 | 2 | 2 |")


def test_la_seccion_es_la_ultima_del_informe_y_el_informe_sigue_determinista() -> None:
    corrida = _corrida(
        {"2030-01-07": (_op("2030-01-07", 7, 30),)}, {"2030-01-07": (_op("2030-01-07", 7, 31),)}
    )
    uno = arnes.informe(corrida, CRITERIO, VOCABULARIO, opciones=(), simulacion=None)
    dos = arnes.informe(corrida, CRITERIO, VOCABULARIO, opciones=(), simulacion=None)
    assert uno.encode("utf-8") == dos.encode("utf-8")
    assert uno.index("## Por sesion") < uno.index("## Diferencias por operacion")
    assert uno.rstrip("\n").splitlines()[-1].startswith("trader | 2030-01-07 | ")
    # la cabecera lleva las tolerancias del criterio, no cifras escritas en el codigo
    assert "## Diferencias por operacion (ADR-0043: 3 puntos, 15 min)" in uno
    # y es la misma medida que la seccion del criterio: las parejas coinciden
    assert "cobertura: 1/1 (100.0 %)" in uno and "2030-01 | 1 | 1 | 1 | 0 | 1 |" in uno


def test_la_linea_por_sesion_dice_que_bloqueo_un_gate_y_ninguna_si_no_hubo() -> None:
    """Respuesta del consultor a la PARADA 3, punto 1: `bloqueadas` de la traza, en «Por sesion»,
    con la regla, la accion y el motivo; «ninguna» si no hubo. Solo salida."""
    dia = "2030-01-07"
    traza = _traza("sesgo", "liquidez")
    traza.bloqueadas = {
        ("RN-015", "accion:colocar_orden_limite", "prohibida:abrir_operacion"),
        ("RN-011", "accion:dimensionar", "gate desconocido:abrir_operacion"),
    }
    corrida = _corrida({dia: (_op(dia, 7, 30),)}, {}, {dia: traza})
    texto = arnes.informe(corrida, CRITERIO, VOCABULARIO, opciones=(), simulacion=None)
    (linea,) = [ln for ln in texto.splitlines() if ln.startswith(f"{dia} {SESION} | trader")]
    assert linea.endswith(
        "| bloqueadas RN-011:accion:dimensionar:gate desconocido:abrir_operacion, "
        "RN-015:accion:colocar_orden_limite:prohibida:abrir_operacion"
    )
    assert "| disparadas ninguna | bloqueadas " in linea
    # y sin bloqueadas, «ninguna»: la traza vacia de una sesion normal
    sin = _corrida({dia: (_op(dia, 7, 30),)}, {}, {dia: _traza("sesgo", "liquidez")})
    texto = arnes.informe(sin, CRITERIO, VOCABULARIO, opciones=(), simulacion=None)
    (linea,) = [ln for ln in texto.splitlines() if ln.startswith(f"{dia} {SESION} | trader")]
    assert linea.endswith("| bloqueadas ninguna")
    assert arnes.bloqueadas_de(TrazaSesion()) == "ninguna"


def test_la_seccion_no_anade_ninguna_opcion_al_comando() -> None:
    """ADR-0070: la lista cerrada sigue igual y el subparser de `motor arnes` tiene exactamente las
    opciones de antes de esta rama (leidas del parser, no de --help)."""
    lista = {"--salida", "--tracemalloc", "--meses", "--simular", "--perfil", "--fase"}
    assert lista == arnes.OPCIONES_QUE_NO_CAMBIAN_LA_CORRIDA
    args = build_parser().parse_args(["motor", "arnes", "--salida", "x.txt"])
    largas = sorted(
        o
        for a in args.parser_de_la_corrida._actions
        for o in a.option_strings
        if o.startswith("--")
    )
    assert largas == [
        "--depuracion", "--diagnostico-a27", "--diagnostico-a35", "--diagnostico-a44",
        "--diagnostico-a47", "--diagnostico-cuenta-diaria", "--fase", "--help", "--meses",
        "--perfil", "--salida", "--simular", "--tracemalloc",
    ]  # fmt: skip
