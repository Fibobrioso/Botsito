# ENTRADA-JULIO · Julio de 2026 entra como material de construcción (R2.1, entrada S)

Rama `trabajo/entrada-julio`, abierta el 2026-10-12 desde `main` en 1d37c7a (commit de estado
sobre el merge 79e74b2, tag `stable/F37n-activar-sesion-04-motor`). Encargo:
`docs/encargos/trabajo-entrada-julio.md`. Tramo: R2 (R2.1 de `docs/plan/HOJA-DE-RUTA.md`; S de
la Next Action).

(Hasta que existió, ADR-0078 iba declarado aquí en un bloque `ids-inexistentes`, como exige
`knowledge validate`; salió con el commit de la fase 2, que lo crea.)

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

## Respuesta del consultor a la PARADA (2026-10-12)

Copiada tal cual (los huecos `______` son de Aleks y llegan aparte; en §0.d, cada uno con su fecha):

> Respuesta a la PARADA de trabajo/entrada-julio (consultor, 2026-10-12). Copia esta respuesta tal cual en el informe y aplícala punto por punto.
>
> 0. Ruta: (a), corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026/. Es la raíz del corpus, la que protege la guardia y la que inventaría corpus inventory; la ruta del encargo era un error del consultor.
> 1. Las fotos: ______ (Aleks). Sea lo que sea, en esta rama no se abren: solo se hashean.
> 2. Columna de fechas del xlsx, leída por Aleks una sola vez hoy (ADR-0072): mínima ____-__-__, máxima ____-__-__. Declárala hoy en HOLDOUT-EXPOSICIONES.
> 3. ¿El xlsx es la exportación del backtest del vídeo?: ______ (Aleks). Si es «no» o «no lo sé», sigue igual con el xlsx y apúntalo para la rama del vídeo y para el cuestionario de la sesión 5.
> 4. El vídeo: (a). Aleks lo subió a Drive, a la carpeta de v5; enlace: ______. Entra como v11 con su drive_id y la naturaleza «backtest de julio del trader, material de desarrollo». Es el único camino que no toca código. La transcripción y los fotogramas, en su rama propia.
> 5. El orden: (a). Fase 1 → 3.a-e (inventario, huso, libros.yaml, exposición, cobertura, reparto y ancla) → fase 2 en su propio commit (ADR-0078, construccion y test_criterio_fidelidad.py:108) → 3.f → fase 4 → fase 5 → fase 6. Así cada commit se sella y la decisión sigue siendo anterior a cualquier corrida con julio.
> 6. El huso: (a). Un anexo huso_julio.py que repite el de enero con las funciones de main, comprobando dentro 0 ocultos y 0 reservados, y con el control de agosto por la herramienta de main. Es el procedimiento ya revisado. Amplía el contrato con docs/validation/anexos/ENTRADA-JULIO/.
> 7. El inventario: (a). Aleks copió solo julio. Mira el diff de manifest.yaml y PARA si entra cualquier cosa que no sea de julio.
> 8. Los textos: (a). Corrige R_SIN_ABRIR, R_LIBRO y el docstring de la guardia en la fase 1; y ARNES-MOTOR.md, SESION-DE-PREGUNTAS.md y una NOTA en ADR-0043 en el commit de ADR-0078. Amplía el contrato. Lo que un commit deja falso se corrige en ese commit.
> 9. Las fechas antes del libro: (a). ADR-0078 extiende a julio la excepción de ADR-0039 §1, con una NOTA en ADR-0039 §1 que apunte a ADR-0078. La excepción se ve donde está la regla.
> 10. La fase 6: (a). FTMO-P-D1.md cita ADR-0026 «Impacto» como origen; no es un hallazgo nuevo, y así lo corrige el consultor. Declara que es falso lo que dicen el perfil («Lo consume el broker simulado») y parametros.yaml («F21 lo comprueba»). Propón para el cierre una línea de Technical Debt (que el simulador compruebe el margen, con su rama) y el texto nuevo del heredado 37. No toques el perfil ni la spec.
>
> Además:
> - Las «en parte» son 9 elementos (8 ambigüedades y S-14). La entrada de R4.1 que propongas para el cierre nombra también las preguntas de los §5 (la confirmación bajista de S-13, el último minuto, las dos de ADR-0076 §4 y la racha tras la novena).
> - R0.1 y NA:P: de acuerdo, no hay nada que corregir. Retiro esa propuesta.
> - O va a un fichero nuevo porque RESPUESTAS-FTMO es un informe cerrado: declárala como desviación de la letra de O, aceptada por el consultor.
> - La consecuencia de 0.c (make check corre el sesgo H4 sobre las velas de julio) queda aceptada: solo lee velas y no mide nada.
>
> Sigue con la fase 1. Si la rama cambia el Makefile o el clasificador niega un push, para y dame el comando con «!». Al terminar, revisor, CI de fix/entrada-julio con los números de run, y «Rama lista para revisión, NO cerrada».

### Cómo se aplica, punto por punto

| Punto | Estado |
|---|---|
| 0 | aplicado: la ruta es la de la raíz del corpus. **La carpeta todavía no está en la máquina** (`ls` de esa carpeta y solo de ella, 2026-10-12, después de la respuesta: «No such file or directory»), aunque la respuesta diga «Aleks copió solo julio»: se le pide al terminar la fase 1 |
| 1, 2, 3 y el enlace de 4 | huecos de Aleks: se le piden al terminar la fase 1; van a §0.d con su fecha |
| 4, 5, 6, 7, 9, 10 | se aplican en su fase, en el orden del punto 5 |
| 8 | la parte de la guardia, en la fase 1 (§1); la de ADR-0078, en su commit |
| Además | las propuestas del cierre, al final; R0.1 retirada; la desviación de O, en la fase 6; la consecuencia de 0.c, aceptada |

## Datos para la fase 3 (Aleks y consultor, 2026-10-13)

Copiados tal cual. Rellenan los huecos de los puntos 1 a 4 de la respuesta (lo que se mide con ellos, en §0.d):

> Datos para la fase 3 (Aleks y consultor, 2026-10-13). Si recibiste antes un mensaje que recortaba la rama porque no había xlsx, queda ANULADO: el Excel llegó y sigue el plan completo de la respuesta a la PARADA (decisiones 0 a 10, con el orden de la decisión 5).
>
> 1. Material copiado a corpus/Estrategia del trader/Material adicional de su operativa/Backtest julio 2026/: el xlsx de julio (nombre tal como lo exportó FX Replay), 4 vídeos de julio y fotos de resumen. Nada de otros meses.
> 2. Las fotos son capturas de resumen (estadística del mes): se tratan como Analytics y no se abren nunca. Solo nombre, tamaño y sha256.
> 3. Columna de fechas del xlsx, leída por mí una sola vez hoy (ADR-0072): mínima 2026-07-01, máxima 2026-07-17. Al leerla vi también la hora de esas dos filas, y nada más. Declárala hoy en HOLDOUT-EXPOSICIONES.
> 4. Lo que dice el trader, de palabra a Aleks el 2026-10-13: el xlsx es la exportación de los 3 primeros vídeos. El 4.º termina el mes (desde el 20 de julio), pero de esos días no exportó el Excel, y ya no puede porque borró el backtest. Así que del 1 al 17 hay vídeo y Excel; del 20 al 31, solo vídeo y las fotos de resumen.
> 5. Vídeos: 4, en Drive de Aleks (carpeta «backtest Julio 2026», 1W0KQ12C-TKCQDTlYmekWgUmYQoCxj2Jq). Entran por orden de grabación, que es el de su nombre:
>    - v11: «2026-10-02 20-18-00.mkv», drive_id 13v1eZMhVq-g9ao17hqqv-hQwjC6xTb1T, 419918585 bytes en Drive
>    - v12: «2026-10-02 20-53-08.mkv», drive_id 1C7lZOtYZ0J12IjzdpWnCEo-CPzwchCz_, 739623714 bytes
>    - v13: «2026-10-04 09-45-43.mkv», drive_id 1w0zlVCMFt1e_TjMOUbNpzPxtQ7-_pYwT, 815725885 bytes
>    - v14: «2026-10-04 12-40-14.mkv», drive_id 19yHqjeekIllhB0zV9Ks_78M3jKZrubU6, 1194821502 bytes
>    Comprueba que los bytes en disco coinciden con los de Drive. Si alguno no coincide, PARA.
>    Naturaleza: «backtest de julio del trader en FX Replay, material de desarrollo». Que v11 a v13 son los del xlsx (1 a 17 de julio) y v14 el del tramo final sin xlsx es lo que dice el trader; como el orden de grabación lo hace probable pero no lo prueba, escríbelo así en fuentes.yaml y en el informe, y lo comprueba la rama de transcripción.
>    De cada uno, con ffprobe y sin abrir fotogramas: duración y si tiene pista de audio, al informe.
>
> DECISIÓN DEL CONSULTOR SOBRE EL TRAMO
> - El tramo de 2026-07 en cobertura_material es 2026-07-01 a 2026-07-17, con el material_sha256 del xlsx. Igual que abril, es un LÍMITE INFERIOR de lo que cubre el libro: un día del borde sin operaciones no se distingue de uno no cubierto.
> - Los días del 20 al 31 de julio NO entran en el reparto dev-visto ni en los casos: no hay libro que los cubra (ADR-0042 §2). Quedan solo en v14.
> - Las fotos tampoco sirven para ellos: son un agregado del mes entero.
> - En el informe y en ADR-0078 queda escrito por qué julio entra en construcción solo del 1 al 17, y que la decisión de sacar casos del vídeo para el resto va después de la rama que transcriba v11-v14.
> - Ticks: download-ticks con --solo-dias-dev bajará solo los días del reparto (1 al 17). Compruébalo en su salida.
> - Propuesta para la orden de cierre: R2.1 pasa a HECHA en lo del libro, y entra una entrada nueva, «Julio 20-31: solo en vídeo (v14); decidir si se extraen casos del vídeo, tras transcribir v11-v14».
>
> Sigue con la fase 3 y el resto, en el orden aprobado. Si el diff de manifest.yaml trae cualquier cosa que no sea de Backtest julio 2026, PARA. Si el Makefile cambia o el clasificador niega un push, para y dame el comando con «!». Al terminar: revisor, CI de fix/entrada-julio con los números de run, y «Rama lista para revisión, NO cerrada».

## 1. Fase 1 · la guardia y los textos (2026-10-12)

**`.claude/hooks/guardia.py`** (`git diff main --numstat -- .claude/hooks/guardia.py`: 12 líneas más, 8 menos, todas de estas tres cosas):
- `MESES_DE_DESARROLLO = ("2026-01", "2026-04", "2026-07", "2026-08")`, con su comentario
  (decisión del consultor del 2026-10-12; las imágenes siguen en `R_CAPTURA`).
- `R_SIN_ABRIR`: «la columna de fechas la lee Aleks (ADR-0072)», donde decía «el CONSULTOR».
- `R_LIBRO` y el docstring: «enero, abril, julio y agosto».

**Tests** (`tests/unit/test_guardia_claude.py`):
- `meses_legibles` con julio, en el repo sintético y en el real.
- `test_julio_se_lee_y_lo_demas_sigue_cerrado`, los dos sentidos y los dos rotos a propósito: el
  libro y el vídeo de julio se leen; dos imágenes de su carpeta (`.jpeg` y `.png`) dan
  `R_CAPTURA` y se pueden hashear; los libros de febrero, marzo y diciembre de 2025 dan
  `R_SIN_ABRIR`. Roto (1): sin 2026-07 en la lista (`monkeypatch`), el libro y el vídeo de julio
  vuelven a `R_SIN_ABRIR`. Roto (2): con un día de julio en una partición reservada, el libro da
  `R_LIBRO`.
- `test_cada_bloqueo_cita_su_regla_en_el_repo_real`: tres casos más (una foto de julio, el libro de
  febrero y el de diciembre de 2025), por la ruta y en la CI.
- `test_el_libro_de_julio_se_lee_en_el_repo_real`, con los repartos reales.
- **`test_la_guardia_frente_a_la_de_main_caso_a_caso`**: carga la guardia de `main`
  (`git show main:.claude/hooks/guardia.py`) y decide con las dos, por el NOMBRE de la regla y con
  los repartos reales, una matriz de 100 rutas sintéticas (ninguna se abre): de cada mes de
  diciembre de 2025 a diciembre de 2026, el libro, una `.jpeg`, una `.png`, un vídeo y un texto
  en su carpeta `Backtest`, el libro suelto en el material y el libro fuera del corpus; y nueve
  rutas sin mes (mensajes del trader, hojas de sesión, crudas en cuarentena, holdout, una
  `CRUDA-NO-LEER`, un caso dev). Exige que lo único que cambie sea el material de julio que no es
  imagen. Sin `main` en el clon, se salta.

**La comparación caso a caso** (anexo `docs/validation/anexos/ENTRADA-JULIO/guardia_caso_a_caso.txt`,
la salida del test con `-s`): **100 casos, 5 cambian**, y los cinco son de julio y pasan de
`R_SIN_ABRIR` a legibles: el libro en su carpeta, el vídeo, un texto de la carpeta, el libro suelto
en el material y el libro fuera del corpus. Los otros 95 deciden lo mismo con las dos guardias:
las 26 imágenes (las dos de cada mes) dan `R_CAPTURA` también en julio; febrero, marzo, octubre,
noviembre y diciembre (de 2025 y de 2026) siguen en `R_SIN_ABRIR`; mayo, junio y septiembre en
`R_LIBRO`; enero, abril y agosto, legibles, como en `main`. **Ningún caso que `main` bloqueaba deja
de bloquearse, salvo el material de julio que no es imagen.**

`uv run pytest tests/unit/test_guardia_claude.py -q`: todo en verde (dentro de `make check`, abajo).

**Los textos** (punto 8 y fase 1 del encargo):
- `CLAUDE.md`, «Material de DESARROLLO»: «enero, abril, julio y agosto de 2026», con la rama y la
  decisión; y «Sus imagenes no se abren».
- `knowledge/cases/kit/config.yaml`, el comentario sobre los meses de desarrollo: la columna la lee
  Aleks (ADR-0072), y ya no dice que abril y agosto no se declaran (lo están desde ADR-0042). Solo
  comentario: ningún valor cambia.
- `docs/runbooks/MIRAR-EL-MATERIAL.md`: un recuadro de CORRECCIÓN fechado junto al pasaje de julio,
  sin tocar el cuerpo.
- `knowledge/corpus/libros.yaml`: **no se toca.** Es de SOLO AÑADIR (ADR-0039, y su cabecera lo
  dice); su línea 15 («NO ESTAN enero ni septiembre») es falsa desde el 2026-10-06 y queda así.
  La validación compara solo las entradas, pero el régimen es del fichero.

**El contrato**, ampliado en este commit por los puntos 6, 8 y 9 de la respuesta:
`docs/validation/anexos/ENTRADA-JULIO/`, `docs/runbooks/ARNES-MOTOR.md`,
`docs/runbooks/SESION-DE-PREGUNTAS.md`, `docs/adr/0043-*.md` y `docs/adr/0039-*.md`.

## 0.d Los datos de Aleks y el material de julio (2026-10-13)

Los huecos de la respuesta, rellenos por los «Datos para la fase 3» (copiados arriba):
- **Fotos** (punto 1): capturas de RESUMEN, estadística del mes entero: se tratan como Analytics y
  **no se abrió ninguna, ni miniatura**. Solo nombre, tamaño y sha256.
- **Fechas** (punto 2): mínima 2026-07-01, máxima 2026-07-17, leídas por Aleks una vez el
  2026-10-13 (ADR-0072), con la hora de esas dos filas y nada más. Declarado el mismo día en
  `HOLDOUT-EXPOSICIONES.md` (fila del 2026-10-13).
- **El xlsx** (punto 3): según el trader, exporta los tres primeros vídeos; el cuarto, desde el 20
  de julio, no tiene xlsx. Va a la rama del vídeo y al cuestionario de la sesión 5.
- **Vídeos** (punto 4): cuatro, v11 a v14, con su `drive_id`.

**La carpeta** (`ls -la` de `corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/`
y solo de ella; su nombre real lleva **J mayúscula**) y los sha256 (`sha256sum` en la carpeta, sin
abrir nada):

| Fichero | Bytes | sha256 | Qué es |
|---|---|---|---|
| `2026-10-02 20-18-00.mkv` | 419918585 | `5732fe442ae416b736f7027c28aab438f291f5184b74d78027ee6145e8ba299f` | v11 |
| `2026-10-02 20-53-08.mkv` | 739623714 | `a045ec0bec87d6e6d899e6b5bd4fb585d5f261e1ec5873378d868984243f01a3` | v12 |
| `2026-10-04 09-45-43.mkv` | 815725885 | `8dc7efa12e264f64652179d6cfce1be8f84c3626baccf77576f8541d62b0c1ff` | v13 |
| `2026-10-04 12-40-14.mkv` | 1194821502 | `e13e4e4df1ffcc2aad90d3d07d138e217d6c0aa871178cb90f766a17203961d6` | v14 |
| `444444.jpeg` | 111816 | `0090a516f2d4031fc6dc7855f525ddea09fd8562adf892136c02d875ce6a26df` | captura de resumen, no se abre |
| `55125.jpeg` | 120215 | `585198ad997ae9eb3db0ea75cdfe548dfe0348822f4d1bdc157dcda719346bf9` | captura de resumen, no se abre |
| `66235.jpeg` | 96554 | `a9fe580bd254aca8b97c963e6e91104e09591a99e81c0db1181b00e2c391ac62` | captura de resumen, no se abre |
| `76543.jpeg` | 65071 | `b9aacda3d6273ee2375e109b8b121700e3ad14c9345c6b0c2e67a04f870c84f4` | captura de resumen, no se abre |
| `WhatsApp Image 2026-10-04 at 11.51.57 AM.jpeg` | 107323 | `8fae379fa3a73b19896a73da5c0de4a662bf46f399accc7886779476049b712a` | captura de resumen, no se abre |
| `WhatsApp Image 2026-10-04 at 11.51.57 AM4214.jpeg` | 93727 | `40507f5ff5987c78fc6929f295475482b9cc63e846e0e1ffd499303545d51fa9` | captura de resumen, no se abre |
| `backtesting-analytics_JULIO_2026.xlsx` | 13265 | `a8cb4ef47faaccee4d0f35adb13da9001abd241a10a3ab810acc33986b41f49f` | el libro |

- **Bytes frente a Drive**: los cuatro vídeos coinciden byte a byte con los que dio Aleks; no
  hace falta parar. Nada de otros meses en la carpeta.
- **El libro**: su nombre lleva guiones bajos (`backtesting-analytics_JULIO_2026.xlsx`); la guardia
  lo reconoce igual como libro de julio (`_MES` admite hasta tres no-dígitos entre mes y año).
- **Duración y audio** (de `knowledge/corpus/manifest.yaml`, por `corpus inventory`, que llama a
  ffprobe): v11 1260,9 s (21:01), v12 2220,8 s (37:01), v13 2449,3 s (40:49), v14 3587,5 s
  (59:47); los cuatro **con pista de audio**, 1280×720 a 30 fps. Total, 2 h 38 min.
- **HALLAZGO (importa): la guardia niega `ffprobe` sobre un vídeo.** `ffprobe -v error ... "<.mkv>"`
  se bloqueó con «la guardia no sabe con que se ejecuta ... (ni extension ni `#!`)»: trata el
  fichero como un guion que se ejecuta. No se rodeó: la duración salió por `corpus inventory`, la
  vía revisada. Propuesta para la Next Action (junto a K, el otro falso positivo de la guardia):
  que `ffprobe` y `ffmpeg -i` lean y no ejecuten, con un test que rompa los dos sentidos.

## 3. Fase 3.a-e · el libro, su lectura y su reparto (2026-10-13)

**Desviación declarada: v11 a v14 entran en `fuentes.yaml` aquí y no en la fase 5.** `corpus
inventory` regenera `manifest.yaml` desde el disco y solo clasifica como vídeo lo que está en
`fuentes.yaml`: sin ellos, los cuatro `.mkv` entrarían como material suelto y la fase 5 tendría que
rehacer el manifiesto. Con ellos entran los dos tests que listan vídeos (`test_inventario.py`, ahora
v1 a v14; `test_cuarentena.py`, el ejemplo sintético de sesión sin listar pasa de v11 a v15). Los
cuatro tienen `drive_id`: no son sesiones, no van a `SESIONES_EN_CUARENTENA` y la guardia no los
pone en cuarentena (decisión 4).

**3.a, otra vez antes de leer** (`recuento_julio.py`, el mismo guion de la fase 0):
`2026-07: casos_reservados 0; casos_ocultos 0`. El anexo del huso lo comprueba otra vez dentro
antes de abrir el libro.

**El inventario** (`uv run botsito corpus inventory`, decisión 7). La primera pasada salió con los
`.mkv` contados dos veces, como vídeos y como material: `fuentes.yaml` decía «Backtest julio 2026» y
la carpeta es «Backtest **J**ulio 2026» (Windows no distingue, el inventario sí). Corregida la
grafía (en `fuentes.yaml` y en el anexo), la segunda pasada da el diff limpio: **solo entran
ficheros de `Backtest Julio 2026`**, 7 como material (las seis capturas y el libro: 59 → 66) y 4
como vídeo (10 → 14). Nada de otros meses: no hay que parar.

**3.b El huso, por velas** (decisión 6; anexo `anexos/ENTRADA-JULIO/huso_julio.py`, que repite el
de enero con las funciones de `scripts/huso_por_velas.py` de `main` y comprueba dentro 0 ocultos, 0
reservados y que julio no está en `meses_reservados.yaml`; salida en `huso_julio.txt`):

```
== 2026-07: libro a8cb4ef47faa... formato 'AAAA-MM-DD HH:MM:SS'; declarado: NO (sin entrada en libros.yaml)
FILAS comparables: 72; sin entrada numerica: 0; descartadas por frontera de dia: no
UTC: 5/72 = 6.9 %
Europe/Madrid: 71/72 = 98.6 %
VEREDICTO (ADR-0039 §5, entre UTC y Europe/Madrid): Europe/Madrid

== 2026-08: libro 33a01f1d8124... formato 'AAAA/MM/DD HH:MM:SS'; declarado: UTC
UTC: 47/47 = 100.0 %   Europe/Madrid: 1/47 = 2.1 %   CONTROL: declarado UTC -> COINCIDE
```

Y el control con la herramienta de `main` tal cual sobre los 21 días `dev` de agosto
(`control_herramienta_agosto.txt`): UTC 47/47, Europe/Madrid 1/47, COINCIDE.

**Concluyente: Europe/Madrid** (98,6 % ≥ 90 % y 6,9 % ≤ 50 %). **Es el primer libro del trader
que no viene en UTC**: enero, abril, mayo y agosto vienen en UTC, y el formato es también distinto
del de enero, abril y agosto (es el de mayo, con guiones). No se interpreta por qué (otra versión de
la exportación de FX Replay, otro ajuste de la cuenta del trader); queda como dato para la rama del
vídeo, que puede comparar las horas del replay con las del libro. El procedimiento no se cambió para
llegar a este veredicto: es el de enero, con el umbral del criterio.

**3.c El libro** en `knowledge/corpus/libros.yaml` (entrada nueva al final, solo añadir):
formato `AAAA-MM-DD HH:MM:SS`, huso `Europe/Madrid`, con la medida y el control. **La exposición**,
en `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-13, con el nombre del fichero (lo que `visto.requisitos`
comprueba), declarada ANTES de la ingesta, que la completa hoy.

**3.d El tramo** en `cobertura_material` (`knowledge/cases/kit/config.yaml`): `2026-07-01` a
`2026-07-17`, con el `material_sha256` copiado del manifiesto. Los días del 20 al 31 no entran
(decisión del consultor del 2026-10-13).

**3.e El reparto**: `visto.requisitos(repo, "2026-07")` → `[]`; y
`uv run botsito casos visto --mes 2026-07` → `OK: knowledge/cases/visto/2026-07/particiones.yaml: 13
dias laborables, todos dev, sin sorteo; anclado en knowledge/cases/visto/anclas.yaml` (blob
`ee78cc0c22c697ca1be137748b9fd55f4fca3548`). Los 13 laborables del 1 al 17.

**Dos tests de contrato que fijan la lista a propósito**, ampliados con julio (fallaron en un
`make check` que se paró al verlos): `tests/contract/test_libros.py`, el registro real declara
enero, abril, mayo, julio y agosto, y el de julio es `AAAA-MM-DD HH:MM:SS` en Europe/Madrid (el mes
se lee ahora de la palabra en mayúsculas del NOMBRE del fichero, porque el de julio lleva guiones
bajos); y `tests/contract/test_mes_del_material.py`, los meses con `material_sha256` son abril, mayo,
julio y agosto. El contrato de la rama se amplía con los dos.

`uv run botsito knowledge validate`: `OK: manifiesto del corpus coherente con 14 videos esperados`,
`OK: 5 libros declarados con formato y huso, solo-anadir intacto, cruzados con cobertura_material`,
`... 3 repartos dev-visto`.

## 2. Fase 2 · ADR-0078: julio entra en construcción (2026-10-13)

En su propio commit, DESPUÉS del reparto dev-visto de julio (decisión 5) y ANTES de cualquier
corrida del arnés que incluya julio: no se ha corrido ninguna en esta rama.
- **ADR-0078** (`docs/adr/0078-julio-entra-en-construccion.md`; 0077 era el último): 2026-07 se
  añade a `construccion`, solo del 1 al 17; los días 20 a 31 quedan fuera (sin libro, ADR-0042 §2)
  y lo que se haga con ellos se decide tras la rama que transcriba v11-v14; extiende a julio la
  excepción de ADR-0039 §1 (decisión 9); cita la decisión del consultor, ADR-0043, ADR-0070 §2 y
  ADR-0042; **ningún umbral cambia**. Declara también que el spread supuesto de ADR-0051 §6 sigue
  medido solo sobre abril y agosto, y los guiones de medidas cerradas que fijan
  `("2026-04", "2026-08")` y no se tocan.
- `knowledge/cases/criterio_fidelidad.yaml`: `construccion: ["2026-04", "2026-07", "2026-08"]`, con
  un comentario; `medida` y los cuatro umbrales, iguales. `tests/unit/test_criterio_fidelidad.py:108`
  lo afirma.
- Lo que el commit deja falso, corregido en él (decisión 8): una NOTA en ADR-0043 («construcción =
  abril y agosto») y otra en ADR-0039 §1, sin reescribir sus cuerpos; `docs/runbooks/ARNES-MOTOR.md`
  y `docs/runbooks/SESION-DE-PREGUNTAS.md`.
- ADR-0078 sale de los bloques `ids-inexistentes` del encargo y de este informe, y entra en el
  índice `docs/adr/README.md` (lo exige `tests/unit/test_adr.py`; el contrato se amplía con él).
- La consecuencia aceptada: `test_huecos_motor.py::test_la_forma_y_la_primitiva_coinciden_en_todas_las_sesiones_de_construccion`
  corre ahora el sesgo H4 sobre las velas de los 13 días de julio, y pasa (ejecutado aparte con
  `-rs`: sin saltar).

## Estado

EN CURSO: fases 1 y 3.a-e hechas; siguen la fase 2 (ADR-0078), 3.f, 4, 5 y 6.
