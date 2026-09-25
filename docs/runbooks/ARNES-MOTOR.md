# El arnés del motor

Cómo se corre el motor sobre CONSTRUCCIÓN y se lee su informe (ADR-0048). Escrito el 2026-09-25 en
la rama `trabajo/arnes-motor`.

## Qué hace

Toma los días `dev` de los meses de construcción de `knowledge/cases/criterio_fidelidad.yaml` (hoy
abril y agosto de 2026) y hace pasar cada uno por el motor. El motor es el intérprete del árbol
genérico de ADR-0030, con las primitivas que haya escritas. Después compara las operaciones del
bot con las del trader usando el criterio de ADR-0043, y escribe un informe con:
- **cobertura y precisión**, y las operaciones del bot en días sin operaciones del trader;
- **el embudo sobre el grafo de hechos**: cuántas sesiones con operaciones del trader producen cada
  hecho, y cuántas se paran en cada primitiva `NO_IMPLEMENTADA`;
- **RN-003 al abrir la sesión**, por sesión y por operación del trader;
- **una línea por sesión** con lo que se produjo y dónde se paró cada hecho que faltó.

## Cómo se corre

```
uv run botsito motor arnes --salida arnes.txt
```

Sin `--meses` corre sobre todos los meses de construcción. Con `--meses AAAA-MM,AAAA-MM` corre solo
sobre esos, y tienen que ser de construcción. Por pantalla sale `OK` con la ruta del informe, y una
línea `TIEMPO` y `MEMORIA` que **no** va en el informe: el informe es determinista y dos ejecuciones
dan el mismo fichero byte a byte, así que dos informes se comparan con `diff`.

## Cuándo se niega

- **Un mes de medida** (hoy mayo) o **cualquier mes que no sea de construcción** (marzo, septiembre,
  febrero...): sale con `ERROR` y código 2, y **no escribe nada**. La medida tendrá su propia rama y
  su propio ADR (ADR-0048 §7).
- **Un día oculto** (reservado o retirado) entre los días `dev`: sale con `ERROR` y código 3 sin
  leer su caso. No debería pasar nunca, porque la biblioteca lo impide; si pasa, se para y se
  investiga.

## Cómo leer el embudo

- `hecho:si`: la sesión lo produjo.
- `hecho:no[primitivas]`: no lo produjo, y las reglas que lo producen se pararon en esas primitivas
  `NO_IMPLEMENTADA`.
- `hecho:no[productoras sin cumplirse]`: las reglas que lo producen se evaluaron y no se cumplieron.
  Por ejemplo, RN-003 con el sesgo ambiguo.
- `rn003`: lo que dijo `domain/sesgo.py` al abrir la sesión.

Una primitiva `NO_IMPLEMENTADA` vale DESCONOCIDO y no decide: ni deja pasar ni prohíbe (ADR-0048
§2). Hasta que exista el bróker simulado, el motor real no produce ninguna operación y la cobertura
es 0.

## Lo que no hace

No mide nada sobre mayo, no abre ningún holdout y no cambia la spec. Los huecos de interpretación
que encontró al construirse están en ADR-0048 (H1-H6).
