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

## Enmienda del 2026-09-21 (la puerta es de una pregunta, no de una versión)

El cuerpo de arriba **no se reescribe**. Lo que cambia se dice aquí.

ADR-0033 puso la puerta. Esta enmienda dice **de qué es la llave**.

**El defecto, medido antes de escribirlo.** `abrir()` es pura: comprueba el estado del repositorio
y vuelve. No registra nada. Con una autorización válida y el pre-registro intacto se abre **dos
veces, y cincuenta**: medido, `git status` vacío después y `rev-list --count` del fichero de
autorización en **1**. El historial de git no distingue «firmada una vez y usada una» de «firmada
una vez y usada cincuenta», porque son el mismo árbol y el mismo commit — no es una limitación de
git, es que una función pura del estado no puede dar dos respuestas sobre el mismo estado.

Lo único que volvía a cerrar era que cambiara el blob del pre-registro. Dicho con precisión: **una
autorización era de un solo uso POR VERSIÓN DEL PRE-REGISTRO, no por pregunta.** Con tres preguntas
escritas en el blob B1, una autorización anclada a B1 abría para las tres — y para una cuarta que a
nadie se le ocurrió escribir. Eso rompe lo que la puerta existe para garantizar: que **cada apertura
responde a una pregunta escrita antes de mirar**. Y lo rompía *aparentando* cumplirlo.

**1. La autorización cita la pregunta que abre.** Campo nuevo `pregunta` en
`_CAMPOS_AUTORIZACION`, y esa pregunta tiene que existir en el `PREREGISTRO.md` de HEAD con estado
`ABIERTA`. El pre-registro gana una sección `## Preguntas` con una línea por pregunta y el estado en
la misma línea — una sola fuente de verdad: una sección aparte de «gastadas» se desincroniza y
además invita a borrarla entera.

**2. `abrir` sigue siendo PURA, y `pregunta` pasa a ser load-bearing.** El tercer argumento era
`para_que`, una frase que sólo aparecía en el mensaje de error: cuando la puerta **abría** —que es
cuando importa— esa cadena no dejaba rastro en ninguna parte. Ahora es el id de la pregunta y se
compara con la que la autorización cita. El acto de abrir **declara** para qué se abre.

**3. Gastar la pregunta lo hace el COMANDO, y la gasta ANTES de leer.** `botsito kit kappa
--incluir-holdout` exige `--pregunta <id>`, y el orden dentro del comando es: comprobar la puerta →
gastar → leer. **Los dos modos de fallo no son simétricos**: «gastada y no leída» cuesta volver a
pre-registrar; «leída y no gastada» es exactamente el defecto que esta enmienda cierra. `abrir` no
escribe: una puerta que escribe se dispara en cada test y a los dos meses nadie se fía del registro
que produce.

**4. La caducidad automática es deseable y no se «arregla» después.** Gastar una pregunta cambia el
blob del pre-registro, y eso **invalida todas las autorizaciones vivas**, que hay que volver a
firmar. Es el mecanismo de ADR-0033 usado como lo que es. **Firmar no invalida nada: sólo gastar o
editar.**

Medido: en cuanto el comando escribe la marca, la puerta ya está cerrada **antes del commit**,
porque `_commiteado_y_sin_cambios` exige que el árbol coincida con HEAD. Tres motivos independientes
tapan el mismo agujero —el árbol sucio, el blob que ya no cuadra y la pregunta marcada— y sólo el
tercero sobrevive a una **re-firma**, que es donde hoy se reabría: medido, re-firmar citando una
pregunta ya gastada daba `motivos == []`.

**5. Borrar una pregunta en vez de gastarla también cierra, y ahora es irreversible como atajo.**
Confirmado midiendo: borrar la línea cambia el blob y la autorización se cierra sola. Pero eso no
aguantaba una re-firma —medido, `[]`—, y con el punto 1 esa re-firma cae por «cita una pregunta que
el pre-registro no tiene».

**6. `casos_reservados` deja de saltarse en silencio un reparto ilegible.** Lanza
`RepartoIlegibleError`. El comentario que delegaba en `knowledge validate` era **falso** para toda
carpeta que el glob ve y el validador de su camino no reconoce: medido, un `BORRADOR_2026-09/` daba
exit 0 en todas partes con sus casos reservados invisibles. Y el atenuante que existía —un test que
reimplementa el bucle sin `try`— no basta: un truncado que siga siendo YAML válido pierde ocho casos
y el test pasa. La puerta no puede responder a medias: si no puede leer la asignación, **no sabe qué
ocultar**.

**7. El lector decide sobre la ruta RESUELTA.** `knowledge/cases/holdout/../holdout/2/<fichero>`
leía material reservado **sin llamar a `abrir`** —medido—, porque el `..` hacía que el primer tramo
no fuera `1|2|3` mientras `read_text` sí lo resolvía. Tres puntos y una barra saltaban la puerta. Y
ahora niega por defecto: dentro del directorio guardado, todo lo que no sea el `README.md` de una
partición conocida pasa por `abrir`, incluida una `4/` que aparezca mañana.

**Lo que esta enmienda NO cierra, y queda dicho:**

- **El agujero de `excluir` en `kappa_entre_sesiones` sigue abierto**: tras pasar la puerta,
  `excluir` queda vacío y una autorización lee las etiquetas de todos los cubos. Está declarado como
  bloqueante para abrir en ADR-0036 §6 y en Technical Debt. Con esta enmienda es **peor de
  explicar**, porque la autorización dirá «pregunta P1 sobre holdout-2» y el código leerá los tres.
- **El camino de fidelidad no tiene lector guardado, y hoy no lo necesita**, medido:
  `knowledge/cases/holdout/{1,2,3}/` contiene cuatro README y nada más, y el material del camino de
  fidelidad vive en `knowledge/feedback/` —que cubren `casos_reservados` y `trazar(ocultar=)`— y en
  `corpus/`, que ningún código lee. **El disparador, escrito para no volver a medirlo:** el día que
  exista bajo `knowledge/cases/<camino>/` un fichero con una etiqueta, un precio o el detalle por
  operación de un día asignado a una partición reservada, ese camino necesita lector guardado
  **antes de que ese fichero se commitee**.
- **Quien llame `abrir()` en un bucle sin gastar entre medias sigue abriendo N veces.** La puerta
  comprueba la AUTORIZACIÓN, no cuenta aperturas. Lo que hace que se abra una sola vez es que el
  camino soportado —el comando— gaste, y por eso gasta antes.
- **`EXPOSICIONES` sigue sin mecanismo**: ADR-0021 §4 obliga a declarar cada exposición el mismo
  día, y ningún código lo comprueba ni sabe que hubo una apertura que declarar.

## Fecha / fase

2026-09-17, rama `trabajo/guarda-de-holdout` (revisión de diseño con dos agentes antes de programar).

## Estado

ACTIVE
