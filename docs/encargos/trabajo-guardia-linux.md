# Encargo · trabajo/guardia-linux

Rama abierta por Claude Code el 2026-10-01 durante el cierre de `trabajo/guardias-claude`, sin
prompt propio: la orden de cierre de Aleks pedia terminar con la CI en verde, y la CI del commit de
estado (`ebb836b`, run 36889215829) salio ROJA. Lo que se copia aqui es la parte de esa orden que
la origina, tal cual:

> Commit sellado y ritual completo: merge a main, tag, PROJECT_STATE, make check, sello, commit de
> estado, push atómico de main y el tag (con la regla ask, te pedirá confirmación: es lo esperado),
> CI en verde y borrado de la rama. Termina con el sha final de main y el estado del CI.

Lo que pide esta rama, por tanto: que la guardia de Claude Code (`.claude/hooks/guardia.py`)
funcione igual en Linux que en Windows, para que la CI de `main` salga verde. Nada mas. No se
abre por `RITUAL.md` («Si la CI sale roja»: un commit encima de `main`) porque ese camino deja la
CI roja otra vez: `state check` (regla 5) no admite en `main`, tras el ultimo tag `stable/*`,
commits que toquen algo distinto de `PROJECT_STATE.md`. El merge y el tag de esta rama necesitan
una orden de cierre propia.
