"""Busqueda de desarrollo sobre la base de conocimiento (F08, ADR-0010).

Junta evidencia (`knowledge/evidence`), crudas activas (`data/transcripciones`) y fotogramas
(`data/fotogramas`) en un indice en memoria, regenerado en cada ejecucion, y responde a `kb find`
(texto) y `kb at` (instante). Lexica, sin embeddings ni ranking; toda respuesta lleva fuente.
Capa entre `spec` y `feedback`: no importa `validation` ni `cli`.
"""
