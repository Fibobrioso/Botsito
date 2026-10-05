"""Los tramos no citables de las sesiones con el trader y el criterio de sus limites
(`docs/runbooks/SESION-DE-PREGUNTAS.md`, «Los limites de un tramo: el criterio unico";
`docs/validation/FILTRADAS-ESCENARIO-B.md`).

- Un tramo que termina justo donde empieza la ventana declarada de un item no la pisa, y uno que se
  mete 1 ms en ella si: es la regla de `tramo_no_citable`, la que aplica `knowledge validate`.
- En el repo real, cada tramo de cuarentena de la sesion 03 (v9), registrado sin margen, tiene un
  companero con el segundo de margen, salvo que ese segundo pise la ventana de un item; el bloque de
  v10 de 1:55:27 del escenario B tiene su tramo; y ningun item de v7-v10 solapa un tramo.
"""

from __future__ import annotations

from pathlib import Path

from botsito.corpus.cuarentena import cargar_tramos_no_citables
from botsito.evidence.modelo import cargar_evidencia
from botsito.evidence.verificacion import ContextoEvidencia, tramo_no_citable

RAIZ = Path(__file__).resolve().parents[2]
SEGUNDO = 1000
CUARENTENA_SESION_03 = "cuarentena mecanica de la sesion 03"
TRAMO_V10_1_55_27 = (6_927_000, 6_934_000)  # bloque [CUARENTENA 115:27–115:33] de B, mas 1 s

Tramos = dict[str, tuple[tuple[int, int, str], ...]]
Ventanas = list[tuple[int, int]]


def sin_margen_sin_companero(tramos: Tramos, ventanas_v9: Ventanas) -> list[tuple[int, int]]:
    """Los tramos de cuarentena de v9 cuyo segundo de margen no cubre ningun tramo, cuando ese
    segundo no pisa la ventana declarada de ningun item (si la pisa, el tramo termina en el inicio
    de la ventana: el criterio del runbook)."""
    v9 = tramos.get("v9", ())
    salida = []
    for t0, t1, motivo in v9:
        if not motivo.startswith(CUARENTENA_SESION_03):
            continue
        cubierto = any(x <= t0 and t1 + SEGUNDO <= y for x, y, _ in v9)
        pisa_item = any(a < t1 + SEGUNDO and t1 < b for a, b in ventanas_v9)
        if not cubierto and not pisa_item:
            salida.append((t0, t1))
    return salida


def _contexto(t0: int, t1: int) -> ContextoEvidencia:
    return ContextoEvidencia(tramos_no_citables={"vx": ((t0, t1, "sintetico"),)})


def test_un_tramo_que_termina_en_el_inicio_de_la_ventana_no_la_pisa() -> None:
    assert tramo_no_citable(_contexto(10_000, 20_000), "vx", 20_000, 24_000) is None


def test_un_tramo_que_se_mete_1_ms_en_la_ventana_la_pisa() -> None:
    motivo = tramo_no_citable(_contexto(10_000, 20_001), "vx", 20_000, 24_000)
    assert motivo is not None and "sintetico" in motivo


def test_el_criterio_de_los_limites_sintetico() -> None:
    sin_companero: Tramos = {"v9": ((10_000, 20_000, CUARENTENA_SESION_03 + ": x"),)}
    assert sin_margen_sin_companero(sin_companero, []) == [(10_000, 20_000)]
    con_companero: Tramos = {
        "v9": (
            (10_000, 20_000, CUARENTENA_SESION_03 + ": x"),
            (10_000, 21_000, "completa el tramo"),
        )
    }
    assert sin_margen_sin_companero(con_companero, []) == []
    # El segundo de margen pisaria la ventana de un item: el tramo se queda en su inicio.
    assert sin_margen_sin_companero(sin_companero, [(20_000, 24_000)]) == []
    assert sin_margen_sin_companero(sin_companero, [(21_000, 24_000)]) == [(10_000, 20_000)]


def _ventanas(video: str) -> Ventanas:
    return [
        (it.t0_ms, it.t1_ms)
        for it in cargar_evidencia(RAIZ / "knowledge" / "evidence")
        if it.video_id == video
    ]


def test_los_tramos_de_sesion_del_repo_real() -> None:
    tramos = cargar_tramos_no_citables(RAIZ)
    assert sin_margen_sin_companero(tramos, _ventanas("v9")) == []
    assert any(x <= TRAMO_V10_1_55_27[0] and TRAMO_V10_1_55_27[1] <= y for x, y, _ in tramos["v10"])


def test_la_rotura_a_proposito_cae() -> None:
    """Quitar un tramo nuevo de v9 del repo real: la comprobacion lo nombra."""
    tramos = cargar_tramos_no_citables(RAIZ)
    nuevo = next(t for t in tramos["v9"] if t[2].startswith("completa el tramo"))
    roto = {**tramos, "v9": tuple(t for t in tramos["v9"] if t != nuevo)}
    assert sin_margen_sin_companero(roto, _ventanas("v9")) == [(nuevo[0], nuevo[1] - SEGUNDO)]


def test_ningun_item_de_las_sesiones_solapa_un_tramo() -> None:
    """Solo los items ACTIVOS: uno supersedido no se cita (decision del consultor del 2026-10-05,
    VENTANA-EV-V9.md, punto 4). ev-v9-003456-9ef48fb5, supersedido, si pisa el tramo de margen."""
    tramos = cargar_tramos_no_citables(RAIZ)
    contexto = ContextoEvidencia(tramos_no_citables=tramos)
    items = cargar_evidencia(RAIZ / "knowledge" / "evidence")
    supersedidos = {it.supersede for it in items if it.supersede}
    pisan = [
        it.id
        for it in items
        if it.video_id in {"v7", "v8", "v9", "v10"}
        and it.id not in supersedidos
        and tramo_no_citable(contexto, it.video_id, it.t0_ms, it.t1_ms) is not None
    ]
    assert pisan == []
    # El negativo: el supersedido si lo pisa, y por eso hace falta contar solo los activos.
    viejo = next(it for it in items if it.id == "ev-v9-003456-9ef48fb5")
    assert viejo.id in supersedidos
    assert tramo_no_citable(contexto, "v9", viejo.t0_ms, viejo.t1_ms) is not None
