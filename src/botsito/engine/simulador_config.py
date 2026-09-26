"""La configuracion del simulador (ADR-0051 §6, PROPUESTO): `knowledge/simulador/llenado.yaml`.

Lo elegible del modelo de llenado vive en datos, no en codigo: si una limite se llena al toque,
el deslizamiento fijo (con su motivo) y el spread supuesto por hora LOCAL para los minutos sin
ticks, con la fuente de la que se midio. Lectura estricta: claves cerradas, tipos exactos, y sin
valor por defecto para nada que no este escrito. Un fichero que no existe o esta incompleto es un
error: el respaldo M1 se niega a correr sin spread supuesto (ADR-0051 §6).
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.domain.ticks import MS_POR_MINUTO
from botsito.domain.velas import MinutoUtc
from botsito.engine.llenado import Configuracion, spread_por_hora

FICHERO_LLENADO = Path("knowledge") / "simulador" / "llenado.yaml"
CLAVES = frozenset(
    {"adr", "limite_llena_al_toque", "deslizamiento_fijo_puntos", "deslizamiento_motivo", "spread"}
)
CLAVES_SPREAD = frozenset({"fuente", "huso", "por_hora_local", "fuera_de_ventana"})
_EPOCA = datetime(1970, 1, 1, tzinfo=UTC)


class ConfigSimuladorError(ValueError):
    """El fichero de configuracion del simulador no tiene la forma declarada."""


@dataclass(frozen=True)
class ConfigLlenado:
    adr: str
    limite_llena_al_toque: bool
    deslizamiento_fijo_puntos: int
    deslizamiento_motivo: str
    spread_fuente: str
    spread_huso: str
    spread_por_hora_local: Mapping[int, int]
    spread_fuera_de_ventana: int

    def configuracion(self) -> Configuracion:
        """La `Configuracion` del modelo, con el spread supuesto resuelto por hora local."""
        zona = huso_canonico(self.spread_huso)
        return Configuracion(
            self.limite_llena_al_toque,
            self.deslizamiento_fijo_puntos,
            spread_por_hora(
                dict(self.spread_por_hora_local), self.spread_fuera_de_ventana, _hora_local(zona)
            ),
        )


def _hora_local(zona: ZoneInfo) -> Callable[[MinutoUtc], int]:
    def hora(minuto: MinutoUtc) -> int:
        return (_EPOCA + timedelta(milliseconds=int(minuto) * MS_POR_MINUTO)).astimezone(zona).hour

    return hora


def _entero_no_negativo(doc: Mapping[str, object], clave: str, donde: str) -> int:
    v = doc.get(clave)
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise ConfigSimuladorError(f"{donde}: {clave} es un entero no negativo")
    return v


def cargar_config_llenado(ruta: Path) -> ConfigLlenado:
    if not ruta.exists():
        raise ConfigSimuladorError(f"no existe {ruta}: el simulador no corre sin su configuracion")
    try:
        doc = leer_yaml(ruta)
    except YamlError as exc:
        raise ConfigSimuladorError(f"{ruta.name}: {exc}") from exc
    donde = ruta.name
    if not isinstance(doc, dict) or set(doc) != CLAVES:
        raise ConfigSimuladorError(f"{donde}: claves exactas {sorted(CLAVES)}")
    adr = doc.get("adr")
    if not isinstance(adr, str) or not adr.startswith("ADR-"):
        raise ConfigSimuladorError(f"{donde}: adr debe ser un id ADR-NNNN")
    al_toque = doc.get("limite_llena_al_toque")
    if not isinstance(al_toque, bool):
        raise ConfigSimuladorError(f"{donde}: limite_llena_al_toque es true o false, sin comillas")
    deslizamiento = _entero_no_negativo(doc, "deslizamiento_fijo_puntos", donde)
    motivo = doc.get("deslizamiento_motivo")
    if not isinstance(motivo, str) or not motivo.strip():
        raise ConfigSimuladorError(f"{donde}: deslizamiento_motivo es obligatorio")
    spread = doc.get("spread")
    if not isinstance(spread, dict) or set(spread) != CLAVES_SPREAD:
        raise ConfigSimuladorError(f"{donde}: spread lleva exactamente {sorted(CLAVES_SPREAD)}")
    fuente = spread.get("fuente")
    if not isinstance(fuente, str) or not fuente.strip():
        raise ConfigSimuladorError(f"{donde}: spread.fuente es obligatoria (de que se midio)")
    huso = spread.get("huso")
    if not isinstance(huso, str):
        raise ConfigSimuladorError(f"{donde}: spread.huso es un nombre IANA")
    try:
        huso_canonico(huso)
    except HusoDesconocidoError as exc:
        raise ConfigSimuladorError(f"{donde}: spread.huso: {exc}") from exc
    por_hora = spread.get("por_hora_local")
    if not isinstance(por_hora, dict) or not por_hora:
        raise ConfigSimuladorError(f"{donde}: spread.por_hora_local es un mapa hora -> puntos")
    tabla: dict[int, int] = {}
    for h, v in por_hora.items():
        if isinstance(h, bool) or not isinstance(h, int) or not 0 <= h <= 23:
            raise ConfigSimuladorError(f"{donde}: hora local invalida {h!r}")
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ConfigSimuladorError(f"{donde}: spread de la hora {h} es un entero no negativo")
        tabla[h] = v
    fuera = _entero_no_negativo(spread, "fuera_de_ventana", donde)
    return ConfigLlenado(
        adr=adr,
        limite_llena_al_toque=al_toque,
        deslizamiento_fijo_puntos=deslizamiento,
        deslizamiento_motivo=motivo,
        spread_fuente=fuente,
        spread_huso=huso,
        spread_por_hora_local=tabla,
        spread_fuera_de_ventana=fuera,
    )


__all__ = ["FICHERO_LLENADO", "ConfigLlenado", "ConfigSimuladorError", "cargar_config_llenado"]
