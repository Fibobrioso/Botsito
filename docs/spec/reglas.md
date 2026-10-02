<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Reglas de la operativa

`spec_version 15.6.0` · hash `2ff8956291b2…`

30 vigentes y 5 descartadas. La precedencia va por CLASE y no por el orden de este documento, que es editorial: `gate` > `terminal` > `disparador` > `fallback` (ADR-0018).

## Vigentes

### RN-001 · la ventana operativa es el horario del trader, no el de las velas

- **Clase**: `gate`
- **Cuando**: la hora de pared, en el reloj que dice reloj_sesiones, esta en el intervalo MEDIO ABIERTO que empieza en ventana_inicio e incluye hasta el instante anterior a ventana_fin, en un dia de dias_operables
- **Entonces**: el bot busca entradas; fuera de ese intervalo no opera
- **Parametros**: `ventana_inicio`, `ventana_fin`, `reloj_sesiones`, `dias_operables`
- **Cita**: `fb-2026-09-09-sesion-01-8741c388` — *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*
- **Decision**: `ADR-0017` — dice mas que su cita, y lo declara
- **Notas**: manda SU horario, no la rejilla. La ventana coincide con dos velas H4 completas 337 dias al año; los otros 28 -del 8 al 28 de marzo y del 25 al 31 de octubre, cuando la UE y EE.UU. no cambian la hora el mismo dia- el ancla se ve a las 22:00 y el bot empieza una hora DENTRO de la vela. Se decidio asi a proposito el 2026-09-10: el trader se sienta a su hora, sea cual sea la fecha (ADR-0017). El titulo anterior afirmaba una alineacion que no es cierta siempre. DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0063, ACEPTADO) EL RELOJ DE LA VENTANA LO ELIGE reloj_sesiones y ya no es huso_operativa, que se queda como reloj del dia de riesgo. Nace en `civil_operativa`, asi que NADA CAMBIA todavia: es el mecanismo que ADR-0059 pedia para poder aplicar, cuando se confirme, la lectura de A-42 -las sesiones en el reloj del grafico- sin mover el corte del dia de la firma

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "ninguno_de": [
          {
            "en_ventana": {
              "dias": "dias_operables",
              "fin": "ventana_fin",
              "inicio": "ventana_inicio",
              "reloj": "reloj_sesiones"
            }
          }
        ]
      },
      {
        "hecho": "detenido_por_tope"
      },
      {
        "hecho": "detenido_por_tope_total"
      },
      {
        "hecho": "detenido_por_cartuchos"
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "buscar_entradas",
      "abrir_operacion"
    ]
  }
}
```

### RN-002 · toda operacion se cierra antes de que termine su vela H4, y lo que quede, al llegar el fin de la ventana

- **Clase**: `terminal`
- **Cuando**: quedan operaciones abiertas y, o bien a la vela H4 en curso -en la rejilla de anclaje_h4- le queda cierre_h4_antelacion o menos para terminar, o bien la hora de pared, en el reloj que dice reloj_sesiones, alcanza ventana_fin
- **Entonces**: se cierra a mercado si cierre_forzoso_fin_ventana
- **Parametros**: `ventana_fin`, `cierre_forzoso_fin_ventana`, `reloj_sesiones`, `anclaje_h4`, `cierre_h4_antelacion`
- **Cita**: `fb-2026-09-29-sesion-03-c38c4aef` — *«siempre menos un minuto, antes de que cierre, pues, como tal, la sesión de cuatro horas»*
- **Decision**: `ADR-0017` — dice mas que su cita, y lo declara
- **Notas**: LA CITA ES LA DE LA PRIMERA RAMA DESDE EL 2026-09-30 (decision del consultor al aceptar ADR-0060): el CORRECT de la sesion 3. La segunda rama, el cierre en ventana_fin, sale de fb-2026-09-09-sesion-01-ffb528d7 («la operativa se cierra a las 3pm en punto»), que era la cita hasta entonces. "las 3pm" son las suyas: la hora de pared en huso_operativa, que cambia con el horario de verano igual que la de cualquiera (ADR-0017) DESDE EL 2026-09-29 (sesion 3, S-1; fb-2026-09-29-sesion-03-c38c4aef, ev-v9-002735-472432b8): el trader cierra TODA operacion un minuto antes de que termine su vela H4 -«siempre menos un minuto, antes de que cierre la sesión de cuatro horas»-, este donde este y sea cual sea el sesgo siguiente; y no tiene hora limite para abrir (A-30, ev-v9-012514-b5b6c84f). DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0060, ACEPTADO) LA FORMA LO HACE: `vence_vela_h4` da SI cuando a la vela H4 en curso le queda cierre_h4_antelacion o menos, sobre la rejilla de anclaje_h4 -la del sesgo, no la de la ventana-, y tambien en el propio limite, para que nada llenado en el ultimo minuto cruce a la vela siguiente. No se toca ventana_fin, que tambien decide que sesiones se operan, y su cierre en punto se conserva como segunda rama. El interruptor es el mismo cierre_forzoso_fin_ventana. LO QUE NO HACE: retirar la orden pendiente al vencer la vela; A-39, de donde sale esto, sigue ABIERTA por el corte de audio de v9 0:28:49-0:29:53 y por la orden pendiente (A-30).

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "cualquiera_de": [
          {
            "vence_vela_h4": {
              "anclaje": "anclaje_h4",
              "antelacion": "cierre_h4_antelacion"
            }
          },
          {
            "alcanza_hora": {
              "hora": "ventana_fin",
              "reloj": "reloj_sesiones"
            }
          }
        ]
      },
      {
        "hecho": "operacion_abierta",
        "liga": "OP"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "cerrar_a_mercado": {
          "de": "OP",
          "si": "cierre_forzoso_fin_ventana"
        }
      }
    ]
  }
}
```

### RN-003 · el sesgo lo fija la vela H4 previa, y solo cambia si rompe su extremo

- **Clase**: `disparador`
- **Cuando**: abre una sesion operativa
- **Entonces**: el sesgo es el de la vela H4 previa cerrada segun sesgo_h4_regla; cambia solo si esa vela rompio el extremo de la anterior, y basta con la mecha; un equal no lo cambia. Se fija AL ABRIR la sesion con las H4 cuyo fin no es posterior a la apertura, y no cambia dentro de ella; romper es superar el extremo, por poco que sea, e igualarlo no rompe. Si la vela rompe los dos extremos, decide el color con que cierra -verde, alcista; roja, bajista-, y solo si cierra sin cuerpo el sesgo es AMBIGUO; si ninguna de las ultimas sesgo_h4_tope_velas rompio, es INSUFICIENTE; con cualquiera de los dos no se opera
- **Parametros**: `sesgo_h4_regla`, `anclaje_h4`, `sesgo_h4_criterio_ruptura`, `sesgo_h4_tope_velas`
- **Cita**: `fb-2026-09-29-sesion-03-31fb311f` — *«si rompe por los dos, como te digo, importa el color de importa el color de la vela.»*
- **Decision**: `ADR-0044` — dice mas que su cita, y lo declara
- **Notas**: LA CITA ES EL CORRECT DE LA SESION 3 DESDE EL 2026-09-30 (decision del consultor al aceptar ADR-0060). Hasta entonces era fb-2026-09-09-sesion-01-8eccf5c0, que sigue sosteniendo la ruptura de un extremo: «si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista». Con un solo extremo roto, el color de la vela NO decide: una vela que cierra roja pero cuya mecha rompio por encima deja el sesgo alcista. La rejilla H4 la fija anclaje_h4 -la medianoche del servidor- y NO huso_operativa: son relojes distintos y se separan 28 dias al año (ADR-0017). En esas semanas la H4 que cierra a mitad de sesion cuenta desde la sesion siguiente. El sesgo AMBIGUO espera a A-34, y el tope y lo demas los decide ADR-0044. Una ruptura de uno o dos puntos puede serlo en la serie del trader y no en la nuestra (A-16). DESDE ADR-0049 (H1) la forma fija `sesgo` tambien a `ambiguo` o `insuficiente` -hasta entonces con esos dos no fijaba nada, y una segunda sesion heredaba el sesgo de la primera, contra ADR-0044 §1-, y la prohibicion de operar con ellos es RN-033. La busqueda hacia atras y el tope van en el predicado `sesgo_h4_al_abrir`, que los nombra; `rompe` sobre la vela previa no los expresaba y la primitiva los hacia por su cuenta DESDE EL 2026-09-29 (sesion 3, A-34 RESUELTA; fb-2026-09-29-sesion-03-617f496a y fb-2026-09-29-sesion-03-31fb311f, ev-v9-001617-4b47e01a): si la vela rompe LOS DOS extremos, el sesgo lo decide el COLOR con que cierra -roja, bajista; verde, alcista-; que el color no decide vale solo para la ruptura de un extremo. La misma sesion confirma que el sesgo no cambia dentro de la sesion (ev-v9-001504-72aa462a) y que basta un pip con mecha (ev-v9-001312-19e45e4a). DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0060, ACEPTADO) EL MOTOR LO HACE: con la doble ruptura sesgo_h4_al_abrir ata el lado del color, y `ambiguo` queda solo para la vela que rompe los dos extremos y cierra sin cuerpo, que el trader no describio.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "abre_sesion_operativa": {}
      },
      {
        "sesgo_h4_al_abrir": {
          "contra": "extremo_de_la_h4_anterior",
          "criterio": "sesgo_h4_criterio_ruptura",
          "que": "vela_h4_previa",
          "tope": "sesgo_h4_tope_velas"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "sentido_de_la_ruptura",
          "hecho": "sesgo"
        }
      }
    ]
  }
}
```

### RN-004 · la liquidez de M15 se toma con cuerpo

- **Clase**: `disparador`
- **Cuando**: el precio alcanza el alto o el bajo de M15 marcado
- **Entonces**: se da por tomada solo si una vela de M1 cierra con cuerpo al otro lado segun liquidez_m15_criterio_toma; una mecha que lo perfore no cuenta
- **Parametros**: `liquidez_m15_criterio_toma`, `toma_antes_de_la_ventana`, `intentos_tras_toma_nueva`, `cartuchos_reinicio`, `max_escenarios_por_sesion`, `orden_pendiente_al_abrir_escenario`
- **Cita**: `fb-2026-09-09-sesion-01-6e15504f` — *«¿Vale con que la vela cierre con el cuerpo por encima del máximo, por debajo del mínimo, o vale con que la mecha lo perfore? Con cuerpo»*
- **Decision**: `ADR-0066` — dice mas que su cita, y lo declara
- **Notas**: solo en M15; en M1 el rompimiento es indiferente. ESTA REGLA NO PUEDE DISPARARSE HOY: su `cuando` lee `liquidez_m15`, y ningun `fijar` de esta spec produce ese token (medido el 2026-09-20). Con ella no se enciende `liquidez_tomada`, del que dependen `se_da_esquema` y `toca_colocar_orden_limite`, asi que RN-008 -que es un `ninguno_de`- prohibe abrir operacion SIEMPRE, y `cartuchos_reinicio: siguiente_liquidez_m15` espera un reinicio que no llega. No se tapa con una regla de marcado inventada. El hueco esta anotado como deuda en PROJECT_STATE e informado en docs/validation/LIQUIDEZ-M15.md. DESDE EL 2026-09-24 A-24 ESTA DECIDIDA (ADR-0045): la liquidez es el pivote de M15 MAS RECIENTE YA FORMADO. El productor sigue sin escribirse porque la spec no define cuando esta formado un pivote, y eso es A-35, bloqueante: no se tapa con un parametro provisional, porque es un mecanismo y no una cifra DESDE EL 2026-09-29 (sesion 3, A-45 RESUELTA; fb-2026-09-29-sesion-03-b2e074e3 y fb-2026-09-29-sesion-03-43e0f90e, ev-v9-004037-ca58e486, ev-v9-004217-c014bfdc): la vela que cierra con cuerpo pasado el nivel de M15 es una vela de M1, no la de 15 minutos; la mecha solo vale para actualizar el punto de breaker en M1. Queda corregido en ese punto lo de «solo en M15; en M1 el rompimiento es indiferente» de estas notas. DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0062, ACEPTADO) EL MOTOR LO HACE: `alcanza_nivel` y `cruza` miran la ultima M1 cerrada, y lo PROVISIONAL de ADR-0054 §4 queda cerrado. SIGUE SIN ACTIVAR que la toma tenga que ocurrir dentro del horario aunque el nivel se formara antes de las 7 (A-43, ev-v9-004533-d075b080): hoy cuenta tambien la M1 que cierra en el instante mismo de la apertura. DESDE EL 2026-10-01 (rama feature/escenarios-por-sesion, ADR-0066) la toma tiene que ser DE LA SESION (`la_toma_es_de_la_sesion`): una liquidez que ya estaba tomada al abrirla no cuenta si se tomo en una sesion anterior del dia (A-46: cada sesion es «un mundo diferente», fb-2026-09-29-sesion-03-5021677e), y si se tomo antes de la primera sesion lo decide toma_antes_de_la_ventana, PROVISIONAL hasta la pregunta 15 de la sesion 4. Medido: sin esta condicion, RN-004 volvia a fijar la toma de la manana en la apertura de la tarde sobre el mismo pivote si el precio seguia pasado (docs/validation/ESCENARIOS-POR-SESION.md §0.2). Y cada toma de una liquidez nueva abre un ESCENARIO (`abrir_escenario`): RN-004 fija el hecho en cada M1 que cierra pasada la linea, asi que la misma liquidez no abre nada; una toma con el escenario vigente vivo la decide intentos_tras_toma_nueva, PROVISIONAL hasta la pregunta 18. Abrir un escenario es el reinicio de los cartuchos (cartuchos_reinicio = siguiente_liquidez_m15)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "alcanza_nivel": {
          "que": "liquidez_m15"
        }
      },
      {
        "cruza": {
          "criterio": "liquidez_m15_criterio_toma",
          "que": "liquidez_m15"
        }
      },
      {
        "la_toma_es_de_la_sesion": {
          "antes_de_la_ventana": "toma_antes_de_la_ventana",
          "criterio": "liquidez_m15_criterio_toma",
          "que": "liquidez_m15"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "si",
          "hecho": "liquidez_tomada"
        }
      },
      {
        "abrir_escenario": {
          "intentos": "intentos_tras_toma_nueva",
          "maximo": "max_escenarios_por_sesion",
          "orden_pendiente": "orden_pendiente_al_abrir_escenario",
          "reinicio": "cartuchos_reinicio"
        }
      }
    ]
  }
}
```

### RN-005 · lo que se desarrolla en el lado de ruido de la liquidez de M15 no es entrada

- **Clase**: `gate`
- **Cuando**: el precio se desarrolla por encima de la liquidez de M15 en sesgo alcista, o por debajo de ella en sesgo bajista
- **Entonces**: no hay entrada
- **Cita**: `ev-v3-001725-bca9714b` — *«la operativa está por encima no por debajo todo lo que haya por debajo es ruido»*
- **Notas**: HASTA EL 2026-09-16 ESTA REGLA ESTABA AL REVES: prohibia abrir "por debajo de la liquidez de M15 en sesgo alcista, o al reves", que es justo donde el trader opera, en los dos sentidos (auditoria del 2026-09-13, hallazgo [2]; verificado otra vez en la revision de diseno de la rama de fidelidad). Es el unico filtro direccional de la spec -`sesgo` lo consumen esta regla y, desde ADR-0049, RN-033- y es un gate, la clase que gana siempre. Con `sesgo` en `ambiguo` o `insuficiente` esta regla no tiene lado que mirar y no lo inventa: RN-033 ya prohibe abrir en esas sesiones (ADR-0049, H1). LO QUE SOSTIENE CADA SENTIDO. Bajista: esta cita (v3 0:17:25) y la que llevaba antes, ev-v3-001600-ed45b091 (v3 0:16:00, "por debajo de esta liquidez de m15 es ruido"), las dos sobre un ejemplo cuyo sesgo H4 es bajista por el contexto de v3 0:15:08, no por la frase citada; la sesion 1 lo repite sin item de evidencia propio (v6 0:18:16-0:19:08). Alcista: la cita del predicado, ev-v1-001306-f98e12e9 (v1 0:13:06, "nuestra operativa tiene que estar por debajo"), con el sesgo alcista dicho en v1 0:01:22 y 0:12:29. Ningun item junta en su propia frase el sesgo y el lado: la ligadura es lectura del tramo. Por eso el lado se nombra en el predicado (`lado_de_ruido`) y no se deduce de "el lado contrario al sesgo", que es la frase que se tradujo al reves DESDE EL 2026-09-29 (sesion 3, A-26 RESUELTA; fb-2026-09-29-sesion-03-fc2c5c1f, ev-v9-001915-d03d1565): cuando el flujo de M15 va contra el sesgo de H4, manda el sesgo y en M15 solo se busca a favor, que es lo que este filtro ya hace.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "hecho": "sesgo",
        "liga": "S"
      },
      {
        "se_desarrolla_en_el_lado_de_ruido": {
          "que": "liquidez_m15",
          "sentido": "S"
        }
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-006 · la orden limite se reubica al completarse cada zona de control

- **Clase**: `disparador`
- **Cuando**: hay una orden limite COLOCADA Y TODAVIA SIN LLENAR, y el precio rompe el extremo anterior, con lo que la zona de control en curso queda completada
- **Entonces**: la orden limite se mueve a la zona recien completada segun reubicacion_cadencia
- **Parametros**: `reubicacion_cadencia`, `zona_control_criterio_completada`
- **Cita**: `fb-2026-09-09-sesion-01-6b29059d` — *«cuando ya me rompe a este nivel de aquí, entonces ya esta orden límite aquí se pasa aquí»*
- **Notas**: no es por vela ni por tiempo; mientras la zona no se completa, el limite no se mueve. La precondicion de que la orden siga pendiente se anadio el 2026-09-10: sin ella esta regla se disparaba sobre EL MISMO evento que RN-014 -"se completa una zona de control"- y, con la operacion ya abierta, reubicaba una limite en paralelo (lo que RN-018 prohibe) en vez de poner el break even. El literal habla de una orden que aun no ha entrado. SEGUNDA CORRECCION, mismo dia: la precondicion se escribio primero como "las operaciones abiertas son cero", que es un PROXY FALSO -tras un stop o un break even la cuenta vuelve a cero y la orden limite ya no existe, porque se lleno-, y ademas metia un numero de negocio en un campo ejecutable. La condicion es que la orden exista y siga pendiente DESDE EL 2026-09-29 (sesion 3): la orden de entrada es una STOP en la ruptura (A-47 RESUELTA, fb-2026-09-29-sesion-03-92a38105); «límite» es vocabulario del trader, que la sigue llamando asi (v9 1:34:46). Sigue viva hasta que aparece otro posible punto de breaker, que la actualiza, y que el precio se aleje no la anula (A-38 RESUELTA, fb-2026-09-29-sesion-03-c7fa3068, ev-v9-013205-85840dcc, ev-v9-013437-ffdd9c87). La vida de la orden stop es la rama 3 de ADR-0056: la cadencia de esta forma se revisa alli. DESDE EL 2026-09-30 (rama feature/F35-orden-stop-pivote, ADR-0064) LA FORMA LO HACE con orden_limite_nace = al_aparecer_punto_de_breaker: la zona se completa al formarse un posible punto de breaker nuevo y reubicar_orden_limite CANCELA la orden, que RN-011 y RN-015 vuelven a colocar en el mismo cierre de M1 en el punto nuevo, con la caja, el stop y el lote recalculados («se cancela y se vuelve a colocar», ADR-0056 §7). La cadencia al_romper no cambia

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "hecho": "orden_limite_pendiente"
      },
      {
        "se_completa_zona_de_control": {
          "criterio": "zona_control_criterio_completada",
          "liga": "Z"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "reubicar_orden_limite": {
          "a": "Z",
          "cadencia": "reubicacion_cadencia"
        }
      }
    ]
  }
}
```

### RN-007 · varias velas de M1 que forman un order block mayor se mapean como una estructura, y una vela casi plana no cuenta

- **Clase**: `disparador`
- **Cuando**: se mapea la estructura en M1
- **Entonces**: se agrupan segun mapeo_dos_velas y el resto se trata como ruido; una vela casi plana, sin color claro, cuenta como si no existiera y sobre ella no se traza punto de breaker
- **Parametros**: `mapeo_dos_velas`
- **Cita**: `fb-2026-09-29-sesion-03-ffab23dc` — *«cuenta como si no existiera no se puede trazar, o sea allí no se puede trazar un punto de breaker»*
- **Notas**: DESDE EL 2026-09-30 (rama feature/reflejar-feedback-s3) la regla cita la correccion de la sesion 3 (E-3). Que varias velas formen una estructura lo sostiene mapeo_dos_velas, que cita fb-2026-09-09-sesion-01-7ee9cabc («sería considerado una estructura»), la cita de esta regla hasta ese dia. DESDE EL 2026-09-29 (sesion 3, E-3; fb-2026-09-29-sesion-03-ffab23dc, ev-v9-013021-ea0db73a): una vela casi plana, sin color claro, «cuenta como si no existiera», y sobre ella no se traza punto de breaker. El trader no dio el umbral de «casi plana» («en EURUSD muy rara vez»). DESALINEADO CON EL MOTOR: el mapeo de M1 no trata esas velas aparte; hacen falta el umbral y una rama de codigo.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_mapea_estructura": {
          "criterio": "mapeo_dos_velas"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "agrupar_estructura": {
          "criterio": "mapeo_dos_velas"
        }
      }
    ]
  }
}
```

### RN-008 · sin ninguno de los esquemas de entrada no hay entrada

- **Clase**: `gate`
- **Cuando**: no se da el breaker ni el otro esquema de entrada
- **Entonces**: no se opera
- **Parametros**: `breaker_m1_criterio_ruptura`, `orden_limite_nace`
- **Cita**: `ev-v4-001844-93dcb658` — *«aquí no hay entrada por el hecho de que el precio no genera el esquema de entrada que ya sabemos cuál es [...] cualquiera de estos dos de aquí»*
- **Decision**: `ADR-0064` — dice mas que su cita, y lo declara
- **Notas**: el 2026-09-10 esta regla se marco `pendiente_definicion` porque el glosario definia breaker de forma circular y su cita dice "el que ya sabemos cual es". ERA UN ERROR DE BUSQUEDA: la definicion SI esta en el corpus, repartida en una docena de items -ev-v4-000243 (los dos esquemas), ev-v3-004201 (el primero no espera retroceso), ev-v3-004230 (el segundo deja zona de control y rompe), ev-v3-011653 (el breaker marca el bloque de origen, sin CHoCH), ev-v4-005910 (en M1 vale mecha o cuerpo; en M15 cuerpo)- y lo que faltaba era recogerla en el glosario. Afirmar una ausencia exige buscarla en la fuente, no en el indice. El 2026-09-17 el criterio de M1 deja de ser prosa de `se_da_esquema` y pasa a breaker_m1_criterio_ruptura, que esta forma lee: era el unico de su familia sin parametro. DESDE EL 2026-09-30 (rama feature/F35-orden-stop-pivote, ADR-0064, que escribe lo que ADR-0056 §7 dejo PROVISIONAL): con orden_limite_nace = al_aparecer_punto_de_breaker esta regla NO FRENA LA COLOCACION de la orden stop. Prohibe abrir sin esquema, y la orden stop solo abre cuando el precio rompe el punto, que es el esquema 1. Con la orden en el esquema sigue como estaba

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "ninguno_de": [
          {
            "se_da_esquema": {
              "criterio": "breaker_m1_criterio_ruptura",
              "cual": "primer_esquema"
            }
          },
          {
            "se_da_esquema": {
              "criterio": "breaker_m1_criterio_ruptura",
              "cual": "segundo_esquema"
            }
          }
        ]
      },
      {
        "ninguno_de": [
          {
            "la_orden_nace_antes_del_esquema": {
              "momento": "orden_limite_nace"
            }
          }
        ]
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-009 · mas zonas de control de las admitidas invalidan el esquema

- **Clase**: `gate`
- **Cuando**: dentro del mismo esquema se desarrollan mas zonas de control de las que admite zonas_control_max_por_esquema
- **Entonces**: no se opera
- **Parametros**: `zonas_control_max_por_esquema`
- **Cita**: `fb-2026-09-09-sesion-01-1b2203b0` — *«solo 1 zona control bro. si hay 2 se descarta»*
- **Notas**: hasta el 2026-09-11 esta regla citaba `ev-v4-001909-54ac2edd` -"aqui no habria un trade usando este modelo aqui por el hecho de que te genera dos zonas de control [...] por lo general solo buscamos uno"-, que describe el caso pero remata con una TENDENCIA, no con una prohibicion; de ahi A-20 y el default. El trader la cierra por escrito y en duro, asi que la regla pasa a citar sus palabras y la evidencia se queda en A-20, que es donde documenta de donde venia la duda

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "zonas_desarrolladas_superan": {
          "tope": "zonas_control_max_por_esquema"
        }
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-010 · una entrada activada sin ruptura se gestiona como cualquier otra

- **Clase**: `disparador`
- **Cuando**: la orden se activa sin que la estructura llegue a romperse, lo que el trader acaba llamando un equal
- **Entonces**: se protege y se deja correr segun salida_sin_ruptura, con el stop en su nivel
- **Parametros**: `salida_sin_ruptura`, `stop_fraccion_caja`
- **Cita**: `fb-2026-09-09-sesion-01-9626d3dd` — *«se activa la entrada y apenas automáticamente [...] proteger a 0.80 [...] o continúa ya nos saca con menos 0.80»*
- **Notas**: hasta el 2026-09-16 su forma decia `se_activa_entrada: {por: equal}` y ademas fijaba `operacion_abierta`. Lo primero usaba un token con tres significados -resultado de cierre, geometria y causa de activacion-; ahora es `activacion_sin_ruptura`. Lo segundo contradecia ADR-0028 §5 -la posicion viva la lee el motor del broker- y se quita (ADR-0032); F14b §0, que lo habia anadido, queda deshecho. Por que via llega una orden a activarse sin ruptura depende de cuando nace la orden: A-29, RESUELTA el 2026-10-02 en `al_aparecer_punto_de_breaker` (fb-2026-09-29-sesion-03-b41ecf9b)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_activa_entrada": {
          "por": "activacion_sin_ruptura"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "gestionar_salida": {
          "segun": "salida_sin_ruptura",
          "stop": "stop_fraccion_caja"
        }
      }
    ]
  }
}
```

### RN-011 · al tocar colocar la orden limite, el lote se dimensiona hasta el stop y el stop se escribe en ella

- **Clase**: `disparador`
- **Cuando**: toca colocar la orden limite en la zona de control que la ancla segun orden_limite_nace, y no hay ni orden limite pendiente ni posicion viva
- **Entonces**: el lote sale de la distancia que va de la entrada a stop_fraccion_caja segun lotaje_base y riesgo_por_operacion sobre base_calculo_riesgo; el stop se escribe EN LA ORDEN segun stop_en_orden_pendiente, en ese mismo stop_fraccion_caja redondeado segun stop_fraccion_redondeo, antes de enviarla; y la orden queda dimensionada en esa zona, a la espera de su objetivo y de su envio
- **Parametros**: `lotaje_base`, `riesgo_por_operacion`, `base_calculo_riesgo`, `stop_en_orden_pendiente`, `stop_fraccion_caja`, `stop_fraccion_redondeo`, `orden_limite_nace`
- **Cita**: `fb-2026-09-09-sesion-01-76fd91ba` — *«el SL se pone junto a la orden limite, no cuando se apertura recien»*
- **Decision**: `ADR-0020` — dice mas que su cita, y lo declara
- **Notas**: hasta el 2026-09-10 esta regla decia que el stop "se mueve inmediatamente" tras activarse la entrada, citando "El primer stop loss es para el calculo del lotaje y el segundo es para proteccion". El trader lo corrigio, y ese es el literal de ahora. Los dos stops de la frase anterior son el del CALCULO y el que se ESCRIBE en la orden, y desde ADR-0020 son EL MISMO: stop_fraccion_caja. El corpus describe lo mismo desde el lado del resultado -"me activa la entrada y si yo protejo a 0.80", ev-v5-000312- y por eso parecia un movimiento posterior. Importa en un caso concreto: un hueco de precio que atraviese la entrada NO puede saltar al stop de rango completo, porque ese nunca llega a estar vivo en el mercado. El 2026-09-11 el consultor cierra el acuerdo final y el lote deja de dimensionarse sobre la caja completa: lo que absorbe riesgo_por_operacion es la distancia hasta el stop, asi que el lote sube un 25 % con stop_fraccion_caja = 0,8. Esa parte de la regla NO la sostiene el literal del trader -que decia lo contrario- y por eso declara `decision`. DESDE EL 2026-09-16 (ADR-0032) esta regla PREPARA la orden y no la da por colocada: su `cuando` era el evento `se_coloca_orden_limite`, que ninguna regla producia, asi que la jornada entera daba cero colocaciones (auditoria del 2026-09-13). Ahora dispara con la condicion de mercado (`toca_colocar_orden_limite`, cuyo momento es A-29, RESUELTA el 2026-10-02 en `al_aparecer_punto_de_breaker`) y deja la zona en `orden_dimensionada`; RN-015 escribe el objetivo y coloca. Son dos reglas para que entre las dos pasen los gates -RN-027 redondea el lote- sin depender de un orden entre disparadores que ADR-0028 no da. Tampoco fija ya `orden_limite_pendiente`: lo lee del broker (ADR-0028 §5). El `ninguno_de` evita una segunda orden con una pendiente viva, que RN-018 no ve porque cuenta posiciones y no ordenes DESDE EL 2026-09-29 (sesion 3): la orden es STOP en la ruptura (A-47, entrada_tipo_orden = stop_en_ruptura, fb-2026-09-29-sesion-03-8f091ed8) y la vela contraria de la que sale el stop se mira en M1 (A-37 RESUELTA, fb-2026-09-29-sesion-03-91eeee94). A-18 en lo firme: el objetivo es 3 veces la distancia del 0 al 1 (base_calculo_objetivo, fb-2026-09-29-sesion-03-f572f1a0) y el lote se calcula del 0 al 0,8 (lotaje_base, fb-2026-09-29-sesion-03-d62c788a), que es lo que esta regla ya hace; y el 0,8 se redondea ALEJANDOSE de la entrada, lo minimo (stop_fraccion_redondeo, fb-2026-09-29-sesion-03-11910e0a). DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0061, ACEPTADO) LA FORMA NOMBRA stop_fraccion_redondeo y el motor lo lee: la distancia de la entrada al stop se redondea al punto entero siguiente, el stop queda un poco mas lejos y el lote, que sale de esa distancia, un poco menor.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "toca_colocar_orden_limite": {
          "liga": "Z",
          "momento": "orden_limite_nace"
        }
      },
      {
        "ninguno_de": [
          {
            "hecho": "orden_limite_pendiente"
          },
          {
            "hecho": "operacion_abierta"
          }
        ]
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "dimensionar_lote": {
          "base": "lotaje_base",
          "riesgo": "riesgo_por_operacion",
          "sobre": "base_calculo_riesgo"
        }
      },
      {
        "escribir_stop_en_la_orden": {
          "donde": "stop_en_orden_pendiente",
          "nivel": "stop_fraccion_caja",
          "redondeo": "stop_fraccion_redondeo"
        }
      },
      {
        "fijar": {
          "a": "Z",
          "hecho": "orden_dimensionada"
        }
      }
    ]
  }
}
```

### RN-012 · el stop cuesta el riesgo entero, y el resto de la caja no es presupuesto

- **Clase**: `disparador`
- **Cuando**: el stop salta
- **Entonces**: la perdida es riesgo_por_operacion sobre base_calculo_riesgo, entera y sin fraccion, porque el lote se dimensiono sobre la distancia hasta stop_fraccion_caja. El tramo que va de stop_fraccion_caja al extremo de la caja no se arriesga nunca: ahi ya esta cerrada
- **Parametros**: `riesgo_por_operacion`, `base_calculo_riesgo`, `stop_fraccion_caja`
- **Complementa**: RN-011
- **Cita**: `fb-2026-09-09-sesion-01-17ed6193` — *«el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8 de la cuenta, ese es el acuerdo final»*
- **Decision**: `ADR-0020` — dice mas que su cita, y lo declara
- **Notas**: HASTA EL 2026-09-11 esta regla decia lo contrario: que la perdida real era MENOR que el riesgo nominal -riesgo_por_operacion x stop_fraccion_caja, 0,4 % con 0,5 y 0,8- porque el lote se dimensionaba sobre la caja completa, y citaba al trader: "La operativa se calcula con el SL normal, pero apenas de abre la operacion se mueve el SL hasta el nivel 0.8 para todos los modelos de entrada" (fb-2026-09-09-sesion-01-c4922acb). El acuerdo final del consultor invierte la base del lotaje (ADR-0020) y con ella esta regla: el stop cuesta el 0,5 % completo. El RR realizado no cambia -sigue siendo objetivo_rr / stop_fraccion_caja = 3,75- porque las dos distancias se escalan igual; lo que cambia es el tamano del lote. INVARIANTE, no parametro: `stop_proteccion_capital` sigue UNKNOWN a proposito para que no haya dos puertas para el mismo numero. Un motor que guarde el riesgo real como dato aparte puede desincronizarlo del stop

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "salta_stop": {}
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "realizar_perdida": {
          "riesgo": "riesgo_por_operacion",
          "sobre": "base_calculo_riesgo"
        }
      }
    ]
  }
}
```

### RN-014 · el break even se pone al romperse la zona de control posterior

- **Clase**: `disparador`
- **Cuando**: tras la entrada se desarrolla otra zona de control y el precio la rompe
- **Entonces**: el stop pasa a la entrada, en el instante del toque segun break_even_condicion
- **Parametros**: `break_even_condicion`, `break_even_criterio_ruptura`
- **Cita**: `fb-2026-09-29-sesion-03-9f506366` — *«apenas toca, pues se pone en B la entrada»*
- **Notas**: DESDE EL 2026-09-30 (rama feature/reflejar-feedback-s3) la regla cita la correccion de la sesion 3, que dice lo mismo que la de la sesion 1 y anade el marco (M1) y el precio (la entrada exacta). La cita anterior, fb-2026-09-09-sesion-01-0ccafcba («apenas toca»), la sigue citando break_even_condicion. el disparador NO es un nivel de precio sino la ruptura de la zona de control que se forma despues de la entrada. A-13 pregunta si esa ruptura deberia exigir cuerpo DESDE EL 2026-09-29 (sesion 3; fb-2026-09-29-sesion-03-9f506366 y fb-2026-09-29-sesion-03-2cff5008): el break even se pone AL TOCAR -«apenas toca, pues se pone en B la entrada»-, mirado en M1, con el stop EXACTAMENTE en la entrada, sin puntos a favor para costes, y despues el stop no se mueve (A-40 RESUELTA, fb-2026-09-29-sesion-03-7a79dcd7). break_even_criterio_ruptura pasa a CONFIRMED en `mecha`, que era su default. A-13 sigue ABIERTA solo por el corte de audio de v9 0:57:00-0:58:06. DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0061, ACEPTADO) EL MOTOR LO EVALUA: `se_completa_zona_de_control` con `posterior_a` deja de ser un hueco y el cableado mueve el stop a la entrada. Hasta la rama feature/be-al-tick lo movia en el cierre de la M1 que toca el punto, no en el tick (ADR-0053 §2.1). DESDE EL 2026-09-30 (ADR-0065, PROVISIONAL) ES AL TICK: con break_even_condicion en `tocar`, el stop pasa a la entrada en el primer tick cuyo BID pasa el mismo nivel; sin ticks, con `cierre` o con el criterio `cuerpo`, sigue en el cierre de la M1. La forma no cambia.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "hecho": "operacion_abierta",
        "liga": "OP"
      },
      {
        "se_completa_zona_de_control": {
          "criterio": "break_even_criterio_ruptura",
          "distinta_de": "OP.zona_de_entrada",
          "liga": "Z",
          "posterior_a": "OP.instante_entrada"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "mover_stop": {
          "a": "OP.precio_entrada",
          "cuando": "break_even_condicion",
          "de": "OP"
        }
      }
    ]
  }
}
```

### RN-015 · el objetivo es fijo, se traza con la orden antes de enviarla y no se mueve

- **Clase**: `disparador`
- **Cuando**: la orden limite ya esta dimensionada en su zona, con su lote y su stop
- **Entonces**: el objetivo se fija en objetivo_rr sobre la distancia que declara base_calculo_objetivo, en la misma orden que ya lleva el stop, y no se extiende (objetivo_extension_activa) ni se sacan parciales (parciales); la orden se coloca en esa zona
- **Parametros**: `objetivo_rr`, `base_calculo_objetivo`, `objetivo_extension_activa`, `parciales`
- **Complementa**: RN-011
- **Cita**: `fb-2026-09-29-sesion-03-3f69a5f7` — *«el objetivo es fijo como bien sabemos bro Ahora no lo gestionamos Es fijo»*
- **Notas**: DESDE EL 2026-09-30 (rama feature/reflejar-feedback-s3) la regla cita el CONFIRM de la sesion 3 sobre el objetivo fijo (G-2). El 1:3 lo sigue sosteniendo objetivo_rr, que cita fb-2026-09-09-sesion-01-7fbbb2e7 («Siempre se fija el 1:3»), la cita de esta regla hasta ese dia. El otro CONFIRM de la sesion 3 sobre esta regla (G-1, fb-2026-09-29-sesion-03-280cf8f7) no cabe en una cita sola y queda anotado mas abajo. la BASE del 1:3 no la dice el literal, y por eso vive en base_calculo_objetivo y no en esta frase (ADR-0014). El objetivo se traza sobre la caja completa y el lote YA NO: desde ADR-0020 el lote se dimensiona hasta stop_fraccion_caja, asi que las dos distancias dejaron de ser la misma. El RR REALIZADO sigue siendo objetivo_rr / stop_fraccion_caja, no objetivo_rr, porque esa razon no depende del lote. Quien mida fidelidad en F26 no debe leer esa diferencia como un fallo del bot: es la mecanica. ev-v4-011951 empuja al otro lado -el trader dice que un ganador cubre "2 o 3" perdidas, que cuadra mejor con medir sobre el riesgo real-, pero es una estimacion redonda hablando de margenes, no una descripcion del calculo; A-18 lo deja a la vista hasta ratificarlo. LA BASE, ANOTADA Y NO CAMBIADA (2026-09-16): las dos premisas con las que ADR-0014 eligio la caja completa estan revocadas -que el stop se mueve tras el llenado (A-11) y que el lote se dimensiona sobre la caja (ADR-0020)-, asi que el argumento "en el instante de trazar la orden solo existe la caja completa" ya no discrimina: en ese instante el stop ya esta escrito en la misma orden. Cambiar la base cambia el RR realizado y queda para el consultor. EL INSTANTE (2026-09-16, ADR-0032): hasta entonces esta regla disparaba al ACTIVARSE la entrada `por: cualquier_esquema`, a pesar de su titulo, y una activacion sin ruptura (RN-010) no casaba con ese token: la posicion nacia y vivia sin objetivo. Ahora el objetivo se escribe en la orden antes de enviarla, en la regla que la coloca, asi que ninguna posicion puede existir sin el. Coloca aqui y no en RN-011 porque los gates tienen que ver la orden con el objetivo ya escrito -RN-026 compara stop y objetivo con el minimo del broker- y porque `colocar_orden_limite` lleva `efecto`: si un gate prohibe abrir, no se envia, y `orden_dimensionada` se apaga igual CONFIRMADA el 2026-09-29 (sesion 3): G-1, no cierra a mano antes del stop -«o bien se gana o bien se pierde, o bien ocurre break-even»- (fb-2026-09-29-sesion-03-280cf8f7); G-2, no deja correr mas alla del objetivo -«el objetivo es fijo»- (fb-2026-09-29-sesion-03-3f69a5f7). La unica salida fuera del objetivo, el stop y el break even es el cierre al vencer la vela H4 (RN-002).

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "hecho": "orden_dimensionada",
        "liga": "Z"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar_objetivo": {
          "extension": "objetivo_extension_activa",
          "multiplo": "objetivo_rr",
          "parciales": "parciales",
          "sobre": "base_calculo_objetivo"
        }
      },
      {
        "colocar_orden_limite": {
          "en": "Z"
        }
      },
      {
        "fijar": {
          "a": "no",
          "hecho": "orden_dimensionada"
        }
      }
    ]
  }
}
```

### RN-016 · el dia se limita por cartuchos, y solo una perdida gasta uno

- **Clase**: `gate`
- **Cuando**: se cierra la operacion
- **Entonces**: suma al contador solo si fue perdida (cartucho_criterio); al llegar a cartuchos_max se deja de operar hasta cartuchos_reinicio
- **Parametros**: `cartuchos_max`, `cartucho_criterio`, `cartuchos_reinicio`
- **Cita**: `fb-2026-09-09-sesion-01-aa2abe65` — *«un intento no es considerado un break even, ¿vale? una entrada invalidada pues tampoco es considerado un intento [...] reentrada después de equal, tampoco es considerado un intento»*
- **Notas**: el contador NO es diario; se reinicia con la siguiente liquidez de M15. DESDE EL 2026-09-16 el cierre lleva `por`: una perdida de una operacion activada SIN RUPTURA no suma -es lo que el trader llama cerrar un equal, "te genera una perdida" (v6 1:23:13-1:23:19), y la reentrada despues de un equal no es un intento (el literal)-; y el break even es su propio resultado (`break_even`), clasificado por mecanismo, asi que unos dolares de comision no lo convierten en perdida. Hasta entonces esa perdida llegaba como `perdida` y gastaba cartucho, contra el literal de esta misma regla. CORREGIDO EL 2026-09-17: la exencion del 2026-09-16 era ANCHA DE MAS. Eximia toda perdida de una operacion activada sin ruptura, tambien la que se va al stop de stop_fraccion_caja y cuesta el riesgo entero, y el trader exime tres casos -break even, entrada invalidada y reentrada despues de un equal- y ninguno es ese: el equal que describe es una salida que no llega al stop. Ahora gasta cartucho todo cierre en que salto ese stop, se activara como se activara, y una perdida SIN stop solo si la operacion vino de un esquema. Que el stop entero de una activacion sin ruptura gaste es LECTURA NUESTRA y es A-31; que no gaste la salida en rojo sin stop de esa activacion, tambien, y es la de RN-019 DESDE EL 2026-09-29 (sesion 3): el contador es de TRES INTENTOS POR LIQUIDEZ, sin tope por dia, y los break even y las entradas invalidadas no cuentan (A-41 RESUELTA, fb-2026-09-29-sesion-03-7b87c3ee y fb-2026-09-29-sesion-03-68a21dc0); y el stop entero de una activacion sin ruptura SI gasta un intento, que era lectura nuestra y ahora es del trader (A-31 RESUELTA, fb-2026-09-29-sesion-03-d36ba0d2). El titulo dice «el dia», pero el contador no es diario. DESDE EL 2026-10-01 (rama feature/escenarios-por-sesion, ADR-0066) ESTA REGLA PUEDE DISPARAR: el acumulador `cartuchos` cuenta los intentos del ESCENARIO vigente de la sesion -la liquidez tomada y sus zonas- en vez de ser un hueco, y detenido_por_cartuchos lo apaga `abrir_escenario` con la siguiente liquidez de M15, que es cartuchos_reinicio. Si una toma nueva con el escenario vivo empieza con los intentos enteros lo decide intentos_tras_toma_nueva (A-25), PROVISIONAL.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "todos_de": [
          {
            "se_cierra_operacion": {
              "por": "cualquier_activacion",
              "resultado": "salto_el_stop"
            }
          },
          {
            "alcanza_tope": {
              "acumulador": "cartuchos",
              "tope": "cartuchos_max"
            }
          }
        ]
      },
      {
        "todos_de": [
          {
            "se_cierra_operacion": {
              "por": "cualquier_esquema",
              "resultado": "perdida"
            }
          },
          {
            "alcanza_tope": {
              "acumulador": "cartuchos",
              "tope": "cartuchos_max"
            }
          }
        ]
      },
      {
        "hecho": "detenido_por_cartuchos"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "hasta_cartuchos_reinicio",
          "hecho": "detenido_por_cartuchos"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-017 · un trade ganador no apaga el dia

- **Clase**: `disparador`
- **Cuando**: la operacion cierra en positivo
- **Entonces**: se sigue operando, con el limite de cartuchos intacto
- **Parametros**: `cartuchos_max`
- **Cita**: `fb-2026-09-09-sesion-01-af02495f` — *«que siga operando, pero que respete la regla de los 3 cartuchos de perdida»*
- **Notas**: corrige lo que se daba por sabido antes de la sesion: la confirmacion R-07 de la hoja, que apunta a ev-v4-004936-d7004417 (ver el anexo del informe de la sesion)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_cierra_operacion": {
          "por": "cualquier_activacion",
          "resultado": "ganancia"
        }
      }
    ]
  },
  "entonces": {
    "permite": [
      "buscar_entradas"
    ]
  }
}
```

### RN-018 · no hay operaciones en paralelo

- **Clase**: `gate`
- **Cuando**: el numero de operaciones abiertas alcanza operaciones_simultaneas_max
- **Entonces**: no se abre ninguna mas; para reentrar hay que haber salido antes
- **Parametros**: `operaciones_simultaneas_max`
- **Cita**: `ev-v4-003710-c753f3d3` — *«para que tú puedas entrar nuevamente o bien te ha tocado stop loss»*
- **Notas**: la cita sigue en el item hasta "con el profit ya no operas mas", pero ESA MITAD quedo revocada en la sesion 1 (RN-017): el trader dijo que un ganador no apaga el dia. El literal se corta donde sigue siendo cierto

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "operaciones_abiertas_alcanzan": {
          "tope": "operaciones_simultaneas_max"
        }
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-019 · se puede reentrar tras un equal sin gastar cartucho

- **Clase**: `disparador`
- **Cuando**: se cierra en negativo la operacion en curso, que se habia activado sin ruptura, sin que la cerrara ningun stop: lo que el trader llama cerrar un equal
- **Entonces**: se puede volver a entrar segun reentrada_tras_equal, por la via normal de colocacion, y ese cierre no suma al contador
- **Parametros**: `reentrada_tras_equal`, `cartucho_criterio`
- **Cita**: `fb-2026-09-09-sesion-01-060cd801` — *«Sí, esto no gasta intentos, me dijiste, ¿no? No»*
- **Notas**: HASTA EL 2026-09-16 NO PODIA DISPARAR NUNCA, por dos motivos. Su forma pedia `se_cierra_operacion: {resultado: equal}`, y el caso que el trader describe cierra con perdida -"te genera una perdida" (v6 1:23:13-1:23:19)-, asi que llegaba como `perdida`, y encima RN-016 gastaba cartucho. Y unia en un `todos_de` ese cierre, que es un evento del broker, con `vuelve_a_dar_el_esquema`, que se evalua al cierre de M1: con las fases de ADR-0028 los dos pulsos no coinciden nunca. Ahora dispara con el cierre solo, reconocido por COMO se activo la operacion, y la reentrada la hace la colocacion de siempre (RN-011 y RN-015) cuando vuelva a tocar, con los gates delante: `reentrar` ya no envia nada. LECTURA NUESTRA, declarada: el trader habla de una entrada activada sin validar que un equal saca (v6 1:22:25-1:23:19); la spec no tiene forma de reconocer el equal en si. Del 2026-09-16 al 2026-09-17 trataba igual TODO cierre de una operacion activada sin ruptura, incluido el stop entero, que el trader no eximio nunca: ahora solo la salida en negativo que no cerro ningun stop, que es la que el describe ("te saque la entrada, te genera una perdida", v6 1:23:13-1:23:19). Si el stop entero de una activacion sin ruptura gasta intento lo pregunta A-31. Cuando se reentra -en cuanto se cierra o al volver a darse la condicion de colocar- depende de A-29, RESUELTA el 2026-10-02 en `al_aparecer_punto_de_breaker` (fb-2026-09-29-sesion-03-b41ecf9b)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_cierra_operacion": {
          "por": "activacion_sin_ruptura",
          "resultado": "perdida"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "reentrar": {
          "cuenta_como": "cartucho_criterio",
          "segun": "reentrada_tras_equal"
        }
      }
    ]
  }
}
```

### RN-020 · el tope porcentual del trader es el unico freno del dia de su operativa

- **Clase**: `gate`
- **Cuando**: la perdida acumulada desde el corte que marca reloj_dia_riesgo -la medianoche civil en huso_operativa, que es tambien la de la firma- alcanza perdida_maxima_diaria sobre base_calculo_perdida_diaria, o perdida_maxima_semanal sobre base_calculo_perdida_semanal
- **Entonces**: se deja de operar hasta el corte siguiente
- **Parametros**: `perdida_maxima_diaria`, `base_calculo_perdida_diaria`, `perdida_maxima_semanal`, `base_calculo_perdida_semanal`, `reloj_dia_riesgo`
- **Cita**: `fb-2026-09-09-sesion-01-bff260ea` — *«De la cuenta basado en el saldo, y que sea en el saldo inicial del día»*
- **Decision**: `ADR-0027` — dice mas que su cita, y lo declara
- **Notas**: OJO a la aritmetica, corregida en la auditoria del 2026-09-09: agotar los cartuchos cuesta tres perdidas, pero el contador NO es diario -se reinicia con la siguiente liquidez de M15 (cartuchos_reinicio)-, asi que no hay cota diaria por esa via: son tres perdidas POR ZONA, y nada limita cuantas zonas se desarrollan entre la apertura y el cierre de la ventana. El tope porcentual no es una red que nunca se toca: es el unico freno del dia DE LA OPERATIVA, y el titulo de esta regla decia lo contrario hasta la auditoria del 2026-09-10. Las dos bases NO son la misma -el dia sobre el saldo inicial del dia, la semana sobre el saldo actual, que es lo que dijo el trader en cada caso-. El corte lo marca reloj_dia_riesgo, que fue un default nuestro en el reloj del servidor hasta el 2026-09-14 (A-19) y ahora es la medianoche civil que dice el reglamento de FTMO (ADR-0027): por eso esta regla ya no nombra broker_dst ni broker_offset_base. Desde ADR-0026 hay OTRO freno, el de la firma (RN-029): no es de la operativa del trader sino de la cuenta, y el motor respeta siempre el mas restrictivo de los dos. LO QUE ESTE TOPE NO HACE (2026-09-16): se comprueba antes de abrir sin descontar la operacion que se abre, asi que se rebasa por construccion -la auditoria del 2026-09-13 lo midio en 4,865 % sobre el 4,5 % ([d1-interprete-04])-. No se cambia su lectura, porque es la que dijo el trader. Lo que impide que ese desbordamiento cueste la cuenta son los frenos de la firma, que saltan antes de su limite y no abren una operacion que no cabe (RN-029, RN-031 y RN-032, ADR-0031)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "alcanza_tope": {
          "acumulador": "perdida_dia",
          "tope": "perdida_maxima_diaria"
        }
      },
      {
        "alcanza_tope": {
          "acumulador": "perdida_semana",
          "tope": "perdida_maxima_semanal"
        }
      },
      {
        "hecho": "detenido_por_tope"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "hasta_el_corte_siguiente",
          "hecho": "detenido_por_tope"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-021 · el spread no se filtra

- **Clase**: `disparador`
- **Cuando**: el spread se ensancha
- **Entonces**: no se filtra (filtro_spread); se opera igual
- **Parametros**: `filtro_spread`
- **Cita**: `fb-2026-09-09-sesion-01-3565552d` — *«a mí me es indiferente si hay noticia o no [...] Sí, incluimos noticias»*
- **Notas**: HASTA EL 2026-09-12 esta regla decia tambien que se opera DURANTE LAS NOTICIAS, y para el trader sigue siendo cierto: opera cuentas propias que no lo prohiben y su estrategia funciona dentro de esos eventos. Del 2026-09-12 al 2026-09-14 esa mitad se fue a RN-028 (ADR-0022) porque la cuenta fondeada podia prohibirlo. Desde ADR-0026 la cuenta es FTMO 2-Step Swing, que no lo restringe: el bot vuelve a operar noticias como el trader, RN-028 queda DESCARTADA y filtro_noticias vale `no`. Esta regla sigue diciendo solo lo del spread

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "contexto_filtrable": {
          "spread": "filtro_spread"
        }
      }
    ]
  },
  "entonces": {
    "permite": [
      "buscar_entradas",
      "abrir_operacion"
    ]
  }
}
```

### RN-022 · cuando la situacion no encaja, el bot se abstiene

- **Clase**: `fallback`
- **Cuando**: no se cumple ninguna regla de entrada
- **Entonces**: no se opera (comportamiento_sin_regla)
- **Parametros**: `comportamiento_sin_regla`
- **Cita**: `fb-2026-09-09-sesion-01-c698bc6a` — *«Que sea fiel a la operativa y no busque nada adicional.»*

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "ninguna_regla_de_entrada_aplica": {}
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "abstenerse": {
          "segun": "comportamiento_sin_regla"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-026 · si el broker no admite el stop donde toca, el bot se abstiene

- **Clase**: `gate`
- **Cuando**: el stop o el limite que pide la spec queda mas cerca del precio que instrumento_stops_level, que viene en puntos y se traduce a precio con instrumento_digitos
- **Entonces**: no se abre la operacion; nunca se aproxima el nivel al minimo que el broker admite
- **Parametros**: `instrumento_stops_level`, `comportamiento_sin_regla`, `instrumento_digitos`
- **Cita**: `fb-2026-09-09-sesion-01-c698bc6a` — *«Que sea fiel a la operativa y no busque nada adicional.»*
- **Decision**: `ADR-0016` — dice mas que su cita, y lo declara
- **Notas**: la decision explicita que pide MASTER_PLAN H.2: rechazo por stops level = abstencion. Mover el stop a donde el broker lo admite seria operar OTRA estrategia con el nombre de esta, y el trader pidio fidelidad, no aproximacion. La cita sostiene el PRINCIPIO -ser fiel y no buscar nada adicional-, no esta regla: el trader nunca hablo del stops level. Lo que la regla decide lo decide ADR-0016. OJO: instrumento_stops_level vale 0 en la demo medida, asi que hoy esta regla no llega a activarse; hay que volver a medirlo en la cuenta fondeada

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "distancia_menor_que": {
          "digitos": "instrumento_digitos",
          "que": "stop_o_limite",
          "tope": "instrumento_stops_level"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "abstenerse": {
          "segun": "comportamiento_sin_regla"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-027 · el lotaje se redondea al escalon del broker, siempre a la baja

- **Clase**: `gate`
- **Cuando**: el lote calculado no es un multiplo de instrumento_lote_paso
- **Entonces**: se redondea hacia abajo al escalon; si queda por debajo de instrumento_lote_minimo, no se opera
- **Parametros**: `instrumento_lote_paso`, `instrumento_lote_minimo`, `instrumento_contrato`
- **Cita**: `fb-2026-09-09-sesion-01-17ed6193` — *«el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8 de la cuenta, ese es el acuerdo final»*
- **Decision**: `ADR-0016` — dice mas que su cita, y lo declara
- **Notas**: a la baja y no al mas cercano: redondear hacia arriba haria arriesgar mas de lo que el trader dijo, y el error se acumularia operacion tras operacion. La cita sostiene DE DONDE sale el lotaje, no la DIRECCION del redondeo, de la que el trader nunca hablo: eso lo decide ADR-0016. Citaba el registro de la sesion 1, revocado el 2026-09-11 por el acuerdo del lotaje (ADR-0020); ahora cita el vigente y el redondeo importa mas que antes, porque el lote es un 25 % mayor sobre la misma caja

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "no_es_multiplo_de": {
          "paso": "instrumento_lote_paso",
          "que": "lote_calculado"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "redondear_lote": {
          "a_la_baja": "si",
          "contrato": "instrumento_contrato",
          "minimo": "instrumento_lote_minimo",
          "paso": "instrumento_lote_paso"
        }
      }
    ]
  }
}
```

### RN-029 · el freno diario de la firma, que salta antes de su limite

- **Clase**: `gate`
- **Cuando**: el equity -firma_magnitud_vigilada- cae hasta el limite del dia de la firma menos firma_margen_seguridad; ese limite es el saldo al corte de reloj_dia_riesgo segun firma_base_perdida_diaria menos firma_perdida_diaria_max del capital saldo_inicial_cuenta
- **Entonces**: se prohibe abrir y buscar entradas, y la detencion dura hasta el corte siguiente. Cerrar lo que quede vivo lo hace la regla complementaria, que solo dispara con una posicion viva
- **Parametros**: `firma_perdida_diaria_max`, `firma_base_perdida_diaria`, `firma_magnitud_vigilada`, `saldo_inicial_cuenta`, `reloj_dia_riesgo`, `firma_margen_seguridad`
- **Cita**: `ev-v4-012524-0ef85a89` — *«5% como drawdown máximo de pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí»*
- **Decision**: `ADR-0026` — dice mas que su cita, y lo declara
- **Notas**: LO QUE LA CITA SOSTIENE y lo que no: sostiene que la cuenta de fondeo tiene sus PROPIOS topes, uno diario y uno total, distintos de los del trader. No sostiene ni las cifras -el trader las dice de memoria, de otra firma y dudando- ni la base, ni la magnitud, ni el corte, ni el margen: eso lo escriben el reglamento de FTMO y ADR-0026, y ADR-0031, y por eso esta regla declara `decision`. El trader cerraba su recuerdo en un 8 % total -el de otra firma-; la cifra vigente es la del reglamento. POR QUE EXISTE aparte de RN-020: el mas restrictivo NO es siempre el del trader. El 4,5 % del trader va sobre el saldo inicial del dia y el 5 % de la firma sobre el capital inicial, asi que con el saldo al empezar el dia por encima de 5.000 / 0,045 = 111.111,11 manda la firma. LLEGAR AL LIMITE DE LA FIRMA ES LA INFRACCION, y por eso desde el 2026-09-16 (ADR-0031) esta regla no dispara en el limite sino en el limite menos firma_margen_seguridad, leyendo el equity (`magnitud` del acumulador). La lectura prospectiva -no abrir una operacion cuyo riesgo no cabe- es otra regla, RN-032, porque no fija detencion. EL LIMITE TOTAL SE FUE A RN-031 el 2026-09-16: esta regla lo alcanzaba en otra rama del `cualquiera_de` y fijaba tambien para el "hasta el corte siguiente", que para el total es falso -la cuenta esta perdida- y solo se mantenia porque el acumulador no se reinicia y la regla volvia a disparar tras el corte. Produce Y LEE `detenido_por_tope`, como RN-020: quien fija un freno tiene que seguir viendolo, o su prohibicion dura un tick (lo exige una guardia). POR QUE NO CIERRA ESTA REGLA (correccion del 2026-09-14): llevaba en su `hace` un `cerrar_a_mercado: {de: OP, si: "si"}` con OP SIN LIGAR y un literal donde RN-002 usa un parametro; y como lee `detenido_por_tope`, habria emitido un cierre en CADA evento mientras el bot esta parado. Ligar OP aqui no se puede -el `cuando` es un `cualquiera_de` y la prohibicion tiene que valer sin posicion-, asi que el cierre vive en RN-030. Desde el 2026-09-16 una guardia (`comprobar_ligaduras`) rechaza aquel OP sin ligar

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "se_acerca_al_limite": {
          "acumulador": "perdida_dia_firma",
          "margen": "firma_margen_seguridad",
          "tope": "firma_perdida_diaria_max"
        }
      },
      {
        "hecho": "detenido_por_tope"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "hasta_el_corte_siguiente",
          "hecho": "detenido_por_tope"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion",
      "buscar_entradas"
    ]
  }
}
```

### RN-030 · al acercarse a un limite de la firma con una posicion viva, se cierra a mercado

- **Clase**: `terminal`
- **Cuando**: el equity -firma_magnitud_vigilada- cae hasta el limite del dia o el limite total de la firma menos firma_margen_seguridad, en los mismos terminos que sus dos frenos, y hay una posicion viva
- **Entonces**: se cierra a mercado esa posicion si firma_cierre_al_tope lo dice
- **Parametros**: `firma_perdida_diaria_max`, `firma_perdida_total_max`, `firma_base_perdida_diaria`, `firma_perdida_total_arrastra`, `firma_magnitud_vigilada`, `saldo_inicial_cuenta`, `reloj_dia_riesgo`, `firma_cierre_al_tope`, `firma_margen_seguridad`
- **Complementa**: RN-029, RN-031
- **Cita**: `ev-v4-012524-0ef85a89` — *«5% como drawdown máximo de pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí»*
- **Decision**: `ADR-0026` — dice mas que su cita, y lo declara
- **Notas**: nace el 2026-09-14 partiendo RN-029, que cerraba a mercado con OP sin ligar y con un literal en `si` (ver sus notas). Aqui el cierre DEPENDE DE LA LIGADURA y no el gate entero: sin posicion viva esta regla no dispara, asi que no emite un cierre por evento mientras el bot esta detenido, y tampoco dispara cuando el freno alcanzado fue el del trader, porque no lee `detenido_por_tope` sino los acumuladores de la firma. Complementa a RN-029 y a RN-031 -mismo disparador, otro efecto- y lo declara. La cita sostiene lo mismo que en RN-029 y nada mas: que la cuenta tiene sus propios topes; el cierre lo decide ADR-0026 y el margen ADR-0031. CLASE (2026-09-16): era `gate` y no prohibe nada, solo cierra; su gemela por efecto, RN-002, es `terminal`. ADR-0018 define el gate como lo que "prohibe o frena" y el terminal como lo que cierra y gana a mover un stop o activar una entrada, que es lo que esta regla necesita frente a RN-014 en el mismo evento. Como `terminal`, `complementa` ya no la exime de nada -los gates de la firma son de otra clase- y se conserva porque dice la verdad: refina a sus dos frenos. Dispara en el limite MENOS firma_margen_seguridad (ADR-0031): cerrar en el propio limite es cerrar con el limite roto. Lo que quedaba del brief anterior -el lector de firma_magnitud_vigilada, el valor permanente del tope total y el `reinicia_con` booleano- esta resuelto en los acumuladores, en RN-031 y en el token `nunca`

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "cualquiera_de": [
          {
            "se_acerca_al_limite": {
              "acumulador": "perdida_dia_firma",
              "margen": "firma_margen_seguridad",
              "tope": "firma_perdida_diaria_max"
            }
          },
          {
            "se_acerca_al_limite": {
              "acumulador": "perdida_total_firma",
              "margen": "firma_margen_seguridad",
              "tope": "firma_perdida_total_max"
            }
          }
        ]
      },
      {
        "hecho": "operacion_abierta",
        "liga": "OP"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "cerrar_a_mercado": {
          "de": "OP",
          "si": "firma_cierre_al_tope"
        }
      }
    ]
  }
}
```

### RN-031 · el freno total de la firma, que no se levanta nunca

- **Clase**: `gate`
- **Cuando**: el equity -firma_magnitud_vigilada- cae hasta el limite total de la firma menos firma_margen_seguridad; ese limite es saldo_inicial_cuenta menos firma_perdida_total_max, y no se mueve mientras firma_perdida_total_arrastra lo diga
- **Entonces**: se prohibe abrir y buscar entradas para siempre: ningun corte de dia ni de semana levanta la detencion. Cerrar lo que quede vivo lo hace la regla complementaria
- **Parametros**: `firma_perdida_total_max`, `saldo_inicial_cuenta`, `firma_perdida_total_arrastra`, `firma_magnitud_vigilada`, `firma_margen_seguridad`
- **Cita**: `ev-v4-012524-0ef85a89` — *«5% como drawdown máximo de pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí»*
- **Decision**: `ADR-0026` — dice mas que su cita, y lo declara
- **Notas**: nace el 2026-09-16 partiendo RN-029, que alcanzaba los dos limites de la firma en ramas de un `cualquiera_de` y fijaba para los dos `detenido_por_tope: hasta_el_corte_siguiente`. Para el total eso era falso: si se alcanza, la cuenta esta perdida, y la detencion solo se mantenia porque el acumulador no se reinicia y la regla volvia a disparar tras el corte -funcionaba por accidente, y dependia de que el acumulador se siguiera evaluando-. ADR-0019 no da semantica a una accion condicionada a una rama, asi que el valor permanente no cabia dentro de RN-029: va en una regla hermana con su propio hecho, `detenido_por_tope_total`, que lee RN-001. Hecho aparte y no otro valor de `detenido_por_tope`: RN-020 y RN-029 leen ese hecho sin mirar su valor y lo reescriben en cada evento, y machacarian el permanente. La cita sostiene lo mismo que en RN-029 y nada mas; el limite, la magnitud, la permanencia y el margen los deciden ADR-0026 y ADR-0031

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "se_acerca_al_limite": {
          "acumulador": "perdida_total_firma",
          "margen": "firma_margen_seguridad",
          "tope": "firma_perdida_total_max"
        }
      },
      {
        "hecho": "detenido_por_tope_total"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "fijar": {
          "a": "permanente",
          "hecho": "detenido_por_tope_total"
        }
      }
    ],
    "prohibe": [
      "abrir_operacion",
      "buscar_entradas"
    ]
  }
}
```

### RN-032 · no se abre una operacion cuyo riesgo no cabe antes del limite de la firma

- **Clase**: `gate`
- **Cuando**: la perdida acumulada de la firma -la del dia o la total, sobre firma_magnitud_vigilada- mas el riesgo de la operacion que se va a abrir, riesgo_por_operacion sobre base_calculo_riesgo, llega al limite menos firma_margen_seguridad
- **Entonces**: no se abre esa operacion. No detiene nada: si la cuenta recupera holgura en el mismo dia, la siguiente puede caber
- **Parametros**: `firma_perdida_diaria_max`, `firma_perdida_total_max`, `firma_base_perdida_diaria`, `firma_perdida_total_arrastra`, `firma_magnitud_vigilada`, `saldo_inicial_cuenta`, `reloj_dia_riesgo`, `firma_margen_seguridad`, `riesgo_por_operacion`, `base_calculo_riesgo`
- **Complementa**: RN-029, RN-031
- **Cita**: `ev-v4-012524-0ef85a89` — *«5% como drawdown máximo de pérdida diaria, creo, y el total es un 7, ¿no? O un 10. 8, 8. Un 8, sí»*
- **Decision**: `ADR-0031` — dice mas que su cita, y lo declara
- **Notas**: nace el 2026-09-16 con ADR-0031. Los topes se comprobaban antes de abrir SIN descontar la operacion que se abre, asi que se rebasaban por construccion: la auditoria del 2026-09-13 midio el del trader en 4,865 % sobre un 4,5 % ([d1-interprete-04], escenario s05a), y con la aritmetica en el borde el diario de la firma podia acabar en 5,475 % y el total en 10,45 %. Esta regla es la lectura PROSPECTIVA, y solo para los limites de la firma: el tope del trader (RN-020) sigue leyendose como el lo dijo. Va aparte de RN-029 y RN-031 porque no fija detencion: prohibe operacion a operacion. Lo que NO cubre -deslizamiento, gap, costes y equity flotante antes de que un cierre se ejecute- es lo que cubre el margen. La cita sostiene lo mismo que en RN-029 y nada mas

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "no_cabe_la_operacion": {
          "acumulador": "perdida_dia_firma",
          "margen": "firma_margen_seguridad",
          "riesgo": "riesgo_por_operacion",
          "sobre": "base_calculo_riesgo",
          "tope": "firma_perdida_diaria_max"
        }
      },
      {
        "no_cabe_la_operacion": {
          "acumulador": "perdida_total_firma",
          "margen": "firma_margen_seguridad",
          "riesgo": "riesgo_por_operacion",
          "sobre": "base_calculo_riesgo",
          "tope": "firma_perdida_total_max"
        }
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "abrir_operacion"
    ]
  }
}
```

### RN-033 · con sesgo ambiguo o insuficiente no se opera

- **Clase**: `gate`
- **Cuando**: el sesgo fijado al abrir la sesion es AMBIGUO o INSUFICIENTE
- **Entonces**: se prohibe buscar entradas y abrir operacion en esa sesion; no fija nada, porque el sesgo lo vuelve a fijar la regla del sesgo en la apertura siguiente
- **Cita**: `ev-v3-000531-4d6375b6` — *«alcistas sólo compras bajistas sólo ventas»*
- **Decision**: `ADR-0049` — dice mas que su cita, y lo declara
- **Notas**: LO QUE LA CITA SOSTIENE: que el sesgo alcista solo compra y el bajista solo vende, o sea que sin un lado no hay direccion en la que buscar entrada. LO QUE NO: que con la vela previa rompiendo los dos extremos, o sin ninguna ruptura en sesgo_h4_tope_velas, no se opere. Eso lo decidio el consultor en ADR-0044 §1-2 -"la mas conservadora donde no habla"- y hasta ADR-0049 vivia solo en la prosa de RN-003, sin forma: RN-005, entonces el unico consumidor de `sesgo`, solo prohibe SI el hecho existe, asi que sin el hecho el bot se quedaba sin filtro direccional, y una segunda sesion ambigua heredaba el sesgo de la primera (medido sobre construccion el 2026-09-25: 15 sesiones ambiguas de 84, 6 de ellas heredando, 0 insuficientes). El sentido de la doble ruptura sigue siendo A-34: si el trader lo da, `ambiguo` desaparece y esta regla queda para `insuficiente` DESDE EL 2026-09-29 (sesion 3, S-1; fb-2026-09-29-sesion-03-1168f036, ev-v9-001529-ac28bb40): «Siempre va a haber un sesgo … no existe un sesgo no claro». Con A-34 RESUELTA la doble ruptura tiene sentido -el color-, asi que `ambiguo` deja de ser del trader; y `insuficiente` tampoco lo es: para el el sesgo es el del ultimo rango, dure lo que dure. DESDE EL 2026-09-30 (rama trabajo/nocturno-01oct, ADR-0060, ACEPTADO) RN-003 ya no produce `ambiguo` con la doble ruptura, que toma el lado del color, y esta regla se queda para lo que el trader no describio: la doble ruptura de una vela sin cuerpo (`ambiguo`) y la falta de ruptura dentro de sesgo_h4_tope_velas (`insuficiente`), que es un tope del proyecto y no suyo. Lo medido sobre construccion esta en ADR-0060. DESDE EL 2026-09-30 (decision del consultor al aceptar ADR-0060): ESTA REGLA ES UNA GUARDIA DEL PROYECTO, NO DEL TRADER. Prohibe solo en los dos casos que el trader no describio -la doble ruptura de una vela sin cuerpo (`ambiguo`, ADR-0060 §2) y ninguna ruptura dentro de sesgo_h4_tope_velas (`insuficiente`, ADR-0044 §2 y ADR-0060 §3)-, con la lectura mas conservadora donde el no habla (ADR-0044 §1). Por eso no cita el CORRECT de la sesion 3 (fb-2026-09-29-sesion-03-1168f036), que dice que siempre hay sesgo, ni cambia de forma.

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "hecho": "sesgo",
        "vale": "ambiguo"
      },
      {
        "hecho": "sesgo",
        "vale": "insuficiente"
      }
    ]
  },
  "entonces": {
    "prohibe": [
      "buscar_entradas",
      "abrir_operacion"
    ]
  }
}
```

### RN-034 · tras una ganadora, el escenario termina y se espera otra liquidez de M15

- **Clase**: `disparador`
- **Cuando**: la operacion cierra en positivo
- **Entonces**: el escenario de esa operacion -la liquidez tomada que la dio- no da mas entradas; la siguiente sale de otra liquidez de M15 que se tome despues
- **Complementa**: RN-017
- **Cita**: `ev-v6-003227-c4efcf49` — *«pues trazamos nuevamente liquidez, o sea, ya aquí está el trade ganador, aquí no buscamos nada, [...] pues tenemos que esperar nuevamente a que se desarrolle la liquidez»*
- **Decision**: `ADR-0066` — dice mas que su cita, y lo declara
- **Notas**: NACE el 2026-10-01 (rama feature/escenarios-por-sesion, ADR-0066) y sustituye la DECISION 2 de ADR-0064 -una sola vida de orden por sesion que llega a llenarse-, que se escribio porque los cartuchos no existian. No contradice RN-017: el dia sigue (un ganador no lo apaga), pero en otra liquidez. Tras una perdida, un break even o un equal el escenario SIGUE con los intentos que le queden (ev-v3-002405-a202dbf6: «nuevamente tiene todavía un gatillo [...] un cartucho»). Tras un break even lo dijo el trader en v4: «los breakeven no se cuenta o sea, si te saca un breakeven es un trade que [...] tienes un cartucho todavía para poder seguir operando» (ev-v4-004832-6543b551, v4 0:48:32-0:48:52); y en la sesion 3, a la pregunta «¿Cuentan los break-even y las entradas invalidadas?», «no cuentan» (ev-v9-013117-c683f9b5, confianza media: el hablante se atribuye por contexto). LA VERSION DE v4 DE QUE EL DIA TERMINA CON LA PRIMERA GANADORA NO ES LA VIGENTE: ev-v4-004936-d7004417 (v4 0:49:36, «apenas tengo el trade positivo ya no opero más») lo rechazo el trader en la sesion 1 (fb-2026-09-09-sesion-01-af02495f, «NO. Que siga operando, pero que respete la regla de los 3 cartuchos de perdida»), y ev-v4-011351-74b8bb39 (v4 1:13:51) y ev-v1-000959-b82650ad los sustituyen ev-v6-000732-f7189541 y ev-v6-000732-5945fd87 («no estamos pausando cuando se dé el trade ganador»). Lo vigente es RN-017 mas esta regla: el dia sigue, en otra liquidez. Complementa a RN-017 con el mismo disparador: una sigue el dia, la otra cierra el escenario, y las dos valen en cualquier orden

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_cierra_operacion": {
          "por": "cualquier_activacion",
          "resultado": "ganancia"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "terminar_escenario": {}
      }
    ]
  }
}
```

### RN-035 · la orden que sigue pendiente al abrir otra sesion se retira (PROVISIONAL)

- **Clase**: `disparador`
- **Cuando**: abre una sesion operativa y queda una orden de la sesion anterior sin llenar
- **Entonces**: se retira, segun orden_pendiente_al_abrir_sesion; la sesion nueva empieza sin escenario
- **Parametros**: `orden_pendiente_al_abrir_sesion`
- **Cita**: `fb-2026-09-29-sesion-03-5021677e` — *«tú básicamente distingues ambas sesiones. O sea, cada uno es un mundo diferente. Claro, exacto.»*
- **Decision**: `ADR-0066` — dice mas que su cita, y lo declara
- **Notas**: NACE el 2026-10-01 (rama feature/escenarios-por-sesion, ADR-0066), PROVISIONAL: que hace el trader con una orden sin llenar al acabar la sesion no lo dijo -el corte de audio de v9 0:28:49-0:29:53 cae en esa respuesta- y es la pregunta 5 de la sesion 4 (A-30 y A-39). La cita es la de la independencia de las sesiones (A-46 RESUELTA), que es lo que sostiene el valor provisional `se_retira`; la otra opcion, `sigue_hasta_ventana_fin`, es lo que hacia el motor hasta hoy (DECISION 3 de ADR-0064): la orden de la manana no se reubicaba con los puntos de la tarde y, como RN-011 no coloca con una orden pendiente, dejaba la tarde sin operar. Una posicion ABIERTA no entra aqui: la cierra RN-002. La opcion de la pregunta 5 «la dejo y la sigo moviendo en la sesión siguiente» no se escribe hasta que el trader la elija

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "abre_sesion_operativa": {}
      },
      {
        "hecho": "orden_limite_pendiente",
        "liga": "ORDEN"
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "retirar_orden_limite": {
          "de": "ORDEN",
          "segun": "orden_pendiente_al_abrir_sesion"
        }
      }
    ]
  }
}
```

## Descartadas

### RN-013 · hay un unico esquema de stop, y vale para cualquier esquema de entrada

- **Clase**: `disparador`
- **Cuando**: se abre la operacion, por el esquema de entrada que sea
- **Entonces**: el stop va a stop_fraccion_caja, sea cual sea el esquema
- **Parametros**: `stop_fraccion_caja`, `stop_en_orden_pendiente`
- **Complementa**: RN-010, RN-011, RN-012
- **Cita**: `fb-2026-09-09-sesion-01-bc829942` — *«tanto primero como segundo esquema de entrada en 0.80, ¿verdad? Sí»*
- **Notas**: hasta el 2026-09-10 existia `stop_segundo_esquema` con el MISMO valor que stop_fraccion_caja: dos puertas para el mismo numero, que es lo que RN-012 prohibe expresamente y ADR-0002 para todo. Ahora es cierto por construccion, no por coincidencia: el parametro del segundo esquema queda UNKNOWN a proposito. DESCARTADA EL 2026-09-16 SIN QUE CAMBIE LO QUE DICE: queda absorbida (ADR-0032). Su forma escribia el stop al LLENARSE la orden -dentro de `se_activa_entrada`, contra su propio verbo "antes de que se active"- y fijaba dos hechos del broker. Quitadas las dos cosas, su `hace` se quedaba vacio. Lo que afirma sigue siendo cierto, y ahora por construccion: RN-011 escribe el stop en la orden sin leer el esquema, asi que no puede haber dos

### RN-023 · no hay colchon de spread separado del stop

- **Clase**: `disparador`
- **Cuando**: se coloca el stop
- **Entonces**: no se suma ningun margen; el nivel del stop ya lo incorpora
- **Parametros**: `stop_fraccion_caja`
- **Cita**: `fb-2026-09-09-sesion-01-08761847` — *«Por temas de Spread ... se reduce al 0.8»*
- **Notas**: por eso `stop_colchon_spread` se queda UNKNOWN. Cierra A-10. La contradiccion mecanica `stop.nivel` sigue ABIERTA a proposito: los items que dicen 0,75 son citas ciertas de lo que el trader hacia antes, y cerrarla exige superseder esos items (F06/F07), no una regla

### RN-024 · no se baja la proteccion segun el porcentaje de vela transcurrido

- **Clase**: `disparador`
- **Cuando**: pasa buena parte de la vela sin que el precio avance
- **Entonces**: no se hace nada; el stop se queda donde esta
- **Cita**: `fb-2026-09-09-sesion-01-728b68da` — *«Descartar esto, se mantiene el SL fijo de 0.8»*
- **Notas**: cierra A-12 y con ella la duda del 40 % / 50 % que arrastraba el corpus. `stop_reduccion_*` se quedan UNKNOWN

### RN-025 · el tercer esquema de entrada queda fuera de la primera version

- **Clase**: `gate`
- **Cuando**: el precio permite anticiparse al segundo esquema
- **Entonces**: no se entra
- **Cita**: `ev-v4-013008-73dcd8c3` — *«solo sería agregar un modelo de entrada más, o sea, no un modelo, sino un esquema de entrada más [...] antes que se desarrolle esta zona de control pues operar»*
- **Notas**: lo explico en v6 entre 0:41:00 y 0:50:11, tramo declarado fuera de la operativa por ambos y no citable (knowledge/corpus/tramos_no_citables.yaml)

### RN-028 · el bot no abre alrededor de una noticia de alto impacto, aunque el trader si lo haga

- **Clase**: `gate`
- **Cuando**: hay una noticia de alto impacto y filtro_noticias dice que se filtra
- **Entonces**: no se abre ninguna operacion. NO es lo que hace el trader -el opera cuentas propias que no lo prohiben y su estrategia funciona dentro de esos eventos-: es una restriccion de la cuenta a la que va el bot
- **Parametros**: `filtro_noticias`
- **Cita**: `fb-2026-09-09-sesion-01-3565552d` — *«a mí me es indiferente si hay noticia o no [...] Sí, incluimos noticias»*
- **Decision**: `ADR-0022` — dice mas que su cita, y lo declara
- **Notas**: La cita dice lo CONTRARIO de lo que esta regla hace, y por eso declara `decision`. Lo que el trader dijo sigue siendo verdad sobre SU operativa y se conserva intacto en RN-021 y en la descripcion de filtro_noticias. Lo que decide ADR-0022 es donde corre el bot: una cuenta fondeada que puede prohibirlo como norma, con la cuenta como sancion aunque la operacion acabe en profit. El propio trader lo aviso en la sesion 1. La CAPACIDAD se conserva: basta poner filtro_noticias en `no` el dia que el bot opere donde se permita. F26 tiene que citar esta regla: si el trader opero una noticia y el bot se abstuvo, NO es un fallo del bot. DESCARTADA el 2026-09-14 (ADR-0026 y la enmienda de ADR-0022): la cuenta elegida es FTMO 2-Step Swing, sin restriccion de noticias, asi que el motivo de esta regla desaparece y el bot opera noticias igual que el trader. Pierde su `forma`, que solo decia `pendiente_definicion: A-17`: una regla descartada no se ejecuta, y A-17 ya no esta abierta. SE CONSERVA como capacidad: si el bot corre algun dia en una cuenta con restriccion (firma_noticias_restringe), se revive esta regla con su condicion definida, filtro_noticias pasa a `regla` y hace falta un calendario economico -precondicion del pre-vuelo de F33-. La divergencia de F26 que citaba tambien desaparece

## Vocabulario

### predicados (27)

- **`abre_sesion_operativa`** — empieza una de las sesiones de la ventana Fuente: `reloj`. Cita `fb-2026-09-09-sesion-01-8741c388`: *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*.
- **`alcanza_hora`** — la hora de pared, en el reloj que dice `reloj`, llega al instante declarado Argumentos: `hora`, `reloj`. Fuente: `reloj`. Cita `fb-2026-09-09-sesion-01-ffb528d7`: *«la operativa se cierra a las 3pm en punto»*.
- **`alcanza_nivel`** — el precio llega al nivel marcado: la ultima vela de M1 cerrada lo toca, aunque sea solo con la mecha Argumentos: `que`. Fuente: `mercado`. Cita `ev-v3-001600-ed45b091`: *«yo no busco entrada aquí todo lo que se desarrolle dentro o sea por debajo de m15 [...] de esta liquidez de m15 es ruido»*.
- **`alcanza_tope`** — un acumulador llega al tope declarado Argumentos: `acumulador`, `tope`. Fuente: `acumulador`. Cita `fb-2026-09-09-sesion-01-bff260ea`: *«De la cuenta basado en el saldo, y que sea en el saldo inicial del día»*.
- **`contexto_filtrable`** — el spread se ensancha por encima de lo tolerable Argumentos: `spread`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-3565552d`: *«a mí me es indiferente si hay noticia o no [...] Sí, incluimos noticias»*.
- **`cruza`** — el precio pasa al otro lado del nivel con el criterio declarado, mirado en la ultima vela de M1 cerrada y no en la de M15 (A-45 RESUELTA en la sesion 3; cierra lo PROVISIONAL de ADR-0054 §4) Argumentos: `que`, `criterio`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-6e15504f`: *«¿Vale con que la vela cierre con el cuerpo por encima del máximo, por debajo del mínimo, o vale con que la mecha lo perfore? Con cuerpo»*.
- **`distancia_menor_que`** — el nivel que pide la spec queda mas cerca del precio que el minimo del broker; el minimo viene en puntos y `digitos` lo traduce a precio Argumentos: `que`, `tope`, `digitos`. Fuente: `bot`. Lo provoca la accion: escribir_stop_en_la_orden, fijar_objetivo. Cita `fb-2026-09-09-sesion-01-c698bc6a`: *«Que sea fiel a la operativa y no busque nada adicional.»*.
- **`en_ventana`** — la hora de pared, en el reloj que dice `reloj`, cae en el intervalo medio abierto [inicio, fin). `reloj` es un selector del registro: dice con cual de sus relojes se cuenta, y el huso de cada reloj vive en su propio parametro (ADR-0063) Argumentos: `inicio`, `fin`, `reloj`, `dias`. Fuente: `reloj`. Cita `fb-2026-09-09-sesion-01-8741c388`: *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*.
- **`la_orden_nace_antes_del_esquema`** — la orden de entrada nace antes de que se de el esquema, segun `momento` (orden_limite_nace): SI con `al_aparecer_punto_de_breaker`, en la que la orden stop espera en el posible punto de breaker y solo se llena cuando el precio lo rompe, que es el esquema 1 (ADR-0056 §7, ADR-0064). Lo lee RN-008 para no frenar la colocacion Argumentos: `momento`. Fuente: `motor`.
- **`la_toma_es_de_la_sesion`** — la liquidez no estaba tomada ya al abrir la sesion: ninguna M1 cerro pasada la linea, con el `criterio` de la toma, entre la formacion del pivote y la apertura. Una toma previa en una sesion anterior del dia no cuenta (A-46, cada sesion es un mundo diferente); una previa a la primera sesion del dia la decide `antes_de_la_ventana` (A-43). Sin ella, RN-004 volvia a fijar la toma de la manana en la apertura de la tarde sobre el mismo pivote si el precio seguia pasado (ADR-0066) Argumentos: `que`, `criterio`, `antes_de_la_ventana`. Fuente: `mercado`. Cita `ev-v9-004533-d075b080`: *«si la liquidez se formó antes de las 7, pero el precio la toma ya dentro. Es valio la entrada, sí.»*.
- **`ninguna_regla_de_entrada_aplica`** — la situacion no encaja en ningun esquema Fuente: `motor`. Cita `fb-2026-09-09-sesion-01-c698bc6a`: *«Que sea fiel a la operativa y no busque nada adicional.»*.
- **`no_cabe_la_operacion`** — el acumulador, sumandole el riesgo de la operacion que se va a abrir (riesgo sobre su base), llega al tope menos el margen. Es la lectura PROSPECTIVA: `alcanza_tope` se comprueba antes de abrir y no descuenta la operacion que se abre, por eso un tope se rebasa por construccion Argumentos: `acumulador`, `tope`, `margen`, `riesgo`, `sobre`. Fuente: `acumulador`.
- **`no_es_multiplo_de`** — el lote calculado no cae en el escalon del broker Argumentos: `que`, `paso`. Fuente: `bot`. Lo provoca la accion: dimensionar_lote. Cita `fb-2026-09-09-sesion-01-17ed6193`: *«el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8 de la cuenta, ese es el acuerdo final»*.
- **`operaciones_abiertas_alcanzan`** — el numero de posiciones vivas llega al tope declarado Argumentos: `tope`. Fuente: `broker`. Lo provoca la accion: colocar_orden_limite. Cita `ev-v4-003710-c753f3d3`: *«ya la respuesta es no o sea, por el hecho de que para que tú puedas entrar nuevamente o bien te ha tocado stop loss»*.
- **`rompe`** — el sujeto supera el extremo de la referencia, con el criterio declarado Argumentos: `que`, `contra`, `criterio`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-8eccf5c0`: *«si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista»*.
- **`salta_stop`** — el precio alcanza el stop y cierra la posicion en perdida Fuente: `broker`. Lo provoca la accion: colocar_orden_limite. Cita `fb-2026-09-09-sesion-01-c4922acb`: *«La operativa se calcula con el SL normal, pero apenas de abre la operacion se mueve el SL hasta el nivel 0.8 para todos los modelos de entrada.»*.
- **`se_acerca_al_limite`** — el acumulador llega al tope menos el margen: el limite de la firma deja de ser el sitio donde se frena, porque llegar a el ya es la infraccion Argumentos: `acumulador`, `tope`, `margen`. Fuente: `acumulador`.
- **`se_activa_entrada`** — la orden limite se llena. `por` dice COMO se activo: por uno de los dos esquemas, o sin que la estructura llegara a romperse (`activacion_sin_ruptura`, lo que el trader acaba llamando cerrar un equal cuando el precio forma el equal y lo saca) Argumentos: `por`. Fuente: `broker`. Lo provoca la accion: colocar_orden_limite. Valores: `por` en `primer_esquema`, `segundo_esquema`, `cualquier_esquema`, `activacion_sin_ruptura`. Cita `fb-2026-09-09-sesion-01-9626d3dd`: *«se activa la entrada y apenas automáticamente [...] proteger a 0.80 [...] o continúa ya nos saca con menos 0.80»*.
- **`se_cierra_operacion`** — la posicion deja de estar viva. `resultado`, por MECANISMO: `salto_el_stop` si la cierra el stop en stop_fraccion_caja; `break_even` si la cierra el stop que RN-014 llevo a la entrada; y si no la cierra ningun stop, `ganancia` o `perdida` por su signo. El P/L neto de costes no cambia la clase. `por`: como se activo la operacion que se cierra (ver se_activa_entrada) Argumentos: `resultado`, `por`. Fuente: `broker`. Lo provoca la accion: colocar_orden_limite. Valores: `por` en `primer_esquema`, `segundo_esquema`, `cualquier_esquema`, `activacion_sin_ruptura`, `cualquier_activacion`; `resultado` en `ganancia`, `perdida`, `break_even`, `salto_el_stop`. Cita `fb-2026-09-09-sesion-01-aa2abe65`: *«un intento no es considerado un break even, ¿vale? una entrada invalidada pues tampoco es considerado un intento [...] reentrada después de equal, tampoco es considerado un intento»*.
- **`se_completa_zona_de_control`** — el precio rompe el punto extremo anterior y deja la zona cerrada Argumentos: `criterio`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-a456bc3f`: *«como sé que una zona de control se ha completado, cuando apenas me generó un rompimiento [...] rompe el punto alto anterior con mecha, con mecha no importa»*.
- **`se_da_esquema`** — el precio forma uno de los dos esquemas de entrada en M1, con la liquidez de M15 ya tomada. `primer_esquema`: rompe directamente, sin retroceso, y el breaker basta. `segundo_esquema`: pequeno retroceso que deja una zona de control, y despues rompe. Los dos marcan el bloque de origen con el breaker (BOS); el CHoCH no se usa. La ruptura en M1 se juzga con `criterio` (breaker_m1_criterio_ruptura); la de M15 es otra cosa y la fija RN-004 Argumentos: `cual`, `criterio`. Fuente: `mercado`. Valores: `cual` en `primer_esquema`, `segundo_esquema`, `cualquier_esquema`. Depende de: liquidez_tomada. Cita `ev-v4-000243-5f8875ce`: *«ya recordamos los dos esquemas que era uno, o bien me hace esto de aquí, rompe o bien directamente rompe el precio como tal o sea sólo con velas rojas y si hace el otro esquema pues con un pequeño retroceso pequeña zona de control y luego rompe»*.
- **`se_desarrolla_en_el_lado_de_ruido`** — el precio se desarrolla en el lado de la liquidez de M15 donde el trader NO busca entrada: por encima si el sesgo es alcista, por debajo si es bajista. Su operativa esta en el otro: por debajo en alcista (ev-v1-001306, v1 0:13:06) y por encima en bajista (ev-v3-001725, v3 0:17:25, sobre un ejemplo cuyo sesgo H4 es bajista por el contexto de 0:15:08, no por la frase citada). Que en alcista lo de ENCIMA sea ruido es simetria del ejemplo bajista, no una frase del trader Argumentos: `que`, `sentido`. Fuente: `mercado`. Lado de ruido: en `alcista`, `por_encima`; en `bajista`, `por_debajo`. Cita `ev-v1-001306-f98e12e9`: *«el precio puede o bien continuar o bien puede hacer lo que quiera, no me importa nuestra operativa tiene que estar por debajo»*.
- **`se_mapea_estructura`** — varias velas de M1 se agrupan como una estructura Argumentos: `criterio`. Fuente: `motor`. Cita `fb-2026-09-09-sesion-01-7ee9cabc`: *«sería considerado una estructura [...] en el lenguaje del bot sería considerado una estructura»*.
- **`sesgo_h4_al_abrir`** — el sesgo H4 al abrir la sesion (ADR-0044): la ultima H4 cerrada -con fin no posterior a la apertura- que supero un extremo de su anterior segun `criterio`, buscada hacia atras como mucho `tope` velas. Ata en `sentido_de_la_ruptura` el lado de esa ruptura -alcista o bajista-. Si la vela rompio LOS DOS extremos, el lado es el del COLOR con que cerro (sesion 3, A-34 RESUELTA; ADR-0060), y solo si cerro sin cuerpo ata `ambiguo`. Si ninguna rompio dentro del tope, ata `insuficiente`. SIEMPRE tiene respuesta: por eso RN-003 fija `sesgo` en cada apertura y ninguna sesion hereda el de la anterior (ADR-0049, H1) Argumentos: `que`, `contra`, `criterio`, `tope`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-8eccf5c0`: *«si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista»*.
- **`toca_colocar_orden_limite`** — llega el momento de colocar la orden limite en una zona de control, segun `momento` (orden_limite_nace): `al_darse_el_esquema`, cuando se da uno de los dos esquemas de entrada (se_da_esquema) y la orden se marca en su bloque de origen; o `al_tomarse_la_liquidez`, cuando la liquidez de M15 ya esta tomada y se completa la primera zona de control en M1, desde la que RN-006 la ira moviendo; o `al_aparecer_punto_de_breaker`, tras la toma, en cuanto hay un posible punto de breaker con caja (orden_stop_punto, caja_bloque) que la sesion no haya usado (ADR-0056 §7, ADR-0064). Ata la zona con `liga` Argumentos: `momento`. Fuente: `mercado`. Depende de: liquidez_tomada. Cita `ev-v3-004201-bfeb3734`: *«Yo no espero ningún retroceso, si se han dado cuenta. Con el breaker ya me basta [...] apenas el breaker, o sea, marco mi orden limit y ya está»*.
- **`vence_vela_h4`** — a la vela H4 que contiene el minuto que acaba de cerrar le queda `antelacion` o menos para terminar, en la rejilla H4 que fija `anclaje` -la del sesgo, la que construye la agregacion de velas- y no en la de la ventana operativa. Vale tambien en el propio limite: lo que se llene en el ultimo minuto de la vela se cierra antes de que empiece la siguiente (ADR-0060) Argumentos: `anclaje`, `antelacion`. Fuente: `reloj`. Cita `fb-2026-09-29-sesion-03-c38c4aef`: *«siempre menos un minuto, antes de que cierre, pues, como tal, la sesión de cuatro horas»*.
- **`zonas_desarrolladas_superan`** — el esquema desarrolla mas zonas de control de las admitidas Argumentos: `tope`. Fuente: `mercado`. Cita `fb-2026-09-09-sesion-01-1b2203b0`: *«solo 1 zona control bro. si hay 2 se descarta»*.

### acciones (17)

- **`abrir_escenario`** — la toma que RN-004 acaba de dar abre un escenario si es de una liquidez NUEVA -otro pivote que el de la toma del escenario vigente- y el vigente ha terminado; con el vigente vivo, lo decide `intentos` (A-25). Con la misma liquidez, que RN-004 vuelve a fijar en cada M1 pasada la linea, no hace nada. Abrir un escenario es el reinicio de los cartuchos (`reinicio`): apaga detenido_por_cartuchos. No abre mas de `maximo` escenarios por sesion (A-46). Y si al abrirlo queda una orden pendiente del escenario anterior, `orden_pendiente` dice si se retira en ese momento o sigue hasta el primer punto de la liquidez nueva, donde la reubica RN-006 (ADR-0066) Argumentos: `intentos`, `reinicio`, `maximo`, `orden_pendiente`.
- **`abstenerse`** — no operar, sin aproximar ni buscar nada adicional Argumentos: `segun`.
- **`agrupar_estructura`** — mapea como una sola estructura las velas de M1 que forman un order block mayor Argumentos: `criterio`.
- **`cerrar_a_mercado`** — cierra la posicion al precio de mercado Argumentos: `de`, `si`.
- **`colocar_orden_limite`** — envia al broker la orden limite en la zona `en`, con el lote (ya redondeado por RN-027), el stop (RN-011) y el objetivo (RN-015) escritos. Es lo que hace verdaderos `orden_limite_pendiente` y, al llenarse, `operacion_abierta` Argumentos: `en`. Lo frena un gate que prohibe: `abrir_operacion`. Cita `ev-v3-004201-bfeb3734`: *«Yo no espero ningún retroceso, si se han dado cuenta. Con el breaker ya me basta [...] apenas el breaker, o sea, marco mi orden limit y ya está»*.
- **`dimensionar_lote`** — calcula el lote a partir del riesgo y la distancia declarada Argumentos: `base`, `riesgo`, `sobre`.
- **`escribir_stop_en_la_orden`** — escribe el stop en la orden que se va a colocar, antes de enviarla (RN-011): en `nivel` de la caja y, cuando ese nivel no cae en un punto exacto, redondeado hacia donde diga `redondeo` Argumentos: `donde`, `nivel`, `redondeo`.
- **`fijar`** — establece un hecho de estado Argumentos: `hecho`, `a`.
- **`fijar_objetivo`** — escribe el objetivo en la orden que se va a colocar, antes de enviarla (RN-015) Argumentos: `multiplo`, `sobre`, `extension`, `parciales`.
- **`gestionar_salida`** — protege y deja correr una entrada que no rompio Argumentos: `segun`, `stop`.
- **`mover_stop`** — cambia el nivel del stop de una posicion viva Argumentos: `de`, `a`, `cuando`.
- **`realizar_perdida`** — contabiliza la perdida efectiva cuando el stop salta Argumentos: `riesgo`, `sobre`.
- **`redondear_lote`** — ajusta el lote al escalon del broker Argumentos: `a_la_baja`, `paso`, `minimo`, `contrato`.
- **`reentrar`** — habilita volver a entrar tras cerrar una operacion activada sin ruptura, sin sumar al contador. NO envia nada por si misma: la orden se vuelve a colocar por la via de todas (RN-011 y RN-015), con su lote, su stop, su objetivo y los gates delante. Hasta el 2026-09-16 decia "vuelve a colocar la orden", y habria sido una segunda puerta al broker sin ninguno de los tres ni ventana para los gates Argumentos: `segun`, `cuenta_como`.
- **`retirar_orden_limite`** — cancela en el broker la orden limite pendiente `de`, si `segun` lo dice. Hasta el 2026-10-01 estaba DECLARADA Y SIN REGLA que la usara: que se hace con una orden pendiente al llegar ventana_fin no lo dice el corpus ni lo cierra ninguna ambiguedad (A-30). Desde entonces la usa RN-035 al abrir una sesion, con `segun` = orden_pendiente_al_abrir_sesion, PROVISIONAL hasta la pregunta 5 de la sesion 4 (ADR-0066) Argumentos: `de`, `segun`.
- **`reubicar_orden_limite`** — mueve la orden pendiente a otra zona Argumentos: `a`, `cadencia`.
- **`terminar_escenario`** — el escenario de la operacion que se cerro no da mas entradas, y se espera otra liquidez de M15 (RN-034, ADR-0066)

### efectos (2)

- **`abrir_operacion`** — colocar una orden o abrir una posicion nueva
- **`buscar_entradas`** — mirar M1 en busca de un esquema de entrada

### hechos (8)

- **`detenido_por_cartuchos`** — los cartuchos estan agotados y no se opera hasta cartuchos_reinicio. Va aparte del tope porque su reinicio es OTRO: la siguiente liquidez de M15, no el corte del dia. Desde el 2026-10-01 (ADR-0066) lo apaga `abrir_escenario`, la accion de RN-004, cuando una toma de una liquidez nueva abre otro escenario: hasta entonces nadie lo apagaba, y si RN-016 hubiera podido disparar habria parado el resto del dia Origen: `regla`. Lo produce: RN-016. Lo consume: RN-001, RN-016. Valores: `hasta_cartuchos_reinicio`.
- **`detenido_por_tope`** — un tope porcentual esta alcanzado -el diario o el semanal del trader (RN-020), o el diario de la firma (RN-029)- y no se abre hasta el corte siguiente. Es un HECHO que dura, no un instante: sin el, la prohibicion solo valia en el tick del evento y nada impedia abrir en el siguiente. Lo leen RN-001, que es el gate maestro, y las dos reglas que lo fijan. El limite TOTAL de la firma ya no lo fija: su detencion no caduca y va en `detenido_por_tope_total` Origen: `regla`. Lo produce: RN-020, RN-029. Lo consume: RN-001, RN-020, RN-029. Valores: `hasta_el_corte_siguiente`.
- **`detenido_por_tope_total`** — el limite TOTAL de la firma esta alcanzado (RN-031): la cuenta esta perdida y ningun corte la devuelve. Hasta el 2026-09-16 lo fijaba RN-029 en `detenido_por_tope` con `hasta_el_corte_siguiente`, y funcionaba por accidente -tras el corte la regla volvia a disparar porque el acumulador no se reinicia-. Va en un hecho aparte y no como otro valor del mismo: RN-020 y RN-029 leen `detenido_por_tope` sin mirar su valor y lo reescriben en cada evento, asi que machacarian el permanente Origen: `regla`. Lo produce: RN-031. Lo consume: RN-001, RN-031. Valores: `permanente`.
- **`liquidez_tomada`** — la liquidez de M15 marcada ya se ha tomado con cuerpo (RN-004). Es la PRECONDICION de los dos esquemas de entrada y de colocar la orden: sin ella no se mira M1. Hasta el 2026-09-11 esta condicion vivia solo en la prosa de `se_da_esquema`, y RN-004 fijaba un hecho que ninguna forma leia: un motor que implementara `forma` habria entrado sin esperar la toma. Lo consumen los predicados `se_da_esquema` y `toca_colocar_orden_limite` (`depende_de`), no una regla. CADUCA AL ABRIR CADA SESION desde el 2026-09-30 (rama trabajo/nocturno-01oct): para el trader cada sesion es un escenario propio -«cada uno es un mundo diferente», A-46 RESUELTA, fb-2026-09-29-sesion-03-5021677e-, asi que una toma de la primera sesion no vale en la segunda. Era la deuda de ADR-0055 §4: con la toma de la manana viva, RN-008 y RN-009 leian esa toma en la segunda sesion y RN-011 no podia disparar, porque su breaker ya habia pasado. DESDE EL 2026-10-01 (ADR-0066) la caducidad no basta sola: RN-004 tampoco lo vuelve a fijar sobre una liquidez que ya estaba tomada al abrir la sesion (`la_toma_es_de_la_sesion`), y cada toma de una liquidez nueva abre un ESCENARIO de la sesion (`abrir_escenario`): el hecho dice que hay toma en la sesion, y el escenario, cual es y cuantos intentos le quedan Origen: `regla`. Lo produce: RN-004. Lo consume: predicado se_da_esquema, predicado toca_colocar_orden_limite. Valores: `si`.
- **`operacion_abierta`** — hay una posicion viva Origen: `broker`. Lo decide ADR-0028. Lo provoca la accion: colocar_orden_limite. Lo consume: RN-002, RN-011, RN-014, RN-030.
- **`orden_dimensionada`** — la orden limite ya tiene lote y stop (RN-011) y espera su objetivo y su envio (RN-015). Guarda la ZONA en la que se va a colocar. Existe porque ADR-0028 no ordena dos reglas de la misma clase dentro de un evento: sin este hecho, la que coloca podia disparar antes que la que dimensiona, y entre las dos tienen que pasar los gates (RN-027 redondea el lote). RN-015 lo apaga aunque un gate prohiba colocar, asi que nunca sobrevive al evento (ADR-0032) Origen: `regla`. Lo produce: RN-011, RN-015. Lo consume: RN-015.
- **`orden_limite_pendiente`** — hay una orden colocada y todavia sin llenar Origen: `broker`. Lo decide ADR-0028. Lo provoca la accion: colocar_orden_limite. Lo consume: RN-006, RN-011, RN-035.
- **`sesgo`** — el sentido en el que se busca entrada, o que no lo hay: `ambiguo` e `insuficiente` (ADR-0044) son valores del hecho desde ADR-0049, y con ellos RN-033 prohibe operar. Lo fija RN-003 en CADA apertura de sesion y CADUCA al abrir: sin la caducidad, la primera pasada del evento de apertura evaluaba los gates con el sesgo de la sesion anterior todavia vivo y RN-033 disparaba una vez sobre el (medido el 2026-09-25 sobre construccion: en 24 sesiones de 84, y solo 15 eran ambiguas). Asi nunca se hereda de la sesion anterior, ni el valor ni la prohibicion Origen: `regla`. Lo produce: RN-003. Lo consume: RN-005, RN-033. Valores: `sentido_de_la_ruptura`, `ambiguo`, `insuficiente`.

### acumuladores (5)

- **`cartuchos`** — perdidas que cuentan como intento, en el escenario vigente de la sesion: los cierres de las ordenes de sus zonas que nombran las dos ramas de RN-016. Como cada liquidez nueva abre otro escenario (`abrir_escenario`), el contador vuelve a empezar con la siguiente liquidez de M15 sin que nadie lo ponga a cero (ADR-0066); hasta el 2026-10-01 era un hueco con nombre y RN-016 no podia disparar Base: `cartucho_criterio`. Se reinicia con: `cartuchos_reinicio`. Cita `fb-2026-09-09-sesion-01-e3eedcaa`: *«»*.
- **`perdida_dia`** — perdida acumulada desde el corte del dia de riesgo Base: `base_calculo_perdida_diaria`. Se reinicia con: `reloj_dia_riesgo`. Cita `fb-2026-09-09-sesion-01-462134c7`: *«»*.
- **`perdida_dia_firma`** — caida de la magnitud vigilada (equity) por debajo del saldo al corte diario; ese corte lo marca reloj_dia_riesgo y la base la declara firma_base_perdida_diaria. El tope es un porcentaje del capital INICIAL, no del saldo del corte (ADR-0026) Base: `firma_base_perdida_diaria`. Se reinicia con: `reloj_dia_riesgo`. Magnitud vigilada: `firma_magnitud_vigilada`.
- **`perdida_semana`** — perdida acumulada desde el corte de la semana Base: `base_calculo_perdida_semanal`. Se reinicia con: `reloj_dia_riesgo`. Cita `fb-2026-09-09-sesion-01-a85b6bc7`: *«»*.
- **`perdida_total_firma`** — caida de la magnitud vigilada (equity) por debajo del capital inicial (saldo_inicial_cuenta). No se reinicia nunca, y la base no sigue al maximo mientras firma_perdida_total_arrastra valga false, que es lo que dice el programa 2-Step (ADR-0026) Base: `saldo_inicial_cuenta`. Se reinicia con: `nunca`. Magnitud vigilada: `firma_magnitud_vigilada`. La base sigue al maximo segun: `firma_perdida_total_arrastra`.

### tokens (31)

- **`OP`** — la operacion en curso; sus campos se nombran con punto (`OP.precio_entrada`)
- **`ORDEN`** — la orden pendiente, ligada al hecho orden_limite_pendiente (RN-035, ADR-0066); como OP, se liga al valor del hecho y la accion la busca en el broker, donde solo puede haber una
- **`activacion_sin_ruptura`** — la orden se lleno sin que la estructura llegara a romperse (RN-010, A-3). Si despues el precio forma un equal y saca la posicion, es lo que el trader llama cerrar un equal (RN-019)
- **`al_abrir_sesion`** — el hecho caduca al empezar el evento de apertura de cada sesion, antes de la primera pasada: ningun gate lee el de la sesion anterior (ADR-0049, H1). Lo declaran `sesgo`, que RN-003 vuelve a fijar en ese mismo evento, y desde el 2026-09-30 `liquidez_tomada`, que se queda apagado hasta que la sesion tome su propia liquidez (A-46 RESUELTA) Clase: `caducidad`.
- **`ambiguo`** — valor de `sesgo` cuando la H4 que lo fija rompio LOS DOS extremos de su anterior y cerro SIN CUERPO, sin color que decida (ADR-0044 §1, ADR-0060): no hay lado, y RN-033 prohibe operar. Con cuerpo, la doble ruptura toma el lado del color (A-34 RESUELTA) y no es `ambiguo`
- **`break_even`** — salto el stop que RN-014 llevo a la entrada. Se clasifica por MECANISMO, no por el P/L neto: con comisiones o deslizamiento cierra unos dolares en negativo y sigue siendo un break even, que no gasta cartucho (cartucho_criterio)
- **`cualquier_activacion`** — cualquier forma de activarse, por un esquema o sin ruptura
- **`cualquier_esquema`** — cualquiera de los dos esquemas de entrada, sin distinguirlos. NO incluye una activacion sin ruptura, que no es un esquema
- **`extremo_de_la_h4_anterior`** — el maximo o el minimo de la vela H4 previa, segun el sentido
- **`ganancia`** — la operacion cerro en positivo sin que la cerrara ningun stop
- **`hasta_cartuchos_reinicio`** — la detencion dura hasta el reinicio que diga `cartuchos_reinicio` Clase: `duracion`.
- **`hasta_el_corte_siguiente`** — la detencion dura hasta el siguiente corte del dia o de la semana de riesgo Clase: `duracion`.
- **`instante_entrada`** — campo de OP, el momento en que se lleno la orden
- **`insuficiente`** — valor de `sesgo` cuando ninguna de las ultimas sesgo_h4_tope_velas H4 rompio un extremo de su anterior (ADR-0044 §2): no hay lado, y RN-033 prohibe operar
- **`liquidez_m15`** — la liquidez marcada en M15 que hay que tomar antes de mirar M1. ES UN NIVEL, no una banda: medido en pantalla el 2026-09-20 (v4 0:57:06, fr-v4-9ad0ebb8/3426000) lo que queda dibujado es una LINEA horizontal etiquetada "15 lq"; el trader dice que le es indiferente desde cual de los puntos anteriores la marque porque considera liquidez todo lo que hay entre ellos (ev-v4-005644-e06ef304), pero lo que deja en el grafico es un nivel, que es lo que `alcanza_nivel` y `cruza` necesitan. LA MARCA LA PONE UNA PERSONA: ninguna regla de esta spec produce este token -no hay `fijar` que lo escriba- y por eso RN-004 no puede dispararse. Que pivote se marca lo decide A-24, DECIDIDA por ADR-0045: el MAS RECIENTE YA FORMADO. Cuando esta formado es A-35, y hasta que se responda la regla no se escribe: escribir aqui una inventada seria hacer pasar por metodo del trader lo que decide el plan. La vela que lo marca es contraria al FLUJO DE M15, no al sesgo de H4 (ev-v3-001204-889179d2, ev-v4-003451-d750e553, ev-v6-003701-7613b381, ev-v3-011147-fa2e6984: "seria solo M15, M15 y ya"); que pasa cuando ese flujo va contra el sesgo de H4 es A-26
- **`lote_calculado`** — el lote que acaba de calcular `dimensionar_lote`, antes de redondear
- **`no`** — apaga un hecho de estado. Va ENTRECOMILLADO en el YAML a proposito: sin comillas, `no` es el booleano falso de YAML 1.1 mientras que `si` es una cadena, y la misma casilla de la misma regla acababa con dos tipos distintos (RN-013, encontrado el 2026-09-12)
- **`nunca`** — el acumulador no se reinicia. Nace el 2026-09-16 para `perdida_total_firma`, que ponia en `reinicia_con` un parametro booleano -firma_perdida_total_arrastra- donde los demas llevan un reloj o un evento Clase: `reinicio`.
- **`perdida`** — la operacion cerro en negativo sin que la cerrara ningun stop: un cierre a mercado, o la salida por un equal que describe el trader (v6 1:23:13-1:23:19), que no llega al stop
- **`permanente`** — la detencion no caduca: ningun corte de dia ni de semana la levanta. Es la del limite TOTAL de la firma, cuya infraccion pierde la cuenta (RN-031, ADR-0026) Clase: `duracion`.
- **`por_debajo`** — el lado de un nivel que queda por debajo del precio
- **`por_encima`** — el lado de un nivel que queda por encima del precio
- **`precio_entrada`** — campo de OP, el precio al que se lleno la orden
- **`primer_esquema`** — el primer esquema de entrada
- **`salto_el_stop`** — la cerro el stop en stop_fraccion_caja: la perdida del riesgo entero (RN-012), sea cual sea el P/L neto de deslizamiento y costes. Gasta cartucho sea cual sea la activacion (RN-016)
- **`segundo_esquema`** — el segundo esquema de entrada
- **`sentido_de_la_ruptura`** — el lado hacia el que rompio la referencia; es lo que fija el hecho `sesgo`. Lo ata `sesgo_h4_al_abrir`, que cuando no hay lado ata en su lugar `ambiguo` o `insuficiente` (ADR-0049)
- **`si`** — enciende un hecho de estado (`fijar`) o activa una opcion de una accion
- **`stop_o_limite`** — el nivel al que llega el precio, sea el stop o el objetivo
- **`vela_h4_previa`** — la vela H4 cerrada inmediatamente anterior al anclaje
- **`zona_de_entrada`** — campo de OP, la zona de control desde la que se entro
