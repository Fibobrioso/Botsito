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

## Estado

**Fase 0 hecha. Espera el visto bueno del consultor** a:
- la vía del punto a (el anexo con `escribir_item` y quién figura en `revisado_por`);
- A-46: sustituir o añadir;
- contar solo los ítems activos en los controles del punto c;
- la condición y el sitio del punto e.

No se ha tocado `knowledge/`, `src/` ni ningún informe cerrado. Rama NO cerrada.
