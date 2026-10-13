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
- **v5** entró con `drive_id` (`fuentes.yaml:33-40`): Aleks lo subió a Drive (la fecha, en `fuentes.yaml`), a la
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
  imagen. Sin `main` en el clon, se salta (y desde el revisor, b3, prueba antes `origin/main`, que
  es lo que tiene la CI).

**La comparación caso a caso** (anexo `docs/validation/anexos/ENTRADA-JULIO/guardia_caso_a_caso.txt`,
la salida del test con `-s`): **100 casos, 5 cambian**, y los cinco son de julio y pasan de
`R_SIN_ABRIR` a legibles: el libro en su carpeta, el vídeo, un texto de la carpeta, el libro suelto
en el material y el libro fuera del corpus. Los otros 95 deciden lo mismo con las dos guardias:
las 26 imágenes (las dos de cada mes) dan `R_CAPTURA` también en julio; febrero, marzo, octubre,
noviembre y diciembre (de 2025 y de 2026) siguen en `R_SIN_ABRIR`; mayo, junio y septiembre en
`R_LIBRO`; enero, abril y agosto, legibles, como en `main`. **Ningún caso que `main` bloqueaba deja
de bloquearse, salvo el material de julio que no es imagen.** Eso va más allá de la letra del
encargo («salvo el libro de julio»): son 5 rutas y no una, porque la regla de la carpeta
(`guardia.py:471`) y la del nombre (`:473`) miran el mes, y meter 2026-07 en la lista abre todo lo
de julio que no es imagen (el vídeo y un texto de su carpeta, y el libro donde esté). Hallazgo b4
del revisor (§14).

**Ampliada el 2026-10-13 tras el revisor (b5):** la matriz suma por mes la grafía real de julio
(carpeta con mayúscula, `backtesting-analytics_<MES>_<año>.xlsx`, un `.mkv` y una `.jpeg`) y un
libro suelto sin «backtesting-analytics» (`operaciones <mes> <año>.csv`, que solo ve la regla de
`guardia.py:473`). **152 casos, 8 cambian**, los ocho de julio y no imagen (los cinco de arriba, el
libro y el `.mkv` con la grafía real, y el `.csv` suelto); las 39 imágenes, `R_CAPTURA` con las dos.
El anexo se regeneró con la misma orden.

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
  medido solo sobre abril y agosto (y, corregido tras el revisor, a1, que las 3 horas perdidas de
  los ticks de julio sí lo usan, por el respaldo M1), y los guiones de medidas cerradas que fijan
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

## 3.f-g La ingesta (2026-10-13)

`uv run botsito casos ingerir --material "corpus/Estrategia del trader/Material adicional de su operativa/Backtest Julio 2026/backtesting-analytics_JULIO_2026.xlsx" --fecha 2026-10-13`:

```
INGESTA: 4 dias del camino de FIDELIDAD no los toma este comando sin `--artefacto` [...] No se han leido ni escrito
INGESTA: 2026-09: hay material declarado y ningun libro atado por su sha. Este comando no lee ningun dia de ese mes, con ningun libro
INGESTA: 10 dias de 2026-06 NO son ingeribles: 2026-06 esta declarado con CERO tramos [...]
INGESTA: 5 filas SIN `initialSL` no produjeron caso: una fila sin stop no es una decision completa. [...]
INGESTA: 13 casos escritos de 13 dias ingeribles; 72 filas leidas; 0 pestanas de agregado abiertas
OK: knowledge/cases/dev/ con 13 casos. Commitealos con `Fuente:`
```

- **13 casos nuevos**, `knowledge/cases/dev/caso-eurusd-2026-07-{01..17}.yaml` (los laborables), y
  ninguno de los que ya había cambia (`git status`: solo los 13 nuevos, sin seguir). Las tres
  primeras líneas son los avisos de siempre, de otros caminos y meses, sin leer nada.
- **5 de las 72 filas no tienen `initialSL`** y no producen caso, como en los otros libros: una fila
  sin stop no es una decisión completa. Se cuentan, no se nombran.
- **La conversión de la hora con Europe/Madrid, comprobada en un caso** (`caso-eurusd-2026-07-01`):
  las entradas de las 06:15:55 y 07:33:05 UTC caen en la sesión `07-11` (08:15 y 09:33 en Madrid)
  y la de las 10:59:05 UTC en la `11-15` (12:59 en Madrid).
- `uv run botsito casos check`: `OK: los casos de la biblioteca tienen la forma declarada y ninguno
  esta reservado`.
- **3.g**: el docstring de `casos_ingerir` (`src/botsito/cli.py:1626`) decía «de los repartos
  commiteados DEL KIT»; ahora nombra también el reparto dev-visto (ADR-0042) y dice «menos los
  ocultos», que es lo que hace `dias_ingeribles`. Solo el docstring: ningún código cambia.

## 4. Fase 4 · los ticks de julio (2026-10-13)

Con el símbolo, la escala y las horas de agosto (`eurusd-ticks-2026-08-75bd3a08`: EURUSD, escala
100.000, horas 05-13 UTC) y `--solo-dias-dev`, que toma los días de `dias_de_construccion` (por eso
va detrás de la fase 2):

`uv run botsito data download-ticks --dataset eurusd-ticks-2026-07 --simbolo EURUSD --escala 100000 --desde 2026-07-01 --hasta 2026-07-31 --solo-dias-dev --horas 05-13 --pausa 2`

```
OK: data/manifests/ticks/eurusd-ticks-2026-07-6e7dc7cd.yaml (eurusd-ticks-2026-07-6e7dc7cd)
  373014 ticks en 13 ficheros; horas presentes 114, ausentes (404) 0, vacias 0, PERDIDAS 3; cotizaciones cruzadas 0
  SELECCION: 13 dias y horas UTC 05-13; el resto del rango no esta en este dataset
```

`uv run botsito data check-ticks --dataset eurusd-ticks-2026-07-6e7dc7cd --hashes`: `OK:
eurusd-ticks-2026-07-6e7dc7cd coincide con el disco (hashes)`.

- **Los 13 días son los del reparto dev-visto** (07-01 a 07-03, 07-06 a 07-10, 07-13 a 07-17), y
  ninguno del 20 al 31: `--hasta 2026-07-31` no trae más porque la selección sale de
  `dias_de_construccion`, que solo ve la partición.
- **Faltan 3 de 117 horas** (13 × 9), listadas en el manifiesto: **2026-07-10 05h, 2026-07-14 12h y
  2026-07-16 11h** UTC, perdidas tras 5 intentos cada una (no son 404 ni horas vacías). Las cubre el
  respaldo M1 del modelo de llenado, como las 7 de abril y las 3 de agosto (`TICKS-LLENADO.md`).
- **Fue la segunda pasada, como en abril y agosto.** La primera (sin `--pausa`) dio el dataset
  `eurusd-ticks-2026-07-7a52cf6d`, con 21 horas perdidas y 321.108 ticks, verificado también con
  `--hashes`; se descartó sin commitear (manifiesto y carpeta borrados antes de estadiar, tras
  comprobar que git no lo seguía), igual que las primeras pasadas de abril y agosto, con 28 horas
  perdidas cada una. La segunda reanuda por la caché cruda y solo vuelve a pedir lo que faltaba.
- Ninguna cotización cruzada. El manifiesto es inmutable desde su commit (`CLAUDE.md`).

## 5. Fase 5 · el vídeo

Hecha dentro de la fase 3 (desviación declarada en §3): v11 a v14 en `fuentes.yaml` con su
`drive_id`, sus bytes (iguales a los de Drive) y su `naturaleza` («backtest de julio del trader en
FX Replay, material de desarrollo», y que la correspondencia con el xlsx es lo que dice el trader,
probable por el orden de grabación pero sin comprobar); en `manifest.yaml` por `corpus inventory`,
con su sha256, duración y audio (§0.d); y en los tests que listan vídeos. No son sesiones: ni
`SESIONES_EN_CUARENTENA` ni `EXCEPCIONES` cambian, y la guardia no los pone en cuarentena (tienen
`drive_id`). La cuarentena por condición del texto se les aplica igual que a todos cuando se
transcriban. **Sin transcripción ni fotogramas en esta rama.**

**La rama que propongo para ellos** (`trabajo/video-julio`): transcribir v11 a v14 (2 h 38 min, los
cuatro con audio) con el guion de `main` y su cuarentena; extraer fotogramas SOLO por instantes
localizados en la transcripción (ADR-0038; las capturas de resumen siguen sin abrirse); comprobar
qué días de julio cubre cada vídeo (lo que dice el trader: v11-v13 del 1 al 17, v14 desde el 20);
comparar el vídeo con el xlsx en los días 1 a 17 (fecha, dirección, entrada y stop de cada
operación que se vea en pantalla, contra el caso); comparar las horas del replay con las del libro,
que es el primero en Europe/Madrid (§3.b); y dejar al consultor la decisión de si se sacan casos del
vídeo para los días 20 a 31 (ADR-0078 §3).

## 6. Fase 6 · la respuesta de FTMO a P-D1

En un fichero nuevo, `docs/validation/FTMO-P-D1.md`, porque RESPUESTAS-FTMO.md es un informe
cerrado (**desviación de la letra de O, aceptada por el consultor**). Paráfrasis, nunca el texto del
correo. En resumen:
- **Hedging** en todas las cuentas de FTMO Global, y **50 lotes** en EURUSD: confirman el perfil.
- **El tope sumado: sin respuesta directa**; una pauta de gestión del riesgo que no es regla.
- **El margen, ya escrito en ADR-0026 «Impacto»**, medido de nuevo: `firma_apalancamiento` no lo
  lee ningún código y el simulador no comprueba el margen; son falsas las descripciones del perfil
  («Lo consume el broker simulado») y de `parametros.yaml` («F21 lo comprueba»). Con todo el saldo
  como margen caben 27,27 lotes a 1,10 y 25,00 a 1,20, y el 0,5 % deja de cumplirse con stops de
  menos de 1,83 y 2,00 pips (anexo `margen_p_d1.py`, que lee el registro y el perfil). **Partir en
  varias órdenes no lo arregla**: la documentación de MT5 dice que en cobertura los volúmenes del
  mismo lado se suman.
- **La prueba**: el CSV de la ejecución 2 ya trae el margen de 1,00 lote (`MargenAlcanza`, script
  1.1); la fórmula predice 100.000 × ask / 30.
- Ningún código ni parámetro cambia.

## 7. Las exposiciones de la rama

- **2026-10-12**: ninguna (fase 0 y fase 1: no se abrió ni se listó nada de julio ni de ningún mes
  reservado; la búsqueda de `MargenAlcanza` que habría entrado en `corpus/` la paró la guardia).
- **2026-10-13**: una fila en `HOLDOUT-EXPOSICIONES.md`: julio, leído entero, en este orden: la
  columna de fechas por Aleks (mínima, máxima y la hora de esas dos filas); el listado y el hash de
  la carpeta `Backtest Julio 2026` (seis capturas de resumen SIN abrir); `dateStart` y `entryPrice`
  de las 72 filas por el anexo del huso; y el detalle por operación de las 72 filas por
  `casos ingerir`. Ninguna partición: julio no tiene ningún día en ninguna.
- **Ninguna foto se abrió**, ni de julio ni de otro mes, ni miniatura; tampoco ningún fotograma ni
  ninguna transcripción de v11 a v14.

## 8. Propuestas para la orden de cierre

Una por línea, para el commit del contrato del cierre (`RITUAL.md`):

- **S sale de la Next Action, HECHA** (a HISTORIA como «Next Action HECHA · S»: lo exige
  `test_hoja_de_ruta.py`, porque R2.1 cita NA:S): «Julio de 2026 entra como material de construcción
  (ADR-0078): libro declarado en Europe/Madrid, reparto dev-visto de los 13 laborables del 1 al 17,
  13 casos, ticks; v11 a v14 en el inventario. Los días 20 a 31 quedan solo en v14».
- **F apunta a lo siguiente según la hoja de ruta**: «Orden de trabajo: lo siguiente es X (R2.2:
  los ticks de invierno por la rejilla, para que enero cuente), que no depende de nada; R2.3 (Q,
  agosto) espera la exportación del trader, y R3.1 depende de R2 entera».
- **R2.1 pasa a HECHA en HOJA-DE-RUTA.md en lo del libro**: «HECHA (`trabajo/entrada-julio`;
  ENTRADA-JULIO.md, ADR-0078): julio es construcción del 1 al 17, con sus ticks; del 20 al 31 no
  hay libro: va a la entrada nueva de abajo».
- **Entrada nueva de la Next Action** (y de la hoja de ruta, en R2): «Julio 20-31: solo en vídeo
  (v14); decidir si se extraen casos del vídeo, tras transcribir v11-v14».
- **Entrada nueva de la Next Action para la rama del vídeo**: «Transcribir v11 a v14 (backtest de
  julio en vídeo, 2 h 38 min, con audio), comprobar qué días cubre cada uno, compararlos con el xlsx
  en los días 1 a 17 y con las horas del libro (el primero en Europe/Madrid); en su rama
  (ENTRADA-JULIO.md §5)». Va antes de la de los días 20-31, que depende de ella.
- **O sale por P-D1** (a HISTORIA como «Next Action HECHA · O»: A.2 de la hoja de ruta cita NA:O):
  «Respondida por FTMO el 2026-10-12 (ticket JSP-CPQRQ-197): hedging y 50 lotes; el tope sumado, sin
  respuesta directa. Registrada en paráfrasis en docs/validation/FTMO-P-D1.md».
- **El texto nuevo del heredado 37**: el de `FTMO-P-D1.md` §4 (el margen corta antes que el volumen:
  1,83 y 2,00 pips a 1,10 y 1,20; partir en órdenes no lo arregla; la ejecución 2 lo comprueba con
  `MargenAlcanza`).
- **Una línea de Technical Debt**: la de `FTMO-P-D1.md` §4 (el simulador no comprueba el margen;
  `firma_apalancamiento` no lo lee nadie; dos descripciones falsas; rama propia con su test).
- **La entrada nueva de la Next Action «Preparar, celebrar y activar la sesión 5 (R4.1)»**, con
  una letra nueva que R4.1 lleve en sus `Refs` (`test_hoja_de_ruta.py`, test a): las 9 «en parte»,
  verificadas contra ACTIVAR-SESION-04.md §0.e/§5 y ACTIVAR-SESION-04-MOTOR.md §5 y §6 -A-13, A-32,
  A-35, la segunda parte de A-43, A-44, A-49, A-50, A-53 y S-14 (la casi plana de RN-007, NA:H)-, y
  las preguntas de los §5: la confirmación bajista de S-13, el último minuto (cuándo se retira una
  orden pendiente a la hora de cerrar), las dos de ADR-0076 §4 (la vela sin cuerpo en el retroceso y
  el breaker contrario que rompe con mecha) y la racha tras la novena pérdida. Y ahora también, de
  esta rama: si el xlsx de julio es la exportación de v11 a v13 (punto 3 de los datos de la fase 3).
  Depende de R1.1, de R3.1 y de que `kit hoja` funcione con un paquete nuevo (NA:J).
- **La guardia y `ffprobe`** (§0.d): junto a K, que `ffprobe` y `ffmpeg -i` sobre un vídeo lean y no
  ejecuten, con un test de los dos sentidos.
- **La guardia y los tests en el clon de `main`** (§9): junto a K, que reconozca como tests los de
  un clon `git worktree add --detach` en `C:/cm/` (la ruta de `comparar-con-main`), para que un test
  de la guardia se pueda probar con el código de `main`; con un test de los dos sentidos.
- **R0.1 y NA:P**: retirada por el consultor (respuesta, «Además»); nada que corregir.

## 9. Tests que rompen a propósito, con el código de `main`

El encargo pide uno, el de la fase 1: «julio se lee; febrero, marzo y diciembre siguen bloqueados,
y las imágenes de la carpeta de julio siguen bloqueadas», roto a propósito en los dos sentidos.

**Lo que se intentó, y lo paró la guardia** (2026-10-13, skill `comparar-con-main`): `git worktree
add --detach C:/cm/main main` (1d37c7a), `tests/unit/test_guardia_claude.py` de la rama copiado
dentro, y `uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider -k "julio or
caso_a_caso or meses_legibles or cita_su_regla"` allí. La guardia de Claude Code lo bloqueó: «el
codigo que se ejecuta pide el corpus SIN FILTRAR». Lo probable, sin medirlo en la guardia: el
fichero de test lleva el literal (`grep -c crudo tests/unit/test_guardia_claude.py`: 1), y dentro
del repo los tests son llamadores autorizados, pero en un clon fuera de `$CLAUDE_PROJECT_DIR` no los
reconoce. **No se rodeó**: el clon se retiró con
`git worktree remove --force C:/cm/main` (con `--force` por el fichero de test copiado, sin
seguir allí) y `git worktree prune`; `git status --short` vacío, `git branch --list` igual
(`main` y la rama) y la lista de worktrees como antes. En `trabajo/activar-sesion-04-motor` el mismo
recorrido sí corrió, y sus ficheros de test no llevan ese literal (`grep -c crudo` sobre
`test_sesgo_h4.py`, `test_huecos_motor.py`, `test_racha_perdidas.py` y `test_kit.py`: 0 cada uno). Propuesta, junto a K (§8): que la
guardia reconozca los tests de un clon `--detach` de `C:/cm/` como reconoce los del repo, con un
test de los dos sentidos.

**Lo que demuestra igual que el código de `main` falla** (sin rodear nada, porque corre en el repo
y lo carga la propia suite):
- `test_la_guardia_frente_a_la_de_main_caso_a_caso` carga la guardia de `main` (`git show
  main:.claude/hooks/guardia.py`, a un fichero de `tmp_path`) y decide con las dos la matriz de 100
  rutas: con la de `main`, el libro, el vídeo, el texto de la carpeta, el libro suelto y el libro
  fuera del corpus de julio dan `R_SIN_ABRIR` (anexo `guardia_caso_a_caso.txt`). Esas cinco rutas son
  justo las que `test_julio_se_lee_y_lo_demas_sigue_cerrado` exige legibles: con la guardia de
  `main`, ese test falla en su primera aserción.
- Y cada sentido roto dentro del propio test, con la guardia de la rama. **Julio se lee**: (1) sin
  2026-07 en `MESES_DE_DESARROLLO` (`monkeypatch`, que reproduce la lista de `main`) el libro y el
  vídeo de julio vuelven a `R_SIN_ABRIR`; (4) con un día de julio en una partición reservada, el
  libro da `R_LIBRO`. **Lo demás sigue cerrado** (añadido el 2026-10-13 tras el revisor, b2: antes
  las dos roturas eran del mismo sentido): (2) con 2026-02, 2026-03 y 2025-12 en la lista, los
  libros de febrero, marzo y diciembre dejan de dar `R_SIN_ABRIR`; (3) sin `.jpeg` ni `.png` en
  `EXT_IMAGEN`, las fotos de julio dejan de dar `R_CAPTURA`. Las comprobaciones de arriba del
  test verían cada cambio.
- **La comparación corre ahora en la CI** (b3): prueba `main` y, si no está, `origin/main`, que
  la CI tiene (`fetch-depth: 0`). En los runs 38325750041 y 38444066133 se había saltado («sin la
  rama main en este clon»). Después del merge compara la guardia consigo misma (`esperados = []`):
  es una prueba de la rama, para revisarla antes del cierre; las guardias permanentes son las de
  `test_julio_se_lee_y_lo_demas_sigue_cerrado` y las del repo real.

`uv run pytest tests/unit/test_guardia_claude.py -q -p no:cacheprovider -k "julio or caso_a_caso
or meses_legibles or cita_su_regla"`, con el test cambiado: 12 pasan, ninguno saltado; y el fichero
entero, en verde dentro de cada `make check` de la rama (§13).

## 10. El encargo, punto por punto

| # | Requisito | Estado | Evidencia |
|---|---|---|---|
| B1 | Abrir con `abrir-rama` desde `main` 1d37c7a, con el tag, la CI de `main` y ninguna otra rama comprobados | Hecho | c17f3ed; «Base, comprobada con git al abrir» |
| B2 | Revisar `/model` | Hecho | Opus 5.5, esfuerzo alto (fase 0) |
| D1 | Repetir en la fase 0 los puntos 1, 2 y 5 de la decisión | Hecho | §0.a (recuentos de `casos_reservados` y `casos_ocultos` por mes, sin ids) |
| N1 | Ni el motor ni la spec | Hecho | `git diff --stat main...HEAD -- src/botsito/engine src/botsito/domain knowledge/spec` vacío (§11) |
| N2 | Ningún umbral de `criterio_fidelidad.yaml`: solo `construccion` | Hecho | §11: el diff del fichero es la lista y su comentario |
| N3 | Ni febrero, ni marzo, ni diciembre, ni días reservados; PREREGISTRO sin rellenar | Hecho | §7; `PREREGISTRO.md` y `holdout/` sin diff (§11); la revisión de fechas, en el revisor |
| N4 | No correr el arnés ni medir cobertura ni precisión | Hecho | ningún `motor arnes` en la rama; solo `test_huecos_motor` dentro de `make check` (§2) |
| N5 | Las fotos de julio no se abren nunca, solo se hashean | Hecho | §0.d (sha256 sin abrir), §7; la guardia `R_CAPTURA` sigue (§1) |
| F0a-c | Inventario de la base, el material y el terreno, con `fichero:linea` | Hecho | e2d2430; §0.a-§0.c |
| F0d | PARADA con las 4 preguntas, respuestas tal cual | Hecho | §«Lo que necesito que decidas»; respuestas del 2026-10-12 y del 2026-10-13, tal cual |
| F1a | 2026-07 en `MESES_DE_DESARROLLO`, con un test que rompe los dos sentidos | Hecho | 10002d9; el otro sentido roto, tras el revisor (b2), en el último commit; §1 y §9 (con `main` en el clon, bloqueado por la guardia: declarado) |
| F1b | Textos vivos: CLAUDE.md, cabecera de `kit/config.yaml`, recuadro en MIRAR-EL-MATERIAL | Hecho | 10002d9; §1 «Los textos» |
| F1c | `libros.yaml`, de solo añadir: su cabecera no se toca y se declara | Hecho | §1 («no se toca»; la línea 15 queda falsa) |
| F1d | Guardia comparada caso a caso con la de `main`: ninguno deja de bloquearse «salvo el libro de julio» | Hecho, más allá de la letra | §1; anexo `guardia_caso_a_caso.txt` (152 casos, 8 cambian, todos de julio y no imagen: no solo el libro, también el vídeo, un texto y el libro suelto, por la regla de la carpeta; b4) |
| F2 | ADR-0078 (siguiente número verificado), cita la decisión, ADR-0043, ADR-0070 §2 y ADR-0042; ningún umbral; antes de cualquier corrida; `Fuente: ADR-0078` | Hecho de otra forma (orden) | 80e7a78; §2. Va después de 3.a-e por la decisión 5 del consultor, porque antes rompía `test_huecos_motor` |
| F3a | `casos_reservados` y `casos_ocultos` de 2026-07 = 0 en el commit que lee | Hecho | 79549c7; §3.a |
| F3b | Huso por velas, UTC y Europe/Madrid, sobre todas las filas, con control de agosto | Hecho | §3.b: Europe/Madrid 71/72 (98,6 %), UTC 5/72 (6,9 %); control de agosto COINCIDE, también con la herramienta de `main` |
| F3c | Entrada en `libros.yaml` (solo añadir) y lectura declarada el mismo día | Hecho | 79549c7; `HOLDOUT-EXPOSICIONES.md`, fila del 2026-10-13 |
| F3d | Tramo de cobertura con mínima, máxima y `material_sha256` | Hecho | `kit/config.yaml`, 2026-07-01..2026-07-17, `a8cb4ef4…` |
| F3e | `casos visto --mes 2026-07` y commit del reparto y su ancla antes de ingerir | Hecho | 79549c7 (13 días dev; ancla `ee78cc0c…`) |
| F3f | `casos ingerir` y `casos check` | Hecho | e959c88; §3.f-g (13 casos; `casos check` OK) |
| F3g | Docstring de `casos_ingerir` | Hecho | e959c88; `src/botsito/cli.py`, solo el docstring |
| F3h | `Fuente: ADR-0078` (y ADR-0042/ADR-0039) en todo commit de `knowledge/cases/` | Hecho de otra forma | 80e7a78 y e959c88 llevan ADR-0078. **79549c7 no** («Fuente: ADR-0042, ADR-0039, ADR-0072») **ni 10002d9** («Fuente: ADR-0072», solo el comentario de `kit/config.yaml`): por la decisión 5 iban antes de la fase 2, cuando ADR-0078 no existía, y un id que no existe hace fallar `knowledge validate`. Cada uno cita el ADR de lo que cambia. No declarado hasta el revisor (b1) |
| F4 | Ticks con el símbolo, la escala y las horas de agosto, `--solo-dias-dev`, `check-ticks --hashes`, horas perdidas contadas | Hecho, con segunda pasada | e959c88; §4: `eurusd-ticks-2026-07-6e7dc7cd`, 3 horas perdidas de 117; la primera pasada (21), descartada sin commitear |
| F5 | El vídeo en el inventario y en los tests; no es sesión; sin transcripción ni fotogramas; duración y rama propuesta | Hecho de otra forma (como v11-v14 y en la fase 3) | 79549c7; §5. Cuatro vídeos y no uno «v5», por los datos de Aleks del 2026-10-13 y la respuesta 4 |
| F6 | FTMO-P-D1 en paráfrasis, el margen medido, la documentación de MT5 citada, el heredado 37 y la prueba de la demo; ni código ni parámetros | Hecho | e959c88; `FTMO-P-D1.md` y su anexo |
| I1 | Informe con fase 0, PARADA, respuestas literales, evidencia por fase y desviaciones | Hecho | este fichero |
| I2 | Las exposiciones del día | Hecho | §7 y `HOLDOUT-EXPOSICIONES.md` |
| I3 | Las propuestas de cierre, una por línea | Hecho | §8 (con 9 «en parte», no 8: la lista del encargo nombra nueve; respuesta, «Además») |
| I4 | Tamaño de `PROJECT_STATE.md` | Hecho | §12 |
| T1 | `make check` sellado antes de cada commit, nunca `--no-verify` | Hecho | seis commits, todos por los hooks |
| T2 | Si cambia el Makefile o se niega un push, parar | No hizo falta | el Makefile no cambia (§11); los pushes salieron desde la sesión |
| T3 | `fix/entrada-julio` y CI de Linux, con los números de run | Hecho | §13 (el run del último commit, en el mensaje final: este informe va en ese commit) |
| R1 | Revisor con su informe pegado, con el alcance del encargo | Hecho | §14 |

**Desviaciones declaradas** (todas en su sección): la fase 2 después de 3.a-e (decisión 5); el vídeo
como v11-v14 y en el commit de la fase 3 (respuesta 4 y datos del 2026-10-13); el tramo de julio
del 1 al 17 (decisión del consultor del 2026-10-13); FTMO-P-D1 en un fichero nuevo (aceptado); la
segunda pasada de ticks (§4); el test con `main` en el clon, que bloqueó la guardia (§9); y, tras
el revisor, el trailer de 79549c7 y 10002d9 sin ADR-0078 (F3h) y la comparación que abre 5 rutas de
julio y no solo el libro (F1d).

## 11. Lo que NO cambia, medido

`git diff --stat main...HEAD -- src/botsito/engine src/botsito/domain knowledge/spec Makefile
knowledge/cases/holdout knowledge/cases/meses_reservados.yaml knowledge/evidence knowledge/feedback
docs/validation/RESPUESTAS-FTMO.md docs/validation/PREREGISTRO.md knowledge/cuentas`: **vacío**.

`git diff main...HEAD -- knowledge/cases/criterio_fidelidad.yaml`: solo la lista y su comentario:

```
-construccion: ["2026-04", "2026-08"]
+# Julio, del 1 al 17 (lo que cubre su libro), desde ADR-0078 (2026-10-13): decidido ANTES de
+# cualquier corrida del arnes que lo incluya; ningun umbral cambia.
+construccion: ["2026-04", "2026-07", "2026-08"]
```

`uv run python scripts/contrato_rama.py`: «CONTRATO: 50 ficheros dentro del contrato de
trabajo/entrada-julio (riesgo alto, artefacto docs/validation/ENTRADA-JULIO.md, tramo 'R2', 6
comprobaciones para el revisor)». `git diff --stat main...HEAD`: 50 ficheros, 2708 líneas más y 42
menos (antes de este último commit del informe).

## 12. Tamaño de `PROJECT_STATE.md`

`wc -c PROJECT_STATE.md`: **22.172 bytes** (en `main`, 21.908: la rama suma 264, en `Current
Branch` y `Current Feature`, en «Tests Currently Passing», 1526 → 1529, y en las dos líneas
«ninguna desde el Archivo 30» → «Archivo 31»; corregido tras el revisor, a3). El tope es el de `tests/unit/test_project_state.py:21`, `TOPE_BYTES =
25_000`: quedan 2.828. El encargo no fija otro.

## 13. CI de Linux

Toca `.claude/` (la guardia), así que va por `fix/entrada-julio` (`RITUAL.md`). Los pushes salieron
desde la sesión con `git push origin trabajo/entrada-julio:fix/entrada-julio`, sin que el
clasificador negara ninguno.

- **Run 38325750041**, sobre 10002d91fce72051c50421de8384711bb8da1b19 (la fase 1, la guardia):
  `1 failed, 2604 passed, 10 skipped in 229.99s`; el único fallo es el aceptado,
  `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (`gh run view 38325750041
  --log-failed`).
- **Run 38444066133**, sobre e959c88be2e7f5dfb19f89e81ece932790e86f32 (la ingesta, los ticks y
  FTMO-P-D1): `1 failed, 2604 passed, 10 skipped in 295.76s`; el único fallo es el aceptado,
  `tests/unit/test_cli.py::test_state_check_ok_on_real_repo` (`gh run view 38444066133
  --log-failed`; API de check-runs con el sha literal: `python completed failure`). Uno de los 10
  saltados era la comparación caso a caso, sin `main` local (b3, arreglado en el commit siguiente).
- El run del commit con los arreglos del revisor (§14), con su número, en el mensaje final de la
  sesión: este informe va dentro de ese commit y no puede llevar su propio run.

## 14. Informe del revisor

Lanzado el 2026-10-13 (subagente `revisor`) sobre e959c88 más §9-§13 sin commitear, con el alcance
del encargo (la comparación caso a caso, ninguna foto abierta, ninguna fecha reservada en lo
commiteado). Se pega tal cual: no cita ningún tramo no citable (0 retiradas).

### 14.1 Lo que se hizo con cada hallazgo

| # | Gravedad | Qué se hizo |
|---|---|---|
| a1 | importa | **Arreglado.** ADR-0078 (Impacto) dice ahora que las 3 horas perdidas de `eurusd-ticks-2026-07-6e7dc7cd` van por el respaldo M1 con el spread supuesto de ADR-0051 §6. El ADR es de esta rama y no está en `main`: se corrige antes del cierre, como pide el revisor; §2 lo dice. |
| a2 | menor | **Arreglado en el informe; queda en la historia.** La fecha era la de la subida de v5 a Drive (`fuentes.yaml`, ya en `main`), no un día operado; §0.b remite ahora a `fuentes.yaml` sin escribirla. En el commit e2d2430 sigue estando: la historia no se reescribe. Las 2 de `HISTORIA.md` son la copia literal del PROJECT_STATE de `main` que exige el Archivo. |
| a3 | menor | **Arreglado** en §12: nombra también «Tests Currently Passing» y las dos líneas del Archivo. |
| a4 | menor | **Arreglado** en `FTMO-P-D1.md` §2 y §4: «ningún código del bot» (`src/`, `scripts/`, `tools/`: 0 apariciones, medido de nuevo), y que lo lee solo el anexo de la medida. |
| b1 | importa | **Declarado** en §10 (F3h, «Hecho de otra forma») y en las desviaciones: 79549c7 y 10002d9 no llevan ADR-0078 porque iban antes de la fase 2 (decisión 5) y un id inexistente rompe `knowledge validate`; cada uno cita el ADR de lo que cambia. Los commits no se reescriben. |
| b2 | importa | **Arreglado** en `test_julio_se_lee_y_lo_demas_sigue_cerrado`: dos roturas del otro sentido, (2) febrero, marzo y diciembre en la lista los abren y (3) sin `.jpeg`/`.png` en `EXT_IMAGEN` las fotos de julio se abren; la del día reservado pasa a ser la (4). 12 pasan (§9). |
| b3 | importa | **Arreglado**: la comparación prueba `main` y después `origin/main`, que tiene la CI (`fetch-depth: 0`); el run del commit de los arreglos dirá si ya no se salta (mensaje final). Que después del merge se compare consigo misma queda dicho en §9: es una prueba de la rama. |
| b4 | importa | **Declarado** en §1 y en §10 (F1d, «Hecho, más allá de la letra»): dejan de bloquearse 5 rutas de julio, no solo el libro (8 con la matriz ampliada), todas de julio y ninguna imagen, por la regla de la carpeta (`guardia.py:471`). |
| b5 | menor | **Arreglado**: la matriz suma la grafía real de julio (carpeta con mayúscula, libro con guiones bajos, `.mkv`, `.jpeg`) y un `.csv` suelto sin «backtesting-analytics» (la regla de `:473`). 152 casos, 8 cambian; el anexo se regeneró. Decidir por comandos y no solo por `motivo_fichero` ya lo hacen los otros tests de la guardia; no se repite aquí. |
| b6 | menor | **Arreglado**: T3 y R1 se rellenan con este commit, y §13 dice dónde va el run del último. |

«Lo que no pude comprobar», punto 1 (la guardia sobre las rutas reales de julio): la matriz cubre
ahora la grafía real con rutas sintéticas (b5); la ruta real de una foto de julio ya está en
`test_cada_bloqueo_cita_su_regla_en_el_repo_real` (§1). Punto 2 (que la sesión no abriera ninguna
foto): lo afirma la sesión en §7; ningún Read ni ningún comando sobre una imagen, y la guardia
habría parado cualquiera (`R_CAPTURA`).

### 14.2 El informe, tal cual

> ## Informe del revisor · trabajo/entrada-julio · 2026-10-13
>
> Base: `git merge-base main HEAD` = 1d37c7a. Seis commits (c17f3ed, e2d2430, 10002d9, 79549c7, 80e7a78, e959c88). Sin commitear queda solo `docs/validation/ENTRADA-JULIO.md` (§9 a §13). Contrato: `contrato.yaml`. Informe: `docs/validation/ENTRADA-JULIO.md`.
>
> ### Eje (a) · Reglas de la casa
> Resumen: 0 bloquea, 1 importa, 3 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | a1 | importa | ADR-0078 dice que los días de julio no usan el spread supuesto del respaldo, y no es verdad. Hay 3 horas perdidas que van por el respaldo M1, y ese respaldo usa el spread supuesto de §6. El propio informe lo cuenta. | `docs/adr/0078-julio-entra-en-construccion.md:89-91`: «está medido sobre los ticks de abril y agosto y NO se rehace aquí: con ticks de julio, los días de julio no lo usan». En cambio, `ENTRADA-JULIO.md:595-597`: «Faltan 3 de 117 horas … Las cubre el respaldo M1 del modelo de llenado». ADR-0051:73-75: el minuto sin ticks va «con la vela M1 BID del repositorio y el spread supuesto de §6». Las tres horas están en `data/manifests/ticks/eurusd-ticks-2026-07-6e7dc7cd.yaml:91-94`. El ADR es inmutable una vez commiteado: si se corrige aquí, tiene que ser antes del cierre. |
> | a2 | menor | Una fecha de septiembre que coincide con un día reservado aparece en lo commiteado. Es la fecha en que v5 se subió a Drive, no un día operado, y ya está en `main`. | Al contar con `casos_reservados`/`casos_ocultos`, sin imprimir fechas, sale 1 aparición en `docs/validation/ENTRADA-JULIO.md:145` (formato iso, mes 2026-09). Esa misma fecha ya está en `main` en `knowledge/corpus/fuentes.yaml` (1 vez) y en 4 informes de `docs/validation/`. Las otras 2 apariciones (`docs/state/HISTORIA.md:8852` y `:8855`) son copia literal del PROJECT_STATE de `main` («línea idéntica en PROJECT_STATE de main: True»), que el Archivo exige. |
> | a3 | menor | §12 dice que el PROJECT_STATE solo suma `Current Branch` y `Current Feature`. Cambian también otras líneas. | En `git diff main...HEAD -- PROJECT_STATE.md` cambian además «Tests Currently Passing» (1526 → 1529) y las dos líneas «ninguna desde el Archivo 30» → «Archivo 31». La cifra de bytes sí es correcta (22172 frente a 21908). |
> | a4 | menor | FTMO-P-D1 dice que `firma_apalancamiento` «aparece solo» en parametros.yaml y en el perfil, y que «no lo lee ningún código». Lo lee el anexo de la propia rama. | `docs/validation/FTMO-P-D1.md:43-44`. En cambio, `docs/validation/anexos/ENTRADA-JULIO/margen_p_d1.py:45` hace `perfil.entero("firma_apalancamiento")`. Para `src/`, `scripts/` y `tools/` la afirmación sí se cumple (el grep no da nada). El texto propuesto para el heredado 37 (`FTMO-P-D1.md:103`) repite lo mismo. |
>
> Comprobado sin hallazgos:
> - **Contrato.** `scripts/contrato_rama.py` da «CONTRATO: 50 ficheros dentro del contrato …», con exit 0.
> - **Guardia.** `pytest tests/unit/test_guardia_claude.py -q` sale con exit 0. Las pruebas de julio, caso a caso, meses legibles y regla citada: 12 passed y ninguna saltada.
> - **Comprobaciones de la rama.** `casos check` da OK. `check-ticks --dataset eurusd-ticks-2026-07-6e7dc7cd --hashes` da OK. `knowledge validate`, ejecutado sin redirigir, da OK en todo; sus AVISOS son los ya conocidos.
> - **make check.** El `make-check.log` trae `SELLO … 76ed8e25…`, que es igual a `git rev-parse HEAD^{tree}`; 2615 passed; `PICO DE MEMORIA … 295 MiB`.
> - **Trailers.** Los 4 commits que tocan `knowledge/cases` llevan `Fuente:` en el cuerpo, y los ids existen: ADR-0039, 0042, 0051, 0072 y 0078.
> - **Regímenes de cambio.** `data/manifests` solo tiene `A`. `libros.yaml` suma 16 líneas y no quita ninguna. No hay nada en evidence, feedback, transcripciones, fotogramas, spec, holdout, engine, domain, Makefile, config, cuentas ni plan.
> - **Holdout.** Ningún fichero de holdout cambia. Hay fila en HOLDOUT-EXPOSICIONES del 2026-10-13, el mismo día de la lectura (79549c7 y e959c88 son de esa fecha).
> - **Fechas reservadas.** Las 34 de `casos_reservados` y `casos_ocultos` (todas de 05, 06 y 09) aparecen 0 veces en los mensajes de commit, 0 en los nombres de fichero, 0 escritas con palabras o como dd/mm, y 0 días de 2026-02 o 2026-03.
> - **Rastro de imágenes.** En las líneas añadidas no hay ningún término de Analytics (win rate, PnL, profit factor, drawdown, balance, equity). El manifiesto solo trae nombre, bytes y sha de las 6 capturas.
> - **ADR.** 0078 tiene `## Estado` ACTIVE. 0039 y 0043 solo reciben NOTAs, sin tocar el cuerpo.
> - **Informes cerrados.** Ningún informe cerrado de `main` cambia, salvo la fila añadida a HOLDOUT-EXPOSICIONES.
> - **Spec.** No cambian ni la spec ni las citas, así que las tres guardias de `cita` no aplican.
> - **HISTORIA.** El Archivo 31 contiene entero el PROJECT_STATE de `main`, y no se quita ninguna línea.
> - **Citas revisadas.** Las comprobé contra su fuente y aguantan: HOLDOUT-EXPOSICIONES:40, vistos.yaml:60-64, ADR-0073 §5 (líneas 70-77), test_huecos_motor.py:300-310, parametros.yaml:1821/1828, perfil:270/276 y ADR-0026:118-123.
> - **Cifras del margen.** Rehice la aritmética y cuadra: 3666,67 USD; 27,27 lotes; 1,83 pips. Y 25,00 lotes; 2,00 pips.
>
> ### Eje (b) · Encargo
> Resumen: 0 bloquea, 4 importa, 2 menor. Requisitos: 35 hechos, 2 parciales, 0 no hechos, 2 hechos de otra forma (uno declarado y otro no), 2 pendientes de entrega.
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Abrir con abrir-rama desde 1d37c7a; encargo, contrato, Archivo | Hecho | c17f3ed; el Archivo 31 coincide con el PS de main |
> | 2 | Revisar /model | Hecho (declarado, no verificable) | ENTRADA-JULIO.md:20 |
> | 3 | F0a: puntos 1, 2 y 5 | Hecho | §0.a, líneas 31-47 |
> | 4 | F0b: ruta, nombres, tamaños y sha256 sin abrir | Hecho | §0.d, tabla en las líneas 427-439; coincide con el diff de manifest.yaml |
> | 5 | F0c: terreno con fichero:línea | Hecho | §0.c |
> | 6 | F0d: PARADA con 4 preguntas y respuestas tal cual | Hecho | `diff` de los dos bloques del encargo y del informe: PARADA_IGUAL y DATOS_IGUAL |
> | 7 | F1: 2026-07 en MESES_DE_DESARROLLO | Hecho | guardia.py:211 |
> | 8 | F1: test que rompe a propósito los dos sentidos | Parcial | ver b2 |
> | 9 | F1: CLAUDE.md, cabecera de kit/config.yaml y recuadro en MIRAR-EL-MATERIAL | Hecho | diff de los tres ficheros |
> | 10 | F1: cabecera de libros.yaml sin tocar y declarado | Hecho | numstat 16/0; §1, líneas 403-405 |
> | 11 | F1: caso a caso, «salvo el libro de julio» | Hecho de otra forma, no declarado | ver b3 y b4 |
> | 12 | F2: número 0078 verificado | Hecho | adr/README.md: 0077 era el último |
> | 13 | F2: cita la decisión, ADR-0043, ADR-0070 §2 y ADR-0042 | Hecho | ADR-0078:9-11, 53-54 y 20-26 |
> | 14 | F2: ningún umbral cambia y es anterior a la corrida; que lo diga | Hecho | ADR-0078:12-13 y 17-19; diff de criterio_fidelidad.yaml |
> | 15 | F2: commit con `Fuente: ADR-0078` | Hecho | 80e7a78 |
> | 16 | F3a: recuento 0 en el commit que lee | Hecho | huso_julio.py:61-67; §3.a |
> | 17 | F3b: huso por velas, UTC y Madrid, control de agosto | Hecho | huso_julio.txt: 71/72 y 5/72; control COINCIDE; control_herramienta_agosto.txt |
> | 18 | F3c: libros.yaml y exposición el mismo día | Hecho | diff de libros.yaml (`declarado_el` 2026-10-13); fila de HOLDOUT del 2026-10-13 con el nombre del fichero |
> | 19 | F3d: tramo con mínima, máxima y sha | Hecho | kit/config.yaml, julio 01..17, `a8cb4ef4…` |
> | 20 | F3e: reparto y ancla commiteados antes de ingerir | Hecho | 79549c7 va antes que e959c88; ancla `ee78cc0c…` |
> | 21 | F3f: ingerir y casos check | Hecho | 13 casos, todos `A`; `casos check` OK, ejecutado por mí |
> | 22 | F3g: docstring | Hecho | cli.py:1626-1628 |
> | 23 | F3: `Fuente: ADR-0078` en todo commit de knowledge/cases | Parcial | ver b1 |
> | 24 | F4: ticks con los parámetros de agosto, `--solo-dias-dev`, `--hashes`, horas perdidas contadas | Hecho | manifiesto: 13 días, horas 5-13, 3 perdidas; `check-ticks` OK |
> | 25 | Datos: ticks solo de los días 1-17 | Hecho | manifiesto, `seleccion.dias`: 13 días, ninguno a partir del 20 |
> | 26 | F5: vídeo al inventario y tests; no es sesión; sin transcripción; duración; rama propuesta | Hecho de otra forma (declarado) | §3, líneas 456-462; §5 |
> | 27 | Datos: bytes en disco iguales a los de Drive | Hecho | §0.d frente a los datos de Aleks: los 4 coinciden |
> | 28 | Datos: en fuentes.yaml, «probable pero no lo prueba» | Hecho | `naturaleza` de v11 a v14: «no comprobado» |
> | 29 | Datos: tramo 1-17, días 20-31 fuera y el porqué en el informe y en ADR-0078 | Hecho | ADR-0078:20-32; §3.d |
> | 30 | F6: paráfrasis, consumo de `firma_apalancamiento`, margen, doc de MT5, heredado 37, prueba en la demo, ni código ni parámetros | Hecho | FTMO-P-D1.md; ver a4 |
> | 31 | Decisión 10: ADR-0026 como origen, las dos falsedades, línea de Technical Debt | Hecho | FTMO-P-D1.md:36-51 y 106-111 |
> | 32 | Decisión 8: los textos de la guardia, ARNES-MOTOR, SESION-DE-PREGUNTAS y NOTA en ADR-0043 | Hecho | diffs de 10002d9 y 80e7a78 |
> | 33 | Decisión 9: NOTA en ADR-0039 §1 | Hecho | diff de 80e7a78 |
> | 34 | Decisión 7: en el manifiesto solo entra julio | Hecho | diff de manifest.yaml: solo `Backtest Julio 2026` |
> | 35 | Propuestas para el cierre (todas las listadas, con las 9 «en parte») | Hecho | §8; lista comprobada contra ACTIVAR-SESION-04.md:789-791 |
> | 36 | Tamaño de PROJECT_STATE | Hecho | §12; ver a3 |
> | 37 | No tocar motor, spec, umbrales, febrero, marzo, diciembre ni PREREGISTRO; no correr el arnés; no abrir fotos | Hecho | name-status vacío en esas rutas; ningún rastro en lo commiteado |
> | 38 | make check con sello antes de cada commit | Hecho (verificado solo el último) | SELLO = árbol de HEAD |
> | 39 | CI de `fix/entrada-julio` con números de run | Hecho; el informe no está al día | 38325750041 y 38444066133. Este último ya terminó: `headSha e959c88…`, «1 failed, 2604 passed, 10 skipped», y el único fallo es `test_state_check_ok_on_real_repo` («PROJECT_STATE declara la rama 'trabajo/entrada-julio'; la rama actual es 'fix/entrada-julio'»). §13 sigue diciendo PENDIENTE_RUN. |
> | 40 | Revisor pegado en §14 | Pendiente | lo hace la sesión |
> | 41 | «Rama lista para revisión, NO cerrada» | Pendiente | `## Estado` dice EN CURSO |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | b1 | importa | El encargo pide `Fuente: ADR-0078` en todo commit que toque `knowledge/cases/`. 79549c7 no lo lleva, y 10002d9 tampoco. Aun así, la fila F3h del informe da «Hecho» y cita 79549c7. Hay causa: con el orden de la decisión 5, ADR-0078 aún no existía. Pero la desviación no está declarada. | `git log … -- knowledge/cases`: 79549c7 lleva «Fuente: ADR-0042, ADR-0039, ADR-0072» y toca kit/config.yaml y visto/; 10002d9 lleva «Fuente: ADR-0072» y toca kit/config.yaml. ENTRADA-JULIO.md:762 dice «F3h … Hecho \| 79549c7, 80e7a78, e959c88». |
> | b2 | importa | «Los dos sentidos, rotos a propósito» no es lo que hace el test: las dos roturas son del mismo sentido. Las dos cierran julio (sin julio en la lista, o con un día de julio reservado). El otro sentido (febrero, marzo, diciembre y las imágenes siguen cerradas) nunca se rompe para ver que el test lo detecta. Y la prueba con el código de `main` en el clon no corrió (§9, la paró la guardia). | `tests/unit/test_guardia_claude.py:223-233`: los dos «Roto a proposito» afirman `R_SIN_ABRIR` o `R_LIBRO` sobre el libro de julio. ENTRADA-JULIO.md:366-371 y :728-731 lo presentan como «los dos sentidos y los dos rotos a propósito». |
> | b3 | importa | La comparación caso a caso no corre en la CI de Linux. Además, después del merge pasa a comparar la guardia consigo misma (`esperados = []`), así que solo prueba algo en el Windows de la rama y antes del cierre. El informe dice «Sin `main` en el clon, se salta», pero no dice que en las dos CI de la rama se saltó. | En los dos runs, `gh run view 38325750041 --log` y `38444066133 --log-failed` dan «SKIPPED [1] tests/unit/test_guardia_claude.py:414: sin la rama main en este clon». El checkout usa `fetch-depth: 0`, pero no crea la rama local `main`. Ver también `test_guardia_claude.py:439-440`. |
> | b4 | importa | El encargo dice «ningún caso que bloqueaba deja de bloquearse, salvo el libro de julio». En la rama dejan de bloquearse 5: el libro en su carpeta, el vídeo, un texto de la carpeta, el libro suelto en el material y el libro fuera del corpus. Es consecuencia directa de añadir 2026-07 a la lista (la regla de carpeta, guardia.py:471), pero el informe da F1d como «Hecho» sin decir que va más allá de la letra. | Encargo:54. `guardia_caso_a_caso.txt:54-60`. ENTRADA-JULIO.md:753 y :391 («salvo el material de julio que no es imagen»). |
> | b5 | menor | A la matriz le faltan casos. No pasa por la rama de guardia.py:473: un libro de julio sin «backtesting-analytics» en el nombre (por ejemplo un `.csv` suelto). Tampoco prueba los nombres reales: carpeta con J mayúscula, libro con guiones bajos y vídeos `.mkv`. Solo decide por `motivo_fichero`, no por comandos. Visto el diff, que solo cambia la tupla y textos, el riesgo es bajo. | `test_guardia_claude.py`, `_matriz_de_material`: nombres fijos `backtesting-analytics {MES} {año}.xlsx`, `video.mp4`, carpeta `Backtest julio 2026`. Los usos de `meses_legibles` están en guardia.py:434, :471 y :473. |
> | b6 | menor | La tabla de §10 da como «Hecho» la CI (T3) y el revisor (R1) cuando el árbol aún tenía PENDIENTE_RUN y no existía §14. | ENTRADA-JULIO.md:772-773 frente a :816-817 y :821-822. |
>
> Lo que la rama hace y el encargo no pide, todo justificado en el informe:
> - los dos tests de contrato `test_libros.py` y `test_mes_del_material.py` (§3, líneas 514-519);
> - el v11 → v15 sintético de `test_cuarentena.py` (§3);
> - reescribir entero el comentario de kit/config.yaml, no solo «quién lee» (§1, líneas 398-400);
> - las propuestas sobre `ffprobe` y sobre los tests en `C:/cm/` (§0.d, §8 y §9).
>
> Lo que el encargo dice que no se toca: comprobado con el diff (fila 37).
>
> ### Lo que no pude comprobar
> - **La guardia de la rama sobre las rutas REALES de julio** (`Backtest Julio 2026`, `backtesting-analytics_JULIO_2026.xlsx`, los `.mkv` y las 6 `.jpeg`). La guardia bloqueó mi `python -c` porque nombra la carpeta: «el codigo nombra la carpeta … que contiene material protegido». No lo rodeé. Leyendo el código: `_normcase` y `mes_de` (`\D{0,3}`) lo tratarían como julio, y `EXT_IMAGEN` pone R_CAPTURA a cualquier `.jpeg`. Pero no lo ejecuté.
> - **Que en la sesión no se abriera ninguna foto.** Solo puedo comprobar lo commiteado (sin rastro). No veo el historial de herramientas de la sesión.
> - **Que FTMO-P-D1 no copie el correo.** No tengo el correo. Lo comparé con la paráfrasis del consultor en el encargo (líneas 83-85) y coincide; no hay texto en inglés salvo las dos citas de la documentación de MT5.
> - **La documentación de MT5 citada** (metatrader5.com): no tengo acceso a la red para leerla.
> - **`make check` y `git write-tree`**: escriben, así que no los ejecuté. La evidencia es el `make-check.log` (SELLO sobre el árbol de HEAD, 2615 passed, PICO 295 MiB). El cambio sin commitear de ENTRADA-JULIO.md no está sellado: necesita su propio make check.
> - **`knowledge validate > knowledge-validate.log`**: la ejecuté sin la redirección, porque la redirección escribe.
> - **`recuento_julio.py`** (guion de la carpeta de trabajo) no está en el repo: no pude ver su código.
> - **Que cada commit intermedio se sellara**: los hooks lo exigen, pero solo pude comprobar el sello del último.
>
> ### Comandos ejecutados
> 1. `git branch --show-current && git merge-base main HEAD && git log --format='%h %s' main..HEAD && git status --short`
> 2. `git diff --stat main...HEAD`
> 3. Read de `docs/encargos/trabajo-entrada-julio.md`, `contrato.yaml` y `docs/validation/ENTRADA-JULIO.md` (entero)
> 4. `uv run python scripts/contrato_rama.py`
> 5. `git diff main...HEAD -- .claude/hooks/guardia.py`
> 6. `uv run pytest tests/unit/test_guardia_claude.py -q` (y `-rs -p no:cacheprovider`, exit 0)
> 7. Read de `docs/validation/anexos/ENTRADA-JULIO/guardia_caso_a_caso.txt`
> 8. (bloqueado por solo_lectura: pytest con redirección a la carpeta de trabajo)
> 9. `uv run pytest tests/unit/test_guardia_claude.py -v -p no:cacheprovider -k "julio or caso_a_caso or meses_legibles or cita_su_regla"`: 12 passed
> 10. `git diff main...HEAD -- tests/unit/test_guardia_claude.py`
> 11. Grep de `MESES_DE_DESARROLLO|meses_legibles` en guardia.py; Read de guardia.py:215-494
> 12. (bloqueado por la guardia: `python -c` con las rutas reales de julio)
> 13. Grep de `def casos_reservados|casos_ocultos` en src
> 14. `uv run python -c` (recuento de fechas reservadas en el diff, sin imprimirlas); después su localización por fichero:línea; después la comparación con PS y fuentes.yaml de main; después mensajes de commit y nombres de fichero; después fechas escritas con palabras o dd/mm
> 15. `git diff main...HEAD | grep -E '^\+' | grep -inE 'win ?rate|…|balance'`
> 16. `git diff main...HEAD -- knowledge/corpus/manifest.yaml knowledge/corpus/fuentes.yaml knowledge/corpus/libros.yaml docs/validation/HOLDOUT-EXPOSICIONES.md`
> 17. Read de `huso_julio.py`, `huso_julio.txt` y `control_herramienta_agosto.txt`
> 18. Read de `knowledge/cases/dev/caso-eurusd-2026-07-01.yaml`; `git diff main...HEAD -- knowledge/cases/kit/config.yaml knowledge/cases/visto knowledge/cases/criterio_fidelidad.yaml`; `git show main:knowledge/cases/dev/caso-eurusd-2026-08-03.yaml | head -30`
> 19. `git log --format='=== %h %ad %s%n%b' --date=iso main..HEAD -- knowledge/spec knowledge/cases`
> 20. `ls docs/adr | grep …`; `git show --stat … 10002d9 79549c7 80e7a78 e959c88 e2d2430 c17f3ed`
> 21. `git show 80e7a78 -- <encargo, ADR-0043, ADR-0039, runbooks, README, test_criterio_fidelidad>`
> 22. Read de `docs/adr/0078-julio-entra-en-construccion.md`
> 23. `grep -c ': dev' knowledge/cases/visto/2026-0{4,8,7}/particiones.yaml`; `grep -n -i 'spread|respaldo' docs/adr/0051-*.md`
> 24. Grep de `julio` en PROJECT_STATE.md
> 25. `git diff main...HEAD -- PROJECT_STATE.md CLAUDE.md docs/runbooks/MIRAR-EL-MATERIAL.md src/botsito/cli.py tests/contract tests/unit/test_inventario.py tests/unit/test_cuarentena.py`
> 26. `wc -c PROJECT_STATE.md`; `git show main:PROJECT_STATE.md | wc -c`; `tail` y `grep` de `make-check.log`
> 27. `git rev-parse HEAD^{tree}`; `git log -1 --format='%h %ad' --date=iso HEAD`
> 28. (bloqueado por la guardia: `casos check` y `check-ticks` encadenados); después `uv run botsito casos check`; `uv run botsito data check-ticks --dataset eurusd-ticks-2026-07-6e7dc7cd --hashes`; `uv run botsito knowledge validate`
> 29. `git diff --name-status main...HEAD -- <rutas inmutables y protegidas>`; `git diff --numstat … libros.yaml`; `git diff --name-status … docs/validation/ docs/adr/`
> 30. Read de `data/manifests/ticks/eurusd-ticks-2026-07-6e7dc7cd.yaml`
> 31. Read de `docs/validation/FTMO-P-D1.md`
> 32. `grep -rn firma_apalancamiento src scripts tools`; `sed -n` de parametros.yaml, del perfil y de ADR-0026; `grep -n` de las líneas citadas y de `MedirDemoFTMO.mq5`
> 33. `sed -n` de HOLDOUT-EXPOSICIONES.md:40, vistos.yaml:60-64, test_huecos_motor.py:300-310 y ADR-0073:70-77
> 34. `ls .claude/skills/`; `grep -n` de entregar-rama/SKILL.md
> 35. `grep -n -A4 checkout .github/workflows/*.yml`
> 36. `gh run view 38325750041 --log | grep …`; `gh run view 38444066133`; `gh run view 38444066133 --log-failed | grep …` (dos veces); `gh run view 38444066133 --json headSha,conclusion,headBranch`
> 37. `diff` de los bloques de respuesta (encargo frente a informe)
> 38. `git diff c17f3ed HEAD -- docs/encargos/trabajo-entrada-julio.md | grep '^-'`
> 39. `grep -n -i "en parte"` en ACTIVAR-SESION-04*.md; `sed -n '787,793p' docs/validation/ACTIVAR-SESION-04.md`
> 40. `grep -n "R2\.[123]" docs/plan/HOJA-DE-RUTA.md`
> 41. `uv run python -c` (comprobación de que el Archivo 31 de HISTORIA contiene el PS de main)
> 42. `git diff --name-status main...HEAD -- knowledge/cases | …`
> 43. Read de `docs/validation/anexos/ENTRADA-JULIO/margen_p_d1.py`

## Estado

LISTA PARA REVISIÓN (2026-10-13): fases 0 a 6 hechas en el orden aprobado (1 → 3.a-e → 2 →
3.f-g → 4 → 5 → 6); el revisor pasó (0 bloquea, 5 importa, 5 menor) y cada hallazgo está arreglado
o declarado (§14.1); CI de Linux en `fix/entrada-julio` con el único fallo aceptado (§13). Lo que
queda es del consultor: la revisión, y las propuestas de §8 para la orden de cierre.

Rama lista para revisión, NO cerrada.
