# knowledge/cases/
Biblioteca de casos ejecutables (F14). `dev/` cierra reglas; `holdout/1`, `holdout/2` y `holdout/3` son
las tres particiones reservadas (se abren una sola vez cada una: F26, cifra final, fase 7); `fixtures/`
guarda las instantaneas OHLC/ticks con hash. La asignacion a particiones se commitea con seed ANTES de
la sesion de etiquetado.
