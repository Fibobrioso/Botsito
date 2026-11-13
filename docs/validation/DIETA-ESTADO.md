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

(En la rama, con su Current Feature, 24.683 → 24.074; el Current Feature de la rama es 31 bytes más
largo que el de `main`.)

### 0.2 Lo que pagaron las ramas desde el último recorte (F38u a F39a), comprobado

- **cmp / G.6 (F39a)**: ninguna línea de Technical Debt nombra `cmp` ni G.6; la de `:84` ya la
  reescribió el cierre de F39a (registro de cierre, HISTORIA hacia :17938-17941) y lo que dice sigue
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
| :84 | La guardia niega a un guion nuevo dos falsos positivos, … | 411 | **(e)** | 411 -> 168, ahorra 243; F1 sigue aplazado y el `/` de `compilar.py` sigue negado (GUARDIA-FALSOS-POSITIVOS.md:224 y registro de cierre de F39a, HISTORIA hacia :17938-17941): no pagada |
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
| :114 | La ingesta asigna la sesión con el reloj del registro y … | 216 | se queda | (e) ahorraria 55 (MARGEN-PENDIENTE.md §0.h.2) |
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
| :147 | La comparación de motor decisiones mira cada operación… | 265 | se queda | el corte valido mas largo (142) ahorraria 48 (< 60) |
| :148 | El toca_colocar_orden_limite sintético de tests/unit/t… | 246 | se queda | el corte valido mas largo (160) ahorraria 13 |
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
`:100`, `:107` 29, `:110`, `:114` 55, `:115` 27, `:116` 46, `:147` 48, `:148` 13, `:149`) o no tienen
corte estricto en 160 (`:102`, `:130`, `:132`, `:146`; y `:142`, cuyo único corte caería dentro del
trailer `Fuente:`).

### 0.5 Dudosas (se quedan; para el consultor)

1. `:96` «ADR 0087 (S-15, no existe) sigue en los `ids-inexistentes`…»: la numeración ya pasó de
   0087 (existen 0088 a 0093; `trabajo/activar-sesion-06-motor` dejó el 0087 reservado para S-15 y
   numeró su ADR 0089, ACTIVAR-SESION-06-MOTOR.md:41-42); podría ser (c) si ningún ADR va a llevar
   ya ese número, pero eso lo decide el consultor, no un hecho del repo.
2. `:100` «El visor no conecta `--diagnostico-cuenta-diaria` (cli.py:2558; el arnés sí, :2438)»:
   la deuda sigue viva (la opción solo existe en un parser, `cli.py:2322`), pero sus números de línea
   ya no casan. No hay criterio para corregirlos; se queda como está.
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

## Estado

PARADA de la fase 0 (encargo, punto 4): la previsión queda en 24.043 bytes, por encima de 24.000. PROJECT_STATE.md no se ha tocado más allá de la apertura. Espera la decisión del consultor.
