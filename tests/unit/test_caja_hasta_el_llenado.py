"""`caja_se_fija` = `en_cada_cierre_m1` (ADR-0074; sesion 4, S-4): el registro lo dice, y la cota
de peticiones con el 1 expandiendose, sobre velas y un freno SINTETICOS de 2030. El primer test
falla en `main` (el valor era `al_verse_el_punto`); el segundo falla con la caja fija."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from pathlib import Path

from botsito.config.registro import Estado, cargar_registro
from botsito.data.velas import a_minuto
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.engine import zonas
from botsito.engine.broker import PETICION_CANCELAR, PETICION_COLOCAR
from botsito.engine.freno import MOTIVO_BUCLE, FrenoPeticiones
from botsito.engine.simulacion import limites_freno_de
from tests.unit import test_orden_stop_pivote as top

RAIZ = Path(__file__).resolve().parents[2]
REGISTRO = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
DIA = date(2030, 1, 15)
M0 = int(a_minuto(datetime(2030, 1, 15, 8, 0, tzinfo=UTC)))
# una venta: una bajada que marca un BAJO (el punto), y despues velas verdes que suben el maximo
VENTA_CON_SUBIDAS = [1000, 990, 980, 985, 990, 995, 1000, 1006, 1013, 1021]


def test_el_registro_dice_en_cada_cierre_m1_bajo_a49() -> None:
    p = REGISTRO.parametros["caja_se_fija"]
    assert p.valor == "en_cada_cierre_m1"
    assert p.estado is Estado.DEFAULT_AMBIGUOUS and p.ambiguedad_id == "A-49"
    assert p.fuente is not None and (p.fuente.tipo, p.fuente.id) == ("decision", "ADR-0074")


def _zonas_vistas() -> list[zonas.Zona]:
    velas = top._serie(VENTA_CON_SUBIDAS)
    datos = top._Datos(velas, toma=M0 + 1)
    e = top._estado()
    zonas.zona_del_punto(REGISTRO, top._momento(datos, 0), e)  # la toma
    vistas: list[zonas.Zona] = []
    for k in range(3, len(velas)):
        z = zonas.zona_del_punto(REGISTRO, top._momento(datos, k), e)
        assert z is not None, k
        vistas.append(z)
    return vistas


def test_cada_maximo_nuevo_es_otra_zona_del_mismo_punto_y_el_0_no_se_mueve() -> None:
    vistas = _zonas_vistas()
    assert len({z.entrada for z in vistas}) == 1  # el 0, el punto, no se mueve
    extremos = [z.extremo for z in vistas]
    assert extremos == sorted(extremos) and len(set(extremos)) > 1  # el 1 solo sube
    # una zona por maximo distinto: la caja se recalcula en cada cierre de M1 (ADR-0074)
    assert len({z.id for z in vistas}) == len(set(extremos))


def test_la_cota_de_peticiones_con_el_1_expandiendose_no_dispara_el_freno() -> None:
    """Cada 1 nuevo cuesta cancelar y colocar (ADR-0056 §7); la primera colocacion no cancela nada.
    El precio (el 0) es el mismo en todas; el stop, el objetivo y el lote salen del 1 y cambian,
    asi que el freno de bucles (ADR-0067) no las ve iguales; las mismas colocaciones con una sola
    firma si lo disparan. La firma se arma aqui con la forma del broker, no con su codigo: la
    cadena entera por el cableado real es de la rama de motor (ADR-0074 §3)."""
    vistas = _zonas_vistas()
    distintas = sorted({z.id: z for z in vistas}.values(), key=lambda z: z.extremo)
    limites = limites_freno_de(REGISTRO)
    freno = FrenoPeticiones(limites)
    t = M0 * MS_POR_MINUTO
    admitidas = 0
    firmas: list[tuple[object, ...]] = []
    for k, z in enumerate(distintas):
        t += MS_POR_MINUTO
        if k > 0:
            assert freno.admitir(DIA, t, PETICION_CANCELAR, f"o{k - 1}", None, True) is None
            admitidas += 1
        # la forma de la firma del broker (engine/broker.py, `colocar`): el precio es el 0, que
        # no se mueve; el stop y el objetivo salen del 1 y el lote de la distancia, y son los que
        # cambian de una colocacion a la siguiente
        altura = z.extremo - z.entrada
        firma = (
            PETICION_COLOCAR,
            "stop",
            "venta",
            z.entrada,
            z.entrada + altura * 4 // 5,
            z.entrada - 3 * altura,
            (Decimal(600) / Decimal(altura)).quantize(Decimal("0.01")),
        )
        firmas.append(firma)
        assert freno.admitir(DIA, t, PETICION_COLOCAR, f"o{k}", firma, False) is None
        admitidas += 1
    assert len({f[3] for f in firmas}) == 1 and len({f[4] for f in firmas}) == len(firmas)
    assert admitidas == 2 * len(distintas) - 1 == freno.total() and freno.cortado() is None
    # el contraste: las mismas colocaciones con la MISMA firma son un bucle, y el freno corta
    igual = FrenoPeticiones(limites)
    n = limites.bucle_repeticiones
    assert n is not None and len(distintas) >= n
    firma_fija = (PETICION_COLOCAR, "stop", "venta", 979, 991, 919, Decimal(1))
    motivos = [igual.admitir(DIA, t + k * 1000, PETICION_COLOCAR, f"i{k}", firma_fija, False)
               for k in range(len(distintas))]  # fmt: skip
    assert MOTIVO_BUCLE in motivos
