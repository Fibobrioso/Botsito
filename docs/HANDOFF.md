# HANDOFF · continuar Bot v3 desde otra terminal

Contexto humano que no cabe en `PROJECT_STATE.md`. Lee primero `PROJECT_STATE.md`: si este fichero
lo contradice, manda `PROJECT_STATE.md`. Regla (MASTER_PLAN §F): el HANDOFF se actualiza DENTRO de la
rama de cada funcionalidad, antes del merge; en `main`, tras el tag `stable/*`, solo puede cambiar
`PROJECT_STATE.md` (un `docs(handoff)` en main puso la CI en rojo dos veces, F04 y F05).

## Estado (2026-09-21, rama `trabajo/cobertura-material-del-kit` esperando validacion; lo de debajo es anterior)
- **LA RAMA NO VA DE JUNIO. VA DE QUE EL CERO SIGNIFIQUE UNA SOLA COSA.** Hasta hoy un dia sin
  filas podia ser DOS cosas incompatibles -«el trader miro y no opero», que es UN DATO SUYO, y
  «este mes no tiene material», que es AUSENCIA DE CONOCIMIENTO- y las dos daban EXACTAMENTE EL
  MISMO SILENCIO. El dia que alguien decida que un dia sin filas produce un `no_trade`, esa
  decision convertiria la segunda en la primera sin que nadie lo viera: fabricar una etiqueta del
  trader donde no hay material.
- **LAS DOS PREGUNTAS SON ORTOGONALES Y HACEN FALTA LAS DOS**, y esto es lo que hay que tener
  delante antes de tocar nada:

      vistos.yaml         ->  ¿ES CIEGO?       abril: NO.  junio: SI.
      cobertura_material  ->  ¿HAY MATERIAL?   abril: SI.  junio: NO.

  Junio es el UNICO mes con dataset que es ciego y esta vacio, y esa combinacion no se podia
  expresar hasta hoy.
- **TRES AGUJEROS, no uno.** (1) junio es ingerible HOY porque `dias_ingeribles` no leia el config;
  (2) junio entraria en el universo de un `kit build` NUEVO porque la llamada del kit no pasaba
  `cobertura`; (3) el cero significa dos cosas y ademas `--material` puede ser el libro equivocado
  sin que nada lo diga. El (3) es el que mas vale.
- **CERO TRAMOS ES UN VALOR CON SIGNIFICADO**, no un error: dice "hay decision sobre este mes y NO
  hay material". Hasta hoy el esquema lo rechazaba (`paquete.py:139-140`), y por eso la unica forma
  de excluir un mes era invertir el default para TODOS con `solo_con_cobertura`. **Ese flag SIGUE
  EN FALSE**: un mes no declarado queda SIN ACOTAR, no excluido, para no negar un mes legitimo que
  nadie haya declarado todavia.
- MEDIDO: `dias_ingeribles` pasa de **20 dias** (6 mayo + 10 JUNIO + 4 septiembre) a **10**, y
  junio se niega POR MES y con motivo, nunca nombrando dias.
- **LA REVISION DE DISENO REFUTO EL BRIEF TRES VECES**, y dos de esas refutaciones corrigen una
  medida que habia dado YO: que abril entraria en el universo de la sesion 2 -FALSO, esta en
  `vistos.yaml` desde el 2026-09-12- y que bastaba con poner el campo en el config -FALSO, la
  llamada del kit no lo pasaba-. Lei `manifiestos_del_prefijo` y afirme sobre la cadena sin seguir
  hasta el filtro de vistos. Es el patron 3 de la lista.
- **LA LIMITACION QUE ESTA RAMA CREA, y va dicha**: la regla por mes usa los DIAS PEDIDOS, asi que
  si el trader no hubiera operado en NINGUNO de los dias ingeribles de un mes, el libro correcto
  daria cero filas y el comando lo llamaria error. Con seis dias `dev` de mayo es improbable pero
  NO imposible. La alternativa -preguntarle al lector si el fichero tiene alguna fila de ese mes-
  rompe la regla de que el lector no acumula nada del libro (ADR-0037 §6). Si algun dia aparece ese
  error sobre un libro que SI es el suyo, esa es la salida y hay que decidirla entonces.
- **LO QUE NO SE DECIDE**: si un dia ingerible sin filas produce un `no_trade`. Hoy no produce nada
  y asi se queda. Lo que esta rama aporta es que, cuando se tome esa decision, se tomara sobre un
  conjunto donde el cero YA NO ES AMBIGUO.
- No se descargo abril, ni febrero, ni marzo. No se ingirio mayo: cero `caso-*.yaml`. A-18 y la
  prediccion congelada, sin tocar. El reparto y las anclas, sin tocar.

## La pasada por el material de septiembre (2026-09-21) · NADA DECIDIDO, TODO MEDIDO

- **LOS IDS NO SON CRONOLOGICOS Y LEERLOS COMO SECUENCIA ES UN ERROR.** Orden real por
  `fecha_grabacion` de `knowledge/corpus/fuentes.yaml`: **v2 (08-03) -> v3 (08-06) -> v1 (08-20) ->
  v4 (08-30) -> v5 (09-05) -> v6 (09-09)**.
- **LA BASE DE EVIDENCIA ESTA CONSTRUIDA SOBRE EL MATERIAL VIEJO.** De 368 items: v2 53, v3 102
  -los dos mas viejos, **42 %**-, v1 46, v4 132, v5 12, v6 23. **El material de septiembre aporta
  35 items, menos del 10 %.** Y el usuario dice que la operativa se fue aclarando video a video y
  que la version buena, con los arreglos, es la del ultimo.
- **NADA declara que lo mas reciente mande.** `fecha_grabacion` existe en `fuentes.yaml` y NINGUN
  mecanismo la usa. 11 items llevan `supersede` -13 ficheros lo mencionan-, y **8 de los 11 salen
  de v6**: el mecanismo existe y se usa a mano, pero no hay eje de recencia.

### LO QUE SALIO, Y POR QUE HAY QUE PARAR ANTES DE TOCARLO

**A-18 CITA UN ITEM QUE OTRO SUPERSEDE, Y EL QUE LO SUPERSEDE DICE LO CONTRARIO.** A-18 cita
`ev-v4-011951-5fb49e03`, y `ev-v6-014702-2d7096db` lo supersede. Las `notas` de ese item de v6
concluyen, con la aritmetica del trader -"3 - 3x0,75 = 0,75 y 3 - 3x0,80 = 0,60"-, que **el 1:3 se
mide sobre la CAJA COMPLETA**. Es la lectura OPUESTA a la que apunta el material de agosto (suelo
del RR realizado en 3,00, informe F14A §4), y **es tambien la opuesta a la que ADR-0037 escribio**
diciendo que `ev-v4-011951` "empujaba al mismo lado" que agosto: ese item esta superseded y su
sucesor empuja al otro.

**Y v5 -la DEMOSTRACION- apunta al tercer sitio, que es el de agosto.** En `v5 0:04:52` y
`v5 0:04:53` la herramienta de posicion de FX Replay muestra sus propias cifras mientras el trader
arrastra el objetivo:

```
0:04:52   Risk/Reward Ratio: 3.21   Target: 0.00061 (0.052%) 6.1   Amount: 1802.63
0:04:53   Risk/Reward Ratio: 3      Target: 0.00057 (0.049%) 5.7   Amount: 1750
```

0,00061/3,21 = 0,00019 y 0,00057/3 = 0,00019: **el riesgo es constante -1,9 pips- y lo que mueve es
el objetivo, hasta que el ratio marca exactamente 3.** Esa razon la calcula la herramienta entre su
zona de stop y su zona de objetivo, o sea **sobre la distancia entrada-stop**. Si el stop esta en el
0,8 -que es lo que el propio v5 dice en `0:03:12`, "si yo protejo a 0.80, que es el SL por
defecto"-, entonces el objetivo es 3 x RIESGO REAL y no 3 x caja. **CUIDADO CON ESTO**: no esta
medido a que nivel de la caja cae la zona roja en ese fotograma, y las dos lecturas se separan ahi.
Lo que si esta medido es que **la razon 3 se fija sobre entrada-stop**, no sobre la caja.

Y lo que el audio de v5 anade, `0:04:42`: *"sabemos que manejamos el calculo del RR en base al 1%"*,
seguido de un deictico -"que seria alli"- y NUEVE SEGUNDOS de silencio mientras dibuja. El 1 % puede
ser la caja entera o el riesgo por operacion, y el texto solo no lo decide.

**POR QUE NO HE ESCRITO EL ITEM NUEVO, que es lo que la regla manda.** Lo que un item de v5 sobre la
geometria contradice NO es la `afirmacion` de ningun item -la de `ev-v6-014702` es solo la
aritmetica, y es correcta- sino **las `notas` de ese item**, que son una INTERPRETACION. Y el tema no
coincide: `objetivo.rr_13_margen_tres_perdidas` frente a `objetivo.rr`. La guardia de
`evidence new --supersede` exige el MISMO tema, asi que por ahi no entra. **Se para y se avisa, como
estaba acordado.**

**LA CUARTA APARICION DEL PUNTO CIEGO, y con la dimension nueva.** `comprobar_citas_revocadas`
vigila reglas, glosario y vocabulario contra registros de FEEDBACK revocados. **No mira
`ambiguedades.yaml`, y no mira los `supersede` de EVIDENCIA.** Medido: **TRES ambiguedades citan
evidencia superseded** -A-10 y A-11, ya RESUELTAS, y **A-18, que sigue ABIERTA**-. `make check` pasa
verde con eso.

### A-21 y A-24 CONTRA v6: BUSCADO, NO APARECE

- **A-21** -que es una zona de control LIMPIA, sin ruido; bloqueante, `resuelve_en [F12, F20, F26]`;
  pregunta cuantas velas o cuanto retroceso de mas la invalida-. Terminos buscados en la cruda de
  v6: `limpi`, `ruido`. Diez coincidencias, y **ninguna da un criterio evaluable**: el "ruido" de v6
  es el de QUE VELAS cuentan al mapear el order block en temporalidad menor (`79:52`, `97:19`,
  `126:44`), no el de la zona de control. Lo mas cerca es `80:02`, *"yo por eso considero tratar de
  mapear de la manera mas limpia y mas objetiva posible, creo yo"*, que es una aspiracion y no una
  regla: si acaso REFUERZA la premisa de A-21. **Sigue abierta.**
- **A-24** -que hace que marques un pivote de M15 y no otro; bloqueante-. Terminos buscados:
  `pivote`, `considere`, y `m15` cruzado con `marc|traz|elij|escoj`. Diez coincidencias sobre M15 y
  **ninguna sobre el criterio de seleccion**: hablan de la temporalidad (`26:18`, *"la liquidez la
  solemos marcar en M15 y con eso basta"*), no de cual de varios candidatos se marca. **Sigue
  abierta.**

### LA RECENCIA ES SENAL, NUNCA ARBITRO, Y ESTE CASO ES POR QUE

El consultor iba a escribir "lo mas reciente manda" la manana del 2026-09-21. **A-18 es su
contraejemplo**: la recencia sola elegiria `caja_completa` -v6 es el mas nuevo- y LA PANTALLA de v5
y los backtests de agosto dicen lo contrario. **Un trader razonando sobre su regla puede
equivocarse sobre su propia regla; la herramienta que usa, no.** Por eso la recencia entra como
SENAL y no como arbitro, y por eso "el ultimo gana" a secas es peligroso: dejaria que un comentario
de pasada tumbe una explicacion cuidada, y aqui ademas dejaria que un razonamiento tumbe una
medida.

### Y LA DENSIDAD DE v5, QUE ES EL OTRO DATO DE LA PASADA

**v5 dura SEIS MINUTOS y aporta 12 items**; v3 y v4 son grabaciones largas y aportan 102 y 132. Lo
que falta no es material, es haberlo explotado. Y su naturaleza es la que mas decide, porque es la
UNICA donde el trader **dibuja la caja mientras explica**: la pasada de hoy saco de esos seis
minutos un fotograma que contradice una interpretacion escrita en un ADR. Mirar v5 es barato y no
esta hecho.

### LO QUE PUEDE CERRAR A-18, MEDIDO Y SIN EJECUTAR

La via del consultor: si la pata roja del fotograma es 0,8 de la caja, la caja mide **0,0002375**;
si es la caja entera, mide **0,00019**. La caja son niveles de estructura sobre EURUSD M1 del
**miercoles 29 de abril de 2026**, hacia las 10:03-10:08 (se lee en el eje del propio fotograma).
Con las velas de ese dia se mide la estructura y se compara. **`data/manifests/` NO tiene abril**
-tiene 2026-01, 05, 06, 07, 08 y 09-.

**MEDIDO ANTES DE DESCARGAR NADA, que es lo que el consultor pidio:**

1. **La colision que se temia NO se da.** El defecto documentado salta cuando DOS manifiestos del
   prefijo del kit cubren EL MISMO DIA (`universo()`: "dos datasets cubren el mismo dia: ids de
   caso repetidos"). Abril (2026-04-01..30) **no solapa** con ninguno de los seis meses presentes,
   y `reemplaza_a` no hace falta porque no sustituye a nadie.
2. **El paquete de la sesion 1 es INMUNE, y esta medido**: `ventanas.yaml` congela
   `datasets: [eurusd-m1-2026-01, -05, -06, -07, -08]` -cinco ids- y
   `manifiestos_del_prefijo(datasets=...)` (`cases/paquete.py:523-546`) devuelve EXACTAMENTE esos y
   falla si falta alguno. Es ADR-0035 haciendo su trabajo: `kit check --sesion
   2026-09-09-sesion-01` no cambia.
3. **PERO HAY OTRA COLISION, Y ES LA DE JUNIO CON UN MES MAS.** Un `kit build` NUEVO llama a
   `manifiestos_del_prefijo` **sin** `datasets`, o sea coge TODO lo que empiece por
   `eurusd-m1-`. Abril entraria en el universo de la sesion 2, y **abril es material de
   DESARROLLO** -la spec se infirio en parte de esos dias-. El `config.yaml` del kit NO tiene
   `cobertura_material`; el de fidelidad si. Son **22 dias laborables** de abril que se sumarian a
   los 10 de junio ya anotados.
4. **MITIGACION BARATA Y MEDIDA**, si se quiere descargar abril sin ampliar esa deuda: el filtro es
   `dataset_id.startswith(config.dataset_prefijo)` (`paquete.py:536`) y `data download --dataset`
   controla el nombre -el id le anade `-hash8`-. Un nombre que NO empiece por `eurusd-m1-` queda
   fuera de todo universo, ahora y en la sesion 2. **Contra**: un dataset de EURUSD M1 con otro
   nombre es en si mismo confuso, y esconde el problema en vez de arreglarlo. **La alternativa
   honesta es poner `cobertura_material` al `config.yaml` del kit ANTES de descargar abril**, que
   es lo que ya esta decidido para junio en `trabajo/mayo-dev-ingerido`. NO SE EJECUTA NADA: lo
   decide el consultor.

### EL ORDEN, DECIDIDO EL 2026-09-21: `cobertura_material` -> ABRIL -> A-18 -> MAYO

Tres ramas, y **ninguna mezclada con otra**. El motivo del consultor, que vale mas que el orden:

1. **`cobertura_material` PRIMERO Y SOLA.** Es una GUARDIA, y las guardias aterrizan solas: tiene
   criterio de aceptacion propio y desbloquea DOS cosas distintas -junio y abril-, asi que metida
   dentro de la rama que ingiere mayo no se puede validar ninguna de las dos por separado. Lleva la
   exclusion que GRITA -motivo y recuento- y tests. **DESCARTADA Y ESCRITA COMO DESCARTADA** la
   salida de descargar abril con un nombre fuera del prefijo: funciona, pero ESCONDE EL DEFECTO, y
   esconder defectos es lo que este proyecto lleva pagando toda la semana.
2. **ABRIL DESPUES, TAMBIEN SOLA.** Si la medida cierra A-18 cambia un parametro CONFIRMED de la
   spec, y eso exige ADR e informe propios: no se mete de matute en la rama que ingiere mayo.
3. **MAYO AL FINAL**, con la prediccion congelada intacta.

**LA ADVERTENCIA SOBRE LA MEDIDA DE ABRIL, para que no se venda antes de tiempo.** LA CAJA LA
DIBUJA EL TRADER SOBRE NIVELES QUE EL ELIGE. Con las velas del 29 de abril tendremos los altos y
bajos CANDIDATOS, pero **cual par escogio como nivel 0 y nivel 1 sigue siendo interpretacion
nuestra**. La via: entrada = nivel 0, riesgo = **0,00019** medido en el fotograma, y ver si
`entrada + 0,00019` cae sobre un nivel que este a 0,8 del siguiente alto estructural -lectura
`riesgo_real`, caja 0,0002375- o **sobre el alto mismo** -lectura `caja_completa`, caja 0,00019-.
Es un SELL sobre EURUSD M1 del miercoles 29 de abril de 2026 hacia las 10:03-10:08, que se lee en
el eje del propio fotograma. **PUEDE SALIR NO CONCLUYENTE, Y SI SALE ASI SE ESCRIBE ASI.** No es
una medida garantizada; es una medida que merece la pena.

**Y SI ABRIL CIERRA A-18, LA PREDICCION DE MAYO NO SE TOCA**: pasa a ser comprobacion
INDEPENDIENTE, que es mejor y no peor. No se reescribe ni se ajusta en ningun caso.

### QUIEN MIDIO QUE, PORQUE DESDE HOY SE MARCA

El consultor instituyo el 2026-09-21 marcar lo que se RELAYA y no se ha medido en primera persona.
De este bloque: **medido por la sesion** -que la frase falsa estaba en el informe y no en el ADR;
el tema `objetivo.rr_13_margen_tres_perdidas`; el comportamiento de `manifiestos_del_prefijo` con y
sin `datasets` (`cases/paquete.py:523-546`); los 22 laborables de abril-. **Medido por el
consultor** -que el .mkv de v5 es nativamente 1280x720; que en `0:04:52` se ven rotulados los
niveles 0, 0.5 y 0.8 con la herramienta de posicion encima-. **Medido por los dos por separado**
-que `fr-v5-718ecabb.yaml` declara esa misma resolucion, y que `data/manifests/` tiene 2026-01, 05,
06, 07, 08 y 09 y no abril-.

### LO QUE NO SE HA HECHO, A PROPOSITO

No se ha declarado ninguna regla de recencia: **la decide el consultor con ADR**, y lleva matiz -v6
es un cuestionario y manda sobre lo que se le pregunto, callando en lo demas; v5 es una demostracion
y manda sobre la geometria que ensena; "el ultimo gana" a secas dejaria que un comentario de pasada
tumbe una explicacion cuidada-. No se ha tocado `evidence/`, ni `ambiguedades.yaml`, ni la
prediccion pre-registrada de mayo, que **no se toca pase lo que pase**: si v5 o v6 cierran A-18, esa
prediccion se queda como comprobacion INDEPENDIENTE.

## Estado (2026-09-21, rama `feature/F14a-ingesta-del-detalle` esperando validacion; lo de debajo es anterior)
- LO PRIMERO, PORQUE VUELVE A PASAR: `CLAUDE.md` §3 prohibia "el detalle por operacion de los xlsx"
  EN BLOQUE, y ADR-0021 §1 dice "en esos dias" desde el 2026-09-12. TERCERA VEZ que este fichero es
  mas estricto que el ADR sin que ningun ADR lo diga, y las tres veces bloqueo un paso NECESARIO.
  Corregido, con su caja. **Si te topas con una prohibicion de `CLAUDE.md`, buscala en el ADR antes
  de obedecerla.**
- EL CRITERIO, que es lo que hay que entender antes de tocar nada: LA GRANULARIDAD DEL DATO, no el
  tipo de fichero (ADR-0037). Las filas de un dia `dev` se leen; una pestana de totales del mismo
  libro NO se abre nunca, y NINGUNA autorizacion la abre, porque lleva los reservados dentro y no se
  puede trocear. Y la ESTRUCTURA se VERIFICA contra una lista escrita antes: la pestana se
  SELECCIONA, no se enumera, y el conjunto de FECHAS del libro no sale del lector -un "14 dias en el
  libro" publica que dias reservados NO opero el trader, y un dia laborable sin operaciones ES su
  etiqueta-.
- LO QUE MAS VALE DE LA RAMA NO ES EL CODIGO, ES LO QUE SE MIDIO. Se abrio AGOSTO -material de
  desarrollo, cero dias reservados, comprobado ANTES con `casos_reservados(repo)` y declarado el
  mismo dia- y resulto que NINGUNA columna del libro es el objetivo planeado. `maxTP` esta relleno
  si y solo si la operacion gano (20/20 con `rPnL > 0`; 27 sin `maxTP`, ninguna ganadora): es un
  resultado. `idealTP` cae DEL LADO DE LA PERDIDA en 4 de 47 -las cuatro `sell` perdedoras-.
- EL OBJETIVO ES UNA REGLA, `objetivo_rr` con `base_calculo_objetivo`, y el xlsx NO LO REGISTRA.
  Cita literal del trader: `ev-v2-001658-d02fb71a` (v2 0:16:58). POR ESO EL CASO NO LLEVA CAMPO
  `objetivo`, y no es que lo lleve vacio: un campo opcional vacio es una invitacion a que alguien lo
  rellene con `maxTP` dentro de seis meses. QUITAR EL CAMPO ES EL MECANISMO.
- LA LECCION QUE HAY QUE LLEVARSE: lo cazo EL INVARIANTE GEOMETRICO -para `buy` el stop por debajo
  de la entrada, para `sell` por encima-, que estaba puesto como test PERMANENTE DE HIGIENE y no
  como discriminador. Tres cruces disenados a proposito -presencia contra resultado, RR calculado
  contra RR declarado, recuento de valores distintos- miraban CORRELACIONES y no lo vieron. Una
  comprobacion de sentido puesta por higiene vale mas que un cruce disenado, porque no sabe que
  esta buscando. Se queda como guardia permanente: cualquier fila que la viole ABORTA la ingesta
  nombrando la fila.
- EL CORPUS CONTESTO DOS VECES LO QUE IBA A IRSE AL TRADER, en el mismo dia: el objetivo
  (`ev-v2-001658-d02fb71a`) y los parciales (`ev-v1-002313-6342a154`, `ev-v2-001819-60a1b0f1`, y
  sobre todo v6 0:17:07, el trader EN LA SESION 1: "sin toma de parciales y que tiene que llegar al
  ratio 1.3 si o si" -el ASR escribe 1.3 donde dice 1:3-). BUSCA EN EL CORPUS ANTES DE REDACTAR
  CUALQUIER AMBIGUEDAD. Una pregunta al trader cuesta un hueco de sesion; la busqueda no cuesta
  nada. A-33 NO se abre.
- `dateStart` VIENE EN UTC, y esa medida sostiene la asignacion a sesion H4: convertidas a
  `huso_operativa` las 47 operaciones de agosto caen dentro de las dos sesiones; leidas como hora
  local de Madrid, 16 quedarian fuera.
- LOS DIAS NO SE ELIGEN, SE DERIVAN: no hay `--dias`. `dias_ingeribles` = casos de un reparto
  COMMITEADO menos `casos_reservados`. Un dia fuera de todo reparto ABORTA el comando entero; un dia
  reservado se descarta sin escribirse y SIN NOMBRARSE en la salida.
- ES LA PRIMERA VEZ QUE HAY PRECIOS BAJO `knowledge/cases/`. Por eso `problemas_de_biblioteca` corre
  dentro de `knowledge validate` siempre y sin `data/`, y hay test de contrato: ningun fichero de
  `knowledge/cases/dev/` puede corresponder a un caso reservado.
- NO SE HA INGERIDO NADA DE VERDAD: cero `caso-*.yaml` en el arbol. Los tests van contra un xlsx
  SINTETICO. Si el usuario dice que si, la ingesta real de mayo son 6 casos y su commit necesita
  trailer `Fuente:` (`knowledge/cases/` esta en `DIRECTORIOS_CON_FUENTE`).
- ERROR MIO, VISIBLE Y SIN REESCRIBIR: ADR-0037 se commiteo (`a791f92`) diciendo que el objetivo es
  `idealTP`. La correccion va EN CAJA dentro del propio ADR. Y peor que el error: antes de medir
  escribi DOS consecuencias para F26 en direcciones OPUESTAS, las dos falsas. Una consecuencia para
  F26 es una afirmacion como cualquier otra y no se escribe sin medir la cadena entera hasta ella.
- DEUDA QUE DESCUBRE ESTA RAMA Y HAY QUE LEER: JUNIO sigue siendo `dev` en el reparto de la sesion 1
  y ADR-0025 lo descarto. `dias_ingeribles` devuelve 20 dias: 6 de mayo, 10 DE JUNIO y 4 de
  septiembre. Hoy inocuo -no hay xlsx de junio- pero el dia que llegue uno se escribirian 10 casos
  de un mes descartado sin que nada chille.
- Y AL VALIDAR, EL CONSULTOR ENCONTRO LO MEJOR DE LA RAMA MIRANDO LO MISMO OTRA VEZ: el suelo del
  RR no mide el objetivo PLANEADO, mide el RR REALIZADO sobre entrada-stop, que es exactamente lo
  que A-18 lleva abierta desde F11. Las dos lecturas PREDICEN: `caja_completa` da
  `objetivo_rr / stop_fraccion_caja` = 3/0,8 = 3,75; `riesgo_real` da 3,00. Agosto da SUELO EN 3,00
  -18 filas con `maxTP` e `initialSL`, minimo 2,50, TRES clavadas en 3,00, 16 de 18 por debajo de
  3,75-. **LA COMBINACION CONFIRMED DE HOY NO CUADRA CON EL MATERIAL**: o la base es `riesgo_real`,
  o el stop del trader en su backtest no esta a 0,8 de la caja, y las dos tocan un parametro
  CONFIRMED.
- POR QUE NO SE DECIDE A-18, y esto es lo que hay que entender antes de tocarla: es UN mes, son 18
  filas, y **LA CAJA NO ESTA EN EL FICHERO**. El RR que se mide es riesgo real POR CONSTRUCCION, asi
  que si el stop del trader viviera en el borde de la caja las dos lecturas coincidirian y la medida
  NO DISCRIMINARIA. Lo que hay es la primera medida que A-18 ha tenido nunca, y apunta al mismo lado
  que `ev-v4-011951-5fb49e03` ya empujaba. A-18 gana la nota en `ambiguedades.yaml`; su estado, su
  `decision` y su `evidencia` NO se tocan.
- CORREGI UN NUMERO DEL BRIEF: decia "todos por debajo de 3,75" y son 16 de 18 -hay un 3,75 exacto y
  un 5,33-. No cambia la conclusion; la refuerza, porque un suelo EN 3,00 con tres filas clavadas es
  la firma de un objetivo en 3R sobrepasado, no la de un 3,75R al que 16 ganadoras no llegaron.
- LA FRASE DE F26 VA POR SU TERCERA REDACCION EN UN DIA: F26 podra puntuar el objetivo contra la
  regla CUANDO A-18 ESTE CERRADA, no antes, porque hoy la regla tiene dos lecturas que difieren un
  25 % del recorrido. LAS DOS PRIMERAS VERSIONES LAS ESCRIBIO EL CONSULTOR EN EL BRIEF y se
  transcribieron a ADR-0037 y al informe, que hasta hoy se las atribuian a quien las redacto: EL
  FALLO FUE EN LA DECISION, NO EN LA REDACCION, y por eso la regla vigila EL BRIEF y no la
  transcripcion. La tercera no es error de nadie: la cadena era mas larga de lo que estaba escrito. La regla se amplia: **la cadena hasta F26 incluye las ambiguedades
  ABIERTAS que cuelgan de los parametros que nombra.**
- LA PREDICCION DE MAYO ESTA PRE-REGISTRADA Y COMMITEADA EL 2026-09-21, ANTES DE MIRAR MAYO. NO SE
  TOCA DESPUES DE MIRAR; si la cambias despues, no vale nada. REGION DISCRIMINANTE: el RR implicito
  de `maxTP` sobre entrada-stop en **[3,00 , 3,75)**. `riesgo_real` la predice POBLADA con suelo y
  moda en 3,00; `caja_completa` la predice VACIA con suelo en 3,75. AGOSTO: **15 de 18 dentro**
  (fuera: un 2,50 por debajo, un 3,75 y un 5,33 por arriba).
- EL CRITERIO, congelado: region POBLADA con suelo en 3,00 -> dos meses independientes, SE DECIDE
  A-18 hacia `riesgo_real`, con ADR y con el cambio del parametro. Region VACIA con suelo en 3,75
  -> los dos meses se contradicen, A-18 sigue ABIERTA y SUBE A `bloqueante: true`, porque el
  material diciendo cosas distintas segun el mes es peor que no saber. Otra cosa -> se escribe lo
  que de y NO SE FUERZA.
- Y LA TRAMPA DE ESA MEDIDA, que hay que repetir en el brief: LA CAJA NO ESTA EN EL FICHERO. Si
  mayo apunta a `riesgo_real`, la lectura alternativa es que el stop real del trader este en 1,0 y
  no en 0,8, y eso tocaria `stop_fraccion_caja`, que TAMBIEN es CONFIRMED. Las dos salidas son
  hallazgos y las dos exigen ADR: NO SE ELIGE LA COMODA.
- EL 2,50 SE MIRA APARTE: es una GANADORA que cerro por debajo de 3R, y contradice el "sin toma de
  parciales y que tiene que llegar al ratio 1.3 si o si" de v6 0:17:07. Una fila no tumba una cita,
  pero se nombra, y en mayo se mira si hay mas como ella.
- **EL TERCER PATRON DE DEFECTO, y desde hoy se comprueba en cada rama junto a los otros dos: UNA
  REGLA QUE ENUMERA LOS CASOS EN VEZ DE NOMBRAR LA CONDICION DEJA FUERA EL CASO QUE NADIE PENSO.**
  Los otros dos son (1) un input GLOBAL y MUTABLE del que depende la reproduccion (ADR-0035) y (2)
  una prohibicion escrita MAS ESTRICTA que el ADR. Tres apariciones del tercero esta semana:
  `CLAUDE.md` decia que sitios toca ABRIR y CERRAR una ambiguedad y no contemplaba EDITARLA -eso
  dejo `ambiguedades.md` desincronizado hoy y `make check` en rojo-; `leer_fichero` enumeraba
  `1|2|3` en vez de negar por defecto y el `..` se colaba; y `CARPETAS_RESERVADAS` convive con un
  fallback a `holdout-1` que es una enumeracion con agujero. EL ARREGLO ES SIEMPRE EL MISMO:
  nombrar la condicion y negar por defecto.
- LO QUE VIENE, decidido: rama `trabajo/mayo-dev-ingerido`, y NO es solo ingerir. Ingiere los 6
  `dev` de mayo Y REPITE LA MEDIDA DEL RR sobre ellos. Si mayo tambien da suelo en 3,00, la lectura
  `caja_completa` queda en serios apuros y entonces SI toca decidir A-18. Ahi entra tambien
  `cobertura_material` para junio, CON LA EXCLUSION QUE GRITA -nunca en silencio-, y sin tocar el
  reparto de la sesion 1, que esta anclado por blob.
- A-33 CERRADA SIN ABRIRLA, y bien cerrada: v6 0:17:07, y encaja con `parciales` y con
  `objetivo_extension_activa: false` que la sesion 1 ya cerro.
- LA PUERTA SIGUE CERRADA: `PREREGISTRO.md` intacto (blob `52649183...`, marca `SIN RELLENAR`), cero
  `AUTORIZACION-*.md`, ninguna particion abierta. Esta rama no pre-registra ni firma nada.
- LO SIGUIENTE, que no es codigo y lleva semanas de plazo: pedirle al trader FEBRERO O MARZO.

## Estado (2026-09-21, rama `trabajo/puerta-por-pregunta` esperando validacion; lo de debajo es anterior)
- EL SORTEO DE SEPTIEMBRE ESTA CERRADO EN MAIN (merge 15a49b0, tag `stable/F13-septiembre-sorteo`).
- LO QUE HAY QUE ENTENDER ANTES DE TOCAR LA PUERTA: `abrir` es PURA y lo seguira siendo. Por eso el
  historial de git NO puede servir de registro de aperturas -no distingue "usada una vez" de "usada
  cincuenta", porque son el mismo arbol y el mismo commit-, y por eso una funcion pura del estado no
  puede negar la segunda apertura si nada cambio entre las dos. Medido: cincuenta aperturas
  seguidas, `git status` vacio.
- LO QUE CIERRA EL AGUJERO: la autorizacion CITA una pregunta, la pregunta vive en `PREREGISTRO.md`
  con estado, y EL COMANDO la gasta ANTES de leer. El orden importa y no es simetrico: "gastada y no
  leida" cuesta volver a pre-registrar; "leida y no gastada" es el defecto.
- GASTAR INVALIDA TODAS LAS AUTORIZACIONES VIVAS, y eso es DESEABLE, no un fallo: es la caducidad
  automatica. Si alguien ve varias autorizaciones caidas a la vez tras una apertura, es el mecanismo
  funcionando. Firmar no invalida nada: solo gastar o editar.
- `kit kappa --incluir-holdout` EXIGE `--pregunta <id>`. El acto de abrir declara para que se abre.
- DOS HUECOS MAS CERRADOS: `casos_reservados` GRITA ante un reparto ilegible (antes devolvia un mapa
  incompleto indistinguible de uno completo), y `leer_fichero` decide sobre la ruta RESUELTA -el
  `..` saltaba la puerta, medido-.
- Y UNA CORRECCION DE LO QUE ESCRIBI AYER: el test de la puerta NO cazaba "un camino fuera del glob"
  como decia su docstring; los dos lados de la igualdad pasaban por `repartos_commiteables`. Ahora
  hay una enumeracion que sale del disco. ADR-0036 §Impacto lleva la correccion.
- SIGUE ABIERTO Y ES LO PRIMERO ANTES DE FIRMAR NADA, pero NO es lo que yo habia escrito: NO HAY
  FUGA. Medido con etiqueta en holdout-1 y holdout-2 y firmada solo la de holdout-2, el comando
  FALLA nombrando `AUTORIZACION-holdout-1.md` y NO gasta la pregunta. Lo que hay es el ESPEJO: una
  pregunta se gasta UNA vez y abre N particiones, y N LO DECIDE EL DATO -hay que firmar toda
  particion con etiqueta en esas rondas o el comando falla entero-. El arreglo, que el llamante
  pueda nombrar la particion, es RAMA PROPIA.
- Y OJO CON ESTO ANTES DE LA PRIMERA FIRMA: hoy no existe ni un LABEL_CASE, asi que
  `kit kappa --incluir-holdout --pregunta P1` GASTA LA PREGUNTA SIN ABRIR NADA -`por_particion`
  vacio: cero `abrir`, un `gastar_pregunta`- y falla despues con "no hay unidades que comparar".
- `leer_fichero` NO TIENE LLAMANTE DE PRODUCCION: hoy la puerta protege UN SOLO COMANDO. Por eso su
  fallback -que juzga una carpeta desconocida bajo la autorizacion de holdout-1- se queda en
  Technical Debt y no se toco aqui.
- EL PREREGISTRO SIGUE VACIO Y NO HAY NI UNA AUTORIZACION FIRMADA. Esta rama construye el mecanismo;
  no pre-registra ni firma nada.
- LO SIGUIENTE, que no es codigo: pedirle al trader febrero o marzo.

## Estado (2026-09-21, rama `trabajo/septiembre-sorteo` esperando validacion; lo de debajo es anterior)
- EL CAMINO DE FIDELIDAD ESTA CERRADO EN MAIN (merge 06330e2, tag `stable/F13-camino-de-fidelidad`,
  CI verde). Esta rama lo ESTRENA con el reparto de septiembre.
- EL REPARTO, y su argumento, que es lo que hay que poder reproducir: artefacto `eurusd-2026-09`,
  seed 20260921, 14 dias del 1 al 18, cupos 4 `fidelidad-dev` + 10 `fidelidad-1`, y `fidelidad-2` y
  `fidelidad-3` VACIAS a proposito. Se concentro por la TENTACION y no por la potencia: ningun
  reparto llega a 36 unidades efectivas, y tres cubos de ~3 dias no dan tres medidas sino tres
  cifras que se contradicen, que es una invitacion a escoger la que convenga.
- LOS DOS CUBOS VACIOS SON UNA RESERVA, no un olvido: esperan a febrero o marzo, el mes limpio que
  sigue pendiente de pedirle al trader. Si alguien los llena con material ya visto, quema dos
  aperturas para no medir nada.
- SOLO 4 `dev` porque MAYO YA TIENE SEIS SIN ABRIR. Los de septiembre estan para comprobar la
  ingesta y el formato contra un mes DISTINTO, no para afinar el motor.
- NADIE HA ABIERTO NADA, ni antes ni despues del sorteo. Los `dev` se abren con su propio brief.
- LA FECHA DEL BACKTEST ES EL 2026-09-19, no el 20. El 20 era la fecha de la ENTREGA y hacia de
  sustituta. La fuente es la declaracion del consultor del 2026-09-21 y esta escrita TAL CUAL: no
  hay captura en `corpus/.../Mensajes del trader/`. EL 19 ES SABADO Y CUADRA -el material llega al
  viernes 18-, y esta dicho en `vistos.yaml` y en el informe porque es el tipo de dato que dentro
  de seis meses alguien "corrige" pensando que es una errata.
- SIGUEN EN PIE, y no son de esta rama: el freno de ADR-0036 §6 -antes de la PRIMERA autorizacion
  hay que cerrar `excluir` en `kappa_entre_sesiones`- y la cita con el problema de re-descargar un
  mes, que nos ata al rango 2026-09-01..20.
- LO SIGUIENTE DE VERDAD: pedirle al trader un mes que no haya tocado (febrero o marzo). Es lo unico
  que puede llenar `fidelidad-2` con una cifra defendible.

## Estado (2026-09-21, rama `trabajo/septiembre-particiones` esperando validacion; lo de debajo es anterior)
- LOS CUPOS CONGELADOS ESTAN CERRADOS EN MAIN (merge 93e17a2, tag `stable/F13-cupos`, CI verde).
- ESTA RAMA SE ABRIO PARA SORTEAR SEPTIEMBRE Y LA REVISION DE DISENO LO PARO, y el consultor lo dio
  por bueno: `kit build` NO PUEDE construir un paquete de septiembre. `vistos.yaml` declara
  `2026-09` con `visto_el: 2026-09-20`, `universo()` excluye sus 14 dias con motivo "mes visto por
  el trader" y `construir()` aborta si alguno se cuela. Forzarlo exigia falsear la fecha de la
  sesion o desactivar el filtro de vistos. ADR-0034 §6 YA LO DECIA: "el camino del kit es el del
  etiquetado ciego y, por construccion, no sirve aqui". Leelo antes de proponer nada por ahi.
- LA RAMA ENTREGA SOLO EL MECANISMO (ADR-0036). EL SORTEO VA EN LA SIGUIENTE, a proposito: un ADR
  decidido y estrenado en el mismo aliento acaba con la forma de la conveniencia de un mes.
- LO QUE HAY QUE SABER PARA LA RAMA DEL SORTEO:
  * Los cupos de `knowledge/cases/fidelidad/config.yaml` estan EN CERO. Los decide el consultor con
    `Fuente:` y su argumento, y DESPUES de ver cuantos casos quedan de verdad: `asignar` descarta el
    sobrante EN SILENCIO, que es como la sesion 1 perdio `2026-05-25` y `2026-06-29`.
  * Lo medido sobre el reparto: los nombres de particion del kit son GLOBALES -un
    `AUTORIZACION-<nombre>.md` por nombre y un mapa plano que tira el paquete-, y el proyecto tiene
    TRES aperturas en total. Partir 14 dias en tres cubos las quema todas en una sola pregunta y
    baja la potencia de 0,68 a ~0,27 por cubo.
  * `botsito fidelidad build --artefacto <id> --seed <n>` y DESPUES
    `botsito fidelidad anclar --artefacto <id>`, EN EL MISMO COMMIT. Sin ancla, el artefacto nace
    con el agujero que la rama de ayer tapo.
- LO QUE ESTE CAMINO NO PROMETE, Y ESTA ESCRITO EN TRES SITIOS A PROPOSITO (ADR-0036 §8, el README
  del directorio y la cabecera de `cases/fidelidad.py`): NO da una cifra con potencia. Hacen falta
  36 unidades efectivas y septiembre entero da ~23; mayo tampoco llega. Da ANTERIORIDAD DEMOSTRABLE
  y una cifra DESCRIPTIVA con su intervalo. Si alguien cita esa cifra como fidelidad medida, esta
  afirmando lo que no se probo.
- LA CAPTURA QUE MAS VALE DE ESTA RAMA: `cobertura_material` NO admite una lista de dias, solo
  tramos, y el validador lo rechaza por la FORMA. Un dia laborable del rango que no apareciera en la
  lista seria un dia sin operaciones, y eso ES su etiqueta: declararlos publicaria etiquetas por la
  puerta de atras.
- LA DEUDA DE LA GUARDIA DE ANCESTRO QUEDA CERRADA en su cuarta aparicion:
  `cases/anterioridad.py` empareja por CASO y no por `sesion`, recorre los repartos de los DOS
  caminos y no depende de que existan etiquetas. Se ve fallar con mutante, incluido el que hoy
  pasaba: una etiqueta que lleva en `sesion` el nombre de otro paquete.
- BLOQUEANTE PARA ABRIR, no para esta rama: `kappa_entre_sesiones` deja `excluir` vacio tras pasar
  la puerta, asi que UNA autorizacion lee las etiquetas de los tres cubos. Hay que cerrarlo ANTES DE
  LA PRIMERA AUTORIZACION. Hoy es seguro porque `PREREGISTRO.md` sigue vacio.
- OJO SI EL TRADER ENTREGA MAS SEPTIEMBRE: la descarga de hoy cubre del 1 al 20 -`congelar` rechaza
  `hasta >= hoy`, asi que era el maximo legal- y re-descargar el mes entero rompe `kit build` en
  silencio: dos manifiestos del prefijo que cubran el mismo dia dan "dos datasets cubren el mismo
  dia". `reemplaza_a` se escribe para datasets y NADIE LO LEE. Anotado en Technical Debt.
- EL NOMBRE DE LA RAMA SE QUEDO VIEJO a mitad de camino; el informe se llama
  `docs/validation/CAMINO-DE-FIDELIDAD.md`, por lo que la rama hace.

## Estado (2026-09-21, rama `trabajo/cupos-congelados` esperando validacion; lo de debajo es anterior)
- EL UNIVERSO CONGELADO ESTA CERRADO EN MAIN (merge dfc7e20, tag `stable/F13-universo`, CI verde).
- ESTA RAMA ES SU ENMIENDA, no un ADR nuevo, y el motivo no es de estilo: ADR-0035 dejo escrito en
  su Impacto que NO cerraba "los cupos de `config.yaml`, que suman 40 frente a los 14 dias
  laborables de septiembre". El precedente del repo para esto es unanime (ADR-0007, ADR-0015,
  ADR-0022 llevan la enmienda DENTRO del fichero viejo; ADR-0033 fue nuevo porque estrenaba
  mecanismo).
- EL BLOQUEO DE SEPTIEMBRE ESTA QUITADO: `comprobar()` recompone con el bloque `config:` congelado
  del paquete, asi que editar `config.yaml` para los 14 dias ya NO rompe la sesion 1. Medido con el
  global a 6/3/3/2: `kit check` de la sesion 1 IDENTICO a su linea base y `knowledge validate` en
  exit 0 con el aviso de deriva.
- EL HALLAZGO DE LA RAMA, Y ES EL QUE HAY QUE RECORDAR: LA FALSABILIDAD DE LO CONGELADO NO ERA
  UNIFORME. Editar `particiones` dentro del bloque congelado se ve -`particiones.yaml` no se exime
  nunca-, pero editar `anclajes_candidatos`, `sesiones` o `etiquetas` NO se veia: solo alimentan
  `ventanas.yaml` y `hoja_trader.md`, que una sesion celebrada exime. Mutante medido ANTES de
  escribir codigo: exit 0 y "sin diferencias que no explique la sesion celebrada". La linea que
  comparaba contra `config.yaml` era LO UNICO que lo impedia, asi que cambiarla de sujeto sin nada a
  cambio habria abierto el agujero. De ahi que la rama sea la completa (opcion A) y no la minima.
- EL ANCLA: `knowledge/cases/kit/anclas.yaml` declara el sha del BLOB de `ventanas.yaml` y
  `particiones.yaml` por sesion. Patron `preregistro_blob` (ADR-0033) y sus tres requisitos: vive
  FUERA del fichero que ata, es BLOB y no commit -`ventanas.yaml` ya tiene dos commits y un ancla de
  commit lo habria dado por alterado sin estarlo- y RE-ANCLAR ES EXPLICITO
  (`botsito kit anclar --sesion <s> --reanclar`). NO depende de que existan etiquetas, a proposito:
  `validar_paquetes` se desentiende con `if not etiquetas: continue` y hoy no hay ni un LABEL_CASE.
- SI TOCAS UN PAQUETE, RE-ANCLALO. Es el unico paso nuevo del dia a dia: cualquier byte de esos dos
  ficheros que no coincida con su ancla pone `knowledge validate` en rojo, y eso es lo que se quiere.
- DOS TESTS CAMBIAN DE SIGNIFICADO A PROPOSITO, y esta escrito en su docstring: donde afirmaban que
  sin etiquetas el paquete se podia regenerar libremente, ahora exigen que tocarlo se vea.
- LO QUE SIGUE ABIERTO y no se mezclo: la guardia de ancestro empareja por `sesion` y no por caso
  -ANTES DE LA PRIMERA ETIQUETA-, y `lectura_de_velas` aun lee el `config.yaml` de hoy para el
  prefijo (ultimo hilo del patron, anotado en Technical Debt).
- LO SIGUIENTE, YA SIN BLOQUEO: descargar las velas de 2026-09 y SORTEAR Y COMMITEAR las particiones
  de sus 14 dias laborables antes de que nadie lea una etiqueta. Y ahi hay una decision que es del
  consultor y no del codigo: CUANTOS CUPOS para 14 dias, con su `Fuente:`. Acotar el universo al
  1-18 -lo que cubre el backtest del trader- sigue pendiente de decidir COMO; "visto" no es el
  motivo correcto para los dias 19 y 20, porque no los ha backtesteado.

## Estado (2026-09-20, rama `trabajo/universo-congelado` esperando validacion; lo de debajo es anterior)
- LA ENTRADA DE SEPTIEMBRE ESTA CERRADA EN MAIN (merge ad2693d, tag `stable/F13-septiembre`).
- EL BLOQUEO ESTA ARREGLADO: cada paquete declara sus `datasets:` en `ventanas.yaml` y `comprobar()`
  se recompone con esa lista, no con el disco de hoy. `construir()` de un paquete NUEVO sigue
  leyendo el disco A PROPOSITO: congelarlo tambien seria el tercer caso del mes de una prohibicion
  que bloquea un paso que el proceso exige. ADR-0035.
- LA CIFRA, MEDIDA, por si hace falta defenderla: el universo de la sesion 1 son 42 dias y `asignar`
  reproduce `particiones.yaml` exacto; metiendo los 14 dias de septiembre cambian 23 de esos 42 y
  `holdout-3` se queda sin ninguno de sus 8 dias. (En la revision dije 33: sumaba los 10 dias de
  septiembre que entran, que no son casos que cambien de particion.)
- DERIVAR LA LISTA NO VALE, medido: enero, julio y agosto aportan 66 de las 67 exclusiones de la
  sesion 1 y ni un solo caso, y el donante por contiguidad es invisible en `casos[]`.
- LA EDICION DE LA SESION 1 SE HIZO HOY PORQUE HOY SE PODIA: la guardia que congela `ventanas.yaml`
  se arma con el primer `LABEL_CASE`, y hay cero. Fue aditiva -6 lineas, ninguna quitada- y la
  prueba es que `kit check` da la salida IDENTICA a la linea base comparada con `diff`.
- OJO AL SIGUIENTE MES: esta rama tiene que estar dentro ANTES de congelar ABRIL tambien, no solo
  septiembre. `2026-05-01` esta hoy excluido por "ventana fuera del dataset" porque falta abril, y
  abril es mes visto: el dia que abril entre, ese dia pasa a ser caso con un donante de cero casos.
- SIGUEN ABIERTOS, y no se mezclaron: los cupos de `config.yaml` (40 frente a 14 dias de
  septiembre) y la guardia de ancestro, que empareja por `sesion` y no por caso y se arregla ANTES
  DE LA PRIMERA ETIQUETA.

## Estado (2026-09-20, rama `trabajo/septiembre-entra` esperando validacion; lo de debajo es anterior)
- LA LIQUIDEZ DE M15 ESTA CERRADA EN MAIN (merge b60c44b, tag `stable/F13-liquidez`, CI verde).
- ENTRO EL BACKTEST DE SEPTIEMBRE (seis capturas y un xlsx, 2026-09-20). Hecho: la EXPOSICION
  declarada el mismo dia -el consultor leyo la columna de fechas, del 1 al 18: NO QUEMA-, los siete
  ficheros en el inventario, septiembre declarado visto con `visto_el: 2026-09-20` y ADR-0034
  diciendo QUE ES.
- LA FECHA EN QUE EL TRADER LO BACKTESTEO NO SE SABE y esta PEDIDA. `visto_el` es la de la entrega,
  que es la unica con fuente (mismo criterio que abril). Si llega, se corrige con su fuente delante.
- LAS VELAS Y LAS PARTICIONES NO ENTRARON, y el motivo NO es el que el brief preveia: ademas de que
  los cupos suman 40 para 14 dias, DESCARGAR LAS VELAS DE SEPTIEMBRE ROMPE LA SESION 1 POR SI SOLO.
  `_manifiestos_del_kit` coge todo manifiesto con el prefijo del kit, asi que un dataset nuevo entra
  en el universo de TODOS los paquetes. Decidido: se congela el universo EN EL PROPIO PAQUETE, como
  se hizo con config.yaml; NO se separa el prefijo y NO se acepta perder la reproduccion. Rama
  propia. LINEA BASE medida hoy: `kit check --sesion 2026-09-09-sesion-01` exit 0, y el criterio de
  esa rama es salida IDENTICA con `diff`, no solo exit 0.
- LA GUARDIA DE ANCESTRO SE ARREGLA ANTES DE LA PRIMERA ETIQUETA. Empareja por el campo `sesion` y
  nunca por el caso; hoy no hay ningun LABEL_CASE y por eso no puede fallar, pero en cuanto exista
  uno la prueba de anterioridad ya esta comprometida. Tercera vez que se apunta: ahora va con
  condicion fechada en ADR-0034 §Impacto y en Technical Debt.
- PENDIENTE DEL CONSULTOR: precisar `CLAUDE.md`, que pone el backtest de septiembre entero fuera de
  alcance hasta tener las particiones commiteadas; la lectura del dia 20 cruzo esa regla. No se toco
  en la rama, porque cambia una regla de la casa.
- OJO CON EXCEL: el `~$*.xlsx` de un libro abierto entra al inventario si se ejecuta con Excel
  abierto, y desaparece al cerrarlo, rompiendo `corpus check`. Cerrar Excel ANTES de inventariar.

## Estado (2026-09-20, rama `trabajo/liquidez-m15` esperando validacion; lo de debajo es anterior)
- LAS TRES RAMAS DEL 17-09 ESTAN CERRADAS EN MAIN: vistos (1c2561e), reglas de la casa (52f579d) y
  breaker de M1 (53e9d17, docs(state) 60216f8, CI verde). Main tenia la spec en 12.1.0.
- EL METODO VOLVIO A GANARLE AL TEXTO. Los dos agentes de la revision DISCREPARON en lo principal
  -si A-24 era una eleccion o dos casos- y lo resolvio el fotograma: el "complex pullback" de v3
  0:12:42 esta dicho sobre un CROQUIS A MANO en un grafico de 1h (fr-v3-982da728/781000), y en ese
  dibujo el alto mas alto es ademas el ultimo, asi que no distingue nada. Cuando dos lecturas del
  texto chocan, la pantalla decide; y si la pantalla no lo dice, eso tambien es un resultado.
- A-24, A-25 Y A-26 EXISTEN YA en ambiguedades.yaml, con sus ids reservados y las tres reescritas.
  A-24 es BLOQUEANTE: nadie produce `liquidez_m15` en la spec, RN-008 es un `ninguno_de` y por eso
  prohibe abrir operacion SIEMPRE. La regla de marcado NO se ha escrito a proposito: la decide A-24.
- LO QUE EL CORPUS YA CERRABA SE ESCRIBE, no se vuelve a preguntar: el flujo de la vela que marca la
  liquidez es el de M15 -cuatro citas- y eso esta ahora en la spec, no solo en una pregunta.
- ANTES DE ABRIR UNA AMBIGUEDAD, MIRA EL FOTOGRAMA: A-33 (¿nivel o rango?) no se abrio porque v4
  0:57:06 ensena una LINEA etiquetada "15 lq", no una banda. Entra como nota en el token.
- TRES ITEMS CON EL MISMO VICIO (ev-v4-005319 el 17-09; ev-v3-001531 y ev-v4-005703 hoy): la
  `afirmacion` quita el deictico o el matiz de la cita -"aqui", "suelo", "en este caso", "me es
  indiferente"- y la convierte en regla general. Son de `extractor: llm` y los tres se cazaron
  MIRANDO LA PANTALLA. Es un patron de extraccion, no tres descuidos: el proximo repaso de F07 tiene
  que mirar los items llm con esa lente.
- EL PUNTO CIEGO DEL DETECTOR VA POR LA TERCERA (0,75, breaker, liquidez). Queda contado en
  PROJECT_STATE con la consecuencia: rama con nombre en la proxima planificacion, no mas parches.
- RIESGO DE FIDELIDAD, DICHO EN EL INFORME §3: el trader marca la liquidez "la que tu consideres". Si
  la sesion 2 responde eso, el bot no puede reproducirlo y la pregunta deja de ser de la spec para
  ser del proyecto.

## Estado (2026-09-17, rama `trabajo/breaker-m1` validada y pendiente del ritual; lo de debajo es anterior)
- LAS REGLAS DE LA CASA YA ESTAN EN MAIN (merge 52f579d, tag `stable/F13-reglas`), y esta rama las
  lleva incorporadas: se fusiono `main` DENTRO de la rama para reconciliar el choque en
  `PROJECT_STATE.md` y en este fichero. Merge y no rebase: los commits de la rama estan validados y
  citados por sha en el informe y en PROJECT_STATE, y un rebase los reescribiria.
- LA CONTRADICCION DEL BREAKER NO ERA UNA CONTRADICCION, y se resolvio MIRANDO LA PANTALLA, no
  razonando: en v4 0:53:12-0:53:17 el grafico esta en M15 (con zonas etiquetadas `m1 lq` y `15 lq`)
  y desde 0:53:18 en M1; lo que rompe con mecha es un NIVEL DIBUJADO al que apunta una flecha -la
  mecha lo perfora y el cuerpo cierra por debajo-, no la ruptura del esquema de entrada.
  `ev-v4-005319` decia mas que su cita: lo supersede `ev-v4-005310-ce69f8c6`, con cita de audio Y de
  pantalla. Para fechar una afirmacion del trader sobre lo que se VE, el fotograma manda.
- UNA PROPUESTA NO PUEDE LLEVAR `supersede`: el esquema de `_proposals` no lo admite y `evidence
  accept` tampoco. Los supersede se crean con `evidence new --supersede`, como los ocho primeros
  (commit 2003e61). Si alguna vez se quiere el rastro de propuesta, hay que ampliar el esquema.
- EL CONFIRM SOBRE UN ITEM SUPERSEDIDO NO ROMPE NADA, medido antes de aceptar: la comprobacion de
  existencia usa TODOS los items desde 653efdc. Ojo con `feedback pending`, que imprime "un CONFIRM
  confirma un item que ya vive" sin mirar si vive; el veredicto es correcto, la frase no.
- `breaker_m1_criterio_ruptura` ES NUEVO (enum mecha|cuerpo, `mecha`, CONFIRMED por ev-v4-005910).
  `se_da_esquema` lo toma como argumento y RN-008 lo pasa en su forma: sin eso no tendria lector.
- A-32 VA A LA SESION 2 con el fotograma delante: si el nivel roto es la liquidez de M15 o de M1.
- CLAUDE.md YA NO PROHIBE `data/` EN BLOQUE, y se separa en TRES cosas (peticion del consultor al
  cerrar esta rama, 2026-09-17): los fotogramas y las transcripciones SE LEEN; las velas para
  recalcular ventanas se leen y no es abrir (ADR-0021 §1, ADR-0033); y lo prohibido sin la puerta es
  `knowledge/cases/holdout/**`, el detalle por operacion de los xlsx, las capturas de Analytics y el
  backtest de septiembre hasta que sus particiones esten sorteadas y commiteadas. POR QUE SE SEPARA:
  la prohibicion en bloque venia de una instruccion del consultor mal redactada, y dejo sin abrir la
  unica fuente que cierra geometria sin gastarle un turno al trader. Medido hoy: 25.372 PNG a 1 fps y
  solo 8 fotogramas citados por 9 items de 365 -dos de esos ocho los cita esta rama-.
- CORRECCION A LA PREMISA DEL ENCARGO: el fotograma obligatorio v4 0:12:30 ("caja con el nivel
  0,75 = 1,19537") SI se abrio y SI esta citado, por `ev-v4-001221-1e66b5fd`
  (`fr-v4-9ad0ebb8/750000`, revisado "fotograma visto"). Los tres obligatorios de
  `fotogramas_obligatorios.yaml` estan citados. Lo que la auditoria del 09-13 dice de ese fotograma es
  mas estrecho: no se midio QUE VELA O MAXIMO ANCLA EL NIVEL 1 en v4 0:12:30, que sigue sin medirse.
- VALIDADA por el usuario el 2026-09-17, desviacion incluida.
- TRES DEUDAS ANOTADAS en PROJECT_STATE, todas medidas en esta rama: el detector no ve los temas
  hermanos (segunda vez); la via de propuesta no admite `supersede`, asi que toda correccion de
  evidencia se sale del mecanismo de propuestas; y un CONFIRM sobre un item supersedido queda
  invisible -`kb find` filtra por activos- y sin aviso -`feedback pending` dice REFLEJADO con un
  motivo que ya no es cierto-.

## Estado (2026-09-17, rama `trabajo/reglas-de-la-casa` esperando validacion; lo de debajo es anterior)
- LOS MESES VISTOS ESTAN CERRADOS EN MAIN (merge 1c2561e, tag `stable/F13-vistos`, CI verde).
- YA NO SE PEGA EL RITUAL A MANO EN EL CHAT. Hay dos ficheros nuevos, ambos de esta rama:
  - `CLAUDE.md` en la raiz: lo que toda sesion lee sola. Por donde se empieza, main no se toca, los
    regimenes de cambio, el trailer `Fuente:`, las TRES guardias de `cita`, las cifras al registro
    (ADR-0002), el holdout (ADR-0033: leer velas no es abrir), los cuatro sitios de una ambiguedad,
    las trampas medidas (heredoc y ``, `## Estado` con punto, `make check` a `/dev/null`) y DONDE
    ESTA EL TEXTO DE LAS TRANSCRIPCIONES. Toda regla se verifico contra el repositorio antes de
    escribirla; si una deja de ser cierta, se corrige ahi en el mismo commit que la rompe.
  - `docs/runbooks/RITUAL.md`: el ritual de cierre tal como se ejecuta, con lineas `!`, con sus
    puertas y con las tres correcciones de esta semana.
- LA CORRECCION DE PROCESO DEL 2026-09-17: con lineas `!`, `make check` pasa de los 120 s y se va a
  segundo plano, asi que el push NO se encadena detras en la misma tanda. Se espera el aviso de la
  tarea y se pushea despues. Ese dia se pusheo antes de saber si pasaba (paso, pero fue suerte).
- `BOTSITO_ALLOW_MAIN=1` va PEGADA a la linea del `git commit`: cada linea `!` abre una shell nueva.

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
