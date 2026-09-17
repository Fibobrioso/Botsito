# Las correcciones de fidelidad de la spec — INFORME DE VALIDACIÓN

**Rama:** `trabajo/fidelidad-de-la-spec` (rama de trabajo sin número propio, MASTER_PLAN §F), desde `main` en `0a98edd`
**Cierre previsto:** tag `stable/F13-fidelidad`
**Decisiones:** ADR-0031 (el freno de la firma antes del límite) y ADR-0032 (de dónde sale cada hecho y cada evento, y cómo nace la orden). Notas en ADR-0014 y ADR-0028
**spec_version:** 11.1.0 → **12.0.0**, un solo bump, en el commit `feat(spec)` de la rama
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 1. Por qué existe esta rama

Leída al pie de la letra, la `forma` que F18-F22 van a implementar **no colocaba ninguna orden**,
**vetaba las dos direcciones en las que el trader opera** (RN-005), **abría posiciones sin objetivo**
por una de las dos vías de activación y **podía evaluar el límite de la firma sobre P/L realizado**.
Y contradecía un ADR ACTIVE (ADR-0028 §5) sin que ninguna guardia lo viera. El brief pedía nueve
correcciones, las cinco del informe de FTMO «al brief siguiente» y ADR-0028 §5, todo antes de F18.

No se ha escrito una línea de motor. No se ha tocado `knowledge/evidence/` ni `knowledge/feedback/`.
No se ha abierto ningún holdout ni se ha ejecutado `kit check` o `kit build` (los dos leen velas de
días reservados cuando `data/` está presente).

## 2. La revisión de diseño (dos agentes, antes de programar)

Dos agentes en solo lectura, con los resultados en disco: **A** (Opus) sobre el esquema y las
guardias, con mediciones ejecutadas sobre copias en memoria; **B** (Sonnet) sobre el corpus, el
margen de la firma y el cuestionario. Todo lo que dijeron y chocaba con el brief lo comprobé en el
corpus o en el código antes de aceptarlo.

### 2.1 Las tres preguntas del brief

**Q1 · Cómo se declara el origen de un hecho derivado del bróker sin romper la guardia de productor
real, y cómo se prohíbe fijarlo.** Con `origen: broker`, `decision` (el ADR que lo deriva) y
`lo_provoca` (las ACCIONES que lo hacen verdadero), sin `produce`. La guardia exige:
- que ninguna forma lo fije: cualquier `fijar` sobre él en un `entonces` es un error con el id de la
  regla;
- que cada acción de `lo_provoca` exista y la ejecute alguna regla vigente.

Esto último sustituye a «tiene un productor real». Sin ello, derivar del bróker habría dejado a
RN-002, RN-014, RN-030 y RN-006 inalcanzables en silencio, que es exactamente lo que ya pasaba con
`se_coloca_orden_limite`. Se descartó `produce: [broker]`, que mezcla un nombre mágico con ids de
regla (ADR-0032).

**Q2 · Margen, lectura prospectiva o las dos.** Las dos, porque arreglan cosas distintas:

| | Desbordamiento por construcción | Deslizamiento, gap, costes, equity flotante antes del cierre |
|---|---|---|
| Lectura prospectiva | **lo cierra** para el riesgo nominal | no |
| Margen | solo si es de al menos un riesgo, a costa de operar menos siempre | **deja colchón** |

`s05a` ([d1-interprete-04]): tras nueve pérdidas, 4.388,99 acumulado; se abre la décima porque
`alcanza_tope` no descuenta la operación que se abre, y el día acaba en 4,865 %. Con la aritmética
en el borde, el peor caso de cada tope con la lectura vigente es el tope más un riesgo: 4,9775 %
(trader, con 100.000 al empezar el día), 5,475 % (firma diaria) y 10,45 % (firma total). Ninguna de
las dos cubre un gap mayor que el margen (ADR-0031).

**Q3 · `permanente` sin condicionar una acción a una rama de `cualquiera_de`.** Con **un hecho
aparte** (`detenido_por_tope_total`, valor `permanente`) y **una regla hermana** (RN-031), no con
otro valor del mismo hecho. RN-020 y RN-029 leen `detenido_por_tope` sin mirar su valor y lo
reescriben en cada evento: machacarían el `permanente`. Y dos gates de la misma clase fijando el
mismo hecho con valores distintos en el mismo evento dejarían el resultado al orden del fichero, que
ADR-0018 prohíbe. RN-001 lee el hecho nuevo.

### 2.2 Hallazgos que el brief no vio, y qué se hizo

| Hallazgo | Quién | Qué se hizo |
|---|---|---|
| **No se puede renombrar ningún parámetro que cite al trader** (`reentrada_tras_equal`, `salida_sin_ruptura`, `cartucho_criterio`): `knowledge validate` pasa TODOS los registros de feedback, también los supersedidos, contra el registro, y cuatro registros inmutables los nombran | A | P2.3 se hace con tokens y descripciones. Ningún valor cambia, así que tampoco hace falta `valor_canonico` |
| **Colocar y comprobar en la misma regla deja a los gates sin ventana**: RN-026 y RN-027 necesitan lote y niveles calculados antes de enviar | A | Dos reglas encadenadas por un hecho (§3, P2.2) y `efecto` en la acción que envía |
| **`prohibe: [abrir_operacion]` no estaba ligado a ninguna acción** | A | `colocar_orden_limite` lleva `efecto: abrir_operacion`; toda acción que provoca un hecho o un evento del bróker tiene que declararlo |
| **RN-019 no podía disparar nunca**, y no solo por el token: unía en un `todos_de` un evento del bróker (`se_cierra_operacion`) con uno del cierre de M1 (`vuelve_a_dar_el_esquema`), pulsos de fases distintas que con ADR-0028 no coinciden | A | RN-019 dispara con el cierre solo, reconocido por cómo se activó; la reentrada va por la colocación normal (§3, P2.3) |
| **Ninguna guardia validaba las claves del vocabulario**: un `origen` mal escrito se habría ignorado | A | Claves cerradas por sección (`comprobar_vocabulario`) |
| **`complementa` solo se validaba por formato**: un id inexistente o una regla descartada eximían igual | A | `comprobar_precedencia` lo comprueba |
| **Los CUATRO mutantes de `comprobar_precedencia` sobrevivían**, no uno: dos denuncias no las ejecutaba nadie y las otras dos saltaban juntas | A | Un test que dispara cada una por separado |
| **El corpus no fija cuándo nace la orden límite**: `ev-v3-004201` la marca con el breaker; `ev-v1-001358` la va «bajando» en cuanto rompe la liquidez; `ev-v3-002511` la tiene «predefinida»; y en la sesión 1 (v6 1:22:14) ya está en la zona de «posible breaker» y se activa sin validar | A, comprobado en la transcripción | **A-29** (pregunta) y `orden_limite_nace` DEFAULT_AMBIGUOUS. Ver §4 |
| **El cierre del equal de v6 1:23:13-1:23:19 es una pérdida real** («te genera una pérdida»), y justo después el trader vuelve a colocar la orden | B, comprobado en la transcripción | Confirma el motivo de P2.3 tal como estaba escrito. Además, en v6 0:52:50 el trader empieza diciendo que la reentrada tras un equal «sí es considerado» y se corrige en el acto: «no, no es considerado». El literal registrado es el corregido |
| **Ningún item de evidencia junta en su propia frase el sesgo y el lado** de la liquidez: la ligadura de RN-005 es lectura del tramo | B | Declarado en las notas de RN-005 y en la descripción del predicado |
| **A-24..A-26 están reservadas** para F14b (`test_kit`): las ambigüedades nuevas no pueden ser A-24 | A | Se numeran A-29 y A-30 |
| **La rama no tiene CI**: `ci.yml` solo dispara en `main`, `feature/**` y `fix/**` | A | Lo que valida la rama es `make check` en local |

**Descartado de la revisión:** tipar cada predicado como `evento | estado` además de su `fuente`
(A lo proponía). Solo `fuente` lo pide una guardia, y un campo que nada comprueba es decorativo.

## 3. Qué se hizo, punto por punto

| Punto | Hecho | Dónde |
|---|---|---|
| **1 · ADR-0028 §5** | `operacion_abierta` y `orden_limite_pendiente` con `origen: broker`, `decision: ADR-0028` y `lo_provoca: [colocar_orden_limite]`. RN-010, RN-011 y RN-013 dejan de fijarlos. Fijarlos salta con el id de la regla | ADR-0032; `comprobar_forma`; F14b §0 anotado como deshecho |
| **2.1 · RN-005** | El predicado pasa a `se_desarrolla_en_el_lado_de_ruido`, con `lado_de_ruido: {alcista: por_encima, bajista: por_debajo}`. Dos citas, una por sentido: RN-005 cita el bajista (`ev-v3-001725`, «la operativa está por encima no por debajo»), el predicado el alcista (`ev-v1-001306`, «nuestra operativa tiene que estar por debajo») | `alcista` y `bajista` **no** son tokens a propósito: si lo fueran, `sentido: alcista` volvería a pasar la guardia de argumentos que cerró F13 |
| **2.2 · colocar** | `colocar_orden_limite` (con `efecto`). **RN-011** prepara: con `toca_colocar_orden_limite` (momento según `orden_limite_nace`) y sin orden pendiente ni posición viva, dimensiona el lote, escribe el stop y fija `orden_dimensionada` con la zona. **RN-015** coloca: escribe el objetivo, envía la orden y apaga el hecho. `se_coloca_orden_limite` y `vuelve_a_dar_el_esquema` desaparecen. `retirar_orden_limite` queda **declarada y sin regla**: lo de la pendiente a las 15:00 es **A-30** | ADR-0032 |
| **2.3 · `equal`** | El token `equal` desaparece. Quedan `activacion_sin_ruptura` (cómo se activó), `break_even` (resultado, clasificado por **mecanismo** y no por el P/L neto de costes) y `cualquier_resultado` / `cualquier_activacion`. `se_cierra_operacion` gana el argumento `por` y declara su conjunto cerrado de valores. RN-016 solo gasta con `por: cualquier_esquema`; RN-019 dispara con `por: activacion_sin_ruptura`. El glosario conserva `equal` como geometría y gana «cerrar un equal» | Sin renombrar parámetros (§2.2) |
| **2.4 · el instante** | Stop (RN-011) y objetivo (RN-015) se escriben antes de enviar, en la cadena que coloca la orden. Ninguna regla los escribe ya al llenarse. RN-013 queda **DESCARTADA por absorbida**: sin sus dos `fijar` y sin reescribir el stop, su `hace` quedaba vacío, y lo que afirma (un único stop) es ahora cierto por construcción. La base del objetivo **no se toca**: se anota en RN-015, en la cabecera de ADR-0014 y en la descripción de `base_calculo_objetivo`, que usaba la premisa revocada | Test: la única regla que coloca escribe el objetivo antes |
| **3 · margen** | `firma_margen_seguridad` (0,5, **a validar**). RN-029 (diario) y RN-031 (total) frenan en límite − margen; RN-030 cierra ahí; **RN-032** es la lectura prospectiva, solo para la firma. El tope del trader (RN-020) no cambia de lectura: su desbordamiento queda declarado en sus notas | ADR-0031 |
| **4 · `clase`** | `medicion | pregunta` en `ambiguedades.yaml`: opcional en el esquema y obligatoria por guardia en toda ABIERTA (en `knowledge validate`). El cuestionario no incluye mediciones. `spec status` separa «falta preguntarlo» de «falta medirlo». A-16, A-27 y A-28 son medición; A-13, A-18, A-21, A-29 y A-30, pregunta | `abiertas_sin_clase`; test con el cuestionario real, sin `data/` |
| **5 · RN-030** | `terminal`, como su gemela RN-002. ADR-0018: el gate «prohíbe o frena»; el terminal cierra y gana a mover un stop, que es lo que hace falta frente a RN-014. Medido: como terminal, `comprobar_precedencia` da `[]` con y sin `complementa`; como gate sin él, denuncia el subconjunto. `complementa: [RN-029, RN-031]` se conserva porque dice la verdad | Test propio de la clase; y el de los cuatro mutantes |
| **6 · ligadura** | `comprobar_ligaduras`: toda ligadura usada (en `entonces` y en `cuando`) tiene que estar atada en un camino de `todos_de` desde la raíz. Mira la forma del nombre, no el catálogo. Falla con la RN-029 de antes del 2026-09-14; pasan RN-002, RN-005, RN-006, RN-014 y RN-030 | Commit propio, antes que la spec |
| **7 · magnitud** | `magnitud: firma_magnitud_vigilada` en los dos acumuladores de la firma. `comprobar_consumo` solo cuenta como lector una **forma** vigente (un argumento, o un campo de un acumulador que una forma usa). Quitar `magnitud` hace saltar la guardia | §5 |
| **8 · permanente** | Token `permanente` (clase `duracion`), hecho `detenido_por_tope_total` con `valores: [permanente]`, RN-031. Los hechos declaran `valores`, y fijar `permanente` en `detenido_por_tope` salta | Q3 |
| **9 · `reinicia_con`** | `perdida_total_firma.reinicia_con: nunca`, token de clase `reinicio`. **Reescrito respecto al brief**: la guardia no prohíbe un parámetro, prohíbe uno que no sea enum. Con «nunca un parámetro», cuatro de los cinco acumuladores vigentes fallaban (`reloj_dia_riesgo` en tres, `cartuchos_reinicio`). `firma_perdida_total_arrastra` pasa al campo `arrastra`, que es lo que es: una propiedad de la base | Test con un booleano y con un token de otra clase |

## 4. Lo que cambió respecto al brief, y por qué

| Pedía el brief | Se hizo | Motivo |
|---|---|---|
| 2.2 · «la regla que la dispara **al darse el esquema de entrada**» | Una condición con el momento en un parámetro (`orden_limite_nace`), DEFAULT_AMBIGUOUS en `al_darse_el_esquema`, y **A-29** abierta | El corpus sostiene dos momentos (§2.2). El default es el único literal que nombra el momento, y con la otra lectura RN-008 frenaría la propia colocación. Con la otra lectura hay que reescribir RN-008; con el default, **RN-010 se vuelve difícil de alcanzar** (inferencia nuestra: la orden nace ya con el breaker). Las dos consecuencias están escritas en A-29 y en la descripción del parámetro |
| 2.2 · `colocar_orden_limite` con argumentos zona, lote, stop, objetivo | Argumento `en` (la zona); lote, stop y objetivo como **acciones hermanas** escritas antes | Un argumento solo lleva un nombre. Y los gates tienen que ver el lote y los niveles antes de enviar |
| 2.2 · una regla que coloca | **Dos** reglas encadenadas (RN-011 prepara, RN-015 coloca) | ADR-0028 §4 no ordena dos disparadores dentro de un evento; con una sola, los gates no tienen ventana; con tres, el que coloca podía disparar antes que el del objetivo (ADR-0032) |
| 2.3 · renombrar `reentrada_tras_equal` y `cartucho_criterio` si hiciera falta, con `valor_canonico` | Ningún renombre | Imposible sin tocar feedback inmutable (§2.2) |
| 2.3 · RN-019 con el token nuevo | RN-019 **reescrita**: dispara con el cierre solo; `reentrar` ya no envía nada | Con el token nuevo seguía sin poder disparar (§2.2). **Lectura nuestra, declarada**: se trata igual todo cierre de una operación activada sin ruptura, porque la spec no puede reconocer el equal en sí |
| 8 · `detenido_por_tope: permanente` | Hecho aparte, `detenido_por_tope_total` | Q3 |
| 9 · «`reinicia_con` solo admite un token de reloj o evento, nunca un parámetro» | Token de clase `reinicio` **o parámetro enum**; nunca booleano ni cifra | Cuatro de cinco acumuladores usan un parámetro legítimo como reinicio |
| 3 · «un parámetro y/o la lectura prospectiva» | Los dos, y la prospectiva solo para la firma | ADR-0031. Cambiar la lectura del tope del trader sería atribuirle una regla que no dijo |
| 4 · obligatorio «desde la sesión 2» | Obligatorio en toda ABIERTA del fichero real, comprobado por `knowledge validate` y no por la construcción del paquete | El kit construye paquetes sobre repositorios de prueba con ambigüedades sin `clase`; el fichero que alimenta la sesión 2 es el real |

## 5. Lo que destapó el endurecimiento de `comprobar_consumo` (P7)

Medido antes de cambiar nada (revisión A). Parámetros con valor que figuraban en la lista
`parametros` de una regla vigente y **ninguna forma leía**, sin `consumido_por`:

| Parámetro | Qué se hizo |
|---|---|
| `firma_magnitud_vigilada` | **Lector ejecutable**: campo `magnitud` de `perdida_dia_firma` y `perdida_total_firma` |
| `instrumento_digitos` | **Lector ejecutable**: argumento `digitos` de `distancia_menor_que` (RN-026), que traduce el mínimo del bróker de puntos a precio |
| `anclaje_h4` | `consumido_por: [F15]`: la rejilla H4 la construye la agregación de velas («H4 reproducible para cualquier `anclaje_h4`», MASTER_PLAN), no una regla |
| `sesgo_h4_regla` | `consumido_por: [ADR-0019]`, con la descripción diciendo por qué: mezclaba sujeto y criterio, y la forma los separa en `rompe` y en `sesgo_h4_criterio_ruptura`. Se conserva porque es la respuesta del trader |
| `firma_perdida_total_arrastra` | Habría sido el quinto al salir de `reinicia_con`: lo lee el campo `arrastra` del acumulador |

Contar los campos de los acumuladores como lectura es necesario. Sin ellos salían siete falsos
positivos más (`base_calculo_perdida_*`, `cartuchos_reinicio`, `reloj_dia_riesgo`,
`saldo_inicial_cuenta`, `firma_base_perdida_diaria`…).

Siguen listados en `parametros` de su regla sin que SU forma los lea, pero con lector en otra forma
(no son huérfanos, se deja constancia): RN-003 (`anclaje_h4`, `sesgo_h4_regla`), RN-012
(`stop_fraccion_caja`), RN-017 (`cartuchos_max`) y RN-029 (`saldo_inicial_cuenta`, base del porcentaje
del límite diario). La guardia no se ha bajado para ninguno.

## 6. La auditoría de cierre

Dos agentes en paralelo (Sonnet, solo lectura, prohibido `kit check`, `kit build`, `data/` y el
holdout): uno sobre código, spec y tests, con mutantes en memoria contra las funciones reales; otro
sobre ADR, documentos vivos y proceso.

**Lo que comprobaron y se sostiene.**
- Cada cita con minuto de las notas nuevas está en la transcripción, incluido el sesgo bajista de
  `ev-v3-001725` por contexto (v3 0:12:34 y 0:15:08).
- La aritmética cuadra: 4.388,99, 478,06, 4.867,05, 4,9775 %, 5,475 %, 10,45 % y 111.111,11.
- Los ocho mutantes pedidos hacen saltar su guardia, y apagar `comprobar_ligaduras` o
  `comprobar_vocabulario` rompe tests reales.
- Las tres guardias de cita recorren `acciones`.
- Hay un solo bump del manifiesto, 11.1.0 → 12.0.0.
- Los directorios inmutables no se tocaron.
- Los ids del trailer `Fuente:` existen.
- No hay caracteres de control en los ficheros tocados.
- Los ADR dicen lo que el código hace.

| Hallazgo | Gravedad | Quién | Qué se hizo |
|---|---|---|---|
| `PROJECT_STATE`, índice de ADR: ADR-0028 seguía diciendo «la spec todavía fija `operacion_abierta` y `orden_limite_pendiente`» | grave | documentos | **Corregido** |
| `comprobar_forma` contaba como productor real a una regla DESCARTADA que conservara su forma (mutante: RN-013 con una forma que fija `detenido_por_tope` pasaba). Latente: hoy ninguna descartada conserva forma | media | código | **Corregido** (solo cuentan las vigentes) y **test** del mutante |
| ADR-0031 e informe: «la décima solo se abriría con un margen por debajo de 0,13»; el umbral exacto es 0,133, así que con 0,13 también se abre | media | código | **Corregido** en los dos |
| `Current Feature` de PROJECT_STATE seguía diciendo que lo siguiente era el brief de esta misma rama | media | documentos | **Corregido** |
| `firma_margen_seguridad` es CONFIRMED y su descripción dice «decisión pendiente de validar»; no sale en `spec status` | menor | código | **No se cambia el estado, y se dice por qué**: la cierra un ADR, no el trader ni una medición, así que no cabe en una ambigüedad; lo que falta es la validación de esta rama, y está en §7. Si el valor cambia al validar, cambia en el registro y en ADR-0031 antes del merge |
| MASTER_PLAN, fila del veto de riesgo: solo nombraba RN-029 y RN-030 | menor | documentos | **Corregido**: nombra RN-031, RN-032 y el margen |
| El literal de «cerrar un equal» (v6 1:52:26) puntúa como pregunta una frase que el ASR da como afirmación | menor | código | **Sin cambio**: es el `respuesta_literal` del registro de feedback, copiado tal cual, y la guardia de literales lo compara por tokens |

## 7. Qué debe decidir el usuario

1. **¿Validar la rama y hacer el ritual** (§9)?
2. **El valor del margen de la firma, 0,5** (ADR-0031). Implica que, con 100.000 o más al empezar el
   día, la décima pérdida seguida del día no se abre. Con 0,25 pasaría lo mismo; solo con 0,13 o
   menos (el umbral exacto es 0,133) se volvería a abrir. Mientras la pérdida del día más el riesgo de la operación siguiente
   quede por debajo de 4.500, el margen no cambia nada. ¿0,5, otro valor, o se prefiere que el
   margen sea exactamente un riesgo por operación?
3. **A-29, el default de cuándo nace la orden.** Corre con `al_darse_el_esquema`, que es la única
   frase que nombra el momento, pero la sesión 1 (v6 1:22:14) describe la orden ya puesta antes de
   validar. ¿Se deja el default hasta preguntarlo, o se prefiere la otra lectura, reescribiendo
   RN-008 en otra rama? Con el default, RN-010 (activación sin ruptura) se vuelve difícil de alcanzar.
4. **RN-019, lectura nuestra.** Todo cierre de una operación activada sin ruptura habilita la
   reentrada sin gastar cartucho, aunque no haya equal. ¿Aceptable, o se lleva a la sesión 2 junto
   con A-29?
5. **RN-013 DESCARTADA por absorbida.** No se descarta lo que dijo el trader (el stop es único): se
   descarta una forma que se quedaba vacía. ¿Se acepta el estado, o se prefiere conservarla
   VIGENTE con otra forma?
6. **ADR-0032 punto 3** precisa ADR-0028 §4: una acción con `efecto` no se ejecuta si un gate
   prohíbe ese efecto en ese instante, y el resto de la regla sí. Es la semántica que F22-F23 tienen
   que implementar. ¿De acuerdo?

## 8. Cómo comprobarlo

```
git checkout trabajo/fidelidad-de-la-spec
make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log
uv run botsito spec check                   # spec 12.0.0, sin problemas
uv run botsito spec status                  # "falta MEDIRLO" separado de "falta preguntarlo"
uv run botsito knowledge validate           # trailers Fuente y clase en toda ABIERTA
uv run pytest tests/unit/test_spec_fidelidad.py -q
git log --oneline 0a98edd..HEAD
git diff 0a98edd..HEAD --stat -- knowledge/evidence knowledge/feedback   # vacio
git log -p 0a98edd..HEAD -- knowledge/spec/spec_manifest.yaml | grep spec_version   # un solo bump
```

## 9. El ritual de cierre (lo ejecuta el usuario)

Nada de esto lo ha hecho la sesión: ni merge, ni tag, ni push. Git Bash desde la raíz, con
`BOTSITO_ALLOW_MAIN=1` exportada durante toda la secuencia:

```
export BOTSITO_ALLOW_MAIN=1
git checkout main
git status --short                 # vacio

git merge --no-ff trabajo/fidelidad-de-la-spec -m "merge: las correcciones de fidelidad de la spec"
git tag -a stable/F13-fidelidad -m "Fidelidad: RN-005, la colocacion, equal, los instantes y el freno de la firma; spec 12.0.0"
git rev-parse --short HEAD         # el sha del merge

# docs(state) que toca SOLO PROJECT_STATE.md:
#   Current Branch: main · Current Feature: ninguna abierta · Stable Main State y Last Stable Commit:
#   sha del merge, tag stable/F13-fidelidad · Completed Features: + "Fidelidad de la spec · validada el
#   <fecha> · docs/validation/FIDELIDAD-DE-LA-SPEC.md · tag stable/F13-fidelidad" · Features Waiting
#   for Validation: "— ninguna." · Change Log: la entrada del 2026-09-16 pasa a "cerrada en main"
git add PROJECT_STATE.md
git diff --cached --name-only      # SOLO PROJECT_STATE.md
git commit -m "docs(state): las correcciones de fidelidad, cerradas en main (stable/F13-fidelidad)"

make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log

git push origin main
git push origin stable/F13-fidelidad
unset BOTSITO_ALLOW_MAIN
```

Entre el merge y el `docs(state)`, `state check` falla a propósito. Si `make check` falla en el
paso de después, no se pushea. La CI que cuenta es la del `docs(state)`:
`curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`.

## Estado
WAITING_FOR_USER_VALIDATION
