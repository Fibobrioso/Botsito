# CUARENTENA-POR-CONDICION-2 · Diciembre, la coma y el punto, y el barrido ancho en la skill (G.5)

Rama `trabajo/cuarentena-por-condicion-2`, abierta el 2026-10-28 desde `main` en 0fa9c81 (commit de
estado sobre el merge faf5ce2, tag `stable/F38g-recorrida-construccion`). Encargo:
`docs/encargos/trabajo-cuarentena-por-condicion-2.md`. Tramo: «Carril: guardias y deuda» (G.5 de
`docs/plan/HOJA-DE-RUTA.md`; F de la Next Action).

Antes de abrir se comprobó con git (skill `abrir-rama`, paso 1):

- `git rev-parse --short main` = 0fa9c81; `git rev-parse main origin/main` da dos veces
  0fa9c81b5b26d47f884860ff4530eb0a37eb6b02; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F38g-recorrida-construccion`;
  `git rev-parse "stable/F38g-recorrida-construccion^{commit}"` = `git rev-parse main^1` =
  faf5ce20a4dbcec47b7b18dbc4ff41420946e23b; `git ls-remote --tags origin stable/F38g-recorrida-construccion`
  devuelve el tag (6af57ae3…).
- La CI de `main` sobre 0fa9c81b5b26d47f884860ff4530eb0a37eb6b02, por la API de check-runs con el
  sha literal (`gh api repos/{owner}/{repo}/commits/<sha>/check-runs`): un check `python`,
  `completed` / `success`, run 40633309578 (el que cita el cierre).
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío, y
  `git ls-remote --heads origin` solo da `main`.

Al abrir, la guardia de Claude Code negó dos comandos y se siguió la forma que ella misma propone
(regla de la rama, declarada aquí): `c=$(git log ...)` («el nombre de entorno `c` no esta en la
lista cerrada») se partió en dos llamadas sin variable; y `git add ... && uv run botsito state check`
(«antes, en el mismo comando, va `git add`») se partió en llamadas sueltas.

## 0. Fase 0 (2026-10-28, sin escribir código)

Todo medido en el árbol de la rama en c0607bd, cuyo código es el de `main`. Ninguna lectura de
material: solo código, tests y documentos del repositorio, y una sonda con TEXTO SINTÉTICO
(`sonda_fase0.py`, en el scratchpad, fuera del repo) que del repositorio real solo imprime cuántos
meses son libres y si octubre y diciembre lo son.

### 0.a `src/botsito/cases/holdout.py`: los meses libres y su fuente

- **`meses_libres`** (`holdout.py:620-640`). Un mes es libre solo si se demuestran dos cosas:
  (a) ningún día suyo, de ningún año, está en `casos_ocultos` ni en `casos_reservados`
  (`:631`, la unión de los dos; `:635-639`, el mes de cada id por `_MES_DE_CASO`, `:559`); (b) no
  está en `meses_reservados.yaml` en ningún año (`:630` y `:634`, `int(mes[5:7])`: la entrada
  `2025-12` tapa el mes 12 de cualquier año). Si el fichero falta o no valida, un reparto es
  ilegible o un caso no trae fecha, devuelve None (`:632-633`, `:638`) y la regla tapa los doce.
- **`_problemas_de_mes`** (`:582-602`) exige de cada entrada: la clave con forma AAAA-MM
  (`_MES_AAAA_MM`, `:557`); EXACTAMENTE las tres claves `motivo`, `fuente`, `declarado_el`
  (`CLAVES_MES_RESERVADO`, `:556`); motivo no vacío; `fuente` una lista no vacía cuyas fuentes
  existan (`_fuente_existe`, `:575-579`: `ADR-NNNN` con su fichero en `docs/adr/`, o un fichero del
  repositorio); `declarado_el` AAAA-MM-DD.
- **`knowledge validate`** (`validation/knowledge.py:664-692`) llama a
  `problemas_de_meses_reservados` (`holdout.py:667-714`): la forma de arriba, y SOLO AÑADIR contra
  el historial, versión a versión y también contra el árbol de trabajo (`:692`): sacar un mes
  (`:707-711`) o cambiar su entrada (`:712-713`) es un ERROR, y borrar el fichero entero también
  (`meses_reservados_borrado`, `:652-664`). **No hay ninguna excepción**: ni por ADR ni por nada.
- **De dónde sale el régimen.** De la decisión del consultor del 2026-10-04 sobre la fase 0 de
  `trabajo/cuarentena-por-condicion`, copiada en `docs/validation/CUARENTENA-POR-CONDICION.md`,
  «Decisiones tras la fase 0», punto 1 (`:206-208`: «Régimen: solo añadir. Un mes que entra no
  sale; si algún día hiciera falta sacarlo, sería con un ADR.»). **No es un ADR**: ningún ADR
  define el fichero (`grep -l meses_reservados docs/adr/*.md` da solo ADR-0078 y ADR-0079, que lo
  citan como criterio, abajo).

### 0.b `src/botsito/corpus/cuarentena.py`: la regla de la fecha

- **`_RE_FECHA`** (`cuarentena.py:283-289`), con `_NUM = \d{1,2}`:
  1. `(?<![\d.,])N\s*[/-]\s*N(?:\s*[/-]\s*\d{2,4})?(?![\d.,])`: «31/02», «31-02-26»;
  2. `(?<![\d.,])N\.N\.\d{2,4}(?![\d.,])`: «31.02.26», con TRES partes (el comentario: «dos
     partes: precio»);
  3. `(?<![\d.,])N\s+del?\s+N(?![\d.,])`: «45 del 13», «3 de 9»;
  4. `\bmes\s+N\b`: «el mes 9».
- **Por qué los lookarounds excluyen la coma y el punto.** Para no partir un número decimal: sin
  ellos, «1.0850» o «10,5» darían un trozo que casa. Lo dice el docstring de origen
  (`scripts/transcribir_sesion.py` en 9688571: «las fechas numericas con «/» o «-» (con punto y
  dos partes son precios)») y el comentario de la alternativa 2. **El comentario de hoy no habla de
  «10,5»** como dice el encargo: solo de «precio» en la alternativa 2 (`:286`). El efecto es el
  hueco: la exclusión no mira si al otro lado hay un dígito, así que una coma o un punto de
  PUNTUACIÓN también la disparan.
- **`numeros_a_cifras`** (`:186-213`) pasa a cifras los números en letra de 0 a 99 («treinta y
  cinco» → 35, «veinticinco» → 25), sobre texto ya normalizado; «un» y «una» no. `motivos_cuarentena`
  (`:301-316`) aplica `numeros_a_cifras(normalizar(texto))` (`:305`) antes de las reglas, así que
  «el veinticinco del diez,» es lo mismo que «el 25 del 10,».
- **Medido en el código de `main`** (sonda, texto sintético):

  | Texto | `motivos_cuarentena` en `main` |
  |---|---|
  | `hoy 25 del 10` | `['fecha numerica']` |
  | `hoy, 25 del 10,` | `[]` |
  | `el 31/02,` | `[]` |
  | `, 31-02 ,` | `['fecha numerica']` |
  | `el 31.02.99` | `['fecha numerica']` |
  | `el 31.02.99.` | `[]` |
  | `cuesta 10,5 pips`, `son 1,5 pips`, `1.0850 del 2`, `2.000 mensajes`, `10,5 del 3` | `[]` |

  Así que de los cuatro textos que el encargo manda tapar, los nuevos son el primero, el segundo y
  el CUARTO («el 31.02.99.», que `main` no tapa por el punto final); el de control, que ya se tapa
  hoy, es el TERCERO («, 31-02 ,»). La frase del encargo («los tres primeros nuevos y el tercero,
  de control») se lee así.
- **«hoy, 25 del 10,» no es una fecha imposible**, como piden los tests de
  `test_transcribir_sesion.py` (su docstring, `:5-7`). Es el literal del encargo y el de la línea
  PRIORITARIA de Technical Debt; se usa porque octubre es un mes DEMOSTRADO libre (sonda: «octubre
  libre: True»), así que ningún caso reservado ni oculto cae en él. Se dice en el docstring del test.

### 0.c Los tests de hoy

- **La fecha numérica**: `test_una_fecha_numerica_va_a_cuarentena`
  (`tests/unit/test_transcribir_sesion.py:100-112`, seis textos: «el 31/02 entré», «fue el
  31-02», «el 31.02.99», «el 45 del 13», «el treinta y dos del trece», «el mes 13 fue otro»), y
  `test_los_vecinos_van_tambien_a_cuarentena` (`:127-134`). En `tests/unit/test_cuarentena.py`
  la fecha sale por el `Filtro` y por `fechas_en` (`:597`, `:629`, `:633`, `:649`, `:670`, `:674`,
  siempre «31/02» sin signo detrás).
- **Leen el repositorio real**: `test_5_ningun_mes_con_dias_ocultos_o_reservados_queda_sin_cubrir`
  (`test_cuarentena_por_condicion.py:188-197`, solo recuento), `test_6` y `test_set_suelto...`
  (`:224-227`, `:248-252`), `test_la_lista_blanca_de_la_guardia_no_se_separa_de_la_fuente`
  (`:274-286`), `test_la_fuente_real_valida` (`:299-301`: valida y contiene 2026-02 y 2026-03) y
  `test_abril_agosto_enero_y_el_lenguaje_normal_no_se_filtran`
  (`test_transcribir_sesion.py:88-94`, `{1, 4, 8} <= libres`). `test_la_fuente_es_solo_anadir`
  (`:332-352`) va en un repo temporal. Ninguno enumera los meses reservados: añadir 2025-12 no les
  cambia nada (diciembre no es 1, 4 ni 8; `test_la_fuente_real_valida` usa `<=`), y la lista blanca
  de la guardia (`MESES_DE_DESARROLLO`, `.claude/hooks/guardia.py:243`: 2026-01, -04, -07, -08) no
  tiene diciembre.

### 0.d Quién más depende de `meses_libres` y de la regla

- **`scripts/ficheros_con_ocultos.py`** (`calcular`, `:98-111`) llama a `meses_libres(raiz)`
  (`:103`) y con él: `propuestas_con_ocultos(raiz, libres)` (`:104`; `cuarentena.py:491-515`, que
  aplica `Filtro.motivos` -y por tanto `en_cuarentena`/`motivos_cuarentena`- a los segmentos
  copiados en cada propuesta); `_filtros` (`:51-63`), que por cada transcripción del corpus construye
  `filtro_de(raiz, video, libres)` y CARGA SU CRUDA con ese filtro (`cargar_cruda(carpeta,
  filtro)`, que anota qué segmentos oculta); `lineas_ocultas` (`:66-77`), que lee las cuatro
  `SALIDAS_DE_MEDICIONES` (`cuarentena.py:473-480`) y se queda con las líneas de segmentos ocultos;
  y `_que_copian` (`:80-95`), que lee todos los ficheros de `docs/` seguidos por git (md, txt, yaml,
  yml, json, jsonl) y mira si copian alguna de esas líneas. **Lo que lee**: `knowledge/_proposals/
  pr-*.yaml`, `knowledge/corpus/tramos_no_citables.yaml`, los manifiestos de transcripción, LA CRUDA
  ENTERA de cada transcripción en `data/transcripciones/` (en memoria, sin imprimirla), las cuatro
  salidas de medición y los ficheros de `docs/`. Imprime rutas y recuentos, nunca texto.
- **`test_la_lista_de_la_guardia_es_la_que_se_calcula`** (`tests/unit/test_guardia_claude.py:850-863`)
  exige que `.claude/hooks/ficheros_con_ocultos.txt` sea EXACTAMENTE `texto_de_la_lista(propuestas +
  otros)` de `calcular(RAIZ)`. Corre en cada `make check` con los datos en la máquina, así que **cada
  `make check` de la máquina ya hace esa misma lectura** (en memoria, sin imprimir nada), también el
  de esta rama.
- **`items_que_copian`** (`cuarentena.py:641-666`) no depende de la regla del mes ni de la fecha
  para la evidencia: `kb` la llama solo con `motivos={MOTIVO_TRAMO}` (`retrieval/indice.py:232-237`).
  **`evidencia_a_ocultar`** (`cuarentena.py:568-607`) oculta un ítem solo por tramo no citable o por
  una fecha de `casos_ocultos` en su texto o en los segmentos que pisa, que busca `fechas_en`
  (`:593`, `:596`). La regla del mes (c) y `_RE_FECHA` no ocultan evidencia (sexta orden del
  consultor, 2026-10-01). Lo demás que usa `meses_libres`: `cli.py` (`:435`, `:587`, `:1134`,
  `_kb_indice` en `:1328-1333`) y `scripts/transcribir_sesion.py` (`:655`, `:669-674`).

### 0.e Qué documentos dicen qué meses son libres

- `knowledge/cases/meses_reservados.yaml`, cabecera (`:1-15`): «aqui van SOLO los que no tienen
  casos y tampoco se pueden leer». Diciembre cumple las dos: sigue siendo verdad.
- `docs/validation/CUARENTENA-POR-CONDICION.md:258` («hay 7 meses demostrados libres y se tapan
  5»): informe cerrado, cierto en su fecha. Con diciembre serán 6 y 6 (sonda: 7 libres hoy). No se
  toca (régimen de `docs/validation/`); el informe de esta rama da la cifra nueva.
- `docs/runbooks/MIRAR-EL-MATERIAL.md` y la skill `ingerir-sesion` no nombran meses libres ni
  diciembre. `PROJECT_STATE.md:96` (la línea PRIORITARIA) y `docs/plan/HOJA-DE-RUTA.md:556-565`
  (G.5) describen el hueco: salen o pasan a HECHA en el cierre.
- ADR-0078 (`:39`) y ADR-0079 (`:50`) dan como PRIMER criterio de que julio y enero sean
  construcción que «no está en `knowledge/cases/meses_reservados.yaml`». Ver el hallazgo 3.

### 0.f El barrido y la skill

- **`docs/validation/anexos/SESION-05/barrido_18_31.py`**: `LINEA` (`:13`) casa solo las líneas
  `[mm:ss] texto` de la filtrada (las de `version_filtrada`, `scripts/transcribir_sesion.py:384`;
  los encabezados no); `ALTO` (`:14`) es un entero de 1 o 2 cifras no pegado a una letra, a un
  punto o a una coma por delante (`(?<![\w.,])`), ni a un dígito o a `[.,]dígito` por detrás; el
  bucle (`:20-29`) se queda con las líneas con algún entero de 18 a 31 y las imprime con esos
  enteros cambiados por `[N]`; al final, el recuento (`:30`). **Solo ve dígitos**: no pasa la
  línea por `normalizar` ni por `numeros_a_cifras`, así que «el veinticinco» no sale
  (SESION-05-EXTRACCION.md §11, a7, `:1632`). Y por delante tiene el mismo hueco que `_RE_FECHA`:
  «hoy,25» no sale.
- **La skill** (`.claude/skills/ingerir-sesion/SKILL.md`): el paso 4 (`:89-93`) escribe la filtrada
  y dice que es «lo UNICO que se lee»; el paso 6 (`:96-100`) es donde se LEE («Se localiza a mano
  en la filtrada»). Ninguno manda un barrido antes. El cambio va al paso 6, que es donde se lee.

### 0.g Hallazgos (sorpresas)

1. **El mismo hueco en `fechas_en`.** `_RE_DIA_BARRA_MES` (`cuarentena.py:377`) tiene los mismos
   lookarounds que `_RE_FECHA`, y `fechas_en` (`:380-391`) es lo que usa la EVIDENCIA para ocultar
   un ítem que trae un día de `casos_ocultos` (`evidencia_a_ocultar`, `:593` y `:596`; y
   `Oculto.fecha_vigilada`, `:443`). Medido: `fechas_en("el 31/02")` = `{(2, 31)}`;
   `fechas_en("el 31/02,")` y `fechas_en("el 31/02.")` = `set()`. Un ítem que diga un día reservado
   seguido de coma o punto no se oculta en `kb`. El encargo solo nombra `_RE_FECHA`.
2. **La fase 1 ya mueve la lista de la guardia.** `test_la_lista_de_la_guardia_es_la_que_se_calcula`
   recalcula la lista en cada `make check`; con diciembre tapado, toda propuesta o salida de medición
   con un segmento que diga «diciembre» pasa a oculta, y el `make check` de la fase 1 saldría rojo
   hasta regenerar. La regeneración del encargo está en la fase 2.
3. **La regla nueva promete una salida que el código no tiene.** «Sale de ahí solo con la decisión
   que lo lleva a construcción, escrita en un ADR», pero `problemas_de_meses_reservados` rechaza
   SIEMPRE sacar o cambiar una entrada (0.a), y ADR-0078 y ADR-0079 dan como criterio de
   construcción no estar en el fichero. Si NA:I decide que diciembre es construcción, hoy no hay
   forma de sacarlo sin que `knowledge validate` salga en ERROR, y el mes seguiría tapado en el texto.

### 0.h El auditor del encargo (`auditor-encargo`, 2026-10-28)

Lanzado sobre c0607bd. Resultado: 53 afirmaciones, 34 correctas, 2 incorrectas y 17 con matiz;
7 cosas que el repo pide y el encargo no dice. Lo que añade a 0.g, comprobado después por la sesión:

4. **La regla nueva atrapa agosto.** «Todo mes del que se reciba material del trader entra en
   meses_reservados.yaml el mismo día» alcanza la exportación de agosto ya pedida (Next Action Q,
   `PROJECT_STATE.md:50`): agosto, que es construcción, entraría en el fichero, se taparía en el
   texto, y romperían `test_abril_agosto_enero...` (`{1, 4, 8} <= libres`) y el cruce con la lista
   blanca de la guardia (`test_cuarentena_por_condicion.py:274-286`, agosto en
   `MESES_DE_DESARROLLO`). Y, por el hallazgo 3, ya no saldría.
5. **«hoy, 25 del 10,» es una fecha real**: la de la grabación de v16 (SESION-05-EXTRACCION.md:351,
   «solo dejó a la vista la fecha de la propia grabación»). Octubre es libre, así que no es un día
   reservado; pero choca con «todo test va con texto sintético, sin fechas reales» del encargo y con
   el docstring del fichero de tests («fechas IMPOSIBLES»). «hoy, 45 del 13,» rompe igual en `main`
   (`[]`) y se tapa con la regla nueva (medido por el auditor).
6. **El recuento de evidencia de la fase 2 da 0 por construcción** si solo cambia `_RE_FECHA` y
   diciembre: la evidencia se oculta solo por tramo o por `fechas_en` (0.d), y ninguno cambia.
   Medirlo además exige una segunda lectura de las crudas (`kb` las carga), que el encargo no prevé.
7. **Cerrar G.5 tal cual rompe `test_hoja_de_ruta`**: su «Qué es» dice «NA:I» (`HOJA-DE-RUTA.md:558`)
   y `problemas_b` (`tests/unit/test_hoja_de_ruta.py:139-145`) da «esta HECHA y la letra sigue
   viva». Las líneas del cierre tendrán que escribir la I sin el prefijo `NA:`.
8. Menores: G.5 tiene Refs «—» (la F la nombra PROJECT_STATE); la frase literal de la fase 4 cambia
   la segunda oración del consultor («Las dos letras solo si se vuelven a agotar.»,
   RECORRIDA-CONSTRUCCION.md:1962) y las dos letras no se descartaron, se aplazaron (`:1784`); las
   filtradas hechas son v7-v10, v15 y v16 (v11-v14 sin transcribir); `barrido_dias.py` imprime líneas
   de la filtrada por diseño (enmascaradas), que es la excepción natural a «solo recuentos»; y la
   regla del 2026-10-25 (§2.7, punto 3) hablaba de julio del 18 en adelante.

## PARADA · fase 0 (2026-10-28)

Sin escribir código. Lo que necesito que decidas:

1. **El hueco gemelo en `fechas_en`** (hallazgo 1). (a) **Recomendado:** en esta rama, los mismos
   dos lookarounds en `_RE_DIA_BARRA_MES` (`cuarentena.py:377`), con su test que rompe en `main`
   («el 31/02,» da `{(2, 31)}`), `src/` ya está en el contrato; entonces la evidencia SÍ puede pasar
   de visible a oculta, y su recuento (fase 2) se mide de verdad: `kb` con el código de `main` (clon)
   y con el de la rama, solo recuentos, declarado como segunda lectura de las crudas. (b) Línea de
   Technical Debt y nada más; el recuento de evidencia se da como 0 por construcción.
2. **La regla nueva y la salida de diciembre** (hallazgos 3 y 4). (a) **Recomendado:** la regla se
   acota y dice lo que hay: «todo mes del que se reciba material del trader y que no sea ya de
   construcción por su ADR entra en meses_reservados.yaml el mismo día que se recibe, antes de que el
   consultor decida; hoy el fichero es SOLO AÑADIR sin salida, así que la rama que decida que un mes
   así es construcción construye antes la salida por ADR en `cases/holdout.py`». Y una línea de
   Technical Debt con ese dueño (la rama de NA:I, R5.4). (b) Construir aquí la salida por ADR
   (`cases/holdout.py`, hoy protegido en el contrato; amplía el alcance). (c) No añadir diciembre y
   taparlo de otra forma (no veo una que no sea una lista a mano).
3. **El literal del test** (hallazgo 5). (a) **Recomendado:** «hoy, 45 del 13,» en lugar de «hoy, 25
   del 10,», con la misma rotura en `main`. (b) El literal del encargo, declarado.
4. **El orden de la regeneración** (hallazgo 2). Propuesta: una sola fila en HOLDOUT-EXPOSICIONES,
   ANTES del primer `make check` con diciembre, que declare las tres lecturas de la rama (la que hace
   `test_la_lista_de_la_guardia_es_la_que_se_calcula` en cada `make check`, la regeneración con
   `--escribir` y, si 1(a), los recuentos de `kb`); regenerar tras la fase 1 y otra vez tras la fase
   2, con las condiciones de PARADA del encargo (una ruta que sale, un ítem que pasa de oculto a
   visible) en cada una.
5. Sin decisión, para que lo sepas: el reparto nuevo/control de la fase 2 se escribe como lo medido
   (nuevos el 1.º, 2.º y 4.º; control el 3.º); y las líneas del cierre de G.5 escriben la I sin `NA:`.

## Estado

EN CURSO. PARADA de la fase 0, esperando al consultor.

EN CURSO.
