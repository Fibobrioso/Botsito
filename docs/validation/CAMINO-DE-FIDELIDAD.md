# El camino de fidelidad: el material ya visto se reparte por su sitio

Rama `trabajo/septiembre-particiones`, desde `d78a373` (tag `stable/F13-cupos`). Sin tocar main, sin
merge, sin tag, sin push. Sin abrir nada —ni el xlsx, ni una fila, ni las capturas, ni ningún
holdout; `PREREGISTRO.md` sigue vacío—, sin tocar `knowledge/spec/` (12.1.1, mismo hash),
`evidence/` ni `feedback/`, y sin tocar el paquete de la sesión 1.

**El nombre de la rama se quedó viejo a mitad de camino.** Se abrió para sortear las particiones de
septiembre; la revisión de diseño encontró que eso no se podía hacer, y el consultor decidió que
esta rama entrega **solo el mecanismo**. El sorteo va en la siguiente. El informe se llama por lo
que la rama hace.

## 1. La línea base, guardada antes de tocar nada

`kit check --sesion 2026-09-09-sesion-01` a un fichero: 5 líneas, exit 0. **Resultado: salida
IDÉNTICA**, medida **antes y después de descargar septiembre** y otra vez al final.

## 2. Lo que la revisión encontró, y por qué paró la rama

El brief daba por hecho que el sorteo iba por `kit build`. **No puede ir**, y está medido:

```
2026-09-09-sesion-01 -> 2026-09 visto? False
2026-09-22-sesion-02 -> 2026-09 visto? True
```

`vistos.yaml` declara `2026-09` con `visto_el: 2026-09-20`, así que para cualquier sesión fechada el
20 o después `universo()` excluye sus 14 días con motivo *«mes visto por el trader»* y `construir()`
aborta si alguno se cuela (`paquete.py:626-631`). Forzarlo exigía **falsear la fecha de la sesión** o
**desactivar el filtro de vistos**.

Y no era un descuido: **ADR-0034 §6 ya lo decía** —*«el camino del kit (`kit build`) es el del
etiquetado ciego y, por construcción, no sirve aquí»*— y dejaba abierta la decisión de cómo se
sortean esas particiones. Los dos bloqueos que ese ADR enumeraba son los que cerraron las dos ramas
anteriores; este tercero es estructural.

El coste de forzarlo, medido: **tres falsedades**. Una fecha de sesión falsa (única forma de que el
filtro no muerda), un cuestionario inventado —`validar_paquetes` exige al menos una pregunta con
casos que citen evidencia real— y el test de la puerta roto o una protección perdida.

## 3. Los nombres de partición son globales: medido

| evidencia | qué dice |
|---|---|
| `holdout.py:175` (antes) | globeaba **todos** los `kit/*/particiones.yaml` |
| `holdout.py:183-185` | guarda `caso -> particion`: **el paquete se descarta** |
| `holdout.py:146` | `abrir(repo, particion: str, para_que)` — un nombre a secas |
| `holdout.py:63` | `AUTORIZACION-{particion}.md` — **un fichero por nombre** |

Abrir `holdout-1` por una pregunta de mayo quemaría también los días de septiembre asignados a
`holdout-1`. **No está escrito en ninguna parte que no se compartan**, y los textos hablan del
nombre: `holdout/README.md` («se abre una sola vez»), ADR-0021 §6, `MASTER_PLAN` §203.

Reparto real hoy: 24 reservados, 8/8/8 (mayo 6/4/3 + junio 2/4/5).

Por eso los nombres del camino nuevo son propios: mezclar 3 días **ciegos** de mayo con 14 **no
ciegos** de septiembre daría un cubo cuya cifra no tiene interpretación, y `casos_reservados`
devuelve un mapa plano que no permite separarlos al medir.

## 4. El tamaño mínimo: no hay umbral, porque nada lo alcanza

La unidad ejecutable es la **sesión H4**, no el día (`kappa.py:3-5`): 14 días = 28 unidades brutas,
~23 efectivas con rho=0,2. El mínimo es **36 unidades efectivas independientes**
(`AUDITORIA-2026-09-13-ultracode.md:1458`, `[d7-metodo-06]`), recomputado con binomial exacta en la
revisión y coincidente.

Septiembre entero: potencia **0,50-0,68**. Mayo entero tampoco llega. Mayo **más** septiembre sí
pasaría de 36 — y es exactamente la mezcla que ADR-0034 prohíbe interpretar como una cifra.

**Conclusión, y va escrita en el ADR, en el README del directorio y en el módulo**: lo que este
camino aporta **no es una cifra con potencia** sino **anterioridad demostrable** más una **cifra
descriptiva con su intervalo**. Es lo que impide que dentro de seis meses alguien cite esa cifra como
si midiera algo.

## 5. El 1-18, y un hecho que cambia la pregunta

**19 y 20 de septiembre de 2026 son sábado y domingo** (medido). `dias_laborables` (`ventanas.py:91`)
no los genera: hoy no pueden entrar al universo ni gastar holdout. El mecanismo hace falta igual —el
día que alguien re-descargue el mes entero entran 8 laborables sin material, y el camino de fidelidad
**se salta el filtro de vistos**, con lo que la cobertura pasa a ser el único filtro que queda—.

`cobertura_material`, clave opcional del bloque `config:`, lista de **tramos**, con motivo propio:

```yaml
- dia: '2026-09-21'
  motivo: fuera de la cobertura del material del trader (2026-09 cubre 2026-09-01..2026-09-18)
```

**Y una captura que no estaba nombrada en ningún sitio:** `cobertura_material` **no puede admitir una
lista de días**. `SEPTIEMBRE-ENTRA.md:22-26` deja escrito que un día laborable del rango que no
aparezca en la columna de fechas *«sería un día sin operaciones, y eso es su etiqueta»*. Declarar los
días cubiertos publicaría esas etiquetas por la puerta de atrás. El validador lo rechaza **por la
forma**, con el motivo dicho en el mensaje de error, y hay un test que lo ve fallar.

## 6. La descarga

`congelar` rechaza `hasta >= hoy` **antes de tocar la red** (`dataset.py:148`), así que el máximo
legal hoy era el día 20. Manifiesto `eurusd-m1-2026-09-9d707383`: del 1 al 20, **20 días presentes,
20.036 velas, cero ausentes**, sin datos los tres sábados (5, 12, 19).

Y lo que costaron dos ramas, medido: **`kit check` de la sesión 1 idéntico a su línea base con
septiembre en disco**. Antes de ADR-0035 esta descarga habría reparticionado la sesión 1 en silencio.

## 7. Qué se construyó

1. **`cases/fidelidad.py`** y `knowledge/cases/fidelidad/`: un artefacto es un universo, un reparto y
   un ancla. Sin cuestionario, sin hoja, sin sesión, sin fecha en el id. Reutiliza `universo()`,
   `asignar()`, el congelado de ADR-0035 y el ancla; **no duplica ninguna**.
2. **El filtro de vistos se salta a propósito**, escrito en tres sitios. El kit no se toca.
3. **`cobertura_material`** (§5), y en este camino un mes **sin** cobertura declarada no aporta
   ningún caso: existe para repartir material etiquetado. Los manifiestos de los demás meses se
   siguen pasando, porque el día 1 necesita las velas de la víspera.
4. **Nombres propios con puerta**: `fidelidad-1..3` son reservadas y pasan por `holdout.py`, con su
   `AUTORIZACION-fidelidad-N.md`. `repartos_commiteables` agrega los dos caminos.
5. **`cases/anterioridad.py`**: la anterioridad por **CASO**, enganchada en `knowledge validate`,
   sin `data/`.

## 8. Los tests, con sus mutantes

- `test_mutante_la_etiqueta_antes_que_su_reparto_falla`: el mutante que manda. También el caso del
  **mismo commit**, que tampoco vale.
- `test_una_etiqueta_sobre_un_caso_sin_reparto_no_pasa`: el agujero entero en una línea.
- `test_empareja_por_caso_aunque_la_sesion_sea_de_otro_paquete`: **lo que hoy pasaba y ya no pasa**.
- `test_un_caso_repartido_dos_veces_es_problema`.
- `test_el_camino_de_fidelidad_reparte_lo_que_el_material_cubre`: el filtro de vistos saltado (un día
  visto **es** caso aquí), el motivo propio de la cobertura, y que **nada se exime** —con un mutante
  sobre un campo que la recomposición sí regenera, porque mutar el bloque congelado no serviría: se
  recompone **con** él, y para eso está el ancla—.
- `test_un_mes_sin_material_declarado_no_aporta_casos`.
- `test_cobertura_material_no_admite_una_lista_de_dias`, más tramos al revés, de otro mes y solapados.
- `test_los_casos_reservados_...` **cambia a una afirmación más fuerte**: la **unión exacta** de todos
  los repartos de los dos caminos, más el reparto concreto de la sesión 1. No se rompe al añadir un
  camino, y caza lo que la anterior no veía: un camino fuera del glob de la puerta.

## 9. Lo que NO se ha hecho

- **El sorteo de septiembre.** Va en la rama siguiente. Los cupos de
  `knowledge/cases/fidelidad/config.yaml` están **en cero** y no existe ningún artefacto: el
  mecanismo queda estrenado en vacío a propósito, porque un ADR decidido y estrenado en el mismo
  aliento acaba con la forma de la conveniencia de un mes.
- **El agujero de `excluir`** en `kappa_entre_sesiones`: tras pasar la puerta queda vacío y una
  autorización lee las etiquetas de todos los cubos. Queda **bloqueante para ABRIR**, escrito en
  ADR-0036 §6 y en el README del directorio. Hoy es seguro porque `PREREGISTRO.md` sigue vacío.
- **Re-descargar un mes** sigue rompiendo `kit build` en silencio: dos manifiestos del prefijo que
  cubran el mismo día dan *«dos datasets cubren el mismo día»*, y `reemplaza_a` se escribe para
  datasets pero **nadie lo lee**. La descarga de hoy nos ata al rango 1-20: si el trader entrega del
  19 al 30, se choca con esto. Anotado como deuda con nombre.

## 10. Qué debe decidir el usuario

Validar la rama. Y para la siguiente: **los cupos de septiembre**, con su `Fuente:` y su argumento,
**después** de ver cuántos casos quedan de verdad —`asignar` descarta el sobrante en silencio, que es
como la sesión 1 perdió dos días—. Lo medido: partir 14 días en tres cubos quema las tres aperturas
del proyecto en una sola pregunta y baja la potencia de 0,68 a ~0,27 por cubo.

## 11. Cómo comprobarlo

```
uv run botsito kit check --sesion 2026-09-09-sesion-01     # identico a la linea base
uv run botsito knowledge validate                           # exit 0
uv run pytest tests/contract/test_anterioridad.py tests/unit/test_puerta_holdout.py -q
uv run pytest tests/unit/test_kit.py -k "fidelidad or cobertura or material" -q
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
