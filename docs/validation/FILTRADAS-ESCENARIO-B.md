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

## Estado

FASE 0 ENTREGADA Y PARADA (§0.3 y §0.4): esperando las decisiones del consultor. No se ha escrito
ninguna filtrada ni ningún tramo; **ninguna exposición**. Rama NO cerrada.
