---
status: ACTIVE
date: 2026-09-24
phase: post-F14 (rama `trabajo/entrada-marzo`)
---

# 0046 · Marzo entra por el camino de fidelidad, con su reserva y sin repetir el sorteo

## Decision

Decisión del consultor sobre el punto 1 de la rama `trabajo/entrada-marzo`. Se tomó cuando **no
hay material de marzo**: no hay ningún libro, tramo, manifiesto ni reparto de 2026-03, comprobado
solo por metadatos.

1. **Marzo entra por el camino de fidelidad (ADR-0036)**, con sorteo y con la misma puerta
   (`holdout.py`, ADR-0033).
   - Lo que caiga en `fidelidad-2` y `fidelidad-3` **queda oculto**.
   - Es la reserva que `knowledge/cases/fidelidad/config.yaml` dejó escrita el 2026-09-21:
     «`fidelidad-2` y `fidelidad-3` SE QUEDAN VACIAS A PROPOSITO, reservadas para material que pueda
     cargar una cifra de verdad -febrero o marzo, el mes limpio que sigue pendiente-».

2. **La parte `fidelidad-dev` de marzo es conjunto de MEDICIÓN de desarrollo, junto con mayo.**
   - **Aclara ADR-0043:** su «medida = mayo (y marzo cuando entre)» significa **solo la parte
     `fidelidad-dev` de marzo**, nunca sus días reservados.

3. **Los cupos de marzo son una REGLA fijada antes de ver marzo**, no cifras sueltas: todavía no se
   sabe cuántos días tendrá. Siendo N el número de casos del universo del artefacto:
   - `fidelidad-dev` = ⌊N / 3⌋;
   - `fidelidad-2` = ⌊(N − `fidelidad-dev`) / 2⌋;
   - `fidelidad-3` = N − `fidelidad-dev` − `fidelidad-2`;
   - `fidelidad-1` = 0, porque es de septiembre.

   **Qué es N.** Son los casos del universo: los días laborables del tramo de marzo que entran, con
   velas suficientes. No son los días del calendario. `asignar` deja fuera, en silencio, cualquier
   caso que no quepa en los cupos, así que los cupos tienen que sumar exactamente el universo, como
   hicieron los de septiembre.

   **Es una decisión de criterio del consultor:**
   - la medición de desarrollo es algo menor, porque mayo ya aporta la suya;
   - el holdout se reparte entre dos puertas.

   **Dónde vive.** La regla es un DATO de la configuración de fidelidad (ADR-0002), por mes
   (`cupos_por_mes`), y no una cifra en `src/`. El cálculo desde N se hace al sortear: es
   determinista y queda registrado en el `particiones.yaml` del artefacto. N = 0 se niega.

4. **Un artefacto `<simbolo>-AAAA-MM` limita su universo a ese mes.**
   - Hoy la configuración es una sola y su `cobertura_material` suma todos los meses, así que un
     artefacto de marzo se habría llevado también los 14 días de septiembre, medido.
   - Septiembre se reconstruye igual byte a byte, porque todos sus casos son de 2026-09.

5. **EL SORTEO NO SE REPITE NUNCA.** Un artefacto que ya se sorteó una vez no se vuelve a sortear:
   - ni con otra semilla;
   - ni borrando su carpeta;
   - ni después de un huso NO CONCLUYENTE.

   Repetir el sorteo sería buscar la semilla. Si el huso sale NO CONCLUYENTE:
   - el libro no se declara;
   - los días reservados siguen reservados;
   - los días `dev` esperan una decisión del consultor.

   `fidelidad build` se niega en cuanto el id tiene ancla, carpeta o cualquier commit en el
   historial.

6. **El orden de entrada** resuelve una circularidad entre ADR-0039 §5 y el sorteo, y lleva una
   **excepción acotada a ADR-0039 §1**:
   - a. **Aleks lee SOLO la columna de fechas, UNA vez, antes del sorteo**, y lo declara el mismo
     día en `docs/validation/HOLDOUT-EXPOSICIONES.md`. El tramo es la **intersección** de los días
     que salen con UTC y con Europe/Madrid, así que un día dudoso de borde no entra.
   - b. **Sorteo**, con los cupos de la regla del punto 3.
   - c. **Huso medido por velas** (ADR-0039 §5), con las filas `dev` que caen el mismo día con los
     dos husos, más el control.
   - d. **Declaración del libro** en `knowledge/corpus/libros.yaml`.
   - e. **Ingesta de los días `fidelidad-dev`.**

   **La excepción cubre solo** la columna de fechas, en una sola lectura, hecha por Aleks, antes de
   declarar el libro. Nada más del fichero.

7. **`casos ingerir --artefacto <id>` ingiere los días `fidelidad-dev` de un artefacto ya sorteado,
   anclado y commiteado.**
   - Sin sorteo, se niega.
   - Nunca toma un día reservado ni retirado (`casos_ocultos`).
   - Sin `--artefacto`, el comando hace exactamente lo de antes.

## Problema que resuelve

**Tres documentos decían tres cosas distintas sobre marzo** (paso 0 de esta rama):
- ADR-0025 §5, que entra por el kit como paquete nuevo;
- la configuración de fidelidad y PROJECT_STATE, que entra por el camino de fidelidad con su
  reserva;
- ADR-0043, que es medición de desarrollo, lo que se lee como todo `dev`.

Y el camino de fidelidad no sabía repartir un segundo mes:
- sus cupos eran los de septiembre, 4/10/0/0;
- su universo sumaba todos los meses con cobertura.

**La circularidad:**
- el huso solo se mide con filas `dev` (ADR-0039 §5);
- los días `dev` solo existen después del sorteo;
- el sorteo necesita el tramo de cobertura;
- el tramo sale de la columna de fechas;
- y leer la columna exige formato y huso: el tramo de mayo se leyó «con el formato y el huso de
  libros.yaml», según `knowledge/cases/kit/config.yaml`.

## Alternativas consideradas

- Marzo todo `dev`, por el camino dev-visto (ADR-0042).
- Marzo por el kit ciego, como decía ADR-0025 §5.
- Cupos fijos escritos hoy.
- Configuración separada por artefacto.
- Declarar el libro antes del sorteo, midiendo el huso con todas sus filas.

## Por que elegimos esta opcion

**El motivo de fondo: el material que puede ir al holdout es el recurso más escaso del proyecto.**
- Ningún reparto llega a las 36 unidades efectivas que pide F26.
- Mayo ya tiene su reserva en el kit.
- Septiembre llenó `fidelidad-1` y dejó `fidelidad-2` y `fidelidad-3` vacías esperando justo este
  mes.
- Un mes que el trader etiqueta y nosotros no hemos visto es lo único que puede llenarlas.

## Por que descartamos las demas

- **Dev-visto (ADR-0042).** Su segunda condición exige que la lectura completa del libro esté «ya
  declarada». Marzo no se ha leído entero, y declararlo leído sería falso. Además gastaría toda la
  reserva en desarrollo.
- **El kit ciego. Enmienda de ADR-0025 §5.** Marzo no entra por el kit porque el backtest lo hace
  el propio trader: ese material no es ciego para él, y ADR-0036 §1 lo saca del kit.
- **Cupos fijos hoy.** No se sabe cuántos días tendrá el tramo, y unos cupos que no suman el
  universo dejan casos fuera en silencio.
- **Configuración por artefacto.** Es un cambio mayor que el filtro por el mes del id, y el filtro
  basta.
- **Declarar antes del sorteo con todas las filas.** Leería las filas de días que van a quedar
  reservados. Es justo lo que ADR-0039 §5 limita a las filas `dev`.

## Impacto

- **ADR-0025 §5 queda enmendado.** ADR-0043 queda aclarado para marzo. ADR-0039 §1 gana la
  excepción del punto 6. Los tres llevan una nota que remite aquí, sin reescribir su cuerpo.
- **`knowledge/cases/fidelidad/config.yaml`** gana `cupos_por_mes` con la regla de 2026-03. Sus
  cifras de septiembre no cambian.
- **`knowledge/cases/criterio_fidelidad.yaml`** dice que marzo entra en medida solo con su parte
  `fidelidad-dev`. Ninguna cifra cambia.
- **El código:**
  - `fidelidad.construir` filtra por el mes del id y calcula los cupos desde N;
  - `fidelidad.escribir` se niega a repetir un sorteo;
  - `casos ingerir` gana `--artefacto`.
- **El runbook de entrada** es `docs/runbooks/ENTRADA-MARZO.md`.

## Fecha / fase

2026-09-24, post-F14, rama `trabajo/entrada-marzo`.

## Estado

ACTIVE
