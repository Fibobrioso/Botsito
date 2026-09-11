"""Version y hash de la spec (F11, ADR-0013).

Para que un backtest, un informe o un `Params.mqh` puedan decir contra que spec corrieron hace
falta un identificador que cambie cuando cambia lo que el bot hace. Aqui esta.

Dos decisiones que valen mas que el codigo:

1. El hash entra sobre los TRES ficheros, `parametros.yaml` incluido. Si el registro quedara
   fuera, mover el stop de 0,8 a 0,75 no cambiaria el hash y el pre-vuelo de la demo daria verde
   con una estrategia distinta de la validada, que es justo lo que esto existe para impedir.
2. Se hashea la ESTRUCTURA re-serializada de forma canonica, no los bytes del fichero. Hashear
   bytes convertiria cada comentario y cada salto de linea en parte del contrato: reordenar un
   comentario cambiaria la version de la spec sin cambiar la spec.

Por parametro entran nombre, categoria, tipo, unidad, huso, estado, valor, fuente,
ambiguedad_id, opciones y limites. El ESTADO y la FUENTE entran a proposito: pasar de
DEFAULT_AMBIGUOUS a CONFIRMED no cambia el valor pero si cambia lo que la spec afirma, y quien
mida fidelidad tiene que poder distinguirlo.

`clase` entra desde ADR-0018: decide que regla gana cuando dos aplican a la vez, o sea lo que el
bot hace.

Por regla entra TODO su texto, no solo los campos ejecutables. Un `titulo`, unas `notas` o un
`literal` no los lee el motor, pero son lo que lee la persona que valida, y por tanto parte de lo
que la spec afirma. Con `notas` fuera del hash, la correccion de riesgo de RN-020 se podia borrar
sin mover `spec_version`.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from botsito.comun.yaml_estricto import YamlError, leer_yaml

FICHERO_MANIFIESTO = "knowledge/spec/spec_manifest.yaml"
_SEMVER = re.compile(r"^\d+\.\d+\.\d+$", re.ASCII)

CAMPOS_PARAMETRO = (
    "nombre",
    "categoria",
    "tipo",
    "unidad",
    "estado",
    "valor",
    # `huso` entra porque MUEVE la operativa: cambiar Etc/GMT-2 por UTC desplaza la ventana
    # dos horas y, sin esto, la spec seguiria diciendo ser la misma version.
    "huso",
    "fuente",
    "ambiguedad_id",
    "opciones",
    "minimo",
    "maximo",
)


class ManifiestoSpecError(ValueError):
    """El manifiesto de la spec no cumple su esquema."""


def _canonico(valor: Any) -> Any:
    """Numeros como texto y claves ordenadas: dos formas de escribir lo mismo dan el mismo hash."""
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, int | float):
        return str(valor)
    if isinstance(valor, dict):
        return {str(k): _canonico(v) for k, v in sorted(valor.items(), key=lambda kv: str(kv[0]))}
    if isinstance(valor, list):
        return [_canonico(v) for v in valor]
    return valor


def estructura_para_hash(repo: Path) -> dict[str, Any]:
    """Lo que se hashea: registro, reglas y glosario, sin comentarios ni formato."""
    from botsito.spec.modelo import FICHERO_GLOSARIO, FICHERO_SPEC

    try:
        registro = leer_yaml(repo / "knowledge" / "spec" / "parametros.yaml")
        spec = leer_yaml(repo / FICHERO_SPEC)
        glosario = leer_yaml(repo / FICHERO_GLOSARIO)
    except (OSError, YamlError) as exc:
        raise ManifiestoSpecError(str(exc)) from exc

    parametros = []
    for p in registro.get("parametros", []) if isinstance(registro, dict) else []:
        if not isinstance(p, dict):
            continue
        parametros.append({c: _canonico(p.get(c)) for c in CAMPOS_PARAMETRO})
    parametros.sort(key=lambda p: str(p["nombre"]))

    reglas = []
    for r in spec.get("reglas", []) if isinstance(spec, dict) else []:
        if not isinstance(r, dict):
            continue
        reglas.append(
            {
                c: _canonico(r.get(c))
                # `titulo`, `literal`, `notas` y `decision` entran desde la auditoria del
                # 2026-09-10. No los ejecuta el motor, pero SON lo que la spec afirma: la
                # correccion de riesgo de RN-020 -que el tope porcentual es el unico freno del
                # dia- vivia solo en sus `notas` y se podia borrar sin mover spec_version, y el
                # `titulo` de esa misma regla decia lo contrario que ellas sin que nada lo viera.
                for c in (
                    "id",
                    "titulo",
                    "cuando",
                    "entonces",
                    "parametros",
                    "clase",
                    "complementa",
                    # `forma` es LO QUE EL MOTOR EJECUTA: si queda fuera, cambiar un predicado o un
                    # argumento no moveria la version. Es el mismo fallo que P5 encontro con
                    # `notas`, en el campo mas ejecutable de todos.
                    "forma",
                    "cita",
                    "literal",
                    "notas",
                    "decision",
                    "estado",
                )
            }
        )
    reglas.sort(key=lambda r: str(r["id"]))

    terminos = []
    for t in glosario.get("terminos", []) if isinstance(glosario, dict) else []:
        if not isinstance(t, dict):
            continue
        terminos.append(
            {c: _canonico(t.get(c)) for c in ("termino", "definicion", "cita", "literal")}
        )
    terminos.sort(key=lambda t: str(t["termino"]))

    # El vocabulario con el que se escriben las reglas entra tambien: cambiar los argumentos de un
    # predicado, la base de un acumulador o quien produce un hecho cambia lo que el bot hace.
    vocabulario = {
        seccion: _canonico(spec.get(seccion) or {})
        for seccion in ("predicados", "acciones", "hechos", "acumuladores")
    }
    return {
        "parametros": parametros,
        "reglas": reglas,
        "terminos": terminos,
        **vocabulario,
    }


def hash_de(repo: Path) -> str:
    crudo = json.dumps(
        estructura_para_hash(repo), sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    return hashlib.sha256(crudo.encode("utf-8")).hexdigest()


def cargar_manifiesto(ruta: Path) -> dict[str, Any]:
    try:
        doc = leer_yaml(ruta)
    except (OSError, YamlError) as exc:
        raise ManifiestoSpecError(f"{ruta.name}: {exc}") from exc
    if not isinstance(doc, dict) or set(doc) != {"spec_version", "hash", "generado_el", "cubre"}:
        raise ManifiestoSpecError(
            f"{ruta.name}: se esperan 'spec_version', 'hash', 'generado_el' y 'cubre'"
        )
    version = str(doc["spec_version"])
    if not _SEMVER.match(version):
        raise ManifiestoSpecError(f"{ruta.name}: spec_version {version!r} no es semver")
    if not re.fullmatch(r"[0-9a-f]{64}", str(doc["hash"])):
        raise ManifiestoSpecError(f"{ruta.name}: hash invalido")
    cubre = doc["cubre"]
    if not isinstance(cubre, list) or len(cubre) != 3:
        raise ManifiestoSpecError(f"{ruta.name}: 'cubre' debe nombrar los tres ficheros")
    return doc


def version_sin_subir(repo: Path, ruta: Path) -> str | None:
    """El problema, si la spec cambio respecto a HEAD y `spec_version` sigue siendo la misma.

    El hash solo dice que el manifiesto esta al dia con los ficheros; no impide regenerarlo sin
    pensar. Sin esto, dos backtests con estrategias distintas podrian decir que corrieron con la
    misma version de la spec, que es justo lo que el manifiesto existe para impedir.

    Se compara con HEAD y no con el fichero anterior porque lo que importa es lo que quedo
    registrado: un cambio sin commitear todavia no ha ocurrido para nadie mas.
    """
    from botsito.comun.historial import contenido_en_head
    from botsito.comun.yaml_estricto import cargar_yaml

    ruta_relativa = FICHERO_MANIFIESTO
    anterior = contenido_en_head(repo, ruta_relativa)
    if anterior is None:
        return None  # sin git, sin commits o manifiesto nuevo: no hay con que comparar
    try:
        doc_anterior = cargar_yaml(anterior)
        doc_actual = cargar_manifiesto(ruta)
    except (YamlError, ManifiestoSpecError):
        return None  # el manifiesto de HEAD no es legible: no es este el sitio para denunciarlo
    if not isinstance(doc_anterior, dict):
        return None
    hash_anterior = str(doc_anterior.get("hash", ""))
    version_anterior = str(doc_anterior.get("spec_version", ""))
    cambio = bool(hash_anterior) and hash_anterior != str(doc_actual["hash"])
    if cambio and version_anterior == str(doc_actual["spec_version"]):
        return (
            f"la spec cambio (hash {hash_anterior[:12]}… -> "
            f"{str(doc_actual['hash'])[:12]}…) pero spec_version sigue en "
            f"{version_anterior}: sube la version o dos specs distintas diran ser la misma"
        )
    return None


def comprobar(repo: Path, ruta: Path) -> list[str]:
    """Problemas entre lo que dice el manifiesto y lo que hay en los ficheros."""
    try:
        doc = cargar_manifiesto(ruta)
    except ManifiestoSpecError as exc:
        return [str(exc)]
    problema_version = version_sin_subir(repo, ruta)
    if problema_version is not None:
        return [f"{ruta.name}: {problema_version}"]
    actual = hash_de(repo)
    if doc["hash"] != actual:
        return [
            f"{ruta.name}: el hash no coincide con los ficheros (dice {doc['hash'][:12]}…, "
            f"es {actual[:12]}…); si la spec cambio a proposito, sube spec_version y regenera"
        ]
    return []
