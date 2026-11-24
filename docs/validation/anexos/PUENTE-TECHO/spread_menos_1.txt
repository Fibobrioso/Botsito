# puente.py variante spread_menos_1, sobre cuenta-por-mes.txt (ADR-0099; PUENTE-TECHO)

## El control (ADR-0098 §1), con el bucle de puente.py (D2 a)
posiciones del bot en la salida: 235; entran en el control: 235; fuera (manual de una regla solo del bot): 0
reproducidas al centimo (lote, motivo, instante del cierre, PnL neto): 235 de 235
control: PASA

## Variante spread_menos_1 (suelta): [spread_menos_1]
### Los cuatro meses
N (llenadas y cerradas): 196; no colocables: 2; no llenadas: 0; fuera por el tope de lotes: 0; fuera por el lote minimo: 0; fuera de la ventana: 0
cerradas con riesgo no positivo (no entran): 0
rechazadas por el broker, por motivo: ninguna
break even movido: 85; cerradas en el break even: 50; cierres por RN-002: 7; al fin del dia: 0
esperanza antes de comision y swaps (media del R bruto): 0.168; neta (media del R neto): -0.196
percentil 5 y percentil 95 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, 76 dias): -0.419 y 0.034; replicas descartadas: 0
d) perdida diaria maxima, por cuenta: 4.95 % del capital inicial; la peor, la cuenta de 2026-07
e) equity minima, por cuenta: 93.54 % del capital inicial; la peor, la cuenta de 2026-07
f) alguna cuenta entro en SUSPENDIDA: no
LECTURA POR EL R (ADR-0099 §3): no_gana
lectura de ADR-0098 §2 (lectura_techo): no_gana
### Abril y agosto juntos (sin lectura)
N (llenadas y cerradas): 77; no colocables: 0; no llenadas: 0; fuera por el tope de lotes: 0; fuera por el lote minimo: 0; fuera de la ventana: 0
rechazadas por el broker, por motivo: ninguna
break even movido: 31; cerradas en el break even: 17; cierres por RN-002: 4; al fin del dia: 0
esperanza antes de comision y swaps (media del R bruto): 0.088; neta (media del R neto): -0.340
percentil 5 y percentil 95 de la media del R neto, por remuestreo por dias (10000 replicas, semilla 20261107, 42 dias): -0.704 y 0.010; replicas descartadas: 0
d) perdida diaria maxima, por cuenta: 2.29 % del capital inicial; la peor, la cuenta de 2026-08
e) equity minima, por cuenta: 95.93 % del capital inicial; la peor, la cuenta de 2026-08
f) alguna cuenta entro en SUSPENDIDA: no
