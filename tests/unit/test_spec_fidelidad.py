"""Las correcciones de fidelidad de la spec (rama `trabajo/fidelidad-de-la-spec`, 2026-09-16).

Un test por punto del brief y dos por guardia nueva: uno que la dispara y otro que no. Aqui no hay
motor, asi que lo que se fija es la FORMA que el motor leera: si alguien vuelve a invertir RN-005,
a dejar una posicion sin objetivo o a fijar un hecho del broker, la suite se pone roja.
"""

from __future__ import annotations

import copy
import dataclasses
import json
from pathlib import Path
from typing import Any

import pytest

from botsito.config.registro import cargar_registro
from botsito.spec.modelo import (
    FICHERO_SPEC,
    Regla,
    cargar_reglas,
    cargar_vocabulario,
    comprobar_consumo,
    comprobar_forma,
    comprobar_precedencia,
    comprobar_vocabulario,
)

REPO = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def spec() -> tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]]:
    reglas = cargar_reglas(REPO / FICHERO_SPEC)
    vocabulario = cargar_vocabulario(REPO / FICHERO_SPEC)
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    tipos = {n: str(getattr(p.tipo, "value", p.tipo)) for n, p in registro.parametros.items()}
    return reglas, vocabulario, set(registro.nombres()), tipos


def _por_id(reglas: list[Regla]) -> dict[str, Regla]:
    return {r.id: r for r in reglas}


def _forma(regla: Regla) -> dict[str, Any]:
    assert isinstance(regla.forma, dict), regla.id
    return regla.forma


def _hace(regla: Regla) -> list[str]:
    return [next(iter(a)) for a in _forma(regla).get("entonces", {}).get("hace", [])]


# ---------------------------------------------------------------- 2.1 · RN-005 en los dos sentidos


def test_rn005_prohibe_el_lado_de_ruido_y_no_el_de_la_operativa(spec: Any) -> None:
    """Estaba al reves: prohibia abrir por debajo de la liquidez de M15 en sesgo alcista, que es
    donde el trader opera (v1 0:13:06), y por encima en bajista (v3 0:17:25). Se fijan los dos
    sentidos por separado: invertir uno solo tambien tiene que romper la suite."""
    reglas, vocabulario, _, _ = spec
    rn005 = _por_id(reglas)["RN-005"]
    assert rn005.clase == "gate"
    cuando = _forma(rn005)["cuando"]["todos_de"]
    assert {"hecho": "sesgo", "liga": "S"} in cuando
    (llamada,) = [c for c in cuando if "se_desarrolla_en_el_lado_de_ruido" in c]
    assert llamada["se_desarrolla_en_el_lado_de_ruido"] == {"que": "liquidez_m15", "sentido": "S"}
    assert _forma(rn005)["entonces"] == {"prohibe": ["abrir_operacion"]}

    lados = vocabulario["predicados"]["se_desarrolla_en_el_lado_de_ruido"]["lado_de_ruido"]
    # alcista: opera por DEBAJO, asi que lo de ENCIMA es ruido y se prohibe
    assert lados["alcista"] == "por_encima"
    # bajista: opera por ENCIMA, asi que lo de DEBAJO es ruido y se prohibe
    assert lados["bajista"] == "por_debajo"
    # y cada sentido cita lo suyo: la regla, el bajista; el predicado, el alcista
    assert rn005.cita == "ev-v3-001725-bca9714b" and "por encima no por debajo" in rn005.literal
    predicado = vocabulario["predicados"]["se_desarrolla_en_el_lado_de_ruido"]
    assert predicado["cita"] == "ev-v1-001306-f98e12e9"
    assert "tiene que estar por debajo" in " ".join(predicado["literal"].split())


def test_el_lado_de_ruido_nombra_los_dos_sentidos_y_no_el_mismo_lado(spec: Any) -> None:
    reglas, vocabulario, _, _ = spec
    assert comprobar_vocabulario(reglas, vocabulario) == []
    for roto, aguja in (
        ({"alcista": "por_encima"}, "exactamente"),
        ({"alcista": "por_encima", "bajista": "por_encima"}, "mismo lado"),
        ({"alcista": "arriba", "bajista": "por_debajo"}, "'arriba'"),
    ):
        voc = copy.deepcopy(vocabulario)
        voc["predicados"]["se_desarrolla_en_el_lado_de_ruido"]["lado_de_ruido"] = roto
        assert any(aguja in p for p in comprobar_vocabulario(reglas, voc)), roto


# ---------------------------------------------------------------- 1 · hechos derivados del broker


def test_fijar_un_hecho_del_broker_hace_fallar_la_forma(spec: Any) -> None:
    reglas, vocabulario, parametros, tipos = spec
    assert comprobar_forma(reglas, vocabulario, parametros, tipos=tipos) == []
    por_id = _por_id(reglas)
    rn010 = por_id["RN-010"]
    forma = copy.deepcopy(_forma(rn010))
    forma["entonces"]["hace"].append({"fijar": {"hecho": "operacion_abierta", "a": "si"}})
    rotas = [dataclasses.replace(rn010, forma=forma) if r.id == "RN-010" else r for r in reglas]
    fallos = comprobar_forma(rotas, vocabulario, parametros, tipos=tipos)
    assert any("RN-010" in f and "operacion_abierta" in f and "broker" in f for f in fallos), fallos


def test_un_hecho_del_broker_sin_accion_que_lo_provoque_salta(spec: Any) -> None:
    reglas, vocabulario, parametros, tipos = spec
    voc = copy.deepcopy(vocabulario)
    voc["hechos"]["orden_limite_pendiente"].pop("lo_provoca")
    assert any(
        "orden_limite_pendiente" in f and "lo_provoca" in f
        for f in comprobar_forma(reglas, voc, parametros, tipos=tipos)
    )
    # y si la accion existe pero NINGUNA regla vigente la ejecuta, tambien: es lo que era
    # `se_coloca_orden_limite`, un evento que nadie producia
    sin_colocar = [
        dataclasses.replace(r, estado="DESCARTADA") if r.id == "RN-015" else r for r in reglas
    ]
    fallos = comprobar_forma(sin_colocar, vocabulario, parametros, tipos=tipos)
    assert any("colocar_orden_limite" in f and "NINGUNA regla vigente" in f for f in fallos)


def test_una_regla_descartada_no_cuenta_como_productor_real(spec: Any) -> None:
    """Mutante de la auditoria de cierre: RN-013 DESCARTADA con una forma que fija
    `detenido_por_tope`, declarada productora, pasaba sin una queja."""
    reglas, vocabulario, parametros, tipos = spec
    fija = {
        "cuando": {"todos_de": [{"salta_stop": {}}]},
        "entonces": {
            "hace": [{"fijar": {"hecho": "detenido_por_tope", "a": "hasta_el_corte_siguiente"}}]
        },
    }
    con_forma = [dataclasses.replace(r, forma=fija) if r.id == "RN-013" else r for r in reglas]
    voc = copy.deepcopy(vocabulario)
    voc["hechos"]["detenido_por_tope"]["produce"] = ["RN-013", "RN-020", "RN-029"]
    fallos = comprobar_forma(con_forma, voc, parametros, tipos=tipos)
    assert any("detenido_por_tope" in f and "produce" in f for f in fallos), fallos


def test_un_predicado_del_broker_o_del_bot_declara_quien_lo_provoca(spec: Any) -> None:
    reglas, vocabulario, _, _ = spec
    voc = copy.deepcopy(vocabulario)
    voc["predicados"]["salta_stop"].pop("lo_provoca")
    assert any("salta_stop" in p and "lo_provoca" in p for p in comprobar_vocabulario(reglas, voc))
    voc = copy.deepcopy(vocabulario)
    voc["predicados"]["rompe"].pop("fuente")
    assert any("'rompe'" in p and "fuente" in p for p in comprobar_vocabulario(reglas, voc))


def test_una_clave_mal_escrita_en_el_vocabulario_ya_no_se_ignora(spec: Any) -> None:
    reglas, vocabulario, _, _ = spec
    voc = copy.deepcopy(vocabulario)
    voc["hechos"]["operacion_abierta"]["orgien"] = "broker"
    assert any("orgien" in p for p in comprobar_vocabulario(reglas, voc))


# ---------------------------------------------------------------- 2.2 y 2.4 · colocar, con objetivo


def test_existe_la_regla_que_coloca_y_la_orden_sale_con_stop_y_objetivo(spec: Any) -> None:
    """Antes, ninguna de las trece acciones colocaba una orden: la jornada daba cero colocaciones.
    Y RN-015 escribia el objetivo al LLENARSE por un esquema, asi que una activacion sin ruptura
    dejaba la posicion sin objetivo. Ahora la unica accion que provoca una posicion es colocar, y
    toda regla que coloca escribe el objetivo antes, en su mismo `hace`; el stop lo escribe la regla
    que produce el hecho que la dispara."""
    reglas, vocabulario, _, _ = spec
    que_colocan = [r for r in reglas if r.vigente and "colocar_orden_limite" in _hace(r)]
    assert [r.id for r in que_colocan] == ["RN-015"]
    for r in que_colocan:
        hace = _hace(r)
        assert hace.index("fijar_objetivo") < hace.index("colocar_orden_limite"), r.id
        assert {"hecho": "orden_dimensionada", "liga": "Z"} in _forma(r)["cuando"]["todos_de"]
    # la unica via de una posicion viva es esa accion, sea cual sea la forma de activarse
    for derivado in ("operacion_abierta", "orden_limite_pendiente"):
        assert vocabulario["hechos"][derivado]["lo_provoca"] == ["colocar_orden_limite"]
    for evento in ("se_activa_entrada", "salta_stop", "se_cierra_operacion"):
        assert vocabulario["predicados"][evento]["lo_provoca"] == ["colocar_orden_limite"]
    # y quien produce `orden_dimensionada` escribe el stop: RN-011, antes que el hecho
    hechos = vocabulario["hechos"]["orden_dimensionada"]
    for rid in hechos["produce"]:
        r = _por_id(reglas)[rid]
        if "escribir_stop_en_la_orden" in _hace(r):
            assert _hace(r).index("escribir_stop_en_la_orden") < _hace(r).index("fijar")
    assert "escribir_stop_en_la_orden" in _hace(_por_id(reglas)["RN-011"])
    # colocar lleva efecto: un gate que prohibe abrir la frena
    assert vocabulario["acciones"]["colocar_orden_limite"]["efecto"] == "abrir_operacion"
    # ninguna regla escribe ya el stop o el objetivo al llenarse la orden
    for r in reglas:
        if r.vigente and "se_activa_entrada" in json.dumps(r.forma or {}, ensure_ascii=False):
            assert not {"escribir_stop_en_la_orden", "fijar_objetivo"} & set(_hace(r)), r.id


def test_una_accion_que_provoca_un_hecho_del_broker_declara_su_efecto(spec: Any) -> None:
    reglas, vocabulario, parametros, tipos = spec
    voc = copy.deepcopy(vocabulario)
    voc["acciones"]["colocar_orden_limite"].pop("efecto")
    assert any(
        "colocar_orden_limite" in f and "efecto" in f
        for f in comprobar_forma(reglas, voc, parametros, tipos=tipos)
    )


def test_la_pendiente_a_las_15_esta_declarada_como_ambiguedad_y_no_supuesta(spec: Any) -> None:
    from botsito.cases.ambiguedades import FICHERO_AMBIGUEDADES, cargar_ambiguedades

    reglas, vocabulario, _, _ = spec
    assert "retirar_orden_limite" in vocabulario["acciones"]
    assert not [
        r.id for r in reglas if isinstance(r.forma, dict) and "retirar_orden_limite" in _hace(r)
    ], "ninguna regla la usa hasta que el trader responda A-30"
    por_id = {a.id: a for a in cargar_ambiguedades(REPO / FICHERO_AMBIGUEDADES)}
    assert por_id["A-30"].estado == "ABIERTA" and por_id["A-30"].clase == "pregunta"
    assert por_id["A-29"].parametros == ("orden_limite_nace",)


# ---------------------------------------------------------------- 2.3 · el caso de v6 1:23:13


_COMODINES = {"cualquier_activacion": None}


def _casa(esperado: str, real: str) -> bool:
    if esperado in _COMODINES:
        return True
    if esperado == "cualquier_esquema":
        return real in ("primer_esquema", "segundo_esquema")
    return esperado == real


def _dispara_con_cierre(regla: Regla, resultado: str, por: str) -> bool:
    """Si la regla tiene un `se_cierra_operacion` que casa con este cierre."""
    from botsito.spec.modelo import _invocaciones

    return any(
        _casa(args["resultado"], resultado) and _casa(args["por"], por)
        for nombre, args in _invocaciones(_forma(regla)["cuando"])
        if nombre == "se_cierra_operacion"
    )


def test_cerrar_un_equal_con_perdida_no_gasta_cartucho_y_habilita_la_reentrada(spec: Any) -> None:
    """v6 1:23:13-1:23:19: la entrada se activa sin validar, un equal la saca y "te genera una
    perdida". Con la forma anterior llegaba como `perdida`: RN-016 gastaba cartucho y RN-019 -que
    pedia `resultado: equal`- no disparaba, contra "reentrada despues de equal, tampoco es
    considerado un intento"."""
    reglas, _, _, _ = spec
    por_id = _por_id(reglas)
    # el caso del trader
    assert not _dispara_con_cierre(por_id["RN-016"], "perdida", "activacion_sin_ruptura")
    assert _dispara_con_cierre(por_id["RN-019"], "perdida", "activacion_sin_ruptura")
    # y la contraparte: una perdida de un esquema SI gasta, y RN-019 no se mete ahi
    assert _dispara_con_cierre(por_id["RN-016"], "perdida", "primer_esquema")
    assert not _dispara_con_cierre(por_id["RN-019"], "perdida", "segundo_esquema")
    # un break even no gasta cartucho, tenga el P/L neto que tenga
    assert not _dispara_con_cierre(por_id["RN-016"], "break_even", "primer_esquema")
    assert not _dispara_con_cierre(por_id["RN-016"], "break_even", "activacion_sin_ruptura")


def test_el_stop_entero_gasta_cartucho_aunque_la_entrada_se_activara_sin_ruptura(
    spec: Any,
) -> None:
    """Hallazgo posterior al informe (2026-09-17): la exencion era ancha de mas. Una operacion
    activada sin ruptura que se iba al stop de stop_fraccion_caja -el riesgo entero- no gastaba
    intento y RN-019 habilitaba reentrar. El trader exime el break even, la entrada invalidada y la
    reentrada tras un equal, y el equal que describe no llega al stop. Lo que queda es A-31."""
    reglas, vocabulario, _, _ = spec
    por_id = _por_id(reglas)
    # stop saltado sobre una entrada activada sin ruptura: GASTA, y no habilita reentrar
    assert _dispara_con_cierre(por_id["RN-016"], "salto_el_stop", "activacion_sin_ruptura")
    assert not _dispara_con_cierre(por_id["RN-019"], "salto_el_stop", "activacion_sin_ruptura")
    # y sobre un esquema, igual
    assert _dispara_con_cierre(por_id["RN-016"], "salto_el_stop", "segundo_esquema")
    # cierre en rojo SIN stop de esa misma entrada: no gasta, y RN-019 si dispara
    assert not _dispara_con_cierre(por_id["RN-016"], "perdida", "activacion_sin_ruptura")
    assert _dispara_con_cierre(por_id["RN-019"], "perdida", "activacion_sin_ruptura")
    # el mecanismo esta declarado, no inventado en el test
    assert (
        "salto_el_stop" in vocabulario["predicados"]["se_cierra_operacion"]["valores"]["resultado"]
    )
    assert "cualquier_resultado" not in vocabulario["tokens"]


def test_ningun_token_equal_y_el_cierre_declara_su_conjunto_de_resultados(spec: Any) -> None:
    reglas, vocabulario, _, _ = spec
    assert "equal" not in vocabulario["tokens"]
    valores = vocabulario["predicados"]["se_cierra_operacion"]["valores"]
    assert {"ganancia", "perdida", "break_even", "salto_el_stop"} <= set(valores["resultado"])
    assert "activacion_sin_ruptura" in valores["por"]
    # y la guardia compara lo que las formas pasan con ese conjunto
    rn017 = _por_id(reglas)["RN-017"]
    forma = copy.deepcopy(_forma(rn017))
    forma["cuando"]["todos_de"][0]["se_cierra_operacion"]["resultado"] = "equal"
    rota = [dataclasses.replace(rn017, forma=forma) if r.id == "RN-017" else r for r in reglas]
    vocab = copy.deepcopy(vocabulario)
    vocab["tokens"]["equal"] = {"descripcion": "reintroducido para la prueba"}
    assert any("RN-017" in p and "conjunto" in p for p in comprobar_vocabulario(rota, vocab))


# ---------------------------------------------------------------- 3 · el margen antes del limite


def test_los_frenos_de_la_firma_saltan_antes_del_limite_y_hay_lectura_prospectiva(
    spec: Any,
) -> None:
    reglas, _, parametros, _ = spec
    assert "firma_margen_seguridad" in parametros
    por_id = _por_id(reglas)
    for rid in ("RN-029", "RN-030", "RN-031"):
        texto = json.dumps(_forma(por_id[rid])["cuando"], ensure_ascii=False)
        assert "se_acerca_al_limite" in texto and "firma_margen_seguridad" in texto, rid
        assert "alcanza_tope" not in texto, f"{rid}: vuelve a frenar EN el limite"
    rn032 = por_id["RN-032"]
    assert rn032.clase == "gate" and rn032.decision == "ADR-0031"
    texto = json.dumps(_forma(rn032)["cuando"], ensure_ascii=False)
    for acumulador in ("perdida_dia_firma", "perdida_total_firma"):
        assert acumulador in texto
    assert "riesgo_por_operacion" in texto and "firma_margen_seguridad" in texto
    assert "hace" not in _forma(rn032)["entonces"], "la prospectiva prohibe, no detiene"


# ---------------------------------------------------------------- 5 · la clase de RN-030


def test_rn030_es_terminal_y_su_complementa_sigue_siendo_verdad(spec: Any) -> None:
    reglas, _, _, _ = spec
    por_id = _por_id(reglas)
    assert por_id["RN-030"].clase == por_id["RN-002"].clase == "terminal"
    assert comprobar_precedencia(reglas) == []
    # como gate, RN-029 y RN-031 son subconjunto suyo y SIN `complementa` saltaria; como terminal
    # no comparte clase con ellas y `complementa` se conserva porque dice la verdad
    sin_comp = dataclasses.replace(por_id["RN-030"], complementa=())
    assert comprobar_precedencia([sin_comp if r.id == "RN-030" else r for r in reglas]) == []
    como_gate = dataclasses.replace(por_id["RN-030"], clase="gate", complementa=())
    fallos = comprobar_precedencia([como_gate if r.id == "RN-030" else r for r in reglas])
    assert any("RN-030" in f and "subconjunto" in f for f in fallos), fallos


# ---------------------------------------------------------------- 7 · firma_magnitud_vigilada


def test_la_magnitud_vigilada_la_lee_la_forma_y_quitarla_salta(spec: Any) -> None:
    reglas, vocabulario, _, _ = spec
    registro = cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml")
    consumidores = {n: p.consumido_por for n, p in registro.parametros.items()}
    con_valor = {n for n, p in registro.parametros.items() if p.valor is not None}
    ids = {
        **{c: "funcionalidad" for cs in consumidores.values() for c in (cs or ()) if c[0] == "F"},
        **{c: "ADR" for cs in consumidores.values() for c in (cs or ()) if c.startswith("ADR")},
        **{r.id: ("regla vigente" if r.vigente else "regla") for r in reglas},
    }
    assert comprobar_consumo(reglas, consumidores, ids, con_valor, vocabulario) == []
    for nombre in ("perdida_dia_firma", "perdida_total_firma"):
        assert vocabulario["acumuladores"][nombre]["magnitud"] == "firma_magnitud_vigilada"

    voc = copy.deepcopy(vocabulario)
    for datos in voc["acumuladores"].values():
        datos.pop("magnitud", None)
    fallos = comprobar_consumo(reglas, consumidores, ids, con_valor, voc)
    assert any("firma_magnitud_vigilada" in f and "NINGUNA forma" in f for f in fallos), fallos
    # y la lista `parametros` de una regla ya no cuenta como lectura: RN-029 lo sigue listando
    assert "firma_magnitud_vigilada" in _por_id(reglas)["RN-029"].parametros


# ---------------------------------------------------------------- 8 · el tope total, permanente


def test_el_tope_total_no_lo_levanta_ningun_corte(spec: Any) -> None:
    reglas, vocabulario, parametros, tipos = spec
    por_id = _por_id(reglas)
    rn031 = por_id["RN-031"]
    assert rn031.clase == "gate"
    assert {"fijar": {"hecho": "detenido_por_tope_total", "a": "permanente"}} in _forma(rn031)[
        "entonces"
    ]["hace"]
    assert vocabulario["tokens"]["permanente"]["clase"] == "duracion"
    total = vocabulario["hechos"]["detenido_por_tope_total"]
    assert total["valores"] == ["permanente"] and "RN-001" in total["consume"]
    assert {"hecho": "detenido_por_tope_total"} in _forma(por_id["RN-001"])["cuando"][
        "cualquiera_de"
    ]
    # RN-029 ya no alcanza el total: no puede ponerle "hasta el corte siguiente"
    assert "perdida_total_firma" not in json.dumps(_forma(por_id["RN-029"]), ensure_ascii=False)
    # y fijar `permanente` en el hecho diario salta: sus lectores lo reescribirian en cada evento
    rn029 = por_id["RN-029"]
    forma = copy.deepcopy(_forma(rn029))
    forma["entonces"]["hace"][0]["fijar"]["a"] = "permanente"
    rotas = [dataclasses.replace(rn029, forma=forma) if r.id == "RN-029" else r for r in reglas]
    fallos = comprobar_forma(rotas, vocabulario, parametros, tipos=tipos)
    assert any("RN-029" in f and "permanente" in f and "valores" in f for f in fallos), fallos


# ---------------------------------------------------------------- 9 · reinicia_con


def test_reinicia_con_no_admite_un_booleano_y_si_un_token_de_reinicio(spec: Any) -> None:
    reglas, vocabulario, parametros, tipos = spec
    assert vocabulario["acumuladores"]["perdida_total_firma"]["reinicia_con"] == "nunca"
    assert comprobar_forma(reglas, vocabulario, parametros, tipos=tipos) == []

    voc = copy.deepcopy(vocabulario)
    voc["acumuladores"]["perdida_total_firma"]["reinicia_con"] = "firma_perdida_total_arrastra"
    fallos = comprobar_forma(reglas, voc, parametros, tipos=tipos)
    assert any("perdida_total_firma" in f and "booleano" in f for f in fallos), fallos

    voc = copy.deepcopy(vocabulario)
    voc["acumuladores"]["perdida_total_firma"]["reinicia_con"] = "permanente"
    fallos = comprobar_forma(reglas, voc, parametros, tipos=tipos)
    assert any("perdida_total_firma" in f and "reinicio" in f for f in fallos), fallos


# ---------------------------------------------------------------- 4 · medicion o pregunta


def test_las_mediciones_no_entran_en_el_cuestionario() -> None:
    """A-16, A-27 y A-28 dicen en su propio texto que son mediciones, y `cuestionario.py` metia
    toda abierta en la sesion siguiente: le habrian llegado al trader como preguntas."""
    from botsito.cases.ambiguedades import abiertas_sin_clase
    from botsito.cases.cuestionario import generar
    from botsito.cases.paquete import _cargar_todo
    from botsito.comun.documentos import activos
    from botsito.evidence.contradicciones import detectar

    _config, registro, ambiguedades, mapa, _meses, _dias, items = _cargar_todo(REPO)
    assert abiertas_sin_clase(ambiguedades) == []
    clases = {a.id: a.clase for a in ambiguedades if a.estado == "ABIERTA"}
    assert {clases[x] for x in ("A-16", "A-27", "A-28")} == {"medicion"}
    vivos = activos(list(items))
    preguntas = generar(registro, ambiguedades, mapa, detectar(vivos), vivos, lambda _v, _t: None)
    en_cuestionario = {o["id"] for p in preguntas for o in p.origenes if o["tipo"] == "ambiguedad"}
    assert not {"A-16", "A-27", "A-28"} & en_cuestionario
    assert {"A-13", "A-29", "A-30"} <= en_cuestionario

    sin_clase = [dataclasses.replace(a, clase=None) if a.id == "A-29" else a for a in ambiguedades]
    (fallo,) = abiertas_sin_clase(sin_clase)
    assert "A-29" in fallo
