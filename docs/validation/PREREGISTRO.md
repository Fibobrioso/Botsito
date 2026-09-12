# PREREGISTRO de umbrales — VACIO: NO SE HA PRE-REGISTRADO NADA

**Estado: SIN RELLENAR. Mientras este fichero siga asi, NO SE PUEDE ABRIR NINGUN HOLDOUT.**

Existe desde el 2026-09-12 porque `docs/validation/README.md` y `MASTER_PLAN §G` llevaban meses
exigiendolo en presente y el fichero no existia: una puerta que no esta puesta no cierra nada.
Ponerlo vacio es mas honesto que no ponerlo, porque hace visible que la puerta sigue abierta.

## Para que sirve

Un umbral pre-registrado es un numero que se escribe **antes** de ver el resultado, para que nadie
lo pueda ajustar despues. Es la unica forma de que la cifra de fidelidad de F26 signifique algo:
sin esto, siempre se puede encontrar un criterio con el que el bot apruebe.

## Que tiene que llevar, antes de abrir `holdout-1` (F26)

1. **La metrica exacta** y como se calcula: que cuenta como "misma decision" entre el bot y el
   trader (direccion, ventana de tiempo, nivel de entrada, stop y objetivo con que tolerancia).
2. **El umbral**, con su numero, y que pasa si no se alcanza.
3. **La particion** sobre la que se mide y por que esa.
4. **Quien autoriza la apertura** (el usuario, ADR-0021) y la fecha.
5. **Las exposiciones declaradas** que afectan a esa particion, copiadas de
   `docs/validation/HOLDOUT-EXPOSICIONES.md`. Hoy hay una: la del 2026-09-11.
6. **Que se hace si falla**: usar `holdout-2` tras la correccion, y con que condiciones.

## Lo que hay que saber al rellenarlo

- Mayo es el unico material: 19 dias, 6 `dev` y 13 holdout (6/4/3). Junio quedo descartado el
  2026-09-12.
- Trece de esos dias tienen su PnL diario expuesto desde el 2026-09-11. No los quema (ADR-0021),
  pero F26 lo cita.
- Esta pendiente pedirle al trader un mes que no haya tocado. Si llega antes de F26, la cifra se
  mide sobre material limpio y esto se replantea.
