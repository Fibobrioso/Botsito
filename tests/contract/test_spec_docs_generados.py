"""`docs/spec/` sale de `knowledge/spec/` y no de la mano de nadie (F13).

Copiar a mano una cifra de la spec a un documento ha fallado seis veces en tres dias, todas
documentadas. La leccion estaba escrita -"el recuento vivo lo da `botsito spec status` y NO se
copia aqui"- pero es disciplina, y la disciplina se olvida. Esto es el mecanismo.

Compara el TEXTO ENTERO y no un hash, a proposito: el hash de la spec cubre tres ficheros y no
`ambiguedades.yaml`, asi que sellar con el mentiria sobre uno de los cuatro documentos. Es el
patron que `kit check` ya sostuvo en produccion.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.cases.spec_docs import DIRECTORIO, FICHEROS, comprobar, generar


def _sin_holdout(directorio: str, nombres: list[str]) -> set[str]:
    """`ignore` de `copytree`: nada de `holdout/{1,2,3}` salvo su README (copiar es leer)."""
    partes = Path(directorio).parts
    if len(partes) >= 2 and partes[-2] == "holdout" and partes[-1] in {"1", "2", "3"}:
        return {n for n in nombres if n != "README.md"}
    return set()


REPO = Path(__file__).resolve().parents[2]


def test_lo_commiteado_es_lo_que_sale_de_la_fuente() -> None:
    problemas = comprobar(REPO)
    assert not problemas, "; ".join(problemas)


def test_estan_los_cuatro_y_dicen_que_son_generados() -> None:
    for nombre in FICHEROS:
        ruta = REPO / DIRECTORIO / nombre
        assert ruta.is_file(), f"falta {nombre}"
        primera = ruta.read_text(encoding="utf-8").splitlines()[0]
        assert "GENERADO" in primera and "No editar a mano" in primera, nombre


def test_la_guardia_no_es_decorativa(tmp_path: Path) -> None:
    """Si cambiar la fuente no cambiara el documento, esto no vigilaria nada.

    Es el mismo criterio con el que F12 escribio las suyas: una guardia que pasa igual con la
    spec rota no es una guardia.
    """
    generado = generar(REPO)
    assert any("stop_fraccion_caja" in texto for texto in generado.values())

    # Un documento editado a mano se denuncia, y el mensaje dice cual
    copia = tmp_path / DIRECTORIO
    copia.mkdir(parents=True)
    for nombre, texto in generado.items():
        (copia / nombre).write_text(texto, encoding="utf-8", newline="\n")
    for enlace in ("knowledge", "docs"):
        del enlace  # el repo de trabajo es REPO; aqui solo se comprueba el mensaje

    (copia / "reglas.md").write_text("editado a mano\n", encoding="utf-8", newline="\n")
    import shutil

    falso = tmp_path / "repo"
    shutil.copytree(REPO / "knowledge", falso / "knowledge", ignore=_sin_holdout)
    shutil.copytree(copia, falso / DIRECTORIO)
    problemas = comprobar(falso)
    assert any("reglas.md" in p for p in problemas), problemas
    assert not any("parametros.md" in p for p in problemas), "los otros tres seguian cuadrando"


def test_la_forma_ejecutable_se_imprime_verbatim_y_no_parafraseada() -> None:
    """Parafrasear un arbol con `ninguno_de` y ligadura perderia lo que F12 construyo."""
    reglas = (REPO / DIRECTORIO / "reglas.md").read_text(encoding="utf-8")
    assert "```json" in reglas
    assert '"ninguno_de"' in reglas or '"cualquiera_de"' in reglas
    # y las citas del vocabulario, que durante toda F12 nadie comprobaba, se ven
    assert "### predicados" in reglas and "Cita `" in reglas


@pytest.mark.parametrize("nombre", FICHEROS)
def test_ningun_documento_generado_se_edita_a_mano_sin_que_salte(nombre: str) -> None:
    texto = (REPO / DIRECTORIO / nombre).read_text(encoding="utf-8")
    assert texto.endswith("\n") and "\r" not in texto, f"{nombre}: LF y salto final"
