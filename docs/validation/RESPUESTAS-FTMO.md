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
(la del repositorio es local), así que se le dio una propia (`prueba-fase0`). Después de la prueba,
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

- **`uv run botsito state check`** sobre el árbol de este commit:
  `OK: rama 'trabajo/respuestas-ftmo' - funcionalidad actual: ...`.
- **`make check > make-check.log 2>&1`:** se corre con todo estadiado antes del commit, y el hook
  `pre-commit` rechaza el commit sin su sello. El resultado (exit, tests y SELLO) va en el commit del
  revisor (§5).
- **Tests de lo que toca la rama**, antes de `make check`: 125 tests, rc 0. Cubren `test_push_atomico`, que
  lee los pushes de RITUAL; `test_guardia_claude`, cuyo ritual y runbooks pasan; `test_spec_docs_generados`;
  `test_kit` (la tabla de abiertas); `test_hoja_preguntas`; `test_project_state`; `test_historia`; y
  `test_reabrir_y_fuente_documental`.
- **`uv run botsito knowledge validate`:** rc 0 («OK: 55 ambiguedades registradas; ...»), con la `pregunta` nueva de A-54 y A-55.
- **Bytes de `PROJECT_STATE.md`:** 23.670 en `main` y 23.607 en la rama, un saldo de **−63**.
  - Al abrir subió 213 (+213): la Current Feature de la rama.
  - La línea de R17 restó 276.
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

(Se pega al terminar.)

## Estado

EN CURSO (2026-10-05). Decisiones 1 a 4 aplicadas; falta el revisor. NO cerrada.
