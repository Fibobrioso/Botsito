"""Todo parametro PROVISIONAL cuelga de una ambiguedad ABIERTA (decision del consultor del
2026-10-02, `feature/escenarios-por-sesion`, cuarta orden).

PROVISIONAL es el estado `DEFAULT_AMBIGUOUS` del registro (ADR-0002): un valor por defecto que se
lee anotando su ambiguedad mientras el trader no conteste. Si esa ambiguedad ya esta RESUELTA o
DECIDIDA, o no existe, el valor se queda PROVISIONAL sin pregunta abierta que lo vaya a fijar, y
nadie lo vuelve a mirar. El test recorre el registro entero: nombra la condicion, no un caso."""

from __future__ import annotations

from pathlib import Path

from botsito.cases.ambiguedades import Ambiguedad, cargar_ambiguedades
from botsito.config.registro import Estado, Registro, cargar_registro

RAIZ = Path(__file__).resolve().parents[2]


def provisionales_sin_ambiguedad_abierta(
    registro: Registro, ambiguedades: list[Ambiguedad]
) -> list[str]:
    """Los parametros DEFAULT_AMBIGUOUS cuya `ambiguedad_id` no es una ABIERTA del YAML."""
    estado = {a.id: a.estado for a in ambiguedades}
    return [
        f"{p.nombre} -> {p.ambiguedad_id} ({estado.get(str(p.ambiguedad_id), 'no existe')})"
        for p in sorted(registro.parametros.values(), key=lambda p: p.nombre)
        if p.estado is Estado.DEFAULT_AMBIGUOUS and estado.get(str(p.ambiguedad_id)) != "ABIERTA"
    ]


def test_todo_parametro_provisional_cuelga_de_una_ambiguedad_abierta() -> None:
    registro = cargar_registro(RAIZ / "knowledge" / "spec" / "parametros.yaml")
    ambiguedades = cargar_ambiguedades(RAIZ / "knowledge" / "spec" / "ambiguedades.yaml")
    assert provisionales_sin_ambiguedad_abierta(registro, ambiguedades) == []
