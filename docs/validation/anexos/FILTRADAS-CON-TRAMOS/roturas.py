"""Las roturas a proposito de `trabajo/filtradas-con-tramos` (encargo, «TESTS»): cada una cambia una
linea de `scripts/transcribir_sesion.py`, corre los tests nuevos, apunta cuales caen y restaura el
fichero, comprobando que su sha256 vuelve a ser el de antes.

ESCRIBE en el guion, asi que se ejecuta SOLO sobre un clon desechable (`git worktree add`), nunca
sobre el repositorio de trabajo (CLAUDE.md, «Ensayos aislados»). La raiz sale del primer argumento:

    git worktree add <dir temporal> HEAD
    (copiar alli los ficheros sin commitear, si los hay)
    <python del repo> docs/validation/anexos/FILTRADAS-CON-TRAMOS/roturas.py <dir temporal>

Se niega si la raiz es la del repositorio de trabajo.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parents[4]
ROTURAS = [
    (
        "1. no se aplican los tramos (lineas_filtradas no tapa ningun segmento por tramo)",
        "    no_citables = tapados_por_tramos(segmentos, tramos)\n",
        "    no_citables: frozenset[int] = frozenset()\n",
    ),
    (
        "2. sin fichero de tramos se sigue (se quita la comprobacion de que existe)",
        "    if not (repo / FICHERO_TRAMOS_NO_CITABLES).is_file():\n",
        "    if False:\n",
    ),
    (
        "3. el borde se tapa (>= en lugar de >: un segmento que empieza en el fin del tramo)",
        "if any(s.t1_ms > a and s.t0_ms < b for a, b, _ in tramos)",
        "if any(s.t1_ms >= a and s.t0_ms <= b for a, b, _ in tramos)",
    ),
    (
        "4. sin --video se sigue sin tramos (None da una tupla vacia)",
        '        raise SesionError("falta --video: sin el video de la sesion no se aplican sus '
        'tramos")\n',
        "        return ()\n",
    ),
    (
        "5. no se comprueba que el audio sea del video (respuesta del consultor del 2026-10-05)",
        "    sha_wav = comprobar_audio_del_video(audio, video, RAIZ)\n",
        '    sha_wav = "0" * 64\n',
    ),
]


def main(raiz: Path) -> int:
    raiz = raiz.resolve()
    if raiz == AQUI:
        print("ERROR: esto escribe en el guion; solo sobre un clon desechable (git worktree)")
        return 2
    guion = raiz / "scripts" / "transcribir_sesion.py"
    original = guion.read_bytes()
    sha = hashlib.sha256(original).hexdigest()
    print(f"guion: sha256 {sha}")
    for nombre, de, a in ROTURAS:
        texto = original.decode("utf-8")
        assert texto.count(de) == 1, f"la rotura {nombre!r} no encuentra su linea"
        guion.write_bytes(texto.replace(de, a).encode("utf-8"))
        try:
            salida = subprocess.run(
                [sys.executable, "-m", "pytest", "tests/unit/test_filtradas_con_tramos.py", "-q",
                 "-p", "no:cacheprovider", "-rf"],
                cwd=raiz, capture_output=True, text=True, encoding="utf-8",
            )  # fmt: skip
        finally:
            guion.write_bytes(original)
        caidos = sorted(set(re.findall(r"^FAILED \S+?::(.+?)(?: - .*)?$", salida.stdout, re.M)))
        # La configuracion de pytest del repo no imprime la linea de resumen: manda el codigo.
        resumen = f"pytest sale con {salida.returncode} (0 = todos pasan)"
        print(f"\n{nombre}\n  resultado: {resumen}\n  caen ({len(caidos)}):")
        for c in caidos:
            print(f"    - {c}")
        restaurado = hashlib.sha256(guion.read_bytes()).hexdigest()
        print(f"  restaurado: {'sha igual' if restaurado == sha else 'SHA DISTINTO'}")
        if restaurado != sha:
            return 1
    final = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/test_filtradas_con_tramos.py", "-q",
         "-p", "no:cacheprovider"],
        cwd=raiz, capture_output=True, text=True, encoding="utf-8",
    )  # fmt: skip
    print(f"\nrestaurado, de nuevo: pytest sale con {final.returncode} (0 = todos pasan)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(Path(sys.argv[1])))
