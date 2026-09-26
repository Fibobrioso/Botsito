# Ticks, modelo de llenado y bróker simulado

Rama `trabajo/ticks-llenado`, noche del 2026-09-26 y la mañana siguiente, en dos sesiones
autónomas: la primera cortada por el límite de uso a la 01:35, la segunda retomada desde el
registro vivo `docs/validation/NOCHE-TICKS-BROKER.md`, que conserva el detalle de cada fase. Sin
merge, sin tag y sin push: el cierre lo decide Aleks. Dos ADR nuevos, los dos PROPUESTOS
(ADR-0051, el modelo de llenado; ADR-0052, el bróker simulado): los acepta o corrige el consultor.

Guardas: `PREREGISTRO.md` con blob `52649183…`, cero autorizaciones en el holdout; solo abril y
agosto de 2026 en todo lo descargado y ejecutado, y la CLI de ticks SE NIEGA a cualquier otro mes
(test); mayo, marzo, febrero y septiembre ni se descargaron ni se ejecutaron; la spec,
`ambiguedades.yaml` y el motor de reglas, sin tocar; ningún `--no-verify`; `kit check` y
`fidelidad check` idénticos byte a byte antes y después de descargar.

## Resumen por fase

| fase | estado | dónde |
|---|---|---|
| 0 · comisión conservadora | HECHA | `knowledge/cuentas/ftmo-2step-swing-100k.yaml`: `firma_comision_por_lado` CONFIRMED `true` (decisión del consultor del 2026-09-25, pendiente de FTMO); recuadro en `SIMULADOR-CUENTA.md` |
| 1 · ADR del modelo de llenado | HECHA | ADR-0051, PROPUESTO |
| 2 · ticks de construcción | HECHA, con selección (DN-5) | `data/manifests/ticks/`: abril 182 de 189 horas, agosto 186 de 189; integridad 100 % de las M1 con ticks; spread medido; `knowledge/simulador/llenado.yaml` |
| 3 · modelo de llenado en código | HECHA | `engine/llenado.py`, `engine/simulador_config.py`, 9 + 12 tests |
| 4 · bróker simulado | HECHA | ADR-0052, PROPUESTO; `engine/broker.py`, 9 tests |
| 5 · punta a punta sintética | HECHA | `engine/simulacion.py`; estrategia de juguete en `tests/unit/test_simulacion.py`, 6 tests |
| 6 · repetición descriptiva del trader | HECHA, con ticks (DN-8) | `scripts/repeticion_trader.py` → `REPETICION-TRADER-SALIDA.txt` |
| 7 · instante con ticks | HECHA | `scripts/instante_ticks.py` → `INSTANTE-TICKS-SALIDA.txt` |

**Qué hay ahora que no había.** El simulador tiene sus dos mitades: la capa de cuenta (ADR-0050)
y el bróker (ADR-0052) con el modelo de llenado (ADR-0051) detrás, unidos en `simular_fase` con
la cuenta persistiendo entre días. Una estrategia de juguete recorre todo el camino —mercado,
órdenes, llenado con ticks o respaldo M1, cargos, marcas, veredicto FTMO— con tests de
determinismo, de no mirar al futuro, de suspensión en el instante exacto y de fase EN_CURSO por
días mínimos. El motor de reglas sigue sin enchufar: el contrato que tendrá que cumplir está en
ADR-0052 §5 y en `simulacion.Estrategia`.

## Decisiones nocturnas, todas, con sus alternativas

- **DN-0 (proceso).** La guardia de ADR solo admite `status: ACTIVE|SUPERSEDED`; los ADR
  PROPUESTOS llevan `ACTIVE` en el campo y PROPUESTO en el título, el Estado y los índices.
  Alternativa: cambiar la guardia; no de noche.
- **DN-1 (ADR-0051 §1, conservadora).** Las límites y los objetivos exigen que el precio pase
  ESTRICTAMENTE su nivel; los stops saltan al toque. Alternativa: llenar al toque los tres, como
  un tester de MT5 (es un booleano de `llenado.yaml`).
- **DN-2 (ADR-0051 §3).** Un tick que cruza stop y objetivo a la vez es stop, al precio del tick.
- **DN-3 (ADR-0051 §4).** Sin deslizamiento fijo (no hay medida; ADR-0002); el de hueco lo dan
  los ticks. Alternativa: una cifra inventada.
- **DN-4 (ADR-0051 §6, conservadora).** El spread supuesto sin ticks es el percentil 90 por hora
  local, medido. Alternativa: la media.
- **DN-5 (Fase 2).** Los ticks se congelan solo para los días dev de construcción y las horas
  05-13 UTC (la ventana 07:00-15:00 CEST más una hora), con la selección escrita en el
  manifiesto, porque el servidor no da un mes entero en una noche (medido: de 2 s a más de un
  minuto por hora, con 503 y conexiones rechazadas). Alternativas: el mes entero (otro dataset,
  con el mismo comando sin `--solo-dias-dev`); solo los minutos de las operaciones.
- **DN-6 (ADR-0052 §3, conservadora).** El swap se cobra en cada medianoche del huso del perfil
  (CE(S)T), porque el reloj del servidor no tiene calendario publicado (A-28). Alternativas:
  00:00 UTC; no modelar swaps.
- **DN-7 (proceso).** En ADR-0051 se quitó el bloque `ids-inexistentes` que declaraba a ADR-0052,
  porque la guardia falla cuando el id pasa a existir. Único cambio a un ADR PROPUESTO; no toca su
  contenido.
- **DN-8 (Fase 6).** La salida de cada operación del trader se repite con la regla de la spec
  (stop del caso, objetivo por `objetivo_rr`, cierre forzoso a fin de ventana), porque el caso no
  trae la salida real, y se declara como reconstrucción por regla. El lote sale de una rejilla
  hipotética de riesgo. Alternativas: cerrar la fase sin cifras; leer la salida del libro, que
  ADR-0037 deja fuera.

## Integridad de los ticks y spread medido

**Datasets** (`data/manifests/ticks/`, inmutables, verificados con `check-ticks --hashes`):
`eurusd-ticks-2026-04-1d189bdd` (21 días dev, horas 05-13 UTC, 182 de 189 horas presentes, 7
perdidas tras dos pasadas, 687.585 ticks) y `eurusd-ticks-2026-08-75bd3a08` (21 días, 186 de 189,
3 perdidas, 484.035 ticks). Las horas perdidas están listadas en cada manifiesto; el modelo de
llenado las cubre con el respaldo M1 y lo marca. Los dos datasets de la primera pasada se
descartaron sin comitear (28 horas perdidas cada uno; el de abril, además, incoherente por un
borrado mío a mitad de descarga; el descargador recrea ahora la carpeta antes de cada día).

**Integridad, tolerancia fijada antes de comparar** (|ΔO|, |ΔH|, |ΔL|, |ΔC| ≤ 2 puntos, volumen
sin comparar; `TICKS-INTEGRIDAD-SALIDA.txt`): de las M1 del repo cuyo minuto tiene ticks
**cuadran el 100 %** (22.075 de 22.075; abril 10.915, agosto 11.160), ninguna discrepa; las 39.731
M1 restantes están fuera de la selección o en las 10 horas perdidas; ningún minuto con ticks
carece de M1 en el repo. La tolerancia no se tocó.

**Spread** (`TICKS-SPREAD-SALIDA.txt`, ASK − BID en puntos de 0,00001, por hora local del trader):
media 2,8-3,4 según la hora, p50 3, **p90 5** de 07 a 11 y a las 14, **4** a las 12 y 13, p99 5-8;
fuera de la ventana p90 4; un máximo aislado de 121 a las 14:00 de abril. `llenado.yaml` lleva el
p90 por hora con su fuente.

## Fases 6 y 7

**Fase 6, repetición descriptiva** (perfil FTMO 2-Step Swing 100k, fase `reto`, con ticks; el
detalle en `REPETICION-TRADER-SALIDA.txt` y en el registro): al 0,25 % de riesgo por operación,
abril queda EN_CURSO con pérdida diaria máxima 3,89 % y total 6,29 % (35 operaciones, 16 días);
agosto EN_CURSO con 1,29 % y 3,46 % (42 operaciones, 19 días). Al 0,5 %, EN_CURSO los dos (5,42
y 6,92 % de pérdida total máxima). Al 2 %, abril SUSPENDIDA el 2026-04-13 a las 12:03:59Z por
pérdida diaria (5,06 %). Con riesgo alto y stops cortos el lote supera `firma_volumen_max_lotes`
y la operación no entra (hasta 31 rechazadas de 42), así que esos escenarios quedan más benignos
de lo que serían: la cifra que vale es la de 0,25-0,5 %. **Ticks frente a respaldo M1: el
desenlace cambia en 12 de 35 operaciones de abril y 18 de 42 de agosto** (30-43 %): el respaldo
pesimista da stop donde los ticks dan objetivo. Es la medida de cuánto pesa no tener ticks. Todo
esto es «qué habría pasado en la cuenta si el trader hubiera salido por la regla de la spec»,
no lo que le pasó al trader; no cambia ningún ADR, parámetro ni spec.

**Fase 7, instante con ticks** (`INSTANTE-TICKS-SALIDA.txt`): de las 77 operaciones dev, 75 con
ticks en su minuto; **el precio de entrada se toca dentro del minuto del xlsx en 75 de 75**;
control −30 min 7,4 %, +30 min 14,9 %: cae claramente. Distancia al primer toque: mediana −2,4 s
(de −51,4 a +6,5); en 43 de 75 el primer toque es en el mismo segundo o antes, lo que se espera
de un instante de LLENADO. Coincide con la medida M1 (98,9 %, controles 5,3 y 12,8 %). Y en 31 de
75 la M1 del minuto cubre entrada y stop a la vez sin decir cuál se tocó antes; los ticks lo dicen
en las 31.

## Paradas

- Corte por límite de uso a la 01:35, con el árbol estadiado; resuelto en la segunda sesión.
- La descarga se paró de noche por conexiones rechazadas; el proceso desacoplado terminó solo y
  una segunda pasada recuperó casi todas las horas. No hubo ninguna parada por contradicción con
  un ADR, riesgo para el holdout ni cambio del kit o de fidelidad.

## Lo que decide el consultor

Los dos ADR PROPUESTOS y las ocho decisiones nocturnas; si el mes entero de ticks se descarga de
día (otro dataset, mismo comando); y si el modelo de llenado pasa a llenar al toque
(`limite_llena_al_toque`). El cableado del motor de reglas al bróker es la siguiente rama, con el
contrato de ADR-0052 §5 y los huecos de ADR-0050 §5.

## Estado

WAITING_FOR_USER_VALIDATION.
