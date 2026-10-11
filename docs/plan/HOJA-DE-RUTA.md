# Hoja de ruta · de hoy a operar en vivo

El ORDEN y el ESTADO vivos de todo lo pendiente (desde `trabajo/hoja-de-ruta`, 2026-10-10;
inventario y fuentes en `docs/validation/HOJA-DE-RUTA.md` §0). `docs/plan/MASTER_PLAN.md` define
las funcionalidades (§A); su §E queda como historia.

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

### R0.2 · El entorno de trabajo del consultor y de la sesión
- **Refs:** NA:F
- **Qué es:** `trabajo/entorno-code`: skills y agente del consultor (entre ellos el auditor del
  encargo y las skills fase-cero y comparar-con-main, ERRORES-RECURRENTES), hook de arranque y la
  medida de `make check`.
- **Depende de:** R0.1.
- **Quién:** la sesión, con el encargo del consultor.
- **Hecho cuando:** la rama se cierra en `main`.

## R1 · Activar la sesión 4

### R1.1 · Las respuestas de la sesión 4 entran en la spec
- **Refs:** NA:E · HER:15 · ID:A-13 · ID:A-18 · ID:A-21 · ID:A-25 · ID:A-30 · ID:A-32 · ID:A-33 ·
  ID:A-35 · ID:A-36 · ID:A-39 · ID:A-43 · ID:A-44 · ID:A-49 · ID:A-50 · ID:A-51 · ID:A-52 ·
  ID:A-53 · NA:H · ID:RN-007
- **Qué es:** las ambigüedades que SESION-04-EXTRACCION.md §5 (y SESION-03-EXTRACCION.md §5) dan
  como «resuelve» o «en parte» y siguen ABIERTA. Se activan las «resuelve»; las «en parte» van a la
  sesión 5 (R4). Con parámetro que ya lleva valor: A-13, A-18, A-25, A-32, A-33 (CONFIRMED), A-30,
  A-43, A-52, A-53 (DEFAULT_AMBIGUOUS). Falta código: A-36, A-49, A-51; A-21 a medias (falta la
  opción que da la respuesta). A-35 y A-44 tienen el código y les falta el valor. RN-007 (NA:H)
  espera el umbral de «casi plana» (S-14, en parte). El heredado 15 (la pregunta de A-18) sale
  cuando se cierre A-18. El refiltrado de las filtradas v7–v10 que E citaba está HECHO
  (ACTIVACION-A42.md §2.2).
- **Depende de:** R0.2 (NA:F).
- **Quién:** la sesión, con el encargo del consultor; cada cierre toca los cinco sitios de
  `docs/runbooks/AMBIGUEDADES.md`.
- **Hecho cuando:** cada «resuelve» está RESUELTA y cada «en parte» está en la hoja de la sesión 5.

## R2 · Material de construcción

### R2.1 · Julio
- **Refs:** NA:S
- **Qué es:** el backtest de julio (xlsx, vídeo y fotos), sin abrir; el consultor decide antes si es
  construcción o reservado, y se baja con sus ticks (ADR-0051 §8: sin ticks no cuenta).
- **Depende de:** R1.1 (NA:E).
- **Quién:** la decisión, el consultor; la columna de fechas, Aleks (ADR-0072); la rama, la sesión.
- **Hecho cuando:** julio está ingerido o declarado reservado, con sus ticks si cuenta.

### R2.2 · Enero cuenta: los ticks de invierno por la rejilla
- **Refs:** NA:X · HER:34 · ID:ADR-0069 · ID:ADR-0051
- **Qué es:** `scripts/ticks_spread.py` cuenta la ventana de ticks por la rejilla (ADR-0069 §5), y
  la rama que baje ticks de un mes de invierno los baja así (heredado 34, parte a). Las partes b
  (deslizamiento) y c (swap) las miden las ejecuciones de la demo (carril de Aleks, NA:A).
- **Depende de:** nada.
- **Quién:** la sesión, en la rama que baje ticks de un mes de invierno.
- **Hecho cuando:** la ventana de ticks sale de la rejilla, con su test.

## R3 · Una corrida del arnés sobre toda la construcción

### R3.1 · La corrida de ADR-0070 y las diferencias clasificadas
- **Refs:** ID:ADR-0070 · ID:ADR-0043 · HER:25 · HER:30 · HER:35 · ID:A-21 · ID:A-35 ·
  ID:A-44 · ID:RN-004 · ID:RN-020
- **Qué es:** una corrida del arnés sobre la construcción simulada, con las opciones de la lista
  cerrada de ADR-0070, y la clasificación de las diferencias por el consultor. RN-004 está bloqueada
  por A-35 (heredados 25 y 30) y RN-020 por A-44 (heredado 35).
- **Depende de:** R1.1 y R2; y, para que la corrida CUENTE (ADR-0070 §3), que el motor corra sin
  ningún `--diagnostico-*`: hoy lo necesita para A-21, A-35 y A-44, y sus valores van a R1.1 o, si
  la sesión 4 no basta, a R4.1. Hasta entonces la corrida es diagnóstico y no habilita R5.2.
- **Quién:** la corrida, la sesión; la clasificación, el consultor.
- **Hecho cuando:** la corrida está en un informe y cada diferencia tiene su clase.

## R4 · La sesión 5 con el trader y su activación

### R4.1 · Preparar, celebrar y activar la sesión 5
- **Refs:** ID:A-13 · ID:A-21 · ID:A-32 · ID:A-35 · ID:A-43 · ID:A-44 · ID:A-49 · ID:A-50 ·
  ID:A-53 · NA:J
- **Qué es:** las «en parte» de la sesión 4, y lo que salga de R3, con la hoja de preguntas. La hoja
  Word necesita antes que `kit hoja` funcione con un paquete nuevo (NA:J).
- **Depende de:** R1.1, R3.1 y la copia de seguridad del carril de Aleks.
- **Quién:** la sesión prepara y activa; Aleks celebra la sesión con el trader.
- **Hecho cuando:** la sesión 5 está ingerida y activada.

## R5 · Fidelidad

### R5.1 · Las condiciones previas de F26
- **Refs:** NA:G · F:F26 · ID:A-16 · ID:A-18 · ID:ADR-0021 · ID:ADR-0033
- **Qué es:** rellenar PREREGISTRO.md (métrica, umbral, partición, autorización); arreglar que una
  pregunta abre N particiones (rama de código en la puerta); decidir qué conjunto es el universo
  (los dos días de la sesión 1 sin partición); A-18 cerrada para puntuar el objetivo; A-16 (Oanda
  frente a Dukascopy).
- **Depende de:** R1.1 (A-18) y la decisión del consultor sobre cuántos días reservados necesita F26.
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
- **Refs:** HER:2 · HER:12 · ID:ADR-0046 · ID:ADR-0072
- **Qué es:** la entrada de marzo por el camino de fidelidad (`docs/runbooks/ENTRADA-MARZO.md`):
  marzo en `vistos.yaml` y la confirmación escrita del trader (heredado 2); la columna de fechas por
  Aleks (paso a); sorteo; huso por velas; `libros.yaml` (heredado 12); ingesta de los
  `fidelidad-dev`.
- **Depende de:** la confirmación del trader y la lectura de Aleks.
- **Quién:** Aleks (fechas, confirmación); la sesión (cada paso, con sus PARADAS).
- **Hecho cuando:** marzo está sorteado, declarado e ingerido en sus días `dev`.

### R5.4 · Diciembre de 2025
- **Refs:** NA:I · NA:N
- **Qué es:** el backtest de diciembre (sin vídeo), sin abrir; antes, renovar hacia atrás el
  calendario de cierres (RENOVAR-CIERRES.md, condición 1) y que el consultor decida si es
  construcción o reservado.
- **Depende de:** R2.2 (NA:X), R2.1 (NA:S) y R1.1 (NA:E).
- **Quién:** el consultor decide; Aleks lee la columna de fechas (ADR-0072); la sesión ejecuta.
- **Hecho cuando:** diciembre está ingerido o declarado reservado.

### R5.5 · Medir fidelidad, y la ventaja
- **Refs:** F:F26 · F:F27
- **Qué es:** F26 (fidelidad contra el trader sobre lo reservado) y F27 (sensibilidad y ventaja).
- **Depende de:** R5.1, R5.2 y R5.3.
- **Quién:** la sesión; la autorización de abrir, Aleks.
- **Hecho cuando:** F26 y F27 tienen informe con su cifra contra el umbral pre-registrado.

## R6 · Plataforma

### R6.1 · Del modelo a MQL5
- **Refs:** F:F28 · F:F29 · F:F30 · F:F31 · F:F32
- **Qué es:** parámetros y fixtures generados, dominio en MQL5, el harness Python-MQL5, el EA con
  órdenes idempotentes, y la paridad con el Strategy Tester.
- **Depende de:** R5.5 (fidelidad antes de MQL5, MASTER_PLAN §A).
- **Quién:** la sesión, con los encargos del consultor.
- **Hecho cuando:** F32 cerrada con su paridad medida.

## R7 · Demo y sombra

### R7.1 · Demo, reconciliación y decisión
- **Refs:** F:F33 · F:F34 · F:F35 · NA:N
- **Qué es:** pre-vuelo y despliegue en la demo, la reconciliación demo-backtest y el memorando de
  decisión. De F33 ya existen el entorno de la demo, el calendario de cierres y el freno.
- **Depende de:** R6.1; y la rama que conecte el bot en tiempo real (demo o real) no se cierra sin
  la lectura de SymbolInfoSessionTrade o un procedimiento que cierre el hueco del jueves
  (NA:N, condición 2; ADR-0068 §4).
- **Quién:** la sesión; el despliegue y la decisión, Aleks.
- **Hecho cuando:** F35 tiene su memorando.

## Carril: lo de Aleks

### A.1 · Las ejecuciones 2 y 3 de la demo de FTMO
- **Refs:** NA:A · NA:M · ID:A-28 · HER:10 · HER:34 · F:F17
- **Qué es:** las ejecuciones 2 y 3 de MedirDemoFTMO (A-28, el nivel exacto de ADR-0057, los
  deslizamientos y los swaps; heredado 34, partes b y c); el BE de una venta que salta por el ASK
  (NA:M); y, del heredado 10, lo que queda: A-28 y el grabador de spread y ticks (F17, PARCIAL).
- **Depende de:** la prueba nueva de FTMO del 26 de octubre (fechas fijas).
- **Quién:** Aleks ejecuta; la sesión congela cada CSV en su rama.
- **Hecho cuando:** los dos CSV están congelados y A-28 decidida.

### A.2 · Las preguntas a FTMO
- **Refs:** NA:O · HER:27 · HER:37 · ID:A-54 · ID:A-55 · ID:ADR-0068 · ID:ADR-0071
- **Qué es:** P-D1 (hedging, volumen máximo, tope sumado; decide el heredado 37); lo que queda del
  heredado 27: la «maximum capital allocation rule» y el asterisco de «USD/LOT*»; y lo que FTMO
  no contestó del ticket: la pregunta 6 (A-55, sin respuesta) y las respondidas solo en parte
  (A-54 y A-55; FTMO-REGLAS.md, recuadro del 2026-10-05). La comisión por lado ya está confirmada
  (ADR-0071 §3).
- **Depende de:** la respuesta de FTMO.
- **Quién:** Aleks pregunta; la sesión registra la respuesta parafraseada (RESPUESTAS-FTMO).
- **Hecho cuando:** las respuestas están registradas y el heredado 37 decidido.

### A.3 · La agenda con el trader
- **Refs:** HER:2
- **Qué es:** la confirmación escrita del trader sobre marzo (heredado 2) y la fecha de la sesión 5.
- **Depende de:** nada.
- **Quién:** Aleks.
- **Hecho cuando:** la confirmación está registrada y la sesión 5 tiene fecha.

### A.4 · La copia de seguridad
- **Refs:** (Technical Debt de PROJECT_STATE, «Copia de seguridad … INCOMPLETA desde el 2026-09-09»)
- **Qué es:** las crudas y los WAV fuera de la máquina: falta v6 (la sesión 1), y el texto de la
  deuda no dice nada de v7–v10.
- **Depende de:** nada. **Fecha límite: antes de grabar la próxima sesión con el trader.**
- **Quién:** Aleks (el consultor no tiene acceso a su máquina ni a su Drive).
- **Hecho cuando:** v6 a v10 están en Drive con su SHA256SUMS.

## Carril: guardias y deuda

### G.1 · La guardia de Claude Code
- **Refs:** NA:B · NA:C · NA:D · NA:K
- **Qué es:** lo que importa o ejecuta un guion (B); las rutas compuestas (C); las formas raras (D);
  el falso positivo de `exigir_sin_crudo` (K, junto a B o C si cabe).
- **Depende de:** nada.
- **Quién:** la sesión, en ramas propias.
- **Hecho cuando:** cada una con su test que la rompe a propósito.

### G.2 · Pendientes del consultor y del kit
- **Refs:** NA:L · NA:J · NA:N · HER:6 · HER:7 · HER:8 · HER:9
- **Qué es:** la revisión de `ev-v7-001550-82e5cffc` (L); `kit hoja` roto para un paquete nuevo
  (J, antes de R4); el calendario de cierres por condición (N); y, del Next Action viejo: febrero no
  se toca (6), junio y la guardia (7), el brief de los `dev` de septiembre (8) y re-descargar un mes
  rompe `kit build` (9).
- **Depende de:** nada (J, antes de R4.1).
- **Quién:** el consultor (L, 6 y la decisión de 7 y 8); la sesión, en ramas propias.
- **Hecho cuando:** cada una sale de PROJECT_STATE con su evidencia.

### G.3 · El perfil de FTMO dice algo que ya no es verdad
- **Refs:** HER:27
- **Qué es:** la descripción de `firma_tamano_posicion_ratio_aviso`
  (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`) dice todavía «PENDIENTE PARA ALEKS con FTMO»;
  FTMO respondió sin cifra (`docs/validation/FTMO-REGLAS.md`, respuesta 10).
- **Depende de:** nada.
- **Quién:** la próxima rama que toque el perfil de FTMO.
- **Hecho cuando:** la descripción dice lo que respondió FTMO.

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
- La copia de seguridad, antes de grabar la próxima sesión con el trader (A.4).
