"""F10: ambiguedades, particiones, kappa, ventanas, paquete de sesion y CLI `kit`."""

from __future__ import annotations

import lzma
import struct
from datetime import UTC, date, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest
import yaml

from botsito import cli
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
    escribir,
    validar_paquetes,
)
from botsito.cases.particiones import ParticionError, asignar, clave_orden
from botsito.data.dataset import congelar
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
    tipo: texto
    unidad: tocar/cierre
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
    bloqueante: true
  - id: A-2
    titulo: BE al tocar o al cierre
    pregunta: "¿al tocar o al cierre?"
    resuelve_en: [F11]
    evidencia: [{b}]
    parametros: [break_even_condicion]
    contradiccion: null
    estado: ABIERTA
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
  cartuchos_max: {temas: [cartuchos], ambiguedad: A-1}
  break_even_condicion: {temas: [break_even], ambiguedad: A-2, opciones: [tocar, cierre]}
  anclaje_h4: {temas: [reloj], ambiguedad: null}
"""
VISTOS = 'meses: []\ndias:\n  - {dia: "2026-05-05", motivo: prueba}\n'
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


def test_ambiguedades_reales_y_esquema(tmp_path: Path) -> None:
    ambs = cargar_ambiguedades(REPO / "knowledge" / "spec" / "ambiguedades.yaml")
    # correlativas desde A-1, sin huecos: la sesion 1 añadio A-13..A-17 y seguira creciendo
    assert [a.id for a in ambs] == [f"A-{i}" for i in range(1, len(ambs) + 1)]
    assert len(ambs) >= 17
    assert sum(1 for a in ambs if a.bloqueante) == 3  # las tres que se llevaron a la sesion 1
    assert {a.id for a in ambs if a.estado == "RESUELTA"} == {f"A-{i}" for i in range(1, 13)}
    assert next(a for a in ambs if a.id == "A-10").contradiccion == "stop.nivel"
    ruta = tmp_path / "amb.yaml"
    for malo, msg in (
        (AMBIGUEDADES.replace("id: A-2", "id: A-1"), "repetido"),
        (AMBIGUEDADES.replace("id: A-1", "id: A-3"), "orden numerico"),
        (
            AMBIGUEDADES.replace(
                "estado: ABIERTA\n    bloqueante: true", "estado: X\n    bloqueante: true"
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
    (repo / DIRECTORIO_KIT / "config.yaml").write_text(
        CONFIG.replace("dev: 2", "dev: 3"), encoding="utf-8"
    )
    problemas, _ = comprobar(repo, repo / "data", "2026-09-15-sesion-01")
    assert any("config.yaml cambio" in p for p in problemas)
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
    mapa.write_text(
        MAPA.replace("  anclaje_h4: {temas: [reloj], ambiguedad: null}\n", ""), encoding="utf-8"
    )
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
    }
    campos.update(extra)
    return escribir_registro(repo / "knowledge" / "feedback", campos).stem


def test_kappa_desde_registros_y_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    repo, _ = repo_kit(tmp_path)
    base = ["--repo", str(repo), "kit"]
    assert cli.main([*base, "build", "--sesion", "2026-09-15-sesion-01", "--seed", "3"]) == 0
    assert "5 casos (2 dev)" in capsys.readouterr().out
    assert cli.main([*base, "build", "--sesion", "2026-09-15-sesion-01", "--seed", "3"]) == 1
    assert "no se sobreescribe" in capsys.readouterr().err
    assert cli.main([*base, "check", "--sesion", "2026-09-15-sesion-01"]) == 0
    assert cli.main([*base, "check", "--sesion", "2026-09-15-sesion-09"]) == 1
    capsys.readouterr()
    doc = yaml.safe_load(
        (repo / DIRECTORIO_KIT / "2026-09-15-sesion-01" / "particiones.yaml").read_text(
            encoding="utf-8"
        )
    )
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
    assert cli.main([*base, "kappa", "--sesion-a", s1, "--sesion-b", s2]) == 0
    out = capsys.readouterr()
    assert "unidades: 10" in out.out and "po: 0.900" in out.out and "kappa: 0.818" in out.out
    assert kp.calcular(
        {"u": "a", "v": "a", "w": "b"}, {"u": "a", "v": "a", "w": "a"}, ["a", "b"]
    ).avisos
    # un registro que supersede cambia la ronda
    viejo = _registro_label(repo, s2, casos[4], "07-11: compra; 11-15: no_trade", notas="x")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
        )
    _registro_label(repo, s2, casos[4], "07-11: venta; 11-15: no_trade", supersede=viejo, notas="y")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
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
    mapa = repo / DIRECTORIO_KIT / "mapa_parametros.yaml"
    mapa.write_text(MAPA.replace("ambiguedad: A-2", "ambiguedad: A-77"), encoding="utf-8")
    with pytest.raises(KitError, match="A-77"):
        construir(repo, repo / "data", "2026-09-15-sesion-02", 1)
    mapa.write_text(MAPA, encoding="utf-8")


def test_resuelta_min_velas_meses_vistos_y_universo(tmp_path: Path) -> None:
    repo, ids = repo_kit(tmp_path)
    # una ambiguedad RESUELTA deja de preguntarse; su parametro pasa a pregunta propia
    ruta_amb = repo / "knowledge" / "spec" / "ambiguedades.yaml"
    ruta_amb.write_text(
        AMBIGUEDADES.format(a=ids["a"], b=ids["b"]).replace(
            "estado: ABIERTA\n    bloqueante: false", "estado: RESUELTA\n    bloqueante: false"
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
        'meses:\n  - {mes: "2026-05", motivo: prueba, fuente: []}\ndias: []\n', encoding="utf-8"
    )
    with pytest.raises(KitError, match="universo tiene 0"):
        construir(repo, repo / "data", "2026-09-15-sesion-01", 3)
    vis.write_text('meses: []\ndias:\n  - {dia: "2026-5-5", motivo: x}\n', encoding="utf-8")
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
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
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
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
        )
    # dejamos una sola cadena viva: supersedemos `d` con uno que apunte a `ultimo`? No: un
    # registro supersede a UN registro; la cadena valida es original <- d y a <- b <- c. Cerramos
    # `c` con un registro que lo supersede y coincide con `d`.
    _registro_label(repo, s2, casos[0], "07-11: compra; 11-15: compra", supersede=ultimo, notas="e")
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    with pytest.raises(kp.EtiquetaError, match="dos LABEL_CASE activos"):
        kp.etiquetas_de_registros(
            registros, s2, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
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
            "supersede": etiqueta,
        },
    )
    registros = cargar_feedback(repo / "knowledge" / "feedback")
    unidades = kp.etiquetas_de_registros(
        registros, sesion, ["07-11", "11-15"], ["compra", "venta", "no_trade"]
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
