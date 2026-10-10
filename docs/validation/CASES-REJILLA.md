# CASES-REJILLA · cases/ cuenta la ventana de cada caso por la rejilla H4 (puntos W y Z)

Rama `trabajo/cases-rejilla`, abierta el 2026-10-10 desde `main` en 26326b2 (commit de estado sobre
el merge 0b1c8ef, tag `stable/F37i-demo-ejecucion-1`). Encargo:
`docs/encargos/trabajo-cases-rejilla.md`. Primer commit: f8237bd (encargo, contrato y Archivo 26).

Antes de abrir se comprobó con git: `git rev-parse HEAD` en `main` = 26326b2;
`git rev-parse "stable/F37i-demo-ejecucion-1^{commit}"` = 0b1c8ef; `git branch -a` solo da `main` y
`origin/main`.

**Día de desfase**, aquí y en el código: un día en que el horario de verano de EE. UU. (el huso del
ancla de `anclaje_h4`, `America/New_York`) y el de Europa (`Europe/Madrid`) no coinciden. Se calcula
con zoneinfo: `bool(dst EE. UU.) != bool(dst Madrid)` a las 12:00 UTC del día. Nunca con una lista.

Las mediciones de esta fase son dos guiones de la carpeta de trabajo, fuera del repo
(`medir_fase0.py` y `medir_fase0_e2.py`); su salida, que solo da recuentos, va citada donde se usa.

## 0. Fase 0 · Inventario, sin tocar código

### 0.a Dónde convierte cases/ una hora nominal en un instante, o al revés

Registro de hoy: `huso_operativa` = `Europe/Madrid`, `reloj_sesiones` = `rejilla_h4`, `anclaje_h4` =
`17:00 America/New_York`, `sesiones_primera_vela_h4` = 3, `ventana_inicio` = `07:00`,
`huso_grafico` = `Europe/Madrid`. Config del kit (`knowledge/cases/kit/config.yaml`):
`ventana_local` 00:00–15:00, sesiones `07-11` y `11-15`.

| Sitio | Qué calcula hoy | Con qué reloj |
|---|---|---|
| `cases/ventanas.py:75-78` (`_minuto`) | de (día, «HH:MM») a minuto UTC, con `datetime.combine(..., tzinfo=huso)` | el huso que le pasen |
| `cases/ventanas.py:115-117` (`construir_caso`) | `desde` y `hasta` de la ventana del caso: `ventana_local` (00:00–15:00) en `huso_operativa`. De ellos salen `n_velas`, `sha256` (y por tanto la asignación del sorteo) y los `limites_h4` de cada anclaje candidato (`:132-135`, `limites_entre` sobre `[desde, hasta)`) | `huso_operativa` |
| `cases/ventanas.py:163-176, 252-254` (`universo`) | recibe `huso_operativa` y `ventana_local` y los pasa a `construir_caso` | `huso_operativa` |
| `cases/paquete.py:690-694, 726-731` (`construir`, `kit build` y `kit check`) | lee `huso_operativa` del registro y llama a `universo` | `huso_operativa` |
| `cases/paquete.py:765` | congela `huso_operativa: <huso>` en `ventanas.yaml` (informativo: `kit check` no lo lee, recompone con el del registro) | — |
| `cases/paquete.py:439-442` (`_hora_local`) y `:461, 504-507` (`hoja_trader`) | `hoja_trader.md`: pinta los `limites_h4` de cada caso en hora de `huso_operativa` | `huso_operativa` |
| `cases/paquete.py:489` (`hoja_trader`) | texto: «Dia operativo 00:00-15:00 (Europe/Madrid). Sesiones: 07-11 (07:00-11:00), 11-15 (11:00-15:00)» | `ventana_local` literal, nombrado en `huso_operativa` |
| `cases/fidelidad.py:262-266, 275-280` (`fidelidad build` y `check`) | igual que el kit: `universo` con `huso_operativa` | `huso_operativa` |
| `cases/fidelidad.py:300` | congela `huso_operativa` en su `ventanas.yaml` | — |
| `cases/hoja_docx.py:187-188` (`hora_local`) y `:480` (`documento`) | la hoja Word: las aperturas H4 «que verás», en hora de `huso_operativa` | `huso_operativa` |
| `cases/hoja_docx.py:425` (`bloque_etiquetado`) | texto al trader: «Gráfico que verás: de 00:00 a 15:00, hora tuya» y «tus dos sesiones: 07-11 de 07:00 a 11:00, ...» | `ventana_local` y las sesiones, literales |
| `cases/ingesta.py:367-375` (`_sesion_de`) y `:468` | asigna cada operación del libro a su sesión: pasa `_instante_utc` a `huso_operativa` y compara «HH:MM» con las sesiones nominales | `huso_operativa` |
| `cases/ingesta.py:409-411` → `corpus/libro.py:193` | el día de cada fila del libro (el filtro que decide qué filas se leen): la fecha del instante en `huso_operativa` | `huso_operativa` |
| `cli.py:1660-1679` (`cases ingest`) | lee `huso_operativa` del registro y se lo pasa a `ingerir` | `huso_operativa` |
| `cases/biblioteca.py:34-36` | solo un comentario: la sesión de cada operación «depende de `huso_operativa`» y se fija al ingerir | — |

Ningún otro sitio de `cases/` convierte horas: `grep` de `huso_operativa`, `ventana_local`,
`ZoneInfo`, `astimezone` y `huso_canonico` en `src/botsito/cases/*.py` y `cli.py` da solo estas
líneas (`criterio_fidelidad.py:152` compara minutos UTC entre sí, sin reloj).

**Qué cambia en un día de desfase (medido, `medir_fase0.py`).** En los laborables de 2024 y 2025,
la diferencia entre el instante que da la pared de `huso_operativa` y el que da la rejilla, para
00:00, 07:00 y 15:00 nominales: 0 minutos en los 1.449 casos fuera de desfase y **60 minutos en los
120 de desfase** (40 días, los mismos 20 al año de ACTIVACION-A42.md §5.1). Las dos semanas de
§4 de ACTIVACION-A42: el lunes 28 de octubre de 2024 (desfase) la ventana 00:00–15:00 por la rejilla
abre en el minuto UTC 28834440 y por la pared en 28834500 (una hora después); el lunes 4 de
noviembre de 2024 (control) las dos dan 28844580–28845480.

### 0.b Lo que ofrece la puerta (`engine/relojes.py`) y si cases/ puede llamarla tal cual

- `reloj_de_las_sesiones(registro)` (`:196`) → `RelojSesiones` del selector `reloj_sesiones`. Con
  `rejilla_h4` lee `anclaje_h4`, `sesiones_primera_vela_h4`, `ventana_inicio` y `huso_grafico`
  (`huso_visible`); con `civil_operativa` y `grafico`, el huso del reloj de pared.
- `RelojSesiones.instante(dia, "HH:MM")` (`:120`): de (día operativo, hora nominal) a minuto UTC,
  para los tres selectores. Con la rejilla, `apertura(dia) + (HH:MM − ventana_inicio)`; vale para
  cualquier hora nominal, también las 00:00 y las 15:00 de `ventana_local`.
- `RelojSesiones.apertura(dia)` (`:127`): la vela número N del día de rejilla; `RelojError` si esa
  vela no es una H4 entera (el día no es operable).
- `RelojSesiones.limites_de_sesiones(dia, sesiones)` (`:152`): (nombre, desde, hasta) UTC de cada
  sesión, con la guardia de que cada sesión sea una vela H4 entera de la rejilla.
- `RelojSesiones.lectura(instante)` (`:177`): de un minuto UTC a (día operativo, minutos nominales
  del día). Es lo que necesita la ingesta.
- `RelojSesiones.de_pared(huso)` (`:105`) y `huso_visible`: el reloj de pared, y el huso en que se
  pintan las horas que el trader ve (`huso_grafico` con la rejilla).

**Por lo que ofrece, cases/ puede usarla tal cual.** Las sesiones del kit son tuplas (nombre,
«HH:MM», «HH:MM»), que es lo que pide `limites_de_sesiones`; `ventana_local` son dos horas
nominales, que es lo que pide `instante`, y devuelve `MinutoUtc`, el mismo tipo que hoy devuelve
`_minuto`.

**Pero cases/ NO puede importarla desde donde está (medido).** El contrato de capas de
import-linter (`pyproject.toml:95-117`) ordena `cli → validation → viewer/mql5bridge → engine →
cases → spec → ...`: `engine` está POR ENCIMA de `cases` («engine consume cases, spec y data»,
ADR-0006), así que un `from botsito.engine.relojes import ...` en `cases/` rompe `lint-imports` y
`make check`. Hoy ningún módulo de `cases/` importa de `engine/` (`grep "from botsito.engine"
src/botsito/cases/` no da nada). Hay que tocar algo, y las salidas son tres:

- **(i) La implementación de la puerta baja a `cases/relojes.py` y `engine/relojes.py` la
  reexporta** con los mismos nombres (`RelojSesiones`, `reloj_de_las_sesiones`, `RelojError`,
  `REJILLA_H4`, `HUSO_DEL_RELOJ`, ...). El código se mueve sin cambiar una línea de lógica; el motor
  y sus tests siguen importando de `engine.relojes`, y es el mismo objeto. Sus dependencias
  (`config.registro`, `data.agregacion`, `data.velas`, `domain`, `comun`) están todas por debajo
  de `cases`, así que el contrato de capas se cumple sin tocarlo. **Es la que propongo**: no toca
  `pyproject.toml` ni la arquitectura, y la puerta sigue siendo una.
- (ii) Una excepción en el contrato (`ignore_imports` de `botsito.cases.* -> botsito.engine.relojes`
  en `pyproject.toml`, que habría que meter en el contrato de la rama). Diff más pequeño, pero abre
  un agujero en las capas.
- (iii) Un módulo nuevo fuera de las capas (`botsito.relojes`): import-linter no lo vigilaría. No la
  propongo.

### 0.c Ficheros congelados con ventanas, y si alguno tiene un día de desfase

Los congelados con ventanas son los `ventanas.yaml` de los repartos commiteados y lo que de ellos
depende (`particiones.yaml`, `hoja_trader.md`, anclas): `knowledge/cases/kit/2026-09-09-sesion-01/`
y `knowledge/cases/fidelidad/eurusd-2026-09/`. Los repartos dev-visto
(`knowledge/cases/visto/2026-04/` y `.../2026-08/`) solo tienen `particiones.yaml`, sin ventanas.
Los casos de `knowledge/cases/dev/` llevan la `sesion` de cada operación, fijada al ingerir.

**Medido por la puerta, sin abrir nada** (`medir_fase0.py`, sección (c)): para cada reparto que
devuelve `repartos_commiteables(repo)` -la misma lista que lee `casos_reservados`-, cuántos de los
casos de su `asignacion` son días de desfase. Solo imprime recuentos, ninguna fecha:

| Reparto | Casos | De desfase |
|---|---|---|
| `kit/2026-09-09-sesion-01` | 40 | 0 |
| `fidelidad/eurusd-2026-09` | 14 | 0 |
| `visto/2026-04` | 21 | 0 |
| `visto/2026-08` | 21 | 0 |

**Y por la condición, sin leer ningún congelado:** los manifiestos de velas son de enero a
septiembre de 2026; en ese rango los únicos días de desfase son los de primavera (marzo), y el
manifiesto de marzo (`eurusd-m1-2026-03-989392e8`) entró el 2026-09-24 (04f1ed9), después del último
commit de los dos `ventanas.yaml` (5facde9, 2026-09-20, y 394a18e, 2026-09-21). Ningún universo
congelado pudo contener un día de marzo, ni en `casos` ni en `excluidos`. Los casos de `dev/` son de
abril, mayo y agosto de 2026: fuera de desfase.

**Ningún congelado contiene un día de desfase: no hay PARADA por (c).** Recomponer cualquiera de
ellos por la rejilla da los mismos instantes que hoy (0.a: 0 minutos de diferencia fuera de
desfase), así que `kit check` y `fidelidad check` siguen reproduciéndolos byte a byte.

### 0.d El formato de lo congelado: propuesta mínima, SIN cambiar el esquema

Hoy `ventanas.yaml` congela el bloque `config:` (con `ventana_local`, `sesiones` y los anclajes),
`huso_operativa: Europe/Madrid`, los casos (`desde_utc`, `hasta_utc`, `n_velas`, `sha256`,
`limites_h4`), `datasets`, `universo` y `excluidos`. `kit check` y `fidelidad check` USAN el
`config:` y los `datasets` congelados, pero el huso lo leen **del registro de hoy**, no del
`ventanas.yaml` (`paquete.py:690`, `fidelidad.py:262`): el `huso_operativa` congelado es solo
informativo.

**Propuesta (opción 1, la mínima): el esquema no cambia.** `kit build`, `kit check`, `fidelidad
build` y `fidelidad check` piden el reloj al registro con `reloj_de_las_sesiones`, igual que hoy
piden `huso_operativa`. `ventanas.yaml` sigue escribiendo `huso_operativa` (es el huso del día de
riesgo y el que nombra la hoja; quitarlo cambiaría un byte de todo paquete nuevo y rompería el
criterio de regresión). Consecuencias:

- los artefactos ya congelados no cambian ni un byte y se siguen comprobando igual (0.c: ninguno
  tiene un día de desfase);
- un paquete nuevo construido fuera de desfase sale idéntico byte a byte al de `main`, que es el
  criterio de regresión del encargo;
- el riesgo que queda es el mismo que hay hoy con `huso_operativa`: si un día se cambiara
  `reloj_sesiones` en el registro, `kit check` de un paquete con días afectados fallaría con
  nombre (no en silencio). No hay cambio previsto: ADR-0069 lo fija.

**Opción 2, que no propongo:** congelar el reloj en `ventanas.yaml` (una clave `reloj_sesiones`
con la opción y sus parámetros) y leer los congelados sin esa clave como reloj de pared en su
`huso_operativa`. Hace a cada artefacto autodescriptivo, pero cambia los bytes de todo
`ventanas.yaml` nuevo (el criterio de regresión dejaría de ser byte a byte en ese fichero) y
necesita un lector para lo viejo. Si el consultor la prefiere, cabe en esta rama.

### 0.e Las guardias de la puerta y los días no operables

**Qué hace cases/ hoy con un día que la puerta no decide: nada**, porque no le pregunta. Propuesta,
negando por defecto: `construir_caso` llama a `reloj.limites_de_sesiones(dia, sesiones)` antes de
calcular la ventana; si la puerta levanta `RelojError` (la vela N no es entera, una sesión no es
una vela H4 de la rejilla, o ningún día de rejilla abre en esa fecha), el día sale como `Excluido`
con el motivo «la puerta del reloj no decide el día: <mensaje de la puerta>», no entra en el
universo y no se sortea. El motivo nombra el día, como todos los de `excluidos`.

**Medido (`medir_fase0.py`, sección (e)): con el ancla del registro, ningún laborable cae nunca en
un día no decidible.** Del 1 de enero de 2000 al 31 de diciembre de 2035 la puerta no decide 72
días, todos domingos (dos por año: el domingo del cambio de hora de EE. UU., en marzo y en
noviembre; p. ej. 2024-03-10 y 2024-11-03). El universo solo tiene laborables, así que con el
registro de hoy la guardia no salta nunca.

**El test la fuerza con un ancla sintética** (`medir_fase0_e2.py`): un ancla `00:00
Asia/Jerusalem` con `primera_vela` 1. Israel cambia la hora en viernes, y la puerta no decide el
viernes 2024-03-29 ni el 2025-03-28 (y los domingos de otoño). El test construye el universo de
una semana sintética con ese reloj y comprueba que el viernes sale excluido con el motivo de la
puerta y los otros cuatro días entran.

### 0.f Tests y criterio de regresión, con su mecánica

**Tests nuevos** (en `tests/unit/test_cases_rejilla.py`, con series de velas sintéticas o
calendario puro; fechas de 2024, ninguna de 2026):

1. **Un solo camino.** Busca en `src/botsito/cases/*.py` (ast/texto) cualquier conversión de hora con
   huso: `ZoneInfo(`, `astimezone(`, `datetime.combine(..., tzinfo=`, `huso_canonico(` y el nombre
   `huso_operativa` usado para algo que no sea escribirlo en `ventanas.yaml` o pasarlo al filtro de
   día de la ingesta (abajo). Con la salida (i) de 0.b, el módulo de la puerta (`cases/relojes.py`)
   es la única excepción, nombrada. Falla si aparece otro sitio. Con el código de `main` falla (los
   sitios de 0.a).
2. **Desfase.** Lunes 2024-10-28: la ventana del caso (`construir_caso` con el reloj del registro)
   empieza y acaba 60 minutos antes que la pared de `huso_operativa`; con el código de `main` el
   test falla porque sale igual que la pared.
3. **Control.** Lunes 2024-11-04: idéntica a la de `main` (la pared de `huso_operativa`), incluidos
   `n_velas`, `sha256` y `limites_h4`.
4. **Día no operable.** El ancla sintética de 0.e: el viernes 2024-03-29 sale excluido con el motivo
   de la puerta. Con `main` falla (el día entra).
5. **Ingesta.** Una operación sintética a las 06:30 de Madrid del 2024-10-28 cae en la sesión
   `07-11` (con `main` no cae en ninguna sesión y `ingerir` aborta); una a las 07:30 del 2024-11-04,
   en `07-11` como en `main`.
6. **Hoja.** Con un caso de desfase entre los `dev`, `hoja_trader.md` y el bloque de etiquetado de la
   hoja Word dicen las horas del gráfico del trader de ese día (de 23:00 de la víspera a 14:00, con
   sus H4 a las 06:00 y 10:00); sin ninguno, el texto es el de hoy byte a byte.

Los tests que ya existen y llaman a `ingerir` o a `universo` con un huso (`tests/contract/
test_ingesta.py`, `test_cobertura.py`, `test_ingesta_fidelidad.py`, `tests/unit/test_kit.py`) se
adaptan a la nueva firma sin cambiar lo que comprueban. Uno trae días sintéticos de marzo de 2026
que la condición del desfase alcanza (`test_ensayo_marzo.py`, tramo del 2 al 13): se mira en la
fase 1 si su resultado cambia y, si cambia, se dice.

**La ingesta, una decisión que se pide (PARADA, punto 3).** La SESIÓN de cada operación sale de
`reloj.lectura(instante)`. El DÍA de cada fila del libro lo decide hoy `corpus/libro.py:193` con
`huso_operativa`: es el filtro que decide qué filas se leen (la puerta del holdout por día), vive
fuera de `cases/` y fuera del contrato. Propongo no tocarlo y añadir en `ingesta.py` una guardia:
si el día que da `lectura` no es el día de la fila, `ingerir` aborta nombrando el caso, sin
instante ni precios. Una operación dentro de las sesiones nunca la dispara (la ventana de sesiones
cae entera en la misma fecha de Madrid también en desfase: 06:00–14:00).

**Criterio de regresión: la mecánica, medida.**

- **Los meses.** Enero, abril y agosto de 2026 (`medir_fase0.py`, sección (f)): 22, 22 y 21
  laborables, **0 días de desfase** y **0 casos en `casos_reservados`** en cada uno.
- **Dos clones desechables**, con `git worktree add --detach <carpeta de trabajo>/wt-main 26326b2`
  y `... wt-rama <sha de la rama>`, en la carpeta temporal de la sesión, fuera del repo. Se borran
  con `git worktree remove` al acabar.
- **Las velas sin copiarlas ni descargarlas.** Un worktree no trae `data/` (`.gitignore:3`,
  `/data/*`). La carpeta de datos la decide `config/ajustes.carpeta_datos`: `[rutas].data` de
  `config/settings.local.toml` (ignorado por git, `.gitignore:19`) unido a la raíz con `/`. Medido:
  `Path("C:/tmp/wt") / "C:/Users/USER/Desktop/Bot v3/data"` da la ruta absoluta del `data/` real.
  Así que cada clon lleva un `config/settings.local.toml` propio con `data` = la ruta absoluta del
  `data/` del repo, y los dos leen las mismas velas, sin copiarlas y sin bajar nada (pendiente
  heredado 9). Nada escribe en `data/`.
- **Dónde escribe cada build.** `kit build` escribe en `<clon>/knowledge/cases/kit/<sesion>/` y no
  sobreescribe: cada clon escribe en el suyo. Sesión sintética `2026-01-02-sesion-99`: con esa
  fecha `vistos.yaml` no excluye enero, abril ni agosto (sus `visto_el` son posteriores). Para que
  el universo sea SOLO enero, abril y agosto, en los dos clones se borran los manifiestos de los
  otros meses (`data/manifests/` es del clon, no del repo); los dos clones reciben la misma
  operación, así que la comparación sigue siendo de código contra código.
- **Qué se compara, por sha256:** los cuatro ficheros del paquete (`cuestionario.yaml`,
  `ventanas.yaml`, `particiones.yaml`, `hoja_trader.md`), la salida de `kit check` de ese paquete
  y la de `kit check` de `2026-09-09-sesion-01` y `fidelidad check` de `eurusd-2026-09` en cada
  clon (que lo congelado se reproduce igual con la rama). Y un tercer hash, el de las ventanas
  calculadas: el YAML de `universo()` sobre los manifiestos de los tres meses, con el `config` del
  kit, en cada clon.
- **Lo que se lee al hacerlo:** las velas M1 de enero, abril y agosto (desarrollo) y, por `kit check`
  de la sesión 1 y `fidelidad check` de septiembre, las de sus datasets congelados, que incluyen días
  reservados: leer velas para recalcular una ventana no es abrir (ADR-0021 §1), y las dos órdenes
  lo declaran por recuento (ADR-0033). Se declara en HOLDOUT-EXPOSICIONES el día que se haga.

### 0.g Lo leído en la fase 0 (declarado en HOLDOUT-EXPOSICIONES, fila del 2026-10-10)

- Código de `src/botsito/cases/`, `engine/relojes.py`, `cli.py`, `config/ajustes.py`, la cabecera
  de `.claude/hooks/guardia.py`, `knowledge/cases/kit/config.yaml`, `vistos.yaml` (cabecera) y los
  valores de reloj de `parametros.yaml`. Ningún `ventanas.yaml`, `particiones.yaml` ni hoja de un
  reparto se abrió.
- **Un listado que no debió hacerse así:** `git ls-files knowledge/cases | grep -v
  '^knowledge/cases/holdout/'`. `knowledge/cases/` contiene el holdout; el `grep` lo filtró antes de
  la salida, que enseñó solo rutas de `dev/` (los nombres de los casos dev de abril, mayo y agosto,
  que son de la partición dev), `fidelidad/`, `kit/` y los README. Ningún nombre de `holdout/`
  llegó a la salida, pero la lección de `trabajo/reloj-invierno` es no listar la carpeta madre. Y
  `git ls-files knowledge/cases/visto` (sus dos `particiones.yaml` y `anclas.yaml`).
- `medir_fase0.py` llama a `repartos_commiteables` y `casos_reservados` y solo imprime recuentos.
- Ninguna vela, ningún libro, ningún fotograma, ninguna transcripción. Marzo: nada.

## 1. PARADA

Lo que decide el consultor antes de escribir código:

0. **Dónde vive la puerta (0.b):** `cases/` no puede importar de `engine/` (contrato de capas de
   import-linter). Propuesta (i): la implementación baja a `cases/relojes.py`, sin cambiar su
   lógica, y `engine/relojes.py` la reexporta; el motor no cambia. Alternativa (ii): una excepción
   en `pyproject.toml`.
1. **El formato de lo congelado (0.d):** opción 1, sin cambiar el esquema (la propuesta), u opción 2,
   con el reloj congelado en `ventanas.yaml`.
2. **El día no operable (0.e):** excluido con motivo propio de la puerta, y el test forzado con un
   ancla sintética en `Asia/Jerusalem` (el registro no da nunca un laborable no decidible).
3. **La ingesta (0.f):** la sesión por `reloj.lectura`; el filtro de día de `corpus/libro.py` sigue
   en `huso_operativa` (fuera de `cases/` y del contrato), con la guardia de que los dos días
   coincidan.
4. **La hoja:** en un paquete con días de desfase entre los `dev`, el texto al trader cambia solo
   para esos días (las horas de su gráfico ese día); sin ellos, el texto de hoy byte a byte. Las
   horas se pintan en `huso_visible` (`huso_grafico`), que hoy vale lo mismo que `huso_operativa`.
5. **La mecánica de la regresión (0.f)**, con la sesión sintética y los manifiestos de los otros
   meses borrados en los dos clones.

## 2. Respuesta del consultor a la PARADA (2026-10-10), tal cual

> Modelo: Opus · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/cases-rejilla (2026-10-10). Cópiala tal cual en docs/validation/CASES-REJILLA.md, en «Respuesta del consultor a la PARADA», con su fecha.
>
> 0. Dónde vive la puerta: ACEPTADO, cases/relojes.py, sin cambiar una línea de lógica, y engine/relojes.py la reexporta con los mismos nombres. Porqué: spec tiene prohibido importar data (contrato «spec no depende del motor ni de los datos», pyproject.toml:90-93) y la puerta usa data.agregacion; una excepción en pyproject rodearía la guardia de capas. Un solo camino: test que falla si engine/relojes.py define una función o una clase propia. Los tests del motor no se tocan: si alguno parchea atributos del módulo engine.relojes y deja de pasar, para y dímelo antes de cambiarlo. Toda la suite en verde sin tocar ningún test del motor; el arnés no se ejecuta.
>
> 1. Qué se congela: NO como propones. Corrección: hoy huso_operativa SÍ se congela, como clave de primer nivel de ventanas.yaml (fidelidad.py:299, paquete.py:765), no solo se lee del registro. Decisión: los artefactos nuevos (kit y fidelidad) congelan también el reloj, en una clave de primer nivel reloj_sesiones con el valor del selector y, si es rejilla_h4, los parámetros que la puerta lee (anclaje_h4, sesiones_primera_vela_h4, ventana_inicio). huso_operativa se queda como está. Lectura, negando por defecto: un artefacto con la clave se comprueba con el reloj congelado, nunca con el del registro de hoy; un artefacto sin la clave se calculó en huso_operativa, y kit check y fidelidad check lo tratan así. Antes de escribirlo, mide que ningún artefacto congelado tiene hoy esa clave, con grep -c o grep -L y sin imprimir contenido (los ventanas.yaml listan casos de días reservados). Un valor de la clave que la puerta no reconoce es un error con nombre. Regresión: en enero, abril y agosto, el bloque casos, universo, excluidos, datasets y todos los demás ficheros salen idénticos byte a byte a main; ventanas.yaml difiere solo en la clave nueva, y el informe lo enseña con el diff. Porqué: el sorteo no se repite (ADR-0046 §5) y el artefacto tiene que decir con qué reloj se calculó, como ya lo dice del huso.
>
> 2. Día no operable: ACEPTADO. El motivo de exclusión lo da la puerta y nombra el día y la razón. El ancla sintética (Asia/Jerusalem) vive solo en los tests, nunca en el registro.
>
> 3. Ingesta: ACEPTADO. corpus/libro.py no se toca, porque el huso con que se lee un libro lo fija libros.yaml y no puede cambiar (CLAUDE.md, régimen de libros.yaml). La guardia nueva (si el día de la fila y el día operativo de la puerta no coinciden, la ingesta para) lleva un test que la rompe a propósito.
>
> 4. Hoja: ACEPTADO. Tests: un día de desfase con el texto nuevo y un día normal idéntico byte a byte al de main.
>
> 5. Mecánica de la regresión: ACEPTADA, con estas condiciones: todo ocurre en los dos worktrees temporales; la sesión 2026-01-02-sesion-99 y el borrado de manifiestos de los demás meses no salen de ellos; antes de ejecutar, comprueba leyendo el código (no ejecutando) que kit build y kit check no escriben en data/, y si escriben, para y dímelo; al acabar, git worktree remove de los dos, y git status del repo real igual antes y después. No listes data/ ni ninguna carpeta que contenga meses reservados.
>
> 6. Z, corrección del consultor: en el encargo escribí «paso a con la columna de fechas por el consultor», y es un error mío. ENTRADA-MARZO.md:20 y :46 y ADR-0046 §6a dicen que la columna de fechas de marzo la lee Aleks. CLAUDE.md dice en general «QUIEN: el consultor». Antes de escribir Z, mide ADR-0046 §6a y ADR-0021 §1: si marzo es una excepción acotada del ADR-0046 a la regla general, el párrafo de marzo de CLAUDE.md dice que la lee Aleks y cita ADR-0046 §6a; si los dos ADR se contradicen de verdad, para y dímelo. Cualquier otra regla de CLAUDE.md que Z toque se contrasta igual con su ADR.
>
> Sigue con la fase 1. Lo demás del encargo, sin cambios: make check sellado antes de cada commit, fix/cases-rejilla con la CI de Linux y sus números de run, informe y revisor con el alcance del encargo, al que añades: que la clave reloj_sesiones se lee negando por defecto y que engine/relojes.py no define nada propio.
>
> Rama lista para revisión, NO cerrada.

La corrección del punto 1 es cierta, y se dice con su nombre: la fase 0 (§0.d) escribió que el
`huso_operativa` congelado era «solo informativo» porque `kit check` no lo lee; pero sí se congela
como clave de primer nivel, y lo que el artefacto dice de sí mismo es parte de lo congelado.

## 3. Fase 1

### 3.1 Medidas previas

- **Ningún artefacto congelado tiene la clave `reloj_sesiones`** (punto 1): `grep -c
  "reloj_sesiones"` sobre las dos rutas literales,
  `knowledge/cases/kit/2026-09-09-sesion-01/ventanas.yaml` y
  `knowledge/cases/fidelidad/eurusd-2026-09/ventanas.yaml`, da `0` y `0`. Son los dos únicos
  `ventanas.yaml` commiteados (§0.c; los repartos de `visto/` no tienen).
- **Z, ADR-0046 §6a contra ADR-0021 §1** (punto 6). ADR-0046 §6 se declara a sí mismo «excepción
  acotada a ADR-0039 §1» y su apartado a dice: «Aleks lee SOLO la columna de fechas, UNA vez,
  antes del sorteo» (líneas 64-76); «la excepción cubre solo la columna de fechas, en una sola
  lectura, hecha por Aleks». ADR-0021 §1 define qué es abrir un holdout (leer etiquetas o el detalle
  por operación; medir una cifra del bot) y **no nombra a nadie** que lea la columna de fechas. No
  se contradicen: marzo es una excepción acotada que fija quién, y la regla general no lo fija. El
  «QUIEN: el consultor» del párrafo general de CLAUDE.md no sale de ADR-0021 §1; queda anotado
  como hallazgo para el consultor (Z solo toca el párrafo de marzo).

### 3.2 PARADA 2 · Un test del motor lee el fuente de `engine/relojes.py`

Antes de mover la puerta se midió qué tests tocan `engine.relojes`. Ninguno parchea atributos del
módulo (`grep` de `relojes` en `tests/`: solo imports y llamadas). Pero uno **lee el fichero
fuente**: `tests/unit/test_sesiones_rejilla_h4.py:237-253`,
`test_el_codigo_del_reloj_no_lleva_ningun_desfase`, abre `src/botsito/engine/relojes.py`, quita
comentarios y docstrings, y exige que no haya `Etc/GMT`, `timezone(`, `timedelta(hours` ni una hora
escrita, y que aparezca `limites_del_dia`. Con la puerta en `cases/relojes.py` y `engine/relojes.py`
reducido a reexportar, la última aserción falla: el código que el test vigila ya no está en el
fichero que abre. Se para aquí, como manda el punto 0, sin tocar el test.

### 3.3 Respuesta del consultor a la PARADA 2 (2026-10-10), tal cual

> Respuesta del consultor (2026-10-10), cópiala tal cual en el informe junto a la PARADA 2 (§3.2).
>
> (a), con un ajuste: test_el_codigo_del_reloj_no_lleva_ningun_desfase no escribe ninguna ruta fija; abre el fichero donde vive de verdad el código, sacado con inspect.getsourcefile(reloj_de_las_sesiones) importado desde botsito.engine.relojes. Así vigila la puerta esté donde esté y no se queda vacío si se vuelve a mover. Lo demás del test no cambia. El test nuevo de un solo camino (engine/relojes.py no define funciones ni clases propias) se queda como está. La (b) queda descartada: meter limites_del_dia en el fichero de reexportación para que el test pase sería rodearlo.
>
> Z: conforme con lo medido. El párrafo de marzo de CLAUDE.md dice que la columna de fechas la lee Aleks y cita ADR-0046 §6a. El hallazgo aparte (el «QUIEN: el consultor» de la regla general no sale de ADR-0021 §1) no se toca en esta rama: apúntalo en el informe como pendiente para el consultor.
>
> Sigue con la fase 1 cuando make check selle el commit en curso.

**Pendiente para el consultor (no se toca en esta rama):** el «QUIEN: el consultor» de la regla
general de CLAUDE.md («Lo minimo para fijar el universo SI se lee») no sale de ADR-0021 §1, que no
nombra a nadie (§3.1).

### 3.4 Lo que cambia en el código

**La puerta (punto 0).** `src/botsito/cases/relojes.py` es `engine/relojes.py` copiado tal cual; lo
único que cambia es un párrafo del docstring que dice por qué vive ahí. `engine/relojes.py` queda
en un docstring y una reexportación de los doce nombres de `__all__`, sin ninguna función ni clase
propias (`test_engine_relojes_no_define_nada_propio`, que además comprueba que cada nombre es el
MISMO objeto en los dos módulos). Del motor no se tocó nada: `motor.py`, `primitivas.py`,
`arnes.py`, `simulacion.py`, `visor.py` y `cli.py:2378` siguen importando de `engine.relojes`.
`lint-imports`: 4 contratos KEPT, 0 rotos. El único test del motor tocado es la línea que pidió el
consultor (§3.3): `test_el_codigo_del_reloj_no_lleva_ningun_desfase` abre
`inspect.getsourcefile(reloj_de_las_sesiones)`, importado de `botsito.engine.relojes`.

**La ventana (`cases/ventanas.py`).** `construir_caso` y `universo` reciben `reloj` (un
`RelojSesiones`) y las `sesiones` del config, y ya no un huso. La ventana es
`reloj.instante(dia, ventana_local[0])` a `reloj.instante(dia, ventana_local[1])`; antes, la
guardia de la puerta: `reloj.limites_de_sesiones(dia, sesiones)`. Si la puerta levanta
`RelojError`, el día sale de `excluidos` con el motivo «la puerta del reloj no decide el día:
<mensaje de la puerta>», que nombra el día y la razón (punto 2). `_minuto`, que pasaba la hora a
`huso_operativa` con `datetime.combine`, desaparece.

**Lo congelado (punto 1).** En `ventanas.py`:
- `reloj_del_registro(registro)`: el reloj de un artefacto NUEVO y su forma congelada, la clave de
  primer nivel `reloj_sesiones` con el valor del selector y los parámetros que la puerta lee con
  él (la tabla `PARAMETROS_DE_LA_REJILLA`, no una copia). Con `rejilla_h4` son cuatro:
  `anclaje_h4`, `sesiones_primera_vela_h4`, `ventana_inicio` y `huso_grafico`. El consultor nombró
  tres; el cuarto entra porque la puerta también lo lee (`huso_visible`, las horas que se pintan en
  la hoja), y sin él el reloj congelado no se podría reconstruir entero.
- `reloj_de_ventanas(ventanas, donde)`: el reloj de un artefacto YA congelado. Con la clave,
  `reloj_congelado`; sin ella, `RelojSesiones.de_pared(<su huso_operativa>)`; sin ninguna de las
  dos, o con un huso que no existe, `RelojError` con nombre. Nunca el registro de hoy.
- `reloj_congelado(doc, donde)`, negando por defecto: un mapa; el selector tiene que ser una
  opción que la puerta reconozca; las claves, EXACTAMENTE las de esa opción; los tipos, los suyos;
  los husos, IANA. Y el reloj se construye por la MISMA función que el del registro
  (`reloj_de_las_sesiones`, servida por un adaptador de solo lectura), así que sus guardias -una
  `sesiones_primera_vela_h4` fuera de la rejilla, por ejemplo- también valen para lo congelado.

`paquete.construir` y `fidelidad.construir` aceptan `reloj` con el mismo contrato que `datasets` y
`config`: `None` es el del registro (artefacto nuevo, que escribe la clave); `kit check` y
`fidelidad check` pasan el de `reloj_de_ventanas`. Un artefacto sin la clave se recompone sin
escribírsela, así que sus bytes no cambian. `huso_operativa` se sigue congelando como estaba.

**Las hojas (punto 4).** `hoja_trader.md` (`paquete.hoja_trader`) y la hoja Word
(`hoja_docx.bloque_etiquetado`) pintan las horas en el `huso_visible` de la puerta
(`ventanas.hora_en_pantalla`). Con `dias_con_otras_horas`, si algún día `dev` no se ve en el gráfico
del trader con la ventana y las sesiones en sus horas nominales, la hoja lo nombra con las de ese
día («de 23:00 de la víspera a 14:00; sesiones 07-11 de 06:00 a 10:00, 11-15 de 10:00 a 14:00»).
Sin ninguno, no añade nada. La hoja Word toma el reloj del `ventanas.yaml` congelado del paquete.

**La ingesta (punto 3).** `ingerir` pide `reloj` (argumento con nombre, obligatorio). La sesión de
cada operación sale de `reloj.lectura(instante)`; el día de la fila sigue saliendo del lector con
`huso_operativa` (`corpus/libro.py` no se toca). Si los dos días no coinciden, la ingesta para
nombrando el caso, sin instante ni precios. La CLI (`casos ingerir`) pasa el reloj del registro.

**Un solo camino.** Fuera de la puerta, en `cases/` solo quedan dos llamadas que tocan un huso, las
dos nombradas en `test_un_solo_camino_ningun_sitio_de_cases_convierte_horas_con_un_huso`:
`ventanas._en_pantalla` (pintar una hora del gráfico; ninguna ventana se calcula con ella) y
`paquete.config_desde_doc` (validar que existe el huso de un anclaje candidato). Cualquier otro
`astimezone`, `ZoneInfo`, `combine`, `localize`, `fromtimestamp` o argumento `tzinfo=` en
`src/botsito/cases/` hace fallar el test.

**Los tests que ya existían.** Se adaptaron a las firmas nuevas sin cambiar lo que comprueban:
`tests/unit/test_kit.py` (el registro sintético gana `reloj_sesiones` = `civil_operativa`, la pared
de `huso_operativa`, para que sus casos sigan siendo los de siempre sin tocar `anclaje_h4`, que es
UNKNOWN a propósito; y `test_ventana_en_invierno` pasa la pared de Madrid por la puerta),
`tests/contract/test_ingesta.py`, `test_cobertura.py` y `test_ingesta_fidelidad.py` (`reloj=RELOJ`,
el reloj del registro real). `test_ensayo_marzo.py`, con días sintéticos de marzo de 2026 que la
condición del desfase alcanza, usa ese registro sintético, así que sigue en la pared y no cambia.

### 3.5 Los tests nuevos, y lo que hace `main` en cada uno (medido)

`tests/unit/test_cases_rejilla.py` (14 funciones) y `tests/contract/test_ingesta_rejilla.py` (3).
Con el código de `main` el módulo de la rama ni siquiera importa (`ImportError: cannot import name
'RelojDelArtefacto' from 'botsito.cases.ventanas'`, salida de pytest en el clon de `main`), así que
se midió con la API de `main`, en su clon, lo que comprueba cada test que rompe a propósito
(`medir_main.py` y `medir_main_hoja.py` de la carpeta de trabajo; botsito importado del clon, y el
guion lo comprueba):

| Test de la rama | Lo que da `main` | Lo que exige el test |
|---|---|---|
| un solo camino (`astimezone`, `ZoneInfo`, `combine`, `tzinfo=`... fuera de la puerta) | 11 llamadas: `ventanas._minuto` (`astimezone`, `combine`, `tzinfo=`), `ventanas.construir_caso` (`ZoneInfo`), `ingesta._sesion_de` (`ZoneInfo`, `astimezone`), `paquete._hora_local` (`astimezone`), `paquete.hoja_trader` (`ZoneInfo`), `hoja_docx.hora_local` (`astimezone`), `hoja_docx.documento` (`ZoneInfo`) y `paquete.config_desde_doc` (`ZoneInfo`) | solo `ventanas._en_pantalla` y `paquete.config_desde_doc` |
| desfase, lunes 2024-10-28 | ventana `2024-10-27T23:00Z - 2024-10-28T14:00Z` | `2024-10-27T22:00Z - 2024-10-28T13:00Z` (una hora antes) |
| control, lunes 2024-11-04 | `2024-11-03T23:00Z - 2024-11-04T14:00Z`, 900 velas | lo mismo, y el caso igual al de la pared |
| día no operable (ancla sintética Asia/Jerusalem, viernes 2024-03-29) | entra como `Caso` | `Excluido`, con «la puerta del reloj no decide el dia: 2024-03-29 ... no es entera» |
| ingesta, 06:30 de Madrid del lunes de desfase | `IngestaError`: «su apertura no cae en ninguna sesion declarada» | sesión `07-11` |
| ingesta, 07:30 de Madrid del lunes de control | sesión `07-11` | `07-11`, igual que con la pared |
| la guardia del día, 23:30 de Madrid del domingo 27 | `IngestaError` con el mensaje de «ninguna sesion» | `IngestaError` con «no es el dia operativo de su apertura», sin instante ni precios |
| hoja, lunes de desfase | «Dia operativo 00:00-15:00 (Europe/Madrid). Sesiones: 07-11 (07:00-11:00), 11-15 (11:00-15:00)» y nada más | además, «- 2024-10-28: dia operativo de 23:00 de la vispera a 14:00; sesiones: 07-11 de 06:00 a 10:00, 11-15 de 10:00 a 14:00.», y lo mismo en la hoja Word |
| hoja, lunes de control | — | idéntica a la de la pared de Madrid, byte a byte, en las dos hojas |

**Una corrección al medir.** El test del día no operable usaba un mínimo de 200 velas, y con él
`main` YA excluía el viernes: la ventana de pared de 00:00 a 04:00 de Jerusalén ese día tiene 180
minutos, por el cambio de hora. Lo excluía por las velas, no por la puerta. El mínimo del test bajó
a 150 (el jueves, con 240 velas, entra igual), y con 150 `main` mete el viernes como `Caso`: ahora
el test solo pasa por la puerta. Su docstring dice lo medido.

Los demás tests nuevos (la clave congelada, negando por defecto; `engine/relojes.py` sin nada
propio; las firmas que piden `reloj`) prueban API que en `main` no existe.

### 3.6 Criterio de regresión: enero, abril y agosto de 2026, `main` contra la rama

Mecánica de §0.f, aceptada en el punto 5. Dos clones desechables en la carpeta de trabajo de la
sesión: `git worktree add --detach .../regresion/wt-main 26326b2` y `.../wt-rama b0e8742`. En cada
uno, un `config/settings.local.toml` con `data` = la ruta absoluta del `data/` del repo real; las
velas no se copiaron ni se descargaron. Antes de ejecutar se comprobó leyendo el código que
`kit build` y `kit check` no escriben en `data/`: `cargar_serie` y `cargar_ventana`
(`data/dataset.py:398-433`) solo leen, y las únicas escrituras de `paquete.py` son la carpeta del
paquete (`escribir`, `:794-801`) y `anclas.yaml` (`:950`), las dos bajo `knowledge/` del clon; las
escrituras de `data/` están en `congelar` y `escribir_manifiesto` (`data/dataset.py:186-251`), que
son de `data download`. La CLI de cada clon se llamó con un guion (`cli.py`) que importa botsito del
`src/` del clon y lo comprueba antes de ejecutar.

**1. Lo congelado, con todos los manifiestos** (antes de quitar ninguno):

| Salida | `main` | rama |
|---|---|---|
| `kit check --sesion 2026-09-09-sesion-01` (exit 0) | `aafe403a…ecb010` | `aafe403a…ecb010` |
| `fidelidad check --artefacto eurusd-2026-09` (exit 0) | `06a71fba…02d02e` | `06a71fba…02d02e` |

Los dos `OK`. La sesión 1 da los mismos dos AVISO en los dos clones (`cuestionario.yaml` y
`hoja_trader.md` ya no se generan igual porque la sesión se celebró, que es lo de siempre), y su
`ventanas.yaml` y `particiones.yaml` se reproducen byte a byte también con la rama. Ningún fichero
congelado cambia.

**2. Un paquete nuevo de enero, abril y agosto.** En los dos clones, y solo en ellos, se quitaron
los manifiestos de marzo, mayo, junio, julio y septiembre (por su nombre literal), y se construyó
`kit build --sesion 2026-01-02-sesion-99 --seed 20261010`: con esa fecha `vistos.yaml` no excluye
ninguno de los tres meses. Salida: «40 casos (16 dev) de un universo de 62 (+ 3 dias excluidos)».

| Fichero o salida (sha256) | `main` | rama |
|---|---|---|
| salida de `kit build` | `b9d0b28b…7c0cb4` | `b9d0b28b…7c0cb4` |
| `cuestionario.yaml` | `13c4947a…94839e1` | igual |
| `hoja_trader.md` | `335bcf66…dadc0ad5` | igual |
| `particiones.yaml` | `a66bd4e5…5229fa9c` | igual |
| `ventanas.yaml` | `15afd5d9…56b551b9` | `9189eb36…fa230325` (la clave nueva) |
| `ventanas.yaml` sin la clave `reloj_sesiones`, volcado como el kit | `15afd5d9…56b551b9` | `15afd5d9…56b551b9` |
| salida de `kit check` del paquete nuevo (exit 0, «se recompone igual») | `be7a6d72…76543a1` | `be7a6d72…76543a1` |

Hashes completos:

```
13c4947ab6bea6bc2976ca188ca1eae41f266df05c73b209367e62c1894839e1  cuestionario.yaml   (main y rama)
335bcf663f8ea960eec9d212fb7e9887f48cca994f20c6b9ae1d3750dadc0ad5  hoja_trader.md      (main y rama)
a66bd4e5aa095844a0188c260e7c61f3afa415237af5a92622c291cd5229fa9c  particiones.yaml    (main y rama)
15afd5d9c163081f41d4dc5764450f64b16e64c8d561800ea576fd88f9b551b9  ventanas.yaml       (main)
9189eb36426a6f54e7b37e148192dbc6f42d2c143aff69b2c5fff737fa230325  ventanas.yaml       (rama)
15afd5d9c163081f41d4dc5764450f64b16e64c8d561800ea576fd88f9b551b9  ventanas.yaml rama sin la clave
15afd5d9c163081f41d4dc5764450f64b16e64c8d561800ea576fd88f9b551b9  ventanas.yaml main revolcado
b9d0b28b765bb49490c4b6480040f49ddc0aa79168ce33004edf46b56d7c0cb4  salida de kit build (main y rama)
be7a6d724b1f21a815273ab343b8f1f5983223e9953c7e2cbda6917fe76543a1  salida de kit check del paquete nuevo
aafe403a5f003a22a903a774dee064def85018ef869078c8cec67e5d6aecb010  kit check de la sesion 1
06a71fba5fb7f6c4327281771cfbfeaca32dea59f6fbf9ebcab51b80a002d02e  fidelidad check de septiembre
```

El `ventanas.yaml` de `main` vuelto a volcar con el mismo `yaml.safe_dump` del kit da su mismo hash:
el volcado es fiel, y quitar la clave del de la rama deja exactamente el de `main`. El diff de los
dos `ventanas.yaml` es solo la clave nueva:

```
873a874,883
> reloj_sesiones:
>   anclaje_h4:
>     hora: '17:00'
>     huso: America/New_York
>   huso_grafico: Europe/Madrid
>   reloj_sesiones: rejilla_h4
>   sesiones_primera_vela_h4: 3
>   ventana_inicio:
>     hora: 07:00
>     huso: Europe/Madrid
```

`kit check` del paquete nuevo en la rama lo recompone con el reloj de esa clave y sale `OK`, así que
la clave se escribe y se vuelve a leer sin perder nada. Las ventanas calculadas (los `casos`, el
`universo` y los `excluidos`) son las de `main`.

**La hoja Word no se pudo comparar:** `kit hoja --sesion 2026-01-02-sesion-99` sale con exit 1 en
LOS DOS clones, con el mismo error (`0073477f…` las dos salidas): «ninguna pregunta del paquete nace
de 'A-9'; revisa el cuestionario». No es de esta rama: `numero_de_pregunta(preguntas, ANCLAJE_H4)`
busca una pregunta nacida de A-9, y el cuestionario que genera hoy el kit ya no la trae. Hallazgo
para el consultor (§3.8). La hoja Word queda cubierta por los dos tests de §3.5, que comparan su
bloque de etiquetado con el de la pared byte a byte.

**3. Al acabar:** `git worktree remove` de los dos (`git worktree list` ya no los da). `git status
--short --untracked-files=all` del repo real: vacío antes; después, solo
`tests/unit/test_cases_rejilla.py`, el cambio deliberado de §3.5 (el mínimo de 150), hecho a mano
en el repo y no por la regresión. Queda en la lista otro worktree que no es de esta sesión
(`.../2ea2c3d2-.../scratchpad/wt-ci`, en e7df30b): no se tocó.

### 3.7 Z

- `CLAUDE.md`, párrafo «Marzo de 2026 esta RECIBIDO y SIN ABRIR»: ya no espera a A-42. Dice que
  A-42 está RESUELTA (ADR-0069) y que `cases/` cuenta la ventana por la rejilla desde esta rama,
  así que la PARADA B0 ya no lo detiene, y que antes del paso b faltan, medidos hoy: del paso 0,
  marzo en `vistos.yaml` (`grep -c "2026-03" knowledge/cases/kit/vistos.yaml` = 0) y la
  confirmación escrita del trader (REGISTRO-MARZO.md §2); y el paso a (no hay
  `cobertura_material."2026-03"` en `knowledge/cases/fidelidad/config.yaml`: el único `"2026-03"`
  es el de `cupos_por_mes`). La columna de fechas la lee Aleks (ADR-0046 §6a).
- `docs/runbooks/ENTRADA-MARZO.md`: recuadro de CORRECCIÓN del 2026-10-10 al principio del paso b,
  encima del de `trabajo/activacion-a42`, sin tocar el cuerpo: la PARADA B0 deja de tener motivo.
- El «QUIEN: el consultor» de la regla general queda como pendiente (§3.3).

### 3.8 Hallazgos para el consultor

1. **`kit hoja` está roto en `main`** para cualquier paquete nuevo: busca una pregunta nacida de
   A-9 que el cuestionario de hoy ya no genera (§3.6). No lo toca esta rama.
2. **La ingesta asigna la sesión con el reloj del registro**, no con el congelado del artefacto
   (punto 3 aceptado así). Con el registro de hoy es el mismo reloj; si un día cambiara
   `reloj_sesiones`, la ingesta de un artefacto sorteado antes usaría el nuevo. No pasa hoy.
3. **El registro sintético de `tests/unit/test_kit.py`** gana `reloj_sesiones` =
   `civil_operativa`: los tests del kit y de fidelidad que se apoyan en él (también
   `test_ensayo_marzo.py`) siguen en la pared de Madrid. La rejilla en esos caminos la prueban los
   tests nuevos y la regresión.
4. **`ventana_inicio` se escribe en YAML como `hora: 07:00` sin comillas** y `anclaje_h4` como
   `'17:00'`: es el volcado de PyYAML (las 17:00 parecerían un número sexagesimal; las 07:00 no). Se
   lee como texto en los dos casos, y `kit check` del paquete nuevo lo demuestra.

## 4. Exposiciones declaradas

Fila del 2026-10-10 en HOLDOUT-EXPOSICIONES (fase 0) y su complemento de la fase 1: las velas M1 de
los días reservados que leen `kit check` de la sesión 1 (24: holdout-1 8, holdout-2 8, holdout-3 8)
y `fidelidad check` de septiembre (10: fidelidad-1 10), por recuento y sin fechas, que no es abrir
(ADR-0021 §1, ADR-0033); y las de enero, abril y agosto (desarrollo). Las 24 «reservadas» que
declara el paquete sintético `2026-01-02-sesion-99` son de su propio sorteo, en un clon desechable
que ya no existe: días de enero, abril y agosto, ningún reparto commiteado. Ninguna etiqueta, ningún
libro, ningún fotograma, nada de marzo.

## Estado

EN CURSO. Fase 1 hecha (§3.4 a §3.8): código, tests, regresión y Z. Faltan la CI de Linux
(`fix/cases-rejilla`) y el revisor.
