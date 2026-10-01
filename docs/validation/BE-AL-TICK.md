# El break even de RN-014 al tick

Rama `feature/be-al-tick`, desde `main` en `2fff834`, el 2026-09-30. Es el Next Action G. El encargo
tiene dos partes:
1. RN-014 pone el break even en el primer tick que toca el nivel de activación, no al cierre de la
   M1: mismo nivel, misma entrada exacta, y solo cambia el instante.
2. Redirigir el registro S-1 de RN-033 a RN-003.

**La parte 1 está hecha y medida. La parte 2 está PARADA**: una guardia la rechaza (§3).

## 1. Lo que cambia

Las decisiones están en **ADR-0065** (ACTIVE y PROVISIONAL, a revisar con la demo de MetaTrader).
Fuente: `fb-2026-09-29-sesion-03-9f506366` («apenas toca, pues se pone en B la entrada») y
`ev-v6-005701-7ae2b8d3`.

- **El nivel.** En cada cierre de M1, con la posición abierta, el predicado de RN-014 calcula el
  nivel vigente. Es el mismo punto de `zona_posterior_completada`, sacado del mismo recorrido
  (`nivel_de_activacion_posterior`). El predicado lo deja en el contexto sin tocar el bróker.
- **El instante.** El cableado lo vigila en el bróker si `break_even_condicion` es `tocar`, que es
  el valor CONFIRMED. El stop pasa a la entrada exacta en el primer tick cuyo BID pasa el nivel:
  la mecha de una M1 BID vista tick a tick.
- **El contador.** Mover el stop es una petición `modificar` de R13, en el instante del tick.
  Vigilar no es una petición. Si RN-014 lo vuelve a pedir al cierre de esa M1, el stop ya está en
  la entrada y el bróker no hace nada: ni petición ni evento.
- **Desempates en el mismo tick.** Primero lo que el servidor hace con lo que ya hay (llenar, saltar
  el stop vigente o el objetivo) y después mover el stop. El stop nuevo cuenta desde el tick
  siguiente.
- **Lo que se queda al cierre de la M1, y la traza lo marca.** Sin ticks (`--depuracion`), con
  `cierre` o con el criterio `cuerpo`, el stop se mueve al cierre de la M1. El evento nuevo
  `stop_movido` lleva la fuente `respaldo_m1` sin ticks y `cierre_m1` con ticks. El respaldo M1
  sigue siendo pesimista: una M1 que pasa el nivel y toca el stop original sale por el stop.
- **La spec.** La nota de RN-014 decía que el motor movía el stop «en el cierre de la M1 que toca
  el punto, no en el tick»; ahora dice lo que hace. La spec pasa a 15.2.1. **Ningún valor ni
  ninguna forma cambia.**

**Tests** (`tests/unit/test_be_al_tick.py`, nuevo, 7 funciones y 8 casos):
- un tick que pasa el nivel y vuelve dentro de la misma M1: antes salía por el stop entero y ahora
  sale por break even;
- el paso del stop es una petición y el cierre de la M1 no la repite;
- sin ticks, el respaldo sigue siendo pesimista y la traza lo marca;
- los desempates en el mismo tick;
- el nivel vigilado es el mismo punto que completa la zona;
- de punta a punta por el motor, con `tocar` y con `cierre`;
- la fuente `cierre_m1`.

**Test que cambia a propósito:**
`test_cableado.py::test_rn014_pone_el_stop_en_la_entrada_al_completarse_la_zona_posterior`. Su
traza lleva ahora `stop_movido` al tick (a los 40 s de la M1) entre el llenado y el stop.

## 2. Lo medido (en DIAGNÓSTICO, solo construcción)

> **No es fidelidad ni un objetivo.** No se ha ajustado nada para mejorar ninguna cifra.

- **Cómo.** `motor arnes --simular` sobre abril y agosto de 2026 (42 días `dev`, 77 operaciones
  del trader), con A-35 `cierre_vela_contraria`, A-44 `sin_tope`, A-21 `solo_una_zona_de_control`
  y A-27 a 0 puntos. Es la configuración de F35. Se mide con la cuenta arrastrada y con la cuenta
  reiniciada cada día. Cada corrida va en un clon desechable (`git worktree add`), con los datos
  del repositorio. Nada se escribió en el repositorio.
- **Antes:** `main` (`2fff834`).
- **Control:** la rama con `break_even_condicion` en `cierre`. Su informe es **el de `main` línea
  a línea, más las líneas `stop_movido`**, con las dos cuentas. Así se cuentan los break even de
  antes sin suponerlos.
- **Después:** la rama tal cual (`tocar`).

| | antes (`main`) | control (`cierre`) | **después (`tocar`)** |
|---|---|---|---|
| **cuenta arrastrada** | | | |
| cobertura | 2 de 77 | 2 de 77 | **2 de 77** |
| operaciones puntuables del bot | 10 | 10 | **10** |
| llenados del bot | 15 | 15 | 15 |
| **pasan a break even** | 5, al cierre de la M1 | 5, `cierre_m1` | **5, al tick** |
| · tras el break even: stop / objetivo | 4 / 1 | 4 / 1 | 4 / 1 |
| peticiones: total (colocar / modificar / cancelar / cerrar) | 35 (24 / 5 / 6 / 0) | 35 (24 / 5 / 6 / 0) | **36 (24 / 5 / 6 / 1)** |
| **máximo diario de peticiones** (frente a 2000) | 7 (04-07) | 7 (04-07) | **7 (04-07)** |
| saldo final simulado | 90.218,33 | 90.218,33 | 90.422,02 |
| **cuenta diaria** | | | |
| cobertura | 7 de 77 | 7 de 77 | **7 de 77** |
| operaciones puntuables del bot | 30 | 30 | **30** |
| llenados del bot | 36 | 36 | 36 |
| **pasan a break even** | 12, al cierre de la M1 | 12, `cierre_m1` | **12, al tick** |
| · tras el break even: stop / objetivo | 9 / 3 | 9 / 3 | 9 / 3 |
| peticiones: total (modificar) | 102 (12) | 102 (12) | **102 (12)** |
| **máximo diario de peticiones** (frente a 2000) | 7 (08-13) | 7 (08-13) | **7 (08-13)** |

**Lo que dice la medida:**

- **Pasan a break even las mismas posiciones, todas al tick y entre 19 y 60 s antes** que al
  cierre de la M1 (12 de 12 con la cuenta diaria).
- **La cobertura, las operaciones del bot y el máximo diario de peticiones no cambian.** El paso
  del stop sigue siendo una petición por posición: el cierre de la M1 no la repite.
- **Posición a posición, con la cuenta diaria:**
  - las 24 posiciones sin break even cierran igual;
  - de las 12 con break even, 10 cierran igual;
  - **cambian dos**: 04-07 pos-o3, una venta, pasa de 0 a −4 puntos, y 04-29 pos-o2 pasa de −3 a
    −1;
  - la suma de las 12 pasa de 118 a 116 puntos.
  - El volcado posición a posición se sacó con un envoltorio de `informe_simulacion` en la carpeta
    de trabajo; no está en el repositorio.
- **El caso que el cambio arregla no aparece en construcción.** Es una M1 que pasa el nivel y
  vuelve al stop original antes de cerrar. Lo prueba el test, pero ninguna de las 36 posiciones lo
  hace.
- **Lo que hay que mirar, aunque no sea una medida: 04-07 pos-o3.**
  - En una venta, el nivel se mira en el BID, como las velas, y el stop salta por el ASK.
  - Con una caja de 12 puntos, el tick que pasa el nivel deja el ASK cerca de la entrada, y el
    tick siguiente, un segundo después, salta el stop movido 4 puntos más allá.
  - Al cierre de la M1, el mismo break even salía a 0.
  - Es la DECISIÓN de ADR-0065 §1 (BID para el nivel) y su alternativa descartada (el ASK en
    una venta). Se anota para la demo y no se decide aquí.
- **Con la cuenta arrastrada, el saldo cambia por un efecto de camino, no por el break even.**
  - Los −4 puntos del 04-07 bajan el saldo de ese día en 165,40.
  - El 04-22, con el saldo más bajo, la pérdida flotante de pos-o1 cruza antes el límite de la
    firma. RN-030 la cierra a mercado al cierre de su M1, a las 05:16 UTC, en vez de saltar su stop
    9 s después. De ahí la petición `cerrar` de más y el saldo final más alto.

**Holdout intacto.** Solo se leyeron días de construcción, por la compuerta del arnés, como en F35 y
en CAJA-77, que no declararon fila. Ninguna fecha reservada aparece en este informe.

## 3. S-1: PARADO, porque la guardia de feedback lo rechaza

**El encargo** pedía un registro nuevo que sustituya (`supersede`) a S-1
(`fb-2026-09-29-sesion-03-1168f036`, CORRECT sobre RN-033) y lo dirija a RN-003, con la misma cita
literal.

**Lo medido.** Se ensayó en un clon desechable con `botsito feedback new --objetivo-id RN-003
--supersede fb-2026-09-29-sesion-03-1168f036`. Sale esto, con el id del registro rechazado sustituido, porque
ese registro no existe y la guardia de ids citados no admite nombrarlo:

```
ERROR: <id del registro ensayado>: supersede a fb-2026-09-29-sesion-03-1168f036, que trata
de regla:RN-033, no de regla:RN-003; una correccion habla del mismo objetivo
```

La guardia está en `feedback/modelo.py:427`: un registro que sustituye a otro tiene que hablar del
mismo objetivo. **No se ha escrito ningún registro ni se ha tocado la guardia.** Rodearla sería
cambiar lo que vigila, y eso es decisión del consultor.

**Hay un segundo obstáculo, aunque la guardia lo admitiera.** RN-003 ya cita un CORRECT de la
sesión 3 (`fb-2026-09-29-sesion-03-31fb311f`, el color decide la doble ruptura). Una regla tiene
una sola cita, así que un segundo CORRECT sobre RN-003 se quedaría pendiente.

Lo que **sí** quedaría en 0 pendientes es un **CONFIRM sin valor** sobre RN-003: «siempre hay
sesgo» confirma lo que RN-003 ya hace desde ADR-0060. Por la opción (b) iría con las
confirmaciones de valores ya fijados.

**Opciones, sin aplicar:**
- **(a) Que la guardia admita la redirección.** Por ejemplo, un registro `reexpresion_consultor`
  que declare el objetivo anterior. Es un cambio en la guardia y necesita un ADR.
- **(b) Dos registros, sin tocar la guardia:**
  - una `correccion_consultor` sobre RN-033 que sustituya a S-1, con el mismo objetivo, como la
    guardia exige;
  - un CONFIRM sin valor sobre RN-003 con la misma cita literal, que nombre a S-1 en sus notas (sin
    `supersede`).

  Las dos quedan fuera de los pendientes. La de RN-033 iría como confirmación de la regla vigente,
  y conviene decir con qué acción se escribe.
- **(c) Dejar S-1 como el único pendiente conocido**, escrito como tal.

**Estado de `feedback pending` en esta rama**: 1 pendiente (S-1), 83 reflejados, 4 confirmaciones y
9 sin mecanismo, igual que en `main`.

## Estado

**Rama lista para revisión, NO cerrada.**
- **Parte 1 hecha y medida:** ADR-0065 ACTIVE y PROVISIONAL.
- **Parte 2 parada** por la guardia de `supersede`. Falta elegir (a), (b) o (c).
