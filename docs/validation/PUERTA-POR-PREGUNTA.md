# La puerta es de una pregunta, no de una versión del pre-registro

Rama `trabajo/puerta-por-pregunta`, desde `3bc31f9` (tag `stable/F13-septiembre-sorteo`). Sin tocar
main, sin merge, sin tag, sin push. **`PREREGISTRO.md` intacto**, con su marca `SIN RELLENAR` y su
mismo blob; **cero ficheros `AUTORIZACION-*.md` en el árbol**; nada abierto. Sin tocar
`knowledge/spec/`, `evidence/`, `feedback/`, ni los repartos y anclas ya commiteados.

Es el último momento en que este mecanismo se podía cambiar sin reescribir una historia que ya
concedió un permiso: hoy no hay ni una firma.

## 1. La línea base

`kit check --sesion 2026-09-09-sesion-01` guardada antes de nada. **Resultado: salida IDÉNTICA** con
`diff` al final de la rama.

## 2. El defecto, medido

```
apertura 1:  motivos=[] -> ABRE
apertura 2:  motivos=[] -> ABRE
apertura 50: motivos=[] -> ABRE
tras 50 aperturas -> git status: ''  |  versiones del fichero de autorizacion: 1
```

Cincuenta aperturas con la autorización válida y el pre-registro intacto: el estado del repositorio
es **idéntico byte a byte** antes y después. La autorización era de un solo uso **por versión del
pre-registro**, no por pregunta.

**La hipótesis del brief está tumbada**, y el motivo es aritmético: el historial de git de
`AUTORIZACION-<particion>.md` no distingue «firmada una vez y usada una» de «firmada una vez y usada
cincuenta», porque son el mismo árbol y el mismo commit. `abrir` es pura —decisión 1— y una función
pura del estado no puede dar dos respuestas sobre el mismo estado.

De ahí que **el criterio 2 original fuera insatisfacible** y el consultor lo reescribiera. La
versión que se ha implementado es: abrir → el comando gasta → la segunda apertura se niega → **y una
re-firma citando la pregunta ya gastada también**.

### Qué se pudo enseñar en rojo y qué no

**El paso 4 se midió pasando antes del arreglo**, que es el que de verdad muerde:

```
re-firma sobre el preregistro con P1 GASTADA -> motivos de HOY: []
```

Los pasos 1-3 **no se pueden enseñar en rojo**, y se dice aquí en vez de fabricar un rojo: hoy no
existe el campo `pregunta` ni la sección `## Preguntas`, así que el estado de partida del que salen
no es representable con el código anterior. Lo que sí se enseña de aquel estado es la medición de
arriba: cincuenta aperturas.

## 3. Lo que se construyó

1. **La autorización cita la pregunta** (`pregunta` en `_CAMPOS_AUTORIZACION`), y el pre-registro
   gana una sección `## Preguntas` con el estado en la misma línea. Dos motivos de cierre nuevos:
   la pregunta no existe, o ya está gastada. Se comprueban contra el texto del pre-registro que
   `motivos_de_cierre` ya tenía en la mano: **ni una llamada más a git**.
2. **`abrir(repo, particion, pregunta)`**: `para_que` era una frase que sólo salía en el mensaje de
   error —cuando la puerta **abría**, no dejaba rastro en ninguna parte—. Ahora es el id y **se
   compara** con el que la autorización cita.
3. **`gastar_pregunta`**, que llama el comando y nunca `abrir`. `kit kappa --incluir-holdout` exige
   `--pregunta <id>` y el orden es **comprobar → gastar → leer**.
4. **`casos_reservados` grita** (`RepartoIlegibleError`) en vez de saltarse un reparto ilegible.
5. **`leer_fichero` decide sobre la ruta resuelta** y niega por defecto dentro del directorio
   guardado.

### Por qué se gasta antes de leer

Los dos modos de fallo no son simétricos: *gastada y no leída* cuesta volver a pre-registrar;
*leída y no gastada* es el defecto que la rama cierra.

**Consecuencia mecánica, que era lo que había que mirar:** empuja la comprobación al principio del
comando. **No resultó caro ni feo**, y el motivo está medido: `leer_fichero` **no tiene ningún
llamante de producción** —sólo tests—, así que el único comando afectado es `kit kappa`, donde las
tres fases quedan seguidas y a la vista. `leer_fichero` conserva su llamada a `abrir` porque es un
lector suelto sin comando alrededor: es la última línea de defensa, no el sitio donde se gasta.

### La caducidad automática, que no se «arregla» luego

Gastar una pregunta cambia el blob del pre-registro e **invalida todas las autorizaciones vivas**.
Es deseable y va escrito en la enmienda. **Firmar no invalida nada: sólo gastar o editar.**

Medido: en cuanto el comando escribe la marca, la puerta ya está cerrada **antes del commit**.

## 4. Hueco 2 — `casos_reservados` grita

Medido con yaml roto de verdad en repositorio sintético: devolvía un mapa incompleto
**indistinguible de uno completo**; sobre el repo real, un `particiones.yaml` ilegible bajaba de 34
casos reservados a 24, y `feedback trace` y `kit kappa` seguían con exit 0 sin mencionar el fichero.

Lo que decide: **ningún comando que deba sobrevivir a un paquete a medio escribir pasa por ahí** —ni
`kit build`, ni `kit check`, ni `knowledge validate`, ni un clon sin `data/`—. Los dos únicos
llamantes usan el mapa para decidir **qué no mirar**.

**El comentario que delegaba en `knowledge validate` se ha borrado, no suavizado**, porque era falso:
un `BORRADOR_2026-09/` —carpeta que el glob ve y el validador de su camino no reconoce— daba exit 0
en todas partes con sus reservados invisibles. Y el atenuante del test no bastaba: un truncado que
siga siendo YAML válido pierde ocho casos **y el test pasa**.

**Comandos que pasan a fallar** (inventario completo de llamantes):

| llamante | antes | ahora |
|---|---|---|
| `botsito feedback trace <id>` | ocultaba de menos, exit 0 | `ERROR:` nombrando el fichero, exit 1 |
| `botsito kit kappa` (y `--incluir-holdout`) | excluía de menos, aviso con cifra falsa | falla nombrando el fichero |
| `kit build`, `kit check`, `knowledge validate`, clon sin `data/` | — | **no lo llaman: no cambian** |

## 5. Hueco 3 — el camino de fidelidad no necesita lector guardado

Medido: `knowledge/cases/holdout/{1,2,3}/` contiene **cuatro README y nada más**, y
`knowledge/cases/fidelidad/` sólo tiene asignación, que ADR-0036 declara que no es abrir. El material
reservado del camino de fidelidad vive en `knowledge/feedback/` —que cubren `casos_reservados` y
`trazar(ocultar=)`— y en `corpus/`, que ningún código lee. **ADR-0033 ya lo declaraba** en «Lo que
esto NO cubre».

**El disparador queda escrito**, en la enmienda y en Technical Debt: el día que exista bajo
`knowledge/cases/<camino>/` un fichero con una etiqueta, un precio o el detalle por operación de un
día asignado a una partición reservada, ese camino necesita lector guardado **antes de que ese
fichero se commitee**.

## 6. El bypass, que no estaba en el brief

```
antes:  LEE    knowledge/cases/holdout/../holdout/2/caso-secreto.yaml -> valor: SECRETO-2
ahora:  NIEGA
```

El `..` hacía que el primer tramo no fuera `1|2|3`, así que **no se llamaba a `abrir`**, mientras
`read_text` sí lo resolvía. No se ha parcheado buscando `".."`: se resuelve la ruta y se decide sobre
lo resuelto. Y ahora niega por defecto: una partición `4/` que aparezca mañana cae del lado seguro.

## 7. Una corrección que me toca a mí

Ayer escribí en el test de la puerta que afirmaba la unión exacta *«y caza lo que la otra no veía:
que un camino nuevo quede fuera del glob»*, y ADR-0036 §Impacto lo repetía. **Era falso**, medido con
un tercer camino `knowledge/cases/marzo/` con un `holdout-2` dentro:

```
el caso del tercer camino esta? False
la igualdad del test se cumple? True
```

Los dos lados usaban `repartos_commiteables`. El docstring se ha **retirado**, no suavizado, y el
par `{"kit","fidelidad"}` pegado a mano se ha ido. En su lugar hay una enumeración **que no pasa por
el glob** —sale del disco— y que sí se rompe con ese tercer camino. ADR-0036 lleva la corrección con
su medición.

## 8. Los tests

- `test_una_pregunta_gastada_no_se_vuelve_a_abrir`: los cuatro pasos, incluido el 4 (la re-firma).
- `test_abrir_exige_la_pregunta_que_la_autorizacion_cita`.
- `test_gastar_una_pregunta_que_no_esta_o_ya_gastada`.
- `test_el_lector_decide_sobre_la_ruta_resuelta`: el bypass del `..` y la partición `4/`.
- `test_un_reparto_ilegible_no_se_salta_en_silencio`: con el yaml roto **de verdad**.
- Tres casos parametrizados nuevos (pregunta inexistente, gastada, ausente del fichero).
- `test_kappa_desde_registros_y_cli` recorre **el ciclo entero por CLI**: sin `--pregunta` se niega;
  con ella y sin autorización se niega; con todo en orden abre; **y la segunda vez no**.
- **`test_con_todo_en_orden_se_abre` sigue verde** (criterio 5). Hay un camino que abre de verdad y
  pasa: firmar → abrir → gastar → re-firmar para la siguiente pregunta.

## 9. Lo que NO se ha hecho

- **El agujero de `excluir`** en `kappa_entre_sesiones` sigue abierto, y con esta enmienda es peor
  de explicar: la autorización dirá «P1 sobre holdout-2» y el código leerá los tres cubos. Sigue
  siendo **bloqueante para abrir**, ahora también escrito en la enmienda.
- **Quien llame `abrir()` en un bucle** sin gastar entre medias abre N veces. La puerta comprueba la
  autorización, no cuenta aperturas. Declarado en la enmienda.
- **`EXPOSICIONES` sigue sin mecanismo.** El comando que gasta está a una línea de añadir también la
  fila de exposición; no se ha hecho aquí.

## 10. Qué debe decidir el usuario

Validar la rama. Y antes de la primera autorización real —que será `fidelidad-1`, con los 10 días de
septiembre—: cerrar el agujero de `excluir`.

## 11. Cómo comprobarlo

```
uv run botsito kit check --sesion 2026-09-09-sesion-01     # identico a la linea base
uv run pytest tests/unit/test_puerta_holdout.py -q
uv run pytest tests/unit/test_kit.py -k kappa -q
git status --short docs/validation/PREREGISTRO.md          # vacio
ls docs/validation | grep -i autoriz                        # nada
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
