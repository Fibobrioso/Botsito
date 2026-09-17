# Los meses vistos, y qué puede etiquetar la sesión 2 — INFORME DE VALIDACIÓN

**Rama:** `trabajo/meses-vistos` (rama de trabajo sin número propio, MASTER_PLAN §F), desde `main` en `c49f99a`
**Cierre previsto:** tag `stable/F13-vistos`
**Decisión:** mecanismo del kit (ADR-0011) con nota; sin ADR nuevo
**spec_version:** 12.0.0 sin tocar, con el mismo hash
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 1. Por qué existe esta rama

`knowledge/cases/kit/vistos.yaml` declaraba de sí mismo un hueco abierto desde el 2026-09-12.
Mayo 2026 debía estar en la lista, porque el trader lo backtesteó entero y lo entregó el 2026-09-11.
Pero añadirlo invalidaba el paquete de la sesión 1, construido cuando mayo era ciego: *«se piden 40
casos y el universo tiene 22»*. Lo que quedaba era una instrucción a un humano, *«MAYO NO ES CIEGO, no
lo sortees»*. Es lo único que bloqueaba cualquier versión de la sesión 2.

No se ha abierto ningún holdout. `PREREGISTRO.md` sigue vacío. `knowledge/spec/`,
`knowledge/evidence/` y `knowledge/feedback/` no se han tocado.

## 2. La prueba que manda, primero

**`kit check --sesion 2026-09-09-sesion-01` sigue reproduciendo el paquete byte a byte con mayo ya
declarado visto.** Medido en el repositorio real, con `data/` presente:
- **Línea base, en `main`, antes de tocar nada:** `exit=0`, con dos AVISO esperados
  (`cuestionario.yaml` y `hoja_trader.md`, por ser una sesión celebrada), las dos líneas `LECTURA:`
  y el OK. `particiones.yaml` y `ventanas.yaml` no dan ni error ni aviso: se reproducen byte a byte.
- **Con mayo declarado visto:** la misma salida, línea a línea (comparada con `diff` sobre la salida
  ordenada). Medido dos veces: tras escribir `vistos.yaml` y sobre el commit del mecanismo.

La lectura de velas quedó declarada por recuento («24 dias reservados…»), como exige ADR-0033.

## 3. La revisión de diseño (dos agentes, antes de programar)

**A** (Opus): con qué fecha se compara y dónde vive la guardia. Midió con prototipos sobre el kit
sintético y, en el repositorio real, solo con `git log` y `commit_que_anadio`. **B** (Sonnet): (a) o
(b) y qué se anota para F26, leyendo `particiones.yaml`, `ventanas.yaml`, la hoja, el corpus y los
ADR, sin abrir `data/` ni el holdout.

### Pregunta 1 · Con qué fecha se compara `visto_el`: con la del NOMBRE DE LA SESIÓN

| Candidata | Medido | Veredicto |
|---|---|---|
| **(i) La fecha del nombre** (`2026-09-09-sesion-01`): el día en que el trader etiqueta | Con mayo en `2026-09-11`, el paquete del 09-09 comprueba `([], [])` y sus 4 ficheros salen idénticos; con el código anterior, `KitError: se piden 5 casos y el universo tiene 0`. Una sesión del 09-11 o del 09-15 falla; una del 09-10 construye. Moverla al 09-22 con `mover_sesion` falla, y el script restaura el paquete intacto; ida y vuelta al 09-10, igual | **Elegida** |
| (ii) El commit que añadió `particiones.yaml` | Hoy devuelve `6266738` (2026-09-09), que es el commit del MOVE y no el del build (`bf9471c`, 09-08), porque `historial.py` no sigue renombrados. Tras cualquier move daría la fecha del move, y un move posterior al 11 rompería la sesión 1. Sin commit devuelve `None`: `kit build`, `mover_sesion` y un `kit check` sin commitear se quedan sin fecha | Descartada |
| (iii) Una fecha nueva dentro del paquete | `comprobar` compara el texto entero: una clave nueva rompe la reproducción de la sesión 1. Si se saca de `date.today()` deja de ser determinista; si se saca del nombre, es la (i) | Descartada |

**La semántica también elige la (i).** Lo que hace ciego un etiquetado es que el trader no haya visto
el mes cuando etiqueta, no cuándo se construyó el paquete. Con `mover_sesion` funciona: si una sesión
se mueve a una fecha posterior al `visto_el` de un mes que contiene, los casos cambian y el script se
niega y restaura. En el caso real ni se llega ahí: la sesión 1 tiene registros de feedback y el script
ya se niega a moverla.

**`visto_el` cuenta si es igual o anterior a la fecha de la sesión.** Mayo se entregó el 09-11: una
sesión ese mismo día ya no lo tiene por ciego.

**Una trampa medida, y cubierta:** poner a una entrada ya usada una fecha POSTERIOR a un paquete que la
excluyó la saca de ese paquete y rompe su reproducción, y sin `data/` nada lo veía. Ahora lo denuncia
`knowledge validate`.

### Pregunta 2 · Dónde vive la guardia: en los dos caminos

- **`construir()`**, que usan `kit build`, `kit check` y `mover_sesion`. El universo se filtra con lo
  visto a más tardar el día de la sesión. Si un día visto se colara igual, `KitError`: **falla, no
  avisa**. Un paquete de una sesión del 09-11 o posterior no puede sortear mayo.
- **`validar_paquetes()`**, que usa `knowledge validate`: corre en `make check` y en CI, sin datos.
  Denuncia un paquete ya escrito con días vistos antes de su sesión, y un día que el paquete excluyó
  como visto cuya entrada ya no lo sostiene (quitada, o fechada después). Medido: con el código
  anterior, ninguno de los dos casos daba un solo error.

**`visto_el` es obligatorio** en meses y en días; sin él, `kit build` y `knowledge validate` fallan
con el motivo. «Visto desde siempre» es justo la suposición que rompía la sesión 1.

### Pregunta 3 · (a) o (b): **(a), confirmada midiendo, con tres condiciones**

**Lo que hay en el paquete de la sesión 1** (verificado contra `particiones.yaml` y `ventanas.yaml`):
- 40 casos, 19 de mayo y 21 de junio, de un universo de 42 (quedan fuera 2026-05-25 y 2026-06-29);
- `dev` 16: 6 de mayo y 10 de junio;
- holdout 8/8/8;
- 67 días excluidos.

Las cifras del brief cuadran.

**¿Sirven de verdad los `dev` de junio?**
- **No hay nada que diga que el trader viera junio.** Búsqueda exhaustiva de `junio`, `2026-06` y
  `june` en evidencia, feedback, `fuentes.yaml` y documentos: ninguna fuente. La operativa real de
  fondeo empieza el 2026-08-20, y los vídeos v1 a v6 son de agosto y septiembre.
- **Los datos de los 10 días `dev` de junio están bien.** Todos pasan de `min_velas` (850); el
  más bajo tiene 896. El 19 de junio (Juneteenth) tiene 898 velas y nada raro.
- **ADR-0025 descartó junio del universo de F14 por falta de material, no por exposición:** *«el
  trader se comprometió a dos meses y entregó uno, así que para junio no hay ninguna decisión suya
  con la que comparar»*. Una sesión en vivo no necesita ese backtest, porque el trader etiqueta
  delante.

**Las tres condiciones de (a), que el brief no tenía:**
1. **La confirmación escrita sobre junio NO se puede dar por supuesta.** La CONFIRM de la sesión 1
   (`fb-2026-09-09-sesion-01-c79021dc`) dice que el trader *«no ha visto esos meses aún, hará el
   backtest con todas las reglas discutidas ahora»*, y habla de mayo **y junio**. Entregó mayo; de
   junio no entregó nada, pero se comprometió a hacerlo. **Si lo backtesteó sin entregarlo, junio
   tampoco es ciego.** Es la condición previa que el README del kit ya exige: antes de la sesión 2,
   confirmación escrita de que no ha operado ni backtesteado junio. Si dice que sí, junio entra en
   `vistos.yaml` con su `visto_el` y (a) se queda sin días ciegos.
2. **La hoja del trader de la sesión 1 enseña los 16 `dev`, mayo incluido.** Para la sesión 2 hay que
   regenerar el material dejando los `dev` de mayo fuera del etiquetado ciego (no borrarlos del
   paquete: el paquete no se toca).
3. **La guardia de ancestro no ve las etiquetas de otra sesión.** `validar_paquetes` solo arma la
   guardia con `LABEL_CASE` cuya `sesion` coincide con la del paquete (`r.sesion == sesion`).
   Etiquetas registradas como sesión 2 sobre casos del paquete de la sesión 1 quedarían FUERA de la
   única prueba mecánica de que las particiones se fijaron antes de etiquetar (lo anotó la auditoría
   del 2026-09-13, [d7-metodo-03]). Lo tiene que resolver el brief del paquete de la sesión 2, antes
   de registrar la primera etiqueta.

**Por qué no (b), medido:**
- **No llega a los cupos.** Con mayo visto, un paquete solo de junio tiene un universo de unos 22
  días laborables, y `config.yaml` pide 40 (16/8/8/8). Habría que cambiar los cupos.
- **Cambiar los cupos rompe la sesión 1.** `config.yaml` es global y `comprobar()` compara el config
  guardado en la sesión 1 con el de hoy, sin excepción: `kit check` de la sesión 1 fallaría con
  «config.yaml cambio despues de generar el paquete». Es un bloqueo mecánico, no solo de ADR.
- **Exige ADR.** `knowledge/cases/holdout/README.md` («Reparticionar») lo pide, y ADR-0025 ya se
  negó a pagar por menos la pérdida de la prueba de anterioridad.
- **Nada impediría asignaciones contradictorias.** El mismo `caso-eurusd-2026-06-DD` podría acabar en
  una partición en la sesión 1 y en otra en el paquete nuevo.

| | (a) paquete de la sesión 1 | (b) paquete nuevo, solo junio |
|---|---|---|
| Días `dev` ciegos | **10** (junio), si el trader confirma por escrito que no lo backtesteó | ~22 × 16/40 ≈ 9, con otro reparto |
| Qué se pierde | los 6 `dev` de mayo como etiquetado ciego | la unicidad de la prueba de anterioridad; `kit check` de la sesión 1, salvo que el config deje de ser global |
| Qué exige | confirmación escrita sobre junio; material sin los `dev` de mayo; resolver la guardia de ancestro para etiquetas de otra sesión | ADR de reparto; config por paquete; guardia contra asignaciones contradictorias |

### Pregunta 4 · Qué se anota para F26 sobre los `dev` de mayo

**Mecanizado, y verificable por test:** `kit kappa` avisa cuando una ronda tiene unidades sobre días
que el trader ya había visto el día de la sesión que las etiquetó: «N casos etiquetados sobre dias que
el trader ya habia visto el <fecha> (vistos.yaml): no fue etiquetado ciego». No excluye esas unidades,
porque el kappa mide consistencia y sigue sirviendo, pero lo dice en la salida, que es donde F26 lo va
a leer. Sale de `vistos.yaml` y de la fecha de la sesión: no depende de que alguien lo recuerde.

**Solo texto:** una nota en `knowledge/cases/kit/README.md` (condición previa de cada sesión). No es
una fila de `HOLDOUT-EXPOSICIONES.md`: los `dev` no son holdout.

## 4. Qué se hizo

| Pieza | Hecho | Dónde |
|---|---|---|
| **`visto_el`** | Obligatorio en meses y días, AAAA-MM-DD. Una entrada cuenta para un paquete si `visto_el` ≤ fecha de su sesión | `cases/paquete.py`: `cargar_vistos_fechados`, `cargar_vistos(ruta, hasta)`, `fecha_de_sesion` |
| **Mayo visto** | `visto_el: 2026-09-11`, con su motivo y su fuente: el commit del corpus `8fb2323`, «entra el backtest de mayo». La CONFIRM de la sesión 1 se cita en el motivo y no en `fuente`, porque prueba lo contrario: que el 09-09 mayo aún no estaba visto | `knowledge/cases/kit/vistos.yaml` |
| **Fechas de los otros cuatro** | Las de sus fuentes, en `knowledge/corpus/manifest.yaml`: enero 2026-08-30 (v4), julio 2026-08-03 (v2, la más antigua de sus dos fuentes), agosto 2026-08-20 (v1), abril 2026-09-05 (v5, ver §6). Todas anteriores a la sesión 1, así que su reproducción no depende de ellas | `vistos.yaml` |
| **Guardia en el kit** | Filtro por fecha en `_cargar_todo` y `KitError` en `construir` si un día visto se colara | `cases/paquete.py` |
| **Guardia sin datos** | `knowledge validate` denuncia días vistos dentro de un paquete y exclusiones que ya no se sostienen | `cases/paquete.py:_problemas_de_vistos` |
| **Aviso para F26** | `kit kappa` avisa de etiquetado no ciego | `cases/paquete.py:kappa_entre_sesiones` |
| **El hueco** | Desaparece del comentario de `vistos.yaml`, que ahora describe el mecanismo y la trampa de refechar una entrada ya usada | `vistos.yaml` |

**Tests** (`tests/unit/test_kit.py`, kit sintético):
- el paquete del 09-09 sigue comprobando `([], [])` tras declarar mayo visto el 09-11, y
  `knowledge validate` no le encuentra nada;
- `kit build` para sesiones del 09-11 y del 09-15 falla, y del 09-10 construye;
- la guardia de `construir` falla con el filtro apagado;
- `knowledge validate` denuncia un paquete escrito con días de mayo, un día refechado después de la
  sesión y un día quitado;
- `visto_el` es obligatorio y con formato;
- el kappa avisa de etiquetado no ciego en la sesión posterior y no en la anterior.

## 5. Lo que cambió respecto al brief

| Pedía el brief | Se hizo | Motivo |
|---|---|---|
| «La fecha del paquete» | La fecha de la SESIÓN (del nombre) | Es la del etiquetado, que es lo que decide si es ciego; la del commit es la del último move, y una fecha dentro del paquete rompe la reproducción (§3) |
| Guardia en `kit build` | Y en `knowledge validate`, sin datos | En CI no hay `data/`, y `kit check` solo avisa sin datos: un paquete escrito con días vistos solo lo vería `knowledge validate` |
| Fuente de mayo: el commit del corpus | El commit `8fb2323` en `fuente`, y la CONFIRM de la sesión 1 en el motivo | La CONFIRM sostiene que mayo era ciego el 09-09 -lo contrario de una fuente de «visto»- y es donde el trader dice que hará el backtest de mayo y junio |
| No pedía nada sobre el kappa | `kit kappa` avisa de etiquetado no ciego | Es la forma mecanizable de la pregunta 4 |
| (a) recomendada | (a) confirmada, con tres condiciones que el brief no tenía (§3) | Medido |

## 6. Lo que esto NO cubre, y queda declarado

- **La fecha de abril no cuadra entre sus fuentes.** El motivo de `vistos.yaml` dice que el xlsx de
  abril está en el corpus «desde el 2026-09-03», y el commit que lo trajo (`da71091`) es del
  2026-09-05. Se fecha con v5 (09-05), que es la fuente citada. No afecta a ningún paquete: no hay
  dataset de abril.
- **Las fechas son «a más tardar».** Son las de la fuente citada; el trader pudo verlo antes. Solo
  importaría si una sesión cayera entre la fecha real y la de la fuente.
- **Las etiquetas de la sesión 1 posteriores al 11 sobre días de mayo** llevarían `fecha: 2026-09-09`
  por contrato y no serían ciegas. Hoy no existe ninguna (0 `LABEL_CASE`). La guardia por fecha de
  sesión no las vería.
- **Congelar un dataset nuevo con el prefijo del kit ya rompe hoy la reproducción de la sesión 1**
  (medido por la revisión A: ventanas, particiones y hoja difieren). No lo introduce esta rama, pero
  el siguiente paquete necesitará meses nuevos y hay que resolverlo antes de construirlo.
- **Construir el paquete de la sesión 2**, fuera de alcance: va con su brief, la confirmación escrita
  del trader sobre junio y las tres condiciones de §3.

## 7. La auditoría de cierre

Dos agentes en paralelo (Sonnet, solo lectura; prohibido `data/`, el holdout y ejecutar el kit sobre el
repositorio real): uno sobre código y tests, con mutantes aplicados por `monkeypatch` sobre el kit
sintético; otro sobre documentos y proceso.

**Código y tests: sin hallazgos que bloqueen.**
- **Mutantes:** los cuatro pedidos (quitar el filtro de `_cargar_todo`, quitar la guardia de
  `construir`, quitar `_problemas_de_vistos` y cambiar `<=` por `<`) los caza algún test. Con el filtro
  y la guardia de `construir` apagados a la vez, `knowledge validate` sigue denunciando el paquete
  escrito.
- **Bordes sin falsos positivos:**
  - los `dias:` sueltos se filtran con la misma regla que los meses;
  - un `vistos.yaml` malformado da un problema limpio;
  - los `excluidos` por otros motivos no hacen ruido;
  - un nombre de sesión inválido no llega a validarse.
- **`mover_sesion`:** sigue funcionando, y si la fecha nueva cruza un `visto_el`, `construir` falla
  limpio.
- **Kappa:** el aviso usa la fecha de cada ronda por separado, y `c[-10:]` es siempre la fecha por
  construcción del id de caso (`ventanas.py`).
- **La única laguna ya estaba declarada en §6:** una etiqueta tardía dentro de la misma sesión.

**Documentos y proceso:** todas las fechas de `vistos.yaml` coinciden con `fecha_grabacion` o con el
commit citado, y en julio y agosto son las de la fuente más antigua. Todas las cifras de §2 a §6 están
verificadas contra el repositorio, la cita de ADR-0025 es literal, y los trailers `Fuente:` y los
documentos vivos están bien.

| Hallazgo | Gravedad | Quién | Qué se hizo |
|---|---|---|---|
| La entrada de mayo citaba en `fuente:` la CONFIRM de la sesión 1, que prueba lo contrario -que el 09-09 mayo aún no estaba visto- | baja | documentos | **Corregido**: `fuente: [8fb2323]`; la CONFIRM queda en el motivo |

## 8. Qué debe decidir el usuario

1. **¿Validar la rama y hacer el ritual** (§10)?
2. **La fecha de la sesión, y no la de construcción, decide qué es ciego.** ¿De acuerdo? La
   consecuencia práctica es que un paquete construido antes de que el trader vea un mes, y celebrado
   después, queda denunciado.
3. **(a) con sus tres condiciones.** ¿Se pide ya al trader la confirmación escrita de que no
   backtesteó junio? Su CONFIRM del 09-09 decía que lo haría.
4. **Abril se fecha el 09-05**, con la fuente que lo sostiene, y no el 09-03 del motivo. ¿Vale?

## 9. Cómo comprobarlo

```
git checkout trabajo/meses-vistos
make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log
uv run botsito kit check --sesion 2026-09-09-sesion-01   # misma salida que en main: exit 0, dos AVISO, LECTURA, OK
uv run pytest tests/unit/test_kit.py -q -k "vist or guardia or kappa_avisa"
uv run botsito knowledge validate
git diff c49f99a..HEAD --stat -- knowledge/spec knowledge/evidence knowledge/feedback   # vacio
```

## 10. El ritual de cierre (lo ejecuta el usuario)

Nada de esto lo ha hecho la sesión. Con líneas `!` en Claude Code, **cada línea abre una shell nueva**:
`BOTSITO_ALLOW_MAIN=1` va pegada al `git commit`.

```
git checkout main
git status --short                 # vacio

git merge --no-ff trabajo/meses-vistos -m "merge: los meses vistos, con fecha"
git tag -a stable/F13-vistos -m "Meses vistos: visto_el por fecha de sesion, mayo declarado visto, guardia en el kit y en knowledge validate"
git rev-parse --short HEAD

git add PROJECT_STATE.md
git diff --cached --name-only      # SOLO PROJECT_STATE.md
BOTSITO_ALLOW_MAIN=1 git commit -m "docs(state): los meses vistos, cerrados en main (stable/F13-vistos)"

make check > make-check.log 2>&1; echo "exit=$?"; tail -5 make-check.log; rm make-check.log

git push origin main
git push origin stable/F13-vistos
```

Entre el merge y el `docs(state)`, `state check` falla a propósito. Si `make check` falla, no se
pushea. La CI que cuenta es la del `docs(state)`.

## Estado
WAITING_FOR_USER_VALIDATION
