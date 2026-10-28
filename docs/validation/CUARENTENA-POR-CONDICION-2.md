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
  «el cuarenta y cinco del trece,» es lo mismo que «el 45 del 13,».
- **Medido en el código de `main`** (sonda, texto sintético):

  | Texto | `motivos_cuarentena` en `main` |
  |---|---|
  | el literal del encargo para la coma, sin las comas (una fecha real: §0.g, 5) | `['fecha numerica']` |
  | el mismo literal, con sus comas | `[]` |
  | `el 31/02,` | `[]` |
  | `, 31-02 ,` | `['fecha numerica']` |
  | `el 31.02.99` | `['fecha numerica']` |
  | `el 31.02.99.` | `[]` |
  | `cuesta 10,5 pips`, `son 1,5 pips`, `1.0850 del 2`, `2.000 mensajes`, `10,5 del 3` | `[]` |

  Así que de los cuatro textos que el encargo manda tapar, los nuevos son el primero, el segundo y
  el CUARTO («el 31.02.99.», que `main` no tapa por el punto final); el de control, que ya se tapa
  hoy, es el TERCERO («, 31-02 ,»). La frase del encargo («los tres primeros nuevos y el tercero,
  de control») se lee así.
- **El literal del encargo para la coma no es una fecha imposible**, como piden los tests de
  `test_transcribir_sesion.py` (su docstring, `:5-7`): es una fecha real (§0.g, 5). Se cambió por
  «hoy, 45 del 13,» en los tests, en el comentario de `_RE_FECHA` y en este informe (respuesta del
  consultor a la PARADA de la fase 0, punto 3); el literal del encargo solo queda en las copias
  literales del encargo y de la respuesta.

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
5. **El literal del encargo para la coma es una fecha real**: la de la grabación de v16 (SESION-05-EXTRACCION.md:351,
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

## Respuesta del consultor a la PARADA · fase 0 (2026-10-28)

Dada por Aleks (consultor) el 2026-10-28. Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/cuarentena-por-condicion-2 (2026-10-28). Cópiala tal cual al encargo y al informe, en «Respuesta del consultor a la PARADA · fase 0», con su fecha, en un commit propio antes de seguir.
>
> 1. fechas_en: (a). La condición es la misma que en _RE_FECHA (una coma o un punto forman parte de un número solo con un dígito a cada lado), y una regla se arregla donde se repite, no en un solo sitio. _RE_DIA_BARRA_MES (cuarentena.py:377) lleva los mismos lookarounds que la fase 2, con su test que rompe en main («el 31/02,» da set() en main y {(2, 31)} en la rama) y el de superconjunto ampliado a ella. Antes de escribir, busca en src/, scripts/ y .claude/hooks/ toda regex con (?<![\d.,]) o (?![\d.,]) y lista en el informe lo que encuentres: si sale alguna fuera de cuarentena.py, PARADA. La evidencia que pase de visible a oculta se mide en main y en la rama, solo por recuento, y se declara; si alguna pasa de oculta a visible, PARADA. El contrato no cambia.
>
> 2. La regla nueva: (a). Queda así, en la cabecera de meses_reservados.yaml y en la sección nueva de MIRAR-EL-MATERIAL.md: «Todo mes del que se reciba material del trader y que no sea ya de construcción por su ADR (hoy enero, abril, julio y agosto) entra en meses_reservados.yaml el mismo día que se recibe, antes de que el consultor decida si es construcción o reservado. Hoy un mes no puede salir de este fichero (holdout.py lo niega sin excepción), y ADR-0078 y ADR-0079 exigen que un mes de construcción no esté en él: la rama que decida llevar a construcción un mes de aquí construye antes la salida, con su ADR.» Verifica contra los ADR cuáles son hoy los meses de construcción antes de escribir la lista; si no son esos cuatro, escribe los que digan los ADR y dilo en el informe. Prepara para el cierre: (i) una línea de Technical Debt con eso mismo, dueña la rama de R5.4; (ii) en la hoja de ruta, R5.4 añade a «Qué es»: «si diciembre va a construcción, antes la salida de meses_reservados.yaml con su ADR (hoy no existe)». La salida no se construye aquí: la rama es corta y la decisión de NA:I no está tomada.
>
> 3. El literal: (a) «hoy, 45 del 13,». Ningún literal de los tests nuevos es una fecha real; sustituye «hoy, 25 del 10,» en todo lo que lo nombre (tests, informe, comentario de _RE_FECHA) y deja escrito en el informe que el encargo lo traía y por qué se cambió. La lista corregida: van a cuarentena «hoy, 45 del 13,», «el 31/02,», «el 31.02.99.» (los tres nuevos: en main dan []) y «, 31-02 ,» (de control: ya se tapa en main); no van «cuesta 10,5 pips», «son 1,5 pips», «1.0850 del 2» y «2.000 mensajes».
>
> 4. La regeneración: (a). Una sola fila en HOLDOUT-EXPOSICIONES.md, ANTES del primer make check con diciembre, que declare las tres lecturas: la de cada make check (test_la_lista_de_la_guardia_es_la_que_se_calcula recalcula la lista leyendo las crudas en memoria), la regeneración tras la fase 1 y la regeneración tras la fase 2. Las dos regeneraciones, con scripts/ficheros_con_ocultos.py de main y PARADA en cada una si sale alguna ruta de la lista o algún ítem pasa de oculto a visible. Solo recuentos en el informe.
>
> Sobre lo que no pedía decisión: las líneas del cierre se escriben sin «NA:» donde test_hoja_de_ruta lo exija con la I viva (bien visto), y la negativa de la guardia seguida por la forma que ella proponía queda bien declarada.
>
> Para la orden de cierre, tres hallazgos del consultor que el auditor del consultor no vio y la fase 0 sí: (1) el encargo arreglaba un hueco en una regex sin buscar otras con el mismo hueco; (2) la regla nueva prometía una salida «por ADR» que el código no tiene y contradecía ADR-0078 y ADR-0079 (habría atrapado agosto); (3) el literal del test era una fecha real y el caso de control estaba mal numerado. Lección para el consultor: antes de escribir una regla sobre un fichero, leer cómo se entra y cómo se sale de él en el código, y qué ADR lo nombran; y antes de arreglar una regex, buscar sus copias.
>
> Sigue con las fases 1 a 4 como dice el encargo, con estos cambios. Rama lista para revisión, NO cerrada.

## 1. Fase 1 · Diciembre (2026-10-28)

### 1.a Antes de escribir: las copias del hueco y los meses de construcción

- **Las regex con el hueco** (respuesta, punto 1). Búsqueda en `src/`, `scripts/` y `.claude/hooks/`
  de `(?<![\d.,])` y `(?![\d.,])` (Grep): solo `src/botsito/corpus/cuarentena.py:285`, `:286`,
  `:287` (`_RE_FECHA`) y `:377` (`_RE_DIA_BARRA_MES`). Ampliada a cualquier clase negada con coma
  y punto en cualquier orden: sale además `scripts/a18_buscar.py:71`, que ya usa la forma buena
  (`(?<![a-z0-9])(?<![0-9][.,:])` y `(?![a-z0-9%])(?![.,:][0-9])`: puntuación solo con dígito a cada
  lado), así que no es una copia del hueco. **Ninguna fuera de `cuarentena.py`: sin PARADA.**
- **Los meses de construcción, por sus ADR** (respuesta, punto 2): abril y agosto (ADR-0043:30,
  «construcción = abril y agosto»), julio (ADR-0078, título y `:20`) y enero (ADR-0079, título y
  `:28`; `:59` resume: «ADR-0043 fijó construcción = abril y agosto; ADR-0078 añadió julio»).
  Ningún otro ADR mete un mes («entra en construcci», «pasa a construcci», «construcción = » en
  `docs/adr/`: mayo solo aparece como condición futura, ADR-0043:42 y ADR-0070:122). Son los
  cuatro de la respuesta, y la regla se escribe con ellos.

### 1.b Lo escrito

- `knowledge/cases/meses_reservados.yaml`: la entrada `"2025-12"` con las tres claves de
  `_problemas_de_mes` (`motivo`, `fuente: [ADR-0072, docs/validation/SESION-05-EXTRACCION.md]`,
  `declarado_el: "2026-10-28"`); ADR-0072:55 nombra diciembre entre los backtests que vienen, y
  `_fuente_existe` admite las dos (sonda de la fase 0). En la cabecera, la regla nueva con el texto
  literal de la respuesta, y debajo los ADR de cada mes de construcción y por qué hacía falta.
- `docs/runbooks/MIRAR-EL-MATERIAL.md`: la sección corta nueva al final, «El material recibido: el
  mes entra en meses_reservados.yaml el mismo día», con la misma regla literal y su porqué.
- **Por qué el hueco no lo cubría ninguna de las dos condiciones de `meses_libres`**: (a) mira los
  casos de los repartos, y un mes recibido y fuera del repo no tiene ninguno; (b) mira
  `meses_reservados.yaml`, y nadie lo había anotado. Un mes así pasaba por DEMOSTRADO libre. La
  regla nombra la condición (material recibido y sin ADR de construcción) en vez de añadir un mes a
  mano cada vez que alguien lo nota.
- Con diciembre, los meses demostrados libres pasan de 7 a 6 (sonda y `medir_visibles.py`); se
  tapan 6.

### 1.c El test

`test_diciembre_recibido_y_sin_decidir_se_tapa_en_el_repo_real`
(`tests/unit/test_cuarentena_por_condicion.py`): `motivos_cuarentena("eso fue en diciembre",
meses_libres(RAIZ)) == [MOTIVO_MES]`, contra el repositorio real y con texto sintético.

- **En `main`** (clon `git worktree add --detach C:/cm/main main`, en 0fa9c81, con el fichero de
  tests de la rama copiado dentro; skill `comparar-con-main`):

  ```
  >       assert cu.motivos_cuarentena("eso fue en diciembre", meses_libres(RAIZ)) == [cu.MOTIVO_MES]
  E       AssertionError: assert [] == ['mes']
  E         Right contains one more item: 'mes'
  FAILED tests/unit/test_cuarentena_por_condicion.py::test_diciembre_recibido_y_sin_decidir_se_tapa_en_el_repo_real
  ```
- **En la rama**: `PASSED`. Y en la misma ejecución, tal cual y en verde,
  `test_5_ningun_mes_con_dias_ocultos_o_reservados_queda_sin_cubrir`, `test_la_fuente_real_valida`,
  `test_la_fuente_es_solo_anadir` y los 15 casos de
  `test_abril_agosto_enero_y_el_lenguaje_normal_no_se_filtran` (enero, abril y agosto siguen libres):
  19 passed.

La guardia de Claude Code aceptó como test el del clon (no salió la deuda K).

### 1.d La regeneración tras la fase 1 y los recuentos

Declarada antes en `HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-28). `scripts/ficheros_con_ocultos.py`
es el de `main` (`git diff main --stat -- scripts/ficheros_con_ocultos.py` vacío).

| Qué | `main` | Rama tras la fase 1 |
|---|---|---|
| Rutas en `.claude/hooks/ficheros_con_ocultos.txt` | 14 | 14 (entran 0, salen 0; el fichero no cambia ni un byte) |
| Propuestas con algún segmento oculto | 10 | 10 (entran 0, salen 0) |
| Ítems de evidencia visibles en `kb` | 555 | 555 (a ocultos 0, a visibles 0) |
| Segmentos visibles en `kb` | 5860 | 5860 (a ocultos 0, a visibles 0) |

La línea base de `main` se midió en el árbol de la rama ANTES de tocar nada de la fase 1, con
`git diff main --stat -- src scripts knowledge .claude tests` vacío: el código y los datos eran los
de `main`. Ninguna ruta sale de la lista y ningún ítem pasa de oculto a visible: sin PARADA.

## PARADA 2 · La guardia no deja correr en el clon de main los tests de la fase 2 (deuda K), 2026-10-28

**Lo hecho de la fase 2, SIN COMMITEAR** (en el árbol de trabajo):

- `src/botsito/corpus/cuarentena.py`: `_ANTES = (?<!\d)(?<!\d[.,])` y `_DESPUES = (?!\d)(?![.,]\d)`,
  con la condición escrita en su comentario, en las tres primeras alternativas de `_RE_FECHA` y en
  `_RE_DIA_BARRA_MES`; «mes N» y `_RE_DIA_NUMERO` sin tocar.
- **Un desvío, medido**: con los mismos lookarounds, `_RE_DIA_BARRA_MES.findall` NO era superconjunto
  de `main`: la batería del test de superconjunto dio 432 textos en los que la rama perdía una fecha
  que `main` sacaba (con una fecha imposible, `,1/31-2`: el borde nuevo deja casar `1/31`, que se
  come el principio de `31-2`, la que `main` sacaba; los ejemplos de esta PARADA se cambiaron tras el
  revisor, B1, por fechas imposibles). `_RE_FECHA.search`
  sí era superconjunto (0 textos). Arreglo mínimo: `_RE_DIA_BARRA_MES` va dentro de un lookahead,
  `(?=...)`, para que `findall` vea también las candidatas que se solapan; solo la usa `fechas_en`.
  Con eso, 0 pérdidas.
- `tests/unit/test_transcribir_sesion.py`: `test_una_fecha_pegada_a_una_coma_o_un_punto_va_a_cuarentena`
  (las tres nuevas y la de control), `test_un_numero_con_decimales_no_es_una_fecha` (las cuatro del
  encargo y tres que SOLO la condición del dígito a cada lado deja fuera, hoy «1,5 del 13», «entre
  1.45/1.46», «de 10,5-13,5» tras el revisor, B1; las cuatro del encargo no las taparía ningún borde, porque no tienen
  separador de fecha), `test_fechas_en_ve_la_fecha_pegada_a_una_coma_o_un_punto`,
  `test_la_coma_y_el_punto_rotos_a_proposito_en_los_dos_sentidos` (con el `_RE_FECHA` y el
  `_RE_DIA_BARRA_MES` de `main` copiados como literales, las nuevas no se tapan; con un borde que
  solo mire el dígito, los decimales serían fechas) y `test_la_rama_no_tapa_menos_que_main` (139.392
  textos sintéticos). **En la rama: 20 passed.**

**La negativa.** En el clon `C:/cm/main` (0fa9c81), con `tests/unit/test_transcribir_sesion.py` de la
rama copiado dentro, `uv run pytest ... -k "pegada or decimales or fechas_en_ve or rotos_a_proposito
or no_tapa_menos"` da:

```
GUARDIA (.claude/hooks/guardia.py) bloquea: el codigo nombra la carpeta \., que contiene material
protegido, y no se puede decidir que abrira dentro.
Como reescribirlo: rutas LITERALES de ficheros que se puedan leer, o la CLI del proyecto.
```

El mismo fichero corre en el repo real (arriba): la guardia no lee como test el del clon y analiza
sus literales de regex (`\.`) como rutas. Es la deuda K (`PROJECT_STATE.md`, Next Action K). El de
diciembre (fase 1) sí corrió en el clon porque su fichero no lleva ese literal. La forma que propone
la guardia no aplica, y la regla de la rama dice «PARADA, sin otra vía».

**Lo que necesito que decidas:**

1. (a) **Recomendado:** que valga como «rompe en main» lo que ya corre en el repo real: el test (1)
   de `test_la_coma_y_el_punto_rotos_a_proposito_en_los_dos_sentidos`, que aplica a los textos
   nuevos las regex de `main` copiadas como literales (con su commit y líneas de origen), más la
   sonda de la fase 0 (§0.b), que midió esos textos con el código de `main` (salvo «hoy, 45 del 13,»,
   que midió el auditor: `[]`). Y si lo autorizas, la sonda (`sonda_fase0.py`, sin regex literales)
   corrida en el clon con los literales corregidos, como segunda medida en `main`. (b) Arreglar antes
   la deuda K en su rama y volver aquí. (c) Otra que digas.
2. El desvío del lookahead en `_RE_DIA_BARRA_MES`: lo doy por bueno salvo que digas otra cosa; es lo
   que exige el superconjunto que pediste (punto 1 de tu respuesta).

Mientras tanto no commiteo la fase 2 ni sigo con la regeneración, las fases 3 y 4 ni el cierre.

## Respuesta del consultor a la PARADA 2 (2026-10-28)

Dada por Aleks (consultor) el 2026-10-28. Copiada tal cual:

> Respuesta del consultor a la PARADA 2 de trabajo/cuarentena-por-condicion-2 (2026-10-28). Cópiala tal cual al encargo y al informe, en «Respuesta del consultor a la PARADA 2», con su fecha, en el commit de la fase 2.
>
> 1. Cómo demostrar que rompen en main: (a) y la segunda medida en el clon, las dos.
>    - La prueba de «rompe en main» es la sonda de la fase 0 repetida en C:/cm/main sobre todos los textos nuevos de los tests (los de _RE_FECHA, los de _RE_DIA_BARRA_MES y los de la fase 3 si aplica), porque mide el código real de main y no una copia. Su salida, literal, en el informe, junto a la de la rama. La guardia la deja pasar porque el guion no lleva el literal que dispara el falso positivo: no es una vía nueva para rodear la negativa, es la misma sonda de la fase 0, y así se declara.
>    - El test con las regex de main copiadas literalmente, con su commit y sus líneas de origen, se queda en el repo como guardia de regresión del superconjunto, no como prueba de que rompe en main. Dilo así en su docstring.
>    - Desviación de G.5 («Hecho cuando: test que rompe en main»), declarada en el informe: se demuestra con la sonda sobre main en el clon, porque la guardia niega los ficheros de test en el clon (deuda K).
>    - Para el cierre, una línea que se añade a K en la Next Action, con la medida: la guardia niega en el clon de comparar-con-main un fichero de test porque «el código nombra la carpeta .», un falso positivo que en el repo real no salta. Escribe en el informe qué literal lo dispara (fichero:línea) y la frase exacta de la guardia.
>
> 2. El lookahead de _RE_DIA_BARRA_MES: aprobado. Condiciones: (i) el test de superconjunto cubre también fechas_en (todo par (mes, día) que main saca, la rama lo saca), con 0 pérdidas; (ii) cuenta, sobre la misma batería sintética, cuántos textos dan en la rama fechas que main no da (solapes como «1/1-12»), y escríbelo; es el lado seguro, pero se declara; (iii) un comentario encima de la regex con la condición y el porqué (findall no ve fechas solapadas sin el lookahead); (iv) entra en la lista de desviaciones del informe.
>
> Después: commit de la fase 2 con su make check sellado, la regeneración tras la fase 2 con scripts/ficheros_con_ocultos.py de main (PARADA si sale alguna ruta o algún ítem pasa de oculto a visible; solo recuentos), y las fases 3 y 4 y el cierre de la rama como dice el encargo. Al terminar, borra el clon C:/cm/main con la skill comparar-con-main, como ella diga.
>
> Rama lista para revisión, NO cerrada.

## 2. Fase 2 · La coma y el punto (2026-10-28)

### 2.a Lo escrito

- `src/botsito/corpus/cuarentena.py`: `_ANTES = (?<!\d)(?<!\d[.,])` y `_DESPUES = (?!\d)(?![.,]\d)`,
  con la condición en su comentario («una coma o un punto forman parte de un numero solo cuando
  tienen un digito a cada lado. Por eso «10,5» y «1.0850» no son fechas y «hoy, 45 del 13,» y «el
  31/02,» si»), en las tres primeras alternativas de `_RE_FECHA` y en `_RE_DIA_BARRA_MES`; «mes N»
  y `_RE_DIA_NUMERO` sin tocar. `_RE_DIA_BARRA_MES`, además, dentro de un lookahead (2.d).
- `tests/unit/test_transcribir_sesion.py`, junto a `test_una_fecha_numerica_va_a_cuarentena`: los
  cinco tests de 2.b. Cambios en ellos respecto a la PARADA 2: el docstring del de superconjunto
  dice que es guardia de regresión y no la prueba de «rompe en main»; el superconjunto cubre
  `fechas_en` entera (todo par (mes, día) que `main` saca); y, tras el revisor (B1), la batería solo
  guarda los textos sin ninguna fecha posible (`_sin_fechas_posibles`: todo par de números sueltos
  unido por un separador tiene el mes fuera de 1-12 o más días que el mes) y sus asserts solo dan
  recuentos: 73.008 textos de 210.912.

### 2.b Rompe en main: la sonda sobre el código real de `main` y la de la rama

Respuesta a la PARADA 2, punto 1: la prueba es la sonda de la fase 0 repetida (`sonda_fase2.py`,
scratchpad, fuera del repo) en el clon `C:/cm/main` (0fa9c81) y en la rama, sobre todos los textos
nuevos de los tests. La guardia la deja pasar porque el guion no lleva el literal que dispara el falso
positivo (2.e): no es una vía nueva para rodear la negativa, es la misma sonda de la fase 0. La fase
3 no aplica: `scripts/barrido_dias.py` no existe en `main`. Salidas literales:

**`main`** (`cd C:/cm/main && uv run python .../sonda_fase2.py .../sonda2-main.json`):

```
codigo de: C:\cm\main\src\botsito\corpus\cuarentena.py
diciembre: []
motivos 'hoy, 45 del 13,' []
motivos 'el 31/02,' []
motivos 'el 31.02.99.' []
motivos ', 31-02 ,' ['fecha numerica']
motivos 'cuesta 10,5 pips' []
motivos 'son 1,5 pips' []
motivos '1.0850 del 2' []
motivos '2.000 mensajes' []
motivos '1,5 del 13' []
motivos 'entre 1.45/1.46' []
motivos 'de 10,5-13,5' []
fechas_en 'el 31/02' [(2, 31)]
fechas_en 'el 31/02,' []
fechas_en 'el 31/02.' []
fechas_en 'entre 1.45/1.46' []
fechas_en ',1/31-2' [(2, 31)]
bateria: 73008 textos; 17203 con fecha numerica; 1284 con alguna fecha de fechas_en
```

**Rama** (la misma orden en el repo):

```
codigo de: C:\Users\USER\Desktop\Bot v3\src\botsito\corpus\cuarentena.py
diciembre: ['mes']
motivos 'hoy, 45 del 13,' ['fecha numerica']
motivos 'el 31/02,' ['fecha numerica']
motivos 'el 31.02.99.' ['fecha numerica']
motivos ', 31-02 ,' ['fecha numerica']
motivos 'cuesta 10,5 pips' []
motivos 'son 1,5 pips' []
motivos '1.0850 del 2' []
motivos '2.000 mensajes' []
motivos '1,5 del 13' []
motivos 'entre 1.45/1.46' []
motivos 'de 10,5-13,5' []
fechas_en 'el 31/02' [(2, 31)]
fechas_en 'el 31/02,' [(2, 31)]
fechas_en 'el 31/02.' [(2, 31)]
fechas_en 'entre 1.45/1.46' []
fechas_en ',1/31-2' [(2, 31)]
bateria: 73008 textos; 25487 con fecha numerica; 1902 con alguna fecha de fechas_en
```

(Las dos salidas, de la sonda repetida tras el revisor, B1, con la batería sin fechas posibles y los
decimales nuevos; la primera pasada, con la batería de 151.008 textos, dio lo mismo en los textos
comunes: 0 pérdidas.)

Así: las tres nuevas («hoy, 45 del 13,», «el 31/02,», «el 31.02.99.») dan `[]` en `main` y
`['fecha numerica']` en la rama; la de control se tapa en los dos; los siete números con decimales no
se tapan en ninguno; `fechas_en("el 31/02,")` da `[]` en `main` y `[(2, 31)]` en la rama.

**Los tests, en la rama** (`uv run pytest -rA tests/unit/test_transcribir_sesion.py -k ...`): PASSED
`test_una_fecha_pegada_a_una_coma_o_un_punto_va_a_cuarentena` (4 casos),
`test_un_numero_con_decimales_no_es_una_fecha` (7), `test_fechas_en_ve_la_fecha_pegada_a_una_coma_o_un_punto`,
`test_la_coma_y_el_punto_rotos_a_proposito_en_los_dos_sentidos` y `test_la_rama_no_tapa_menos_que_main`;
y los 6 de `test_una_fecha_numerica_va_a_cuarentena`, tal cual. Los dos sentidos rotos a propósito,
dentro del test: (1) con el `_RE_FECHA` y el `_RE_DIA_BARRA_MES` de `main` copiados como literales,
las nuevas no se tapan y `fechas_en` no saca «el 31/02,»; (2) con un borde que solo mire el dígito,
los tres decimales («1,5 del 13», «entre 1.45/1.46», «de 10,5-13,5») se taparían. Las cuatro del
encargo que no son fechas no las taparía ningún borde (no tienen separador de fecha): por eso se
añadieron esas tres, que son las que solo la condición nueva deja fuera.

### 2.c La rama no tapa menos que `main`

Por construcción: en cada posición, `(?<![\d.,])` exige que el carácter anterior no sea dígito, ni
coma, ni punto; `(?<!\d)(?<!\d[.,])` solo exige que no sea dígito y que los dos anteriores no sean
dígito+coma o dígito+punto, lo que el primero ya impide. Lo mismo hacia delante. El cuerpo de la
regex no cambia, así que todo `search` que casa con el borde de `main` casa con el de la rama.
Para `findall` no basta (2.d). Medido sobre la batería del test, 73.008 textos sin ninguna fecha
posible (`cruzar_sondas.py`, con las salidas del código real de los dos lados):

```
textos: 73008
fecha numerica: main 17203, rama 25487; main tapa y la rama no: 0; la rama tapa y main no: 8284
fechas_en: textos en que main saca un par que la rama no: 0; en que la rama saca un par que main no: 618 (de ellos, 0 en que main ya sacaba otro: solapes)
```

`test_la_rama_no_tapa_menos_que_main` fija lo mismo como guardia de regresión, y solo da recuentos si
falla. Con la primera batería (151.008 textos, con fechas posibles: B1) el cruce dio también 0
pérdidas, 8430 textos más tapados y 2031 con pares nuevos, 324 de ellos solapes.

### 2.d Desviación: el lookahead de `_RE_DIA_BARRA_MES`

Con solo los lookarounds nuevos, `findall` perdía fechas: la primera versión del test de superconjunto
dio 432 textos en los que la rama no sacaba un par que `main` sí. `findall` no vuelve atrás: con el
borde nuevo, en «,1/31-2», «1/31» (que `main` rechazaba por la coma de delante) se come el principio
de «31-2», y se pierde el par (2, 31) que `main` sacaba. La regex va dentro de un lookahead,
`(?=...)`, para que `findall` vea también las candidatas que se solapan; solo la usa `fechas_en`.
Medido con un mutante sin el lookahead (`mutante_lookahead.py`, scratchpad): `,1/31-2` da
`[('1', '31')]` sin él y `[('1', '31'), ('31', '2')]` con él; y sobre la batería del test el mutante
pierde pares de `main` en 192 textos, la rama en 0. Aprobado por el consultor (PARADA 2, punto 2),
con sus condiciones: (i) el superconjunto cubre `fechas_en`, con 0 pérdidas (2.c); (ii) sobre la
batería del test, la rama saca pares que `main` no en 618 textos, ninguno de ellos un solape con otro
par de `main` (en la primera batería, con fechas posibles, 2031 y 324): es el lado seguro (más
evidencia puede ocultarse, nunca menos); el solape tiene además su literal en el test, «,1/31-2»;
(iii) el comentario encima de la regex dice la condición y el porqué; (iv) entra en la lista de
desviaciones (§5).

### 2.e La negativa de la guardia en el clon (deuda K)

- La frase exacta: «GUARDIA (.claude/hooks/guardia.py) bloquea: el codigo nombra la carpeta \., que
  contiene material protegido, y no se puede decidir que abrira dentro.»
- Lo que la dispara: la constante de texto `"\."` que `ast` saca del f-string de
  `RE_FECHA_MAIN` en `tests/unit/test_transcribir_sesion.py:133` (`:131` en la copia que se llevó al
  clon): el trozo entre `{_NUM_MAIN}` y `{_NUM_MAIN}` de `rf"|(?<![\d.,]){_NUM_MAIN}\.{_NUM_MAIN}\.\d{{2,4}}(?![\d.,])"`.
  `analizar_codigo` (`.claude/hooks/guardia.py:3780-3815`) mira cada literal como ruta
  (`_literales`, `:3818-3830`); en Windows `\.` es la raíz de la unidad, un directorio con material
  protegido (`:3799-3808`). En el repo real el fichero no se analiza porque la guardia lo reconoce
  como test; en el clon no (deuda K).
- **Desviación de G.5** («Hecho cuando: los dos casos tienen su test que rompe en main y pasa en la
  rama»): la coma y el punto se demuestran con la sonda sobre `main` en el clon (2.b), porque la
  guardia niega los ficheros de test en el clon. Diciembre sí con su test en el clon (§1.c).

### 2.f La regeneración tras la fase 2 y los recuentos

Antes del commit, `uv run python scripts/ficheros_con_ocultos.py` (comprobación, el guion de `main`)
da «OK: .claude/hooks/ficheros_con_ocultos.txt coincide» con el código de la fase 2. La regeneración
con `--escribir`, tras el commit (§2.g). `medir_visibles.py` con el código de la rama:

| Qué | `main` | Rama tras la fase 2 |
|---|---|---|
| Propuestas con algún segmento oculto | 10 | 10 (entran 0, salen 0) |
| Ítems de evidencia visibles en `kb` | 555 | 555 (a ocultos 0, a visibles 0) |
| Segmentos visibles en `kb` | 5860 | 5850 (a ocultos 10, a visibles 0) |

Diez segmentos de las crudas pasan a ocultos (fechas pegadas a una coma o un punto, y sus vecinos);
ninguno pasa de oculto a visible, y ningún ítem de evidencia cambia: sin PARADA.

### 2.g La regeneración tras la fase 2

Tras el commit de la fase 2 (bed6968), `uv run python scripts/ficheros_con_ocultos.py --escribir`
(el guion de `main`): «propuestas con segmentos ocultos: 10», «salidas de medicion con lineas
ocultas, y ficheros que las copian: 4», «OK: 14 ficheros». `git status --short` vacío: el fichero
no cambia ni un byte. **14 rutas antes y 14 después; entran 0, salen 0.** Sin PARADA.

## 3. Fase 3 · El barrido ancho en la skill (2026-10-28)

- **`scripts/barrido_dias.py`** (nuevo): recibe la filtrada y el rango (`--desde`, `--hasta`; por
  defecto 18 y 31); de cada línea `[mm:ss] texto` (los encabezados no se barren, como en
  `barrido_18_31.py`) pasa el texto por `normalizar` y `numeros_a_cifras` de
  `botsito.corpus.cuarentena` y, si tiene un entero suelto dentro del rango, imprime la marca y la
  línea con ese número cambiado por `[N]`; al final, el recuento. El entero suelto: `ENTERO =
  (?<!\w){_ANTES}(\d{1,2}){_DESPUES}`, con `_ANTES` y `_DESPUES` IMPORTADOS de
  `botsito.corpus.cuarentena` (tras el revisor, A2: la primera versión los copiaba a mano), es
  decir la condición de la fase 2 (coma o punto solo con dígito a cada lado), más «no pegado a una
  letra» (el código S25 no es un día), que es lo que ya hacía `barrido_18_31.py` (desviación, §5).
  Nunca imprime un número DEL RANGO; sí imprime la línea de la filtrada, normalizada, con los demás
  números a la vista (un mes en cifras, un día por debajo de `--desde`): es su propósito, y la
  excepción a «solo recuentos» (§0.h, 8); por eso el docstring y la skill dicen que el rango cubre
  todos los días fuera de construcción del mes que se barre (tras el revisor, B4).
  `barrido_18_31.py` queda en su anexo tal cual.
- **`tests/unit/test_barrido_dias.py`** (nuevo), con una filtrada SINTÉTICA en una carpeta temporal,
  sin fechas reales (días sueltos o con el mes 13). En la rama, 5 passed:
  `test_el_dia_en_digitos_y_en_letra_sale_con_el_numero_enmascarado` («el 25 del 13» y «el
  veinticinco» salen como `el [N] ...`; «hoy, 31,» sale como `hoy, [N],`; recuento 3),
  `test_fuera_del_rango_un_precio_y_un_codigo_no_salen` (el 5, «1,25», «S25» y los encabezados no
  salen), `test_la_salida_nunca_trae_el_numero`, `test_el_rango_se_fija_por_argumento` y
  `test_roto_a_proposito_en_los_dos_sentidos`: (1) sin `numeros_a_cifras` (como
  `barrido_18_31.py`) el día en letra no sale; (2) sin la condición del dígito a cada lado, «1,25»
  saldría como `1,[N]`; y (3) el lookbehind de `barrido_18_31.py` no ve «hoy,31» y el nuevo sí.
  Rompe en `main` no aplica: el guion no existe allí.
- **La skill** `.claude/skills/ingerir-sesion/SKILL.md`, paso 6 (donde se lee la filtrada; el paso
  4 la escribe, §0.f). `git diff main -- .claude/skills/ingerir-sesion/SKILL.md`, entero:

  ```diff
  @@ -93,7 +93,12 @@ Read de la filtrada y de fotogramas localizados, Write/Edit para `fuentes.yaml`,
      (v7: `3718889`). Desde ese commit `evidence propose --check` y `evidence new` rechazan citarlos.
   5. **Fotogramas.** `uv run botsito corpus frames extract --video <vN>`; puerta:
      `uv run botsito corpus frames check` (0 huecos, 0 extra).
  -6. **Extraccion por pregunta.** La deteccion automatica («pregunta» + codigo ... «fin de pregunta»)
  +6. **Extraccion por pregunta.** Antes de leer o releer cualquier filtrada se pasa
  +   `uv run python scripts/barrido_dias.py <filtrada>` con el rango que fije el encargo de la ingesta
  +   (`--desde`, `--hasta`; por defecto 18 a 31): ve los dias en digitos y en letra, y los imprime
  +   enmascarados. Si sale una linea que sea un dia fuera de construccion del mes que nombra, PARADA
  +   sin copiarla (regla del consultor del 2026-10-25, `SESION-05-EXTRACCION.md` §2.7, punto 3).
  +   La deteccion automatica («pregunta» + codigo ... «fin de pregunta»)
      dio 0 en v7 y en v9, y no se afloja (`SESION-DE-PREGUNTAS.md`). Se localiza a mano en la
      filtrada, por los codigos sueltos o el texto leido de la pregunta; la cita es el literal de la
      filtrada con su `mm:ss`, y el hablante se atribuye por contexto y se declara en `revisado_por`.
  ```

  Solo cambia ese paso. La regla del 2026-10-25 hablaba de julio del 18 en adelante; la skill la
  dice para cualquier mes, como manda el encargo (§0.h, 8).

## 4. Fase 4 · La regla de letras (2026-10-28)

En `docs/runbooks/DECISIONES-DE-PROCESO.md`, «Decisions and Rationale», tras la del 2026-10-21 y con
su formato, la entrada «2026-10-27 · La letra de una entrada nueva de la Next Action»: dice que nace
aquí y no viene de la mudanza de PROJECT_STATE; la frase literal del encargo; el origen (las dos
secciones de RECORRIDA-CONSTRUCCION.md, `:1752` y `:1952`, punto 1 en `:1962`; y la Z, con su
registro HECHA anterior en `docs/state/HISTORIA.md:7644`); el problema; la alternativa; ACTIVE.
Dos matices del auditor (§0.h, 8), escritos en la propia entrada: la segunda oración del consultor era
«Las dos letras solo si se vuelven a agotar.», y las dos letras no se descartaron del todo: se
dejaron para cuando se vuelvan a agotar. Ningún test fija esa sección (`grep DECISIONES-DE-PROCESO
tests/`: solo una mención en un docstring de `tests/contract/test_tramos_fuente.py`).

## 5. Desviaciones

1. **El lookahead de `_RE_DIA_BARRA_MES`** (§2.d), aprobado en la respuesta a la PARADA 2, punto 2.
2. **«Rompe en main» de la coma y el punto, por la sonda y no por el test** (§2.b, §2.e), por la
   deuda K: desviación del «Hecho cuando» de G.5, ordenada en la respuesta a la PARADA 2, punto 1.
3. **El literal del test**: «hoy, 45 del 13,» en lugar del del encargo, que es una fecha real
   (§0.g-h, respuesta a la PARADA de la fase 0, punto 3).
4. **`_RE_DIA_BARRA_MES` también cambia**, no solo `_RE_FECHA` (respuesta a la PARADA de la fase 0,
   punto 1).
5. **Tres textos más que no son fechas** («1,5 del 13», «entre 1.45/1.46», «de 10,5-13,5»), porque
   los cuatro del encargo no los taparía ningún borde (§2.b).
8. **`ENTERO` del barrido añade «no pegado a una letra»** (`(?<!\w)`) a la condición de la fase 2
   que manda el encargo, como hacía `barrido_18_31.py`: el código S25 no es un día (§3; revisor,
   B3).
6. **`tests/unit/test_barrido_dias.py`**, un fichero de tests que el encargo no nombra, para el guion
   nuevo de la fase 3 (en el contrato desde la apertura).
7. **La regeneración tras la fase 1 además de la de la fase 2**, y los recuentos de `kb`, declarados
   en una sola fila de HOLDOUT (respuesta a la PARADA de la fase 0, puntos 1 y 4).

## 6. Las líneas del cierre, preparadas y SIN aplicar

Simuladas en memoria (`simular_cierre.py` y `lineas_cierre.py`, en el scratchpad) sobre el
`PROJECT_STATE.md`, la hoja de ruta y la HISTORIA de la rama: las cuatro comprobaciones de
`test_hoja_de_ruta` (`problemas_a`, `_b`, `_c`, `_d`) dan `[]`. `wc -c` del `PROJECT_STATE.md`
resultante: **22.889 bytes** (hoy, en la rama, 23.056). El cierre de `RITUAL.md` cambia además
Current Branch, Current Feature, Stable Main State y Last Stable Commit, que no se simulan.

**`PROJECT_STATE.md`, Next Action:**

- F, entera: «F. La preparación de la sesión 6 (R4.2); R6a y Z en los huecos.»
- K, se añade al final: «Y la de CUARENTENA-POR-CONDICION-2.md §2.e: en el clon de comparar-con-main
  la guardia niega un fichero de test porque «el codigo nombra la carpeta \.» (la constante `\.` de
  un f-string de regex, que en Windows es la raíz de la unidad), un falso positivo que en el repo real
  no salta.»

**`PROJECT_STATE.md`, Technical Debt:** salen la línea PRIORITARIA de la cuarentena y la de la skill
ingerir-sesion; entra:

- «Hoy un mes no puede salir de `knowledge/cases/meses_reservados.yaml` (holdout.py lo niega sin
  excepción), y ADR-0078 y ADR-0079 exigen que un mes de construcción no esté en él: la rama que
  decida llevar a construcción un mes de aquí construye antes la salida, con su ADR. Dueña: la rama
  de R5.4, diciembre (CUARENTENA-POR-CONDICION-2.md, respuesta del consultor a la PARADA de la fase
  0, punto 2).»

**`docs/plan/HOJA-DE-RUTA.md`:**

- G.5, «Qué es»: «NA:I sin decidir» pasa a «la I sin decidir» (con la I viva, `test_hoja_de_ruta`
  daría «esta HECHA y la letra sigue viva»); y tras «Hecho cuando» entra «- **Estado:** HECHA
  (`stable/F38h-cuarentena-por-condicion-2`; docs/validation/CUARENTENA-POR-CONDICION-2.md: la coma
  y el punto, por la sonda sobre el código de main en un clon, §2.b y §2.e).» (el tag, el siguiente
  de la serie; lo fija la orden de cierre).
- R5.4, «Qué es», se añade al final: «; si diciembre va a construcción, antes la salida de
  meses_reservados.yaml con su ADR (hoy no existe).»

**Para la fila de la rama en `ERRORES-RECURRENTES.md`** (la escribe el cierre): los tres hallazgos
del consultor de su respuesta a la PARADA de la fase 0 y su lección, más lo que diga la orden de
cierre.

## 7. Comandos, literales

De la sesión, en orden (los de solo lectura de código con Read y Grep no se listan):

1. Base: `git fetch origin`; `git status --short`; `git rev-parse --short main`;
   `git rev-parse main origin/main`; `git rev-parse "stable/F38g-recorrida-construccion^{commit}" main^1`;
   `git ls-remote --tags origin stable/F38g-recorrida-construccion`; `git branch --list`;
   `git ls-remote --heads origin "fix/*"`; `gh api repos/{owner}/{repo}/commits/0fa9c81b5b26d47f884860ff4530eb0a37eb6b02/check-runs --jq ...`;
   `git checkout -b trabajo/cuarentena-por-condicion-2`; `git ls-remote --heads origin`.
2. Apertura: `printf '\n# Archivo 50 · ...' >> docs/state/HISTORIA.md`; `git show main:PROJECT_STATE.md >> docs/state/HISTORIA.md`;
   `git add ...`; `uv run botsito state check`; `uv run python scripts/contrato_rama.py`;
   `make check > make-check.log 2>&1` (en segundo plano, cada vez); `git commit -q -F <fichero>`.
3. Fase 0: `uv run python <scratchpad>/sonda_fase0.py` (texto sintético).
4. Fase 1: `uv run python <scratchpad>/fila_holdout.py "<repo>"`; `git diff main --stat -- src scripts knowledge .claude tests`;
   `uv run python <scratchpad>/medir_visibles.py "<repo>" <scratchpad>/visibles-main.json`;
   `uv run pytest -p no:cacheprovider -rA <tests> -k "..."`; `git worktree add --detach C:/cm/main main`;
   `cp <test de la rama> C:/cm/main/tests/unit/...`; `cd C:/cm/main && uv run pytest ...`;
   `cp .claude/hooks/ficheros_con_ocultos.txt <scratchpad>/lista-main.txt`;
   `git diff main --stat -- scripts/ficheros_con_ocultos.py`; `uv run python scripts/ficheros_con_ocultos.py`;
   `uv run python scripts/ficheros_con_ocultos.py --escribir`; `git diff --stat -- .claude/hooks/ficheros_con_ocultos.txt`;
   `uv run python <scratchpad>/medir_visibles.py ... visibles-f1.json`; `uv run python <scratchpad>/comparar_visibles.py ...`;
   `uv run botsito knowledge validate`.
5. Fase 2: `uv run pytest ...`; `cp ...` y `cd C:/cm/main && uv run pytest ...` (negado, PARADA 2);
   `cd C:/cm/main && uv run python <scratchpad>/sonda_fase2.py <scratchpad>/sonda2-main.json`;
   `uv run python <scratchpad>/sonda_fase2.py <scratchpad>/sonda2-rama.json`;
   `uv run python <scratchpad>/cruzar_sondas.py ...`; `uv run python scripts/ficheros_con_ocultos.py`;
   `uv run python <scratchpad>/medir_visibles.py ... visibles-f2.json`; `uv run ruff check ...`;
   `uv run ruff format --check ...`; `uv run mypy`; tras el commit, `uv run python scripts/ficheros_con_ocultos.py --escribir`.
6. Fase 3: `cp <scratchpad>/barrido_dias.py scripts/`; `cp <scratchpad>/test_barrido_dias.py tests/unit/`;
   `uv run ruff format scripts/barrido_dias.py tests/unit/test_barrido_dias.py`; `uv run pytest -rA tests/unit/test_barrido_dias.py`;
   `git diff main -- .claude/skills/ingerir-sesion/SKILL.md`.
7. Cierre preparado: `uv run python <scratchpad>/simular_cierre.py "<repo>"`; `wc -c ...`.

**Negativas de la guardia, todas seguidas por la forma que ella propone** (regla de la rama):
`c=$(git log ...)` (variable de entorno fuera de la lista); `git add ... && uv run botsito state check`;
`git log ... | xargs grep` (se hizo con la herramienta Grep); `pytest ... | sed ...` (se quitó el
`sed`); `cp ... && cd C:/cm/main && uv run pytest` (en dos llamadas); `git diff ... ; uv run python
scripts/ficheros_con_ocultos.py` (en dos); `uv run --project ...` (desde el repo); `git status --short;
uv run botsito state check` (en dos); `git status --short; cmp ...` (se usó `git status` solo). La
única que no tenía forma propuesta, la del clon, fue la PARADA 2.

## 8. El encargo, punto por punto

| # | Requisito (encargo y respuestas) | Estado | Evidencia |
|---|---|---|---|
| 1 | Base verificada con git (main, tag, que no hay otra rama) | Hecho | cabecera |
| 2 | Abrir con `abrir-rama`: encargo tal cual, contrato, Archivo en HISTORIA | Hecho | c0607bd |
| 3 | Fase 0: holdout.py (a), (b), `_problemas_de_mes`, validate, origen del régimen (no ADR) | Hecho | §0.a |
| 4 | Fase 0: `_RE_FECHA`, por qué excluye coma y punto, `numeros_a_cifras` | Hecho, con matiz (el comentario no habla de «10,5») | §0.b |
| 5 | Fase 0: tests de la fecha y los que leen el repo real | Hecho | §0.c |
| 6 | Fase 0: dependientes de `meses_libres` y de la regla; qué lee el guion de la lista | Hecho | §0.d |
| 7 | Fase 0: documentos que dicen qué meses son libres | Hecho | §0.e |
| 8 | Fase 0: `barrido_18_31.py` línea a línea y la skill | Hecho | §0.f |
| 9 | Fase 0: PARADA si pide más | Hecho (PARADA de la fase 0) | §0.g-h, respuesta |
| 10 | Copiar las respuestas tal cual, en commits propios | Hecho | a21edf8; la de la PARADA 2, en bed6968 |
| 11 | F1: entrada 2025-12 con tres claves, motivo, fuentes, fecha; trailer `Fuente: ADR-0072` | Hecho | f5bc65b |
| 12 | F1: test de diciembre que rompe en main y pasa en la rama; los cuatro siguen | Hecho | §1.c |
| 13 | F1: la regla nueva, literal, en la cabecera y en MIRAR-EL-MATERIAL; meses de construcción verificados | Hecho | §1.a-b |
| 14 | F1: por qué el hueco no lo cubre ninguna condición | Hecho | §1.b |
| 15 | Resp. 1: buscar copias del hueco en src/, scripts/, .claude/hooks/ | Hecho (solo en `cuarentena.py`) | §1.a |
| 16 | F2: lookarounds nuevos en las tres primeras alternativas; «mes N» y `_RE_DIA_NUMERO` intactos | Hecho | §2.a |
| 17 | Resp. 1: los mismos en `_RE_DIA_BARRA_MES`, test que rompe en main | Hecho de otra forma (lookahead, aprobado; rompe en main por la sonda) | §2.b, §2.d |
| 18 | F2: tests de las cuatro que se tapan y las cuatro que no, rotos en los dos sentidos | Hecho, con tres de más | §2.b |
| 19 | Resp. 3: «hoy, 45 del 13,» en tests, informe y comentario | Hecho | §0.b, §2.a |
| 20 | F2: superconjunto, escrito y con test; ampliado a `fechas_en` con 0 pérdidas | Hecho | §2.c |
| 21 | Resp. PARADA 2: rompe en main por la sonda en el clon, salidas literales | Hecho | §2.b |
| 22 | Resp. PARADA 2: el test de regex copiadas, como guardia de regresión en su docstring | Hecho | `test_la_rama_no_tapa_menos_que_main` |
| 23 | Resp. PARADA 2: desviación de G.5 declarada; literal y frase de la guardia | Hecho | §2.e |
| 24 | Resp. PARADA 2: solapes contados | Hecho (sobre la batería del test, 618 textos y 0 solapes; en la primera, 2031 y 324; el solape, con su literal) | §2.c-d |
| 25 | Fila de HOLDOUT antes de leer, con las tres (y cuatro) lecturas | Hecho | §1.d, §9 |
| 26 | Regeneración tras la fase 1 y tras la fase 2, solo recuentos, PARADA si sale algo | Hecho (14 → 14 las dos veces) | §1.d, §2.g |
| 27 | Ítems de evidencia y propuestas de visibles a ocultos, por recuento | Hecho (0 y 0; 10 segmentos) | §1.d, §2.f |
| 28 | F3: `scripts/barrido_dias.py` (normalizar, numeros_a_cifras, [N], misma condición) | Hecho, con «no pegado a una letra» (§5, 8) | §3 |
| 29 | F3: tests sintéticos rotos en los dos sentidos | Hecho | §3 |
| 30 | F3: la skill, solo ese paso, con el diff | Hecho | §3 |
| 31 | F4: la entrada en DECISIONES-DE-PROCESO con su frase literal, origen, problema, alternativa, ACTIVE | Hecho | §4 |
| 32 | Contrato con lo que toca la rama | Hecho (con `test_barrido_dias.py`, declarado) | `contrato.yaml` |
| 33 | Líneas del cierre preparadas sin aplicar; `test_hoja_de_ruta` y `wc -c` | Hecho (22.889 bytes) | §6 |
| 34 | Resp. 2: línea de Technical Debt (R5.4) y la frase en R5.4 | Hecho (preparadas) | §6 |
| 35 | Resp. PARADA 2: la línea que se añade a K | Hecho (preparada) | §6 |
| 36 | `make check` sellado, push a `fix/`, CI de Linux | Hecho | §10 |
| 37 | Revisor con el informe terminado y su alcance; su informe pegado | Hecho (lanzado sobre 1086d7d; pegado tras su informe, con lo que se hizo) | §11, §12 |
| 38 | Borrar el clon `C:/cm/main` con `comparar-con-main` | Hecho (tras el revisor) | §12 |
| 39 | QUÉ NO CAMBIA: motor, spec, ambigüedades, feedback, evidencia, casos, repartos, corpus, guardia, settings | Hecho (`git diff --stat main...HEAD`, §10) | §10 |

## 9. Exposiciones del día

Una fila en `docs/validation/HOLDOUT-EXPOSICIONES.md` (2026-10-28), escrita ANTES del primer `make
check` con diciembre y antes de ejecutar nada que leyera material: las cuatro lecturas en memoria (la
de cada `make check`, las dos regeneraciones y los recuentos de `kb` con el código de `main` y el de
la rama). Fuera de eso, ninguna lectura de material: ni libros, ni imágenes, ni fotogramas, ni
filtradas; las sondas y los tests, con texto sintético. El auditor del encargo declaró lo suyo en su
informe (§0.h): una llamada a `meses_libres` con texto sintético y un `git ls-files knowledge/cases`
que solo listó rutas de README.

## 10. Sello, CI de Linux y lo que no cambia

- **`make check`** de cada commit, en verde con su línea `SELLO` (el de 9567a8c: 2990 passed,
  `SELLO: make check en verde sobre el arbol 294323dc...`). El primer intento de la fase 2 salió en
  rojo por dos líneas de más de 100 caracteres (ruff); se partieron y se volvió a sellar.
- **CI de Linux**: `git push origin trabajo/cuarentena-por-condicion-2:refs/heads/fix/cuarentena-por-condicion-2`;
  run **40731298628** sobre 9567a8c449bdfbed14ca03fc388ad4cff33c15ca (por la API de check-runs con
  el sha literal; consultado con `gh run view` suelto, con una espera `sleep` en segundo plano entre
  medias). Resultado: un solo fallo, el esperado, `test_state_check_ok_on_real_repo` («PROJECT_STATE
  declara la rama 'trabajo/cuarentena-por-condicion-2'; la rama actual es
  'fix/cuarentena-por-condicion-2'»); `1 failed, 2943 passed, 46 skipped`. El run del último commit
  de la rama se anota al final, tras el revisor.
- **Lo que no cambia**: `git diff --stat main...HEAD` da 15 ficheros, todos del contrato
  (`.claude/skills/ingerir-sesion/SKILL.md`, `PROJECT_STATE.md`, `contrato.yaml`, el encargo,
  `DECISIONES-DE-PROCESO.md`, `MIRAR-EL-MATERIAL.md`, `HISTORIA.md`, este informe,
  `HOLDOUT-EXPOSICIONES.md`, `meses_reservados.yaml`, `scripts/barrido_dias.py`,
  `src/botsito/corpus/cuarentena.py` y los tres ficheros de tests). Ni el motor, ni la spec, ni las
  ambigüedades, el feedback, la evidencia, los casos, los repartos, el corpus, `fuentes.yaml`,
  `libros.yaml`, `SESIONES_EN_CUARENTENA`, los tramos no citables, `.claude/hooks/guardia.py` ni
  `.claude/settings.json`. `.claude/hooks/ficheros_con_ocultos.txt` no aparece porque las dos
  regeneraciones lo dejaron igual. `uv run python scripts/contrato_rama.py`: «15 ficheros dentro
  del contrato».
- **El clon `C:/cm/main`** se deja hasta después del revisor y se borra con `comparar-con-main`
  (respuesta a la PARADA 2); se anota al final.

## 11. Informe del revisor (subagente `revisor`, 2026-10-28), pegado tal cual

Lanzado sobre 9567a8c con este informe terminado y estadiado (luego commiteado como 1086d7d), con
los cinco alcances del encargo. Sin retiradas: no cita nada de un tramo no citable.

> ## Informe del revisor · trabajo/cuarentena-por-condicion-2 · 2026-10-28
>
> La rama no tiene ningún hallazgo que bloquee. Hay tres que importan y tres menores. Lo más serio es B1: la batería del test de superconjunto y un literal de los tests nuevos usan fechas posibles de meses reservados (diciembre y septiembre), y eso choca con «sin fechas reales».
>
> Base: `merge-base main HEAD` = 0fa9c81. Seis commits (c0607bd..9567a8c). El informe está estadiado sin commitear y lo he leído del árbol de trabajo. `git diff --stat main...HEAD` da 15 ficheros.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | importa | La sección nueva de MIRAR-EL-MATERIAL cita mal de dónde sale la fecha. Dice «Diciembre de 2025 fue el caso (recibido el 2026-10-09, SESION-05-EXTRACCION.md §2.7)», pero §2.7 no habla de diciembre. | `docs/runbooks/MIRAR-EL-MATERIAL.md:133`. `grep -ni diciembre` en SESION-05-EXTRACCION.md da las líneas 41, 308, 1066-1073, 1148, 1229, 1417 y 1535 en adelante; ninguna cae en §2.7 (líneas 329-378). La fecha está en §3.5 (`:1073`, «NA:I dice que el backtest llegó el 2026-10-09 sin vídeo») y en `PROJECT_STATE.md:42` (NA:I). El hueco de diciembre en `meses_libres` está en §11, a4 (`:1535`). |
> | A2 | menor | `scripts/barrido_dias.py` crea una tercera copia escrita a mano de la regla «coma o punto solo con un dígito a cada lado», en vez de usar `_ANTES` y `_DESPUES` de `cuarentena.py`. Ningún test ata las dos copias, así que si la regla cambia en `cuarentena.py`, el barrido no la sigue. Es la misma lección del consultor: «antes de arreglar una regex, buscar sus copias». | `scripts/barrido_dias.py:30` frente a `src/botsito/corpus/cuarentena.py:289-290` |
>
> Comprobado sin hallazgos:
> - **Contrato.** `uv run python scripts/contrato_rama.py`: «CONTRATO: 15 ficheros dentro del contrato de trabajo/cuarentena-por-condicion-2 (riesgo alto, artefacto docs/validation/CUARENTENA-POR-CONDICION-2.md, tramo 'Carril: guardias y deuda', 4 comprobaciones para el revisor)».
> - **Tests del contrato.** `pytest` de `test_cuarentena_por_condicion`, `test_transcribir_sesion`, `test_cuarentena` y `test_barrido_dias`: **233 passed**, exit 0. `test_guardia_claude.py` no lo ejecuté porque lee las crudas (ver «Lo que no pude comprobar»).
> - **El árbol sellado.** `git rev-parse 9567a8c^{tree}` = 294323dc7948…, el mismo que el SELLO que cita el informe (§10).
> - **CI.** `gh run view 40731298628`: headSha 9567a8c449bd…, rama `fix/cuarentena-por-condicion-2`, `failure`. En `--log-failed` solo falla `test_state_check_ok_on_real_repo`, con «1 failed, 2943 passed, 46 skipped».
> - **Trailer `Fuente:`.** El único commit que toca `knowledge/cases/` es f5bc65b, y lleva «Fuente: ADR-0072» en el cuerpo. El ADR existe (`docs/adr/0072-…`) y su línea 55 nombra diciembre.
> - **Holdout y material.** Nada toca `knowledge/cases/holdout/`. Hay fila del 2026-10-28 en HOLDOUT-EXPOSICIONES, y solo añade (+1/-0).
> - **Regímenes de cambio.**
>   - Nada cambia en `evidence/`, `feedback/`, `manifests/`, `corpus/` ni `libros.yaml`.
>   - `meses_reservados.yaml` y `HISTORIA.md` solo añaden: +19/-0 y +167/-0 (`git diff --numstat`).
> - **Ambigüedades, ADR y `cita` de la spec.** La rama no los toca.
> - **Informes cerrados.** No se modifica ninguno de `docs/validation/`; HOLDOUT-EXPOSICIONES es un registro y solo gana una fila.
> - **`git diff --check main...HEAD`** limpio. **Fin de línea:** LF en los ficheros nuevos y en los cambiados que comprobé (`git ls-files --eol`).
> - **Tres citas del informe, contrastadas con su fuente:**
>   - `ADR-0043:30` («construcción = abril y agosto»).
>   - `ADR-0078:39` y `ADR-0079:50` («no está en meses_reservados.yaml»).
>   - `CUARENTENA-POR-CONDICION.md:208` («Régimen: solo añadir…»).
>   - `RECORRIDA-CONSTRUCCION.md:1752`, `:1952` y `:1962`.
>   - `HISTORIA.md:7644` («# Next Action HECHA · Z · …»).
>   - `guardia.py:3780`, `:3805-3807` y `:3818-3830`.
>   - Todas cuadran.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 42 hechos y 2 hechos de otra forma (aprobados), 2 parciales, 1 no hecho (pendiente por diseño).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base verificada con git, sin otra rama | Hecho | informe :8-20; merge-base 0fa9c81 |
> | 2 | abrir-rama: encargo, contrato y Archivo 50 | Hecho | c0607bd; HISTORIA +167 «# Archivo 50 · …0fa9c81» |
> | 3-8 | Fase 0: holdout.py, `_RE_FECHA`, tests, dependientes, documentos, barrido y skill | Hecho | §0.a-f; líneas comprobadas (`holdout.py:556,557,575,582,620,667`; `guardia.py:243`) |
> | 9 | PARADA de la fase 0 y su respuesta copiada tal cual, en commit propio | Hecho | `diff` encargo:68-82 frente a informe:254-268, idénticos; a21edf8 |
> | 10 | Entrada 2025-12 con sus tres claves, el motivo, `fuente: [ADR-0072, SESION-05-EXTRACCION.md]` y `declarado_el` | Hecho | diff de `meses_reservados.yaml` |
> | 11 | Trailer `Fuente: ADR-0072` | Hecho | f5bc65b |
> | 12 | Test de diciembre: rompe en main y pasa en la rama | Hecho | reproducido: en el clon `C:/cm/main` (HEAD 0fa9c81, solo tests modificados) `motivos_cuarentena('eso fue en diciembre', meses_libres(...))` da `[]`; en la rama, `['mes']` |
> | 13 | test_5, fuente_real_valida, fuente_es_solo_anadir y abril_agosto_enero siguen en verde | Hecho | 233 passed |
> | 14 | Regla literal en la cabecera y en MIRAR-EL-MATERIAL | Hecho | texto idéntico al de la respuesta, punto 2 (cabecera :17-24; MIRAR :123-128) |
> | 15 | Meses de construcción comprobados en los ADR | Hecho | §1.a |
> | 16 | Por qué ninguna condición cubría el hueco | Hecho | §1.b |
> | 17 | Buscar copias de `(?<![\d.,])` en src/, scripts/ y .claude/hooks/ | Hecho | mi Grep: solo el comentario de `cuarentena.py:287` |
> | 18 | Lookarounds nuevos en las tres alternativas; «mes N» y `_RE_DIA_NUMERO` intactos | Hecho | diff de `cuarentena.py` |
> | 19 | La condición escrita en el comentario | Hecho | `cuarentena.py:284-288` |
> | 20 | `_RE_DIA_BARRA_MES` con el mismo borde | Hecho de otra forma (lookahead aprobado en la PARADA 2, punto 2) | `cuarentena.py:384-390`; §2.d; §5.1 |
> | 21 | Tests: cuatro que se tapan y cuatro que no | Hecho, con tres de más (declarado) | test_transcribir_sesion.py:115-146; §5.5 |
> | 22 | «hoy, 45 del 13,» rompe en main | Hecho de otra forma (por la sonda; desviación ordenada) | reproducido en el clon: `[[], [], [], ['fecha numerica'], [], [], []]`; en la rama, las cuatro dan `['fecha numerica']` y los decimales `[]` |
> | 23 | Test de superconjunto con las regex de main literales y su origen | Hecho | :126-135, copia idéntica a `git show 0fa9c81:…:283-290,377` |
> | 24-27 | PARADA 2, punto 2 (i) a (iv) | Hecho | :206-216; §2.c-d; comentario :384-389; §5.1 |
> | 28 | Docstring: «guardia de regresión», no la prueba de rompe en main | Hecho | :199-203 |
> | 29 | Literal que dispara la guardia (fichero:línea) y su frase | Hecho | `test_transcribir_sesion.py:133` (y `:131` en la copia del clon, comprobado con grep) |
> | 30 | Fila de HOLDOUT con las lecturas | Hecho | diff de HOLDOUT; el orden temporal, ver «no pude» |
> | 31 | Dos regeneraciones con el guion de main; ninguna ruta sale | Hecho | `ficheros_con_ocultos.txt` no aparece en el diff; 14 rutas sin comentario (`grep -vc`); el guion, sin diff |
> | 32 | Recuentos de evidencia, propuestas y segmentos | Hecho (no reproducible por mí) | §1.d, §2.f |
> | 33 | `scripts/barrido_dias.py` | Hecho (con «no pegado a letra» añadido, ver B3) | :29-49 |
> | 34 | Tests del barrido, rotos en los dos sentidos | Hecho | `test_barrido_dias.py`, 5 passed |
> | 35 | `barrido_18_31.py` intacto | Hecho | no está en el diff |
> | 36 | Skill: solo el paso de lectura, con su diff | Hecho | `git diff`: un solo hunk (@@ -93,7 +93,12), paso 6, +6/-1 |
> | 37 | Fase 4: frase literal, origen, problema, alternativa y ACTIVE | Hecho | `DECISIONES-DE-PROCESO.md:29`; la frase, idéntica a la del encargo |
> | 38 | Contrato | Hecho | contrato_rama.py |
> | 39 | Líneas del cierre, `test_hoja_de_ruta` y `wc -c` | Hecho | reproducido en memoria (sin la escritura final de `simular_cierre.py`): `a: [] b: [] c: [] d: []`, 22889 bytes, hoy 23056 |
> | 40 | Respuesta 2 (i) y (ii) preparadas | Hecho | `lineas_cierre.py:26-30, 52-59` |
> | 41 | Línea de K preparada | Hecho | `lineas_cierre.py:7-13` |
> | 42 | make check sellado | Hecho para 9567a8c | árbol 294323dc |
> | 43 | Push a `fix/` y CI | Hecho | run 40731298628 |
> | 44 | Revisor y su informe pegado | Parcial (en curso) | — |
> | 45 | Borrar `C:/cm/main` | No hecho (pendiente, por orden del llamador) | el clon existe, HEAD 0fa9c81 |
> | 46 | «Sin fechas reales» en los tests nuevos | Parcial | B1 |
> | 47 | QUÉ NO CAMBIA | Hecho | `diff --name-status`: nada de motor, spec, guardia, settings, corpus ni evidencia |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | importa | Los datos de prueba nuevos incluyen fechas posibles de meses reservados, contra el encargo («Todo test va con texto sintético, sin fechas reales»), la respuesta del consultor a la PARADA de la fase 0, punto 3 («Ningún literal de los tests nuevos es una fecha real»), y el docstring del propio fichero (`:5-7`: «Ningun dato de prueba lleva una fecha real de un dia reservado … fechas IMPOSIBLES»). Concretamente:<br>• La batería combina 1, 9, 12 y 31 con «/», «-», « de » y « del » (`:177`, `:182`): salen «12/9», «1/12», «31 de 12»… (septiembre tiene días reservados y diciembre es reservado entero).<br>• `:216` afirma `{(12, 1)}` para «,1/1-12»: el 1 de diciembre.<br>Si el test falla, pytest imprime esas listas (`assert menos == []`, `:210`; `assert perdidas == []`, `:212`).<br>Atenúa la gravedad que «1/1-12» lo propuso el propio consultor en la PARADA 2, punto 2 (ii).<br>Arreglo posible: los números de mes de la batería, solo de construcción (1, 4, 7, 8) o imposibles, y «,1/1-4» en lugar de «,1/1-12»; lo he medido a mano y conserva el solape. | `tests/unit/test_transcribir_sesion.py:5-7`, `:177`, `:180`, `:210`, `:212`, `:216` |
> | B2 | importa | La tabla «El encargo, punto por punto» da por hechas dos cosas que no lo están:<br>• La fila 38 dice «Borrar el clon `C:/cm/main` · Hecho · §10», pero el propio §10 dice que se deja hasta después del revisor, y el clon sigue en pie (`cd C:/cm/main && git rev-parse HEAD` = 0fa9c81…; `git status` muestra los dos tests modificados).<br>• La fila 37 dice «su informe pegado · Hecho», y todavía no está pegado. | `docs/validation/CUARENTENA-POR-CONDICION-2.md:760-761` frente a `:796-797` y `:801-802` |
> | B3 | menor | `ENTERO` añade `(?<!\w)` (no pegado a una letra) a la condición de la fase 2 que manda el encargo. Está explicado en §3, pero no figura en §5 «Desviaciones», y la fila 28 dice «Hecho» a secas. | `scripts/barrido_dias.py:30`; informe §3 :573-576, §5, §8 fila 28 |
> | B4 | menor | La skill dice que el barrido imprime los días «enmascarados», pero el guion imprime la línea entera normalizada: solo enmascara los enteros que caen dentro del rango, y los demás números de esa línea (un mes en cifras, un día por debajo de `--desde`) salen tal cual. Es lo que pide el encargo, pero conviene escribirlo en la skill y en el docstring: el rango tiene que cubrir todos los días que no son de construcción del mes que se barre. | `scripts/barrido_dias.py:45-48`; `SKILL.md:96-100` |
>
> **Los alcances del encargo:**
> 1. **Que los tests rompen de verdad en main.**
>    - Diciembre: reproducido en el clon (`[]`) y en la rama (`['mes']`).
>    - La coma y el punto: reproducido con el código real de main en el clon (`cu.__file__` = `C:\cm\main\src\…`): las tres nuevas dan `[]`, la de control `['fecha numerica']`, `fechas_en('el 31/02,')` da `[]` y `fechas_en(',1/1-12')` da `[(12, 1)]`. En la rama: `[(2, 31)]`.
>    - Coincide con §2.b.
> 2. **Que nada imprime un mes reservado, una fecha real ni un caso.**
>    - Las sondas imprimen texto sintético y recuentos. `medir_visibles.py`, `comparar_visibles.py` y `cruzar_sondas.py` imprimen solo recuentos.
>    - Si el test de diciembre falla, pytest no imprime el conjunto de meses libres: la explicación propia de la comparación de listas sustituye los «where». Solo enseña el literal «diciembre», que ya está en el yaml commiteado.
>    - `barrido_dias.py` imprime líneas de la filtrada enmascaradas, por diseño del encargo. Está declarado en el docstring, en §3 y en §0.h punto 8 (ver B4).
>    - Queda abierto B1.
> 3. **Que la rama no tapa menos que main.**
>    - Lo demuestro: `(?<!\d)(?<!\d[.,])` acepta toda posición que acepta `(?<![\d.,])`, y lo mismo hacia delante. En cada posición de `_RE_DIA_BARRA_MES` el cuerpo deja una sola elección de grupos, así que, con el lookahead, `findall` de la rama ve todas las posiciones en que casa main y saca los mismos pares.
>    - `_RE_FECHA` solo se usa con `.search` (`cuarentena.py:317`); `_RE_DIA_BARRA_MES` solo en `fechas_en` (`:402`).
>    - El test pasa.
> 4. **La regeneración.** Está declarada en la fila del 2026-10-28. El fichero no cambia (14 rutas, sin diff) y el guion es el de main.
> 5. **El diff de la skill.** Un solo hunk, en el paso 6.
>
> **Las líneas del cierre (§6), puestas a prueba.** Ejecuté `simular_cierre.py` en memoria contra las funciones de `test_hoja_de_ruta`, sin su última línea, que escribe. Resultado: `a: [] b: [] c: [] d: []` y 22889 bytes. Las cuatro sustituciones casan una sola vez. Z está viva en la Next Action (`PROJECT_STATE.md:58`), así que «R6a y Z en los huecos» vale.
>
> ### Lo que no pude comprobar
> - **El sello del commit del informe y la línea `PICO DE MEMORIA`.** `make-check.log` está a medio escribir: su línea 3 es «SELLO: borrado el anterior…».
> - **El CI del commit del informe.** Todavía no existe.
> - **`test_guardia_claude.py` (la comprobación 3 del contrato).** No lo ejecuté porque `test_la_lista_de_la_guardia_es_la_que_se_calcula` lee las crudas. Su evidencia: el run 40731298628 pasa salvo state check, y el fichero de la lista no aparece en el diff.
> - **Los recuentos de `kb`** (555 ítems de evidencia; segmentos de 5860 a 5850) y las salidas de las regeneraciones. Para reproducirlos habría que leer las crudas. Solo tengo las salidas que cita el informe y los JSON del scratchpad.
> - **Que la fila de HOLDOUT se escribiera antes de la primera lectura.** Git no lo dice. Lo que hay son las fechas de modificación del scratchpad, que encajan: `fila_holdout.py` 10:39, `visibles-main.json` 10:40.
> - **La negativa de la guardia en el clon (deuda K).** Reproducirla exige ejecutar pytest en el clon con el fichero copiado. Comprobé el literal en `C:/cm/main/tests/unit/test_transcribir_sesion.py:131` y el texto del mensaje en `guardia.py:3805-3807`.
> - **Que la guardia deje pasar `barrido_dias.py` sobre una filtrada real.** Habría que tocar material.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
> 2. Read de: el encargo, `contrato.yaml`, el informe (enteros); `scripts/barrido_dias.py`, `tests/unit/test_barrido_dias.py`, `test_cuarentena_por_condicion.py:180-309`, `test_transcribir_sesion.py:1-30, 128-135`, `SKILL.md:70-114`, `guardia.py:3780-3831`; y los guiones del scratchpad (`sonda_fase2.py`, `cruzar_sondas.py`, `medir_visibles.py`, `comparar_visibles.py`, `simular_cierre.py`, `lineas_cierre.py`, `fila_holdout.py`).
> 3. `uv run python scripts/contrato_rama.py`
> 4. `git diff main...HEAD -- src/botsito/corpus/cuarentena.py knowledge/cases/meses_reservados.yaml`
> 5. Grep de `_RE_DIA_BARRA_MES|_RE_FECHA\b|_ANTES|_DESPUES` en `*.py`
> 6. `git diff main...HEAD -- tests/unit/test_transcribir_sesion.py tests/unit/test_cuarentena_por_condicion.py`
> 7. `sed -n '1,35p' docs/validation/anexos/SESION-05/barrido_18_31.py`
> 8. `git show 0fa9c81:src/botsito/corpus/cuarentena.py | sed -n '283,290p;377,392p'`
> 9. `git diff main...HEAD --` de HOLDOUT-EXPOSICIONES, DECISIONES-DE-PROCESO, MIRAR-EL-MATERIAL, SKILL.md y PROJECT_STATE
> 10. `git log --format='%h%n%B' main..HEAD -- knowledge/spec knowledge/cases`; `git diff --name-status main...HEAD`; `git log … -- HOLDOUT/meses_reservados/test`
> 11. `git diff --numstat main...HEAD`; `ls docs/adr | grep …`; `sed -n '50,58p' docs/adr/0072*.md`
> 12. Grep de `2026-10-09|diciembre` en SESION-05-EXTRACCION.md; `grep -n '^#'` y `sed` de sus líneas 300-312 y 1064-1074; Grep en PROJECT_STATE; `sed -n '42p' PROJECT_STATE.md`
> 13. `sed` de ADR-0043:30, ADR-0078:39, ADR-0079:50,59, RECORRIDA:1752,1784,1952,1960-1963 y HISTORIA:7644
> 14. `git worktree list…` y `git -C C:/cm/main …`: negados por `solo_lectura.py`. Los sustituí por `cd C:/cm/main && git rev-parse HEAD`, `git status --short`.
> 15. `ls -la <scratchpad>`
> 16. `cd "C:/Users/USER/Desktop/Bot v3" && uv run python -c "<exec de simular_cierre.py sin su última línea de escritura>"`
> 17. `grep -n '^[A-Z]\. ' PROJECT_STATE.md`; `grep -n 'def \|stable\|HECHA' tests/unit/test_hoja_de_ruta.py`
> 18. Grep de `data/transcripciones|cargar_cruda|…` en los cuatro tests; `grep -n 'def repo\|tmp_path\|RAIZ' tests/unit/test_cuarentena.py`
> 19. `uv run pytest -p no:cacheprovider` sobre los cuatro ficheros de test (`-q`, y después `-rA` con `tail`): 233 passed, exit=0
> 20. `ls -la make-check.log && grep -nE 'SELLO|PICO DE MEMORIA|passed|failed' make-check.log`
> 21. `git rev-parse 9567a8c^{tree} bed6968^{tree} f5bc65b^{tree}`
> 22. `gh run view 40731298628 --json headSha,conclusion,status,headBranch`; `gh run view 40731298628 --log-failed | grep …`
> 23. `git diff main...HEAD -- docs/state/HISTORIA.md | sed -n '1,12p'`; `git show main:PROJECT_STATE.md | wc -l`
> 24. `diff <(sed encargo 68-82) <(sed informe 254-268)` y lo mismo con 88-100 frente a 400-412: IGUAL1 e IGUAL2
> 25. Un bucle `for` negado por la guardia; lo sustituí por `git log --stat --format='== %h %s' main..HEAD`
> 26. `cd C:/cm/main && uv run --frozen python -c "<motivos y fechas_en de los textos sintéticos>"` y lo mismo en la rama; `meses_libres` con «eso fue en diciembre» en el clon y en la rama
> 27. `grep -n 'NUM_MAIN}\\\.' C:/cm/main/tests/unit/test_transcribir_sesion.py`; grep de las funciones de la guardia
> 28. Grep de lookarounds con `\d`, coma y punto en `{src,scripts,.claude}/**/*.py`, en tres variantes
> 29. `ls data/transcripciones/` (solo nombres)
> 30. `grep -vc '^#\|^$' .claude/hooks/ficheros_con_ocultos.txt`; `git diff main...HEAD --stat -- .claude/hooks/ficheros_con_ocultos.txt | wc -l`
> 31. `git diff --check main...HEAD`; `git ls-files --eol` de cinco ficheros. Un `grep $'\r'` fue negado por la guardia; lo sustituí por `ls-files --eol`.
> 32. `grep -n` de las líneas de los hallazgos en el test, en MIRAR-EL-MATERIAL y en el informe; `grep -n` de las funciones de `holdout.py`; `sed -n '204,209p;258p' docs/validation/CUARENTENA-POR-CONDICION.md`
>
> No leí ninguna transcripción, filtrada, fotograma, libro ni nada del holdout, y no ejecuté nada que los lea.

## 12. Lo que se hizo con los hallazgos del revisor

- **A1 (importa), arreglado.** `docs/runbooks/MIRAR-EL-MATERIAL.md`: la fecha de recepción cita la
  entrada I de la Next Action y SESION-05-EXTRACCION.md §3.5 (`:1062`, «Para cerrar»); el hueco,
  §11, a4.
- **A2 (menor), arreglado.** `scripts/barrido_dias.py` importa `_ANTES` y `_DESPUES` de
  `botsito.corpus.cuarentena` en lugar de copiarlos: la condición vive en un solo sitio, y los tests
  del barrido siguen en verde (5 passed).
- **B1 (importa), arreglado.** En `tests/unit/test_transcribir_sesion.py`: la batería guarda solo
  los textos sin ninguna fecha posible (`_sin_fechas_posibles`, con `DIAS_DEL_MES`: todo par de
  números sueltos unidos por un separador, también coma y espacio, tiene el mes fuera de 1-12 o más
  días que el mes; 73.008 de 210.912 textos); los asserts del superconjunto dan solo recuentos; el
  solape va con «,1/31-2» (el 31 de febrero) en lugar del ejemplo de la PARADA 2; y los tres
  decimales añadidos pasan a «1,5 del 13», «entre 1.45/1.46», «de 10,5-13,5». Medido después: la
  batería sigue detectando la falta del lookahead (un mutante sin él pierde pares de `main` en 192
  textos; la rama, en 0); la sonda, repetida en el clon y en la rama con esa batería (§2.b, §2.c),
  da 0 pérdidas. El comentario del test ya no nombra el literal de la fecha real. Los cuatro textos
  que no son fechas que dicta el encargo se quedan tal cual. Los pasajes del informe con los
  ejemplos viejos se rehicieron (§2.a-d, la PARADA 2, §5 y la tabla).
- **B2 (importa), arreglado.** Filas 37 y 38 de §8 al día: el revisor está pegado aquí y el clon,
  borrado (abajo).
- **B3 (menor), arreglado.** «No pegado a una letra» entra en §5 como desviación 8, y la fila 28
  lo dice.
- **B4 (menor), arreglado.** El docstring de `barrido_dias.py` y el paso 6 de la skill dicen que solo
  se enmascaran los números DEL RANGO y que el rango cubre todos los días fuera de construcción del
  mes que se barre. El diff de la skill contra `main` sigue siendo un solo hunk, en el paso 6.
- **El clon `C:/cm/main`**, borrado con `comparar-con-main`: `git worktree remove --force
  C:/cm/main` (con `--force` porque llevaba los dos ficheros de tests de la rama copiados) y
  `git worktree prune`. Después, `git worktree list` sin el clon; `git branch --list`, `main` y la
  rama; `git tag -l`, 141, como antes; `git ls-remote --heads origin`, `main` y
  `fix/cuarentena-por-condicion-2` (el push de la rama). Queda un worktree de otra sesión
  (`.../2ea2c3d2-.../scratchpad/wt-ci`, e7df30b), que esta rama no creó y no toca.
- Lo que el revisor no pudo comprobar se queda así: la CI del último commit, abajo.
- Las tres negativas que el revisor declara en sus comandos 14, 25 y 31 (`solo_lectura.py` y la
  guardia) las rodeó él con otra forma; se dejan dichas aquí para el consultor.

## 13. El último commit y su CI

Los arreglos de §12 van en un commit sellado con `make check`, que se empuja a
`fix/cuarentena-por-condicion-2` con la misma orden de §10. Su run (el que cuenta, el del último
commit) se da en el mensaje final a Aleks con su número y resultado; anotarlo aquí exigiría otro
commit sin CI. El de 9567a8c es el 40731298628 (§10).

## Orden de cierre (2026-10-28)

Dada por Aleks (consultor) el 2026-10-28. Copiada tal cual:

> Modelo: Opus · Esfuerzo: medio
>
> Orden de cierre de trabajo/cuarentena-por-condicion-2 (2026-10-28). Copia esta orden tal cual al final del encargo y del informe, en «Orden de cierre (2026-10-28)», en un commit propio antes del commit del contrato.
>
> Ciérrala con la skill cerrar-rama, siguiendo docs/runbooks/RITUAL.md con todas sus puertas. Tag: stable/F38h-cuarentena-por-condicion-2. Antes del tag, comprueba que stable/F38h-* no existe ni en local ni en origin.
>
> En el commit del contrato (chore(cierre): sale el contrato y entra el registro en HISTORIA):
> - Sale contrato.yaml; entra el registro del cierre en HISTORIA con stable/F38h-cuarentena-por-condicion-2^{commit} en lugar del sha.
> - Todas las líneas de CUARENTENA-POR-CONDICION-2.md §6, tal cual: en la Next Action, F entera y la frase nueva al final de K; en Technical Debt, salen la línea PRIORITARIA de la cuarentena y la de la skill ingerir-sesion, y entra la de la salida de meses_reservados.yaml (dueña, la rama de R5.4); en la hoja de ruta, G.5 con «la I sin decidir» y su «Estado: HECHA» con el tag de arriba, y R5.4 con su añadido. Ninguna letra sale de la Next Action (G.5 no tenía letra propia: la llevaba F), así que no hay registro «# Next Action HECHA».
> - ERRORES-RECURRENTES, la fila de la rama. Del consultor, tres hallazgos de su encargo que vio la fase 0 y no su auditor: (1) arreglaba un hueco en una regex sin buscar sus copias (_RE_DIA_BARRA_MES); (2) la regla nueva prometía una salida «por ADR» que el código no tiene y contradecía ADR-0078 y ADR-0079 (habría atrapado agosto); (3) el literal del test era una fecha real y el caso de control estaba mal numerado. Lección para el consultor: antes de escribir una regla sobre un fichero, leer cómo se entra y cómo se sale de él en el código y qué ADR lo nombran; antes de arreglar una regex, buscar sus copias. De la sesión, lo que el revisor encontró (B1: la batería del superconjunto tenía fechas posibles de meses reservados; A1, la cita de MIRAR-EL-MATERIAL). Y un hallazgo menor del consultor sobre el revisor: en sus comandos 14, 25 y 31 sustituyó por su cuenta tres comandos negados (git -C por solo_lectura.py, un bucle for y un grep $'\r' por la guardia) en vez de declararlos y seguir sin ellos; eran de solo lectura y no tocaron material, pero la regla del 2026-10-21 (DECISIONES-DE-PROCESO.md) dice PARADA salvo seguir la forma que la propia guardia propone. Lección para el revisor: una negativa se declara; solo se usa otra forma si la propone la guardia en su mensaje.
> - Antes de commitear, mide PROJECT_STATE con wc -c (tiene que dar unos 22.889, por debajo de 23.000) y pasa test_hoja_de_ruta y test_project_state en el make check sellado.
>
> Después, lo de siempre: merge --no-ff a main, el tag, el commit de estado que solo reemplaza Current Branch (main), Current Feature («Ninguna rama abierta. trabajo/cuarentena-por-condicion-2 cerrada en main el 2026-10-28 (stable/F38h-cuarentena-por-condicion-2): diciembre tapado en la cuarentena mientras no se decida, la coma y el punto en la regla de fecha, el barrido ancho en la skill ingerir-sesion y la regla de letras (CUARENTENA-POR-CONDICION-2.md).»), Stable Main State y Last Stable Commit (la Next Action ya cambió en el contrato y aquí no se toca), make check sellado, push atómico de main y el tag en un solo comando (confirmo la regla ask con «1. Yes»), la CI de main en verde mirada sin guion ni bucle, y borrar la rama local y la remota fix/cuarentena-por-condicion-2.
>
> El worktree de otra sesión (.../scratchpad/wt-ci, e7df30b): mide con git worktree list, git -C <ruta> status --short y git merge-base --is-ancestor e7df30b main. Si está limpio y e7df30b ya está en main, quítalo con git worktree remove <ruta> (sin --force) y git worktree prune; si no, no lo toques y dímelo con la medida.
>
> Nunca --no-verify, push --force, borrar tags, cherry-pick ni rebase. Si algo no cuadra, PARADA antes del merge.
>
> Informe final: sha de main, tag, número del run de la CI de main con su resultado, ramas que quedan (local y remota), lo del worktree wt-ci y tamaño de PROJECT_STATE en bytes.

## Estado

Fases 0 a 4 hechas; los hallazgos del revisor, arreglados (§12); el clon, borrado (§12). Orden de cierre del 2026-10-28 recibida (arriba): se cierra con cerrar-rama, tag stable/F38h-cuarentena-por-condicion-2.
