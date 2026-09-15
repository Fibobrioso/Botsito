---
status: ACTIVE
date: 2026-09-12
phase: F13
---

# 0022 · El bot no opera noticias en la cuenta fondeada, y una ambigüedad puede cerrarse por decisión

## Decision

1. **El bot NO opera alrededor de noticias de alto impacto en su primera versión.** No porque la
   estrategia falle ahí —no falla— sino porque **la cuenta a la que va destinado puede prohibirlo**
   como norma, y el coste de incumplirla es perder la cuenta aunque la operación acabe en profit.
2. **La capacidad se conserva.** `filtro_noticias` sigue siendo un enum con `no` (no filtra, que es
   lo que el trader hace en sus cuentas propias) y `regla` (filtra). La primera versión corre con
   `regla`; el día que el bot opere en una cuenta que lo permita, se cambia el valor y nada más.
3. **`filtro_noticias` pasa a `regla` y su fuente pasa a ser este ADR**, no el feedback del trader.
   El trader dijo lo contrario —*"a mí me es indiferente si hay noticia o no […] Sí, incluimos
   noticias"*— y esa frase sigue siendo verdad sobre SU operativa: se conserva donde estaba.
4. **RN-021 se parte en dos**, porque hoy dice dos cosas y solo una sigue siendo cierta para el bot:
   el spread sigue sin filtro (lo dijo el trader) y las noticias pasan a **RN-028**, una regla de
   clase `gate` que prohíbe abrir, con `decision: ADR-0022`.
5. **RN-028 nace con `pendiente_definicion: A-17`**: sabemos QUE se bloquea y no CON QUÉ VENTANA,
   porque nadie ha leído todavía el reglamento de FundedNext.
6. **A-17 se parte en dos** (lo pide el consultor el 2026-09-12):
   - **A-17** se queda con la VERIFICACIÓN, que es un hecho y no una decisión: qué prohíbe
     exactamente el reglamento, con qué ventana antes y después, y qué sanción. Sigue **ABIERTA**.
   - **A-22** nace con la DECISIÓN de alcance —bloquear en la v1, conservar la capacidad— y queda
     **DECIDIDA** por este ADR.
7. **Nace el estado `DECIDIDA`** para las ambigüedades. Es lo que faltaba: una ambigüedad de
   alcance, método o herramienta la cierra el consultor, y hasta hoy el fichero solo admitía
   cerrarlas con feedback del trader.

## Problema que resuelve

Son dos problemas que se cruzaron el mismo día.

**El de negocio.** La spec dice hoy, con la voz del trader y sin asterisco, que se opera durante las
noticias (RN-021, `filtro_noticias: no`). Es cierto para él: opera cuentas propias que no lo
prohíben y su estrategia funciona dentro de esos eventos. **Pero el bot no va a una cuenta propia**,
va a una cuenta fondeada, y ahí puede ser una norma cuya sanción es perder la cuenta. El propio
trader lo avisó, y RN-021 lo lleva escrito en sus notas desde F11: *"el propio trader avisa de que
la cuenta de fondeo puede prohibirlo y cerrar la cuenta aunque se acabe en profit. Verificar antes
de operar en real"*. Ese aviso llevaba tres días esperando en un campo de notas que ninguna guardia
mira.

**El de método.** A-17 mezclaba una decisión con una verificación, y ninguna de las dos se podía
cerrar: el fichero de ambigüedades solo admite cerrarlas con un registro del trader, y esto no lo
decide él. Lo mismo le pasa a A-15 y A-16 desde el 2026-09-09, y la auditoría de proceso del
2026-09-12 lo levantó: *"cuatro documentos dicen que sólo cierra el trader; uno dice que A-15 cierra
por ADR; el código solo conoce dos estados"*.

## Impacto

- **El bot deja de abrir operaciones alrededor de noticias**, y no podrá hacerlo de verdad hasta que
  A-17 diga con qué ventana: RN-028 lo declara con `pendiente_definicion`, que es el mecanismo que
  F12 creó para una regla vigente cuya condición nadie ha definido todavía.
- **La fidelidad de F26 tendrá una divergencia CONOCIDA Y DECLARADA**: si el trader operó en una
  noticia y el bot se abstuvo, no es un fallo del bot, es esta decisión. F26 la cita.
- **`filtro_noticias` cambia de dueño**: pasa de citar al trader a citar este ADR, que es lo que
  ADR-0016 exige cuando una regla dice más que su literal.
- **Nace `DECIDIDA`** con sus tres guardias: el ADR existe, el ADR **nombra** la ambigüedad, y no
  vale sobre una `bloqueante` ni sobre una que sostenga el `ambiguedad_id` de un parámetro (si el
  bot corre con un default nuestro por culpa de esa pregunta, no la cierra una decisión).
- `spec status` gana una sección: *"Cerradas por decisión del consultor (no las respondió el
  trader)"*. Sin ella, `DECIDIDA` sería invisible.

## Alternativas consideradas

1. **Bloquear las noticias y conservar la capacidad** (elegida).
2. **Dejarlo como está** y confiar en que el reglamento lo permita.
3. **Bloquear y borrar la opción `no`**, simplificando el enum.
4. **Esperar a verificar el reglamento** antes de decidir nada.

## Por que elegimos esta opcion

Porque el riesgo es asimétrico y no hace falta saber la ventana exacta para saber de qué lado hay
que equivocarse. Si bloqueamos de más, perdemos algunas operaciones y F26 lo medirá como
divergencia declarada. Si operamos de menos y la norma existe, se pierde la cuenta entera, con lo
que cuesta conseguirla. Y conservar la opción `no` no cuesta nada: el enum ya la tenía.

## Por que descartamos las demas

- **(2) Dejarlo como está**: es lo que el propio trader avisó que no hiciéramos, y el aviso llevaba
  tres días en un campo de notas sin que ninguna guardia lo mirara.
- **(3) Borrar la opción `no`**: destruiría información cierta. El trader **sí** opera noticias, su
  estrategia funciona dentro de ellas, y el día que el bot corra en una cuenta propia esa es la
  configuración correcta. Borrarla obligaría a reabrir la decisión con el corpus ya frío.
- **(4) Esperar a verificar**: el reglamento se lee en F33, meses después de que F22 implemente las
  reglas. Esperar significaría escribir el motor con el comportamiento equivocado y corregirlo
  luego, que es exactamente lo que ADR-0021 y ADR-0020 costaron.

## Fecha / fase

2026-09-12, F13 (decisión del consultor, con el matiz que él mismo aportó: la estrategia funciona
dentro de las noticias; lo que cambia es dónde corre el bot).

## Estado

ACTIVE

## Enmienda del 2026-09-14 (ADR-0026)

**Este ADR partió de un supuesto que era cierto para una cuenta y no para la que se ha elegido.**
Decía que el bot no opera noticias porque la cuenta fondeada «puede prohibirlo» dos minutos antes y
después y cerrarla aunque la operación acabe en profit. El cuerpo de arriba no se reescribe —igual
que se hizo con `Operativa_Cerrada.md`—; lo que cambia se dice aquí.

1. **El supuesto se verificó el 2026-09-14, y es correcto para dos cuentas:**
   - **FTMO Standard**, en la cuenta fondeada: *«it is not permitted to open or close any trades
     [...] within a time window starting 2 minutes before and ending 2 minutes after the release of
     selected news announcements»*; la ejecución de un stop o un objetivo dentro de la ventana cuenta
     como infracción, y la sanción puede ser terminar la cuenta.
   - **FundedNext**, con otra forma: recorta el 40 % del beneficio de lo operado entre 5 minutos
     antes y 5 minutos después de una noticia de alto impacto correlacionada.
2. **ADR-0026 elige un tipo de cuenta sin esa restricción**: FTMO 2-Step **Swing**, que *«have no
   restrictions on trading during news releases»*. El motivo de este ADR desaparece.
3. **En consecuencia:**
   - **`filtro_noticias` vuelve a `no`**, que es lo que hace el trader y lo que dice su registro
     (`fb-2026-09-09-sesion-01-3565552d`). Su fuente sigue siendo una decisión —ADR-0026—, porque
     la norma es de la cuenta y no de la operativa.
   - **RN-028 pasa a `DESCARTADA`**, con nota que cita ADR-0026, y pierde su `forma`: una regla
     descartada no se ejecuta y su `pendiente_definicion` apuntaba a una ambigüedad que ya no está
     abierta.
   - **A-17 queda CERRADA como DECIDIDA por ADR-0026**: la verificación está hecha y el tipo de
     cuenta la vuelve irrelevante.
   - **A-22 sigue DECIDIDA por este ADR, con el sentido invertido**: el bot SÍ opera noticias en la
     cuenta elegida. La decisión de alcance que A-22 recogía —bloquear en la v1— se revoca aquí, y
     la otra mitad —conservar la capacidad— sigue en pie.
   - **La divergencia declarada de F26 desaparece**: si el trader operó una noticia, el bot también
     tiene que hacerlo.
4. **La capacidad se conserva.** El día que el bot corra en una cuenta con restricción de noticias,
   se cambia `filtro_noticias` a `regla`, se revive RN-028 y hace falta el calendario económico.
   Eso queda como **precondición del pre-vuelo de F33**, no como funcionalidad abierta hoy.
