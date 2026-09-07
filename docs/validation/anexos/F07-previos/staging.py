"""Carpeta lista para arrastrar a Drive: crudas + manifiestos + WAV + v5, con SHA256SUMS."""
import hashlib, shutil, sys, yaml, pathlib
sys.path.insert(0, "src")
dst = pathlib.Path("data/drive_staging"); dst.mkdir(exist_ok=True)
d = pathlib.Path("knowledge/corpus/transcripciones")
docs = {p.stem: (p, yaml.safe_load(p.read_text(encoding="utf-8"))) for p in d.glob("tr-*.yaml")}
reemplazados = {m.get("reemplaza_a") for _, m in docs.values() if m.get("reemplaza_a")}
lineas = []
def add(src, name):
    out = dst / name
    if not out.exists() or out.stat().st_size != src.stat().st_size: shutil.copy2(src, out)
    h = hashlib.sha256(out.read_bytes()).hexdigest(); lineas.append(f"{h}  {name}"); return h
for tid, (p, m) in sorted(docs.items()):
    if tid in reemplazados: continue
    v = m["video_id"]; c = pathlib.Path("data") / m["carpeta"]
    h = add(c / "cruda.jsonl", f"{tid}.cruda.jsonl"); assert h == m["sha256_cruda"], tid
    add(c / "cruda.txt", f"{tid}.cruda.txt"); add(p, p.name)
    hw = add(pathlib.Path(f"data/transcripciones/{v}/audio.wav"), f"{v}.audio.wav"); assert hw == m["sha256_wav"], v
add(pathlib.Path("corpus/Estrategia del trader/2026-09-05 21-03-59.mkv"), "2026-09-05 21-03-59.mkv")
(dst / "SHA256SUMS.txt").write_text("\n".join(lineas) + "\n", encoding="utf-8", newline="\n")
print("\n".join(lineas)); print("total MiB", sum(f.stat().st_size for f in dst.iterdir()) / 2**20)
