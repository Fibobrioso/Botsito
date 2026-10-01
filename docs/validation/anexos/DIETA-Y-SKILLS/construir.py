"""Compone el PROJECT_STATE.md nuevo y docs/state/HISTORIA.md (rama `trabajo/dieta-y-skills`).

Segundo guion de la dieta, despues de `dieta.py`, cuya salida lee. Tampoco escribe en el
repositorio: deja `PROJECT_STATE.md` e `HISTORIA.md` en `--salida`, y la sesion los copia.

Todo lo que PROJECT_STATE conserva sale del original COPIADO, no reescrito: cada trozo se busca
literal en el original y el guion se para si no esta. Lo unico escrito de nuevo son los marcos de
cada seccion (que hay aqui y donde esta lo demas) y la linea J del Next Action, que pide el
encargo.

Uso: uv run python docs/validation/anexos/DIETA-Y-SKILLS/construir.py --salida <la de dieta.py>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from dieta import entradas, secciones  # noqa: E402

CABECERA_HISTORIA = """\
# Historia del estado del proyecto

> Lo que `PROJECT_STATE.md` ya no lleva porque dejo de ser el presente: la historia de merges, las
> funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas pagadas y las
> secciones que se quedaron sin uso. Nacio el 2026-10-01 en `trabajo/dieta-y-skills`
> (docs/validation/DIETA-Y-SKILLS.md), cuando `PROJECT_STATE.md` pesaba 418.819 bytes.
>
> **SOLO SE AMPLIA. Nunca se reescribe ni se borra una linea**: cada version commiteada empieza por
> la anterior, byte a byte, y lo vigila `tests/unit/test_historia.py` contra el historial de git.
> Un archivo nuevo se anade AL FINAL con su encabezado `# Archivo N · …` (docs/state/README.md).
>
> Cada archivo copia TAL CUAL lo que se saco de `PROJECT_STATE.md`, con sus encabezados `##` de
> entonces. Para buscar: el titulo de la seccion (`## Change Log`, `## Technical Debt`…) o la frase
> que `PROJECT_STATE.md` conserva como arranque de una entrada.

# Archivo 1 · PROJECT_STATE.md entero en df6aa2c (2026-10-01, `stable/F36j-guardia-linux`)

"""

PREAMBULO = """\
# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).
"""

CURRENT_FEATURE = (
    "EN CURSO: `trabajo/dieta-y-skills` (2026-10-01; encargo "
    "docs/encargos/trabajo-dieta-y-skills.md, informe docs/validation/DIETA-Y-SKILLS.md): menos "
    "contexto por sesion y los rituales como skills; no cambia motor, spec, knowledge ni ninguna "
    "cifra. En `main`, NINGUNA ABIERTA tras `stable/F36j-guardia-linux`; lo que decia esta seccion, "
    "en docs/state/HISTORIA.md (Archivo 1)."
)

TESTS = (
    "{n} funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la "
    "lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently "
    "Passing»)."
)

LINEA_J = (
    "J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan "
    "híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el "
    "umbral no lo escribe la sesion.)"
)

MARCO_AMBIGUEDADES = """\
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).
"""

MARCO_CANDIDATAS = "Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):"

MARCO_DEUDA = """\
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.
"""

PUNTERO_PATRONES = " Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md."

MARCO_REGLAS = """\
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.
"""

MARCO_COMPLETED = """\
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos.
— ninguna desde el Archivo 1 (2026-10-01).
"""

MARCO_CHANGELOG = """\
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli.
— ninguna desde el Archivo 1 (2026-10-01).
"""


def literal(original: str, trozo: str) -> str:
    assert trozo in original, trozo[:80]
    return trozo


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--tests", required=True, type=int)
    args = ap.parse_args()
    s: Path = args.salida
    original = (s / "original.md").read_text(encoding="utf-8")
    sec = secciones(original)

    estable = literal(original, sec["Stable Main State"].strip().split("\n")[0])
    ultimo = literal(original, sec["Last Stable Commit"].strip())

    na = sec["Next Action"].split("\n")
    corte = next(i for i, ln in enumerate(na) if ln.startswith("LO QUE DECIA NEXT ACTION"))
    # Vigente = lo que no esta HECHO: B, C, D y G de la lista AHORA dicen HECHA y se quedan en
    # HISTORIA, con lo que cada una deja pendiente citado literal en el puntero.
    hechas = {"B", "C", "D", "G"}
    vigente = "\n\n".join(
        literal(original, ln)
        for ln in na[:corte]
        if ln.strip() and not (ln[:1] in hechas and ln[1:3] == ". ")
    )
    for letra in hechas:
        assert any(ln.startswith(f"{letra}. ") and "HECHA" in ln for ln in na[:corte]), letra
    pendientes_de_hechas = (
        "B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, "
        "«Next Action»); de ellas sigue pendiente lo que D dice -«"
        + literal(original, "El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor")
        + "»- y lo que G dice: «"
        + literal(
            original,
            "pendiente para la demo de FTMO, el break even de una venta que salta por el ASK "
            "(ADR-0065 §6)",
        )
        + "»."
    )
    historico = "\n".join(na[corte:])
    sin_hecho = []
    for ln in historico.split("\n"):
        m = re.match(r"\s*(?:(\d+)\.|(A\d)\.|(\w)\))\s", ln)
        if m and "HECH" not in ln[:220]:
            sin_hecho.append(next(g for g in m.groups() if g))
    print("Next Action historico sin HECHO en su arranque:", sin_hecho)
    puntero_na = (
        "Lo que decia esta seccion debajo de la lista de arriba -«LO QUE DECIA NEXT ACTION HASTA "
        "EL 2026-09-30», «LO QUE ERA AHORA HASTA EL 2026-09-30» (A1 a A5, con las ramas a) a e) "
        "de A3) y los puntos 0 a 37 «numerados como estaba»- esta tal cual en "
        "docs/state/HISTORIA.md (Archivo 1, «Next Action»). Sin HECHO ni HECHA en su propia "
        "linea quedan alli: "
        + ", ".join(sin_hecho)
        + ". La primera linea de ese bloque da ademas por HECHAS las ramas a, b, c y 0 de A3 y "
        "A4 (la d es la D de arriba), y A4 deja «PENDIENTE, NO APLICADO» la propuesta de cambiar "
        "ADR-0057 §5."
    )

    candidatas = literal(
        original,
        next(
            e for e in entradas(sec["Open Questions"]) if e.startswith("- Candidatas a ambiguedad")
        ),
    )
    deuda = (s / "deuda.md").read_text(encoding="utf-8").rstrip("\n").split("\n- ")
    deuda = [d if d.startswith("- ") else "- " + d for d in deuda]
    deuda = [d + PUNTERO_PATRONES if "LOS CINCO PATRONES" in d else d for d in deuda]
    for d in deuda:
        literal(original, d.removesuffix(PUNTERO_PATRONES).rstrip("…"))
    tabla = (s / "ambiguedades.md").read_text(encoding="utf-8").strip()

    # De «Change Regimes», solo las lineas que `CLAUDE.md` («Regimenes de cambio») no dice: las
    # demas estan alli con las mismas palabras.
    regimenes = [
        e
        for e in entradas(sec["Change Regimes (must be respected)"])
        if e.startswith(("- knowledge/cases/holdout/", "- data/manifests/"))
    ]
    assert len(regimenes) == 2
    reglas = [
        "### Change Regimes (must be respected), lo que CLAUDE.md no dice\n"
        + "\n".join(literal(original, e) for e in regimenes)
        + "\n"
    ]
    for titulo in (
        "Things That Must Not Be Changed",
        "Decisions and Rationale",
        "Known Issues",
    ):
        reglas.append(f"### {titulo}\n" + literal(original, sec[titulo].strip()) + "\n")

    partes = [
        PREAMBULO,
        "## Current Branch\ntrabajo/dieta-y-skills\n",
        f"## Current Feature\n{CURRENT_FEATURE}\n",
        f"## Stable Main State\n{estable}\n",
        f"## Last Stable Commit\n{ultimo}\n",
        "## Tests Currently Passing\n" + TESTS.format(n=args.tests) + "\n",
        f"## Next Action\n\n{vigente}\n\n{LINEA_J}\n\n{pendientes_de_hechas}\n\n{puntero_na}\n",
        f"## Known Ambiguities\n{MARCO_AMBIGUEDADES}\n{tabla}\n\n{MARCO_CANDIDATAS}\n{candidatas}\n",
        "## Technical Debt\n" + MARCO_DEUDA + "\n" + "\n".join(deuda) + "\n",
        "## Reglas vivas\n" + MARCO_REGLAS + "\n" + "\n".join(reglas),
        f"## Completed Features\n{MARCO_COMPLETED}",
        f"## Change Log\n{MARCO_CHANGELOG}",
    ]
    estado = "\n".join(partes)
    (s / "PROJECT_STATE.md").write_text(estado, encoding="utf-8", newline="\n")
    historia = CABECERA_HISTORIA + original
    assert historia.endswith(original)
    (s / "HISTORIA.md").write_text(historia, encoding="utf-8", newline="\n")
    print(f"PROJECT_STATE.md: {len(estado.encode('utf-8'))} bytes")
    print(f"HISTORIA.md: {len(historia.encode('utf-8'))} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
