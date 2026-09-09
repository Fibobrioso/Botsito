"""La hoja de la sesion en Word se compone del paquete real y es un .docx que Word abre.

Es el artefacto que se lleva a la sesion con el trader: si se rompe, se rompe delante de el y no
hay segunda oportunidad. Aqui se comprueba lo que se puede comprobar sin Word: que el generador
corre sobre el paquete real, que el zip y el XML son validos, que el orden de los hijos que el
esquema WordprocessingML exige se respeta, que ninguna pregunta se queda sin caja de respuesta y
que no se escapa al papel nada de la particion oculta.
"""

from __future__ import annotations

import importlib.util
import re
import sys
import xml.dom.minidom
import zipfile
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.paquete import DIRECTORIO_KIT, esquema_paquete, sesiones_del_kit
from botsito.comun.yaml_estricto import cargar_yaml

REPO = Path(__file__).resolve().parents[2]
GENERADOR = REPO / "scripts" / "hoja_sesion_docx.py"
# Orden de hijos que el esquema exige dentro de cada contenedor (ECMA-376, parte 1). Word abre
# igual documentos con otro orden, pero avisa de que hay que repararlos, y eso delante del
# trader parece que el trabajo esta mal hecho.
ORDEN = {
    "w:pPr": ["w:pStyle", "w:keepNext", "w:spacing", "w:ind", "w:outlineLvl"],
    "w:rPr": ["w:b", "w:i", "w:color", "w:sz", "w:szCs"],
    "w:tcPr": ["w:tcW", "w:shd", "w:vAlign"],
    "w:trPr": ["w:cantSplit", "w:tblHeader"],
    "w:tblPr": ["w:tblW", "w:tblBorders", "w:tblCellMar"],
}


def _generador() -> Any:
    spec = importlib.util.spec_from_file_location("hoja_sesion_docx", GENERADOR)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["hoja_sesion_docx"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="module")
def sesion() -> str:
    sesiones = sesiones_del_kit(REPO)
    if not sesiones:
        pytest.skip("no hay ningun paquete en knowledge/cases/kit/")
    return sesiones[-1]


@pytest.fixture(scope="module")
def xml_documento(sesion: str) -> str:
    return str(_generador().documento(REPO, sesion))


def test_el_xml_es_valido_y_sin_control(xml_documento: str) -> None:
    xml.dom.minidom.parseString(xml_documento.encode("utf-8"))
    sueltos = re.findall(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", xml_documento)
    assert sueltos == []
    assert [c for c in xml_documento if ord(c) < 0x20 and c not in "\t\n\r"] == []


def test_el_docx_es_un_zip_que_word_reconoce(xml_documento: str, tmp_path: Path) -> None:
    ruta = tmp_path / "hoja.docx"
    _generador().escribir_docx(ruta, xml_documento)
    with zipfile.ZipFile(ruta) as z:
        assert z.testzip() is None
        nombres = set(z.namelist())
        assert nombres == {
            "[Content_Types].xml",
            "_rels/.rels",
            "word/document.xml",
            "word/_rels/document.xml.rels",
            "word/styles.xml",
        }
        estilos = z.read("word/styles.xml").decode("utf-8")
        for parte in nombres:
            xml.dom.minidom.parseString(z.read(parte))
    usados = set(re.findall(r'<w:pStyle w:val="([^"]+)"/>', xml_documento))
    definidos = set(re.findall(r'w:styleId="([^"]+)"', estilos))
    assert usados <= definidos, f"estilos usados sin definir: {sorted(usados - definidos)}"


@pytest.mark.parametrize("contenedor", sorted(ORDEN))
def test_orden_de_hijos_segun_el_esquema(xml_documento: str, contenedor: str) -> None:
    esperado = ORDEN[contenedor]
    for bloque in re.findall(rf"<{contenedor}>(.*?)</{contenedor}>", xml_documento, re.S):
        hijos = re.findall(r"<(w:[a-zA-Z]+)[ />]", bloque)
        hijos = [h for h in hijos if h in esperado]
        posiciones = [esperado.index(h) for h in hijos]
        assert posiciones == sorted(posiciones), f"{contenedor}: {hijos}"
        assert len(set(hijos)) == len(hijos), f"{contenedor} repite un hijo: {hijos}"


def test_cada_tabla_va_seguida_de_un_parrafo(xml_documento: str) -> None:
    """Word repara el documento si una tabla toca otra o cierra el cuerpo."""
    assert "</w:tbl><w:tbl>" not in xml_documento
    assert "</w:tbl><w:sectPr>" not in xml_documento
    for tabla in re.findall(r"<w:tbl>.*?</w:tbl>", xml_documento, re.S):
        for celda in re.findall(r"<w:tc>.*?</w:tc>", tabla, re.S):
            assert "<w:p>" in celda, "una celda sin parrafo hace que Word repare el fichero"


def test_toda_pregunta_de_la_hoja_tiene_caja_de_respuesta(xml_documento: str, sesion: str) -> None:
    cuestionario, _, _ = esquema_paquete(REPO, sesion)
    ctx = cargar_yaml((REPO / DIRECTORIO_KIT / "contexto_preguntas.yaml").read_text("utf-8"))
    esperadas = (
        len(cuestionario["preguntas"]) + len(ctx.get("preguntas_extra") or []) + 1  # precondicion
    )
    assert xml_documento.count("Respuesta literal del trader:") == esperadas


def test_las_citas_son_las_del_cuestionario(xml_documento: str, sesion: str) -> None:
    """Ni una palabra puesta en boca del trader: el texto sale del paquete, no del generador."""
    cuestionario, _, _ = esquema_paquete(REPO, sesion)
    plano = re.sub(r"<[^>]+>", " ", xml_documento)
    plano = " ".join(plano.replace("&amp;", "&").replace("&quot;", '"').split())
    for pregunta in cuestionario["preguntas"]:
        for caso in pregunta["casos"]:
            cita = " ".join(str(caso["cita"]).split())
            if len(cita) <= 400:  # las largas se truncan; ver LIMITE_CITA
                assert cita in plano, f"{pregunta['id']}: la cita no aparece intacta"


def test_la_hoja_no_filtra_la_particion_oculta(xml_documento: str, sesion: str) -> None:
    """Si el trader ve los dias de holdout, la medida de fidelidad de F26 deja de valer."""
    _, ventanas, particiones = esquema_paquete(REPO, sesion)
    plano = re.sub(r"<[^>]+>", " ", xml_documento)
    ocultos = [c for c in ventanas["casos"] if particiones["asignacion"].get(c["id"]) != "dev"]
    assert ocultos, "el paquete no tiene holdout: revisa los cupos"
    for caso in ocultos:
        assert str(caso["dia"]) not in plano, f"{caso['id']} es holdout y sale en la hoja"
    for prohibido in ("holdout", "sha256", "dataset_id", "seed"):
        assert prohibido not in plano.lower()


def test_el_generador_avisa_en_vez_de_reventar(tmp_path: Path, sesion: str) -> None:
    generador = _generador()
    with pytest.raises(SystemExit, match="carpeta"):
        generador.escribir_docx(tmp_path, "<w:document/>")
    with pytest.raises(SystemExit, match="no existe la carpeta"):
        generador.escribir_docx(tmp_path / "no" / "existe" / "x.docx", "<w:document/>")
    with pytest.raises(SystemExit, match="ninguna pregunta del paquete nace"):
        generador.numero_de_pregunta([], "A-999")


def test_toda_pregunta_declarada_tiene_objetivo_registrable(sesion: str) -> None:
    """La guardia que impide volver a escribir una pregunta cuya respuesta no se puede registrar."""
    generador = _generador()
    ctx = cargar_yaml((REPO / DIRECTORIO_KIT / "contexto_preguntas.yaml").read_text("utf-8"))
    generador.comprobar_objetivos(ctx, sesion, REPO)
    roto = {**ctx, "precondicion": {**ctx["precondicion"], "objetivo": "parametro no_existe"}}
    with pytest.raises(SystemExit, match="no esta en el registro"):
        generador.comprobar_objetivos(roto, sesion, REPO)
