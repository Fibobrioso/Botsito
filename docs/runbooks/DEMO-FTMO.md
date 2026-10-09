# La medida en la demo de FTMO

Para Aleks. Un script de MetaTrader 5 mide en la cuenta de **prueba gratuita** de FTMO lo que el
simulador todavía supone: qué hace el servidor con una orden mal colocada, el stops level, la
comisión y el reloj del servidor (ADR-0057, A-27, A-28 y `docs/validation/FTMO-REGLAS.md`). Tú lo
ejecutas tres veces; el repositorio lee lo que sale. **No cambia nada de la estrategia ni de los
parámetros**: los valores entran después, en otra rama, con los ficheros delante.

El script es `tools/mql5/MedirDemoFTMO.mq5`. Tarda menos de un minuto si la orden del paso 7 salta
enseguida (44 segundos en la ejecución 1, el 2026-10-09) y como mucho unos tres si no salta: el paso 7
la espera hasta 120 segundos.

## Lo que hace, y lo que no hace nunca

- **Se niega a correr si la cuenta no es de prueba (DEMO).** En una cuenta real no hace nada.
- Solo toca **EURUSD**, con el **lote mínimo** (0,01 si no dice otra cosa la cuenta), salvo el
  paso 6: desde la versión 1.1 abre y cierra enseguida una compra de **1,00 lote**, con su stop de
  protección, para medir la comisión por lote (ADR-0071 §3). Antes de abrir comprueba el margen
  libre; si no alcanza, no abre y lo escribe en el fichero.
- Pone unas veinte órdenes de prueba y **las borra todas**; abre como mucho unas pocas posiciones
  pequeñas (y, desde la 1.1, la de 1,00 lote del paso 6) y **las cierra**.
  Toda orden de prueba caduca sola a los 15 minutos, y toda posición lleva un stop de protección.
- Al empezar y al terminar busca cualquier orden o posición suya que siga abierta y la quita. Si
  algo se quedara abierto, sale un aviso en pantalla y queda escrito en el fichero.

## Una vez: la cuenta y MetaTrader

1. **La cuenta de prueba.** Entra en ftmo.com, pulsa *Free Trial* y regístrate. Si te deja
   elegir, pide **MetaTrader 5**, **Swing** y **100.000 USD**, como la cuenta de verdad. Al
   terminar, en tu área de cliente (*Client Area*) verás tres datos de la cuenta: **login**,
   **contraseña** y **servidor**. Apúntalos.
2. **MetaTrader 5.** En este ordenador ya está instalado. Si no lo estuviera, se descarga desde el
   área de cliente de FTMO o desde metatrader5.com, y se instala con las opciones por defecto.
3. **Entrar en la cuenta.** Abre MetaTrader 5. Menú **Archivo → Iniciar sesión en la cuenta de
   trading** (en inglés, *File → Login to Trade Account*). Escribe el login, la contraseña y elige el servidor de FTMO que te dieron. Abajo a
   la derecha tiene que aparecer una conexión en verde con unos números (kb).
4. **Copiar el script.** Menú **Archivo → Abrir carpeta de datos** (*File → Open Data Folder*). Se abre una carpeta de Windows:
   entra en **MQL5**, luego en **Scripts**, y copia ahí el fichero
   `tools/mql5/MedirDemoFTMO.mq5` del repositorio.
5. **Compilarlo.** En MetaTrader pulsa **F4**: se abre MetaEditor. A la izquierda, en *Scripts*,
   haz doble clic en **MedirDemoFTMO.mq5** y pulsa **F7**. Abajo tiene que decir **0 errors**.
   Cierra MetaEditor.

## Cada vez: ejecutarlo

1. **Mercado abierto**, de lunes a viernes, entre las **9:00 y las 18:00 hora de España** (Londres
   o Nueva York abiertos). Evita la hora exacta de una noticia importante.
2. Pulsa el botón **Algo Trading** de la barra de arriba hasta que se vea en verde. Sin él, el
   script se niega y te lo dice.
3. **Un gráfico de EURUSD.** Menú **Ver → Observación del mercado** (*View → Market Watch*); en la lista, clic derecho en
   **EURUSD → Ventana de gráfico**.
4. **Lanzarlo.** Menú **Ver → Navegador** (*View → Navigator*); despliega **Scripts**, arrastra **MedirDemoFTMO** encima
   del gráfico de EURUSD y pulsa **Aceptar** sin cambiar nada.
5. **Esperar** de uno a tres minutos, sin tocar nada, hasta que salga una ventana que diga
   **«MedirDemoFTMO: terminado (completo)»**.
6. **Comprobar.** Abajo, en la caja de herramientas (**Ctrl+T**), pestaña **Trading** (*Trade*), no
   tiene que quedar ninguna orden ni posición. Si la ventana dijera **«ATENCIÓN: quedan…»**, en esa pestaña clic derecho
   sobre cada una → **Cerrar** o **Eliminar**.
7. **Si se corta** (se va la conexión, cierras MetaTrader…): vuelve a lanzarlo. Lo primero que hace
   es limpiar lo que quedara de la vez anterior.

## Dónde queda el fichero y a dónde va

MetaTrader lo deja en **Archivo → Abrir carpeta de datos → MQL5 → Files**, con el nombre
`MedirDemoFTMO_AAAAMMDD_HHMMSS.csv` (la fecha y la hora del servidor). **No lo abras con Excel ni lo
renombres**: cópialo tal cual a la carpeta **`data/demo_ftmo/`** del repositorio (créala la primera
vez). Para ver la tabla:

    uv run python scripts/leer_demo_ftmo.py data/demo_ftmo

**Por qué ahí y no en `knowledge/`.** `data/` es donde el repositorio guarda los datos medidos en
bruto, fuera de git (`.gitignore`), como las velas y los ticks; lo que entra en git es su manifiesto
con el hash, en `data/manifests/`, que es inmutable. `knowledge/evidence/` no sirve: es para items
de evidencia del corpus con su esquema y su cita, no para ficheros de una plataforma. Cuando estén
los tres CSV, la rama que los use congela su hash en un manifiesto y, desde ahí, cambia los
parámetros con su fuente. El script no escribe el login de la cuenta: el fichero no lleva datos
personales.

## Cuándo: tres veces

| vez | cuándo | por qué |
|---|---|---|
| 1 | **esta semana**, y en cualquier caso antes del domingo **25 de octubre** | todo lo que no depende de la fecha, y el desfase del reloj en horario de verano |
| 2 | entre el **lunes 26 y el viernes 30 de octubre** | Europa ya cambió de hora (el 25) y Nueva York todavía no: el desfase dice qué calendario sigue el servidor (A-28) |
| 3 | después del **domingo 1 de noviembre** | Nueva York ya cambió: confirma el horario de invierno |

**Antes de la ejecución 2: el script 1.1.** La ejecución 1 (2026-10-09) usó la versión 1.0. Para la
2 hay una versión nueva, la 1.1 (rama `trabajo/demo-ejecucion-1`, ADR-0071), que mide la comisión
con 1,00 lote. Antes de lanzarla:
1. vuelve a copiar `tools/mql5/MedirDemoFTMO.mq5` del repositorio a **MQL5 → Scripts**, encima del
   que hay (paso 4 de «Una vez»);
2. compílalo otra vez: **F4**, doble clic en **MedirDemoFTMO.mq5**, **F7**, y abajo tiene que decir
   **0 errors** (paso 5 de «Una vez»);
3. ejecútalo como siempre, sin cambiar nada en la ventana de **Aceptar** (el volumen del paso 6 ya
   viene en 1,00);
4. al terminar, **comprueba que el fichero dice 1.1**: la primera columna de cada fila,
   `version_script`, tiene que ser `"1.1"`. El lector lo dice también: «(script 1.1)» junto al
   nombre del fichero. Si dice 1.0, el terminal sigue con la versión vieja: repite 1 y 2.

Si puedes, aprovecha una de las tres para mirar en el panel de la cuenta de FTMO **a qué hora se
recalcula el límite de pérdida diaria**: a medianoche de España o a medianoche del servidor (A-28,
«verificación explícita»). Apúntalo con la fecha.

## Lo que mide cada paso

| paso | qué | para qué |
|---|---|---|
| 1 | la ficha de EURUSD: stops level, freeze level, digits, point, contrato, lote mínimo, máximo y paso, modos de llenado, swaps y día del triple swap | A-27, ADR-0057 §5, FTMO-REGLAS R11 y R12 |
| 2 | la hora del servidor, la hora GMT y el desfase | A-28 |
| 3 | cuatro pendientes del lado equivocado: si se rechazan, se colocan o se llenan, y a qué precio | ADR-0057 d2, d3 y d4 |
| 4 | las cuatro pendientes en el nivel exacto, a la distancia del stops level y un punto dentro | ADR-0057 d2 y §5, A-27 |
| 5 | una pendiente buena, movida al lado equivocado: si se acepta y si la original sigue viva | ADR-0057 d3 |
| 6 | una compra y un cierre a mercado: la comisión de cada lado, el spread y el deslizamiento (con 1,00 lote desde la 1.1; la 1.0 usaba el lote mínimo) | FTMO-REGLAS R12, DN-3 |
| 7 | una buy stop muy cerca del precio: a qué precio se llena frente a su nivel | ADR-0057 d1 |

**Importante para leerlo:** la hora GMT sale del reloj de este ordenador. Si el ordenador no está en
hora, el desfase sale mal: comprueba que la hora de Windows está sincronizada antes de lanzarlo.

## La prueba de octubre de 2026

Lo que declara Aleks (fuente: Aleks, 2026-10-08; anotado en `trabajo/adelgazar-estado`). El número
de la cuenta no se escribe aquí: el repositorio es público.

- **La cuenta.** Prueba gratuita creada el 2026-10-08: 2-Step, Swing, USD, 100.000, MetaTrader 5,
  servidor FTMO-Demo. Vence hacia el 22 de octubre, así que la ejecución 1 va antes. El script se
  copió y se compiló con 0 errores el 2026-10-08.
- **La ejecución 1**, entre las 03:00 y las 08:00 hora de Lima, evitando las 07:30 de Lima. Medido
  con `zoneinfo` (America/Lima, UTC−5 sin cambio de hora, frente a Europe/Madrid, UTC+2 hasta el 25
  de octubre) para cualquier día anterior al 25 de octubre: **de 10:00 a 15:00 hora de España, y las
  07:30 de Lima son las 14:30 de España**. Cae dentro de la franja de 9:00 a 18:00 de «Cada vez:
  ejecutarlo» y dentro de la ventana del bot, de 07:00 a 15:00 Europe/Madrid (`ventana_inicio` y
  `ventana_fin`, `knowledge/spec/parametros.yaml`); las 08:00 de Lima son justo las 15:00, el
  final de esa ventana.
- **Netting o hedging: HEDGING en la prueba, medido.** La ejecución 1 (2026-10-09) da `modo_margen`
  = `ACCOUNT_MARGIN_MODE_RETAIL_HEDGING` (fila 25 del CSV, congelado en
  `data/manifests/demo_ftmo/demo-ftmo-2026-10-09-86f0df8b.yaml`), y Aleks declara que la barra de
  título de MT5 dice «Hedge»; lo de «Netting» que se anotó aquí el 2026-10-08 no casa con lo medido.
  Para el simulador no cambia nada: la estrategia nunca tiene dos posiciones a la vez
  (`docs/validation/DEMO-EJECUCION-1.md` §0.c). Si la cuenta Swing de verdad es también de hedging
  no se supone: es una pregunta para FTMO (la misma sección).
