---
status: ACTIVE
date: 2026-09-09
phase: F11
---

# 0012 · El registro despues de la sesion 1: tipos nuevos, ausencia de valor, categorias y el reloj del trader

## Decision

1. **Cinco tipos nuevos**: `enum` (con `opciones`, al menos dos y sin repetir), `booleano`,
   `puntos`, `minutos` y `lotes`, cada uno con su accesor tipado. Las `opciones` **bajan** desde
   `knowledge/cases/kit/mapa_parametros.yaml` al registro. `booleano` se escribe sin comillas.
2. **La ausencia de valor no es un valor**: un `booleano` dice si la regla se aplica
   (`filtro_spread`, `objetivo_extension_activa`) y el umbral **se queda UNKNOWN**. Una respuesta
   que descarta una regla se guarda como `REJECT` sobre el parametro, que sigue existiendo y sin
   valor, y la regla descartada vive en `strategy_spec.yaml` con su cita.
3. **Un valor bajo ambigüedad abierta entra CONFIRMED**. Que esta en revision se responde cruzando
   el registro con las ambigüedades `ABIERTA` (`botsito spec status`), no degradando el estado.
   `DEFAULT_AMBIGUOUS` queda reservado para valores que inventamos nosotros.
4. **Categorias corregidas**: `instrumento` pasa a `estrategia`; `cuenta_objetivo` pasa a
   `prop_firm` y se parte en `cuenta_objetivo` (fondeada), `cuenta_pruebas` (demo) y
   `saldo_inicial_cuenta`.
5. **`huso_grafico` = `Etc/GMT-2`**, del que cuelgan `anclaje_h4`, `ventana_inicio` y `ventana_fin`.
   `huso_operativa`, que ADR-0005 fijo en `Europe/Madrid`, se alinea con el por decision.
6. **Parametros que la sesion obligo a crear**: `cartucho_criterio`, `cartuchos_reinicio`,
   `base_calculo_riesgo` y `base_calculo_perdida_diaria`.
7. **`valor_canonico`** en `FeedbackRecord` (opcional), y `feedback apply` deliberadamente tonto:
   usa ese valor tal cual y falla ante lo que no convierta.

## Problema que resuelve

La sesion 1 dejo 33 registros de feedback sobre parametros. Al llevarlos al registro, **catorce
valores no encajaban** y dos parametros no se podian escribir siquiera. No era formato: el registro
no sabia decir cosas que el trader habia dicho con claridad. "No hay tope de spread" no cabia en un
decimal; "no aplica" tampoco; su reloj no tenia nombre; que un break even no gaste cartucho no tenia
donde guardarse; y la diferencia entre "saldo actual" y "saldo inicial del dia" se perdia porque
ambos parametros declaraban la misma unidad.

## Alternativas consideradas

- **A. Que `feedback apply` normalice**: traducir "0,8" a 0.8, "3 perdidas" a 3, "sin limite" a
  ausencia.
- **B. Guardar los valores como `texto` libre** y que cada consumidor los interprete.
- **C. Un cuarto estado** para "respondido pero sin valor aplicable".
- **D. Borrar del registro los parametros descartados.**
- **E. `DEFAULT_AMBIGUOUS`** para los valores bajo ambigüedad abierta.

## Por que elegimos esta opcion

Porque deja **el negocio en los datos y el codigo tonto**. Un tipo nuevo, un booleano o un registro
con `valor_canonico` son diez lineas que una persona revisa de un vistazo y que git versiona con su
cita; una funcion que interpreta al trader es una decision escondida.

Que los parametros descartados **sigan existiendo sin valor** conserva la pregunta que se hizo y su
respuesta: `UNKNOWN` ya significa "leerlo falla", que es exactamente lo que debe ocurrir con un
numero que no existe.

Y `CONFIRMED` para lo que el trader dijo es simplemente cierto: lo dijo, con minuto y cita.

## Por que descartamos las demas

- **A**: mete en el codigo una tabla de interpretacion de las palabras del trader, sin cita, sin
  revision e invisible para `test_no_business_literals`. Es lo que ADR-0002 existe para impedir.
- **B**: aplaza el problema al motor, donde cada consumidor lo resolveria a su manera y ninguno
  quedaria registrado.
- **C**: `UNKNOWN` ya lo significa. Un cuarto estado es el "default silencioso" que ADR-0002 lista
  como la primera corrupcion posible del registro.
- **D**: probado y revertido en el acto: al borrar `stop_colchon_spread`, su registro de feedback
  quedaba apuntando al vacio y el sistema se negaba, con razon.
- **E**: marcaria como "default inventado" cinco parametros que sostienen sesgo, ventana y break
  even, y `feedback pending` volveria a preguntarle al trader lo que ya contesto.

## Impacto

- El registro pasa de 33 a 42 parametros: 36 con valor y 6 UNKNOWN a proposito.
- Un valor de estrategia con `fuente: decision` es ahora un error, vigilado por test.
- El `enum` hizo fallar seis valores que pasaban como texto porque traian la eleccion con una
  coletilla detras: ese es el efecto buscado.
- **Ojo al signo**: `Etc/GMT-2` significa UTC**+**2 en nomenclatura IANA. Un test lo fija afirmando
  +02:00 en enero y en julio.
- Renombrar o recategorizar un parametro rompe referencias del kit y de las ambigüedades: se hace en
  un commit propio con `knowledge validate` detras.

## Fecha / fase

2026-09-09, F11 (tras la sesion 1 con el trader).

## Estado

ACTIVE
