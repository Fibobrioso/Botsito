# PROJECT STATE

> Lo que es verdad HOY. Que va aqui, que va a `docs/state/HISTORIA.md` y como se archiva:
> `docs/state/README.md`.

## Current Branch
trabajo/laminas

## Current Feature
trabajo/laminas, EN CURSO: F (1), las láminas del bot (R4.5) y la enmienda de RUMBO §0, §4 y §5. Encargo docs/encargos/trabajo-laminas.md; informe docs/validation/LAMINAS.md.

## Stable Main State
76bbe09 · merge de `trabajo/trazas-ablacion` (tag `stable/F38v-trazas-ablacion`), sobre `stable/F38u-video-julio` (129ea33). Informe docs/validation/TRAZAS-ABLACION.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
76bbe09 · merge: trabajo/trazas-ablacion, motor decisiones (bitácora y ablación por regla) y las clases de 04-13, 07-02, 07-03 y 07-14 · tag stable/F38v-trazas-ablacion

## Tests Currently Passing
1976 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-10-08). El orden lo decide el consultor en cada encargo; cada entrada dice de qué depende.

D. Endurecer la guardia por formas raras de bash, git, awk, sed y PowerShell que ninguna sesión usa (lista en GUION-MISMO-COMANDO.md §1.26). Rama propia, sin prisa: la barrera real sigue siendo el código.


F. Sesión 6 ACTIVADA en spec (F38n) y motor (F38o); S-22 y S-19 a la sesión 7. La re-corrida que cuenta está hecha (RECORRIDA-CONSTRUCCION-2.md: «no», cobertura 15.7 % y precisión 13.9 %; línea base anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt). Las trazas del motor y la ablación por regla están hechas (TRAZAS-ABLACION.md; `motor decisiones`; clases en su PARADA final). El rumbo: docs/plan/RUMBO-2026-11.md (R0.3) con las correcciones del consultor del 2026-11-09 recogidas en R4.3, R4.5 y R6.0 de la hoja de ruta. Siguiente, en este orden: (1) las láminas del bot (R4.5), con la enmienda de RUMBO §0, §4 y §5 en un commit propio; (2) J, si la hoja sale de kit hoja; (3) la preparación de la sesión 7, partida en 7a y 7b (R4.3): el ADR del método (RUMBO §1), el pre-registro de los puntos de pivote (esquema de tres salidas sobre julio que aceptó Aleks el 2026-11-09; los números los propone el consultor con la línea base), los ítems de evidencia de F7 #1, #2, #3, #6 y #10 y lo que el trader ya dijo del rango de H4. El vídeo de mapeo, si llega, SIN ABRIR y fuera del repo, y entra antes de elegir los días. C, R5.7 y R6a en los huecos.



C. La voz que el ASR se salta (v12 a v14), prioridad baja, en los huecos: exponer en corpus transcribe la configuración del VAD (o su desactivación), con tests; retranscribir v12, v13 y v14 con --reemplaza-a; volver a medir en los huecos lo de F2, F3, F4 y F6 de VIDEO-JULIO.md y, con eso, volver a decidir F5 (material_sin_video de julio). No va antes de las trazas, de las láminas ni de la preparación de la sesión 7.

G. PREREGISTRO.md está SIN RELLENAR: no se abre ningún holdout y F26 no empieza. Antes, el consultor fija cuántos días reservados necesita F26 (y si hay que pedir otro mes al trader), con las condiciones previas que hoy viven en Technical Debt (una pregunta abre N particiones, los dos días sin partición, F26 y A-56, la regla del objetivo frente al material, ADR-0073) y A-16 (medida en R3.7, sigue ABIERTA). G rellena PREREGISTRO.md con lo de ADR-0092 §13 (borrador de la NOTA en METODO-FIDELIDAD-RENTABILIDAD.md, PARADA 2), y en el mismo commit cambia test_puerta_holdout, que ata ese fichero a HEAD (_commiteado_y_sin_cambios); y MASTER_PLAN §H (y la fila de F30) con la rentabilidad. Holdout-3 tiene un día medido menos desde el 2026-10-14 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta. fidelidad-1 tiene 3 días medidos menos desde el 2026-10-17 (ADR-0041, retirados.yaml), y F26 lo tiene en cuenta al fijar cuántos días hacen falta. Y, para elegir los libros que miden (S-14, sesión 5): en sus backtests sin vídeo el trader se saltaba las sesiones que iban a acabar en break even; qué libro viene de vídeo, ACTIVAR-SESION-05.md §0.b.7.

I. Backtest de DICIEMBRE de 2025, recibido el 2026-10-09 (xlsx y capturas de estadística, SIN vídeo), SIN ABRIR y fuera del repo; las capturas son de Analytics y no se abren nunca. Entra por su propia rama después de renovar hacia atrás el calendario de cierres (RENOVAR-CIERRES.md, condición 1); julio ya entró (ADR-0078). Antes, el consultor decide si es construcción o reservado, teniendo en cuenta que no trae vídeo. En v10 el trader ya comentó operaciones de diciembre (HOLDOUT-EXPOSICIONES, 2026-10-04). En la sesión 6 el trader dijo que aún no lo ha grabado con su voz (declaración de Aleks, SESION-06-EXTRACCION.md §3.5).

J. kit hoja falla en main para todo paquete nuevo: busca una pregunta nacida de A-9 que el cuestionario de hoy ya no trae (CASES-REJILLA.md). Rama propia antes de la próxima sesión con el trader que use la hoja.

A. Opcional, para Aleks: el calendario de las noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en corpus/noticias/ como CSV fecha_utc,hora_utc,divisa,evento; stops_cortos.py --noticias <csv> --ventana-min 2 da la medida (MARGEN-LOTE.md §2.b). El panel del límite diario quedó declarado el 2026-11-07 (HISTORIA, Next Action HECHA · A).

Q. El trader da por bueno el backtest de agosto grabado en vídeo (S-16, sesión 4; ADR-0073 §5); Aleks le pide su exportación; hasta que llegue, los casos dev de agosto siguen saliendo del xlsx; al llegar, entra por su propia rama (libros.yaml solo se amplía) y ADR-0040/A-56 se revisan. Julio ya entró por su xlsx (ADR-0078); su exportación cubre solo del 1 al 17. En la sesión 6 no afirmó que la exportación esté en el Drive (§3.5); Aleks se la vuelve a pedir.

L. **Pendiente del consultor: la revision de `ev-v7-001550-82e5cffc`** (el item nuevo de la D). caja_bloque ya no cuelga de ese ítem (sesión 6).

M. **Pendiente de la demo de FTMO: el break even de una venta que salta por el ASK** (ADR-0065 §6).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026 y se renueva por condición, no cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres; docs/runbooks/RENOVAR-CIERRES.md). La condición 2 la cumple la lectura de SymbolInfoSessionTrade de R6a.1 (EA-CONEXION.md §11, el journal de la demo del 2026-10-21 en anexos/EA-CONEXION/demo-20261021-cierre/), y R6a.5 la usa (ADR-0082 D6).

### Pendientes heredados (sin verificar)

Del Next Action viejo, sin evidencia de estar hechos; texto entero: `docs/state/HISTORIA.md`;
criterio de salida: `docs/state/README.md`.

- 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego limpio confirmado por el trader. Bajar sus velas es…
- 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de `stable/F14-cobertura` saca junio del universo de un…
- 8. EL BRIEF PARA ABRIR LOS 4 `dev` DE SEPTIEMBRE, que es lo unico que se puede abrir de ese material y no se…
- 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una deuda abstracta: RE-DESCARGAR UN MES ROMPE `kit build`…
- 10. De la demo de FTMO queda el grabador de spread y ticks, F17.
- 27. Para Aleks con FTMO: la «maximum capital allocation rule» y el asterisco de «USD/LOT*» (hoja de ruta, A.2); la medida de ADR-0090 §3 casa con leer «commission: 5» como ida y vuelta.
## Known Ambiguities
Las ABIERTAS, exactamente (`tests/unit/test_kit.py`); de donde salen: `docs/state/README.md`.

| Id | Ambiguedad | Clase | Bloqueante | Resuelve en |
|---|---|---|---|---|
| A-13 | break even al toque o con cuerpo | pregunta | no | F11, F23, F26 |
| A-16 | cuanto se separan las velas de Oanda de las de Dukascopy | medicion | no | F26 |
| A-35 | cuándo un pivote de M15 está formado | pregunta | si | F19, F20 |
| A-43 | si una liquidez de M15 tomada antes de las 7 cuenta para operar después | pregunta | no | F19, F20 |
| A-48 | qué velas forman el bloque de la caja | pregunta | no | F20, F21 |
| A-53 | la orden sin llenar cuando el precio toma otra liquidez de M15 | pregunta | no | F20, F22 |
| A-54 | qué cuenta FTMO como petición al servidor y con qué margen frena el bot | medicion | no | F33 |
| A-55 | qué hace FTMO con las órdenes pendientes antes de un cierre largo, y qué mercado cuenta | medicion | no | F33 |
| A-56 | la regla del objetivo dicha por el trader frente a lo que mide su material | medicion | no | F26 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49 (A-49 RESUELTA por la sesión 6); C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.
- Hoy un mes no puede salir de `knowledge/cases/meses_reservados.yaml` (holdout.py lo niega sin excepción) … (CUARENTENA-POR-CONDICION-2.md, respuesta del consultor a la PARADA de la fase 0, punto 2; entera en HISTORIA, Technical Debt ACORTADA)
- El validador del journal v1 vive en `botsito.mql5bridge`, que `engine` no puede importar (import-linter): cuando F23 lo necesite, el esquema baja a una capa que `engine` vea, en su rama y tocando pyproject.toml (EA-CONEXION.md, respuesta a la PARADA, punto 4).
- El bróker simulado reserva margen por cada pendiente stop viva y comprueba el margen al colocarla (ADR-0081 §4) … (DEMO-EJECUCIONES-2-3.md §0.f; entera en HISTORIA, Technical Debt ACORTADA)
- Los docstrings de `scripts/viabilidad_trader.py:11` («5 USD por lote en cada lado») y `scripts/viabilidad_comision.py:46` («10 (perfil)») … (DEMO-EJECUCIONES-2-3.md §3.1; entera en HISTORIA, Technical Debt ACORTADA)
- La comprobación del LF final en `UltimaLinea` (`mql5/Include/Botsito/Capa/Journal.mqh`) es redundante con la del formato: ninguna prueba la caza sola (EA-CONEXION.md §6, rotura r3).
- Que el EA reinicie sus globales tras un cambio de símbolo (el defecto de la demo del 2026-10-20) … (EA-CONEXION.md §10; entera en HISTORIA, Technical Debt ACORTADA)
- La guardia no mira las herramientas que leen un fichero local fuera de Read/Grep/Glob/Bash/PowerShell/Monitor … (GUARDIA-G1.md §1.j; entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de `trabajo/guardia-g1` (§4.3) … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de C (§5): una ruta compuesta a través de una función propia, de un dato leído o de un nombre asignado más de una vez no se calcula … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de B (§5): solo Python; `node`, `perl` y demás siguen sin resolver lo que cargan, y un `getattr(os, ...)` no se ve … (entera en HISTORIA, Technical Debt ACORTADA)
- Los guiones de la plataforma (`contrato_rama.py`, `sello_make_check.py`, `instalar_hooks.py`, `pico_memoria.py`, `huso_por_velas.py`) … (GUARDIA-G1.md §6.4; entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de la excepción de la carga por ruta (revisor, A2; GUARDIA-G1.md §6.2) … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de ADR-0088 (revisor, B7) … (entera en HISTORIA, Technical Debt ACORTADA)
- ADR 0087 (S-15, no existe) sigue en los `ids-inexistentes` del encargo y del informe de trabajo/activar-sesion-05-motor; lo saca la rama que lo cree.
- RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden stop lleva `por = primer_esquema` (zonas.py); nada produce ese `por`, y la acción `reentrar` no está escrita (PUNTO-USADO.md §1.h).
- La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta, y A-31 está RESUELTA desde el 2026-09-29 (PUNTO-USADO.md §1.h).
- Una zona del productor reutilizada en un escenario nuevo (misma caja del mismo punto tras una toma nueva) … (PUNTO-USADO.md §1.c y §4.f; entera en HISTORIA, Technical Debt ACORTADA)
- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2558; el arnés sí, :2438): con `--todos --simular` corre una cuenta por mes como el arnés (ADR-0092 §8), nunca la diaria (VISOR-CONSTRUCCION.md §4.3).
- `curva_con_deslizamiento` y `veredicto_con_f17` (criterio_fidelidad.py) toman una sola curva y arrastran `previo` entre cuentas: cuando F17 los use, por cuenta (CUENTA-POR-MES.md, fase 0 e) 8).
- make check, en una rama trabajo/*, no sella si HOLDOUT-EXPOSICIONES.md no tiene una fila con la fecha del día (cada make check lee el M1 de marzo, RESPALDO-M1.md): guardia pendiente, propuesta en trabajo/cuenta-por-mes (CUENTA-POR-MES.md).
- VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del mes anterior (VISOR-CONSTRUCCION.md §4.3).
- El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; VISOR-CONSTRUCCION.md §4.3).
- `test_visor.py` y `test_preparar_a35.py` hacen leer el M1 de marzo (calienta abril) en cada make check (HOLDOUT-EXPOSICIONES, 2026-10-18 y 2026-10-26; VISOR-CONSTRUCCION.md §4.3).
- `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker (VISOR-CONSTRUCCION.md §4.3).
- `arnes.dias_de_mercado` lee para calentar el M1 entero de marzo y de junio (días reservados) en cada corrida del arnés y cada make check, sin declararlo; declarado en HOLDOUT-EXPOSICIONES (2026-10-14); la línea LECTURA: va a G.2 (CORRIDA-CONSTRUCCION.md §1.c).
- El docstring de `engine/freno.py:7-8` dice que el adaptador real de MetaTrader usará la misma clase; ADR-0082 lo enmienda (el EA la porta). Lo paga R6a.4 (PLATAFORMA-ADELANTADA.md).
- La guardia no niega leer con Read las crudas de data/transcripciones/ de un vídeo sin cuarentena ni tramos (VIDEO-JULIO.md §10.8).
- La forma de medida de ffmpeg de la guardia no admite -ss/-t sobre un tramo de un vídeo del corpus: falso positivo de la lista cerrada de GUARDIA-FFMPEG (VIDEO-JULIO.md, respuesta a las PARADAS 2 y 3).
- test_hoja_de_ruta no distingue un registro «HECHA · T» de una letra reutilizada del de la T vigente: letras_hechas es un conjunto (VIDEO-JULIO.md §10.1).
- Un fotograma dentro de un tramo no citable se puede abrir: la guardia niega corpus frames show en el tramo, pero no el Read del PNG por su ruta, y la CLI imprime la ruta (VIDEO-JULIO.md §11.1).

- La ingesta asigna la sesión con el reloj del registro y no con el congelado del artefacto; hoy son el mismo. Antes de cambiar reloj_sesiones en el registro, la ingesta pasa a leer el congelado (CASES-REJILLA.md).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- La condición 2 de ADR-0042 §2 (la lectura COMPLETA del libro, declarada) … (falso positivo medido con enero, ENTRADA-ENERO.md §0.b; entera en HISTORIA, Technical Debt ACORTADA)
- `engine/simulador_config.py` busca el spread supuesto de `llenado.yaml` por la hora de PARED de Europe/Madrid, no por la rejilla … (ENTRADA-ENERO.md §0.c; entera en HISTORIA, Technical Debt ACORTADA)
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- `cherry-pick` Y `rebase` NO PASAN POR LA PUERTA DEL COMMIT (2026-09-25, medido con git 2.55 en docs/validation/BLINDAJE.md §2):
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY (2026-09-21, rama de abril; el reloj quedó corregido el 2026-10-06, ADR-0069).
- EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRUCTURA (2026-09-21, informe §R2).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21); y (S-14, sesión 5) … (ACTIVAR-SESION-05.md §0.b.7; entera en HISTORIA, Technical Debt ACORTADA)
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- F26 lee la diferencia 3,00/3,75 entre la regla y el material como conocida y la mide en A-56 (ADR-0073, ADR-0040).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA PARTICION, y F26 tiene que saberlo (2026-09-20, medido en la rama del universo congelado; ADR-0035 §Impacto y docs/validation/UNIVERSO-CONGELADO.md §2b).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO … (entera en HISTORIA, Technical Debt ACORTADA)
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta).
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Copia de seguridad de las crudas y los WAV … (entera en HISTORIA, Technical Debt ACORTADA)
- La skill ingerir-sesion no nombra el trailer Fuente: de tramos_no_citables.yaml y abrir-rama no nombra la línea de PLANTILLA del informe (SESION-06-EXTRACCION.md §7, puntos 1 y 3; segunda vez): rama corta de skills.
- Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza OSError la guardia compara la forma sin prefijos … (entera en HISTORIA, Technical Debt ACORTADA)
- Las cotizaciones sin tick del bróker no usan la misma vela. En el cierre de la M1 k, Mercado.cotizacion (precio_invalido y stops_level, ADR-0057 §4) … (RESPALDO-M1.md §0.a y §0.b; entera en HISTORIA, Technical Debt ACORTADA)
- El panel de FTMO quedó declarado el 2026-11-07 (medianoche de España; HISTORIA, Next Action HECHA · A) … (entera en HISTORIA, Technical Debt ACORTADA)
- La zona que RN-005 liga al escenario vigente en el mismo cierre de M1 en que RN-004 abre uno nuevo se queda en el escenario anterior, y su stop cuenta en los cartuchos de ese (2026-07-03 09:23 y 09:35, zona:46 y zona:51; TRAZAS-ABLACION.md F5): la deuda de la zona reutilizada de PUNTO-USADO.md §1.c y §4.f en su forma directa; no se toca sin la regla del trader.
- La comparación de `motor decisiones` mira cada operación por (día, sesión, lado, instante, entrada) y no su lote, su stop ni su objetivo: un cambio de lote solo se ve si mueve las no enviadas, los rechazos o las cuentas suspendidas (TRAZAS-ABLACION.md F4.3).
- El `toca_colocar_orden_limite` sintético de tests/unit/test_cableado.py guarda en una clausura que ya dio SÍ y solo coloca en la primera corrida del proceso; los tests que corren el día dos veces usan uno sin estado (TRAZAS-ABLACION.md F2).

## Reglas vivas
Las que solo vivian aqui y se quedan (`docs/state/README.md`). Change Regimes de los manifiestos, el LF y UTF-8, Decisions and Rationale y Known Issues: `docs/runbooks/DECISIONES-DE-PROCESO.md`, en sus secciones del mismo nombre.

### Change Regimes (must be respected), lo que CLAUDE.md no dice
- knowledge/cases/holdout/{1,2,3}/ → tres particiones reservadas; cada una se abre una sola vez. QUE CUENTA COMO ABRIRLA, quien lo autoriza y que se hace ante una exposicion: `knowledge/cases/holdout/README.md` (ADR-0021). No se lee desde ningun sitio salvo la puerta `botsito.cases.holdout`, que se niega sin `PREREGISTRO.md` relleno y sin autorizacion commiteada por particion; la guarda de `tests/conftest.py` vigila a cualquier llamante durante los tests, y `kit build` / `kit check` declaran las velas de dias reservados que leen, que no es abrir (ADR-0021, ADR-0033).

### Things That Must Not Be Changed
- Regimenes de cambio de knowledge/. · Pureza de domain/. · Parametros no se optimizan contra resultados.
- La rentabilidad pre-registrada de ADR-0092, medida una vez sobre meses que el bot no ha visto, precede a todo lo que decida operaciones en vivo (F29, F30 y lo de F31-F32 que dependa de ellos), y la fidelidad sigue siendo la herramienta de construcción; la capa de plataforma de ADR-0082, que nunca decide una operación, puede ir antes.
- La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-0026) no se cambian sin ADR: el tipo se elige EN LA COMPRA, Standard -> Swing no existe, y con Standard vuelve la restriccion de noticias entera (calendario, RN-028, `filtro_noticias`).

## Completed Features
Las cerradas desde el ultimo archivo; el cierre no anade nada (`docs/state/README.md`).
— ninguna desde el Archivo 65 (2026-11-10).

## Change Log
Las entradas desde el ultimo archivo; el cierre no anade ninguna (`docs/state/README.md`).
— ninguna desde el Archivo 65 (2026-11-10).
