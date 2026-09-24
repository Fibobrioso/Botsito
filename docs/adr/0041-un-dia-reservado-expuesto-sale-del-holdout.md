---
status: ACTIVE
date: 2026-09-23
phase: post-F14 (rama `trabajo/v6-fuera-del-holdout`)
---

# 0041 · Un día reservado expuesto sale del holdout y no se sustituye

## Decision

1. **Un día reservado cuya exposición no se puede descartar SALE del holdout.** Deja de medirse:
   no cuenta en ninguna partición.
2. **No pasa a desarrollo y no se sustituye por ningún otro día.** Sigue OCULTO, y sus etiquetas
   no se leen nunca: **la puerta lo rechaza siempre, con o sin autorización**
   (`holdout.abrir_caso`, `holdout.leer_fichero`).
3. **Dos conjuntos derivados, y cada consumidor usa el suyo.**
   - `casos_medidos` = reservados − retirados. Lo usa todo lo que MIDE.
   - `casos_ocultos` = reservados ∪ retirados. Lo usa todo lo que OCULTA: `feedback trace`,
     `knowledge validate` (`biblioteca`), `kit kappa` y `dias_ingeribles`.
   - `casos_reservados` sigue siendo lo que declaran los repartos, sin tocar.
4. **La retirada vive en `knowledge/cases/retirados.yaml`, SOLO AÑADIR.**
   - Cada entrada va por la **huella** del id del caso (su sha256), nunca por el id ni por la
     fecha.
   - Lleva `motivo`, `exposicion` (su entrada en `docs/validation/HOLDOUT-EXPOSICIONES.md`), `adr`
     y `retirado_el`.
   - `knowledge validate` comprueba tres cosas: la forma; que cada huella sea de un caso reservado;
     y que ninguna entrada commiteada se borre ni se modifique. Lo hace contra el historial, con
     el mismo mecanismo que `libros.yaml` (ADR-0039).
5. **El reparto no se toca.** `particiones.yaml` sigue declarando el mismo cupo, y la medida de su
   partición se hace sobre un día menos. La diferencia se documenta en el propio `retirados.yaml`
   y en el informe de la rama que retira.
6. **El primer día retirado** es el día reservado en que se grabó v6. Motivos:
   - su transcripción se leyó en ramas anteriores, y si trae detalle por operación de ese día solo
     se sabe leyéndola (exposición posible);
   - su identidad quedó escrita en el historial de git por el commit `cdcf58e`.
   
   Las dos cosas están declaradas en `HOLDOUT-EXPOSICIONES.md`.

## Problema que resuelve

`casos_reservados` hacía dos trabajos a la vez: decía qué se MIDE y qué se OCULTA.

- **Por qué no bastaba con sacar el día de ese conjunto.** Lo habría dejado sin ocultar:
  - `feedback trace` imprimiría el valor de sus etiquetas;
  - `knowledge validate` aceptaría un caso suyo en `dev`;
  - `kit kappa` las leería.
  
  Eso es pasarlo a desarrollo, justo lo contrario de retirarlo.
- **Por qué no se podía escribir la retirada en el reparto.** Rompe la garantía del camino de
  fidelidad (ADR-0036): el reparto se reproduce byte a byte desde la semilla y está anclado por el
  sha de su blob. Un estado nuevo dentro de él haría fallar `fidelidad check` para siempre, y el
  reparto dejaría de ser el que se fijó antes de leer etiquetas.

## Alternativas consideradas

- **(a) Un estado «retirado» dentro de `particiones.yaml`.**
- **(b) Un fichero aparte, solo añadir.** Es la elegida.
- **(c) Que `construir` aplique las retiradas después del sorteo.**
- **Sustituir el día por otro no reservado.**

## Por que elegimos esta opcion

(b) deja intactas las dos garantías del reparto, la reproducción y el ancla. Además da a la
retirada su propio régimen: se ve en un diff, cita su exposición y su ADR, y no se puede deshacer
sin que `knowledge validate` lo diga. Separar «medidos» de «ocultos» hace explícito para qué
quiere cada consumidor el conjunto, que es donde estaba el defecto.

## Por que descartamos las demas

- **(a)** rompe la reproducción byte a byte y obliga a re-anclar un reparto que tiene que ser el
  del sorteo.
- **(c)** cambia el mecanismo de reproducción de ADR-0036 para resolver un caso que no es suyo.
- **Sustituir el día** metería en la partición un día elegido DESPUÉS de conocer la exposición,
  que es el tipo de decisión que un reparto pre-registrado existe para impedir.

## Impacto

- `holdout.py` gana `huella_de_caso`, `cargar_retirados`, `casos_retirados`, `casos_medidos`,
  `casos_ocultos`, `abrir_caso` y `problemas_de_retirados`.
- `leer_fichero` rechaza un fichero cuyo nombre sea el id de un retirado.
- `biblioteca`, `ingesta`, `cli` (`feedback trace`) y `paquete` (`kit kappa`) pasan a
  `casos_ocultos`. `kit kappa` no lee nunca un retirado, ni con `--incluir-holdout`, y lo dice por
  recuento.
- `knowledge validate` añade la comprobación de `retirados.yaml`.
- Reservados: 34. Medidos: 33.
- **La huella no es un secreto.** Un día laborable de un mes se adivina probando una veintena de
  fechas. Lo que la huella evita es que la fecha quede escrita en el repositorio, no que se pueda
  deducir.

## Fecha / fase

2026-09-23, post-F14, rama `trabajo/v6-fuera-del-holdout`. Decisión del consultor sobre las
preguntas P1 a P4 de `docs/validation/V6-FUERA-DEL-HOLDOUT.md`.

## Estado

ACTIVE
