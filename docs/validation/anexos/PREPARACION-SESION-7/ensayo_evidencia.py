"""0.5 de trabajo/preparacion-sesion-7: ensayo SIN ESCRIBIR de los items de F7 #1, #2, #3, #6 y
#10. Hace lo mismo que `evidence new` antes de escribir (cli.evidence_new: limpiar, validar,
calcular el id y `_EntornoEvidencia.comprobar`, que localiza la cita en la transcripcion por las
funciones de verificacion) y se para ahi: no llama a `escribir_item`.

Uso (desde la raiz del repo): uv run python ensayo_evidencia.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from botsito.cli import _EntornoEvidencia
from botsito.evidence.modelo import _validar_campos, calcular_id, item_desde_dict, limpiar_campos

REPO = Path(".")
V14_VIEJA = "tr-v14-large-v3-int8-float16-2253ec10"

ITEMS = {
    "#1": dict(video_id="v11", t0="0:00:38", t1="0:00:53", tema="sesgo.h4.rango", valor=None,
               cita="A ver, este es nuestro rango Por lo general, como no ha sido mitigado Ni por "
                    "debajo por una vela bajista Ni por arriba por una vela alcista Para actualizar "
                    "el rango Entonces nosotros nos enfocamos en buscar Traits alcistas",
               transcripcion=None),
    "#2": dict(video_id="v11", t0="0:05:50", t1="0:06:00", tema="sesgo.h4.rango", valor="mecha",
               cita="Si en caso esta vela roja hubiera roto con mecha o con cuerpo por debajo de "
                    "esta vela, hubiéramos trazado nuestro rango bajista y esta operativa sería "
                    "bajista", transcripcion=None),
    "#3": dict(video_id="v12", t0="0:06:50", t1="0:07:07", tema="sesgo.h4.importancia", valor=None,
               cita="es que es muy pero muy pero muy importante y es lo principal yo diría que un "
                    "70% o sea que uno defina bien el rango el el bias", transcripcion=None),
    "#6": dict(video_id="v12", t0="0:00:15", t1="0:00:58", tema="entrada.breaker_m1_con_cuerpo",
               valor="cuerpo",
               cita="aquí no había entrada porque es con mecha, sabemos que tiene que ser con "
                    "cuerpo [...] aquí sí que tenemos una entrada vale porque nos genera un breaker "
                    "con cuerpo", transcripcion=None),
    "#10": dict(video_id="v14", t0="0:42:02", t1="0:42:40", tema="backtest.entradas_sin_tomar",
                valor=None,
                cita="aquí hay una entrada que no le voy a tomar para no afectar al mostreo",
                transcripcion=V14_VIEJA),
    "#10 activa": dict(video_id="v14", t0="0:44:04", t1="0:44:11", tema="backtest.entradas_sin_tomar",
                       valor=None,
                       cita="aquí hay una entrada que no le voy a tomar para no afectar al mostreo",
                       transcripcion=None),
    "#10 vieja ventana buena": dict(video_id="v14", t0="0:44:04", t1="0:44:11",
                                    tema="backtest.entradas_sin_tomar", valor=None,
                                    cita="aquí hay una entrada que no le voy a tomar para no afectar al mostreo",
                                    transcripcion=V14_VIEJA),
}  # fmt: skip


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    entorno = _EntornoEvidencia(REPO)
    print(f"activas: v11 {entorno.contexto.activas.get('v11')}, v12 "
          f"{entorno.contexto.activas.get('v12')}, v14 {entorno.contexto.activas.get('v14')}")
    for clave, it in ITEMS.items():
        transcripcion = it["transcripcion"] or entorno.contexto.activas.get(it["video_id"])
        campos = {
            "video_id": it["video_id"], "t0": it["t0"], "t1": it["t1"], "modalidad": "audio",
            "tipo": "RULE_STATEMENT", "cita_literal": it["cita"], "afirmacion": "ensayo",
            "tema": it["tema"], "valor": it["valor"], "confianza": "media", "extractor": "llm",
            "revisado_por": "ensayo", "provenance": "botsito", "fotogramas": [],
            "supersede": None, "notas": None, "transcripcion": transcripcion,
        }  # fmt: skip
        campos = limpiar_campos(campos)
        try:
            _validar_campos(campos, "nuevo")
            campos["id"] = calcular_id(campos)
            item = item_desde_dict(campos, "nuevo")
            problemas = entorno.comprobar(item)
        except Exception as exc:  # noqa: BLE001 - ensayo: se imprime y se sigue
            print(f"{clave}: ERROR al validar: {exc}")
            continue
        # sin el id calculado delante: el item no existe, y docs/** no puede nombrarlo
        sin_id = [p.removeprefix(f"{item.id}: ") for p in problemas]
        estado = "ACEPTADA" if not sin_id else "RECHAZADA: " + "; ".join(sin_id)
        print(f"{clave}: {it['video_id']} {it['t0']}-{it['t1']} ({transcripcion}): {estado}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
