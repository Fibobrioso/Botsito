# DIETA-ESTADO · PROJECT_STATE.md adelgazado antes de la sesion 7a

PLANTILLA: este informe no trae tabla final de preguntas al trader; es una rama de estado.

Rama `trabajo/dieta-estado` (tramo «Carril: guardias y deuda» de `docs/plan/HOJA-DE-RUTA.md`;
precedentes: `trabajo/adelgazar-estado` y `trabajo/margen-pendiente`). Encargo del consultor del
2026-11-13: `docs/encargos/trabajo-dieta-estado.md`.

## Apertura (2026-11-13)

Base comprobada con git y gh antes de abrir, tras `git fetch --prune origin`:

| Comprobación | Salida |
|---|---|
| `git rev-parse --short main` | `c473d4c9` |
| `git rev-parse main origin/main` | `c473d4c9c28956039ce69ae88989261d47e6349c` las dos veces |
| `git rev-parse "stable/F39a-guardia-falsos-positivos^{commit}"` = `git rev-parse main^1` | `e931459873e9b73f6bd6e05d97b91e2f3c7afe9e` las dos |
| `git ls-remote --tags origin "stable/F39a*"` | `36e8c914… refs/tags/stable/F39a-guardia-falsos-positivos` (`^{}` = `e9314598…`) |
| Último `- Tag: ` de HISTORIA | `stable/F39a-guardia-falsos-positivos` (HISTORIA:17953) |
| CI de `main` en `c473d4c9…` (check-runs) | `python completed success`, run 43459199788 |
| `git branch --list` / `git ls-remote --heads origin` | solo `main` en local y en origin |
| `stable/F39b-dieta-estado` | no existe ni en local (`git tag -l`) ni en origin (`git ls-remote --tags`) |
| Tramo | `## Carril: guardias y deuda` en `docs/plan/HOJA-DE-RUTA.md:700`, literal |
| `wc -c PROJECT_STATE.md` en main | 24652 |

Desviación declarada (encargo, punto 0): la fila de `docs/validation/HOLDOUT-EXPOSICIONES.md` de
los `make check` del día entra en el commit de apertura, así que `git diff main --stat` de la
apertura trae un fichero más de los cinco que nombra la verificación de `abrir-rama`.

Pico de memoria del `make check` de la apertura (árbol `ef4830b0…`, commit `b031559d`): «PICO DE
MEMORIA de make check: 318 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el
mayor proceso, 308 MiB)»; 3513 passed, 6 xfailed, SELLO.

## Fase 0 · Inventario (2026-11-13), sin tocar PROJECT_STATE

El criterio es el de `docs/state/README.md`, «Que sale de PROJECT_STATE, y con que criterio»,
sin cambiarlo, con las **tres precisiones del consultor** (encargo, punto 3; decisión del
consultor, no del README): (1) en (b), «otro sitio» es otra entrada de la Next Action, `CLAUDE.md`
o un runbook; (2) en (d), el sitio donde vive literal tampoco puede ser la hoja de ruta, un informe
ni HISTORIA; (3) una línea ya ACORTADA no se vuelve a acortar. (e), en la lectura de
MARGEN-PENDIENTE.md §0.h.2 que fija README: corte antes de «. », «; » o «: », o tras el «)» de un
inciso, nunca dentro de una ruta, un id o un literal entre acentos graves, y el corte válido MÁS
LARGO de 160 bytes como mucho desde el «- » (la práctica de `trabajo/margen-pendiente` y
`trabajo/trazas-ablacion`); los 200 bytes, con el salto de línea. Las cifras salen de dos guiones de
la carpeta de trabajo, fuera del repo, que solo leen `PROJECT_STATE.md`.

### 0.1 Bytes por sección (main, `c473d4c9`: 24.652)

| Sección | Antes | Previsión después |
|---|---|---|
| Next Action entera (de ella, «Pendientes heredados») | 6.514 (895) | 6.514 (895) |
| Technical Debt | 13.368 | 12.759 |
| Reglas vivas | 1.615 | 1.615 |
| **PROJECT_STATE.md** (main) | **24.652** | **24.043** |

(En la rama, con sus cabeceras, 24.683 → 24.074; Current Branch y Current Feature de la rama suman 31
bytes más que los de `main`: 16 y 15; corregido tras el revisor, a2.)

### 0.2 Lo que pagaron las ramas desde el último recorte (F38u a F39a), comprobado

- **cmp / G.6 (F39a)**: ninguna línea de Technical Debt nombra `cmp` ni G.6; la de `:84` ya la
  reescribió el cierre de F39a (registro de cierre, HISTORIA :17944-17946; corregido tras el revisor, a5) y lo que dice sigue
  vivo: F1 aplazado y el `/` de `compilar.py` negado. La de `:152` (« / », `</li>`, `$'\r'`) F39a no
  la tocó (GUARDIA-FALSOS-POSITIVOS.md:225).
- **capa_hash, R6a.2, LATIDO_SEG (F38z)**: ninguna línea las nombra (grep sobre PROJECT_STATE
  vacío). La de F38z que queda (`:83`, la skill `activar-sesion` y `Generado.mqh`) no está pagada:
  `.claude/skills/activar-sesion/SKILL.md` no nombra `Generado.mqh` ni `generar_capa`.
- **Las láminas y `motor laminas` (F38w, F38y)**: `:149` sigue (`engine/laminas.py:534-536`, «Vuelve
  cuando lo distinga»); `:151` sigue (los tests solo llaman `cli.main` con la negativa,
  `tests/unit/test_laminas.py:701`); `:152`, arriba.
- **La preparación de la sesión 7 (F38x)**: `:150` sigue: `scripts/graficos_sesion.py:66` («La regla
  2 de SESION-DE-PREGUNTAS.md») y `src/botsito/engine/decisiones.py:7-8` («lo fijara el ADR del
  metodo») no han cambiado.
- Y las de antes que podían haberse pagado de paso: el ADR 0087 sigue sin existir (`docs/adr/` salta de
  0086 a 0088); la nota de RN-019 sigue (`strategy_spec.yaml:2024`); el docstring de `freno.py:7-8`
  sigue; `VISOR-DIAS.md` sigue sin «diagnostico»; `letras_hechas` sigue siendo un conjunto
  (`test_hoja_de_ruta.py:60`); ni `sello_make_check.py` ni el `Makefile` comprueban la fila de
  HOLDOUT-EXPOSICIONES; las skills `ingerir-sesion` y `abrir-rama` siguen sin nombrar `Fuente:` ni
  PLANTILLA.

**Ninguna línea de las tres secciones sale por (a), (b), (c) ni (d).** Los pendientes heredados 6 a
10 y 27 tampoco: siguen como los dejó `trabajo/margen-pendiente` (MARGEN-PENDIENTE.md §0.h, tabla
1), sin evidencia nueva; ningún `HER:n` sale de la hoja de ruta.

### 0.3 La tabla, línea a línea

Numeración de `PROJECT_STATE.md` en la rama tras la apertura, que es la de `main` (la apertura solo
cambió el texto de dos líneas de cabecera y dos de Archivo). Bytes con el salto de línea.

| PS | arranque | bytes | condicion | evidencia |
|---|---|---|---|---|
| :55 | 6. FEBRERO NO SE TOCA Y NO SE DESCARGA. Unico mes ciego … | 113 | se queda | sin evidencia de hecho (texto entero, Archivo 1); igual en MARGEN-PENDIENTE.md §0.h, tabla 1 |
| :56 | 7. JUNIO, LA GUARDIA Y LOS ONCE DIAS. La guardia de sta… | 110 | se queda | sin evidencia de hecho (Archivo 1); igual en MARGEN-PENDIENTE.md §0.h |
| :57 | 8. EL BRIEF PARA ABRIR LOS 4 dev DE SEPTIEMBRE, que es… | 114 | se queda | sin evidencia de hecho (Archivo 1); igual en MARGEN-PENDIENTE.md §0.h |
| :58 | 9. LA CITA QUE YA TENEMOS CON UN PROBLEMA, y no es una d… | 115 | se queda | sin evidencia de hecho (Archivo 1); igual en MARGEN-PENDIENTE.md §0.h |
| :59 | 10. De la demo de FTMO queda el grabador de spread y tic… | 67 | se queda | F17 sin hacer; `HER:10` en las Refs de R5 (HOJA-DE-RUTA.md:470) y del carril (:703); MARGEN-PENDIENTE.md §0.h |
| :60 | 27. Para Aleks con FTMO: la «maximum capital allocation … | 195 | se queda | A.2 sigue abierta (HOJA-DE-RUTA.md:667-673); la hoja de ruta no vale para (b) (precision 1) |
| :81 | Hoy un mes no puede salir de knowledge/cases/meses_rese… | 248 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :82 | El validador del journal (v1 y v2) vive en botsito.mql5… | 270 | se queda | (e) ahorraria 58 (< 60), medido igual en MARGEN-PENDIENTE.md §0.h.2 |
| :83 | La skill activar-sesion no dice que una activación que… | 227 | se queda | no pagada: `.claude/skills/activar-sesion/SKILL.md` no nombra `Generado.mqh` ni `generar_capa` (grep vacio); (e) ahorraria < 60 |
| :84 | La guardia niega a un guion nuevo dos falsos positivos, … | 411 | **(e)** | 411 -> 168, ahorra 243; F1 sigue aplazado y el `/` de `compilar.py` sigue negado (GUARDIA-FALSOS-POSITIVOS.md:224 y registro de cierre de F39a, HISTORIA :17944-17946; corregido tras el revisor, a5): no pagada |
| :85 | El bróker simulado reserva margen por cada pendiente sto… | 197 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :86 | Los docstrings de scripts/viabilidad_trader.py:11 («5 … | 225 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :87 | La comprobación del LF final en UltimaLinea (mql5/Inc… | 186 | se queda | sin evidencia de pagada, repetida o sustituida |
| :88 | Que el EA reinicie sus globales tras un cambio de símbol… | 171 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :89 | La guardia no mira las herramientas que leen un fichero … | 183 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :90 | Riesgo residual de trabajo/guardia-g1 (§4.3) … (entera… | 100 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :91 | Riesgo residual de C (§5): una ruta compuesta a través d… | 205 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :92 | Riesgo residual de B (§5): solo Python; node, perl y… | 185 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :93 | Los guiones de la plataforma (contrato_rama.py, sello… | 207 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :94 | Riesgo residual de la excepción de la carga por ruta (re… | 141 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :95 | Riesgo residual de ADR-0088 (revisor, B7) … (entera en H… | 94 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :96 | ADR 0087 (S-15, no existe) sigue en los ids-inexistente… | 152 | se queda (dudosa 1) | El ADR 0087 no existe (`docs/adr/` salta de 0086 a 0088): no pagada; ver dudosas |
| :97 | RN-019 no dispara nunca en el motor: su forma pide por:… | 229 | se queda | (e) ahorraria 18 (MARGEN-PENDIENTE.md §0.h.2) |
| :98 | La nota de RN-019 (strategy_spec.yaml, hacia :1840) dice… | 147 | se queda | la nota sigue: `strategy_spec.yaml:2024` («lo pregunta A-31») |
| :99 | Una zona del productor reutilizada en un escenario nuevo… | 188 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :100 | El visor no conecta --diagnostico-cuenta-diaria (cli.p… | 216 | se queda (dudosa 2) | no pagada: `--diagnostico-cuenta-diaria` solo en un parser (`cli.py:2322`); sus numeros de linea ya no casan; (e) ahorraria < 60 |
| :101 | curva_con_deslizamiento y veredicto_con_f17 (criteri… | 196 | se queda | sin evidencia de pagada, repetida o sustituida |
| :102 | make check, en una rama trabajo/*, no sella si HOLDOUT-E… | 243 | se queda | no pagada (ni `scripts/sello_make_check.py` ni el `Makefile` nombran HOLDOUT-EXPOSICIONES); sin corte estricto en 160 |
| :103 | VISOR-DIAS.md no recoge las opciones de diagnóstico del … | 139 | se queda | `docs/runbooks/VISOR-DIAS.md` sigue sin «diagnostico» (grep -c = 0) |
| :104 | El visor no enseña las H4 que el sesgo salta por el colo… | 107 | se queda | sin evidencia de pagada, repetida o sustituida |
| :105 | test_visor.py y test_preparar_a35.py hacen leer el M… | 183 | se queda | sin evidencia de pagada, repetida o sustituida |
| :106 | motor visor --hasta no recorta las H4 de contexto, las… | 123 | se queda | sin evidencia de pagada, repetida o sustituida |
| :107 | arnes.dias_de_mercado lee para calentar el M1 entero d… | 267 | se queda | (e) ahorraria 29 (MARGEN-PENDIENTE.md §0.h.2) |
| :108 | El docstring de engine/freno.py:7-8 dice que el adapta… | 185 | se queda | el docstring sigue (`src/botsito/engine/freno.py:7-8`); R6a.4 sin hacer |
| :109 | La guardia no niega leer con Read las crudas de data/tra… | 135 | se queda | sin evidencia de pagada, repetida o sustituida |
| :110 | La forma de medida de ffmpeg de la guardia no admite -ss… | 204 | se queda | otra regla (lista cerrada de ffmpeg), fuera de F39a (GUARDIA-FALSOS-POSITIVOS.md:228); (e) ahorraria < 60 |
| :111 | test_hoja_de_ruta no distingue un registro «HECHA · T» d… | 160 | se queda | `letras_hechas` sigue devolviendo un conjunto (`tests/unit/test_hoja_de_ruta.py:60`) |
| :112 | Un fotograma dentro de un tramo no citable se puede abri… | 197 | se queda | sin evidencia de pagada, repetida o sustituida |
| :113 | … | 1 | — (linea en blanco) | 1 byte; no es una linea de deuda; no se toca (ver dudosas) |
| :114 | La ingesta asigna la sesión con el reloj del registro y … | 216 | se queda | el corte valido mas largo (110) ahorraria 37 (< 60; corregido tras el revisor, a3) |
| :115 | Sin git callan, sin aviso, las comprobaciones que leen g… | 234 | se queda | (e) ahorraria 27 (MARGEN-PENDIENTE.md §0.h.2) |
| :116 | RN-029 a RN-032 citan de relleno ev-v4-012524-0ef85a89 (… | 220 | se queda | (e) ahorraria 46 (MARGEN-PENDIENTE.md §0.h.2) |
| :117 | La condición 2 de ADR-0042 §2 (la lectura COMPLETA del l… | 184 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :118 | engine/simulador_config.py busca el spread supuesto de… | 205 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :119 | LA GRAMATICA DEL KIT PASA A LA UNIDAD OPERACION (2026-09… | 74 | se queda | sin evidencia de pagada, repetida o sustituida |
| :120 | cherry-pick Y rebase NO PASAN POR LA PUERTA DEL COMM… | 131 | se queda | el consultor la dejo en `trabajo/margen-pendiente` (respuesta a la PARADA, punto 7: «la deuda de cherry-pick se queda», MARGEN-PENDIENTE.md:510) |
| :121 | scripts/v5_criterio.py SOLO RECONOCE CAJAS DE VENTA (2… | 70 | se queda | sin evidencia de pagada, repetida o sustituida |
| :122 | NADA COMPRUEBA MECANICAMENTE QUE EL CUERPO DE UN INFORME… | 119 | se queda | CLAUDE.md apunta aqui («Nada lo comprueba mecanicamente todavia (Technical Debt)») |
| :123 | LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY (202… | 134 | se queda | sin evidencia de pagada, repetida o sustituida |
| :124 | EL FRACTAL 5/120 NO CAPTURA LO QUE EL TRADER LLAMA ESTRU… | 92 | se queda | sin evidencia de pagada, repetida o sustituida |
| :125 | LA GUARDIA DE cobertura_material EN universo() ES MA… | 156 | se queda | sin evidencia de pagada, repetida o sustituida |
| :126 | EL no_trade POR AUSENCIA NO ESTA DECIDIDO, Y NO ENTRA … | 191 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :127 | fecha_grabacion TIENE QUE SER UN EJE DE PRIMERA CLASE,… | 175 | se queda | sin evidencia de pagada, repetida o sustituida |
| :128 | F26 lee la diferencia 3,00/3,75 entre la regla y el mate… | 117 | se queda | la entrada G de la Next Action dice que vive en Technical Debt |
| :129 | BUSCAR EN EL CORPUS ANTES DE REDACTAR CUALQUIER AMBIGUED… | 111 | se queda | sin evidencia de pagada, repetida o sustituida |
| :130 | EL DIA QUE UN CAMINO GUARDE MATERIAL EN knowledge/cases… | 214 | se queda | sin corte estricto en 160 (MARGEN-PENDIENTE.md §0.h.2) |
| :131 | lectura_de_velas SIGUE LEYENDO EL config.yaml DE HOY… | 140 | se queda | sin evidencia de pagada, repetida o sustituida |
| :132 | DOS DIAS DEL UNIVERSO DE LA SESION 1 NO ESTAN EN NINGUNA… | 215 | se queda | la entrada G dice que vive aqui; sin corte estricto en 160 |
| :133 | UNA PREGUNTA ABRE N PARTICIONES Y N LO DECIDE EL DATO, N… | 120 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :134 | EL FALLBACK DE leer_fichero JUZGA UNA CARPETA DESCONOC… | 144 | se queda | sin evidencia de pagada, repetida o sustituida |
| :135 | UN TOKEN NO PUEDE DECLARAR QUIEN LO PRODUCE, Y LOS PREDI… | 184 | se queda | sin evidencia de pagada, repetida o sustituida |
| :136 | UNA pregunta DE AMBIGUEDAD PUEDE NOMBRAR UN INSTANTE D… | 171 | se queda | sin evidencia de pagada, repetida o sustituida |
| :137 | EL PUNTO CIEGO DEL DETECTOR DE CONTRADICCIONES, TERCERA … | 82 | se queda | sin evidencia de pagada, repetida o sustituida |
| :138 | EL DETECTOR DE CONTRADICCIONES NO VE LOS TEMAS HERMANOS … | 109 | se queda | sin evidencia de pagada, repetida o sustituida |
| :139 | LA VIA DE PROPUESTA NO ADMITE supersede (2026-09-17, r… | 95 | se queda | CLAUDE.md la nombra pero no entera (MARGEN-PENDIENTE.md §0.h.1) |
| :140 | UN CONFIRM SOBRE UN ITEM SUPERSEDIDO QUEDA INVISIBLE Y S… | 118 | se queda | sin evidencia de pagada, repetida o sustituida |
| :141 | Copia de seguridad de las crudas y los WAV … (entera en … | 95 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :142 | La skill ingerir-sesion no nombra el trailer Fuente: de … | 329 | se queda | no pagada: ni `ingerir-sesion` ni `abrir-rama` nombran `Fuente:` ni PLANTILLA (grep vacio); su unico corte en 160 cae dentro del trailer `Fuente:` |
| :143 | Riesgos residuales del alias de la raíz (GUARDIA-ALIAS.m… | 194 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :144 | Las cotizaciones sin tick del bróker no usan la misma ve… | 233 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :145 | El panel de FTMO quedó declarado el 2026-11-07 (medianoc… | 158 | se queda | ACORTADA ya (precision 3: no se vuelve a acortar) |
| :146 | La zona que RN-005 liga al escenario vigente en el mismo… | 368 | se queda | sin corte estricto en 160 (el primer cierre de inciso pasa de 160) |
| :147 | La comparación de motor decisiones mira cada operación… | 265 | se queda | el corte valido mas largo (142) ahorraria 47 (< 60; corregido tras el revisor, a3) |
| :148 | El toca_colocar_orden_limite sintético de tests/unit/t… | 246 | se queda | el corte valido mas largo (160) ahorraria 12 (corregido tras el revisor, a3) |
| :149 | motor laminas no dice el esquema: con la orden en el p… | 247 | se queda | no pagada: `engine/laminas.py:534-536` sigue sin frase del esquema; (e) ahorraria < 60 |
| :150 | Dos textos que ADR-0093 deja viejos y que trabajo/prepar… | 273 | **(e)** | 273 -> 180, ahorra 93; no pagada: `scripts/graficos_sesion.py:66` y `engine/decisiones.py:7-8` siguen con el texto viejo |
| :151 | motor laminas: la CLI solo se prueba entera con las ve… | 208 | **(e)** | 208 -> 138, ahorra 70; la cita del informe ya va en el arranque |
| :152 | La guardia toma por ruta una barra dentro de una cadena … | 502 | **(e)** | 502 -> 299, ahorra 203; no pagada (F39a no la toco: GUARDIA-FALSOS-POSITIVOS.md:225); las dos citas, literales, delante |
| :158 | knowledge/cases/holdout/{1,2,3}/ → tres particiones rese… | 576 | se queda | Regla viva: (b) exige entera en CLAUDE.md o runbook; CLAUDE.md no dice «cada una se abre una sola vez» ni la guarda de `tests/conftest.py` |
| :161 | Regimenes de cambio de knowledge/. · Pureza de domain/. … | 108 | se queda | «Parametros no se optimizan contra resultados» no vive en CLAUDE.md ni en un runbook (MARGEN-PENDIENTE.md §0.h.1) |
| :162 | La rentabilidad pre-registrada de ADR-0092, medida una v… | 340 | se queda | ADR-0092 la sostiene, pero no vive literal en CLAUDE.md ni en un runbook |
| :163 | La firma y el tipo de cuenta (FTMO 2-Step Swing, ADR-002… | 241 | se queda | ADR-0026 la sostiene; no vive literal en CLAUDE.md ni en un runbook |

### 0.4 (e) ACORTADA: las cuatro que cumplen

Todas de Technical Debt, ninguna ACORTADA antes, más de 200 bytes, corte válido más largo ≤ 160 y
ahorro ≥ 60. Lo que quedaría en PROJECT_STATE, literal:

| PS | antes | arranque | después | ahorra | queda |
|---|---|---|---|---|---|
| :84 | 411 | 83 | 168 | 243 | `- La guardia niega a un guion nuevo dos falsos positivos, que lanza Aleks con «!» … (CAPA-GENERADA.md, «La guardia»; entera en HISTORIA, Technical Debt ACORTADA)` |
| :150 | 273 | 88 | 180 | 93 | `- Dos textos que ADR-0093 deja viejos y que trabajo/preparacion-sesion-7 no podía tocar … (PREPARACION-SESION-7.md §0.2, H8 y H19; entera en HISTORIA, Technical Debt ACORTADA)` |
| :151 | 208 | 87 | 138 | 70 | `` - `motor laminas`: la CLI solo se prueba entera con las velas reales (LAMINAS.md, F4.3) … (entera en HISTORIA, Technical Debt ACORTADA) `` |
| :152 | 502 | 130 | 299 | 203 | `- La guardia toma por ruta una barra dentro de una cadena que no es una ruta (una etiqueta de cierre HTML, « / » entre espacios) … (LAMINAS.md, «Aplicación de la respuesta a la PARADA final», al final; LAMINAS.md, respuesta tras revisar la v4, 6; entera en HISTORIA, Technical Debt ACORTADA)` |

Total: **609 bytes**. Dos lecturas mías, para que las veas:
- `:151` ya lleva su cita en el arranque, así que el paréntesis no la repite (como la de «Riesgo
  residual de la excepción de la carga por ruta», que acortó `trabajo/trazas-ablacion`).
- `:152` cita su informe DOS veces (una por cada falso positivo); conservo las dos, literales y en su
  orden, porque README dice «la cita», y quitar una sería escoger.

Las demás de más de 200 bytes se quedan enteras: ahorrarían menos de 60 (`:82` 58, `:83`, `:97` 18,
`:100`, `:107` 29, `:110`, `:114` 37, `:115` 27, `:116` 46, `:147` 47, `:148` 12, `:149`) o no tienen
corte estricto en 160 (`:102`, `:130`, `:132`, `:146`; y `:142`, cuyo único corte caería dentro del
trailer `Fuente:`).

### 0.5 Dudosas (se quedan; para el consultor)

1. `:96` «ADR 0087 (S-15, no existe) sigue en los `ids-inexistentes`…»: la numeración ya pasó de
   0087 (existen 0088 a 0093; `trabajo/activar-sesion-06-motor` dejó el 0087 reservado para S-15 y
   numeró su ADR 0089, ACTIVAR-SESION-06-MOTOR.md:41-42); podría ser (c) si ningún ADR va a llevar
   ya ese número, pero eso lo decide el consultor, no un hecho del repo.
2. `:100` «El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2558; el arnés sí, :2438)»:
   la deuda sigue viva (la opción solo existe en un parser, `cli.py:2322`), pero sus números de línea
   ya no casan. No hay criterio para corregirlos; se queda como está. Los corrige la próxima rama que
   toque esa línea o `cli.py` (respuesta del consultor a la PARADA, punto 4).
3. `:113`, una línea en blanco suelta dentro de Technical Debt (1 byte). No es una línea de deuda; no
   la toco.

## PARADA (encargo, punto 4): la previsión no baja de 24.000 bytes

Con las cuatro (e) de 0.4 y nada por (a)-(d), `main` quedaría en **24.043 bytes**, 43 por encima
del umbral. No sigo a la fase 1. Lo que haría, por orden de preferencia:

1. **Aplicar las cuatro (e) tal cual (0.4) y cerrar en ~24.043.** Libera 609 bytes (957 de margen
   hasta 25.000, contra 348 hoy), sin forzar ningún criterio. Es lo que recomiendo: el umbral de
   24.000 es del encargo, no del test, y bajarlo más pide salirse de README o de las precisiones.
2. Lo mismo, pero en `:152` solo la PRIMERA cita (la del falso positivo que queda en el arranque):
   45 bytes menos, **~23.998**. Cumple el umbral por 2 bytes, y el cierre (que reescribe Current
   Feature, Stable Main State y Last Stable Commit) puede volver a pasarlo. Es una lectura de «la
   cita» que tendrías que darme tú.
3. Sacar también la deuda de `cherry-pick` y `rebase` (`:120`, 131 bytes) por (b) (`CLAUDE.md:62-63`
   y la guardia), **~23.912**. La rechazaste en `trabajo/margen-pendiente` (MARGEN-PENDIENTE.md:510,
   «la deuda de cherry-pick se queda»): solo con una decisión tuya nueva.

Las tres dudosas de 0.5 no cambian la cifra salvo `:96` (152 bytes si saliera por (c): ~23.891).

Pico de memoria del `make check` de la fase 0 (árbol `03de840a…`, commit `89419ca0`; el primer
intento salió en rojo por el ADR 0087 escrito con guion en este informe, `knowledge validate`, y se
corrigió antes de commitear): «PICO DE MEMORIA de make check: 320 MiB en `test` (suma de sus
procesos, memoria comprometida, Windows; el mayor proceso, 310 MiB)»; 3513 passed, 6 xfailed, SELLO.

## Respuesta del consultor a la PARADA de la fase 0 (2026-11-13)

Copiada tal cual:

> Respuesta del consultor a la PARADA de la fase 0 de trabajo/dieta-estado (2026-11-13). Cópiala tal cual en el informe, en su sección, y aplícala.
>
> 1. Opción 1: se acortan por (e) las cuatro líneas que lo admiten, tal cual las propones, con sus bloques literales en HISTORIA. El umbral de 24.000 bytes del encargo era un freno por si la rama no merecía la pena, no un objetivo: 609 bytes liberados dejan unos 957 de margen hasta el tope (hoy 348), y eso basta para la ingesta y la activación de la 7a. Decláralo en el informe como respuesta a la PARADA.
> 2. Opción 2, no: dejar en :152 solo la primera cita reescribe la línea, y (e) manda conservar la cita del informe. La :152 se acorta como en la opción 1.
> 3. Opción 3, no: la :120 (cherry-pick y rebase) se quedó por decisión del consultor en trabajo/margen-pendiente, y reabrir esa decisión por unos 130 bytes no compensa. Se queda.
> 4. Las tres dudosas se quedan, sin tocar un byte, como manda la negación por defecto:
>    - :96 (ADR 0087): que el número quede abandonado es una decisión aparte, ligada a S-15 de la sesión 5, y no se toma aquí.
>    - :100 (cli.py:2558 y :2438): los números de línea viejos no son ninguna de las condiciones de README. En la lista de dudosas del informe, una línea que diga que los corrige la próxima rama que toque esa línea o cli.py.
>    - :113 (la línea en blanco): README no la cubre y no es una línea con contenido. Se queda, y va a la lista de dudosas.
> 5. Lo demás, como dice el encargo: el pico de memoria del make check de la fase 0 entra en el informe en el próximo commit; el tamaño final exacto con wc -c; las pruebas de §5; y el revisor con su alcance. Después, «Rama lista para revisión, NO cerrada».

**Declarado como respuesta a la PARADA** (punto 1): la previsión queda por encima del umbral de
24.000 bytes del encargo y la rama sigue igual, porque el consultor fija que ese umbral era un freno
y no un objetivo.

## Fase 1 · Aplicar (2026-11-13)

Punto por punto:

1. **Las cuatro (e), tal cual 0.4.** En PROJECT_STATE, Technical Debt, `:84`, `:150`, `:151` y
   `:152` pasan a su arranque literal con el sufijo de README; las cuatro, enteras y literales, con lo
   que queda de cada una, al final de `docs/state/HISTORIA.md`, bajo «# Technical Debt ACORTADA · sale
   de PROJECT_STATE.md en trabajo/dieta-estado (2026-11-13)», con la forma del bloque de
   `trabajo/trazas-ablacion`. Lo escribe un guion de la carpeta de trabajo que toma la línea original
   del propio fichero (no la reescribe), comprueba que el arranque es prefijo literal, que lo que sigue
   al corte es «. », «; » o «: » o que el corte acaba en «)», que la línea pasa de 200 bytes, que el
   arranque no pasa de 160 y que ahorra 60 o más, y añade el bloque a HISTORIA sin tocar lo que había.
2. **`:152` con sus dos citas** (punto 2).
3. **`:120` se queda** (punto 3).
4. **Las tres dudosas se quedan sin tocar un byte**; la línea de `:100` entra en 0.5 (punto 4).
5. Ninguna línea sale por (a)-(d), así que no hay bloque «# Pendiente heredado SALE», «PAGADA»,
   «RECLASIFICADA» ni «SUSTITUIDA», y `docs/plan/HOJA-DE-RUTA.md` no se toca (ningún `HER:n` sale).

`git diff` de PROJECT_STATE en la fase 1: cuatro líneas quitadas y cuatro puestas, todas en
Technical Debt; nada más.

### Bytes por sección, antes y después

| Sección | Antes (main) | Después |
|---|---|---|
| Next Action entera (de ella, «Pendientes heredados») | 6.514 (895) | 6.514 (895) |
| Technical Debt | 13.368 | 12.759 |
| Reglas vivas | 1.615 | 1.615 |
| **PROJECT_STATE.md** | **24.652** (main) | **24.074** en la rama (`wc -c`) |

En la rama, `wc -c PROJECT_STATE.md` = **24.074**; con las cabeceras de `main` (el Current Branch y
el Current Feature de la rama suman 31 bytes más), **24.043**. El cierre reescribe Current Feature, Stable Main State y
Last Stable Commit, así que la cifra de `main` tras el cierre la da la orden de cierre.

### Desviaciones

1. La fila de HOLDOUT-EXPOSICIONES.md entró en el commit de apertura (encargo, punto 0), un fichero
   más de los que nombra la verificación de `abrir-rama`.
2. La previsión no bajó de 24.000 y la rama siguió tras la PARADA, por la respuesta del consultor
   (punto 1).
3. Ninguna línea se queda distinta de lo que manda el criterio.
4. La fase 0 no lanzó el agente `auditor-encargo` ni invocó la skill `fase-cero`, y el informe no
   tiene «El encargo frente al repo» (revisor, b2). El encargo pedía la fase 0 como inventario, sin
   nombrar el auditor; la sesión comprobó a mano las afirmaciones del encargo que lo necesitaban
   (base, tramo, tag libre, tamaño de 24.652, la sección de README, los registros de cierre de F38u a
   F39a). Es una omisión, no una decisión: se declara aquí.
5. `:142` se quedó entera con una lectura más estricta que README, sin declararla como tal (revisor,
   a4): su único corte en 160 bytes (byte 53) cae justo antes del «:» del trailer «Fuente:», que en
   PROJECT_STATE no va entre acentos graves, así que no es ruta, id ni literal. Leído al pie de la
   letra, se podría acortar (ahorraría unos 169 bytes). Se queda por niega-por-defecto, y el consultor
   aceptó la lista de 0.4 tal cual (respuesta, punto 1); si la quiere acortada, es una decisión suya
   para la orden de cierre o para otra rama.
6. La respuesta del consultor a la PARADA se copió al final del encargo después del revisor (b1), como
   pide `fase-cero` y hicieron las ramas anteriores.

Pico de memoria del `make check` de la fase 1 (árbol `af74fa5c…`, commit `41983743`): «PICO DE
MEMORIA de make check: 318 MiB en `test` (suma de sus procesos, memoria comprometida, Windows; el
mayor proceso, 307 MiB)»; 3513 passed, 6 xfailed, SELLO. Antes, las siete pruebas de §5 del encargo
sueltas, en verde: `tests/unit/test_project_state.py`, `test_project_state_rutas.py`,
`test_historia.py`, `test_kit.py`, `test_hoja_de_ruta.py`, `tests/contract/test_ids_citados.py` y
`tests/contract/test_documentos_vivos.py` (el encargo lo nombraba sin carpeta: vive en `contract/`).

**Tamaño final**: `wc -c PROJECT_STATE.md` = **24074** en el último commit de la rama.

## El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 0.1 | `git fetch --prune`; base main/origin/tag/CI; ninguna otra rama; F39b libre | Hecho | «Apertura», tabla |
| 0.2 | Abrir con `abrir-rama`: encargo tal cual con Write, contrato, Archivo | Hecho | `b031559d`; Archivo 70 en HISTORIA |
| 0.3 | Contrato: tramo entre comillas y literal, riesgo bajo, rutas extra (HOLDOUT, HOJA solo para HER:n) | Hecho | `contrato.yaml`; `HOJA-DE-RUTA.md:700` |
| 0.4 | Informe con PLANTILLA en sus primeros 600 caracteres | Hecho | línea 3 de este informe |
| 0.5 | Fila de HOLDOUT-EXPOSICIONES antes del primer `make check`, en la apertura; desviación declarada | Hecho | `HOLDOUT-EXPOSICIONES.md:147`; desviación 1 |
| 0.6 | Modelo Opus, esfuerzo medio | Hecho | la sesión corre en Opus 5.5, esfuerzo medio (lo fijó Aleks con `/effort` antes del encargo) |
| 1 | Bajar PROJECT_STATE con los criterios de README sin cambiarlos | Hecho | 24.652 → 24.074 en la rama (24.043 con las cabeceras de main); README sin tocar |
| 2.1 | Letras de la Next Action, Known Ambiguities, ritual, secciones: sin cambiar | Hecho | `git diff main...HEAD -- PROJECT_STATE.md`: solo Current Branch/Feature, los dos «Archivo 70» y las cuatro de Technical Debt |
| 2.2 | Ningún fichero fuera de la lista | Hecho | `git diff --stat main...HEAD`: 6 ficheros, todos del contrato; `contrato_rama.py` en verde |
| 2.3 | Ni material, ni velas, ni ticks, ni holdout; sin arnés | Hecho | solo documentos del repo y dos guiones que leen PROJECT_STATE (los `make check` leen el M1 de marzo, declarado) |
| 3.1 | (a)-(d) con evidencia y sección | Hecho | 0.2 y 0.3: ninguna sale |
| 3.2 | (e) solo Technical Debt, con sus reglas | Hecho | 0.4; bloque de HISTORIA |
| 3.3 | Las tres precisiones, declaradas como decisión del consultor | Hecho | «Fase 0», párrafo inicial |
| 3.4 | Leer el texto entero de los heredados antes de sacarlos; HER:n | No aplica | ningún heredado sale; HOJA-DE-RUTA sin tocar |
| 3.5 | Niega por defecto; dudosas a una lista | Hecho | 0.5 |
| 3.6 | Bloques al final de HISTORIA con su forma | Hecho | «# Technical Debt ACORTADA · sale de PROJECT_STATE.md en trabajo/dieta-estado (2026-11-13)» |
| 4 | Fase 0: tabla, pagos de F38u-F39a, bytes por sección y previsión; PARADA si no baja de 24.000 | Hecho | 0.1-0.5; PARADA en `89419ca0` |
| R.1-R.4 | Respuesta a la PARADA: opción 1, no la 2 ni la 3, dudosas sin tocar y la línea de `:100` | Hecho | fase 1; 0.5, punto 2 |
| R.5 / 5 | Commits sellados, pico de cada `make check`, pruebas de §5, `wc -c` | Hecho | los tres picos en el informe; tamaño final arriba |
| 6 | Informe completo y la fila de ERRORES-RECURRENTES preparada | Hecho | este informe; «Para la orden de cierre» |
| 7 | Revisor con su alcance; sin CI de Linux | Hecho | «Informe del revisor», abajo; sin CI: la rama no toca hooks, rutas, sistema de archivos ni código (`RITUAL.md`, «Antes del merge: la CI de Linux») |

Exposiciones: los `make check` (M1 de marzo, calienta con junio), en la fila del 2026-11-13. Ninguna
otra.

## Para la orden de cierre

- **Next Action**: no sale, no entra y no cambia ninguna letra.
- **Hoja de ruta**: ninguna entrada cambia (la rama no tiene entrada propia en el carril).
- **Fila de `docs/runbooks/ERRORES-RECURRENTES.md`** (la escribe `cerrar-rama`; la cifra del revisor,
  de su informe):

  `| trabajo/dieta-estado | Una pasada (DIETA-ESTADO.md, «Informe del revisor»): eje (a) 1 bloquea, 0 importa, 4 menor; eje (b) 0 bloquea, 2 importa, 1 menor. a1 (bloquea: la propia fila para este fichero repetía la trampa que cuenta; arreglada) y b1/b2 (la respuesta del consultor sin copiar al encargo, y la fase 0 sin auditor: arreglada y declarada). La fase 0 escribió en el informe el id del ADR 0087 con su guion, y ese ADR no existe, y knowledge validate tumbó el make check (25 min): la trampa de los ids inexistentes, otra vez, ahora en un INFORME de estado que solo cita la deuda; y el número de línea de los heredados salió corrido una línea por leerlo con sed sobre una línea en blanco, cazado al montar la tabla. | Antes de un make check, uv run botsito knowledge validate sobre el informe; los números de línea de PROJECT_STATE, con grep -n, no con sed -n de un rango. |`

## Informe del revisor (una pasada, 2026-11-13)

Pegado tal cual. Cita el id del ADR 0087 con su guion (hallazgo a1), así que va declarado aquí, como
exige `knowledge validate`:

```ids-inexistentes
ADR-0087 — lo cita el informe del revisor, pegado tal cual (hallazgo a1); no existe
```

> ## Informe del revisor · trabajo/dieta-estado · 2026-11-13
>
> La rama no está lista: hay un hallazgo que bloquea. La línea preparada para ERRORES-RECURRENTES, que todavía no está commiteada, escribe «ADR-0087» con guion. Ese ADR no existe, `knowledge validate` sale en rojo y el próximo `make check` no sellará. Es la misma trampa que esa línea describe. El trabajo sobre PROJECT_STATE.md está bien: las cuatro líneas acortadas cumplen (e), las cuatro están literales en HISTORIA y lo demás del fichero no cambia ni un byte.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 1 bloquea, 0 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | **bloquea** | La línea de ERRORES-RECURRENTES que el informe prepara (cambio sin commitear) cita «ADR-0087» con guion. Ese ADR no existe (`docs/adr/` salta de 0086 a 0088), así que `knowledge validate` falla. Con el informe como está, el próximo `make check` sale en rojo y no hay commit sellado posible. | `docs/validation/DIETA-ESTADO.md:340` («La fase 0 escribió «ADR-0087» con guion…»). `uv run botsito knowledge validate` → `ERROR: id citado que no existe: docs/validation/DIETA-ESTADO.md:340: ADR-0087`, exit=1. Se arregla escribiéndolo sin guion («ADR 0087», como en :113 y :200) o declarándolo en un bloque `ids-inexistentes`. |
> | a2 | menor | El informe atribuye al Current Feature los 31 bytes de diferencia entre la rama y `main`. En realidad son 16 del Current Branch y 15 del Current Feature. El total (24.043 con las cabeceras de main) sí es correcto. | `DIETA-ESTADO.md:56-57` y `:284`. Medido: línea 7, «main» 4 B → «trabajo/dieta-estado» 20 B; línea 10, 227 B → 242 B. |
> | a3 | menor | Tres ahorros de la tabla 0.3 no salen del corte válido más largo que el propio informe dice usar (`:42-44`). En `:114` el corte más largo está en el byte 110 (antes de «. ») y ahorra 37; el 55 sale del corte en el byte 92. En `:147` sale 47, no 48; en `:148` sale 12, no 13. Ninguna conclusión cambia: todas quedan por debajo de 60. | `DIETA-ESTADO.md:131`, `:164`, `:165`. Medido sobre `git show main:PROJECT_STATE.md` con el sufijo de README y la cita de la línea. |
> | a4 | menor | El motivo para no acortar `:142` es que el corte «cae dentro del trailer `Fuente:`». Eso no es una de las exclusiones de README (ruta o id), ni la que el informe declara (literal entre acentos graves): en PROJECT_STATE `Fuente:` no va entre acentos graves. Es una lectura más estricta que no se declara como tal. Acortarla ahorraría unos 169 bytes. Se queda por niega-por-defecto y el consultor la vio en la PARADA (opción 1, «tal cual las propones»), así que no cambia nada. | `DIETA-ESTADO.md:42`, `:159`, `:195-196`. `PROJECT_STATE.md:142` («…el trailer Fuente: de tramos_no_citables.yaml…»). Único corte ≤160: byte 53. |
> | a5 | menor | El informe cita el registro de cierre de F39a «hacia :17938-17941» como el que reescribe `:84`. La instrucción de reescribirla está en `HISTORIA.md:17944-17946`; :17936-17942 trata del ensayo D7. | `sed -n '17936,17946p' docs/state/HISTORIA.md`; `DIETA-ESTADO.md:62`. |
>
> Comprobado sin hallazgos:
> - **Contrato:**
>   - `uv run python scripts/contrato_rama.py` → `CONTRATO: 6 ficheros dentro del contrato de trabajo/dieta-estado (riesgo bajo, artefacto docs/validation/DIETA-ESTADO.md, tramo 'Carril: guardias y deuda', 4 comprobaciones para el revisor)`, exit 0.
>   - `uv run botsito state check` → OK, exit 0.
>   - `wc -c PROJECT_STATE.md` → 24074 (main 24652).
>   - `make check`: no lo ejecuté. `make-check.log` trae `SELLO: make check en verde sobre el arbol af74fa5c…`, que es `git rev-parse HEAD^{tree}`, con `3513 passed, 6 xfailed` y `PICO DE MEMORIA de make check: 318 MiB … el mayor proceso, 307 MiB`. Coincide con `DIETA-ESTADO.md:295-297`. Ese sello no cubre el informe sin commitear (a1).
> - **Trailer `Fuente:`:** ningún commit toca `knowledge/spec` ni `knowledge/cases`. El diff solo trae los 6 ficheros del contrato.
> - **Holdout:** no se toca nada. La fila de HOLDOUT-EXPOSICIONES del 2026-11-13 está en el commit de apertura (`b031559d`), con la forma de la de guardia-falsos-positivos.
> - **Regímenes de cambio:** ni evidence, ni feedback, ni manifests, ni corpus. HISTORIA solo se amplía: `main:HISTORIA` es prefijo exacto de `HEAD:HISTORIA`, sin CR añadidos. El Archivo 70 es `main:PROJECT_STATE.md` byte a byte, con un salto antes y otro después.
> - **Ambigüedades y ADR:** sin cambios en ninguno de los dos.
> - **Informes cerrados:** solo HOLDOUT-EXPOSICIONES, un registro vivo, con una línea añadida.
> - **Tres guardias de una `cita`:** no aplica.
> - **Pruebas:** pasan en verde, sobre el árbol de trabajo, `test_project_state`, `test_project_state_rutas`, `test_historia`, `test_kit`, `test_hoja_de_ruta`, `test_ids_citados`, `test_documentos_vivos` y `test_adr`. Ojo: `test_ids_citados` solo prueba repos sintéticos y no ve a1; la guardia real del repo es `knowledge validate`.
> - **Citas del informe comprobadas contra su fuente** (todas sostienen lo que se dice):
>   - `GUARDIA-FALSOS-POSITIVOS.md:224/225/228`
>   - `engine/laminas.py:534-536`
>   - `test_laminas.py:701`
>   - `graficos_sesion.py:66`
>   - `decisiones.py:7-8`
>   - `strategy_spec.yaml:2024`
>   - `freno.py:7-8`
>   - `test_hoja_de_ruta.py:60`
>   - `cli.py:2322`
>   - `MARGEN-PENDIENTE.md:510`
>   - `ACTIVAR-SESION-06-MOTOR.md:41-42`
>   - `HOJA-DE-RUTA.md:470/700/703/667-673`
>   - grep vacío de `Generado.mqh|generar_capa` en la skill `activar-sesion`, de `Fuente:|PLANTILLA` en `ingerir-sesion` y `abrir-rama`, y de «diagnostico» en `VISOR-DIAS.md`.
> - **Items de evidencia nuevos:** ninguno.
>
> **Alcance añadido por el encargo (punto 7):**
> 1. **Nada sale sin evidencia:** no sale ninguna línea. El diff de PROJECT_STATE frente a main cambia las líneas 7, 10, 84, 150, 151, 152, 167 y 171, y nada más.
> 2. **Literal en HISTORIA:** las cuatro líneas quitadas están byte a byte en el bloque `HISTORIA.md:18130`, y las cuatro que se ponen están literales en su «Queda en PROJECT_STATE:».
> 3. **Lo que se queda no cambia:** fuera de esas ocho líneas, PROJECT_STATE es idéntico al de main (172 líneas en los dos). Comparado línea a línea con Python.
> 4. **Las cuatro acortadas cumplen (e):** todas son de Technical Debt (`:81-152`) y ninguna estaba ya ACORTADA.
>
>    | PS | antes | arranque | después | ahorra | corte |
>    |---|---|---|---|---|---|
>    | :84 | 411 | 83 | 168 | 243 | antes de «: », el único ≤160 |
>    | :150 | 273 | 88 | 180 | 93 | antes de «: », el único ≤160 |
>    | :151 | 208 | 87 | 138 | 70 | tras «)» y antes de «; », el más largo |
>    | :152 | 502 | 130 | 299 | 203 | tras «)» y antes de «: », el más largo |
>
>    En las cuatro el arranque es prefijo literal de la línea entera, ninguno corta una ruta o un id, y el sufijo es el de README. `:151` lleva la cita en el arranque y el paréntesis no la repite; hay precedente en `PROJECT_STATE.md:94`. `:152` conserva sus dos citas, como fijó el consultor (punto 2).
> 5. **Ninguna sale por (b) o (d):** comprobado. Los registros de cierre de F38w a F39a (HISTORIA :16959, :17233, :17696, :17944) solo añaden o sustituyen deuda; ninguno la paga.
> 6. **HER:n:** `docs/plan/HOJA-DE-RUTA.md` no aparece en el diff, y no sale ningún heredado.
>
> **Cifras del informe** (son correctas salvo a2 y a3):
> - Bytes por sección: Next Action 5.619 + 895 = 6.514, Technical Debt 13.368 → 12.759, Reglas vivas 247 + 642 + 726 = 1.615.
> - Totales: 24.652, 24.683 y 24.074.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 2 importa, 1 menor. Requisitos: 19 hechos, 1 parcial, 1 no hecho.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Base comprobada (main, origin, tag, CI, ninguna otra rama, F39b libre) | Hecho (según el informe) | `DIETA-ESTADO.md:13-24`. No relancé `gh` ni `ls-remote`. |
> | 2 | Encargo tal cual, contrato y Archivo 70 | Hecho | `b031559d`. El Archivo 70 es idéntico a `main:PROJECT_STATE.md`. |
> | 3 | Contrato: tramo literal, riesgo bajo, rutas extra | Hecho | `contrato.yaml:2-11`; `HOJA-DE-RUTA.md:700` |
> | 4 | Informe con PLANTILLA en los primeros 600 caracteres | Hecho | `DIETA-ESTADO.md:3` |
> | 5 | Fila de HOLDOUT en la apertura, desviación declarada | Hecho | `HOLDOUT-EXPOSICIONES.md:147`; `DIETA-ESTADO.md:26-28`, `:289-290` |
> | 6 | Bajar PROJECT_STATE sin cambiar los criterios | Hecho | 24.652 → 24.074; README fuera del diff |
> | 7 | Lo que no cambia (letras, Known Ambiguities, secciones, ficheros) | Hecho | diff de 8 líneas (eje a, punto 3); 6 ficheros; contrato en verde |
> | 8 | Sin material, sin velas, sin arnés | Hecho (según el informe) | `DIETA-ESTADO.md:317`. Los dos guiones de fuera del repo no los puedo ver. |
> | 9 | (a)-(d) con evidencia y sección | Hecho | tabla 0.3, `:90-173`; no sale ninguna |
> | 10 | (e) solo Technical Debt, con sus reglas | Hecho | eje a, punto 4 |
> | 11 | Tres precisiones declaradas como del consultor | Hecho | `DIETA-ESTADO.md:37-40` |
> | 12 | Leer los heredados enteros y quitar su HER:n | Hecho (no aplica) | no sale ninguno; HOJA-DE-RUTA sin tocar |
> | 13 | Dudosas a una lista | Hecho | `:198-209`, con la línea de `:100` que pide R.4 |
> | 14 | Bloques al final de HISTORIA, con la forma de los que ya hay | Hecho | `HISTORIA.md:18130`; misma forma que `:16659` |
> | 15 | Fase 0: tabla, pagos de F38u-F39a, bytes, previsión y PARADA | Hecho | `:47-232`; PARADA en `89419ca0` |
> | 16 | Aplicar la respuesta R.1-R.4 | Hecho | fase 1, `:253-269`; diff de PROJECT_STATE |
> | 17 | Commits sellados y pico de cada `make check` | Parcial | Los tres picos están y `41983743` está sellado (log). El cambio sin commitear no puede sellar (a1). |
> | 18 | `wc -c` final | Hecho | `:302` = 24074, medido igual |
> | 19 | Informe completo y fila de ERRORES-RECURRENTES preparada | Hecho, con defecto | `:333-340`; la fila rompe `knowledge validate` (a1) |
> | 20 | Revisor pegado al final del informe | No hecho todavía | No hay sección «Informe del revisor». Lo pega la sesión: lo devuelvo, no lo pego. |
> | 21 | Sin CI de Linux | Hecho | La rama no toca código, hooks ni rutas. No veo nada que exija CI de Linux. |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | La respuesta del consultor a la PARADA no está copiada al final del encargo; solo está en el informe. La skill `fase-cero` pide copiarla en los dos sitios, y así lo hicieron las ramas anteriores. | `tail docs/encargos/trabajo-dieta-estado.md` acaba en «Rama lista para revisión, NO cerrada.». `.claude/skills/fase-cero/SKILL.md:90`. Precedentes: `docs/encargos/trabajo-margen-pendiente.md:118`, `trabajo-guardia-falsos-positivos.md:64`. |
> | b2 | importa | La fase 0 no lanzó el `auditor-encargo` y el informe no tiene «El encargo frente al repo», y no se declara por qué. | `grep -i "auditor\|frente al repo"` sobre el informe → vacío. `fase-cero/SKILL.md:60-63`; `CLAUDE.md` («`auditor-encargo`: al empezar la fase 0»). |
> | b3 | menor | La tabla «El encargo, punto por punto» da por «Hecho» el punto 7 remitiendo a «Informe del revisor», abajo, una sección que aún no existe. | `DIETA-ESTADO.md:328` (sin commitear) |
>
> Lo que la rama hace y el encargo no pide: nada. El repaso extra de 0.2 (ADR 0087, RN-019 y lo demás) es inventario.
> Lo que el encargo dice que no se toca: no se toca. Ni README, ni src, ni tests, ni `.claude`, ni knowledge, ni HOJA-DE-RUTA aparecen en `git diff --stat main...HEAD`.
>
> ### Lo que no pude comprobar
> - La base contra origin y la CI de main (run 43459199788): necesitan red o `gh`. Me quedo con la tabla del informe.
> - Que el encargo es el prompt tal cual: no tengo el mensaje original.
> - Los dos guiones de la carpeta de trabajo, fuera del repo, que midieron los bytes. Repetí las cifras con Python sobre `git show`.
> - Los `make check` de la apertura y de la fase 0: solo queda el log del último. Sus picos solo los da el informe.
> - Que la sesión corrió en Opus con esfuerzo medio (requisito 0.6).
> - `make check` sobre el informe sin commitear: escribe y no lo ejecuto. `knowledge validate` ya muestra que fallaría.
>
> ### Comandos ejecutados
> 1. `git branch --show-current; git merge-base main HEAD; git log --format='%h %s' main..HEAD; git diff --stat main...HEAD; git status --short`
> 2. `cat docs/encargos/trabajo-dieta-estado.md; cat contrato.yaml`
> 3. `uv run python scripts/contrato_rama.py`
> 4. `uv run botsito state check; wc -c PROJECT_STATE.md; git show main:PROJECT_STATE.md | wc -c`
> 5. `git diff main...HEAD -- PROJECT_STATE.md`
> 6. `grep -n "" docs/state/README.md`
> 7. `grep -n "" docs/validation/DIETA-ESTADO.md` (entero) y `git diff -- docs/validation/DIETA-ESTADO.md`
> 8. `grep -n "ADR-0087…" DIETA-ESTADO.md PROJECT_STATE.md; ls docs/adr | tail`
> 9. Grep de `ids-inexistentes` y Read de `src/botsito/validation/ids_citados.py`
> 10. `uv run pytest -q -p no:cacheprovider tests/contract/test_ids_citados.py`
> 11. `uv run python -c` (gramática `ids.FUENTE` sobre ADR-0087)
> 12. `uv run botsito knowledge validate` → exit 1, ERROR en `DIETA-ESTADO.md:340`
> 13. `grep -n` del bloque ACORTADA en HISTORIA; `sed -n '18120,18147p' docs/state/HISTORIA.md`
> 14. Python por stdin: comparación byte a byte de PROJECT_STATE (main/HEAD) y del bloque de HISTORIA
> 15. Python por stdin: cortes válidos ≤160 de cada línea de Technical Debt de más de 200 bytes, y ahorro de cada candidata
> 16. `git show main:PROJECT_STATE.md | sed -n` (las líneas candidatas y la numeración)
> 17. `grep -n` del precedente `:94` y de los bloques ACORTADA; `sed -n '16659,16700p'` de HISTORIA
> 18. Python por stdin: bytes por sección de main, `b031559d` y HEAD (un primer intento con f-string lo bloqueó la guardia; lo repetí con refs literales)
> 19. Python por stdin: HISTORIA solo se amplía y el Archivo 70 es igual a main
> 20. `git diff main...HEAD -- docs/validation/HOLDOUT-EXPOSICIONES.md; git log --name-status main..HEAD`
> 21. `ls -la make-check.log; grep SELLO/PICO/passed; git rev-parse HEAD^{tree}`
> 22. `sed -n` de las citas: `GUARDIA-FALSOS-POSITIVOS.md`, `laminas.py`, `test_laminas.py`, `graficos_sesion.py`, `decisiones.py`, HISTORIA :17936-17953, `strategy_spec.yaml`, `freno.py`, `test_hoja_de_ruta.py`, `cli.py`, `MARGEN-PENDIENTE.md:510`, `ACTIVAR-SESION-06-MOTOR.md:41-42`, `HOJA-DE-RUTA.md`; los grep de las skills y de `VISOR-DIAS.md`
> 23. `grep` de los registros de cierre y awk de los cambios de Technical Debt en HISTORIA de F38w a F39a; `sed` de los de F38y, F38x y F38z
> 24. `grep`/`sed` de `.claude/skills/fase-cero/SKILL.md`; `grep` de auditor y respuesta en informe y encargos (también los de las ramas anteriores)
> 25. `uv run pytest -q -p no:cacheprovider` de los 8 ficheros de test → verde
> 26. `git show --numstat 41983743 / b031559d -- PROJECT_STATE.md` (un `git diff` que nombraba `data` lo bloqueó la guardia; lo sustituye el `--stat` del punto 1)

## Lo que se hizo con los hallazgos del revisor

- **a1 (bloquea)**: arreglado. La fila preparada para ERRORES-RECURRENTES ya no escribe el id con
  guion («el id del ADR 0087 con su guion»); el informe del revisor, que sí lo cita, va con su bloque
  `ids-inexistentes` delante. `uv run botsito knowledge validate` en verde antes del `make check`.
- **a2 (menor)**: corregido en 0.1 y en la fase 1: 16 bytes de Current Branch y 15 de Current Feature.
- **a3 (menor)**: corregidas `:114` (37), `:147` (47) y `:148` (12) en la tabla 0.3 y en 0.4. Ninguna
  conclusión cambia. La de `:114` venía copiada de MARGEN-PENDIENTE.md, que la midió con otro corte.
- **a4 (menor)**: declarado como desviación 5. `:142` se queda; si se acorta, lo decide el consultor.
- **a5 (menor)**: corregida la cita, ahora `HISTORIA.md:17944-17946`, en 0.2 y en la fila `:84` de 0.3.
- **b1 (importa)**: arreglado. La respuesta, copiada tal cual al final de
  `docs/encargos/trabajo-dieta-estado.md`; desviación 6.
- **b2 (importa)**: declarado como desviación 4. No se lanza ahora: la fase 0 ya pasó y el revisor
  repitió las comprobaciones que el auditor habría hecho (las citas, contra su fuente, todas buenas).
- **b3 (menor)**: resuelto al pegar esta sección.

Sin CI de Linux: ni el revisor ni la sesión ven nada que la exija (encargo, punto 7).

## Estado

Rama lista para revisión, NO cerrada.
