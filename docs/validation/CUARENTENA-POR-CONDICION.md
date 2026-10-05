# La cuarentena por condición: tapar todo mes que no se pueda demostrar libre

Rama `trabajo/cuarentena-por-condicion`, abierta el 2026-10-04 desde `main` en `e98815a` (commit de
estado sobre el merge `eec79a0`, tag `stable/F36v-sesion-04`). Encargo:
`docs/encargos/trabajo-cuarentena-por-condicion.md`. Viene de `SESION-04-EXTRACCION.md` §2.4 y §6
(pendiente a) y es el punto P de la Next Action.

**Esta entrega es SOLO la fase 0**: inventario y medida, sin tocar código. La fase 1 espera la
decisión del consultor sobre la fuente de (b) (§0.1) y sobre los ítems de evidencia (§0.4).

## 0. Fase 0: el inventario

### 0.1 De dónde sale hoy la lista de meses reservados enteros (b)

**No hay una fuente única ni legible por máquina.** Lo que hay, repartido:

| Dónde | Qué dice | ¿La lee el código? |
|---|---|---|
| `src/botsito/corpus/cuarentena.py:218` (`MESES_FILTRADOS`) | septiembre, marzo, mayo y febrero, con sus grafías del ASR | **Sí**: es lo que hoy decide qué mes se tapa en el texto. Mezcla (a), meses con casos, y (b), marzo y febrero, sin decir cuál es cuál |
| `CLAUDE.md:152` | «Marzo de 2026 esta RECIBIDO y SIN ABRIR» | No (prosa) |
| `CLAUDE.md:145-146` | «febrero o marzo vienen detrás» | No (prosa) |
| `PROJECT_STATE.md:58` (pendientes heredados, punto 6) | «FEBRERO NO SE TOCA Y NO SE DESCARGA. Único mes ciego limpio» | No (prosa) |
| `docs/validation/REGISTRO-MARZO.md` | la recepción de marzo, sin abrir | No (prosa) |
| `.claude/hooks/guardia.py:199` (`MESES_DE_DESARROLLO`) | **lista BLANCA** a mano: `2026-01`, `2026-04` y `2026-08` | Sí, pero para los LIBROS (qué xlsx se pueden leer), no para el texto de las transcripciones |
| `knowledge/cases/kit/vistos.yaml:33` | meses que el trader YA vio (2026-01, 04, 05, 07, 08 y 09) | Sí, para el sorteo («¿es ciego?»). No dice qué está reservado |
| `knowledge/cases/kit/config.yaml:55-82` (`cobertura_material`) | qué meses tienen material; `"2026-06": []` (sin material) | Sí, para la ingesta. Tampoco dice qué está reservado |

- **(a) sí tiene fuente única:** `botsito.cases.holdout.casos_ocultos(repo)` (`holdout.py:455`),
  que hoy es el mismo mapa que `casos_reservados(repo)` (`holdout.py:350`). Lo sacan de los
  `particiones.yaml` commiteados de los tres caminos (`repartos_commiteables`), y lanza si uno no se
  puede leer.
- **(b) habría que crearla.** Febrero (ciego, sin descargar) y marzo (recibido, sin abrir) no tienen
  casos, y ningún fichero de datos dice que estén reservados. Tampoco se puede derivar: febrero no
  tiene material en ningún sitio.

**Propuesta** (decide el consultor):
- un fichero nuevo, `knowledge/cases/meses_reservados.yaml`, **SOLO AÑADIR** como `libros.yaml` y
  `retirados.yaml`;
- una entrada por mes reservado entero (`mes: AAAA-MM`, `motivo`, `fuente`, `declarado_el`);
  hoy, `2026-02` y `2026-03`, cada uno citando su fuente;
- lo lee una función de `cases/holdout.py` que **lanza** si el fichero existe y está mal formado, y
  `knowledge validate` lo vigila como a `retirados.yaml`.

Sin ese fichero, la condición (c) no se puede cumplir para ningún mes, y la regla tapa los 12.

**Una consecuencia que hay que saber.** Una vez escrito, ese fichero ES una lista de meses escrita a
mano. Pero solo AÑADE meses tapados: quitar una entrada no se puede (solo añadir), y un mes fuera de
él solo queda libre si además no tiene casos. Es la fuente de (b) que pide el encargo, no una lista
de meses vigilados.

### 0.2 Quién construye el filtro y cómo le llegan los días

**La regla del mes es pura.** `motivos_cuarentena` y `en_cuarentena` (`cuarentena.py:252` y `268`)
solo miran el texto, con las constantes del módulo (`MESES_FILTRADOS`, `_RE_MES`, `_RE_ABREV`). No
leen el repositorio.

**`Filtro`** (`cuarentena.py`, `@dataclass Filtro`):
- usa esa regla para el motivo (c);
- lleva los tramos no citables, que lee `cargar_tramos_no_citables(repo)` desde
  `filtros(repo)` y `filtro_de(repo, v)`;
- los días (`dias: frozenset[(mes, día)]`) **no los lee él: se los pasa quien lo construye**,
  porque `corpus` no puede importar `cases`. Las capas de import-linter son `… cases -> spec ->
  retrieval -> … corpus …`.

**Quién le pasa los días hoy:**
- `cli.py:1306` (`dias_de_casos(casos_ocultos(repo))`) → `retrieval/indice.py:279` y `:299`;
- los anexos de `CUARENTENA-POR-DEFECTO`.

**Quién usa la regla sin días ni repo:**
- `Filtro.motivos` (todas las vías de la CLI);
- `scripts/transcribir_sesion.py:234` (`en_cuarentena`);
- `cuarentena.propuestas_con_ocultos` (dentro de `corpus`, sin acceso a `cases`);
- `scripts/ficheros_con_ocultos.py` (la lista de la guardia).

**Propuesta de por dónde entra la condición.** La condición entra igual que los días, sin que
`domain/` ni el filtro lean el repo:
1. **En `cases/holdout.py`, una función nueva** (p. ej. `meses_libres(repo) -> frozenset[int]`).
   Junta (a), los meses de `casos_ocultos | casos_reservados` en cualquier año, y (b),
   `meses_reservados.yaml`. Devuelve los números de mes DEMOSTRADOS libres. Si algo no se puede
   leer, lanza; no devuelve un conjunto parcial.
2. **En `corpus/cuarentena.py`, la regla recibe `libres: frozenset[int] | None`.** Con `None` (nadie
   le dio los datos), tapa los 12 meses. Es el criterio 2 de la fase 1: ningún valor por defecto deja
   un mes a la vista. `Filtro` gana el campo `libres` igual que tiene `dias`. `en_cuarentena(textos,
   libres=None)` y `motivos_cuarentena(texto, libres=None)` también.
3. **`MESES_FILTRADOS` deja de ser una lista de meses vigilados.** Pasa a ser un diccionario de
   grafías por mes, con las 12 claves: las grafías del ASR de hoy para septiembre, marzo, mayo y
   febrero, y para cada mes su nombre en español, en inglés y su abreviatura. El patrón se compila
   con los meses NO libres.
4. **Los llamadores que hoy construyen el filtro con días le pasan también `libres`:**
   - `cli.py:1306` y `retrieval/indice.py`;
   - `scripts/transcribir_sesion.py` y `scripts/ficheros_con_ocultos.py`, que pueden importar
     `cases`.

   Los que no, como `propuestas_con_ocultos` dentro de `corpus`, quedan con `None` y tapan todo,
   salvo que se les pase.

### 0.3 Todos los sitios que usan `MESES_FILTRADOS`, `_RE_MES` o `_RE_ABREV`

| Sitio | Uso |
|---|---|
| `src/botsito/corpus/cuarentena.py:218-243` | la definición: `MESES_FILTRADOS`, `_RE_MES`, `_RE_ABREV` (las abreviaturas sep, sept, set, mar, may y feb, solo junto a «backtest») |
| `src/botsito/corpus/cuarentena.py:257` y `263` | `motivos_cuarentena`: motivo «mes» y «backtest con mes» |
| `scripts/transcribir_sesion.py:23-29` | el docstring nombra los cuatro meses y «Abril, agosto y enero no se filtran»: prosa que pasa a ser falsa |
| `tests/unit/test_transcribir_sesion.py:40-127` | los tests de grafías (meses filtrados con sus grafías, «abril, agosto, enero y el lenguaje normal no se filtran», backtest con abreviatura, vecinos). **El de «abril, agosto, enero no se filtran» depende de la lista**: con la regla nueva sigue valiendo solo si esos meses son libres en el repo, o en el repo temporal del test |
| `tests/unit/test_cuarentena.py:83` y `135` | `motivos_cuarentena` sobre textos sin mes |
| `knowledge/corpus/tramos_no_citables.yaml:283-285` | el motivo y el acuerdo del tramo manual de v10 1:55:29 nombran `MESES_FILTRADOS` (prosa; el tramo se queda como está) |
| `docs/validation/CUARENTENA-POR-DEFECTO.md:20`, `57`, `89` | prosa, informe cerrado (no se edita) |
| `docs/validation/SESION-04-EXTRACCION.md:265-274`, `978`, `1081`, `1152-1153` | prosa, informe cerrado |

**La verificación de citas no los usa.** `evidence/verificacion.py` comprueba las citas contra la
cruda (`crudo=True`, autorizado) y contra los tramos no citables, no contra la regla del mes. Y la
evidencia, por la sexta orden del 2026-10-01 (`cuarentena.evidencia_a_ocultar`), solo se oculta por
(b) tramo o por una FECHA de `casos_ocultos`, **nunca por la regla del mes (c)**.

**Otras listas de meses a mano, que no deciden qué se tapa en el texto pero que el revisor debe
ver:**
- `.claude/hooks/guardia.py:199` (`MESES_DE_DESARROLLO`, lista blanca de libros legibles) y su
  diccionario de nombres `:223-236`.
- `src/botsito/cli.py:2637`, que acota los meses de construcción.
- Los guiones de medida (`scripts/caja_77.py:33`, `embudo_77.py:416`, `viabilidad_trader.py:236`,
  `viabilidad_comision.py:262`, `sesgo_h4_diagnostico.py:26`), que acotan qué velas leen
  (`2026-04` y `2026-08`).
- `cuarentena.py:316` (`_MESES_NUM`, nombre → número, para `fechas_en`): no decide qué se tapa,
  convierte.

### 0.4 La regla nueva medida sin aplicarla, de v1 a v10

Guion: `docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase0.py`, con la salida en
`medir_fase0-SALIDA.txt`. Se volvió a ejecutar en `ad4fd75` y la salida salió idéntica byte a
byte. **Solo imprime recuentos, marcas de tiempo e ids, nunca texto ni qué mes.**

> **Corrección (2026-10-04, tras el revisor, A1):** desde la fase 1 este guion ya **no corre**.
> Importa `_RE_MES`, que la fase 1 eliminó, y sus entradas (las filtradas de v9 y v10) se rehicieron
> en la fase 2. Queda como la medida que fue, marcado HISTÓRICO en su cabecera. El contrato ya no lo
> lleva como comprobación; lleva `medir_fase2.py`, que es la medida de después y sí se reproduce.

- **Qué se mide:** los segmentos que la regla nueva taparía y que hoy se enseñan, con su vecino
  anterior y siguiente como la regla de hoy, y los ítems `ev-*` cuyo intervalo pisa alguno.
- **v1 a v6:** los segmentos VISIBLES de la transcripción ACTIVA (la que no reemplaza otra
  transcripción), leídos con `cargar_cruda` y su `Filtro`.
- **v9 y v10:** sus versiones filtradas, fuera del repo, quitando lo que cae en un tramo.
- **Grafías nuevas:** nombre en español y en inglés, y abreviatura española de tres letras como
  palabra suelta. `set` queda solo junto a «backtest», como hoy. Con `set` suelto, un primer intento
  daba 3 segmentos «nuevos» en v1 que eran la palabra «set», no un mes: se corrigió antes de medir.

**Dos escenarios.** Hoy no hay fuente para (b), así que la regla tal cual está es el escenario A:

| Vídeo | A: tapa los 12 meses (sin fuente de (b)) | B: con `meses_reservados.yaml` (2026-02 y 2026-03) |
|---|---|---|
| v1 | 0 segmentos, 0 ítems | 0 segmentos, 0 ítems |
| v2 | 0, 0 | 0, 0 |
| v3 | 16 segmentos, 3 ítems | 0, 0 |
| v4 | 6 segmentos, 1 ítem | 0, 0 |
| v5 | 2 segmentos, 1 ítem | 0, 0 |
| v6 | 24 segmentos, 0 ítems | **2 segmentos (0:01:00 y 0:01:02)**, 0 ítems |
| v7 | **no medible** | **no medible** |
| v8 | **no medible** | **no medible** |
| v9 | 24 segmentos, 0 ítems | 0, 0 |
| v10 | 37 segmentos, 2 ítems | 0, 0 |
| **Total** | **109 segmentos, 7 ítems** | **2 segmentos, 0 ítems** |

- **Los meses en cada escenario:** con casos ocultos o reservados hay 3. B tapa 5: esos 3 más los
  2 reservados enteros. A tapa los 12.
- **En B, todo lo nuevo viene del nombre del mes**, ninguno de la abreviatura. En v10 sale 0 porque
  el único segmento afectado ya es el tramo manual de 1:55:29.
- **v7 y v8 no se pueden medir aquí.** Son sesiones en cuarentena: el `Filtro` oculta la sesión
  entera y la CLI no enseña ningún segmento. Sus filtradas no están en esta máquina, y su cruda solo
  la lee el guion revisado. Al aplicar la regla (fase 2), su filtrada se rehace con
  `scripts/transcribir_sesion.py`, ya en `main`, y el recuento sale de su registro, que no trae
  texto.
- **4 ítems** citan una transcripción NO activa (v1–v5 tienen dos) y no se cruzaron.
- **Lo que mide la regla de hoy.** Lo que hoy se tapa queda fuera de la cuenta: los segmentos que ya
  oculta `_RE_MES` y los tramos. Un segmento que casa con la regla de hoy y con la nueva no cuenta
  como nuevo.

**Los ítems afectados.** En B no hay ninguno; en A hay 7 (v3: 3, v4: 1, v5: 1 y v10: 2).

**Propuesta de qué hacer con ellos** (decide el consultor):
- **(i) Con el criterio de la evidencia de hoy no hay que retirar nada.** La regla del mes (c) no
  oculta evidencia (sexta orden del 2026-10-01): un ítem es un extracto revisado y solo se oculta si
  cae en un tramo no citable o trae una fecha de `casos_ocultos`. Recomendación: dejarlos.
- **(ii) Si el consultor quiere que dejen de verse,** la vía que no edita nada es un **tramo no
  citable nuevo** por cada segmento afectado. Así `kb` los oculta por (b), sin tocar la evidencia.
- **(iii) Si además hay que sustituirlos,** `botsito evidence new --supersede <id>` con el MISMO
  tema y una cita que no pise el segmento. No hay una vía de «retirar sin sustituto», y la de
  propuesta no admite `supersede` (deuda de 2026-09-17).

### 0.5 Lo que el consultor tiene que decidir antes de la fase 1

1. **La fuente de (b):** crear `knowledge/cases/meses_reservados.yaml` (la propuesta del §0.1), u
   otra. Sin ella, la regla correcta es la del escenario A, que tapa los 12 meses.
2. **Los ítems:** (i), (ii) o (iii). En B no hay ninguno afectado.
3. **La lista blanca de la guardia** (`MESES_DE_DESARROLLO`, libros legibles): si entra en esta rama
   o queda como está. No decide qué se tapa en el texto, pero es una lista de meses a mano en una
   guardia del holdout. Hoy falla cerrado: lo que no está en ella no se lee.
4. **v7 y v8:** si basta con medirlas al rehacer su filtrada en la fase 2 con el guion de `main`.

## Decisiones tras la fase 0 (2026-10-04)

Decisiones del consultor del 2026-10-04 sobre la fase 0, copiadas tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisiones del consultor sobre la fase 0 de trabajo/cuarentena-por-condicion (2026-10-04). Cópialas tal cual, con su fecha, al informe docs/validation/CUARENTENA-POR-CONDICION.md, en una sección «Decisiones tras la fase 0».
>
> 1. Sí: crea knowledge/cases/meses_reservados.yaml como fuente única de (b), con 2026-02 y 2026-03, cada uno con su fuente.
>    Por qué: (b) hoy solo existe en prosa y mezclado con (a) en la lista. Una condición sin fuente no se puede comprobar.
>    - Régimen: solo añadir. Un mes que entra no sale; si algún día hiciera falta sacarlo, sería con un ADR.
>    - knowledge validate exige que cada entrada tenga fuente y formato AAAA-MM.
>    - Si el fichero falta, no se puede leer o no valida, la función de cases/holdout.py devuelve None y se tapan los 12 meses (escenario A). Ningún fallo de lectura deja un mes a la vista.
>    - La función que devuelve los meses libres une casos_ocultos, casos_reservados y meses_reservados.yaml. Aunque hoy (a) coincida con casos_reservados, se leen los dos.
>    - Acepto el diseño del punto 2: la condición se calcula en cases, y Filtro y en_cuarentena la reciben. MESES_FILTRADOS pasa a ser un diccionario de grafías de los 12 meses.
>
> 2. Los 7 ítems del escenario A se quedan como están.
>    Por qué: con la fuente de (b) el escenario que vale es el B, y en él no cae ningún ítem.
>    - Regla para la fase 2: si al rehacer v7 y v8 algún ítem ev-* cae en un segmento que pasa a ocultarse, para antes de seguir y dame solo el recuento por vídeo. Lo decido yo.
>
> 3. La lista blanca MESES_DE_DESARROLLO (guardia.py:199) no se cambia en esta rama, pero entra un test que la cruza con la fuente nueva.
>    Por qué: una lista blanca sí niega por defecto, pero escrita a mano puede separarse de la fuente sin que nadie lo vea.
>    - El test falla si algún mes de MESES_DE_DESARROLLO tiene días en casos_ocultos o en casos_reservados, o está en meses_reservados.yaml.
>    - Mídelo antes de escribirlo. Si hoy fallara, para y dímelo: sería un hallazgo, no algo que se arregla en silencio.
>    - En el informe, una línea que diga qué protege exactamente esa lista y por qué no la sustituye la condición.
>
> 4. Sí: v7 y v8 se miden cuando se rehagan sus filtradas en la fase 2, y siempre con el guion revisado.
>    - Primero recuentos y marcas de tiempo; ningún texto se muestra antes.
>    - Las cifras de v7 y v8 entran en la tabla de antes y después del informe, al lado de las demás.
>
> 5. El primer intento que contaba «set» suelto en v1 se declara como desviación corregida en el informe. Añade un test: «set» sin «backtest» no se filtra como mes, y con «backtest» sí.
>
> Sigue con las fases 1 y 2, con los tests y la CI del encargo. Al final:
> - push como fix/cuarentena-por-condicion y CI de Linux, con los números de run;
> - revisor independiente, con su informe pegado al final;
> - tamaño de PROJECT_STATE.
>
> Rama lista para revisión, NO cerrada.

## 1. Fase 1: la condición, tal cual quedó

### 1.1 La regla

**Un mes se tapa en el texto salvo que esté DEMOSTRADO libre.** Libre quiere decir:
- (a) ningún día suyo, de ningún año, está en `casos_ocultos` ni en `casos_reservados` (se leen los
  dos);
- (b) no está en `knowledge/cases/meses_reservados.yaml`;
- (c) las dos cosas se pudieron comprobar.

**Dónde vive cada pieza:**

| Pieza | Dónde | Qué hace |
|---|---|---|
| La fuente de (b) | `knowledge/cases/meses_reservados.yaml` (nuevo) | `2026-02` (fuente ADR-0025 y ADR-0046) y `2026-03` (ADR-0046 y `docs/validation/REGISTRO-MARZO.md`), con motivo y `declarado_el`. SOLO AÑADIR |
| La condición | `cases/holdout.py`: `meses_libres(repo) -> frozenset[int] | None` | une (a) y (b). Devuelve **None** si el fichero falta, no se lee o no valida, si un reparto es ilegible o si un id de caso no trae fecha |
| La validación | `cases/holdout.py`: `problemas_de_meses_reservados`; `validation/knowledge.py` | forma (AAAA-MM, claves exactas, motivo, fuente que exista —ADR o fichero— y fecha) y SOLO AÑADIR contra el historial, igual que `retirados.yaml`. Sin el fichero, `knowledge validate` da un AVISO |
| La regla del texto | `corpus/cuarentena.py`: `motivos_cuarentena(texto, libres)`, `en_cuarentena(textos, libres)`, `Filtro(..., libres=)`, `filtros`, `filtro_de`, `propuestas_con_ocultos` | tapan `meses_tapados(libres)`. Con **`libres=None` tapan los doce**. `corpus` no importa `cases`: lo comprueba un test por `ast` además de import-linter |
| Las grafías | `GRAFIAS_MES` (las 12 claves) y `ABREVIATURAS_MES` | un diccionario de grafías por mes, no una lista de meses vigilados. Las del ASR de septiembre, marzo, mayo y febrero no cambian. Cada mes tiene su nombre en español, en inglés y su abreviatura. «set» solo cuenta junto a «backtest» |
| Quién pasa `libres` | `cli.py` (`_meses_libres`, en `kb` y en los tres `filtro_de`), `retrieval/indice.py` (`construir_indice(..., libres=)`), `scripts/transcribir_sesion.py` (`lineas_filtradas(..., libres)`) y `scripts/ficheros_con_ocultos.py` | calculan `meses_libres` en la capa que puede leer `cases` |

**En el repositorio real** hay 7 meses demostrados libres y se tapan 5: los 3 con casos y los 2
reservados enteros.

`MESES_FILTRADOS`, `_RE_MES` y `_RE_ABREV` ya no existen.

### 1.2 Lo que sigue igual

«marco» no se tapa, y los límites de palabra («mayor», «mayoría», «siempre», «junto», «hago»)
tampoco tapan, ni con los doce meses. El test `test_6b` lo comprueba con `libres=None`.

### 1.3 Los tests (`tests/unit/test_cuarentena_por_condicion.py`, 60 casos)

| Encargo | Test | Qué hace |
|---|---|---|
| 1 | `test_1_*` | en un repo TEMPORAL, un caso reservado inventado en noviembre tapa noviembre sin tocar ninguna lista (`GRAFIAS_MES` no cambia). También un caso de otro año; uno `dev` no tapa |
| 2 | `test_2_*` | un `Filtro` sin datos tapa los doce meses (12 casos); y si la fuente de (b) falta, no se lee, tiene un mes mal escrito, no tiene fuente, cita un ADR que no existe o un fichero que no existe, o el reparto es ilegible, o un caso no trae fecha: `meses_libres` da None |
| 3 | `test_3_*` | un mes reservado entero sin casos se tapa |
| 4 | `test_4_*` | un mes libre de verdad no se tapa: la guardia puede dejar pasar algo |
| 5 | `test_5_*` | contra el repo real: **0 sin cubrir**, sin decir qué mes |
| 6 | `test_6_*` y los de `test_transcribir_sesion.py` | las grafías del ASR siguen tapando, con los meses libres del repo y sin ellos |
| decisión 5 | `test_set_suelto_no_es_un_mes_y_con_backtest_si` | «set» suelto no se tapa; con «backtest», sí |
| decisión 3 | `test_la_lista_blanca_de_la_guardia_no_se_separa_de_la_fuente` y `test_el_cruce_*_no_es_decorativo` | `MESES_DE_DESARROLLO` contra (a) y (b). Medido antes de escribirlo: **no fallaba** (2026-01, 2026-04 y 2026-08, ninguno con días en casos ni en la fuente de (b)) |
| fuente de (b) | `test_la_fuente_*`, `test_sin_la_fuente_*` | valida, y es SOLO AÑADIR: sacar o cambiar un mes es un error en un repo git temporal; añadir uno, no |

**Rotos a propósito, sobre el código y con el fichero restaurado después (mismo sha256):**
- **(i) `meses_tapados(None)` devuelve vacío en vez de los doce:** caen 36 casos (`test_2` 12,
  `test_2b` 7, `test_6` 16 y el de «set»).
- **(ii) `meses_libres` no usa `meses_reservados.yaml`:** caen 10 (`test_3`, `test_4`, `test_5` y 7
  de `test_6`).

**Un test viejo que cambia.** `test_abril_agosto_enero_y_el_lenguaje_normal_no_se_filtran`
(`test_transcribir_sesion.py`) daba por hecho que esos tres meses nunca se tapan. Ahora les pasa los
`meses_libres` del repo real y comprueba primero que los tres están demostrados libres. Sin ese
dato, la regla los taparía, y eso es lo que pide el encargo.

**Lo que protege la lista blanca de la guardia, y por qué la condición no la sustituye.**
`MESES_DE_DESARROLLO` decide qué **libros** (los xlsx del trader) se pueden ABRIR enteros, filas de
operaciones incluidas. La condición decide qué **nombre de mes** se tapa en el TEXTO de una
transcripción. Que un mes no tenga días reservados no lo hace legible como libro: hace falta además
que sea material de desarrollo leído y declarado (`CLAUDE.md:139`, ADR-0021 §1). Por eso la lista
blanca sigue negando por defecto, y el test solo vigila que no contradiga la fuente.

## 2. Fase 2: la aplicación

### 2.1 Cómo se aplica cada parte

- **v1–v6** no son sesiones en cuarentena. La regla se aplica al leer, en la CLI (`kb`,
  `corpus transcript show`, `frames show`, `evidence propose`), que desde la fase 1 pasa
  `meses_libres`. No hay filtrada que regenerar.
- **v7–v10** son sesiones en cuarentena. La CLI no enseña ningún segmento suyo; lo que se lee son
  sus filtradas, fuera del repo, que se rehacen con `scripts/transcribir_sesion.py`.
- **El guion revisado es el de `main`.** El de la rama pasa `libres`, pero la guardia solo deja
  ejecutar sobre una cruda el guion idéntico al blob de `main`. Se usó el de `main`: el cambio de la
  rama se apartó con `git restore --source=main --worktree` y se restauró después
  (`git diff --quiet HEAD` lo confirma).
- **El de `main` llama a `en_cuarentena(textos)` sin `libres`**, así que, con la librería nueva,
  **las filtradas de sesión salen en el escenario A (los 12 meses)**, que es un techo de B (B ⊆ A).
  Taparán solo los 5 meses de B cuando el guion nuevo esté en `main` (pendiente, §5).
- **Cómo se rehizo cada sesión:**
  - **v9 y v10:** `--solo-filtrar` sobre su cruda de siempre. Las filtradas de antes se guardaron
    como `*.filtrada-ANTES-condicion.md`.
  - **v7 y v8:** ASR completo sobre el audio extraído sin recodificar a `Desktop/sesion-02-v7-audio`
    y `-v8-audio`. Dan 602 y 229 segmentos, los mismos que sus transcripciones del corpus. Sus
    filtradas de antes no estaban en la máquina.
- **Nada se leyó:** solo se miraron los registros (sin texto) y las marcas `[CUARENTENA mm:ss–mm:ss]`.

Guion: `docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase2.py`, con su salida en
`medir_fase2-SALIDA.txt`.

### 2.2 Antes y después, por vídeo

**v1–v6**, con la regla REAL de la librería: el `Filtro` con los meses libres de hoy (escenario B)
frente al mismo `Filtro` con los libres que equivalen a la lista vieja. Son todos los meses menos
septiembre, marzo, mayo y febrero: sus grafías y abreviaturas no cambiaron, así que la regla vieja
es exactamente la nueva con esos libres. Se cuentan los segmentos ocultos por la regla (c):

| Vídeo | Antes (c) | Después (c) | Nuevos | Ítems ev-* en los nuevos |
|---|---|---|---|---|
| v1 | 0 | 0 | 0 | 0 |
| v2 | 3 | 3 | 0 | 0 |
| v3 | 3 | 3 | 0 | 0 |
| v4 | 26 | 26 | 0 | 0 |
| v5 | 0 | 0 | 0 | 0 |
| v6 | 69 | 72 | **3** (0:01:00, 0:01:02, 2:26:17) | 0 |

**v7–v10**, bloques `[CUARENTENA]` de la filtrada, en el escenario A:

| Sesión | Segmentos en cuarentena antes → después | Bloques antes | Bloques después (A) | Bloques nuevos | Ítems ev-* en los nuevos |
|---|---|---|---|---|---|
| v7 | sin filtrada de antes → 9 | 1 (su tramo no citable) | 3 | 2 (0:10:47, 0:32:59) | **0** |
| v8 | sin filtrada de antes → 0 | 0 | 0 | 0 | **0** |
| v9 | 29 → 57 | 8 | 15 | 8 | 0 |
| v10 | 45 → 89 | 12 | 23 | 15 | 2 (`ev-v10-014823-64248489`, `ev-v10-014853-76602fb4`, S-16) |

**Las diez, una al lado de otra** (decisión 4; añadida tras el revisor, R19 y A3).
- **Qué se cuenta:** los segmentos ocultos por la regla del texto (c) con sus vecinos.
- **De dónde sale cada cifra:**
  - v1–v6, de `medir_fase2-SALIDA.txt`;
  - v7–v10, de los registros de `transcribir_sesion.py`, cuyas líneas de recuento están copiadas, sin
    texto, en `medir_fase2-REGISTROS.txt`.
- **Escenarios:** v1–v6 en B, la regla que vale; v7–v10 en A, un techo de B.

| Vídeo | Antes | Después | Escenario del después | Nuevos | Ítems ev-* en los nuevos |
|---|---|---|---|---|---|
| v1 | 0 | 0 | B | 0 | 0 |
| v2 | 3 | 3 | B | 0 | 0 |
| v3 | 3 | 3 | B | 0 | 0 |
| v4 | 26 | 26 | B | 0 | 0 |
| v5 | 0 | 0 | B | 0 | 0 |
| v6 | 69 | 72 | B | 3 | 0 |
| v7 | sin filtrada de antes | 9 | A | ≤ 9 (2 bloques nuevos) | 0 |
| v8 | sin filtrada de antes | 0 | A | 0 | 0 |
| v9 | 29 | 57 | A | 28 (en B: 0, fase 0) | 0 |
| v10 | 45 | 89 | A | 44 (en B: 0, fase 0) | 2 (en B: 0) |

**Lo que dicen estas cifras:**
- **La regla de la decisión 2 no salta:** en v7 y v8 no cae ningún ítem ni siquiera con A, así que
  tampoco con B.
- **Los 2 ítems de v10** son de los 7 del escenario A que el consultor decidió dejar como están, y
  en B no caen (fase 0: v9 y v10, 0 segmentos nuevos en B).
- **v6 da 3 nuevos donde la fase 0 daba 2.** La fase 0 solo miraba los segmentos VISIBLES. Un
  segmento que ya estaba oculto, como vecino de otro, y que nombra el mes ahora tapado pasa a
  arrastrar a su otro vecino (2:26:17). La medida de la fase 2 usa el `Filtro` real sobre la
  transcripción entera, y es la que vale.

### 2.3 Los tramos no citables

> **Corrección (2026-10-04, tras el revisor, A4):** sí se añaden **dos tramos en v6**, los únicos
> segmentos nuevos del escenario B que vale: `0:01:00.72–0:01:03.16`, que cubre los segmentos de
> 0:01:00 y 0:01:02, y `2:26:17.201–2:26:18.341`. Los límites son los de los segmentos en
> milisegundos, sacados del `Filtro` real y sin imprimir texto. El motivo es «precaución: mes con
> días ocultos que la cuarentena mecánica no cubría», con el mismo criterio que el tramo de v10
> 1:55:29.
> - v6 no es una sesión en cuarentena: su cruda se lee por trozos con Read, y la guardia solo
>   respeta los tramos.
> - Ningún ítem cae en ellos: `knowledge validate` está en verde y la lista de la guardia coincide.
>
> Lo que sigue vale para v7–v10.

**En v7–v10 no se añade ningún tramo.**
- Los bloques nuevos de v9 y v10 son de A, no de B: en B no hay ninguno (fase 0). Registrarlos
  como tramos taparía de forma permanente, para la evidencia, nombres de meses demostrados libres,
  y ocultaría por (b) los 2 ítems de S-16 que el consultor decidió dejar.
- En v7 no se puede saber hoy cuáles de sus 2 bloques nuevos son de B, por la misma razón del
  guion.
- La filtrada de A ya los tapa al leer, y no hay ningún ítem que los pise.
- El tramo manual de v10 1:55:29–1:55:32 se queda como está.

### 2.4 Exposición

**Ninguna exposición nueva.**
- Las medidas solo imprimieron recuentos, marcas de tiempo e ids.
- Las filtradas rehechas no se abrieron: solo se miraron sus marcas de cuarentena.
- No hay fila nueva en `HOLDOUT-EXPOSICIONES.md`.

## 3. Los ítems afectados y qué se hizo con ellos

**Ninguno se tocó** (decisión 2). En el escenario B, el que vale, no cae ningún ítem en v1–v6 ni en
v9–v10. En v7 y v8 no cae ninguno ni siquiera en A. Los 7 ítems de A (v3: 3, v4: 1, v5: 1 y
v10: 2) siguen como estaban. Además, la regla del mes no oculta evidencia: lo dice la sexta orden
del 2026-10-01.

## 4. Desviaciones declaradas

1. **Fase 0, el primer intento contaba «set» suelto como septiembre** (decisión 5). Salían 3
   segmentos «nuevos» en v1 que eran la palabra «set». Se corrigió antes de entregar las cifras, y
   desde la fase 1 lo vigila `test_set_suelto_no_es_un_mes_y_con_backtest_si`.
2. **Las filtradas de sesión, en el escenario A y no en B.** La guardia solo ejecuta sobre una
   cruda el guion revisado (el de `main`), que no pasa `libres` (§2.1). Por eso las cifras de
   v7–v10 son un techo, y el «antes» de v7 y v8 sale de sus tramos y no de sus filtradas viejas, que
   ya no estaban.
3. **`scripts/a18_buscar.py` sigue construyendo su filtro sin `libres`.** Tapa los 12 meses: falla
   cerrado. No está en el contrato; su salida commiteada no se regenera en esta rama.
4. **`test_historial_sin_git.py` entra en el contrato** a mitad de rama. Enumera las líneas OK de
   `knowledge validate` y los ámbitos con historial; la fuente de (b) es una comprobación de
   historial más, como `retirados.yaml` (se amplió en el commit de la fase 1).
5. **`test_abril_agosto_enero_*` cambia** (§1.3): pasa los meses libres del repo real.
6. **La decisión 4 se cumple en la letra y no en el propósito** (revisor, B1). Las filtradas se
   rehicieron con el guion revisado, como pide la decisión, pero ese guion no da todavía la regla
   que entrega la rama. Lo que hay en disco para v7–v10 es A, un techo de B.
   - La parada de ítems se evaluó con A. Es conservadora y vale: si nada cae en A, nada cae en B.
   - Dejar la sesión 4 lista para activar con B exige el guion nuevo en `main` (§5).
7. **Las demás vías que construyen el filtro sin `libres`** (revisor, A7):
   - `retrieval/consultas.py:345`, cuando un vídeo no tiene filtro en el índice;
   - `cases/paquete.py`, con `construir_indice` por defecto;
   - los anexos de `CUARENTENA-POR-DEFECTO/` y `scripts/a18_buscar.py`.

   Todas tapan los 12: fallan cerrado. Las salidas commiteadas de esos anexos ya no se
   reproducirían igual, y son de una rama cerrada.
8. **La fuente de febrero** (revisor, A6). Cita ADR-0025 y ADR-0046, que solo dicen que es «el mes
   limpio pendiente». «Ciego, sin descargar, no se toca» está en el pendiente heredado 6 (Archivo 1
   de HISTORIA), que el motivo nombra pero la lista de fuentes no cita. **No se corrige:** la entrada
   ya está commiteada (`8b5b7fc`) y el fichero es SOLO AÑADIR. `knowledge validate` lo vigila y
   daría ERROR al modificarla, que es justo el régimen pedido.
9. **El test 5 usa las mismas fuentes que `meses_libres`** (revisor, A8). Si las dos se equivocaran
   igual, no lo vería. Lo compensa la rotura (ii) del §1.3, que lo hace caer.
10. **Arreglado en esta rama tras el revisor:**
    - A1: `medir_fase0.py`, histórico, fuera del contrato;
    - A2: el borrado del fichero entero da ERROR en `knowledge validate`, con su test
      `test_borrar_el_fichero_entero_tambien_es_sacar_meses`;
    - A3: los recuentos de los registros, en un anexo;
    - A4: los dos tramos de v6. La guardia de Claude los vigila al leer la cruda de v6 por trozos,
      y `test_guardia_claude.py::test_los_tramos_del_repo_real`, que fija esa lista, los incluye;
    - A5: `TODOS_LOS_MESES` tiene una sola definición, en `corpus/cuarentena.py`, y `cases` la
      importa;
    - B2: el Estado.

## 5. Pendientes que deja la rama

- **Con el guion nuevo ya en `main`:**
  - rehacer las filtradas de v7–v10 en el escenario B, con `--solo-filtrar --sesion 02/03/04` sobre
    las crudas que ya están fuera del repo;
  - registrar como tramo no citable cada bloque nuevo de B, si lo hay (en v9 y v10 la fase 0 dice
    que ninguno);
  - comparar la filtrada de v9 con `--sesion 03`: ya NO sale `f7529459…`, porque la regla cambió;
    el sha nuevo se anota allí.
- **`a18_buscar.py`**, si algún día se regenera su salida: pasarle `libres`.

## Estado

**Fases 0 y 1, hechas. Fase 2, hecha en lo que hoy se puede.**
- v1–v6: la regla se aplica en B, y v6 lleva sus dos tramos.
- Las filtradas de v7–v10 están en A, un techo de B. Su versión en B y sus posibles tramos, en el
  §5, cuando el guion nuevo esté en `main`.

Rama lista para revisión, NO cerrada.

Tamaño de `PROJECT_STATE.md`: 23.060 bytes (el tope del test es 25.000).

**CI de Linux** (push `git push origin trabajo/cuarentena-por-condicion:refs/heads/fix/cuarentena-por-condicion`):
- **run 208** (37241039661), `5584d8b`: **1 failed, 1970 passed, 8 skipped**.
- El único fallo es el esperado: `test_cli.py::test_state_check_ok_on_real_repo`, por el nombre
  `fix/`.
- 1979 casos, los mismos que el `make check` sellado en local (1979 passed).

El commit que recoge el informe del revisor tiene su propia CI; su número se da en el terminal.


## Informe del revisor

Lanzado el 2026-10-04 con el informe terminado (CI 208 incluida) sobre `5584d8b`. Se pega tal cual.

### Lo que se hizo con cada hallazgo

| # | Gravedad | Qué se hizo |
|---|---|---|
| A1 | bloquea | **Arreglado.** `medir_fase0.py` queda marcado HISTÓRICO, con su recuadro de corrección en el §0.4, y sale del contrato. La comprobación es ahora `medir_fase2.py`, que sí se reproduce. |
| A2 | importa | **Arreglado.** `meses_reservados_borrado(repo)`: si el fichero falta y HEAD o algún commit lo tuvo, `knowledge validate` da ERROR. Lo cubre `test_borrar_el_fichero_entero_tambien_es_sacar_meses`. Al escribir el test salió otro caso: un commit raíz no tiene padre, y `versiones_del_fichero` no lo veía. Se mira también HEAD. |
| A3 | importa | **Arreglado.** Las líneas de recuento de los registros, sin texto, van en `medir_fase2-REGISTROS.txt`. |
| A4 | importa | **Arreglado.** Dos tramos de precaución en v6 (§2.3), con 0 ítems dentro. |
| A5 | menor | **Arreglado.** `TODOS_LOS_MESES` tiene una sola definición (`corpus/cuarentena.py`), y `cases/holdout.py` la importa. |
| A6 | menor | **Declarado** (§4.8). La entrada ya está commiteada y el régimen es SOLO AÑADIR: no se reescribe. |
| A7 | menor | **Declarado** (§4.7). Todas esas vías fallan cerrado. |
| A8 | menor | **Declarado** (§4.9). Lo compensa la rotura (ii). |
| B1 | importa | **Declarado** (§4.6). Es la limitación de la guardia: el guion nuevo no se puede ejecutar sobre una cruda hasta que esté en `main`. |
| B2 | importa | **Arreglado.** El Estado dice «fase 2 hecha en lo que hoy se puede». |
| B3 | menor | Ya declarado (§4.4). |
| R19 | parcial | **Arreglado.** La tabla única de v1 a v10 está en el §2.2. |

### El informe, tal cual

**Informe del revisor · trabajo/cuarentena-por-condicion · 2026-10-04**

Base: `e98815a` (merge-base con `main`). Commits: `ad4fd75`, `8b5b7fc`, `5584d8b`. Único cambio sin commitear: el párrafo de la CI en «Estado» del informe, que he leído. Lo he comprobado todo por lectura y con comandos que no escriben. Los hallazgos de cada eje están separados. Al final hay una sección con las preguntas expresas del consultor, que solo apunta a los hallazgos.

#### Eje (a) · Reglas de la casa

Resumen: 1 bloquea, 3 importa, 4 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| A1 | **bloquea** | **El contrato falla.** La primera línea de `comprobaciones` (`medir_fase0.py`) no se ejecuta en HEAD: importa `_RE_MES`, que la fase 1 eliminó. El informe (§0.4) dice «se volvió a ejecutar y la salida sale idéntica byte a byte». Fue cierto en `ad4fd75` y ya no lo es. Aunque se arreglara el import, el guion lee `sesion-03.filtrada.md` y `sesion-04.filtrada.md`, que la fase 2 rehízo en el escenario A. Su `medir_fase0-SALIDA.txt` ya no se reproduciría. | `uv run python docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase0.py` → `ImportError: cannot import name '_RE_MES' from 'botsito.corpus.cuarentena'`. Líneas: `medir_fase0.py:19` y `:68`; `contrato.yaml:37`. Salida del guion `scripts/contrato_rama.py` sin ver este fallo, porque solo valida rutas. Arreglos posibles: quitar la línea del contrato y declarar el anexo como histórico, o congelarlo con la regla vieja incluida. |
| A2 | importa | **El «solo añadir» de `meses_reservados.yaml` no ve que se borre el fichero.** `knowledge validate` solo llama a `problemas_de_meses_reservados` si el fichero existe. Si falta, da `AVISO` y sale sin error, aunque el historial lo tenga. Así, borrar el fichero quita todos los meses sin error. En ejecución la regla falla cerrada (tapa los 12), pero el régimen «un mes que entra no sale» queda sin guardia en ese caso. Lo demás sí se comprueba contra el historial (ver «Comprobado»). Hallazgo por lectura de código; no lo ejecuté, porque habría que borrar el fichero. | `src/botsito/validation/knowledge.py` (diff de `8b5b7fc`): `if (repo / FICHERO_MESES_RESERVADOS).exists(): ... else: salida.append("AVISO: ... no existe ...")`. En cambio `holdout.py:problemas_de_meses_reservados` sí devuelve «no existe» como problema, pero `validate` no lo usa en esa rama. |
| A3 | importa | **Las cifras de v7–v10 del §2.2 no se reproducen con lo commiteado.** La columna «Segmentos en cuarentena antes → después» (v7: 9, v8: 0, v9: 29→57, v10: 45→89) no sale de `medir_fase2-SALIDA.txt`, que solo imprime bloques y marcas. Salen de registros fuera del repositorio. | `medir_fase2-SALIDA.txt` (sin ninguna de esas cifras); `CUARENTENA-POR-CONDICION.md` §2.2 (tabla de v7–v10). |
| A4 | importa | **Los 3 segmentos nuevos de v6 no son tramo y §2.3 no los discute.** Es el único vídeo donde el escenario B (el que vale) oculta algo nuevo: 0:01:00, 0:01:02 y 2:26:17. Se ocultan solo por la CLI. La guardia de Claude deja leer la cruda de v6 con `Read` por trozos y solo respeta los tramos. Esos segmentos nombran un mes con días ocultos que la lista vieja no cubría. Hay precedente exacto: el tramo manual de v10 1:55:29, con la regla «cada segmento que nombre un mes con días ocultos fuera de `MESES_FILTRADOS` entra aquí». §2.3 justifica «ningún tramo» solo para v7, v9 y v10. Tapar v6 con un tramo no choca con los ítems: 0 ítems caen ahí. | `medir_fase2-SALIDA.txt` (v6: `3 (0:01:00, 0:01:02, 2:26:17)`); `knowledge/corpus/tramos_no_citables.yaml:279-285` (el precedente); `.claude/hooks/guardia.py:203` (`SESIONES_SIN_CUARENTENA = {"v6"}`); informe §2.3. |
| A5 | menor | `TODOS_LOS_MESES` está definida dos veces, con el mismo valor: en `cases/holdout.py` y en `corpus/cuarentena.py`. Se podrían separar sin que nada lo avise. | `src/botsito/cases/holdout.py` (junto a `FICHERO_MESES_RESERVADOS`); `src/botsito/corpus/cuarentena.py` (tras `ABREVIATURAS_MES`). |
| A6 | menor | La `fuente` de `2026-02` cita ADR-0025 y ADR-0046. Ambos solo dicen que febrero es «el mes limpio que sigue pendiente». «Ciego, sin descargar, no se toca» está en HISTORIA Archivo 1 / PROJECT_STATE, que la lista de fuentes no cita. `knowledge validate` solo comprueba que la fuente exista, no que sostenga el motivo. | `docs/adr/0025-*.md:34` y `docs/adr/0046-*.md:20` (los únicos «febrero»); `knowledge/cases/meses_reservados.yaml` (entrada 2026-02). |
| A7 | menor | Los anexos de `CUARENTENA-POR-DEFECTO/*.py` (`recuento.py`, `exposicion_items.py`, `exposicion_79.py`, `copias_items.py`, `auditoria_knowledge.py`, `citas_de_salidas.py`) y `scripts/a18_buscar.py:194` construyen el `Filtro` sin `libres`. Fallan cerrado (tapan los 12), pero sus salidas commiteadas ya no se reproducirían. El informe lo declara solo para `a18_buscar` (§4.3). | `rg "Filtro\(\|filtro_de\("` sobre `docs/validation/anexos/CUARENTENA-POR-DEFECTO/` y `scripts/a18_buscar.py`. |
| A8 | menor | El test 5 del encargo («0 sin cubrir») calcula `vigilados` con las mismas fuentes que `meses_libres` (casos ocultos y reservados, más `meses_reservados.yaml`). Por eso casi no puede fallar si `meses_libres` se equivoca igual. La rotura (ii) del informe sí lo hace caer, y eso lo compensa en parte. | `tests/unit/test_cuarentena_por_condicion.py:187-196`. |

**Comprobado sin hallazgos:**
- **Contrato.**
  - `scripts/contrato_rama.py`: «CONTRATO: 20 ficheros dentro del contrato… 4 comprobaciones».
  - `scripts/ficheros_con_ocultos.py` → `OK: .claude/hooks/ficheros_con_ocultos.txt coincide`.
  - `botsito knowledge validate` → sin ERROR. Incluye `OK: 2 meses reservados enteros, con formato y fuente, solo-anadir intacto`.
  - `make-check.log`: `1979 passed`, y `SELLO: ... c5fc0454fe97...` es exactamente `git rev-parse HEAD^{tree}`. `PICO DE MEMORIA` 289 MiB.
  - `make check` no lo lancé.
- **Trailers `Fuente:`.** Solo `8b5b7fc` toca `knowledge/cases/` (el fichero nuevo). Lleva `Fuente: ADR-0025` y `Fuente: ADR-0046` en el cuerpo, y ambos ADR existen.
- **Regímenes de cambio.** `git diff --name-status main...HEAD` no toca evidence, feedback, manifests, transcripciones, fotogramas, `libros.yaml`, holdout, spec, engine ni domain. `HISTORIA.md` solo suma (0 líneas borradas), y `tramos_no_citables.yaml` no cambia.
- **Ambigüedades, ADR e informes cerrados.** No cambia ninguno. No hay sitios nuevos con `cita`, así que no aplican las tres guardias. No hay cifras de negocio nuevas.
- **Exposición.** `HOLDOUT-EXPOSICIONES.md` sin cambios. Los anexos solo imprimen recuentos, marcas e ids (los dos guiones y sus salidas). Nombran un mes únicamente en comentarios o tests, y que ese mes tiene días ocultos ya es público en `SESION-04-EXTRACCION.md` de `main`.
- **PROJECT_STATE.** El punto P queda «En revision en trabajo/cuarentena-por-condicion», sin moverlo a HISTORIA. `wc -c` da 22.998 bytes, como dice el informe.
- **CI.** El run 208 es `37241039661` y su `headSha` es `5584d8b` (mismo que HEAD y que `origin/fix/cuarentena-por-condicion`). `gh run view --log-failed` muestra `FAILED tests/unit/test_cli.py::test_state_check_ok_on_real_repo` y `1 failed, 1970 passed, 8 skipped`, que suman 1979. El último commit tiene su CI.
- **Citas.** Cinco citas del informe contra su fuente: `main:cuarentena.py:218`, `holdout.py:350` y `:455`, `guardia.py:199` y `CLAUDE.md:145-146` y `152`. Las cinco son correctas. La de `vistos.yaml:33` apunta a `meses:`.
- **Tests.** `pytest tests/unit/test_cuarentena_por_condicion.py tests/unit/test_transcribir_sesion.py -p no:cacheprovider`: todo pasa. Son 60 casos en el fichero nuevo, como dice el informe.
- **«Solo añadir» contra el historial, en lo que sí cubre.** Hay un test en un repo git temporal (`test_la_fuente_es_solo_anadir`). Detecta sacar un mes, modificar uno (también sin commitear) y deja pasar añadir. Se compara cada versión con cada padre (`versiones_del_fichero`, `--full-history`) más el árbol de trabajo contra HEAD. En el repo real `validate` dice «intacto». La laguna es solo A2.

#### Eje (b) · Encargo

Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 20 hechos, 2 parciales, 0 no hechos (más 1 «hecho de otra forma» declarado, el R17).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| R1 | Fase 0.1: fuente de (b), con fichero y línea | Hecho | Informe §0.1 (tabla con 8 sitios). Las citas coinciden. |
| R2 | Fase 0.2: quién construye el filtro y propuesta de entrada | Hecho | §0.2. Es lo que se implementó. |
| R3 | Fase 0.3: sitios de `MESES_FILTRADOS`, `_RE_MES` y `_RE_ABREV` | Hecho | §0.3. |
| R4 | Fase 0.4: medida v1–v10 sin texto ni mes, ítems afectados y propuesta de retirada | Hecho (v7 y v8 «no medible», declarado) | `medir_fase0-SALIDA.txt`; §0.4. (Ver A1: el guion ya no corre.) |
| R5 | Fase 1: `MESES_FILTRADOS` deja de ser la fuente de verdad y queda un diccionario de grafías | Hecho | `rg MESES_FILTRADOS\|_RE_MES\|_RE_ABREV src scripts` solo da comentarios y prosa. `GRAFIAS_MES` tiene los 12 meses (`test_ningun_mes_queda_sin_grafias`). |
| R6 | Sin datos se filtran los 12 meses; ningún valor por defecto deja un mes a la vista | Hecho | `meses_tapados(None)` devuelve los 12; `Filtro.libres=None`, `filtros()`, `filtro_de()`, `propuestas_con_ocultos()` y `construir_indice()` tienen `None` por defecto. Tests `test_2_*`, `test_2b`, `test_2c` y `test_2d`. |
| R7 | El «marco» y los límites de palabra siguen funcionando | Hecho | `test_6b_*`, con `libres=None`. |
| R8 | Fase 2: filtradas y tramos regenerados con la regla nueva por la vía de su régimen | **Parcial** | v1–v6: la regla se aplica al leer, por la CLI (hecho). v7–v10: se rehicieron en el escenario A, no en el B que entrega la rama (§2.1 y §4.2, declarado). Tramos: ninguno nuevo (§2.3; ver A4 para v6). El rehacer en B queda para §5. |
| R9 | El tramo manual de v10 1:55:29–1:55:32 se queda | Hecho | `tramos_no_citables.yaml` sin diff. |
| R10 | Lo que se decida sobre los ítems de la fase 0 | Hecho | §3. Los 7 del escenario A se dejan (decisión 2). En v7 y v8 no cae ninguno ni en A, así que la regla de parada no salta. Reproducido con `medir_fase2.py`. |
| R11 | Exposición nueva declarada hoy, sin texto ni fechas | Hecho | §2.4: ninguna. `HOLDOUT-EXPOSICIONES.md` sin diff. |
| R12 | Test 1: caso inventado en un mes que no se filtra, en repo temporal | Hecho | `test_1_*` con `tmp_path`, sin tocar listas. |
| R13 | Test 2: filtro sin datos filtra todos | Hecho | `test_2_*` (12 casos). |
| R14 | Test 3: mes reservado entero sin casos se filtra | Hecho | `test_3_*`. |
| R15 | Test 4: mes libre de verdad no se filtra | Hecho | `test_4_*`. |
| R16 | Test 5: ningún mes con días queda sin cubrir, «0 sin cubrir» | Hecho (ver A8) | `test_5_*`. |
| R17 | Test 6: los tests de grafías que ya existían siguen pasando | Hecho de otra forma (declarado) | `test_abril_agosto_enero_*` cambió para pasar los `meses_libres` del repo real (diff de `test_transcribir_sesion.py`; declarado en §1.3 y §4.5, con motivo). El resto no cambia. **Matiz:** los tests viejos de grafías llaman a `motivos_cuarentena(texto)` sin `libres`, así que tapan los 12 y pasan trivialmente. La prueba de que siguen tapando con los libres reales está en `test_6_*` del fichero nuevo. |
| R18 | CI como `fix/...` con números de run; solo falla el de `state check` | Hecho | Run 208 (`37241039661`); único fallo `test_state_check_ok_on_real_repo`. |
| R19 | Informe con fase 0, condición, recuentos por vídeo, ítems, desviaciones y tamaño de PROJECT_STATE | **Parcial** | Están todos. El apartado de recuentos tiene dos defectos: v7–v10 salen en una tabla aparte, con otra métrica (bloques) y en el escenario A, no «al lado de las demás» (decisión 4). Ver B1 y A3. |
| R20 | PROJECT_STATE: el punto P pasa a «en revisión…», sin moverlo | Hecho | Diff de `PROJECT_STATE.md`. |
| R21 | Decisión 1: `meses_reservados.yaml` con 2026-02 y 2026-03 y su fuente; solo añadir; `validate` exige fuente y AAAA-MM; `None` si falta, no se lee o no valida; la función une `casos_ocultos`, `casos_reservados` y el fichero | Hecho (ver A2 y A6) | `holdout.py:meses_libres`; `knowledge validate`; `test_2b`. Se leen los dos mapas, aunque hoy coincidan. |
| R22 | Decisión 3: test que cruza `MESES_DE_DESARROLLO` con la fuente, medido antes; línea sobre qué protege la lista | Hecho | `test_la_lista_blanca_de_la_guardia_*` y `test_el_cruce_*_no_es_decorativo`; informe §1.3 («Lo que protege la lista blanca…»). |
| R23 | Decisión 5: «set» suelto declarado como desviación y con test | Hecho | §4.1; `test_set_suelto_no_es_un_mes_y_con_backtest_si`. |
| R24 | Qué NO se toca: motor, spec, feedback, ambigüedades, nada de la sesión 4, evidencia y transcripciones inmutables | Hecho | `git diff --name-status` sin esas rutas. |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| B1 | importa | **La decisión 4 se cumple en la letra y no en el propósito.** Se usó el guion de `main`. Eso es lo que pide «siempre con el guion revisado», y está declarado. Pero ese guion llama `en_cuarentena(textos)` sin `libres`, así que con la librería de la rama las filtradas de v7–v10 salen tapando los 12 meses. Efectos: (1) lo que hay en disco no es lo que la regla entrega (B). (2) Las cifras «después» de v7–v10 son un techo (A). El B de v7 (2 bloques nuevos en A) no se conoce, y el de v9 y v10 se infiere de la medida de la fase 0 sobre las filtradas viejas. (3) Con v8 no hay duda, porque en A da 0. (4) El propósito de la rama, dejar la sesión 4 lista para activar, no se logra hasta que el guion nuevo esté en `main` (§5). Con el matiz de que la parada de ítems se evaluó con A, que es conservador y válido. | Informe §2.1, §2.2 (v7–v10 «después (A)»), §4.2 y §5. `scripts/transcribir_sesion.py:460` (en la rama pasa `libres`; el de `main` no). |
| B2 | importa | **El «Estado» afirma más de lo que hay.** Dice «FASES 0, 1 y 2 HECHAS». Pero §5 deja pendiente lo central de la fase 2: rehacer las filtradas de v7–v10 en B y registrar los tramos que salgan. Y A4 deja el tema v6 sin cerrar. Lo honesto sería «fase 2 hecha en lo posible; filtradas de v7–v10 en A, pendiente de B». | Informe «Estado» y §5. |
| B3 | menor | Fuera del encargo y declarado: `test_historial_sin_git.py` entra en el contrato a mitad de rama (§4.4). Está justificado, porque enumera los OK de `knowledge validate` y la fuente de (b) es un OK nuevo. `validation/knowledge.py` también se toca, y es necesario para la decisión 1. | `contrato.yaml`; informe §4.4. |

#### Preguntas expresas del consultor

**1. ¿Queda una lista de meses escrita a mano que decida qué se tapa en el texto de las transcripciones?** No.
- **Lo que decide el texto, todo declarado y legítimo:**
  - `knowledge/cases/meses_reservados.yaml`: la fuente de (b), aprobada, con `fuente`, solo añadir y validada.
  - `GRAFIAS_MES` y `ABREVIATURAS_MES`: tablas de grafías por mes, con las 12 claves. No eligen qué se vigila. Quién se tapa lo decide `meses_libres(repo)` con los datos.
  - `TODOS_LOS_MESES`: constante (ver A5).
- **Lo que parece lista pero no decide qué se tapa:**
  - `_MESES_NUM` y `_RE_NOMBRE_MES` (`cuarentena.py`): tabla de conversión nombre→número de los 12 meses, para `fechas_en`.
  - `guardia.py:221` (`MESES`): tabla de conversión, para leer rutas.
  - `cli.py:2630-2642`: los meses de construcción salen de `criterio_fidelidad.yaml`, no están escritos a mano.
- **Lo que sí es una lista a mano, y decide libros, no texto:**
  - `guardia.py:199` `MESES_DE_DESARROLLO`: decide qué libros se leen y no cambia en esta rama. Falla cerrado, y ahora un test la cruza con la fuente. Medido: hoy no choca. La línea del informe (§1.3) explica por qué la condición no la sustituye.
  - Los guiones de medida de velas (`caja_77`, `embudo_77`, `viabilidad_*`, `sesgo_h4_diagnostico`) acotan velas, no texto.
- **Una en un anexo, sin efecto sobre el filtro:** `medir_fase2.py:44` (`LIBRES_DE_LA_LISTA_VIEJA = todos − {2,3,5,9}`) es el comparador «antes», una lista explícita para medir. `medir_fase0.py:85` lleva otra igual (`{2, 3, 5, 9}`), en un guion que ya no corre (A1).

**2. Sin datos se tapan los doce, y ningún camino deja meses a la vista.** Comprobado.
- `meses_libres` devuelve `None` si el fichero falta, no se lee o no valida, si un reparto es ilegible o si un caso no trae fecha (`test_2b`, `test_2c`, `test_2d`).
- `meses_tapados(None)` devuelve los 12, y `Filtro`, `filtros`, `filtro_de`, `propuestas_con_ocultos` y `construir_indice` tienen `libres=None` por defecto.
- Rutas que no pasan `libres`: `retrieval/consultas.py:345` (`Filtro(video)`), `cases/paquete.py:708` (`construir_indice` por defecto), `scripts/a18_buscar.py:194`, los anexos de `CUARENTENA-POR-DEFECTO` y la rama del guion de `main`. Todas tapan los 12, es decir, fallan cerrado.
- `meses_libres` solo captura `MesesReservadosError`, `RepartoIlegibleError` y `RetiradosError`. Otra excepción haría fallar el comando, no dejaría un mes visible.
- Lo que falta: ningún test recorre los llamadores. Todo se apoya en el valor por defecto. Es una observación, no un hallazgo.

**3. Solo-añadir contra el historial.** Se comprueba de verdad, salvo el borrado del fichero entero (A2).

**4. Medidas.** `medir_fase0-SALIDA.txt` y `medir_fase2-SALIDA.txt` imprimen solo recuentos, marcas de tiempo e ids. Lo mismo hacen los guiones: leen texto, pero nunca lo imprimen. Reproduje `medir_fase2.py` y la salida coincide con la commiteada. El guion de la fase 0 ya no se puede reproducir (A1).

**5. Desviación de las filtradas en el escenario A.** Cumple la letra de la decisión 4 («siempre con el guion revisado»). El guion de la rama habría roto la guardia, y el de `main` es el único que se puede ejecutar. La desviación está declarada (§2.1, §4.2, §5) y es segura: A cubre a B. No cumple el propósito: lo entregado es un techo, no la regla nueva (B1 y B2).

#### Lo que no pude comprobar

- **Las roturas a propósito del §1.3** (36 y 10 tests caen, «mismo sha256»). Exigirían escribir el código. Solo leí que el informe las declara.
- **Los registros y las filtradas de v7–v10 fuera del repo.** No abrí ninguna filtrada ni registro. Las cifras «602 y 229 segmentos, los mismos que el corpus» y «9, 29→57, 45→89» (A3) quedan sin verificar. De las filtradas solo vi marcas de tiempo, al ejecutar `medir_fase2.py`, que las abre sin imprimir texto.
- **El procedimiento `git restore --source=main --worktree`** del §2.1 y que «`git diff --quiet HEAD` lo confirme». No lo reconstruí. Sí vi que HEAD y el árbol son consistentes con el sello.
- **El borrado del fichero en `knowledge validate` (A2).** Lo derivo de leer el código; no lo ejecuté porque habría que borrar o mover un fichero.
- **Contenido de las crudas v6, v7 y v8.** No lo abrí. Que los 3 segmentos de v6 nombran un mes con días ocultos lo tomo del informe y de las medidas, que cuentan marcas, no texto.
- **El `make check` local.** No lo lancé. Verifiqué el log (`1979 passed`, `SELLO` igual al árbol de HEAD) y el run 208 de CI.

#### Comandos ejecutados

1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `git diff main...HEAD` sobre `cuarentena.py`, `indice.py`, `cli.py`, `ficheros_con_ocultos.py` y `transcribir_sesion.py`
4. `git diff main...HEAD -- src/botsito/cases/holdout.py src/botsito/validation/knowledge.py` y `cat knowledge/cases/meses_reservados.yaml`
5. `rg` de nombres de meses y de `filtro_de|Filtro(|en_cuarentena|motivos_cuarentena|propuestas_con_ocultos|construir_indice|meses_libres|MESES_FILTRADOS|_RE_MES|_RE_ABREV` en src, scripts, tests y config
6. `rg` de `MESES_DE_DESARROLLO` y de fechas en `.claude/hooks/*.py`, `cli.py`, `corpus` y `validation`
7. `uv run python docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase0.py` → ImportError
8. `uv run python scripts/ficheros_con_ocultos.py` → OK
9. `uv run botsito knowledge validate` → sin ERROR
10. `uv run python docs/validation/anexos/CUARENTENA-POR-CONDICION/medir_fase2.py` → salida idéntica a la commiteada
11. `uv run python -m pytest tests/unit/test_cuarentena_por_condicion.py -p no:cacheprovider -q --collect-only` → 60
12. `uv run python -m pytest tests/unit/test_cuarentena_por_condicion.py tests/unit/test_transcribir_sesion.py -p no:cacheprovider -q` → todo pasa
13. `git diff main...HEAD -- PROJECT_STATE.md`, `wc -c PROJECT_STATE.md`, `git diff main...HEAD --name-status`, `git diff HEAD -- docs/validation/CUARENTENA-POR-CONDICION.md`
14. `git log --format='%h%n%B' main..HEAD`, `git show <sha> --stat` (los tres commits)
15. `gh run list --branch fix/cuarentena-por-condicion`, `gh run view 37241039661 --log-failed`, `git rev-parse origin/fix/cuarentena-por-condicion` y `HEAD` y `HEAD^{tree}`, `grep` de `SELLO|PICO|passed|failed` en `make-check.log`
16. `git diff main...HEAD -- tests/unit/test_transcribir_sesion.py tests/unit/test_historial_sin_git.py`
17. `git grep`, `grep` y `sed` para verificar citas (`main:cuarentena.py`, `holdout.py`, `CLAUDE.md`, `HISTORIA.md`, `ADR-0025` y `ADR-0046`, `tramos_no_citables.yaml`), `ls docs/adr`, y la lectura de `historial.py` y del bloque de `holdout.py` sobre `casos_reservados` y `casos_ocultos`

## Orden de cierre (2026-10-04)

Orden de cierre del consultor del 2026-10-04, copiada tal cual:

> Modelo: el que tengas · Esfuerzo: medio
>
> Orden de cierre de trabajo/cuarentena-por-condicion (consultor, 2026-10-04). Revisada: último commit 7120217, CI de Linux run 209 (37244398309) con el único fallo esperado, el de state check por el nombre fix/. Cópiala tal cual al informe y al registro del cierre en HISTORIA.
>
> TAG: stable/F36w-cuarentena-por-condicion. Antes de usarlo, comprueba en HISTORIA que la última letra es la v. Si no lo es, para y dímelo.
>
> DECISIONES QUE CIERRAN LA REVISIÓN
> 1. La fuente de febrero en meses_reservados.yaml se queda como está, sin ADR.
>    Por qué: no cambia qué se tapa, y «ciego, sin descargar» ya consta en CLAUDE.md. Déjalo declarado en el informe como desviación aceptada.
> 2. Las filtradas de sesión en el escenario A son aceptables hasta la rama siguiente.
>    Por qué: tapar de más no expone nada, y rehacerlas en B necesita el guion nuevo en main.
>
> HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
> - importa · De Claude Code, no del revisor: en la primera medida de la fase 0, «set» suelto contaba como mes. Lección: toda medida de un filtro nuevo se compara con un caso negativo conocido antes de dar cifras.
> - importa · Del revisor: el guion de la fase 0 importaba algo que la fase 1 eliminó, y la comprobación del contrato dejó de correr sin avisar. Lección para el revisor: después de cada fase que borra o renombra algo, correr la comprobación del contrato.
> - Del consultor, nada que el revisor no viera.
>
> NEXT ACTION EN EL COMMIT DE ESTADO
> Sustituye P por:
> «P. Rama corta: rehacer con el guion de main las filtradas de sesión (v7–v10) en el escenario B. Medir antes con recuentos y marcas de tiempo, sin texto. Si algún ítem ev-* cae en un segmento que pasa a ocultarse, parar y avisar al consultor. Va antes de activar la sesión 4 (CUARENTENA-POR-CONDICION.md §5).»
> No toques los demás puntos.
>
> RITUAL
> Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
> - registro y fila de ERRORES-RECURRENTES en la rama;
> - merge y tag;
> - commit de estado;
> - make check sellado;
> - push atómico de main y el tag;
> - CI de main en verde;
> - borrar trabajo/cuarentena-por-condicion en local y fix/cuarentena-por-condicion en origin.
>
> INFORME FINAL
> Sha de main, tag y el sha al que apunta, run de la CI de main con su resultado, ramas que quedan y tamaño de PROJECT_STATE.

**Desviaciones aceptadas por el consultor:**
- **La fuente de febrero (§4.8).** Se queda como está, sin ADR: no cambia qué se tapa, y «ciego, sin
  descargar» ya consta en `CLAUDE.md`.
- **Las filtradas de sesión en el escenario A (§4.2 y §4.6).** Valen hasta la rama siguiente: tapar
  de más no expone nada, y rehacerlas en B exige el guion nuevo en `main`. Es el nuevo punto P de la
  Next Action.

Letra comprobada en HISTORIA: la última cerrada era la `v` (`stable/F36v-sesion-04`), y
`stable/F36w-*` no existe ni en local ni en `origin`.
