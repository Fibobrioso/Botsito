# El reloj de invierno: qué reloj tiene el gráfico del trader y a qué horas UTC opera en enero

Rama `trabajo/reloj-invierno`, abierta el 2026-10-06 desde `main` en 25469ff (tag
`stable/F37b-guardias-citas`). Encargo: `docs/encargos/trabajo-reloj-invierno.md`. Es una rama de
MEDIDA, previa a la activación de A-42 (Next Action E): no cambia motor, spec, parámetros,
ambigüedades, evidencia ni corpus.

## 1. Las hipótesis del consultor, tal cual (escritas ANTES de medir)

- H1 (lectura de ADR-0059): gráfico en UTC+2 fijo y sesiones fijas 07–15 en ese reloj; en enero opera 05:00–13:00 UTC.
- H2: gráfico en Europe/Madrid con cambio de hora (el selector muestra el desfase de hoy); en enero opera 06:00–14:00 UTC. Dos variantes que enero no separa: H2a, 07–15 de reloj civil de Madrid; H2b, las sesiones son las velas H4 de la rejilla de anclaje_h4 que en verano caen 07–11 y 11–15 (01:00–09:00 de Nueva York). Solo se separan cuando Europa y EE. UU. no coinciden en el cambio de hora.
- Hoy el UTC+2 fijo sale del fotograma fr-v4-9ad0ebb8/1200000 («14:29:59 UTC+2» sobre «Thu 29 Jan '26», ABRIL-Y-LA-CAJA.md R0). v4 se grabó el 2026-08-30 (MESES-VISTOS.md), en verano: si el reloj del pie da la hora real de la grabación, marcaría +2 también con H2.

**La regla de M2, escrita en el encargo antes de medir** (copiada del encargo, que entra en el
primer commit de la rama, antes de cualquier salida de M2):

- H2 si hay ≥3 en [13:00, 14:00) y 0 en [05:00, 06:00);
- H1 si hay ≥3 en [05:00, 06:00) y 0 en [13:00, 14:00);
- cualquier otra cosa, NO CONCLUYENTE.

## 2. La respuesta del trader al punto E: NO se registra en esta rama

El encargo pedía registrarla como feedback (medio escrito, literal) y parar si el procedimiento
pedía algo que no estuviera en él. Lo pedía, y se paró antes de abrir la rama:

- **No hay acción que apunte a A-42 dejándola ABIERTA.** Sobre una ambigüedad, el modelo de
  feedback solo admite `RESOLVE_UNKNOWN` -que la cierra y exige valor- y `REOPEN` -que exige un
  cierre previo- (`src/botsito/feedback/modelo.py`, `OBJETIVOS_POR_ACCION`).
- **Sobre `huso_grafico` o `reloj_sesiones`**, `CONFIRM` y `CORRECT` son acciones que
  `feedback apply` escribe en el parámetro (`ACCIONES_QUE_FIJAN`, `feedback/aplicar.py`). Y leer
  «etc+2 madrid» como Etc/GMT-2 o como Europe/Madrid es justo lo que esta rama mide.
- **No existe todavía** `knowledge/feedback/2026-10-04-sesion-04/`.
- **No hay captura del texto del WhatsApp en el corpus**, y `knowledge/feedback/README.md`
  («Material que llega fuera de sesión», pasos 1-4) la pide para `procedencia: trader_escrito`.

**Decisión del consultor (2026-10-06, en el terminal, literal):**
1. Sobre el registro: «Aplazarlo». No se crea registro en esta rama. El texto literal ya entra al
   repo en `docs/encargos/trabajo-reloj-invierno.md` y se cita en el informe. El registro se hace
   en la activación de A-42.
2. Sobre la procedencia: «trader_escrito con captura, pero en la activación de A-42, no en esta
   rama. Antes de esa rama, Aleks deja en «Mensajes del trader» la captura del texto del WhatsApp
   (solo los mensajes de 09:53 y 09:59 del 2026-10-06, sin la captura del selector), y también la
   de sus respuestas al mensaje nuevo cuando lleguen; la activación las pasa por fuentes.yaml e
   inventory. Motivo: una respuesta referida por el consultor es lo que dejó a A-11 sin respaldo
   literal (GUARDIAS-CITAS.md §8 y §9.3), y no repetimos eso con A-42. En esta rama no se registra
   nada.»

Lo que el trader escribió, tal como lo trae el encargo (2026-10-06, hora de Lima): 09:53 «según la
configuración de la plataforma etc+2 madrid»; 09:59 «xd» «sep» «seria cuestion que se adapte a lo
que bote la plataforma». No dio las horas de cierre de las velas de 4 horas. Aquí se usa solo como
contexto: ninguna medida de esta rama depende de cómo se lea.

## 3. Fase 0: inventario, sin tocar nada

### 3.a Ningún día de enero de 2026 en ninguna partición

`casos_reservados(repo)` y `casos_ocultos(repo)` sobre los 4 repartos commiteados
(`repartos_commiteables`), el 2026-10-06 en 25469ff:

```
repartos 4
reservados total 34 ocultos total 34
2026-01 reservados 0 ocultos 0
2026-04 reservados 0 ocultos 0
2026-08 reservados 0 ocultos 0
meses_libres contiene 1,4,8: True
```

Enero sale limpio, y también los dos meses de control (abril y agosto). Ninguno de los tres está en
`knowledge/cases/meses_reservados.yaml`. **Sigue la fase 1.**

### 3.b El libro de enero y sus velas

- Fichero: `corpus/Estrategia del trader/Material adicional de su operativa/backtesting-analytics ENERO 2026.xlsx`,
  11.991 bytes.
- sha256 `ee4ade46094c73c1f1de0043acc5345cf7fa42c729b71a4b57d781002554ab86`, el mismo que
  inventaría `knowledge/corpus/manifest.yaml` para esa ruta.
- **No está en `knowledge/corpus/libros.yaml`**: ni su sha ni «ENERO» aparecen (la cabecera del
  fichero lo dice: «NO ESTAN enero ni septiembre»). Sin entrada, el lector no lo abre: M1 lo lee
  con una declaración EN MEMORIA por huso, que es la hipótesis que se mide, como hace
  `scripts/huso_por_velas.py`.
- Velas: `uv run botsito data check --dataset eurusd-m1-2026-01-e37291d4 --hashes` → `OK: ...
  coincide con el disco (hashes)`. Su manifiesto: 31 días presentes, 0 ausentes, 5 sin datos (los
  cinco sábados), primera vela 2026-01-01T22:04Z, última 2026-01-30T21:59Z. Los de control,
  `eurusd-m1-2026-04-990211bd` y `eurusd-m1-2026-08-0d42230e`, también `OK (hashes)`.

### 3.c Fotogramas de v4 y lo que localiza la transcripción

- `data/fotogramas/v4/png-1fps/` tiene 5.620 PNG a 1 fps. Alrededor de 1200000 están los 100 de
  `001150000.png` a `001249000.png`, sin hueco. No se abrió ninguno en la fase 0.
- **La transcripción filtrada de v4 no localiza ningún instante en que el trader lea en voz alta la
  leyenda O/H/L/C de una vela de enero.** Búsquedas con `kb find --video v4 --solo cruda --prefijo`
  (filtradas; 26 segmentos ocultos por material reservado o sin sortear en cada una): «enero»,
  «apertura», «cierre», «máximo», «mínimo», «open», «close», «high», «low» y «vela». La única
  mención de enero es 1:11:48 («Para este mes de enero, pero no, o sea», segmento 1225), sin
  ningún precio.
- Alrededor de 1200000 la transcripción localiza: `ev-v4-001909-54ac2edd` (0:19:09, fotograma
  1149000), `ev-v4-001954-10576ea4` (0:19:54, 1194000) y el segmento 353 (0:20:00.755–0:20:48.225,
  1200000), en el que el trader explica una operación de ejemplo. Es el vecindario de un instante
  ya citado, así que cuenta como localizado (ADR-0038) para M3.

**Consecuencia para M3:** la fase 0 c no da una vela de enero con leyenda y hora del eje. La
comparación con Dukascopy de M3 solo se hace si los fotogramas de 1200000 que M3 abre la traen
ellos mismos; si no, se dice y no se busca en otro sitio.

### 3.d Lo que se va a leer, declarado el mismo día

Fila del 2026-10-06 en `docs/validation/HOLDOUT-EXPOSICIONES.md`.

### 3.e Lo que se vio de pasada durante el inventario, y no se debió ver

Dos listados tocaron nombres de febrero, marzo o septiembre. Ningún contenido.
- `ls` de `Material adicional de su operativa/`: enseñó los nombres de sus subcarpetas, entre ellas
  `Backtest marzo 2026` y `Backtest septiembre 2026`.
- Un `grep` de «backtesting-analytics» sobre `knowledge/corpus/manifest.yaml`: enseñó las líneas
  de RUTA de los libros de marzo y septiembre, ya commiteadas en el inventario. Ni sha, ni tamaño,
  ni nada de dentro.

Nada de julio ni de febrero. Desde aquí, ningún listado de esa carpeta: las rutas de enero, abril
y agosto se nombran enteras.

## Estado

EN CURSO. Fase 0 entregada; fase 1 (M1–M4) en marcha.
