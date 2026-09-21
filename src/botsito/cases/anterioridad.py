"""La prueba de que un reparto se fijo ANTES de la etiqueta, emparejando por CASO (ADR-0036).

Por que existe, y por que entra con el camino de fidelidad y no en otra rama: lo unico que ese
camino puede prometer es **anterioridad demostrable** -potencia estadistica no tiene, y eso esta
medido-. Sin una comprobacion mecanica, el camino afirmaria justo lo que no puede probar.

**Empareja por CASO, no por sesion.** La guardia del kit (`paquete.validar_paquetes`) busca los
`LABEL_CASE` cuyo campo `sesion` coincide con el nombre de la carpeta del paquete, y nunca los que
etiquetan un caso DE ese paquete. Es deuda anotada cuatro veces (MESES-VISTOS.md §3, la rama del
breaker, la del universo congelado y la de los cupos), con dos agujeros medidos: una etiqueta sobre
un caso de un paquete puede llevar en `sesion` el nombre de otro -cuyo `particiones.yaml` es
ancestro de todo- y pasar; y una `sesion` sin paquete no la visita el bucle siquiera. En el camino
de fidelidad NO HAY SESION, asi que emparejar por ella no es solo insuficiente: es imposible. La
guardia nueva y la deuda vieja son el mismo trabajo, y esto lo cierra.

El id de caso sirve de clave porque es GLOBAL: `ventanas.id_caso` da `caso-<simbolo>-<dia>`, uno
por dia y simbolo, en cualquier reparto de cualquier camino.

**Que prueba cada pieza, que no es lo mismo:**

- El ANCLA (`anclas.yaml`, ADR-0035 enmendado) prueba INMUTABILIDAD: que el contenido es byte a
  byte el declarado. Un sha de blob no lleva tiempo dentro: no ordena nada. Su valor es que no se
  desentiende cuando no hay etiquetas, que es el periodo actual.
- Esta guardia prueba ANTERIORIDAD, y solo la puede dar el DAG de git: el commit que anadio el
  reparto es ancestro ESTRICTO del que anadio la etiqueta.

Hacen falta las dos y ninguna sustituye a la otra: el ancla cubre desde que el reparto se commitea
hasta que aparece la primera etiqueta; esta, el instante en que aparece.

**Disciplina de holdout:** aqui se usan `accion`, `objetivo.id`, `id` y `sesion` de cada registro.
NUNCA `valor_resultante`, que es la etiqueta. Leer la ASIGNACION no es abrir; leer el valor, si.
"""

from __future__ import annotations

from pathlib import Path

from botsito.cases.holdout import repartos_commiteables
from botsito.comun.historial import commit_que_anadio, es_ancestro, intacto_desde
from botsito.comun.yaml_estricto import YamlError, leer_yaml
from botsito.feedback.modelo import FeedbackRecord


def indice_de_repartos(repo: Path) -> tuple[dict[str, tuple[str, str]], list[str]]:
    """`caso -> (ruta de su particiones.yaml, nombre del reparto)`, de los DOS caminos.

    Un caso en dos repartos es PROBLEMA: se sortea una vez, y dos repartos del mismo dia harian
    ambigua la prueba de anterioridad -cual de los dos es el que tiene que ser anterior-.
    """
    indice: dict[str, tuple[str, str]] = {}
    problemas: list[str] = []
    for fichero in repartos_commiteables(repo):
        try:
            doc = leer_yaml(fichero)
        except (OSError, YamlError):
            continue  # el esquema lo denuncian los validadores de cada camino
        asignacion = doc.get("asignacion") if isinstance(doc, dict) else None
        if not isinstance(asignacion, dict):
            continue
        ruta = fichero.relative_to(repo).as_posix()
        nombre = fichero.parent.name
        for caso in asignacion:
            anterior = indice.get(str(caso))
            if anterior is not None:
                problemas.append(
                    f"{caso} esta repartido dos veces: en {anterior[1]} y en {nombre}. Un caso se "
                    f"sortea una vez, o la prueba de anterioridad es ambigua"
                )
                continue
            indice[str(caso)] = (ruta, nombre)
    return indice, problemas


def problemas_de_anterioridad(repo: Path, registros: list[FeedbackRecord]) -> list[str]:
    """Toda etiqueta cae sobre un caso repartido, y su reparto es anterior a ella. Sin `data/`."""
    indice, problemas = indice_de_repartos(repo)
    # La lista CRUDA, no los activos: una etiqueta supersedida se leyo igual, y lo que se prueba
    # aqui es cuando se leyo respecto al reparto.
    etiquetas = [r for r in registros if r.accion == "LABEL_CASE"]
    for r in etiquetas:
        caso = r.objetivo.id
        entrada = indice.get(caso)
        if entrada is None:
            problemas.append(
                f"{r.id}: LABEL_CASE sobre {caso}, que ningun reparto commiteado contiene. La "
                f"anterioridad no se puede probar contra nada"
            )
            continue
        ruta_reparto, nombre = entrada
        alta_reparto = commit_que_anadio(repo, ruta_reparto)
        if alta_reparto is None:
            problemas.append(
                f"{nombre}: hay un LABEL_CASE sobre {caso} y su reparto no esta commiteado"
            )
            continue
        ruta_fb = f"knowledge/feedback/{r.sesion}/{r.id}.yaml"
        alta_fb = commit_que_anadio(repo, ruta_fb)
        if alta_fb is None:
            continue  # el registro sin commitear lo vigila la guardia de feedback
        if (
            alta_fb[0] == alta_reparto[0]
            or es_ancestro(repo, alta_reparto[0], alta_fb[0]) is not True
        ):
            problemas.append(
                f"{nombre}: el reparto que contiene {caso} ({alta_reparto[0][:7]}, "
                f"{alta_reparto[1]}) no es anterior a su LABEL_CASE {r.id} ({alta_fb[0][:7]}, "
                f"{alta_fb[1]})"
            )
            continue
        for nombre_fichero in ("particiones.yaml", "ventanas.yaml"):
            ruta = f"{Path(ruta_reparto).parent.as_posix()}/{nombre_fichero}"
            origen = commit_que_anadio(repo, ruta)
            if origen is not None and intacto_desde(repo, origen[0], ruta) is not True:
                problemas.append(
                    f"{nombre}: {nombre_fichero} cambio despues de su commit {origen[0][:7]} y ya "
                    f"hay un LABEL_CASE sobre {caso} (el reparto es inmutable tras la etiqueta)"
                )
    return problemas
