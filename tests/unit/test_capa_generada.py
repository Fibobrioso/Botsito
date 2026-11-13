"""Lo que la capa de MT5 recibe del repo, generado (trabajo/capa-generada, R6a.2; ADR-0082
D5): `src/botsito/mql5bridge/generar_capa.py` y su salida commiteada,
`mql5/Include/Botsito/Capa/Generado.mqh`.

- Regenerar no da diff: el fichero del repo es, byte a byte, lo que da el generador hoy; y
  cambiar un valor de un yaml sin regenerar lo rompe (sobre una copia de los yaml, nunca sobre
  el repo).
- `capa_hash` se recalcula AQUI por su cuenta (sin importar la funcion del generador):
  SHA-256 de los bytes sin la unica linea de `CAPA_HASH`; y es el valor que lleva esa linea.
- D2 y la respuesta a la PARADA (puntos 0 y 3): el generador falla, sin elegir, si un nombre de los
  dos ficheros difiere en tipo, valor, opciones o estado; si la pareja de stops level difiere; si
  `firma_huso_corte` y `huso_operativa` no dan la misma medianoche cada dia de `cubre` o
  `reloj_dia_riesgo` deja de ser `civil_operativa`; y si un parametro que entra es UNKNOWN.
- D1: nada de lo que entra es de categoria `estrategia`, y los de la estrategia o del simulador
  que la fase 0 dejo fuera no entran.

Cada comprobacion, rota a proposito en los dos sentidos.
"""

from __future__ import annotations

import hashlib
import re
import shutil
from pathlib import Path

import pytest

from botsito.config.registro import cargar_registro
from botsito.mql5bridge.generar_capa import (
    ENTRAN,
    GENERADO,
    GenerarError,
    capa_hash,
    generar,
    main,
)

RAIZ = Path(__file__).resolve().parents[2]
PERFIL = "ftmo-2step-swing-100k"
REGISTRO = Path("knowledge/spec/parametros.yaml")
CUENTA = Path(f"knowledge/cuentas/{PERFIL}.yaml")
CIERRES = Path(f"knowledge/cuentas/cierres/{PERFIL}.yaml")

# Independiente del generador: la linea del hash, como la define CAPA-GENERADA.md (fase 0, d).
LINEA_HASH = re.compile(rb'^const string CAPA_HASH = "([0-9a-f]{64})";\n', re.MULTILINE)


def hash_por_su_cuenta(contenido: bytes) -> tuple[str, str]:
    """(el hash que lleva el fichero, el recalculado sobre los bytes sin su linea)."""
    lineas = LINEA_HASH.findall(contenido)
    assert len(lineas) == 1, f"{len(lineas)} lineas de CAPA_HASH"
    sin = LINEA_HASH.sub(b"", contenido)
    return lineas[0].decode("ascii"), hashlib.sha256(sin).hexdigest()


@pytest.fixture
def copia(tmp_path: Path) -> Path:
    """Una raiz con solo los tres yaml que lee el generador, copiados del repo."""
    for r in (REGISTRO, CUENTA, CIERRES):
        (tmp_path / r).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(RAIZ / r, tmp_path / r)
    return tmp_path


def cambiar(raiz: Path, fichero: Path, nombre: str, viejo: str, nuevo: str) -> None:
    """Cambia `viejo` por `nuevo` (una sola vez) dentro del bloque del parametro `nombre`."""
    texto = (raiz / fichero).read_text(encoding="utf-8")
    m = re.search(rf"^  - nombre: {nombre}\n(?:(?!  - nombre: ).*\n)*", texto, re.MULTILINE)
    assert m is not None, nombre
    bloque = m.group(0)
    assert bloque.count(viejo) == 1, (nombre, viejo)
    (raiz / fichero).write_text(
        texto[: m.start()] + bloque.replace(viejo, nuevo) + texto[m.end() :],
        encoding="utf-8",
        newline="\n",
    )


# --- regenerar no da diff ------------------------------------------------------------------------


def test_regenerar_no_da_diff() -> None:
    assert generar(RAIZ, PERFIL) == (RAIZ / GENERADO).read_bytes()


def test_la_copia_de_los_yaml_da_lo_mismo_y_un_valor_cambiado_no(copia: Path) -> None:
    repo = (RAIZ / GENERADO).read_bytes()
    assert generar(copia, PERFIL) == repo
    cambiar(copia, REGISTRO, "firma_margen_seguridad", 'valor: "0.5"', 'valor: "0.6"')
    otro = generar(copia, PERFIL)
    assert otro != repo
    assert b"P_FIRMA_MARGEN_SEGURIDAD = 0.6;" in otro
    assert hash_por_su_cuenta(otro)[0] != hash_por_su_cuenta(repo)[0]


def test_cambiar_el_estado_o_el_calendario_tambien_cambia_lo_generado(copia: Path) -> None:
    repo = (RAIZ / GENERADO).read_bytes()
    cambiar(
        copia,
        REGISTRO,
        "lote_si_no_cabe",
        "estado: CONFIRMED",
        "estado: DEFAULT_AMBIGUOUS\n    ambiguedad_id: A-57",
    )
    ambigua = generar(copia, PERFIL)
    assert b"P_LOTE_SI_NO_CABE_ESTADO = BOTSITO_ESTADO_DEFAULT_AMBIGUOUS;" in ambigua
    assert ambigua != repo
    shutil.copyfile(RAIZ / REGISTRO, copia / REGISTRO)
    texto = (copia / CIERRES).read_text(encoding="utf-8")
    (copia / CIERRES).write_text(
        texto.replace('hasta: "2026-10-07"', 'hasta: "2026-10-06"'), encoding="utf-8", newline="\n"
    )
    assert generar(copia, PERFIL) != repo


def test_la_orden_comprobar_no_escribe_y_dice_si_difiere(
    copia: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (copia / GENERADO).parent.mkdir(parents=True)
    (copia / GENERADO).write_bytes((RAIZ / GENERADO).read_bytes())
    assert main(["--repo", str(copia), "--perfil", PERFIL, "--comprobar"]) == 0
    assert "al dia" in capsys.readouterr().out
    cambiar(copia, CUENTA, "firma_volumen_max_lotes", 'valor: "50"', 'valor: "40"')
    antes = (copia / GENERADO).read_bytes()
    assert main(["--repo", str(copia), "--perfil", PERFIL, "--comprobar"]) == 1
    assert "DISTINTO" in capsys.readouterr().out
    assert (copia / GENERADO).read_bytes() == antes
    assert main(["--repo", str(copia), "--perfil", PERFIL]) == 0
    assert (copia / GENERADO).read_bytes() == generar(copia, PERFIL) != antes


# --- el hash ---------------------------------------------------------------------------------


def test_el_hash_se_recalcula_por_su_cuenta() -> None:
    contenido = (RAIZ / GENERADO).read_bytes()
    lleva, recalculado = hash_por_su_cuenta(contenido)
    assert lleva == recalculado == capa_hash(contenido)


def test_el_hash_en_los_dos_sentidos() -> None:
    contenido = (RAIZ / GENERADO).read_bytes()
    lleva, _ = hash_por_su_cuenta(contenido)
    # un byte cambiado fuera de la linea del hash: el recalculado ya no es el que lleva
    roto = contenido.replace(b"CIERRES_N", b"CIERRES_M", 1)
    assert hash_por_su_cuenta(roto)[1] != lleva
    # cambiar el hash escrito no cambia el recalculado (la linea no entra en la cuenta)
    otro = contenido.replace(lleva.encode(), b"f" * 64)
    assert hash_por_su_cuenta(otro)[1] == hash_por_su_cuenta(contenido)[1]
    # dos lineas de hash, o ninguna: no hay hash
    linea = LINEA_HASH.search(contenido)
    assert linea is not None
    for malo in (contenido + linea.group(0), LINEA_HASH.sub(b"", contenido)):
        with pytest.raises(GenerarError, match="lineas de CAPA_HASH"):
            capa_hash(malo)


def test_lo_generado_es_utf8_sin_bom_lf_y_sin_define_ni_variables() -> None:
    contenido = (RAIZ / GENERADO).read_bytes()
    assert not contenido.startswith(b"\xef\xbb\xbf") and b"\r" not in contenido
    texto = contenido.decode("utf-8")
    assert "#define" not in texto
    codigo = [x for x in texto.splitlines() if x.strip() and not x.lstrip().startswith("//")]
    cabezas = {x.split()[0] for x in codigo if not x.startswith((" ", "{", "}"))}
    assert cabezas == {"const", "enum"}, cabezas


# --- D2 y los relojes ------------------------------------------------------------------------


def test_un_nombre_de_los_dos_ficheros_que_difiere_hace_fallar(copia: Path) -> None:
    cambiar(copia, CUENTA, "firma_apalancamiento", "valor: 30", "valor: 20")
    with pytest.raises(GenerarError, match="firma_apalancamiento.*valor"):
        generar(copia, PERFIL)
    shutil.copyfile(RAIZ / CUENTA, copia / CUENTA)
    cambiar(
        copia,
        CUENTA,
        "firma_apalancamiento",
        "estado: CONFIRMED",
        "estado: DEFAULT_AMBIGUOUS\n    ambiguedad_id: A-57",
    )
    with pytest.raises(GenerarError, match="firma_apalancamiento.*estado"):
        generar(copia, PERFIL)


def test_la_pareja_de_stops_level_tiene_que_coincidir(copia: Path) -> None:
    contenido = generar(copia, PERFIL)
    assert b"P_INSTRUMENTO_STOPS_LEVEL = 0;" in contenido
    assert b"FIRMA_STOPS_LEVEL" not in contenido
    cambiar(copia, CUENTA, "firma_stops_level_puntos", "valor: 0", "valor: 5")
    with pytest.raises(GenerarError, match="instrumento_stops_level y firma_stops_level_puntos"):
        generar(copia, PERFIL)


def test_los_dos_relojes_tienen_que_dar_la_misma_medianoche(copia: Path) -> None:
    contenido = generar(copia, PERFIL)
    assert b'P_FIRMA_HUSO_CORTE = "Europe/Prague";' in contenido
    assert b"HUSO_OPERATIVA" not in contenido
    # otro huso con el mismo horario de verano de la UE pasa (Europe/Berlin)...
    cambiar(copia, CUENTA, "firma_huso_corte", '"Europe/Prague"', '"Europe/Berlin"')
    assert b'"Europe/Berlin"' in generar(copia, PERFIL)
    # ...y uno que corta a otra hora, no
    cambiar(copia, CUENTA, "firma_huso_corte", '"Europe/Berlin"', '"Europe/London"')
    with pytest.raises(GenerarError, match="misma medianoche"):
        generar(copia, PERFIL)


def test_el_dia_de_riesgo_tiene_que_ser_el_civil(copia: Path) -> None:
    cambiar(copia, REGISTRO, "reloj_dia_riesgo", 'valor: "civil_operativa"', 'valor: "servidor"')
    with pytest.raises(GenerarError, match="reloj_dia_riesgo"):
        generar(copia, PERFIL)


def test_un_parametro_que_entra_sin_valor_hace_fallar(copia: Path) -> None:
    texto = (copia / CUENTA).read_text(encoding="utf-8")
    m = re.search(r"^  - nombre: firma_volumen_max_lotes\n(?:(?!  - nombre: ).*\n)*", texto, re.M)
    assert m is not None
    bloque = re.sub(r"    estado: CONFIRMED\n", "    estado: UNKNOWN\n", m.group(0))
    bloque = re.sub(r"    valor: .*\n", "", bloque)
    bloque = re.sub(r"    fuente: .*\n", "", bloque)
    (copia / CUENTA).write_text(
        texto[: m.start()] + bloque + texto[m.end() :], encoding="utf-8", newline="\n"
    )
    with pytest.raises(GenerarError, match="firma_volumen_max_lotes.*UNKNOWN"):
        generar(copia, PERFIL)


# --- D1 ----------------------------------------------------------------------------------------


def test_nada_de_lo_generado_es_de_la_estrategia() -> None:
    registro = cargar_registro(RAIZ / REGISTRO)
    cuenta = cargar_registro(RAIZ / CUENTA)
    for n in ENTRAN:
        p = registro.parametros.get(n) or cuenta.parametros[n]
        assert p.categoria != "estrategia", n
    estrategia = {n for n, p in registro.parametros.items() if p.categoria == "estrategia"}
    assert not estrategia & set(ENTRAN)
    fuera = {
        "huso_grafico",
        "sesgo_h4_tope_velas",
        "caja_se_fija",
        "reloj_sesiones",
        "sesiones_primera_vela_h4",
        "modelo_llenado",
        "latencia_ms",
        "huso_operativa",
        "cierre_pendientes",
        "firma_stops_level_puntos",
    }
    assert not fuera & set(ENTRAN)
    texto = (RAIZ / GENERADO).read_text(encoding="utf-8")
    for n in fuera | estrategia:
        assert f"P_{n.upper()} " not in texto, n
    for n in ENTRAN:
        assert f"P_{n.upper()} = " in texto, n
