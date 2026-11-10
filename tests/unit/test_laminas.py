"""Las laminas del bot (`engine/laminas.py`, rama trabajo/laminas) sobre el dia SINTETICO de 2030 de
`test_cableado.py`, ampliado: ningun test lee velas, ticks ni operaciones reales (respuesta del
consultor a la fase 0, «lo demas queda aprobado»). La estrategia sintetica liga dos zonas y escribe
la toma, el escenario y el punto en la memoria con las MISMAS funciones de `engine/zonas.py` que
usa el motor, asi que la forma de la memoria es la real. Se prueba: que el motor decide lo mismo
con el recolector (golden) y que la mutacion lo ve; que la foto no mira al futuro y que un
recolector con la referencia viva si (mutacion); que salen exactamente las laminas (a) y (b); la
puerta; la tabla de frases; las fechas, los ids y el dinero; la salida; y el determinismo."""

from __future__ import annotations

import argparse
import re
from collections.abc import Mapping
from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.criterio_fidelidad import Operacion
from botsito.cli import build_parser
from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.domain.pivotes_m15 import BAJO, CIERRE_VELA_CONTRARIA
from botsito.engine import arnes, cableado, laminas, zonas
from botsito.engine.cableado import Cierre, MotorCableado
from botsito.engine.interprete import EstadoDia, Momento, NoImplementada, Resultado, Tri
from botsito.engine.motor import DatosMercado, DiaDeMercado
from botsito.engine.zonas import Zona
from tests.unit.test_cableado import (
    BASE,
    DIA,
    ENTRADA,
    ESCALA,
    EXTREMO,
    HUSO,
    MINUTO_ZONA,
    SESIONES,
    _criterio,
    _h4_alcista,
    _mercado,
    _motor,
)
from tests.unit.test_decisiones import _foto

RAIZ = Path(__file__).resolve().parents[2]
CLAVE = DIA.isoformat()
# una bajada y una subida antes de la zona dejan un BAJO de M15 formado (la liquidez); despues, la
# ruta de RUTA_STOP: la primera orden se llena y salta el stop
RUTA = {
    MINUTO_ZONA - 50: BASE - 30,
    MINUTO_ZONA - 35: BASE,
    MINUTO_ZONA + 3: ENTRADA - 2,
    MINUTO_ZONA + 6: ENTRADA - 17,
}
SEGUNDA = MINUTO_ZONA + 60  # la segunda orden, muy por debajo: no se llena, se retira al final
ENTRADA_2, EXTREMO_2 = ENTRADA - 60, ENTRADA - 80
TRADER_B = MINUTO_ZONA + 90  # una operacion del trader sin pareja: lamina (b), con la segunda viva
PUERTA = laminas.Puerta(((date(2030, 1, 10), date(2030, 1, 20)),), frozenset(), HUSO)


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    from botsito.spec.modelo import cargar_vocabulario

    return cargar_vocabulario(RAIZ / "knowledge" / "spec" / "strategy_spec.yaml")


def _lectura(registro: Registro) -> laminas.Lectura:
    return laminas.Lectura(
        registro.opcion("liquidez_m15_criterio_toma"),
        registro.fraccion("stop_fraccion_caja").valor,
        registro.entero("zonas_control_max_por_esquema"),
        registro.hora("anclaje_h4"),
        registro.opcion("perdida_trader_reinicio"),
    )


def _dia(registro: Registro, mercado: Any) -> DiaDeMercado:
    """El dia de `test_cableado.py` con las M15 y las M1 en los datos y la lectura de «formado»,
    para que haya liquidez de M15 que el recolector lea."""
    m1 = list(mercado.m1)
    anclaje = registro.hora("anclaje_h4")
    datos = DatosMercado(
        _h4_alcista(), agregar(m1, 15, anclaje), m1, CIERRE_VELA_CONTRARIA,
        registro.opcion("liquidez_m15_mecha_que_vuelve"),
        registro.opcion("liquidez_m15_criterio_toma"),
    )  # fmt: skip
    return DiaDeMercado(DIA, HUSO, SESIONES, datos)


def _estrategia(motor: MotorCableado) -> MotorCableado:
    """Sin estado (sirve para correr el dia dos veces): en MINUTO_ZONA abre el escenario con la
    toma de la liquidez de M15 de ese instante y liga `zona:1` con su punto, por las funciones de
    `engine/zonas.py`; en SEGUNDA liga `zona:2` al mismo escenario. `toca_colocar_orden_limite` da
    SI en esos dos minutos."""

    def toca(
        args: Mapping[str, Any], momento: Momento, estado: EstadoDia
    ) -> Resultado | NoImplementada:
        m = int(momento.instante)
        if m not in (MINUTO_ZONA, SEGUNDA):
            return Resultado(Tri.NO)
        mem = zonas._de_la_sesion(estado, momento.sesion)
        if not mem.get(zonas.ESCENARIOS):
            p = momento.datos.liquidez_m15(m - 2, BAJO)
            assert p is not None, "el dia sintetico tiene que dejar un BAJO de M15 formado"
            toma = {"instante": m - 2, "nivel": p.nivel, "lado": "compra",
                    "pivote": (p.lado, p.nivel, int(p.formado_en))}  # fmt: skip
            zonas._abrir(estado, momento.sesion, toma)
        zid = "zona:1" if m == MINUTO_ZONA else "zona:2"
        entrada, extremo = (ENTRADA, EXTREMO) if m == MINUTO_ZONA else (ENTRADA_2, EXTREMO_2)
        zonas._memoria(estado).setdefault("zonas", {})[zid] = Zona(
            zid, "compra", entrada, extremo, "primer_esquema", m - 3, m - 1
        )
        mem.setdefault("punto_de_zona", {})[zid] = f"{entrada}@{m - 3}"
        zonas._ligar_al_escenario(estado, momento.sesion, zid)
        return Resultado(Tri.SI, {"Z": zid})

    predicados = dict(motor.primitivas_extra)
    predicados["toca_colocar_orden_limite"] = toca
    motor.primitivas_extra = predicados
    z1 = cableado.zona_sintetica("zona:1", "compra", ENTRADA, EXTREMO, "primer_esquema")
    z2 = cableado.zona_sintetica("zona:2", "compra", ENTRADA_2, EXTREMO_2, "primer_esquema")
    motor.zonas_de = lambda md: {"zona:1": z1, "zona:2": z2}
    return motor


def _plantilla(registro: Registro, vocabulario: dict[str, Any]) -> MotorCableado:
    return _estrategia(_motor(registro, vocabulario, _mercado(RUTA)))


def _trader() -> list[Operacion]:
    """Una que empareja con la primera orden del bot y otra sin pareja (TRADER_B)."""

    def op(minuto: int, segundos: int, direccion: str, entrada: int) -> Operacion:
        instante = datetime.fromtimestamp(minuto * 60 + segundos, UTC)
        return Operacion(CLAVE, "07-11", direccion, instante, Decimal(entrada) / ESCALA)

    return [op(MINUTO_ZONA + 3, 0, "compra", ENTRADA), op(TRADER_B, 30, "venta", BASE + 77)]


def _limites(
    registro: Registro, vocabulario: dict[str, Any]
) -> dict[str, tuple[tuple[str, int, int], ...]]:
    d = _dia(registro, _mercado(RUTA))
    return {CLAVE: tuple((n, int(a), int(b)) for n, a, b in d.limites())}


def _correr_con(registro: Registro, dia: DiaDeMercado) -> Any:
    def correr(motor: MotorCableado) -> list[Operacion]:
        corrida = arnes.correr(
            "x",
            ("2030-01",),
            (arnes.DiaTrader("caso-x-2030-01-15", CLAVE, tuple(_trader())),),
            {CLAVE: dia},
            motor,
        )
        return [op for r in corrida.resultados for op in r.operaciones]

    return correr


def _generar(
    registro: Registro, vocabulario: dict[str, Any], puerta: laminas.Puerta = PUERTA
) -> tuple[dict[str, str], list[str]]:
    plantilla = _plantilla(registro, vocabulario)
    dia = _dia(registro, _mercado(RUTA))
    return laminas.generar(
        plantilla, plantilla.reglas, _correr_con(registro, dia),
        (laminas.Pedida(1, CLAVE, "07-11"),), _limites(registro, vocabulario), _trader(),
        _criterio().tolerancias, puerta, _lectura(registro),
    )  # fmt: skip


# --------------------------------------------------------------- lo que el motor decide no cambia


def test_con_el_recolector_el_motor_decide_lo_mismo(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    dia = _dia(registro, _mercado(RUTA))
    sin = _foto(m := _plantilla(registro, vocabulario), m.correr_dia(dia))
    con = _plantilla(registro, vocabulario)
    rec = laminas.Recolector(
        _limites(registro, vocabulario), {CLAVE: frozenset({TRADER_B})}, PUERTA
    )
    con.observador = rec
    assert _foto(con, con.correr_dia(_dia(registro, _mercado(RUTA)))) == sin
    assert rec.fotos_a and rec.fotos_b


def test_un_recolector_que_muta_el_estado_hace_fallar_la_comparacion(
    registro: Registro, vocabulario: dict[str, dict[str, Any]]
) -> None:
    sin = _foto(
        m := _plantilla(registro, vocabulario), m.correr_dia(_dia(registro, _mercado(RUTA)))
    )

    class Muta(laminas.Recolector):
        def __call__(self, c: Cierre) -> None:
            super().__call__(c)
            if c.instante == MINUTO_ZONA - 1:
                c.estado.hechos["detenido_por_cartuchos"] = "hasta_cartuchos_reinicio"

    con = _plantilla(registro, vocabulario)
    con.observador = Muta(_limites(registro, vocabulario), {}, PUERTA)
    assert _foto(con, con.correr_dia(_dia(registro, _mercado(RUTA)))) != sin


# ------------------------------------------------------------------------ las fotos y el corte


def _recolectado(
    registro: Registro, vocabulario: dict[str, Any], clase: type = laminas.Recolector
) -> Any:
    motor = _plantilla(registro, vocabulario)
    rec = clase(_limites(registro, vocabulario), {CLAVE: frozenset({TRADER_B})}, PUERTA)
    motor.observador = rec
    motor.correr_dia(_dia(registro, _mercado(RUTA)))
    return rec


def test_la_foto_no_mira_al_futuro(registro: Registro, vocabulario: dict[str, Any]) -> None:
    rec = _recolectado(registro, vocabulario)
    a = rec.fotos_a[(CLAVE, "o1")]
    assert a.corte == MINUTO_ZONA and a.orden("o1").estado == "colocada"
    assert all(int(v.inicio) < a.corte for v in a.m1) and int(a.m1[-1].inicio) == a.corte - 1
    assert not a.posiciones and a.orden("o2") is None  # ni el llenado ni la segunda
    b = rec.fotos_b[(CLAVE, TRADER_B)]
    assert b.orden("o2") is not None and b.orden("o2").estado == "colocada"
    assert all(int(v.inicio) < TRADER_B for v in b.m1)
    assert all(p.cerrada_ms is None or p.cerrada_ms < TRADER_B * 60_000 for p in b.posiciones)


def test_un_recolector_con_la_referencia_viva_ve_el_futuro_y_el_test_lo_caza(
    registro: Registro, vocabulario: dict[str, Any]
) -> None:
    """La mutacion de la referencia viva: guardar el `broker` del cierre en vez de copiarlo deja en
    la foto de la colocacion de o1 la orden o2, que nace una hora despues."""

    class Vivo(laminas.Recolector):
        def __call__(self, c: Cierre) -> None:
            super().__call__(c)
            if c.instante == MINUTO_ZONA:
                self.vivo = c.broker

    rec = _recolectado(registro, vocabulario, Vivo)
    assert rec.fotos_a[(CLAVE, "o1")].orden("o2") is None
    assert "o2" in rec.vivo.ordenes  # lo que habria visto un dibujo hecho al final


# --------------------------------------------------------------------------------- las laminas


def test_salen_exactamente_la_de_la_orden_llenada_y_la_del_trader_sin_pareja_en_orden(
    registro: Registro, vocabulario: dict[str, Any]
) -> None:
    ficheros, resumen = _generar(registro, vocabulario)
    assert sorted(ficheros) == [
        "clave.txt", "sesion-01/indice.html", "sesion-01/lamina-01.html",
        "sesion-01/lamina-02.html",
    ]  # fmt: skip
    clave = ficheros["clave.txt"]
    assert "lamina-01.html: 2030-01-15, sesion 07-11" in clave and "tipo a" in clave
    assert "lamina-02.html" in clave and "tipo b" in clave
    a, b = ficheros["sesion-01/lamina-01.html"], ficheros["sesion-01/lamina-02.html"]
    assert "Coloca la orden de compra en 1.09995, el 0 de la caja" in a
    assert "Tiene una orden de compra pendiente en 1.09935" in b
    assert "Antes, en esta sesión: 1 cerrada en el stop." in b
    assert "En esta liquidez ya lleva un stop." in b
    # la operacion del trader no se dibuja: ni su direccion ni su precio
    assert "1.10077" not in b and "de venta" not in b
    assert resumen == ["sesion-01: 2 laminas; la H4 que fija el sesgo, dentro en 0 y fuera en 2"]


def test_las_marcas_salen_con_su_clase_y_ninguna_a_la_derecha_del_corte(
    registro: Registro, vocabulario: dict[str, Any]
) -> None:
    ficheros, _ = _generar(registro, vocabulario)
    a = ficheros["sesion-01/lamina-01.html"]
    for clase in ('class="caja compra"', 'class="nivel"', 'class="orden"', 'class="stop"',
                  'class="objetivo"', 'class="punto"', 'class="linea-m15 bajo tomada"',
                  'class="toma"'):  # fmt: skip
        assert clase in a, clase
    derecha = 1600 - 110
    for x in re.findall(r'\sx2?="([\d.]+)"', a):
        assert float(x) <= derecha + 1e-6 or float(x) >= derecha + 8  # los precios del eje


def test_sin_fechas_ids_ni_dinero_y_determinista(
    registro: Registro, vocabulario: dict[str, Any]
) -> None:
    uno, _ = _generar(registro, vocabulario)
    dos, _ = _generar(registro, vocabulario)
    assert {k: v.encode("utf-8") for k, v in uno.items()} == {
        k: v.encode("utf-8") for k, v in dos.items()
    }
    for nombre, texto in uno.items():
        if nombre == "clave.txt":
            continue
        assert not laminas.RE_FECHA.search(texto) and not laminas.RE_FECHA.search(nombre)
        assert not laminas.RE_PROHIBIDO.search(texto)
        assert "<script" not in texto and "<title" not in texto and "<!--" not in texto


def test_la_regex_de_fechas_lleva_limites_de_palabra() -> None:
    assert laminas.RE_FECHA.search("el 3 de mayo")
    assert not laminas.RE_FECHA.search("otro rango mayor")
    for fecha in ("2026-07-03", "03/07", "03-07", "julio", "July"):
        assert laminas.RE_FECHA.search(fecha), fecha
    for libre in ("1.14496", "a las 09:35", "H4", "M15", "mayormente", "marzos"):
        assert not laminas.RE_FECHA.search(libre), libre
    with pytest.raises(laminas.LaminaError):
        laminas.comprobar_texto("x.html", "sesión 07-11")
    with pytest.raises(laminas.LaminaError):
        laminas.comprobar_texto("x.html", "lo prohíbe RN-009")
    with pytest.raises(laminas.LaminaError):
        laminas.comprobar_texto("x.html", "<p onclick=x>")


# ---------------------------------------------------------------------------------- la puerta


def test_la_puerta_recorta_la_ventana_y_niega_el_corte_fuera() -> None:
    corte = int(datetime(2030, 1, 15, 9, 0, tzinfo=UTC).timestamp()) // 60
    desde = int(datetime(2030, 1, 9, 0, 0, tzinfo=UTC).timestamp()) // 60
    # el 10 en Madrid empieza el 9 a las 23:00 UTC: el primer minuto que cumple en los dos relojes
    assert (
        PUERTA.recorte(desde, corte)
        == int(datetime(2030, 1, 10, 0, 0, tzinfo=UTC).timestamp()) // 60
    )
    oculto = laminas.Puerta(PUERTA.tramos, frozenset({(1, 13)}), HUSO)
    assert (
        oculto.recorte(desde, corte)
        == int(datetime(2030, 1, 14, 0, 0, tzinfo=UTC).timestamp()) // 60
    )
    fuera = laminas.Puerta(((date(2030, 1, 1), date(2030, 1, 14)),), frozenset(), HUSO)
    with pytest.raises(laminas.LaminaError):
        fuera.recorte(desde, corte)


def test_lo_que_no_cumple_la_puerta_no_sale(
    registro: Registro, vocabulario: dict[str, Any]
) -> None:
    """Con el dia del corte fuera de la puerta (en el huso de las sesiones el 15 es oculto), la
    corrida entera sale con error y no da ningun fichero. Lo nacido antes de la ventana con el
    corte dentro lo prueban las fotos hechas a mano (test_laminas_svg.py)."""
    oculto = laminas.Puerta(PUERTA.tramos, frozenset({(1, 15)}), HUSO)
    with pytest.raises(laminas.LaminaError, match="corte"):
        _generar(registro, vocabulario, oculto)


def test_un_dia_pedido_que_no_cumple_se_niega_antes_de_correr() -> None:
    limites = {CLAVE: (("07-11", 100, 200),)}
    pedidas = (laminas.Pedida(1, CLAVE, "07-11"),)
    with pytest.raises(laminas.LaminaError, match="dev"):
        laminas.comprobar_pedidas(pedidas, [], PUERTA, limites, {})
    with pytest.raises(laminas.LaminaError, match="dev"):
        laminas.comprobar_pedidas(
            pedidas, [CLAVE], laminas.Puerta(PUERTA.tramos, frozenset({(1, 15)}), HUSO), limites, {}
        )
    with pytest.raises(laminas.LaminaError, match="no es una sesion"):
        laminas.comprobar_pedidas(
            (laminas.Pedida(1, CLAVE, "11-15"),), [CLAVE], PUERTA, limites, {}
        )
    sesion = (("07-11", int(datetime(2030, 1, 15, 6, tzinfo=UTC).timestamp()) // 60,
               int(datetime(2030, 1, 15, 10, tzinfo=UTC).timestamp()) // 60),)  # fmt: skip
    with pytest.raises(laminas.LaminaError, match="hora perdida"):
        laminas.comprobar_pedidas(
            pedidas, [CLAVE], PUERTA, {CLAVE: sesion}, {CLAVE: ("2030-01-15T09Z",)}
        )
    laminas.comprobar_pedidas(
        pedidas, [CLAVE], PUERTA, {CLAVE: sesion}, {CLAVE: ("2030-01-15T10Z",)}
    )


def test_los_tramos_salen_de_cobertura_material_y_el_30_de_abril_queda_fuera() -> None:
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config

    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    meses = list(cargar_criterio(RAIZ).construccion)
    puerta = laminas.puerta_de(config.cobertura, meses, (), HUSO)
    assert puerta.dia_permitido(date(2026, 4, 29)) and not puerta.dia_permitido(date(2026, 4, 30))
    assert puerta.dia_permitido(date(2026, 7, 17)) and not puerta.dia_permitido(date(2026, 7, 18))
    assert not puerta.dia_permitido(date(2026, 1, 1)) and not puerta.dia_permitido(
        date(2026, 6, 30)
    )


# ------------------------------------------------------------------------- la tabla de frases


def test_la_tabla_de_gates_es_la_de_las_vigente_que_prohiben() -> None:
    from botsito.spec.modelo import cargar_reglas

    prohiben = {
        r.id for r in cargar_reglas(RAIZ / "knowledge" / "spec" / "strategy_spec.yaml")
        if r.estado == "VIGENTE"
        and ((getattr(r, "forma", None) or {}).get("entonces") or {}).get("prohibe")
    }  # fmt: skip
    assert set(laminas.MOTIVO_GATE) == prohiben and len(prohiben) == 15


def test_ninguna_frase_lleva_ids_dinero_ni_fechas() -> None:
    textos: list[str] = []
    for nombre, valor in vars(laminas).items():
        if not nombre.startswith(("FRASE_", "MOTIVO_GATE", "LIMITE_NO_ENVIO", "LADO_TOMA")):
            continue
        if isinstance(valor, str):
            textos.append(valor)
        elif isinstance(valor, dict):
            textos += [v for v in valor.values() if isinstance(v, str)]
            textos += [
                x for v in valor.values() if isinstance(v, tuple) for x in v if isinstance(x, str)
            ]
        elif isinstance(valor, tuple):
            textos += [x for x in valor if isinstance(x, str)]
    frases = [t for t in textos if t[:1].isupper() and t.endswith(".")]
    assert len(frases) > 30
    for t in frases:
        assert not laminas.RE_FECHA.search(t) and not laminas.RE_PROHIBIDO.search(t), t
    assert all("el único freno" not in t for t in textos)


def test_el_tope_dice_quien_lo_encendio_y_si_no_se_sabe_falla(registro: Registro) -> None:
    from tests.unit.test_laminas_svg import foto_base

    lectura = _lectura(registro)
    for reglas, frase in (
        (("RN-020",), "pérdida máxima del día del trader"),
        (("RN-029",), "freno diario de la cuenta"),
    ):
        f = foto_base(
            hechos=(("detenido_por_tope", "hasta_el_corte_siguiente"), ("sesgo", "alcista")),
            origen=(("detenido_por_tope", reglas),),
        )
        comp = laminas.componer(
            laminas.Lamina(laminas.Pedida(1, CLAVE, "07-11"), laminas.TIPO_B, f), lectura
        )
        assert any(frase in x for x in comp.frases)
    dudosas: tuple[tuple[str, ...], ...] = ((), ("RN-020", "RN-029"))
    for dudosa in dudosas:
        f = foto_base(
            hechos=(("detenido_por_tope", "hasta_el_corte_siguiente"), ("sesgo", "alcista")),
            origen=(("detenido_por_tope", dudosa),),
        )
        with pytest.raises(laminas.LaminaError, match="detenido_por_tope"):
            laminas.componer(
                laminas.Lamina(laminas.Pedida(1, CLAVE, "07-11"), laminas.TIPO_B, f), lectura
            )


def test_una_causa_o_un_valor_sin_frase_falla_con_su_nombre(registro: Registro) -> None:
    from tests.unit.test_laminas_svg import foto_base

    lectura = _lectura(registro)
    for cambio, nombre in (
        (
            {"hechos": (("sesgo", "alcista"), ("detenido_por_otra_cosa", "si"))},
            "detenido_por_otra_cosa",
        ),
        ({"prohibido": (("abrir_operacion", ("RN-999",)),)}, "RN-999"),
        ({"no_enviadas": ((1, "zona:1", "otro_limite"),)}, "otro_limite"),
    ):
        f = foto_base(**cambio)
        with pytest.raises(laminas.LaminaError, match=nombre):
            laminas.componer(
                laminas.Lamina(laminas.Pedida(1, CLAVE, "07-11"), laminas.TIPO_B, f), lectura
            )


# ------------------------------------------------------------------------------- la salida


def test_la_salida_dentro_del_repo_o_no_vacia_se_niega(tmp_path: Path) -> None:
    for mala in (RAIZ, RAIZ / "data" / "laminas", RAIZ / "docs"):
        with pytest.raises(laminas.LaminaError, match="dentro del repositorio"):
            laminas.comprobar_salida(mala, RAIZ)
    llena = tmp_path / "llena"
    llena.mkdir()
    (llena / "x").write_text("x", encoding="utf-8")
    with pytest.raises(laminas.LaminaError, match="no se pisa"):
        laminas.comprobar_salida(llena, RAIZ)
    assert laminas.comprobar_salida(tmp_path / "nueva", RAIZ) == (tmp_path / "nueva").resolve()


def test_la_cli_niega_la_salida_en_el_repo_antes_de_leer_nada(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from botsito import cli

    carpeta = RAIZ / "data" / "laminas-no"
    codigo = cli.main(
        [
            "--repo",
            str(RAIZ),
            "motor",
            "laminas",
            "--sesiones",
            "2026-07-03:07-11",
            "--salida",
            str(carpeta),
        ]
    )
    assert codigo == 2 and not carpeta.exists()
    assert "dentro del repositorio" in capsys.readouterr().err


def _hijo(parser: argparse.ArgumentParser, nombre: str) -> argparse.ArgumentParser:
    for accion in parser._actions:
        if isinstance(accion, argparse._SubParsersAction):
            return accion.choices[nombre]  # type: ignore[no-any-return]
    raise AssertionError(f"{parser.prog} sin subcomandos")


def _largas(sub: argparse.ArgumentParser) -> list[str]:
    return sorted(o for a in sub._actions for o in a.option_strings if o.startswith("--"))


def test_el_subcomando_tiene_sus_dos_opciones_obligatorias() -> None:
    sub = _hijo(_hijo(build_parser(), "motor"), "laminas")
    assert _largas(sub) == ["--help", "--salida", "--sesiones"]
    for faltan in (["--sesiones", "x:y"], ["--salida", "x"]):
        with pytest.raises(SystemExit):
            build_parser().parse_args(["motor", "laminas", *faltan])


# las opciones de los tres comandos que no cambian, leidas del parser de main (e5394c5)
OPCIONES_DE_MAIN = {
    "arnes": [
        "--depuracion",
        "--diagnostico-a27",
        "--diagnostico-a35",
        "--diagnostico-a44",
        "--diagnostico-a47",
        "--diagnostico-cuenta-diaria",
        "--fase",
        "--help",
        "--meses",
        "--perfil",
        "--salida",
        "--simular",
        "--tracemalloc",
    ],
    "visor": [
        "--caso",
        "--depuracion",
        "--diagnostico-a27",
        "--diagnostico-a35",
        "--diagnostico-a44",
        "--diagnostico-a47",
        "--diagnostico-cuenta-diaria",
        "--fase",
        "--hasta",
        "--help",
        "--meses",
        "--perfil",
        "--salida",
        "--simular",
        "--todos",
    ],
    "decisiones": [
        "--ablacion",
        "--ablacion-vigentes",
        "--bitacora",
        "--carpeta",
        "--help",
        "--meses",
    ],
}


def test_arnes_visor_y_decisiones_tienen_las_mismas_opciones_que_en_main() -> None:
    motor = _hijo(build_parser(), "motor")
    for nombre, opciones in OPCIONES_DE_MAIN.items():
        assert _largas(_hijo(motor, nombre)) == opciones, nombre


# ------------------------------------------------------------------------ una sola fuente

DE_DECISION = (
    "botsito.domain.sesgo",
    "botsito.domain.estructura_m1",
    "botsito.domain.pivotes_m15",
    "botsito.engine.zonas",
    "botsito.engine.primitivas",
    "botsito.engine.primitivas_broker",
    "botsito.engine.interprete",
)


def _importados(ruta: Path) -> list[tuple[str, str]]:
    import ast

    salida: list[tuple[str, str]] = []
    for nodo in ast.walk(ast.parse(ruta.read_text(encoding="utf-8"))):
        if isinstance(nodo, ast.Import):
            salida += [(a.name, "*") for a in nodo.names]
        elif isinstance(nodo, ast.ImportFrom) and nodo.module:
            salida += [(nodo.module, a.name) for a in nodo.names]
    return salida


def test_las_laminas_no_recalculan_ninguna_decision() -> None:
    """Punto 1 del encargo: de los modulos que deciden, las laminas solo importan CONSTANTES (los
    nombres de las anotaciones, los lados); el dibujo ni siquiera ve el cierre ni el motor."""
    motor = RAIZ / "src" / "botsito" / "engine"
    for fichero in ("laminas.py", "laminas_svg.py"):
        for modulo, nombre in _importados(motor / fichero):
            if modulo in DE_DECISION:
                assert nombre.isupper(), f"{fichero} importa {nombre} de {modulo}"
    for modulo, _ in _importados(motor / "laminas_svg.py"):
        assert modulo not in ("botsito.engine.cableado", "botsito.engine.motor"), modulo
