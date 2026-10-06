"""G1 sobre el repositorio real, sin conectarla a nada: lo que daria `knowledge validate`.

Solo ids y el campo `supersede` de la evidencia. Imprime cada aparicion de un supersedido que no
comparte valor escalar o linea de comentario con su sustituto, y las que si lo comparten (las
menciones en prosa que pasan), para comprobar la respuesta del consultor a la fase 0, punto 2.

Uso: uv run python docs/validation/anexos/GUARDIAS-CITAS/medir_g1.py [<repo>]
"""

from __future__ import annotations

import sys
from pathlib import Path

from botsito.evidence.modelo import cargar_evidencia
from botsito.validation.citas_supersedidas import (
    ID_EVIDENCIA,
    citas_a_supersedidos,
    ficheros_vigilados,
    sustitutos,
)


def main(repo: Path) -> int:
    items = cargar_evidencia(repo / "knowledge" / "evidence")
    cadenas = sustitutos(items)
    vigilados = ficheros_vigilados(repo)
    print(f"ficheros vigilados ({len(vigilados)}):")
    for p in vigilados:
        print(f"  {p.relative_to(repo).as_posix()}")
    print("\napariciones de supersedidos en los vigilados:")
    total = 0
    for p in vigilados:
        texto = p.read_text(encoding="utf-8", errors="replace")
        for m in ID_EVIDENCIA.finditer(texto):
            if m.group() in cadenas:
                total += 1
                linea = texto.count("\n", 0, m.start()) + 1
                print(f"  {p.relative_to(repo).as_posix()}:{linea}: {m.group()}")
    print(f"  total: {total}")
    problemas, n = citas_a_supersedidos(repo, items)
    print(f"\nG1 sobre {n} ficheros: {len(problemas)} fallos")
    for prob in problemas:
        print(f"  {prob}")
    print(f"pasan: {total - len(problemas)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()))
