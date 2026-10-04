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
`medir_fase0-SALIDA.txt`. Se volvió a ejecutar y la salida sale idéntica byte a byte. **Solo
imprime recuentos, marcas de tiempo e ids, nunca texto ni qué mes.**

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

## Estado

FASE 0 ENTREGADA. Esperando las decisiones del §0.5 antes de escribir código. Rama NO cerrada.

Tamaño de `PROJECT_STATE.md` al abrir: se da en el informe final.
