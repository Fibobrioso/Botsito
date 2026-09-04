---
status: ACTIVE
date: 2026-09-04
phase: F02
---

# 0002 · Registro de parametros: una sola puerta, tipos no intercambiables, lectura estricta

## Decision
Todo parametro de negocio vive en `knowledge/spec/parametros.yaml` y se lee por
`botsito.config.registro`. Cada uno declara tipo, unidad, fuente (evidencia, feedback o decision) y
estado. Leer un `UNKNOWN` falla siempre; un `DEFAULT_AMBIGUOUS` exige `ambiguedad_id` y su lectura
queda anotada para el journal. Los valores son `Decimal`; `Fraccion` y `Porcentaje` son tipos
distintos que no se operan entre si. Un test de contrato prohibe los literales de negocio fuera de
`config/`; `settings.toml` no admite claves del registro.

## Problema que resuelve
Tres corrupciones documentadas en la auditoria de fases: un default silencioso que se convierte en
regla; un 0,5 % escrito como 0,5 (factor 100); y dos puertas para el mismo valor (config y spec)
que divergen sin que nadie lo vea.

## Alternativas consideradas
1. Constantes en modulos Python con comentario que cita la regla.
2. Un unico `settings.toml` con negocio y entorno mezclados.
3. Registro con `float` y un solo tipo numerico.
4. Registro generico con perfiles y herencia por entorno.

## Por que elegimos esta opcion
El estado del parametro es informacion de negocio (que sabe el trader, que es default) y debe viajar
con el valor; el tipo evita el error de unidad en compilacion y en revision; el `Decimal` evita el error
binario del `float` en Python. No elimina el redondeo frente a MQL5: la regla de redondeo
fraccion → puntos (0,75 × 137 puntos) se define en F18 y se exporta como racional en F28
(auditoria extrema 2026-09-04).

## Por que descartamos las demas
(1) Un comentario no falla en rojo. (2) Mezcla regimenes de cambio y crea dos puertas. (3) `float`
introduce discrepancias con la implementacion MQL5 y no distingue unidades. (4) Sobre-diseno: hay
un instrumento, una estrategia y menos de treinta parametros.

## Impacto
`domain/valores.py`, `config/registro.py`, `config/ajustes.py`, `knowledge/spec/parametros.yaml`
(vacio hasta F11), `tests/contract/test_no_business_literals.py` con lista real, contrato de
importacion `domain` ↛ `config`. F11 anade los valores citando evidencia; F28 exporta desde aqui.

## Fecha / fase
2026-09-04 · F02

## Estado
ACTIVE
