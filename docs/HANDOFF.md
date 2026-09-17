# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-17, rama `trabajo/meses-vistos` esperando validacion; lo de debajo es anterior)
- LA GUARDA DEL HOLDOUT ESTA CERRADA EN MAIN (merge 44a9fc1, tag `stable/F13-guarda`).
- VALIDADA por el usuario el 2026-09-17: manda la fecha de la sesion porque la ceguera tiene que
  valer al ETIQUETAR; abril fechado el 2026-09-05. `mover_sesion` a una fecha posterior a un
  `visto_el` falla y restaura (test).
- MAYO 2026 ESTA DECLARADO VISTO en `knowledge/cases/kit/vistos.yaml`, con `visto_el: 2026-09-11`.
  Cada entrada lleva ya su `visto_el` (obligatorio) y cuenta para un paquete solo si es igual o
  anterior a la FECHA DE SU SESION -la del nombre, el dia en que el trader etiqueta-. La sesion 1
  (2026-09-09) se sigue reproduciendo igual; un paquete de una sesion del 09-11 o posterior no puede
  sortear mayo (`kit build` falla) y `knowledge validate` denuncia un paquete escrito que lo tenga.
  Lo que HANDOFF dice mas abajo de que mayo "no se puede declarar en `vistos.yaml`" ya no es cierto.
- LA SESION 2 ETIQUETA SOBRE EL PAQUETE DE LA SESION 1 (opcion (a) del brief, medida): solo sus 10
  `dev` de junio son ciegos. Tres condiciones antes de registrar una etiqueta:
  (1) confirmacion escrita del trader de que NO backtesteo junio -su CONFIRM del 09-09 decia que lo
  haria-; (2) material de la sesion sin los `dev` de mayo en el etiquetado ciego; (3) la guardia de
  ancestro solo mira `LABEL_CASE` con la MISMA sesion que el paquete, asi que etiquetas registradas
  como sesion 2 sobre casos de la sesion 1 quedarian fuera. Es un DEFECTO de la guardia, no una
  restriccion (usuario, 2026-09-17): el brief del paquete la corrige comprobando POR CASO -las
  particiones del paquete del caso, commiteadas antes de esa etiqueta- y no por sesion.
  (b) -paquete nuevo solo con junio- esta bloqueado: `config.yaml` es global y cambiar los cupos
  rompe `kit check` de la sesion 1.
- `kit kappa` avisa cuando una ronda tiene unidades sobre dias que el trader ya habia visto el dia de
  su sesion: "no fue etiquetado ciego". Es lo que F26 tiene que leer.
- Lecciones de la rama:
  - La fecha de un commit no es la de un paquete: `commit_que_anadio` sigue sin renombrados y da la
    del ultimo `mover_sesion`. Para fechar algo del kit, la fecha va en el nombre de la sesion.
  - Refechar una entrada de `vistos.yaml` ya usada por un paquete lo rompe en silencio sin `data/`:
    por eso la guardia de `knowledge validate` mira tambien las exclusiones, no solo los casos.
  - Congelar un dataset nuevo con el prefijo del kit ya rompe hoy la reproduccion de la sesion 1
    (medido por la revision de diseno). Resolverlo antes de construir el siguiente paquete.
  - Medir la linea base de `kit check` ANTES de tocar nada, y comparar la salida entera con `diff`:
    es la unica forma de decir "byte a byte" sin fiarse.

## Estado (2026-09-17, rama `trabajo/guarda-de-holdout` esperando validacion; lo de debajo es anterior)
- LA RAMA DE FIDELIDAD ESTA CERRADA EN MAIN (merge e4f761c, tag `stable/F13-fidelidad`, spec 12.0.0).
  Esta rama sale de ahi y no toca `knowledge/spec/`.
- LA GUARDA DEL HOLDOUT EXISTE (ADR-0033): hook de auditoria en `tests/guarda_holdout.py`, `autouse`
  en toda la suite, para CUALQUIER llamante -no solo `spec` y `domain`: restringida a esos dos no
  veia nada-. Salta con cualquier apertura de `knowledge/cases/holdout/{1,2,3}/**` salvo su README;
  copiar cuenta, listar no. Un test que la quiera provocar se marca `provoca_holdout` y reapunta la
  raiz a un holdout sintetico.
- LA PUERTA: todo lo que ABRE pasa por `botsito.cases.holdout.abrir()`, que se niega sin
  `PREREGISTRO.md` commiteado y sin la marca `SIN RELLENAR` y sin
  `docs/validation/AUTORIZACION-<particion>.md` commiteado, cuyo `preregistro_blob` tiene que ser
  el blob del PREREGISTRO commiteado: cambiar un umbral despues de autorizar cierra la puerta hasta
  una autorizacion nueva. Cubre los ficheros del holdout y el
  VALOR de las etiquetas de casos reservados: `kit kappa` las excluye y dice sobre cuantas unidades
  y casos calculo (`--incluir-holdout` pasa por la puerta) y `feedback trace` las oculta. Cargar registros NO es abrir: `knowledge validate` y la
  guardia de ancestro no pasan por ella.
- LAS VELAS NO PASAN POR LA PUERTA, y no pueden: que dias son reservados depende de cuales entran en
  el universo, y eso de sus velas. `kit build` y `kit check` SE PUEDEN ejecutar con `data/` presente
  -la obligacion 6 que lo prohibia esta reescrita- y declaran en su salida (`LECTURA:`) CUANTOS
  dias reservados leen por particion, sin fechas: esa salida puede acabar delante del trader. Eso desbloquea el paquete de la sesion 2.
- Lecciones de la rama:
  - EL RITUAL POR LINEAS `!` EN CLAUDE CODE: cada linea abre una shell nueva, asi que un `export
    BOTSITO_ALLOW_MAIN=1` no sobrevive a la linea siguiente. La variable va pegada al commit:
    `BOTSITO_ALLOW_MAIN=1 git commit -m "..."`. El merge, el tag y el push no la necesitan. Y un
    bloque de varias lineas con `!` delante de cada una falla: `!` solo va al principio del mensaje.
  - Una obligacion escrita a mano puede ser mas ancha que el problema: "no ejecutar el kit con datos"
    bloqueaba la sesion 2 para siempre. Antes de escribir una prohibicion, medir que impide.
  - Una guarda por RUTA no cubre lo que no vive en esa ruta: las etiquetas del holdout estan en
    `knowledge/feedback/` y en el xlsx. Y quien muestra un valor no es solo quien lo parsea:
    `feedback trace` imprimia la etiqueta de cualquier caso.
  - `sys.addaudithook` no se puede quitar; en Windows las copias de `shutil` no emiten `open`; y una
    guarda que hereda de `Exception` se la traga cualquier `except` del kit.
  - `os.path.normcase` baja a minusculas en Windows: compara TODO normalizado o `README.md` deja de
    casar.

## Estado (2026-09-16, rama `trabajo/fidelidad-de-la-spec` esperando validacion; lo de debajo es anterior)
- FTMO Y ARQUITECTURA ESTA CERRADA EN MAIN (merge 00ad174, tag `stable/F13-ftmo`). Esta rama sale de
  ahi y lleva la spec a 12.0.0 con un solo bump.
- RN-005 ESTABA AL REVES y ya no: prohibia abrir por debajo de la liquidez de M15 en sesgo alcista,
  que es donde el trader opera. El lado se nombra en el predicado (`lado_de_ruido`); `alcista` y
  `bajista` NO son tokens a proposito, o `sentido: alcista` volveria a pasar la guardia de argumentos.
- LA ORDEN SE COLOCA EN DOS REGLAS (ADR-0032): RN-011 prepara (lote, stop y `orden_dimensionada` con
  la zona) y RN-015 escribe el objetivo, coloca y apaga el hecho. Una sola regla dejaba a los gates
  sin ventana; tres dejaban el orden entre disparadores al azar. `colocar_orden_limite` lleva
  `efecto: abrir_operacion`: un gate la frena en el instante de ejecutarla y el resto de la regla
  sigue. RN-013 quedo DESCARTADA por absorbida (no por falsa).
- CUANDO NACE LA ORDEN NO ESTA CERRADO: A-29, con `orden_limite_nace` en DEFAULT. Con la otra
  lectura hay que reescribir RN-008. Lo de la pendiente a las 15:00 es A-30, y
  `retirar_orden_limite` esta declarada sin regla.
- HECHOS DEL BROKER: `operacion_abierta` y `orden_limite_pendiente` llevan `origen: broker`,
  `decision` y `lo_provoca`; fijarlos en una forma es un error. F14b §0 quedo deshecho y anotado.
- `equal` YA NO ES TOKEN. El resultado de un cierre es `ganancia | perdida | break_even` (break even
  por mecanismo, no por P/L neto) y como se activo va en `por`. Desde el 2026-09-17 el mecanismo
  distingue tambien `salto_el_stop`: el stop entero GASTA cartucho sea cual sea la activacion, y
  solo la salida en rojo SIN stop de una entrada activada sin ruptura (el equal del trader) no gasta
  y habilita RN-019. Que el stop entero gaste es lectura nuestra: A-31, sesion 2, junto a A-29, que
  el consultor marco como prioridad. NO SE PUEDE RENOMBRAR un parametro
  que nombra un registro de feedback: `knowledge validate` pasa todos los registros, tambien los
  supersedidos, contra el registro.
- LA FIRMA FRENA ANTES DEL LIMITE (ADR-0031): `firma_margen_seguridad` = 0,5, VALIDADO por el
  consultor el 2026-09-17 (un riesgo nominal de colchon, que crece con el drawdown); RN-029
  diario, RN-031 total con `detenido_por_tope_total: permanente`, RN-032 prospectiva, RN-030
  `terminal`. El tope del trader (RN-020) no cambia de lectura.
- Lecciones de la rama:
  - Un bump unico con varios commits: los commits de guardias que no cambian la spec van antes, y
    toda la spec, el manifiesto y los documentos generados en UN commit. `version_sin_subir` compara
    con HEAD, asi que un segundo commit de spec en 12.0.0 fallaria.
  - Una guardia que exige un campo nuevo en un fichero que el kit reconstruye en repos de prueba
    (`clase` en ambiguedades) va en `knowledge validate`, no en la construccion del paquete: los
    fixtures del kit no la llevan y catorce tests cayeron a la vez.
  - "Nunca un parametro en `reinicia_con`" parecia limpio y rompia cuatro de cinco acumuladores. Medir
    la guardia sobre la spec real ANTES de escribirla en el brief.
  - Una regla nueva que usa en su `cuando` la palabra "una" junto a zona u operacion salta la guardia
    de cifras en letra: "en la zona de control que la ancla", "la operacion en curso".
  - Otra vez los heredocs: dos scripts de Python con f-strings y comillas simples no llegaron a
    ejecutarse en Git Bash. Scripts largos, con Write al scratchpad.
  - Una exencion se escribe con los casos que el trader nombra, no con una clase que los contiene:
    "activada sin ruptura" contenia el equal que el eximio y el stop entero, que no eximio. Lo
    cazo el consultor al revisar, no una guardia.
  - `spec_version` fijo con la spec cambiada: `version_sin_subir` compara con HEAD, asi que da rojo
    hasta commitear y verde despues. Si hay que corregir la spec de una rama sin fusionar sin subir
    la version, se corrige, se regenera el manifiesto y se commitea antes de `make check`.
  - No ejecutar `kit check` ni `kit build` para probar el cuestionario: con `data/` presente leen
    velas de dias reservados. El test llama a `cuestionario.generar` con `_cargar_todo` y sin indice.

## Estado (2026-09-14, rama `trabajo/ftmo-y-arquitectura` esperando validacion; lo de debajo es anterior)
- LA FIRMA ES FTMO 2-Step SWING de 100.000 (ADR-0026). FundedNext no admite bots desde 50.000, ni en
  el reto ni en la fondeada. Todo lo que diga "FundedNext" en material anterior al 2026-09-14 habla
  de la firma descartada, incluida la demo 34891752: sus mediciones del instrumento corren como
  DEFAULT declarado bajo A-27 y las del reloj del servidor estan SIN VALOR bajo A-28. El tipo Swing
  se elige en la compra y no se cambia despues: no comprar sin confirmarlo en el panel.
- EL BOT SI OPERA NOTICIAS otra vez (enmienda de ADR-0022): `filtro_noticias = no`, RN-028
  DESCARTADA, A-17 DECIDIDA. Con Swing no hay ventana que respetar; con Standard volveria entera.
- EL DIA DE RIESGO ES CIVIL (ADR-0027): el reglamento corta a medianoche CE(S)T, que es
  `huso_operativa`. `reloj_dia_riesgo = civil_operativa`, A-19 DECIDIDA, y RN-020 ya no nombra el
  reloj del servidor. Quedan dos relojes: el civil y el del servidor (rejilla de velas).
- NACEN RN-029, el freno de la firma (5 % diario desde el saldo al corte, 10 % total estatico, los
  dos del capital inicial y sobre equity), y RN-030, que cierra a mercado SOLO con posicion viva
  ligada a OP (se partieron al validar: RN-029 cerraba con OP sin ligar y un `si` literal, y
  habria emitido un cierre por evento mientras el bot estaba parado). El mas restrictivo no es siempre el del trader: por
  encima de 111.111,11 de saldo al empezar el dia manda la firma.
- CUATRO ADR DE ARQUITECTURA que F18-F24 necesitan: ADR-0028 (riesgo por tick, estrategia al cierre
  de M1, ordenes por evento, punto fijo con refraccion, hechos del broker derivados), ADR-0029 (BID,
  redondeo al mas cercano con empate en contra del bot), ADR-0030 (arbol generico + primitivas a
  mano). OJO: ADR-0028 punto 5 NO esta aplicado a la spec -RN-010, RN-011 y RN-013 siguen fijando
  `operacion_abierta` y `orden_limite_pendiente`- y va en el brief siguiente.
- A-24, A-25 y A-26 estan RESERVADAS (F14b §3) y no existen; `test_kit` las lista en
  `IDS_RESERVADOS` y falla en cuanto se cree una, para obligar a retirarla de la lista.
- Lecciones de la rama:
  - Un brief puede pedir algo que el esquema no admite: "UNKNOWN con ambiguedad_id" no existe
    (solo DEFAULT_AMBIGUOUS lleva `ambiguedad_id`), y una regla vigente no puede nombrar un UNKNOWN.
    Se pregunto antes de escribir; el consultor partio la ambiguedad en dos (A-27 default, A-28
    sin valor) y dejo que `comprobar_forma` y `comprobar_consumo` decidieran si el reloj podia
    quedar sin valor.
  - Una regla DESCARTADA con `forma: {pendiente_definicion: A-N}` falla si A-N se cierra:
    `comprobar_forma` mira las descartadas tambien. Al descartar, se quita la forma.
  - Quien fija un freno tiene que leerlo (`test_los_hechos_declarados_coinciden...`), aunque otra
    regla ya lo lea: RN-029 lee `detenido_por_tope`.
  - Una accion que usa una ligadura (`de: OP`) necesita que el `cuando` la ATE en un `todos_de`:
    ninguna guardia lo comprueba -OP es tambien un token y pasa-, y en un `cualquiera_de` no tiene
    semantica. Lo cazo el consultor al validar, no una guardia; la guardia queda ACEPTADA para el
    brief siguiente, junto con decidir la clase de RN-030 (esta como `gate` y no prohibe nada).
  - F14b usa ids de regla PROVISIONALES (RN-030, RN-034) que ya no significan eso: RN-029 y
    RN-030 son el freno de la firma. Al aplicar F14b, numerar desde el primer id libre.
  - Otra vez el heredoc: `\b` dentro de un heredoc de Git Bash es BACKSPACE. Los regex, con Write.
  - `## Estado` de un ADR se lee con `split()[0]`: "ACTIVE." con punto falla. Texto, en otra linea.
  - `spec status` pone los parametros UNKNOWN sin REJECT bajo "falta preguntarlo", y los de A-28 no
    son preguntas sino mediciones: la etiqueta miente para ellos (informe de la rama).

## Estado (2026-09-12, fase 1 cerrada en main; F11 y F12 validadas y cerradas; F13 CERRADA, esperando validacion)
- `main`: merge de F11 `b62f4aa` con tag `stable/F11`; `docs(state)` `3597b3d`. La fase 1 (F03-F08)
  se cerro antes, en `5d8cf3c` con tag `stable/F08`. Protegida en GitHub.
- Cerradas y en main: F01-F09 (salvo las no iniciadas), F15, la auditoria global y los previos
  de F07. Ramas fusionadas borradas.
- F10 elicitation-kit CERRADA el 2026-09-08 (tag `stable/F10`). Lo que dejo: ADR-0011;
  `knowledge/spec/ambiguedades.yaml` (A-1..A-12 legibles por maquina); registro con 24
  parametros de estrategia en UNKNOWN; `knowledge/cases/kit/{config,mapa_parametros,vistos}.yaml`
  (cifras de negocio como datos; meses VISTOS por el trader: enero, ABRIL -v5 es el, backtesteandolo-, julio y agosto. MAYO tambien lo esta desde que lo backtesteo entero el 2026-09-11, pero no se puede declarar en `vistos.yaml` sin invalidar el paquete de la sesion 1: el hueco esta escrito en el propio fichero); paquete `cases`
  (cuestionario con casos `ev-*` -el recuento lo da el propio paquete, no esta linea-, ventanas de dias no vistos de mayo y junio de
  2026 con hash y limites H4 por anclaje, particiones por hash con seed, kappa desde los
  `LABEL_CASE`); CLI `kit build|check|kappa`; `knowledge validate` capa kit con guardia de
  ancestro (particiones commiteadas antes del primer `LABEL_CASE`); paquete real
  `knowledge/cases/kit/2026-09-09-sesion-01/` (nacio con la fecha provisional 2026-09-15 y se movio al celebrarse).
- SESION 1 CELEBRADA el 2026-09-09 y procesada entera (video v6, 2 h 27 min; 117 registros de
  feedback; A-1..A-12 RESUELTAS). Informe: `docs/validation/SESION-01-2026-09-09.md`, que es el
  ACTA: que se pregunto, que respondio y con que minuto de v6. El ESQUEMA de la estrategia ya NO
  vive ahi -se quedo viejo dos veces en dos dias, las dos en hechos de negocio-: se GENERA en
  `docs/spec/` desde `knowledge/spec/` y `make check` lo compara (F13). Cerrada en main con el tag
  `stable/F10-sesion-01`.
- CUIDADO al citar v6: dos tramos NO son especificacion y la guardia los rechaza
  (`knowledge/corpus/tramos_no_citables.yaml`): 0:41:00-0:50:11, donde ambos acuerdan en voz que lo
  que se explica "no va para la operativa", y 1:53:30-1:57:31, donde suena un video ajeno mientras
  el trader se ausenta.
- F11 strategy-spec-schema VALIDADA y cerrada en main el 2026-09-10 (tag `stable/F11`). Lo que dejo:
  - `botsito feedback apply --sesion <s> [--check]`: lleva los valores del feedback al registro.
    NO interpreta: si un valor no encaja en el tipo, falla y dice cual. La re-expresion se hace
    fuera, con un registro que supersede y lleva `valor_canonico` (campo opcional nuevo).
  - `botsito spec status`: con que corre el bot y que sigue en revision (cruza el registro con las
    ambiguedades ABIERTAS).
  - `botsito spec manifest [--escribir]`: hash de la spec sobre los TRES ficheros. Si el hash
    cambia y `spec_version` no, `knowledge validate` falla.
  - `knowledge/spec/`: el recuento vivo lo da `botsito spec status` y NO se copia aqui: esa copia
    se quedo vieja tres veces en dos dias (P8 y P11 de la auditoria). Un test lo vigila.
  - ADR-0012 a ADR-0017. La enmienda a ADR-0005 del 2026-09-09 queda REVOCADA por ADR-0017:
    `huso_operativa` vuelve a `Europe/Madrid`, que es lo que ADR-0005 decia. El trader opera
    siempre a SU hora, sea cual sea la fecha, asi que su reloj es civil y no un offset fijo.
    La rejilla H4 se ancla aparte, en `17:00 America/New_York` = 00:00 de servidor.
- F12 spec-semantic-validator VALIDADA y cerrada en `main` el 2026-09-12 (merge `77c7501`, tag
  `stable/F12`; encima va `stable/F12-holdout`). Aporto ADR-0018 (la precedencia va por CLASE),
  ADR-0019 (la forma ejecutable: predicados con argumentos, ligadura, y el vocabulario DENTRO de
  strategy_spec.yaml) y ADR-0020 (la base del lotaje); los parametros sin lector declaran
  `consumido_por`, existe `botsito spec check` y los `R-NN` son explicitos. **El recuento de
  reglas no se pega aqui**: lo dan `botsito spec status` y `docs/spec/reglas.md`, que se genera.
  Informe: `docs/validation/F12-spec-semantic-validator.md`.
- F13 spec-documents CERRADA y esperando validacion (rama `feature/F13-spec-documents`).
  `docs/spec/` se GENERA desde `knowledge/spec/` con `botsito spec docs` -cuatro documentos, uno
  por fichero fuente- y un test de contrato regenera y compara el TEXTO ENTERO; mueren dos copias
  vivas (el §2 del acta de la sesion 1 y el recuento del README de la spec). Cierra las cuatro
  deudas heredadas, y tres estaban mal enunciadas: lo que faltaba en las cadenas de `supersede` no
  era recorrerlas sino el TIEMPO, y `_ARGS_DE_VALOR` era una lista blanca AL REVES. Entran ademas
  ADR-0022 (el bot no opera noticias; nace el estado `DECIDIDA`) y ADR-0023 (`recibido_el` y
  `procedencia` en el feedback), la hoja del trader se muda a `src/botsito/cases/hoja_docx.py`
  (`botsito kit hoja`) y el vocabulario de la forma gana `tokens`. La auditoria de cierre (dos
  agentes) encontro SEIS formas de colar un valor de negocio en `forma` -incluida `tope: 9.5`- y
  que `feedback pending` daba por reflejado un `RESOLVE_CONTRADICTION` con la contradiccion
  todavia abierta. Y la mitad B del objetivo, que la auditoria vio sin entregar: `test_documentos_vivos.py` prohibe pegar un recuento en los documentos que describen el presente, con exenciones por seccion nombradas y una por linea con motivo (`<!-- cifra-congelada: ... -->`). Informe: `docs/validation/F13-spec-documents.md`.
- EL LOTAJE CAMBIO DE BASE el 2026-09-11 (ADR-0020) y es lo mas caro de este tramo: el 0,5 % de
  riesgo se mide EN el nivel 0,8 y no sobre la caja completa, asi que `lotaje_base` vale
  `hasta_stop_fraccion`, el lote es un 25 % mayor y el stop cuesta el riesgo entero. RN-012 dice
  ahora lo contrario de lo que decia. Si alguien lee material anterior al 2026-09-11 -incluidos
  los mensajes del trader sobre la rentabilidad de mayo- lo encontrara contado en CAJAS
  COMPLETAS, que es la convencion vieja: esta anotado en ADR-0020, con la pregunta pendiente de
  ratificar con el trader.
- BACKTEST DE MAYO 2026 recibido el 2026-09-11 (junio NO). Esta en el corpus, fuera de git, en
  `Material adicional de su operativa/Backtest mayo 2026/`. OJO: 13 de los 19 dias de mayo son
  holdout-1/2/3 segun `knowledge/cases/kit/2026-09-09-sesion-01/particiones.yaml`, asi que no
  puede usarse para elegir parametros; es entrada de F14 y F26.
- Lecciones tecnicas (F12), y la mas cara es la primera:
  - UNA GUARDIA NUEVA NO HEREDA NADA. El vocabulario de ADR-0019 (predicados, acciones, efectos,
    hechos, acumuladores) lleva `cita` y `literal` propios desde el dia uno, y durante toda la
    funcionalidad NADIE los comprobaba: se podia poner cualquier frase en boca del trader dentro
    de un predicado, o citar un `fb-...-deadbeef`. El comentario que habia en `comprobar_literales`
    lo predijo con esas palabras y aun asi paso. Al anadir un sitio con cita, amplia TODAS las
    guardias en el mismo commit: `comprobar_contra`, `comprobar_literales` y
    `comprobar_citas_revocadas`.
  - Casar por SUBCADENA en un JSON serializado es una trampa que bendice mentiras: `hechos.sesgo`
    declaraba que RN-003 lo consume -lo produce- y colaba porque su `cuando` contiene
    `sesgo_h4_criterio_ruptura`. Peor: corregir la declaracion hacia FALLAR la guardia. Se casa el
    token exacto, o se recorre el arbol.
  - Un hecho que se fija y nadie declara es invisible: `liquidez_tomada` (RN-004) y `estructura_m1`
    (RN-007) se fijaban sin estar en `hechos:`, asi que la guardia -que iteraba los declarados- no
    los veia. El primero es la precondicion de los dos esquemas de entrada: un motor que leyera
    `forma` habria entrado sin esperar a que se tomara la liquidez de M15.
  - `permite`/`prohibe` llevan LISTA, no mapa, asi que el recorrido de invocaciones los saltaba y
    sus objetivos no se comprobaban contra nada en once de las veinticuatro reglas vigentes.
  - Las cifras de un informe se verifican con la calculadora antes de escribirlas: 21, 27,6 y 28,2
    salen de 18x3-33x1, 18x3-33x0,8 y 18x3,4-33x1, y eso es lo que dice en que convencion cuenta
    el trader.
  - Cambiar un valor de negocio no es cambiar un valor: al superseder el registro del lotaje,
    dos citas quedaron apuntando a un registro revocado (RN-027 y el predicado
    `no_es_multiplo_de`) y dos textos quedaron afirmando algo falso (la nota de RN-015 y la
    descripcion de `base_calculo_objetivo` decian que el objetivo y el lote comparten distancia).
    Lo destaparon las guardias, no la lectura.
  - La guardia de citas revocadas ha nacido corta CUATRO veces: parametros (P13), luego reglas y
    glosario (RN-013), luego los predicados y acciones de F12, y en la auditoria de cierre se vio
    que seguian fuera los ACUMULADORES, que tambien llevan cita. Al anadir un sitio con `cita`
    propia, amplia `comprobar_citas_revocadas` en el mismo commit.
  - Las reglas no admiten cifras NI en un "nivel 0": `comprobar_contra` salta con el digito
    suelto. Se escribe "la entrada" y "el extremo de la caja".
  - `feedback apply` daba por NO-OP que el trader ratificara un default nuestro: comparaba la
    fuente anterior solo si era de tipo `feedback`, y un DEFAULT_AMBIGUOUS cita evidencia por
    definicion. Arreglado el 2026-09-11 con A-20. Si alguien anade un tipo de fuente, que mire
    esto.
  - Al cerrar una ambiguedad hay que tocar CUATRO sitios y solo dos los vigila una guardia:
    el registro (via `apply`), `ambiguedades.yaml`, la regla que la citaba -que probablemente
    citaba la evidencia DEBIL que abrio la duda- y la tabla de PROJECT_STATE. Mas el test de
    `test_kit` que congela que ambiguedades estan RESUELTAS. El quinto sitio era el recuento de
    `knowledge/spec/README.md` y ya no existe: F13 lo mato y ahora lo da `spec status`.
  - Y hay DOS formas de cerrarla, no una (ADR-0022): `RESUELTA` con un registro del trader que
    apunte A LA AMBIGUEDAD -no al parametro: es la guardia que A-20 estreno-, o `DECIDIDA` por el
    consultor con el ADR que la nombre, cuando lo que se decide es alcance, metodo o herramienta.
  - Una respuesta del trader POR ESCRITO fuera de sesion se registra con su captura en
    `Material adicional de su operativa/Mensajes del trader/`: asi el `respuesta_literal` son
    sus palabras y no una sintesis del consultor, que es la diferencia que A-11 y el lotaje
    tuvieron que declarar en `registrado_por`.
- Lecciones tecnicas (F11):
  - Los heredocs de bash convierten `\b` en el CARACTER backspace (0x08) dentro de un regex, y el
    patron deja de casar sin dar ningun error. Le paso a `test_no_business_literals`, que estuvo
    con dos patrones muertos sin que nadie lo viera. Escribir regex con Write o con `chr(92)`.
  - `make check` incluye `ruff format --check`: filtrar su salida con grep por "All checks passed"
    engana, porque esa linea la imprime `ruff check` y el format falla despues.
  - `grep -c` sin coincidencias devuelve exit 1 y corta un `&&`.
  - El paquete de una sesion ya celebrada NO se reproduce con `kit build`, y es correcto: el
    cuestionario se genera desde los parametros UNKNOWN y ya no lo estan. `kit check` lo trata
    como aviso si hay feedback de esa sesion.
- Lecciones tecnicas (F10): Dukascopy devuelve 503 y resets a mitad de mes: `data download`
  cachea por dia y se relanza hasta que el manifiesto existe; los literales de negocio no pueden
  ir en `src/` (`config.yaml` del kit); `random.shuffle` no es estable entre versiones (orden por
  hash); la guardia de fecha de commit se falsifica, la de ancestro no; el trader decide por
  sesion H4, no por dia.
- Lecciones tecnicas (F08): el token de CITA (F07, fiel a la cruda) y el token de BUSQUEDA (F08,
  acentos plegados y `0,75` = `0.75`) son distintos a proposito; `localizar_cita` no sirve para
  buscar frases (minimos de 4/3 tokens, una ventana, una localizacion): `buscar_secuencia` es la
  base comun; los segmentos de Whisper son de 5-15 s, asi que el AND va por segmento y la frase
  puede cruzar segmentos; `frames show` (mas cercano por pts) y `kb` (regular anterior
  existente, `referencia_en`) responden preguntas distintas.
- Lecciones tecnicas (F07): el ASR repite palabras en los bordes de segmento ("tiene tiene",
  "no no"): la cita literal las incluye; los segmentos con `boss/voz/blog/split` fuera de las 6
  sustituciones quedan como `dudas` y obligan `confianza: media`; la ventana `t0/t1` debe cubrir
  las palabras localizadas (+-2 s), el `--check` dice donde estan; una cita de <4 tokens o con
  `0,75` donde la cruda dice `0.75` no se localiza a proposito.
- Lecciones tecnicas (previos de F07): con `condition_on_previous_text=False` el
  `initial_prompt` solo condiciona la primera ventana de 30 s de cada fragmento; `hotwords`
  entra en todas pero alarga los segmentos mas alla de la ventana (hasta 40 s) y Whisper salta
  audio (~10 s perdidos en v5, "sell" -> "SL"); faster-whisper trunca el prompt a 223 tokens
  sin avisar (guardia `comprobar_prompt`, contar con `add_special_tokens=False`); medir SIEMPRE
  con la pasada oficial (`corpus transcribe`), no solo con un script suelto (el paso 1 no
  mostro la perdida, el paso 2 si); el YAML estricto rechaza un valor que empieza por comillas
  y sigue texto (`motivo: "x" ...`): sin comillas o todo entrecomillado; `write_text` sin
  `newline="\n"` mete CRLF en Windows y rompe `test_repository_integrity`; las herramientas de
  la sesion no suben binarios grandes a Drive (API: texto/base64 en el mensaje; navegador:
  dialogo nativo; `file_upload`: 10 MB).

## F05 (validada el 2026-09-05)
- Fotogramas de TODO el corpus a 1 fps en PNG sin perdida (ADR-0008), decision del usuario
  ("maxima fidelidad, sin restriccion de recursos") tras medir que una regla de "tramos con
  decision" marca el 46-99 % de cada video. 5 videos: 16 548 fotogramas (8,9 GiB los cuatro de
  F05 + v5) en `data/fotogramas/` (solo en esta maquina; se regeneran en ~11 min con `corpus
  frames extract`). Manifiestos inmutables `fr-v1-5a2a42c3`, `fr-v2-c5a09508`, `fr-v3-982da728`,
  `fr-v4-9ad0ebb8`, `fr-v5-718ecabb` (uno activo por video).
- Informe `docs/validation/F05-frame-extraction.md`: obligatorios leidos, candidatos A-9, ficha
  de reglas en Word (`fr-v3-982da728/101000`), material del 2026-09-05 (v5, xlsx abril, capturas),
  dos auditorias de cierre aplicadas.
- Material del 2026-09-05 ("Info extra de backtesting"): v5 `2026-09-05 21-03-59.mkv` (6 min,
  FXReplay abril; `tr-v5-large-v3-int8-float16-01a1ae03`, 99 segmentos, reemplazada el 2026-09-06
  por `tr-v5-...-3c6fbb57`, 80; en Drive desde el 2026-09-06), xlsx
  abril 2026 (38 operaciones) y 6 capturas de Analytics en `Material adicional de su operativa`.
  Hechos en PROJECT_STATE (seccion "Lineamientos recibidos del usuario y hechos del corpus", ya con ids de evidencia desde F07).
- Lecciones tecnicas: `fps=1` de ffmpeg NO da el fotograma del segundo exacto ni conserva el
  `pts` (regla `select` + `-fps_mode passthrough`); `-ss` necesita `-copyts`; `showinfo` despues
  de `select`; `start_time` debe ser 0. Otra build de ffmpeg = otra carpeta y otro manifiesto con
  `--reemplaza-a`.

## Metodo de trabajo acordado con el usuario
1. Brief en `docs/plan/features/F##-*.md` -> revision de diseno por un agente ANTES de programar.
2. Construir en la rama; commits pequenos; `make check` (o `uv run --no-sync ...` si la GPU tiene
   abierto `botsito.exe`).
3. Auditoria de cierre con dos agentes en paralelo (codigo/tests y docs/proceso) -> aplicar
   correcciones -> informe WAITING_FOR_USER_VALIDATION -> decirle al usuario explicitamente que
   pasos seguir y que debe decidir.
4. El usuario valida -> ritual, con `BOTSITO_ALLOW_MAIN=1` EXPORTADA durante toda la secuencia
   (la exige el hook `pre-commit` en el commit `docs(state)`, NO el merge: `git merge --no-ff`
   no dispara `pre-commit` y no hay `pre-merge-commit`): `git merge --no-ff` -> `git tag -a stable/F##`
   sobre el merge -> commit `docs(state)` que solo toca PROJECT_STATE.md -> `make check` -> push
   main + tag. (`state check` falla a proposito entre el merge y el docs(state).) El HANDOFF ya
   vino actualizado en la rama.
5. Commits que toquen `knowledge/spec` o `knowledge/cases` necesitan trailer `Fuente: ADR-NNNN` o
   ids `ev-`/`fb-` existentes. `knowledge/evidence`, `knowledge/feedback`, `data/manifests`,
   `knowledge/corpus/transcripciones` y `knowledge/corpus/fotogramas` son inmutables (hook +
   historial de git).
6. El usuario exige evidencia (hechos / hipotesis / inferencias separados), no quiere
   recomendaciones prematuras y quiere saber siempre "que debo hacer ahora".

## Comandos utiles
```
make check
uv run botsito knowledge validate
uv run botsito corpus transcript check
uv run botsito corpus transcript show --video v1 --t0 0:06:19 --t1 0:06:19 --margen-s 30
uv run botsito corpus transcribe --video v1        # reanudable; no llama al modelo si ya esta
uv run botsito corpus frames check
uv run botsito corpus frames show --video v3 --t 0:28:56 --n 3
uv run botsito corpus frames extract --video v5    # idempotente
uv run botsito kb find "break even" --top 10       # busqueda con fuente (F08)
uv run botsito kb at --video v4 --t 0:44:56 --contexto
uv run botsito spec check                              # la capa semantica sola (F12); sale con 1
uv run botsito kit build --sesion 2026-09-20-sesion-02 --seed 20260920   # paquete de sesion (F10)
uv run botsito kit check --sesion 2026-09-09-sesion-01   # el paquete real de la sesion 1
uv run botsito kit kappa --sesion-a 2026-09-09-sesion-01 --sesion-b 2026-09-20-sesion-02
uv run botsito kit hoja                                # hoja de respuestas en Word (raiz)
```

## Lecciones operativas
- `make check` mira la rama ACTUAL contra `Current Branch` de PROJECT_STATE: si creas la rama
  despues de pasar `make check`, la CI falla aunque en local estuviera verde. Crea la rama, ajusta
  PROJECT_STATE y luego valida.
- `knowledge validate` (guardia del trailer `Fuente:`) solo ve commits existentes: correrlo
  DESPUES de commitear cuando el commit toque `knowledge/spec` o `knowledge/cases` (README incluido).
- El clasificador del modo automatico de Claude Code bloquea `rebase`, `cherry-pick`, `branch -f`
  y a veces el merge a `main` con `BOTSITO_ALLOW_MAIN=1`: el usuario ejecuta esos comandos con `!`.
- La CI se consulta sin `gh`: `curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`
  (los logs del job requieren el token de `git credential fill`). El merge no tiene run propio: el
  que cuenta es el del `docs(state)`. Mirar SIEMPRE la CI de main tras el ritual.
- Heredocs bash con comillas simples anidadas o barras invertidas fallan en Git Bash: escribir el
  script a un fichero del scratchpad y ejecutarlo.
- Escribir ficheros con `newline="\n"`; git en UTF-8 con `core.quotepath=false`.
- Agentes: pueden caer por limite de sesion; si pasa, hacer la auditoria a mano y decirlo.
- Dukascopy da 503/cortes: la descarga tiene cache por dia y reintentos.
- Datos pesados (`data/transcripciones/`, `data/fotogramas/`) no estan en git: si se cambia de
  maquina, copiarlos o regenerarlos (transcribir ~1 h de GPU; fotogramas ~11 min).
