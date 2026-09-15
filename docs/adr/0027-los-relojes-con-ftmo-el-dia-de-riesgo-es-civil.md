---
status: ACTIVE
date: 2026-09-14
phase: post-F13
---

# 0027 · Los relojes con FTMO: el día de riesgo es el día civil del trader

## Decision

1. **El corte del día de riesgo es 00:00 CE(S)T**, que es el mismo huso civil que `huso_operativa`
   (`Europe/Madrid`). FTMO lo escribe así: el límite diario es *«Account balance at midnight CE(S)T
   of the previous day – 5% of the Initial Simulated Capital»*. `reloj_dia_riesgo` deja de valer
   `servidor` y pasa a valer `civil_operativa`, que es opción nueva del enum.
2. **Eso elimina el tercer reloj.** Quedan dos: el civil del trader (ventana operativa y día de
   riesgo) y el del servidor del bróker (rejilla de velas). ADR-0015 decía que «el día de riesgo
   necesita el suyo»; con FTMO coincide con el del trader, y este ADR lo enmienda.
3. **El reloj del servidor de FTMO es «GMT+2 +DST»** en MT4/MT5 según su ficha de cuenta, igual en
   forma al de FundedNext. **La ficha no dice qué calendario de horario de verano sigue**, así que
   `broker_offset_base` y `broker_dst` no se heredan: pasan a UNKNOWN bajo **A-28** y se miden en la
   demo de FTMO. Comprobar el calendario exige observar una transición, así que A-28 no se cierra
   antes del cambio de hora de octubre.
4. **`anclaje_h4` = `17:00 America/New_York` se mantiene** como decisión de ADR-0017, y se
   **verifica** contra la rejilla H4 real del servidor de FTMO en la misma medición. Si no coincide
   —por ejemplo, si el servidor cambia de hora con el calendario europeo—, se abre una ambigüedad y
   el valor no se toca por su cuenta.
5. **A-19 queda CERRADA como DECIDIDA**, con este ADR como `decision`. Era una verificación y no un
   juicio del trader, y el reglamento la contesta.
6. **La semana de riesgo del trader corta con el mismo reloj.** `perdida_maxima_semanal` es un freno
   del trader, no de la firma (FTMO no tiene tope semanal), y su acumulador reinicia con
   `reloj_dia_riesgo`: desde hoy, en hora civil de `huso_operativa`.

## Problema que resuelve

A-19 preguntaba en qué reloj cae la medianoche que reinicia el tope diario, y `reloj_dia_riesgo`
corría con un default nuestro (`servidor`) que ADR-0015 justificó como «como lo calculan las
cuentas de fondeo», sin verificar. Con la firma elegida (ADR-0026) la respuesta está escrita en su
reglamento, y es la contraria: la medianoche es civil centroeuropea, no la del servidor.

Mantener el default habría desplazado el corte una hora todo el año respecto al que usa FTMO
(servidor GMT+2/+3 frente a CET/CEST, que va a GMT+1/+2) y, en una cuenta fondeada, equivocarse en
el corte cuesta la cuenta.

## Alternativas consideradas

1. **Corte en `civil_operativa`, que coincide con CE(S)T** (elegida).
2. **Mantener `servidor`** hasta medirlo en el panel.
3. **Un parámetro de huso propio para la firma** (`firma_huso_corte = Europe/Prague`), separado de
   `huso_operativa`.

## Por que elegimos esta opcion

Porque es lo que dice el reglamento, y porque coincide con un reloj que el proyecto ya tiene y ya
verificó empíricamente: la observación de invierno de la auditoría del material (enero de 06 a 13
UTC, abril y agosto de 05 a 12 UTC) confirma que el trader vive en hora civil centroeuropea.

## Por que descartamos las demas

- **(2) Mantener `servidor`**: contradice el texto del reglamento, y el panel no aporta nada que el
  reglamento no diga ya sobre el corte. Lo que sí hay que medir —el reloj del servidor— no decide
  el corte.
- **(3) Huso propio para la firma**: CE(S)T y `Europe/Madrid` tienen hoy las mismas reglas de horario
  de verano, así que serían dos puertas para el mismo instante (ADR-0002). Si algún día divergen, o
  el trader cambia de huso, se abre ambigüedad y se separan; la opción `civil_operativa` lo nombra
  para que ese día se vea.

## Impacto

- `reloj_dia_riesgo`: `servidor` → `civil_operativa`, DEFAULT_AMBIGUOUS → CONFIRMED, fuente
  ADR-0027, sin `ambiguedad_id`. A-19: ABIERTA → DECIDIDA. Se tocan los cuatro sitios que avisa el
  HANDOFF: el registro, `ambiguedades.yaml`, la regla que la citaba (RN-020, que deja de nombrar
  `broker_dst` y `broker_offset_base`) y la tabla de PROJECT_STATE, más el test de `test_kit` que
  congela qué ambigüedades están cerradas.
- **Coincidencia afortunada, y declarada**: `base_calculo_perdida_diaria: saldo_inicial_dia` (del
  trader) y la fórmula de FTMO (saldo a medianoche CE(S)T) coinciden en forma. Lo que NO coincide es
  el porcentaje ni la base del porcentaje (ADR-0026, impacto). Está escrito en la descripción del
  parámetro, no se da por obvio.
- MASTER_PLAN H.2 decía «5 % diario sobre equity a medianoche de servidor» y «F31: día de riesgo =
  día de servidor»: se corrigen citando este ADR y ADR-0026.
- La medición en la demo de FTMO es trabajo del dueño y bloquea a F24 y F33, no a esta rama.

## Fecha / fase

2026-09-14, después de F13 (decisión del consultor sobre el reglamento leído ese día).

## Estado

ACTIVE

Enmienda ADR-0015 (el día de riesgo ya no necesita un reloj propio) y confirma ADR-0017.
