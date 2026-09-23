# A-18 en las transcripciones: el criterio, congelado antes de buscar

Rama `trabajo/a18-transcripciones`, 2026-09-23. Next Action 14. Sin merge, sin tag y sin push.

Este documento y `scripts/a18_buscar.py` se commitean JUNTOS y ANTES de ejecutar ninguna búsqueda.
El script es la implementación exacta de lo que dice aquí: cambiarlo después de ver la salida es
cambiar el criterio. Su test (`tests/unit/test_a18_buscar.py`) trabaja sobre una transcripción
SINTÉTICA, y ninguna transcripción real se ha leído para escribir nada de esto.

## 0. El alcance (decisión del consultor, 2026-09-23)

- **Entran las cinco transcripciones vigentes de v1 a v5**, todas del modelo
  `large-v3-int8-float16`:
  - `tr-v1-large-v3-int8-float16-bbd8a931`
  - `tr-v2-large-v3-int8-float16-28391c2c`
  - `tr-v3-large-v3-int8-float16-270a4851`
  - `tr-v4-large-v3-int8-float16-a8d1bccc`
  - `tr-v5-large-v3-int8-float16-3c6fbb57`
- **Quedan fuera:**
  - la de v6, porque se grabó en un día que es reservado (ADR-0037);
  - las 7 heredadas de `_procesado/`, porque no tienen fecha declarada en su fila del manifiesto y
    son el ASR pequeño (ADR-0007);
  - las cinco sustituidas, porque cada una la sustituye su vigente (`reemplaza_a`).
- **«Material de septiembre»** es el backtest de septiembre del trader, no la fecha de grabación.
  El brief del paso 0 lo decía de forma que dejaba fuera a v5; ese error de redacción es del
  consultor y va al informe.

## 1. La regla, literal del punto 14 de Next Action

> Un pasaje RESPONDE si dice ambas cosas, o si dice una sola de forma incompatible con uno de los
> dos supervivientes. Si hay pasajes en sentidos opuestos, o ninguno responde, se pregunta al
> trader con la pregunta abierta de `docs/validation/V5-INSTANTES.md`.

Las «dos cosas» son **dónde pone el stop respecto a la caja** y **cómo calcula el TP**. Los dos
supervivientes son `(riesgo_real, 0,8)` y `(caja_completa, 1,0)` (ADR-0040).

## 2. Los términos, lista cerrada

Se busca sin distinguir mayúsculas ni tildes, y la coincidencia es por palabra o por frase:

stop · stop loss · SL · protejo · proteger · protección · protegido · 0.8 · 0,8 · 0.80 · 0,80 ·
punto ocho · ochenta por ciento · 80% · caja · caja completa · toda la caja · nivel uno · nivel 1 ·
cien por ciento · 100% · take profit · TP · objetivo · uno a tres · 1 a 3 · 1:3 · tres R · 3R ·
relación · ratio · RR · riesgo · uno por ciento · 1% · beneficio

Son 36 términos. **No se añade ni se quita ninguno después de ver resultados.**

**Cómo lo implementa el script:**
- **Normalización.** Se pasa a minúsculas, se quitan las tildes (NFD sin marcas combinantes) y
  los espacios se reducen a uno.
- **Límite de palabra.** A ningún lado de la coincidencia puede haber una letra o una cifra
  pegada. Tampoco puede haber una cifra al otro lado de un separador decimal (`.`, `,` o `:`),
  así que `0.8` no casa dentro de `0.80`, `1%` no casa en `11%` ni en `100%`, y `1:3` no casa en
  `1:30`.
- **Frases.** Una frase se busca sobre el texto de toda la transcripción, con los segmentos
  unidos por un espacio. Así casa también cuando queda partida entre dos segmentos.
- **Términos que se solapan.** Una frase y sus palabras cuentan las dos: «stop loss» es una
  coincidencia de `stop` y otra de `stop loss`.

## 3. La ventana

- **±45 s** alrededor de cada coincidencia, medidos con las marcas de tiempo de los segmentos:
  desde el inicio del segmento donde empieza la coincidencia hasta el final del segmento donde
  acaba.
- **Las ventanas que se solapan** dentro de una misma transcripción se unen en una sola.
- **El pasaje trae entero cada segmento** que toque su ventana, sin recortar.

## 4. El texto que se lee y su integridad

- **Se lee la transcripción CRUDA** (`cruda.jsonl`), porque es de la que se copia una cita
  literal (`CLAUDE.md`, «Donde esta el texto de las transcripciones»).
- **Integridad antes de leer.** El script comprueba antes que sus bytes son los que fija el
  manifiesto commiteado (`sha256_cruda`) e imprime esa comprobación.
- **Lista cerrada.** Cualquier transcripción fuera de las cinco se rechaza antes de leer un byte.

## 5. La salida

Por cada pasaje, la salida trae:
- la transcripción;
- el intervalo de tiempo;
- los términos que coincidieron, con su número;
- el texto completo de la ventana, un segmento por línea con su intervalo y su número.

Al final va el número de pasajes por transcripción y el total. Se ejecuta **una sola vez**:
`uv run python scripts/a18_buscar.py --salida docs/validation/A18-TRANSCRIPCIONES-SALIDA.txt`.
La salida se commitea tal cual, en su propio commit, con todos los pasajes y sin filtrar.

## 6. La clasificación, que se hace DESPUÉS y en otro commit

Cada pasaje recibe una de tres etiquetas, citando la frase exacta que lo decide:
- **responde → riesgo_real**;
- **responde → caja_completa**;
- **no responde**.

Para «responde», la frase tiene que decir **dónde va el stop respecto a la caja** o **cómo se
calcula el TP**. **Un número suelto no basta.**

## 7. Sin trato especial

Lo que ya se sabe de v5 (las frases «SL por defecto» y «protejo a 0.80») entra como cualquier
otro pasaje, sin trato especial: se busca con los mismos términos y se clasifica con la misma
regla.

## Estado

CRITERIO CONGELADO. La búsqueda no se ha ejecutado.
