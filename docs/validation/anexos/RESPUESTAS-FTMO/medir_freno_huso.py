"""Fase 0 b) de trabajo/respuestas-ftmo: que cuenta el freno (ADR-0067) y donde corta el dia.

1. Una orden que el SERVIDOR rechaza (precio del lado equivocado) frente a una que el propio bot
   niega (freno): cual se cuenta.
2. firma_huso_corte: su valor en el perfil de FTMO, y el instante UTC de cada medianoche de 2026 y
   2027 en ese huso, comparado con una regla CET/CEST escrita a mano (UTC+1; UTC+2 desde el ultimo
   domingo de marzo a la 01:00 UTC hasta el ultimo domingo de octubre a la 01:00 UTC, la regla de
   la UE), y el freno a cero justo en ese instante."""

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import yaml

from botsito.engine.broker import _dia_local, _medianoche_ms
from botsito.engine.freno import FrenoPeticiones
from tests.unit import test_freno_peticiones as t

RAIZ = Path.cwd()

print("== 1. que cuenta el freno")
b = t._broker()
r = b.colocar_limite("srv", "compra", t.BID + 5000, t.UNO, t.BID + 4900, t.BID + 5300, t._ms(t.M0, 1))
pet = b.traza().peticiones
print(f"  compra limite por ENCIMA del ask: {type(r).__name__} con motivo {getattr(r, 'motivo', '-')}")
print(f"  peticiones en la traza: {len(pet)} (aceptada={[p.aceptada for p in pet]})")
print(f"  freno.total() = {b.freno.total()}  -> la rechazada por el servidor CUENTA")
b2 = t._broker()
n = t.LIMITES.bucle_repeticiones
for i in range(n):
    t._compra(b2, i, t._ms(t.M0, 1) + i * 100, precio=t.BID - 1000)
print(f"  {n} compras iguales: freno.total() = {b2.freno.total()}, negadas = {len(t._negadas(b2))} -> la negada por el bot NO cuenta")

print("== 2. firma_huso_corte")
perfil = yaml.safe_load((RAIZ / "knowledge/cuentas/ftmo-2step-swing-100k.yaml").read_text(encoding="utf-8"))
(valor,) = [p["valor"] for p in perfil["parametros"] if p["nombre"] == "firma_huso_corte"]
print(f"  valor en knowledge/cuentas/ftmo-2step-swing-100k.yaml: {valor}")
from zoneinfo import ZoneInfo  # noqa: E402

huso = ZoneInfo(valor)


def ultimo_domingo(anio: int, mes: int) -> date:
    d = date(anio, mes + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - 6) % 7)


def medianoche_cet_cest(d: date) -> datetime:
    """00:00 hora de Europa central del dia d, en UTC, con la regla de la UE escrita a mano."""
    verano_desde = datetime.combine(ultimo_domingo(d.year, 3), datetime.min.time(), UTC) + timedelta(hours=1)
    verano_hasta = datetime.combine(ultimo_domingo(d.year, 10), datetime.min.time(), UTC) + timedelta(hours=1)
    for desfase in (1, 2):
        candidato = datetime.combine(d, datetime.min.time(), UTC) - timedelta(hours=desfase)
        en_verano = verano_desde <= candidato < verano_hasta
        if (desfase == 2) == en_verano:
            return candidato
    raise AssertionError(d)


dias = invierno = verano = 0
discrepancias = []
d = date(2026, 1, 1)
while d <= date(2027, 12, 31):
    m = _medianoche_ms(d, huso)
    esperado = int(medianoche_cet_cest(d).timestamp() * 1000)
    if m != esperado:
        discrepancias.append(d)
    assert _dia_local(m - 1, huso) == d - timedelta(days=1) and _dia_local(m, huso) == d
    f = FrenoPeticiones(t.LIMITES)
    f.admitir(_dia_local(m - 1, huso), m - 1, "colocar", "a", None, False)
    f.admitir(_dia_local(m, huso), m, "colocar", "b", None, False)
    assert f.total() == 1  # a cero justo en la medianoche
    if (m // 1000) % 86400 == 23 * 3600:
        invierno += 1
    elif (m // 1000) % 86400 == 22 * 3600:
        verano += 1
    dias += 1
    d += timedelta(days=1)
print(f"  {dias} medianoches (2026-01-01..2027-12-31): {invierno} a las 23:00 UTC (CET), {verano} a las 22:00 UTC (CEST)")
print(f"  discrepancias con la regla CET/CEST escrita a mano: {len(discrepancias)}")
print("  el freno vuelve a cero en el milisegundo de cada medianoche: si (assert en los", dias, "dias)")
for anio in (2026, 2027):
    print(f"  {anio}: verano desde {ultimo_domingo(anio, 3)}, invierno desde {ultimo_domingo(anio, 10)}")
