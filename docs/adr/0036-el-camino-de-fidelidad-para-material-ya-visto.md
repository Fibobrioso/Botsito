---
status: ACTIVE
date: 2026-09-21
phase: post-F13 (abre el reparto del material etiquetado, antes de la primera etiqueta)
---

# 0036 · El material ya visto se reparte por su propio camino, con nombres propios y con puerta

## Decision

1. **Septiembre no entra por el kit.** `knowledge/cases/kit/` y `cases/paquete.py` son el camino del
   etiquetado **ciego**. Se abre un camino propio, `knowledge/cases/fidelidad/` y
   `cases/fidelidad.py`, para repartir **material ETIQUETADO de un mes que el trader ya vio**
   (ADR-0034). Es la decisión que ADR-0034 §6 dejó abierta con esas palabras: *«lo que este ADR NO
   decide: cómo se sortean esas particiones»*.

2. **Un artefacto de fidelidad es tres cosas y ninguna más**: un universo, un reparto fijado antes
   de leer ninguna etiqueta, y un ancla. No lleva cuestionario, ni hoja del trader, ni sesión, ni
   fecha de reunión. Su id no lleva fecha (`eurusd-2026-09`), porque no hay reunión que fechar.

3. **El filtro de `vistos.yaml` se salta A PROPÓSITO**, y queda escrito aquí, en el README del
   directorio y en el módulo: `universo()` recibe `meses_vistos=set()` y `dias_vistos=set()`. **El
   kit no se toca**: su guardia sigue entera.

4. **`cobertura_material`**, clave opcional del bloque `config:`, declara hasta dónde llega el
   material etiquetado, por mes, como **lista de tramos `{desde, hasta}`**. Acota el universo con
   **motivo propio** en `excluidos:`: `fuera de la cobertura del material del trader (<mes> cubre
   <tramos>)`. Y en este camino, **un mes sin cobertura declarada no aporta ningún caso**: existe
   para repartir material etiquetado, y de un mes sin material no hay nada que medir.

   **PROHIBIDO declarar la lista de DÍAS cubiertos**, y el validador lo rechaza por la forma, no por
   convenio. `docs/validation/SEPTIEMBRE-ENTRA.md` dejó escrito que un día laborable del rango que
   **no** aparezca en la columna de fechas del backtest **es un día sin operaciones, y eso ES su
   etiqueta**. Declarar los días cubiertos publicaría esas etiquetas por la puerta de atrás, sin
   pasar por la de ADR-0033.

5. **Nombres de partición propios**: `fidelidad-dev`, `fidelidad-1`, `fidelidad-2`, `fidelidad-3`.
   Los del kit son **globales** —`casos_reservados` agrega sobre todos los repartos y devuelve un
   mapa plano que tira el paquete, y hay **un** `AUTORIZACION-<nombre>.md` por nombre—, así que
   meter días **no ciegos** en `holdout-N` daría un cubo mezclado con los días ciegos de mayo y una
   cifra que no se puede interpretar (ADR-0034: llamarlo holdout *«sería vender por ciego lo que no
   lo es»*).

6. **Y pasan por la MISMA puerta** (`holdout.py`, ADR-0033), con su propio
   `AUTORIZACION-fidelidad-N.md`. ADR-0034 separó dos cegueras: la **del trader**, que septiembre ya
   no tiene, y **la nuestra**, que sigue intacta. Es la nuestra la que la puerta protege. Dejar estos
   nombres fuera sería material reservado **por intención** y desprotegido **por mecanismo**, que es
   la forma de defecto que llevan cerrando las tres últimas ramas; a sabiendas sería peor que las
   anteriores.

   > **FRENO, y es bloqueante.** `kappa_entre_sesiones` deja `excluir` vacío después de pasar la
   > puerta, así que **una autorización lee las etiquetas de todos los cubos**. Extender una puerta
   > con fuga multiplica la fuga: **antes de la PRIMERA autorización hay que cerrarlo**. Hoy es
   > seguro porque `PREREGISTRO.md` sigue vacío y no existe ninguna autorización. Es bloqueante para
   > **abrir**, no para crear los nombres.

7. **La anterioridad se prueba por CASO, no por sesión** (`cases/anterioridad.py`, enganchada en
   `knowledge validate`): toda etiqueta cae sobre un caso que algún reparto commiteado contiene, y
   el commit de ese reparto es ancestro **estricto** del de la etiqueta. Corre sin `data/`.

8. **Lo que este camino puede prometer, y lo que no.** Puede prometer **anterioridad demostrable**.
   **No** puede prometer una cifra con potencia estadística: el mínimo son **36 unidades efectivas
   independientes** (`docs/validation/AUDITORIA-2026-09-13-ultracode.md` §6.1) y **nada construible
   hoy lo alcanza** —los 14 días laborables de septiembre dan 28 unidades brutas y ~23 efectivas, y
   ninguna combinación de mayo llega tampoco—. Lo que sale de aquí es una **cifra descriptiva con su
   intervalo**. Va escrito en el ADR, en el README del directorio y en el módulo a propósito: es lo
   que impide que dentro de seis meses alguien cite esa cifra como si midiera algo.

## Problema que resuelve

`kit build` no puede construir un paquete de septiembre, y está medido: `vistos.yaml` declara
`2026-09` con `visto_el: 2026-09-20`, así que `universo()` excluye sus 14 días con motivo *«mes
visto por el trader»* y `construir()` aborta si alguno se cuela. Forzarlo exigía una de dos:
**falsear la fecha de la sesión** (para que el filtro no mordiera) o **desactivar el filtro de
vistos**. Las dos corrompen un mecanismo para reaprovechar código.

Y el problema de fondo es el que ADR-0034 ya nombró: el material de septiembre **no es ciego**, y el
kit entero está construido alrededor de la ceguera —cuestionario, hoja, `vistos.yaml`, exención de
«sesión celebrada»—. Meterlo ahí habría dejado un paquete que miente sobre lo que es.

## Alternativas consideradas

1. Forzar septiembre por el kit, con una fecha de sesión anterior al `visto_el`.
2. Meter los días de septiembre en `holdout-3`, el cubo más barato de gastar.
3. Nombres propios sin puerta: declararlos y no tocar `holdout.py`.
4. Acotar el 1-18 recortando el manifiesto, o declarándolo en `vistos.yaml`.
5. Dejar la guardia de anterioridad para otra rama.

## Por que elegimos esta opcion

**Camino propio** porque el coste de la alternativa 1 está medido y son **tres falsedades**: una
fecha de sesión falsa, un cuestionario inventado —`validar_paquetes` exige al menos una pregunta con
casos que citen evidencia real— y el test de la puerta roto o una protección perdida. Tres
falsedades para ahorrar un validador.

**Nombres propios** porque los del kit son globales y el mapa que la puerta mira es plano: la
alternativa 2 produce un cubo que mezcla 3 días ciegos de mayo con 14 no ciegos de septiembre, y
ninguna cifra sobre él tiene una interpretación. El camino propio lo resuelve **por construcción**,
no por convenio.

**Con puerta** porque la ceguera que protege ADR-0033 es la nuestra, no la del trader, y esa sigue
intacta.

**Y la guardia de anterioridad entra aquí, no en otra rama**, por tres motivos: (i) lo único que
este camino vende es anterioridad demostrable, así que sin comprobación mecánica afirmaría justo lo
que no puede probar; (ii) «antes de la primera etiqueta» no es una fecha, es una condición sin
dueño, y la guardia de ancestro lleva **cuatro apariciones** enseñando qué les pasa aquí a las
condiciones sin dueño —hacerla ahora cierra una deuda de cuarta aparición en vez de crear una
quinta—; y (iii) sin `sesion` no se puede emparejar por sesión, así que la guardia nueva y la deuda
vieja son ya el mismo trabajo. La línea que separa esto de meter de todo: la guardia es
**constitutiva** de lo que este camino afirma; el agujero de `excluir` es **adyacente** —es de la
puerta, no de este camino—. Por eso una entra y el otro se escribe.

## Por que descartamos las demas

- **(1) Forzar el kit**: ver arriba. Además `comprobar()` no serviría igualmente: llama a
  `construir()`, que valida el nombre de sesión, filtra por `vistos.yaml` y aborta.
- **(2) `holdout-3`**: es el más barato de gastar —3 días en mayo, potencia 0,26, papel de fase 7—
  pero sigue mezclando ciego con no ciego en el mismo cubo, que es justo lo que no se puede
  interpretar.
- **(3) Nombres sin puerta**: medido, `casos_reservados` filtra por los nombres reservados y `abrir`
  rechaza cualquier otro, así que los nombres nuevos nacerían invisibles para la puerta y **no
  autorizables**. Material etiquetado sin guarda.
- **(4) Recortar el manifiesto**: un dataset es inmutable y reutilizable, y dos manifiestos del
  mismo prefijo cubriendo el mismo día hacen fallar `universo()` con *«dos datasets cubren el mismo
  día»*. Y `vistos.yaml` es peor: fusiona «visto» con «etiquetado» justo donde más cuesta separarlos
  después, y su esquema **acepta claves extra en silencio** (medido), así que entraría sin
  validación.
- **(5) Dejar la guardia fuera**: ver arriba.

## Impacto

- **`kit check --sesion 2026-09-09-sesion-01` no se mueve**: salida idéntica a su línea base, con
  `diff`, antes y después de descargar septiembre. El kit no se toca.
- `config_desde_doc` pasa de «las 8 claves exactas» a «las 8 exactas más las opcionales declaradas»
  y acepta un juego de nombres de partición parametrizado. Sigue siendo estricta: lo que no está en
  ninguna de las dos listas se rechaza.
- `asignar` acepta el orden de llenado por parámetro. **El orden importa**: decide qué caso cae en
  qué partición, así que forma parte de lo que `particiones.yaml` reproduce.
- La puerta agrega ahora los repartos de **los dos caminos** (`repartos_commiteables`), y
  `tests/unit/test_puerta_holdout.py` afirma **la unión exacta** en vez de una cifra pegada: no se
  rompe al añadir un camino.

  > **Corrección del 2026-09-21 (enmienda de ADR-0033).** La frase que seguía aquí —que ese test
  > «caza un camino que quede fuera del glob»— **era falsa**, y está medido: con un tercer camino
  > `knowledge/cases/marzo/eurusd-2026-03/particiones.yaml` con un `holdout-2` dentro, los **dos**
  > lados de la igualdad usan `repartos_commiteables`, así que el caso es invisible para ambos y la
  > igualdad se cumple igual. Lo único que afirmaba algo sobre el glob era un par `{"kit",
  > "fidelidad"}` pegado a mano. El test lleva ahora una enumeración que **no** pasa por el glob
  > —sale del disco— y que sí se rompe con ese tercer camino.
- **En este camino ningún fichero se exime nunca** de reproducirse byte a byte: no hubo sesión
  celebrada cuyas respuestas expliquen una diferencia.
- **No cierra** el agujero de `excluir` en `kappa_entre_sesiones` (bloqueante para abrir, §6), ni el
  sorteo de septiembre —que va en su propia rama, porque un ADR decidido y estrenado en el mismo
  aliento acaba con la forma de la conveniencia de un mes—, ni la petición del mes limpio.
- **Queda estrenado en vacío**: los cupos de `knowledge/cases/fidelidad/config.yaml` están en cero y
  no existe ningún artefacto. La prueba entera son los tests de contrato en repositorios sintéticos,
  incluido el caso que hoy pasaba y ya no pasa.

## Fecha / fase

2026-09-21, post-F13, rama `trabajo/septiembre-particiones`. Informe:
`docs/validation/CAMINO-DE-FIDELIDAD.md`.

## Estado

ACTIVE
