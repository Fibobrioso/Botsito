"""`make rapido` (rama `trabajo/entorno-code`, E3 punto 0 y respuesta del consultor a la PARADA de
ENTORNO-CODE.md §4): itera SIN SELLAR. Ni llega a `desellar`, `sellar` o `check`, ni por sus
prerrequisitos (tambien los de una regla con varios objetivos) ni por un `make` o `$(MAKE)` en una
receta, ni una de sus recetas nombra `sello_make_check`, tampoco a traves de una variable. Lo que
este lector no sabe seguir (`include`, `define`, `!=`) es un problema, no un silencio."""

from __future__ import annotations

import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROHIBIDOS = frozenset({"desellar", "sellar", "check"})
VARIABLE = re.compile(
    r"^(?:(?:export|override)\s+)*([A-Za-z_][A-Za-z0-9_]*)\s*(:=|::=|\?=|\+=|!=|=)\s*(.*)$"
)
OBJETIVO = re.compile(r"^([^\s:#=][^:#=]*?)\s*::?(?!=)\s*(.*)$")
NO_SE_SIGUE = re.compile(r"^\s*(?:-?include|sinclude|define)\b")
REFERENCIA = re.compile(r"\$[({]([A-Za-z_][A-Za-z0-9_]*)[)}]")
SUBMAKE = re.compile(r"(?:\$[({]MAKE[)}]|(?<![\w./\\-])make)(?![\w.-])((?:\s+[^\s;&|]+)*)")


def _leer(
    texto: str,
) -> tuple[dict[str, str], dict[str, tuple[list[str], list[str]]], list[str]]:
    """Las variables; por objetivo, sus prerrequisitos y sus recetas; y lo que no se sabe seguir."""
    variables: dict[str, str] = {}
    objetivos: dict[str, tuple[list[str], list[str]]] = {}
    no_seguido: list[str] = []
    actuales: list[str] = []
    for linea in texto.splitlines():
        if linea.startswith("\t"):
            for nombre in actuales:
                objetivos[nombre][1].append(linea[1:])
            continue
        actuales = []
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if NO_SE_SIGUE.match(linea):
            no_seguido.append(linea.strip())
        elif v := VARIABLE.match(linea):
            nombre, operador, valor = v.groups()
            if operador == "!=":
                no_seguido.append(linea.strip())
            elif operador == "+=":
                variables[nombre] = f"{variables.get(nombre, '')} {valor}"
            else:
                variables[nombre] = valor
        elif o := OBJETIVO.match(linea):
            prerrequisitos, _, en_linea = o.group(2).partition(";")
            for nombre in o.group(1).split():
                actuales.append(nombre)
                previo = objetivos.setdefault(nombre, ([], []))
                previo[0].extend(prerrequisitos.split("#", 1)[0].split())
                if en_linea.strip():
                    previo[1].append(en_linea.strip())
    return variables, objetivos, no_seguido


def _expandir(texto: str, variables: dict[str, str], profundidad: int = 0) -> str:
    assert profundidad < 20, "variables en bucle"
    return REFERENCIA.sub(
        lambda m: (
            _expandir(variables.get(m.group(1), ""), variables, profundidad + 1)
            if m.group(1) != "MAKE"
            else m.group(0)
        ),
        texto,
    )


def problemas(texto: str, inicio: str = "rapido") -> list[str]:
    """Lo que hace que `inicio` pueda desellar, sellar o comprobar entero; vacio si nada."""
    variables, objetivos, no_seguido = _leer(texto)
    if inicio not in objetivos:
        return [f"no existe el objetivo `{inicio}`"]
    vistos: set[str] = set()
    pendientes = [inicio]
    salida = [f"el test no sabe seguir: {linea}" for linea in no_seguido]
    while pendientes:
        nombre = pendientes.pop()
        if nombre in vistos:
            continue
        vistos.add(nombre)
        if nombre in PROHIBIDOS:
            salida.append(f"`{inicio}` llega a `{nombre}`")
            continue
        prerrequisitos, recetas = objetivos.get(nombre, ([], []))
        pendientes.extend(_expandir(" ".join(prerrequisitos), variables).split())
        for receta in recetas:
            expandida = _expandir(receta, variables)
            if "sello_make_check" in expandida:
                salida.append(f"la receta de `{nombre}` nombra sello_make_check: {receta}")
            for sub in SUBMAKE.finditer(expandida):
                destinos = [
                    x for x in sub.group(1).split() if not x.startswith("-") and "=" not in x
                ]
                pendientes.extend(destinos or ["<por defecto>"])
    return salida


def test_el_makefile_real_tiene_rapido_y_no_sella() -> None:
    texto = (RAIZ / "Makefile").read_text(encoding="utf-8")
    assert problemas(texto) == []
    _, objetivos, _ = _leer(texto)
    assert objetivos["rapido"][0] == ["lint", "types", "contracts"]
    assert objetivos["rapido"][1] == []  # sin recetas propias ni variables


def test_el_hook_de_arranque_pasa_por_mypy_strict() -> None:
    _, objetivos, _ = _leer((RAIZ / "Makefile").read_text(encoding="utf-8"))
    estrictas = [r for r in objetivos["types"][1] if "--strict" in r]
    assert any(".claude/hooks/estado_sesion.py" in r for r in estrictas)


# ---------------------------------------------------------------- el test, probado contra roturas

BASE = (
    "PICO = uv run python scripts/pico_memoria.py\n"
    "lint:\n\truff check src\n"
    "desellar:\n\tpython scripts/sello_make_check.py borrar\n"
    "sellar:\n\tpython scripts/sello_make_check.py sellar\n"
    "check: desellar lint sellar\n"
)


def test_rapido_limpio_no_tiene_problemas() -> None:
    assert problemas(BASE + "rapido: lint\n") == []


def test_falla_si_rapido_no_existe() -> None:
    assert problemas(BASE) == ["no existe el objetivo `rapido`"]


def test_falla_si_rapido_llega_a_sellar_desellar_o_check() -> None:
    for objetivo in ("sellar", "desellar", "check"):
        assert problemas(BASE + f"rapido: lint {objetivo}\n") == [f"`rapido` llega a `{objetivo}`"]


def test_falla_si_llega_a_traves_de_otro_objetivo() -> None:
    assert problemas(BASE + "medio: lint sellar\nrapido: medio\n") == ["`rapido` llega a `sellar`"]


def test_falla_si_una_regla_con_varios_objetivos_le_anade_el_sello() -> None:
    # segundo revisor, b1: `rapido otro: sellar` suma `sellar` a `rapido` en GNU make
    assert problemas(BASE + "rapido otro: sellar\nrapido: lint\n") == ["`rapido` llega a `sellar`"]
    assert problemas(BASE + "lint otro: check\nrapido: lint\n") == ["`rapido` llega a `check`"]


def test_falla_si_una_receta_lanza_make_check() -> None:
    for receta in (
        "$(MAKE) check",
        "${MAKE} -f Makefile check",
        "make check",
        "$(UV) run make check",
    ):
        assert problemas(BASE + f"UV = uv\nrapido: lint\n\t{receta}\n") == [
            "`rapido` llega a `check`"
        ], receta
    assert problemas(BASE + "rapido: lint\n\tpython x.py > make-check.log\n") == []


def test_falla_si_una_receta_en_linea_sella() -> None:
    texto = BASE + "rapido: lint ; python scripts/sello_make_check.py sellar\n"
    assert len(problemas(texto)) == 1 and "sello_make_check" in problemas(texto)[0]


def test_lo_que_no_sabe_seguir_es_un_problema() -> None:
    for linea in ("include extra.mk", "-include extra.mk", "define S\nx\nendef", "S != cat x"):
        salida = problemas(f"{linea}\n" + BASE + "rapido: lint\n")
        assert any(p.startswith("el test no sabe seguir") for p in salida), linea


def test_falla_si_una_receta_nombra_sello_make_check_aunque_sea_por_variable() -> None:
    directa = BASE + "rapido:\n\tpython scripts/sello_make_check.py sellar\n"
    assert len(problemas(directa)) == 1 and "sello_make_check" in problemas(directa)[0]
    oculta = "SELLO = scripts/sello_make_check.py\n" + BASE + "rapido:\n\tpython $(SELLO) sellar\n"
    assert len(problemas(oculta)) == 1 and "sello_make_check" in problemas(oculta)[0]
    sumada = "S = scripts/\nS += sello_make_check.py\n" + BASE + "rapido:\n\tpython $(S) sellar\n"
    assert len(problemas(sumada)) == 1 and "sello_make_check" in problemas(sumada)[0]
