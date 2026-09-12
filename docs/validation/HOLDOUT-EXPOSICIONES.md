# Exposiciones de holdout

Registro de todo lo que se ha visto de una particion reservada, aunque fuera de pasada. Lo exige
ADR-0021: una exposicion no siempre quema, pero **siempre se declara**, el mismo dia, y F26 la cita
en su informe. Una cifra de fidelidad que no mencione lo que sabia quien la produjo no se puede
defender.

Qué es cada cosa, en corto (la definicion completa esta en ADR-0021 y en
`knowledge/cases/holdout/README.md`):

- **Abrir** = leer las etiquetas de esos dias, o medir cualquier cifra del bot sobre ellos. Quema.
- **Exponerse** = ver un resultado agregado de esos dias sin ninguna decision dentro. No quema, se
  declara.

| Fecha | Que se vio | Particiones | Quien | ¿Quema? |
|---|---|---|---|---|
| 2026-09-11 | El calendario de PnL **dia a dia de todo mayo de 2026** (4 may +30 $ … 29 may −118 $), en una de las siete capturas de la pestana Analytics de FX Replay que el trader entrego con el backtest del mes. Tambien el agregado del mes: 68 operaciones, 18 ganadoras / 33 perdedoras / 17 en break even, win rate 35,29 %, RR medio 3,45, profit factor 2,14, +650 $ sobre 100 000 | `holdout-1` (6 dias), `holdout-2` (4), `holdout-3` (3) — los trece de mayo | la sesion de trabajo que proceso el material (consultor + agente) | **NO** (ADR-0021 §5): no se vio ninguna decision -ni hora, ni direccion, ni entrada, ni stop- y un PnL diario no se puede invertir para deducirlas |

## Lo que esto obliga

1. **F26 cita esta tabla** en su informe de fidelidad, junto al pre-registro de umbrales. Sin esa
   frase, la cifra sobre `holdout-1` no es defendible.
2. **`holdout-1` sigue reservado** para la nota, intacto. `holdout-2` es la segunda oportunidad si
   hay que corregir y volver a medir; `holdout-3`, la de la fase final.
3. **El detalle por operacion del backtest de mayo** (el xlsx: ticket, precios, R por operacion) es
   material de holdout para los trece dias reservados: no se abre sin autorizacion del usuario y
   sin `PREREGISTRO.md` commiteado antes.
4. **Pendiente**: pedirle al trader un mes que no haya tocado, para tener una particion limpia de
   verdad. Mayo ya esta expuesto y junio quedo descartado el 2026-09-12.
