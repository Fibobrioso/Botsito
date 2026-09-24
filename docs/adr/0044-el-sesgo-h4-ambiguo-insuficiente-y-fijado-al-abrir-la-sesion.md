---
status: ACTIVE
date: 2026-09-24
phase: post-F14 (rama `trabajo/motor-sesgo-h4`)
---

# 0044 · El sesgo H4: ambiguo, insuficiente, y fijado al abrir la sesión

## Decision

RN-003 dice que el sesgo es el de la vela H4 previa cerrada, que cambia solo si esa vela rompió
el extremo de la anterior, que basta con la mecha y que un equal no lo cambia. Deja cuatro cosas
sin definir, medidas en el paso 0 de `docs/validation/MOTOR-SESGO-H4.md`. El consultor decide:

1. **Si la vela previa rompe LOS DOS extremos de la anterior, el sesgo es AMBIGUO en esa sesión,
   y con sesgo ambiguo no se opera.** Queda abierta **A-34**, que es una pregunta para el trader:
   «vela H4 previa que rompe ambos extremos: ¿qué sentido toma el sesgo?».
2. **El estado inicial.**
   - Se busca hacia atrás la última H4 que rompió un extremo de su anterior, con un tope de
     `sesgo_h4_tope_velas` velas H4.
   - Si no hay ninguna, el sesgo es **INSUFICIENTE** y no se opera.
   - El tope es una decisión **provisional del proyecto, no del trader**. Vive en
     `parametros.yaml` con fuente este ADR, y su valor inicial es 60.
3. **El sesgo se fija AL ABRIR la sesión operativa y no cambia dentro de ella** (RN-003,
   `cuando: abre una sesión operativa`).
   - Solo cuentan las H4 cuyo **fin** es anterior o igual a la apertura de la sesión.
   - En las semanas en que la UE y EE. UU. no cambian la hora el mismo día, la H4 que cierra a
     mitad de sesión cuenta desde la sesión siguiente.
   - La firma es `sesgo_h4(velas_h4, apertura_sesion)`, no un instante cualquiera.
4. **Romper es superar el extremo por al menos 1 punto (0,00001).** Una diferencia de 0 es un
   equal, y no rompe.
   - **Anotado sobre A-16:** las series del trader y las nuestras difieren 1-2 puntos, así que una
     ruptura de 1-2 puntos puede serlo en una serie y no en la otra.

**Salidas posibles:** alcista, bajista, ambiguo e insuficiente.

**Cómo se implementa:**
- **Qué vela cuenta como cerrada:** la que tiene su hora de fin anterior o igual a la apertura, y
  no la marca `completa` de la agregación, que depende de cuántas M1 recibe.
- **Dónde vive:** el sesgo va en el dominio (`src/botsito/domain/sesgo.py`), sobre velas ya
  agregadas. La agregación con huso se queda en `data`.
- **Las cifras no van en el código** (ADR-0002): el tope y el criterio de ruptura se leen del
  registro.

## Problema que resuelve

Sin estas cuatro decisiones, cualquier implementación del sesgo las habría tomado en silencio:
- una vela que rompe por los dos lados;
- un histórico sin ninguna ruptura;
- una H4 que cierra a mitad de sesión;
- qué cuenta como romper.

Y las cuatro cambian qué días opera el bot.

## Alternativas consideradas

- Ante una ruptura doble, tomar el sentido del cierre de la vela.
- Sin ruptura en el histórico, un sesgo por defecto.
- Recalcular el sesgo en cada instante.
- Exigir más de un punto para romper.

## Por que elegimos esta opcion

- **Es la lectura literal de RN-003** donde RN-003 habla: el sesgo se fija al abrir la sesión, y
  basta la mecha.
- **Es la más conservadora donde no habla:** con ambiguo o insuficiente no se opera. Así no se
  inventa un sentido que el trader no ha dado, y lo que falta se pregunta (A-34).

## Por que descartamos las demas

- **El sentido del cierre** es exactamente el criterio que las notas de RN-003 descartan: «el
  color de la vela NO decide».
- **Un sesgo por defecto** es una decisión del trader que el trader no ha tomado.
- **Recalcular en cada instante** contradice el `cuando` de RN-003.
- **Más de un punto para romper** contradice el literal: «al menos por un pip o una milésima de
  pip». Nuestra resolución es un punto.

## Impacto

- **La spec:**
  - RN-003 recoge las cuatro decisiones en su texto;
  - `parametros.yaml` gana `sesgo_h4_tope_velas`;
  - `ambiguedades.yaml` gana A-34.
- **El código:** el dominio gana el sesgo, con tests sintéticos, entre ellos los de cambio de hora
  de EE. UU.
- **El diagnóstico** sobre abril y agosto es solo eso: no cambia la regla.

## Fecha / fase

2026-09-24, post-F14, rama `trabajo/motor-sesgo-h4`. Next Action 19.

## Estado

ACTIVE
