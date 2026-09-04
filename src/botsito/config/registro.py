"""Registro de parametros: la unica puerta por la que un valor de negocio entra en el codigo.

Fuente de datos: `knowledge/spec/parametros.yaml`. Cada parametro declara nombre, tipo, valor,
unidad, estado, fuente (evidencia, feedback o decision), rango y, si es un default de ambiguedad,
el id de la ambiguedad. Reglas de lectura:

- `UNKNOWN`            → leerlo falla siempre (`ParametroDesconocidoError`).
- `DEFAULT_AMBIGUOUS`  → solo se lee si declara `ambiguedad_id`; la lectura queda anotada.
- `CONFIRMED`          → se lee sin mas.

En F02 el fichero esta vacio de valores: los valores llegan en F11 citando evidencia.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from pathlib import Path
from typing import Literal

import yaml

from botsito.domain.valores import Fraccion, Porcentaje

RUTA_POR_DEFECTO = Path("knowledge/spec/parametros.yaml")
TIPOS = ("fraccion", "porcentaje", "decimal", "entero", "hora", "texto")
TipoParametro = Literal["fraccion", "porcentaje", "decimal", "entero", "hora", "texto"]
TipoFuente = Literal["evidence", "feedback", "decision"]
_HORA = re.compile(r"^\d{2}:\d{2}$")
_NOMBRE = re.compile(r"^[a-z][a-z0-9_]*$")


class Estado(StrEnum):
    CONFIRMED = "CONFIRMED"
    DEFAULT_AMBIGUOUS = "DEFAULT_AMBIGUOUS"
    UNKNOWN = "UNKNOWN"


class RegistroError(ValueError):
    """El fichero de parametros no cumple las reglas del registro."""


class ParametroDesconocidoError(LookupError):
    """Se intento leer un parametro UNKNOWN o inexistente."""


class AmbiguedadNoDeclaradaError(LookupError):
    """Se intento leer un DEFAULT_AMBIGUOUS sin `ambiguedad_id`."""


@dataclass(frozen=True, slots=True)
class Fuente:
    tipo: TipoFuente
    id: str


Valor = Fraccion | Porcentaje | Decimal | int | str


@dataclass(frozen=True, slots=True)
class Parametro:
    nombre: str
    tipo: TipoParametro
    unidad: str
    estado: Estado
    descripcion: str
    valor: Valor | None = None
    fuente: Fuente | None = None
    ambiguedad_id: str | None = None
    minimo: Decimal | None = None
    maximo: Decimal | None = None


@dataclass(frozen=True, slots=True)
class LecturaAmbigua:
    nombre: str
    ambiguedad_id: str
    valor: Valor


@dataclass(slots=True)
class Registro:
    parametros: dict[str, Parametro]
    _lecturas: list[LecturaAmbigua] = field(default_factory=list)

    def obtener(self, nombre: str) -> Valor:
        parametro = self.parametros.get(nombre)
        if parametro is None:
            raise ParametroDesconocidoError(f"parametro no registrado: {nombre}")
        if parametro.estado is Estado.UNKNOWN:
            raise ParametroDesconocidoError(
                f"{nombre} es UNKNOWN: no se puede leer hasta que el trader lo resuelva"
            )
        assert parametro.valor is not None  # garantizado por cargar_registro
        if parametro.estado is Estado.DEFAULT_AMBIGUOUS:
            if not parametro.ambiguedad_id:
                raise AmbiguedadNoDeclaradaError(f"{nombre} es DEFAULT_AMBIGUOUS sin ambiguedad_id")
            self._lecturas.append(LecturaAmbigua(nombre, parametro.ambiguedad_id, parametro.valor))
        return parametro.valor

    def lecturas_ambiguas(self) -> tuple[LecturaAmbigua, ...]:
        """Que defaults de ambiguedad se han usado: el journal (F23) lo recoge."""
        return tuple(self._lecturas)

    def nombres(self) -> frozenset[str]:
        return frozenset(self.parametros)

    def no_confirmados(self) -> tuple[str, ...]:
        """Parametros que todavia no estan CONFIRMED: lo que falta cerrar con el trader."""
        return tuple(n for n, p in self.parametros.items() if p.estado is not Estado.CONFIRMED)

    # Accesores tipados: el dominio lee un tipo concreto, nunca la union `Valor`.

    def fraccion(self, nombre: str) -> Fraccion:
        return self._tipado(nombre, Fraccion)

    def porcentaje(self, nombre: str) -> Porcentaje:
        return self._tipado(nombre, Porcentaje)

    def decimal(self, nombre: str) -> Decimal:
        return self._tipado(nombre, Decimal)

    def entero(self, nombre: str) -> int:
        return self._tipado(nombre, int)

    def hora(self, nombre: str) -> str:
        return self._texto(nombre, "hora")

    def texto(self, nombre: str) -> str:
        return self._texto(nombre, "texto")

    def _tipado[T](self, nombre: str, clase: type[T]) -> T:
        valor = self.obtener(nombre)
        if type(valor) is not clase:
            raise TipoDeParametroError(
                f"{nombre} es {type(valor).__name__}, se esperaba {clase.__name__}"
            )
        return valor

    def _texto(self, nombre: str, tipo: str) -> str:
        valor = self.obtener(nombre)
        if self.parametros[nombre].tipo != tipo or not isinstance(valor, str):
            raise TipoDeParametroError(f"{nombre} no es de tipo {tipo}")
        return valor


def _convertir(tipo: str, bruto: object, nombre: str) -> Valor:
    if isinstance(bruto, float):
        raise RegistroError(f"{nombre}: el valor debe escribirse entre comillas, no como float")
    try:
        if tipo == "fraccion":
            return Fraccion(str(bruto))
        if tipo == "porcentaje":
            return Porcentaje(str(bruto))
        if tipo == "decimal":
            return Decimal(str(bruto))
        if tipo == "entero":
            if isinstance(bruto, bool) or not isinstance(bruto, int):
                raise RegistroError(f"{nombre}: entero invalido {bruto!r}")
            return bruto
        if tipo == "hora":
            if not isinstance(bruto, str) or not _HORA.match(bruto):
                raise RegistroError(f"{nombre}: hora invalida {bruto!r} (formato HH:MM)")
            return bruto
        if tipo == "texto":
            if not isinstance(bruto, str):
                raise RegistroError(f"{nombre}: texto invalido {bruto!r}")
            return bruto
    except RegistroError:
        raise
    except (ValueError, TypeError) as exc:
        raise RegistroError(f"{nombre}: {exc}") from exc
    raise RegistroError(f"{nombre}: tipo desconocido {tipo!r}")


def _magnitud(valor: Valor) -> Decimal | None:
    if isinstance(valor, Fraccion | Porcentaje):
        return valor.valor
    if isinstance(valor, Decimal):
        return valor
    if isinstance(valor, int):
        return Decimal(valor)
    return None


def _limite(bruto: object, nombre: str, campo: str) -> Decimal | None:
    if bruto is None:
        return None
    if isinstance(bruto, bool | float):
        raise RegistroError(f"{nombre}: {campo} debe escribirse entre comillas o como entero")
    try:
        return Decimal(str(bruto))
    except InvalidOperation as exc:
        raise RegistroError(f"{nombre}: {campo} invalido {bruto!r}") from exc


class TipoDeParametroError(TypeError):
    """El parametro existe pero no es del tipo que el codigo esperaba."""


def _parametro(bruto: dict[str, object]) -> Parametro:
    nombre = bruto.get("nombre")
    if not isinstance(nombre, str) or not _NOMBRE.match(nombre):
        raise RegistroError(f"nombre de parametro invalido: {nombre!r}")
    tipo = bruto.get("tipo")
    if tipo not in TIPOS:
        raise RegistroError(f"{nombre}: tipo {tipo!r} no esta en {TIPOS}")
    try:
        estado = Estado(str(bruto.get("estado")))
    except ValueError as exc:
        raise RegistroError(f"{nombre}: estado invalido {bruto.get('estado')!r}") from exc
    for campo in ("unidad", "descripcion"):
        if not isinstance(bruto.get(campo), str) or not str(bruto.get(campo)).strip():
            raise RegistroError(f"{nombre}: falta '{campo}'")

    fuente_bruta = bruto.get("fuente")
    fuente: Fuente | None = None
    if fuente_bruta is not None:
        if not isinstance(fuente_bruta, dict) or fuente_bruta.get("tipo") not in (
            "evidence",
            "feedback",
            "decision",
        ):
            raise RegistroError(f"{nombre}: fuente invalida {fuente_bruta!r}")
        fuente = Fuente(fuente_bruta["tipo"], str(fuente_bruta.get("id", "")).strip())
        if not fuente.id:
            raise RegistroError(f"{nombre}: la fuente necesita un id")

    valor: Valor | None = None
    if "valor" in bruto and bruto["valor"] is not None:
        valor = _convertir(str(tipo), bruto["valor"], nombre)

    if estado is Estado.UNKNOWN:
        if valor is not None:
            raise RegistroError(f"{nombre}: un UNKNOWN no puede tener valor")
    else:
        if valor is None:
            raise RegistroError(f"{nombre}: {estado.value} exige valor")
        if fuente is None:
            raise RegistroError(
                f"{nombre}: {estado.value} exige fuente (evidence/feedback/decision)"
            )
    ambiguedad_id = bruto.get("ambiguedad_id")
    if estado is Estado.DEFAULT_AMBIGUOUS and not ambiguedad_id:
        raise RegistroError(f"{nombre}: DEFAULT_AMBIGUOUS exige ambiguedad_id")
    if estado is not Estado.DEFAULT_AMBIGUOUS and ambiguedad_id:
        raise RegistroError(f"{nombre}: solo DEFAULT_AMBIGUOUS lleva ambiguedad_id")

    minimo = _limite(bruto.get("minimo"), nombre, "minimo")
    maximo = _limite(bruto.get("maximo"), nombre, "maximo")
    if valor is not None:
        magnitud = _magnitud(valor)
        if magnitud is not None:
            if minimo is not None and magnitud < minimo:
                raise RegistroError(f"{nombre}: valor {magnitud} por debajo del minimo {minimo}")
            if maximo is not None and magnitud > maximo:
                raise RegistroError(f"{nombre}: valor {magnitud} por encima del maximo {maximo}")

    return Parametro(
        nombre=nombre,
        tipo=tipo,  # type: ignore[arg-type]  # validado contra TIPOS arriba
        unidad=str(bruto["unidad"]),
        estado=estado,
        descripcion=str(bruto["descripcion"]),
        valor=valor,
        fuente=fuente,
        ambiguedad_id=str(ambiguedad_id) if ambiguedad_id else None,
        minimo=minimo,
        maximo=maximo,
    )


def cargar_registro(ruta: Path = RUTA_POR_DEFECTO) -> Registro:
    """Carga y valida el fichero. Cualquier incumplimiento es `RegistroError`."""
    if not ruta.exists():
        raise RegistroError(f"no existe {ruta}")
    documento = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    if not isinstance(documento, dict) or "parametros" not in documento:
        raise RegistroError(f"{ruta}: se esperaba un mapa con la clave 'parametros'")
    lista = documento["parametros"] or []
    if not isinstance(lista, list):
        raise RegistroError(f"{ruta}: 'parametros' debe ser una lista")
    parametros: dict[str, Parametro] = {}
    for bruto in lista:
        if not isinstance(bruto, dict):
            raise RegistroError(f"{ruta}: entrada invalida {bruto!r}")
        parametro = _parametro(bruto)
        if parametro.nombre in parametros:
            raise RegistroError(f"parametro duplicado: {parametro.nombre}")
        parametros[parametro.nombre] = parametro
    return Registro(parametros)
