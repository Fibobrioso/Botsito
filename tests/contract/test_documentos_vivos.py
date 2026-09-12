"""Un documento que describe el PRESENTE no pega un recuento que el CLI ya da (F13, mitad B).

El brief de F13 tenia dos mitades y el orden importaba: (A) que el documento generado SUSTITUYA a
lo que se mantiene a mano, y (B) extender la guardia anti-copia a los documentos que SI llevan
cifras vivas, *"que es lo que habria cazado las seis"*. La mitad A se entrego primero; esto es la
B, y nace porque la auditoria de cierre demostro que hacia falta: en el mismo barrido aparecieron
siete cifras y afirmaciones vivas desfasadas mas, dos de ellas de negocio.

Lo que esta guardia cubre y lo que NO, dicho aqui para que nadie la crea mas ancha de lo que es:

- **Cubre** un numero pegado junto a una palabra del dominio -"27 reglas", "59 parametros", "21
  preguntas", "116 registros de feedback"- en los documentos que describen el presente. Es la
  forma exacta que tenian cuatro de los hallazgos de la auditoria.
- **No cubre** una afirmacion de negocio en prosa ("se opera con noticias", "el lotaje va sobre la
  caja completa"). Se intento y se descarto midiendo: los mismos patrones casan con la narracion
  historica legitima -un item de evidencia que DICE eso, el riesgo que una tabla del plan
  enumera- y una guardia con falsos positivos se desactiva sola. Eso lo sigue cazando una
  auditoria con ojos, y por eso se sigue haciendo una por rama.

Las exenciones van NOMBRADAS, y el test comprueba que cada seccion exenta EXISTE: si alguien la
renombra, esto falla en vez de ensancharse en silencio.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

# Un numero pegado a una palabra que el CLI sabe contar. `\b` delante para no casar con la cola de
# otro numero, y las dos grafias (con y sin tilde) porque el repositorio mezcla las dos.
RECUENTO = re.compile(
    r"\b\d{1,4}\s+(?:par[aá]metros?|reglas?|ambig[uü]edades|preguntas|"
    r"registros?\s+de\s+feedback|items?\s+de\s+evidencia|t[eé]rminos?)\b",
    re.IGNORECASE,
)

# Una linea suelta puede eximirse, con MOTIVO obligatorio, igual que el contrato de literales de
# negocio admite `# no-negocio: <motivo>`. Es para el hecho congelado dentro de una seccion viva:
# "las 3 preguntas bloqueantes de la sesion 1" no va a cambiar nunca, porque esa sesion ya se
# celebro y su paquete esta commiteado.
EXENCION = re.compile(r"<!--\s*cifra-congelada:\s*(?!-->)\S")

# Documentos que describen el PRESENTE, enteros.
VIVOS = (
    "docs/spec/README.md",
    "docs/validation/README.md",
    "knowledge/spec/README.md",
    "knowledge/evidence/README.md",
    "knowledge/feedback/README.md",
    "knowledge/cases/kit/README.md",
)

# PROJECT_STATE es mitad presente y mitad archivo. Estas secciones son archivo -o las vigila otra
# guardia- y quedan fuera, cada una con su motivo:
SECCIONES_EXENTAS = {
    "## Completed Phases": "lo que se cerro entonces, con las cifras de entonces",
    "## Completed Features": "idem, una linea por rama cerrada",
    "## Stable Main State": "describe `main`, no la rama: sus cifras son las del ultimo tag",
    "## Tests Currently Passing": "la vigila `state check`, que la compara con pytest",
    "## Lineamientos recibidos del usuario y hechos del corpus (evidencia en F07)": (
        "hechos fechados del corpus, con el id de evidencia que los sostiene"
    ),
    "## Technical Debt": "describe deudas con las cifras del dia en que se anotaron",
    "## Expert Validations": "actas de validacion, fechadas",
    "## Change Log": "el archivo por excelencia: cada entrada dice lo que era cierto ese dia",
}


def _cuerpo_vivo(texto: str) -> str:
    """PROJECT_STATE sin las secciones exentas."""
    trozos: list[str] = []
    seccion = ""
    for linea in texto.splitlines():
        if linea.startswith("## "):
            seccion = linea.strip()
        if seccion not in SECCIONES_EXENTAS:
            trozos.append(linea)
    return "\n".join(trozos)


@pytest.mark.contract
def test_las_secciones_exentas_de_project_state_existen(repo: Path) -> None:
    """Una exencion sobre una seccion que ya no existe no exime nada y engorda la lista."""
    texto = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    faltan = [s for s in SECCIONES_EXENTAS if s not in texto]
    assert not faltan, f"secciones exentas que ya no estan en PROJECT_STATE: {faltan}"


@pytest.mark.contract
def test_project_state_no_pega_recuentos_en_lo_que_describe_el_presente(repo: Path) -> None:
    texto = (repo / "PROJECT_STATE.md").read_text(encoding="utf-8")
    pegados = []
    for n, linea in enumerate(_cuerpo_vivo(texto).splitlines(), 1):
        if EXENCION.search(linea):
            continue
        pegados += [f"{m.group(0)!r} (linea {n})" for m in RECUENTO.finditer(linea)]
    assert not pegados, (
        f"PROJECT_STATE pega recuentos que caducan solos: {pegados}. Los dan `botsito spec status`,"
        f" `botsito knowledge validate` y `docs/spec/`, que se genera. Si la linea es historica, "
        f"va en una seccion exenta y se declara en SECCIONES_EXENTAS con su motivo."
    )


@pytest.mark.contract
@pytest.mark.parametrize("nombre", VIVOS)
def test_los_readme_vivos_no_pegan_recuentos(repo: Path, nombre: str) -> None:
    texto = (repo / nombre).read_text(encoding="utf-8")
    pegados = [m.group(0) for m in RECUENTO.finditer(texto)]
    assert not pegados, (
        f"{nombre} pega recuentos que caducan solos: {pegados}; apunta al comando que los da"
    )


@pytest.mark.contract
def test_la_guardia_no_es_decorativa(repo: Path) -> None:
    """Con la spec real delante: si volviera el recuento que F13 mato, esto tiene que saltar."""
    del repo
    assert RECUENTO.findall("Desde la sesion 1 tiene 59 parametros: 50 confirmados")
    assert RECUENTO.findall("strategy_spec.yaml (27 reglas)")
    assert RECUENTO.findall("cuestionario de 21 preguntas con casos")
    assert RECUENTO.findall("fuente de 116 registros de feedback")
    # y no salta con lo que no es un recuento
    assert not RECUENTO.findall("ADR-0020 subio el lote un 25 %")
    assert not RECUENTO.findall("`botsito spec status` da el recuento vivo")
    # la exencion por linea exige motivo: el marcador pelado no exime
    assert EXENCION.search(
        "3 preguntas bloqueantes <!-- cifra-congelada: la sesion 1 ya se celebro -->"
    )
    assert not EXENCION.search("3 preguntas bloqueantes <!-- cifra-congelada: -->")
