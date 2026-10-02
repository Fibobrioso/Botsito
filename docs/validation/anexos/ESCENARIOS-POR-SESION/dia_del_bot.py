"""Que hace el bot en un dia de construccion, sesion a sesion: ordenes, llenados, cierres y
escenarios. Monta el motor cableado como `botsito motor visor --simular` con las mismas lecturas
de diagnostico (A-35 cierre_vela_contraria, A-44 sin_tope, A-21 solo_una_zona_de_control, A-27 0)
y corre en el arbol desde el que se lanza (la rama o el worktree de main). Por la compuerta del
arnes: un caso oculto se niega antes de leerlo. Imprime por dia, nunca agregados.

Anexo de `docs/validation/ESCENARIOS-POR-SESION.md` §3.2.

    «ahora»: desde la raiz de la rama
        uv run python docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py caso-eurusd-2026-08-03
    «antes»: desde un worktree desechable de main (`git worktree add --detach <dir> a093ffb`) con
    un `config/settings.local.toml` cuyo `[rutas].data` apunta a la carpeta data/ de la maquina,
    el mismo comando con la ruta de este fichero."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.cases.paquete import cargar_config
from botsito.cli import _carpeta_datos
from botsito.config.registro import cargar_registro
from botsito.engine import cableado, diagnostico, entrada, tope_trader, visor, zonas
from botsito.engine.diagnostico import Diagnostico
from botsito.engine.interprete import Interprete, reglas_ejecutables
from botsito.engine.motor import MotorSpec
from botsito.engine.primitivas import primitivas_escritas
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario

MADRID = ZoneInfo("Europe/Madrid")


def hora(ms: int | None) -> str:
    if ms is None:
        return "-"
    return datetime.fromtimestamp((ms + 1) / 1000, UTC).astimezone(MADRID).strftime("%H:%M:%S")


def main() -> int:
    repo = Path.cwd()
    caso_id = sys.argv[1]
    criterio = cargar_criterio(repo)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    vocabulario = cargar_vocabulario(spec)
    reglas = reglas_ejecutables(cargar_reglas(spec))
    caso = visor.caso_de_construccion(repo, criterio, caso_id)
    diag = Diagnostico(
        "cierre_vela_contraria", "sin_tope", "solo_una_zona_de_control", 0, None, False
    )
    lectura = diagnostico.lectura_pivote(registro, diag)
    perfil = cableado.perfil_del_repo(repo, None)
    tope = tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag)
    limpia = zonas.lectura_limpia(registro, diag.a21)
    tipo_orden = entrada.lectura_tipo_orden(registro, diag.a47)
    motor = MotorSpec(Interprete(vocabulario, primitivas_escritas(registro, tope, limpia)), reglas)
    prep = visor.Preparador(
        repo, _carpeta_datos(repo), criterio, registro, config, vocabulario, motor
    )
    prep.lectura_pivote = lectura
    cab = cableado.construir_motor_cableado(
        repo, _carpeta_datos(repo), criterio, config, registro, vocabulario, reglas, (caso,),
        perfil, None, False, tope, limpia, stops_level_diagnostico=diag.a27, tipo_orden=tipo_orden,
    )  # fmt: skip
    prep.motor = cab
    prep.nombre_motor = cableado.NOMBRE_MOTOR
    prep.detalle_broker = lambda dia: cableado.detalle_para_visor(cab, dia)
    prep.preparar(caso)
    dia = caso.dia
    broker = cab.brokers[dia]
    print(f"== {caso_id}")
    for o in sorted(broker.ordenes.values(), key=lambda x: x.colocada_ms):
        print(
            f"  orden {o.id}: colocada {hora(o.colocada_ms)} precio {o.precio} -> {o.estado} "
            f"({hora(o.ultimo_cambio_ms)})"
        )
    for p in sorted(broker.posiciones.values(), key=lambda x: x.abierta_ms):
        print(
            f"  posicion de {p.orden_id}: {p.lado} llenada {hora(p.abierta_ms)} a {p.entrada}, "
            f"cierra {hora(p.cerrada_ms)} por {p.motivo_cierre} a {p.precio_cierre}"
        )
    estado = cab.estados[dia]
    if hasattr(zonas, "ESCENARIOS"):
        for sesion in ("07-11", "11-15"):
            for e in zonas.memoria_de_sesion(estado, sesion).get(zonas.ESCENARIOS, []):
                print(
                    f"  {sesion} escenario {e['n']}: toma {hora(e['toma']['instante'] * 60000 - 1)}"
                    f" nivel {e['toma']['nivel']}, zonas {sorted(e['zonas'])}, "
                    f"terminado {e['terminado']}"
                )
    else:
        for sesion in ("07-11", "11-15"):
            toma = zonas.memoria_de_sesion(estado, sesion).get("toma")
            if toma:
                print(
                    f"  {sesion} toma (unica): {hora(toma['instante'] * 60000 - 1)} nivel {toma['nivel']}"
                )
    print(
        "  hechos al final:", {k: v for k, v in estado.hechos.items() if k.startswith("detenido")}
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
