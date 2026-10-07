# Activación de A-42 con H2b: las sesiones son velas H4 de la rejilla

Rama `trabajo/activacion-a42`, abierta el 2026-10-06 desde `main` en e97af27 (commit de estado tras
`stable/F37c-reloj-invierno`, merge 49c3098). Encargo: `docs/encargos/trabajo-activacion-a42.md`.
Parte de la medida de `docs/validation/RELOJ-INVIERNO.md` (Next Action E).

**Este informe llega hasta la PARADA de la fase 0.** Fuera de él, de sus anexos, de la fila de
HOLDOUT-EXPOSICIONES y de los ficheros de apertura de la rama, no se ha cambiado nada del
repositorio. Fuera del repositorio se rehicieron las cuatro filtradas de sesión, como pide el punto
b (§2.2).

## 0. Resumen de la fase 0

| Punto | Resultado |
|---|---|
| a. Las 8 capturas | Están las 8, con su nombre y tamaño (§1.1). **Los literales NO se han verificado: la guardia de Claude Code bloquea abrir cualquier imagen del material adicional** (§1.2). Decide el consultor (§6, D1). |
| b. Los dos pendientes | Texto literal en §2.1. El (1), hecho: las filtradas de v7–v10 rehechas con `--solo-filtrar --video` y medidas por marcas; **ninguna diferencia** (§2.2). El (2) es de la fase 1, paso 4. |
| c. Lo que depende del reloj de las sesiones | §3. Más sitios que los del encargo dicen «UTC+2 fijo»: `CLAUDE.md`, ENTRADA-MARZO (B0), ADR-0017 y el README de runbooks (§3.5). |
| d. La rejilla en las dos semanas de 2024 | El guion de M4 da 22:00 y velas a las 14:00 la semana del 27 de octubre, y 23:00 y velas a las 15:00 la del 3 de noviembre, en un eje Europe/Madrid. **Coincide con la lectura del consultor del §12 de RELOJ-INVIERNO; contra las imágenes b y c no se pudo comparar**, por lo mismo que el punto a (§4). |
| e. Propuesta | §5: un valor nuevo `rejilla_h4` en `reloj_sesiones`, un parámetro nuevo con la vela que abre la ventana, una sola puerta en `engine/relojes.py`, el ADR nuevo y los registros de feedback. Hoy H2b y el motor solo difieren 20 días laborables al año (§5.1). |
| f. Declaración | Fila del 2026-10-06 en `HOLDOUT-EXPOSICIONES.md` (§7). |

**PARADA.** Lo que hace falta del consultor antes de la fase 1 está en §6: siete decisiones, y la
primera (cómo se verifican los literales) condiciona los registros de feedback.

## 1. Fase 0 a · Las capturas de «Mensajes del trader»

### 1.1 Están las 8

Carpeta `corpus/Estrategia del trader/Material adicional de su operativa/Mensajes del trader/`,
listada el 2026-10-06 (nombre, tamaño y sha256; ninguna abierta). Los nombres son los de hoy: el
renombrado es el paso 1 de la fase 1.

| Fichero hoy | Bytes | sha256 | Nombre que pide el encargo |
|---|---|---|---|
| `a.png` | 184.056 | `063a20cb667a…` | `mensaje-whatsapp-2026-10-06-1344-graficos-h4-y-utc2.png` |
| `b.jpeg` | 89.305 | `46e5ff19554f…` | `mensaje-whatsapp-2026-10-06-1344-grafico-h4-oct-2024.jpeg` |
| `c.jpeg` | 95.721 | `1b7b5d3a2410…` | `mensaje-whatsapp-2026-10-06-1344-grafico-h4-nov-2024.jpeg` |
| `d.png` | 229.789 | `5ca9c354747d…` | `mensaje-whatsapp-2026-10-06-1345-se-opera-a-las-6-y-stop.png` |
| `e.png` | 40.762 | `3f0c06eb25a2…` | `mensaje-whatsapp-2026-10-06-1536-vela-3-nov-y-mitigacion.png` |
| `Captura de pantalla 2026-10-06 154450.png` | 377.183 | `0967a72522a2…` | `mensaje-whatsapp-2026-10-06-1544-respuestas-1b-2c.png` |
| `Captura de pantalla 2026-10-06 154630.png` | 94.987 | `c39e15b541d3…` | `mensaje-whatsapp-2026-10-06-0953-reloj-grafico.png` |
| `Captura de pantalla 2026-10-06 154806.png` | 70.623 | `a6f82bdd1134…` | `mensaje-whatsapp-2026-10-06-0959-reloj-grafico.png` |

Hay un noveno fichero, `mensaje-whatsapp-0208-zonas-de-control.png` (12.417 bytes), que es la
captura del 2026-09-11 que cierra A-20 y ya está inventariada. No falta ninguna de las 8.

### 1.2 Los literales no se han verificado: la guardia bloquea las imágenes

El encargo pide verificar cada literal contra su imagen, y parar si alguno no casa. **No he podido
abrir ninguna.** El único intento, un Read de la captura de las 09:53, lo paró la guardia antes de
leer nada:

```
GUARDIA (.claude/hooks/guardia.py) bloquea: Read de …\Mensajes del trader\Captura de pantalla 2026-10-06 154630.png.
Regla: CLAUDE.md, «Que se puede mirar y que no», punto 3: las capturas de Analytics de FX Replay, EN BLOQUE y de
cualquier mes; una imagen del material adicional no se abre para ver que es (ADR-0038).
```

- La regla está en el código de la guardia: `_motivo_material` devuelve el bloqueo para todo
  fichero con extensión de imagen que cuelgue de `Material adicional de su operativa`, sin excepción
  por subcarpeta (`.claude/hooks/guardia.py`, cabecera: «toda imagen del material adicional: puede
  ser una captura de Analytics»).
- ADR-0038 prohíbe en bloque las capturas de Analytics porque su rango no se conoce antes de
  abrirlas. No nombra los mensajes de WhatsApp. La guardia es más ancha que el ADR a propósito:
  no puede saber qué es un PNG sin abrirlo.
- Una guardia no se rodea (`CLAUDE.md`): no he buscado otra vía para leerlas. Tampoco se toca
  `.claude/` en esta rama.

**Consecuencia.** Ni el punto a (los literales) ni la mitad del punto d (las etiquetas del eje de b
y c) están verificados por esta sesión. Lo que hay es la lectura del consultor, que es quien abrió
las capturas: los literales del encargo y las etiquetas del §12 de RELOJ-INVIERNO. Es la primera
decisión del §6.

### 1.3 Lo que se vio de pasada, y no se debió listar

Antes de listar «Mensajes del trader» hice un `ls` de su carpeta madre, `Material adicional de su
operativa`. Enseñó NOMBRES, sin ningún contenido: sus subcarpetas (`Backtest marzo 2026`, `Backtest
mayo 2026`, `Backtest septiembre 2026`, `Mensajes del trader`), los de 21 imágenes de WhatsApp de
septiembre y los de los libros de enero, abril y agosto.

- **Es el mismo error que el consultor apuntó al cerrar `trabajo/reloj-invierno`** («nunca se lista
  una carpeta que contiene meses reservados»), y el encargo de esta rama dice que marzo no se
  lista. Lo repetí porque leí esa lección en HISTORIA después de hacer el listado, no antes.
- Ningún contenido de marzo: ni un fichero de dentro de su carpeta, ni tamaño, ni sha. Nada de
  febrero ni de julio.
- Un segundo comando contó las imágenes de esa carpeta (`ls | grep -c`): su salida fue solo el
  número 21.
- Declarado en la fila del 2026-10-06 de HOLDOUT-EXPOSICIONES. Desde ahí, solo la ruta literal de
  «Mensajes del trader».

Un `ls` de las cuatro carpetas de audio del Escritorio (para el punto b) enseñó también nombres de
ficheros personales ajenos al proyecto en `sesion-03-audio`. No se abrió ninguno.

## 2. Fase 0 b · Los dos pendientes que salieron de PROJECT_STATE

### 2.1 El texto literal

Del registro de cierre de `trabajo/reloj-invierno` en `docs/state/HISTORIA.md` («El texto de E que
sale, literal»):

> E. **A-42 respondida en la sesión 4 (S-7, SESION-04-EXTRACCION.md §3.1), pendiente de activar ANTES del 25 de octubre, con las horas fijadas en UTC (punto 11 del §4)**. Respuesta del trader y medida de enero: RELOJ-INVIERNO.md. La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee. La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.

Los dos pendientes son sus dos últimas frases:

1. «La fase 0 de la activación rehace con --solo-filtrar --video las filtradas de v7–v10 y las
   comprueba contra FILTRADAS-ESCENARIO-B.md; hasta entonces nadie las lee.»
2. «La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles
   tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem
   ev-v10-010438-024f76b8.»

Lo que hay que comprobar en el (1) lo fija `FILTRADAS-CON-TRAMOS.md` §5: «que lo tapado es B más
los tramos, que nada se destapa frente a A dentro de un tramo y que los 12 casos del segundo de
margen quedan tapados».

### 2.2 El (1), hecho: ninguna diferencia

**Antes de escribir.** Las filtradas instaladas eran las A: el sha256 de cada `*.filtrada.md` y de
cada `*.registro.txt` era el de su copia `*-A-condicion.*`, así que rehacerlas no pierde nada. Las
B siguen apartadas como `*.filtrada-B-condicion.md`, sin abrir.

**El guion de `main`, tal cual** (`git diff --quiet main -- scripts/transcribir_sesion.py` dio
igual), uno por vídeo:

- `uv run python scripts/transcribir_sesion.py --solo-filtrar --video v7 --sesion 02 --audio "C:/Users/USER/Desktop/sesion-02-v7-audio/sesion-02-v7.m4a"`
- `… --solo-filtrar --video v8 --sesion 02 --audio "C:/Users/USER/Desktop/sesion-02-v8-audio/sesion-02-v8.m4a"`
- `… --solo-filtrar --video v9 --sesion 03 --audio "C:/Users/USER/Desktop/sesion-03-audio/sesion-03.m4a"`
- `… --solo-filtrar --video v10 --sesion 04 --audio "C:/Users/USER/Desktop/sesion-04-audio/sesion-04.m4a"`

Los cuatro salieron con exit 0, y en los cuatro el guion comprobó que el sha256 del WAV es el de la
transcripción del corpus de ese vídeo. De su salida solo se miraron las líneas de recuento.

| Vídeo | Tramos del vídeo | Segmentos | Tapados: solo meses / solo tramos / ambos | Bloques `[NO CITABLE]` | sha256 de la filtrada nueva |
|---|---|---|---|---|---|
| v7 | 1 | 602 | 0 / 1 / 3 | 1 | `be4c076388c5bcbb4d337422f2f19871ce2ad2e964f72497fcfc244579f084b3` |
| v8 | 0 | 229 | 0 / 0 / 0 | 0 | `9f1bf4dff1f051a8d67ea483075a6cb096f7f0a6425d9095efec3e0c4c595916` |
| v9 | 21 | 1.664 | 0 / 88 / 29 | 8 | `c12af9de6460d7f53742a4cf2338fca4840b814d5fec304f1916f5b7a9f8734b` |
| v10 | 22 | 1.914 | 0 / 63 / 48 | 14 | `87e1be9cc26832d6fde119679588f9920ac552a0fc612842511bfd1bbff159f5` |

La de v8 cambia de sha aunque no tapa nada: la cabecera de la filtrada lleva ahora la frase de los
`[NO CITABLE]`.

**La medida, solo por marcas.** Anexo `anexos/ACTIVACION-A42/medir_filtradas.py`, con la salida en
`medir_filtradas-SALIDA.txt`. De cada filtrada lee las marcas de los bloques y la marca `[mm:ss]`
del principio de cada línea visible; el texto no se guarda ni se imprime. De cada registro, sus
líneas de recuento. Las tres filtradas de un vídeo salen de la misma cruda, así que se comparan
como multiconjuntos de marcas (lección de `medir_fase1.py`).

| Comprobación | v7 | v8 | v9 | v10 |
|---|---|---|---|---|
| D1 · visible en la nueva que B tapaba | 0 | 0 | 0 | 0 |
| Lo que la nueva tapa y B no (B − nueva) | 1 | 0 | 88 | 63 |
| … con la marca dentro de un tramo | 0 | 0 | 82 | 52 |
| … que asoman por el INICIO de un tramo (medida de VENTANA-EV-V9 §5) | 1 | 0 | 6 | 11 |
| D2 · tapado sin explicar / esperado que falta | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| D3 · el registro cuadra (solo meses 0; meses = los de B; solo tramos = B − nueva) | sí | sí | sí | sí |
| D4 · destapado frente a A dentro de un tramo (o en el segundo anterior) | 0 | 0 | 0 | 0 |
| D5 · línea visible de la nueva con la marca dentro de un tramo | 0 | 0 | 0 | 0 |

- **Lo tapado es B más los tramos, exactamente.** Los segmentos por meses son los de B (3, 0, 29 y
  48), y todos caen además en un tramo («solo por meses»: 0). Lo que los tramos tapan de más
  cuadra uno a uno con lo esperado: las líneas de B con la marca dentro de un tramo, más los
  segmentos que empiezan antes de un tramo y lo pisan.
- **De VENTANA-EV-V9.md.** Su medida daba 32 filas de segmentos que asoman por un borde (21 de
  tramos de cuarentena mecánica y 11 de otros). Las 18 de aquí son las de sus filas «inicio» de
  v7, v9 y v10 que empiezan fuera de todo tramo. Las de «fin» empiezan dentro del tramo y ya
  cuentan en la fila de arriba.
- **Los 12 casos del segundo de margen** (`FILTRADAS-ESCENARIO-B.md` §5.2), uno por uno: en A y en
  B había una línea visible en el último segundo de cada tramo (en el de v9 de 1:13:55, solo en B);
  en la nueva, 0 en los 12.

**DIFERENCIAS: ninguna** (el guion sale con exit 0). Sigue la fase 0.

Una primera pasada del guion dio «se esperaban 12 tramos de margen y hay 14». Era un defecto mío:
identificaba los 12 por su segundo de inicio, y en v9 hay dos tramos que empiezan en el mismo
segundo (el original y el que lo completa con el margen). Ahora se identifican por su intervalo
entero. D1 a D5 ya salían en 0.

**Lo que esto cambia fuera del repositorio.** Las `*.filtrada.md` y los `*.registro.txt`
instalados en las cuatro carpetas del Escritorio son ahora los nuevos. Las A y las B siguen
apartadas con su nombre. Con la comprobación hecha, las filtradas se pueden volver a leer; esta
sesión no ha leído ninguna.

### 2.3 El (2): añadir `ev-v10-010438-024f76b8` a la evidencia de A-42

Es el paso 4 de la fase 1. El ítem existe (`knowledge/evidence/v10/ev-v10-010438-024f76b8.yaml`,
supersede a `ev-v10-010438-0d4e6798`) y no está en ningún tramo. A-42 cita hoy cuatro ítems de v3,
v4 y v9, y ninguno de v10. Propongo añadir también `ev-v10-010429-0c93f24a` («sería de 6 a 10 […]
después del día 25»), que es la frase de S-7 que separa H2b de H2a (§6, D6).

## 3. Fase 0 c · Todo lo que depende del reloj de las sesiones

### 3.1 El registro (`knowledge/spec/parametros.yaml`)

| Parámetro | Hoy | Dónde se lee |
|---|---|---|
| `reloj_sesiones` | enum `[civil_operativa, grafico]`, valor `civil_operativa`, `DEFAULT_AMBIGUOUS` bajo A-42, categoría `ejecucion`, fuente ADR-0063 | `engine/relojes.py` (`HUSO_DEL_RELOJ`: cada opción nombra el parámetro que lleva su huso); las formas de RN-001 y RN-002 lo nombran en `reloj:` |
| `huso_operativa` | `Europe/Madrid`. Reloj civil del trader y del DÍA DE RIESGO. **No cambia** | `engine/cableado.py` (`comprobar_reloj_unico`), `cases/` (ventanas del kit, ingesta), `reloj_dia_riesgo` |
| `huso_grafico` | `Etc/GMT-2`, `CONFIRMED`, fuente `ev-v4-011425-ae028b78`. Su descripción dice «UTC+2 FIJO» y cita R0 y ADR-0039 | Solo por `reloj_sesiones = grafico`, que nadie selecciona. Ninguna regla cuelga de él |
| `anclaje_h4` | `17:00` `America/New_York`, fuente `fb-2026-09-09-sesion-01-479e68b9` | `data/agregacion.py` (la rejilla), `engine/arnes.py`, `engine/visor.py`, `vence_vela_h4` (RN-002), tres scripts |
| `ventana_inicio`, `ventana_fin` | `07:00` y `15:00`, huso `Europe/Madrid`, «en el reloj que dice reloj_sesiones»; fuente, dos registros de la sesión 1 | `en_ventana` (RN-001), `alcanza_hora` (RN-002), `scripts/ticks_spread.py` |
| `cierre_h4_antelacion` | 1 minuto antes del fin de la vela H4 de la rejilla | `vence_vela_h4` (RN-002). **Ya va por la rejilla, con zoneinfo: no cambia** |

La descripción de `anclaje_h4` ya dice lo que vería un gráfico en Madrid (las 23:00, y las 22:00 en
las semanas del cambio). Con `huso_grafico` en Europe/Madrid deja de contradecirlo
(RELOJ-INVIERNO.md §8.5). Sus fechas («8 a 28 de marzo y 25 a 31 de octubre») son las de 2026.

### 3.2 Las reglas (`knowledge/spec/strategy_spec.yaml`)

- **RN-001** (la ventana): forma `en_ventana: {inicio: ventana_inicio, fin: ventana_fin, reloj:
  reloj_sesiones, dias: dias_operables}`. Su título («la ventana operativa es el horario del
  trader, no el de las velas») y sus notas («manda SU horario, no la rejilla […] el bot empieza una
  hora DENTRO de la vela. Se decidió así a propósito el 2026-09-10») **dicen lo contrario de H2b**.
- **RN-002** (el cierre): `vence_vela_h4: {anclaje: anclaje_h4, antelacion: cierre_h4_antelacion}`
  o `alcanza_hora: {hora: ventana_fin, reloj: reloj_sesiones}`. Con H2b las dos ramas caen sobre
  el mismo límite de vela.
- RN-003 (el sesgo) lee `anclaje_h4`; RN-035 nombra `sigue_hasta_ventana_fin`. No cambian.

### 3.3 El código

| Sitio | Qué hace con el reloj |
|---|---|
| `engine/relojes.py` | `huso_del_reloj` y `huso_de_las_sesiones`: del selector a un huso IANA |
| `engine/primitivas.py` | `en_ventana` y `alcanza_hora`: instante → hora de pared en el huso del selector, comparada con las horas del registro. `vence_vela_h4`: por la rejilla |
| `engine/motor.py` | `DiaDeMercado(dia, huso, sesiones, datos)`; `_minuto_utc(dia, "HH:MM", huso)` da el límite de cada sesión |
| `engine/arnes.py` | `dias_de_mercado(…, huso_sesiones, …)`; las sesiones salen de `knowledge/cases/kit/config.yaml` (`07-11`, `11-15`) |
| `engine/simulacion.py` | `mercado_de_construccion`: la ventana del día (`ventana_local` del kit, 00:00–15:00) en `huso_de_las_sesiones` |
| `engine/cableado.py` | los límites de sesión con `dia.huso`; y `comprobar_reloj_unico`, que es el día de riesgo y **no cambia** |
| `engine/visor.py` | `huso` = `huso_de_las_sesiones`, para los límites y para pintar las horas |
| `cli.py` (línea 2392), `scripts/caja_77_exploratoria.py`, `scripts/embudo_77.py` | pasan `huso_de_las_sesiones(registro)` |
| `scripts/ticks_spread.py` | las horas de `ventana_inicio` a `ventana_fin` en `huso_operativa` |
| `cases/ventanas.py`, `cases/ingesta.py`, `cases/fidelidad.py`, `cases/paquete.py`, `cases/hoja_docx.py` | la ventana y la sesión de cada caso, por hora de pared en **`huso_operativa`**. No pasan por `reloj_sesiones` |

El simulador de cuenta (`engine/cuenta.py`) corta el día en el huso del perfil de la firma, que el
cableado compara con `huso_operativa`. No lee el reloj de las sesiones.

`tests/contract/test_no_business_literals.py` prohíbe en `src/` las horas `07:00`, `11:00`,
`15:00`, `17:00` y `23:00` y los husos `Europe/Madrid`, `America/New_York` y `Etc/GMT-N`: el motor
solo puede sacarlos del registro.

### 3.4 Los tests que fijan el estado de hoy

| Test | Qué fija |
|---|---|
| `tests/unit/test_dos_relojes.py` | el selector vale `civil_operativa`, es `DEFAULT_AMBIGUOUS` bajo A-42 y sus opciones son exactamente las de `HUSO_DEL_RELOJ`; las horas de la ventana declaran el huso del reloj de las sesiones; las formas de RN-001 y RN-002; la ventana y el motor con cada selector; el día de riesgo |
| `tests/unit/test_huecos_motor.py` (H2) | las sesiones del kit cubren exactamente `[ventana_inicio, ventana_fin)` y el huso de las dos horas es `huso_de_las_sesiones` |
| `tests/unit/test_registro.py` (líneas 447–478) | el huso del ancla no es el del gráfico; las horas de la ventana declaran el huso del reloj de las sesiones |
| `tests/unit/test_kit.py` | las bloqueantes abiertas son `{A-21, A-35, A-42, A-44, A-51}`; el conjunto de RESUELTAS; la tabla de PROJECT_STATE |
| `tests/unit/test_hoja_preguntas.py` y `scripts/hoja_preguntas.py` | A-42 está en «Lo primero» de la hoja; una RESUELTA no puede estar |
| `tests/unit/test_cierre_vela_h4.py` | los argumentos de `vence_vela_h4` y de `alcanza_hora` en RN-002 |
| `tests/contract/test_spec_docs_generados.py` | `docs/spec/*.md` es lo que sale de los YAML |
| `tests/unit/test_transcribir_sesion.py` | el orden de la hoja de la sesión 02, fijado como historia (lleva A-42; no depende de su estado) |

### 3.5 Los textos que dicen «UTC+2 fijo»

Los que nombra el encargo:

| Sitio | Qué dice |
|---|---|
| ADR-0039, «Problema que resuelve» | «el eje de FX Replay supuesto UTC (es UTC+2 fijo)» |
| ADR-0059, título, recuadro y decisión | la lectura provisional: sesiones fijas en el reloj del gráfico, UTC+2 todo el año (es H1) |
| ADR-0063 | no dice «UTC+2 fijo», pero su §2 deja el selector bajo A-42 y dice que aplicar la lectura será pasarlo a `grafico` |
| `ABRIL-Y-LA-CAJA.md` R0 (líneas 220–236, 431 y 440) | «es un UTC+2 fijo», «también en enero. No es Europe/Madrid» |
| `docs/runbooks/MIRAR-EL-MATERIAL.md` (línea 53) | «EL RELOJ DE LOS GRAFICOS DE FX REPLAY ES UTC+2 FIJO […] NO es Europe/Madrid» |
| `ambiguedades.yaml`, A-42 | la pregunta lleva la lectura provisional; el comentario, «El grafico de FX Replay es UTC+2 fijo» |
| `PROJECT_STATE.md`, Technical Debt | «LA SERIE DEL TRADER ES OANDA Y LA NUESTRA DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO» y «EL «UTC+2 FIJO» FALLA EN ENERO» |

**Los que el encargo no nombra** y dicen lo mismo (§6, D7):

- **`CLAUDE.md`**, «Que se puede mirar y que no», punto 1: «el reloj de los graficos de FX Replay es
  UTC+2 FIJO». Su cabecera manda corregirlo en el mismo commit que deja de ser cierto.
- **`docs/runbooks/ENTRADA-MARZO.md`**, PARADA B0: «El grafico de FX Replay es UTC+2 fijo».
- **`docs/runbooks/README.md`** (línea 8): «el reloj de FX Replay (UTC+2 fijo)».
- **ADR-0017**, sus dos enmiendas: la del 2026-09-25 (`huso_grafico` es `Etc/GMT-2`) y la
  provisional del 2026-09-29 (ADR-0059).
- **`docs/adr/README.md`**: el título de ADR-0059 en el índice.
- `docs/HANDOFF.md` lo dice en una entrada de estado del 2026-09-21: es historia fechada.
- `docs/spec/*.md` se regenera con `spec docs --escribir`.

### 3.6 La PARADA B0 de ENTRADA-MARZO, y lo que A-42 RESUELTA no arregla

La condición de B0 es que el campo `estado` de A-42 diga `RESUELTA`. Al acabar la fase 1 la
cumplirá. **Pero el motivo de la parada no queda resuelto con eso**, y el informe lo dice sin
tocar nada, como pide el encargo:

- B0 existe porque el sorteo congela la ventana de cada caso en `ventanas.yaml`, y el sorteo no se
  repite. Esa ventana la calcula `cases/ventanas.py` con las horas de pared del kit en
  `huso_operativa`.
- Con H2b, del 9 al 27 de marzo de 2026 el trader opera de 06:00 a 14:00 de Madrid (05:00–13:00
  UTC), y `huso_operativa` da 07:00–15:00. Son 15 de los días laborables de marzo (§5.1).
- Así que la rama de marzo necesita, ANTES de su paso b, que `cases/` cuente la ventana por la
  rejilla, o la ventana congelada de esos 15 días saldrá una hora tarde.

Esta rama no toca `cases/` ni marzo. Va a la entrada de marzo.

## 4. Fase 0 d · La rejilla H4 en las dos semanas de 2024

Anexo `anexos/ACTIVACION-A42/rejilla_h4_2024.py`, con la salida en `rejilla_h4_2024.txt`. Importa
`tabla` del guion de M4 (`anexos/RELOJ-INVIERNO/rejilla_h4.py`, sin tocarlo) y añade lo que el eje
enseña: la hora del ancla de cada día y los seis límites H4, sacados de `limites_del_dia`, la
función que parte las velas del bot. En 2024 Europa cambió la hora el domingo 27 de octubre y
EE. UU. el domingo 3 de noviembre.

| Semana (anclas) | Ancla en UTC | En un eje Europe/Madrid | En un eje Etc/GMT-2 | Límites H4 en Europe/Madrid | Primera sesión con H2b |
|---|---|---|---|---|---|
| dom 27 a jue 31 de octubre de 2024 | 21:00 | **22:00** del mismo día | 23:00 | 22, 02, 06, 10, **14**, 18 | 05:00 UTC = 06:00 de Madrid |
| dom 3 a jue 7 de noviembre de 2024 | 22:00 | **23:00** del mismo día | 00:00 del día siguiente | 23, 03, 07, 11, **15**, 19 | 06:00 UTC = 07:00 de Madrid |

Los cinco días de cada semana dan lo mismo.

**Contra la lectura del consultor (RELOJ-INVIERNO.md §12): coincide.** Él leyó en b «dom 27 Oct
'24 22:00», «jue 31 Oct '24 22:00» y velas a las «14:00»; y en c «dom 03 Nov '24 23:00», «jue 07
Nov '24 23:00» y velas a las «15:00». Es lo que da un eje Europe/Madrid, y no lo que daría
Etc/GMT-2 (23:00 y 00:00). El mensaje de las 15:36 («la del 3 de noviembre empeiza las 23:00 pm»)
dice lo mismo que la segunda fila.

**Contra las imágenes b y c: no comparado.** No pude abrirlas (§1.2). El cálculo del consultor
queda repetido; su lectura de las etiquetas sigue sin una segunda verificación.

## 5. Fase 0 e · Propuesta para meter H2b

### 5.1 Cuánto cambia: 20 días laborables al año

Anexo `anexos/ACTIVACION-A42/dias_distintos.py` (solo calendario, con zoneinfo y el registro), con
la salida en `dias_distintos.txt`. Compara la ventana de H2b con la que el motor calcula hoy
(`civil_operativa`, que es H2a) y con H1.

| Año | Ventanas UTC de H2b | H2b ≠ el motor de hoy (H2a) | H2b ≠ H1 |
|---|---|---|---|
| 2024 | 05:00–13:00 y 06:00–14:00 | 20 días: 11 a 29 de marzo; 28 de octubre a 1 de noviembre | 92 días |
| 2025 | las mismas | 20 días: 10 a 28 de marzo; 27 a 31 de octubre | 91 días |
| 2026 | las mismas | 20 días: **9 a 27 de marzo; 26 a 30 de octubre** | 91 días: 1 de enero a 6 de marzo; 2 de noviembre a 31 de diciembre |
| 2027 | las mismas | 15 días: 15 a 26 de marzo; 1 a 5 de noviembre | 91 días |

- **En el material de construcción no cambia nada.** Enero, abril, mayo, agosto y septiembre de
  2026 no tienen ningún día en esos dos tramos: con H2b el motor abre a la misma hora que hoy.
- **Lo primero que cambia es la semana del 26 al 30 de octubre de 2026**: 05:00 UTC en vez de
  06:00.
- **H1 coincide con H2b esa semana** y falla todo el invierno; **H2a falla solo esa semana** (y
  marzo). Ningún día suelto separa las tres: los tests necesitan el conjunto de fechas del
  encargo.

### 5.2 El registro: un valor nuevo y un parámetro nuevo

1. **`reloj_sesiones` gana la opción `rejilla_h4` y pasa a valer eso**: `CONFIRMED`, sin
   `ambiguedad_id`, fuente el ADR nuevo. Es de categoría `ejecucion`, así que lo cambia una decisión y
   no un registro de feedback: `feedback apply` se niega (`feedback/aplicar.py`, ADR-0004).
   - `civil_operativa` y `grafico` **se quedan como opciones**. No son H2b, pero con ellas los
     tests calculan H2a y H1 por el mismo camino que H2b y demuestran que fallan (§5.5).
   - Descartado: reusar `grafico` con `huso_grafico` en Europe/Madrid. Eso es H2a.
2. **Parámetro nuevo `sesiones_primera_vela_h4`**, entero, valor 3, categoría `ejecucion`, fuente
   el ADR nuevo: la ventana empieza al abrir la TERCERA vela H4 del día de rejilla, contando desde el
   ancla (ancla + 8 h). La cifra no puede vivir en el código (ADR-0002).
3. **`ventana_inicio` y `ventana_fin` conservan valor, huso y fuente** (`07:00` y `15:00`,
   Europe/Madrid, los dos registros de la sesión 1). Cambia lo que significan, y su `unidad` y su
   descripción lo dicen: son las horas que marca el gráfico del trader cuando Europa y EE. UU.
   coinciden en el horario. Siguen nombrando las sesiones del kit (`07-11`, `11-15`) y las
   etiquetas de los casos, que no se tocan.
4. **`huso_grafico` pasa a `Europe/Madrid`**, y su descripción deja el «UTC+2 FIJO». La fuente, en
   §5.4.
5. **`anclaje_h4`**: solo la descripción, que ya no contradice a `huso_grafico`. Valor y fuente,
   intactos.

### 5.3 El motor: una sola puerta, y ningún desfase

**La definición.** Con `rejilla_h4`, el reloj de las sesiones marca `ventana_inicio` en el instante
en que abre la vela H4 número `sesiones_primera_vela_h4` del día de rejilla, y corre desde ahí. Una
hora nominal H de ese día es el instante `apertura de esa vela + (H − ventana_inicio)`.

- **La apertura sale de `limites_del_dia`** (`data/agregacion.py`), la misma función que parte las
  velas H4 del bot con zoneinfo sobre el huso del ancla. No hay ningún desfase respecto de UTC en
  ningún sitio: ni `Etc/GMT-N`, ni una suma de horas a una hora UTC.
- **Las formas de RN-001 y RN-002 no cambian.** Siguen nombrando `ventana_inicio`, `ventana_fin`,
  `reloj_sesiones` y `dias_operables`. Qué parámetros lee cada reloj vive en la tabla de
  `engine/relojes.py`, como hoy `HUSO_DEL_RELOJ` (ADR-0063): `rejilla_h4` → `anclaje_h4`,
  `sesiones_primera_vela_h4` y `ventana_inicio`.
- **El día.** El día de rejilla de un día operativo es el que abre su vela número N en esa fecha,
  mirada en el huso del ancla. Con el ancla a las 17:00 es el de la víspera, pero no se escribe «la
  víspera»: se calcula.
- **Guardias dentro de la puerta**, que fallan con nombre y no adivinan: cada límite de sesión del
  kit tiene que ser un límite de la rejilla, y cada sesión, una vela H4 entera. Un día de rejilla
  con una vela irregular (el domingo de un cambio de hora) no es operable.

**Lo que se toca**, todo por esa puerta de `engine/relojes.py`:

| Sitio | Cambio |
|---|---|
| `engine/relojes.py` | la puerta: de (día, hora nominal) a instante UTC, y de instante a (día, hora nominal), para los tres selectores |
| `engine/primitivas.py` | `en_ventana` y `alcanza_hora` preguntan a la puerta en vez de pasar un instante a un huso |
| `engine/motor.py`, `engine/cableado.py`, `engine/arnes.py`, `engine/simulacion.py`, `engine/visor.py`, `cli.py`, dos scripts | `DiaDeMercado` deja de llevar un huso con el que convertir «HH:MM»; los límites de cada sesión salen de la puerta |
| `engine/visor.py` | pinta las horas en `huso_grafico`, que es lo que el trader ve. En el material de hoy da las mismas horas que ahora |

**Lo que no se toca:** `comprobar_reloj_unico` y todo el día de riesgo (`huso_operativa`,
ADR-0063); `vence_vela_h4`; `cases/` (§3.6); el kit y sus sesiones.

### 5.4 El ADR nuevo y el feedback

**El ADR nuevo**, antes de citarlo en ningún sitio (le toca el número 0069; aquí no se escribe
su id, porque `knowledge validate` rechaza la cita de un ADR que todavía no existe): «A-42: las
sesiones son las velas H4 de la rejilla de anclaje_h4 (H2b)».

- Decide: H2b y no H2a, con el porqué del encargo; `rejilla_h4`; el parámetro nuevo;
  `huso_grafico` en Europe/Madrid; que las horas del registro pasan a ser nominales; y que
  `cases/` queda pendiente para la entrada de marzo.
- **Deja superada la lectura provisional de ADR-0059**, que pasa a `SUPERSEDED` con su recuadro.
- Enmienda ADR-0063 (una tercera opción, que no es un huso) y ADR-0017 (el punto 4 vuelve a
  Europe/Madrid; el punto 1, «manda su horario y no la rejilla», queda corregido).
- Fuentes: RELOJ-INVIERNO.md (M2, M3 y M4), S-7 (`ev-v10-010429-0c93f24a`,
  `ev-v10-010438-024f76b8`) y los registros de feedback de abajo.

**Los registros.** No existe `knowledge/feedback/2026-10-04-sesion-04/`. Propongo crearla: los
mensajes contestan a S-7, que es de la sesión 4, y el precedente es el WhatsApp de A-20, registrado
en la sesión 1 con su fecha de llegada aparte.

- Comunes: `sesion: 2026-10-04-sesion-04`, `fecha: 2026-10-04`, `recibido_el: 2026-10-06`, `medio:
  escrito`, `procedencia: trader_escrito`, la ruta de la captura en `notas`. En `registrado_por`,
  quién leyó el literal en la captura (§6, D1) y «el trader, desde sus dos números, confirmado por
  Aleks». Ningún nombre ni número.

| # | Mensaje | Objetivo y acción | Valor |
|---|---|---|---|
| F1 | 15:44, «1-B)» | `ambiguedad` A-42, `RESOLVE_UNKNOWN` | `rejilla_h4` |
| F2 | 09:53, «según la configuración de la plataforma etc+2 madrid» | `parametro` `huso_grafico`, `CORRECT` | `Europe/Madrid` |
| F3 | 13:45, «si es por cuestion horaria se oepra a las 6» | `evidence` `ev-v10-010429-0c93f24a`, `CONFIRM` | — |
| F4 | 13:44, «1- Si esta configurado UTC+2» | sin objetivo claro (§6, D4) | — |
| F5 | 09:59, «xd» «sep» «seria cuestion que se adapte a lo que bote la plataforma» | sin objetivo claro (§6, D4) | — |
| F6 | 15:36, «la del 3 de noviembre empeiza las 23:00 pm» | sin objetivo claro (§6, D4) | — |

Dos problemas medidos, que decide el consultor:

- **F1 no cabe sola.** `feedback/modelo.py` exige 5 caracteres en `respuesta_literal` (línea 284),
  y «1-B)» tiene 4 (medido con `_normalizar_texto`). Además, lo que «B» significa está en la
  pregunta de las 15:38, que solo está en la captura (§6, D2).
- **F2 afirma más que su cita.** El trader escribe «etc+2 madrid» y, a las 13:44, «UTC+2». Que la
  zona sea Europe/Madrid con su cambio de hora lo dice la medida (el eje de enero va en UTC+1,
  RELOJ-INVIERNO §5.4) y lo enseñan las capturas b y c, no la frase. `trabajo/reloj-invierno` se
  negó a leerla así por eso (§6, D3).

**Lo que NO se registra**, como manda el encargo: los tres mensajes sobre el stop (13:46, la
segunda frase de las 15:36 y «2-c»). Quedan en el corpus con su captura, y aquí solo como contexto
para U.

### 5.5 Los tests

**Nuevos**, en `tests/unit/test_sesiones_rejilla_h4.py`, con fechas de calendario y sin leer datos:

| Test | Qué afirma |
|---|---|
| Las horas del encargo | apertura de la primera sesión: 2026-10-23, 05:00 UTC; 2026-10-26, 05:00; 2026-11-02, 06:00; 2026-01-15, 06:00; 2025-03-10 a 14, 05:00; 2024-10-28 a 11-01, 05:00; 2024-11-04 a 08, 06:00. Y la segunda sesión y el cierre, 4 y 8 horas después |
| H2a falla | con `civil_operativa`, el mismo camino da otra hora el 2026-10-26, del 2025-03-10 al 14 y del 2024-10-28 al 11-01 |
| H1 falla | con `grafico` y un registro de prueba con el gráfico en Etc/GMT-2, da otra hora el 2026-11-02, en enero y del 2024-11-04 al 08 |
| Ningún desfase fijo | (a) en todos los días laborables de 2024 a 2027, la apertura es un límite de `limites_del_dia`, y la hora UTC toma dos valores, no uno; (b) ningún desfase fijo de UTC−12 a UTC+14 con la hora nominal reproduce el año entero; (c) con el ancla en un huso sin cambio de hora, las fechas de verano fallan |
| El motor entero | un día de la semana del cambio, de punta a punta: las sesiones abren en los límites de la rejilla y RN-001 no prohíbe dentro |
| El día de riesgo | `comprobar_reloj_unico` no se niega en invierno con `rejilla_h4` |
| Las guardias de la puerta | una sesión que no es una vela entera, y un día con vela irregular, fallan con nombre |
| Construcción | fuera de los 20 días de §5.1, la ventana por rejilla es la de `civil_operativa` en todo 2026 |

**Los que rompen la guardia y se actualizan** (§3.4): `test_dos_relojes.py`, `test_huecos_motor.py`
(H2), `test_registro.py`, `test_kit.py`, `test_hoja_preguntas.py` con `scripts/hoja_preguntas.py`,
y los que construyen `DiaDeMercado` con un huso. `docs/spec/` se regenera.

### 5.6 El orden de la fase 1, con lo que añade esta propuesta

El del encargo, con dos añadidos: el parámetro nuevo entra en el paso 4, con el resto de la spec; y
el contrato se amplía en un commit propio antes del paso 1, con las rutas de cada paso.

Un riesgo de orden: el paso 4 deja `reloj_sesiones` en un valor que el motor no sabe leer hasta el
paso 5, y `make check` no sella un commit en rojo. O el valor nuevo del selector entra en el paso
5, con el motor, o el paso 5 va antes que el 4 (§6, D5).

## 6. Lo que decide el consultor (PARADA)

| # | Decisión | Opciones, y la que recomiendo |
|---|---|---|
| D1 | **Cómo se verifican los literales y las etiquetas de b y c**, si la sesión no puede abrir las capturas | (a) **Recomendada:** vale la lectura del consultor, y el informe y `registrado_por` lo dicen así («leído por el consultor en la captura; la sesión no la abrió»). (b) Una rama previa que abra en la guardia las imágenes de «Mensajes del trader», y esta espera. (c) Otra vía que diga el consultor |
| D2 | **F1: «1-B)» tiene 4 caracteres** y su sentido está en la pregunta de las 15:38 | (a) **Recomendada:** el consultor da el texto literal de la pregunta de las 15:38 y de la opción B; el registro lleva como literal la respuesta tal como está en su burbuja y, en `notas`, la pregunta y la opción. Si «1-B)» es una burbuja sola, hace falta (b) o (c). (b) El `RESOLVE_UNKNOWN` de A-42 lleva el literal de las 13:45, y «1-B)» queda en el ADR y en el corpus. (c) El `RESOLVE_UNKNOWN` es de la voz de S-7 (`trader_grabado`, v10 64:29–64:34) |
| D3 | **`huso_grafico` = Europe/Madrid: con qué fuente** | (a) **Recomendada:** fuente el ADR nuevo, que cita la medida; F2 se registra sin valor. (b) F2 como `CORRECT` con valor `Europe/Madrid`, y `feedback apply` lo escribe |
| D4 | **F4, F5 y F6**: no son respuesta a un parámetro ni a un ítem concreto | (a) **Recomendada:** no se registran como feedback; quedan en el corpus con su captura, en `fuentes.yaml` y citados en el ADR nuevo. (b) El consultor da objetivo y acción para cada uno |
| D5 | **El selector y el motor** (§5.6) | (a) **Recomendada:** el paso 4 deja A-42 RESUELTA, `huso_grafico` y las descripciones; `rejilla_h4`, el parámetro nuevo y el valor del selector entran en el paso 5 con el motor, con el ADR nuevo en su `Fuente:`. (b) El paso 5 antes que el 4 |
| D6 | **La evidencia de A-42** | Añadir `ev-v10-010438-024f76b8` (el encargo) y también `ev-v10-010429-0c93f24a` (§2.3). Recomiendo los dos |
| D7 | **Los textos de «UTC+2 fijo» que el encargo no nombra** (§3.5) | Recomiendo corregir en esta rama `CLAUDE.md`, ENTRADA-MARZO (B0, con la nota de §3.6), el README de runbooks, ADR-0017 y el índice de ADR |

Y dos cosas de la propuesta que conviene confirmar: el nombre y la categoría del parámetro nuevo
(`sesiones_primera_vela_h4`, `ejecucion`, §5.2), y que `civil_operativa` y `grafico` se queden como
opciones.

### 6.1 Respuesta del consultor a la PARADA (2026-10-06), tal cual

> Modelo: Fable 5.1 · Esfuerzo: alto
>
> Respuesta del consultor a la PARADA de la fase 0 (2026-10-06). Cópiala tal cual al informe como §6.1 y sigue con la fase 1.
>
> D1 · (a). Vale la lectura del consultor, que abrió las 8 capturas el 2026-10-06. En registrado_por y en el informe: «literal transcrito por el consultor de la captura <ruta> (sha256 <hash>); la sesión no la abrió porque la guardia lo impide (ADR-0038)». La guardia no se toca en esta rama. Porqué: el literal es palabra por palabra, no una paráfrasis como la de A-11, y la captura queda en el corpus con su hash para verificarlo.
>
> D2 · (a). «1-B)» no es una burbuja sola: va en la misma burbuja que «2-c)», con una sola hora (15:44). respuesta_literal de F1 = «1-B)\n2-c) la orden se pone y se ejecuta cuando ocurre la mitiga ion». En notas, la pregunta de las 15:38, literal: «1) Este año la hora cambia en Europa el domingo 25 de octubre y en EE. UU. el domingo 1 de noviembre. Me dijiste que desde el 25 empiezas a las 6 de tu gráfico. Desde el lunes 2 de noviembre, ¿a qué hora empieza tu primera sesión en tu gráfico? a) a las 6 b) a las 7 c) otra, ¿cuál?». Y que la parte «2-c)» contesta a otra pregunta, sobre el stop, que no se interpreta (punto U). Porqué: el literal entero es la burbuja; partirla sería editar lo que escribió el trader.
>
> D3 · (a), corregida. Fuente de huso_grafico = Europe/Madrid: el ADR nuevo, que cita la medida (RELOJ-INVIERNO §5.4 y M4, y las capturas b y c). F2 (09:53) NO se registra como feedback: pasa al grupo de D4. Porqué: no hay acción sin valor en el modelo, y CORRECT con Europe/Madrid afirmaría más que «etc+2 madrid».
>
> D4 · (a). F2, F4, F5 y F6 quedan en el corpus con su captura, en fuentes.yaml y citados literales en el ADR nuevo. F3 (13:45, CONFIRM de ev-v10-010429-0c93f24a) sí se registra.
>
> D5 · (a). El paso 4 deja A-42 RESUELTA, huso_grafico y las descripciones. rejilla_h4, el parámetro nuevo y el valor del selector entran en el paso 5 con el motor, con el ADR nuevo en su Fuente:. Porqué: ningún commit queda en rojo.
>
> D6 · Los dos: ev-v10-010438-024f76b8 y ev-v10-010429-0c93f24a.
>
> D7 · Sí: CLAUDE.md, ENTRADA-MARZO (B0, con la nota de §3.6, sin abrir ni listar nada de marzo), el README de runbooks, ADR-0017 y el índice de ADR. Recuadro donde el documento esté cerrado.
>
> Confirmado: sesiones_primera_vela_h4, entero, valor 3, categoría ejecucion, fuente el ADR nuevo; civil_operativa y grafico se quedan como opciones.
>
> Añadidos del consultor:
> 1. Test más: ningún día laborable de 2024 a 2027 lo declara no operable la guardia de la vela irregular. Ella solo puede caer en días de rejilla sin mercado; si cae en uno laborable, PARA y dímelo.
> 2. Lo de §3.6 (cases/ cuenta la ventana en huso_operativa, y del 9 al 27 de marzo la ventana congelada saldría una hora tarde con H2b) es pendiente con dueño: la rama de entrada de marzo, antes de su paso b. Escríbelo así en el informe; entra en la Next Action en el commit del contrato, al cerrar.
> 3. Exposiciones del consultor, a la fila del 2026-10-06 de HOLDOUT-EXPOSICIONES, hoy: (a) abrió las 8 capturas de «Mensajes del trader»: texto de WhatsApp del 2026-10-06 y dos gráficos H4 de octubre y noviembre de 2024; ningún día de 2026; (b) listó por el puente, de forma recursiva, «Material adicional de su operativa»: vio nombres y tamaños de los ficheros de las subcarpetas de marzo, mayo y septiembre, sin abrir ninguno; es el mismo error de §1.3.
> 4. Hallazgos del consultor para la tabla de ERRORES-RECURRENTES en el cierre (no la toques ahora; apúntalos en el informe para que no vivan solo en el chat): (a) el consultor listó una carpeta que contiene meses reservados; (b) el consultor dio un prompt que afirmaba la CI de main en verde con un hueco «<NÚMERO>» sin rellenar, y la rama se borró con esa afirmación (salió bien: run #226 en verde). Lección: un prompt del consultor no afirma un hecho con un hueco; o lo comprueba él, o el prompt manda comprobarlo.
>
> Lo demás, como el encargo: commits separados con Fuente:, fix/activacion-a42 y CI de Linux con su número de run, make check y uv run botsito state check en verde, y revisor con su informe pegado al final.
>
> Rama lista para revisión, NO cerrada.

### 6.2 Pendiente con dueño, y hallazgos para el cierre

- **Pendiente con dueño: la rama de entrada de marzo, antes de su paso b.** `cases/` (kit,
  fidelidad, ingesta y hoja) cuenta la ventana de cada caso en `huso_operativa`; con H2b, del 9 al
  27 de marzo de 2026 la ventana congelada en `ventanas.yaml` saldría una hora tarde (§3.6). Entra
  en la Next Action en el commit del contrato, al cerrar (añadido 2 del consultor).
- **Para la fila de `trabajo/activacion-a42` en ERRORES-RECURRENTES, al cerrar** (añadido 4; esa
  tabla no se toca en esta rama):
  - (a) el consultor listó, por el puente y de forma recursiva, una carpeta que contiene meses
    reservados (nombres y tamaños de las subcarpetas de marzo, mayo y septiembre, sin abrir
    ninguno); la sesión hizo lo mismo con un `ls` no recursivo (§1.3). Lección, la del cierre de
    `trabajo/reloj-invierno`: nunca se lista una carpeta que contiene meses reservados; cada
    fichero se nombra por su ruta literal;
  - (b) el consultor dio un prompt que afirmaba la CI de `main` en verde con un hueco «<NÚMERO>»
    sin rellenar, y la rama se borró con esa afirmación (salió bien: run #226 en verde). Lección:
    un prompt del consultor no afirma un hecho con un hueco; o lo comprueba él, o el prompt manda
    comprobarlo.

## 7. Fase 0 f · Declaración de lo leído

Fila del 2026-10-06 en `docs/validation/HOLDOUT-EXPOSICIONES.md`, escrita el mismo día:

- ninguna captura abierta;
- de las filtradas, solo marcas, recuentos y sha256;
- ningún libro, ninguna vela y ningún fotograma;
- los nombres que enseñó el `ls` de §1.3.

Nada de febrero ni de julio. De marzo, el nombre de su subcarpeta.

## 8. Lo que cambia esta rama hasta aquí

- `docs/encargos/trabajo-activacion-a42.md`, `contrato.yaml`, el Archivo 20 de `HISTORIA.md` y
  `PROJECT_STATE.md` (`Current Branch`, `Current Feature` y las dos líneas del archivo).
- Una nota al final de `HISTORIA.md`, por orden del consultor del 2026-10-06: la CI de `main` sobre
  e97af27 es el run #226, que el registro de cierre de `trabajo/reloj-invierno` no pudo llevar.
- `docs/validation/ACTIVACION-A42.md` y `docs/validation/anexos/ACTIVACION-A42/` (tres guiones y
  sus salidas).
- Una fila en `docs/validation/HOLDOUT-EXPOSICIONES.md`.

El contrato solo permite hoy esas rutas. Las de la fase 1 se añaden tras la respuesta.

## 9. Fase 1

Por el orden del encargo, un commit por paso, cada uno con su `Fuente:`. El contrato se amplió con
las rutas de la fase 1 en el commit del paso 1 (no en uno propio, como decía §5.6: ahorra un
`make check` y el contrato lo explica en su cabecera).

### 9.1 Paso 1 · El corpus

- **El renombrado lo hizo Aleks, no la sesión.** La guardia bloquea también `mv` sobre una imagen
  del material adicional («origen de `mv`: a.png», misma regla que §1.2), y no se rodea: Aleks
  ejecutó los ocho `mv` en su terminal (prefijo `!`), con los nombres del encargo. Los sha256
  después del renombrado son los de la tabla de §1.1, fichero a fichero.
- `knowledge/corpus/fuentes.yaml`: la entrada de «Mensajes del trader» crece con las ocho capturas,
  su fecha de entrega, su papel (entrada de la activación de A-42) y las cautelas: dos números del
  trader, los dos suyos y confirmados por Aleks, sin ningún nombre ni número en el repo; los
  literales transcritos por el consultor porque la guardia no deja abrir las imágenes; y los tres
  mensajes sobre el stop, que no se registran ni se interpretan.
- `uv run botsito corpus inventory`: «OK: manifiesto escrito»; `material_adicional` pasa de 51 a 59
  ficheros. Las ocho entradas nuevas de `manifest.yaml` llevan los sha256 de §1.1.

### 9.2 Paso 2 · ADR-0069, antes de citarlo en ningún sitio

`docs/adr/0069-a42-las-sesiones-son-velas-h4-de-la-rejilla.md`, con su fila en el índice. Decide
H2b con el porqué del encargo, la puerta del motor (`rejilla_h4`, `sesiones_primera_vela_h4`, las
horas nominales), `huso_grafico` = Europe/Madrid por la medida (D3), qué se registra y qué queda
en el corpus (D2, D4), lo que no cambia y el pendiente de marzo. Deja superado ADR-0059: su
estado y su recuadro cambian en el paso 6, con las demás correcciones. A partir de aquí el
informe lo cita por su id (hasta este commit no podía: `knowledge validate` rechaza un id que no
existe).

### 9.3 Paso 3 · Los registros del trader

Carpeta nueva `knowledge/feedback/2026-10-04-sesion-04/` (los mensajes contestan a S-7, de la sesión
4; `recibido_el: 2026-10-06`, `medio: escrito`, `procedencia: trader_escrito`), creados con
`botsito feedback new`:

| Id | Objetivo y acción | Literal | Captura (en `notas` y en `registrado_por`, con su sha256) |
|---|---|---|---|
| `fb-2026-10-04-sesion-04-fb7831cc` | `ambiguedad` A-42, `RESOLVE_UNKNOWN`, valor `rejilla_h4` | «1-B) 2-c) la orden se pone y se ejecuta cuando ocurre la mitiga ion» | `mensaje-whatsapp-2026-10-06-1544-respuestas-1b-2c.png`; en `notas`, la pregunta de las 15:38 literal (D2) y que «2-c)» no se interpreta |
| `fb-2026-10-04-sesion-04-af490a3a` | `evidence` `ev-v10-010429-0c93f24a`, `CONFIRM` | «si es por cuestion horaria se oepra a las 6» | `mensaje-whatsapp-2026-10-06-1345-se-opera-a-las-6-y-stop.png`; en `notas`, que el 13:46 de la misma captura no se registra |

- `registrado_por`, como pide D1: «literal transcrito por el consultor de la captura <ruta>
  (sha256 <hash>); la sesión no la abrió porque la guardia lo impide (ADR-0038). El trader, desde
  sus dos números, confirmado por Aleks el 2026-10-06».
- **El salto de línea de la burbuja de las 15:44 queda como un espacio.** El modelo de feedback
  normaliza todo espacio en blanco (`comun/documentos.normalizar_texto`: `" ".join(split())`), y el
  id es el hash de ese contenido normalizado: un registro no puede conservar el salto. Las palabras
  son las de la burbuja, en su orden; la forma la conserva la captura.
- F2, F4, F5 y F6 no se registran (D3 y D4): están en el corpus, en `fuentes.yaml` y citados
  literales en ADR-0069 §4.
- `knowledge validate`: OK. `feedback apply --sesion 2026-10-04-sesion-04 --check`: «la sesion no
  propone ningun valor de parametro», que es lo esperado: `reloj_sesiones` y `huso_grafico` cambian
  por decisión (ADR-0069), no por `apply`. `feedback pending` lista el `RESOLVE_UNKNOWN` con «A-42
  esta ABIERTA» hasta el paso 4.

### 9.4 Pasos 4 y 5 · La spec y el motor, en UN commit (y por qué)

**Los pasos 4 y 5 van juntos.** D5 (a) pedía A-42 RESUELTA y `huso_grafico` en el paso 4 y el
selector con el motor en el 5, para que ningún commit quedara en rojo. Medido al preparar el 4:
`tests/contract/test_provisional_cuelga_de_abierta.py` exige que todo parámetro
`DEFAULT_AMBIGUOUS` cuelgue de una ambigüedad ABIERTA, y `reloj_sesiones` cuelga de A-42. Con
A-42 RESUELTA y el selector todavía en `civil_operativa`, el paso 4 solo quedaba en rojo; por el
motivo mismo de D5 se juntan. Dos desviaciones más, medidas:

- **`huso_grafico` pasa a categoría `ejecucion`.** D3 fija su fuente en ADR-0069, y
  `tests/unit/test_registro.py::test_fichero_real_cada_valor_de_estrategia_cita_al_trader` exige
  que un valor de estrategia venga de `feedback` o `evidence`, nunca de un ADR («un numero de la
  operativa lo dice el trader, no lo decidimos nosotros»). Este no lo dice el trader: lo dice la
  medida. La descripción del parámetro lo explica.
- **`sesiones_primera_vela_h4` declara `consumido_por: [ADR-0069]`**: ninguna forma lo lee (lo lee
  la puerta), y `problemas_de_spec` exige saber quién lo consume.

**La spec** (`spec_version` 15.8.0 → 15.9.0: entra un parámetro):
- `ambiguedades.yaml`: A-42 `RESUELTA`, con la respuesta, los dos registros y los dos ítems de v10
  en su evidencia (D6); el comentario de «UTC+2 fijo» queda corregido encima, como historia.
- `parametros.yaml`: `reloj_sesiones` → opciones `[civil_operativa, grafico, rejilla_h4]`, valor
  `rejilla_h4`, `CONFIRMED`, sin `ambiguedad_id`, fuente ADR-0069; `sesiones_primera_vela_h4`
  nuevo (3, `ejecucion`, ADR-0069); `huso_grafico` → `Europe/Madrid`; `ventana_inicio` y
  `ventana_fin` conservan valor, huso y fuente, y su unidad dice «hora NOMINAL»; la descripción
  de `anclaje_h4`.
- `strategy_spec.yaml`: las formas de RN-001 y RN-002 **no cambian**; cambian el título de RN-001
  («las dos velas H4 del trader»), sus `notas` (lo de «manda SU horario, no la rejilla» queda
  corregido) y las de RN-002, y su `decision` pasa a ADR-0069.
- Los cinco sitios de cerrar una ambigüedad: el YAML, la fila de PROJECT_STATE, la hoja
  (`scripts/hoja_preguntas.py` y su test), `test_kit.py` y `spec docs --escribir`.

**El motor**, todo por `src/botsito/engine/relojes.py`:
- `RelojSesiones`, la única puerta: `instante(dia, "HH:MM")`, `lectura(instante)`,
  `limites_de_sesiones(dia, sesiones)`, `apertura(dia)` y `huso_visible`. Con `rejilla_h4` la
  apertura sale de `limites_del_dia` (`data/agregacion.py`); con `civil_operativa` y `grafico`,
  hora de pared en su huso; `de_pared(huso)` para los guiones de ramas cerradas que siguen dando
  `huso_operativa` al arnés (ADR-0063 §5), que así no se rompen.
- `DiaDeMercado` gana `reloj` (opcional: sin él, hora de pared en `huso`, que es lo que los tests
  sintéticos construyen) y `limites()`; `motor.py` y `cableado.py` lo usan; `arnes.py`, `cli.py`,
  `simulacion.py`, `visor.py` y los dos scripts pasan el reloj; `primitivas.py` lee `en_ventana` y
  `alcanza_hora` por la puerta y pierde el helper `_local`. El visor pinta en `huso_visible`
  (`huso_grafico`): en el material de hoy, las mismas horas que antes.
- Guardias de la puerta: una sesión que no sea una vela H4 entera de la rejilla y un día de rejilla
  con vela irregular fallan con nombre.

**Los tests** (`tests/unit/test_sesiones_rejilla_h4.py`, 15 funciones, 40 casos): las fechas del
encargo en UTC (apertura, segunda sesión y cierre, y la lectura inversa); H2a y H1 dan otra hora
exactamente en los días previstos (§5.1); ningún desfase fijo (dos horas UTC en 2024–2027, cada
apertura es un límite de la rejilla, ningún desfase de UTC reproduce el año, con un ancla sin
cambio de hora fallan las fechas de verano, y el código de la puerta no lleva `Etc/GMT`, un
`timezone(` fijo, `timedelta(hours` ni una hora escrita); **el añadido 1 del consultor: ningún día
laborable de 2024 a 2027 cae en la guardia de la vela irregular** (pasa: no hay PARADA); las
guardias; `en_ventana` por la rejilla; el motor de punta a punta el lunes 26 de octubre de 2026
(abre a las 05:00 y 09:00 UTC); el día de riesgo no se mueve; y fuera de los 20 días de §5.1 la
rejilla es la ventana civil en todo 2026. Los que fijaban el estado anterior se actualizan:
`test_dos_relojes.py` (el fixture `registro` vuelve el selector a `civil_operativa`, y
`en_el_grafico` escribe el UTC+2 fijo de H1 como hipótesis), `test_huecos_motor.py` (H2),
`test_registro.py`, `test_kit.py`, `test_hoja_preguntas.py`.

### 9.5 Medido sobre construcción: el arnés sale idéntico byte a byte

Como hizo ADR-0063: `botsito motor arnes` sobre los meses de construcción, con los mismos
diagnósticos (`--diagnostico-a35 cierre_vela_contraria --diagnostico-a44 sin_tope
--diagnostico-a21 solo_una_zona_de_control`; sin ellos el motor se niega, A-21 y A-35 sin fijar),
en `main` (e97af27, en un worktree desechable en la carpeta temporal, con `data` apuntando al de
esta máquina por `settings.local.toml`) y en la rama (85b3be6, con `rejilla_h4`). Los dos informes
dan el mismo sha256, `4f512303e056795ab53a…`, 175 líneas. Ningún instante de ninguna sesión cambia
en el material de hoy, que es lo que §5.1 predecía por calendario. Los informes quedan fuera del
repo (son corridas en hipótesis, sin valor de medida).

### 9.6 Paso 6 · Las correcciones con recuadro, y la deuda

Con el recuadro `CORRECCIÓN (2026-10-06, rama trabajo/activacion-a42, ADR-0069)` donde el documento
está cerrado, y el cuerpo intacto:

| Documento | Qué corrige |
|---|---|
| ADR-0039 | el «es UTC+2 fijo» del problema que resuelve; lo que decide del huso de cada libro no cambia |
| ADR-0059 | `status: SUPERSEDED`, recuadro con el porqué y `## Estado` «SUPERSEDED por ADR-0069»; el índice de ADR lo dice |
| ADR-0017 | el punto 4 vuelve a Europe/Madrid; los puntos 1 y 5 quedan corregidos para las sesiones; `huso_operativa` sigue siendo el reloj civil y el del día de riesgo |
| `ABRIL-Y-LA-CAJA.md` R0 | el «UTC+2 fijo» es el reloj del pie, que va con el replay; lo medido en abril no cambia |
| `MIRAR-EL-MATERIAL.md` | el reloj de los gráficos es Europe/Madrid; la regla de fijar el huso antes de comparar sigue, y para invierno el desfase es 1 |
| `ENTRADA-MARZO.md`, PARADA B0 | la condición se cumple pero su motivo no: `cases/` a la rejilla antes del paso b, pendiente con dueño (D7, añadido 2); nada de marzo abierto ni listado |
| `docs/runbooks/README.md` y `CLAUDE.md` | la frase del reloj de FX Replay (D7); `CLAUDE.md` manda corregirse en el mismo commit que deja de ser cierto |
| `ambiguedades.yaml`, A-42 | el comentario, ya en el paso 4 (§9.4) |

**Technical Debt:** «EL «UTC+2 FIJO» FALLA EN ENERO» queda pagada por ADR-0069 y sale de
PROJECT_STATE a HISTORIA (`# Technical Debt PAGADA`). De «LA SERIE DEL TRADER ES OANDA Y LA NUESTRA
DUKASCOPY, Y EL RELOJ DE SU GRAFICO ES UTC+2 FIJO» sigue viva la parte de la serie: la línea lo dice
y conserva su arranque literal, que es como se busca en HISTORIA.

**Lo que no se toca:** la Next Action (E sale en el commit del contrato, al cierre, con el pendiente
de marzo del §6.2); `docs/runbooks/ERRORES-RECURRENTES.md` (su fila, al cierre, con los hallazgos
de §6.2 y los del revisor); `docs/HANDOFF.md` (su mención del 2026-09-21 es historia fechada).

## 10. Lo que cambia esta rama

- **Corpus:** las 8 capturas renombradas (por Aleks), `fuentes.yaml` y `manifest.yaml`.
- **ADR-0069** nuevo; recuadros en ADR-0017, ADR-0039 y ADR-0059 (SUPERSEDED); el índice.
- **Feedback:** `knowledge/feedback/2026-10-04-sesion-04/`, dos registros.
- **Spec** (15.8.0 → 15.9.0): A-42 RESUELTA; `reloj_sesiones` = `rejilla_h4`;
  `sesiones_primera_vela_h4`; `huso_grafico` = Europe/Madrid (`ejecucion`); descripciones;
  RN-001 y RN-002 (notas, título, `decision`); `docs/spec/` regenerado.
- **Motor:** `engine/relojes.py` (la puerta), `primitivas.py`, `motor.py`, `cableado.py`,
  `arnes.py`, `simulacion.py`, `visor.py`, `cli.py`, dos scripts.
- **Tests:** `test_sesiones_rejilla_h4.py` nuevo; `test_dos_relojes.py`, `test_huecos_motor.py`,
  `test_registro.py`, `test_kit.py`, `test_hoja_preguntas.py`; `scripts/hoja_preguntas.py`.
- **Documentos:** R0 de ABRIL-Y-LA-CAJA, MIRAR-EL-MATERIAL, ENTRADA-MARZO (B0), el README de
  runbooks, `CLAUDE.md`; una fila de HOLDOUT-EXPOSICIONES; una línea menos y otra ampliada en
  Technical Debt; HISTORIA (Archivo 20, la nota del run #226 y la deuda pagada); este informe y sus
  anexos.
- **Fuera del repo:** las filtradas de v7–v10, rehechas (§2.2).

## Estado

**EN CURSO (2026-10-06): fase 1 hecha hasta el paso 6; faltan la CI de Linux (`fix/activacion-a42`)
y el revisor.**

- A-42 RESUELTA (ADR-0069): las dos sesiones son las velas H4 de la rejilla de `anclaje_h4`; el bot
  las fija en instantes UTC con zoneinfo, por una sola puerta, nunca con un desfase fijo.
- `huso_grafico` = Europe/Madrid; los textos de «UTC+2 fijo» llevan su recuadro; la deuda, pagada.
- En construcción nada cambia (el arnés, byte a byte, §9.5); lo primero que cambia es la semana del
  26 al 30 de octubre de 2026 (05:00 UTC).
- **Sin verificar por la sesión:** los literales de las 8 capturas y las etiquetas del eje de b y c:
  la guardia bloquea las imágenes y vale la lectura del consultor (D1), con la captura y su hash en
  cada registro.
- **Pendiente con dueño:** `cases/` por la rejilla, en la rama de entrada de marzo, antes de su
  paso b (§6.2). La PARADA B0 cumple su condición y no su motivo.
- Marzo, febrero y julio: nada abierto ni listado (salvo el nombre de la subcarpeta de marzo en el
  `ls` de §1.3, declarado).
