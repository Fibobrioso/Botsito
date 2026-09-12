"""Cada `registro.<accesor>("nombre")` en src/ cita un parametro existente con ese tipo
(ADR-0006): un typo o un tipo cambiado se detecta aqui, no en produccion."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from botsito.config.registro import cargar_registro

ACCESORES = {
    "fraccion": "fraccion",
    "porcentaje": "porcentaje",
    "decimal": "decimal",
    "entero": "entero",
    "hora": "hora",
    "texto": "texto",
    # F11
    "opcion": "enum",
    "booleano": "booleano",
    "puntos": "puntos",
    "minutos": "minutos",
    "lotes": "lotes",
}


def _usos(repo: Path) -> list[tuple[str, str, str]]:
    usos: list[tuple[str, str, str]] = []
    for py in sorted((repo / "src" / "botsito").rglob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in ACCESORES
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in {"registro", "reg", "parametros"}
            ):
                usos.append((f"{py.name}:{node.lineno}", node.func.attr, node.args[0].value))
    return usos


@pytest.mark.contract
def test_accesores_del_registro_citan_parametros_existentes_con_su_tipo(repo: Path) -> None:
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    problemas: list[str] = []
    for donde, accesor, nombre in _usos(repo):
        p = registro.parametros.get(nombre)
        if p is None:
            problemas.append(f"{donde}: parametro {nombre!r} no existe en el registro")
        elif p.tipo != ACCESORES[accesor]:
            problemas.append(f"{donde}: {nombre} es {p.tipo}, se lee con .{accesor}()")
    assert problemas == [], problemas


def test_el_detector_ve_los_usos(tmp_path: Path) -> None:
    (tmp_path / "src" / "botsito").mkdir(parents=True)
    (tmp_path / "src" / "botsito" / "m.py").write_text(
        'x = registro.fraccion("stop_fraccion")\ny = reg.hora("inicio")\n', encoding="utf-8"
    )
    assert _usos(tmp_path) == [
        ("m.py:1", "fraccion", "stop_fraccion"),
        ("m.py:2", "hora", "inicio"),
    ]


# Renombres de opcion posteriores a una sesion ya celebrada. La clave es (parametro, opcion tal
# como se le pregunto al trader) y el valor dice en que se convirtio y quien lo decidio. Van
# nombradas y razonadas, como las exenciones de `paquete.py:574`: una lista vacia seria mas
# comoda y no distinguiria un renombre acordado de una opcion que se perdio por el camino.
RENOMBRADAS = {
    ("lotaje_base", "desde_075"): "hasta_stop_fraccion (ADR-0020, 2026-09-11)",
}


@pytest.mark.contract
def test_lo_que_se_le_pregunto_al_trader_sigue_teniendo_objeto_en_el_registro(repo: Path) -> None:
    """Cada opcion cerrada del cuestionario COMMITEADO existe hoy en el registro, o esta declarada
    como renombre.

    Sustituye (F13) a la guardia que cruzaba las `opciones` del mapa con las del registro. Aquella
    vigilaba que dos copias no se separaran; al unificarlas -las opciones las da ahora el registro-
    se quedo sin las dos copias, pero lo que protegia sigue importando y no era la copia: era que
    el paquete de una sesion celebrada es la PRUEBA de lo que se le pregunto al trader, y una
    respuesta suya solo se puede aplicar si el registro todavia admite la opcion que eligio.

    Es mas ancha que la que sustituye: mira el paquete real y no el fichero del que salio, asi que
    tambien cubre las sesiones futuras sin tocar nada. En su primera ejecucion encontro el
    renombre de `desde_075`, que la anterior no podia ver.
    """
    import yaml

    from botsito.cases.paquete import DIRECTORIO_KIT, sesiones_del_kit

    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    problemas: list[str] = []
    sesiones = sesiones_del_kit(repo)
    assert sesiones, "no hay ningun paquete commiteado: la guardia no vigilaria nada"
    for sesion in sesiones:
        ruta = repo / DIRECTORIO_KIT / sesion / "cuestionario.yaml"
        doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
        for q in doc["preguntas"]:
            esperada = q["respuesta_esperada"]
            nombres = esperada.get("parametros") or []
            # Las opciones de una pregunta de contradiccion son VALORES vistos en el corpus, no
            # un enum: no tienen por que estar en el registro y no se miran aqui.
            if not esperada.get("opciones") or not nombres:
                continue
            admitidas: set[str] = set()
            for n in nombres:
                p = registro.parametros.get(n)
                if p is None:
                    problemas.append(f"{sesion}/{q['id']}: {n} ya no esta en el registro")
                    continue
                admitidas |= set(p.opciones or ())
            for o in esperada["opciones"]:
                if o in admitidas or (len(nombres) == 1 and (nombres[0], o) in RENOMBRADAS):
                    continue
                problemas.append(
                    f"{sesion}/{q['id']}: se pregunto por {o!r} de {nombres} y el registro "
                    f"admite {sorted(admitidas)}"
                )
    assert not problemas, "; ".join(problemas)


@pytest.mark.contract
def test_la_guardia_de_las_opciones_ve_un_renombre_no_declarado(repo: Path) -> None:
    """Si no cazara una opcion desaparecida, no vigilaria nada. Se comprueba sobre el renombre
    real: `desde_075` sigue en el cuestionario commiteado, ya no esta en el registro, y lo unico
    que impide que salte es su entrada en RENOMBRADAS."""
    import yaml

    from botsito.cases.paquete import DIRECTORIO_KIT

    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    assert "desde_075" not in (registro.parametros["lotaje_base"].opciones or ())
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "cuestionario.yaml").read_text(
            encoding="utf-8"
        )
    )
    preguntadas = {
        o
        for q in doc["preguntas"]
        if (q["respuesta_esperada"].get("parametros") or []) == ["lotaje_base"]
        for o in q["respuesta_esperada"]["opciones"]
    }
    assert "desde_075" in preguntadas
    assert ("lotaje_base", "desde_075") in RENOMBRADAS


def test_el_readme_de_la_spec_no_puede_llevar_cifras_viejas(repo: Path) -> None:
    """Las cifras de la spec se quedaron viejas TRES veces en dos dias.

    P8 las encontro desfasadas tres versiones, P11 vio que dejaron de cuadrar al aparecer el
    primer `DEFAULT_AMBIGUOUS`, y la tercera copia nacio desfasada porque `spec_version` subio dos
    veces mas antes del merge. La leccion no es "revisar mejor": una foto de un estado que cambia
    en cada commit no se pega a mano.

    De los documentos que las llevaban, solo UNO describe el presente sin mezcla: este README, que
    dice que contiene `knowledge/spec/` AHORA. El HANDOFF es una narracion con fechas -su seccion
    de F10 dice "registro con 24 parametros de estrategia en UNKNOWN", que era cierto entonces- asi
    que ahi la cifra se quito y se apunta al comando; los informes de validacion y los ADR son
    artefactos fechados y no se tocan.

    La guardia es pequena a proposito. Una que cazara tambien la narracion historica daria falsos
    positivos, y una guardia con falsos positivos se desactiva sola.
    """
    import re

    ruta = repo / "knowledge" / "spec" / "README.md"
    texto = ruta.read_text(encoding="utf-8")

    # LA GUARDIA SE INVIRTIO EN F13, y es mejor guardia. Antes exigia que el recuento pegado a
    # mano cuadrara con el registro; ahora exige que NO HAYA recuento que cuadrar. El numero vive
    # en `docs/spec/parametros.md`, que se GENERA desde el registro y que `test_spec_docs_generados`
    # compara entero: una copia que no existe no se puede quedar vieja.
    sospechosas = re.findall(r"\d+ parametros|\d+ confirmados|A-1\.\.A-\d+", texto)
    assert not sospechosas, (
        f"el README de la spec volvio a pegar cifras vivas ({sospechosas}); el recuento lo dan "
        f"`botsito spec status` y `docs/spec/parametros.md`, que se genera"
    )
    assert "spec status" in texto, "tiene que apuntar al comando que da el recuento vivo"


def test_el_handoff_no_pega_un_recuento_que_caduca(repo: Path) -> None:
    """El HANDOFF llevaba la copia que se quedo vieja tres veces; ahora apunta al comando."""
    texto = (repo / "docs" / "HANDOFF.md").read_text(encoding="utf-8")
    assert "`botsito spec status`" in texto
    import re as _re

    pegados = _re.findall(r"manifiesto \d+\.\d+\.\d+", texto)
    assert not pegados, (
        f"el HANDOFF pega una version del manifiesto ({pegados}); esa foto caduca sola, "
        "y por eso se apunta al comando en vez de copiarla"
    )
