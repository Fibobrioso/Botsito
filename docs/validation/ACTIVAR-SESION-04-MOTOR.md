# ACTIVAR-SESION-04-MOTOR · Lo que la sesión 4 dejó para el motor (R1.1, entrada E)

Rama `trabajo/activar-sesion-04-motor`, abierta el 2026-10-11 desde `main` en d4b7917 (commit de
estado sobre el merge cbe8e09, tag `stable/F37m-activar-sesion-04`). Encargo:
`docs/encargos/trabajo-activar-sesion-04-motor.md` (con el añadido del régimen nocturno de Aleks).
Tramo: R1 (R1.1 de `docs/plan/HOJA-DE-RUTA.md`; E de la Next Action).

Los ids que este informe cita y todavía no existen (los ADR que el encargo manda escribir; cada uno
sale de aquí en el commit que lo crea):

```ids-inexistentes
ADR-0075 — el ADR de S-13 (decisión 2 del encargo); no existe hasta su commit
ADR-0076 — el ADR de A-21 (decisión 3 del encargo); no existe hasta su commit
ADR-0077 — el ADR de A-51 (decisión 4 del encargo); no existe hasta su commit
```

## Pendiente de Aleks

Régimen nocturno (añadido de Aleks del 2026-10-11, copiado en el encargo): nada espera; lo que
depende de él va aquí con su comando exacto.

1. **La PARADA de la decisión 3 (A-21)**, abajo en «Lo que necesito que decidas»: la responde el
   consultor; hasta entonces A-21 no se toca y `--diagnostico-a21` sigue.
2. **El literal de v10 1:44:49** («1 o 2» o «12»), si lo lee con `--crudo` en su terminal: va al
   informe y a las líneas de H; si no llega, H se queda como está.
3. (Se añaden según avance la rama: el push a `fix/`, un `make check` que el reaper corte, …)

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
| m9 | «Un test que demuestre que `detectar_esquema` con una lectura fuera de LECTURAS_LIMPIA sigue fallando» | Ya existe: `tests/unit/test_estructura_m1.py:236-237` (`"al_ojo"`, `match="A-21"`) | Se cita; con la opción nueva se amplía (PARADA) |
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
   sesión 3»). Sin eso, el CORRECT es un pendiente que la skill prohíbe dejar.
2. **La fila de A-51 (y la de A-21, tras la PARADA) sale de Known Ambiguities en su commit**, no en
   el cierre: `test_kit.py:414-423` (a4).
3. **A-51 lleva su RESOLVE_UNKNOWN** además de los cuatro registros de parámetro (m12).
4. **La racha tras la novena** (m6): el acumulador `racha_perdidas` da SÍ contra `racha_perdidas_max`
   cuando la racha es ≥ tope Y la pérdida que la puso ahí cayó en el día operativo en curso (el de
   `reloj_sesiones`); al día siguiente la racha sigue en 9 (`reinicio = nunca`) pero la detención
   ha caducado (`reanudacion = dia_siguiente`), y la siguiente pérdida -la décima- vuelve a
   detener el día en que caiga. Es la única lectura en la que las tres cosas del encargo («tras la
   novena no se opera más en ese día», «se vuelve … el día siguiente», «la racha sigue de un día a
   otro») valen a la vez; va escrita en ADR-0077 como lectura de la sesión.
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
   `EstructuraError` (la guardia de `test_estructura_m1.py:236-237`, m9).
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

**Espero tu respuesta a la PARADA** para la decisión 3. Las decisiones 1, 2, 4 y 5 siguen esta
noche, cada una en su commit, con lo de §0.8 declarado.

## Estado

EN CURSO (abierta el 2026-10-11).
