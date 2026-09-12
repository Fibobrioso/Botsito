<!-- GENERADO por `botsito spec docs`. No editar a mano: `make check` lo comprueba. -->

# Reglas de la operativa

`spec_version 10.0.0` · hash `f429867bee02…`

25 vigentes y 3 descartadas. La precedencia va por CLASE y no por el orden de este documento, que es editorial: `gate` > `terminal` > `disparador` > `fallback` (ADR-0018).

## Vigentes

### RN-001 · la ventana operativa es el horario del trader, no el de las velas

- **Clase**: `gate`
- **Cuando**: la hora de pared en huso_operativa esta en el intervalo MEDIO ABIERTO que empieza en ventana_inicio e incluye hasta el instante anterior a ventana_fin, en un dia de dias_operables
- **Entonces**: el bot busca entradas; fuera de ese intervalo no opera
- **Parametros**: `ventana_inicio`, `ventana_fin`, `huso_operativa`, `dias_operables`
- **Cita**: `fb-2026-09-09-sesion-01-8741c388` — *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*
- **Decision**: `ADR-0017` — dice mas que su cita, y lo declara
- **Notas**: manda SU horario, no la rejilla. La ventana coincide con dos velas H4 completas 337 dias al año; los otros 28 -del 8 al 28 de marzo y del 25 al 31 de octubre, cuando la UE y EE.UU. no cambian la hora el mismo dia- el ancla se ve a las 22:00 y el bot empieza una hora DENTRO de la vela. Se decidio asi a proposito el 2026-09-10: el trader se sienta a su hora, sea cual sea la fecha (ADR-0017). El titulo anterior afirmaba una alineacion que no es cierta siempre

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
              "huso": "huso_operativa",
              "inicio": "ventana_inicio"
            }
          }
        ]
      },
      {
        "hecho": "detenido_por_tope"
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

### RN-002 · al llegar el fin de la ventana se cierra lo que quede abierto

- **Clase**: `terminal`
- **Cuando**: la hora de pared en huso_operativa alcanza ventana_fin y quedan operaciones abiertas
- **Entonces**: se cierra a mercado si cierre_forzoso_fin_ventana
- **Parametros**: `ventana_fin`, `cierre_forzoso_fin_ventana`, `huso_operativa`
- **Cita**: `fb-2026-09-09-sesion-01-ffb528d7` — *«la operativa se cierra a las 3pm en punto»*
- **Decision**: `ADR-0017` — dice mas que su cita, y lo declara
- **Notas**: "las 3pm" son las suyas: la hora de pared en huso_operativa, que cambia con el horario de verano igual que la de cualquiera (ADR-0017)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "alcanza_hora": {
          "hora": "ventana_fin",
          "huso": "huso_operativa"
        }
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
- **Entonces**: el sesgo es el de la vela H4 previa cerrada segun sesgo_h4_regla; cambia solo si esa vela rompio el extremo de la anterior, y basta con la mecha; un equal no lo cambia
- **Parametros**: `sesgo_h4_regla`, `anclaje_h4`, `sesgo_h4_criterio_ruptura`
- **Cita**: `fb-2026-09-09-sesion-01-8eccf5c0` — *«si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista»*
- **Notas**: el color de la vela NO decide: una vela que cierra roja pero cuya mecha rompio por encima deja el sesgo alcista. La rejilla H4 la fija anclaje_h4 -la medianoche del servidor- y NO huso_operativa: son relojes distintos y se separan 28 dias al año (ADR-0017)

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "abre_sesion_operativa": {}
      },
      {
        "rompe": {
          "contra": "extremo_de_la_h4_anterior",
          "criterio": "sesgo_h4_criterio_ruptura",
          "que": "vela_h4_previa"
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
- **Entonces**: se da por tomada solo si una vela cierra con cuerpo al otro lado segun liquidez_m15_criterio_toma; una mecha que lo perfore no cuenta
- **Parametros**: `liquidez_m15_criterio_toma`
- **Cita**: `fb-2026-09-09-sesion-01-6e15504f` — *«¿Vale con que la vela cierre con el cuerpo por encima del máximo, por debajo del mínimo, o vale con que la mecha lo perfore? Con cuerpo»*
- **Notas**: solo en M15; en M1 el rompimiento es indiferente

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
      }
    ]
  }
}
```

### RN-005 · lo que ocurre al otro lado de la liquidez de M15 es ruido

- **Clase**: `gate`
- **Cuando**: el precio se desarrolla por debajo de la liquidez de M15 en sesgo alcista, o al reves
- **Entonces**: no hay entrada
- **Cita**: `ev-v3-001600-ed45b091` — *«yo no busco entrada aquí todo lo que se desarrolle dentro o sea por debajo de m15 [...] de esta liquidez de m15 es ruido»*

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
        "esta_al_otro_lado_de": {
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
- **Notas**: no es por vela ni por tiempo; mientras la zona no se completa, el limite no se mueve. La precondicion de que la orden siga pendiente se anadio el 2026-09-10: sin ella esta regla se disparaba sobre EL MISMO evento que RN-014 -"se completa una zona de control"- y, con la operacion ya abierta, reubicaba una limite en paralelo (lo que RN-018 prohibe) en vez de poner el break even. El literal habla de una orden que aun no ha entrado. SEGUNDA CORRECCION, mismo dia: la precondicion se escribio primero como "las operaciones abiertas son cero", que es un PROXY FALSO -tras un stop o un break even la cuenta vuelve a cero y la orden limite ya no existe, porque se lleno-, y ademas metia un numero de negocio en un campo ejecutable. La condicion es que la orden exista y siga pendiente

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

### RN-007 · varias velas de M1 que forman un order block mayor se mapean como una estructura

- **Clase**: `disparador`
- **Cuando**: se mapea la estructura en M1
- **Entonces**: se agrupan segun mapeo_dos_velas y el resto se trata como ruido
- **Parametros**: `mapeo_dos_velas`
- **Cita**: `fb-2026-09-09-sesion-01-7ee9cabc` — *«sería considerado una estructura [...] en el lenguaje del bot sería considerado una estructura»*

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
- **Cita**: `ev-v4-001844-93dcb658` — *«aquí no hay entrada por el hecho de que el precio no genera el esquema de entrada que ya sabemos cuál es [...] cualquiera de estos dos de aquí»*
- **Notas**: el 2026-09-10 esta regla se marco `pendiente_definicion` porque el glosario definia breaker de forma circular y su cita dice "el que ya sabemos cual es". ERA UN ERROR DE BUSQUEDA: la definicion SI esta en el corpus, repartida en una docena de items -ev-v4-000243 (los dos esquemas), ev-v3-004201 (el primero no espera retroceso), ev-v3-004230 (el segundo deja zona de control y rompe), ev-v3-011653 (el breaker marca el bloque de origen, sin CHoCH), ev-v4-005910 (en M1 vale mecha o cuerpo; en M15 cuerpo)- y lo que faltaba era recogerla en el glosario. Afirmar una ausencia exige buscarla en la fuente, no en el indice

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "ninguno_de": [
      {
        "se_da_esquema": {
          "cual": "primer_esquema"
        }
      },
      {
        "se_da_esquema": {
          "cual": "segundo_esquema"
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
- **Cuando**: la orden se activa por un equal y la estructura no llega a romperse
- **Entonces**: se protege y se deja correr segun salida_sin_ruptura, con el stop en su nivel
- **Parametros**: `salida_sin_ruptura`, `stop_fraccion_caja`
- **Cita**: `fb-2026-09-09-sesion-01-9626d3dd` — *«se activa la entrada y apenas automáticamente [...] proteger a 0.80 [...] o continúa ya nos saca con menos 0.80»*

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_activa_entrada": {
          "por": "equal"
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

### RN-011 · el lote se dimensiona hasta el stop, y la orden nace con ese mismo stop

- **Clase**: `disparador`
- **Cuando**: se coloca la orden limite
- **Entonces**: el lote sale de la distancia que va de la entrada a stop_fraccion_caja segun lotaje_base y riesgo_por_operacion sobre base_calculo_riesgo; el stop viaja EN LA ORDEN segun stop_en_orden_pendiente, en ese mismo stop_fraccion_caja, antes de que la entrada se active
- **Parametros**: `lotaje_base`, `riesgo_por_operacion`, `base_calculo_riesgo`, `stop_en_orden_pendiente`, `stop_fraccion_caja`
- **Cita**: `fb-2026-09-09-sesion-01-76fd91ba` — *«el SL se pone junto a la orden limite, no cuando se apertura recien»*
- **Decision**: `ADR-0020` — dice mas que su cita, y lo declara
- **Notas**: hasta el 2026-09-10 esta regla decia que el stop "se mueve inmediatamente" tras activarse la entrada, citando "El primer stop loss es para el calculo del lotaje y el segundo es para proteccion". El trader lo corrigio, y ese es el literal de ahora. Los dos stops de la frase anterior son el del CALCULO y el que se ESCRIBE en la orden, y desde ADR-0020 son EL MISMO: stop_fraccion_caja. El corpus describe lo mismo desde el lado del resultado -"me activa la entrada y si yo protejo a 0.80", ev-v5-000312- y por eso parecia un movimiento posterior. Importa en un caso concreto: un hueco de precio que atraviese la entrada NO puede saltar al stop de rango completo, porque ese nunca llega a estar vivo en el mercado. El 2026-09-11 el consultor cierra el acuerdo final y el lote deja de dimensionarse sobre la caja completa: lo que absorbe riesgo_por_operacion es la distancia hasta el stop, asi que el lote sube un 25 % con stop_fraccion_caja = 0,8. Esa parte de la regla NO la sostiene el literal del trader -que decia lo contrario- y por eso declara `decision`

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_coloca_orden_limite": {}
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
          "nivel": "stop_fraccion_caja"
        }
      },
      {
        "fijar": {
          "a": "si",
          "hecho": "orden_limite_pendiente"
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

### RN-013 · hay un unico esquema de stop, y vale para cualquier esquema de entrada

- **Clase**: `disparador`
- **Cuando**: se abre la operacion, por el esquema de entrada que sea
- **Entonces**: el stop va a stop_fraccion_caja, sea cual sea el esquema
- **Parametros**: `stop_fraccion_caja`, `stop_en_orden_pendiente`
- **Complementa**: RN-010, RN-011, RN-012
- **Cita**: `fb-2026-09-09-sesion-01-bc829942` — *«tanto primero como segundo esquema de entrada en 0.80, ¿verdad? Sí»*
- **Notas**: hasta el 2026-09-10 existia `stop_segundo_esquema` con el MISMO valor que stop_fraccion_caja: dos puertas para el mismo numero, que es lo que RN-012 prohibe expresamente y ADR-0002 para todo. Ahora es cierto por construccion, no por coincidencia: el parametro del segundo esquema queda UNKNOWN a proposito

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_activa_entrada": {
          "por": "cualquier_esquema"
        }
      }
    ]
  },
  "entonces": {
    "hace": [
      {
        "escribir_stop_en_la_orden": {
          "donde": "stop_en_orden_pendiente",
          "nivel": "stop_fraccion_caja"
        }
      },
      {
        "fijar": {
          "a": "si",
          "hecho": "operacion_abierta"
        }
      },
      {
        "fijar": {
          "a": false,
          "hecho": "orden_limite_pendiente"
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
- **Cita**: `fb-2026-09-09-sesion-01-0ccafcba` — *«yo siempre lo he estado trabajando, o sea, apenas toca»*
- **Notas**: el disparador NO es un nivel de precio sino la ruptura de la zona de control que se forma despues de la entrada. A-13 pregunta si esa ruptura deberia exigir cuerpo

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

### RN-015 · el objetivo es fijo, se traza con la orden y no se mueve

- **Clase**: `disparador`
- **Cuando**: se abre la operacion
- **Entonces**: el objetivo se fija en objetivo_rr sobre la distancia que declara base_calculo_objetivo, en el mismo instante en que se traza la orden, y no se extiende (objetivo_extension_activa) ni se sacan parciales (parciales)
- **Parametros**: `objetivo_rr`, `base_calculo_objetivo`, `objetivo_extension_activa`, `parciales`
- **Complementa**: RN-013
- **Cita**: `fb-2026-09-09-sesion-01-7fbbb2e7` — *«Siempre se fija el 1:3, no importa en que escenario nos encontremos»*
- **Notas**: la BASE del 1:3 no la dice el literal, y por eso vive en base_calculo_objetivo y no en esta frase (ADR-0014). El objetivo se traza sobre la caja completa y el lote YA NO: desde ADR-0020 el lote se dimensiona hasta stop_fraccion_caja, asi que las dos distancias dejaron de ser la misma. El RR REALIZADO sigue siendo objetivo_rr / stop_fraccion_caja, no objetivo_rr, porque esa razon no depende del lote. Quien mida fidelidad en F26 no debe leer esa diferencia como un fallo del bot: es la mecanica. ev-v4-011951 empuja al otro lado -el trader dice que un ganador cubre "2 o 3" perdidas, que cuadra mejor con medir sobre el riesgo real-, pero es una estimacion redonda hablando de margenes, no una descripcion del calculo; A-18 lo deja a la vista hasta ratificarlo

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_activa_entrada": {
          "por": "cualquier_esquema"
        }
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
- **Notas**: el contador NO es diario; se reinicia con la siguiente liquidez de M15

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "cualquiera_de": [
      {
        "todos_de": [
          {
            "se_cierra_operacion": {
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
- **Cuando**: un equal cierra la operacion y el precio vuelve a dar el esquema
- **Entonces**: se reentra segun reentrada_tras_equal, y no suma al contador
- **Parametros**: `reentrada_tras_equal`, `cartucho_criterio`
- **Cita**: `fb-2026-09-09-sesion-01-060cd801` — *«Sí, esto no gasta intentos, me dijiste, ¿no? No»*

**Forma ejecutable**, tal cual la lee el motor:

```json
{
  "cuando": {
    "todos_de": [
      {
        "se_cierra_operacion": {
          "resultado": "equal"
        }
      },
      {
        "vuelve_a_dar_el_esquema": {}
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

### RN-020 · el tope porcentual es el unico freno del dia

- **Clase**: `gate`
- **Cuando**: la perdida acumulada desde el corte que marca reloj_dia_riesgo -que cae en el reloj del servidor, cuyo calendario declara broker_dst y cuyo desfase base declara broker_offset_base- alcanza perdida_maxima_diaria sobre base_calculo_perdida_diaria, o perdida_maxima_semanal sobre base_calculo_perdida_semanal
- **Entonces**: se deja de operar hasta el corte siguiente
- **Parametros**: `perdida_maxima_diaria`, `base_calculo_perdida_diaria`, `perdida_maxima_semanal`, `base_calculo_perdida_semanal`, `reloj_dia_riesgo`, `broker_dst`, `broker_offset_base`
- **Cita**: `fb-2026-09-09-sesion-01-bff260ea` — *«De la cuenta basado en el saldo, y que sea en el saldo inicial del día»*
- **Decision**: `ADR-0015` — dice mas que su cita, y lo declara
- **Notas**: OJO a la aritmetica, corregida en la auditoria del 2026-09-09: agotar los cartuchos cuesta tres perdidas, pero el contador NO es diario -se reinicia con la siguiente liquidez de M15 (cartuchos_reinicio)-, asi que no hay cota diaria por esa via: son tres perdidas POR ZONA, y nada limita cuantas zonas se desarrollan entre la apertura y el cierre de la ventana. El tope porcentual no es una red que nunca se toca: es el unico freno del dia que existe, y el titulo de esta regla decia lo contrario hasta la auditoria del 2026-09-10. Las dos bases NO son la misma -el dia sobre el saldo inicial del dia, la semana sobre el saldo actual, que es lo que dijo el trader en cada caso- y el corte lo marca reloj_dia_riesgo, que sigue siendo un default nuestro (A-19)

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
- **Notas**: HASTA EL 2026-09-12 esta regla decia tambien que se opera DURANTE LAS NOTICIAS, y para el trader sigue siendo cierto: opera cuentas propias que no lo prohiben y su estrategia funciona dentro de esos eventos. Para el BOT ya no, porque va a una cuenta fondeada que puede prohibirlo: esa mitad se fue a RN-028 (ADR-0022). El propio trader lo habia avisado y el aviso llevaba tres dias en estas notas sin que ninguna guardia lo mirara

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

### RN-028 · el bot no abre alrededor de una noticia de alto impacto, aunque el trader si lo haga

- **Clase**: `gate`
- **Cuando**: hay una noticia de alto impacto y filtro_noticias dice que se filtra
- **Entonces**: no se abre ninguna operacion. NO es lo que hace el trader -el opera cuentas propias que no lo prohiben y su estrategia funciona dentro de esos eventos-: es una restriccion de la cuenta a la que va el bot
- **Parametros**: `filtro_noticias`
- **Cita**: `fb-2026-09-09-sesion-01-3565552d` — *«a mí me es indiferente si hay noticia o no [...] Sí, incluimos noticias»*
- **Decision**: `ADR-0022` — dice mas que su cita, y lo declara
- **Notas**: La cita dice lo CONTRARIO de lo que esta regla hace, y por eso declara `decision`. Lo que el trader dijo sigue siendo verdad sobre SU operativa y se conserva intacto en RN-021 y en la descripcion de filtro_noticias. Lo que decide ADR-0022 es donde corre el bot: una cuenta fondeada que puede prohibirlo como norma, con la cuenta como sancion aunque la operacion acabe en profit. El propio trader lo aviso en la sesion 1. La CAPACIDAD se conserva: basta poner filtro_noticias en `no` el dia que el bot opere donde se permita. F26 tiene que citar esta regla: si el trader opero una noticia y el bot se abstuvo, NO es un fallo del bot

**No es ejecutable todavia** (A-17): la prohibicion esta en pie, pero falta definir su condicion.

## Descartadas

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

## Vocabulario

### predicados (22)

- **`abre_sesion_operativa`** — empieza una de las sesiones de la ventana Cita `fb-2026-09-09-sesion-01-8741c388`: *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*.
- **`alcanza_hora`** — la hora de pared llega al instante declarado Argumentos: `hora`, `huso`. Cita `fb-2026-09-09-sesion-01-ffb528d7`: *«la operativa se cierra a las 3pm en punto»*.
- **`alcanza_nivel`** — el precio llega al nivel marcado Argumentos: `que`. Cita `ev-v3-001600-ed45b091`: *«yo no busco entrada aquí todo lo que se desarrolle dentro o sea por debajo de m15 [...] de esta liquidez de m15 es ruido»*.
- **`alcanza_tope`** — un acumulador llega al tope declarado Argumentos: `acumulador`, `tope`. Cita `fb-2026-09-09-sesion-01-bff260ea`: *«De la cuenta basado en el saldo, y que sea en el saldo inicial del día»*.
- **`contexto_filtrable`** — hay noticia de alto impacto o el spread se ensancha Argumentos: `noticias`, `spread`. Cita `fb-2026-09-09-sesion-01-3565552d`: *«a mí me es indiferente si hay noticia o no [...] Sí, incluimos noticias»*.
- **`cruza`** — el precio pasa al otro lado del nivel con el criterio declarado Argumentos: `que`, `criterio`. Cita `fb-2026-09-09-sesion-01-6e15504f`: *«¿Vale con que la vela cierre con el cuerpo por encima del máximo, por debajo del mínimo, o vale con que la mecha lo perfore? Con cuerpo»*.
- **`distancia_menor_que`** — el nivel que pide la spec queda mas cerca del precio que el minimo del broker Argumentos: `que`, `tope`. Cita `fb-2026-09-09-sesion-01-c698bc6a`: *«Que sea fiel a la operativa y no busque nada adicional.»*.
- **`en_ventana`** — la hora de pared cae en el intervalo medio abierto [inicio, fin) Argumentos: `inicio`, `fin`, `huso`, `dias`. Cita `fb-2026-09-09-sesion-01-8741c388`: *«Tu operativa inicia 7AM, me dijiste, ¿no? Sí [...] Por ahora vamos a trabajarlo en esas dos sesiones»*.
- **`esta_al_otro_lado_de`** — el precio se desarrolla del lado contrario al sesgo Argumentos: `que`, `sentido`. Cita `ev-v3-001600-ed45b091`: *«yo no busco entrada aquí todo lo que se desarrolle dentro o sea por debajo de m15 [...] de esta liquidez de m15 es ruido»*.
- **`ninguna_regla_de_entrada_aplica`** — la situacion no encaja en ningun esquema Cita `fb-2026-09-09-sesion-01-c698bc6a`: *«Que sea fiel a la operativa y no busque nada adicional.»*.
- **`no_es_multiplo_de`** — el lote calculado no cae en el escalon del broker Argumentos: `que`, `paso`. Cita `fb-2026-09-09-sesion-01-17ed6193`: *«el 0.5% de riesgo de la cuenta se calcula sobre el nivel 0.8 de la cuenta, ese es el acuerdo final»*.
- **`operaciones_abiertas_alcanzan`** — el numero de posiciones vivas llega al tope declarado Argumentos: `tope`. Cita `ev-v4-003710-c753f3d3`: *«ya la respuesta es no o sea, por el hecho de que para que tú puedas entrar nuevamente o bien te ha tocado stop loss»*.
- **`rompe`** — el sujeto supera el extremo de la referencia, con el criterio declarado Argumentos: `que`, `contra`, `criterio`. Cita `fb-2026-09-09-sesion-01-8eccf5c0`: *«si no genera un rompimiento por encima, o sea, al menos por un pip o una milésima de pip, entonces seguiríamos operando bajista»*.
- **`salta_stop`** — el precio alcanza el stop y cierra la posicion en perdida Cita `fb-2026-09-09-sesion-01-c4922acb`: *«La operativa se calcula con el SL normal, pero apenas de abre la operacion se mueve el SL hasta el nivel 0.8 para todos los modelos de entrada.»*.
- **`se_activa_entrada`** — la orden limite se llena Argumentos: `por`. Cita `fb-2026-09-09-sesion-01-9626d3dd`: *«se activa la entrada y apenas automáticamente [...] proteger a 0.80 [...] o continúa ya nos saca con menos 0.80»*.
- **`se_cierra_operacion`** — la posicion deja de estar viva Argumentos: `resultado`. Cita `fb-2026-09-09-sesion-01-aa2abe65`: *«un intento no es considerado un break even, ¿vale? una entrada invalidada pues tampoco es considerado un intento [...] reentrada después de equal, tampoco es considerado un intento»*.
- **`se_coloca_orden_limite`** — se envia la orden pendiente, con su lote, su stop y su objetivo Cita `fb-2026-09-09-sesion-01-76fd91ba`: *«el SL se pone junto a la orden limite, no cuando se apertura recien»*.
- **`se_completa_zona_de_control`** — el precio rompe el punto extremo anterior y deja la zona cerrada Argumentos: `criterio`. Cita `fb-2026-09-09-sesion-01-a456bc3f`: *«como sé que una zona de control se ha completado, cuando apenas me generó un rompimiento [...] rompe el punto alto anterior con mecha, con mecha no importa»*.
- **`se_da_esquema`** — el precio forma uno de los dos esquemas de entrada en M1, con la liquidez de M15 ya tomada. `primer_esquema`: rompe directamente, sin retroceso, y el breaker basta. `segundo_esquema`: pequeno retroceso que deja una zona de control, y despues rompe. Los dos marcan el bloque de origen con el breaker (BOS); el CHoCH no se usa. En M1 la ruptura vale con mecha o con cuerpo; la de M15 tiene que ser con cuerpo (RN-004) Argumentos: `cual`. Depende de: liquidez_tomada. Cita `ev-v4-000243-5f8875ce`: *«ya recordamos los dos esquemas que era uno, o bien me hace esto de aquí, rompe o bien directamente rompe el precio como tal o sea sólo con velas rojas y si hace el otro esquema pues con un pequeño retroceso pequeña zona de control y luego rompe»*.
- **`se_mapea_estructura`** — varias velas de M1 se agrupan como una estructura Argumentos: `criterio`. Cita `fb-2026-09-09-sesion-01-7ee9cabc`: *«sería considerado una estructura [...] en el lenguaje del bot sería considerado una estructura»*.
- **`vuelve_a_dar_el_esquema`** — tras un equal, el precio forma otra vez el esquema de entrada Cita `fb-2026-09-09-sesion-01-060cd801`: *«Sí, esto no gasta intentos, me dijiste, ¿no? No»*.
- **`zonas_desarrolladas_superan`** — el esquema desarrolla mas zonas de control de las admitidas Argumentos: `tope`. Cita `fb-2026-09-09-sesion-01-1b2203b0`: *«solo 1 zona control bro. si hay 2 se descarta»*.

### acciones (13)

- **`abstenerse`** — no operar, sin aproximar ni buscar nada adicional Argumentos: `segun`.
- **`agrupar_estructura`** — mapea como una sola estructura las velas de M1 que forman un order block mayor Argumentos: `criterio`.
- **`cerrar_a_mercado`** — cierra la posicion al precio de mercado Argumentos: `de`, `si`.
- **`dimensionar_lote`** — calcula el lote a partir del riesgo y la distancia declarada Argumentos: `base`, `riesgo`, `sobre`.
- **`escribir_stop_en_la_orden`** — escribe el stop en la orden pendiente, antes de que se active Argumentos: `donde`, `nivel`.
- **`fijar`** — establece un hecho de estado Argumentos: `hecho`, `a`.
- **`fijar_objetivo`** — escribe el objetivo en la orden Argumentos: `multiplo`, `sobre`, `extension`, `parciales`.
- **`gestionar_salida`** — protege y deja correr una entrada que no rompio Argumentos: `segun`, `stop`.
- **`mover_stop`** — cambia el nivel del stop de una posicion viva Argumentos: `de`, `a`, `cuando`.
- **`realizar_perdida`** — contabiliza la perdida efectiva cuando el stop salta Argumentos: `riesgo`, `sobre`.
- **`redondear_lote`** — ajusta el lote al escalon del broker Argumentos: `a_la_baja`, `paso`, `minimo`, `contrato`.
- **`reentrar`** — vuelve a colocar la orden tras un equal Argumentos: `segun`, `cuenta_como`.
- **`reubicar_orden_limite`** — mueve la orden pendiente a otra zona Argumentos: `a`, `cadencia`.

### efectos (2)

- **`abrir_operacion`** — colocar una orden o abrir una posicion nueva
- **`buscar_entradas`** — mirar M1 en busca de un esquema de entrada

### hechos (6)

- **`detenido_por_cartuchos`** — los cartuchos estan agotados y no se opera hasta cartuchos_reinicio. Va aparte del tope porque su reinicio es OTRO: la siguiente liquidez de M15, no el corte del dia Lo produce: RN-016. Lo consume: RN-001, RN-016.
- **`detenido_por_tope`** — el tope porcentual -diario o semanal- esta alcanzado y no se abre hasta el corte siguiente. Es un HECHO que dura, no un instante: sin el, la prohibicion de RN-020 solo valia en el tick del evento y nada impedia abrir en el siguiente Lo produce: RN-020. Lo consume: RN-001, RN-020.
- **`liquidez_tomada`** — la liquidez de M15 marcada ya se ha tomado con cuerpo (RN-004). Es la PRECONDICION de los dos esquemas de entrada: sin ella no se mira M1. Hasta el 2026-09-11 esta condicion vivia solo en la prosa de `se_da_esquema`, y RN-004 fijaba un hecho que ninguna forma leia: un motor que implementara `forma` habria entrado sin esperar la toma. Lo consume el predicado `se_da_esquema` (`depende_de`), no una regla Lo produce: RN-004. Lo consume: predicado se_da_esquema.
- **`operacion_abierta`** — hay una posicion viva Lo produce: RN-013. Lo consume: RN-002, RN-014.
- **`orden_limite_pendiente`** — hay una orden colocada y todavia sin llenar Lo produce: RN-011, RN-013. Lo consume: RN-006.
- **`sesgo`** — el sentido en el que se busca entrada Lo produce: RN-003. Lo consume: RN-005.

### acumuladores (3)

- **`cartuchos`** — perdidas que cuentan como intento Cita `fb-2026-09-09-sesion-01-e3eedcaa`: *«»*.
- **`perdida_dia`** — perdida acumulada desde el corte del dia de riesgo Cita `fb-2026-09-09-sesion-01-462134c7`: *«»*.
- **`perdida_semana`** — perdida acumulada desde el corte de la semana Cita `fb-2026-09-09-sesion-01-a85b6bc7`: *«»*.
