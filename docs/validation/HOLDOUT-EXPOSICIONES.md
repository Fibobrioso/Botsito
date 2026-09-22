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
| 2026-09-20 | **La columna de fechas del xlsx del backtest de SEPTIEMBRE 2026** (`backtesting-analytics SEPTIEMBRE 2026.xlsx`, entregado ese dia por WhatsApp junto a seis capturas de las 06:03 que por el patron son de la pestana Analytics), abierto en Excel para saber QUE DIAS CUBRE EL MATERIAL: del 1 al 18 de septiembre. El consultor declara que NO miro resultados, ni PnL, ni el detalle por operacion, ni ninguna captura. **No hay prueba mecanica de que la pantalla solo renderizara esa columna**: Excel pinta la hoja activa entera. El unico rastro que queda en el directorio es el fichero de bloqueo `~$backtesting-analytics SEPTIEMBRE 2026.xlsx` (2026-09-20 14:51), que prueba la apertura y nada mas sobre que se vio. Tampoco consta si se retuvo la lista dia a dia o solo el rango: lo declarado es el RANGO | **Ninguna todavia, y todas las que nazcan.** El 2026-09-20 septiembre no tiene particiones: ni un `caso-eurusd-2026-09-*` en `particiones.yaml` -solo mayo y junio-, ningun dataset `eurusd-m1-2026-09` en `data/manifests/` y CERO registros `LABEL_CASE` en todo el repositorio. La exposicion es ANTERIOR al sorteo, asi que alcanza a lo que se sortee | el consultor, el 2026-09-20, al recibir el material (rama `trabajo/septiembre-entra`) | **NO** (ADR-0021 §1, con el precedente del 2026-09-13): saber que dias cubre un fichero no es leer una etiqueta ni medir una cifra del bot, igual que no lo es leer velas para fijar un universo; y no hay particion que quemar. **Con la reserva del 2026-09-12**: un dia laborable del 1 al 18 que NO aparezca en esa columna seria un dia sin operaciones, y eso ES su etiqueta. Como no consta si la columna se vio dia a dia o solo su rango, no se puede nombrar ninguno -nombrarlo exigiria abrir el fichero-, asi que F26 excluye de cualquier cifra de septiembre los dias sin operaciones, por anticipado y en bloque, igual que excluye 2026-05-14. **Se declara ademas que esta lectura cruzo `CLAUDE.md`**, que desde el 2026-09-17 ponia el backtest de septiembre entero fuera de alcance "hasta que sus particiones esten sorteadas y commiteadas": no se abrio ningun holdout, pero la regla escrita era mas ancha que ADR-0021 §1 y se rompio |
| 2026-09-21 | **El xlsx del backtest de AGOSTO 2026 entero** (`backtesting-analytics AGOSTO 2026.xlsx`), en TRES pasadas el mismo dia: la primera para aprender el FORMATO del libro antes de escribir la ingesta de F14a -miembros del zip, serializacion de texto, pestanas, las 22 cabeceras y la forma de las celdas-; la segunda para decidir POR MEDIDA cual de las dos columnas candidatas es el objetivo (`maxTP` frente a `idealTP`) y en que huso viene `dateStart`, y ahi si se miraron `status`, `rPnL` y las columnas de RR; la tercera, a peticion del consultor, para sacar la DISTRIBUCION ENTERA del RR realizado de las 18 filas con `maxTP` e `initialSL`, que es la primera medida que A-18 ha tenido nunca (ninguna columna nueva: `entryPrice`, `initialSL`, `maxTP` y `side`, las mismas de la segunda). **NO es una exposicion de holdout**: agosto no tiene NI UN DIA en ninguna particion -comprobado ANTES de abrir con `casos_reservados(repo)`: 34 claves, ninguna de `2026-08`- y es material de DESARROLLO, no de holdout (§ de este mismo fichero: la spec se infirio en parte de esos dias, asi que medir fidelidad sobre ellos seria circular). Se declara igual, y el motivo es que dentro de seis meses alguien vera que se abrio y va a querer saber por que; declarar de mas no cuesta nada | **ninguna** | la sesion, con autorizacion del consultor del 2026-09-21 y despues de corregir `CLAUDE.md` §3 y escribir ADR-0037 | **NO**: ningun dia de agosto esta repartido, asi que no hay particion que quemar. Enero y abril quedan sin abrir: con uno se aprende el formato |

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
7. **Septiembre se sortea con el universo de las VELAS, no con lo que diga el xlsx**, y sus
   particiones se commitean ANTES de que exista ninguna etiqueta de septiembre. La cobertura del
   material (1-18) solo acota que dias pueden entrar; ninguna asignacion depende del contenido del
   fichero. Y **los dias del 1 al 18 sin operaciones no se miden**, sean cuales sean: misma regla
   que 2026-05-14 (punto 4), declarada por anticipado porque aqui no se pueden nombrar.
8. **El detalle por operacion del xlsx de SEPTIEMBRE y sus seis capturas son material de holdout**
   para los dias que el sorteo reserve, exactamente como el punto 3 dice de mayo. El fichero de
   bloqueo `~$*.xlsx` no es material: no entra en el inventario ni en ningun manifiesto, y Excel se
   cierra antes de inventariar, porque un libro abierto puede cambiar de bytes y con ellos su hash.
9. **Que septiembre haya llegado NO cierra el punto 5.** Sigue pendiente pedirle al trader un mes
   que no haya tocado: septiembre lo backtesteo el, asi que no es material ciego. Sirve para medir
   fidelidad con las particiones fijadas antes de leer una etiqueta, que es otra cosa.
