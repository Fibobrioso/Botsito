# Las filtradas de sesión en el escenario B

Rama `trabajo/filtradas-escenario-b`, abierta el 2026-10-04 desde `main` en `f712650` (commit de
estado sobre el merge `44f461d`, tag `stable/F36w-cuarentena-por-condicion`). Encargo:
`docs/encargos/trabajo-filtradas-escenario-b.md`. Es el punto P de la Next Action.

**Esta entrega es SOLO la fase 0, y se para en ella**: hay dos cosas del encargo que no se pueden
hacer como están escritas sin rodear la guardia (§0.3), y una parada que saltaría por diseño
(§0.4). No se ha escrito ninguna filtrada ni ningún tramo, y no se ha leído ningún texto.

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
`medir_fase1-SALIDA.txt`. Se reprodujo y la salida es idéntica byte a byte. **Nadie ha abierto
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

## Estado

**PARADA en los tramos (§2.2).** Antes, la fase 1 se paró por P2 (§1.3) y por el punto 2 (§1.4). A está restaurada, con su sha comprobado;
las B, guardadas sin abrir; ningún tramo registrado. **Ninguna exposición.** Esperando al consultor.
Rama NO cerrada.
