# El universo de un paquete se congela en el paquete

Rama `trabajo/universo-congelado`, desde `084c8ba` (tag `stable/F13-septiembre`). Sin tocar main, sin
merge, sin tag, sin push. Sin descargar velas, sin sortear particiones, sin tocar `config.yaml` ni
`knowledge/spec/` (12.1.1, mismo hash), sin abrir nada.

## 1. La línea base, guardada antes de tocar nada

`kit check --sesion 2026-09-09-sesion-01` a un fichero: 5 líneas, exit 0. Es contra eso, con `diff`,
contra lo que se compara. **Resultado al final de la rama: salida IDÉNTICA.** Medido dos veces, antes
y después de `make check`.

## 2. El tamaño del defecto, medido sobre el paquete real

El universo de hoy son **42 días** —el `ventanas.yaml` escribe 40 casos porque los cupos suman 40— y
`asignar(universo, seed 20260915, cupos 16/8/8/8)` reproduce `particiones.yaml` **exacto**.

Metiendo los 14 días laborables de septiembre (1‑4, 7‑11, 14‑18):

| | |
|---|---|
| Universo | 42 → 56 |
| De los 42 de hoy, **cambian de resultado** | **23** |
| ↳ se caen del paquete | 10 (8 de `holdout-3`, 2 de `holdout-2`) |
| ↳ cambian de partición sin salir | 13 |
| Días de septiembre que entran | 10 |
| `holdout-3` | **se queda sin ninguno de sus 8 días** |

**Corrección sobre lo que dije en la revisión:** la cifra es **23 de 42**, no 33. El 33 sumaba los 10
días de septiembre que entran, que no son «casos que cambian de partición» sino casos nuevos.

## 2b. Los dos días del universo que no están en ninguna partición

El universo son 42 días y el paquete 40, porque los cupos suman 40. **Los dos que sobran son
`2026-05-25` y `2026-06-29`** (`caso-eurusd-2026-05-25` y `caso-eurusd-2026-06-29`).

**Dónde están, medido:** en ninguna parte del paquete. No están en `particiones.yaml`, así que **no
son `dev` ni holdout**; no están en `casos:` de `ventanas.yaml`; y **tampoco están en `excluidos:`**,
porque no se excluyeron por ningún motivo de datos. Lo único que deja constancia de que existen es
el contador `universo: 42`.

**Cómo se eligieron:** los descarta el sorteo por cupos, y de forma **reproducible**. `asignar()`
ordena los casos por `sha256(f"{seed}:{caso}")` —con el id como desempate— y reparte los cupos en
orden sobre esa lista; los sobrantes «quedan fuera del paquete». Con el seed commiteado (20260915),
`2026-05-25` queda en el **puesto 41** y `2026-06-29` en el **42** de 42. No hay azar no reproducible:
mismo seed y mismo universo dan los mismos dos días, y eso se vuelve a comprobar cada vez que
`kit check` reproduce `particiones.yaml`.

### La consecuencia para F26, que hay que tener delante

- **Un kappa «sobre el universo» y uno «sobre el paquete» NO son el mismo conjunto.** Se diferencian
  en estos dos días. Cualquier cifra tiene que decir sobre cuál de los dos se calcula.
- **«Las particiones se fijaron antes de etiquetar» cubre el PAQUETE, no el universo.** La prueba
  mecánica es `particiones.yaml`, y esos dos días no aparecen ahí. Si algún día se etiquetaran, su
  anterioridad no estaría probada por ese fichero: habría que fijarlos antes, en un paquete.
- **No son holdout, así que no queman ni protegen nada.** No sirven para medir fidelidad contra un
  reparto ciego, porque nunca estuvieron repartidos.

## 3. Derivar la lista no vale, y está medido por los dos lados

**(a) El dataset sin casos ocurre hoy, tres veces.** Los 40 casos de la sesión 1 citan solo mayo y
junio, pero **66 de sus 67 exclusiones** salen de enero, julio y agosto: tres datasets que están en
el universo y **no dejan ni un caso**, porque son meses vistos. Una lista derivada daría `{05, 06}` y
borraría esas 66 líneas: `ventanas.yaml` deja de reproducirse.

**(b) El donante por contigüidad.** `universo()` cose meses y el anterior aporta las velas de las
22:00/23:00Z al primer día del siguiente, pero **el caso sigue citando el dataset del mes nuevo**, así
que el donante es invisible en `casos[]`. Medido en sintético: derivar **pierde un caso entero** y,
con cupos que lo alcancen, **reasigna un caso reservado** — y el diff de `ventanas.yaml` que lo
delataría queda tapado como AVISO por la exención de sesión celebrada.

Hoy (b) no muerde por suerte, porque el único donante real es mayo→junio y mayo también aporta casos.
Pero **está a un manifiesto de morder**: `2026-05-01` figura excluido por «ventana fuera del dataset»
porque no hay abril, y abril es mes visto. El día que se congele `eurusd-m1-2026-04`, ese día pasa a
ser caso con un donante de cero casos. **Esta rama tiene que estar dentro antes de descargar abril,
no solo antes de septiembre.**

## 4. Qué se construyó

| Pieza | Qué hace |
|---|---|
| `ventanas.yaml` gana `datasets:` | La lista de ids con la que se construyó el paquete. La escribe `construir()` |
| `_manifiestos_del_kit(repo, config, datasets=None)` | Con lista, devuelve exactamente esos y **falla nombrando** los que ya no estén; sin lista, el disco |
| `construir(..., datasets=None)` | Por omisión, **disco**: un paquete nuevo se hace con lo que hay |
| `comprobar()` | Usa la lista congelada, y la valida **aparte** del bucle byte a byte |
| `lectura_de_velas(..., datasets=None)` | Declara los datasets que **de verdad** se van a leer (ADR-0033) |
| `validar_paquetes` | Sin velas, en CI: la lista existe, está ordenada y sin repetidos, y sus ids siguen en `data/manifests/` |
| `scripts/mover_sesion.py` | Arrastra la lista del paquete viejo, leída **antes** de borrar su carpeta |

**El criterio, para que siga siendo prueba y no permiso:** sin `datasets:` es **problema, no aviso**,
también en una sesión celebrada; `DEPENDEN_DE_LAS_RESPUESTAS` **no se toca**, y el comentario que la
acompaña dice ahora por qué `datasets:` nunca entra ahí. Si entrara, alterar la lista congelada sería
invisible justo en las sesiones que importan.

## 5. La sesión 1: aditivo y verificado

La lista **no la eligió nadie**: la escribió `construir()` con el disco de hoy, que son los cinco
manifiestos con los que el paquete se construyó, todos dados de alta antes que él. `git diff --stat`:
**6 líneas añadidas, 0 quitadas**, y `git diff -U0` no tiene ni una línea `-`.

La prueba de que la edición es correcta es que **`kit check` siga dando la salida idéntica**: cero
problemas, los dos mismos AVISO de sesión celebrada y ni uno nuevo. Si no se reprodujera, la edición
estaría mal y se corregiría la edición — **jamás se eximiría el fichero**.

Se hizo **hoy porque hoy se puede**: la guardia que congela `ventanas.yaml` y `particiones.yaml` solo
se arma cuando existe algún `LABEL_CASE` de esa sesión, y hay **cero** en el repositorio.

## 6. El exit 0 que no comprobaba nada, ahora nombra

`hay_datos_del_kit` era un AND global sobre **todos** los datasets del prefijo: un manifiesto
commiteado sin descargar sus ficheros —aunque fuera **ajeno** al paquete— convertía `kit check` en un
exit 0 que no comprobaba nada y que **no declaraba ninguna lectura**, así que ADR-0033 se quedaba
mudo. Es la misma clase de defecto que esta rama arregla, y está en el camino de lo siguiente que se
va a hacer, que es descargar septiembre.

Ahora `datasets_que_faltan_en_disco` los **nombra**, y la frontera es esa: nombrar, y nada más. No se
ha rediseñado `kit build` ni se ha cambiado lo que construye.

## 7. `lectura_de_velas` declaraba de más

Sin partir por llamante, `kit check` habría declarado **seis** datasets leyendo cinco. Declarar de más
es menos peligroso que declarar de menos, pero sigue siendo **una declaración falsa en el único
fichero que existe para ser creíble**. Queda corregido: se declara la lista congelada.

## 8. Los tests, que ven fallar el defecto

Cuatro nuevos, todos metiendo el manifiesto de verdad en un repositorio de prueba:

1. **Un dataset nuevo no cambia un paquete ya escrito**, y un paquete nuevo **sí** lo ve.
2. **Sin `datasets:` es problema**, con `celebrada=False` y con `celebrada=True`, y `knowledge
   validate` lo ve sin datos.
3. **Quitar un dataset de la lista congelada se ve**, aunque la sesión esté celebrada: es el caso del
   donante.
4. **Un manifiesto sin sus ficheros nombra los datasets**, y no apaga la comprobación de un paquete
   que no lo tiene congelado.

**Mutante comprobado:** devolviendo `comprobar()` a leer el disco, el test 1 falla. Restaurado, pasa.

## 9. Lo que NO se ha hecho

- **No se descargan las velas de septiembre** ni se sortea nada: esto desbloquea esa rama, no la hace.
- **`construir()` no se congela**, a propósito: sería el tercer caso del mes de una prohibición que
  bloquea un paso que el proceso exige.
- **La guardia de ancestro** sigue emparejando por `sesion` y no por caso. Anotada, con su condición
  fechada: **antes de la primera etiqueta**.
- **Los cupos de `config.yaml`** siguen sumando 40 frente a 14 días de septiembre. Otro brief.

## 10. Qué debe decidir el usuario

1. **¿Validar la rama** y hacer el ritual (tag `stable/F13-universo`)?
2. **El orden de lo siguiente**: con esto dentro se puede descargar septiembre, pero el sorteo sigue
   bloqueado por los cupos. ¿Se hace la rama de los cupos antes de descargar, o se descarga ya?
3. **Abril**: el aviso del §3 dice que congelar `eurusd-m1-2026-04` cambia el 2026-05-01. Con esta
   rama dentro, el paquete de la sesión 1 está protegido; ¿se quiere abril en el corpus de datos, o
   se deja fuera?

## 11. Cómo comprobarlo

```
uv run botsito kit check --sesion 2026-09-09-sesion-01     # identica a la linea base
git diff -U0 084c8ba -- knowledge/cases/kit/2026-09-09-sesion-01/ventanas.yaml   # 6 lineas, ninguna '-'
uv run pytest tests/unit/test_kit.py -k "congelad or dataset_nuevo or sin_sus_ficheros" -q
uv run botsito knowledge validate
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
