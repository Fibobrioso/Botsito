# PROJECT STATE

> Lo que es verdad HOY. Que va aqui, que va a `docs/state/HISTORIA.md` y como se archiva:
> `docs/state/README.md`.

## Current Branch
main

## Current Feature
Ninguna abierta: trabajo/contraste-trader cerrada en main (stable/F39o-contraste-trader). Lo siguiente, en la Next Action (F).

## Stable Main State
96b250fd · merge de `trabajo/contraste-trader` (tag `stable/F39o-contraste-trader`), sobre `stable/F39n-diagnostico-premisa` (42fdb0b5). Informe docs/validation/CONTRASTE-TRADER.md; el registro del cierre, al final de HISTORIA.

## Last Stable Commit
96b250fd · merge trabajo/contraste-trader: el contraste con el trader de ADR-0099 §6 y la petición escrita de los meses del backtest con costes · tag stable/F39o-contraste-trader

## Tests Currently Passing
2149 funciones de test. Lo que cubre cada una lo dice el informe de la rama que la trajo; la lista acumulada hasta el 2026-10-01, en docs/state/HISTORIA.md (Archivo 1, «Tests Currently Passing»).

## Next Action

**AHORA** (2026-11-22). El orden lo decide el consultor en cada encargo; cada entrada dice de qué depende.

D. Endurecer la guardia por formas raras de bash, git, awk, sed y PowerShell que ninguna sesión usa (lista en GUION-MISMO-COMANDO.md §1.26). Rama propia, sin prisa: la barrera real sigue siendo el código.


F. La sesión 7, en dos días con el método de ADR-0093 (R4.3), ingerida y ACTIVADA: la 7a (F39e: ADR-0094, A-58 abierta; break even al cierre, A-13 abierta por el margen) y la 7b (F39k: la stop cuyo 0 queda del lado malo espera, ADR-0097, A-59 abierta); A-48 y A-58, a la sesión siguiente. La corrida (3) de ADR-0070 §3 dio «no» (cobertura 15.2 %, precisión 14.4 %; RECORRIDA-CONSTRUCCION-3.md). La línea base vigente es anexos/RECORRIDA-CONSTRUCCION-3/cuenta-por-mes.txt. El pivote de ADR-0093 §6, por su contingencia sobre la diaria (19 parejas de julio y 40 de más): «una sesión más». La meta de ADR-0098: salida C (el techo no gana), que manda sobre el pivote; lo que pide antes de seguir, en R4.7: hasta el ADR de Aleks que la resuelva no se graba ninguna sesión de fidelidad, y la siguiente (R4.6) se prepara. ADR-0099: se mide primero; el puente del techo, hecho (PUENTE-TECHO.md, lectura «solo_juntas»); F17 (ADR-0099 §5) y el backtest del trader con costes (ADR-0100, R4.10), pendientes; el diagnóstico de la premisa y el contraste con el trader, hechos. El vídeo de mapeo (recibido el 2026-11-18): SIN ABRIR y fuera del repo, no se ingiere; octubre y noviembre de 2026, reservados. La letra C y R6a, en los huecos.



C. La voz que el ASR se salta (v12 a v14), prioridad baja, en los huecos: exponer en corpus transcribe la configuración del VAD (o su desactivación), con tests; retranscribir v12, v13 y v14 con --reemplaza-a; volver a medir en los huecos lo de F2, F3, F4 y F6 de VIDEO-JULIO.md y, con eso, volver a decidir F5 (material_sin_video de julio).

G. PREREGISTRO.md relleno (ADR-0096, F39g): la rentabilidad de ADR-0092 fijada; F26, diagnóstico con la referencia de ADR-0043 y la regla de las 36 unidades efectivas, sobre febrero de 2026 grabado con vídeo y voz (holdout-1 cerrada mientras tanto); ninguna pregunta ni autorización. Falta, con dueño: Aleks pide febrero al trader (mensaje del consultor); la rama del comando de medida de F26, que abre una sola partición y añade la primera pregunta; la rama corta del arreglo de kappa_entre_sesiones, antes de cualquier autorización de kappa; el hash de la spec, en la rama de la medida de rentabilidad (ADR-0096 §5). fidelidad-1: 4 retirados y 6 medibles; holdout-3: 1 y 7.

I. Backtest de DICIEMBRE de 2025, recibido el 2026-10-09 (xlsx y capturas de estadística, SIN vídeo), SIN ABRIR y fuera del repo; las capturas son de Analytics y no se abren nunca. Entra por su propia rama después de renovar hacia atrás el calendario de cierres (RENOVAR-CIERRES.md, condición 1); julio ya entró (ADR-0078). Antes, el consultor decide si es construcción o reservado, teniendo en cuenta que no trae vídeo. En v10 el trader ya comentó operaciones de diciembre (HOLDOUT-EXPOSICIONES, 2026-10-04). En la sesión 6 el trader dijo que aún no lo ha grabado con su voz (declaración de Aleks, SESION-06-EXTRACCION.md §3.5). Pesa más desde la 7a: el sesgo de las sesiones de enero depende de diciembre (Technical Debt).

J. kit hoja falla en main para todo paquete nuevo: busca una pregunta nacida de A-9 que el cuestionario de hoy ya no trae (CASES-REJILLA.md). Rama propia antes de la próxima sesión que etiquete días (G.2).

A. Opcional, para Aleks: el calendario de las noticias restringidas de FTMO (FAQ «Can I trade news?») de los meses de construcción, en corpus/noticias/ como CSV fecha_utc,hora_utc,divisa,evento; stops_cortos.py --noticias <csv> --ventana-min 2 da la medida (MARGEN-LOTE.md §2.b). El panel del límite diario quedó declarado el 2026-11-07 (HISTORIA, Next Action HECHA · A).

Q. El trader da por bueno el backtest de agosto grabado en vídeo (S-16, sesión 4; ADR-0073 §5); Aleks le pide su exportación; hasta que llegue, los casos dev de agosto siguen saliendo del xlsx; al llegar, entra por su propia rama (libros.yaml solo se amplía) y ADR-0040/A-56 se revisan. Julio ya entró por su xlsx (ADR-0078); su exportación cubre solo del 1 al 17. En la sesión 6 no afirmó que la exportación esté en el Drive (§3.5); Aleks se la vuelve a pedir.

M. **El break even de una venta que salta por el ASK** (ADR-0065 §6): sin objeto mientras break_even_condicion sea cierre (ACTIVAR-SESION-07.md).

N. El calendario de cierres (knowledge/cuentas/cierres/) cubre hasta el 7-10-2026, ya pasado, y se renueva por condición, no cada semana (decisión del consultor del 2026-10-03, stable/F36s-renovar-cierres; docs/runbooks/RENOVAR-CIERRES.md). La condición 2 la cumple la lectura de SymbolInfoSessionTrade de R6a.1 (EA-CONEXION.md §11, el journal de la demo del 2026-10-21 en anexos/EA-CONEXION/demo-20261021-cierre/), y R6a.5 la usa (ADR-0082 D6).

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
| A-58 | qué alto y qué bajo forman el rango de H4 cuando una H4 lo rompe | pregunta | no | F18 |
| A-59 | qué haces con la orden cuando se forma la caja y el precio ya está más allá del 0 | pregunta | no | F20, F22 |

Candidatas a ambiguedad sin abrir (de «Open Questions», tal cual):
- Candidatas a ambiguedad de docs/validation/DISENO-ENTRADA-RUPTURA.md §2.8 (2026-09-28, ADR-0056), SIN ABRIR: C1 que hace con la orden pendiente cuando aparece una caja nueva (v7 n.o 2 redibujo la caja con la orden puesta); C2 y C3 abiertas como A-48 y A-49 (A-49 RESUELTA por la sesión 6); C4 el stop en dos tiempos y la orden sin stop de v8 n.o 1 (toca A-18 y A-11); C5 la caja frente a la toma de M15 (hay una caja anterior a la toma del productor; toca RN-004, RN-008 y A-29); C6 la orden 2 puntos mas alla del 0 en v7 n.o 3 (toca A-36); C7 cuanto vive una orden stop sin llenar.

## Technical Debt
Una linea por deuda ABIERTA; texto entero y criterio de salida: `docs/state/README.md`.
- Hoy un mes no puede salir de `knowledge/cases/meses_reservados.yaml` (holdout.py lo niega sin excepción) … (CUARENTENA-POR-CONDICION-2.md, respuesta del consultor a la PARADA de la fase 0, punto 2; entera en HISTORIA, Technical Debt ACORTADA)
- El validador del journal (v1 y v2) vive en `botsito.mql5bridge`, que `engine` no puede importar (import-linter): cuando F23 lo necesite, el esquema baja a una capa que `engine` vea, en su rama y tocando pyproject.toml (EA-CONEXION.md, respuesta a la PARADA, punto 4).
- La guardia niega a un guion nuevo dos falsos positivos, que lanza Aleks con «!» … (CAPA-GENERADA.md, «La guardia»; entera en HISTORIA, Technical Debt ACORTADA)
- El bróker simulado reserva margen por cada pendiente stop viva y comprueba el margen al colocarla (ADR-0081 §4) … (DEMO-EJECUCIONES-2-3.md §0.f; entera en HISTORIA, Technical Debt ACORTADA)
- Los docstrings de `scripts/viabilidad_trader.py:11` («5 USD por lote en cada lado») y `scripts/viabilidad_comision.py:45` («10 (perfil)») … (DEMO-EJECUCIONES-2-3.md §3.1; entera en HISTORIA, Technical Debt ACORTADA)
- La comprobación del LF final en `UltimaLinea` (`mql5/Include/Botsito/Capa/Journal.mqh`) es redundante con la del formato: ninguna prueba la caza sola (EA-CONEXION.md §6, rotura r3).
- Que el EA reinicie sus globales tras un cambio de símbolo (el defecto de la demo del 2026-10-20) … (EA-CONEXION.md §10; entera en HISTORIA, Technical Debt ACORTADA)
- La guardia no mira las herramientas que leen un fichero local fuera de Read/Grep/Glob/Bash/PowerShell/Monitor … (GUARDIA-G1.md §1.j; entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de `trabajo/guardia-g1` (§4.3) … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de C (§5): una ruta compuesta a través de una función propia, de un dato leído o de un nombre asignado más de una vez no se calcula … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de B (§5): solo Python; `node`, `perl` y demás siguen sin resolver lo que cargan … (entera en HISTORIA, Technical Debt ACORTADA)
- Los guiones de la plataforma (`contrato_rama.py`, `sello_make_check.py`, `instalar_hooks.py`, `pico_memoria.py`, `huso_por_velas.py`) … (GUARDIA-G1.md §6.4; entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de la excepción de la carga por ruta (revisor, A2; GUARDIA-G1.md §6.2) … (entera en HISTORIA, Technical Debt ACORTADA)
- Riesgo residual de ADR-0088 (revisor, B7) … (entera en HISTORIA, Technical Debt ACORTADA)
- ADR 0087 (S-15, no existe) sigue en los `ids-inexistentes` del encargo y del informe de trabajo/activar-sesion-05-motor; lo saca la rama que lo cree.
- RN-019 no dispara nunca en el motor: su forma pide `por: activacion_sin_ruptura` y la orden stop lleva `por = primer_esquema` (zonas.py); nada produce ese `por`, y la acción `reentrar` no está escrita (PUNTO-USADO.md §1.h). Dueño: va con la reentrada de ADR-0083 D1 (R4.6).
- La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice que A-31 lo pregunta, y A-31 está RESUELTA desde el 2026-09-29 (PUNTO-USADO.md §1.h).
- Una zona del productor reutilizada en un escenario nuevo (misma caja del mismo punto tras una toma nueva) … (PUNTO-USADO.md §1.c y §4.f; entera en HISTORIA, Technical Debt ACORTADA)
- El visor no conecta `--diagnostico-cuenta-diaria` (cli.py: la valida `_diagnostico_de`, :2250-2261; el arnés la aplica, :2438; `motor_visor`, :2479, no): la pone en el nombre y en el HTML y corre una cuenta por mes (ADR-0092 §8; VISOR-CONSTRUCCION.md §4.3; auditoría del 2026-11-21, C1). Dueño: rama corta del visor (conectarla o negarla).
- `curva_con_deslizamiento` y `veredicto_con_f17` (criterio_fidelidad.py) toman una sola curva y arrastran `previo` entre cuentas: cuando F17 los use, por cuenta (CUENTA-POR-MES.md, fase 0 e) 8).
- Sin guardia contra fechas de días ocultos en lo que añade una rama. En main hay 32 ids exactos de casos ocultos fuera de knowledge/cases, uno de ellos de F39a-F39g en tests/unit. Primero, una rama que los sustituya en tests sin abrirlos (los informes cerrados, por recuadro o declarados); después, la variante estrecha V2 (GUARDIAS-HOLDOUT.md §4.3 y §9).
- VISOR-DIAS.md no recoge las opciones de diagnóstico del visor ni que calienta con el M1 del mes anterior (VISOR-CONSTRUCCION.md §4.3).
- El visor no enseña las H4 que el sesgo salta por el color (ADR-0080 §10; VISOR-CONSTRUCCION.md §4.3).
- `test_visor.py` y `test_preparar_a35.py` hacen leer el M1 de marzo (calienta abril) en cada make check (HOLDOUT-EXPOSICIONES, 2026-10-18 y 2026-10-26; VISOR-CONSTRUCCION.md §4.3).
- `motor visor --hasta` no recorta las H4 de contexto, las listas ni el resumen del bróker (VISOR-CONSTRUCCION.md §4.3).
- `arnes.dias_de_mercado` lee para calentar el M1 entero de marzo y de junio (días reservados) en cada corrida del arnés y cada make check, sin declararlo; declarado en HOLDOUT-EXPOSICIONES (2026-10-14); la línea LECTURA: va a G.2 (CORRIDA-CONSTRUCCION.md §1.c).
- El docstring de `engine/freno.py:7-8` dice que el adaptador real de MetaTrader usará la misma clase; ADR-0082 lo enmienda (el EA la porta). Lo paga R6a.4 (PLATAFORMA-ADELANTADA.md).
- La guardia no niega leer con Read las crudas de data/transcripciones/ de un vídeo sin cuarentena ni tramos (VIDEO-JULIO.md §10.8).
- La forma de medida de ffmpeg de la guardia no admite -ss/-t sobre un tramo de un vídeo del corpus: falso positivo de la lista cerrada de GUARDIA-FFMPEG (VIDEO-JULIO.md, respuesta a las PARADAS 2 y 3).
- Un fotograma dentro de un tramo no citable se puede abrir: la guardia niega corpus frames show en el tramo, pero no el Read del PNG por su ruta, y la CLI imprime la ruta (VIDEO-JULIO.md §11.1).

- La ingesta asigna la sesión con el reloj del registro y no con el congelado del artefacto; hoy son el mismo. Antes de cambiar reloj_sesiones en el registro, la ingesta pasa a leer el congelado (CASES-REJILLA.md).
- Sin git callan, sin aviso, las comprobaciones que leen git fuera de validation/ y no pasan por Historial: las anclas de paquetes, fidelidad y dev-visto y la subida de spec_version (docs/validation/HISTORIAL-SIN-GIT.md §3 y §6.1).
- RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (FundedNext): las sostienen el reglamento de FTMO y ADR-0026/0031, y una regla no admite fuente documental (docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md §4.4).
- La condición 2 de ADR-0042 §2 (la lectura COMPLETA del libro, declarada) … (falso positivo medido con enero, ENTRADA-ENERO.md §0.b; entera en HISTORIA, Technical Debt ACORTADA)
- `engine/simulador_config.py` busca el spread supuesto de `llenado.yaml` por la hora de PARED de Europe/Madrid, no por la rejilla … (ENTRADA-ENERO.md §0.c; entera en HISTORIA, Technical Debt ACORTADA)
- LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09-25, ADR-0047).
- `scripts/v5_criterio.py` SOLO RECONOCE CAJAS DE VENTA (2026-09-23):
- NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME CERRADO NO CAMBIE (2026-09-22, `trabajo/guardia-ids-docs`).
- LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY (2026-09-21, rama de abril; el reloj quedó corregido el 2026-10-06, ADR-0069).
- LA GUARDIA DE `cobertura_material` EN `universo()` ES MAS ESTRICTA DE LO QUE ADR-0025 SOSTIENE (2026-09-21, y el defecto es de la rama del dia anterior).
- EL `no_trade` POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA EN LA RAMA DE MAYO (2026-09-21); y (S-14, sesión 5) … (ACTIVAR-SESION-05.md §0.b.7; entera en HISTORIA, Technical Debt ACORTADA)
- `fecha_grabacion` TIENE QUE SER UN EJE DE PRIMERA CLASE, Y EL DETECTOR DE CONTRADICCIONES TIENE QUE ORDENAR POR ELLA (2026-09-21, deuda con nombre puesta por el consultor).
- BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUEDAD, Y ESCRIBIR QUE SE BUSCO (2026-09-21, rama F14a).
- EL DIA QUE UN CAMINO GUARDE MATERIAL EN `knowledge/cases/<camino>/`, NECESITA LECTOR GUARDADO ANTES DE QUE ESE FICHERO SE COMMITEE (2026-09-21, rama de la puerta por pregunta; enmienda de ADR-0033, informe §5).
- `lectura_de_velas` SIGUE LEYENDO EL `config.yaml` DE HOY para el prefijo del kit (2026-09-21, rama de los cupos congelados, informe §7).
- UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, NO EL HUMANO … (entera en HISTORIA, Technical Debt ACORTADA) Dueños (ADR-0096 §4): el comando de medida de F26 nace abriendo una; kappa, rama corta.
- EL FALLBACK DE `leer_fichero` JUZGA UNA CARPETA DESCONOCIDA BAJO LA AUTORIZACION DE `holdout-1` (2026-09-21, rama de la puerta por pregunta). Dueño: la rama del comando de medida de F26.
- UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDICADOS DE `fuente: mercado` NO PASAN POR COMPROBACION DE ALCANZABILIDAD (2026-09-20, rama de la liquidez de M15, informe §4).
- UNA `pregunta` DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE DEL CORPUS SIN ENLAZAR SU ITEM, Y NINGUNA GUARDIA SE QUEJA (2026-09-20, rama de la liquidez de M15, informe §8).
- EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA APARICION (2026-09-20).
- EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS (2026-09-17, rama del breaker de M1, informe §5).
- LA VIA DE PROPUESTA NO ADMITE `supersede` (2026-09-17, rama del breaker de M1, informe §3).
- UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y SIN AVISO (2026-09-17, rama del breaker de M1, informe §2).
- Copia de seguridad de las crudas y los WAV … falta v18, v19, v20 y v21 (entera en HISTORIA, Technical Debt ACORTADA)
- A-35 sigue ABIERTA y bloqueante tras la 7b: su respuesta cayó en un tramo no citable (SESION-08-EXTRACCION.md §3.1); va al trader por WhatsApp con el esquema del PDF y entra por «Mensajes del trader».
- Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.md §5): si `os.path.realpath` lanza OSError la guardia compara la forma sin prefijos … (entera en HISTORIA, Technical Debt ACORTADA)
- Las cotizaciones sin tick del bróker no usan la misma vela. En el cierre de la M1 k, Mercado.cotizacion (precio_invalido y stops_level, ADR-0057 §4) … (RESPALDO-M1.md §0.a y §0.b; entera en HISTORIA, Technical Debt ACORTADA)
- La zona que RN-005 liga al escenario vigente en el mismo cierre de M1 en que RN-004 abre uno nuevo se queda en el escenario anterior, y su stop cuenta en los cartuchos de ese (2026-07-03 09:23 y 09:35, zona:46 y zona:51; TRAZAS-ABLACION.md F5): la deuda de la zona reutilizada de PUNTO-USADO.md §1.c y §4.f en su forma directa; no se toca sin la regla del trader.
- La comparación de `motor decisiones` mira cada operación por (día, sesión, lado, instante, entrada) y no su lote, su stop ni su objetivo: un cambio de lote solo se ve si mueve las no enviadas, los rechazos o las cuentas suspendidas (TRAZAS-ABLACION.md F4.3).
- El `toca_colocar_orden_limite` sintético de tests/unit/test_cableado.py guarda en una clausura que ya dio SÍ y solo coloca en la primera corrida del proceso; los tests que corren el día dos veces usan uno sin estado (TRAZAS-ABLACION.md F2).
- `motor laminas` no dice el esquema: con la orden en el punto, `zona_del_punto` crea toda zona con `por = primer_esquema` (zonas.py:414-416); la frase vuelve cuando el motor distinga los dos esquemas (LAMINAS.md, respuesta a la PARADA final, 1).
- Un texto que ADR-0093 deja viejo y que trabajo/preparacion-sesion-7 no podía tocar … (PREPARACION-SESION-7.md §0.2, H8; el de engine/decisiones.py lo corrigió trabajo/activar-sesion-08; entera en HISTORIA, Technical Debt ACORTADA)
- `motor laminas`: la CLI solo se prueba entera con las velas reales (LAMINAS.md, F4.3) … (entera en HISTORIA, Technical Debt ACORTADA)
- La guardia toma por ruta una barra dentro de una cadena que no es una ruta (una etiqueta de cierre HTML, « / » entre espacios) … (LAMINAS.md, «Aplicación de la respuesta a la PARADA final», al final; LAMINAS.md, respuesta tras revisar la v4, 6; entera en HISTORIA, Technical Debt ACORTADA)
- `feedback pending` lista como pendientes los CORRECT antiguos de una regla que ya cita otro (RN-003; ACTIVAR-SESION-07.md F1.1).
- El sesgo de 20 sesiones de enero con menos de 60 H4 cargadas depende del arranque (ACTIVAR-SESION-07.md F1.3).
- El texto del sesgo del visor no tiene test (revisor de trabajo/activar-sesion-07, b7).
- Los guiones de los anexos no pasan por lint en make check.
- test_guardia_falsos_positivos falla a veces por el nombre aleatorio de una carpeta temporal.
- b1: la lámina calla la segunda causa de tope si también se cumple (0 casos en la 7b; LAMINAS-7B.md F2).
- motor laminas da LaminaError si RN-004 abre escenario en el cierre en que RN-016 o RN-001 dispararon por los intentos (0 casos en la 7a y la 7b; LAMINAS-7B.md F2).
- La CI de Linux se cuelga a veces instalando ffmpeg (dos veces: trabajo/laminas y trabajo/laminas-sesion-7b): cachearlo o ponerle límite al paso.
- No existe el comando que mida F26 sobre una partición: la puerta protege solo `kit kappa --incluir-holdout`, y el arnés y la ingesta excluyen lo oculto. Dueño: la rama del comando de medida, que nace abriendo una sola partición (ADR-0096 §4).
- El libro de septiembre no está en libros.yaml: no se lee, ni por la puerta, sin su declaración (ADR-0039). Dueño: la rama que vaya a leer septiembre.
- El día quemado de holdout-2 no está en retirados.yaml (lo excluyen HOLDOUT-EXPOSICIONES, «Lo que esto obliga», 4, y PREREGISTRO.md) y casos_medidos lo cuenta. Dueño: la rama que dé uso a holdout-2 lo retira antes (ADR-0096 §2).
- tests/unit/test_kit.py:706-707 (docstring de _autorizar) dice que el PREREGISTRO del proyecto «sigue vacio a proposito»: viejo desde ADR-0096. Lo corrige la rama que toque test_kit.py.
- `motor laminas` no dibuja las esperas de ADR-0097 (ACTIVAR-SESION-08.md). Dueño: la rama que genere las láminas de la sesión siguiente.
- Tests que no miran el estado en los días sin ticks (`test_sello_respaldo`; ACTIVAR-SESION-08.md, F2). Dueño: la rama que vuelva a tocar el respaldo M1 o test_sello_respaldo.

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
— ninguna desde el Archivo 83 (2026-11-25).

## Change Log
Las entradas desde el ultimo archivo; el cierre no anade ninguna (`docs/state/README.md`).
— ninguna desde el Archivo 83 (2026-11-25).
