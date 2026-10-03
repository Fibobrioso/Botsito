# Renovar el calendario de cierres

El calendario de cierres de un perfil (`knowledge/cuentas/cierres/<perfil>.yaml`, ADR-0068) solo
vale entre `cubre.desde` y `cubre.hasta`. Fuera, el broker niega abrir y colocar
(`cierre_sin_calendario`), y el simulador se niega a correr un día que no cubre (exit 2,
nombrando los días). Decisiones del consultor del 2026-10-03 (`docs/validation/RENOVAR-CIERRES.md`,
«Decisiones»).

## Cuándo se renueva: por una condición, no cada semana

No se renueva a fecha fija. Hoy nadie consume el calendario en tiempo real, y renovar a ciegas
cuesta y no cambia nada. Se renueva en dos casos:

1. **Una simulación pide días posteriores a `hasta`.** Lo avisa el propio simulador:
   `ERROR: dias fuera del calendario de cierres de <perfil> (ADR-0068): [...]` y exit 2. Lo vigila
   `tests/unit/test_renovar_cierres.py`, que comprueba que se niega por la fecha simulada y nunca por
   la de hoy. En ese momento se renueva **hacia atrás**, hasta cubrir esos días, con las Trading
   Updates ya publicadas de esas semanas.
2. **Antes de que el bot corra en tiempo real** (demo o real). La rama que lo conecte trae una de
   estas dos cosas:
   - la lectura de las sesiones del símbolo con `SymbolInfoSessionTrade` (ADR-0068 §4, entrada N de
     Next Action);
   - o un procedimiento de renovación que cierre el hueco del jueves por la mañana. FTMO publica la
     Trading Update casi siempre el jueves entre las 07:25 y las 13:14 UTC (26 de 43, medido en
     RENOVAR-CIERRES.md §0.2), y `cubre` acaba el miércoles.

   **Sin una de las dos, esa rama no se cierra.**

No hay aviso por fecha en `state check` ni en `make check`: leer la fecha de hoy ahí sería una
entrada global que cambia sola (patrón 1 de `ERRORES-RECURRENTES.md`).

## Quién, y en qué rama

Claude Code, con orden de Aleks, en una rama PROPIA (`trabajo/renovar-cierres-<AAAA-MM-DD>`), con el
ritual entero. Tocar el YAML en `main` exige un tag `stable/*` nuevo (regla 5 de `state check`,
medido en RENOVAR-CIERRES.md §0.3), y la rama la exige el hook `pre-commit`. La renovación no se
mete en otra rama: mezclaría un dato ajeno con su contrato.

## De dónde sale el dato

- **Las Trading Updates de FTMO**, archivadas en `https://ftmo.com/en/blog/trading-updates/`. Hay
  una cada semana, casi siempre el jueves, con nombre `trading-update-<día>-<mes>-<año>` (alguna con
  otro nombre: medido en `docs/validation/CIERRES-DE-MERCADO.md` §0.2).
- **Cada cierre extraordinario del Forex** entra en `extraordinarios`, con su `fuente`: la URL de la
  Trading Update y la fecha de consulta.
- **`cubre.hasta`** llega solo hasta el día antes del jueves siguiente a la última actualización
  leída, nunca más allá. En el comentario de `cubre`, las fechas de lectura.
- **Lo que no tenga fuente no entra**: un festivo que «suele» no cerrar el Forex (el Columbus Day,
  por ejemplo) se queda fuera.
- **FTMO limita el ritmo** (HTTP 429): las descargas, con pausa entre una y otra.

## Cómo se comprueba

`uv run botsito knowledge validate`, los tests de `tests/unit/test_cierres_de_mercado.py` y de
`tests/unit/test_renovar_cierres.py`, y el arnés que pedía esos días, que ya no se niega.
