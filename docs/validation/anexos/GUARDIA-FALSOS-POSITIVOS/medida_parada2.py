"""TEMPORAL (PARADA 2 de trabajo/guardia-falsos-positivos): mide en memoria tres arreglos simulados.
Se borra antes de commitear; su salida va al anexo."""

from __future__ import annotations

import re
import time
from pathlib import Path
from types import ModuleType

import importlib.util
import sys

import pytest

_spec = importlib.util.spec_from_file_location(
    "gfp_t", Path(__file__).with_name("test_guardia_falsos_positivos.py")
)
assert _spec is not None and _spec.loader is not None
t = importlib.util.module_from_spec(_spec)
sys.modules["gfp_t"] = t
_spec.loader.exec_module(t)

g = t.g
repo = t.repo
base = t.base


def _simula(g: ModuleType, m: pytest.MonkeyPatch, variante: str, repo: Path) -> None:
    original = g.analizar_codigo
    if variante in {"B1", "B1+b", "B1+d"}:
        def tramo(lit: str) -> bool:
            tr = re.split(r"[\\/]", lit[2:], maxsplit=1)[0].strip(" \t")
            return re.search(r"[ \t]", tr) is not None
        m.setattr(g, "_tramo_lleva_blanco", tramo)
    if variante in {"B1+b", "B1+d"}:
        comentario = g._comentario_que_no_es_ruta

        def nueva(lit: str) -> bool:
            if not comentario(lit):
                return False
            if variante == "B1+b":
                sufijos = [lit[x.end():] for x in re.finditer(r"[\\/]", lit[2:])]
                sufijos = [lit[2 + x.end():] for x in re.finditer(r"[\\/]", lit[2:])]
            else:
                sufijos = [lit[i:] for i in range(2, len(lit))]
            pol = g.Politica(repo)
            for s in sufijos:
                if not s.strip():
                    continue
                try:
                    r = g._absoluta(s, str(repo))
                except g.BloqueoError:
                    return False
                if pol.motivo_fichero(r) or (Path(r).is_dir() and pol.motivo_ruta(r, recursivo=True)):
                    return False
            return True

        m.setattr(g, "_comentario_que_no_es_ruta", nueva)
    del original


CASOS = ["b1-h7-blanco-detras", "b1-h8-blanco-detras", "b1-h7-tab-detras", "b1-h4-blanco-detras",
         "b2-oculto-sin-fragmento"]  # fmt: skip


@pytest.mark.parametrize("variante", ["hoy", "B1", "B1+b", "B1+d"])
def test_medida(g: ModuleType, repo: Path, monkeypatch: pytest.MonkeyPatch, variante: str) -> None:
    t._con_oculto(repo)
    with monkeypatch.context() as m:
        if variante != "hoy":
            _simula(g, m, variante, repo)
        for caso in CASOS:
            mot = t._guion(g, repo, "t/rev.py", t._revisor(repo)[caso])
            print(f"PARADA2 | {variante} | {caso} | {'PASA' if mot is None else 'NIEGA'}")
        for caso, codigo in t._h_windows(repo).items():
            mot = t._guion(g, repo, "t/h.py", codigo)
            print(f"PARADA2 | {variante} | {caso} | {'PASA' if mot is None else 'NIEGA'}")
        t0 = time.perf_counter()
        mot = t._decide(g, repo, t._copia_de_generar_capa(repo))
        s = time.perf_counter() - t0
        print(f"PARADA2 | {variante} | f1-copia-generar-capa | {'PASA' if mot is None else 'NIEGA'} | {s:.2f}s")
        for i, lit in enumerate([t.LIT_364, "//\tx docs/a/b.md", "\\\\ x docs\\a\\b.md"]):
            mot = t._guion(g, repo, f"t/f1_{i}.py", t._lista(lit))
            print(f"PARADA2 | {variante} | f1-literal-{i} | {'PASA' if mot is None else 'NIEGA'}")
