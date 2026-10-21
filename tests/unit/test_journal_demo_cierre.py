"""Los journals de la demo de FTMO congelados en los anexos de `trabajo/ea-conexion` (R6a.1;
EA-CONEXION.md §10 y §11): el de la corrida de cierre del 2026-10-21 y el del defecto del
2026-10-20.

Congelar es fijar los bytes: el sha256 de cada fichero es el del original de `MQL5\\Files\\Botsito`
del terminal, y no cambia. Y la corrida de cierre tiene que tener lo que el runbook manda comprobar
(`docs/runbooks/DEMO-FTMO.md`, «El EA de conexion (R6a.1)»): cada `arranque` seguido de `cuenta`,
`reloj` y `sesiones`, un cambio de simbolo, el cambio de dia con sus sesiones y un reinicio pasada
la medianoche del servidor, todo en una sola cadena. El journal del defecto es el otro sentido: le
faltan las lecturas tras los dos cambios de grafico y el reinicio, y la comprobacion lo dice.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from pathlib import Path

from botsito.mql5bridge.journal import Linea, leer

ANEXOS = Path(__file__).resolve().parents[2] / "docs" / "validation" / "anexos" / "EA-CONEXION"
CIERRE = {
    "demo-20261021-cierre/journal_20261021.jsonl": (
        "cc0f2228abd7a2ed131361667ece8fdd0ab223e6cf275566e7bc5acfd82eefce"
    ),
    "demo-20261021-cierre/journal_20261022.jsonl": (
        "82c0e64d199d44e2e256fbce726da663420e2b2118d7571c8b8720c55f5d29ce"
    ),
}
DEFECTO = {
    "demo-20261020-defecto/journal_20261020.jsonl": (
        "f25ab7681b8ee53482396b53a2fbc6c65266eccd8bfe492769b360c6e2fbf0a2"
    ),
    "demo-20261020-defecto/journal_20261021.jsonl": (
        "cde88c65ba2ad2085e3aba31089524daab09f363397909c65db7138a56b6a2e0"
    ),
}
LECTURAS = ("cuenta", "reloj", "sesiones")


def _leer(ficheros: dict[str, str]) -> list[Linea]:
    return leer([(n, (ANEXOS / n).read_bytes()) for n in ficheros])


def problemas_de_la_corrida(lineas: Sequence[Linea]) -> list[str]:
    """Lo que falta a una corrida de la demo frente al runbook; vacio si no falta nada."""
    problemas: list[str] = []
    evs = [x.objeto["ev"] for x in lineas]
    arranques = [i for i, ev in enumerate(evs) if ev == "arranque"]
    for i in arranques:
        if tuple(evs[i + 1 : i + 4]) != LECTURAS:
            problemas.append(f"arranque seq {lineas[i].objeto['seq']} sin cuenta, reloj y sesiones")
    for n, i in enumerate(arranques):
        esperada = "ninguna" if n == 0 else "sigue"
        if lineas[i].objeto["datos"]["cadena_anterior"] != esperada:
            problemas.append(f"arranque seq {lineas[i].objeto['seq']} no es {esperada!r}")
    simbolos = [lineas[i].objeto["datos"]["simbolo"] for i in arranques]
    cambios = [
        i
        for i in arranques
        if i > 0
        and lineas[i - 1].objeto["ev"] == "fin"
        and lineas[i - 1].objeto["datos"]["motivo_texto"] == "REASON_CHARTCHANGE"
    ]
    if not cambios or len(set(simbolos)) < 2:
        problemas.append("ningun cambio de simbolo")
    dias = [i for i, ev in enumerate(evs) if ev == "cambio_de_dia"]
    if not dias:
        problemas.append("ningun cambio_de_dia")
    for i in dias:
        if evs[i + 1 : i + 2] != ["sesiones"]:
            problemas.append(f"cambio_de_dia seq {lineas[i].objeto['seq']} sin sesiones")
    reinicios = [
        i
        for i in arranques
        if dias
        and i > dias[0]
        and lineas[i - 1].objeto["ev"] == "fin"
        and lineas[i - 1].objeto["datos"]["motivo_texto"] == "REASON_REMOVE"
    ]
    if not reinicios:
        problemas.append("ningun reinicio (quitar y poner) pasada la medianoche del servidor")
    if evs[-1] != "fin":
        problemas.append("no acaba en fin")
    return problemas


def test_los_journals_congelados_son_los_bytes_del_terminal() -> None:
    for nombre, sha in {**CIERRE, **DEFECTO}.items():
        assert hashlib.sha256((ANEXOS / nombre).read_bytes()).hexdigest() == sha, nombre


def test_la_corrida_de_cierre_es_una_cadena_con_todo_lo_del_runbook() -> None:
    lineas = _leer(CIERRE)
    assert len(lineas) == 131
    assert problemas_de_la_corrida(lineas) == []


def test_el_journal_del_defecto_no_pasa_por_corrida_de_cierre() -> None:
    lineas = _leer(DEFECTO)
    assert problemas_de_la_corrida(lineas) == [
        "arranque seq 6 sin cuenta, reloj y sesiones",
        "arranque seq 8 sin cuenta, reloj y sesiones",
        "ningun reinicio (quitar y poner) pasada la medianoche del servidor",
    ]


def test_quitar_una_lectura_o_el_reinicio_de_la_corrida_de_cierre_se_ve() -> None:
    lineas = _leer(CIERRE)
    sin_cuenta = [x for x in lineas if x.objeto["seq"] != 12]
    assert problemas_de_la_corrida(sin_cuenta) == ["arranque seq 11 sin cuenta, reloj y sesiones"]
    sin_reinicio = [x for x in lineas if x.objeto["seq"] < 116]
    assert problemas_de_la_corrida(sin_reinicio) == [
        "ningun reinicio (quitar y poner) pasada la medianoche del servidor"
    ]
    sin_sesiones_del_dia = [x for x in lineas if x.objeto["seq"] != 45]
    assert problemas_de_la_corrida(sin_sesiones_del_dia) == ["cambio_de_dia seq 44 sin sesiones"]
