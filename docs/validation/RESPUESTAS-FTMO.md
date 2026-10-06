# Respuestas de FTMO al ticket VDW-DPMWR-965 (2026-10-05) y los tags tras F36z

- **Rama:** `trabajo/respuestas-ftmo`, punto T del Next Action.
- **Encargo:** `docs/encargos/trabajo-respuestas-ftmo.md`, dado por el consultor el 2026-10-05.
- **Base:** `main` en `54c69fe`, el commit de estado de `stable/F36z-ventana-no-citable`, que apunta
  a `f8b291c`. La CI de `main` es el run 221, en verde. Se comprobó antes de abrir: `main` =
  `origin/main` = `54c69fe`, `git rev-parse "stable/F36z-ventana-no-citable^{commit}"` = `f8b291c` y
  `gh run view 37383049905` da `success` sobre `54c69fe`.
- **Regla de toda la rama:** el correo de FTMO no se copia. Ningún texto commiteado lleva frases en
  inglés del correo ni el nombre de la persona de soporte. La fuente del contenido es la paráfrasis
  del consultor del 2026-10-05, que está en el encargo.

## 0. Fase 0: inventario sin tocar nada

Las medidas están en `docs/validation/anexos/RESPUESTAS-FTMO/`, cada guion con su salida. Ninguna
escribe en el repositorio.

### 0.a El tag `stable/F37a-<nombre>` frente a cada lector del formato

**La prueba** es `prueba_f37a.py` (salida en `prueba_f37a-SALIDA.txt`). Se ejecuta desde la raíz del
repositorio real, con un argumento: un `git clone` desechable de `main` hecho en la carpeta de
trabajo de la sesión, fuera del repositorio. El tag de prueba `stable/F37a-respuestas-ftmo` se crea
SOLO en el clon, sobre `f8b291c` y con una fecha posterior a la de F36z. Un `git worktree` no valía:
comparte los refs y el tag habría quedado en el repositorio real. El clon no tiene identidad de git
(la del repositorio es local), así que el guion le pone una propia (`prueba-fase0`). Al principio se
hizo a mano; tras el hallazgo a-3 del revisor lo hace el guion, y repetido sobre un clon nuevo da una
salida idéntica. Después de la prueba,
`git tag -l "stable/F37*"` en el repositorio real sale vacío.

| Lector | Qué lee | ¿Pasa F37a? | Prueba (ejecutada) |
|---|---|---|---|
| `.claude/skills/cerrar-rama/SKILL.md:32` | Propone el tag «siguiendo el ultimo `git tag -l "stable/*" --sort=-creatordate`» y lo CONFIRMA antes del merge. Es prosa: no deriva la letra con ningún código. | Sí | En el clon, `git tag -l "stable/*" --sort=-creatordate` da primero `stable/F37a-respuestas-ftmo`, luego F36z y F36y (§4 de la salida) |
| `.claude/hooks/guardia.py:1293-1298`, `:1378` y `:1783` | Solo el prefijo `stable/` (o `refs/tags/`) y las banderas que borran o mueven (`-d`, `--delete`, `-f`, `--force`, `:ref`). No mira la letra ni el número. | Sí | `decidir` sobre el repositorio real: pasan las seis órdenes del ritual con F37a (`tag -a`, `rev-parse ^{commit}`, `push --atomic`, `ls-remote`, el commit de estado y `tag -l`), y siguen bloqueadas las cuatro que borran o mueven el tag (§1) |
| `uv run botsito state check` (`src/botsito/cli.py:96-102`, `_ultimo_tag_estable`; reglas 3 y 5, `:140-157`) | El primer tag de `git tag -l "stable/*" --sort=-creatordate`, sin mirar su forma, y su `^{commit}` | Sí | `_ultimo_tag_estable(clon)` = `('stable/F37a-respuestas-ftmo', 'f8b291c')` y `state_check(clon)` = 0 («OK: rama 'main'») (§4) |
| `src/botsito/cli.py:166`, regla 4 de `state check` (Completed Features) | `-\s*(F\d{2})\b`: una línea `- F##` exige un informe `docs/validation/F##-*.md` | Sí: no casa | `- F37a-respuestas-ftmo` no casa (tampoco `- F36z-...`, que ya no casaba); `- F37 algo` sí, como control (§2). Además, el cierre no escribe en Completed Features desde `trabajo/ajustes-cierre` |
| `src/botsito/validation/knowledge.py:38-47` (`ids_de_funcionalidad`) y `src/botsito/config/registro.py:293` (`_CONSUMIDOR`) | Las filas `\| F## \|` de la tabla de `docs/plan/MASTER_PLAN.md`, para validar `consumido_por` de los parámetros. Ningún tag. | Sí: no lo lee | 35 ids, sin F36 ni F37 (§3) |
| `tests/unit/test_project_state.py` | Secciones de `PROJECT_STATE.md` y su tope de 25.000 bytes. Ningún tag. | Sí: no lo lee | Lectura del fichero entero (56 líneas): ni `stable` ni `F##` |
| `tests/unit/test_guardia_claude.py` | Ejemplos fijos: `stable/F36h-...` y `stable/F36j-...` en las órdenes que bloquean (`:539-542`, `:719-766`, `:921-944`); `stable/F37-guardias-claude` en el ritual que pasa (`:796-808`, `:965`); `stable/F01` | Sí | No deriva ningún formato. Las mismas formas, con F37a, pasan por `decidir` arriba |
| Resto del grep de `stable/` y `F\d` en `tests/`, `scripts/`, `src/`, `.claude/` y `.github/` | `stable/F99` en repositorios sintéticos (`tests/unit/test_cli.py:84`, `:176`); `stable/viejo` y `stable/nuevo` (`tests/unit/test_push_atomico.py`); el ancla fija `stable/F06` (`src/botsito/comun/historial.py:37`, `tests/contract/test_feedback_history.py`, `.github/workflows/ci.yml:23`); las reglas `ask` de `.claude/settings.json:24-40` (`stable/*`) | Sí | Ninguno compone ni ordena un tag por su letra; `scripts/` no tiene ninguna coincidencia |

**Conclusión:** nada lee el formato del tag de forma que `stable/F37a-<nombre>` lo rompa. La skill
`cerrar-rama` no deriva la letra mecánicamente, así que, por la decisión 4, `.claude/` no se toca y
la rama no necesita `fix/`.

**Hallazgo (PARADA):** RITUAL.md no tiene la regla que la decisión 4 da por existente, «la regla que
manda consultar la última letra en HISTORIA». `grep -n "letra" docs/runbooks/RITUAL.md` solo
encuentra la letra del Next Action (`:138-139`). Tampoco está en `.claude/skills/`, `CLAUDE.md`,
`docs/state/README.md` ni `MASTER_PLAN.md`. Esa comprobación solo venía en las órdenes de cierre de
F36y y F36z. Lo más cerca es el paso del tag, `git tag -a stable/<tag>` (`RITUAL.md:200-205`).
Va a la decisión del consultor (§1).

### 0.b ADR-0067 frente a las preguntas 1 a 4

**La prueba** es `medir_freno_huso.py` (salida en `medir_freno_huso-SALIDA.txt`). Se ejecuta con
`PYTHONPATH=.`, porque usa el broker de prueba de `tests/unit/test_freno_peticiones.py`.

- **Qué cuenta hoy el freno.** Toda petición que deja salir en los cinco métodos del broker:
  `_colocar`, `modificar`, `cancelar`, `cerrar_a_mercado` y `_mover` (ADR-0067 §1). Eso incluye lo
  que protege la cuenta, que sale siempre y cuenta (§3): cancelar, cerrar y el primer movimiento del
  stop hacia el lado del riesgo. El comentario de A-54 (`ambiguedades.yaml:1524-1526`) dice lo mismo.
- **Una orden que rechaza el servidor CUENTA.** El freno la admite, y la cuenta, antes de que el
  servidor la mire (`broker.py:411-421` al colocar; `:473-484` al modificar). Medido: una compra
  límite por encima del ask vuelve como `Rechazo` con motivo `precio_invalido`, la traza tiene 1
  petición con `aceptada=False` y `freno.total()` = 1.
- **Lo que niega el propio bot NO cuenta**, ni por el freno ni por la ventana de cierre: no llega al
  servidor (`broker.py:406-414`). Medido: 5 compras iguales seguidas dan `freno.total()` = 4 y una
  negada por bucle.
- **`firma_huso_corte`** = `Europe/Prague`, CONFIRMED, fuente ADR-0050
  (`knowledge/cuentas/ftmo-2step-swing-100k.yaml:63-75`). El freno corta el día con ese huso
  (`broker.py:320`, `_dia_local`).
- **¿Coincide con las 00:00 CET/CEST en las dos estaciones? Sí, medido.** Se calcularon las 730
  medianoches del 2026-01-01 al 2027-12-31 en `Europe/Prague` (`broker._medianoche_ms`) y se
  compararon con una regla CET/CEST escrita a mano: UTC+1, y UTC+2 desde el último domingo de marzo
  a la 01:00 UTC hasta el último domingo de octubre a la 01:00 UTC.
  - 0 discrepancias;
  - 303 medianoches a las 23:00 UTC (CET) y 427 a las 22:00 UTC (CEST);
  - en los 730 días, el freno vuelve a cero justo en el milisegundo de la medianoche (un `assert`
    por día).
  - Cambios: 2026-03-29 y 2026-10-25; 2027-03-28 y 2027-10-31.
- Además, `uv run pytest tests/unit/test_freno_peticiones.py -k "vuelve_a_cero or el_dia_lo_da"`
  sale con rc 0 (2 tests).

### 0.c ADR-0068 frente a las preguntas 5 a 9

Qué hace hoy el bot dentro de la ventana de dos horas antes de un cierre largo (ADR-0068 §2):

| Caso | Qué hace | Dónde |
|---|---|---|
| Colocar una pendiente (límite o stop) | Se niega con motivo `cierre_mercado`. No llega al servidor y no cuenta | `broker.py:408-410`, antes que el freno |
| Modificar una pendiente | Se niega, y la orden sigue como estaba | `broker.py:470-472` |
| Pendiente puesta antes | Con `cierre_pendientes` = `cancelar` (DEFAULT_AMBIGUOUS bajo A-55, `knowledge/spec/parametros.yaml:1648-1660`), se cancela al empezar la ventana, antes de cualquier llenado de ese instante. Protege la cuenta, así que sale siempre y cuenta | ADR-0068 §2 |
| Posición abierta | Nada | R7 |
| Mercado cerrado, o fuera de lo que cubre el calendario | Se niega (`cierre_mercado`, `cierre_sin_calendario`) | ADR-0068 §1-2 |

- **Qué mercado usa el calendario:** el horario de EURUSD en los servidores de FTMO, y nada más.
  - `knowledge/cuentas/cierres/ftmo-2step-swing-100k.yaml`: `simbolo: EURUSD`.
  - Fuentes: la API de símbolos de FTMO (`tradingHours` de EUR/USD) y las Trading Updates.
  - No hay bolsas ni otros mercados.
  - La pausa diaria (`diario`, de las 16:55 a las 17:05 de Nueva York) dura 10 minutos: no es un
    cierre largo y no bloquea nada.
- **Prueba:** `uv run pytest tests/unit/test_cierres_de_mercado.py -k "dentro_de_la_ventana or
  pendiente_puesta_antes or con_mantener or modificar_una_pendiente or posicion_abierta or
  calendario_de_ftmo or fuera_de_lo_que_cubre"` sale con rc 0 (8 tests).
- **Fuera del encargo, solo se anota:** el calendario cubre hasta el 2026-10-07. Se renueva por
  condición (`docs/runbooks/RENOVAR-CIERRES.md`). **Conocido, punto N** del Next Action (respuesta
  del consultor, punto 3): no se cambia nada.

### 0.d Dónde vive hoy cada cosa que esta rama actualiza

**`docs/validation/FTMO-REGLAS.md`** (Estado `WAITING_FOR_USER_VALIDATION`, línea 283):
- la fila R17 de la tabla del §2, línea 64;
- R17 en el §3 (líneas 239-241) y en el §4 (270-271 y 276-277);
- tres recuadros del ticket:
  1. el traslado del 29-09, de `trabajo/sesion-03` (97-122);
  2. la respuesta literal del 29-09, de `trabajo/fuentes-ftmo` (124-160);
  3. el correo literal de Aleks del 2026-10-03, con la tabla «A quién responde cada pregunta», de
     `trabajo/fuentes-ftmo` (162-215).

El recuadro nuevo va detrás del tercero, antes del §3 (línea 217).

**`PROJECT_STATE.md`:** la línea de Technical Debt «- PENDIENTE DE FTMO: SI UN LOTE QUE VARIA CON EL
STOP…» (línea 125 en `main`).
- **Para el consultor:** esa línea lleva entre comillas una frase en inglés. No es del correo del
  2026-10-05: es el texto público de R17 (la fila 64 del §2), que la pregunta 10 del correo de Aleks
  también cita. La decisión 3 la manda pasar LITERAL a HISTORIA, y así se hará salvo que se diga otra
  cosa. **Respondido** (respuesta del consultor, punto 2): pasa literal, porque no choca con la regla
  de no copiar el correo.

**`knowledge/spec/ambiguedades.yaml`:**
- A-54 en las líneas 1507-1547, con el campo `pregunta` en 1509-1519;
- A-55 en las líneas 1548-1592, con el campo `pregunta` en 1550-1563;
- las dos son `medicion`, no bloqueantes y ABIERTAS;
- la tabla de Known Ambiguities de `PROJECT_STATE.md` no cambia, porque las dos siguen abiertas.

### 0.e Textos literales de FTMO ya commiteados (solo la lista; no se tocan, decisión 5)

- `docs/validation/FTMO-REGLAS.md`:
  - la respuesta literal del 2026-09-29, en las líneas 124-147;
  - la misma frase de esa respuesta en las líneas 150-151;
  - el correo literal de Aleks del 2026-10-03, en las líneas 162-203: lo escribió Aleks, pero su
    saludo, en la línea 169, nombra a la persona de soporte, y la línea 181 cita la frase de la
    respuesta.
- `docs/encargos/trabajo-fuentes-ftmo.md`: la respuesta en las líneas 11-17, y el correo de Aleks
  con el mismo saludo en la línea 45 y la frase en la 55.
- `docs/adr/0068-...md`, «Problema que resuelve» (líneas 88-91): una frase de la respuesta.
- La misma frase en:
  - `knowledge/spec/ambiguedades.yaml:1584` (el `literal` de la segunda fuente documental de A-55);
  - `docs/spec/ambiguedades.md:151`, que es su espejo generado;
  - `docs/validation/REABRIR-Y-FUENTE-DOCUMENTAL.md:365` y `:612`;
  - `docs/validation/FUENTES-FTMO.md`.
- Están en el historial desde `c4adb52` y `0e69da5` (`trabajo/fuentes-ftmo`).

## 1. Para el consultor: la PARADA

Las decisiones 1, 2, 3 y 5 se mantienen: la fase 0 no las contradice.
- **Pregunta 4:** coincide con `firma_huso_corte`, medido en las dos estaciones.
- **Preguntas 1-3:** el freno cuenta todo lo que llega al servidor, incluidas las órdenes que el
  servidor rechaza.
- **Preguntas 5-9:** el bot niega colocar y modificar dentro de la ventana, cancela la pendiente
  puesta antes, y el calendario es el de EURUSD.

**La decisión 4 se apoya en algo que no existe.** RITUAL.md no tiene «la regla que manda consultar
la última letra en HISTORIA» (§0.a). Propuesta:
- **(A), recomendada.** La línea literal, con su fecha y su fuente (decisión del consultor del
  2026-10-05; tras `stable/F36z` la serie sigue en `stable/F37a-<nombre>`), justo antes del bloque
  `git tag -a stable/<tag>` (`RITUAL.md:200`). No se añade nada más.
- **(B)** Lo mismo, y además la comprobación que han pedido las dos últimas órdenes de cierre, con
  sus palabras: antes de crear el tag, la última letra cerrada se mira en HISTORIA, y
  `stable/<serie><letra>-*` no existe ni en local ni en `origin`. Sería un texto nuevo en RITUAL que
  la decisión 4 no dicta palabra a palabra.

Hasta la respuesta no se escribió nada de las decisiones 1 a 4.

### 1.1 La respuesta del consultor a la fase 0 (2026-10-05), copiada tal cual

> Modelo: Opus · Esfuerzo: medio
>
> Respuesta del consultor a la fase 0 de trabajo/respuestas-ftmo (2026-10-05). Cópiala tal cual al encargo y al informe.
>
> 1. Decisión 4: opción B. Justo antes del bloque git tag -a stable/<tag> (RITUAL.md:200), con fecha 2026-10-05 y fuente «decisión del consultor; la comprobación venía de las órdenes de cierre de F36y y F36z», añade estas dos líneas literales:
>    «Antes del tag, se mira en HISTORIA el último tag cerrado y se comprueba que el nuevo no existe ni en local ni en origin; si algo falla, se para.»
>    «Agotadas las letras de una serie, se sigue en el número siguiente con la a; un número posterior a F35 es un contador, no una fase del MASTER_PLAN.»
>    Por qué: esa comprobación ya se ha ejecutado en dos cierres y no estaba escrita en el ritual. Lo que se ejecuta tiene que estar escrito.
>
> 2. La línea de R17 pasa literal a HISTORIA (decisión 3). Su frase en inglés sale del texto público de R17, no del correo del 2026-10-05, así que no choca con la regla de no copiar el correo.
>
> 3. Que el calendario de cierres llegue solo hasta el 2026-10-07 ya lo cubre el punto N del Next Action (se renueva por condición). Anótalo en el informe como «conocido, punto N» y no cambies nada.
>
> 4. Hallazgo del consultor para el informe (irá a la fila de ERRORES-RECURRENTES en el cierre):
>    importa · El consultor dio por existente en RITUAL.md una regla que solo estaba en las órdenes de cierre de F36y y F36z, citándola de memoria sin leer el fichero.
>    Lección: antes de escribir en un encargo «junto a la regla X de <fichero>», se lee esa regla en el fichero; si no se puede leer, se escribe «comprueba si existe».
>    La fase 0 lo detectó y paró, como debía.
>
> Sigue con las decisiones 1 a 4 del encargo y las comprobaciones: make check y uv run botsito state check en verde, saldo de bytes de PROJECT_STATE menor o igual que cero, y el diff releído para confirmar que no hay frases del correo ni el nombre de la persona de soporte. No toca .claude/, así que no hace falta fix/. Después, el revisor, con su informe pegado al final del informe de la rama.
>
> Rama lista para revisión, NO cerrada.

## 2. Encargo frente a lo hecho

| Encargo | Hecho | Dónde |
|---|---|---|
| Base `54c69fe`, CI 221 en verde; abrir con `abrir-rama` | Comprobado antes de abrir; abierta con su encargo, `contrato.yaml` (riesgo bajo) y el Archivo 17 de `PROJECT_STATE.md` en HISTORIA | `64b6f60` |
| Fase 0 a)-e), entregada antes de escribir | §0, con dos anexos ejecutados; PARADA en la decisión 4 | `64b6f60` |
| Decisión 1: recuadro nuevo en FTMO-REGLAS.md con la cabecera de fuente y una fila por pregunta 1-10 (lo que responde, estado, qué cambia) | Recuadro fechado (2026-10-05, `trabajo/respuestas-ftmo`) detrás del correo de Aleks y su tabla, antes del §3. Cabecera: el ticket, `support@ftmo.com`, 2026-10-05 10:29:36 UTC, que responde al correo del 2026-10-03, y las páginas Symbols y Forbidden Trading Practices. Diez filas con la paráfrasis del consultor; «qué cambia» dice «nada» en las diez, con el motivo de la decisión. Las preguntas 5 y 7 se declaran restricción ELEGIDA, más estricta que FTMO. La nota sobre la cuenta Normal se anota sin efecto. Los recuadros anteriores no se tocan | `docs/validation/FTMO-REGLAS.md` |
| Decisión 2: A-54 y A-55, solo el campo `pregunta`; siguen ABIERTAS con la misma clase y bloqueante; `spec docs --escribir` en el mismo commit | Hecho. Desviación declarada abajo | `knowledge/spec/ambiguedades.yaml`, `docs/spec/ambiguedades.md` |
| Decisión 3: la línea de R17 sale de Technical Debt y pasa literal a HISTORIA; no entra otra; saldo de bytes ≤ 0 | Sale y pasa literal bajo «# Technical Debt RESPONDIDA · sale de PROJECT_STATE.md en trabajo/respuestas-ftmo (2026-10-05)». Su frase en inglés es el texto público de R17, no del correo (punto 2 de la respuesta) | `PROJECT_STATE.md`, `docs/state/HISTORIA.md` |
| Decisión 4, opción B: las dos líneas literales justo antes de `git tag -a stable/<tag>`, con fecha y fuente | Hecho, con la fecha 2026-10-05, la fuente («decisión del consultor; la comprobación venía de las órdenes de cierre de F36y y F36z») y, del encargo, «tras `stable/F36z` la serie sigue en `stable/F37a-<nombre>`». La skill `cerrar-rama` no se toca (§0.a) | `docs/runbooks/RITUAL.md` |
| Decisión 5: los literales previos no se tocan; una línea que los liste | §0.e | — |
| Respuesta, punto 3: el calendario hasta el 2026-10-07 | Conocido, punto N del Next Action; no se cambia nada | §0.c |
| Respuesta, punto 4: el hallazgo del consultor, para el informe | §3 | — |

**Desviación (decisión 2).** La decisión dice que el campo `pregunta` «añade» la frase. El texto de
las dos decía «respuesta pendiente», que deja de ser verdad. Añadir sin quitar dejaría las dos
afirmaciones juntas, y una de ellas falsa. Así que «respuesta pendiente» se SUSTITUYE por la frase de
la decisión, y nada más del campo cambia:
- A-54: «…, respondida en parte el 2026-10-05 (FTMO-REGLAS.md, recuadro de esa fecha).»
- A-55: «…, respondida en parte el 2026-10-05 (FTMO-REGLAS.md, recuadro de esa fecha), y la pregunta 6
  sigue sin respuesta; y con la respuesta se fija cierre_pendientes …».

Estado, clase, bloqueante, parámetros, fuentes y comentarios no cambian.

## 3. Hallazgo del consultor (para la fila de ERRORES-RECURRENTES en el cierre)

**Importa.** El consultor dio por existente en RITUAL.md una regla que solo estaba en las órdenes de
cierre de F36y y F36z, citándola de memoria sin leer el fichero.
- **Lección (consultor):** antes de escribir en un encargo «junto a la regla X de <fichero>», se lee
  esa regla en el fichero; si no se puede leer, se escribe «comprueba si existe».
- La fase 0 lo detectó y paró, como debía.

## 4. Comprobaciones

- **`uv run botsito state check`**, sobre el árbol final de la rama (rc 0), sin recortar (es una
  sola línea; aquí va partida):

  ```
  OK: rama 'trabajo/respuestas-ftmo' - funcionalidad actual: `trabajo/respuestas-ftmo` EN CURSO
  (2026-10-05): punto T, la respuesta de FTMO del 2026-10-05 sin copiar el correo, y la regla de los
  tags tras F36z. Lista para revisión. Encargo docs/encargos/trabajo-respuestas-ftmo.md; informe
  docs/validation/RESPUESTAS-FTMO.md.
  ```

  También pasa dentro de cada `make check`.
- **`make check > make-check.log 2>&1`** sobre el árbol de `0e1457c`, con todo estadiado:
  - `exit=0`, ninguna línea con `failed`;
  - `CONTRATO: 13 ficheros dentro del contrato de trabajo/respuestas-ftmo (riesgo bajo, ...)`;
  - `2027 passed in 818.88s (0:13:38)`;
  - `SELLO: make check en verde sobre el arbol e8242d78a63a8731460514bb8a59dfe98cfb7d57`;
  - `PICO DE MEMORIA de make check: 290 MiB en `test``.

  El commit de los arreglos del revisor pasa por su propio `make check` antes de commitearse: el hook
  `pre-commit` no deja commitear sin el sello. Su salida no puede ir dentro del mismo commit.
- **Tests de lo que toca la rama**, antes de `make check`: 125 tests, rc 0. Cubren `test_push_atomico`, que
  lee los pushes de RITUAL; `test_guardia_claude`, cuyo ritual y runbooks pasan; `test_spec_docs_generados`;
  `test_kit` (la tabla de abiertas); `test_hoja_preguntas`; `test_project_state`; `test_historia`; y
  `test_reabrir_y_fuente_documental`.
- **`uv run botsito knowledge validate`:** rc 0 («OK: 55 ambiguedades registradas; ...»), con la `pregunta` nueva de A-54 y A-55.
- **Bytes de `PROJECT_STATE.md`:** 23.670 en `main` y 23.611 en la rama, un saldo de **−59**.
  - Al abrir subió 213: la Current Feature de la rama.
  - La línea de R17 restó 276 (23.607 en `0e1457c`).
  - «Lista para revisión» en lugar de «Falta el revisor» sumó 4.
- **Fuente:** el commit que toca `knowledge/spec/` lleva `Fuente: ADR-0067, ADR-0068`, la convención
  de `trabajo/fuentes-ftmo` para A-54 y A-55.
- **Regla de no-literal**, releyendo el diff entero de la rama frente a `main`:
  - ninguna línea añadida lleva el nombre de la persona de soporte;
  - en inglés, la búsqueda de palabras funcionales del inglés solo encuentra:
    - la cita pública de R15 en la `pregunta` de A-55, que ya estaba y sale en el diff porque cambia
      ese párrafo (también en su espejo `docs/spec/ambiguedades.md`);
    - código de los anexos.
  - La línea de R17 que pasa a HISTORIA lleva el texto público de R17 (punto 2 de la respuesta).
  - Del correo del 2026-10-05 no hay ninguna frase. Las únicas palabras inglesas del recuadro nuevo son
    los nombres de las páginas públicas y los términos de la paráfrasis del consultor (gap trading,
    rollover).
- **Sin `fix/`:** la rama no toca `.claude/`, ni hooks, ni rutas, ni código de plataforma.

## 5. Informe del revisor

Pegado tal cual (el subagente `revisor`, una pasada, sobre `64b6f60` y `0e1457c`). Lo hecho con
cada hallazgo, en §5.1.

## Informe del revisor · trabajo/respuestas-ftmo · 2026-10-05

Base: `54c69fe` (merge-base = main). Commits: `64b6f60`, `0e1457c`. `git status --short` limpio. `contrato_rama.py` sale con rc 0: «13 ficheros dentro del contrato de trabajo/respuestas-ftmo (riesgo bajo, ... 4 comprobaciones)». `uv run botsito state check` sale con rc 0: «OK: rama 'trabajo/respuestas-ftmo' - funcionalidad actual: ...».

**Veredicto: LISTA PARA REVISIÓN, con dos cosas que arreglar antes de declararla. Una es la salida de `make check` en el informe (hallazgo b-1). La otra es la frase sobre el 0,5 % de la fila 10 (hallazgo a-1). Recuento total: 0 bloquea, 2 importa, 2 menor.**

### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 1 importa, 2 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a-1 | importa | La fila 10 del recuadro nuevo dice «el riesgo fijo del 0,5 % desde el primer día (ADR-0020) es el patrón histórico de la cuenta». ADR-0020 no sostiene «desde el primer día» ni «patrón histórico». Dice lo contrario: antes del 2026-09-11 el stop costaba un 0,4 %, y el 0,5 % medido en el stop es el acuerdo de ese día. La frase es de la paráfrasis del consultor (encargo, decisión 1), pero la cita que la acompaña no la cubre. Basta atribuirla («según el consultor») o citar solo lo que ADR-0020 sí dice. | `docs/validation/FTMO-REGLAS.md:236`. `docs/adr/0020-*.md:27-28` («un **0,4 %** por operacion en vez del 0,5 % declarado») y `:31`, `:38` («La perdida por operacion sube de 0,4 % a 0,5 %»). |
| a-2 | menor | El recuadro nuevo deja afirmaciones viejas en el mismo fichero. La línea final de Estado dice «No se ha tocado `ambiguedades.yaml` ni la spec», y la rama sí toca el campo `pregunta` de A-54 y A-55. El §3 dice de R17 «El repositorio no lo contempla». Los recuadros anteriores no se pueden editar, pero estas dos frases no son recuadro. | `docs/validation/FTMO-REGLAS.md:267-268` y la última línea del fichero (`WAITING_FOR_USER_VALIDATION. No se ha tocado ...`). |
| a-3 | menor | `prueba_f37a.py` hace `git tag -a` en el clon, y eso exige identidad de git. Ni el guion ni la línea del contrato lo dicen; solo lo cuenta el informe (§0.a, «prueba-fase0»). Quien repita la comprobación del contrato sin esa pista falla. | `docs/validation/anexos/RESPUESTAS-FTMO/prueba_f37a.py:66`. `contrato.yaml`, comprobación 1. |

Comprobado sin hallazgos:
- **Contrato.** `rutas_protegidas` intactas: el diff no toca `src/`, `.claude/`, `scripts/`, `docs/adr/`, `knowledge/evidence|feedback|cases|cuentas`, `parametros.yaml` ni `strategy_spec.yaml`.
- **Comprobaciones del contrato que no escriben.**
  - `PYTHONPATH=. uv run python .../medir_freno_huso.py`: su salida coincide con `medir_freno_huso-SALIDA.txt` (1 petición rechazada que cuenta; 5 iguales dan total 4 y una negada; 730 medianoches; 303 CET y 427 CEST; 0 discrepancias).
  - `pytest test_freno_peticiones.py -k "vuelve_a_cero or el_dia_lo_da"`: pasa.
  - `pytest test_cierres_de_mercado.py -k <los 7 filtros del informe>`: pasa (8 tests).
  - `pytest` de `test_adr`, `test_historia`, `test_project_state`, `test_hoja_preguntas`, `test_reabrir_y_fuente_documental`, `test_spec_docs_generados` y `test_push_atomico`: pasan.
- **Trailer `Fuente:`.** El único commit que toca `knowledge/spec/` es `0e1457c` y lleva `Fuente: ADR-0067, ADR-0068` en el cuerpo. Los dos ADR existen en `docs/adr/`. La convención coincide con `ecc8307` y `0e69da5` de `trabajo/fuentes-ftmo`.
- **Holdout y material.** Nada de la rama toca `knowledge/cases/` ni el corpus; no hay exposiciones que declarar.
- **Regímenes de cambio.** `git diff --name-status main...HEAD` solo tiene `A` y `M` en los ficheros esperados. Ningún fichero de `knowledge/evidence/`, `knowledge/feedback/`, `data/manifests/`, transcripciones, fotogramas ni `libros.yaml`.
- **HISTORIA solo se amplía.** 219 líneas añadidas, 0 borradas. El Archivo 17 es idéntico a `git show main:PROJECT_STATE.md` salvo el apéndice final (un `diff` solo muestra líneas añadidas).
- **Ambigüedades.**
  - `docs/spec/ambiguedades.md` cambia en el mismo commit que el yaml (`0e1457c`), y `test_spec_docs_generados` pasa.
  - A-54 y A-55 siguen ABIERTAS, con la misma clase y bloqueante: los hunks del yaml (`1514` y `1558`) solo tocan `pregunta`.
  - No cambia la tabla de Known Ambiguities (`PROJECT_STATE.md:108-109`), correcto porque siguen abiertas.
  - No hay `evidencia` nueva de relleno.
  - El `literal` de la segunda fuente documental de A-55 (línea 1584) queda intacto.
- **ADR.** Ninguno tocado.
- **Informes cerrados.** `FTMO-REGLAS.md` tiene Estado `WAITING_FOR_USER_VALIDATION` (no está cerrado). Su diff son 28 líneas añadidas y 0 borradas, todas dentro de un recuadro `>`. Los tres recuadros anteriores no cambian.
- **Tres guardias de una `cita`.** La rama no añade ninguna `cita` en la spec.
- **Cifras.** Ninguna cifra nueva en forma ejecutable.
- **PROJECT_STATE.**
  - 23.670 bytes en main, 23.607 en la rama: saldo **−63**, ≤ 0 y por debajo de 25.000.
  - Del informe: +213 al abrir (64b6f60 = 23.883) y −276 por la línea de R17 (cuenta 276 bytes con salto de línea). Cuadra.
  - Solo sustituye lo que deja de ser verdad; no hay «Lo anterior:».
- **R17 a HISTORIA.** `sha256sum` de la línea en `main:PROJECT_STATE.md` y de su copia nueva en `HISTORIA.md`: ambos `a7b11cc69b48...`, y `od -c` muestra los mismos bytes finales. La línea ya no está en `PROJECT_STATE.md`.
- **`.claude/`.** Sin cambios. No hace falta `fix/`.
- **Informe.** Existe, acaba en `## Estado` con «EN CURSO ... NO cerrada».
- **Citas del informe contra su fuente** (seis, todas correctas):
  - `broker.py:320`, `:406-414`, `:411-421`, `:470-472` y `:473-484`.
  - `parametros.yaml:1648-1660`.
  - `ftmo-2step-swing-100k.yaml:63-75`.
  - ADR-0067 §3 (cancelar y cerrar cuentan).
  - `ambiguedades.yaml:1524-1526`.
  - `gh run view 37383049905` da `success`, run 221, `headSha` 54c69fe.
  - El único hallazgo de citas es a-1 (ADR-0020).

### Eje (b) · Encargo
Resumen: 0 bloquea, 1 importa, 0 menor. Requisitos: 17 hechos, 1 parcial, 0 no hechos (1 «hecho de otra forma», declarado; 1 pendiente del propio revisor).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Comprobar base y CI, abrir con `abrir-rama` (encargo copiado, contrato, Archivo en HISTORIA) | Hecho | `docs/encargos/` presente; `contrato.yaml` pasa; el Archivo 17 es copia exacta de main; `gh run view` da run 221 en `success` sobre 54c69fe. |
| 2 | Fase 0 a) lectores del tag | Hecho (reproducción parcial, ver «No pude comprobar») | Informe §0.a. `guardia.py:1293-1298`, `:1378` y `:1783` solo miran el prefijo `stable/` y las banderas `-d/-f`. `cli.py:96-102` toma el primer tag sin mirar su forma. `cli.py:166` (`-\s*(F\d{2})\b`): reproducido, `- F37a-...` no casa y `- F37 algo` sí. `ids_de_funcionalidad`: reproducido, 35 ids, ni F36 ni F37. El grep propio no encuentra ningún lector del formato que falte: `src` y `scripts` solo tienen `cli.py:97`, `historial.py:37` (ancla `stable/F06`) y `knowledge.py` (ancla); `.claude` solo `guardia.py`, `settings.json` (`stable/*`) y `SKILL.md:32`; `.github` solo `ci.yml:23`. `git for-each-ref refs/tags/stable/F37*` en el repo real: 0. `git ls-remote --tags origin "stable/F37*"`: vacío. |
| 3 | Fase 0 b) ADR-0067 y 1-4 | Hecho | `medir_freno_huso.py` reproducido. Una orden rechazada por el servidor cuenta; la negada por el bot no. `firma_huso_corte` = `Europe/Prague`; 0 discrepancias en 730 medianoches; el cambio de hora cae en 2026-03-29, 2026-10-25, 2027-03-28 y 2027-10-31. |
| 4 | Fase 0 c) ADR-0068 y 5-9 | Hecho | Tabla de §0.c cuadra con `broker.py:408-410` y `:470-472`, y con `cierre_pendientes` = `cancelar` en `parametros.yaml:1648-1660`. El calendario es solo de EURUSD. |
| 5 | Fase 0 d) y e) | Hecho | §0.d y §0.e. Los literales previos listados quedan intactos: el diff de `FTMO-REGLAS.md`, del encargo anterior y del yaml no los toca. |
| 6 | Decisión 1: recuadro nuevo con cabecera de fuente y tabla 1-10 | Hecho | `FTMO-REGLAS.md:217-243`. Cabecera: ticket, `support@ftmo.com`, 2026-10-05 10:29:36 UTC, responde al correo del 2026-10-03, páginas Symbols y Forbidden Trading Practices. Diez filas con tres columnas; «qué cambia» dice «Nada» en las diez; 5 y 7 declaradas restricción ELEGIDA, más estricta que FTMO; nota de la cuenta Normal «sin efecto». 0 líneas borradas. |
| 7 | Decisión 2: A-54 y A-55, solo `pregunta`; siguen ABIERTAS; `spec docs --escribir` en el mismo commit | Hecho de otra forma, declarado | Informe §2, «Desviación (decisión 2)»: «respuesta pendiente» se sustituye en vez de solo añadir. Está bien declarada: dice qué cambia y por qué (añadir sin quitar dejaría una afirmación falsa) y cita el texto exacto de las dos. La frase de la decisión y la «6 sigue sin respuesta» están. Diff del yaml: 5 líneas añadidas, 3 quitadas, todas de `pregunta`. `docs/spec/ambiguedades.md` va en el mismo commit y `test_spec_docs_generados` pasa. |
| 8 | Decisión 3: la línea de R17 sale y pasa literal; no entra otra; saldo ≤ 0 | Hecho | La línea no está en `PROJECT_STATE.md`. Mismo sha256 que en main. Saldo −63. |
| 9 | Decisión 4 (opción B, respuesta punto 1): dos líneas literales antes de `git tag -a`, con fecha y fuente | Hecho (byte a byte) | Ver sección 2 abajo. |
| 10 | Decisión 5: literales previos sin tocar y una línea que los liste | Hecho | §0.e. |
| 11 | Respuesta punto 2: R17 pasa literal | Hecho | Ver requisito 8. |
| 12 | Respuesta punto 3: «conocido, punto N» del calendario hasta el 2026-10-07, sin cambios | Hecho | Informe §0.c, última viñeta. |
| 13 | Respuesta punto 4: hallazgo del consultor en el informe (a la fila de ERRORES-RECURRENTES en el cierre) | Hecho | Informe §3. `ERRORES-RECURRENTES.md` no se toca, correcto (va en el cierre). |
| 14 | «Cópiala tal cual al encargo y al informe» | Hecho | `diff` de `encargo:77-97` frente a `informe:174-194`: idéntico. |
| 15 | Comprobaciones: `make check` y `state check` en verde, con su salida en el informe | Parcial | `state check`: el informe (§4) pone «OK: rama ... - funcionalidad actual: ...», con puntos suspensivos. `make check`: el informe (§4) dice «El resultado (exit, tests y SELLO) va en el commit del revisor (§5)». No hay `make-check.log` en el árbol de trabajo y el informe no trae ni el exit, ni los tests, ni la línea SELLO. Yo reproduje `state check` rc 0. |
| 16 | No-literal declarado y trailer `Fuente:` | Hecho | Ver sección 1 abajo y «Comprobado» del eje (a). |
| 17 | NO cambia: motor, broker, freno, spec ejecutable, parámetros, evidence, cifras; no se abre ni se cierra ninguna ambigüedad | Hecho | Ningún fichero de `src/` ni de `knowledge/` salvo `ambiguedades.yaml` (solo `pregunta`). `parametros.yaml` y `strategy_spec.yaml` intactos. |
| 18 | Revisor y su informe pegado al final | Pendiente (lo hace quien llama) | `docs/validation/RESPUESTAS-FTMO.md:257-259` tiene el hueco «(Se pega al terminar.)». Este informe no lo pego yo. |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b-1 | importa | El encargo pide `make check` y `state check` «en verde, con su salida en el informe». El informe no trae la salida de `make check` (exit, tests, SELLO, PICO DE MEMORIA) y la de `state check` va recortada. Declarado como pendiente, pero hay que añadirlo antes de declarar lista la rama. | `docs/validation/RESPUESTAS-FTMO.md:230-234`. `make-check.log` no está en el árbol de trabajo (`ls: cannot access 'make-check.log'`). |

Fuera del encargo (cada cosa justificada, sin hallazgo):
- `contrato.yaml`: lo exige `abrir-rama`.
- Las líneas de `PROJECT_STATE.md` (rama actual, Current Feature, «ninguna desde el Archivo 17»): son del ritual de apertura.
- La frase «Tras `stable/F36z` la serie sigue en `stable/F37a-<nombre>`» de RITUAL: sale de la decisión 4 original.
- El párrafo «Lo que eso deja» del recuadro: resume lo que el encargo manda.

### 1. Regla de no-literal (aparte)
**Sin hallazgos.**
- (i) El nombre de la persona de soporte, tal como aparece en el saludo del correo de Aleks (`FTMO-REGLAS.md:169`), no aparece en ninguna línea añadida (`git diff -U0 main..HEAD`: 0 coincidencias), en ningún mensaje de commit (0) ni en ninguna ruta (0). En el árbol de `HEAD` solo está en `docs/encargos/trabajo-fuentes-ftmo.md` y `docs/validation/FTMO-REGLAS.md`, y en `main` en los mismos dos ficheros: es lo que ya estaba.
- (ii) Frases en inglés de las líneas añadidas. Se excluyeron los anexos de código y el Archivo 17, que es copia exacta de main.
  - La cita pública de R15 en la `pregunta` de A-55 («perform gap trading [...] two hours or less before a relevant financial market is closed ...»): ya estaba en main y sale en el diff porque cambia ese párrafo.
  - «relevant financial market» y «opening», de esa misma cita pública de R15.
  - La línea de R17 en HISTORIA («substantially larger position sizes»): texto público de R17 (`FTMO-REGLAS.md:64`), ya en main.
  - Nombres de páginas públicas (Symbols, Forbidden Trading Practices) y términos de la paráfrasis del consultor (gap trading, rollover, Normal, Swing).
  - `support@ftmo.com`, el ticket y la fecha y hora de llegada, permitidos por el encargo.
  - Ninguna es una frase nueva del correo del 2026-10-05.
- Los mensajes de los dos commits no llevan frases del correo.

### 2. La línea de RITUAL tal cual (aparte)
**Hecho; coinciden byte a byte.**
- Comparación por programa (`python`, `in` sobre los textos leídos con `newline=''`, y sha256 de cada frase del encargo, punto 1 de la respuesta):
  - «Antes del tag, ...» (145 bytes UTF-8): aparece exactamente 1 vez en `RITUAL.md`, como línea `- ` + la frase y nada más (`ln == '- ' + l`: True).
  - «Agotadas las letras ...» (148 bytes UTF-8): ídem.
  - No hay `\r` en el fichero.
- Posición: `RITUAL.md:200-206` (bloque «**Antes del tag**»), antes de la única aparición de `git tag -a stable/<tag>` (`:209`).
- Fecha 2026-10-05 y fuente «decisión del consultor; la comprobación venía de las órdenes de cierre de F36y y F36z», presentes. La fuente está partida en dos líneas por el ajuste de línea (`la` / `comprobación`), sin cambio de contenido. La frase de fuente del encargo no se pudo comparar por programa a la manera de las otras (`in` da False), solo por diferencia de salto de línea.
- La afirmación «un número posterior a F35 es un contador» cuadra con `docs/plan/MASTER_PLAN.md:111-113` (la tabla acaba en F35).

### 3. La prueba de F37a (aparte)
**Hecho en lo que pude reproducir; no pude re-ejecutar la parte que crea el tag en el clon.**
- `solo_lectura.py` me bloqueó `git clone` («cambia el repositorio o sus referencias»), y también un `git tag -a` escrito dentro de un guion en línea. No lo rodeé.
- Reproducido a mano, sin clon:
  - Regla de Completed Features de `cli.py:166`: `- F37a-respuestas-ftmo` no casa, `- F36z-...` no casa y `- F37 algo` sí.
  - `ids_de_funcionalidad`: 35 ids, F36 y F37 ausentes.
  - `guardia.py`: solo mira prefijo `stable/`, `refs/tags/` y banderas `-d/--delete/-f/--force`; no tiene patrón de letra ni de número (líneas 1293-1298, 1378, 1783, y grep de `F\d` en `.claude/hooks/*.py` sin resultados sobre tags).
- Del anexo `prueba_f37a-SALIDA.txt` (no re-ejecutado): `decidir` deja pasar las seis órdenes del ritual con F37a y bloquea las cuatro que borran o mueven el tag; en el clon, `_ultimo_tag_estable` da `('stable/F37a-respuestas-ftmo', 'f8b291c')` y `state_check` da 0. El diseño de la prueba es correcto: el tag va solo en el clon, sobre `f8b291c`, y reproduce el estado posterior a un cierre.
- Lectores del encargo que la fase 0 no listó: ninguno.
- `git for-each-ref "refs/tags/stable/F37*"` en el repo real: 0 líneas. `git tag -l "stable/F37*"` no se pudo ejecutar con ese comando por el hook; lo sustituí por `for-each-ref`, con el mismo resultado: vacío. `git ls-remote` a `origin` también vacío.

### Lo que no pude comprobar
- La sección 4 de `prueba_f37a.py` (crear el tag en un clon y correr `state_check` ahí): el hook de solo lectura bloquea `git clone` y `git tag`. Hay que repetirla fuera, con identidad local (`user.name`/`user.email`) en el clon.
- `make check`: no lo ejecuté (escribe). Tampoco hay `make-check.log` en el árbol, así que no pude leer la línea SELLO ni PICO DE MEMORIA. Cuento con lo que dices (exit 0, 2027 passed, SELLO sobre `e8242d78…`), no verificado por mí.
- El correo del 2026-10-05: no lo tengo, así que no puedo comprobar que la paráfrasis del consultor sea fiel; solo que el repositorio no lleva texto del correo ni el nombre de la persona de soporte.
- Los números de línea de `test_guardia_claude.py` que cita el informe (§0.a): no los verifiqué uno a uno.

### Comandos ejecutados
`git branch --show-current`; `git merge-base main HEAD`; `git log --format='%h %s' main..HEAD`; `git diff --stat main...HEAD`; `git status --short`; `uv run python scripts/contrato_rama.py` (dos veces); `cat contrato.yaml`; `git diff main...HEAD -- RITUAL.md ambiguedades.yaml ambiguedades.md PROJECT_STATE.md`; `git log --format='=== %h%n%B' main..HEAD`; `git show --stat` de cada commit; `git diff --name-status` y `--numstat main...HEAD`; `git diff main...HEAD -- FTMO-REGLAS.md`; búsqueda del saludo en `FTMO-REGLAS.md` y conteos del nombre en líneas añadidas, mensajes, rutas y árboles (con el nombre en literal); `diff` de `git show main:PROJECT_STATE.md` frente al Archivo 17; `wc -c` de PROJECT_STATE en main, 64b6f60 y HEAD; sha256 y `od -c` de la línea de R17; script `python` de comparación de las dos líneas de RITUAL con el encargo; `diff` del encargo frente al informe (líneas 77-97 frente a 174-194); lectura del encargo, el informe y los dos anexos con Read; greps de `stable/` y `F\d` en `src`, `scripts`, `.claude`, `.github`, `tests`; `sed -n` de `cli.py:90-200`, `guardia.py`, `broker.py`, `parametros.yaml`, `ftmo-2step-swing-100k.yaml`, `ambiguedades.yaml`, `RITUAL.md`, `FTMO-REGLAS.md`; `uv run botsito state check`; `uv run botsito spec docs --check` (no existe esa opción, rc 2, sin efecto); `PYTHONPATH=. uv run python .../medir_freno_huso.py`; `uv run pytest` de los ficheros y filtros citados arriba (con `-p no:cacheprovider`); `uv run python` en línea (ids_de_funcionalidad y regex de Completed Features); `git for-each-ref refs/tags/stable/F37*` y `--sort=-creatordate --count=3`; `git ls-remote --tags origin "stable/F37*"`; `gh run view 37383049905`; `grep` del trailer `Fuente:` en `git log` de main; `git grep -i` del nombre en HEAD y main. Bloqueados por el hook y no ejecutados: redirección a fichero, `git clone`, `tee` y el `git tag` dentro del guion en línea.

### 5.1 Lo hecho con cada hallazgo

- **a-1 (importa), arreglado.** La fila 10 del recuadro nuevo de `FTMO-REGLAS.md` atribuye la frase
  al consultor («Según el consultor (encargo de `trabajo/respuestas-ftmo`, decisión 1), ...») y cita
  de ADR-0020 solo lo que dice: el 0,5 % medido en el stop, desde el 2026-09-11. El recuadro es de
  esta rama y no está cerrado en `main`, así que se corrige en él.
- **a-2 (menor), arreglado sin editar el cuerpo.** El recuadro nuevo declara al final que dos frases
  del informe de origen dejan de ser verdad desde él: la del Estado (`ambiguedades.yaml`) y la del §3
  sobre R17. El cuerpo no se toca.
- **a-3 (menor), arreglado.** `prueba_f37a.py` pone él mismo la identidad local al clon
  (`user.name` y `user.email`). Repetido sobre un clon nuevo de `main` sin configurar nada a mano, sale
  con rc 0 y la salida es idéntica a `prueba_f37a-SALIDA.txt` (`diff` vacío). Después,
  `git tag -l "stable/F37*"` en el repositorio real sigue vacío. Con eso queda re-ejecutada también la
  sección 4 que el revisor no pudo correr.
- **b-1 (importa), arreglado.** El §4 trae la salida de `make check` de `0e1457c` (exit, CONTRATO,
  2027 passed, SELLO y PICO DE MEMORIA) y la línea entera de `state check` sobre el árbol final.
- **Una cifra que el revisor midió cambia tras su pasada:** el saldo de `PROJECT_STATE.md` pasa de
  −63 a −59 (§4), porque la Current Feature dice ahora «Lista para revisión».

## 6. Orden de cierre del consultor (2026-10-05)

Copiada tal cual:

> Modelo: el que tengas · Esfuerzo: medio
>
> Orden de cierre de trabajo/respuestas-ftmo (consultor, 2026-10-05). Revisada: último commit 2bc23a1, make check sellado con 2027 tests pasados. La rama solo toca documentación y no lleva fix/ ni CI de Linux. Cópiala tal cual al informe y al registro del cierre en HISTORIA. El diagnóstico tras cerrar la terminal confirmó que no se había ejecutado ningún paso del ritual.
>
> TAG: stable/F37a-respuestas-ftmo. Es el primero de la serie F37 (RITUAL.md, las dos líneas de esta rama). Comprueba antes que el último tag cerrado en HISTORIA es stable/F36z-ventana-no-citable y que stable/F37a-* no existe ni en local ni en origin. Si algo falla, para.
>
> DESVIACIÓN ACEPTADA
> 1. En A-54 y A-55 se sustituyó «respuesta pendiente» por la frase nueva en vez de añadirla, porque juntas el campo afirmaría algo falso. El resto del campo no cambia.
>
> HALLAZGOS PARA ERRORES-RECURRENTES (fila de la rama)
> - importa · Del consultor (ya en el §3 del informe): dio por existente en RITUAL.md una regla que solo estaba en las órdenes de cierre de F36y y F36z. Lección: antes de escribir en un encargo «junto a la regla X de <fichero>», se lee esa regla en el fichero; si no se puede leer, se escribe «comprueba si existe». La fase 0 lo detectó y paró, como debía.
> - Del revisor: nada que el consultor viera y él no. Sus a-1, a-2, a-3 y b-1 están arreglados.
>
> NEXT ACTION EN EL COMMIT DE ESTADO
> - T sale, porque pasa a HISTORIA con este cierre.
> - Los demás puntos no cambian.
>
> RITUAL
> Sigue docs/runbooks/RITUAL.md con la skill cerrar-rama:
> - registro del cierre y fila de ERRORES-RECURRENTES en la rama;
> - merge y tag;
> - commit de estado;
> - make check sellado;
> - push atómico de main y el tag (si el clasificador lo bloquea, para y dame el comando con «!»);
> - CI de main en verde;
> - borrar trabajo/respuestas-ftmo en local (no hay fix/ remota).
> No toques .git/REBASE_HEAD: es un resto del 2026-09-23 y no hay ningún rebase en curso.
>
> INFORME FINAL
> Sha de main, tag y el sha al que apunta, run de la CI de main, ramas que quedan y tamaño de PROJECT_STATE.

T sale de `PROJECT_STATE.md` en el commit del contrato, en la rama, y no en el de estado: así lo
manda `RITUAL.md` (punto 3 de «el contrato sale de la rama»), porque su texto entra en HISTORIA en el
mismo commit y en `main`, tras el tag, HISTORIA ya no puede cambiar. El resultado en `main` es el que
pide la orden. Mismo camino que R en `trabajo/ventana-ev-v9-003456`.

## Estado

Lista para revisión, NO cerrada (2026-10-05). Fase 0, decisiones 1 a 4 y la respuesta del
consultor aplicadas; el revisor pasado (0 bloquea, 2 importa, 2 menor), con los cuatro hallazgos
arreglados (§5.1). Sin `fix/`: la rama no toca `.claude/`. El cierre será el primero con
`stable/F37a-respuestas-ftmo` (§0.a).
