# PROJECT STATE

> Lo que es verdad HOY. Que va aqui, que va a `docs/state/HISTORIA.md` y como se archiva:
> `docs/state/README.md`.

## Current Branch
trabajo/punto-usado

## Current Feature
trabajo/punto-usado EN CURSO (abierta el 2026-10-18 desde main f96b581; Y de la Next Action, R3.4): qué gasta un punto (un ADR nuevo enmienda la decisión 1 de ADR-0064), con sus tests que rompen en main y la corrida de R3.1 repetida. Encargo: docs/encargos/trabajo-punto-usado.md. Informe: docs/validation/PUNTO-USADO.md.

## Stable Main State
3ae2933 · merge de `trabajo/plataforma-adelantada` (tag `stable/F37u-plataforma-adelantada`): ADR-0082, la capa de MT5 que nunca decide una operación va antes de F26, en el EA de MQL5 (enmienda MASTER_PLAN §0, la regla de PROJECT_STATE, ADR-0067 §1 y ADR-0068 §4); el tramo R6a de la hoja de ruta; PROJECT_STATE adelgazado; solo documentos. Sobre `stable/F37t-visor-construccion` (7d3783d). Informe docs/validation/PLATAFORMA-ADELANTADA.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
3ae2933 · merge: trabajo/plataforma-adelantada, ADR-0082 (la capa de MT5 que no decide operaciones, antes de F26), el tramo R6a y PROJECT_STATE adelgazado · tag stable/F37u-plataforma-adelantada

## Tests Currently Passing
1603 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-10-08). El orden lo decide el consultor en cada encargo; cada entrada dice de qué depende.

B. La guardia lee el guion pero no lo que importa o ejecuta a su vez (import de un módulo local, runpy, exec, subprocess con otro guion), ni en un guion ni en el código en línea (GUION-MISMO-COMANDO.md §0.c). Rama propia: decidir qué módulos se resuelven y se leen, negando por defecto lo que no se pueda resolver.

C. La guardia no ve una ruta protegida compuesta por partes dentro de un guion (joinpath, os.path.join, el operador /, f-strings, concatenación): analizar_codigo solo mira literales enteros y niega lo compuesto solo si el código además recorre directorios (GUION-MISMO-COMANDO.md, hallazgo 5 del consultor). Rama propia: negar por defecto un guion que nombra un fragmento sensible y compone rutas, con un test que lo rompa a propósito.

D. Endurecer la guardia por formas raras de bash, git, awk, sed y PowerShell que ninguna sesión usa (lista en GUION-MISMO-COMANDO.md §1.26). Rama propia, sin prisa: la barrera real sigue siendo el código.


F. Y → V. Las ramas de R6a (ADR-0082) van en los huecos de espera y no le quitan turno ni a Y ni a V.

Y. Que el punto de una orden ya llenada no se vuelva a colocar con otra caja (ADR-0064, decisión 1): hoy se marca la zona y no el punto; en la corrida 2, hasta 47 órdenes en 22 sesiones van al 0 de una ya llenada (VISOR-CONSTRUCCION.md §2.d.4). Rama de código, con su test y la corrida 2 repetida.



T. Transcribir v11 a v14 (backtest de julio en vídeo, 2 h 38 min, con audio), comprobar qué días cubre cada uno, compararlos con el xlsx en los días 1 a 17 y con las horas del libro (el primero en Europe/Madrid); en su rama (ENTRADA-JULIO.md §5).

U. Julio 20-31: solo en vídeo (v14); decidir si se extraen casos del vídeo, tras transcribir v11-v14. Depende de T.

G. PREREGISTRO.md está SIN RELLENAR: no se abre ningún holdout y F26 no empieza. Antes, el consultor fija cuántos días reservados necesita F26 (y si hay que pedir otro mes al trader), con las condiciones previas que hoy viven en Technical Debt (una pregunta abre N particiones, los dos días sin partición, F26 y A-56, la regla del objetivo frente al material, ADR-0073) y A-16. Holdout-3 tiene un día medido menos desde el 2026-10-14 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta. fidelidad-1 tiene 3 días medidos menos desde el 2026-10-17 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta.

I. Backtest de DICIEMBRE de 2025, recibido el 2026-10-09 (xlsx y capturas de estadística, SIN vídeo), SIN ABRIR y fuera del repo; las capturas son de Analytics y no se abren nunca. Entra por su propia rama después de renovar hacia atrás el calendario de cierres (RENOVAR-CIERRES.md, condición 1); julio ya entró (ADR-0078). Antes, el consultor decide si es construcción o reservado, teniendo en cuenta que no trae vídeo. En v10 el trader ya comentó operaciones de diciembre (HOLDOUT-EXPOSICIONES, 2026-10-04).

J. kit hoja falla en main para todo paquete nuevo: busca una pregunta nacida de A-9 que el cuestionario de hoy ya no trae (CASES-REJILLA.md). Rama propia antes de la próxima sesión con el trader que use la hoja.

A. **Demo de FTMO: las ejecuciones 2 y 3 de MedirDemoFTMO** (Aleks; detalle en docs/runbooks/DEMO-FTMO.md): la 2 entre el 26 y el 30 de octubre, con el script 1.1 compilado antes; la 3 después del 1 de noviembre. Miden A-28, el nivel de ADR-0057 §2, deslizamientos, swaps y la comisión con 1,00 lote. La ejecución 2 comprueba la fórmula del margen con `MargenAlcanza` (FTMO-P-D1.md §3), y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4). Y, opcional: Aleks, el calendario de las noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en `corpus/noticias/` como CSV `fecha_utc,hora_utc,divisa,evento`; `stops_cortos.py --noticias <csv> --ventana-min 2` da la medida (MARGEN-LOTE.md §2.b).

K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos. Y en la misma rama, los dos arreglos de ENTRADA-JULIO.md §8: que `ffprobe` y `ffmpeg -i` sobre un vídeo lean y no ejecuten; y que reconozca como tests los de un clon `git worktree add --detach` de comparar-con-main (`C:/cm/`); cada uno con su test de los dos sentidos.

H. **RN-007, la vela casi plana: espera a la pregunta 14 de la sesion 4** (el umbral de «casi plana», que el trader no dio). RN-007 ya lo dice en su texto, pero sin umbral no hay rama de codigo y su forma ejecutable no cambia (docs/validation/REFLEJAR-FEEDBACK-S3.md §1.3). Respondida en parte en S-14; si el literal de 1:44:49 es «1 o 2» o «12» lo lee Aleks con `--crudo` en su terminal (punto 8 de la respuesta del consultor del 2026-10-11); S-14 va a la sesión 5 (R4.1).

Q. El trader da por bueno el backtest de agosto grabado en vídeo (S-16, sesión 4; ADR-0073 §5); Aleks le pide su exportación; hasta que llegue, los casos dev de agosto siguen saliendo del xlsx; al llegar, entra por su propia rama (libros.yaml solo se amplía) y ADR-0040/A-56 se revisan. Julio ya entró por su xlsx (ADR-0078); su exportación cubre solo del 1 al 17.

V. Preparar, celebrar y activar la sesión 5 (R4.1): las «en parte» de ACTIVAR-SESION-04.md §0.e y §5 y ACTIVAR-SESION-04-MOTOR.md §5 y §6 (A-13, A-32, A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14, que es H) y las preguntas de esos §5; si el xlsx de julio es la exportación de v11 a v13 (ENTRADA-JULIO.md §8); y la lista «Para el cuestionario de la sesión 5» de CORRIDA-CONSTRUCCION.md §4.5 con su pregunta 1 sustituida por las dos de SESGO-H4-COLOR.md §4.4 (la ruptura simple sin cuerpo, D3 de ADR-0080, y la contradicción con la sesión 1, con un esquema dibujado), en su orden; A-57 (el lote que no cabe, MARGEN-LOTE.md §5); y las preguntas de VISOR-CONSTRUCCION.md §3.2. Depende de R1.1, de R3.1, de Y, de J (kit hoja) y de la copia de seguridad (A.4).

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y se renueva por condición, no cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres; docs/runbooks/RENOVAR-CIERRES.md). La condición 2 la cumplirá R6a.1, que trae la lectura de SymbolInfoSessionTrade, y R6a.5 la usa (ADR-0082 D6).

### Pendientes heredados (sin verificar)

Del Next Action viejo, sin evidencia de estar hechos; texto entero: `docs/state/HISTORIA.md`;
criterio de salida: `docs/state/README.md`.

- 2. Marzo: faltan vistos.yaml, la confirmacion escrita del trader y el paso a (hoja de ruta, R5.3 y A.3).
- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. De la demo de FTMO quedan A-28 y el grabador de spread y ticks, F17 (NA:A).
- 27. Para Aleks con FTMO: la «maximum capital allocation rule» y el asterisco de «USD/LOT*» (hoja de ruta, A.2); A-28 va con A.
## Known Ambiguities
Las ABIERTAS, exactamente (`tests/unit/test_kit.py`); de donde salen: `docs/state/README.md`.

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-28 | el reloj del servidor de FTMO y su regla de horario de verano | medicion | no | F17 |
| A-32 | el nivel que al romperse con mecha invalida la entrada | pregunta | no | F19, F20 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-44 | magnitud y corte del tope de pérdida propio del trader (perdida_dia, perdida_semana) | pregunta | si | F11, F18 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-49 | si la caja se traza con la vela del bloque cerrada o en formación | pregunta | no | F20, F21 |
| A-50 | para descartar una zona frente al nivel tomado, si cuenta solo el 0 de la caja o la caja entera | pregunta | no | F19, F20 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |
| A-56 | la regla del objetivo dicha por el trader frente a lo que mide su material | medicion | no | F26 |
| A-57 | qué hace el trader cuando el lote de su riesgo no cabe en el margen o en el volumen máximo de la cuenta | pregunta | no | F24 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.
- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2557; el arnés sí, :2437): con `--todos` arrastra la cuenta (VISOR-CONSTRUCCION.md §4.3).
- VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del mes anterior (VISOR-CONSTRUCCION.md §4.3).
- El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; VISOR-CONSTRUCCION.md §4.3).
- `test_visor.py` hace leer al visor el M1 de marzo (calienta abril) en cada make check (HOLDOUT-EXPOSICIONES, 2026-10-18; VISOR-CONSTRUCCION.md §4.3).
- `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker (VISOR-CONSTRUCCION.md §4.3).
- El bróker simulado cotiza con el respaldo M1 la orden del primer cierre de la ventana: los ticks empiezan en ventana_inicio y la orden lleva 1 ms antes (VISOR-CONSTRUCCION.md §4.3).
- `arnes.dias_de_mercado` lee para calentar el M1 entero de marzo y de junio (días reservados) en cada corrida del arnés y cada make check, sin declararlo; declarado en HOLDOUT-EXPOSICIONES (2026-10-14); la línea LECTURA: va a G.2 (CORRIDA-CONSTRUCCION.md §1.c).
- El docstring de `engine/freno.py:7-8` dice que el adaptador real de MetaTrader usará la misma clase; ADR-0082 lo enmienda (el EA la porta). Lo paga R6a.4 (PLATAFORMA-ADELANTADA.md).

- La ingesta asigna la sesión con el reloj del registro y no con el congelado del artefacto; hoy son el mismo. Antes de cambiar reloj_sesiones en el registro, la ingesta pasa a leer el congelado (CASES-REJILLA.md).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- La condición 2 de ADR-0042 §2 (la lectura COMPLETA del libro, declarada) se comprueba buscando el NOMBRE del fichero en HOLDOUT-EXPOSICIONES (`cases/visto.py:requisitos`): una fila que lo nombra sin declarar la lectura completa la da por cumplida (falso positivo medido con enero, ENTRADA-ENERO.md §0.b). El mecanismo por nombre lo fija ADR-0042 §2: arreglarlo pide una NOTA o un ADR nuevo, no solo código.
- `engine/simulador_config.py` busca el spread supuesto de `llenado.yaml` por la hora de PARED de Europe/Madrid, no por la rejilla: los días de desfase sale corrido una hora (2026-10-27: 4 de 11 horas, 1 punto de spread distinto; ENTRADA-ENERO.md §0.c). Importará cuando se mida un mes con días de desfase: marzo, del 9 al 27, y octubre.
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO (2026-09-21, rama de abril). Sigue viva solo la parte de la serie: el reloj quedó corregido el 2026-10-06 (ADR-0069: Europe/Madrid).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- F26 lee la diferencia 3,00/3,75 entre la regla y el material como conocida y la mide en A-56 (ADR-0073, ADR-0040).
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
- Proteccion de rama en GitHub activada el 2026-09-04 (sin force-push ni borrado de `main`); no exige
  checks previos porque el ritual hace merge local y push. Revisar si se anade `required_status_checks`
  cuando el merge pase por PR.

## Reglas vivas
Las que solo viven aqui (`docs/state/README.md`).

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).
- data/manifests/, knowledge/corpus/transcripciones/ y knowledge/corpus/fotogramas/ → INMUTABLES tras commit (hook + historial de git; ADR-0005, ADR-0007 y ADR-0008). Corrección = manifiesto nuevo con `reemplaza_a`; exactamente una extracción de fotogramas activa por vídeo.

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).
- Ficheros de texto siempre con LF y UTF-8 (escribir con `newline="\n"`); toda salida de git se
  decodifica como UTF-8 con `core.quotepath=false` (la consola Windows es cp1252).

### Decisions and Rationale
Formato obligatorio por decision (ver docs/adr/0000-template.md). Decisiones de proceso vigentes:
- 2026-09-04 · Tres particiones reservadas (holdout-1/2/3) y pre-registro de umbrales antes de F26. Problema: holdout unico se quema al abrirlo; umbral ajustable a posteriori. Alternativas: holdout unico (descartada), validacion cruzada temporal (insuficiente con pocos casos). Estado: ACTIVE.
- 2026-09-04 · La garantia de inmutabilidad/solo-anadir es un test en CI contra el historial de git; los hooks son comodidad. Estado: ACTIVE.
- 2026-09-04 · Sin inferencias en evidence/; todo lo importado de Bot v2 se re-cita o entra como UNKNOWN. Estado: ACTIVE.

### Known Issues
- El trailer `Fuente:` se exige por commit, no por linea: un commit que mezcle esquema y valor
  cita ambas fuentes.
- El hash de 8 hex en los ids de evidencia/feedback (32 bits) se considera suficiente para
  cientos de items; desde F07 `escribir_item` distingue "mismo contenido" (idempotente) de una
  colision real (error). 353 items sin colision.

## Completed Features
Las cerradas desde el ultimo archivo; el cierre no anade nada (`docs/state/README.md`).
— ninguna desde el Archivo 38 (2026-10-18).

## Change Log
Las entradas desde el ultimo archivo; el cierre no anade ninguna (`docs/state/README.md`).
— ninguna desde el Archivo 38 (2026-10-18).
