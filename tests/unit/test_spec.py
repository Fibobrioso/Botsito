"""StrategySpec, glosario y manifiesto (F11, ADR-0013)."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito.spec.manifiesto import (
    ManifiestoSpecError,
    cargar_manifiesto,
    estructura_para_hash,
    hash_de,
)
from botsito.spec.modelo import SpecError, cargar_glosario, cargar_reglas, comprobar_contra

REPO = Path(__file__).resolve().parents[2]
FB = "fb-2026-09-09-sesion-01-846fb0d7"


def _regla(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "id": "RN-001",
        "titulo": "una regla",
        "cuando": "el precio alcanza la liquidez de M15",
        "entonces": "se opera segun stop_fraccion_caja",
        "parametros": ["stop_fraccion_caja"],
        "cita": FB,
        "literal": "lo dijo asi",
        "clase": "disparador",
        "estado": "VIGENTE",
    }
    d.update(cambios)
    return d


def _escribir(tmp_path: Path, reglas: list[dict[str, Any]]) -> Path:
    ruta = tmp_path / "strategy_spec.yaml"
    ruta.write_text(
        yaml.safe_dump({"version_esquema": 3, "reglas": reglas}, allow_unicode=True),
        encoding="utf-8",
        newline="\n",
    )
    return ruta


def test_una_regla_no_puede_llevar_un_valor_de_negocio(tmp_path: Path) -> None:
    """El valor vive en el registro: aqui solo va el nombre del parametro."""
    with pytest.raises(SpecError, match="contiene la cifra"):
        cargar_reglas(_escribir(tmp_path, [_regla(entonces="el stop va al 0,8 de la caja")]))
    with pytest.raises(SpecError, match="contiene la cifra"):
        cargar_reglas(_escribir(tmp_path, [_regla(cuando="son las 15:00")]))


def test_los_nombres_con_digitos_si_pasan(tmp_path: Path) -> None:
    """`M15`, `H4` y `liquidez_m15_criterio_toma` son nombres, no valores."""
    reglas = cargar_reglas(
        _escribir(
            tmp_path,
            [
                _regla(
                    cuando="el precio toma la liquidez de M15 dentro de la vela H4",
                    entonces="se aplica liquidez_m15_criterio_toma",
                )
            ],
        )
    )
    assert len(reglas) == 1


def test_el_literal_si_puede_llevar_cifras(tmp_path: Path) -> None:
    """Son las palabras del trader; prohibirselas seria censurar la cita."""
    reglas = cargar_reglas(_escribir(tmp_path, [_regla(literal="se reduce al 0.80")]))
    assert reglas[0].literal == "se reduce al 0.80"


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"id": "R-1"}, "formato RN-NNN"),
        ({"estado": "PROVISIONAL"}, "estado"),
        ({"cita": "no-es-un-id"}, "no es un id"),
        ({"parametros": "stop_fraccion_caja"}, "lista de nombres"),
        ({"titulo": "  "}, "falta 'titulo'"),
    ],
)
def test_esquema_estricto(tmp_path: Path, cambio: dict[str, Any], mensaje: str) -> None:
    with pytest.raises(SpecError, match=mensaje):
        cargar_reglas(_escribir(tmp_path, [_regla(**cambio)]))


def test_ids_repetidos(tmp_path: Path) -> None:
    with pytest.raises(SpecError, match="id repetido"):
        cargar_reglas(_escribir(tmp_path, [_regla(), _regla()]))


def test_campos_desconocidos(tmp_path: Path) -> None:
    with pytest.raises(SpecError, match="campos desconocidos"):
        cargar_reglas(_escribir(tmp_path, [{**_regla(), "prioridad": 3}]))


def test_comprobar_contra_el_registro_y_las_citas(tmp_path: Path) -> None:
    reglas = cargar_reglas(_escribir(tmp_path, [_regla()]))
    assert comprobar_contra(reglas, [], {"stop_fraccion_caja"}, {FB}) == []
    problemas = comprobar_contra(reglas, [], set(), set())
    assert any("no esta en el registro" in p for p in problemas)
    assert any("no existe" in p for p in problemas)


# --- la spec real ---


def test_la_spec_real_carga_y_cita_lo_que_existe() -> None:
    from botsito.config.registro import cargar_registro
    from botsito.evidence.modelo import cargar_evidencia
    from botsito.feedback.modelo import cargar_feedback
    from botsito.spec.modelo import FICHERO_GLOSARIO, FICHERO_SPEC

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    terminos = cargar_glosario(REPO / FICHERO_GLOSARIO)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    citas = {i.id for i in cargar_evidencia(REPO / "knowledge" / "evidence")} | {
        r.id for r in cargar_feedback(REPO / "knowledge" / "feedback")
    }
    assert comprobar_contra(reglas, terminos, set(registro.nombres()), citas) == []
    assert any(r.vigente for r in reglas) and any(not r.vigente for r in reglas)


def test_toda_regla_vigente_usa_parametros_con_valor() -> None:
    """Una regla vigente que nombra un UNKNOWN no se podria ejecutar."""
    from botsito.config.registro import Estado, cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC

    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    for r in cargar_reglas(REPO / FICHERO_SPEC):
        if not r.vigente:
            continue
        for nombre in r.parametros:
            p = registro.parametros[nombre]
            assert p.estado is not Estado.UNKNOWN, f"{r.id} usa {nombre}, que sigue UNKNOWN"


# --- manifiesto ---


def _copia_de_la_spec(tmp_path: Path) -> Path:
    (tmp_path / "knowledge" / "spec").mkdir(parents=True)
    for nombre in ("parametros.yaml", "strategy_spec.yaml", "glossary.yaml"):
        origen = REPO / "knowledge" / "spec" / nombre
        (tmp_path / "knowledge" / "spec" / nombre).write_text(
            origen.read_text(encoding="utf-8"), encoding="utf-8", newline="\n"
        )
    return tmp_path


def test_el_hash_es_reproducible() -> None:
    assert hash_de(REPO) == hash_de(REPO)
    estructura = estructura_para_hash(REPO)
    assert {p["nombre"] for p in estructura["parametros"]}
    assert all(isinstance(p.get("estado"), str) for p in estructura["parametros"])


def test_el_hash_cubre_el_registro_no_solo_las_reglas(tmp_path: Path) -> None:
    """Si el registro quedara fuera, cambiar el stop no cambiaria la version de la spec y el
    pre-vuelo de la demo daria verde con otra estrategia (MASTER_PLAN H.2)."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "parametros.yaml"
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace('valor: "0.8"', 'valor: "0.75"', 1),
        encoding="utf-8",
        newline="\n",
    )
    assert hash_de(repo) != antes


def test_el_hash_cubre_el_estado_y_la_fuente(tmp_path: Path) -> None:
    """Pasar de CONFIRMED a DEFAULT_AMBIGUOUS no cambia el valor, pero si lo que la spec afirma."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "parametros.yaml"
    # Linea a linea y no con `replace`: las primeras coincidencias de "estado: CONFIRMED" estan
    # dentro del ejemplo COMENTADO de la cabecera, y el hash ignora los comentarios a proposito.
    # Un replace ciego cambiaria el comentario y el test afirmaria lo contrario de lo que cree.
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    for i, linea in enumerate(lineas):
        if linea == "    estado: CONFIRMED":
            lineas[i] = "    estado: DEFAULT_AMBIGUOUS"
            break
    else:  # pragma: no cover
        pytest.fail("el registro real no tiene ningun parametro CONFIRMED")
    ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
    assert hash_de(repo) != antes


def test_un_comentario_no_cambia_el_hash(tmp_path: Path) -> None:
    """Se hashea la estructura, no los bytes: reordenar un comentario no es cambiar la spec."""
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    ruta.write_text(
        "# comentario nuevo\n" + ruta.read_text(encoding="utf-8"),
        encoding="utf-8",
        newline="\n",
    )
    assert hash_de(repo) == antes


def test_el_manifiesto_real_esta_al_dia() -> None:
    from botsito.spec.manifiesto import FICHERO_MANIFIESTO
    from botsito.spec.manifiesto import comprobar as comprobar_manifiesto

    assert comprobar_manifiesto(REPO, REPO / FICHERO_MANIFIESTO) == []
    doc = cargar_manifiesto(REPO / FICHERO_MANIFIESTO)
    assert len(doc["cubre"]) == 3
    # la version sube con cada cambio de la spec: se comprueba el formato, no el numero
    assert re.fullmatch(r"\d+\.\d+\.\d+", str(doc["spec_version"]))


def test_manifiesto_mal_escrito(tmp_path: Path) -> None:
    ruta = tmp_path / "spec_manifest.yaml"
    ruta.write_text(
        'spec_version: "1"\nhash: abc\ngenerado_el: "x"\ncubre: [a, b, c]\n',
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ManifiestoSpecError, match="semver"):
        cargar_manifiesto(ruta)


# --- una regla no puede decir algo distinto de lo que cita ---


def test_el_literal_de_una_regla_debe_estar_en_lo_que_cita(tmp_path: Path) -> None:
    """La guardia que faltaba: sin ella una regla puede poner palabras en boca del trader."""
    from botsito.spec.modelo import comprobar_literales

    reglas = cargar_reglas(_escribir(tmp_path, [_regla(literal="se reduce al 0.80")]))
    assert comprobar_literales(reglas, {FB: "por temas de spread se reduce al 0.80"}) == []
    problemas = comprobar_literales(reglas, {FB: "el stop se queda en 0.75"})
    assert len(problemas) == 1 and "no aparece en" in problemas[0]


def test_el_literal_admite_el_comodin_como_la_evidencia(tmp_path: Path) -> None:
    from botsito.spec.modelo import comprobar_literales

    reglas = cargar_reglas(
        _escribir(tmp_path, [_regla(literal="apenas se abre [...] se mueve el stop")])
    )
    citado = "la operativa se calcula normal, apenas se abre la operacion se mueve el stop a 0.8"
    assert comprobar_literales(reglas, {FB: citado}) == []


def test_la_spec_real_dice_lo_que_cita() -> None:
    from botsito.evidence.modelo import cargar_evidencia
    from botsito.feedback.modelo import cargar_feedback
    from botsito.spec.modelo import FICHERO_SPEC, comprobar_literales

    textos = {i.id: i.cita_literal for i in cargar_evidencia(REPO / "knowledge" / "evidence")}
    textos.update(
        {r.id: r.respuesta_literal for r in cargar_feedback(REPO / "knowledge" / "feedback")}
    )
    assert comprobar_literales(cargar_reglas(REPO / FICHERO_SPEC), textos) == []


# --- numeros escritos en letras ---


@pytest.mark.parametrize(
    ("texto", "salta"),
    [
        ("el stop va al ochenta por ciento de la caja", True),
        ("se permiten tres intentos por zona", True),
        ("el spread supera los veinte puntos", True),
        # Hasta ADR-0018 esto se daba por espanol corriente. NO lo era: "una operacion" y "los
        # dos esquemas" son cardinalidades de negocio, y por creerlas prosa vivieron fuera del
        # registro en RN-018 y RN-009. Ahora son operaciones_simultaneas_max y
        # zonas_control_max_por_esquema, y esta redaccion tiene que saltar.
        ("se abre una operacion por cualquiera de los dos esquemas", True),
        ("el precio toma la liquidez de M15 dentro de la vela H4", False),
        ("se opera segun stop_fraccion_caja", False),
    ],
)
def test_numeros_en_letras_solo_cuentan_con_unidad(tmp_path: Path, texto: str, salta: bool) -> None:
    if salta:
        with pytest.raises(SpecError, match="contiene"):
            cargar_reglas(_escribir(tmp_path, [_regla(entonces=texto)]))
    else:
        assert len(cargar_reglas(_escribir(tmp_path, [_regla(entonces=texto)]))) == 1


# --- la version de la spec no puede quedarse atras ---


def test_version_sin_subir_detecta_una_spec_cambiada(tmp_path: Path) -> None:
    """Regenerar el hash sin subir la version haria que dos specs distintas dijeran ser la misma."""
    from botsito.spec.manifiesto import version_sin_subir

    ruta = tmp_path / "spec_manifest.yaml"
    ruta.write_text(
        'spec_version: "1.0.1"\nhash: ' + "b" * 64 + '\ngenerado_el: "x"\ncubre: [a, b, c]\n',
        encoding="utf-8",
        newline="\n",
    )
    # Sin git no hay con que comparar, y eso no es un error: se dice que no se puede saber.
    assert version_sin_subir(tmp_path, ruta) is None


def test_el_hash_cubre_el_huso_de_las_horas(tmp_path: Path) -> None:
    """Cambiar el huso mueve la ventana operativa dos horas.

    Sin `huso` en el hash, `Europe/Madrid` -> `UTC` dejaba la spec diciendo ser la misma version
    con el mismo hash, mientras el bot operaria de 07:00 a 15:00 UTC en vez de las del trader.
    """
    repo = _copia_de_la_spec(tmp_path)
    antes = hash_de(repo)
    ruta = repo / "knowledge" / "spec" / "parametros.yaml"
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace("huso: Europe/Madrid", "huso: UTC"),
        encoding="utf-8",
        newline="\n",
    )
    assert hash_de(repo) != antes


def test_una_base_de_calculo_no_puede_vivir_en_la_prosa() -> None:
    """Un `base_calculo_*` existe para sacar la base de la frase y meterla en el registro.

    Sirve de poco si luego la regla que lo necesita no lo nombra: el motor lee `parametros`, no el
    espanol de `entonces`. Es el fallo que ADR-0014 corrigio -RN-015 decia "sobre la caja completa"
    mientras la `unidad` de `objetivo_rr` decia "multiplo del riesgo"-, y el mismo que ADR-0012 ya
    habia corregido dos veces con `base_calculo_riesgo` y `base_calculo_perdida_diaria`.
    """
    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC

    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    bases = {n for n in registro.nombres() if n.startswith("base_calculo_")}
    assert bases, "el registro deberia declarar sus bases de calculo como parametros"

    # 1. Toda base la usa alguna regla vigente. Una base que nadie nombra no fija nada.
    usadas = {p for r in reglas if r.vigente for p in r.parametros}
    assert not (bases - usadas), f"bases que ninguna regla vigente nombra: {sorted(bases - usadas)}"

    # 2. Y quien usa la magnitud, usa su base: si no, la base la vuelve a poner la prosa.
    magnitudes = {
        "objetivo_rr": "base_calculo_objetivo",
        "riesgo_por_operacion": "base_calculo_riesgo",
        "perdida_maxima_diaria": "base_calculo_perdida_diaria",
    }
    huerfanas = [
        f"{r.id}: nombra {magnitud} sin nombrar {base}"
        for r in reglas
        if r.vigente
        for magnitud, base in magnitudes.items()
        if magnitud in r.parametros and base not in r.parametros
    ]
    assert not huerfanas, "; ".join(huerfanas)


def test_una_regla_sobre_parametros_de_entorno_declara_su_adr() -> None:
    """Lo que `comprobar_literales` no puede ver: una regla que dice mas que su cita.

    No es mecanizable en general, pero si lo es la señal que lo acompaña: un parametro cuya
    `fuente` es `decision` no lo dijo el trader -es la ficha del simbolo, el reloj del broker, la
    cuenta-, asi que una regla construida sobre el decide por su cuenta y su cita no la sostiene.
    RN-026 (abstenerse por stops level) y RN-027 (redondear el lotaje a la baja) eran justo eso.
    """
    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, comprobar_decisiones

    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    fuentes = {n: p.fuente.tipo for n, p in registro.parametros.items() if p.fuente is not None}
    ids_adr = {
        f"ADR-{f.name[:4]}"
        for f in (REPO / "docs" / "adr").glob("[0-9][0-9][0-9][0-9]-*.md")
        if f.name[:4] != "0000"
    }
    assert comprobar_decisiones(reglas, fuentes, ids_adr) == []

    # y la guardia denuncia de verdad: se le quita el ADR a la regla que lo necesita
    sin_adr = [
        (r if r.decision is None else __import__("dataclasses").replace(r, decision=None))
        for r in reglas
    ]
    fallos = comprobar_decisiones(sin_adr, fuentes, ids_adr)
    assert any("RN-026" in f for f in fallos) and any("RN-027" in f for f in fallos)


def test_el_hash_cubre_el_texto_que_lee_una_persona() -> None:
    """`titulo`, `literal` y `notas` no los ejecuta el motor, pero son lo que la spec afirma.

    La correccion de riesgo mas cara de la fase -que el tope porcentual es el unico freno del dia
    que existe- vive en las `notas` de RN-020. Con `notas` fuera del hash se podia borrar sin que
    `spec_version` se moviera, y el `titulo` de esa misma regla decia lo contrario sin que nada lo
    viera.
    """
    from botsito.spec.manifiesto import estructura_para_hash

    estructura = estructura_para_hash(REPO)
    rn020 = next(r for r in estructura["reglas"] if r["id"] == "RN-020")
    for campo in ("titulo", "literal", "notas", "decision"):
        assert campo in rn020, f"el hash no cubre '{campo}' de las reglas"
    assert "unico freno del dia" in str(rn020["notas"])
    assert all("literal" in t for t in estructura["terminos"])


def test_la_precedencia_no_la_decide_el_orden_del_fichero() -> None:
    """Tres pares reales daban la respuesta equivocada con el orden del fichero (ADR-0018).

    RN-006 (id 006) ganaba a RN-014 y a RN-018: con una operacion abierta, el bot reubicaba una
    orden limite en paralelo en vez de poner el break even. RN-019 ganaba a RN-020: se reentraba
    tras tocar el tope diario. Y RN-022, que es la clausula `else`, estaba ANTES de RN-026 y
    RN-027, que son reglas reales.
    """
    from botsito.spec.modelo import CLASES_REGLA, FICHERO_SPEC, comprobar_precedencia

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    assert comprobar_precedencia(reglas) == []

    por_id = {r.id: r for r in reglas}
    # los frenos son gates y ganan a los disparadores
    # RN-001 y RN-016 entraron en la auditoria del arreglo: las dos frenan -"fuera de ese
    # intervalo no opera", "al llegar a cartuchos_max se deja de operar"- y estaban como
    # disparador, que es el mismo defecto que ADR-0018 arreglo para RN-019/RN-020.
    for rid in (
        "RN-001",
        "RN-005",
        "RN-008",
        "RN-009",
        "RN-016",
        "RN-018",
        "RN-020",
        "RN-026",
        "RN-027",
    ):
        assert por_id[rid].clase == "gate", rid
    assert CLASES_REGLA.index("terminal") < CLASES_REGLA.index("disparador"), (
        "cerrar la jornada tiene que ganar a mover un stop en ventana_fin"
    )
    assert por_id["RN-002"].clase == "terminal"
    assert por_id["RN-022"].clase == "fallback", "la clausula else no puede ser un disparador"
    assert sum(1 for r in reglas if r.vigente and r.clase == "fallback") == 1
    assert all(r.clase in CLASES_REGLA for r in reglas)

    # y la guardia denuncia de verdad: dos reglas de la misma clase con los mismos parametros
    import dataclasses

    gemela = dataclasses.replace(por_id["RN-006"], id="RN-999")
    fallos = comprobar_precedencia([*reglas, gemela])
    assert any("RN-006" in f and "RN-999" in f for f in fallos)


def test_las_cardinalidades_de_negocio_no_pueden_vivir_en_la_prosa(tmp_path: Path) -> None:
    """ "mas de una zona" y "una operacion abierta" eran dos numeros fuera del registro.

    La guardia de cifras estaba escrita para no verlos: su propio comentario declaraba que "se abre
    una operacion" y "los dos esquemas" eran espanol y no parametros. Eran RN-009 y RN-018, y son
    la razon de que las dos estuvieran sin ningun parametro (ADR-0018).
    """
    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import SpecError

    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    for nombre in ("operaciones_simultaneas_max", "zonas_control_max_por_esquema"):
        assert registro.entero(nombre) == 1, nombre

    for prosa, aguja in (
        ("se desarrolla mas de una zona de control", "una zona"),
        ("hay una operacion abierta", "una operacion"),
        ("no se da ninguno de los dos esquemas", "dos esquemas"),
    ):
        with pytest.raises(SpecError, match=aguja):
            cargar_reglas(_escribir(tmp_path, [_regla(cuando=prosa)]))


def test_el_piloto_de_la_forma_ejecutable_carga_y_se_valida() -> None:
    """Las cuatro reglas mas dificiles, en predicados con argumentos (ADR-0019).

    La forma decidida en D1 -predicado = nombre + booleano- aguantaba UNA de ocho. El piloto son
    RN-003 (sujeto, referencia y criterio distintos sobre la misma primitiva), RN-006 (ligadura:
    "la zona recien completada"), RN-014 (ligadura + cuantificador: "otra zona POSTERIOR a la
    entrada") y RN-020 (dos acumuladores con base y reinicio propios).
    """
    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    parametros = set(registro.nombres())

    con_forma = {r.id for r in reglas if r.forma is not None}
    # El piloto ya no es lo unico que tiene forma -las 24 vigentes la tienen- pero estas cuatro
    # siguen siendo las que la decidieron, y por eso se comprueban por su nombre.
    assert {"RN-003", "RN-006", "RN-014", "RN-020"} <= con_forma
    assert comprobar_forma(reglas, vocabulario, parametros) == []

    # y cada una conserva lo que la hacia dificil
    por_id = {r.id: r for r in reglas}
    assert "criterio" in str(por_id["RN-003"].forma), "RN-003: el criterio es un argumento"
    assert "liga" in str(por_id["RN-006"].forma), "RN-006: la zona se liga a una variable"
    assert "posterior_a" in str(por_id["RN-014"].forma), "RN-014: el cuantificador temporal"
    assert str(por_id["RN-020"].forma).count("alcanza_tope") == 2, "RN-020: dos acumuladores"


def test_la_forma_no_puede_esconder_un_valor_de_negocio() -> None:
    """El fallo que hundio la primera version de D1, ahora mecanizado.

    El ejemplo canonico del brief era `cierra_con_cuerpo_al_otro_lado`: el VALOR `cuerpo` horneado
    en el NOMBRE de un predicado cuyo parametro admite tambien `mecha`. Dos puertas para el mismo
    hecho (ADR-0002), y ninguna de las guardias heredadas lo veia.
    """
    import copy
    import dataclasses

    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())
    base = next(r for r in reglas if r.id == "RN-003")

    def falla(forma: dict[str, Any], aguja: str) -> None:
        rota = dataclasses.replace(base, forma=forma)
        assert any(aguja in p for p in comprobar_forma([rota], vocabulario, parametros)), aguja

    # el valor en vez del nombre del parametro
    falla(
        {"cuando": {"todos_de": [{"rompe": {"que": "x", "criterio": "mecha"}}]}},
        "lleva el NOMBRE, no el valor",
    )
    # un predicado que nadie declara
    falla(
        {"cuando": {"todos_de": [{"inventado": {"criterio": "sesgo_h4_criterio_ruptura"}}]}},
        "que no esta en `predicados`",
    )
    # un argumento que el predicado no admite
    falla({"cuando": {"todos_de": [{"rompe": {"inventado": True}}]}}, "que no declara")

    # y un acumulador cuya base no es un parametro del registro
    roto = copy.deepcopy(vocabulario)
    roto["acumuladores"]["perdida_dia"]["base"] = "saldo_inicial_dia"
    assert any("acumulador" in p for p in comprobar_forma([], roto, parametros))


def test_el_hash_cubre_la_forma_y_el_vocabulario() -> None:
    """`forma` es lo que el motor ejecuta: fuera del hash, cambiarla no moveria la version.

    Es el mismo fallo que P5 encontro con `notas`, esta vez en el campo mas ejecutable de todos.
    """
    from botsito.spec.manifiesto import estructura_para_hash

    estructura = estructura_para_hash(REPO)
    assert {"predicados", "acciones", "efectos", "hechos", "acumuladores"} <= set(estructura)
    rn003 = next(r for r in estructura["reglas"] if r["id"] == "RN-003")
    assert rn003.get("forma") is not None, "el hash no cubre la forma ejecutable"
    assert estructura["acumuladores"]["cartuchos"]["reinicia_con"] == "cartuchos_reinicio"


def test_toda_regla_vigente_tiene_forma_ejecutable() -> None:
    """La deuda del §8 de F11, cerrada: ninguna regla vigente se queda en prosa.

    El motor de F18-F23 lee `forma`, no el español de `cuando`. Una regla VIGENTE sin forma es una
    que el motor tendria que interpretar, que es exactamente lo que F12 existe para impedir.
    """
    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())

    sin_forma = [r.id for r in reglas if r.vigente and r.forma is None]
    assert sin_forma == [], f"reglas vigentes todavia en prosa: {sin_forma}"
    assert comprobar_forma(reglas, vocabulario, parametros) == []


def test_un_predicado_se_evalua_y_una_accion_se_ejecuta() -> None:
    """Dos vocabularios, no uno. Meterlos en el mismo saco era el hueco de ADR-0019.

    Lo encontro la propia guardia al escribir las veinte reglas restantes: `cerrar_a_mercado`,
    `dimensionar_lote` o `abstenerse` no son condiciones que se evaluen, son cosas que el motor
    hace, y no tenian donde declararse.
    """
    import dataclasses

    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())
    assert vocabulario["acciones"] and vocabulario["predicados"]
    assert not (set(vocabulario["acciones"]) & set(vocabulario["predicados"])), (
        "un nombre no puede ser a la vez predicado y accion"
    )

    base = next(r for r in reglas if r.id == "RN-013")
    # una accion en la rama de las condiciones
    cruzada = dataclasses.replace(
        base,
        forma={"cuando": {"todos_de": [{"abstenerse": {"segun": "comportamiento_sin_regla"}}]}},
    )
    fallos = comprobar_forma([cruzada], vocabulario, parametros)
    assert any("no esta en `predicados`" in f for f in fallos)


def test_los_dos_esquemas_de_entrada_estan_definidos(repo: Path) -> None:
    """Afirmar una ausencia exige buscarla en la FUENTE, no en el indice.

    El 2026-09-10 marque RN-008 como `pendiente_definicion` porque el glosario definia breaker de
    forma circular -"uno de los dos esquemas de entrada; sin el no hay entrada"- y su cita dice "el
    esquema de entrada que ya sabemos cual es". Era un error de busqueda: la definicion estaba en
    el corpus, repartida en una docena de items, y lo que faltaba era recogerla en el glosario.

    Este test fija las dos mitades: que la definicion esta, y que ninguna regla vigente se queda
    marcada como no ejecutable por una ausencia que no existe.
    """
    from botsito.spec.modelo import FICHERO_GLOSARIO, FICHERO_SPEC, cargar_glosario

    terminos = {t.termino: t for t in cargar_glosario(repo / FICHERO_GLOSARIO)}
    for nombre in ("breaker", "primer esquema de entrada", "segundo esquema de entrada"):
        assert nombre in terminos, nombre
    # y la definicion de breaker deja de nombrarse a si misma
    assert "esquema de entrada" not in terminos["breaker"].definicion
    assert "bloque de origen" in terminos["breaker"].definicion

    reglas = cargar_reglas(repo / FICHERO_SPEC)
    pendientes = [
        r.id
        for r in reglas
        if r.vigente and isinstance(r.forma, dict) and r.forma.get("pendiente_definicion")
    ]
    assert pendientes == [], f"reglas vigentes declaradas no ejecutables: {pendientes}"


def test_los_hechos_declarados_coinciden_con_lo_que_las_formas_hacen() -> None:
    """La guardia miraba la DECLARACION y no la realidad, y pasaban tres fallos caros.

    `operativa_detenida` declaraba `consume: [RN-001]` mientras RN-001 no lo leia: el tope diario
    del 4,5 %, el semanal y el corte por cartuchos prohibian abrir EN EL TICK DEL EVENTO y nada
    impedia abrir en el siguiente. En cuenta fondeada eso no cuesta un trade.

    `operacion_abierta` declaraba producirse en RN-011 -que solo coloca la orden- asi que NADIE lo
    producia, y RN-002 (cierre forzoso a las 15:00) y RN-014 (break even) eran INALCANZABLES.

    Y `operaciones_abiertas` se invocaba como acumulador sin estar declarado como tal.
    """
    import json

    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())
    assert comprobar_forma(reglas, vocabulario, parametros) == []

    # los dos frenos DURAN: quien los fija tambien los lee, o solo valdrian un instante
    for freno in ("detenido_por_tope", "detenido_por_cartuchos"):
        h = vocabulario["hechos"][freno]
        assert h["produce"], freno
        assert "RN-001" in h["consume"], f"{freno}: el gate maestro tiene que leerlo"
        assert set(h["produce"]) <= set(h["consume"]), (
            f"{freno}: quien lo fija tiene que seguir viendolo, o el freno dura un tick"
        )

    # y el cierre forzoso y el break even tienen de verdad quien les produzca la posicion
    por_id = {r.id: r for r in reglas}
    productor = next(
        r.id
        for r in reglas
        if isinstance(r.forma, dict)
        and "operacion_abierta" in json.dumps(r.forma.get("entonces", {}), ensure_ascii=False)
    )
    assert productor == "RN-013"
    for consumidor in ("RN-002", "RN-014"):
        forma = por_id[consumidor].forma
        assert isinstance(forma, dict)
        assert "operacion_abierta" in json.dumps(forma.get("cuando", {}), ensure_ascii=False), (
            consumidor
        )


def test_el_vocabulario_tampoco_puede_citar_un_registro_revocado() -> None:
    """La guardia de citas revocadas nacio corta TRES veces; esta es la tercera.

    Miraba `parametros.yaml` (P13), luego reglas y glosario (RN-013), y el vocabulario que estreno
    F12 seguia fuera aunque predicados y acciones llevan `cita` propia. Se vio en real el
    2026-09-11: el acuerdo del lotaje (ADR-0020) revoco el registro de la sesion 1 y
    `no_es_multiplo_de` se quedo citandolo sin que nada lo dijera.
    """
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_citas_revocadas

    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    citado = next(
        d["cita"]
        for d in vocabulario["predicados"].values()
        if isinstance(d, dict) and d.get("cita")
    )

    # el caso que NO salta: nada revocado
    assert comprobar_citas_revocadas([], [], vocabulario, {}) == []

    # el caso que SI salta, y nombra la seccion y el predicado
    fallos = comprobar_citas_revocadas([], [], vocabulario, {citado: "fb-el-que-lo-corrige"})
    assert fallos, "un predicado que cita un registro revocado tiene que saltar"
    assert all("predicados '" in f and "fb-el-que-lo-corrige" in f for f in fallos)

    # Y los ACUMULADORES, que tambien llevan cita y se quedaron fuera hasta la auditoria de
    # cierre de F12: era la cuarta vez que esta guardia nacia corta
    cita_acc = next(
        d["cita"]
        for d in vocabulario["acumuladores"].values()
        if isinstance(d, dict) and d.get("cita")
    )
    fallos = comprobar_citas_revocadas([], [], vocabulario, {cita_acc: "fb-el-que-lo-corrige"})
    assert any("acumuladores '" in f for f in fallos), fallos


def test_la_spec_real_no_cita_ningun_registro_revocado() -> None:
    """El golden: sobre la spec de verdad, con la cadena de supersede de verdad."""
    from botsito.feedback.modelo import cargar_feedback
    from botsito.spec.modelo import (
        FICHERO_GLOSARIO,
        FICHERO_SPEC,
        cargar_vocabulario,
        comprobar_citas_revocadas,
    )

    registros = cargar_feedback(REPO / "knowledge" / "feedback")
    revocados = {r.supersede: r.id for r in registros if r.supersede}
    fallos = comprobar_citas_revocadas(
        cargar_reglas(REPO / FICHERO_SPEC),
        cargar_glosario(REPO / FICHERO_GLOSARIO),
        cargar_vocabulario(REPO / FICHERO_SPEC),
        revocados,
    )
    assert not fallos, "; ".join(fallos)


def test_un_valor_sin_lector_salta_y_dice_cual() -> None:
    """Un parametro con valor que ninguna regla nombra y que nadie declara leer.

    F11 dejo nueve asi -la ficha del instrumento, el reloj del broker, las cuentas, el modelo de
    llenado-: valores de negocio que ninguna guardia miraba, porque todas miran las reglas. No se
    arreglan inventandoles una regla (ADR-0016): se declara quien los lee.
    """
    from botsito.spec.modelo import FICHERO_SPEC, comprobar_consumo

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    nombrado = next(p for r in reglas if r.vigente for p in r.parametros)

    # NO salta: una regla vigente lo nombra
    assert comprobar_consumo(reglas, {nombrado: None}, {}) == []
    # NO salta: no lo nombra nadie, pero declara la funcionalidad que lo consumira
    assert comprobar_consumo(reglas, {"suelto": ("F24",)}, {"F24": "funcionalidad"}) == []

    # SALTA: ni regla ni declaracion
    (fallo,) = comprobar_consumo(reglas, {"suelto": None}, {})
    assert "suelto" in fallo and "consumido_por" in fallo
    # SALTA: declara algo que no existe
    (fallo,) = comprobar_consumo(reglas, {"suelto": ("F99",)}, {"F24": "funcionalidad"})
    assert "F99" in fallo and "no existe" in fallo
    # SALTA: declara una regla vigente que NO lo nombra, que es peor que no declarar nada
    vigente = next(r for r in reglas if r.vigente)
    (fallo,) = comprobar_consumo(reglas, {"suelto": (vigente.id,)}, {vigente.id: "regla vigente"})
    assert vigente.id in fallo and "NO lo nombra" in fallo


def test_la_forma_no_puede_usar_un_parametro_que_la_regla_no_declara() -> None:
    """`parametros` y `forma` tienen que decir lo mismo.

    Varias guardias leen la lista `parametros` -la del ADR de una regla de entorno, la de los
    UNKNOWN- y se vuelven ciegas si la forma usa algo que la lista no menciona. Las cuatro reglas
    del piloto estaban asi: RN-014 ejecutaba `break_even_criterio_ruptura`, DEFAULT_AMBIGUOUS bajo
    A-13, sin declararlo.
    """
    import dataclasses

    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())

    base = next(r for r in reglas if r.id == "RN-014")
    assert "break_even_criterio_ruptura" in base.parametros, "la regla real ya lo declara"
    # Solo miramos esta comprobacion: pasar una regla suelta hace saltar la de los hechos, que
    # necesita el conjunto entero para saber quien produce y quien consume.
    assert not [f for f in comprobar_forma([base], vocabulario, parametros) if "no lo declara" in f]

    mutilada = dataclasses.replace(
        base, parametros=tuple(p for p in base.parametros if p != "break_even_criterio_ruptura")
    )
    fallos = comprobar_forma([mutilada], vocabulario, parametros)
    assert any(
        "RN-014" in f and "break_even_criterio_ruptura" in f and "no lo declara" in f
        for f in fallos
    ), fallos


def test_el_vocabulario_no_puede_poner_palabras_en_boca_del_trader() -> None:
    """Un predicado lleva `cita` y `literal` propios, y nadie los cruzaba.

    El comentario que habia en `comprobar_literales` lo predijo con estas palabras: "el dia que
    algo con cita propia -un predicado, F12- no pase por `comprobar_contra`, esta guardia se
    apagaria sin avisar". Paso: se podia escribir cualquier frase como literal de un predicado.
    """
    from botsito.spec.modelo import (
        FICHERO_GLOSARIO,
        FICHERO_SPEC,
        cargar_vocabulario,
        comprobar_contra,
        comprobar_literales,
    )

    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    terminos = cargar_glosario(REPO / FICHERO_GLOSARIO)
    nombre, datos = next(
        (n, d) for n, d in vocabulario["predicados"].items() if d.get("cita") and d.get("literal")
    )

    # NO salta: el literal real esta en lo que cita
    textos = {str(datos["cita"]): str(datos["literal"])}
    assert not comprobar_literales([], textos, [], vocabulario)

    # SALTA: se le pone otra frase en la boca
    mentira = {**vocabulario, "predicados": {nombre: {**datos, "literal": "esto no lo dijo nadie"}}}
    (fallo,) = comprobar_literales([], textos, [], mentira)
    assert nombre in fallo and str(datos["cita"]) in fallo

    # Y la cita tiene que existir: antes un fb-...-deadbeef pasaba entero
    inventada = {**vocabulario, "predicados": {nombre: {**datos, "cita": "fb-no-existe-deadbeef"}}}
    fallos = comprobar_contra([], terminos, set(), set(textos), inventada)
    assert any(nombre in f and "no existe" in f for f in fallos), fallos


def test_lo_que_una_regla_prohibe_tiene_que_existir() -> None:
    """`permite` y `prohibe` no se comprobaban contra nada: su valor es una lista.

    Once de las veinticuatro reglas vigentes prohiben algo, y sus dos unicos objetivos
    -`abrir_operacion` y `buscar_entradas`- no estaban declarados en ninguna seccion: una ene de
    mas pasaba entera (F12, auditoria de cierre).
    """
    import dataclasses

    from botsito.config.registro import cargar_registro
    from botsito.spec.modelo import FICHERO_SPEC, cargar_vocabulario, comprobar_forma

    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    parametros = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())
    assert vocabulario["efectos"], "la seccion `efectos` tiene que existir"

    base = next(r for r in reglas if r.forma and "prohibe" in str(r.forma))
    torcida = dataclasses.replace(
        base,
        forma={**(base.forma or {}), "entonces": {"prohibe": ["abrir_operacionn"]}},
    )
    fallos = comprobar_forma([torcida], vocabulario, parametros)
    assert any("abrir_operacionn" in f and base.id in f for f in fallos), fallos


def test_la_puerta_de_spec_check_denuncia_y_nombra_ids() -> None:
    """`spec check` y `knowledge validate` comparten `problemas_de_spec`: se prueba la puerta.

    Solo se probaba el camino verde, asi que nada fijaba que la capa devuelva los fallos con su
    id (criterio de aceptacion 4 del brief) ni que `spec check` pueda salir con 1.
    """
    from botsito.config.registro import Registro, cargar_registro
    from botsito.evidence.modelo import cargar_evidencia
    from botsito.feedback.modelo import cargar_feedback
    from botsito.validation.knowledge import problemas_de_spec

    items = cargar_evidencia(REPO / "knowledge" / "evidence")
    fb = cargar_feedback(REPO / "knowledge" / "feedback")
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")

    problemas, resumen = problemas_de_spec(REPO, registro, items, fb)
    assert problemas == [], "la spec real tiene que estar limpia"
    assert "reglas de spec" in resumen

    # Un registro sin parametros: todas las reglas nombran cosas que no existen
    problemas, _ = problemas_de_spec(REPO, Registro(parametros={}), items, fb)
    assert problemas, "un registro vacio tiene que romper la capa"
    assert all(
        re.match(r"(RN-\d{3}|glosario |predicados |acciones |hecho |acumulador |\w+:)", p)
        for p in problemas
    ), problemas[:5]
