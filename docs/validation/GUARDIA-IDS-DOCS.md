# La guardia de ids citados en los documentos

Rama `trabajo/guardia-ids-docs`, 2026-09-22. Sin merge, sin tag y sin push. Objetivo: que todo id
citado en `docs/**`, `CLAUDE.md` y `PROJECT_STATE.md` (`ev-*`, `fb-*`, `ADR-NNNN`) exista de verdad.
Hasta hoy nada lo comprobaba: es el patrón 5, lo escrito y lo que existe se separan y nada los
compara. Era la deuda de Next Action 11.

Este informe cita los ids que no existen, porque medirlos es su tema. Van declarados aquí, con la
misma regla que exige a todos:

```ids-inexistentes
ev-v4-003710-f32c06e4 — medido en esta rama como id inexistente; se cita en las tablas de §1 y §3
ev-v4-003710-f610cc8f — medido en esta rama como id inexistente; se cita en las tablas de §1 y §3
ev-v6-001707-9f2b6e31 — medido en esta rama como id inexistente; se cita en las tablas de §1 y §3
ADR-9999 — medido en esta rama como id inexistente; se cita en las tablas de §1 y §3
```

## 1. La medida del paso 0, antes de escribir nada

**Qué es un id:** una sola definición, `comun.ids.FUENTE`, la gramática del trailer `Fuente:`. Se
aplica con `fullmatch` a cada tramo `[A-Za-z0-9-]` del texto; el tramo solo corta el texto, no
decide qué es un id. **Qué ids existen:** el mismo conjunto con el que `knowledge validate` valida
los trailers, que es evidencia, más feedback, más `ids_de_adr`.

**`docs/**`, 131 ficheros de texto:**

| tipo | citas | ids distintos | distintos que no existen |
|---|---|---|---|
| `ev-*` | 234 | 104 | 3 |
| `fb-*` | 124 | 58 | 0 |
| `ADR-NNNN` | 1019 | 41 | 1 |

**Los inexistentes de `docs/**`, 8 citas.** Ninguno es una errata de un id real ni un id
renombrado. Todos son ids que nunca existieron en el repositorio.

| id | fichero:línea | clase |
|---|---|---|
| `ev-v4-003710-f32c06e4` | `AUDITORIA-2026-09-13-ultracode.md:786` | nunca existió: es salida pegada de un `evidence new --supersede` ejecutado en una copia desechable. El id real vecino es el item que esa copia supersedía, y no es una errata de él |
| `ev-v4-003710-f610cc8f` | `AUDITORIA-2026-09-13-ultracode.md:977` | nunca existió: el texto lo llama «un ítem con cita inventada», creado en la copia para reproducir un hallazgo |
| `ADR-9999` | `F09-expert-feedback-model.md:118` | citado a propósito: el ejemplo de ADR inexistente que antes pasaba el trailer |
| `ev-v6-001707-9f2b6e31` | `LA-CAJA-DEL-29-DE-ABRIL.md:279`, `:343`, `:359` | citado a propósito como el id que la sesión estuvo a punto de inventar; `git log -S` no lo encuentra en ningún commit |
| `ev-v4-003710-f32c06e4`, `ev-v4-003710-f610cc8f` | `LA-CAJA-DEL-29-DE-ABRIL.md:357`, `:358` | citados a propósito en la tabla de §R8 |

Los 3 `ev-*` son los mismos que ya midió `LA-CAJA-DEL-29-DE-ABRIL.md` §R8. `ADR-9999` es nuevo,
porque aquella medida solo miraba `ev-*`.

## 2. La medida A: `CLAUDE.md` y `PROJECT_STATE.md`

| fichero | citas | inexistentes |
|---|---|---|
| `CLAUDE.md` | 21 `ADR-` | 0 |
| `PROJECT_STATE.md` | 255 `ADR-`, 118 `ev-*`, 2 `fb-*` | 5 citas de 3 ids |

Las cinco de `PROJECT_STATE.md` eran citas a propósito:
- cuatro en las **dos** redacciones de la deuda «la guardia de ids citados no mira `docs/**`», que
  estaba anotada dos veces (líneas 403 y 404);
- una, `ADR-9999`, en el Change Log de F09.

Por esta sorpresa se paró antes de escribir nada. El consultor decidió que `PROJECT_STATE.md` y
`CLAUDE.md` entran en el alcance de la guardia.

**Al pagar la deuda salió un error de las dos redacciones.** Las dos listaban como uno de los tres
ids inexistentes el item REAL que supersedía la copia de la auditoría, y omitían el segundo id
inventado de esa auditoría. La entrada única que queda, marcada como resuelta, lo dice sin citar
ninguno de ellos. Así, en `PROJECT_STATE.md` solo queda declarado `ADR-9999`.

**Y una omisión del brief, detectada antes de escribir.** La lista de declaraciones del consultor
para la auditoría traía un solo id. La auditoría cita dos, y el segundo (`:977`) habría dejado la
guardia en rojo. El motivo del segundo lo propuso la sesión y lo aceptó el consultor.

## 3. La guardia en ROJO sobre el árbol real, antes de declarar nada

Esperado: las 8 citas de `docs/**` más las 5 de `PROJECT_STATE.md`, 13 en total. Salieron
exactamente esas. Cada línea da solo fichero, línea e id:

```
ERROR: id citado que no existe: PROJECT_STATE.md:403: ev-v4-003710-f32c06e4
ERROR: id citado que no existe: PROJECT_STATE.md:403: ev-v6-001707-9f2b6e31
ERROR: id citado que no existe: PROJECT_STATE.md:404: ev-v4-003710-f32c06e4
ERROR: id citado que no existe: PROJECT_STATE.md:404: ev-v6-001707-9f2b6e31
ERROR: id citado que no existe: PROJECT_STATE.md:624: ADR-9999
ERROR: id citado que no existe: docs/validation/AUDITORIA-2026-09-13-ultracode.md:786: ev-v4-003710-f32c06e4
ERROR: id citado que no existe: docs/validation/AUDITORIA-2026-09-13-ultracode.md:977: ev-v4-003710-f610cc8f
ERROR: id citado que no existe: docs/validation/F09-expert-feedback-model.md:118: ADR-9999
ERROR: id citado que no existe: docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md:279: ev-v6-001707-9f2b6e31
ERROR: id citado que no existe: docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md:343: ev-v6-001707-9f2b6e31
ERROR: id citado que no existe: docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md:357: ev-v4-003710-f32c06e4
ERROR: id citado que no existe: docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md:358: ev-v4-003710-f610cc8f
ERROR: id citado que no existe: docs/validation/LA-CAJA-DEL-29-DE-ABRIL.md:359: ev-v6-001707-9f2b6e31
```

Con las declaraciones puestas: `OK: … documentos: todo id citado existe o está declarado con
motivo`.

## 4. La declaración: sintaxis, y por qué vive en el documento

Es un bloque de código con nombre fijo, `ids-inexistentes`, que se ve al renderizar y puede ir
dentro de un recuadro `>`. Una línea por id, con esta forma:

    ```ids-inexistentes
    <id según FUENTE> — <motivo>
    ```

**Las reglas, cada una con su test** (`tests/contract/test_ids_citados.py`):
1. La declaración exime ese id **solo en ese documento**.
2. Si el id declarado **existe**, falla: la declaración está obsoleta.
3. Si el id **no se cita fuera del bloque**, falla: la declaración está muerta. La mención dentro del
   propio bloque no cuenta, porque si contara la regla no podría fallar nunca. Esta corrección la
   hizo el consultor sobre su propia regla.
4. **Sin motivo** falla. También falla una línea que no empiece por un id y un segundo bloque en el
   mismo documento.

Un control que parece id y no lo es para `FUENTE` (`ADR-12345`, `ADR-0001x`,
`ev-v1-12345-0000aaaa`) se ignora.

**Un ajuste medido antes de commitear este informe.** La primera versión del parser aceptaba
cualquier sangría antes de la valla, así que el ejemplo de arriba, indentado 4 espacios para
enseñar la sintaxis, contaba como un **segundo bloque**. Ahora funciona como en CommonMark: la valla
admite como mucho 3 espacios por nivel de recuadro, y con 4 o más la línea es código. Va en su
propio commit, con su test (`3663549`).

**Por qué en el documento y no en el código.** Una lista de ids exentos en el código enumera casos
en vez de nombrar la condición, que es el patrón 3. Además separa la excepción del texto que la
justifica: quien lea el informe no ve por qué ese id no existe, y quien toque el código no sabe de
qué documento es. Con el bloque, el motivo vive junto a la cita. Las reglas 2 y 3 impiden que la
declaración se quede atrás si el id aparece después o si la cita desaparece.

**Dónde va cada declaración:**
- En los tres informes cerrados, dentro de un recuadro de corrección al principio, sin tocar el
  cuerpo. El diff de esos tres ficheros es solo de líneas añadidas.
- En `PROJECT_STATE.md`, sin recuadro, porque no es un informe cerrado: debajo de la entrada
  resuelta de Technical Debt. `state check` da exactamente lo mismo con el bloque dentro.
- En este informe, al principio.

## 5. Lo demás

- **Régimen de `docs/validation/`, en `CLAUDE.md`:** un informe cerrado en `main` se corrige con un
  recuadro al principio y el cuerpo queda intacto. Es la práctica ya seguida con `F14A-INGESTA.md` y
  ADR-0037 §7.
- **Deuda anotada, no arreglada:** nada comprueba mecánicamente que el cuerpo de un informe cerrado
  no cambie. Es el patrón 5 sin detector.
- **El conjunto de existencia se extrajo a `ids_de_fuente`**, que usan los dos validadores, el de
  los trailers y el de los documentos. Antes era una expresión en línea; ahora no puede haber dos.

## 6. Cierre

`state check` OK. `make check` en verde (819 tests, 4 contratos de importación) y log borrado. `kit
check` idéntico a la línea base. PREREGISTRO con blob `52649183…` y cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
