"""El arnes del motor (ADR-0048), sobre velas y dias SINTETICOS: el interprete del arbol, el motor
de un dia, la compuerta y el informe. Ningun dia real se lee aqui salvo el criterio commiteado,
para comprobar que el arnes se niega a medida y a lo que no es construccion."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.criterio_fidelidad import Criterio, Operacion, Tolerancias, cargar_criterio
from botsito.cases.holdout import HoldoutCerradoError
from botsito.cases.ventanas import MINUTOS_H4
from botsito.comun.yaml_estricto import YamlError
from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
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
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

RAIZ = Path(__file__).resolve().parents[2]
SPEC = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
DIA = date(2030, 1, 15)  # martes; ninguna fecha real


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def vocabulario() -> dict[str, dict[str, Any]]:
    return cargar_vocabulario(SPEC)


@pytest.fixture(scope="module")
def motor(registro: Registro, vocabulario: dict[str, dict[str, Any]]) -> MotorSpec:
    reglas = reglas_ejecutables(cargar_reglas(SPEC))
    return MotorSpec(Interprete(vocabulario, primitivas_escritas(registro)), reglas)


def _m1(hasta: datetime) -> list[Vela]:
    """M1 continuas y en zigzag desde seis dias antes: rompen extremos H4 en los dos sentidos."""
    velas: list[Vela] = []
    t = datetime(2030, 1, 9, tzinfo=UTC)
    base = 110_000
    i = 0
    while t < hasta:
        a = base + int(300 * math.sin(i / 97) + 120 * math.sin(i / 23)) + i // 50
        c = base + int(300 * math.sin((i + 1) / 97) + 120 * math.sin((i + 1) / 23)) + (i + 1) // 50
        alto, bajo = Puntos(max(a, c) + 3), Puntos(min(a, c) - 3)
        velas.append(Vela(a_minuto(t), Puntos(a), alto, bajo, Puntos(c), 1))
        t += timedelta(minutes=1)
        i += 1
    return velas


def _dia(registro: Registro, m1: list[Vela], dia: date = DIA) -> DiaDeMercado:
    h4 = agregar(m1, MINUTOS_H4, registro.hora("anclaje_h4"))
    return DiaDeMercado(dia, HUSO, SESIONES, DatosMercado(h4))


def _fin_del_dia() -> datetime:
    return datetime(DIA.year, DIA.month, DIA.day, 23, 0, tzinfo=UTC)


# --------------------------------------------------------------------------- el interprete


def _interprete_de_prueba(predicados: dict[str, Any]) -> Interprete:
    vocab: dict[str, dict[str, Any]] = {
        "predicados": {n: {"fuente": "mercado"} for n in ("si", "no", "falta")},
        "acciones": {"fijar": {}, "colocar": {"efecto": "abrir"}},
        "hechos": {"h": {"origen": "regla"}},
        "acumuladores": {},
        "efectos": {"abrir": {}},
        "tokens": {},
    }

    def fijar(args: Any, lig: Any, momento: Any, estado: EstadoDia) -> list[tuple[str, str]]:
        estado.hechos[str(args["hecho"])] = str(args["a"])
        return [(str(args["hecho"]), str(args["a"]))]

    def colocar(args: Any, lig: Any, momento: Any, estado: EstadoDia) -> list[tuple[str, str]]:
        estado.hechos["colocado"] = "si"
        return [("colocado", "si")]

    return Interprete(vocab, Primitivas(predicados, {"fijar": fijar, "colocar": colocar}, {}))


def _cte(valor: Tri) -> Any:
    return lambda args, momento, estado: Resultado(valor)


MOMENTO = Momento(MinutoUtc(0), "s", False, None)


def test_kleene_desconocido_no_decide_por_la_primitiva_que_falta() -> None:
    it = _interprete_de_prueba({"si": _cte(Tri.SI), "no": _cte(Tri.NO)})
    faltan: set[str] = set()

    def evaluar(nodo: dict[str, Any]) -> Tri:
        return it.evaluar(nodo, MOMENTO, EstadoDia(), faltan).valor

    assert evaluar({"todos_de": [{"no": {}}, {"falta": {}}]}) is Tri.NO
    assert evaluar({"todos_de": [{"si": {}}, {"falta": {}}]}) is Tri.DESCONOCIDO
    assert evaluar({"cualquiera_de": [{"falta": {}}, {"si": {}}]}) is Tri.SI
    assert evaluar({"cualquiera_de": [{"falta": {}}, {"no": {}}]}) is Tri.DESCONOCIDO
    assert evaluar({"ninguno_de": [{"falta": {}}]}) is Tri.DESCONOCIDO
    assert evaluar({"ninguno_de": [{"no": {}}]}) is Tri.SI
    assert faltan == {"predicado:falta"}


def test_una_regla_desconocida_no_fija_y_un_gate_desconocido_bloquea_su_efecto() -> None:
    it = _interprete_de_prueba({"si": _cte(Tri.SI), "no": _cte(Tri.NO)})
    reglas = [
        ReglaEjecutable("G", "gate", {"falta": {}}, {"prohibe": ["abrir"]}),
        ReglaEjecutable(
            "D1", "disparador", {"falta": {}}, {"hace": [{"fijar": {"hecho": "h", "a": "x"}}]}
        ),
        ReglaEjecutable("D2", "disparador", {"si": {}}, {"hace": [{"colocar": {}}]}),
    ]
    estado = EstadoDia()
    ev = it.evento(reglas, MOMENTO, estado)
    assert "h" not in estado.hechos and "colocado" not in estado.hechos
    assert ("G", "predicado:falta") in ev.no_implementadas
    assert ("D1", "predicado:falta") in ev.no_implementadas
    assert ("D2", "accion:colocar", "gate desconocido:abrir") in ev.bloqueadas


# ---------------------------------------------------------------------- el motor de un dia


def test_sin_mirar_al_futuro(registro: Registro, motor: MotorSpec) -> None:
    """Anadir velas posteriores al instante T no cambia nada de lo decidido hasta T."""
    corte = datetime(DIA.year, DIA.month, DIA.day, 10, 0, tzinfo=UTC)  # 11:00 en Madrid, enero
    t = a_minuto(corte)
    completo = motor.correr_dia(_dia(registro, _m1(_fin_del_dia())))
    cortado = motor.correr_dia(_dia(registro, _m1(corte)))

    def hasta_t(r: ResultadoDia) -> list[tuple[str, tuple[int, str, str, str]]]:
        return sorted((s, f) for s, tr in r.sesiones.items() for f in tr.fijados if f[0] <= t)

    assert hasta_t(completo) == hasta_t(cortado)
    assert hasta_t(completo), "el dia sintetico tiene que decidir algo antes del corte"
    assert completo.sesiones["07-11"].anotaciones == cortado.sesiones["07-11"].anotaciones
    datos = _dia(registro, _m1(_fin_del_dia())).datos
    assert all(v.fin <= t for v in datos.velas_h4_cerradas(t))


def test_no_implementada_detiene_la_sesion_y_queda_registrada(
    registro: Registro, motor: MotorSpec, vocabulario: dict[str, dict[str, Any]]
) -> None:
    r = motor.correr_dia(_dia(registro, _m1(_fin_del_dia())))
    assert r.operaciones == ()
    traza = r.sesiones["07-11"]
    assert ("RN-004", "predicado:alcanza_nivel") in traza.no_implementadas
    assert "liquidez_tomada" not in traza.hechos_producidos
    op = Operacion(
        DIA.isoformat(), "07-11", "compra", datetime(2030, 1, 15, 7, 30, tzinfo=UTC), Decimal("1.1")
    )
    corrida = arnes.Corrida(
        "spec", ("2030-01",), (arnes.DiaTrader("c", DIA.isoformat(), (op,)),), (r,)
    )
    texto = arnes.informe(corrida, _criterio(), vocabulario)
    assert "- predicado:alcanza_nivel: 1 de 1" in texto
    assert "liquidez_tomada:no[predicado:alcanza_nivel, predicado:cruza]" in texto


# ---------------------------------------------------------------------------- la compuerta


def _criterio() -> Criterio:
    return Criterio(
        Tolerancias(3, 15, 100_000), Fraction(7, 10), Fraction(6, 10), ("2030-01",), ("2030-02",)
    )


def test_se_niega_a_medida_y_a_lo_que_no_es_construccion() -> None:
    real = cargar_criterio(RAIZ)
    for mes in real.medida:
        with pytest.raises(arnes.ConjuntoError, match="MEDIDA"):
            arnes.validar_meses(real, [mes])
        with pytest.raises(arnes.ConjuntoError, match="MEDIDA"):
            arnes.dias_de_construccion(RAIZ, real, [mes])
    for mes in ("2026-02", "2026-03", "2026-09", "2030-01"):
        with pytest.raises(arnes.ConjuntoError, match="construccion"):
            arnes.validar_meses(real, [mes])
    with pytest.raises(arnes.ConjuntoError):
        arnes.validar_meses(real, [])


def test_centinela_un_dia_oculto_no_se_lee(tmp_path: Path) -> None:
    centinela = "CENTINELA-9f3c"
    dev = tmp_path / "knowledge" / "cases" / "dev"
    dev.mkdir(parents=True)
    oculto = "caso-x-2030-01-02"
    (dev / f"{oculto}.yaml").write_text(f"{centinela}: [roto\n", encoding="utf-8")
    asignaciones = {"2030-01": {oculto: "dev", "caso-x-2030-01-03": "dev"}}
    with pytest.raises(HoldoutCerradoError) as exc:
        arnes.dias_de_construccion(
            tmp_path, _criterio(), ["2030-01"], ocultos={oculto}, asignaciones=asignaciones
        )
    assert centinela not in str(exc.value) and "2030-01-02" not in str(exc.value)
    # el centinela esta vivo: sin la compuerta, ese fichero SI se habria leido y habria fallado
    with pytest.raises(YamlError):
        arnes.dias_de_construccion(
            tmp_path, _criterio(), ["2030-01"], ocultos=set(), asignaciones=asignaciones
        )


# --------------------------------------------------------------------------------- el informe


@dataclass
class _Copia:
    """Motor sintetico que copia al trader y dice haber producido todos los hechos."""

    ops: dict[str, tuple[Operacion, ...]]
    hechos: list[str]

    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia:
        propias = self.ops.get(dia.dia.isoformat(), ())
        trazas = {s.nombre: TrazaSesion() for s in dia.sesiones}
        for op in propias:
            trazas[op.sesion].fijados += [(0, "sintetico", h, "si") for h in self.hechos]
        return ResultadoDia(dia.dia.isoformat(), propias, trazas)


@dataclass
class _Quieto:
    def correr_dia(self, dia: DiaDeMercado) -> ResultadoDia:
        return ResultadoDia(
            dia.dia.isoformat(), (), {s.nombre: TrazaSesion() for s in dia.sesiones}
        )


def _dias_trader() -> tuple[arnes.DiaTrader, ...]:
    def op(dia: str, sesion: str, h: int, direccion: str, entrada: str) -> Operacion:
        return Operacion(
            dia,
            sesion,
            direccion,
            datetime.fromisoformat(f"{dia}T{h:02d}:05:00+00:00"),
            Decimal(entrada),
        )

    return (
        arnes.DiaTrader("c1", "2030-01-15", (op("2030-01-15", "07-11", 7, "compra", "1.10010"),)),
        arnes.DiaTrader(
            "c2",
            "2030-01-16",
            (
                op("2030-01-16", "07-11", 8, "venta", "1.10200"),
                op("2030-01-16", "11-15", 12, "compra", "1.10300"),
            ),
        ),
        arnes.DiaTrader("c3", "2030-01-17", ()),
    )


def _mercado(dias: tuple[arnes.DiaTrader, ...]) -> dict[str, DiaDeMercado]:
    return {
        d.dia: DiaDeMercado(date.fromisoformat(d.dia), HUSO, SESIONES, DatosMercado([]))
        for d in dias
    }


def test_un_motor_que_copia_al_trader_da_cien_por_cien_y_embudo_completo(
    vocabulario: dict[str, dict[str, Any]],
) -> None:
    dias = _dias_trader()
    hechos = [h for h, _ in arnes.hechos_de_regla(vocabulario)]
    motor = _Copia({d.dia: d.operaciones for d in dias}, hechos)
    corrida = arnes.correr("copia", ("2030-01",), dias, _mercado(dias), motor)
    texto = arnes.informe(corrida, _criterio(), vocabulario)
    assert "cobertura: 3/3 (100.0 %)" in texto
    assert "precision: 3/3 (100.0 %)" in texto
    for h in hechos:
        assert f"- {h}: 3 de 3" in texto
    assert "- operacion del bot: 3 de 3" in texto
    assert "cuantas se paran en cada primitiva NO_IMPLEMENTADA:\n- ninguna" in texto


def test_un_motor_que_no_opera_da_cobertura_cero_y_precision_sin_definir(
    vocabulario: dict[str, dict[str, Any]],
) -> None:
    dias = _dias_trader()
    corrida = arnes.correr("quieto", ("2030-01",), dias, _mercado(dias), _Quieto())
    medida = arnes.medida_de(corrida, _criterio())
    assert medida.cobertura == 0 and medida.precision is None
    texto = arnes.informe(corrida, _criterio(), vocabulario)
    assert "cobertura: 0/3 (0.0 %)" in texto
    assert "precision: sin definir (cero operaciones del bot puntuables)" in texto
    assert "precision: 0" not in texto and "precision: 100" not in texto


def test_determinismo_byte_a_byte(
    registro: Registro, motor: MotorSpec, vocabulario: dict[str, dict[str, Any]]
) -> None:
    dias = (arnes.DiaTrader("c1", DIA.isoformat(), _dias_trader()[0].operaciones),)
    mercado = {DIA.isoformat(): _dia(registro, _m1(_fin_del_dia()))}
    uno = arnes.informe(
        arnes.correr("spec", ("2030-01",), dias, mercado, motor), _criterio(), vocabulario
    )
    dos = arnes.informe(
        arnes.correr("spec", ("2030-01",), dias, mercado, motor), _criterio(), vocabulario
    )
    assert uno.encode("utf-8") == dos.encode("utf-8")


def test_la_cli_se_niega_sin_escribir_nada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli

    salida = tmp_path / "informe.txt"
    for mes in (*cargar_criterio(RAIZ).medida, "2026-03"):
        codigo = cli.main(
            ["--repo", str(RAIZ), "motor", "arnes", "--meses", mes, "--salida", str(salida)]
        )
        assert codigo == 2
        assert not salida.exists()
    assert "MEDIDA" in capsys.readouterr().err
