# El breaker de M1: lo que la pantalla acota y lo que la spec horneaba

Rama `trabajo/breaker-m1`. Sin tocar main, sin merge, sin tag, sin push. Sin abrir holdout, ni xlsx, ni
capturas de Analytics: solo fotogramas de v4, la cruda y el repositorio.

## 1. De dónde viene

Había una contradicción viva entre dos items de confianza alta del mismo vídeo, a seis minutos uno de
otro, con un CONFIRM escrito del trader encima de uno de ellos:

- `ev-v4-005910-d24c0345` (v4 0:59:10, tema `entrada.breaker_m1_mecha_m15_cuerpo`, valor `cuerpo`):
  «en M1 pues es válido con mecha o con cuerpo; pero en M15 cuando nos va a romper es con cuerpo».
- `ev-v4-005319-dee95093` (v4 0:53:19, tema `no_trade.rompe_con_mecha_no_valida`): «el precio me rompe
  aquí con mecha, no hay validez de tomar este trade», **sin decir la temporalidad**.
- `fb-2026-09-09-sesion-01-9deda56d`: CONFIRM del trader sobre el segundo, «SI (una rotura con mecha no
  valida el trade)».

**Se resolvió mirando la pantalla.** Los fotogramas del tramo (extracción `fr-v4-9ad0ebb8`, 1 fps) dicen:

| Momento | Lo que hay en pantalla |
|---|---|
| 0:53:12-0:53:17 | Gráfico en **M15** (`15m` resaltado, etiqueta `…/USD · 15`, paso de replay `15m`), con zonas azules dibujadas y dos etiquetadas a mano: **`m1 lq`** y **`15 lq`** |
| 0:53:18 en adelante | Cambia a **M1** (`1m` resaltado, `…/USD · 1 ·`) y ahí se queda. EURUSD en FX Replay, viernes 02 ene 2026, eje de 14:20 a 18:15, reloj UTC+2 |
| 0:53:19-0:53:31 | Una **línea horizontal azul a ~1,1729**, que viene de un máximo anterior y se prolonga a la derecha, y un zigzag que sube y **termina en una flecha apuntando a esa línea**. Hacia las 15:44-15:46 la línea está seleccionada, con su círculo de extremo bajo el cursor |
| 0:53:23 y 0:53:29 | La vela de ese extremo tiene una **mecha superior que perfora la línea y el cuerpo cierra por debajo**. Las siguientes son rojas. El precio solo supera la línea con cuerpos bastante más tarde, cerca de las 16:50 |

Y la cruda, en el mismo tramo: 3190,3 s «*mira aquí en m1 vemos*»; 3199,1 s «*el precio me rompe aquí
con mecha no hay validez de poder yo seguir operando, no de seguir operando sino de tomar este 3d*».

**Los dos items son ciertos.** Lo que se rompe con mecha en 0:53:19 es **un nivel dibujado al que apunta
la flecha** -una toma de liquidez, cuya regla del cuerpo ya existe: RN-004-, y el de 0:59:10 habla de la
**ruptura del esquema de entrada**, que es otra cosa. Lo que estaba mal era cómo estaba escrito
`ev-v4-005319`: su `afirmacion` era incondicional y decía más que su cita y que su pantalla.

## 2. Las guardias sobre el CONFIRM, medidas ANTES de aceptar nada

`fb-2026-09-09-sesion-01-9deda56d` es un CONFIRM del trader sobre el item que se iba a superseder. Medido
con el repositorio real y el item nuevo simulado, sin escribir nada:

| Guardia | Con TODOS los items (lo que se hace hoy) | Si alguien pasara solo los VIVOS |
|---|---|---|
| `feedback.validar_contra_contexto` (la que usa `knowledge validate`) | **sin problemas** | `fb-…-9deda56d: evidencia objetivo ev-v4-005319-dee95093 no existe` |
| `cases.validar_paquetes` (cuestionario de la sesión 1; R-12 cita el item viejo) | `([], [])` | tres «cita evidencia inexistente», ninguna por nuestro item |
| `cases.validar_ambiguedades` | sin problemas | — |

**Ninguna guardia se queja**, y la razón es el precedente que el brief recuerda: el commit `653efdc`
(«superseder un item no borra la pregunta que ese item abrió») ya alineó a los dos llamantes para que la
EXISTENCIA se compruebe contra todos los items, no contra los vivos. Existir y seguir vigente no son lo
mismo; un CONFIRM confirma lo que el trader dijo aquel día, y eso no deja de haberse dicho.

Dos cosas que sí conviene tener anotadas, y que no son quejas de ninguna guardia:

1. **`feedback pending` devuelve REFLEJADO sin mirar si el item vive.** El motivo que imprime es «un
   CONFIRM confirma un item que ya vive: no deja trabajo» (`cli.py:1628`), y la frase deja de ser cierta
   en cuanto el item se supersede, aunque el veredicto siga siendo el correcto.
2. **`kb find` deja de mostrar el item viejo:** el índice de recuperación filtra por activos
   (`retrieval/indice.py:203`). Lo que se busque de ese minuto encontrará el item nuevo.

## 3. El item nuevo

`ev-v4-005310-ce69f8c6`, `supersede: ev-v4-005319-dee95093`, mismo tema -lo exige la guardia: «una
corrección habla del mismo tema»-, `modalidad: ambas`, cita de audio de la cruda y **cita de pantalla
anclada a los fotogramas** `fr-v4-9ad0ebb8/3203000` y `/3209000`.

> **afirmación:** en M1, lo que rompe con mecha es el nivel horizontal dibujado al que apunta la flecha:
> la vela lo perfora con la mecha y cierra el cuerpo por debajo, y por eso no toma la entrada.

`confianza: media`, como los demás items que se apoyan en un fotograma (`ev-v2-003320`, `ev-v4-000813`):
la cita de audio es limpia, pero la identificación del objeto que se rompe sale de la pantalla.

**Una desviación del brief, y por qué.** El brief pedía `evidence propose --check` y luego `accept`. Ese
camino **no puede crear este item**: el esquema de una propuesta no admite `supersede`
(`CAMPOS_ITEM_OPCIONALES` es `valor, fotogramas, notas, marca_heredada`) y `evidence accept` tampoco lo
acepta. Se usó `botsito evidence new --supersede`, que es como se crearon los **ocho primeros supersede
del proyecto** (commit `2003e61`, cerrando `stop.nivel`) y que verifica la cita contra la cruda igual
que el resto. La evidencia no se ha editado a mano en ningún momento. Dejar además una propuesta sellada
con un item pendiente habría ensuciado el recuento de `knowledge validate` («25 propuestas, 0 items
pendientes») sin aportar nada.

## 4. El criterio de M1 deja de ser prosa

Vivía en `strategy_spec.yaml:149-150`, dentro de la descripción de `se_da_esquema`, y era el único de su
familia sin parámetro. Ahora:

- **Nace `breaker_m1_criterio_ruptura`** (enum `mecha|cuerpo`, valor `mecha`), junto a sus hermanos
  `sesgo_h4_criterio_ruptura`, `zona_control_criterio_completada`, `break_even_criterio_ruptura` y
  `liquidez_m15_criterio_toma`. Fuente: `ev-v4-005910-d24c0345`.
- **`se_da_esquema` lo toma como argumento** (`argumentos: [cual, criterio]`) y su descripción ya no
  lleva el criterio escrito en la frase.
- **RN-008 lo pasa en su forma** (`criterio: breaker_m1_criterio_ruptura` en los dos esquemas) y lo
  declara en `parametros`. Eso es lo que le da un lector de verdad: desde el 2026-09-16,
  `comprobar_consumo` solo cuenta como lector **una forma vigente**, no una lista.

**Estado: CONFIRMED, y no DEFAULT_AMBIGUOUS.** El trader lo dice él mismo dos veces, en dos vídeos, sin
desdecirse: `ev-v4-005910` («en M1 pues es válido con mecha o con cuerpo») y `ev-v3-000606-f2aff599`
(«¿tomas en cuenta la mecha o solo el cuerpo?» → «basta que rompa con lo mínimo un pip», tema
`mapeo.m1.mecha_rompe_break`, valor `mecha`). DEFAULT_AMBIGUOUS exige `ambiguedad_id`, es decir, una
pregunta abierta sobre ESTE criterio, y no la hay: A-13 es el break even, y A-32 (§6) pregunta por otra
cosa. Hay precedente de CONFIRMED citando evidencia y no feedback: `huso_grafico`,
`operaciones_simultaneas_max`, `base_calculo_objetivo` e `instrumento`.

Comprobado: `spec check` da 32 reglas, 27 vigentes y 27 con forma ejecutable, y `comprobar_consumo` no
protesta. Si se quita el `criterio` de la forma de RN-008, el parámetro se queda sin lector y la guardia
lo dice.

## 5. El detector de contradicciones: el hueco, escrito

`src/botsito/evidence/contradicciones.py:47` agrupa por `tema` **idéntico** y compara `valor`. Esta clase
de choque le es invisible por **dos** motivos, no uno:

1. los temas eran hermanos (`entrada.breaker_m1_mecha_m15_cuerpo` y `no_trade.rompe_con_mecha_no_valida`);
2. `ev-v4-005319` **no tenía `valor`**, así que no entraba siquiera en la comparación.

No se ha registrado nada en `_contradicciones.yaml` -sigue en `contradicciones: []`-, y con el item nuevo
no hay contradicción que registrar: las dos afirmaciones conviven.

**No es la primera vez.** El commit `2003e61` ya encontró a mano dos items que afirmaban 0,75 en temas
hermanos («agrupando la evidencia POR PARÁMETRO en vez de por tema, usando el mapa del kit») y lo dejó
dicho. Es el mismo hueco, en su segunda aparición.

**Recomendación: deuda, no esta rama.** Arreglarlo bien es decidir qué agrupa -por parámetro, usando el
mapa del kit, es lo que funcionó las dos veces a mano- y qué hacer con los items sin `valor`, que son la
mayoría. Es trabajo de F06 con su propio criterio de aceptación, y meterlo aquí mezclaría una corrección
de conocimiento con un cambio de mecanismo. Queda anotado en **Technical Debt** de `PROJECT_STATE.md`.

## 6. La pregunta para la sesión 2

**A-32 · el nivel que al romperse con mecha invalida la entrada**, ABIERTA, clase `pregunta`, resuelve en
F19 y F20, con el fotograma como caso:

> En v4 0:53:23 (`fr-v4-9ad0ebb8/3203000`) descartas la entrada porque el precio rompe con mecha el nivel
> horizontal que tienes dibujado, al que apunta tu flecha: ¿ese nivel es la liquidez de M15 -y entonces lo
> que exige cuerpo es RN-004, ya escrito- o es un nivel de M1, y entonces hay rupturas de M1 que tampoco
> valen con mecha, contra `breaker_m1_criterio_ruptura`?

Lo que la sostiene: la línea **no lleva etiqueta** en pantalla, y en esa misma pantalla, segundos antes y
en M15, hay zonas marcadas `m1 lq` y `15 lq`. El trader distingue las dos; aquí no consta cuál es.

## 7. `spec_version`: 12.0.0 → 12.1.0, menor

La regla del manifiesto: «mayor si una regla cambia de sentido o desaparece, **menor si se añade una
regla o un parámetro**, parche si solo cambia un valor o una redacción». Esta rama **añade un parámetro**
y ninguna regla cambia de sentido: RN-008 sigue prohibiendo lo mismo, y lo que era prosa pasa a ser
argumento con el MISMO criterio (`mecha`) que la prosa ya afirmaba. Por eso menor y no mayor, y no parche
porque un parámetro nuevo es más que una redacción.

## 8. Lo que NO se ha tocado

- **`_contradicciones.yaml`**: sigue vacío (§5).
- **El paquete de la sesión 1**: `R-12` de `contexto_preguntas.yaml` sigue citando `ev-v4-005319`, que
  existe. Cambiarlo reescribiría material de una sesión ya celebrada. `kit check --sesion
  2026-09-09-sesion-01` sigue dando OK, con los dos AVISO de siempre.
- **Holdout**: no se abre nada. `kit check` declara por recuento las velas que lee (ADR-0033).
- **`knowledge/feedback/`**: el CONFIRM se queda como está; es solo-añadir y sigue siendo cierto.

## 9. Qué debe decidir el usuario

1. **¿Validar la rama** y hacer el ritual (`docs/runbooks/RITUAL.md`)?
2. **El item nuevo se creó con `evidence new --supersede`** y no con `propose`/`accept`, porque ese camino
   no admite `supersede` (§3). ¿De acuerdo, o se prefiere ampliar el esquema de propuesta en otra rama?
3. **`breaker_m1_criterio_ruptura` entra CONFIRMED** citando evidencia (§4). ¿O se prefiere
   DEFAULT_AMBIGUOUS colgado de A-32, aunque A-32 no pregunte por este criterio?
4. **El hueco del detector queda como deuda** (§5). ¿Se abre rama propia después de la sesión 2, o entra
   antes?
5. **A-32** tal como está redactada (§6).

## 10. Cómo comprobarlo

```
cat knowledge/evidence/v4/ev-v4-005310-ce69f8c6.yaml   # el item nuevo, con sus dos fotogramas
uv run botsito corpus frames show --video v4 --t 0:53:23 --n 3
uv run botsito spec check                             # 32 reglas, hash al dia
uv run botsito knowledge validate                     # 365 items, 29 ambiguedades, 0 contradicciones
uv run botsito kit check --sesion 2026-09-09-sesion-01  # OK, con los dos AVISO de siempre
make check > make-check.log 2>&1; echo "exit=$?"
```

## Estado
WAITING_FOR_USER_VALIDATION
