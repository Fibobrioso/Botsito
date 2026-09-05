"""Carga de YAML estricta para los ficheros de knowledge/.

PyYAML acepta claves duplicadas (gana la ultima, sin aviso) y convierte fechas sin comillas en
`datetime.date`. Ninguna de las dos cosas es aceptable en evidencia, feedback o parametros:
una clave repetida es un fichero corrupto y una fecha debe seguir siendo texto (`2026-09-20`).
Este cargador rechaza las claves duplicadas y deja las fechas como texto. Los enteros, booleanos y
sexagesimales de YAML 1.1 (`1:05:00` -> 3900) se siguen resolviendo: cada esquema exige `str`
donde corresponde y explica que el valor va entre comillas.
"""

from __future__ import annotations

from typing import Any

import yaml

_TAG_FECHA = "tag:yaml.org,2002:timestamp"


class YamlError(ValueError):
    """El texto YAML esta corrupto (clave duplicada) o no es un documento valido."""


class _Cargador(yaml.SafeLoader):
    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
        vistas: set[Any] = set()
        for nodo_clave, _ in node.value:
            clave = self.construct_object(nodo_clave, deep=True)
            if clave in vistas:
                raise YamlError(
                    f"clave duplicada {clave!r} en la linea {nodo_clave.start_mark.line + 1}"
                )
            vistas.add(clave)
        return super().construct_mapping(node, deep)


# Sin resolucion implicita de fechas: `fecha: 2026-09-20` se carga como texto.
_Cargador.yaml_implicit_resolvers = {
    inicial: [(tag, regex) for tag, regex in lista if tag != _TAG_FECHA]
    for inicial, lista in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def cargar_yaml(texto: str) -> Any:
    try:
        return yaml.load(texto, Loader=_Cargador)  # noqa: S506  # SafeLoader derivado
    except yaml.YAMLError as exc:
        raise YamlError(f"YAML invalido: {exc}") from exc
    except TypeError as exc:  # clave no hashable (`? [1, 2]`): PyYAML la deja escapar
        raise YamlError(f"YAML invalido: clave no admitida ({exc})") from exc
