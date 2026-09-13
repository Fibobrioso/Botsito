# Las tres decisiones del consultor que quedaban — INFORME DE VALIDACIÓN

**Rama:** `trabajo/ambiguedades-del-consultor` (rama de trabajo sin número propio, MASTER_PLAN §F)
**Cierre previsto:** tag `stable/F13-decisiones`
**Decisiones:** ADR-0024 y ADR-0025
**Estado:** WAITING_FOR_USER_VALIDATION

---

## 1. Por qué existe esta rama

F13 construyó el estado `DECIDIDA` —la forma de cerrar una ambigüedad que decide el consultor y no
el trader— y dejó **expresamente fuera de su alcance** usarlo (brief de F13 §4). Esta rama lo usa,
y de paso cierra la decisión que bloqueaba abrir F14.

Dejarlas abiertas no era neutral. `cases/cuestionario.py` mete **toda** ambigüedad `ABIERTA` en el
cuestionario de la sesión siguiente, así que el próximo `kit build` le habría vuelto a preguntar al
trader dos cosas que ya estaban decididas desde el 2026-09-09.

## 2. Qué se decidió

| | Decisión | Dónde |
|---|---|---|
| **A-15** | La ventana operativa se queda en 07-11 y 11-15. **No se amplía a Nueva York** en esta fase. `DECIDIDA` | ADR-0024 |
| **A-16** | **Se parte en dos**, porque mezclaba una decisión con una medición | ADR-0024 |
| **A-23** (nace) | La referencia para medir fidelidad es **Dukascopy**; MT5/FundedNext para spread, ejecución, reloj de servidor y paridad; la divergencia entra en F26 como **margen declarado**. `DECIDIDA` | ADR-0024 |
| **Reparto de mayo** | **No se reparticiona**: 6 días `dev` y 13 de holdout (6/4/3). Junio sale del universo de F14 | ADR-0025 |

## 3. Lo que cambió respecto a lo que se iba a hacer

Se entró a cerrar A-15 y A-16 enteras. **A-16 no se podía cerrar.**

Su pregunta literal es cómo se comparan decisiones tomadas sobre velas de **Oanda** (FX Replay, que
es donde el trader decide) con un bot medido sobre **Dukascopy**. El anexo del 2026-09-09
(`anexos/A-16-proveedor-de-datos-2026-09-09.md`) midió una pareja **distinta** —MT5/FundedNext
contra Dukascopy, 2 puntos de mediana una vez corregido el reloj de servidor— y lo dice él mismo
sin ambigüedad:

> *"Queda una tercera fuente en juego, que es la del trader: él backtestea en FX Replay, que usa
> datos de Oanda. Esta medición no la cubre."*

Cerrarla con ese anexo habría sido afirmar más de lo que la evidencia sostiene. Así que se partió,
con el mismo corte que ADR-0022 le hizo a A-17 tres días antes y por el mismo motivo: **la decisión
la cierra el consultor, la medición la cierra F26**.

La diferencia no es formal. Si A-16 se cerrara entera, la obligación de medir la divergencia
Oanda/Dukascopy viviría dentro de la prosa de un ADR — que es exactamente donde el aviso de RN-021
sobre las noticias vivió tres días sin que ninguna guardia lo mirara. Ahora vive en una ambigüedad
abierta, con `resuelve_en: F26`, que `spec status` y el cuestionario enseñan solos.

**Y A-15 resultó más simple de lo que parecía.** No era una pregunta que el trader se reservara: es
una que **devolvió**. *"Por ahora vamos a trabajarlo en esas dos sesiones. Aunque si quieres
incluir Nueva York como te digo, pues lo puedes hacer. O sea, por mí no hay problema"*
(`ev-v6-014610-597e442a`) y *"puedes buscar las operaciones donde sea, o sea, no hay problema"*
(`ev-v6-014623-f23c5f63`). Una pregunta que el trader devuelve no se cierra esperando su respuesta.

## 4. El reparto de mayo: decir que no a cuatro días

La tentación era obvia y todavía legítima —**no existe ni un solo `LABEL_CASE`**, comprobado— :
repartir de nuevo los 19 días de mayo para tener diez días de desarrollo en vez de seis.

Se decidió que no, y el canje está escrito en ADR-0025. `particiones.yaml` **no está exento** de
reproducirse byte a byte ni siquiera con la sesión celebrada, y `cases/paquete.py` dice por qué:
*"es la prueba de que las particiones se fijaron antes de etiquetar"*. Repartir otra vez convierte
esa prueba en una afirmación que hay que creerse.

A cambio de cuatro días de un mes **que ya está expuesto** —su PnL diario entero se vio el
2026-09-11— y que por eso nunca va a ser la partición limpia de la que salga la cifra de F26.

Hay además un motivo mecánico que cierra la puerta: `cases/paquete.py` compara el `config` que el
paquete guardó contra el `config.yaml` de hoy. Tocar los cupos no rompe "los cupos": rompe la
comprobación de la sesión 1 entera.

## 5. Qué debe decidir el usuario

1. **Validar esta rama** y ordenar el merge con `stable/F13-decisiones`.
2. **Mandarle el mensaje a Jonathan** pidiendo febrero o marzo de 2026. Después de ADR-0025 no es
   "conveniente": es la **única** vía para que la biblioteca crezca sin tocar nada sellado.
3. Nada más. F14 queda desbloqueada.

## 6. Cómo comprobarlo

```
uv run botsito spec status      # A-15 y A-23 bajo "cerradas por decision del consultor"
                                # ventana_inicio y ventana_fin YA NO figuran "en revision"
uv run botsito kit check --sesion 2026-09-09-sesion-01   # exit 0: el paquete sigue intacto
make check
```

Y leer los dos ADR, que son cortos. El de A-16 tiene el argumento que más se va a reutilizar:
cuándo una pregunta se puede cerrar decidiendo y cuándo hay que medirla.

## Estado
WAITING_FOR_USER_VALIDATION
