"""Cambia la fecha de una sesion del kit sin cambiar nada mas. F10, ADR-0011.

El id de un paquete lleva la fecha dentro (`AAAA-MM-DD-sesion-NN`), y el registro de feedback
exige que la fecha de cada respuesta sea la de su sesion. Si la reunion se mueve, el paquete hay
que rehacerlo con la fecha nueva o cada respuesta nacera con una fecha que no es.

Rehacerlo a mano tiene una trampa: `kit build` pide un `--seed`, y el seed decide que dias caen
en `dev` y cuales quedan reservados. Con otro seed el paquete sale con dias distintos, no falla
nada y nadie se entera. Aqui el seed no se teclea: se lee del paquete que ya existe, y despues se
comprueba que los casos y su reparto son EXACTAMENTE los mismos que antes. Si no lo son, se
restaura el paquete original y no se toca nada.

Uso:
    uv run --no-sync python scripts/mover_sesion.py --a 2026-09-22
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.paquete import (  # noqa: E402
    DIRECTORIO_KIT,
    comprobar,
    construir,
    escribir,
    esquema_paquete,
    sesiones_del_kit,
)
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.feedback.modelo import cargar_feedback  # noqa: E402

FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$", re.ASCII)


def sesion_unica(sesion: str | None) -> str:
    sesiones = sesiones_del_kit(RAIZ)
    if not sesiones:
        raise SystemExit("no hay ningun paquete en knowledge/cases/kit/")
    if sesion:
        if sesion not in sesiones:
            raise SystemExit(f"no existe el paquete {sesion} (hay {sesiones})")
        return sesion
    if len(sesiones) > 1:
        raise SystemExit(f"hay varios paquetes {sesiones}: di cual con --sesion")
    return sesiones[0]


def sin_etiquetar(sesion: str) -> None:
    """Una vez etiquetado, el reparto es inmutable: rehacer el paquete seria borrar la prueba."""
    directorio = RAIZ / "knowledge" / "feedback"
    registros = cargar_feedback(directorio) if directorio.is_dir() else []
    etiquetas = [r for r in registros if r.sesion == sesion and r.accion == "LABEL_CASE"]
    if etiquetas:
        raise SystemExit(
            f"{sesion} ya tiene {len(etiquetas)} LABEL_CASE: el reparto esta congelado y la fecha "
            "no se puede mover sin invalidar el etiquetado ciego"
        )
    de_esa_sesion = [r for r in registros if r.sesion == sesion]
    if de_esa_sesion:
        raise SystemExit(
            f"{sesion} ya tiene {len(de_esa_sesion)} registros de feedback: quedarian huerfanos "
            "con la fecha nueva; muevelos tu antes o quedate con la fecha actual"
        )


def huella(sesion: str) -> tuple[list[str], dict[str, str], list[str]]:
    """Lo que NO puede cambiar al mover la fecha: los casos, su reparto y las preguntas."""
    cuestionario, ventanas, particiones = esquema_paquete(RAIZ, sesion)
    casos = [str(c["id"]).replace(sesion, "") for c in ventanas["casos"]]
    reparto = {str(k).replace(sesion, ""): str(v) for k, v in particiones["asignacion"].items()}
    preguntas = [str(p["titulo"]) for p in cuestionario["preguntas"]]
    return casos, reparto, preguntas


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--a", dest="fecha", required=True, help="fecha real de la sesion, AAAA-MM-DD")
    ap.add_argument("--sesion", help="paquete a mover (por defecto, el unico que hay)")
    args = ap.parse_args()
    if not FECHA.match(args.fecha):
        raise SystemExit(f"fecha {args.fecha!r} invalida: se escribe AAAA-MM-DD")

    vieja = sesion_unica(args.sesion)
    nueva = f"{args.fecha}{vieja[10:]}"
    if nueva == vieja:
        print(f"OK: {vieja} ya tiene esa fecha; no hay nada que mover.")
        return 0
    if nueva in sesiones_del_kit(RAIZ):
        raise SystemExit(f"ya existe el paquete {nueva}: borralo antes o elige otra fecha")
    sin_etiquetar(vieja)

    _, _, particiones = esquema_paquete(RAIZ, vieja)
    seed = int(particiones["seed"])
    antes = huella(vieja)
    carpeta_vieja = RAIZ / DIRECTORIO_KIT / vieja

    respaldo = Path(tempfile.mkdtemp(prefix="kit-")) / vieja
    shutil.copytree(carpeta_vieja, respaldo)
    try:
        shutil.rmtree(carpeta_vieja)
        escribir(RAIZ, construir(RAIZ, carpeta_datos(RAIZ), nueva, seed))
        despues = huella(nueva)
        if despues != antes:
            raise SystemExit(
                "el paquete reconstruido NO es el mismo (casos, reparto o preguntas han "
                "cambiado): se restaura el original y no se mueve nada"
            )
        problemas, _ = comprobar(RAIZ, carpeta_datos(RAIZ), nueva)
        if problemas:
            raise SystemExit("el paquete nuevo no se recompone: " + "; ".join(problemas))
    except BaseException:
        shutil.rmtree(RAIZ / DIRECTORIO_KIT / nueva, ignore_errors=True)
        if not carpeta_vieja.exists():
            shutil.copytree(respaldo, carpeta_vieja)
        raise
    finally:
        shutil.rmtree(respaldo.parent, ignore_errors=True)

    casos, reparto, preguntas = antes
    dev = sum(1 for v in reparto.values() if v == "dev")
    print(f"OK: {vieja} -> {nueva} (seed {seed} reutilizado)")
    print(f"    {len(preguntas)} preguntas, {len(casos)} casos, {dev} dias para etiquetar: iguales")
    viejo_docx = RAIZ / f"Sesion 1 - hoja de respuestas ({vieja}).docx"
    if viejo_docx.exists():
        viejo_docx.unlink()
        print(f"    borrada la hoja vieja: {viejo_docx.name}")
    print("\nAhora regenera la hoja y commitea el paquete ANTES de la sesion:")
    print(f"    uv run --no-sync python scripts/hoja_sesion_docx.py --sesion {nueva}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit as salida_:
        if isinstance(salida_.code, str):
            print(f"ERROR: {salida_.code}", file=sys.stderr)
            raise SystemExit(1) from None
        raise
