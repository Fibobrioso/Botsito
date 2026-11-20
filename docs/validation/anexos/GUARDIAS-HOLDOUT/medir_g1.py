"""G1 · ESTUDIO, sin implementar: fechas de dias ocultos en lo que añaden las ramas cerradas.

Rama `trabajo/guardias-holdout` (encargo del consultor del 2026-11-19; GUARDIAS-HOLDOUT.md, G1).
Mide, sobre las lineas AÑADIDAS por los commits de las ramas cerradas desde
`stable/F39a-guardia-falsos-positivos` (incluida) y sobre sus mensajes de commit, cuantas lineas
contienen como AAAA-MM-DD un dia oculto, por CLASE. `knowledge/cases/holdout/` queda fuera de la
unica llamada que lee diffs, con una pathspec de exclusion.

Los dias ocultos salen de la puerta (`botsito.cases.holdout.casos_ocultos`) y viven solo en memoria:
NO se imprime ninguna fecha, ningun id de caso, ninguna linea ni ningun nombre de fichero. Solo
recuentos, por clase y por rama (el nombre de su tag, que no lleva fecha).

Cada llamada a git es LITERAL entera -subcomando, rango y pathspec-: la guardia de Claude Code
niega en un guion sin revisar un `git` con un argumento que se construye al ejecutarse, y la clave
`-c core.quotepath` (medido el 2026-11-19 con la guardia por stdin; GUARDIAS-HOLDOUT.md, G1). Por
eso el reparto por rama se reconstruye en Python a partir del grafo, y no con un `rev-list` por
merge.

Uso (desde la raiz del repo):
    uv run python docs/validation/anexos/GUARDIAS-HOLDOUT/medir_g1.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.holdout import cargar_meses_reservados, casos_ocultos  # noqa: E402

# El primer dia del proyecto (docs/runbooks/DECISIONES-DE-PROCESO.md, las tres primeras
# decisiones): una fecha anterior no puede ser una fecha de trabajo.
INICIO_PROYECTO = "2026-09-04"
FECHA = re.compile(r"(?<!\d)(\d{4}-\d{2}-\d{2})(?!\d)")
FIN_DE_CASO = re.compile(r"-(\d{4}-\d{2}-\d{2})$")
CASO_DELANTE = re.compile(r"caso-[A-Za-z]+-$")
ID_DE_CASO = re.compile(r"caso-[A-Za-z]+-\d{4}-\d{2}-\d{2}")
IDS_OCULTOS: set[str] = set()  # se llena en main(), solo en memoria
SEP = "\x1e"  # separador de registros en los --format (no sale en ningun texto del repo)

CLASES = (
    "trailer Fuente: (mensaje)",
    "mensaje de commit, fuera del trailer",
    "uv.lock",
    "fichero de asignacion (particiones.yaml)",
    "id de trabajo (ev-/fb-/...-sesion-)",
    "id de caso (caso-...)",
    "docs/state/",
    "docs/validation/HOLDOUT-EXPOSICIONES.md",
    "prosa de docs/",
    "codigo o tests",
    "otra",
)
CODIGO = (".py", ".mqh", ".mq5", ".sh", ".ps1", ".toml", ".cfg", ".ini")


def _salida(r: subprocess.CompletedProcess[str]) -> str:
    r.check_returncode()
    return r.stdout


def grafo() -> str:
    """`<sha> <padres>` de cada commit del rango, merges incluidos."""
    return _salida(
        subprocess.run(
            ["git", "log", "--format=%H %P", "stable/F39a-guardia-falsos-positivos^1..main"],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    )


def mensajes() -> str:
    """El mensaje de cada commit del rango, merges incluidos, tras `SEP<sha>`."""
    return _salida(
        subprocess.run(
            ["git", "log", "--format=%x1e%H%n%B", "stable/F39a-guardia-falsos-positivos^1..main"],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    )


def diffs() -> str:
    """Lo que añade cada commit sin merge del rango, tras `SEP<sha>`, sin el holdout."""
    return _salida(
        subprocess.run(
            [
                "git",
                "log",
                "--no-merges",
                "-p",
                "-U0",
                "--no-renames",
                "--no-color",
                "--format=%x1e%H",
                "stable/F39a-guardia-falsos-positivos^1..main",
                "--",
                ".",
                ":(exclude)knowledge/cases/holdout/",
            ],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    )


def tags() -> str:
    """`<objeto> <commit pelado> <tag>` de cada tag stable/."""
    return _salida(
        subprocess.run(
            [
                "git",
                "for-each-ref",
                "--format=%(objectname) %(*objectname) %(refname:short)",
                "refs/tags/stable/",
            ],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    )


def cabeza_de_main() -> str:
    return _salida(
        subprocess.run(
            ["git", "rev-parse", "main"],
            cwd=RAIZ,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    ).strip()


def dias_ocultos() -> frozenset[str]:
    salida: set[str] = set()
    for caso in casos_ocultos(RAIZ):
        m = FIN_DE_CASO.search(caso)
        if m:
            salida.add(m.group(1))
    return frozenset(salida)


def es_id_de_trabajo(linea: str, ini: int, fin: int) -> bool:
    return linea[max(0, ini - 3) : ini] in ("fb-", "ev-") or linea[fin:].startswith("-sesion")


def es_id_de_caso(linea: str, ini: int) -> bool:
    return CASO_DELANTE.search(linea[max(0, ini - 20) : ini]) is not None


def clase_de_linea(
    fichero: str | None, linea: str, dias: frozenset[str]
) -> tuple[str, bool] | None:
    """(clase, alguna anterior al proyecto) de una linea con un dia de `dias`, o None si no tiene.
    `fichero` None: la linea es del mensaje de commit."""
    ocultas = [(m.start(1), m.end(1), m.group(1)) for m in FECHA.finditer(linea)]
    ocultas = [(i, f, d) for i, f, d in ocultas if d in dias]
    if not ocultas:
        return None
    anterior = any(d < INICIO_PROYECTO for _, _, d in ocultas)
    if fichero is None:
        return (CLASES[0] if re.match(r"\s*Fuente:", linea) else CLASES[1]), anterior
    if fichero == "uv.lock":
        return CLASES[2], anterior
    if fichero.startswith("knowledge/cases/") and fichero.endswith("/particiones.yaml"):
        return CLASES[3], anterior
    if all(es_id_de_trabajo(linea, i, f) for i, f, _ in ocultas):
        return CLASES[4], anterior
    if any(es_id_de_caso(linea, i) for i, _, _ in ocultas):
        exacto = any(x in IDS_OCULTOS for x in ID_DE_CASO.findall(linea))
        return (CLASES[5] + (", id exacto" if exacto else ", solo la fecha")), anterior
    if fichero.startswith("docs/state/"):
        return CLASES[6], anterior
    if fichero == "docs/validation/HOLDOUT-EXPOSICIONES.md":
        return CLASES[7], anterior
    if fichero.startswith("docs/"):
        return CLASES[8], anterior
    if fichero.startswith(("src/", "tests/", "scripts/", ".claude/", "mql5/")) or fichero.endswith(
        CODIGO
    ):
        return CLASES[9], anterior
    return CLASES[10], anterior


# Lo que dice que una fecha es de TRABAJO y no de mercado: una de estas palabras en los 60
# caracteres de delante (la decision, la rama, la sesion grabada, el dia en que se escribio).
MARCA_DE_TRABAJO = re.compile(
    r"(?i)(consultor|decisi[oó]n|respuesta|encargo|rama|cerrad|abiert|escrit|declarad|recibid|"
    r"grabad|sesi[oó]n|commit|merge|orden|revisor|_el\b|el d[ií]a que)"
)


# Lo que dice que una fecha es de MERCADO: una hora detras, o una palabra del metodo cerca.
MARCA_DE_MERCADO = re.compile(
    r"(?i)(\d{1,2}:\d{2}|\bH4\b|\bM15\b|\bM1\b|operaci[oó]n|entrada|stop|vela|compra|venta|"
    r"ruptura|caja|liquidez|no_trade|sesgo|escenario|\bcaso\b)"
)


def alguna_de_mercado(linea: str, dias: frozenset[str]) -> bool:
    """Algun dia oculto de la linea tiene una marca de mercado en los 40 caracteres de cada lado."""
    for m in FECHA.finditer(linea):
        if m.group(1) in dias:
            alrededor = (
                linea[max(0, m.start(1) - 40) : m.start(1)] + linea[m.end(1) : m.end(1) + 40]
            )
            if MARCA_DE_MERCADO.search(alrededor):
                return True
    return False


def ids_de_caso_en_main() -> str:
    """Cada id `caso-<simbolo>-AAAA-MM-DD` del arbol de main, con su fichero, fuera del holdout."""
    r = subprocess.run(
        [
            "git",
            "grep",
            "-o",
            "-I",
            "-E",
            "caso-[A-Za-z]+-[0-9]{4}-[0-9]{2}-[0-9]{2}",
            "main",
            "--",
            ".",
            ":(exclude)knowledge/cases/holdout/",
        ],
        cwd=RAIZ,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if r.returncode not in (0, 1):  # 1: ninguna coincidencia
        r.check_returncode()
    return r.stdout


def todas_de_trabajo(linea: str, dias: frozenset[str]) -> bool:
    """Cada dia oculto de la linea lleva delante una marca de trabajo."""
    ocultas = [m for m in FECHA.finditer(linea) if m.group(1) in dias]
    return all(
        MARCA_DE_TRABAJO.search(linea[max(0, m.start(1) - 60) : m.start(1)]) for m in ocultas
    )


def carpeta(fichero: str | None) -> str:
    """La carpeta de primer o segundo nivel (nunca el nombre del fichero, que puede llevar una
    fecha)."""
    if fichero is None:
        return "(mensaje de commit)"
    partes = fichero.split("/")
    return (
        "/".join(partes[:2]) if len(partes) > 2 else (partes[0] if len(partes) == 2 else "(raiz)")
    )


def por_registro(texto: str) -> dict[str, list[str]]:
    """`sha -> lineas` de una salida con `SEP<sha>` delante de cada commit."""
    salida: dict[str, list[str]] = {}
    for trozo in texto.split(SEP)[1:]:
        lineas = trozo.split("\n")
        salida[lineas[0].strip()] = lineas[1:]
    return salida


def lineas_añadidas(lineas: list[str]) -> list[tuple[str, str]]:
    """(fichero, linea) de cada linea añadida de un `-p`."""
    salida: list[tuple[str, str]] = []
    fichero: str | None = None
    for x in lineas:
        if x.startswith("+++ "):
            # Sin `-c core.quotepath=false`: una ruta con caracteres no ASCII sale entre comillas
            # y con escapes; para la clase basta el prefijo.
            ruta = x[4:].strip('"')
            fichero = ruta[2:] if ruta.startswith("b/") else None
        elif x.startswith("+") and fichero is not None:
            salida.append((fichero, x[1:]))
    return salida


def ramas(padres: dict[str, list[str]], nombres: dict[str, str]) -> list[tuple[str, set[str]]]:
    """(rama, commits) de cada merge de la primera linea de main dentro del rango (los commits que
    trae su segundo padre y no estan en esa primera linea), mas los commits de estado de main."""
    primera: list[str] = []
    c: str | None = cabeza_de_main()
    while c is not None and c in padres:
        primera.append(c)
        c = padres[c][0] if padres[c] else None
    en_primera = set(primera)
    salida: list[tuple[str, set[str]]] = []
    for m in reversed(primera):
        if len(padres[m]) < 2:
            continue
        propios: set[str] = {m}
        pila = [padres[m][1]]
        while pila:
            x = pila.pop()
            if x in propios or x in en_primera or x not in padres:
                continue
            propios.add(x)
            pila.extend(padres[x])
        salida.append((nombres.get(m, "merge sin tag"), propios))
    estado = {x for x in primera if len(padres[x]) < 2}
    salida.append(("commits de main sin merge (docs(state))", estado))
    return salida


def main() -> int:
    dias = dias_ocultos()
    IDS_OCULTOS.update(casos_ocultos(RAIZ))
    meses = set(cargar_meses_reservados(RAIZ))
    padres = {
        partes[0]: partes[1:] for partes in (x.split() for x in grafo().splitlines()) if partes
    }
    nombres: dict[str, str] = {}
    for x in tags().splitlines():
        partes = x.split()
        if len(partes) == 3:
            nombres[partes[1]] = partes[2]
        elif len(partes) == 2:
            nombres[partes[0]] = partes[1]
    msj = por_registro(mensajes())
    dif = por_registro(diffs())

    print(
        f"dias ocultos (casos_ocultos): {len(dias)}; desde el inicio del proyecto: "
        f"{sum(d >= INICIO_PROYECTO for d in dias)}; meses reservados enteros: {len(meses)}"
    )
    print(f"commits en el rango: {len(padres)} (con diff fuera del holdout: {len(dif)})")
    total: Counter[tuple[str, bool]] = Counter()
    detalle: Counter[tuple[str, str, str, bool, bool, bool]] = Counter()
    filas: list[tuple[str, int, int, int]] = []
    lineas_vistas = lineas_mes = 0
    for nombre, commits in ramas(padres, nombres):
        n_rama = 0
        for sha in commits:
            pares: list[tuple[str | None, str]] = [(None, x) for x in msj.get(sha, [])]
            pares += lineas_añadidas(dif.get(sha, []))
            for fichero, linea in pares:
                lineas_vistas += 1
                if any(d[:7] in meses for d in FECHA.findall(linea)):
                    lineas_mes += 1
                clase = clase_de_linea(fichero, linea, dias)
                if clase:
                    total[clase] += 1
                    n_rama += 1
                    trabajo = todas_de_trabajo(linea, dias)
                    mercado = alguna_de_mercado(linea, dias)
                    clave = (nombre, clase[0], carpeta(fichero), clase[1], trabajo, mercado)
                    detalle[clave] += 1
        merges = sum(len(padres[s]) > 1 for s in commits)
        filas.append((nombre, len(commits) - merges, merges, n_rama))
    print(f"lineas miradas (añadidas y de mensajes): {lineas_vistas}")
    print("")
    print("| Clase | Lineas con un dia oculto | De ellas, con uno anterior al proyecto |")
    print("|---|---|---|")
    for c in sorted(
        {k for k, _ in total} | set(CLASES),
        key=lambda x: (next(i for i, c in enumerate(CLASES) if x.startswith(c)), x),
    ):
        n_si, n_no = total[(c, True)], total[(c, False)]
        print(f"| {c} | {n_si + n_no} | {n_si} |")
    print(f"| TOTAL | {sum(total.values())} | {sum(v for (_, a), v in total.items() if a)} |")
    print("")
    print("| Rama | Commits sin merge | Merges | Lineas con un dia oculto |")
    print("|---|---|---|---|")
    for nombre, n_c, n_m, n in filas:
        print(f"| {nombre} | {n_c} | {n_m} | {n} |")
    print("")
    print(
        "| Rama | Clase | Carpeta (1.er o 2.o nivel) | Anterior al proyecto | Marca de trabajo "
        "delante de cada una | Marca de mercado cerca de alguna | Lineas |"
    )
    print("|---|---|---|---|---|---|---|")
    for (nombre, c, carp, anterior, trabajo, mercado), n in sorted(detalle.items()):
        si = {True: "si", False: "no"}
        print(f"| {nombre} | {c} | {carp} | {si[anterior]} | {si[trabajo]} | {si[mercado]} | {n} |")
    print("")
    print(f"lineas con una fecha AAAA-MM-DD de un MES reservado entero: {lineas_mes}")
    print("")
    en_main: Counter[str] = Counter()
    exactos: Counter[str] = Counter()
    ids_ocultos = set(casos_ocultos(RAIZ))
    todos = 0
    for x in ids_de_caso_en_main().splitlines():
        # `main:<ruta>:<id>`; la ruta solo se usa para su carpeta, el id solo para su fecha
        partes = x.split(":")
        if len(partes) < 3:
            continue
        todos += 1
        m = FIN_DE_CASO.search(partes[-1])
        if m and m.group(1) in dias:
            en_main[carpeta(":".join(partes[1:-1]))] += 1
            if partes[-1] in ids_ocultos:
                exactos[carpeta(":".join(partes[1:-1]))] += 1
    print(
        f"ids de caso en el arbol de main (fuera del holdout): {todos}; con un dia oculto: "
        f"{sum(en_main.values())}"
    )
    print(f"  de ellos, el id EXACTO de un caso oculto: {sum(exactos.values())}")
    for carp, n in sorted(en_main.items()):
        print(f"  {carp}: {n} (id exacto: {exactos[carp]})")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - el mensaje podria nombrar un fichero o un caso
        print(f"medir_g1: fallo ({type(exc).__name__}); sin el mensaje, que podria nombrar un caso")
        sys.exit(1)
