"""Monta test_volcado_informe.py AUTOCONTENIDO: las lineas 1-225 de tests/unit/test_cableado.py
(imports y ayudantes, copiados literalmente), sin la linea que importa tests.unit, y el volcado.
Uso: python montar_volcado.py <test_cableado.py> <salida>"""

import sys
from pathlib import Path

origen = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[:225]
cuerpo = [x for x in origen if not x.startswith("from tests.unit.")]
cola = """

# ------------------------------------------------- volcado para comparar-con-main (no se commitea)
RUTAS_VOLCADO = {"stop": RUTA_STOP, "hueco": RUTA_HUECO, "viva": RUTA_VIVA}


@pytest.mark.parametrize("nombre", sorted(RUTAS_VOLCADO))
def test_volcar(registro: Registro, vocabulario: dict[str, dict[str, Any]], nombre: str) -> None:
    motor = _motor(registro, vocabulario, _mercado(RUTAS_VOLCADO[nombre]))
    motor.correr_dia(_dia())
    (RAIZ / f"volcado-{nombre}.txt").write_text(
        cableado.informe_simulacion(motor), encoding="utf-8", newline="\\n"
    )
"""
Path(sys.argv[2]).write_text("\n".join(cuerpo) + cola, encoding="utf-8", newline="\n")
print(len(cuerpo), "lineas copiadas")
