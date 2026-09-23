# A-18 en las transcripciones: ningún pasaje responde, y se pregunta al trader

Rama `trabajo/a18-transcripciones`, 2026-09-23. Es el punto 14 de Next Action. Sin merge, sin tag
y sin push.

## 1. El alcance

- **Entran las cinco transcripciones vigentes de v1 a v5**, del modelo `large-v3-int8-float16`.
  Solo se lee la cruda, y antes se verifica contra el `sha256_cruda` de su manifiesto.
- **Queda fuera la de v6.** Se grabó en un día reservado (ADR-0037), y su lectura previa se
  declara como exposición posible en `HOLDOUT-EXPOSICIONES.md`.
- **Quedan fuera las 7 heredadas de `_procesado/`.** No tienen fecha declarada en su fila del
  manifiesto, y son el ASR pequeño (ADR-0007).
- **Quedan fuera las cinco sustituidas.** A cada una la sustituye su vigente (`reemplaza_a`).

## 2. El camino, citado por commit

- **Criterio congelado antes de buscar:** `cdcf58e`. Está en `A18-TRANSCRIPCIONES-CRITERIO.md` y
  `scripts/a18_buscar.py`, con su test sobre una transcripción sintética. Fija la regla literal
  del punto 14, 36 términos en lista cerrada y una ventana de ±45 s que se une si se solapa.
- **Salida de una sola ejecución:** `019ed47`, en `A18-TRANSCRIPCIONES-SALIDA.txt`. Tiene 42
  pasajes: 5 de v1, 8 de v2, 9 de v3, 19 de v4 y 1 de v5.
- **Control positivo, antes de clasificar.** Las tres frases ya conocidas de v5 están en la salida:
  - «SL por defecto», en el segmento #47;
  - «protejo a 0.80», que en la cruda queda partida entre #46 y #47;
  - «el cálculo del RR en base al 1%», en #59.
- **Clasificación:** `468ec59`, en `A18-TRANSCRIPCIONES-CLASIFICACION.md`, con una fila por
  pasaje y la frase literal que la decide.

## 3. La regla, aplicada

| clase | pasajes |
|---|---|
| responde → riesgo_real | 0 |
| responde → caja_completa | 0 |
| no responde | 42 (11 con duda) |

La regla congelada dice: *«Si hay pasajes en sentidos opuestos, o ninguno responde, se pregunta al
trader con la pregunta abierta de `docs/validation/V5-INSTANTES.md`.»*

**Ninguno responde, así que se pregunta al trader** con la pregunta de reserva de
`V5-INSTANTES.md`. **La búsqueda en las transcripciones queda cerrada.** Aplicó la regla el
consultor.

## 4. Las 11 dudas, SIN resolver

**Son INFERENCIAS de esta sesión, no frases del trader.** Ninguna dice por sí misma dónde va el
stop respecto a la caja ni cómo se calcula el TP. La dirección de cada una es la que anotó la
clasificación, y queda sin decidir.

| pasaje | transcripción | dirección anotada | por qué es duda |
|---|---|---|---|
| 1 | v1 | caja_completa | «perderíamos menos un 0.75» y el 1:3 en la misma unidad; es inferencia entre frases, con deícticos |
| 2 | v1 | ninguna | stop protegido a 0,75 al generarse la entrada; el 1:3 sin base |
| 3 | v1 | ninguna | el stop que usa es 0,75 y el 1 es la alternativa; no habla del TP |
| 10 | v2 | caja_completa | el lote se calcula antes de proteger y el 0,25 guardado «se agrega» al 3; «desde aquí» es deíctico y el stop que queda es 0,75 |
| 15 | v3 | caja_completa | ganadas de cerca de 3 y perdidas de 0,75 en la misma unidad; es una cuenta de resultados, no la regla |
| 18 | v3 | caja_completa | el lote se calcula sobre la caja entera, y el 1:3 medido «hasta el mismo nivel» desde el stop protegido daría 3,5; el 1:3 va con deícticos |
| 19 | v3 | ninguna | «dejado en 0.75» y el 1:3, sin base |
| 25 | v4 | ninguna | stop a 0,75; el «0.80» es un margen por spread que pregunta el interlocutor |
| 26 | v4 | choca con el 18 | se acuerda calcular el lote al 0,75, no a la caja entera; no habla del TP; la cruda no dice quién habla |
| 39 | v4 | caja_completa | la misma cuenta que el 15 (3 por cada 1 %, pérdidas de 0,75); resultados, no la regla |
| 42 | v5 | riesgo_real, si el 0,80 es el stop inicial | «el SL por defecto» a 0,80; si «protejo» es el movimiento al activarse la entrada, vale para las dos |

## 5. Observación descriptiva, que no decide nada

- **El stop en dos tiempos.** En v1 a v4 el trader describe el stop así: el lote se calcula sobre
  la caja entera, y el stop se protege a 0,75 al activarse la entrada.
- **La fecha del material.** Todo es anterior al lineamiento del 9 de septiembre, que fija el stop
  a 0,8.
- **Lo que suponen las hipótesis.** Las dos hipótesis de A-18, `(riesgo_real, 0,8)` y
  `(caja_completa, 1,0)`, suponen un solo stop.
- **Así que puede que A-18 esté mal planteada.** Se decidirá con la respuesta del trader.

## 6. El error del consultor

El brief del paso 0 usó «material de septiembre» como fecha de grabación. Tomado así, dejaba fuera
v5 y chocaba con su propio punto c), que metía los pasajes de v5 en la búsqueda. En el proyecto,
«material de septiembre» es el backtest de septiembre del trader, y así lo fijó el consultor antes
del criterio. El error de redacción es del consultor, y lo dice él.

## 7. Lo que deja la rama en el registro de exposiciones

- **La lectura previa de la transcripción de v6**, declarada como exposición POSIBLE y no
  verificada (`82039dd`).
- **El desliz de `cdcf58e`.** Ese commit escribió en `PROJECT_STATE.md` la fecha de grabación de
  v6 junto a «día reservado», así que la identidad de ese día queda en el historial de git. Se
  declara en su propio commit.

Las dos refuerzan la decisión pendiente, que va en su propia rama y antes de usar el holdout:
**retirar o no ese día del holdout**.

## 8. Cierre

Cada commit de la rama se hizo solo con `make check` en verde, y con el log borrado.
- Guardia de ids OK.
- `kit check --sesion 2026-09-09-sesion-01` idéntico a la línea base.
- PREREGISTRO con blob `52649183…`.
- Cero autorizaciones.

**Un tropiezo, dicho.** El primer intento del commit de criterio no se hizo. La comprobación del
recuento de tests buscaba mal el texto, así que se volvió a ejecutar entera antes de commitear.
Ningún commit se hizo en rojo.

## Estado

WAITING_FOR_USER_VALIDATION
