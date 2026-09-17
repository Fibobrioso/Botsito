---
status: ACTIVE
date: 2026-09-17
phase: post-F13 (extrae F14 D4)
---

# 0033 · La guarda y la puerta del holdout: qué vigilan, por dónde se abre y cómo se autoriza

## Decision

1. **Guarda de tests, para cualquier llamante.** Un hook de auditoría de Python
   (`tests/guarda_holdout.py`), encendido en todos los tests por la fixture `autouse`
   `holdout_guard`, lanza `LecturaDeHoldout` ante cualquier apertura de
   `knowledge/cases/holdout/{1,2,3}/**` que no sea su `README.md`. Qué cuenta:
   - los eventos `open` (que cubre `open`, `Path.read_*`, `os.open` e `io.FileIO`),
     `shutil.copyfile` y `_winapi.CopyFile2`. **Copiar es leer**;
   - listar nombres (`os.listdir`, `os.scandir`) **no** cuenta.

   La excepción hereda de `BaseException` y queda anotada antes de lanzarse: si un test la traga,
   la fixture falla igual al terminar. Solo un test marcado `provoca_holdout`, que apunta la raíz a
   un holdout sintético, puede dispararla.
2. **Una puerta en `src/`, `botsito.cases.holdout`**, que es el único módulo que puede nombrar la
   carpeta del holdout (contrato por grep). Todo lo que ABRE (ADR-0021 §1) pasa por `abrir()`:
   - leer un fichero de `holdout/{1,2,3}/` (`leer_fichero`);
   - usar el VALOR de un `LABEL_CASE` cuyo caso está asignado a una partición reservada.
     `kit kappa` los excluye sin parsearlos y lo dice, y dice junto al kappa sobre cuántas
     unidades y cuántos casos lo calculó -un kappa alto sobre pocos casos no significa nada-;
     `--incluir-holdout` pasa por la puerta. Excluir y no negarse entero, por decisión del
     consultor: negarse dejaría el kappa inservible hasta abrir un holdout, y el kappa sirve para
     cazar deriva de etiquetado ANTES de eso.
     `feedback trace` no IMPRIME ni el valor ni el literal de un caso reservado: los oculta. Fue
     la segunda via, encontrada al revisar quien mas mostraba `valor_resultante`.
3. **La frontera es usar el valor, no cargar el fichero.** `knowledge validate`, `feedback pending`
   y la guardia de ancestro cargan todos los registros y no pasan por la puerta: no leen ninguna
   etiqueta.
4. **Las velas de mercado no pasan por la puerta.** Construir o comprobar un paquete exige leer
   las de todos los días del universo, reservados incluidos, y eso no es abrir (ADR-0021 §1). Lo que
   se exige es **declararlo**: `kit build` y `kit check` imprimen líneas `LECTURA:` con los datasets
   leídos y **cuántos** días reservados se leen y de qué partición
   (`LECTURA: 24 dias reservados cuyas velas se leen: holdout-1 8, holdout-2 8, holdout-3 8`),
   **sin fechas**, sin cifras de velas y sin precios. Recuento y no fechas por decisión del
   consultor (2026-09-17): las fechas ya están en `particiones.yaml` para quien las quiera, la
   lectura es siempre la misma, y esa salida puede acabar delante del trader, a quien la hoja le
   oculta esos días por contrato. `check` lo declara antes de leer; `build`, después, porque qué días son
   reservados solo se sabe al construir.
5. **La autorización es un fichero commiteado por partición**,
   `docs/validation/AUTORIZACION-<partición>.md`, con `particion`, `autorizado_por`, `fecha`, `adr`
   (un ADR que exista) y **`preregistro_blob`**. La puerta exige además
   `docs/validation/PREREGISTRO.md` **commiteado y relleno**. «Relleno» es mecánico: sin la marca
   `SIN RELLENAR` con la que nació. Los dos tienen que estar en HEAD tal como están en el árbol:
   lo que no está en git no autoriza. Una clave repetida cierra.
6. **`preregistro_blob` fija QUÉ pre-registro se aprobó** (añadido el 2026-09-17, al validar): el sha
   del BLOB de `PREREGISTRO.md` que se autoriza, el que da
   `git rev-parse HEAD:docs/validation/PREREGISTRO.md`. La puerta lo compara con el blob del
   PREREGISTRO commiteado, y si no coincide cierra: «el pre-registro cambió después de autorizar, y
   hace falta una autorización nueva». Sin él se podía rellenar, autorizar, abrir y después cambiar
   los umbrales, y la autorización seguía valiendo con el fichero commiteado y relleno.
   **El blob y no el commit** porque lo que se aprueba es un contenido. El sha del blob cambia con
   cualquier byte del fichero y con nada más: otro commit que no toque el PREREGISTRO no lo mueve.
   Sobrevive a un rebase o a un merge, y se compara directamente. El sha de un commit fija un
   instante: habría que buscar el fichero dentro de él, y un rebase lo deja apuntando a nada.

## Problema que resuelve

- **La guarda era un stub.** ADR-0001 y ADR-0021 decían que el holdout es ilegible «con guarda en
  tests», y `tests/conftest.py` devolvía `None` desde F10.
- **Aunque se hubiera implementado como estaba prometida, no habría visto nada.** La revisión de
  diseño registró cada apertura de la suite entera: ninguna lleva `botsito.spec` ni `botsito.domain`
  en la pila. `domain` no hace E/S, y quien abre físicamente es `comun.yaml_estricto`.
- **La CLI no tenía ninguna guarda.** El 2026-09-13, `kit check` leyó dos veces las velas de los 24
  días reservados sin decirlo en la salida (`HOLDOUT-EXPOSICIONES.md`).
- **Nada comprobaba ADR-0021 §3.** Nada impedía leer la etiqueta de un día reservado: el kappa las
  leía todas.
- **La obligación 6 del 2026-09-17 prohibía `kit build` y `kit check` con `data/`**, y eso impedía
  construir el paquete de la sesión 2.

## Alternativas consideradas

1. **Hook de auditoría para los tests + puerta en `src/` + declaración en la salida + fichero de
   autorización** (elegida).
2. **`monkeypatch` de `builtins.open`/`Path.open`** en vez del hook.
3. **Guarda restringida a `spec` y `domain`**, como prometía el stub.
4. **Autorización por variable de entorno** (como `BOTSITO_ALLOW_MAIN`) o por flag.
5. **Que la puerta cubra también las velas.**

## Por que elegimos esta opcion

Porque cada pieza está medida:
- **El hook cuesta ~3 µs por apertura.** Sobre la suite completa, la diferencia no se distingue del
  ruido (245 y 231 s sin hook, 230 y 228 s con él); la suite de pytest dentro de `make check` tardó
  242 s en esta rama y entre 238 y 246 s en la anterior.
- **Ve todas las vías de lectura**, copias de Windows incluidas, y los tests lo prueban una por una.
- **La puerta vive en un solo módulo** que un grep puede vigilar.
- **Un fichero commiteado** con autor, fecha y ADR es difícil de crear sin querer y queda en
  `git log`.

## Por que descartamos las demas

- **(2) monkeypatch**: medido, se le escapan `os.open`, `io.FileIO`, `shutil.copy2` y
  `numpy.loadtxt`; y si solo se envuelve `builtins.open`, también `pathlib`, que es la vía real de
  lectura del proyecto.
- **(3) Solo `spec` y `domain`**: no protege nada (arriba). Los que leerán y medirán son `cases`, el
  motor, la validación y la CLI.
- **(4) Variable de entorno o flag**: una variable se deja puesta sin querer y no queda en ningún
  sitio. Un flag se teclea. Las dos se activan sin dejar rastro de quién autorizó ni con qué ADR.
- **(5) Puerta sobre las velas**: sin sesión 2. Qué días son reservados depende de cuáles entran en
  el universo, y eso de sus velas (`universo()` descarta los días con menos de `min_velas`); además,
  la unidad de lectura es el fichero mensual.

## Lo que esto NO cubre, y queda declarado

- **Lo que lee un subproceso** (`git show`, la CLI lanzada en otro proceso) no lo ve el hook de los
  tests. La CLI tiene su propia puerta, y el hook no la sustituye.
- **Las etiquetas que no viven en `knowledge/cases/holdout/`.** Los `LABEL_CASE` están en
  `knowledge/feedback/` y los cubre la puerta del valor. El detalle por operación del backtest de
  mayo está en el corpus: ningún código lo lee hoy (grep: ni xlsx ni pandas en `src/`), y
  `corpus inventory` solo hashea sus bytes. El día que F14 escriba la ingesta, pasa por la puerta.
- **Medir una cifra del bot sobre días reservados** (la otra mitad de ADR-0021 §1): el motor no
  existe. F24 y F26 llaman a `abrir()` antes de medir.
- **Que el ADR de la autorización diga de verdad qué se mide y contra qué umbral** no es
  mecanizable: se comprueba que exista, no lo que dice.
- **Volver al contenido aprobado reabre.** Si los umbrales se cambian y después se devuelven byte a
  byte a lo aprobado, el blob vuelve a coincidir y la puerta vuelve a abrir: el contenido es otra vez
  el aprobado. Lo que el pre-registro protege -que la medida se haga con los umbrales aprobados- se
  sostiene; que nadie los tocara entretanto lo dice `git log`, no la puerta.
- **Un test legítimo de F26 que lea holdout real** no tiene hoy vía en la guarda de tests. La
  diseña F26, ligada a esta misma autorización.

## Impacto

- ADR-0001 («`knowledge/cases/holdout/` es ilegible para `spec/` y `domain/`») queda ampliada: es
  ilegible para cualquier llamante durante los tests. Lleva una nota.
- ADR-0021 lleva una nota que apunta aquí. Su §3 pasa a tener mecanismo.
- `docs/validation/HOLDOUT-EXPOSICIONES.md`, obligación 6: reescrita. Ya no prohíbe ejecutar el kit
  con datos; prohíbe abrir sin autorización, y la CLI declara lo que lee.
- `docs/plan/features/F14-case-library.md`: D4 y el criterio 3 quedan hechos aquí.
- `knowledge/spec/` no se toca: spec 12.0.0, mismo hash.

## Fecha / fase

2026-09-17, rama `trabajo/guarda-de-holdout` (revisión de diseño con dos agentes antes de programar).

## Estado

ACTIVE
