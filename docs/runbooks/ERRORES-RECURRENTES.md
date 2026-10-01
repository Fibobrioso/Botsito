# Errores recurrentes: lo que encuentra el revisor y lo que se le escapa

Desde el 2026-10-01 (`trabajo/guardias-claude`), toda rama pasa por el subagente revisor
(`.claude/agents/revisor.md`) antes de declararse «lista para revisión», y su informe va pegado al
final del informe de la rama (`CLAUDE.md`, «Como se trabaja»). Esta tabla mide si sirve: por rama,
cuantos hallazgos encontro el revisor y cuantos encontro DESPUES el consultor que el revisor no
habia visto. **El segundo numero debe tender a cero.** Si no baja, el revisor no esta mirando lo que
hay que mirar, y se corrige su lista (eje a) o la forma de partir el encargo (eje b).

## Como se rellena

- **Hallazgos del revisor**: los del informe que se pego, por gravedad (bloquea / importa / menor),
  ANTES de arreglarlos. Se apunta al declarar la rama lista, en el mismo commit que el informe.
- **Hallazgos del consultor despues**: los que el consultor senala en su revision y que NO estaban en
  el informe del revisor, por gravedad. Se apunta al cerrar la rama, o en la rama siguiente si se
  cerro sin apuntarlo. Un hallazgo del consultor que el revisor SI vio no cuenta aqui.
- **Que se le escapo**: una linea por hallazgo del consultor, con la regla o el requisito. Es lo que
  hay que ensenarle al revisor.

## Patrones que ya se conocen

Errores que han vuelto o que se sabe que volveran, con la senal que los delata y lo que se hace.

| Patron | Senal | Que hacer |
|---|---|---|
| **Pasa en Windows y falla en Linux** (rutas con `\`, `os.path.normcase`, mayusculas y minusculas). Medido el 2026-10-01: la guardia de Claude Code paso entera en local y rompio 24 tests en la CI, y el primer arreglo destapo otros dos (una carpeta en minusculas que en Linux no existe) | CI de `main` roja tras un merge con tests verdes en local | La regla de `RITUAL.md`, «Antes del merge: la CI de Linux, si la rama toca la plataforma»: se empuja la rama como `fix/<rama>` y se espera la CI de Linux en verde ANTES del merge |

## La tabla

| Rama | Hallazgos del revisor | Hallazgos del consultor despues | Que se le escapo |
|---|---|---|---|
| `trabajo/guardias-claude` | 0 bloquea, 3 importa, 3 menor (GUARDIAS-CLAUDE.md §6; pasado con un agente general que seguia `revisor.md`) | 0 bloquea, 2 importa, 0 menor | (1) los tramos no citables de v6 no se bloqueaban, y la exencion de v6 los dejaba legibles; (2) un guion nuevo o cambiado en la rama, una vez commiteado, se trataba como codigo revisado |
