"""La spec, legible por una persona y GENERADA (F13).

Vive en `cases/` y no en `spec/` por las capas: necesita `cases.ambiguedades` -uno de los cuatro
documentos son las ambiguedades- y `spec` no puede importar `cases` (import-linter). Es el mismo
motivo por el que la hoja del trader tampoco puede ir a `spec/`.

Por que existe: copiar a mano una cifra de `knowledge/spec/` a un documento ha fallado seis veces
en tres dias, y las seis estan documentadas. La leccion ya estaba escrita -"el recuento vivo lo da
`botsito spec status` y NO se copia aqui"- pero es disciplina, no mecanismo. Esto es el mecanismo:
lo que una persona lee sale de la fuente, y una guardia lo comprueba.

CUATRO documentos y no uno, uno por fichero fuente (D1 del brief). El motivo no es el tamano: es
que el hash de la spec cubre TRES ficheros y NO cubre `ambiguedades.yaml`, asi que una cabecera
con `spec_version` y hash mentiria sobre una cuarta parte del contenido. Partiendo por esa
frontera, tres documentos se sellan y el cuarto dice por que no.

Lo que este generador NO hace, y conviene no creer que hace:
  - NO parafrasea la `forma` ejecutable de una regla. La imprime verbatim, en bloque. Parafrasear
    un arbol con `cualquiera_de`/`ninguno_de` y ligadura de variables perderia justo lo que F12
    construyo, y la leccion de F12 esta escrita: casar por subcadena en un JSON "es una trampa que
    bendice mentiras".
  - NO recoge los comentarios de los YAML. `parametros.yaml` lleva significado en sus comentarios
    -"documental por ADR-0017", por ejemplo- y el modelo no los carga. Se pierden aqui y nada lo
    notaria: por eso lo que importa vive en `descripcion`, que si entra (y desde F12, en el hash).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from botsito.spec.modelo import CLASES_REGLA

FICHEROS = ("reglas.md", "parametros.md", "glosario.md", "ambiguedades.md")
DIRECTORIO = "docs/spec"
_AVISO = "<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->"


def _cabecera(titulo: str, manifiesto: dict[str, Any], sellado: bool) -> list[str]:
    sello = (
        f"`spec_version {manifiesto['spec_version']}` · hash `{str(manifiesto['hash'])[:12]}…`"
        if sellado
        else (
            f"`spec_version {manifiesto['spec_version']}` · **sin sello**: el hash cubre "
            f"{', '.join(str(c) for c in manifiesto['cubre'])} y este documento no sale de ninguno "
            f"de ellos"
        )
    )
    return [_AVISO, "", f"# {titulo}", "", sello, ""]


def _bloque(valor: Any) -> list[str]:
    """La `forma` tal cual, sin interpretarla."""
    volcado = json.dumps(valor, ensure_ascii=False, indent=2, sort_keys=True)
    return ["```json", *volcado.splitlines(), "```"]


def _reglas(reglas: list[Any], vocabulario: dict[str, dict[str, Any]], man: dict[str, Any]) -> str:
    vigentes = [r for r in reglas if r.vigente]
    fuera = [r for r in reglas if not r.vigente]
    lineas = _cabecera("Reglas de la operativa", man, sellado=True)
    lineas += [
        f"{len(vigentes)} vigentes y {len(fuera)} descartadas. La precedencia va por CLASE y "
        f"no por el orden de este documento, que es editorial: "
        # De `CLASES_REGLA` y no escrita aqui: es la decision viva (ADR-0018), y ya se escribio
        # AL REVES en dos documentos el 2026-09-12. Copiarla en el fichero cuyo trabajo es matar
        # las copias seria gracioso si no fuera el mismo fallo.
        f"{' > '.join(f'`{c}`' for c in CLASES_REGLA)} (ADR-0018).",
        "",
    ]
    for titulo, grupo in (("Vigentes", vigentes), ("Descartadas", fuera)):
        lineas += [f"## {titulo}", ""]
        for r in sorted(grupo, key=lambda x: x.id):
            lineas += [f"### {r.id} · {r.titulo}", ""]
            lineas += [f"- **Clase**: `{r.clase}`"]
            lineas += [f"- **Cuando**: {r.cuando}"]
            lineas += [f"- **Entonces**: {r.entonces}"]
            if r.parametros:
                lineas += [f"- **Parametros**: {', '.join(f'`{p}`' for p in r.parametros)}"]
            if r.complementa:
                lineas += [f"- **Complementa**: {', '.join(r.complementa)}"]
            lineas += [f"- **Cita**: `{r.cita}` — *«{r.literal}»*"]
            if r.decision:
                lineas += [f"- **Decision**: `{r.decision}` — dice mas que su cita, y lo declara"]
            if r.notas:
                lineas += [f"- **Notas**: {r.notas}"]
            if isinstance(r.forma, dict):
                pendiente = r.forma.get("pendiente_definicion")
                if pendiente:
                    lineas += [
                        "",
                        f"**No es ejecutable todavia** ({pendiente}): la prohibicion esta en pie, "
                        f"pero falta definir su condicion.",
                    ]
                else:
                    lineas += ["", "**Forma ejecutable**, tal cual la lee el motor:", ""]
                    lineas += _bloque(r.forma)
            lineas += [""]
    lineas += ["## Vocabulario", ""]
    for seccion in ("predicados", "acciones", "efectos", "hechos", "acumuladores"):
        entradas = vocabulario.get(seccion) or {}
        lineas += [f"### {seccion} ({len(entradas)})", ""]
        for nombre, datos in sorted(entradas.items()):
            if not isinstance(datos, dict):
                continue
            partes = [f"**`{nombre}`** — {datos.get('descripcion', '')}"]
            if datos.get("argumentos"):
                partes.append(f"Argumentos: {', '.join(f'`{a}`' for a in datos['argumentos'])}.")
            for campo, etiqueta in (("produce", "Lo produce"), ("consume", "Lo consume")):
                if datos.get(campo):
                    partes.append(f"{etiqueta}: {', '.join(str(x) for x in datos[campo])}.")
            if datos.get("depende_de"):
                partes.append(f"Depende de: {', '.join(str(x) for x in datos['depende_de'])}.")
            # La cita del vocabulario se imprime a proposito: durante toda F12 nadie la comprobaba
            # y se podia poner cualquier frase en boca del trader dentro de un predicado.
            if datos.get("cita"):
                partes.append(f"Cita `{datos['cita']}`: *«{datos.get('literal', '')}»*.")
            lineas += ["- " + " ".join(p.strip() for p in partes if p)]
        lineas += [""]
    return "\n".join(lineas).rstrip() + "\n"


def _parametros(registro: Any, man: dict[str, Any]) -> str:
    parametros = registro.parametros
    con_valor = {n: p for n, p in sorted(parametros.items()) if p.valor is not None}
    sin_valor = {n: p for n, p in sorted(parametros.items()) if p.valor is None}
    lineas = _cabecera("Parametros: la unica puerta de los valores", man, sellado=True)
    lineas += [
        f"{len(parametros)} en total: {len(con_valor)} con valor y {len(sin_valor)} sin el. "
        # "Ninguna regla contiene numeros" estuvo aqui escrito a mano hasta la auditoria de cierre
        # de F13, que demostro que no era cierto: `tope: 9.5` pasaba. Ahora lo es -`comprobar_forma`
        # exige que todo argumento sea un NOMBRE- y la frase dice quien lo sostiene, para que se
        # caiga con la guardia el dia que alguien la quite.
        "Ninguna regla contiene un numero: `spec check` exige que cada argumento de una forma "
        "ejecutable sea el NOMBRE de un parametro, de un token declarado o de una ligadura "
        "(ADR-0002, ADR-0019).",
        "",
        "| Parametro | Valor | Estado | Categoria | De donde sale | Unidad |",
        "|---|---|---|---|---|---|",
    ]
    for nombre, p in con_valor.items():
        fuente = f"`{p.fuente.id}`" if p.fuente else "—"
        amb = f" · en revision por {p.ambiguedad_id}" if p.ambiguedad_id else ""
        lineas += [
            f"| `{nombre}` | `{p.valor}` | {p.estado.value}{amb} | {p.categoria} | {fuente} | "
            f"{p.unidad} |"
        ]
    lineas += ["", "## Sin valor, y leerlos FALLA a proposito", ""]
    lineas += [
        "No es que falte rellenarlos: es el comportamiento. El motor que intente leer uno de estos "
        "revienta, y eso es lo correcto.",
        "",
    ]
    for nombre, p in sin_valor.items():
        lineas += [f"- **`{nombre}`** ({p.categoria}) — {p.descripcion}"]
    lineas += ["", "## Quien lee cada valor", ""]
    lineas += [
        "Un valor que ninguna regla nombra declara quien lo consumira; si no, seria un valor que "
        "nadie usa y nadie vigila (F12).",
        "",
    ]
    for nombre, p in con_valor.items():
        if p.consumido_por:
            lineas += [f"- `{nombre}` → {', '.join(p.consumido_por)}"]
    lineas += ["", "## Que dice cada uno", ""]
    for nombre, p in sorted(parametros.items()):
        lineas += [f"### `{nombre}`", "", p.descripcion, ""]
        if p.opciones:
            lineas += [f"Opciones: {', '.join(f'`{o}`' for o in p.opciones)}.", ""]
    return "\n".join(lineas).rstrip() + "\n"


def _glosario(terminos: list[Any], man: dict[str, Any]) -> str:
    lineas = _cabecera("Glosario: que es cada cosa", man, sellado=True)
    lineas += [
        f"{len(terminos)} terminos. Aqui se dice QUE es cada cosa, no que se hace con ella "
        "-eso son las reglas- ni con que numero -eso es el registro-.",
        "",
    ]
    for t in sorted(terminos, key=lambda x: x.termino):
        lineas += [f"### {t.termino}", ""]
        if t.alias:
            lineas += [f"*Tambien: {', '.join(t.alias)}.*", ""]
        lineas += [t.definicion, ""]
        lineas += [
            f"Cita `{t.cita}`: *«{t.literal}»*"
            + (f" · visto en {t.visto_en}" if t.visto_en else ""),
            "",
        ]
    return "\n".join(lineas).rstrip() + "\n"


def _ambiguedades(ambiguedades: list[Any], man: dict[str, Any]) -> str:
    lineas = _cabecera("Ambiguedades: lo que todavia no se sabe", man, sellado=False)
    por_estado: dict[str, list[Any]] = {}
    for a in ambiguedades:
        por_estado.setdefault(a.estado, []).append(a)
    lineas += [
        "Como se cierra cada una: **RESUELTA** solo con un registro de feedback del trader; "
        "**DECIDIDA** por el consultor, con su ADR (ADR-0022); **ABIERTA** es la unica que se "
        "sigue preguntando, y entra en el cuestionario de la sesion siguiente.",
        "",
    ]
    for estado in ("ABIERTA", "DECIDIDA", "RESUELTA"):
        grupo = sorted(por_estado.get(estado, []), key=lambda a: int(a.id[2:]))
        if not grupo:
            continue
        lineas += [f"## {estado} ({len(grupo)})", ""]
        for a in grupo:
            marca = " · **BLOQUEANTE**" if a.bloqueante else ""
            cierre = f" · cerrada por `{a.decision}` el {a.decidida_el}" if a.decision else ""
            lineas += [f"### {a.id} · {a.titulo}{marca}{cierre}", "", a.pregunta, ""]
            if a.parametros:
                lineas += [f"Afecta a: {', '.join(f'`{p}`' for p in a.parametros)}.", ""]
    return "\n".join(lineas).rstrip() + "\n"


def generar(repo: Path) -> dict[str, str]:
    """Los cuatro documentos, como texto. Deterministico: mismo repositorio, mismo resultado."""
    from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades
    from botsito.config.registro import cargar_registro
    from botsito.spec.manifiesto import FICHERO_MANIFIESTO, cargar_manifiesto
    from botsito.spec.modelo import (
        FICHERO_GLOSARIO,
        FICHERO_SPEC,
        cargar_glosario,
        cargar_reglas,
        cargar_vocabulario,
    )

    man = cargar_manifiesto(repo / FICHERO_MANIFIESTO)
    return {
        "reglas.md": _reglas(
            cargar_reglas(repo / FICHERO_SPEC), cargar_vocabulario(repo / FICHERO_SPEC), man
        ),
        "parametros.md": _parametros(
            cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml"), man
        ),
        "glosario.md": _glosario(cargar_glosario(repo / FICHERO_GLOSARIO), man),
        "ambiguedades.md": _ambiguedades(cargar_ambiguedades(repo / FICHERO_AMBIGUEDADES), man),
    }


def comprobar(repo: Path) -> list[str]:
    """Que lo commiteado sea lo que sale de la fuente. Nombra el fichero que no cuadra.

    Se compara el texto entero y no un hash: el hash de la spec no cubre `ambiguedades.yaml`, asi
    que sellar con el mentiria sobre uno de los cuatro. Es el patron de `kit check`, que ya
    sostuvo esto en produccion.
    """
    generado = generar(repo)
    problemas: list[str] = []
    for nombre, texto in sorted(generado.items()):
        ruta = repo / DIRECTORIO / nombre
        if not ruta.is_file():
            problemas.append(f"{DIRECTORIO}/{nombre}: no existe; se genera con `botsito spec docs`")
        elif ruta.read_text(encoding="utf-8") != texto:
            problemas.append(
                f"{DIRECTORIO}/{nombre}: lo commiteado no es lo que sale de knowledge/spec/; "
                f"o se edito a mano, o la spec cambio sin regenerarlo (`botsito spec docs`)"
            )
    return problemas


def escribir(repo: Path) -> list[Path]:
    destino = repo / DIRECTORIO
    destino.mkdir(parents=True, exist_ok=True)
    escritos = []
    for nombre, texto in sorted(generar(repo).items()):
        ruta = destino / nombre
        ruta.write_text(texto, encoding="utf-8", newline="\n")
        escritos.append(ruta)
    return escritos
