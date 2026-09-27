"""RN-004 lista para activarse con la respuesta a A-35 (rama trabajo/preparar-a35-a44): el
selector `liquidez_m15_pivote_formado` SIN FIJAR hace que el motor se niegue nombrando A-35; el
modo diagnostico corre con una lectura hipotetica y lo etiqueta todo; con cada lectura el pivote
esta disponible en el instante que esa lectura define y ni un minuto antes; la misma secuencia da
resultados distintos y predecibles con las dos lecturas; RN-004 dispara sobre un dia SINTETICO con
la spec REAL; sin mirar al futuro; y la invariancia de H3 sigue en pie con la lectura puesta."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.config.registro import Registro, cargar_registro
from botsito.data.agregacion import agregar
from botsito.data.velas import a_minuto
from botsito.domain.pivotes_m15 import BAJO, CIERRE_VELA_CONTRARIA, INICIO_VELA_CONTRARIA, LECTURAS
from botsito.domain.valores import Puntos
from botsito.domain.velas import MinutoUtc, Vela
from botsito.engine import diagnostico
from botsito.engine.diagnostico import (
    Diagnostico,
    DiagnosticoRechazadoError,
    SinFijarError,
    etiquetar,
    etiquetar_html,
    lectura_pivote,
    nombre_etiquetado,
)
from botsito.engine.interprete import Interprete, ReglaEjecutable, reglas_ejecutables
from botsito.engine.motor import (
    DatosMercado,
    DiaDeMercado,
    MotorSpec,
    ResultadoDia,
    Sesion,
    SinLecturaDePivoteError,
)
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

RAIZ = Path(__file__).resolve().parents[2]
SPEC = RAIZ / "knowledge" / "spec" / "strategy_spec.yaml"
HUSO = "Europe/Madrid"
SESIONES = (Sesion("07-11", "07:00", "11:00"), Sesion("11-15", "11:00", "15:00"))
DIA = date(2030, 1, 15)  # martes, invierno: 07:00 Madrid = 06:00Z
BASE = 110_000
INICIO = int(a_minuto(datetime(2030, 1, 15, 6, 0, tzinfo=UTC)))
FIN = int(a_minuto(datetime(2030, 1, 15, 14, 0, tzinfo=UTC)))
M15 = 15


@pytest.fixture(scope="module")
def registro() -> Registro:
    return cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")


@pytest.fixture(scope="module")
def reglas() -> list[ReglaEjecutable]:
    return list(reglas_ejecutables(cargar_reglas(SPEC)))


def _h4_alcista() -> list[Vela]:
    """Tres H4 cerradas antes de la ventana, la ultima rompe la maxima de la anterior: alcista."""
    inicio = int(a_minuto(datetime(2030, 1, 14, 10, 0, tzinfo=UTC)))
    velas = []
    for i, (lo, hi) in enumerate([(-300, -100), (-200, -50), (-150, 20)]):
        m = inicio + 240 * i
        velas.append(
            Vela(
                MinutoUtc(m),
                Puntos(BASE + lo + 10),
                Puntos(BASE + hi),
                Puntos(BASE + lo),
                Puntos(BASE + hi - 10),
                1,
                240,
                240,
            )
        )
    return velas


# Los bloques de M15 de la ventana, en orden desde las 06:00Z: (apertura, cierre, minimo). El
# sesgo es alcista, asi que la liquidez es el BAJO mas reciente ya formado.
#   B0, B1 rojas (flujo bajista; el minimo de la racha, 109790, esta en B1)
#   B2 verde: la CONTRARIA que marca el pivote BAJO en 109790
#   B3 verde, B4 roja que TOCA el nivel sin cruzarlo con el cuerpo, B5 roja que lo cruza con el
#   cuerpo: RN-004 dispara al cierre de B5
BLOQUES: list[tuple[int, int, int | None]] = [
    (BASE, BASE - 100, None),
    (BASE - 100, BASE - 200, BASE - 210),
    (BASE - 200, BASE - 150, None),
    (BASE - 150, BASE - 100, None),
    (BASE - 100, BASE - 200, BASE - 210),
    (BASE - 200, BASE - 300, None),
]
NIVEL = BASE - 210
CONTRARIA = 2
CRUZA = 5


def _bloque(n: int, apertura: int, cierre: int, minimo: int | None) -> list[Vela]:
    """Quince M1 que van linealmente de `apertura` a `cierre`; el minimo del bloque, si se pide,
    lo hace la M1 del medio con su mecha."""
    velas = []
    for k in range(M15):
        a = apertura + (cierre - apertura) * k // M15
        c = apertura + (cierre - apertura) * (k + 1) // M15
        lo = min(a, c) - 1
        if minimo is not None and k == 7:
            lo = min(lo, minimo)
        velas.append(
            Vela(
                MinutoUtc(INICIO + M15 * n + k),
                Puntos(a),
                Puntos(max(a, c) + 1),
                Puntos(lo),
                Puntos(c),
                1,
            )
        )
    return velas


# La misma secuencia, pero la vela CONTRARIA (B2) vuelve al nivel con su mecha antes de cerrar
# verde: aqui las dos lecturas de A-35 dejan trazas distintas (fase 1 de la verificacion).
BLOQUES_VUELVE: list[tuple[int, int, int | None]] = [
    (BASE, BASE - 100, None),
    (BASE - 100, BASE - 200, BASE - 210),
    (BASE - 200, BASE - 150, BASE - 215),
    (BASE - 150, BASE - 100, None),
    (BASE - 100, BASE - 200, BASE - 210),
    (BASE - 200, BASE - 300, None),
]


def _m1(
    hasta: int | None = None, bloques: list[tuple[int, int, int | None]] | None = None
) -> list[Vela]:
    """Las M1 de la ventana: los bloques disenados y, despues, bloques verdes suaves hasta el fin
    del dia. Con `hasta`, solo las M1 con inicio < hasta (para no mirar al futuro)."""
    bloques = BLOQUES if bloques is None else bloques
    velas: list[Vela] = []
    n = 0
    precio = BASE
    while INICIO + M15 * n < FIN:
        if n < len(bloques):
            a, c, lo = bloques[n]
        else:
            a, c, lo = precio, precio + 5, None
        velas += _bloque(n, a, c, lo)
        precio = c
        n += 1
    return [v for v in velas if hasta is None or int(v.inicio) < hasta]


def _datos(
    registro: Registro,
    lectura: str | None,
    hasta: int | None = None,
    bloques: list[tuple[int, int, int | None]] | None = None,
) -> DatosMercado:
    m1 = _m1(hasta, bloques)
    anclaje = registro.hora("anclaje_h4")
    return DatosMercado(_h4_alcista(), agregar(m1, M15, anclaje), m1, lectura)


def _motor(registro: Registro, reglas: list[ReglaEjecutable], desempate: Any = None) -> MotorSpec:
    voc = cargar_vocabulario(SPEC)
    if desempate is None:
        return MotorSpec(Interprete(voc, primitivas_escritas(registro)), reglas)
    return MotorSpec(Interprete(voc, primitivas_escritas(registro), desempate=desempate), reglas)


def _dia(datos: DatosMercado) -> DiaDeMercado:
    return DiaDeMercado(DIA, HUSO, SESIONES, datos)


def _fijados(r: ResultadoDia, hecho: str) -> list[int]:
    return [t for s in r.sesiones.values() for t, _, h, _ in s.fijados if h == hecho]


# ------------------------------------------------------------------------- el pivote en el dia


def test_cada_lectura_da_el_pivote_en_su_instante_y_ni_un_minuto_antes(registro: Registro) -> None:
    contraria_inicio = INICIO + M15 * CONTRARIA
    contraria_fin = contraria_inicio + M15
    esperado = {INICIO_VELA_CONTRARIA: contraria_inicio + 1, CIERRE_VELA_CONTRARIA: contraria_fin}
    for lectura in LECTURAS:
        datos = _datos(registro, lectura)
        primero = next(
            t for t in range(INICIO, contraria_fin + 1) if datos.liquidez_m15(t, BAJO) is not None
        )
        assert primero == esperado[lectura], lectura
        assert datos.liquidez_m15(primero - 1, BAJO) is None, lectura
        p = datos.liquidez_m15(primero, BAJO)
        assert p is not None and p.nivel == NIVEL and p.lado == BAJO
    # la misma secuencia, las dos lecturas: `inicio` lo ve catorce minutos antes que `cierre`
    assert esperado[CIERRE_VELA_CONTRARIA] - esperado[INICIO_VELA_CONTRARIA] == M15 - 1


def test_sin_mirar_al_futuro_con_cada_lectura(registro: Registro) -> None:
    """Recortar las M1 en `t` no cambia lo que la liquidez dice en ningun instante <= t."""
    for lectura in LECTURAS:
        completo = _datos(registro, lectura)
        for corte in (INICIO + M15 * CONTRARIA + 1, INICIO + M15 * CONTRARIA + 8, INICIO + M15 * 4):
            recortado = _datos(registro, lectura, hasta=corte)
            for t in range(INICIO, corte + 1):
                assert completo.liquidez_m15(t, BAJO) == recortado.liquidez_m15(t, BAJO), (
                    lectura,
                    corte,
                    t,
                )


def test_sin_lectura_no_hay_liquidez_y_rn004_sigue_no_implementada(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    datos = _datos(registro, None)
    with pytest.raises(SinLecturaDePivoteError, match="A-35"):
        datos.liquidez_m15(INICIO + 60, BAJO)
    r = _motor(registro, reglas).correr_dia(_dia(datos))
    traza = r.sesiones["07-11"]
    assert ("RN-004", "predicado:alcanza_nivel") in traza.no_implementadas
    assert "RN-004" not in traza.disparadas and not _fijados(r, "liquidez_tomada")
    # y los datos de siempre, solo con H4, siguen valiendo tal cual
    viejo = _motor(registro, reglas).correr_dia(_dia(DatosMercado(_h4_alcista())))
    assert ("RN-004", "predicado:alcanza_nivel") in viejo.sesiones["07-11"].no_implementadas


def test_rn004_dispara_con_la_spec_real_al_cierre_de_la_m15_que_cruza_con_cuerpo(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Con cualquiera de las dos lecturas: B4 toca el nivel sin cruzarlo (no dispara), B5 cierra
    por debajo con el cuerpo y RN-004 fija `liquidez_tomada` justo en su cierre. Las dos lecturas
    dan el MISMO instante aqui porque los toques cuentan desde el fin de la vela contraria; lo que
    las separa es cuando el pivote esta disponible (test anterior)."""
    cierre_b5 = INICIO + M15 * (CRUZA + 1)
    for lectura in LECTURAS:
        r = _motor(registro, reglas).correr_dia(_dia(_datos(registro, lectura)))
        traza = r.sesiones["07-11"]
        assert "RN-004" in traza.disparadas, lectura
        assert min(_fijados(r, "liquidez_tomada")) == cierre_b5, lectura
        assert not any(p == "predicado:alcanza_nivel" for _, p in traza.no_implementadas)
        assert not any(p == "predicado:cruza" for _, p in traza.no_implementadas)


def test_por_el_arnes_real_las_lecturas_dejan_trazas_distintas_si_el_precio_vuelve(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    """Fase 1 de la verificacion: la sesion completa pasa por `arnes.correr` con el motor real. La
    vela contraria (B2) vuelve al nivel con su mecha antes de cerrar verde. Con
    `inicio_vela_contraria` el pivote ya existia en su primera M1, asi que al cerrar B2 la ultima
    M15 cerrada puede tomarlo y `alcanza_nivel` da SI en ese cierre; con `cierre_vela_contraria`
    el pivote nace al cerrar B2 y el primer toque es el de B4. Las trazas difieren en la huella del
    selector (`liquidez_m15`, `liquidez_m15_alcanzada`). RN-004 dispara en el mismo cierre (B5) con
    las dos, porque la vela que marca el pivote no puede cerrar con cuerpo al otro lado del extremo
    que acaba de hacer: con la toma medida al cierre de M15 y con cuerpo, la diferencia esta en el
    toque, no en la toma (VERIFICACION-A35-A44.md, fases 1 y 2)."""
    from botsito.engine import arnes
    from botsito.engine.primitivas import ANOTACION_LIQUIDEZ, ANOTACION_LIQUIDEZ_ALCANZADA

    trazas = {}
    for lectura in LECTURAS:
        datos = _datos(registro, lectura, bloques=BLOQUES_VUELVE)
        dias = (arnes.DiaTrader("caso-x-2030-01-15", DIA.isoformat(), ()),)
        corrida = arnes.correr(
            "x", ("2030-01",), dias, {DIA.isoformat(): _dia(datos)}, _motor(registro, reglas)
        )
        trazas[lectura] = corrida.resultados[0].sesiones["07-11"]
    inicio, cierre = trazas[INICIO_VELA_CONTRARIA], trazas[CIERRE_VELA_CONTRARIA]
    b2_inicio = INICIO + M15 * CONTRARIA
    assert inicio.anotaciones[ANOTACION_LIQUIDEZ] == f"bajo {NIVEL} formado_en {b2_inicio + 1}"
    assert cierre.anotaciones[ANOTACION_LIQUIDEZ] == f"bajo {NIVEL} formado_en {b2_inicio + M15}"
    assert inicio.anotaciones[ANOTACION_LIQUIDEZ_ALCANZADA] == f"{NIVEL} en {b2_inicio + M15}"
    assert cierre.anotaciones[ANOTACION_LIQUIDEZ_ALCANZADA] == f"{NIVEL} en {INICIO + M15 * 5}"
    assert inicio.anotaciones != cierre.anotaciones
    cierre_b5 = INICIO + M15 * (CRUZA + 1)
    for t in (inicio, cierre):
        assert "RN-004" in t.disparadas
        assert min(i for i, _, h, _ in t.fijados if h == "liquidez_tomada") == cierre_b5
    # y sin que el precio vuelva en la contraria, las huellas del toque coinciden: es la vuelta
    # dentro de la contraria lo que el selector separa
    iguales = {}
    for lectura in LECTURAS:
        r = _motor(registro, reglas).correr_dia(_dia(_datos(registro, lectura)))
        iguales[lectura] = r.sesiones["07-11"].anotaciones[ANOTACION_LIQUIDEZ_ALCANZADA]
    assert iguales[INICIO_VELA_CONTRARIA] == iguales[CIERRE_VELA_CONTRARIA]


def test_la_invariancia_de_h3_sigue_con_la_lectura_puesta(
    registro: Registro, reglas: list[ReglaEjecutable]
) -> None:
    def inverso(r: ReglaEjecutable) -> str:
        return "".join(chr(0x10FFFF - ord(c)) for c in r.id)

    def huella(r: ResultadoDia) -> dict[str, Any]:
        return {
            s: (t.fijados, sorted(t.no_implementadas), sorted(t.bloqueadas), sorted(t.disparadas))
            for s, t in r.sesiones.items()
        }

    for lectura in LECTURAS:
        directo = huella(_motor(registro, reglas).correr_dia(_dia(_datos(registro, lectura))))
        invertido = huella(
            _motor(registro, reglas, inverso).correr_dia(_dia(_datos(registro, lectura)))
        )
        assert directo == invertido, lectura


# ------------------------------------------------------------------------- el diagnostico


def test_sin_fijar_el_motor_se_niega_nombrando_a35(registro: Registro) -> None:
    with pytest.raises(SinFijarError, match="A-35") as exc:
        lectura_pivote(registro)
    assert diagnostico.PARAMETRO_A35 in str(exc.value) and "diagnostico" in str(exc.value)
    assert lectura_pivote(registro, Diagnostico(a35=INICIO_VELA_CONTRARIA)) == INICIO_VELA_CONTRARIA


def test_con_el_valor_fijado_el_diagnostico_se_rechaza(tmp_path: Path) -> None:
    """Un registro sintetico con el selector ya CONFIRMED: la corrida cuenta y no admite el modo
    diagnostico (que la etiquetaria como si no contara)."""
    contenido = f"""
parametros:
  - nombre: {diagnostico.PARAMETRO_A35}
    categoria: estrategia
    tipo: enum
    unidad: cuando esta formado
    opciones: [inicio_vela_contraria, cierre_vela_contraria]
    descripcion: el selector, ya respondido en este registro de prueba
    estado: CONFIRMED
    valor: cierre_vela_contraria
    fuente: {{tipo: feedback, id: fb-2030-01-16-sesion-02-1a2b3c4d}}
"""
    ruta = tmp_path / "parametros.yaml"
    ruta.write_text(contenido, encoding="utf-8")
    fijado = cargar_registro(ruta)
    assert lectura_pivote(fijado) == CIERRE_VELA_CONTRARIA
    with pytest.raises(DiagnosticoRechazadoError, match="ya esta fijado"):
        lectura_pivote(fijado, Diagnostico(a35=INICIO_VELA_CONTRARIA))


def test_el_diagnostico_etiqueta_cada_linea_cada_fichero_y_cada_pagina() -> None:
    d = Diagnostico(a35=INICIO_VELA_CONTRARIA, a44="sin_tope")
    assert d.etiquetas == ("DIAGNOSTICO-A35-inicio_vela_contraria", "DIAGNOSTICO-A44-sin_tope")
    texto = etiquetar("uno\ndos\n\ntres\n", d.etiquetas)
    lineas = texto.split("\n")
    assert lineas[-1] == "" and all(ln.startswith("[DIAGNOSTICO-A35") for ln in lineas[:-1])
    assert "[DIAGNOSTICO-A44-sin_tope] " in lineas[0]
    assert etiquetar("x", ()) == "x"
    assert nombre_etiquetado(Path("a/informe.txt"), d.etiquetas) == Path(
        "a/informe.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.txt"
    )
    assert nombre_etiquetado(Path("a/informe.txt"), ()) == Path("a/informe.txt")
    pagina = etiquetar_html(
        "<html><head><title>Visor</title></head><body><p>x</p></body></html>", d.etiquetas
    )
    assert "<title>[DIAGNOSTICO-A35-inicio_vela_contraria DIAGNOSTICO-A44-sin_tope] Visor" in pagina
    assert pagina.index("DIAGNOSTICO-A35") < pagina.index("<p>x</p>")
    with pytest.raises(ValueError, match="A-35"):
        Diagnostico(a35="al_ojo")
    with pytest.raises(ValueError, match="A-44"):
        Diagnostico(a44="plausible")


def test_la_cli_se_niega_sin_lectura_y_no_escribe_nada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """La compuerta de construccion manda primero (medida se niega con su mensaje aunque se pida
    el diagnostico); un mes de construccion SIN el diagnostico se niega nombrando A-35 antes de
    leer una sola vela."""
    from botsito import cli

    real = cargar_criterio(RAIZ)
    salida = tmp_path / "informe.txt"
    mes = real.medida[0]
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", mes, "--salida", str(salida),
         "--diagnostico-a35", INICIO_VELA_CONTRARIA]
    )  # fmt: skip
    assert codigo == 2 and "MEDIDA" in capsys.readouterr().err
    construccion = real.construccion[0]
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", construccion, "--salida", str(salida)]
    )
    err = capsys.readouterr().err
    assert codigo == 2 and "A-35" in err and diagnostico.PARAMETRO_A35 in err
    assert not list(tmp_path.iterdir())
    for peticion in (["--caso", f"caso-x-{real.construccion[0]}-00"], ["--todos"]):
        codigo = cli.main(
            ["--repo", str(RAIZ), "motor", "visor", *peticion, "--salida", str(tmp_path / "v")]
        )
        assert codigo in (2, 3), peticion  # 2: sin lectura (o sin datos); 3: caso oculto
        assert not (tmp_path / "v").exists()


def test_por_la_cli_en_diagnostico_todo_sale_etiquetado_si_hay_datos(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Con `data/` en la maquina: el informe del arnes en diagnostico lleva la etiqueta en el
    nombre y en CADA linea, y no existe un fichero con el nombre pedido a secas."""
    from botsito import cli
    from botsito.cases.paquete import cargar_config
    from botsito.data.dataset import DatasetError, buscar_manifiesto

    real = cargar_criterio(RAIZ)
    mes = real.construccion[0]
    config = cargar_config(RAIZ / "knowledge" / "cases" / "kit" / "config.yaml")
    try:
        buscar_manifiesto(RAIZ, f"{config.dataset_prefijo}{mes}")
        cli._carpeta_datos(RAIZ)
    except (DatasetError, SystemExit):
        pytest.skip("sin las velas de construccion en esta maquina")
    salida = tmp_path / "informe.txt"
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", mes, "--salida", str(salida),
         "--diagnostico-a35", CIERRE_VELA_CONTRARIA, "--diagnostico-a44", "sin_tope",
         "--diagnostico-a21", "solo_una_zona_de_control"]
    )  # fmt: skip
    if codigo == 2 and "falta en disco" in capsys.readouterr().err:
        pytest.skip("sin las velas de construccion en esta maquina")
    assert codigo == 0
    etiquetado = (
        tmp_path / f"informe.DIAGNOSTICO.a35={CIERRE_VELA_CONTRARIA}.a44=sin_tope"
        ".a21=solo_una_zona_de_control.txt"
    )
    assert etiquetado.exists() and not salida.exists()
    lineas = etiquetado.read_text(encoding="utf-8").split("\n")
    prefijo = (
        f"[DIAGNOSTICO-A35-{CIERRE_VELA_CONTRARIA}][DIAGNOSTICO-A44-sin_tope]"
        "[DIAGNOSTICO-A21-solo_una_zona_de_control] "
    )
    assert all(ln.startswith(prefijo) for ln in lineas if ln)
    assert "sin valor para ninguna medida" in lineas[0]
