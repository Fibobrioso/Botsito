# La medida en la demo de FTMO

Para Aleks. Un script de MetaTrader 5 mide en la cuenta de **prueba gratuita** de FTMO lo que el
simulador todavía supone: qué hace el servidor con una orden mal colocada, el stops level, la
comisión y el reloj del servidor (ADR-0057, A-27, A-28 y `docs/validation/FTMO-REGLAS.md`). Tú lo
ejecutas tres veces; el repositorio lee lo que sale. **No cambia nada de la estrategia ni de los
parámetros**: los valores entran después, en otra rama, con los ficheros delante.

El script es `tools/mql5/MedirDemoFTMO.mq5`. Tarda menos de un minuto si la orden del paso 7 salta
enseguida (44 segundos en la ejecución 1, el 2026-10-09) y como mucho unos tres si no salta: el paso 7
la espera hasta 120 segundos. **Desde la versión 1.2** (rama `trabajo/margen-pendiente`) el paso 8
añade de medio minuto a unos dos minutos y medio (su última medida espera hasta otros 120 segundos a
que salte una orden): en total, **como mucho unos seis minutos**.

## Lo que hace, y lo que no hace nunca

- **Se niega a correr si la cuenta no es de prueba (DEMO).** En una cuenta real no hace nada.
- Solo toca **EURUSD**, con el **lote mínimo** (0,01 si no dice otra cosa la cuenta), salvo en
  los pasos 6 y 8. En el 6, desde la versión 1.1, abre y cierra enseguida una compra de **1,00
  lote**, con su stop de protección, para medir la comisión por lote (ADR-0071 §3); antes de abrir
  comprueba el margen libre y, si no alcanza, no abre y lo escribe en el fichero. El 8, desde la
  1.2, usa lotes grandes (el punto siguiente).
- **Desde la versión 1.2, el paso 8 usa lotes GRANDES**, porque mide qué hace MetaTrader cuando no
  hay margen libre: órdenes pendientes de unos 15 a 27 lotes, lejos del precio (100 pips), que se
  borran en cuanto se leen, y, al final, una orden cerca del precio y otra orden o una compra que
  ocupan el margen (unos 28 a 30 lotes entre todas; las cifras, con unos 100.000 de margen libre).
  Las grandes llevan un stop de protección muy cercano (de 1,3 a 1,7 pips), y la pequeña de en medio
  (menos de un lote), uno de 20 pips; el script los calcula ANTES de enviar para que, aunque todo se llenara y fuera
  hasta su stop, no se pierdan más de **1.000 USD** (la quinta parte de la pérdida diaria máxima de
  FTMO), contando la comisión (5 USD por lote y lado en el script, el doble de los 2,50 medidos en
  las ejecuciones 2 y 3, ADR-0090: más caro, del lado seguro) y **un deslizamiento SUPUESTO de un pip por
  operación**. Ese pip no es una garantía: sale de tres medidas pequeñas de la ejecución 1 (de 1 y 2
  décimas de pip), y FTMO ejecuta a mercado, así que en un salto brusco del precio un stop puede
  llenarse más lejos y la pérdida pasar de esa cifra. Por eso las órdenes grandes viven unos
  segundos, y el script se lanza lejos de las noticias (paso 1 de «Cada vez»). Si el stop que sale
  es menor de un pip, esa medida no se hace y queda escrito en el fichero. Lo normal es no perder
  casi nada; si la orden cercana se llena, el script la cierra enseguida, y lo esperable es una
  pérdida de unos cientos de dólares como mucho.
- Pone unas veinte órdenes de prueba (y unas pocas más en el paso 8) y **las borra todas**; abre como
  mucho unas pocas posiciones pequeñas (y, desde la 1.1, la de 1,00 lote del paso 6; desde la 1.2, las
  del paso 8) y **las cierra**. Toda orden de prueba caduca sola a los 15 minutos. Las órdenes de los
  pasos 3, 4 y 5 van **sin stop a propósito** (solo se juzga su precio): si una se llena al instante,
  el script cierra la posición en cuanto la lee. Toda otra posición lleva un stop de protección.
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
   sobre cada una → **Cerrar** o **Eliminar**. **Con la 1.2, hazlo enseguida**: lo que quede del paso
   8 puede ser de muchos lotes; su stop de protección limita la pérdida, pero no hay que esperar a
   que salte. Después, mira que la pestaña quede vacía, copia el fichero como siempre y díselo a la
   sesión: en el fichero queda en qué medida pasó.
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
de evidencia del corpus con su esquema y su cita, no para ficheros de una plataforma. Los tres CSV
están congelados en `data/manifests/demo_ftmo/` (la 1 en `trabajo/demo-ejecucion-1`, la 2 y la 3 en
`trabajo/demo-ejecuciones-2-3`), y lo que fijan entró en los parámetros con su fuente (ADR-0071 y
ADR-0090). Los tres son CRLF: para contar retornos de carro en Git Bash hace falta `grep -U`, porque
sin `-U` el `grep` de Git para Windows los quita y cuenta 0 (ADR-0090, «La medida»). El script no escribe el login de la cuenta: el fichero no lleva datos
personales.

## Cuándo: tres veces

| vez | cuándo | por qué |
|---|---|---|
| 1 | **esta semana**, y en cualquier caso antes del domingo **25 de octubre** | todo lo que no depende de la fecha, y el desfase del reloj en horario de verano |
| 2 | entre el **lunes 26 y el viernes 30 de octubre** | Europa ya cambió de hora (el 25) y Nueva York todavía no: el desfase dice qué calendario sigue el servidor (A-28) |
| 3 | después del **domingo 1 de noviembre** | Nueva York ya cambió: confirma el horario de invierno |

**Las tres, hechas** (ADR-0071 y ADR-0090; horas comprobadas con `zoneinfo`):

| vez | cuándo (servidor) | España / Lima | script | prueba | lo que dio el reloj |
|---|---|---|---|---|---|
| 1 | 2026-10-09 15:35 | 14:35 / 07:35, dentro de la franja | 1.0 | la del 2026-10-08 | 180 min (los dos calendarios dan 180) |
| 2 | 2026-10-29 19:40 | 17:40 / 11:40, dentro de la franja | 1.1 | la del 2026-10-29 | 180 min: sigue a Nueva York (con Europa habría dado 120) |
| 3 | 2026-11-05 20:35 | 19:35 / 13:35, **fuera de la franja** de 9 a 18 de España | 1.2 | la del 2026-10-29 | 120 min: horario de invierno |

La 3 corrió con Nueva York abierto (13:35 EST) y Londres ya cerrado (18:35 GMT): la hora puede
afectar al spread, al deslizamiento y al llenado de los pasos 6 y 7, y no afecta al desfase, a la
comisión ni a la ficha. Con las tres, A-28 quedó DECIDIDA (el servidor va 120 minutos por delante de
UTC en invierno y cambia de hora con EE. UU.) y la comisión medida es 2,50 USD por lote y lado.
**No hay más ejecuciones previstas.**

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

**Antes de la ejecución 3: el script 1.2.** La 2 (2026-10-29) usó la 1.1. Para la 3 hay una versión
nueva, la 1.2 (rama `trabajo/margen-pendiente`), con los pasos 1 a 7 iguales y un paso 8 que mide
cuándo comprueba MetaTrader el margen de una orden pendiente stop (ADR-0081 §4). Antes de lanzarla:
1. vuelve a copiar `tools/mql5/MedirDemoFTMO.mq5` del repositorio a **MQL5 → Scripts**, encima del
   que hay (paso 4 de «Una vez»);
2. compílalo otra vez: **F4**, doble clic en **MedirDemoFTMO.mq5**, **F7**, y abajo tiene que decir
   **0 errors** (paso 5 de «Una vez»);
3. ejecútalo como siempre, sin cambiar nada en la ventana de **Aceptar**: el paso 8 ya viene activado
   (`InpMedirMargen`), y al final de la lista aparecen sus dos opciones nuevas;
4. al terminar, **comprueba que el fichero dice 1.2**: la columna `version_script` tiene que ser
   `"1.2"`, y el lector dice «(script 1.2)» junto al nombre del fichero y saca una sección nueva,
   «Paso 8». Si dice 1.1, el terminal sigue con la versión vieja: repite 1 y 2.

**Cuándo, la 3:** el lunes 2, el miércoles 4, el jueves 5 o el viernes 6 de noviembre de 2026, **de
03:00 a 12:00 hora de Lima** (la franja de 9:00 a 18:00 de España; desde el 25 de octubre España va
en UTC+1 y Lima en UTC−5, medido con `zoneinfo`). La sesión 6 con el trader fue el miércoles 4 (no
el martes 3, como se preveía), y la ejecución 3 se hizo el jueves 5 (corregido en el cierre de
`trabajo/activar-sesion-06`).

**Pendiente, sin ejecución:** mirar en el panel de la cuenta de FTMO **a qué hora se recalcula el
límite de pérdida diaria**: a medianoche de España o a medianoche del servidor. Era la «verificación
explícita» de A-28; ninguna de las tres la hizo, y desde ADR-0090 es una línea propia para ti en la
Next Action. Apúntalo con la fecha y la hora, mientras la prueba del 2026-10-29 siga viva.

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
| 8 (desde la 1.2) | el margen de una pendiente stop, en cuatro medidas: M1, si MetaTrader rechaza al colocarla una pendiente cuyo margen no cabe; M2, si una pendiente viva ocupa margen libre, y a qué precio; M3, si suma las pendientes al colocar otra; M4, si comprueba el margen cuando la pendiente salta. Lotes calculados en el momento, todo del mismo lado (compras) y con el tope de 1.000 USD | ADR-0081 §4 |

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

## La prueba del 2026-10-29

Lo que declara Aleks (2026-11-06, en el chat del consultor; `trabajo/demo-ejecuciones-2-3`): una
prueba gratuita nueva, creada el 2026-10-29, la misma clase de cuenta (2-Step, Swing, USD, 100.000,
MetaTrader 5, servidor FTMO-Demo). En ella corrieron la ejecución 2 (ese mismo día, script 1.1) y la
3 (2026-11-05, script 1.2), las dos «completo» y sin nada abierto al terminar; los CSV se copiaron
tal cual, sin abrirlos con Excel, y los originales siguen en **MQL5 → Files** (la sesión midió el
2026-11-06 que coinciden byte a byte con las copias). Que la 3 fuera en esta prueba lo dice el
encargo del consultor; los CSV no traen el número de cuenta.

## El EA de conexión (R6a.1)

Es el primer EA de la capa de MetaTrader que **nunca opera**: no envía, no modifica ni cancela
ninguna orden, ni cierra ninguna posición. Lee la cuenta, el reloj del servidor y las sesiones del
símbolo del gráfico, y lo apunta todo en un fichero, el *journal* (`mql5/JOURNAL.md`). Si la cuenta
no es de demo, se niega y no hace nada.

**La corrida de cierre: el miércoles 21 de octubre de 2026, de 15:30 a 17:15 de Lima, en la prueba
actual** (la del 2026-10-08, que vence hacia el 22). Lo decidió Aleks el 2026-10-20 (rama
`trabajo/ea-conexion`, `docs/validation/EA-CONEXION.md`, fase 3): la primera corrida, la del 20,
encontró un defecto (tras un cambio de símbolo el EA no volvía a leer la cuenta, el reloj ni las
sesiones), y esta repite la corrida entera con el EA arreglado. Va antes de la ejecución 2 de
MedirDemoFTMO, que es en la prueba nueva del 26: **nunca las dos a la vez**.

**Hecha el 2026-10-21**, de 15:30 a 17:22 de Lima: el journal valida como una sola cadena y está
congelado en los anexos de la rama, con la hora real de cada paso (`EA-CONEXION.md` §11). Lo de
abajo se queda como el procedimiento de esa corrida.

**Por qué esas horas.** La medianoche del servidor cae por la tarde en Lima: hasta el 25 de octubre
el servidor va 3 horas por delante de GMT, y son **las 16:00 de Lima** (medido el 20: el cambio de día
llegó a las 16:00:48). Desde el 25 serán las 16:00 o las 17:00 (justo lo que mide A-28).
*(Medido después, ADR-0090: el servidor siguió a EE. UU., así que del 25 de octubre al 1 de
noviembre la medianoche del servidor siguió a las 16:00 de Lima, y desde el 1 de noviembre cae a las
17:00.)*

**No hay que copiar ni compilar nada.** La sesión deja el EA arreglado compilado en la carpeta de
datos del terminal: **MQL5 → Experts → Botsito → Botsito.ex5** (instalado el 2026-10-20). En
MetaTrader aparece en **Ver → Navegador**, **Asesores expertos → Botsito → Botsito**. Los journals
del 20 ya no están en **MQL5 → Files → Botsito**: la sesión los movió a la subcarpeta
`demo-20261020-defecto`, para que la corrida del 21 empiece un journal nuevo.

**Los pasos, con la hora de Lima.** Si te equivocas de minuto no pasa nada: apunta la hora a la que
lo hiciste y díselo a la sesión, que lo compara con el journal.

1. **Antes de las 15:30: la hora de Windows, en hora.** Configuración → Hora e idioma → Fecha y hora
   → **Sincronizar ahora**. La hora GMT del journal sale del reloj de este ordenador: si no está en
   hora, el desfase sale mal.
2. **Antes de las 15:30: la cuenta.** MetaTrader abierto con la cuenta de prueba actual (como en «Una
   vez»), la conexión en verde abajo a la derecha.
3. **Antes de las 15:30: un gráfico de EURUSD** (Observación del mercado → clic derecho en **EURUSD →
   Ventana de gráfico**; el marco temporal da igual). Solo ese gráfico lleva el EA.
4. **15:30 · Ponerlo.** Arrastra **Botsito** desde el Navegador encima del gráfico de EURUSD y pulsa
   **Aceptar** sin cambiar nada. El botón **Algo Trading** da igual: el EA no opera. Arriba a la
   derecha del gráfico aparece el nombre del EA. En la caja de herramientas (**Ctrl+T**), pestaña
   **Expertos**, no tiene que salir «la cuenta NO es DEMO».
5. **15:35 · El cambio de símbolo, a propósito.** Sin quitar el EA, arrastra **US100.cash** desde
   Observación del mercado **encima del mismo gráfico**. El gráfico pasa a US100.cash y el EA sigue
   puesto (su nombre sigue arriba a la derecha). Es lo que pasó por error el 20, y ahora se comprueba
   que el EA vuelve a leerlo todo.
6. **15:37 · Volver a EURUSD.** Arrastra **EURUSD** encima del mismo gráfico. Desde aquí el gráfico
   ya no se toca.
7. **Dejarlo puesto hasta las 17:00.** Pasa la medianoche del servidor (16:00 de Lima). No hace falta
   mirar nada: cada minuto apunta una línea.
8. **17:00 · Quitarlo.** Clic derecho en el gráfico → **Asesores expertos → Quitar** (*Expert
   Advisors → Remove*).
9. **17:01 · Volver a ponerlo**, como en el paso 4, en el mismo gráfico de EURUSD.
10. **17:03 · Quitarlo otra vez**, como en el paso 8. El journal tiene que seguir su cadena tras el
    reinicio: es lo que se comprueba.
11. **17:05 · Copiar el journal.** **Archivo → Abrir carpeta de datos → MQL5 → Files → Botsito**:
    copia los dos ficheros **`journal_20261021.jsonl`** y **`journal_20261022.jsonl`** (uno por día
    del servidor; no las subcarpetas) **tal cual, sin abrirlos ni renombrarlos**, a la carpeta
    **`data/ea_conexion/`** del repositorio. Como el CSV, quedan fuera de git.
12. **Avisar a la sesión.** Ella los valida y los congela en los anexos de la rama (el fichero tal
    cual y su sha256). Si quieres verlos tú:

        uv run python src/botsito/mql5bridge/journal.py data/ea_conexion/journal_20261021.jsonl data/ea_conexion/journal_20261022.jsonl

    (los ficheros en orden de fecha). Dice «NO VALIDO» y por qué, o el resumen: cuántas líneas, el
    desfase, la cuenta, las sesiones y el cambio de día.

**Lo que la sesión comprueba en el journal:** cuatro `arranque` (15:30 EURUSD, 15:35 US100.cash,
15:37 EURUSD y 17:01 EURUSD), **cada uno seguido de `cuenta`, `reloj` y `sesiones` del símbolo de ese
arranque** (el defecto del 20 era que tras un cambio de símbolo faltaban); el `cambio_de_dia` hacia
las 16:00, con las sesiones otra vez; el `fin` de las 17:00 y el de las 17:03; y una sola cadena,
con `cadena_anterior: sigue` en cada arranque menos el primero.

**Lo que no puede probar esta corrida:** que se niega en una cuenta real. Eso no se ejecuta nunca en
una cuenta real: está probado con las pruebas estáticas de la CI y con el script de pruebas en este
terminal (`docs/validation/EA-CONEXION.md`).

## El EA con la capa generada: journal v2 (R6a.2; la corrida, en R6a.8)

Desde R6a.2 (`trabajo/capa-generada`, `docs/validation/CAPA-GENERADA.md`) el EA es la versión 1.1:
recibe del repo, generado, `mql5/Include/Botsito/Capa/Generado.mqh` (los parámetros de firma,
bróker, instrumento y ejecución, el perfil de cuenta y el calendario de cierres), y cada línea de su
journal es **v2**: lleva el `capa_hash` de ese fichero (`mql5/JOURNAL.md`). R6a.2 lo comprobó con el
script de pruebas, sin demo (decisión del consultor del 2026-11-12). **La corrida en la demo es de
R6a.8**, que ya necesita la demo una semana. Este es su procedimiento; la hora y la cuenta las fija
esa rama.

**Antes del primer arranque v2: apartar el journal v1.** Un EA v2 no sigue una cadena v1 (no hay
cadena mixta): si en **MQL5 → Files → Botsito** queda un `journal_*.jsonl` de la versión 1.0, el
primer arranque dice `cadena_anterior: rota`, y si es del mismo día del servidor, el EA escribe las
líneas v2 detrás de las v1 en el mismo fichero, que ya no valida.

1. **Antes de cerrar MetaTrader**, abre la carpeta: **Archivo → Abrir carpeta de datos → MQL5 →
   Files → Botsito**. Deja abierta esa ventana del Explorador y cierra MetaTrader.
2. **Mueve** (no borres) todos los `journal_*.jsonl` sueltos de **Botsito** **fuera de MQL5 →
   Files**: a la carpeta **`data/ea_conexion/journal-v1/`** del repositorio (fuera de git, como los
   journals de R6a.1). Las subcarpetas de **Botsito** (`pruebas` y las de las corridas de R6a.1) se
   quedan donde están: el EA solo mira los ficheros sueltos. En **Botsito** no tiene que quedar
   ningún `journal_*.jsonl`.
3. El EA instalado tiene que ser el compilado del tag vigente: lo compila e instala la sesión con
   `compilar.py compilar --instalar` sobre ese tag (`MQL5 → Experts → Botsito → Botsito.ex5`).

**La corrida.** Los pasos de «El EA de conexión (R6a.1)» de arriba valen igual. Lo único que cambia
es que el primer `arranque` tiene que decir `cadena_anterior: ninguna`, y cada uno de los siguientes,
`sigue`.

**Lo que comprueba la sesión** con los journals copiados a `data/` (fuera de git):

    uv run python src/botsito/mql5bridge/journal.py <los journal_*.jsonl, en orden de fecha>

- La primera línea del resumen dice **`formato v2`** y valida como una sola cadena.
- La línea **`capa_hash:`** es igual a la de `const string CAPA_HASH` del `Generado.mqh` del tag
  vigente (`git show <tag>:mql5/Include/Botsito/Capa/Generado.mqh`), y
  `generar_capa.py --repo . --perfil ftmo-2step-swing-100k --comprobar` sale con 0 en ese tag (lo
  generado es lo de los yaml). Si el hash no coincide, el EA de la demo no es el del tag: se
  recompila y se repite.
