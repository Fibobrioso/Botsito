"""Carga estricta de la StrategySpec y del glosario (F11, ADR-0013).

Una regla no lleva numeros: nombra parametros del registro y el valor lo pone el registro, que es
la unica puerta (ADR-0002). Lo que si lleva es la frase del trader que la sostiene, y esa frase
tiene que coincidir con el registro de feedback que declara: si alguien la retoca para que "quede
mejor", la comprobacion falla. Es la misma idea que ADR-0009 aplica a la evidencia.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from botsito.comun import ids
from botsito.comun.yaml_estricto import YamlError, leer_yaml

FICHERO_SPEC = "knowledge/spec/strategy_spec.yaml"
FICHERO_GLOSARIO = "knowledge/spec/glossary.yaml"

ESTADOS_REGLA = ("VIGENTE", "DESCARTADA")
CAMPOS_REGLA = {"id", "titulo", "cuando", "entonces", "parametros", "cita", "literal", "estado"}
CAMPOS_REGLA_OPCIONALES = {"notas"}
CAMPOS_TERMINO = {"termino", "definicion", "cita"}
CAMPOS_TERMINO_OPCIONALES = {"alias", "visto_en"}

# Un campo ejecutable no puede llevar un valor de negocio: el valor vive en el registro y aqui
# solo va el nombre del parametro. Basta con exigir que ninguna cifra empiece una palabra: asi
# `M15`, `H4` y `liquidez_m15_criterio_toma` pasan -son nombres, no valores- y `0,8` o `15:00`
# no. El lookbehind excluye tambien los digitos, o el `5` de `m15` contaria por su cuenta.
_CIFRA = re.compile(r"(?<![A-Za-z_0-9])\d")


def _cifra_de_negocio(texto: str) -> str | None:
    """La primera cifra que empieza palabra, o None si el texto solo nombra parametros."""
    m = _CIFRA.search(texto)
    return m.group(0) if m else None


class SpecError(ValueError):
    """La spec no cumple su esquema o cita algo que no existe."""


@dataclass(frozen=True, slots=True)
class Regla:
    id: str
    titulo: str
    cuando: str
    entonces: str
    parametros: tuple[str, ...]
    cita: str
    literal: str
    estado: str
    notas: str | None = None

    @property
    def vigente(self) -> bool:
        return self.estado == "VIGENTE"


@dataclass(frozen=True, slots=True)
class Termino:
    termino: str
    definicion: str
    cita: str
    alias: tuple[str, ...] = ()
    visto_en: str | None = None


def _texto(doc: dict[str, Any], campo: str, origen: str) -> str:
    v = doc.get(campo)
    if not isinstance(v, str) or not v.strip():
        raise SpecError(f"{origen}: falta '{campo}'")
    return " ".join(v.split())


def _campos(doc: dict[str, Any], obligatorios: set[str], opcionales: set[str], origen: str) -> None:
    faltan = obligatorios - set(doc)
    if faltan:
        raise SpecError(f"{origen}: faltan campos {sorted(faltan)}")
    sobran = set(doc) - obligatorios - opcionales
    if sobran:
        raise SpecError(f"{origen}: campos desconocidos {sorted(map(str, sobran))}")


def _cita_valida(cita: str) -> bool:
    return ids.es_id_de("evidence", cita) or ids.es_id_de("feedback", cita)


def cargar_reglas(ruta: Path) -> list[Regla]:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise SpecError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"version_esquema", "reglas"}:
        raise SpecError(f"{ruta.name}: se esperan 'version_esquema' y 'reglas'")
    if doc["version_esquema"] != 1:
        raise SpecError(f"{ruta.name}: version_esquema desconocida {doc['version_esquema']!r}")
    bruto = doc["reglas"]
    if not isinstance(bruto, list) or not bruto:
        raise SpecError(f"{ruta.name}: 'reglas' debe ser una lista no vacia")

    reglas: list[Regla] = []
    vistos: set[str] = set()
    for i, r in enumerate(bruto, start=1):
        origen = f"{ruta.name}: regla {i}"
        if not isinstance(r, dict):
            raise SpecError(f"{origen}: no es un mapa")
        _campos(r, CAMPOS_REGLA, CAMPOS_REGLA_OPCIONALES, origen)
        rid = str(r["id"])
        if not ids.es_id_de("regla", rid):
            raise SpecError(f"{origen}: id {rid!r} no tiene formato RN-NNN")
        if rid in vistos:
            raise SpecError(f"{origen}: id repetido {rid}")
        vistos.add(rid)
        estado = str(r["estado"])
        if estado not in ESTADOS_REGLA:
            raise SpecError(f"{rid}: estado {estado!r} no esta en {ESTADOS_REGLA}")
        params = r["parametros"]
        if not isinstance(params, list) or not all(
            isinstance(p, str) and p.strip() for p in params
        ):
            raise SpecError(f"{rid}: 'parametros' debe ser una lista de nombres")
        cita = str(r["cita"])
        if not _cita_valida(cita):
            raise SpecError(f"{rid}: cita {cita!r} no es un id de evidencia ni de feedback")
        for campo in ("cuando", "entonces"):
            texto = _texto(r, campo, rid)
            cifra = _cifra_de_negocio(texto)
            if cifra is not None:
                raise SpecError(
                    f"{rid}: '{campo}' contiene la cifra {cifra!r}; el valor vive en el registro "
                    f"y aqui solo va el nombre del parametro"
                )
        reglas.append(
            Regla(
                id=rid,
                titulo=_texto(r, "titulo", rid),
                cuando=_texto(r, "cuando", rid),
                entonces=_texto(r, "entonces", rid),
                parametros=tuple(params),
                cita=cita,
                literal=_texto(r, "literal", rid),
                estado=estado,
                notas=" ".join(str(r["notas"]).split()) if r.get("notas") else None,
            )
        )
    return reglas


def cargar_glosario(ruta: Path) -> list[Termino]:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise SpecError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"terminos"}:
        raise SpecError(f"{ruta.name}: se espera una unica clave 'terminos'")
    bruto = doc["terminos"]
    if not isinstance(bruto, list) or not bruto:
        raise SpecError(f"{ruta.name}: 'terminos' debe ser una lista no vacia")
    terminos: list[Termino] = []
    vistos: set[str] = set()
    for i, t in enumerate(bruto, start=1):
        origen = f"{ruta.name}: termino {i}"
        if not isinstance(t, dict):
            raise SpecError(f"{origen}: no es un mapa")
        _campos(t, CAMPOS_TERMINO, CAMPOS_TERMINO_OPCIONALES, origen)
        nombre = _texto(t, "termino", origen)
        if nombre.casefold() in vistos:
            raise SpecError(f"{origen}: termino repetido {nombre!r}")
        vistos.add(nombre.casefold())
        cita = str(t["cita"])
        if not _cita_valida(cita):
            raise SpecError(f"{nombre}: cita {cita!r} no es un id de evidencia ni de feedback")
        alias = t.get("alias") or []
        if not isinstance(alias, list) or not all(isinstance(a, str) and a.strip() for a in alias):
            raise SpecError(f"{nombre}: 'alias' debe ser una lista de textos")
        terminos.append(
            Termino(
                termino=nombre,
                definicion=_texto(t, "definicion", nombre),
                cita=cita,
                alias=tuple(" ".join(a.split()) for a in alias),
                visto_en=" ".join(str(t["visto_en"]).split()) if t.get("visto_en") else None,
            )
        )
    return terminos


def comprobar_contra(
    reglas: list[Regla],
    terminos: list[Termino],
    parametros: set[str],
    citas_conocidas: set[str],
) -> list[str]:
    """Que cada regla nombre parametros que existen y cite algo que existe."""
    problemas: list[str] = []
    for r in reglas:
        for p in r.parametros:
            if p not in parametros:
                problemas.append(f"{r.id}: nombra el parametro {p!r}, que no esta en el registro")
        if r.cita not in citas_conocidas:
            problemas.append(f"{r.id}: cita {r.cita}, que no existe")
    for t in terminos:
        if t.cita not in citas_conocidas:
            problemas.append(f"glosario {t.termino!r}: cita {t.cita}, que no existe")
    return problemas
