# docs/spec/

La spec **legible por una persona**, GENERADA desde `knowledge/spec/` por `botsito spec docs`.
No se edita a mano: `make check` regenera y compara, y dice que fichero no cuadra.

| Fichero | Sale de | Sellado |
|---|---|---|
| `reglas.md` | `strategy_spec.yaml` (reglas y vocabulario) | si, con `spec_version` y hash |
| `parametros.md` | `parametros.yaml` | si |
| `glosario.md` | `glossary.yaml` | si |
| `ambiguedades.md` | `ambiguedades.yaml` | **no**: el hash de la spec cubre los otros tres |

Este README es el unico fichero de la carpeta que se escribe a mano, y a proposito no lleva
ninguna cifra viva: el recuento lo dan los documentos generados y `botsito spec status`.
