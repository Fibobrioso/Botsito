"""El dibujo y la sustentacion de las laminas (`engine/laminas_svg.py` y `laminas.componer`) sobre
FOTOS HECHAS A MANO: una con todo -sesgo con dos H4 saltadas, la toma, dos lineas de M15, la caja y
su punto- y sus variantes. El dibujo solo ve la foto, asi que «sin mirar al futuro» se prueba
dandole velas posteriores al corte: tiene que cortar por `foto.corte` (la mutacion es un dibujo que
no corta)."""

from __future__ import annotations

import dataclasses
import re
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import cargar_registro
from botsito.data.agregacion import agregar
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import laminas, laminas_svg

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
HUSO = "Europe/Madrid"
ESCALA = 100_000
CORTE = int(datetime(2030, 1, 15, 9, 0, tzinfo=UTC).timestamp()) // 60  # 10:00 en Madrid
DESDE = CORTE - 4 * 1440
SESION = int(datetime(2030, 1, 15, 6, 0, tzinfo=UTC).timestamp()) // 60
LIMITES = (("07-11", SESION, SESION + 240), ("11-15", SESION + 240, SESION + 480))
LECTURA = laminas.Lectura(
    REGISTRO.opcion("liquidez_m15_criterio_toma"),
    REGISTRO.fraccion("stop_fraccion_caja").valor,
    REGISTRO.entero("zonas_control_max_por_esquema"),
    REGISTRO.hora("anclaje_h4"),
    REGISTRO.opcion("perdida_trader_reinicio"),
)


def _m1(desde: int, hasta: int) -> tuple[Vela, ...]:
    """M1 en zigzag: media hora sube, media hora baja."""
    velas, p = [], 110_000
    for k, m in enumerate(range(desde, hasta)):
        c = p + (7 if (k // 30) % 2 == 0 else -7)
        velas.append(
            Vela(
                MinutoUtc(m), Puntos(p), Puntos(max(p, c) + 2), Puntos(min(p, c) - 2), Puntos(c), 1
            )
        )
        p = c
    return tuple(velas)


M1 = _m1(DESDE, CORTE)
H4 = agregar(list(M1), 240, REGISTRO.hora("anclaje_h4"))
FIJA, SALTADA_1, SALTADA_2 = (int(v.inicio) for v in H4[-5:-2])
TOMA = CORTE - 30
FORMADO = CORTE - 185


def foto_base(**cambios: Any) -> laminas.Foto:
    f = laminas.Foto(
        dia="2030-01-15",
        sesion="07-11",
        corte=CORTE,
        huso=HUSO,
        escala=ESCALA,
        limites=LIMITES,
        desde_h4=DESDE,
        desde_m15=CORTE - 1440,
        desde_m1=SESION - 60,
        m1=M1,
        hechos=(("liquidez_tomada", "si"), ("sesgo", "alcista")),
        origen=(),
        broker=(("operacion_abierta", "False"), ("orden_limite_pendiente", "False")),
        anotaciones=(
            ("sesgo_h4", "alcista"),
            ("sesgo_h4_saltadas", f"{SALTADA_2}:color_contrario,{SALTADA_1}:color_contrario"),
            ("sesgo_h4_saltadas_color_contrario", "2"),
            ("sesgo_h4_vela", str(FIJA)),
        ),
        escenarios=(
            laminas.EscenarioFoto(
                1, laminas.TomaFoto(TOMA, "compra", "bajo", 109_990, FORMADO), ("zona:1",), None
            ),
        ),
        zonas=(
            laminas.ZonaFoto(
                "zona:1", "compra", 110_010, 109_980, "primer_esquema", CORTE - 20, CORTE - 10
            ),
        ),
        puntos=(("zona:1", f"110010@{CORTE - 20}"),),
        usadas=frozenset(),
        rechazados=frozenset(),
        ordenes=(),
        colocadas=frozenset(),
        movidas=frozenset(),
        posiciones=(),
        lineas=(
            laminas.LineaM15("alto", 110_060, CORTE - 300, CORTE - 290, CORTE - 280, CORTE - 100),
            laminas.LineaM15("bajo", 109_990, CORTE - 200, FORMADO, CORTE - 180, CORTE),
        ),
        prohibido=(),
        quizas=(),
        bloqueos=(),
        disparadas=(),
        no_enviadas=(),
    )
    return dataclasses.replace(f, **cambios)


def _lamina(
    f: laminas.Foto, tipo: str = laminas.TIPO_B, orden: str | None = None
) -> laminas.Lamina:
    return laminas.Lamina(laminas.Pedida(1, f.dia, "07-11"), tipo, f, orden)


def _pagina(
    f: laminas.Foto, tipo: str = laminas.TIPO_B, orden: str | None = None
) -> tuple[str, laminas.Composicion]:
    comp = laminas.componer(_lamina(f, tipo, orden), LECTURA)
    return laminas_svg.pagina(comp, 1, "La sesión de las 07:00 a las 11:00"), comp


def test_la_foto_con_todo_dibuja_cada_marca_con_su_clase() -> None:
    texto, comp = _pagina(foto_base())
    for clase in ('class="h4-fija"', 'class="h4-saltada"', 'class="linea-m15 bajo tomada"',
                  'class="linea-m15 alto dejo"', 'class="caja compra"', 'class="nivel"',
                  'class="punto"', 'class="toma"', 'class="corte"'):  # fmt: skip
        assert clase in texto, clase
    assert texto.count('class="h4-saltada"') == 2
    for rotulo in (">0<", ">0,25<", ">0,5<", ">0,8<", ">1<"):
        assert rotulo in texto, rotulo
    assert comp.fija_dentro is True


def test_la_sustentacion_de_la_foto_con_todo() -> None:
    _, comp = _pagina(foto_base())
    assert comp.frases == (
        "Sesgo de H4 alcista: la vela H4 que lo fija rompió el alto de la anterior y cerró verde.",
        "Antes de esa vela saltó 2 velas H4 que rompieron un extremo y cerraron del color "
        "contrario.",
        "Liquidez de M15 tomada: una vela de M1 cerró con cuerpo por debajo del bajo de M15 en "
        "1.09990, a las 09:30.",
        "Sigue la liquidez de M15 número 1 de esta sesión.",
        "Es el primer esquema.",
        "La caja va de 1.10010 (el 0) a 1.09980 (el 1).",
        "El punto de breaker está en 1.10010, de la vela de las 09:40.",
        "Con la caja formada, todavía no le toca colocar la orden.",
    )


def test_el_dibujo_corta_por_el_corte_aunque_la_foto_traiga_velas_despues() -> None:
    con_futuro = foto_base(m1=M1 + _m1(CORTE, CORTE + 120))
    limpio, _ = _pagina(foto_base())
    sucio, _ = _pagina(con_futuro)
    assert sucio == limpio


def test_la_caja_que_nace_en_el_propio_cierre_del_corte_se_dibuja() -> None:
    """El ensayo de F4.3 lo destapo: la caja de la orden que se coloca en el corte nace en ese
    mismo cierre (`formada` = el corte, el cierre del breaker), y su vela es la ultima M1."""
    zona = laminas.ZonaFoto(
        "zona:1", "compra", 110_010, 109_980, "primer_esquema", CORTE - 3, CORTE
    )
    texto, comp = _pagina(foto_base(zonas=(zona,)))
    assert "La caja va de 1.10010 (el 0) a 1.09980 (el 1)." in comp.frases
    assert 'class="caja compra"' in texto
    fuera = dataclasses.replace(zona, formada=SESION - 60)  # su vela, antes de la ventana de M1
    _, comp = _pagina(foto_base(zonas=(fuera,)))
    assert "La caja viene de antes de la ventana." in comp.frases


def test_lo_nacido_antes_de_la_ventana_no_se_dibuja_ni_da_precio() -> None:
    """Las dos lineas y la H4 que fija nacen antes de sus ventanas: no salen, y la sustentacion
    dice que vienen de antes. La toma, dentro, sale sin el precio de la linea."""
    f = foto_base(desde_m15=CORTE - 150, desde_h4=SALTADA_2)
    texto, comp = _pagina(f)
    assert "linea-m15" not in texto and 'class="h4-fija"' not in texto and "1.09990" not in texto
    assert "La vela H4 que fija el sesgo viene de antes de la ventana." in comp.frases
    assert "2 líneas de M15 de esta sesión vienen de antes de la ventana." in comp.frases
    assert any(
        x.startswith("Liquidez de M15 tomada a las 09:30: la línea que toma viene de antes")
        for x in comp.frases
    )
    assert comp.fija_dentro is False


def test_la_orden_colocada_y_la_viva_dicen_su_0_su_stop_y_su_objetivo() -> None:
    orden = laminas.OrdenFoto(
        "o1",
        "compra",
        110_010,
        109_986,
        110_100,
        (CORTE - 1) * 60_000 + 59_999,
        "colocada",
        "07-11",
        "zona:1",
    )
    f = foto_base(
        ordenes=(orden,),
        colocadas=frozenset({"o1"}),
        broker=(("operacion_abierta", "False"), ("orden_limite_pendiente", "True")),
    )
    texto, comp = _pagina(f, laminas.TIPO_A, "o1")
    assert ("Coloca la orden de compra en 1.10010, el 0 de la caja, con el stop en 1.09986 (el 0,8 "
            "redondeado) y el objetivo en 1.10100.") in comp.frases  # fmt: skip
    for clase in ('class="orden"', 'class="stop"', 'class="objetivo"'):
        assert clase in texto
    _, viva = _pagina(f)
    assert any(x.startswith("Tiene una orden de compra pendiente en 1.10010") for x in viva.frases)
    fuera_del_0 = dataclasses.replace(orden, precio=110_011)
    with pytest.raises(laminas.LaminaError):
        _pagina(dataclasses.replace(f, ordenes=(fuera_del_0,)), laminas.TIPO_A, "o1")


def test_lo_de_antes_del_corte_se_cuenta_sin_resultados() -> None:
    o = [
        laminas.OrdenFoto(f"o{k}", "compra", 110_010, 109_986, 110_100, 0, e, "07-11", "zona:1")
        for k, e in ((1, "llenada"), (2, "llenada"), (3, "cancelada"), (4, "rechazada"))
    ]
    p = (
        laminas.PosicionFoto("o1", 1, (CORTE - 50) * 60_000, "stop"),
        laminas.PosicionFoto("o2", 1, (CORTE - 40) * 60_000, "objetivo"),
    )
    _, comp = _pagina(foto_base(ordenes=tuple(o), posiciones=p))
    assert "Antes, en esta sesión: 1 cerrada en el stop y 1 en el objetivo." in comp.frases
    assert "Una orden anterior se retiró sin llenarse." in comp.frases
    assert "El bróker rechazó una orden anterior." in comp.frases
    assert "En esta liquidez ya lleva un stop." in comp.frases
    with pytest.raises(laminas.LaminaError, match="cierre"):
        _pagina(
            foto_base(
                ordenes=tuple(o), posiciones=(dataclasses.replace(p[0], motivo_cierre="otro"),)
            )
        )


def test_por_que_no_hay_orden_sale_de_la_lista_cerrada() -> None:
    _, comp = _pagina(
        foto_base(
            prohibido=(("abrir_operacion", ("RN-033",)),),
            quizas=(("abrir_operacion", ("RN-005",)),),
            no_enviadas=((1, "zona:1", "no_operar:volumen+margen"),),
            usadas=frozenset({"zona:1"}),
            rechazados=frozenset({f"110010@{CORTE - 20}"}),
        )
    )
    assert "Esa caja ya tuvo su orden." in comp.frases
    assert "Ese punto ya se gastó: el bróker rechazó la orden." in comp.frases
    assert ("Iba a colocar la orden y no la envía: no cabe en la cuenta (por el volumen máximo y "
            "por el margen).") in comp.frases  # fmt: skip
    assert "No abre: no hay sesgo de H4 claro." in comp.frases
    assert ("No abre porque no puede descartar que lo que se forma queda en la zona de ruido de la "
            "liquidez de M15, donde no se busca entrada.") in comp.frases  # fmt: skip
    assert "Con la caja formada, todavía no le toca colocar la orden." not in comp.frases


def test_rn009_dice_cuantas_zonas_conto_y_las_dibuja() -> None:
    anot = dict(foto_base().anotaciones)
    anot["zonas_de_control"] = f"{CORTE}|110000@{CORTE - 15},109995@{CORTE - 8}"
    f = foto_base(
        anotaciones=tuple(sorted(anot.items())), prohibido=(("abrir_operacion", ("RN-009",)),)
    )
    texto, comp = _pagina(f)
    m = LECTURA.zonas_max
    assert (
        f"No abre: el esquema tiene más zonas de control de las que admite (2, y admite {m})."
        in comp.frases
    )
    assert texto.count('class="zona-control"') == 2
    viejo = dict(anot)
    viejo["zonas_de_control"] = f"{CORTE - 1}|110000@{CORTE - 15}"
    with pytest.raises(laminas.LaminaError, match="RN-009"):
        _pagina(
            foto_base(
                anotaciones=tuple(sorted(viejo.items())),
                prohibido=(("abrir_operacion", ("RN-009",)),),
            )
        )


def test_el_html_es_autocontenido_sin_script_ni_fechas_y_determinista() -> None:
    uno, _ = _pagina(foto_base())
    dos, _ = _pagina(foto_base())
    assert uno.encode("utf-8") == dos.encode("utf-8")
    assert (
        "<script" not in uno
        and "<title" not in uno
        and "<!--" not in uno
        and "http" not in uno.replace("http://www.w3.org/2000/svg", "")
    )
    laminas.comprobar_texto("lamina-01.html", uno)
    assert not re.search(r"\son[a-z]+=", uno)


def test_los_colores_salen_de_la_tabla_unica() -> None:
    texto, _ = _pagina(foto_base())
    usados = set(re.findall(r"#[0-9a-f]{6}", texto))
    assert usados <= set(laminas_svg.COLOR.values())
    assert Decimal(laminas_svg.OPACIDAD_CAJA) < 1
