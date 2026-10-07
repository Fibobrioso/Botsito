"""La guardia de Claude Code: un hook `PreToolUse` para Read, Grep, Glob, Bash y PowerShell.

Rama `trabajo/guardias-claude` (2026-10-01, docs/validation/GUARDIAS-CLAUDE.md). Es DEFENSA EN
PROFUNDIDAD: la barrera principal sigue siendo el codigo (`botsito.cases.holdout`, la compuerta del
arnes, el lector de libros), que esta guardia no toca. Lo que vigila es lo que el codigo no ve: lo
que la SESION abre directamente con sus herramientas.

Dos familias de reglas:

1. EL CONTENIDO PROTEGIDO no se lee (CLAUDE.md, «Que se puede mirar y que no», punto 3). Se puede
   listar, medir y hashear -stat, tamano, sha256, `botsito corpus inventory`-, pero no abrir:
   - `knowledge/cases/holdout/{1,2,3}/`, salvo su README;
   - los libros del trader (xlsx, csv...) de un mes que no sea de DESARROLLO legible -enero, abril
     y agosto, y solo mientras ninguno tenga un dia reservado-; por mes, porque un agregado no se
     trocea por dia (ADR-0037);
   - toda imagen del material adicional: puede ser una captura de Analytics (ADR-0038);
   - todo lo que haya en una carpeta `Backtest <mes> <ano>` de un mes no legible (marzo, recibido
     SIN ABRIR: docs/validation/REGISTRO-MARZO.md);
   - las hojas de las sesiones (`Sesiones/`), que traen las etiquetas del trader;
   - las transcripciones crudas de las sesiones con el trader en cuarentena
     (`scripts/transcribir_sesion.py`: «ninguna persona ni ningun modelo lee la cruda») y todo
     `*cruda-NO-LEER*`, este donde este; y los comandos de la CLI que las imprimen;
   - un fichero de `knowledge/cases/` o `data/visor/` con el id de un caso reservado en el nombre,
     y un registro de feedback que etiquete un caso reservado.
   Los casos reservados se leen de los `particiones.yaml` commiteados con la misma regla que
   `casos_reservados` (`tests/unit/test_guardia_claude.py` compara las dos).

2. LAS OPERACIONES PROHIBIDAS: `--no-verify`, `push --force`, borrar o mover tags, borrar una
   referencia remota que no sea una rama `trabajo/`, `feature/` o `fix/` (`trabajo/dieta-y-skills`:
   la `fix/<rama>` de la CI de Linux se borra al cerrar), `cherry-pick` y `rebase`, `rm -rf`
   sobre `data/`, `corpus/` o `knowledge/`, `make check` sin la salida a un fichero, un heredoc
   sin comillas con `\\` dentro y, en `main`, `git add -A`, `commit -a`, `revert` y
   `reset --hard`, y `branch -D` en cualquier rama.

3. LO QUE SE EJECUTA ES LO QUE SE LEYO (`trabajo/guion-mismo-comando`, 2026-10-07): toda ejecucion
   -un guion, codigo en linea, un heredoc, `make`, `pytest`, `botsito`, lo que lanza `find -exec`
   o un alias de git- pasa por UNA funcion, `exigir_ejecucion_verificable`, que niega por defecto:
   el guion tiene que existir y leerse al inspeccionar, y en el mismo comando solo puede ir antes
   o a la vez lo de una lista cerrada (`cd`, asignaciones literales, `export`, `set -e/-u/-o
   pipefail`, y detras, en la tuberia, filtros que no escriben). En PowerShell, ninguna ejecucion.

Un comando que no se puede decidir con seguridad -una ruta construida al ejecutarse, `eval`, un
`xargs` que lee contenido- SE BLOQUEA si podria llegar a material protegido, y el mensaje dice como
reescribirlo. Un fallo interno de la guardia bloquea solo lo que menciona material sensible.

Sin dependencias: solo la biblioteca estandar, porque corre con el Python del sistema y no con el
entorno del proyecto. Contrato con Claude Code: lee el JSON del evento por stdin; sale con 0 para
dejar pasar y con 2, y el motivo por stderr, para bloquear.
"""

from __future__ import annotations

import ast
import glob as globmod
import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import NoReturn

RAIZ = Path(__file__).resolve().parents[2]

# ------------------------------------------------------------------------------------ las reglas
# Cada bloqueo cita la regla que lo manda. Las de material, CLAUDE.md punto 3 y su ADR.
R_HOLDOUT = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3: `knowledge/cases/holdout/**` esta "
    "PROHIBIDO sin pasar por la puerta de ADR-0033 (`botsito.cases.holdout`)"
)
R_LIBRO = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3: el detalle por operacion de los dias "
    "reservados y todo AGREGADO sobre un rango con un dia reservado no se leen (ADR-0021 §1, "
    "ADR-0037); solo enero, abril y agosto son material de DESARROLLO. Las filas `dev` se leen "
    "por el codigo (`botsito casos ingerir`, `scripts/huso_por_velas.py`), no abriendo el libro"
)
R_SIN_ABRIR = (
    "CLAUDE.md, «Lo minimo para fijar el universo»: la columna de fechas la lee el CONSULTOR, una "
    "vez y antes del sorteo; un mes sin sortear no lo abre la sesion "
    "(docs/runbooks/ENTRADA-MARZO.md, PARADAS 0 y A; docs/validation/REGISTRO-MARZO.md)"
)
R_CAPTURA = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3: las capturas de Analytics de FX Replay, "
    "EN BLOQUE y de cualquier mes; una imagen del material adicional no se abre para ver que es "
    "(ADR-0038)"
)
R_HOJA = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3: la hoja de una sesion trae las etiquetas "
    "del trader, tambien las de los casos reservados"
)
R_CUARENTENA = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3, y `scripts/transcribir_sesion.py`: la "
    "cruda de una sesion con el trader no la lee ninguna persona ni ningun modelo; solo la version "
    "FILTRADA"
)
R_TRAMO = (
    "CLAUDE.md, «Las guardias de Claude Code»: los tramos no citables "
    "(`knowledge/corpus/tramos_no_citables.yaml`) de un video que no esta en cuarentena no se "
    "leen; la cruda de v6 queda exenta de la cuarentena SOLO con sus tramos bloqueados (decision "
    "del consultor del 2026-10-01)"
)
R_CASO = (
    "CLAUDE.md, «Que se puede mirar y que no», punto 3: un caso de una particion reservada "
    "(`casos_reservados`, `casos_ocultos`) no se lee sin la puerta de ADR-0033"
)
R_NO_VERIFY = (
    "CLAUDE.md, «main no se toca»: «Ningun commit sin el sello de `make check`, y NUNCA "
    "`--no-verify`»"
)
R_CHERRY = (
    "CLAUDE.md, «main no se toca»: «`cherry-pick` y `rebase` no pasan por `pre-commit`: no se "
    "usan para meter trabajo»"
)
R_FORCE = (
    "encargo de `trabajo/guardias-claude` y CLAUDE.md, «main no se toca» (`main` y el tag en un "
    "push atomico): no se reescribe historia publicada"
)
R_TAG = (
    "encargo de `trabajo/guardias-claude`: un tag `stable/*` es el ancla de un estado citado en "
    "PROJECT_STATE y en la trazabilidad (`historial.ANCLA_FUENTE`); no se borra ni se mueve"
)
R_RM = (
    "CLAUDE.md, «Regimenes de cambio»: `data/`, `corpus/` y `knowledge/` guardan material "
    "inmutable o que no esta en git"
)
R_DEVNULL = (
    "CLAUDE.md, «Trampas medidas»: «`make check` con la salida a un FICHERO, nunca a `/dev/null`»; "
    "la forma es `make check > make-check.log 2>&1`"
)
R_HEREDOC = (
    "CLAUDE.md, «Trampas medidas»: «Los regex se escriben con Write, nunca dentro de un heredoc "
    "con delimitador sin comillas» (`\\b` se vuelve BACKSPACE)"
)
R_ADD_A = (
    "docs/runbooks/RITUAL.md, correccion 4: «`git add PROJECT_STATE.md`, NUNCA `git add -A`»; en "
    "`main` se estadia nombrando el fichero"
)
R_BRANCH_D = (
    "docs/runbooks/RITUAL.md: «`-d` y no `-D`: si git se niega, es que algo no esta fusionado»"
)
R_REVERT = "docs/runbooks/RITUAL.md, «Si la CI sale roja»: «No se revierte `main`»"
R_FICHERO_OCULTO = (
    "ordenes del consultor del 2026-10-01 (`trabajo/cuarentena-por-defecto`): un fichero del "
    "repositorio que copia texto que hoy se oculta (sesion en cuarentena, tramo no citable o "
    "material reservado o sin sortear) no se lee: las propuestas de `knowledge/_proposals/` con "
    "segmentos ocultos y las salidas de medicion que ya no se reproducen. La lista la calcula "
    "`botsito.corpus.cuarentena` (`.claude/hooks/ficheros_con_ocultos.txt`)"
)
R_CRUDO = (
    "encargo de `trabajo/cuarentena-por-defecto`: los comandos que ensenan el corpus lo filtran "
    "por defecto (cuarentena de sesiones, tramos no citables y material reservado o sin sortear), "
    "y `--crudo` -o `crudo=True` en Python- es SOLO para Aleks, en su propia terminal, nunca para "
    "Claude. Los unicos llamadores de `crudo=True` son los de `AUTORIZADOS` en "
    "`tests/unit/test_cuarentena.py`, cada uno con su motivo, y los tests"
)
# `--cr` es el prefijo mas corto que argparse aceptaria por `--crudo` (abrevia las opciones
# largas); `crudo=` con cualquier valor que no sea False, y la clave "crudo" de un dict.
CRUDO_OPCION = re.compile(r"(?<![\w-])--cr(?:u(?:d(?:o)?)?)?(?![\w-])")
CRUDO_PYTHON = re.compile(r"\bcrudo\s*=\s*(?!False\b)\S|[\"']crudo[\"']\s*:")
# Lo que la regla deja pasar sin mirar: `make check` y `pytest` sin argumentos (orden del
# consultor).
# `make check` solo con su redireccion a un fichero: con cualquier otro argumento se mira
# (revisor de esta rama, A2).
SIN_MIRAR_CRUDO = re.compile(
    r"\s*(?:uv\s+run\s+)?(?:make\s+check(?:\s*>\s*[\w./\\-]+(?:\s+2>&1)?)?|pytest)\s*"
)


def exigir_sin_crudo(texto: str, donde: str) -> None:
    """Bloquea `--crudo` y `crudo=True` en un comando, en su codigo en linea o en un guion."""
    if SIN_MIRAR_CRUDO.fullmatch(texto):
        return
    if CRUDO_OPCION.search(texto) or CRUDO_PYTHON.search(texto):
        raise BloqueoError(f"{donde} pide el corpus SIN FILTRAR.\nRegla: {R_CRUDO}.")


R_BORRAR_REMOTO = (
    "docs/runbooks/RITUAL.md: la rama remota `fix/<rama>` de la CI de Linux se borra al final del "
    "ritual; un `git push` solo borra ramas `trabajo/`, `feature/` o `fix/` nombradas una a una, "
    "nunca `main` ni un tag (encargo de `trabajo/dieta-y-skills`)"
)

COMO_REESCRIBIR = (
    "Como reescribirlo: rutas LITERALES, sin `$VAR`, `$(...)`, `eval` ni `xargs` delante de un "
    "lector; un fichero, con la herramienta Read; y para el material protegido solo `stat`, "
    "`ls`, `du`, `wc -c`, `sha256sum` o `uv run botsito corpus inventory`."
)

# ---------------------------------------------------------------------- lo que se lee del repo
PARTICIONES_RESERVADAS = (
    "holdout-1",
    "holdout-2",
    "holdout-3",
    "fidelidad-1",
    "fidelidad-2",
    "fidelidad-3",
)
DIRECTORIOS_DE_REPARTO = (
    "knowledge/cases/kit",
    "knowledge/cases/fidelidad",
    "knowledge/cases/visto",
)
# Material de DESARROLLO (CLAUDE.md): legible solo mientras ninguno de sus dias este reservado.
MESES_DE_DESARROLLO = ("2026-01", "2026-04", "2026-08")
# Sesiones con el trader (drive_id: null en fuentes.yaml) cuya cruda SI se lee: v6 se transcribio
# y se leyo antes de que existiera la cuarentena, y su dia reservado esta RETIRADO del holdout
# (ADR-0041, docs/validation/V6-FUERA-DEL-HOLDOUT.md). Desde v7 la cruda no se lee.
SESIONES_SIN_CUARENTENA = frozenset({"v6"})
TRAMOS_NO_CITABLES = "knowledge/corpus/tramos_no_citables.yaml"
FICHEROS_OCULTOS = ".claude/hooks/ficheros_con_ocultos.txt"
# Lo que hay en la carpeta de una transcripcion y no es texto: se puede abrir aunque tenga tramos.
SIN_TEXTO = (".wav", ".sha256", ".sha256_video", "huella.txt", "video.sha256")
# Ficheros de una transcripcion que van por segmentos, una linea cada uno: con tramos, se leen
# por trozos (Read con offset y limit) que no los toquen.
POR_LINEAS = ("cruda.jsonl", "corregida.jsonl", "cruda.txt")
ACCIONES_DE_CASO = ("LABEL_CASE", "MARK_FALSE_POSITIVE", "MARK_FALSE_NEGATIVE", "BORDERLINE")

MATERIAL = "corpus/estrategia del trader/material adicional de su operativa"
SESIONES = "corpus/estrategia del trader/sesiones"
TRANSCRIPCIONES = "data/transcripciones"
HOLDOUT = "knowledge/cases/holdout"
RAICES_IGNORADAS = ("corpus", "data")  # fuera de git: ripgrep no entra desde fuera

EXT_LIBRO = (".xlsx", ".xls", ".xlsm", ".xlsb", ".csv", ".ods", ".tsv")
EXT_IMAGEN = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".tif", ".tiff", ".heic")
MESES = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "setiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
}
_MES = re.compile(r"(?<![a-z])(" + "|".join(MESES) + r")(?![a-z])\D{0,3}(\d{4})?")
_INSTANTE = re.compile(r"^(\d+):(\d{1,2}):(\d{1,2})(?:[.,](\d+))?$")
_CASO = re.compile(r"caso-[a-z0-9]+-(\d{4}-\d{2})-\d{2}")
_ASIGNACION = re.compile(r"^\s+([A-Za-z0-9_.-]+)\s*:\s*['\"]?([A-Za-z0-9_-]+)['\"]?\s*$")


class BloqueoError(Exception):
    """Lo que la guardia rechaza, con el motivo y la regla."""


@dataclass
class Politica:
    """Lo protegido, calculado del repositorio en cada evento (los ficheros son pequenos)."""

    raiz: Path

    @cached_property
    def raiz_norm(self) -> str:
        return _normcase(str(self.raiz))

    @cached_property
    def reservados(self) -> dict[str, str]:
        """`caso -> particion` de las particiones reservadas, como `casos_reservados`."""
        salida: dict[str, str] = {}
        for directorio in DIRECTORIOS_DE_REPARTO:
            for fichero in sorted((self.raiz / directorio).glob("*/particiones.yaml")):
                dentro = False
                for linea in fichero.read_text(encoding="utf-8").splitlines():
                    if re.match(r"^asignacion\s*:", linea):
                        dentro = True
                        continue
                    if dentro and linea and not linea[0].isspace() and not linea.startswith("#"):
                        dentro = False
                    m = _ASIGNACION.match(linea) if dentro else None
                    if m and m.group(2) in PARTICIONES_RESERVADAS:
                        salida[m.group(1)] = m.group(2)
        return salida

    @cached_property
    def meses_reservados(self) -> frozenset[str]:
        return frozenset(m.group(1) for c in self.reservados if (m := _CASO.search(c.lower())))

    @cached_property
    def meses_legibles(self) -> frozenset[str]:
        return frozenset(m for m in MESES_DE_DESARROLLO if m not in self.meses_reservados)

    @cached_property
    def sesiones_en_cuarentena(self) -> frozenset[str]:
        """Los videos de `fuentes.yaml` con `drive_id: null` (grabaciones de sesion), menos v6."""
        fuentes = self.raiz / "knowledge" / "corpus" / "fuentes.yaml"
        salida: set[str] = set()
        actual: str | None = None
        for linea in fuentes.read_text(encoding="utf-8").splitlines():
            if m := re.match(r"^\s*-\s*video_id:\s*['\"]?(\w+)", linea):
                actual = m.group(1)
            elif re.match(r"^\s*-\s", linea):
                actual = None
            elif actual and re.match(r"^\s*drive_id:\s*null\b", linea):
                salida.add(actual.lower())
        return frozenset(salida - SESIONES_SIN_CUARENTENA)

    @cached_property
    def tramos(self) -> dict[str, list[tuple[int, int]]]:
        """`video -> [(t0_ms, t1_ms)]` de `tramos_no_citables.yaml`."""
        salida: dict[str, list[tuple[int, int]]] = {}
        ruta = self.raiz / TRAMOS_NO_CITABLES
        if not ruta.is_file():
            return salida
        video: str | None = None
        t0: int | None = None
        for linea in ruta.read_text(encoding="utf-8").splitlines():
            if m := re.match(r"^\s*-\s*video_id:\s*['\"]?(\w+)", linea):
                video, t0 = m.group(1).lower(), None
            elif video and (m := re.match(r"^\s*t0:\s*['\"]?([\d:.]+)", linea)):
                t0 = a_ms(m.group(1))
            elif video and t0 is not None and (m := re.match(r"^\s*t1:\s*['\"]?([\d:.]+)", linea)):
                t1 = a_ms(m.group(1))
                if t1 is not None:
                    salida.setdefault(video, []).append((t0, t1))
                t0 = None
        return salida

    @cached_property
    def tramos_vigilados(self) -> dict[str, list[tuple[int, int]]]:
        """Los de los videos que no estan en cuarentena: los de una cuarentena ya no se leen."""
        return {v: t for v, t in self.tramos.items() if v not in self.sesiones_en_cuarentena}

    def tramo_que_solapa(self, video: str, a_ms: int, b_ms: int) -> tuple[int, int] | None:
        return next(
            (
                (t0, t1)
                for t0, t1 in self.tramos_vigilados.get(video.lower(), [])
                if a_ms <= t1 and t0 <= b_ms
            ),
            None,
        )

    def lineas_de_tramo(self, ruta: str) -> list[int] | None:
        """Las lineas (desde 1) de un fichero POR_LINEAS que caen en un tramo; None si no se
        pueden saber."""
        rel = self.relativa(ruta) or ""
        partes = rel.split("/")
        nombre = os.path.basename(ruta).lower()
        if len(partes) < 4 or nombre not in POR_LINEAS:
            return None
        video = partes[2]
        try:
            lineas = Path(ruta).read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return None
        intervalos: list[tuple[int, int] | None] = []
        if nombre.endswith(".jsonl"):
            for linea in lineas:
                try:
                    d = json.loads(linea)
                    intervalos.append((int(d["t0_ms"]), int(d["t1_ms"])))
                except (ValueError, KeyError, TypeError):
                    intervalos.append(None)
        else:
            inicios = [
                a_ms(m.group(1)) if (m := re.match(r"^\[([\d:.]+)\]", linea)) else None
                for linea in lineas
            ]
            for i, t0 in enumerate(inicios):
                siguiente = next((t for t in inicios[i + 1 :] if t is not None), None)
                fin = siguiente if siguiente is not None else 10**12
                intervalos.append((t0, fin) if t0 is not None else None)
        prohibidas = []
        for n, iv in enumerate(intervalos, start=1):
            if iv is None or self.tramo_que_solapa(video, iv[0], iv[1]):
                prohibidas.append(n)
        return prohibidas

    @cached_property
    def ficheros_ocultos(self) -> frozenset[str]:
        """Las rutas (relativas al repo, en minusculas) de la lista CALCULADA por
        `botsito.corpus.cuarentena` (la guardia no importa `botsito`: lee el fichero que genera
        `scripts/ficheros_con_ocultos.py`, y un test comprueba que coincide). Sin fichero,
        ninguna."""
        try:
            texto = (self.raiz / FICHEROS_OCULTOS).read_text(encoding="utf-8")
        except OSError:
            return frozenset()
        return frozenset(
            ln.strip().lower() for ln in texto.splitlines() if ln.strip() and not ln.startswith("#")
        )

    def _motivo_propuesta(self, ruta: str, nombre: str) -> str | None:
        # Segunda capa, la de antes: lo que pisa un tramo, con la copia de la guardia.
        m = re.match(r"^pr-(v\d+)-", nombre)
        if not m or m.group(1) not in self.tramos_vigilados:
            return None
        try:
            texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        t0s = [int(x) for x in re.findall(r"\bt0_ms:\s*(\d+)", texto)]
        t1s = [int(x) for x in re.findall(r"\bt1_ms:\s*(\d+)", texto)]
        for a, b in zip(t0s, t1s, strict=False):
            if self.tramo_que_solapa(m.group(1), a, b):
                return R_TRAMO
        return None

    # ---------------------------------------------------------------- decidir sobre una ruta
    def relativa(self, ruta: str) -> str | None:
        """La ruta relativa a la raiz, en minusculas y con `/`, o None si esta fuera."""
        n = _normcase(ruta)
        if n == self.raiz_norm:
            return ""
        if n.startswith(self.raiz_norm + "/"):
            return n[len(self.raiz_norm) + 1 :]
        return None

    def mes_de(self, texto: str) -> str | None:
        m = _MES.search(texto.lower())
        if not m or not m.group(2):
            return None
        return f"{m.group(2)}-{MESES[m.group(1)]:02d}"

    def motivo_fichero(self, ruta: str) -> str | None:
        """Por que no se puede leer el contenido de ESTE fichero, o None si se puede."""
        nombre = os.path.basename(ruta).lower()
        if "cruda-no-leer" in _normcase(ruta):
            return R_CUARENTENA
        rel = self.relativa(ruta)
        es_libro = nombre.endswith(EXT_LIBRO) and "backtesting-analytics" in nombre
        if es_libro and self.mes_de(nombre) not in self.meses_legibles:
            return self.regla_del_mes(self.mes_de(nombre))
        if rel is None:
            return None
        if rel in self.ficheros_ocultos:
            return R_FICHERO_OCULTO
        partes = rel.split("/")
        if rel.startswith(HOLDOUT + "/") and len(partes) > 4 and partes[3] in {"1", "2", "3"}:
            return None if nombre == "readme.md" and len(partes) == 5 else R_HOLDOUT
        if rel.startswith(MATERIAL + "/"):
            return self._motivo_material(rel)
        if rel.startswith(SESIONES + "/"):
            return R_HOJA
        en_transcripciones = rel.startswith(TRANSCRIPCIONES + "/") and len(partes) > 3
        if en_transcripciones and partes[2] in self.sesiones_en_cuarentena:
            return R_CUARENTENA
        if (
            en_transcripciones
            and partes[2] in self.tramos_vigilados
            and not nombre.endswith(SIN_TEXTO)
        ):
            return R_TRAMO
        if rel.startswith("knowledge/_proposals/") and nombre.endswith(".yaml"):
            return self._motivo_propuesta(ruta, nombre)
        if rel.startswith(("knowledge/cases/", "data/visor/")) and self._nombra_reservado(nombre):
            return R_CASO
        if rel.startswith("knowledge/feedback/") and nombre.endswith(".yaml"):
            return self._motivo_feedback(ruta)
        return None

    def _motivo_material(self, rel: str) -> str | None:
        resto = rel[len(MATERIAL) + 1 :]
        nombre = resto.rsplit("/", 1)[-1]
        if nombre.endswith(EXT_IMAGEN):
            return R_CAPTURA
        if "/" in resto:
            carpeta = resto.split("/", 1)[0]
            if carpeta.startswith("backtest") and self.mes_de(carpeta) not in self.meses_legibles:
                return self.regla_del_mes(self.mes_de(carpeta))
        if nombre.endswith(EXT_LIBRO) and self.mes_de(nombre) not in self.meses_legibles:
            return self.regla_del_mes(self.mes_de(nombre))
        return None

    def regla_del_mes(self, mes: str | None) -> str:
        """Un mes con dias reservados es un libro con holdout; uno sin sortear (o sin mes
        legible en el nombre), material recibido sin abrir."""
        return R_LIBRO if mes in self.meses_reservados else R_SIN_ABRIR

    def _nombra_reservado(self, nombre: str) -> bool:
        return any(c.lower() in nombre for c in self.reservados)

    def _motivo_feedback(self, ruta: str) -> str | None:
        try:
            texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        if any(a in texto for a in ACCIONES_DE_CASO) and any(c in texto for c in self.reservados):
            return R_CASO
        return None

    def motivo_directorio(self, ruta: str, respeta_ignore: bool) -> str | None:
        """Por que no se puede leer RECURSIVAMENTE este directorio: el primer fichero protegido
        que alcanzaria. `respeta_ignore`: la herramienta no entra en lo que ignora git (ripgrep,
        `git grep`) salvo que se le de una ruta de dentro."""
        rel = self.relativa(ruta)
        if rel is None:
            return None
        dentro_ignorado = rel.split("/")[0] in RAICES_IGNORADAS
        if rel == "knowledge/_proposals" or rel.startswith("knowledge/_proposals/"):
            # Solo con una ruta de dentro: desde mas arriba bloquearia toda busqueda del repo
            # (limite declarado en docs/validation/GUARDIAS-CLAUDE.md §1.7).
            return self._primer_protegido(Path(ruta))
        for zona in self._zonas():
            if rel.startswith(zona + "/"):  # el directorio esta DENTRO de una zona
                return self._primer_protegido(Path(ruta))
            contiene = rel == "" or zona == rel or zona.startswith(rel + "/")
            if not contiene:
                continue
            ignorada = zona.split("/")[0] in RAICES_IGNORADAS
            if respeta_ignore and ignorada and not dentro_ignorado:
                continue  # ripgrep no entra en lo ignorado si no se le da una ruta de dentro
            en_disco = self._ruta_real(zona)
            motivo = self._primer_protegido(en_disco) if en_disco else None
            if motivo:
                return motivo
        return None

    def _ruta_real(self, rel: str) -> Path | None:
        """La ruta de disco de `rel` (en minusculas), con la grafia de cada carpeta tal como esta.
        En Windows da igual; en Linux, `corpus/estrategia del trader` no existe y la segunda CI de
        la guardia (run 36891855700) lo midio: sin esto, la zona se daba por vacia."""
        actual = self.raiz
        for parte in rel.split("/"):
            if not parte:
                continue
            try:
                actual = next(h for h in actual.iterdir() if h.name.lower() == parte)
            except (OSError, StopIteration):
                return None
        return actual

    def _zonas(self) -> list[str]:
        zonas = [MATERIAL, SESIONES, f"{HOLDOUT}/1", f"{HOLDOUT}/2", f"{HOLDOUT}/3", "data/visor"]
        zonas += [f"{TRANSCRIPCIONES}/{v}" for v in sorted(self.sesiones_en_cuarentena)]
        zonas += [f"{TRANSCRIPCIONES}/{v}" for v in sorted(self.tramos_vigilados)]
        zonas += ["knowledge/feedback", "knowledge/cases"]
        return zonas

    def _primer_protegido(self, base: Path) -> str | None:
        if base.is_file():
            return self.motivo_fichero(str(base))
        if not base.is_dir():
            return None
        for actual, _dirs, ficheros in os.walk(base):
            for f in ficheros:
                motivo = self.motivo_fichero(os.path.join(actual, f))
                if motivo:
                    return motivo
        return None

    def motivo_ruta(
        self, ruta: str, recursivo: bool = False, respeta_ignore: bool = False
    ) -> str | None:
        if not os.path.isdir(ruta):
            return self.motivo_fichero(ruta)
        if recursivo:
            return self.motivo_directorio(ruta, respeta_ignore)
        return self.motivo_dentro_de_zona(ruta)

    def motivo_dentro_de_zona(self, ruta: str) -> str | None:
        """Un directorio pasado a un lector no recursivo: protegido si ESTA dentro de una zona
        con algo protegido (un `cat` de una carpeta falla, pero un `python x.py <carpeta>` no)."""
        rel = self.relativa(ruta)
        if rel is None:
            return None
        if any(rel == z or rel.startswith(z + "/") for z in self._zonas()):
            return self._primer_protegido(Path(ruta))
        return None


def a_ms(texto: str) -> int | None:
    """`h:mm:ss[.d]` en milisegundos, o None."""
    m = _INSTANTE.match(texto.strip())
    if not m:
        return None
    fraccion = int((m.group(4) or "0").ljust(3, "0")[:3])
    return (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))) * 1000 + fraccion


def _rangos(lineas: list[int]) -> str:
    trozos: list[str] = []
    for n in lineas:
        if trozos and int(trozos[-1].split("-")[-1]) == n - 1:
            trozos[-1] = f"{trozos[-1].split('-')[0]}-{n}"
        else:
            trozos.append(str(n))
    return ", ".join(trozos[:12]) + (" ..." if len(trozos) > 12 else "")


def _normcase(ruta: str) -> str:
    """La ruta normalizada, en minusculas y con `/`, en CUALQUIER sistema. `os.path.normcase` no
    vale: en Linux no toca nada, y la primera CI de esta guardia (run 36889215829) salio roja
    porque fuera de Windows ninguna ruta se reconocia dentro del repo."""
    normal = os.path.normpath(ruta)
    if os.altsep:
        normal = normal.replace(os.altsep, "/")
    return normal.replace(os.sep, "/").lower()


# ------------------------------------------------------------------------- el tokenizador bash
OPERADORES = (
    "&&", "||", ";;", "|&", "<<-", "<<<", "<<", ">>", ">&", "&>", ">|", "<&", "<>",
    ";", "|", "&", "(", ")", "<", ">", "\n",
)  # fmt: skip
SEPARADORES = {"&&", "||", ";;", "|&", ";", "|", "&", "(", ")", "\n"}
REDIRECCIONES = {">>", ">&", "&>", ">|", "<&", "<>", "<", ">", "<<<"}
_VAR = re.compile(r"\$(?:\{([^}]*)\}|([A-Za-z_][A-Za-z0-9_]*)|([0-9@*#?$!-]))")
VARIABLES_NO_RUTA = {"?", "#", "$", "!", "-"}


@dataclass
class Palabra:
    texto: str  # con marcas \x00S<n>\x00 (sustitucion) y \x00V<nombre>\x00 (variable)
    glob: bool = False
    op: bool = False
    pegada_a_siguiente: bool = False


@dataclass
class Heredoc:
    delimitador: str
    con_comillas: bool
    cuerpo: str = ""
    indice_palabra: int = 0  # la palabra del delimitador, para saber a que comando pertenece


@dataclass
class Lexico:
    palabras: list[Palabra] = field(default_factory=list)
    sustituciones: list[str] = field(default_factory=list)
    heredocs: list[Heredoc] = field(default_factory=list)


def tokenizar(texto: str) -> Lexico:
    lex = Lexico()
    i, n = 0, len(texto)
    actual: list[str] = []
    en_palabra = False
    glob = False
    pendientes: list[Heredoc] = []
    esperando_delim: Heredoc | None = None

    def cerrar(pegada: bool = False) -> None:
        nonlocal actual, en_palabra, glob, esperando_delim
        if en_palabra:
            p = Palabra("".join(actual), glob=glob, pegada_a_siguiente=pegada)
            if esperando_delim is not None:
                esperando_delim.delimitador = p.texto
                esperando_delim.indice_palabra = len(lex.palabras)
                pendientes.append(esperando_delim)
                esperando_delim = None
            lex.palabras.append(p)
        actual, en_palabra, glob = [], False, False

    def sustitucion(inicio: int, abre: str, cierra: str) -> int:
        """Desde `inicio` (justo tras la apertura), hasta el cierre equilibrado."""
        nivel, j, comilla = 1, inicio, ""
        while j < n:
            c = texto[j]
            if comilla:
                if c == comilla:
                    comilla = ""
                elif c == "\\" and comilla == '"':
                    j += 1
            elif c in "'\"":
                comilla = c
            elif c == "\\":
                j += 1
            elif abre and texto.startswith(abre, j):
                nivel += 1
            elif texto.startswith(cierra, j):
                nivel -= 1
                if nivel == 0:
                    return j
            j += 1
        raise BloqueoError("una sustitucion `$(...)` o con acentos graves sin cerrar")

    def expansion(j: int) -> int:
        """Un `$` sin comillas simples: devuelve el indice siguiente y anade la marca."""
        nonlocal en_palabra
        en_palabra = True
        if texto.startswith("$((", j):
            fin = sustitucion(j + 3, "((", "))")
            actual.append("0")
            return fin + 2
        if texto.startswith("$(", j):
            fin = sustitucion(j + 2, "(", ")")
            actual.append(f"\x00S{len(lex.sustituciones)}\x00")
            lex.sustituciones.append(texto[j + 2 : fin])
            return fin + 1
        m = _VAR.match(texto, j)
        if m:
            nombre = m.group(1) or m.group(2) or m.group(3)
            actual.append(f"\x00V{nombre}\x00")
            return m.end()
        actual.append("$")
        return j + 1

    while i < n:
        c = texto[i]
        # El delimitador suele ser la ultima palabra de la linea (`<<'EOF'` y salto): al llegar
        # al salto aun esta abierto, y sin cerrarlo aqui el cuerpo se leia como comandos de bash
        # y su primera linea se perdia (`trabajo/guion-mismo-comando`, medido en la fase 1).
        if c == "\n" and (pendientes or (esperando_delim is not None and en_palabra)):
            cerrar()
            lex.palabras.append(Palabra("\n", op=True))
            i += 1
            for h in pendientes:
                lineas: list[str] = []
                while i < n:
                    fin = texto.find("\n", i)
                    fin = n if fin < 0 else fin
                    linea = texto[i:fin]
                    i = fin + 1
                    if linea.lstrip("\t") == h.delimitador:
                        break
                    lineas.append(linea)
                h.cuerpo = "\n".join(lineas)
                lex.heredocs.append(h)
            pendientes = []
            continue
        if c in " \t\r":
            cerrar()
            i += 1
            continue
        if c == "#" and not en_palabra:
            fin = texto.find("\n", i)
            i = n if fin < 0 else fin
            continue
        op = next((o for o in OPERADORES if texto.startswith(o, i)), None)
        if op:
            pegada = en_palabra and op in REDIRECCIONES
            cerrar(pegada=pegada)
            lex.palabras.append(Palabra(op, op=True))
            if op in {"<<", "<<-"}:
                esperando_delim = Heredoc("", con_comillas=False)
            i += len(op)
            continue
        if c == "\\":
            en_palabra = True
            if i + 1 < n and texto[i + 1] == "\n":
                i += 2
                continue
            if i + 1 < n:
                actual.append(texto[i + 1])
            i += 2
            continue
        if c == "'":
            fin = texto.find("'", i + 1)
            if fin < 0:
                raise BloqueoError("una comilla simple sin cerrar")
            actual.append(texto[i + 1 : fin])
            en_palabra = True
            if esperando_delim is not None:
                esperando_delim.con_comillas = True
            i = fin + 1
            continue
        if c == "$" and texto.startswith("$'", i):
            fin = texto.find("'", i + 2)
            if fin < 0:
                raise BloqueoError("una comilla $'...' sin cerrar")
            actual.append(texto[i + 2 : fin])
            en_palabra = True
            i = fin + 1
            continue
        if c == '"':
            en_palabra = True
            if esperando_delim is not None:
                esperando_delim.con_comillas = True
            j = i + 1
            while j < n and texto[j] != '"':
                if texto[j] == "\\" and j + 1 < n and texto[j + 1] in '$`"\\\n':
                    actual.append(texto[j + 1])
                    j += 2
                elif texto[j] == "$":
                    j = expansion(j)
                elif texto[j] == "`":
                    fin = sustitucion(j + 1, "", "`")
                    actual.append(f"\x00S{len(lex.sustituciones)}\x00")
                    lex.sustituciones.append(texto[j + 1 : fin])
                    j = fin + 1
                else:
                    actual.append(texto[j])
                    j += 1
            if j >= n:
                raise BloqueoError("una comilla doble sin cerrar")
            i = j + 1
            continue
        if c == "$":
            i = expansion(i)
            continue
        if c == "`":
            fin = sustitucion(i + 1, "", "`")
            actual.append(f"\x00S{len(lex.sustituciones)}\x00")
            lex.sustituciones.append(texto[i + 1 : fin])
            en_palabra = True
            i = fin + 1
            continue
        if c in "*?[":
            glob = True
        actual.append(c)
        en_palabra = True
        i += 1
    cerrar()
    if pendientes:  # heredoc sin salto de linea final: cuerpo vacio
        lex.heredocs.extend(pendientes)
    return lex


# ----------------------------------------------------------------------- los comandos simples
@dataclass
class Comando:
    argv: list[Palabra]
    entradas: list[Palabra]  # destinos de `<`, `<<<`, `<&`, `<>`
    salidas: list[tuple[str, Palabra]]  # (operador, destino)
    asignaciones: dict[str, Palabra]
    heredocs: list[Heredoc]
    tras_tuberia: bool = False  # recibe por stdin la salida de otro comando
    separador: str = ""  # el que lo cierra: `&` lo deja en segundo plano


PALABRAS_CLAVE = {"then", "do", "else", "elif", "if", "while", "until", "!", "{", "}", "time"}
FINALES = {"done", "fi", "esac"}


def comandos(lex: Lexico) -> list[Comando]:
    salida: list[Comando] = []
    actual = Comando([], [], [], {}, [])
    heredoc_de = {h.indice_palabra: h for h in lex.heredocs}
    palabras = lex.palabras
    i = 0
    tuberia = False

    def cerrar(sep: str) -> None:
        nonlocal actual, tuberia
        if actual.argv or actual.salidas or actual.entradas or actual.asignaciones:
            actual.tras_tuberia = tuberia
            actual.separador = sep
            salida.append(actual)
        tuberia = sep in {"|", "|&"}
        actual = Comando([], [], [], {}, [])

    while i < len(palabras):
        p = palabras[i]
        if p.op and p.texto in SEPARADORES:
            cerrar(p.texto)
            i += 1
            continue
        if p.op and p.texto in {"<<", "<<-"}:
            if i + 1 in heredoc_de:
                actual.heredocs.append(heredoc_de[i + 1])
            i += 2
            continue
        if p.op and p.texto in REDIRECCIONES:
            destino = palabras[i + 1] if i + 1 < len(palabras) else Palabra("")
            if (
                actual.argv
                and actual.argv[-1].pegada_a_siguiente
                and actual.argv[-1].texto.isdigit()
            ):
                actual.argv.pop()  # `2>`: el numero es el descriptor, no un argumento
            if p.texto in {"<", "<<<", "<&", "<>"}:
                actual.entradas.append(destino)
            else:
                actual.salidas.append((p.texto, destino))
            i += 2
            continue
        if not actual.argv and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", p.texto) and not p.op:
            nombre, valor = p.texto.split("=", 1)
            actual.asignaciones[nombre] = Palabra(valor, glob=False)
            i += 1
            continue
        if not actual.argv and p.texto in PALABRAS_CLAVE:
            i += 1
            continue
        if not actual.argv and p.texto in FINALES:
            i += 1
            continue
        actual.argv.append(p)
        i += 1
    cerrar("")
    return salida


# ------------------------------------------------------------------------ el analisis de bash
LECTOR_DE_METADATOS = {
    "stat", "ls", "dir", "du", "df", "sha256sum", "sha1sum", "sha512sum", "md5sum", "b2sum",
    "cksum", "test", "[", "realpath", "readlink", "basename", "dirname", "mkdir", "touch",
    "echo", "printf", "true", "false", "pwd", "export", "unset", "sleep", "date", "which",
    "type", "command", "cd", "rmdir", "ln", "chmod", "tree", "local", "declare", "read",
    "set", "shift", "return", "exit", "wait", "kill", "jobs", "trap", "env", "uname", "whoami",
    "hostname", "nproc", "seq", "tty", "clear", "hash", "alias", "help", "history",
}  # fmt: skip
# No leen el contenido de sus argumentos de ruta (o el del proyecto, que es su puerta).
SIN_LECTURA_DE_RUTAS = {"make", "rm", "mv", "curl", "wget", "gh", "uv", "cmake", "ffprobe"}
RECURSIVOS_CON_IGNORE = {"rg"}
ARCHIVADORES = {"tar", "zip", "7z", "7za"}
INTERPRETES = {"python", "python3", "py", "node", "perl", "ruby", "deno", "bun", "Rscript"}
SHELLS = {"bash", "sh", "zsh", "dash"}
# `$(...)` cuya salida no es una ruta: un sha, una rama, una fecha.
SUSTITUCIONES_SIN_RUTA = re.compile(
    r"^\s*(git\s+(rev-parse(\s+[-\w./^{}~@]+)+|branch\s+--show-current"
    r"|merge-base(\s+[-\w./]+){2}|describe(\s+[-\w./=]+)*|log\s+-1(\s+--format=%\w+)?(\s+[-\w./]+)*"
    r"|symbolic-ref\s+--short\s+HEAD)|date(\s+[-+][^|;&]*)?|whoami|hostname|nproc)\s*$"
)
CODIGO_QUE_RECORRE = re.compile(r"\b(os\.walk|walk|glob|rglob|iterdir|listdir|scandir)\s*\(")
SCRIPTS_CON_PUERTA = {"scripts/huso_por_velas.py"}  # leen solo las filas `dev` (ADR-0039 §5)
CLI_QUE_IMPRIME_CRUDA = {
    ("corpus", "frames", "show"),
    ("corpus", "transcript", "show"),
    ("kb", "at"),
}


@dataclass
class Contexto:
    politica: Politica
    cwd: str
    variables: dict[str, list[str]] = field(default_factory=dict)
    rama: str | None = None
    rama_leida: bool = False
    profundidad: int = 0
    # Para `exigir_ejecucion_verificable`: los comandos de ESTE nivel (lo que va antes y a la vez
    # de una ejecucion), su lexico (sus sustituciones), si el nivel corre dentro de un `$(...)` y
    # si es PowerShell.
    secuencia: list[Comando] = field(default_factory=list)
    posicion: int = 0
    nivel: Lexico | None = None
    en_sustitucion: bool = False
    powershell: bool = False

    def rama_actual(self) -> str:
        if not self.rama_leida:
            self.rama_leida = True
            try:
                r = subprocess.run(
                    ["git", "symbolic-ref", "--short", "-q", "HEAD"],
                    cwd=self.politica.raiz,
                    capture_output=True,
                    encoding="utf-8",
                    timeout=10,
                    check=False,
                )
                self.rama = r.stdout.strip()
            except (OSError, subprocess.SubprocessError):
                self.rama = ""
        return self.rama or ""


class DinamicoError(Exception):
    """Una palabra cuyo valor solo se sabe al ejecutar."""


def resolver(p: Palabra, ctx: Contexto, lex: Lexico, max_valores: int = 256) -> list[str]:
    """Los valores posibles de una palabra (con globs expandidos), o `DinamicoError`."""
    valores = [""]
    for trozo in re.split(r"(\x00[SV][^\x00]*\x00)", p.texto):
        if not trozo:
            continue
        if trozo.startswith("\x00S"):
            interior = lex.sustituciones[int(trozo[2:-1])]
            if re.match(r"^\s*pwd\s*$", interior):
                opciones = [ctx.cwd]
            elif re.match(r"^\s*git\s+rev-parse\s+--show-toplevel\s*$", interior):
                opciones = [str(ctx.politica.raiz)]
            elif SUSTITUCIONES_SIN_RUTA.match(interior):
                opciones = ["x"]
            else:
                raise DinamicoError(f"$({interior.strip()})")
        elif trozo.startswith("\x00V"):
            nombre = trozo[2:-1]
            base = re.split(r"[:#%/^,@\[]", nombre, maxsplit=1)[0]
            if base in VARIABLES_NO_RUTA:
                opciones = ["0"]
            elif base in ctx.variables:
                opciones = ctx.variables[base]
            elif base == "PWD":
                opciones = [ctx.cwd]
            elif base == "CLAUDE_PROJECT_DIR":
                opciones = [str(ctx.politica.raiz)]
            elif base in os.environ and base == nombre:
                opciones = [os.environ[base]]
            else:
                raise DinamicoError(f"${nombre}")
        else:
            opciones = [trozo]
        valores = [v + o for v in valores for o in opciones]
        if len(valores) > max_valores:
            raise DinamicoError(p.texto)
    if valores and valores[0].startswith("~"):
        valores = [os.path.expanduser(v) for v in valores]
    if not p.glob:
        return valores
    expandidos: list[str] = []
    for v in valores:
        patron = _absoluta(v, ctx.cwd)
        encontrados = globmod.glob(patron, recursive=True)
        expandidos.extend(encontrados or [v])
        if len(expandidos) > 5000:
            raise DinamicoError(f"{v} (el glob abarca demasiados ficheros)")
    return expandidos


def _absoluta(ruta: str, cwd: str) -> str:
    r = ruta.strip()
    m = re.match(r"^/(?:cygdrive/)?([a-zA-Z])(/.*)?$", r)
    if m:
        r = f"{m.group(1).upper()}:{m.group(2) or '/'}"
    elif r.startswith("~"):
        r = os.path.expanduser(r)
    relativa = not os.path.isabs(r) or re.match(r"^[\\/](?![\\/])", r)
    if relativa and not re.match(r"^[a-zA-Z]:", r):
        r = os.path.join(cwd, r)
    return os.path.normpath(r)


def candidatos_de_ruta(valor: str) -> Iterator[str]:
    """Las rutas que puede esconder un argumento: el mismo, `--x=ruta`, `rev:ruta` y `@ruta`."""
    yield valor
    if "=" in valor:
        yield valor.split("=", 1)[1]
    m = re.match(r"^[^:/\\]{2,}:(.+)$", valor)
    if m:
        yield m.group(1)
    if valor.startswith("@"):
        yield valor[1:]


def analizar_bash(texto: str, ctx: Contexto) -> None:
    """Lanza `BloqueoError` si el comando lee algo protegido, hace algo prohibido o no se puede
    decidir y podria leer algo protegido."""
    if ctx.profundidad > 4:
        raise BloqueoError("demasiados niveles de `bash -c` o `$(...)` anidados para decidir")
    exigir_sin_crudo(texto, "el comando")
    lex = tokenizar(texto)
    for h in lex.heredocs:
        if not h.con_comillas and "\\" in h.cuerpo:
            raise BloqueoError(
                f"un heredoc con delimitador sin comillas (`<<{h.delimitador}`) y `\\` dentro.\n"
                f"Regla: {R_HEREDOC}.\nComo reescribirlo: `<<'{h.delimitador}'`, o el fichero "
                "con la herramienta Write."
            )
    for interior in lex.sustituciones:
        analizar_bash(interior, _sub(ctx, en_sustitucion=True))
    bucle: str | None = None
    secuencia = comandos(lex)
    for posicion, cmd in enumerate(secuencia):
        ctx.secuencia, ctx.posicion, ctx.nivel = secuencia, posicion, lex
        for nombre, valor in cmd.asignaciones.items():
            try:
                ctx.variables[nombre] = resolver(valor, ctx, lex)
            except DinamicoError:
                ctx.variables.pop(nombre, None)
        if not cmd.argv:
            continue
        cabeza = cmd.argv[0].texto
        if cabeza == "for" and len(cmd.argv) >= 3 and cmd.argv[2].texto == "in":
            bucle = cmd.argv[1].texto
            valores: list[str] = []
            try:
                for p in cmd.argv[3:]:
                    valores.extend(resolver(p, ctx, lex))
                ctx.variables[bucle] = valores
            except DinamicoError:
                ctx.variables.pop(bucle, None)
            continue
        if cabeza == "for":
            continue
        analizar_comando(cmd, ctx, lex)


def _sub(
    ctx: Contexto, en_sustitucion: bool | None = None, powershell: bool | None = None
) -> Contexto:
    """Un contexto para analizar codigo anidado (`$(...)`, `bash -c`, un guion de shell)."""
    sub = Contexto(ctx.politica, ctx.cwd, dict(ctx.variables), ctx.rama, ctx.rama_leida)
    sub.profundidad = ctx.profundidad + 1
    sub.en_sustitucion = ctx.en_sustitucion if en_sustitucion is None else en_sustitucion
    sub.powershell = ctx.powershell if powershell is None else powershell
    return sub


def _valores(p: Palabra, ctx: Contexto, lex: Lexico) -> list[str] | None:
    try:
        return resolver(p, ctx, lex)
    except DinamicoError:
        return None


# Las opciones de `uv run` (uv 0.9): las que toman valor y las que no. Una que no esta en ninguna de
# las dos se niega: sin saber si toma valor, no se sabe que programa ejecuta (lista cerrada).
UV_RUN_CON_VALOR = frozenset({
    "--with", "-w", "--with-requirements", "--with-editable", "--python", "-p", "--group",
    "--only-group", "--no-group", "--extra", "--no-extra", "--directory", "--project",
    "--env-file", "--package", "--index", "--default-index", "--index-url", "--extra-index-url",
    "--find-links", "-f", "--config-file", "--cache-dir", "--exclude-newer", "--index-strategy",
    "--keyring-provider", "--resolution", "--prerelease", "--link-mode", "--python-platform",
    "--color", "--refresh-package", "--reinstall-package", "--upgrade-package", "-P",
    "--no-binary-package", "--no-build-package", "--config-setting", "-C",
    "--allow-insecure-host",
})  # fmt: skip
UV_RUN_SIN_VALOR = frozenset({
    "--no-sync", "--frozen", "--locked", "--isolated", "--no-project", "--script", "-s",
    "--gui-script", "--quiet", "-q", "--verbose", "-v", "--offline", "--active", "--no-active",
    "--all-extras", "--no-dev", "--dev", "--all-groups", "--no-default-groups",
    "--all-packages", "--no-env-file", "--no-editable", "--exact", "--inexact", "--no-cache",
    "-n", "--native-tls", "--no-progress", "--no-config", "--compile-bytecode", "--refresh",
    "--upgrade", "-U", "--reinstall", "--no-build-isolation", "--no-sources", "--no-build",
    "--no-binary", "--no-python-downloads", "--managed-python", "--no-managed-python",
    "--preview", "--no-preview", "--show-resolution",
})  # fmt: skip


def _saltar_opciones(argv: list[Palabra], con_valor: set[str]) -> list[Palabra]:
    while argv and argv[0].texto.startswith("-") and argv[0].texto != "-":
        if argv[0].texto == "--":
            return argv[1:]
        argv = argv[2:] if argv[0].texto in con_valor else argv[1:]
    return argv


class IndecidibleError(Exception):
    """Una via que no sabe que se ejecutara: lo decide `exigir_ejecucion_verificable`."""


# Las opciones de cada envoltorio, cerradas: (las que toman valor, las que no). Una que no esta se
# niega, porque sin saber si toma valor no se sabe que programa corre (revisor, A3).
OPCIONES_DE_ENVOLTORIO: dict[str, tuple[set[str], set[str]]] = {
    "timeout": (
        {"-s", "--signal", "-k", "--kill-after"},
        {"--preserve-status", "--foreground", "-v", "--verbose"},
    ),
    "nice": ({"-n", "--adjustment"}, set()),
    "stdbuf": ({"-i", "-o", "-e", "--input", "--output", "--error"}, set()),
    "exec": ({"-a"}, {"-c", "-l"}),
    "nohup": (set(), set()),
    "command": (set(), {"-p"}),
    "builtin": (set(), set()),
    "noglob": (set(), set()),
    "time": (set(), {"-p"}),
    "uv": (set(UV_RUN_CON_VALOR), set(UV_RUN_SIN_VALOR) | {"--version", "-V", "--help", "-h"}),
}


def _opciones_cerradas(argv: list[Palabra], nombre: str) -> list[Palabra]:
    con_valor, sin_valor = OPCIONES_DE_ENVOLTORIO[nombre]
    while argv and argv[0].texto.startswith("-") and argv[0].texto != "-":
        t = argv[0].texto
        if t == "--":
            return argv[1:]
        clave, igual, _valor = t.partition("=")
        corta = (nombre == "nice" and re.fullmatch(r"-n?\d+", t)) or (
            nombre == "stdbuf" and re.fullmatch(r"-[ioe]\S+", t)
        )
        if clave in con_valor:
            argv = argv[1:] if igual else argv[2:]
        elif t in sin_valor or corta:
            argv = argv[1:]
        else:
            raise IndecidibleError(
                f"`{nombre} {t}`: una opcion que la guardia no conoce; sin saber si toma valor, "
                "no sabe que programa ejecuta"
            )
    return argv


def _envoltorios(argv: list[Palabra]) -> list[Palabra]:
    """`timeout 5 x`, `nice -n 5 x`, `/usr/bin/env A=1 x`, `uv -q run [--opciones] x`, `uvx x` ->
    `x`, con sus opciones (por el NOMBRE del programa, no por su texto: revisor, B1). Lo que no se
    sabe quitar con seguridad lanza `IndecidibleError`, y lo decide `exigir_ejecucion_verificable`
    (encargo de `trabajo/guion-mismo-comando`)."""
    while argv:
        if "\x00" in argv[0].texto:
            break
        c = _nombre_de_programa(argv[0].texto)
        if c == "timeout":
            argv = _opciones_cerradas(argv[1:], "timeout")
            if not argv:
                return []
            if not re.fullmatch(r"\d+(\.\d+)?[smhd]?", argv[0].texto):
                raise IndecidibleError(f"`timeout {argv[0].texto}`: no es una duracion literal")
            argv = argv[1:]
        elif c == "command" and len(argv) > 1 and argv[1].texto in {"-v", "-V"}:
            return []  # `command -v x` busca `x`, no lo ejecuta
        elif c in {"nice", "stdbuf", "exec", "nohup", "command", "builtin", "noglob", "time"}:
            argv = _opciones_cerradas(argv[1:], c)
        elif c == "env":
            argv = argv[1:]
            while argv and (argv[0].texto.startswith("-") or "=" in argv[0].texto):
                t = argv[0].texto
                if t in {"-S", "--split-string"} or t.startswith(("-S", "--split-string=")):
                    raise IndecidibleError(f"`env {t}` parte una cadena en un comando que no ve")
                if "\x00" in t:
                    raise IndecidibleError("`env` con un valor que se construye al ejecutarse")
                argv = argv[2:] if t in {"-u", "--unset", "-C", "--chdir"} else argv[1:]
        elif c in {"uv", "uvx"}:
            resto = _opciones_cerradas(argv[1:], "uv")  # las globales de `uv`
            textos = [a.texto for a in resto[:2]]
            if c == "uvx":
                pass
            elif textos[:1] == ["run"]:
                resto = resto[1:]
            elif textos == ["tool", "run"]:
                resto = resto[2:]
            else:
                break  # `uv sync`, `uv pip ...`: no ejecuta un programa de la rama
            argv = resto
            while argv and argv[0].texto.startswith("-"):
                t = argv[0].texto
                clave, igual, valor = t.partition("=")
                if clave in {"-m", "--module"}:  # `uv run -m x` es `python -m x`
                    modulo = [Palabra(valor)] if igual else []
                    return [Palabra("python"), Palabra("-m"), *modulo, *argv[1:]]
                argv = _opciones_cerradas(argv, "uv")
        else:
            break
    return argv


def _quitar_envoltorios(argv: list[Palabra]) -> list[Palabra]:
    """Lo mismo que `_envoltorios`, sin lanzar: para `solo_lectura.py`, que lo importa (revisor,
    A4). Lo que no se sabe quitar se devuelve tal cual."""
    try:
        return _envoltorios(argv)
    except IndecidibleError:
        return argv


def analizar_comando(cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    try:
        argv = _envoltorios(cmd.argv)
    except IndecidibleError as exc:
        que = " ".join(p.texto for p in cmd.argv[:3])
        exigir_ejecucion_verificable(ctx, lex, cmd, que, indecidible=str(exc))
        return
    if not argv:
        return
    if "\x00" in argv[0].texto:  # `$PY x.py`: el programa, si se sabe, es su valor
        vals = _valores(argv[0], ctx, lex)
        if vals is None or len(vals) != 1:
            exigir_ejecucion_verificable(
                ctx, lex, cmd, argv[0].texto, indecidible="el programa se construye al ejecutarse"
            )
        argv = [Palabra((vals or [""])[0]), *argv[1:]]
    if argv[0].glob or re.search(r"\{[^}]*(,|\.\.)[^}]*\}", argv[0].texto):
        exigir_ejecucion_verificable(
            ctx,
            lex,
            cmd,
            argv[0].texto,
            indecidible="el programa lleva un comodin o una expansion de llaves: se construye al "
            "ejecutarse",
        )
    prog = os.path.basename(argv[0].texto).lower()
    for ext in (".exe", ".cmd", ".bat"):
        prog = prog.removesuffix(ext)
    args = argv[1:]

    for destino in cmd.entradas:  # `< fichero` lee su contenido
        _exigir_legible(destino, ctx, lex, "redireccion de entrada")

    if prog == "cd":
        if not args:  # `cd` a secas va a HOME (revisor, B4)
            ctx.cwd = os.path.expanduser("~")
        else:
            vals = _valores(args[0], ctx, lex)
            if vals and len(vals) == 1:
                ctx.cwd = _absoluta(vals[0], ctx.cwd)
        return
    if prog == "git":
        _analizar_git(args, cmd, ctx, lex)
        return
    if prog == "rm":
        _analizar_rm(args, ctx, lex)
        return
    if prog == "make":
        _analizar_make(args, cmd, ctx, lex)
        return
    if prog in {"eval", "source", "."}:
        exigir_ejecucion_verificable(
            ctx, lex, cmd, prog, indecidible=f"`{prog}` ejecuta texto que solo se conoce al correr"
        )
    if prog == "xargs":
        _analizar_xargs(args, cmd, ctx, lex)
        return
    if prog == "find":
        _analizar_find(args, cmd, ctx, lex)
        return
    if prog == "botsito":
        que = " ".join(["botsito", *(a.texto for a in args[:2])])
        exigir_ejecucion_verificable(ctx, lex, cmd, que)
        _analizar_cli(args, ctx, lex)
        return
    if prog in SHELLS:
        _analizar_shell(prog, args, cmd, ctx, lex)
        return
    if prog in {"pytest", "py.test"}:
        _analizar_pytest(args, cmd, ctx, lex)
        return
    if _es_interprete(prog):
        _analizar_interprete(prog, args, cmd, ctx, lex)
        return
    if prog in {"pwsh", "powershell"}:
        _analizar_pwsh(prog, args, cmd, ctx, lex)
        return
    if prog == "cmd":
        exigir_ejecucion_verificable(
            ctx, lex, cmd, "cmd", indecidible="`cmd /c` ejecuta un comando que no se puede analizar"
        )
    if _es_fichero_programa(argv[0].texto, ctx):  # `./x.py`, `uv run x.py`
        lenguaje = _lenguaje_del_fichero(_absoluta(argv[0].texto, ctx.cwd))
        _exigir_guion(argv[0], args, cmd, ctx, lex, lenguaje, argv[0].texto)
        return
    if prog in LECTOR_DE_METADATOS:
        return
    if prog == "wc":
        flags = [a.texto for a in args if a.texto.startswith("-")]
        if flags and all(re.fullmatch(r"-c|--bytes", f) for f in flags) and not cmd.tras_tuberia:
            return
    if prog == "certutil" and any(a.texto.lower() == "-hashfile" for a in args):
        return
    if prog in {"mv", "cp", "rsync", "scp"}:
        fuentes = [a for a in args if not a.texto.startswith("-")][:-1]
        recursivo = prog != "mv" and any(
            re.fullmatch(r"-[a-zA-Z]*[rRa][a-zA-Z]*|--recursive|--archive", a.texto) for a in args
        )
        for f in fuentes:
            _exigir_legible(f, ctx, lex, f"origen de `{prog}`", recursivo=recursivo)
        return
    if prog in SIN_LECTURA_DE_RUTAS:
        if prog == "curl":
            for a in args:
                if a.texto.startswith("@"):
                    _exigir_legible(
                        Palabra(a.texto[1:], a.glob), ctx, lex, "fichero que envia curl"
                    )
        return
    # Un programa que la guardia no conoce y que lanza otro (`winpty python x`, `sudo bash x`):
    # no sabe que ejecutara, asi que la ejecucion no es verificable.
    lanzada = next((a for a in args if _lanza_una_ejecucion(a.texto)), None)
    if lanzada is not None and prog not in LECTORES_CON_PATRON:
        exigir_ejecucion_verificable(
            ctx,
            lex,
            cmd,
            f"{prog} {lanzada.texto}",
            indecidible=f"`{prog}` lanza `{lanzada.texto}`, y la guardia no conoce `{prog}`: no "
            "sabe que ejecutara",
        )
    # Cualquier otro programa LEE el contenido de sus argumentos de ruta.
    textos = [a.texto for a in args]
    flag_r = any(
        re.fullmatch(r"-[a-zA-Z]*[rR][a-zA-Z]*|--(dereference-)?recursive", t) for t in textos
    )
    recursivo = (
        prog in RECURSIVOS_CON_IGNORE
        or prog in ARCHIVADORES
        or (prog in {"grep", "egrep", "fgrep"} and flag_r)
    )
    respeta = prog in RECURSIVOS_CON_IGNORE and not any(
        re.fullmatch(r"--no-ignore\S*|-[a-zA-Z]*u[a-zA-Z]*", t) for t in textos
    )
    con_rutas = _exigir_args_legibles(args, ctx, lex, recursivo=recursivo, respeta_ignore=respeta)
    if recursivo and not con_rutas and prog in {"grep", "egrep", "fgrep", "rg"}:
        motivo = ctx.politica.motivo_ruta(ctx.cwd, recursivo=True, respeta_ignore=respeta)
        if motivo:
            raise BloqueoError(
                f"`{prog}` recursivo sin ruta recorre {ctx.cwd}, que alcanza material protegido."
                f"\nRegla: {motivo}.\nComo reescribirlo: dale una ruta que no lo contenga "
                "(`src`, `docs`, `knowledge/spec`...) o usa la herramienta Grep."
            )


def _tras_opcion(args: list[Palabra], opciones: set[str]) -> str | None:
    """El valor de la primera de `opciones` (`--video v7` o `--video=v7`), o None."""
    for i, a in enumerate(args):
        clave, igual, valor = a.texto.partition("=")
        if clave.lower() in opciones:
            if igual:
                return valor
            if i + 1 < len(args):
                return args[i + 1].texto
    return None


def _exigir_args_legibles(
    args: list[Palabra], ctx: Contexto, lex: Lexico, recursivo: bool, respeta_ignore: bool = False
) -> bool:
    """Comprueba cada argumento como posible ruta. Devuelve si alguno era una ruta existente."""
    alguna = False
    for a in args:
        if a.texto.startswith("-") and "=" not in a.texto:
            continue
        valores = _valores(a, ctx, lex)
        if valores is None:
            texto_visible = re.sub(r"\x00[SV]([^\x00]*)\x00", r"$\1", a.texto)
            raise BloqueoError(
                f"el argumento `{texto_visible}` se construye al ejecutarse y este comando lee "
                f"contenido: no se puede decidir si llega a material protegido. {COMO_REESCRIBIR}"
            )
        for v in valores:
            for cand in candidatos_de_ruta(v):
                ruta = _absoluta(cand, ctx.cwd)
                if os.path.exists(ruta) or ctx.politica.motivo_fichero(ruta):
                    alguna = alguna or os.path.exists(ruta)
                    motivo = ctx.politica.motivo_ruta(ruta, recursivo, respeta_ignore)
                    if motivo:
                        raise BloqueoError(f"leer el contenido de {cand}.\nRegla: {motivo}.")
    return alguna


def _exigir_legible(
    p: Palabra, ctx: Contexto, lex: Lexico, que: str, recursivo: bool = False
) -> None:
    valores = _valores(p, ctx, lex)
    if valores is None:
        raise BloqueoError(f"el {que} se construye al ejecutarse. {COMO_REESCRIBIR}")
    for v in valores:
        ruta = _absoluta(v, ctx.cwd)
        motivo = ctx.politica.motivo_ruta(ruta, recursivo=recursivo)
        if motivo:
            raise BloqueoError(f"{que}: {v}.\nRegla: {motivo}.")


# ------------------------------------------------------------------------------- git, rm, make
GIT_CON_VALOR = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
GIT_QUE_MUESTRA = {
    "show",
    "diff",
    "log",
    "blame",
    "grep",
    "cat-file",
    "archive",
    "annotate",
    "whatchanged",
}


def _analizar_git(args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    i = 0
    base = ctx.cwd  # `git -C <dir>`: las rutas de los argumentos son relativas a <dir>
    while i < len(args) and args[i].texto.startswith("-"):
        opcion = args[i].texto
        valor = args[i + 1].texto if opcion in GIT_CON_VALOR and i + 1 < len(args) else ""
        if opcion.startswith("--config-env"):
            exigir_ejecucion_verificable(
                ctx,
                lex,
                cmd,
                f"git {opcion}",
                indecidible="`--config-env` toma el valor de una variable de entorno: puede ser un "
                "alias con `!` que la guardia no ve",
            )
        if opcion == "-c" and re.match(r"(?is)alias\.[^=]+=\s*!", valor):
            # El alias ejecuta un shell, lanzado por el propio `git`.
            cuerpo = valor.split("=", 1)[1].strip()[1:]
            _ejecucion_lanzada(cmd, [Palabra("sh"), Palabra("-c"), Palabra(cuerpo)], ctx, lex)
        if opcion == "-C" and valor:
            vals = _valores(args[i + 1], ctx, lex)
            if vals is None or len(vals) != 1:
                raise BloqueoError(f"`git -C` con una ruta dinamica. {COMO_REESCRIBIR}")
            base = _absoluta(vals[0], base)
        if opcion == "-c" and "core.hookspath" in valor.lower():
            raise BloqueoError(
                f"`git -c core.hooksPath=...` salta los hooks.\nRegla: {R_NO_VERIFY}."
            )
        i += 2 if opcion in GIT_CON_VALOR else 1
    if i >= len(args):
        return
    sub = args[i].texto
    resto = args[i + 1 :]
    textos = [a.texto for a in resto]
    if "--no-verify" in textos or (sub == "commit" and _flag_corta(textos, "n", "mFCct")):
        raise BloqueoError(f"`git {sub} --no-verify`.\nRegla: {R_NO_VERIFY}.")
    if sub == "config" and any("core.hookspath" in t.lower() for t in textos):
        valores = [t for t in textos if not t.startswith("-")]
        if len(valores) > 1 or any(t.startswith("--unset") or t == "--add" for t in textos):
            raise BloqueoError(
                f"`git config core.hooksPath` cambia donde git busca los hooks: es saltarlos."
                f"\nRegla: {R_NO_VERIFY}."
            )
    if sub in {"cherry-pick", "rebase"} and not {"--abort", "--quit"} & set(textos):
        raise BloqueoError(f"`git {sub}`.\nRegla: {R_CHERRY}.")
    if sub == "push":
        if any(
            t in {"--force", "--force-with-lease", "--force-if-includes", "--mirror"}
            or t.startswith("--force-with-lease=")
            or _flag_corta([t], "f", "")
            or (not t.startswith("-") and t.startswith("+"))
            for t in textos
        ):
            raise BloqueoError(f"`git push` forzado.\nRegla: {R_FORCE}.")
        decidir_borrado_remoto([_valor_unico(a, ctx, lex) for a in resto])
    if sub == "tag" and (
        {"-d", "--delete", "-f", "--force"} & set(textos) or _flag_corta(textos, "df", "mFu")
    ):
        raise BloqueoError(f"`git tag` que borra o mueve un tag.\nRegla: {R_TAG}.")
    if sub == "update-ref" and "-d" in textos:
        raise BloqueoError(f"`git update-ref -d`.\nRegla: {R_TAG}.")
    if sub == "branch" and (
        "-D" in textos or ({"-d", "--delete"} & set(textos) and {"-f", "--force"} & set(textos))
    ):
        raise BloqueoError(f"`git branch -D`.\nRegla: {R_BRANCH_D}.")
    if sub in {"checkout", "switch"}:
        destino = [t for t in textos if not t.startswith("-")]
        if destino and "--" not in textos and len(destino) == 1:
            ctx.rama, ctx.rama_leida = destino[0], True
        return
    if sub in {"add", "commit", "revert", "reset"} and ctx.rama_actual() == "main":
        if sub == "add" and ({"-A", "--all", ".", ":/", "-u", "--update"} & set(textos)):
            raise BloqueoError(f"`git add {' '.join(textos)}` en `main`.\nRegla: {R_ADD_A}.")
        if sub == "commit" and ("--all" in textos or _flag_corta(textos, "a", "mFCct")):
            raise BloqueoError(f"`git commit -a` en `main`.\nRegla: {R_ADD_A}.")
        if sub == "revert" or (sub == "reset" and "--hard" in textos):
            raise BloqueoError(f"`git {sub}` en `main`.\nRegla: {R_REVERT}.")
    if sub in GIT_QUE_MUESTRA:
        _analizar_git_que_muestra(sub, resto, ctx, lex, base)
    # `git push origin main` sin BOTSITO_ALLOW_MAIN NO se vigila: el ritual empuja `main` sin esa
    # variable (RITUAL.md, `git push --atomic origin main stable/<tag>` y el arreglo de una CI
    # roja), asi que la regla lo bloquearia (docs/validation/GUARDIAS-CLAUDE.md §1.4).


# El borrado remoto (encargo de `trabajo/dieta-y-skills`): RITUAL.md manda borrar la `fix/<rama>`
# que se empuja para la CI de Linux, asi que un `git push` puede borrar una rama de trabajo, y nada
# mas. Se NIEGA POR DEFECTO: lo que no casa con RAMA_BORRABLE -`main`, un tag, `refs/tags/`, un
# comodin, una referencia construida al ejecutarse- se bloquea, y un borrado de varias referencias
# se bloquea entero si una sola no casa.
_TRAMO_DE_RAMA = r"[A-Za-z0-9_-][A-Za-z0-9._-]*"
RAMA_BORRABLE = re.compile(
    rf"(?:refs/heads/)?(?:trabajo|feature|fix)/{_TRAMO_DE_RAMA}(?:/{_TRAMO_DE_RAMA})*"
)
PUSH_CON_VALOR = {"-o", "--push-option", "--receive-pack", "--exec", "--repo"}


def _valor_unico(p: Palabra, ctx: Contexto, lex: Lexico) -> str | None:
    """El valor de una palabra si se sabe ANTES de ejecutar y es uno solo; si no, None."""
    valores = _valores(p, ctx, lex)
    return valores[0] if valores is not None and len(valores) == 1 else None


def decidir_borrado_remoto(argumentos: list[str | None]) -> None:
    """Los argumentos de `git push` (None = se construye al ejecutarse): bloquea si borra algo que
    no sea una rama `trabajo/`, `feature/` o `fix/`, o si no se puede saber que borra."""
    flags = [a for a in argumentos if a is not None and a.startswith("-")]
    for flag in ("--prune", "--mirror"):
        if flag in flags:
            raise BloqueoError(
                f"`git push {flag}` borra ramas remotas sin nombrarlas.\nRegla: {R_BORRAR_REMOTO}."
            )
    borra = "--delete" in flags or _flag_corta(flags, "d", "")
    posicionales: list[str | None] = []
    saltar = False
    for a in argumentos:
        if saltar:
            saltar = False
        elif a is not None and a in PUSH_CON_VALOR:
            saltar = True
        elif a is None or not a.startswith("-"):
            # `+:main` borra igual que `:main` (el `+` solo fuerza): se mira sin el `+`, aunque
            # el push forzado ya lo bloquee antes (revisor de `trabajo/dieta-y-skills`, B1).
            posicionales.append(a if a is None else a.removeprefix("+"))
    if borra:
        borradas = posicionales[1:]
        if not borradas:
            raise BloqueoError(
                f"`git push --delete` sin una rama que se pueda nombrar.\nRegla: {R_BORRAR_REMOTO}."
            )
    else:
        # Sin `--delete`, borra cada refspec `:<ref>`; uno construido al ejecutarse podria serlo.
        borradas = [p if p is None else p[1:] for p in posicionales if p is None or p[:1] == ":"]
    for ref in borradas:
        if ref is None:
            raise BloqueoError(
                f"`git push` con una referencia que se construye al ejecutarse: no se sabe si "
                f"borra. {COMO_REESCRIBIR}"
            )
        if RAMA_BORRABLE.fullmatch(ref) and ".." not in ref and not ref.endswith(".lock"):
            continue
        regla = R_TAG if ref.startswith(("refs/tags/", "stable/")) else R_BORRAR_REMOTO
        raise BloqueoError(f"`git push` que borra la referencia remota `{ref}`.\nRegla: {regla}.")


def _flag_corta(textos: Iterable[str], letras: str, con_valor: str) -> bool:
    """Si alguna agrupacion de flags cortas (`-an`) lleva una de `letras` antes de una flag que
    toma valor (lo que sigue a `-m` es el mensaje, no flags)."""
    for t in textos:
        if re.fullmatch(r"-[a-zA-Z]+", t):
            for c in t[1:]:
                if c in letras:
                    return True
                if c in con_valor:
                    break
    return False


def _analizar_git_que_muestra(
    sub: str, resto: list[Palabra], ctx: Contexto, lex: Lexico, base: str
) -> None:
    """`rev:ruta` es relativa a la raiz del repo, salvo `rev:./ruta`, que lo es al directorio de
    git (`-C`); una ruta suelta, siempre al directorio de git."""
    rutas = False
    for a in resto:
        valores = _valores(a, ctx, lex)
        if valores is None:
            raise BloqueoError(
                f"`git {sub}` con un argumento que se construye al ejecutarse. {COMO_REESCRIBIR}"
            )
        for v in valores:
            if v.startswith("-"):
                continue
            m = re.match(r"^[^:]*:(.+)$", v) if not re.match(r"^[a-zA-Z]:[\\/]", v) else None
            candidata = m.group(1) if m else v
            relativa_al_repo = m is not None and not candidata.startswith(("./", "../"))
            ruta = _absoluta(candidata, str(ctx.politica.raiz) if relativa_al_repo else base)
            if ctx.politica.relativa(ruta) is not None and (os.path.exists(ruta) or m):
                rutas = True
                motivo = ctx.politica.motivo_ruta(ruta, recursivo=True, respeta_ignore=True)
                if motivo:
                    raise BloqueoError(f"`git {sub}` sobre {candidata}.\nRegla: {motivo}.")
    if not rutas and sub in {"diff", "log", "show", "grep", "whatchanged"}:
        motivo = ctx.politica.motivo_ruta(
            str(ctx.politica.raiz), recursivo=True, respeta_ignore=True
        )
        if motivo:
            raise BloqueoError(
                f"`git {sub}` sin rutas puede mostrar ficheros seguidos protegidos."
                f"\nRegla: {motivo}."
                "\nComo reescribirlo: nombra las rutas, o excluyelas con "
                "`-- . ':!knowledge/cases/holdout' ':!knowledge/feedback'`."
            )


RAICES_INTOCABLES = ("data", "corpus", "knowledge")


def _analizar_rm(args: list[Palabra], ctx: Contexto, lex: Lexico) -> None:
    textos = [a.texto for a in args]
    recursivo = any(re.fullmatch(r"-[a-zA-Z]*[rR][a-zA-Z]*|--recursive", t) for t in textos)
    forzado = any(re.fullmatch(r"-[a-zA-Z]*f[a-zA-Z]*|--force", t) for t in textos)
    if not (recursivo and forzado):
        return
    for a in args:
        if a.texto.startswith("-"):
            continue
        valores = _valores(a, ctx, lex)
        if valores is None:
            raise BloqueoError(
                f"`rm -rf` con una ruta que se construye al ejecutarse. {COMO_REESCRIBIR}"
            )
        for v in valores:
            rel = ctx.politica.relativa(_absoluta(v, ctx.cwd))
            if rel is None:
                continue
            if rel == "" or rel.split("/")[0] in RAICES_INTOCABLES:
                raise BloqueoError(f"`rm -rf {v}`.\nRegla: {R_RM}.")


def _analizar_make(args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    objetivos = {a.texto for a in args}
    if objetivos & {"check", "regress"}:
        ficheros = [d for op, d in cmd.salidas if op in {">", ">>", "&>", ">|"}]
        nulos = [d for d in ficheros if d.texto.lower() in {"/dev/null", "nul", "nul:"}]
        if nulos or not ficheros:
            raise BloqueoError(f"`make check` sin la salida a un fichero.\nRegla: {R_DEVNULL}.")
    que = " ".join(["make", *(a.texto for a in args)])
    rara = next((a.texto for a in args if a.texto.startswith("-") or "=" in a.texto), None)
    # El `Makefile` es el guion de `make`: el que GNU make elige, con su grafia real.
    try:
        presentes = set(os.listdir(ctx.cwd))
    except OSError:
        presentes = set()
    candidatos = ("GNUmakefile", "makefile", "Makefile")
    nombre = next((n for n in candidatos if n in presentes), "Makefile")
    exigir_ejecucion_verificable(
        ctx,
        lex,
        cmd,
        que,
        guiones=[(Palabra(os.path.join(ctx.cwd, nombre)), "make")],
        indecidible=f"`make {rara}`: solo se admiten objetivos; una opcion o una variable cambia "
        "que recetas corren"
        if rara
        else None,
    )


def _analizar_xargs(args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    i = 0
    while i < len(args) and args[i].texto.startswith("-"):
        i += 2 if args[i].texto in {"-I", "-n", "-L", "-P", "-d", "-E", "-s"} else 1
    if i >= len(args):
        return
    prog = os.path.basename(args[i].texto).lower()
    if prog in LECTOR_DE_METADATOS or prog in {"sha256sum", "stat"}:
        return
    exigir_ejecucion_verificable(
        ctx,
        lex,
        cmd,
        f"xargs {prog}",
        indecidible=f"`xargs {prog}` lee o ejecuta ficheros cuyos nombres se saben al ejecutar",
    )


def _analizar_find(args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    raices: list[Palabra] = []
    i = 0
    while i < len(args) and not args[i].texto.startswith(("-", "(", "!")):
        raices.append(args[i])
        i += 1
    textos = [a.texto for a in args[i:]]
    for accion in ("-exec", "-execdir", "-ok", "-okdir"):
        if accion in textos:
            j = textos.index(accion) + 1
            prog = os.path.basename(textos[j]).lower() if j < len(textos) else ""
            if (
                prog in LECTOR_DE_METADATOS
                or prog in {"sha256sum", "stat"}
                or (prog == "wc" and "-c" in textos)
            ):
                continue
            # Lo que lanza `-exec`, con el propio `find` corriendo a la vez.
            k = next((m for m in range(j, len(textos)) if textos[m] in {";", "+"}), len(textos))
            _ejecucion_lanzada(cmd, args[i + j : i + k], ctx, lex)
            for r in raices or [Palabra(".")]:
                valores = _valores(r, ctx, lex)
                if valores is None:
                    raise BloqueoError(
                        f"`find ... {accion}` sobre una ruta dinamica. {COMO_REESCRIBIR}"
                    )
                for v in valores:
                    motivo = ctx.politica.motivo_ruta(_absoluta(v, ctx.cwd), recursivo=True)
                    if motivo:
                        raise BloqueoError(
                            f"`find {v} {accion} {prog}` lee el contenido de lo que encuentra."
                            f"\nRegla: {motivo}."
                        )


def _analizar_cli(args: list[Palabra], ctx: Contexto, lex: Lexico) -> None:
    """La CLI es la puerta del proyecto y se deja pasar, salvo lo que IMPRIME una cruda."""
    textos = [a.texto for a in args]
    sin_opciones = tuple(t for t in textos if not t.startswith("-"))
    video = _tras_opcion(args, {"--video"})
    cuarentena = ctx.politica.sesiones_en_cuarentena
    for clave in CLI_QUE_IMPRIME_CRUDA:
        if sin_opciones[: len(clave)] == clave and (video is None or video.lower() in cuarentena):
            raise BloqueoError(
                f"`botsito {' '.join(clave)} --video {video}` imprime la transcripcion cruda."
                f"\nRegla: {R_CUARENTENA}.\nComo reescribirlo: localiza el instante en la version"
                " filtrada y abre el PNG por su ruta (`data/fotogramas/<v>/png-1fps/<ms>.png`)."
            )
    _tramos_en_la_cli(sin_opciones, args, video, ctx)
    # `kb find` SIN `--video` pasa desde `trabajo/cuarentena-por-defecto`: el indice que consulta
    # se construye filtrado (`botsito.corpus.cuarentena`). Con `--video` de una sesion en
    # cuarentena sigue bloqueado: segunda capa, por decision del consultor del 2026-10-01.
    if sin_opciones[:2] == ("kb", "find") and video is not None and video.lower() in cuarentena:
        raise BloqueoError(
            f"`botsito kb find --video {video}` busca en una sesion en cuarentena."
            f"\nRegla: {R_CUARENTENA}.\nComo reescribirlo: `--video <v>` con un video que no sea "
            "una sesion en cuarentena, o sin `--video` (la busqueda sale filtrada)."
        )


PYTEST_CON_VALOR = frozenset({
    "-k", "-m", "-p", "-c", "-o", "-W", "-r", "-n", "--deselect", "--rootdir", "--basetemp",
    "--tb", "--maxfail", "--durations", "--ignore", "--ignore-glob", "--confcutdir",
    "--junitxml", "--junit-xml", "--cov", "--cov-report", "--import-mode", "--log-level",
    "--log-cli-level", "--color", "--capture", "--override-ini",
})  # fmt: skip


def _analizar_pytest(args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico) -> None:
    """La suite de `tests/` es codigo revisado y corre con la guarda del holdout
    (`tests/guarda_holdout.py`): no se lee. Un fichero de pruebas FUERA de `tests/` es codigo
    suelto: es un guion de la ejecucion, y pasa por `exigir_ejecucion_verificable`."""
    guiones: list[tuple[Palabra, str]] = []
    indecidible: str | None = None
    posicionales = 0
    i = 0
    while i < len(args):
        t = args[i].texto
        if t.startswith("-"):
            clave, igual, valor = t.partition("=")
            if clave == "--pyargs":
                indecidible = "`--pyargs`: las rutas son paquetes que la guardia no resuelve"
            if clave in {"-c", "-o", "--override-ini", "--config-file"} or (
                clave.startswith("-o") and not clave.startswith("--")
            ):
                indecidible = (
                    f"`pytest {clave}` cambia su configuracion, que puede cargar plugins o "
                    "ficheros que la guardia no lee (revisor, B3)"
                )
            valor_dinamico = i + 1 < len(args) and "\x00" in args[i + 1].texto
            if "\x00" in t or (clave in PYTEST_CON_VALOR and not igual and valor_dinamico):
                indecidible = f"`pytest {clave}` con un valor que se construye al ejecutarse"
            if clave == "-p" or (clave.startswith("-p") and not clave.startswith("--")):
                siguiente = args[i + 1].texto if i + 1 < len(args) else ""
                plugin = valor if igual else (t[2:] or siguiente)
                if not plugin.startswith("no:"):
                    indecidible = f"`-p {plugin}` carga un plugin que la guardia no lee"
            i += 2 if clave in PYTEST_CON_VALOR and not igual and len(clave) == len(t) else 1
            continue
        posicionales += 1
        valores = _valores(args[i], ctx, lex)
        if valores is None:
            indecidible = "`pytest` sobre una ruta que se construye al ejecutarse"
            valores = []
        for v in valores:
            fichero = v.split("::", 1)[0]
            rel = ctx.politica.relativa(_absoluta(fichero, ctx.cwd))
            if rel is not None and (rel == "tests" or rel.startswith("tests/")):
                continue
            guiones.append((Palabra(fichero), "python"))
        i += 1
    if not posicionales and _normcase(ctx.cwd) != ctx.politica.raiz_norm:
        indecidible = indecidible or (
            "`pytest` sin rutas fuera de la raiz del repositorio recoge ficheros que la guardia "
            "no lee"
        )
    exigir_ejecucion_verificable(ctx, lex, cmd, "pytest", guiones=guiones, indecidible=indecidible)


def _tramos_en_la_cli(
    sin_opciones: tuple[str, ...], args: list[Palabra], video: str | None, ctx: Contexto
) -> None:
    """Un video con tramos vigilados: lo que la CLI imprimiria de dentro de un tramo, no."""
    if video is None or video.lower() not in ctx.politica.tramos_vigilados:
        return
    if sin_opciones[:3] in {("corpus", "frames", "show")} or sin_opciones[:2] == ("kb", "at"):
        desde = hasta = _tras_opcion(args, {"--t"})
    elif sin_opciones[:3] == ("corpus", "transcript", "show"):
        desde, hasta = _tras_opcion(args, {"--t0"}), _tras_opcion(args, {"--t1"})
    elif sin_opciones[:2] == ("kb", "find"):
        desde, hasta = _tras_opcion(args, {"--desde"}), _tras_opcion(args, {"--hasta"})
    else:
        return
    a = a_ms(desde) if desde else None
    b = a_ms(hasta) if hasta else None
    tramo = ctx.politica.tramo_que_solapa(video, a, b) if a is not None and b is not None else None
    if a is None or b is None or tramo:
        donde = f"{desde}-{hasta}" if desde and hasta else "un intervalo sin acotar"
        raise BloqueoError(
            f"`botsito {' '.join(sin_opciones[:3])} --video {video}` en {donde} puede imprimir un "
            f"tramo no citable de {video}.\nRegla: {R_TRAMO}.\nComo reescribirlo: un instante o un "
            "intervalo (`--desde`/`--hasta` en `kb find`) fuera de los tramos de "
            "`knowledge/corpus/tramos_no_citables.yaml`."
        )


SHELL_CON_VALOR = {"-o", "+o", "-O", "+O", "--rcfile", "--init-file"}
INTERPRETE_CON_VALOR = {"-X", "-W", "-r", "--require", "--import", "--loader"}
# Lo unico que se admite a un interprete o un shell sin guion ni codigo: no ejecuta nada.
SOLO_VERSION = frozenset({"--version", "-V", "-VV", "--help", "-h"})


def _analizar_shell(
    prog: str, args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico
) -> None:
    codigo = _tras_opcion(args, {"-c", "-lc", "-ic"})
    if codigo is not None:
        exigir_ejecucion_verificable(ctx, lex, cmd, f"{prog} -c", codigo=(codigo, "shell"))
        return
    resto = _saltar_opciones(args, SHELL_CON_VALOR)
    lee_stdin = any(a.texto == "-s" for a in args[: len(args) - len(resto)])
    if resto and resto[0].texto != "-" and not lee_stdin:
        _exigir_guion(resto[0], resto[1:], cmd, ctx, lex, "shell", f"{prog} {resto[0].texto}")
        return
    _sin_guion(prog, args, cmd, ctx, lex, "shell")


def _analizar_interprete(
    prog: str, args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico
) -> None:
    lenguaje = "python" if prog.startswith("py") else "otro"
    i = 0
    while i < len(args) and args[i].texto.startswith("-") and args[i].texto != "-":
        t = args[i].texto
        if t in {"-c", "-e", "--eval"}:
            codigo = args[i + 1].texto if i + 1 < len(args) else ""
            exigir_ejecucion_verificable(ctx, lex, cmd, f"{prog} {t}", codigo=(codigo, lenguaje))
            _exigir_args_legibles(args[i + 2 :], ctx, lex, recursivo=False)
            return
        if t == "-m" or (lenguaje == "python" and t.startswith("-m")):
            modulo = t[2:] or (args[i + 1].texto if i + 1 < len(args) else "")
            resto = args[i + 1 :] if t[2:] else args[i + 2 :]
            if modulo == "pytest":
                _analizar_pytest(resto, cmd, ctx, lex)
                return
            exigir_ejecucion_verificable(
                ctx,
                lex,
                cmd,
                f"{prog} -m {modulo}",
                indecidible=f"`-m {modulo}`: la guardia no resuelve que fichero ejecuta un modulo "
                "(solo admite `-m pytest`); ejecuta el guion por su ruta",
            )
        i += 2 if t in INTERPRETE_CON_VALOR else 1
    resto = args[i:]
    if resto and resto[0].texto != "-":
        _exigir_guion(resto[0], resto[1:], cmd, ctx, lex, lenguaje, f"{prog} {resto[0].texto}")
        return
    _sin_guion(prog, args, cmd, ctx, lex, lenguaje)


def _sin_guion(
    prog: str, args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico, lenguaje: str
) -> None:
    """Un interprete o un shell sin guion: ejecuta su heredoc, lo que le llega por `<`, o lo que
    le llega por la entrada estandar."""
    if cmd.heredocs:
        h = cmd.heredocs[-1]
        expande = not h.con_comillas and re.search(r"[$`]", h.cuerpo)
        exigir_ejecucion_verificable(
            ctx,
            lex,
            cmd,
            f"{prog} <<{h.delimitador}",
            codigo=(h.cuerpo, lenguaje),
            indecidible="un heredoc sin comillas: el shell expande `$` y los acentos graves "
            "antes de ejecutar"
            if expande
            else None,
        )
        return
    if cmd.entradas:
        entrada = cmd.entradas[-1]
        que = f"{prog} < {entrada.texto}"
        exigir_ejecucion_verificable(ctx, lex, cmd, que, guiones=[(entrada, lenguaje)])
        return
    if args and not cmd.tras_tuberia and {a.texto for a in args} <= SOLO_VERSION:
        return
    exigir_ejecucion_verificable(
        ctx,
        lex,
        cmd,
        prog,
        indecidible="no tiene guion ni codigo: ejecuta lo que le llegue por la entrada estandar, "
        "que la guardia no ve",
    )


def _exigir_guion(
    guion: Palabra,
    resto: list[Palabra],
    cmd: Comando,
    ctx: Contexto,
    lex: Lexico,
    lenguaje: str,
    que: str,
) -> None:
    """El guion pasa por la condicion; despues se miran sus argumentos, salvo los de un guion de
    `main` con su propia puerta (`SCRIPTS_CON_PUERTA`)."""
    revisado = exigir_ejecucion_verificable(ctx, lex, cmd, que, guiones=[(guion, lenguaje)])
    valores = _valores(guion, ctx, lex) or [guion.texto]
    rel = ctx.politica.relativa(_absoluta(valores[0], ctx.cwd))
    if revisado and rel in SCRIPTS_CON_PUERTA:
        return
    _exigir_args_legibles(resto, ctx, lex, recursivo=False)


def _analizar_pwsh(
    prog: str, args: list[Palabra], cmd: Comando, ctx: Contexto, lex: Lexico
) -> None:
    """`pwsh -c` desde Bash: su codigo se analiza como PowerShell, donde no se admite ninguna
    ejecucion; `pwsh x.ps1` es un guion de PowerShell, que la guardia no analiza."""
    codigo = _tras_opcion(args, {"-c", "-command", "-commandwithargs"})
    if codigo is not None:
        exigir_ejecucion_verificable(ctx, lex, cmd, f"{prog} -c", codigo=(codigo, "powershell"))
        return
    fichero = _tras_opcion(args, {"-file", "-f"})
    guion = (
        Palabra(fichero)
        if fichero is not None
        else next((a for a in args if not a.texto.startswith("-")), None)
    )
    if guion is not None:
        exigir_ejecucion_verificable(
            ctx, lex, cmd, f"{prog} {guion.texto}", guiones=[(guion, "powershell")]
        )
        return
    _sin_guion(prog, args, cmd, ctx, lex, "powershell")


# ------------------------------------------------------------- la ejecucion verificable
# Encargo de `trabajo/guion-mismo-comando` y respuesta del consultor a su fase 0 (2026-10-07). UNA
# condicion, con nombre propio, que todas las vias de ejecucion llaman y ninguna decide por su
# cuenta. Niega por defecto: lo que puede ir antes de una ejecucion, o a la vez, es una LISTA
# CERRADA (`_es_preparacion`, `_es_filtro`); todo lo demas se niega.
R_EJECUCION = (
    "encargo de `trabajo/guion-mismo-comando` (respuesta del consultor del 2026-10-07): la guardia "
    "solo deja ejecutar codigo si es SEGURO que lo que se ejecuta es lo que ella leyo al "
    "inspeccionar el comando; si no lo puede garantizar, NIEGA (RELOJ-INVIERNO.md §4.5)"
)
COMO_EJECUTAR = (
    "Como reescribirlo: el guion, con la herramienta Write, y su ejecucion en OTRA llamada; "
    "delante, solo `cd`, asignaciones con valor literal, `export X=valor` o `set -e`/`-u`/"
    "`-o pipefail`; detras, en la misma tuberia, solo `head`, `tail`, `grep`, `wc`, `sort`, "
    "`uniq` o `cut` sin redirigir su salida; y ningun `$(...)` ni acento grave en el comando."
)
FILTROS_TRAS_LA_EJECUCION = frozenset({"head", "tail", "grep", "wc", "sort", "uniq", "cut"})
EXT_GUION = (
    ".py", ".pyw", ".sh", ".bash", ".zsh", ".pl", ".rb", ".js", ".mjs", ".cjs", ".ts", ".r",
    ".ps1", ".psm1", ".bat", ".cmd",
)  # fmt: skip
EJECUTORES = frozenset({"pytest", "py.test", "make", "botsito", "pwsh", "powershell", "uv", "uvx"})
# Programas que se sabe que LEEN y no ejecutan, aunque un argumento suyo se llame `python` (un
# patron de busqueda). Cualquier otro programa que reciba un interprete se toma por un lanzador.
LECTORES_CON_PATRON = frozenset({
    "grep", "egrep", "fgrep", "rg", "ag", "ack", "man", "info", "apropos", "whatis", "less",
    "more", "cat", "head", "tail", "wc", "file", "diff", "sed", "awk", "gawk", "sort", "uniq",
    "cut", "tr",
})  # fmt: skip
PS_LANZADORES = frozenset({
    "start-process", "saps", "start", "invoke-item", "ii", "invoke-command", "icm", "cmd",
})  # fmt: skip


def _es_interprete(prog: str) -> bool:
    """Un interprete, tambien con version (`python3.12`, `pythonw`)."""
    return (
        prog in {p.lower() for p in INTERPRETES}
        or re.fullmatch(r"pythonw?(\d+(\.\d+)*)?", prog) is not None
    )


def _nombre_de_programa(texto: str) -> str:
    nombre = os.path.basename(texto).lower()
    for ext in (".exe", ".cmd", ".bat"):
        nombre = nombre.removesuffix(ext)
    return nombre


def _lanza_una_ejecucion(texto: str) -> bool:
    nombre = _nombre_de_programa(texto)
    return _es_interprete(nombre) or nombre in SHELLS or nombre in EJECUTORES


def _es_fichero_programa(texto: str, ctx: Contexto) -> bool:
    """El programa es un FICHERO (`./x`, `x.py`, una ruta del repositorio), no un programa del
    entorno: es codigo, y lo que se ejecuta es su contenido."""
    if texto.lower().endswith(EXT_GUION) or texto.startswith(("./", "../", ".\\", "..\\")):
        return True
    if "/" in texto or "\\" in texto:
        return ctx.politica.relativa(_absoluta(texto, ctx.cwd)) is not None
    return False


def _lenguaje_del_fichero(ruta: str) -> str:
    """Con que se lee un fichero que se ejecuta: por su extension o por su `#!`."""
    bajo = ruta.lower()
    if bajo.endswith((".py", ".pyw")):
        return "python"
    if bajo.endswith((".sh", ".bash", ".zsh")):
        return "shell"
    if bajo.endswith((".ps1", ".psm1")):
        return "powershell"
    try:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            primera = f.readline()
    except OSError:
        return "desconocido"
    if primera.startswith("#!") and "python" in primera:
        return "python"
    if primera.startswith("#!") and re.search(r"\b(ba|z|da)?sh\b", primera):
        return "shell"
    return "desconocido"


def _ejecucion_lanzada(lanzador: Comando, argv: list[Palabra], ctx: Contexto, lex: Lexico) -> None:
    """Lo que ejecuta otro programa (`find -exec`, un alias de git con `!`): se analiza como un
    comando que corre A LA VEZ que su lanzador, que va delante en la secuencia."""
    if not argv:
        return
    lanzado = Comando(list(argv), [], [], {}, [])
    sub = _sub(ctx)
    sub.secuencia, sub.posicion, sub.nivel = [lanzador, lanzado], 1, ctx.nivel
    analizar_comando(lanzado, sub, lex)


def _literal(p: Palabra) -> bool:
    return "\x00" not in p.texto and not p.glob


def _set_admitido(opciones: list[str]) -> bool:
    """`set -e`, `set -u`, `set -o pipefail` y sus combinaciones (`set -euo pipefail`)."""
    if not opciones:
        return False
    i = 0
    while i < len(opciones):
        m = re.fullmatch(r"-([eu]*)(o?)", opciones[i])
        if not m or not (m.group(1) or m.group(2)):
            return False
        i += 1
        if m.group(2):
            if i >= len(opciones) or opciones[i] != "pipefail":
                return False
            i += 1
    return True


def _es_preparacion(cmd: Comando) -> bool:
    """Lo UNICO que puede ir antes de una ejecucion, o a la vez, en el mismo comando (lista cerrada
    aceptada por el consultor el 2026-10-07): `cd`, asignaciones con valor literal, `export X=valor`
    literal y `set -e`/`-u`/`-o pipefail`. Sin ninguna redireccion."""
    if cmd.salidas or cmd.entradas or cmd.heredocs:
        return False
    if not all(_literal(p) for p in [*cmd.asignaciones.values(), *cmd.argv]):
        return False
    if not cmd.argv:
        return bool(cmd.asignaciones)
    textos = [p.texto for p in cmd.argv]
    if textos[0] == "cd":
        return len(textos) == 2 and textos[1] != "-"  # `cd` a secas va a HOME; `cd -`, ?
    if textos[0] == "export":
        return len(textos) > 1 and all(
            re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", t, re.S) for t in textos[1:]
        )
    if textos[0] == "set":
        return _set_admitido(textos[1:])
    return False


def _es_filtro(cmd: Comando) -> bool:
    """Lo UNICO que puede ir detras de una ejecucion en su tuberia: un filtro que lee de la
    entrada estandar y no escribe ningun fichero."""
    if cmd.salidas or cmd.entradas or cmd.heredocs or cmd.asignaciones or not cmd.argv:
        return False
    if not all(_literal(p) for p in cmd.argv):
        return False
    textos = [p.texto for p in cmd.argv]
    if textos[0] not in FILTROS_TRAS_LA_EJECUCION:
        return False
    if textos[0] == "sort" and any(
        t.startswith("--output") or re.fullmatch(r"-[a-zA-Z]*o.*", t) for t in textos[1:]
    ):
        return False  # `sort -o f` escribe
    return not (textos[0] == "uniq" and any(not t.startswith("-") for t in textos[1:]))


def _visible(cmd: Comando) -> str:
    partes = [f"{k}=..." for k in cmd.asignaciones]
    partes += [re.sub(r"\x00[SV]([^\x00]*)\x00", r"$\1", p.texto) for p in cmd.argv]
    texto = " ".join(partes) or "una redireccion"
    return texto if len(texto) <= 80 else texto[:77] + "..."


def _hay_sustitucion_de_proceso(lex: Lexico) -> bool:
    """`<(...)` o `>(...)`: el tokenizador los ve como `<` o `>` seguidos de `(`."""
    p = lex.palabras
    return any(
        a.op and a.texto in {"<", ">"} and b.op and b.texto == "("
        for a, b in zip(p, p[1:], strict=False)
    )


def _niega(que: str, por: str, como: str = COMO_EJECUTAR) -> NoReturn:
    que = re.sub(r"\x00[SV]([^\x00]*)\x00", r"$\1", que)  # las marcas, como se escribieron
    raise BloqueoError(f"ejecutar `{que}`: {por}.\nRegla: {R_EJECUCION}.\n{como}")


def _exigir_sin_expansiones(ctx: Contexto, lex: Lexico, cmd: Comando, que: str) -> None:
    """Nada que el shell expanda ANTES de ejecutar: sustituciones y asignaciones no literales."""
    if ctx.en_sustitucion:
        _niega(que, "va dentro de una sustitucion `$(...)`, que corre antes que el resto")
    nivel = ctx.nivel if ctx.nivel is not None else lex
    if nivel.sustituciones or _hay_sustitucion_de_proceso(nivel):
        _niega(
            que,
            "el comando lleva una sustitucion (`$(...)`, acentos graves o `<(...)`), que corre "
            "antes que la ejecucion o a la vez",
        )
    for nombre, valor in cmd.asignaciones.items():
        if not _literal(valor):
            _niega(que, f"la asignacion `{nombre}=...` delante de la ejecucion no es literal")


def _exigir_lo_de_antes(ctx: Contexto, cmd: Comando, que: str) -> None:
    """Todo lo que va antes en el mismo comando, de la lista cerrada (`_es_preparacion`)."""
    secuencia = ctx.secuencia if ctx.secuencia else [cmd]
    i = ctx.posicion if ctx.secuencia else 0
    for otro in secuencia[:i]:
        if not _es_preparacion(otro):
            _niega(que, f"antes, en el mismo comando, va `{_visible(otro)}`")


def _exigir_lo_de_a_la_vez(ctx: Contexto, cmd: Comando, que: str) -> None:
    """Lo que corre a la vez: detras en su tuberia, solo filtros; con un `&`, todo lo demas de la
    lista cerrada."""
    secuencia = ctx.secuencia if ctx.secuencia else [cmd]
    i = ctx.posicion if ctx.secuencia else 0
    fin = i
    while fin + 1 < len(secuencia) and secuencia[fin + 1].tras_tuberia:
        fin += 1
        if not _es_filtro(secuencia[fin]):
            _niega(
                que,
                f"detras, en la misma tuberia, va `{_visible(secuencia[fin])}`: solo filtros que "
                "leen de la entrada estandar y no escriben ningun fichero",
            )
    if any(c.separador == "&" for c in secuencia):
        for otro in secuencia[fin + 1 :]:
            if not _es_preparacion(otro):
                _niega(
                    que,
                    f"el comando lanza algo en segundo plano (`&`), y `{_visible(otro)}` puede "
                    "correr a la vez",
                )


def _exigir_salida_ajena(
    ctx: Contexto, lex: Lexico, cmd: Comando, que: str, guiones: list[Palabra]
) -> None:
    """La ejecucion no redirige su salida a su propio guion (el shell lo vaciaria antes)."""
    rutas: set[str] = set()
    for palabra in guiones:
        rutas.update(_normcase(_absoluta(v, ctx.cwd)) for v in _valores(palabra, ctx, lex) or [])
    for _op, destino in cmd.salidas:
        valores = _valores(destino, ctx, lex)
        if valores is None:
            _niega(que, "redirige su salida a un fichero que se construye al ejecutarse")
        if any(_normcase(_absoluta(v, ctx.cwd)) in rutas for v in valores):
            _niega(que, "redirige su salida a su propio guion, que el shell vacia antes")


def _exigir_comando_verificable(
    ctx: Contexto, lex: Lexico, cmd: Comando, que: str, guiones: list[Palabra]
) -> None:
    """Que nada del mismo comando pueda cambiar lo que se ejecuta entre la inspeccion y la
    ejecucion: cuatro piezas, cada una con su nombre (y su mutacion en el anexo)."""
    _exigir_sin_expansiones(ctx, lex, cmd, que)
    _exigir_lo_de_antes(ctx, cmd, que)
    _exigir_lo_de_a_la_vez(ctx, cmd, que)
    _exigir_salida_ajena(ctx, lex, cmd, que, guiones)


def _exigir_guion_legible(
    ctx: Contexto, lex: Lexico, que: str, palabra: Palabra, lenguaje: str
) -> bool:
    """El guion existe, se lee y se analiza; o es el de `main` (codigo revisado: devuelve True)."""
    valores = _valores(palabra, ctx, lex)
    if valores is None or len(valores) != 1:
        _niega(que, "el guion se construye al ejecutarse", COMO_REESCRIBIR)
    nombre = valores[0]
    ruta = _absoluta(nombre, ctx.cwd)
    motivo = ctx.politica.motivo_fichero(ruta)
    if motivo:
        raise BloqueoError(f"ejecutar {nombre}.\nRegla: {motivo}.")
    if os.path.isdir(ruta):
        _niega(que, f"{nombre} es un directorio: la guardia no sabe que ficheros ejecutara")
    if not os.path.isfile(ruta):
        _niega(que, f"{nombre} no existe al inspeccionar el comando: no se puede leer")
    rel = ctx.politica.relativa(ruta)
    if rel is not None and _igual_que_en_main(ctx.politica.raiz, ruta, rel):
        return True
    if lenguaje == "make":
        _niega(
            que,
            f"{nombre} no es el de `main`: sus recetas son codigo de la rama sin revisar",
            "Como reescribirlo: no se reescribe; lo lanza Aleks en su terminal con «!».",
        )
    if lenguaje == "powershell":
        _niega(que, f"{nombre} es un guion de PowerShell, que la guardia no analiza")
    if lenguaje == "desconocido":
        _niega(que, f"la guardia no sabe con que se ejecuta {nombre} (ni extension ni `#!`)")
    try:
        texto = Path(ruta).read_text(encoding="utf-8", errors="replace")
    except OSError:
        _niega(que, f"{nombre} no se puede leer")
    _analizar_codigo_de(texto, lenguaje, ctx)
    return False


def _analizar_codigo_de(texto: str, lenguaje: str, ctx: Contexto) -> None:
    if lenguaje == "shell":
        analizar_bash(texto, _sub(ctx))
    elif lenguaje == "powershell":
        analizar_powershell(texto, _sub(ctx, powershell=True))
    else:
        analizar_codigo(texto, ctx, lenguaje == "python")


def exigir_ejecucion_verificable(
    ctx: Contexto,
    lex: Lexico,
    cmd: Comando,
    que: str,
    *,
    guiones: Sequence[tuple[Palabra, str]] = (),
    codigo: tuple[str, str] | None = None,
    indecidible: str | None = None,
) -> bool:
    """LA condicion de toda ejecucion -un guion, codigo en linea, un heredoc, `make`, `pytest`,
    `botsito`, lo que lanza `find -exec` o un alias de git-: pasa solo si es SEGURO que lo que se
    ejecuta es lo que la guardia lee ahora. Niega por defecto, en este orden: en PowerShell, toda
    ejecucion (su lista cerrada esta vacia); lo que la via no sabe decidir (`indecidible`); el
    comando, si algo de lo que va antes o a la vez no esta en la lista cerrada; cada guion que no
    exista, no se pueda leer o -si no es el de `main`- no se pueda analizar; y el codigo, que se
    analiza. Devuelve si todos los guiones son el de `main` (codigo revisado)."""
    if ctx.powershell:
        raise BloqueoError(
            f"`{que}` en PowerShell: no se admite ninguna ejecucion (su lista cerrada esta "
            f"vacia).\nRegla: {R_EJECUCION}.\nComo reescribirlo: la herramienta Bash."
        )
    if indecidible:
        _niega(que, indecidible)
    _exigir_comando_verificable(ctx, lex, cmd, que, [p for p, _ in guiones])
    revisado = True
    for palabra, lenguaje in guiones:
        revisado = _exigir_guion_legible(ctx, lex, que, palabra, lenguaje) and revisado
    if codigo is not None:
        texto, lenguaje = codigo
        if re.search(r"\x00[SV]", texto):
            _niega(que, "el codigo se construye al ejecutarse", COMO_REESCRIBIR)
        _analizar_codigo_de(texto, lenguaje, ctx)
    return revisado


def _igual_que_en_main(raiz: Path, ruta: str, rel: str) -> bool:
    """Un guion es codigo revisado solo si es EXACTAMENTE el de `main` (decision del consultor del
    2026-10-01): mismo blob. Uno nuevo o cambiado en la rama en curso se lee entero."""
    del rel  # en minusculas; git necesita la ruta con su grafia
    relativa = os.path.relpath(ruta, raiz).replace("\\", "/")

    def git(*args: str) -> str | None:
        try:
            r = subprocess.run(
                ["git", "-c", "core.quotepath=false", *args],
                cwd=raiz,
                capture_output=True,
                encoding="utf-8",
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return r.stdout.strip() if r.returncode == 0 else None

    en_main = git("rev-parse", "--verify", "-q", f"main:{relativa}") or git(
        "rev-parse", "--verify", "-q", f"origin/main:{relativa}"
    )
    return en_main is not None and git("hash-object", "--", relativa) == en_main


SENSIBLES = (
    "corpus",
    "data/",
    "data\\",
    "xlsx",
    "holdout",
    "transcripciones",
    "cruda",
    "knowledge/cases",
    "knowledge/feedback",
    "material adicional",
    "backtest",
)


def analizar_codigo(codigo: str, ctx: Contexto, es_python: bool) -> None:
    """Codigo en linea (o un guion sin seguir). Cada literal de texto que sea una ruta se mira; y
    si el codigo recorre directorios o construye rutas con literales sensibles, no se decide."""
    exigir_sin_crudo(codigo, "el codigo que se ejecuta")
    literales = _literales(codigo, es_python)
    recorre = CODIGO_QUE_RECORRE.search(codigo) is not None
    directorios = 0
    for lit in literales:
        if not lit or len(lit) > 400 or "\n" in lit:
            continue
        ruta = _absoluta(lit, ctx.cwd)
        es_dir = os.path.isdir(ruta)
        directorios += es_dir
        motivo = ctx.politica.motivo_fichero(ruta)
        if motivo:
            raise BloqueoError(f"el codigo nombra {lit}.\nRegla: {motivo}.")
        if es_dir:
            # Un directorio que el codigo recorre se mira entero; uno que solo nombra, si esta
            # dentro de una zona con material protegido: lo que se abra bajo el no se sabe.
            motivo = ctx.politica.motivo_ruta(ruta, recursivo=recorre)
        if motivo:
            raise BloqueoError(
                f"el codigo nombra la carpeta {lit}, que contiene material protegido, y no se "
                f"puede decidir que abrira dentro.\nRegla: {motivo}.\nComo reescribirlo: rutas "
                "LITERALES de ficheros que se puedan leer, o la CLI del proyecto."
            )
    if recorre and not directorios and any(s in codigo.lower() for s in SENSIBLES):
        raise BloqueoError(
            "el codigo recorre directorios que construye al ejecutarse y nombra material "
            "sensible: no se puede decidir que ficheros abrira. Como reescribirlo: recorre una "
            "ruta LITERAL que no contenga material protegido, o usa la CLI del proyecto "
            "(`uv run botsito ...`), que es la puerta (casos_reservados, casos_ocultos)."
        )


def _literales(codigo: str, es_python: bool) -> list[str]:
    if es_python:
        try:
            arbol = ast.parse(codigo)
        except SyntaxError:
            pass
        else:
            return [
                n.value
                for n in ast.walk(arbol)
                if isinstance(n, ast.Constant) and isinstance(n.value, str)
            ]
    return [a or b for a, b in re.findall(r"'([^'\n]*)'|\"([^\"\n]*)\"", codigo)]


# ------------------------------------------------------------------------------- powershell
PS_LECTORES = re.compile(
    r"(?i)\b(get-content|gc|cat|type|select-string|sls|import-csv|import-excel|copy-item|cpi|"
    r"copy|expand-archive|compress-archive|readall\w*|openread|invoke-item|ii|start-process|"
    r"python\w*|py|uv|node|more|format-hex|fhx|get-filehash\s+-inputstream)\b"
)
PS_METADATOS = re.compile(
    r"(?i)^\s*(get-item|gi|get-childitem|gci|ls|dir|get-filehash|test-path|resolve-path|"
    r"split-path|measure-object|select-object|where-object|sort-object|format-\w+|ft|fl|"
    r"write-output|echo|write-host|out-string|join-path|get-location|pwd|set-location|cd|"
    r"foreach-object|%|\?)\b"
)


def _ejecucion_en_powershell(texto: str) -> str | None:
    """Cualquier ejecucion en un texto de PowerShell: un interprete, un shell, pytest, make,
    botsito, `uv run`, un lanzador (`Start-Process`, `Invoke-Item`...), el operador de llamada `&`
    o `. x` (dot-source), o un guion como primera palabra. Solo palabras SIN comillas: una cadena
    entre comillas no se ejecuta salvo tras `&`."""
    for segmento in re.split(r"[;|\n]|&&|\|\|", texto):
        fichas = re.findall(r"'[^']*'|\"[^\"]*\"|[^\s'\"]+", segmento)
        for k, ficha in enumerate(fichas):
            if ficha == "&" or (ficha == "." and k == 0):
                return " ".join(fichas[k : k + 2])
            if ficha[0] in "'\"":
                continue
            limpia = ficha.lstrip("$@({")
            nombre = _nombre_de_programa(limpia)
            siguiente = fichas[k + 1].lower() if k + 1 < len(fichas) else ""
            if (
                _es_interprete(nombre)
                or nombre in SHELLS
                or nombre in EJECUTORES - {"uv"}
                or nombre in PS_LANZADORES
                or (nombre == "uv" and siguiente == "run")
                or (k == 0 and limpia.lower().endswith(EXT_GUION))
            ):
                return segmento.strip()[:80]
    return None


def analizar_powershell(texto: str, ctx: Contexto) -> None:
    """Mas tosco que bash: rutas por las comillas y las palabras; si una es protegida, solo se
    deja pasar si TODOS los comandos del texto son de metadatos."""
    exigir_sin_crudo(texto, "PowerShell")
    ctx.powershell = True
    bajo = texto.lower()
    if re.search(r"(?i)\b(invoke-expression|iex|-encodedcommand|-enc)\b", texto):
        raise BloqueoError(
            f"PowerShell con `Invoke-Expression` o `-EncodedCommand`. {COMO_REESCRIBIR}"
        )
    for patron, regla in (
        (r"--no-verify", R_NO_VERIFY),
        (r"(?i)core\.hookspath\s*[=\s]\s*\S", R_NO_VERIFY),
        (r"\bgit\b[^;|&\n]*\bpush\b[^;|&\n]*(--force|\s-f\b|\s\+)", R_FORCE),
        (r"\bgit\b[^;|&\n]*\btag\b[^;|&\n]*\s(-d|--delete|-f|--force)\b", R_TAG),
        (r"\bgit\b[^;|&\n]*\b(cherry-pick|rebase)\b(?![^;|&\n]*--abort)", R_CHERRY),
    ):
        if re.search(patron, texto):
            raise BloqueoError(f"PowerShell: {patron}.\nRegla: {regla}.")
    for segmento in re.split(r"[;|\n]|&&|\|\|", texto):
        palabras = [
            a or b or c for a, b, c in re.findall(r"'([^']*)'|\"([^\"]*)\"|([^\s'\"]+)", segmento)
        ]
        if "git" in palabras and "push" in palabras[palabras.index("git") :]:
            argumentos = palabras[palabras.index("push", palabras.index("git")) + 1 :]
            decidir_borrado_remoto([None if re.search(r"[$`(]", a) else a for a in argumentos])
    if re.search(r"(?i)\b(remove-item|rm|ri|del|erase|rd|rmdir)\b[^;|\n]*-r", texto):
        for raiz in RAICES_INTOCABLES:
            if re.search(rf"(?i)(^|[\s'\"\\/.]){raiz}([\\/'\"\s]|$)", texto):
                raise BloqueoError(f"PowerShell: borrado recursivo sobre {raiz}/.\nRegla: {R_RM}.")
    if re.search(r"(?i)\bmake\b[^;|\n]*\bcheck\b", texto) and not re.search(
        r">\s*['\"]?(?!\$null|nul\b)[\w.\\/-]+", texto
    ):
        raise BloqueoError(f"`make check` sin la salida a un fichero.\nRegla: {R_DEVNULL}.")
    ejecucion = _ejecucion_en_powershell(texto)
    if ejecucion is not None:
        exigir_ejecucion_verificable(ctx, Lexico(), Comando([], [], [], {}, []), ejecucion)
    trozos = [
        a or b or c for a, b, c in re.findall(r"'([^']*)'|\"([^\"]*)\"|([^\s'\";|&(){}]+)", texto)
    ]
    protegido: str | None = None
    for t in trozos:
        if not t or t.startswith("-") or t.startswith("$"):
            continue
        ruta = _absoluta(t, ctx.cwd)
        motivo = ctx.politica.motivo_fichero(ruta) or (
            ctx.politica.motivo_dentro_de_zona(ruta) if os.path.isdir(ruta) else None
        )
        if motivo:
            protegido = f"{t}.\nRegla: {motivo}."
            break
    lectora = PS_LECTORES.search(texto)
    if protegido:
        segmentos = [s for s in re.split(r"[;|\n]|&&|\|\|", texto) if s.strip()]
        if lectora or not all(PS_METADATOS.match(s) for s in segmentos):
            raise BloqueoError(f"PowerShell lee el contenido de {protegido}")
        return
    dinamico = re.search(
        r"\$(?!env:|true\b|false\b|null\b|_\b|PSItem\b)\w|\$\(|-recurse|[*?]", bajo
    )
    if (
        lectora
        and dinamico
        and any(s in bajo for s in SENSIBLES + ("gci", "get-childitem", " ls ", "dir"))
    ):
        raise BloqueoError(
            "PowerShell lee contenido de rutas que solo se saben al ejecutar (variables, comodines "
            f"o -Recurse) y puede llegar a material protegido. {COMO_REESCRIBIR}"
        )
    if lectora and re.search(r"(?i)(get-childitem|gci|\bls\b|\bdir\b)[^;|\n]*-recurse", texto):
        motivo = ctx.politica.motivo_ruta(ctx.cwd, recursivo=True)
        if motivo:
            raise BloqueoError(
                f"PowerShell recorre {ctx.cwd} y lee su contenido.\nRegla: {motivo}."
            )


# ---------------------------------------------------------------------------- las herramientas
def decidir(evento: dict[str, object], politica: Politica) -> str | None:
    """El motivo del bloqueo, o None si pasa."""
    herramienta = str(evento.get("tool_name", ""))
    entrada = evento.get("tool_input") or {}
    if not isinstance(entrada, dict):
        return None
    cwd = str(evento.get("cwd") or politica.raiz)
    try:
        if herramienta == "Read":
            ruta = _absoluta(str(entrada.get("file_path", "")), cwd)
            motivo = politica.motivo_fichero(ruta)
            if motivo == R_TRAMO:
                prohibidas = politica.lineas_de_tramo(ruta)
                if prohibidas is not None:
                    desde = int(str(entrada.get("offset") or 1))
                    hasta = desde + int(str(entrada.get("limit") or 2000)) - 1
                    if not any(desde - 1 <= n <= hasta + 1 for n in prohibidas):
                        return None
                    motivo += (
                        f". Lineas en tramo no citable: {_rangos(prohibidas)}; lee con `offset` y "
                        "`limit` fuera de ellas, o `botsito corpus transcript show` fuera del tramo"
                    )
            return f"Read de {ruta}.\nRegla: {motivo}." if motivo else None
        if herramienta == "Grep":
            ruta = _absoluta(str(entrada.get("path") or cwd), cwd)
            motivo = politica.motivo_ruta(ruta, recursivo=True, respeta_ignore=True)
            return (
                f"Grep sobre {ruta} llega a material protegido.\nRegla: {motivo}.\nComo "
                "reescribirlo: una ruta que no lo contenga."
                if motivo
                else None
            )
        if herramienta == "Glob":
            return None  # listar nombres no es abrir (ADR-0021 §1)
        if herramienta in {"Bash", "PowerShell"}:
            comando = str(entrada.get("command", ""))
            ctx = Contexto(politica, cwd)
            if herramienta == "Bash":
                analizar_bash(comando, ctx)
            else:
                analizar_powershell(comando, ctx)
            return None
    except BloqueoError as exc:
        return str(exc)
    return None


def _menciona_material(evento: dict[str, object]) -> bool:
    texto = json.dumps(evento.get("tool_input", {}), ensure_ascii=False).lower()
    return any(s in texto for s in SENSIBLES + ("rm ", "push", "--no-verify", "tag "))


def main() -> int:
    for flujo in (sys.stdout, sys.stderr):
        reconfigurar = getattr(flujo, "reconfigure", None)
        if reconfigurar:
            reconfigurar(encoding="utf-8")
    try:
        evento = json.loads(sys.stdin.buffer.read().decode("utf-8") or "{}")
    except ValueError:
        print("guardia: el evento no es JSON; se bloquea por prudencia", file=sys.stderr)
        return 2
    try:
        motivo = decidir(evento, Politica(RAIZ))
    except Exception as exc:  # noqa: BLE001  # la guardia no puede caerse en silencio
        if not _menciona_material(evento):
            return 0
        motivo = (
            f"la guardia fallo ({type(exc).__name__}: {exc}) ante algo que toca material sensible"
        )
    if motivo:
        print(f"GUARDIA (.claude/hooks/guardia.py) bloquea: {motivo}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
