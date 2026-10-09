# PROJECT STATE

> Lo que es verdad HOY. Que va aqui, que va a `docs/state/HISTORIA.md` y como se archiva:
> `docs/state/README.md`.

## Current Branch
trabajo/demo-ejecucion-1

## Current Feature
`trabajo/demo-ejecucion-1` EN CURSO: la ejecución 1 de MedirDemoFTMO (punto A de la Next Action): congelar el CSV, inventario medida → decisión con PARADA, y después fijar los valores de ADR-0057 y A-27 que decida el consultor. Encargo docs/encargos/trabajo-demo-ejecucion-1.md; informe docs/validation/DEMO-EJECUCION-1.md.

## Stable Main State
f6d3117 · merge de `trabajo/adelgazar-estado` (tag `stable/F37h-adelgazar-estado`): salen de PROJECT_STATE 12 lineas por el criterio (a)-(d), literales en HISTORIA con su evidencia; las introducciones apuntan a docs/state/README.md; la Next Action cambia entera en el commit del contrato (punto Y); DEMO-FTMO.md lleva la prueba de octubre de 2026. Sobre `stable/F37g-guion-mismo-comando` (8d1578d). Informe docs/validation/ADELGAZAR-ESTADO.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
f6d3117 · merge: PROJECT_STATE adelgazado, punto Y en RITUAL y la prueba de octubre de FTMO (ADELGAZAR-ESTADO.md) · tag stable/F37h-adelgazar-estado

## Tests Currently Passing
1425 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-10-08). El orden lo decide el consultor en cada encargo; cada entrada dice de qué depende.

S. Backtest de JULIO recibido el 2026-10-04 (xlsx, vídeo y fotos del trader), SIN ABRIR y fuera del repo. Entra por su propia rama DESPUÉS de Q, de la activación de la sesión 4 y de la primera ejecución de la demo de FTMO. Antes de esa rama, el consultor decide si es material de construcción o reservado, y lo comprueba en el repo (año del mes, casos_ocultos, casos_reservados, meses_reservados.yaml). En el v10 el trader ya comentó en pantalla operaciones de julio (HOLDOUT-EXPOSICIONES, fila del 2026-10-04). Nadie abre nada hasta entonces, ni miniaturas de las fotos. La condición de la primera ejecución de la demo de FTMO está cumplida (2026-10-09, DEMO-EJECUCION-1.md).

B. La guardia lee el guion pero no lo que importa o ejecuta a su vez (import de un módulo local, runpy, exec, subprocess con otro guion), ni en un guion ni en el código en línea (GUION-MISMO-COMANDO.md §0.c). Rama propia: decidir qué módulos se resuelven y se leen, negando por defecto lo que no se pueda resolver.

C. La guardia no ve una ruta protegida compuesta por partes dentro de un guion (joinpath, os.path.join, el operador /, f-strings, concatenación): analizar_codigo solo mira literales enteros y niega lo compuesto solo si el código además recorre directorios (GUION-MISMO-COMANDO.md, hallazgo 5 del consultor). Rama propia: negar por defecto un guion que nombra un fragmento sensible y compone rutas, con un test que lo rompa a propósito.

D. Endurecer la guardia por formas raras de bash, git, awk, sed y PowerShell que ninguna sesión usa (lista en GUION-MISMO-COMANDO.md §1.26). Rama propia, sin prisa: la barrera real sigue siendo el código.

W. Antes del paso b de la rama de entrada de marzo: cases/ (kit, fidelidad, ingesta y hoja) cuenta la ventana de cada caso por la rejilla y no en huso_operativa; si no, del 9 al 27 de marzo la ventana congelada en ventanas.yaml sale una hora tarde (ACTIVACION-A42.md §3.6 y §6.2, ADR-0069).

X. La rama que baje ticks de un mes de invierno pasa scripts/ticks_spread.py a la rejilla: hoy cuenta la ventana de ticks en huso_operativa (ACTIVACION-A42.md §6.2, ADR-0069 §5).

Z. CLAUDE.md (párrafo «Marzo de 2026 esta RECIBIDO y SIN ABRIR») dice que marzo no se sortea ni se ingiere hasta que A-42 esté RESUELTA, y lo está desde stable/F37d-activacion-a42 (ADR-0069). La rama de entrada de marzo, en su primer commit, mide contra docs/runbooks/ENTRADA-MARZO.md (PARADA B0) y ACTIVACION-A42.md qué sigue bloqueando y corrige ese párrafo; W va antes de su paso b (ADELGAZAR-ESTADO.md §0).

A. **Demo de FTMO: las ejecuciones 2 y 3 de MedirDemoFTMO** (las hace Aleks; docs/runbooks/DEMO-FTMO.md). La ejecución 1 se hizo el 2026-10-09 en la prueba gratuita del 2026-10-08 y fijó lo que no depende de la fecha (ADR-0071, docs/validation/DEMO-EJECUCION-1.md; A-27 DECIDIDA). Las 2 y 3, en una segunda prueba creada el 26 de octubre desde el mismo registro, con el script 1.1: antes de la ejecución 2 Aleks copia y compila el script 1.1 (F7, 0 errors), y el CSV de la ejecución 2 tiene que decir 1.1. La 2 entre el 26 y el 30 de octubre, la 3 después del 1 de noviembre. Miden A-28 (el desfase en invierno y el calendario del servidor: 180 min el 2026-10-09), repiten el nivel exacto de ADR-0057 §2 (filas 39-42), los deslizamientos (DN-3) y los swaps, y la 2 mide la comisión con 1,00 lote (ADR-0071 §3). Con cada CSV, rama para congelarlo y fijar lo que mida; si la ficha de EURUSD difiere, A-27 se reabre con otro ADR.

O. Para Aleks, con FTMO: la pregunta P-D1 (DEMO-EJECUCION-1.md §0.c): si la cuenta 2-Step Swing real es hedging como la prueba y si su volumen máximo en EURUSD es 50 o 100. La respuesta se registra parafraseada (RESPUESTAS-FTMO).

K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; se decide en la activación.

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y NO se renueva cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres). Se renueva por condición, según docs/runbooks/RENOVAR-CIERRES.md: (1) cuando una simulación pida días posteriores a hasta, porque el simulador sale con exit 2 y los nombra, se renueva hacia atrás con las Trading Updates archivadas, en rama propia; (2) antes de que el bot corra en tiempo real (demo o real), la rama que lo conecte trae la lectura de SymbolInfoSessionTrade (ADR-0068 §4) o un procedimiento que cierre el hueco del jueves por la mañana, y sin una de las dos esa rama no se cierra.

### Pendientes heredados (sin verificar)

Del Next Action viejo, sin evidencia de estar hechos; texto entero y criterio de salida:
`docs/state/README.md`.

- 2. MARZO INTERRUMPE LO QUE HAYA EN VUELO CUANDO LLEGUE. El trader confirmo el 2026-09-21 que no habia visto…
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. EL DUEÑO, EN PARALELO: no comprar todavia -confirmar en el panel de FTMO que el tipo Swing existe para…
- 12. **MARZO, AL LLEGAR, ENTRA POR SU PROPIA RAMA**: declaracion en `knowledge/corpus/libros.yaml` con formato…
- 15. **EN ESPERA: A-18: pregunta de reserva enviada al trader el 2026-09-23** (lo declara el consultor; es la…
- 25. **RN-004, bloqueada SOLO por A-35** (K-04, docs/validation/SESION-02-DECISIONES.md §1): A-21 es la zona…
- 27. **PENDIENTE PARA ALEKS, CON FTMO:** donde esta la linea entre operar con noticias en Swing y el gap…
- 30. **DESPUES DE LA SESION 02: RN-004 TRAS A-35, medida con el arnes y mirada con el visor** (`botsito motor…
- 34. **PENDIENTES QUE DEJA `trabajo/ticks-llenado`, con dueno** (ADR-0051 §7): (a) la VENTANA DE TICKS DE…
- 35. **DESPUES DE LA SESION 02: RN-020 TRAS A-44.** Con A-44 respondida -que perdida hace que el trader deje…
- 37. **PENDIENTE: LOS RECHAZOS POR VOLUMEN MAXIMO, EN LA RAMA DE STOP Y LOTE (A-18)** (2026-09-28, orden de… · Desde ADR-0071 (2026-10-09) el maximo es 50 lotes, no 100: con riesgo_por_operacion (0,5 %) sobre 100.000 y 10 USD por lote y pip, corta todo stop de menos de 1 pip (ADR-0071 §2).

## Known Ambiguities
Las ABIERTAS, exactamente (`tests/unit/test_kit.py`); de donde salen: `docs/state/README.md`.

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-18 | base sobre la que se mide el objetivo 1:3 | pregunta | no | F11, F26 |
| A-21 | que es una zona de control limpia, sin ruido | pregunta | si | F12, F20, F26 |
| A-25 | la vida de la marca de liquidez de M15 | pregunta | no | F19, F20 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-30 | la orden limite pendiente al llegar el fin de la ventana | pregunta | no | F22, F23 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-33 | tres ganadoras que cierran por debajo de 3R | pregunta | no | F20, F24, F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-36 | en qué punto de la mecha va la orden límite | pregunta | no | F20, F22 |
| A-39 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | pregunta | no | F22, F23 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-51 | qué corta la racha de 9 pérdidas seguidas del trader y cuándo vuelve a operar | pregunta | si | F11, F18 |
| A-52 | cuántos escenarios puede abrir una misma sesión como máximo | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.

- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril). Sigue viva solo la parte de la serie: el reloj quedó corregido el 2026-10-06 (ADR-0069: Europe/Madrid).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- `maxTP` ES EL PRECIO DE CIERRE DE LAS GANADORAS, NO LA EXCURSION MAXIMA (2026-09-21).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- CUARTA APARICION DEL PUNTO CIEGO DEL DETECTOR, CON DIMENSION NUEVA: LA RECENCIA (2026-09-21).
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
Las que solo viven aqui (`docs/state/README.md`).

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

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo; el cierre no anade nada (`docs/state/README.md`).
— ninguna desde el Archivo 25 (2026-10-09).

## Change Log
Las entradas desde el ultimo archivo; el cierre no anade ninguna (`docs/state/README.md`).
— ninguna desde el Archivo 25 (2026-10-09).
