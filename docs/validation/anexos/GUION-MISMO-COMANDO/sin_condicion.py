"""trabajo/guion-mismo-comando, fase 1: que los tests de la condicion fallan si se quita, y que
fallan LOS QUE TIENEN QUE FALLAR.

Sin tocar el codigo ni los tests: carga la guardia como el modulo que usan los tests
(`guardia_claude`), le cambia EN MEMORIA una pieza y corre los tests `ejecucion` de
`tests/unit/test_guardia_claude.py` dentro de este proceso. Las mutaciones:

- «sin la condicion»: `exigir_ejecucion_verificable` no hace nada. Tienen que fallar EXACTAMENTE
  todos los casos de los tests que esperan una negacion, y ninguno de los que esperan que pase;
- una por cada pieza con nombre de la condicion (`_exigir_sin_expansiones`, `_exigir_lo_de_antes`,
  `_exigir_lo_de_a_la_vez`, `_exigir_salida_ajena`) y «sin la existencia» (un guion que no existe
  pasa, como en `main`): tienen que fallar, al menos, los casos que solo esa pieza niega.

Con la condicion entera, todos pasan; restaurada cada mutacion, vuelven a pasar. Los tests corren
sobre el repositorio SINTETICO de su fixture: ningun material se abre y no se ejecuta ninguno de los
comandos que miden (revisor de la rama, A7: la primera version solo pedia «que falle algo»).

Uso: uv run python docs/validation/anexos/GUION-MISMO-COMANDO/sin_condicion.py
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

RAIZ = Path(__file__).resolve().parents[4]
GUARDIA = RAIZ / ".claude" / "hooks" / "guardia.py"
TESTS = RAIZ / "tests" / "unit" / "test_guardia_claude.py"

# Los tests que esperan una NEGACION: sin la condicion, fallan todos sus casos.
NIEGAN = (
    "test_ejecucion_cambiada_en_el_mismo_comando_se_niega",
    "test_ejecucion_cada_via_pasa_por_la_condicion",
    "test_ejecucion_lo_de_fuera_de_la_lista_se_niega",
    "test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo",
    "test_ejecucion_make_solo_con_el_makefile_de_main",
    "test_ejecucion_powershell_sin_ejecuciones_y_lo_demas_igual",
    "test_ejecucion_lo_que_no_esta_en_la_lista_es_una_ejecucion",
    "test_ejecucion_lo_que_vio_la_segunda_pasada_se_niega",
    "test_ejecucion_un_modo_que_ejecuta_se_niega",
    "test_ejecucion_la_ultima_ronda_niega",
    "test_ejecucion_cuarta_pasada_niega",
    "test_ejecucion_cuarta_pasada_powershell_git_niega",
    "test_ejecucion_quinta_pasada_niega",
    "test_ejecucion_sexta_pasada_niega",
)
# Los de los nombres de entorno: esa regla vale para TODO comando (tambien `git commit`, que corre
# hooks), asi que vive junto a la funcion y no dentro; se miran con su propia mutacion.
NOMBRES = (
    "test_ejecucion_un_nombre_de_entorno_que_carga_codigo_se_niega",
    "test_ejecucion_los_nombres_de_entorno_son_una_lista_cerrada",
    "test_ejecucion_la_ultima_ronda_fija_variable_niega",
    "test_ejecucion_cuarta_pasada_fija_variable_niega",
    "test_ejecucion_quinta_pasada_fija_variable_niega",
    "test_ejecucion_sexta_pasada_fija_variable_niega",
)
CAMBIADA = "test_ejecucion_cambiada_en_el_mismo_comando_se_niega"
LISTA = "test_ejecucion_lo_que_no_esta_en_la_lista_es_una_ejecucion"
SEGUNDA = "test_ejecucion_lo_que_vio_la_segunda_pasada_se_niega"
VIA = "test_ejecucion_cada_via_pasa_por_la_condicion"
FUERA = "test_ejecucion_lo_de_fuera_de_la_lista_se_niega"
# Lo que SOLO niega cada pieza (el guion existe y lo demas del comando esta en la lista).
ESPERADOS: dict[str, list[str]] = {
    "_exigir_sin_expansiones": [
        f"{CAMBIADA}[python existente.py <(cp a.py existente.py)]",
        f"{FUERA}[PYTHONUTF8=$Y python inocuo.py]",
        f"{FUERA}[PYTHONUTF8=$(echo 1) python inocuo.py]",
    ],
    "_exigir_lo_de_antes": [
        f"{CAMBIADA}[cp a.py existente.py && uv run python existente.py]",
        f"{CAMBIADA}[cp a.py scripts/otro.py && uv run python scripts/otro.py]",
        f"{FUERA}[inventado && python inocuo.py]",
        f"{FUERA}[grep hola docs/a.md && python inocuo.py]",
        f"{FUERA}[python inocuo.py && python existente.py]",
        f"{FUERA}[set -x; python inocuo.py]",
        # `cd && python inocuo.py` no: tras `cd` a secas (HOME) el guion tampoco existe, y lo
        # niegan las dos piezas.
    ],
    "_exigir_lo_de_a_la_vez": [
        f"{CAMBIADA}[python existente.py & cp a.py existente.py]",
        f"{FUERA}[python inocuo.py | tee salida.txt]",
        f"{FUERA}[python inocuo.py | sort -o salida.txt]",
        f"{FUERA}[python inocuo.py | uniq - salida.txt]",
        f"{FUERA}[python inocuo.py | cat]",
    ],
    "_exigir_salida_ajena": [f"{CAMBIADA}[python existente.py > existente.py]"],
    "_no_ejecuta": [
        f"{LISTA}[cp a.py b.php && php b.php]",
        f"{LISTA}[cp a.py b.py && setsid ./b.py]",
        f"{LISTA}[php nuevo.php]",
        f"{LISTA}[inventado docs/nuevo.md]",
        f"{LISTA}[inventado $X]",
        f"{LISTA}[sudo make check > make-check.log 2>&1]",
        f"{LISTA}[winpty python inocuo.py]",
    ],
    "_ficheros_de_un_programa_desconocido": [
        f"{LISTA}[php nuevo.php]",
        f"{LISTA}[inventado docs/nuevo.md]",
        f"{LISTA}[inventado $X]",
    ],
    "_nombre_admitido": [
        *(
            f"{NOMBRES[0]}[{n}]"
            for n in (
                "PYTHONPATH",
                "PYTHONSTARTUP",
                "PYTHONHOME",
                "BASH_ENV",
                "ENV",
                "NODE_OPTIONS",
                "PERL5OPT",
                "RUBYOPT",
                "LD_PRELOAD",
                "LD_LIBRARY_PATH",
            )
        ),
        NOMBRES[1],
    ],
    "_fichero_de_programa": [
        f"{LISTA}[awk -f a.py docs/a.md]",
        f"{LISTA}[awk -fa.py docs/a.md]",
        f"{LISTA}[sed -f a.py docs/a.md]",
        f"{SEGUNDA}[Bash-sed -nf a.py docs/a.md]",
        f"{SEGUNDA}[Bash-sed -sf a.py docs/a.md]",
    ],
    "_ejecucion_en_powershell": [
        f"{SEGUNDA}[PowerShell-Write-Output ( php x.php )]",
        f"{SEGUNDA}[PowerShell-Write-Output $( cscript x.js )]",
        f"{SEGUNDA}[PowerShell-Write-Output @( php x.php )]",
        f"{SEGUNDA}[PowerShell-Get-Content docs/a.md; ( php x.php )]",
        f"{SEGUNDA}[PowerShell-git -c alias.x='!python a.py' x]",
        f"{VIA}[PowerShell-python inocuo.py]",
        f"{VIA}[PowerShell-uv run botsito state check]",
        "test_ejecucion_powershell_sin_ejecuciones_y_lo_demas_igual",
    ],
    "_set_admitido": [f"{FUERA}[set -x; python inocuo.py]"],
    "_es_filtro": [
        f"{FUERA}[python inocuo.py | tee salida.txt]",
        f"{FUERA}[python inocuo.py | sort -o salida.txt]",
        f"{FUERA}[python inocuo.py | uniq - salida.txt]",
        f"{FUERA}[python inocuo.py | cat]",
    ],
    "botsito": [f"{CAMBIADA}[cp a.py b.py && uv run botsito state check]"],
    "_codigo_de_opciones": [
        f"{SEGUNDA}[Bash-node -r ./a.py inocuo.py]",
        f"{SEGUNDA}[Bash-node --require=./a.py inocuo.py]",
        f"{SEGUNDA}[Bash-node --import ./a.py inocuo.py]",
        f"{SEGUNDA}[Bash-ruby -r ./a.py inocuo.py]",
        f"{SEGUNDA}[Bash-node -r dotenv/config inocuo.py]",
        f"{SEGUNDA}[Bash-bash --rcfile malo.sh -i -c true]",
    ],
    "_es_fichero_de_la_rama": [
        f"{SEGUNDA}[Bash-./git status]",
        f"{SEGUNDA}[Bash-sub/git status]",
        f"{SEGUNDA}[Bash-./python inocuo.py]",
    ],
    "GIT_SUBCOMANDOS": [
        "test_ejecucion_un_modo_que_ejecuta_se_niega[git bisect run python a.py]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[git submodule foreach 'python a.py']",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[git filter-branch --tree-filter 'python a.py']",  # noqa: E501
    ],
    "GIT_C_CLAVES": ["test_ejecucion_la_ultima_ronda_niega"],
    "_git_transporte": ["test_ejecucion_la_ultima_ronda_niega"],
    "_modo_git": ["test_ejecucion_la_ultima_ronda_niega"],
    "_awk_admitido": ["test_ejecucion_la_ultima_ronda_niega"],
    "_sed_admitido": ["test_ejecucion_la_ultima_ronda_niega"],
    "_exigir_builtin_que_fija": ["test_ejecucion_la_ultima_ronda_fija_variable_niega"],
    "_exigir_for": ["test_ejecucion_la_ultima_ronda_fija_variable_niega"],
    "_exigir_sin_aritmetica": ["test_ejecucion_la_ultima_ronda_fija_variable_niega"],
    "_modo_que_ejecuta": [
        "test_ejecucion_un_modo_que_ejecuta_se_niega[gh alias set -s x 'python a.py']",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sort --compress-program=./a.py docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sort --random-source=./a.py docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[awk 'BEGIN{system(\"python a.py\")}' docs/a.md]",  # noqa: E501
        "test_ejecucion_un_modo_que_ejecuta_se_niega[awk '{print > \"out\"}' docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[awk '{while((getline x)>0) y=x}' docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sed 's/x/y/e' docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sed '1e python a.py' docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sed 'w salida.txt' docs/a.md]",
        "test_ejecucion_un_modo_que_ejecuta_se_niega[sed '1r /etc/passwd' docs/a.md]",
    ],
    "_exigir_guion_legible": [
        f"{FUERA}[python nuevo.py]",
        "test_ejecucion_un_guion_que_no_existe_dice_como_reescribirlo",
    ],
}


class _TodoDentro:
    """Un conjunto de mentira para la mutacion de `GIT_SUBCOMANDOS`: todo subcomando esta dentro,
    asi que la guardia nunca lo trata como ejecucion."""

    def __contains__(self, _x: object) -> bool:
        return True


class Resultados:
    def __init__(self) -> None:
        self.por_test: dict[str, str] = {}

    def pytest_runtest_logreport(self, report: Any) -> None:
        if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
            self.por_test[report.nodeid.split("::", 1)[1]] = report.outcome


def correr() -> dict[str, str]:
    resultados = Resultados()
    argumentos = [str(TESTS), "-q", "-p", "no:cacheprovider", "-k", "ejecucion", "--no-header"]
    pytest.main([*argumentos, "-rN", "--tb=no"], plugins=[resultados])
    return resultados.por_test


def main() -> int:
    spec = importlib.util.spec_from_file_location("guardia_claude", GUARDIA)
    assert spec is not None and spec.loader is not None
    g = importlib.util.module_from_spec(spec)
    sys.modules["guardia_claude"] = g  # el fixture `g` de los tests reutiliza este modulo
    spec.loader.exec_module(g)

    original_guion = g._exigir_guion_legible

    def guion_como_en_main(ctx: Any, lex: Any, que: str, palabra: Any, lenguaje: str) -> bool:
        valores = g._valores(palabra, ctx, lex) or []
        if len(valores) == 1 and not Path(g._absoluta(valores[0], ctx.cwd)).exists():
            return False
        resultado: bool = original_guion(ctx, lex, que, palabra, lenguaje)
        return resultado

    def nada(*_args: Any, **_kwargs: Any) -> bool:
        return True

    mutaciones: list[tuple[str, str, Callable[..., Any]]] = [
        ("sin la condicion", "exigir_ejecucion_verificable", nada),
        ("sin las expansiones", "_exigir_sin_expansiones", nada),
        ("sin lo de antes", "_exigir_lo_de_antes", nada),
        ("sin lo de a la vez", "_exigir_lo_de_a_la_vez", nada),
        ("sin la salida ajena", "_exigir_salida_ajena", nada),
        ("sin la existencia", "_exigir_guion_legible", guion_como_en_main),
        ("sin lo que activa (todo programa no ejecuta)", "_no_ejecuta", lambda _p: True),
        (
            "sin los ficheros de un programa desconocido",
            "_ficheros_de_un_programa_desconocido",
            lambda *_a, **_k: ([], False),
        ),
        ("sin los nombres de entorno", "_nombre_admitido", lambda _n: True),
        ("sin awk/sed -f (segunda pasada, A4)", "_fichero_de_programa", lambda *_a: None),
        ("sin PowerShell (A4)", "_ejecucion_en_powershell", lambda _t: None),
        ("sin la lista de set (A4)", "_set_admitido", lambda _o: True),
        ("sin los filtros (A4)", "_es_filtro", lambda _c: True),
        ("sin botsito como ejecucion (A4, B8)", "botsito", None),
        ("sin el codigo de las opciones (B1)", "_codigo_de_opciones", lambda *_a: []),
        (
            "sin el fichero de la rama como programa (B5)",
            "_es_fichero_de_la_rama",
            lambda *_a: False,
        ),
        ("sin la lista de subcomandos de git (§1.21)", "GIT_SUBCOMANDOS", _TodoDentro()),
        ("sin los modos que ejecutan (§1.21)", "_modo_que_ejecuta", lambda *_a: None),
        ("sin las claves de git -c (§1.27)", "GIT_C_CLAVES", _TodoDentro()),
        ("sin las opciones de transporte de git (§1.27)", "_git_transporte", lambda *_a: None),
        ("sin config/remote/merge de git (§1.27)", "_modo_git", lambda *_a: None),
        ("sin la lista de awk (§1.27)", "_awk_admitido", lambda *_a: True),
        ("sin la lista de sed (§1.27)", "_sed_admitido", lambda *_a: True),
        ("sin los builtins que fijan (§1.27)", "_exigir_builtin_que_fija", lambda *_a, **_k: None),
        ("sin la variable del for (§1.27)", "_exigir_for", lambda *_a: None),
        ("sin el (( )) aritmetico (§1.27)", "_exigir_sin_aritmetica", lambda *_a: None),
    ]
    base = correr()
    niegan = {t for t in base if t.split("[", 1)[0] in NIEGAN}
    print(
        f"\n== con la condicion: {len(base)} tests, fallan {sum(r != 'passed' for r in base.values())}"  # noqa: E501
    )
    print(f"   esperan una negacion: {len(niegan)}")
    ok = all(r == "passed" for r in base.values())
    exigir = g.exigir_ejecucion_verificable

    def sin_botsito(ctx: Any, lex: Any, cmd: Any, que: str, **kw: Any) -> bool:
        if que.startswith("botsito"):
            return True
        resultado: bool = exigir(ctx, lex, cmd, que, **kw)
        return resultado

    for titulo, nombre, sustituta in mutaciones:
        if nombre == "botsito":  # la rama de `botsito` en `analizar_comando`, sin la funcion
            nombre, sustituta = "exigir_ejecucion_verificable", sin_botsito
        original = getattr(g, nombre)
        setattr(g, nombre, sustituta)
        try:
            mutado = correr()
        finally:
            setattr(g, nombre, original)
        restaurado = correr()
        fallan = {t for t, r in mutado.items() if r != "passed"}
        print(f"\n== {titulo} ({nombre}): fallan {len(fallan)} de {len(mutado)}")
        if sustituta is sin_botsito:
            nombre = "botsito"
        if nombre == "exigir_ejecucion_verificable":
            fallan = {t for t in fallan if t.split("[", 1)[0] not in NOMBRES}
            exacto = fallan == niegan
            print(f"   fallan EXACTAMENTE los que esperan una negacion: {'si' if exacto else 'NO'}")
            for t in sorted(fallan ^ niegan):
                print(f"   DIFERENCIA  {t}")
            ok = ok and exacto
        else:
            faltan = [
                e
                for e in ESPERADOS[nombre]
                if not any(f == e or f.split("[", 1)[0] == e for f in fallan)
            ]
            print(
                f"   de los {len(ESPERADOS[nombre])} que solo niega esta pieza, fallan "
                f"{len(ESPERADOS[nombre]) - len(faltan)}"
            )
            for t in faltan:
                print(f"   NO FALLA  {t}")
            ok = ok and not faltan
        for t in sorted(fallan):
            print(f"   FALLA  {t}")
        no_restaura = [t for t, r in restaurado.items() if r != "passed"]
        print(f"   restaurado: fallan {len(no_restaura)}")
        ok = ok and not no_restaura
    print(
        "\nVEREDICTO: "
        + (
            "sin la condicion fallan exactamente los que esperan una negacion; cada pieza rompe "
            "los suyos; restaurada, todo pasa"
            if ok
            else "NO"
        )
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
