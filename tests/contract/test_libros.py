"""ADR-0039: ningun libro se lee sin su formato y su huso declarados, atados a su sha.

Nacio el 2026-09-22 en `trabajo/mayo-dev-ingerido`: el libro de mayo viene entero en
`AAAA-MM-DD HH:MM:SS` y el lector daba por hecho el formato de agosto. Aqui se prueba que el lector
acepta EXACTAMENTE lo declarado para cada libro, que el registro es SOLO ANADIR contra el historial,
y que se cruza con `cobertura_material`.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from botsito.corpus.libro import LibroError, filas_de_los_dias
from botsito.corpus.libros import (
    FICHERO_LIBROS,
    LibrosError,
    cargar_libros,
    declaracion_de,
    problemas_de_libros,
    sha256_de,
)

from .test_ingesta import COLS, _decl, _declarar, _xlsx

REAL = Path(__file__).resolve().parents[2]
NUEVO = "AAAA-MM-DD HH:MM:SS"
CAB = ["dateStart", "side", "entryPrice", "initialSL"]


def _leer(libro: Path, formato: str) -> list[dict[str, str | None]]:
    return filas_de_los_dias(
        libro,
        {"2026-05-08"},
        "backtesting-analytics",
        COLS,
        _decl(libro, formato),
        huso_de_los_dias="Europe/Madrid",
    )


@pytest.mark.contract
@pytest.mark.parametrize(
    ("formato", "fecha"),
    [("AAAA/MM/DD HH:MM:SS", "2026/05/08 07:30:00"), (NUEVO, "2026-05-08 07:30:00")],
)
def test_cada_formato_se_lee_con_su_declaracion(tmp_path: Path, formato: str, fecha: str) -> None:
    libro = tmp_path / "l.xlsx"
    _xlsx(libro, [CAB, [fecha, "buy", "1.1", "1.0"]])
    filas = _leer(libro, formato)
    assert [f["_instante_utc"] for f in filas] == ["2026-05-08T07:30:00+00:00"]


@pytest.mark.contract
def test_un_libro_en_un_formato_distinto_del_declarado_falla(tmp_path: Path) -> None:
    """Nunca «probar formatos hasta que uno parsee»: el de mayo declarado como el de agosto no se
    lee, aunque el vocabulario conozca los dos."""
    libro = tmp_path / "l.xlsx"
    _xlsx(libro, [CAB, ["2026-05-08 07:30:00", "buy", "1.1", "1.0"]])
    with pytest.raises(LibroError, match="no casa con ningun formato declarado") as exc:
        _leer(libro, "AAAA/MM/DD HH:MM:SS")
    assert "2026-05-08" not in str(exc.value), "el error no publica el valor"


@pytest.mark.contract
def test_un_dia_mes_ambiguo_no_se_lee_con_ninguna_declaracion(tmp_path: Path) -> None:
    """El vocabulario no tiene DD/MM ni MM/DD (el orden no se ha demostrado en ningun libro): un
    `08/05/2026` no se lee ni como 8 de mayo ni como 5 de agosto."""
    libro = tmp_path / "l.xlsx"
    _xlsx(libro, [CAB, ["08/05/2026 07:30:00", "buy", "1.1", "1.0"]])
    for formato in ("AAAA/MM/DD HH:MM:SS", NUEVO):
        with pytest.raises(LibroError, match="no casa"):
            _leer(libro, formato)


@pytest.mark.contract
def test_sin_declaracion_no_se_lee_y_con_una_ajena_tampoco(tmp_path: Path) -> None:
    repo = tmp_path
    libro = tmp_path / "l.xlsx"
    _xlsx(libro, [CAB, ["2026/05/08 07:30:00", "buy", "1.1", "1.0"]])
    otro = tmp_path / "o.xlsx"
    _xlsx(otro, [CAB, ["2026/05/08 08:30:00", "buy", "1.1", "1.0"]])
    _declarar(repo, otro)
    with pytest.raises(LibrosError, match="no esta declarado"):
        declaracion_de(repo, libro)
    with pytest.raises(LibroError, match="declaracion ajena"):
        filas_de_los_dias(
            libro,
            {"2026-05-08"},
            "backtesting-analytics",
            COLS,
            declaracion_de(repo, otro),
            huso_de_los_dias="Europe/Madrid",
        )


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def _repo_con_registro(tmp_path: Path) -> tuple[Path, Path, Path]:
    repo = tmp_path / "repo"
    repo.mkdir()
    a, b = tmp_path / "a.xlsx", tmp_path / "b.xlsx"
    _xlsx(a, [CAB, ["2026/05/08 07:30:00", "buy", "1.1", "1.0"]])
    _xlsx(b, [CAB, ["2026/05/08 08:30:00", "buy", "1.1", "1.0"]])
    _declarar(repo, a)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "a declarado")
    return repo, a, b


@pytest.mark.contract
def test_solo_anadir_una_entrada_nueva_pasa(tmp_path: Path) -> None:
    repo, a, b = _repo_con_registro(tmp_path)
    _declarar(repo, b)
    _git(repo, "commit", "-qam", "b declarado")
    assert problemas_de_libros(repo, {sha256_de(a), sha256_de(b)}) == []


@pytest.mark.contract
def test_solo_anadir_un_commit_que_modifica_una_entrada_falla(tmp_path: Path) -> None:
    """El sha fija los bytes: el formato y el huso de un libro no cambian nunca."""
    repo, a, _ = _repo_con_registro(tmp_path)
    ruta = repo / FICHERO_LIBROS
    doc = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    doc["libros"][sha256_de(a)]["lecturas"][0]["huso"] = "Europe/Madrid"
    ruta.write_text(yaml.safe_dump(doc), encoding="utf-8")
    _git(repo, "commit", "-qam", "cambio el huso de a")
    problemas = problemas_de_libros(repo, set())
    assert any("modifica la declaracion" in p for p in problemas), problemas


@pytest.mark.contract
def test_solo_anadir_borrar_una_entrada_falla_aunque_no_se_commitee(tmp_path: Path) -> None:
    repo, a, b = _repo_con_registro(tmp_path)
    (repo / FICHERO_LIBROS).write_text("libros: {}\n", encoding="utf-8")
    problemas = problemas_de_libros(repo, set())
    assert any("borra la declaracion" in p and "arbol de trabajo" in p for p in problemas)


@pytest.mark.contract
def test_cobertura_y_libros_se_cruzan(tmp_path: Path) -> None:
    """Todo `material_sha256` de `cobertura_material` tiene que estar en `libros.yaml`: dos
    registros con la misma llave y nada que los compare es como empieza una deriva."""
    repo, a, b = _repo_con_registro(tmp_path)
    problemas = problemas_de_libros(repo, {sha256_de(a), sha256_de(b)})
    assert len(problemas) == 1 and sha256_de(b)[:12] in problemas[0]


@pytest.mark.contract
def test_el_registro_real_declara_mayo_agosto_y_abril_y_nada_mas() -> None:
    """Enero y septiembre fuera, y es lo correcto: nadie ha medido como se leen (ADR-0039)."""
    libros = cargar_libros(REAL)
    manifiesto = yaml.safe_load(
        (REAL / "knowledge/corpus/manifest.yaml").read_text(encoding="utf-8")
    )
    por_sha = {f["sha256"]: f["ruta"] for f in manifiesto["ficheros"]}
    meses = sorted(por_sha[s].rsplit(" ", 2)[-2] for s in libros)
    assert meses == ["ABRIL", "AGOSTO", "MAYO"]
    formatos = {por_sha[s].rsplit(" ", 2)[-2]: d.lecturas for s, d in libros.items()}
    assert [(le.formato, le.huso) for le in formatos["MAYO"]] == [(NUEVO, "UTC")]


@pytest.mark.contract
def test_un_xml_roto_no_publica_su_posicion_en_la_hoja(tmp_path: Path) -> None:
    """Medido el 2026-09-22 antes de leer mayo: el `ParseError` del XML traia «line 1, column
    4913», una posicion en la hoja ENTERA que crece con las filas de antes, reservadas incluidas."""
    import zipfile

    ns = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    fila = '<row r="{n}"><c r="A{n}" t="inlineStr"><is><t>2026/05/07 08:00:00</t></is></c></row>'
    libro = tmp_path / "roto.xlsx"
    with zipfile.ZipFile(libro, "w") as z:
        z.writestr(
            "xl/workbook.xml",
            f'<workbook xmlns="{ns}"><sheets>'
            '<sheet name="backtesting-analytics"/></sheets></workbook>',
        )
        z.writestr(
            "xl/worksheets/sheet1.xml",
            f'<worksheet xmlns="{ns}"><sheetData>'
            + "".join(fila.format(n=n) for n in range(2, 60))
            + "<row><c &&& </row></sheetData></worksheet>",
        )
    with pytest.raises(LibroError) as exc:
        _leer(libro, "AAAA/MM/DD HH:MM:SS")
    msg = str(exc.value)
    assert "XML mal formado" in msg
    assert "column" not in msg and "line" not in msg
    assert exc.value.__cause__ is None and exc.value.__suppress_context__
