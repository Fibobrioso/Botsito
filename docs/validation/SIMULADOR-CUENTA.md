# El simulador: la capa de cuenta

Rama `trabajo/simulador-cuenta`, 2026-09-25. Sin merge, sin tag y sin push. ADR-0050. Next Action
31. Sesión autónoma de unas dos horas y media, con el brief del consultor delante.

Guardas verificadas al empezar y al terminar: `docs/validation/PREREGISTRO.md` con blob
`52649183…`, el declarado; cero autorizaciones en `knowledge/cases/holdout/` (solo los README).
Nada del material de septiembre; mayo no se ejecuta; febrero no se toca; ninguna fecha de día
reservado o retirado en ningún fichero de esta rama: las secuencias sintéticas de los tests son de
2030. No se toca `knowledge/spec/` ni `ambiguedades.yaml`. Ningún `--no-verify`.

## 0. El arreglo previo: los hooks ya no dependen de la consola

Desde la consola de Windows en cp1252, `uv run --no-sync lint-imports` pintaba un emoji, Python
reventaba con `UnicodeEncodeError` y `pre-commit` lo contaba como «contrato de importación roto»;
la salida era anteponer `PYTHONUTF8=1` a cada `git commit`. **Medido antes de tocar nada**: con
`PYTHONUTF8=0` (y también sin la variable) el `print` de un emoji por tubería falla en esta
máquina; con `PYTHONUTF8=1` pasa.

Los dos hooks versionados (`scripts/git-hooks/pre-commit` y `pre-merge-commit`) exportan ahora la
variable antes de lanzar ninguna herramienta Python, en un bloque comentado que va ANTES del bloque
del sello, así que el test que exige el bloque del sello idéntico en los dos sigue verde.

`tests/unit/test_hooks_utf8.py` lo prueba sobre un repo temporal: simula la consola (UTF-8
apagado, locale C sin coerción) con un `uv` FALSO en el PATH que hace lo que hacía el real, pintar
un emoji; un CONTROL demuestra que la simulación muerde (la herramienta suelta falla); el hook
versionado pasa; y **el mismo hook sin la línea del export —el mutante— vuelve a rechazar con
«contrato de importacion roto»**, que es la prueba de que el test caza el fallo de antes. Más un
test estático: el export existe una vez en cada hook y va antes de cualquier llamada a `uv`, y
`RITUAL.md` ya no pide anteponer la variable.

`docs/runbooks/RITUAL.md`, corrección 9, y `scripts/git-hooks/README.md` lo dejan escrito. Hay que
reinstalar los hooks una vez con `make hooks` desde esta rama. **El commit del propio arreglo
entró sin `PYTHONUTF8=1` delante**, que es la comprobación en vivo.

## 1. Qué se modeló

**El perfil de cuenta** (`knowledge/cuentas/ftmo-2step-swing-100k.yaml`, ADR-0050 §3). UN fichero
con el FORMATO DEL REGISTRO, leído por `config.registro.cargar_registro`: la misma puerta
(ADR-0002), los mismos tipos y los mismos tres estados (ADR-0012). Cada cifra cita su regla de
`FTMO-REGLAS.md` en su descripción y un test comprueba que la regla existe. Lo que coincide con
`parametros.yaml` lleva el mismo valor, cruzado por test (precedente ADR-0012 §1). El reloj de
corte, `Europe/Prague` (R2, R4), da hoy los mismos instantes que `huso_operativa` en las 365
medianoches de un año, con sus dos cambios de hora: afirmado por test, como pedía ADR-0027.

Lo que hay en el perfil, por regla:

| regla | parámetros |
|---|---|
| R1 objetivo | `firma_reto_objetivo` 10 %, `firma_verificacion_objetivo` 5 %, `firma_fondeada_objetivo_aplica` false; `firma_fases`, `saldo_inicial_cuenta` |
| R2 pérdida diaria | `firma_perdida_diaria_max` 5 %, `firma_base_perdida_diaria` saldo_corte_diario, `firma_magnitud_vigilada` equity, `firma_huso_corte` |
| R3 pérdida total | `firma_perdida_total_max` 10 %, `firma_perdida_total_arrastra` false |
| R4 días mínimos | `firma_reto_dias_minimos` 4, `firma_verificacion_dias_minimos` 4, `firma_fondeada_dias_minimos_aplica` false |
| R6, R8 | `firma_noticias_restringe` false, `firma_tipo_cuenta` swing, `firma`, `firma_programa` |
| R9 | `firma_apalancamiento` 30 |
| R11 | `firma_volumen_max_lotes` 100 |
| R12 costes | `firma_comision_usd_por_lote` 5, `firma_swap_largo_puntos` −9,49, `firma_swap_corto_puntos` 0,36 |
| R13 | `firma_ordenes_simultaneas_max` 200, `firma_posiciones_dia_max` 2000, `firma_mensajes_dia_max` 2000 |
| R17 | `firma_tamano_posicion_aviso_aplica` true |

**La capa de cuenta** (`src/botsito/engine/cuenta.py`, ADR-0050 §4): funciones puras.
`reglas_de_fase(perfil, fase)` lee del perfil lo que UNA fase necesita, y ahí se niega si falta un
valor; `evaluar_fase(operaciones, reglas, contrato)` corre la fase desde el capital inicial sobre
una línea de tiempo de aperturas, marcas de precio, cargos y cierres, ordenada por instante. Lleva
saldo y equity (comisión y swaps como cargos con instante), el día de la firma en el huso del
perfil con un corte a cada medianoche local antes de cualquier evento de ese instante, la pérdida
diaria sobre el saldo del corte vigilando la equity, la pérdida total estática (o arrastrando el
saldo máximo si el perfil lo declara), el objetivo por fase con sus días mínimos (día de trading
= día local con una apertura), el estado final `EN_CURSO`, `SUPERADA` o `SUSPENDIDA` con motivo e
instante exactos, y la guardia de tamaño de posición solo como aviso. Ninguna cifra en `src` y
nada que asuma EURUSD ni FTMO: el contrato entra como argumento y el perfil como fichero.

Los convenios que no estaban escritos en ninguna parte y ahora sí (ADR-0050 §4): el límite se
infringe estrictamente POR DEBAJO (R18, «drops below»), el objetivo se cumple al LLEGAR (el ejemplo
oficial es 110.000), a igual instante el cierre va antes que la apertura, la primera suspensión o
superación es terminal y lo posterior se cuenta sin evaluarse. **El margen de ADR-0031 no está
aquí**: es un freno de la estrategia; la capa modela la firma, que suspende en el límite.

**Un segundo perfil, inventado** (`tests/fixtures/cuentas/sintetica-una-fase-50k.yaml`, marcado
SINTÉTICO en su cabecera): una fase, 50.000, corte en Nueva York, vigila el SALDO, 3 % diario sobre
el capital, 6 % total que arrastra el saldo máximo, y cifra para la guardia. La misma secuencia
que con FTMO queda EN_CURSO se SUSPENDE con él por el total arrastrado, y el día 7 a las 03:30Z es
el día 6 en Nueva York. Ni una línea de código distinta.

## 2. Qué parámetros quedaron sin valor, y por qué

> **RECUADRO DE CORRECCIÓN (2026-09-26, rama `trabajo/ticks-llenado`).** `firma_comision_por_lado`
> ya NO está sin valor: por decisión del consultor del 2026-09-25 toma el supuesto conservador de
> cobrarse en cada lado (`CONFIRMED`, `true`, fuente ADR-0050), pendiente de confirmar con FTMO.
> La fila de abajo describe el estado del 2026-09-25 y se conserva tal cual.


| parámetro | por qué no tiene valor | quién lo resuelve |
|---|---|---|
| `firma_comision_por_lado` | R12: si los 5 USD por lote son por lado o por operación completa, y qué aclara el asterisco de «USD/LOT*», es NO ENCONTRADA en la fuente oficial | medirlo en la plataforma (FTMO-REGLAS §4, «para datos»); lo consume el bróker simulado |
| `firma_tamano_posicion_ratio_aviso` | R17 no da cifra para «substantially larger», y si un lote que varía con el stop a riesgo constante cuenta como tal está pendiente para Aleks con FTMO | Next Action 27. Mientras tanto la guardia queda NO EVALUABLE y el resultado lo dice nombrando el parámetro; no impide correr, porque no decide nada sobre la cuenta (ADR-0050 §4.7; el consultor puede pedir lo contrario) |
| `firma_fondeada_objetivo` | R1: la fondeada no tiene objetivo, así que no hay cifra (ADR-0012 §2: el booleano dice que no aplica y el umbral queda UNKNOWN) | nadie: es la ausencia correcta |
| `firma_fondeada_dias_minimos` | R4: la fondeada no tiene días mínimos; ídem | nadie |

Fuera del perfil y sin modelar, con motivo: R5 (sin límite de tiempo: no hay nada que modelar);
R15 (gap trading: la línea con R6 la tiene que dar FTMO, Next Action 27); R16, R18 y R19 (prácticas
prohibidas y consecuencias: no son cifras); R20 (FTMO no tiene tope semanal); R10 (el reloj del
servidor, A-28, es del instrumento y no de la cuenta). Y una limitación del registro: `firma_fases`
es TEXTO con nombres separados por espacios porque no hay tipo lista; crear uno es cambio de
ADR-0012 y queda para el consultor.

## 3. Los tests

`tests/unit/test_perfil_cuenta.py`: el perfil de FTMO carga con sus tres fases y su reloj; cada
cifra cita una regla de FTMO-REGLAS que existe; los cuatro sin valor son exactamente esos y leer
uno se niega nombrando parámetro y perfil; lo que coincide con `parametros.yaml` lleva el mismo
valor; el reloj de corte coincide con el del trader en todo un año; el perfil sintético carga y es
otra firma; y las guardias del cargador: un parámetro que no es `prop_firm`, sin reloj de corte o
con uno que no existe o sin valor, sin fases, con una fase repetida, incompleta o mal nombrada, y
un fichero que no pasa el registro.

`tests/unit/test_cuenta.py`, los nueve del brief y algunos más: suspensión en el instante EXACTO
que cruza el límite diario (caer HASTA 95.000 no infringe, 94.999 sí, y en esa marca y no antes);
reinicio del día en los dos cambios de hora europeos (medianoches medidas y afirmadas en UTC:
el 31 de marzo de 2030 empieza a las 23:00Z del 30 y el 1 de abril a las 22:00Z del 31; el 27 de
octubre a las 22:00Z del 26 y el 28 a las 23:00Z del 27; una marca a −4.999 justo tras la
medianoche vive con el límite nuevo y habría suspendido con el viejo); pérdida diaria por equity
flotante aunque el saldo no cruce (y la misma secuencia vigilando el saldo no suspende); objetivo
alcanzado sin los días mínimos que no supera, y que supera en el cierre que completa el cuarto día
aunque no gane; el objetivo exige todas las posiciones cerradas; comisión y swaps que dejan una
fase superada en no superada (110.000 brutos, 109.950 netos); persistencia entre días (tres días
perdiendo 4.500, 4.500 y 1.500: ningún diario cruza porque cada día se reinicia sobre su corte, y
el tercero cruza el total estático de 90.000); negativa a correr con un parámetro sin valor (una
fase que declara objetivo sin cifra) y la fondeada de FTMO, que corre sin objetivo; el perfil
sintético; determinismo (dos veces igual, y con la entrada invertida igual); el primer día usa el
capital inicial; el día de trading es el de la apertura; la diaria y la total a la vez se nombran
las dos; tras el final no se evalúa nada y se cuenta; a igual instante el cierre va antes que la
apertura; operaciones mal formadas que no se adivinan; una venta gana cuando el precio baja. Y lo
que el perfil le da al motor: las reglas de fase, que todo parámetro del perfil tenga lector, y el
contrato de accesores `perfil.<accesor>("nombre")`.

`tests/unit/test_hooks_utf8.py`: los cuatro de la sección 0.

## 4. Lo que falta para cablearlo al motor (ADR-0050 §5)

Nada de esto se hace en esta rama, y ninguno se inventa:

1. **El bróker simulado**, que produce las operaciones con sus marcas y sus cargos (Next Action
   32: ticks y modelo de llenado; con OHLC de M1, marcas pesimistas).
2. **La forma incremental** de la capa de cuenta: hoy `evaluar_fase` recorre una secuencia
   completa; el motor necesita el estado ANTES de cada decisión. El estado interno ya avanza evento
   a evento; hay que exponerlo como `avanzar(estado, evento)`.
3. **El signo y el recorte de los acumuladores** `perdida_dia_firma` y `perdida_total_firma`: la
   spec dice «caída» y no dice si vale cero o negativo con la equity por encima de la base; con
   `no_cabe_la_operacion` (RN-032) la diferencia importa. Pendiente de la spec o de ADR-0031.
4. **Las dos comparaciones**: mayor o igual para los frenos de la estrategia (`se_acerca_al_limite`,
   `alcanza_tope`), estrictamente por debajo para la firma.
5. **Un solo reloj declarado** para el cableado: `reloj_dia_riesgo` de la spec o `firma_huso_corte`
   del perfil; hoy coinciden y un test lo vigila.
6. **El margen de ADR-0031** se aplica en el motor de estrategia sobre los acumuladores que esta capa
   alimente; la capa de cuenta no lo conoce.

## 5. Para el consultor

- **`firma_huso_corte` en el perfil frente a ADR-0027 §alt. 3.** ADR-0027 descartó ese parámetro
  para la SPEC por ser dos puertas del mismo instante. Aquí vive en el perfil porque el reloj es de
  la FIRMA (el sintético corta en Nueva York) y el brief lo pide así; el test de las 365
  medianoches es la vigilancia que aquel ADR pedía. Si el consultor lo ve como contradicción, la
  alternativa es que el perfil no lleve reloj y la capa de cuenta lea `huso_operativa` del registro
  de la spec, y entonces una firma con otro reloj ya no sería solo configuración.
- **La guardia de tamaño sin cifra no impide correr** (ADR-0050 §4.7 y alternativa 5). Es una
  lectura del «se niega si lo necesita»: la guardia no decide. Si se prefiere la negativa, es una
  línea en `reglas_de_fase`.
- **La duplicación vigilada** con `parametros.yaml` (ocho nombres comunes, cruzados por test) y si
  algún día RN-029 a RN-032 deben leer del perfil.
- **Un tipo `lista` del registro** para `firma_fases`.

## 6. Los commits de la rama, cada uno con su sello

Cuatro commits antes de este informe, uno por pieza, cada uno con `make check` en verde sobre su
árbol exacto (exit 0, ningún failed, línea `SELLO`) y ninguno con `--no-verify`:

| commit | pieza |
|---|---|
| `0d85ca8` | los hooks exportan `PYTHONUTF8=1`, con su test y RITUAL.md |
| `704278b` | ADR-0050 |
| `3370e48` | el perfil FTMO 2-Step Swing 100k, su cargador y el perfil sintético |
| `617acd7` | la capa de cuenta y sus tests |

El quinto es este informe. Tag propuesto para el ritual: `stable/F24-simulador-cuenta` (la capa de
cuenta es la primera pieza del simulador, F24 en MASTER_PLAN H.2). Después del merge hay que
ejecutar `make hooks` una vez desde esta rama, ANTES de `git checkout main` (RITUAL.md, «La
primera vez con la puerta»).

## Estado

WAITING_FOR_USER_VALIDATION.
