"""Cambios de hora con M1 sintetico 24/7 (donde si aparecen velas de 3, 5 y 1 h), desplazamiento
semanal con datos reales, asociatividad M1->M15->H4 == M1->H4 y vela de borde incompleta."""

from datetime import date
from pathlib import Path

import pytest

from botsito.data.agregacion import agregar
from botsito.data.dukascopy import descargar_dia
from botsito.data.velas import formato_ts, parse_ts
from botsito.domain.valores import HoraLocal, Puntos
from botsito.domain.velas import MinutoUtc, Vela

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "ohlc"
MADRID = HoraLocal("00:00", "Europe/Madrid")
SERVIDOR = HoraLocal("17:00", "America/New_York")
H4 = 240


def continuo(desde: str, hasta: str) -> list[Vela]:
    """M1 sin huecos en [desde, hasta) UTC; el precio es el minuto (sirve para verificar)."""
    a, b = parse_ts(desde), parse_ts(hasta)
    return [Vela(MinutoUtc(m), Puntos(m), Puntos(m), Puntos(m), Puntos(m), 1) for m in range(a, b)]


def dia_real(dia: str) -> list[Vela]:
    d = date.fromisoformat(dia)
    return list(
        descargar_dia("F", d, lambda _u: (FIXTURES / f"EURUSD_{dia}.bi5").read_bytes()).velas
    )


def resumen(velas: list[Vela]) -> list[tuple[str, int]]:
    return [(formato_ts(v.inicio), v.duracion_min) for v in velas]


def test_primavera_ee_uu_vela_de_3h_con_anclaje_servidor() -> None:
    # 2026-03-08 07:00Z: 01:00 EST -> 03:00 EDT. Limites 17:00 NY (22:00Z EST) + 4k: 02:00Z, 06:00Z
    # (01:00 EST), luego 05:00 EDT = 09:00Z. La vela [06:00, 09:00) dura 3 h.
    salida = agregar(continuo("2026-03-07T22:00Z", "2026-03-09T01:00Z"), H4, SERVIDOR)
    assert resumen(salida) == [
        ("2026-03-07T22:00Z", 240),
        ("2026-03-08T02:00Z", 240),
        ("2026-03-08T06:00Z", 180),
        ("2026-03-08T09:00Z", 240),
        ("2026-03-08T13:00Z", 240),
        ("2026-03-08T17:00Z", 240),
        ("2026-03-08T21:00Z", 240),
    ]
    assert all(v.completa for v in salida) and sum(v.n_m1 for v in salida) == 27 * 60
    # Madrid no cambia ese dia: todas de 4 h.
    assert {
        v.duracion_min
        for v in agregar(continuo("2026-03-07T23:00Z", "2026-03-08T23:00Z"), H4, MADRID)
    } == {240}


def test_primavera_ue_vela_de_3h_con_anclaje_madrid() -> None:
    # 2026-03-29 01:00Z: 02:00 CET -> 03:00 CEST. Limites 00:00 Madrid: 23:00Z (CET), luego
    # 04:00 CEST = 02:00Z. La vela [23:00, 02:00) dura 3 h.
    salida = agregar(continuo("2026-03-28T23:00Z", "2026-03-29T22:00Z"), H4, MADRID)
    assert resumen(salida)[:3] == [
        ("2026-03-28T23:00Z", 180),
        ("2026-03-29T02:00Z", 240),
        ("2026-03-29T06:00Z", 240),
    ]
    assert {
        v.duracion_min
        for v in agregar(continuo("2026-03-28T21:00Z", "2026-03-29T21:00Z"), H4, SERVIDOR)
    } == {240}


def test_otono_ue_vela_de_5h_y_m15_sin_vela_de_75_min() -> None:
    # 2025-10-26 01:00Z: 03:00 CEST -> 02:00 CET. Limites 00:00 Madrid: 22:00Z (CEST), luego
    # 04:00 CET = 03:00Z. La vela [22:00, 03:00) dura 5 h.
    salida = agregar(continuo("2025-10-25T22:00Z", "2025-10-26T23:00Z"), H4, MADRID)
    assert resumen(salida)[:2] == [("2025-10-25T22:00Z", 300), ("2025-10-26T03:00Z", 240)]
    m15 = agregar(continuo("2025-10-25T22:00Z", "2025-10-26T23:00Z"), 15, MADRID)
    assert {v.duracion_min for v in m15} == {15} and len(m15) == 100


def test_otono_ee_uu_vela_de_1h_mas_4h_con_anclaje_servidor() -> None:
    # 2025-11-02 06:00Z: 02:00 EDT -> 01:00 EST. 01:00 de pared existe dos veces: 05:00Z (EDT) y
    # 06:00Z (EST). Ambos son limites: [05:00, 06:00) de 1 h y [06:00, 10:00) de 4 h.
    salida = agregar(continuo("2025-11-01T21:00Z", "2025-11-02T22:00Z"), H4, SERVIDOR)
    assert resumen(salida)[:4] == [
        ("2025-11-01T21:00Z", 240),
        ("2025-11-02T01:00Z", 240),
        ("2025-11-02T05:00Z", 60),
        ("2025-11-02T06:00Z", 240),
    ]
    assert sum(v.n_m1 for v in salida) == 25 * 60


@pytest.mark.parametrize(
    ("domingo_antes", "domingo_despues", "anclaje", "esperado"),
    [
        # EE. UU. cambia el 8 de marzo: la apertura del servidor pasa de 22:00Z a 21:00Z.
        ("2026-03-01", "2026-03-08", SERVIDOR, ("2026-03-01T22:00Z", "2026-03-08T21:00Z")),
        # ...y Madrid no se entera: misma hora de pared, mismo limite UTC (19:00Z, CET).
        ("2026-03-01", "2026-03-08", MADRID, ("2026-03-01T19:00Z", "2026-03-08T19:00Z")),
        # La UE cambia el 29 de marzo: el limite de Madrid pasa de 19:00Z a 18:00Z...
        ("2026-03-22", "2026-03-29", MADRID, ("2026-03-22T19:00Z", "2026-03-29T18:00Z")),
        # ...y el servidor sigue en 21:00Z (EDT desde el 8).
        ("2026-03-22", "2026-03-29", SERVIDOR, ("2026-03-22T21:00Z", "2026-03-29T21:00Z")),
        # Otono UE (26 oct): Madrid 18:00Z -> 19:00Z; servidor 21:00Z ambos.
        ("2025-10-19", "2025-10-26", MADRID, ("2025-10-19T18:00Z", "2025-10-26T19:00Z")),
        ("2025-10-19", "2025-10-26", SERVIDOR, ("2025-10-19T21:00Z", "2025-10-26T21:00Z")),
        # Otono EE. UU. (2 nov): servidor 21:00Z -> 22:00Z; Madrid 19:00Z ambos.
        ("2025-10-26", "2025-11-02", SERVIDOR, ("2025-10-26T21:00Z", "2025-11-02T22:00Z")),
        ("2025-10-26", "2025-11-02", MADRID, ("2025-10-26T19:00Z", "2025-11-02T19:00Z")),
    ],
)
def test_desplazamiento_semanal_real(
    domingo_antes: str, domingo_despues: str, anclaje: HoraLocal, esperado: tuple[str, str]
) -> None:
    """Con datos reales la vela larga no existe (el mercado esta cerrado): lo observable es que
    la primera H4 con datos del domingo se mueve una hora en UTC solo para el anclaje cuyo huso
    cambio."""
    antes = agregar(dia_real(domingo_antes), H4, anclaje)
    despues = agregar(dia_real(domingo_despues), H4, anclaje)
    assert (formato_ts(antes[0].inicio), formato_ts(despues[0].inicio)) == esperado


def test_asociatividad_m1_m15_h4_en_dia_real() -> None:
    velas = dia_real("2026-07-02")
    directo = agregar(velas, H4, MADRID)
    via_m15 = agregar(agregar(velas, 15, MADRID), H4, MADRID)
    assert via_m15 == directo
    # Tambien con el anclaje de servidor y a traves de H1.
    assert agregar(agregar(velas, 60, SERVIDOR), H4, SERVIDOR) == agregar(velas, H4, SERVIDOR)


def test_inicio_de_dataset_deja_una_vela_de_borde_incompleta() -> None:
    # Dataset que empieza el 2026-01-01 00:00Z con anclaje de servidor (EST): el limite anterior
    # es 2025-12-31 22:00Z; la primera vela es esa, con 120 M1, y su cierre (02:00Z) ya paso.
    salida = agregar(continuo("2026-01-01T00:00Z", "2026-01-01T03:00Z"), H4, SERVIDOR)
    assert resumen(salida) == [("2025-12-31T22:00Z", 240), ("2026-01-01T02:00Z", 240)]
    assert salida[0].n_m1 == 120 and salida[0].completa is True
    assert salida[1].n_m1 == 60 and salida[1].completa is False
    # Si la serie termina exactamente en un limite, la ultima vela esta cerrada.
    cerrada = agregar(continuo("2026-01-01T00:00Z", "2026-01-01T02:00Z"), H4, SERVIDOR)
    assert cerrada[-1].completa is True


def test_duraciones_admisibles_en_un_semestre_con_los_cuatro_cambios() -> None:
    """Sobre 24/7 sintetico, octubre 2025 a abril 2026 (los cuatro cambios): solo 240, 180, 300
    y 60 minutos, limites estrictamente crecientes y cada M1 en exactamente una vela."""
    velas = continuo("2025-10-01T00:00Z", "2026-04-10T00:00Z")
    for anclaje in (MADRID, SERVIDOR):
        salida = agregar(velas, H4, anclaje)
        assert {v.duracion_min for v in salida} <= {240, 180, 300, 60}
        assert sum(v.n_m1 for v in salida) == len(velas)
        assert all(a.fin == b.inicio for a, b in zip(salida, salida[1:], strict=False))


def test_huso_con_salto_de_30_min_y_periodo_diario() -> None:
    """Las invariantes generales (cada M1 una vez, limites contiguos) valen para husos exoticos;
    las duraciones son P-d, P, P+d o d con d el salto del huso, y 2P-d si P = 1440 y el anclaje
    cae en el salto."""
    lord_howe = HoraLocal("00:00", "Australia/Lord_Howe")  # DST de 30 min, primer domingo de abril
    velas = continuo("2026-04-03T00:00Z", "2026-04-07T00:00Z")
    salida = agregar(velas, H4, lord_howe)
    assert {v.duracion_min for v in salida} <= {240, 210, 270}
    assert sum(v.n_m1 for v in salida) == len(velas)
    assert all(a.fin == b.inicio for a, b in zip(salida, salida[1:], strict=False))
    diario = agregar(continuo("2026-03-27T00:00Z", "2026-04-01T00:00Z"), 1440, MADRID)
    assert {v.duracion_min for v in diario} <= {1440, 1380}
    assert sum(v.n_m1 for v in diario) == 5 * 1440
