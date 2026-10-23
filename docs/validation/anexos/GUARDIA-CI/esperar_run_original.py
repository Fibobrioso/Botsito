"""Espera a que un run de la CI termine y dice su estado (con gh run view)."""
import json
import subprocess
import sys
import time

RUN = sys.argv[1]
while True:
    salida = subprocess.run(
        ["gh", "run", "view", RUN, "--json", "status,conclusion"],
        capture_output=True,
        text=True,
    )
    if salida.returncode == 0:
        datos = json.loads(salida.stdout)
        if datos["status"] == "completed":
            print(f"run {RUN}: {datos['status']} {datos['conclusion']}")
            sys.exit(0)
    time.sleep(30)
