"""Lo que la capa de MT5 recibe del repo, generado y con su hash (R6a.2, rama trabajo/capa-generada;
ADR-0082 D5; respuesta del consultor a la PARADA de la fase 0, docs/validation/CAPA-GENERADA.md).

Escribe UN fichero, `mql5/Include/Botsito/Capa/Generado.mqh`, con:

- los parametros de firma, broker, instrumento y ejecucion y del perfil de cuenta que lee alguna
  pieza de R6a.3 a R6a.8 (`ENTRAN`; la tabla de la fase 0 dice por que entra cada uno y por que
  no los demas), cada uno con su valor y su estado (`P_<NOMBRE>` y `P_<NOMBRE>_ESTADO`): un
  DEFAULT_AMBIGUOUS no se lee como CONFIRMED;
- el calendario de cierres del perfil, como lo recibe el predicado de Python: `cubre` y los cierres
  ya juntos de `DefinicionCalendario.calendario()`, en segundos UTC, con su fuente;
- `CAPA_HASH`, en su propia linea: el SHA-256 (hexadecimal en minusculas) de los bytes del fichero
  SIN esa linea, quitada entera con su LF (`capa_hash`).

Todo son `const` y `enum` de MQL5: ni `#define` ni variables (D8). El fichero es UTF-8 sin BOM con
LF y no lleva fecha ni sha: regenerar sin cambiar los yaml da los mismos bytes.

Falla, sin escribir, si (D2 y respuesta a la PARADA, puntos 0 y 3):
- un nombre de `ENTRAN` no esta en ninguno de los dos ficheros, o esta sin valor (UNKNOWN);
- un nombre que esta en `parametros.yaml` y en el perfil difiere en tipo, valor, opciones o estado;
- `instrumento_stops_level` y `firma_stops_level_puntos` difieren (sale el primero);
- `firma_huso_corte` y `huso_operativa` no dan el mismo instante en la medianoche de cada dia de
  `cubre` (ADR-0053 §4), o `reloj_dia_riesgo` no es `civil_operativa` (la medianoche en
  `huso_operativa`, ADR-0027): entonces `firma_huso_corte` ya no resuelve el dia de riesgo.

Uso, por su ruta (la guardia de Claude Code no ejecuta `python -m` de un modulo que no sea
pytest), con la raiz del repositorio por argumento:

    uv run python src/botsito/mql5bridge/generar_capa.py --repo <raiz> --perfil <perfil>
    uv run python src/botsito/mql5bridge/generar_capa.py --repo <raiz> --perfil <perfil> --comprobar

La primera escribe el fichero; con `--comprobar` no escribe nada y sale con 1 si el fichero del repo
no es exactamente lo que generaria.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any

import yaml

from botsito.comun.husos import huso_canonico
from botsito.config.registro import Estado, Parametro, cargar_registro
from botsito.engine.calendario_cierres import cargar_calendario, ruta_calendario

GENERADO = Path("mql5") / "Include" / "Botsito" / "Capa" / "Generado.mqh"
REGISTRO = Path("knowledge") / "spec" / "parametros.yaml"
CUENTAS = Path("knowledge") / "cuentas"

# Lo que entra, en el orden del fichero (fase 0, tabla a; respuesta a la PARADA, puntos 0 a 3).
ENTRAN: tuple[str, ...] = (
    # instrumento
    "instrumento_digitos",
    "instrumento_contrato",
    "instrumento_lote_minimo",
    "instrumento_lote_paso",
    "instrumento_stops_level",
    # broker
    "broker_offset_base",
    "broker_dst",
    # perfil y firma
    "firma",
    "firma_programa",
    "firma_tipo_cuenta",
    "saldo_inicial_cuenta",
    "reloj_dia_riesgo",
    "firma_huso_corte",
    "firma_perdida_diaria_max",
    "firma_perdida_total_max",
    "firma_base_perdida_diaria",
    "firma_perdida_total_arrastra",
    "firma_magnitud_vigilada",
    "firma_cierre_al_tope",
    "firma_margen_seguridad",
    "firma_mensajes_dia_max",
    "firma_gap_margen_minutos",
    "firma_gap_cierre_minimo_minutos",
    "firma_apalancamiento",
    "firma_volumen_max_lotes",
    # ejecucion
    "freno_peticiones_aviso",
    "freno_peticiones_corte",
    "freno_bucle_repeticiones",
    "freno_bucle_minutos",
    "lote_si_no_cabe",
    "lote_margen_libre_fraccion",
)
# De cada pareja sale el primero; el segundo solo se compara (respuesta, punto 3).
SINONIMOS: tuple[tuple[str, str], ...] = (("instrumento_stops_level", "firma_stops_level_puntos"),)
# La pareja de relojes (respuesta, punto 0; ADR-0053 §4): sale el primero, el segundo no, y se
# comprueban por instantes. `reloj_dia_riesgo` tiene que nombrar el segundo.
RELOJ_CAPA, RELOJ_TRADER = "firma_huso_corte", "huso_operativa"
RELOJ_DIA_RIESGO, RELOJ_DIA_RIESGO_VALOR = "reloj_dia_riesgo", "civil_operativa"

_TIPO_MQL5 = {
    "fraccion": "double",
    "porcentaje": "double",
    "decimal": "double",
    "lotes": "double",
    "entero": "int",
    "minutos": "int",
    "puntos": "int",
    "booleano": "bool",
    "texto": "string",
    "hora": "string",
}
_OPCION = re.compile(r"[a-z][a-z0-9_]*")
_LINEA_HASH = re.compile(rb'^const string CAPA_HASH = "[0-9a-f]{64}";\n', re.MULTILINE)
_HUECO_HASH = "@@CAPA_HASH@@"


class GenerarError(ValueError):
    """Lo que impide generar: el mensaje dice que y donde. No se elige: se falla."""


@dataclass(frozen=True)
class Entrada:
    """Un parametro que entra: el leido por la puerta del registro y su valor tal como esta
    escrito."""

    parametro: Parametro
    bruto: Any
    origen: str


def capa_hash(contenido: bytes) -> str:
    """El hash de lo generado: SHA-256 de los bytes sin la unica linea de `CAPA_HASH`."""
    lineas = _LINEA_HASH.findall(contenido)
    if len(lineas) != 1:
        raise GenerarError(f"lo generado lleva {len(lineas)} lineas de CAPA_HASH, no una")
    return hashlib.sha256(_LINEA_HASH.sub(b"", contenido, count=1)).hexdigest()


def _brutos(ruta: Path) -> dict[str, Any]:
    datos = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    return {p["nombre"]: p.get("valor") for p in datos["parametros"]}


def _ruta_perfil(repo: Path, perfil: str) -> Path:
    return repo / CUENTAS / f"{perfil}.yaml"


def _iguales(a: Parametro, b: Parametro) -> list[str]:
    return [
        campo
        for campo in ("tipo", "valor", "opciones", "estado")
        if getattr(a, campo) != getattr(b, campo)
    ]


def leer_entradas(repo: Path, perfil: str) -> list[Entrada]:
    """Los parametros de `ENTRAN`, con las comprobaciones de D2 hechas. Lanza `GenerarError`."""
    ruta_r, ruta_p = repo / REGISTRO, _ruta_perfil(repo, perfil)
    registro, cuenta = cargar_registro(ruta_r), cargar_registro(ruta_p)
    brutos_r, brutos_p = _brutos(ruta_r), _brutos(ruta_p)
    comunes = sorted(set(registro.parametros) & set(cuenta.parametros))
    for n in comunes:
        distintos = _iguales(registro.parametros[n], cuenta.parametros[n])
        if distintos:
            raise GenerarError(
                f"{n} esta en {REGISTRO.as_posix()} y en el perfil con distinto "
                f"{', '.join(distintos)}"
            )
    for sale, comparado in SINONIMOS:
        a = registro.parametros.get(sale) or cuenta.parametros.get(sale)
        b = registro.parametros.get(comparado) or cuenta.parametros.get(comparado)
        if a is None or b is None:
            raise GenerarError(f"falta {sale if a is None else comparado} para compararlos")
        distintos = [c for c in ("tipo", "valor", "estado") if getattr(a, c) != getattr(b, c)]
        if distintos:
            raise GenerarError(f"{sale} y {comparado} difieren en {', '.join(distintos)}")
    entradas = []
    for n in ENTRAN:
        if n in registro.parametros:
            p, bruto = registro.parametros[n], brutos_r[n]
            origen = REGISTRO.as_posix() + (" y el perfil" if n in cuenta.parametros else "")
        elif n in cuenta.parametros:
            p, bruto, origen = cuenta.parametros[n], brutos_p[n], "el perfil"
        else:
            raise GenerarError(f"{n} no esta ni en {REGISTRO.as_posix()} ni en el perfil")
        if p.estado is Estado.UNKNOWN or p.valor is None:
            raise GenerarError(f"{n} no tiene valor (UNKNOWN): no se genera")
        if p.tipo not in _TIPO_MQL5 and p.tipo != "enum":
            raise GenerarError(f"{n}: tipo {p.tipo} sin forma en MQL5")
        entradas.append(Entrada(p, bruto, origen))
    return entradas


def comprobar_relojes(repo: Path, perfil: str, desde: date, hasta: date) -> None:
    """ADR-0053 §4: los dos relojes dan el mismo instante en la medianoche de cada dia de [desde,
    hasta] (las fechas de `cubre`), y `reloj_dia_riesgo` es la medianoche en `huso_operativa`."""
    registro = cargar_registro(repo / REGISTRO)
    cuenta = cargar_registro(_ruta_perfil(repo, perfil))
    dia_riesgo = registro.opcion(RELOJ_DIA_RIESGO)
    if dia_riesgo != RELOJ_DIA_RIESGO_VALOR:
        raise GenerarError(
            f"{RELOJ_DIA_RIESGO} es {dia_riesgo!r}: {RELOJ_CAPA} solo lo resuelve si es "
            f"{RELOJ_DIA_RIESGO_VALOR!r} (ADR-0027, ADR-0053 §4)"
        )
    capa = huso_canonico(cuenta.texto(RELOJ_CAPA))
    trader = huso_canonico(registro.texto(RELOJ_TRADER))
    dia = desde
    while dia <= hasta:
        a = datetime.combine(dia, time(0), tzinfo=capa).astimezone(UTC)
        b = datetime.combine(dia, time(0), tzinfo=trader).astimezone(UTC)
        if a != b:
            raise GenerarError(
                f"{RELOJ_CAPA} y {RELOJ_TRADER} no dan la misma medianoche el {dia.isoformat()}"
            )
        dia += timedelta(days=1)


def _literal(e: Entrada) -> tuple[str, str]:
    """(tipo de MQL5, literal) del valor, escrito como lo trae el yaml."""
    p, bruto = e.parametro, e.bruto
    if p.tipo == "enum":
        assert p.opciones is not None
        return f"ENUM_P_{p.nombre.upper()}", f"P_{p.nombre.upper()}_{str(bruto).upper()}"
    tipo = _TIPO_MQL5[p.tipo]
    if tipo == "bool":
        if not isinstance(bruto, bool):
            raise GenerarError(f"{p.nombre}: un booleano se escribe true o false")
        return tipo, "true" if bruto else "false"
    if tipo == "string":
        texto = str(bruto)
        if any(c in texto for c in '"\\') or not texto.isprintable():
            raise GenerarError(f"{p.nombre}: el texto lleva comillas, barras o controles")
        return tipo, f'"{texto}"'
    texto = str(bruto)
    if not re.fullmatch(r"-?\d+(\.\d+)?", texto):
        raise GenerarError(f"{p.nombre}: {texto!r} no es un numero escrito como se espera")
    if tipo == "int":
        if "." in texto:
            raise GenerarError(f"{p.nombre}: {texto!r} no es un entero")
        return tipo, texto
    return tipo, texto if "." in texto else texto + ".0"


def _enums(entradas: Sequence[Entrada]) -> list[str]:
    salida = [
        "// Los estados del registro (ADR-0002): un DEFAULT_AMBIGUOUS no es un CONFIRMED.",
        "enum ENUM_BOTSITO_ESTADO",
        "  {",
        "   BOTSITO_ESTADO_CONFIRMED,",
        "   BOTSITO_ESTADO_DEFAULT_AMBIGUOUS,",
        "   BOTSITO_ESTADO_UNKNOWN",
        "  };",
        "",
    ]
    for e in entradas:
        p = e.parametro
        if p.tipo != "enum":
            continue
        assert p.opciones is not None
        for o in p.opciones:
            if not _OPCION.fullmatch(o):
                raise GenerarError(f"{p.nombre}: la opcion {o!r} no se puede nombrar en MQL5")
        nombres = [f"P_{p.nombre.upper()}_{o.upper()}" for o in p.opciones]
        salida += [f"enum ENUM_P_{p.nombre.upper()}", "  {"]
        salida += [f"   {n}{',' if i < len(nombres) - 1 else ''}" for i, n in enumerate(nombres)]
        salida += ["  };", ""]
    return salida


def _parametros(entradas: Sequence[Entrada]) -> list[str]:
    salida = []
    for e in entradas:
        p = e.parametro
        tipo, literal = _literal(e)
        nota = f"// {p.nombre} · {p.tipo} · {p.categoria} · {e.origen}"
        if p.ambiguedad_id:
            nota += f" · {p.estado.value} bajo {p.ambiguedad_id}"
        salida += [
            nota,
            f"const {tipo} P_{p.nombre.upper()} = {literal};",
            f"const ENUM_BOTSITO_ESTADO P_{p.nombre.upper()}_ESTADO = "
            f"BOTSITO_ESTADO_{p.estado.value};",
            "",
        ]
    return salida


def _iso(segundos: int) -> str:
    return datetime.fromtimestamp(segundos, UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _segundos(ms: int, donde: str) -> int:
    if ms % 1000:
        raise GenerarError(f"{donde}: {ms} ms no cae en un segundo entero")
    return ms // 1000


def _calendario(repo: Path, perfil: str) -> list[str]:
    definicion = cargar_calendario(ruta_calendario(repo, perfil))
    cal = definicion.calendario()
    desde = _segundos(cal.cubre_desde_ms, "cubre.desde")
    hasta = _segundos(cal.cubre_hasta_ms, "cubre.hasta")
    cierres = [
        (_segundos(c.inicio_ms, c.fuente), _segundos(c.fin_ms, c.fuente), c.fuente)
        for c in cal.cierres
    ]
    for _, _, fuente in cierres:
        if any(x in fuente for x in '"\\') or not fuente.isprintable():
            raise GenerarError(
                f"la fuente de un cierre lleva comillas, barras o controles: {fuente!r}"
            )
    n = len(cierres)
    ruta = ruta_calendario(Path("."), perfil).as_posix().removeprefix("./")
    salida = [
        f"// El calendario de cierres de {ruta} (ADR-0068), como lo recibe el",
        "// predicado de Python: los cierres ya juntos de DefinicionCalendario.calendario(),",
        "// en segundos UTC, [inicio, fin). Fuera de [CIERRES_CUBRE_DESDE, CIERRES_CUBRE_HASTA)",
        "// no se sabe: el predicado niega (cierre_sin_calendario). Se filtra por duracion en",
        "// el predicado, no aqui.",
        f"const long CIERRES_CUBRE_DESDE = {desde}; // {_iso(desde)}",
        f"const long CIERRES_CUBRE_HASTA = {hasta}; // {_iso(hasta)}",
        f"const int  CIERRES_N = {n};",
        "",
        f"const long CIERRES_INICIO[{n}] =",
        "  {",
    ]
    salida += [
        f"   {i}{',' if k < n - 1 else ''} // {_iso(i)}" for k, (i, _, _) in enumerate(cierres)
    ]
    salida += ["  };", "", f"const long CIERRES_FIN[{n}] =", "  {"]
    salida += [
        f"   {f}{',' if k < n - 1 else ''} // {_iso(f)}" for k, (_, f, _) in enumerate(cierres)
    ]
    salida += ["  };", "", f"const string CIERRES_FUENTE[{n}] =", "  {"]
    salida += [f'   "{fu}"{"," if k < n - 1 else ""}' for k, (_, _, fu) in enumerate(cierres)]
    salida += ["  };", ""]
    return salida


def _fechas_de_cubre(repo: Path, perfil: str) -> tuple[date, date]:
    cubre = cargar_calendario(ruta_calendario(repo, perfil)).datos["cubre"]
    return date.fromisoformat(str(cubre["desde"])), date.fromisoformat(str(cubre["hasta"]))


def generar(repo: Path, perfil: str) -> bytes:
    """Los bytes de `Generado.mqh` para `perfil`, con su `CAPA_HASH`. Lanza `GenerarError`."""
    entradas = leer_entradas(repo, perfil)
    comprobar_relojes(repo, perfil, *_fechas_de_cubre(repo, perfil))
    calendario = _calendario(repo, perfil)
    cabecera = [
        "//+------------------------------------------------------------------+",
        "//| Generado.mqh - lo que la capa de MT5 recibe del repo (R6a.2,     |",
        "//| ADR-0082 D5). GENERADO: no se edita a mano.                      |",
        "//+------------------------------------------------------------------+",
        "// Se genera, desde la raiz del repositorio, con:",
        f"//   uv run python src/botsito/mql5bridge/generar_capa.py --repo . --perfil {perfil}",
        f"// desde {REGISTRO.as_posix()}, {(CUENTAS / perfil).as_posix()}.yaml y",
        f"// {ruta_calendario(Path('.'), perfil).as_posix().removeprefix('./')}.",
        "// Quien cambie uno de esos valores (una activacion, el perfil, el calendario)",
        "// regenera, y un test falla si este fichero no es exactamente lo que da el generador.",
        "// CAPA_HASH = SHA-256 de este fichero sin su linea (docs/validation/CAPA-GENERADA.md).",
        "",
    ]
    lineas = [
        *cabecera,
        *_enums(entradas),
        *_parametros(entradas),
        *calendario,
        f'const string CAPA_HASH = "{_HUECO_HASH}";',
        "//+------------------------------------------------------------------+",
    ]
    texto = "\n".join(lineas) + "\n"
    sin_hash = texto.replace(f'const string CAPA_HASH = "{_HUECO_HASH}";\n', "")
    h = hashlib.sha256(sin_hash.encode("utf-8")).hexdigest()
    contenido = texto.replace(_HUECO_HASH, h).encode("utf-8")
    assert capa_hash(contenido) == h
    return contenido


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Genera lo que la capa de MT5 recibe del repo (R6a.2).")
    p.add_argument("--repo", type=Path, required=True, help="la raiz del repositorio")
    p.add_argument("--perfil", required=True, help="el perfil de knowledge/cuentas/, sin .yaml")
    p.add_argument("--comprobar", action="store_true", help="no escribe: sale con 1 si difiere")
    a = p.parse_args(argv)
    try:
        nuevo = generar(a.repo, a.perfil)
    except GenerarError as e:
        print(f"NO SE GENERA: {e}")
        return 2
    destino = a.repo / GENERADO
    if a.comprobar:
        viejo = destino.read_bytes() if destino.is_file() else b""
        if viejo == nuevo:
            print(f"{GENERADO.as_posix()}: al dia (capa_hash {capa_hash(nuevo)})")
            return 0
        lv, ln = viejo.split(b"\n"), nuevo.split(b"\n")
        k = next(
            (i for i, (x, y) in enumerate(zip(lv, ln, strict=False)) if x != y),
            min(len(lv), len(ln)),
        )
        print(
            f"{GENERADO.as_posix()}: DISTINTO de lo que se genera (primera linea distinta: {k + 1})"
        )
        return 1
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(nuevo)
    print(f"{GENERADO.as_posix()}: escrito (capa_hash {capa_hash(nuevo)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
