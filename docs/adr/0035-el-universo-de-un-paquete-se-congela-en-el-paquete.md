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

## Fecha / fase

2026-09-20, post-F13, rama `trabajo/universo-congelado`. Informe:
`docs/validation/UNIVERSO-CONGELADO.md`.

## Estado

ACTIVE
