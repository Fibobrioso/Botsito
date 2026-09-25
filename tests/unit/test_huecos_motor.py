"""Los huecos del arnes (ADR-0049) sobre H4 SINTETICAS y la spec real.

H1: una sesion ambigua fija `sesgo` a `ambiguo` y RN-033 prohibe; una segunda sesion ambigua no
hereda el sesgo de la primera, ni una no ambigua la prohibicion de una ambigua -el hecho caduca al
abrir-; insuficiente prohibe; y, cuando `data/` esta en la maquina, la forma y la primitiva
coinciden en todas las sesiones de construccion. Mas las guardias nuevas: `vale`, `caduca`, los
`valores` de un hecho como tokens y `sentido` como ligadura.

H2: las sesiones de `kit/config.yaml` cubren exactamente [ventana_inicio, ventana_fin). H3: la
misma traza con el orden de cada clase invertido, y el aviso cuando dos reglas de la misma clase
dan SI en la misma pasada. Ninguna fecha real: el dia sintetico es de 2030.
"""

from __future__ import annotations

import copy
import dataclasses
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from fractions import Fraction
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pytest

from botsito.cases.criterio_fidelidad import Criterio, Tolerancias
from botsito.cases.paquete import cargar_config
from botsito.config.registro import Registro, cargar_registro
from botsito.data.dataset import DatasetError, buscar_manifiesto
from botsito.data.velas import a_minuto
from botsito.domain.sesgo import sesgo_h4
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import arnes
from botsito.engine.interprete import (
    EstadoDia,
    Interprete,
    Momento,
    Primitivas,
    ReglaEjecutable,
    Resultado,
    Tri,
    reglas_ejecutables,
)
from botsito.engine.motor import (
    DatosMercado,
    DiaDeMercado,
    MotorSpec,
    ResultadoDia,
    Sesion,
    TrazaSesion,
)
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import (
    FICHERO_SPEC,
    Regla,
    _nodos_hecho,
    cargar_reglas,
    cargar_vocabulario,
    comprobar_forma,
)

RAIZ = Path(__file__).resolve().parents[2]
SPEC = RAIZ / FICHERO_SPEC
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
# Martes de enero de 2030: Madrid es UTC+1, asi que las sesiones abren a las 06:00 y a las 10:00
# UTC, y la rejilla H4 (17:00 Nueva York) abre a las 22:00 UTC: velas 22-02, 02-06, 06-10...
DIA = date(2030, 1, 15)
APERTURA = {
    "07-11": datetime(2030, 1, 15, 6, tzinfo=UTC),
    "11-15": datetime(2030, 1, 15, 10, tzinfo=UTC),
}
PROHIBE_RN033 = frozenset({"buscar_entradas", "abrir_operacion"})
SIN_LADO = ("ambiguo", "insuficiente")


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def motor(registro: Registro) -> MotorSpec:
    reglas = reglas_ejecutables(cargar_reglas(SPEC))
    return MotorSpec(Interprete(cargar_vocabulario(SPEC), primitivas_escritas(registro)), reglas)


@pytest.fixture(scope="module")
def spec_real(
    registro: Registro,
) -> tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]]:
    tipos = {n: str(getattr(p.tipo, "value", p.tipo)) for n, p in registro.parametros.items()}
    return cargar_reglas(SPEC), cargar_vocabulario(SPEC), set(registro.nombres()), tipos


# ------------------------------------------------------------------------------- velas H4


def _h4(inicio: datetime, maxima: int, minima: int) -> Vela:
    return Vela(
        a_minuto(inicio),
        Puntos(minima + 20),
        Puntos(maxima),
        Puntos(minima),
        Puntos(maxima - 20),
        1,
        duracion_min=240,
        n_m1=240,
    )


def _velas(*pasos: str) -> list[Vela]:
    """H4 desde las 22:00 UTC de la vispera; cada paso dice que hace la vela respecto a la previa.

    `arriba` rompe solo el maximo, `abajo` solo el minimo, `ambos` los dos y `dentro` ninguno. La
    sesion 07-11 mira el primer paso (02-06 contra 22-02) y la 11-15 el segundo (06-10 contra
    02-06).
    """
    inicio = datetime(2030, 1, 14, 22, tzinfo=UTC)
    maxima, minima = 100_100, 99_900
    velas = [_h4(inicio, maxima, minima)]
    for i, paso in enumerate(pasos, start=1):
        if paso == "arriba":
            maxima, minima = maxima + 50, minima + 10
        elif paso == "abajo":
            maxima, minima = maxima - 10, minima - 50
        elif paso == "ambos":
            maxima, minima = maxima + 50, minima - 50
        elif paso == "dentro":
            maxima, minima = maxima - 10, minima + 10
        else:
            raise ValueError(paso)
        velas.append(_h4(inicio + timedelta(hours=4 * i), maxima, minima))
    return velas


def _dia(velas: list[Vela]) -> DiaDeMercado:
    return DiaDeMercado(DIA, HUSO, SESIONES, DatosMercado(velas))


def _apertura(sesion: str, velas: list[Vela]) -> Momento:
    return Momento(MinutoUtc(a_minuto(APERTURA[sesion])), sesion, True, DatosMercado(velas))


def _sesgo_de(traza: TrazaSesion) -> list[str]:
    return [v for _, r, h, v in traza.fijados if h == "sesgo" and r == "RN-003"]


# ------------------------------------------------------------------------------------- H1


def test_una_sesion_ambigua_fija_sesgo_ambiguo_y_rn033_prohibe(motor: MotorSpec) -> None:
    velas = _velas("ambos", "arriba")
    estado = EstadoDia()
    ev = motor.interprete.evento(motor.reglas, _apertura("07-11", velas), estado)
    assert ("RN-003", "sesgo", "ambiguo") in ev.fijados
    assert estado.hechos["sesgo"] == "ambiguo"
    assert "RN-033" in ev.disparadas and ev.prohibidos >= PROHIBE_RN033
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["07-11"]) == ["ambiguo"]
    assert "RN-033" in r.sesiones["07-11"].disparadas
    assert r.sesiones["07-11"].anotaciones["sesgo_h4"] == "ambiguo"


def test_una_segunda_sesion_ambigua_no_hereda_el_sesgo_de_la_primera(motor: MotorSpec) -> None:
    velas = _velas("arriba", "ambos")
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["07-11"]) == ["alcista"]
    assert _sesgo_de(r.sesiones["11-15"]) == ["ambiguo"]
    assert "RN-033" not in r.sesiones["07-11"].disparadas
    assert "RN-033" in r.sesiones["11-15"].disparadas
    # Con el sesgo de la primera sesion en pie, la apertura de la segunda lo caduca ANTES de la
    # primera pasada y fija el suyo: el estado acaba en `ambiguo`, no en `alcista`.
    estado = EstadoDia(hechos={"sesgo": "alcista"})
    ev = motor.interprete.evento(motor.reglas, _apertura("11-15", velas), estado)
    assert ev.caducados == ["sesgo"]
    assert estado.hechos["sesgo"] == "ambiguo" and "RN-033" in ev.disparadas


def test_una_sesion_no_ambigua_tras_una_ambigua_no_hereda_la_prohibicion(motor: MotorSpec) -> None:
    """Medido el 2026-09-25 antes de la caducidad: RN-033 disparaba en la apertura de la segunda
    sesion sobre el sesgo de la primera (24 sesiones de 84 en construccion, y solo 15 ambiguas)."""
    velas = _velas("ambos", "arriba")
    r = motor.correr_dia(_dia(velas))
    assert _sesgo_de(r.sesiones["11-15"]) == ["alcista"]
    assert "RN-033" not in r.sesiones["11-15"].disparadas
    estado = EstadoDia(hechos={"sesgo": "ambiguo"})
    ev = motor.interprete.evento(motor.reglas, _apertura("11-15", velas), estado)
    assert ev.caducados == ["sesgo"]
    assert "RN-033" not in ev.disparadas and not (PROHIBE_RN033 & ev.prohibidos)
    assert estado.hechos["sesgo"] == "alcista"


def test_insuficiente_prohibe(motor: MotorSpec) -> None:
    velas = _velas("dentro", "dentro")
    r = motor.correr_dia(_dia(velas))
    for sesion in ("07-11", "11-15"):
        assert _sesgo_de(r.sesiones[sesion]) == ["insuficiente"]
        assert "RN-033" in r.sesiones[sesion].disparadas
    ev = motor.interprete.evento(motor.reglas, _apertura("07-11", velas), EstadoDia())
    assert ev.prohibidos >= PROHIBE_RN033


def test_el_hecho_solo_caduca_en_la_apertura(motor: MotorSpec) -> None:
    velas = _velas("arriba", "arriba")
    estado = EstadoDia(hechos={"sesgo": "bajista"})
    dentro = Momento(
        MinutoUtc(a_minuto(APERTURA["07-11"]) + 5), "07-11", False, DatosMercado(velas)
    )
    ev = motor.interprete.evento(motor.reglas, dentro, estado)
    assert ev.caducados == [] and estado.hechos["sesgo"] == "bajista"
    assert motor.interprete.caducan_al_abrir == ("sesgo",)


def test_vale_en_el_nodo_hecho() -> None:
    vocab: dict[str, dict[str, Any]] = {
        "predicados": {},
        "acciones": {},
        "hechos": {"h": {"origen": "regla", "valores": ["x", "y"]}},
        "acumuladores": {},
        "efectos": {},
        "tokens": {},
    }
    it = Interprete(vocab, Primitivas({}, {}, {}))
    momento = Momento(MinutoUtc(0), "s", False, None)
    estado = EstadoDia(hechos={"h": "x"})
    assert it.evaluar({"hecho": "h", "vale": "x"}, momento, estado, set()).valor is Tri.SI
    assert it.evaluar({"hecho": "h", "vale": "y"}, momento, estado, set()).valor is Tri.NO
    assert it.evaluar({"hecho": "h"}, momento, estado, set()).valor is Tri.SI
    assert it.evaluar({"hecho": "h", "vale": "x"}, momento, EstadoDia(), set()).valor is Tri.NO


def test_la_forma_y_la_primitiva_coinciden_en_todas_las_sesiones_de_construccion(
    registro: Registro, motor: MotorSpec
) -> None:
    """Sobre las velas de `data/` (fuera de git): por la compuerta y leyendo solo velas, que no es
    abrir (ADR-0021 §1). Sin las velas en la maquina se salta, no se finge."""
    from botsito import cli
    from botsito.cases.criterio_fidelidad import cargar_criterio
    from botsito.cases.paquete import cargar_config
    from botsito.engine import arnes

    criterio = cargar_criterio(RAIZ)
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        carpeta = cli._carpeta_datos(RAIZ)
        for mes in criterio.construccion:
            buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{mes}")
    except (SystemExit, DatasetError) as exc:
        pytest.skip(f"sin las velas de construccion: {exc}")
    if not carpeta.is_dir():
        pytest.skip(f"sin carpeta de datos: {carpeta}")
    dias = arnes.dias_de_construccion(RAIZ, criterio, list(criterio.construccion))
    try:
        mercado = arnes.dias_de_mercado(
            RAIZ, carpeta, config, registro, dias, registro.texto("huso_operativa")
        )
    except (OSError, DatasetError) as exc:
        pytest.skip(f"sin las velas de construccion: {exc}")
    tope = registro.entero("sesgo_h4_tope_velas")
    criterio_ruptura = registro.opcion("sesgo_h4_criterio_ruptura")
    salidas: Counter[str] = Counter()
    for d in dias:
        dm = mercado[d.dia]
        r = motor.correr_dia(dm)
        for s in dm.sesiones:
            local = datetime.fromisoformat(f"{d.dia}T{s.desde}:00").replace(
                tzinfo=ZoneInfo(dm.huso)
            )
            t = MinutoUtc(a_minuto(local))
            esperado = sesgo_h4(
                dm.datos.velas_h4_cerradas(t), t, tope, criterio_ruptura
            ).sesgo.value
            assert _sesgo_de(r.sesiones[s.nombre]) == [esperado], (d.dia, s.nombre)
            assert ("RN-033" in r.sesiones[s.nombre].disparadas) == (esperado in SIN_LADO), (
                d.dia,
                s.nombre,
            )
            salidas[esperado] += 1
    assert sum(salidas.values()) == 2 * len(dias)
    assert salidas["alcista"] + salidas["bajista"] > 0, "sin velas de verdad no se compara nada"


# ------------------------------------------------------------------------- las guardias


def _fallos(
    spec: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> list[str]:
    reglas, voc, parametros, tipos = spec
    return comprobar_forma(reglas, voc, parametros, tipos=tipos)


def _con_forma(reglas: list[Regla], rid: str, forma: dict[str, Any]) -> list[Regla]:
    return [dataclasses.replace(r, forma=forma) if r.id == rid else r for r in reglas]


def _forma_de(reglas: list[Regla], rid: str) -> dict[str, Any]:
    forma = next(r for r in reglas if r.id == rid).forma
    assert isinstance(forma, dict), rid
    return copy.deepcopy(forma)


def test_la_spec_real_pasa_y_rn033_pregunta_por_sesgo_con_vale(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, _, _ = spec_real
    assert _fallos(spec_real) == []
    rn033 = next(r for r in reglas if r.id == "RN-033")
    assert rn033.clase == "gate" and rn033.vigente and isinstance(rn033.forma, dict)
    assert {n["vale"] for n in _nodos_hecho(rn033.forma["cuando"])} == set(SIN_LADO)
    assert voc["hechos"]["sesgo"]["caduca"] == "al_abrir_sesion"
    assert voc["hechos"]["sesgo"]["consume"] == ["RN-005", "RN-033"]
    assert "rompe" in voc["predicados"]  # declarado, sin ninguna regla que lo invoque


def test_vale_fuera_de_los_valores_o_sobre_un_hecho_sin_valores_falla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    forma = _forma_de(reglas, "RN-033")
    forma["cuando"]["cualquiera_de"][0]["vale"] = "permanente"  # token, pero no de `sesgo`
    fallos = comprobar_forma(_con_forma(reglas, "RN-033", forma), voc, parametros, tipos=tipos)
    assert any("RN-033" in f and "vale='permanente'" in f for f in fallos), fallos
    forma = _forma_de(reglas, "RN-033")
    forma["cuando"]["cualquiera_de"][0] = {"hecho": "orden_dimensionada", "vale": "ambiguo"}
    fallos = comprobar_forma(_con_forma(reglas, "RN-033", forma), voc, parametros, tipos=tipos)
    assert any("orden_dimensionada" in f and "no declara `valores`" in f for f in fallos), fallos


def test_un_valor_de_hecho_que_no_es_token_falla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["sesgo"]["valores"].append("raro")
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("hechos 'sesgo'" in f and "'raro'" in f for f in fallos), fallos


def test_sentido_como_token_no_pasa_en_un_predicado_con_lado_de_ruido(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    forma = _forma_de(reglas, "RN-005")
    forma["cuando"]["todos_de"][1]["se_desarrolla_en_el_lado_de_ruido"]["sentido"] = "ambiguo"
    fallos = comprobar_forma(_con_forma(reglas, "RN-005", forma), voc, parametros, tipos=tipos)
    assert any("RN-005" in f and "LIGADURA" in f for f in fallos), fallos


def test_caduca_exige_un_token_de_caducidad_y_solo_en_hechos_de_regla(
    spec_real: tuple[list[Regla], dict[str, dict[str, Any]], set[str], dict[str, str]],
) -> None:
    reglas, voc, parametros, tipos = spec_real
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["sesgo"]["caduca"] = "permanente"  # token de clase duracion, no caducidad
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("hechos 'sesgo'" in f and "caducidad" in f for f in fallos), fallos
    voc2 = copy.deepcopy(voc)
    voc2["hechos"]["operacion_abierta"]["caduca"] = "al_abrir_sesion"
    fallos = comprobar_forma(reglas, voc2, parametros, tipos=tipos)
    assert any("operacion_abierta" in f and "origen broker" in f for f in fallos), fallos


# ------------------------------------------------------------------------------------- H2


def test_las_sesiones_del_kit_cubren_exactamente_la_ventana_operativa(registro: Registro) -> None:
    """ADR-0049 H2 (a): las sesiones del motor salen de `kit/config.yaml` y la ventana de RN-001
    del registro. Los dos sitios siguen existiendo; esta guardia caza que se separen."""
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    inicio, fin = registro.hora("ventana_inicio"), registro.hora("ventana_fin")
    sesiones = list(config.sesiones)
    assert sesiones, "sin sesiones no hay motor"
    assert sesiones[0].desde == inicio.hora and sesiones[-1].hasta == fin.hora
    for anterior, siguiente in zip(sesiones, sesiones[1:], strict=False):
        assert anterior.hasta == siguiente.desde, (anterior, siguiente)  # ni hueco ni solape
    for s in sesiones:
        assert s.desde < s.hasta, s  # "HH:MM" se ordena como texto
    assert inicio.huso == fin.huso == registro.texto("huso_operativa")


# ------------------------------------------------------------------------------------- H3


def _inverso(r: ReglaEjecutable) -> str:
    """Un desempate que ordena los ids AL REVES que el del interprete."""
    return "".join(chr(0x10FFFF - ord(c)) for c in r.id)


def _huella(r: ResultadoDia) -> dict[str, Any]:
    return {
        s: (
            t.fijados,
            sorted(t.no_implementadas),
            sorted(t.bloqueadas),
            t.anotaciones,
            sorted(t.disparadas),
            sorted(t.empates),
        )
        for s, t in r.sesiones.items()
    }


def test_invariancia_al_orden_dentro_de_cada_clase(registro: Registro, motor: MotorSpec) -> None:
    """H3 (b): con el orden de cada clase invertido, la misma traza en todos los escenarios."""
    invertido = MotorSpec(
        Interprete(cargar_vocabulario(SPEC), primitivas_escritas(registro), desempate=_inverso),
        motor.reglas,
    )
    ids = [r.id for r in motor.reglas]
    assert sorted(ids, key=lambda i: _inverso(ReglaEjecutable(i, "gate", {}, {}))) == sorted(
        ids, reverse=True
    )
    escenarios = (
        ("ambos", "arriba"),
        ("arriba", "ambos"),
        ("dentro", "dentro"),
        ("abajo", "arriba"),
    )
    for pasos in escenarios:
        directo = _huella(motor.correr_dia(_dia(_velas(*pasos))))
        assert directo == _huella(invertido.correr_dia(_dia(_velas(*pasos)))), pasos
        assert any(t[0] for t in directo.values()), pasos  # el escenario decide algo


def test_dos_reglas_de_la_misma_clase_que_dan_si_a_la_vez_dejan_aviso() -> None:
    """H3 (c): el empate se anota ANTES de ejecutar la primera, sobre el mismo estado."""
    vocab: dict[str, dict[str, Any]] = {
        "predicados": {"si": {"fuente": "mercado"}, "sin_h": {"fuente": "mercado"}},
        "acciones": {"fijar": {}},
        "hechos": {"h": {"origen": "regla"}, "g": {"origen": "regla"}},
        "acumuladores": {},
        "efectos": {},
        "tokens": {},
    }

    def fijar(args: Any, lig: Any, momento: Any, estado: EstadoDia) -> list[tuple[str, str]]:
        estado.hechos[str(args["hecho"])] = "si"
        return [(str(args["hecho"]), "si")]

    def sin_h(args: Any, momento: Any, estado: EstadoDia) -> Resultado:
        return Resultado(Tri.NO if "h" in estado.hechos else Tri.SI)

    it = Interprete(
        vocab,
        Primitivas({"si": lambda a, m, e: Resultado(Tri.SI), "sin_h": sin_h}, {"fijar": fijar}, {}),
    )
    momento = Momento(MinutoUtc(0), "s", False, None)
    fija_h = {"hace": [{"fijar": {"hecho": "h", "a": "si"}}]}
    fija_g = {"hace": [{"fijar": {"hecho": "g", "a": "si"}}]}
    reglas = [
        ReglaEjecutable("D2", "disparador", {"si": {}}, fija_g),
        ReglaEjecutable("D1", "disparador", {"si": {}}, fija_h),
        ReglaEjecutable("G", "gate", {"si": {}}, {"prohibe": ["abrir"]}),
    ]
    ev = it.evento(reglas, momento, EstadoDia())
    assert ev.disparadas == ["G", "D1", "D2"]
    assert ev.empates == [("disparador", ("D1", "D2"))]
    # Encadenadas por un hecho no hay empate: D2 solo se da mientras D1 no haya fijado `h`, asi
    # que en la pasada de D1 las dos dan SI -eso es el aviso- pero con D2 condicionada al hecho
    # que D1 fija, deja de darse y no dispara: la spec resuelve el orden, no el desempate.
    reglas = [
        ReglaEjecutable("D1", "disparador", {"si": {}}, fija_h),
        ReglaEjecutable("D2", "disparador", {"sin_h": {}}, fija_g),
    ]
    ev = it.evento(reglas, momento, EstadoDia())
    assert ev.disparadas == ["D1"] and ev.empates == [("disparador", ("D1", "D2"))]
    reglas = [
        ReglaEjecutable("D1", "disparador", {"si": {}}, fija_h),
        ReglaEjecutable("D2", "disparador", {"todos_de": [{"hecho": "h"}]}, fija_g),
    ]
    ev = it.evento(reglas, momento, EstadoDia())
    assert ev.disparadas == ["D1", "D2"] and ev.empates == []


@dataclasses.dataclass
class _ConEmpate:
    """Motor sintetico que deja un aviso de H3 en la primera sesion."""

    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia:
        trazas = {s.nombre: TrazaSesion() for s in dia.sesiones}
        trazas["07-11"].empates.add(("disparador", ("RN-006", "RN-014")))
        return ResultadoDia(dia.dia.isoformat(), (), trazas)


def test_el_informe_lista_los_avisos_de_orden_y_el_motor_real_no_deja_ninguno(
    motor: MotorSpec,
) -> None:
    criterio = Criterio(
        Tolerancias(3, 15, 100_000), Fraction(7, 10), Fraction(6, 10), ("2030-01",), ("2030-02",)
    )
    voc = cargar_vocabulario(SPEC)
    dias = (arnes.DiaTrader("c1", DIA.isoformat(), ()),)
    mercado = {DIA.isoformat(): _dia(_velas("arriba", "arriba"))}
    texto = arnes.informe(
        arnes.correr("x", ("2030-01",), dias, mercado, _ConEmpate()), criterio, voc
    )
    assert "## Avisos de orden dentro de una clase (ADR-0049, H3)" in texto
    assert "- 2030-01-15 07-11: disparador RN-006, RN-014" in texto
    texto = arnes.informe(arnes.correr("spec", ("2030-01",), dias, mercado, motor), criterio, voc)
    assert "- ninguno: en ninguna sesion dieron SI dos reglas de la misma clase a la vez" in texto
    assert "- RN-003: 2 de 2; 0 de 0" in texto  # reglas disparadas sobre las sesiones corridas
