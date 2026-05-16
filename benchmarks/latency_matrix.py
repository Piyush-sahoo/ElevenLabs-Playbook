#!/usr/bin/env python3
"""
Latency matrix benchmark — measure per-component latency directly against
provider APIs. Bypasses Vapi/orchestrators so you can isolate which model is
slow.

Components measured:
  - TTS  (ElevenLabs)     : time-to-first-audio-byte (TTFB) + total
  - LLM  (OpenAI)         : time-to-first-token (TTFT) + total
  - STT  (Deepgram)       : pre-recorded transcription wall-time

Usage:
  export ELEVENLABS_API_KEY=sk_...
  export OPENAI_API_KEY=sk-...
  export DEEPGRAM_API_KEY=...
  python3 latency_matrix.py

Prints a markdown table. Pipe to a file to capture:
  python3 latency_matrix.py > results.md

Extend the MATRIX constants at the top to add models.
"""

import os
import sys
import time
import json
import statistics
from typing import Optional

import requests  # pip install requests

# --- Configuration ----------------------------------------------------------
TTS_MODELS = [
    # (model_id, label) — complete set Vapi exposes
    ("eleven_flash_v2",        "Flash v2"),
    ("eleven_flash_v2_5",      "Flash v2.5"),
    ("eleven_turbo_v2",        "Turbo v2"),
    ("eleven_turbo_v2_5",      "Turbo v2.5"),
    ("eleven_multilingual_v2", "Multilingual v2"),
    ("eleven_english_v1",      "English v1 (legacy)"),
    # v3 is excluded from realtime by ElevenLabs (HTTP streaming, higher TTFB) — kept for comparison
    ("eleven_v3",              "Eleven v3 (experimental)"),
]

# A neutral default voice that exists in every account's free library.
# Override via env if you want to benchmark a specific clone.
TTS_VOICE_ID = os.environ.get("EL_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Rachel

LLM_MODELS = [
    "gpt-4o-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    # add Claude / Gemini here if you have their keys
]

STT_MODELS = [
    "nova-2",
    "nova-3",
    "nova-3-general",
    "flux-general-en",
]

# Fixed test inputs — short, realistic for a phone-agent turn
TTS_TEXT = "Sure, let me check that for you. One moment please."
LLM_PROMPT = (
    "You are a customer support agent. The user just said: "
    "'My order hasn't arrived.' Reply in one short sentence."
)

# How many trials per (model, request) — median is reported
TRIALS = 3

EL_KEY = os.environ.get("ELEVENLABS_API_KEY")
OAI_KEY = os.environ.get("OPENAI_API_KEY")
DG_KEY = os.environ.get("DEEPGRAM_API_KEY")


# --- Helpers ----------------------------------------------------------------
def require(key_value: Optional[str], name: str) -> None:
    if not key_value:
        sys.stderr.write(f"missing env var: {name}\n")
        sys.exit(2)


def median_ms(values):
    vals = [v for v in values if v is not None]
    return statistics.median(vals) if vals else None


def fmt(x):
    return f"{int(round(x))}" if x is not None else "—"


# --- TTS (ElevenLabs) -------------------------------------------------------
def bench_tts(model_id: str) -> dict:
    """Return {'ttfb_ms': float|None, 'total_ms': float|None}."""
    require(EL_KEY, "ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{TTS_VOICE_ID}/stream"
    headers = {"xi-api-key": EL_KEY, "Content-Type": "application/json"}
    payload = {"text": TTS_TEXT, "model_id": model_id}

    t0 = time.perf_counter()
    try:
        r = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    except Exception as e:
        return {"ttfb_ms": None, "total_ms": None, "err": str(e)}
    if r.status_code >= 400:
        return {"ttfb_ms": None, "total_ms": None, "err": f"HTTP {r.status_code}: {r.text[:120]}"}

    ttfb = None
    bytes_received = 0
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            if ttfb is None:
                ttfb = (time.perf_counter() - t0) * 1000
            bytes_received += len(chunk)
    total = (time.perf_counter() - t0) * 1000
    return {"ttfb_ms": ttfb, "total_ms": total, "bytes": bytes_received}


# --- LLM (OpenAI streaming) -------------------------------------------------
def bench_llm(model: str) -> dict:
    require(OAI_KEY, "OPENAI_API_KEY")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {OAI_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": LLM_PROMPT}],
        "stream": True,
        "max_tokens": 60,
    }
    t0 = time.perf_counter()
    try:
        r = requests.post(url, headers=headers, json=payload, stream=True, timeout=30)
    except Exception as e:
        return {"ttft_ms": None, "total_ms": None, "err": str(e)}
    if r.status_code >= 400:
        return {"ttft_ms": None, "total_ms": None, "err": f"HTTP {r.status_code}: {r.text[:120]}"}

    ttft = None
    for line in r.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8", errors="ignore")
        if decoded.startswith("data:") and "[DONE]" not in decoded:
            try:
                payload = json.loads(decoded[5:].strip())
                if payload.get("choices", [{}])[0].get("delta", {}).get("content"):
                    if ttft is None:
                        ttft = (time.perf_counter() - t0) * 1000
            except Exception:
                pass
    total = (time.perf_counter() - t0) * 1000
    return {"ttft_ms": ttft, "total_ms": total}


# --- STT (Deepgram pre-recorded) --------------------------------------------
# We generate the audio sample once via ElevenLabs Flash v2.5, then transcribe
# it with each Deepgram model. This gives a consistent input across runs.
_AUDIO_CACHE_PATH = "/tmp/elevenlabs_playbook_stt_sample.mp3"


def _ensure_stt_audio() -> bytes:
    if os.path.exists(_AUDIO_CACHE_PATH):
        return open(_AUDIO_CACHE_PATH, "rb").read()
    require(EL_KEY, "ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{TTS_VOICE_ID}"
    headers = {"xi-api-key": EL_KEY, "Content-Type": "application/json"}
    payload = {
        "text": "My order number is one two three four five and it has not arrived yet.",
        "model_id": "eleven_flash_v2_5",
    }
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    open(_AUDIO_CACHE_PATH, "wb").write(r.content)
    return r.content


def bench_stt(model: str) -> dict:
    require(DG_KEY, "DEEPGRAM_API_KEY")
    audio = _ensure_stt_audio()
    url = f"https://api.deepgram.com/v1/listen?model={model}&smart_format=true"
    headers = {"Authorization": f"Token {DG_KEY}", "Content-Type": "audio/mpeg"}
    t0 = time.perf_counter()
    try:
        r = requests.post(url, headers=headers, data=audio, timeout=30)
    except Exception as e:
        return {"total_ms": None, "err": str(e)}
    total = (time.perf_counter() - t0) * 1000
    if r.status_code >= 400:
        return {"total_ms": None, "err": f"HTTP {r.status_code}: {r.text[:120]}"}
    return {"total_ms": total}


# --- Runners ----------------------------------------------------------------
def run_tts():
    rows = []
    for model_id, label in TTS_MODELS:
        ttfbs, totals = [], []
        err = None
        for _ in range(TRIALS):
            res = bench_tts(model_id)
            if res.get("err"):
                err = res["err"]
                break
            ttfbs.append(res["ttfb_ms"])
            totals.append(res["total_ms"])
        rows.append((label, model_id, median_ms(ttfbs), median_ms(totals), err))
    return rows


def run_llm():
    rows = []
    for model in LLM_MODELS:
        ttfts, totals = [], []
        err = None
        for _ in range(TRIALS):
            res = bench_llm(model)
            if res.get("err"):
                err = res["err"]
                break
            ttfts.append(res["ttft_ms"])
            totals.append(res["total_ms"])
        rows.append((model, median_ms(ttfts), median_ms(totals), err))
    return rows


def run_stt():
    rows = []
    for model in STT_MODELS:
        totals = []
        err = None
        for _ in range(TRIALS):
            res = bench_stt(model)
            if res.get("err"):
                err = res["err"]
                break
            totals.append(res["total_ms"])
        rows.append((model, median_ms(totals), err))
    return rows


# --- Output -----------------------------------------------------------------
def main():
    out = []
    out.append("# Latency matrix — measured\n")
    out.append(f"_Trials per model: {TRIALS} (median reported)._\n")
    out.append(f"_Run from a machine in: {os.environ.get('REGION', '(unknown)')}._\n")
    out.append("")

    if EL_KEY:
        out.append("## ElevenLabs TTS")
        out.append("")
        out.append("| Model | model_id | TTFB ms | Total ms | Error |")
        out.append("|---|---|---:|---:|---|")
        for label, mid, ttfb, total, err in run_tts():
            out.append(f"| {label} | `{mid}` | {fmt(ttfb)} | {fmt(total)} | {err or ''} |")
        out.append("")

    if OAI_KEY:
        out.append("## OpenAI LLM (streaming chat.completions)")
        out.append("")
        out.append("| Model | TTFT ms | Total ms | Error |")
        out.append("|---|---:|---:|---|")
        for model, ttft, total, err in run_llm():
            out.append(f"| `{model}` | {fmt(ttft)} | {fmt(total)} | {err or ''} |")
        out.append("")

    if DG_KEY:
        out.append("## Deepgram STT (pre-recorded)")
        out.append("")
        out.append("| Model | Total ms | Error |")
        out.append("|---|---:|---|")
        for model, total, err in run_stt():
            out.append(f"| `{model}` | {fmt(total)} | {err or ''} |")
        out.append("")

    print("\n".join(out))


if __name__ == "__main__":
    main()
