"""El visor de dias de construccion, sobre un dia SINTETICO de 2030 (velas en zigzag, una traza del
motor inventada, operaciones del trader y del bot conocidas): la negativa a medida y a lo que no
es construccion -misma compuerta y mismos mensajes que el arnes-, el centinela de un dia oculto
que no se lee, el determinismo byte a byte, que cada cosa aparece donde debe, que la vista no mira
al futuro, el indice, y que la salida cae en una carpeta que git ignora. Ningun dia real se lee
salvo el criterio commiteado y, si `data/` esta en la maquina, un dia dev de construccion por la
CLI."""

from __future__ import annotations

import math
import subprocess
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import Criterio, Tolerancias, cargar_criterio, medir
from botsito.cases.holdout import HoldoutCerradoError
from botsito.comun.yaml_estricto import YamlError
from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import visor
from botsito.engine.arnes import ConjuntoError
from botsito.engine.motor import ResultadoDia, Sesion, TrazaSesion
from botsito.engine.visor import (
    BOT,
    TRADER,
    DiaVisor,
    Lienzo,
    OperacionVisor,
    caso_de_construccion,
    render_dia,
)

RAIZ = Path(__file__).resolve().parents[2]
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
VENTANA = ("00:00", "15:00")
DIA = date(2030, 1, 15)  # martes; ninguna fecha real
ESCALA = 100_000
HECHOS = (("sesgo", ("RN-003",)), ("liquidez_tomada", ("RN-004",)))


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


def _t(h: int, m: int = 0, s: int = 0) -> datetime:
    return datetime(DIA.year, DIA.month, DIA.day, h, m, s, tzinfo=UTC)


def _m1(desde: datetime, hasta: datetime) -> list[Vela]:
    velas: list[Vela] = []
    t, i, base = desde, 0, 110_000
    while t < hasta:
        a = base + int(300 * math.sin(i / 97) + 120 * math.sin(i / 23))
        c = base + int(300 * math.sin((i + 1) / 97) + 120 * math.sin((i + 1) / 23))
        velas.append(
            Vela(a_minuto(t), Puntos(a), Puntos(max(a, c) + 3), Puntos(min(a, c) - 3), Puntos(c), 1)
        )
        t += timedelta(minutes=1)
        i += 1
    return velas


def _criterio() -> Criterio:
    return Criterio(
        Tolerancias(3, 15, ESCALA), Fraction(7, 10), Fraction(6, 10), ("2030-01",), ("2030-02",)
    )


def _dia(registro: Registro, *, con_bot: bool = True) -> DiaVisor:
    """Un dia con una compra del trader a las 08:05Z (sesion 07-11), una del bot un minuto
    despues y a dos puntos, y una venta del trader a las 12:00Z (sesion 11-15) sin pareja."""
    desde = visor._minuto_local(DIA, VENTANA[0], HUSO)
    hasta = visor._minuto_local(DIA, VENTANA[1], HUSO)
    m1 = _m1(datetime.fromtimestamp(desde * 60, UTC), datetime.fromtimestamp(hasta * 60, UTC))
    m15 = agregar(m1, visor.MINUTOS_M15, registro.hora("anclaje_h4"))
    trader = (
        OperacionVisor(
            TRADER, "07-11", "compra", _t(8, 5, 20), Decimal("1.10010"), Decimal("1.09950")
        ),
        OperacionVisor(
            TRADER, "11-15", "venta", _t(12, 0, 0), Decimal("1.10300"), Decimal("1.10360")
        ),
    )
    bot = (
        (OperacionVisor(BOT, "07-11", "compra", _t(8, 6, 0), Decimal("1.10012")),)
        if con_bot
        else ()
    )
    fijados_1 = [
        (int(visor._minuto_local(DIA, "07:00", HUSO)), "RN-003", "sesgo", "alcista"),
        (int(a_minuto(_t(8, 4))), "RN-004", "liquidez_tomada", "si"),
    ]
    fijados_2 = [(int(visor._minuto_local(DIA, "11:00", HUSO)), "RN-003", "sesgo", "bajista")]
    traza_1 = TrazaSesion(fijados=fijados_1, disparadas={"RN-003", "RN-004"})
    traza_2 = TrazaSesion(
        fijados=fijados_2,
        no_implementadas={("RN-004", "predicado:alcanza_nivel")},
        bloqueadas={("RN-015", "accion:colocar_orden_limite", "gate desconocido:abrir_operacion")},
        empates={("gate", ("RN-001", "RN-033"))},
        anotaciones={"sesgo_h4": "bajista"},
    )
    traza_1.anotaciones["sesgo_h4"] = "alcista"
    resultado = ResultadoDia(
        DIA.isoformat(),
        tuple(o.como_criterio(DIA.isoformat()) for o in bot),
        {"07-11": traza_1, "11-15": traza_2},
    )
    parejas = medir(
        [o.como_criterio(DIA.isoformat()) for o in trader],
        [o.como_criterio(DIA.isoformat()) for o in bot],
        _criterio().tolerancias,
    ).parejas
    return DiaVisor(
        caso="caso-x-2030-01-15",
        dia=DIA,
        huso=HUSO,
        sesiones=SESIONES,
        ventana=VENTANA,
        escala=ESCALA,
        m1=tuple(m1),
        m15=tuple(m15),
        h4=(),
        trader=trader,
        bot=bot,
        resultado=resultado,
        parejas=parejas,
        hechos=HECHOS,
        sesgos=(),
        objetivo_rr=Decimal(3),
        motor="sintetico",
    )


# --------------------------------------------------------------------------------- compuerta


def test_se_niega_a_medida_y_a_lo_que_no_es_construccion() -> None:
    """Los mismos mensajes que el arnes: sale de `arnes.validar_meses`."""
    real = cargar_criterio(RAIZ)
    for mes in real.medida:
        with pytest.raises(ConjuntoError, match="MEDIDA"):
            caso_de_construccion(RAIZ, real, f"caso-x-{mes}-00")
    for mes in ("2026-02", "2026-03", "2026-09", "2030-01"):
        with pytest.raises(ConjuntoError, match="construccion"):
            caso_de_construccion(RAIZ, real, f"caso-x-{mes}-00")
    with pytest.raises(ConjuntoError, match="AAAA-MM-DD"):
        caso_de_construccion(RAIZ, real, "caso-sin-fecha")


def test_la_cli_se_niega_sin_escribir_nada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli

    salida = tmp_path / "visor"
    real = cargar_criterio(RAIZ)
    peticiones = [
        ["--caso", f"caso-x-{real.medida[0]}-00"],
        ["--caso", "caso-x-2026-03-00"],
        ["--todos", "--meses", real.medida[0]],
        ["--todos", "--meses", "2026-03"],
    ]
    for peticion in peticiones:
        codigo = cli.main(
            ["--repo", str(RAIZ), "motor", "visor", *peticion, "--salida", str(salida)]
        )
        assert codigo == 2, peticion
        assert not salida.exists()
    err = capsys.readouterr().err
    assert "MEDIDA" in err and "construccion" in err


def test_centinela_un_dia_oculto_no_se_lee(tmp_path: Path) -> None:
    """Un fixture con un dia reservado: si el visor lo leyera, el YAML roto reventaria y el
    centinela apareceria. Ni pidiendo ese caso ni pidiendo otro del mismo mes se abre."""
    centinela = "CENTINELA-visor-4b1e"
    dev = tmp_path / "knowledge" / "cases" / "dev"
    dev.mkdir(parents=True)
    oculto, visible = "caso-x-2030-01-02", "caso-x-2030-01-03"
    (dev / f"{oculto}.yaml").write_text(f"{centinela}: [roto\n", encoding="utf-8")
    (dev / f"{visible}.yaml").write_text("operaciones: []\n", encoding="utf-8")
    asignaciones = {"2030-01": {oculto: "dev", visible: "dev"}}
    for pedido in (oculto, visible):
        with pytest.raises(HoldoutCerradoError) as exc:
            caso_de_construccion(
                tmp_path, _criterio(), pedido, ocultos={oculto}, asignaciones=asignaciones
            )
        assert centinela not in str(exc.value) and "2030-01-02" not in str(exc.value)
    # el centinela esta vivo: sin la compuerta, el fichero SI se leeria y reventaria
    with pytest.raises(YamlError):
        caso_de_construccion(
            tmp_path, _criterio(), visible, ocultos=set(), asignaciones=asignaciones
        )
    # con el oculto fuera del reparto, el visible se lee y el pedido que no existe se nombra
    solo_visible = {"2030-01": {visible: "dev"}}
    assert (
        caso_de_construccion(
            tmp_path, _criterio(), visible, ocultos=set(), asignaciones=solo_visible
        ).id
        == visible
    )
    with pytest.raises(ConjuntoError, match="no es un dia dev de construccion"):
        caso_de_construccion(
            tmp_path, _criterio(), "caso-x-2030-01-09", ocultos=set(), asignaciones=solo_visible
        )


# ------------------------------------------------------------------------------------ render


def test_determinismo_byte_a_byte(registro: Registro, tmp_path: Path) -> None:
    d = _dia(registro)
    assert render_dia(d).encode("utf-8") == render_dia(d).encode("utf-8")
    uno = visor.generar([d], tmp_path / "a", "sintetico", con_indice=True)
    dos = visor.generar([d], tmp_path / "b", "sintetico", con_indice=True)
    assert [p.name for p in uno] == [p.name for p in dos] == [f"{d.caso}.html", visor.INDICE]
    for a, b in zip(uno, dos, strict=True):
        assert a.read_bytes() == b.read_bytes()


def test_un_dia_sintetico_aparece_donde_debe(registro: Registro) -> None:
    d = _dia(registro)
    pagina = render_dia(d)
    desde, hasta = d.ventana_utc
    precios = [int(p) for v in d.m1 for p in (v.minima, v.maxima)]
    for op in (*d.trader, *d.bot):
        precios.append(int((op.entrada * ESCALA).to_integral_value()))
        if op.stop is not None:
            precios.append(int((op.stop * ESCALA).to_integral_value()))
    margen = max((max(precios) - min(precios)) // 20, 1)
    lienzo = Lienzo(desde, hasta, min(precios) - margen, max(precios) + margen)

    # cada operacion, en su instante de llenado y a su precio
    for op in (*d.trader, *d.bot):
        x = lienzo.x(a_minuto(op.instante.replace(second=0)))
        y = lienzo.y(int((op.entrada * ESCALA).to_integral_value()))
        assert f'<circle class="llenado" cx="{x:.1f}" cy="{y:.1f}"' in pagina, op
    # el stop del trader, y el objetivo derivado por objetivo_rr, con su aviso
    stop = lienzo.y(int((d.trader[0].stop or 0) * ESCALA))
    assert '<line class="stop" x1="' in pagina and f'y1="{stop:.1f}"' in pagina
    assert "objetivo DERIVADO por regla (objetivo_rr), no del caso" in pagina
    # la pareja del criterio: la compra del trader con la del bot, y la venta sin pareja
    assert len(d.parejas) == 1
    assert pagina.count('<line class="pareja"') == 1
    assert "pareja: Δ 40 s, 2.00000 puntos" in pagina
    # la tabla de operaciones, con el criterio
    assert "<td>trader</td><td>07-11</td><td>compra</td><td>09:05:20</td>" in pagina
    assert "<td>bot</td><td>07-11</td><td>compra</td><td>09:06:00</td>" in pagina
    assert "<td>trader</td><td>11-15</td><td>venta</td><td>13:00:00</td>" in pagina
    assert pagina.count("pareja 1") == 2
    # por sesion: sesgo, embudo, donde se para, no implementadas, bloqueadas y avisos H3
    assert "<b>Sesgo anotado por el motor:</b> alcista" in pagina
    assert "<b>Sesgo anotado por el motor:</b> bajista" in pagina
    assert "sesgo:si · liquidez_tomada:si" in pagina
    assert "sesgo:si · liquidez_tomada:no[predicado:alcanza_nivel]" in pagina
    assert "<b>Donde se para:</b> produce todos los hechos" in pagina
    assert (
        "<b>Donde se para:</b> liquidez_tomada:no[predicado:alcanza_nivel]; bloqueado por gate "
        "desconocido:abrir_operacion"
    ) in pagina
    assert "RN-015: accion:colocar_orden_limite: gate desconocido:abrir_operacion" in pagina
    assert "gate RN-001, RN-033" in pagina
    # los hechos, en la calle de cada uno y en su instante
    for instante, _, hecho, valor in (
        *d.resultado.sesiones["07-11"].fijados,
        *d.resultado.sesiones["11-15"].fijados,
    ):
        assert f'data-instante="{instante}"' in pagina
        assert f"{hecho}={valor}" in pagina
    # M1 y M15, ambos en la pagina, conmutables por CSS y sin JavaScript
    assert pagina.count('<rect class="sube"') + pagina.count('<rect class="baja"') == len(
        d.m1
    ) + len(d.m15)
    assert "<script" not in pagina and "#m15:checked" in pagina


def test_sin_mirar_al_futuro(registro: Registro) -> None:
    """Con `hasta` la vista no ensena ningun hecho fijado despues, ni velas cerradas despues, ni
    operaciones llenadas despues; y un hecho nunca aparece antes de su instante."""
    d = _dia(registro)
    liquidez = next(
        t for t, _, h, _ in d.resultado.sesiones["07-11"].fijados if h == "liquidez_tomada"
    )
    antes, justo = MinutoUtc(liquidez - 1), MinutoUtc(liquidez)
    pagina_antes, pagina_justo = render_dia(d, antes), render_dia(d, justo)
    assert f'data-instante="{liquidez}"' not in pagina_antes
    assert f'data-instante="{liquidez}"' in pagina_justo
    assert "liquidez_tomada:no[productoras sin cumplirse]" in pagina_antes
    assert "liquidez_tomada:si" in pagina_justo
    assert "sesgo=bajista" not in pagina_antes and "sesgo=alcista" in pagina_antes
    assert "vista hasta las" in pagina_antes
    velas = pagina_antes.count('<rect class="sube"') + pagina_antes.count('<rect class="baja"')
    assert velas == sum(1 for v in (*d.m1, *d.m15) if v.fin <= antes)
    assert "<td>trader</td>" not in pagina_antes and '<line class="pareja"' not in pagina_antes
    completa = render_dia(d)
    for instante, _, _, _ in d.resultado.sesiones["07-11"].fijados:
        assert f'data-instante="{instante}"' in completa
        assert f'data-instante="{instante}"' not in render_dia(d, MinutoUtc(instante - 1))


def test_el_indice_enlaza_cada_dia_y_dice_donde_se_para(registro: Registro, tmp_path: Path) -> None:
    d = _dia(registro)
    otro = DiaVisor(
        **{
            **d.__dict__,
            "caso": "caso-x-2030-01-16",
            "dia": date(2030, 1, 16),
            "bot": (),
            "parejas": (),
        }
    )
    escritos = visor.generar([otro, d], tmp_path, "sintetico", con_indice=True)
    assert [p.name for p in escritos] == [f"{d.caso}.html", f"{otro.caso}.html", visor.INDICE]
    indice = (tmp_path / visor.INDICE).read_text(encoding="utf-8")
    assert indice.index(f'href="{d.caso}.html"') < indice.index(f'href="{otro.caso}.html"')
    fila = visor.fila_indice(d)
    assert (
        fila.sesiones_con_trader,
        fila.operaciones_trader,
        fila.operaciones_bot,
        fila.parejas,
    ) == (2, 2, 1, 1)
    assert fila.sesgos == "07-11 alcista; 11-15 bajista"
    assert fila.parada.startswith("07-11: produce todos los hechos; 11-15: liquidez_tomada:no[")
    assert "<td>2</td><td>2</td><td>1</td><td>1</td>" in indice
    assert "<script" not in indice


def test_la_salida_esta_ignorada_por_git() -> None:
    r = subprocess.run(
        ["git", "check-ignore", "-q", str(visor.CARPETA_SALIDA / "x.html")],
        cwd=RAIZ,
        capture_output=True,
        check=False,
    )
    assert r.returncode == 0, "data/visor/ tiene que estar ignorada: la salida no se comitea"


def test_el_embudo_lee_como_el_arnes() -> None:
    traza = TrazaSesion(
        fijados=[(5, "RN-003", "sesgo", "no")], no_implementadas={("RN-004", "predicado:cruza")}
    )
    assert visor.embudo_de_sesion(traza, HECHOS) == [
        ("sesgo", "no[productoras sin cumplirse]"),
        ("liquidez_tomada", "no[predicado:cruza]"),
    ]
    assert visor.donde_se_para(traza, HECHOS) == "sesgo:no[productoras sin cumplirse]"


def test_por_la_cli_sobre_un_dia_dev_de_construccion_si_hay_datos(tmp_path: Path) -> None:
    """Con `data/` en la maquina: una pagina por el caso, y dos ejecuciones dan los mismos bytes.
    Abril es material de desarrollo (sin dias reservados); sin datos, se salta."""
    from botsito import cli
    from botsito.cases import visto

    real = cargar_criterio(RAIZ)
    mes = real.construccion[0]
    if mes not in visto.artefactos(RAIZ):
        pytest.skip("sin reparto dev-visto")
    caso = sorted(c for c, p in visto.asignacion(RAIZ, mes).items() if p == "dev")[0]
    salida = tmp_path / "visor"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "visor", "--caso", caso, "--salida", str(salida)]
    )
    if codigo == 2:
        pytest.skip("sin dataset en esta maquina")
    assert codigo == 0
    pagina = salida / f"{caso}.html"
    primero = pagina.read_bytes()
    assert (
        cli.main(["--repo", str(RAIZ), "motor", "visor", "--caso", caso, "--salida", str(salida)])
        == 0
    )
    assert pagina.read_bytes() == primero
    assert not (salida / visor.INDICE).exists()
    assert b"<script" not in primero
