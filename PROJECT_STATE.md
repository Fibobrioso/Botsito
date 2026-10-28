# PROJECT STATE

> Lo que es verdad HOY. Que va aqui, que va a `docs/state/HISTORIA.md` y como se archiva:
> `docs/state/README.md`.

## Current Branch
main

## Current Feature
Ninguna rama abierta. trabajo/recorrida-construccion cerrada en main el 2026-10-27 (stable/F38g-recorrida-construccion): la corrida que cuenta por ADR-0070 §3 dio «no» (cobertura 3,5 %, precisión 13,2 %); se sigue construyendo (RECORRIDA-CONSTRUCCION.md).

## Stable Main State
faf5ce2 · merge de `trabajo/recorrida-construccion` (tag `stable/F38g-recorrida-construccion`): la corrida que cuenta por ADR-0070 §3 («no»), la línea base nueva, las dos listas para la sesión 6 y el error del respaldo M1 (Z). Sobre `stable/F38f-activar-sesion-05-motor` (d843dbc). Informe docs/validation/RECORRIDA-CONSTRUCCION.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
faf5ce2 · merge: trabajo/recorrida-construccion, la corrida que cuenta por ADR-0070 §3 (no), la linea base nueva, las dos listas para la sesion 6 y el error del respaldo M1 (Z) · tag stable/F38g-recorrida-construccion

## Tests Currently Passing
1730 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-10-08). El orden lo decide el consultor en cada encargo; cada entrada dice de qué depende.

B. La guardia lee el guion pero no lo que importa o ejecuta a su vez (import de un módulo local, runpy, exec, subprocess con otro guion), ni en un guion ni en el código en línea (GUION-MISMO-COMANDO.md §0.c). Rama propia: decidir qué módulos se resuelven y se leen, negando por defecto lo que no se pueda resolver.

C. La guardia no ve una ruta protegida compuesta por partes dentro de un guion (joinpath, os.path.join, el operador /, f-strings, concatenación): analizar_codigo solo mira literales enteros y niega lo compuesto solo si el código además recorre directorios (GUION-MISMO-COMANDO.md, hallazgo 5 del consultor). Rama propia: negar por defecto un guion que nombra un fragmento sensible y compone rutas, con un test que lo rompa a propósito.

D. Endurecer la guardia por formas raras de bash, git, awk, sed y PowerShell que ninguna sesión usa (lista en GUION-MISMO-COMANDO.md §1.26). Rama propia, sin prisa: la barrera real sigue siendo el código.


F. La rama corta de la cuarentena por condición (Technical Debt, PRIORITARIA) antes de ingerir la sesión 6; la preparación de la sesión 6 (R4.2); R6a en los huecos.



T. Transcribir v11 a v14 (backtest de julio en vídeo, 2 h 38 min, con audio), comprobar qué días cubre cada uno, compararlos con el xlsx en los días 1 a 17 y con las horas del libro (el primero en Europe/Madrid); en su rama (ENTRADA-JULIO.md §5).

U. Julio 20-31: solo en vídeo (v14); decidir si se extraen casos del vídeo, tras transcribir v11-v14. Depende de T.

G. PREREGISTRO.md está SIN RELLENAR: no se abre ningún holdout y F26 no empieza. Antes, el consultor fija cuántos días reservados necesita F26 (y si hay que pedir otro mes al trader), con las condiciones previas que hoy viven en Technical Debt (una pregunta abre N particiones, los dos días sin partición, F26 y A-56, la regla del objetivo frente al material, ADR-0073) y A-16. Holdout-3 tiene un día medido menos desde el 2026-10-14 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta. fidelidad-1 tiene 3 días medidos menos desde el 2026-10-17 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta. Y, para elegir los libros que miden (S-14, sesión 5): en sus backtests sin vídeo el trader se saltaba las sesiones que iban a acabar en break even; qué libro viene de vídeo, ACTIVAR-SESION-05.md §0.b.7.

I. Backtest de DICIEMBRE de 2025, recibido el 2026-10-09 (xlsx y capturas de estadística, SIN vídeo), SIN ABRIR y fuera del repo; las capturas son de Analytics y no se abren nunca. Entra por su propia rama después de renovar hacia atrás el calendario de cierres (RENOVAR-CIERRES.md, condición 1); julio ya entró (ADR-0078). Antes, el consultor decide si es construcción o reservado, teniendo en cuenta que no trae vídeo. En v10 el trader ya comentó operaciones de diciembre (HOLDOUT-EXPOSICIONES, 2026-10-04).

J. kit hoja falla en main para todo paquete nuevo: busca una pregunta nacida de A-9 que el cuestionario de hoy ya no trae (CASES-REJILLA.md). Rama propia antes de la próxima sesión con el trader que use la hoja.

A. **Demo de FTMO: las ejecuciones 2 y 3 de MedirDemoFTMO** (Aleks; detalle en docs/runbooks/DEMO-FTMO.md): la 2 entre el 26 y el 30 de octubre, con el script 1.1 compilado antes; la 3 después del 1 de noviembre. Miden A-28, el nivel de ADR-0057 §2, deslizamientos, swaps y la comisión con 1,00 lote. La ejecución 2 comprueba la fórmula del margen con `MargenAlcanza` (FTMO-P-D1.md §3), y la 3 mide cuándo comprueba MT5 el margen de una pendiente stop (ADR-0081 §4). Y, opcional: Aleks, el calendario de las noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en `corpus/noticias/` como CSV `fecha_utc,hora_utc,divisa,evento`; `stops_cortos.py --noticias <csv> --ventana-min 2` da la medida (MARGEN-LOTE.md §2.b).

K. La guardia exigir_sin_crudo da un falso positivo con una asignación a una variable llamada crudo (scripts/leer_demo_ftmo.py; DEMO-EJECUCION-1.md). Rama propia, junto a B o C si cabe: que la guardia nombre la forma de la opción, con un test que rompa a propósito los dos sentidos. Y en la misma rama, el arreglo que queda de ENTRADA-JULIO.md §8: que reconozca como tests los de un clon `git worktree add --detach` de comparar-con-main (`C:/cm/`), con su test de los dos sentidos. Y las dos negativas de ACTIVAR-SESION-05-MOTOR.md §0.d (pytest desde C:/cm/, encadenadas).

Q. El trader da por bueno el backtest de agosto grabado en vídeo (S-16, sesión 4; ADR-0073 §5); Aleks le pide su exportación; hasta que llegue, los casos dev de agosto siguen saliendo del xlsx; al llegar, entra por su propia rama (libros.yaml solo se amplía) y ADR-0040/A-56 se revisan. Julio ya entró por su xlsx (ADR-0078); su exportación cubre solo del 1 al 17.

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y se renueva por condición, no cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres; docs/runbooks/RENOVAR-CIERRES.md). La condición 2 la cumple la lectura de SymbolInfoSessionTrade de R6a.1 (EA-CONEXION.md §11, el journal de la demo del 2026-10-21 en anexos/EA-CONEXION/demo-20261021-cierre/), y R6a.5 la usa (ADR-0082 D6).

Z. El bróker simulado llena con el respaldo M1 una orden en la vela cuyo cierre la colocó, en todo minuto sin ticks (el borde de la ventana y las horas perdidas), contra ADR-0051 §2 (RECORRIDA-CONSTRUCCION.md §2.8; antes, VISOR-CONSTRUCCION.md §4.3). Rama propia con su test que rompe en main, una NOTA en ADR-0051 §5 y las corridas repetidas; antes de la próxima corrida del arnés que cuente (ADR-0070 §3).

### Pendientes heredados (sin verificar)

Del Next Action viejo, sin evidencia de estar hechos; texto entero: `docs/state/HISTORIA.md`;
criterio de salida: `docs/state/README.md`.

- 2. Marzo: faltan vistos.yaml y el paso a (hoja de ruta, R5.3); la confirmacion escrita del trader llego el 2026-10-25 (A.3 HECHA; SESION-05-EXTRACCION.md §3.5).
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

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49; C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.
- PRIORITARIA. La cuarentena por condición deja pasar texto de un mes que puede acabar reservado: `meses_libres` cuenta diciembre como libre con NA:I sin decidir (`motivos_cuarentena('el [N] de diciembre')`: `[]` con meses libres, `['mes']` sin ellos), y la fecha numérica seguida de coma no se tapa (`'hoy 25 del 10'` da `['fecha numerica']`; `'hoy, 25 del 10,'`, `[]`). Carril de guardias y cuarentena (SESION-05-EXTRACCION.md §2.7 y §11, a4).
- La skill ingerir-sesion tiene que mandar el barrido ancho ANTES de leer cada filtrada: días 18 a 31 en dígitos y en letra, con el número enmascarado (`anexos/SESION-05/barrido_18_31.py` solo ve dígitos). Dueño: la próxima rama que toque `.claude/skills/ingerir-sesion` (SESION-05-EXTRACCION.md §2.7).
- El validador del journal v1 vive en `botsito.mql5bridge`, que `engine` no puede importar (import-linter): cuando F23 lo necesite, el esquema baja a una capa que `engine` vea, en su rama y tocando pyproject.toml (EA-CONEXION.md, respuesta a la PARADA, punto 4).
- El modo texto ANSI de MT5 (build 6230) escribe CRLF y el CSV de la ejecución 1 de MedirDemoFTMO tiene LF, sin explicación: la rama que congele los CSV de las ejecuciones 2 y 3 comprueba el CRLF del CSV 2 en `MQL5\Files` antes de copiarlo (EA-CONEXION.md §0.c).
- La comprobación del LF final en `UltimaLinea` (`mql5/Include/Botsito/Capa/Journal.mqh`) es redundante con la del formato: ninguna prueba la caza sola (EA-CONEXION.md §6, rotura r3).
- Que el EA reinicie sus globales tras un cambio de símbolo (el defecto de la demo del 2026-10-20) lo comprueban un test estático textual (`globales_sin_reiniciar`, `tests/contract/test_capa_mt5.py`) y la corrida de la demo: el script de pruebas no puede provocar un `REASON_CHARTCHANGE` (EA-CONEXION.md §10).
- La guardia de Claude Code no ve una consulta de CI en código cuando la mención se monta a trozos (`"g" + "h"`) junto a una vía de salida, ni cuando la vía de salida es un cliente de Python fuera de la lista cerrada del consultor (`aiohttp`); no ve como bucle una espera hecha a nivel de agente (`ScheduleWakeup`, `CronCreate`) con una consulta suelta en cada despertar; y no lee el código bajo `tests/` que se le pasa a pytest (`_analizar_pytest`): un test que esperase a la CI pasaría. Riesgos residuales declarados en trabajo/guardia-ci (GUARDIA-CI.md §5.2 y §9; los fijan `test_riesgo_residual_la_mencion_a_trozos_no_se_ve` y `test_riesgo_residual_un_cliente_fuera_de_la_lista_pasa`); el hueco de `tests/` es anterior a la rama. Para el carril de guardias.
- Artifact, ArtifactData, DesignSync y `file_upload`, `navigate`, `get_page_text` y `read_page` de claude-in-chrome leen un fichero local o una página `file://` fuera del matcher de la guardia: desde trabajo/guardia-ci están cerradas en `permissions.deny` de `.claude/settings.json` (GUARDIA-CI.md, PARADA 2). La regla fina, mirar sus rutas como un Read por si algún día hacen falta, va en su propia rama del carril de guardias, junto a K (el alias de la raíz).
- ADR 0087 (S-15, no existe) sigue en los `ids-inexistentes` del encargo y del informe de trabajo/activar-sesion-05-motor; lo saca la rama que lo cree.
- RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden stop lleva `por = primer_esquema` (zonas.py); nada produce ese `por`, y la acción `reentrar` no está escrita (PUNTO-USADO.md §1.h).
- La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta, y A-31 está RESUELTA desde el 2026-09-29 (PUNTO-USADO.md §1.h).
- Una zona del productor reutilizada en un escenario nuevo (misma caja del mismo punto tras una toma nueva) sigue ligada al escenario en que nació y sus cierres cuentan en los cartuchos de aquel (zonas.py, `zona_del_punto` liga solo al crearla); ADR-0083 lo hace alcanzable y la fase 4 no lo midió: hace falta la traza por cierre (PUNTO-USADO.md §1.c y §4.f).
- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2557; el arnés sí, :2437): con `--todos` arrastra la cuenta (VISOR-CONSTRUCCION.md §4.3).
- VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del mes anterior (VISOR-CONSTRUCCION.md §4.3).
- El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; VISOR-CONSTRUCCION.md §4.3).
- `test_visor.py` y `test_preparar_a35.py` hacen leer el M1 de marzo (calienta abril) en cada make check (HOLDOUT-EXPOSICIONES, 2026-10-18 y 2026-10-26; VISOR-CONSTRUCCION.md §4.3).
- `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker (VISOR-CONSTRUCCION.md §4.3).
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
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY (2026-09-21, rama de abril; el reloj quedó corregido el 2026-10-06, ADR-0069).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21); y (S-14, sesión 5) en los backtests sin vídeo faltan las sesiones que el trader se saltó por ir a break even: un día en que el bot opera y él no puede ser eso, no un no_trade (ACTIVAR-SESION-05.md §0.b.7).
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- F26 lee la diferencia 3,00/3,75 entre la regla y el material como conocida y la mide en A-56 (ADR-0073, ADR-0040).
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
- Copia de seguridad de las crudas y los WAV: hecha hasta v10 (2026-10-22, Drive privado de Aleks, con SHA256SUMS). Cada sesión nueva se añade tras su ingesta; los vídeos de las sesiones, recomendado, sin hacer.
- Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza OSError la guardia compara la forma sin prefijos; Grep y `rg` sobre una carpeta que contiene la raíz se deciden como sobre la raíz, suponiendo, sin medirlo, que respetan su `.gitignore`.
- La guardia no expande las llaves de bash que componen una ruta (`'<raíz>/'{a,b}`) ni mira las URL `file:///` (urllib, curl), que leen material protegido en `main` y en la rama (GUARDIA-ALIAS.md §9, b6 y b7): van con la deuda C de la Next Action (rutas compuestas).

## Reglas vivas
Las que solo vivian aqui y se quedan (`docs/state/README.md`). Change Regimes de los manifiestos, el LF y UTF-8, Decisions and Rationale y Known Issues: `docs/runbooks/DECISIONES-DE-PROCESO.md`, en sus secciones del mismo nombre.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La validación de fidelidad (F26) precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos); la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).

## Completed Features
Las cerradas desde el ultimo archivo; el cierre no anade nada (`docs/state/README.md`).
— ninguna desde el Archivo 49 (2026-10-27).

## Change Log
Las entradas desde el ultimo archivo; el cierre no anade ninguna (`docs/state/README.md`).
— ninguna desde el Archivo 49 (2026-10-27).
