# La ventana declarada de ev-v9-003456-9ef48fb5

Rama `trabajo/ventana-ev-v9-003456`, abierta el 2026-10-05 desde `main` en `fffaa03` (commit de
estado; tag `stable/F36y-filtradas-con-tramos` en `06adac1`). Encargo:
`docs/encargos/trabajo-ventana-ev-v9-003456.md`. Es el punto R de la Next Action.

**v9 es material en cuarentena.**
- Las medidas usan solo `n`, `t0_ms` y `t1_ms` de los segmentos, por la misma vía que
  `FILTRADAS-ESCENARIO-B/ancla_v9.py`: `construir_contexto`, `contexto.crudas` y `verificar_citas`.
- No se imprime texto, ni palabras, ni longitudes de cita.
- No se ha abierto ninguna filtrada de v7–v10.

## 0. Fase 0: el inventario, sin tocar nada

### 0.a El régimen que corrige la ventana de un ítem

- **La regla:** `knowledge/evidence/` es **INMUTABLE tras commit**. Una corrección es **un ítem nuevo
  que supersede** al viejo, con el **mismo tema** (`CLAUDE.md`, «Regímenes de cambio», líneas
  60-63).
  - La guardia es el hook `pre-commit`, que impide editar un ítem commiteado.
  - El «mismo tema» lo comprueba `evidence/modelo.py:355-363`: «una corrección habla del mismo tema».
  - El ítem viejo no se borra ni se edita: sigue en el repo, y el nuevo lleva `supersede:
    ev-v9-003456-9ef48fb5`.
  - La vía de propuesta (`evidence propose --check` + `accept`) no admite `supersede` (misma cita
    de `CLAUDE.md`).
- **La vía por la CLI existe:** `uv run botsito evidence new --supersede <id>`. Pero pide en la
  línea de comandos `--cita` (la cita literal) y `--afirmacion`.
  - Para usarla, la sesión tendría que leer el texto del ítem viejo y escribirlo en un comando.
  - Eso choca con la regla de esta rama («no imprimas texto»). No rodea ninguna guardia.
- **Propuesta, para autorizarla a la vista:** un anexo, `docs/validation/anexos/VENTANA-EV-V9/
  sustituir_item.py`, que hace **lo mismo que `evidence new`**, sin que el texto pase por la sesión:
  1. carga el ítem viejo con `cargar_evidencia`;
  2. construye los `campos` del nuevo copiando los suyos, salvo `t0` (el nuevo), `supersede` (el
     id viejo) y `notas` (la razón, con la referencia a `FILTRADAS-ESCENARIO-B.md` §4.1). La cita,
     la afirmación, el tema, el tipo, la confianza y la transcripción quedan igual;
  3. escribe con **`escribir_item(directorio, campos, entorno.comprobar)`**, la función y la
     comprobación de la CLI (`cli.py:1034` y `_EntornoEvidencia.comprobar`, `cli.py:621-662`):
     manifiesto, transcripción activa, `tramo_no_citable` y `verificar_citas`;
  4. imprime solo el id nuevo y la ruta.

  **El consultor decide quién figura en `revisado_por`.** Hoy lleva el del ítem viejo. Propuesta:
  el consultor, con la fecha de su orden.

### 0.b La medida

Anexo: `docs/validation/anexos/VENTANA-EV-V9/medir_ventana.py`, con su salida en
`medir_ventana-SALIDA.txt`.

**«Segmento en cuarentena»**, operativamente: todo segmento de la cruda de v9 que se solapa más de
0 ms con un tramo no citable de v9, contando el tramo de margen del punto c (añadido en memoria).

| Medida | Valor (ms) |
|---|---|
| Ventana declarada hoy | 2.096.000–2.100.000 |
| Segmento 612 (en cuarentena) | 2.096.380–**2.096.900** |
| Segmento 613 (no en cuarentena) | **2.098.060–2.100.240** |
| Segmento 614 (no en cuarentena) | 2.100.880–2.101.320 |
| Hoy, con `verificar_citas` | 0 problemas, 1 aparición; palabras en el segmento 613 (2.098.060–2.100.240) |

**Ventanas candidatas** (fin en 2.100.000; mismo ítem con su `t0` cambiado en memoria):

| t0 | Solapa segmentos en cuarentena | Solapa un tramo | Problemas | Apariciones | Cumple |
|---|---|---|---|---|---|
| 2.094.000 (0:34:54) | 612 | sí | 0 | 1 | no |
| 2.095.000 (0:34:55) | 612 | sí | 0 | 1 | no |
| 2.096.000 (0:34:56, hoy) | 612 | sí (el de margen) | 0 | 1 | no |
| **2.097.000 (0:34:57)** | ninguno | no | 0 | 1 | **SÍ** |
| 2.098.000 (0:34:58) | ninguno | no | 0 | 1 | sí |

**Ventana nueva: 2.097.000–2.100.000 ms (0:34:57–0:35:00).**
- Es el segundo entero más temprano que cumple las tres condiciones.
- **El fin actual (2.100.000) sigue cumpliendo.** Las palabras acaban en 2.100.240, 240 ms después,
  dentro de la tolerancia de 2 s de `localizar_cita`. No solapa el segmento 614 ni ningún tramo.

### 0.c El tramo de margen 0:34:44–0:34:57

Entra solo añadiendo, como 2.084.000–2.097.000 ms.
- **Solape con la ventana nueva: 0 ms**, porque la ventana empieza justo donde acaba el tramo.
- Con él, el segmento 612 queda entero dentro de un tramo, y el bloque de B de 34:44 (hasta
  2.096.900) cabe entero.

**Consecuencia, para el consultor.**
- El ítem **viejo** sigue en el repo (es inmutable), y su ventana (desde 2.096.000) **sí solapa
  1.000 ms el tramo de margen**.
- Dos controles cuentan hoy **todos** los ítems, superseded incluidos:
  - `tests/unit/test_tramos_de_sesion.py::test_ningun_item_de_las_sesiones_solapa_un_tramo`;
  - el anexo `FILTRADAS-ESCENARIO-B/tramos_registrados.py`.
- Con el tramo de margen, los dos marcarían el ítem viejo. **El «0 ítems» de la fase 5 solo puede
  cumplirse contando los ítems activos** (los que ningún otro supersede).
- Propuesta:
  - el test pasa a contar solo los activos;
  - el control de la fase 5 va en un anexo nuevo de esta rama, que no toca el de la rama cerrada y
    cuenta los activos, diciendo cuántos superseded deja fuera (1).

### 0.d Quién cita ev-v9-003456-9ef48fb5, y por qué régimen se mueve cada referencia

Búsqueda del id en todo el repo: 31 apariciones en 14 ficheros. **Ninguna en `knowledge/feedback/`
ni en la spec de reglas (`strategy_spec.yaml`, `parametros.yaml`).**

| Dónde | Qué es | Régimen | Propuesta |
|---|---|---|---|
| `knowledge/evidence/v9/ev-v9-003456-9ef48fb5.yaml` | el ítem | inmutable | no se toca; el nuevo lo supersede |
| `knowledge/spec/ambiguedades.yaml:1280` | la lista `evidencia` de **A-46** (RESUELTA) | versionado, con trailer `Fuente:` y `botsito spec docs --escribir` si cambia lo generado | **decide el consultor**: (i) sustituir el id por el nuevo, o (ii) añadir el nuevo junto al viejo. A-46 no se reabre: la evidencia sigue diciendo lo mismo |
| `PROJECT_STATE.md` (punto R) | la Next Action | presente | R sale a HISTORIA al cerrar esta rama |
| `docs/state/HISTORIA.md` (3) | archivo | solo se amplía | no se toca |
| `docs/encargos/trabajo-filtradas-escenario-b.md` (4) y el de esta rama (2) | copias literales | no se editan | no se tocan |
| `docs/validation/FILTRADAS-ESCENARIO-B.md` (10) | informe cerrado | recuadro de corrección | recuadro en el §4.1 y el §4.3: el ítem está superseded por el nuevo, con su ventana (y lo del punto e) |
| `docs/validation/SESION-03-EXTRACCION.md` (1) | informe cerrado (ítems de A-46) | recuadro | recuadro junto a la lista de ítems de A-46 |
| `docs/validation/CUARENTENA-POR-DEFECTO.md` (1) | informe cerrado, una tabla del estado de entonces | recuadro, o nada | **nada**: la tabla describe lo que era cierto aquel día |
| `docs/validation/anexos/FILTRADAS-ESCENARIO-B/` (`ancla_v9.py`, sus salidas, `tramos_nuevos-SALIDA.txt`) | anexos de una rama cerrada | instantáneas | no se tocan: el ítem viejo sigue existiendo, y `ancla_v9.py` sigue corriendo |
| `docs/validation/anexos/VENTANA-EV-V9/` | anexos de esta rama | — | nombran el id viejo a propósito |

### 0.e ¿Falla algo hoy si la ventana de un ítem solapa más de 0 ms un tramo o un segmento en cuarentena?

**Con un tramo:**
- **Al crear un ítem, sí.** `evidence new` (`cli.py:628`) y `evidence propose --check`
  (`evidence/propuestas.py:404`) llaman a `tramo_no_citable` (`evidence/verificacion.py:358`), con
  la condición de más de 0 ms.
- **Sobre los ítems que ya existen, `knowledge validate` no lo comprueba.** No llama a
  `tramo_no_citable`.
  - Lo único que lo mira es un test, `test_tramos_de_sesion.py::test_ningun_item_de_las_sesiones_solapa_un_tramo`,
    y solo para v7–v10.
  - Un tramo nuevo que pise un ítem viejo de otro vídeo no hace fallar nada.
  - **Corrección de un informe cerrado:** `FILTRADAS-ESCENARIO-B.md` §4.3 dice que
    `tramo_no_citable` «hace que `knowledge validate` y `evidence new` rechacen» el ítem. Validate
    no lo hace. Va en un recuadro (fase 3).

**Con un segmento en cuarentena que el tramo no cubre entero:** **ninguna comprobación.** Es el
caso de este ítem: el tramo original acaba en 2.096.000 y el segmento 612, en 2.096.900.

**Propuesta, por condición:**

> La ventana declarada [t0, t1) de todo ítem **activo** (que ningún otro supersede) no se solapa
> más de 0 ms con ningún tramo no citable de su vídeo, ni con ningún segmento de su transcripción
> citada que a su vez se solape más de 0 ms con un tramo no citable de su vídeo.

**Dónde:**
- Una función en `src/botsito/evidence/verificacion.py`, junto a `tramo_no_citable`.
- `knowledge validate` (`validation/knowledge.py`, junto a `verificar_citas`) la llama sobre todos
  los ítems activos, y es la única vía que recorre todos.
- `evidence new` la llama al crear, para que las dos digan lo mismo.

**Cómo, sin ver texto:** los segmentos salen por `contexto.crudas`, el llamador autorizado de la
verificación de citas, y solo se usan `t0_ms` y `t1_ms`. Sin cruda en la máquina, se mira solo el
tramo y se da un aviso, como hoy `verificar_citas`.

**Coste:** toca `src/` y `tests/`, así que el contrato se amplía en la fase 4.

## Decisiones del consultor tras la fase 0 (2026-10-05)

Copiadas tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Visto bueno a la fase 0 de trabajo/ventana-ev-v9-003456, con estas decisiones. Cópialas al encargo y al informe con fecha 2026-10-05, como decisiones del consultor:
>
> 1. Vía de (a): AUTORIZADA a la vista. Es el anexo que carga el ítem viejo y llama a escribir_item con _EntornoEvidencia.comprobar, la misma comprobación que evidence new --supersede.
>    Porqué: la CLI obliga a leer y reescribir texto en cuarentena, y el anexo pasa por la misma comprobación. No es un rodeo.
>    Condiciones:
>    - el anexo vive en docs/validation/anexos/ y cita el archivo y la línea de la CLI que replica;
>    - comprueba que el ítem nuevo es igual campo a campo al viejo, salvo id, t0, supersede, notas y los campos de fecha o autoría que el modelo genere solo. Lista en el informe los campos que cambian;
>    - solo imprime el id nuevo y el resultado de la comprobación.
>    revisado_por lleva el mismo valor que el ítem viejo, porque la cita no cambia. notas dice: «ventana corregida por orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó». Si notas no admite texto libre, dímelo antes de escribir.
>
> 2. Orden de las fases. Primero el tramo de margen 0:34:44–0:34:57 (fase 2), con Fuente:, sin quitar ninguna línea. Después el anexo, en dos pasadas:
>    - con t0 = 2.096.000, la comprobación TIENE que rechazar el ítem por tramo_no_citable. Pega la salida en el informe. Si lo acepta, para: la vía no pasa por la guardia y no está autorizada;
>    - con t0 = 2.097.000, escribe el ítem nuevo, que supersede a ev-v9-003456-9ef48fb5. Fin en 2.100.000.
>    Porqué: así se demuestra que la vía pasa por la guardia y no la rodea.
>
> 3. A-46: SUSTITUIR el id viejo por el nuevo en ambiguedades.yaml, con Fuente:, y regenerar con uv run botsito spec docs --escribir.
>    Porqué: la spec tiene que citar el ítem activo, y si deja el viejo cita una ventana que pisa un tramo.
>    Mide y di en el informe si algo avisa hoy cuando la spec o las ambigüedades citan un ítem supersedido. Si nada avisa, añade una línea a Technical Debt que apunte a este informe. No lo arregles en esta rama.
>
> 4. Control de la fase 5: se cuentan los ítems ACTIVOS (los que nadie supersede). El anexo nuevo declara cuántos supersedidos deja fuera (se espera 1) y cuáles son.
>    Porqué: un ítem supersedido no se cita.
>
> 5. La condición de (e): APROBADA tal cual la nombras. «La ventana declarada de todo ítem activo no se solapa más de 0 ms con ningún tramo no citable de su vídeo, ni con ningún segmento de su transcripción que a su vez solape un tramo.»
>    - Va en una función junto a tramo_no_citable, en evidence/verificacion.py. La llaman knowledge validate, para todos los ítems activos de todos los vídeos (no solo v7–v10), evidence new y evidence propose --check.
>    - Solo usa milisegundos de los segmentos, por la vía autorizada. Nunca texto.
>    - Antes de activarla, mídela sobre el repo con el ítem ya corregido. Tiene que dar 0 ítems. Si sale cualquier otro, para y entrégame la lista (id, vídeo y ms de solape, sin texto). Su arreglo no entra en esta rama.
>    - Sin la transcripción disponible (por ejemplo, en la CI sin data/), mide qué hace hoy verificar_citas en ese caso y haz exactamente lo mismo. Nunca puede pasar en silencio: si no puede comprobar, lo dice. Declara el comportamiento en el informe.
>    - Tests que la rompen a propósito: ventana vieja → falla; ventana que solo pisa la cola de un segmento que solapa un tramo, sin tocar el tramo (el caso de este ítem) → falla; ventana que toca el tramo a 0 ms → pasa; ítem supersedido que pisa un tramo → no cuenta; ventana nueva → pasa.
>
> 6. Recuadros en FILTRADAS-ESCENARIO-B.md (§4.1 y §4.3, con tu corrección sobre knowledge validate) y en SESION-03-EXTRACCION.md, cada uno con fecha y la referencia a este informe. HISTORIA, encargos, anexos cerrados y la tabla de CUARENTENA-POR-DEFECTO.md no se tocan.
>
> 7. Tu corrección sobre §4.3 entra en el informe como hallazgo, para la fila de ERRORES-RECURRENTES en el cierre: un informe afirmó lo que hacía una comprobación sin medirlo.
>
> Sigue con las fases 1 a 5 y amplía el contrato. CI de Linux: solo si tocas hooks, rutas o algo que dependa de la plataforma; si no, di por qué no hace falta. Después:
> - uv run botsito knowledge validate (exit 0, sin ERROR);
> - uv run python scripts/ficheros_con_ocultos.py;
> - make check sellado;
> - informe completo en VENTANA-EV-V9.md con el revisor al final.
>
> Rama lista para revisión, NO cerrada.

## 1. Lo hecho tras el visto bueno, en el orden que fijó el consultor

### 1.1 Fase 2, primero: el tramo de margen

`knowledge/corpus/tramos_no_citables.yaml` gana una entrada al final: v9, `0:34:44`–`0:34:57`
(2.084.000–2.097.000 ms).
- El motivo nombra el tramo original (segmentos 609-612) y dice por qué se quedó fuera en
  `FILTRADAS-ESCENARIO-B.md` §4.2.
- El diff es +7/−0: no quita ninguna línea.
- v9 pasa de 20 a 21 tramos.

### 1.2 Fase 1: el ítem nuevo, por la vía autorizada, en dos pasadas

Anexo: `docs/validation/anexos/VENTANA-EV-V9/sustituir_item.py`.
- Replica `evidence_new` (`src/botsito/cli.py:988-1040`): los mismos `campos` (cli.py:1014-1032),
  la misma escritura, `escribir_item(entorno.directorio, campos, entorno.comprobar)` (cli.py:1034),
  y la misma comprobación, `_EntornoEvidencia.comprobar` (cli.py:621-662).
- `escribir_item` comprueba **antes** de mirar si el fichero existe (`evidence/modelo.py:429-435`),
  así que un rechazo es de la comprobación y no del id.

**Pasada 1, con t0 = 0:34:56** (`sustituir_item-PASADA1.txt`): **rechazada por
`tramo_no_citable`**, por el tramo de margen 0:34:44.000–0:34:57.000. No escribió nada. La salida,
tal cual:

```
item viejo: ev-v9-003456-9ef48fb5 (2096000-2100000 ms); t0 nuevo: 0:34:56
RECHAZADO por la comprobacion de evidence new: <candidato sin escribir>: el tramo no es especificacion, 0:34:44.000-0:34:57.000: completa el tramo de cuarentena mecanica de la sesion 03 de 0:34:44-0:34:56 (segmentos 609-612 de la cruda), […motivo del tramo…]
```

Sobre el `<candidato sin escribir>`:
- La primera ejecución imprimía el id que habría tenido el candidato.
- `knowledge validate` exige que exista todo id citado en `docs/`, y ese no existe, porque no se
  escribió: dio un ERROR.
- El anexo sustituye ahora ese id antes de imprimir.
- La pasada se repitió y su salida es la misma salvo ese id: sigue rechazada y sin escribir nada.

**Pasada 2, con t0 = 0:34:57** (`sustituir_item-PASADA2.txt`):

```
item viejo: ev-v9-003456-9ef48fb5 (2096000-2100000 ms); t0 nuevo: 0:34:57
ESCRITO: ev-v9-003457-3e28e325 (2097000-2100000 ms), knowledge/evidence/v9/ev-v9-003457-3e28e325.yaml
campos distintos del viejo: ['id', 'notas', 'supersede', 't0']
igual campo a campo salvo ['id', 'notas', 'supersede', 't0']: True
```

**Los campos que cambian:**

| Campo | Viejo | Nuevo |
|---|---|---|
| `id` | `ev-v9-003456-9ef48fb5` | **`ev-v9-003457-3e28e325`** |
| `t0` | 0:34:56 | **0:34:57** |
| `supersede` | — | `ev-v9-003456-9ef48fb5` |
| `notas` | la del viejo | «ventana corregida por orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó» |

**Todos los demás campos son iguales:** `t1` (0:35:00), `cita_literal`, `afirmacion`, `tema`,
`tipo`, `modalidad`, `confianza`, `extractor`, `revisado_por` (el del viejo), `provenance`,
`fotogramas`, `valor` y `transcripcion`. El modelo no genera campos de fecha ni de autoría
(`EvidenceItem`, `evidence/modelo.py:121-138`). `notas` admite texto libre (`str | None`).

### 1.3 Fase 3: las referencias

| Referencia | Qué se hizo |
|---|---|
| `knowledge/spec/ambiguedades.yaml`, A-46, `evidencia` | **sustituido** el id viejo por el nuevo (decisión 3). `botsito spec docs --escribir` no cambia nada: los documentos generados no listan la evidencia de las ambigüedades |
| `FILTRADAS-ESCENARIO-B.md` §4.1 | recuadro: el ítem nuevo lo supersede, y entró el tramo de margen |
| `FILTRADAS-ESCENARIO-B.md` §4.3 | recuadro con la corrección: `knowledge validate` no llamaba a `tramo_no_citable` (§3) |
| `SESION-03-EXTRACCION.md`, ítems de A-46 | recuadro: el viejo, superseded por el nuevo |
| HISTORIA, encargos, anexos cerrados, la tabla de `CUARENTENA-POR-DEFECTO.md` | no se tocan (decisión 6) |

**¿Avisa algo hoy si la spec o las ambigüedades citan un ítem superseded?** **No.**
- Medido con `uv run botsito knowledge validate` con el ítem nuevo ya escrito y A-46 citando todavía
  el viejo: ningún aviso ni error sobre eso.
- `src/botsito/validation/knowledge.py` y `spec/modelo.py` solo miran los registros de feedback
  revocados, no la evidencia superseded.
- Va como **deuda** a Technical Debt de `PROJECT_STATE.md`, con una línea que apunta a este informe.
  No se arregla aquí.

## 2. Fase 4: la condición, escrita y medida, y PARADA

**La función:** `ventana_no_citable(contexto, video_id, t0_ms, t1_ms, segmentos)`, en
`src/botsito/evidence/verificacion.py`, junto a `tramo_no_citable`.
- Implementa la condición aprobada tal cual: el tramo, con el mismo mensaje que hoy, y los segmentos
  que solapan un tramo.
- De los segmentos solo usa `n`, `t0_ms` y `t1_ms`.
- Con `segmentos=None` solo mira el tramo, y quien la llama tiene que decirlo.

**Todavía no la llama nadie.** Antes de activarla, la decisión 5 pide medirla.

**Medida sobre el repo**, con el ítem ya corregido. Anexo `medir_condicion.py`, salida en
`medir_condicion-SALIDA.txt`:
- 502 ítems: 490 activos y 12 superseded, todos los de todos los vídeos;
- vídeos con tramos: v6, v7, v9 y v10;
- cruda presente para todos los activos de esos vídeos;
- control: el ítem viejo, superseded, incumple la condición, como se espera.
- **Activos que la incumplen: 1, distinto de 0. PARADA.**

| id | vídeo | ventana declarada (ms) | qué pisa | ms de solape |
|---|---|---|---|---|
| `ev-v10-010438-0d4e6798` | v10 | 3.878.000–3.895.500 | el segmento **1058** (3.894.997–3.896.537), que solapa el tramo de cuarentena mecánica de v10 **1:04:56–1:05:29** (3.896.000–3.929.000) | **503** (ventana–segmento); el segmento solapa el tramo 537 ms; la ventana no toca el tramo |

**Lo que dicen los milisegundos, sin texto, para el consultor:**
- **Las palabras citadas** de ese ítem caen en los segmentos 1053 a 1058 (`verificar_citas`: 0
  problemas, 1 aparición, palabras de 3.878.937 a 3.896.537). Lo cita entero, y su final, 537 ms,
  cae dentro del tramo.
- **El segmento 1058 no está en el bloque en cuarentena.** El tramo nace del bloque
  `[CUARENTENA 64:56–65:28]` (su motivo), y la marca de inicio de un bloque es el `t0` de su primer
  segmento, truncado. El 1058 empieza en 64:54,997, así que su marca sería 64:54, y no hay ningún
  tramo de v10 que empiece en 1:04:54. El primer segmento del bloque es el 1059 (3.896.537 = 64:56).
- **Es el efecto del inicio al segundo**, el mismo que el §5.2 de `FILTRADAS-ESCENARIO-B.md` vio en
  v9 1:07:45 y v10 0:00:58.
  - El tramo empieza en 3.896.000, el segundo truncado del 1059, y no en 3.896.537.
  - Así pisa la cola de un segmento visible, que la filtrada enseña y del que salió la cita.
  - Con la condición aprobada, ese segmento cuenta como «segmento que solapa un tramo», y el ítem
    falla.
- **Además, el ítem es de A-42:** es la cita de S-7, «…de 10 a 2… y el cierre también sería 10»,
  cuyo final la cuarentena corta. Es una de las dos citas que sostienen la activación de A-42
  (Next Action E).

**Su arreglo no entra en esta rama** (decisión 5). Queda para el consultor. Las opciones que veo:
- (i) un ítem nuevo con la ventana y la cita recortadas antes del 1058;
- (ii) acotar la condición a los segmentos que el filtro tapa, y no a todo segmento que toque un
  tramo;
- (iii) otra.

**Lo que esta parada deja sin hacer:**
- la condición no está activada en `knowledge validate`, `evidence new` ni `evidence propose --check`;
- faltan sus tests, el anexo del control de la fase 5 (los activos) y la regla del caso sin cruda.

Lo medido para el caso sin cruda: `verificar_citas` no da error. Da un AVISO agregado por
transcripción, «N citas sobre tr-… no verificables aqui (cruda ausente en data/)»
(`evidence/modelo.py:398-399`). La condición haría lo mismo, con su propio aviso.

**Lo aprobado que sí se aplicó:** `tests/unit/test_tramos_de_sesion.py::test_ningun_item_de_las_sesiones_solapa_un_tramo`
cuenta ya solo los ítems activos (decisión 4). Comprueba, como negativo, que el superseded sí pisa
el tramo de margen.

## 3. Hallazgo para ERRORES-RECURRENTES (decisión 7)

`FILTRADAS-ESCENARIO-B.md` §4.3 afirmó que `tramo_no_citable` «hace que `knowledge validate` y
`evidence new` rechacen» un ítem que pisa un tramo. **No se midió.** `knowledge validate` no lo llama
(§0.e). Lección: lo que hace una comprobación se mide antes de escribirlo, buscando sus llamadores.

## Estado

**PARADA en el punto 5 de las decisiones del consultor (§2).** Un ítem activo,
`ev-v10-010438-0d4e6798`, incumple la condición aprobada. No se ha activado y su arreglo no entra en
esta rama: decide el consultor.

**Hecho:**
- el tramo de margen (§1.1);
- el ítem nuevo `ev-v9-003457-3e28e325`, que supersede al viejo, por la vía autorizada, con su
  primera pasada rechazada por la guardia (§1.2);
- A-46 y los tres recuadros (§1.3);
- la línea de deuda;
- la función `ventana_no_citable`, sin llamar todavía;
- el test de tramos contando solo los activos.

**`uv run botsito knowledge validate`:** exit 0, sin ERROR. Hay que hacerlo después de la
corrección del §1.2: con el id del candidato en la salida de la primera pasada daba un ERROR.

**Exposición en HOLDOUT-EXPOSICIONES.md: ninguna.** No se leyó ningún texto de v9 ni de v10: solo
milisegundos e índices de segmento, por la vía autorizada. El ítem nuevo copia campos del viejo sin
que la sesión los lea.

**CI de Linux:** no hace falta. No se tocan hooks, rutas ni nada que dependa de la plataforma.

**`PROJECT_STATE.md`:** 24.014 bytes, por debajo del tope de 25.000.

Rama NO cerrada.
