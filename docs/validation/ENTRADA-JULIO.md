# ENTRADA-JULIO · Julio de 2026 entra como material de construcción (R2.1, entrada S)

Rama `trabajo/entrada-julio`, abierta el 2026-10-12 desde `main` en 1d37c7a (commit de estado
sobre el merge 79e74b2, tag `stable/F37n-activar-sesion-04-motor`). Encargo:
`docs/encargos/trabajo-entrada-julio.md`. Tramo: R2 (R2.1 de `docs/plan/HOJA-DE-RUTA.md`; S de
la Next Action).

(El bloque de abajo declara el ADR que el encargo manda escribir y que aún no existe, como exige `knowledge validate`;
sale de aquí en el commit que lo crea.)

```ids-inexistentes
ADR-0078 — el ADR de la fase 2 (julio entra en construcción); no existe hasta su commit
```

## Base, comprobada con git al abrir

- `git rev-parse main origin/main`: dos veces `1d37c7a7dba81240a8dbda626f7a657b14294910`.
- `git rev-parse main^1` y `git rev-parse "stable/F37n-activar-sesion-04-motor^{commit}"`: los dos
  `79e74b292c4aa95935712c114c14e0f92959a049`; el tag está en origin
  (`git ls-remote --tags origin`: objeto 6651cfc, anotado), y es el último `- Tag: ` de HISTORIA.
- CI de `main` sobre 1d37c7a (check-runs, sha literal): run 38296106720, `completed` / `success`.
- `git branch --list`: solo `main`; `git ls-remote --heads origin "fix/*" "trabajo/*" "feature/*"`:
  vacío.
- `/model`: Opus 5.5 con esfuerzo alto (lo pedía el encargo antes de nada).

## 0. Fase 0 · inventario (2026-10-12), sin abrir nada y sin escribir en el repo

Medido en la rama sobre `main` 1d37c7a. Ningún fichero de julio está todavía en la máquina (0.b),
así que no se ha abierto, listado ni hasheado nada suyo. El auditor del encargo
(`auditor-encargo`) contrastó 55 afirmaciones; su resumen, en «El encargo frente al repo».

### 0.a La base y los puntos 1, 2 y 5 de la decisión

- Base: arriba, «Base, comprobada con git al abrir».
- **Punto 1.** `knowledge/cases/meses_reservados.yaml` declara solo `2026-02` y `2026-03`: julio no
  está. CORRECTO.
- **Punto 2.** Con `casos_reservados(repo)` y `casos_ocultos(repo)` sobre los repartos commiteados
  de los dos caminos, contando por mes y sin imprimir ids (guion de la carpeta de trabajo,
  `recuento_julio.py`): `2026-07: casos_reservados 0; casos_ocultos 0`. Control con el mismo guion
  sobre mayo: `2026-05: casos_reservados 13; casos_ocultos 13`, los 13 días holdout que ya
  documentan `kit/config.yaml` y ADR-0025. El auditor, por su lado: 34 reservados en total,
  ninguno de julio, y `meses_libres` incluye julio. CORRECTO.
- **Punto 3** (lo midió el auditor): `knowledge/cases/kit/vistos.yaml:60-64`, `mes: "2026-07"`,
  `visto_el: "2026-08-03"`, fuentes `ev-v2-003320-a736fd37` y `ev-v3-002714-742f2589`. CORRECTO.
- **Punto 4**: `HOLDOUT-EXPOSICIONES.md:40`, fila del 2026-10-04: julio en 0:26:36, 0:57:08 y
  1:48:58 de v10, operaciones comentadas en voz. CORRECTO.
- **Punto 5.** `huso_operativa` = `Europe/Madrid` y `reloj_sesiones` = `rejilla_h4`
  (`knowledge/spec/parametros.yaml`). ADR-0069 §1 (líneas 34-37): la rejilla y Madrid difieren
  solo los días en que un lado cambió la hora y el otro no, que en 2026 son del 9 al 27 de marzo y
  del 26 al 30 de octubre; ninguno de julio. §5 deja pendiente de X solo la ventana de un mes de
  invierno. CORRECTO.
- **Punto 6** (auditor): ADR-0073 §5, líneas 70-77. CORRECTO.

### 0.b El material de julio

**No está en la máquina.** `test -d` (sin listar ninguna carpeta madre):
`corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026` no existe.

**La ruta que da el encargo no es la del corpus** (auditor, fila 8, comprobado):
«corpus/Material adicional de su operativa/Backtest julio 2026/» queda FUERA de la raíz del corpus,
que es `corpus/Estrategia del trader` (`knowledge/corpus/fuentes.yaml:6`). Ahí:
- la guardia no protege las fotos: solo mira
  `MATERIAL = "corpus/estrategia del trader/material adicional de su operativa"`
  (`.claude/hooks/guardia.py:221`, `:439-440`, `:460-464`);
- `botsito corpus inventory` no ve nada, y la ruta de `libros.yaml` (relativa a la raíz:
  `"Material adicional de su operativa/Backtest mayo 2026/..."`, línea 41) no casaría.

La ruta buena es la de mayo y marzo:
`corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026/`. Es la
decisión 0.

Los nombres, tamaños y sha256 (xlsx, vídeo y fotos) se calculan en cuanto esté copiado, sin abrir
nada, y van a la sección 0.b-bis con la respuesta a la PARADA.

### 0.c El terreno

**1. La guardia.**
- `MESES_DE_DESARROLLO = ("2026-01", "2026-04", "2026-08")` (`guardia.py:207`); `meses_legibles`
  son esos menos los que tengan un caso reservado (`:286-288`).
- Lo que hoy bloquea el material de julio, todo con `R_SIN_ABRIR` porque julio no tiene días
  reservados (`regla_del_mes`, `:473-476`):
  - el libro, por su nombre (`es_libro`: extensión de libro y «backtesting-analytics» en el
    nombre, `:429-431`), esté donde esté;
  - todo lo que haya en la carpeta `Backtest julio 2026` (`:465-468`), también el vídeo;
  - un libro suelto en `Material adicional` con «julio» en el nombre (`:469-470`).
- Las imágenes del material adicional se bloquean SIEMPRE con `R_CAPTURA` (`:463-464`), antes que
  la regla del mes: añadir julio a la lista no las desbloquea.
- Texto de la guardia que la fase 1 deja falso o que ya lo es: `R_SIN_ABRIR` (`:80-84`) dice que
  «la columna de fechas la lee el CONSULTOR», contra ADR-0072 (la lee Aleks); `R_LIBRO` (`:77`) y
  el docstring (`:13-14`) dicen «enero, abril y agosto».

**2. El camino dev-visto (ADR-0042), `src/botsito/cases/visto.py:69-112`, `requisitos`.** Tres
condiciones:
1. el mes en `knowledge/cases/kit/vistos.yaml` (julio ya está);
2. un libro del mes declarado en `knowledge/corpus/libros.yaml` Y su lectura completa declarada en
   `HOLDOUT-EXPOSICIONES.md`, comprobada porque el NOMBRE del fichero (el basename de la entrada de
   libros.yaml) aparece en ese documento (`:102-111`);
3. un tramo de `cobertura_material` (`kit/config.yaml`) con UN `material_sha256`, que es el sha del
   libro (`:87-93`).
El reparto (`construir`, `:135-149`) pone `dev` a TODOS los laborables de los tramos del mes, sin
sorteo: un laborable dentro del tramo sin filas en el libro es un día sin operaciones. Se escribe y
se ancla en `knowledge/cases/visto/<mes>/particiones.yaml` y `anclas.yaml` (`:152-165`), y no
sobreescribe.

**3. `casos ingerir`** (`src/botsito/cases/ingesta.py`, `dias_ingeribles`, `:160-206`): los días
son los casos de los repartos COMMITEADOS del kit **y del dev-visto** (`:193-195`) menos
`casos_ocultos`; antes comprueba `visto.problemas` y falla cerrado si el reparto dev-visto no es
válido (`:180-188`). Además `dias_del_material` niega un libro cuyo sha no esté en
`knowledge/corpus/manifest.yaml` (`:324-335`; auditor, herencia 1): **el xlsx de julio tiene que
estar inventariado antes de ingerirlo**, y el `material_sha256` del tramo se copia del manifiesto
(`kit/config.yaml:73-75`). El docstring de `casos_ingerir` (`src/botsito/cli.py:1626`) dice «de
los repartos commiteados DEL KIT» y no nombra dev-visto: se corrige en 3.g.

**4. Los ticks.**
- `data download-ticks` (`cli.py:2680-2790`) sale con 2 si un mes del rango no está en
  `construccion` de `knowledge/cases/criterio_fidelidad.yaml` (`:2711-2719`; hoy
  `construccion: ["2026-04", "2026-08"]`, línea 35). Con `--solo-dias-dev` toma los días de
  `dias_de_construccion` (`:2724-2739`). Sin `--horas` baja las 24 horas (`:3279`).
- `dias_de_construccion` (`src/botsito/engine/arnes.py:127-161`): el mes tiene que estar en
  `construccion` (`validar_meses`, `:100-115`) Y tener reparto dev-visto; si no, `ConjuntoError`
  «no hay reparto dev-visto» (`:145`). Un día del reparto sin fichero de caso entra con cero
  operaciones.
- **El manifiesto de agosto** (`data/manifests/ticks/eurusd-ticks-2026-08-75bd3a08.yaml`):
  `simbolo: EURUSD`, `escala: 100000`, `proveedor: dukascopy`, `huso_datos: UTC`, rango
  `2026-08-01`…`2026-08-31`, `seleccion.completa: false` con 21 días y `horas_utc` de 5 a 13; 186
  horas presentes, 3 perdidas, 0 ausentes. Para julio, lo mismo:
  `uv run botsito data download-ticks --dataset eurusd-ticks-2026-07 --simbolo EURUSD --escala 100000 --desde 2026-07-01 --hasta 2026-07-31 --solo-dias-dev --horas 05-13`.
  05-13 UTC es la ventana de verano (ADR-0051 DN-5; ADR-0069 §1).
- Un día dev de julio sin ticks no solo «no cuenta» (ADR-0051 §8): deja sin corrida habilitante a
  R3.1, porque `cableado.py:157-160` lo rechaza salvo con `--depuracion` y ADR-0070 §3 dice que
  `--depuracion` da «no» (auditor, fila 32).

**5. El libro de enero en `libros.yaml`** (líneas 53-67): entrada nueva con
`formato "AAAA/MM/DD HH:MM:SS"` y `huso: UTC`, medida por velas sobre TODAS las filas del mes
porque enero no tenía ningún día en ninguna partición (casos_ocultos y casos_reservados, 0): UTC
58/58, Europe/Madrid 2/58; controles abril (95 % / 11 %) y agosto (100 % / 2 %). La herramienta
`scripts/huso_por_velas.py` mide solo días `dev` de repartos commiteados (su docstring, y `:323`
«nada que medir»), así que enero se midió con un anexo propio,
`docs/validation/anexos/RELOJ-INVIERNO/huso_enero.py`, que usa las funciones de la herramienta
de `main` y comprueba dentro que ningún día está oculto (RELOJ-INVIERNO.md §4.1). **Julio está igual
que enero**: su reparto exige antes el libro declarado, y el libro se declara con la medida. Hace
falta un anexo igual y una ruta en el contrato (decisión 6). Velas M1 de julio: existe
`data/manifests/eurusd-m1-2026-07-aa162170.yaml`.

**6. El vídeo.**
- El siguiente `video_id` libre es **v11**: `fuentes.yaml` llega a v10, `manifest.yaml` también, y
  `v11` solo aparece como ejemplo SINTÉTICO en `tests/unit/test_cuarentena.py:102` (el de una
  sesión sin listar; la rama de la sesión 4 lo pasó de v10 a v11, y con un v11 real pasaría a v12).
- **v5** entró con `drive_id` (`fuentes.yaml:33-40`): Aleks lo subió a Drive el 2026-09-07, a la
  subcarpeta «transcripciones (crudas, Bot v3)», dos días después de recibirlo en local; su
  `naturaleza` describe el contenido (un día de abril en FXReplay).
- **Un vídeo con `drive_id: null` es, para tres sitios, una sesión con el trader:**
  - `src/botsito/corpus/inventario.py:99-105`: `InventarioError` si no tiene drive_id y su
    `naturaleza` no empieza por «sesion»;
  - `src/botsito/corpus/cuarentena.py:66-84`, `problemas_de_la_lista`: tiene que estar en
    `SESIONES_EN_CUARENTENA` o en `EXCEPCIONES`;
  - la guardia deduce la cuarentena de `drive_id: null` menos `SESIONES_SIN_CUARENTENA = {"v6"}`
    (`guardia.py:208-211`, `:290-303`): bloquearía su transcripción.
- Tests que listan vídeos: `tests/unit/test_inventario.py:171` (lista literal v1…v10),
  `tests/unit/test_cuarentena.py:91-96` (cruza con fuentes.yaml) y
  `tests/unit/test_guardia_claude.py:152` (`sesiones_en_cuarentena == {"v7","v8","v9","v10"}`).
- Un vídeo en la subcarpeta del mes vale: `fichero` es una ruta relativa a la raíz y el inventario
  lo clasifica como vídeo si está en `fuentes.yaml` (`inventario.py:196-197`, `:249`).
- `corpus check` NO forma parte de `make check` (`Makefile:69-70`, `:82`): copiar el material a
  `corpus/` antes de inventariarlo no pone `make check` en rojo.

**7. Los textos vivos**, y qué se puede corregir:

| Texto | Dice | Régimen | Qué propongo |
|---|---|---|---|
| `CLAUDE.md:159`, «Material de DESARROLLO» | «enero, abril y agosto de 2026» | editable (se corrige «en el mismo commit que la rompe») | fase 1: «enero, abril, julio y agosto» |
| `knowledge/cases/kit/config.yaml:50-54` | «NO SE DECLARAN enero, abril, julio ni agosto … lo hace EL CONSULTOR» | editable desde ADR-0035 (`:111-117`), con `Fuente:` | fase 1: quién lee es Aleks (ADR-0072); y además abril y agosto SÍ están declarados (`:61-65`, `:88-92`), así que el párrafo entero es falso hoy |
| `knowledge/corpus/libros.yaml:15` | «NO ESTAN enero ni septiembre» (enero está desde el 2026-10-06) | SOLO AÑADIR por ADR-0039; la validación compara solo las ENTRADAS parseadas (`libros.py:155-182`), no los comentarios | no se toca y se declara: la cabecera es parte de un fichero de solo añadir |
| `docs/runbooks/MIRAR-EL-MATERIAL.md:50-51` | «mayo o julio, que SI tienen dias reservados» | runbook; precedente de recuadro de corrección (el del 2026-10-06, `:53`) | fase 1: recuadro fechado; julio tiene 0 |
| `guardia.py:13-14, 77, 80-84` | «enero, abril y agosto»; «lee el CONSULTOR» | código de la rama | fase 1, mismo commit (decisión 8) |
| `docs/runbooks/ARNES-MOTOR.md:8-9`, `docs/runbooks/SESION-DE-PREGUNTAS.md:21` | construcción = «abril y agosto» | runbooks | en el commit de ADR-0078 (decisión 8) |
| `docs/adr/0043-*.md:29-30` | «construcción = abril y agosto» | ADR ACTIVE: precedente, una NOTA sin reescribir el cuerpo (la de ADR-0046) | en el commit de ADR-0078 (decisión 8) |

### El encargo frente al repo

Del auditor (55 afirmaciones: 38 correctas, 2 incorrectas y 15 con matiz; 13 cosas que el repo
pide y el encargo no recoge), comprobado por la sesión lo que cambia el trabajo:

- **INCORRECTA, la ruta de copia** (0.b): decisión 0.
- **INCORRECTA, el orden fase 2 → fase 3.e.** Con 2026-07 en `construccion` y sin reparto
  dev-visto de julio, `tests/unit/test_huecos_motor.py:300-310` llama a `dias_de_construccion` sobre
  todos los meses de construcción sin capturar `ConjuntoError`: en esta máquina, donde están las
  velas M1 de julio, `make check` sale en rojo y el commit de la fase 2 no se puede sellar. Y
  `tests/unit/test_criterio_fidelidad.py:108` afirma `construccion == ("2026-04", "2026-08")`.
  Decisión 5.
- **MATIZ, el huso «sobre todas las filas»**: la herramienta no lo hace sin días dev (0.c.5).
  Decisión 6.
- **MATIZ, `casos ingerir`**: exige el sha del xlsx en `manifest.yaml`, así que hace falta
  `uv run botsito corpus inventory` antes de 3.d (0.c.3). Decisión 7.
- **MATIZ, el vídeo «por defecto»**: sin `drive_id` no entra en el inventario (0.c.6). Decisión 4.
- **MATIZ, ADR-0072 y ADR-0039 §1.** ADR-0072 fija QUIÉN, CUÁNDO y QUÉ de la columna de fechas
  para cualquier backtest, pero leer fechas ANTES de declarar el libro en `libros.yaml` es una
  excepción a ADR-0039 §1 que su NOTA del 2026-09-24 acota a marzo. Decisión 9.
- **MATIZ, el «hallazgo» del margen no es nuevo**: ADR-0026, «Impacto» (líneas 116-123), ya dice
  que el margen supera los 100.000 con un stop por debajo de 1,67 × P pips «y F21 lo comprueba»;
  lo nuevo es que nadie lo comprueba (`firma_apalancamiento` no lo lee ningún código de `src/`, y
  el perfil `ftmo-2step-swing-100k.yaml:276` dice falsamente «Lo consume el broker simulado»). El
  informe de la fase 6 lo citará así. Decisión 10.
- **MATIZ, las «8 en parte»**: son 9 elementos (8 ambigüedades y S-14), los de
  `ACTIVAR-SESION-04.md` §0.e y `ACTIVAR-SESION-04-MOTOR.md` §5; y el §5 de los dos añade preguntas
  que la entrada propuesta no nombra (la confirmación bajista de S-13; el último minuto, las dos de
  ADR-0076 §4 y la racha tras la novena). Va a las propuestas del cierre.
- **MATIZ, R0.1 y NA:P**: R0.1 está HECHA y P está registrada como «Next Action HECHA · P» en
  HISTORIA, que es lo que exige `tests/unit/test_hoja_de_ruta.py:140-164`. Citar una letra ya
  hecha desde una entrada hecha es correcto por diseño; no hay nada que corregir.
- **MATIZ, `FTMO-P-D1.md`**: la entrada O dice «se registra parafraseada (RESPUESTAS-FTMO)»; ir a
  un fichero nuevo porque el otro está cerrado es una desviación de la letra de O y se declara.
- **Lo que el repo pide y el encargo no dice**, además de lo anterior: `--horas 05-13` explícito
  (0.c.4); en el cierre, «Next Action HECHA · S» y «· O» en HISTORIA, porque R2.1 (NA:S) y A.2
  (NA:O) los citan (`test_hoja_de_ruta.py`); la letra nueva de R4.1 en la Next Action y en los
  `Refs` de R4.1, que va al commit del contrato del cierre porque `docs/plan/` está protegido en la
  rama; y que ADR-0051 §6 (el spread supuesto de `llenado.yaml`) está medido solo sobre abril y
  agosto, cosa que ADR-0078 debe decir.
- **Una consecuencia que se declara**: desde que julio esté en `construccion`, `make check`
  (`test_huecos_motor.py:290-337`) corre el sesgo H4 del motor sobre las velas M1 de los días dev
  de julio, como ya hace con abril y agosto. Lee solo velas (ADR-0021 §1), ninguna etiqueta, y no
  es la corrida del arnés ni mide cobertura ni precisión.

### Lo que no pude medir

- Nada de julio: no está en la máquina (0.b).
- El nombre real del xlsx: la guardia lo reconoce como libro por «backtesting-analytics» en el
  nombre, y `visto.requisitos` busca su basename en HOLDOUT-EXPOSICIONES.
- Si hay en `corpus/` material de diciembre: no se lista ninguna carpeta de meses. `corpus
  inventory` regenera `manifest.yaml` desde el disco entero y lo metería (decisión 7).
- La documentación de MT5 sobre el margen en cuentas hedging: se mide en la fase 6.

### Exposiciones de la fase 0

Ninguna: no se abrió ni se listó nada de julio ni de ningún mes reservado. Una búsqueda de
`MargenAlcanza` con `grep -r .` desde la raíz del repo la bloqueó la guardia antes de leer nada,
porque habría entrado en `corpus/`; se repitió sobre `scripts/` y `docs/`.

## Lo que necesito que decidas

0. **La ruta de copia.** Opciones: (a) `corpus/Estrategia del trader/Material adicional de su
   operativa/Backtest julio 2026/`; (b) la del encargo, `corpus/Material adicional de su
   operativa/Backtest julio 2026/`. Recomiendo (a): es la raíz del corpus, la que protege la guardia
   y la que inventaría `corpus inventory`. Coste de (b): las fotos quedarían SIN guardia y nada se
   inventaría.
1. **Las fotos de julio** (pregunta 1 del encargo): ¿son capturas de Analytics, o de estadística?
   En esta rama no se abren en ningún caso; solo se hashean.
2. **La fecha MÍNIMA y la MÁXIMA de la columna de fechas del xlsx** (pregunta 2), leídas por ti una
   sola vez (ADR-0072). Las declaro hoy en HOLDOUT-EXPOSICIONES.
3. **¿El xlsx es la exportación del backtest grabado en el vídeo, o de otro?** (pregunta 3).
4. **El vídeo** (pregunta 4: cómo llegó y si lo subes a Drive). Opciones: (a) lo subes a Drive y
   entra como **v11** con su `drive_id`, como v5, con `naturaleza` «backtest de julio del trader,
   material de desarrollo»; (b) entra sin `drive_id`; (c) se queda fuera de `fuentes.yaml` en esta
   rama. Recomiendo (a): es el único camino que no toca código. Coste de (b): cambiar la regla de
   `inventario.py`, `EXCEPCIONES` de `cuarentena.py`, `SESIONES_SIN_CUARENTENA` de la guardia y
   `test_guardia_claude.py:152`, todo fuera del encargo. Coste de (c): `corpus inventory` lo
   inventaría como un fichero más de material adicional, y su rama propia lo pasa a vídeo.
5. **El orden de los commits.** Opciones: (a) fase 1 → fase 3.a-e (inventario del corpus, huso,
   libros.yaml, exposición, cobertura, reparto con su ancla) → **fase 2 (ADR-0078 y `construccion`,
   con `test_criterio_fidelidad.py:108`) en su propio commit** → 3.f (ingesta) → fase 4 (ticks, que
   exigen julio en `construccion`) → fase 5 → fase 6; (b) la fase 2 en el mismo commit que el
   reparto. Recomiendo (a): cada commit hace una cosa y la decisión sigue siendo anterior a
   cualquier corrida del arnés con julio. Coste de (b): un commit que mezcla reparto y decisión.
   Con el orden del encargo, el commit de la fase 2 no se puede sellar.
6. **El huso de julio.** Opciones: (a) un anexo `docs/validation/anexos/ENTRADA-JULIO/huso_julio.py`
   que repite el de enero (las funciones de `scripts/huso_por_velas.py` de `main` y las cifras de
   `criterio_huso.yaml`, todas las filas tras comprobar dentro 0 ocultos y 0 reservados), con el
   control de agosto por la herramienta de `main` sobre sus días dev; (b) cambiar la herramienta.
   Recomiendo (a): es el procedimiento ya revisado de enero. Coste de (b): código nuevo en una
   herramienta que decide `libros.yaml` para siempre. Amplío el contrato con
   `docs/validation/anexos/ENTRADA-JULIO/`.
7. **El inventario del corpus.** `corpus inventory` regenera `manifest.yaml` desde el disco
   entero. Opciones: (a) copias SOLO julio, lo corro antes de 3.d y compruebo en el diff que solo
   entran los ficheros de julio, parando si entra cualquier otra cosa (diciembre, por ejemplo);
   (b) diciembre ya está en disco y entra también. Recomiendo (a). Coste de (b): diciembre entraría
   en el inventario por nombres y sha antes de su rama (NA:I).
8. **Los textos que el encargo no nombra.** Opciones: (a) corregir en la fase 1 `R_SIN_ABRIR`
   (Aleks, no el consultor), `R_LIBRO` y el docstring de la guardia; y en el commit de ADR-0078
   `ARNES-MOTOR.md`, `SESION-DE-PREGUNTAS.md` y una NOTA en ADR-0043 (como la de ADR-0046), ampliando
   el contrato; (b) solo lo que nombra el encargo. Recomiendo (a): CLAUDE.md pide corregir en el
   mismo commit lo que el commit rompe. Coste de (b): tres textos vivos falsos desde esta rama.
9. **La lectura de fechas antes de declarar el libro.** Opciones: (a) ADR-0078 dice que la
   excepción de ADR-0039 §1 (hoy acotada a marzo por la NOTA de ADR-0046) cubre julio, y añado una
   NOTA en ADR-0039 §1 que apunta a ADR-0078; (b) solo ADR-0078. Recomiendo (a): quien lea ADR-0039
   ve la excepción donde está la regla. Coste de (b): ADR-0039 sigue diciendo «solo marzo».
10. **La fase 6.** `knowledge/cuentas/` y `knowledge/spec/` están protegidos y el encargo prohíbe
   cambiar parámetros. Opciones: (a) `FTMO-P-D1.md` cita ADR-0026 Impacto (no es un hallazgo nuevo),
   declara lo falso del perfil («Lo consume el broker simulado») y de `parametros.yaml` («F21 lo
   comprueba»), y propone para el cierre una línea de Technical Debt y el texto nuevo del heredado
   37; (b) corregir aquí esas dos descripciones. Recomiendo (a): es lo que pide el encargo. Coste de
   (b): tocar el perfil y la spec, que esta rama no toca.

Espero tu respuesta a la PARADA.

## Estado

EN CURSO: fase 0 entregada, en la PARADA; espera la respuesta de Aleks.
