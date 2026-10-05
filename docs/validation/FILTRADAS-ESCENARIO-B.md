# Las filtradas de sesión en el escenario B

Rama `trabajo/filtradas-escenario-b`, abierta el 2026-10-04 desde `main` en `f712650` (commit de
estado sobre el merge `44f461d`, tag `stable/F36w-cuarentena-por-condicion`). Encargo:
`docs/encargos/trabajo-filtradas-escenario-b.md`. Es el punto P de la Next Action.

**Cómo se lee.** El informe va en el orden en que se hizo, con cada respuesta del consultor copiada
antes de lo que hizo con ella.
- La fase 0 (§0) se paró sin escribir nada.
- Después, por orden del consultor:
  - las B se escribieron fuera del repositorio y no se instalaron (§1);
  - se registraron 8 tramos nuevos (§4);
  - se documentó el hueco (§5).
- El estado final está en «## Estado».

De ninguna filtrada ni cruda se ha leído texto en toda la rama.

## 0. Fase 0

### 0.1 Rutas y hoja de cada vídeo

Todo fuera del repositorio, en el Escritorio de esta máquina. Solo se miraron nombres (`ls`), sha256
y la línea `hoja:` de cada registro, que no trae texto del trader.

| Vídeo | Hoja | Cruda | Filtrada actual (A) | Filtrada ANTES |
|---|---|---|---|---|
| v7 | `--sesion 02` (registro: «hoja: la de la sesion 02») | `sesion-02-v7-audio/sesion-02-v7.cruda-NO-LEER.jsonl` | `sesion-02-v7-audio/sesion-02-v7.filtrada.md` (sha256 `8690ce43…`) | no hay: su «antes» es su tramo no citable |
| v8 | `--sesion 02` | `sesion-02-v8-audio/sesion-02-v8.cruda-NO-LEER.jsonl` | `sesion-02-v8-audio/sesion-02-v8.filtrada.md` (`4e752803…`) | no hay; sin tramos |
| v9 | `--sesion 03` | `sesion-03-audio/sesion-03.cruda-NO-LEER.jsonl` | `sesion-03-audio/sesion-03.filtrada.md` (`61a084f6…`) | `sesion-03-audio/sesion-03.filtrada-ANTES-condicion.md` (`f7529459…`, la de `SESION-04-EXTRACCION.md` §1.2) |
| v10 | `--sesion 04` | `sesion-04-audio/sesion-04.cruda-NO-LEER.jsonl` | `sesion-04-audio/sesion-04.filtrada.md` (`2952b8f5…`) | `sesion-04-audio/sesion-04.filtrada-ANTES-condicion.md` (`6394c3f3…`) |

- El audio de cada sesión está en la misma carpeta (`*.m4a`), y es el `--audio` que corresponde.
- Los registros ANTES de v9 y v10 no llevan la línea `hoja:`, porque los escribió el guion de antes
  de la sesión 4. La hoja de esos dos ya era la 03 y la 04.
- Hay además una copia antigua de la filtrada de v9, de la rama `sesion-04`, en
  `sesion-03-audio-copia/` (`f7529459…`, idéntica a ANTES).

### 0.2 Lo que se midió sin escribir nada

Guion: `docs/validation/anexos/FILTRADAS-ESCENARIO-B/medir_fase0.py`, con la salida en
`medir_fase0-SALIDA.txt`. Lee solo:
- las marcas `[CUARENTENA mm:ss–mm:ss]` de las filtradas;
- la marca `[mm:ss]` del principio de cada línea visible (el texto que la sigue no se guarda ni se
  imprime);
- la línea de recuento de cada registro.

Del repo lee los tramos y los intervalos de los ítems. Se ejecutó dos veces y la salida es idéntica.
**Su salida commiteada es una instantánea de la fase 0** (revisor, A1). Lee los tramos del repo, así
que desde que entraron los 8 tramos del §4 da v9 20 tramos y v10 22, frente a los 13 y 21 de la
salida y de la tabla del §0.4. No se regenera, porque documenta lo que se midió entonces.

**Los controles, antes de dar cifras** (lección de la rama anterior):
- **Caso negativo, v8:** 0 bloques en A y 0 tramos, como se esperaba.
- **Caso positivo, v9 y v10:** los bloques de ANTES se registraron como tramos en sus ramas, así que
  cada uno tiene que caber en un tramo. **El primer intento falló en v9 (6 de 8 «fuera»)**:
  - la causa era mi medida, no los datos;
  - la marca de la filtrada trunca al segundo y yo le sumaba uno al final, mientras que los tramos de
    v9 terminan en el segundo exacto;
  - con un segundo de tolerancia en el final, 0 fuera en v9 y en v10;
  - la función `cabe` lo documenta, y la salida commiteada es la del guion corregido.

**ANTES y A** (no hace falta escribir nada para medirlos):

| Vídeo | ANTES: segmentos / bloques | A: segmentos / bloques | Bloques de A que no estaban antes | Ítems ev-* en ellos |
|---|---|---|---|---|
| v7 | sin filtrada; 1 tramo | 9 / 3 | 2 (0:10:47, 0:32:59) | 0 |
| v8 | sin filtrada; 0 tramos | 0 / 0 | 0 | 0 |
| v9 | 29 / 8 | 57 / 15 | 8 | 0 |
| v10 | 45 / 12 | 89 / 23 | 15 | 2 (`ev-v10-014823-64248489`, `ev-v10-014853-76602fb4`) |

Las marcas de los bloques nuevos, una por una, están en la salida del anexo.

### 0.3 Lo que NO se puede hacer como dice el encargo: la guardia

**(a) Medir B «con el Filtro real y `meses_libres` del repo, sin escribir la filtrada».** En las
sesiones no hay camino que no sea rodear:
- El `Filtro` de la librería oculta la sesión entera (motivo a: `SESIONES_EN_CUARENTENA`) y no deja
  ver ningún segmento.
- Aplicar la regla mecánica (`en_cuarentena(textos, libres)`) a la cruda exige leerla:
  - con `crudo=True`, que solo usan los llamadores de `AUTORIZADOS` y la guardia bloquea;
  - o con código que nombre `*.cruda-NO-LEER.jsonl`, que la guardia solo admite si es el guion de
    `main` tal cual.
- El guion de `main`, la única vía revisada, **siempre escribe la filtrada** (`procesar` →
  `_escribir`). No tiene un modo «medir sin escribir».

**(b) Los límites en milisegundos «sacados del Filtro» para los tramos nuevos (fase 1, punto 5).**
Por la misma razón, en las sesiones no se pueden sacar del `Filtro`. La filtrada solo da `mm:ss`.
Los tramos de la cuarentena mecánica de v9 y v10 se registraron así: el `mm:ss` del bloque, con t1
un segundo después (`SESION-04-EXTRACCION.md` §2.2). En v6 sí se pudo usar el `Filtro`, porque no es
una sesión en cuarentena.

**Propuestas para (a), decide el consultor:**
1. **(recomendada) Rehacer en una carpeta aparte, sin tocar las oficiales.**
   - Se copia solo el `*.m4a` de cada sesión a una carpeta nueva del Escritorio y se ejecuta el guion
     de `main` tal cual, sin `--solo-filtrar`: `uv run python scripts/transcribir_sesion.py --sesion
     NN --audio <copia>.m4a`.
   - Hace el ASR otra vez y escribe una cruda nueva y la filtrada B en esa carpeta. El ASR es
     determinista: con v7, v8 y v10 dio los mismos segmentos que el corpus (602, 229 y 1914).
   - Así se mide B con las marcas, y se evalúan las paradas ANTES de tocar las filtradas oficiales.
   - Escribe ficheros fuera del repo, en una carpeta nueva, y cuesta una hora y media de GPU.
2. **Dar la fase 1 por adelantada.** Apartar A como `*.filtrada-A-condicion.md`, ejecutar
   `--solo-filtrar` en su sitio y medir después. Si salta una parada, se devuelve A a su nombre.
   Escribe las oficiales antes del visto bueno.

**Para (b):** `mm:ss` del bloque con t1 un segundo después, como los de v9 y v10, o lo que diga el
consultor.

### 0.4 La parada de «DESTAPADO dentro de un tramo» saltaría por diseño

**Las filtradas no aplican los tramos no citables:** el guion solo conoce la regla mecánica. La
medida, que solo cuenta marcas de tiempo, da hoy:

| Vídeo | Líneas visibles dentro de un tramo, en ANTES | En A |
|---|---|---|
| v7 | — | 0 (0 de 1 tramo) |
| v8 | — | 0 (no tiene tramos) |
| v9 | 82, en 5 de 13 tramos | 79, en 4 de 13 |
| v10 | 52, en 15 de 21 tramos | 49, en 14 de 21 |

**De dónde vienen esas líneas:**
- **Bordes.** Las marcas truncan al segundo, y los tramos de cuarentena y de SIN AUDIO llevan un
  segundo de margen al final. Así cuentan como «dentro» la línea visible que empieza en el mismo
  segundo que el tramo, o la que lo sigue. En v10, por ejemplo, los tramos que empiezan en 0:00:58 y
  0:45:05.
- **Tramos de precaución y de conversación personal**, que se marcaron AL LEER la filtrada y que la
  filtrada sigue enseñando:
  - v9: 0:32:20, 1:13:04 y 1:39:43;
  - v10: 0:40:20, 1:27:44, 1:43:42 y 1:56:07.

Con B pasará lo mismo, salvo donde un bloque nuevo los tape. Con la definición del encargo («visible
en B y dentro de un tramo»), **la parada saltaría en v9 y v10 seguro**, y no por la regla nueva.

**Para el consultor:**
- (i) Si la parada se refiere solo a lo que B DESTAPA respecto a A (visible en B, oculto en A y
  dentro de un tramo), eso sí se puede medir con la propuesta 1.
- (ii) Que la filtrada enseñe el texto de los tramos no citables es un hueco aparte. Lo ve cualquiera
  que lea la filtrada. Arreglarlo exige cambiar el guion (que la filtrada tape también los tramos),
  que esta rama no puede tocar.

## Respuesta del consultor a la fase 0 (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la fase 0 de trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Cómo se mide B: adelantando la fase 1, en su sitio. Nada de ASR nuevo.
>    Por qué: escribir una filtrada que nadie lee no expone nada. Un ASR completo crea otra copia de material en cuarentena fuera del repo, cuesta hora y media de GPU y no garantiza los mismos segmentos en v9.
>    Cómo:
>    a) Antes de ejecutar nada, copia cada filtrada A a *.filtrada-A-condicion.md y apunta su sha256. Las ANTES no se tocan.
>    b) Ejecuta uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion NN, con el --audio de cada vídeo, guion de main tal cual.
>    c) De las filtradas B solo se miran las marcas [CUARENTENA …], los recuentos y los ids. Nadie las abre hasta que yo dé el visto bueno.
>    d) Si salta una parada, se restaura A desde la copia, se comprueba que el sha256 coincide con el apuntado y me avisas.
>
> 2. Límites de los tramos nuevos: mm:ss del bloque, con el inicio al segundo y un segundo de margen al final.
>    Por qué: es lo único que da la filtrada sin leer la cruda, y el segundo de margen corrige el truncado que tu control positivo detectó.
>    Antes de usarlo, verifica en tramos_no_citables.yaml y en sus informes que v9 y v10 se registraron así. Si no fue así, para y dime cómo se hizo.
>    Cada tramo nuevo tiene que pasar tu control positivo: el bloque de B cabe entero dentro del tramo.
>
> 3. Las paradas quedan así, y sustituyen a las del encargo:
>    - algún ev-* cae en un segmento oculto en B que estaba visible en ANTES (o en sus tramos, para v7 y v8);
>    - algún segmento oculto en A pasa a visible en B y cae, aunque sea en parte, dentro de un tramo no citable;
>    - algún segmento oculto en ANTES pasa a visible en B. Dame cuántos y de qué vídeo, y no se usa esa filtrada hasta que yo decida.
>    Por qué: la parada de tramos que escribí presuponía que las filtradas aplicaban los tramos, y no lo hacen. Lo que mide esta rama es lo que B cambia frente a A, no un hueco que ya estaba.
>
> 4. El hueco de los tramos no se arregla aquí; se documenta.
>    Por qué: arreglarlo exige cambiar el guion, y la guardia solo deja ejecutar el de main.
>    En el informe, una sección propia con:
>    - para cada tramo de v7–v10: su clase (precaución, conversación personal u otra), el commit y la fecha en que entró, y cuántas líneas de la filtrada A y de la B caen dentro. Todo sin texto;
>    - qué lecturas de esas filtradas constan en los informes (extracción de las sesiones 3 y 4 y otras) después de la fecha de cada tramo;
>    - si hay alguna lectura posterior de un tramo de precaución, no la declares tú: me la pasas, y yo decido si va a HOLDOUT-EXPOSICIONES.md.
>
> 5. Next Action, en el commit que cierre esta rama: añadir después de P un punto nuevo:
>    «Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con test sintético que rompa la guardia a propósito; tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10. Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera.»
>    Por qué: la activación de la sesión 4 lee la filtrada de v10, y hoy esa filtrada enseña tramos de precaución.
>
> 6. Hallazgo del consultor para ERRORES-RECURRENTES, que se apunta en la fila de esta rama al cerrarla:
>    importa · El consultor escribió una parada sobre los tramos dando por hecho, sin medirlo, que las filtradas los aplicaban. Lección: antes de escribir una parada sobre un mecanismo, medir que el mecanismo existe.
>
> Lo demás del encargo sigue igual: los sha, v9 frente a f7529459…, los tramos nuevos por su régimen, ficheros_con_ocultos, knowledge validate, el test de tramos con su rotura a propósito, los recuadros en los dos informes cerrados, make check sellado, fix/ con la CI de Linux y sus números de run, y el revisor.
>
> Rama lista para revisión, NO cerrada.

## 1. B medido en su sitio (respuesta del consultor, punto 1), y la parada P2

### 1.1 Lo que se hizo

**a) Las A, apartadas, con su sha256 apuntado ANTES de ejecutar nada.** Cada filtrada A se copió a
`*.filtrada-A-condicion.md` y su registro a `*.registro-A-condicion.txt`. Los sha256 de las A:

| Vídeo | sha256 de A |
|---|---|
| v7 | `8690ce4385106098bdd97ced429a00f558648fd9e7fc4f9c8c37b43b15b99f1e` |
| v8 | `4e7528034bbafd11e4dfe70c9dcd27170f1d1cb3874c0517e09c39ff1f48bc71` |
| v9 | `61a084f60d20fe6ebe74a08c072a57b42c4c3cf63221b40f050211909b2b03c0` |
| v10 | `2952b8f55fa2c5a2bf9c28ca369cc477a18f8a96af862fb44801d2d3468240c4` |

Las ANTES no se tocaron.

**b) El guion de `main`, tal cual.** `git diff --quiet main -- scripts/transcribir_sesion.py` dio
igual, y el guion pasa `meses_libres_del_repo()`. Se ejecutó uno por vídeo:
- `uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion 02 --audio "C:/Users/USER/Desktop/sesion-02-v7-audio/sesion-02-v7.m4a"`
- `uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion 02 --audio "C:/Users/USER/Desktop/sesion-02-v8-audio/sesion-02-v8.m4a"`
- `uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion 03 --audio "C:/Users/USER/Desktop/sesion-03-audio/sesion-03.m4a"`
- `uv run python scripts/transcribir_sesion.py --solo-filtrar --sesion 04 --audio "C:/Users/USER/Desktop/sesion-04-audio/sesion-04.m4a"`

De su salida solo se miraron las líneas `hoja`, `segmentos` y `motivos`.

**c) De las B solo se miraron marcas, recuentos e ids.** Anexo:
`docs/validation/anexos/FILTRADAS-ESCENARIO-B/medir_fase1.py`, con la salida en
`medir_fase1-SALIDA.txt`. Se reprodujo y la salida es idéntica byte a byte. Después del §4 ya no:
su tabla por tramo da 8 filas más, una por tramo nuevo. Es una instantánea de la fase 1 y no se
regenera (revisor, A1). **Nadie ha abierto
ninguna B.**

**d) Salta la parada P2, así que se restauró A** (§1.3).

### 1.2 Lo que da B

| Vídeo | ANTES: segmentos / bloques | A | B | sha256 de B |
|---|---|---|---|---|
| v7 | sin filtrada; 1 tramo | 9 / 3 | **3 / 1** | `213ecbf2e0bf67500859c27d8b9b2f09bb91c5fd4551ec8ade25c2911a4e8345` |
| v8 | sin filtrada; 0 tramos | 0 / 0 | **0 / 0** | `4e7528034bbafd11…` (la misma que A) |
| v9 | 29 / 8 | 57 / 15 | **29 / 8** | `f7529459b4c97d12bb9ad74ef24318d6b7c8b15365f6fafb06e4228c4c4a027b` |
| v10 | 45 / 12 | 89 / 23 | **48 / 13** | `a07251504287cfba092881ffb5202fb745dae8224471d1e81d758e44e73e59eb` |

- **v9:** su B es **byte a byte** la de ANTES y la de `SESION-04-EXTRACCION.md` §1.2
  (`f7529459…a027b`). La regla por condicion no cambia nada en v9, porque v9 no nombra el mes que la
  lista vieja no cubría.
- **v10:** B tapa 3 segmentos y 1 bloque más que ANTES. El bloque nuevo es el de 1:55:27, junto al
  tramo manual de 1:55:29.

**Las paradas, medidas a nivel de segmento y sin bordes.** Las tres filtradas de cada vídeo salen de
la misma cruda. Así, una línea que B destapa es una marca que aparece más veces entre las visibles de
B que entre las de A (o las de ANTES), contadas como multiconjunto.
- La primera versión comparaba marcas con rangos de bloques y daba falsos destapados en los bordes,
  porque la marca trunca al segundo.
- La delató v9: su B es idéntica a ANTES, y aun así salían 4 destapados. Con el multiconjunto salen
  0, que es lo correcto.

| Parada | v7 | v8 | v9 | v10 |
|---|---|---|---|---|
| P1: ev-* en un bloque de B que no estaba oculto en ANTES (o en sus tramos) | 0 | 0 | 0 | 0 (el bloque nuevo de 1:55:27 no lleva ningún ítem) |
| P2: segmento oculto en A, visible en B, que cae (aunque sea en parte) en un tramo | 0 | 0 | **3** (1:13:55, 1:14:04, 1:14:05) | **3** (0:01:26, 0:40:20, 0:40:41) |
| P3: segmento oculto en ANTES y visible en B | 0 | 0 | 0 | 0 |

### 1.3 La parada P2: qué es y qué se hizo

**Salta P2 en v9 y en v10, con 3 segmentos cada una.** Ninguno es nuevo frente a ANTES (P3 = 0):
estaban visibles en las filtradas de antes de la regla por condicion, y solo A, que tapaba los 12
meses, los ocultaba.

| Vídeo | Segmentos | Tramo en el que caen |
|---|---|---|
| v9 | 1:13:55, 1:14:04, 1:14:05 | el tramo de precaución 1:13:04–1:14:16 |
| v10 | 0:40:20, 0:40:41 | el tramo de precaución 0:40:20–0:40:42 |
| v10 | 0:01:26 | empieza en el segundo anterior al tramo de cuarentena 0:01:27–0:01:37 («aunque sea en parte») |

Es el hueco del §0.4 (las filtradas no aplican los tramos), visto desde B.

**Lo que se hizo, por el punto 1d:**
- Se **restauró A desde la copia** en las cuatro sesiones, con su registro, y los sha256 coinciden con
  los apuntados (`8690ce43…`, `4e752803…`, `61a084f6…` y `2952b8f5…`).
- Antes, cada B se guardó como `*.filtrada-B-condicion.md` (y su registro como
  `*.registro-B-condicion.txt`), sin abrirla, para que el consultor decida sin repetir nada.
- **No se ha registrado ningún tramo, y la filtrada oficial vuelve a ser A.**

### 1.4 Antes de registrar tramos, el punto 2: v9 y v10 no se registraron igual

Se compararon los tramos de cuarentena de v9 y v10 con las marcas de sus filtradas ANTES, solo con
tiempos:
- **v10 (sesión 4):** inicio al segundo y final con un segundo de margen, en los 12 bloques. Es lo que
  propone el punto 2.
- **v9 (sesión 3): inicio al segundo y final AL SEGUNDO EXACTO DE LA MARCA, sin margen**, en los 8
  bloques. Por ejemplo, el bloque `[CUARENTENA 22:11–22:16]` es el tramo `0:22:11`–`0:22:16`.
  - Según `SESION-03-EXTRACCION.md` §1 y el motivo de cada tramo («segmentos 404-406 de la cruda»),
    se sacaron de los índices de segmento con un guion que no imprimía texto, antes de que existiera
    la guardia.
  - El resultado es que el final de cada tramo de v9 es el segundo truncado del último segmento: la
    cola de ese último segundo puede quedar fuera del tramo.

**Por el punto 2 («si no fue así, para y dime cómo se hizo») se para aquí también.** El único tramo
nuevo que pediría B es el de v10, el bloque de 1:55:27, que no cabe en el tramo manual de 1:55:29.

### 1.5 Por tramo: líneas visibles en A y en B (para la sección del hueco, punto 4)

La tabla completa, sin texto, está al final de `medir_fase1-SALIDA.txt`. Lo que más pesa:
- **v9:** el tramo de precaución de 1:39:43 enseña 67 líneas en A y en B; el de 1:13:04, 9 en A y 12
  en B.
- **v10:** el de precaución de 1:56:07, 13 líneas en A y en B; el de conversación personal de 1:43:42,
  14; el de precaución de 0:40:20, 9 en A y 11 en B.

La sección completa del punto 4 (clase, commit y fecha de cada tramo, y lecturas posteriores) espera a
que el consultor decida sobre la parada.

## Segunda respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Segunda respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. P2: B no se instala en esta rama. A se queda donde la has restaurado, y las B siguen apartadas como *.filtrada-B-condicion.md, sin abrir.
>    Por qué: una parada no se relaja después de ver el resultado. B no empeora nada frente a ANTES (P3 = 0), pero sí frente a A en 6 segmentos de tramos de precaución, y la rama Q rehará las filtradas en todo caso, ya con los tramos aplicados. Instalar B ahora no aporta nada.
>    El alcance de esta rama queda así: medir B (hecho), arreglar los tramos y documentar el hueco. Declara este cambio de alcance como desviación aceptada por el consultor.
>
> 2. Tramos, por su régimen (solo añadir, sin editar los que ya existen):
>    a) v10, bloque de 1:55:27: tramo nuevo con inicio al segundo y un segundo de margen al final, el criterio de los 12 de v10, y con el motivo de precaución de siempre. Tiene que pasar tu control positivo: el bloque de B cabe entero dentro del tramo.
>    b) v9: un tramo nuevo por cada uno de los 8 bloques. Cubre el bloque entero con un segundo de margen al final, y el motivo dice que completa el tramo original (nombra cuál), porque ese se registró sin margen. Control positivo igual.
>    Por qué: con el final sin margen, la cola del último segundo de cada bloque queda fuera de su tramo, y los tramos son los que respeta la guardia.
>    Parada: si algún ev-* cae en los segundos que cubren los tramos nuevos, para y dime cuál, sin tocar el ítem.
>    Después: scripts/ficheros_con_ocultos.py, uv run botsito knowledge validate y el test de tramos del repo real, con la rotura a propósito (quitar un tramo nuevo y ver que cae).
>
> 3. Termina la sección del hueco (punto 4 de mi respuesta anterior) con las 10 sesiones de tramos que haya en v7–v10: clase, commit y fecha de entrada, líneas visibles dentro en A y en B, y las lecturas de cada filtrada que constan en los informes después de esa fecha. Sin texto. Lo que encuentres sobre lecturas de tramos de precaución me lo pasas, y yo decido si va a HOLDOUT-EXPOSICIONES.md.
>
> 4. Recuadros en los dos informes cerrados:
>    - CUARENTENA-POR-CONDICION.md §5 decía que en v9 «ya NO sale f7529459…». Sí sale: B es idéntica a ANTES. El recuadro lo corrige y remite al informe nuevo.
>    - SESION-04-EXTRACCION.md §1.2: la comparación pendiente queda hecha (v9 da f7529459…a027b), con remisión al informe nuevo.
>
> 5. El punto Q de la Next Action se sustituye por este texto (va en el commit de la rama, para que entre con el merge):
>    «Q. Rama corta: que las filtradas de sesión apliquen los tramos no citables (scripts/transcribir_sesion.py), con un test sintético que rompa la guardia a propósito. Tras el merge, rehacer con --solo-filtrar las filtradas de v7–v10 en B con los tramos, y comprobar que lo tapado es B más los tramos, y nada destapado frente a A dentro de un tramo (FILTRADAS-ESCENARIO-B.md). Hasta cerrar Q, nadie lee las filtradas de v9 ni de v10, y la activación de la sesión 4 espera.»
>    Y P se quita: pasa a HECHO con esta rama.
>
> 6. Para la fila de ERRORES-RECURRENTES, además del hallazgo de mi respuesta anterior:
>    importa · De Claude Code: la comparación por bloques marcaba destapados falsos porque las marcas truncan al segundo, y el criterio de los tramos de v9 (sin margen) era distinto del de v10. Lección: toda comparación de marcas con segundos truncados se valida contra un caso idéntico conocido (aquí, v9 B = ANTES), y los criterios de registro de tramos se fijan por escrito en un solo sitio.
>    Dime dónde está hoy escrito el criterio de registro de tramos. Si no lo está, añádelo al runbook que corresponda en esta rama.
>
> Lo demás del encargo sigue igual: make check sellado, push como fix/filtradas-escenario-b con la CI de Linux y sus números de run (único fallo aceptado: state check por el nombre fix/), revisor con su informe pegado al final, y el tamaño de PROJECT_STATE.
>
> Rama lista para revisión, NO cerrada.

## 2. Los tramos nuevos (segunda respuesta, punto 2): la parada salta

### 2.1 El criterio, que no estaba escrito (punto 6)

**El criterio de registro de tramos no estaba escrito en ningún sitio.**
- La skill `ingerir-sesion` (paso 4) solo dice que los bloques entran «con `motivo` y `acordado`, SIN
  contenido».
- La cabecera de `tramos_no_citables.yaml` dice «t0, t1 (h:mm:ss del video)».
- Ningún runbook fija el inicio, el final ni el margen. Por eso v9 y v10 se hicieron distinto.

Queda escrito en esta rama en `docs/runbooks/SESION-DE-PREGUNTAS.md`, «Después», punto 4, como
«Los límites de un tramo: el criterio único»:
- bloque de la filtrada: inicio al segundo y final más un segundo;
- segmento del `Filtro`: sus milisegundos;
- corte de audio: inicio por abajo y final por arriba;
- control positivo de cada tramo nuevo;
- SOLO AÑADIR, completando con un tramo nuevo que nombra al original.

### 2.2 Los nueve tramos calculados, y la parada

Anexo: `docs/validation/anexos/FILTRADAS-ESCENARIO-B/tramos_nuevos.py`, con la salida en
`tramos_nuevos-SALIDA.txt`. Solo lee marcas `[CUARENTENA …]` y tiempos.

Los nueve tramos son estos: ocho de v9, cada uno completando al original de la sesión 3, y uno de
v10, el bloque de B de 1:55:27. **Los nueve pasan el control positivo**: el bloque de B cabe entero
en el tramo nuevo.

| Vídeo | Tramo nuevo | Completa a | Ítems en los segundos nuevos |
|---|---|---|---|
| v9 | 0:22:11–0:22:17 | 0:22:11–0:22:16 | 0 |
| v9 | 0:24:11–0:24:24 | 0:24:11–0:24:23 | 0 |
| v9 | **0:34:44–0:34:57** | 0:34:44–0:34:56 | **1: `ev-v9-003456-9ef48fb5`** |
| v9 | 1:06:38–1:07:33 | 1:06:38–1:07:32 | 0 |
| v9 | 1:07:34–1:07:40 | 1:07:34–1:07:39 | 0 |
| v9 | 1:07:45–1:07:52 | 1:07:45–1:07:51 | 0 |
| v9 | 1:13:25–1:13:40 | 1:13:25–1:13:39 | 0 |
| v9 | 1:13:55–1:14:05 | 1:13:55–1:14:04 | 0 |
| v10 | 1:55:27–1:55:34 | (bloque nuevo de B) | 0 |

**Salta la parada del punto 2.** El ítem `ev-v9-003456-9ef48fb5`:
- va de 0:34:56 a 0:35:00;
- es de tipo RULE_STATEMENT, con el tema `reentrada.sesgo_distinto_sesiones_diferentes` y la nota
  «A-46»;
- entró con `0e3ca88` el 2026-09-29, en la ingesta de la sesión 3.

Empieza en el segundo exacto en que termina el tramo original 0:34:44–0:34:56, y el tramo nuevo, que
llega a 0:34:57, lo pisa. Con la marca truncada al segundo no se puede saber, sin leer la cruda, si
el segmento que cita empieza antes o después de que acabe el último segmento del bloque.

**No se ha tocado el ítem y no se ha registrado ningún tramo**, tampoco los otros ocho. Decide el
consultor.

## Tercera respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Tercera respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Antes de registrar nada, comprueba solo con marcas, sin texto, en la filtrada ANTES de v9 (o en la A):
>    a) que el bloque [CUARENTENA …] que completa este tramo termina en la marca 0:34:56;
>    b) que la línea siguiente es visible y lleva la marca 0:34:56;
>    c) que el ancla de ev-v9-003456-9ef48fb5 es esa línea visible y no un segmento de dentro del bloque.
>    Si alguna de las tres falla, para y dímelo sin tocar nada.
>    Por qué: si se cumplen, el segmento oculto termina antes de que empiece el del ítem, porque la transcripción no solapa segmentos, y el choque es solo del truncado al segundo.
>
> 2. Si se cumplen las tres: el tramo nuevo que completa el de 0:34:44 va de 2.084.000 a 2.096.000 ms, es decir, termina en el inicio del ítem. Su motivo nombra el tramo original y el ítem. El ítem no se toca.
>
> 3. El criterio de docs/runbooks/SESION-DE-PREGUNTAS.md («Los límites de un tramo: el criterio único») se completa con esta condición, escrita como regla general y no como caso de v9:
>    «Si el segundo de margen pisa el ancla de un ítem ev-*, el tramo termina en el inicio de ese ítem, siempre que las marcas demuestren que el ítem viene de una línea visible que sigue al bloque. Si no se puede demostrar, se para y decide el consultor.»
>    Añade un test que lo vigile: con un tramo y un ítem sintéticos, el tramo que pisa el ancla de un ítem tiene que fallar en knowledge validate, o en el control que ya tengas. Si hoy ningún control lo detecta, dilo en el informe y queda como requisito de Q, no de esta rama.
>
> 4. El texto de Q en la Next Action (el de mi segunda respuesta) se amplía con esta frase:
>    «La aplicación de un tramo a la filtrada tapa un segmento solo si se solapa con el tramo más de 0 ms: un segmento que empieza exactamente donde termina un tramo queda visible. Test sintético con ese caso de borde (v9, 0:34:56; FILTRADAS-ESCENARIO-B.md).»
>    Por qué: si no, la regla de Q taparía el segmento del ítem y lo dejaría sin ancla.
>
> 5. Sigue con los puntos 3 a 6 de mi segunda respuesta: la sección del hueco, los recuadros, la Next Action, la fila de ERRORES-RECURRENTES, make check sellado, push como fix/filtradas-escenario-b con la CI de Linux y sus números de run, revisor con su informe pegado al final y el tamaño de PROJECT_STATE.
>    Pregunta expresa para el revisor: que compruebe que ningún tramo nuevo pisa el ancla de ningún ítem ev-* y que todos pasan el control positivo.
>
> Rama lista para revisión, NO cerrada.

## 3. La comprobación de la tercera respuesta (punto 1): falla (b), y se para

Anexo: `docs/validation/anexos/FILTRADAS-ESCENARIO-B/ancla_v9.py`, con la salida en
`ancla_v9-SALIDA.txt`. Solo lee la clase de cada línea (bloque, visible, «…», sección) y su marca,
en la filtrada ANTES de v9 y en la A, que dan lo mismo.

Antes, del guion de `main` (`scripts/transcribir_sesion.py`, `version_filtrada`):
- la marca de una línea visible es el `t0` de su segmento;
- las dos marcas de un bloque son el `t0` de su primer segmento y el `t1` del último;
- todas truncadas al segundo.

La filtrada va agrupada por pregunta: solo dentro de una sección, y sin «…» entre medias, la línea
siguiente del fichero es el segmento siguiente de la cruda.

| Comprobación | ANTES | A | Resultado |
|---|---|---|---|
| (a) el bloque termina en la marca 34:56 | línea 611: `[CUARENTENA 34:44–34:56]`, el único | línea 600, igual | **se cumple** |
| (b) la línea siguiente es visible y lleva la marca 34:56 | línea 612: visible, misma sección, sin «…», **marca 34:58** | línea 601, igual | **FALLA: la marca es 34:58** |
| (c) el ancla del ítem es esa línea visible | — | — | **no se puede demostrar con marcas** |

Lo que dicen las marcas, sin texto:
- **El último segmento oculto termina** en algún punto de 0:34:56.000 a 0:34:56.999.
- **El segmento visible siguiente empieza** en 0:34:58 o después. Entre los dos, en la cruda, no hay
  ningún segmento.
- **En la ventana declarada del ítem** (t0 0:34:56, t1 0:35:00) **no empieza ninguna línea visible
  en los segundos 34:56 y 34:57.** Lo único que hay en esos dos segundos es la cola del segmento
  oculto. La primera línea visible empieza dos segundos después del t0 del ítem.
- **La cita del ítem se localiza con 2 s de tolerancia** (`TOLERANCIA_CITA_MS = 2000`), es decir,
  desde 0:34:54, que cae dentro del bloque. Con marcas no se puede saber si sus palabras están en la
  línea de 34:58 o en el segmento oculto.
- **Lo más probable es que el ítem ya solape hoy el bloque.** Su ventana declarada empieza en
  2.096.000 ms y el segmento oculto termina entre 2.096.000 y 2.096.999 ms: se solapan siempre,
  salvo que el segmento termine justo en 2.096.000. `knowledge validate` no lo ve porque ningún
  tramo cubre ese milisegundo.

**No se ha registrado ningún tramo y el ítem no se ha tocado.** Decide el consultor.

## Cuarta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Cuarta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Autorizo medir el ancla de ev-v9-003456-9ef48fb5 con la misma localización de citas que usa uv run botsito knowledge validate. Debe ser la misma función, llamada como la llama validate; nada de una vía paralela.
>    Condiciones:
>    - la salida es solo: índice y milisegundos de inicio y fin de cada segmento en que caen las palabras citadas, y el índice y los milisegundos de fin del último segmento del bloque [CUARENTENA 34:44-34:56];
>    - ni texto, ni palabras, ni longitudes de cita;
>    - el guion va como anexo (ancla_v9.py) con su salida commiteada, y el informe dice qué función llama y que es la de validate.
>    Por qué: es un control ya autorizado y no expone texto. Lo que decide es si el ítem cita la línea visible o el segmento oculto.
>
> 2. Según el resultado:
>    a) Todas las palabras citadas caen en la línea visible (la de 0:34:58 o posteriores): el ítem no pisa la cuarentena, y lo que está mal es solo su ventana declarada.
>       - Tramo nuevo de 2.084.000 a 2.096.000 ms, que completa el de 0:34:44. Pasa validate porque no solapa la ventana del ítem.
>       - Declara en el informe que la cola del segmento oculto, desde 2.096.000 ms hasta su fin real, queda fuera del tramo. La tapará Q, porque ese segmento solapa el tramo más de 0 ms.
>       - El ítem no se toca en esta rama. Su ventana se corrige por su régimen (evidence new --supersede, con t0 en el inicio real del ancla) en una rama aparte. Añade a la Next Action, tras Q:
>         «R. Rama corta: corregir por su régimen la ventana declarada de ev-v9-003456-9ef48fb5 (empieza 2 s antes de su ancla, sobre la cola de un segmento en cuarentena; FILTRADAS-ESCENARIO-B.md §3).»
>    b) Alguna palabra citada cae en el segmento oculto: para. No registres el tramo, no toques el ítem y no declares nada. Dame solo índices y milisegundos, y yo decido la exposición y qué se hace con el ítem.
>    c) La localización falla o es ambigua: para y dime por qué, también sin texto.
>
> 3. Lección para la fila de ERRORES-RECURRENTES (del consultor):
>    importa · El consultor dio por hecho, sin medirlo, que la línea visible empezaba en la marca del fin del bloque. La comprobación (b) lo desmintió. Lección: las hipótesis sobre marcas truncadas se escriben como comprobaciones con parada, nunca como premisa de una decisión.
>
> 4. El criterio de SESION-DE-PREGUNTAS.md: la condición de mi tercera respuesta («el tramo termina en el inicio del ítem…») se cambia por esta, porque la otra se apoyaba en la premisa que ha fallado:
>    «Si el segundo de margen solapa la ventana declarada de un ítem ev-*, se mide el ancla del ítem con la localización de validate, sin texto. Si el ancla está fuera del bloque, el tramo termina en el inicio de la ventana del ítem y la ventana se corrige por su régimen. Si el ancla cae dentro del bloque, se para y decide el consultor.»
>    Test sintético contra tramo_no_citable (verificacion.py:358): un tramo que termina justo en el inicio de la ventana de un ítem pasa, y uno que se mete 1 ms en ella falla.
>
> 5. Lo demás sigue como en mis respuestas segunda y tercera: los puntos 3 a 6, el texto de Q con el solapamiento de más de 0 ms, make check sellado, fix/ con la CI de Linux y sus números de run, y el revisor con la pregunta expresa sobre tramos e ítems.
>
> Rama lista para revisión, NO cerrada.

## 4. El ancla medida (cuarta respuesta), los tramos registrados y el criterio

### 4.1 El ancla de `ev-v9-003456-9ef48fb5`: caso (a)

Anexo: `ancla_v9.py`, función `ancla_validate`, con la salida al final de `ancla_v9-SALIDA.txt`.

**Llama a la función de `knowledge validate`, llamada igual que en validate.**
`src/botsito/validation/knowledge.py`, líneas 668-695, hace esto:
- `cargar_evidencia` de `knowledge/evidence`;
- `cargar_manifiesto` de `knowledge/corpus/manifest.yaml`;
- `construir_contexto(repo, _carpeta_datos(repo), manifiesto)`;
- `verificar_citas(items, contexto)`, con **todos** los ítems.

El anexo hace lo mismo y toma la `Localizacion` del ítem. De los segmentos solo lee `n`, `t0_ms` y
`t1_ms`, por el mismo `contexto.crudas` que usa `verificar_citas` (el llamador autorizado de
`tests/unit/test_cuarentena.py`). No imprime texto, ni palabras, ni longitudes de cita.

| Medida | Valor |
|---|---|
| Ventana declarada del ítem | 2.096.000–2.100.000 ms |
| Problemas de cita del ítem | 0 |
| Apariciones de la cita en la ventana | 1 (no es ambigua) |
| Avisos de tiempos parciales | 0 |
| **Segmento en que caen las palabras citadas** | **n 613, de 2.098.060 a 2.100.240 ms** |
| **Último segmento del bloque `[CUARENTENA 34:44–34:56]`** | **n 612, termina en 2.096.900 ms** |

**El bloque está bien identificado.** En la lista de validate solo un segmento acaba en el segundo
34:56 y va seguido de uno que empieza en 34:58. El bloque ocupa las posiciones 609-612 y los
segmentos n 609-612, y su primer segmento empieza en el segundo 34:44. Coincide con el motivo del
tramo original («segmentos 609-612 de la cruda»).

La cruda de `data/` que lee validate no es byte a byte la del Escritorio, de la que salió la
filtrada: tienen sha256 distinto, `dcd6e5bd…` frente a `d7464d30…`. Por eso el bloque se buscó por
sus marcas y no por su índice. Las dos vías dan 609-612.

**Veredicto: caso (a).** Todas las palabras citadas caen en el segmento visible 613, que empieza
1.160 ms después de que termine el último segmento del bloque. El ítem no pisa la cuarentena: lo que
está mal es solo su ventana declarada, que empieza 2.060 ms antes de su ancla, sobre la cola del
segmento 612.

### 4.2 Lo que se registró (punto 2a de la cuarta respuesta; punto 2 de la segunda)

En `knowledge/corpus/tramos_no_citables.yaml`, solo añadiendo (el diff no quita ninguna línea), hay
**8 tramos nuevos**:

| Vídeo | Tramo nuevo | Completa a / motivo |
|---|---|---|
| v9 | 0:22:11–0:22:17 | 0:22:11–0:22:16 (segmentos 404-406) |
| v9 | 0:24:11–0:24:24 | 0:24:11–0:24:23 (438-441) |
| v9 | 1:06:38–1:07:33 | 1:06:38–1:07:32 (1075-1080) |
| v9 | 1:07:34–1:07:40 | 1:07:34–1:07:39 (1082-1084) |
| v9 | 1:07:45–1:07:52 | 1:07:45–1:07:51 (1088-1090) |
| v9 | 1:13:25–1:13:40 | 1:13:25–1:13:39 (1180-1182) |
| v9 | 1:13:55–1:14:05 | 1:13:55–1:14:04 (1192-1194) |
| v10 | 1:55:27–1:55:34 | precaución: el bloque de B `[CUARENTENA 115:27–115:33]`, que el tramo de 1:55:29–1:55:32 no cubre entero |

**Desviación aceptada por el consultor (quinta respuesta, punto 2): el tramo de 2.084.000 a
2.096.000 ms NO se registra.** Es idéntico al original, `0:34:44`–`0:34:56`, y duplicarlo no tapa
nada.
- **El bloque de 0:34:44 se queda sin el segundo de margen por la condición del ancla** (§4.3): ese
  segundo solapa la ventana declarada de `ev-v9-003456-9ef48fb5`, y el ancla del ítem está fuera del
  bloque (§4.1). Por eso el tramo termina en el inicio de la ventana del ítem, que es donde ya
  termina el original.
- La ventana del ítem se corrige por su régimen en **R** (Next Action).

**Declarado (punto 2a): la cola del segmento oculto 612, de 2.096.000 a 2.096.900 ms, queda fuera de
todo tramo.** La tapará Q, porque el segmento 612 solapa el tramo original más de 0 ms.

**Control positivo, sobre lo ya registrado** (anexo `tramos_registrados.py`, con su salida):
- Cada bloque de B de v9 y de v10, con su final un segundo después de la marca, cabe entero en un
  tramo registrado: 20 de 21.
- El que no cabe es el de 34:44, que se midió con su fin real (2.096.900) y está cubierto hasta
  2.096.000: es la cola declarada.
- **Ningún ítem ev-* de v7–v10 solapa un tramo registrado más de 0 ms** (0 ítems).

**Después** (segunda respuesta, punto 2):
- `uv run python scripts/ficheros_con_ocultos.py`: «OK: .claude/hooks/ficheros_con_ocultos.txt
  coincide». No hay que regenerar nada.
- `uv run botsito knowledge validate`: exit 0 y ningún ERROR, con 501 ítems de evidencia e
  historial intacto.

### 4.3 El criterio y su test (punto 4 de la cuarta respuesta)

En `docs/runbooks/SESION-DE-PREGUNTAS.md`, «Los límites de un tramo: el criterio único», entra la
condición de la cuarta respuesta, que sustituye a la de la tercera: si el segundo de margen solapa la
ventana declarada de un ítem, se mide el ancla con la localización de validate. Si el ancla está
fuera del bloque, el tramo termina en el inicio de la ventana. Si cae dentro, se para.

**El control ya existía.** `tramo_no_citable` (`src/botsito/evidence/verificacion.py:358`) hace que
`knowledge validate` y `evidence new` rechacen un ítem cuya ventana declarada solape un tramo más de
0 ms. El test nuevo es `tests/unit/test_tramos_de_sesion.py`, con 6 funciones:
- **Sintéticos contra `tramo_no_citable`:**
  - un tramo que termina justo en el inicio de la ventana de un ítem pasa;
  - uno que se mete 1 ms en ella falla.
- **El criterio de los límites, sintético:**
  - un tramo de cuarentena de v9 sin margen y sin compañero se nombra;
  - con su compañero, o cuando el segundo de margen pisaría la ventana de un ítem, no.
- **Repo real:**
  - cada tramo de cuarentena de la sesión 03 tiene su compañero con margen, salvo el de 0:34:44, que
    se queda en el inicio de la ventana del ítem;
  - el bloque de v10 de 1:55:27 tiene su tramo;
  - ningún ítem de v7–v10 solapa un tramo.
- **La rotura a propósito, en el test:** quitar en memoria un tramo nuevo del repo real hace que la
  comprobación lo nombre.

**La rotura a propósito, en el fichero** (segunda respuesta, punto 2):
1. Se apuntó el sha256 del yaml, `a7d093cb…`.
2. Se quitó la entrada nueva de 0:22:11–0:22:17.
3. Con eso, `test_los_tramos_de_sesion_del_repo_real` **cae** y nombra `(1331000, 1336000)`, el
   original sin compañero.
4. Se restauró el fichero desde la copia: el sha256 vuelve a ser `a7d093cb…` y pasan los 6 tests.

## 5. El hueco: las filtradas de sesión no aplican los tramos (segunda respuesta, punto 3)

Anexo: `hueco.py`, con la salida en `hueco-SALIDA.txt`, que tiene la tabla entera. No hay texto: solo
la clase de cada tramo (por el comienzo de su motivo), el commit y la fecha en que entró (el primer
commit del fichero de tramos en que aparece), y las líneas visibles cuya marca cae dentro, en la
filtrada A (la instalada) y en la B (apartada).

**Cuántos tramos.** La segunda respuesta habla de «10». En v7–v10 había **35 tramos** antes de esta
rama (v7: 1, v8: 0, v9: 13, v10: 21), y esta rama añade 8, así que son 43. La tabla los da todos.

### 5.1 Clase, entrada y líneas visibles dentro

| Clase | Vídeo: entrada | Tramos | Con líneas visibles dentro (A / B) |
|---|---|---|---|
| cuarentena mecánica | v7: `3718889` (2026-09-27) | 1 | ninguno |
| cuarentena mecánica | v9: `0e3ca88` (2026-09-29) | 8 | 1:07:45 (1 / 1); 1:13:55 (0 / 1) |
| sin audio (cero digital) | v9: `0e3ca88` | 2 | ninguno |
| precaución | v9: `0e3ca88` | 3 | 0:32:20 (2 / 2), 1:13:04 (9 / 12), 1:39:43 (67 / 67) |
| cuarentena mecánica | v10: `cfec50b` (2026-10-04) | 12 | 7 con 1 / 1, todos en el segundo de margen (abajo); 0:00:58 (1 / 1) |
| sin audio (cero digital) | v10: `cfec50b` | 4 | 0:45:05 y 1:39:08, 1 / 1 cada uno, en el segundo de margen |
| precaución | v10: `c489685` (2026-10-04) | 4 | 0:40:20 (9 / 11), 1:27:44 (4 / 4), 1:56:07 (13 / 13); 1:55:29 (0 / 0) |
| conversación personal | v10: `c489685` | 1 | 1:43:42 (14 / 14) |
| completa (margen), esta rama | v9 | 7 | 1:07:45 (1 / 1), 1:13:25 (1 / 1), 1:13:55 (0 / 2) |
| precaución, esta rama | v10 | 1 | 1:55:27 (1 / 1), en el segundo de margen |

### 5.2 Hallazgo para Q: el segundo de margen tapa el segmento siguiente

**En 12 tramos con margen hay una línea visible que empieza en el último segundo del tramo**, el de
margen (`hueco-SALIDA.txt`, «ultimo s»). Hay que separar dos grupos:
- **9 tramos de antes de esta rama:** 7 de cuarentena de v10 (1:03:24, 1:26:34, 1:26:44, 1:55:58,
  1:56:04, 2:06:42 y 2:07:04) y 2 sin audio de v10 (0:45:05 y 1:39:08). En cada uno es la única
  línea visible de dentro.
- **3 tramos de esta rama:** el nuevo de 1:55:27, y los dos completos de v9 de 1:13:25 y 1:13:55,
  que ya caen dentro del tramo de precaución de 1:13:04.

La primera versión de este apartado decía «9» y no sumaba los 3 de esta rama. Esa cifra pasó al
texto de Q (revisor, A2; ver §9).

Por las marcas, esa línea es el segmento que sigue al bloque, visible y citable. Con la regla de Q
(se tapa todo segmento que solape un tramo más de 0 ms), **Q lo taparía**. Pasa lo mismo al principio
(v9 1:07:45, v10 0:00:58, B de v9 1:13:55): una línea visible que empieza en el mismo segundo que el
bloque.

Ningún ítem está afectado: ninguno solapa un tramo (§4.2). Pero el revisor de `trabajo/sesion-04` ya
encontró citas del informe en esos segundos de margen (su A2). Lo que decide el consultor para Q:
- o lo tapado de más se acepta y se dice;
- o Q aplica los tramos de cuarentena mecánica por sus segmentos (los milisegundos reales), y los
  segundos solo a los demás.

**Decidido (quinta respuesta, punto 3): se acepta que Q tape la línea visible que cae en el segundo
de margen de esos 9 tramos.** Tapar de más no expone nada, y ningún ítem tiene su ventana ahí, porque
`tramo_no_citable` lo impide. La frase entra en el texto de Q de la Next Action.

### 5.3 Lecturas de las filtradas en los informes, después de la entrada de cada tramo

Se buscó en `docs/validation/` cada mención de una lectura de la filtrada de v7, v9 o v10, y las
marcas que caen en los tramos de precaución de v9. Resultado:

- **v7** (tramo del 2026-09-27): su único tramo no tiene ninguna línea visible dentro. Las lecturas de
  la filtrada de v7 son las de su propia ingesta (`SESION-02-VIDEO.md`, el mismo día).
- **v9** (tramos del 2026-09-29, `0e3ca88`):
  - Después de esa fecha no consta ninguna lectura de líneas dentro de sus tramos de precaución.
  - Lo que aparece son marcas sueltas, en `CUARENTENA-POR-CONDICION/medir_fase2-SALIDA.txt` y en esta
    rama, y menciones de los rangos de los tramos (`CERRAR-A29-A36.md`).
  - La lectura con máscara de los segmentos 1075-1080 la ordenó el consultor ese mismo día y la
    declara el motivo del tramo.
- **v10** (tramos del 2026-10-04, `cfec50b` y `c489685`): **lecturas de tramos de precaución, para
  el consultor** (no se declaran aquí; decide si van a `HOLDOUT-EXPOSICIONES.md`):
  1. **0:40:20–0:40:42 (precaución, `c489685`).** Después de que entrara el tramo:
     - el revisor de `trabajo/sesion-04` hizo `grep -n` de los patrones de las citas de A1 en la
       filtrada de v10 y los localizó en `[40:25]`, `[40:27]` y `[40:36]` (`SESION-04-EXTRACCION.md`,
       su A1 y su búsqueda 14);
     - el texto citado, con una cifra que la fila de HOLDOUT no declara («SIN cifra»), estaba en el
       informe en el commit `c489685` y se quitó después (A1, arreglado). Sigue en la historia de ese
       commit.
  2. **1:27:44–1:28:19 (precaución, `c489685`).** El informe describía su contenido más allá de lo
     declarado (A6 de aquel revisor, arreglado). La descripción sigue en la historia de `c489685`.
  3. **1:56:07–1:56:19 (precaución, `c489685`).** El cuerpo del commit `c489685` nombra «junio» junto
     a una cifra (A5 de aquel revisor). Se declaró como no reparable, y el consultor decidió entonces.
  4. **Los segundos de margen (cuarentena y sin audio, `cfec50b`).** El informe citaba las líneas de
     86:40, 127:02, 46:40 y 99:41, que caen en el segundo de margen de cuatro tramos (A2 de aquel
     revisor, arreglado). No son de precaución: son el segmento visible que sigue al bloque (§5.2).
- **Esta rama:** de ninguna filtrada se ha leído texto. Solo marcas, recuentos, ids, sha256 y, para
  el ítem de v9, índices y milisegundos de segmentos por la localización de validate.

## 6. Recuadros, Next Action y ERRORES-RECURRENTES

- **Recuadros** (segunda respuesta, punto 4), con fecha y rama, junto al pasaje que corrigen:
  - `CUARENTENA-POR-CONDICION.md` §5: en v9 sí sale `f7529459…a027b`;
  - `SESION-04-EXTRACCION.md` §1.2: la comparación queda hecha.
- **Next Action** (segunda respuesta, punto 5; tercera, punto 4; cuarta, punto 2a):
  - P sale a `docs/state/HISTORIA.md` como «Next Action HECHA · P», con su texto literal.
  - Entran Q, con el texto de la segunda respuesta más la frase del solapamiento de más de 0 ms, y
    R.
  - No había un Q que sustituir: la primera respuesta pedía añadirlo, y no se había hecho. Entra
    ahora con su texto final.
- **ERRORES-RECURRENTES:** la fila de la rama va con los tres hallazgos del consultor (primera
  respuesta, punto 6; segunda, punto 6; cuarta, punto 3) y los del revisor, en el commit que pega su
  informe.

## Quinta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Quinta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Aleks ha hecho a mano el commit y el push a fix/. Cópiala tal cual al encargo y al informe, en un commit nuevo.
>
> 1. Comprueba que el commit que hizo Aleks es el que preparaste: el mensaje es el de msg-tramos.txt, el árbol coincide con el sello 5727c7de… y no se coló ningún fichero más. Comprueba también que fix/filtradas-escenario-b apunta a ese commit. Si algo no cuadra, para.
>
> 2. El tramo de 2.084.000 a 2.096.000 ms no se registra, y aceptamos la desviación.
>    Por qué: es idéntico al original, y duplicarlo no tapa nada. Basta con que el informe explique que ese tramo se queda sin margen por la condición del ancla, nombrando ev-v9-003456-9ef48fb5 y R.
>
> 3. El hallazgo para Q: se acepta que Q tape la línea visible que cae en el segundo de margen de esos 9 tramos.
>    Por qué: tapar de más no expone nada, y ningún ítem tiene su ventana ahí (tramo_no_citable lo garantiza). Aplicar los tramos por los milisegundos reales de los segmentos de cuarentena obligaría a leerlos de la cruda, y eso es otra vía que no hace falta.
>    Añade al texto de Q en la Next Action: «Se acepta que la regla de más de 0 ms tape el segmento visible que cae en el segundo de margen de un tramo (9 casos, FILTRADAS-ESCENARIO-B.md); el informe de Q da su recuento.»
>
> 4. Las tres lecturas de tramos de precaución de v10 durante trabajo/sesion-04 (0:40:20, 1:27:44 y 1:56:07) se declaran hoy en docs/validation/HOLDOUT-EXPOSICIONES.md, como exposición de precaución.
>    - Por cada una: fecha, quién (sesión o revisor), qué se vio por su clase (un grep, una descripción, una cifra en el cuerpo de c489685) y dónde queda (historia de git, inmutable). Sin copiar el contenido en ningún sitio nuevo.
>    - Sigue el procedimiento de knowledge/cases/holdout/README.md para una exposición. Con casos_ocultos y casos_reservados, sin abrir nada, dime si el mes al que apunta cada tramo tiene días en alguna partición reservada o en el universo de marzo. Si los tiene, para antes de marcar nada y dame los recuentos (no las fechas). Yo decido si algo queda quemado.
>    - No se reescribe la historia de git ni se toca c489685.
>    Por qué: un tramo de precaución existe porque su texto puede tocar un mes con días ocultos, y lo leído ya no se puede deshacer, pero sí declarar.
>
> 5. Sigue: CI de Linux sobre el commit de Aleks y sobre el nuevo, con sus números de run (único fallo aceptado: state check por el nombre fix/). Si el push del commit nuevo vuelve a bloquearse, para y dame los comandos con «!», como esta vez. Después, el revisor con su informe pegado al final, más dos preguntas expresas: (a) que ningún tramo nuevo pise la ventana de ningún ítem y que todos pasen el control positivo; (b) que la declaración del punto 4 no copie contenido de los tramos.
>    La fila de ERRORES-RECURRENTES lleva los hallazgos de mis respuestas segunda, tercera y cuarta.
>
> Rama lista para revisión, NO cerrada.

## 7. La quinta respuesta: el commit de Aleks, y la parada del punto 4

### 7.1 El commit de Aleks (punto 1): cuadra

La primera vez que se comprobó, el commit y el push no estaban en este repositorio: `HEAD` seguía en
`ffc518d` y `origin` no tenía `fix/filtradas-escenario-b`. Se paró. Aleks los ejecutó después en la
sesión, con `!`:
- **Commit `f50b680`:** su mensaje es el de `msg-tramos.txt` (la única diferencia es la línea en
  blanco final de `git log`), su árbol es `5727c7de…`, el del sello, y trae los 15 ficheros
  estadiados, ninguno más. El árbol de trabajo quedó limpio.
- **`fix/filtradas-escenario-b`** en `origin` apunta a `f50b680`, igual que `HEAD`.
- **CI de Linux de `f50b680`:** run **211** (`37259081415`), `failure` por 1 fallo, el único
  aceptado: `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (state check, por el nombre
  `fix/`). Además, 1977 passed y 8 skipped, que con el fallo suman los 1986 de `make check`.

### 7.2 Punto 2 y punto 3

Hechos: el §4.2 explica que el tramo de 0:34:44 se queda sin margen por la condición del ancla,
nombrando el ítem y R; el §5.2 recoge la decisión sobre Q, y la frase entra en Q.

### 7.3 Punto 4: PARADA antes de marcar nada

Anexo: `meses_de_los_tramos.py`, con su salida. Usa `casos_ocultos`, `casos_reservados` y
`cargar_meses_reservados` (`botsito.cases.holdout`) y no abre nada. Solo imprime recuentos de días
por partición, sin fechas ni ids de caso.

El mes de cada tramo sale de su `motivo` y de la fila del 2026-10-04 de `HOLDOUT-EXPOSICIONES.md`.
El año no consta en ninguno, así que se cuentan todos los años.

| Tramo de precaución (v10) | Mes al que apunta | Días en `casos_ocultos` | Días en `casos_reservados` | Meses reservados enteros (universo de marzo) | ¿Tiene? |
|---|---|---|---|---|---|
| 0:40:20–0:40:42 | enero (por el contexto) | ninguno | ninguno | 0 | **no** |
| 1:56:07–1:56:19 | junio (posible exposición) | holdout-1: 2, holdout-2: 4, holdout-3: 5 | los mismos | 0 | **sí** |
| 1:27:44–1:28:19 | ninguno: «un periodo que el audio no identifica» | cualquier mes: fidelidad-1: 10, holdout-1: 8, holdout-2: 8, holdout-3: 8 | los mismos | 2 (2026-02 y 2026-03) | **no se puede descartar** |

**Salta la parada del punto 4.** No se ha escrito nada en `HOLDOUT-EXPOSICIONES.md` y no se ha
marcado nada. Decide el consultor si algo queda quemado:
- junio tiene 11 días reservados, en tres particiones;
- el tramo de 1:27:44 no apunta a ningún mes, así que puede tocar cualquiera de los reservados,
  marzo incluido.

## Sexta respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Sexta respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04). Cópiala tal cual al encargo y al informe.
>
> 1. Las tres lecturas de tramos de precaución de v10 ya estaban declaradas en la fila del 2026-10-04 de HOLDOUT-EXPOSICIONES.md: la de trabajo/sesion-04, con la corrección del consultor sobre junio y el commit c489685. El grep del revisor y la descripción de su A6 son el mismo contenido.
>    Mi punto 4 de la quinta respuesta pedía declararlas de nuevo porque escribí sin leer el fichero. Queda así: no hay exposición nueva.
>
> 2. En HOLDOUT-EXPOSICIONES.md, por su régimen (solo añadir; la fila del 2026-10-04 no se toca), una fila nueva con fecha de hoy y estas columnas:
>    - qué: «Complemento a la fila del 2026-10-04 (v10, sesión 4). Recuento por partición del alcance de sus tres tramos de precaución, sin abrir nada (anexo meses_de_los_tramos.py, FILTRADAS-ESCENARIO-B.md): 0:40:20, enero, sin días reservados; 1:56:07, junio, 11 días (holdout-1: 2, holdout-2: 4, holdout-3: 5); 1:27:44, periodo no identificado, que no se puede descartar en ningún mes reservado (fidelidad-1: 10, holdout-1: 8, holdout-2: 8, holdout-3: 8, y febrero y marzo de 2026 enteros). Las lecturas posteriores (grep y A6 del revisor de trabajo/sesion-04, cuerpo de c489685) son el mismo contenido ya declarado.»
>    - particiones: las que da el recuento.
>    - quién: la sesión autónoma de trabajo/filtradas-escenario-b; la decisión, del consultor.
>    - ¿quema?: «No. Decisión del consultor (2026-10-04): lo visto son agregados sin fecha, un máximo de operaciones en un día y tres valores de R, que no identifican ningún día reservado ni permiten ajustar decisiones a un día concreto. Las cifras siguen excluidas de todo uso, como dice la fila del 2026-10-04, y además: ninguna regla ni parámetro sobre el número de operaciones por día o sobre el R de salida puede tener esas cifras como fuente. F26 cita las dos filas.»
>    No copies las cifras de los tramos en la fila nueva ni en ningún otro fichero nuevo: «un máximo de operaciones en un día» y «tres valores de R» bastan.
>
> 3. Para la fila de ERRORES-RECURRENTES, además de mis hallazgos anteriores:
>    importa · Del consultor: pidió declarar unas lecturas que ya estaban declaradas, porque no leyó HOLDOUT-EXPOSICIONES.md antes de escribir la orden. Lección: antes de ordenar una declaración de exposición, leer la tabla y citar la fila que ya cubre el caso, si la hay.
>
> 4. Sigue: make check sellado, commit, y push a fix/filtradas-escenario-b con la CI de Linux y sus números de run (único fallo aceptado: state check por el nombre fix/). Si el commit o el push se bloquean, para y dame los comandos con «!».
>    Después, el revisor con su informe pegado al final y tres preguntas expresas:
>    (a) ningún tramo nuevo pisa la ventana de ningún ítem, y todos pasan el control positivo;
>    (b) la fila nueva de HOLDOUT-EXPOSICIONES no copia contenido ni cifras de los tramos y no modifica la del 2026-10-04;
>    (c) el texto de Q y de R en la Next Action coincide con mis respuestas.
>    Y la fila de ERRORES-RECURRENTES.
>
> Rama lista para revisión, NO cerrada.

## 8. La sexta respuesta: la parada del §7.3 se resuelve

- **No hay exposición nueva** (punto 1). Las tres lecturas ya estaban declaradas en la fila del
  2026-10-04 de `HOLDOUT-EXPOSICIONES.md` (`trabajo/sesion-04`). El `grep` y el A6 del revisor de
  aquella rama, y el cuerpo de `c489685`, son el mismo contenido.
- **Fila nueva en `HOLDOUT-EXPOSICIONES.md`** (punto 2), debajo de la del 2026-10-04, que no se toca:
  el diff es una línea añadida y ninguna quitada. Lleva los textos de «qué» y «¿quema?» literales de
  la respuesta, y la columna de particiones según el recuento del §7.3.
- **Ninguna cifra de los tramos** en la fila nueva. Al comprobarlo apareció una en el §5.3 de este
  informe: la del cuerpo de `c489685`, la misma que ya declara la fila del 2026-10-04. Se quitó en
  `e2ee6cc`, pero **ya estaba en `f50b680`, empujado a `fix/`**: queda en la historia de la rama, que
  no se reescribe (revisor, A3; para el consultor, §9). Esta frase decía antes «se quitó antes del
  commit», y no era cierto.
- **ERRORES-RECURRENTES:** el hallazgo del punto 3 se suma a los del consultor para la fila de la
  rama.

## 9. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Qué se hizo |
|---|---|---|
| A1 | importa | **Declarado.** `medir_fase0-SALIDA.txt` y `medir_fase1-SALIDA.txt` son instantáneas de sus fases, de antes de los 8 tramos. Leen los tramos del repo, así que hoy dan más. El §0.2 y el §1.1 lo dicen, y no se regeneran. Los otros 5 anexos se reproducen. |
| A2 | importa | **Arreglado en el informe, y para el consultor.** El §5.2 da ahora 12: 9 tramos de antes y 3 de esta rama. El texto de Q dice «9 casos», literal de la quinta respuesta, y no se toca sin su orden. El informe de Q dará el recuento real, como pide la misma frase. |
| A3 | importa | **No se puede arreglar; se declara, para el consultor.** `f50b680`, ya empujado a `fix/`, lleva en el §5.3 del informe la cifra del cuerpo de `c489685` (tramo 1:56:07). `e2ee6cc` la quitó. No se reescribe la historia. Es la misma cifra que ya declara la fila del 2026-10-04, en `main`. El §8 decía «se quitó antes del commit», y está corregido. |
| A4 | importa | **Para el consultor.** El §5.3.1 dice, citando el A1 del revisor de `trabajo/sesion-04`, que el informe de `c489685` traía una cifra del tramo 0:40:20, mientras que la fila del 2026-10-04 lo declara «SIN cifra». La sexta respuesta concluye «mismo contenido ya declarado» sin esa salvedad. Medido (§7.3): enero no tiene días ocultos ni reservados. |
| A5 | importa | **Arreglado.** La entrada del informe ya no dice «SOLO la fase 0»: explica cómo se lee el informe. |
| A6 | menor | **Para el consultor.** R remite a «§3», literal de la cuarta respuesta. La medida del ancla está en el §4.1; el §3 es la comprobación por marcas que falló, la que llevó a medirla. No se toca. |
| B1 | importa | **Arreglado.** `PROJECT_STATE.md`: 24.218 bytes en `e2ee6cc`, por debajo del tope de 25.000. El de este commit, en el Estado. |
| B2 | importa | **Declarado.** `test_guardia_claude.py::test_los_tramos_del_repo_real` no cambia y pasa. Fija `tramos_vigilados` de la guardia, que solo vigila tramos de v6, porque desde v7 la cruda de una sesión no se lee entera. Los tramos nuevos son de v9 y v10. El test del repo real que los incluye, con su rotura a propósito, es el nuevo `tests/unit/test_tramos_de_sesion.py` (§4.3). |
| B3 | menor | **Arreglado.** La columna «qué» de la fila nueva de `HOLDOUT-EXPOSICIONES.md` es ahora literal, sin negritas ni rama; la rama consta en «quién». La fila sigue siendo +1 frente a `main`. |
| B4 | menor | **Declarado.** F1.3 («marcas de B = tabla de B de la fase 0»): la fase 0 no podía producir B sin escribir (§0.3). Por eso las marcas de B se compararon con ANTES y con A, en las paradas P1-P3 (§1.2). |
| B5 | menor | **Arreglado.** Los sellos, los picos y la CI de cada commit, en el Estado. |

## Séptima respuesta del consultor (2026-10-04)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Séptima respuesta del consultor a trabajo/filtradas-escenario-b (2026-10-04), sobre los hallazgos del revisor. Cópiala tal cual al encargo y al informe.
>
> 1. A2: en el texto de Q de la Next Action, «9 casos» pasa a «12 casos (9 de tramos anteriores y 3 de esta rama)».
>    Por qué: el 9 lo copió el consultor de un recuento parcial; el informe ya dice 12.
>
> 2. A3 y A4: una fila más en HOLDOUT-EXPOSICIONES.md, solo añadir, sin tocar ni la del 2026-10-04 ni la de esta rama. Fecha de hoy y estas columnas:
>    - qué: «Dos rastros más de tramos de precaución de v10, sin copiar su contenido. (1) El informe del commit f50b680 (rama trabajo/filtradas-escenario-b, empujado a fix/) copió la cifra del tramo 1:56:07; la quitó e2ee6cc, pero queda en la historia de la rama y entrará en main con el merge. Es la cifra ya declarada en la fila del 2026-10-04. (2) La fila del 2026-10-04 dice que el tramo 0:40:20 fue visto sin cifra, pero el informe de c489685 copió una (revisor de esta rama, A4).»
>    - particiones: (1) las de junio, ya contadas en la fila anterior de esta rama; (2) ninguna, porque enero no tiene días ocultos ni reservados.
>    - quién: la sesión autónoma de esta rama y la de trabajo/sesion-04; lo detectó el revisor de esta rama.
>    - ¿quema?: «No. Decisión del consultor (2026-10-04): (1) es la misma cifra ya declarada y excluida de todo uso; (2) enero no tiene días reservados. La historia de git no se reescribe.»
>    Sin cifras en la fila.
>
> 3. A6: en el texto de R de la Next Action, «FILTRADAS-ESCENARIO-B.md §3» pasa a «FILTRADAS-ESCENARIO-B.md §4.1».
>
> 4. Para la fila de ERRORES-RECURRENTES, hallazgo de la sesión (lo detectó el revisor):
>    importa · Una cifra de un tramo de precaución se coló en un informe commiteado y empujado, aunque la regla era no copiar contenido de los tramos. Lección: antes de commitear un informe que habla de tramos de precaución, buscar en el diff las cifras y palabras del motivo de cada tramo; el revisor lo comprueba en cada pasada.
>    Del consultor, sin hallazgos que el revisor no viera. Los dos de A2 y A6 son errores de redacción del consultor; anótalos así.
>
> 5. make check sellado, commit, push a fix/filtradas-escenario-b y CI de Linux con su número de run (único fallo aceptado: state check por el nombre fix/). Si el commit o el push se bloquean, para y dame los comandos con «!». No hace falta otro revisor: son cambios de texto que pidió el propio revisor. Cuando termines, dame el sha, el run y el tamaño de PROJECT_STATE.
>
> Rama lista para revisión, NO cerrada.

## 10. La séptima respuesta: los hallazgos del revisor para el consultor, resueltos

- **A2:** Q dice ahora «12 casos (9 de tramos anteriores y 3 de esta rama)».
- **A6:** R remite ahora al «§4.1».
- **A3 y A4:** una fila más en `HOLDOUT-EXPOSICIONES.md`, debajo de la primera de esta rama, con los
  textos de la respuesta y sin cifras. No toca ni la del 2026-10-04 ni la anterior de esta rama:
  frente a `main`, el fichero tiene dos líneas añadidas y ninguna quitada. No quema, por decisión
  del consultor.
- **ERRORES-RECURRENTES:** la fila de la rama lleva el hallazgo de la sesión que vio el revisor (A3,
  con su lección), los cuatro del consultor y sus dos errores de redacción (A2, A6). En «qué se le
  escapó»: nada. Frente a `main` sigue siendo una línea añadida.
- Sin otro revisor, por orden del consultor: son cambios de texto que pidió el propio revisor.

## Estado

**Lista para revisión, NO cerrada.** Hecho, con el alcance que fijó el consultor.

**Desviaciones aceptadas por el consultor:**
- B se midió y no se instaló (parada P2, segunda respuesta, punto 1). A sigue instalada, con su sha
  comprobado, y las B, guardadas sin abrir.
- El tramo de 2.084.000 a 2.096.000 ms no se registra, porque es el original (quinta respuesta,
  punto 2; §4.2).

**Lo hecho:**
- El ancla de `ev-v9-003456-9ef48fb5`, medida con la localización de validate: caso (a) (§4.1).
- 8 tramos nuevos, con su control positivo; `ficheros_con_ocultos`, `knowledge validate`, y el test
  con su rotura a propósito (§4.2-§4.3).
- El criterio de los límites de un tramo, escrito (§2.1, §4.3).
- La sección del hueco, con la decisión sobre el segundo de margen en Q (§5).
- Los recuadros, y P, Q y R en la Next Action (§6, §7.2).
- La fila complementaria de `HOLDOUT-EXPOSICIONES.md`, sin exposición nueva (§7.3, §8).
- El revisor y lo hecho con sus hallazgos (§9, «Informe del revisor»).
- La fila de la rama en `docs/runbooks/ERRORES-RECURRENTES.md`.

**Ninguna exposición en esta rama:** de ninguna filtrada ni cruda se ha leído texto.

**Lo que el revisor dejó para el consultor (§9), resuelto por la séptima respuesta (§10):**
- A2 y A6: corregidos en Q y en R.
- A3 y A4: declarados en una fila más de `HOLDOUT-EXPOSICIONES.md`, sin quemar.

**Sellos y CI** (Linux; el único fallo es el aceptado,
`tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, por el nombre `fix/`):

| Commit | Sello de `make check` | Pico de memoria | CI |
|---|---|---|---|
| `f50b680` | `5727c7de…`, 1986 passed | 288 MiB | run 211 (`37259081415`): 1 failed, 1977 passed, 8 skipped |
| `e2ee6cc` | `4a0ceb23…`, 1986 passed | 290 MiB | run 212 (`37260857834`): 1 failed, 1977 passed, 8 skipped |
| `c4bf89b` | `a87e03e0…`, 1986 passed | 289 MiB | run 213 (`37262859430`): 1 failed, 1977 passed, 8 skipped |

La CI de este commit, el último, va en el mensaje al consultor: un commit no puede llevar su propia
CI.

**`PROJECT_STATE.md`:** 24.294 bytes en este commit (24.218 en `e2ee6cc`), por debajo del tope
de 25.000.

## Informe del revisor

Subagente `revisor` (`.claude/agents/revisor.md`), lanzado con el informe terminado sobre `e2ee6cc`,
con las tres preguntas expresas de la sexta respuesta y cuatro más de la sesión. Pegado tal cual,
salvo las cifras de los tramos de precaución de v10, que se quitan al pegar (sexta respuesta, punto
2: «No copies las cifras de los tramos … en ningún otro fichero nuevo»).

> ## Informe del revisor · trabajo/filtradas-escenario-b · 2026-10-04
>
> Base `f712650`; HEAD `e2ee6cc` (6 commits, árbol limpio). `contrato_rama.py`: «25 ficheros dentro del contrato de trabajo/filtradas-escenario-b (riesgo medio, …, 4 comprobaciones para el revisor)». No se tocan `src/`, `scripts/`, `.claude/`, `knowledge/spec|cases|feedback|evidence`; lo único de `knowledge/` es `tramos_no_citables.yaml` (+56/−0).
>
> Veredicto en una línea: **ningún bloquea**; 5 «importa» de eje (a) y 2 de eje (b), todos de informe, no de mecanismo; respuestas (a)-(g) al final.
>
> ### Eje (a) · Reglas de la casa
>
> Resumen: 0 bloquea, 5 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | La comprobación 1 del contrato (`medir_fase0.py`) y `medir_fase1.py` ya no reproducen su `-SALIDA.txt` commiteada: las SALIDA son instantáneas previas a los 8 tramos añadidos (v9 13→20 tramos, v10 21→22). El informe dice «la salida es idéntica» (§0.2, §1.1c) y su tabla §0.4 cita 13/21 tramos, sin avisar de que es una instantánea previa. | `uv run python …/medir_fase0.py` → `v9: 20 tramos`, `v10: 22 tramos`, `v9 ANTES: 82 lineas en 8 de 20 tramos` frente a la SALIDA commiteada `v9: 13 tramos`, `v10: 21 tramos`, `5 de 13`. `medir_fase1` imprime ahora 8 filas más (0:22:11, 0:24:11, 1:06:38, 1:07:34, 1:07:45, 1:13:25, 1:13:55, 1:55:27). Los otros 5 anexos sí reproducen (solo difiere el EOL; `diff --strip-trailing-cr` = idéntico). |
> | A2 | importa | «9 casos» / «esos 9 tramos» (§5.2, texto de Q en `PROJECT_STATE.md`) no cuadra con el anexo: hay **12** tramos con una línea visible en su último segundo. El propio §5.2 suma 9 + «el nuevo de 1:55:27» + «los dos completos de v9» pero encabeza «9», y Q fija esa cifra en la Next Action. | `grep -c "ultimo s)" hueco-SALIDA.txt` = 12: 10 de v10 (7 cuarentena + 2 sin audio + 1:55:27) y 2 de v9 (1:13:25, 1:13:55). §5.2: «En **9 tramos con margen**… A esos se suman el nuevo de 1:55:27 y los dos completos de v9». |
> | A3 | importa | La cifra reservada del tramo 1:56:07 se copió en un fichero nuevo de la rama en el commit `f50b680`, ya empujado a `fix/` (la 6ª respuesta ordena no copiarla). El árbol de HEAD está limpio (`git diff main` no la contiene), pero queda en la historia de la rama; `e2ee6cc` la quitó y lo dice en su mensaje. Esa cifra ya está en la fila del 2026-10-04 (en `main`). Las demás cifras de esa fila no están en ningún commit. | `git log -S"[retirado al pegar]" main..HEAD` → `e2ee6cc`, `f50b680`. `git show f50b680:docs/validation/FILTRADAS-ESCENARIO-B.md` línea 655: «[retirado al pegar] (A5 de aquel revisor)…». Declarar o decidir; no se reescribe historia. |
> | A4 | importa | El §5.3.1 sigue afirmando que el informe de `c489685` traía, para el tramo 0:40:20, «una cifra que la fila de HOLDOUT no declara («SIN cifra»)». La fila antigua dice «SIN cifra». El §8 y la 6ª respuesta concluyen «mismo contenido ya declarado / no hay exposición nueva» sin reconciliar esa cifra; la fila nueva da 0:40:20 como enero sin días reservados. No abrí el texto de A1 de aquel informe. | `FILTRADAS-ESCENARIO-B.md:656-658` frente a la fila antigua de `HOLDOUT-EXPOSICIONES.md` («comentados SIN cifra»). Pasárselo al consultor expresamente. |
> | A5 | importa | La entrada del informe sigue diciendo «Esta entrega es SOLO la fase 0, y se para en ella… No se ha escrito ninguna filtrada ni ningún tramo, y no se ha leído ningún texto»: falso en el estado final (se escribieron las B y hay 8 tramos nuevos). Contradice el §1 y el «## Estado». | `FILTRADAS-ESCENARIO-B.md:7-9`. |
> | A6 | menor | R en la Next Action remite a «FILTRADAS-ESCENARIO-B.md §3»; el texto es literal de la 4ª respuesta, pero la medida del ancla está en §4.1 (el §3 es la comprobación por marcas que falló). | `PROJECT_STATE.md` punto R; el §3 del informe es «La comprobación de la tercera respuesta». |
>
> Comprobado sin hallazgos:
> - Contrato: comprobaciones 2 y 3 en verde (`ficheros_con_ocultos.py`: «OK: .claude/hooks/ficheros_con_ocultos.txt coincide»; `knowledge validate`: exit sin ERROR, 501 ítems, historial intacto). Los 25 ficheros están en `rutas_permitidas`; ninguna ruta protegida tocada.
> - `make check`: `make-check.log` con `1986 passed in 829.68s`, `SELLO: … sobre el arbol 4a0ceb232860d6ec2bb1efd67f73b994d04171a8` y `PICO DE MEMORIA … 290 MiB`; ese árbol es `HEAD^{tree}`. El `f50b680` tiene árbol `5727c7de…` (el sello citado) y 15 ficheros. `origin/fix/filtradas-escenario-b` = `e2ee6cc` (`ls-remote`).
> - CI de Linux: run 211 (`37259081415`, `f50b680`) y run 212 (`37260857834`, `e2ee6cc`, ya terminada) — ambos `failure` con un único fallo, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (`1 failed, 1977 passed, 8 skipped`).
> - Trailers `Fuente:`: ningún commit toca `knowledge/spec` ni `knowledge/cases`.
> - Regímenes: solo hay `A` en `knowledge/evidence`, `knowledge/feedback`, `data/manifests`, transcripciones y fotogramas; sin cambios en `libros.yaml`. El yaml de tramos: +56/−0. Sin feedback nuevo, ambigüedades, ADR ni las tres guardias de `cita`.
> - Parámetros y test_adr: no se tocan cifras de parámetros ni ADR.
> - Informes cerrados: `CUARENTENA-POR-CONDICION.md` (+9/−0) y `SESION-04-EXTRACCION.md` (+7/−0), solo recuadros `>` con fecha y rama.
> - HOLDOUT: +1/−0; la fila del 2026-10-04 no cambia.
> - Tests: `test_tramos_de_sesion.py` (6 pasan), `test_project_state.py`, `test_historia.py`, `test_adr.py`, `test_guardia_claude.py -k tramos` (2 pasan) en verde; `state check` OK.
> - Citas del informe contra su fuente: `knowledge.py:668-695` (validate → `verificar_citas`), `verificacion.py:358` (`tramo_no_citable`), §4.1 del ancla frente a `ancla_v9-SALIDA` (613, 2.098.060–2.100.240; 612 termina en 2.096.900; ventana 2.096.000–2.100.000; 2.060 ms y 1.160 ms), §5.1 frente a `hueco-SALIDA` fila a fila, §7.3 frente a `meses_de_los_tramos-SALIDA`, y los motivos «segmentos 404-406 … 1192-1194» frente a los tramos originales en `main`.
> - sha256 en disco (`sha256sum`, sin abrir): las cuatro A restauradas coinciden con el informe; `v9 B` = `v9 ANTES` = `f7529459…a027b`.
>
> ### Eje (b) · Encargo
>
> Resumen: 0 bloquea, 2 importa, 3 menor. Requisitos: 22 hechos (+2 «hecho de otra forma»: R4 declarado, R14 no declarado), 4 parciales, 1 no hecho; R30 (ERRORES-RECURRENTES) pendiente por orden de la 6ª respuesta, no cuenta como fallo.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | main en `f712650` y tag | Hecho | `git merge-base` = `f712650`; cabecera del informe |
> | 2 | Abrir rama: encargo, contrato, Archivo 14 | Hecho | `docs/encargos/…`, `contrato.yaml`, `HISTORIA.md` «# Archivo 14» |
> | 3 | Fase 0.1: rutas y hoja por vídeo | Hecho | §0.1 |
> | 4 | Fase 0.2: tabla B/nuevos/destapados | Hecho de otra forma (declarado: B medido en su sitio, 1ª respuesta) | §0.3, §1.2 |
> | 5 | Caso negativo v8 | Hecho | `medir_fase0-SALIDA`: «CASO NEGATIVO v8: 0 … (esperado 0 y 0)» |
> | 6 | Paradas (las de la 1ª respuesta) | Hecho (P2 salta y se honra) | §1.2-§1.3; B no se instala |
> | 7 | F1.1: A apartadas con sha | Hecho | sha en disco = informe |
> | 8 | F1.2: `--solo-filtrar` tal cual | Hecho | §1.1b (4 comandos) |
> | 9 | F1.3: marcas de B = «tabla de B de la fase 0» | Parcial | La fase 0 nunca produjo tabla de B (§0.3); el informe no concilia esa exigencia. |
> | 10 | F1.4: sha de cada B; v9 frente a `f7529459…` | Hecho | §1.2, verificado en disco |
> | 11 | F1.5: tramos nuevos por su régimen | Hecho | 8 tramos (7 de v9 + v10 1:55:27); el de 2.084.000–2.096.000 no se registra (5ª), declarado en §4.2 y Estado |
> | 12 | `ficheros_con_ocultos` + `knowledge validate` | Hecho | ejecutados, OK |
> | 13 | `test_guardia_claude.py::test_los_tramos_del_repo_real` | Parcial | no se menciona en el informe; pasa sin cambios, pero su lista (`tramos_vigilados`) solo tiene v6, así que no incluye los tramos nuevos |
> | 14 | Test de la lista de tramos del repo real + rotura a propósito | Hecho de otra forma, **no declarado** | se creó `tests/unit/test_tramos_de_sesion.py`; rotura hecha en el fichero (§4.3) y en memoria; el informe no explica por qué no se amplió el test de la guardia |
> | 15 | Informe: fase 0, tablas, sha, tramos, desviaciones | Hecho | §0-§5, Estado |
> | 16 | Informe: tamaño de `PROJECT_STATE.md` (encargo y 2ª, 3ª respuestas) | **No hecho** | no hay «bytes»/«KB» en el informe. Medido aquí: 24.218 B |
> | 17 | Anexo reproducible, commiteado, sin texto | Parcial | ver A1: dos SALIDA ya no se reproducen, sin aviso |
> | 18 | Recuadros en los dos informes cerrados | Hecho | solo líneas añadidas, en `>` |
> | 19 | Exposición ninguna | Hecho | de ninguna filtrada se leyó texto |
> | 20 | `make check` sellado | Hecho | sello = `HEAD^{tree}`; el informe no lo cita (menor) |
> | 21 | Push a `fix/` y CI con números de run | Parcial | run 211 en el informe; el 212 (`e2ee6cc`, terminado, mismo único fallo) aún no |
> | 22 | 2ª.1 desviación «B no se instala» declarada | Hecho | Estado |
> | 23 | 2ª.2 tramos v10 1:55:27 y v9; parada ev-* | Hecho | §2.2 (salta y se para), §4.2 |
> | 24 | 2ª.3 sección del hueco | Hecho | §5 (43 tramos, no «10»; explicado) |
> | 25 | Next Action: P → HISTORIA, Q, R | Hecho | ver (c) |
> | 26 | 2ª.6 criterio escrito + 4ª.4 test | Hecho | `SESION-DE-PREGUNTAS.md` +24/−0; 2 tests sintéticos contra `tramo_no_citable` |
> | 27 | 3ª.1 y 4ª.1: ancla con la función de validate | Hecho | `ancla_v9.py`; (b) falla y se para; luego caso (a) |
> | 28 | 5ª.1 commit de Aleks = el preparado | Hecho | árbol `5727c7de…`, 15 ficheros |
> | 29 | 6ª.2 fila de HOLDOUT | Hecho (casi literal) | ver menor B3 |
> | 30 | ERRORES-RECURRENTES | Pendiente por orden | — |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | El encargo (y las respuestas 2ª y 3ª) piden el tamaño de `PROJECT_STATE.md` en el informe; no está. | Grep «bytes\|KB\|tamaño» en el informe: solo citas del encargo. 24.218 B < 25.000. |
> | B2 | importa | El encargo pide que el test de la lista de tramos del repo real los incluya y correr `test_guardia_claude.py::test_los_tramos_del_repo_real`. La rama hizo otra cosa (test nuevo) sin declararlo ni explicar por qué el de la guardia no cambia (su lista es solo v6). | Requisitos 13-14. |
> | B3 | menor | La columna «qué» de la fila nueva no es literal de la 6ª respuesta: añade negritas y «, rama `trabajo/filtradas-escenario-b`». «Particiones» y «quién» también llevan texto añadido (estos dos no tenían texto literal exigido). | `git diff main -- docs/validation/HOLDOUT-EXPOSICIONES.md` |
> | B4 | menor | F1.3 (marcas de B = tabla de B de la fase 0) sin conciliar (requisito 9). | — |
> | B5 | menor | El informe no cita aún el run 212, el sello de `make check` ni el pico (`PICO DE MEMORIA` 290 MiB). | — |
>
> Lo que la rama hace y el encargo no pide: nada fuera de encargo (el test nuevo es el sustituto de B2; la fila de HOLDOUT y los tramos v9 los piden la 2ª/6ª respuesta); los ficheros caen dentro de `rutas_permitidas`.
>
> Lo que el encargo dice que no se toca (motor, spec, regla de cuarentena, `meses_reservados.yaml`, guion): sin cambios en el diff.
>
> ### Respuestas a las preguntas expresas
>
> **(a) Tramos nuevos, ventanas de ítems y control positivo: sí, con la excepción declarada.**
> - 8 tramos (7 de v9, 1 de v10); el diff solo añade. Límites por tramo coherentes con el control positivo de las SALIDA (p. ej. 1:55:27–1:55:34 = 6.927.000–6.934.000 ms).
> - Comprobación propia, independiente, sobre el yaml (47 tramos) y todos los ítems de v7 (5), v8 (2), v9 (62) y v10 (64), con `solape = a_t0 < t_fin y t_ini < a_t1`: **0 ítems solapan ningún tramo** (ni nuevos ni viejos). `tramos_registrados` también: `items … que solapan un tramo mas de 0 ms: 0 []`; `test_ningun_item_de_las_sesiones_solapa_un_tramo` pasa.
> - Control positivo: 20 de 21 bloques de B «cabe». El que no: v9 34:44 (`2084000-2096900: NO CABE (cubierto hasta 2096000)`), la excepción declarada, con su cola 2.096.000–2.096.900 ms. Esa cola cae sobre la ventana del ítem `ev-v9-003456-9ef48fb5` (2.096.000–2.100.000) y no está en ningún tramo; el ancla está en el segmento 613 (2.098.060–2.100.240), fuera del bloque.
> - El tramo 2.084.000–2.096.000 **no** se registró (ninguno de los 8 empieza en 0:34:44; el diff es solo de añadidos).
>
> **(b) Fila nueva de HOLDOUT: sin copia de contenido ni cifras, con una salvedad.**
> - La fila nueva solo lleva conteos de días por partición y los literales «un máximo de operaciones en un día» y «tres valores de R». La fila antigua del 2026-10-04 tiene +1/−0 de diff, es decir, no cambia.
> - Cifras prohibidas (las de la fila antigua: [retirado al pegar: las cifras de los tramos 1:27:44 y 1:56:07 y la frase del tramo 0:40:20]): con `git diff main` no aparecen en ninguna línea añadida (las únicas coincidencias son un número de sección de otro documento, en el Archivo 14 de HISTORIA, que no es esa cifra), ni en los mensajes de los 6 commits. Salvedad: la cifra de 1:56:07 sí estuvo en `f50b680` (ver A3).
> - «qué» y «¿quema?» literales de la 6ª respuesta salvo lo de B3.
>
> **(c) Next Action: Q, R y P coinciden.**
> - Q = texto de la 2ª respuesta + frase de la 3ª + frase de la 5ª; R = texto de la 4ª. Comparé cada frase con las respuestas, línea por línea: coinciden.
> - P: «Next Action HECHA · P» en `HISTORIA.md` línea 4078, con texto literal (sha256 de la línea de `main` = el de la copia, `c3ab0df2…`); en `PROJECT_STATE.md` ya no hay rastro de P (el diff quita la línea).
>
> **(d) Copia de texto de segmentos o tramos: no encontrada.** Revisé los fragmentos entrecomillados «…» de los ficheros cambiados: son todos citas de documentos o plantillas. `ancla_v9.py` solo imprime n, ms y marcas. Los motivos nuevos del yaml solo nombran el tramo original y los índices de segmento ya publicados. La única referencia de contenido es la del A4.
>
> **(e) Numéricas del informe frente a las SALIDA:** coinciden §4.1, §5.1 (fila a fila), §7.3 y §1.2 (B v10 48/13, P2 = 3 + 3). Dos discrepancias: A1 (instantáneas viejas) y A2 (9 frente a 12).
>
> **(f) Recuadros:** `CUARENTENA-POR-CONDICION.md` §5 (+9/−0) y `SESION-04-EXTRACCION.md` §1.2 (+7/−0): solo líneas añadidas, en `>`, con fecha 2026-10-04 y rama; el cuerpo, intacto. Régimen de informes cerrados cumplido.
>
> **(g) `PROJECT_STATE.md`:** 24.218 bytes, 782 por debajo del tope de 25.000 (el test `test_project_state.py` pasa).
>
> ### Lo que no pude comprobar
> - §5.3, ausencia de lecturas posteriores en v9 y v7: me apoyo en el informe; no releí los informes por fecha.
> - El texto de A1 de `SESION-04-EXTRACCION.md`: no lo abrí para evitar cifras, así que el A4 se apoya solo en lo que dice la frase del informe.
> - `git write-tree` y `make check`: no los ejecuté; usé el sello de `make-check.log` (`4a0ceb23…` = `HEAD^{tree}`).
> - La rotura a propósito en el fichero: escribe; no la repetí; la comprobé solo por el test en memoria (`test_la_rotura_a_proposito_cae`, que pasa).
> - El control positivo de los bloques de B: no lo recalculé yo desde las B apartadas sin escribir un guion nuevo que nombre esa carpeta; reproduje los anexos de la rama (que solo leen marcas), y salieron idénticos.
> - ERRORES-RECURRENTES: su fila está pendiente por orden de la 6ª respuesta.
>
> ### Comandos ejecutados
> `git branch/merge-base/log/diff/status`; `uv run python scripts/contrato_rama.py`; `uv run python scripts/ficheros_con_ocultos.py`; `uv run python docs/validation/anexos/FILTRADAS-ESCENARIO-B/{medir_fase0,medir_fase1,tramos_registrados,tramos_nuevos,meses_de_los_tramos,hueco,ancla_v9}.py` (comparados con su SALIDA con `diff --strip-trailing-cr`); `uv run botsito knowledge validate`; `uv run botsito state check`; `uv run pytest tests/unit/test_tramos_de_sesion.py tests/unit/test_project_state.py tests/unit/test_historia.py tests/unit/test_adr.py` y `tests/unit/test_guardia_claude.py -k tramos`; un `uv run python -c` de solo lectura que carga el yaml de tramos y los ítems de v7–v10 para el solape; `git diff main` (varios ficheros), `git show`, `git log -S`, `git rev-parse`, `git ls-remote`; `sha256sum` de las filtradas; `gh run list/view`. Dos bloqueos de hooks, ya esperados: redirección a fichero (`solo_lectura.py`) y una variable `$A` en una ruta (guardia); ambos se corrigieron con rutas literales sin rodear nada.
