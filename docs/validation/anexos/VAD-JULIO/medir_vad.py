"""La medida de D3 y D4 de trabajo/vad-julio (docs/validation/VAD-JULIO.md): compara la cruda de
una o varias candidatas con la de la referencia K0 (la transcripcion ACTIVA del video), con el
criterio escrito antes de correr ninguna candidata (VAD-JULIO.md §2).

Uso (la raiz y la salida por argumento):

    uv run python docs/validation/anexos/VAD-JULIO/medir_vad.py --repo . --datos data \
        --video v14 --salida docs/validation/anexos/VAD-JULIO/medida-v14.txt \
        --candidata K1=transcripciones/v14/ensayo-... --candidata K2=transcripciones/v14/ensayo-...

Cada cruda se lee con `cargar_cruda(carpeta, filtro_de(...))`, FILTRADA, y la salida dice cuantos
segmentos oculto el filtro en cada una. No imprime texto del ASR salvo las palabras utiles del
minuto de control (v14 0:10:00-0:11:00, el que escucho Aleks), normalizadas.

**Palabra util:** una palabra con tiempo de un segmento que no lleva `repeticion`, `compresion` ni
`no_habla` (`baja_prob` no excluye) y cuyo texto normalizado no se repite identico en 3 o mas
segmentos visibles de la misma cruda. Los segundos son los de la UNION de los intervalos de las
palabras utiles (no la duracion de los segmentos).
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

from botsito.cases.holdout import meses_libres
from botsito.corpus.cuarentena import filtro_de
from botsito.corpus.glosario import aplicar, cargar_glosario
from botsito.corpus.pipeline_transcripcion import cargar_cruda
from botsito.corpus.transcripcion import Segmento

EXCLUYEN = frozenset({"repeticion", "compresion", "no_habla"})
REPETICIONES_MAX = 3  # 3 o mas segmentos con el mismo texto normalizado: fuera de «util»
CONTROL_VIDEO = "v14"
CONTROL_MS = (600_000, 660_000)  # v14 0:10:00-0:11:00
CONTROL_PALABRAS = ("bias", "bajista")
CONTROL_OTRAS_MAX = 4
UMBRAL_PIERDE = 0.10
UMBRAL_SOSPECHA = 0.05

Intervalos = list[tuple[int, int]]


def normalizar(texto: str) -> str:
    """Minusculas, sin acentos, sin signos de puntuacion, espacios colapsados."""
    sin_acentos = "".join(
        c for c in unicodedata.normalize("NFD", texto.casefold()) if not unicodedata.combining(c)
    )
    limpio = "".join(c if c.isalnum() or c.isspace() else " " for c in sin_acentos)
    return " ".join(limpio.split())


def unir(intervalos: Intervalos) -> Intervalos:
    salida: Intervalos = []
    for a, b in sorted(i for i in intervalos if i[1] > i[0]):
        if salida and a <= salida[-1][1]:
            salida[-1] = (salida[-1][0], max(salida[-1][1], b))
        else:
            salida.append((a, b))
    return salida


def medida(intervalos: Intervalos) -> int:
    return sum(b - a for a, b in intervalos)


def interseccion(x: Intervalos, y: Intervalos) -> Intervalos:
    salida: Intervalos = []
    i = j = 0
    while i < len(x) and j < len(y):
        a, b = max(x[i][0], y[j][0]), min(x[i][1], y[j][1])
        if a < b:
            salida.append((a, b))
        if x[i][1] < y[j][1]:
            i += 1
        else:
            j += 1
    return salida


def diferencia_ms(x: Intervalos, y: Intervalos) -> int:
    """Medida de x menos y (los dos ya unidos)."""
    return medida(x) - medida(interseccion(x, y))


class Cruda:
    def __init__(self, repo: Path, datos: Path, video: str, carpeta_rel: str) -> None:
        self.carpeta_rel = carpeta_rel
        carpeta = datos / carpeta_rel
        filtro = filtro_de(repo, video, meses_libres(repo))
        self.visibles: list[Segmento] = cargar_cruda(carpeta, filtro)
        self.ocultos = len(filtro.ocultos)
        cuenta = Counter(normalizar(s.texto) for s in self.visibles)
        self.utiles: list[Segmento] = []
        self.solo_por_repeticion = 0
        for s in self.visibles:
            por_senal = bool(EXCLUYEN & set(s.senales))
            por_repeticion = cuenta[normalizar(s.texto)] >= REPETICIONES_MAX
            if not por_senal and not por_repeticion:
                self.utiles.append(s)
            elif por_repeticion and not por_senal:
                self.solo_por_repeticion += 1
        self.palabras: Intervalos = unir(
            [(p.t0_ms, p.t1_ms) for s in self.utiles for p in s.palabras]
        )

    def control(self, glosario: object) -> list[str]:
        """Las palabras utiles del minuto de control, normalizadas y con el glosario aplicado."""
        a, b = CONTROL_MS
        trozos: list[Segmento] = []
        for s in self.utiles:
            dentro = [p.texto for p in s.palabras if a <= p.t0_ms < b]
            if dentro:
                trozos.append(Segmento(len(trozos), s.t0_ms, s.t1_ms, " ".join(dentro)))
        corregidos, _registro, _dudas = aplicar(trozos, glosario)  # type: ignore[arg-type]
        return [t for s in corregidos for t in normalizar(s.texto).split()]


def _activa(repo: Path, video: str) -> dict[str, object]:
    docs = [
        yaml.safe_load(p.read_text(encoding="utf-8"))
        for p in sorted((repo / "knowledge/corpus/transcripciones").glob(f"tr-{video}-*.yaml"))
    ]
    reemplazados = {d.get("reemplaza_a") for d in docs if d.get("reemplaza_a")}
    activas = [d for d in docs if d["transcripcion_id"] not in reemplazados]
    if len(activas) != 1:
        raise SystemExit(f"ERROR: {video} tiene {len(activas)} transcripciones activas")
    return activas[0]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", required=True, type=Path)
    ap.add_argument("--datos", required=True, type=Path, help="la carpeta [rutas].data")
    ap.add_argument("--video", required=True)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument(
        "--referencia",
        help="transcripcion_id de K0 (por defecto, la activa del video)",
    )
    ap.add_argument(
        "--candidata",
        action="append",
        default=[],
        help="NOMBRE=carpeta relativa a --datos (transcripciones/<video>/...)",
    )
    args = ap.parse_args(argv)
    repo = args.repo.resolve()
    datos = args.datos if args.datos.is_absolute() else (repo / args.datos)
    if args.referencia:
        ruta = repo / "knowledge/corpus/transcripciones" / f"{args.referencia}.yaml"
        k0 = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    else:
        k0 = _activa(repo, args.video)
    huecos: Intervalos = unir([(h["desde_ms"], h["hasta_ms"]) for h in k0["huecos"]])  # type: ignore[index]
    glosario = cargar_glosario(repo / "knowledge/corpus/glosario_asr.yaml")
    candidatas = [("K0", str(k0["carpeta"]))]
    for c in args.candidata:
        nombre, _, carpeta = c.partition("=")
        if not nombre or not carpeta:
            raise SystemExit(f"ERROR: --candidata {c!r}: se espera NOMBRE=carpeta")
        candidatas.append((nombre, carpeta))

    crudas = {n: Cruda(repo, datos, args.video, c) for n, c in candidatas}
    ref = crudas["K0"]
    ref_ms = medida(ref.palabras)
    lineas: list[str] = [
        f"# medir_vad.py · {args.video} · K0 = {k0['transcripcion_id']} ({k0['carpeta']})",
        f"# huecos de mas de 30 s de K0: {len(huecos)}, {medida(huecos) / 1000:.1f} s",
        "",
        "| Candidata | Carpeta | Segmentos visibles | Ocultos | Utiles | Seg. utiles (s) "
        "| (i) bias y bajista | (ii) otras palabras | (iii) gana (s) | (iv) pierde "
        "| (v) sospecha | Cumple |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    detalle: list[str] = []
    for nombre, cr in crudas.items():
        gana_ms = medida(interseccion(cr.palabras, huecos))
        pierde = diferencia_ms(ref.palabras, cr.palabras) / ref_ms if ref_ms else 0.0
        sospecha = cr.solo_por_repeticion / len(cr.visibles) if cr.visibles else 0.0
        if args.video == CONTROL_VIDEO:
            tokens = cr.control(glosario)
            i_ok = all(p in tokens for p in CONTROL_PALABRAS)
            otras = [t for t in tokens if t not in CONTROL_PALABRAS]
            ii_ok = len(otras) <= CONTROL_OTRAS_MAX
            i_txt, ii_txt = ("si" if i_ok else "no"), f"{len(otras)} ({'si' if ii_ok else 'no'})"
            detalle.append(f"- {nombre}: palabras utiles del minuto de control: {tokens}")
        else:
            i_ok = ii_ok = True
            i_txt = ii_txt = "n/a"
        cumple = (
            i_ok and ii_ok and pierde <= UMBRAL_PIERDE and sospecha <= UMBRAL_SOSPECHA
        )
        if nombre == "K0":
            cumple_txt = "referencia"
        else:
            cumple_txt = "si" if cumple else "no"
        lineas.append(
            f"| {nombre} | `{cr.carpeta_rel}` | {len(cr.visibles)} | {cr.ocultos} | "
            f"{len(cr.utiles)} | {medida(cr.palabras) / 1000:.1f} | {i_txt} | {ii_txt} | "
            f"{gana_ms / 1000:.1f} | {pierde:.3f} | {sospecha:.3f} | {cumple_txt} |"
        )
        por_hueco = [
            f"{a / 1000:.1f}-{b / 1000:.1f}: {medida(interseccion(cr.palabras, [(a, b)])) / 1000:.1f} s"
            for a, b in huecos
        ]
        detalle.append(f"- {nombre}: (iii) por hueco de K0: " + "; ".join(por_hueco))
        if nombre != "K0":
            ganados = [
                f"{s.t0_ms / 1000:.1f}-{s.t1_ms / 1000:.1f}"
                for s in cr.utiles
                if interseccion(unir([(p.t0_ms, p.t1_ms) for p in s.palabras]), huecos)
            ]
            detalle.append(
                f"- {nombre}: segmentos utiles con palabras en los huecos de K0 (s, sin texto): "
                + ", ".join(ganados)
            )
    lineas += ["", *detalle, ""]
    texto = "\n".join(lineas)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(texto, encoding="utf-8", newline="\n")
    sys.stdout.write(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
