"""Genera el golden del journal v1 (trabajo/ea-conexion, fase 1): los casos fijos que el script de
pruebas de MQL5 (mql5/Scripts/BotsitoPruebasCapa.mq5) tiene que escribir byte a byte con el mismo
escritor que el EA.

Uso (la carpeta de salida, por argumento; nada sale de __file__):

    uv run python docs/validation/anexos/EA-CONEXION/fase1/generar_golden.py <carpeta>

Escribe <carpeta>/continua/journal_20261026.jsonl y journal_20261027.jsonl (una cadena que sigue
tras un reinicio y un cambio de dia) y <carpeta>/rota/journal_20261028.jsonl (la cadena nueva tras
una ultima linea truncada). Todos los valores son de prueba: ni el servidor, ni el simbolo, ni las
horas son de ninguna cuenta.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from botsito.mql5bridge.journal import CLAVES, GENESIS, RESERVADAS, canonica, hash_linea

SERVIDOR = 'Servidor "Prueba" ñ\\ü'
SIMBOLO = "XYZ.prueba"
TRADE = {
    "SUNDAY": [],
    "MONDAY": [[300, 86100]],
    "TUESDAY": [[300, 86100]],
    "WEDNESDAY": [[300, 86100]],
    "THURSDAY": [[300, 86100]],
    "FRIDAY": [[300, 86100]],
    "SATURDAY": [],
}
QUOTE = {
    "SUNDAY": [],
    "MONDAY": [[0, 3600], [3660, 86340]],
    "TUESDAY": [[300, 86100]],
    "WEDNESDAY": [[300, 86100]],
    "THURSDAY": [[300, 86100]],
    "FRIDAY": [[300, 86100]],
    "SATURDAY": [],
}


def _iso(t: str) -> str:
    return datetime.fromisoformat(t).isoformat()


class Cadena:
    def __init__(self) -> None:
        self.seq = 0
        self.prev = GENESIS
        self.lineas: list[tuple[str, bytes]] = []

    def nueva(self) -> None:
        self.seq = 0
        self.prev = GENESIS

    def escribir(self, fichero: str, srv: str, gmt: str, ev: str, datos: dict) -> None:
        self.seq += 1
        d = int((datetime.fromisoformat(srv) - datetime.fromisoformat(gmt)).total_seconds())
        obj = {
            "v": 1,
            "seq": self.seq,
            "srv": _iso(srv),
            "gmt": _iso(gmt),
            "desfase_s": d,
            "ev": ev,
            "datos": datos,
            **{k: None for k in RESERVADAS},
            "prev": self.prev,
        }
        assert tuple(obj) == CLAVES
        b = canonica(obj)
        self.lineas.append((fichero, b))
        self.prev = hash_linea(b)


def _arranque(cadena: str, conectado: bool) -> dict:
    return {
        "version_ea": "1.0",
        "build": 6230,
        "simbolo": SIMBOLO,
        "conectado": conectado,
        "cadena_anterior": cadena,
    }


def _cuenta(trade_mode: str) -> dict:
    return {
        "trade_mode": trade_mode,
        "margin_mode": "ACCOUNT_MARGIN_MODE_RETAIL_HEDGING",
        "servidor": SERVIDOR,
        "conectado": True,
    }


def _reloj() -> dict:
    return {
        "time_current": "2026-10-26T23:51:58",
        "time_trade_server": "2026-10-26T23:52:00",
        "time_gmt": "2026-10-26T21:52:00",
        "time_local": "2026-10-26T16:52:00",
        "desfase_servidor_gmt_min": 120,
        "desfase_local_gmt_min": -300,
        "time_gmt_offset_seg": 18000,
        "horario_verano_local_seg": 0,
    }


def _sesiones() -> dict:
    return {"trade": TRADE, "quote": QUOTE, "tope_alcanzado": False}


def casos() -> dict[str, list[bytes]]:
    c = Cadena()
    d26, d27 = "continua/journal_20261026.jsonl", "continua/journal_20261027.jsonl"
    c.escribir(
        d26, "2026-10-26T23:50:00", "2026-10-26T21:50:00", "arranque", _arranque("ninguna", False)
    )
    c.escribir(
        d26,
        "2026-10-26T23:51:00",
        "2026-10-26T21:51:00",
        "latido",
        {"conectado": False, "time_current": "2026-10-23T23:54:59"},
    )
    c.escribir(
        d26,
        "2026-10-26T23:52:00",
        "2026-10-26T21:52:00",
        "cuenta",
        _cuenta("ACCOUNT_TRADE_MODE_DEMO"),
    )
    c.escribir(d26, "2026-10-26T23:52:00", "2026-10-26T21:52:00", "reloj", _reloj())
    c.escribir(d26, "2026-10-26T23:52:00", "2026-10-26T21:52:00", "sesiones", _sesiones())
    c.escribir(
        d26,
        "2026-10-26T23:53:00",
        "2026-10-26T21:53:00",
        "latido",
        {"conectado": True, "time_current": "2026-10-26T23:52:59"},
    )
    c.escribir(
        d26,
        "2026-10-26T23:54:00",
        "2026-10-26T21:54:00",
        "fin",
        {"motivo": 1, "motivo_texto": "REASON_REMOVE"},
    )
    # el reinicio: el mismo dia, la cadena sigue
    c.escribir(
        d26, "2026-10-26T23:56:00", "2026-10-26T21:56:00", "arranque", _arranque("sigue", True)
    )
    c.escribir(
        d26,
        "2026-10-26T23:56:00",
        "2026-10-26T21:56:00",
        "cuenta",
        _cuenta("ACCOUNT_TRADE_MODE_DEMO"),
    )
    c.escribir(
        d26,
        "2026-10-26T23:59:00",
        "2026-10-26T21:59:00",
        "latido",
        {"conectado": True, "time_current": "2026-10-26T23:58:59"},
    )
    # el cambio de dia del servidor: fichero nuevo, la cadena sigue
    c.escribir(
        d27,
        "2026-10-27T00:00:00",
        "2026-10-26T22:00:00",
        "cambio_de_dia",
        {"dia_anterior": "2026-10-26", "dia_nuevo": "2026-10-27"},
    )
    c.escribir(d27, "2026-10-27T00:00:00", "2026-10-26T22:00:00", "sesiones", _sesiones())
    c.escribir(
        d27,
        "2026-10-27T00:01:00",
        "2026-10-26T22:01:00",
        "fin",
        {"motivo": 0, "motivo_texto": "REASON_PROGRAM"},
    )

    # la cadena rota: la ultima linea del dia anterior no valida, y empieza otra desde ceros
    c.nueva()
    r = "rota/journal_20261028.jsonl"
    c.escribir(r, "2026-10-28T09:00:00", "2026-10-28T07:00:00", "arranque", _arranque("rota", True))
    c.escribir(
        r,
        "2026-10-28T09:00:00",
        "2026-10-28T07:00:00",
        "cuenta",
        _cuenta("ACCOUNT_TRADE_MODE_REAL"),
    )
    c.escribir(
        r,
        "2026-10-28T09:00:00",
        "2026-10-28T07:00:00",
        "negativa",
        {
            "trade_mode": "ACCOUNT_TRADE_MODE_REAL",
            "motivo": 'la cuenta NO es DEMO: "el EA" se quita\ty no hace nada\n\x01',
        },
    )
    c.escribir(
        r,
        "2026-10-28T09:00:01",
        "2026-10-28T07:00:01",
        "fin",
        {"motivo": 1, "motivo_texto": "REASON_REMOVE"},
    )

    ficheros: dict[str, list[bytes]] = {}
    for f, b in c.lineas:
        ficheros.setdefault(f, []).append(b)
    return ficheros


def main(argv: list[str]) -> int:
    salida = Path(argv[1])
    for nombre, lineas in casos().items():
        destino = salida / nombre
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(b"".join(x + b"\n" for x in lineas))
        print(destino)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
