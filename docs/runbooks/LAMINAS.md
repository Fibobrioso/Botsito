# Las láminas del bot: cómo se generan y qué no se enseña

Rama que las trajo: `trabajo/laminas` (R4.5; informe `docs/validation/LAMINAS.md`).

## Lo primero: todavía no se enseñan al trader

La regla 2 de `docs/runbooks/SESION-DE-PREGUNTAS.md` corta los gráficos ANTES de la colocación y
prohíbe enseñar la orden, el stop y el objetivo. La lámina enseña las tres cosas. **Hasta que el ADR
del método (la rama de la preparación de la sesión 7, RUMBO §1) cambie esa regla, las láminas no se
enseñan al trader.** Las revisan Aleks y el consultor.

## Cómo se generan

```
uv run botsito motor laminas --sesiones 2026-07-03:07-11,2026-07-03:11-15 --salida <carpeta fuera del repo>
```

- `--sesiones` lleva pares `día:sesión`, con la sesión por el nombre de los datos (`config.sesiones`
  del kit). El orden manda el número de la carpeta (`sesion-01`, `sesion-02`...).
- `--salida` es obligatoria. Tiene que estar FUERA del repositorio y no existir o estar vacía: el
  comando no pisa nada. Si no se cumple, sale con error sin leer una vela.
- Corre la misma corrida que `motor decisiones`: toda la construcción, la cuenta por mes, el perfil
  y la fase por defecto, sin depuración. La corre DOS veces, con y sin el recolector. Si las dos no
  dan lo mismo, sale con error y no escribe nada. Tarda unos 12-15 minutos; se lanza sola, nunca
  junto a un `make check`.
- Antes de cada día de corridas, una fila en `docs/validation/HOLDOUT-EXPOSICIONES.md`: calienta
  con el M1 de marzo y de junio, como el arnés.
- Para ensayar, primero en un clon desechable (`git worktree add` en un directorio temporal, con su
  `config/settings.local.toml` y `[rutas].data` absoluto), como manda CLAUDE.md, «Ensayos aislados».

## Qué sale

- `sesion-NN/indice.html` y `sesion-NN/lamina-NN.html`: un HTML autocontenido por lámina, con un
  SVG de tres paneles (H4, M15 y M1) y la sustentación debajo, en el idioma del trader. Sin fechas,
  ids, lote, R, dinero ni porcentajes, y sin JavaScript.
- `clave.txt`, en la raíz de la salida: qué día, qué sesión, qué corte y de qué tipo es cada lámina.
  **No entra al repositorio ni al informe, y no se enseña:** lo guarda Aleks.
- Por consola, por sesión: cuántas láminas y en cuántas la H4 que fija el sesgo cae dentro de la
  ventana.

Los dos tipos de lámina: (a) una por cada orden del bot que se llenó en la sesión, cortada en el
último cierre de M1 en que la colocó o la movió a ese precio; (b) una por cada operación del trader
de la sesión que el criterio no empareja, cortada en la última M1 cerrada antes de su entrada, sin
dibujar la operación del trader.

## Qué niega

- Un día que no sea dev de construcción, uno de `casos_ocultos`, una sesión con una hora perdida
  dentro, un corte fuera de los tramos de `cobertura_material` (abril, hasta el 29) o una causa sin
  frase en la tabla cerrada: error que lo nombra, y no se escribe nada.
- Lo que nace antes de la ventana de su panel (la H4 que fija el sesgo, una línea de M15, la caja,
  el punto) no se dibuja ni da precio; la sustentación dice que viene de antes de la ventana.
