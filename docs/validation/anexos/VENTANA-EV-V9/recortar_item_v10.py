"""Sustituye ev-v10-010438-0d4e6798 por un item nuevo con la cita y la ventana recortadas antes del
segmento 1058 (decision del consultor del 2026-10-05 sobre ese item), SIN que el texto pase por la
sesion. Hermano de `sustituir_item.py`: replica igual `botsito evidence new --supersede`
(`src/botsito/cli.py:988-1040`; los `campos` de cli.py:1014-1032, `escribir_item(entorno.directorio,
campos, entorno.comprobar)` de cli.py:1034, y `_EntornoEvidencia.comprobar` de cli.py:621-670, que
desde esta rama llama a `ventana_no_citable`).

- La cita nueva es el prefijo MAS LARGO de la vieja (cortada por palabras, sin el separador final)
  cuya localizacion, con `localizar_cita` (la de `verificar_citas`), cae entera antes del segmento
  1058 y aparece una sola vez. Los segmentos salen por `contexto.crudas`, el llamador autorizado.
- La ventana nueva: el mismo inicio y el fin en el ultimo segundo entero que no solapa el 1058.
- Copia los demas campos del viejo; cambian `t1`, `cita_literal`, `supersede` y `notas` (y el id).

Solo imprime ids, segmentos, milisegundos y el resultado de las comprobaciones: nunca la cita ni la
afirmacion, ni cuantas palabras tiene la cita.

Uso (desde la raiz del repo):
    uv run python docs/validation/anexos/VENTANA-EV-V9/recortar_item_v10.py vieja
        (la cita y la ventana viejas: tiene que rechazarlo ventana_no_citable)
    uv run python docs/validation/anexos/VENTANA-EV-V9/recortar_item_v10.py nueva
        (las recortadas: comprueba y escribe el item nuevo)
"""

from __future__ import annotations

import sys
from dataclasses import asdict, replace
from pathlib import Path

from botsito.cli import _EntornoEvidencia
from botsito.evidence.modelo import (
    EvidenciaError,
    calcular_id,
    cargar_item,
    escribir_item,
    limpiar_campos,
    verificar_citas,
)
from botsito.evidence.verificacion import CitaError, localizar_cita, ventana_no_citable

RAIZ = Path(__file__).resolve().parents[4]
VIEJO = "ev-v10-010438-0d4e6798"
LIMITE = 1058
NOTAS = (
    "cita recortada antes del segmento 1058, que el filtro tapa por el tramo 1:04:56–1:05:29; "
    "orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó"
)
CAMBIAN = {"id", "t1", "cita_literal", "supersede", "notas"}


def hms(ms: int) -> str:
    s = ms // 1000
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}"


def main(modo: str) -> int:
    entorno = _EntornoEvidencia(RAIZ)
    contexto = entorno.contexto
    viejo = next(i for i in entorno.existentes if i.id == VIEJO)
    assert viejo.transcripcion is not None and contexto.crudas is not None
    segmentos = list(contexto.crudas(viejo.transcripcion) or [])
    limite = next(s for s in segmentos if s.n == LIMITE)
    t1_nuevo = limite.t0_ms // 1000 * 1000
    print(f"item viejo: {VIEJO} ({viejo.t0_ms}-{viejo.t1_ms} ms)")
    print(
        f"segmento {LIMITE}: {limite.t0_ms}-{limite.t1_ms} ms; fin de la ventana nueva: {t1_nuevo}"
    )
    if modo == "vieja":
        cita, t1 = viejo.cita_literal, viejo.t1
    else:
        cita = None
        palabras = viejo.cita_literal.split(" ")
        for k in range(len(palabras) - 1, 0, -1):
            candidata = " ".join(palabras[:k]).rstrip(" /,;:.")
            try:
                loc = localizar_cita(segmentos, viejo.t0_ms, t1_nuevo, candidata)
            except CitaError:
                continue
            if loc.coincidencias == 1 and max(loc.segmentos) < LIMITE:
                cita = candidata
                break
        if cita is None:
            print("PARADA: ningun prefijo de la cita cae entero antes del segmento 1058")
            return 2
        t1 = hms(t1_nuevo)
    prueba = replace(viejo, t1=t1, cita_literal=cita)
    problemas, _avisos, locs = verificar_citas([prueba], contexto)
    loc = locs.get(prueba.id)
    print(
        f"verificar_citas: {len(problemas)} problemas; apariciones "
        f"{loc.coincidencias if loc else '-'}; segmentos de la cita "
        f"{list(loc.segmentos) if loc else '-'}"
    )
    fuera = ventana_no_citable(contexto, viejo.video_id, prueba.t0_ms, prueba.t1_ms, segmentos)
    print(f"ventana_no_citable ({prueba.t0_ms}-{prueba.t1_ms} ms): {fuera or 'pasa'}")
    campos = {k: v for k, v in asdict(viejo).items() if k != "id"}
    campos["fotogramas"] = list(viejo.fotogramas)
    campos.update(t1=t1, cita_literal=cita, supersede=VIEJO, notas=NOTAS)
    try:
        ruta = escribir_item(entorno.directorio, campos, entorno.comprobar)
    except EvidenciaError as exc:
        # El id del candidato no se escribe nunca, y `knowledge validate` exige que exista todo id
        # citado en docs/: se nombra sin el. Los mensajes son de plantilla (ids, segmentos, ms).
        candidato = calcular_id(limpiar_campos(dict(campos)))
        print(
            "RECHAZADO por la comprobacion de evidence new: "
            + str(exc).replace(candidato, "<candidato sin escribir>")
        )
        return 1
    nuevo = cargar_item(ruta)
    a, b = asdict(viejo), asdict(nuevo)
    distintos = sorted(k for k in a if a[k] != b[k])
    print(
        f"ESCRITO: {nuevo.id} ({nuevo.t0_ms}-{nuevo.t1_ms} ms), {ruta.relative_to(RAIZ).as_posix()}"
    )
    print(f"campos distintos del viejo: {distintos}")
    print(f"igual campo a campo salvo {sorted(CAMBIAN)}: {set(distintos) <= CAMBIAN}")
    return 0 if set(distintos) <= CAMBIAN else 2


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("vieja", "nueva"):
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
