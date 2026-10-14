# Anexos de CORRIDA-CONSTRUCCION (R3.1)

Las salidas de las tres corridas del arnés de la fase 2 de `trabajo/corrida-construccion`
(`docs/validation/CORRIDA-CONSTRUCCION.md`), sobre toda la construcción vigente (abril, julio del 1
al 17, agosto y enero del 2 al 30 de 2026; `criterio_fidelidad.yaml`, `construccion`), con los
diagnósticos que el motor aún necesita (A-35 y A-44). **Son DIAGNÓSTICO etiquetado: cada línea y
cada nombre lleva su rótulo, no cuentan para ninguna medida de fidelidad, no habilitan mayo
(ADR-0070 §3) y no son una línea base** (`diagnostico.py`: un fichero de diagnóstico nunca lleva el
nombre de una línea base). Este README existe antes de correr para que la carpeta esté en git: el
arnés no la crea (`cli.py`, `salida.write_text`).

Los cuatro comandos autorizados por el consultor (encargo del 2026-10-14 y su respuesta a la
PARADA, punto 15), desde la raíz del repositorio, y el fichero que escribe cada uno
(`diagnostico.nombre_etiquetado` añade el rótulo):

1. Principal, cuenta arrastrada (como operará el bot):
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/arrastrada.txt`
   → `arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt`
2. La misma con la cuenta reiniciada cada día (la estrategia sin el camino de la cuenta; sobre
   esta se clasifica):
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/diaria.txt`
   → `diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
3. La otra lectura de A-35, con la cuenta diaria:
   `uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/CORRIDA-CONSTRUCCION/a35-inicio.txt`
   → `a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
4. La repetición de la 2 con `--salida` fuera del repositorio, solo para comprobar con `diff`
   que el informe es determinista byte a byte; la copia se borra después y no se commitea:
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida <carpeta temporal>/diaria.txt`

Cada salida lleva al final de su parte del arnés la sección `## Diferencias por operacion`
(resumen por mes, embudo por mes y una fila por operación del trader y por operación del bot sin
pareja; `docs/runbooks/ARNES-MOTOR.md`), y después la cola de la simulación. Las líneas `TIEMPO` y
`MEMORIA` van por pantalla, no al fichero: están copiadas en el informe de la rama.
