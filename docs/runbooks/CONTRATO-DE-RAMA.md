# El contrato de rama

Que puede tocar una rama de trabajo, que no, que hay que ejecutar y que informe deja. Escrito el
2026-10-01 en `trabajo/guardias-claude` (docs/validation/GUARDIAS-CLAUDE.md §2). El contrato es
`contrato.yaml`, en la RAIZ de la rama, y lo escribe Claude Code al abrirla, justo despues de
copiar el encargo en `docs/encargos/<rama>.md` (la rama con `-` en lugar de `/`).

## Que comprueba `make check`, y que no

`make check` llama a `scripts/contrato_rama.py` justo despues de `desellar`. Si hay un
`contrato.yaml`, compara contra el merge-base con `main` TODO lo que la rama cambia -lo commiteado
y lo ESTADIADO, que es el arbol que se va a sellar- y sale en ROJO, sin sello, nombrando:

- cada fichero que no case con ninguna de `rutas_permitidas`;
- cada fichero que case con alguna de `rutas_protegidas`, aunque tambien case con una permitida
  (lo protegido manda);
- el `artefacto`, si no esta estadiado;
- un contrato mal escrito (claves de mas o de menos, un `riesgo` fuera de bajo/medio/alto, un
  `artefacto` que no sea `docs/validation/<NOMBRE>.md`);
- un contrato HEREDADO: su `rama` no es la rama actual. Se compara sin el prefijo, porque el cierre
  puede llevar `trabajo/x` a `feature/x`;
- el `tramo` (desde `trabajo/hoja-de-ruta`, 2026-10-10): la entrada de `docs/plan/HOJA-DE-RUTA.md`
  a la que pertenece la rama, por el titulo de su `## ` (entero, o su id: `R1`,
  `Carril: lo de Aleks`). Falla si falta o si no es un tramo de la hoja. **Es obligatorio solo si
  la hoja de ruta existe en el merge-base con `main`**: rige desde la rama siguiente a la que la
  trajo, sin tocar ningun contrato anterior. Si el titulo lleva `: `, va entre comillas.

`contrato.yaml` se permite siempre a si mismo. **Sin contrato no se comprueba nada**, asi que una
rama vieja sin contrato sigue funcionando igual.

**`make check` NO ejecuta las `comprobaciones`.** Podrian escribir en el repositorio mientras corre
(CLAUDE.md, «nada escribe mientras corre `make check`») y lo alargarian. Las ejecuta el revisor
(`.claude/agents/revisor.md`), que pega su salida en su informe.

**En `main` no se exige**, y no debe llegar: el contrato sale de la rama ANTES del merge, como
primer paso del ritual tras la orden de cierre (RITUAL.md, «Antes del merge: el contrato sale de
la rama»). Si llegara a `main`, la rama siguiente lo heredaria y su `make check` fallaria por la
regla del contrato heredado, que es justo lo que se quiere: nadie trabaja con el contrato de otro.

## Los patrones

Rutas tal como las da git, con `/`. `*` no cruza carpetas, `**` si (`docs/**/*.md` casa con
`docs/a.md` y con `docs/a/b.md`), `?` es un caracter, y un patron que acaba en `/` es todo lo que
cuelga de esa carpeta. Mayusculas y minusculas cuentan.

## La plantilla

```yaml
rama: trabajo/<nombre>
riesgo: medio  # bajo, medio o alto, y en el comentario por que
artefacto: docs/validation/<NOMBRE>.md
tramo: R1  # el `## ` de docs/plan/HOJA-DE-RUTA.md al que pertenece la rama
rutas_permitidas:
  - docs/validation/<NOMBRE>.md
  - docs/encargos/
  - PROJECT_STATE.md
rutas_protegidas:
  - knowledge/evidence/
  - knowledge/feedback/
comprobaciones:
  - make check > make-check.log 2>&1
```

Como elegir el `riesgo`: **bajo** si la rama solo anade documentos o registros y no cambia nada que
se ejecute; **medio** si cambia codigo, tests o herramientas pero no la spec ni el motor; **alto**
si cambia la spec, el motor, el broker, la cuenta o cualquier cifra, o si abre material (un
holdout, un mes nuevo). El riesgo no cambia lo que comprueba `make check`: le dice al revisor y al
consultor cuanto mirar.

`PROJECT_STATE.md` va casi siempre en `rutas_permitidas`: abrir la rama cambia su `Current Branch`,
y anadir tests cambia el recuento de `Tests Currently Passing`.

## Tres ejemplos

### Una rama de solo knowledge (registrar el feedback de una sesion)

Toca registros nuevos y la spec que los refleja; el codigo y los registros ya escritos, no.

```yaml
rama: trabajo/reflejar-feedback-s4
riesgo: alto  # cambia la spec: cada valor con su Fuente: y su registro del trader
artefacto: docs/validation/REFLEJAR-FEEDBACK-S4.md
rutas_permitidas:
  - knowledge/feedback/2026-10-*-sesion-04/
  - knowledge/spec/
  - knowledge/evidence/
  - docs/spec/
  - docs/validation/REFLEJAR-FEEDBACK-S4.md
  - docs/encargos/
  - PROJECT_STATE.md
  - tests/unit/test_kit.py
rutas_protegidas:
  - src/
  - knowledge/feedback/2026-09-09-sesion-01/
  - knowledge/feedback/2026-09-29-sesion-03/
  - knowledge/cases/
  - knowledge/corpus/libros.yaml
comprobaciones:
  - uv run botsito feedback apply --sesion 2026-10-XX-sesion-04 --check
  - uv run botsito knowledge validate > knowledge-validate.log 2>&1
  - uv run botsito spec docs --escribir
  - make check > make-check.log 2>&1
```

`knowledge/evidence/` esta permitida porque se ANADEN items; editarlos lo para el hook de
`pre-commit`, no el contrato. Las sesiones anteriores van en `rutas_protegidas`: un registro ya
escrito no se toca nunca.

### Una rama de motor (una regla nueva en el motor)

Toca el motor, sus tests y su ADR; la spec, el broker y el material, no.

```yaml
rama: trabajo/rn-004-tras-a35
riesgo: alto  # cambia lo que el bot hace; diagnostico etiquetado antes de cualquier medida
artefacto: docs/validation/RN-004.md
rutas_permitidas:
  - src/botsito/engine/
  - src/botsito/domain/
  - tests/unit/test_*.py
  - tests/golden/
  - docs/adr/0066-*.md
  - docs/validation/RN-004.md
  - docs/validation/RN-004-SALIDA.txt
  - docs/encargos/
  - PROJECT_STATE.md
rutas_protegidas:
  - src/botsito/engine/broker.py
  - src/botsito/engine/cuenta.py
  - knowledge/
  - config/
  - data/manifests/
comprobaciones:
  - uv run pytest tests/unit/test_estructura_m1.py tests/unit/test_cableado.py -q
  - uv run botsito motor arnes --salida arnes.txt
  - make check > make-check.log 2>&1
```

### Una rama de medicion (un criterio pre-registrado y su salida)

Escribe un script de medida, su criterio ANTES de medir y su salida; no cambia nada de lo que se
mide.

```yaml
rama: trabajo/medir-r1-r6-marzo
riesgo: alto  # lee filas de un libro: solo las dev, por la puerta, y se declara el mismo dia
artefacto: docs/validation/MEDIR-R1-R6-MARZO.md
rutas_permitidas:
  - scripts/medir_r1_r6.py
  - tests/unit/test_medir_r1_r6.py
  - docs/validation/MEDIR-R1-R6-MARZO.md
  - docs/validation/MEDIR-R1-R6-MARZO-CRITERIO.md
  - docs/validation/MEDIR-R1-R6-MARZO-SALIDA.txt
  - docs/validation/HOLDOUT-EXPOSICIONES.md
  - docs/encargos/
  - PROJECT_STATE.md
rutas_protegidas:
  - src/
  - knowledge/
  - config/
comprobaciones:
  - git log --format=%H -1 -- docs/validation/MEDIR-R1-R6-MARZO-CRITERIO.md
  - uv run python scripts/medir_r1_r6.py --salida docs/validation/MEDIR-R1-R6-MARZO-SALIDA.txt
  - make check > make-check.log 2>&1
```

La primera comprobacion es la del pre-registro: el criterio tiene que estar commiteado ANTES que la
salida. `HOLDOUT-EXPOSICIONES.md` esta permitido porque toda lectura se declara el mismo dia.

## El contrato de la primera rama que lo uso

`trabajo/guardias-claude` llevo el suyo desde el primer commit: `contrato.yaml` en esa rama, y
copiado en `docs/validation/GUARDIAS-CLAUDE.md` §2.
