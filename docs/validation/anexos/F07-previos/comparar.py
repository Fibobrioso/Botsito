"""Compara la cruda activa nueva de cada video con la reemplazada: ratio de palabras, segmentos,
duracion maxima de segmento, y presencia de hechos clave (por texto)."""
import json, re, difflib, sys, yaml, pathlib
sys.path.insert(0, "src")
d = pathlib.Path("knowledge/corpus/transcripciones")
docs = {p.stem: yaml.safe_load(p.read_text(encoding="utf-8")) for p in d.glob("tr-*.yaml")}
reemplazados = {v.get("reemplaza_a") for v in docs.values() if v.get("reemplaza_a")}
def load(c): return [json.loads(l) for l in open("data/" + c + "/cruda.jsonl", encoding="utf-8")]
HECHOS = {"v1": ["0.75", "50", "Gann"], "v2": ["4.08", "3.94", "stop loss", "order flow"], "v3": ["2.83", "3.3", "utc", "backtesteando", "TPs"],
          "v4": ["1.19537", "0.50", "0.40", "spread", "lotaje", "tres"], "v5": ["0.80", "por defecto", "sell", "1.3", "1.4"]}
for tid, m in sorted(docs.items()):
    if tid in reemplazados or not m.get("reemplaza_a"): continue
    v = m["video_id"]; old = docs[m["reemplaza_a"]]
    a, b = load(old["carpeta"]), load(m["carpeta"])
    ta, tb = " ".join(s["texto"] for s in a), " ".join(s["texto"] for s in b)
    wa, wb = re.findall(r"\w+", ta.lower()), re.findall(r"\w+", tb.lower())
    sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
    print(f"{v}: {tid} reemplaza {m['reemplaza_a']}: segmentos {len(a)}->{len(b)}, palabras {len(wa)}->{len(wb)}, ratio {sm.ratio():.3f}, "
          f"max seg {max(s['t1_ms']-s['t0_ms'] for s in b)/1000:.1f}s, habla {old['ms_con_habla']/1000:.0f}->{m['ms_con_habla']/1000:.0f}s, senales {m['senales']}, huecos {len(m['huecos'])}, tokens {m['motor'].get('initial_prompt_tokens')}")
    for h in HECHOS[v]: print("   ", h, "vieja", h.lower() in ta.lower(), "nueva", h.lower() in tb.lower())
    grandes = [(t, " ".join(wa[i1:i2])[:80], " ".join(wb[j1:j2])[:80]) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != "equal" and (i2-i1 > 6 or j2-j1 > 6)]
    print("    bloques >6 palabras distintos:", len(grandes))
    for g in grandes[:12]: print("     ", g)
