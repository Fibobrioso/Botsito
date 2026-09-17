# Exposiciones de holdout

Registro de todo lo que se ha visto de una particion reservada, aunque fuera de pasada. Lo exige
ADR-0021: una exposicion no siempre quema, pero **siempre se declara**, el mismo dia, y F26 la cita
en su informe. Una cifra de fidelidad que no mencione lo que sabia quien la produjo no se puede
defender.

Qué es cada cosa, en corto (la definicion completa esta en ADR-0021 y en
`knowledge/cases/holdout/README.md`):

- **Abrir** = leer las etiquetas de esos dias, o medir cualquier cifra del bot sobre ellos. Quema.
- **Exponerse** = ver un resultado agregado de esos dias sin ninguna decision dentro. No quema, se
  declara.

| Fecha | Que se vio | Particiones | Quien | ¿Quema? |
|---|---|---|---|---|
| 2026-09-11 | El calendario de PnL **dia a dia de todo mayo de 2026** (4 may +30 $ … 29 may −118 $), en una de las siete capturas de la pestana Analytics de FX Replay que el trader entrego con el backtest del mes. Tambien el agregado del mes: 68 operaciones, 18 ganadoras / 33 perdedoras / 17 en break even, win rate 35,29 %, RR medio 3,45, profit factor 2,14, +650 $ sobre 100 000 | `holdout-1` (6 dias), `holdout-2` (4), `holdout-3` (3) — los trece de mayo | la sesion de trabajo que proceso el material (consultor + agente) | **NO** (ADR-0021 §5): no se vio ninguna decision -ni hora, ni direccion, ni entrada, ni stop- y un PnL diario no se puede invertir para deducirlas |
| 2026-09-12 | El **recuento de operaciones por dia** de los 19 dias de mayo que trae el xlsx del trader (entre 1 y 7 por dia), visto al listar las fechas de los cuatro backtests para decidir el universo de F14; y, dentro de ese recuento, que **2026-05-14 no tiene ninguna operacion**. Tambien los recuentos de relleno por columna del mes entero (`initialSL` 62/68, `avgRiskReward` 62/68, `maxTP` 18/68, `tags` 0/68). NO se vio ninguna hora, direccion, entrada, stop ni objetivo de un dia reservado | `holdout-1` (6), `holdout-2` (4), `holdout-3` (3) | la revision de diseno de F14 (agente), por encargo del consultor | **PARCIAL**: los recuentos NO queman (ADR-0021 §2: son agregados sin ninguna decision dentro). Pero **un dia sin ninguna operacion ES su etiqueta**: saber que 2026-05-14 es `no_trade` entero es saber su decision, y eso ADR-0021 §1 lo llama ABRIR. **Ese dia, y solo ese, queda QUEMADO** |
| 2026-09-12 | Los AGREGADOS DEL MES de mayo que traen las capturas de Analytics, al clasificarlas en la auditoria de material: Max RR 4,47; Ideal Average RR 15,03 (max 47,5); could-have-profit 3; expectancy 9,56 $ (+17,96 / -8,40); ganadoras mejor 0,2 %, media 0,07 %, duracion 18 min, racha maxima 4; perdedoras peor -0,05 %, media -0,02 %, duracion 4 min, racha maxima 8; lado 51,5 % compra / 48,5 % venta; frecuencia 3,67/dia; histograma horario 05:00-12:00 UTC. Y la RE-EXPOSICION al calendario diario: se vio que dos capturas LO SON, sin leer ni transcribir ninguna celda | `holdout-1` (6), `holdout-2` (4), `holdout-3` (3) | la auditoria de material del 2026-09-12 (agente), por encargo del consultor | **NO** (ADR-0021 §5): son cifras del MES entero, ninguna atada a un dia. La re-exposicion al calendario es la misma ya declarada el 2026-09-11 |
| 2026-09-13 | **Dos ejecuciones de `kit check --sesion 2026-09-09-sesion-01` sobre el repositorio original con `data/` presente**, durante la auditoria ultracode (`AUDITORIA-2026-09-13-ultracode.md` §1, parrafo de exposiciones, y §6.8): un intento anterior de la dimension `exec-cli`, y otra de `d7-metodo` por mandato explicito de su tarea. Con datos, `kit check` llama a `construir()` (`cases/paquete.py`), que recorre el universo de ventanas de MAYO Y JUNIO de 2026 leyendo las velas M1 de Dukascopy de cada dia para recalcular `n_velas`, el `sha256` del CSV canonico y los limites H4 -limites de TIEMPO por anclaje, no precios- (`cases/ventanas.py`), regenera los cuatro ficheros del paquete y los compara con los commiteados. La salida mostro solo dos AVISO (`cuestionario.yaml` y `hoja_trader.md`, esperados en una sesion celebrada) y el OK, las dos veces. NO se vio ni se transcribio ningun precio, ningun hash ni ningun recuento de velas; no se leyo ninguna etiqueta ni ningun detalle del backtest; no se midio ninguna cifra del bot. Las escrituras de esa auditoria (commits de prueba, `evidence new`) fueron en clones sin `data/` | Los 24 dias de holdout del paquete: los 13 de mayo -`holdout-1` (6), `holdout-2` (4), `holdout-3` (3)- y ademas los 11 de JUNIO -`holdout-1` (2), `holdout-2` (4), `holdout-3` (5)-, junio descartado del universo de F14 pero asignado en `particiones.yaml`. Tambien los 16 `dev` | los agentes `exec-cli` y `d7-metodo` de la auditoria ultracode, por encargo del consultor. Declarada el 2026-09-17, cuatro dias tarde, contra ADR-0021 §4 | **NO** (ADR-0021 §1 y §2): leer velas de mercado para recalcular hashes no es leer una etiqueta ni medir una cifra del bot, y ni siquiera se vio un agregado -solo que los ficheros regenerados coincidian-. Se declara igual porque es acceso a datos de dias reservados, y porque el resumen que circulaba ("un agente, velas de mayo") se quedaba corto: fueron dos ejecuciones y tambien dias de junio |

## Lo que esto obliga

1. **F26 cita esta tabla** en su informe de fidelidad, junto al pre-registro de umbrales. Sin esa
   frase, la cifra sobre `holdout-1` no es defendible.
2. **`holdout-1` sigue reservado** para la nota, intacto. `holdout-2` es la segunda oportunidad si
   hay que corregir y volver a medir; `holdout-3`, la de la fase final.
3. **El detalle por operacion del backtest de mayo** (el xlsx: ticket, precios, R por operacion) es
   material de holdout para los trece dias reservados: no se abre sin autorizacion del usuario y
   sin `PREREGISTRO.md` commiteado antes.
4. **2026-05-14 no se mide.** Sigue escrito en `particiones.yaml` como `holdout-2` -ese fichero
   no se reescribe: es la prueba de que las particiones se fijaron antes de etiquetar, y ADR-0025
   acaba de negarse a tocarlo por menos que esto- pero F26 tiene que EXCLUIRLO de cualquier cifra
   que mida sobre `holdout-2`, que se queda en 3 dias medibles. Declarar y excluir cuesta un dia;
   reescribir el reparto costaria la prueba entera.
5. **Pendiente, y la revision de diseno de F14 lo confirmo**: pedirle al trader un mes que no haya
   tocado. No es redundante aunque el corpus tenga otros tres backtests suyos (enero, abril,
   agosto): esos tres meses son material de DESARROLLO y no de holdout, porque **la spec se
   infirio en parte de esos mismos dias** -v4, el video en el que recorre enero en pantalla, aporta
   130 de los 353 items de evidencia-. Medir fidelidad sobre los dias de los que salieron las
   reglas es circular. Mayo sigue siendo el unico material ciego que existe.
6. **Leer las velas de un dia reservado no es abrirlo; abrirlo exige autorizacion, y la CLI declara
   lo que lee.** (Reescrita el 2026-09-17, ADR-0033. La redaccion anterior prohibia ejecutar
   `kit check` y `kit build` con `data/` presente, y tomada al pie de la letra impedia construir el
   paquete de la sesion 2 para siempre.)
   - **Leer velas para recalcular una ventana no es abrir** (ADR-0021 §1). Y el paquete no se puede
     construir sin hacerlo: `universo()` (`src/botsito/cases/ventanas.py`) lee el mes entero de cada
     dataset y descarta los dias con menos de `min_velas`, y que dias son reservados depende de
     cuales entran. Las ventanas de los dias reservados son la prueba de que las particiones se
     fijaron antes de etiquetar.
   - **Lo prohibido sin autorizacion del usuario y sin pre-registro es ABRIR**: las etiquetas
     (`LABEL_CASE`) y el detalle por operacion de esos dias (ADR-0021 §1 y §3). Todo lo que abre pasa
     por `botsito.cases.holdout` (`src/botsito/cases/holdout.py`), que se niega sin
     `docs/validation/PREREGISTRO.md` commiteado y relleno y sin
     `docs/validation/AUTORIZACION-<particion>.md` commiteado, que fija con `preregistro_blob` el
     pre-registro exacto que aprueba. `kit kappa` excluye las etiquetas de
     los casos reservados sin leerlas, y lo dice.
   - **Lo que faltaba, y ya esta**: que `kit build` y `kit check` lo declaren en su salida -lineas
     `LECTURA:` con los datasets y CUANTOS dias reservados se leen por particion, sin fechas, sin
     cifras de velas y sin precios-; y que la guarda de `tests/conftest.py` deje de ser un stub y vigile a cualquier
     llamante, no solo a `spec` y `domain`.
   - **La fila del 2026-09-13 no cambia**: lo que paso sigue siendo lo que paso, y sigue sin quemar.
     Lo que cambia es que ya no pasaria en silencio.
