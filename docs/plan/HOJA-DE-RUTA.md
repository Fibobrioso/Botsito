# Hoja de ruta · de hoy a operar en vivo

El ORDEN y el ESTADO vivos de todo lo pendiente (desde `trabajo/hoja-de-ruta`, 2026-10-10;
inventario y fuentes en `docs/validation/HOJA-DE-RUTA.md` §0). `docs/plan/MASTER_PLAN.md` define
las funcionalidades (§A); su §E queda como historia.

Metas (Aleks): firme, el bot testeado y funcional para marzo de 2027; optimista, diciembre de 2026, que ya no cabe por los 3 meses de sombra de F34; y, desde el 2026-10-22, el bot operativo y generando dinero antes de agosto de 2027, cuando Aleks empieza sus prácticas.

**Cómo se lee.** Cada entrada lleva sus referencias: `NA:X` (letra viva de la Next Action de
`PROJECT_STATE.md`), `HER:n` (pendiente heredado), `ID:` (una ambigüedad `A-nn`, un `ADR-nnnn` o una
regla `RN-nnn`) y `F:Fnn` (funcionalidad de MASTER_PLAN §A). Y cuatro campos: qué es, de qué
depende, quién la hace y cuándo está hecha. Se nombran ids, nunca recuentos que caducan.

**Cómo se mantiene.** `tests/unit/test_hoja_de_ruta.py` falla si una letra viva o un heredado vivo
no está aquí, si una referencia no existe, si una entrada HECHA sigue viva, si una entrada de la
Next Action depende de una letra que no está viva, o si una ambigüedad que una sesión dio por
respondida sigue ABIERTA y no está en R1 o R4. En el cierre de cada rama, en el commit del
contrato, se actualiza junto a la Next Action (`docs/runbooks/RITUAL.md`). Cada rama nombra en su
`contrato.yaml` el tramo al que pertenece (`tramo:`, el título de un `## ` de aquí).

## R0 · Lo que ordena el trabajo

### R0.1 · Esta hoja de ruta y sus guardias
- **Refs:** NA:P · ID:ADR-0072
- **Qué es:** este fichero, `tests/unit/test_hoja_de_ruta.py`, el campo `tramo` del contrato y la
  regla de quién lee la columna de fechas (ADR-0072).
- **Depende de:** nada.
- **Quién:** la sesión, con el encargo del consultor (`trabajo/hoja-de-ruta`).
- **Hecho cuando:** la rama se cierra en `main` con la hoja, el test y ADR-0072.
- **Estado:** HECHA (`stable/F37k-hoja-de-ruta`; docs/validation/HOJA-DE-RUTA.md).

### R0.2 · El entorno de trabajo del consultor y de la sesión
- **Refs:** —
- **Qué es:** `trabajo/entorno-code`: skills y agente del consultor (entre ellos el auditor del
  encargo y las skills fase-cero y comparar-con-main, ERRORES-RECURRENTES), hook de arranque y la
  medida de `make check`.
- **Depende de:** R0.1.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** la rama se cierra en `main`.
- **Estado:** HECHA (`stable/F37l-entorno-code`; docs/validation/ENTORNO-CODE.md).

## R1 · Activar la sesión 4

### R1.1 · Las respuestas de la sesión 4 entran en la spec
- **Refs:** ID:A-13 · ID:A-18 · ID:A-21 · ID:A-25 · ID:A-30 · ID:A-32 · ID:A-33 ·
  ID:A-35 · ID:A-36 · ID:A-39 · ID:A-43 · ID:A-44 · ID:A-49 · ID:A-50 · ID:A-51 · ID:A-52 ·
  ID:A-53 · ID:RN-007 · ID:ADR-0073 · ID:ADR-0074 · ID:ADR-0075 · ID:ADR-0076 · ID:ADR-0077
- **Qué es:** las ambigüedades que SESION-04-EXTRACCION.md §5 (y SESION-03-EXTRACCION.md §5) dan
  como «resuelve» o «en parte» y siguen ABIERTA. Se activan las «resuelve»; las «en parte» van a la
  sesión 5 (R4.1). La parte de spec (A-18, A-25, A-30, A-33, A-36, A-39 y A-52 RESUELTAS; ADR-0073
  y ADR-0074) y la de motor (S-13 con ADR-0075; A-21 con ADR-0076; A-51 con ADR-0077 y RN-036; la
  rama `ventana_fin` de RN-035; el CONFIRM de S-4). RN-007 espera el umbral de «casi plana» (S-14,
  en parte), que pasa a R4.1.
- **Depende de:** R0.2.
- **Quién:** la sesión, con el encargo del consultor; cada cierre toca los cinco sitios de
  `docs/runbooks/AMBIGUEDADES.md`.
- **Hecho cuando:** cada «resuelve» está RESUELTA y cada «en parte» está escrita en la lista de la
  sesión 5 de ACTIVAR-SESION-04.md §5 y ACTIVAR-SESION-04-MOTOR.md §5.
- **Estado:** HECHA. La parte de spec en `trabajo/activar-sesion-04` (`stable/F37m-activar-sesion-04`;
  ACTIVAR-SESION-04.md) y la de motor en `trabajo/activar-sesion-04-motor`
  (`stable/F37n-activar-sesion-04-motor`; ACTIVAR-SESION-04-MOTOR.md). Las «en parte» (A-13, A-32,
  A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14) quedan escritas en el §5 de esos
  dos informes y pasan a R4.1.

### R1.2 · El sesgo de H4 que el trader respondió por WhatsApp
- **Refs:** NA:W · ID:ADR-0060 · ID:RN-003 · ID:ADR-0080
- **Qué es:** activar la regla que el trader respondió el 2026-10-14 a la pregunta P1 de R3.1
  (CORRIDA-CONSTRUCCION.md §4.4): el sesgo cambia solo si la H4 rompe el extremo de la anterior
  (con mecha o con cuerpo) y cierra del color de esa ruptura. Amplía ADR-0060 y sustituye la
  re-expresión `sesgo_h4_criterio_ruptura = mecha` por su feedback nuevo. Las capturas y los
  gráficos están fuera de git (`corpus/whatsapp-sesgo-h4-2026-10-14/`).
- **Depende de:** R3.1 (HECHA).
- **Quién:** la sesión, en rama de motor propia con ADR; la entrada del material, como decida la
  rama.
- **Hecho cuando:** la regla está en la spec y en el motor, con su feedback y su ADR, y el arnés
  se ha vuelto a correr con los tres comandos de R3.1.
- **Estado:** HECHA (`trabajo/sesgo-h4-color`, `stable/F37r-sesgo-h4-color`; SESGO-H4-COLOR.md,
  ADR-0080): la regla del color en la spec y en el motor, dos registros de feedback, el arnés
  vuelto a correr con los tres comandos de R3.1 (§4). La contradicción con la sesión 1 y la
  ruptura simple sin cuerpo van a la sesión 5 (R4.1).

## R2 · Material de construcción

### R2.1 · Julio
- **Refs:** NA:S
- **Qué es:** el backtest de julio (xlsx, vídeo y fotos), sin abrir; el consultor decide antes si es
  construcción o reservado, y se baja con sus ticks (ADR-0051 §8: sin ticks no cuenta).
- **Depende de:** R1.1.
- **Quién:** la decisión, el consultor; la columna de fechas, Aleks (ADR-0072); la rama, la sesión.
- **Hecho cuando:** julio está ingerido o declarado reservado, con sus ticks si cuenta.
- **Estado:** HECHA (`trabajo/entrada-julio`, `stable/F37o-entrada-julio`; ENTRADA-JULIO.md,
  ADR-0078): julio es construcción del 1 al 17, con sus ticks; del 20 al 31 no hay libro: va a
  R2.4.

### R2.2 · Enero cuenta: los ticks de invierno por la rejilla
- **Refs:** NA:X · ID:ADR-0069 · ID:ADR-0051 · ID:ADR-0079
- **Qué es:** `scripts/ticks_spread.py` cuenta la ventana de ticks por la rejilla (ADR-0069 §5), y
  la rama que baje ticks de un mes de invierno los baja así (heredado 34, parte a). Las partes b
  (deslizamiento) y c (swap) las miden las ejecuciones de la demo (carril de Aleks, R7.1).
- **Depende de:** nada.
- **Quién:** la sesión, en la rama que baje ticks de un mes de invierno.
- **Hecho cuando:** la ventana de ticks sale de la rejilla, con su test.
- **Estado:** HECHA (`trabajo/entrada-enero`, `stable/F37p-entrada-enero`; ENTRADA-ENERO.md,
  ADR-0079): la ventana de ticks sale de la rejilla, con su test; enero es construcción del 2 al
  30, con sus ticks. Las partes b y c del heredado 34 siguen en R7.1.

### R2.3 · Agosto: el backtest grabado en vídeo
- **Refs:** NA:Q · ID:A-56
- **Qué es:** en S-16 el trader da por bueno el backtest de agosto grabado en vídeo y no el xlsx
  del que salen hoy los casos dev de agosto. Aleks le pide su exportación; al llegar, entra por su
  propia rama (libros.yaml solo se amplía) y se revisan ADR-0040 y A-56.
- **Depende de:** la exportación del trader (carril de Aleks, A.3).
- **Quién:** Aleks la pide; la rama, la sesión con encargo del consultor.
- **Hecho cuando:** la exportación está declarada en libros.yaml y los casos dev de agosto dicen de
  qué libro salen.

### R2.4 · Julio en vídeo
- **Refs:** NA:T · NA:U · ID:ADR-0078
- **Qué es:** transcribir v11 a v14 (el backtest de julio en vídeo), comprobar qué días cubre cada
  uno y compararlos con el xlsx en los días 1 a 17 y con las horas del libro (NA:T); y, tras eso,
  decidir si se extraen casos del vídeo para los días 20 a 31, que solo están en v14 (NA:U;
  ADR-0078 §3).
- **Depende de:** R2.1 (HECHA); NA:U depende de NA:T.
- **Quién:** la transcripción y la comparación, la sesión con encargo del consultor; la decisión
  de los días 20 a 31, el consultor.
- **Hecho cuando:** v11 a v14 están transcritos y comparados con el xlsx, y los días 20 a 31 tienen
  decisión escrita.

## R3 · Una corrida del arnés sobre toda la construcción

### R3.1 · La corrida de ADR-0070 y las diferencias clasificadas
- **Refs:** ID:ADR-0070 · ID:ADR-0043 · ID:ADR-0074 · ID:ADR-0067 · ID:A-35 · ID:A-44 ·
  ID:RN-004 · ID:RN-020
- **Qué es:** una corrida del arnés sobre la construcción simulada, con las opciones de la lista
  cerrada de ADR-0070, y la clasificación de las diferencias por el consultor; y la medida de
  peticiones por día con la caja recalculada (ADR-0074 §3) frente al freno de ADR-0067. RN-004 está
  bloqueada por A-35 y RN-020 por A-44 (los heredados de los dos siguen vivos en R4.1).
- **Depende de:** R1.1 y R2.1 y R2.2 (HECHAS); R2.3 y R2.4 la amplían cuando lleguen, sin
  bloquearla; y, para que la corrida CUENTE (ADR-0070 §3), que el motor corra sin
  ningún `--diagnostico-*`: hoy lo necesita para A-35 y A-44, y sus valores van a R1.1 o, si
  la sesión 4 no basta, a R4.1. Hasta entonces la corrida es diagnóstico y no habilita R5.2.
- **Quién:** la corrida, la sesión; la clasificación, el consultor.
- **Hecho cuando:** la corrida está en un informe y cada diferencia tiene su clase.
- **Estado:** HECHA (`trabajo/corrida-construccion`, `stable/F37q-corrida-construccion`;
  CORRIDA-CONSTRUCCION.md): la corrida sobre los 76 días dev de construcción en diagnóstico (A-35 y
  A-44), su tabla por operación con la vida de la orden, y la clasificación del consultor (§4.5).
  No habilita R5.2 (ADR-0070 §3). De ella salen R1.2, R3.2 y R3.3.

### R3.2 · Comprobaciones en el visor de R3.1
- **Refs:** NA:O · ID:ADR-0057 · ID:RN-005 · ID:RN-009 · ID:RN-011
- **Qué es:** las comprobaciones E de la clasificación de R3.1, con sus días
  (CORRIDA-CONSTRUCCION.md §4.5, «Ramas candidatas»): el 0 de la caja en tres días de P2; RN-005,
  RN-009 y el minuto de `ventana_fin` de RN-001 en las sesiones sin orden; por qué RN-011 no
  dimensionó en dos sesiones; y dónde colocó el bot la orden en los rechazos por `precio_invalido`.
- **Depende de:** R3.1 (HECHA); los tres días de P2 los elige el consultor.
- **Quién:** la sesión, con el visor y el encargo del consultor.
- **Hecho cuando:** cada comprobación tiene su gráfico y su conclusión (E o R) en un informe.
- **Estado:** HECHA (`trabajo/visor-construccion`; VISOR-CONSTRUCCION.md): los gráficos son
  las páginas del visor, regenerables con los comandos del informe (§2.c), fuera de git; 19
  días con «no» de `contexto_h4.py`, que se pueden enseñar a V (si el visor o la spec cambian
  lo que pintan, se vuelven a comprobar antes), y 2026-07-01 sin página (su contexto pinta un
  día oculto). Una E (la reentrada en un punto ya llenado: R3.4, que ADR-0083 rehízo en el
  sentido contrario: el llenado no gasta el punto) y el resto «correcto», que
  aquí quiere decir que la regla se aplica como está escrita y la diferencia con el trader es
  de regla: va a V con sus preguntas (§3.2).

### R3.3 · La rama del margen
- **Refs:** NA:E · HER:37 · ID:A-18
- **Qué es:** la decisión, por ADR, de qué hace el bot cuando el lote del 0,5 % no cabe en los 50
  lotes de la firma (limitar el lote o no operar), con el margen a 1:30, que corta antes, y el
  simulador que lo compruebe; con las dos medidas de la orden de cierre de R3.1 (stops de menos
  de unos 2 pips y noticias; rechazos por volumen y por margen en la corrida de R3.1).
- **Depende de:** R3.1 (HECHA).
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** el ADR está escrito y el simulador rechaza lo que FTMO rechazaría.
- **Estado:** HECHA (`trabajo/margen-lote`, `stable/F37s-margen-lote`; MARGEN-LOTE.md): ADR-0081
  (el bot limita el lote al menor de tres; el bróker simulado rechaza por `margen_libre` al colocar
  y al llenar), A-57 abierta para la sesión 5, y las dos medidas de E (§2.b y §2.c). La re-corrida
  en diagnóstico, §4.

### R3.4 · Qué gasta un punto: el rechazo y el no envío, no el llenado
- **Refs:** NA:Y · ID:ADR-0083 · ID:ADR-0064 · ID:ADR-0074
- **Qué es:** fijar por ADR qué gasta un punto (ADR-0083, que enmienda la decisión 1 de
  ADR-0064): el rechazo del bróker -al colocar o al llenar- y el no envío lo gastan; el
  llenado no, y tras una pérdida o un break even el mismo punto se vuelve a colocar, con la
  misma caja o con otra; el código lo cumple, con tests que rompen en `main`, y la corrida 2
  repetida.
- **Depende de:** R3.2 (HECHA).
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** un test lo rompe en `main` y pasa en la rama, y la corrida 2 está repetida
  con los tres comandos de R3.1.
- **Estado:** HECHA (`trabajo/punto-usado`; PUNTO-USADO.md): ADR-0083; `liberar_usada` y el
  rechazo al llenar gasta el punto, por el cableado; 13 tests por el cableado real (4 rompen
  en `main` por D1); la corrida 2 repetida con los tres comandos de R3.1 (§4). PROVISIONAL en
  D1 hasta la pregunta 3 de la sesión 5 (R4.1).

## R4 · La sesión 5 con el trader y su activación

### R4.1 · Preparar, celebrar y activar la sesión 5
- **Refs:** ID:A-13 · ID:A-32 · ID:A-35 · ID:A-43 · ID:A-44 · ID:A-48 · ID:A-49 · ID:A-50 ·
  ID:A-53 · ID:A-57 · ID:RN-007 · NA:V · ID:RN-004 · ID:RN-020 ·
  ID:ADR-0076 · ID:ADR-0077
- **Qué es:** RN-004 tras A-35 y RN-020 tras A-44, con su medida (`docs/runbooks/ACTIVAR-A35-A44.md`
  §5.1); las «en parte» de la sesión 4 (con la segunda parte de A-43 y S-14, que es RN-007 y
  la casi plana, la antigua H), escritas en ACTIVAR-SESION-04.md §5 y ACTIVAR-SESION-04-MOTOR.md §5; las
  preguntas de ACTIVAR-SESION-04-MOTOR.md §5: el último minuto (cuándo se retira una orden
  pendiente a la hora de cerrar), la vela sin cuerpo en medio del retroceso y el breaker contrario
  que rompe con mecha (ADR-0076 §4), la racha tras la novena pérdida (ADR-0077 §5) y la
  confirmación del caso bajista de S-13; y lo que salga de R3, con la hoja de preguntas: la lista
  «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5, con su pregunta 1
  sustituida por las dos de SESGO-H4-COLOR.md §4.4 (la ruptura simple sin cuerpo y la
  contradicción con la sesión 1; R1.2); A-57 (el lote que no cabe, MARGEN-LOTE.md §5); y las
  preguntas de VISOR-CONSTRUCCION.md §3.2 (las dos nuevas y los días que ganan la 5, la 8 y la
  9; R3.2); y lo que V añade: las «en parte» de ACTIVAR-SESION-04.md §0.e, las líneas de
  ACTIVAR-SESION-04-MOTOR.md §6, si el xlsx de julio es la exportación de v11 a v13
  (ENTRADA-JULIO.md §8) y la pregunta 3 con el ejemplo del 29 de abril y la caja de la
  reentrada (PUNTO-USADO.md §5). Hoja de preguntas: docs/sesion-5/PREGUNTAS.md
  (trabajo/barrido-sesion-5).
- **Depende de:** R1.1 (HECHA), R3.1 (HECHA), R1.2 (HECHA), R3.2 (HECHA), R3.3 (HECHA),
  R3.4 (HECHA) y la copia de seguridad del carril de Aleks (A.4, HECHA el 2026-10-22).
- **Quién:** la sesión prepara y activa; Aleks celebra la sesión con el trader.
- **Hecho cuando:** la sesión 5 está ingerida y activada.
- **Estado:** spec HECHA (`trabajo/activar-sesion-05`, `stable/F38e-activar-sesion-05`;
  ACTIVAR-SESION-05.md): A-57 y A-32 RESUELTAS, A-35 y A-44 con valor y ABIERTAS (desviación
  declarada), el arnés sin diagnóstico; cinco CONFIRM y un CORRECT; S-11 «en parte», a R4.2. Motor
  pendiente (`trabajo/activar-sesion-05-motor`, §2 del informe) y después la re-corrida de
  ADR-0070 §3 con su `diff` (ACTIVAR-A35-A44.md §5.1).

### R4.2 · Preparar y celebrar la sesión 6
- **Refs:** NA:V · ID:A-35 · ID:A-44 · ID:A-13 · ID:A-43 · ID:A-46 · ID:A-48 · ID:A-49 · ID:A-50 ·
  ID:A-53 · ID:ADR-0083 · ID:RN-007
- **Qué es:** la lista de ACTIVAR-SESION-05.md §3: la magnitud de A-44 primero y su reloj; la
  mecha de A-35; A-13; A-53; A-43; A-49/A-48; A-50; ADR-0083; S-16; S-19 frente a S-24; S-20;
  S-14 con los días de construcción que dé la re-corrida; y S-11 «en parte» (la toma de la mañana
  con el MISMO sesgo en la tarde; A-46 sigue RESUELTA).
- **Depende de:** `trabajo/activar-sesion-05-motor` y la re-corrida del arnés (R4.1, lo que queda).
- **Quién:** la sesión prepara la hoja con el consultor; Aleks celebra la sesión con el trader.
- **Hecho cuando:** la sesión 6 está ingerida y activada.

## R5 · Fidelidad

### R5.1 · Las condiciones previas de F26
- **Refs:** NA:G · F:F26 · ID:A-16 · ID:A-56 · ID:ADR-0021 · ID:ADR-0033
- **Qué es:** rellenar PREREGISTRO.md (métrica, umbral, partición, autorización); arreglar que una
  pregunta abre N particiones (rama de código en la puerta); decidir qué conjunto es el universo
  (los dos días de la sesión 1 sin partición); A-56 medida, o declarada conocida, para puntuar el
  objetivo; A-16 (Oanda frente a Dukascopy); y, al elegir los libros que miden, que en los
  backtests sin vídeo faltan las sesiones que el trader se saltó por ir a break even (S-14,
  sesión 5; ACTIVAR-SESION-05.md §0.b.7).
- **Depende de:** la decisión del consultor sobre cuántos días reservados necesita F26.
- **Quién:** el consultor decide; Aleks autoriza la apertura (ADR-0021 §3); la sesión ejecuta.
- **Hecho cuando:** PREREGISTRO está relleno y commiteado, y la puerta abre una sola partición.

### R5.2 · Mayo
- **Refs:** ID:ADR-0070 · ID:ADR-0043
- **Qué es:** medir mayo, el conjunto de medida de ADR-0043, cuando la corrida de R3 llegue al
  umbral (ADR-0070).
- **Depende de:** R3.1, con una corrida que cuente (sin diagnóstico; ADR-0070 §3).
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** la medida de mayo está en su informe.

### R5.3 · Marzo
- **Refs:** HER:2 · ID:ADR-0046 · ID:ADR-0072
- **Qué es:** la entrada de marzo por el camino de fidelidad (`docs/runbooks/ENTRADA-MARZO.md`):
  marzo en `vistos.yaml` (heredado 2; lo que queda de su paso 0: la confirmación escrita del trader
  llegó el 2026-10-25, A.3); la columna de fechas por Aleks (paso a); sorteo; huso por velas;
  `libros.yaml` (paso 0 y paso d); ingesta de los `fidelidad-dev`.
- **Depende de:** la lectura de Aleks (la confirmación del trader ya está: A.3, HECHA).
- **Quién:** Aleks (fechas, confirmación); la sesión (cada paso, con sus PARADAS).
- **Hecho cuando:** marzo está sorteado, declarado e ingerido en sus días `dev`.

### R5.4 · Diciembre de 2025
- **Refs:** NA:I · NA:N
- **Qué es:** el backtest de diciembre (sin vídeo), sin abrir; antes, renovar hacia atrás el
  calendario de cierres (RENOVAR-CIERRES.md, condición 1) y que el consultor decida si es
  construcción o reservado.
- **Depende de:** R2.2 (HECHA) y R2.1 (HECHA) y R1.1.
- **Quién:** el consultor decide; Aleks lee la columna de fechas (ADR-0072); la sesión ejecuta.
- **Hecho cuando:** diciembre está ingerido o declarado reservado.

### R5.5 · Medir fidelidad, y la ventaja
- **Refs:** F:F26 · F:F27
- **Qué es:** F26 (fidelidad contra el trader sobre lo reservado) y F27 (sensibilidad y ventaja).
- **Depende de:** R5.1, R5.2 y R5.3.
- **Quién:** la sesión; la autorización de abrir, Aleks.
- **Hecho cuando:** F26 y F27 tienen informe con su cifra contra el umbral pre-registrado.

## R6a · La capa de MT5 que no decide operaciones (ADR-0082)

Va en paralelo a R2-R5, en los huecos de espera (del trader, de FTMO, de la demo), sin quitarle
turno a F. La capa vive en el EA de MQL5, solo en DEMO hasta F35, y nunca decide una operación: si
una pieza lee un hecho o un parámetro de la estrategia, espera a F26 (ADR-0082 D3). Cada pieza que
porta código de Python se prueba contra los mismos casos que sus tests.

### R6a.1 · Conexión, reloj del servidor, sesiones del símbolo y journal
- **Refs:** ID:ADR-0082 · F:F31 · F:F33 · F:F17 · ID:A-28
- **Qué es:** el EA que se conecta y se niega fuera de una cuenta DEMO (como
  `tools/mql5/MedirDemoFTMO.mq5`); lee el desfase del reloj del servidor (no decide A-28); lee las
  sesiones del símbolo con `SymbolInfoSessionTrade` (condición 2 de `RENOVAR-CIERRES.md`);
  lee y registra `ACCOUNT_MARGIN_MODE` al arrancar, sin abortar, y lo compara R6a.7 (MASTER_PLAN
  §H; ADR-0082 §10, recuadro del 2026-10-19); y fija el formato del journal, uno
  solo y versionado, pensando en F34. Su fase 0 mide cómo se compila y se prueba en MT5, con
  PARADA (ADR-0082 D7).
- **Depende de:** nada.
- **Quién:** la sesión, con el encargo del consultor: compila y ejecuta las pruebas en la máquina
  de Aleks (`src/botsito/mql5bridge/compilar.py`); Aleks pone el EA en la demo.
- **Hecho cuando:** el EA conecta en la demo, escribe el journal con el desfase y las sesiones del
  símbolo, y se niega fuera de una demo; esto último lo prueban las pruebas estáticas de la CI y
  las dinámicas del script de pruebas, porque no se ejecuta en una cuenta real.
- **Estado:** HECHA (`trabajo/ea-conexion`, `stable/F37x-ea-conexion`; EA-CONEXION.md): el EA
  `mql5/Experts/Botsito.mq5`, el journal v1 (`mql5/JOURNAL.md`) con su validador y su golden, y
  la corrida del 2026-10-21 en la demo con el journal congelado en los anexos.

### R6a.2 · Parámetros, perfil y calendario generados
- **Refs:** ID:ADR-0082 · F:F28 · ID:ADR-0068
- **Qué es:** los parámetros de firma, bróker, instrumento y ejecución, el perfil de cuenta y el
  calendario de cierres, generados desde el repo para el EA, con su propio hash en el journal; ni
  una cifra a mano (ADR-0082 D5). La parte de estrategia de F28 espera a F26. Si se decide, también
  `LATIDO_SEG` y `TOPE_SESIONES`, las dos cifras del formato del journal (`mql5/JOURNAL.md`).
- **Depende de:** R6a.1.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** regenerar no da diff y el hash está en el journal.

### R6a.3 · Órdenes stop idempotentes y reconstrucción del estado
- **Refs:** ID:ADR-0082 · F:F31 · ID:ADR-0057
- **Qué es:** colocar, modificar y cancelar órdenes stop sin duplicarlas nunca, con sus códigos de
  retorno; y, al arrancar, reconstruir órdenes, posiciones y journal contra la cuenta, con el test
  «reinicio a media jornada» (MASTER_PLAN §H.2; ADR-0082 §5). La reconciliación demo-backtest
  sigue en F34.
- **Depende de:** R6a.1 y R6a.2.
- **Quién:** la sesión, con el encargo del consultor; Aleks ejecuta en la demo.
- **Hecho cuando:** el reinicio a media jornada no duplica nada en la demo.

### R6a.4 · Freno de peticiones y veto de la firma
- **Refs:** ID:ADR-0082 · ID:ADR-0067 · ID:A-54 · ID:RN-029 · ID:RN-030 · ID:RN-031 · F:F31
- **Qué es:** el freno de ADR-0067 portado al EA y el veto de la firma de RN-029, RN-030 y RN-031;
  RN-032 lee parámetros de la estrategia y espera a F26 (ADR-0082 D3). Arregla el docstring de
  `engine/freno.py` (Technical Debt) y nombra la deuda de las citas de relleno de RN-029 a RN-032.
- **Depende de:** R6a.2 y R6a.3.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** el freno y el veto portados pasan los mismos casos que sus tests de Python.

### R6a.5 · Veto antes de los cierres de mercado
- **Refs:** ID:ADR-0082 · ID:ADR-0068 · ID:A-55 · NA:N · F:F31
- **Qué es:** el veto de ADR-0068 en el EA, con `cierres_desde_sesiones` y `unir_cierres` portados
  y las sesiones del símbolo que lee R6a.1 unidas al calendario generado.
- **Depende de:** R6a.1 y R6a.2.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** lo portado pasa los mismos casos que sus tests de Python y la demo veta antes de
  un cierre largo.

### R6a.6 · Tope por margen y volumen
- **Refs:** ID:ADR-0082 · ID:ADR-0081 · ID:A-57 · F:F31
- **Qué es:** el EA recibe un lote y lo limita por margen libre y por volumen, o no lo envía,
  según `lote_si_no_cabe` (las dos opciones, con el valor que deje A-57); y el rechazo por margen.
  Con la ejecución 3 de la demo, que mide cuándo comprueba MT5 el margen de una pendiente stop
  (A.1).
- **Depende de:** R6a.2, R6a.3 y la ejecución 3 de la demo.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** el límite portado pasa los mismos casos que sus tests de Python.

### R6a.7 · Pre-vuelo
- **Refs:** ID:ADR-0082 · F:F33 · ID:A-28
- **Qué es:** antes de operar, el EA compara el hash de lo que recibe (ADR-0082 D5) con el del repo
  en el tag stable vigente, y el hash de la spec solo cuando el EA la lleve (desde F29); el desfase
  del reloj con la tabla, `ACCOUNT_MARGIN_MODE`, y `SymbolInfo`/`AccountInfo` con el perfil; y aborta
  si algo no cuadra (MASTER_PLAN §H y §H.2). Antes de comparar `ACCOUNT_MARGIN_MODE`, el parámetro
  del modo de margen se crea con su fuente, la respuesta de FTMO sobre la cuenta Swing (A.2).
- **Depende de:** R6a.1 a R6a.6.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** el pre-vuelo aborta en la demo ante cada discrepancia provocada.

## R6 · Plataforma

### R6.1 · Del modelo a MQL5
- **Refs:** F:F28 · F:F29 · F:F30 · F:F31 · F:F32
- **Qué es:** parámetros y fixtures generados, dominio en MQL5, el harness Python-MQL5, el EA con
  órdenes idempotentes, y la paridad con el Strategy Tester.
- **Depende de:** F29, F30 y lo de F31-F32 que decide operaciones dependen de R5.5 (ADR-0082, que
  enmienda MASTER_PLAN §0); lo demás de F31 vive en R6a.
- **Quién:** la sesión, con los encargos del consultor.
- **Hecho cuando:** F32 cerrada con su paridad medida.

## R7 · Demo y sombra

### R7.1 · Demo, reconciliación y decisión
- **Refs:** F:F33 · F:F34 · F:F35 · NA:N
- **Qué es:** el despliegue en la demo, la reconciliación demo-backtest y el memorando de
  decisión; el pre-vuelo va en R6a.7. De F33 ya existen el entorno de la demo, el calendario de
  cierres y el freno.
- **Depende de:** R6.1 y R6a (la lectura de SymbolInfoSessionTrade de la condición 2 de NA:N llega
  en R6a.1 y R6a.5).
- **Quién:** la sesión; el despliegue y la decisión, Aleks.
- **Hecho cuando:** F35 tiene su memorando.

## Carril: lo de Aleks

### A.1 · Las ejecuciones 2 y 3 de la demo de FTMO
- **Refs:** NA:A · NA:M · ID:A-28 · HER:10 · F:F17
- **Qué es:** las ejecuciones 2 y 3 de MedirDemoFTMO (A-28, el nivel exacto de ADR-0057, los
  deslizamientos y los swaps); el BE de una venta que salta por el ASK
  (NA:M); y, del heredado 10, lo que queda: A-28 y el grabador de spread y ticks (F17, PARCIAL).
- **Depende de:** la prueba nueva de FTMO del 26 de octubre (fechas fijas).
- **Quién:** Aleks ejecuta; los dos CSV los congela una sola rama, tras la ejecución 3, que es la
  que decide A-28 con los dos (EA-CONEXION.md, D6).
- **Hecho cuando:** los dos CSV están congelados y A-28 decidida.

### A.2 · Las preguntas a FTMO
- **Refs:** HER:27 · ID:A-54 · ID:A-55 · ID:ADR-0068 · ID:ADR-0071
- **Qué es:** P-D1 (hedging, volumen máximo, tope sumado; el heredado 37 quedó decidido en
  ADR-0081); lo que queda del
  heredado 27: la «maximum capital allocation rule» y el asterisco de «USD/LOT*»; y lo que FTMO
  no contestó del ticket: la pregunta 6 (A-55, sin respuesta) y las respondidas solo en parte
  (A-54 y A-55; FTMO-REGLAS.md, recuadro del 2026-10-05). La comisión por lado ya está confirmada
  (ADR-0071 §3).
- **Depende de:** la respuesta de FTMO.
- **Quién:** Aleks pregunta; la sesión registra la respuesta parafraseada (RESPUESTAS-FTMO).
- **Hecho cuando:** las respuestas están registradas.

### A.3 · La agenda con el trader
- **Refs:** (la parte del heredado 2 que es la confirmación escrita; lo que queda de él vive en R5.3)
- **Qué es:** la confirmación escrita del trader sobre marzo (heredado 2) y la fecha de la sesión 5.
- **Depende de:** nada.
- **Quién:** Aleks.
- **Hecho cuando:** la confirmación está registrada y la sesión 5 tiene fecha.
- **Estado:** HECHA (2026-10-25). La sesión 5 se grabó en dos días, el 2026-10-23 (v15) y el
  2026-10-25 (v16), con un solo id, `2026-10-23-sesion-05` (SESION-05-EXTRACCION.md). La
  confirmación escrita del trader sobre marzo llegó por WhatsApp el 2026-10-25 a las 13:58 (hora
  de Lima), «Confirmado backtest de marzo», registrada en `fuentes.yaml` («Mensajes del trader») y
  en SESION-05-EXTRACCION.md §3.5. Lo que queda del paso 0 de marzo, marzo en `vistos.yaml`, es de
  R5.3.

### A.4 · La copia de seguridad
- **Refs:** (Technical Debt de PROJECT_STATE, «Copia de seguridad de las crudas y los WAV: hecha hasta v10»)
- **Qué es:** las crudas y los WAV fuera de la máquina: falta v6 (la sesión 1), y el texto de la
  deuda no dice nada de v7–v10.
- **Depende de:** nada. **Fecha límite: antes de grabar la próxima sesión con el trader.**
- **Quién:** Aleks (el consultor no tiene acceso a su máquina ni a su Drive).
- **Hecho cuando:** v6 a v10 están en Drive con su SHA256SUMS.
- **Estado:** HECHA (2026-10-22, Aleks: data/transcripciones/v6 a v10 (158 ficheros) y SHA256SUMS-v6-v10.txt (158 líneas, una por fichero) en una carpeta privada de su Google Drive).

## Carril: guardias y deuda

### G.1 · La guardia de Claude Code
- **Refs:** NA:B · NA:C · NA:D · NA:K
- **Qué es:** lo que importa o ejecuta un guion (B); las rutas compuestas (C); las formas raras (D);
  el falso positivo de `exigir_sin_crudo` (K, junto a B o C si cabe). Y lo medido en
  `trabajo/entorno-code` (ENTORNO-CODE.md §6):
  - **Prioritario dentro de G.1** (consultor, 2026-10-11): la guardia no niega
    `git ls-files knowledge/cases | grep ...`, listar la carpeta madre del holdout con un filtro
    detrás (§10.1). Es la 4.ª vez que alguien lo hace, esta vez el propio revisor.
  - `solo_lectura.py` niega `git worktree list`, que solo lee.
  - El test del ritual quedó ciego al caso del Makefile cambiado hasta entorno-code (corregido).
  - La guardia niega ejecutar desde la sesión, en un clon fuera del repo real, un test que lleve
    `crudo=True`, aunque sea el de `main` (§4.5): «probar un test con el código de `main`», de
    `comparar-con-main`, no sirve para esos tests.
  - Que `cerrar-rama` diga que, si la rama cambia el `Makefile`, los `make check` en la rama los
    lanza Aleks con «!» (§6, aviso para el cierre).
  - Desde `trabajo/activar-sesion-04-motor` (ACTIVAR-SESION-04-MOTOR.md §6 y §9.3): un falso
    positivo. `grep -rn --include=*.py` con cuatro `-e` sobre rutas literales (`src/ tests/
    scripts/`) se bloquea («leer el contenido de .») y el mismo comando con dos `-e` pasa.
  - Desde `trabajo/corrida-construccion` (CORRIDA-CONSTRUCCION.md §1.j): la guardia niega un
    guion de la carpeta de trabajo que nombre `data/manifests/ticks/<manifiesto>.yaml` de un mes de
    construcción, aunque Read deja abrir esos manifiestos; que admita esas rutas literales.
  - Desde `trabajo/activar-sesion-05` (ACTIVAR-SESION-05.md §0.f; va con K, el clon de
    `C:/cm/`): la guardia niega como tests los de un clon de `C:/cm/` que globean
    `knowledge/cases` o recorren directorios: `test_kit.py`, `test_selector_orden_stop.py` y
    `test_renovar_cierres.py` no se pudieron correr en ese clon.
- **Depende de:** nada.
- **Quién:** la sesión, en ramas propias.
- **Hecho cuando:** cada una con su test que la rompe a propósito.

### G.2 · Pendientes del consultor y del kit
- **Refs:** NA:L · NA:J · NA:N · HER:6 · HER:7 · HER:8 · HER:9
- **Qué es:** la revisión de `ev-v7-001550-82e5cffc` (L); `kit hoja` roto para un paquete nuevo
  (J, antes de la próxima sesión que etiquete días); el calendario de cierres por condición (N); y, del Next Action viejo: febrero no
  se toca (6), junio y la guardia (7), el brief de los `dev` de septiembre (8) y re-descargar un mes
  rompe `kit build` (9). Y, desde `trabajo/activar-sesion-04`: `--diagnostico-a47` (A-47 RESUELTA)
  y `--diagnostico-a27` (A-27 DECIDIDA) siguen en la CLI sin deuda que los recoja (`--diagnostico-a21`
  ya salió, ADR-0076), y se retiran en G.1 o en rama propia; dos `make check` de esa rama dieron
  `MemoryError` de `lzma` en `tests/unit/test_ticks.py`, ajenos a la rama: la decisión de
  `pytest-xdist` (G.4) necesita la RAM de la máquina, que dará Aleks. Y, desde
  `trabajo/activar-sesion-04-motor` (ACTIVAR-SESION-04-MOTOR.md §6): el token `ambiguo` del sesgo
  sin productor (ADR-0075); `feedback pending` no admite dos CORRECT vivos sobre una regla (RN-003
  cita `fb-2026-10-04-sesion-04-6e7da456` desde ADR-0080, y salen pendientes los dos
  CORRECT anteriores, `fb-2026-09-29-sesion-03-31fb311f` y `fb-2026-10-04-sesion-04-ca0afae6`,
  BARRIDO-SESION-5.md §1.f); el recuadro que le falta a
  ADR-0044 §1 («doble ruptura = AMBIGUO», enmendado por ADR-0060 §1 y ADR-0075) y su fila del
  índice; y el anexo `docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`, que no corre
  con el código de hoy (`Diagnostico` por posición): no se edita, se reproduce con el código de su
  commit. Y, desde `trabajo/corrida-construccion` (CORRIDA-CONSTRUCCION.md §1.c): que
  `arnes.dias_de_mercado` imprima una línea `LECTURA:` por recuento de los días reservados cuyas
  velas lee para calentar, como `kit check` (ADR-0033 §4); hoy lo cubre HOLDOUT-EXPOSICIONES.
  Y, desde `trabajo/barrido-sesion-5` (BARRIDO-SESION-5.md §1.d y §4): `scripts/hoja_preguntas.py`
  sigue con el encabezado y la regla 2 de la sesión 2, lleva A-24 (DECIDIDA) en su orden, no
  lleva A-50, A-53 ni A-57 y no puede llevar la B de VISOR-CONSTRUCCION.md §3.2 (toca A-46,
  RESUELTA). El paso 6 de «Antes» de `docs/runbooks/SESION-DE-PREGUNTAS.md`, que decía todavía
  «abril o agosto», remite a su regla 2 desde `trabajo/previa-sesion-5` (PREVIA-SESION-5.md §3).
- **Depende de:** nada (J, antes de la próxima sesión que etiquete días).
- **Quién:** el consultor (L, 6 y la decisión de 7 y 8); la sesión, en ramas propias.
- **Hecho cuando:** cada una sale de PROJECT_STATE con su evidencia.

### G.3 · El perfil de FTMO dice algo que ya no es verdad
- **Refs:** —
- **Qué es:** la descripción de `firma_tamano_posicion_ratio_aviso`
  (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`) dice todavía «PENDIENTE PARA ALEKS con FTMO»;
  FTMO respondió sin cifra (`docs/validation/FTMO-REGLAS.md`, respuesta 10).
- **Depende de:** nada.
- **Quién:** la próxima rama que toque el perfil de FTMO.
- **Hecho cuando:** la descripción dice lo que respondió FTMO.
- **Estado:** HECHA (`trabajo/margen-lote`, `stable/F37s-margen-lote`): la descripción de
  `firma_tamano_posicion_ratio_aviso` dice lo que respondió FTMO (respuesta 10).

### G.4 · Las tareas repetidas que ninguna skill cubre
- **Refs:** NA:F
- **Qué es:** los huecos de ENTORNO-CODE.md §0.c: escribir un ADR nuevo; sacar líneas de
  PROJECT_STATE a HISTORIA con saldo ≤ 0; material escrito del trader al corpus; registrar
  respuestas de FTMO o de Aleks; congelar un CSV de la demo; demostrar un test por mutación;
  comparar reglas con main caso a caso; recuadros de corrección; las notas del consultor para la
  orden de cierre. Y volver a medir `pytest-xdist` con la cifra nueva de E3 (respuesta 1).
- **Depende de:** R0.2.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** cada hueco tiene skill o se decide que no la necesita.

## Carril: material reservado que no se toca

- Febrero de 2026 (heredado 6): no se toca ni se descarga.
- Lo reservado de cada reparto (`knowledge/cases/holdout/`, los días de las particiones
  reservadas): solo por la puerta de ADR-0033, con PREREGISTRO relleno (R5.1).
- Las capturas de Analytics, de cualquier mes: no se abren nunca.
- Marzo, julio y diciembre: sin abrir hasta su rama (R5.3, R2.1, R5.4); de cada uno, antes del
  sorteo, solo la columna de fechas, y la lee Aleks (ADR-0072).

## F01-F35 · Estado medido (MASTER_PLAN §A)

Medido por el contenido, no por el número del tag (inventario en `docs/validation/HOJA-DE-RUTA.md`
§0.d). Reserva de esa medida: F14, F22 y F23 se clasifican PARCIAL por sus módulos, sus fichas y
sus ambigüedades, sin revisar cada informe a fondo.

| Funcionalidad | Estado | Prueba |
|---|---|---|
| F:F01 a F:F13, F:F15 | HECHA | tags `stable/F01`..`stable/F13`, `stable/F15` y sus informes |
| F:F18, F:F19, F:F20, F:F21 | HECHA, con ambigüedades abiertas | `MOTOR-SESGO-H4.md`, `LIQUIDEZ-M15.md`, `BREAKER-M1.md`, `BE-AL-TICK.md` |
| F:F14 | PARCIAL: casos y particiones, sin cierre formal | `CASOS-AGOSTO-ABRIL.md`, `GUARDA-DE-HOLDOUT.md` |
| F:F16 | PARCIAL: ticks congelados en CSV, no Parquet | `TICKS-LLENADO.md` |
| F:F17 | PARCIAL: el script de medición, no el grabador | `DEMO-EJECUCION-1.md` |
| F:F22 | PARCIAL: el motor es un intérprete de la spec | `ARNES-MOTOR.md` |
| F:F23 | PARCIAL: bucle y reloj, sin journal | `ARNES-MOTOR.md` |
| F:F24 | PARCIAL: broker, llenado y cuenta, sin contador de N | `CABLEADO-SIMULADOR.md` |
| F:F25 | PARCIAL: el visor de días, no el de tres marcos | `docs/runbooks/VISOR-DIAS.md` |
| F:F33 | PARCIAL: entorno de la demo, cierres y freno | `DEMO-EJECUCION-1.md`, `RENOVAR-CIERRES.md` |
| F:F26 | SIN EMPEZAR (preparada) | `PREREGISTRO.md`, sin rellenar |
| F:F27, F:F28, F:F29, F:F30, F:F31, F:F32, F:F34, F:F35 | SIN EMPEZAR | sin código ni informe |

## Fechas fijas

- La prueba gratuita de FTMO del 2026-10-08 vence hacia el 2026-10-22 (NA:A).
- La ejecución 2 de la demo, entre el 26 y el 30 de octubre de 2026, en una prueba creada el 26; la
  ejecución 3, después del 1 de noviembre (NA:A).
- La semana del 26 al 30 de octubre de 2026 es la primera en que el bot abre a otra hora: Europa ya
  cambió la hora y EE. UU. no (ADR-0069).
