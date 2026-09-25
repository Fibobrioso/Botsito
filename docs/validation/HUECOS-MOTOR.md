# Los huecos del arnés

Rama `trabajo/huecos-motor`, 2026-09-25. Sin merge, sin tag y sin push. ADR-0049. Next Action 29.

Guardas verificadas al empezar y al terminar: `docs/validation/PREREGISTRO.md` con blob
`52649183…`, el declarado; cero autorizaciones en `knowledge/cases/holdout/`. Nada del material de
septiembre; mayo no se ejecuta (el arnés se niega a cualquier mes de medida antes de leer);
febrero no se toca; ninguna fecha de día reservado o retirado en ningún fichero de esta rama. Las
velas de construcción (abril y agosto, material de desarrollo sin días reservados) se leen para
recalcular ventanas, que no es abrir (ADR-0021 §1), y los casos `dev` pasan por la compuerta.

## 1. El informe de solo lectura que precedió a la rama

El mismo día, sobre `main` en `1d92a60`, una sesión de solo lectura preparó la decisión sobre los
seis huecos de ADR-0048. Lo que midió, y de donde salen las decisiones de ADR-0049:

- **H1.** Sobre construcción (42 días, 84 sesiones): **15 sesiones AMBIGUAS** (9 primeras y 6
  segundas), **0 INSUFICIENTES**. En las 6 segundas sesiones ambiguas el estado conservaba el sesgo
  de la primera (3 con operaciones del trader, 4 operaciones), contra ADR-0044 §1 «en esa sesión».
  En 9 de 84 sesiones (5 de 49 con operaciones) el sesgo salía de una H4 anterior a la previa, así
  que la forma —`rompe` sobre «la vela H4 previa»— y la primitiva —la búsqueda hacia atrás de
  ADR-0044, leyendo `sesgo_h4_tope_velas` sin nombrarlo— no decían lo mismo. Y la ausencia de
  `sesgo` no frenaba nada: RN-005, su único consumidor, solo prohíbe SI el hecho existe.
- **H2.** Las sesiones del motor salen de `kit/config.yaml` y la ventana de RN-001 del registro;
  el motor no tiene eventos antes de las 07:00, así que RN-004 no puede ver una toma de liquidez
  anterior.
- **H3.** El orden por id no tiene efecto medible hoy: solo RN-003 dispara.
- **H4.** Diez gates en DESCONOCIDO prohíben `abrir_operacion` (RN-005, 008, 009, 016, 018, 020,
  026, 029, 031, 032): escribir el bróker no basta para que la cobertura pase de 0.
- **H5.** `evento.permitidos` se llena y nadie lo lee; RN-017 y RN-021 declaran la ausencia de un
  freno.
- **H6.** `EstadoDia()` nace cada día; inofensivo hoy porque no hay acumuladores y `sesgo` se
  recalcula desde las velas.

Los cuatro ajustes de redacción sobre el H1 de ADR-0048 están en ADR-0049, «Decision», H1.

## 2. Lo que se decidió y lo que se construyó

Las decisiones del consultor, hueco a hueco, están en ADR-0049. Lo que esta rama deja hecho:

| hueco | decisión | dónde vive |
|---|---|---|
| H1 | opción (c): `ambiguo` e `insuficiente` como valores de `sesgo`; RN-003 con `sesgo_h4_al_abrir`, que nombra `sesgo_h4_tope_velas`; RN-033 (gate) prohíbe con ellos; el nodo `hecho` admite `vale`; el hecho **caduca al abrir** (§3) | spec 13.0.0, `spec/modelo.py`, `engine/interprete.py`, `engine/primitivas.py` |
| H2 | opción (a): test de que las sesiones cubren exactamente `[ventana_inicio, ventana_fin)`; el rango de eventos se queda en 07:00; nace **A-43**, no bloqueante, en la hoja justo después de A-35 | `tests/unit/test_huecos_motor.py`, `ambiguedades.yaml`, `scripts/hoja_preguntas.py` |
| H3 | opciones (b) y (c): test de invariancia con el orden de cada clase invertido; aviso de empate en la traza y en el informe | `engine/interprete.py` (`desempate`, `empates`), `engine/motor.py`, `engine/arnes.py` |
| H4 | documentado: gate DESCONOCIDO estricto; intravela pesimista por OHLC hasta tener ticks; bróker y cuenta en las ramas del simulador | ADR-0049 |
| H5 | opción (a): `permite` nunca levanta un `prohibe` | ADR-0049 |
| H6 | opción (c), PROVISIONAL: estrategia de cero cada día, cuenta persistente en el simulador; el resto pendiente de A-25, A-30 y A-38 | ADR-0049 |

**`sesgo_h4_tope_velas` no cambia de estado.** El brief pedía PROVISIONAL «como dice ADR-0044 §2»,
y el registro no tiene ese estado: `Estado` es `CONFIRMED`, `DEFAULT_AMBIGUOUS` o `UNKNOWN`
(ADR-0012). `DEFAULT_AMBIGUOUS` exige una ambigüedad del trader que no existe y `UNKNOWN` lo haría
ilegible para el motor. Se queda `CONFIRMED` con `fuente: decision ADR-0044` y la palabra
PROVISIONAL en su descripción, que ya estaba; crear un estado nuevo es cambio de ADR-0002 y
ADR-0012, y queda para el consultor (ADR-0049, H1.8).

**`lado_de_ruido` con `ambiguo` o `insuficiente` no se define.** RN-005 liga `S` al valor de
`sesgo` y el predicado no tiene lado para esos dos. En esas sesiones RN-033 ya prohíbe lo único que
RN-005 prohíbe, así que RN-005 no puede decidir nada; una guardia exige que `sentido` sea una
LIGADURA, nunca un token, y cuando se escriba la primitiva un sentido fuera de `lado_de_ruido`
tiene que ser un error, no un valor (ADR-0049, H1.7).

## 3. Lo que se midió antes de cerrar H1, y cambió el diseño

ADR-0049 decía en su primera versión que, como RN-003 fija `sesgo` en cada apertura, «no hace falta
ninguna regla que lo borre». **Medido antes de commitear la spec: era falso para la prohibición.**
En el evento de apertura la primera pasada evalúa los `gate` ANTES de que RN-003 (disparador)
vuelva a fijar el hecho, y RN-033 leía el `sesgo` de la sesión anterior —vivo por ADR-0048 §3— y
disparaba una vez sobre él. Sintético: una sesión 11-15 alcista tras una 07-11 ambigua salía con
`disparadas: RN-001, RN-003, RN-033`. Construcción: **RN-033 en 24 sesiones de 84**, las 15
ambiguas más 4 alcistas y 5 bajistas que seguían a una primera sesión ambigua.

El consultor eligió, entre caducar el hecho, documentar y contar 24, o excluir la apertura de
RN-033 (que dejaba sin prohibición el minuto de apertura de una sesión ambigua): **el hecho caduca
al abrir**. `sesgo` declara `caduca: al_abrir_sesion` —token de clase `caducidad`, la caducidad de
hechos que F14b anticipó para `liquidez_tomada` y `zona_perdida`— y el intérprete lo apaga al
empezar el evento de apertura, antes de la primera pasada. No es una retirada del arnés (ADR-0048
§3): la declara la spec, hecho a hecho. Con eso, RN-033 queda en las 15 (§5).

## 4. Los tests nuevos (`tests/unit/test_huecos_motor.py`, 16)

Sobre H4 SINTÉTICAS de un martes de 2030 y la spec real:

- **H1**: una sesión ambigua fija `sesgo` a `ambiguo` y RN-033 prohíbe `buscar_entradas` y
  `abrir_operacion`; una segunda sesión ambigua no hereda el sesgo de la primera; una sesión no
  ambigua tras una ambigua no hereda la prohibición (§3, con el estado de la primera en pie);
  insuficiente prohíbe en las dos sesiones; el hecho solo caduca en la apertura; `vale` en el
  nodo `hecho`; y, cuando `data/` está en la máquina, **la forma y la primitiva coinciden en las
  84 sesiones de construcción** —el valor fijado por RN-003 es el de `sesgo_h4` a la apertura, y
  RN-033 dispara exactamente en las que salen sin lado— (sin las velas se salta, no se finge).
- **Las guardias**: `vale` fuera de los `valores` del hecho o sobre un hecho sin `valores`, un
  valor de hecho que no es token, `sentido: ambiguo` en un predicado con `lado_de_ruido`, y
  `caduca` sin token de caducidad o en un hecho del bróker: todo falla nombrando la regla o el
  hecho. La spec real pasa `comprobar_forma` sin un solo problema.
- **H2**: las sesiones de `kit/config.yaml` empiezan en `ventana_inicio`, acaban en
  `ventana_fin`, son contiguas y sin solape, y su huso es `huso_operativa`.
- **H3**: la misma traza con el orden de cada clase invertido en cuatro escenarios; el aviso
  cuando dos reglas de la misma clase dan SÍ en la misma pasada —y ninguno cuando la spec las
  encadena por un hecho—; el informe lista los avisos y, con el motor real sobre los escenarios
  sintéticos, ninguno.

Los tests del arnés (`test_arnes_motor.py`), de la spec y de la hoja siguen verdes; `make check`
en verde en cada commit, con su sello.

## 5. La línea base nueva frente a la anterior

`docs/validation/HUECOS-MOTOR-LINEA-BASE.txt`, escrito con `uv run botsito motor arnes --salida
docs/validation/HUECOS-MOTOR-LINEA-BASE.txt` (36,2 s, 32,4 MiB), al lado de
`ARNES-MOTOR-LINEA-BASE.txt`, que no se toca.

| | ARNES-MOTOR (ADR-0048) | HUECOS-MOTOR (ADR-0049) |
|---|---|---|
| operaciones del trader / del bot | 77 / 0 | 77 / 0 |
| cobertura · precisión | 0/77 · sin definir | 0/77 · sin definir |
| `sesgo` producido (sesiones del trader) | 43 de 49 | **49 de 49** |
| paradas NO_IMPLEMENTADA | las 9 de siempre, 49 de 49 | las mismas 9, 49 de 49 |
| RN-003 por sesión | alcista 21; ambiguo 6; bajista 22 | alcista 21; ambiguo 6; bajista 22 |
| RN-003 por operación | a favor 58; en contra 12; ambiguo 7 | a favor 58; en contra 12; ambiguo 7 |
| reglas disparadas por sesión | (no se contaban) | RN-001 42 de 84; RN-003 84 de 84; **RN-033 15 de 84, 6 de 49** |
| avisos de orden (H3) | (no existían) | 6, todos `gate RN-001, RN-033` |

Lo que cambia es lo que ADR-0049 pedía: `sesgo` con valor en todas las sesiones —las 6 ambiguas
del trader pasan de `sesgo:no[productoras sin cumplirse]` a `sesgo:si`— y RN-033 disparado
exactamente en las 15 sesiones ambiguas de las 84 corridas (6 de las 49 con operaciones). El
diagnóstico por operación no se mueve: 58/12/7. Cobertura 0, como toca sin bróker.

**Los 6 avisos de H3 son una novedad que el brief no preveía y se reportan tal cual.** Todos son
el evento de las 15:00 de una segunda sesión ambigua: RN-001 (fuera de la ventana) y RN-033
(sesgo ambiguo) dan SÍ en la misma pasada. Los dos son gates que solo prohíben, sin `hace`, y
prohíben lo mismo, así que cuál dispara primero no cambia nada. ADR-0018 §1 bis dice que un
solape deliberado se declara con `complementa`; hoy el intérprete no mira `complementa` al avisar
y RN-033 no lo declara. Las dos cosas —declararlo y que el aviso lo respete— son una decisión
del consultor, fuera de esta rama.

## 6. La hoja de la sesión 02

`ORDEN_SESION_02`, con A-43 justo después de A-35 (21 preguntas):

1. Lo primero: A-35, **A-43**, A-21, A-24, A-42.
2. La liquidez de M15: A-26, A-25, A-32.
3. La orden y el stop: A-36, A-37, A-29, A-30, A-38.
4. La gestión de la operación: A-18, A-13, A-31, A-40, A-33.
5. Para terminar: A-34, A-41, A-39.

Regenerada con `uv run python scripts/hoja_preguntas.py` (en la raíz, no versionada); su test
sigue verde con el orden nuevo.

## 7. Lo que queda abierto, con dueño

- A-34 (el sentido de la doble ruptura): si el trader lo da, `ambiguo` desaparece y RN-033 queda
  para `insuficiente`.
- A-42 y A-43: el reloj y el rango de la sesión.
- A-25, A-30 y A-38: el estado de estrategia entre días.
- El ADR del simulador: H4, la capa de cuenta y H6.
- Un estado PROVISIONAL del registro, si el consultor lo quiere (ADR-0002 y ADR-0012).
- `complementa` entre RN-033 y RN-001, y si el aviso de H3 lo respeta (§5).

## Estado

WAITING_FOR_USER_VALIDATION.
