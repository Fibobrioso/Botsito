# Sesión 02: los candidatos C-xx en las transcripciones, criterio congelado antes de buscar

Rama `trabajo/sesion-02`, 2026-09-25. Sin merge, sin tag y sin push.

Este documento y la lista `TERMINOS_SESION02` de `scripts/buscar_ambiguedades.py` se commitean
juntos y **antes** de ejecutar la búsqueda. El script es la implementación exacta de este
documento: cambiarlo después de ver la salida es cambiar el criterio.

Es el **mismo método que A-24 y A-35** (`A24-A21-A26-A34-CRITERIO.md`,
`A35-PIVOTE-FORMADO-CRITERIO.md`): misma normalización, misma ventana y mismo corte. Los candidatos
van en un conjunto aparte (`--conjunto sesion02`). Regeneradas fuera del repositorio con el script
ya modificado, las salidas de A-18, de A-24/A-21/A-26/A-34 y de A-35 salen **idénticas byte a
byte** a las commiteadas (`cmp` sin diferencias). El conjunto lleva test propio
(`tests/unit/test_buscar_sesion02.py`).

## 0. El alcance

Las mismas cinco transcripciones vigentes de v1 a v5; solo la cruda, verificada contra el
`sha256_cruda` de su manifiesto. Quedan fuera v6 -su día está retirado (ADR-0041)- y las heredadas
y las sustituidas. No se abre nada más del corpus, ni ningún fotograma.

## 1. Los candidatos que se buscan, y por qué estos

Los huecos de `SESION-02-INVENTARIO.md` §4.3 en orden causal del motor, a partir de RN-005. Seis de
ocho:

- **Se buscan:** C-01, C-02, C-04, C-05, C-06 y C-07.
- **No se buscan:** C-03 (el lado del libro que dibuja FX Replay es una propiedad de la plataforma:
  se mide, no lo dice el trader), C-08 (la unidad de F26 la decide el consultor) y A-18 (su
  búsqueda ya se hizo: 0 de 42).

Para todos, la **hipótesis es ABIERTA**: no hay una respuesta que se espere confirmar.

## 2. Por candidato: la pregunta, los términos y qué responde

Los términos son frases o combinaciones de dos o más palabras. Queda prohibida cualquier palabra
suelta de uso constante (liquidez, zona, M15, H4, sesgo, vela, pivote), y un test lo comprueba. La
búsqueda no distingue mayúsculas ni tildes, y casa por palabra o por frase: una cifra no casa dentro
de otra («nivel 1» no casa con «nivel 10», con test).

### C-01 · El precio de la orden límite dentro de la zona

- **Pregunta:** ¿a qué precio exacto, dentro de la zona de control, se pone la orden límite?
- **Términos:** orden limit · orden límite · mi orden · la orden limit · pongo la orden · coloco la
  orden · marco mi orden · poner la orden · colocar la orden · precio de entrada · punto de entrada
  · bloque de origen · origen del breaker · order block · mitad de la zona · cincuenta por ciento ·
  50 por ciento
- **RESPONDE:** enuncia en general en qué punto de la zona (o del bloque) va el precio de la orden.
- **DUDA:** lo muestra en un ejemplo o con deícticos («aquí», «esta») que solo resuelve el gráfico,
  o dice en qué zona va pero no en qué precio.
- **NO RESPONDE:** habla de cuándo se pone la orden (A-29), del stop o del objetivo.

### C-02 · El extremo de la caja, del que sale el stop

- **Pregunta:** ¿qué punto del mercado marca el extremo de la caja, del que sale el stop?
- **Términos:** punto más abajo · punto más bajo · punto más arriba · punto más alto · caja de gann ·
  cuadro de gann · nivel cero · nivel uno · nivel 0 · nivel 1 · desde aquí hasta · de aquí hasta
  aquí · de aquí a aquí · extremo de la caja · mi stop · el stop va · pongo el stop · defino el stop
  · definir el stop
- **RESPONDE:** enuncia en general qué punto (qué vela, qué extremo, de qué temporalidad) marca el
  borde de la caja o el origen del stop.
- **DUDA:** lo hace sobre un ejemplo o con deícticos; o dice dónde va el stop respecto a la caja
  (eso es A-18) sin decir de dónde sale la caja.
- **NO RESPONDE:** habla de la fracción de la caja (0,8, A-10), del lote o del objetivo.

### C-04 · La orden pendiente que el precio deja sin llenar

- **Pregunta:** ¿qué pasa con una orden límite pendiente si el precio se aleja sin llenarla antes
  del fin de la ventana?
- **Términos:** no se llenó · no se llena · no me llenó · no se activó · no se activa · no me activó ·
  no me activa · se fue sin · se va sin · se me fue · sin activar · sin activarse · no entró · no me
  entró · cancelo la orden · cancelar la orden · quito la orden · quitar la orden · borro la orden ·
  elimino la orden
- **RESPONDE:** enuncia en general qué hace con una orden que no se llena y el precio se va:
  cancelarla, dejarla, moverla, y cuándo.
- **DUDA:** lo cuenta de una operación concreta, sin regla.
- **NO RESPONDE:** habla de una orden que sí se llenó, o del fin de la ventana (eso es A-30).

### C-05 · Lo que viene de una sesión cuando empieza la otra con otro sesgo

- **Pregunta:** ¿qué pasa con una orden pendiente o una posición viva cuando empieza la otra sesión
  H4 con un sesgo distinto?
- **Términos:** siguiente sesión · otra sesión · nueva sesión · cambio de sesión · segunda sesión · a
  las once · de 11 a 15 · de once a · nueva vela de 4 · nueva vela de cuatro · cambia el sesgo ·
  cambió el sesgo · sigue abierta · sigo dentro · la dejo abierta · queda abierta
- **RESPONDE:** enuncia en general qué hace con lo pendiente o lo abierto al cambiar de sesión, o
  cuando la nueva H4 cambia el sesgo.
- **DUDA:** lo cuenta de un caso concreto, o habla del cambio de sesión sin decir qué pasa con la
  orden o la posición.
- **NO RESPONDE:** habla del sesgo al empezar el día (RN-003), o del cierre de las 15:00 (RN-002).

### C-06 · El stop después del break even

- **Pregunta:** después del break even, ¿el stop vuelve a moverse?
- **Términos:** muevo el stop · mover el stop · subo el stop · bajo el stop · subir el stop · bajar
  el stop · trailing stop · arrastrar el stop · arrastro el stop · voy moviendo el stop · asegurar
  ganancias · asegurar beneficio · después del break even · luego del break even · ya en break even
- **RESPONDE:** enuncia en general si, una vez en break even, el stop se queda o se sigue moviendo,
  y con qué criterio.
- **DUDA:** lo muestra en una operación concreta.
- **NO RESPONDE:** habla de cuándo se pone el break even (RN-014, A-13) o del stop inicial.

### C-07 · El tope de entradas por día

- **Pregunta:** ¿hay un tope de entradas por día, además de los cartuchos por liquidez?
- **Términos:** dos entradas · tres entradas · dos operaciones · tres operaciones · una operación al
  día · una entrada al día · máximo de operaciones · máximo de entradas · como máximo · ya no opero ·
  dejo de operar · cierro el día · se acabó el día · por día · al día
- **RESPONDE:** enuncia en general un máximo de entradas u operaciones por día, o que no lo hay.
- **DUDA:** da un máximo que puede ser por liquidez o por zona (los cartuchos) y no por día; o lo
  dice de un día concreto.
- **NO RESPONDE:** habla del tope porcentual (RN-020) o de cuántas operaciones hizo sin enunciar
  regla.

**Para todos:** si la respuesta depende de un gráfico, se anota el fotograma más cercano
(`botsito corpus frames show`) y si ya estaba medido o citado; **no se abre ninguno** (ADR-0038).
Para la regla global, **una DUDA no responde**.

## 3. La regla global

**Si hay pasajes que RESPONDEN en sentidos opuestos, o ninguno responde, se pregunta al trader.** La
aplica el consultor, no esta rama.

## 4. La ventana y el corte

Los mismos que en A-24 y A-35:
- **ventana** de ±45 s alrededor de cada coincidencia, uniendo las que se solapan;
- **corte:** un pasaje mide como mucho **180 s**; una unión más larga se corta en pasajes
  consecutivos contados desde su inicio;
- **cada trozo** lista sus propias coincidencias, y un trozo sin coincidencias propias no se emite.

Se busca por separado para cada candidato, así que un mismo tramo puede salir en más de uno.

## 5. El control positivo

Tienen que aparecer en la salida, y un test comprueba que casan con la lista:
- **C-01:** la cita de `colocar_orden_limite` en la spec, «marco mi orden limit»
  (`ev-v3-004201-bfeb3734`);
- **C-02:** v1 #192, «Desde el punto más abajo te genera la vela contraria» (la frase de
  `ev-v1-001454-69cebe62`);
- **C-07:** «en un día como máximo dos entradas» (`ev-v4-003350-acb03ee7`).

**Si falta alguna, se para.** C-04, C-05 y C-06 **no tienen control positivo conocido**: no hay
en el repositorio ninguna frase del corpus que se sepa que les responde, y por eso sus términos
son la única garantía de alcance. Se dice aquí para que un cero en ellos no se lea como más de lo
que es.

## 6. La salida y la clasificación

- **Una sola ejecución**, con la salida tal cual en `SESION-02-BUSQUEDA-SALIDA.txt`, en su propio
  commit.
- **Después, la clasificación**, en su propio commit: por pasaje, su clase, la frase literal
  comprobada por script contra la salida, la referencia de vídeo y de segmento, y el fotograma
  cuando dependa de un gráfico. **Sin aplicar la regla global.**

## Estado

CRITERIO CONGELADO. La búsqueda no se ha ejecutado.
