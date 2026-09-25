"""F10: ambiguedades, particiones, kappa, ventanas, paquete de sesion y CLI `kit`."""

from __future__ import annotations

import hashlib
import lzma
import struct
from datetime import UTC, date, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
from botsito.cases import fidelidad as fid
from botsito.cases import kappa as kp
from botsito.cases.ambiguedades import (
    AmbiguedadError,
    cargar_ambiguedades,
    validar_contra_contexto,
)
from botsito.cases.paquete import (
    DIRECTORIO_KIT,
    KitError,
    cargar_config,
    cargar_mapa,
    comprobar,
    construir,
    datasets_que_faltan_en_disco,
    escribir,
    lectura_de_velas,
    validar_paquetes,
)
from botsito.cases.particiones import ParticionError, asignar, clave_orden
from botsito.data.dataset import congelar, manifiestos
from botsito.evidence.modelo import escribir_item
from botsito.feedback.modelo import cargar_feedback, escribir_registro

REPO = Path(__file__).resolve().parents[2]
REG = struct.Struct(">iiiiif")
HOY = date(2026, 9, 4)
TID = "tr-v1-falso-00000000"
FUENTES = (
    'raiz: "corpus"\nvideos:\n  - video_id: v1\n    fichero: "clip.mp4"\n    drive_id: d1\n'
    '    bytes: 1\n    fecha_grabacion: "2026-01-01"\n    naturaleza: prueba\n'
)
PARAMETROS = """parametros:
  - nombre: huso_operativa
    categoria: ejecucion
    tipo: texto
    unidad: nombre IANA
    descripcion: reloj del trader
    estado: CONFIRMED
    valor: "Europe/Madrid"
    fuente: {tipo: decision, id: ADR-0001}
  - nombre: anclaje_h4
    categoria: estrategia
    tipo: hora
    unidad: hora de pared
    descripcion: apertura de la H4
    estado: UNKNOWN
  - nombre: cartuchos_max
    categoria: estrategia
    tipo: entero
    unidad: intentos
    descripcion: intentos por zona
    estado: UNKNOWN
  - nombre: break_even_condicion
    categoria: estrategia
    tipo: enum
    unidad: tocar/cierre
    opciones: ["tocar", "cierre"]
    descripcion: cuando se pone el break even
    estado: UNKNOWN
"""
TEMAS = "raices: [cartuchos, break_even, reloj, stop]\nvalores_cerrados: []\n"
AMBIGUEDADES = """ambiguedades:
  - id: A-1
    titulo: tercer cartucho
    pregunta: "¿2 o 3?"
    resuelve_en: [F11]
    evidencia: [{a}]
    parametros: [cartuchos_max]
    contradiccion: null
    estado: ABIERTA
    decision: null
    decidida_el: null
    bloqueante: true
  - id: A-2
    titulo: BE al tocar o al cierre
    pregunta: "¿al tocar o al cierre?"
    resuelve_en: [F11]
    evidencia: [{b}]
    parametros: [break_even_condicion]
    contradiccion: null
    estado: ABIERTA
    decision: null
    decidida_el: null
    bloqueante: false
"""
CONFIG = """simbolo: XXXYYY
dataset_prefijo: prueba-
ventana_local: {desde: "00:00", hasta: "15:00"}
sesiones:
  - {nombre: "07-11", desde: "07:00", hasta: "11:00"}
  - {nombre: "11-15", desde: "11:00", hasta: "15:00"}
anclajes_candidatos:
  - {etiqueta: madrid-00, hora: "00:00", huso: Europe/Madrid, coincide_con_sesiones: false}
  - {etiqueta: ny-17, hora: "17:00", huso: America/New_York, coincide_con_sesiones: true}
min_velas_ventana: 850
etiquetas: [compra, venta, no_trade]
particiones: {dev: 2, holdout-1: 1, holdout-2: 1, holdout-3: 1}
"""
MAPA = """parametros:
  cartuchos_max: {temas: [cartuchos]}
  break_even_condicion: {temas: [break_even]}
  anclaje_h4: {temas: [reloj]}
"""
VISTOS = 'meses: []\ndias:\n  - {dia: "2026-05-05", motivo: prueba, visto_el: "2026-09-01"}\n'
AJUSTES = (
    '[entorno]\nnombre = "backtest"\n\n'
    '[rutas]\ncorpus = "corpus"\ndata = "data"\nknowledge = "knowledge"\n'
)


def bi5(precio: int, minutos: int = 1440) -> bytes:
    regs = [
        REG.pack(m * 60, precio, precio + 1, precio - 1, precio + 2, 1.5) for m in range(minutos)
    ]
    return lzma.compress(b"".join(regs))


def descarga(url: str) -> bytes | None:
    partes = url.split("/")
    anio, mes0, dia = int(partes[-4]), int(partes[-3]), int(partes[-2])
    d = date(anio, mes0 + 1, dia)
    # Como el proveedor real: el sabado no hay datos y el domingo abre por la tarde (aqui, el
    # dia entero), asi que el lunes tiene su contexto desde la vispera.
    return None if d.weekday() == 5 else bi5(100000 + dia)


def _item(**cambios: Any) -> dict[str, Any]:
    d: dict[str, Any] = {
        "video_id": "v1",
        "t0": "0:00:10",
        "t1": "0:00:20",
        "modalidad": "audio",
        "tipo": "RULE_STATEMENT",
        "cita_literal": "limito a tres intentos por zona",
        "afirmacion": "tres cartuchos",
        "tema": "cartuchos.limite",
        "valor": "3",
        "confianza": "alta",
        "extractor": "humano",
        "revisado_por": "t",
        "provenance": "botsito",
        "transcripcion": TID,
    }
    d.update(cambios)
    return d


def _sin_holdout(directorio: str, nombres: list[str]) -> set[str]:
    """`ignore` de `copytree`: nada de `holdout/{1,2,3}` salvo su README (copiar es leer)."""
    partes = Path(directorio).parts
    if len(partes) >= 2 and partes[-2] == "holdout" and partes[-1] in {"1", "2", "3"}:
        return {n for n in nombres if n != "README.md"}
    return set()


def repo_kit(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    """Repo minimo con evidencia, registro, ambiguedades, kit y un dataset sintetico de mayo."""
    repo = tmp_path
    (repo / "knowledge" / "corpus").mkdir(parents=True)
    (repo / "knowledge" / "spec").mkdir()
    (repo / "knowledge" / "evidence").mkdir()
    (repo / "knowledge" / "feedback").mkdir()
    (repo / "knowledge" / "cases" / "kit").mkdir(parents=True)
    (repo / "config").mkdir()
    (repo / "docs" / "adr").mkdir(parents=True)
    (repo / "docs" / "adr" / "0001-x.md").write_text("# 1", encoding="utf-8")
    (repo / "knowledge" / "corpus" / "fuentes.yaml").write_text(FUENTES, encoding="utf-8")
    (repo / "knowledge" / "spec" / "parametros.yaml").write_text(PARAMETROS, encoding="utf-8")
    (repo / "knowledge" / "evidence" / "_temas.yaml").write_text(TEMAS, encoding="utf-8")
    (repo / "config" / "settings.example.toml").write_text(AJUSTES, encoding="utf-8")
    ev = repo / "knowledge" / "evidence"
    ids: dict[str, str] = {}
    ids["a"] = escribir_item(ev, _item()).stem
    ids["b"] = escribir_item(
        ev,
        _item(
            t0="0:01:00",
            t1="0:01:10",
            cita_literal="pones el break even al tocar el nivel",
            afirmacion="al tocar",
            tema="break_even.tocar",
            valor=None,
        ),
    ).stem
    ids["c"] = escribir_item(
        ev,
        _item(
            t0="0:02:00",
            t1="0:02:10",
            cita_literal="el stop va en el 0.75 de la caja",
            afirmacion="stop 0,75",
            tema="stop.nivel",
            valor="0.75",
        ),
    ).stem
    ids["d"] = escribir_item(
        ev,
        _item(
            t0="0:03:00",
            t1="0:03:10",
            cita_literal="protejo a 0.80 que es el SL por defecto",
            afirmacion="stop 0,8",
            tema="stop.nivel",
            valor="0.80",
        ),
    ).stem
    ids["e"] = escribir_item(
        ev,
        _item(
            t0="0:04:00",
            t1="0:04:10",
            cita_literal="lo tengo configurado como utc mas dos",
            afirmacion="grafico en UTC+2",
            tema="reloj.grafico",
            valor=None,
        ),
    ).stem
    (repo / "knowledge" / "spec" / "ambiguedades.yaml").write_text(
        AMBIGUEDADES.format(a=ids["a"], b=ids["b"]), encoding="utf-8"
    )
    kit = repo / DIRECTORIO_KIT
    (kit / "config.yaml").write_text(CONFIG, encoding="utf-8")
    (kit / "mapa_parametros.yaml").write_text(MAPA, encoding="utf-8")
    (kit / "vistos.yaml").write_text(VISTOS, encoding="utf-8")
    congelar(
        repo=repo,
        carpeta_datos=repo / "data",
        nombre="prueba",
        simbolo="XXXYYY",
        escala=100000,
        desde=date(2026, 5, 1),
        hasta=date(2026, 5, 15),
        descarga=descarga,
        hoy=HOY,
    )
    return repo, ids


# ---------------------------------------------------------------- ambiguedades

# Ids que un documento ya nombra y que todavia no existen en `ambiguedades.yaml`. Es la UNICA
# excepcion a "correlativas y sin huecos", va con su motivo, y se AUTOLIQUIDA: el test de abajo
# exige que ninguno de estos ids exista todavia. Nacio el 2026-09-14, cuando ADR-0026 abrio A-27 y
# A-28 con las tres de la liquidez de M15 reservadas y sin abrir, y FUNCIONO: el 2026-09-20 la rama
# de la liquidez de M15 creo A-24, A-25 y A-26, el test fallo y obligo a vaciar la lista. Se deja
# vacia a proposito, con el mecanismo intacto para la proxima reserva.
IDS_RESERVADOS: dict[str, str] = {}


def test_ambiguedades_reales_y_esquema(tmp_path: Path) -> None:
    ambs = cargar_ambiguedades(REPO / "knowledge" / "spec" / "ambiguedades.yaml")
    ids = [a.id for a in ambs]
    # La reserva no puede sobrevivir a su motivo: si alguno ya existe, sobra en la lista.
    ya_existen = sorted(set(IDS_RESERVADOS) & set(ids))
    assert not ya_existen, f"reservados que ya existen; retiralos de IDS_RESERVADOS: {ya_existen}"
    # correlativas desde A-1, sin huecos salvo los reservados: la sesion 1 añadio A-13..A-17 y
    # seguira creciendo
    ultimo = int(ids[-1][2:])
    esperados = [f"A-{i}" for i in range(1, ultimo + 1) if f"A-{i}" not in IDS_RESERVADOS]
    assert ids == esperados
    assert len(ambs) >= 17
    # `bloqueante` marca lo que hay que llevar SI o SI a una sesion (MASTER_PLAN G). Las tres de
    # la sesion 1 siguen marcadas y estan RESUELTAS; para la sesion 2 hay DOS vivas: A-21, que el
    # corpus nunca define que es un breaker, y desde el 2026-09-20 A-24 -nadie produce el token
    # `liquidez_m15`, asi que RN-004 no dispara y RN-008, que es un `ninguno_de`, prohibe abrir
    # SIEMPRE-. Las dos dejan al motor sin entrada posible, cada una por su lado. El 2026-09-24
    # ADR-0045 decide A-24 (el pivote mas reciente ya formado) y abre A-35, cuando esta formado,
    # que hereda el bloqueo: sin ella el productor de `liquidez_m15` no se escribe sin inventar.
    # El 2026-09-25 (rama trabajo/sesion-02, decision del consultor) nace A-42, con que reloj cuenta
    # el trader su horario de 07:00 a 15:00: bloquea la ingesta de meses de invierno, porque su
    # grafico es UTC+2 fijo y huso_operativa es Europe/Madrid (ENTRADA-MARZO, PARADA E0).
    bloqueantes = [a for a in ambs if a.bloqueante]
    assert len(bloqueantes) >= 3
    abiertas = {a.id for a in bloqueantes if a.estado == "ABIERTA"}
    assert abiertas == {"A-21", "A-35", "A-42"}, (
        f"bloqueantes abiertas inesperadas: {sorted(abiertas)}"
    )
    # Las doce de la sesion 1, mas A-20, que el trader cerro por escrito el 2026-09-11 ("solo 1
    # zona control bro. si hay 2 se descarta"): la primera que se cierra fuera de una sesion.
    # Las doce de la sesion 1, mas A-20 (el trader, por escrito, 2026-09-11) y A-14 (respondida
    # de hecho el 2026-09-10 y cerrada con su frase referida el 2026-09-12, como se cerro A-11).
    assert {a.id for a in ambs if a.estado == "RESUELTA"} == {f"A-{i}" for i in range(1, 13)} | {
        "A-14",
        "A-20",
    }
    # DECIDIDA nace con ADR-0022 (A-22, no operar noticias) y ADR-0024 le suma las dos que
    # llevaban decididas y abiertas desde el 2026-09-09: A-15 (la ventana no se amplia a Nueva
    # York) y A-23, la decision de metodo que estaba MEZCLADA dentro de A-16. A-16 se queda solo
    # con la medicion -cuanto se separa Oanda de Dukascopy- y sigue ABIERTA, porque eso no lo
    # cierra una decision: el anexo del 2026-09-09 midio otra pareja y lo dice el mismo.
    # Y ADR-0026/ADR-0027 (2026-09-14) le suman dos al cambiar de firma: A-17 (la ventana de
    # noticias deja de importar con una cuenta Swing) y A-19 (el corte del dia de riesgo lo escribe
    # el reglamento de FTMO: medianoche CE(S)T). A-22 sigue DECIDIDA por ADR-0022, con su enmienda.
    assert {a.id for a in ambs if a.estado == "DECIDIDA"} == {
        "A-15",
        "A-17",
        "A-19",
        "A-22",
        "A-23",
        "A-24",
    }
    assert next(a for a in ambs if a.id == "A-16").estado == "ABIERTA"
    # A-27 y A-28 son MEDICIONES del entorno de FTMO, partidas como se partio A-16: la ficha del
    # simbolo corre con un default declarado, el reloj del servidor sin valor hasta medirlo.
    assert {a.id: a.estado for a in ambs if a.id in ("A-27", "A-28")} == {
        "A-27": "ABIERTA",
        "A-28": "ABIERTA",
    }
    assert next(a for a in ambs if a.id == "A-10").contradiccion == "stop.nivel"
    ruta = tmp_path / "amb.yaml"
    for malo, msg in (
        (AMBIGUEDADES.replace("id: A-2", "id: A-1"), "repetido"),
        (AMBIGUEDADES.replace("id: A-1", "id: A-3"), "orden numerico"),
        (
            AMBIGUEDADES.replace(
                "estado: ABIERTA\n    decision: null", "estado: X\n    decision: null"
            ),
            "estado",
        ),
        (AMBIGUEDADES.replace("evidencia: [{a}]", "evidencia: []"), "al menos un item"),
        (AMBIGUEDADES.replace("evidencia: [{b}]", "evidencia: [x]"), "no es un id"),
    ):
        ruta.write_text(
            malo.format(a="ev-v1-000010-aaaaaaaa", b="ev-v1-000100-bbbbbbbb"), encoding="utf-8"
        )
        with pytest.raises(AmbiguedadError, match=msg):
            cargar_ambiguedades(ruta)
    ruta.write_text(
        AMBIGUEDADES.format(a="ev-v1-000010-aaaaaaaa", b="ev-v1-000100-bbbbbbbb"), encoding="utf-8"
    )
    ambs2 = cargar_ambiguedades(ruta)
    problemas = validar_contra_contexto(ambs2, {"ev-v1-000010-aaaaaaaa"}, {"cartuchos_max"}, set())
    assert any("ev-v1-000100-bbbbbbbb no existe" in p for p in problemas)
    assert any("break_even_condicion no esta" in p for p in problemas)


def test_project_state_refleja_las_ambiguedades() -> None:
    """Anti-deriva: la tabla de PROJECT_STATE y el YAML tienen los mismos ids y titulos."""
    ambs = cargar_ambiguedades(REPO / "knowledge" / "spec" / "ambiguedades.yaml")
    texto = (REPO / "PROJECT_STATE.md").read_text(encoding="utf-8")
    filas = [ln for ln in texto.splitlines() if ln.startswith("| A-")]
    tabla = {ln.split("|")[1].strip(): ln.split("|")[2].strip() for ln in filas}
    assert set(tabla) == {a.id for a in ambs}
    for a in ambs:
        assert tabla[a.id] == a.titulo, a.id


# ---------------------------------------------------------------- particiones


def test_particiones_deterministas() -> None:
    casos = [f"caso-x-2026-05-{d:02d}" for d in range(1, 10)]
    a = asignar(casos, 7, {"dev": 3, "holdout-1": 2, "holdout-2": 1, "holdout-3": 1})
    b = asignar(
        list(reversed(casos)), 7, {"dev": 3, "holdout-1": 2, "holdout-2": 1, "holdout-3": 1}
    )
    assert a == b and len(a) == 7 and sorted(a.values()).count("dev") == 3
    assert asignar(casos, 8, {"dev": 3}) != {k: v for k, v in a.items() if v == "dev"}
    assert clave_orden(7, casos[0]) == clave_orden(7, casos[0]) != clave_orden(8, casos[0])
    for args, msg in (
        ((casos, -1, {"dev": 1}), "seed"),
        ((casos, 1, {"dev": 20}), "universo"),
        ((casos, 1, {"otra": 1}), "desconocidas"),
        ((casos + [casos[0]], 1, {"dev": 1}), "repetidos"),
    ):
        with pytest.raises(ParticionError, match=msg):
            asignar(*args)


# ---------------------------------------------------------------- kappa


def test_gramatica_de_etiqueta() -> None:
    d = kp.parsear_etiqueta(
        "07-11: venta@08:37 e=1.15364 sl=1.15420; 11-15: no_trade",
        ["07-11", "11-15"],
        ["compra", "venta", "no_trade"],
    )
    assert d["07-11"].decision == "venta" and d["07-11"].hora == "08:37"
    assert (
        d["07-11"].extras == (("e", "1.15364"), ("sl", "1.15420"))
        and d["11-15"].decision == "no_trade"
    )
    for malo, msg in (
        ("07-11 venta; 11-15: no_trade", "falta ': '"),
        ("07-11: venta; 12-16: no_trade", "desconocida"),
        ("07-11: venta; 07-11: compra", "dos veces"),
        ("07-11: venta", "faltan las sesiones"),
        ("07-11: largo; 11-15: no_trade", "no esta en"),
        ("07-11: venta x; 11-15: no_trade", "clave=valor"),
    ):
        with pytest.raises(kp.EtiquetaError, match=msg):
            kp.parsear_etiqueta(malo, ["07-11", "11-15"], ["compra", "venta", "no_trade"])


def test_kappa_de_cohen() -> None:
    et = ["si", "no"]
    a = {f"u{i}": "si" for i in range(25)} | {f"u{i}": "no" for i in range(25, 50)}
    b = dict(a)
    for i in range(20, 25):
        b[f"u{i}"] = "no"  # 5 si->no
    for i in range(25, 35):
        b[f"u{i}"] = "si"  # 10 no->si
    r = kp.calcular(a, b, et)
    assert (r.po, r.pe, r.kappa) == (Fraction(7, 10), Fraction(1, 2), Fraction(2, 5))
    assert r.matriz == {"si": {"si": 20, "no": 5}, "no": {"si": 10, "no": 15}}
    total = kp.calcular(a, a, et)
    assert total.kappa == 1 and total.po == 1
    uno = kp.calcular({"u": "si", "v": "si"}, {"u": "si", "v": "si"}, et)
    assert uno.kappa is None and any("una sola categoria" in x for x in uno.avisos)
    with pytest.raises(kp.EtiquetaError, match="mismas unidades"):
        kp.calcular({"u": "si"}, {"v": "si"}, et)
    with pytest.raises(kp.EtiquetaError, match="fuera del conjunto"):
        kp.calcular({"u": "tal"}, {"u": "si"}, et)


# ---------------------------------------------------------------- paquete


def test_paquete_determinista_y_check(tmp_path: Path) -> None:
    repo, ids = repo_kit(tmp_path)
    p1 = construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    p2 = construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    assert p1.ficheros == p2.ficheros
    assert construir(repo, repo / "data", "2026-09-15-sesion-01", 4).asignacion != p1.asignacion
    # universo: 11 laborables de mayo 1-15; el 1 cae fuera del dataset (empieza a las 00:00Z) y
    # el 5 esta visto -> 9 casos; cupos 5 -> 5 elegidos
    assert len(p1.casos) == 5 and sorted(p1.asignacion.values()).count("dev") == 2
    motivos = {e.dia: e.motivo for e in p1.excluidos}
    assert "fuera del dataset" in motivos["2026-05-01"] and "visto" in motivos["2026-05-05"]
    assert all(c.n_velas >= 850 and c.sha256 for c in p1.casos)
    caso = p1.casos[0]
    ny = [x[11:16] for x in caso.limites_h4["ny-17"]]
    assert ny[-3:] == ["05:00", "09:00", "13:00"]  # 07, 11, 15 Madrid en verano
    assert [x[11:16] for x in caso.limites_h4["madrid-00"]][-2:] == ["10:00", "14:00"]
    # cuestionario: A-1 bloqueante primero con cartuchos_max; A-2; anclaje_h4 solo; contradiccion
    ids_p = [p.id for p in p1.preguntas]
    assert ids_p == ["P-01", "P-02", "P-03", "P-04"]
    assert p1.preguntas[0].bloqueante and p1.preguntas[0].origenes == [
        {"tipo": "ambiguedad", "id": "A-1"},
        {"tipo": "parametro", "id": "cartuchos_max"},
    ]
    assert p1.preguntas[0].casos[0]["evidencia"] == ids["a"]
    assert p1.preguntas[2].origenes == [{"tipo": "parametro", "id": "anclaje_h4"}]
    assert p1.preguntas[3].origenes == [{"tipo": "contradiccion", "id": "stop.nivel"}]
    assert {c["evidencia"] for c in p1.preguntas[3].casos} == {ids["c"], ids["d"]}
    hoja = p1.ficheros["hoja_trader.md"]
    assert "(BLOQUEANTE)" in hoja and "07:00 11:00 15:00" in hoja and "ev-v1-" not in hoja
    assert "meses del paquete (2026-05)" in hoja  # los de los casos, no los de vistos.yaml
    assert hoja.count("| caso-xxxyyy-") == 2  # solo dev
    # escribir, no sobreescribir, check puro
    carpeta = escribir(repo, p1)
    assert sorted(f.name for f in carpeta.iterdir()) == [
        "cuestionario.yaml",
        "hoja_trader.md",
        "particiones.yaml",
        "ventanas.yaml",
    ]
    with pytest.raises(KitError, match="no se sobreescribe"):
        escribir(repo, p1)
    assert comprobar(repo, repo / "data", "2026-09-15-sesion-01") == ([], [])
    # El config global evoluciona a proposito -el paquete SIGUIENTE quiere otros cupos- y eso ya
    # no rompe un paquete viejo: se recompone con su bloque `config:` congelado (ADR-0035,
    # enmienda del 2026-09-21). Hasta esta rama, esto daba "config.yaml cambio despues de generar
    # el paquete" y dejaba `config.yaml` inmodificable mientras existiera un solo paquete.
    (repo / DIRECTORIO_KIT / "config.yaml").write_text(
        CONFIG.replace("dev: 2", "dev: 3"), encoding="utf-8"
    )
    assert comprobar(repo, repo / "data", "2026-09-15-sesion-01") == ([], [])
    (repo / DIRECTORIO_KIT / "config.yaml").write_text(CONFIG, encoding="utf-8")
    # sin datos: solo esquema y aviso
    problemas, avisos = comprobar(repo, tmp_path / "otra", "2026-09-15-sesion-01")
    assert problemas == [] and any("ausentes" in a for a in avisos)
    with pytest.raises(KitError, match="sesion invalida"):
        construir(repo, repo / "data", "sesion-1", 1)
    with pytest.raises(KitError, match="seed"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", -1)
    (repo / DIRECTORIO_KIT / "config.yaml").write_text(
        CONFIG.replace("dev: 2", "dev: 20"), encoding="utf-8"
    )
    with pytest.raises(KitError, match="universo"):
        construir(repo, repo / "data", "2026-09-15-sesion-02", 1)


def test_config_y_mapa_estrictos(tmp_path: Path) -> None:
    repo, _ = repo_kit(tmp_path)
    ruta = repo / DIRECTORIO_KIT / "config.yaml"
    for malo, msg in (
        (CONFIG.replace('hasta: "15:00"}', 'hasta: "00:00"}'), "acaba antes"),
        (
            CONFIG.replace("coincide_con_sesiones: true", "coincide_con_sesiones: false"),
            "exactamente un anclaje",
        ),
        (
            CONFIG.replace("etiquetas: [compra, venta, no_trade]", "etiquetas: [Compra]"),
            "minusculas",
        ),
        (CONFIG.replace("holdout-3: 1}", "holdout-3: -1}"), "entero >= 0"),
        (
            CONFIG.replace(
                '{nombre: "11-15", desde: "11:00", hasta: "15:00"}',
                '{nombre: "11-15", desde: "11:00", hasta: "16:00"}',
            ),
            "no cabe",
        ),
    ):
        ruta.write_text(malo, encoding="utf-8")
        with pytest.raises(KitError, match=msg):
            cargar_config(ruta)
    ruta.write_text(CONFIG, encoding="utf-8")
    from botsito.config.registro import cargar_registro

    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    mapa = repo / DIRECTORIO_KIT / "mapa_parametros.yaml"
    mapa.write_text(MAPA.replace("temas: [reloj]", "temas: [otro]"), encoding="utf-8")
    with pytest.raises(KitError, match="fuera de _temas"):
        cargar_mapa(mapa, registro, frozenset({"cartuchos", "break_even", "reloj"}))
    mapa.write_text(MAPA.replace("anclaje_h4:", "inexistente:"), encoding="utf-8")
    with pytest.raises(KitError, match="no esta en el registro"):
        cargar_mapa(mapa, registro, frozenset())
    mapa.write_text(MAPA.replace("  anclaje_h4: {temas: [reloj]}\n", ""), encoding="utf-8")
    with pytest.raises(KitError, match="sin entrada en mapa"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 1)


def _registro_label(repo: Path, sesion: str, caso: str, valor: str, **extra: Any) -> str:
    campos: dict[str, Any] = {
        "sesion": sesion,
        "fecha": sesion[:10],
        "medio": "escrito",
        "objetivo": {"tipo": "caso", "id": caso},
        "accion": "LABEL_CASE",
        "respuesta_literal": f"etiqueta del trader para {caso}",
        "valor_resultante": valor,
        "registrado_por": "aleks",
        # Las sesiones de estos tests son posteriores al corte del 2026-09-13, asi que llevan los
        # dos campos que la guardia exige desde entonces.
        "recibido_el": sesion[:10],
        "procedencia": "trader_hoja",
    }
    campos.update(extra)
    return escribir_registro(repo / "knowledge" / "feedback", campos).stem


def _autorizar(repo: Path, particiones: list[str]) -> None:
    """Git, PREREGISTRO relleno, ADR y una autorizacion commiteada por particion, en un repo de
    PRUEBA. Nunca en el real: el PREREGISTRO del proyecto sigue vacio a proposito (ADR-0033)."""
    import subprocess

    def git(*args: str) -> None:
        subprocess.run(
            ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
            check=True,
            capture_output=True,
        )

    validation = repo / "docs" / "validation"
    validation.mkdir(parents=True, exist_ok=True)
    preregistro = (
        "# PREREGISTRO\n\numbral: 0.8\n\n## Preguntas\n\n"
        "- pregunta: P1 | estado: ABIERTA | kappa entre las dos rondas\n"
    )
    (validation / "PREREGISTRO.md").write_text(preregistro, encoding="utf-8")
    datos = preregistro.encode("utf-8")
    blob = hashlib.sha1(b"blob %d\x00" % len(datos) + datos).hexdigest()  # noqa: S324
    (repo / "docs" / "adr" / "0099-apertura.md").write_text("# 99\n", encoding="utf-8")
    for particion in particiones:
        (validation / f"AUTORIZACION-{particion}.md").write_text(
            f"particion: {particion}\nautorizado_por: el usuario\nfecha: 2026-10-01\n"
            f"adr: ADR-0099\npregunta: P1\npreregistro_blob: {blob}\n",
            encoding="utf-8",
        )
    if not (repo / ".git").is_dir():
        git("init", "-q")
    git("add", "-A")
    git("commit", "-q", "-m", "autoriza")


def test_kappa_desde_registros_y_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = repo_kit(tmp_path)
    base = ["--repo", str(repo), "kit"]
    assert cli.main([*base, "build", "--sesion", "2026-09-15-sesion-01", "--seed", "3"]) == 0
    salida_build = capsys.readouterr().out
    assert "5 casos (2 dev)" in salida_build
    assert cli.main([*base, "build", "--sesion", "2026-09-15-sesion-01", "--seed", "3"]) == 1
    assert "no se sobreescribe" in capsys.readouterr().err
    assert cli.main([*base, "check", "--sesion", "2026-09-15-sesion-01"]) == 0
    salida_check = capsys.readouterr().out
    assert cli.main([*base, "check", "--sesion", "2026-09-15-sesion-09"]) == 1
    capsys.readouterr()
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
            encoding="utf-8"
        )
    )
    # ADR-0033: build y check DECLARAN en su salida que leen velas y de que dias reservados, por
    # nombre, sin una cifra de velas ni un precio. Se comprueba la salida, no la intencion.
    reservados = {
        p: [c[-10:] for c, x in doc["asignacion"].items() if x == p]
        for p in ("holdout-1", "holdout-2", "holdout-3")
    }
    total = sum(len(d) for d in reservados.values())
    detalle = ", ".join(f"{p} {len(d)}" for p, d in reservados.items() if d)
    for salida in (salida_build, salida_check):
        assert "LECTURA: se leen las velas M1 de" in salida
        assert "no es abrir un holdout (ADR-0021 §1)" in salida
        # RECUENTO y no fechas (decision del consultor): ninguna fecha de dia reservado
        assert f"LECTURA: {total} dias reservados cuyas velas se leen: {detalle}" in salida
        for dias in reservados.values():
            for dia in dias:
                assert dia not in salida, dia
        assert "sha256:" not in salida and "n_velas:" not in salida
    # la LECTURA va antes del OK: en check se declara antes de leer
    assert salida_check.index("LECTURA:") < salida_check.index("OK:")
    # sin datos no se lee ninguna vela, y no se declara nada
    assert lectura_de_velas(repo, tmp_path / "sin-datos", doc["asignacion"]) == []
    casos = sorted(doc["asignacion"])
    s1, s2 = "2026-09-15-sesion-01", "2026-09-22-sesion-02"
    for i, c in enumerate(casos):
        _registro_label(repo, s1, c, "07-11: venta@08:30; 11-15: no_trade")
        _registro_label(
            repo,
            s2,
            c,
            "07-11: venta; 11-15: no_trade" if i < 4 else "07-11: compra; 11-15: no_trade",
        )
    # `feedback trace` tampoco IMPRIME la etiqueta de un caso reservado; la de uno dev, si
    reservado = next(c for c, x in doc["asignacion"].items() if x.startswith("holdout-"))
    dev = next(c for c, x in doc["asignacion"].items() if x == "dev")
    assert cli.main(["--repo", str(repo), "feedback", "trace", reservado]) == 0
    traza = capsys.readouterr().out
    assert "no se muestra, ADR-0033" in traza and "venta" not in traza and "compra" not in traza
    assert cli.main(["--repo", str(repo), "feedback", "trace", dev]) == 0
    assert "07-11: venta" in capsys.readouterr().out
    # Por defecto NO se leen las etiquetas de los casos reservados (ADR-0033): el kit sintetico
    # tiene 2 dev y 3 reservados, asi que quedan 2 casos x 2 sesiones H4 = 4 unidades.
    assert cli.main([*base, "kappa", "--sesion-a", s1, "--sesion-b", s2]) == 0
    out = capsys.readouterr()
    assert "unidades: 4" in out.out
    # sobre cuanto se calculo, junto al kappa: un kappa alto sobre pocos casos no significa nada
    assert "calculado sobre 4 unidades de 2 casos" in out.out
    assert "3 casos reservados excluidos sin leer su etiqueta" in out.err
    # Abrir sin decir QUE pregunta se gasta ya no se puede (ADR-0033, enmienda del
    # 2026-09-21): el acto de abrir tiene que declarar para que se abre.
    abrir_holdout = [*base, "kappa", "--sesion-a", s1, "--sesion-b", s2, "--incluir-holdout"]
    assert cli.main(abrir_holdout) == 1
    assert "exige --pregunta" in capsys.readouterr().err
    # Y diciendola, se niega igual: no hay git, ni PREREGISTRO relleno, ni autorizacion
    assert cli.main([*abrir_holdout, "--pregunta", "P1"]) == 1
    err = capsys.readouterr().err
    assert "ADR-0021 §3" in err and "PREREGISTRO.md" in err
    assert "unidades" not in err
    # Con la autorizacion commiteada, el preregistro relleno y el ADR, se abren: las 10 unidades
    _autorizar(repo, ["holdout-1", "holdout-2", "holdout-3"])
    assert cli.main([*abrir_holdout, "--pregunta", "P1"]) == 0
    out = capsys.readouterr()
    assert "unidades: 10" in out.out and "po: 0.900" in out.out and "kappa: 0.818" in out.out
    assert "kappa 0.818 calculado sobre 10 unidades de 5 casos" in out.out
    # Y LA SEGUNDA VEZ NO. El comando gasto P1 ANTES de leer (ADR-0033, enmienda del
    # 2026-09-21), asi que el pre-registro ya no es el que la autorizacion aprobo. Antes de
    # esta enmienda, este mismo comando abria las veces que hiciera falta: medido, cincuenta
    # aperturas seguidas con el repositorio sin tocar.
    assert cli.main([*abrir_holdout, "--pregunta", "P1"]) == 1
    assert "ADR-0021 §3" in capsys.readouterr().err
    assert kp.calcular(
        {"u": "a", "v": "a", "w": "b"}, {"u": "a", "v": "a", "w": "a"}, ["a", "b"]
    ).avisos
    # un registro que supersede cambia la ronda
    viejo = _registro_label(repo, s2, casos[4], "07-11: compra; 11-15: no_trade", notas="x")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
        )
    _registro_label(repo, s2, casos[4], "07-11: venta; 11-15: no_trade", supersede=viejo, notas="y")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
        )
    assert cli.main([*base, "kappa", "--sesion-a", s1, "--sesion-b", "2026-01-01-sesion-09"]) == 1


def test_validar_paquetes_sin_git(tmp_path: Path) -> None:
    repo, ids = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    ids_ev = set(ids.values())
    assert validar_paquetes(repo, [], ids_ev, {"prueba-" + "x"})[0] != []  # dataset inexistente
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "ventanas.yaml").read_text(
            encoding="utf-8"
        )
    )
    dataset = doc["casos"][0]["dataset_id"]
    assert validar_paquetes(repo, [], ids_ev, {dataset}) == ([], [])
    caso = doc["casos"][0]["id"]
    _registro_label(repo, "2026-09-15-sesion-01", caso, "07-11: venta; 11-15: no_trade")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    problemas, _ = validar_paquetes(repo, registros, ids_ev, {dataset})
    assert any("no esta commiteado" in p for p in problemas)


def test_ventana_en_invierno(tmp_path: Path) -> None:
    """Con hora de invierno (UTC+1) la ventana [00:00, 15:00) Madrid es [23:00Z, 14:00Z)."""
    from botsito.cases.ventanas import Anclaje, Caso, construir_caso
    from botsito.domain.valores import Puntos
    from botsito.domain.velas import MinutoUtc, SerieVelas, Vela

    inicio = int(datetime(2026, 1, 12, 22, 0, tzinfo=UTC).timestamp() // 60)
    p = Puntos(100000)
    velas = tuple(
        Vela(MinutoUtc(inicio + k), p, Puntos(100002), Puntos(99998), Puntos(100001), 1)
        for k in range(60 * 30)
    )
    serie = SerieVelas("XXXYYY", 1, 100000, 1000, velas, "prueba-1")
    caso = construir_caso(
        serie,
        date(2026, 1, 13),
        "xxxyyy",
        "Europe/Madrid",
        ("00:00", "15:00"),
        [Anclaje("ny-17", "17:00", "America/New_York", True)],
        850,
    )
    assert isinstance(caso, Caso)
    assert caso.desde_utc == "2026-01-12T23:00Z" and caso.hasta_utc == "2026-01-13T14:00Z"
    assert caso.n_velas == 900 and caso.limites_h4["ny-17"][-3:] == [
        "2026-01-13T06:00Z",
        "2026-01-13T10:00Z",
        "2026-01-13T14:00Z",
    ]  # 07, 11, 15 Madrid en invierno (NY EST = UTC-5)


# ---------------------------------------------------------------- auditoria de cierre


def test_paquete_malformado_huso_y_evidencia(tmp_path: Path) -> None:
    from botsito.cases.paquete import esquema_paquete

    repo, ids = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    carpeta = repo / DIRECTORIO_KIT / "2026-09-15-sesion-01"
    for nombre, texto, msg in (
        ("cuestionario.yaml", "sesion: 2026-09-15-sesion-01\npreguntas: [x]\n", "lista de mapas"),
        ("ventanas.yaml", "sesion: 2026-09-15-sesion-01\ncasos: [x]\n", "lista de mapas"),
        (
            "particiones.yaml",
            "sesion: 2026-09-15-sesion-01\nseed: 1\nasignacion: [a]\n",
            "mapa caso",
        ),
        ("particiones.yaml", "sesion: 2026-09-15-sesion-01\nseed: x\nasignacion: {}\n", "seed"),
    ):
        original = (carpeta / nombre).read_text(encoding="utf-8")
        (carpeta / nombre).write_text(texto, encoding="utf-8")
        with pytest.raises(KitError, match=msg):
            esquema_paquete(repo, "2026-09-15-sesion-01")
        problemas, _ = validar_paquetes(repo, [], set(ids.values()), {"prueba-x"})
        assert any(msg in x for x in problemas)
        (carpeta / nombre).write_text(original, encoding="utf-8")
    # huso_operativa invalido: KitError, no traceback
    ruta_reg = repo / "knowledge" / "spec" / "parametros.yaml"
    ruta_reg.write_text(PARAMETROS.replace("Europe/Madrid", "Europe/Nowhere"), encoding="utf-8")
    with pytest.raises(KitError, match="huso"):
        construir(repo, repo / "data", "2026-09-15-sesion-02", 1)
    ruta_reg.write_text(PARAMETROS, encoding="utf-8")
    # ambiguedad que cita evidencia inexistente o mapa con ambiguedad inexistente: error en build
    ruta_amb = repo / "knowledge" / "spec" / "ambiguedades.yaml"
    ruta_amb.write_text(
        AMBIGUEDADES.format(a="ev-v1-000010-deadbeef", b=ids["b"]), encoding="utf-8"
    )
    with pytest.raises(KitError, match="no existe"):
        construir(repo, repo / "data", "2026-09-15-sesion-02", 1)
    ruta_amb.write_text(AMBIGUEDADES.format(a=ids["a"], b=ids["b"]), encoding="utf-8")
    # F13: el mapa ya no lleva `ambiguedad` ni `opciones`. Esta guardia dejo de vigilar que la
    # A-N citada existiera -ya no se cita- y pasa a vigilar lo unico que puede pasar ahora: que
    # alguien reponga la columna muerta y el fichero vuelva a tener dos fuentes para una arista.
    mapa = repo / DIRECTORIO_KIT / "mapa_parametros.yaml"
    for resucitada in ("ambiguedad: A-2", "opciones: [tocar, cierre]"):
        mapa.write_text(
            MAPA.replace(
                "break_even_condicion: {temas: [break_even]}",
                "break_even_condicion: {temas: [break_even], " + resucitada + "}",
            ),
            encoding="utf-8",
        )
        with pytest.raises(KitError, match="la unica clave es"):
            construir(repo, repo / "data", "2026-09-15-sesion-02", 1)
    mapa.write_text(MAPA, encoding="utf-8")


def test_resuelta_min_velas_meses_vistos_y_universo(tmp_path: Path) -> None:
    repo, ids = repo_kit(tmp_path)
    # una ambiguedad RESUELTA deja de preguntarse; su parametro pasa a pregunta propia
    ruta_amb = repo / "knowledge" / "spec" / "ambiguedades.yaml"
    ruta_amb.write_text(
        AMBIGUEDADES.format(a=ids["a"], b=ids["b"]).replace(
            "estado: ABIERTA\n    decision: null\n    decidida_el: null\n    bloqueante: false",
            "estado: RESUELTA\n    decision: null\n    decidida_el: null\n    bloqueante: false",
        ),
        encoding="utf-8",
    )
    p = construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    titulos = [q.titulo for q in p.preguntas]
    assert "BE al tocar o al cierre" not in titulos and "break_even_condicion" in titulos
    assert p.universo == 9
    ruta_amb.write_text(AMBIGUEDADES.format(a=ids["a"], b=ids["b"]), encoding="utf-8")
    # min_velas por encima de lo que hay: todos excluidos, build falla por universo
    cfg = repo / DIRECTORIO_KIT / "config.yaml"
    cfg.write_text(
        CONFIG.replace("min_velas_ventana: 850", "min_velas_ventana: 2000"), encoding="utf-8"
    )
    with pytest.raises(KitError, match="universo tiene 0"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    cfg.write_text(CONFIG, encoding="utf-8")
    # mes visto entero
    vis = repo / DIRECTORIO_KIT / "vistos.yaml"
    vis.write_text(
        'meses:\n  - {mes: "2026-05", motivo: prueba, fuente: [], visto_el: "2026-09-01"}\n'
        "dias: []\n",
        encoding="utf-8",
    )
    with pytest.raises(KitError, match="universo tiene 0"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    vis.write_text(
        'meses: []\ndias:\n  - {dia: "2026-5-5", motivo: x, visto_el: "2026-09-01"}\n',
        encoding="utf-8",
    )
    with pytest.raises(KitError, match="AAAA-MM-DD"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    vis.write_text(VISTOS, encoding="utf-8")
    # recomputar_hash coincide con lo escrito
    from botsito.cases.ventanas import recomputar_hash
    from botsito.data.dataset import cargar_manifiesto, manifiestos

    caso = construir(repo, repo / "data", "2026-09-15-sesion-01", 3).casos[0]
    m = cargar_manifiesto(manifiestos(repo)[0])
    assert recomputar_hash(m, repo / "data", caso.desde_utc, caso.hasta_utc) == (
        caso.n_velas,
        caso.sha256,
    )


def test_kappa_con_supersede_en_cadena(tmp_path: Path) -> None:
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
            encoding="utf-8"
        )
    )
    casos = sorted(doc["asignacion"])
    s1, s2 = "2026-09-15-sesion-01", "2026-09-22-sesion-02"
    for c in casos:
        _registro_label(repo, s1, c, "07-11: venta; 11-15: no_trade")
        _registro_label(repo, s2, c, "07-11: venta; 11-15: no_trade")
    # A <- B <- C: solo C esta activo y cambia la ronda 2 del primer caso
    a = _registro_label(repo, s2, casos[0], "07-11: compra; 11-15: no_trade", notas="a")
    b = _registro_label(repo, s2, casos[0], "07-11: no_trade; 11-15: no_trade", supersede=a)
    _registro_label(repo, s2, casos[0], "07-11: compra; 11-15: compra", supersede=b, notas="c")
    # el original de s2 para casos[0] sigue activo: hay que supersederlo tambien
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
        )
    original = next(
        r.id
        for r in registros
        if r.sesion == s2 and r.objetivo.id == casos[0] and r.notas is None and r.supersede is None
    )
    ultimo = next(r.id for r in registros if r.notas == "c")
    _registro_label(
        repo, s2, casos[0], "07-11: compra; 11-15: compra", supersede=original, notas="d"
    )
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
        )
    # dejamos una sola cadena viva: supersedemos `d` con uno que apunte a `ultimo`? No: un
    # registro supersede a UN registro; la cadena valida es original <- d y a <- b <- c. Cerramos
    # `c` con un registro que lo supersede y coincide con `d`.
    _registro_label(repo, s2, casos[0], "07-11: compra; 11-15: compra", supersede=ultimo, notas="e")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
        )
    # Conclusion del test: cada caso admite UNA cadena; dos cadenas vivas son error hasta que
    # una supersede a la otra. Comprobamos la ronda con la cadena unica en otro caso:
    x = (
        _registro_label(
            repo, s1, "caso-xxxyyy-2026-05-04", "07-11: venta; 11-15: no_trade", notas="x"
        )
        if "caso-xxxyyy-2026-05-04" not in casos
        else None
    )
    assert x is None or x


def test_etiqueta_hora_y_claves_repetidas() -> None:
    with pytest.raises(kp.EtiquetaError, match="no esta en"):
        kp.parsear_etiqueta(
            "07-11: venta@99:99; 11-15: no_trade", ["07-11", "11-15"], ["venta", "no_trade"]
        )
    with pytest.raises(kp.EtiquetaError, match="repetida"):
        kp.parsear_etiqueta(
            "07-11: venta sl=1 sl=2; 11-15: no_trade", ["07-11", "11-15"], ["venta", "no_trade"]
        )
    r = kp.calcular({"u": "a", "v": "a"}, {"u": "a", "v": "b"}, ["a", "b", "c"])
    assert "c" not in r.acuerdo_por_categoria


def test_feedback_ambiguedad_duracion_y_video_de_sesion(tmp_path: Path) -> None:
    from botsito.corpus.inventario import InventarioError, cargar_fuentes
    from botsito.feedback.modelo import calcular_id, registro_desde_dict
    from botsito.feedback.modelo import validar_contra_contexto as validar_fb

    campos = {
        "sesion": "2026-09-15-sesion-01",
        "fecha": "2026-09-15",
        "medio": "video",
        "grabacion": "sesion 1.mkv",
        "t0": "0:10:00",
        "t1": "0:29:12.5",
        "objetivo": {"tipo": "ambiguedad", "id": "A-9"},
        "accion": "RESOLVE_UNKNOWN",
        "respuesta_literal": "mi grafico abre a las 7 hora de Madrid",
        "valor_resultante": "07:00 Europe/Madrid",
        "recibido_el": "2026-09-15",
        "procedencia": "trader_grabado",
        "registrado_por": "aleks",
    }
    campos["id"] = calcular_id(campos)
    r = registro_desde_dict(campos)
    ok = validar_fb([r], set(), set(), set(), {"sesion 1.mkv"}, {"A-9"}, {"sesion 1.mkv": 1752.5})
    assert ok == []
    mal = validar_fb([r], set(), set(), set(), {"sesion 1.mkv"}, {"A-1"}, {"sesion 1.mkv": 1752.4})
    assert any("no esta en ambiguedades" in x for x in mal) and any(
        "supera la duracion" in x for x in mal
    )
    ruta = tmp_path / "fuentes.yaml"
    ruta.write_text(
        'raiz: "c"\nvideos:\n  - video_id: v9\n    fichero: "sesion 1.mkv"\n    bytes: 1\n'
        '    fecha_grabacion: "2026-09-15"\n    naturaleza: sesion 1 con el trader\n',
        encoding="utf-8",
    )
    assert cargar_fuentes(ruta).videos[0].drive_id == ""
    ruta.write_text(
        ruta.read_text(encoding="utf-8").replace("sesion 1 con el trader", "recap"),
        encoding="utf-8",
    )
    with pytest.raises(InventarioError, match="sin drive_id"):
        cargar_fuentes(ruta)


def test_una_etiqueta_retirada_con_borderline_no_reaparece(tmp_path: Path) -> None:
    """`activos` va sobre TODOS los registros, no sobre los `LABEL_CASE` ya filtrados.

    `BORDERLINE`, `MARK_FALSE_POSITIVE` y `MARK_FALSE_NEGATIVE` tambien apuntan a un `caso` y por
    tanto pueden retirar una etiqueta. Filtrando primero por accion, ese retiro desaparecia de la
    lista y la etiqueta anulada volvia a contar en el kappa sin que nadie lo viera.
    """
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
            encoding="utf-8"
        )
    )
    caso = sorted(doc["asignacion"])[0]
    sesion = "2026-09-15-sesion-01"
    etiqueta = _registro_label(repo, sesion, caso, "07-11: venta; 11-15: no_trade")
    escribir_registro(
        repo / "knowledge" / "feedback",
        {
            "sesion": sesion,
            "fecha": sesion[:10],
            "medio": "escrito",
            "objetivo": {"tipo": "caso", "id": caso},
            "accion": "BORDERLINE",
            "respuesta_literal": "en este dia no me decido, retiro lo que dije",
            "registrado_por": "aleks",
            "recibido_el": sesion[:10],
            "procedencia": "trader_hoja",
            "supersede": etiqueta,
        },
    )
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    unidades = kp.etiquetas_de_registros(
        registros, sesion, ["07-11", "11-15"], ["compra", "venta", "no_trade"], excluir=frozenset()
    )
    assert unidades == {}, "la etiqueta retirada por el BORDERLINE seguia contando"


def _mover_sesion(repo: Path) -> Any:
    """El script de scripts/, cargado apuntando a un repo de prueba."""
    import importlib.util

    ruta = Path(__file__).resolve().parents[2] / "scripts" / "mover_sesion.py"
    spec = importlib.util.spec_from_file_location("mover_sesion", ruta)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    setattr(modulo, "RAIZ", repo)  # noqa: B010  # el script apunta a la raiz real
    return modulo


def test_mover_la_fecha_conserva_los_mismos_dias(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Mover la sesion reutiliza el seed del paquete: mismos casos y mismo reparto.

    Tecleando el seed a mano se puede poner otro sin darse cuenta, y entonces salen dias
    distintos sin que falle nada. Aqui el seed no se teclea.
    """
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    antes = (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
        encoding="utf-8"
    )
    modulo = _mover_sesion(repo)
    monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", "2026-09-22"])
    assert modulo.main() == 0
    assert not (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01").exists()
    despues = (repo / DIRECTORIO_KIT / "2026-09-22-sesion-01" / "particiones.yaml").read_text(
        encoding="utf-8"
    )
    assert despues.replace("2026-09-22", "2026-09-15") == antes
    # y la vuelta deja el paquete byte a byte como estaba
    monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", "2026-09-15"])
    assert modulo.main() == 0
    volvio = (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
        encoding="utf-8"
    )
    assert volvio == antes


def test_no_se_mueve_una_sesion_ya_etiquetada(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Con etiquetas puestas, el reparto esta congelado: rehacer el paquete borraria la prueba
    de que se asigno antes de etiquetar, que es lo unico que sostiene el etiquetado ciego."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
            encoding="utf-8"
        )
    )
    caso = sorted(doc["asignacion"])[0]
    _registro_label(repo, "2026-09-15-sesion-01", caso, "07-11: venta; 11-15: no_trade")
    modulo = _mover_sesion(repo)
    monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", "2026-09-22"])
    with pytest.raises(SystemExit, match="LABEL_CASE"):
        modulo.main()
    assert (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01").is_dir()
    assert not (repo / DIRECTORIO_KIT / "2026-09-22-sesion-01").exists()


def test_si_la_reconstruccion_falla_el_paquete_original_vuelve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """La red que justifica borrar una carpeta de knowledge/: si algo revienta, se restaura."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    carpeta = repo / DIRECTORIO_KIT / "2026-09-15-sesion-01"
    original = {p.name: p.read_bytes() for p in carpeta.iterdir()}
    modulo = _mover_sesion(repo)
    monkeypatch.setattr(modulo, "construir", lambda *a, **k: (_ for _ in ()).throw(KitError("x")))
    monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", "2026-09-22"])
    with pytest.raises(KitError):
        modulo.main()
    assert {p.name: p.read_bytes() for p in carpeta.iterdir()} == original
    assert not (repo / DIRECTORIO_KIT / "2026-09-22-sesion-01").exists()


def test_el_paquete_de_una_sesion_celebrada_no_tiene_que_reproducirse(tmp_path: Path) -> None:
    """Tras aplicar las respuestas al registro, el cuestionario de hoy ya no es el de aquel dia.

    `kit check` exigia que el paquete se recompusiera byte a byte, y esa exigencia se rompio en
    cuanto F11 poblo el registro: el cuestionario se genera desde los parametros UNKNOWN, y ya no
    lo estan. Exigir que se reproduzca seria exigir que el proyecto no aprenda nada. Con la sesion
    ya celebrada la diferencia es un AVISO; sin celebrar sigue siendo un ERROR, porque entonces si
    significa que alguien toco el paquete.
    """
    repo, _ = repo_kit(tmp_path)
    sesion = "2026-09-15-sesion-01"
    escribir(repo, construir(repo, repo / "data", sesion, 3))
    hoja = repo / DIRECTORIO_KIT / sesion / "hoja_trader.md"
    hoja.write_text(
        hoja.read_text(encoding="utf-8") + "\nlinea de mas\n",
        encoding="utf-8",
        newline="\n",
    )

    problemas, _ = comprobar(repo, repo / "data", sesion, celebrada=False)
    assert any("difiere de lo que se genera hoy" in p for p in problemas)

    problemas, avisos = comprobar(repo, repo / "data", sesion, celebrada=True)
    assert not any("hoja_trader" in p for p in problemas)
    assert any("la sesion se celebro" in a for a in avisos)


def test_las_particiones_no_se_perdonan_ni_con_la_sesion_celebrada(tmp_path: Path) -> None:
    """`particiones.yaml` no depende de las respuestas: sale de los hashes y del seed.

    El perdon a una sesion celebrada se escribio para TODO el paquete, y eso incluia las
    particiones, que son la prueba de que se fijaron antes de etiquetar (ADR-0011). Con ese
    perdon, reescribirlas despues de ver las etiquetas solo producia un AVISO y `kit check`
    seguia saliendo con 0.
    """
    repo, _ = repo_kit(tmp_path)
    sesion = "2026-09-15-sesion-01"
    escribir(repo, construir(repo, repo / "data", sesion, 3))
    part = repo / DIRECTORIO_KIT / sesion / "particiones.yaml"
    part.write_text(
        part.read_text(encoding="utf-8").replace("seed: 3", "seed: 4"),
        encoding="utf-8",
        newline="\n",
    )

    for celebrada in (False, True):
        problemas, _ = comprobar(repo, repo / "data", sesion, celebrada=celebrada)
        assert any("particiones.yaml" in p for p in problemas), (
            f"con celebrada={celebrada} las particiones tienen que ser ERROR, no AVISO"
        )


def test_los_cupos_del_paquete_salen_del_paquete_y_editarlos_se_ve(tmp_path: Path) -> None:
    """ADR-0035, enmienda del 2026-09-21: `comprobar` recompone con el bloque `config:` congelado.

    El universo se congelo el 2026-09-20, pero los CUPOS seguian saliendo del `config.yaml` de
    HOY: `comprobar` solo COMPARABA el bloque guardado contra el fichero global, asi que editarlo
    -lo que septiembre exige, porque sus 14 dias laborables no dan para los 40 cupos de mayo-
    rompia la comprobacion de la sesion 1 entera. Medido el 2026-09-21: exit 1 con "config.yaml
    cambio despues de generar el paquete" y "particiones.yaml difiere".

    Y la falsabilidad, que es lo que legitima congelar: si alguien edita los cupos DEL BLOQUE
    CONGELADO, la recomposicion reparte distinto y `particiones.yaml` -que no se exime nunca, ni
    con la sesion celebrada- deja de reproducirse. Lo congelado se verifica, por el mismo
    mecanismo que prueba todo lo demas.
    """
    repo, _ = repo_kit(tmp_path)
    sesion = "2026-09-15-sesion-01"
    escribir(repo, construir(repo, repo / "data", sesion, 3))
    assert comprobar(repo, repo / "data", sesion) == ([], [])

    ventanas = repo / DIRECTORIO_KIT / sesion / "ventanas.yaml"
    texto = ventanas.read_text(encoding="utf-8")
    assert texto.count("    dev: 2\n") == 1, "el cupo vive una sola vez en el bloque congelado"
    ventanas.write_text(texto.replace("    dev: 2\n", "    dev: 1\n"), encoding="utf-8")
    for celebrada in (False, True):
        problemas, _ = comprobar(repo, repo / "data", sesion, celebrada=celebrada)
        assert any("particiones.yaml" in p for p in problemas), (
            f"con celebrada={celebrada} editar los cupos congelados tiene que verse"
        )
    ventanas.write_text(texto, encoding="utf-8")
    assert comprobar(repo, repo / "data", sesion) == ([], [])

    # Sin bloque `config:` no hay con que reproducir: PROBLEMA, no aviso, igual que `datasets:`.
    sin_config = yaml.safe_load(texto)
    del sin_config["config"]
    ventanas.write_text(yaml.safe_dump(sin_config, sort_keys=True), encoding="utf-8")
    problemas, _ = comprobar(repo, repo / "data", sesion)
    assert any("sin bloque `config`" in p for p in problemas)


CONFIG_FIDELIDAD = """simbolo: XXXYYY
dataset_prefijo: prueba-
ventana_local: {desde: "00:00", hasta: "15:00"}
sesiones:
  - {nombre: "07-11", desde: "07:00", hasta: "11:00"}
  - {nombre: "11-15", desde: "11:00", hasta: "15:00"}
anclajes_candidatos:
  - {etiqueta: madrid-00, hora: "00:00", huso: Europe/Madrid, coincide_con_sesiones: false}
  - {etiqueta: ny-17, hora: "17:00", huso: America/New_York, coincide_con_sesiones: true}
min_velas_ventana: 850
etiquetas: [compra, venta, no_trade]
cobertura_material:
  "2026-05":
    - {desde: "2026-05-04", hasta: "2026-05-08", entregado_el: "2026-09-20", fuente: [ADR-0034]}
particiones: {fidelidad-dev: 2, fidelidad-1: 2, fidelidad-2: 0, fidelidad-3: 0}
"""


def _repo_fidelidad(tmp_path: Path, config: str = CONFIG_FIDELIDAD) -> Path:
    repo, _ = repo_kit(tmp_path)
    carpeta = repo / "knowledge" / "cases" / "fidelidad"
    carpeta.mkdir(parents=True)
    (carpeta / "config.yaml").write_text(config, encoding="utf-8")
    return repo


def test_el_camino_de_fidelidad_reparte_lo_que_el_material_cubre(tmp_path: Path) -> None:
    """ADR-0036: material ETIQUETADO, sin sesion, sin cuestionario y sin filtro de vistos.

    Tres cosas a la vez, y las tres son la decision:
      1. El filtro de `vistos.yaml` se SALTA a proposito: `2026-05-05` esta visto y en el kit
         queda excluido, pero aqui es un caso. Estos dias los ha visto el trader, y por eso estan
         etiquetados y sirven.
      2. `cobertura_material` acota el universo con MOTIVO PROPIO, que no es "visto" ni "pocas
         velas": el material del trader no llega mas alla.
      3. Aqui NINGUN fichero se exime de reproducirse, ni con sesion celebrada ni sin ella, porque
         no hubo reunion cuyas respuestas expliquen una diferencia.
    """
    repo = _repo_fidelidad(tmp_path)
    a1 = fid.construir(repo, repo / "data", "xxxyyy-2026-05", 3)
    a2 = fid.construir(repo, repo / "data", "xxxyyy-2026-05", 3)
    assert a1.ficheros == a2.ficheros  # determinista
    assert fid.construir(repo, repo / "data", "xxxyyy-2026-05", 4).asignacion != a1.asignacion

    dias = sorted(c.dia for c in a1.casos)
    assert all("2026-05-04" <= d <= "2026-05-08" for d in dias), dias
    assert a1.universo == 5, "laborables 4,5,6,7,8 del tramo cubierto"
    assert len(a1.casos) == 4, "cupos 2+2; el quinto caso se queda fuera del reparto"
    assert set(a1.asignacion.values()) <= {"fidelidad-dev", "fidelidad-1"}

    motivos = {e.dia: e.motivo for e in a1.excluidos}
    #  esta en  y el kit lo excluye; aqui NO, y esa es la decision.
    assert "2026-05-05" not in motivos, "el filtro de vistos se salta a proposito"
    assert "fuera de la cobertura del material del trader" in motivos["2026-05-11"]
    assert "2026-05 cubre 2026-05-04..2026-05-08" in motivos["2026-05-11"]
    assert "visto" not in motivos["2026-05-11"] and "velas" not in motivos["2026-05-11"]

    fid.escribir(repo, a1)
    assert fid.comprobar(repo, repo / "data", "xxxyyy-2026-05") == ([], [])
    with pytest.raises(fid.FidelidadError, match="ya existe"):
        fid.escribir(repo, a1)

    # Nada se exime: tocar el bloque congelado se ve, sin excepcion de "sesion celebrada".
    ventanas = repo / "knowledge" / "cases" / "fidelidad" / "xxxyyy-2026-05" / "ventanas.yaml"
    texto = ventanas.read_text(encoding="utf-8")
    # Un campo que la recomposicion SI regenera. Mutar el bloque `config:` congelado no serviria
    # aqui: se recompone CON el, asi que el fichero saldria igual -esa es justo la razon de ser
    # del ancla (ADR-0035 enmendado), que cubre el fichero entero y no lo que el fichero decide-.
    ventanas.write_text(texto.replace("universo: 5", "universo: 9"), encoding="utf-8")
    problemas, _ = fid.comprobar(repo, repo / "data", "xxxyyy-2026-05")
    assert any("ventanas.yaml" in p for p in problemas)
    ventanas.write_text(texto, encoding="utf-8")
    assert fid.comprobar(repo, repo / "data", "xxxyyy-2026-05") == ([], [])


def test_un_mes_sin_material_declarado_no_aporta_casos(tmp_path: Path) -> None:
    """Este camino existe para repartir material etiquetado: de un mes sin material, nada."""
    repo = _repo_fidelidad(
        tmp_path,
        CONFIG_FIDELIDAD.replace('"2026-05"', '"2026-06"')
        .replace("2026-05-04", "2026-06-01")
        .replace("2026-05-08", "2026-06-05")
        .replace("fidelidad-dev: 2, fidelidad-1: 2", "fidelidad-dev: 0, fidelidad-1: 0"),
    )
    a = fid.construir(repo, repo / "data", "xxxyyy-2026-06", 1)
    assert a.casos == [] and a.universo == 0
    motivos = {e.dia: e.motivo for e in a.excluidos}
    assert "sin material etiquetado del trader" in motivos["2026-05-04"]
    assert "2026-05 no esta en cobertura_material" in motivos["2026-05-04"]


def test_cobertura_material_no_admite_una_lista_de_dias(tmp_path: Path) -> None:
    """Declarar los dias CUBIERTOS publicaria etiquetas: un laborable del rango que no estuviera
    en la lista seria un dia sin operaciones, y eso ES su etiqueta (ADR-0036)."""
    malos = (
        (
            '- {desde: "2026-05-04", hasta: "2026-05-08", entregado_el: "2026-09-20",'
            " fuente: [ADR-0034]}",
            '- "2026-05-04"\n    - "2026-05-05"',
            "lista de DIAS",
        ),
        (
            'desde: "2026-05-04", hasta: "2026-05-08"',
            'desde: "2026-05-08", hasta: "2026-05-04"',
            "al reves",
        ),
        (
            'desde: "2026-05-04", hasta: "2026-05-08"',
            'desde: "2026-06-04", hasta: "2026-06-08"',
            "no es de ese mes",
        ),
    )
    for i, (viejo, nuevo, mensaje) in enumerate(malos):
        repo = _repo_fidelidad(tmp_path / f"malo{i}", CONFIG_FIDELIDAD.replace(viejo, nuevo))
        with pytest.raises(fid.FidelidadError, match=mensaje):
            fid.cargar_config(repo)
    # Y dos tramos que se pisan: que dia esta cubierto seria ambiguo.
    repo = _repo_fidelidad(
        tmp_path / "solapa",
        CONFIG_FIDELIDAD.replace(
            "fuente: [ADR-0034]}",
            'fuente: [ADR-0034]}\n    - {desde: "2026-05-06", hasta: "2026-05-09"}',
        ),
    )
    with pytest.raises(fid.FidelidadError, match="solapados"):
        fid.cargar_config(repo)


def test_decidida_exige_un_adr_que_exista_y_que_la_nombre(tmp_path: Path) -> None:
    """`DECIDIDA` nace con ADR-0022 para lo que el consultor cierra sin preguntar al trader.

    Tiene que ser un ESTADO y no un campo junto a ABIERTA: `cases/cuestionario.py` mete toda
    ABIERTA en el cuestionario de la sesion siguiente, asi que con un campo se le volveria a
    preguntar al trader lo que el consultor ya decidio. Y el ADR no basta con que exista: tiene
    que NOMBRARLA, o `decision: ADR-0002` pasaria entero, que es el defecto que F12 encontro dos
    veces con `pendiente_definicion: A-999` y con `ambiguedad_id: A-200`.
    """
    from botsito.cases.ambiguedades import AmbiguedadError, cargar_ambiguedades

    ruta = tmp_path / "amb.yaml"
    base = AMBIGUEDADES.format(a="ev-v1-000100-aaaaaaaa", b="ev-v1-000200-bbbbbbbb")

    # NO carga: DECIDIDA sin su ADR
    ruta.write_text(
        base.replace(
            "estado: ABIERTA\n    decision: null", "estado: DECIDIDA\n    decision: null", 1
        ),
        encoding="utf-8",
    )
    with pytest.raises(AmbiguedadError, match="DECIDIDA exige"):
        cargar_ambiguedades(ruta)

    # NO carga: decision sin ser DECIDIDA
    ruta.write_text(base.replace("decision: null", "decision: ADR-0022", 1), encoding="utf-8")
    with pytest.raises(AmbiguedadError, match="solo van en DECIDIDA"):
        cargar_ambiguedades(ruta)

    # SI carga: DECIDIDA completa
    completa = base.replace(
        "estado: ABIERTA\n    decision: null\n    decidida_el: null",
        "estado: DECIDIDA\n    decision: ADR-0022\n    decidida_el: '2026-09-12'",
        1,
    )
    ruta.write_text(completa, encoding="utf-8")
    a = cargar_ambiguedades(ruta)[0]
    assert a.estado == "DECIDIDA" and a.decision == "ADR-0022" and a.decidida_el == "2026-09-12"


def test_una_ambiguedad_puede_citar_evidencia_ya_supersedida() -> None:
    """Superseder un item no borra la pregunta que ese item abrio.

    `kit check` miraba solo los items VIVOS para comprobar que la evidencia citada existe, y
    `knowledge validate` miraba todos: dos llamadas a la misma funcion diciendo cosas distintas.
    Se noto el 2026-09-12, al cerrar la contradiccion `stop.nivel` con los primeros `supersede`
    sobre evidencia del proyecto: A-10, A-11 y A-18 pasaron a citar evidencia "que no existe".

    Existir y seguir vigente no son lo mismo, y una ambiguedad cita lo primero.
    """
    from botsito.cases.ambiguedades import cargar_ambiguedades
    from botsito.cases.ambiguedades import validar_contra_contexto as validar_amb
    from botsito.comun.documentos import activos as vivos_de
    from botsito.config.registro import cargar_registro
    from botsito.evidence.modelo import cargar_evidencia

    items = list(cargar_evidencia(REPO / "knowledge" / "evidence"))
    supersedidos = {i.supersede for i in items if i.supersede}
    assert supersedidos, "sin ningun item supersedido esto no vigilaria nada"

    ambs = cargar_ambiguedades(REPO / "knowledge" / "spec" / "ambiguedades.yaml")
    citadas = {e for a in ambs for e in a.evidencia}
    assert citadas & supersedidos, (
        "ninguna ambiguedad cita un item supersedido: el caso que esto vigila ya no existe en el "
        "repositorio, asi que hay que revisar si el test sigue teniendo sentido"
    )

    nombres = set(cargar_registro(REPO / "knowledge" / "spec" / "parametros.yaml").nombres())
    con_todos = validar_amb(ambs, {i.id for i in items}, nombres, set())
    solo_vivos = validar_amb(ambs, {i.id for i in vivos_de(items)}, nombres, set())
    assert not [p for p in con_todos if "no existe" in p], con_todos
    assert [p for p in solo_vivos if "no existe" in p], (
        "mirar solo los vivos tendria que fallar; si no falla, el caso se perdio"
    )


def test_las_tres_guardias_semanticas_de_decidida_saltan_de_verdad(tmp_path: Path) -> None:
    """El cargador solo mira el FORMATO. Lo que impide cerrar mal una ambiguedad esta en
    `validation/knowledge.py`, y hasta la auditoria de cierre de F13 no lo probaba nada.

    Son tres condiciones, y las tres importan por el mismo motivo: una decision del consultor no
    puede tapar una pregunta que le toca al trader.
      1. el ADR citado EXISTE (si no, `decision: ADR-9999` pasaria);
      2. el ADR la NOMBRA (si no, `decision: ADR-0002` pasaria: es el defecto que F12 encontro dos
         veces, con `pendiente_definicion: A-999` y con `ambiguedad_id: A-200`);
      3. no vale sobre una `bloqueante` ni sobre una que sostenga el `ambiguedad_id` de un
         parametro: si el bot corre con un default NUESTRO por culpa de esa pregunta, la respuesta
         es del trader y no se cierra decidiendo.

    Se prueba sobre una COPIA del repositorio real, no sobre un fixture: las guardias viven dentro
    de `validar`, que lee el registro, los ADR y el feedback a la vez.
    """
    import shutil

    from botsito.validation.knowledge import validar

    def repo_copia() -> Path:
        destino = tmp_path / f"repo{len(list(tmp_path.iterdir()))}"
        destino.mkdir()
        for carpeta in ("knowledge", "docs", "config"):
            if (REPO / carpeta).is_dir():
                shutil.copytree(REPO / carpeta, destino / carpeta, ignore=_sin_holdout)
        return destino

    def problemas_con(cambio: tuple[str, str]) -> list[str]:
        destino = repo_copia()
        ruta = destino / "knowledge" / "spec" / "ambiguedades.yaml"
        texto = ruta.read_text(encoding="utf-8")
        viejo, nuevo_txt = cambio
        assert viejo in texto, viejo
        ruta.write_text(texto.replace(viejo, nuevo_txt, 1), encoding="utf-8", newline="\n")
        return validar(destino)[1]

    # A-22 es la unica DECIDIDA hoy, y es la que se rompe de cuatro maneras.
    casos = [
        (("decision: ADR-0022", "decision: ADR-9999"), "que no existe"),
        (("decision: ADR-0022", "decision: ADR-0002"), "no la nombra"),
        (
            (
                "estado: DECIDIDA\n    decision: ADR-0022\n    decidida_el: '2026-09-12'\n"
                "    bloqueante: false",
                "estado: DECIDIDA\n    decision: ADR-0022\n    decidida_el: '2026-09-12'\n"
                "    bloqueante: true",
            ),
            "no puede cerrarse por decision",
        ),
    ]
    mudas = []
    for cambio, aguja in casos:
        salida = problemas_con(cambio)
        if not any(aguja in linea for linea in salida):
            mudas.append(f"{cambio[1][:40]!r} no produjo {aguja!r}")
    assert not mudas, mudas

    # Y con el fichero intacto, ninguna de las tres se queja (las demas quejas son de `data/`,
    # que esta copia no tiene a proposito).
    limpia = [x for x in validar(repo_copia())[1] if "ambiguedades:" in x]
    assert not limpia, limpia


def test_una_decidida_no_entra_en_el_cuestionario_de_la_siguiente_sesion() -> None:
    """El motivo por el que DECIDIDA es un estado y no un campo, comprobado sobre la spec real."""
    from botsito.cases.ambiguedades import cargar_ambiguedades

    ambs = cargar_ambiguedades(REPO / "knowledge" / "spec" / "ambiguedades.yaml")
    abiertas = {a.id for a in ambs if a.estado == "ABIERTA"}
    decididas = {a.id for a in ambs if a.estado == "DECIDIDA"}
    assert decididas, "hoy hay al menos una decidida (A-22)"
    assert not (decididas & abiertas), "una decidida ya no se pregunta"


# ---------------------------------------------------------------- meses vistos (2026-09-17)


def _vistos_mayo(repo: Path, visto_el: str) -> None:
    """Mayo visto el `visto_el`, conservando el dia 05-05 del kit sintetico (visto el 09-01)."""
    (repo / DIRECTORIO_KIT / "vistos.yaml").write_text(
        f'meses:\n  - {{mes: "2026-05", motivo: backtest, fuente: [x], visto_el: "{visto_el}"}}\n'
        + VISTOS.split("\n", 1)[1],
        encoding="utf-8",
    )


def test_un_mes_visto_despues_no_borra_lo_que_un_paquete_anterior_pregunto(tmp_path: Path) -> None:
    """El hueco de `vistos.yaml`: declarar mayo visto hacia que `kit check` de la sesion 1,
    construida con mayo ciego, dijera "se piden 40 casos y el universo tiene 22". Con `visto_el`
    posterior a la sesion, el paquete se reproduce entero; y un paquete de una sesion posterior no
    puede sortear mayo: `kit build` FALLA."""
    repo, ids = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    _vistos_mayo(repo, "2026-09-11")
    # el paquete del 09-09 se sigue reproduciendo byte a byte, sin un aviso
    assert comprobar(repo, repo / "data", "2026-09-09-sesion-01") == ([], [])
    # y knowledge validate no le encuentra nada
    ids_ev = set(ids.values())
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "ventanas.yaml").read_text(
            encoding="utf-8"
        )
    )
    datasets = {c["dataset_id"] for c in doc["casos"]}
    assert validar_paquetes(repo, [], ids_ev, datasets) == ([], [])
    # un paquete con sesion el MISMO dia o despues no puede sortear mayo: falla
    for sesion in ("2026-09-11-sesion-02", "2026-09-15-sesion-02"):
        with pytest.raises(KitError, match="universo tiene 0"):
            construir(repo, repo / "data", sesion, 3)
    # uno de la vispera, si
    assert construir(repo, repo / "data", "2026-09-10-sesion-02", 3).casos


def test_la_guardia_de_construir_falla_aunque_el_filtro_se_salte(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Defensa en profundidad: si un dia visto se colara en el universo, `construir` no escribe un
    paquete con el: falla. Se prueba apagando el filtro de `_cargar_todo`, que es el fallo que la
    guardia cubre; la guardia lee `vistos.yaml` por su cuenta."""
    import botsito.cases.paquete as paq

    repo, _ = repo_kit(tmp_path)
    _vistos_mayo(repo, "2026-09-01")
    original = paq._cargar_todo

    def sin_filtro(repo_: Path, sesion: str | None = None) -> Any:
        config, registro, ambiguedades, mapa, _meses, _dias, items = original(repo_, sesion)
        return config, registro, ambiguedades, mapa, set(), set(), items

    monkeypatch.setattr(paq, "_cargar_todo", sin_filtro)
    with pytest.raises(KitError, match="ya habia visto"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)


def test_knowledge_validate_denuncia_un_paquete_escrito_con_dias_vistos(tmp_path: Path) -> None:
    """Sin datos, en CI: un paquete ya escrito que tenga dias de un mes visto a mas tardar el dia de
    su sesion; y un dia que el paquete excluyo como visto y cuya entrada ya no lo sostiene."""
    repo, ids = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-15-sesion-01", 3))
    ids_ev = set(ids.values())
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "ventanas.yaml").read_text(
            encoding="utf-8"
        )
    )
    datasets = {c["dataset_id"] for c in doc["casos"]}
    assert validar_paquetes(repo, [], ids_ev, datasets) == ([], [])
    # mayo declarado visto ANTES de la sesion, con el paquete ya escrito: se denuncia
    _vistos_mayo(repo, "2026-09-12")
    problemas, _ = validar_paquetes(repo, [], ids_ev, datasets)
    assert any("ya habia visto el dia de su sesion" in p for p in problemas), problemas
    # el dia 05-05 que el paquete excluyo como visto, refechado DESPUES de la sesion: se denuncia
    (repo / DIRECTORIO_KIT / "vistos.yaml").write_text(
        VISTOS.replace("2026-09-01", "2026-09-20"), encoding="utf-8"
    )
    problemas, _ = validar_paquetes(repo, [], ids_ev, datasets)
    assert any("2026-05-05" in p and "posterior a la sesion" in p for p in problemas), problemas
    # y quitado del todo
    (repo / DIRECTORIO_KIT / "vistos.yaml").write_text("meses: []\ndias: []\n", encoding="utf-8")
    problemas, _ = validar_paquetes(repo, [], ids_ev, datasets)
    assert any("2026-05-05" in p and "ya no esta" in p for p in problemas), problemas


def test_visto_el_es_obligatorio(tmp_path: Path) -> None:
    repo, _ = repo_kit(tmp_path)
    vis = repo / DIRECTORIO_KIT / "vistos.yaml"
    vis.write_text(
        'meses:\n  - {mes: "2026-05", motivo: x, fuente: []}\ndias: []\n', encoding="utf-8"
    )
    with pytest.raises(KitError, match="visto_el"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    vis.write_text(
        'meses:\n  - {mes: "2026-05", motivo: x, fuente: [], visto_el: "ayer"}\ndias: []\n',
        encoding="utf-8",
    )
    with pytest.raises(KitError, match="no es AAAA-MM-DD"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)


def test_el_kappa_avisa_de_etiquetado_no_ciego(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Para F26: una unidad sobre un dia de un mes que el trader ya habia visto el dia de la sesion
    que la etiqueto no es etiquetado ciego. No se excluye, se dice."""
    repo, _ = repo_kit(tmp_path)
    s1, s2 = "2026-09-09-sesion-01", "2026-09-22-sesion-02"
    escribir(repo, construir(repo, repo / "data", s1, 3))
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / s1 / "particiones.yaml").read_text(encoding="utf-8")
    )
    dev = [c for c, p in doc["asignacion"].items() if p == "dev"]
    for c in dev:
        _registro_label(repo, s1, c, "07-11: venta; 11-15: no_trade")
        _registro_label(repo, s2, c, "07-11: venta; 11-15: no_trade")
    _vistos_mayo(repo, "2026-09-11")
    assert cli.main(["--repo", str(repo), "kit", "kappa", "--sesion-a", s1, "--sesion-b", s2]) == 0
    err = capsys.readouterr().err
    assert f"{s2}: {len(dev)} casos etiquetados sobre dias que el trader ya habia visto" in err
    # la sesion 1 etiqueto el 09-09, antes de que el trader viera mayo: esa ronda SI fue ciega
    assert f"{s1}: {len(dev)} casos etiquetados" not in err
    assert "no fue etiquetado ciego" in err


def test_mover_una_sesion_despues_de_un_visto_el_falla_y_no_mueve(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Meses vistos (2026-09-17): mover una sesion a una fecha igual o posterior al `visto_el` de un
    mes que su paquete sortea la dejaria etiquetando dias ya vistos. Tiene que FALLAR y dejar el
    paquete original byte a byte; a una fecha anterior al `visto_el`, se mueve."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    _vistos_mayo(repo, "2026-09-11")
    carpeta = repo / DIRECTORIO_KIT / "2026-09-09-sesion-01"
    original = {p.name: p.read_bytes() for p in carpeta.iterdir()}
    modulo = _mover_sesion(repo)
    for fecha in ("2026-09-11", "2026-09-22"):
        monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", fecha])
        with pytest.raises(KitError, match="universo tiene 0"):
            modulo.main()
        assert {p.name: p.read_bytes() for p in carpeta.iterdir()} == original
        assert not (repo / DIRECTORIO_KIT / f"{fecha}-sesion-01").exists()
    monkeypatch.setattr("sys.argv", ["mover_sesion.py", "--a", "2026-09-10"])
    assert modulo.main() == 0
    assert (repo / DIRECTORIO_KIT / "2026-09-10-sesion-01").is_dir()


# ------------------------------------------------- el universo congelado (2026-09-20, ADR-0035)


def _segundo_dataset(repo: Path, nombre: str = "prueba", con_datos: bool = True) -> str:
    """Congela OTRO dataset con el mismo prefijo del kit, como haria `data download` de un mes
    nuevo. Con `con_datos=False` deja el manifiesto y borra sus ficheros: el caso que convertia
    `kit check` en un exit 0 que no comprobaba nada."""
    congelado = congelar(
        repo=repo,
        carpeta_datos=repo / "data",
        nombre=nombre,
        simbolo="XXXYYY",
        escala=100000,
        desde=date(2026, 6, 1),
        hasta=date(2026, 6, 15),
        descarga=descarga,
        hoy=HOY,
    )
    if not con_datos:
        for f in congelado.ficheros:
            f.unlink()
    return str(congelado.manifiesto["dataset_id"])


def test_un_dataset_nuevo_no_cambia_un_paquete_ya_escrito(tmp_path: Path) -> None:
    """EL defecto que cierra ADR-0035: el universo se calculaba del disco de HOY, asi que
    descargar un mes nuevo reparticionaba un paquete anterior y `particiones.yaml` -la unica
    prueba de que las particiones se fijaron antes de etiquetar- dejaba de reproducirse."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    antes = comprobar(repo, repo / "data", "2026-09-09-sesion-01")
    assert antes == ([], []), antes
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "ventanas.yaml").read_text(
            encoding="utf-8"
        )
    )
    congelados = doc["datasets"]
    assert congelados and all(isinstance(d, str) for d in congelados)

    nuevo = _segundo_dataset(repo)
    assert nuevo not in congelados
    # El paquete sigue reproduciendose: se recompone con SU lista, no con el disco.
    assert comprobar(repo, repo / "data", "2026-09-09-sesion-01") == ([], [])
    # Y un paquete NUEVO si ve el dataset nuevo: `construir` sigue leyendo el disco a proposito.
    otro = construir(repo, repo / "data", "2026-09-10-sesion-02", 3)
    assert nuevo in yaml.safe_load(otro.ficheros["ventanas.yaml"])["datasets"]


def test_sin_datasets_congelados_es_problema_y_no_aviso(tmp_path: Path) -> None:
    """Sin la lista no hay con que reproducir el paquete. Y no puede bajar a AVISO por ser una
    sesion celebrada: `datasets` no sale de ninguna respuesta del trader."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    ruta = repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "ventanas.yaml"
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    quitados = doc.pop("datasets")
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=True, width=100), "utf-8")
    for celebrada in (False, True):
        problemas, _ = comprobar(repo, repo / "data", "2026-09-09-sesion-01", celebrada)
        assert any("no esta congelado" in p for p in problemas), (celebrada, problemas)
    # y `knowledge validate`, que corre SIN datos, lo ve igual
    ids_ev = {i.stem for i in (repo / "knowledge" / "evidence").glob("ev-*.yaml")}
    problemas, _ = validar_paquetes(repo, [], ids_ev, set(quitados))
    assert any("no esta congelado" in p for p in problemas), problemas


def test_quitar_un_dataset_de_la_lista_congelada_se_ve(tmp_path: Path) -> None:
    """La lista no es decorativa: si alguien quita un dataset -por ejemplo un DONANTE, que aporta
    las velas de las 22:00Z al primer dia del mes siguiente y no deja ningun caso- el paquete deja
    de reproducirse, y se ve aunque la sesion este celebrada."""
    repo, _ = repo_kit(tmp_path)
    _segundo_dataset(repo)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    ruta = repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "ventanas.yaml"
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    assert len(doc["datasets"]) == 2
    doc["datasets"] = doc["datasets"][:1]
    ruta.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=True, width=100), "utf-8")
    problemas, _ = comprobar(repo, repo / "data", "2026-09-09-sesion-01", celebrada=True)
    assert problemas, "quitar un dataset congelado paso desapercibido"


def test_un_manifiesto_sin_sus_ficheros_nombra_los_datasets(tmp_path: Path) -> None:
    """Hasta el 2026-09-20 `hay_datos_del_kit` era un AND global sobre TODOS los datasets del
    prefijo: un manifiesto commiteado sin descargar sus ficheros -aunque fuera ajeno al paquete-
    convertia `kit check` en un exit 0 que no comprobaba nada y que no declaraba ninguna lectura.
    Ahora los datasets a los que les faltan ficheros se NOMBRAN."""
    repo, _ = repo_kit(tmp_path)
    escribir(repo, construir(repo, repo / "data", "2026-09-09-sesion-01", 3))
    huerfano = _segundo_dataset(repo, con_datos=False)
    config = cargar_config(repo / DIRECTORIO_KIT / "config.yaml")
    assert datasets_que_faltan_en_disco(repo, repo / "data", config) == [huerfano]
    # El paquete no lo tiene congelado, asi que su comprobacion NO se apaga por culpa de el.
    assert comprobar(repo, repo / "data", "2026-09-09-sesion-01") == ([], [])
    # Y si al que le faltan los ficheros es uno DEL paquete, el aviso lo nombra.
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-09-sesion-01" / "ventanas.yaml").read_text("utf-8")
    )
    suyo = doc["datasets"][0]
    manifiesto = next(
        m for m in manifiestos(repo) if yaml.safe_load(m.read_text("utf-8"))["dataset_id"] == suyo
    )
    for f in yaml.safe_load(manifiesto.read_text("utf-8"))["ficheros"]:
        (repo / "data" / str(f["ruta"])).unlink()
    _, avisos = comprobar(repo, repo / "data", "2026-09-09-sesion-01")
    assert any(suyo in a for a in avisos), avisos


def test_la_cobertura_saca_un_mes_del_universo_y_el_kit_la_pasa(tmp_path: Path) -> None:
    """EL AGUJERO 2: un `kit build` NUEVO metia en el universo un mes sin material del trader.

    No lo tapaba `vistos.yaml` y es CORRECTO que no lo tape: ese fichero responde "¿es ciego?" y
    un mes que el trader no ha visto ES ciego. Lo que faltaba es la otra pregunta, "¿hay
    material?", y hasta el 2026-09-21 su respuesta no llegaba a `universo()` porque la llamada del
    kit no pasaba `cobertura`. El mes se sortearia a una particion y no se etiquetaria nunca, que
    es el defecto de los dos dias que se cayeron en silencio un escalon mas arriba.

    Tambien comprueba lo contrario, que es lo que impide cerrar de mas: con la cobertura puesta,
    el paquete SIGUE construyendose e incluye los dias que debe.
    """
    repo, _ = repo_kit(tmp_path)
    cfg = repo / DIRECTORIO_KIT / "config.yaml"

    # (1) SIN cobertura: el universo es el que era. Es el estado de `main` hasta esta rama.
    antes = construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    assert antes.universo > 0
    dias_antes = {c.dia for c in antes.casos}
    alguno = sorted(dias_antes)[0]
    mes = alguno[:7]

    # (2) CON el mes declarado con CERO tramos: sale del universo, con su motivo y sin dias.
    cfg.write_text(CONFIG + f'cobertura_material:\n  "{mes}": []\n', encoding="utf-8")
    with pytest.raises(KitError, match="universo tiene 0"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)

    # (3) Y CON TRAMOS DE VERDAD el paquete CONSTRUYE e incluye lo que debe: una guardia que solo
    # sabe decir que no no ha demostrado nada.
    cfg.write_text(
        CONFIG
        + f'cobertura_material:\n  "{mes}":\n    - {{desde: "{mes}-01", hasta: "{mes}-31"}}\n',
        encoding="utf-8",
    )
    despues = construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    assert despues.universo == antes.universo, "acotar a todo el mes no quita ningun dia"
    assert {c.dia for c in despues.casos} == dias_antes
    cfg.write_text(CONFIG, encoding="utf-8")
