# Anexos de MARGEN-LOTE (R3.3)

Las salidas de las corridas del arnés y los guiones de medida de `trabajo/margen-lote`
(`docs/validation/MARGEN-LOTE.md`), sobre la misma construcción que R3.1 y R1.2 (enero del 2 al
30, abril, julio del 1 al 17 y agosto de 2026) y con los mismos diagnósticos (A-35 y A-44). **Son
DIAGNÓSTICO etiquetado, como las de R3.1 y R1.2: no cuentan para ninguna medida de fidelidad, no
habilitan mayo (ADR-0070 §3), no deciden ningún parámetro y no son una línea base.** Este README
existe antes de correr para que la carpeta esté en git: el arnés no la crea (`cli.py`,
`salida.write_text`).

## La corrida «antes» (fase 1), sobre el código de `main` más el campo de salida

Con la corrida diaria de R3.1 tal cual (su «cuenta=diaria» renace cada día), y la única diferencia
respecto a `main` son las cinco columnas nuevas de «### Ordenes» (lote, distancia, margen requerido,
margen libre al colocar y riesgo), que no cambian ninguna decisión:

   `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/antes-diaria.txt`
   → `antes-diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`

Su repetición con `--salida` fuera del repositorio, para el `diff` de determinismo, no se commitea.

## Las medidas (fase 1)

- `medida_2.py <salida> --fraccion 0.95`: rechazos por `volumen_max_lotes` y órdenes que rechazaría el
  margen, por mes, por orden y por sesión; salida en `medida_2.txt`. La fracción llega por argumento
  porque `lote_margen_libre_fraccion` no existe en el registro cuando corre la medida «antes».
- `fase4_medidas.py <salida> [--escribir <txt>]`: fase 4, sobre la corrida 2 con el limite: rechazos
  por motivo, ordenes limitadas y por que limite, riesgo efectivo; salida en `fase4_medidas.txt`.
- `stops_cortos.py --precios 1.10 1.20 [--noticias <csv> --ventana-min 2]`: la medida 1, sobre las
  operaciones del trader de los días dev de construcción por la compuerta del arnés, con las dos
  lecturas de A-56; salida en `stops_cortos.txt`. Su lectura de los casos dev se declara en
  `HOLDOUT-EXPOSICIONES.md` el día que corre.

## La re-corrida (fase 4), con el límite del lote y el rechazo por margen

Los tres comandos de R3.1 tal cual (`CORRIDA-CONSTRUCCION.md` §3.1) salvo la carpeta de `--salida`:

1. `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --salida docs/validation/anexos/MARGEN-LOTE/arrastrada.txt`
   → `arrastrada.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.txt`
2. `uv run botsito motor arnes --simular --diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/diaria.txt`
   → `diaria.DIAGNOSTICO.a35=cierre_vela_contraria.a44=sin_tope.cuenta=diaria.txt`
3. `uv run botsito motor arnes --simular --diagnostico-a35 inicio_vela_contraria --diagnostico-a44 sin_tope --diagnostico-cuenta-diaria --salida docs/validation/anexos/MARGEN-LOTE/a35-inicio.txt`
   → `a35-inicio.DIAGNOSTICO.a35=inicio_vela_contraria.a44=sin_tope.cuenta=diaria.txt`

La tabla de patrones (T0 y P1-P7) se cuenta con `patrones.py` de los anexos de R3.1, que lee la
ruta por argumento; no se copia ni se toca, y su salida sobre la corrida 2 queda aquí como
`patrones.txt`.

Lo que leen las corridas para calentar el sesgo (el M1 entero de marzo y de junio de 2026) se
declara en `docs/validation/HOLDOUT-EXPOSICIONES.md` el día de cada corrida y antes de correrla.
Ninguna salida de esta carpeta lleva la fecha ni el precio de la H4 que fija un sesgo, ni una fecha
fuera de los días dev de construcción salvo la línea de cobertura del calendario de cierres.
