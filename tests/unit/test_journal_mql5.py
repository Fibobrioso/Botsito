"""El journal v1 de la capa de MT5 (trabajo/ea-conexion, R6a.1): el validador de
`botsito.mql5bridge.journal` contra el golden de `tests/golden/journal/`, y cada regla del formato
rota a proposito en los dos sentidos (lo bueno pasa, lo roto no).

El golden lo escribe en MQL5 el script de pruebas (`mql5/Scripts/BotsitoPruebasCapa.mq5`) con el
mismo escritor que el EA, byte a byte (la prueba cruzada; la salida del script, en los anexos de la
rama). La CI no tiene MetaTrader: aqui se valida el golden, que esta en git.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from botsito.mql5bridge.journal import (
    CLAVES,
    GENESIS,
    JournalError,
    canonica,
    hash_linea,
    leer,
    main,
)

GOLDEN = Path(__file__).resolve().parents[1] / "golden" / "journal"
CONTINUA = ("continua/journal_20261026.jsonl", "continua/journal_20261027.jsonl")
ROTA = "rota/journal_20261028.jsonl"
# El hash de la ultima linea de cada cadena del golden. La ultima linea no la encadena ninguna otra:
# fijar su hash aqui hace que cambiar CUALQUIER byte del golden rompa un test (README de golden/).
FINAL_CONTINUA = "e493bc768389a9c7199ca71a894230f0434340f2d1b29c404d2b3c2c5ece43e3"
FINAL_ROTA = "0d2df27139c2ef79ce126ee1f4309fa9a6546a17fe707245e450fcf231a9154b"


def _golden(*nombres: str) -> list[tuple[str, bytes]]:
    return [(n, (GOLDEN / n).read_bytes()) for n in nombres]


def _lineas(contenido: bytes) -> list[bytes]:
    return contenido[:-1].split(b"\n")


def _rehacer(lineas: list[bytes]) -> bytes:
    return b"".join(x + b"\n" for x in lineas)


def _reencadenar(objetos: list[dict[str, Any]]) -> bytes:
    """Escribe objetos como un journal valido: seq y prev recalculados (para romper UNA cosa)."""
    prev, salida = GENESIS, []
    for i, o in enumerate(objetos, start=1):
        o = {**o, "seq": i, "prev": prev}
        b = canonica({k: o[k] for k in CLAVES})
        salida.append(b)
        prev = hash_linea(b)
    return _rehacer(salida)


def _objetos(nombre: str) -> list[dict[str, Any]]:
    return [json.loads(x) for x in _lineas((GOLDEN / nombre).read_bytes())]


# --- el golden ------------------------------------------------------------------------------


def test_el_golden_continuo_es_una_sola_cadena_entre_dias_y_reinicios() -> None:
    lineas = leer(_golden(*CONTINUA))
    assert [x.objeto["seq"] for x in lineas] == list(range(1, len(lineas) + 1))
    assert [x.objeto["prev"] for x in lineas].count(GENESIS) == 1
    arranques = [
        x.objeto["datos"]["cadena_anterior"] for x in lineas if x.objeto["ev"] == "arranque"
    ]
    assert arranques == ["ninguna", "sigue"]
    assert {x.fichero for x in lineas} == set(CONTINUA)
    assert lineas[-1].hash == FINAL_CONTINUA


def test_el_golden_de_la_cadena_rota_empieza_desde_ceros_con_su_arranque() -> None:
    lineas = leer(_golden(ROTA))
    primera = lineas[0].objeto
    assert (primera["ev"], primera["seq"], primera["prev"]) == ("arranque", 1, GENESIS)
    assert primera["datos"]["cadena_anterior"] == "rota"
    assert lineas[-1].hash == FINAL_ROTA


def test_el_hash_es_sha256_de_los_bytes_de_la_linea_sin_el_lf() -> None:
    contenido = (GOLDEN / CONTINUA[0]).read_bytes()
    a, b = _lineas(contenido)[:2]
    assert json.loads(b)["prev"] == hash_linea(a)
    assert json.loads(b)["prev"] != hash_linea(a + b"\n")


def _un_segundo_mas(linea: bytes) -> bytes:
    """La misma linea con srv y gmt un segundo despues: sigue siendo valida por si sola (canonica,
    con su desfase y su prev), asi que solo la caza la cadena."""
    o = json.loads(linea)
    for k in ("srv", "gmt"):
        o[k] = (datetime.fromisoformat(o[k]) + timedelta(seconds=1)).isoformat()
    return canonica(o)


def test_cambiar_una_linea_rompe_la_cadena_o_el_hash_final() -> None:
    for cadena, final in ((CONTINUA, FINAL_CONTINUA), ((ROTA,), FINAL_ROTA)):
        ficheros = _golden(*cadena)
        posiciones = [(f, i) for f, (_, c) in enumerate(ficheros) for i in range(len(_lineas(c)))]
        for f, i in posiciones:
            lineas = _lineas(ficheros[f][1])
            lineas[i] = _un_segundo_mas(lineas[i])
            cambiado = [*ficheros[:f], (ficheros[f][0], _rehacer(lineas)), *ficheros[f + 1 :]]
            if (f, i) != posiciones[-1]:
                with pytest.raises(JournalError, match="prev"):
                    leer(cambiado)
            else:  # la ultima no la encadena ninguna: la caza el hash final fijado
                assert leer(cambiado)[-1].hash != final


# --- cada regla, en los dos sentidos ----------------------------------------------------------


def test_bom_cr_y_ultima_linea_truncada_se_rechazan() -> None:
    bueno = (GOLDEN / ROTA).read_bytes()
    assert leer([("x", bueno)])
    with pytest.raises(JournalError, match="BOM"):
        leer([("x", b"\xef\xbb\xbf" + bueno)])
    with pytest.raises(JournalError, match="CR"):
        leer([("x", bueno.replace(b"\n", b"\r\n"))])
    with pytest.raises(JournalError, match="truncada"):
        leer([("x", bueno[:-1])])
    with pytest.raises(JournalError, match="truncada"):
        leer([("x", bueno[:-20])])


def test_la_forma_canonica_es_obligatoria() -> None:
    # en la ULTIMA linea, que no encadena ninguna otra: si fallara, solo podria ser por la forma
    lineas = _lineas(_reencadenar(_objetos(ROTA)[:2]))
    assert leer([("x", _rehacer(lineas))])
    con_espacio = [lineas[0], lineas[1].replace(b'"v":1,', b'"v": 1,', 1)]
    with pytest.raises(JournalError, match="canonica"):
        leer([("x", _rehacer(con_espacio))])
    escapado = [lineas[0], lineas[1].replace("ñ".encode(), b"\\u00f1")]
    assert escapado[1] != lineas[1]
    with pytest.raises(JournalError, match="canonica"):
        leer([("x", _rehacer(escapado))])


def test_las_claves_y_su_orden() -> None:
    objetos = _objetos(ROTA)
    assert leer([("x", _reencadenar(objetos))])
    desordenado = [{"seq": o["seq"], **{k: v for k, v in o.items() if k != "seq"}} for o in objetos]
    with pytest.raises(JournalError, match="claves"):
        leer(
            [
                (
                    "x",
                    _rehacer(
                        [
                            json.dumps(o, ensure_ascii=False, separators=(",", ":")).encode()
                            for o in desordenado
                        ]
                    ),
                )
            ]
        )
    with pytest.raises(JournalError, match="claves"):
        sobra = [{**o, "login": 1} for o in objetos]
        leer(
            [
                (
                    "x",
                    _rehacer(
                        [
                            json.dumps(o, ensure_ascii=False, separators=(",", ":")).encode()
                            for o in sobra
                        ]
                    ),
                )
            ]
        )


def test_las_reservadas_valen_null_en_v1() -> None:
    objetos = _objetos(ROTA)
    assert leer([("x", _reencadenar(objetos))])
    for clave in ("regla", "condicion", "capa_hash", "spec_hash", "risk_hash", "ambiguas"):
        with pytest.raises(JournalError, match=clave):
            leer([("x", _reencadenar([{**objetos[0], clave: "algo"}, *objetos[1:]]))])


def test_version_seq_y_desfase() -> None:
    objetos = _objetos(ROTA)
    assert leer([("x", _reencadenar(objetos))])
    with pytest.raises(JournalError, match="version"):
        leer([("x", _reencadenar([{**objetos[0], "v": 2}, *objetos[1:]]))])
    with pytest.raises(JournalError, match="desfase"):
        leer([("x", _reencadenar([{**objetos[0], "desfase_s": 7199}, *objetos[1:]]))])
    with pytest.raises(JournalError, match="hora"):
        leer([("x", _reencadenar([{**objetos[0], "srv": "2026.10.28 09:00:00"}, *objetos[1:]]))])
    lineas = _lineas(_reencadenar(objetos))
    hueco = [json.loads(x) for x in lineas]
    hueco[2]["seq"] = 4
    with pytest.raises(JournalError):
        leer([("x", _rehacer([canonica(o) for o in hueco]))])


def test_el_prev_encadena_y_solo_una_cadena_rota_empieza_de_cero() -> None:
    a = (GOLDEN / CONTINUA[0]).read_bytes()
    b = (GOLDEN / CONTINUA[1]).read_bytes()
    assert leer([("a", a), ("b", b)])
    with pytest.raises(JournalError, match="prev"):
        leer([("b", b)])  # el segundo dia solo: su primer prev no tiene linea anterior
    with pytest.raises(JournalError, match="prev"):
        leer([("b", b), ("a", a)])
    # una cadena nueva en medio: valida si la abre un arranque con cadena rota, y no si no
    rota = (GOLDEN / ROTA).read_bytes()
    assert leer([("a", a), ("b", b), ("r", rota)])
    sin_rota = _reencadenar(
        [
            {
                **_objetos(ROTA)[0],
                "datos": {**_objetos(ROTA)[0]["datos"], "cadena_anterior": "ninguna"},
            }
        ]
    )
    with pytest.raises(JournalError, match="cadena nueva"):
        leer([("a", a), ("b", b), ("r", sin_rota)])


def test_los_datos_de_cada_evento_sin_login_ni_dinero() -> None:
    objetos = _objetos(ROTA)
    assert leer([("x", _reencadenar(objetos))])
    cuenta = next(o for o in objetos if o["ev"] == "cuenta")
    for extra in ({"login": 1}, {"saldo": 0}, {"balance": 0}):
        roto = [o if o is not cuenta else {**o, "datos": {**o["datos"], **extra}} for o in objetos]
        with pytest.raises(JournalError, match="datos"):
            leer([("x", _reencadenar(roto))])
    with pytest.raises(JournalError, match="evento"):
        leer([("x", _reencadenar([*objetos[:1], {**objetos[1], "ev": "orden"}]))])
    sesiones = next(o for o in _objetos(CONTINUA[0]) if o["ev"] == "sesiones")
    assert leer([("x", _reencadenar([sesiones]))])
    sin_domingo = {**sesiones["datos"]["trade"]}
    del sin_domingo["SUNDAY"]
    with pytest.raises(JournalError, match="trade"):
        leer(
            [
                (
                    "x",
                    _reencadenar(
                        [{**sesiones, "datos": {**sesiones["datos"], "trade": sin_domingo}}]
                    ),
                )
            ]
        )


def test_la_cli_valida_y_dice_no_valido(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(GOLDEN / n) for n in CONTINUA]) == 0
    assert FINAL_CONTINUA in capsys.readouterr().out
    roto = tmp_path / "j.jsonl"
    roto.write_bytes((GOLDEN / ROTA).read_bytes()[:-1])
    assert main([str(roto)]) == 1
    assert "NO VALIDO" in capsys.readouterr().out
