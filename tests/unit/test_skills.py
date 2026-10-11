"""Las skills y los agentes de `.claude/` no senalan a la nada (E4, rama `trabajo/entorno-code`).

Las skills apuntan a runbooks, ficheros y otras skills; si uno se renombra, la skill queda
senalando a la nada sin que nadie lo note (patron 5 de ERRORES-RECURRENTES). Falla si una skill o
un agente: nombra entre comillas invertidas una ruta del repo que empieza por `docs/`, `src/`,
`scripts/`, `tests/`, `knowledge/` o `.claude/` y no existe (se ignoran las plantillas: con `<`,
`>`, `{`, `*`, `0N` o `NN`; NN por `ingerir-sesion`, respuesta del consultor del 2026-10-11, 3);
nombra una skill o un agente que no existe; o le falta su cabecera (`name` igual a su carpeta y
`description` en una skill; `name`, `description`, `tools` y `model` en un agente).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[2]
PREFIJOS = ("docs/", "src/", "scripts/", "tests/", "knowledge/", ".claude/")
PLANTILLA = re.compile(r"[<>{*]|0N|NN")
CODIGO = re.compile(r"`([^`\n]+)`")
# un nombre entre comillas invertidas junto a «skill(s)», «subagente» o «agente»
NOMBRADO = re.compile(
    r"\b(?:skills?|subagentes?|agentes?)\s+`([a-z][a-z0-9-]*)`"
    r"|`([a-z][a-z0-9-]*)`\s+(?:skills?|subagentes?|agentes?)\b"
)


def cabecera(texto: str) -> dict[str, object] | None:
    if not texto.startswith("---\n"):
        return None
    bloque, separador, _ = texto[4:].partition("\n---\n")
    if not separador:
        return None
    try:
        doc = yaml.safe_load(bloque)
    except yaml.YAMLError:
        # Claude Code lee la cabecera sin YAML estricto: `abrir-rama` lleva «: » dentro de su
        # `description` sin comillas. Aqui, igual: cada `clave: valor` de primer nivel.
        doc = {
            m.group(1): m.group(2)
            for linea in bloque.splitlines()
            if (m := re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", linea))
        }
    return doc if isinstance(doc, dict) else None


def piezas(raiz: Path) -> list[tuple[str, Path]]:
    """`(tipo, fichero)` de cada skill y cada agente."""
    salida = [("skill", p) for p in sorted((raiz / ".claude" / "skills").glob("*/SKILL.md"))]
    salida += [("agente", p) for p in sorted((raiz / ".claude" / "agents").glob("*.md"))]
    return salida


def rutas_nombradas(texto: str) -> list[str]:
    """Las rutas del repo nombradas entre comillas invertidas: el primer termino del codigo, sin
    `:linea` ni puntuacion final; las plantillas fuera."""
    salida = []
    for codigo in CODIGO.findall(texto):
        termino = codigo.split()[0] if codigo.split() else ""
        if not termino.startswith(PREFIJOS) or PLANTILLA.search(termino):
            continue
        salida.append(re.sub(r"(:\d[\d\-,]*)?[.,;:)]*$", "", termino))
    return salida


def problemas(raiz: Path) -> list[str]:
    todas = piezas(raiz)
    skills = {p.parent.name for t, p in todas if t == "skill"}
    agentes = {p.stem for t, p in todas if t == "agente"}
    salida: list[str] = []
    for tipo, fichero in todas:
        rel = fichero.relative_to(raiz).as_posix()
        texto = fichero.read_text(encoding="utf-8")
        doc = cabecera(texto)
        if doc is None:
            salida.append(f"{rel}: sin cabecera YAML")
            continue
        if tipo == "skill":
            if doc.get("name") != fichero.parent.name:
                salida.append(f"{rel}: `name` ({doc.get('name')}) no es su carpeta")
            if not doc.get("description"):
                salida.append(f"{rel}: sin `description`")
        else:
            for clave in ("name", "description", "tools", "model"):
                if not doc.get(clave):
                    salida.append(f"{rel}: sin `{clave}`")
            if doc.get("name") != fichero.stem:
                salida.append(f"{rel}: `name` ({doc.get('name')}) no es su fichero")
        for ruta in rutas_nombradas(texto):
            if not (raiz / ruta).exists():
                salida.append(f"{rel}: nombra `{ruta}`, que no existe")
        for m in NOMBRADO.finditer(texto):
            nombre = m.group(1) or m.group(2)
            if nombre not in skills | agentes:
                salida.append(f"{rel}: nombra la skill o el agente `{nombre}`, que no existe")
    return salida


def test_las_skills_y_los_agentes_del_repo_no_senalan_a_la_nada() -> None:
    assert problemas(RAIZ) == []


def test_estan_las_piezas_del_entorno() -> None:
    nombres = {p.parent.name if t == "skill" else p.stem for t, p in piezas(RAIZ)}
    assert nombres >= {
        "abrir-rama", "fase-cero", "activar-sesion", "comparar-con-main", "entregar-rama",
        "cerrar-rama", "ingerir-sesion", "retomar-rama", "auditor-encargo", "revisor",
    }  # fmt: skip


# ------------------------------------------------- el test, roto a proposito, tiene que fallar

BUENA = "---\nname: {n}\ndescription: hace algo\n---\n\n# {n}\n\nLee `docs/runbooks/RITUAL.md`.\n"


def _arbol(tmp_path: Path, skills: dict[str, str]) -> Path:
    (tmp_path / "docs" / "runbooks").mkdir(parents=True)
    (tmp_path / "docs" / "runbooks" / "RITUAL.md").write_text("x\n", encoding="utf-8")
    (tmp_path / ".claude" / "agents").mkdir(parents=True)
    for carpeta, texto in skills.items():
        (tmp_path / ".claude" / "skills" / carpeta).mkdir(parents=True)
        (tmp_path / ".claude" / "skills" / carpeta / "SKILL.md").write_text(texto, encoding="utf-8")
    return tmp_path


def test_una_skill_buena_pasa(tmp_path: Path) -> None:
    assert problemas(_arbol(tmp_path, {"buena": BUENA.format(n="buena")})) == []


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        (BUENA.format(n="x") + "Y `docs/runbooks/NO-EXISTE.md`.\n", "que no existe"),
        (BUENA.format(n="otro-nombre"), "no es su carpeta"),
        (BUENA.format(n="x") + "Despues, la skill `no-existe`.\n", "`no-existe`, que no existe"),
        (BUENA.format(n="x") + "Lanza el subagente `fantasma`.\n", "`fantasma`, que no existe"),
        ("---\nname: x\n---\n\n# x\n", "sin `description`"),
        ("# x sin cabecera\n", "sin cabecera YAML"),
    ],
)
def test_cada_defecto_falla(tmp_path: Path, texto: str, esperado: str) -> None:
    salida = problemas(_arbol(tmp_path, {"x": texto}))
    assert len(salida) == 1 and esperado in salida[0], salida


def test_un_agente_sin_model_falla(tmp_path: Path) -> None:
    raiz = _arbol(tmp_path, {})
    (raiz / ".claude" / "agents" / "a.md").write_text(
        "---\nname: a\ndescription: d\ntools: Read\n---\n\ncuerpo\n", encoding="utf-8"
    )
    assert problemas(raiz) == [".claude/agents/a.md: sin `model`"]


@pytest.mark.parametrize(
    "plantilla",
    [
        "`docs/encargos/<rama con - en lugar de />.md`",
        "`docs/validation/SESION-0N-EXTRACCION.md`",
        "`docs/validation/SESION-NN-EXTRACCION.md`",
        "`knowledge/cases/holdout/{1,2,3}/`",
        "`docs/validation/*.md`",
    ],
)
def test_una_plantilla_no_falla(tmp_path: Path, plantilla: str) -> None:
    texto = BUENA.format(n="x") + f"Escribe {plantilla}.\n"
    assert problemas(_arbol(tmp_path, {"x": texto})) == []


def test_la_linea_y_la_puntuacion_no_cuentan(tmp_path: Path) -> None:
    texto = BUENA.format(n="x") + "Ver `docs/runbooks/RITUAL.md:61`, y `docs/runbooks/RITUAL.md`.\n"
    assert problemas(_arbol(tmp_path, {"x": texto})) == []
