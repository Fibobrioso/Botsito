# A-24, A-21, A-26 y A-34 en las transcripciones: el criterio, congelado antes de buscar

Rama `trabajo/a24-a21-a26-a34`, 2026-09-24. Sin merge, sin tag y sin push.

Este documento y `scripts/buscar_ambiguedades.py` se commitean juntos y **antes** de ejecutar
ninguna búsqueda. El script es la implementación exacta de este documento: cambiarlo después de ver
la salida es cambiar el criterio.

Reutiliza `scripts/a18_buscar.py`, generalizado sin cambiar su comportamiento para A-18. Su test
sigue en verde, y su salida, regenerada fuera del repositorio, sale **idéntica byte a byte** a la
commiteada (`A18-TRANSCRIPCIONES-SALIDA.txt`).

## 0. El alcance

Las mismas cinco transcripciones vigentes que en A-18, de v1 a v5. Solo se lee la cruda, verificada
contra el `sha256_cruda` de su manifiesto.

Quedan fuera:
- **v6**, porque su día está retirado (ADR-0041);
- **las heredadas y las sustituidas.**

## 1. Las hipótesis en competencia (decisión del consultor sobre el paso 0)

| ambigüedad | hipótesis |
|---|---|
| **A-24**, qué hace que marques un pivote de M15 y no otro | (a) el pivote **más reciente**; (b) el **más extremo**; (c) **otra o discrecional** («el que tú consideres»), que se registra aunque no sea ejecutable |
| **A-21**, qué es una zona de control limpia | **abierta**: responde si el trader enuncia una regla general |
| **A-26**, el flujo de M15 contra el sesgo de H4 | (a) se marca igual la liquidez con la vela contraria al flujo de M15, y el lado de ruido se lee de ese flujo; (b) solo cuentan las velas contrarias al flujo que va en el sentido del sesgo. Las dos, tal como están en el yaml |
| **A-34**, vela H4 previa que rompe ambos extremos | **abierta**: responde si el trader enuncia una regla general |

## 2. La regla común

- **Un pasaje RESPONDE** si enuncia la regla de forma general, o si es incompatible con todas las
  hipótesis menos una.
- **Un pasaje NO RESPONDE** si es una operación concreta sin regla, o una frase que valga para
  varias hipótesis.
- **Si hay pasajes en sentidos opuestos, o ninguno responde, se pregunta al trader.** La regla
  global la aplica el consultor, no esta rama.
- **Ante la duda, NO RESPONDE**, con la duda anotada.

## 3. Los términos, lista cerrada por ambigüedad

Solo frases o combinaciones específicas, en los dos sentidos. Queda prohibida **cualquier palabra
suelta de uso constante**: liquidez, zona, M15, H4, sesgo, vela y pivote. Un test lo comprueba.

La búsqueda no distingue mayúsculas ni tildes, y casa por palabra o por frase, igual que en A-18.

- **A-24:** más reciente · más recientes · estructura más reciente · más próximo · más cercano · más
  extremo · alto más alto · bajo más bajo · el más alto · el más bajo · punto más alto · punto más
  bajo · que tú consideres · que yo considere · yo considero · invadiría · no se toma en cuenta ·
  velas atrás
- **A-21:** zona limpia · zona de control limpia · sea limpia · mucho ruido · sin ruido · sin mucho
  ruido · haga ruido · hace ruido · ruidoso · ruidosa · cuántas velas · número de velas · retroceso
  complejo · complex pullback · ningún retroceso · segunda zona de control · otra zona de control
- **A-26:** contra el sesgo · contra la tendencia · contra tendencia · a favor de la tendencia · a
  favor del sesgo · sentido del sesgo · flujo de 15 · flujo de m15 · flujo de m 15 · flujo en m15 ·
  flujo en m 15 · vela contraria · velas contrarias · contraria al flujo · envuelve · envolvente
- **A-34:** por arriba y por abajo · por abajo y por arriba · los dos extremos · ambos extremos · los
  dos lados · ambos lados · las dos direcciones · rompe los dos · envolvente · outside · vela de 4
  previa · previa cerrada · vela previa · vela de 4 horas

**No se añade ni se quita ningún término después de ver resultados.**

## 4. La ventana y el corte a 180 s

- **Ventana:** ±45 s alrededor de cada coincidencia, y las que se solapan se unen, como en A-18.
- **El corte:** un pasaje mide como mucho **180 s**. Si la unión pasa de 180 s, se corta en
  pasajes consecutivos de 180 s contados desde su inicio.
- **Qué lleva cada trozo:** lista **sus propias** coincidencias, que son las que empiezan dentro
  del trozo, y trae los segmentos que lo tocan.
- **Un trozo sin coincidencias propias no se emite.**
- **Se busca por separado para cada ambigüedad**, así que un mismo tramo puede salir en más de una.

## 5. El control positivo

Las frases ya conocidas, una por ambigüedad, tienen que aparecer en la salida:
- A-21: «sea una zona limpia»;
- A-24: «la zona de liquidez tiene que ser la más reciente»;
- A-26: «vela bajista envuelve a la vela anterior»;
- A-34: «lo fija la vela de 4 previa cerrada».

**Si falta alguna, se para:** la búsqueda tendría un fallo. Un test comprueba que cada frase casa
con su lista.

## 6. La salida y la clasificación

- **Una sola ejecución**, con la salida tal cual en `A24-A21-A26-A34-SALIDA.txt`, en su propio
  commit.
- **Después, la clasificación**, en su propio commit. Cada pasaje recibe su ambigüedad, su clase
  (responde → hipótesis X, o no responde) y la frase literal que lo decide.

## 7. Aplicación de la regla global

La aplica el consultor, el 2026-09-24, sobre la clasificación de `A24-A21-A26-A34-CLASIFICACION.md`.
El criterio de arriba no ha cambiado.

| ambigüedad | decisión | base |
|---|---|---|
| **A-24** | **DECIDIDA → (a), el pivote más reciente ya formado** (ADR-0045). No queda RESUELTA porque no hay registro del trader | Responde v1 #180 («la zona de liquidez tiene que ser la más reciente») y ninguno responde en contra; refuerza v4 #1174-#1182, confirmado con «Exacto»; acota v4 #846 («Uno ya formado») |
| **A-21** | Sigue ABIERTA: **se pregunta al trader** | Ninguno de sus 14 pasajes responde |
| **A-26** | Sigue ABIERTA: **se pregunta al trader** | Ninguno de sus 9 pasajes responde |
| **A-34** | Sigue ABIERTA: **se pregunta al trader** | Ninguno de sus 3 pasajes responde |
| **A-35** (nueva) | ABIERTA y bloqueante: **cuándo un pivote de M15 está formado** | La spec vigente no lo define en ninguna parte: ni el glosario, ni las reglas, ni el registro, ni los tokens. Bloquea RN-004 y no se sustituye por un parámetro provisional |

**Lo que cambió al aplicarla:**
- La fila 5 de la clasificación decía que el fotograma del croquis no se había abierto. Ya estaba
  medido: la nota de A-24 dice que en ese dibujo el alto más alto es además el último. Está
  corregida en la misma rama, antes del merge.
- El ítem `ev-v3-003916-447dc8d7`, que sostenía la hipótesis discrecional, es del TP (#479) y no de
  la liquidez de entrada.

**Lo que no se tocó:**
- PROJECT_STATE, salvo la tabla Known Ambiguities, que exige
  `test_project_state_refleja_las_ambiguedades`.
- Nada de septiembre ni de febrero, y mayo tampoco.
- PREREGISTRO sigue vacío, y no se ha firmado ninguna autorización.
- La salida de `kit check` y `fidelidad check` es idéntica antes y después de cada commit.

**Lo siguiente** no es el productor de RN-004, que está bloqueado por A-35. Es buscar A-35 en las
transcripciones con el método congelado de A-24.

## Estado

CERRADA PARA EL RITUAL: el criterio congelado, una sola ejecución, la clasificación y la regla
global aplicada (ADR-0045). Sin merge, sin tag y sin push.
