# Sesión 02: inventario y auditoría antes de preparar la reunión

Rama `trabajo/sesion-02`, 2026-09-24. Parte A de la tanda: **solo lectura**. No se ha tocado
`ambiguedades.yaml`, ni la spec, ni el código, ni ningún material del trader. Sin merge, sin tag y
sin push.

**Una regla de escritura de este documento.** El id de la sesión 01 lleva dentro la fecha de la
sesión, que es la de grabación de v6 y, por ADR-0041, la de un día retirado del holdout. Por eso
aquí no se escribe esa fecha: el paquete se cita como `knowledge/cases/kit/*-sesion-01/`, el
informe como `docs/validation/SESION-01-*.md`, y los registros de feedback de esa sesión por su
sufijo (`fb-…-e030e316`). Donde un texto literal la trae, va sustituida por «[fecha omitida]».
Las demás fechas que aparecen son fechas de decisiones y no dicen de ningún día que esté reservado.

Guardas verificadas al empezar: `docs/validation/PREREGISTRO.md` con blob `52649183…`, el
declarado; **cero** ficheros `docs/validation/AUTORIZACION-*`.

## 1. Cómo se hizo la sesión 01

Fuentes: ADR-0011 (el kit), ADR-0012 (el registro tras la sesión 1), ADR-0022 §7 y ADR-0023 (el
feedback), `knowledge/cases/kit/README.md`, el paquete `knowledge/cases/kit/*-sesion-01/`, el
informe `docs/validation/SESION-01-*.md` y el código de las guardias. **No hay runbook de sesión**:
el procedimiento está repartido entre esos documentos (ver §8, candidato a documento propio).

### (a) Los pasos de una sesión, de principio a fin

1. **Registro pre-poblado.** Todo parámetro que la evidencia nombra existe en
   `knowledge/spec/parametros.yaml` en `UNKNOWN`, para que la respuesta tenga dónde aterrizar
   (ADR-0011 §2: «para que `RESOLVE_UNKNOWN` tenga objetivo en la sesion 1»).
2. **Paquete determinista.** `botsito kit build --sesion AAAA-MM-DD-sesion-NN --seed N` escribe
   `cuestionario.yaml`, `ventanas.yaml`, `particiones.yaml` y `hoja_trader.md` (ADR-0011 §9;
   `knowledge/cases/kit/README.md`, tabla de ficheros). El cuestionario lleva «una pregunta por
   origen (parametro UNKNOWN, ambiguedad, contradiccion) con sus casos `ev-*`».
3. **Particiones commiteadas ANTES de la sesión.** «`particiones.yaml` se commitea ANTES de la
   sesion; la guardia (`knowledge validate`) es de ANCESTRO en git» (ADR-0011 §5). Desde ese
   momento `particiones.yaml` y `ventanas.yaml` son inmutables.
4. **`kit check`** recompone el paquete y lo compara byte a byte (ADR-0011 §9).
5. **La hoja en Word, lo último.** `uv run botsito kit hoja` genera un `.docx` «con cada pregunta,
   su contexto, sus citas y una caja de respuesta, mas la tabla de etiquetado de los casos `dev`.
   Se rellena a mano durante la sesion. No se versiona» (`knowledge/cases/kit/README.md`, «Hoja en
   Word»). «Regenerar la hoja en Word es siempre lo ultimo, justo antes de imprimir».
6. **Precondición de ceguera.** «El trader confirma por escrito (registro F09, `medio: escrito`)
   que no ha operado ni backtesteado los meses del paquete», como `CONFIRM` sobre el objetivo
   `paquete` cuyo id es la sesión; un `REJECT` obliga a añadir el mes a `vistos.yaml` y regenerar
   (README del kit, «Condicion previa de cada sesion»; ADR-0011 §4).
7. **La sesión, grabada.** La hoja se rellena en paralelo: «La hoja trae la **síntesis** que
   escribió el consultor durante la sesión; la grabación trae la **voz** del trader»
   (`SESION-01-*.md` §1).
8. **Registro de las respuestas** como `FeedbackRecord` en `knowledge/feedback/<sesion>/`
   (§1(c) abajo). «Donde ambas coexisten, el registro del vídeo supersede al de la hoja»
   (`SESION-01-*.md` §1).
9. **La grabación al corpus** y su evidencia (§1(d) abajo).
10. **`feedback apply`** lleva los valores al registro (ADR-0012 §7) y las ambigüedades se cierran
    en `ambiguedades.yaml` (§1(c)).
11. **Informe de la sesión** en `docs/validation/` con lo decidido, lo abierto y los compromisos.

### (b) Días mostrados al trader, de qué partición y qué lo garantiza

- **La hoja llevaba SOLO los días `dev`.** ADR-0011 §5: «La hoja del trader solo lleva los casos
  `dev`». El generador filtra así: `dev = [c for c in casos if asignacion.get(c.id) == "dev"]`
  (`src/botsito/cases/paquete.py:485`), bajo el título «## Ventanas de etiquetado (solo `dev`)». La
  hoja generada del paquete termina con «16 casos dev de 40 del paquete (los holdout no se
  muestran).» (`knowledge/cases/kit/*-sesion-01/hoja_trader.md:255`).
- **No se llegaron a etiquetar.** «Ese backtest **sustituye al etiquetado a mano** de los 16 días
  `dev` de la hoja» (`SESION-01-*.md` §6). Medido hoy: **0** registros con `accion: LABEL_CASE` en
  `knowledge/feedback/`.
- **Qué lo garantiza:**
  - el test de contrato `test_la_hoja_no_filtra_la_particion_oculta`
    (`tests/contract/test_hoja_sesion_docx.py:128`): recorre todos los casos no `dev` y exige que
    su día no aparezca en el texto del `.docx`, ni las palabras `holdout`, `sha256`,
    `dataset_id` o `seed`;
  - la guardia de ancestro: el reparto se commitea antes del primer `LABEL_CASE` (ADR-0011 §5);
  - **para los retirados**, `abrir_caso` rechaza siempre un día retirado, con o sin autorización
    (ADR-0041; `src/botsito/cases/holdout.py`, `abrir_caso`). El único retirado está en el camino
    de fidelidad, no en el paquete de la sesión 01.
- **Lo que NO garantiza nada mecánico:** que la hoja rellenada o la grabación no muestren un día
  reservado por otra vía (una pantalla compartida, un gráfico abierto). En la sesión 01 eso se
  cubrió con la precondición de ceguera, no con un mecanismo.

### (c) Cómo cuenta una respuesta como «registro del trader» para RESUELTA

- **La regla:** «Hay DOS formas de cerrarla (ADR-0022): `RESUELTA` con un registro del trader que
  apunte A LA AMBIGUEDAD -no al parametro-, o `DECIDIDA` por el consultor con el ADR que la nombre»
  (`CLAUDE.md`, «Cerrar una ambigüedad…»). ADR-0022 §7 crea `DECIDIDA`.
- **La guardia que lo hace cumplir** (`src/botsito/validation/knowledge.py:495-500`): «{id} figura
  RESUELTA y ningun registro de feedback la cierra (hace falta uno con objetivo ambiguedad/{id} y
  accion RESOLVE_UNKNOWN)». Y una bloqueante no se puede cerrar por decisión: «es bloqueante y no
  puede cerrarse por decision del consultor; eso lo responde el trader» (misma función).
- **La forma del registro** (`src/botsito/feedback/modelo.py`): obligatorios `sesion`, `fecha`,
  `medio`, `objetivo`, `accion`, `respuesta_literal` y `registrado_por`; `medio` ∈ {replay, audio,
  video, escrito}; `RESOLVE_UNKNOWN` admite objetivo `ambiguedad`.
- **Desde el 2026-09-13 son obligatorios por guardia `recibido_el` y `procedencia`** (ADR-0023 §2,
  `CORTE_PROCEDENCIA`). `procedencia` tiene seis valores; los que son del trader son
  `trader_grabado` (exige medio grabado, con `grabacion`, `t0` y `t1`), `trader_hoja` y
  `trader_escrito` (exige `medio: escrito`, con la captura en el corpus). `referido_por_consultor`
  es el consultor contando lo que respondió, «NO es transcripcion».
- **Consecuencia para la sesión 02:** una ambigüedad pasa a RESUELTA solo si hay un
  `RESOLVE_UNKNOWN` sobre `ambiguedad/A-NN`, con `procedencia` del trader y su soporte (grabación
  inventariada o captura), en un commit con `Fuente:`.

### (d) Grabación y transcripción: cómo entran al corpus

- **Grabación como vídeo del corpus.** ADR-0011 §8: «Grabaciones de sesion como `videos` de
  `fuentes.yaml` (transcribibles con F04, citables), con `drive_id` opcional cuando la `naturaleza`
  empieza por `sesion`». v6 está así en `knowledge/corpus/fuentes.yaml`: `drive_id: null  #
  grabacion de sesion: nace en local, no viene de Drive (ADR-0011)`.
- **Transcripción** con el mismo motor que los otros vídeos (`tr-v6-large-v3-int8-float16-7718b3f4`,
  2146 segmentos), **fotogramas** a 1 fps (`fr-v6-22982c02`) y **evidencia** propia (12 ítems en
  `knowledge/evidence/v6/`, aceptados por el consultor) (`SESION-01-*.md` §1).
- **Tramos no citables** declarados en `knowledge/corpus/tramos_no_citables.yaml`, con guardia en
  `evidence propose --check` y `evidence new` (`SESION-01-*.md` §4).
- **La hoja rellenada**: se copia a `corpus/…/Sesiones/<sesion>/` y está inventariada en
  `knowledge/corpus/manifest.yaml` con `papel: material_adicional`; el `.docx` de la raíz lo pisa el
  generador (`SESION-01-*.md` §1). **Su FORMATO:** un `.docx` generado por `kit hoja` con una caja
  de respuesta por pregunta y la tabla de etiquetado de los `dev`; las respuestas escritas en ella
  entraron como registros con `medio: escrito` y la nota «sintesis escrita por el consultor en la
  hoja durante la sesion; la version explicada esta en la grabacion v6». **No se ha abierto.**
- **Advertencia para la sesión 02:** v6 se grabó el día de la sesión, que resultó ser un día
  reservado y hoy está retirado (ADR-0041). **Si la sesión 02 se graba un día laborable que esté en
  una partición reservada, pasa lo mismo.** Candidato a guardia: comprobar el día de grabación
  contra `casos_ocultos` antes de inventariar (ver §8).

## 2. Inventario de preguntas pendientes

### 2.1 Ambigüedades no RESUELTA

Son **21**: 15 ABIERTA y 6 DECIDIDA. RESUELTA son 14 (A-1 a A-12, A-14 y A-20). Texto de
`pregunta` copiado del fichero por script (en UTF-8), salvo la fecha omitida.

#### A-13 · break even al toque o con cuerpo

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas RN-014; parámetros `break_even_criterio_ruptura`
- **`pregunta`, literal:**

  > ¿el rompimiento de la zona de control que dispara el break even vale al toque (por un pip) o hay que esperar a que la vela cierre con cuerpo? El parametro que responde a esto es `break_even_criterio_ruptura`, no `break_even_condicion`: aquel dice CON QUE se da por rota la zona y este si el stop se mueve al TOCAR el nivel o al cierre, que es otra pregunta y la cerro A-4. Hasta el 2026-09-11 esta ambiguedad nombraba el segundo, asi que `spec status` ensenaba como "en revision" un valor CONFIRMED y ESCONDIA el default que de verdad corre

#### A-15 · alcance de la ventana operativa

- **Estado:** DECIDIDA (ADR-0024, 2026-09-12) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas ninguna regla la cita; parámetros `ventana_inicio`, `ventana_fin`
- **`pregunta`, literal:**

  > ¿el bot busca solo en las dos sesiones de 07-11 y 11-15, o tambien en la de Nueva York? DECIDIDO por el consultor el 2026-09-12: NO se amplia en esta fase. No es una pregunta que el trader se reservara, es una que DEVOLVIO -"puedes buscar las operaciones donde sea, o sea, no hay problema"-, y toda su operativa GRABADA va de 07:00 a 15:00. Ampliar sin una sola sesion grabada en Nueva York meteria en el universo de etiquetado dias que nadie ha visto operar y cambiaria el sesgo H4 de la mitad. La capacidad se conserva: ampliar es cambiar ventana_inicio y ventana_fin, nada mas

#### A-16 · cuanto se separan las velas de Oanda de las de Dukascopy

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** medicion
- **Afecta a:** reglas RN-003; parámetros —
- **`pregunta`, literal:**

  > ¿como se comparan decisiones tomadas sobre velas de Oanda (FX Replay) con un bot medido sobre Dukascopy, si la regla depende de romper por una milesima? Partida el 2026-09-12 (ADR-0024): aqui queda solo la MEDICION, que no la puede cerrar ninguna decision. El anexo del [fecha omitida] midio OTRA pareja -MT5/FundedNext contra Dukascopy, 2 puntos de mediana- y el lo dice: "queda una tercera fuente en juego, que es la del trader [...] esta medicion no la cubre". La decision de metodo que estaba mezclada aqui es A-23

#### A-17 · noticias frente a la regla de la cuenta de fondeo

- **Estado:** DECIDIDA (ADR-0026, 2026-09-14) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas RN-028; parámetros `filtro_noticias`
- **`pregunta`, literal:**

  > DESCARTADA una via el 2026-09-12: se penso que la pestaña `Prop firm` de FX Replay -que el trader tiene con el plan Pro- podria llevar dentro la ventana de noticias y el corte del dia de riesgo, y cerrar esta y A-19 de golpe. El trader responde que NO la tiene configurada con FundedNext. Sigue haciendo falta el reglamento. ¿QUE prohibe exactamente el reglamento de FundedNext sobre operar en noticias: que eventos, cuantos minutos antes y despues, y que sancion? Es un HECHO que se verifica en su reglamento, no una decision. Partida en dos el 2026-09-12 (ADR-0022): la decision de alcance -el bot no opera noticias en la v1 aunque la estrategia del trader si funcione dentro de ellas- se fue a A-22 y esta DECIDIDA; aqui se queda lo que hay que leer y medir. Sin esta respuesta, RN-028 sabe QUE bloquea y no CON QUE VENTANA. DECIDIDA el 2026-09-14 por ADR-0026, que cambia de firma. El reglamento se leyo ese dia y el supuesto era cierto donde se miro: FTMO Standard prohibe abrir o cerrar -incluida la ejecucion de un stop o un objetivo- de dos minutos antes a dos despues de noticias seleccionadas, con la cuenta como sancion, y FundedNext recorta el 40 % del beneficio operado cinco minutos antes y despues. Pero la cuenta elegida es FTMO 2-Step SWING, que no tiene restricciones de noticias, asi que la ventana deja de importar: filtro_noticias vuelve a `no` y RN-028 se descarta

#### A-18 · base sobre la que se mide el objetivo 1:3

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas RN-015; parámetros `base_calculo_objetivo`, `objetivo_rr`
- **`pregunta`, literal:**

  > ¿el 1:3 se mide sobre la caja completa o sobre la distancia hasta el stop, que es la que dimensiona el lote? Hasta el 2026-09-11 las dos eran la MISMA distancia y la pregunta sonaba academica; desde ADR-0020 el lote se dimensiona hasta stop_fraccion_caja y el objetivo sigue midiendose sobre la caja entera, asi que la respuesta cambia el RR realizado de verdad. PRIMERA MEDIDA, y no sale de la sesion sino del material (2026-09-21, agosto, ADR-0037): las dos lecturas predicen RR distintos sobre la distancia entrada-stop -`caja_completa` da objetivo_rr/stop_fraccion_caja = 3,75; `riesgo_real` da 3,00- y las 18 filas de agosto con `maxTP` e `initialSL` tienen SUELO EN 3,00 (minimo 2,50, tres clavadas en 3,00, 16 de 18 por debajo de 3,75). La combinacion CONFIRMED de hoy -caja_completa con stop a 0,8- no cuadra con el material: o la base es `riesgo_real`, o el stop del trader en su backtest no esta a 0,8 de la caja. NO DECIDE NADA: es un mes, son 18 filas, y LA CAJA NO ESTA EN EL FICHERO -el RR medido es riesgo real por construccion, asi que si el stop viviera en el borde de la caja las dos lecturas coincidirian y la medida no discriminaria-. Se repite sobre mayo al ingerirlo. v5 (2026-09-05 21-03-59.mkv), 36 fotogramas en ventanas fijas de los instantes 1, 2, 3, 4, 6 y 7: ninguno cumple la condicion congelada; la medida no esta en v5; via cerrada. Transcripciones v1–v5: 42 pasajes, ninguno responde con la regla congelada; se pregunta al trader. En v1–v4 el stop se describe en dos tiempos (lote sobre la caja entera, stop protegido a 0,75 tras la entrada), anterior al lineamiento del [fecha omitida]; las dos hipótesis vigentes suponen un solo stop.

#### A-19 · cuando empieza el dia y la semana de riesgo

- **Estado:** DECIDIDA (ADR-0027, 2026-09-14) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas RN-020; parámetros `reloj_dia_riesgo`
- **`pregunta`, literal:**

  > DESCARTADA una via el 2026-09-12: la pestaña `Prop firm` de FX Replay no la tiene el trader configurada con FundedNext, asi que no hay atajo. Sigue siendo el panel de la cuenta (F17). ¿en que reloj cae la medianoche que reinicia el tope diario del 4,5 % y el domingo que reinicia el semanal: el del servidor del broker, que cambia con el calendario de Nueva York, o el del grafico? Hay que verificarlo en el panel de la cuenta, no suponerlo. DECIDIDA el 2026-09-14 por ADR-0027: con la firma elegida (ADR-0026) la contesta el reglamento, no el panel -"Account balance at midnight CE(S)T of the previous day"-. El corte es la medianoche CIVIL centroeuropea, que es el reloj del trader (huso_operativa), y no la del servidor, que era nuestro default. reloj_dia_riesgo pasa a `civil_operativa`, CONFIRMED. Lo que SI queda por medir -el reloj del servidor, que ya no decide el corte- es A-28

#### A-21 · que es una zona de control limpia, sin ruido

- **Estado:** ABIERTA · **bloqueante:** SÍ · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros —
- **`pregunta`, literal:**

  > el trader condiciona la entrada a que la zona de control "no haga mucho ruido, o sea, sea una zona limpia". Los dos esquemas SI estan definidos en el corpus -rompe directo sin retroceso, o pequeno retroceso con zona de control y luego rompe- pero "limpia" no: es lo unico de la geometria de entrada que sigue siendo cualitativo y que el motor no puede evaluar. ¿cuantas velas? ¿cuanto retroceso de mas la invalida? ¿o se mide por otra cosa? ESTA AMBIGUEDAD NACIO MAL el 2026-09-10, preguntando que es un breaker; la definicion ya estaba en el corpus y lo que faltaba era recogerla en el glosario. Reformulada el mismo dia

#### A-22 · si el bot opera noticias, y que pasa con la capacidad para otras cuentas

- **Estado:** DECIDIDA (ADR-0022, 2026-09-12) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas ninguna regla la cita; parámetros `filtro_noticias`
- **`pregunta`, literal:**

  > el trader opera noticias en sus cuentas propias -que no lo prohiben- y su estrategia funciona dentro de esos eventos. ¿el bot hace lo mismo? DECIDIDO por el consultor el 2026-09-12: NO en la primera version, porque va a una cuenta fondeada que puede prohibirlo como norma y la sancion es perder la cuenta aunque la operacion acabe en profit. La CAPACIDAD se conserva: `filtro_noticias` mantiene la opcion `no`, asi que el dia que el bot corra en una cuenta que lo permita se cambia el valor y nada mas. Lo que falta por saber -que ventana exacta- es A-17. SENTIDO INVERTIDO el 2026-09-14 por la enmienda de ADR-0022 (que la nombra, y por eso sigue siendo su decision): la cuenta elegida es FTMO 2-Step Swing, sin restriccion de noticias (ADR-0026), asi que el bot SI opera noticias, como el trader. La mitad que conserva la capacidad sigue en pie: si algun dia corre en una cuenta con restriccion, filtro_noticias pasa a `regla`, se revive RN-028 y hace falta un calendario economico (pre-vuelo de F33)

#### A-23 · que proveedor es la referencia para medir la fidelidad

- **Estado:** DECIDIDA (ADR-0024, 2026-09-12) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas ninguna regla la cita; parámetros —
- **`pregunta`, literal:**

  > el trader decide sobre velas de Oanda (FX Replay) y el bot se mide sobre otras. ¿cual es la referencia? DECIDIDO por el consultor el 2026-09-12: DUKASCOPY (ADR-0005), porque cubre 2026 entero, es publico y reproducible, y donde se puede comparar esta a 2 puntos del feed del broker. MT5/FundedNext no puede sustituirlo -no sirve los meses del paquete: cero velas M1 de mayo- y se usa para lo que si aporta: spread real, condiciones de ejecucion, reloj de servidor y paridad con Strategy Tester. La divergencia entre proveedores entra en F26 como MARGEN DECLARADO y no como ruido ignorado: una regla que depende de romper por una milesima puede cambiar de decision dentro de ese margen. Cuanto vale ese margen frente a Oanda es A-16, que sigue abierta

#### A-24 · que hace que marques un pivote de M15 y no otro

- **Estado:** DECIDIDA (ADR-0045, 2026-09-24) · **bloqueante:** no · **clase:** —
- **Afecta a:** reglas RN-004; parámetros —
- **`pregunta`, literal:**

  > cuando en M15 tienes varios pivotes candidatos, ¿que hace que marques uno y no otro? En v3 0:15:31 (fotograma fr-v3-982da728/944000) descartas expresamente el alto mas alto -"aunque yo invadiria este alto"- y marcas el de abajo, el que te deja el precio. No te preguntamos si es "el mas reciente" o "el mas extremo": las dos veces que lo hemos medido, el que eliges es el mismo. La pregunta es por el CRITERIO, y lo necesitamos dicho de forma que se pueda reproducir sin ti: que dos personas mirando el mismo grafico marquen el mismo nivel. Si la respuesta es "el que yo considere" (v3 0:39:16), dinos QUE MIRAS para considerarlo: cuantas velas atras, que tamano de movimiento, que lo descalifica

#### A-25 · la vida de la marca de liquidez de M15

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros `cartuchos_reinicio`
- **`pregunta`, literal:**

  > ya has marcado la liquidez de M15 y el precio todavia no la ha tomado, o la ha tomado y sigues con cartuchos: si M15 desarrolla entretanto otro pivote del mismo lado y mas reciente, ¿mueves la liquidez a ese pivote -y con ella el lado de ruido de RN-005 y el reinicio de los cartuchos, que es `siguiente_liquidez_m15`- o la marca se queda fija hasta que la retire uno de los eventos que si nombras: trade ganador (v6 0:32:27), invalidacion (v3 0:51:10) o cambio de dia (v4 1:09:21)?

#### A-26 · el flujo de M15 cuando va contra el sesgo de H4

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros —
- **`pregunta`, literal:**

  > la vela que marca la liquidez es "contraria al flujo", y ese flujo es el de M15: eso ya lo dijiste cuatro veces y desde el 2026-09-20 esta escrito en la spec. Lo que no has dicho: en v3 0:12:42 el sesgo de H4 es bajista y el flujo de M15 que describes es un "complex pullback ALCISTA". Cuando el flujo de M15 va contra el sesgo de H4, ¿marcas igual la liquidez con la vela contraria a ese flujo alcista -y entonces el lado de ruido hay que leerlo del flujo de M15 y no del sesgo de H4, como esta hoy en RN-005- o solo cuentan las velas contrarias al flujo que va en el sentido del sesgo? DIAGNOSTICO del 2026-09-24 (MOTOR-SESGO-H4, construccion abril y agosto, sin tocar la regla): de 77 operaciones del trader, 12 van EN CONTRA del sesgo H4 del bot al abrir su sesion (58 a favor, 7 con sesgo ambiguo)

#### A-27 · las especificaciones de EURUSD en FTMO

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** medicion
- **Afecta a:** reglas ninguna regla la cita; parámetros `instrumento_digitos`, `instrumento_contrato`, `instrumento_lote_minimo`, `instrumento_lote_paso`, `instrumento_stops_level`
- **`pregunta`, literal:**

  > MEDICION, no pregunta al trader. ¿que digits, tamaño de contrato, lote minimo, paso de lote y stops level tiene EURUSD en la cuenta de FTMO? Los cinco se midieron el 2026-09-05 en una demo de FundedNext, la firma que ADR-0026 descarta, y se conservan como DEFAULT declarado porque EURUSD tiene las mismas especificaciones en casi cualquier broker: no se heredan como medicion. El que mas puede diferir es el stops level, que en FundedNext valia 0 y dejaba RN-026 sin activarse nunca. Se mide en la prueba gratuita de FTMO con SymbolInfo* (junto con el lote maximo, el freeze level y los modos de llenado, que el registro todavia no guarda) y el pre-vuelo de F33 aborta si la cuenta real dice otra cosa

#### A-28 · el reloj del servidor de FTMO y su regla de horario de verano

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** medicion
- **Afecta a:** reglas ninguna regla la cita; parámetros `broker_offset_base`, `broker_dst`
- **`pregunta`, literal:**

  > MEDICION, no pregunta al trader. ¿cuanto va el reloj del servidor de FTMO por delante de UTC en horario estandar, y con que calendario cambia de hora: el de Nueva York, el europeo o ninguno? La ficha de FTMO dice "GMT+2 +DST" sin nombrar el calendario, y lo que midio la demo de FundedNext (120 minutos, calendario de Nueva York) no se hereda (ADR-0026). Desde ADR-0027 este reloj ya no decide el dia de riesgo, que es civil; decide la rejilla de velas del servidor y si anclaje_h4 (17:00 Nueva York) cae de verdad en su medianoche. COMPROBAR EL CALENDARIO EXIGE OBSERVAR UNA TRANSICION de hora en el terminal, asi que esta ambiguedad NO SE CIERRA ANTES DEL CAMBIO DE HORA DE OCTUBRE: el desfase base se puede medir cualquier dia, la regla de horario de verano no. VERIFICACION EXPLICITA (añadida el 2026-09-14 al validar la rama): confirmar EN EL PANEL de la prueba gratuita de FTMO que el corte del dia de riesgo -cuando se recalcula el limite diario- cae a medianoche CE(S)T y NO a la medianoche del servidor. Las dos se separan una hora (el servidor va a GMT+2/+3 y CE(S)T a GMT+1/+2) y equivocarse cuesta la cuenta. reloj_dia_riesgo se queda CONFIRMED en `civil_operativa` por el reglamento (ADR-0027); si el panel dijera otra cosa, se reabre A-19 y el parametro vuelve a DEFAULT_AMBIGUOUS

#### A-29 · cuando nace la orden limite

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas RN-010, RN-011, RN-019; parámetros `orden_limite_nace`
- **`pregunta`, literal:**

  > ¿cuando colocas la orden limite por primera vez en una zona: cuando ya se ha dado el esquema de entrada ("apenas el breaker, o sea, marco mi orden limit"), o en cuanto tomas la liquidez de M15, en la primera zona de control que se completa, y desde ahi la vas moviendo? El corpus dice las dos: v3 0:42:01 marca la orden con el breaker; v1 0:13:58 la va "bajando" en cuanto rompe la liquidez; v3 0:25:11 la tiene "predefinida" esperando el breaker; y en la sesion 1 (v6 1:22:14) la orden ya esta en la zona de "posible breaker" y se activa sin validar, que es el caso de RN-010. La spec corre con la primera como default (orden_limite_nace). Con la segunda hay que reescribir RN-008, que hoy prohibe abrir sin esquema y frenaria la propia colocacion. PRIORIDAD DE LA SESION 2 (consultor, 2026-09-17): el default se queda hasta que el trader responda

#### A-30 · la orden limite pendiente al llegar el fin de la ventana

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros —
- **`pregunta`, literal:**

  > ¿que haces con una orden limite que sigue pendiente, sin llenar, cuando llegan las 15:00: la cancelas, o la dejas puesta y, si se llena despues, la gestionas? A las 15:00 cierras lo que tengas abierto (RN-002), pero de una orden todavia sin llenar no hablaste, y ninguna ambiguedad lo preguntaba: la auditoria del 2026-09-13 midio que, sin respuesta, una limite viva sobrevive al cierre y se llena fuera de la ventana. La accion `retirar_orden_limite` esta declarada y ninguna regla la usa hasta que respondas

#### A-31 · el stop entero de una entrada que se activo sin ruptura

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas RN-016, RN-019; parámetros —
- **`pregunta`, literal:**

  > una entrada que se activo sin ruptura y se fue al stop entero, ¿gasta intento? Dijiste que no cuentan como intento "un break even [...] una entrada invalidada [...] reentrada despues de equal" (RN-016, v6 0:52:19), y el equal que describes en v6 1:22:25-1:23:19 es una salida que no llega al stop: se activa sin validar, un equal "te saque la entrada, te genera una perdida" y actualizas el limit para reentrar. Del stop entero de esa misma entrada no hablaste. La spec corre con que SI gasta, porque cuesta el riesgo entero y ninguno de tus tres casos lo exime; y con que la salida en negativo sin stop NO gasta. Las dos cosas son lectura nuestra (cartucho_criterio, RN-016, RN-019). Se lleva a la sesion 2

#### A-32 · el nivel que al romperse con mecha invalida la entrada

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros `breaker_m1_criterio_ruptura`
- **`pregunta`, literal:**

  > en v4 0:53:23 (fotograma fr-v4-9ad0ebb8/3203000) descartas la entrada porque el precio rompe con mecha el nivel horizontal que tienes dibujado, al que apunta tu flecha: ¿ese nivel es la liquidez de M15 -y entonces lo que exige cuerpo es RN-004, ya escrito- o es un nivel de M1, y entonces hay rupturas de M1 que tampoco valen con mecha, contra breaker_m1_criterio_ruptura?

#### A-33 · tres ganadoras que cierran por debajo de 3R

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas ninguna regla la cita; parámetros `parciales`, `objetivo_rr`
- **`pregunta`, literal:**

  > en la sesion 1 dijiste "sin toma de parciales y que tiene que llegar al ratio 1.3 si o si" (v6 0:17:07). Pero en tu material hay TRES operaciones GANADORAS que CIERRAN por debajo de 3R: una en agosto (2,50) y dos en abril (2,57 y 2,94), en dos meses independientes. ¿cerraste esas a mano? ¿tomaste parciales en ellas? ¿o hubo otro motivo -un break even que salto, una noticia, cerrar antes de una sesion-? No te preguntamos si tomas parciales EN GENERAL, que ya lo contestaste: te preguntamos que paso en esas. MEDIDO ANTES DE PREGUNTAR, y es lo que hace que la pregunta exista: `maxTP` es el PRECIO DE CIERRE de las ganadoras y no la excursion maxima -`== avgClosePrice` en 17 de 17 filas de abril donde existen las dos, y presente si y solo si `rPnL > 0`-, asi que esas tres no son operaciones que NO LLEGARON a 3R: son operaciones que CERRARON en ganancia por debajo de 3R. En F14a esa columna se habia SUPUESTO al reves (ADR-0037 y su correccion del 2026-09-22). OBSERVACION DESCRIPTIVA del 2026-09-22 (MAYO-DEV, ADR-0040), sin atribuir causa: ganadoras por debajo de 3R = agosto 1 (2,50), abril 2 (2,57; 2,94), mayo 1 (2,90), esta ultima sobre los 6 dias `dev` de mayo

#### A-34 · vela H4 previa que rompe ambos extremos

- **Estado:** ABIERTA · **bloqueante:** no · **clase:** pregunta
- **Afecta a:** reglas RN-003; parámetros —
- **`pregunta`, literal:**

  > vela H4 previa que rompe ambos extremos: ¿que sentido toma el sesgo? Dijiste que el sesgo cambia si la vela rompe el extremo de la anterior, y que basta con la mecha; no dijiste que pasa si la rompe por arriba y por abajo. Mientras no lo digas, el bot da el sesgo por AMBIGUO en esa sesion y no opera (ADR-0044)

#### A-35 · cuándo un pivote de M15 está formado

- **Estado:** ABIERTA · **bloqueante:** SÍ · **clase:** pregunta
- **Afecta a:** reglas RN-004; parámetros —
- **`pregunta`, literal:**

  > Cuando marcas un alto o un bajo en M15 como liquidez, ¿en qué momento lo das por bueno? ¿Y qué haces si después el precio lo supera un poco?

### 2.2 Lo pendiente en PROJECT_STATE

Solo lo que sigue abierto; lo marcado HECHO, RESUELTA o CERRADA no se lista. Ids `PS-NN` de este
documento.

| id | dónde | qué | clase |
|---|---|---|---|
| PS-01 | Next Action 2, 12 y 23 | la entrada de marzo cuando llegue el libro | DATOS |
| PS-02 | Next Action 6 | febrero no se toca ni se descarga; rama propia si se abre | CONSULTOR |
| PS-03 | Next Action 7 y Technical Debt «JUNIO SIGUE SIENDO `dev`» | junio en el reparto de la sesión 1: la guardia y los once días reservados | CONSULTOR |
| PS-04 | Next Action 8 | el brief para abrir los 4 `dev` de septiembre | CONSULTOR |
| PS-05 | Next Action 9 | re-descargar un mes rompe `kit build` en silencio | CONSULTOR |
| PS-06 | Next Action 10 | la prueba gratuita de FTMO y sus medidas (A-27, A-28) | DATOS |
| PS-07 | Next Action 15 | A-18 en espera de la respuesta del trader | TRADER |
| PS-08 | Next Action 22 | la reunión con el trader | TRADER |
| PS-09 | Technical Debt | el `no_trade` por ausencia no está decidido (forma del caso) | CONSULTOR |
| PS-10 | Technical Debt | una pregunta abre N particiones y N lo decide el dato: bloqueante antes de la primera autorización | CONSULTOR |
| PS-11 | Technical Debt | el fallback de `leer_fichero` juzga una carpeta desconocida bajo `holdout-1` | CONSULTOR |
| PS-12 | Technical Debt | con el huso mal declarado, filas desplazadas desaparecen sin aviso | CONSULTOR |
| PS-13 | Technical Debt | nada comprueba que el cuerpo de un informe cerrado no cambie | CONSULTOR |
| PS-14 | Technical Debt | el fractal 5/120 no captura lo que el trader llama estructura | CONSULTOR |
| PS-15 | Technical Debt (tres entradas) | el detector de contradicciones: temas hermanos, recencia y `fecha_grabacion` como eje | CONSULTOR |
| PS-16 | Technical Debt | la vía de propuesta no admite `supersede` | CONSULTOR |
| PS-17 | Technical Debt | un CONFIRM sobre un ítem supersedido queda invisible | CONSULTOR |
| PS-18 | Technical Debt | un token no puede declarar quién lo produce | CONSULTOR |
| PS-19 | Technical Debt | una `pregunta` puede nombrar un instante del corpus sin enlazar su ítem | CONSULTOR |
| PS-20 | Technical Debt | `lectura_de_velas` lee el config de hoy para el prefijo | CONSULTOR |
| PS-21 | Technical Debt | dos días del universo de la sesión 1 fuera de toda partición: F26 tiene que saberlo | CONSULTOR |
| PS-22 | Technical Debt | un camino que guarde material en `knowledge/cases/<camino>/` necesita lector guardado antes | CONSULTOR |
| PS-23 | Technical Debt | la guardia de `cobertura_material` en `universo()` es más estricta de lo que ADR-0025 sostiene | CONSULTOR |
| PS-24 | Technical Debt | `scripts/v5_criterio.py` solo reconoce cajas de venta | CONSULTOR |
| PS-25 | Technical Debt | copia de seguridad fuera de la máquina: falta v6 | CONSULTOR |
| PS-26 | Technical Debt | `idealTP`: columna del material que no sabemos qué es | DATOS |
| PS-27 | Technical Debt | F26 no puede puntuar el objetivo hasta que A-18 esté cerrada | TRADER (vía A-18) |
| PS-28 | Technical Debt | la serie del trader es Oanda y la nuestra Dukascopy | DATOS (= A-16) |
| PS-29 | Open Questions | fuente de ticks históricos (F16) | CONSULTOR |

### 2.3 Dudas abiertas sin ambigüedad asignada

Comprobado contra `ambiguedades.yaml` que ninguna A-NN las cubre.

- **D-01 · El lado del libro que dibuja FX Replay.** ADR-0029 mide la geometría en BID y declara:
  «Lo que NO está verificado: que sea también el lado sobre el que decide el trader [...] Si
  dibujara ASK o el precio medio, se abre ambigüedad y este punto se revisa»; Impacto: «El punto 1
  queda pendiente de verificación con el trader o con FX Replay». `PROJECT_STATE.md`, índice:
  «geometria en BID (sin verificar que FX Replay dibuje BID)». Afecta a RN-011, RN-012 y RN-015.
  → **C-03**.
- **D-02 · Qué punto marca el extremo de la caja, del que sale el stop.** `glossary.yaml`, `caja`:
  «la distancia entre la entrada y el extremo del stop inicial». La auditoría del 2026-09-13, hallazgo
  [3] (`AUDITORIA-2026-09-13-ultracode.md:375`): «La caja no tiene ancla citable ni precio: nadie
  dice qué es el nivel 0 ni el nivel 1», con ítems del corpus sin citar en la spec
  (`ev-v1-001454-69cebe62`, «desde el punto mas abajo... se puede definir el stop loss»). Sigue
  así: `LIQUIDEZ-M15.md:166`, «**v1 0:14:54** (`stop.origen_vela_contraria`) queda anotado y sin
  tocar: es otra rama». Afecta a RN-011, RN-012 y RN-015, y a A-18. → **C-02**.
- **D-03 · La unidad de medida de F26.** La auditoría del 2026-09-13
  (`AUDITORIA-2026-09-13-ultracode.md:895`) mide que la unidad `(caso, sesión H4)` de ADR-0011 y
  `kappa.py` no representa varias operaciones por sesión, mientras `PREREGISTRO.md:17-18` habla de
  operación. No bloquea el motor. → **C-08**.
- **D-04 · `spread_maximo` UNKNOWN sin decir «a propósito».** Es inerte mientras `filtro_spread`
  sea `false` (CONFIRMED), pero, a diferencia de los otros UNKNOWN deliberados, su descripción no
  lo declara. Revisión del consultor.

Parámetros no CONFIRMED del registro: 7 `DEFAULT_AMBIGUOUS`, todos con su ambigüedad (A-27 ×5,
A-13, A-29), y 9 `UNKNOWN`: `broker_offset_base` y `broker_dst` (A-28), y siete que siguen UNKNOWN a
propósito tras un REJECT o por ser derivados o inertes (`stop_reduccion_fraccion`,
`stop_reduccion_umbral_vela`, `stop_segundo_esquema`, `objetivo_extension`, `spread_maximo`,
`stop_colchon_spread`, `stop_proteccion_capital`).

### 2.4 La sesión 01: lo que quedó sin respuesta o dudoso

Medido con script sobre `cuestionario.yaml` y los registros activos (no superseded) de
`knowledge/feedback/*-sesion-01/`, sin leer respuestas:

- **Las 27 preguntas (P-01 a P-27) tienen al menos un registro activo** sobre cada uno de sus
  orígenes. **Ninguna quedó sin respuesta.**
- **Siete orígenes quedaron en UNKNOWN por REJECT**, a propósito (la regla se descartó y el
  parámetro sigue sin valor, ADR-0012 §2): P-08 `stop_segundo_esquema`, P-10
  `stop_colchon_spread`, P-12 `stop_reduccion_umbral_vela` y `stop_reduccion_fraccion`, P-15
  `stop_proteccion_capital`, P-17 `objetivo_extension` y P-24 `spread_maximo`.
- **Lo que la sesión dejó dudoso** son las cinco ambigüedades que abrió (`SESION-01-*.md` §3), con
  su estado de hoy: A-13 ABIERTA, A-14 RESUELTA, A-15 DECIDIDA, A-16 ABIERTA (medición) y A-17
  DECIDIDA.
- **Las catorce confirmaciones R-01 a R-14** tienen su registro (`SESION-01-*.md`, anexo).
- Registros: 118 en total, 73 activos (36 `RESOLVE_UNKNOWN`, 14 `REJECT`, 13 `CORRECT`, 9
  `CONFIRM`, 1 `RESOLVE_CONTRADICTION`); 1 `CONFIRM` sobre `paquete`.

## 3. Clasificación

### 3.1 PARA EL TRADER

«Sugiere respuesta» = el campo `pregunta` nombra alternativas, cifras o la respuesta esperada.

| id | bloquea | sugiere respuesta | la parte que sugiere |
|---|---|---|---|
| A-35 | **RN-004** (bloqueante) | **no** | — («¿en qué momento lo das por bueno? ¿Y qué haces si después el precio lo supera un poco?») |
| A-21 | bloqueante; ninguna regla la cita (ver K-04) | **sí** | «¿cuantas velas? ¿cuanto retroceso de mas la invalida? ¿o se mide por otra cosa?» |
| A-24 (confirmar la DECIDIDA) | RN-004 | **sí, y a propósito la niega** | «No te preguntamos si es "el mas reciente" o "el mas extremo"» — nombra las dos |
| A-26 | RN-005 (lado de ruido) | **sí** | «¿marcas igual la liquidez con la vela contraria a ese flujo alcista [...] o solo cuentan las velas contrarias al flujo que va en el sentido del sesgo?» |
| A-25 | RN-005, reinicio de cartuchos | **sí** | «¿mueves la liquidez a ese pivote [...] o la marca se queda fija hasta que la retire uno de los eventos que si nombras» |
| A-32 | RN-008 / RN-004 | **sí** | «¿ese nivel es la liquidez de M15 [...] o es un nivel de M1» |
| A-29 | RN-010, RN-011, RN-019 | **sí** | «cuando ya se ha dado el esquema de entrada [...] o en cuanto tomas la liquidez de M15» |
| A-30 | fin de ventana, `retirar_orden_limite` | **sí** | «la cancelas, o la dejas puesta y, si se llena despues, la gestionas?» |
| A-18 | RN-015 | **sí, con cifras** | «¿el 1:3 se mide sobre la caja completa o sobre la distancia hasta el stop [...]?»; «3,75»; «3,00» |
| A-13 | RN-014 | **sí** | «¿[...] vale al toque (por un pip) o hay que esperar a que la vela cierre con cuerpo?» |
| A-31 | RN-016, RN-019 | **sí, con el default** | «La spec corre con que SI gasta» |
| A-33 | parciales, `objetivo_rr` | **sí** | «¿cerraste esas a mano? ¿tomaste parciales en ellas? ¿o hubo otro motivo -un break even que salto, una noticia, cerrar antes de una sesion-?» |
| A-34 | RN-003 (hoy AMBIGUO, no opera) | **parcial** | «Mientras no lo digas, el bot da el sesgo por AMBIGUO en esa sesion y no opera» |

Nota: salvo A-35, los campos `pregunta` mezclan la pregunta con historia y medidas internas
(fechas, ADR, recuentos). **No están escritos para leérselos al trader tal cual**: A-35 es el único
que ya tiene la forma de la pregunta abierta de un informe.

### 3.2 PARA EL CONSULTOR y PARA DATOS

- **PARA EL CONSULTOR: 29.** Las 5 DECIDIDA que no pasan por el trader (A-15, A-17, A-19, A-22
  y A-23: sin acción salvo reabrirlas; A-24 cuenta en TRADER por su confirmación); 22 de
  PROJECT_STATE (PS-02 a PS-05, PS-09 a PS-25 y PS-29); y D-03 y D-04. Las siete contradicciones de
  §5 también las decide el consultor, y van aparte.
- **PARA DATOS: 7.** A-16, A-27 y A-28 (mediciones); PS-01 (marzo), PS-06 (demo de FTMO), PS-26
  (`idealTP`), y D-01 (el lado del libro de FX Replay, que se mide en la plataforma). PS-28 es la
  misma que A-16.

## 4. Duplicados, dependencias y huecos de cara al futuro

### 4.1 Duplicados

- PS-28 = A-16 (la divergencia Oanda/Dukascopy); PS-06 = A-27 + A-28 (la demo de FTMO).
- PS-03 aparece dos veces en PROJECT_STATE (Next Action 7 y Technical Debt «JUNIO SIGUE SIENDO
  `dev`»).
- PS-15 son tres entradas de Technical Debt sobre el mismo detector (temas hermanos, «cuarta
  aparición» y `fecha_grabacion`).
- A-24 (DECIDIDA) y A-35 son la misma pregunta partida: qué pivote, y cuándo está formado.

### 4.2 Dependencias, en orden causal del motor

- **A-35 → RN-004 → RN-005**: sin «formado» no hay `liquidez_m15`, y RN-005 lee el lado de ruido de
  esa liquidez. A-24 ya está decidida; su confirmación va con A-35.
- **A-26 → RN-005**: de qué flujo se lee el lado de ruido cuando M15 va contra H4.
- **A-25** depende de A-35: la vida de una marca solo tiene sentido cuando se sabe cuándo nace.
- **A-21 → RN-008**, la geometría de la entrada, no RN-004 (ver K-04). **A-32** se parte: si el
  nivel es la liquidez de M15, cae en RN-004; si es de M1, en RN-008.
- **A-29 → C-01 → C-02 → RN-011/RN-012**: cuándo nace la orden, a qué precio dentro de la zona y
  dónde acaba la caja. **C-02 → A-18**: las dos hipótesis de A-18 dependen de dónde está el extremo.
- **A-13 → C-06**: qué rompe la zona para el break even, y qué pasa con el stop después.
- **A-30, C-04 y C-05**: la vida de una orden pendiente (fin de ventana, precio que se va, cambio
  de sesión con otro sesgo).
- **A-31 y C-07**: el cómputo de intentos y el tope del día.
- **A-34 → RN-003**: hoy el bot no opera con sesgo AMBIGUO; no bloquea el resto.

### 4.3 Huecos: candidatos C-xx

Pasos que el motor necesitará de RN-005 en adelante **sin ambigüedad abierta ni regla fijada**,
comprobados contra `strategy_spec.yaml`, `glossary.yaml` y `ambiguedades.yaml`. **No se añaden a
`ambiguedades.yaml`: abrirlas lo decide el consultor.**

| id | orden causal | pregunta del motor, neutra | por qué es hueco |
|---|---|---|---|
| C-01 | RN-011 / RN-015 | ¿A qué precio exacto, dentro de la zona de control, se pone la orden límite? | `colocar_orden_limite` lleva solo `en: Z` (`strategy_spec.yaml:323-337`); el veredicto del hallazgo [3] de la auditoría del 2026-09-13 ya lo decía: «hay ancla citable para dónde va la límite (bloque de origen del breaker / zona de control, no un precio suelto) aunque no para el precio exacto» |
| C-02 | RN-011 / RN-012 | ¿Qué punto del mercado marca el extremo de la caja, del que sale el stop? | D-02 |
| C-03 | todo lo geométrico | ¿En qué lado del libro dibuja FX Replay las velas del trader? | D-01. **PARA DATOS**: se mide en la plataforma |
| C-04 | orden pendiente | ¿Qué pasa con una orden límite pendiente si el precio se aleja sin llenarla (p. ej. alcanza el nivel del objetivo) antes del fin de la ventana? | RN-006 solo la reubica al completarse otra zona; A-30 solo cubre el fin de ventana y A-32 la invalidación con mecha |
| C-05 | orden o posición viva | ¿Qué pasa con una orden pendiente o una posición viva cuando empieza la otra sesión H4 con un sesgo distinto? | el sesgo se fija al abrir cada sesión (ADR-0044) y ninguna regla dice qué hacer con lo que viene de la anterior |
| C-06 | tras RN-014 | Después del break even, ¿el stop vuelve a moverse? | RN-014 lo lleva a la entrada; nada dice si se queda ahí hasta el objetivo o el cierre |
| C-07 | RN-016 / RN-017 | ¿Hay un tope de entradas por día, además de los cartuchos por liquidez? | la spec deja escrito que agotar los cartuchos «NO acote el dia» (`strategy_spec.yaml:567-568`), y hay evidencia de «como maximo dos entradas por dia» (`ev-v4-003350-acb03ee7`) que ninguna regla recoge |
| C-08 | F26, no el motor | ¿Cuál es la unidad de fidelidad: la operación o la sesión H4? | D-03. **PARA EL CONSULTOR** |

## 5. Contradicciones en la documentación que manda

Recorridos los ADR, las configuraciones de `knowledge/`, `CLAUDE.md`, los runbooks y
PROJECT_STATE. **No se corrige ninguna.** Comprobado sin hallazgo: toda enmienda entre ADR lleva
su nota en el ADR enmendado salvo K-05; las cifras cruzadas (`stop_fraccion_caja`,
`firma_margen_seguridad`, `sesgo_h4_tope_velas`, umbrales de ADR-0043) coinciden; los ADR citados
en `knowledge/` existen; la tabla Known Ambiguities coincide con el yaml; los tags `stable/*`
están todos en PROJECT_STATE.

| id | tipo | lado A (cita) | lado B (cita) | manda | afecta a | gravedad |
|---|---|---|---|---|---|---|
| K-01 | índice | `PROJECT_STATE.md`, «Architectural Decisions (index)»: salta de ADR-0044 a ADR-0046 y a ADR-0039; **ADR-0045 no está** (CONFIRMADO: solo aparece fuera del índice) | `docs/adr/README.md`: «\| 0045 \| La liquidez de M15 es el pivote mas reciente ya formado \| ACTIVE \|» | el ADR existe y está ACTIVE: falta la línea | documentación | MEDIA |
| K-02 | índice | `scripts/` contiene `mover_sesion.py` | `scripts/README.md` lista los demás y no lo nombra (lo documenta `knowledge/cases/kit/README.md`, «Si cambia la fecha de la sesion») | el disco | documentación | BAJA |
| K-03 | pendiente hecho | `PROJECT_STATE.md:445` (Technical Debt): «El arreglo del runbook queda pendiente en Next Action 5» | `PROJECT_STATE.md`, Next Action 5: «**HECHA en `trabajo/ritual-ventanas`**» | Next Action 5 (la rama cerrada) | documentación | MEDIA |
| K-04 | regla en dos sitios | `PROJECT_STATE.md:39` y Next Action 22: «RN-004 sigue BLOQUEADA por A-21 y A-35» | `strategy_spec.yaml`: RN-004 cita A-24 y A-35 (`:429`, `:732`) y **ninguna regla cita A-21**; A-21 trata de la zona de control limpia, que es geometría de la entrada (RN-008) | la spec; qué bloquea A-21 lo decide el consultor | **motor** (qué regla espera a quién) | **ALTA** |
| K-05 | ADR sin nota | ADR-0011:16: «Se cierra una ambiguedad solo con un registro del trader, en un commit con `Fuente:`» | ADR-0022 §7: «**Nace el estado `DECIDIDA`** [...] hasta hoy el fichero solo admitía cerrarlas con feedback del trader» | ADR-0022 (posterior); ADR-0011 no lleva nota | documentación (la guardia ya aplica ADR-0022) | BAJA |
| K-06 | cifra | `CLAUDE.md:72`: «solo **8 fotogramas distintos, citados por 9 items de 365**» | `knowledge/evidence/`: 368 ítems hoy, y las ramas de A-35 y v5 citaron y midieron más fotogramas | el repositorio; el texto está fechado el 2026-09-17 pero se lee como presente | documentación | BAJA |
| K-07 | cifra / regla | `parametros.yaml:214-227`, `huso_grafico` CONFIRMED `Europe/Madrid`: «su plataforma muestra su hora local, que es la misma de huso_operativa» | `CLAUDE.md:150`: «**EL RELOJ DE LOS GRAFICOS DE FX REPLAY ES UTC+2 FIJO.** Medido en el propio grafico de v4 sobre un fotograma de ENERO -asi que NO es Europe/Madrid»; ADR-0039:64, «(es UTC+2 fijo)» | `parametros.yaml` es la única puerta (ADR-0002), pero la medida es posterior y ningún ADR la lleva al registro; lo decide el consultor | toda comparación vídeo-velas y la traducción de lo que el trader dice a un instante; ninguna regla consume `huso_grafico` | MEDIA |

Recuento: **7**. ALTA 1 (K-04), MEDIA 3 (K-01, K-03, K-07), BAJA 3 (K-02, K-05, K-06). Motor 1,
holdout 0, documentación 6 (K-07 toca mediciones, no reglas).

## 6. Lo que sigue en esta rama

La parte B busca en las transcripciones los candidatos C-01, C-02, C-04, C-05, C-06 y C-07, por
orden causal. Quedan fuera C-03 (se mide en la plataforma, no en lo que dice el trader), C-08 (es
del consultor) y A-18 (su búsqueda ya se hizo: 0 de 42).

## 7. Cómo se hizo

- La sesión 01 y el inventario de ambigüedades y de la sesión 01, por lectura directa y por
  script sobre los yaml, sin leer respuestas del trader.
- El barrido de contradicciones (K-01 a K-03) y el de dudas y huecos, por dos agentes de solo
  lectura con las mismas guardias; K-04 a K-07 y los candidatos C-01, C-04, C-05, C-06 y C-07, por
  la sesión, comprobados contra la spec.
- Nada de `corpus/`, `data/`, `knowledge/cases/holdout/` ni `knowledge/cases/dev/` se ha abierto.

## 8. Para preparar la sesión 02 (observaciones, sin decidir)

- **No hay runbook de sesión.** El procedimiento de §1(a) está repartido en cinco documentos.
- **La ceguera de la sesión 02 ya no es la de la sesión 01**: `knowledge/cases/kit/README.md` dice
  que en la sesión 2 «solo son ciegos sus `dev` de junio», y que la confirmación escrita «tiene que
  decir expresamente que no ha backtesteado junio». Junio está además en PS-03.
- **El día de grabación** puede caer en una partición reservada, como v6 (§1(d)).

## Estado

PARTE A CERRADA: inventario y auditoría. La parte B (búsqueda de los candidatos) va en commits
propios.
