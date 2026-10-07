"""Que el test de rotura de G1 falla cuando debe (trabajo/respaldo-a11, respuesta del consultor del
2026-10-07, punto 2). Sin tocar el codigo ni los tests: se ejecuta la misma comprobacion que
`test_rotura_cada_supersedido_real_citado_en_una_spec_hace_fallar_g1` sobre un `knowledge/spec/`
temporal, y luego dos roturas a proposito, en memoria:

1. con una excepcion para un par real, ese id deja de fallar (el test lo cazaria);
2. con G1 «ciega» (sin cadenas de sustitucion: ningun id cuenta como supersedido), ninguno falla.

Solo lee ids de `knowledge/evidence/`; ninguna cita, ninguna transcripcion.

Uso: uv run python docs/validation/anexos/RESPALDO-A11/rotura_g1.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from botsito.evidence.modelo import cargar_evidencia
from botsito.validation import citas_supersedidas as g1

RAIZ = Path(__file__).resolve().parents[4]


def fallos_por_id(items: list, excepciones: tuple = ()) -> dict[str, int]:
    salida: dict[str, int] = {}
    supersedidos = sorted({i.supersede for i in items if i.supersede})
    with tempfile.TemporaryDirectory() as tmp:
        for n, viejo in enumerate(supersedidos):
            ruta = Path(tmp) / str(n) / "knowledge" / "spec" / "ambiguedades.yaml"
            ruta.parent.mkdir(parents=True)
            ruta.write_text(
                f"ambiguedades:\n  - id: A-11\n    evidencia:\n      - {viejo}\n", encoding="utf-8"
            )
            fallos = g1.citas_a_supersedidos(Path(tmp) / str(n), items, excepciones)[0]
            salida[viejo] = sum(1 for f in fallos if f"nombra {viejo}" in f)
    return salida


def main() -> int:
    items = list(cargar_evidencia(RAIZ / "knowledge" / "evidence"))
    print(f"EXCEPCIONES reales: {g1.EXCEPCIONES!r}")
    normal = fallos_por_id(items)
    print(f"supersedidos reales: {len(normal)}; con G1 tal cual, fallan {sum(normal.values())}")
    for viejo, n in normal.items():
        print(f"  {viejo}: {n} fallo(s)")
    primero = next(iter(normal))
    excepcion = g1.Excepcion("A-11", primero, "rotura a proposito")
    con_excepcion = fallos_por_id(items, (excepcion,))
    print(f"ROTURA 1, una excepcion para (A-11, {primero}): ese id da {con_excepcion[primero]} "
          f"fallo(s) -> el test de rotura FALLARIA")  # fmt: skip
    original = g1.sustitutos
    g1.sustitutos = lambda _items: {}  # type: ignore[assignment]
    try:
        ciega = fallos_por_id(items)
    finally:
        g1.sustitutos = original
    print(f"ROTURA 2, G1 sin cadenas de sustitucion: fallan {sum(ciega.values())} de {len(ciega)} "
          f"-> el test de rotura FALLARIA")  # fmt: skip
    ok = all(n == 1 for n in normal.values()) and con_excepcion[primero] == 0
    ok = ok and sum(ciega.values()) == 0
    print(
        "VEREDICTO: " + ("el test de rotura pasa hoy y falla con las dos roturas" if ok else "NO")
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
