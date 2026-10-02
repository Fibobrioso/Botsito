# PROJECT STATE

> Memoria operativa: lo que es verdad HOY, y nada mas. Una sesion nueva lee este fichero y
> `CLAUDE.md`; lo demas, solo si la tarea lo pide (`CLAUDE.md`, «Por donde se empieza»).
>
> **Lo que dejo de ser presente vive en `docs/state/HISTORIA.md`, que solo se amplia**: la historia
> de merges, las funcionalidades cerradas, el Change Log, los bloques «LO QUE DECIA…», las deudas
> pagadas, el indice de ADR (que vive en `docs/adr/README.md`), los componentes y los ficheros
> importantes. Desde el 2026-10-01 (`trabajo/dieta-y-skills`) aqui se SUSTITUYE lo que deja de ser
> verdad, sin «Lo anterior:», y al abrir cada rama se archiva en HISTORIA el `PROJECT_STATE.md` de
> `main` (docs/state/README.md, skill `abrir-rama`). Tope: 25 KB (`tests/unit/test_project_state.py`).

## Current Branch
main

## Current Feature
NINGUNA ABIERTA tras `stable/F36l-cuarentena-por-defecto`.

## Stable Main State
8a3b501 · merge de `trabajo/cuarentena-por-defecto` (tag `stable/F36l-cuarentena-por-defecto`), sobre `stable/F36k-dieta-y-skills` (0744ece). La CLI ensena el corpus filtrado por defecto -sesiones en cuarentena, tramos no citables y material reservado o sin sortear, con `src/botsito/corpus/cuarentena.py` como unica fuente- y dice cuanto oculto y por que; la evidencia tiene su propio criterio (solo un tramo no citable o un dia de `casos_ocultos`); la opcion que lo ensena todo y su equivalente en Python, solo para Aleks y para las funciones de `AUTORIZADOS`; la guardia bloquea esa opcion y 14 ficheros que copian texto oculto. Informe docs/validation/CUARENTENA-POR-DEFECTO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
8a3b501 · merge: la CLI enseña el corpus filtrado por defecto (cuarentena, tramos no citables y material reservado), la evidencia con su propio criterio y la guardia bloquea el contenido sin filtrar · tag stable/F36l-cuarentena-por-defecto

## Tests Currently Passing
1149 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-09-30, orden de cierre de `feature/nocturno-01oct`; el I, 2026-10-01, al cerrar `trabajo/guardias-claude`), en este orden:

A. **Demo de FTMO: tres ejecuciones de MedirDemoFTMO**, la primera antes del 25 de octubre (las hace Aleks; docs/runbooks/DEMO-FTMO.md). Con el primer CSV, rama para fijar los valores de ADR-0057 y A-27.

E. **A-42 RESUELTA con el trader en la sesion 4, no por ADR** (orden del consultor del 2026-09-30, docs/validation/REGISTRO-MARZO.md): es la pregunta del reloj de invierno de docs/sesion-4/PREGUNTAS.md, y marzo no se sortea ni se ingiere hasta entonces (PARADA B0, sin cambio). Era: **A-42 decidida antes del 25 de octubre** (el cambio de hora; el mecanismo ya esta: `reloj_sesiones`, ADR-0063).

F. **Preguntas para la sesion 4 con el trader** (HOJA HECHA tras el barrido del corpus, 2026-09-30, `stable/F36e-barrido-sesion-4`: docs/sesion-4/PREGUNTAS.md, 19 por preguntar -las 17 del barrido y 2 que anadio el consultor al cerrar `feature/registro-marzo`, la primera y la ultima- y 15 ya respondidas; lo que sigue es lo que la origino): el bloque, R1 o R4; la caja con la vela en curso; el stop en el 0,8 o en el 1; el umbral de la vela casi plana (RN-007); la doble ruptura sin cuerpo (ADR-0060 §2); el redondeo, un punto o un pip (ADR-0061 §2); el reloj de invierno (A-42); el break even al tick (ADR-0061 §5); la confirmacion grabada de A-47; y «¿pones la orden en el ultimo minimo (o maximo) que se formo en M1 y la vas moviendo cuando se forma uno nuevo?» (CAJA-77 §3.3).

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3).

I. **HECHA, `stable/F36l-cuarentena-por-defecto` (2026-10-01).** Queda una sola cosa de lo que decia: el comentario de `knowledge/corpus/tramos_no_citables.yaml` no se cambio, porque el encargo protegia `knowledge/`. Era: **Rama nueva: la cuarentena y los tramos no citables en la CLI** (orden del consultor del 2026-10-01, al cerrar `trabajo/guardias-claude`; docs/validation/GUARDIAS-CLAUDE.md §0 fila 36 y §7): «kb find, kb at, transcript show y corpus frames show respetan por defecto la cuarentena y tramos_no_citables; la salida cruda exige una opcion explicita que el hook bloquea». Hoy esos cuatro comandos imprimen el segmento crudo de v7, v8 y v9 y los tramos de v6, y solo los para el hook de Claude Code (`.claude/hooks/guardia.py`). En esa rama, tambien el comentario de `knowledge/corpus/tramos_no_citables.yaml` que dice que un tramo «se puede leer y buscar con `kb find`». Mayo queda como esta.

J. **Pendiente del consultor: umbral de cobertura tras la sesión 4 para pasar al plan híbrido, pre-registrado antes de medir.** (encargo de `trabajo/dieta-y-skills`, punto 5: el umbral no lo escribe la sesion.)

B, C, D y G de esa lista, HECHAS, estan tal cual en docs/state/HISTORIA.md (Archivo 1, «Next Action»); de ellas sigue pendiente lo que D dice -«El item nuevo ev-v7-001550-82e5cffc espera la revision del consultor»- y lo que G dice: «pendiente para la demo de FTMO, el break even de una venta que salta por el ASK (ADR-0065 §6)».

### Pendientes heredados (sin verificar)

Los puntos del Next Action viejo (Archivo 1 de docs/state/HISTORIA.md, donde esta su texto entero) que no tienen evidencia de estar hechos -commit, tag, ADR o test-, uno por linea con su arranque literal; la evidencia, punto por punto, en docs/validation/DIETA-Y-SKILLS.md §6. Las ramas a), c) y 0) de A3 si la tienen y solo estan en HISTORIA. Se quitan de aqui cuando haya evidencia o lo decida el consultor.

- A2. **Aleks ejecuta MedirDemoFTMO en la demo de FTMO** (docs/runbooks/DEMO-FTMO.md), tres ejecuciones: antes…
- A3. **Ramas de codigo, en este orden** (orden del consultor del 2026-09-29):
- b) **sesiones independientes y varios escenarios por sesion**: `liquidez_tomada` caduca al abrir la sesion…
- d) **vida de la orden stop** (RN-006, rama 3 de ADR-0056) y RN-007 (la vela casi plana; falta el umbral);
- e) **calendario de cierres de mercado** para la regla de gap trading de FTMO (Technical Debt, 2026-09-29).
- A4. **La memoria de la suite: EN REVISION en `trabajo/memoria-suite`** (docs/validation/MEMORIA-SUITE.md). El…
- A5. **Para la sesion 4 con el trader**: confirmar A-42 (dijo «creo»); las siete ganadoras anotadas de mas de…
- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 22. **SIGUIENTE: la sesion 02 con el trader, con A-35 y A-44 como PRIORIDAD** (desde ADR-0049 A-43 va en la…
- 23. **MARZO: RECIBIDO el 2026-09-30 y SIN ABRIR** (`stable/F36f-registro-marzo`,…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 36. **EN MARCHA (el script existe desde `stable/F26-demo-ftmo-script`; lo ejecuta Aleks, punto A2): MEDIR EN…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de…

## Known Ambiguities
Las ABIERTAS. La fuente es `knowledge/spec/ambiguedades.yaml`, y `tests/unit/test_kit.py` exige que
esta tabla tenga exactamente sus ids `ABIERTA`, con el mismo titulo, clase y bloqueante: abrir una
anade su fila; cerrarla (RESUELTA o DECIDIDA) la quita. La pregunta entera y su historia, en
`docs/spec/ambiguedades.md` (generado); las cerradas y la tabla con sus notas hasta el 2026-10-01,
en docs/state/HISTORIA.md (Archivo 1, «Known Ambiguities»).

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-27 | las especificaciones de EURUSD en FTMO | medicion | no | F17, F33 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-29 | cuando nace la orden limite | pregunta | no | F20, F22 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-42 | con qué reloj cuenta el trader su horario de operar de 07:00 a 15:00 | pregunta | si | F14, F26 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA: el arranque literal de su entrada; el texto entero, buscando esa frase
en docs/state/HISTORIA.md (Archivo 1, «Technical Debt»). Una deuda nueva entra con una linea que
apunte a su informe; una pagada se borra de aqui. Las entradas que su propio texto ya daba por
cerradas el 2026-10-01 (RESUELTA, CORREGIDA, DECIDIDA, CERRADA, HECHO…) solo estan en HISTORIA, y
la de los cinco patrones de defecto, que es una regla, esta entera en
docs/runbooks/ERRORES-RECURRENTES.md.

- PENDIENTE DE FTMO: EL BOT PUEDE ABRIR DENTRO DE LAS DOS HORAS PREVIAS A UN CIERRE DE MERCADO DE DOS HORAS O MAS, EN UN DIA DE CIERRE ANTICIPADO O FESTIVO (2026-09-29, `trabajo/sesion-03`, docs/validation/FTMO-REGLAS.md, recuadro de la respuesta del soporte, ticket VDW-DPMWR-965).
- EL BROKER SIMULADO LLENA AL INSTANTE UNA LIMITE COLOCADA CON EL PRECIO YA PASADO EL NIVEL (2026-09-28, `trabajo/orden-stop-o-limite`, docs/validation/ORDEN-STOP-O-LIMITE.md §8 y §10c).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- LA LECTURA PREVIA DE LA TRANSCRIPCION DE v6, DECLARADA COMO EXPOSICION POSIBLE (2026-09-23, `trabajo/a18-transcripciones`, en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
- LOS CINCO PATRONES DE DEFECTO QUE SE COMPRUEBAN EN CADA RAMA (el tercero, anadido el 2026-09-21 en la rama F14a; el cuarto y el quinto, el 2026-09-22, en la rama de la caja y en la del runbook). Entera, tal cual, en docs/runbooks/ERRORES-RECURRENTES.md.
- LA PRIMERA MEDIDA DE A-18 SALE DEL MATERIAL, NO DE LA SESION, Y SE REPITE SOBRE MAYO (2026-09-21, rama F14a, informe §4).
- F26 NO PUEDE PUNTUAR EL OBJETIVO HASTA QUE A-18 ESTE CERRADA (2026-09-21).
- `idealTP`: UNA COLUMNA DEL MATERIAL QUE NO SABEMOS QUE ES Y NO USAMOS (2026-09-21, rama F14a, ADR-0037 §7).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO. BLOQUEANTE ANTES DE LA PRIMERA AUTORIZACION (2026-09-21, medido en la rama de la puerta por pregunta; ADR-0033 enmienda §Lo que NO cierra, ADR-0036 §6).
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Transcripciones heredadas (Whisper tiny, `_procesado/`): se conservan como historia y NO se citan; F07 cita solo sobre la transcripcion `tr-*` activa (decision 4 del informe F04, confirmada por el usuario el 2026-09-05).
- Copia de seguridad de las crudas activas y los WAV fuera de esta maquina: HECHA HASTA v5, INCOMPLETA desde el 2026-09-09.
- v5 (`corpus/Estrategia del trader/2026-09-05 21-03-59.mkv`, 121,5 MB) en Drive desde el 2026-09-06 (`drive_id` `1VP1ATfgqkkYf88blLeax1Ir2WaXycWcS`, en la subcarpeta de transcripciones, no en la raiz de "Estrategia del trader"; anotado en `fuentes.yaml`).
- `data/fotogramas/` (8,9 GiB los 4 videos de F05 mas 0,15 GiB de v5) no se copia a Drive: se regenera en ~10 min desde los videos; si otra build de ffmpeg decodifica distinto, `extract` lo delata y la salida es otro manifiesto con `--reemplaza-a`.
- F07, limitacion declarada: el proponente de las 20 propuestas, el autor de la lista de referencia (golden) y el primer filtro fueron la misma sesion (`claude-fable-5-1`); no hay cliente de API de LLM (sin clave).
- Hook local: tras cambiar `scripts/git-hooks/`, ejecutar `make hooks` (el 2026-09-07 la copia instalada no protegia `knowledge/corpus/fotogramas`; los tests de historial en CI son la garantia real).
- `data aggregate` con una ventana fuera del dataset devuelve solo cabeceras (con AVISO en
  stderr desde la auditoria); F14 debe tratar la ventana vacia como error del caso.
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.
- F11: las reglas de `strategy_spec.yaml` son PROSA citada y validada, no codigo; que el motor haga lo que dicen lo cierra F12 (validacion semantica).

## Reglas vivas
Las que hasta el 2026-10-01 solo estaban en este fichero, copiadas tal cual con su titulo de
entonces. Las demas viven en `CLAUDE.md` y en `docs/runbooks/`.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validacion de fidelidad (F26) precede a cualquier MQL5.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Umbrales pre-registrados no se relajan tras ver resultados. · Un holdout abierto queda quemado (que es "abrir" lo define ADR-0021; las exposiciones se declaran en `docs/validation/HOLDOUT-EXPOSICIONES.md`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.
- 2026-09-25 · Sobre el informe SIMULADOR-CUENTA §5 (ADR-0050), al validar: `firma_huso_corte` se queda en el perfil de cuenta, vigilado por el test de las medianoches de un ano contra `huso_operativa` (no contradice ADR-0027 §alt. 3, que hablaba de la spec); la guardia de tamano de posicion sin cifra NO impide correr, porque es solo aviso; y se acepta la duplicacion de los `firma_*` comunes entre el perfil y `parametros.yaml` mientras el test que los cruza la vigile. Estado: ACTIVE.
- 2026-09-25 · `firma_comision_por_lado` toma el SUPUESTO CONSERVADOR: la comision se cobra en cada lado (apertura y cierre), con fuente decision del consultor, hasta que FTMO confirme si es por lado o por operacion completa (R12, NO ENCONTRADA). PENDIENTE DE IMPLEMENTAR en la proxima rama: hoy el perfil lo lleva UNKNOWN. Estado: ACTIVE.
- 2026-09-30 · Marzo entra por el camino de fidelidad (ADR-0036, ADR-0046) como mes reservado para medir fidelidad, con el artefacto `eurusd-2026-03`, los cupos de la regla y la semilla AAAAMMDD fijada por el consultor antes del sorteo (REGISTRO-MARZO.md §4, aceptada). A-42 se cierra como RESUELTA con el trader en la sesion 4 y NO como DECIDIDA por ADR: la PARADA B0 de ENTRADA-MARZO.md queda como esta. Las 7 imagenes del backtest de marzo no se abren y quedan fuera del protocolo; se pregunta al trader que son. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli. `state check`
(regla 4) mira las dos.
— ninguna desde el Archivo 2 (2026-10-01).

## Change Log
Las entradas desde el ultimo archivo de docs/state/HISTORIA.md; las anteriores, alli.
— ninguna desde el Archivo 2 (2026-10-01).
