# F11 · strategy-spec-schema — INFORME DE VALIDACIÓN

**Estado:** WAITING_FOR_USER_VALIDATION · **Rama:** `feature/F11-strategy-spec-schema` ·
**Fecha:** 2026-09-09 · **Cierre previsto:** tag `stable/F11`

`make check` verde: 573 casos (402 funciones), 4 contratos de capas, mypy strict sobre src y tests,
`state/config/knowledge validate` en verde.

---

## 1. Qué hace F11

Convierte lo que el trader dijo el 9 de septiembre en una especificación que el bot puede leer:

| Pieza | Qué es |
|---|---|
| `botsito feedback apply` | la puerta que F09 dejó diferida: lleva los valores del feedback al registro, cada uno con su fuente |
| `knowledge/spec/parametros.yaml` | 42 parámetros: **36 con valor, 6 UNKNOWN a propósito** |
| `knowledge/spec/strategy_spec.yaml` | 25 reglas: 22 vigentes y 3 descartadas, todas con su cita |
| `knowledge/spec/glossary.yaml` | 9 términos del trader, definidos una vez |
| `knowledge/spec/spec_manifest.yaml` | `spec_version` 1.0.1 y hash sobre los tres ficheros |
| `botsito spec status` | con qué corre el bot y qué sigue en revisión |
| `botsito spec manifest` | comprueba el hash; `--escribir` lo regenera |

## 2. La decisión que más importa: `apply` no interpreta

Catorce valores de la sesión no encajaban en el registro: `"0,8"` con coma, `"3"` como texto donde
se espera un entero, `"sin limite"` donde se espera un decimal, la frase entera del anclaje.

La salida fácil era que `apply` los tradujera. Eso habría metido en el código **una tabla de
interpretación de las palabras del trader**, sin cita, sin revisión y —lo peor— invisible para
`test_no_business_literals`.

En su lugar, `FeedbackRecord` tiene un campo opcional `valor_canonico` que escribe el consultor en
un registro que supersede al de la sesión, **con el literal del trader intacto**. `apply` lo usa tal
cual y **falla** ante cualquier otra cosa.

En su primer uso real falló nueve veces seguidas, y **cada fallo era un problema de verdad**:

1. tres horas sin huso declarado — sin huso, una hora no dice cuándo ocurre;
2. `instrumento` y `cuenta_objetivo`, cuya categoría prohíbe escribirlos por feedback;
3. dos `"no aplica"` y un `"sin limite"`, que no son números;
4. dos registros vigentes a la vez sobre `stop_proteccion_capital`;
5. y, al convertir a `enum`, seis valores que traían la elección con una coletilla explicativa
   detrás (`"al_romper (cada zona de control completada)"`).

## 3. Lo que la sesión obligó a cambiar en el registro

- **`huso_grafico` = `Etc/GMT-2`**, del que cuelgan las tres horas. Y `huso_operativa` deja de decir
  `Europe/Madrid`: la sesión lo desmintió. **Ojo al signo**: `Etc/GMT-2` es UTC**+**2, y hay un test
  que lo fija afirmando +02:00 en enero y en julio.
- **`cartucho_criterio`** y **`cartuchos_reinicio`**: el trader dijo con claridad que un break even
  no gasta cartucho y que el contador se reinicia con la siguiente liquidez de M15, pero no había
  dónde guardarlo. Sin ellos, el bot leería "3" como tres entradas y con reinicio diario: **operaría
  de menos y volvería tarde**.
- **`base_calculo_riesgo`** (saldo actual) y **`base_calculo_perdida_diaria`** (saldo inicial del
  día): la diferencia se perdía porque ambos declaraban "porcentaje de la cuenta", y es justo como
  mide una cuenta de fondeo.
- **`filtro_spread`** y **`objetivo_extension_activa`**: "no hay tope" es un interruptor apagado, no
  un umbral en cero. Un cero en el tope de spread significaría no operar nunca.
- **`cuenta_objetivo`** (fondeada), **`cuenta_pruebas`** (demo) y **`saldo_inicial_cuenta`**, por
  ADR: la cuenta la decide el consultor.

**Seis parámetros se quedan UNKNOWN a propósito**, cada uno con un registro `REJECT` que explica por
qué: el colchón de spread, los dos de reducción por porcentaje de vela, el tope de spread, la
extensión del objetivo y `stop_proteccion_capital`, que es derivado. `UNKNOWN` significa "leerlo
falla", que es exactamente lo que debe pasar con un número que no existe.

## 4. Las reglas no pueden llevar números

Los campos ejecutables de `strategy_spec.yaml` rechazan cualquier cifra que empiece palabra; `M15`,
`H4` y `liquidez_m15_criterio_toma` pasan, porque son nombres. Así, cambiar el stop de 0,8 a 0,75 se
hace **en un sitio** y la spec no se toca. El campo `literal` sí admite cifras: son las palabras del
trader, y censurarlas sería falsear la cita.

Tres reglas nacen **DESCARTADAS** con su motivo y su cita: no hay colchón de spread separado, no se
baja la protección por porcentaje de vela, y el tercer esquema queda fuera. Una regla descartada con
su porqué vale más que una regla ausente, porque la ausencia no se puede revisar.

Y `knowledge validate` avisa de algo que no es formato: **una regla vigente que nombra un parámetro
UNKNOWN no se puede ejecutar**.

## 5. El hash cubre lo que el bot hace

Sobre los **tres** ficheros, `parametros.yaml` incluido. Si el registro quedara fuera, mover el stop
no cambiaría el hash y el pre-vuelo de la demo (F33) daría verde con una estrategia distinta de la
validada — el fallo exacto que MASTER_PLAN H.2 pide impedir, y hay un test que lo comprueba.

Entran también el **estado** y la **fuente** de cada parámetro: pasar de `DEFAULT_AMBIGUOUS` a
`CONFIRMED` no cambia el valor pero sí lo que la spec afirma, y quien mida fidelidad tiene que poder
distinguirlo.

Se hashea la **estructura re-serializada**, no los bytes: un comentario no cambia la spec. La
guardia ya saltó una vez de verdad, al alinear `huso_operativa`, y obligó a subir la versión a 1.0.1.

## 6. Qué está corriendo y qué sigue en revisión

```
spec 1.0.1 · 22 reglas vigentes, 3 descartadas · 36 parámetros con valor, 6 sin él

Corriendo con un valor que sigue en revisión:
  anclaje_h4              23:00 Etc/GMT-2    A-14
  break_even_condicion    tocar              A-13
  filtro_noticias         no                 A-17
  ventana_fin             15:00 Etc/GMT-2    A-15
  ventana_inicio          07:00 Etc/GMT-2    A-15
```

Los cinco entran **CONFIRMED**: lo dijo el trader, con minuto y cita. Que estén en revisión se ve
cruzando con las ambigüedades abiertas, no degradando su estado.

## 7. Lo que el usuario debe decidir

1. **Validar F11** para el ritual de cierre (merge + `stable/F11`).
2. **A-15 (Nueva York)**, **A-16 (proveedor de datos)** y **A-17 (noticias)** tienen tu decisión
   tomada y anotada, pero siguen `ABIERTA` en `ambiguedades.yaml`, que solo admite cerrarlas con
   feedback del trader. Hay que decidir si esa asimetría se resuelve permitiendo cerrar una
   ambigüedad por ADR, o si se dejan abiertas hasta poder medirlas.
3. **A-13 y A-14 se miden, no se preguntan**: la primera comparando toque y cuerpo sobre los mismos
   días; la segunda, mirando su gráfico en una fecha de invierno (enero ya está congelado).

## 8. Deuda que F11 deja anotada

- `knowledge/cases/kit/mapa_parametros.yaml` conserva `temas` y `ambiguedad`; sus `opciones` ya
  bajaron al registro. Queda decidir dónde vive el resto (F13).
- La tabla R-01..R-14 → `fb-…` no se ha escrito: las reglas citan directamente el registro de
  feedback, así que ninguna cita "R-03", pero el informe de la sesión sí lo hace.
- `feedback pending` sigue listando todo lo aplicado; con el registro ya poblado, conviene que
  filtre por lo que falta.
