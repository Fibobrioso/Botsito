# Septiembre entra: lo que se puede cerrar hoy, y el bloqueo que se lleva su propia rama

Rama `trabajo/septiembre-entra`, desde `4f571ac` (tag `stable/F13-liquidez`). Sin tocar main, sin
merge, sin tag, sin push. **Sin abrir el xlsx ni las capturas**, sin tocar velas, `config.yaml`, el
paquete de la sesión 1 ni `knowledge/spec/` (12.1.1, mismo hash).

## 1. La exposición del 2026-09-20, declarada el mismo día

El consultor abrió `backtesting-analytics SEPTIEMBRE 2026.xlsx` en Excel y leyó **la columna de
fechas**, para saber qué días cubre el material: **del 1 al 18 de septiembre**. Declara que no miró
resultados, ni PnL, ni el detalle por operación, ni ninguna captura.

**Veredicto: NO QUEMA** (ADR-0021 §1, con el precedente del 2026-09-13). Saber qué días cubre un
fichero no es leer una etiqueta ni medir una cifra del bot, igual que no lo es leer velas para fijar
un universo. Y medido hoy, **no hay nada que quemar**: `particiones.yaml` solo tiene casos de mayo y
junio, no existe dataset `eurusd-m1-2026-09` y **no hay ni un `LABEL_CASE` en todo el repositorio**.
La exposición es **anterior** al sorteo.

Va con tres cosas más escritas en la fila, porque ninguna se puede probar de otra forma:

- **Excel pinta la hoja activa entera**, y no hay prueba mecánica de que solo se renderizara esa
  columna. El único rastro es el fichero de bloqueo `~$…`, que prueba la apertura y nada más.
- **La reserva del 2026-09-12**: un día laborable del 1 al 18 que **no** aparezca en esa columna
  sería un día sin operaciones, y eso *es* su etiqueta. Como no consta si se vio día a día o solo el
  rango, no se puede nombrar ninguno —nombrarlo exigiría abrir el fichero—, así que **F26 excluye en
  bloque los días sin operaciones**, por anticipado, igual que excluye 2026-05-14.
- **Esa lectura cruzó `CLAUDE.md`**, que desde el 2026-09-17 ponía el backtest de septiembre entero
  fuera de alcance «hasta que sus particiones estén sorteadas y commiteadas». No se abrió ningún
  holdout, pero la regla escrita era más ancha que ADR-0021 §1 y se rompió. Queda declarado.

## 2. El inventario, medido antes de ejecutarlo

`corpus inventory` guarda por fichero **ruta, papel, bytes y sha256**, y el hash se calcula abriendo
en binario por bloques. No hay parseo, ni rama por extensión, ni `ffprobe` fuera de los vídeos
declarados; el único `read_text` del módulo es para un `index.txt` del material heredado. Refuerzo
mecánico: las dependencias del proyecto son **solo `pyyaml` y `tzdata`** —no hay openpyxl, ni
pandas, ni Pillow—, así que ninguna ruta de código puede leer el libro ni renderizar un JPEG.

Entraron **siete** ficheros. El fichero de bloqueo de Excel **no**: se cerró Excel y se borró antes
de inventariar, porque `rglob` no excluye nada y un libro abierto puede cambiar de bytes y con ellos
su hash. Verificado después: el xlsx conserva sus **10.066 bytes** y el mtime de la copia, así que el
sha256 congelado es el del fichero tal como lo mandó el trader. `corpus check`: OK.

## 3. Septiembre, declarado visto — con la fecha que sí tiene fuente

`visto_el: "2026-09-20"`, que es el día de la **entrega**. **La fecha en que el trader lo backtesteó
no se sabe, y está pedida.** Se fecha con lo único que tiene fuente, que es el mismo criterio que se
aplicó a abril el 2026-09-17: el motivo decía 09-03 y solo el commit del 09-05 lo sostenía. Si llega
otra fecha con su fuente delante, se corrige; y corregirla no rompe nada, porque **ningún paquete ha
sorteado septiembre**.

Comprobado: `kit check --sesion 2026-09-09-sesion-01` sigue en **OK**. La sesión 1 es del 09-09 y
septiembre se declara visto el 09-20, así que no entra en su universo por el mecanismo que cerró
`stable/F13-vistos`.

## 4. El bloqueo: por qué las velas y las particiones NO entran en esta rama

Son dos bloqueos distintos, los dos medidos.

**(a) Los cupos no dan, y no se pueden tocar.** `config.yaml` pide 16 `dev` + 8 + 8 + 8 = **40
casos**; septiembre tiene **14 días laborables** (1-4, 7-11, 14-18). No sale un reparto pequeño:
salta `ParticionError: se piden 40 casos y el universo tiene 14`. Y `comprobar()` compara el
`config` que el paquete guardó contra el fichero de hoy, así que cambiar los cupos **rompe la
comprobación de la sesión 1 entera** —lo que ADR-0025 ya se negó a hacer por menos—.

**(b) Y esto no lo preveía el brief: descargar las velas de septiembre rompe la sesión 1 por sí
solo.** `_manifiestos_del_kit` recoge **todo** manifiesto cuyo `dataset_id` empiece por el prefijo
del kit. Un dataset `eurusd-m1-2026-09` entraría por tanto en el universo de **cualquier** paquete,
incluido el de la sesión 1: el universo cambia, el sorteo con el mismo seed reparte distinto y
`particiones.yaml` deja de reproducirse. Y ese fichero es **problema, no aviso**: es la única prueba
mecánica de que las particiones se fijaron antes de etiquetar.

Declarar septiembre en `vistos.yaml` **no protege** contra esto: el filtro compara con la fecha de
la **sesión**, así que blindar a la sesión 1 exigiría un `visto_el` anterior al 2026-09-09, y ninguna
fuente lo sostiene. Ya estaba declarado como pendiente en `MESES-VISTOS.md` §6, y nadie lo había
resuelto.

**(c) Y el kit no sabe hacer lo que hacía falta.** `kit build` es el camino del etiquetado **ciego**;
sortear particiones de un mes **ya visto**, para medir fidelidad, es otra operación (ADR-0034).

### La decisión, ya tomada: se congela el universo en el propio paquete

La causa raíz es una sola: **el universo de un paquete se calcula del disco de hoy, en vez de con lo
que el paquete se construyó.** Se arregla **congelando el universo dentro del paquete**, exactamente
como ya se hizo con `config.yaml`, que el paquete guarda y `comprobar()` compara.

Lo que **no** se hace, y por qué:

- **NO se separa el prefijo del kit para el dataset nuevo.** Compra silencio y vuelve en octubre, y
  otra vez con febrero o marzo —el mes limpio que está pedido—, y para entonces puede haber
  etiquetas, que es cuando ya no hay marcha atrás.
- **NO se acepta perder la reproducción** del paquete de la sesión 1. Es justo lo que ADR-0025 se
  negó a canjear.

**Línea base medida hoy, antes de tocar nada:** `kit check --sesion 2026-09-09-sesion-01` sale
**exit 0**. El criterio de aceptación de la rama siguiente no es volver a sacar 0: es que **la salida
sea IDÉNTICA comparada con `diff`**, como se hizo en la rama de los meses vistos. Exit 0 con otra
salida sería un cambio silencioso.

## 5. El defecto de la guardia de ancestro, con su condición fechada

`validar_paquetes` empareja las etiquetas con las particiones **por el campo `sesion` del registro,
nunca por el caso**. Medido en repositorio sintético: una etiqueta sobre un caso de septiembre pasa
la guardia sin problema si lleva en `sesion` el nombre de la sesión 1 —cuyo `particiones.yaml` es
ancestro de todo— o un nombre de sesión sin paquete, que el bucle ni visita.

**Se arregla ANTES DE LA PRIMERA ETIQUETA de septiembre, no «algún día».** Hoy no existe ni un
`LABEL_CASE`, así que la guardia no puede fallar; en cuanto exista uno, la prueba de anterioridad ya
está comprometida y no se recupera. **Es la tercera vez que queda apuntado** —MESES-VISTOS §3 lo
llamó defecto, BREAKER-M1 lo repitió— y ahora queda con su condición y con dueño en el tiempo, en
ADR-0034 §Impacto y en Technical Debt.

## 6. Qué es septiembre (ADR-0034)

Material **etiquetado** de un mes que el trader **ya ha visto**. No es ciego para una sesión en vivo
—y el mecanismo de `vistos.yaml` ya lo impide— y sí sirve para medir fidelidad, con las particiones
fijadas antes de leer ninguna etiqueta. **No cierra** la petición del mes limpio: eso sigue
pendiente, y es la lectura fácil y equivocada.

## 7. Qué debe decidir el usuario

1. **¿Validar la rama** y hacer el ritual (tag `stable/F13-septiembre`)?
2. **La precisión de `CLAUDE.md`** (§1): hoy dice que el backtest de septiembre no se abre hasta
   tener particiones, y eso ya no describe lo que pasó. Lo propuesto: de septiembre no se abren el
   detalle por operación ni las capturas; la columna de fechas para fijar el universo sí, y se
   declara. **No lo he tocado en esta rama**, porque cambia una regla de la casa y es tuya.
3. **La rama del universo congelado**: es el bloqueo entero y necesita su brief y su ADR.
4. **La fecha real del backtest del trader**, que está pedida y hoy no consta.

## 8. Cómo comprobarlo

```
uv run botsito corpus check                                  # el corpus coincide con el manifiesto
uv run botsito kit check --sesion 2026-09-09-sesion-01       # OK, y su salida es la linea base
grep -A14 '2026-09' knowledge/cases/kit/vistos.yaml
sed -n '/2026-09-20/p' docs/validation/HOLDOUT-EXPOSICIONES.md
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
