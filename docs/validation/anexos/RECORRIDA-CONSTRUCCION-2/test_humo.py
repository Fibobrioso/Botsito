"""Tests de humo de los guiones de esta carpeta, sobre salidas SINTETICAS y en los dos sentidos
(RECORRIDA-CONSTRUCCION-2, fase 1). No los recoge `make check` (`testpaths = ["tests"]`):

    uv run pytest docs/validation/anexos/RECORRIDA-CONSTRUCCION-2/test_humo.py -q

De `anexos/RECORRIDA-CONSTRUCCION/test_humo.py` vienen COPIADOS TAL CUAL sus constantes
`ROTULO`, `POR_SESION` y `TRADER`, `_clasifica` y dos de sus tests de `patrones.py`
(`test_la_copia_lee_el_sesgo_con_rotulo_y_sin_el` y
`test_la_copia_solo_corta_el_rotulo_de_diagnostico`).
No vienen: los de `entradas_antes_alternancia.py`, que esta rama no copia (encargo, D4), y
`test_la_lectura_vieja_rompe_sin_rotulo` con su `_cargar`, que prueba el guion de R3.1
(`anexos/CORRIDA-CONSTRUCCION/patrones.py`) y no el de esta carpeta, y que la guardia niega en un
fichero que no es el de `main` (carga un modulo por una ruta calculada). El original sigue
corriendo en su sitio, identico al de `main` (RECORRIDA-CONSTRUCCION-2.md, fase 1). Lo nuevo:
un test de `horas_perdidas.py`, que el original no probaba, y los de `para_clasificar.py`.
"""

from __future__ import annotations

import sys
from pathlib import Path
from types import ModuleType

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import antes_del_dia  # noqa: E402
import horas_perdidas  # noqa: E402
import para_clasificar as pc  # noqa: E402
import patrones  # noqa: E402

ROTULO = "[DIAGNOSTICO-CUENTA-diaria] "
POR_SESION = (
    "2026-04-01 07-11 | trader 1 | bot 0 | rn003 alcista | sesgo:si "
    "orden_dimensionada:no[productoras sin cumplirse] | disparadas RN-003 | bloqueadas ninguna"
)
TRADER = (
    "trader | 2026-04-01 | 07-11 | compra | 2026-04-01T08:00:00+00:00 | 1.10000 | SIN PAREJA; "
    "ninguna operacion del bot en la sesion; primer hecho que falto: liquidez_tomada[x]"
)


# ------------------------------------------------------------- patrones.py: con rotulo y sin el


def _clasifica(modulo: ModuleType, ruta: Path) -> tuple[int, list[str]]:
    filas, sesgo = modulo.leer(ruta)
    return len(sesgo), [p for p, *_ in modulo.clasificar(filas, sesgo)]


def test_la_copia_lee_el_sesgo_con_rotulo_y_sin_el(tmp_path: Path) -> None:
    con = tmp_path / "con.txt"
    sin = tmp_path / "sin.txt"
    con.write_text(f"{ROTULO}{POR_SESION}\n{ROTULO}{TRADER}\n", encoding="utf-8")
    sin.write_text(f"{POR_SESION}\n{TRADER}\n", encoding="utf-8")
    assert _clasifica(patrones, con) == (1, ["P4 sin orden"])
    assert _clasifica(patrones, sin) == (1, ["P4 sin orden"])


def test_la_copia_solo_corta_el_rotulo_de_diagnostico() -> None:
    assert patrones._cuerpo(ROTULO + POR_SESION) == POR_SESION
    assert patrones._cuerpo(POR_SESION) == POR_SESION
    assert patrones._cuerpo("[otra cosa] texto") == "[otra cosa] texto"


# ------------------------------------------------------- horas_perdidas.py, en los dos sentidos


def test_una_fila_en_una_hora_perdida_se_marca_y_otra_no(tmp_path: Path) -> None:
    """2026-04-03T09Z es una de las 18 horas; la misma fila una hora despues, no."""
    dentro = TRADER.replace("2026-04-01 | ", "2026-04-03 | ").replace(
        "2026-04-01T08:00:00", "2026-04-03T09:10:00"
    )
    fuera = dentro.replace("T09:10:00", "T10:10:00")
    for fila, marcada in ((dentro, True), (fuera, False)):
        ruta = tmp_path / "s.txt"
        ruta.write_text(f"{POR_SESION}\n{fila}\n", encoding="utf-8")
        filas, sesgo = patrones.leer(ruta)
        [(_, _, marca, _)] = patrones.clasificar(filas, sesgo)
        assert bool(marca) is marcada
    assert "2026-04-03T09Z" in horas_perdidas.HORAS_PERDIDAS


# ------------------------------------------------------- para_clasificar.py, en los dos sentidos
#
# Una salida sintetica minima con las secciones que el guion lee: una operacion del trader (compra
# a 1.10000 a las 08:00) y una orden del bot en su sesion. Los dias son de 2026-04 y 2026-07 solo
# para el `material_sin_video`; nada es de una salida real.

DIA = "2026-04-01"
ESCALONES_SALIDA = (
    "sin orden del bot en su (dia, sesion, direccion) | orden, con la entrada fuera de "
    "tolerancia | "
    "entrada, con el stop fuera de tolerancia | entrada; el caso no trae stop | en el nivel, no "
    "llenada | en el nivel, llenada fuera de tolerancia de instante | las cuatro piezas"
)


def _salida(
    *,
    precio: str = "1.10002",
    caja: str = "1.09980",
    llenada: bool = True,
    lado_posicion: str = "compra",
    cascada: str = "0 | 0 | 0 | 0 | 0 | 0 | 1 | 1",
    sin_trader: int = 0,
    stop_movido: bool = False,
    rotulo: str = "",
) -> str:
    resultado = "llenada" if llenada else "cancelada"
    orden = (
        f"{DIA} | 07-11 | o1 | {DIA}T07:59:59.999000+00:00 | {precio} | {resultado} | - | "
        f"{DIA}T08:02:00+00:00 | 1.00 | 20 | 1.00 | 1.00 | 0.500 | 1.00 | ninguno | x | {caja}"
    )
    posicion = (
        f"{DIA} | 07-11 | pos-o1 | o1 | {lado_posicion} | limite | {DIA}T08:02:00+00:00 | "
        f"{precio} | {DIA}T09:00:00+00:00 | 1.10062 | objetivo | objetivo | 1.00 | 60.00 | 5.00 | "
        "0.00 | 55.00 | 20.00 | 2.750"
    )
    eventos = [f"{DIA} | {DIA}T08:02:00+00:00 | llenada | o1 | ticks"]
    if stop_movido:
        eventos.append(f"{DIA} | {DIA}T08:30:00+00:00 | stop_movido | pos-o1 | ticks")
    lineas = [
        "## Por sesion",
        POR_SESION.replace("bot 0", "bot 1"),
        "## Diferencias por operacion (ADR-0043: 3 puntos, 15 min)",
        "quien | dia | sesion | lado | instante UTC | entrada | resultado",
        TRADER,
        "### Eventos del broker (dia | instante UTC | tipo | id | fuente)",
        *eventos,
        "",
        f"eventos: {len(eventos)}; por fuente: respaldo_m1 0, ticks {len(eventos)}",
        "### Ordenes (dia | sesion | id | ...)",
        orden,
        f"ordenes: {resultado} 1",
        "### Posiciones (dia | sesion | id | ...)",
        *([posicion] if llenada else ["ninguna"]),
        f"posiciones: {1 if llenada else 0}; PnL neto total (USD): 55.00",
        "### Fidelidad por criterios (ADR-0092 §1 y §2; diagnostico de construccion, sin umbral)",
        "tolerancias: entrada 3 puntos, stop 3 puntos, llenado 15 min",
        f"mes | {ESCALONES_SALIDA} | total",
        f"2026-04 | {cascada}",
        f"total | {cascada}",
        "ordenes del bot en un (dia, sesion, direccion) sin ninguna operacion del trader: "
        f"{sin_trader}",
        "libros sin video: 2026-01, 2026-04, 2026-08, salvo 2026-04-29; cuentan como CON video, "
        "provisionales hasta que T lo compruebe: 2026-07 (fuente: x)",
    ]
    return "\n".join(rotulo + ln for ln in lineas) + "\n"


def _correr(texto: str, tmp_path: Path) -> tuple[pc.Salida, dict, list[str]]:
    ruta = tmp_path / "s.txt"
    ruta.write_text(texto, encoding="utf-8")
    salida = pc.leer_salida(texto)
    filas, sesgo = patrones.leer(ruta)
    trader = pc.trader_de(patrones.clasificar(filas, sesgo))
    pasos = {k: pc.cascada_hasta_la_entrada(k, salida) for k in trader}
    return salida, pasos, pc.comprobar(pasos, salida, "s")


def test_entrada_a_dos_puntos_queda_dentro_y_coincide_con_la_salida(tmp_path: Path) -> None:
    _, pasos, problemas = _correr(_salida(), tmp_path)
    [paso] = pasos.values()
    assert paso.escalon == pc.ENTRADA_DENTRO
    assert paso.orden == "o1 llenada, llenada a 2.0 min del trader"
    assert problemas == []


def test_entrada_a_diez_puntos_queda_fuera_y_la_cascada_vieja_no_coincide(tmp_path: Path) -> None:
    _, pasos, problemas = _correr(_salida(precio="1.10010", caja="1.09990"), tmp_path)
    [paso] = pasos.values()
    assert paso.escalon == pc.ENTRADA_FUERA
    # la salida sigue diciendo «las cuatro piezas»: el guion lo cuenta y lo dice
    assert problemas == ["s: 2026-04 contado (0, 1, 0), la salida (0, 0, 1)",
                         "s: total contado (0, 1, 0), la salida (0, 0, 1)"]  # fmt: skip
    _, _, problemas = _correr(
        _salida(precio="1.10010", caja="1.09990", cascada="0 | 1 | 0 | 0 | 0 | 0 | 0 | 1"),
        tmp_path,
    )
    assert problemas == []


def test_la_direccion_de_una_no_llenada_sale_de_su_caja(tmp_path: Path) -> None:
    """Por debajo del precio, compra: la orden cuenta en la sesion del trader; por encima, venta:
    el trader se queda sin orden y la orden pasa a «sin trader»."""
    _, pasos, problemas = _correr(
        _salida(llenada=False, cascada="0 | 0 | 0 | 0 | 1 | 0 | 0 | 1"), tmp_path
    )
    assert [p.escalon for p in pasos.values()] == [pc.ENTRADA_DENTRO]
    assert problemas == []
    salida, pasos, problemas = _correr(
        _salida(llenada=False, caja="1.10030", cascada="1 | 0 | 0 | 0 | 0 | 0 | 0 | 1",
                sin_trader=1),
        tmp_path,
    )  # fmt: skip
    assert [p.escalon for p in pasos.values()] == [pc.SIN_ORDEN]
    assert problemas == []
    assert [o.direccion for o in salida.ordenes] == ["venta"]


def test_una_caja_que_contradice_a_su_posicion_se_dice(tmp_path: Path) -> None:
    salida, _, problemas = _correr(_salida(caja="1.10030"), tmp_path)
    assert salida.contradicciones == ["2026-04-01 o1: posicion compra, caja venta"]
    assert "s: 2026-04-01 o1: posicion compra, caja venta" in problemas
    assert [o.direccion for o in salida.ordenes] == ["compra"]  # manda la posicion


def test_las_ordenes_sin_trader_que_no_cuadran_se_dicen(tmp_path: Path) -> None:
    _, _, problemas = _correr(_salida(sin_trader=1), tmp_path)
    assert problemas == ["s: ordenes sin trader contadas 0, la salida 1"]


def test_lee_igual_con_rotulo_de_diagnostico(tmp_path: Path) -> None:
    _, pasos, problemas = _correr(_salida(rotulo=ROTULO), tmp_path)
    assert [p.escalon for p in pasos.values()] == [pc.ENTRADA_DENTRO]
    assert problemas == []


def test_el_video_de_cada_dia() -> None:
    sin_video = ({"2026-01", "2026-04", "2026-08"}, {"2026-04-29"}, {"2026-07"})
    assert pc.video_de("2026-04-01", sin_video) == "sin video"
    assert pc.video_de("2026-04-29", sin_video).startswith("con video")
    assert pc.video_de("2026-07-03", sin_video) == "con video, provisional"
    assert pc.video_de("2026-01-05", sin_video) == "sin video"


def test_la_orden_sin_trader_lleva_r_desenlace_y_stop_movido(tmp_path: Path) -> None:
    for movido, esperado in ((True, "si"), (False, "no")):
        salida = pc.leer_salida(_salida(caja="1.09980", stop_movido=movido, sin_trader=1))
        # sin trader en esa clave: la orden entera sale en la lista
        [fila] = pc.bot_sin_trader(salida, set(), [])
        campos = fila.split(" | ")
        assert campos[2:9] == [
            "compra", "o1", "llenada", "2.750", "objetivo", esperado,
            "sin fila del bot sin pareja (emparejada)",
        ]  # fmt: skip
    # con la clave del trader, no sale
    salida = pc.leer_salida(_salida())
    assert pc.bot_sin_trader(salida, {(DIA, "07-11", "compra")}, []) == []


def test_el_resumen_de_la_lista_suma_solo_las_llenadas() -> None:
    lista = [
        "2026-04-01 | 07-11 | compra | o1 | llenada | 2.750 | objetivo | si | P6 donde [en dia]",
        "2026-04-01 | 07-11 | compra | o2 | cancelada | - | - | - | - (no llenada)",
        "2026-07-01 | 07-11 | venta | o1 | llenada | -1.000 | salto_el_stop | no | P5 de mas",
    ]
    abril, julio, total = pc.resumen_sin_trader(lista)
    assert abril.startswith(
        "2026-04 | ordenes 2 | llenadas 1 | suma del R neto 2.750 | stop movido 1"
    )
    assert "patrones P6 donde 1" in abril
    assert julio.startswith(
        "2026-07 | ordenes 1 | llenadas 1 | suma del R neto -1.000 | stop movido 0"
    )
    assert total.startswith(
        "total | ordenes 3 | llenadas 2 | suma del R neto 1.750 | stop movido 1"
    )


# ------------------------------------------------------------ antes_del_dia.py, en los dos sentidos


def test_antes_del_dia_caza_una_fecha_y_un_minuto_anteriores_y_deja_los_del_dia(
    tmp_path: Path,
) -> None:
    # minutos UTC desde 1970: 29583840 = 2026-04-01 08:00. Las filas «malas» son del 2026-04-02 con
    # algo del 2026-04-01 (dos dias dev), y la fecha fuera de la construccion, de 2030 (sintetica):
    # ninguna fecha de un mes con dias reservados (revisor, b1)
    buena = tmp_path / "buena.txt"
    buena.write_text(
        "2026-04-01 | 07-11 | o1 | 2026-04-01T08:00:59.999000+00:00 | 110000@29583840\n",
        encoding="utf-8",
    )
    assert antes_del_dia.main([buena]) == 0
    for mala in (
        "2026-04-02 | 07-11 | o1 | 2026-04-01T23:00:00+00:00 | x\n",
        "2026-04-02 | 07-11 | o1 | x | 110000@29583840\n",
        "nota suelta con una fecha sintetica, 2030-02-14\n",
        f"{ROTULO}2026-04-02 | 07-11 | o1 | 2026-04-01T23:00:00+00:00 | x\n",
        "P4 sin orden: trader | 2026-04-02 | 07-11 | compra | 2026-04-01T23:00:00+00:00 | 1\n",
    ):
        ruta = tmp_path / "mala.txt"
        ruta.write_text(mala, encoding="utf-8")
        assert antes_del_dia.main([ruta]) == 1, mala
