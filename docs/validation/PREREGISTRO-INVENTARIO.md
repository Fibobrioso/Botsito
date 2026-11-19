# PREREGISTRO-INVENTARIO · Lo que hace falta para rellenar PREREGISTRO.md (R5.1, entrada G) · primer tiempo: fase 0

> PLANTILLA hasta la fase 0 (la línea con que nació): la fase 0 ya está, abajo.

Rama `trabajo/preregistro`, abierta el 2026-11-19 desde `main` en e490fe33 (commit de estado sobre
el merge 50f6a6fc del tag `stable/F39f-laminas-sesion-7b`). Encargo:
`docs/encargos/trabajo-preregistro.md`. Tramo: R5 (R5.1 de `docs/plan/HOJA-DE-RUTA.md`; la G de la
Next Action). Tag previsto: `stable/F39g-preregistro` (no existe ni en local ni en origin:
`git tag -l 'stable/F39g*'` y `git ls-remote --tags origin 'stable/F39g*'` vacíos). Riesgo: **alto**,
como manda el encargo (toca la puerta del holdout).

```ids-inexistentes
ADR-0087 — el de S-15, que nunca se creó; se cita como precedente de un número saltado
ADR-0095 — declarado inexistente por trabajo/laminas-sesion-7b; se cita para decir por qué no se usa
ADR-0096 — el número que le tocaría al ADR del pre-registro; no se crea en esta fase
```

## La base, comprobada al abrir (skill `abrir-rama`, paso 1)

- `git rev-parse --short main` = `e490fe33`, y `git rev-parse main origin/main` da dos veces
  `e490fe3361701bb30f1d5708674d1acf0678d813`.
- `git rev-parse "stable/F39f-laminas-sesion-7b^{commit}"` = `50f6a6fc9293bdb5f9b72a54a9d394e10289b89f`
  = `git rev-parse main^1`; el tag está en origin (`git ls-remote --tags origin` lo da).
- CI de `main` sobre e490fe33: run **44576448998**, `completed` / `success`
  (`gh run view 44576448998 --json headSha,status,conclusion`: `headSha` =
  `e490fe3361701bb30f1d5708674d1acf0678d813`).
- `git branch --list` solo da `main`; `git ls-remote --heads origin "fix/*"` sale vacío.

## Cómo se hizo, y qué no se tocó

Solo lectura del repo, más tres guiones que imprimen recuentos, commiteados en
`anexos/PREREGISTRO-INVENTARIO/` con su salida:

| Guion | Qué lee | Qué imprime | Salida |
|---|---|---|---|
| `recuento_particiones.py` | `casos_reservados`, `casos_retirados`, `casos_medidos` y `cargar_retirados` (`src/botsito/cases/holdout.py`), y los VALORES de la `asignacion` de cada reparto de `repartos_commiteables` | días por partición, retirados (y cuántos con `retirado_el` anterior al 2026-10-17), medibles; ninguna clave | `recuento-particiones.txt` |
| `exposiciones_por_particion.py` | `docs/validation/HOLDOUT-EXPOSICIONES.md` | filas que nombran cada partición y su fecha de declaración (primera columna); nada del contenido | `exposiciones-por-particion.txt` |
| `densidad_construccion.py` | `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` (construcción) | operaciones del trader por día `dev` y por mes | `densidad-construccion.txt` |

Dos negativas, ninguna rodeada: el clasificador de Claude Code negó un `grep -rn` sobre `knowledge/`
y `docs/validation/` buscando umbrales de kappa (recursivo sobre una carpeta que contiene el
holdout; con razón), y lo rehíce con Grep limitado a `docs/adr/` y al primer nivel de
`docs/validation/`; la guardia negó un `git ls-files | grep` y un bucle `for`, que rehíce con rutas
literales. El subagente del barrido de 0.1 dice que un primer Grep suyo devolvió dos líneas de
`docs/validation/anexos/` (de `A-16-proveedor-de-datos…md` y de `METODO-FIDELIDAD-RENTABILIDAD/README.md`)
y que no las usó ni abrió esos ficheros; ninguno está en `.claude/hooks/ficheros_con_ocultos.txt`.

Nada de `src/`, `tests/`, `knowledge/` ni `docs/adr/` cambia; `PREREGISTRO.md` sigue con su marca.
Ninguna corrida del arnés, de `motor laminas` ni de `motor decisiones`; nada de `data/`. Ningún
fichero de `knowledge/cases/holdout/**`. Ninguna fecha de un día reservado en lo commiteado.

---

## 0.1 Las herencias

Búsqueda de los diez términos del encargo en la Next Action, los pendientes heredados (texto entero
en `docs/state/HISTORIA.md`), Technical Debt, la hoja de ruta (R5.1 a R5.6) y los 92 informes de
primer nivel de `docs/validation/` tocados desde el 2026-10-01 (`git log --since=2026-10-01
--name-only -- 'docs/validation/*.md'`, sin `anexos/`). El barrido de los informes lo hizo un
subagente de solo lectura; tres de sus citas las comprobé yo (`SEPTIEMBRE-ENTRA.md:32-33`,
`SESGO-H4-COLOR.md:665-673`, `METODO-FIDELIDAD-RENTABILIDAD.md:543-551`). Columna «la cubre»: el
punto de este informe que la trata.

| Herencia | Fichero:línea | Qué pide a esta rama (o a G) | La cubre |
|---|---|---|---|
| La G | `PROJECT_STATE.md:34` | rellenar PREREGISTRO con lo de ADR-0092 §13; antes, el consultor fija cuántos días reservados y si se pide otro mes; condiciones previas de Technical Debt y A-16; cambiar `test_puerta_holdout` en el mismo commit; MASTER_PLAN §H y la fila de F30; holdout-3 y fidelidad-1 con días retirados; S-14 al elegir libros | 0.2 d, 0.3, 0.6, 0.7, 0.8 |
| R5.1 | `docs/plan/HOJA-DE-RUTA.md:418-430` | métrica, umbral, partición, autorización; «una pregunta abre N particiones» (rama de código); qué conjunto es el universo; A-56; A-16; S-14. «Hecho cuando: PREREGISTRO relleno y commiteado, y la puerta abre una sola partición» | 0.2 c, 0.3, 0.6 |
| R5.2 · Mayo | `HOJA-DE-RUTA.md:432-440` | medir mayo cuando la corrida llegue al umbral de ADR-0070 | 0.5 (no es de esta rama) |
| R5.5 · F26 y F27 | `HOJA-DE-RUTA.md:462-467` | F26 y F27 con su cifra contra el umbral pre-registrado; depende de R5.1, R5.2 y R5.3 | 0.5, 0.6 d |
| R5.6 · Rentabilidad | `HOJA-DE-RUTA.md:469-481` | «la spec sellada en PREREGISTRO (G)»; heredados 7, 9 y 10; calendario de cierres; F17 | 0.7 |
| Heredado 6 (febrero) | `HISTORIA.md:696` | febrero no se toca ni se descarga: rama propia y declaración | 0.3 |
| Heredado 7 (junio) | `HISTORIA.md:698` | la guardia de `stable/F14-cobertura` saca junio del universo de un paquete ciego; el reparto de la sesión 1 tiene once días de junio reservados | 0.3, 0.7 (R5.6 lo nombra por junio de 2025) |
| Heredado 9 (re-descargar) | `HISTORIA.md:701` | re-descargar un mes rompe `kit build`; R5.6 lo nombra por los manifiestos de 2025 | 0.7 (de la rama de la medida) |
| Heredado 10 (demo, F17) | `HISTORIA.md:702` | el grabador de spread y ticks; F17 da el deslizamiento | 0.7 (§4) |
| TD «F26 lee 3,00/3,75» | `PROJECT_STATE.md:128` | A-56, medida o declarada conocida | 0.6 a |
| TD «dos días sin partición» | `PROJECT_STATE.md:132` (entera, `HISTORIA.md:569`) | F26 tiene que saberlo | 0.3 |
| TD «una pregunta abre N particiones» | `PROJECT_STATE.md:133` (entera, `HISTORIA.md:570`) | bloqueante antes de la primera autorización; el arreglo es rama propia | 0.2 c |
| TD «fallback de `leer_fichero`» | `PROJECT_STATE.md:134` (entera, `HISTORIA.md:571`) | juzga una carpeta desconocida bajo `holdout-1`; entra el día que tenga llamante | «Lo que el encargo no preguntó» |
| TD «lector guardado por camino» | `PROJECT_STATE.md:130` (entera, `HISTORIA.md:567`) | el día que un camino guarde material reservado en `knowledge/cases/<camino>/`, lector guardado antes | «Lo que el encargo no preguntó» |
| TD «no_trade por ausencia» y S-14 | `PROJECT_STATE.md:126` | sin decidir; S-14 | 0.6 c |
| TD «M1 de marzo en cada `make check`» | `PROJECT_STATE.md:102`, `:105`, `:107` | se declara cada día | Exposiciones |
| `ACTIVAR-SESION-05.md:1146-1148` | | R5.1: al elegir libros, los sin vídeo omiten las sesiones de break even | 0.6 c |
| `CASES-REJILLA.md:772` | | G: el consultor fija antes cuántos días y si se pide otro mes | Decisiones |
| `CORRIDA-CONSTRUCCION.md:1790`; `SESGO-H4-COLOR.md:1287-1324` | | holdout-3 y fidelidad-1 con días retirados: F26 lo tiene en cuenta | 0.3 |
| `SESGO-H4-COLOR.md:665-673` | | el sesgo del trader en directo sobre velas de `fidelidad-1` (v6 1:03:48-1:05:35): «lo que eso vale para la fidelidad lo decide F26 al rellenar el PREREGISTRO» | 0.3, decisiones |
| `SEPTIEMBRE-ENTRA.md:32-33` | | «F26 excluye en bloque los días sin operaciones» del rango de septiembre, por anticipado | 0.3, decisiones |
| `METODO-FIDELIDAD-RENTABILIDAD.md:348`, `:1061-1074`, `:1269` | | la NOTA de PREREGISTRO (borrador) y la línea de G; no aflojar `test_puerta_holdout` | 0.8, 0.2 d |
| `METODO-FIDELIDAD-RENTABILIDAD.md:543-551` | | si la rentabilidad se midiera en reservados iría por la puerta en la misma apertura que F26 (descartado: se mide sobre 2025) | 0.7 |
| `PLATAFORMA-ADELANTADA.md:39-41`; `CAPA-GENERADA.md:364` | | la parte de estrategia de la capa (RN-032, hash de la spec) espera a F26 | 0.7 (hash) |
| `FILTRADAS-ESCENARIO-B.md:804` | | F26 cita dos filas de exposición | 0.3 |
| `BARRIDO-SESION-5.md:85` | | A-16 y A-56 se miden, no se preguntan | 0.6 |
| `PUERTA-POR-PREGUNTA.md:169-216` (anterior al 2026-10-01; lo trajo el auditor) | | «una pregunta abre N» bloqueante y rama propia; `kit kappa --incluir-holdout` sin etiquetas gasta la pregunta sin abrir nada; «la primera autorización real será `fidelidad-1`» | 0.2 c, decisiones |

---

## 0.2 La puerta, tal como es hoy

**Los ADR que la sostienen, y los que no pintan.** Pintan: ADR-0021 (qué es abrir, §1; quién
autoriza y con qué, §3: «`PREREGISTRO.md` commiteado ANTES con los umbrales, mas un ADR que diga que
se midio y contra que umbral»; §6: `holdout-1` para la nota de F26, `holdout-2` para corregir,
`holdout-3` para la fase final; §7: pedir un mes no tocado), ADR-0033 (la puerta y su enmienda del
2026-09-21), ADR-0025 (el reparto de mayo no se toca), ADR-0034 y ADR-0036 (septiembre, el camino
de fidelidad y sus nombres de partición), ADR-0035 (los dos días fuera del paquete), ADR-0037 (la
granularidad por día), ADR-0041 (los retirados), ADR-0043, ADR-0047 (la unidad es la operación
también en el holdout), ADR-0046 (marzo), ADR-0072 (quién lee la columna de fechas). Añado:
ADR-0070 y ADR-0092 (umbral de construcción y papel de F26), ADR-0040 y ADR-0073 (A-56). No pintan
en la puerta: ADR-0042 (el reparto dev-visto no tiene particiones reservadas; la puerta solo recorre
sus repartos, `holdout.py:61-63`) y ADR-0088 (cómo se cuentan los nombres de dentro del holdout: es
de la guardia de la sesión, no de la puerta).

**(a) Qué forma tiene que tener `PREREGISTRO.md` para que la puerta lo dé por relleno, y qué no lee.**
Lo único que la puerta lee del fichero (`motivos_de_cierre`, `holdout.py:151-232`):
1. que esté commiteado y sea igual en el árbol que en `HEAD` (`_commiteado_y_sin_cambios`,
   `:124-134`; normaliza BOM y CRLF);
2. que la cadena `SIN RELLENAR` no aparezca **en ninguna parte** del fichero (`:159-165`, por
   subcadena: quitarla también de los comentarios);
3. las líneas de pregunta, por la expresión `_PREGUNTA` (`:88-91`): `- pregunta: <id> | estado:
   <estado>`, con el id empezando por letra o dígito; lo que siga tras el estado es libre. Se busca
   en **todo** el texto (`preguntas_del_preregistro`, `:137-148`, `finditer` con `MULTILINE`): el
   encabezado `## Preguntas` lo dice el docstring (`:140`), pero **el código no lo exige**. La
   pregunta que cita la autorización tiene que existir y estar exactamente `ABIERTA` (`:220-231`).

**No lee nada más**: ni `umbral:`, ni la métrica, ni la partición, ni las exposiciones, ni a qué
partición va cada pregunta. Medido en los propios tests: `RELLENO` lleva `umbral: 0.8` y ningún
código lo lee (`test_puerta_holdout.py:145-148`), y el test que lo cambia a 0.6 solo cierra la
puerta por el blob (`:214-230`). **Las cifras del fichero las protege solo el `preregistro_blob`**,
y con una consecuencia declarada: si se cambian y se devuelven byte a byte, la puerta vuelve a abrir
(`holdout.py:33-35`). De la autorización tampoco lee el ADR: solo que exista un fichero
`docs/adr/<NNNN>-*.md` (`:195-197`); su contenido -«qué se midió y contra qué umbral», ADR-0021 §3-
no lo comprueba nadie.

**(b) Qué ata la autorización a la versión del fichero.** `AUTORIZACION-<particion>.md`, commiteada
y sin cambios en el árbol (`:166-170`), con seis campos sin repetir (`:77-84`, `:171-190`):
`particion` (tiene que ser la que se abre), `autorizado_por`, `fecha` (AAAA-MM-DD), `adr` (que
exista), `pregunta` y `preregistro_blob`, que tiene que ser `git rev-parse HEAD:docs/validation/PREREGISTRO.md`
(`:198-214`). Consecuencias, medidas en los tests:
- **cualquier** cambio del fichero, commiteado o no, cierra todas las autorizaciones de todas las
  particiones (`test_una_autorizacion_sin_commitear_no_autoriza`, `:200-211`;
  `test_cambiar_el_preregistro_despues_de_autorizar_cierra_la_puerta`, `:214-230`); hace falta una
  autorización nueva con el blob nuevo;
- **gastar una pregunta es un cambio del fichero** (`gastar_pregunta`, `holdout.py:269-301`): tras la
  primera apertura, toda autorización anterior -también las de otras particiones y otras preguntas-
  deja de valer (`test_una_pregunta_gastada_no_se_vuelve_a_abrir`, `:273-304`);
- y por lo mismo: **escribir algo después en `PREREGISTRO.md`** (el hash de la spec, una NOTA, una
  pregunta nueva) invalida las autorizaciones ya dadas. Pesa en la decisión 5.

**(c) «Una pregunta abre N particiones».** El único bucle está en `kappa_entre_sesiones`
(`src/botsito/cases/paquete.py:1364-1373`): cuenta las particiones reservadas con etiqueta en las
dos rondas (`por_particion`), llama a `abrir` para **cada una** con la misma pregunta y gasta la
pregunta **una vez**. Lo que permite hoy: contestar una pregunta exige firmar toda partición
reservada con etiqueta en esas rondas, o el comando falla entero sin gastar
(`test_una_pregunta_abre_todas_las_particiones_con_etiqueta`, `test_puerta_holdout.py:373-432`); y
una autorización de cada partición que cite la misma pregunta abre las N a la vez. La puerta no ata
la pregunta a una partición: en el pre-registro la línea de pregunta no lleva partición, y en la
autorización la pregunta y la partición son campos independientes. Dos datos más, de
`PUERTA-POR-PREGUNTA.md:198-203`: hoy no hay ningún `LABEL_CASE`, así que `kit kappa
--incluir-holdout --pregunta P1` **gasta P1 sin abrir nada**; y `leer_fichero` no tiene llamante de
producción: la puerta protege hoy un solo comando, `kit kappa --incluir-holdout`.

El cambio mínimo, **descrito y no hecho**:
1. `kappa_entre_sesiones` recibe la partición que se abre (y la CLI una opción `--particion`,
   obligatoria con `--incluir-holdout`); llama a `abrir` solo para ella, y los casos de las demás
   particiones siguen en `excluir` (`excluir = (etiquetados - casos de esa partición) |
   (etiquetados & retirados)`); gasta la pregunta una vez, como hoy;
2. opcional, para cerrar el espejo desde el pre-registro: la línea de pregunta lleva su partición
   (`- pregunta: P1 | estado: ABIERTA | particion: holdout-1 | ...`) y `motivos_de_cierre` exige que
   la `particion` de la autorización sea la de la pregunta.
Tests que romperían: `test_una_pregunta_abre_todas_las_particiones_con_etiqueta`
(`test_puerta_holdout.py:373`), que hoy exige el fallo nombrando `AUTORIZACION-holdout-1.md` y
pasaría a tener que exigir que se abre solo `holdout-2` y que la etiqueta de `holdout-1` sigue sin
leerse; y `test_kappa_desde_registros_y_cli` (`tests/unit/test_kit.py`, con `_autorizar` en
`:703-735` firmando las tres particiones con P1 y esperando `unidades: 10` en `:815-817`). Con el
punto 2, además, `RELLENO`/`BUENA` de `test_puerta_holdout.py:145-152` y `RELLENO` de
`test_retirados.py:51`. Las cadenas de comando de `test_revisor.py:187` y `:224` no rompen (solo
clasifican la orden).

**(d) El test que cambia en el commit que quite la marca, y su sustituto.**
`test_con_el_preregistro_de_hoy_la_puerta_se_niega_y_nombra_adr_0021`
(`test_puerta_holdout.py:34-40`, parametrizado sobre las seis `RESERVADAS`) afirma tres cosas: la
marca está en el fichero (`:36`), la puerta se niega con «ADR-0021 §3» y el motivo contiene «sigue
vacio» (`:39`) y nombra `AUTORIZACION-<p>.md` (`:40`). Dos roturas, no una:
- quitar la marca rompe `:36` y `:39`;
- **y antes, cualquier edición del fichero** rompe `:39` en el `make check` que sella el commit: con
  el fichero estadiado y sin commitear, el motivo pasa a ser «no esta commiteado tal como esta en el
  arbol» y no «sigue vacio». Es lo que paró la NOTA en la PARADA 2 de
  `METODO-FIDELIDAD-RENTABILIDAD.md` (`:1061`); vale para el segundo tiempo de esta rama aunque la
  marca se quedara.
Sustituto que propongo describir en el segundo tiempo (no escrito): para cada reservada, la puerta
se niega con «ADR-0021 §3» y nombrando `AUTORIZACION-<p>.md` (cierto commiteado o no, mientras no
haya autorizaciones), más dos afirmaciones que no dependen del estado de git: que no existe ningún
`docs/validation/AUTORIZACION-*.md` en el repo real, y que `preguntas_del_preregistro` del fichero
real da solo estados `ABIERTA` o `GASTADA`. La marca deja de ser una de las barreras; quedan la
autorización por partición y la pregunta `ABIERTA`. `test_kit.py:806-811` (repo sintético) y
`test_retirados.py` no dependen del fichero real.

---

## 0.3 Las particiones

**Recuento** (`recuento_particiones.py`, salida en el anexo; ninguna clave impresa):

| Partición | Reparto | Días | Retirados | de ellos, `retirado_el` antes del 2026-10-17 | Medibles por `casos_medidos` | Filas de HOLDOUT-EXPOSICIONES que la nombran | Declaradas los días |
|---|---|---|---|---|---|---|---|
| holdout-1 | `kit/2026-09-09-sesion-01` | 8 | 0 | 0 | 8 | 15 | 2026-09-11, -12, -13, -22; 2026-10-04, -10, -14, -17, -18, -27 |
| holdout-2 | `kit/2026-09-09-sesion-01` | 8 | 0 | 0 | 8 | 16 | las mismas diez fechas, más 2026-11-19 (la fila de esta rama, que nombra el día quemado; no es una exposición nueva) |
| holdout-3 | `kit/2026-09-09-sesion-01` | 8 | 1 | 1 | 7 | 19 | las mismas, más 2026-11-08 |
| fidelidad-1 | `fidelidad/eurusd-2026-09` | 10 | 4 | 1 | 6 | 4 | 2026-09-23; 2026-10-04, -10, -17 |
| fidelidad-2 | — | 0 | 0 | 0 | 0 | 0 | — |
| fidelidad-3 | — | 0 | 0 | 0 | 0 | 0 | — |
| **total** | | **34** | **5** | **2** | **29** | | |

Además, 15 filas nombran «holdout» sin partición (entre el 2026-09-20 y el 2026-11-14), y la tabla
tiene 149 filas en total (`exposiciones-por-particion.txt`, sacada con la fila de esta rama ya
ampliada). Las fechas de retirada: una del 2026-09-23, una del 2026-10-14 y tres del
2026-10-17 (`retirados.yaml:11-13` lo dice igual). Los repartos de los cuatro meses de construcción
(`visto/2026-01`, `-04`, `-07`, `-08`) solo tienen `dev` (21, 21, 13 y 21).

Lo que el recuento NO dice, y pesa más que el recuento:
- **La Next Action se queda corta con `fidelidad-1`**: dice «3 días medidos menos desde el
  2026-10-17» (`PROJECT_STATE.md:34`) y son 4 retirados, uno de ellos del 2026-09-23 (el día de v6):
  medibles 6 de 10, no 7. La cabecera de `retirados.yaml:11-13` ya decía 6.
- **El día quemado de `holdout-2` no está en `retirados.yaml`**: `HOLDOUT-EXPOSICIONES.md:176-180`
  (obligación 4) dice que F26 lo excluye y que `holdout-2` «se queda en 3 dias medibles», pero
  `casos_medidos` lo cuenta como medible (0 retirados en `holdout-2`). La exclusión vive solo en
  prosa.
- **Los 24 días de `holdout-1/2/3` son de mayo y de junio de 2026** (`recuento-compuerta.txt` de
  METODO-FIDELIDAD-RENTABILIDAD §1.3: los 34 reservados están en 2026-05, 2026-06 y 2026-09). Junio
  quedó descartado como material el 2026-09-12 (`PREREGISTRO.md:28-29`; heredado 7, once días de
  junio reservados): **los días de junio no tienen operaciones del trader**, y la ingesta no ingiere
  un día de un mes sin `cobertura_material` (`cases/ingesta.py:24-29`). Los de mayo, por partición,
  son 6, 4 y 3 según `PREREGISTRO.md:28` y la fila del 2026-09-11 de HOLDOUT-EXPOSICIONES. Partir
  los medibles por mes exige leer el mes de la clave: no lo saqué (el encargo lo limita a contar
  valores) y va a la PARADA (decisión 2). Con lo escrito: `holdout-2` con material, 3 (4 menos el
  quemado); `holdout-3`, 3 o 2 según de qué mes sea el retirado del 2026-10-14, que no sé.
- **Septiembre no es ciego** (ADR-0034) y el trader dio su sesgo en directo sobre velas de días de
  `fidelidad-1` (`SESGO-H4-COLOR.md:665-673`); y «F26 excluye en bloque los días sin operaciones» de
  septiembre (`SEPTIEMBRE-ENTRA.md:32-33`).

**Los dos días del universo de la sesión 1 fuera de toda partición.** Recuento: **2** (universo 42,
paquete 40, porque los cupos suman 40). Fuente: `docs/validation/UNIVERSO-CONGELADO.md:32-60` (§2b)
y ADR-0035 «Impacto» (`docs/adr/0035-*.md:104-110`; ese párrafo escribe las fechas y no se copian).
No son `dev` ni holdout, «no queman ni protegen nada» y «no sirven para medir fidelidad contra un
reparto ciego» (UNIVERSO-CONGELADO.md §2b). **Lo que el ADR deja decidir**: sobre qué conjunto se da
cada cifra («un kappa sobre el universo y uno sobre el paquete no son el mismo conjunto»: toda cifra
dice sobre cuál), y que si algún día se etiquetaran habría que fijarlos antes en un paquete.

**El material fuera de construcción, por mes, sin abrir nada:**

| Mes | Qué hay | Estado | Por dónde entraría |
|---|---|---|---|
| Febrero 2026 | nada recibido | el mes limpio pedido al trader, «ciego, sin descargar y sin reparto»; reservado entero (`meses_reservados.yaml:29-35`); heredado 6 | rama propia y declaración (`HISTORIA.md:696`); no hay runbook |
| Marzo 2026 | xlsx y 7 imágenes, sin vídeo (`REGISTRO-MARZO.md` §1) | recibido el 2026-09-30, SIN ABRIR; reservado entero (`meses_reservados.yaml:36-41`, cuyo motivo aún dice «hasta que A-42 este resuelta»: está resuelta, ADR-0069, y el fichero es solo-añadir); no está en `vistos.yaml` (solo 01, 04, 05, 07, 08 y 09) | `docs/runbooks/ENTRADA-MARZO.md`: falta el paso 0 (marzo en `vistos.yaml`), el paso a (fechas, Aleks) y el sorteo; cupos por regla: 1/3 a `fidelidad-dev` y el resto a `fidelidad-2` y `fidelidad-3` (`knowledge/cases/fidelidad/config.yaml:102-107`; ADR-0046 §3); el paso b2 retira los días vistos en v13 |
| Mayo 2026 | xlsx, 7 capturas de Analytics y 2 de WhatsApp, sin vídeo (`fuentes.yaml:288-295`); `libros.yaml:41` | 6 `dev` y 13 reservados (6/4/3) más los de junio en las mismas particiones; el «conjunto de medida» de ADR-0043 son sus días `dev` | `kit/2026-09-09-sesion-01`; la medida, por R5.2 (ADR-0070) |
| Septiembre 2026 | xlsx y 6 capturas (ADR-0034:38), sin vídeo; **no está en `libros.yaml`** | sorteado (4 `fidelidad-dev`, 10 `fidelidad-1`); el libro no se puede leer sin su entrada (CLAUDE.md, ADR-0039) | camino de fidelidad (ADR-0036); falta declarar el libro |
| Octubre y noviembre 2026 | un vídeo de mapeo (2026-10-23 a 2026-11-17 según el trader) | SIN ABRIR, fuera del repo, no se ingiere; reservados enteros (`meses_reservados.yaml:49-64`) | ninguno escrito |
| Diciembre 2025 | xlsx y capturas de Analytics, sin vídeo | SIN ABRIR, fuera del repo; reservado entero hasta que el consultor decida (`meses_reservados.yaml:42-48`; NA:I) | R5.4; antes, `RENOVAR-CIERRES.md` condición 1; si va a construcción, la salida de `meses_reservados.yaml` con su ADR (hoy no existe) |

---

## 0.4 La densidad, solo sobre construcción

De `anexos/RECORRIDA-CONSTRUCCION-2/cuenta-por-mes.txt` (la línea base vigente, ADR-0070 NOTA del
2026-11-08), sección «## Por sesion» sumada por día y «Resumen por mes» para los días corridos
(`densidad_construccion.py`; el guion comprueba que la suma de cada mes da el total del resumen):

| Mes | Días dev | Operaciones del trader | Días con alguna | Media por día | Mediana | Mín | Máx |
|---|---|---|---|---|---|---|---|
| 2026-01 | 21 | 54 | 21 | 2,57 | 2 | 1 | 7 |
| 2026-04 | 21 | 35 | 16 | 1,67 | 2 | 0 | 5 |
| 2026-07 | 13 | 67 | 13 | 5,15 | 5 | 2 | 11 |
| 2026-08 | 21 | 42 | 19 | 2,00 | 2 | 0 | 6 |
| **total** | **76** | **198** | **69** | **2,61** | **2** | **0** | **11** |

Ningún día reservado entra. Julio, el único con vídeo según el trader, tiene el doble de
operaciones por día que los otros tres (S-14: los libros sin vídeo omiten sesiones; 0.6 c). El
mínimo de potencia escrito para F26 son «36 unidades efectivas independientes»
(`AUDITORIA-2026-09-13-ultracode.md` §6.1, citado en `cases/fidelidad.py:18-24` y ADR-0036 §8), que
«nada construible hoy lo alcanza»; esa cifra se escribió para unidades de etiqueta, no para
operaciones, y no la traduzco.

---

## 0.5 La métrica de F26, tal como está escrita hoy

- **Unidad y emparejamiento** (ADR-0043:14-26): la operación dentro de su día y su sesión; uno a uno
  si coinciden día, sesión y dirección, |Δentrada| ≤ 3 puntos y |Δinstante de llenado| ≤ 15 min;
  desempate por menor |Δinstante|, menor |Δentrada| y la más temprana, voraz y global (`:78-79`).
- **Métricas**: cobertura = trader emparejadas / trader; precisión = bot emparejadas / bot, solo en
  días con alguna del trader; las del bot en días sin trader se informan aparte (ADR-0016); sin
  denominador, sin definir (`:80`).
- **Tolerancias** (`criterio_fidelidad.yaml:14-22`): `tolerancia_entrada_puntos: 3`,
  `tolerancia_instante_min: 15`, `tolerancia_stop_puntos: 3` (solo la fidelidad por criterios),
  `escala_puntos: 100000`.
- **`umbral_cobertura: "0.70"`, `umbral_precision: "0.60"`** (`:24-25`), «sobre el conjunto de
  MEDIDA». **ADR-0043:55-56: «Umbral de desarrollo: cobertura ≥ 70 % y precisión ≥ 60 % sobre el
  conjunto de medida. Esto NO es el PREREGISTRO del holdout.»** La cabecera del yaml (`:10`) lo
  repite. `medida: ["2026-05"]` (`:48`): son los días **`dev`** de mayo (y la parte `fidelidad-dev`
  de marzo, ADR-0043:49-52), no los reservados.
- **Fuera del criterio**: stop (solo en la fidelidad por criterios), **TP, resultado y gestión**
  (ADR-0043:34-40 con el recuadro de ADR-0092).
- **«Cambios»** (ADR-0043:59-61): no se modifica tras la primera salida del motor sobre la medida
  salvo con un ADR que declare quemado lo visto; **NOTA de ADR-0092** (`:63-69`): esa salida no se
  ha producido, ADR-0092 enmienda sin quemar mayo, y lo que obliga a declarar lo visto de
  construcción es ADR-0070 punto 4 (declarado en ADR-0092 §12).
- **ADR-0070**: mayo se mide solo cuando UNA corrida de `motor arnes` sobre toda la construcción,
  con `--simular`, perfil `ftmo-2step-swing-100k` y su primera fase, solo con opciones de la lista
  cerrada y una cuenta por mes, dé cobertura ≥ 0,70 y precisión ≥ 0,60 a la vez (`:44-70`, `:115-122`);
  el arnés lo escribe en la línea «habilita medir…» (`:151-160`). No se construye ningún comando de
  medida (`:161-163`). **La última re-corrida que cuenta**: `RECORRIDA-CONSTRUCCION-2.md:420` y su
  anexo `cuenta-por-mes.txt:13`: `habilita medir el conjunto de medida (2026-05) (ADR-0070): no
  (cobertura 15.7 % por debajo de 70.0 %; precision 13.9 % por debajo de 60.0 %)`. Es la más reciente
  que la publica con cifra propia; la repiten ADR-0070:124-128 y la citan `ACTIVAR-SESION-07.md:684`,
  `SESION-07-EXTRACCION.md:881` y `TRAZAS-ABLACION.md:973`.
- **ADR-0092**: §1 (`:26-45`) la fidelidad por operación y por criterios es la herramienta de
  construcción, la de criterios **sin umbral de paso**; §2 la cascada; §7 (`:180-201`) **F26 «deja
  de ser la condición necesaria para operar en vivo y queda como diagnóstico que se informa en el
  memorando»**, y sus condiciones previas (3,00/3,75 y los dos días) siguen siendo de cualquier
  métrica sobre reservados; F27 (DSR, N de pruebas) no se sustituye y F35 depende de ella; F35 es la
  decisión de Aleks y la puerta de §3 es condición necesaria, no la decisión; §9 (`:233-239`) las
  tolerancias quedan y la regla de A-16 (0.6 b).

---

## 0.6 Las condiciones previas que nombra la G

**(a) A-56 y 3,00/3,75.** `knowledge/spec/ambiguedades.yaml:1911-1950`: ABIERTA, clase medición,
no bloqueante, `resuelve_en: [F26]`, sin evidencia (fuentes documentales a ADR-0040). **Solo
declarada conocida, no medida**: «F26 lee la diferencia como conocida» (`:1926`; ADR-0073 §4,
`:62-68`; ADR-0040 «Impacto», `:124-129`); lo que la resolvería es «un material que traiga la caja»
y el libro de agosto con vídeo (NA:Q). **Cómo puntuaría F26 el objetivo: hoy no lo puntúa en ningún
caso.** El criterio por operación deja fuera TP y resultado (ADR-0043:34-40), y la fidelidad por
criterios no tiene la caja como pieza precisamente para no arrastrar A-56 (ADR-0092 §1, `:36-39`).
A-56 solo pesaría si el pre-registro añadiera el objetivo como pieza: con la diferencia «conocida»,
una pieza de objetivo sobre el material del trader daría por construcción una distancia de hasta
0,75 R entre lo que dice la regla y lo que mide el libro.

**(b) A-16.** Medida en R3.7 (`METODO-FIDELIDAD-RENTABILIDAD.md:858-909`, §1.3): 198 operaciones,
mediana M1 0 puntos, p90 0, 92,4 % dentro del rango de la M1, 8 sin ticks. Regla de ADR-0092 §9
(mediana > 3 puntos o proporción < 50 %): veredicto literal «**no se dispara**. No nace ninguna
línea de Technical Debt por ella, y la tolerancia no cambia» (`:882-884`). A-16 sigue ABIERTA,
`resuelve_en: [F26]` (`ambiguedades.yaml:313-331`): la medida no compara vela con vela ni la ruptura
por una milésima (`:889-893`).

**(c) El material sin vídeo.** El bloque `material_sin_video` (`criterio_fidelidad.yaml:55-65`) solo
cubre construcción (enero, abril salvo el 29, agosto; julio provisional con vídeo). Para lo
reservado, sin abrir nada: **mayo, septiembre y marzo llegaron como xlsx más capturas, ninguno
grabado en vídeo** (`ACTIVAR-SESION-05.md:298`: «Mayo 2026 | No»; ADR-0034:38 para septiembre;
`REGISTRO-MARZO.md` §1 para marzo); diciembre de 2025, sin vídeo (NA:I). Por S-14 (`ev-v15-011912-0ae32588`,
`ev-v16-003421-b824b770`), en los backtests sin vídeo el trader se saltaba las sesiones que iban a
acabar en break even: **todo el material reservado que existe tiene ese sesgo**, y la cobertura que
F26 midiera sobre él lo arrastra. Octubre y noviembre traen un vídeo de mapeo, no un backtest.

**(d) Lo que MASTER_PLAN §H pide además** (`MASTER_PLAN.md:229`): «`PREREGISTRO.md` con umbrales de
fidelidad, kappa, paridad y DSR, commiteado antes de abrir cualquier holdout; los informes citan su
hash | F26, F27, F32, F35». Ningún ADR fija ni retira ninguno de los tres: kappa sin cifra en ningún
ADR (búsqueda en `docs/adr/`; `AUDITORIA-2026-09-13-ultracode.md:1598` y `:1622` lo pedían «con su
N»); DSR, solo nombrado en ADR-0092 §7 (`:193-194`) para F27; paridad, sin umbral en ningún ADR (la
fila de F32, `MASTER_PLAN.md:134`, dice «> 95 % operaciones» y la de F30, `:132`, «100 % decisiones
iguales», como criterio de la fila, no pre-registrado). Kappa mide la consistencia del trader entre
rondas (sesión 2, `MASTER_PLAN.md:208`), no se ha celebrado ninguna ronda con etiquetas
(`PUERTA-POR-PREGUNTA.md:198`); la paridad (F30, F32) y el DSR (F27) no abren ningún holdout de
fidelidad. **De quién**: lo leo como de cada funcionalidad, pero la fila de §H dice «antes de abrir
cualquier holdout»: decisión 7.

**(e) Otras condiciones de 0.1.** El comando que mida F26 no existe (0.2 c y «Lo que el encargo no
preguntó»); el día quemado de `holdout-2` fuera de `retirados.yaml` y los días de junio sin material
(0.3); el sesgo del trader en directo sobre `fidelidad-1` (0.3); y `PUERTA-POR-PREGUNTA.md:216`, que
da `fidelidad-1` como primera autorización, frente a MASTER_PLAN:127 y `PREREGISTRO.md:15`, que dan
`holdout-1` (decisión 1).

---

## 0.7 La rentabilidad: lo que ADR-0092 §13 manda llevar a PREREGISTRO.md

ADR-0092 §13 (`:323-326`). **La rentabilidad no lee reservados ni material del trader** (§7,
`:191-192`; se mide sobre junio a noviembre de 2025): no pasa por la puerta y su pre-registro no
protege ningún holdout; protege contra ajustar la spec a la cifra (§6).

| Pieza | Dónde vive ya | ¿Se fija hoy? |
|---|---|---|
| Métrica y cálculo (§3): R neto por operación llenada, comisión del perfil y swaps entre riesgo al colocar; criterios a) a f); «insuficiente» si no a); remuestreo por días con su forma (PARADA 2, punto 2) | ADR-0092:66-97; funciones puras en `cases/criterio_fidelidad.py` | Sí: se copia |
| Umbrales | `criterio_fidelidad.yaml:66-80` (`n_minimo`, `esperanza_minima_r`, `percentil_remuestreo`, `replicas_remuestreo`, `semilla_remuestreo`, `perdida_diaria_max`, `perdida_total_max`) | Sí: se copian |
| Meses, extensión y por qué | yaml `:84-85`; ADR-0092 §5 `:117-158` | Sí |
| Fase | yaml `:68` (`fondeada`); §5 | Sí |
| Deslizamiento (§4) | yaml `:82-83` (`pendiente_F17`, percentil 90); ADR-0092:99-115; «la puerta no puede dar "pasa" antes de F17» | Sí, la regla; la cifra la da F17 |
| Qué se hace si no pasa | §5 `:155-158`, §6; `vistos_rentabilidad: []` (yaml `:86`) | Sí |
| Hash de la spec sellada y sha de `src/` | §5 `:142-144`: «el hash de `strategy_spec.yaml`, `parametros.yaml`, el perfil de `knowledge/cuentas/` y `knowledge/simulador/llenado.yaml`, y el sha de `src/`, en `PREREGISTRO.md`, que rellena G» | **No hoy** (abajo) |

**El hash de la spec.** No existe ningún comando ni función que calcule el conjunto de §5. Lo que
existe: `spec/manifiesto.hash_de` (`src/botsito/spec/manifiesto.py:168-172`) y `botsito spec
manifest` (`cli.py:869`, `:3465`), un hash CANÓNICO (estructura re-serializada, no bytes) sobre
`parametros.yaml`, `strategy_spec.yaml` y `glossary.yaml` (`knowledge/spec/spec_manifest.yaml:14-17`,
`spec_version` 19.0.5): incluye el glosario, que §5 no nombra, y **no incluye ni el perfil ni
`llenado.yaml`**. §5 no dice si el hash es de bytes o canónico, ni cómo se compone el de cuatro
ficheros, ni si el sha de `src/` es el de un árbol (`git rev-parse HEAD:src`) o el de un commit.
**Un hash escrito hoy caduca** con la activación de la 7b (cambia `knowledge/spec/`, NA:F paso 2) y
con cada rama de construcción hasta que la corrida dé «habilita medir: sí» (§5 `:154`). Y escribirlo
más tarde en `PREREGISTRO.md` cambia su blob (0.2 b): cualquier autorización de holdout dada antes
caduca con él. De ahí la decisión 5.

**Si el pivote de la sesión 7 pasara a un bot de alta precisión** (solo con lo escrito; la lectura
no está hecha, ADR-0093 §6): seguirían valiendo la puerta y su mecanismo, las particiones y sus
recuentos, las exposiciones, los retirados, la regla «medir una vez», la rentabilidad de ADR-0092
entera (no depende de cómo se construya el bot: mide R neto del bot sobre meses no vistos), y la
unidad «operación» si el bot sigue colocando las mismas órdenes. Habría que rehacer: la métrica de
F26 en lo que la ate a reproducir al trader -con un bot que opera menos, la **cobertura** de
ADR-0043 deja de medir lo que se quiere y la **precisión** pasa a ser la cifra que importa-, el
umbral de construcción de ADR-0070 (exige las dos a la vez), y el reparto de pesos entre fidelidad
y rentabilidad que fija ADR-0092 §1 y §7. Eso no se precisa aquí: el pivote no es de esta rama.

---

## 0.8 Los textos que el segundo tiempo tendrá que tocar

**El borrador de la NOTA** (`METODO-FIDELIDAD-RENTABILIDAD.md:1066-1074`), tal cual:

> **NOTA de ADR-0092 (2026-11-07, `trabajo/metodo-fidelidad-rentabilidad`; no rellena nada: este
> fichero sigue SIN RELLENAR).** Desde ADR-0092 la condicion necesaria para operar en vivo es la
> RENTABILIDAD pre-registrada (ADR-0092 §3), medida una vez sobre meses que el bot no ha visto
> (junio a noviembre de 2025, con su extension, §5); F26 queda como diagnostico. Para la
> rentabilidad, este fichero tendra que llevar (ADR-0092 §13): la metrica y su calculo (el R neto
> por operacion, §3); los umbrales (`criterio_fidelidad.yaml`, bloque `rentabilidad`); los meses, la
> extension y por que esos, y la fase (§5); el hash de la spec sellada y el sha de `src/` (§5); el
> tratamiento del deslizamiento, pendiente de F17 (§4); y que se hace si no pasa
> (`vistos_rentabilidad`, §5). La ampliacion de «Que tiene que llevar» es de G.

Lo que respondió el consultor (`:1269`), tal cual: «0. PREREGISTRO.md: (a). No se toca en esta rama
y test_puerta_holdout no se afloja. Lo que tendrá que llevar ya está en ADR-0092 §13 y en la NOTA de
MASTER_PLAN; tu texto de la NOTA se queda en el informe como borrador para G. Línea para el cierre,
en G de la Next Action: «G rellena PREREGISTRO.md con lo de ADR-0092 §13 (borrador de la NOTA en
METODO-FIDELIDAD-RENTABILIDAD.md, PARADA 2), y en el mismo commit cambia test_puerta_holdout, que ata
ese fichero a HEAD (_commiteado_y_sin_cambios)». Porqué: una guardia del holdout no se afloja para
meter una nota; G tiene que tocar ese test de todos modos.» Ojo: el borrador lleva la cadena «SIN
RELLENAR» en su primera línea; copiado tal cual a un fichero ya relleno, la puerta lo volvería a
dar por vacío (`holdout.py:159`).

**`PREREGISTRO.md`, «Que tiene que llevar» (`:15-24`)** y **«Lo que hay que saber al rellenarlo»
(`:26-33`)**, con lo viejo marcado:

| Línea | Texto | ¿Viejo? |
|---|---|---|
| `:1` | «# PREREGISTRO de umbrales — VACIO: NO SE HA PRE-REGISTRADO NADA» | cambia al rellenar |
| `:3` | «**Estado: SIN RELLENAR. …**» | la marca |
| `:15` | «## Que tiene que llevar, antes de abrir `holdout-1` (F26)» | viejo: la primera apertura puede ser otra partición (`PUERTA-POR-PREGUNTA.md:216`), y desde ADR-0092 el fichero lleva también la rentabilidad, que no abre nada |
| `:17-18` | 1. la métrica exacta «… stop y objetivo con que tolerancia» | en parte: el objetivo no se puntúa (ADR-0043:34-40; 0.6 a) |
| `:19` | 2. el umbral «y que pasa si no se alcanza» | vigente, pero F26 es diagnóstico (ADR-0092 §7): decisión 0 |
| `:20-21` | 3. la partición; 4. quién autoriza | vigentes (quien autoriza: Aleks, ADR-0021 §3; ADR-0072:20 fija los papeles) |
| `:22-23` | 5. las exposiciones «Hoy hay una: la del 2026-09-11» | **viejo**: hoy de 15 a 19 filas por partición de `holdout-*` y 4 de `fidelidad-1` (0.3) |
| `:24` | 6. si falla, `holdout-2` | vigente según ADR-0021 §6, pero `holdout-2` tiene 3 días de mayo medibles (0.3) |
| `:28-29` | «Mayo es el unico material: 19 dias, 6 `dev` y 13 holdout (6/4/3). Junio quedo descartado» | **viejo**: hay septiembre (`fidelidad-1`), marzo recibido, diciembre de 2025, octubre y noviembre; y no dice que en las tres `holdout-*` hay también días de junio sin material |
| `:30-31` | «Trece de esos dias tienen su PnL diario expuesto … F26 lo cita» | vigente, incompleto (más exposiciones; retirados) |
| `:32-33` | «Esta pendiente pedirle al trader un mes que no haya tocado. Si llega antes de F26 …» | vigente: febrero sigue pendiente (heredado 6) |

**MASTER_PLAN.md**:
- §A, F26 (`:127`): «| F26 | `feature/F26-fidelity-validator` | Fidelidad contra el trader (holdout-1; umbrales pre-registrados en `PREREGISTRO.md`; cita la exposicion declarada, ADR-0021) | F10, F14, F24 | comparador; holdout; pre-registro | informe reproducible que cita PREREGISTRO.md |» — vieja en «holdout-1» y en que no dice que es diagnóstico (ADR-0092 §7).
- §A, F30 (`:132`): «| F30 | `feature/F30-differential-testing` | Harness Python ↔ MQL5 | F29, F26 | harness | 100 % decisiones iguales |» — la G pide tocarla «con la rentabilidad» (`PROJECT_STATE.md:34`): depende de F26, y desde ADR-0092 lo que precede a F29-F30 es la rentabilidad (Regla viva, `PROJECT_STATE.md:169`).
- §H, el pre-registro (`:229`): citada en 0.6 d.
- Además (auditor): el principio «Validacion de fidelidad (F26) antes de cualquier MQL5»
  (`MASTER_PLAN.md:45`), ya enmendado por las NOTAS de cabecera (`:11-26`).

**R5.1** (`docs/plan/HOJA-DE-RUTA.md:418-430`): citada en 0.1. Su «Hecho cuando» exige «la puerta
abre una sola partición», que es código en la puerta (0.2 c) y no entra en las rutas del segundo
tiempo que nombra el encargo; y `docs/plan/HOJA-DE-RUTA.md` tampoco está entre ellas (solo
`MASTER_PLAN.md`).

---

## El número del ADR del pre-registro

El último que existe es el **0094** (`ls docs/adr`). El **0095** está declarado inexistente en
**dos** bloques, no uno: `docs/encargos/trabajo-laminas-sesion-7b.md:11-13` y
`docs/validation/LAMINAS-7B.md:13-15` (informe cerrado). Leído en el código
(`src/botsito/validation/ids_citados.py:20-24`, `:55`, `:143-145`): «si el id declarado EXISTE,
falla (declaracion obsoleta)», con el mensaje «id declarado inexistente que SI existe»; lo corre
`knowledge validate` sobre `docs/**`, `CLAUDE.md` y `PROJECT_STATE.md` (`:66-71`). Crear el 0095
rompe los dos documentos hasta sacar los dos bloques. Precedente: el ADR-0087 nunca se creó, sigue
declarado en el encargo e informe de `trabajo/activar-sesion-05-motor` y la numeración siguió en el
0088 (`PROJECT_STATE.md:96`). **Le toca el ADR-0096** si se sigue el precedente; el ADR-0095 exige
sacarlo de los dos bloques, uno de ellos en un informe cerrado. Nada creado. Este informe declara
los dos (y el 0087) en su propio bloque `ids-inexistentes`: la rama que cree el ADR-0096 lo saca de
aquí en el mismo commit.

---

## El encargo frente al repo (auditor)

El subagente `auditor-encargo` contrastó 32 afirmaciones: 22 correctas, 0 incorrectas, 10 con
matiz, y 7 herencias que el encargo no recoge. Las que cambian lo que se pide:

1. **Los umbrales de fidelidad «ya pre-registrados»** (OBJETIVO): las cifras 0,70 y 0,60 están en
   el yaml, pero son el umbral de DESARROLLO sobre los días `dev` de mayo y el de construcción;
   ADR-0043:55-56 y `criterio_fidelidad.yaml:10` dicen que no son el PREREGISTRO del holdout, y
   ADR-0092 §7 dejó F26 como diagnóstico. **Ningún ADR fija hoy un umbral de F26 sobre lo
   reservado**, y `PREREGISTRO.md:19` lo pide «con su numero». El segundo tiempo no lo puede
   «copiar»: decisión 0.
2. **ADR-0070 punto 4** gobierna el umbral de construcción; el de medida lo gobierna la cláusula
   «Cambios» de ADR-0043 (`:59-61`) con su NOTA.
3. **El 0095 está declarado en dos documentos**, no en uno (arriba).
4. **«Una pregunta abre N particiones»** es «bloqueante antes de la primera autorización» y «rama
   propia» (`PUERTA-POR-PREGUNTA.md:171-174`, anterior al corte del 2026-10-01 de 0.1), y R5.1 lo
   pone en su «Hecho cuando»; las rutas del segundo tiempo no incluyen `src/botsito/cases/`.
5. **La Next Action con `fidelidad-1`**: 4 retirados, no 3 (0.3).
6. **«No busques dentro de anexos/: hay ficheros con líneas ocultas»**: `.claude/hooks/ficheros_con_ocultos.txt`
   no lista ninguno de `anexos/`; los cuatro de `docs/validation/` son `*-SALIDA.txt` del primer
   nivel. La prohibición es prudente y la cumplí (salvo el anexo de construcción que manda 0.4).
7. **El orden**: R5.1 «Depende de: la decisión del consultor sobre cuántos días» (`HOJA-DE-RUTA.md:428`),
   y la F de la Next Action pone delante grabar y activar la 7b; el encargo no dice por qué G se
   adelanta (la Next Action deja el orden al consultor, `PROJECT_STATE.md:23`).
8. **Las rutas del segundo tiempo** nombran `MASTER_PLAN.md` pero no `docs/plan/HOJA-DE-RUTA.md`,
   y el cierre actualiza R5.1.

Los demás matices (el tag en origin, que el auditor no pudo ver sin red y yo sí; el tamaño de
`PROJECT_STATE.md` en la rama, 24.480 tras la apertura; «## Preguntas» que el código no exige; los
papeles de ADR-0072) están recogidos en sus puntos.

---

## Lo que el encargo no preguntó y hace falta

1. **No existe el camino que mide F26 sobre una partición.** La puerta protege hoy un solo comando
   (`kit kappa --incluir-holdout`). El arnés solo lee días `dev` y lanza si un caso está oculto
   (`engine/arnes.py:139-162`), y niega todo mes de medida (ADR-0048 §7); la ingesta descarta los
   días reservados «sin escribirse en ningun sitio» (`cases/ingesta.py:8-18`). Medir F26 exige
   ingerir el detalle por operación de los días de una partición -eso ES abrirla (ADR-0021 §1)- por
   un camino guardado que llame a `abrir` y gaste la pregunta antes de leer, y que no deje ese
   detalle commiteado en `knowledge/cases/<camino>/` sin lector guardado (Technical Debt,
   `PROJECT_STATE.md:130`). Es rama propia con su ADR, como la de mayo (ADR-0070 punto 6), y es el
   sitio natural del arreglo de 0.2 c: un comando nuevo que nombre su partición no tiene el bucle de
   `kappa_entre_sesiones`.
2. **El día quemado de `holdout-2` debería estar en `retirados.yaml`** (ADR-0041 es posterior a la
   obligación 4 de HOLDOUT-EXPOSICIONES) o el pre-registro tiene que excluirlo por escrito; hoy
   `casos_medidos` lo cuenta.
3. **Los días de junio de `holdout-1/2/3` no tienen material**: el pre-registro tiene que decir si
   el conjunto medido es «los días de la partición con material del trader» y qué pasa con los de
   junio (fuera, y no `no_trade`, que está sin decidir: `PROJECT_STATE.md:126`).
4. **El fallback de `leer_fichero`** (`holdout.py:328-331`) juzga una carpeta desconocida bajo
   `holdout-1`; entra con su primer llamante de producción (`PROJECT_STATE.md:134`).
5. **El libro de septiembre no está en `libros.yaml`**: no se puede leer, ni siquiera abierto por la
   puerta, sin su declaración (ADR-0039).
6. **El motivo de marzo en `meses_reservados.yaml:36-41`** dice «hasta que A-42 este resuelta», y
   lo está (ADR-0069); el fichero es solo-añadir y no se corrige: lo vigente lo dice `CLAUDE.md`.
7. **Quién autoriza y quién decide**: el encargo dice «decido yo» (el consultor); la apertura la
   autoriza Aleks (ADR-0021 §3; ADR-0072:20), y el pre-registro tiene que nombrarlo así.

## Lo que no me convence

1. **Que G sea un solo fichero para dos cosas que no se parecen.** La rentabilidad no abre ningún
   holdout y tiene todas sus cifras fijadas; F26 sobre lo reservado no tiene umbral, ni partición
   decidida, ni comando, y ya no es condición necesaria de nada. Con un solo `PREREGISTRO.md`, quitar
   la marca para escribir la rentabilidad deja a la puerta con dos barreras (autorización y pregunta
   `ABIERTA`) aunque nada de F26 esté decidido; y escribir después el hash de la spec o la parte de
   F26 invalida cualquier autorización ya dada (0.2 b). Se puede vivir con ello (sin preguntas
   `ABIERTA` ninguna autorización vale), pero hay que decidirlo sabiendo que es así.
2. **Que F26 tenga potencia para algo.** Con lo escrito: `holdout-1` tiene 6 días de mayo con
   material, `holdout-2` 3, `holdout-3` 3 o 2, y `fidelidad-1` 6 días medibles de un mes no ciego en
   el que «F26 excluye en bloque los días sin operaciones»; todo sin vídeo (S-14). A la densidad de
   construcción (mediana 2 operaciones por día, 0.4), cualquiera de esas particiones da unas pocas
   decenas de operaciones como mucho. `cases/fidelidad.py:18-24` ya lo dice: una cifra descriptiva
   con su intervalo, no una medida con potencia.
3. **Que el sesgo del material sin vídeo afecte por igual a construcción y a medida.** Todo lo
   reservado es sin vídeo; julio, el único con vídeo, tiene el doble de operaciones por día. Una
   cobertura medida sobre un libro que omite sesiones no es la del trader.
4. **El conteo de exposiciones** (15, 16, 19 y 4 filas) no dice que ninguna queme; lo dice cada
   fila, y el pre-registro las tiene que copiar (`PREREGISTRO.md:22-23`). Copiarlas sin abrir su
   contenido en el terminal no es posible: la fila del 2026-09-11 escribe el PnL diario de mayo.
5. **El hash de la spec en G**: ADR-0092 §5 lo pone en «la spec sellada en PREREGISTRO, que rellena
   G», pero la spec no está sellada hoy y no lo estará hasta que la construcción llegue al umbral;
   G no puede escribir hoy un hash que valga.

## Lo que no pude medir

- Cuántos días medibles de cada partición son de mayo, de junio o de septiembre: exige leer el mes
  de la clave de la asignación, que el encargo no permite (decisión 2).
- De qué mes es el día retirado de `holdout-3` el 2026-10-14.
- Si las exposiciones de cada fila afectan a días concretos: el encargo pide solo su número.

## Exposiciones

Declaradas en `docs/validation/HOLDOUT-EXPOSICIONES.md`, fila del 2026-11-19 de esta rama, escrita
antes del primer `make check` y de la primera lectura de 0.2, y ampliada en el commit de la fase 0
con lo leído de más ese mismo día (abajo). Ninguna quema:
- recuentos de días de la asignación por partición (ninguna clave en el terminal);
- los `make check` del día (el M1 de marzo, como siempre);
- **escrito tarde, el mismo día**: al mirar la forma de la tabla de HOLDOUT-EXPOSICIONES y la
  obligación 4, el terminal enseñó la fila del 2026-09-11 (el calendario de PnL de mayo, ya
  declarado ese día), la fecha del día quemado de `holdout-2` (que escriben
  `HOLDOUT-EXPOSICIONES.md:176` y `tests/unit/test_puerta_holdout.py:98`), y al leer ADR-0021 las
  cuatro cifras de PnL de su línea 48 (ya declaradas); y el subagente auditor leyó la cabecera de
  `retirados.yaml` y su recuento.

## Lo que necesito que decidas

0. **El umbral de F26 sobre lo reservado, que no existe.** Opciones: (a) el ADR del pre-registro
   adopta para F26 las cifras de ADR-0043 (las mismas, sin cifra nueva) y dice que F26 es diagnóstico
   (ADR-0092 §7): un «no llega» no bloquea nada, se informa en el memorando; (b) F26 sin umbral:
   cifra descriptiva con su intervalo, y el ADR del pre-registro enmienda ADR-0021 §3 («contra que
   umbral») para el diagnóstico; (c) un umbral propio de F26, que fijas tú en el ADR. Recomiendo
   (a): cumple ADR-0021 §3 sin cifra nueva y no contradice §7. Coste de (b): enmendar ADR-0021.
   Coste de (c): una cifra nueva elegida con las corridas de construcción a la vista.
1. **Sobre qué partición se mide F26 primero.** Opciones: (a) `holdout-1` (ADR-0021 §6,
   MASTER_PLAN:127): mayo, ciego, 6 días con material; (b) `fidelidad-1` (`PUERTA-POR-PREGUNTA.md:216`):
   septiembre, no ciego, 6 medibles, sesgo en directo del trader sobre sus velas; (c) esperar a
   marzo (`fidelidad-2`/`-3`, entra por R5.3) o a febrero (heredado 6). Recomiendo (a): es el único
   reservado ciego y el que ADR-0021 guarda para esto. Coste de (b): un mes visto y con una
   exposición en directo. Coste de (c): F26 espera a R5.3 o a una rama de febrero.
2. **Cuántos días hacen falta, y cómo se cuentan.** Opciones: (a) los días de la partición CON
   material del trader (mayo), excluyendo por escrito los de junio y el quemado de `holdout-2`, y me
   autorizas a contar los medibles por mes de la clave sin imprimirla, para dártelos; (b) tomar los
   recuentos de `PREREGISTRO.md:28` (6/4/3) y la obligación 4 tal cual, sin medir; (c) juntar
   particiones en una sola medida. Recomiendo (a): el número que decide es «días con material»,
   y hoy no está medido. Coste de (b): no ve el retirado de `holdout-3`. Coste de (c): gasta dos
   oportunidades a la vez (ADR-0021 §6).
3. **Pedir otro mes al trader.** Opciones: (a) pedírselo ya, con vídeo (por S-14); (b) contar con
   marzo y febrero; (c) no pedirlo. Recomiendo (a): todo lo reservado es sin vídeo. Coste de (b):
   marzo tampoco es ciego para el sesgo de S-14 ni tiene vídeo.
4. **«Una pregunta abre N particiones».** Opciones: (a) la rama que construya el comando de medida
   de F26 lo nace abriendo una sola partición, y el arreglo de `kappa_entre_sesiones` es una rama
   corta aparte antes de cualquier autorización de kappa; (b) el segundo tiempo de esta rama hace el
   arreglo (amplía el contrato a `src/botsito/cases/` y `tests/`); (c) nada hasta la primera
   autorización. Recomiendo (a): hoy el bucle solo existe en kappa, y no hay etiquetas. Coste de
   (b): una rama de documentos se convierte en rama de código de la puerta. Coste de (c): R5.1 no
   puede darse por hecha («abre una sola partición»).
5. **Qué entra en PREREGISTRO.md en el segundo tiempo.** Opciones: (a) la rentabilidad entera menos
   el hash de la spec y el sha de `src/`, que se escriben en la rama de la medida antes de correr (con
   el procedimiento fijado ahora: qué ficheros, bytes o canónico, árbol o commit); la parte de F26
   con lo que decidas aquí; las preguntas sin ninguna `ABIERTA` hasta la rama de medida; marca fuera;
   (b) lo mismo, pero la marca se queda hasta que F26 tenga comando; (c) dos ficheros
   (`PREREGISTRO.md` para el holdout y otro para la rentabilidad), enmendando ADR-0092 §13.
   Recomiendo (a): la rentabilidad queda fijada ya y la puerta sigue cerrada por las preguntas.
   Coste de (b): cada edición siguiente vuelve a toparse con `test_puerta_holdout`. Coste de (c): un
   ADR que enmienda ADR-0092.
6. **Qué se hace si F26 no llega.** Opciones: (a) lo de ADR-0021 §6: se corrige y se mide en
   `holdout-2`; (b) con F26 diagnóstico, se informa y no se repite; (c) se repite solo con un mes
   nuevo. Recomiendo (b) si en 0 eliges (a) o (b): un diagnóstico no se re-mide, y `holdout-2` tiene
   3 días de mayo. Coste de (a): gasta `holdout-2` en una cifra que ya no decide nada.
7. **Kappa, paridad y DSR de MASTER_PLAN §H.** Opciones: (a) cada uno a su funcionalidad (kappa a
   la sesión que etiquete, paridad a F30/F32, DSR a F27), y la fila de §H lo dice; (b) los fija el
   segundo tiempo. Recomiendo (a): ninguno abre un holdout de fidelidad y no hay medida que los
   sostenga. Coste de (b): tres cifras nuevas sin medida.
8. **El número del ADR del pre-registro.** Opciones: (a) el 0096, saltando el 0095 como se saltó el
   0087; (b) el 0095, sacándolo de los dos bloques (uno en un informe cerrado). Recomiendo (a):
   no toca un informe cerrado. Coste de (b): editar `LAMINAS-7B.md`, cerrado en `main`.
9. **Las rutas del segundo tiempo.** Además de las que nombra el encargo: `docs/plan/HOJA-DE-RUTA.md`
   (R5.1) y, si en 2 eliges retirar el quemado, `knowledge/cases/retirados.yaml` (con `Fuente:`).
   Opciones: (a) entran; (b) R5.1 se toca en el cierre. Recomiendo (a).

## Estado

`PROJECT_STATE.md`: 24.505 bytes (`wc -c`), por debajo de 25.000. Sin revisor en este primer tiempo,
como manda el encargo (lo lleva el segundo, sobre la rama entera); el auditor sí se lanzó.

Rama en PARADA de la fase 0, NO lista para revisión y NO cerrada. Espero tu respuesta a la PARADA.
