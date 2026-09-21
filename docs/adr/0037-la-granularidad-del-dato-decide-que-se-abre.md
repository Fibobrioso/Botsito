---
status: ACTIVE
date: 2026-09-21
phase: post-F13 (abre F14a: la ingesta del detalle por operación)
---

# 0037 · La granularidad del dato decide qué se abre, no el tipo de fichero

## Decision

1. **El criterio es la granularidad del dato.** Lo que se puede atribuir a un día se abre para ese
   día, si ese día no está en una partición reservada. **Lo que AGREGA sobre un rango que incluye
   días reservados no se abre nunca**, ni siquiera para mirar un día: el agregado lleva los
   reservados dentro y no se puede trocear, así que mirarlo **es** leer una cifra que los contiene.

2. **Esto no cambia ni una palabra de ADR-0021 §1**, que ya era granular por día desde el
   2026-09-12: *«el detalle por operación del backtest del trader **en esos días**»*. Ni de
   ADR-0025 §4, que lo aplicó a mayo: *«se puede abrir para esos 6 días `dev`, y solo para ellos»*.
   Lo que no existía en ninguna parte, y es lo que este ADR añade, son **dos reglas**: la de un
   fichero que **mezcla granularidades** —filas atribuibles a un día y agregados que no se
   trocean, en el mismo libro— y la de **leer estructura sin leer valores**.

3. **Lo que se VE y lo que se LEE A PROPÓSITO son cosas distintas, y las gobiernan documentos
   distintos.** ADR-0021 §2 sigue vigente y gobierna **lo que se ve**: una exposición humana y
   accidental —ver un resultado agregado— no abre, pero es exposición y se declara. Este ADR
   gobierna **lo que se lee a propósito**: una ingesta mecánica **no lee un agregado nunca**, y
   **ninguna autorización lo abre**, porque no hay pregunta que pueda responderse sobre él sin
   contener días reservados.

4. **Este ADR NO reclasifica ninguna exposición ya declarada.** Las filas del 2026-09-11, del
   2026-09-12 y del 2026-09-13 de `docs/validation/HOLDOUT-EXPOSICIONES.md` siguen siendo
   exactamente lo que su fila dice, con su veredicto. Un ADR nuevo que cambiara la clasificación de
   exposiciones ya declaradas sería una enmienda retroactiva, y no es lo que se está haciendo.

5. **La estructura se VERIFICA, no se lee.** Contra un fichero que contenga días reservados, la
   lista de pestañas y de cabeceras esperadas **se escribe antes**, y el lector devuelve un
   booleano y, como mucho, **las esperadas que faltan**. Nunca devuelve, imprime ni registra el
   conjunto **encontrado**. La pestaña se selecciona por la lista pre-declarada; no se enumera.

   El motivo es que la asimetría no se puede resolver de otro modo: una cabecera que es un **nombre
   de campo** (`initialSL`) no es atribuible a ningún día —es la misma cadena para las 68 filas— y
   no abre ni expone; una cabecera que es un **valor** (`04-may`, `Totales mayo`) **es** el dato. Y
   para saber cuál de las dos es, habría que haberla leído. Mismo patrón que `preregistro_blob`
   —compara sin mostrar— y que `cobertura_material` —tramos y nunca días, rechazado por la forma—.

6. **Y tampoco se expone el conjunto de FECHAS encontradas**, ni en un retorno, ni en un aviso, ni
   en una línea de log. El lector **recibe** los días que quiere y devuelve sus filas; nunca dice
   qué días hay en el fichero. Un `«14 días en el libro»` publica qué días reservados **no** operó
   el trader, y un día laborable sin ninguna operación **es su etiqueta** —está medido: por eso
   `2026-05-14` quedó quemado el 2026-09-12—. Hay un test que lo vigila.

7. **El objetivo es `idealTP`, y `maxTP` queda EXCLUIDO por ser un resultado.** Medido sobre agosto
   —material de desarrollo, cero días reservados— el libro tiene **dos familias de columnas**: lo que
   se fija al abrir (`initialSL`, `idealTP`, `entryPrice`) y lo que pasa después (`avg*`, `max*`,
   `rPnL`, `status`, `avgClosePrice`). Dos medidas lo separan:

   - **`maxTP` está relleno si y sólo si la operación ganó**: 20 filas con `maxTP`, las 20 con
     `rPnL > 0`; 27 sin `maxTP`, **ninguna** con `rPnL > 0` (22 en pérdida, 5 a cero). Un objetivo
     *planeado* no puede faltar precisamente cuando la operación pierde. `maxTP` es «lo más lejos
     que llegó a favor»: un resultado.
   - **`idealTP` está en 47 de 47.** Se fija al abrir.

   Las columnas de RR se calculan desde `maxTP` (18/18 cuadran redondeando a dos decimales) y no
   desde `idealTP` (3 de 42), lo cual **no** convierte a `maxTP` en el objetivo: confirma que las
   columnas de RR son también métricas de resultado, de la misma familia.

   **El objetivo no se reconstruye por RR** en ningún caso: fabricaría un número que el trader no
   escribió, y este proyecto no inventa una elección que el trader no ha hecho —es la misma regla
   por la que A-24 sigue abierta—. (El motivo mecánico que se había supuesto para descartarlo —que
   `avgRiskReward` fuera un promedio agregado repetido por fila— resultó **falso**: tiene 16 valores
   distintos en 42 filas, y `maxRiskReward` 15 en 47. Es por operación. El motivo de fondo basta.)

   > **CORRECCIÓN del 2026-09-21 (mismo día, commit `a791f92` arriba).** El cuerpo de esta
   > decisión **afirmaba que el objetivo es `idealTP`, y es falso**. Se midió después, al probar el
   > lector, y lo cazó el invariante geométrico —que estaba puesto como test permanente de higiene,
   > no como discriminador—:
   >
   > ```
   > idealTP:   del lado correcto 43, del lado MALO 4, sin valor 0
   > maxTP:     del lado correcto 20, del lado MALO 0, sin valor 27
   > initialSL: del lado correcto 42, del lado MALO 0, sin valor 5
   > ```
   >
   > **Ninguna de las dos columnas es el objetivo planeado.** `maxTP` se cae por estar relleno sólo
   > cuando se gana; `idealTP` se cae porque en 4 de 47 filas está **del lado de la pérdida** —entre
   > la entrada y el stop, las cuatro `sell` perdedoras—, y su RR implícito no tiene estructura
   > (0,2 · 0,1 · −0,2 · 2,1 · 1,1 · 56,6).
   >
   > **Lo que sí es el objetivo, y lo contestó el corpus:** una REGLA, no una columna. El trader
   > dice en cámara *«el ratio de riesgo-beneficio de 1 a 3»* como mínimo
   > (`ev-v2-001658-d02fb71a`, v2 0:16:58) y *«como objetivo fijo»* (v1 0:04:14), y la spec ya lo
   > tiene como `objetivo_rr` con su `base_calculo_objetivo`. **El xlsx simplemente no registra el
   > objetivo planeado.**
   >
   > Y hay huella mecánica de la regla dentro del propio fichero, independiente de la cita: el RR
   > implícito de `maxTP` tiene **suelo en 3,00** —17 de 18 filas en 3,00 o por encima, tres
   > clavadas en 3,00, con un único 2,50—, que es lo que se ve si la salida ocurre en 3R. Y que 15
   > de 18 **se pasen** de 3,00 es evidencia de que el TP **no** es una orden límite colocada en
   > 3R exacto: una orden límite habría cerrado ahí y el recorrido máximo no podría superarlo.
   >
   > **Consecuencia para F26, corregida.** F26 **sí** puede puntuar el objetivo, comparando el del
   > bot contra la REGLA —`entrada ± objetivo_rr × base_calculo_objetivo`—. Lo que **no** puede es
   > verificar que en una operación concreta el trader colocara ese TP, porque el fichero no lo
   > guarda. (Antes de esta corrección se escribieron **dos** consecuencias para F26 sin medir la
   > cadena, y las dos eran falsas en direcciones opuestas: «el objetivo falta en la mayoría de
   > unidades» y «no se puede puntuar en absoluto». La regla que sale: una consecuencia para F26 es
   > una afirmación como cualquier otra y no se escribe sin medir la cadena entera hasta ella.)
   >
   > **Por eso el caso NO lleva campo `objetivo`**, y no es que lo lleve vacío: un campo opcional
   > vacío es una invitación a que dentro de seis meses alguien lo rellene con `maxTP`. Quitar el
   > campo **es** el mecanismo; un comentario no lo es. El caso lleva cuatro cosas: instante de
   > apertura, dirección, entrada y stop.
   >
   > **Y `idealTP` no se guarda** en el caso, con motivo medido: no sabemos qué es. Queda anotado
   > como deuda —*columna del material que no sabemos qué es y no usamos*— y no se le gasta al
   > trader una pregunta por ella.

8. **El instante de apertura viene en UTC, y esa es la medida que sostiene la asignación a sesión
   H4.** `dateStart` es texto sin huso (`2026/08/03 06:03:05`). Interpretado como UTC y llevado a
   `huso_operativa`, **las 47 operaciones de agosto caen dentro de las dos sesiones declaradas**
   (25 en `07-11`, 22 en `11-15`, cero fuera); interpretado como hora local de Madrid, 16 de 47
   quedarían fuera de toda sesión. La ingesta convierte desde UTC, y lo declara.

8b. **Dos propiedades medidas del material, que no se corrigen ni se descartan.** Van escritas
   porque van a reaparecer en mayo y en septiembre y alguien va a tropezar con ellas:

   - **4 de 47 filas de agosto tienen `idealTP` entre la entrada y el stop**, las cuatro `sell` en
     pérdida. No es un error del fichero: es cómo viene.
   - **5 de 47 filas no tienen `initialSL`.** Una fila sin stop **no produce caso**, y no se cae en
     silencio: se cuenta y se dice, con su motivo, en la salida del comando. Un caso que desaparece
     sin constancia es el defecto que a la sesión 1 le costó dos días —`2026-05-25` y
     `2026-06-29`— y que sólo delata un contador.

   Y el **invariante geométrico** queda como guardia permanente, no como comprobación de una vez:
   para `buy`, `initialSL` por debajo de `entryPrice`; para `sell`, por encima. Cualquier fila que
   lo viole **aborta la ingesta nombrando la fila**. Caza para siempre un intercambio de columnas,
   que es el fallo silencioso que más caro sale aquí —y es el que cazó lo de `idealTP`—.

9. **`knowledge/cases/dev/` es un camino con PRECIOS, y ésa es su novedad.** Un `caso-*.yaml` lleva
   entrada y stop: es la primera vez que este repositorio pone precios bajo `knowledge/cases/`. El
   disparador que ADR-0033 dejó escrito —*«el día que exista bajo `knowledge/cases/<camino>/` un
   fichero con una etiqueta, un PRECIO o el detalle por operación de un día asignado a una partición
   reservada, ese camino necesita lector guardado antes de que ese fichero se commitee»*— **no se
   cumple hoy**, porque sólo hay días `dev`. Lo que no existía es el mecanismo que garantice que
   siga sin cumplirse mañana, y entra aquí:

   - la ingesta **se niega** a escribir un caso cuyo día esté en `casos_reservados`, con la
     comprobación escrita y no por convenio;
   - **un test de contrato** afirma que ningún fichero bajo `knowledge/cases/dev/` corresponde a un
     caso reservado, y se rompe si alguien deja uno ahí, hoy o dentro de un año.

10. **Material de DESARROLLO**: enero, abril y agosto de 2026 no son holdout —la spec se infirió en
   parte de esos días, así que medir fidelidad sobre ellos sería circular— y se abren **sin puerta**.
   Que no tienen ni un día en ninguna partición **se comprueba antes de abrir** con
   `casos_reservados(repo)`, no se supone. Y se declara igual el mismo día: no porque sea exposición,
   sino porque dentro de seis meses alguien verá que se abrió y va a querer el motivo.

## Problema que resuelve

`CLAUDE.md` §3 prohibía «el detalle por operación de los xlsx del corpus» **en bloque, sin distinguir
días**, mientras que los dos documentos que mandan ya eran granulares por día. Tomado al pie de la
letra, prohibía F14a entera: la ingesta del detalle de los días `dev`, que es el paso que el proceso
exige. **Tercera vez que este fichero resulta ser más estricto que ADR-0021 sin que ningún ADR lo
diga**, y las dos anteriores también bloquearon un paso necesario.

Pero relajar el saco entero habría sido cambiar un problema por una fuga: se abriría un resumen del
mes con los 10 días de `fidelidad-1` dentro. De ahí el criterio de la granularidad, que da
resultados **opuestos dentro del mismo fichero** —las filas de un día `dev` se leen; la pestaña de
totales no, aunque esté al lado— y que por eso es el criterio correcto y no una excusa.

## Alternativas consideradas

1. Mantener la prohibición en bloque y no hacer F14a.
2. Relajar la prohibición por fichero: «el xlsx se abre».
3. Enmendar ADR-0021 en vez de escribir un ADR nuevo.
4. Reconstruir el objetivo por RR cuando falte.
5. Tomar `maxTP` como objetivo, que es lo que su nombre sugiere.

## Por que elegimos esta opcion

**Por granularidad y no por fichero** porque es lo único que distingue lo que de verdad contamina de
lo que no, y porque **ya estaba decidido**: ADR-0021 §1 dice «en esos días» desde el principio. Este
ADR no inventa el criterio; lo nombra, lo extiende al caso que faltaba —el fichero mixto— y le da
mecanismo.

**ADR nuevo y no enmienda** por el precedente exacto del propio repositorio: **ADR-0033 nació nuevo
y le dio mecanismo a ADR-0021 §3**, dejando en ADR-0021 una nota que apunta a él. Aquí pasa lo
mismo con §1. Y además es asunto adyacente: la regla del fichero mixto y la de la estructura no
existían en ninguna parte. El criterio que se lee del repositorio es *enmienda cuando cambia la
misma pieza sobre el mismo asunto; ADR nuevo cuando se da mecanismo o se decide un asunto adyacente
que el viejo sólo señalaba*.

**El objetivo no se reconstruye** porque fabricar un número que el trader no escribió es exactamente
lo que este proyecto no hace.

## Por que descartamos las demas

- **(1) No hacer F14a**: F14 lleva desde el MASTER_PLAN dependiendo de la ingesta, y la prohibición
  que lo impedía no sale de ningún ADR.
- **(2) Relajar por fichero**: abre el agregado del mes con `fidelidad-1` dentro. Es la fuga que
  esta rama podría haber creado, y el motivo de que el criterio sea la granularidad.
- **(3) Enmendar ADR-0021**: no cambia ni una palabra suya, y escribir aquí «el agregado no se ve
  nunca» **contradiría su §2**, que está vivo y dice que ver un agregado no abre, es exposición y se
  declara. Habría convertido esto en una enmienda retroactiva sobre tres filas ya declaradas. La
  distinción de la decisión 3 es lo que lo evita.
- **(4) Reconstruir el objetivo**: por el motivo de fondo. El motivo mecánico que se había supuesto
  —que `avgRiskReward` fuera un agregado— se midió y es **falso**; no hacía falta.
- **(5) `maxTP` como objetivo**: se consideró, y se cae con la medida de la decisión 7. Su presencia
  correlaciona perfectamente con que la operación ganara, así que es un resultado y no una decisión
  del trader. Meterlo habría puesto un resultado dentro de la forma del caso, que es exactamente lo
  que la lista corta de columnas existe para evitar.

## Impacto

- **`CLAUDE.md` §3 reescrito** para decir lo que dice este ADR y ni una palabra más, con la caja de
  «por qué cambió esta regla, tercera vez».
- **ADR-0021 lleva una nota** que apunta aquí, igual que la que apunta a ADR-0033.
- La ingesta de F14a puede leer las filas de los días `dev` de mayo y de septiembre **sin puerta**, y
  se niega sobre cualquier día reservado **nombrando su partición**.
- **`docs/validation/SEPTIEMBRE-ENTRA.md`** apoyaba en que «las dependencias del proyecto son sólo
  `pyyaml` y `tzdata`» el argumento de que ninguna ruta de código podía leer el libro. **Ese refuerzo
  muere con F14a** —un lector de stdlib también lee— y su sustituto entra en el mismo commit: un
  contrato por grep, *un solo módulo de `src/` puede nombrar el xlsx*.
- La guarda de tests se extiende a `corpus/`: hoy nada impide que un test abra el xlsx de mayo.
- **No cierra**: el alcance de `excluir` en `kappa_entre_sesiones` (bloqueante para firmar, ADR-0033
  enmendado), ni `EXPOSICIONES` sin mecanismo, ni el `no_trade` por ausencia, que se declara como
  inferencia nuestra (ADR-0016) y no como dato del trader.

## Fecha / fase

2026-09-21, post-F13, rama `feature/F14a-ingesta-del-detalle`. Informe:
`docs/validation/F14A-INGESTA.md`.

## Estado

ACTIVE
