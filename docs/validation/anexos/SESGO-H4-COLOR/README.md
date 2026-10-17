# Anexos de SESGO-H4-COLOR (R1.2)

Las salidas de la re-corrida del arnés de la fase 4 de `trabajo/sesgo-h4-color`
(`docs/validation/SESGO-H4-COLOR.md`), con el motor que aplica la regla del sesgo de H4 que el
trader respondió por WhatsApp el 2026-10-14 (una H4 cambia el sesgo solo si rompe el extremo de la
anterior y cierra del color de esa ruptura), sobre la misma construcción que R3.1 y con los mismos
diagnósticos (A-35 y A-44). **Son DIAGNÓSTICO etiquetado, como las de R3.1: no cuentan para ninguna
medida de fidelidad, no habilitan mayo (ADR-0070 §3), no deciden ningún parámetro y no son una
línea base.** Este README existe antes de correr para que la carpeta esté en git: el arnés no la
crea (`cli.py`, `salida.write_text`).

Los tres comandos, los de R3.1 tal cual (`CORRIDA-CONSTRUCCION.md` §3.1) salvo la carpeta de
`--salida`, desde la raíz del repositorio, y el fichero que escribe cada uno
(`diagnostico.nombre_etiquetado` añade el rótulo):

1. Principal, cuenta arrastrada:
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/SESGO-H4-COLOR/arrastrada.txt`
   → `arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt`
2. La misma con la cuenta reiniciada cada día (sobre esta se comparan los patrones):
   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/SESGO-H4-COLOR/diaria.txt`
   → `diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
3. La otra lectura de A-35, con la cuenta diaria:
   `uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/SESGO-H4-COLOR/a35-inicio.txt`
   → `a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt`

La tabla de patrones (T0 y P1-P7) se cuenta con `patrones.py` de los anexos de R3.1, que lee la
ruta por argumento (`docs/validation/anexos/CORRIDA-CONSTRUCCION/patrones.py <salida 2>`); no se
copia ni se toca, y su salida sobre la corrida 2 de esta rama queda aquí como `patrones.txt`.

Lo que leen las corridas para calentar el sesgo (el M1 entero de marzo y de junio de 2026) se
declara en `docs/validation/HOLDOUT-EXPOSICIONES.md` el día de la corrida y antes de correrla.
Ninguna salida de esta carpeta lleva la fecha ni el precio de la H4 que fija un sesgo.
