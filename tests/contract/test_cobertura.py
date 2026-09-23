"""La cobertura del material en el camino del kit: que el CERO signifique una sola cosa.

Lo que esta rama cierra no es "junio": es que hasta hoy un dia sin filas podia ser DOS cosas
incompatibles -«el trader miro y no opero», que es un DATO SUYO, y «este mes no tiene material»,
que es AUSENCIA DE CONOCIMIENTO- y las dos daban exactamente el mismo silencio. El dia que alguien
decida que un dia sin filas produce un `no_trade`, esa decision convertiria la segunda en la
primera sin que nadie lo viera: fabricar una etiqueta del trader donde no hay material.

Los tres agujeros, cada uno con su test:

1. junio es ingerible HOY, porque `dias_ingeribles` no leia el config;
2. junio entraria en el universo de un `kit build` NUEVO, porque la llamada del kit no pasaba
   `cobertura`. NO cae por `vistos.yaml`: el trader no vio junio, y es CORRECTO que no este ahi.
   Las dos preguntas son ortogonales -`vistos.yaml` responde ¿es ciego?, `cobertura_material`
   responde ¿hay material?- y junio es el unico mes con dataset que es ciego y esta vacio;
3. el cero significa dos cosas, y ademas `--material` puede ser el libro equivocado sin que nada
   lo diga.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.cases.ingesta import IngestaError, dias_ingeribles, ingerir
from botsito.cases.paquete import KitError, _cobertura_desde_doc
from botsito.cases.ventanas import motivo_de_cobertura

from .test_ingesta import CABECERA, SESIONES, _declarar, _repo, _xlsx

MAYO = {"2026-05": (("2026-05-01", "2026-05-31"),)}
MAYO_Y_JUNIO_VACIO: dict[str, tuple[tuple[str, str], ...]] = {**MAYO, "2026-06": ()}


@pytest.mark.contract
def test_sin_cobertura_un_mes_descartado_sigue_siendo_ingerible(tmp_path: Path) -> None:
    """EL DEFECTO, EN ROJO. Es el estado de `main` hasta esta rama.

    Sin cobertura, `dias_ingeribles` devuelve los dias de un mes que el consultor descarto, y la
    unica constancia de que se descarto vive en un ADR que ningun codigo lee.
    """
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev", "caso-eurusd-2026-06-01": "dev"})
    sin_puerta = dias_ingeribles(repo)
    assert "2026-06-01" in sin_puerta.dias, "ASI ESTABA main: junio entraba"
    assert sin_puerta.negados == {}


@pytest.mark.contract
def test_la_puerta_niega_el_mes_sin_material_y_lo_dice_por_mes(tmp_path: Path) -> None:
    """Y el grito: se CUENTA, se nombra el MES y el motivo. NUNCA los dias."""
    repo = _repo(
        tmp_path,
        {
            "caso-eurusd-2026-05-08": "dev",
            "caso-eurusd-2026-06-01": "dev",
            "caso-eurusd-2026-06-02": "dev",
        },
    )
    con_puerta = dias_ingeribles(repo, MAYO_Y_JUNIO_VACIO)
    assert set(con_puerta.dias) == {"2026-05-08"}
    assert set(con_puerta.negados) == {"2026-06"}
    cuantos, motivo = con_puerta.negados["2026-06"]
    assert cuantos == 2, "se CUENTAN, que es lo unico que delata una desaparicion"
    assert "CERO tramos" in motivo and "no hay material" in motivo
    # LA GUARDIA QUE IMPORTA: ni un solo dia en el motivo. Un dia laborable que no aparece ES su
    # etiqueta, y publicarlo seria abrir por la puerta de atras (ADR-0036, ADR-0037).
    assert "2026-06-01" not in motivo and "2026-06-02" not in motivo


@pytest.mark.contract
def test_un_mes_no_declarado_se_niega_con_otro_motivo(tmp_path: Path) -> None:
    """Un mes del que nadie ha dicho nada NO es lo mismo que uno declarado vacio."""
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev", "caso-eurusd-2026-07-01": "dev"})
    r = dias_ingeribles(repo, MAYO_Y_JUNIO_VACIO)
    assert set(r.dias) == {"2026-05-08"}
    _, motivo = r.negados["2026-07"]
    assert "no esta declarado" in motivo, "no es lo mismo que declarado con cero tramos"


@pytest.mark.contract
def test_los_dos_ceros_se_distinguen(tmp_path: Path) -> None:
    """EL CRITERIO QUE DE VERDAD PRUEBA ESTA RAMA: cada cero con su linea y su motivo.

    (a) un dia ingerible DENTRO de la cobertura en el que el trader no opero -> se cuenta aparte y
        NO es error: es un dato suyo;
    (b) un mes pedido sin NI UNA fila en el libro -> ERROR nombrando el mes, porque el libro no es
        el suyo y ese cero no se puede distinguir de (a) si se deja pasar.
    """
    repo = _repo(tmp_path, {"caso-eurusd-2026-05-08": "dev", "caso-eurusd-2026-05-12": "dev"})
    material = tmp_path / "solo-el-8.xlsx"
    _xlsx(material, [CABECERA, ["2026/05/08 07:30:00", "buy", "1.1000", "1.0990", "", ""]])
    _declarar(repo, material)

    # (a) el 12 esta cubierto y no tiene operaciones: NO es error, y se cuenta.
    r = ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08", "2026-05-12"])
    assert r.sin_operaciones == 1, "el dia sin operaciones se CUENTA"
    assert [d for d, ops in r.casos.items() if ops] == ["2026-05-08"]

    # (b) el mismo libro, pidiendole un mes del que no tiene ni una fila: ERROR con el MES.
    with pytest.raises(IngestaError) as exc:
        ingerir(repo, material, "Europe/Madrid", SESIONES, dias=["2026-05-08", "2026-06-01"])
    assert "2026-06" in str(exc.value) and "no tiene ni una fila" in str(exc.value)
    # habla del FICHERO, no de los dias del trader: no publica calendario
    assert "2026-06-01" not in str(exc.value)


@pytest.mark.contract
def test_el_esquema_admite_cero_tramos_y_sigue_rechazando_lo_demas() -> None:
    """CERO TRAMOS es un valor con significado; hasta hoy se rechazaba como si fuera un error."""
    assert _cobertura_desde_doc({"2026-06": []}, "c.yaml") == {"2026-06": ()}
    with pytest.raises(KitError, match="lista de tramos"):
        _cobertura_desde_doc({"2026-06": "nada"}, "c.yaml")
    with pytest.raises(KitError, match="lista de DIAS cubiertos no se admite"):
        _cobertura_desde_doc({"2026-06": ["2026-06-01"]}, "c.yaml")


@pytest.mark.contract
def test_el_motivo_de_cero_tramos_no_miente() -> None:
    """Decia «(2026-06 cubre )» con la lista vacia detras: una frase FALSA, en el unico sitio que
    alguien va a leer dentro de un ano. Se comprueba LA FRASE REAL, no una copia."""
    cero = motivo_de_cobertura("2026-06-01", ())
    assert "sin material del trader" in cero and "cero tramos" in cero
    assert "cubre" not in cero, "la frase vieja mentia con la lista vacia detras"
    # y la otra rama sigue diciendo lo que cubre
    acotado = motivo_de_cobertura("2026-09-25", (("2026-09-01", "2026-09-18"),))
    assert "cubre 2026-09-01..2026-09-18" in acotado
