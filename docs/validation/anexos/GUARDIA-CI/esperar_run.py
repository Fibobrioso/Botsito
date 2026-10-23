"""Rehecho desde la descripcion de EA-CONEXION.md §13: llama a `gh run view` cada 30 s hasta que el
run termina. NO SE EJECUTA: solo existe para que la guardia lo lea en la fase 0 de trabajo/guardia-ci."""

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
        check=False,
    ).stdout
    datos = json.loads(salida or "{}")
    print(datos)
    if datos.get("status") == "completed":
        break
    time.sleep(30)
