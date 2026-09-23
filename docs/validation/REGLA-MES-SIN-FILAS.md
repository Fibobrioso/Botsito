# La regla del mes sin filas

Rama `trabajo/regla-mes-sin-filas`, 2026-09-23. Sin merge, sin tag y sin push. Es Next Action 13:
decidir, antes de que llegue marzo, qué hacer con la regla de `ingerir` que para el comando cuando
un mes pedido no tiene filas. Febrero no se ha tocado, marzo no existe en esta rama, y no se ha
leído ningún libro real: todo lo medido sale del código y de libros sintéticos.

## 1. El criterio, fijado por el consultor antes de medir

> - se **mantiene** si detecta al menos una situación que nada más detecta y no toca días
>   reservados;
> - se **restringe** a los días pedidos si detecta algo único pero cuenta sobre el mes completo;
> - se **quita** si todo lo que detecta ya lo detecta otro mecanismo;
> - se **convierte en aviso** solo si bloquea casos válidos (d o e) y lo que detecta no es único.

## 2. Lo que hace la regla, leído del código

- **Condición:** `{d[:7] for d in pedidos} − {f["_dia"][:7] for f in filas}` no está vacío.
- **Dónde:** `src/botsito/cases/ingesta.py`, en `ingerir`, después de leer y antes de procesar
  ninguna fila. Aborta con `IngestaError` y no escribe nada.
- **Desde:** `c9cfbc6` (2026-09-21, rama de cobertura). Llegó a `main` con `stable/F14-cobertura`.
- **Cuenta SOLO sobre los días pedidos, no sobre el mes completo.** `filas` sale de
  `filas_de_los_dias(…, pedidos, …)`, que descarta sin contar toda fila de un día no pedido. Que un
  mes «no tenga filas» quiere decir que **ninguno de los días pedidos** de ese mes las tiene. Lo que
  sí toca todo el libro es el lector, que parsea en memoria el `dateStart` de cada fila para saber
  de qué día es; eso ocurre antes de la regla y no es parte de ella.
- **Por la CLI, desde ADR-0039, solo puede disparar con un mes:** `dias_del_material` limita los
  pedidos al mes que declara el sha del libro.

## 3. La tabla de situaciones

Cada fila lleva el test que la demuestra, o «sin test» si no lo había. Los tests nuevos de esta
rama van marcados.

| situación | con la regla | sin ella | otro mecanismo | test |
|---|---|---|---|---|
| **a1)** libro equivocado cuyo sha no está declarado para ningún mes | no se llega a la regla | igual | **sí**: `dias_del_material` (sha fuera del manifiesto o sin tramo) y `libros.yaml` (sin declaración no se lee) | `test_mes_del_material::test_b_un_sha_que_no_declara_ningun_tramo_es_error_y_no_escribe`, `::test_b_un_libro_fuera_del_manifiesto_es_error_y_no_escribe`; `test_libros::test_sin_declaracion_no_se_lee_y_con_una_ajena_tampoco` |
| **a2)** libro con su sha atado al tramo de OTRO mes | **error** de la regla | exit 0, 0 casos y el aviso de días sin operaciones: **pasa en silencio** | **ninguno** | **nuevo:** `test_regla_mes_sin_filas::test_a2_un_libro_atado_al_tramo_de_otro_mes_lo_para_la_regla` |
| **b)** huso mal declarado, caso extremo: todas las filas de los días pedidos salen del mes | **error** de la regla | pasa en silencio | ninguno en el código; al declarar, el método de velas con control (ADR-0039) | **nuevo:** `test_regla_mes_sin_filas::test_b_extremo_un_huso_mal_declarado_que_saca_todas_las_filas_del_mes_lo_para_la_regla` (con control en UTC) |
| **b)** huso mal declarado, caso normal: filas que se van a otro día del mes que no se pidió | no dispara | igual | la sesión H4 caza las que caen fuera de sesión; **las que caen dentro, nada** | **sin test**: hoy nada lo detecta (§6) |
| **c)** formato de fecha mal declarado | no se llega: el lector falla antes | igual | **sí**: el lector parsea solo con lo declarado (ADR-0039) | `test_libros::test_un_libro_en_un_formato_distinto_del_declarado_falla`, `::test_un_dia_mes_ambiguo_no_se_lee_con_ninguna_declaracion` |
| **d)** ninguno de los días pedidos tiene filas en el libro correcto | **error** (coste aceptado, §4) | exit 0, 0 casos | ninguno lo distingue de a2 | **nuevo:** `test_regla_mes_sin_filas::test_d_dias_pedidos_sin_ninguna_fila_en_un_libro_correcto_dan_el_mismo_error` |
| **e)** algunos días pedidos sin operaciones, en un mes que sí tiene filas | no dispara; se cuentan como días sin operaciones | igual | es el comportamiento normal | `test_cobertura::test_los_dos_ceros_se_distinguen` (a); `test_mes_del_material::test_a_y_el_otro_mes_con_su_libro_ingiere_el_suyo` |
| **f)** todos los días pedidos son reservados | no se llega a la regla | igual | **sí**: la puerta los quita; por la CLI, «ese mes no tiene ningun dia ingerible en el camino del kit», sin nombrar ninguno | `test_ingesta::test_un_dia_reservado_no_se_ingiere_ni_se_nombra`, que llama a `ingerir`; **nuevo, por la CLI:** `test_regla_mes_sin_filas::test_f_si_todos_los_dias_pedidos_son_reservados_no_hay_nada_que_leer_y_no_se_nombra_ninguno` |

## 4. La aplicación del criterio: SE MANTIENE

- **Detecta algo único:** a2, un libro cuyo sha está atado en `cobertura_material` al tramo de otro
  mes. Ningún otro mecanismo lo ve. Sin la regla, el comando termina con exit 0, sin escribir nada,
  y solo con un aviso.
- **No toca días reservados:** cuenta sobre los días pedidos y nada más (§2).
- Así que no se restringe, porque ya está restringida a los días pedidos, y no se quita.
- **No se convierte en aviso**, aunque bloquea el caso d: lo que detecta es único.
- **El coste aceptado es d.** La regla no puede distinguir «el libro no es de este mes» de «ninguno
  de los días pedidos tiene filas en la exportación»: los dos dan exactamente el mismo cero sobre los
  días pedidos. En d no hay nada que escribir, así que parar no pierde ningún caso; solo obliga a
  mirar. El test de d lleva ese razonamiento en su docstring.

## 5. El mensaje: decía más de lo que la regla sabe

**Antes:**

    el material que se ha pasado no tiene ni una fila de <mes>: o es el libro de otro mes, o falta.
    No se escribe nada, porque un cero de aqui no se puede distinguir de un dia sin operaciones

Afirmaba algo del mes entero, que la regla no comprueba. Si el libro tuviera filas únicamente en
días reservados de ese mes, el mensaje diría algo falso sobre él. No era una fuga de datos, pero sí
el patrón 5: el mensaje dice una cosa y la regla comprueba otra.

**Ahora** (`mensaje_mes_sin_filas`, comparado con su texto exacto en los tests):

    ninguno de los dias pedidos de <mes> tiene filas en este material: o el libro no es de <mes>
    (revisa a que tramo de cobertura_material esta atado su sha), o esos dias no tienen ninguna fila
    en la exportacion. No se escribe nada

**Una desviación del brief, dicha.** El texto propuesto decía «o el trader no operó ninguno de
esos días». El aviso hermano de días sin operaciones se reescribió en la rama de cobertura para ir
**sin sujeto humano**, con el motivo escrito en `ingesta.py`: de una ausencia de filas salen dos
lecturas, que no operó o que operó y la fila no está en la exportación, y quedarse con la primera
sería atribuirle una decisión al trader. El brief pedía el texto «más o menos así», y el mensaje
sigue esa misma regla.

## 6. El hueco que queda: el caso normal de b

Con el huso mal declarado, una fila puede caer en **otro día del mismo mes que no se pidió**, y el
lector la descarta sin contarla. **Ningún código lo detecta**:
- la regla solo caza el extremo en que todas las filas salen del mes;
- la comprobación de sesión H4 solo caza las que caen fuera de sesión.

Hoy solo lo evita el **procedimiento** de velas con control de ADR-0039 al declarar el libro. Queda
en Technical Debt como patrón 5 sin detector, y no se arregla aquí.

## 7. Cierre

`state check` OK. `make check` en verde (826 tests, 4 contratos de importación), con el log borrado.
`kit check --sesion 2026-09-09-sesion-01` idéntico a la línea base. PREREGISTRO con blob
`52649183…` y cero autorizaciones.

## Estado

WAITING_FOR_USER_VALIDATION
