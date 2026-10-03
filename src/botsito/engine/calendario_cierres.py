"""El calendario versionado de cierres de mercado de un perfil de cuenta (ADR-0068).

Vive en `knowledge/cuentas/cierres/<perfil>.yaml`, uno por perfil, porque el horario es el de los
servidores de la firma (y en una subcarpeta, porque `perfil_del_repo` toma cada `*.yaml` de
`knowledge/cuentas/` como un perfil). Cada hora DECLARA SU HUSO, como los libros (ADR-0039), y aqui
se convierte en un instante con `zoneinfo`, que pone el cambio de hora en su sitio. Lo que sale es
un `CalendarioCierres` del dominio, ya unido, para el predicado de `domain/cierres.py`.

Lleva:
- `cubre`: los dias revisados, los dos incluidos, en el huso que declara. Fuera, el predicado niega
  (`cierre_sin_calendario`) y el cableado no corre;
- `semanal`: el cierre y la apertura del fin de semana (dia, hora y huso);
- `diario`: el corte de cada dia (hora y huso), aunque sea corto;
- `extraordinarios`: cada cierre con fecha, hora y huso de inicio y fin, y su fuente.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.domain.cierres import CalendarioCierres, Cierre, CierresError, juntar_cierres

CARPETA_CALENDARIOS = Path("knowledge") / "cuentas" / "cierres"
DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")
FUENTE_SEMANAL = "semanal"
FUENTE_DIARIO = "diario"
FUENTE_EXTRAORDINARIO = "extraordinario"
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)
_CLAVES = {"perfil", "simbolo", "cubre", "semanal", "diario", "extraordinarios"}


class CalendarioError(ValueError):
    """Un calendario mal escrito: no se adivina."""


def _ms(dt: datetime) -> int:
    return int((dt - _EPOCA).total_seconds() * 1000)


def _huso(valor: object, donde: str) -> ZoneInfo:
    try:
        return huso_canonico(valor)
    except HusoDesconocidoError as exc:
        raise CalendarioError(f"{donde}: {exc}") from exc


def _hora(valor: object, donde: str) -> time:
    try:
        return time.fromisoformat(str(valor))
    except ValueError as exc:
        raise CalendarioError(f"{donde}: hora {valor!r} no es HH:MM") from exc


def _fecha(valor: object, donde: str) -> date:
    if isinstance(valor, date):
        return valor
    try:
        return date.fromisoformat(str(valor))
    except ValueError as exc:
        raise CalendarioError(f"{donde}: fecha {valor!r} no es AAAA-MM-DD") from exc


def _instante(dia: date, hora: time, huso: ZoneInfo) -> int:
    return _ms(datetime.combine(dia, hora, tzinfo=huso))


def _mapa(valor: object, donde: str) -> Mapping[str, Any]:
    if not isinstance(valor, Mapping):
        raise CalendarioError(f"{donde}: se esperaba un mapa")
    return valor


@dataclass(frozen=True)
class DefinicionCalendario:
    """El YAML leido y validado, todavia sin expandir."""

    ruta: Path
    simbolo: str
    datos: Mapping[str, Any]

    def calendario(self) -> CalendarioCierres:
        """Los cierres de todo lo que cubre, unidos: la pauta semanal y la diaria expandidas dia a
        dia en su huso, y los extraordinarios."""
        cubre = _mapa(self.datos["cubre"], "cubre")
        huso = _huso(cubre.get("huso"), "cubre.huso")
        desde = _fecha(cubre.get("desde"), "cubre.desde")
        hasta = _fecha(cubre.get("hasta"), "cubre.hasta")
        if hasta < desde:
            raise CalendarioError("cubre: hasta va antes que desde")
        cubre_desde = _instante(desde, time(0), huso)
        cubre_hasta = _instante(hasta + timedelta(days=1), time(0), huso)
        # se expande una semana mas a cada lado: un cierre que empieza fuera puede tocar dentro
        dias = [desde + timedelta(days=i) for i in range(-7, (hasta - desde).days + 8)]
        try:
            cierres = self._semanales(dias) + self._diarios(dias) + self._extraordinarios()
            return CalendarioCierres(juntar_cierres(cierres), cubre_desde, cubre_hasta)
        except CierresError as exc:
            raise CalendarioError(f"{self.ruta}: {exc}") from exc

    def _semanales(self, dias: list[date]) -> list[Cierre]:
        s = _mapa(self.datos["semanal"], "semanal")
        cierre, apertura = (
            _mapa(s.get("cierre"), "semanal.cierre"),
            _mapa(s.get("apertura"), "semanal.apertura"),
        )
        dia_c, dia_a = cierre.get("dia"), apertura.get("dia")
        if dia_c not in DIAS or dia_a not in DIAS:
            raise CalendarioError(f"semanal: el dia es uno de {DIAS}")
        h_c, h_a = (
            _hora(cierre.get("hora"), "semanal.cierre"),
            _hora(apertura.get("hora"), "semanal.apertura"),
        )
        z_c, z_a = (
            _huso(cierre.get("huso"), "semanal.cierre"),
            _huso(apertura.get("huso"), "semanal.apertura"),
        )
        salto = (DIAS.index(dia_a) - DIAS.index(dia_c)) % 7 or 7
        return [
            Cierre(
                _instante(d, h_c, z_c),
                _instante(d + timedelta(days=salto), h_a, z_a),
                FUENTE_SEMANAL,
            )
            for d in dias
            if d.weekday() == DIAS.index(dia_c)
        ]

    def _diarios(self, dias: list[date]) -> list[Cierre]:
        s = _mapa(self.datos["diario"], "diario")
        cierre, apertura = (
            _mapa(s.get("cierre"), "diario.cierre"),
            _mapa(s.get("apertura"), "diario.apertura"),
        )
        h_c, h_a = (
            _hora(cierre.get("hora"), "diario.cierre"),
            _hora(apertura.get("hora"), "diario.apertura"),
        )
        z_c, z_a = (
            _huso(cierre.get("huso"), "diario.cierre"),
            _huso(apertura.get("huso"), "diario.apertura"),
        )
        salida = []
        for d in dias:
            inicio = _instante(d, h_c, z_c)
            fin = _instante(d, h_a, z_a)
            if fin <= inicio:
                fin = _instante(d + timedelta(days=1), h_a, z_a)
            salida.append(Cierre(inicio, fin, FUENTE_DIARIO))
        return salida

    def _extraordinarios(self) -> list[Cierre]:
        salida = []
        for i, e in enumerate(self.datos.get("extraordinarios") or []):
            e = _mapa(e, f"extraordinarios[{i}]")
            fuente = e.get("fuente")
            if not isinstance(fuente, str) or not fuente.strip():
                raise CalendarioError(f"extraordinarios[{i}]: sin fuente no entra")
            bordes = []
            for lado in ("inicio", "fin"):
                b = _mapa(e.get(lado), f"extraordinarios[{i}].{lado}")
                donde = f"extraordinarios[{i}].{lado}"
                bordes.append(
                    _instante(
                        _fecha(b.get("fecha"), donde),
                        _hora(b.get("hora"), donde),
                        _huso(b.get("huso"), donde),
                    )
                )
            inicio = _mapa(e.get("inicio"), f"extraordinarios[{i}].inicio")
            salida.append(
                Cierre(bordes[0], bordes[1], f"{FUENTE_EXTRAORDINARIO} {inicio.get('fecha')}")
            )
        return salida


def cargar_calendario(ruta: Path) -> DefinicionCalendario:
    """Lee y valida un calendario; lo que no se entiende se dice, nombrando el fichero."""
    try:
        datos = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise CalendarioError(f"{ruta}: {exc}") from exc
    datos = _mapa(datos, str(ruta))
    if set(datos) != _CLAVES:
        raise CalendarioError(f"{ruta}: claves {sorted(datos)}, se esperaban {sorted(_CLAVES)}")
    if datos["perfil"] != ruta.stem:
        raise CalendarioError(f"{ruta}: perfil {datos['perfil']!r} no es el del fichero")
    definicion = DefinicionCalendario(ruta, str(datos["simbolo"]), datos)
    definicion.calendario()  # que se pueda expandir: si no, falla aqui
    return definicion


def ruta_calendario(repo: Path, perfil: str) -> Path:
    return repo / CARPETA_CALENDARIOS / f"{perfil}.yaml"


__all__ = [
    "CARPETA_CALENDARIOS",
    "CalendarioError",
    "DefinicionCalendario",
    "cargar_calendario",
    "ruta_calendario",
]
