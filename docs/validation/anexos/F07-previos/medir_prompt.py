"""Mide en v5 (365 s) tres variantes: sin prompt, initial_prompt, hotwords. Cuenta terminos."""
import json, re, sys, time, pathlib
sys.path.insert(0, "src")
from botsito.corpus.motor_whisper import _anadir_dlls_cuda
_anadir_dlls_cuda()
from faster_whisper import WhisperModel
from faster_whisper.utils import download_model
V2 = ['EURUSD','M1','M15','H4','break even','cartucho','FTMO','FundedNext','fondeo','mitigacion','breaker','zona de control','orden limite','stop loss','take profit','lotaje','spread','FXReplay','TradingView','MetaTrader','mitigación','orden límite','BOS','order flow','order block','complex pullback','backtesting','Gann','TP','SL','RR']
voc = ", ".join(V2)
wav = "data/transcripciones/v5/audio.wav"
m = WhisperModel(download_model("large-v3"), device="cuda", compute_type="int8_float16")
base = dict(language="es", beam_size=5, temperature=0.0, word_timestamps=True, vad_filter=True, condition_on_previous_text=False)
variantes = {"sin_prompt": {}, "initial_prompt": {"initial_prompt": voc}, "hotwords": {"hotwords": voc}}
buenos = ["stop loss","take profit","break even","spread","lotaje","BOS","order flow","order block","backtest","TP","SL","RR","Gann","mitigaci","FXReplay"]
malos = ["store loss","orden flow","gan ","boss","voz","blog","split","sprint","rotaje","tepes","bacteseando"]
res = {}
for nombre, extra in variantes.items():
    t = time.time()
    segs, _ = m.transcribe(wav, **base, **extra)
    texto = " ".join(s.text for s in segs)
    dur = time.time() - t
    low = texto.lower()
    res[nombre] = {"s": round(dur,1), "chars": len(texto),
        "buenos": {b: len(re.findall(r"(?<!\w)"+re.escape(b.lower()), low)) for b in buenos},
        "malos": {b: len(re.findall(r"(?<!\w)"+re.escape(b.lower()), low)) for b in malos}}
    pathlib.Path(f"medir_{nombre}.txt").write_text(texto, encoding="utf-8")
    print(nombre, json.dumps(res[nombre], ensure_ascii=False), flush=True)
pathlib.Path("medir_resultado.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
