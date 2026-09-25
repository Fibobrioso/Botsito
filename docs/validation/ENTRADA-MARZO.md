# La entrada de marzo, preparada antes de que llegue

Rama `trabajo/entrada-marzo`, 2026-09-24. Deja listo el camino por el que entrara el backtest de
MARZO de 2026, **sin material de marzo**: no hay libro, ni tramo, ni reparto de 2026-03 en el
repositorio. Lo unico de marzo que existe son sus velas.

## 1. ADR-0046: las tres decisiones

Decisiones del consultor, tomadas antes de ver marzo (`docs/adr/0046-marzo-entra-por-el-camino-de-fidelidad.md`):

1. **Marzo entra por el camino de fidelidad (ADR-0036)**, con sorteo y con la misma puerta
   (ADR-0033). Lo que caiga en `fidelidad-2` y `fidelidad-3` queda oculto: es la reserva que el
   config de fidelidad dejo vacia a proposito el 2026-09-21. Enmienda ADR-0025 §5, que lo mandaba
   por el kit.
2. **Su parte `fidelidad-dev` es conjunto de MEDICION de desarrollo, junto con mayo.** Aclara
   ADR-0043: «marzo cuando entre» es solo esa parte, nunca sus dias reservados.
3. **Los cupos son una REGLA fijada antes de ver marzo**, no cifras: `fidelidad-dev` = ⌊N/3⌋,
   `fidelidad-2` = ⌊(N − dev)/2⌋, `fidelidad-3` el resto y `fidelidad-1` = 0, con N los casos del
   universo del artefacto. Vive como dato en `cupos_por_mes` del config de fidelidad (ADR-0002).

Y lo que las hace cumplir, del mismo ADR: el artefacto `<simbolo>-AAAA-MM` limita su universo a
su mes (§4); **el sorteo no se repite nunca**, ni con otra semilla, ni borrando la carpeta, ni tras
un huso NO CONCLUYENTE (§5); el orden de entrada a-e con la excepcion acotada a ADR-0039 §1 -Aleks
lee solo la columna de fechas, una vez, antes del sorteo- (§6); y `casos ingerir --artefacto` para
los `fidelidad-dev` (§7).

### Los cupos, para N = 18, 20 y 22

Calculados con `cupos_desde_regla` sobre la regla real de `knowledge/cases/fidelidad/config.yaml`:

| N | `fidelidad-dev` | `fidelidad-2` | `fidelidad-3` | `fidelidad-1` |
|---|---|---|---|---|
| 18 | 6 | 6 | 6 | 0 |
| 20 | 6 | 7 | 7 | 0 |
| 22 | 7 | 7 | 8 | 0 |

Suman N en los tres casos: `asignar` deja fuera en silencio lo que no quepa, y la regla se niega
a cargar si no reparte los N (test de 1 a 40 contra la formula escrita a mano).

## 2. Lo que se construyo, un commit por pieza

| Commit | Que |
|---|---|
| `e9ef8b0` | ADR-0046, con notas en ADR-0025, 0039 y 0043 sin reescribir su cuerpo |
| `04f1ed9` | Las velas M1 de marzo (§3) |
| `c9b6a55` | `fidelidad build`: universo limitado al mes del id, cupos desde la regla, sorteo irrepetible (ancla, carpeta o historial) |
| `425b3be` | `casos ingerir --artefacto`: solo los `fidelidad-dev` de un artefacto sorteado, anclado y commiteado, menos los ocultos; test con CENTINELA en las filas reservadas |
| `b4139ae` | `scripts/huso_por_velas.py`: ADR-0039 §5 hecho herramienta, con sus cifras en `knowledge/corpus/criterio_huso.yaml` |
| `2054b58` | El ensayo de punta a punta sobre un repo sintetico (`tests/contract/test_ensayo_marzo.py`) |
| `ae90410` | El runbook `docs/runbooks/ENTRADA-MARZO.md` |

**La centinela, aprobada por el consultor tal como esta.** Las filas de dias reservados del libro
sintetico llevan una cadena que no es ni precio ni direccion. Los tests exigen que no salga ni por
stdout, ni por stderr, ni en los ficheros escritos, y comprueban que esta viva: pedido a
proposito, el dia reservado rompe la ingesta sin reproducirla.

## 3. Las velas de marzo, con kit y fidelidad identicos

`eurusd-m1-2026-03-989392e8`: 31800 velas M1, 31 dias presentes, 0 ausentes, 4 sin datos y 4 huecos
de 60 min o mas. La primera descarga se corto por red (timeout y 503 de Dukascopy en el dia 17) y
se reanudo desde la cache. Descargar velas no abre nada (ADR-0021 §1).

Es la cita con el problema de Next Action 9: un segundo manifiesto del mismo prefijo podia romper
`kit build` en silencio. **Medido antes y despues de la descarga**, `kit check --sesion
2026-09-09-sesion-01`, `fidelidad check --artefacto eurusd-2026-09` y `knowledge validate` dieron
salida identica byte a byte. **Y otra vez al final de la rama**: `kit check` da OK (con los dos
AVISO de la sesion celebrada) y `fidelidad check --artefacto eurusd-2026-09` da `OK: eurusd-2026-09
se recompone igual desde el repo y data/`; `knowledge/cases/kit/`, `fidelidad/eurusd-2026-09/` y
`fidelidad/anclas.yaml` no difieren de `main`. Septiembre se recompone igual con el filtro por mes
(test `test_septiembre_se_reconstruye_igual_con_el_filtro_por_mes`).

## 4. El control del huso sobre abril

Las cifras de §5 (margen de 2 puntos, >= 90 % frente a <= 50 %, UTC frente a Europe/Madrid) salen
de `criterio_huso.yaml`, y un test por AST comprueba que el script no lleva ninguna escrita. Los
tests sinteticos estaban en verde ANTES del control, y los blobs del script (`8508af79`) y del
criterio (`34d54399`) son los mismos antes y despues: la herramienta no se ajusto para que cuadrara.

Control sobre **ABRIL**, no mayo (`docs/validation/HUSO-POR-VELAS-CONTROL-ABRIL.txt`):

| libro | dias `dev` | filas comparables | frontera | UTC | Europe/Madrid | veredicto | declarado |
|---|---|---|---|---|---|---|---|
| abril (`5e5d9b83…`) | 21 | 38 | no | 36/38 (94,7 %) | 4/38 (10,5 %) | UTC | UTC: **COINCIDE** |

Reproduce exactamente la medida hecha a mano el 2026-09-22 (`MAYO-DEV.md`, punto 6: 36 y 4 de 38).
Declarado en `HOLDOUT-EXPOSICIONES.md`.

**Fechas con otro formato, decision del consultor del 2026-09-24:** una fecha que no casa con el
formato para la medida entera, porque de esa fila no se sabe de que dia es. Es correcto, y el
runbook lo convierte en PARADA en los pasos a y c: no se toca el lector sobre la marcha, y la
sesion describe el caso sin mostrar fechas.

## 5. El orden del runbook

`docs/runbooks/ENTRADA-MARZO.md`, ensayado entero en `test_ensayo_marzo.py`:

- **0 · entrega:** el xlsx al corpus y al inventario. PARADA sin material.
- **a · fechas:** Aleks lee solo la columna de fechas y da el tramo -interseccion UTC/Madrid- y el
  formato; la sesion anade el tramo sin sha. PARADA antes, y PARADA si hay mas de un formato.
- **b · sorteo:** semilla fijada antes, anclado en el mismo commit, N casos de un universo de N.
  PARADA si falla; nunca se vuelve a sortear.
- **c · huso:** primero el control con abril, que tiene que dar un `diff` vacio contra la salida
  commiteada; despues marzo. PARADA si el control no coincide, si una fecha no casa con el formato,
  o si sale NO CONCLUYENTE.
- **d · declaracion:** la entrada en `libros.yaml` y el sha atado al tramo. La sesion PARA antes
  del commit: la entrada es solo anadir.
- **e · ingesta:** `casos ingerir --artefacto eurusd-2026-03`. PARADA ante cualquier error.

## 6. Lo que esta rama NO hace

- No toca material de marzo: no existe todavia.
- No mide la fidelidad de nada: el motor no existe.
- No toca `PROJECT_STATE.md` salvo `Current Branch` y la linea de tests, que exige `state check`.
  Change Log, indice de ADR-0046, Next Action y estado van en el paso 3 del ritual.
- El aviso de `casos ingerir` sin `--artefacto` cambia de texto -ahora dice por donde entran los
  dias de fidelidad- y conserva el prefijo que vigilan los tests.

## Estado

CERRADA PARA EL RITUAL. Marzo tiene camino, herramienta, ensayo y runbook; entra cuando el trader
lo entregue.
