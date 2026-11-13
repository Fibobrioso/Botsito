"""Compila la capa de MT5 con MetaEditor y ejecuta su script de pruebas en el terminal (R6a.1,
rama trabajo/ea-conexion; respuesta del consultor a la PARADA, punto 2).

Lo medido en la fase 0 (`docs/validation/EA-CONEXION.md` §0.a y §0.b) que este modulo respeta:

- MetaEditor sale con 1 cuando compila y con 0 cuando hay un error: su codigo de salida NO es la
  puerta. La puerta es la linea `Result: N errors, M warnings` de su log, con N = 0, y que exista el
  `.ex5`.
- El log es UTF-16LE con BOM y CRLF; a los anexos va en UTF-8 y LF, con el sha256 del original.
- MetaEditor deja el `.ex5` y el log junto al fuente: se compila una COPIA de `mql5/` exportada del
  INDICE de git (lo estadiado, que es lo que sella `make check`) a una carpeta temporal, nunca en el
  repo ni en la carpeta del terminal. `/include` apunta a la `mql5/` exportada.
- Al terminal solo se copia el `.ex5` (`--instalar`), a `MQL5\\Experts\\Botsito\\` o
  `MQL5\\Scripts\\Botsito\\`; los fuentes no salen del repo.
- El script de pruebas se lanza con `terminal64.exe /config:<ini>` (`[StartUp]`, `Script`,
  `ShutdownTerminal=1`) y escribe en `MQL5\\Files\\Botsito\\pruebas\\`.

Todas las rutas llegan por argumento (nada sale de `__file__`). Uso, por ruta (la guardia de Claude
Code no ejecuta `python -m` de un modulo que no sea pytest):

    uv run python src/botsito/mql5bridge/compilar.py compilar --repo <raiz> --metaeditor <exe>
        --salida <carpeta de anexos> [--instalar <carpeta de datos del terminal>]
        [--sustituir <ruta> <viejo> <nuevo>]... <fuente>...
    uv run python src/botsito/mql5bridge/compilar.py pruebas --terminal <exe>
        --datos <carpeta de datos del terminal> --simbolo <simbolo del grafico>
        --golden <tests/golden/journal_v2> --salida <carpeta de anexos> --repo <raiz>

`pruebas` compara con el golden, valida cada cadena, y (R6a.2) valida como v2 el journal aparte
`capa/capa_hash.jsonl`, que tiene que llevar el capa_hash del Generado.mqh del indice; al final
da el sha256 de cada fichero de la salida.

`--sustituir` cambia un texto, que tiene que aparecer exactamente una vez, en la copia exportada
antes de compilar: es como se rompen a proposito las pruebas dinamicas sin tocar el repo.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import shutil
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from botsito.mql5bridge.generar_capa import GENERADO, GenerarError, capa_hash
from botsito.mql5bridge.journal import JournalError, leer

CARPETA_PRUEBAS = ("Botsito", "pruebas")
# R6a.2 (respuesta del consultor a la PARADA, punto 6): el script de pruebas escribe aparte, FUERA
# de --golden, un journal v2 con el CAPA_HASH real de Generado.mqh; `pruebas` lo valida y compara su
# capa_hash con el recalculado desde el Generado.mqh del indice (lo que se compilo).
FICHERO_CAPA = Path("capa") / "capa_hash.jsonl"
SCRIPT_PRUEBAS = "Botsito\\BotsitoPruebasCapa"
_RESULT = re.compile(r"Result:\s+(\d+)\s+errors?,\s+(\d+)\s+warnings?")


class CompilarError(RuntimeError):
    """Algo que impide compilar o probar; el mensaje dice que."""


@dataclass(frozen=True)
class Compilacion:
    fuente: str
    sha_fuente: str
    log_original: bytes
    texto: str
    errores: int
    avisos: tuple[str, ...]
    codigo_salida: int
    ex5: Path | None

    @property
    def pasa(self) -> bool:
        """La puerta: 0 errores en el log y el `.ex5` existe (el codigo de salida no cuenta)."""
        return self.errores == 0 and self.ex5 is not None and self.ex5.is_file()


def leer_log(original: bytes) -> tuple[str, int, tuple[str, ...]]:
    """El texto del log de MetaEditor (UTF-16 con BOM), sus errores y sus avisos."""
    texto = original.decode("utf-16")
    resultados = list(_RESULT.finditer(texto))
    if not resultados:
        raise CompilarError("el log de MetaEditor no trae la linea `Result: N errors, M warnings`")
    m = resultados[-1]
    avisos = tuple(x for x in texto.splitlines() if " : warning " in x)
    if len(avisos) != int(m.group(2)):
        raise CompilarError(f"el log dice {m.group(2)} avisos y lista {len(avisos)}")
    return texto, int(m.group(1)), avisos


def exportar(repo: Path, destino: Path) -> list[str]:
    """Copia a `destino` los ficheros de `mql5/` tal como estan en el INDICE de git."""
    listado = subprocess.run(
        ["git", "-C", str(repo), "ls-files", "-z", "--", "mql5"],
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    ficheros = [f for f in listado.split("\0") if f]
    if not ficheros:
        raise CompilarError("no hay nada de mql5/ en el indice de git")
    prefijo = destino.resolve().as_posix().rstrip("/") + "/"
    subprocess.run(
        ["git", "-C", str(repo), "checkout-index", "-f", f"--prefix={prefijo}", "--", *ficheros],
        check=True,
        capture_output=True,
    )
    return ficheros


def sustituir(raiz: Path, ruta: str, viejo: str, nuevo: str) -> None:
    """Cambia `viejo` por `nuevo` en la copia exportada; `viejo` aparece exactamente una vez."""
    f = raiz / ruta
    texto = f.read_text(encoding="utf-8")
    n = texto.count(viejo)
    if n != 1:
        raise CompilarError(f"{ruta}: el texto a sustituir aparece {n} veces, no una")
    f.write_text(texto.replace(viejo, nuevo), encoding="utf-8", newline="\n")


def compilar_uno(metaeditor: Path, raiz: Path, fuente: str) -> Compilacion:
    """Compila `raiz/fuente` con `/include:raiz/mql5` y lee su log."""
    ruta = raiz / fuente
    log = ruta.with_suffix(".log")
    ex5 = ruta.with_suffix(".ex5")
    for viejo in (log, ex5):
        viejo.unlink(missing_ok=True)
    r = subprocess.run(
        [
            str(metaeditor),
            f"/compile:{ruta}",
            f"/include:{raiz / 'mql5'}",
            f"/log:{log}",
        ],
        check=False,
        capture_output=True,
    )
    if not log.is_file():
        raise CompilarError(f"MetaEditor no dejo log de {fuente} (salida {r.returncode})")
    original = log.read_bytes()
    texto, errores, avisos = leer_log(original)
    return Compilacion(
        fuente=fuente,
        sha_fuente=hashlib.sha256(ruta.read_bytes()).hexdigest(),
        log_original=original,
        texto=texto,
        errores=errores,
        avisos=avisos,
        codigo_salida=r.returncode,
        ex5=ex5 if ex5.is_file() else None,
    )


def log_para_anexo(c: Compilacion, sustituciones: Sequence[tuple[str, str, str]] = ()) -> str:
    """El log en UTF-8 y LF, con una cabecera que dice de donde sale y si pasa la puerta."""
    sha_log = hashlib.sha256(c.log_original).hexdigest()
    puerta = "PASA" if c.pasa else "NO PASA"
    ex5 = "si" if c.ex5 is not None else "no"
    cabecera = [
        f"# fuente: {c.fuente} (copia del indice de git; sha256 {c.sha_fuente})",
        f"# log original: UTF-16LE con BOM y CRLF, sha256 {sha_log}",
        f"# codigo de salida de MetaEditor: {c.codigo_salida} "
        "(1 con exito, 0 con error: no es la puerta)",
        f"# puerta: {puerta} ({c.errores} errores, {len(c.avisos)} avisos, .ex5 {ex5})",
    ]
    cabecera += [f"# aviso: {a}" for a in c.avisos]
    cabecera += [f"# sustitucion a proposito en {r}: {v!r} -> {n!r}" for r, v, n in sustituciones]
    return "\n".join([*cabecera, *c.texto.splitlines()]) + "\n"


def instalar(c: Compilacion, datos: Path) -> Path:
    """Copia el `.ex5` a `MQL5/Experts/Botsito/` o `MQL5/Scripts/Botsito/` del terminal."""
    if c.ex5 is None:
        raise CompilarError(f"{c.fuente}: no hay .ex5 que instalar")
    tipo = Path(c.fuente).parts[1]
    if tipo not in ("Experts", "Scripts"):
        raise CompilarError(f"{c.fuente}: solo se instalan Experts y Scripts")
    destino = datos / "MQL5" / tipo / "Botsito" / c.ex5.name
    destino.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(c.ex5, destino)
    return destino


def ini_de_pruebas(simbolo: str) -> str:
    """El fichero de arranque del terminal que lanza el script de pruebas y lo cierra al acabar."""
    lineas = [
        "[StartUp]",
        f"Script={SCRIPT_PRUEBAS}",
        f"Symbol={simbolo}",
        "Period=M1",
        "ShutdownTerminal=1",
    ]
    return "\r\n".join(lineas) + "\r\n"


def comparar_con_golden(salida: Path, golden: Path) -> list[str]:
    """Cada journal del golden frente al que escribio el script: las diferencias, o []."""
    diferencias = []
    for g in sorted(golden.rglob("*.jsonl")):
        rel = g.relative_to(golden)
        s = salida / rel
        if not s.is_file():
            diferencias.append(f"{rel.as_posix()}: el script no lo escribio")
        elif s.read_bytes() != g.read_bytes():
            diferencias.append(f"{rel.as_posix()}: distinto del golden")
    return diferencias


def comprobar_capa_hash(salida: Path, generado: bytes) -> list[str]:
    """El journal de `FICHERO_CAPA` que dejo el script: valida como v2 y cada linea lleva el
    capa_hash recalculado desde `generado` (los bytes de Generado.mqh). Los problemas, o []."""
    f = salida / FICHERO_CAPA
    if not f.is_file():
        return [f"{FICHERO_CAPA.as_posix()}: el script no lo escribio"]
    try:
        esperado = capa_hash(generado)
    except GenerarError as e:
        return [f"Generado.mqh: {e}"]
    try:
        lineas = leer([(FICHERO_CAPA.as_posix(), f.read_bytes())])
    except JournalError as e:
        return [f"{FICHERO_CAPA.as_posix()}: no valida: {e}"]
    problemas = []
    if not lineas:
        problemas.append(f"{FICHERO_CAPA.as_posix()}: sin lineas")
    for x in lineas:
        if x.objeto["v"] != 2:
            problemas.append(f"{FICHERO_CAPA.as_posix()}:{x.numero}: es v{x.objeto['v']}, no v2")
        elif x.objeto["capa_hash"] != esperado:
            problemas.append(
                f"{FICHERO_CAPA.as_posix()}:{x.numero}: capa_hash {x.objeto['capa_hash']} no es el "
                f"del Generado.mqh del repo ({esperado})"
            )
    return problemas


def generado_del_indice(repo: Path) -> bytes:
    """Los bytes de Generado.mqh tal como estan en el INDICE de git (lo que `compilar` exporta)."""
    r = subprocess.run(
        ["git", "-C", str(repo), "show", f":{GENERADO.as_posix()}"],
        check=False,
        capture_output=True,
    )
    if r.returncode != 0:
        raise CompilarError(f"{GENERADO.as_posix()} no esta en el indice de git")
    return r.stdout


def resumen_de_resultado(texto: str) -> tuple[int, int]:
    """(ok, fallos) de la linea RESUMEN del resultado del script."""
    m = re.search(r"^RESUMEN\|ok=(\d+)\|fallos=(\d+)$", texto, re.MULTILINE)
    if m is None:
        raise CompilarError("el resultado del script no trae la linea RESUMEN")
    return int(m.group(1)), int(m.group(2))


def _compilar(a: argparse.Namespace) -> int:
    a.salida.mkdir(parents=True, exist_ok=True)
    sustituciones = [tuple(s) for s in (a.sustituir or [])]
    todas = True
    with tempfile.TemporaryDirectory(prefix="botsito-mql5-") as tmp:
        raiz = Path(tmp)
        exportar(a.repo, raiz)
        for ruta, viejo, nuevo in sustituciones:
            sustituir(raiz, ruta, viejo, nuevo)
        for fuente in a.fuentes:
            c = compilar_uno(a.metaeditor, raiz, fuente)
            nombre = Path(fuente).stem + (f"-{a.etiqueta}" if a.etiqueta else "") + ".log"
            (a.salida / nombre).write_text(
                log_para_anexo(c, sustituciones), encoding="utf-8", newline="\n"
            )
            puerta = "PASA" if c.pasa else "NO PASA"
            print(f"{fuente}: {puerta} ({c.errores} errores, {len(c.avisos)} avisos)")
            todas = todas and c.pasa
            if c.pasa and a.instalar is not None:
                print(f"  instalado en {instalar(c, a.instalar)}")
    return 0 if todas else 1


def _pruebas(a: argparse.Namespace) -> int:
    carpeta = a.datos / "MQL5" / "Files" / Path(*CARPETA_PRUEBAS)
    resultado = carpeta / "resultado.txt"
    resultado.unlink(missing_ok=True)
    # Ni el del terminal ni el de la salida de otra corrida: si el script no lo escribe, falta.
    (carpeta / FICHERO_CAPA).unlink(missing_ok=True)
    (a.salida / FICHERO_CAPA).unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="botsito-ini-") as tmp:
        ini = Path(tmp) / "pruebas.ini"
        ini.write_text(ini_de_pruebas(a.simbolo), encoding="ascii", newline="")
        r = subprocess.run([str(a.terminal), f"/config:{ini}"], check=False, capture_output=True)
    if not resultado.is_file():
        raise CompilarError(f"el script no dejo {resultado} (salida del terminal {r.returncode})")
    a.salida.mkdir(parents=True, exist_ok=True)
    texto = resultado.read_bytes()
    (a.salida / "resultado.txt").write_bytes(texto)
    for j in sorted(carpeta.rglob("*.jsonl")):
        destino = a.salida / j.relative_to(carpeta)
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(j.read_bytes())
    ok, fallos = resumen_de_resultado(texto.decode("utf-8"))
    diferencias = comparar_con_golden(a.salida, a.golden)
    print(f"script: {ok} OK, {fallos} FALLO (salida del terminal {r.returncode})")
    for d in diferencias:
        print(f"golden: {d}")
    valido = True
    for cadena in sorted({g.parent for g in a.golden.rglob("*.jsonl")}):
        nombres = sorted(p.name for p in cadena.glob("*.jsonl"))
        sal = a.salida / cadena.relative_to(a.golden)
        try:
            leer([(n, (sal / n).read_bytes()) for n in nombres])
            print(f"validador: {cadena.name} valida")
        except (JournalError, FileNotFoundError) as e:
            print(f"validador: {cadena.name} NO valida: {e}")
            valido = False
    if not diferencias:
        print("golden: los journals del script son iguales byte a byte")
    capa = comprobar_capa_hash(a.salida, generado_del_indice(a.repo))
    for problema in capa:
        print(f"capa_hash: {problema}")
    if not capa:
        print(
            f"capa_hash: {FICHERO_CAPA.as_posix()} valida como v2 y lleva el capa_hash del "
            f"Generado.mqh del repo ({capa_hash(generado_del_indice(a.repo))})"
        )
    for f in sorted(p for p in a.salida.rglob("*") if p.is_file()):
        print(
            f"sha256 {hashlib.sha256(f.read_bytes()).hexdigest()} "
            f"{f.relative_to(a.salida).as_posix()}"
        )
    return 0 if fallos == 0 and not diferencias and valido and not capa else 1


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Compila la capa de MT5 y ejecuta sus pruebas.")
    sub = p.add_subparsers(dest="orden", required=True)
    c = sub.add_parser("compilar")
    c.add_argument("--repo", type=Path, required=True)
    c.add_argument("--metaeditor", type=Path, required=True)
    c.add_argument("--salida", type=Path, required=True)
    c.add_argument("--instalar", type=Path)
    c.add_argument("--etiqueta", default="")
    c.add_argument("--sustituir", nargs=3, action="append", metavar=("RUTA", "VIEJO", "NUEVO"))
    c.add_argument("fuentes", nargs="+")
    t = sub.add_parser("pruebas")
    t.add_argument("--terminal", type=Path, required=True)
    t.add_argument("--datos", type=Path, required=True)
    t.add_argument("--simbolo", required=True)
    t.add_argument("--golden", type=Path, required=True)
    t.add_argument("--salida", type=Path, required=True)
    t.add_argument("--repo", type=Path, required=True, help="de donde sale Generado.mqh (indice)")
    a = p.parse_args(argv)
    try:
        return _compilar(a) if a.orden == "compilar" else _pruebas(a)
    except CompilarError as e:
        print(f"ERROR: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
