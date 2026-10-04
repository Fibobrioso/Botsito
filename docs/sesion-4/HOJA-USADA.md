# La hoja que se llevó a la sesión 4 (2026-10-04)

Rama `trabajo/sesion-04`. Escrita el 2026-10-04 desde las decisiones del consultor de los días
2026-10-03 y 2026-10-04, que están copiadas en el encargo (`docs/encargos/trabajo-sesion-04.md`,
«La hoja que se llevó»). **No lleva ninguna cita del trader**: la hoja de papel, con las notas de
Aleks, no va al repositorio, y la fuente de cada respuesta es la voz (v10), no la hoja
(`docs/runbooks/SESION-DE-PREGUNTAS.md`).

## 1. Los códigos de voz

S-1 a S-24, dichos en voz como «pregunta ese siete» … «fin de pregunta». S-n es la pregunta n de
`docs/sesion-4/PREGUNTAS.md`; S-23 y S-24 son nuevas y no están en ese documento.

Estos S-n **no son** los de la sesión 3: allí S-1 era «cómo decide el sesgo del día». Por eso
`scripts/transcribir_sesion.py` guarda los textos POR SESIÓN (`CODIGOS_DE_SESION_TEXTO["03"]` y
`["04"]`) y la hoja con la que se agrupa la filtrada se elige con `--sesion`.

| código | título | n.º en PREGUNTAS.md | ambigüedad o fuente |
|---|---|---|---|
| S-1 | Cuándo pones la orden, una vez formado el mínimo (o máximo) en M1 | 1 | A-49 (F35 §5.2); subpregunta de A-49 |
| S-2 | Cuándo un mínimo de M1 se convierte en tu punto de breaker | 2 | A-49 y F de Next Action |
| S-3 | El stop al poner la orden: ¿en el 1 o en el 0,8? | 3 | A-18; subpregunta de A-18 |
| S-4 | Si el precio sube más antes de llenarse, ¿se mueve el 1 de la caja? | 4 | A-49 (decisión 5 del ADR de F35, `caja_se_fija`) |
| S-5 | La orden sin llenar al acabar la sesión o la ventana | 5 | A-30 y A-39; subpregunta de A-39 |
| S-6 | «Lo mínimo posible» al redondear el stop: ¿un punto o un pip entero? | 6 | ADR-0061 §2 (sin ambigüedad) |
| S-7 | Con qué reloj empiezas a las 7 en invierno | 7 | A-42 |
| S-8 | Qué corta la racha de 9 pérdidas y cuándo vuelves a operar | 8 | A-51 |
| S-9 | El tope de pérdida: ¿porcentaje o 9 seguidas? | 9 | A-44 |
| S-10 | Zona limpia | 10 | A-21 |
| S-11 | El alto de M15 que el precio supera un poco | 11 | A-35 |
| S-12 | Las salidas por encima de 3 R | 12 | G-2 de la sesión 3 y A-33 |
| S-13 | La vela de 4 horas que rompe por los dos lados y cierra sin cuerpo | 13 | ADR-0060 §2 (sin ambigüedad) |
| S-14 | El umbral de la vela casi plana | 14 | RN-007 (E-3 de la sesión 3) |
| S-15 | Una liquidez tomada antes de las 7 | 15 | A-43 |
| S-16 | Cuál de tus dos backtests de agosto vale | 16 | E-1 de la sesión 3 |
| S-17 | Si solo el 0 de la caja cuenta frente al nivel tomado | 17 | A-50 |
| S-18 | Los intentos: ¿por marca o por toma? | 18 | A-25; subpregunta de A-25 |
| S-19 | Las 7 capturas que venían con el backtest de marzo | 19 | `docs/validation/REGISTRO-MARZO.md` (sin ambigüedad) |
| S-20 | Cuántos escenarios puede haber en una sesión como máximo | 20 | A-52 |
| S-21 | La orden puesta cuando el precio toma otra liquidez | 21 | A-53 |
| S-22 | Dónde va la orden de entrada frente al 0 de la caja | 22 | A-36 |
| S-23 | El nivel que, roto con mecha, anula la entrada | — (nueva) | A-32 |
| S-24 | Confirmar el break even tapado por el corte de audio de v9 | — (nueva) | A-13 |

## 2. El orden de la sesión

S-1, S-2, S-3, S-4, S-5, S-6, S-22, S-7, S-8, S-9, S-10, S-11, S-12, S-13, S-14, S-15, S-16, S-17,
S-18, S-20, S-21, S-23, S-24, S-19.

Es `ORDEN_SESION_04` en `scripts/transcribir_sesion.py`, el orden con el que se agrupa la versión
filtrada de v10.

## 3. Las subpreguntas añadidas a las de PREGUNTAS.md

- **S-1**: si la caja se traza con la vela del bloque cerrada o en formación (A-49).
- **S-3**: si el objetivo de 3 a 1 se mide sobre la distancia 0→1 o 0→0,8 (A-18).
- **S-5**: qué hace con la orden si a las 11:00 cambia el sesgo de H4 (A-39).
- **S-18**: qué pasa con la marca del alto viejo (A-25).

## 4. Los esquemas que se enseñaron

Cuatro esquemas INVENTADOS, en S-2, S-4, S-11 y S-13, rotulados «Esquema inventado, no es un día
real». Muestran la situación sin las opciones. Por decisión del consultor, esto enmienda el «sin
gráficos» del encargo del barrido (`PREGUNTAS.md`, «Las preguntas van cerradas y sin gráficos»).
**No se enseñó ningún gráfico de un día real.**
