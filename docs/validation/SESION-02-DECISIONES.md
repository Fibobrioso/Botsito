# Sesión 02: las decisiones del consultor sobre el inventario, aplicadas

Rama `trabajo/sesion-02`, 2026-09-25. Sin merge, sin tag y sin push. Aplica las decisiones del
consultor sobre `SESION-02-INVENTARIO.md` y `SESION-02-BUSQUEDA-CLASIFICACION.md`, una pieza por
commit.

## 1. K-04: a qué regla afecta A-21

**El origen.** A-21 nace en ADR-0019 (commit `d264912`, 2026-09-10) preguntando qué es un breaker,
y se reformula el mismo día. ADR-0019: «Lo que sí queda abierto, y por eso A-21 se reformula en vez
de borrarse: **qué es una zona de control "limpia, sin ruido"**. Es lo único de la geometría de
entrada que sigue siendo cualitativo.» La nota de `PROJECT_STATE.md`, entrada (10) del 2026-09-10,
dice lo mismo: «A-21 se REFORMULA a lo unico que sigue siendo cualitativo: que es una zona de
control "limpia, sin ruido"», con RN-008 como la regla que dejaba de estar pendiente.

**Los pasajes que la sostienen** son los tres de su `evidencia`, y los tres hablan del esquema de
entrada en M1:
- `ev-v1-001435-f0586d02` (v1 0:14:35): «cuando se desarrolle esta zona de control que no haga
  mucho ruido, o sea, sea una zona limpia», y a continuación el breaker activa la orden límite;
- `ev-v4-000243-5f8875ce`: los dos esquemas de entrada;
- `ev-v3-004201-bfeb3734`: el primero no espera retroceso.

**La spec.** Ninguna regla cita A-21. RN-004 (`strategy_spec.yaml`, la liquidez de M15) cita A-24,
DECIDIDA por ADR-0045, y A-35, bloqueante. La geometría de la entrada es RN-008 («sin ninguno de
los esquemas de entrada no hay entrada»), cuyo segundo esquema es el que deja una zona de control.

**De dónde salía el error.** La frase «RN-004 sigue BLOQUEADA por A-21 y A-35» entra en
`PROJECT_STATE.md` en `0901d2c` (2026-09-24, `docs(state)` del cierre de `trabajo/a35-pivote-formado`)
y en el cuerpo de `A35-FOTOGRAMAS-RESULTADO.md`, sin fuente en ninguno de los dos.

**Qué se corrige.** El lado equivocado es `PROJECT_STATE.md`: sus dos apariciones (la funcionalidad
actual y Next Action 22) dicen ahora que RN-004 está bloqueada solo por A-35 y que A-21 toca RN-008.
`A35-FOTOGRAMAS-RESULTADO.md` está cerrado en `main`, así que lleva un recuadro de corrección junto
al pasaje y su cuerpo no cambia. La spec no se toca: no dice nada falso.

**Resultado: A-21 afecta a RN-008, no a RN-004. RN-004 queda bloqueada solo por A-35.** A-21 sigue
siendo bloqueante, ahora de la regla que le corresponde. Que ninguna regla la cite es un hueco de
enlace, no un error: no se abre aquí.

## 2. K-07: `huso_grafico` frente al «UTC+2 fijo»

**Hablan de lo mismo.** `huso_grafico` es, según su propia `unidad`, el «nombre IANA del huso
configurado en el grafico del trader», es decir cómo se etiquetan las horas en su pantalla de FX
Replay. El «UTC+2 fijo» de `CLAUDE.md` y de ADR-0039 es el reloj de esos mismos gráficos. **No es
el huso del xlsx**: ese se declara libro a libro (ADR-0039, `knowledge/corpus/libros.yaml`) y se
mide por velas. Tampoco es el reloj del servidor (A-28) ni `huso_operativa`. Son cuatro relojes.

**La cadena.**
- ADR-0012 §5 (2026-09-09) lo fijó en `Etc/GMT-2`.
- ADR-0015 lo discutió: todas las lecturas eran de verano.
- ADR-0017 §4 (2026-09-10) lo pasó a `Europe/Madrid`, con la premisa de que «no hay ninguna
  configuracion deliberada de huso» y la plataforma muestra la hora local.
- `ABRIL-Y-LA-CAJA.md` R0 (2026-09-21) lo mide en un fotograma de **enero** de v4: el propio gráfico
  marca «14:29:59 UTC+2» sobre «Thu 29 Jan '26», y en enero Madrid es UTC+1.
- ADR-0039, posterior y vigente, lo da por hecho: «el eje de FX Replay supuesto UTC (es UTC+2
  fijo)».

Nadie llevó la medida al registro ni enmendó ADR-0017: esa es la contradicción. La medida contesta
justo la objeción de ADR-0015, porque es de invierno.

**Qué se aplica, solo en documentación y configuración:**
- `huso_grafico` pasa a `Etc/GMT-2`, CONFIRMED, con fuente `ev-v4-011425-ae028b78`. En v4, a la
  pregunta de si el horario es «en el horario UTC más 2», el trader contesta «De UTC más 2, de 7,
  claro». La descripción cita la medida y ADR-0039.
- ADR-0017 lleva una enmienda del punto 4; ADR-0012 y ADR-0005, una nota cada uno.
- `spec_version` sube de 12.2.1 a 12.2.2 (parche: cambia un valor) y se regeneran el manifiesto y
  `docs/spec/`.

**Por qué no altera nada que esté commiteado:**
- Ningún código lee `huso_grafico`: su único consumidor declarado es ADR-0017, documental.
- El kit, la fidelidad, la ingesta, la hoja y `scripts/huso_por_velas.py` leen `huso_operativa`.
- Ningún artefacto de `knowledge/cases/` ni `docs/runbooks/ENTRADA-MARZO.md` congela
  `spec_version` ni el hash de la spec.

**Lo que NO se cambia, y es del consultor.** La premisa que cae sostenía también ADR-0017 §1:
`huso_operativa = Europe/Madrid`, es decir que la ventana de 07:00 a 15:00 es la hora civil del
trader. Con el gráfico en UTC+2 fijo, la ventana puede seguir su reloj civil o el de su gráfico.
Las dos lecturas coinciden en verano y se separan una hora en invierno: las 07:00 de su gráfico
son las 06:00 de Madrid. El corpus tiene las dos formas:
- «de 7 a 15 por España» (`ev-v3-000136-6160fcea`);
- «De UTC más 2, de 7, claro» (v4 #1280).

A-14 (RESUELTA) dice que «mantiene el mismo rango de horarios», sin decir en qué reloj. **Esto sí
toca a marzo:** del 1 al 28 de marzo de 2026 Madrid va en UTC+1 y a partir del 29 en UTC+2, así
que con una de las dos lecturas la ventana del bot va una hora desplazada respecto a la del trader
casi todo el mes. Lo mismo vale para enero. Cambiar `huso_operativa` alteraría el reparto en
sesiones de la fidelidad, la ingesta y los días que usa la herramienta del huso de ENTRADA-MARZO.
**No se toca.**

## Estado

EN CURSO. Cada sección entra con su commit.
