"""La ruta de compilacion y de pruebas de la capa de MT5 (`botsito.mql5bridge.compilar`;
trabajo/ea-conexion, respuesta a la PARADA, punto 2), sin MetaTrader: la CI es Linux. Lo que se
prueba aqui es lo que no necesita MetaEditor ni el terminal: leer su log, la puerta, exportar del
indice, sustituir a proposito, el fichero de arranque y la comparacion con el golden. Cada cosa en
los dos sentidos. La compilacion y el script de pruebas, de verdad, en los anexos de la rama.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from botsito.mql5bridge.compilar import (
    Compilacion,
    CompilarError,
    comparar_con_golden,
    exportar,
    ini_de_pruebas,
    leer_log,
    log_para_anexo,
    resumen_de_resultado,
    sustituir,
)

RAIZ = Path(__file__).resolve().parents[2]
FASE0 = RAIZ / "docs" / "validation" / "anexos" / "EA-CONEXION" / "fase0"
GOLDEN = RAIZ / "tests" / "golden" / "journal"


def _como_metaeditor(texto: str) -> bytes:
    """Un log como lo escribe MetaEditor: UTF-16LE con BOM y CRLF (medido en la fase 0)."""
    return b"\xff\xfe" + ("\r\n".join(texto.splitlines()) + "\r\n").encode("utf-16-le")


def _log_de_fase0(nombre: str) -> bytes:
    return _como_metaeditor((FASE0 / nombre).read_text(encoding="utf-8"))


def _compilacion(errores: int, ex5: Path | None) -> Compilacion:
    return Compilacion("mql5/Experts/X.mq5", "0" * 64, b"", "", errores, (), 1, ex5)


def test_el_log_de_la_fase_0_se_lee_en_los_dos_sentidos() -> None:
    _, errores, avisos = leer_log(_log_de_fase0("compilar-medirdemoftmo-ok.log"))
    assert (errores, avisos) == (0, ())
    _, errores, _ = leer_log(_log_de_fase0("compilar-error-provocado.log"))
    assert errores == 1
    with pytest.raises(CompilarError, match="Result"):
        leer_log(_como_metaeditor("X.mq5 : information: compiling X.mq5\n"))


def test_los_avisos_se_listan_y_se_cuentan() -> None:
    texto = "X.mq5(3,1) : warning 43: possible loss of data\nResult: 0 errors, 1 warnings, 9 ms\n"
    _, errores, avisos = leer_log(_como_metaeditor(texto))
    assert (errores, len(avisos)) == (0, 1)
    with pytest.raises(CompilarError, match="avisos"):
        leer_log(_como_metaeditor(texto.replace("1 warnings", "2 warnings")))


def test_la_puerta_es_cero_errores_y_el_ex5_no_el_codigo_de_salida(tmp_path: Path) -> None:
    ex5 = tmp_path / "X.ex5"
    ex5.write_bytes(b"x")
    assert _compilacion(0, ex5).pasa
    assert not _compilacion(1, ex5).pasa
    assert not _compilacion(0, None).pasa
    assert not _compilacion(0, tmp_path / "no-existe.ex5").pasa


def test_el_log_del_anexo_va_en_utf8_y_lf_con_el_sha_del_original(tmp_path: Path) -> None:
    original = _log_de_fase0("compilar-medirdemoftmo-ok.log")
    texto, errores, avisos = leer_log(original)
    ex5 = tmp_path / "X.ex5"
    ex5.write_bytes(b"x")
    c = Compilacion("mql5/Experts/X.mq5", "a" * 64, original, texto, errores, avisos, 1, ex5)
    anexo = log_para_anexo(c, [("mql5/X.mqh", "!=", "==")])
    assert "\r" not in anexo and anexo.endswith("\n")
    assert "PASA" in anexo and "sustitucion a proposito" in anexo
    assert hashlib.sha256(original).hexdigest() in anexo


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "mql5" / "Experts").mkdir(parents=True)
    (repo / "otro").mkdir()
    (repo / "mql5" / "Experts" / "X.mq5").write_text("estadiado\n", encoding="utf-8")
    (repo / "otro" / "Y.txt").write_text("fuera\n", encoding="utf-8")
    for orden in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", "-C", str(repo), *orden], check=True, capture_output=True)
    return repo


def test_exportar_copia_mql5_del_indice_y_nada_mas(tmp_path: Path) -> None:
    repo = _repo(tmp_path)
    (repo / "mql5" / "Experts" / "X.mq5").write_text("sin estadiar\n", encoding="utf-8")
    destino = tmp_path / "copia"
    assert exportar(repo, destino) == ["mql5/Experts/X.mq5"]
    assert (destino / "mql5" / "Experts" / "X.mq5").read_text(encoding="utf-8") == "estadiado\n"
    assert not (destino / "otro").exists()


def test_exportar_sin_mql5_en_el_indice_falla(tmp_path: Path) -> None:
    repo = tmp_path / "vacio"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True, capture_output=True)
    with pytest.raises(CompilarError, match="indice"):
        exportar(repo, tmp_path / "copia")


def test_sustituir_exige_una_sola_aparicion(tmp_path: Path) -> None:
    f = tmp_path / "a.mqh"
    f.write_text("x != y;\n", encoding="utf-8")
    sustituir(tmp_path, "a.mqh", "!=", "==")
    assert f.read_text(encoding="utf-8") == "x == y;\n"
    with pytest.raises(CompilarError, match="0 veces"):
        sustituir(tmp_path, "a.mqh", "!=", "==")
    f.write_text("a; a;\n", encoding="utf-8")
    with pytest.raises(CompilarError, match="2 veces"):
        sustituir(tmp_path, "a.mqh", "a;", "b;")


def test_el_ini_lanza_el_script_y_cierra_el_terminal() -> None:
    ini = ini_de_pruebas("XYZ.prueba")
    assert ini.startswith("[StartUp]\r\n")
    assert "Script=Botsito\\BotsitoPruebasCapa\r\n" in ini
    assert "Symbol=XYZ.prueba\r\n" in ini and "ShutdownTerminal=1\r\n" in ini


def test_comparar_con_el_golden_en_los_dos_sentidos(tmp_path: Path) -> None:
    for g in GOLDEN.rglob("*.jsonl"):
        destino = tmp_path / g.relative_to(GOLDEN)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(g.read_bytes())
    assert comparar_con_golden(tmp_path, GOLDEN) == []
    roto = tmp_path / "rota" / "journal_20261028.jsonl"
    roto.write_bytes(roto.read_bytes().replace(b"REASON_REMOVE", b"REASON_REMOVF"))
    assert comparar_con_golden(tmp_path, GOLDEN) == [
        "rota/journal_20261028.jsonl: distinto del golden"
    ]
    roto.unlink()
    assert comparar_con_golden(tmp_path, GOLDEN) == [
        "rota/journal_20261028.jsonl: el script no lo escribio"
    ]


def test_el_resumen_del_script() -> None:
    assert resumen_de_resultado("OK|a\nRESUMEN|ok=18|fallos=0\n") == (18, 0)
    assert resumen_de_resultado("FALLO|a\nRESUMEN|ok=17|fallos=1\n") == (17, 1)
    with pytest.raises(CompilarError, match="RESUMEN"):
        resumen_de_resultado("OK|a\n")
