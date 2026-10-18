"""Lo comun a los guiones de VISOR-CONSTRUCCION (R3.2): construye el motor cableado y prepara UN
dia de construccion EXACTAMENTE como `botsito motor visor --simular --caso <caso>` con las opciones
de la corrida 2 de R3.1 (`--diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope
--diagnostico-cuenta-diaria`): las mismas llamadas, en el mismo orden, que `cli.motor_visor`
(cli.py:2478-2557). No cambia ninguna decision del motor ni escribe nada; solo devuelve objetos.

Y la regla de esta rama sobre lo que se imprime (respuesta del consultor a la PARADA, punto 5):
nada anterior a las 00:00Z de la fecha del caso -ni instante, ni vela, ni precio-, aunque sea del
dia operativo; y nada en dinero. `antes_del_dia` es la puerta que usan los guiones para enmascarar.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "src"))

from botsito.cases.criterio_fidelidad import cargar_criterio  # noqa: E402
from botsito.cases.paquete import cargar_config  # noqa: E402
from botsito.config.ajustes import carpeta_datos  # noqa: E402
from botsito.config.registro import cargar_registro  # noqa: E402
from botsito.domain.ticks import MS_POR_MINUTO  # noqa: E402
from botsito.engine import cableado, diagnostico, entrada, tope_trader, visor, zonas  # noqa: E402
from botsito.engine.interprete import Interprete, reglas_ejecutables  # noqa: E402
from botsito.engine.motor import MotorSpec  # noqa: E402
from botsito.engine.primitivas import primitivas_escritas  # noqa: E402
from botsito.spec.modelo import cargar_reglas, cargar_vocabulario  # noqa: E402

# las opciones de la corrida 2 de R3.1 (anexos/MARGEN-LOTE/README.md, punto 2): argumentos de la
# linea de comandos, no parametros del registro
DIAGNOSTICO = diagnostico.Diagnostico(
    a35="cierre_vela_contraria", a44="sin_tope", cuenta_diaria=True
)
HUSO_TRADER = ZoneInfo("Europe/Madrid")  # el reloj de pared del grafico (ADR-0069)
OCULTO = "(antes del dia)"


@dataclass
class Dia:
    caso: str
    fecha: date
    motor: Any  # cableado.MotorCableado
    preparador: Any  # visor.Preparador
    pagina: Any  # visor.DiaVisor
    registro: Any
    criterio: Any

    @property
    def clave(self) -> str:
        return self.fecha.isoformat()

    @property
    def broker(self) -> Any:
        return self.motor.brokers[self.clave]

    @property
    def traza_broker(self) -> Any:
        return self.motor.trazas_broker[self.clave]

    @property
    def estado(self) -> Any:
        return self.motor.estados[self.clave]

    def inicio_utc_ms(self) -> int:
        return int(
            datetime(self.fecha.year, self.fecha.month, self.fecha.day, tzinfo=UTC).timestamp()
            * 1000
        )

    def antes_del_dia(self, minuto: int) -> bool:
        """Si un minuto UTC es anterior a las 00:00Z de la fecha del caso (punto 5)."""
        return minuto * MS_POR_MINUTO < self.inicio_utc_ms()


def construir(caso: str, antes_de_correr: Any = None) -> Dia:
    """El motor cableado y el dia preparado, como `motor visor --simular --caso`. Si se da
    `antes_de_correr(motor)`, se llama antes de correr el dia (para instalar los lectores)."""
    repo = RAIZ
    criterio = cargar_criterio(repo)
    registro = cargar_registro(repo / "knowledge" / "spec" / "parametros.yaml")
    config = cargar_config(repo / "knowledge" / "cases" / "kit" / "config.yaml")
    spec = repo / "knowledge" / "spec" / "strategy_spec.yaml"
    vocabulario = cargar_vocabulario(spec)
    reglas = reglas_ejecutables(cargar_reglas(spec))
    dt = visor.caso_de_construccion(repo, criterio, caso)
    diag = DIAGNOSTICO
    lectura = diagnostico.lectura_pivote(registro, diag)
    perfil = cableado.perfil_del_repo(repo, None)
    tope = tope_trader.tope_del_registro(registro, perfil.huso_corte(), diag)
    limpia = zonas.lectura_limpia(registro)
    tipo_orden = entrada.lectura_tipo_orden(registro, diag.a47)
    datos = carpeta_datos(repo)
    preparador = visor.Preparador(
        repo,
        datos,
        criterio,
        registro,
        config,
        vocabulario,
        MotorSpec(Interprete(vocabulario, primitivas_escritas(registro, tope, limpia)), reglas),
    )
    preparador.lectura_pivote = lectura
    motor = cableado.construir_motor_cableado(
        repo,
        datos,
        criterio,
        config,
        registro,
        vocabulario,
        reglas,
        (dt,),
        perfil,
        None,
        False,
        tope,
        limpia,
        stops_level_diagnostico=diag.a27,
        tipo_orden=tipo_orden,
    )
    preparador.motor = motor
    preparador.nombre_motor = cableado.NOMBRE_MOTOR
    preparador.detalle_broker = lambda d: cableado.detalle_para_visor(motor, d)
    if antes_de_correr is not None:
        antes_de_correr(motor)
    pagina = preparador.preparar(dt)
    return Dia(dt.id, date.fromisoformat(dt.dia), motor, preparador, pagina, registro, criterio)


def hora(minuto_o_ms: int, es_ms: bool = False) -> str:
    """«HH:MM:SSZ (HH:MM:SS del trader)» de un instante del dia."""
    ms = minuto_o_ms if es_ms else minuto_o_ms * MS_POR_MINUTO
    t = datetime.fromtimestamp(ms / 1000, UTC)
    local = t.astimezone(HUSO_TRADER)
    return f"{t:%H:%M:%S}Z ({local:%H:%M:%S} del trader)"


def lineas_ordenes_de_main(caso_fecha: str) -> list[list[str]]:
    """Las filas de «### Ordenes» del dia en la salida de main (anexos/MARGEN-LOTE, corrida 2)."""
    ruta = (
        RAIZ
        / "docs/validation/anexos/MARGEN-LOTE"
        / "diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt"
    )
    filas: list[list[str]] = []
    dentro = False
    for ln in ruta.read_text(encoding="utf-8").splitlines():
        c = ln.split("] ", 1)[-1] if ln.startswith("[") else ln
        if c.startswith("### Ordenes ("):
            dentro = True
            continue
        if dentro and c.startswith("### "):
            break
        if dentro and c.startswith(f"{caso_fecha} | "):
            filas.append(c.split(" | "))
    return filas


def ordenes_coinciden(d: Dia) -> tuple[bool, list[str]]:
    """Compara las ordenes del dia corrido aqui con las de main: dia, sesion, id, colocada, precio,
    resultado y motivo (las siete primeras columnas, sin las de dinero)."""
    propias = [
        [str(x) if not hasattr(x, "isoformat") else x.isoformat() for x in f[:7]]
        for f in cableado.vida_de_las_ordenes(d.motor)
    ]
    de_main = [f[:7] for f in lineas_ordenes_de_main(d.clave)]
    diferencias = []
    for i in range(max(len(propias), len(de_main))):
        a = propias[i] if i < len(propias) else None
        b = de_main[i] if i < len(de_main) else None
        if a != b:
            diferencias.append(f"fila {i + 1}: aqui {a} | main {b}")
    return not diferencias, diferencias
