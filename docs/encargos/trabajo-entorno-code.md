# Encargo · trabajo/entorno-code

Dado por Aleks (consultor) el 2026-10-10. Copiado tal cual:

> Modelo: Opus · Esfuerzo: alto
>
> Rama nueva: trabajo/entorno-code, desde main en d32db01 (commit de estado sobre el merge 7823568, tag stable/F37k-hoja-de-ruta). Antes de abrirla, verifica con git que main y origin/main están en d32db01, que el tag apunta a 7823568, que la CI de main sobre d32db01 está en success y que no hay otra rama abierta en local ni fix/* en origin; si algo no cuadra, para y dímelo. Ábrela con la skill abrir-rama: este prompt tal cual en docs/encargos/trabajo-entorno-code.md, su contrato.yaml con tramo: R0 (R0.2 de docs/plan/HOJA-DE-RUTA.md, NA:F) y el archivo en HISTORIA del PROJECT_STATE.md de main.
>
> Objetivo: R0.2 de la hoja de ruta. Instalar el entorno de trabajo de Claude Code que diseñó el consultor (2026-10-10, versión 2), auditado por un agente independiente contra el repo. Está en C:\Users\USER\Desktop\paquete-skills-code\ (fuera del repo): cinco skills (.claude/skills/fase-cero, activar-sesion, comparar-con-main, entregar-rama, retomar-rama), un agente (.claude/agents/auditor-encargo.md) y ESPECIFICACION.md con siete puntos (E1 a E7). Antes de nada, comprueba que es la versión 2: .claude/agents/auditor-encargo.md tiene el punto «5. **El tramo**»; si no lo tiene, para y dímelo. Las skills y el agente se copian TAL CUAL, salvo lo que la fase 0 demuestre falso o en conflicto con el repo, que se corrige y se declara. ESPECIFICACION.md no se copia al repo: es el encargo de lo que hay que construir.
> NO cambia: src/ salvo E1, E3 y E7; spec, knowledge, parámetros e informes cerrados; nada de lo que sella make check; las puertas de abrir-rama, cerrar-rama e ingerir-sesion. Los papeles son los de ADR-0072. Nada de holdout. Saldo de bytes de PROJECT_STATE ≤ 0.
>
> FASE 0, sin escribir nada en el repo, con entrega y PARADA:
> a) Lee cada fichero del paquete entero. Por cada regla, paso, ruta, comando y opción: ¿existe así y coincide con CLAUDE.md, RITUAL.md, CONTRATO-DE-RAMA.md, AMBIGUEDADES.md, MIRAR-EL-MATERIAL.md, knowledge/feedback/README.md, ERRORES-RECURRENTES.md, docs/plan/HOJA-DE-RUTA.md, ADR-0072 y los demás ADR que cite? Tabla con fichero:línea de cada discrepancia y tu corrección propuesta. Atención a lo que trajo trabajo/hoja-de-ruta (el campo tramo, la hoja de ruta en el commit del contrato, abrir-rama y cerrar-rama cambiadas): E6 se ajusta a la abrir-rama de hoy.
> b) E1: qué función de la guardia decide si un fichero se puede leer, y cómo la llamaría estado_sesion.py; el hook muestra también el tramo de la rama. E2: el recuento de filas de ERRORES-RECURRENTES con hallazgos del consultor que el revisor no vio. E3: la duración de cada paso de make check en una ejecución y los veinte tests más lentos; y, en un clon --detach, la suite con pytest-xdist en serie y con -n auto (cinco veces, mismos resultados por nombre, la guarda de provoca_holdout y el pico de memoria de cada modo). No añadas xdist al repo todavía.
> c) Solapes con las skills existentes y con el revisor, y lo que ninguna pieza cubre de los diez últimos encargos.
> Entrega la fase 0 en docs/validation/ENTORNO-CODE.md y PARA.
>
> FASE 1 (tras mi respuesta): instalar las piezas, construir E1 a E7 con los tests que pide cada punto (incluidos los que rompen a propósito) y actualizar CLAUDE.md (E5). Desde la fase 1, la rama usa ya sus propias skills: entrega con entregar-rama.
>
> Cierre de la rama:
> - make check > make-check.log 2>&1, con el exit 0, ningún failed y la línea SELLO, antes de cada commit.
> - Toca .claude/ y hooks: empújala como fix/entorno-code y pasa la CI de Linux. El único fallo aceptado es el de state check por el nombre fix/. Dame los números de run.
> - Informe en docs/validation/ENTORNO-CODE.md, con la fase 0, la PARADA y mi respuesta tal cual, lo hecho y su estado al final; y, preparadas para el commit del contrato, las líneas de la Next Action (F) y de la hoja de ruta (R0.2 hecha).
> - Pasa el revisor (subagente revisor), con este alcance: que ninguna pieza contradiga un runbook, RITUAL, CLAUDE.md, la hoja de ruta o un ADR; que no se pierda ninguna puerta de las skills existentes; que el hook de arranque no lea nada que la guardia bloquee y nunca bloquee la sesión; que make rapido, si existe, no selle; y nada de holdout. Pega su informe al final del tuyo.
>
> Rama lista para revisión, NO cerrada.
