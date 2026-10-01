# La recepcion del backtest de marzo de 2026, sin abrir

Rama `feature/registro-marzo`, desde `main` en `3375249`, el 2026-09-30. Encargo de Aleks: recibir el
material del backtest de marzo de 2026 que el trader le ha pasado, ponerlo donde el repositorio guarda
el material sin ingerir, registrar su huella y **no abrir nada**. Tampoco se ingiere: este informe
acaba antes del paso a de `docs/runbooks/ENTRADA-MARZO.md`.

**Lo que la sesion ha hecho con esos ficheros, y nada mas:** listar su nombre, su extension y su
tamano; comprobar con `git check-ignore` que el destino esta fuera de git; moverlos con `mv -n`; y
calcular el sha256 de sus bytes, primero con `sha256sum` y despues con `botsito corpus inventory`
(`src/botsito/corpus/inventario.py`: para el material adicional solo hace `stat` y `sha256_fichero`,
y no interpreta el contenido). **Ningun fichero se ha abierto, previsualizado ni convertido**, ni para
comprobar el formato. La recepcion se anota en `docs/validation/HOLDOUT-EXPOSICIONES.md`, en una
fila del 2026-09-30 que dice que no se vio nada.

## 1. Lo que llego, y que parece cada cosa

Origen: `C:\Users\USER\Desktop\para-revisar\backtest marzo`, con 8 ficheros y sin subcarpetas. El
tipo se deduce **solo del nombre y la extension**; no se ha comprobado mirando dentro.

| Fichero | Bytes | Que parece, por nombre y extension |
|---|---:|---|
| `backtesting-analytics MARZO 2026.xlsx` | 11121 | **El libro de operaciones del backtest del mes.** Se llama igual que los de abril, mayo, agosto y septiembre (`backtesting-analytics <MES> 2026.xlsx`), que son la exportacion de FX Replay |
| `aaaaa.jpeg` | 96567 | Una captura de pantalla con el nombre tecleado al azar |
| `asdasdasd.jpeg` | 66124 | Igual |
| `asdasdasdwad.jpeg` | 52957 | Igual |
| `asfasfasf.jpeg` | 115611 | Igual |
| `dwarfawfa.jpeg` | 91627 | Igual |
| `fwafafawfaw.jpeg` | 49758 | Igual |
| `wdawad.jpeg` | 125001 | Igual |

**Las 7 imagenes se tratan como CAPTURAS DE ANALYTICS mientras no se sepa otra cosa.** Por el
precedente, un libro del mes acompanado de capturas: mayo trajo 7 JPEG (y 2 PNG) y septiembre 6 que, "por el patron,
son de la pestana Analytics" (`HOLDOUT-EXPOSICIONES.md`, fila del 2026-09-20). No se puede saber sin
abrirlas, y abrirlas para averiguarlo es justo lo que ADR-0038 prohibe: no se abre una imagen por
muestreo cuando una clase entera de imagenes esta prohibida.

## 2. Que exigen las reglas antes de ingerir un mes de invierno, por tipo de material

### El libro (`.xlsx`)

Mezcla granularidades (ADR-0037): trae filas por operacion y posiblemente hojas con agregados. Hasta
que haya sorteo, **cualquier dia de marzo puede acabar reservado**, asi que hoy no se puede leer ni
una fila ni un agregado. El orden lo fija `docs/runbooks/ENTRADA-MARZO.md`:

1. **Paso 0.** El libro, dentro del corpus y en el manifiesto. **Hecho en esta rama.** Una diferencia
   con el runbook: este espera que el diff del manifiesto traiga "SOLO la entrada nueva del libro", y
   aqui trae ademas las 7 imagenes. El `<SHA>` del libro, que es lo que usan los pasos siguientes, es
   el de la tabla del §3. Tambien siguen pendientes del paso 0 (Next Action 2 y 12 de
   `PROJECT_STATE.md`) marzo en `vistos.yaml` y la confirmacion escrita del trader de que es material
   que ya ha visto (F09).
2. **Paso a, PARADAS A y A2.** La sesion no abre el libro. **Aleks** lee **solo** la columna de
   fechas, **una sola vez y antes del sorteo** (CLAUDE.md, "lo minimo para fijar el universo"), y
   entrega el tramo (la interseccion de leerlo en UTC y en Europe/Madrid), el formato de `dateStart`
   y su fila en `HOLDOUT-EXPOSICIONES.md` ese mismo dia. Si la columna trae mas de un formato, se para.
   Despues, `cobertura_material."2026-03"` en `knowledge/cases/fidelidad/config.yaml`.
3. **PARADA B0: A-42 tiene que estar `RESUELTA` antes del sorteo.** Es lo que hace de marzo un caso
   aparte: es un mes de INVIERNO (en 2026 el horario de verano empieza el 29 de marzo), y en invierno
   el reloj del grafico (UTC+2 fijo) y el de Madrid se separan una hora. `fidelidad build` congela
   `huso_operativa` en `ventanas.yaml` (`src/botsito/cases/fidelidad.py:262` y `:300`) y **el sorteo
   no se repite nunca** (ADR-0046 §5): si se decide despues, ya no hay arreglo. Hoy A-42 esta
   `ABIERTA` (§4).
4. **Paso b, PARADA B.** El sorteo, con la semilla que fija el consultor antes de ejecutarlo.
5. **Paso c, PARADAS C1, C2 y C3.** El control del huso por velas: la herramienta abre SOLO las
   filas de los dias `fidelidad-dev`. Si sale NO CONCLUYENTE, marzo no se ingiere.
6. **Paso d, PARADA D.** La entrada en `knowledge/corpus/libros.yaml`, que es solo anadir (ADR-0039).
   El sha fija los bytes, asi que el formato y el huso con que se lee el libro no se podran cambiar
   nunca. La sesion la escribe y para antes del commit.
7. **Paso e, PARADA E.** La ingesta, solo de los `fidelidad-dev`.

Las filas de los dias que el sorteo reserve (`fidelidad-2` y `fidelidad-3`) solo se leen por la
puerta de ADR-0033 (`PREREGISTRO.md` y una autorizacion commiteada por particion). **Un agregado del
fichero entero no lo abre ninguna autorizacion**, porque contiene dias reservados.

### Las imagenes (`.jpeg`)

- **Si son capturas de Analytics, estan PROHIBIDAS EN BLOQUE y sin puerta posible**, sea cual sea el
  sorteo: un agregado de marzo contiene los dias reservados de marzo (CLAUDE.md §3; ADR-0021 §1;
  ADR-0037). No hay un paso del runbook que las abra, y nada de la entrada de marzo las necesita.
- **No se abren "para ver que son"** (ADR-0038). Si algun dia hace falta saberlo, el camino es
  preguntar al trader que mando, no mirar. Y si una se abriera por error y trajera un agregado, se
  declara el mismo dia con sus cifras y no se usa ninguna (ADR-0021 §2).
- Por eso **se quedan en el corpus sin ingerir**, con su huella en el manifiesto y nada mas.

## 3. Donde quedan y con que huella

**Destino:** `corpus/Estrategia del trader/Material adicional de su operativa/Backtest marzo 2026/`,
junto a `Backtest mayo 2026/` y `Backtest septiembre 2026/`, que es donde el repositorio guarda los
backtests del trader que llegan con capturas.

**Esta fuera de git, comprobado ANTES de mover** con `git check-ignore -v --no-index` sobre las 8
rutas de destino: las 8 caen en `.gitignore:2:/corpus/`. Tras moverlas, `git status` no mostro ningun
fichero nuevo, y la carpeta de origen quedo vacia. El repositorio es publico: **nada de marzo entra en
ningun commit**. Lo unico versionado es la huella, en `knowledge/corpus/manifest.yaml`, generado con
`botsito corpus inventory` y no editado a mano.

| Fichero | sha256 |
|---|---|
| `backtesting-analytics MARZO 2026.xlsx` | `6b92694791b0b045b725a591810e4fc83b2b440e9d66805e08a6ae0b1a588598` |
| `aaaaa.jpeg` | `6a3fc3e64748a2d456aca8d3706f6ccd458bc467c28482897ba4abc9a2e202bc` |
| `asdasdasd.jpeg` | `f78735055cfde2f160f36fe8840ff031900b9c764b079127870b0fa060fcbbcd` |
| `asdasdasdwad.jpeg` | `f7c92eca9836893fc275b529efc6d82a3616e9a75a602cfb7fd5357d2927e556` |
| `asfasfasf.jpeg` | `12f63cebb507ca40d0239e3235fb2656f9fbd23cf3072e55527f3870fccc1472` |
| `dwarfawfa.jpeg` | `a279730342292dac38e7c94369a40a70ff67243e570263cf3eec5671f94e96d4` |
| `fwafafawfaw.jpeg` | `51af4a8b24ee97acd774dbaafa942d4d0bec54f4a8c77756c79daadad3ae141f` |
| `wdawad.jpeg` | `b5742edef30ee74dbcf3a21dd688869b32a296bc4d036c063dd128f151a53fad` |

Los sha256 se calcularon antes y despues de moverlos, y coinciden. El manifiesto pasa, en
`material_adicional`, de 43 ficheros y 3794523 bytes a 51 y 4403289.

**Fecha de recepcion: 2026-09-30. Contenido: NO ABIERTO.** Asi consta en la fila de
`HOLDOUT-EXPOSICIONES.md`. El manifiesto, que es generado, no tiene campos para eso, y no se ha
tocado a mano.

## 4. Propuesta, SIN APLICAR: como queda marzo en el protocolo

Nada de este apartado esta escrito en `knowledge/`, en la spec ni en los casos. Es propuesta para el
consultor.

1. **Marzo entra por el camino de fidelidad** (ADR-0036 y ADR-0046), como mes de material ya visto
   por el trader que sirve para MEDIR la fidelidad del bot, no para ajustar la spec. Artefacto
   `eurusd-2026-03`, con los cupos que da la regla sobre el universo N que salga del paso a:
   `fidelidad-dev` = ⌊N/3⌋, `fidelidad-2` = ⌊(N − dev)/2⌋, `fidelidad-3` el resto y `fidelidad-1` = 0.
   `fidelidad-2` y `fidelidad-3` quedan reservadas detras de la puerta de ADR-0033.
2. **La semilla la fija el consultor antes del `fidelidad build`**, con formato `AAAAMMDD`
   (precedente de `SEPTIEMBRE-SORTEO.md` §4), y va en el mensaje del commit.
3. **Las 7 imagenes quedan fuera del protocolo:** ni dev ni holdout. No se abren nunca como material
   de marzo. Si el trader confirma que son de Analytics, se anota asi en la fila de recepcion.
4. **El orden de ramas:** una para el paso a, con la lectura de Aleks; y solo despues de cerrar A-42,
   otra para los pasos b a e.

### La decision de A-42 que hace falta ANTES del sorteo

A-42 ("con que reloj cuenta el trader su horario de operar de 07:00 a 15:00") esta hoy **ABIERTA**,
con una **lectura PROVISIONAL**: la de ADR-0059, que pone la ventana en el reloj del grafico, UTC+2
todo el ano. En invierno eso son las 06:00-14:00 de Madrid. Y el parametro `reloj_sesiones`, separado
de `huso_operativa` por ADR-0063, sigue en `civil_operativa`. La PARADA B0 exige `RESUELTA`, y
ADR-0022 admite dos formas de cerrarla:

- **RESUELTA por el trader**, con un registro de feedback que apunte a A-42. Es la pregunta 7 de la
  hoja de la sesion 4 (`docs/sesion-4/PREGUNTAS.md`; era la 6 hasta que el consultor anadio la
  primera, el 2026-09-30). La sesion 3 dejo un «creo» en v9 1:07:53 y 1:08:09 que falta confirmar.
- **O DECIDIDA por el consultor**, con un ADR que la nombre. Pero **la PARADA B0 esta escrita pidiendo
  `RESUELTA`**: si se cierra como DECIDIDA, hay que enmendar el runbook en la misma rama, o decir
  expresamente que DECIDIDA tambien vale.

La decision tiene dos piezas, y las dos hacen falta antes del paso b:

- **a) El valor de `reloj_sesiones`:** `grafico` (07-11 y 11-15 en UTC+2 fijo; en invierno, de 06:00
  a 14:00 de Madrid) o `civil_operativa` (07:00-15:00 de Madrid todo el ano).
- **b) Con que reloj se cuenta el DIA de marzo en el kit y en la ingesta.** Hoy
  `cases/ventanas.py`, `cases/fidelidad.py` y `cases/ingesta.py` usan `huso_operativa` para la
  ventana del caso y para asignar la sesion de cada operacion (`ingesta.py:468`), no
  `reloj_sesiones`. Si a) es `grafico`, el lado de los casos tiene que seguir al motor, y eso es
  codigo que va antes del sorteo, porque `ventanas.yaml` se congela con el. Si a) es
  `civil_operativa`, no cambia nada del lado de los casos.

## Estado

**ACEPTADA por el consultor el 2026-09-30, con orden de cierre en `main`.** Decide:
- **La propuesta del §4 queda ACEPTADA:** marzo entra por el camino de fidelidad con el
  artefacto `eurusd-2026-03`.
- **A-42 se cerrara como RESUELTA con el trader en la sesion 4, y no por ADR.** Asi que marzo no
  se sortea ni se ingiere hasta entonces, y **la PARADA B0 de `ENTRADA-MARZO.md` no cambia**: la
  enmienda del runbook que pedia la via DECIDIDA no hace falta.
- **Las 7 imagenes se quedan sin abrir y fuera del protocolo.** Se le pregunta al trader que son:
  es la ultima pregunta de `docs/sesion-4/PREGUNTAS.md`, la 19.

Lo que sigue es el estado previo a la revision, sin tocar.

Material de marzo **recibido, movido al corpus (fuera de git), con huella en el manifiesto y SIN
ABRIR**. Recepcion anotada en `HOLDOUT-EXPOSICIONES.md`, sin exposicion. **Nada ingerido**: marzo se
queda antes del paso a de `ENTRADA-MARZO.md`, a la espera de la lectura de fechas de Aleks, y antes
del paso b, a la espera de la decision de A-42. La propuesta del §4 **no esta aplicada**. Rama subida
sin cerrar.
