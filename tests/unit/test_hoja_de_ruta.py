"""La hoja de ruta (docs/plan/HOJA-DE-RUTA.md) cuadra con la Next Action, con los heredados y con
lo que el trader ya respondio (`trabajo/hoja-de-ruta`, docs/validation/HOJA-DE-RUTA.md).

Nacio de cuatro descuadres medidos por el consultor el 2026-10-10: el plan maestro sin mantener
desde el 2026-09-16, la activacion de la sesion 4 caida de la Next Action porque solo vivia como
condicion dentro de otras entradas, y la propia F dependiendo de W, ya hecha. Niega por defecto,
en cuatro sentidos:

(a) una letra viva de la Next Action o un heredado vivo que no esta en la hoja como `NA:`/`HER:`;
(b) una referencia `NA:`, `HER:`, `ID:` o `F:` que no existe, o una entrada HECHA que sigue viva;
(c) una entrada de la Next Action que depende de una letra que no esta viva;
(d) una ambiguedad que la tabla final de una sesion da por respondida («resuelve» o «en parte»),
    que sigue ABIERTA y que no esta como `ID:` en un tramo de activacion o de sesion (R1 o R4).

Las funciones reciben TEXTOS: los tests de abajo las corren sobre los ficheros del repo, y los
sinteticos las rompen a proposito en cada sentido.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
HOJA = RAIZ / "docs" / "plan" / "HOJA-DE-RUTA.md"
# Los tramos de activacion o de sesion: donde tiene que estar toda ambiguedad ya respondida.
TRAMOS_DE_SESION = ("R1", "R4")
DEPENDENCIA = re.compile(
    r"(despu[eé]s de|antes de|espera a|junto a|\btras\b)([^.;:]{0,90})", re.IGNORECASE
)
LETRA_SUELTA = re.compile(r"(?<![\w-])([A-Z])(?![\w-])")
REF = re.compile(r"\b(NA|HER|ID|F):((?:A|ADR|RN)-\d+|F\d{2}|\d+|[A-Z])(?![\w-])")
HECHA = re.compile(r"\*\*Estado:\*\*\s*HECHA")
VEREDICTO = re.compile(r"^(no resuelve|resuelve|en parte)", re.IGNORECASE)


# ------------------------------------------------------------------ lo que se lee de cada fichero


def _next_action(ps: str) -> str:
    return ps.split("## Next Action", 1)[1].split("### Pendientes heredados", 1)[0]


def entradas_vivas(ps: str) -> dict[str, str]:
    """`letra -> linea` de cada entrada de la Next Action."""
    salida: dict[str, str] = {}
    for linea in _next_action(ps).splitlines():
        m = re.match(r"^([A-Z])\. ", linea)
        if m:
            salida[m.group(1)] = linea
    return salida


def heredados_vivos(ps: str) -> set[int]:
    bloque = ps.split("### Pendientes heredados", 1)[1].split("\n## ", 1)[0]
    return {int(m.group(1)) for m in re.finditer(r"^- (\d+)\. ", bloque, re.M)}


def letras_hechas(historia: str) -> set[str]:
    return set(re.findall(r"^# Next Action HECHA · ([A-Z]) ·", historia, re.M))


def entradas_de_la_hoja(hoja: str) -> list[tuple[str, str, str]]:
    """`(tramo, titulo, bloque)` de cada `### ` de la hoja; el tramo es el id de su `## `."""
    salida: list[tuple[str, str, str]] = []
    tramo = ""
    for trozo in re.split(r"(?m)^(?=#{2,3} )", hoja):
        if trozo.startswith("## "):
            tramo = trozo[3:].split("·", 1)[0].split("\n", 1)[0].strip()
        elif trozo.startswith("### "):
            salida.append((tramo, trozo.split("\n", 1)[0][4:].strip(), trozo))
    return salida


def referencias(texto: str) -> set[tuple[str, str]]:
    return {(m.group(1), m.group(2)) for m in REF.finditer(texto)}


def respondidas(extraccion: str, nombre: str) -> set[str]:
    """Las `A-nn` que la tabla FINAL de un informe de extraccion da como «resuelve» o «en parte».

    La tabla final es la del ultimo `## ` que nombra una «Tabla». Una plantilla sin contenido no
    tiene: se reconoce por la palabra PLANTILLA en su cabecera. Cualquier otro informe sin tabla
    final es un error, no un cero."""
    secciones = [s for s in re.split(r"(?m)^(?=## )", extraccion) if s.startswith("## ")]
    tablas = [s for s in secciones if "Tabla" in s.split("\n", 1)[0]]
    if not tablas:
        if "PLANTILLA" in extraccion[:600]:
            return set()
        raise AssertionError(f"{nombre}: sin tabla final y sin decir que es una PLANTILLA")
    salida: set[str] = set()
    for fila in tablas[-1].splitlines():
        if not fila.startswith("|") or set(fila) <= set("|-: "):
            continue
        celdas = [c.strip() for c in fila.strip().strip("|").split("|")]
        for k, celda in enumerate(celdas[1:], start=1):
            m = VEREDICTO.match(celda.replace("*", "").strip())
            if m:
                if m.group(1).lower() != "no resuelve":
                    salida |= set(re.findall(r"\bA-\d+\b", " ".join(celdas[:k])))
                break
    return salida


# ------------------------------------------------------------------ los cuatro sentidos


def problemas_a(ps: str, hoja: str) -> list[str]:
    refs = referencias(hoja)
    faltan = [f"NA:{x}" for x in sorted(entradas_vivas(ps)) if ("NA", x) not in refs]
    faltan += [f"HER:{n}" for n in sorted(heredados_vivos(ps)) if ("HER", str(n)) not in refs]
    return [f"vivo en PROJECT_STATE y ausente de la hoja de ruta: {r}" for r in faltan]


def problemas_b(
    ps: str,
    hoja: str,
    historia: str,
    ids_existentes: set[str],
    funcionalidades: set[str],
) -> list[str]:
    vivas, heredados = set(entradas_vivas(ps)), heredados_vivos(ps)
    hechas = letras_hechas(historia)
    problemas: list[str] = []
    for tramo, titulo, bloque in entradas_de_la_hoja(hoja):
        es_hecha = bool(HECHA.search(bloque))
        for tipo, valor in sorted(referencias(bloque)):
            donde = f"{tramo} «{titulo}»: {tipo}:{valor}"
            if tipo == "NA":
                if es_hecha and valor in vivas:
                    problemas.append(f"{donde} esta HECHA y la letra sigue viva")
                elif es_hecha and valor not in hechas:
                    problemas.append(f"{donde} esta HECHA y HISTORIA no la registra")
                elif not es_hecha and valor not in vivas:
                    problemas.append(f"{donde} no es una letra viva de la Next Action")
            elif tipo == "HER":
                vivo = int(valor) in heredados
                if es_hecha and vivo:
                    problemas.append(f"{donde} esta HECHA y el heredado sigue vivo")
                elif not es_hecha and not vivo:
                    problemas.append(f"{donde} no es un heredado vivo")
            elif tipo == "ID" and valor not in ids_existentes:
                problemas.append(f"{donde} no existe")
            elif tipo == "F" and valor not in funcionalidades:
                problemas.append(f"{donde} no es una funcionalidad de MASTER_PLAN §A")
    return problemas


def problemas_c(ps: str) -> list[str]:
    entradas = entradas_vivas(ps)
    problemas: list[str] = []
    for letra, linea in entradas.items():
        for m in DEPENDENCIA.finditer(linea):
            for dep in LETRA_SUELTA.findall(m.group(2)):
                if dep not in entradas:
                    problemas.append(
                        f"{letra} depende («{m.group(0).strip()}») de {dep}, que no esta viva"
                    )
    return problemas


def problemas_d(
    hoja: str, extracciones: Mapping[str, str], estados: Mapping[str, str]
) -> list[str]:
    en_sesion = {
        valor
        for tramo, _, bloque in entradas_de_la_hoja(hoja)
        if tramo in TRAMOS_DE_SESION
        for tipo, valor in referencias(bloque)
        if tipo == "ID"
    }
    problemas: list[str] = []
    for nombre, texto in sorted(extracciones.items()):
        for amb in sorted(respondidas(texto, nombre)):
            if estados.get(amb) == "ABIERTA" and amb not in en_sesion:
                problemas.append(
                    f"{amb}: {nombre} la da por respondida, sigue ABIERTA y no esta en "
                    f"{' ni '.join(TRAMOS_DE_SESION)}"
                )
    return problemas


# ------------------------------------------------------------------ el repo de verdad


def _estados_de_ambiguedades(texto: str) -> dict[str, str]:
    salida: dict[str, str] = {}
    actual = None
    for linea in texto.splitlines():
        if linea.startswith("  - id: "):
            actual = linea.split(": ", 1)[1].strip()
        elif actual and linea.startswith("    estado:"):
            salida[actual] = linea.split(":", 1)[1].strip()
            actual = None
    return salida


def _ids_existentes() -> set[str]:
    spec = RAIZ / "knowledge" / "spec"
    ids = set(_estados_de_ambiguedades((spec / "ambiguedades.yaml").read_text(encoding="utf-8")))
    ids |= {f"ADR-{p.name[:4]}" for p in (RAIZ / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")}
    reglas = (spec / "strategy_spec.yaml").read_text(encoding="utf-8")
    ids |= set(re.findall(r"^\s*- id: (RN-\d+)\s*$", reglas, re.M))
    return ids


def _funcionalidades() -> set[str]:
    plan = (RAIZ / "docs" / "plan" / "MASTER_PLAN.md").read_text(encoding="utf-8")
    seccion = plan.split("## A ·", 1)[1].split("\n## ", 1)[0]
    return set(re.findall(r"^\| (F\d{2}) \|", seccion, re.M))


def _leer(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8")


def _extracciones() -> dict[str, str]:
    return {
        p.name: _leer(p)
        for p in sorted((RAIZ / "docs" / "validation").glob("SESION-*-EXTRACCION.md"))
    }


def test_a_todo_lo_vivo_esta_en_la_hoja_de_ruta() -> None:
    assert problemas_a(_leer(RAIZ / "PROJECT_STATE.md"), _leer(HOJA)) == []


def test_b_cada_referencia_existe_y_ninguna_hecha_sigue_viva() -> None:
    problemas = problemas_b(
        _leer(RAIZ / "PROJECT_STATE.md"),
        _leer(HOJA),
        _leer(RAIZ / "docs" / "state" / "HISTORIA.md"),
        _ids_existentes(),
        _funcionalidades(),
    )
    assert problemas == []


def test_c_ninguna_entrada_de_la_next_action_depende_de_una_letra_muerta() -> None:
    assert problemas_c(_leer(RAIZ / "PROJECT_STATE.md")) == []


def test_d_lo_que_el_trader_respondio_y_sigue_abierto_esta_en_un_tramo_de_sesion() -> None:
    estados = _estados_de_ambiguedades(_leer(RAIZ / "knowledge" / "spec" / "ambiguedades.yaml"))
    assert problemas_d(_leer(HOJA), _extracciones(), estados) == []


def test_las_tablas_finales_de_las_sesiones_se_leen() -> None:
    """Sin esto, (d) podria pasar porque no lee nada: las sesiones 3 y 4 dan respuestas, y la 2
    es una plantilla vacia."""
    extracciones = _extracciones()
    assert respondidas(extracciones["SESION-02-EXTRACCION.md"], "s2") == set()
    assert {"A-18", "A-44", "A-35"} <= respondidas(extracciones["SESION-03-EXTRACCION.md"], "s3")
    s4 = respondidas(extracciones["SESION-04-EXTRACCION.md"], "s4")
    assert {"A-18", "A-49", "A-36", "A-51", "A-42"} <= s4


# ------------------------------------------------------------------ los sinteticos: se rompen


PS = """# PROJECT STATE

## Next Action

E. Activar la sesion 4. Va despues de F.

F. Orden de trabajo: la hoja de ruta manda.

### Pendientes heredados (sin verificar)

- 15. **EN ESPERA: A-18** …

## Known Ambiguities
"""
HISTORIA = "# Next Action HECHA · W · sale de PROJECT_STATE.md en x (2026-10-10)\n"
HOJA_BIEN = """# Hoja

## R0 · Orden

### R0.1 · Esto
- **Refs:** NA:F · ID:ADR-0072 · F:F26

## R1 · Activar

### R1.1 · Sesion 4
- **Refs:** NA:E · HER:15 · ID:A-18

## Carril: hecho

### H.1 · W
- **Refs:** NA:W
- **Estado:** HECHA (CASES-REJILLA.md)
"""
IDS = {"A-18", "ADR-0072"}
FUNCIONES = {"F26"}
EXTRACCION = """# Sesion

## 5. Tabla final

| Codigo | Ambiguedad | Tramo | Propuesta |
|---|---|---|---|
| S-3 | A-18 | 1:00 | **resuelve**: stop |
| S-9 | A-44 | 2:00 | en parte |
| S-17 | A-50 | 3:00 | no resuelve |
"""


def test_los_sinteticos_bien_formados_no_dan_ningun_problema() -> None:
    assert problemas_a(PS, HOJA_BIEN) == []
    assert problemas_b(PS, HOJA_BIEN, HISTORIA, IDS, FUNCIONES) == []
    assert problemas_c(PS) == []
    estados = {"A-18": "ABIERTA", "A-44": "RESUELTA", "A-50": "ABIERTA"}
    assert problemas_d(HOJA_BIEN, {"s.md": EXTRACCION}, estados) == []


def test_a_se_rompe_si_falta_una_letra_viva_o_un_heredado_vivo() -> None:
    sin_e = HOJA_BIEN.replace("NA:E · ", "")
    sin_15 = HOJA_BIEN.replace("HER:15 · ", "")
    assert problemas_a(PS, sin_e) == ["vivo en PROJECT_STATE y ausente de la hoja de ruta: NA:E"]
    assert problemas_a(PS, sin_15) == ["vivo en PROJECT_STATE y ausente de la hoja de ruta: HER:15"]


def test_b_se_rompe_con_una_referencia_que_no_existe() -> None:
    for mala, motivo in (
        ("ID:A-99", "no existe"),
        ("ID:RN-999", "no existe"),
        ("F:F99", "no es una funcionalidad"),
        ("NA:Q", "no es una letra viva"),
        ("HER:99", "no es un heredado vivo"),
    ):
        hoja = HOJA_BIEN.replace("ID:A-18", f"ID:A-18 · {mala}")
        problemas = problemas_b(PS, hoja, HISTORIA, IDS, FUNCIONES)
        assert len(problemas) == 1 and motivo in problemas[0], (mala, problemas)


def test_b_se_rompe_si_una_entrada_hecha_sigue_viva() -> None:
    hoja = HOJA_BIEN.replace("- **Refs:** NA:W", "- **Refs:** NA:E")
    problemas = problemas_b(PS, hoja, HISTORIA, IDS, FUNCIONES)
    assert any("esta HECHA y la letra sigue viva" in p for p in problemas), problemas
    sin_registro = problemas_b(PS, HOJA_BIEN, "", IDS, FUNCIONES)
    assert sin_registro == ["Carril: hecho «H.1 · W»: NA:W esta HECHA y HISTORIA no la registra"]


def test_c_se_rompe_si_una_entrada_depende_de_una_letra_muerta() -> None:
    """Es la forma exacta del `main` del 2026-10-10: F dependia de W, ya HECHA."""
    ps = PS.replace("F. Orden de trabajo", "F. Orden tras W (consultor, 2026-10-10)")
    assert problemas_c(ps) == [
        "F depende («tras W (consultor, 2026-10-10)») de W, que no esta viva"
    ]


def test_d_se_rompe_si_una_respondida_abierta_no_esta_en_un_tramo_de_sesion() -> None:
    estados = {"A-18": "ABIERTA", "A-44": "ABIERTA", "A-50": "ABIERTA"}
    problemas = problemas_d(HOJA_BIEN, {"s.md": EXTRACCION}, estados)
    # A-44 («en parte») falta; A-50 («no resuelve») no cuenta; A-18 esta en R1
    assert problemas == ["A-44: s.md la da por respondida, sigue ABIERTA y no esta en R1 ni R4"]
    fuera = HOJA_BIEN.replace("NA:E · HER:15 · ID:A-18", "NA:E · HER:15").replace(
        "ID:ADR-0072", "ID:ADR-0072 · ID:A-18"
    )
    problemas = problemas_d(fuera, {"s.md": EXTRACCION}, {"A-18": "ABIERTA"})
    assert problemas == ["A-18: s.md la da por respondida, sigue ABIERTA y no esta en R1 ni R4"]


def test_d_niega_un_informe_sin_tabla_final_que_no_es_plantilla() -> None:
    import pytest

    with pytest.raises(AssertionError, match="sin tabla final"):
        respondidas("# Sesion\n\n## 1. Algo\n", "x.md")
    assert respondidas("# PLANTILLA\n\n## 1. Algo\n", "p.md") == set()
