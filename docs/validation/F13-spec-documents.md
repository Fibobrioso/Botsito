# F13 · spec-documents — INFORME DE VALIDACIÓN

**Funcionalidad:** F13 spec-documents
**Rama:** `feature/F13-spec-documents`
**Objetivo (el corregido por la revisión de diseño, y es doble):** **A**, que el documento generado
**sustituya** a lo que hoy se mantiene a mano; **B**, extender la guardia anti-copia a los
documentos que **sí** llevan cifras vivas. El orden importa: si solo se suma, F13 es coste.
**Brief:** `docs/plan/features/F13-spec-documents.md`
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 0. Lo que hay que mirar primero

F13 iba a ser "generar un documento". Lo que la hace cara es otra cosa: **las guardias que se
escribieron encontraron defectos vivos**, y tres de las cuatro deudas que heredaba estaban **mal
enunciadas en el brief**. Nada de esto es hipótesis: cada fila se disparó sola, con su id.

| # | Lo que se encontró | Dónde | Coste si nadie lo mira |
|---|---|---|---|
| 1 | **Seis** formas de meter un valor de negocio en la forma ejecutable. La deuda (d) cerró una; la auditoría de cierre demostró cinco más | `c9ba546` | `tope: 9.5` en vez de `tope: perdida_maxima_diaria` sube el tope de pérdida diaria de 4,5 a 9,5 **sin tocar el registro y sin una queja** |
| 2 | RN-013 tenía **dos tipos en la misma casilla**: `a: si` es la cadena `'si'`, `a: no` es el booleano falso de YAML 1.1 | `c9ba546` | Un motor que compare con una cadena no apaga nunca `orden_limite_pendiente` al llenarse la orden, y RN-006 sigue reubicando una orden que ya es una posición viva |
| 3 | `feedback pending` daba por **reflejado** lo que no podía comprobar, y un caso estaba vivo | `c9ba546` | El `RESOLVE_CONTRADICTION` del 0,75 vs 0,8 salía como aplicado mientras `stop.nivel` sigue ABIERTA |
| 4 | `spec status` decía "0 todavía en prosa" con RN-028, de clase `gate`, sin condición definida | `c9ba546` | Quien lea el recuento concluye que la spec está lista para F22 |
| 5 | Una guardia **muerta**, escrita en esta misma rama: tres BACKSPACE literales (0x08) donde iban `\b` | `c9ba546` | No podía saltar nunca. Un barrido confirma que era el único sitio del repositorio con caracteres de control |
| 6 | Dos afirmaciones de negocio **falsas** en `PROJECT_STATE.md` | `c9ba546` | Es el primer fichero que lee toda sesión: quien implemente F22 leyéndolo construye un motor que abre en noticias en la cuenta que puede cerrarse por ello |
| 7 | El mapa del kit tenía una columna **parada desde F10** y nadie lo veía | `06f0708` | De las diez A-N nacidas después, ninguna figuraba en ella; en A-7 además decía otra cosa. El cuestionario hacía la UNIÓN de las dos fuentes, así que la unión tapaba la deriva |

## 0 bis. La auditoría de cierre (dos agentes, 2026-09-12)

Dos agentes en paralelo, código/tests y docs/proceso, con el encargo de no modificar nada.

### Código y tests

| Hallazgo | Estado |
|---|---|
| `feedback pending` daba por reflejado `contradiccion`, `regla` y `parametro`+REJECT | **CORREGIDO**. Tres estados en vez de dos (§3) |
| `comprobar_forma` se saltaba todo argumento que no fuera texto (`tope: 9.5`) | **CORREGIDO** |
| Una invocación con carga escalar se saltaba la comprobación entera | **CORREGIDO**: la carga viaja bajo una clave que ninguna regla puede escribir, y se juzga |
| Nadie exigía que una invocación trajera los argumentos que su predicado **declara** | **CORREGIDO**. Al encenderlo saltó un residuo real: `contexto_filtrable` seguía declarando `noticias` después de que ADR-0022 se las llevara a RN-028 |
| `_ESTRUCTURALES` escondía valores de negocio, y `a: si`/`a: no` tenían dos tipos | **CORREGIDO**: nace la sección `tokens` del vocabulario, y los dos se entrecomillan |
| `_ligaduras` admitía cualquier cosa: `liga: alcista` reabría el agujero | **CORREGIDO**: la ligadura tiene forma |
| `spec_docs` afirmaba "ninguna regla contiene números" sin que nada lo sostuviera | **CORREGIDO**: ahora lo sostiene `comprobar_forma`, y la frase dice quién |
| La precedencia escrita a mano en el generador | **CORREGIDO**: sale de `CLASES_REGLA` |
| Tautología y bucle muerto en `test_spec_docs_generados` | **CORREGIDO** |
| La hoja de la sesión 2 se habría llamado "Sesion 1" | **CORREGIDO** |
| El prefijo de la notación punteada no se validaba | **CORREGIDO** |
| La guardia del README de la spec era más estrecha que el problema | **CORREGIDO**, y al ensancharla apareció que además estaba **muerta** (fila 5 de §0) |

### Documentación y proceso

| Hallazgo | Estado |
|---|---|
| "A-17: se opera con noticias" en `PROJECT_STATE`, contra ADR-0022 | **CORREGIDO** |
| Cita al MASTER_PLAN por "lotaje sobre la distancia completa", que el plan ya no dice | **CORREGIDO** |
| **La mitad B del objetivo no se había entregado** | **CORREGIDO DESPUÉS**, en `5576c28` (§4) |
| El hueco que F13 cerró seguía declarado ABIERTO en cuatro documentos | **CORREGIDO** (MASTER_PLAN §0 bis y §G, `PROJECT_STATE`, README de la spec) |
| Recuentos caducados: 27 reglas, 24 vigentes, 21 preguntas, 116 registros | **CORREGIDO**, y ahora los vigila la guardia de §4 |
| El HANDOFF decía que F12 espera validación y no tenía sección de F13 | **CORREGIDO** |
| La plantilla del README del feedback ya no validaba desde que existe el corte | **CORREGIDO** |
| El registro que cierra A-14 no lleva `recibido_el`, siendo el problema que el campo resuelve | **CORREGIDO A MEDIAS Y DECLARADO**: el registro es inmutable y no se toca; `feedback new` ahora **avisa** cuando se escribe hoy un registro de una sesión anterior al corte sin declarar cuándo llegó |
| No existía ADR para el cambio de esquema del feedback | **CORREGIDO**: ADR-0023 |
| El índice de ADR no marcaba ADR-0011 como enmendado | **CORREGIDO** |
| El registro apuntaba a `mapa_parametros.yaml` por unas opciones que ya no están allí | **CORREGIDO** |
| El acta declaraba tres reversiones y son cuatro | **CORREGIDO** |
| El brief seguía con los enunciados desmentidos y con una salida que las capas impidieron | **CORREGIDO** en el propio brief, tachado y con el enunciado real |
| `stop.nivel` sigue ABIERTA | **REASIGNADO**: es trabajo de corpus (items nuevos que supersedan a los de 0,75), no de F13. §9 |
| A-15 y A-16 decididas y ABIERTA | **REASIGNADO**: cerrarlas está fuera de F13 por su §4. §9 |
| Las afirmaciones de negocio en prosa no las caza ninguna guardia | **NO APLICA como guardia**, y se declara por qué en §4 |

## 1. Qué se construyó

**(a) `docs/spec/` se genera.** `botsito spec docs [--escribir]` produce cuatro documentos, uno por
fichero fuente (D1), y `tests/contract/test_spec_docs_generados.py` **regenera y compara el texto
entero**, no un hash: el hash de la spec cubre tres ficheros y no `ambiguedades.yaml`, así que
sellar con él mentiría sobre una cuarta parte. El mensaje dice **qué fichero** no cuadra, y un test
comprueba que los otros tres siguen cuadrando. La forma ejecutable se imprime **verbatim** como
bloque JSON: parafrasear un árbol con `ninguno_de` y ligaduras perdería lo que F12 construyó.

**(b) Las cuatro deudas heredadas.** Tres estaban mal enunciadas, y eso es parte del resultado:

| # | Lo que decía el brief | Lo que era de verdad | Qué se hizo |
|---|---|---|---|
| a | "unificar `opciones` y decidir dónde viven `temas` y `ambiguedad`" | correcto, y además la columna `ambiguedad` llevaba **parada desde F10** | el mapa queda solo con `temas`; las `opciones` las da el registro y la `ambiguedad`, `ambiguedades.yaml`. La única arista viva (A-7 → `stop_segundo_esquema`) se mudó antes de borrar |
| b | "lista los 70 activos sin mirar si el valor ya llegó" | correcto | filtra, con criterio por tipo de objetivo (§3) |
| c | "compara el objetivo solo con el predecesor inmediato" | **falso**: comparar con el predecesor ya es transitivo | el hueco real era el **tiempo**: nada impedía que un registro corrigiera a otro POSTERIOR. No se podía cerrar antes de `recibido_el`, porque con `fecha` sola los 117 de la sesión 1 son del mismo día |
| d | "un argumento fuera de la lista admite un valor crudo" | correcto, **y era una de seis puertas** | se niega por defecto, y nace `tokens` |

Al unificar (a) moría el test que cruzaba las dos listas de opciones. Se repuso contra el
**paquete commiteado**, que es mejor guardia —mira la prueba de lo que se le preguntó al trader, no
el fichero del que salió— y en su primera ejecución encontró un renombre que la anterior no podía
ver: `desde_075` → `hasta_stop_fraccion` (ADR-0020), que queda declarado en una tabla con su motivo.

**(c) `DECIDIDA` (D4) y los dos campos del feedback (D5).** El estado `DECIDIDA` cierra lo que
decide el consultor y no el trader, con tres guardias semánticas —el ADR existe, el ADR **nombra**
la ambigüedad, y no vale sobre una `bloqueante` ni sobre una que sostenga el `ambiguedad_id` de un
parámetro— que hasta la auditoría **no probaba nada**: ahora las rompe un test, una a una, sobre una
copia del repositorio real. `recibido_el` y `procedencia` son opcionales en el esquema y
obligatorios por guardia desde el 2026-09-13, validados **al cargar** y no solo en `feedback new`.
ADR-0022 y ADR-0023.

**(d) La hoja que se lleva a la sesión** pasa de `scripts/hoja_sesion_docx.py` a
`src/botsito/cases/hoja_docx.py`, con `botsito kit hoja`. Era el único código que se ejecuta
**delante del trader** y el único sin red. El traslado destapó, en cuanto quedó al alcance de las
guardias, un `EURUSD` horneado —el instrumento lo dice el registro— y catorce `SystemExit` en lo que
ya es un módulo de librería.

**(e) `tokens`.** El vocabulario de la forma ejecutable gana una sección: los sujetos de geometría,
los estados y los campos de la operación, declarados uno a uno. Era la mitad que quedaba abierta al
invertir `_ARGS_DE_VALOR`, y estaba escrita como deuda en el propio código.

## 2. Lo que muere, y dos apartamientos del brief declarados

**Muere** (criterio 3): el §2 del acta de la sesión 1 —"la estrategia tal como queda
especificada", que ya había estado vieja dos veces en dos días, las dos en hechos de negocio— y el
recuento de `knowledge/spec/README.md`. El acta se queda con lo que solo ella puede decir: qué se
preguntó, qué respondió el trader y con qué minuto de v6.

**Apartamiento 1.** El brief §3.1 daba por muerto también `docs/spec/README.md` ("lo reemplaza el
índice generado"). **Sigue escrito a mano**, a propósito: explica qué es la carpeta y cuál de los
cuatro documentos NO está sellado por el hash, que es justamente lo que un índice generado no puede
decir de sí mismo. No lleva ninguna cifra viva y está bajo la guardia de §4.

**Apartamiento 2.** El brief §7 pedía "goldens: la spec real entra entera". No hay goldens
congelados: hay un contrato que **regenera** sobre la spec real entera y compara. Un golden
congelado habría que actualizarlo a mano cada vez que la spec cambia, que es la disciplina que F13
existe para no necesitar.

## 3. `feedback pending`: tres estados, no dos

La primera versión filtraba y cerraba con un `return False` —"el resto no se aplica a la spec"—. La
auditoría demostró que ese catch-all escondía casos, y uno estaba vivo. Pero negarlo todo habría
mentido en el otro sentido. Así que:

- **pendiente**: se puede comprobar que falta. Hoy hay **uno**, y es real: el
  `RESOLVE_CONTRADICTION` con el que el trader cerró el 0,75 vs 0,8, porque `_contradicciones.yaml`
  **se deriva de los items vivos** y ninguno se ha supersedido.
- **reflejado**: se puede comprobar que está.
- **sin mecanismo**: no hay forma mecánica de saberlo, y se dice en voz alta con su recuento, no se
  cuela en una de las otras dos. Son los ocho CORRECT/REJECT sobre evidencia: el item **cita bien**
  lo que se dijo en el vídeo —v4 sí contiene la propuesta de un tercer esquema; lo que el trader
  hace es no adoptarla— y su efecto entra por el parámetro.

La decisión salió de dentro de la función a `situacion_de`, para poder probar los dos criterios que
**no tienen ningún caso real todavía**: hoy no existe ni un registro con objetivo `regla`, y los
once REJECT sobre parámetro están todos aplicados.

## 4. La mitad B, que no se había entregado

La auditoría de docs lo levantó: las guardias anti-copia seguían siendo exactamente las dos de antes
de F13, y **siete de sus hallazgos son consecuencia directa**.

`tests/contract/test_documentos_vivos.py` prohíbe pegar un recuento —"27 reglas", "59 parametros",
"21 preguntas", "116 registros de feedback"— en los documentos que describen el presente. Habría
cazado cuatro de los hallazgos de hoy, y al encenderla saltaron dos copias vivas más.

**Lo que NO cubre, y por qué.** Una afirmación de negocio en prosa ("se opera con noticias", "el
lotaje va sobre la caja completa") no se puede vigilar así: se intentó, se midió, y los mismos
patrones casan con narración histórica legítima —un item de evidencia que **dice** eso, un riesgo
que una tabla del plan enumera—. Una guardia con falsos positivos se desactiva sola. Eso lo sigue
cazando una auditoría con ojos, y por eso se hace una por rama.

Exenciones en dos niveles y **nombradas**: ocho secciones de `PROJECT_STATE` que son archivo y no
presente —y un test comprueba que cada una **existe**, para que renombrarlas rompa esto en vez de
ensancharlo en silencio— y una exención por línea con motivo obligatorio,
`<!-- cifra-congelada: <motivo> -->`.

## 5. Cómo ejecutarlo

```
uv run botsito spec docs                 # comprueba; --escribir regenera
uv run botsito spec check                # la capa semantica sola
uv run botsito spec status               # la vista viva
uv run botsito feedback pending [--todos]
uv run botsito kit hoja [--sesion <s>]   # la hoja de la sesion en Word
uv run botsito kit check --sesion 2026-09-09-sesion-01
make check
```

## 6. Qué está corriendo hoy

El recuento vivo lo dan `botsito spec status` y `botsito knowledge validate`, y **no se copia**: lo
que sigue es la instantánea del cierre, 2026-09-12, cada cifra de un comando ejecutado ese día.

- spec **10.1.1**, hash `f11b708ae3f8…`; 25 reglas vigentes y 3 descartadas; 24 con forma
  ejecutable y **una vigente sin condición definida**: RN-028, bajo A-17.
- 59 parámetros: 50 confirmados, 2 con un default nuestro, 7 sin valor a propósito.
- 117 registros de feedback, 22 ambigüedades, 353 items de evidencia, **1 contradicción abierta**.
- `feedback pending`: 1 pendiente de 72 activos, 63 reflejados, 8 sin forma mecánica de comprobarlo.
- `kit check` de la sesión 1: exit 0, con los dos avisos que explica la sesión celebrada.

## 7. Los siete criterios de aceptación, uno a uno

| # | Criterio (§8 del brief) | Evidencia | |
|---|---|---|---|
| 1 | `make check` verde, `knowledge validate` y `spec check` incluidos | ruff, ruff format, mypy strict, 4 contratos KEPT, pytest, `state check`, `config validate`, `knowledge validate`: todo exit 0 | **CUMPLE** |
| 2 | `docs/spec/` generado, con guardia que falla si se edita a mano o si la spec cambia sin regenerar | `test_spec_docs_generados.py`, con un test que **rompe** un documento en un repo falso y comprueba que se denuncia nombrándolo | **CUMPLE** |
| 3 | Al menos dos copias vivas mueren | §2 del acta y recuento del README de la spec; la guardia del README está **invertida**: ahora exige que NO haya recuento | **CUMPLE** |
| 4 | Las cuatro deudas cerradas o reasignadas con su motivo | §1(b); tres con el enunciado corregido, y el motivo queda escrito en el código, en el brief y aquí | **CUMPLE** |
| 5 | `DECIDIDA` y los dos campos existen **con su guardia**, no solo en el esquema | las tres guardias semánticas de `DECIDIDA` las rompe un test una a una; los dos campos se validan al cargar | **CUMPLE** |
| 6 | El paquete de la sesión 1 sigue dando exit 0 en `kit check` | ejecutado hoy: OK, con los dos avisos esperados | **CUMPLE** |
| 7 | Los registros de feedback conservan su id | `knowledge validate` dice "historial intacto", que es el test que compara byte a byte contra la primera versión commiteada. Los 116 previos conservan su id; hoy son 117 porque A-14 sumó uno | **CUMPLE** |

## 8. Deuda que F13 deja anotada

1. **El valor de un argumento estructural no se contrasta con un catálogo cerrado** en un caso: los
   tokens están declarados, pero nada impide declarar un token nuevo que sea en realidad un valor de
   negocio. La puerta es mucho más estrecha que antes y queda escrita en el código.
2. **Un `CORRECT`/`REJECT` sobre evidencia no tiene mecanismo de aplicación.** Son los ocho "sin
   mecanismo" de §3. Decidir si el corpus debe supersederlos es trabajo de F06/F07, no de aquí.
3. **La guarda del holdout de `tests/conftest.py` sigue siendo un stub** (ADR-0021, F14).
4. **`docs/spec/` no incluye `spec_manifest.yaml`**: los cuatro documentos salen de los otros
   cuatro ficheros. No hay nada que un humano necesite leer del manifiesto que `spec status` no dé.

## 9. Qué debe decidir el usuario

| | Decisión | Bloquea | Recomendación |
|---|---|---|---|
| 1 | **Validar F13** y, si procede, el ritual de merge | F14, que comparte esquema y necesita `feedback pending` fiable | validar: los siete criterios cumplen y la auditoría está aplicada |
| 2 | **Pedirle al trader un mes que no haya tocado** (febrero o marzo de 2026) | F26 de verdad | pedirlo **hoy**: tiene semanas de plazo, exige `data download`, y hasta que llegue no existe ninguna partición limpia. Mayo está expuesto y junio descartado |
| 3 | **El reparto de mayo para F14**: 6 días `dev` y 13 de holdout, frente a los 16/8/8/8 que pedía `config.yaml` | F14 | aceptar 6/13 con un ADR, mientras no exista ningún `LABEL_CASE`; con la advertencia de que 6 días es una biblioteca pequeña y la partición limpia real será la de (2) |
| 4 | **El ADR que cierre A-15 y A-16** como `DECIDIDA` | la sesión 2 | escribirlo antes del `kit build` de la sesión 2: están decididas desde el 2026-09-09 y, mientras sigan ABIERTA, se le vuelve a preguntar al trader lo que ya decidimos. El mecanismo ya existe; cerrarlas quedó fuera de F13 por su §4 |
| 5 | **`stop.nivel` (0,75 vs 0,8)** sigue ABIERTA en `_contradicciones.yaml` | nada hoy | dejarla abierta **a propósito** y que `feedback pending` siga enseñándola. Cerrarla exige items de evidencia nuevos que supersedan a los dos de 0,75; fabricarlos para que un contador dé cero sería lo contrario de lo que el proyecto hace |

## 10. Qué puede comprobar sin recursos especiales

Sin `data/`, sin GPU y sin el corpus de vídeo:

```
uv run botsito spec docs         # OK en los cuatro
uv run botsito spec status
uv run botsito feedback pending  # 1 pendiente, 8 sin mecanismo
make check
```

Y tres roturas a propósito, que es como se comprueba que una guardia no es decorativa:

1. **edite a mano una línea de `docs/spec/reglas.md`** → `make check` falla y **nombra el fichero**;
2. **cambie `tope: perdida_maxima_diaria` por `tope: 9.5`** en RN-020 de `strategy_spec.yaml` →
   `spec check` falla diciendo que un argumento lleva el NOMBRE, no el valor;
3. **pegue "27 reglas" en `knowledge/spec/README.md`** → `make check` falla y le dice qué comando
   da ese número.

Deshaga los tres con `git checkout --`.

## Estado

WAITING_FOR_USER_VALIDATION
