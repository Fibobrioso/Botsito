---
status: ACTIVE
date: 2026-09-20
phase: post-F13 (desbloquea la descarga de meses nuevos)
---

# 0035 · El universo de un paquete se congela en el paquete: `comprobar` va por la lista, `construir` por el disco

## Decision

1. **Cada paquete declara los datasets con los que se construyó**, en una clave `datasets:` de su
   `ventanas.yaml`, al lado de `config:` y con la misma lógica: el paquete guarda su copia de lo que
   es global y mutable.
2. **`comprobar()` recompone el paquete con esa lista, nunca con el disco.** Si un dataset de la
   lista ya no está en `data/manifests/`, falla nombrándolo; si en el disco hay datasets del prefijo
   que no están en la lista, los ignora y no se queja.
3. **`construir()` de un paquete NUEVO sigue leyendo el disco**, a propósito. Se expone como
   argumento opcional (`datasets=None` → disco), no como una prohibición: congelar también este
   camino dejaría al proyecto sin poder construir ningún paquete nunca más.
4. **`datasets:` no se exime jamás.** Se comprueba aparte del bucle de comparación byte a byte, como
   `config:`, y **no entra en `DEPENDEN_DE_LAS_RESPUESTAS`**: una diferencia ahí no sale de ninguna
   respuesta del trader. Sin la lista es **problema, no aviso**.
5. **Lo que se puede comprobar sin velas se comprueba sin velas.** `knowledge validate` exige que la
   lista exista, esté ordenada y sin repetidos, y que sus ids sigan en `data/manifests/`.
6. **`lectura_de_velas` declara la lista que de verdad se va a leer** (ADR-0033): con un paquete
   existente, su lista congelada. Declarar de más es menos peligroso que declarar de menos, pero
   sigue siendo una declaración falsa en el único fichero que existe para ser creíble.
7. **`scripts/mover_sesion.py` arrastra la lista del paquete viejo.** Mover una sesión no puede
   reabrir su universo al disco de hoy.
8. **Basta con congelar los ids.** `dataset_id` lleva el hash de su contenido y `data/manifests/` es
   inmutable tras commit (ADR-0005, con hook y guardia de historial), así que el id ya identifica el
   contenido: congelar hashes engordaría el paquete sin añadir garantía.

## Problema que resuelve

`_manifiestos_del_kit` recogía **todo** manifiesto del disco cuyo `dataset_id` empezara por el
prefijo del kit. El universo de un paquete no se calculaba con lo que el paquete usó, sino **con lo
que hubiera en el repositorio ese día**. Descargar un mes nuevo metía sus días en el universo de
paquetes anteriores, el sorteo con el mismo seed repartía distinto y `particiones.yaml` dejaba de
reproducirse — y ese fichero es **la única prueba mecánica de que las particiones se fijaron antes de
etiquetar**, que es lo que hace defendible la cifra de fidelidad de F26.

Y fallaba en silencio: nadie lo veía hasta el día que alguien descargara un mes.

**Medido sobre el paquete real** (`2026-09-09-sesion-01`, seed 20260915, cupos 16/8/8/8): el universo
de hoy son 42 días y `asignar` reproduce `particiones.yaml` exacto. Metiendo los 14 días laborables
de septiembre, **23 de esos 42 cambian de resultado**: 10 se caen del paquete —8 de `holdout-3` y 2
de `holdout-2`—, 13 cambian de partición y entran 10 días de septiembre. **`holdout-3` se queda sin
ninguno de sus 8 días.**

Estaba declarado como pendiente desde el 2026-09-17 (`MESES-VISTOS.md` §6) y bloqueaba la descarga de
septiembre (`SEPTIEMBRE-ENTRA.md` §4). Y no es solo septiembre: el 2026-05-01 está hoy excluido por
«ventana fuera del dataset» porque falta abril, y abril es un mes visto; el día que se congele
`eurusd-m1-2026-04`, ese día pasa a ser caso. **Esta decisión tiene que estar dentro antes de
descargar abril, no solo antes de septiembre.**

## Alternativas consideradas

1. **Congelar la lista en el paquete** (elegida).
2. **Derivarla de `casos[].dataset_id`** en vez de escribirla.
3. **Separar el prefijo del kit** para los datasets nuevos.
4. **Aceptar que la reproducción se pierde** y documentarlo.

## Por que elegimos esta opcion

- **Imita un precedente que ya funciona**: `config.yaml` es global y mutable, así que el paquete
  guarda su copia y `comprobar()` la compara contra ella. Aquí el input que faltaba es el otro.
- **La edición de la sesión 1 fue estrictamente aditiva y se verificó**: 6 líneas añadidas, ninguna
  quitada, y la salida de `kit check --sesion 2026-09-09-sesion-01` es **idéntica** a la línea base
  medida antes de tocar nada, comparada con `diff`. La lista no la eligió nadie: la escribió el
  propio código.
- **Se hizo con 0 `LABEL_CASE` en el repositorio**, que es cuando `ventanas.yaml` todavía se puede
  tocar: la guardia de inmutabilidad se arma con la primera etiqueta.

## Por que descartamos las demas

- **(2) Derivar es lossy, medido por dos vías.** (a) Un dataset cuyos días queden todos excluidos no
  deja ningún caso: hoy mismo pasa tres veces —enero, julio y agosto aportan **66 de las 67
  exclusiones** de la sesión 1 y ni un solo caso—, así que derivar borraría esas 66 líneas y
  `ventanas.yaml` dejaría de reproducirse. (b) El donante por contigüidad: el mes anterior aporta las
  velas de las 22:00/23:00Z al primer día del mes siguiente, y el caso sigue citando el dataset del
  mes nuevo, así que el donante es invisible en `casos[]`; medido en sintético, derivar **pierde un
  caso y reasigna uno reservado**, y el diff que lo delataría queda tapado por la exención de sesión
  celebrada.
- **(3) Separar el prefijo** compra silencio: vuelve en octubre, y con febrero o marzo, y para
  entonces puede haber etiquetas. No arregla la causa, la aplaza.
- **(4) Perder la reproducción** es exactamente lo que ADR-0025 se negó a canjear por seis días de
  biblioteca.
- **Una nota en ADR-0011**, como se hizo con `visto_el`, no vale: allí se añadía un filtro dentro de
  un mecanismo existente; aquí el paquete gana un artefacto nuevo y `comprobar()` deja de preguntarle
  al disco. Además hace falta un id citable para el trailer `Fuente:` de los commits que tocan
  `knowledge/cases/`.

## Impacto

- `ventanas.yaml` de todo paquete lleva `datasets:`. El de la sesión 1 se rellenó el 2026-09-20.
- **Desbloquea** `botsito data download` de meses nuevos: septiembre, y el mes limpio cuando llegue.
- **Arregla de paso un exit 0 que no comprobaba nada**: `hay_datos_del_kit` era un AND global sobre
  todos los datasets del prefijo, así que un manifiesto commiteado sin sus ficheros —aunque fuera
  ajeno al paquete— apagaba `kit check` entero sin declarar ninguna lectura. Ahora los datasets a los
  que les faltan ficheros se **nombran**.
- **Para el paquete de la sesión 2**: su lista se fija en el momento del build y para siempre, así
  que todos los meses que se quieran dentro tienen que estar congelados antes.
- **Para F26, y no es un detalle:** el universo de la sesión 1 son 42 días y su paquete 40, porque
  los cupos suman 40. Los dos que sobran -`2026-05-25` y `2026-06-29`- **no están en
  `particiones.yaml`, ni en `casos:`, ni en `excluidos:`**: los descarta el sorteo por cupos, de
  forma reproducible (puestos 41 y 42 del orden `sha256(seed:caso)`). Consecuencia: un kappa «sobre
  el universo» y uno «sobre el paquete» no son el mismo conjunto, y la frase «las particiones se
  fijaron antes de etiquetar» **cubre el paquete, no el universo** — esos dos días no aparecen en el
  fichero que lo prueba.
- **No cierra** ni la petición del mes limpio, ni el defecto de la guardia de ancestro —que empareja
  por el campo `sesion` y nunca por el caso, y se arregla **antes de la primera etiqueta**—, ni los
  cupos de `config.yaml`, que suman 40 frente a los 14 días laborables de septiembre.

## Enmienda del 2026-09-21 (los cupos, y el ancla que hace falsable lo congelado)

El cuerpo de arriba **no se reescribe**. Lo que cambia se dice aquí.

Este ADR dejó escrito en su Impacto que **no cerraba** «los cupos de `config.yaml`, que suman 40
frente a los 14 días laborables de septiembre». Era el mismo defecto un escalón más abajo, y así se
midió el 2026-09-21: `comprobar()` recomponía con `config.yaml` de HOY —`construir()` se recarga
todo el config en `_cargar_todo`— y solo **comparaba** el bloque `config:` que el paquete ya
guardaba. Consecuencia medida: editar los cupos daba `exit 1` con *«config.yaml cambió después de
generar el paquete»* y *«particiones.yaml difiere»*, así que `config.yaml` era inmodificable
mientras existiera un solo paquete, y septiembre no podía sortearse (`asignar` con 14 casos y 40
cupos: `ParticionError: se piden 40 casos y el universo tiene 14`).

**1. El bloque `config:` se USA, no se compara.** `construir(..., config=)` recibe el config
congelado con el MISMO contrato que `datasets=`: `None` lee el disco —lo que un paquete NUEVO tiene
que hacer— y no-`None` usa el congelado. Un mecanismo, dos entradas, la misma forma. `mover_sesion`
arrastra las dos.

**2. La guardia que comparaba no se borra: cambia de sujeto.** Hacía dos trabajos en una línea y por
eso estorbaba: probaba la reproducción del paquete *y* avisaba de que el config global había
derivado. Lo primero se hace ahora contra el congelado. Lo segundo vive en `validar_paquetes` como
**AVISO con exit 0**, nombrando las claves que difieren: un paquete viejo se reproduce con el suyo y
no tiene por qué saber nada del config de hoy, y editar `config.yaml` para el paquete SIGUIENTE es
el camino normal, no una avería. Vive ahí y no en `comprobar()` porque `validar_paquetes` corre en
`make check` **sin `data/`**, y `comprobar()` sale antes por dos `return` cuando no hay velas.

**3. La falsabilidad, que es lo que legitima congelar — y NO es uniforme.** Si alguien edita los
`cupos` del bloque congelado, la recomposición reparte distinto y `particiones.yaml` —que no se
exime nunca, ni con la sesión celebrada— deja de reproducirse: medido, `ERROR: particiones.yaml
difiere de lo que se genera hoy`. Pero eso **solo vale para los cupos**. `anclajes_candidatos`,
`sesiones` y `etiquetas` alimentan únicamente `ventanas.yaml` y `hoja_trader.md`, que una sesión
celebrada SÍ exime. Medido el 2026-09-21 sobre el paquete real, renombrando la etiqueta del anclaje
dentro del bloque congelado: **`exit 0`, «sin diferencias que no explique la sesión celebrada»**. Y
la guardia de ancestro no lo tapa: se desentiende con `if not etiquetas: continue` y hoy no existe
ni un `LABEL_CASE` en el repositorio. Dicho de frente: **hasta esta enmienda, la línea que aquí se
cambia de sujeto era lo único que impedía editar a mano el bloque congelado de un paquete
celebrado.** Cambiarla sin nada a cambio habría abierto justo el agujero que la Decisión punto 4 de
arriba se escribió para no abrir.

**4. Por eso lo congelado se ata FUERA, con un ancla de blob.** `knowledge/cases/kit/anclas.yaml`
declara, por sesión, el sha del **blob** de `ventanas.yaml` y `particiones.yaml`. Es el patrón de
`preregistro_blob` (ADR-0033) y cumple sus tres requisitos: vive **fuera** del fichero que ata —un
ancla dentro de lo que ancla la reescribe quien reescriba el fichero—; es **blob y no commit**,
porque el blob cambia con cualquier byte y con nada más y sobrevive a un rebase (`ventanas.yaml`
tiene ya dos commits, y un ancla de commit lo habría dado por alterado sin estarlo); y **re-anclar
es un acto explícito**, `botsito kit anclar --sesion <s> --reanclar`, cuyo diff se ve en otro
fichero. El ancla **no depende de que existan etiquetas**: ese `continue` es precisamente lo que
deja sin atar el período en el que hace falta.

Medido después: editar `config.yaml` a 6/3/3/2 deja `kit check` de la sesión 1 **idéntico a su línea
base** con `diff` y `knowledge validate` en exit 0 con el aviso de deriva; el mutante sobre los
cupos congelados sigue viéndose fallar; y el mutante sobre `anclajes_candidatos`, que daba exit 0,
pasa a `exit 1`.

**Lo que esta enmienda NO cambia.** La decisión de ADR-0025 sigue en pie: los cupos de `config.yaml`
no se tocan *para reparticionar mayo*. Lo que caduca es su **argumento**, que decía que tocarlos
«rompería la comprobación del paquete entero» citando este mecanismo de comparación. Ya no la rompe,
y ADR-0025 lo dice ahora en su propia nota. Tampoco hacen falta cupos por paquete: editar
`config.yaml` antes de cada `kit build` basta, porque cada paquete guarda el suyo — y eso solo es
seguro **con** el ancla puesta.

## Fecha / fase

2026-09-20, post-F13, rama `trabajo/universo-congelado`. Informe:
`docs/validation/UNIVERSO-CONGELADO.md`. Enmienda del 2026-09-21, rama
`trabajo/cupos-congelados`. Informe: `docs/validation/CUPOS-CONGELADOS.md`.

## Estado

ACTIVE
