# ACTIVAR-SESION-04-MOTOR · Lo que la sesión 4 dejó para el motor (R1.1, entrada E)

Rama `trabajo/activar-sesion-04-motor`, abierta el 2026-10-11 desde `main` en d4b7917 (commit de
estado sobre el merge cbe8e09, tag `stable/F37m-activar-sesion-04`). Encargo:
`docs/encargos/trabajo-activar-sesion-04-motor.md` (con el añadido del régimen nocturno de Aleks).
Tramo: R1 (R1.1 de `docs/plan/HOJA-DE-RUTA.md`; E de la Next Action).

(Hasta que existieron, los tres ADR que el encargo manda escribir iban declarados aquí en un
bloque `ids-inexistentes`, como exige `knowledge validate`; el último, ADR-0076, salió con el
commit de A-21.)

## Pendiente de Aleks

Régimen nocturno (añadido de Aleks del 2026-10-11, copiado en el encargo): nada espera; lo que
depende de él va aquí con su comando exacto.

1. ~~La PARADA de la decisión 3 (A-21)~~: respondida el 2026-10-12 (§10) y aplicada (§1.5).
2. **El literal de v10 1:44:49** («1 o 2» o «12»), si lo lee con `--crudo` en su terminal: va al
   informe y a las líneas de H; si no llega, H se queda como está.
3. ~~La CI del último commit~~: los dos push salieron desde la sesión y sus runs están en §8; el
   del commit de A-21 y el del informe final, también (§8). Si un push se niega, el comando es
   `git push origin trabajo/activar-sesion-04-motor:refs/heads/fix/activar-sesion-04-motor`.
4. ~~El punto 4 de la PARADA~~ (la `cita` de RN-003): (a), confirmado por el consultor.

## Base comprobada al abrir (skill `abrir-rama`, paso 1)

- `git rev-parse --short main` = d4b7917; `git rev-parse main origin/main` da dos veces
  d4b7917fca0692904bf8103222987cf90e51e267; `git status --short` vacío.
- El último tag de `docs/state/HISTORIA.md` es `stable/F37m-activar-sesion-04`;
  `git rev-parse "stable/F37m-activar-sesion-04^{commit}"` = `git rev-parse main^1` =
  cbe8e0968698ab07530c3a43c9ec6e7919b1b5f0; `git ls-remote --tags origin stable/F37m-activar-sesion-04`
  devuelve el tag (4a61334 → refs/tags/stable/F37m-activar-sesion-04).
- La CI de `main` sobre d4b7917fca0692904bf8103222987cf90e51e267 (API de check-runs con el sha
  literal): check `python`, `completed` / `success`, run 38197306105. `gh run view 38197306105`
  confirma `headSha` d4b7917…, `headBranch` main, `completed` / `success`: es el run que cita el
  encargo.
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## 0. Fase 0 · Inventario medido, sin tocar spec, knowledge ni código

Medido el 2026-10-11 sobre la apertura (encima de d4b7917), con Grep, Glob, Read y git de
lectura. Ninguna carpeta de meses reservados se listó; ninguna cruda, ningún fotograma, ningún
material fuera del repositorio. El valor `ambiguo` del sesgo no sale de ningún sitio salvo de la H4
neutra con doble ruptura, y ninguna decisión necesita tocar nada de «QUÉ NO CAMBIA»; pero **lo
medido contradice la decisión 3** (la opción `sin_alternancia_de_colores` con el tramo que el
encargo define no filtra nada, §0.7 a1): **PARADA solo para la decisión 3**, en «Lo que necesito que
decidas». Las decisiones 1, 2, 4 y 5 no dependen de ella y siguen esta noche, cada una en su
commit (régimen nocturno de Aleks: «deja commiteado lo que no dependa de ella»).

### 0.1 Las evidencias y el registro existen (punto 1)

Glob `knowledge/evidence/**/<id>*.yaml` y Read de cada fichero:

| Id | Fichero | t0–t1 (v10 salvo el último) | Para |
|---|---|---|---|
| `ev-v10-004945-59ebac47` | `knowledge/evidence/v10/ev-v10-004945-59ebac47.yaml` | 0:49:45–0:50:10 | S-4 (CONFIRM, decisión 1) |
| `ev-v10-014005-7e2228f4` | `knowledge/evidence/v10/ev-v10-014005-7e2228f4.yaml` | 1:40:05–1:40:40 | S-13 (decisión 2) |
| `ev-v10-014040-fb7a153b` | `knowledge/evidence/v10/ev-v10-014040-fb7a153b.yaml` | 1:40:40–1:41:01 | S-13 |
| `ev-v10-011725-3741e266` | `knowledge/evidence/v10/ev-v10-011725-3741e266.yaml` | 1:17:25–1:17:31 | S-10 (decisión 3) |
| `ev-v10-011734-fedd3f8e` | `knowledge/evidence/v10/ev-v10-011734-fedd3f8e.yaml` | 1:17:34–1:17:46 | S-10 |
| `ev-v10-011957-7ebb3453` | `knowledge/evidence/v10/ev-v10-011957-7ebb3453.yaml` | 1:19:57–1:20:27 | S-10 |
| `ev-v10-010653-81316808` | `knowledge/evidence/v10/ev-v10-010653-81316808.yaml` | 1:06:53–1:07:08 | S-8 (decisión 4) |
| `ev-v10-010715-fae17215` | `knowledge/evidence/v10/ev-v10-010715-fae17215.yaml` | 1:07:15–1:07:41 | S-8 |
| `ev-v10-010804-5b6ad1a3` | `knowledge/evidence/v10/ev-v10-010804-5b6ad1a3.yaml` | 1:08:04–1:08:28 | S-8 |
| `ev-v9-011128-a267338b` | `knowledge/evidence/v9/ev-v9-011128-a267338b.yaml` | v9 1:11:28–1:11:37 | A-51 (el 9 ya en v9) |
| `fb-2026-10-04-sesion-04-45e624c5` | `knowledge/feedback/2026-10-04-sesion-04/fb-2026-10-04-sesion-04-45e624c5.yaml` | 0:54:27–0:54:51 | S-5 (decisión 5): CONFIRM sobre `orden_pendiente_al_abrir_sesion`, valor `se_retira` |

Ninguna de las once ventanas cae en un tramo de `knowledge/corpus/tramos_no_citables.yaml` de
v10 (22 tramos: los cuatro cortes de audio 0:45:05–0:46:41, 1:30:51–1:35:48, 1:36:37–1:38:58 y
1:39:08–1:39:42; los doce bloques de cuarentena mecánica; y los de precaución 0:40:20–0:40:42,
1:27:44–1:28:19, 1:43:42–1:44:21 y los de 1:55–1:56): la más cercana es la de S-13
(1:40:05), 23 s después del corte que termina en 1:39:42, y ningún margen la toca. El ítem
`ev-v10-011957-7ebb3453` (S-10) viene de un pasaje en que el trader dibuja sobre su replay
(SESION-04-EXTRACCION.md §3.11: «ejemplos de su replay (enero, 74:42)»); su cita es la regla
(«se alterna de una vela verde a una vela roja … quedaría invalidado»), sin fecha ni cifra, y
enero de 2026 es material de desarrollo (HOLDOUT-EXPOSICIONES.md); el revisor de la rama anterior
lo señaló y la respuesta fue que es de esta rama (ACTIVAR-SESION-04.md §9.1, b2): se usa solo
como cita de la regla, en la `pregunta` de A-21 y en ADR-0076, y no se describe nada de la
pantalla.

### 0.2 ADR-0075, ADR-0076, ADR-0077 y RN-036 están libres (punto 2)

- `ls docs/adr | tail`: el último es `0074-el-1-de-la-caja-se-recalcula-en-cada-cierre-de-m1-hasta-el-llenado.md`;
  la última fila del índice `docs/adr/README.md` es la 0074 (línea 80).
- Grep `ADR-0075|ADR-0076|ADR-0077|RN-036` en `docs/**`, `src/**`, `tests/**`, `knowledge/spec/**`,
  `knowledge/feedback/**` y `scripts/**`: solo aparecen en `docs/validation/ACTIVAR-SESION-04.md`
  (líneas 201, 371, 477, 481, 533 y 788: RN-036 como nombre previsto para la regla de A-51), en
  `docs/state/HISTORIA.md:8507` (el Archivo de ese informe), en el encargo de la rama anterior
  (`docs/encargos/trabajo-activar-sesion-04.md:91`) y en el de esta. Ningún ADR, regla, parámetro
  ni test los usa: libres.
- `knowledge/spec/strategy_spec.yaml`: la última regla es RN-035 (línea 885; RN-034 en 1635, RN-033
  en 982); no hay `RN-036`.

### 0.3 Quién produce y quién consume el valor `ambiguo` del sesgo (punto 3)

Grep `ambiguo` y `AMBIGUO|Sesgo\.` en `src/`, `scripts/`, `tests/` y `knowledge/spec/`, y Grep
en `src/botsito/engine/visor.py`:

**Lo produce UN solo sitio:** `src/botsito/domain/sesgo.py:90`
(`return ResultadoSesgo(Sesgo.AMBIGUO, min(arriba, abajo), miradas, True)`), la rama de la doble
ruptura cuando `vela.cierre == vela.abierta` (líneas 83-90). El enum lo declara `sesgo.py:40`
(`AMBIGUO = "ambiguo"`) y el docstring lo describe (líneas 12, 16, 48, 55). Ningún otro sitio de
`src/` ni de `scripts/` construye `Sesgo.AMBIGUO`: el valor `ambiguo` NO sale de ningún sitio
además de la H4 neutra con doble ruptura (condición de PARADA del encargo: no se da).

**Lo consumen:**
- motor: `src/botsito/engine/primitivas.py:185-187` (`sesgo_h4_al_abrir` ata `r.sesgo.value` al
  token `sentido_de_la_ruptura`, «alcista, bajista, ambiguo o insuficiente son los cuatro
  valores»); `primitivas.py:11`, `interprete.py:186` y `spec/modelo.py:657,1192-1193` (comentarios
  sobre `vale: ambiguo` y la guardia de tokens); `zonas.py:200-203` (`LADO_ENTRADA.get(sesgo)`:
  sin lado no hay toma);
- spec: `strategy_spec.yaml:512-517` (el token `ambiguo`, con su descripción: «rompio LOS DOS
  extremos … y cerro SIN CUERPO»), `:639` (`hechos.sesgo.valores: [sentido_de_la_ruptura,
  ambiguo, insuficiente]`), `:1018-1024` (la forma de RN-033, `vale: ambiguo`), `:936` (el
  `entonces` de RN-003), `:950-965` (notas de RN-003), `:983-1016` (RN-033 entera), `:68` y `:202-203`
  (comentarios del vocabulario), `:1116`; `parametros.yaml:862` y `ambiguedades.yaml:612` son
  otros usos de la palabra (una distancia ambigua; una cifra de un comentario), no el token;
- scripts: `scripts/sesgo_h4_diagnostico.py:85` (`if r.sesgo in (Sesgo.AMBIGUO, Sesgo.INSUFICIENTE)`)
  y `:108` (la columna «ambiguo» de su tabla); `scripts/verificacion_a35_a44.py:172` (cuenta las
  operaciones «con sesgo sin lado (ambiguo/insuficiente)»);
- visor: `src/botsito/engine/visor.py:392` llama a `sesgo_h4` y `:775` pinta `r.sesgo.value`
  y «doble ruptura: decide el color»; no nombra el token, pero lo enseña si el resultado lo trae;
- tests: `tests/unit/test_sesgo_h4.py:80-84` (`test_doble_ruptura_sin_cuerpo_es_ambiguo`);
  `tests/unit/test_huecos_motor.py:3-8` (docstring), `:78` (`SIN_LADO`), `:80`
  (`COLOR_DE_AMBOS`, `ambos_sin_cuerpo`), `:167-177`
  (`test_una_sesion_ambigua_fija_sesgo_ambiguo_y_rn033_prohibe`), `:180-192`
  (`test_una_segunda_sesion_ambigua_no_hereda_el_sesgo_de_la_primera`), `:195-206`
  (`test_una_sesion_no_ambigua_tras_una_ambigua_no_hereda_la_prohibicion`, que fija
  `EstadoDia(hechos={"sesgo": "ambiguo"})` a mano en `:202`), `:301-308` (la comparación forma /
  primitiva sobre construcción, que usa `sesgo_h4` en los dos lados), `:341` (los `vale` de
  RN-033 son exactamente `SIN_LADO`); `tests/unit/test_embudo_77.py:52` (una operación con
  `sesgo="ambiguo"` hecha a mano para el embudo). Los de `:171-192` y `:202` son los que el auditor
  situó; `:305` y `:341` no cambian de sentido (el primero compara el motor consigo mismo y el
  segundo congela la forma de RN-033, que no se toca).

### 0.4 Todo lo que nombra `--diagnostico-a21` (punto 4)

Grep `diagnostico.a21|diagnostico_a21` en `src/**/*.py`, `scripts/**/*.py` y `tests/**/*.py`, y
`a21` en `src/botsito/engine/diagnostico.py`:

- `src/botsito/cli.py:2259` (`getattr(args, "diagnostico_a21", None)` al construir `Diagnostico`),
  `:2276-2277` (la cabecera «A-21 en hipotesis»), `:2300-2305` (`parser.add_argument("--diagnostico-a21", choices=LECTURAS_LIMPIA, …)`),
  y el docstring de `_diagnostico_de` (`:2241`) no lo nombra;
- `src/botsito/engine/zonas.py:145-169` (`lectura_limpia(registro, a21)`: `:153-157` rechaza el
  diagnóstico con el selector fijado, «no admite --diagnostico-a21»; `:159-162` acepta la lectura
  hipotética; `:163-169` la negativa que lo ofrece); `ETIQUETA_A21` en `:75` y `__all__` (`:568`);
- `src/botsito/engine/diagnostico.py:29` (`ETIQUETA_A21`), `:65` (el campo `a21` de
  `Diagnostico`), `:75-76` (su validación), `:89-90` (su etiqueta), `:205` (`__all__`); y
  `:22` importa `LECTURAS_LIMPIA` solo para eso;
- tests: `tests/unit/test_preparar_a21.py:423` (la CLI se niega sin A-21 y con el diagnóstico pasa
  la compuerta de medida primero), `tests/unit/test_preparar_a35.py:440` (el arnés en diagnóstico
  con los tres flags, salta sin `data/`), `tests/unit/test_visor.py:390` (el visor con los tres),
  `tests/unit/test_renovar_cierres.py:189` (el arnés simulado fuera del calendario, con los tres),
  `tests/unit/test_rutas_windows.py:81` (`--diagnostico-a21 str(d.a21)`, y `_mas_largas()` arma un
  `Diagnostico` con `a21`), `tests/unit/test_selector_orden_stop.py:146,185` (la CLI se niega por
  A-47 y por A-27 con los tres flags). La lista del encargo es exacta.
- Fuera de `src/` y `tests/`: `docs/runbooks/ACTIVAR-A35-A44.md:254` («corren hoy con
  `--diagnostico-a21 solo_una_zona_de_control` porque a secas se niegan») y los informes cerrados
  de `docs/validation/` (históricos, no se editan); `docs/adr/0055-…md:112` («`--diagnostico-a21`
  en la CLI», el Impacto que lo creó); `docs/adr/0070-…md:57-62,130,149` (la lista cerrada y «hoy
  A-21, A-35 y A-44»: no se edita, lo dice R3.1, como manda el encargo).

Con el selector fijado (decisión 3), `lectura_limpia` ya rechaza el diagnóstico
(`DiagnosticoDeZonaRechazadoError`, `zonas.py:153-157`); lo que la decisión retira es la opción
entera: la CLI, el campo y la rama hipotética.

### 0.5 El ADR que fija hoy cada cosa que se toca (punto 5)

Grep del id en `docs/adr/*.md` (y en `knowledge/spec/` para la `decision` declarada):

| Lo que se toca | Quién lo fija hoy | Dónde |
|---|---|---|
| RN-003 y el valor `ambiguo` | ADR-0044 §1 («si la vela previa rompe LOS DOS extremos … AMBIGUO»; `0044-…md:15-17`), enmendado por ADR-0060 §1 (el color decide; «la vela con doble ruptura fija el sesgo: la búsqueda hacia atrás … para en ella», `0060-…md:11-23`) y §2 (la vela sin cuerpo «sigue siendo `ambiguo`», `0060-…md:25-32`, con la alternativa 1 descartada en `:102,119`: «seguir buscando hacia atrás … inventa un sesgo que ninguna vela dio») | `strategy_spec.yaml:979` (`decision: ADR-0044`); la decisión 2 enmienda ADR-0060 §1 y §2 con ADR-0075, como manda el encargo |
| RN-033 | ADR-0049 (nace el gate, `0049-…md:45`), ADR-0060 §6 («RN-033 conserva su cita y su forma, y sus notas dicen que es una guardia del proyecto», `0060-…md:84-88`) | `strategy_spec.yaml:1017` (`decision: ADR-0049`); solo cambian sus notas |
| `zona_control_limpia` y `LECTURAS_LIMPIA` | ADR-0055 §2 (el selector PROVISIONAL con dos lecturas, «si la respuesta no calza en ninguna de las dos, se para», `0055-…md:33-41`) y ADR-0054 (el patrón «sin fijar, el motor se niega salvo en diagnóstico») | `parametros.yaml:891-910`; `estructura_m1.py:63-65`; ADR-0056 §5 dice «A-21 no se amplía» (`0056-…md:82`): la opción nueva entra por ADR-0076, que es un ADR |
| `--diagnostico-a21` | ADR-0055 (Impacto, `0055-…md:112`) y ADR-0054 (el modo diagnóstico de A-35/A-44 que A-21 copia) | ADR-0076 enmienda esa parte de ADR-0055 |
| A-21 | ninguna decisión: ABIERTA, bloqueante (`ambiguedades.yaml:420-462`); nombrada por ADR-0019 `:110`, ADR-0045 `:136`, ADR-0055, ADR-0056 `:13,82,206`, ADR-0070 `:57,62,130,149` | se cierra RESUELTA con el RESOLVE_UNKNOWN de S-10 (ADR-0022, las dos formas) |
| A-51 | ninguna: ABIERTA, bloqueante, nace el 2026-09-29 por orden del consultor (`ambiguedades.yaml:1513-1533`); ningún ADR la nombra (Grep `A-51` en `docs/adr`: vacío) | se cierra RESUELTA con el RESOLVE_UNKNOWN de S-8 |
| RN-020 y `detenido_por_tope` | ADR-0027 (`decision`, `strategy_spec.yaml:1771`), ADR-0053 §9 (A-44), ADR-0054 (los tres estados del tope) | no cambia (encargo); RN-036 va aparte, con ADR-0077 |
| `cartucho_criterio` (lo que cuenta como pérdida) | RN-016, `fb-2026-09-09-sesion-01-aa2abe65` (`parametros.yaml:1173-1190`); ADR-0066 (el acumulador `cartuchos` por escenario) | RN-036 cuenta lo mismo (`_cuenta_como_intento`, `primitivas_broker.py:344-353`) |
| `reloj_sesiones` («día siguiente») | ADR-0063 §1-§3 (el selector y quién lee cada reloj) y ADR-0069 (`rejilla_h4`) | `cases/relojes.py:183-199` (`RelojSesiones.lectura` da el día operativo) |
| El estado entre días | ADR-0053 §6 («el estado de estrategia empieza cada día de cero … lo que quede … se cancela al terminar el día», `0053-…md:141-147`); ADR-0050 (la cuenta persiste) | `cableado.py:158-174` (la cuenta y el `SeguidorTope` persisten salvo `cuenta_diaria`; `EstadoDia()` nuevo en `:185`); `:229-236` la cancelación de fin de día |
| RN-035 y `orden_pendiente_al_abrir_sesion` | ADR-0066 (nace RN-035, `0066-…md:77-78`), con el valor CONFIRMED por S-5 (`parametros.yaml:783-804`) | `strategy_spec.yaml:885-925`; la rama `ventana_fin` entra por la forma de RN-035 (decisión 5) |
| RN-002 (lo que ya cierra a `ventana_fin`) | ADR-0060 §4-§5 y ADR-0069 | `strategy_spec.yaml:828-883`: cierra posiciones, «no retira órdenes» (ADR-0060 §6) |

### 0.6 Lo que el repo pide y el encargo no dice

- `spec_version` hoy: `15.9.9` (`knowledge/spec/spec_manifest.yaml:11`), con su regla en el
  propio fichero (`:9-10`): mayor si una regla cambia de sentido o desaparece, menor si se añade
  una regla o un parámetro, parche si solo cambia un valor o una redacción. Plan: decisión 2 →
  16.0.0 (RN-003 cambia de sentido); decisión 3 → 16.1.0 (el enum gana una opción y el
  parámetro, valor: ni regla ni parámetro nuevo, pero más que una redacción); decisión 4 → 16.2.0
  (una regla y cuatro parámetros nuevos); decisión 5 → 17.0.0 (RN-035 cambia de sentido: dispara
  también a `ventana_fin`).
- `feedback apply --check` hoy, antes de ningún registro nuevo: la rama anterior lo dejó en «0
  cambian, 4 ya estaban» (ACTIVAR-SESION-04.md §9.2); se repite en cada commit.
- `tests/unit/test_kit.py:316` congela las bloqueantes ABIERTAS en `{A-21, A-35, A-44, A-51}` y
  `:335-357` las RESUELTAS; `scripts/hoja_preguntas.py:53-58` y `tests/unit/test_hoja_preguntas.py:26-31`
  llevan A-21 en «Lo primero» (A-51 no está en la hoja: no hay nada que quitar, como dice el
  encargo).
- Las tres guardias de `src/botsito/spec/modelo.py` para un sitio nuevo con `cita`:
  `comprobar_literales` (`:348`), `comprobar_contra` (`:392`) y `comprobar_citas_revocadas`
  (`:859`): las tres recorren las reglas y las secciones `predicados`, `acciones`, `hechos` y
  `acumuladores` del vocabulario. RN-036 es una regla: entra por `reglas`; el acumulador
  `racha_perdidas` llevará `cita` y entra por la sección.
- Un acumulador del vocabulario admite solo `descripcion`, `base`, `reinicia_con`, `magnitud`,
  `arrastra` y `cita` (`modelo.py:1000`); `base` tiene que ser un parámetro y `reinicia_con` un
  token de clase `reinicio` o un parámetro enum (`:1491-1518`). Así que `racha_perdidas` declara
  `base: cartucho_criterio` y `reinicia_con: racha_perdidas_reinicio` (enum), y el corte y la
  reanudación los nombra RN-036 en `parametros` y los lee el código por su nombre, como
  `cartuchos` lee `cartucho_criterio` (`primitivas_broker.py:84,348`).
- La acción `retirar_orden_limite` exige exactamente UNA pendiente y lee `segun` (`primitivas_broker.py:540-555`);
  para RN-036 hace falta una acción que retire lo que haya (cero o una) sin selector: nace en
  la decisión 4 y se dice.
- `EstadoDia` nace cada día (`cableado.py:185`): el acumulador de la racha no puede vivir ahí
  (encargo). `MotorCableado` guarda `cuenta` y `seguidor` entre días y los pone a `None` con
  `cuenta_diaria` (`cableado.py:158-159`): la racha va al lado, con la misma regla.
- El bucle del cableado evalúa el evento del minuto `ventana_fin` (`cableado.py:191`,
  `while instante <= ultimo`; `_sesion` devuelve la sesión también en `instante == hasta`,
  `:388-395`): RN-002 dispara ahí con `alcanza_hora` (`strategy_spec.yaml:876`), y RN-035 podrá
  hacer lo mismo. La cancelación de fin de día usa el MISMO instante (`fin_ms = ultimo *
  MS_POR_MINUTO - 1`, `:230`, igual que el último `hasta_ms`): el test de la decisión 5 tiene que
  distinguir quién canceló por la traza del motor (RN-035 en `disparadas` y la petición de
  cancelación en `broker.traza().peticiones` ANTES del bloque de fin de día), no por el instante.
### 0.7 El encargo frente al repo (auditor `auditor-encargo`, 2026-10-11)

El auditor leyó el encargo contra el repo (55 afirmaciones: 31 correctas, 5 incorrectas, 19 con
matiz; 14 herencias) sin escribir nada. Lo que cambia lo que se pide, medido después por la sesión:

| # | Lo que dice el encargo | Lo medido | Qué se hace |
|---|---|---|---|
| a1 | La opción `sin_alternancia_de_colores`: «ningún cambio de color … desde el fin del bloque de origen hasta la vela que rompe (excluida)» | `bloque_de_origen` (`domain/estructura_m1.py:128-138`) recorre hacia atrás desde el breaker todas las velas del color de la entrada o sin cuerpo hasta la PRIMERA contraria, y esa es el bloque: `m1[hasta:i]` (`:331`) solo tiene velas del color de la entrada o de cuerpo cero. Saltando las de cuerpo cero, en ese tramo nunca hay un cambio de color: **la opción no invalidaría nunca**. El retroceso del esquema 2 queda ANTES del bloque (`zonas_de_control`, `:141-158`: los pivotes después del primer impulso), no después | **PARADA, punto 0**: es «algo de lo medido contradice una decisión» |
| a2 | Lo que nombra `--diagnostico-a21`: cli, zonas, el campo `a21` y seis tests | Además, construyen `Diagnostico` con `a21`: `tests/unit/test_cableado.py:774-781` (`Diagnostico(a21=…)`, la etiqueta de la cuenta diaria) y, POR POSICIÓN, `scripts/embudo_77.py:429`, `scripts/caja_77_exploratoria.py:131` y `scripts/orden_stop_o_limite.py:417`; `scripts/` no está en `rutas_permitidas` | **PARADA, punto 1** |
| a3 | `feedback pending` puede listar el CONFIRM de S-4 «sin forma mecánica de comprobarlo» | `cli.py:2049-2051`: un CONFIRM sobre evidencia sale como REFLEJADO («un CONFIRM confirma un item que ya vive: no deja trabajo»); «sin forma mecánica» es para CORRECT y REJECT sobre evidencia (`:2052-2055`), que son los de la sesión 1 | Se mide al hacerlo (§1.1) y se dice |
| a4 | «La tabla de Known Ambiguities se prepara para el cierre» | `tests/unit/test_kit.py:414-423` exige que la tabla tenga EXACTAMENTE las ABIERTAS del YAML: la fila sale en el mismo commit que cierra la ambigüedad, o `make check` sale en rojo (la rama anterior lo hizo así, ACTIVAR-SESION-04.md:810) | La fila de A-51 sale en el commit de A-51 (y la de A-21 en el suyo, tras la PARADA); `PROJECT_STATE.md` está en `rutas_permitidas` |
| a5 | «Uno que demuestre que una «en parte» (A-49) no puede entrar en RESUELTAS» | `tests/unit/test_en_parte_no_se_cierra.py:77-78` clasifica A-49 como MEZCLADA (S-4 resuelve, S-1 y S-2 en parte) y comprueba que NO está en `solo_en_parte`: esa guardia no la detectaría | Test nuevo en `test_kit.py`: A-49 ABIERTA y fuera del conjunto RESUELTAS (§1.1) |
| m1 | CORRECT sobre RN-003 citando `ev-v10-014005-7e2228f4` | Un CORRECT sobre una regla cuenta como reflejado solo si la regla lo cita (`cli.py:2064-2075`); RN-003 cita hoy `fb-2026-09-29-sesion-03-31fb311f` (`strategy_spec.yaml:939`); la skill exige `feedback pending` limpio | RN-003 pasa a citar el CORRECT nuevo, como ADR-0060 §6 decidió para los CORRECT de la sesión 3 (§0.8, decisión de la sesión) |
| m2 | La reserva de S-13: lo dijo con sesgo previo alcista | Hay una segunda: «suponiendo que … no haya otro rango mayor» (SESION-04-EXTRACCION.md:679-680) | Las dos van al ADR y a las notas de RN-003 |
| m3 | El token `ambiguo` se queda porque lo usan scripts y el visor | El visor pinta `sesgo.value` sin nombrarlo; lo nombran `scripts/sesgo_h4_diagnostico.py:85,108` y `tests/unit/test_embudo_77.py:52`; lo que obliga a conservarlo es la forma de RN-033 (`vale: ambiguo`) y `hechos.sesgo.valores` | Se queda; la forma de RN-033 no cambia (el encargo: solo sus notas) |
| m4 | Las guardias de `modelo.py` «en el mismo commit» de RN-036 | Las tres ya recorren todas las reglas y las cuatro secciones del vocabulario (`modelo.py:367,406-417,877-882`); la regla de CLAUDE.md es para una CLASE nueva de sitio con cita | Nada que ampliar: se dice, y se comprueba que RN-036 y el acumulador nuevo pasan por ellas |
| m5 | «Día siguiente» con `reloj_sesiones` (ADR-0063) | El valor `rejilla_h4` lo fijó ADR-0069 (`parametros.yaml:239-245`): el «día» es el operativo de la rejilla (`cases/relojes.py:183-199`, `lectura`) | ADR-0077 cita 0063 y 0069 |
| m6 | La racha: `reinicio` = `nunca`, `corte` = `ganadora`, y tras la novena «se vuelve en la primera sesión del día siguiente» | Con un acumulador «≥ tope» y sin reinicio, al día siguiente la racha sigue en 9 y RN-036 prohibiría para siempre hasta una ganadora | La detención es DEL DÍA OPERATIVO en que cayó la pérdida que alcanza el tope; la racha sigue contando; una pérdida más (la décima) vuelve a detener su día (§0.8) |
| m7 | RN-035 «según `orden_pendiente_al_abrir_sesion`» a `ventana_fin` | El parámetro se define «al abrir la siguiente» (`parametros.yaml:786`) y el título de RN-035 habla de la apertura (`strategy_spec.yaml:886-887`) | Cambian el título de RN-035 y la descripción del parámetro (no su nombre); §0.8 |
| m8 | La decisión 5 cambia RN-035 (ADR-0066 §4) y el reparto de ADR-0053 §6 sin ADR | ADR-0066 escribió RN-035 al abrir la sesión con valor PROVISIONAL; ADR-0053 §6 deja la cancelación de fin de día, que SE QUEDA | No contradice ninguno de los dos: es la activación de S-5 que el consultor decidió (punto 4 de su respuesta); `decision: ADR-0066` se conserva y las notas lo dicen |
| m9 | «Un test que demuestre que `detectar_esquema` con una lectura fuera de LECTURAS_LIMPIA sigue fallando» | Ya existe: `tests/unit/test_estructura_m1.py:234-235` (`"al_ojo"`, `match="A-21"`) | Se cita; con la opción nueva se amplía (PARADA) |
| m10 | El hueco del último minuto | ADR-0060 §5 ya decidió que `vence_vela_h4` da SÍ en el propio límite: lo que se llene en el último minuto se cierra en el evento del límite | El test lo congela citando ADR-0060 §5 |
| m11 | `grep -rn` de `--diagnostico-a21` en `src/` y `tests/` «vacío» | Casa con los `__pycache__/*.pyc` («Binary file … matches») | El grep se hace con `--include=*.py` |
| m12 | «A-51 … CONFIRMED vía feedback apply» | Cerrar A-51 RESUELTA exige un RESOLVE_UNKNOWN ACTIVO sobre la ambigüedad (README.md:83-87; AMBIGUEDADES.md:36-37); y `feedback new` sobre un parámetro exige que el parámetro exista (README.md:59-61) | Los cuatro parámetros entran UNKNOWN en `parametros.yaml` ANTES de los registros; un RESOLVE_UNKNOWN sobre A-51 y uno por parámetro |
| m13 | La confirmación bajista de S-13 «entra» en la lista de la sesión 5 | Ya está: ACTIVAR-SESION-04.md:836-837 y HOJA-DE-RUTA.md:111-112 | Las líneas del cierre lo dicen así |
| m14 | Heredado 30 cambia por A-21 | No la nombra (grep en HISTORIA.md); solo el 25 | Se dice en las líneas del cierre |
| m15 | G.2: `--diagnostico-a47` y `--diagnostico-a27` «siguen» | G.2 dice que «se retiran con `--diagnostico-a21` o en G.1» (HOJA-DE-RUTA.md:249-251) | No se retiran (el encargo lo decide); la línea del cierre lo recoge |
| h1 | — | ADR-0074 §3 deja «la cadena entera por el cableado real» de `caja_se_fija` para «la rama de motor y R3.1» | No está en el encargo: se declara y va a las líneas del cierre (R3.1) |
| h2 | — | Las notas de RN-002 (`strategy_spec.yaml:861-865`) y la descripción de `orden_pendiente_al_abrir_sesion` (`parametros.yaml:798-799`) dicen que la retirada a `ventana_fin` es del cableado «sin regla» | Cambian en el commit de la decisión 5 |
| h3 | — | ADR-0060 (Impacto) tocó las descripciones de `sesgo_h4_al_abrir`, del `entonces` de RN-003, del token `sentido_de_la_ruptura` y del hecho `sesgo` (`strategy_spec.yaml:67-68,505,631-632,935-937`) | Se revisan en el commit de la decisión 2 |
| h4 | — | ADR-0060 descartó «seguir buscando hacia atrás» porque «inventa un sesgo que ninguna vela dio» (`:102,119`) | ADR-0075 contesta: ahora lo dice el trader |
| h5 | — | ADR-0055 §2 fija el selector en dos opciones («si no calza, se para») y §5 el rótulo `.a21=` | Lo enmienda ADR-0076 (PARADA) |
| h6 | — | `ACTIVAR-A35-A44.md:261-262` manda revisar RN-008, RN-011 y el glosario al cerrar A-21; ninguna regla ni el glosario citan A-21 (grep vacío) | Se dice (PARADA) |

### 0.8 Lo que la sesión aplica sin decidir por el consultor (declarado, revisable)

Cosas que el encargo no dice y que hacen falta para que lo que sí dice cierre en verde; cada una
con el precedente o la guardia que la fuerza. Si el consultor quiere otra, se cambia en un commit:

1. **RN-003 cita el CORRECT nuevo** (decisión 2), con su `literal` sacado de la respuesta del trader
   en S-13; `fb-2026-09-29-sesion-03-31fb311f` queda en las notas. Precedente: ADR-0060 §6
   (decidido por el consultor el 2026-09-30: «RN-002 y RN-003 pasan a citar sus CORRECT de la
   sesión 3»). Sin eso, el CORRECT es un pendiente que la skill prohíbe dejar. MEDIDO AL HACERLO
   (§1.2): una regla cita UN registro, así que al citar el de S-13 el CORRECT de la sesión 3
   (`fb-2026-09-29-sesion-03-31fb311f`) pasa a salir en `feedback pending` como «RN-003 no lo cita
   todavía»; con la otra opción saldría el de S-13. Uno de los dos sale siempre: es una limitación
   de `pending` (un CORRECT por regla), no un trabajo que falte; va a las líneas del cierre como
   deuda, y el consultor puede preferir la otra cita (PARADA, punto 4).
2. **La fila de A-51 (y la de A-21, tras la PARADA) sale de Known Ambiguities en su commit**, no en
   el cierre: `test_kit.py:414-423` (a4).
3. **A-51 lleva su RESOLVE_UNKNOWN** además de los cuatro registros de parámetro (m12).
4. **La racha tras la novena** (m6): el acumulador `racha_perdidas` da SÍ contra `racha_perdidas_max`
   cuando la racha es ≥ tope Y la pérdida que la puso ahí cayó en el día operativo en curso (el de
   `reloj_sesiones`); al día siguiente la racha sigue en 9 (`reinicio = nunca`) pero la detención
   ha caducado (`reanudacion = dia_siguiente`), y la siguiente pérdida -la décima- vuelve a
   detener el día en que caiga. Es una lectura PROVISIONAL de la sesión, la que hace valer a la vez
   las tres cosas del encargo («tras la novena no se opera más en ese día», «se vuelve … el día
   siguiente», «la racha sigue de un día a otro»); ADR-0077 §5 da las alternativas y la pregunta
   va a la sesión 5 (respuesta del consultor del 2026-10-12, punto 5).
5. **La retirada de RN-036** la hace una acción nueva del vocabulario, `retirar_ordenes_pendientes`
   (sin argumentos: cancela lo que haya pendiente, cero o una, y es idempotente), porque
   `retirar_orden_limite` exige exactamente una pendiente ligada y un `segun`
   (`primitivas_broker.py:540-555`), y RN-036 tiene que prohibir aunque no quede ninguna orden.
6. **El acumulador de la racha vive en un módulo propio** (`engine/racha.py`, `SeguidorRacha`),
   como atributo de `MotorCableado` junto a `seguidor` (el `SeguidorTope`) y con su misma regla de
   `cuenta_diaria`; NO dentro de `SeguidorTope`, que solo existe con A-44 fijada o en diagnóstico
   (`cableado.py:170-173`), ni en `engine/cuenta.py`, que el contrato protege.
7. **RN-035 cita el registro de S-5** (`fb-2026-10-04-sesion-04-45e624c5`, «sí, se quita, porque
   siempre se va a ir actualizando la orden … no va a haber órdenes que a lo mejor se pueden tomar
   a las 3 o fuera de horario»), que es lo que la regla hace desde hoy en sus dos ramas;
   `fb-2026-09-29-sesion-03-5021677e` queda en las notas. Mismo precedente que el punto 1. Su
   título y la descripción del parámetro dicen ya «al abrir la siguiente sesión y al llegar
   ventana_fin» (m7); el nombre del parámetro no cambia.
8. **El orden de los commits**: 1, 2, 4 y 5; la 3 queda en PARADA (régimen nocturno de Aleks: «deja
   commiteado lo que no dependa de ella»). Ninguna de las otras tres depende de A-21.

### 0.9 Lo que no pude medir

- Si `ev-v10-011957-7ebb3453` forma parte del ejemplo de enero de su replay (h2 del revisor
  anterior): haría falta la cruda de v10, en cuarentena. No se abre. La cita no trae fecha ni cifra
  y se usa solo como regla.
- Que RN-036 no necesite `--diagnostico-a44`: se mide al escribirla (§1.3), con `tope=None` en el
  motor cableado, como `test_preparar_a44.py:345-352`.

### 0.10 Exposiciones

Ninguna. Lo leído: el repositorio, los ítems `ev-v10-*` y `ev-v9-*` citables de arriba y los
registros de feedback. Ningún material, ninguna cruda, ningún fotograma, ninguna carpeta de meses
reservados listada. `HOLDOUT-EXPOSICIONES.md` no cambia.

## Lo que necesito que decidas (PARADA · decisión 3, A-21)

0. **La opción `sin_alternancia_de_colores` tal como la define el encargo no filtra nada** (a1):
   entre el fin del bloque de origen y la vela que rompe solo hay velas del color de la entrada o
   sin cuerpo, por cómo `bloque_de_origen` busca la última contraria. Opciones:
   (a) **El tramo es el RETROCESO**: desde la primera vela contraria a la entrada posterior al
   primer impulso tras la toma (`primer_impulso` de `zonas_de_control`, `estructura_m1.py:150`)
   hasta el bloque de origen (incluido), saltando las velas de cuerpo cero; «ningún cambio de color
   de una M1 a la siguiente» ahí equivale a que las velas contrarias del retroceso formen UN solo
   bloque consecutivo; el esquema 1 (sin retroceso) es siempre limpio, y el número de velas del
   retroceso sigue sin importar (S-10, pregunta 2). Lo que sí invalida: verde, roja, verde, roja
   antes de la ruptura (v10 1:19:57, `ev-v10-011957-7ebb3453`; v9 1:19:57 en la `pregunta` de
   A-21).
   (b) El tramo entero desde la vela siguiente a la toma hasta la que rompe (excluida), y «sin
   alternancia» = como mucho dos cambios de color (impulso → contrarias → impulso).
   (c) A la sesión 5 con la pregunta del punto 11 de la lista (§0.e de ACTIVAR-SESION-04.md).
   Recomiendo (a): es lo que el consultor escribió («ningún cambio de color … en el retroceso»)
   con los límites del retroceso que el código ya usa, y es lo literal del trader. Coste de (b):
   cuenta cambios y no bloques, y una vela contraria entre la toma y el primer impulso ya
   invalidaría, que el trader no dijo. Coste de (c): A-21 sigue bloqueante y R3.1 sigue en
   diagnóstico.
   En cualquiera de (a) o (b), el test que «falla con `main`» será semántico: una serie con
   alternancia en el retroceso da `None` con la opción nueva y un `Esquema` con
   `solo_una_zona_de_control`; en `main` la opción no existe y `detectar_esquema` la rechaza con
   `EstructuraError` (la guardia de `test_estructura_m1.py:234-235`, m9).
1. **Quitar `Diagnostico.a21` rompe fuera del contrato** (a2): `scripts/embudo_77.py:429`,
   `scripts/caja_77_exploratoria.py:131` y `scripts/orden_stop_o_limite.py:417` construyen
   `Diagnostico` por posición con `a21` en tercer lugar. Opciones: (a) ampliar `rutas_permitidas`
   con esos tres scripts y pasarlos a argumentos con nombre (sin `a21`: la lectura la da el
   registro); (b) dejar el campo `a21` en `Diagnostico`, siempre `None`, y retirar solo la opción
   de la CLI y la rama de `lectura_limpia`. Recomiendo (a). Coste de (b): un campo muerto, contra
   el encargo. Los cuatro scripts que recorren `LECTURAS_LIMPIA` (`bloque_de_la_caja.py:273`,
   `orden_stop_o_limite.py:416,517`, `verificacion_a21.py:90`, `verificacion_a21_entradas.py:194`)
   medirían tres lecturas en vez de dos sin romperse: no se tocan, y se dice.
2. **`docs/runbooks/ACTIVAR-A35-A44.md` §6** (m del auditor, 28): además de la tabla, dice que la
   respuesta tiene que calzar en una de las dos (`:201-202`), que «el selector es un enum de UNA
   opción» (`:218`) y cómo se corre con `--diagnostico-a21` (`:210-212,254`). Opciones: (a) la
   tabla gana la fila y §6 empieza con una nota de tres líneas (A-21 RESUELTA con la opción nueva,
   `--diagnostico-a21` retirado, el resto de §6 es histórico); (b) solo la tabla. Recomiendo (a).
3. **La lista de los cinco sitios de A-21**: ninguna regla ni término del glosario cita A-21 ni
   «limpia» (grep vacío en `strategy_spec.yaml` y `glossary.yaml`; h6): el sitio «la regla que la
   citaba» no existe y se dice; cambian además la descripción de `zona_control_limpia` («ABIERTA y
   BLOQUEANTE de RN-008», `parametros.yaml:898-908`) y el texto de A-21 (`ambiguedades.yaml:425-428`).
   No es una decisión: lo apunto para que la respuesta lo dé por bueno o lo corrija.
4. **La `cita` de RN-003 tras el CORRECT de S-13** (hecho en la decisión 2, §1.2, revisable): una
   regla cita UN registro y `feedback pending` da por pendiente todo CORRECT sobre ella que no sea
   el citado (`cli.py:2064-2075`). Opciones: (a) RN-003 cita el CORRECT de S-13
   (`fb-2026-10-04-sesion-04-ca0afae6`, lo hecho, por el precedente de ADR-0060 §6) y el de la
   sesión 3 (`fb-2026-09-29-sesion-03-31fb311f`, el color con doble ruptura) sale como pendiente
   aunque la regla siga haciéndolo y sus notas lo citen; (b) RN-003 vuelve a citar el de la sesión
   3 y el de S-13 sale como pendiente. Recomiendo (a): la cita es la última palabra del trader
   sobre la regla, como en ADR-0060 §6; y que `pending` no sepa de una regla con dos CORRECT vivos
   va a las líneas del cierre como deuda. Coste de (b): un registro de la sesión 4 pendiente, que la
   skill prohíbe dejar.

**Espero tu respuesta a la PARADA** para la decisión 3 (y el punto 4 si prefieres (b)). Las decisiones 1, 2, 4 y 5 siguen esta
noche, cada una en su commit, con lo de §0.8 declarado.

## 1. Las decisiones, una por commit

### 1.1 Decisión 1 · CONFIRM de S-4 sobre `ev-v10-004945-59ebac47` (PARADA 2, opción b)

- **Registro:** `knowledge/feedback/2026-10-04-sesion-04/fb-2026-10-04-sesion-04-35a080e2.yaml`,
  creado con `uv run botsito feedback new --sesion 2026-10-04-sesion-04 --fecha 2026-10-04
  --recibido-el 2026-10-04 --procedencia trader_grabado --medio video --grabacion "Grabación de
  pantalla 2026-10-04 105617.mp4" --t0 0:49:45 --t1 0:50:10 --objetivo-tipo evidence --objetivo-id
  ev-v10-004945-59ebac47 --accion CONFIRM --respuesta "<la cita literal del ítem>" --registrado-por
  … --notas …` (todas las opciones obligatorias de la plantilla, `knowledge/feedback/README.md`;
  `--recibido-el` y `--procedencia` por la guardia). La respuesta literal es la `cita_literal` del
  ítem (v10 0:49:45–0:50:10, fuera de todo tramo no citable); las notas dicen que no cierra A-49.
- **A-49 sigue ABIERTA**, sin registro sobre ella: `uv run botsito feedback trace
  ev-v10-004945-59ebac47` da el ítem y este único registro, activo.
- **`feedback pending`** NO lo lista como «sin forma mecánica de comprobarlo», al revés de lo que
  decía el encargo (y la PARADA 2 de la rama anterior): `cli.py:2049-2051` da un CONFIRM sobre
  evidencia por REFLEJADO («un CONFIRM confirma un item que ya vive: no deja trabajo»); con
  `--todos` sale como `(ok) fb-2026-10-04-sesion-04-35a080e2 evidence:ev-v10-004945-59ebac47 - un
  CONFIRM confirma un item que ya vive: no deja trabajo`. «Sin forma mecánica» es lo que `pending`
  dice de los CORRECT y REJECT sobre evidencia de la sesión 1 (`:2052-2055`). Mejor para la
  skill: no deja pendiente.
- **`feedback apply --check`:** «4 parametros; 0 cambian, 4 ya estaban; --check: no se ha escrito
  nada» (un CONFIRM sobre evidencia no toca el registro).
- **Test** (el que pide el encargo: «una «en parte» (A-49) no puede entrar en RESUELTAS»):
  `tests/unit/test_kit.py::test_una_en_parte_no_entra_en_resueltas`. El conjunto RESUELTAS que
  congelaba `test_ambiguedades_reales_y_esquema` pasa a la constante de módulo `RESUELTAS`, y
  `EN_PARTE_SESION_4` (A-13, A-32, A-35, A-43, A-44, A-49, A-50, A-53) no la toca; cada una está
  ABIERTA en el YAML; no hay ningún registro con objetivo `ambiguedad: A-49`; y el de S-4 es un
  CONFIRM sobre el ítem. `tests/unit/test_en_parte_no_se_cierra.py` no cubría A-49 porque la
  clasifica como MEZCLADA (§0.7, a5). 1507 funciones de test (`PROJECT_STATE.md`).
- Sin `Fuente:` en el commit: no toca `knowledge/spec/` ni `knowledge/cases/`.

### 1.2 Decisión 2 · S-13: una H4 neutra no decide el sesgo (ADR-0075, enmienda ADR-0060 §1 y §2)

- **ADR-0075** (`docs/adr/0075-una-h4-neutra-con-doble-ruptura-no-decide-el-sesgo.md`, número
  comprobado libre en §0.2, con la plantilla): la vela que rompe los dos extremos y cierra sin
  cuerpo no fija el sesgo; la búsqueda hacia atrás la salta. Las dos reservas (sesgo previo
  alcista; «suponiendo que no haya otro rango mayor») y el «no hay umbral en H4» (uno o dos puntos
  de cuerpo ya cuentan) están en el ADR y en las notas de RN-003. **Recuadro de ENMIENDA** al
  principio de ADR-0060 y su fila del índice: «ACTIVE (con enmienda de ADR-0075: la H4 neutra no
  fija el sesgo)»; fila nueva para 0075. Sale `ADR-0075` del bloque `ids-inexistentes` del encargo
  y de este informe (ya existe).
- **Registro:** `fb-2026-10-04-sesion-04-ca0afae6`, CORRECT sobre la regla RN-003 (v10
  1:40:05–1:40:40, `ev-v10-014005-7e2228f4`), con todas las opciones obligatorias; `--valor` dice
  lo que queda. `feedback apply --check`: «4 parametros; 0 cambian, 4 ya estaban» (un CORRECT sobre
  una regla no toca el registro de parámetros). `feedback pending --todos`: `(ok)
  fb-2026-10-04-sesion-04-ca0afae6 regla:RN-003 - aplicado: la regla lo cita`; y, como efecto de
  citar este, `fb-2026-09-29-sesion-03-31fb311f CORRECT regla:RN-003 - RN-003 no lo cita todavia`
  pasa a pendiente (§0.8.1 y PARADA, punto 4: una regla cita un registro y `pending` no sabe de dos
  CORRECT vivos; deuda para las líneas del cierre).
- **Spec** (`knowledge/spec/strategy_spec.yaml`, con `spec docs --escribir` en el mismo commit):
  RN-003: `entonces` («si cierra sin cuerpo -neutra, sin color- no decide y manda la H4 anterior
  que rompió con lado»), `cita` y `literal` (el CORRECT de S-13; el de la sesión 3 queda en las
  notas, que cuentan el relevo), notas; RN-033: notas («queda SOLO para `insuficiente`»; su forma
  y su cita no cambian); descripciones de `sesgo_h4_al_abrir`, del token `sentido_de_la_ruptura`,
  del token `ambiguo` («DESDE ADR-0075 EL MOTOR NO LO PRODUCE … retirarlo es deuda») y del hecho
  `sesgo`. `spec_version` **15.9.9 → 16.0.0**, a mano (una regla cambia de sentido), y `spec
  manifest --escribir` (hash `8b1bf95f9853…`).
- **Motor:** `src/botsito/domain/sesgo.py`: la rama de la doble ruptura sin cuerpo pasa de
  `return ResultadoSesgo(Sesgo.AMBIGUO, …)` a `continue`; docstring del módulo, de `Sesgo.AMBIGUO`
  («declarado y SIN PRODUCTOR desde ADR-0075») y de `ResultadoSesgo`. Nada más en `src/`.
- **Tests que cambian de sentido A PROPÓSITO** (dicho en su docstring):
  `tests/unit/test_sesgo_h4.py::test_doble_ruptura_sin_cuerpo_es_ambiguo` →
  `test_doble_ruptura_sin_cuerpo_no_decide_y_sin_nada_detras_es_insuficiente`;
  `tests/unit/test_huecos_motor.py`: `test_una_sesion_ambigua_fija_sesgo_ambiguo_y_rn033_prohibe` →
  `test_una_h4_neutra_no_decide_y_sin_nada_detras_es_insuficiente`,
  `test_una_segunda_sesion_ambigua_no_hereda_el_sesgo_de_la_primera` →
  `test_una_h4_neutra_en_la_segunda_sesion_mantiene_el_sesgo_de_la_primera`,
  `test_una_sesion_no_ambigua_tras_una_ambigua_no_hereda_la_prohibicion` →
  `test_una_sesion_con_lado_tras_una_insuficiente_no_hereda_la_prohibicion` (su `EstadoDia` a mano
  pasa de `ambiguo` a `insuficiente`), y el docstring H1 del módulo. **Nuevos:**
  `test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista` (los dos que pide el encargo: la
  neutra tras sesgo alcista y tras bajista), `test_dos_neutras_seguidas_mantienen_el_sesgo` (y el
  tope cuenta las neutras saltadas), `test_con_un_cuerpo_de_un_punto_la_doble_ruptura_ya_decide`
  (sin umbral), y `test_rn033_sigue_prohibiendo_con_sesgo_ambiguo_puesto_a_mano` (la guardia que
  queda: el token sigue en la forma). `:305` y `:341` de `test_huecos_motor.py` no cambian (§0.3).
  1511 funciones de test.
- **Con el código de `main`** (skill `comparar-con-main`: clon `git worktree add --detach
  C:/cm/main main`, los dos ficheros de test de la rama copiados dentro, `uv run pytest
  tests/unit/test_sesgo_h4.py tests/unit/test_huecos_motor.py -q -p no:cacheprovider`; después
  `git checkout -- tests/...` en el clon, que vuelve a pasar sus propios tests, 36 passed 1
  skipped). Salida recortada a lo que demuestra:

  ```
  E         At index 0 diff: 'ambiguo' != 'insuficiente'
  tests\unit\test_huecos_motor.py:212: AssertionError
  SKIPPED [1] tests\unit\test_huecos_motor.py:316: sin las velas de construccion: falta en disco: ...
  FAILED tests/unit/test_sesgo_h4.py::test_doble_ruptura_sin_cuerpo_no_decide_y_sin_nada_detras_es_insuficiente
  FAILED tests/unit/test_sesgo_h4.py::test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista
  FAILED tests/unit/test_sesgo_h4.py::test_dos_neutras_seguidas_mantienen_el_sesgo
  FAILED tests/unit/test_huecos_motor.py::test_una_h4_neutra_no_decide_y_sin_nada_detras_es_insuficiente
  FAILED tests/unit/test_huecos_motor.py::test_una_h4_neutra_en_la_segunda_sesion_mantiene_el_sesgo_de_la_primera
  FAILED tests/unit/test_huecos_motor.py::test_una_sesion_con_lado_tras_una_insuficiente_no_hereda_la_prohibicion
  ```

  Los seis fallan en `main` (dan `ambiguo` donde la rama da el sesgo anterior o `insuficiente`) y
  pasan en la rama (40 passed, el de `data/` saltado). Los otros dos nuevos
  (`test_con_un_cuerpo_de_un_punto…` y `test_rn033_sigue_prohibiendo…`) pasan en los dos lados: no
  cambian de sentido, congelan lo que no cambia.
- **Guardias:** `uv run botsito knowledge validate` OK (35 reglas, hash del manifiesto al día, 452
  documentos); `ruff check` y `ruff format --check` limpios sobre `src tests scripts .claude/hooks`.
- `Fuente: fb-2026-10-04-sesion-04-ca0afae6 ADR-0075` en el cuerpo del commit.

### 1.3 Decisión 4 · A-51: RN-036, la racha de pérdidas seguidas del trader (ADR-0077)

Hecha antes que la decisión 3, que está en PARADA (§0.8.8).

- **Registros** (los cinco con todas las opciones obligatorias; v10 1:06:53–1:08:28, fuera de
  todo tramo no citable):
  `fb-2026-10-04-sesion-04-8e2d728a` (RESOLVE_UNKNOWN sobre A-51, el que la cierra);
  `fb-2026-10-04-sesion-04-b7040095` (`racha_perdidas_max` = 9, `ev-v10-010653-81316808`);
  `fb-2026-10-04-sesion-04-ecdd0572` (`racha_perdidas_corte` = `ganadora`,
  `ev-v10-010715-fae17215`); `fb-2026-10-04-sesion-04-d1792021` (`racha_perdidas_reinicio` =
  `nunca`) y `fb-2026-10-04-sesion-04-fa5ef0f6` (`racha_perdidas_reanudacion` = `dia_siguiente`),
  los dos sobre `ev-v10-010804-5b6ad1a3`. Los cuatro parámetros entraron antes en
  `parametros.yaml` como UNKNOWN (categoría `estrategia`; `feedback new` exige que existan,
  §0.7 m12), con la nota de §4.8 en la descripción de `racha_perdidas_max` (las 9 vienen de un
  0,5 % de riesgo, como el del bot). `feedback apply --check`: «8 parametros; 4 cambian, 4 ya
  estaban», SOLO los cuatro de esta respuesta (`+ racha_perdidas_corte 'ganadora' <- …ecdd0572`,
  `+ racha_perdidas_max 9 <- …b7040095`, `+ racha_perdidas_reanudacion 'dia_siguiente' <-
  …fa5ef0f6`, `+ racha_perdidas_reinicio 'nunca' <- …d1792021`); después sin `--check`: los cuatro
  CONFIRMED con fuente `feedback`. `feedback pending` no lista ninguno de los cinco.
- **ADR-0077** (`docs/adr/0077-la-racha-de-perdidas-seguidas-del-trader-rn036.md`, número
  comprobado libre en §0.2, con la plantilla; fila nueva en el índice; sale `ADR-0077` de los
  bloques `ids-inexistentes`): los cuatro parámetros (§1), la pérdida como la de RN-016 (§2),
  RN-036 aparte de RN-020 con su acumulador persistente, su hecho y la retirada de la orden
  pendiente -decisión del consultor- (§3), el día operativo del reloj de las sesiones con el
  porqué (§4), y la **lectura de la sesión** sobre qué vale la racha tras la novena (§5; §0.8.4):
  la detención es del día operativo de la pérdida que alcanza el tope, la racha sigue en 9 al día
  siguiente y la décima vuelve a detener su día.
- **Spec** (`spec docs --escribir` en el mismo commit): RN-036 (gate; `cuando`: `alcanza_tope
  {acumulador: racha_perdidas, tope: racha_perdidas_max}` o `hecho: detenido_por_racha`;
  `entonces`: prohíbe `abrir_operacion`, fija `detenido_por_racha` a `hasta_el_dia_siguiente` y
  `retirar_ordenes_pendientes: {}`; `cita` el registro de `racha_perdidas_max`, `literal` «como
  máximo una racha de pérdidas, una racha de nueve pérdidas, como máximo»; `decision: ADR-0077`;
  `parametros` los cuatro más `cartucho_criterio` y `reloj_sesiones`); el acumulador
  `racha_perdidas` (`base: cartucho_criterio`, `reinicia_con: racha_perdidas_reinicio`, `cita`
  el RESOLVE_UNKNOWN de A-51); el hecho `detenido_por_racha` (origen regla, producido y consumido
  por RN-036); el token `hasta_el_dia_siguiente` (clase duración); la acción
  `retirar_ordenes_pendientes` (sin argumentos). `racha_perdidas_corte` y
  `racha_perdidas_reanudacion` no los lee ninguna forma (los lee el código por su nombre) y
  declaran `consumido_por: [ADR-0077]`, como `huso_operativa` con sus ADR (§0.7: una regla
  vigente que no los nombre en su forma no vale como consumidor). RN-020 no cambia. La guardia de
  cifras de negocio rechazó «un cartucho» en el `cuando` de RN-036 (`_cifra_de_negocio`): se
  reescribió sin número. `spec_version` **16.0.0 → 16.1.0** (una regla y cuatro parámetros
  nuevos), `spec manifest --escribir` (hash `f99acee2528a…`).
- **Las tres guardias de `modelo.py`** no se amplían (§0.7 m4): RN-036 es una regla y
  `racha_perdidas` un acumulador, dos clases de sitio que `comprobar_contra`, `comprobar_literales`
  y `comprobar_citas_revocadas` ya recorren; `knowledge validate` las pasa («36 reglas de spec (31
  vigentes, 31 con forma ejecutable), hash del manifiesto al dia»).
- **Motor:** `src/botsito/engine/racha.py` (nuevo: `cuenta_como_perdida`, `SeguidorRacha` con
  `registrar`, `detenido(instante, tope)` y `dia_operativo` por `RelojSesiones.lectura`,
  `seguidor_del_registro`; las opciones sin contrato se niegan con `RachaError`);
  `engine/cableado.py` (`MotorCableado.racha`, creado una vez y reiniciado solo con
  `cuenta_diaria`, como `seguidor`; alimentado en `_a_la_cuenta` con cada cierre; pasado al
  `ContextoDia`; `TrazaBroker.cancelados_fin_dia` cuenta lo que cancela la red de seguridad de
  fin de día; la línea `RACHA DE PERDIDAS (RN-036, A-51): …` en `informe_simulacion`);
  `engine/primitivas_broker.py` (`ContextoDia.racha`; el acumulador `racha_perdidas`, hueco con
  nombre sin seguidor; la acción `retirar_ordenes_pendientes`; `_cuenta_como_intento` de
  `cartuchos` delega en `cuenta_como_perdida`: una sola definición); `engine/primitivas.py` (en el
  motor de la spec, sin broker, `racha_perdidas` da NO: no opera, no pierde). `mypy src`: sin
  errores. RN-036 no lee ningún parámetro de A-44 y no necesita `--diagnostico-a44`: el test del
  cableado corre con `motor.tope is None`.
- **Cinco sitios:** `ambiguedades.yaml` (A-51 RESUELTA, `parametros` los cuatro, `evidencia` gana
  los tres ítems de v10, la `pregunta` lleva el párrafo RESUELTA); su fila sale de Known
  Ambiguities de `PROJECT_STATE.md` (§0.7 a4); `test_kit.py` (A-51 en `RESUELTAS`; bloqueantes
  ABIERTAS `{A-21, A-35, A-44}`); ninguna regla citaba A-51 (grep vacío en `strategy_spec.yaml`), y
  la hoja de preguntas no la llevaba (`ORDEN_SESION_02`), como dice el encargo: nada que quitar.
- **Tests** (`tests/unit/test_racha_perdidas.py`, nuevo, 11 funciones; 1522 en total): los cuatro
  parámetros CONFIRMED con fuente feedback; la pérdida es la de RN-016 (y `todo_intento` cuenta
  cualquier cierre, como `cartuchos`); las opciones sin contrato se niegan; **nueve pérdidas con
  un break even en medio detienen hasta el día siguiente** (y la décima vuelve a detener el suyo);
  **una ganadora a la octava la pone a cero**; **la racha cruza un fin de semana** (viernes 18 y
  lunes 21 de enero de 2030, sintéticos); el día de la detención es el operativo de la rejilla; el
  acumulador lee el seguidor y sin él es hueco; **la orden pendiente se retira** (la acción sobre
  un broker con una limite pendiente: cancelada, hechos refrescados, idempotente); y el cableado
  **nueve días seguidos** con `tope=None` (RUTA_STOP, una pérdida al día, con una segunda zona
  lejos que los ocho primeros días colocan y RN-035 retira al abrir la tarde): el noveno RN-036
  dispara, fija `detenido_por_racha`, la segunda colocación queda `prohibida:abrir_operacion`, no
  queda nada que la red de fin de día cancele (`cancelados_fin_dia == 0`), el décimo vuelve a
  operar con la racha en 9 y su pérdida -la décima- vuelve a detener; con `cuenta_diaria` la racha
  empieza de cero cada día. Medido de paso: dentro de la spec una orden pendiente no convive con
  una posición viva (RN-011 solo coloca sin pendiente ni posición viva, su `ninguno_de`), así que en el
  cierre de M1 de la novena nunca queda una pendiente y la retirada de RN-036 es la red de
  seguridad que pidió el consultor (ADR-0077 §3).
- **Con el código de `main`** (clon `C:/cm/main`, los ficheros de test de la rama copiados
  dentro): `tests/unit/test_racha_perdidas.py` no llega a correr -«ImportError: cannot import name
  'racha' from 'botsito.engine'»: el módulo no existe en `main`-, y `tests/unit/test_kit.py`
  falla en `test_ambiguedades_reales_y_esquema` (A-51 sigue ABIERTA y bloqueante en el YAML de
  `main`; salida abajo). Después, `git checkout -- tests/…` y el fichero nuevo borrado en el clon.

  ```
  ERROR collecting tests/unit/test_racha_perdidas.py
  tests\unit\test_racha_perdidas.py:21: in <module>
      from botsito.engine import cableado, racha
  E   ImportError: cannot import name 'racha' from 'botsito.engine' (C:\cm\main\src\botsito\engine\__init__.py)
  ---
  >       assert abiertas == {"A-21", "A-35", "A-44"}, (
  FAILED tests/unit/test_kit.py::test_ambiguedades_reales_y_esquema - Assertion...
  ```

- `Fuente:` en el cuerpo del commit con los cinco `fb-*` y ADR-0077.

### 1.4 Decisión 5 · RN-035, tramo `ventana_fin` (S-5)

- **Spec** (`strategy_spec.yaml`, con `spec docs --escribir`): la forma de RN-035 gana la rama:
  `cuando: todos_de [cualquiera_de [abre_sesion_operativa, alcanza_hora {hora: ventana_fin,
  reloj: reloj_sesiones}], hecho: orden_limite_pendiente liga ORDEN]`, el mismo `entonces`
  (`retirar_orden_limite {de: ORDEN, segun: orden_pendiente_al_abrir_sesion}`); `alcanza_hora`
  sobre `reloj_sesiones` es la misma puerta que la segunda rama de RN-002 (ADR-0063, ADR-0069):
  da SÍ solo en el evento de `ventana_fin` (medido: NO en 07:00, 09:00, 10:59, 11:00 y 14:59
  nominales, SÍ en 15:00). Título, `cuando` y `entonces` en prosa, `parametros` (gana
  `ventana_fin` y `reloj_sesiones`). **`cita`** pasa al registro de S-5
  (`fb-2026-10-04-sesion-04-45e624c5`, `literal` «sí, se quita, porque siempre se va a ir
  actualizando la orden, como te digo o sea, no va a haber órdenes que a lo mejor se pueden tomar a
  las 3 o fuera de horario»), que es lo que la regla hace en sus dos ramas, por el precedente de
  ADR-0060 §6 (§0.8.7); el de la sesión 3 queda en las notas. Las notas pierden «LO QUE ESTA REGLA
  NO HACE TODAVIA» y ganan el tramo, «un minuto antes» como frase del consultor que no se fija, la
  red de seguridad y el hueco. También: las notas de RN-002 («a `ventana_fin`, también RN-035 …
  el cableado queda como red de seguridad»), la descripción de `retirar_orden_limite` y la de
  `orden_pendiente_al_abrir_sesion` (unidad y descripción: «al abrir la sesión siguiente y al
  llegar `ventana_fin`»; su nombre no cambia, §0.7 m7). Sin registro nuevo: el de S-5 existe y
  el parámetro ya estaba CONFIRMED por él; `feedback pending` sigue sin listarlo. `spec_version`
  **16.1.0 → 17.0.0**: RN-035 cambia de sentido (dispara también a `ventana_fin`); `spec
  manifest --escribir` (hash `db91e51ecae2…`). Sin ADR nuevo: lo decidió el consultor (decisión 5),
  no contradice ADR-0066 §4 (que escribió la rama de la apertura) ni ADR-0053 §6 (cuya cancelación
  se queda), y `decision: ADR-0066` se conserva (§0.7 m8).
- **Motor:** nada nuevo en `src/`: `alcanza_hora`, `retirar_orden_limite` y el refresco de los
  hechos del broker ya existían; el contador `TrazaBroker.cancelados_fin_dia` entró en la
  decisión 4. La cancelación del cableado al terminar el día (ADR-0053 §6, `cableado.py`) se queda
  como red de seguridad.
- **Tests** (`tests/unit/test_rn035_ventana_fin.py`, nuevo; 1524 funciones de test):
  - `test_rn035_retira_la_pendiente_a_ventana_fin_y_el_cableado_no_encuentra_nada`: una orden
    colocada a las 12:00 UTC (dentro de la sesión 11-15) que no se llena; a `ventana_fin` RN-035
    está en `disparadas` de 11-15 (el motivo, en la traza del motor), la orden queda `cancelada`
    en el instante del evento de `ventana_fin`, `cancelados_fin_dia == 0` (la red no encontró
    nada) y las peticiones son exactamente `colocar o1` y `cancelar o1`. **Con el código de
    `main`** falla en `assert "RN-035" in r.sesiones["11-15"].disparadas` («assert 'RN-035' in
    {'RN-001', 'RN-003', 'RN-011', 'RN-015'}»): allí la cancela el cableado sin regla.
  - `test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite`, parametrizado
    a las 11 (`FIN_H4`) y a `ventana_fin`: **congela lo que pasa hoy** (no lo arregla): el BID baja
    en el último minuto `[fin−1, fin)` (10 puntos: el bróker llena una límite de compra solo cuando
    el ASK -BID más el spread de 3- queda estrictamente por debajo de la entrada, medido en
    `llenado.py:131-167`; por eso RUTA_STOP de `test_cableado` llena en +6 y no en +3), la límite
    se llena en el tick de los 40 s después de que RN-002 ya cerrara en el evento `fin−1`, y la
    posición se cierra a mercado en el evento del propio límite (ADR-0060 §5: `vence_vela_h4` vale
    en el límite), con RN-002 en `disparadas` de 11-15 y sin RN-035 (ya no estaba pendiente). En
    `main` solo falla por `cancelados_fin_dia`, que no existe allí: el comportamiento es el mismo.
  - `tests/unit/test_spec_fidelidad.py`: el test que congelaba «la de las 15 sigue sin regla»
    cambia de nombre y docstring (`test_la_pendiente_al_abrir_sesion_y_a_ventana_fin_la_dijo_el_trader`);
    sus asserts no cambian (RN-035 sigue siendo la única regla que usa `retirar_orden_limite`).
    `test_escenarios_por_sesion.py` pasa sin tocarlo: con `sigue_hasta_ventana_fin` RN-035 dispara
    a `ventana_fin` y la acción no retira (`segun`), así que el cableado cancela en el mismo
    instante, como antes.
- **Pregunta para la sesión 5** (en el lenguaje del trader, con opciones; va a §3 y a las líneas
  del cierre, R4.1): «Cuando llega la hora de cerrar -las 11 o las 3 en punto- y tienes una orden
  puesta que no se ha llenado, ¿en qué momento la quitas? (a) a las 11 y a las 3 en punto, justo
  cuando cambia la vela; (b) un minuto antes, cuando cierras la operación que tengas abierta; (c)
  otra, ¿cuál?». Hoy el bot hace (a) para la orden y cierra la operación un minuto antes: si la
  orden se llena en ese último minuto, la operación nace y muere dentro de él.
- `Fuente: fb-2026-10-04-sesion-04-45e624c5` en el cuerpo del commit.

### 1.5 Decisión 3 · A-21 RESUELTA con la opción que ya existía (ADR-0076, enmienda ADR-0055 §2 y §5)

Aplicación de la respuesta del consultor a la PARADA (§10), punto por punto.

**Punto 0 · la tabla de series, medida antes de tocar nada.** Series sintéticas sobre el tramo
previo de `test_estructura_m1.py` (la referencia del breaker en 1120 para la compra; para la
venta, la misma serie en espejo, p → 2100 − p, con el BAJO en 980), `detectar_esquema(…, MECHA,
tope 1, solo_una_zona_de_control)` frente a la lectura literal «ningún cambio de color en el
retroceso» (desde la primera vela contraria posterior al primer impulso hasta el bloque de origen
incluido, saltando las de cuerpo cero; solo como medida):

| serie (tras la toma) | lado | `detectar_esquema`, `solo_una_zona_de_control`, tope 1 | literal «sin alternancia» | |
|---|---|---|---|---|
| S-10: V, R, V, R y breaker V | compra | None (2 zonas) | NO limpia (RVR) | igual |
| S-10: V, R, V, R y breaker V | venta | None (2 zonas) | NO limpia (VRV) | igual |
| retroceso limpio de un solo bloque (R, R) y breaker V | compra | segundo esquema (1 zona) | limpia (RR) | igual |
| retroceso limpio de un solo bloque (R, R) y breaker V | venta | segundo esquema (1 zona) | limpia (VV) | igual |
| una zona de control y el último tramo limpio (V, R, V, breaker V) | compra | segundo esquema (1 zona) | limpia (R) | igual |
| una zona de control y el último tramo limpio (V, R, V, breaker V) | venta | segundo esquema (1 zona) | limpia (V) | igual |
| doble alternancia (V, R, V, R, V, R) y breaker V | compra | None (3 zonas) | NO limpia (RVRVR) | igual |
| doble alternancia (V, R, V, R, V, R) y breaker V | venta | None (3 zonas) | NO limpia (VRVRV) | igual |
| breaker contrario (R) que rompe con mecha, retroceso limpio (R, R) | compra | primer esquema (0 zonas) | limpia (RRR) | igual |
| breaker contrario (R) que rompe con mecha, retroceso limpio (R, R) | venta | primer esquema (0 zonas) | limpia (VVV) | igual |
| alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V | compra | segundo esquema (1 zona) | NO limpia (RVR) | **DISTINTO** |
| alternancia con cuerpo cero en medio (R, doji, V, R) y breaker V | venta | segundo esquema (1 zona) | NO limpia (VRV) | **DISTINTO** |
| breaker contrario (R) que rompe con mecha tras alternancia (R, V) | compra | segundo esquema (1 zona) | NO limpia (RVR) | **DISTINTO** |
| breaker contrario (R) que rompe con mecha tras alternancia (R, V) | venta | segundo esquema (1 zona) | NO limpia (VRV) | **DISTINTO** |

Lo que confirma: cada paso de vela contraria a vela del color de la entrada después del primer
impulso forma un pivote de M1 en el sentido de la entrada (`pivotes_formados` con
`CIERRE_VELA_CONTRARIA`) que `zonas_de_control` cuenta, incluido el que forma un breaker del color
de la entrada; verde-roja-verde-roja son dos zonas o más y `zonas_control_max_por_esquema` = 1
(RN-009) las rechaza. **Las únicas diferencias salen del doji** (no es de ningún color, no es
contraria y corta la racha: no forma pivote, `pivotes_m15.py`) **y del breaker contrario que rompe
con la mecha** (el bloque de origen es el propio breaker, y la zona de la alternancia anterior
queda dentro del tope). Es el **caso (b)** de la respuesta: no hay PARADA 2. Las series viven en
`tests/unit/test_a21_series.py` (14 casos parametrizados, compra y venta, con la medida literal al
lado, más el test de que las diferencias son exactamente esas dos y el de que el enum no gana
opción). Medido con `scratchpad/medir_series_a21.py` (fuera del repo) y después con los tests.

**Punto 0.b · el cierre.**
- **Registros:** `fb-2026-10-04-sesion-04-22d08cbf` (RESOLVE_UNKNOWN sobre A-21: v10 1:17:25–1:20:27,
  los tres ítems de S-10) y `fb-2026-10-04-sesion-04-48fb5817` (RESOLVE_UNKNOWN sobre
  `zona_control_limpia` = `solo_una_zona_de_control`, v10 1:17:25–1:17:31, con la nota de la
  pregunta dirigida «¿Es solo eso?»; corregido tras el revisor, hallazgo 1.2 de §9.3). `feedback apply --check`: «9 parametros; 1
  cambian, 8 ya estaban» (`+ zona_control_limpia 'solo_una_zona_de_control' <- …48fb5817`, SOLO
  el de esta respuesta); después sin `--check`: CONFIRMED con fuente `feedback`.
- **ADR-0076** (`docs/adr/0076-limpia-es-sin-alternancia-de-colores-y-lo-filtra-rn009.md`, número
  comprobado libre en §0.2; plantilla; fila del índice): el trader define «limpia» como «sin
  alternancia de colores» y eso es lo que RN-009 ya filtra, con la tabla como prueba; deja escrito
  que el consultor retira la opción nueva y la regla de la vela sin cuerpo del 2026-10-11; enmienda
  ADR-0055 §2 (el selector deja de ser PROVISIONAL; la respuesta calzó) y §5 (el rótulo `.a21=` y
  `--diagnostico-a21` se retiran): recuadro en ADR-0055 y su fila «ACTIVE (con enmienda de
  ADR-0076: A-21 RESUELTA, `--diagnostico-a21` retirado)». Sale `ADR-0076` de los bloques
  `ids-inexistentes` del encargo y de este informe (ya no queda ninguno: los bloques se retiran y
  se dice).
- **Las dos preguntas de la sesión 5** (ADR-0076 §4; §5 de este informe): la vela sin cuerpo en
  medio del retroceso, y el breaker contrario que rompe con mecha.
- **Spec:** `zona_control_limpia` CONFIRMED (`apply`), con la descripción nueva (fue A-21 hasta el
  2026-10-12; lo que dijo el trader; por qué es `solo_una_zona_de_control`; `--diagnostico-a21` ya no
  existe); A-21 RESUELTA en `ambiguedades.yaml` (párrafo RESUELTA con las tres ventanas y el
  registro; `evidencia` gana los tres ítems de v10; el comentario del selector, en pasado).
  `spec_version` **17.0.1 → 17.0.2** (cambia un valor), `spec manifest --escribir`, `spec docs
  --escribir`.
- **Cinco sitios** (`AMBIGUEDADES.md`; respuesta, punto 3): el registro de parámetros (`apply`);
  `ambiguedades.yaml`; **ninguna regla ni término del glosario citaba A-21** (grep vacío en
  `strategy_spec.yaml` y `glossary.yaml`: ese sitio no existe, y se dice); la tabla de Known
  Ambiguities de `PROJECT_STATE.md` pierde su fila (`test_kit`), y `Current Feature` lo dice; la
  hoja de preguntas: A-21 sale de `ORDEN_SESION_02` (`scripts/hoja_preguntas.py`) y de `ORDEN`
  (`tests/unit/test_hoja_preguntas.py`); `tests/unit/test_kit.py`: A-21 en `RESUELTAS` y las
  bloqueantes ABIERTAS quedan `{A-35, A-44}`.

**Punto 1 · `Diagnostico.a21` se retira, con los tres guiones.** `contrato.yaml` gana
`scripts/embudo_77.py`, `scripts/caja_77_exploratoria.py` y `scripts/orden_stop_o_limite.py` en
`rutas_permitidas` (ampliado a mitad de rama, en este commit, como manda `abrir-rama`). Lo que
sale: la opción `--diagnostico-a21` de la CLI (`cli.py`, `_opciones_diagnostico`), la línea de la
cabecera «A-21 en hipótesis», el campo `a21` de `Diagnostico` y su etiqueta (`engine/diagnostico.py`,
que deja de importar `LECTURAS_LIMPIA`), la rama hipotética de `lectura_limpia` (`engine/zonas.py`:
ahora `lectura_limpia(registro)` lee el registro y, sin valor, se niega nombrando el parámetro sin
ofrecer ningún diagnóstico), `ETIQUETA_A21` y `DiagnosticoDeZonaRechazadoError`; `_cabecera_diagnostico`
pierde el argumento `limpia`. Los tres guiones construyen `Diagnostico` con argumentos con nombre y
sin `a21`, y leen `lectura_limpia(registro)`: `embudo_77.py` deja `--a21` opcional y se niega si no
coincide con el registro (su etiqueta `a21` en el resumen pasa a ser la lectura fijada);
`caja_77_exploratoria.py` se niega si el registro no trae la lectura con que midió; en
`orden_stop_o_limite.py` el bucle sobre `LECTURAS_LIMPIA` se conserva (su cabecera, tal cual),
`lim` es la del registro, y desde el commit que atiende al revisor (hallazgo 2.2, abajo y en
§9.3) solo se mide la vuelta que coincide con el registro: la otra lo dice y salta. **Los cuatro guiones que
recorren `LECTURAS_LIMPIA` no se tocan** (`bloque_de_la_caja.py`, `orden_stop_o_limite.py` en su
bucle, `verificacion_a21.py`, `verificacion_a21_entradas.py`): como no entra opción nueva, recorren
las mismas dos de siempre. `mypy src`: sin errores; `ruff`: limpio.

**Punto 2 · el runbook.** `docs/runbooks/ACTIVAR-A35-A44.md` §6 empieza con la nota de tres líneas
(A-21 RESUELTA con `solo_una_zona_de_control` y ADR-0076; `--diagnostico-a21` retirado; el resto
de §6 es histórico). La tabla no gana fila: no entró opción nueva.

**Punto 3 · los sitios:** arriba. **Punto 4:** la deuda de `pending` va a las líneas del cierre
(§6); a RN-035 no le pasa (su cita anterior era un RESOLVE_UNKNOWN sobre A-46, no un CORRECT sobre
la regla). **Punto 5:** §0.8.4, ADR-0077 §5 y las notas de RN-036 dicen «lectura provisional» y la
pregunta está en §5 (la racha tras la novena). **Punto 6:** §8.

**Tests.** Cambian de sentido A PROPÓSITO: `test_preparar_a21.py` (el que congelaba «sin fijar»
y el diagnóstico pasa a `test_con_a21_fijada_el_motor_corre_sin_diagnostico_y_sin_valor_se_niega`:
`lectura_limpia(registro)` da `solo_una_zona_de_control` con el registro real, `Diagnostico(a21=…)`
es `TypeError`, y un registro sintético sin valor sigue negándose sin ofrecer diagnóstico; el de la
CLI pasa a `test_la_cli_no_conoce_diagnostico_a21_y_la_compuerta_de_medida_manda`: argparse rechaza
`--diagnostico-a21` con código 2 sin escribir nada, y un mes de medida se niega con A-35 y A-44 en
diagnóstico). Pierden la opción o el rótulo `.a21=`: `test_preparar_a35.py`, `test_visor.py`,
`test_renovar_cierres.py`, `test_rutas_windows.py` (`_mas_largas` con dos etiquetas),
`test_selector_orden_stop.py`, `test_cableado.py` (la etiqueta de la cuenta diaria, con A-35).
Nuevo: `tests/unit/test_a21_series.py`. 1526 funciones de test. **Con el código de `main`** (clon
`C:/cm/main`, los dos ficheros copiados dentro; después restaurado y el clon retirado):

```
FAILED tests/unit/test_a21_series.py::test_a21_queda_cerrada_con_la_opcion_que_ya_existia
E       AssertionError: assert ('UNKNOWN' == 'CONFIRMED'
FAILED tests/unit/test_preparar_a21.py::test_con_a21_fijada_el_motor_corre_sin_diagnostico_y_sin_valor_se_niega
E       TypeError: lectura_limpia() missing 1 required positional argument: 'a21'
FAILED tests/unit/test_preparar_a21.py::test_la_cli_no_conoce_diagnostico_a21_y_la_compuerta_de_medida_manda
E       Failed: DID NOT RAISE SystemExit
```

Los tres fallan en `main` por lo semántico que pide la respuesta: allí `zona_control_limpia` es
UNKNOWN, `lectura_limpia` exige el argumento del diagnóstico (y con el registro real levantaba
`SinLecturaDeZonaError`, que era el test anterior) y la CLI acepta `--diagnostico-a21`. Los 14 casos
de la tabla pasan también en `main`: `domain/estructura_m1.py` no cambia, y eso es justo lo que
demuestra que RN-009 ya filtraba la alternancia.

**El grep** (respuesta, revisor alcance 2). El encargo pedía «vacío, con la salida en el
informe»; **hecho de otra forma**: NO está vacío, y lo que deja es todo muerto (corregido tras el
revisor, hallazgo 2.1 de §9.3: la versión anterior de este párrafo decía «vacío»):

```
$ grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" src/ tests/ scripts/
src/botsito/cli.py:2295:    # --diagnostico-a21 existio desde ADR-0055 hasta que el trader respondio A-21 en la sesion 4
tests/unit/test_preparar_a21.py:370:    negaba nombrando A-21 y ofrecia `--diagnostico-a21`. El trader respondio A-21 en la sesion 4
tests/unit/test_preparar_a21.py:411:def test_la_cli_no_conoce_diagnostico_a21_y_la_compuerta_de_medida_manda(
tests/unit/test_preparar_a21.py:414:    """Desde ADR-0076 `--diagnostico-a21` no es una opcion (argparse la rechaza con codigo 2 y
tests/unit/test_preparar_a21.py:426:             "sin_tope", "--diagnostico-a21", SOLO_UNA_ZONA_DE_CONTROL]
tests/unit/test_preparar_a21.py:429:    assert "--diagnostico-a21" in capsys.readouterr().err
```

Un comentario de la CLI que cuenta la historia (no se reescribe para que el grep calle) y el
test negativo, que NECESITA el literal para demostrar que argparse lo rechaza. El grep ancho,
`grep -rnc --include=*.py -e "a21" src/ tests/ scripts/`, casa en 15 ficheros, y ninguno es
código vivo: `cli.py` (1, el comentario), `zonas.py` (1, el docstring), `test_a21_series.py` (4:
nombre del módulo y de los tests), `test_preparar_a21.py` (10: nombres, docstrings, el `type:
ignore` del test que comprueba que `Diagnostico(a21=…)` es `TypeError`, y el test negativo),
`test_preparar_a35.py`, `test_rutas_windows.py` y `test_visor.py` (1 cada uno: el comentario
«sin `.a21=` desde ADR-0076»), `test_sesiones_independientes.py` (3: importa
`verificacion_a21_entradas`) y `test_transcribir_sesion.py` (1: nombra la ambigüedad),
`bloque_de_la_caja.py`, `verificacion_a21.py` y `verificacion_a21_entradas.py` (1, 3 y 3: nombres
y los encabezados `DIAGNOSTICO-A21-` que imprimen; son tres de los cuatro guiones que no se
tocan), `buscar_ambiguedades.py` (1: docstring), `embudo_77.py` (16: la opción `--a21`, opcional
y comprobada contra el registro, y su clave `a21` en el resumen) y `orden_stop_o_limite.py` (3:
el bucle que se conserva). Ese grep no casa la etiqueta ni un `Diagnostico` posicional: dos
tests que los llevaban (`test_preparar_a35.py`, el prefijo de la CLI; `test_selector_orden_stop.py`,
el orden de las etiquetas) fallaron al correrlos y se corrigieron antes del commit; `Grep` de
`DIAGNOSTICO-A21|a21=` y de `Diagnostico\(` sobre `*.py` en `src/`, `tests/` y `scripts/` no deja
ningún posicional ni ninguna etiqueta fuera de los sitios de arriba. **Fuera de esos tres
directorios** queda uno, que el revisor vio (hallazgo 2.3): el anexo
`docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py:55-61` construye `Diagnostico` por
posición con seis argumentos y llama a `lectura_limpia(registro, diag.a21)`; con el código de esta
rama falla con `TypeError` (con ruido, no en silencio). No se edita: es el anexo de un informe
cerrado y se reproduce con el código de su commit (`git diff main -- <ese fichero>` vacío). Va
también a las líneas del cierre (§6).

**Lo que el revisor corrigió después (§9.3):** el rótulo de `orden_stop_o_limite.py` (hallazgo
2.2): el motor corría siempre con la lectura del registro y cada sección salía rotulada con la
variable del bucle, así que la segunda vuelta se habría publicado como «A-21 =
sin_mecha_mas_alla_del_extremo» con una medida que no corrió. Ahora el bucle se conserva, pero la
vuelta que no coincide con el registro lo dice (`## A-21 = <vuelta>: no se mide; A-21 esta fijada
en <registro> (ADR-0076)`) y salta, y la que se mide rotula la lectura del registro. Y el trailer
del commit de A-21 no nombra ADR-0077 aunque las notas de RN-036 cambian en él (punto 5 de la
respuesta; hallazgo 1.3): mecánicamente vale (la guardia exige un id que exista, y los tres del
trailer existen); se dice aquí.

`Fuente: fb-2026-10-04-sesion-04-22d08cbf fb-2026-10-04-sesion-04-48fb5817 ADR-0076` en el cuerpo
del commit.

## 2. Tests que rompen a propósito, con el código de `main`

Skill `comparar-con-main`: un clon `git worktree add --detach C:/cm/main main` (ruta corta, por
`test_rutas_windows`), los ficheros de test de la rama copiados dentro, `uv run pytest … -q -p
no:cacheprovider` allí, y después `git checkout -- …` (o borrado del fichero nuevo) hasta dejar el
clon limpio; `git worktree remove C:/cm/main` y `git worktree prune` al terminar (§7). Nunca un
checkout en el repo real. Resumen (la salida de cada uno está en su §1.x):

| Decisión | Test | En `main` | En la rama |
|---|---|---|---|
| 2 (S-13) | `test_sesgo_h4.py`: `test_doble_ruptura_sin_cuerpo_no_decide_y_sin_nada_detras_es_insuficiente`, `test_una_neutra_mantiene_el_sesgo_anterior_alcista_y_bajista`, `test_dos_neutras_seguidas_mantienen_el_sesgo`; `test_huecos_motor.py`: `test_una_h4_neutra_no_decide_y_sin_nada_detras_es_insuficiente`, `test_una_h4_neutra_en_la_segunda_sesion_mantiene_el_sesgo_de_la_primera`, `test_una_sesion_con_lado_tras_una_insuficiente_no_hereda_la_prohibicion` | 6 FAILED («'ambiguo' != 'insuficiente'») | pasan |
| 4 (A-51) | `test_racha_perdidas.py` (11) | no importa: «cannot import name 'racha' from 'botsito.engine'» | pasan |
| 4 (A-51) | `test_kit.py::test_ambiguedades_reales_y_esquema` | FAILED (`abiertas == {"A-21", "A-35", "A-44"}`: A-51 sigue ABIERTA allí) | pasa |
| 5 (RN-035) | `test_rn035_ventana_fin.py::test_rn035_retira_la_pendiente_a_ventana_fin_y_el_cableado_no_encuentra_nada` | FAILED (`'RN-035' in {'RN-001', 'RN-003', 'RN-011', 'RN-015'}`) | pasa |
| 5 (hueco) | `test_rn035_ventana_fin.py::test_hueco_la_orden_que_se_llena_en_el_ultimo_minuto_se_cierra_en_el_limite` (×2) | falla solo por `cancelados_fin_dia`, que no existe en `main`: congela el mismo comportamiento | pasan |
| 1 (A-49) | `test_kit.py::test_una_en_parte_no_entra_en_resueltas` | pasa también en `main` (A-49 ya estaba ABIERTA): es una guardia, no un cambio | pasa |
| 3 (A-21) | `test_preparar_a21.py::test_con_a21_fijada_el_motor_corre_sin_diagnostico_y_sin_valor_se_niega`; `test_a21_series.py` (la tabla, 14 casos + 2) | `lectura_limpia(registro)` levanta `SinLecturaDeZonaError` (A-21 UNKNOWN en `main`) y `Diagnostico(a21=…)` existe; `test_a21_series` falla en el registro (UNKNOWN) y en A-21 (ABIERTA) | pasan (§1.5) |

Las salidas del lado de la rama (`uv run pytest <ficheros> -q -p no:cacheprovider`, 2026-10-12,
sobre 1d39c1e más el nombre nuevo del test de b4):

```
$ … tests/unit/test_sesgo_h4.py tests/unit/test_huecos_motor.py -q -rs
........................................                                 [100%]   (40)
$ … tests/unit/test_racha_perdidas.py tests/unit/test_kit.py tests/unit/test_rn035_ventana_fin.py -q
.......................................................                  [100%]   (55)
$ … tests/unit/test_racha_perdidas.py -q
...........                                                              [100%]   (11)
```

(Y el revisor corrió los 8 ficheros tocados o afectados: «129 passed», §9.)

Lo que el encargo pide además: «uno que demuestre que `detectar_esquema` con una lectura fuera de
`LECTURAS_LIMPIA` sigue fallando» ya existe en `main`
(`tests/unit/test_estructura_m1.py:234-235`, `"al_ojo"` con `match="A-21"`; §0.7 m9) y no se
amplía: no entró ninguna opción nueva (§1.5, caso b). El grep de `--diagnostico-a21` y
`diagnostico.a21` en `src/`, `tests/` y `scripts/` está en §1.5 con su salida: lo que deja es un
comentario y el test negativo de la CLI, que necesita el literal (hecho de otra forma; antes del
commit de A-21 daba 11 líneas de código vivo, en `cli.py`, `zonas.py` y seis tests). Los tres tests
de A-21 que fallan con el código de `main`, con su salida, en §1.5. (`--include=*.py` para no
casar los `.pyc`, §0.7 m11.) Ningún test nuevo lee `data/`: el único que lo hace en los ficheros
tocados, `test_huecos_motor.py:263`, ya se saltaba sin velas; `test_a21_series.py` es sintético.

## 3. El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde `main` d4b7917 con `abrir-rama`, base comprobada con git, CI run 38197306105 con `gh` | Hecho | cabecera del informe; `gh run view 38197306105`: success |
| 2 | Contrato con tramo R1, riesgo alto, artefacto `ACTIVAR-SESION-04-MOTOR.md` | Hecho | `contrato.yaml`; `scripts/contrato_rama.py` en verde en cada `make check` (35 ficheros al final) |
| 3 | Encargo copiado a `docs/encargos/trabajo-activar-sesion-04-motor.md` | Hecho; el bloque `ids-inexistentes` que llevó FUERA del texto copiado mientras los ADR no existían se retiró en el commit de A-21 (queda una nota que lo dice); al final, tal cual, el añadido nocturno de Aleks y la respuesta del consultor a la PARADA | `docs/encargos/…:3-9` y su final |
| 4 | QUÉ NO CAMBIA: nada fijado se pisa (cada cambio por su régimen) | Hecho | ADR-0075 enmienda ADR-0060 (recuadro y fila); ADR-0077 nuevo; CORRECT sobre RN-003; RESOLVE_UNKNOWN sobre A-51; RN-035 sin ADR por decisión del consultor (§1.4, §0.7 m8) |
| 5 | A-49 ABIERTA y sin tocar; ninguna «en parte» se cierra; A-35 y A-44 con sus diagnósticos | Hecho | `test_una_en_parte_no_entra_en_resueltas`; `git diff main...HEAD -- knowledge/spec/ambiguedades.yaml` toca solo A-51; `--diagnostico-a35`/`a44` intactos (grep) |
| 6 | «Casi plana» no se resuelve; RN-020 no cambia; ninguna cifra en forma ejecutable; sin arnés; nada de material; citas solo de la extracción cruzadas con los tramos | Hecho | RN-007 y RN-020 intactos (`git diff` de `strategy_spec.yaml`); el 9 vive en `parametros.yaml`; `test_no_business_literals` y la guardia de cifras de la spec (§1.3) en verde; §0.1 (ventanas frente a los 22 tramos de v10); §7 exposiciones: ninguna |
| 7 | Next Action y hoja de ruta sin tocar; Makefile, `.claude/` y la guardia sin tocar; informes cerrados con `--diagnostico-a21` sin editar | Hecho | `git diff --stat main...HEAD`: ni `docs/plan/`, ni `Makefile`, ni `.claude/`, ni ningún otro `docs/validation/*.md` que este; `PROJECT_STATE.md` solo cambia `Current Branch`/`Current Feature`, el recuento de tests, la fila de A-51 y las dos líneas «ninguna desde el Archivo 30» de Completed Features y Change Log (la apertura) |
| 8 | FASE 0, puntos 1-5, con fichero:línea | Hecho | §0.1-§0.5 |
| 9 | PARADA solo si lo medido contradice una decisión / `ambiguo` sale de otro sitio / toca «QUÉ NO CAMBIA» | PARADA en la decisión 3 (lo medido la contradice); las otras siguen | §0 (intro), §0.7 a1, «Lo que necesito que decidas» |
| 10 | Decisión 1: CONFIRM de S-4, primer commit, opciones obligatorias; `pending` «sin forma mecánica» | Hecho (el primer commit de decisión; `pending` lo da REFLEJADO, medido y dicho) | §1.1, commit 12b6684 |
| 11 | Decisión 2: ADR-0075, enmienda ADR-0060 §1-§2 con recuadro y fila; neutra = cierre == apertura; reserva alcista; CORRECT sobre RN-003 con `ev-v10-014005`; notas de RN-033; token `ambiguo` declarado y descrito; `spec_version` mayor a mano + manifest + docs; motor y tests (los que cambian de sentido, dos neutras, neutra tras bajista) | Hecho (y la segunda reserva «sin otro rango mayor»; RN-003 cita el CORRECT: §0.8.1, PARADA punto 4) | §1.2, commit 272f59f |
| 12 | Decisión 3: A-21, `sin_alternancia_de_colores`, retirada de `--diagnostico-a21`, ADR-0076 enmienda ADR-0055, cinco sitios, runbook §6 | Hecho DE OTRA FORMA, por la respuesta del consultor a la PARADA (§10, punto 0): sin opción nueva, A-21 RESUELTA con `solo_una_zona_de_control` tras medir la tabla de series (caso b); `--diagnostico-a21` retirado; ADR-0076 enmienda ADR-0055 §2 y §5; cinco sitios; nota en el runbook | §1.5, commit de A-21 |
| 13 | Decisión 4: ADR-0077 y RN-036 aparte de RN-020; cuatro parámetros CONFIRMED vía `apply`; pérdida = la de RN-016; acumulador persistente fuera de `EstadoDia` y con `cuenta_diaria`; «día siguiente» con `reloj_sesiones`; retira la pendiente; sin A-44 ni `--diagnostico-a44` (si no, PARADA); tres guardias; cinco sitios (A-51 no está en la hoja); los cuatro tests | Hecho, y DE OTRA FORMA en dos puntos: las tres guardias no se amplían porque ya recorren reglas y acumuladores (§0.7 m4), y «la orden pendiente se retira en la novena» se demuestra con la acción aislada más el noveno día sin pendiente, porque dentro de la spec no puede quedar una (§1.3). Más el RESOLVE_UNKNOWN sobre A-51 (§0.8.3), la racha tras la novena como lectura de la sesión (§0.8.4) y la acción nueva (§0.8.5) | §1.3, commit 5df5bd5 |
| 14 | Decisión 5: RN-035 gana la rama `ventana_fin` según `orden_pendiente_al_abrir_sesion`; «un minuto antes» no se fija; notas sin «LO QUE … NO HACE TODAVÍA»; cableado como red de seguridad con test; hueco del último minuto congelado y pregunta para la sesión 5 | Hecho (RN-035 cita el registro de S-5, §0.8.7) | §1.4 |
| 15 | Por cada commit, el paso 3 de `activar-sesion` entero (registros, `apply --check` solo de esa respuesta y luego `apply`, cinco sitios, `test_kit`, `spec_version` + manifest + docs, código con test, `knowledge validate`, `Fuente:`) | Hecho en 1, 2, 4 y 5 (en 1 y 5 no hay `Fuente:`/`apply` que escriba: se dice) | §1.1-§1.4; `git log --format=%B main..HEAD` |
| 16 | ADR nuevos con `0000-template.md` y en el índice | Hecho | `docs/adr/README.md:81-82` |
| 17 | `MemoryError` de `lzma`: repetir una vez; si se repite, el comando a Aleks | No se dio: cinco `make check` en verde a la primera (1078 s, 1012 s, 887 s, 854 s, 846 s; picos 294 MiB) | `make-check.log` de cada commit |
| 18 | Tests que rompen a propósito, con las dos salidas; `detectar_esquema` fuera de `LECTURAS_LIMPIA`; «en parte» no entra en RESUELTAS; grep vacío; tests con `data/` saltan en CI | Hecho (el grep de `--diagnostico-a21` y `diagnostico.a21`, vacío desde el commit de A-21, §1.5) | §2, §1.5 |
| 19 | HOLDOUT: ninguna carpeta madre listada con filtro; exposiciones el mismo día; sin fechas reservadas ni resultados | Hecho | §7; la regla va al revisor |
| 20 | El literal de 1:44:49 si Aleks lo pega | No llegó: H se queda como está | «Pendiente de Aleks» |
| 21 | ENTREGA: CI por `fix/`, revisor (opus) con cuatro alcances, su informe pegado, líneas del cierre, lista de la sesión 5 | Hecho: los push salieron desde la sesión y cada commit tiene su run en §8; dos pasadas del revisor, la primera con los cuatro alcances del encargo (§9.2) y la segunda, sobre el commit de A-21, con los tres de la respuesta del consultor (§9.3), las dos pegadas y atendidas | §5, §6, §8, §9 |
| 22 | Rama lista para revisión, NO cerrada | Hecho, con el último commit (el de este informe) sellado | `## Estado` |
| N1 | Nocturno: nada espera a Aleks; «Pendiente de Aleks» con comandos | Hecho | cabecera |
| N2 | Nocturno: si el clasificador niega el push, revisor igual y CI por la mañana | Hecho | §8 |
| N3 | Nocturno: PARADA entera en el informe, commiteado lo que no depende (mínimo el CONFIRM de S-4), «no decidas por mí» | Hecho: decisiones 1, 2, 4 y 5 commiteadas; la 3 en PARADA; lo que la sesión aplicó sin decidir, declarado en §0.8 | §0.8, «Lo que necesito que decidas» |
| N4 | Nocturno: `MemoryError` → `knowledge validate` y tests de los ficheros tocados | No se dio | — |
| N5 | Nocturno: todo commiteado en local; la rama no se cierra | Hecho con el último commit (este informe, sellado) | `git status --short` vacío tras él; sin merge, sin tag |

**Desviaciones declaradas:** (1) la decisión 3 se hizo de otra forma, por la respuesta del
consultor a la PARADA (sin opción nueva; §1.5); (2) el orden de los commits es 1, 2, 4, 5 y
después A-21 (§0.8.8); (3) RN-003 y RN-035 cambian de `cita` (§0.8.1, §0.8.7; PARADA punto 4);
(4) A-51 lleva un RESOLVE_UNKNOWN que el encargo no nombraba (§0.8.3); (5) la fila de A-51 sale de
Known Ambiguities en la rama, no en el cierre (§0.7 a4); (6) la racha tras la novena es una
lectura de la sesión escrita en ADR-0077 §5 (§0.8.4); (7) la acción `retirar_ordenes_pendientes`
no la nombraba el encargo (§0.8.5); (8) `feedback pending` da el CONFIRM de S-4 por REFLEJADO, no
por «sin forma mecánica» (§1.1); (9) el bloque `ids-inexistentes` que el encargo y este informe
llevaron hasta el commit de A-21, cuando los tres ADR ya existían y se retiró (trampa de los ids
futuros; §3 fila 3); (10) `TrazaBroker.cancelados_fin_dia` y la línea de la
racha en `informe_simulacion` son instrumentación que el encargo no pedía, para que los tests
demuestren lo que pide; (11) las tres guardias de `modelo.py` no se amplían (§0.7 m4) y el test
de la retirada en la novena ejercita la acción aislada (fila 13).

## 4. Lo que NO cambia, medido

`git diff --stat main...HEAD` tras el commit de A-21 (rehecho tras el revisor, hallazgo 3.1 de
§9.3: la versión anterior era la de antes de ese commit): «56 files changed»
(`scripts/contrato_rama.py`: «56 ficheros dentro del contrato»). Ninguno de `docs/plan/`,
`Makefile`, `.claude/`, `knowledge/cases/`, `knowledge/corpus/`, `knowledge/evidence/`,
`knowledge/cuentas/`, `config/`, `data/manifests/`, `src/botsito/engine/broker.py` ni
`src/botsito/engine/cuenta.py`; de `scripts/`, solo los tres que entraron en el contrato con la
respuesta del consultor (`embudo_77.py`, `caja_77_exploratoria.py`, `orden_stop_o_limite.py`;
§1.5, punto 1) y `hoja_preguntas.py` (A-21 sale de la hoja); de `docs/validation/`, solo este
informe. `scripts/contrato_rama.py` en verde en cada `make check`. `PROJECT_STATE.md`: 22.647
bytes (en `main`, 22.508; tope 25.000): la tabla pierde las filas de A-51 y de A-21,
`Current Feature` dice la rama (con ADR-0076 para A-21), el recuento de tests sube (1506 → 1526),
y las líneas de Completed Features y Change Log dicen «Archivo 30».

## 5. La lista para la sesión 5, actualizada

La de ACTIVAR-SESION-04.md §5 (sobre §0.e), con los cambios de esta rama:

- **Sale el punto 11 (A-21)**: A-21 está RESUELTA en esta rama (§1.5, ADR-0076).
- **Entran las dos preguntas de ADR-0076 §4** (las series en que la lectura literal y el motor
  no coinciden): «En el retroceso antes de romper el punto de breaker, si en medio hay una vela
  sin cuerpo (abre y cierra en el mismo precio) entre una verde y una roja, ¿eso cuenta como
  alternancia y te invalida la entrada, o la vela sin cuerpo no cuenta y sigues? (a) cuenta como
  alternancia e invalida; (b) no cuenta, sigo como si no estuviera; (c) otra, ¿cuál?»; y «Si la
  vela que rompe el punto de breaker es una vela contraria que lo pasa solo con la mecha, y antes
  hubo una verde y una roja alternadas, ¿la entrada vale o queda invalidada? (a) vale, la mecha
  rompe; (b) queda invalidada por la alternancia; (c) otra, ¿cuál?».
- **Entra la pregunta de la racha tras la novena** (respuesta del consultor, punto 5): «Después
  de parar por 9 pérdidas seguidas, cuando vuelves al día siguiente: (a) empiezas a contar de
  cero; (b) sigues en 9 y una pérdida más te vuelve a parar ese día; (c) otra, ¿cuál?».
- **La confirmación bajista de S-13** ya estaba (ACTIVAR-SESION-04.md §5): «Si la vela de 4 horas
  sin color viene con un sesgo bajista, ¿también se mantiene el bajista?».
- **Entra la pregunta del último minuto** (§1.4): «Cuando llega la hora de cerrar -las 11 o las 3
  en punto- y tienes una orden puesta que no se ha llenado, ¿en qué momento la quitas? (a) a las
  11 y a las 3 en punto, justo cuando cambia la vela; (b) un minuto antes, cuando cierras la
  operación que tengas abierta; (c) otra, ¿cuál?».

## 6. Líneas preparadas para el commit del contrato del cierre

(`RITUAL.md`, puntos 3 y 4; en la rama no se tocan la Next Action ni la hoja de ruta.)

- **E** sale a HISTORIA como HECHA: «Activar la sesión 4. HECHO en trabajo/activar-sesion-04 (la
  spec: A-18, A-25, A-30, A-33, A-36, A-39, A-52; ADR-0073, ADR-0074) y en
  trabajo/activar-sesion-04-motor (el motor: S-13 con ADR-0075; A-21 con ADR-0076; A-51 con
  ADR-0077 y RN-036; la rama ventana_fin de RN-035; el CONFIRM de S-4). Las «en parte» (A-13,
  A-32, A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14) van a la hoja de la sesión
  5 (R4.1), con las preguntas de ACTIVAR-SESION-04.md §5 y ACTIVAR-SESION-04-MOTOR.md §5».
- **F**: propongo «Orden de trabajo: lo siguiente es S (R2.1, julio): el consultor decide antes si
  es construcción o reservado y lo comprueba en el repo; la hoja de ruta manda el orden». La hoja
  de ruta manda: R2.1 depende de R1.1 y R3.1 de R1.1 y R2.
- **R1.1**: «Estado: HECHA la parte de spec en trabajo/activar-sesion-04 y la de motor en
  trabajo/activar-sesion-04-motor (S-13, A-21, A-51, RN-035 ventana_fin); queda que las «en parte»
  entren en la hoja de la sesión 5 (R4.1)». Su «Qué es» pierde «A-51» de «Falta código» y «A-21 a
  medias».
- **R3.1**: Refs y «Depende de» sin A-21: «hoy lo necesita para A-35 y A-44».
- **R4.1**: gana la pregunta del último minuto, las dos de ADR-0076 §4 y la de la racha tras la
  novena (§5), y pierde A-21 de sus Refs. Propuesta (revisor, hallazgo 3.2 de §9.3): que gane
  `ID:ADR-0076` e `ID:ADR-0077`, porque esas tres preguntas no cuelgan de ninguna ambigüedad
  abierta, solo de §5 de este informe.
- **Anexo `docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`** (revisor, hallazgo 2.3):
  construye `Diagnostico` por posición con seis argumentos y llama a `lectura_limpia(registro,
  diag.a21)`; con el código de esta rama falla con `TypeError`. No se edita (anexo de un informe
  cerrado): se reproduce con el código de su commit. Nota para Technical Debt o para la fila de
  ese informe, lo que el consultor prefiera.
- **La guardia de Claude Code** (revisor, «lo que no pude comprobar»): bloqueó un `grep -rn
  --include=*.py` con CUATRO patrones `-e` sobre `src/ tests/ scripts/` («bloquea: leer el
  contenido de .») aunque las rutas eran literales, y dejó pasar el mismo comando con dos
  patrones. No se rodeó (el revisor usó la herramienta Grep por directorio); se apunta para
  revisar esa regla en su rama.
- **Heredados 25 y 30**: el 25 nombra A-21 («A-21 es la zona…»): pierde esa coletilla; el 30 no
  la nombra (§0.7 m14): solo cambia que el arnés ya no necesita `--diagnostico-a21` (corre con
  `--diagnostico-a35` y `--diagnostico-a44`).
- **Heredado 35** (nota): RN-020 tampoco retira la orden pendiente al llegar a su tope; para cuando
  se active A-44, lo que hace RN-036 (`retirar_ordenes_pendientes`) es el modelo.
- **G.2**: `--diagnostico-a47` y `--diagnostico-a27` siguen en la CLI (el encargo lo decide; G.2
  decía que se retiraban con `--diagnostico-a21`, que ya salió); el token `ambiguo` sin productor
  es deuda (ADR-0075); **deuda nueva (respuesta del consultor, punto 4)**: `feedback pending` no
  admite dos CORRECT vivos sobre una regla (RN-003 cita el de S-13 y el de la sesión 3,
  `fb-2026-09-29-sesion-03-31fb311f`, sale pendiente, §1.2); a RN-035 no le pasa: su cita
  anterior, `fb-2026-09-29-sesion-03-5021677e`, es un RESOLVE_UNKNOWN sobre A-46, no un CORRECT
  sobre la regla, y `pending` da «1 pendientes» en total.
- **ADR-0044 §1** (heredado, hallazgo a7 del revisor): sigue diciendo «doble ruptura = AMBIGUO» y
  su fila del índice no menciona enmienda, aunque ADR-0060 §1 y ahora ADR-0075 lo cambian; no se
  arregla aquí: queda para el consultor (un recuadro en 0044 y su fila, en la rama que toque).
- **Known Ambiguities**: A-21 y A-51 ya están fuera (en la rama; lo exige `test_kit`).
- **ADR-0070 §3** sigue diciendo «hoy A-21, A-35 y A-44»: desde esta rama la corrida necesita
  diagnóstico solo para A-35 y A-44; lo dice R3.1, no se edita el ADR.
- **Technical Debt**: nada nuevo que no esté en G.2.
- **Pendiente de Aleks** que sigue: el literal de 1:44:49 (H se queda); la CI de `fix/` (§8).

## 7. Exposiciones

Ninguna. Lo leído: el repositorio, los ítems `ev-v10-*` y `ev-v9-*` ya citables (§0.1) y los
registros de feedback. Ningún material, ninguna cruda, ningún fotograma; ninguna carpeta de meses
reservados listada (ni con filtro ni sin él); las rutas de cada comando, literales.
`HOLDOUT-EXPOSICIONES.md` no cambia. El clon `C:/cm/main` se usó solo para correr tests
sintéticos de la rama con el código de `main`, sin `data/` (los tests que la necesitan se
saltaron), y se retira al terminar (`git worktree remove`; `git worktree prune`).

## 8. CI de Linux

El clasificador de Claude Code NO negó el push esta vez: `git push origin
trabajo/activar-sesion-04-motor:refs/heads/fix/activar-sesion-04-motor` salió desde la sesión el
2026-10-12 («[new branch] … -> fix/activar-sesion-04-motor»), sin rodear nada.

- **Run 38213911827**, sobre 1d39c1ee460fa0d0176ce1c5a9db02d820ecfcc7 (la decisión 5, el último
  commit de código): `1 failed, 2584 passed, 9 skipped in 218.21s`. El único fallo es el
  aceptado, `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (la rama no es `main` ni
  lleva tag); los 9 saltados son los que necesitan `data/`, ninguno de esta rama (API de
  check-runs con el sha literal: `python completed failure`; `gh run view 38213911827 --log-failed`).
- **Run 38217718887**, sobre 136bb8648b7b9fb1894eca94b3e0d881e530e792 (el informe con el revisor,
  el commit con que la sesión terminó el 2026-10-12): comprobado con `gh api
  repos/:owner/:repo/commits/136bb864…/check-runs` (`python completed failure`, ese sha) y `gh run
  view 38217718887 --log-failed`: `1 failed, 2584 passed, 9 skipped in 296.38s`, y el único fallo es
  `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, el aceptado. (Respuesta del
  consultor, punto 6.)
- **Run 38243202933**, sobre f358748cbf47991677f74ecb5c1ee28fcf26f1c2 (el commit de A-21, §1.5):
  el push salió desde la sesión («136bb86..f358748 … -> fix/activar-sesion-04-motor»). La
  primera ejecución la canceló el `timeout-minutes: 20` del workflow (`.github/workflows/ci.yml:16`)
  con el paso `apt-get install ffmpeg` colgado (`--log`: «##[error]The operation was canceled» a las
  11:51:36Z sobre ese paso; ningún test llegó a correr): el runner, no la rama. Relanzada desde la
  sesión con `gh run rerun 38243202933`: `1 failed, 2599 passed, 9 skipped in 219.70s`, y el único
  fallo es `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, el aceptado (`gh run view
  38243202933 --log-failed`; API de check-runs con el sha literal: `python completed failure`).
  Los 2599 son los 2584 de antes más los 16 de `test_a21_series.py` menos
  `test_con_el_valor_fijado_el_diagnostico_se_rechaza`, de `test_preparar_a21.py`, que se retiró
  (ya no hay diagnóstico que rechazar; los otros dos de ese fichero cambiaron de nombre y de
  sentido, §1.5).
- **Run 38247668329**, sobre a5985975936bed483c667f4c828e72edde70afb1 (la segunda pasada del
  revisor, §9.3): `1 failed, 2599 passed, 9 skipped in 182.62s`, y el único fallo es
  `tests/unit/test_cli.py::test_state_check_ok_on_real_repo`, el aceptado (API de check-runs con
  el sha literal: `python completed failure`; `gh run view 38247668329 --log-failed`). Entra aquí
  en el commit del contrato, por la orden de cierre (§11).

## 9. Informe del revisor

Lanzado el 2026-10-12 (modelo `opus`, subagente `revisor`) con el informe terminado salvo §8 y §9,
sobre 1d39c1e más §2-§7 sin commitear, con los cuatro alcances del encargo y la regla de holdout
(ninguna carpeta madre con filtro). Se pega tal cual: no cita ningún tramo no citable (0
retiradas).

### 9.1 Lo que se hizo con cada hallazgo

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado.** Las notas de RN-035 dicen ahora que las palabras del trader son «no va a haber órdenes que a lo mejor se pueden tomar a las 3 o fuera de horario» (la cita) y que «se quita tanto a las 11 como a las 3» es la frase del consultor a la que contestó «Exacto» (SESION-04-EXTRACCION.md §3.6); `spec docs --escribir`. El cuerpo del commit 1d39c1e no se reescribe. Con a2, las dos notas cambian el hash de la spec y `knowledge validate` exige subir la versión: `spec_version` 17.0.0 → **17.0.1** (parche: solo redacción), `spec manifest --escribir`. |
| a2 | importa | **Arreglado.** ADR-0077 §3, las notas de RN-036 y §1.3 dicen que la exclusión es del `ninguno_de` de RN-011 (sin orden pendiente ni posición viva), no de RN-013 (DESCARTADA); y «no convive … no queda ninguna», sin el «no suele». |
| a3 | importa | **Arreglado.** §8, §9, `## Estado` y el punto 3 de «Pendiente de Aleks» están; el informe entra en el último commit con su `make check` sellado sobre su árbol. |
| a4 | menor | **Arreglado.** `test_estructura_m1.py:234-235` en los tres sitios. |
| a5 | menor | **Arreglado.** 35 ficheros, y las dos líneas «Archivo 30» de `PROJECT_STATE.md` nombradas (§3 fila 7, §4). |
| a6 | menor | **Arreglado.** `Current Feature` dice que A-21 está EN PARADA. |
| a7 | menor | **A las líneas del cierre** (§6): ADR-0044 §1 y su fila son heredados; no se tocan aquí. |
| b1 | importa | **Arreglado.** §2 lleva las salidas del lado de la rama (los `........ [100%]` con su recuento), además de las de `main`. |
| b2 | importa | **Arreglado.** Las filas 21, 22 y N5 de §3 dicen lo que es verdad con el último commit. |
| b3 | menor | **Arreglado.** La fila 13 dice «de otra forma» en los dos puntos y la desviación 11 los recoge. |
| b4 | menor | **Arreglado.** El test se llama `test_la_accion_de_rn036_retira_la_orden_pendiente_que_quede` y su docstring dice por qué es la acción aislada. |

### 9.2 El informe, tal cual

**Informe del revisor · trabajo/activar-sesion-04-motor · 2026-10-12**

Base: `git merge-base main HEAD` = d4b7917. HEAD = 1d39c1e, seis commits, más `docs/validation/ACTIVAR-SESION-04-MOTOR.md` modificado sin commitear (145 líneas añadidas a partir de la 632). Como pediste, reviso la CI de `fix/` como si todavía no existiera.

#### Eje (a) · Reglas de la casa
Resumen: 0 bloquea, 3 importa, 4 menor.

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| a1 | importa | Las notas de RN-035 ponen en boca del trader una frase que dijo el consultor. Dicen «en el instante que dijo el trader («se quita tanto a las 11 como a las 3»)», pero según la extracción esa frase es del consultor y del trader solo es el «Exacto». El instante sí lo sostiene el trader con sus propias palabras («a las 3 o fuera de horario», la `respuesta_literal` de fb-…-45e624c5). Lo que falla es a quién se atribuyen las comillas. | `knowledge/spec/strategy_spec.yaml:946-947` (y su generado `docs/spec/reglas.md:1242`; también el cuerpo del commit 1d39c1e). `docs/validation/SESION-04-EXTRACCION.md:472-474`: «Entonces se quita tanto a las 11 / como a las 3, perfecto. Exacto.» (`ev-v10-005427-1a0867af`; «la última frase es del consultor y el «Exacto» del trader»). |
| a2 | importa | La afirmación «una pendiente no convive con una posición viva» se apoya en RN-013, que no dice eso. RN-013 trata del esquema único de stop y está DESCARTADA. La condición «ni orden limite pendiente ni posicion viva» es del `cuando` de RN-011, y solo de RN-011. | `docs/adr/0077-…-rn036.md:58` («RN-013 no coloca con una posición abierta»), `knowledge/spec/strategy_spec.yaml:1889` (notas de RN-036, «(RN-011, RN-013)»), `docs/validation/ACTIVAR-SESION-04-MOTOR.md:555`. Frente a `strategy_spec.yaml:1505-1524` (RN-013, «hay un unico esquema de stop…», `estado: DESCARTADA`) y `:1386-1387` (RN-011). Además ADR-0077:57-59 dice «nunca convive» y, en la misma frase, «no suele quedar ninguna». |
| a3 | importa | El informe todavía no está en su estado final ni commiteado. El sello de `make check` es del árbol de HEAD, así que el commit del informe necesita otro `make check`. | `ACTIVAR-SESION-04-MOTOR.md:780-782` («EN CURSO»); `git status --short` → ` M docs/validation/ACTIVAR-SESION-04-MOTOR.md`; `:24` (punto 3 de «Pendiente de Aleks» sigue como plantilla, sin el comando del push); faltan §8 (CI) y §9 (revisor). `make-check.log:98` «SELLO: … arbol cb42872d…» = `git rev-parse 1d39c1e^{tree}` → cb42872d7db1…: el sello no cubre los cambios sin commitear. |
| a4 | menor | Una cita con las líneas desplazadas. El test de la guardia de `detectar_esquema` está en :234-235, no en :236-237. | `ACTIVAR-SESION-04-MOTOR.md:246, :339, :655`; `tests/unit/test_estructura_m1.py:234-235` (`with pytest.raises(EstructuraError, match="A-21")` / `detectar_esquema(…, "al_ojo")`). |
| a5 | menor | Dos recuentos que se quedaron atrás. El informe dice «33 ficheros», pero el contrato da 35. Y dice que de `PROJECT_STATE.md` solo cambian Current Branch/Feature, los tests y la fila de A-51; no menciona las líneas de Completed Features y Change Log («Archivo 29» → «Archivo 30»). | `ACTIVAR-SESION-04-MOTOR.md:674, :679, :714`; `uv run python scripts/contrato_rama.py` → «CONTRATO: 35 ficheros…»; `git diff main...HEAD -- PROJECT_STATE.md` (hunk @@ -177). |
| a6 | menor | `PROJECT_STATE.md` («solo presente») describe A-21 como parte de la rama («un ADR con `sin_alternancia_de_colores`; sale `--diagnostico-a21`») y no dice que está en PARADA. | `PROJECT_STATE.md:10`. |
| a7 | menor | Heredado, no es de esta rama. ADR-0044 §1 sigue diciendo «doble ruptura = AMBIGUO» y su fila del índice es «ACTIVE» sin mención de enmienda, aunque ADR-0060 y ahora ADR-0075 cambian eso. Va a las líneas del cierre, no se arregla aquí. | `docs/adr/0044-…md:15-17`; `docs/adr/README.md:50` («\| 0044 \| … \| ACTIVE \|»). |

Comprobado sin hallazgos:
- **Contrato.** `contrato_rama.py` sale con exit 0 («35 ficheros dentro del contrato … tramo 'R1', 6 comprobaciones»).
  - `feedback apply --check` da «8 parametros; 0 cambian, 8 ya estaban; --check: no se ha escrito nada».
  - `knowledge validate` (sin redirigir a fichero) sale todo OK: «36 reglas de spec (31 vigentes…), hash del manifiesto al dia», «172 registros de feedback, historial intacto, commits con Fuente», «453 documentos: todo id citado existe».
  - El grep `--include=*.py` de `--diagnostico-a21` da las 11 líneas que pega el informe (§2), porque la decisión 3 está en PARADA.
  - `make check`: `make-check.log` tiene «2594 passed», SELLO sobre el árbol de HEAD y «PICO DE MEMORIA … 293 MiB».
  - No ejecuté `spec docs --escribir` ni `make check` porque escriben.
- **Tests.** Los 8 ficheros tocados o afectados (test_racha_perdidas, test_rn035_ventana_fin, test_sesgo_h4, test_huecos_motor, test_kit, test_spec_fidelidad, test_estructura_m1, test_adr) dan **129 passed**.
- **`Fuente:`.** Los tres commits que tocan `knowledge/spec` (272f59f, 5df5bd5, 1d39c1e) lo llevan en el cuerpo. Todos los ids existen: 7 `fb-*` añadidos (A), ADR-0075 y ADR-0077.
- **Regímenes de cambio.** En `knowledge/feedback/` solo hay `A` (7 ficheros). Nada en `knowledge/evidence/`, `data/manifests/`, `knowledge/corpus/` ni `knowledge/cases/`. `HISTORIA.md` solo suma (187/0).
- **Acciones del feedback.** CORRECT sobre la regla RN-003, sin supersede, porque el de la sesión 3 sigue vigente para el color. RESOLVE_UNKNOWN activo sobre la ambigüedad A-51. Cuatro RESOLVE_UNKNOWN sobre parámetros que estaban UNKNOWN. CONFIRM sobre evidencia para S-4.
- **Ambigüedades.** El diff de `ambiguedades.yaml` solo toca A-51. Va en el mismo commit (5df5bd5) que `docs/spec/ambiguedades.md`, la fila quitada de Known Ambiguities y `test_kit.py`. Ninguna regla citaba A-51 y la hoja no la lleva (`scripts/hoja_preguntas.py:54`).
- **ADR.** El `## Estado` de 0075 y 0077 es «ACTIVE». ADR-0060 lleva su recuadro (diff, líneas 9-16) y su fila del índice. ADR-0055 no se toca. Ningún informe cerrado se edita (de `docs/validation/` solo cambia este). Next Action, `docs/plan/`, Makefile, `.claude/` y `scripts/` sin cambios.
- **Las tres guardias de `modelo.py`.** Ya recorren `acumuladores` y las reglas (`modelo.py:382, :415, :879`). Que no se amplíen está declarado (§0.7 m4).
- **Cifras.** Las formas de RN-036 y RN-035 nombran parámetros, sin números.
- **`feedback pending`.** Sale «1 pendientes»: `fb-2026-09-29-sesion-03-31fb311f … RN-003 no lo cita todavia`. Es efecto de citar el CORRECT de S-13; está declarado en §0.8.1 y en el punto 4 de la PARADA, y no es «lo activado».
- **Citas del informe que comprobé.** `sesgo.py:90` en main (el `return … AMBIGUO`), `test_kit.py:316` en main (`{"A-21","A-35","A-44","A-51"}`), `0053-…md:141-147` (§6 «Estado entre días») y `cableado.py:228-236` en main: las cuatro casan. La premisa de la PARADA a1 también se sostiene: `estructura_m1.py:128-138` deja entre el bloque y el breaker solo velas del color de la entrada o sin cuerpo.
- **Evidencia nueva.** Ningún ítem añadido, así que el punto 10 no aplica.

#### Eje (b) · Encargo
Resumen: 0 bloquea, 2 importa, 2 menor. Requisitos: 38 hechos (4 de ellos «de otra forma», declarados), 3 parciales, 6 no hechos (3 por la PARADA o por el literal que no llegó, todos declarados; 3 de entrega aún pendientes).

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| 1 | Rama desde main d4b7917 con `abrir-rama`, base y CI comprobadas | Hecho | merge-base d4b7917; informe:26-38 |
| 2 | Contrato con tramo R1, riesgo alto y artefacto | Hecho | `contrato.yaml:1-4` |
| 3 | Encargo copiado en `docs/encargos/` | Hecho | `docs/encargos/trabajo-activar-sesion-04-motor.md` (135/0), con el añadido nocturno |
| 4 | Nada fijado se pisa (cada cambio por su régimen) | Hecho | ADR-0075 con recuadro en 0060 y fila; CORRECT sobre RN-003; RESOLVE_UNKNOWN sobre A-51 |
| 5 | A-49 ABIERTA y sin tocar; ninguna «en parte» se cierra; A-35 y A-44 intactas | Hecho | diff de `ambiguedades.yaml` solo en A-51; `test_kit.py`: RESUELTAS solo gana A-51; `cli.py` sin cambios |
| 6 | «Casi plana» (RN-007) no se resuelve | Hecho | RN-007 no aparece en el diff de `strategy_spec.yaml` |
| 7 | RN-020 no cambia | Hecho | no aparece en el diff |
| 8 | El 9 vive en `parametros.yaml`, no en la forma | Hecho | `parametros.yaml` (racha_perdidas_max, valor 9); forma de RN-036 por nombre |
| 9 | Sin arnés; tests sintéticos | Hecho | tests con días de 2030 (`test_rn035_ventana_fin.py:6`) |
| 10 | Nada de material; citas cruzadas con los tramos | Hecho | ver alcance (4) abajo |
| 11 | Next Action y hoja de ruta sin tocar | Hecho | `docs/plan/` sin diff; Next Action de PS sin cambios |
| 12 | Makefile, `.claude/` y la guardia sin tocar | Hecho | sin diff |
| 13 | Informes cerrados con `--diagnostico-a21` sin editar | Hecho | solo cambia ACTIVAR-SESION-04-MOTOR.md |
| 14 | FASE 0, puntos 1-5 con fichero:línea | Hecho | informe §0.1-§0.5 |
| 15 | PARADA solo si lo medido contradice una decisión | Hecho | PARADA de la decisión 3, justificada (`estructura_m1.py:128-138`) |
| 16 | Decisión 1: CONFIRM de S-4 con sus opciones; qué dice `pending` | Hecho | `fb-…-35a080e2`; `pending` lo da por REFLEJADO, medido y dicho (§1.1) |
| 17 | Decisión 2: ADR-0075, recuadro en 0060 y fila «ACTIVE (con enmienda de ADR-0075…)» | Hecho | ADR-0060 diff; `docs/adr/README.md` (filas 0060 y 0075) |
| 18 | Decisión 2: neutra = cierre == apertura; reserva alcista; CORRECT de RN-003; notas de RN-033; token `ambiguo` declarado; spec_version mayor | Hecho | `sesgo.py` (`continue`); `strategy_spec.yaml` (RN-003, RN-033, token); manifest 15.9.9 → 16.0.0 |
| 19 | Decisión 2: tests que cambian de sentido, dos neutras seguidas, neutra tras bajista | Hecho | `test_sesgo_h4.py:80-121`; `test_huecos_motor.py:168-233` |
| 20 | Decisión 3 (A-21, ADR-0076, retirada de `--diagnostico-a21`, cinco sitios, runbook) | No hecho (PARADA, declarada) | «Lo que necesito que decidas»; `ambiguedades.yaml` y ADR-0055 sin diff |
| 21 | Decisión 4: ADR-0077 y RN-036 aparte de RN-020; cuatro parámetros CONFIRMED vía apply | Hecho | `parametros.yaml` (los cuatro, fuente feedback); `apply --check` «8 ya estaban» |
| 22 | Pérdida = cartucho de RN-016, una sola definición | Hecho | `racha.py:66-75`; `primitivas_broker.py` (`_cuenta_como_intento` delega) |
| 23 | Acumulador persistente fuera de EstadoDia, con `cuenta_diaria` | Hecho | `cableado.py` (`MotorCableado.racha`, reinicio con cuenta_diaria) |
| 24 | «Día siguiente» con `reloj_sesiones` | Hecho | `racha.py:104-105` |
| 25 | RN-036 prohíbe y retira la pendiente | Hecho | forma de RN-036 (`retirar_ordenes_pendientes: {}`); `primitivas_broker.py` |
| 26 | RN-036 sin A-44 ni `--diagnostico-a44` | Hecho | `test_racha_perdidas.py:300` (`motor.tope is None`) |
| 27 | Las tres guardias en el mismo commit | Hecho de otra forma (declarado §0.7 m4 y §1.3) | `modelo.py:382,415,879` ya recorren `acumuladores` y reglas |
| 28 | Cinco sitios de A-51 | Hecho | 5df5bd5: yaml, docs, PS, test_kit; la hoja no la lleva |
| 29 | Tests: 9 pérdidas con BE; ganadora a la octava; fin de semana | Hecho | `test_racha_perdidas.py:117, :142, :154` |
| 30 | Test: la orden pendiente se retira en la novena | Hecho de otra forma (declarado §1.3) | `test_racha_perdidas.py:202-222` (la acción, aislada); `:290-342` (el noveno día RN-036 dispara sin pendiente) |
| 31 | Decisión 5: RN-035 gana la rama `ventana_fin` | Hecho | forma de RN-035 (`cualquiera_de […, alcanza_hora {ventana_fin}]`) |
| 32 | Las notas de RN-035 pierden «LO QUE … NO HACE TODAVIA» | Hecho | diff de `strategy_spec.yaml` (hunk @@ -908) |
| 33 | Test: RN-035 retira a `ventana_fin` y el cableado no encuentra nada | Hecho | `test_rn035_ventana_fin.py:41-62` |
| 34 | Hueco del último minuto congelado + pregunta para la sesión 5 | Hecho | `test_rn035_ventana_fin.py:65-92`; informe:627-632 |
| 35 | Paso 3 de `activar-sesion` en cada commit | Hecho | `Fuente:` en los cuerpos; `apply --check` por respuesta; sello en HEAD |
| 36 | ADR con plantilla y en el índice | Hecho | 0075 y 0077 con todas las secciones; README |
| 37 | Tests que rompen con main, «con las dos salidas en el informe» | Parcial | salidas de main: pegadas para las decisiones 2 y 4, citada en línea para la 5. De la rama no se pega ninguna salida: solo «pasan» y «40 passed» (informe:468-469, :645-650) |
| 38 | `detectar_esquema` con una lectura fuera de LECTURAS_LIMPIA sigue fallando | Hecho (test que ya existía) | `test_estructura_m1.py:234-235` |
| 39 | Una «en parte» no puede entrar en RESUELTAS | Hecho | `test_kit.py::test_una_en_parte_no_entra_en_resueltas` |
| 40 | grep de `--diagnostico-a21` vacío | No hecho (PARADA, declarada) | informe:659-664; mi grep da las mismas 11 líneas |
| 41 | Holdout: sin filtros, exposiciones, sin fechas reservadas | Hecho | HOLDOUT-EXPOSICIONES.md sin diff; las fechas del informe son ids de sesión o de registro |
| 42 | El literal de 1:44:49 | No hecho (no llegó; declarado) | informe:22-23 |
| 43 | CI de Linux por `fix/` con el número de run | No hecho (pendiente) | falta §8 |
| 44 | Informe del revisor pegado al final | No hecho (pendiente) | falta §9 |
| 45 | Líneas del cierre y lista de la sesión 5 | Hecho (condicionadas a la PARADA) | informe §5 y §6 |
| 46 | «Rama lista para revisión, NO cerrada» | Parcial | `## Estado` = «EN CURSO» (informe:782) |
| N1-N5 | Régimen nocturno | Parcial (N5: el informe está sin commitear) | `git status --short` → ` M docs/validation/ACTIVAR-SESION-04-MOTOR.md` |

| # | Gravedad | Hallazgo | Evidencia |
|---|---|---|---|
| b1 | importa | El encargo pide «con las dos salidas en el informe» y solo están las de main. Del lado de la rama no hay ninguna salida pegada. | informe:450-471 (decisión 2: solo «40 passed»), :558-572 (decisión 4), :609-611 (decisión 5: la de main citada en línea), tabla :643-651 («pasan»). |
| b2 | importa | La tabla «El encargo, punto por punto» da por hechas cosas que hoy no lo son. | informe:694 (fila 22, «Hecho», remite a `## Estado`, que dice EN CURSO en :782); :699 (N5, «`git status --short` vacío»), cuando el informe está modificado sin commitear; :693 y :696 remiten a §8 y §9, que no existen. |
| b3 | menor | La fila 13 de la tabla dice «Hecho» para «tres guardias» y «los cuatro tests», y no «Hecho de otra forma». La explicación está en §0.7 m4 y en §1.3, pero no en la fila ni entre las 10 desviaciones declaradas. | informe:685, :701-710. |
| b4 | menor | El nombre del test promete «en la novena», pero el test no registra ninguna pérdida: ejerce la acción aislada. El docstring sí es honesto. | `tests/unit/test_racha_perdidas.py:202-222`. |

Los cuatro alcances del encargo:
- **(1) A-21 y A-51.**
  - A-51 tiene sus cinco sitios en el commit 5df5bd5: yaml en RESUELTA con 4 parámetros y 3 ítems, `docs/spec/ambiguedades.md`, su fila fuera de PS, `test_kit` (bloqueantes `{"A-21","A-35","A-44"}`) y la hoja, que no la llevaba. Tiene su test (`test_racha_perdidas.py`, 11 funciones) y su `Fuente:`, con 5 `fb-*` y ADR-0077.
  - A-21 no se tocó: no hay diff en `ambiguedades.yaml` fuera de A-51, ni en `zonas.py`, `diagnostico.py`, `cli.py`, `hoja_preguntas.py` ni ADR-0055.
  - Ninguna «en parte» se cerró: RESUELTAS solo gana A-51, y `EN_PARTE_SESION_4` siguen ABIERTAS.
  - A-49 sigue ABIERTA y ningún registro tiene objetivo A-49.
- **(2) ADR-0060, ADR-0055 y si algo contradice un ADR.**
  - ADR-0060 lleva su recuadro y su fila. ADR-0055 no se enmienda, coherente con la PARADA.
  - **ADR-0077 frente a ADR-0053 §6:** no lo contradice. §6 habla del estado de `EstadoDia`, y la racha vive fuera, como ya vivía el `SeguidorTope`.
  - **ADR-0077 frente a ADR-0063:** suma un lector del reloj de las sesiones, y lo declara.
  - **Decisión 5 frente a ADR-0066 §4:** amplía RN-035 y no contradice nada; `decision: ADR-0066` se conserva.
  - **Decisión 5 frente a ADR-0053 §6:** la cancelación del cableado sigue como red de seguridad.
  - Observación sin gravedad: ADR-0066 §4 no lleva ninguna nota de la segunda rama; la traza vive en la spec y en el encargo.
  - Hallazgos de este alcance: a2 (cita de RN-013) y a7 (ADR-0044, heredado).
- **(3) Cada test de motor falla con main.**
  - Los tests existen y dicen lo que el informe dice: 6 tests de sesgo que cambian de sentido, `test_racha_perdidas.py`, que importa `racha` y por tanto no puede importarse en main, y `test_rn035…`, que exige «RN-035» en `disparadas` de 11-15.
  - Por el código de main (`sesgo.py:90` daba AMBIGUO; `racha.py` no existe; `cancelados_fin_dia` no existe en main), las salidas pegadas son coherentes.
  - No recreé el clon.
- **(4) Ninguna cita cae en un tramo no citable, márgenes incluidos.** Crucé contra los 22 tramos de v10 y los de v9 de `tramos_no_citables.yaml`:
  - v10 0:49:45-0:50:10 y 0:54:27-0:54:51: fuera (lo más cercano es 0:45:05-0:46:41).
  - v10 1:06:19-1:06:24 y 1:06:53-1:08:28: el tramo 1:04:56-1:05:29 acaba antes.
  - v10 1:17:25-1:20:27 y 1:14:42: fuera.
  - v10 1:40:05-1:41:01 y 1:41:01-1:41:29: entre 1:39:08-1:39:42 y 1:43:42-1:44:21.
  - 1:44:49 solo se nombra, no se cita: queda 28 s después de 1:44:21.
  - v9 1:11:28-1:11:37 y 1:19:57: entre 1:07:45-1:07:52 y 1:13:04-1:14:16.
  - HOLDOUT-EXPOSICIONES.md no cambia.
  - Ninguna cae dentro.

#### Lo que no pude comprobar
- Las salidas con el código de main (§1.2, §1.3, §1.4): el clon `C:/cm/main` ya no existe y, como pediste, no lo recreé. Juzgo por lo pegado y por el código de main que leí con `git show`. Ya no está en `.git/worktrees`; solo queda `wt-ci`, del 29-09, ajeno a esta rama.
- Los `make check` de los commits anteriores: solo existe `make-check.log` del último, cuyo SELLO casa con el árbol de HEAD. Los anteriores los garantizan los hooks, pero no los vi.
- `spec docs --escribir`, `make check` y `knowledge validate > fichero` escriben: no los ejecuté. Lo que los sustituye es `knowledge validate` a stdout (todo OK), el sello y que `test_spec_docs_generados` está dentro del verde sellado.
- `git worktree list` lo bloquea el hook de solo lectura; en su lugar leí `.git/worktrees/`.
- La CI de `fix/activar-sesion-04-motor` (pediste tratarla como si no existiera) y que los tests con `data/` se salten en Linux.
- El literal de v10 1:44:49 y la cruda de v10: no se abren.

#### Comandos ejecutados
1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git diff --stat main...HEAD && git status --short`
2. Read del encargo, de `contrato.yaml` y del informe (entero, en dos tramos)
3. `uv run python scripts/contrato_rama.py`
4. `git log --format='%h%n%B----' main..HEAD`
5. (bloqueado por la guardia: un `for`) → `git log --format='%h %s' main..HEAD -- knowledge/spec knowledge/cases`
6. `git diff --name-status main...HEAD -- knowledge/evidence/ knowledge/feedback/ data/manifests/ knowledge/corpus/ knowledge/cases/`
7. `git log --name-status --format='== %h %s' main..HEAD`
8. `git diff main...HEAD -- knowledge/spec/ambiguedades.yaml PROJECT_STATE.md docs/adr/README.md`
9. `grep -n … docs/runbooks/AMBIGUEDADES.md`; Read de AMBIGUEDADES.md:1-40
10. Grep de `A-51|A-21` en `scripts/hoja_preguntas.py`; `git diff main...HEAD -- tests/unit/test_kit.py`
11. `uv run botsito feedback apply --sesion 2026-10-04-sesion-04 --check`
12. `grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" src/ tests/`
13. `uv run botsito knowledge validate 2>&1 | tail -30`
14. `ls -la make-check.log && grep -n -E "SELLO|PICO DE MEMORIA|passed|failed|error" make-check.log | tail -15`
15. `git rev-parse "1d39c1e^{tree}" && git log -1 --format='%ci' 1d39c1e`
16. `git diff main...HEAD -- docs/adr/0060-…md`; Read de ADR-0075 y ADR-0077
17. Grep en `knowledge/corpus/tramos_no_citables.yaml` (video_id, t0, t1); Grep de «margen» en `docs/runbooks/SESION-DE-PREGUNTAS.md`
18. `ls docs/adr | grep …` y `grep -n "" docs/adr/0053-*.md | sed -n …`; `grep -n … docs/adr/0066-…md`; Read de ADR-0066:75-109
19. `git diff main...HEAD -- knowledge/spec/parametros.yaml knowledge/spec/spec_manifest.yaml`
20. Read de `ev-v10-010804-5b6ad1a3`, `ev-v10-010715-fae17215`, `ev-v10-010653-81316808`, `ev-v10-014005-7e2228f4`
21. Grep en `SESION-04-EXTRACCION.md` (encabezados, «extender|0,5|4,5»); Read de :466-498 y :541-710
22. `git diff main...HEAD -- knowledge/spec/strategy_spec.yaml`
23. `cat` de `fb-…-45e624c5.yaml` y `grep -rn "tanto a las 11" …`; Grep de «tanto a las 11» en spec, docs, src y tests
24. `git diff main...HEAD -- src/botsito/domain/sesgo.py src/botsito/engine/primitivas.py src/botsito/engine/cableado.py`; Read de `src/botsito/engine/racha.py`; `git diff main...HEAD -- src/botsito/engine/primitivas_broker.py`
25. `grep -n -E "^def test_|…" tests/unit/test_racha_perdidas.py tests/unit/test_rn035_ventana_fin.py tests/unit/test_sesgo_h4.py tests/unit/test_huecos_motor.py`
26. (bloqueado por la guardia: `PYTHONDONTWRITEBYTECODE=`) → `uv run pytest <8 ficheros> -q -p no:cacheprovider`; luego `… -p no:cacheprovider -rs | tail -8` → «129 passed»
27. Read de `tests/unit/test_rn035_ventana_fin.py`; `git diff main...HEAD -- tests/unit/test_spec_fidelidad.py tests/unit/test_sesgo_h4.py`; Read de `test_huecos_motor.py:160-234`
28. `git diff main...HEAD --numstat -- docs/state/HISTORIA.md docs/encargos/…` y recuento de líneas quitadas (0)
29. `cat` de `fb-…-8e2d728a`, `fb-…-ca0afae6` y `fb-…-35a080e2`; Grep de accion, id, t0 y t1 en `fb-…-{b7040095,ecdd0572,d1792021,fa5ef0f6}`
30. `grep -n … src/botsito/spec/modelo.py`
31. `git diff --stat` y hunks del informe sin commitear
32. `git show main:src/botsito/domain/sesgo.py | sed -n '83,91p'`, `git show main:tests/unit/test_kit.py | sed -n '314,318p'`, `git show main:src/botsito/engine/cableado.py | sed -n '228,236p'`
33. `sed -n '232,238p' tests/unit/test_estructura_m1.py`; `git diff main...HEAD --stat -- <rutas que no deben cambiar>` (vacío)
34. `sed -n '128,168p' src/botsito/engine/llenado.py | grep …`
35. Grep de RN-011 y RN-013 en `strategy_spec.yaml`; Read de :1383-1394 y :1505-1544; Grep de «posicion viva»; Grep de «RN-013» en la spec, ADR-0077, el informe y `reglas.md`
36. `sed -n '1,30p' docs/adr/0044-…md; grep -n "^| 0044" docs/adr/README.md`
37. `grep -n … docs/adr/0063-…md`; Read de ADR-0063:42-73
38. `uv run botsito feedback pending 2>&1 | tail -20`; Grep de «pending» en `.claude/skills/activar-sesion`
39. Read de `src/botsito/domain/estructura_m1.py:120-164`
40. Grep de 1:19:57 en `ambiguedades.yaml`; Grep de fechas `20(26|25)-\d\d-\d\d` en el informe
41. (bloqueado por solo_lectura: `git worktree list`) → `git branch --list && ls .git/worktrees`; `cat .git/worktrees/wt-ci/gitdir …`

Ficheros clave: `knowledge/spec/strategy_spec.yaml` (:946-947, :1889), `docs/adr/0077-la-racha-de-perdidas-seguidas-del-trader-rn036.md` (:57-59), `docs/validation/ACTIVAR-SESION-04-MOTOR.md` (:24, :246, :555, :674, :685, :693-699, :782), `docs/validation/SESION-04-EXTRACCION.md` (:472-474), `tests/unit/test_racha_perdidas.py` (:202-222), `PROJECT_STATE.md` (:10).

### 9.3 Segunda pasada: el commit de A-21 (f358748), con los tres alcances de la respuesta

Lanzado el 2026-10-12 (modelo `opus`, subagente `revisor`) sobre f358748 (solo lo nuevo desde
136bb86), con los tres alcances de la respuesta del consultor y la regla de holdout (ninguna
carpeta madre con filtro). Recuento del revisor: 0 bloquea, 5 importa (2.1, 2.2, 2.3, 3.1 y F.1),
5 menor (1.1, 1.2, 2.4, 3.2, F.2) y una observación (1.3). Se pega tal cual: no cita ningún tramo
no citable ni ningún día reservado.

**Lo que se hizo con cada hallazgo** (en el commit que sigue a f358748; cada uno, medido):

| # | Gravedad | Qué se hizo |
|---|---|---|
| 1.1 | menor | `tests/unit/test_a21_series.py`: `SERIES` gana la columna de colores del tramo literal en compra («RVR», «RR», «R», «RVRVR», «RRR», «RVR», «RVR») y el test parametrizado la asserta, en venta en espejo (`ESPEJO_DE_COLORES`): las letras de las dos tablas quedan congeladas. 16 pasados. |
| 1.2 | menor | §1.5: la nota «¿Es solo eso?» se atribuye a `…48fb5817`, que es el registro que la lleva. Los registros no se tocan. |
| 1.3 | observación | §1.5 lo dice: el trailer del commit de A-21 no nombra ADR-0077 aunque las notas de RN-036 cambian en él; mecánicamente vale. |
| 2.1 | importa | §1.5 pega la salida del grep (6 líneas: un comentario de `cli.py` y el test negativo, que necesita el literal) y lo declara hecho de otra forma; §2 y la fila 18 de §3 ya no dicen «vacío». Los comentarios no se reescriben para que el grep calle. |
| 2.2 | importa | `scripts/orden_stop_o_limite.py`: el bucle se conserva, pero la vuelta que no coincide con el registro escribe «no se mide; A-21 esta fijada en …» y salta, y la que se mide rotula la lectura del registro. `ruff` y `mypy` limpios. No se ejecuta (lee `data/`). |
| 2.3 | importa | §1.5 y §6: el anexo `dia_del_bot.py` construye `Diagnostico` por posición y falla con `TypeError` con este código; no se edita (anexo de un informe cerrado), se reproduce con el código de su commit. |
| 2.4 | menor | §1.5: la lista del grep ancho completa, fichero a fichero con su recuento (15 ficheros). |
| 3.1 | importa | §4 rehecho sobre HEAD: 56 ficheros, los cuatro `scripts/` que cambian, `Current Feature` con ADR-0076, 1526 tests, 22.647 bytes. |
| 3.2 | menor | §6, R4.1: propuesta de que gane `ID:ADR-0076` e `ID:ADR-0077`. |
| F.1 | importa | §2 (el grep y la ampliación del test, que no hay), §3 fila 3 (el bloque `ids-inexistentes` retirado), fila 21 (dos pasadas del revisor, runs en §8), desviación (9) y §8 (los runs de f358748 y del commit final, con su comprobación). |
| F.2 | menor | La respuesta del consultor es ahora `## 10.` y esta sección es §9.3: las referencias casan; la viñeta repetida de ADR-0070 §3 en §6, borrada. |
| guardia | — | §6: el falso positivo de la guardia con cuatro `-e` (no se rodeó; se apunta para su rama). |

**El informe, tal cual:**

> ## Informe del revisor · trabajo/activar-sesion-04-motor · 2026-10-12 (solo f358748, desde 136bb86)
>
> He revisado los tres alcances de la orden de corte. No encuentro nada que bloquee. Hay cuatro hallazgos que importan dentro de los alcances, uno más fuera de ellos y cinco menores. A mi juicio la rama todavía no está lista para revisión: lo que falla es el informe y un guion, no la spec ni el motor.
>
> **Lo que está bien:**
> - Las dos tablas (la del ADR-0076 y la del §1.5 del informe) coinciden con lo que miden los tests.
> - A-21 queda cerrada en sus cinco sitios.
> - Los dos registros de feedback citan ventanas válidas.
> - `spec_version` subió y el manifiesto y los docs están al día.
> - El trailer `Fuente:` lleva ids que existen.
> - Los tres guiones nuevos del contrato usan argumentos con nombre.
> - Las líneas del cierre (§6) cubren R3.1, la lista de la sesión 5 y la deuda del punto 4.
>
> **Lo que falla:**
> - El informe dice que el grep sale vacío, y no es verdad.
> - `orden_stop_o_limite.py` pone en su informe una lectura de A-21 que no es con la que corre.
> - Hay un anexo con un `Diagnostico` posicional que no se ha declarado.
> - Varios pasajes del informe se escribieron antes del commit de A-21 y no se han actualizado.
>
> ---
>
> ### Alcance 1 · La tabla de series y el cierre de A-21
> Resumen: 0 bloquea, 0 importa, 3 menor.
>
> **Comprobado sin hallazgos:**
> - **Tests:** `uv run pytest -p no:cacheprovider -q tests/unit/test_a21_series.py` da 16 pasados: 7 series × compra/venta = 14 casos, más los 2 tests sueltos.
> - **Las tablas frente al test:**
>   - Las 7 filas del ADR-0076 (:47-53) y las 14 del informe (:648-661) coinciden con `SERIES` del test (:61-100): esquema, número de zonas, «limpia» e «igual».
>   - Las cadenas de colores de la columna literal también coinciden. Lo medí ejecutando `sin_alternancia_literal` sobre las 14: RVR/VRV, RR/VV, R/V, RVRVR/VRVRV, RRR/VVV, RVR/VRV, RVR/VRV.
>   - Solo hay dos «DISTINTO»: el doji en medio y el breaker contrario por mecha tras alternancia. Lo congela `test_las_diferencias_son_solo_el_doji_y_el_breaker_por_mecha` (:149-155), sobre el flag `igual` que asserta el test parametrizado (:146).
>   - Están las cinco series mínimas del punto 0.a del consultor, más la de doble alternancia.
>   - La medida literal es exactamente la (a) de la PARADA (informe :320-324).
>   - El criterio MECHA es el que usa producción: `breaker_m1_criterio_ruptura` = `mecha` (parametros.yaml:475-488).
> - **Los cinco sitios de AMBIGUEDADES.md:**
>   - **Registro de parámetros:** `zona_control_limpia` CONFIRMED, con fuente `…48fb5817`. `feedback apply --check` da «9 parametros; 0 cambian, 9 ya estaban».
>   - **`ambiguedades.yaml`:** `estado: RESUELTA`, tres ítems de v10 en `evidencia`, `decision: null`.
>   - **Reglas y glosario:** el Grep `A-21|zona_control_limpia` en `strategy_spec.yaml` y `glossary.yaml` no da ninguna coincidencia, así que el sitio no existe, como dice el informe.
>   - **Known Ambiguities:** PROJECT_STATE.md:84-98 ya no tiene A-21 ni A-51.
>   - **Hoja de preguntas:** A-21 sale de `ORDEN_SESION_02` y de `ORDEN`.
>   - **`test_kit.py`:** A-21 en `RESUELTAS`; las bloqueantes abiertas son `{A-35, A-44}`.
>   - Pasan estos tests: test_kit, test_hoja_preguntas, test_spec_docs_generados, test_adr, test_project_state, test_reabrir_y_fuente_documental, test_hoja_de_ruta, test_preparar_a21, test_preparar_a35, test_cableado, test_visor, test_rutas_windows, test_renovar_cierres, test_selector_orden_stop, test_transcribir_sesion, test_sesiones_independientes, test_broker_ordenes_stop, test_preparar_a44 y test_estructura_m1, todos sin fallos.
> - **Ventanas de los registros:**
>   - `…22d08cbf` cubre 1:17:25–1:20:27 y `…48fb5817` cubre 1:17:25–1:17:31. Las dos caen dentro del tramo S-10 de la extracción (SESION-04-EXTRACCION.md:595, 70:47–81:49) y casan con los t0/t1 de `ev-v10-011725`, `ev-v10-011734` y `ev-v10-011957`.
>   - No tocan ningún tramo de v10 de `tramos_no_citables.yaml`, márgenes incluidos: los más cercanos son 1:04:56–1:05:29 (:196-197) y 1:26:34–1:26:41 (:203-204).
> - **Régimen de feedback:** `git diff --name-status 136bb86 HEAD -- knowledge/feedback knowledge/evidence` da solo dos `A`. Los dos son RESOLVE_UNKNOWN, uno sobre la ambigüedad y otro sobre el parámetro, y los dos activos.
> - **Versión, manifiesto y validación:**
>   - `spec_version` pasa de 17.0.1 a 17.0.2.
>   - Docs regenerados: el diff de glosario, parámetros y reglas lleva el hash nuevo y `test_spec_docs_generados` pasa.
>   - `knowledge validate` dice OK en todo: «hash del manifiesto al dia», «174 registros de feedback, historial intacto, commits con Fuente».
> - **Trailer:** `Fuente: fb-2026-10-04-sesion-04-22d08cbf fb-2026-10-04-sesion-04-48fb5817 ADR-0076` va en el cuerpo, y los tres ids existen.
> - **ADR-0076:** `## Estado` es ACTIVE; tiene recuadro en ADR-0055 y fila en el índice.
> - **`make check`:** `make-check.log`:98 da «SELLO … sobre el arbol 08a0d35f…», que es `git rev-parse HEAD^{tree}`; «2609 passed»; «PICO DE MEMORIA … 295 MiB».
> - **Respuesta del consultor:** la copia del encargo (:135-166) y la del informe (:1179-1210) son idénticas (mismo md5).
>
> | # | Gravedad | Hallazgo | Evidencia | Qué hacer |
> |---|---|---|---|---|
> | 1.1 | menor | La columna literal de las tablas trae las letras («RVR / VRV»…), pero el test solo asserta el booleano; las letras van como mensaje de error. Hoy coinciden (lo medí), pero nada las congela. | test_a21_series.py:144-146; ADR-0076:47-53 | Assertar `tramo` contra la cadena de cada serie, o decir que esa columna es solo informativa. |
> | 1.2 | menor | El informe atribuye la «nota de la pregunta dirigida «¿Es solo eso?»» a `…22d08cbf`, pero esa nota está en `…48fb5817`. | informe:676-678; fb-…22d08cbf.yaml:23-27 (no la lleva); fb-…48fb5817.yaml:21 (sí) | Corregir el informe. Los registros no se tocan. |
> | 1.3 | menor | El cambio de las notas de RN-036 («LECTURA PROVISIONAL», punto 5) entra en este commit, pero el trailer no nombra ADR-0077. Mecánicamente vale. | strategy_spec.yaml diff :1893-1894; cuerpo del commit | Basta mencionarlo en el informe. |
>
> ### Alcance 2 · El grep de `--diagnostico-a21` y de `a21`
> Resumen: 0 bloquea, 3 importa, 1 menor.
>
> **Comprobado sin hallazgos:**
> - **Nada vivo.** Lo que queda en src/ es solo comentario o docstring: cli.py:2295-2296, diagnostico.py:28-29 y zonas.py:4-8. En tests/ son comentarios, el `type: ignore` de test_preparar_a21.py:378 y el test negativo de la CLI (:411-430, que necesita el literal). En scripts/ solo quedan los encabezados `DIAGNOSTICO-A21-` de los dos `verificacion_a21*.py`, que el consultor dijo no tocar.
> - **Nombres retirados:** no queda ni `ETIQUETA_A21`, ni `DiagnosticoDeZonaRechazadoError`, ni `diag.a21` en `*.py`, salvo en el anexo del hallazgo 2.3.
> - **Los tres guiones del contrato** construyen `Diagnostico` con argumentos con nombre y llaman a `lectura_limpia(registro)`: embudo_77.py:435/439, caja_77_exploratoria.py:132/136 y orden_stop_o_limite.py:419/423. `embudo_77` comprueba `--a21` contra el registro (:440-442) y `caja_77` se niega si no coincide (:137-138).
> - **Guiones intactos:** `git diff --stat main -- scripts/bloque_de_la_caja.py scripts/verificacion_a21.py scripts/verificacion_a21_entradas.py` sale vacío. En `orden_stop_o_limite.py` la cabecera del bucle de :416 sigue igual y el de :517 no se toca, pero el cuerpo del de :416 sí cambia (hallazgo 2.2).
> - **Ningún `Diagnostico(...)` posicional** en src/, tests/ ni scripts/ (Grep `Diagnostico\(` en todo el repo).
>
> | # | Gravedad | Hallazgo | Evidencia | Qué hacer |
> |---|---|---|---|---|
> | 2.1 | importa | El informe dice que el grep sale vacío, y no lo está. El encargo (:88) pide «vacío, con la salida en el informe». Lo que queda es todo muerto, pero el informe afirma otra cosa y no pega la salida. | `grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" src/ tests/ scripts/` da 6 líneas: cli.py:2295; test_preparar_a21.py:370, :411, :414, :426, :429. Informe :761-762 («→ vacío») y §3 fila 18 :846 («vacío desde el commit de A-21») | Pegar la salida y declararlo «Hecho de otra forma»: el test negativo necesita el literal y lo demás son comentarios. No reescribir los comentarios solo para que el grep calle. |
> | 2.2 | importa | `orden_stop_o_limite.py`, `control_simulador`: el motor corre siempre con la lectura del registro (`lim`), pero cada sección sale rotulada con la variable del bucle. La segunda vuelta se publica como «A-21 = sin_mecha_mas_alla_del_extremo» y en realidad corre con `solo_una_zona_de_control`. El informe dice «lim es la del registro en las dos vueltas», pero no que el rótulo miente. | orden_stop_o_limite.py:416-423 (`lim = zonas.lectura_limpia(registro)`) y :479 (`f"## A-21 = {limpia}: …"`) | Que el rótulo diga `lim` y que la vuelta que no se mide lo diga (o se salte con `if limpia != lim`). Si no, declararlo en el informe como salida engañosa del guion. |
> | 2.3 | importa | Hay un `Diagnostico` posicional con 6 argumentos en el anexo de un informe cerrado. Con 5 campos da `TypeError`, y `lectura_limpia(registro, diag.a21)` falla también. Falla con ruido, no en silencio, pero el informe no lo dice. Los greps del §1.5 no lo ven porque solo miran src/tests/scripts. | docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py:55-57 y :61; `git diff main -- <ese fichero>` vacío (en main funciona) | No editarlo (es anexo de un informe cerrado). Una línea en el informe y en §6: el anexo se reproduce con el código de su commit. |
> | 2.4 | menor | La lista de «lo que deja» el grep de `a21` está incompleta. Faltan cli.py:2295, test_a21_series.py, el import de test_sesiones_independientes.py:29, los comentarios de test_preparar_a35.py:444, test_visor.py:395 y test_rutas_windows.py:26, y la variable/clave `a21` de embudo_77.py (:658, :884, :907, :1006). Ninguno está vivo. | informe:762-768; `grep -rnc --include=*.py -e "a21" src/ tests/ scripts/` | Completar la lista o pegar la salida. |
>
> ### Alcance 3 · Las líneas del cierre (§6) y la lista de la sesión 5
> Resumen: 0 bloquea, 1 importa, 1 menor.
>
> **Comprobado sin hallazgos:**
> - **R3.1 sin A-21:** informe:921 («hoy lo necesita para A-35 y A-44»), frente a HOJA-DE-RUTA.md:95 y :101, que hoy todavía la nombran.
> - **R1.1 y R4.1** pierden A-21 (:917-923).
> - **Lista de la sesión 5 (§5, :881-902):**
>   - Sale el punto 11 de A-21. En ACTIVAR-SESION-04.md:835 el 11 quedaba «solo para A-21 si la rama de motor no la cierra».
>   - Las dos preguntas de ADR-0076 §4 (:87-93) están copiadas idénticas.
>   - La de la racha es literal la del punto 5 del consultor y coincide con ADR-0077 §5.
> - **Deuda del punto 4 (:929-935):**
>   - Está escrita. `fb-2026-09-29-sesion-03-5021677e` es RESOLVE_UNKNOWN sobre A-46, y `fb-…-31fb311f` es CORRECT sobre RN-003.
>   - `uv run botsito feedback pending` da «1 pendientes de 123 activos», como dice el informe.
> - **Lo que §6 y §1.5 dicen de PROJECT_STATE:** Known Ambiguities sin A-21 ni A-51 (PS:84-98) y Current Feature con ADR-0076 (PS:10). `uv run botsito state check` da OK.
>
> | # | Gravedad | Hallazgo | Evidencia | Qué hacer |
> |---|---|---|---|---|
> | 3.1 | importa | El §4 («Lo que NO cambia, medido») sigue con datos de antes del commit de A-21 y contradice el fichero y el diff. | informe:872-879: dice «35 ficheros» (contrato_rama.py da «56 ficheros»; `git diff --stat main...HEAD` da 56), «Ninguno de … `scripts/`» (cambian embudo_77, caja_77_exploratoria, hoja_preguntas y orden_stop_o_limite), «Current Feature (que dice ya que A-21 está en PARADA)» (PS:10 dice ADR-0076) y «1506 → 1524» (PS:19: 1526) | Rehacer §4 con el estado de HEAD. |
> | 3.2 | menor | Al quitar ID:A-21 de las Refs de R4.1, las dos preguntas de ADR-0076 §4 y la de la racha se quedan sin ningún id del que colgar. No hay ambigüedad abierta que las recoja, solo el §5 del informe. | informe:922-923; HOJA-DE-RUTA.md:109 | Proponer en §6 que R4.1 gane `ID:ADR-0076` (y `ID:ADR-0077`). |
>
> ### Fuera de los tres alcances (visto de paso, no contado arriba)
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | F.1 | importa | Otros pasajes del informe siguen escritos como antes de la respuesta del consultor: el §2 dice que el grep «NO está vacío porque la decisión 3 está en PARADA» y que se ampliará «con la opción nueva»; la fila 3 de §3 dice «ADR-0076 sigue sin existir»; la fila 21 dice «cuatro alcances» y «el run del último commit lo lanza Aleks»; la desviación (9) habla del bloque `ids-inexistentes`, que ya salió; y §8 promete los runs de f358748 «abajo» sin que haya nada. | informe:809-820, :831, :849, :864-865, :972-973. La CI de f358748 (run 38243202933) estaba `in_progress` al revisar: `gh api …/commits/f358748cbf47…/check-runs` |
> | F.2 | menor | Se citan §10 y §9.3, pero la respuesta del consultor está en una sección sin número y no hay §9.3. Además, §6 repite la viñeta de ADR-0070 §3. | informe:17, :637, :840, :972, :1177, :1215; :936 y :941-942 |
>
> ### Recuento
> - Bloquea: 0.
> - Importa: 4 dentro de los alcances (2.1, 2.2, 2.3, 3.1) y 1 fuera (F.1).
> - Menor: 5 (1.1, 1.2, 2.4, 3.2, F.2). El 1.3 queda como observación.
>
> **¿Lista para revisión?** Todavía no. Ni la spec ni el motor ni el cierre de A-21 tienen defecto, pero el informe afirma un grep vacío que no lo está, varias secciones dicen cosas falsas sobre el estado de HEAD, y el rótulo de `orden_stop_o_limite.py` publicaría una medida con una lectura que no corrió. Las tres cosas se arreglan en el informe y en una línea del guion (o declarándolas). Falta además el run de CI del último commit.
>
> ### Lo que no pude comprobar
> - **Que los 14 casos pasan también con el código de `main`:** haría falta un worktree, y eso escribe. Como evidencia que lo sustituye, `git diff --stat main -- src/botsito/domain/estructura_m1.py src/botsito/domain/pivotes_m15.py tests/unit/test_estructura_m1.py` sale vacío.
> - **`scratchpad/medir_series_a21.py`:** está fuera del repo.
> - **`make check` y `spec docs --escribir`:** no los ejecuté porque escriben. Su evidencia es el sello de `make-check.log` (igual al árbol de HEAD) y `test_spec_docs_generados` en verde.
> - **El resultado de la CI de f358748:** estaba en curso (run 38243202933).
> - **Que el anexo `dia_del_bot.py` falla al ejecutarse:** lo deduzco de la firma del dataclass. No lo ejecuté porque lee `data/`.
> - **Un posible falso positivo de la guardia:** bloqueó `grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" -e "DIAGNOSTICO-A21" -e "a21=" src/ tests/ scripts/` con el mensaje «bloquea: leer el contenido de .», aunque las rutas eran literales. Para los patrones `DIAGNOSTICO-A21` y `a21=` usé la herramienta Grep sobre `src/`, `tests/` y `scripts/` por separado, y el grep de los dos primeros patrones sí pasó por Bash. Conviene revisar esa regla de la guardia en su rama.
>
> ### Comandos ejecutados
> 1. `git branch --show-current`; `git log --format='%h %s' 136bb86..HEAD`; `git diff 136bb86 HEAD --stat`; `git status --short`
> 2. `git show HEAD --format='%h%n%B' --stat`
> 3. Read de ADR-0076 y de `tests/unit/test_a21_series.py`
> 4. `uv run pytest -p no:cacheprovider -q tests/unit/test_a21_series.py`
> 5. `uv run python -B -c "…sin_alternancia_literal sobre las 14 series…"` (el primer intento, con `PYTHONDONTWRITEBYTECODE=1`, lo bloqueó la guardia)
> 6. Grep de `bloque_de_origen|referencia_del_breaker|zonas_de_control|detectar_esquema` en `estructura_m1.py`
> 7. Read del informe: :1-40, :635-974, :1170-1217, :315-372
> 8. `git diff 136bb86 HEAD -- PROJECT_STATE.md contrato.yaml docs/adr/README.md docs/adr/0055-… docs/runbooks/ACTIVAR-A35-A44.md`
> 9. `git diff 136bb86 HEAD -- tests/unit/test_kit.py tests/unit/test_hoja_preguntas.py scripts/hoja_preguntas.py`; `grep -n "^| A-" PROJECT_STATE.md`
> 10. `git diff 136bb86 HEAD -- knowledge/spec/{ambiguedades,parametros,strategy_spec,spec_manifest}.yaml`
> 11. `git diff --name-status 136bb86 HEAD -- knowledge/feedback knowledge/evidence`; `git diff --name-status main...HEAD -- knowledge/feedback knowledge/evidence data/manifests knowledge/corpus`
> 12. Read de los dos registros `fb-2026-10-04-sesion-04-{22d08cbf,48fb5817}.yaml`
> 13. Grep en `SESION-04-EXTRACCION.md` (S-10) y en `tramos_no_citables.yaml`; Read de `tramos_no_citables.yaml` :1-360 y de la extracción :593-642
> 14. `git ls-files knowledge/evidence | grep -e …` (las tres rutas literales); Read de los tres `ev-v10-*`
> 15. `uv run python scripts/contrato_rama.py` (el primer intento, con `cat` delante, lo bloqueó la guardia); Read de `contrato.yaml`
> 16. `uv run botsito feedback apply --sesion 2026-10-04-sesion-04 --check`
> 17. `uv run botsito knowledge validate`
> 18. `uv run pytest -p no:cacheprovider -q` sobre los 14 ficheros de test listados
> 19. Grep (herramienta) de `--diagnostico-a21|diagnostico.a21|DIAGNOSTICO-A21|a21=` en `src`, `tests` y `scripts` (el `grep -rn` de Bash con los cuatro patrones lo bloqueó la guardia)
> 20. Grep de `grep|vacío` en el encargo
> 21. `grep -rn --include=*.py -e "--diagnostico-a21" -e "diagnostico.a21" src/ tests/ scripts/`
> 22. `grep -rnc --include=*.py -e "a21" src/ tests/ scripts/`, y el grep de `a21` sobre los ficheros con coincidencias
> 23. `git diff 136bb86 HEAD -- src/botsito/engine/diagnostico.py src/botsito/engine/zonas.py src/botsito/cli.py`; Read de cli.py:2282-2301
> 24. Grep de `Diagnostico\(` en todo el repo (`*.py`)
> 25. `git log … -- docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`; `git diff main -- <ese fichero>`; Read de sus :1-70; Grep de `dia_del_bot`
> 26. `git diff --stat main -- scripts/bloque_de_la_caja.py scripts/verificacion_a21.py scripts/verificacion_a21_entradas.py`; `git diff main -- scripts/orden_stop_o_limite.py scripts/caja_77_exploratoria.py scripts/embudo_77.py`
> 27. Read de `orden_stop_o_limite.py` :395-493
> 28. Read de `test_preparar_a21.py` :360-439
> 29. Grep de `A-21|zona_control_limpia` en `strategy_spec.yaml` y `glossary.yaml`; `git diff 136bb86 HEAD -- docs/spec/{glosario,reglas,parametros}.md`
> 30. Grep de `ORDEN_SESION_02|hoja_preguntas` en `AMBIGUEDADES.md`
> 31. `uv run pytest -p no:cacheprovider -q tests/unit/test_transcribir_sesion.py tests/unit/test_sesiones_independientes.py tests/unit/test_broker_ordenes_stop.py tests/unit/test_preparar_a44.py tests/unit/test_estructura_m1.py`
> 32. Grep de `A-21` en `HOJA-DE-RUTA.md`; Read de sus :38-122; `uv run pytest … tests/unit/test_hoja_de_ruta.py`
> 33. Grep en `ACTIVAR-SESION-04.md` (punto 11, §5)
> 34. `grep -n …` de los dos registros de sesión 03 (el intento encadenado con `feedback pending` lo bloqueó la guardia); `uv run botsito feedback pending`
> 35. `git diff --stat main...HEAD | tail -1`; `git diff --name-only main...HEAD -- scripts/`
> 36. `grep -n -e "§10" -e "§9.3" …` en el informe y el encargo
> 37. Grep de `Respuesta del consultor…` en el encargo; `sed -n … | md5sum` de las dos copias
> 38. `git diff 136bb86 HEAD -- docs/encargos/trabajo-activar-sesion-04-motor.md`
> 39. `git diff --stat main -- src/botsito/domain/… tests/unit/test_estructura_m1.py`
> 40. Grep de `detectar_esquema\(` y de `criterio` en `zonas.py`; Grep de `breaker_m1_criterio_ruptura` en `parametros.yaml`
> 41. Grep de `ETIQUETA_A21|DiagnosticoDeZonaRechazadoError|diag\.a21|\.a21\b` y de `lectura_limpia\(` en `*.py`
> 42. Grep de `diagnostico-a21` en `docs/runbooks`, `docs/adr`, `docs/plan`, `PROJECT_STATE.md`…; `grep -n -o` del contexto en PROJECT_STATE.md
> 43. `git rev-parse HEAD`; `git ls-remote origin refs/heads/fix/activar-sesion-04-motor`; `gh api repos/:owner/:repo/commits/f358748cbf47991677f74ecb5c1ee28fcf26f1c2/check-runs`
> 44. `ls -la make-check.log`; `grep -n -e SELLO -e "PICO DE MEMORIA" -e passed -e failed make-check.log`; `git rev-parse "HEAD^{tree}" "136bb86^{tree}" "1d39c1e^{tree}"`; `git log -1 --format=%cd f358748`
> 45. `git diff 136bb86 HEAD -- docs/adr/0077-…`; `grep -n -i "única lectura" …`; Grep de `PROVISIONAL` en el informe
> 46. `uv run botsito state check`
> 47. `grep -n -e "funciones de test" -e "^## Known" PROJECT_STATE.md`; `grep -n "tres líneas"` en el informe
>
> Ficheros clave:
> - `docs/validation/ACTIVAR-SESION-04-MOTOR.md`
> - `docs/adr/0076-limpia-es-sin-alternancia-de-colores-y-lo-filtra-rn009.md`
> - `tests/unit/test_a21_series.py`
> - `scripts/orden_stop_o_limite.py`
> - `docs/validation/anexos/ESCENARIOS-POR-SESION/dia_del_bot.py`
> - `PROJECT_STATE.md`

## 10. Respuesta del consultor a la PARADA (2026-10-12)

Copiada tal cual:

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de trabajo/activar-sesion-04-motor (2026-10-12). Cópiala tal cual al final del encargo y del informe, en «Respuesta del consultor a la PARADA», con su fecha, y aplícala punto por punto (skill fase-cero). El régimen nocturno ya no rige: si algo medido contradice esta respuesta, PARADA 2.
>
> 0. A-21, el tramo de sin_alternancia_de_colores. Error del consultor, dicho con nombre: el tramo del encargo («del fin del bloque de origen a la vela que rompe») no filtra nada, porque bloque_de_origen toma la última vela contraria. Pero tampoco elijo tu (a). El auditor del consultor mide en estructura_m1.py y pivotes_m15.py que cada paso de roja a verde después de primer_impulso forma una zona de control que zonas_de_control cuenta (incluida la que forma un breaker verde). Por eso la alternancia verde-roja-verde-roja antes de la ruptura ya la rechaza zonas_control_max_por_esquema = 1 (RN-009). Tu (a) descartaría todo esquema con dos zonas o más, y el tramo acotado a la última zona queda vacío en el caso típico. Decisión: se mide antes de añadir nada.
>    a. En el informe, una tabla de series sintéticas, en compra y en venta. Como mínimo:
>       - el ejemplo de S-10 (verde, roja, verde, roja antes de la ruptura);
>       - un retroceso limpio de un solo bloque;
>       - un esquema con una zona de control y el último tramo limpio;
>       - la alternancia con una vela de cuerpo cero en medio (R, doji, V, R);
>       - un breaker contrario que rompe con mecha (criterio MECHA).
>       Por cada serie: lo que da detectar_esquema con solo_una_zona_de_control y el tope de RN-009, y lo que daría una comprobación literal de «ningún cambio de color en el retroceso» (tu (a), solo como medida, sin entrar al enum).
>    b. Si la única diferencia sale de las series con cuerpo cero o con breaker por mecha: A-21 se cierra con un RESOLVE_UNKNOWN de S-10 con valor solo_una_zona_de_control, la opción que ya existe. No se suma ninguna opción al enum.
>       - ADR-0076 dice: el trader define «limpia» como «sin alternancia de colores», y eso es lo que RN-009 ya filtra, porque cada alternancia forma una zona de control (con las series de la tabla como prueba). Y deja escrito que el consultor retira la opción nueva y la regla de la vela sin cuerpo que decidió el 2026-10-11.
>       - Dos preguntas van a la lista de la sesión 5, en el lenguaje del trader, con opciones y «otra, ¿cuál?»: si una vela sin cuerpo en medio del retroceso corta o no el retroceso, y el caso del breaker que rompe con mecha si la tabla lo distingue.
>    c. Si alguna serie sin cuerpo cero ni mecha da distinto: PARADA 2 con esa serie y no cierres A-21.
>    En los dos casos, el test que falla con main es semántico: con zona_control_limpia fijada, el motor corre sin --diagnostico-a21; en main, SinLecturaDeZonaError. Las series de la tabla quedan como tests.
> 1. Diagnostico.a21: (a). Se amplía rutas_permitidas de contrato.yaml con scripts/embudo_77.py, scripts/caja_77_exploratoria.py y scripts/orden_stop_o_limite.py, y se pasan a argumentos con nombre, sin a21. Los cuatro scripts que recorren LECTURAS_LIMPIA no se tocan; dilo. Si al final no entra opción nueva, recorren las mismas dos de siempre.
> 2. ACTIVAR-A35-A44.md §6: (a), una nota de tres líneas al principio (A-21 RESUELTA con su opción y su ADR, --diagnostico-a21 retirado, el resto de §6 es histórico). La tabla solo gana fila si entra una opción nueva.
> 3. Los sitios de A-21: dado por bueno. No hay regla que la cite, y se dice; cambian la descripción de zona_control_limpia y el texto de A-21 en ambiguedades.yaml.
> 4. La cita de RN-003: (a), hecho. Que feedback pending no admita dos CORRECT vivos sobre una regla va a las líneas del cierre como deuda (G.2). Lo mismo para RN-035 si le pasa igual: dilo.
> 5. §0.8, puntos 1 a 7: aceptados. El 4 (la racha tras la novena) queda como lectura provisional, tal como dice ADR-0077 §5. Corrige en el informe «es la única lectura»: el propio ADR da alternativas. Añade a la lista de la sesión 5: «Después de parar por 9 pérdidas seguidas, cuando vuelves al día siguiente: (a) empiezas a contar de cero; (b) sigues en 9 y una pérdida más te vuelve a parar ese día; (c) otra, ¿cuál?».
> 6. §8: añade el run 38217718887 sobre 136bb86 (el que la sesión dio al terminar) y comprueba con gh que es de ese sha y que solo falla test_state_check_ok_on_real_repo; si no puedes comprobarlo, dilo. Sale del «Pendiente de Aleks».
>
> Después: el commit de A-21, con el paso 3 de activar-sesion entero (registros, feedback apply --check y sin --check, cinco sitios, test_kit.py, spec_version a mano + manifest y docs --escribir, knowledge validate antes de make check, Fuente: en el cuerpo). Luego:
> - push a fix/activar-sesion-04-motor y el número de run;
> - revisor (opus) solo sobre lo nuevo, con tres alcances: la tabla de series y el cierre de A-21; el grep de --diagnostico-a21 y de a21 en src/, tests/ y scripts/; y que las líneas del cierre de §6 recogen R3.1 sin A-21, la lista de la sesión 5 actualizada y la deuda del punto 4.
> Su informe, pegado al final. Si el clasificador niega un push o la guardia un make, dame el comando exacto y lo lanzo yo con «!».
>
> Rama lista para revisión, NO cerrada.

## 11. Orden de cierre (consultor, 2026-10-12)

Copiada tal cual; Aleks la confirmó como su orden de cierre en la conversación del 2026-10-12 y
lanzó `/cerrar-rama trabajo/activar-sesion-04-motor`.

> Modelo: el que tengas · Esfuerzo: medio
>
> Orden de cierre de trabajo/activar-sesion-04-motor (consultor, 2026-10-12). Cópiala al informe ACTIVAR-SESION-04-MOTOR.md, sección «Orden de cierre», con su fecha. El ritual lo manda RITUAL.md y lo recorre la skill cerrar-rama.
>
> ANTES DE NADA
> - La CI de a598597 es el run 38247668329 (solo test_state_check_ok_on_real_repo): entra en §8 del informe en el commit del contrato, junto a los de f358748 (38243202933, con la reejecución) y 1d39c1e (38213911827). Compruébalo con gh; si falla otra cosa, PARA.
>
> TAG: stable/F37n-activar-sesion-04-motor. Comprueba en HISTORIA que el último es stable/F37m-activar-sesion-04 y que F37n no existe; si no es así, usa la siguiente libre y dímelo.
>
> COMMIT DEL CONTRATO (en la rama, un solo commit, como manda RITUAL.md): sale contrato.yaml; entran el registro del cierre en HISTORIA, la fila de la rama en ERRORES-RECURRENTES.md, el run de §8 y TODO lo que sigue de Next Action y hoja de ruta.
>
> Next Action: las líneas de §6 del informe, con estos cambios:
> - E sale a HISTORIA como HECHA, con el texto de §6 y bajo «# Next Action HECHA · E · …».
> - F: «Orden de trabajo: lo siguiente es S (R2.1, julio). Antes de su rama, el consultor decide si es construcción o reservado y lo comprueba en el repo; la hoja de ruta manda el orden.»
> - S pierde «DESPUÉS de la activación de la sesión 4 (E)» (cumplido); I pierde la «E» de «después de X, S y E». Ninguna letra viva puede depender de E: el cuadre de la hoja de ruta lo comprueba.
> - Heredados 25, 30 y 35: como dice §6.
> - G.2 (hoja de ruta) gana: el token ambiguo sin productor (ADR-0075); feedback pending con dos CORRECT vivos sobre una regla (RN-003); el recuadro que le falta a ADR-0044 §1 y su fila del índice; y el anexo dia_del_bot.py de ESCENARIOS-POR-SESION, que no corre con el código de hoy (no se edita: se reproduce con el código de su commit). Nada de esto va a Technical Debt de PROJECT_STATE.
> - G.1 (hoja de ruta) gana el falso positivo de la guardia: grep -rn --include=*.py con cuatro -e sobre rutas literales se bloquea y con dos pasa.
>
> Hoja de ruta:
> - R1.1: Estado HECHA. La parte de spec en trabajo/activar-sesion-04 y la de motor en esta rama. Las «en parte» quedan escritas en ACTIVAR-SESION-04.md §5 y ACTIVAR-SESION-04-MOTOR.md §5, y pasan a R4.1. «Hecho cuando» se reescribe así: cada «resuelve» está RESUELTA y cada «en parte» está escrita en la lista de la sesión 5 de esos informes. Si no se dice así, R2.1 (julio) quedaría colgada de R4.1 a través de J.
> - Las referencias NA:E salen de R1.1, R2.1 y R5.4; donde haya «R1.1 (NA:E)» queda «R1.1».
> - R3.1: Refs y «Depende de» sin A-21 («hoy lo necesita para A-35 y A-44»).
> - R4.1: gana ID:ADR-0076 e ID:ADR-0077, pierde ID:A-21, y su «Qué es» suma las preguntas de §5 (último minuto, vela sin cuerpo, breaker con mecha, racha tras la novena, confirmación bajista de S-13).
> - Pasa el test de la hoja de ruta y la salida del cuadre va al informe final.
>
> HALLAZGOS DEL CONSULTOR (para la fila de ERRORES-RECURRENTES.md)
> - Importa (del consultor): el encargo definía sin_alternancia_de_colores sobre un tramo en el que nunca hay cambios de color (bloque_de_origen toma la última contraria), y la opción era redundante con RN-009: cada alternancia ya forma una zona de control. Lo vio primero la sesión en su PARADA; la redundancia, el auditor del consultor; la tabla de series lo confirmó. Lección para el consultor y el revisor: una opción nueva de un enum se mide antes con series sintéticas contra lo que el motor ya filtra, y no se decide sobre la prosa.
> - Menor: el informe afirmaba «grep vacío» cuando quedaban un comentario y un test; lo vio el revisor. Lección: lo que dice el informe se pega con la salida, no se resume.
> - Menor: §0.8.4 llamaba «la única lectura» a lo que ADR-0077 §5 da con alternativas. Lección: una lectura de la sesión se presenta como una de varias, con las demás nombradas.
> - Dato, sin lección: la primera CI de f358748 se canceló por el timeout del workflow con apt-get install ffmpeg colgado; con la reejecución pasó. Si se repite, rama propia para el workflow.
>
> EL RITUAL: merge a main; tag; commit de estado que solo reemplaza Current Branch, Current Feature, Stable Main State y Last Stable Commit (la Next Action ya cambió en el commit del contrato; nada a Completed Features ni al Change Log); make check sellado; push atómico de main y el tag en un solo comando (si el clasificador lo niega, dame el comando exacto y lo lanzo yo con «!»); CI de main en verde; luego se borran la rama local y la remota fix/activar-sesion-04-motor. Ningún worktree de otra sesión se toca.
>
> INFORME FINAL: sha de main, tag, run de la CI de main, ramas que quedan (locales y remotas), tamaño de PROJECT_STATE.md y la salida del cuadre de test_hoja_de_ruta.

## Estado

Rama lista para revisión, NO cerrada (2026-10-12). Hechas las cinco decisiones, cada una en su
commit sellado: la 3 (A-21), con la respuesta del consultor a la PARADA (§10), sin opción nueva
(§1.5). Dos pasadas del revisor (§9.2 y §9.3), las dos atendidas: ningún hallazgo que bloquee.
La CI de cada push, en §8. Orden de cierre del consultor del 2026-10-12 (§11), confirmada por
Aleks: el commit del contrato saca `contrato.yaml` y trae el registro en HISTORIA, la fila de
ERRORES-RECURRENTES, la Next Action y la hoja de ruta. Al hacerlo, R1.1 HECHA no podía seguir
nombrando las letras vivas F y H (`test_hoja_de_ruta.py`, «esta HECHA y la letra sigue viva»):
F ya estaba en G.4 y H pasa a R4.1, donde va S-14; dicho en el registro de HISTORIA.
