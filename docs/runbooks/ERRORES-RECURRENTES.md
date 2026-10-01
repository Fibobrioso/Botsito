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

## La tabla

| Rama | Hallazgos del revisor | Hallazgos del consultor despues | Que se le escapo |
|---|---|---|---|
| `trabajo/guardias-claude` | ver su informe (§6 de GUARDIAS-CLAUDE.md) | pendiente de la revision | — |
