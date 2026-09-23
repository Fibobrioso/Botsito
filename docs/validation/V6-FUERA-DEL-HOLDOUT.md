# El día reservado de v6 fuera del holdout: detenida en el paso 0

Rama `trabajo/v6-fuera-del-holdout`, 2026-09-23. Es el punto 16 de Next Action. Sin merge, sin tag
y sin push. En este informe no aparece la fecha del día.

**La decisión del consultor.** El día reservado en que se grabó v6 SE RETIRA del holdout. No pasa
a desarrollo y no se sustituye por ningún otro. El motivo es doble: su lectura previa es una
exposición posible, y su identidad quedó en el historial por `cdcf58e`.

**Lo que se ha hecho: solo el paso 0, leer.** No hay ni código, ni ADR, ni tests, ni cambios en la
asignación. La rama se para aquí por la regla del brief: *«Si el régimen no permite retirar un día
sin romper una garantía […], PARA la rama 1, escribe la pregunta»*. Y hay además dos decisiones de
diseño que el brief no toma (§3).

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

## 3. Por qué se para, y las preguntas

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

## 4. Lo que queda sin hacer

Los pasos 2 a 5 del brief:
- el ADR;
- el estado «retirado»;
- los tests de 33 reservados, de que no sea ingerible y de que ningún comando nombre el día;
- `kit check`;
- la entrada en `HOLDOUT-EXPOSICIONES.md`;
- el punto 16 de Next Action como HECHO.

**El punto 16 sigue abierto.**

## Estado

WAITING_FOR_USER_VALIDATION: detenida en el paso 0, con las preguntas P1 a P4.
