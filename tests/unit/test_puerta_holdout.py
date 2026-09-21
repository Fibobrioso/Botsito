"""La puerta del holdout se niega, y se ve negar (ADR-0021 §3, ADR-0033).

Todo lo que abre de verdad se prueba en repositorios temporales. El `PREREGISTRO.md` del proyecto
sigue vacio a proposito, y este fichero comprueba que, tal como esta, la puerta no deja pasar nada.
"""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path

import pytest

from botsito.cases.holdout import (
    FICHERO_PREREGISTRO,
    MARCA_SIN_RELLENAR,
    PARTICIONES_RESERVADAS,
    RESERVADAS,
    HoldoutCerradoError,
    RepartoIlegibleError,
    abrir,
    casos_reservados,
    gastar_pregunta,
    leer_fichero,
    motivos_de_cierre,
    repartos_commiteables,
)
from botsito.comun.yaml_estricto import leer_yaml

REPO = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("particion", RESERVADAS)
def test_con_el_preregistro_de_hoy_la_puerta_se_niega_y_nombra_adr_0021(particion: str) -> None:
    assert MARCA_SIN_RELLENAR in (REPO / FICHERO_PREREGISTRO).read_text(encoding="utf-8")
    with pytest.raises(HoldoutCerradoError, match="ADR-0021 §3") as exc:
        abrir(REPO, particion, "P1")
    assert "sigue vacio" in str(exc.value)
    assert f"AUTORIZACION-{particion}.md" in str(exc.value)


def test_leer_material_del_holdout_real_pasa_por_la_puerta_y_se_niega() -> None:
    # la ruta no existe, y da igual: la puerta decide antes de abrir nada
    with pytest.raises(HoldoutCerradoError, match="holdout-2"):
        leer_fichero(REPO, "knowledge/cases/holdout/2/caso-xxxyyy-2026-05-07.yaml")
    # el README es libre
    assert leer_fichero(REPO, "knowledge/cases/holdout/1/README.md")
    with pytest.raises(ValueError, match="no esta en"):
        leer_fichero(REPO, "knowledge/cases/kit/config.yaml")


def test_los_casos_reservados_salen_de_la_asignacion_sin_abrir_nada() -> None:
    """Leer `particiones.yaml` no es abrir: es lo que dice que no se puede leer.

    La afirmacion es LA UNION EXACTA de todos los repartos commiteados, de los dos caminos, y no
    una cifra pegada. Hasta el 2026-09-21 esto decia `== dict.fromkeys(PARTICIONES_RESERVADAS, 8)`
    y se habria roto con el primer reparto nuevo; relajarlo a `>= 8` habria perdido la unica
    afirmacion mecanica que existe sobre el reparto. Esta version no se rompe al anadir un camino
    y ademas caza lo que la otra no veia: que un camino nuevo quede FUERA del glob de la puerta,
    que es material reservado invisible (ADR-0036).
    """
    reservados = casos_reservados(REPO)
    esperado: dict[str, str] = {}
    for fichero in repartos_commiteables(REPO):
        doc = leer_yaml(fichero)
        for caso, particion in (doc.get("asignacion") or {}).items():
            if particion in RESERVADAS:
                esperado[str(caso)] = str(particion)
    assert reservados == esperado, "la puerta no ve todos los repartos, o ve de mas"
    assert esperado, "sin un solo reparto, esta prueba no afirma nada"
    # LA AFIRMACION SOBRE EL GLOB, y esta vez de verdad. Hasta el 2026-09-21 aqui habia un par
    # `{"kit", "fidelidad"}` pegado a mano, y el docstring decia que cazaba "un camino nuevo que
    # quede FUERA del glob". Era FALSO y esta medido: con un tercer camino
    # `knowledge/cases/marzo/eurusd-2026-03/particiones.yaml` con un `holdout-2` dentro, los DOS
    # lados de la igualdad de arriba usan `repartos_commiteables`, asi que el caso es invisible
    # para ambos y la igualdad se cumple igual. La enumeracion de abajo NO pasa por el glob: sale
    # del disco, y por eso si se rompe.
    cases = REPO / "knowledge" / "cases"
    del_disco = {
        f.parent.parent.relative_to(cases).as_posix() for f in cases.glob("*/*/particiones.yaml")
    }
    del_glob = {f.parent.parent.name for f in repartos_commiteables(REPO)}
    assert del_disco == del_glob, (
        f"hay repartos en el disco que la puerta no globea: {sorted(del_disco - del_glob)}. "
        f"Casos reservados invisibles para la puerta"
    )
    # Y el reparto concreto de la sesion 1, que sigue siendo el de ADR-0025: 8 por reservada.
    sesion_1 = leer_yaml(
        REPO / "knowledge" / "cases" / "kit" / "2026-09-09-sesion-01" / "particiones.yaml"
    )
    suyos = [p for p in sesion_1["asignacion"].values() if p in PARTICIONES_RESERVADAS]
    assert {p: suyos.count(p) for p in PARTICIONES_RESERVADAS} == dict.fromkeys(
        PARTICIONES_RESERVADAS, 8
    )
    assert "caso-eurusd-2026-05-14" in reservados  # el dia quemado sigue asignado a holdout-2


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@t", *args],
        check=True,
        capture_output=True,
    )


def _repo(tmp_path: Path, preregistro: str, autorizacion: str | None) -> Path:
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / "docs" / "adr").mkdir(parents=True)
    (tmp_path / "docs" / "adr" / "0099-apertura.md").write_text("# 99\n", encoding="utf-8")
    (tmp_path / FICHERO_PREREGISTRO).write_text(preregistro, encoding="utf-8")
    if autorizacion is not None:
        (tmp_path / "docs" / "validation" / "AUTORIZACION-holdout-2.md").write_text(
            autorizacion, encoding="utf-8"
        )
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-q", "-m", "x")
    return tmp_path


def blob_de(texto: str) -> str:
    """El sha que git da al blob de este contenido (`git hash-object`)."""
    datos = texto.encode("utf-8")
    return hashlib.sha1(b"blob %d\x00" % len(datos) + datos).hexdigest()  # noqa: S324


# El umbral y la pregunta van con numeros DISTINTOS a proposito: hay un test que hace
# `RELLENO.replace("0.8", "0.6")` y si la linea de la pregunta llevara 0.8 cambiaria dos sitios.
RELLENO = (
    "# PREREGISTRO\n\numbral: 0.8\n\n## Preguntas\n\n"
    "- pregunta: P1 | estado: ABIERTA | fidelidad de F26 sobre la particion\n"
)
BUENA = (
    "particion: holdout-2\nautorizado_por: el usuario\nfecha: 2026-10-01\nadr: ADR-0099\n"
    f"pregunta: P1\npreregistro_blob: {blob_de(RELLENO)}\n"
)


def test_con_todo_en_orden_se_abre(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []
    abrir(repo, "holdout-2", "P1")  # no lanza
    # y la autorizacion es POR PARTICION: la de holdout-2 no abre holdout-1
    assert any("AUTORIZACION-holdout-1.md" in m for m in motivos_de_cierre(repo, "holdout-1"))


@pytest.mark.parametrize(
    ("preregistro", "autorizacion", "aguja"),
    [
        (f"# PREREGISTRO\n{MARCA_SIN_RELLENAR}\n", BUENA, "sigue vacio"),
        (RELLENO, None, "no hay autorizacion"),
        (RELLENO, BUENA.replace("holdout-2", "holdout-1"), "autoriza 'holdout-1'"),
        (RELLENO, BUENA.replace("ADR-0099", "ADR-0777"), "no es un ADR que exista"),
        (RELLENO, BUENA.replace("2026-10-01", "ayer"), "no es AAAA-MM-DD"),
        (RELLENO, "particion: holdout-2\n", "faltan"),
        (RELLENO, BUENA.replace(f"preregistro_blob: {blob_de(RELLENO)}\n", ""), "faltan"),
        (RELLENO, BUENA.replace(blob_de(RELLENO), "HEAD"), "no es un sha de blob"),
        (RELLENO, BUENA.replace(blob_de(RELLENO), "A" * 40), "no es un sha de blob"),
        (RELLENO, BUENA.replace(blob_de(RELLENO), "0" * 40), "cambio despues de autorizar"),
        (RELLENO, BUENA.replace("pregunta: P1", "pregunta: P9"), "no la tiene"),
        (
            RELLENO.replace("estado: ABIERTA", "estado: GASTADA"),
            BUENA.replace(
                blob_de(RELLENO),
                blob_de(RELLENO.replace("estado: ABIERTA", "estado: GASTADA")),
            ),
            "ya se gasto",
        ),
        (RELLENO, BUENA.replace("pregunta: P1\n", ""), "faltan"),
        (RELLENO, "particion: holdout-1\n" + BUENA, "claves repetidas"),
        (RELLENO, BUENA + "particion: holdout-1\n", "claves repetidas"),
    ],
)
def test_cada_motivo_de_cierre_salta_por_su_cuenta(
    tmp_path: Path, preregistro: str, autorizacion: str | None, aguja: str
) -> None:
    repo = _repo(tmp_path, preregistro, autorizacion)
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any(aguja in m for m in motivos), motivos
    with pytest.raises(HoldoutCerradoError):
        abrir(repo, "holdout-2", "P1")


def test_una_autorizacion_sin_commitear_no_autoriza(tmp_path: Path) -> None:
    """Dificil de activar sin querer y trivial de auditar: lo que no esta en git no cuenta, y
    tampoco un fichero commiteado y cambiado despues en el arbol."""
    repo = _repo(tmp_path, RELLENO, None)
    auto = repo / "docs" / "validation" / "AUTORIZACION-holdout-2.md"
    auto.write_text(BUENA, encoding="utf-8")
    assert any("no hay autorizacion" in m for m in motivos_de_cierre(repo, "holdout-2"))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "autoriza")
    assert motivos_de_cierre(repo, "holdout-2") == []
    (repo / FICHERO_PREREGISTRO).write_text(RELLENO + "umbral: 0.5\n", encoding="utf-8")
    assert any("no esta commiteado" in m for m in motivos_de_cierre(repo, "holdout-2"))


def test_cambiar_el_preregistro_despues_de_autorizar_cierra_la_puerta(tmp_path: Path) -> None:
    """El hueco que cierra `preregistro_blob`: rellenar, autorizar, abrir y despues mover un umbral.
    La autorizacion seguia valiendo y el fichero seguia commiteado y relleno."""
    repo = _repo(tmp_path, RELLENO, BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []  # la autorizacion valida abre
    cambiado = RELLENO.replace("0.8", "0.6")
    (repo / FICHERO_PREREGISTRO).write_text(cambiado, encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "baja el umbral despues de abrir")
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any("cambio despues de autorizar" in m for m in motivos), motivos
    with pytest.raises(HoldoutCerradoError, match="autorizacion nueva"):
        abrir(repo, "holdout-2", "P1")
    # una autorizacion NUEVA sobre el pre-registro cambiado vuelve a abrir
    nueva = BUENA.replace(blob_de(RELLENO), blob_de(cambiado))
    (repo / "docs" / "validation" / "AUTORIZACION-holdout-2.md").write_text(nueva, encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "autoriza el pre-registro nuevo")
    assert motivos_de_cierre(repo, "holdout-2") == []


def test_el_blob_de_la_prueba_es_el_de_git(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, BUENA)
    salida = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", f"HEAD:{FICHERO_PREREGISTRO}"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert salida == blob_de(RELLENO)


def test_un_bom_no_rompe_una_autorizacion_buena(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, "\ufeff" + BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []


def test_sin_el_ejecutable_de_git_se_cierra_con_un_motivo(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import botsito.cases.holdout as puerta

    repo = _repo(tmp_path, RELLENO, BUENA)

    def sin_git(_repo: Path, _ruta: str) -> str | None:
        raise FileNotFoundError("git")

    monkeypatch.setattr(puerta, "contenido_en_head", sin_git)
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any("no esta commiteado" in m for m in motivos), motivos


def test_sin_git_no_se_abre_nada(tmp_path: Path) -> None:
    (tmp_path / "docs" / "validation").mkdir(parents=True)
    (tmp_path / FICHERO_PREREGISTRO).write_text(RELLENO, encoding="utf-8")
    assert motivos_de_cierre(tmp_path, "holdout-1")
    assert motivos_de_cierre(tmp_path, "dev") == [
        f"'dev' no es una particion reservada {RESERVADAS}"
    ]


def test_una_pregunta_gastada_no_se_vuelve_a_abrir(tmp_path: Path) -> None:
    """El defecto que cierra la enmienda de ADR-0033 (2026-09-21), en sus cuatro pasos.

    Hasta hoy una autorizacion era de un solo uso POR VERSION DEL PRE-REGISTRO, no por pregunta:
    medido, cincuenta aperturas seguidas con el repositorio sin tocar y `git status` vacio. No se
    podia detectar sin que algo cambiara entre una y otra, porque `abrir` es pura -y sigue
    siendolo-. Lo que cambia es que ahora el COMANDO gasta la pregunta antes de leer.

    El paso 4 es el que se vio fallar antes del arreglo: re-firmar citando una pregunta ya gastada
    daba `motivos == []` y la puerta abria.
    """
    repo = _repo(tmp_path, RELLENO, BUENA)
    assert motivos_de_cierre(repo, "holdout-2") == []  # 1. la primera apertura pasa
    abrir(repo, "holdout-2", "P1")

    gastar_pregunta(repo, "P1")  # 2. lo que hace el comando, antes de leer
    # Y ya esta cerrada ANTES de commitear: el arbol deja de coincidir con HEAD.
    assert any("no esta commiteado" in m for m in motivos_de_cierre(repo, "holdout-2"))
    _git(repo, "commit", "-q", "-am", "gasta P1")

    with pytest.raises(HoldoutCerradoError, match="cambio despues de autorizar"):
        abrir(repo, "holdout-2", "P1")  # 3. la segunda apertura se niega

    # 4. Y la re-firma sobre el pre-registro con P1 ya gastada TAMPOCO abre, que es lo que hoy si
    #    hacia: el blob vuelve a cuadrar, y lo unico que queda en pie es el estado de la pregunta.
    gastado = (repo / FICHERO_PREREGISTRO).read_text(encoding="utf-8")
    (repo / "docs" / "validation" / "AUTORIZACION-holdout-2.md").write_text(
        BUENA.replace(blob_de(RELLENO), blob_de(gastado)), encoding="utf-8"
    )
    _git(repo, "commit", "-q", "-am", "re-firma citando P1 ya gastada")
    motivos = motivos_de_cierre(repo, "holdout-2")
    assert any("ya se gasto" in m for m in motivos), motivos


def test_abrir_exige_la_pregunta_que_la_autorizacion_cita(tmp_path: Path) -> None:
    """`pregunta` es load-bearing: el acto de abrir DECLARA para que se abre, y se compara."""
    repo = _repo(tmp_path, RELLENO, BUENA)
    abrir(repo, "holdout-2", "P1")  # no lanza
    with pytest.raises(HoldoutCerradoError, match="autoriza la pregunta 'P1'"):
        abrir(repo, "holdout-2", "P2")


def test_gastar_una_pregunta_que_no_esta_o_ya_gastada(tmp_path: Path) -> None:
    repo = _repo(tmp_path, RELLENO, BUENA)
    with pytest.raises(HoldoutCerradoError, match="no declara la pregunta"):
        gastar_pregunta(repo, "P9")
    gastar_pregunta(repo, "P1")
    with pytest.raises(HoldoutCerradoError, match="no se gasta dos veces"):
        gastar_pregunta(repo, "P1")


def test_el_lector_decide_sobre_la_ruta_resuelta(tmp_path: Path) -> None:
    """Tres puntos y una barra saltaban la puerta (medido el 2026-09-21).

    `knowledge/cases/holdout/../holdout/2/<fichero>` hacia que `resto[0]` no fuera `1|2|3`, asi
    que NO se llamaba a `abrir`, mientras que `read_text` si resolvia el `..` y leia el fichero
    reservado. Ahora se decide sobre la ruta resuelta.
    """
    repo = _repo(tmp_path, RELLENO, None)
    reservado = repo / "knowledge" / "cases" / "holdout" / "2"
    reservado.mkdir(parents=True)
    (reservado / "caso-secreto.yaml").write_text("valor: SECRETO\n", encoding="utf-8")
    for ruta in (
        "knowledge/cases/holdout/2/caso-secreto.yaml",
        "knowledge/cases/holdout/./2/caso-secreto.yaml",
        "knowledge/cases/holdout/../holdout/2/caso-secreto.yaml",
    ):
        with pytest.raises(HoldoutCerradoError):
            leer_fichero(repo, ruta, "P1")
    # Y niega por defecto: una particion que no existe hoy cae del lado seguro, no del abierto.
    cuatro = repo / "knowledge" / "cases" / "holdout" / "4"
    cuatro.mkdir()
    (cuatro / "caso.yaml").write_text("valor: SECRETO\n", encoding="utf-8")
    with pytest.raises(HoldoutCerradoError):
        leer_fichero(repo, "knowledge/cases/holdout/4/caso.yaml", "P1")


def test_un_reparto_ilegible_no_se_salta_en_silencio(tmp_path: Path) -> None:
    """La puerta no puede responder a medias: un mapa incompleto es indistinguible de uno completo.

    Hasta el 2026-09-21 esto era un `continue` con un comentario que delegaba en
    `knowledge validate`, y el comentario era FALSO para toda carpeta que el glob ve y el validador
    de su camino no reconoce. Medido: un `particiones.yaml` roto bajaba los reservados del repo
    real de 34 a 24, y `feedback trace` y `kit kappa` seguian con exit 0 sin mencionarlo.
    """
    repo = tmp_path
    sano = repo / "knowledge" / "cases" / "kit" / "2026-09-09-sesion-01"
    sano.mkdir(parents=True)
    (sano / "particiones.yaml").write_text(
        "asignacion:\n  caso-xxxyyy-2026-05-04: holdout-1\n", encoding="utf-8"
    )
    assert casos_reservados(repo) == {"caso-xxxyyy-2026-05-04": "holdout-1"}

    roto = repo / "knowledge" / "cases" / "fidelidad" / "eurusd-2026-09"
    roto.mkdir(parents=True)
    (roto / "particiones.yaml").write_text("asignacion:\n  a: : :\n", encoding="utf-8")
    with pytest.raises(RepartoIlegibleError, match="particiones.yaml"):
        casos_reservados(repo)
