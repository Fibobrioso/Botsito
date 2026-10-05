# La ventana declarada de ev-v9-003456-9ef48fb5

Rama `trabajo/ventana-ev-v9-003456`, abierta el 2026-10-05 desde `main` en `fffaa03` (commit de
estado; tag `stable/F36y-filtradas-con-tramos` en `06adac1`). Encargo:
`docs/encargos/trabajo-ventana-ev-v9-003456.md`. Es el punto R de la Next Action.

**Las líneas de código que cita este informe son las de `main` en `fffaa03`**, salvo que diga otra
cosa. En la rama, `cli.py` crece unas líneas y se desplazan (revisor, A1).

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

## Decisión del consultor sobre ev-v10-010438-0d4e6798 (2026-10-05)

Copiada tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Decisión sobre ev-v10-010438-0d4e6798 (2026-10-05, consultor). Cópiala al encargo y al informe. CAMBIA lo que dije en la decisión 5 («su arreglo no entra en esta rama»): entra aquí, porque sin él la comprobación no se activa y el procedimiento es el mismo que el de v9.
>
> 1. Opción (i): un ítem nuevo que supersede a ev-v10-010438-0d4e6798, con la cita y la ventana recortadas antes del segmento 1058.
>    Porqué no (ii): que el filtro tape todo segmento que toque un tramo más de 0 ms es el criterio de Q, y falla cerrado a propósito. Acotar la condición solo para que este ítem pase es aflojar una guardia por un caso.
>    Porqué no se pierde nada que haga falta: el trozo que sale («…y el cierre también sería 10») es justo lo que se le ha preguntado al trader por escrito antes de activar A-42 (punto E). Su respuesta lo sustituye.
>
> 2. Cómo, con el mismo anexo sustituir_item.py o uno hermano:
>    - La cita nueva es la vieja sin la parte que cae en el segmento 1058. El anexo la construye por programa con los límites de los segmentos (vía autorizada) y verificar_citas. No imprimas el texto: solo el id nuevo, el número de segmentos que cubre la cita (se espera 1053–1057) y el resultado de las comprobaciones.
>    - Ventana nueva: mismo inicio (3.878.000) y fin en el último segundo entero que no solape el segmento 1058 (se espera 3.894.000; mídelo).
>    - Dos pasadas, como en v9:
>      · con la cita y la ventana viejas, la comprobación nueva (ventana_no_citable) TIENE que rechazarlo;
>      · con las nuevas, verificar_citas da 0 problemas y 1 aparición, ventana_no_citable pasa y escribe el ítem.
>    - revisado_por igual que el viejo. notas: «cita recortada antes del segmento 1058, que el filtro tapa por el tramo 1:04:56–1:05:29; orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó».
>    - Lista en el informe los campos que difieren del viejo.
>
> 3. Referencias, cada una por su régimen:
>    - A-42 en ambiguedades.yaml pasa a citar el ítem nuevo, con Fuente:, y se regenera con uv run botsito spec docs --escribir;
>    - recuadro con fecha en SESION-04-EXTRACCION.md §3.1, que diga que la cita de 64:38–64:54 ya no incluye «…y el cierre también sería 10» y por qué, y que esa parte la cubre la pregunta del punto E;
>    - mide si algo más cita el id viejo y dímelo.
>
> 4. Medida, solo para el informe (no se arregla aquí): cuántos segmentos VISIBLES (no en cuarentena) tapa hoy el filtro solo porque un tramo, registrado con el inicio o el fin redondeado al segundo, les pisa un trozo. Por vídeo, con ids de segmento y ms, sin texto. Ya conocemos v9 1:07:45, v10 0:00:58 y este. Sirve para la fase 0 de la activación de E.
>
> 5. Después, lo que quedaba:
>    - activa ventana_no_citable en knowledge validate, evidence new y evidence propose --check, con los cinco tests de rotura más uno con este caso (una ventana que no toca el tramo, pero cuya cita cae en un segmento que sí lo toca → falla);
>    - vuelve a medir en todos los vídeos: 0 ítems activos;
>    - anexo del control de la fase 5 (21 de 21 bloques y 0 ítems activos, más cuántos supersedidos deja fuera: se esperan 2);
>    - uv run botsito knowledge validate, uv run python scripts/ficheros_con_ocultos.py y make check sellado;
>    - revisor, con su informe al final de VENTANA-EV-V9.md.
>
> 6. PROJECT_STATE va en 24.014 bytes, cerca del tope de 25.000. En esta rama no crece más. Si la línea de deuda de los supersedidos lo empuja, condénsala a una línea que apunte al informe.
>
> Rama lista para revisión, NO cerrada.

## 4. ev-v10-010438-0d4e6798, por la decisión del consultor

### 4.1 El ítem nuevo, con la cita y la ventana recortadas, en dos pasadas

Anexo: `docs/validation/anexos/VENTANA-EV-V9/recortar_item_v10.py`, hermano de `sustituir_item.py`.
Usa la misma vía y la misma comprobación de `evidence new` (`cli.py:988-1040`; desde esta rama,
`_EntornoEvidencia.comprobar` llama a `ventana_no_citable`, §6).
- **La cita nueva** es el prefijo más largo de la vieja, cortado por palabras y sin el separador
  final, cuya localización (`localizar_cita`, la de `verificar_citas`) cae entera antes del segmento
  1058 y aparece una sola vez. La sesión no la ha leído.
- **La ventana nueva** tiene el mismo inicio y el fin en el último segundo entero que no solapa el
  1058. **Medido: 3.894.000**, porque el 1058 empieza en 3.894.997.

**Pasada 1, con la cita y la ventana viejas** (`recortar_item_v10-PASADA1.txt`):

```
item viejo: ev-v10-010438-0d4e6798 (3878000-3895500 ms)
segmento 1058: 3894997-3896537 ms; fin de la ventana nueva: 3894000
verificar_citas: 0 problemas; apariciones 1; segmentos de la cita [1053, 1054, 1055, 1056, 1057, 1058]
ventana_no_citable (3878000-3895500 ms): la ventana pisa 503 ms del segmento 1058 (1:04:54.997-1:04:56.537), que solapa un tramo no citable
RECHAZADO por la comprobacion de evidence new: <candidato sin escribir>: la ventana pisa 503 ms del segmento 1058 (1:04:54.997-1:04:56.537), que solapa un tramo no citable
```

**Pasada 2, con la cita y la ventana nuevas** (`recortar_item_v10-PASADA2.txt`):

```
verificar_citas: 0 problemas; apariciones 1; segmentos de la cita [1053, 1054, 1055, 1056, 1057]
ventana_no_citable (3878000-3894000 ms): pasa
ESCRITO: ev-v10-010438-024f76b8 (3878000-3894000 ms), knowledge/evidence/v10/ev-v10-010438-024f76b8.yaml
campos distintos del viejo: ['cita_literal', 'id', 'notas', 'supersede', 't1']
igual campo a campo salvo ['cita_literal', 'id', 'notas', 'supersede', 't1']: True
```

**Los campos que difieren del viejo:**

| Campo | Viejo | Nuevo |
|---|---|---|
| `id` | `ev-v10-010438-0d4e6798` | **`ev-v10-010438-024f76b8`** |
| `t1` | 1:04:55.5 (3.895.500) | **1:04:54** (3.894.000) |
| `cita_literal` | segmentos 1053–1058 | la misma sin la parte del 1058: segmentos **1053–1057** (no impresa) |
| `supersede` | — | `ev-v10-010438-0d4e6798` |
| `notas` | la del viejo | «cita recortada antes del segmento 1058, que el filtro tapa por el tramo 1:04:56–1:05:29; orden del consultor, 2026-10-05, VENTANA-EV-V9.md; la cita no se releyó» |

**Iguales:** `t0`, `afirmacion`, `tema`, `tipo`, `modalidad`, `confianza`, `extractor`,
`revisado_por` (el del viejo), `provenance`, `fotogramas`, `valor` y `transcripcion`.

### 4.2 Las referencias

- **A-42 no citaba el ítem viejo. Desviación, para el consultor.**
  - Su `evidencia` en `ambiguedades.yaml` es `ev-v3-000136-6160fcea`, `ev-v4-011425-ae028b78`,
    `ev-v9-010753-063c8cb7` y `ev-v9-010809-68e4ea44`, sin ningún ítem de v10. No hay referencia
    que mover.
  - Que A-42 cite el ítem nuevo sería **añadirle** evidencia, y eso es parte de su activación
    (punto E). No se ha hecho, y `ambiguedades.yaml` no cambia por v10.
- **`SESION-04-EXTRACCION.md` §3.1:** recuadro con fecha.
  - La cita de 64:38–64:54 ya no incluye «…y el cierre también sería 10», porque esa parte cae en
    el segmento 1058, que el filtro tapa por el tramo 1:04:56–1:05:29.
  - Esa parte la cubre la pregunta escrita al trader del punto E.
- **¿Qué más cita el id viejo?** Búsqueda en todo el repo: además del propio ítem y del nuevo (su
  `supersede`), solo `SESION-04-EXTRACCION.md` (el §3.1, ya con recuadro) y los ficheros de esta
  rama: encargo, informe, anexos y la línea de `PROJECT_STATE.md`. **Nada en la spec, las
  ambigüedades ni el feedback.**

## 5. La medida de los segmentos visibles que el filtro tapa por un tramo redondeado (punto 4)

Anexo: `medir_recortados.py`, con la salida en `medir_recortados-SALIDA.txt`. Solo da ids de segmento
y milisegundos, para la fase 0 de la activación de E. No se arregla aquí.

**a) Segmentos que solapan un tramo pero no caben en la unión de los tramos de su vídeo** (asoman por
un borde; el filtro de Q los taparía por ese trozo):

| Vídeo | Cuántos | Segmentos (solape en ms) |
|---|---|---|
| v6 | 2 | 471 (3), 581 (717): el tramo manual 0:41:00–0:50:11 |
| v7 | 1 | 127 (630) |
| v9 | 7 | 403 (10), 437 (680), 1074 (94), 1081 (4); en tramos de precaución, 567 (130), 1178 (1.923) y 1662 (2.696) |
| v10 | 22 | 25 (860), 650 (50), 1036 (607), 1040 (53), **1058 (537)**, 1358 (672), 1362 (908), 1363 (372), 1367 (588), 1686 (182), 1702 (212), 1708 (188), 1891 (122), 1897 (8 y 932), 1901 (888); en tramos de precaución y sin audio, 664 (270), 705 (270), 1379 (312), 1383 (10.868), 1398 (469), 1724 (28) |
| **Total** | **32 filas, 31 segmentos** | el 1897 asoma por los dos lados de dos tramos seguidos |

**Lo que el consultor preguntó** (tramos redondeados al segundo, es decir, de cuarentena mecánica):
**21 filas** (v7: 1, v9: 4, v10: 16). Las otras **11** son de tramos manuales, de precaución o sin
audio (v6: 2, v9: 3, v10: 6), cuyos bordes no salen de un redondeo de la filtrada (revisor, A3).

- **Los que asoman por el inicio** de un tramo de cuarentena mecánica son visibles seguros: el tramo
  empieza en el segundo truncado de su primer segmento oculto.
- **Por el fin**, también, cuando el tramo lleva el segundo de margen.
- **En los de precaución**, el solape puede pasar de un segundo: esos tramos no salen de un bloque y
  sus bordes se pusieron a mano.

**b) Segmentos visibles que caben enteros dentro de un tramo de cuarentena mecánica**, en su segundo
redondeado:
- **v9, seguros** (los motivos dan qué segmentos ocultó el filtro):
  - **1087** (4.065.344–4.065.824), en 1:07:45–1:07:51: el caso ya conocido de v9 1:07:45;
  - **1191** (4.435.383–4.435.963), en 1:13:55–1:14:04.
- **v10, posibles** (sus motivos no dan el rango; distinguirlos de un oculto exige la filtrada):
  - **12** (58.180–58.540), en 0:00:58–0:01:13: el caso ya conocido de v10 0:00:58;
  - **1703**, **1707** y **1709**, en los tramos de 1:55:58 y 1:56:04.

Lo que pide la fase 0 de E es medirlo sobre las filtradas rehechas, que es donde se sabe qué tapó el
filtro.

## 6. La condición, activada, y los controles

**Dónde la llaman ahora** (decisión 5):
- **`knowledge validate`**, con `ventanas_no_citables(items, contexto)` en
  `src/botsito/validation/knowledge.py`, llamada justo después de `verificar_citas`, sobre **todos
  los ítems activos de todos los vídeos**.
- **`evidence new`**, en `_EntornoEvidencia.comprobar`, `cli.py`, en lugar de `tramo_no_citable`.
- **`evidence propose --check`**, en `evidence/propuestas.py`, también en lugar de
  `tramo_no_citable`. Un ítem de pantalla no cita la transcripción: para él solo cuenta el tramo.

**Sin la cruda**, la función hace lo mismo que `verificar_citas`, que no da error: da un AVISO
agregado por transcripción (`evidence/modelo.py:398-399`).
- Aquí, «N ventanas sobre tr-… no comprobadas contra sus segmentos (cruda ausente en data/); contra
  los tramos, sí».
- No pasa en silencio, y el tramo se comprueba igual.
- Un vídeo sin tramos no tiene nada que comprobar: ni problema ni aviso.

**Tests:** `tests/unit/test_ventana_no_citable.py`, 8 funciones, todo sintético salvo el último:

| Test | Qué rompe a propósito |
|---|---|
| `test_la_ventana_vieja_falla` | la ventana vieja de v9 pisa el tramo de margen → falla |
| `test_pisar_solo_la_cola_de_un_segmento_que_solapa_un_tramo_falla` | la ventana pisa la cola de un segmento que solapa un tramo, sin tocar el tramo → falla (y sin la cruda no se vería) |
| `test_la_ventana_que_toca_el_tramo_a_0_ms_pasa` | toca el tramo a 0 ms → pasa; 1 ms dentro → falla |
| `test_un_item_supersedido_que_pisa_un_tramo_no_cuenta` | el supersedido no cuenta; sin el que lo supersede, sí |
| `test_la_ventana_nueva_pasa` | v9 con los milisegundos medidos: la nueva pasa y la vieja no |
| `test_el_caso_de_v10_…` | el caso de este ítem: la ventana no toca el tramo, pero pisa 503 ms del segmento que lo toca → falla; la recortada pasa |
| `test_sin_la_cruda_no_pasa_en_silencio` | sin la cruda: AVISO, no silencio; el tramo se ve igual |
| `test_la_llaman_validate_evidence_new_y_propose` | el cableado: los tres caminos la llaman |

**Controles:**
- **La condición en todos los vídeos, otra vez** (`medir_condicion-SALIDA2.txt`): 503 ítems, 490
  activos; **0 activos la incumplen**. La primera medida, la de la parada, sigue en
  `medir_condicion-SALIDA.txt`.
- **El control de la fase 5** (`control_activos.py`, con su salida): **21 de 21** bloques de B de v9
  y v10 caben enteros en un tramo.
  - Los bloques salen de la salida ya commiteada de `FILTRADAS-ESCENARIO-B/tramos_registrados`, así
    que no se abre ninguna filtrada.
  - **0 ítems activos** de v7–v10 solapan un tramo más de 0 ms.
  - **Supersedidos que se dejan fuera: 2**, `ev-v9-003456-9ef48fb5` y `ev-v10-010438-0d4e6798`.
- **`uv run botsito knowledge validate`:** exit 0, sin ERROR, con la condición activa. Con la cruda
  presente no sale ningún aviso suyo.
- **`uv run python scripts/ficheros_con_ocultos.py`:** «OK: .claude/hooks/ficheros_con_ocultos.txt
  coincide».

## 7. Lo que se hizo con los hallazgos del revisor

Resultado: 0 bloquea y 0 importa; 4 menores en el eje (a) y 1 en el (b). Los 24 requisitos del
encargo, hechos.

| # | Gravedad | Qué se hizo |
|---|---|---|
| A1 | menor | **Arreglado.** Las líneas de `cli.py` que citan el informe y los anexos son las de `main` en `fffaa03`, y en la rama se desplazan. El informe lo dice en su cabecera; los dos anexos citan ahora las mismas líneas (621-662) y dicen que son de `main`; el recuadro del §4.3 de FILTRADAS dice «en `main`». |
| A2 | menor | **Arreglado.** El recuadro del §4.3 de `FILTRADAS-ESCENARIO-B.md` pasa a ir detrás de la lista de los 6 tests, que es donde no corta la lectura. Lo añadió esta rama: el cuerpo del informe cerrado sigue intacto, y frente a `main` el fichero solo gana líneas (+20/−0). |
| A3 | menor | **Arreglado.** El §5 distingue ya 32 filas de 31 segmentos (el 1897 sale dos veces). Separa también las **21** filas de cuarentena mecánica, las que preguntó el consultor, de las 11 de tramos manuales, de precaución o sin audio. |
| A4 | menor | **Arreglado.** El Estado da el tamaño frente a la cifra del consultor (24.014, no crece) y frente a `main` (23.567, +410). |
| B1 | menor | **Arreglado en el código.** `evidence new` decidía si mirar los segmentos con `item.transcripcion`; validate, con `cita_de_audio` y transcripción; propose, con la modalidad. Ahora `evidence new` usa el mismo criterio que validate (`cita_de_audio and transcripcion`), que equivale al de propose. Los 8 tests siguen pasando. Sin la cruda, `evidence new` sigue dando un ERROR, por la comprobación de transcripción que ya existía: es más estricto que el AVISO de validate, y es lo que hacía antes. |

**Para el consultor, del revisor:** confirmar la desviación de A-42 (§4.2). A-42 no citaba el ítem
viejo de v10, así que no se le ha añadido el nuevo.

## Orden de cierre del consultor (2026-10-05)

Copiada tal cual:

> Modelo: el que tengas · Esfuerzo: medio
>
> Orden de cierre de trabajo/ventana-ev-v9-003456 (consultor, 2026-10-05). Revisada: lista para cerrar.
>
> 1. Desviación de A-42: ACEPTADA. A-42 nunca citó ev-v10-010438-0d4e6798 (su evidencia es de v3, v4 y v9). Añadirle el ítem nuevo ev-v10-010438-024f76b8 toca al activarla en el punto E, no aquí. El error de la orden fue del consultor.
>
> 2. Tag: stable/F36z-ventana-no-citable. Antes de crearlo, comprueba en HISTORIA que la última letra cerrada es la y y que stable/F36z-* no existe ni en local ni en origin. Si la z ya está usada, para y dímelo.
>
> 3. Hallazgos del consultor para la fila de ERRORES-RECURRENTES, cada uno con su lección:
>    a) IMPORTA · El consultor escribió en una orden que A-42 citaba el ítem de v10 sin leer ambiguedades.yaml. Claude Code lo midió y no lo aplicó. Lección (consultor): una referencia del repo se lee antes de ordenarla. Si no se puede leer, se escribe «verifica que…».
>    b) IMPORTA · Los tramos no citables se registran con el inicio o el fin redondeados al segundo. Desde Q, el filtro tapa entero todo segmento que tocan, así que 21 segmentos visibles quedan tapados (1 en v7, 4 en v9 y 16 en v10), y una cita activa (v10) caía en uno de ellos. Nadie lo vio hasta que existió ventana_no_citable. Lección (revisor): cuando una rama cambia qué tapa un filtro, se mide qué ítems activos citan lo que pasa a quedar tapado.
>    c) MENOR · FILTRADAS-ESCENARIO-B §4.3 afirmó sin medirlo que knowledge validate rechazaba esos ítems. Lección (revisor): lo que un informe dice que hace una comprobación se comprueba ejecutándola, no leyendo el informe.
>
> 4. En HISTORIA (registro del cierre, en la rama): R pasa a «Next Action HECHA · R» con su texto literal.
>
> 5. Commit de estado en main. Solo reemplaza las cuatro cabeceras y quita R del Next Action. Al punto E añade al final esta frase:
>    «La fase 0 de la activación parte de la medida de VENTANA-EV-V9.md (21 segmentos visibles tapados por tramos redondeados) y añade a la evidencia de A-42 el ítem ev-v10-010438-024f76b8.»
>    No toques Completed Features ni el Change Log. PROJECT_STATE tiene que seguir por debajo de 25.000 bytes.
>
> 6. Lo de siempre: push atómico de main y el tag, la CI de main en verde antes de borrar la rama, y luego borrar la rama local (no hay fix/ remota).
>
> 7. Informe final con:
>    - sha de main;
>    - el tag y a qué commit apunta;
>    - el run de la CI de main, con tests pasados y saltados;
>    - las ramas que quedan;
>    - el tamaño de PROJECT_STATE.

## Estado

**Lista para revisión, NO cerrada.** El revisor, al final, y lo hecho con sus hallazgos en el §7.

**Encargo frente a lo hecho:**

| Pedido | Hecho |
|---|---|
| Fase 0 | §0 |
| Fase 2: tramo de margen | §1.1 (+7/−0) |
| Fase 1: ítem nuevo de v9, dos pasadas | §1.2: `ev-v9-003457-3e28e325` |
| Fase 3: referencias de v9 | §1.3: A-46 y tres recuadros; la línea de deuda |
| Decisión sobre v10 | §4: `ev-v10-010438-024f76b8`, dos pasadas, el recuadro de SESION-04 |
| Medida de los segmentos visibles recortados | §5: 32 que asoman por un borde; 2 seguros y 4 posibles dentro |
| Fase 4: la condición, activada, con sus tests | §2 y §6: 8 tests |
| Fase 5: controles | §6: 0 activos; 21 de 21; 2 supersedidos fuera; validate y ficheros_con_ocultos en verde |

**Desviaciones declaradas:**
- **A-42 no citaba el ítem viejo de v10**, así que no se le ha añadido el nuevo (§4.2). Citarlo es
  parte de su activación.
- **La primera pasada de v9:** la primera ejecución imprimía el id del candidato no escrito, y
  `knowledge validate` daba ERROR. El anexo lo sustituye ahora, y la pasada se repitió con la misma
  salida (§1.2).
- **La decisión 5** decía que el arreglo del ítem de v10 no entraba aquí. Lo cambió la decisión del
  consultor sobre ese ítem.

**Exposición en HOLDOUT-EXPOSICIONES.md: ninguna.**
- No se leyó ningún texto de v9 ni de v10: solo índices de segmento y milisegundos, por la vía
  autorizada.
- Las citas nuevas se construyeron por programa y no se imprimieron.
- No se abrió ninguna filtrada: los bloques de B salen de una salida ya commiteada.

**CI de Linux: no hace falta.** No se tocan hooks, rutas ni nada que dependa de la plataforma; el
código nuevo es Python puro sobre milisegundos.

**`PROJECT_STATE.md`:** 23.977 bytes.
- Frente a la cifra que dio el consultor (24.014, la de la mitad de la rama), no crece.
- Frente a `main` (23.567), sube 410 bytes: la apertura de la rama y la línea de deuda.
- Sigue por debajo del tope de 25.000 (revisor, A4).

Rama NO cerrada.

## Informe del revisor

Subagente `revisor` (`.claude/agents/revisor.md`), lanzado con el informe terminado sobre `41be086`.
Pegado tal cual; lo que se hizo con cada hallazgo está en el §7.

> ## Informe del revisor · trabajo/ventana-ev-v9-003456 · 2026-10-05
>
> Rama en `41be086` (3 commits sobre `fffaa03`); `git status` limpio; `make-check.log`: `SELLO: make check en verde sobre el arbol ef3624e3f50367e3073923c643604f075d96a7be` = `git rev-parse HEAD^{tree}`, `2027 passed`, `exit=0`, `PICO DE MEMORIA: 288 MiB`. Regla de lectura respetada: no leí ninguna `cita_literal` ni `afirmacion` de `ev-v9-*`/`ev-v10-*`, ninguna cruda ni filtrada; solo programas que imprimen nombres de campo, booleanos, ids y ms.
>
> ### Eje (a) · Reglas de la casa
>
> Resumen: 0 bloquea, 0 importa, 4 menor.
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | A1 | menor | Las referencias de línea a `cli.py` en el informe (§0.a, §1.2) y en los anexos (`sustituir_item.py`, `recortar_item_v10.py`) son las de `main` (`evidence_new` 988-1040, `escribir_item` 1034, `comprobar` 621-662); en la rama `comprobar` crece 7 líneas y quedan desplazadas. Lo mismo en el recuadro de FILTRADAS §4.3 (`cli.py:628`, `propuestas.py:404`). La decisión 1 pedía citar la línea que se replica: conviene decir «en main». | `grep -n "def evidence_new\|escribir_item(" src/botsito/cli.py` → 995 / 1041 (en main 988 / 1034). `recortar_item_v10.py:5` ya dice «621-670», `sustituir_item.py:7` dice «621-662»: inconsistentes entre sí. |
> | A2 | menor | En FILTRADAS-ESCENARIO-B.md §4.3 el recuadro de corrección quedó insertado entre «con 6 funciones:» y su lista de viñetas, que sigue debajo; el cuerpo está intacto, pero la lectura se parte. | `git diff main -- docs/validation/FILTRADAS-ESCENARIO-B.md`: el recuadro entra justo tras la línea «…con 6 funciones:» y antes de «- **Sintéticos contra `tramo_no_citable`:**». |
> | A3 | menor | La medida de §5 (punto 4 del consultor) da «Total 32» con dos imprecisiones: (i) cuenta el segmento 1897 dos veces (inicio y fin): 31 segmentos, 32 filas; (ii) mezcla 21 filas de «cuarentena mecánica» (v7 1, v9 4, v10 16) —las que el consultor preguntó (tramo «redondeado al segundo»)— con 11 de tramos manuales, de precaución o sin audio (v6 2, v9 3, v10 6). El informe sí distingue las clases en prosa, pero el total de cabecera no responde a la pregunta tal cual. | `medir_recortados-SALIDA.txt` (reproducida: idéntica salvo CRLF); filas con clase «cuarentena mecanica» = 21; resto = 11. |
> | A4 | menor | «PROJECT_STATE: 23.977 bytes. No crece: era de 24.014 y bajó.» Respecto de `main` (23.567 bytes) sí crece 410 bytes; 24.014 era el estado intermedio de la propia rama. Por debajo del tope de 25.000 y no rompe la decisión 6, pero la frase puede inducir a error. | `git show fffaa03:PROJECT_STATE.md \| wc -c` = 23567; `3667838` = 23771; `809117b` = 24014; `41be086` = 23977. |
>
> Comprobado sin hallazgos: contrato (`contrato_rama.py`: 33 ficheros dentro, 4 comprobaciones; nada en `rutas_protegidas`); comprobaciones del contrato (`medir_ventana.py` idéntica; `knowledge validate` exit 0, 0 `ERROR`, sin AVISO propio de la condición con la cruda presente; `ficheros_con_ocultos.py` OK; sello = `HEAD^{tree}`); trailers `Fuente:` (solo `809117b` toca `knowledge/spec/`, con `Fuente: ev-v9-003457-3e28e325`, que existe; ningún commit toca `knowledge/cases/`); holdout y material (nada en `knowledge/cases/holdout/`; «Exposición: ninguna» justificada; los anexos no usan `.texto`, `cita_literal` ni `afirmacion` salvo para copiarlas, y sus salidas solo traen ids y ms; el único texto impreso es el `motivo` de un tramo, plantilla y no material; el recuadro de SESION-04 repite «…y el cierre también sería 10», que ya estaba en `main` en ese documento y en la decisión del consultor); regímenes (solo dos `A` en evidencia; tramos +7/−0; HISTORIA solo añade el Archivo 16; nada en feedback, ADR, `libros.yaml` ni ERRORES-RECURRENTES); ambigüedades (A-46 +1/−1, `spec docs` coincide, no se abre ni cierra nada); informes cerrados (FILTRADAS §4.1 y §4.3, SESION-03 y SESION-04 §3.1: solo líneas añadidas, en `>`, con fecha y rama; `CUARENTENA-POR-DEFECTO.md`, `anexos/FILTRADAS-ESCENARIO-B/` y encargos anteriores sin diff); sin sitio nuevo con `cita` en la spec; `test_no_business_literals` dentro de `make check`; el informe existe y acaba en su estado; tres citas del informe contra su fuente (`modelo.py:429-435`, `modelo.py:398-399`, `git grep -n tramo_no_citable main -- src`) ✓.
>
> ### Eje (b) · Encargo
>
> Resumen: 0 bloquea, 0 importa, 1 menor. Requisitos: 24 hechos, 0 parciales, 0 no hechos (1 «hecho de otra forma», bien declarado).
>
> | # | Requisito | Estado | Evidencia |
> |---|---|---|---|
> | 1 | Rama desde `main` en `fffaa03` con `abrir-rama`: encargo, contrato, Archivo 16 en HISTORIA | Hecho | merge-base `fffaa03`; encargo; `contrato.yaml`; `+# Archivo 16` |
> | 2 | Corregir la ventana de `ev-v9-003456-9ef48fb5` por supersede, no por edición | Hecho | `ev-v9-003457-3e28e325`: `t0: 0:34:57`, `supersede: ev-v9-003456-9ef48fb5`; el viejo sin cambios |
> | 3 | No cambia motor, spec de reglas, texto de la cita, otros ítems ni líneas escritas de tramos | Hecho | sin diff en `src/botsito/engine/`, `strategy_spec.yaml`, `parametros.yaml`; tramos +7/−0; campos distintos `['id','notas','supersede','t0']` |
> | 4 | Material: solo `n`, `t0_ms`, `t1_ms`; sin texto ni longitudes; sin filtradas | Hecho | anexos y salidas revisados; que no se abrió ninguna filtrada no se puede probar desde el diff (lo declara el informe) |
> | 5 | Fase 0 (a)-(e) entregada antes de escribir | Hecho | §0.a-§0.e; las afirmaciones comprobadas son ciertas |
> | 6 | (b): 612/613, condiciones, inicio al segundo más temprano; fin 2.100.000 si cumple | Hecho | `medir_ventana.py` reproducido |
> | 7 | (c): tramo de margen solo añadiendo; 0 ms con la ventana nueva | Hecho | +7/−0 (2.084.000–2.097.000); la ventana nueva empieza en 2.097.000 |
> | 8 | (d): quién cita el id y por qué régimen | Hecho | §0.d; Grep: spec solo A-46; nada en feedback |
> | 9 | (e): ¿falla algo hoy? condición y sitio | Hecho | §0.e; la corrección sobre `knowledge validate` es cierta |
> | 10 | Fase 1 con `Fuente:` y referencia a FILTRADAS §4.1 | Hecho | `809117b` |
> | 11 | D1: vía autorizada con sus condiciones | Hecho | `sustituir_item.py`; `revisado_por` igual (`True`); `notas` == la del consultor (`True`) |
> | 12 | D2: tramo primero; dos pasadas; la de 2.096.000 rechazada por `tramo_no_citable` | Hecho | PASADA1 reejecutada: rechazada, exit 1, sin escribir; PASADA2 escribe `ev-v9-003457-3e28e325`. El orden solo lo cuenta el informe |
> | 13 | D3: A-46 sustituye el id, con `Fuente:` y `spec docs --escribir` | Hecho | +1/−1; `spec docs` coincide |
> | 14 | D3: ¿avisa algo de ítems supersedidos citados?; si no, línea de deuda | Hecho | ninguna mención de «supersed» en `spec/` ni `validation/`; línea en Technical Debt |
> | 15 | D4: control sobre ítems ACTIVOS; supersedidos fuera declarados | Hecho | `control_activos.py` reproducido: 0 activos; 2 supersedidos |
> | 16 | D5: función junto a `tramo_no_citable`, solo ms, la llaman validate, new y propose | Hecho | `ventana_no_citable`; `_validar` vía `ventanas_no_citables`; `_EntornoEvidencia.comprobar`; `propuestas.comprobar` |
> | 17 | D5: medir antes de activar; 0 o PARADA | Hecho | `medir_condicion-SALIDA.txt` (1 → parada); `SALIDA2` reproducida: 0 |
> | 18 | D5: sin transcripción, como `verificar_citas`, nunca en silencio | Hecho | simulado sin `data/`: 0 problemas, 4 AVISO agregados por transcripción |
> | 19 | Tests de rotura (cinco + v10) | Hecho | 8 funciones; 14 passed con `test_tramos_de_sesion` |
> | 20 | D6: recuadros; lo que no se toca, intacto | Hecho | ver respuesta 5 |
> | 21 | D7: hallazgo para ERRORES-RECURRENTES en el informe | Hecho | §3 |
> | 22 | v10-1/2: ítem nuevo, cita y ventana recortadas, dos pasadas, campos listados | Hecho | `ev-v10-010438-024f76b8`: distintos `['cita_literal','id','notas','supersede','t1']`; `t1` 3.894.000; segmentos 1053–1057, 0 problemas, 1 aparición; `vieja` reejecutada: rechazada por `ventana_no_citable` (503 ms del 1058), exit 1 |
> | 23 | v10-3: A-42 pasa a citar el nuevo; recuadro SESION-04 §3.1; qué más cita el id viejo | **Hecho de otra forma, declarado** | A-42 no citaba el viejo; recuadro hecho; «qué más cita» medido |
> | 24 | v10-4/5/6: medida de recortados; activar; controles; make check; PS sin crecer | Hecho | §5 (ver A3); PS 23.977 < 24.014 y < 25.000; `state check` OK (1309 = 1301 + 8) |
>
> | # | Gravedad | Hallazgo | Evidencia |
> |---|---|---|---|
> | B1 | menor | Las tres vías que llaman a la condición no pasan los segmentos con el mismo criterio: `evidence new` mira `item.transcripcion` (`cli.py:~629`), `knowledge validate` mira `it.cita_de_audio and it.transcripcion`, `propose` mira `modalidad in ("audio","ambas")`. Hoy no cambia nada (los 156 ítems activos de v6/v7/v9/v10 con tramos son de audio con transcripción, salvo 1 de pantalla sin transcripción en v7), pero es una divergencia latente. Además, sin cruda, `evidence new` da ERROR (por la comprobación de transcripción que ya existía), no el AVISO de validate; el informe solo describe el comportamiento de validate. | `git diff main -- src/botsito/cli.py src/botsito/evidence/propuestas.py src/botsito/validation/knowledge.py`; recuento por (vídeo, modalidad, transcripción) ejecutado. |
>
> Lo que la rama hace sin que el encargo lo pida: nada con evidencia en contra. Lo que el encargo dice que no se toca: sin diff en motor, `parametros.yaml`, `strategy_spec.yaml`, hooks, guardia, skills, `scripts/`, feedback, HISTORIA anterior, encargos ni anexos cerrados.
>
> ### Respuestas 1-10 (resumen)
>
> 1. Ítems nuevos frente a viejos: correcto (v9 difiere en `id`, `notas`, `supersede`, `t0`; v10 en `cita_literal`, `id`, `notas`, `supersede`, `t1`; `revisado_por` igual; `notas` literal; la cita de v10 es prefijo de la vieja; los viejos intactos).
> 2. Tramo de margen: +7/−0, un solo tramo v9 0:34:44–0:34:57, con `motivo` y `acordado`.
> 3. Condición: la aprobada, solo ms, llamada por las tres vías; sin cruda, aviso agregado y nunca en silencio (simulado). Las otras dos vías: B1.
> 4. Tests: 14 passed; cubren los cinco de rotura, el caso v10, sin cruda y el cableado; el cambio de `test_tramos_de_sesion` cuenta solo activos con su negativo.
> 5. Referencias: A-46 cita el nuevo de v9; A-42 no citaba el viejo de v10 (`main` y HEAD), desviación bien declarada que el consultor debe confirmar; recuadros solo con líneas añadidas; lo que no se toca, intacto.
> 6. Medidas reproducidas, idénticas salvo CRLF (`medir_ventana`, `medir_condicion` SALIDA2, `control_activos`, `medir_recortados`); los «seguros» de v9 confirmados con los rangos de los motivos.
> 7. Trailers `Fuente:` correctos.
> 8. `PROJECT_STATE.md`: 23.977 bytes (A4); 1309 funciones; la línea de deuda está.
> 9. `knowledge validate` exit 0 sin ERROR; `ficheros_con_ocultos` OK.
> 10. El hallazgo para ERRORES-RECURRENTES está escrito (§3) y es cierto.
>
> CI de Linux «no hace falta»: comprobado; no se tocan hooks, rutas ni scripts; el único comportamiento que depende del entorno es la ausencia de `data/`, que da avisos sin error.
>
> ### Lo que no pude comprobar
> - Que no se abrió ninguna filtrada ni texto de v9/v10 durante la rama (solo que los anexos no lo imprimen y el diff no lo contiene).
> - El orden real de ejecución de las fases (un commit lo junta todo).
> - La condición con un `data/` realmente ausente (simulada con una ruta inexistente).
> - `make check` (me fié del sello = `HEAD^{tree}` y de `2027 passed`).
> - Que los segmentos «posibles» de v10 sean visibles (exige la filtrada).
> - Que la cita nueva de v10 sea la más larga posible y completa (no la leí; es prefijo y `verificar_citas` da 0 problemas y 1 aparición).
>
> ### Veredicto
>
> Lista para revisión del consultor. Eje (a): sin hallazgos que bloqueen ni importen; 4 menores de redacción y referencias. Eje (b): 24 requisitos hechos; una desviación (A-42 sin referencia que mover) declarada y justificada, que conviene que el consultor confirme; un menor latente (B1). Lo medido es reproducible: 0 activos incumplen, 21 de 21 bloques caben, 2 supersedidos fuera. `make check` sellado sobre el árbol de `HEAD`.
