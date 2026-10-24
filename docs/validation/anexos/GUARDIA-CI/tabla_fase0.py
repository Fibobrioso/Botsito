"""Fase 0 a) de trabajo/guardia-ci: cada comando de la tabla por `decidir` de la guardia, EN MEMORIA.
No ejecuta ninguno: solo construye el evento y llama a la funcion de decision, como los tests."""

import importlib.util
import sys
from pathlib import Path

RAIZ = Path(sys.argv[1])
AQUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("guardia_f0", RAIZ / ".claude" / "hooks" / "guardia.py")
g = importlib.util.module_from_spec(spec)
sys.modules["guardia_f0"] = g
spec.loader.exec_module(g)

RUN = "39893825671"
SHA = "2a99e64fa00d1ff4b0c45ee659614f1a21e2d110"
API = "https://api.github.com/repos/Fibobrioso/Botsito"
GUION = (AQUI / "esperar_run.py").as_posix()
PYC = (
    'python -c "import subprocess, time\n'
    "while True:\n"
    f"    subprocess.run(['gh', 'run', 'view', '{RUN}'])\n"
    '    time.sleep(30)"'
)
PYC_UNA = (
    f"python -c \"import subprocess,time; [(subprocess.run(['gh','run','view','{RUN}']), "
    'time.sleep(30)) for _ in range(20)]"'
)
GREP = "grep -o '\"status\": *\"[^\"]*\"\\|\"conclusion\": *\"[^\"]*\"'"

CASOS = [
    # (id, lado, herramienta, comando)
    ("N1", "negar", "Bash", f"while true; do gh run view {RUN} --json status; sleep 30; done"),
    ("N2", "negar", "Bash", f"until gh run view {RUN} --exit-status; do sleep 30; done"),
    ("N3", "negar", "Bash", f"for i in 1 2 3; do gh run view {RUN}; sleep 30; done"),
    ("N3b", "negar", "Bash", f"for n in 1 2 3; do gh run view {RUN}; sleep 30; done"),
    ("N4", "negar", "Bash", f"gh run view {RUN} && sleep 30 && gh run view {RUN}"),
    ("N5", "negar", "Bash", f"gh run watch {RUN}"),
    ("N5b", "negar", "Bash", f"gh run watch {RUN} --exit-status"),
    ("N6", "negar", "Bash", f"watch -n 30 gh run view {RUN}"),
    ("N7", "negar", "Bash", PYC),
    ("N7b", "negar", "Bash", PYC_UNA),
    ("N8", "negar", "Bash", f'python "{GUION}" {RUN}'),
    ("N8b", "negar", "Bash", f'uv run python "{GUION}" {RUN}'),
    ("N9", "negar", "PowerShell",
     f"for ($i = 0; $i -lt 20; $i++) {{ gh run view {RUN}; Start-Sleep -Seconds 30 }}"),
    ("N9b", "negar", "PowerShell", f"while ($true) {{ gh run view {RUN}; Start-Sleep 30 }}"),
    ("N9c", "negar", "PowerShell", f"gh run view {RUN}; Start-Sleep 30; gh run view {RUN}"),
    # ampliaciones de la fase 0
    ("N10", "negar", "Bash", f"while true; do curl -s {API}/commits/{SHA}/check-runs | {GREP}; sleep 30; done"),
    ("N11", "negar", "Bash", f"while true; do gh api repos/Fibobrioso/Botsito/actions/runs/{RUN} --jq .status; sleep 30; done"),
    ("N12", "negar", "Bash", f"timeout 600 gh run watch {RUN}"),
    ("N13", "negar", "Bash", f"gh run view {RUN}; sleep 30; gh run view {RUN}"),
    ("N14", "negar", "Bash", "gh pr checks 12 --watch"),
    ("N15", "duda", "Bash", f"sleep 300 && gh run view {RUN} --json status,conclusion"),
    ("N16", "duda", "Bash", f"sleep 300; gh run view {RUN}"),
    ("N17", "negar", "Bash", f"until curl -s {API}/commits/{SHA}/check-runs | grep -q completed; do sleep 30; done"),
    ("N18", "negar", "Bash", f"while sleep 30; do gh run view {RUN}; done"),
    # los guiones reales del incidente de EA-CONEXION.md §13 (copiados del scratchpad de aquella
    # sesion, que el auditor encontro: existen)
    ("N8c", "negar", "Bash", f'python "{(AQUI / "esperar_run_original.py").as_posix()}" {RUN}'),
    ("N8d", "negar", "Bash", f'sh "{(AQUI / "esperar_run_original.sh").as_posix()}" {RUN}'),
    # el caso de corrida-construccion (SESGO-H4-COLOR.md:1301): curl con la ruta dentro de Python
    ("N19", "negar", "Bash",
     f"python -c \"import subprocess,time\nwhile True:\n    subprocess.run(['curl','-s',"
     f"'{API}/commits/{SHA}/check-runs'])\n    time.sleep(30)\""),
    # el lado bueno
    ("B1", "pasar", "Bash", f"gh run view {RUN} --json status,conclusion,headSha"),
    ("B2", "pasar", "Bash", f"gh run view {RUN} --log-failed"),
    ("B3", "pasar", "Bash", f"gh run view {RUN} --exit-status"),
    ("B4", "pasar", "Bash", "gh run list --branch fix/x"),
    ("B5", "pasar", "Bash", f"gh run rerun {RUN}"),
    ("B6", "pasar", "Bash", "sleep 120"),
    ("B7", "pasar", "Bash", f"curl -s --ssl-no-revoke {API}/commits/$(git rev-parse HEAD)/check-runs | {GREP}"),
    ("B8", "pasar", "Bash", f"curl -s {API}/commits/{SHA}/check-runs | grep -E '\"(name|status|conclusion|html_url)\"'"),
    ("B9", "pasar", "Bash", f"gh run list --branch fix/guardia-ci --limit 3"),
    ("B10", "pasar", "Bash", f"gh api repos/Fibobrioso/Botsito/actions/runs/{RUN} --jq .status"),
    ("B11", "pasar", "Bash", f"gh run view {RUN} --log-failed | tail -50"),
    ("B12", "pasar", "Bash", f"gh run view {RUN} --json jobs --jq '.jobs[].conclusion'"),
    # la de docs/HANDOFF.md:1051 (auditor, H3)
    ("B13", "pasar", "Bash", f"curl -s {API}/commits/{SHA}/check-runs"),
]


def regla(motivo):
    if motivo is None:
        return "pasa"
    nombres = [n for n in dir(g) if n.startswith("R_") and f"Regla: {getattr(g, n)}" in motivo]
    return ",".join(nombres) or "sin R_"


politica = g.Politica(RAIZ)
for ident, lado, herramienta, comando in CASOS:
    evento = {"tool_name": herramienta, "tool_input": {"command": comando}, "cwd": str(RAIZ)}
    motivo = g.decidir(evento, politica)
    primera = (motivo or "").split("\n")[0]
    print(f"{ident}\t{lado}\t{regla(motivo)}\t{primera[:200]}")
