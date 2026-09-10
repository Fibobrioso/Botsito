---
status: ACTIVE
date: 2026-09-10
phase: F12
---

# 0018 · La precedencia va por clase, no por orden del fichero; y los siete defectos que eso destapó

## Decision

1. **Campo `clase` obligatorio en cada regla**, de conjunto cerrado y con precedencia fija:
   `gate` > `disparador` > `terminal` > `fallback`. Una prohibición gana siempre a un permiso.
2. **El orden del fichero deja de tener semántica.** Es editorial y se queda así.
3. **`clase` entra en el hash**: decide qué regla gana, o sea lo que el bot hace.
4. **`stop_segundo_esquema` pasa a UNKNOWN a propósito.** Hay un único esquema de stop.
5. **La ventana es medio abierta**: `[ventana_inicio, ventana_fin)`. A las 15:00 ya no se abre.
6. **Dos cardinalidades salen de la prosa al registro**: `operaciones_simultaneas_max` (1,
   CONFIRMED) y `zonas_control_max_por_esquema` (1, DEFAULT_AMBIGUOUS bajo A-20).
7. **`dias_operables` pasa de `texto` a `enum`.**
8. **La guardia de cifras deja de exceptuar los sustantivos de dominio** (`zonas`, `esquemas`,
   `operaciones`).

## Problema que resuelve

La revisión de diseño de F12 (tres agentes, 2026-09-10) no encontró un problema de F12: encontró
**siete defectos vivos en la spec recién validada**, dos de ellos capaces de costar dinero.

**El más caro.** RN-006 decía `cuando: el precio rompe el extremo anterior y completa una zona de
control`, **sin precondición de que la orden siguiera pendiente**. RN-014 se dispara sobre EL MISMO
evento, distinguido solo por si hay posición abierta. Entrada llena a las 09:12, zona nueva completada
a las 09:20: con orden de fichero, RN-006 (006) gana a RN-014 (014) y a RN-018 (018), así que el bot
**reubica una orden límite con una operación abierta** —lo que RN-018 prohíbe— **y no pone el break
even**. Se pierde la protección y se abre una segunda exposición.

**El segundo.** RN-019 (reentrada tras equal) es id 019 y RN-020 (tope del 4,5 %) es id 020: en orden
de fichero **se reentra después de haber tocado el tope diario**. En cuenta fondeada eso no cuesta un
trade.

Y cinco más: a las 15:00:00 se cumplían RN-001 (*"busca entradas"*) y RN-002 (*"cierra a mercado"*) a
la vez; `stop_fraccion_caja` y `stop_segundo_esquema` valían ambos `0.8` —dos puertas para el mismo
número, que RN-012 prohíbe expresamente—; RN-009 y RN-018 llevaban cardinalidades de negocio en prosa
**con la guardia escrita para no verlas** (su comentario declaraba que *"se abre una operacion"* y
*"los dos esquemas"* pasaban); `dias_operables` era `texto` con valor `"lunes a viernes"` usado como
condición ejecutable; y RN-002 nombraba *"la hora del gráfico"* mientras sus `parametros` decían
`huso_operativa` —resto de ADR-0017 sin terminar—.

## Alternativas consideradas

- **A. Orden del fichero** como precedencia.
- **B. `prioridad: <entero>`** por regla.
- **C. Dejar la precedencia al motor** (F22), sin declararla en la spec.
- **D. Borrar `stop_segundo_esquema`** en vez de dejarlo UNKNOWN.

## Por que elegimos esta opcion

Porque **la clase dice el porqué y el entero no**. Seis reglas vigentes son prohibiciones puras y una
es el freno del día: "una prohibición gana a un permiso" es una frase que un humano verifica de un
vistazo, y resuelve los tres pares rotos sin tocar ninguna regla más.

Y porque hace la coherencia **mecanizable**: dos reglas de la misma clase con exactamente los mismos
parámetros son ahora un error de `knowledge validate` con los dos ids en el mensaje, que es
literalmente el criterio que MASTER_PLAN pide de F12 (*"falla nombrando el id"*).

## Por que descartamos las demas

- **A**: demostrablemente mal en tres pares, y en dos direcciones a la vez —hay *gates* que llegan
  tarde y un `else` que llega pronto—. Peor: el orden **es editorial**; RN-026 y RN-027 son VIGENTES
  y viven bajo la cabecera `# ---- reglas descartadas`. Adoptarlo convertiría un reagrupamiento
  cosmético en un cambio de comportamiento que el hash sí vería y nadie sabría leer.
- **B**: 24 enteros a mano se pudren en la primera regla nueva, y no dicen por qué.
- **C**: es la deuda del §8 de F11 otra vez —el motor decidiendo lo que la spec calla— y F26 mediría
  fidelidad contra una precedencia que no está escrita en ninguna parte.
- **D**: probado y revertido en F11 con `stop_colchon_spread` (ADR-0012, alternativa D): al borrar un
  parámetro, su registro de feedback queda apuntando al vacío y el sistema se niega, con razón.
  `UNKNOWN` a propósito conserva la pregunta y su respuesta.

## Que sustituye de otros ADR

- **Amplía ADR-0013** (esquema de regla y alcance del hash) con `clase`, igual que ADR-0016 lo amplió
  con `titulo`, `literal`, `notas` y `decision`.
- **Termina ADR-0017**: RN-002 seguía nombrando el reloj del gráfico en su prosa.
- **Cierra el comentario de `spec/modelo.py`** que declaraba como español lo que eran dos
  cardinalidades de negocio.

## Impacto

- `spec_version` **3.0.1 -> 4.0.0**. RN-006, RN-009, RN-013 y RN-018 cambian de sentido, y la
  precedencia entre todas ellas pasa a estar declarada: es otro comportamiento.
- El registro pasa a **56 parámetros**. `stop_segundo_esquema` se suma a los UNKNOWN a propósito.
- **A-20 nueva**: el literal de RN-009 dice *"por lo general sólo buscamos uno"*, que no es una
  prohibición dura. `zonas_control_max_por_esquema` corre con un default nuestro hasta que el trader
  diga si es regla o tendencia.
- La guardia de cifras es más estricta y **obliga a redactar con precisión**: `una zona` ya no pasa,
  así que hay que escribir `la zona de control en curso` o nombrar el parámetro. Es el efecto
  buscado.
- **Queda para F12**, no aquí: la forma ejecutable de las reglas. Este ADR arregla la spec que se va
  a formalizar; formalizarla con estos siete defectos dentro los habría horneado.

## Fecha / fase

2026-09-10, F12 (revisión de diseño, antes de programar la forma).

## Estado

ACTIVE
