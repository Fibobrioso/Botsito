# Sesión 02: las decisiones del consultor sobre el inventario, aplicadas

Rama `trabajo/sesion-02`, 2026-09-25. Sin merge, sin tag y sin push. Aplica las decisiones del
consultor sobre `SESION-02-INVENTARIO.md` y `SESION-02-BUSQUEDA-CLASIFICACION.md`, una pieza por
commit.

## 1. K-04: a qué regla afecta A-21

**El origen.** A-21 nace en ADR-0019 (commit `d264912`, 2026-09-10) preguntando qué es un breaker,
y se reformula el mismo día. ADR-0019: «Lo que sí queda abierto, y por eso A-21 se reformula en vez
de borrarse: **qué es una zona de control "limpia, sin ruido"**. Es lo único de la geometría de
entrada que sigue siendo cualitativo.» La nota de `PROJECT_STATE.md`, entrada (10) del 2026-09-10,
dice lo mismo: «A-21 se REFORMULA a lo unico que sigue siendo cualitativo: que es una zona de
control "limpia, sin ruido"», con RN-008 como la regla que dejaba de estar pendiente.

**Los pasajes que la sostienen** son los tres de su `evidencia`, y los tres hablan del esquema de
entrada en M1:
- `ev-v1-001435-f0586d02` (v1 0:14:35): «cuando se desarrolle esta zona de control que no haga
  mucho ruido, o sea, sea una zona limpia», y a continuación el breaker activa la orden límite;
- `ev-v4-000243-5f8875ce`: los dos esquemas de entrada;
- `ev-v3-004201-bfeb3734`: el primero no espera retroceso.

**La spec.** Ninguna regla cita A-21. RN-004 (`strategy_spec.yaml`, la liquidez de M15) cita A-24,
DECIDIDA por ADR-0045, y A-35, bloqueante. La geometría de la entrada es RN-008 («sin ninguno de
los esquemas de entrada no hay entrada»), cuyo segundo esquema es el que deja una zona de control.

**De dónde salía el error.** La frase «RN-004 sigue BLOQUEADA por A-21 y A-35» entra en
`PROJECT_STATE.md` en `0901d2c` (2026-09-24, `docs(state)` del cierre de `trabajo/a35-pivote-formado`)
y en el cuerpo de `A35-FOTOGRAMAS-RESULTADO.md`, sin fuente en ninguno de los dos.

**Qué se corrige.** El lado equivocado es `PROJECT_STATE.md`: sus dos apariciones (la funcionalidad
actual y Next Action 22) dicen ahora que RN-004 está bloqueada solo por A-35 y que A-21 toca RN-008.
`A35-FOTOGRAMAS-RESULTADO.md` está cerrado en `main`, así que lleva un recuadro de corrección junto
al pasaje y su cuerpo no cambia. La spec no se toca: no dice nada falso.

**Resultado: A-21 afecta a RN-008, no a RN-004. RN-004 queda bloqueada solo por A-35.** A-21 sigue
siendo bloqueante, ahora de la regla que le corresponde. Que ninguna regla la cite es un hueco de
enlace, no un error: no se abre aquí.

## 2. K-07: `huso_grafico` frente al «UTC+2 fijo»

**Hablan de lo mismo.** `huso_grafico` es, según su propia `unidad`, el «nombre IANA del huso
configurado en el grafico del trader», es decir cómo se etiquetan las horas en su pantalla de FX
Replay. El «UTC+2 fijo» de `CLAUDE.md` y de ADR-0039 es el reloj de esos mismos gráficos. **No es
el huso del xlsx**: ese se declara libro a libro (ADR-0039, `knowledge/corpus/libros.yaml`) y se
mide por velas. Tampoco es el reloj del servidor (A-28) ni `huso_operativa`. Son cuatro relojes.

**La cadena.**
- ADR-0012 §5 (2026-09-09) lo fijó en `Etc/GMT-2`.
- ADR-0015 lo discutió: todas las lecturas eran de verano.
- ADR-0017 §4 (2026-09-10) lo pasó a `Europe/Madrid`, con la premisa de que «no hay ninguna
  configuracion deliberada de huso» y la plataforma muestra la hora local.
- `ABRIL-Y-LA-CAJA.md` R0 (2026-09-21) lo mide en un fotograma de **enero** de v4: el propio gráfico
  marca «14:29:59 UTC+2» sobre «Thu 29 Jan '26», y en enero Madrid es UTC+1.
- ADR-0039, posterior y vigente, lo da por hecho: «el eje de FX Replay supuesto UTC (es UTC+2
  fijo)».

Nadie llevó la medida al registro ni enmendó ADR-0017: esa es la contradicción. La medida contesta
justo la objeción de ADR-0015, porque es de invierno.

**Qué se aplica, solo en documentación y configuración:**
- `huso_grafico` pasa a `Etc/GMT-2`, CONFIRMED, con fuente `ev-v4-011425-ae028b78`. En v4, a la
  pregunta de si el horario es «en el horario UTC más 2», el trader contesta «De UTC más 2, de 7,
  claro». La descripción cita la medida y ADR-0039.
- ADR-0017 lleva una enmienda del punto 4; ADR-0012 y ADR-0005, una nota cada uno.
- `spec_version` sube de 12.2.1 a 12.2.2 (parche: cambia un valor) y se regeneran el manifiesto y
  `docs/spec/`.

**Por qué no altera nada que esté commiteado:**
- Ningún código lee `huso_grafico`: su único consumidor declarado es ADR-0017, documental.
- El kit, la fidelidad, la ingesta, la hoja y `scripts/huso_por_velas.py` leen `huso_operativa`.
- Ningún artefacto de `knowledge/cases/` ni `docs/runbooks/ENTRADA-MARZO.md` congela
  `spec_version` ni el hash de la spec.

**Lo que NO se cambia, y es del consultor.** La premisa que cae sostenía también ADR-0017 §1:
`huso_operativa = Europe/Madrid`, es decir que la ventana de 07:00 a 15:00 es la hora civil del
trader. Con el gráfico en UTC+2 fijo, la ventana puede seguir su reloj civil o el de su gráfico.
Las dos lecturas coinciden en verano y se separan una hora en invierno: las 07:00 de su gráfico
son las 06:00 de Madrid. El corpus tiene las dos formas:
- «de 7 a 15 por España» (`ev-v3-000136-6160fcea`);
- «De UTC más 2, de 7, claro» (v4 #1280).

A-14 (RESUELTA) dice que «mantiene el mismo rango de horarios», sin decir en qué reloj. **Esto sí
toca a marzo:** del 1 al 28 de marzo de 2026 Madrid va en UTC+1 y a partir del 29 en UTC+2, así
que con una de las dos lecturas la ventana del bot va una hora desplazada respecto a la del trader
casi todo el mes. Lo mismo vale para enero. Cambiar `huso_operativa` alteraría el reparto en
sesiones de la fidelidad, la ingesta y los días que usa la herramienta del huso de ENTRADA-MARZO.
**No se toca.**

## 3. K-02, K-05 y K-06: documentación

- **K-02.** `scripts/README.md` lista ahora `mover_sesion.py`, con su propósito tomado de su
  docstring y la referencia a `knowledge/cases/kit/README.md`, que explica cuándo se usa.
- **K-05.** ADR-0011 lleva una nota de enmienda: la frase «Se cierra una ambiguedad solo con un
  registro del trader» ya no es la única vía desde que ADR-0022 §7 creó `DECIDIDA`.
- **K-06.** `CLAUDE.md` conserva la cifra del 2026-09-17, ya fechada, y añade la de hoy medida con
  el mismo recuento: 13 fotogramas distintos citados por 12 ítems de 368. El recuento es el de los
  ids `fr-…/<ms>` dentro de `knowledge/evidence/`. Aplicado sobre `a0de4af`, el commit que
  escribió la cifra vieja, reproduce 8 y 9.

K-01 (ADR-0045 en el índice de PROJECT_STATE) y K-03 (la deuda que ya está hecha) no se tocan: van
en el paso 3 del ritual.

## 4. Las ambigüedades nuevas: A-36 a A-41

Se abren con los siguientes números libres, en `knowledge/spec/ambiguedades.yaml` y en la tabla
«Known Ambiguities» de `PROJECT_STATE.md`. La nota de cada una, en comentarios junto a la entrada
como en A-35, cita su evidencia y lo que queda abierto.

| id | candidato | título | evidencia | ¿bloqueante? y por qué |
|---|---|---|---|---|
| A-36 | C-01 | en qué punto de la mecha va la orden límite | `ev-v4-010605-a11249c0` | no: RN-011 coloca la orden en la zona (`en: Z`) y la spec no dice que haga falta el precio exacto |
| A-37 | C-02 | en qué temporalidad se busca la vela contraria de la que sale el stop | `ev-v1-001454-69cebe62`, `ev-v3-004353-b7661782` | no: la spec no lo dice de RN-011 ni de RN-012, aunque las dos miden `stop_fraccion_caja` sobre una caja cuyo extremo sale de aquí |
| A-38 | C-04 | cuándo se da por anulada una orden límite que el precio deja sin llenar | `ev-v4-010731-bb8af97c`, `ev-v4-010857-5bc906c9` | no: ninguna regla la necesita; RN-006 cubre la orden que se mueve |
| A-39 | C-05 | qué pasa con lo que viene de la primera sesión cuando la segunda cambia el sesgo | `ev-v3-010304-4468cc20` (lateral L-1) | no: ninguna regla la necesita |
| A-40 | C-06 | qué se hace con el stop después del break even | `ev-v3-003220-8805194d`, `ev-v3-003318-f1a2d27d` (lateral L-2) | no: RN-014 se escribe sin ella |
| A-41 | C-07 | si hay un tope de entradas por día, aparte de los cartuchos | `ev-v4-003350-acb03ee7`, `ev-v2-001615-d96c699f` | no: RN-016 y RN-020 se escriben sin ella |

**A-41 cita las dos lecturas del pasaje de v4 0:33:50:**
- **por día**, la de su ítem («confirma: como maximo dos entradas por dia, por separado») y la de la
  clasificación;
- **por zona**, la de A-2, que lo lleva como evidencia de «¿2 o 3 intentos por zona?».

Al preparar A-41 apareció que `ev-v3-002714-742f2589`, citado en la clasificación B3 (C-07 P2), está
**supersedido** por `ev-v6-000732-f9c41d5e`. Se corrige con un recuadro en
`SESION-02-BUSQUEDA-CLASIFICACION.md`, y A-41 no lo lleva en su evidencia.

Todas las evidencias citadas se comprobaron: ninguna está supersedida.

**C-03** (el lado del libro que dibuja FX Replay) queda PARA DATOS y no se abre. **C-08** no se abre:
es la unidad de fidelidad y la explica el reporte al consultor.

## 5. El campo `pregunta`, en forma abierta

Se reescriben las de A-13, A-18, A-21, A-24 (como confirmación, con el texto que dio el consultor),
A-25, A-26, A-29, A-30, A-31, A-32, A-33 y A-34, y nacen así las seis nuevas. A-35 se queda como
está. El criterio:
- sin alternativas, sin cifras y sin la respuesta esperada;
- una sola incógnita por pregunta;
- en español natural, en una o dos frases;
- la situación descrita, no la solución.

**El texto anterior queda citado entero** en un comentario junto a la entrada: «PREGUNTA ANTERIOR,
SUSTITUIDA PORQUE SUGERIA RESPUESTA». Con él se conservan las medidas y el historial que llevaba.
El estado de ninguna cambia: A-24 sigue DECIDIDA (ADR-0045) y las demás, ABIERTAS.

## 6. El runbook de la sesión

`docs/runbooks/SESION-DE-PREGUNTAS.md`, que no existía. Consolida los pasos repartidos entre
ADR-0011 §8, ADR-0012 §7, ADR-0022 §7, ADR-0023 §2, `knowledge/cases/kit/README.md` y el informe
de la sesión 01, para una sesión **solo de preguntas**: sin `kit build`, sin paquete y sin casos.
Lleva las cuatro reglas del consultor y lo que hace Aleks antes, durante y después.

**Lo que añade la consolidación y no estaba escrito en ningún sitio:**
- **Comprobar que el día de la sesión no es reservado**, con una línea que imprime solo `True` o
  `False` sobre `casos_ocultos`. Es la lección de v6, cuyo día resultó reservado y hoy está
  retirado (ADR-0041). Se probó con una fecha fuera de todo el material, así que no revela nada;
  y los 34 ids ocultos llevan la fecha ISO, que es lo que la comprobación busca.
- **Dónde va la hoja**: se genera en la raíz del repositorio, que **no es un sitio commiteable**
  (`/*.docx` en `.gitignore`), como la de la sesión 01. Se versionan su fuente
  (`ambiguedades.yaml`) y su orden (el script). La hoja rellenada va a
  `corpus/…/Sesiones/<sesion>/`, que tampoco se versiona y entra por el inventario.

Todos los comandos del runbook se comprobaron contra la CLI (`feedback new`, `corpus transcribe`,
`corpus frames extract`, `corpus inventory`).

## Estado

EN CURSO. Cada sección entra con su commit.
