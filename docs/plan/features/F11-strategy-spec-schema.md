# F11 · strategy-spec-schema

**Rama:** `feature/F11-strategy-spec-schema` · **Fase:** 2 (retroalimentación del experto) ·
**Depende de:** F02 (registro), F07 (evidencia), F09 (feedback), F10 + sesión 1 (`stable/F10-sesion-01`)

## Objetivo

Convertir lo que el trader dijo en la sesión 1 en una **especificación ejecutable y citable**:
`feedback apply` (la puerta que F09 dejó diferida), `strategy_spec.yaml` con las reglas de la
operativa, `glossary.yaml` con sus términos y `spec_manifest.yaml` con versión y hash, para que un
backtest, un informe y un `Params.mqh` puedan decir contra qué spec corrieron. F11 describe, no
ejecuta: el motor es F18–F23.

## Hechos de partida (medidos el 2026-09-09, no estimados)

- **Registro** (`knowledge/spec/parametros.yaml`): **33 parámetros** — 30 `estrategia`, 2
  `ejecucion`, 1 `instrumento`. **32 UNKNOWN**, 1 CONFIRMED (`huso_operativa` = `Europe/Madrid`,
  por ADR-0005). `Registro.obtener` se niega a leer un UNKNOWN: hoy nada puede usarlos.
- **Feedback de la sesión 1**: 72 registros. Sobre parámetros hay **33 registros activos** que
  cubren **32 parámetros**: 27 `RESOLVE_UNKNOWN`, 5 `CORRECT`, 1 `CONFIRM`.
- **Cinco parámetros no tienen ningún `RESOLVE_UNKNOWN` activo** (`break_even_condicion`,
  `cartuchos_max`, `filtro_noticias`, `instrumento`, `perdida_maxima_diaria`). Filtrar por esa
  acción escribiría el valor caducado: en `perdida_maxima_diaria`, "saldo actual del momento" en
  vez de "saldo **inicial del día**".
- **14 valores activos no convierten** al tipo declarado (`_convertir`): `stop_fraccion_caja`
  "0,8", `stop_segundo_esquema` "0,8", `riesgo_por_operacion` "0,5" y `perdida_maxima_diaria`
  (la coma decimal la rechaza `_NUMERO` a propósito), `cartuchos_max` "3" como texto,
  `spread_maximo` "sin limite", `objetivo_extension` "0 (sin extension)", `stop_reduccion_*`
  "no aplica", `anclaje_h4` / `ventana_inicio` / `ventana_fin` con la frase entera, y
  `stop_proteccion_capital` (×2).
- **`stop_proteccion_capital` tiene DOS registros activos** que no se superseden entre sí
  (`fb-…-ced73f4a` y `fb-…-67e1dfb0`). `feedback/modelo.py` detecta dos registros que superseden al
  mismo, no dos activos sobre el mismo objetivo: hueco de F09 que F11 hereda.
- **`instrumento` (`categoria: instrumento`) y `cuenta_objetivo` (`categoria: ejecucion`) no se
  pueden escribir por feedback**: `config/registro.py:266-270` exige `fuente: decision` fuera de
  `estrategia`. `apply` reventaría en esos dos.
- **`huso_operativa` = `Europe/Madrid` está desmentido por la sesión**: el trader trabaja en
  **UTC+2 fijo y no se ajusta al cambio de horario** (`fb-…-bb06f14c`, verificado en pantalla,
  `fr-v6-22982c02/3585000`). Madrid y UTC+2 coinciden en verano y divergen en invierno.
- **`test_no_business_literals` está caducado**: prohíbe `0.75`, `0.5`, `EURUSD`, `Europe/Madrid`
  —las hipótesis previas a la sesión— y **no** los valores que la sesión fijó (`0.8`, `0.2`, `4.5`,
  `23:00`, `FundedNext`).
- **Ningún parámetro declara `minimo`/`maximo`**: la guardia que ADR-0002 vende como su razón de
  ser (el 0,5 % escrito como 0,5) está desarmada.
- **Datasets congelados**: enero, mayo, junio, julio y agosto de 2026. Enero ya existe
  (`eurusd-m1-2026-01-e37291d4`), así que **A-14 se puede medir sin descargar nada**: mayo y junio
  son verano y no distinguen las dos hipótesis del huso; enero sí.

## Decisiones de diseño (cerradas tras la revisión del 2026-09-09)

1. **Estado de un valor bajo ambigüedad abierta: `CONFIRMED`** (decisión del consultor). Lo dijo el
   trader, con minuto y cita, y así queda. "Qué está en revisión" se responde **cruzando el
   registro con las ambigüedades `ABIERTA`**, no degradando el estado: una línea en
   `knowledge validate` y un `botsito spec status`. `DEFAULT_AMBIGUOUS` se reserva para lo que
   siempre significó: un valor que inventamos nosotros.
2. **La normalización se hace con feedback, no con código** (decisión del consultor).
   `FeedbackRecord` gana un campo **opcional** `valor_canonico` (en `CAMPOS_OPCIONALES`: un campo
   ausente no entra en `contenido_canonico`, así que **los 72 registros existentes conservan su
   id**). El consultor escribe un registro nuevo que supersede por cada parámetro afectado, con el
   `respuesta_literal` **intacto** y el valor ya en el tipo del registro.
3. **`feedback apply` es deliberadamente tonto**: toma `valor_canonico` si existe, si no
   `valor_resultante` tal cual, y **falla con error** ante cualquier cosa que no convierta. Cero
   regex, cero heurística: una tabla de interpretación de las palabras del trader dentro del código
   sería negocio fuera del registro, que es justo lo que ADR-0002 prohíbe.
4. **Criterio de selección**: registros **activos** (no superseded) con acción en
   `{RESOLVE_UNKNOWN, CORRECT, CONFIRM}` y `valor` presente. `apply` **rechaza** un registro
   superseded nombrando quién lo supersede, y **aborta** si un parámetro tiene más de un activo.
5. **`huso_grafico`**, parámetro nuevo (`estrategia`, `texto`, `Etc/GMT-2`, fuente
   `fb-…-bb06f14c`), del que cuelgan `anclaje_h4`, `ventana_inicio` y `ventana_fin`. Un test afirma
   que `Etc/GMT-2` da **+02:00 en enero** (el signo de `Etc/*` está invertido y se lee mal).
   `huso_operativa` se corrige por ADR-0012: hoy afirma un reloj que la sesión desmiente.
6. **Cartuchos, con la semántica real**: `cartuchos_max: entero = 3` (nombre estable: es lo que
   acaba en `Params.mqh`), más `cartucho_criterio: enum {solo_perdida, todo_intento} = solo_perdida`
   y `cartuchos_reinicio: enum {siguiente_liquidez_m15, fin_de_dia, nunca} = siguiente_liquidez_m15`.
   El contador **no es diario**: se reinicia con la siguiente liquidez de M15 (v6 2:21:07).
7. **La ausencia de valor son tres cosas distintas y se tratan por separado**: `spread_maximo` →
   `filtro_spread: booleano = false` y el umbral **se queda UNKNOWN** (que ya significa "leerlo
   falla"; un `0` significaría "no operar nunca"); `objetivo_extension` →
   `objetivo_extension_activa: booleano = false`; `stop_reduccion_*` y `stop_colchon_spread` **no
   son valores ausentes sino reglas descartadas**: salen del registro y quedan como regla de
   `strategy_spec` citando su `fb-…`.
8. **`stop_proteccion_capital` sale del registro**: es derivado (`1 − stop_fraccion_caja`) y pasa a
   invariante de la spec con test. Resuelve de paso el duplicado. **El 0,4 % de riesgo real es un
   cálculo del consultor, no una cifra del trader**: entra como invariante derivado
   (`riesgo_por_operacion × stop_fraccion_caja`), nunca como valor del registro.
9. **Categorías**: `instrumento` pasa a `estrategia` (elegir mercado es negocio; ADR-0004 reserva
   `instrumento` para la ficha del símbolo). `cuenta_objetivo` pasa a `prop_firm` por ADR-0012, y
   se separa `saldo_inicial_cuenta`, hoy empotrado en un texto y necesario para dimensionar el lote.
10. **`base_calculo: enum {saldo_actual, saldo_inicial_dia}`** en `riesgo_por_operacion` (saldo
    actual) y `perdida_maxima_diaria` (saldo inicial del día). Hoy ambos declaran la misma unidad y
    la diferencia se pierde; FundedNext mide sobre el balance de inicio de día.
11. **Tipos nuevos**: `enum` (con `opciones`), `booleano`, `puntos`, `minutos`, `lotes`. Las
    `opciones` **bajan** de `knowledge/cases/kit/mapa_parametros.yaml` al registro: `cases` está por
    encima de `feedback` y `config` en ADR-0006, y `apply` no puede importarlo. Efecto inmediato
    declarado: **7 valores que hoy pasarían como `texto` fallarán** (`filtro_noticias`,
    `reentrada_tras_equal`, `stop_en_orden_pendiente`, `mapeo_dos_velas`, `sesgo_h4_regla`,
    `reubicacion_cadencia`, `stop_colchon_spread`), y eso es lo que se busca.
12. **Capas**: las ambigüedades abiertas se **inyectan** desde `cli`/`validation` (como ya hace
    `validar_contra_contexto`), no se importan desde `feedback`. `spec_manifest` y el cargador de
    `strategy_spec` viven en `botsito.spec`.
13. **`apply` no destruye la cabecera**: `parametros.yaml` lleva 45 líneas que son la documentación
    del esquema, citadas por ADR-0002 y el README; un `safe_dump` de ida y vuelta las borra.
    Edición que preserva comentarios, escritura atómica, `newline="\n"` y UTF-8.
14. **Hash del manifiesto sobre los TRES ficheros, `parametros.yaml` incluido** (MASTER_PLAN H.2
    fila 215). Si el registro queda fuera, cambiar el stop de 0,8 a 0,75 no cambia el hash y el
    pre-vuelo de F33 daría verde con otra estrategia. Se hashea la **estructura parseada y
    re-serializada canónicamente** (claves ordenadas, números como texto, LF, UTF-8, sin
    comentarios), no los bytes. Por parámetro entran nombre, categoría, tipo, unidad, **estado**,
    valor, **fuente**, `ambiguedad_id` y min/max: si solo entrara el valor, pasar de
    `DEFAULT_AMBIGUOUS` a `CONFIRMED` no cambiaría el hash y F26 no sabría contra qué midió.
15. **`minimo`/`maximo` en todos los numéricos**: fracciones en [0, 1], `riesgo_por_operacion`
    máximo 5, `objetivo_rr` mínimo 1, `cartuchos_max` entre 1 y 10.
16. **Los literales prohibidos se actualizan a los valores reales** (`0.8`, `0.2`, `4.5`, `23:00`,
    `FundedNext`, `XAUUSD`, `NASDAQ`) y un test cruza la lista con los `CONFIRMED` del registro. Sin
    enteros desnudos (`3`, `9`): para eso está el contrato AST de accesores.
17. **Dos tests de deuda se invierten, no se borran**: `test_fichero_real_sin_valores_de_estrategia`
    y el de feedback pasan a afirmar que **todo `CONFIRMED` de estrategia tiene `fuente` de tipo
    `feedback` o `evidence`**.
18. **Las citas de la spec**: el test de "ni un número de negocio" se aplica solo a los campos
    ejecutables (`condicion`, `accion`, `umbral`, `parametro`); el campo `cita` queda exento y se
    verifica **al revés**: debe coincidir con el `respuesta_literal` del `fb-…` que declara. Se
    escribe además la tabla **R-01..R-14 → `fb-…`**, porque `R-03` no es un id citable
    (`ids.REGLA` es `^RN-\d{3}$`).
19. **Hechos de la sesión que hoy no tienen hogar** y se deciden aquí como parámetro o como regla:
    la frontera de las dos sesiones H4 (11:00), "no hay entradas en paralelo", "para reentrar debe
    haber tocado el stop", el disparador del break even (otra zona de control que se rompe) y el
    reinicio de cartuchos.
20. **ADR-0012** (registro: tipos nuevos, categorías, huso del trader, ausencia de valor,
    `valor_canonico`) y **ADR-0013** (spec: manifiesto, hash canónico, semver, citas).

21. **La ventana NO se amplía a Nueva York en esta fase** (A-15, decisión del consultor,
    2026-09-09): "una vez todo funcione, lo ampliamos". La spec declara las dos sesiones del trader
    y el bot no busca fuera de ellas.
22. **El histórico sigue siendo Dukascopy** (A-16, decisión del consultor con la medición del
    2026-09-09, `docs/validation/anexos/A-16-proveedor-de-datos-2026-09-09.md`): la demo de
    FundedNext solo sirve M1 **desde el 3 de junio de 2026**, así que no cubre mayo ni la primera
    semana de junio, que son casos del paquete. Donde sí se pueden comparar, los dos proveedores
    coinciden a **2 puntos de mediana**. MT5 se reserva para spread, ejecución, reloj de servidor y
    paridad (F17, F24, F30–F33), y los 2 puntos entran como margen declarado en F26.
23. **Cuenta**: el objetivo es la **cuenta fondeada de 100 000 USD** y las pruebas de
    funcionamiento se hacen en una **demo de FundedNext de 100 000 en MT5** (decisión del consultor).
    Son dos parámetros distintos —`cuenta_objetivo` y `cuenta_pruebas`, ambos `prop_firm` por
    ADR-0012— porque los límites que se juegan no son los mismos.
24. **Se opera durante las noticias** (A-17, decisión del consultor): "más adelante veremos si es un
    impedimento". Queda anotado como deuda con dueño: si lo fuera, el filtro se hace **bloqueante y
    anclado a un calendario externo** (Investing o equivalente), lo que implica una fuente de datos
    nueva y una funcionalidad propia, no un parámetro.

**Nota sobre A-15, A-16 y A-17**: las tres las decide el consultor, no el trader, y
`ambiguedades.yaml` dice que una ambigüedad se cierra SOLO con un registro de feedback del trader.
Por eso quedan ABIERTAS hasta que ADR-0012/ADR-0013 las cierre por decisión, dentro de F11, y esa
asimetría —ambigüedades del trader frente a decisiones del consultor— se documenta ahí.

## Alcance cerrado (que SI)

- `botsito feedback apply --sesion <s> [--check]` con las decisiones 2, 3, 4, 13 y 17.
- Registro: tipos nuevos (11), `minimo`/`maximo` (15), categorías y parámetros nuevos (5, 6, 7, 9,
  10), retirada de los derivados y descartados (7, 8).
- `knowledge/spec/strategy_spec.yaml` + cargador estricto en `botsito.spec`, reglas por nombre de
  parámetro con cita verificada (18).
- `knowledge/spec/glossary.yaml`: breaker, zona de control, estructura, equal, cartucho, caja,
  liquidez de M15, order flow.
- `knowledge/spec/spec_manifest.yaml`: `spec_version` semver + hash canónico (14).
- `botsito spec status`: qué valor usa el bot y qué está bajo ambigüedad abierta (1).
- ADR-0012 y ADR-0013.

## Fuera de alcance (que NO)

Motor y backtest (F18–F23), validación semántica (F12), documentos generados (F13), biblioteca de
casos (F14), export MQL5 (F28), medir A-13 y A-14 (F26; F11 solo deja los datos preparados).

## Entradas

`knowledge/feedback/2026-09-09-sesion-01/` (72 registros) · `knowledge/spec/parametros.yaml` (33) ·
`knowledge/spec/ambiguedades.yaml` (17; A-13..A-17 abiertas) · `knowledge/evidence/` (353 items) ·
`knowledge/cases/kit/mapa_parametros.yaml` (opciones, que bajan al registro) ·
`docs/validation/SESION-01-2026-09-09.md` · ADR-0002, ADR-0004, ADR-0005, ADR-0006, ADR-0009.

## Salidas (ficheros)

`knowledge/spec/{parametros.yaml (32 valores escritos), strategy_spec.yaml, glossary.yaml,
spec_manifest.yaml}` · `knowledge/feedback/2026-09-09-sesion-01/` (≈14 registros nuevos con
`valor_canonico`) · `src/botsito/spec/{__init__,modelo,manifiesto}.py` ·
`src/botsito/feedback/aplicar.py` · `docs/adr/0012-*.md`, `docs/adr/0013-*.md` ·
`docs/validation/F11-strategy-spec-schema.md`.

## Tests

1. `apply --check` no escribe y lista los 32 cambios; `apply` los escribe y cada uno queda con
   `fuente: {tipo: feedback, id: fb-…}`.
2. `apply` rechaza un registro superseded nombrando quién lo supersede; aborta con dos activos
   sobre el mismo parámetro; falla ante un valor que no convierte, diciendo cuál.
3. Idempotencia: segundo `apply` con la misma fuente y el mismo valor es no-op; misma fuente y
   valor distinto es error (alguien editó el registro a mano).
4. La cabecera de 45 líneas de `parametros.yaml` sobrevive a `apply` (comparación literal).
5. `Etc/GMT-2` da +02:00 en enero y en julio (el signo invertido no muerde).
6. Hash del manifiesto: reproducible en un clon limpio; cambia si cambia el valor, el estado o la
   fuente de cualquier parámetro; falla si el hash cambió y `spec_version` no.
7. `strategy_spec.yaml`: los campos ejecutables no contienen cifras; cada `cita` coincide con el
   `respuesta_literal` de su `fb-…`; cada regla cita un `ev-…`/`fb-…` existente.
8. `test_no_business_literals` con la lista nueva, y un test que la cruza con los `CONFIRMED`.
9. Los dos tests de deuda, invertidos (17).
10. `spec status` lista los parámetros bajo ambigüedad abierta y coincide con `ambiguedades.yaml`.

## Criterio de aceptacion

1. `botsito feedback apply --sesion 2026-09-09-sesion-01 --check` lista **32 parámetros** y no
   escribe nada; sin `--check`, los escribe y `knowledge validate` queda en verde.
2. Ningún parámetro `CONFIRMED` de estrategia sin `fuente` de tipo `feedback` o `evidence`.
3. `strategy_spec.yaml` carga con esquema estricto y ningún campo ejecutable contiene una cifra.
4. `spec_manifest.yaml` da el mismo hash en un clon limpio en otra máquina, y uno distinto ante
   cualquier cambio de valor, estado o fuente en los tres ficheros.
5. `botsito spec status` muestra los cinco parámetros bajo A-13..A-17 con el valor que usa el bot.
6. `make check` verde, contratos de capas incluidos, y el commit que aplica los valores lleva
   trailer `Fuente:` con los ids `fb-…` (que `apply` imprime listos para pegar).

## Riesgos

- **`apply` reescribe el fichero que es la única puerta de los valores**: escritura atómica, copia
  previa y `--check` obligatorio en la práctica (decisión 13).
- **Renombrar y recategorizar parámetros rompe referencias** (`mapa_parametros.yaml`, cuestionario
  del kit, `ambiguedades.yaml`): hacerlo en un commit propio y pasar `knowledge validate` después.
- **A-13 y A-14 siguen abiertas** mientras la spec ya corre con un valor: por eso el estado es
  CONFIRMED y la revisión se ve por cruce (decisión 1), y por eso `spec status` existe.
- **El hash depende de la serialización canónica**: si cambia la librería de YAML, el hash cambia
  sin que cambie la spec. Se hashea la estructura, no los bytes, y el test se corre en clon limpio.

## Revision de diseno (agente, antes de programar)

Revisión del 2026-09-09 sobre el brief inicial. **Aceptados**: A-1 (recuento: eran 33/32, no 35;
"26" era el número de registros con vídeo, no de parámetros) → hechos de partida y criterio 1;
A-2 (filtrar por `RESOLVE_UNKNOWN` escribe valores caducados en 5 parámetros) → decisión 4; A-3 (14
valores no convierten, no 6) → decisiones 2 y 3; A-4 (`instrumento` y `cuenta_objetivo` no se
pueden escribir por feedback) → decisión 9; A-5 (dos activos sobre `stop_proteccion_capital`) →
decisiones 4 y 8; A-6 (el criterio 6 forzaba `DEFAULT_AMBIGUOUS` y degradaba cinco parámetros
centrales) → decisión 1; A-7 (el hash dejaba fuera `parametros.yaml`) → decisión 14; A-8 (dos
imports que el contrato prohíbe; `safe_dump` borra la cabecera) → decisiones 11, 12 y 13; A-9
(`perdidas_max_dia` habría metido un error nuevo: el contador no es diario) → decisión 6; A-10
(`huso_operativa` desmentido por la sesión) → decisión 5; A-11 (`test_no_business_literals`
caducado) → decisión 16; A-12 (criterios 3 y 5 se contradecían) → decisión 18; A-13 (normalizar en
código sería negocio fuera del registro) → decisiones 2 y 3. **Importantes aceptados**: B-1 →
decisión 10; B-2 → 7; B-3 → 11; B-4 → 11; B-5 → 15; B-6 → tests 3 y criterio 6; B-7 → guardia en
`knowledge validate`; B-8 → 17; B-9 → 18; B-10 → 19. **Menores aceptados**: C-1..C-5, C-7 y C-8
(corregir "25 parámetros" en PROJECT_STATE y "26" en el informe de la sesión). **Descartado**:
nada de fondo; C-6 era una confirmación, no un hallazgo. **Corrección al revisor**: propone
descargar un dataset de enero de 2026 para poder cerrar A-14, pero **ya existe**
(`eurusd-m1-2026-01-e37291d4`, congelado en F15), así que A-14 es medible sin descargar nada.

## Que habilita

F12 (validación semántica sobre un esquema ya estricto), F13 (documentos generados desde la spec),
F14 (casos que citan reglas por id), F18–F23 (motor que lee parámetros por nombre), F26 (medir
A-13 y A-14 contra los días del trader) y F28 (`Params.mqh` con el hash de la spec).
