# El arnés del motor

Cómo se corre el motor sobre CONSTRUCCIÓN y se lee su informe (ADR-0048). Escrito el 2026-09-25 en
la rama `trabajo/arnes-motor`.

## Qué hace

Toma los días `dev` de los meses de construcción de `knowledge/cases/criterio_fidelidad.yaml` (hoy
abril, julio -del 1 al 17-, agosto y enero -del 2 al 30- de 2026; julio desde ADR-0078 y enero desde ADR-0079) y hace pasar cada uno por el motor. El motor es el intérprete del árbol
genérico de ADR-0030, con las primitivas que haya escritas. Después compara las operaciones del
bot con las del trader usando el criterio de ADR-0043, y escribe un informe con:
- **cobertura y precisión**, y las operaciones del bot en días sin operaciones del trader;
- **el embudo sobre el grafo de hechos**: cuántas sesiones con operaciones del trader producen cada
  hecho, y cuántas se paran en cada primitiva `NO_IMPLEMENTADA`;
- **RN-003 al abrir la sesión**, por sesión y por operación del trader;
- **una línea por sesión** con lo que se produjo y dónde se paró cada hecho que faltó;
- **las diferencias por operación** (desde `trabajo/corrida-construccion`, R3.1, 2026-10-14), la
  última sección del informe del arnés: el resumen por mes (en el orden de `construccion`), el
  embudo por mes y una fila por operación del trader y por operación del bot sin pareja. Es el
  MISMO emparejamiento del criterio partido por mes, para que el consultor clasifique cada
  diferencia; no añade ninguna opción al comando. Cómo se lee, abajo.

## Cómo se corre

```
uv run botsito motor arnes --salida arnes.txt
```

Sin `--meses` corre sobre todos los meses de construcción. Con `--meses AAAA-MM,AAAA-MM` corre solo
sobre esos, y tienen que ser de construcción. Por pantalla sale `OK` con la ruta del informe, y una
línea `TIEMPO` y `MEMORIA` que **no** va en el informe: el informe es determinista y dos ejecuciones
dan el mismo fichero byte a byte, así que dos informes se comparan con `diff`.

La `MEMORIA` es el pico del proceso entero, el que lleva el sistema (working set en Windows, RSS
máxima en Linux), y no cuesta nada. Con `--tracemalloc` se añade lo que asigna Python medido con
`tracemalloc`, que era lo único que daba hasta la rama `trabajo/memoria-suite`: es caro en tiempo y
en memoria, y por eso ya no va por defecto.

## El modo simulación (`--simular`, ADR-0053)

```
uv run botsito motor arnes --simular --salida arnes-simulado.txt
```
Corre el MISMO arnés con el motor cableado al broker simulado y a la capa de cuenta: las órdenes
que la spec coloca se llenan con ticks (obligatorios, ADR-0051 §8), la cuenta viva da el veredicto
del tramo y el informe lleva al final una sección «Simulación» con el veredicto, la curva de equity
por día, los eventos del broker y los huecos con nombre (primitivas sin contrato que alguna regla
pidió). Las operaciones del bot que puntúan para el criterio son las posiciones LLENADAS, no las
órdenes colocadas. Opciones: `--perfil <nombre>` (por defecto el único de `knowledge/cuentas/`),
`--fase <fase>` (por defecto la primera del perfil) y `--depuracion`, que admite días sin ticks
sobre el respaldo M1 y marca toda la salida con `DEPURACION: respaldo M1, no cuenta`. Medido el
2026-09-26: abril entero tarda unos tres minutos.

La última sección, «Peticiones al servidor», cuenta por día de la firma (medianoche CE(S)T) las
peticiones que el bot emite al servidor: colocar, modificar, cancelar y cerrar, aceptadas o
rechazadas. Da también el máximo diario junto a `firma_mensajes_dia_max` (R13). Solo mide, nada
frena (`docs/validation/CONTADOR-PETICIONES.md`).

Desde `trabajo/corrida-construccion` (2026-10-14), entre los eventos y las peticiones van **la vida
de la orden**: «Ordenes» (`dia | sesion | id | colocada UTC | precio | resultado | motivo | instante
del resultado`, una línea por orden que el bot intentó colocar; el resultado es `llenada`,
`rechazada`, `cancelada` o `viva al cerrar el dia`, y el motivo lo da el bróker en un rechazo
-`precio_invalido`, `stops_level`…- o el cableado en una cancelación: dónde cayó el cierre de M1
-«al abrir otra sesion», «en ventana_fin»- y las reglas que dispararon en él, o la red de
seguridad del fin del día) y «Rechazos por motivo» (`mes | motivo | peticion | rechazos`). Es
lectura de la traza del bróker: nada decide.

## Cuándo se niega

- **Un mes de medida** (hoy mayo) o **cualquier mes que no sea de construcción** (marzo, septiembre,
  febrero...): sale con `ERROR` y código 2, y **no escribe nada**. La medida tendrá su propia rama y
  su propio ADR (ADR-0048 §7).
- **Un día oculto** (reservado o retirado) entre los días `dev`: sale con `ERROR` y código 3 sin
  leer su caso. No debería pasar nunca, porque la biblioteca lo impide; si pasa, se para y se
  investiga.

## Cómo leer el embudo

- `hecho:si`: la sesión lo produjo.
- `hecho:no[primitivas]`: no lo produjo, y las reglas que lo producen se pararon en esas primitivas
  `NO_IMPLEMENTADA`.
- `hecho:no[productoras sin cumplirse]`: las reglas que lo producen se evaluaron y no se cumplieron.
  Por ejemplo, RN-003 con el sesgo ambiguo.
- `rn003`: lo que dijo `domain/sesgo.py` al abrir la sesión.

Una primitiva `NO_IMPLEMENTADA` vale DESCONOCIDO y no decide: ni deja pasar ni prohíbe (ADR-0048
§2). Hasta que exista el bróker simulado, el motor real no produce ninguna operación y la cobertura
es 0.

## Cómo leer «Diferencias por operacion»

Tres bloques, todos deterministas y con los campos separados por ` | `:

- **Resumen por mes**: `mes | dias | trader | bot puntuables | bot en dias sin trader | parejas |
  cobertura | precision`. Son las cifras del criterio (ADR-0043) partidas por mes: una pareja exige
  el mismo día, así que la partición es idéntica a medir cada mes aparte. Los meses van en el orden
  de `construccion`, no por fecha.
- **Embudo por mes**: para las sesiones con operaciones del trader y SIN operación del bot, el
  primer hecho DEL CAMINO (origen `regla`, en el orden de la spec, sin los frenos
  `detenido_por_*`) que la sesión no produjo, con las primitivas `NO_IMPLEMENTADA` en que se
  pararon sus productoras, o `productoras sin cumplirse`; `todos los hechos del camino producidos`
  si no faltó ninguno (lo que faltó está en la vida de la orden: «Ordenes», abajo). Un freno se
  nombra aparte (`; frenos producidos: …`) solo si se produjo: uno que no se produjo no faltó.
- **Por operación**: `quien | dia | sesion | lado | instante UTC | entrada | resultado`, por mes de
  construcción y por día; en cada día, el trader primero y después el bot sin pareja. Para el
  trader, `PAREJA bot <instante> <entrada> (Δentrada, Δinstante)` o `SIN PAREJA; bot mas cercano en
  la sesion: …` o `SIN PAREJA; ninguna operacion del bot en la sesion`, seguido del primer hecho que
  faltó en esa sesión. Para el bot sin pareja, lo mismo del otro lado (`trader mas cercano en la
  sesion`, `ninguna operacion del trader en la sesion` o `… en el dia`). Los Δ llevan signo (lo
  nombrado menos la fila: bot − trader en una fila del trader) y «más cercano» sigue el orden del
  criterio -menor |Δinstante|, luego menor |Δentrada|, luego el más temprano- sin exigir el lado.
  Una operación del bot emparejada no sale aparte: está en la fila de su trader. Con `--simular`,
  la sección queda antes de la cola «Simulacion» que pega el comando.

## Lo que no hace

No mide nada sobre mayo, no abre ningún holdout y no cambia la spec. Los huecos de interpretación
que encontró al construirse están en ADR-0048 (H1-H6).
