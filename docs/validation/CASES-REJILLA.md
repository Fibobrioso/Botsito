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

## Estado

EN CURSO. Fase 0 entregada; **PARADA** a la espera de la respuesta del consultor. No se ha escrito
código.
