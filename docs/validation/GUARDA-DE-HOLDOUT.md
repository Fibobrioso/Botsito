# La guarda del holdout — INFORME DE VALIDACIÓN

**Rama:** `trabajo/guarda-de-holdout` (rama de trabajo sin número propio, MASTER_PLAN §F), desde `main` en `d7db83f`
**Cierre previsto:** tag `stable/F13-guarda`
**Decisión:** ADR-0033, con notas en ADR-0001 y ADR-0021
**Extrae de F14:** D4 («la guarda del holdout: qué vigila exactamente y cómo») y el criterio de aceptación 3
**spec_version:** 12.0.0 sin tocar, con el mismo hash
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 1. Por qué existe esta rama

La obligación 6 que se añadió el 2026-09-17 a `HOLDOUT-EXPOSICIONES.md` prohibía ejecutar `kit build`
y `kit check` con `data/` presente mientras no hubiera una guarda. Leída al pie de la letra, impedía
construir el paquete de la sesión 2 para siempre. Y la guarda que tenía que existir era un stub desde
F10. Esta rama pone el mecanismo en su sitio:
- la guarda de tests, implementada y vista saltar;
- una puerta que se niega a abrir material de holdout sin lo que exige ADR-0021 §3;
- la CLI declarando qué velas de días reservados lee;
- y la obligación reescrita.

No se ha abierto ningún holdout. `PREREGISTRO.md` sigue vacío. No se ha ejecutado `kit check`,
`kit build` ni `kit kappa` sobre el repositorio real, ni se ha leído `data/`. `knowledge/spec/`,
`knowledge/evidence/` y `knowledge/feedback/` no se han tocado.

## 2. El §0, verificado antes de aceptarlo

**No se puede construir un paquete sin leer las velas de los días reservados.** Medido en el código,
no razonado:

- **Qué día es reservado lo decide `asignar()`** (`cases/particiones.py`). Ordena los casos por
  `clave_orden(seed, id)` y llena los cupos en ese orden. No usa el contenido de las velas, pero sí
  qué casos forman el universo.
- **Qué casos forman el universo lo deciden las velas.** `construir_caso` (`cases/ventanas.py`)
  excluye un día si su ventana cae fuera del dataset o tiene menos de `min_velas`, y un día excluido
  desplaza toda la asignación. Es circular: no se sabe qué días son reservados sin leer los de todos.
- **La unidad de lectura es el mes.** `universo()` llama a `cargar_serie` una vez por dataset, y
  `cargar_ventana` lee el fichero mensual entero. Leer un solo día `dev` de mayo ya lee los trece
  reservados.
- **`kit check` tampoco se libra.** Sabe qué días son reservados sin leer velas, porque
  `particiones.yaml` ya está escrito, pero para verificar tiene que recomponer, y eso lo lee todo.

El brief se sostiene. Por eso las velas no pasan por la puerta.

## 3. La revisión de diseño (dos agentes, antes de programar)

**A** (Opus): mecanismo de la guarda de tests, coste de `autouse` y quién abre. Midió sobre la suite
real con un hook de registro que no bloqueaba, y con un prototipo en el scratchpad. **B** (Sonnet):
alcance de la puerta, autorización y ADR, todo por grep.

### Las cuatro preguntas

**1 · Mecanismo.** Hook de auditoría (`sys.addaudithook`):
- **Vías de lectura:** ve `open`, `Path.read_*`, `os.open`, `io.FileIO` y numpy. Las copias de
  `shutil` en Windows no emiten `open` sino `_winapi.CopyFile2` o `shutil.copyfile`, y hay que
  escucharlas.
- **Coste:** ~3 µs por apertura. En dos pares alternos de la suite completa: 245 y 231 s sin hook,
  230 y 228 s con él, dentro del ruido (revisión A). En esta sesión, la suite de pytest dentro de
  `make check` tardó 242 s en esta rama y entre 238 y 246 s en la rama anterior, que no tenía hook.
- **Sin vuelta atrás:** un hook no se puede quitar, así que consulta un estado que la fixture
  enciende en cada test.
- **Frente a `monkeypatch`:** medido, se le escapan `os.open`, `io.FileIO`, `shutil.copy2` y
  `numpy.loadtxt`.
- **Frente a una capa propia:** no había nada que envolver; ninguna lectura de la carpeta en `src/`.

**2 · Alcance de la puerta, comprobable con grep:**
- **Pasa por ella** toda lectura de `knowledge/cases/holdout/{1,2,3}/**` que no sea su `README.md`,
  y el VALOR de un `LABEL_CASE` cuyo caso está asignado a una partición reservada.
- **No pasan** las velas, `knowledge validate`, `feedback pending` ni la guardia de ancestro: cargan
  registros, pero no usan el valor de la etiqueta. La frontera es usar el valor, no cargar el fichero.
- **Dos contratos lo fijan:** solo `cases/holdout.py` nombra la carpeta, y `parsear_etiqueta` y
  `etiquetas_de_registros` solo se llaman desde el camino que excluye reservados. Meter la ruta del
  holdout en `cli.py` hace fallar el primero (probado).

**3 · Autorización:** un fichero commiteado por partición, `docs/validation/AUTORIZACION-<partición>.md`,
con `particion`, `autorizado_por`, `fecha`, `adr` y, desde la validación, `preregistro_blob` (§11). Además, `PREREGISTRO.md` commiteado y sin la marca
`SIN RELLENAR` con la que nació. Los dos tienen que estar en HEAD tal como están en el árbol. Se
descartó imitar `BOTSITO_ALLOW_MAIN`: una variable de entorno se deja puesta sin querer y no deja
rastro de quién autorizó.

**4 · ADR propio (0033).** ADR-0021 decide qué es abrir y quién lo autoriza, pero ningún mecanismo:
delegaba en F14. Esta rama decide el alcance a cualquier llamante (y enmienda la frase de ADR-0001),
los eventos que cuentan, la frontera del valor, la autorización y lo que no cubre.

### Hallazgos que el brief no vio, y qué se hizo

| Hallazgo | Quién | Qué se hizo |
|---|---|---|
| **La guarda prometida, restringida a `spec` y `domain`, no habría visto nada.** Ninguna apertura de la suite lleva esos paquetes en la pila: `domain` no hace E/S, y quien abre físicamente es `comun.yaml_estricto` | A, medido | La guarda vigila a cualquier llamante. ADR-0001 lleva la nota |
| **Las etiquetas del holdout no viven en `knowledge/cases/holdout/`**: los `LABEL_CASE` están en `knowledge/feedback/` y el detalle por operación, en el xlsx del corpus. Una guarda por ruta es necesaria y no suficiente | A y B | La puerta cubre también el VALOR de las etiquetas de casos reservados |
| **`kit kappa` leía y parseaba las etiquetas de todos los casos, reservados incluidos** | B | Las excluye sin parsearlas y lo dice. `--incluir-holdout` pasa por la puerta. `etiquetas_de_registros` exige `excluir` como argumento obligatorio |
| **Tres tests abrían o copiaban el holdout**: `test_no_crlf_in_tracked_text_files` los abre, y `test_kit` y `test_spec_docs_generados` copian `knowledge/` con `copytree`. Hoy solo tocan los README, pero caerían el día que F14 escriba el primer caso | A, medido | Excluyen el contenido de `holdout/{1,2,3}` |
| **La excepción no puede heredar de `Exception`**: `cases/paquete.py` y la CLI convierten `OSError` en errores del kit y la tragarían | A | `BaseException`, anotada antes de lanzarse |
| **`feedback trace <caso>` imprimía el valor de la etiqueta** y el literal del registro corregido, para cualquier caso: una segunda vía para abrir un día reservado sin pasar por la puerta | encontrado al implementar, revisando quién más mostraba `valor_resultante` | `trazar` los oculta para los casos reservados; los `dev` se ven igual. Test |

**Descartado de la revisión:** un fichero de registro de ejecuciones de la CLI (el brief lo dejaba como
opcional). Sería una segunda tabla compitiendo con `HOLDOUT-EXPOSICIONES.md`, y la salida de la CLI
ya declara lo que lee.

## 4. Qué se hizo, pieza por pieza

| Pieza | Hecho | Dónde |
|---|---|---|
| **1 · guarda de tests** | Hook de auditoría + fixture `autouse`. Salta con cualquier apertura de `holdout/{1,2,3}/**` salvo su README; copiar cuenta y listar no. `BaseException`; si un test no marcado la traga, falla al terminar. Solo un test `provoca_holdout` puede dispararla | `tests/guarda_holdout.py`, `tests/conftest.py`; marcador en `pyproject.toml` |
| **1 · verla saltar** | Salta por cada vía (`read_text`, `read_bytes`, `open`, `os.open`, `io.FileIO`, `shutil.copy2`, `shutil.copyfile`) contra un holdout sintético, y contra una ruta que no existe en el real, sin crear nada: el evento se audita antes de abrir. No salta con README, listar ni `particiones.yaml` | `tests/unit/test_guarda_holdout.py` |
| **2 · puerta** | `abrir()` se niega sin PREREGISTRO relleno y sin autorización commiteada, y nombra ADR-0021 §3. Con el PREREGISTRO real se niega para las tres particiones. Con todo en orden, abre, siempre en repos temporales. Cada motivo de cierre, por su cuenta. Una autorización sin commitear, o un PREREGISTRO cambiado tras commitearlo, no autoriza | `src/botsito/cases/holdout.py`, `tests/unit/test_puerta_holdout.py` |
| **2 · etiquetas** | `kit kappa` excluye los casos reservados sin leer su valor y lo dice; `--incluir-holdout` se niega hoy y, autorizado en un repo de prueba, da las mismas 10 unidades de antes. `feedback trace` los oculta | `cases/paquete.py`, `cases/kappa.py`, `feedback/modelo.py`, `cli.py`; `test_kit.py::test_kappa_desde_registros_y_cli` |
| **2 · contratos** | Solo la puerta nombra la carpeta; el valor de una etiqueta solo se lee por el camino que excluye reservados | `tests/contract/test_import_contracts.py` |
| **3 · declaración** | `kit build` y `kit check` imprimen `LECTURA:` con los datasets leídos y CUÁNTOS días reservados se leen por partición, sin fechas (decisión del consultor, §8), sin cifras ni precios. `check` lo declara antes de leer; `build`, al terminar, porque qué días son reservados solo se sabe al construir. Sin datos, no imprimen nada | `cases/paquete.py:lectura_de_velas`, `cli.py`; test sobre la salida en el kit sintético |
| **§2 · obligación 6** | Reescrita: leer velas no es abrir y el paquete no se construye sin hacerlo; abrir exige autorización; la CLI declara lo que lee. La fila del 2026-09-13 no cambia | `docs/validation/HOLDOUT-EXPOSICIONES.md` |
| **§3 · F14** | D4 y el criterio 3 anotados como hechos aquí; a F14 le queda que su ingesta del xlsx pase por la puerta | `docs/plan/features/F14-case-library.md` |

## 5. Lo que cambió respecto al brief, y por qué

| Pedía el brief | Se hizo | Motivo |
|---|---|---|
| La guarda que F14 prometió: «módulos bajo `botsito.spec` o `botsito.domain`» | Cualquier llamante | Restringida a esos dos no ve nada (§3) |
| Puerta sobre «ficheros de `holdout/**` y `LABEL_CASE` de días reservados» | Sobre los ficheros y sobre el USO del valor de la etiqueta, no sobre cargar los registros | Si cubriera la carga, `knowledge validate` y la guardia de ancestro dejarían de funcionar sin autorización |
| Autorización «explícita del usuario» + PREREGISTRO no vacío | Fichero commiteado por partición con autor, fecha y ADR existente, más PREREGISTRO commiteado sin la marca `SIN RELLENAR` | ADR-0021 §3 pide además un ADR; lo que se puede comprobar de él es que exista, no lo que dice |
| No estaba en el brief | `feedback trace` oculta la etiqueta de los casos reservados | Era una segunda vía para abrir (§3) |
| Anotar las lecturas en un fichero, si salía barato | No se hizo | Competiría con `HOLDOUT-EXPOSICIONES.md` (§3) |

## 6. Lo que esto NO cubre, y queda declarado

- **Lo que lee un subproceso** (`git show`, la CLI lanzada en otro proceso) no lo ve el hook de los
  tests. La CLI tiene su propia puerta.
- **El detalle por operación del backtest de mayo**: ningún código lo lee hoy (ni xlsx ni pandas en
  `src/`, grep), y `corpus inventory` solo hashea sus bytes. La ingesta de F14 tiene que pasar por la
  puerta.
- **Medir una cifra del bot sobre días reservados**, la otra mitad de ADR-0021 §1: el motor no
  existe. F24 y F26 llaman a `abrir()` antes de medir.
- **Que el ADR de la autorización diga de verdad qué se mide y contra qué umbral** no es mecanizable:
  se comprueba que exista.
- **Qué pre-registro se aprobó SÍ se comprueba** desde la validación: `preregistro_blob` en la
  autorización tiene que ser el blob del `PREREGISTRO.md` commiteado, o la puerta cierra (§11). Lo
  que no cubre: si los umbrales se cambian y después se devuelven byte a byte a lo aprobado, vuelve a
  abrir, porque el contenido vuelve a ser el aprobado; que nadie los tocara entretanto lo dice
  `git log`.
- **Un test legítimo de F26 que lea el holdout real** no tiene hoy vía en la guarda de tests. La
  diseña F26, ligada a la misma autorización.

## 7. La auditoría de cierre

Dos agentes en paralelo (Sonnet, solo lectura; prohibido leer `data/`, abrir el holdout o ejecutar el
kit sobre el repositorio real): uno sobre código y tests, con mutantes en repos sintéticos y
`monkeypatch`; otro sobre ADR, documentos y proceso.

**Lo que comprobaron y se sostiene.**
- **La guarda muerde de verdad.** Cargando el `conftest.py` real, un test SIN marcar que se traga
  `LecturaDeHoldout` con `contextlib.suppress(BaseException)` acaba en ERROR por el teardown de
  `holdout_guard`.
- **No hay más vías.** Un grep exhaustivo de `valor_resultante` y `respuesta_literal` en `src/` no
  encontró otra salida del valor de una etiqueta: `feedback apply` solo toca parámetros,
  `feedback pending` no imprime valores, y `knowledge validate` compara literales sin citarlos.
- **Las velas no pasan por la puerta.** `construir`, `comprobar` y `universo` no importan la puerta;
  `check` declara antes de leer y `build`, después.
- **El kappa no lee ningún valor excluido.** `etiquetas_de_registros` salta los excluidos antes de
  tocar su valor.
- **Tiempo:** la suite completa tardó 242 s.
- **La spec no se movió:** el manifiesto es idéntico byte a byte al de `d7db83f`.
- **Sin cambios** en evidencia ni en feedback.
- **Los documentos dicen lo que hace el código**, punto por punto, y ninguna fila de
  `HOLDOUT-EXPOSICIONES.md` cambió.

| Hallazgo | Gravedad | Quién | Qué se hizo |
|---|---|---|---|
| Una autorización con la clave `particion:` repetida valía por su ÚLTIMA línea: un `AUTORIZACION-holdout-1.md` con `particion: holdout-2` y después `particion: holdout-1` abría holdout-1 | media | código | **Corregido**: una clave repetida cierra la puerta. Test en los dos órdenes |
| PROJECT_STATE, «Next Feature» y el punto 3 de «Next Action» seguían llamando stub a la guarda | media | documentos | **Corregido** |
| El informe decía «`make check` tardó 242 s frente a 238 s» sin una medición citable de `make check` completo | media | documentos | **Corregido** en el informe y en ADR-0033: son los tiempos de la suite de pytest dentro de `make check` que se midieron en esta sesión (242 s aquí; 238 y 246 s en la rama anterior) |
| Sin `git` en el PATH, `motivos_de_cierre` lanzaba una excepción en vez de dar un motivo | baja | código | **Corregido**: cierra con motivo. Test |
| Un BOM al principio de la autorización rompía la primera clave (fallaba cerrado, pero con un motivo engañoso) | baja | código | **Corregido**. Test |
| El aviso del kappa contaba etiquetas reservadas ya supersedidas y habría pedido abrir una partición sin ninguna etiqueta activa | info | código | **Corregido**: cuenta sobre `activos()` |
| El test de CRLF excluía también los README del holdout, que la guarda permite leer | baja | los dos | **Corregido**: vuelve a comprobarlos |
| El índice de ADR de PROJECT_STATE ponía ADR-0033 antes que ADR-0032 | baja | documentos | **Corregido** |
| `SIN RELLENAR` se busca en todo el `PREREGISTRO.md`: uno relleno que la mencione en un comentario sigue cerrado | baja | código | **Sin cambio de lógica**, a propósito: falla del lado seguro. El mensaje dice ahora que la marca se quita de todo el fichero |

## 8. Lo que decidió el usuario (2026-09-17)

1. **La rama: validada**, con una corrección posterior (§11) antes del ritual.
2. **RECUENTO, no fechas.** La línea `LECTURA:` dice cuántos días reservados y de qué partición
   («24 dias reservados cuyas velas se leen: holdout-1 8, holdout-2 8, holdout-3 8»), sin fechas.
   Motivo del consultor: las fechas ya están en `particiones.yaml` para quien las quiera, la lectura
   es siempre la misma, y esa salida puede acabar delante del trader, a quien la hoja le oculta esos
   días por contrato. Hecho; el test comprueba además que no sale ninguna fecha de día reservado.
3. **EXCLUIR por defecto, como estaba.** Negarse entero dejaría el kappa inservible hasta abrir un
   holdout, y el kappa sirve para cazar deriva de etiquetado ANTES de eso. Y el kappa dice ahora,
   junto a su valor, sobre cuántas unidades y cuántos casos se calculó («kappa 0.600 calculado sobre
   4 unidades de 2 casos»): un kappa alto sobre ocho casos no significa nada. `kit kappa` no escribe
   ningún fichero; lo dice en su salida, que es todo lo que produce.
4. **El formato de la autorización vale, con el campo nuevo `preregistro_blob`** (§11).

## 9. Cómo comprobarlo

```
git checkout trabajo/guarda-de-holdout
make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log
uv run pytest tests/unit/test_guarda_holdout.py tests/unit/test_puerta_holdout.py -q
uv run pytest tests/contract/test_import_contracts.py -q
uv run pytest "tests/unit/test_kit.py::test_kappa_desde_registros_y_cli" -q   # LECTURA, kappa y trace
git diff d7db83f..HEAD --stat -- knowledge/spec knowledge/evidence knowledge/feedback   # vacio
uv run botsito spec check                   # spec 12.0.0, mismo hash que main
```

## 10. El ritual de cierre (lo ejecuta el usuario)

Nada de esto lo ha hecho la sesión: ni merge, ni tag, ni push. Si se ejecuta con líneas `!` en
Claude Code, **cada línea abre una shell nueva**: `BOTSITO_ALLOW_MAIN=1` va pegada al `git commit`, en
la misma línea. El merge, el tag y el push no la necesitan.

```
git checkout main
git status --short                 # vacio

git merge --no-ff trabajo/guarda-de-holdout -m "merge: la guarda del holdout, la puerta y la lectura de velas declarada"
git tag -a stable/F13-guarda -m "Guarda del holdout: hook de tests, puerta de ADR-0021 §3 y LECTURA en el kit (ADR-0033)"
git rev-parse --short HEAD

# docs(state) que toca SOLO PROJECT_STATE.md
git add PROJECT_STATE.md
git diff --cached --name-only      # SOLO PROJECT_STATE.md
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): la guarda del holdout, cerrada en main (stable/F13-guarda)"

make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log

git push origin main
git push origin stable/F13-guarda
```

Entre el merge y el `docs(state)`, `state check` falla a propósito. Si `make check` falla, no se
pushea. La CI que cuenta es la del `docs(state)`:
`curl -s https://api.github.com/repos/Fibobrioso/Botsito/commits/<sha>/check-runs`.

## 11. Hallazgo posterior al informe, y qué se hizo (2026-09-17)

**Lo encontró el consultor al validar.** La autorización exigía que `PREREGISTRO.md` estuviera
commiteado y relleno, pero no ataba QUÉ versión se aprobó. Se podía rellenar, autorizar, abrir y
después cambiar los umbrales: la autorización seguía valiendo, y el fichero seguía commiteado y
relleno. Es justo lo que un pre-registro existe para impedir.

**Qué se hizo.** Campo obligatorio nuevo en `AUTORIZACION-<partición>.md`: `preregistro_blob`, el sha
del **blob** de `PREREGISTRO.md` que se aprueba (`git rev-parse HEAD:docs/validation/PREREGISTRO.md`).
La puerta lo compara con el blob del PREREGISTRO commiteado. Si no coincide, cierra: «aprueba el
PREREGISTRO.md con blob …, y el commiteado es …: el pre-registro cambió después de autorizar, y hace
falta una autorización nueva». Si falta o no son 40 hexadecimales en minúscula, también cierra.

**Blob y no commit, y por qué.** Lo que se aprueba es un contenido:
- el sha del blob cambia con cualquier byte del fichero y con nada más; otro commit que no toque el
  PREREGISTRO no lo mueve;
- sobrevive a un rebase o a un merge;
- se compara directamente con lo que hay en HEAD.

El sha de un commit fija un instante: habría que buscar el fichero dentro de él, y un rebase lo deja
apuntando a nada. Comprobado que coincide con lo que da git: en este repositorio,
`git rev-parse HEAD:docs/validation/PREREGISTRO.md` y `git hash-object` del fichero dan el mismo sha,
y un test calcula el blob en Python y lo compara con el `rev-parse` de un repo temporal.

**Tests** (`tests/unit/test_puerta_holdout.py`, siempre en repos temporales):
- una autorización válida abre;
- cambiar un umbral del PREREGISTRO y commitearlo cierra, con el motivo;
- una autorización nueva sobre el PREREGISTRO cambiado vuelve a abrir;
- el campo ausente, mal formado (`HEAD`, 40 `A`) o con un blob que no es el commiteado cierra.

El kit sintético de `test_kit.py` autoriza con el campo.

**Lo que no cubre, declarado:** si los umbrales se cambian y después se devuelven byte a byte a lo
aprobado, la puerta vuelve a abrir, porque el contenido vuelve a ser el aprobado. Que nadie los tocara
entretanto lo dice `git log`, no la puerta.

`knowledge/spec/` sigue sin tocarse: spec 12.0.0 y el mismo hash.

## Estado
WAITING_FOR_USER_VALIDATION
