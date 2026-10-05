"""La condicion de la ventana de un item (decision del consultor del 2026-10-05,
docs/validation/VENTANA-EV-V9.md): la ventana declarada de todo item ACTIVO no se solapa mas de 0 ms
con un tramo no citable de su video, ni con un segmento de su transcripcion que a su vez solape un
tramo. Todo sintetico salvo el ultimo test, que solo mira el cableado."""

from __future__ import annotations

import ast
import inspect
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.evidence.modelo import EvidenceItem
from botsito.evidence.verificacion import ContextoEvidencia, tramo_no_citable, ventana_no_citable
from botsito.validation.knowledge import ventanas_no_citables

RAIZ = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class _Seg:
    n: int
    t0_ms: int
    t1_ms: int
    texto: str = "sintetico"
    senales: tuple[str, ...] = ()
    palabras: tuple[Any, ...] = ()


def _contexto(tramos: list[tuple[int, int]], segmentos: list[_Seg] | None = None) -> Any:
    """Un contexto con los tramos del video `vx` y, si se dan, los segmentos de su cruda `tr-x`."""
    crudas = (lambda tid: segmentos) if segmentos is not None else (lambda tid: None)
    return ContextoEvidencia(
        tramos_no_citables={"vx": tuple((a, b, "sintetico") for a, b in tramos)}, crudas=crudas
    )


def _hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}.{ms % 1000:03d}"


def _item(iid: str, t0_ms: int, t1_ms: int, supersede: str | None = None) -> EvidenceItem:
    return EvidenceItem(
        id=iid, video_id="vx", t0=_hms(t0_ms), t1=_hms(t1_ms), modalidad="audio",
        tipo="RULE_STATEMENT", cita_literal="cita sintetica de prueba aqui", afirmacion="a",
        tema="t.x", confianza="media", extractor="humano", revisado_por="r", provenance="botsito",
        supersede=supersede, transcripcion="tr-x",
    )  # fmt: skip


# --------------------------------------------------------------- las roturas que pidio el consultor


def test_la_ventana_vieja_falla() -> None:
    """v9: la ventana vieja (desde 2.096.000) pisa el tramo de margen 0:34:44-0:34:57."""
    ctx = _contexto([(2_084_000, 2_096_000), (2_084_000, 2_097_000)])
    motivo = ventana_no_citable(ctx, "vx", 2_096_000, 2_100_000, None)
    assert motivo is not None and motivo.startswith("el tramo no es especificacion")


def test_pisar_solo_la_cola_de_un_segmento_que_solapa_un_tramo_falla() -> None:
    """El caso de v9 antes del tramo de margen: el tramo acaba en 20.000, su ultimo segmento en
    20.900, y la ventana empieza en 20.000. No toca el tramo, pero si el segmento."""
    segs = [_Seg(612, 15_000, 20_900), _Seg(613, 22_000, 24_000)]
    ctx = _contexto([(10_000, 20_000)], segs)
    assert tramo_no_citable(ctx, "vx", 20_000, 24_000) is None
    motivo = ventana_no_citable(ctx, "vx", 20_000, 24_000, segs)
    assert motivo is not None and "900 ms del segmento 612" in motivo
    # Sin los segmentos (sin la cruda) no se puede ver: por eso quien llama lo tiene que decir.
    assert ventana_no_citable(ctx, "vx", 20_000, 24_000, None) is None


def test_la_ventana_que_toca_el_tramo_a_0_ms_pasa() -> None:
    segs = [_Seg(1, 15_000, 20_000), _Seg(2, 21_000, 24_000)]
    ctx = _contexto([(10_000, 20_000)], segs)
    assert ventana_no_citable(ctx, "vx", 20_000, 24_000, segs) is None
    # El negativo: 1 ms dentro del tramo, falla.
    assert ventana_no_citable(ctx, "vx", 19_999, 24_000, segs) is not None


def test_un_item_supersedido_que_pisa_un_tramo_no_cuenta() -> None:
    segs = [_Seg(1, 15_000, 20_900), _Seg(2, 22_000, 24_000)]
    ctx = _contexto([(10_000, 21_000)], segs)
    viejo = _item("ev-vx-000020-viejo000", 20_000, 24_000)
    nuevo = _item("ev-vx-000021-nuevo000", 21_000, 24_000, supersede=viejo.id)
    problemas, avisos = ventanas_no_citables([viejo, nuevo], ctx)
    assert problemas == [] and avisos == []
    # El negativo: sin el que lo supersede, el viejo cuenta y falla.
    problemas, _ = ventanas_no_citables([viejo], ctx)
    assert len(problemas) == 1 and problemas[0].startswith(viejo.id)


def test_la_ventana_nueva_pasa() -> None:
    """v9 con los milisegundos medidos: 612 acaba en 2.096.900 y 613 empieza en 2.098.060."""
    segs = [_Seg(612, 2_096_380, 2_096_900), _Seg(613, 2_098_060, 2_100_240)]
    ctx = _contexto([(2_084_000, 2_096_000), (2_084_000, 2_097_000)], segs)
    assert ventana_no_citable(ctx, "vx", 2_097_000, 2_100_000, segs) is None
    assert ventana_no_citable(ctx, "vx", 2_096_000, 2_100_000, segs) is not None


def test_el_caso_de_v10_la_ventana_no_toca_el_tramo_pero_si_el_segmento_que_lo_toca() -> None:
    """ev-v10-010438-0d4e6798: la ventana (hasta 3.895.500) no toca el tramo (desde 3.896.000),
    pero pisa 503 ms del segmento 1058, que el tramo solapa por su inicio redondeado al segundo."""
    segs = [
        _Seg(1057, 3_893_497, 3_894_997),
        _Seg(1058, 3_894_997, 3_896_537),
        _Seg(1059, 3_896_537, 3_905_357),
    ]
    ctx = _contexto([(3_896_000, 3_929_000)], segs)
    assert tramo_no_citable(ctx, "vx", 3_878_000, 3_895_500) is None
    motivo = ventana_no_citable(ctx, "vx", 3_878_000, 3_895_500, segs)
    assert motivo is not None and "503 ms del segmento 1058" in motivo
    # La ventana recortada (hasta 3.894.000) pasa.
    assert ventana_no_citable(ctx, "vx", 3_878_000, 3_894_000, segs) is None


# ------------------------------------------------------------------------- sin la cruda, lo dice


def test_sin_la_cruda_no_pasa_en_silencio() -> None:
    """Como `verificar_citas`: no es un error, es un AVISO agregado por transcripcion. El tramo si
    se comprueba."""
    ctx = _contexto([(10_000, 20_000)], None)
    bien = _item("ev-vx-000030-bien0000", 30_000, 34_000)
    problemas, avisos = ventanas_no_citables([bien], ctx)
    assert problemas == []
    assert len(avisos) == 1 and "tr-x" in avisos[0] and "cruda ausente" in avisos[0]
    mal = _item("ev-vx-000015-mal00000", 15_000, 18_000)
    problemas, _ = ventanas_no_citables([mal], ctx)
    assert len(problemas) == 1  # el tramo, sin la cruda, se ve igual
    # Un video sin tramos no tiene nada que comprobar: ni problema ni aviso.
    sin_tramos = ContextoEvidencia(tramos_no_citables={}, crudas=lambda tid: None)
    assert ventanas_no_citables([bien], sin_tramos) == ([], [])


# ------------------------------------------------------------------------------------- el cableado


def _llamadas(funcion: Any, nombre: str) -> int:
    arbol = ast.parse(textwrap.dedent(inspect.getsource(funcion)))
    return sum(
        1
        for n in ast.walk(arbol)
        if isinstance(n, ast.Call)
        and (getattr(n.func, "id", None) == nombre or getattr(n.func, "attr", None) == nombre)
    )


def test_la_llaman_validate_evidence_new_y_propose() -> None:
    """La condicion la aplican los tres caminos (decision del consultor, punto 5)."""
    from botsito import cli
    from botsito.evidence import propuestas
    from botsito.validation import knowledge

    assert _llamadas(knowledge._validar, "ventanas_no_citables") == 1
    assert _llamadas(cli._EntornoEvidencia.comprobar, "ventana_no_citable") == 1
    assert _llamadas(propuestas.comprobar, "ventana_no_citable") == 1
