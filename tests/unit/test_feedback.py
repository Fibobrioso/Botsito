from pathlib import Path
from typing import Any

import pytest
import yaml
from hypothesis import given
from hypothesis import strategies as st

from botsito.feedback.modelo import (
    FeedbackError,
    activos,
    calcular_id,
    cargar_feedback,
    cargar_registro,
    contenido_canonico,
    escribir_registro,
    registro_desde_dict,
    trazar,
    validar_contra_contexto,
)

EV = "ev-v4-001533-1a2b3c4d"


def base(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "sesion": "2026-09-20-sesion-01",
        "fecha": "2026-09-20",
        "medio": "replay",
        "grabacion": "Material adicional/sesion-01.mp4",
        "t0": "0:12:10",
        "t1": "0:12:40",
        "objetivo": {"tipo": "evidence", "id": EV},
        "accion": "CONFIRM",
        "respuesta_literal": "si, con cuerpo, siempre con cuerpo en M15",
        "registrado_por": "aleks",
    }
    d.update(cambios)
    return d


def test_crear_cargar_y_nombre(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    r = cargar_registro(ruta)
    assert r.id.startswith("fb-2026-09-20-sesion-01-") and ruta.stem == r.id
    assert ruta.parent.name == "2026-09-20-sesion-01"
    with pytest.raises(FeedbackError, match="ya existe"):
        escribir_registro(tmp_path, base())


def test_editar_rompe_el_id(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    doc["respuesta_literal"] = "otra cosa distinta"
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True), encoding="utf-8")
    with pytest.raises(FeedbackError, match="no coincide"):
        cargar_registro(ruta)


def test_carpeta_de_sesion(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    otra = tmp_path / "otra" / ruta.name
    otra.parent.mkdir()
    ruta.rename(otra)
    with pytest.raises(FeedbackError, match="carpeta de su sesion"):
        cargar_registro(otra)


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"respuesta_literal": ""}, "obligatorios"),
        ({"respuesta_literal": "si"}, "literal"),
        ({"sesion": "sesion1"}, "sesion invalida"),
        ({"fecha": "20/09/2026"}, "fecha invalida"),
        ({"medio": "telepatia"}, "medio"),
        ({"accion": "APROBAR"}, "accion"),
        ({"objetivo": {"tipo": "regla", "id": "RN-01"}}, "formato"),
        ({"objetivo": {"tipo": "caso", "id": "caso-1"}}, "exige objetivo de tipo"),
        ({"accion": "CORRECT"}, "exige valor_resultante"),
        ({"accion": "RESOLVE_CONTRADICTION"}, "exige objetivo de tipo"),
        ({"grabacion": None}, "exige grabacion"),
        ({"t1": "0:12:10"}, "t0 debe ser menor"),
        ({"supersede": "x"}, "supersede"),
        ({"extra": 1}, "desconocidos"),
        ({"fecha": "2026-09-21"}, "fecha debe ser la de la sesion"),
        ({"t0": 3900}, "t0 debe ser texto entre comillas"),
        ({"medio": "escrito", "grabacion": None, "t0": "basura"}, "t0: tiempo invalido"),
        ({"accion": "CORRECT", "valor_resultante": True}, "valor_resultante debe ser texto"),
    ],
)
def test_rechazos(cambio: dict[str, Any], mensaje: str) -> None:
    campos = base(**cambio)
    campos["id"] = "fb-2026-09-20-sesion-01-00000000"
    with pytest.raises(FeedbackError, match=mensaje):
        registro_desde_dict(campos)


def test_medio_escrito_no_exige_grabacion(tmp_path: Path) -> None:
    campos = base(medio="escrito", grabacion=None, t0=None, t1=None)
    r = cargar_registro(escribir_registro(tmp_path, campos))
    assert r.grabacion is None and r.medio == "escrito"


def test_acciones_coherentes(tmp_path: Path) -> None:
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_CONTRADICTION",
            objetivo={"tipo": "contradiccion", "id": "mitigacion.m15.cierre"},
            valor_resultante="cuerpo",
        ),
    )
    escribir_registro(
        tmp_path,
        base(
            accion="LABEL_CASE",
            objetivo={"tipo": "caso", "id": "caso-2026-07-02-a"},
            valor_resultante="opera",
        ),
    )
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_UNKNOWN",
            objetivo={"tipo": "ambiguedad", "id": "A-1"},
            valor_resultante="cierre",
        ),
    )
    assert len(cargar_feedback(tmp_path)) == 3


def test_validacion_contra_contexto(tmp_path: Path) -> None:
    escribir_registro(tmp_path, base())
    escribir_registro(tmp_path, base(objetivo={"tipo": "parametro", "id": "stop_fraccion"}))
    escribir_registro(
        tmp_path,
        base(
            accion="RESOLVE_CONTRADICTION",
            objetivo={"tipo": "contradiccion", "id": "x.y"},
            valor_resultante="a",
        ),
    )
    escribir_registro(tmp_path, base(supersede="fb-2026-09-20-sesion-01-deadbeef", notas="n"))
    problemas = validar_contra_contexto(
        cargar_feedback(tmp_path),
        ids_evidencia=set(),
        nombres_parametros=set(),
        temas_contradiccion=set(),
        rutas_corpus={"otra.mp4"},
    )
    assert any("no existe" in p and "evidencia" in p for p in problemas)
    assert any("no esta en el registro" in p for p in problemas)
    assert any("no hay contradiccion abierta" in p for p in problemas)
    assert any("supersede a" in p for p in problemas)
    assert any("no esta inventariada" in p for p in problemas)
    ok = validar_contra_contexto(
        [cargar_registro(escribir_registro(tmp_path, base(notas="ok")))],
        ids_evidencia={EV},
        nombres_parametros=set(),
        temas_contradiccion=set(),
        rutas_corpus={"Material adicional/sesion-01.mp4"},
    )
    assert ok == []


def test_supersede_y_traza(tmp_path: Path) -> None:
    primero = cargar_registro(escribir_registro(tmp_path, base()))
    segundo = escribir_registro(
        tmp_path,
        base(
            accion="CORRECT",
            valor_resultante="mecha",
            respuesta_literal="perdon, en M1 vale con mecha",
            supersede=primero.id,
            sesion="2026-09-21-sesion-02",
            fecha="2026-09-21",
        ),
    )
    registros = cargar_feedback(tmp_path)
    assert [r.id for r in activos(registros)] == [cargar_registro(segundo).id]
    lineas = trazar(EV, registros)
    assert len(lineas) == 3 and "[superseded]" in lineas[0] and "corrige a" in lineas[2]
    assert trazar("nada", registros) == ["sin registros de feedback para nada"]


@given(
    espacios=st.text(alphabet=" \t\n", max_size=3),
    extra=st.text(alphabet="xyz", min_size=1, max_size=4),
)
def test_id_estable_y_sensible(espacios: str, extra: str) -> None:
    ref = calcular_id(base())
    assert (
        calcular_id(base(respuesta_literal=espacios + base()["respuesta_literal"] + espacios))
        == ref
    )
    assert calcular_id(base(respuesta_literal=base()["respuesta_literal"] + " " + extra)) != ref


def test_fichero_escrito_a_mano_sin_comillas(tmp_path: Path) -> None:
    """`fecha: 2026-09-20` sin comillas sigue siendo texto; `t0: 1:05:00` sin comillas no lo es."""
    ruta = escribir_registro(tmp_path, base(medio="escrito", grabacion=None, t0=None, t1=None))
    texto = ruta.read_text(encoding="utf-8").replace("fecha: '2026-09-20'", "fecha: 2026-09-20")
    assert "fecha: 2026-09-20\n" in texto
    ruta.write_text(texto, encoding="utf-8")
    assert cargar_registro(ruta).fecha == "2026-09-20"
    ruta.write_text(texto + "t0: 1:05:00\nt1: 1:06:00\n", encoding="utf-8")
    with pytest.raises(FeedbackError, match="t0 debe ser texto entre comillas"):
        cargar_registro(ruta)
    ruta.write_text(texto + "notas: a\nnotas: b\n", encoding="utf-8")
    with pytest.raises(FeedbackError, match="clave duplicada"):
        cargar_registro(ruta)


def test_directorio_real_valida(repo: Path) -> None:
    """Desde la sesion 1 (2026-09-09) el feedback real ya no esta vacio: lo que se exige es que
    todo registro cargue, que los ids no se repitan y que cada `supersede` exista."""
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    ids = [r.id for r in registros]
    assert len(ids) == len(set(ids))
    for r in registros:
        if r.supersede is not None:
            assert r.supersede in set(ids), f"{r.id} supersede a un registro que no existe"


def test_campos_en_blanco_no_rompen_el_id(tmp_path: Path) -> None:
    """Un `--valor "   "` no puede producir un fichero cuyo id no coincida con su contenido."""
    ruta = escribir_registro(
        tmp_path,
        base(medio="escrito", grabacion="  ", t0=None, t1=None, valor_resultante="   ", notas="\t"),
    )
    r = cargar_registro(ruta)
    assert r.valor_resultante is None and r.notas is None and r.grabacion is None
    assert calcular_id(base(notas="  ")) == calcular_id(base())


def test_sesion_vacia_es_error_de_dominio(tmp_path: Path) -> None:
    with pytest.raises(FeedbackError, match="obligatorios"):
        escribir_registro(tmp_path, base(sesion=""))
    with pytest.raises(FeedbackError):
        calcular_id({})


@pytest.mark.parametrize(
    ("cambio", "mensaje"),
    [
        ({"sesion": "\u0662\u0660\u0662\u0666-09-20-sesion-01"}, "sesion invalida"),
        ({"fecha": "\u0662\u0660\u0662\u0666-09-20"}, "fecha invalida"),
        ({"sesion": "2026-13-45-sesion-01", "fecha": "2026-13-45"}, "fecha invalida"),
        ({"sesion": "2026-02-30-sesion-01", "fecha": "2026-02-30"}, "fecha invalida"),
        ({"objetivo": {"tipo": "regla", "id": "RN-\u0660\u0660\u0661"}}, "formato"),
        ({"t0": "\u0660:00:07"}, "t0: tiempo invalido"),
        ({"respuesta_literal": "     "}, "obligatorios"),
        ({"registrado_por": " "}, "obligatorios"),
    ],
)
def test_rechazos_unicode_y_fechas(cambio: dict[str, Any], mensaje: str) -> None:
    campos = base(**cambio)
    campos["id"] = "fb-2026-09-20-sesion-01-00000000"
    with pytest.raises(FeedbackError, match=mensaje):
        registro_desde_dict(campos)


def test_supersede_cruzado_y_ciclo(tmp_path: Path) -> None:
    a = cargar_registro(escribir_registro(tmp_path, base()))
    otro_objetivo = escribir_registro(
        tmp_path,
        base(
            objetivo={"tipo": "parametro", "id": "stop_fraccion"},
            supersede=a.id,
            respuesta_literal="esto va de otra cosa",
        ),
    )
    problemas = validar_contra_contexto(
        cargar_feedback(tmp_path), {EV}, {"stop_fraccion"}, set(), None
    )
    assert any("mismo objetivo" in p for p in problemas)
    otro_objetivo.unlink()
    b = escribir_registro(tmp_path, base(supersede=a.id, notas="b"))
    id_b = cargar_registro(b).id
    # Un ciclo requiere un fichero forjado: se simula con el detector directamente.
    from botsito.feedback.modelo import ciclos_de_supersede

    menor, mayor = sorted([a.id, id_b])
    assert ciclos_de_supersede({a.id: id_b, id_b: a.id}) == [
        f"ciclo de supersede: {menor} -> {mayor} -> {menor}"
    ]
    assert ciclos_de_supersede({a.id: None, id_b: a.id}) == []


def test_fichero_inesperado_no_pasa_en_silencio(tmp_path: Path) -> None:
    escribir_registro(tmp_path, base())
    (tmp_path / "2026-09-20-sesion-01" / "roto.yml").write_text("{", encoding="utf-8")
    with pytest.raises(FeedbackError, match="inesperado"):
        cargar_feedback(tmp_path)
    (tmp_path / "2026-09-20-sesion-01" / "roto.yml").unlink()
    (tmp_path / "README.md").write_text("x", encoding="utf-8")
    assert len(cargar_feedback(tmp_path)) == 1
    with pytest.raises(FeedbackError, match="no existe"):
        cargar_feedback(tmp_path / "nada")


def test_comprobar_impide_escribir(tmp_path: Path) -> None:
    with pytest.raises(FeedbackError, match="no existe"):
        escribir_registro(tmp_path, base(), lambda r: [f"{r.id}: evidencia objetivo no existe"])
    assert not list(tmp_path.rglob("*.yaml"))


def test_precondicion_de_ceguera_sobre_el_paquete(tmp_path: Path) -> None:
    """La confirmacion de que el trader no ha visto los meses del paquete es registrable.

    Antes de F10 no habia ningun objeto al que apuntar: la respuesta se perdia en el video de la
    sesion. Con el tipo `paquete` queda en el registro, y `vistos.yaml` puede citarla.
    """
    escribir_registro(
        tmp_path,
        base(
            accion="CONFIRM",
            objetivo={"tipo": "paquete", "id": "2026-09-20-sesion-01"},
            respuesta_literal="no he tocado mayo ni junio",
        ),
    )
    escribir_registro(
        tmp_path,
        base(
            accion="REJECT",
            objetivo={"tipo": "paquete", "id": "2026-09-20-sesion-01"},
            respuesta_literal="mayo si lo backtestee entero",
        ),
    )
    registros = cargar_feedback(tmp_path)
    assert len(registros) == 2
    assert validar_contra_contexto(registros, set(), set(), set()) == []


def test_el_paquete_confirmado_es_el_de_la_sesion(tmp_path: Path) -> None:
    escribir_registro(
        tmp_path,
        base(objetivo={"tipo": "paquete", "id": "2026-10-01-sesion-02"}),
    )
    (registro,) = cargar_feedback(tmp_path)
    assert validar_contra_contexto([registro], set(), set(), set()) == [
        f"{registro.id}: el paquete objetivo 2026-10-01-sesion-02 "
        "no es la sesion 2026-09-20-sesion-01"
    ]


@pytest.mark.parametrize("accion", ["CORRECT", "RESOLVE_UNKNOWN", "LABEL_CASE"])
def test_el_paquete_solo_se_confirma_o_se_rechaza(accion: str) -> None:
    with pytest.raises(FeedbackError, match="exige objetivo de tipo"):
        registro_desde_dict(
            base(
                accion=accion,
                objetivo={"tipo": "paquete", "id": "2026-09-20-sesion-01"},
                valor_resultante="lo que sea",
            ),
            "prueba",
        )


def test_dos_registros_no_pueden_superseder_al_mismo(tmp_path: Path) -> None:
    """El error natural de una ronda intensiva: corriges, vuelves a corregir y por inercia
    apuntas otra vez al original. Sin esta comprobacion quedan dos activos contradictorios y
    el fallo no asoma hasta el calculo del kappa, semanas despues."""
    original = escribir_registro(tmp_path, base(respuesta_literal="primera version"))
    ido = original.stem
    escribir_registro(tmp_path, base(respuesta_literal="segunda", supersede=ido))
    escribir_registro(tmp_path, base(respuesta_literal="tercera", supersede=ido))
    registros = cargar_feedback(tmp_path)
    problemas = validar_contra_contexto(registros, {EV}, set(), set())
    assert len(problemas) == 2
    assert all(f"{ido} ya esta superseded por" in p for p in problemas)
    assert all(p.startswith(tuple(r.id for r in registros)) for p in problemas)


def test_una_cadena_de_supersede_no_da_falso_positivo(tmp_path: Path) -> None:
    primero = escribir_registro(tmp_path, base(respuesta_literal="version una")).stem
    segundo = escribir_registro(
        tmp_path, base(respuesta_literal="version dos", supersede=primero)
    ).stem
    escribir_registro(tmp_path, base(respuesta_literal="version tres", supersede=segundo))
    assert validar_contra_contexto(cargar_feedback(tmp_path), {EV}, set(), set()) == []


def test_un_duplicado_a_mano_se_distingue_de_una_colision(tmp_path: Path) -> None:
    ruta = escribir_registro(tmp_path, base())
    with pytest.raises(FeedbackError, match="mismo contenido"):
        escribir_registro(tmp_path, base())
    ruta.write_text(ruta.read_text(encoding="utf-8") + "notas: a mano\n", encoding="utf-8")
    with pytest.raises(FeedbackError, match="OTRO contenido"):
        escribir_registro(tmp_path, base())


# --- valor_canonico (F11): re-expresar el valor sin tocar el literal del trader ---


def test_valor_canonico_es_opcional_y_no_cambia_el_id_de_los_registros_previos(
    tmp_path: Path,
) -> None:
    """Un campo ausente no entra en `contenido_canonico`, asi que los registros escritos antes
    de que existiera `valor_canonico` conservan su id."""
    sin = base(medio="escrito", grabacion=None, t0=None, t1=None)
    con = {**sin, "valor_canonico": None}
    assert contenido_canonico(sin) == contenido_canonico(con)
    r1 = cargar_registro(escribir_registro(tmp_path, sin))
    assert r1.valor_canonico is None


def test_valor_canonico_entra_en_el_id_cuando_tiene_contenido(tmp_path: Path) -> None:
    """Pero si lleva valor, es contenido: dos registros que solo difieren en el canonico son
    registros distintos, con ids distintos."""
    a = base(medio="escrito", grabacion=None, t0=None, t1=None, valor_resultante="0,8")
    b = {**a, "valor_canonico": "0.8"}
    assert contenido_canonico(a) != contenido_canonico(b)
    r = cargar_registro(escribir_registro(tmp_path, b))
    assert r.valor_canonico == "0.8" and r.valor_resultante == "0,8"


def test_valor_canonico_en_blanco_se_descarta(tmp_path: Path) -> None:
    campos = base(medio="escrito", grabacion=None, t0=None, t1=None, valor_canonico="   ")
    assert cargar_registro(escribir_registro(tmp_path, campos)).valor_canonico is None


# --- feedback apply (F11): la puerta que F09 dejo diferida ---


def _registro_minimo(tmp_path: Path, extra: str = "") -> Path:
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(
        "parametros:\n"
        "  - nombre: stop_fraccion_caja\n"
        "    categoria: estrategia\n"
        "    tipo: fraccion\n"
        "    unidad: fraccion de la caja\n"
        "    descripcion: nivel del stop\n"
        "    estado: UNKNOWN\n" + extra,
        encoding="utf-8",
        newline="\n",
    )
    return ruta


def _fb(**cambios: Any) -> dict[str, Any]:
    d = base(
        medio="escrito",
        grabacion=None,
        t0=None,
        t1=None,
        objetivo={"tipo": "parametro", "id": "stop_fraccion_caja"},
        accion="RESOLVE_UNKNOWN",
        valor_resultante="0,8",
    )
    d.update(cambios)
    return d


def test_apply_falla_sin_canonico_y_pasa_con_el(tmp_path: Path) -> None:
    """La coma decimal la rechaza el registro a proposito; `apply` no la traduce, la denuncia."""
    from botsito.config.registro import cargar_registro
    from botsito.feedback.aplicar import AplicarError, cambios_de_sesion

    registro = cargar_registro(_registro_minimo(tmp_path))
    sin = registro_desde_dict({**_fb(), "id": calcular_id(_fb())})
    with pytest.raises(AplicarError, match="numero invalido|invalido"):
        cambios_de_sesion(registro, [sin], sin.sesion)

    campos = _fb(valor_canonico="0.8")
    con = registro_desde_dict({**campos, "id": calcular_id(campos)})
    cambios = cambios_de_sesion(registro, [con], con.sesion)
    assert len(cambios) == 1 and cambios[0].valor_escrito == "0.8" and cambios[0].canonico


def test_apply_aborta_con_dos_registros_vigentes_sobre_el_mismo_parametro(tmp_path: Path) -> None:
    from botsito.config.registro import cargar_registro
    from botsito.feedback.aplicar import AplicarError, cambios_de_sesion

    registro = cargar_registro(_registro_minimo(tmp_path))
    a = _fb(valor_canonico="0.8")
    b = _fb(valor_canonico="0.75", respuesta_literal="otra cosa dijo")
    regs = [
        registro_desde_dict({**a, "id": calcular_id(a)}),
        registro_desde_dict({**b, "id": calcular_id(b)}),
    ]
    with pytest.raises(AplicarError, match="vigentes a la vez"):
        cambios_de_sesion(registro, regs, regs[0].sesion)


def test_apply_ignora_lo_superseded_y_aplica_lo_vigente(tmp_path: Path) -> None:
    from botsito.config.registro import cargar_registro
    from botsito.feedback.aplicar import cambios_de_sesion

    registro = cargar_registro(_registro_minimo(tmp_path))
    viejo_campos = _fb(valor_canonico="0.75")
    viejo = registro_desde_dict({**viejo_campos, "id": calcular_id(viejo_campos)})
    nuevo_campos = _fb(valor_canonico="0.8", supersede=viejo.id)
    nuevo = registro_desde_dict({**nuevo_campos, "id": calcular_id(nuevo_campos)})
    cambios = cambios_de_sesion(registro, [viejo, nuevo], nuevo.sesion)
    assert [c.valor_escrito for c in cambios] == ["0.8"]


def test_apply_no_escribe_un_parametro_que_no_sea_de_estrategia(tmp_path: Path) -> None:
    """Un parametro de entorno solo cambia por ADR (ADR-0004): el feedback no puede tocarlo."""
    from botsito.config.registro import cargar_registro
    from botsito.feedback.aplicar import AplicarError, cambios_de_sesion

    ruta = tmp_path / "p.yaml"
    ruta.write_text(
        "parametros:\n"
        "  - nombre: cuenta_objetivo\n"
        "    categoria: prop_firm\n"
        "    tipo: texto\n"
        "    unidad: tipo de cuenta\n"
        "    descripcion: cuenta\n"
        "    estado: UNKNOWN\n",
        encoding="utf-8",
        newline="\n",
    )
    campos = _fb(objetivo={"tipo": "parametro", "id": "cuenta_objetivo"}, valor_canonico="demo")
    r = registro_desde_dict({**campos, "id": calcular_id(campos)})
    with pytest.raises(AplicarError, match="solo se cambia por decision"):
        cambios_de_sesion(cargar_registro(ruta), [r], r.sesion)


def test_apply_conserva_los_comentarios_del_fichero(tmp_path: Path) -> None:
    """La cabecera de `parametros.yaml` documenta el esquema: un volcado la borraria."""
    from botsito.config.registro import cargar_registro
    from botsito.feedback.aplicar import cambios_de_sesion, escribir_cambios

    ruta = _registro_minimo(tmp_path)
    ruta.write_text("# cabecera que debe sobrevivir\n" + ruta.read_text(encoding="utf-8"),
                    encoding="utf-8", newline="\n")
    campos = _fb(valor_canonico="0.8")
    r = registro_desde_dict({**campos, "id": calcular_id(campos)})
    registro = cargar_registro(ruta)
    texto = escribir_cambios(ruta, cambios_de_sesion(registro, [r], r.sesion))
    assert texto.startswith("# cabecera que debe sobrevivir")
    assert "estado: CONFIRMED" in texto and 'valor: "0.8"' in texto and "tipo: feedback" in texto
