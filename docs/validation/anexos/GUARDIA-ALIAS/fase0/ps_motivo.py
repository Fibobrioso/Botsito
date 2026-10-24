r"""Fase 0.e: por que PowerShell niega SIN regla `\\?\` sobre un fichero BUENO (src/) y por que
deja pasar `$env:`. En memoria, con decidir sobre el repo inventado (el de medir_k.py). Uso:
python ps_motivo.py <carpeta de trabajo> <raiz del repo real (para cargar la guardia)>."""

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1]) / "Bot v3 prueba"
GANCHOS = Path(sys.argv[2]) / ".claude" / "hooks"
spec = importlib.util.spec_from_file_location("guardia", GANCHOS / "guardia.py")
g = importlib.util.module_from_spec(spec)
sys.modules["guardia"] = g
spec.loader.exec_module(g)
pol = g.Politica(RAIZ)
R = str(RAIZ)
BUENO = f"{R}\\src\\botsito\\cli.py"
casos = [
    ("src con \\\\?\\", f"Get-Content '\\\\?\\{BUENO}'"),
    ("src con //?/", f"Get-Content '//?/{BUENO.replace(chr(92), '/')}'"),
    ("src absoluta", f"Get-Content '{BUENO}'"),
    ("src con $env:USERPROFILE (no cae)", "Get-Content \"$env:USERPROFILE\\x\\y.txt\""),
    ("src con $HOME", "Get-Content \"$HOME\\x\\y.txt\""),
    ("src con $r propia", f"$r = '{R}'; Get-Content \"$r\\src\\botsito\\cli.py\""),
    ("gci -Recurse sobre el contenedor", f"Get-ChildItem -Recurse '{RAIZ.parent}' | Get-Content"),
    ("gci -Recurse sobre src", f"Get-ChildItem -Recurse '{R}\\src' | Get-Content"),
]
for etiqueta, cmd in casos:
    ev = {"tool_name": "PowerShell", "tool_input": {"command": cmd}, "cwd": R}
    m = g.decidir(ev, pol)
    m = (m or "pasa").replace(R, "<R>").replace(str(RAIZ.parent), "<padre>")
    print(f"- {etiqueta}: {m[:300]!r}")
