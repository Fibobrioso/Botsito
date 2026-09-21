# Los cupos se congelan en el paquete, y lo congelado queda atado

Rama `trabajo/cupos-congelados`, desde `fd2b899` (tag `stable/F13-universo`). Sin tocar main, sin
merge, sin tag, sin push. Sin descargar velas, sin sortear particiones, sin tocar `knowledge/spec/`
(12.1.1, mismo hash), sin `knowledge/evidence/` ni `knowledge/feedback/`, sin abrir nada.

Es la **enmienda de ADR-0035**, no un ADR nuevo: el propio ADR-0035 dejó escrito en su Impacto que
no cerraba «los cupos de `config.yaml`, que suman 40 frente a los 14 días laborables de septiembre».
La misma decisión aplicada al otro input del mismo cálculo.

## 1. La línea base, guardada antes de tocar nada

`kit check --sesion 2026-09-09-sesion-01` a un fichero: 5 líneas, exit 0. Es contra eso, con `diff`,
contra lo que se compara. **Resultado al final de la rama: salida IDÉNTICA**, medida cuatro veces
(tras el cambio de código, tras el ancla, tras editar `config.yaml` y tras `make check`).

## 2. El bloqueo, medido antes de escribir código

`comprobar()` recomponía con el `config.yaml` de HOY —`construir()` se recarga todo el config en
`_cargar_todo`— y solo **comparaba** el bloque `config:` que el paquete ya guardaba
(`paquete.py:748`). Con un mutante en el árbol de trabajo (`dev: 16` → `dev: 6`):

```
exit=1
ERROR: 2026-09-09-sesion-01: config.yaml cambio despues de generar el paquete
ERROR: 2026-09-09-sesion-01/particiones.yaml: difiere de lo que se genera hoy
```

Y por el otro lado, `asignar` con 14 casos y los cupos de hoy:
`ParticionError: se piden 40 casos y el universo tiene 14`. Septiembre tiene 14 días laborables
(1-4, 7-11, 14-18) y `config.yaml` pide 16+8+8+8. Es decir: **para sortear septiembre había que
editar `config.yaml`, y editarlo rompía la sesión 1**. El propio `config.yaml` lo avisaba en su
comentario; lo que nadie había medido es que eso bloqueaba el paso siguiente del proceso.

## 3. La falsabilidad NO es uniforme, y ese es el hallazgo de la rama

Lo que legitima congelar algo dentro de un fichero es que editarlo a mano se vea. Se midió por los
dos lados, mutando el bloque congelado y el global a la vez para que la guardia vieja no enturbiara
la señal:

| mutante sobre el bloque `config:` congelado | antes de esta rama |
|---|---|
| `particiones: dev: 16 → 15` | **exit 1**, `ERROR: particiones.yaml: difiere de lo que se genera hoy` |
| `anclajes_candidatos: etiqueta: servidor-ny-17 → -99` | **exit 0**, `OK: sin diferencias que no explique la sesion celebrada` |

El segundo es el agujero. `anclajes_candidatos`, `sesiones` y `etiquetas` no tocan
`particiones.yaml` jamás: solo producen `casos[].limites_h4` y `hoja_trader.md`, y los dos ficheros
están en `DEPENDEN_DE_LAS_RESPUESTAS`, así que con `celebrada=True` bajan a AVISO. En ese mutante,
las 40 claves `limites_h4` del fichero commiteado dejaron de coincidir con lo regenerado y el
comando dijo **OK**.

Consecuencia: **la línea 748 era lo único en todo el repositorio que impedía editar a mano el bloque
`config:` de un paquete celebrado.** Cambiarle el sujeto sin nada a cambio habría abierto justo el
agujero que el comentario de ADR-0035 se escribió para no abrir. Y la guardia de ancestro no lo
tapa: se desentiende con `if not etiquetas: continue` y hoy no existe **ni un `LABEL_CASE`** en el
repositorio (118 registros de feedback; el único «LABEL_CASE» del repo está en el README del
esquema). El paquete de la sesión 1 estaba ya en el régimen «perdonado» sin estar en el
«inmutable».

Por eso la rama es la completa y no la mínima: una rama puede dejar el repositorio igual o mejor,
nunca peor en un punto concreto.

## 4. Qué se construyó

1. **`construir(..., config=)`**, con el MISMO contrato que `datasets=`: `None` lee el disco —lo
   que un paquete NUEVO tiene que hacer— y no-`None` usa el congelado. `cargar_config(ruta)` se
   parte en `config_desde_doc(doc, nombre)` + la fina, para que el bloque congelado pase por la
   misma validación que el fichero global. `comprobar()` le pasa el bloque del paquete.
2. **La guardia vieja cambia de sujeto, no se borra.** El aviso de deriva del config global vive en
   `validar_paquetes` como **AVISO con exit 0**, nombrando las claves que difieren. Ahí y no en
   `comprobar()` porque `validar_paquetes` corre en `make check` **sin `data/`**, y `comprobar()`
   sale antes por dos `return` cuando no hay velas. El canal `avisos` de `validar_paquetes` existía
   desde F10 y **nunca se había usado**: se estrena aquí.
3. **El ancla, `knowledge/cases/kit/anclas.yaml`**, con el patrón de `preregistro_blob` (ADR-0033)
   y sus tres requisitos: vive **fuera** del fichero que ata; es el sha del **blob** y no de un
   commit —`ventanas.yaml` tiene ya dos commits (`6266738` y el de ADR-0035), y un ancla de commit
   lo habría dado por alterado sin estarlo—; y **re-anclar es explícito**
   (`botsito kit anclar --sesion <s> --reanclar`), con su diff en otro fichero. **No depende de que
   existan etiquetas**: ese `continue` es precisamente lo que deja sin atar el período en el que
   hace falta.
4. **`mover_sesion`** arrastra ahora el config congelado además de los datasets (ADR-0035 §7 tenía
   el mismo agujero un escalón más abajo).

## 5. Lo medido después

| qué | resultado |
|---|---|
| `kit check` de la sesión 1 | **idéntico a la línea base** con `diff`, exit 0 |
| `config.yaml` editado a 6/3/3/2 | sesión 1 **idéntica**, exit 0; `knowledge validate` exit 0 con el AVISO de deriva nombrando `particiones` |
| mutante sobre `particiones` del bloque congelado | `kit check` exit 1, `ERROR: particiones.yaml difiere` (y el ancla también) |
| mutante sobre `anclajes_candidatos` del bloque congelado | `knowledge validate` **exit 1**, `ERROR: ventanas.yaml: editado en el arbol de trabajo … y no coincide con su ancla`. **Antes daba exit 0** |

La segunda fila es la que desbloquea septiembre: editar `config.yaml` ya no rompe la sesión 1.

## 6. Los tests, que ven fallar el defecto

- `test_los_cupos_del_paquete_salen_del_paquete_y_editarlos_se_ve` (unit): el paquete se recompone
  con el bloque congelado; editar los cupos DENTRO del congelado es ERROR con `celebrada` en los dos
  valores; sin bloque `config:` es PROBLEMA, no aviso.
- `test_el_ancla_ata_ventanas_aunque_no_cambie_la_asignacion` (contract): el agujero en su forma
  mínima —se comprueba explícitamente que `particiones.yaml` NO cambió, que es el caso que se
  escapaba.
- `test_un_paquete_sin_ancla_no_pasa_y_reanclar_es_explicito` (contract): sin ancla no se valida;
  anclar es idempotente; re-anclar sin `--reanclar` sale con 1.
- `test_particiones_inmutables_tras_el_etiquetado` **cambia de significado a propósito**: donde
  afirmaba que sin etiquetas todo valía (`== ([], [])`), ahora exige que tocar la asignación se vea
  igual. Y que commitear la reasignación no la lava, porque el ancla vive fuera.
- `test_paquete_determinista_y_check` deja de exigir «config.yaml cambio» y exige lo contrario.

## 7. Lo que NO se ha hecho

- **No se han descargado las velas de septiembre ni se ha sorteado nada.** Esta rama desbloquea los
  cupos; el mes es el paso siguiente.
- **No hay cupos por paquete** y se decidió que no hacen falta: editar `config.yaml` antes de cada
  `kit build` basta, porque cada paquete guarda el suyo —y eso solo es seguro con el ancla puesta—.
  Un `--cupos` dejaría la decisión sin fichero versionado y sin `Fuente:`, y una sección por sesión
  choca con `config_desde_doc`, que exige las claves exactas.
- **La guardia de ancestro sigue emparejando por sesión y no por caso.** Es deuda aparte, vigente, y
  sigue teniendo que arreglarse ANTES de la primera etiqueta. Lo que esta rama quita es la
  dependencia del ancla respecto de ella.
- `lectura_de_velas` sigue leyendo el `config.yaml` de hoy para el prefijo: con los datasets
  congelados pasados no cambia lo que declara, pero es el último hilo suelto del mismo patrón.
  Anotado como deuda.

## 8. Qué debe decidir el usuario

Validar la rama. Y después, con `config.yaml` ya editable, decidir **los cupos de septiembre**: son
14 días laborables y el reparto sale de una decisión con `Fuente:`, no de dejar los 40 de mayo.

## 9. Cómo comprobarlo

```
uv run botsito kit check --sesion 2026-09-09-sesion-01        # identico a la linea base
uv run botsito knowledge validate                              # exit 0
uv run pytest tests/unit/test_kit.py tests/contract/test_kit_particiones.py -q
git diff fd2b899 -- knowledge/cases/kit/config.yaml            # solo comentarios
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
