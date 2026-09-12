---
status: ACTIVE
date: 2026-09-12
phase: F13
---

# 0023 · El registro de feedback sabe cuándo llegó cada respuesta y por dónde

## Decision

1. **`FeedbackRecord` gana dos campos: `recibido_el` y `procedencia`.** `fecha` sigue siendo la de
   la **sesión** —fecha la PREGUNTA— y `recibido_el` es el día en que llegó la RESPUESTA.
2. **Son opcionales en el esquema y obligatorios por guardia desde la sesión del `2026-09-13`**
   (`CORTE_PROCEDENCIA`). No es una concesión: es la única forma de tenerlos sin destruir el
   corpus, y está medida (§ Por qué).
3. **`procedencia` es un enum de seis valores**, sacados de los 117 registros reales y no
   imaginados: `trader_grabado`, `trader_hoja`, `trader_escrito`, `referido_por_consultor`,
   `reexpresion_consultor`, `correccion_consultor`.
4. **No es decorativo: se cruza con `medio` y con `supersede`.** `trader_grabado` exige un medio
   grabado; `trader_escrito` y `referido_por_consultor` exigen `medio: escrito`;
   `correccion_consultor` exige `supersede`, porque no trae una respuesta nueva sino que retira lo
   que otro registro afirmaba.
5. **`recibido_el` no puede ser anterior a `fecha`**: una respuesta no llega antes de que se
   pregunte.
6. **Una corrección no llega antes que lo que corrige.** Si `r.supersede` apunta a un registro
   POSTERIOR en el tiempo, se denuncia. Esta comprobación **no se podía hacer antes de estos
   campos**: con `fecha` sola, los 117 registros de la sesión 1 son del mismo día y la
   comparación no distinguía nada.
7. **Las guardias se aplican AL CARGAR, no solo en `feedback new`.** Un fichero escrito a mano se
   salta el CLI; es la lección que `knowledge validate` ya había aprendido con `feedback apply`.

## Problema que resuelve

`fecha` hace dos trabajos y solo puede hacer uno bien. Los 117 registros de la sesión 1 se fechan
el **2026-09-09**, y eso es correcto: pertenecen a esa sesión. Pero **cuatro de ellos no llegaron
ese día**: A-11 se cerró el 10, el acuerdo del lotaje y el WhatsApp de A-20 llegaron el 11, y el
cierre de A-14 se confirmó el 12. Leídos por su `fecha`, los cuatro son del 9.

Eso importa por una razón concreta y fechada: **el 2026-09-11 hubo una exposición de holdout**
—el calendario de PnL día a día de todo mayo, trece días reservados— declarada en
`docs/validation/HOLDOUT-EXPOSICIONES.md` por ADR-0021. Cuando F26 mida fidelidad, tendrá que
poder decir **qué valores de la spec se fijaron ANTES de esa exposición y cuáles después**. Con
`fecha` sola, esa frase no se puede sostener mecánicamente: hay que reconstruirla leyendo notas.

`procedencia` resuelve el segundo: `medio` dice por qué canal llegó (replay, audio, video,
escrito) pero no **quién lo dice**. No es lo mismo el trader hablando en una grabación que el
consultor reexpresando lo que entendió, y el proyecto entero descansa en esa diferencia
(ADR-0016: una regla que dice más que su literal declara `decision`).

## Impacto

- **Los 117 registros conservan su id EXACTO. Cambian 0, medido y con test.**
  `contenido_canonico` salta el campo ausente, que es el mismo mecanismo con el que F11 añadió
  `valor_canonico`.
- **F26 gana la única frase que puede sostener mecánicamente** sobre el orden entre los valores de
  la spec y la exposición del holdout.
- **La sesión 2 (2026-09-13 en adelante) no puede registrarse sin ellos**: la guardia los exige, y
  la plantilla de `knowledge/feedback/README.md` los lleva.
- **Un hueco conocido y declarado**: un registro de una sesión ANTERIOR al corte escrito hoy sigue
  pudiendo omitir `recibido_el`, y eso ya ha pasado una vez —el cierre de A-14, escrito el 12 y
  fechado el 9—. `feedback new` avisa cuando ocurre; no falla, porque hacerlo fallar obligaría a
  rellenar a mano registros históricos cuya fecha de llegada nadie recuerda.

## Alternativas consideradas

1. **Opcionales en el esquema, obligatorios por guardia desde una fecha de corte** (elegida).
2. **Obligatorios en el esquema desde ya.**
3. **Rellenarlos en los 117 registros existentes.**
4. **No añadirlos: dejarlo en las notas de cada registro.**

## Por que elegimos esta opcion

Porque es la única que tiene los campos sin romper nada, y está **medido sobre los 117 reales**:

- si son **opcionales**, **0 de 117 ids cambian**;
- si son **obligatorios en el esquema**, **117 de 117 DEJAN DE CARGAR**, porque `_validar` revienta
  antes de calcular el hash. No es que "les cambie el id": es que el corpus entero deja de existir;
- si se **rellenan**, el id SÍ se mueve —el campo entra en `contenido_canonico`— y eso significa
  renombrar 117 ficheros que el hook de pre-commit y `test_feedback_history` declaran inmutables.

La fecha de corte es lo que convierte "opcional" en "opcional solo hacia atrás": desde la sesión
del 2026-09-13 la guardia los exige, así que la laxitud no se hereda.

## Por que descartamos las demas

- **(2) Obligatorios ya**: mataría el corpus. Está medido arriba.
- **(3) Rellenarlos**: viola el régimen de cambio de `knowledge/feedback/` (SOLO AÑADIR, ADR-0001)
  y, peor, inventaría un dato: nadie puede saber hoy a qué hora exacta llegó cada una de las 117
  respuestas de una sesión de dos horas y media.
- **(4) Dejarlo en las notas**: es donde estaba, y por eso hizo falta este ADR. Una nota no se
  puede consultar mecánicamente, no la valida ninguna guardia y F26 no la puede citar como prueba.
  El proyecto ya tiene un caso idéntico y caro: el aviso de RN-021 sobre las noticias vivió tres
  días en un campo de notas que ninguna guardia miraba (ADR-0022).

## Fecha / fase

2026-09-12, F13. Escrito en la auditoría de cierre: el brief prometía este ADR en su §5 y la
implementación se había hecho sin él, con la regla viviendo en el código, el README y el Change
Log. El precedente que lo exige es `valor_canonico`, el campo opcional análogo de F11, que sí
tiene ADR (ADR-0012 §7).

## Estado

ACTIVE
