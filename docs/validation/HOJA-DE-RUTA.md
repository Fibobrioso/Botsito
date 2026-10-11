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
| RITUAL y `cerrar-rama` | punto 4 nuevo del commit del contrato: la hoja de ruta junto a la Next Action. En RITUAL, el `git add` y la puerta de `git status` la nombran; en `cerrar-rama`, una viñeta en el paso 3 y la «Verificación» | `docs/runbooks/RITUAL.md`, `.claude/skills/cerrar-rama/SKILL.md` |
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
| 15 | la respuesta del trader a A-18 en la sesión 4: S-3, «resuelve» (SESION-04-EXTRACCION.md §3.4 y §5). El informe no la vincula con la pregunta de reserva del 2026-09-23 (V5-INSTANTES.md), que pregunta lo mismo: stop y objetivo | `- 15. A-18: S-3 de la sesion 4 contesta el stop y el objetivo; sale cuando E cierre A-18.` |
| 27 | noticias y gap trading: respondidas las 4, 7 y 9, en parte las 1, 2, 3, 5 y 8, y SIN respuesta la 6 (FTMO-REGLAS.md, recuadro del 2026-10-05; A-54 y A-55 siguen ABIERTA, hoja de ruta A.2); el tamaño, respondido sin cifra (respuesta 10); la comisión por lado, CONFIRMADA (ADR-0071 §3); A-27 DECIDIDA (ADR-0071) | `- 27. Para Aleks con FTMO: la «maximum capital allocation rule» y el asterisco de «USD/LOT*» (hoja de ruta, A.2); A-28 va con A.` |
| 34 | ninguna parte hecha; las tres tienen ya dueño (en §0.a, «superado en parte» quería decir eso: cubierto por X y por A, no hecho) | `- 34. Ticks: la ventana de invierno por la rejilla es X; el deslizamiento y el swap, las ejecuciones 2 y 3 (A).` |

  Con estas líneas, las de P y la coletilla de E fuera, el saldo de la rama sobre PROJECT_STATE
  sigue por debajo de cero; se mide con `wc -c` antes del commit del contrato.

## 5. Lo que se hizo con los hallazgos del revisor

| # | Gravedad | Hecho |
|---|---|---|
| a1 | importa | `problemas_b` valida también lo que está FUERA de las entradas (la tabla F01-F35, las fechas fijas): un `F:F99`, un `NA:Z` o un `ID:A-99` ahí fallan. Sintético nuevo, `test_b_valida_tambien_lo_que_esta_fuera_de_las_entradas` |
| a2 | importa | `problemas_a` solo cuenta las referencias de la línea `- **Refs:**` de una entrada, no las que se nombran de paso («Depende de», el texto). Sintético nuevo, `test_a_no_basta_con_nombrar_la_letra_de_paso`. La hoja real pasa con el criterio estricto |
| a3 | importa | La línea preparada del heredado 27 (§4) dice ya lo que dice la fuente: respondidas las 4, 7 y 9, en parte las 1, 2, 3, 5 y 8, sin respuesta la 6. La hoja de ruta (A.2) gana `ID:A-54` e `ID:A-55` y la pregunta 6 |
| a4 | importa | R3.1 dice que la corrida solo CUENTA sin ningún `--diagnostico-*` (ADR-0070 §3), y que hoy lo necesita para A-21, A-35 y A-44, cuyos valores van a R1.1 o a R4.1; hasta entonces es diagnóstico y no habilita R5.2. R5.2 depende de una corrida que cuente. R7.1 recoge la condición 2 de NA:N (SymbolInfoSessionTrade, ADR-0068 §4) |
| a5 | menor | La reserva de §0.d (F14, F22 y F23 PARCIAL sin revisar cada informe a fondo) pasa a la tabla F01-F35 de la hoja |
| a6 | menor | §3.1 dice ya qué nombra cada uno: RITUAL, el `git add` y la puerta de `git status`; `cerrar-rama`, una viñeta y la «Verificación» |
| a7 | menor | El encargo dice que el plan maestro no se mantiene «desde el 2026-09-14»; la medida da **2026-09-16** (`5c49127`, «lo que encontro la auditoria de cierre de la rama de fidelidad»); el 2026-09-14 es el commit anterior (`469db7d`). Gana la medida: el recuadro de MASTER_PLAN y §0.d dicen 2026-09-16 |
| a8 | menor | Sintético nuevo para la rama `HER` de una entrada HECHA, `test_b_se_rompe_si_un_heredado_hecho_sigue_vivo` |
| a9 | menor | (i) La línea del heredado 15 ya no dice que S-3 «la responde»: dice que S-3 contesta el stop y el objetivo, y §4 anota que el informe no la vincula con la pregunta de reserva. (ii) A.4: «el texto de la deuda no dice nada de v7–v10». (iii) El 34: §4 explica que «superado en parte» en §0.a quería decir cubierto por X y por A, no hecho |
| b1 | menor | Queda dicho: el guion que midió (c) contra `main` (`c_contra_main.py`) está en la carpeta de trabajo, no en el repo; su resultado, en §3.1, lo reprodujo el revisor. El test sintético de (c) lleva la frase exacta del `main` de hoy; uno que leyera el PROJECT_STATE de `main` dejaría de valer en cuanto `main` cambie |

Con los cambios: 15 funciones en `tests/unit/test_hoja_de_ruta.py`; la suite de la hoja y la de los
documentos vivos, en verde.

## 6. La CI de Linux

`git push origin trabajo/hoja-de-ruta:refs/heads/fix/hoja-de-ruta` (como dice RITUAL.md).

- **Run 38102562925**, sobre 9285237 (la fase 1): `failure` con **un solo fallo, el esperado**,
  `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/hoja-de-ruta'; la rama
  actual es 'fix/hoja-de-ruta'»). `1 failed, 2492 passed, 9 skipped`. Estado por la API de
  check-runs con el sha literal; el log, con `gh run view --log-failed`.
- El commit de este cierre de revisión (los hallazgos atendidos y este informe) se empuja igual; su
  run va en el mensaje de entrega, porque no puede ir dentro de él.

## Informe del revisor (subagente `revisor`, 2026-10-10), tal cual

Pasada sobre 9285237, antes de §5 y §6. Copiado sin tocar.

## Informe del revisor · trabajo/hoja-de-ruta · 2026-10-10

Base 2a007b7. HEAD 928523791c61 (commits 6bcea23, 93e9260, 9285237). `git status --short` vacío. No he abierto holdout, ventanas.yaml/particiones.yaml, data/, crudas ni _proposals. Lo único protegido que toqué fue `grep -c "2026-03"` sobre `knowledge/cases/kit/vistos.yaml`, que dio 0 y es un recuento, no una lectura.

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 4 importa, 5 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | El test (b) no valida las referencias que están fuera de un `### `. Quedan sin comprobar las `F:Fnn` de la tabla F01-F35 y las `NA:` de «Fechas fijas». Un `F:F99` en la tabla o un `NA:Z` en las fechas pasa. El encargo pide que (b) falle si «una referencia NA:, HER:, ID: o F: de la hoja no existe». | Guion de solo lectura que importa `tests/unit/test_hoja_de_ruta.py` y muta la hoja real. `problemas_b` con `F:F99` en la tabla da `[]` (changed True). Con `NA:Z` en «Fechas fijas» da `[]`. Con `ID:A-99` en una entrada sí falla. Refs fuera de `###`: `[F01, F13, F14, F15, F16, F18, F19, F20, F21, F22, F23, F24, F25]`. La causa está en `test_hoja_de_ruta.py:64-73` y `:126`: `entradas_de_la_hoja` solo devuelve bloques `### `. |
| a2 | importa | El test (a) se cumple con cualquier mención de `NA:X` o `HER:n` en cualquier parte de la hoja, no con una entrada que lo lleve en `Refs:`. Quitar `NA:E` solo de `Refs` de R1.1 no lo detecta, porque E sigue citada en `Depende de` de R2.1 y R5.4. | Mutación: `problemas_a(ps, hoja.replace("NA:E ·",""))` da `[]`. Conteo de menciones: A=4, E=3, J=3, X=3, F=2, H=2, M=2, N=2, S=2. Código en `test_hoja_de_ruta.py:109-113`, que usa `referencias(hoja)` sobre el texto entero. Los sintéticos (`:317-321`) no lo ven porque `NA:E` solo aparece una vez. |
| a3 | importa | La línea preparada para el heredado 27 (informe §4, fila 27) dice que noticias y gap trading están «respondidas (FTMO-REGLAS.md, respuestas 1-9 del 2026-10-05)». La fuente dice que la pregunta 6 está «Sin respuesta» y que las 1, 2, 3, 5 y 8 son «respondida en parte». El propio §0.a del informe anota «queda la pregunta 6 de A-55 sin respuesta». La hoja no lleva A-54 ni A-55 (ABIERTAS) ni esa pregunta en ningún sitio: A.2 solo cubre la `maximum capital allocation rule` y el asterisco. | `docs/validation/FTMO-REGLAS.md:227-232` y `:241` («A-54 y A-55 siguen ABIERTAS … la pregunta 6 sigue sin respuesta»). `docs/validation/HOJA-DE-RUTA.md:70` y el §4, fila 27. `grep "A-54\|A-55" docs/plan/HOJA-DE-RUTA.md` no da nada. Mandar a HISTORIA «respondidas 1-9» afirma más de lo que sostiene la cita. |
| a4 | importa | Dependencias de R3.1 y R5.2 que contradicen lo que la propia hoja cita. R3.1 lleva `HER:25`, `HER:30`, `HER:35`, `ID:A-35`, `ID:A-44` y ADR-0070, pero «Depende de: R1.1 y R2». R1.1 dice que A-35 y A-44 «tienen el código y les falta el valor», y esos valores van a R4.1, posterior. ADR-0070 §3 dice que mientras el motor necesite un diagnóstico (A-21, A-35, A-44) «mayo no se mide». R5.2 (Mayo) depende solo de R3.1. La fase 0 no mide estas dependencias; vienen del orden del encargo, pero la hoja no declara la tensión. Tampoco R7.1 («Depende de: R6.1») recoge la condición 2 de la letra N, que dice que la rama que conecte el bot en tiempo real (demo o real) no se cierra sin la lectura de SymbolInfoSessionTrade o un procedimiento equivalente. La hoja cita NA:N solo en R5.4 y G.2. | `docs/plan/HOJA-DE-RUTA.md:79-86`, `:44-49`, `:91-96`, `:111-117`, `:157-163`. `docs/adr/0070-umbral-de-construccion-para-medir-mayo.md:62-63`. `PROJECT_STATE.md:59` (N, condición 2). |
| a5 | menor | La reserva del §0.d («F14, F22 y F23 se clasifican PARCIAL … sin revisar cada informe a fondo») no pasó a la tabla F01-F35 de la hoja. La hoja la presenta como «Medido por el contenido». | `docs/validation/HOJA-DE-RUTA.md:153-154`. `docs/plan/HOJA-DE-RUTA.md:239-240` y `:246-250`. |
| a6 | menor | El informe §3.1 dice que en RITUAL y en `cerrar-rama` «el `git add` y la puerta de `git status` la nombran». La skill solo gana una viñeta («Verificación» y el punto 3) y no nombra ni `git add` ni `git status`; eso está solo en RITUAL. No se pierde ninguna puerta, pero la frase es inexacta. | `git diff 2a007b7 -- .claude/skills/cerrar-rama/SKILL.md`: +1 viñeta y 1 ampliación de «Verificación». `RITUAL.md:158-169` sí lo nombra. |
| a7 | menor | La fecha del último cambio del plan maestro contradice la del encargo y no se dice con su nombre. El encargo dice «no se mantiene desde el 2026-09-14»; la medida da 2026-09-16 (`5c49127`). El recuadro de MASTER_PLAN usa 09-16 correctamente, pero CLAUDE.md pide nombrar la contradicción. | `git log -3 2a007b7 -- docs/plan/MASTER_PLAN.md`: `5c49127 2026-09-16`, `469db7d 2026-09-14`. Encargo, línea 9. |
| a8 | menor | La rama `HER` de `problemas_b` (heredado HECHO que sigue vivo) no tiene sintético. El código funciona: HER:34 en una entrada HECHA da «esta HECHA y el heredado sigue vivo». El test `test_b_se_rompe_si_una_entrada_hecha_sigue_viva` (`:337-342`) solo prueba `NA`. | `test_hoja_de_ruta.py:137-142` frente a `:337-342`. |
| a9 | menor | Dos frases de las líneas del cierre dicen algo que la fase 0 no midió. (i) Heredado 15: «la responde S-3» da por hecho que S-3 es la pregunta de reserva del 2026-09-23. `SESION-04-EXTRACCION.md` no menciona esa pregunta (grep de `reserva` y `2026-09-23`: sin resultados). (ii) A.4 dice «no cuenta v7–v10», y la fuente solo dice que el texto de la deuda no las menciona. (iii) El §0.a llama al heredado 34 «superado en parte» y el §4 «ninguna parte hecha». | `docs/validation/HOJA-DE-RUTA.md:58`, `:366`, `:368`. `docs/plan/HOJA-DE-RUTA.md:194`. `docs/validation/V5-INSTANTES.md:95-102` (la pregunta de reserva es sobre el stop y el TP, parecida a S-3, pero sin vínculo escrito). |

Comprobado sin hallazgos:
- **Contrato.** `uv run python scripts/contrato_rama.py` da `CONTRATO: 20 ficheros dentro del contrato de trabajo/hoja-de-ruta (riesgo medio, artefacto docs/validation/HOJA-DE-RUTA.md, 3 comprobaciones para el revisor)`.
- **Tests.** `uv run pytest tests/unit/test_hoja_de_ruta.py tests/unit/test_contrato_rama.py tests/contract/test_documentos_vivos.py -q -p no:cacheprovider` pasa, 47 puntos.
- **Sello de `make check`.** `make-check.log`: `2502 passed`, `SELLO: make check en verde sobre el arbol 90f5c916515eeca049f141ba3bf501b68511c2ba`, `PICO DE MEMORIA 294 MiB`. `git rev-parse HEAD^{tree}` da 90f5c916515eeca049f141ba3bf501b68511c2ba, el mismo árbol.
- **Trailers `Fuente:`.** La rama no toca `knowledge/spec` ni `knowledge/cases` (`git diff --name-status`). No procede.
- **Regímenes.** Cero cambios en `knowledge/evidence`, `knowledge/feedback`, `data/manifests`, `libros.yaml`, transcripciones y fotogramas. HISTORIA solo gana líneas (194 añadidas, 0 `-`). Archivo 27 es el PROJECT_STATE de `main`.
- **ADR-0072.** `## Estado` es `ACTIVE`. Está en el índice `docs/adr/README.md`.
- **SEPTIEMBRE-ENTRA.md** (informe cerrado). Solo +7 líneas, un recuadro `>` con fecha y rama, al principio, y el cuerpo intacto. La cita «el consultor, no una sesión ni un agente» existe en §2b (líneas 81-82). MASTER_PLAN.md tiene +7 líneas de recuadro y el cuerpo intacto.
- **Tres guardias de una `cita`, ids de ambigüedades e ítems de evidencia nuevos.** No procede: la rama no añade citas en la spec, no toca `ambiguedades.yaml` y no añade evidencia.
- **Saldo de bytes de PROJECT_STATE.md.** `git show 2a007b7:PROJECT_STATE.md | wc -c` = 22799. `wc -c PROJECT_STATE.md` = 22548. Saldo −251, cumple ≤ 0. El diff de PROJECT_STATE solo toca rama, Current Feature, recuento de tests, F, la remisión de la línea 63 y los Archivo 26→27.
- **Punto 3, puertas.** `git diff 2a007b7` sobre RITUAL, cerrar-rama y abrir-rama quita exactamente cuatro líneas y las cuatro vuelven ampliadas en el mismo sitio. No se pierde ninguna puerta:
  - `abrir-rama`: la línea de `rutas_permitidas`, ahora tras `tramo`.
  - `cerrar-rama`: la de los 25.000 bytes, ahora con `;`.
  - `cerrar-rama`: la de «Verificación».
  - RITUAL: la puerta de `git status` del commit del contrato.
- **Punto 1, citas.** Comprobé contra su fuente:
  - `ambiguedades.yaml` líneas 280 (A-16), 329 (A-18), 620 (A-27 DECIDIDA), 662 (A-28), 704 (A-29), 905 (A-35), 944 (A-36), 1209 (A-44), todas con el estado dicho.
  - `SESION-04-EXTRACCION.md` §5 (:928-958): las 13 «resuelve» y las 11 «en parte» cuadran con `respondidas()`.
  - `SESION-04-EXTRACCION.md:413-437` (S-3).
  - `SESION-03-EXTRACCION.md` §5, incluido A-50 «no resuelve».
  - `ACTIVACION-A42.md:18` y §2.2 (refiltrado HECHO).
  - `FTMO-REGLAS.md:61`, `:309`, `:310` y `:236`.
  - ADR-0071 §3, y `ftmo-2step-swing-100k.yaml:458-466` («PENDIENTE PARA ALEKS … Next Action 27»).
  - `REGISTRO-MARZO.md` §2 punto 1.
  - ADR-0069 :37 y :123-126; ADR-0070; ADR-0051 :117; ADR-0021 §3 y ADR-0046 §6a.
  - Existen todos los ficheros que la hoja cita, y los tags `stable/F01`..`F13` y `stable/F15`.
  - `ev-v7-001550-82e5cffc` no la revisa ningún informe.
- **Holdout.** Las fechas de la hoja son solo 2026-10-10, 2026-09-09, 2026-10-08 y 2026-10-22 (más «26 al 30 de octubre», futuras). Ninguna es de un día reservado. No hay ningún resultado, y el informe y el ADR no traen fechas reservadas. No se leyó libro, imagen, fotograma ni transcripción, así que no hacía falta fila en `HOLDOUT-EXPOSICIONES.md`.
- **Punto 6, ADR-0072 y P.**
  - El ADR dice lo que decidió el consultor (punto 1 de su respuesta): los tres papeles, la columna la lee Aleks para todo backtest, ADR-0046 §6a como su caso de marzo, y el recuadro de SEPTIEMBRE-ENTRA.
  - Añade dos cosas ya vigentes y coherentes: la declaración el mismo día (ADR-0021 §4) y el origen en `52c0220`. Ese commit existe, es de 2026-09-20 y es el que introdujo «QUIEN» (`git log -S "QUIEN" -- CLAUDE.md`).
  - CLAUDE.md :151 y :162 dicen «QUIEN: Aleks», citan ADR-0072 y ADR-0046 §6a, y no queda un «por el consultor».
  - Los dos pasajes del ADR sobre `ERRORES-RECURRENTES.md` (fila de `trabajo/cases-rejilla`) existen.
- **Desviación declarada del §3.2 (F reescrita ya en la rama).** Está declarada, razonada y es mínima. Aplica literalmente la línea que el consultor aprobó. Sin ella, (c) deja `make check` rojo en todos los commits de la rama. Con el PROJECT_STATE de `main`, `problemas_c` da `['F depende (tras W (consultor, 2026-10-10)) de W, que no esta viva']`. Sobre la rama da `[]`. La juzgo aceptable; contradice la letra del encargo («no en la Next Action de la rama»), pero el consultor debe saber que la F nueva ya está en la rama y que el §4 ya no la lleva.

### Eje (b) · Encargo
Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 17 hechos, 1 hecho de otra forma (declarado), 2 parciales (CI y revisor, pendientes por orden).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Fase 0 (a)-(h) en el informe, con PARADA | Hecho | `HOJA-DE-RUTA.md` §0.a-§0.h y §1 |
| 2 | Respuesta del consultor copiada tal cual en el encargo y en el informe | Hecho | Comparación por programa: `True`, 2307 caracteres iguales |
| 3 | Hoja: R0…R7, referencias `NA:/HER:/ID:/F:`, cuatro campos, ids sin recuentos | Hecho | 21 entradas `###`, ninguna sin `Refs`, `Qué es`, `Depende de`, `Quién` y `Hecho cuando`. `test_documentos_vivos.py` pasa |
| 4 | Contenido: R1 (NA:E con las ambigüedades de 0.c como ID: y el refiltrado) | Hecho | `HOJA:40-55`; el refiltrado como HECHO con ACTIVACION-A42 §2.2 |
| 5 | R2 (julio NA:S con ticks, NA:X y ADR-0051 §8), R3 (ADR-0070), R4, R5 (G, e, mayo, marzo, I, F26, F27), R6, R7 | Hecho | `HOJA:57-163` (ver a4 sobre las dependencias) |
| 6 | Tres carriles (Aleks, guardias y deuda, material reservado), tabla F01-F35 y fechas fijas sin días reservados | Hecho | `HOJA:165-264` |
| 7 | La hoja entra en `VIVOS` | Hecho | `tests/contract/test_documentos_vivos.py` (+2 líneas) |
| 8 | Test negando por defecto, que falle en (a), (b), (c) y (d), con sintéticos | Hecho, con la debilidad de a1/a2 | Falla en los cuatro sentidos sobre la hoja real: (a) sin HER:15 / sin todas las menciones de una letra; (b) `ID:A-99` y entrada HECHA viva; (c) `Despues de W`, `Espera a Q`, `Junto a Q y R`; (d) sin `ID:A-36` y sin `ID:A-18`. El de «plantilla sin tabla» levanta `AssertionError`. Pero (a) y (b) no son tan estrictos como dice el informe (a1, a2) |
| 9 | (c) falla con el `main` de hoy por F | Hecho | `problemas_c(PS de 2a007b7)` da el fallo de F→W; sobre la rama `[]` |
| 10 | Campo `tramo`: lo admite `contrato_rama.py`, obligatorio solo si la hoja está en el merge-base, valor = título o id de un `##`, con test en los dos sentidos | Hecho | `scripts/contrato_rama.py` (`problemas_de_tramo`, `tramos_de_la_hoja`); tres tests nuevos (sin hoja en la base no se exige, con hoja falta y falla, un tramo inexistente falla); el contrato de esta rama no lo lleva, como pide |
| 11 | `abrir-rama` lo pide; CONTRATO-DE-RAMA.md lo documenta | Hecho | Fila nueva en la tabla de `abrir-rama` y viñeta en el punto 4; viñeta y plantilla en CONTRATO-DE-RAMA.md |
| 12 | RITUAL y `cerrar-rama`: en el commit del contrato, junto a la Next Action, se actualiza la hoja; revisión caso a caso contra `main` | Hecho | RITUAL punto 4, `git add` y puerta; `cerrar-rama` punto 3 y «Verificación». Ver a6 sobre la frase del informe |
| 13 | MASTER_PLAN: recuadro al principio, con fecha y rama, que diga que el orden vivo está en la hoja y que §E queda como historia | Hecho | `MASTER_PLAN.md`, +7 líneas. También se edita `docs/plan/README.md`, no pedido pero declarado en §3.1 |
| 14 | P: lo decidido en la PARADA sobre «QUIEN» | Hecho | ADR-0072, CLAUDE.md y el recuadro de SEPTIEMBRE-ENTRA (todo verificado arriba). La ruta de SEPTIEMBRE-ENTRA se añadió al contrato con comentario |
| 15 | Respuesta 5: corregir la remisión de `PROJECT_STATE.md:63`; `firma_tamano_posicion_ratio_aviso` a la hoja (carril de deuda), sin tocar `knowledge/` | Hecho | `PROJECT_STATE.md:63-64`; hoja G.3. `knowledge/` intacto |
| 16 | Respuesta 7: la copia de seguridad en el carril de Aleks, con fecha límite | Hecho | Hoja A.4, «antes de grabar la próxima sesión con el trader» |
| 17 | Para el cierre, preparado en el informe y no en la Next Action de la rama: P HECHA, F, E sin la coletilla, y los heredados 2, 10, 15, 27 y 34 | Hecho de otra forma (F) | P, E y los cinco heredados preparados en el §4. F se aplicó ya en la rama (§3.2, declarado). Las cinco líneas dicen lo que la fase 0 midió, salvo a3 (27) y a9 (15 y 34). 2, 10 y 34 cuadran con 0.a: faltan `vistos.yaml` (recuento 0), la prueba abierta y A-27 DECIDIDA, y X más NA:A para el 34 |
| 18 | Saldo de bytes de PROJECT_STATE ≤ 0 | Hecho | 22.799 → 22.548 (−251). Las líneas del cierre del §4 restan más (P y la coletilla de E salen) |
| 19 | Informe con fase 0, PARADA, respuesta, lo hecho y estado al final | Hecho | Acaba en `## Estado`: «EN CURSO … Faltan la CI de Linux y el revisor» |
| 20 | `make check` con sello antes de cada commit | Hecho (HEAD) | SELLO sobre el árbol de HEAD. No pude comprobar el sello de los dos commits anteriores |
| 21 | `fix/hoja-de-ruta` y CI de Linux, con números de run | Parcial | El informe dice que falta. No pude consultar la CI (ver abajo) |
| 22 | Pasar el revisor y pegar su informe al final del informe de la rama | Parcial | Lo pega quien lanza el revisor; este texto está listo para pegarlo |
| 23 | No cambia: `src/`, spec, `knowledge/`, parámetros, informe cerrado, fichero congelado | Hecho | `git diff --name-status`: ningún `src/`, `knowledge/`, `config/` ni `data/manifests/`. Los únicos informes cerrados tocados son SEPTIEMBRE-ENTRA y MASTER_PLAN, solo con recuadro |
| 24 | Nada de holdout: ninguna fecha reservada ni resultado en la hoja | Hecho | Comprobado arriba |

Lo que la rama hace y el encargo no pide: la edición de `docs/plan/README.md` (declarada en §3.1) y el test extra `test_las_tablas_finales_de_las_sesiones_se_leen` (declarado en §3.1, y útil para que (d) no pase sin leer nada). Ninguna cosa sin justificar.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | menor | El informe cuenta F01-F35 y las líneas del cierre, pero no dice que el guion `c_contra_main.py` con el que midió que (c) falla con `main` no está commiteado: queda solo la frase de §3.1. Lo reproduje yo con el PROJECT_STATE de 2a007b7 y da lo que dice. Además, ningún test commiteado usa el PROJECT_STATE real de `main`; solo el sintético con la misma frase. | `HOJA-DE-RUTA.md:318`; `test_hoja_de_ruta.py:345-350`. Mi medida: `C con main: ['F depende (tras W …) de W, que no esta viva']` |

### Lo que no pude comprobar
- **CI de Linux de `fix/hoja-de-ruta` sobre 928523791c613fff8ef96e21483e19863b0367b2.** `curl` está bloqueado por el hook de solo lectura («`curl` escribe»), así que no pude consultar `check-runs`. Habrá que mirarlo con `!` de Aleks. El informe todavía no trae el número de run.
- **El sello de `make check` de los commits 6bcea23 y 93e9260.** Solo el log de HEAD (árbol 90f5c91) está disponible; `git write-tree` y las comprobaciones que escriben no se ejecutan.
- **Heredado 10, partes «región» del panel de FTMO.** El apalancamiento sí está medido (`DEMO-EJECUCION-1.md:159`, COINCIDE) y Swing, 100.000 y MT5 constan en ADR-0071:21. La región no la encontré en ninguna fuente que pueda abrir. La línea del cierre («quedan A-28 y el grabador») no la nombra.
- **Valores de ticks y datos de `data/`, material reservado y crudas**, que no abrí por mandato.
- **`git tag -l`.** El hook de solo lectura lo bloquea; usé `git for-each-ref refs/tags/stable/F0* F1*`.

### Comandos ejecutados
1. `git branch --show-current`; `git log --format='%h %s' 2a007b7..HEAD`; `git diff --stat 2a007b7...HEAD`; `git status --short`
2. `uv run python scripts/contrato_rama.py`
3. `uv run pytest tests/unit/test_hoja_de_ruta.py tests/unit/test_contrato_rama.py tests/contract/test_documentos_vivos.py -q -p no:cacheprovider`
4. `git diff 2a007b7 -- PROJECT_STATE.md`; `git show 2a007b7:PROJECT_STATE.md | wc -c`; `wc -c PROJECT_STATE.md`
5. `git diff 2a007b7 -- .claude/skills docs/runbooks/RITUAL.md docs/runbooks/CONTRATO-DE-RAMA.md CLAUDE.md`
6. `git diff 2a007b7 -- docs/validation/SEPTIEMBRE-ENTRA.md docs/plan/MASTER_PLAN.md docs/plan/README.md docs/adr/README.md tests/contract/test_documentos_vivos.py`
7. `git diff 2a007b7 -- scripts/contrato_rama.py tests/unit/test_contrato_rama.py`
8. `git diff 2a007b7 -- docs/state/HISTORIA.md` (más el recuento de líneas `-`); `git diff --name-status 2a007b7...HEAD`; `git diff 2a007b7 -- <RITUAL, cerrar-rama, abrir-rama> | grep '^-[^-]'`
9. `git log -S "QUIEN" -- CLAUDE.md`; `git show 52c0220 --stat`; `git log -3 2a007b7 -- docs/plan/MASTER_PLAN.md`; `git for-each-ref refs/tags/stable/F0* F1*`
10. `git rev-parse HEAD^{tree} HEAD`; lectura de `make-check.log`
11. Varios guiones `uv run python -` de solo lectura:
    - mutación en memoria sobre la hoja real y el PROJECT_STATE de `main`;
    - cobertura de menciones por letra y heredado;
    - comparación del bloque de la respuesta del consultor entre encargo e informe;
    - comprobación de los campos de las 21 entradas;
    - prueba de la rama HER de `problemas_b`.
12. `grep -c "2026-03" knowledge/cases/kit/vistos.yaml` (da 0); `grep -n` sobre `ambiguedades.yaml`; `sed -n` sobre HISTORIA, `GUION-MISMO-COMANDO.md`, `ACTIVACION-A42.md`, `SESION-02-INVENTARIO.md`, `ERRORES-RECURRENTES.md`, `SESION-03-EXTRACCION.md`
13. Intentos bloqueados por los hooks: `for f in …`, `git tag -l`, `curl … check-runs`.

Ficheros de referencia: `C:\Users\USER\Desktop\Bot v3\docs\plan\HOJA-DE-RUTA.md`, `C:\Users\USER\Desktop\Bot v3\tests\unit\test_hoja_de_ruta.py`, `C:\Users\USER\Desktop\Bot v3\docs\validation\HOJA-DE-RUTA.md`, `C:\Users\USER\Desktop\Bot v3\docs\adr\0072-quien-lee-la-columna-de-fechas-y-los-tres-papeles.md`.

## Estado

**LISTA PARA REVISIÓN, NO CERRADA.** Fase 0 con su PARADA (§0, §1) y la respuesta del consultor
(§2); fase 1 hecha (§3): la hoja de ruta, su test en cuatro sentidos, el `tramo` del contrato,
RITUAL y las skills, MASTER_PLAN, ADR-0072 (P) y la remisión de PROJECT_STATE; la desviación de F,
declarada (§3.2). Preparado para el commit del contrato del cierre (§4): P HECHA, E sin la
coletilla y los heredados 2, 10, 15, 27 y 34. Revisor pasado y sus hallazgos atendidos (§5). CI de
Linux: run 38102562925 con solo el fallo esperado de `state check` (§6); el run del último commit,
en el mensaje de entrega. Saldo de PROJECT_STATE frente a `main`: −251 bytes. Exposiciones:
ninguna (no se leyó ningún libro, imagen, fotograma ni transcripción). La rama remota
`fix/hoja-de-ruta` se borra en el cierre.
