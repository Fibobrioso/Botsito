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
    REGISTRO.opcion("perdida_trader_alcance"),
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
# los niveles de las dos lineas: el extremo de una M1 de la ventana de M15 anterior a que se
# formen, como en la corrida (el nivel de un pivote es el extremo de su racha; revisor, b-I3)
ALTO_M15 = int(M1[CORTE - 305 - DESDE].maxima)
BAJO_M15 = int(M1[CORTE - 210 - DESDE].minima)
PRECIO_BAJO = laminas.precio(BAJO_M15, ESCALA)


def en_panel(texto: str, clase: str, k: int) -> int:
    """Cuantos elementos con `class` que empieza por `clase` caen en el panel k (0 H4, 1 M15, 2 M1,
    3 M1 de cerca), por su primera coordenada vertical."""
    import re as _re

    n = 0
    for e in _re.findall(rf'<(?:line|rect|circle|text) class="{clase}[^"]*"[^>]*>', texto):
        y = float(_re.search(r'\s(?:y|y1|cy)="([\d.]+)"', e).group(1))  # type: ignore[union-attr]
        n += k * laminas_svg.ALTO_PANEL <= y < (k + 1) * laminas_svg.ALTO_PANEL
    return n


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
                1, laminas.TomaFoto(TOMA, "compra", "bajo", BAJO_M15, FORMADO), ("zona:1",), None
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
            laminas.LineaM15("alto", ALTO_M15, CORTE - 300, CORTE - 290, CORTE - 280, CORTE - 100),
            laminas.LineaM15("bajo", BAJO_M15, CORTE - 200, FORMADO, CORTE - 180, CORTE),
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
    # la caja de la foto con todo es pequena: sus rotulos siguen la regla de `rotulos_visibles`
    for rotulo in (">0<", ">1<"):
        assert rotulo in texto, rotulo
    assert en_panel(texto, "nivel", 2) == 5 and en_panel(texto, "nivel", 3) == 5  # siempre
    assert comp.fija_dentro is True


def test_la_sustentacion_de_la_foto_con_todo() -> None:
    _, comp = _pagina(foto_base())
    assert comp.frases == (
        "Sesgo de H4 alcista: la vela H4 que lo fija rompió el alto de la anterior y cerró verde.",
        "Antes de esa vela, el bot se saltó 2 velas H4 que rompieron un extremo y cerraron del "
        "color contrario.",
        f"La vela de M1 de las 09:29 cerró con cuerpo por debajo del bajo de M15 en {PRECIO_BAJO}.",
        "Sigue la liquidez de M15 número 1 de esta sesión.",
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


def test_una_linea_cuyo_nivel_solo_lo_marca_una_vela_de_antes_no_sale() -> None:
    """Revisor, b-I3: la contraria de la linea nace dentro, pero ninguna M1 de la ventana de M15
    marca su nivel antes de que se forme (lo marcaria la racha de antes de la ventana): la linea no
    se dibuja ni da precio, y la toma de esa linea dice que viene de antes."""
    nivel = BAJO_M15 - 500  # ninguna M1 del zigzag llega ahi
    lineas = (laminas.LineaM15("bajo", nivel, CORTE - 200, FORMADO, CORTE - 180, CORTE),)
    toma = laminas.TomaFoto(TOMA, "compra", "bajo", nivel, FORMADO)
    f = foto_base(lineas=lineas, escenarios=(laminas.EscenarioFoto(1, toma, ("zona:1",), None),))
    texto, comp = _pagina(f)
    assert "linea-m15" not in texto and laminas.precio(nivel, ESCALA) not in texto
    assert "Una línea de M15 de esta sesión viene de antes de la ventana." in comp.frases
    assert any("la línea que toma viene de antes de la ventana" in x for x in comp.frases)


def test_lo_nacido_antes_de_la_ventana_no_se_dibuja_ni_da_precio() -> None:
    """Las dos lineas y la H4 que fija nacen antes de sus ventanas: no salen, y la sustentacion
    dice que vienen de antes. La toma, dentro, sale sin el precio de la linea."""
    f = foto_base(desde_m15=CORTE - 150, desde_h4=SALTADA_2)
    texto, comp = _pagina(f)
    assert "linea-m15" not in texto and 'class="h4-fija"' not in texto and PRECIO_BAJO not in texto
    assert "La vela H4 que fija el sesgo viene de antes de la ventana." in comp.frases
    assert "2 líneas de M15 de esta sesión vienen de antes de la ventana." in comp.frases
    assert any(
        x.startswith(
            "La vela de M1 de las 09:29 tomó la liquidez de M15: la línea que toma viene de antes"
        )
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
    assert en_panel(texto, "zona-control", 2) == 2 and en_panel(texto, "zona-control", 3) == 2
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


# ------------------------------------------------- la respuesta a la PARADA final (puntos 1 a 3)


def test_la_lamina_no_dice_el_esquema() -> None:
    """Punto 1: con la orden en el punto, toda zona nace con `por = primer_esquema`
    (zonas.py:414-416), asi que la lamina no dice un esquema que el motor no ha distinguido."""
    assert not hasattr(laminas, "FRASE_ESQUEMA")
    for por in ("primer_esquema", "segundo_esquema"):
        zona = dataclasses.replace(foto_base().zonas[0], por=por)
        _, comp = _pagina(foto_base(zonas=(zona,)))
        assert not [x for x in comp.frases if x.startswith("Es el ")]


def test_rn020_dice_del_dia_solo_si_la_rama_semanal_no_puede_disparar() -> None:
    """Punto 2: con el registro de hoy la rama semanal de RN-020 no dispara; si el alcance pasa a
    incluir la semana, la frase «del dia» falla con su nombre (negar por defecto)."""
    assert LECTURA.alcance_trader in laminas.ALCANCES_SOLO_DIA
    f = foto_base(prohibido=(("abrir_operacion", ("RN-020",)),))
    _, comp = _pagina(f)
    assert "No abre: ha llegado a la pérdida máxima del día del trader." in comp.frases
    for alcance in ("semana", "ambos"):
        lectura = dataclasses.replace(LECTURA, alcance_trader=alcance)
        with pytest.raises(laminas.LaminaError, match="perdida_trader_alcance"):
            laminas.componer(_lamina(f), lectura)
        tope = foto_base(
            hechos=(("detenido_por_tope", "hasta_el_corte_siguiente"), ("sesgo", "alcista")),
            origen=(("detenido_por_tope", ("RN-020",)),),
        )
        with pytest.raises(laminas.LaminaError, match="perdida_trader_alcance"):
            laminas.componer(_lamina(tope), lectura)


def test_el_gate_que_bloquea_y_prohibe_en_el_mismo_cierre_da_una_sola_frase() -> None:
    """Punto 3: el bloqueo de la colocacion y la prohibicion del efecto por el MISMO gate en el
    mismo cierre dan solo «Iba a colocar la orden y no la coloca»; otro gate que solo prohibe
    sigue con su «No abre»."""
    bloqueo = (("RN-015", "accion:colocar_orden_limite", "prohibida:abrir_operacion",
                (("RN-005", "dispara"),)),)  # fmt: skip
    f = foto_base(bloqueos=bloqueo, prohibido=(("abrir_operacion", ("RN-005", "RN-033")),))
    _, comp = _pagina(f)
    ruido = (
        "lo que se forma queda en la zona de ruido de la liquidez de M15, donde no se busca entrada"
    )
    assert f"Iba a colocar la orden y no la coloca: {ruido}." in comp.frases
    assert f"No abre: {ruido}." not in comp.frases
    assert "No abre: no hay sesgo de H4 claro." in comp.frases


def test_la_orden_que_nace_en_el_corte_se_ve_con_su_stop_y_su_objetivo() -> None:
    """Lo enseno la captura (respuesta a la PARADA final, punto 5): en una lamina de tipo a la
    orden se coloca en el mismo cierre del corte, y sus tres lineas no tenian largo. Ahora cubren
    la M1 que la coloca y llevan su precio en el eje derecho."""
    import re as _re

    orden = laminas.OrdenFoto(
        "o1", "compra", 110_010, 109_986, 110_100, CORTE * 60_000 - 1, "colocada", "07-11",
        "zona:1",
    )  # fmt: skip
    f = foto_base(ordenes=(orden,), colocadas=frozenset({"o1"}))
    texto, _ = _pagina(f, laminas.TIPO_A, "o1")
    for clase in ("orden", "stop", "objetivo"):
        linea = _re.search(rf'<line class="{clase}" x1="([\d.]+)" y1="[\d.]+" x2="([\d.]+)"', texto)
        assert linea is not None and float(linea.group(2)) - float(linea.group(1)) > 1, clase
        assert f'class="eje-{clase}"' in texto, clase
    for valor in ("1.10010", "1.09986", "1.10100"):
        assert f">{valor}<" in texto, valor


# ---------------------------------- la respuesta a la PARADA final de la ronda (puntos 1 a 3)


def _panel_m1() -> laminas_svg._Panel:
    return laminas_svg._Panel(M1[-240:], "M1", 2 * laminas_svg.ALTO_PANEL, ())


def test_los_rotulos_de_la_caja_siguen_la_regla() -> None:
    """Punto 1: los cinco si caben; si dos quedan a menos de la altura de su letra, el 0, el del
    stop y el 1; si aun asi se montan, el 0 y el 1. Con niveles puestos a pixeles conocidos."""
    p = _panel_m1()
    por_pixel = p.rango / (laminas_svg.ALTO_PANEL - laminas_svg.MARGEN_SUP - laminas_svg.MARGEN_INF)

    def niveles(*pixeles: float) -> list[tuple[str, int]]:
        rotulos = ("0", "0,25", "0,5", "0,8", "1")
        return [(r, int(p.hi - px * por_pixel)) for r, px in zip(rotulos, pixeles, strict=True)]

    def visibles(*pixeles: float) -> list[str]:
        return [r for r, _ in laminas_svg.rotulos_visibles(p, niveles(*pixeles))]

    assert visibles(0, 20, 40, 60, 80) == ["0", "0,25", "0,5", "0,8", "1"]
    assert visibles(0, 4, 8, 40, 60) == ["0", "0,8", "1"]  # el 0,25 y el 0,5 se montan
    assert visibles(0, 2, 4, 6, 8) == ["0", "1"]  # una caja diminuta
    assert visibles(0, 2, 4, 6, 7) == ["0", "1"]  # aunque el 0 y el 1 se monten, se quedan


def test_las_lineas_de_m15_lejanas_van_como_marca_en_el_m1_y_la_tomada_siempre() -> None:
    """Punto 2: una linea de M15 cuyo nivel queda lejos del rango del M1 (velas, caja y orden,
    ampliado una altura de caja) no se dibuja en el M1: va como una marca en el borde, con su
    precio y una flecha; en el M15 se dibuja. La tomada se dibuja en el M1 aunque quede lejos."""
    lejos_alto, lejos_bajo = 113_000, 107_000
    m1 = list(M1)
    i, j = CORTE - 500 - DESDE, CORTE - 400 - DESDE  # en la ventana de M15, antes de la de M1
    m1[i] = dataclasses.replace(m1[i], maxima=Puntos(lejos_alto))
    m1[j] = dataclasses.replace(m1[j], minima=Puntos(lejos_bajo))
    lineas = (
        laminas.LineaM15("alto", lejos_alto, CORTE - 495, CORTE - 490, CORTE - 480, CORTE),
        laminas.LineaM15("bajo", lejos_bajo, CORTE - 395, CORTE - 390, CORTE - 380, CORTE),
    )
    toma = laminas.TomaFoto(TOMA, "compra", "bajo", lejos_bajo, CORTE - 390)
    f = foto_base(
        m1=tuple(m1), lineas=lineas,
        escenarios=(laminas.EscenarioFoto(1, toma, ("zona:1",), None),),
    )  # fmt: skip
    texto, _ = _pagina(f)
    assert en_panel(texto, "linea-m15 alto viva", 1) == 1  # en el M15
    assert en_panel(texto, "linea-m15 alto viva", 2) == 0  # en el M1, no
    assert en_panel(texto, "linea-m15 bajo tomada", 2) == 1  # la tomada, en el M1 siempre
    assert f">▲ {laminas.precio(lejos_alto, ESCALA)}<" in texto
    assert en_panel(texto, "m15-fuera alto", 2) == 1 and en_panel(texto, "m15-fuera bajo", 2) == 0
    # y las que caen dentro del rango, como antes: la foto con todo no tiene ninguna marca
    base, _ = _pagina(foto_base())
    assert en_panel(base, "m15-fuera", 2) == 0 and en_panel(base, "linea-m15 bajo tomada", 2) == 1


def test_el_precio_de_la_rejilla_bajo_una_etiqueta_de_la_orden_no_se_escribe() -> None:
    """Punto 3: con una etiqueta de la orden sobre un precio de la rejilla del eje, ese precio no
    se escribe; los demas, si."""
    p = _panel_m1()
    rejilla = [p.lo + p.rango * k // 4 for k in range(5)]
    escritos = [x for x in laminas_svg._velas(p, HUSO, ESCALA) if 'class="precio"' in x]
    assert len(escritos) == 5
    tapados = laminas_svg._velas(p, HUSO, ESCALA, [p.y(rejilla[2])])
    precios = [x for x in tapados if 'class="precio"' in x]
    assert len(precios) == 4 and f">{laminas.precio(rejilla[2], ESCALA)}<" not in "".join(precios)
    # y en una lamina de tipo a, ningun precio de la rejilla del M1 bajo una etiqueta
    orden = laminas.OrdenFoto(
        "o1", "compra", 110_010, 109_986, 110_100, CORTE * 60_000 - 1, "colocada", "07-11",
        "zona:1",
    )  # fmt: skip
    texto, _ = _pagina(
        foto_base(ordenes=(orden,), colocadas=frozenset({"o1"})), laminas.TIPO_A, "o1"
    )
    import re as _re

    m1_desde = 2 * laminas_svg.ALTO_PANEL
    etiquetas = [
        float(y) for y in _re.findall(r'<rect class="eje-[a-z]+" x="[\d.]+" y="([\d.]+)"', texto)
    ]
    rejilla_m1 = [
        float(y) - 4
        for y in _re.findall(r'<text class="precio" x="[\d.]+" y="([\d.]+)"', texto)
        if float(y) > m1_desde
    ]
    alto = laminas_svg.ALTO_ETIQUETA
    assert etiquetas and all(abs(y - (e + alto / 2)) >= alto for y in rejilla_m1 for e in etiquetas)


# ------------------------------------------- la respuesta tras revisar la v3 (puntos 1 a 3)


def _dibujo(
    f: laminas.Foto, tipo: str = laminas.TIPO_B, orden: str | None = None
) -> laminas.Dibujo:
    return laminas.componer(_lamina(f, tipo, orden), LECTURA).dibujo


def test_el_tramo_del_m1_de_cerca() -> None:
    """Punto 1: desde la M1 de la toma hasta el corte; desde 15 velas antes de la primera zona de
    control si es anterior; como mucho 60 velas; sin toma, las 30 ultimas."""
    d = _dibujo(foto_base())
    tramo = laminas_svg.tramo_de_cerca(d)
    assert int(tramo[0].inicio) == TOMA - 1 and int(tramo[-1].inicio) == CORTE - 1
    anot = dict(foto_base().anotaciones)
    anot["zonas_de_control"] = f"{CORTE}|110000@{CORTE - 40}"
    con_control = _dibujo(foto_base(anotaciones=tuple(sorted(anot.items()))))
    assert int(laminas_svg.tramo_de_cerca(con_control)[0].inicio) == CORTE - 40 - 15
    anot["zonas_de_control"] = f"{CORTE}|110000@{CORTE - 100}"
    lejos = _dibujo(foto_base(anotaciones=tuple(sorted(anot.items()))))
    tramo = laminas_svg.tramo_de_cerca(lejos)
    assert len(tramo) == laminas_svg.VELAS_CERCA_MAX and int(tramo[-1].inicio) == CORTE - 1
    sin_toma = _dibujo(foto_base(escenarios=()))
    assert len(laminas_svg.tramo_de_cerca(sin_toma)) == laminas_svg.VELAS_CERCA_SIN_TOMA


def test_la_escala_del_m1_de_cerca_y_lo_que_queda_fuera() -> None:
    """Punto 1: la escala son las velas del tramo, la caja, la orden y el stop; el objetivo, lejos,
    va como marca de borde con su precio; nada a la derecha del corte."""
    import re as _re

    orden = laminas.OrdenFoto(
        "o1", "compra", 110_010, 109_986, 110_400, CORTE * 60_000 - 1, "colocada", "07-11", "zona:1"
    )
    f = foto_base(ordenes=(orden,), colocadas=frozenset({"o1"}))
    texto, _ = _pagina(f, laminas.TIPO_A, "o1")
    d = _dibujo(f, laminas.TIPO_A, "o1")
    tramo = laminas_svg.tramo_de_cerca(d)
    precios = [int(v.maxima) for v in tramo] + [int(v.minima) for v in tramo]
    precios += [110_010, 109_980, 109_986]
    assert f">▲ {laminas.precio(110_400, ESCALA)}<" in texto
    assert en_panel(texto, "objetivo-fuera", 3) == 1 and en_panel(texto, "objetivo", 2) == 1
    assert en_panel(texto, "orden", 3) == 1 and en_panel(texto, "stop", 3) == 1
    cerca = 3 * laminas_svg.ALTO_PANEL
    ys = [float(y) for y in _re.findall(r'<text class="precio" x="[\d.]+" y="([\d.]+)"', texto)]
    assert any(y > cerca for y in ys)
    # la escala: el mas alto y el mas bajo del tramo, la caja, la orden y el stop
    rejilla = [
        x
        for y, x in _re.findall(r'<text class="precio" x="[\d.]+" y="([\d.]+)"[^>]*>([^<]*)', texto)
        if float(y) > cerca
    ]
    # cada precio que se escribe es uno de los cinco de la rejilla de esa escala (los que caen bajo
    # una etiqueta no se escriben, punto 3 de la ronda anterior)
    hi, lo = max(precios), min(precios)
    esperados = {laminas.precio(lo + (hi - lo) * k // 4, ESCALA) for k in range(5)}
    assert rejilla and set(rejilla) <= esperados
    derecha = laminas_svg.ANCHO - laminas_svg.MARGEN_DER
    for etiqueta in _re.findall(r"<(?:line|rect|circle|text)\b[^>]*>", texto):
        if 'class="precio"' in etiqueta or 'class="eje-' in etiqueta or 'width="1600"' in etiqueta:
            continue
        xs = [float(x) for x in _re.findall(r'\s(?:x|x1|x2|cx)="([\d.]+)"', etiqueta)]
        ancho = _re.search(r'\swidth="([\d.]+)"', etiqueta)
        if ancho and etiqueta.startswith("<rect"):
            xs.append(xs[0] + float(ancho.group(1)))
        assert all(x <= derecha + 0.05 for x in xs), etiqueta


def test_toda_hora_que_nombra_una_vela_es_la_de_su_apertura() -> None:
    """Punto 2: la toma, el punto y la toma con la linea de antes nombran la vela por su apertura,
    como FX Replay; la cabecera nombra el corte y la vela, cada uno el suyo."""
    texto, comp = _pagina(foto_base())
    assert (
        f"La vela de M1 de las 09:29 cerró con cuerpo por debajo del bajo de M15 en {PRECIO_BAJO}."
        in comp.frases
    )
    assert "El punto de breaker está en 1.10010, de la vela de las 09:40." in comp.frases
    assert "Corte: a las 10:00, al cierre de la vela de M1 de las 09:59." in texto
    _, fuera = _pagina(foto_base(desde_m15=CORTE - 150))
    assert any(
        x.startswith("La vela de M1 de las 09:29 tomó la liquidez de M15") for x in fuera.frases
    )
    assert not [x for x in comp.frases + fuera.frases if ", a las " in x]


def test_la_linea_tomada_lleva_su_precio_en_el_m1_de_cerca_y_las_marcas_no_se_montan() -> None:
    """Lo enseno la captura de la v4: en el M1 de cerca, la linea tomada lleva su precio en el eje
    (en el M1, no: alli se montaria con el de la orden); y dos marcas de borde en el mismo sitio se
    apilan."""
    import re as _re

    texto, _ = _pagina(foto_base())
    assert en_panel(texto, "eje-linea-tomada", 3) == 2  # su rect y su texto, en el M1 de cerca
    assert en_panel(texto, "eje-linea-tomada", 2) == 0  # en el M1, no
    assert _re.search(rf'<text class="eje-linea-tomada"[^>]*>{PRECIO_BAJO}</text>', texto)
    panel = _panel_m1()
    lejos = [
        laminas.LineaDibujada("alto", panel.hi + 500, CORTE - 200, CORTE, False, False),
        laminas.LineaDibujada("alto", panel.hi + 900, CORTE - 200, CORTE, False, False),
    ]
    marcas = laminas_svg._fuera(panel, lejos, ESCALA)
    ys = [float(_re.search(r' y="([\d.]+)"', m).group(1)) for m in marcas]  # type: ignore[union-attr]
    assert len(set(ys)) == 2


def test_las_etiquetas_del_eje_no_se_montan_y_cada_una_lleva_su_precio() -> None:
    """Lo enseno la captura de la segunda v4: dos etiquetas del eje una encima de otra. Tres en el
    mismo nivel quedan a ALTO_ETIQUETA, cada una con su precio; y la que se saldria por abajo se
    sube desde el borde."""
    import re as _re

    p = _panel_m1()
    alto = laminas_svg.ALTO_ETIQUETA
    pedidas = [
        ("orden", p.lo + 50, "#000"), ("linea-tomada", p.lo + 50, "#111"),
        ("stop", p.lo + 49, "#222"),
    ]  # fmt: skip
    partes, ys = laminas_svg._etiquetas(p, pedidas, ESCALA)
    assert sorted(ys) == ys and all(b - a >= alto for a, b in zip(ys, ys[1:], strict=False))
    assert ys[-1] <= p.y0 + laminas_svg.ALTO_PANEL - alto / 2
    texto = "".join(partes)
    for clase, nivel, _ in pedidas:
        assert _re.search(
            rf'<text class="eje-{clase}"[^>]*>{laminas.precio(nivel, ESCALA)}<', texto
        )
    # una sola, en su sitio
    _, solo = laminas_svg._etiquetas(p, [("orden", p.lo + 50, "#000")], ESCALA)
    assert solo == [p.y(p.lo + 50)]


def test_en_el_m1_de_cerca_no_entra_la_linea_que_acabo_antes_del_tramo() -> None:
    """Lo enseno la captura de la segunda v4: una linea tomada que acabo antes del tramo del M1 de
    cerca no se ve alli, y ni su precio en el eje ni su marca de borde se dibujan; en el M1, si."""
    d = _dibujo(foto_base())
    tramo = laminas_svg.tramo_de_cerca(d)
    nivel = int(min(v.minima for v in tramo)) + 1
    antes = laminas.LineaDibujada(
        "bajo", nivel, int(tramo[0].inicio) - 50, int(tramo[0].inicio) - 5, True, False
    )
    texto = laminas_svg.svg(dataclasses.replace(d, lineas=(*d.lineas, antes)))
    base = laminas_svg.svg(d)
    assert en_panel(texto, "linea-m15 bajo tomada", 3) == en_panel(base, "linea-m15 bajo tomada", 3)
    assert en_panel(texto, "eje-linea-tomada", 3) == en_panel(base, "eje-linea-tomada", 3)
    assert en_panel(texto, "m15-fuera", 3) == en_panel(base, "m15-fuera", 3)
    assert (
        en_panel(texto, "linea-m15 bajo tomada", 2)
        == en_panel(base, "linea-m15 bajo tomada", 2) + 1
    )
