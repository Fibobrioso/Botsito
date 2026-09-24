# El día reservado de v6 fuera del holdout (ADR-0041)

Rama `trabajo/v6-fuera-del-holdout`, 2026-09-23. Es el punto 16 de Next Action. Sin merge, sin tag
y sin push. En este informe no aparece la fecha del día.

**La decisión del consultor.** El día reservado en que se grabó v6 SE RETIRA del holdout. No pasa
a desarrollo y no se sustituye por ningún otro. El motivo es doble: su lectura previa es una
exposición posible, y su identidad quedó en el historial por `cdcf58e`.

**Cómo va el informe.** La rama se paró en el paso 0 con cuatro preguntas (§1 a §3, `af4be96`).
El consultor las contestó, y la retirada está hecha (§4 en adelante).

## 1. Dónde y cómo está definido el conjunto reservado

- **Dónde vive.** Es `botsito.cases.holdout.casos_reservados(repo)`. Recorre todos los
  `particiones.yaml` que devuelve `repartos_commiteables`, de los dos caminos:
  - el kit, en `knowledge/cases/kit/*/`;
  - la fidelidad, en `knowledge/cases/fidelidad/*/`.
  
  De cada uno devuelve `caso -> particion` para toda partición de `RESERVADAS`, que son
  `holdout-1/2/3` y `fidelidad-1/2/3`.
- **Las cuentas.** Salen 34 casos reservados:
  - 24 del kit (el paquete de la sesión 1: `holdout-1`, `holdout-2` y `holdout-3`, 8 cada una);
  - 10 del artefacto de fidelidad `eurusd-2026-09` (`fidelidad-1`).
  
  El día de v6 está en ese artefacto, en `fidelidad-1`. Lo he medido con un booleano, sin imprimir
  la fecha.
- **Quién lo usa.** Todos los consumidores lo usan como **conjunto de lo que se OCULTA o se
  EXCLUYE**:
  - `ingesta.dias_ingeribles` resta los reservados de lo ingerible;
  - `biblioteca.problemas_de_biblioteca` hace fallar `knowledge validate` si un `caso-*.yaml` de
    `dev` es reservado;
  - `cli` (`feedback trace`) oculta los valores de los reservados al imprimir;
  - `paquete` (`kit kappa`) excluye las etiquetas de los reservados, salvo autorización.

## 2. El régimen del fichero que contiene el día

`knowledge/cases/fidelidad/eurusd-2026-09/particiones.yaml` está **congelado por dos mecanismos**:

1. **Reproducción byte a byte.** `fidelidad.comprobar` recompone el artefacto con lo congelado
   (seed, cupos, universo y config) y lo compara byte a byte con lo commiteado. Su docstring dice
   que «aquí NINGÚN fichero se exime nunca». La asignación sale de `particiones.asignar(casos, seed,
   cupos, orden)`, que es determinista.
2. **Ancla por sha del blob**, en `knowledge/cases/fidelidad/anclas.yaml` (ADR-0035, enmienda).
   Re-anclar es posible, pero explícito: otro fichero, en un diff visible y con trailer `Fuente:`.

Es lo que da la **anterioridad demostrable** del camino de fidelidad (ADR-0036): que el reparto se
fijó ANTES de leer ninguna etiqueta, comprobado por máquina.

**Lo que depende del número 34: ningún test lo afirma.**
- `test_los_casos_reservados_salen_de_la_asignacion_sin_abrir_nada` compara con la unión recalculada desde los ficheros, no con
  una cifra.
- El 34 solo aparece en un docstring de `test_puerta_holdout.py`, que cuenta una medida histórica.
- `test_mes_del_material.py` cuenta los 4 `fidelidad-dev` de septiembre, que no cambian.
- **`kit check` no cambiaría**: el día no está en el paquete del kit.

## 3. Por qué se paró, y las preguntas (contestadas en §4)

**P1. El mecanismo de la retirada rompe una garantía, según cuál se elija.**
- **(a) Escribir un estado «retirado» en `particiones.yaml`** rompe la reproducción byte a byte:
  `asignar` volvería a dar `fidelidad-1`, y `fidelidad comprobar` fallaría para siempre. Además
  obliga a re-anclar. El reparto dejaría de ser el que se fijó antes de leer etiquetas, que es la
  garantía de ADR-0036.
- **(b) Un fichero aparte de retiradas** (por ejemplo `knowledge/cases/retirados.yaml`, solo
  añadir, con ADR y `Fuente:`) deja el reparto intacto y reproducible. Pero es un régimen nuevo, y
  hay que decidir su forma.
- **(c) Enseñar a `construir` a aplicar las retiradas después del sorteo** cambia el mecanismo de
  reproducción de ADR-0036.

¿Cuál?

**P2. «No aparece en el conjunto reservado» choca con lo que ese conjunto hace.** Hoy
`casos_reservados` es el conjunto de lo que se OCULTA (§1). Si el día sale de él sin más:
- `feedback trace` imprimiría el valor de sus etiquetas;
- `knowledge validate` aceptaría un `caso-*.yaml` suyo en `dev`;
- `kit kappa` leería sus etiquetas.

Eso **lo pasaría a desarrollo**, justo lo contrario de la decisión. Lo que parece hacer falta son
dos conjuntos:
- **reservados**: el holdout que se medirá, 33 casos;
- **ocultos**: reservados más retirados, que es lo que usan todos los consumidores que ocultan.

Y hay que decidir si la puerta (`abrir`) se niega a ese día SIEMPRE, sin autorización posible.
¿Es ese el diseño?

**P3. El cupo de `fidelidad-1`.** `particiones.yaml` declara 10. Con la retirada, la medida de F26
sobre `fidelidad-1` se hará con 9. ¿Se deja el cupo congelado como está y se documenta la retirada
aparte, que es lo que haría (b)?

**P4. El ADR.** El siguiente número libre de ADR es el **0041**; lo comprobé en `docs/adr/`. No se ha
escrito, porque su contenido depende de P1 y P2.

## 4. Las decisiones del consultor

- **P1: la opción (b).** Un fichero aparte, solo de añadir: `knowledge/cases/retirados.yaml`.
  Cada entrada lleva la huella (sha256) del id del caso, el motivo, la referencia a su exposición
  y el ADR. Ni `particiones.yaml` ni ADR-0036 se tocan.
  - **Sobre el sitio:** no hay un lugar mejor en el repositorio. `knowledge/cases/` es donde viven
    los repartos que la retirada modifica en efecto, y el otro fichero de solo añadir del mismo
    tipo, `libros.yaml`, vive junto a su dominio (`knowledge/corpus/`).
- **P2: sí.** Dos conjuntos derivados: «medidos» = reservados − retirados, y «ocultos» = reservados
  ∪ retirados. Todo lo que oculta usa «ocultos», y todo lo que mide usa «medidos». La puerta
  rechaza siempre un día retirado.
- **P3:** el reparto sigue declarando 10, y la medida de `fidelidad-1` se hace sobre 9. No se
  sustituye ningún día.
- **P4:** ADR-0041, «un día reservado expuesto sale del holdout y no se sustituye».

## 5. Lo que se ha hecho (`1aeae24`)

- **`knowledge/cases/retirados.yaml`**, con una entrada: la huella del caso, su motivo, su
  exposición y `ADR-0041`. Su cabecera documenta que la medida de `fidelidad-1` se hace sobre 9.
- **`src/botsito/cases/holdout.py`**:
  - `huella_de_caso`, `cargar_retirados`, `casos_retirados`, `casos_medidos`, `casos_ocultos`,
    `abrir_caso` y `problemas_de_retirados`;
  - `leer_fichero` rechaza siempre un fichero cuyo nombre sea el id de un retirado;
  - si `retirados.yaml` está mal formado, `casos_medidos` lanza, porque la puerta no responde a
    medias.
- **Consumidores que ocultan, pasados a `casos_ocultos`:**
  - `biblioteca.problemas_de_biblioteca` (`knowledge validate` y `casos check`);
  - `ingesta.dias_ingeribles`;
  - `feedback trace`;
  - `kit kappa`, que además no lee NUNCA un retirado, ni con `--incluir-holdout`, y lo avisa por
    recuento, sin id.
- **`knowledge validate`** comprueba `retirados.yaml`: la forma; que cada huella sea de un caso
  reservado; y que sea solo de añadir contra el historial, versión a versión, con el mismo
  mecanismo que `libros.yaml`. Imprime «OK: 1 dias retirados del holdout…».
- **Tests** (`tests/unit/test_retirados.py`, 6):
  1. un retirado no está en «medidos», está en «ocultos», y la puerta lo rechaza con una
     autorización válida, que sí abre la partición y el caso medido. El mensaje no nombra el caso;
  2. añadir una entrada vale; modificarla o borrarla falla, y commitear el borrado no lo arregla;
  3. en el repositorio real hay 1 retirado y 33 medidos, y ninguna salida de `knowledge validate`,
     `state check`, `casos check`, `spec status`, `feedback pending`, `kit check` ni
     `fidelidad check` imprime el id del retirado. El test no escribe el id: lo deriva de la
     huella;
  4. una huella que no es de ningún reservado falla;
  
  y dos más: que sin fichero «medidos» es igual a los reservados, y que una entrada mal formada
  cierra la puerta.

**`kit check`, idéntico a la línea base.** El día no está en el paquete del kit, así que no hay
diferencia que explicar.

**`fidelidad check`, idéntico** antes y después del cambio. Sigue diciendo «10 dias reservados
cuyas velas se leen: fidelidad-1 10», y es correcto: leer las velas de un día no es abrirlo
(ADR-0021 §1), y el día retirado sigue en el reparto.

## 6. Una medida que el brief no preveía: el reparto ya nombra el día

**`knowledge/cases/fidelidad/eurusd-2026-09/particiones.yaml` lleva el id del caso retirado EN
CLARO**, con su partición. Lo medí con un booleano, sin imprimirlo. Ese fichero está en `main`
desde `394a18e`, el sorteo de septiembre, y leer la asignación no es abrir.

- **Qué evita la huella de `retirados.yaml`:** que el repositorio diga en claro, en un sitio más,
  qué día se retiró.
- **Qué no evita:** que cualquiera cruce el reparto con la fecha de grabación de v6, que está en
  el manifiesto del corpus. Y la huella de un día laborable de un mes se adivina probando una
  veintena de fechas (ADR-0041, Impacto).
- **Lo que eso dice del desliz de `cdcf58e`.** Lo único nuevo que escribió fue la unión de esas
  dos cosas públicas en una frase. No cambia nada de lo hecho, y se anota para que nadie le
  atribuya a la huella más protección de la que da.

## 7. Lo que queda sin hacer

Nada del brief. Tampoco se ha ingerido ni leído ninguna etiqueta.

## Estado

WAITING_FOR_USER_VALIDATION
