# HOJA-DE-RUTA · El mapa vivo de lo pendiente y las guardias que lo cuadran (entradas F y P)

Rama `trabajo/hoja-de-ruta`, abierta el 2026-10-10 desde `main` en 2a007b7 (commit de estado sobre
el merge f472e06, tag `stable/F37j-cases-rejilla`). Encargo: `docs/encargos/trabajo-hoja-de-ruta.md`.

Antes de abrir se comprobó con git: `main` = `origin/main` = 2a007b7;
`git rev-parse "stable/F37j-cases-rejilla^{commit}"` = f472e06; la CI de `main` sobre 2a007b7 en
`completed` / `success` (API de check-runs con el sha literal); `git branch -a` solo da `main` y
`origin/main`, y `git ls-remote --heads origin` solo `main` (ningún `fix/*`).

## 0. Fase 0 · Inventario, sin escribir nada

Medido el 2026-10-10 sobre 2a007b7. La lectura de (c), (d) y (e)-(g) la hicieron tres subagentes
de solo lectura con las reglas del holdout por escrito en su encargo; lo que se usa aquí de ellos
se volvió a medir en la sesión donde se dice («verificado»). Nada de la cruda, de la cuarentena,
del holdout ni de `data/`.

### 0.a La Next Action y los pendientes heredados, con su estado medido

**La Next Action** (`PROJECT_STATE.md`, «Next Action»; letras vivas, medidas con un guion: A B C D
E F G H I J K L M N O P S X).

| Letra | Qué es | Estado medido | Evidencia |
|---|---|---|---|
| S | backtest de julio, sin abrir | viva | sin rama ni manifiesto de julio que lo ingiera |
| B | la guardia no lee lo que un guion importa o ejecuta | viva | GUION-MISMO-COMANDO.md §0.c; sin rama |
| C | la guardia no ve rutas protegidas compuestas | viva | GUION-MISMO-COMANDO.md, hallazgo 5 |
| D | endurecer la guardia por formas raras | viva | GUION-MISMO-COMANDO.md §1.26 |
| X | `scripts/ticks_spread.py` a la rejilla | viva | ACTIVACION-A42.md §6.2; CASES-REJILLA.md no lo toca (era X) |
| F | orden tras W: esta rama, entorno-code, E | viva, **con dependencia colgante** (W ya salió HECHA) | 0.b |
| E | activar la sesión 4 | viva | 0.c (las ABIERTA de la sesión 4) |
| G | PREREGISTRO y F26 | viva | 0.e |
| I | backtest de diciembre de 2025, sin abrir | viva | entró en el cierre de W |
| J | `kit hoja` roto para todo paquete nuevo | viva | CASES-REJILLA.md §3.6 y §3.8 |
| P | origen de «QUIEN: el consultor» | viva (la cierra esta rama) | 0.g |
| A | ejecuciones 2 y 3 de MedirDemoFTMO | viva | DEMO-FTMO.md; A-28 ABIERTA (`ambiguedades.yaml:662`) |
| O | P-D1 a FTMO | viva (respuesta pendiente) | DEMO-EJECUCION-1.md §0.c |
| K | falso positivo de `exigir_sin_crudo` | viva | DEMO-EJECUCION-1.md |
| H | RN-007, el umbral de «casi plana» | viva | S-14 «en parte» (SESION-04-EXTRACCION) |
| L | revisión de `ev-v7-001550-82e5cffc` | viva | `git log -S` solo da las copias de PROJECT_STATE en HISTORIA; ningún informe la revisa |
| M | BE de una venta que salta por el ASK | viva | DEMO-EJECUCION-1.md §0.h (:297-303): la ejecución 1 no lo mide |
| N | calendario de cierres por condición | viva | RENOVAR-CIERRES.md |

**Los pendientes heredados** (el texto entero está en el primer Archivo de `docs/state/HISTORIA.md`
que los trae completos, líneas 684-729; desde `trabajo/adelgazar-estado` PROJECT_STATE los corta con
«…» y remite a `docs/state/README.md`, **que no tiene ese texto**: la remisión de
`PROJECT_STATE.md:63` apunta al sitio equivocado; el texto está en HISTORIA).

| N.º | Qué pide (resumen de su texto entero, HISTORIA:línea) | Estado medido | Evidencia |
|---|---|---|---|
| 2 | marzo: el xlsx al corpus, marzo a `vistos.yaml`, su `cobertura_material` y la confirmación escrita del trader (HISTORIA:684) | **superado en parte**: el xlsx está en el corpus (REGISTRO-MARZO.md §2, punto 1); faltan `vistos.yaml` (`grep -c "2026-03" knowledge/cases/kit/vistos.yaml` = 0), la cobertura (paso a) y la confirmación | CASES-REJILLA.md §3.7 |
| 6 | febrero no se toca ni se descarga (HISTORIA:696) | viva (regla) | no hay manifiesto `eurusd-m1-2026-02` en `data/manifests/` |
| 7 | junio: la guardia y los once días reservados que un `kit build` nuevo podría poner en `dev` (HISTORIA:698) | viva | sin evidencia de arreglo |
| 8 | el brief para abrir los 4 `dev` de septiembre (HISTORIA:700) | viva | CASOS-AGOSTO-ABRIL.md: quedan fuera porque solo los cubre el libro de septiembre, sin sha |
| 9 | re-descargar un mes rompe `kit build` en silencio (`reemplaza_a` no se lee) (HISTORIA:701) | viva | sin evidencia de arreglo |
| 10 | Aleks: el panel de FTMO, la prueba gratuita, medir A-27 y A-28, grabar spread y ticks (HISTORIA:702) | **superado en parte**: prueba abierta y A-27 DECIDIDA (ADR-0071); quedan A-28 (NA:A) y el grabador (F17, 0.d) | `ambiguedades.yaml:620` y `:662` |
| 12 | marzo entra por su propia rama, con `libros.yaml` medido por velas (HISTORIA:704) | viva | ENTRADA-MARZO.md pasos c y d |
| 15 | A-18: la pregunta de reserva enviada al trader el 2026-09-23; con la respuesta se decide si A-18 se replantea (HISTORIA:707) | **superado en parte**: S-3 de la sesión 4 la responde, «resuelve»: el stop va ya en el 0,8 al poner la orden y el objetivo es 3 veces 0→1 (SESION-04-EXTRACCION.md:413-437 y :935); A-18 sigue ABIERTA (`ambiguedades.yaml:329`) hasta la activación (NA:E) | verificado |
| 25 | RN-004 bloqueada solo por A-35 (HISTORIA:717) | viva | A-35 ABIERTA (`ambiguedades.yaml:905`); S-11 «en parte» |
| 27 | Aleks con FTMO: noticias y gap trading, el lote variable, la «maximum capital allocation rule», el asterisco de «USD/LOT*», medir A-27/A-28, comisión por lado, cifra de la guardia de tamaño (HISTORIA:719) | **superado en parte** (abajo) | FTMO-REGLAS.md, ADR-0068, ADR-0071 |
| 30 | RN-004 tras A-35, medida con el arnés (HISTORIA:722) | viva | A-35 ABIERTA |
| 34 | (a) la ventana de ticks de invierno; (b) el deslizamiento; (c) el swap (HISTORIA:726) | **superado en parte**: (a) es NA:X (ADR-0069 §5); (b) y (c) los miden las ejecuciones 2 y 3 (NA:A: «los deslizamientos (DN-3) y los swaps») | `PROJECT_STATE.md`, entrada A |
| 35 | RN-020 tras A-44 (HISTORIA:727) | viva | A-44 ABIERTA (`ambiguedades.yaml:1209`); S-9 «en parte»; los seis `perdida_trader_*` UNKNOWN |
| 37 | los rechazos por volumen máximo, con A-18 (HISTORIA:729 y la coda de PROJECT_STATE) | viva | NA:O decide el recorte |

**El 27, punto por punto:**

| Pregunta | Estado | Evidencia |
|---|---|---|
| noticias en Swing frente a gap trading | respondida (2026-10-05); queda la pregunta 6 de A-55 sin respuesta | `FTMO-REGLAS.md:226-235`; ADR-0068 |
| si un lote variable a riesgo constante es «substantially larger» | respondida SIN CIFRA; no se repregunta (decisión del consultor) | `FTMO-REGLAS.md:236` |
| `firma_tamano_posicion_ratio_aviso` | **sigue UNKNOWN**, y su descripción todavía dice «PENDIENTE PARA ALEKS con FTMO (Next Action 27)» | `knowledge/cuentas/ftmo-2step-swing-100k.yaml:458-466` |
| la «maximum capital allocation rule» | **viva**: NO ENCONTRADA en ninguna página | `FTMO-REGLAS.md:61` y `:309` |
| el asterisco de «USD/LOT*» | **viva** | `FTMO-REGLAS.md:59` y `:310` |
| la comisión, por lado o por operación | HECHA: por lado, CONFIRMADO como hecho medido | ADR-0071 §3 |
| medir A-27 y A-28 | A-27 DECIDIDA (ADR-0071); A-28 ABIERTA, la miden las ejecuciones 2 y 3 (NA:A) | `ambiguedades.yaml:620`, `:662` |

### 0.b Dependencias colgantes

Guion de lectura sobre la Next Action (patrón «después de», «antes de», «espera a», «junto a» y
«tras», con y sin tilde; las letras mayúsculas sueltas que siguen):

| Entrada | Frase | Letras | ¿Vivas? |
|---|---|---|---|
| S | «DESPUÉS de la activación de la sesión 4 (E)» | E | sí |
| **F** | **«tras W (consultor, 2026-10-10)»** | **W** | **NO: W salió HECHA en el cierre de `trabajo/cases-rejilla`** |
| E | «después de F» | F | sí |
| I | «después de X, S y E» | X, S, E | sí |
| K | «junto a B o C si cabe» | B, C | sí |
| J, A, H, N | «antes de la próxima sesión…», «antes de la ejecución 2…», «espera a la pregunta 14…», «antes de que el bot corra…» | ninguna letra | n/a (dependen de hechos, no de letras) |

La única colgante hoy es **F frente a W**. El test (c) tiene que fallar con el `main` de hoy por ella.

### 0.c Las ambigüedades que las sesiones dan por respondidas y siguen ABIERTA

- **SESION-02-EXTRACCION.md es una PLANTILLA sin contenido** (líneas 1 y 5): no tiene tabla final ni
  ninguna fila `A-nn` con veredicto. El test la tiene que saltar sin fallar.
- **SESION-03-EXTRACCION.md**, `## 5. Tabla de propuestas` (línea 870; cabecera 872, filas
  874-902). Columna 1 el código (mezcla `A-nn` con S-1, G-1..3, E-1..3); columna 2 la propuesta:
  `resuelve`, `resuelve en parte…`, `resuelve con lectura NUEVA…` y `no resuelve` (que contiene la
  subcadena «resuelve»: el patrón se ancla al principio).
- **SESION-04-EXTRACCION.md**, `## 5. Tabla final` (línea 928; cabecera 930, filas 932-955).
  Columna 2 la ambigüedad (a veces dos, «A-30, A-39», o no es un `A-nn`: «ADR-0061 §2», «RN-007»,
  «marzo»); columna 4 la propuesta: `**resuelve**: …` o `en parte…`. Recuento del propio informe
  en su línea 957 (verificado).

Las que siguen ABIERTA (estados de `knowledge/spec/ambiguedades.yaml`, medidos con un guion):

| A-nn | Sesión 4 | Sesión 3 | Parámetro y estado | Código |
|---|---|---|---|---|
| A-13 | en parte (S-24) | en parte | `break_even_criterio_ruptura` CONFIRMED | sí |
| A-18 | resuelve (S-3) | en parte | `base_calculo_objetivo`, `objetivo_rr` CONFIRMED | sí: falta cerrarla |
| A-21 | resuelve (S-10) | en parte, lectura nueva | `zona_control_limpia` UNKNOWN; sus dos opciones no recogen la respuesta | selector sí; **probable falta** (la opción nueva) |
| A-25 | resuelve (S-18) | en parte | `cartuchos_reinicio` CONFIRMED; `intentos_tras_toma_nueva` DEFAULT_AMBIGUOUS | sí |
| A-30 | resuelve (S-5) | en parte | `parametros: []`; `orden_pendiente_al_abrir_sesion` (con `ambiguedad_id: A-30`) DEFAULT_AMBIGUOUS | sí |
| A-32 | en parte (S-23) | — | `breaker_m1_criterio_ruptura` CONFIRMED | sí |
| A-33 | resuelve (S-12) | — | `parciales` CONFIRMED | sí: falta cerrarla |
| A-35 | en parte (S-11) | en parte | `liquidez_m15_pivote_formado` UNKNOWN | selector sí; falta el valor |
| A-36 | resuelve (S-22) | — | `parametros: []` | **falta** (nada expresa «en el 0 con mecha, sin spread») |
| A-39 | resuelve (S-5) | en parte, audio | `parametros: []` | sí en lo esencial |
| A-43 | en parte (S-15) | en parte | `toma_antes_de_la_ventana` DEFAULT_AMBIGUOUS | sí |
| A-44 | en parte (S-9) | resuelve con lectura nueva | los seis `perdida_trader_*` UNKNOWN | sí: faltan los valores |
| A-49 | en parte (S-1, S-2), resuelve (S-4) | — | `caja_se_fija` DEFAULT_AMBIGUOUS; el selector `caja_vela` no existe | **falta** |
| A-50 | en parte (S-17) | no resuelve | `parametros: []` | n/a (sin respuesta) |
| A-51 | resuelve (S-8) | — | `parametros: []` | **falta** (ningún parámetro expresa qué corta la racha) |
| A-52 | resuelve (S-20) | — | `max_escenarios_por_sesion` DEFAULT_AMBIGUOUS | sí |
| A-53 | en parte (S-21) | — | `orden_pendiente_al_abrir_escenario` DEFAULT_AMBIGUOUS | sí |

**Contra la entrada E:** sus «17 ambigüedades … siguen ABIERTA» cuadran (de las 18 de la sesión 4,
solo A-42 está RESUELTA). «Parámetro con valor (A-52, A-30, A-25, A-18, A-33, A-13)» cuadra con dos
matices: A-52 tiene valor pero DEFAULT_AMBIGUOUS, y A-30 no tiene parámetros propios (el que lleva
valor la cita por `ambiguedad_id`). «Falta código en A-21, A-51, A-36 y A-49»: la medida sostiene
A-51, A-36 y A-49; A-21 solo a medias (el selector existe; falta la opción que da la respuesta).
Las nueve ABIERTA de la sesión 3 están todas entre las de la sesión 4: la unión son esas mismas.

### 0.d F01-F35 de MASTER_PLAN.md §A, por el contenido

`docs/plan/MASTER_PLAN.md`, `## A · Fases y funcionalidades` (línea 67), tabla en 69-113; cada
funcionalidad es una fila `| Fnn | …` con el id en la primera celda; las filas de fase van en
negrita y no son ids. **El último cambio de MASTER_PLAN.md es del 2026-09-16** (`5c49127`); §E
(líneas 134-138) es el orden prescrito, sin estado. `docs/plan/features/` solo tiene fichas F01-F15
(y `F14b`, PROPUESTA). Desde F16 los tags `stable/F16..F37` son contador (p. ej.
`stable/F26-demo-ftmo-script` es el script de la demo, no la F26 del plan; `F35-ORDEN-STOP-PIVOTE.md`
no es la F35).

| Estado | Funcionalidades | Prueba |
|---|---|---|
| HECHA | F01-F13, F15 | tags `stable/F01`..`stable/F13`, `stable/F15`; sus informes en `docs/validation/Fnn-*.md` |
| HECHA (con ambigüedades abiertas) | F18 (tipos y sesgo H4), F19 (zonas M15), F20 (M1, breaker), F21 (caja, stop, lote, objetivo, BE) | `MOTOR-SESGO-H4.md`, `LIQUIDEZ-M15.md`, `BREAKER-M1.md`, `BE-AL-TICK.md`, `BLOQUE-DE-LA-CAJA.md`; módulos de `domain/` y `engine/` |
| PARCIAL | F14 (casos y particiones: hechos; sin cierre formal), F16 (ticks congelados en CSV, no Parquet), F17 (solo el script de medición, no el grabador continuo), F22 (motor como intérprete de la spec, no statechart), F23 (bucle y reloj; sin journal), F24 (broker, llenado y cuenta; sin contador de N), F25 (visor de días, no el de tres marcos), F33 (entorno de la demo, cierres y freno; sin pre-vuelo ni EA) | `TICKS-LLENADO.md`, `DEMO-EJECUCION-1.md`, `CABLEADO-SIMULADOR.md`, `VISOR-DIAS.md`, `RENOVAR-CIERRES.md`, `FRENO-PETICIONES.md` |
| SIN EMPEZAR | F26 (preparada: criterio, comparador, particiones; PREREGISTRO sin rellenar), F27, F28-F32, F34, F35 | `PREREGISTRO.md:1-3`; `src/botsito/mql5bridge/` solo `__init__.py` |

Reserva del subagente, que se mantiene: F14, F22 y F23 se clasifican PARCIAL por sus módulos, sus
fichas y las ambigüedades, sin revisar cada informe a fondo.

### 0.e Las condiciones previas de F26 (entrada G)

- **`docs/validation/PREREGISTRO.md`**: existe y está SIN RELLENAR (líneas 1 y 3: «NO SE PUEDE ABRIR
  NINGUN HOLDOUT»). Pide (líneas 15-24) la métrica exacta, el umbral y qué pasa si no se alcanza, la
  partición y por qué, quién autoriza y cuándo (ADR-0021), las exposiciones que la afectan y qué se
  hace si falla. Al trader (líneas 26-33): «un mes que no haya tocado». Sus líneas 28-30 (cifras de
  mayo) no están contrastadas con el estado de hoy.
- **«Una pregunta abre N particiones»** (Technical Debt; texto entero en HISTORIA, Archivo 1, línea
  570): `kappa_entre_sesiones` abre todas las particiones con etiqueta de las dos rondas; el llamante
  no puede nombrar la que pregunta. Arreglo: rama propia de código en la puerta, antes de la primera
  autorización. No depende de ninguna ambigüedad.
- **«Los dos días del universo de la sesión 1 sin partición»** (HISTORIA, Archivo 1, línea 569;
  ADR-0035 §Impacto; UNIVERSO-CONGELADO.md §2b): el universo es mayor que el paquete por los cupos;
  dos días no están en ninguna partición. Pide una decisión del consultor: qué conjunto es «el
  universo» para F26.
- **«F26 no puede puntuar el objetivo hasta que A-18 esté cerrada»** (HISTORIA, Archivo 1, línea
  563): depende de A-18, que la sesión 4 responde (S-3, 0.a) y queda para la activación (NA:E).
- **A-16** (`ambiguedades.yaml:280`): ABIERTA, clase `medicion`, `resuelve_en: [F26]`: cuánto se
  separan las velas de Oanda (las del trader) de las de Dukascopy.

### 0.f Herencias sin dueño visible

- **El refiltrado de las filtradas v7–v10** que E dice heredar («HISTORIA, entrada Q»): **la parte
  (1) ya está HECHA** en la fase 0 de `trabajo/activacion-a42`: «las filtradas de v7–v10 rehechas
  con `--solo-filtrar --video` y medidas por marcas; ninguna diferencia» (ACTIVACION-A42.md:18 y
  §2.2, líneas 117-129, verificado). La frase de E parece heredada sin actualizar; lo que la hoja de
  ruta tiene que decir de ella lo decide el consultor (PARADA, punto 3).
- **La copia de seguridad** (Technical Debt, «HECHA HASTA v5, INCOMPLETA desde el 2026-09-09»; texto
  entero en HISTORIA, Archivo 1, línea 579): falta v6 (la sesión 1), y el texto no cuenta v7–v10.
  SESION-02-INVENTARIO.md:328 la asigna al consultor; ninguna entrada viva la nombra. Va al carril
  de Aleks.
- **Las candidatas C1–C7** (Technical Debt, `PROJECT_STATE.md:110`; DISENO-ENTRADA-RUPTURA.md §2.8,
  líneas 341-360): C2 y C3 ya son A-48 y A-49 (las dos ABIERTA); C4 (el stop en dos tiempos y la
  orden sin stop de v8 n.º 1; toca A-18 y A-11) queda **superada en parte por S-3**: el stop va en
  el 0,8 desde el principio, no en dos tiempos; la orden sin stop de v8 n.º 1 no la contesta. C5
  toca A-29 (RESUELTA, `ambiguedades.yaml:704`); C6 toca A-36 (ABIERTA otra vez,
  `ambiguedades.yaml:944`). C1, C5, C6 y C7 siguen sin abrir y sin dueño.

### 0.g P: de dónde sale «QUIEN: el consultor»

**De ningún ADR** (verificado). La introdujo el commit `52c0220` (2026-09-20, «la regla del backtest
estaba mal escrita, y es la segunda vez»; `git log -S "QUIEN" -- CLAUDE.md`), en la rama de la
entrada de septiembre: sustituyó «hasta que sus particiones estén sorteadas» por «lo mínimo para
fijar el universo», con tres ataduras (QUIEN, CUANDO, QUE). Su fuente es un informe, no un ADR:
SEPTIEMBRE-ENTRA.md §1 (líneas 9-13: «El consultor abrió … y leyó la columna de fechas») y §2b.
Ningún ADR dice «el consultor» de esta lectura: ADR-0021 §1 no nombra a nadie; ADR-0039 §1 (nota
del 2026-09-24) y ADR-0046 §6a dicen «Aleks» para marzo.

Y hay una ambigüedad de fondo que el repositorio no resuelve: si «el consultor» y «Aleks» son la
misma persona. CLAUDE.md habla de «orden de cierre explícita de Aleks, dada tras la revisión del
consultor» (dos papeles), y SEPTIEMBRE-ENTRA.md §1 describe al consultor abriendo el xlsx en Excel
(un acto humano). Ningún documento los define.

Dos opciones:

- **(A) Corregir CLAUDE.md**: «QUIEN: Aleks» (o «el humano que lleva el proyecto»), citando la
  decisión del 2026-09-20 (SEPTIEMBRE-ENTRA.md §2b) y, para marzo, ADR-0046 §6a. Barata y local;
  la atadura sigue sin ADR.
- **(B) Un ADR**: «Quién lee la columna de fechas de un backtest para fijar el universo»: el QUIEN
  (Aleks), el CUANDO (una vez, antes del sorteo), el QUE (solo la columna de fechas), la declaración
  el mismo día, ADR-0046 §6a como su caso de marzo, y el origen en SEPTIEMBRE-ENTRA.md §2b. CLAUDE.md
  remite a él en una línea.

Recomiendo **(B)**: es la regla que aplica a todo backtest que viene (julio, diciembre), y CLAUDE.md
pide que una prohibición se pueda revisar contra su ADR. Pero el QUIEN lo tiene que decir el
consultor: si es Aleks, o si «el consultor» es otro papel que delega.

### 0.h La hoja de ruta frente a las dos guardias de documentos

- **`tests/contract/test_documentos_vivos.py`**: su `RECUENTO` caza un número pegado a «parámetros»,
  «reglas», «ambigüedades», «preguntas», «registros de feedback», «ítems de evidencia» o «términos»
  (líneas 33-36), con una exención por línea `<!-- cifra-congelada: <motivo> -->`. La hoja de ruta
  entra en `VIVOS` (líneas 45-52) y **nombra ids, nunca recuentos**: «las ABIERTA de la sesión 4
  (ID:A-13, ID:A-18, …)», no «17 ambigüedades». Así encaja con lo que pide el encargo y con el test.
- **`tests/unit/test_project_state_rutas.py`**: toda ruta `docs/…` citada en PROJECT_STATE tiene que
  existir (`_RUTA`, línea 16). `docs/plan/HOJA-DE-RUTA.md` solo existe desde esta rama: la F
  reescrita del cierre (que la cita) entra en el commit del contrato, cuando el fichero ya existe en
  la rama, así que pasa. La F de hoy no la cita como ruta (cierre de W: «HOJA-DE-RUTA.md, nueva en
  docs/plan/»).

### 0.i El diseño que se propone para la fase 1

- **El formato de la hoja de ruta**: secciones `## R0` … `## R7`, `## Carril: Aleks`,
  `## Carril: guardias y deuda`, `## Carril: material reservado`, `## F01-F35` y
  `## Fechas fijas`; cada entrada, un `### ` con sus referencias en una línea `Refs:` (`NA:E`,
  `HER:15`, `ID:A-18`, `F:F26`) y cuatro campos: qué es, de qué depende, quién, criterio de hecho.
  Una entrada hecha lleva `Estado: HECHA` y el test comprueba que su `NA:`/`HER:` ya no está viva.
- **El test** (`tests/unit/test_hoja_de_ruta.py`), negando por defecto, con funciones puras que
  reciben textos (los de verdad en el test real, sintéticos en los que rompen a propósito):
  (a) toda letra viva y todo heredado vivo aparece como `NA:`/`HER:`; (b) toda referencia existe
  (`NA:` letra viva o marcada HECHA en HISTORIA, `HER:` en la lista de PROJECT_STATE, `ID:` en
  `ambiguedades.yaml`, `docs/adr/` o `strategy_spec.yaml`, `F:` en §A) y ninguna HECHA sigue viva;
  (c) ninguna dependencia de la Next Action apunta a una letra no viva (falla hoy por F → W);
  (d) toda ABIERTA de las tablas de 0.c aparece como `ID:` en R1 o R4. El test de verdad corre
  sobre los ficheros del repo; los sintéticos rompen cada sentido.
- **El campo `tramo`**: `contrato_rama.py` lo admite como clave, y lo exige si
  `docs/plan/HOJA-DE-RUTA.md` existe en el merge-base con `main` (así no rige para esta rama, cuya
  base no la tiene, y rige desde la siguiente sin tocar este contrato); su valor tiene que ser un
  `## R…` o un carril de la hoja de ruta. `abrir-rama` lo pide; CONTRATO-DE-RAMA.md lo documenta.
- **RITUAL.md y `cerrar-rama`**: en el punto 3 del commit del contrato, «junto a la Next Action se
  actualiza la hoja de ruta»; las puertas existentes no cambian (se revisa línea a línea contra
  `main` en la fase 1).
- **MASTER_PLAN.md**: un recuadro al principio, con fecha y rama.
- **Bytes de PROJECT_STATE**: la rama no le añade nada en la Next Action (las líneas del cierre se
  preparan en el informe); el saldo de esta rama sobre él es hoy −70 bytes (la Current Feature, más
  corta que la de `main`), y se mide antes de cada commit.

## 1. PARADA

Lo que decide el consultor antes de escribir nada de la fase 1:

1. **P, la regla «QUIEN»** (0.g): (A) corregir CLAUDE.md, o (B) un ADR; y, en los dos casos,
   **quién es QUIEN**: Aleks, o «el consultor» como un papel distinto que delega en Aleks. Recomiendo
   (B). Si es (B), el ADR entra en esta rama (`docs/adr/` está en el contrato).
2. **F en el cierre**: la línea que propone el encargo («F. Orden de trabajo: trabajo/entorno-code y
   después E; la hoja de ruta (docs/plan/HOJA-DE-RUTA.md) manda el orden.») se queda tal cual en el
   informe para la orden de cierre. Cita la ruta, que ya existirá en la rama en el commit del
   contrato (0.h).
3. **El refiltrado que E dice heredar** (0.f): la parte (1) está hecha desde `trabajo/activacion-a42`.
   Propuesta: la hoja de ruta lo da por HECHO con esa evidencia, y para la orden de cierre se
   prepara la frase de E sin esa coletilla. Si el consultor sabe de algo que falte (la parte (2),
   o repetirlo si cambian los tramos), lo dice y entra como criterio de R1.
4. **Los heredados superados en parte** (2, 10, 15, 27 y 34): la hoja de ruta los lleva como `HER:n`
   con lo que les queda (no salen de PROJECT_STATE en esta rama: «niega por defecto»). ¿Se prepara
   para la orden de cierre su salida o su reescritura (`docs/state/README.md`, condiciones b y c), o
   se quedan?
5. **Dos remisiones que no apuntan bien**, para decidir si se corrigen aquí o se anotan en el carril
   de deuda: `PROJECT_STATE.md:63` manda el texto entero de los heredados a `docs/state/README.md`,
   que no lo tiene (está en HISTORIA); y la descripción de `firma_tamano_posicion_ratio_aviso`
   (`knowledge/cuentas/ftmo-2step-swing-100k.yaml:463-465`) dice todavía «PENDIENTE PARA ALEKS con
   FTMO (Next Action 27)», y FTMO respondió sin cifra (`FTMO-REGLAS.md:236`). `knowledge/` está
   fuera de esta rama por el encargo.
6. **El campo `tramo`** (0.i): obligatorio si la hoja de ruta existe en el merge-base con `main`; su
   valor, el título de un `## R…` o de un carril. ¿Vale ese mecanismo para «rige desde la rama
   siguiente»?
7. **La copia de seguridad** (0.f) entra en el carril de Aleks con su dueño (el consultor, según
   SESION-02-INVENTARIO.md:328). ¿Quién la hace de verdad: Aleks o el consultor?

## 2. Respuesta del consultor a la PARADA (2026-10-10), tal cual

> Respuesta del consultor a la PARADA de trabajo/hoja-de-ruta (2026-10-10). Cópiala tal cual al final del encargo y en el informe.
>
> 1. P: ADR nuevo, y QUIEN es Aleks para todo backtest, como ya fija ADR-0046 §6a para marzo. Porqué: la regla de CLAUDE.md no sale de ningún ADR (SEPTIEMBRE-ENTRA.md §2b) y dice «no una sesión, no un agente»; el consultor es Claude en el chat, un agente también. El ADR define los tres papeles: Aleks (el usuario: decide, ordena los cierres y lee la columna de fechas de un backtest, una vez y antes del sorteo); el consultor (Claude en el chat: revisa, decide lo técnico y escribe los encargos; no ejecuta en el repo; recibe de Aleks solo la lista de fechas, nunca el fichero); y la sesión (Claude Code: ejecuta). CLAUDE.md se alinea con el ADR (QUIEN: Aleks) y lo cita. SEPTIEMBRE-ENTRA.md es un informe cerrado y no se toca; si contradice al ADR, un recuadro de corrección con fecha y rama.
> 2. F: sí, con la línea del encargo, preparada para el commit del contrato del cierre.
> 3. El refiltrado de v7–v10 está HECHO (ACTIVACION-A42.md §2.2): la coletilla de E fue un error del consultor, que la copió de HISTORIA sin medirla. La hoja de ruta lo da por hecho, y para el cierre se prepara E sin «Hereda el refiltrado de las filtradas v7–v10 (HISTORIA, entrada Q).».
> 4. Heredados 2, 10, 15, 27 y 34: lo HECHO de cada uno sale a HISTORIA con su evidencia (punto 3 de RITUAL), y lo vivo se reescribe en una línea con su dueño (una letra de la Next Action o un carril de la hoja de ruta). El 15 queda ligado a E y sale cuando E cierre A-18. Todo, preparado para el commit del contrato, con el saldo de bytes de PROJECT_STATE ≤ 0.
> 5. PROJECT_STATE.md:63: se corrige aquí la remisión a docs/state/HISTORIA.md. La descripción de firma_tamano_posicion_ratio_aviso no se toca en esta rama (knowledge/ queda fuera); va a la hoja de ruta, carril de deuda, con dueño: la próxima rama que toque el perfil de FTMO.
> 6. Tramo: vale. Obligatorio solo si la hoja de ruta existe en el merge-base con main, con un test que lo rompa en los dos sentidos.
> 7. Copia de seguridad: la hace Aleks; el consultor no tiene acceso a su máquina ni a su Drive. Va al carril de Aleks de la hoja de ruta, con fecha límite: antes de grabar la próxima sesión con el trader.
>
> Sigue con la fase 1.

## 3. Fase 1

### 3.1 Lo hecho, punto por punto

| Encargo / respuesta | Hecho | Dónde |
|---|---|---|
| 1, P: ADR nuevo y QUIEN es Aleks | ADR-0072: los tres papeles (Aleks, el consultor -Claude en el chat-, la sesión) y la columna de fechas la lee Aleks para todo backtest; ADR-0046 §6a es su caso de marzo. CLAUDE.md: «QUIEN: Aleks», con ADR-0072, y el párrafo de marzo lo cita. SEPTIEMBRE-ENTRA.md: recuadro de corrección al principio, cuerpo intacto (el contrato gana esa ruta, solo para el recuadro) | `docs/adr/0072-…`, `docs/adr/README.md`, `CLAUDE.md`, `docs/validation/SEPTIEMBRE-ENTRA.md` |
| La hoja de ruta | R0 a R7, los tres carriles, la tabla F01-F35 y las fechas fijas; cada entrada con `Refs:` y sus cuatro campos; ids, nunca recuentos | `docs/plan/HOJA-DE-RUTA.md` |
| La hoja entra en los documentos vivos | sí | `tests/contract/test_documentos_vivos.py` (`VIVOS`) |
| El test, en cuatro sentidos | (a) lo vivo está; (b) cada referencia existe y ninguna HECHA sigue viva; (c) ninguna dependencia de la Next Action apunta a una letra muerta; (d) toda ABIERTA que una tabla final da por respondida está en R1 o R4. Más uno que comprueba que las tablas de las sesiones se leen (sin él, (d) podría pasar sin leer nada). Sintéticos que rompen cada sentido | `tests/unit/test_hoja_de_ruta.py` |
| (c) falla con el `main` de hoy por F | medido: sobre `git show 2a007b7:PROJECT_STATE.md` da «F depende («tras W (consultor, 2026-10-10)») de W, que no esta viva»; sobre la rama, nada | guion `c_contra_main.py` de la carpeta de trabajo |
| El campo `tramo` | clave opcional en la carga; obligatoria si `docs/plan/HOJA-DE-RUTA.md` está en el merge-base con `main`; su valor, el título o el id de un `## ` de la hoja. Tests en los dos sentidos: sin hoja en la base no se exige; con hoja en la base falta y falla, y con un tramo válido pasa; un tramo que no está en la hoja falla | `scripts/contrato_rama.py`, `tests/unit/test_contrato_rama.py`, `docs/runbooks/CONTRATO-DE-RAMA.md`, `abrir-rama` |
| RITUAL y `cerrar-rama` | punto 4 nuevo del commit del contrato: la hoja de ruta junto a la Next Action; el `git add` y la puerta de `git status` la nombran | `docs/runbooks/RITUAL.md`, `.claude/skills/cerrar-rama/SKILL.md` |
| MASTER_PLAN | recuadro al principio, con fecha y rama; el cuerpo, intacto | `docs/plan/MASTER_PLAN.md`, y `docs/plan/README.md` |
| 5, la remisión de `PROJECT_STATE.md:63` | «texto entero: `docs/state/HISTORIA.md`; criterio de salida: `docs/state/README.md`» | `PROJECT_STATE.md` |
| 5, `firma_tamano_posicion_ratio_aviso` | en la hoja de ruta, carril de deuda (G.3), dueño: la próxima rama que toque el perfil de FTMO | `docs/plan/HOJA-DE-RUTA.md` |
| 7, la copia de seguridad | carril de Aleks (A.4), fecha límite: antes de grabar la próxima sesión con el trader | `docs/plan/HOJA-DE-RUTA.md` |

**Las puertas de RITUAL, `cerrar-rama` y `abrir-rama`, caso a caso contra `main`.** `git diff main`
sobre los tres ficheros quita cuatro líneas, y las cuatro vuelven en el mismo sitio, reescritas
para añadir: la línea de `rutas_permitidas` de `abrir-rama` (ahora tras `tramo`), la de los 25.000
bytes de `cerrar-rama` (punto y coma en vez de punto, y sigue la hoja de ruta), la de la
verificación de `cerrar-rama` (añade la Next Action y la hoja) y la puerta de `git status` de
RITUAL (añade la línea de la hoja). Ninguna puerta sale.

### 3.2 Una desviación, y por qué

**F se reescribe YA en la rama, no en el commit del contrato.** El encargo pide preparar la F nueva
para el cierre, y también un test (c) que falle mientras la Next Action dependa de una letra que no
está viva. Las dos cosas juntas dejan `make check` en rojo en todos los commits de la rama hasta el
cierre, sin sello posible. Se aplicó la línea que el consultor aprobó en el punto 2, tal cual:
«F. Orden de trabajo: trabajo/entorno-code y después E; la hoja de ruta
(docs/plan/HOJA-DE-RUTA.md) manda el orden.». El commit del contrato ya no tiene que tocarla.

### 3.3 Bytes de PROJECT_STATE

`main` (2a007b7): 22.799 bytes. La rama: 22.548 (−251): la Current Feature, más corta; la F nueva,
más corta; la remisión de la línea 63, más larga. Las líneas del cierre de §4 restan más.

## 4. Para el commit del contrato del cierre (preparado; NO aplicado en la Next Action)

Lo que el consultor manda en su respuesta, listo para la orden de cierre:

- **P sale HECHA**, con su texto literal, a HISTORIA:
  `# Next Action HECHA · P · sale de PROJECT_STATE.md en trabajo/hoja-de-ruta (<fecha>)`; evidencia:
  ADR-0072, CLAUDE.md («QUIEN: Aleks») y el recuadro de SEPTIEMBRE-ENTRA.md. En la hoja de ruta,
  R0.1 pasa a `- **Estado:** HECHA (stable/<tag>)`.
- **F**: ya reescrita en la rama (§3.2).
- **E sin la coletilla**: se quita «Hereda el refiltrado de las filtradas v7–v10 (HISTORIA, entrada
  Q).». El refiltrado está HECHO (ACTIVACION-A42.md §2.2).
- **Los heredados 2, 10, 15, 27 y 34**: lo HECHO de cada uno sale a HISTORIA con su evidencia, bajo
  `# Pendiente heredado SALE · <n> (en parte) · sale de PROJECT_STATE.md en trabajo/hoja-de-ruta
  (<fecha>)`, y lo vivo se reescribe en una línea con su dueño:

| N.º | Sale a HISTORIA (lo HECHO, con evidencia) | Queda en PROJECT_STATE |
|---|---|---|
| 2 | el xlsx de marzo al corpus (REGISTRO-MARZO.md §2, punto 1) | `- 2. Marzo: faltan vistos.yaml, la confirmacion escrita del trader y el paso a (hoja de ruta, R5.3 y A.3).` |
| 10 | la prueba gratuita de FTMO abierta y medida; A-27 DECIDIDA (ADR-0071) | `- 10. De la demo de FTMO quedan A-28 y el grabador de spread y ticks, F17 (NA:A).` |
| 15 | la respuesta del trader: S-3 de la sesión 4, «resuelve» (SESION-04-EXTRACCION.md §3.4 y §5) | `- 15. A-18: la responde S-3 de la sesion 4; sale cuando E cierre A-18.` |
| 27 | noticias y gap trading respondidas (FTMO-REGLAS.md, respuestas 1-9 del 2026-10-05); el tamaño, respondido sin cifra (respuesta 10); la comisión por lado, CONFIRMADA (ADR-0071 §3); A-27 DECIDIDA (ADR-0071) | `- 27. Para Aleks con FTMO: la «maximum capital allocation rule» y el asterisco de «USD/LOT*» (hoja de ruta, A.2); A-28 va con A.` |
| 34 | ninguna parte hecha: se reescribe con sus dueños | `- 34. Ticks: la ventana de invierno por la rejilla es X; el deslizamiento y el swap, las ejecuciones 2 y 3 (A).` |

  Con estas líneas, las de P y la coletilla de E fuera, el saldo de la rama sobre PROJECT_STATE
  sigue por debajo de cero; se mide con `wc -c` antes del commit del contrato.

## Estado

EN CURSO. Fase 1 hecha (§3), con lo preparado para el cierre (§4). Faltan la CI de Linux (`fix/hoja-de-ruta`) y el revisor.
