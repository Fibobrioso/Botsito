"""Biblioteca de casos y kit de elicitacion (F10, ADR-0011; F14 anade el runner).

`cases` esta por encima de `spec`, `retrieval`, `feedback`, `evidence`, `data` y `config`: junta
la evidencia, el registro de parametros, las ambiguedades y los datasets congelados para generar
el paquete de una sesion con el trader (cuestionario, ventanas de replay, particiones, hoja) y
para medir el acuerdo entre rondas de etiquetado (kappa). No importa `validation` ni `cli`.
"""
