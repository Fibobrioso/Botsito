"""El estado de la rama al abrir la sesion: hook `SessionStart` de Claude Code (E1).

Rama `trabajo/entorno-code` (2026-10-11; `docs/validation/ENTORNO-CODE.md`). Las sesiones se
compactan y al retomar se trabaja sobre un resumen: este hook pone delante, desde el primer
mensaje, lo que dice el repo: la rama y su ultimo commit, el contrato (artefacto, riesgo, tramo),
el encargo, la linea `## Estado` del informe, «ESPERANDO al consultor» si la ultima PARADA no tiene
respuesta y, en `main`, las letras vivas de la Next Action.

La guardia de `PreToolUse` no ve a este proceso, asi que se vigila el mismo:
- solo abre, con `leer`, las rutas de una lista CERRADA (`contrato.yaml`, `PROJECT_STATE.md`, el
  encargo de la rama y el artefacto del contrato); cualquier otra se niega;
- cada una pasa antes por `guardia.Politica(raiz).motivo_fichero`, la funcion con que la guardia
  decide si un fichero se lee; si da motivo, o si la guardia falla, no se lee y se dice;
- git solo de lectura; nunca bloquea: cualquier error es una linea y sale con 0.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import guardia  # noqa: E402  # la misma decision que la guardia de PreToolUse

RAIZ = Path(__file__).resolve().parents[2]
CABECERA = re.compile(r"^#{1,6}\s+(.*)$")
PARADA = re.compile(r"PARADA|Lo que necesito que decidas")
RESPUESTA = "Respuesta del consultor"


class NoSeLeeError(Exception):
    """Una ruta que `leer` no abre: fuera de la lista, bloqueada por la guardia o ilegible."""


def lista_cerrada(rama: str, artefacto: str | None) -> tuple[str, ...]:
    """Las UNICAS rutas (relativas a la raiz) que este hook puede abrir."""
    rutas = ["contrato.yaml", "PROJECT_STATE.md"]
    if rama:
        rutas.append(f"docs/encargos/{rama.replace('/', '-')}.md")
    if artefacto:
        rutas.append(artefacto)
    return tuple(rutas)


def leer(raiz: Path, rel: str, permitidas: tuple[str, ...]) -> str:
    """El UNICO sitio de este modulo que abre un fichero (lo comprueba un test)."""
    if rel not in permitidas:
        raise NoSeLeeError(f"{rel}: fuera de la lista cerrada del hook")
    ruta = raiz / rel
    try:
        motivo = guardia.Politica(raiz).motivo_fichero(str(ruta))
    except Exception as exc:  # negar por defecto: si la guardia no decide, no se lee
        raise NoSeLeeError(f"{rel}: la guardia no pudo decidir ({type(exc).__name__})") from exc
    if motivo:
        raise NoSeLeeError(f"{rel}: no se lee, la guardia lo bloquea")
    try:
        return ruta.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise NoSeLeeError(f"{rel}: no se pudo leer ({type(exc).__name__})") from exc


def git(raiz: Path, *args: str) -> str:
    r = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=raiz,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=5,
        check=False,
    )
    return r.stdout.strip() if r.returncode == 0 else ""


def campos_del_contrato(texto: str) -> dict[str, str]:
    """Las claves de primer nivel que el hook muestra, sin YAML (el hook corre con el python del
    sistema, como la guardia): `clave: valor  # comentario`, con o sin comillas."""
    campos: dict[str, str] = {}
    for linea in texto.splitlines():
        m = re.match(r"^(rama|riesgo|artefacto|tramo):\s*(.*?)\s*(?:#.*)?$", linea)
        if m:
            campos[m.group(1)] = m.group(2).strip().strip("'\"")
    return campos


def cabeceras(texto: str) -> list[str]:
    return [m.group(1) for linea in texto.splitlines() if (m := CABECERA.match(linea))]


def linea_de_estado(texto: str) -> str:
    """La primera linea no vacia tras `## Estado`, recortada."""
    lineas = texto.splitlines()
    for i, linea in enumerate(lineas):
        if linea.strip() == "## Estado":
            resto = next((x.strip() for x in lineas[i + 1 :] if x.strip()), "")
            return resto[:160] if resto else "(vacio)"
    return "(sin `## Estado`)"


def esperando(informe: str, encargo: str) -> tuple[bool, str | None]:
    """ESPERANDO si la ultima PARADA del informe es posterior a su ultima respuesta del consultor
    y hay mas PARADAS que respuestas copiadas en el encargo. Y un aviso si las respuestas no estan
    en los dos (se copian a los dos: skill `fase-cero`)."""
    cab = cabeceras(informe)
    paradas = [i for i, c in enumerate(cab) if PARADA.search(c) and RESPUESTA not in c]
    respuestas = [i for i, c in enumerate(cab) if RESPUESTA in c]
    en_encargo = sum(1 for c in cabeceras(encargo) if RESPUESTA in c)
    aviso = None
    if len(respuestas) != en_encargo:
        aviso = (
            f"AVISO: respuestas del consultor: {len(respuestas)} en el informe, {en_encargo} en el "
            "encargo (se copian a los dos)"
        )
    if not paradas:
        return False, aviso
    sin_respuesta = paradas[-1] > (respuestas[-1] if respuestas else -1)
    return sin_respuesta and len(paradas) > en_encargo, aviso


def letras_vivas(project_state: str) -> str:
    texto = project_state.split("\n## Next Action", 1)[-1].split("\n## ", 1)[0]
    letras = re.findall(r"^([A-Z])\. ", texto, re.M)
    return " ".join(letras) if letras else "(ninguna)"


def estado(raiz: Path) -> list[str]:
    salida: list[str] = []
    rama = git(raiz, "branch", "--show-current")
    commit = git(raiz, "log", "-1", "--oneline")
    salida.append(f"Rama: {rama or '(HEAD suelto)'} · ultimo commit: {commit or '(ninguno)'}")
    permitidas = lista_cerrada(rama, None)
    contrato: dict[str, str] = {}
    try:
        contrato = campos_del_contrato(leer(raiz, "contrato.yaml", permitidas))
    except NoSeLeeError as exc:
        if (raiz / "contrato.yaml").exists():
            salida.append(f"Contrato: {exc}")
    artefacto = contrato.get("artefacto")
    permitidas = lista_cerrada(rama, artefacto)
    if contrato:
        salida.append(
            f"Contrato: artefacto {artefacto or '?'} · riesgo {contrato.get('riesgo', '?')} · "
            f"tramo {contrato.get('tramo', '(sin tramo)')}"
        )
    if rama and rama != "main":
        rel_encargo = f"docs/encargos/{rama.replace('/', '-')}.md"
        encargo = ""
        try:
            encargo = leer(raiz, rel_encargo, permitidas)
            salida.append(f"Encargo: {rel_encargo}")
        except NoSeLeeError as exc:
            salida.append(f"Encargo: {exc}")
        if not contrato:
            salida.append("Informe: sin informe (no hay contrato)")
        elif artefacto and not (raiz / artefacto).exists():
            salida.append(f"Informe: sin informe ({artefacto} no existe)")
        elif artefacto:
            try:
                informe = leer(raiz, artefacto, permitidas)
            except NoSeLeeError as exc:
                salida.append(f"Informe: {exc}")
            else:
                salida.append(f"Estado del informe: {linea_de_estado(informe)}")
                espera, aviso = esperando(informe, encargo)
                if aviso:
                    salida.append(aviso)
                if espera:
                    salida.append("ESPERANDO al consultor: la ultima PARADA no tiene respuesta")
        else:
            salida.append("Informe: sin informe (no hay `artefacto` en el contrato)")
    if rama == "main":
        try:
            salida.append(
                f"Next Action: {letras_vivas(leer(raiz, 'PROJECT_STATE.md', permitidas))}"
            )
        except NoSeLeeError as exc:
            salida.append(f"Next Action: {exc}")
        ramas = [
            r
            for r in git(raiz, "for-each-ref", "--format=%(refname:short)", "refs/heads").split()
            if r != "main"
        ]
        salida.append("sin rama abierta" if not ramas else f"Ramas locales: {' '.join(ramas)}")
    salida.append("Para retomar: skill retomar-rama")
    return salida


def main() -> int:
    reconfigurar = getattr(sys.stdout, "reconfigure", None)
    if reconfigurar:
        reconfigurar(encoding="utf-8")
    try:
        raiz = Path(os.environ.get("CLAUDE_PROJECT_DIR") or RAIZ).resolve()
        print("\n".join(estado(raiz)))
    except Exception as exc:  # nunca bloquea la sesion
        print(f"estado_sesion: no se pudo leer el estado ({type(exc).__name__}: {exc})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
