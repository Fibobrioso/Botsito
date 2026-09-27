"""Las rutas que generan el arnes y el visor caben en Windows (259 caracteres), y si no caben se
dice ANTES de correr. Medido el 2026-09-26: tres corridas de 9 minutos fallaron al escribir."""

from __future__ import annotations

from pathlib import Path

import pytest

from botsito.cases.criterio_fidelidad import cargar_criterio
from botsito.domain.estructura_m1 import LECTURAS_LIMPIA
from botsito.domain.pivotes_m15 import LECTURAS as LECTURAS_FORMADO
from botsito.engine import visor
from botsito.engine.diagnostico import (
    A44_MARCADOR_CERO,
    LIMITE_RUTA_WINDOWS,
    Diagnostico,
    RutaDemasiadoLargaError,
    comprobar_ruta,
    nombre_etiquetado,
)

RAIZ = Path(__file__).resolve().parents[2]


def _mas_largas() -> Diagnostico:
    return Diagnostico(
        a35=max(LECTURAS_FORMADO, key=len),
        a44=A44_MARCADOR_CERO,
        a21=max(LECTURAS_LIMPIA, key=len),
    )


def test_el_nombre_lleva_la_forma_compacta_y_sigue_siendo_inconfundible() -> None:
    d = Diagnostico(a35="inicio_vela_contraria", a44="sin_tope")
    assert nombre_etiquetado(Path("a/informe.txt"), d.etiquetas) == Path(
        "a/informe.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.txt"
    )
    assert nombre_etiquetado(Path("a/informe.txt"), ()) == Path("a/informe.txt")
    nombre = nombre_etiquetado(Path("x.html"), _mas_largas().etiquetas).name
    assert nombre.startswith("x.DIAGNOSTICO.") and nombre.endswith(".html")
    for valor in (_mas_largas().a35, _mas_largas().a44, _mas_largas().a21):
        assert str(valor) in nombre  # el valor de cada ambiguedad sigue legible en el nombre
    with pytest.raises(ValueError, match="forma esperada"):
        nombre_etiquetado(Path("x.txt"), ("OTRA-COSA",))


def test_comprobar_ruta_deja_pasar_lo_que_cabe_y_para_lo_que_no(tmp_path: Path) -> None:
    corta = tmp_path / "informe.txt"
    assert comprobar_ruta(corta) is corta
    larga = tmp_path / ("x" * (LIMITE_RUTA_WINDOWS + 1 - len(str(tmp_path)) - 1)) / "i.txt"
    assert len(str(larga)) > LIMITE_RUTA_WINDOWS
    with pytest.raises(RutaDemasiadoLargaError, match=str(LIMITE_RUTA_WINDOWS)):
        comprobar_ruta(larga)


def test_las_rutas_por_defecto_con_el_rotulo_mas_largo_caben_en_este_repo() -> None:
    """La carpeta por defecto del visor y el caso mas largo de construccion, con las tres
    etiquetas mas largas: si esto deja de caber, falla aqui y no tras nueve minutos de arnes."""
    etiquetas = _mas_largas().etiquetas
    criterio = cargar_criterio(RAIZ)
    casos = sorted(
        p.stem
        for p in (RAIZ / "knowledge" / "cases" / "dev").glob("*.yaml")
        if p.stem[-7:] in criterio.construccion or p.stem[-10:-3] in criterio.construccion
    )
    caso = max(casos, key=len) if casos else "caso-eurusd-2026-04-01"
    for nombre in (f"{caso}.hasta-0000.html", f"{caso}.html", visor.INDICE, "arnes.txt"):
        ruta = nombre_etiquetado(RAIZ / visor.CARPETA_SALIDA / nombre, etiquetas)
        assert len(str(ruta)) <= LIMITE_RUTA_WINDOWS, ruta


def test_la_cli_se_niega_ante_una_ruta_larga_antes_de_leer_nada(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from botsito import cli

    real = cargar_criterio(RAIZ)
    d = _mas_largas()
    diag = [
        "--diagnostico-a35", str(d.a35), "--diagnostico-a44", str(d.a44), "--diagnostico-a21",
        str(d.a21),
    ]  # fmt: skip
    carpeta = tmp_path / ("c" * max(1, LIMITE_RUTA_WINDOWS - len(str(tmp_path)) - 40))
    codigo = cli.main(
        ["--repo", str(RAIZ), "motor", "arnes", "--meses", real.construccion[0], "--salida",
         str(carpeta / "informe.txt"), *diag]
    )  # fmt: skip
    err = capsys.readouterr().err
    assert codigo == 2 and str(LIMITE_RUTA_WINDOWS) in err and "--salida" in err
    assert not carpeta.exists()
    casos = sorted((RAIZ / "knowledge" / "cases" / "dev").glob(f"*{real.construccion[0]}*.yaml"))
    if casos:
        codigo = cli.main(
            ["--repo", str(RAIZ), "motor", "visor", "--caso", casos[0].stem, "--salida",
             str(carpeta), *diag]
        )  # fmt: skip
        err = capsys.readouterr().err
        assert codigo == 2 and str(LIMITE_RUTA_WINDOWS) in err
        assert not carpeta.exists()
