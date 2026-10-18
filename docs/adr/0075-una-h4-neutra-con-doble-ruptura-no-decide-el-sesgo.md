---
status: ACTIVE
date: 2026-10-11
phase: post-F14 (rama `trabajo/activar-sesion-04-motor`, R1.1 de la hoja de ruta)
---

# 0075 · Una H4 neutra con doble ruptura no decide el sesgo: se mantiene el anterior (enmienda ADR-0060 §1 y §2)

> Decisión del consultor del 2026-10-11 (respuesta a la PARADA de `trabajo/activar-sesion-04`,
> punto 1, y encargo de `trabajo/activar-sesion-04-motor`, decisión 2). **Enmienda ADR-0060 §1 y
> §2** (recuadro allí y fila del índice). Lo dijo el trader en la sesión 4, S-13.

> **ENMIENDA (2026-10-17, rama `trabajo/sesgo-h4-color`, ADR-0080).** En §3, «con un solo extremo
> roto el color no decide (RN-003)» queda sustituido: por WhatsApp (2026-10-14,
> `fb-2026-10-04-sesion-04-6e7da456`) el trader dijo que una H4 cambia el sesgo solo si rompe el
> extremo de la anterior Y cierra del color de esa ruptura; la que cierra del color contrario no
> decide y la búsqueda sigue, igual que la neutra de este ADR. §1 y §2 no cambian; la neutra de
> doble ruptura sigue sin decidir, y desde ADR-0080 el motor la cuenta (`saltadas_neutras_dobles`).

## Decision

### 1. La vela neutra no decide

Si la H4 que rompe **los dos** extremos de su anterior cierra **exactamente donde abrió**
(`cierre == apertura`: sin cuerpo, sin color), **no fija el sesgo**: la búsqueda hacia atrás de
ADR-0044 §2 la salta y sigue en la H4 anterior, como si no hubiera roto nada. El sesgo de la sesión
es el de la última H4 que sí rompió un extremo con lado -por un solo extremo, o por los dos con
color-; si ninguna lo hizo dentro de `sesgo_h4_tope_velas`, `insuficiente` (ADR-0044 §2, ADR-0060
§3). Es lo que el trader respondió en S-13 (v10 1:40:05–1:40:40): «si esta es una vela neutra, no
tiene ningún color, nosotros seguiríamos operando alcistas esto es con la única condición con la
condicional de si éste es una vela neutra o sea no tiene color» (`ev-v10-014005-7e2228f4`); y con
color, el color: «si es una vela roja entonces nuestro sesgo sería bajista … si esta vela termina en
color verde entonces nuestro sesgo sería alcista» (`ev-v10-014040-fb7a153b`), que es ADR-0060 §1 y
no cambia.

- **Neutra es cierre igual a apertura, exacto.** No hay umbral en H4: el trader dijo que con un
  cuerpo «muy pequeño, de uno o dos puntos» ya cuenta el color (SESION-04-EXTRACCION.md §3.14,
  v10 1:41:01–1:41:29, citado allí sin ítem de evidencia). Es lo que `domain/sesgo.py` ya
  comparaba; lo que cambia es qué hace cuando son iguales.
- **El motor ya no produce `ambiguo`.** Con esta decisión ninguna vela da `ambiguo`: el token se
  queda declarado en la spec (`tokens.ambiguo`, los `valores` del hecho `sesgo`, la forma de
  RN-033) y en `Sesgo.AMBIGUO`, porque lo nombran la forma de RN-033, los scripts de diagnóstico y
  el visor, con la descripción diciendo que el motor no lo produce desde este ADR. Retirarlo es
  deuda (G.2 de la hoja de ruta, líneas del cierre). RN-033 queda para `insuficiente`; su forma y
  su cita no cambian, y la prohibición de operar sin lado sigue saliendo de ADR-0044 §1 y
  ADR-0049.
- **Dos reservas, escritas también en las notas de RN-003:** (1) el trader lo dijo con un sesgo
  previo ALCISTA («seguiríamos operando alcistas») y el caso bajista se deduce: su confirmación
  está en la lista de la sesión 5 (ACTIVAR-SESION-04.md §5; R4.1); (2) lo dijo «suponiendo que …
  no haya otro rango mayor» (SESION-04-EXTRACCION.md §3.14): la búsqueda hacia atrás de ADR-0044
  §2 es la que da «el rango anterior», y no se toca.

### 2. Lo que enmienda de ADR-0060

- **§1**, «La vela con doble ruptura fija el sesgo: la búsqueda hacia atrás de ADR-0044 §2 para en
  ella»: vale solo para la doble ruptura CON color. La neutra no para la búsqueda.
- **§2**, la decisión nocturna «la doble ruptura de una vela SIN CUERPO sigue siendo `ambiguo`»:
  queda sustituida por la respuesta del trader. ADR-0060 descartó esta misma lectura (su
  alternativa 1, «seguir buscando hacia atrás») porque «inventa un sesgo que ninguna vela dio»; hoy
  no lo inventa nadie: lo dijo el trader, y es lo que ADR-0060 §2 dejó como pregunta para la
  sesión 4.

### 3. Lo que no cambia

El color decide con doble ruptura (ADR-0060 §1); con un solo extremo roto el color no decide
(RN-003); `sesgo_h4_tope_velas` e `insuficiente` (ADR-0044 §2, ADR-0060 §3); el sesgo se fija al
abrir y caduca al abrir (ADR-0044 §3, ADR-0049); la forma de RN-033.

## Problema que resuelve

ADR-0060 §2 conservó `ambiguo` para un caso que el trader no había descrito y lo dejó como pregunta
para la sesión 4. El trader lo describió (S-13).

## Alternativas consideradas

1. La neutra no decide y la búsqueda sigue hacia atrás (la elegida).
2. Conservar `ambiguo` para la neutra (ADR-0060 §2).
3. Retirar el token `ambiguo` de la spec y del dominio.

## Por que elegimos esta opcion

Es lo que dijo el trader, «con la única condición» y sin dudar; el mecanismo (la búsqueda hacia
atrás) ya existe.

## Por que descartamos las demas

- La 2 contradice la respuesta del trader.
- La 3 toca la forma de RN-033 y lo que los scripts y el visor enseñan, sin que nada del trader lo
  pida: es deuda, no parte de esta decisión.

## Impacto

- **Código:** `src/botsito/domain/sesgo.py` (la rama de la doble ruptura sin cuerpo pasa a
  `continue`).
- **Spec:** CORRECT sobre RN-003 (`fb-2026-10-04-sesion-04-ca0afae6`, el registro de S-13), que pasa a ser
  su `cita` como ADR-0060 §6 hizo con el CORRECT de la sesión 3; el `entonces` y las notas de
  RN-003; las notas de RN-033; las descripciones de `sesgo_h4_al_abrir`, del token
  `sentido_de_la_ruptura`, del token `ambiguo` y del hecho `sesgo`. `spec_version` 15.9.9 →
  **16.0.0**: una regla cambia de sentido.
- **Tests:** `tests/unit/test_sesgo_h4.py` (`test_doble_ruptura_sin_cuerpo_es_ambiguo` cambia de
  sentido a propósito, y dos nuevos: dos neutras seguidas y una neutra tras sesgo bajista);
  `tests/unit/test_huecos_motor.py` (H1: lo que fijaba `ambiguo` con `ambos_sin_cuerpo` cambia de
  sentido a propósito; RN-033 sigue prohibiendo con un `sesgo` puesto a mano en `ambiguo`, que es
  lo que su forma congela).
- **Sin arnés y sin medida sobre material**: todo con velas sintéticas.

## Fecha / fase

2026-10-11 · rama `trabajo/activar-sesion-04-motor` (R1.1). Informe:
`docs/validation/ACTIVAR-SESION-04-MOTOR.md`.

## Estado

ACTIVE
