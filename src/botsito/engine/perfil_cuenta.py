"""El perfil de cuenta del simulador (ADR-0050): UNA firma, UN programa, UN tipo de cuenta y UN
capital, en un fichero con el formato del registro y leido por `config.registro.cargar_registro`.

La misma puerta que ADR-0002, los mismos tipos y los mismos tres estados de ADR-0012: un
`UNKNOWN` no tiene valor y leerlo falla NOMBRANDO el parametro y el perfil, que es como el
simulador se niega a correr con lo que la fuente oficial no dice. Aqui no hay ninguna cifra ni
ningun nombre de firma (`tests/contract/test_no_business_literals.py`): cambiar de firma es
cambiar de fichero.

Lo que un perfil tiene que declarar para serlo: solo parametros de categoria `prop_firm`, el
reloj con el que la firma corta el dia (`firma_huso_corte`, un nombre IANA), las fases del
programa (`firma_fases`, en orden) y, por cada fase, si tiene objetivo y dias minimos y, cuando los
tiene, sus cifras (`firma_<fase>_objetivo_aplica`, `firma_<fase>_objetivo`,
`firma_<fase>_dias_minimos_aplica`, `firma_<fase>_dias_minimos`).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.comun.husos import HusoDesconocidoError, huso_canonico
from botsito.config.registro import (
    Estado,
    ParametroDesconocidoError,
    Registro,
    RegistroError,
    cargar_registro,
)
from botsito.domain.valores import Porcentaje

CATEGORIA_PERFIL = "prop_firm"
FASES = "firma_fases"
HUSO_CORTE = "firma_huso_corte"
SUFIJOS_DE_FASE = (
    "objetivo_aplica",
    "objetivo",
    "dias_minimos_aplica",
    "dias_minimos",
)
_FASE = re.compile(r"^[a-z][a-z0-9_]*$", re.ASCII)


class PerfilError(ValueError):
    """El fichero no es un perfil de cuenta."""


class ParametroSinValorError(LookupError):
    """El simulador necesita un parametro que el perfil no tiene con valor: se niega a correr."""


def nombre_de_fase(fase: str, sufijo: str) -> str:
    return f"firma_{fase}_{sufijo}"


@dataclass(frozen=True)
class PerfilCuenta:
    """Un perfil cargado. Cada accesor tipado delega en el registro y convierte la ausencia de
    valor en `ParametroSinValorError` con el nombre del parametro y el del perfil."""

    ruta: Path
    registro: Registro

    @property
    def nombre(self) -> str:
        return self.ruta.stem

    def nombres(self) -> tuple[str, ...]:
        return tuple(sorted(self.registro.parametros))

    def sin_valor(self) -> tuple[str, ...]:
        """Lo que la fuente no dice: los UNKNOWN del perfil, por nombre."""
        return tuple(
            n for n in self.nombres() if self.registro.parametros[n].estado is Estado.UNKNOWN
        )

    def fases(self) -> tuple[str, ...]:
        return tuple(self.texto(FASES).split())

    def huso_corte(self) -> ZoneInfo:
        return huso_canonico(self.texto(HUSO_CORTE))

    def porcentaje(self, nombre: str) -> Porcentaje:
        return self._leer(nombre, self.registro.porcentaje)

    def decimal(self, nombre: str) -> Decimal:
        return self._leer(nombre, self.registro.decimal)

    def entero(self, nombre: str) -> int:
        return self._leer(nombre, self.registro.entero)

    def booleano(self, nombre: str) -> bool:
        return self._leer(nombre, self.registro.booleano)

    def opcion(self, nombre: str) -> str:
        return self._leer(nombre, self.registro.opcion)

    def texto(self, nombre: str) -> str:
        return self._leer(nombre, self.registro.texto)

    def lotes(self, nombre: str) -> Decimal:
        return self._leer(nombre, self.registro.lotes)

    def _leer[T](self, nombre: str, accesor: Callable[[str], T]) -> T:
        try:
            return accesor(nombre)
        except ParametroDesconocidoError as exc:
            raise ParametroSinValorError(
                f"el simulador no puede correr con el perfil {self.nombre}: "
                f"{nombre} no tiene valor ({exc})"
            ) from exc


def cargar_perfil(ruta: Path) -> PerfilCuenta:
    """Carga un perfil por la puerta del registro y comprueba que ES un perfil: solo `prop_firm`,
    con su reloj de corte, sus fases y los cuatro nombres de cada fase. Los valores no se leen
    aqui -eso lo hace el motor cuando los necesita-, salvo el huso y las fases, que hacen falta
    para saber que hay que exigir."""
    try:
        registro = cargar_registro(ruta)
    except RegistroError as exc:
        raise PerfilError(f"{ruta}: {exc}") from exc
    ajenos = sorted(n for n, p in registro.parametros.items() if p.categoria != CATEGORIA_PERFIL)
    if ajenos:
        raise PerfilError(
            f"{ruta}: un perfil de cuenta solo lleva parametros {CATEGORIA_PERFIL}; sobran {ajenos}"
        )
    perfil = PerfilCuenta(ruta=ruta, registro=registro)
    for obligatorio in (HUSO_CORTE, FASES):
        if obligatorio not in registro.parametros:
            raise PerfilError(f"{ruta}: falta {obligatorio}")
    try:
        perfil.huso_corte()
    except ParametroSinValorError as exc:
        raise PerfilError(f"{ruta}: {HUSO_CORTE} sin valor ({exc})") from exc
    except HusoDesconocidoError as exc:
        raise PerfilError(f"{ruta}: {HUSO_CORTE}: {exc}") from exc
    try:
        fases = perfil.fases()
    except ParametroSinValorError as exc:
        raise PerfilError(f"{ruta}: {FASES} sin valor ({exc})") from exc
    if not fases:
        raise PerfilError(f"{ruta}: {FASES} no declara ninguna fase")
    if len(set(fases)) != len(fases):
        raise PerfilError(f"{ruta}: {FASES} repite una fase: {list(fases)}")
    for fase in fases:
        if not _FASE.match(fase):
            raise PerfilError(f"{ruta}: nombre de fase invalido {fase!r}")
        faltan = [
            nombre_de_fase(fase, s)
            for s in SUFIJOS_DE_FASE
            if nombre_de_fase(fase, s) not in registro.parametros
        ]
        if faltan:
            raise PerfilError(f"{ruta}: la fase {fase!r} no declara {faltan}")
    return perfil
