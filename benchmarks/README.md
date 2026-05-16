# Benchmarks

A repeatable harness for measuring per-component latency directly against provider APIs. Bypasses any orchestrator so you can isolate **which model is actually slow**, not which orchestrator surfaced which number.

> **Note:** the production setup recommended in this playbook is `SIP trunk → ElevenLabs Agents Platform` direct — ElevenLabs is the orchestrator (see [`/telephony-and-sip`](../telephony-and-sip/README.md)). This script bypasses **all** orchestrators (including ElevenLabs) by hitting provider APIs directly with a `requests.post()`. That's intentional — it gives you a model-level latency floor without orchestrator overhead, useful for picking the fastest models. The production-call numbers in [`/models-and-latency`](../models-and-latency/README.md) are from a separate methodology (per-call instrumentation).

---

## What it measures

| Component | What's measured | How |
|---|---|---|
| **TTS** (ElevenLabs) | TTFB (time to first audio byte) + total | Streams `/v1/text-to-speech/{voice}/stream`, times the first non-empty chunk |
| **LLM** (OpenAI) | TTFT (time to first token) + total | Streams `/v1/chat/completions`, times the first SSE event with content |
| **STT** (Deepgram) | Wall-time of `/v1/listen` (pre-recorded) | Posts a small audio sample, times the whole request |

Pre-recorded STT is the simplest first cut. For phone agents, websocket streaming STT is what matters at runtime — that's a separate harness if you need it.

---

## Run it

Three env vars, then one command:

```bash
export ELEVENLABS_API_KEY=sk_...
export OPENAI_API_KEY=sk-...
export DEEPGRAM_API_KEY=...

python3 latency_matrix.py
```

Pipe to a file to keep results:

```bash
python3 latency_matrix.py > results-$(date +%Y-%m-%d).md
```

Only needs `pip install requests`. No other deps.

---

## What's measured by default

Default matrix (edit the constants at the top of `latency_matrix.py` to extend):

| Layer | Models |
|---|---|
| **TTS (ElevenLabs)** | Flash v2, Flash v2.5, Turbo v2, Turbo v2.5, Multilingual v2, Eleven v3 |
| **LLM (OpenAI)** | gpt-4o-mini, gpt-4.1-nano, gpt-4o |
| **STT (Deepgram)** | nova-2, nova-3, nova-3-general, flux-general-en |

`TRIALS = 3` per model — median is reported to smooth out one-off network noise.

The script generates **one shared audio sample** via ElevenLabs Flash v2.5, caches it to `/tmp/`, and feeds it to every Deepgram model. So you're comparing STT models on identical input.

---

## How to read the output

### TTFB / TTFT is the number that matters for phone agents

Total time matters for batch generation; **time-to-first-token / first-byte** is what determines how soon the user hears something. A model with low TTFB and high total can still feel snappy because audio starts playing while the rest streams.

### These numbers are floor, not ceiling

What you measure here is **provider API latency from your machine to the provider's nearest cluster**. Production adds:
- Orchestrator overhead (ElevenLabs Agents Platform, or your own backend)
- Telephony layer (RTP buffer, codec transcoding, carrier hops)
- VAD silence detection
- LLM prompt size (large system prompts can add 100s of ms)
- Connection pooling state (cold vs warm)

Expect production glass-to-glass to be **1.5–3×** the sum of the benchmark numbers, depending on stack.

### Median vs mean

The script uses median across `TRIALS` runs. Single runs are noisy — first request after cold start can be 5× the steady-state.

### What to do with the results

1. Pick the **fastest TTS that meets your quality bar** (Flash v2.5 is almost always the answer for realtime)
2. Pick the **cheapest LLM that meets your reasoning bar** (4.1-nano often beats 4o-mini on latency without losing much on routine intents)
3. For STT, Deepgram nova-3 is usually the sweet spot; flux-general-en for ultra-low latency English-only
4. Sum the medians → that's your **inference floor**. Compare against your real production turn latency to see how much overhead your stack adds.

---

## Extending the matrix

To add a Claude or Gemini LLM benchmark, copy the `bench_llm()` function pattern in `latency_matrix.py` and point it at the provider's streaming endpoint. Same for any other TTS provider (MiniMax, LMNT, smallest-ai).

Production tip: keep a CI job that runs this script once a day against the same machine, posts results to a Slack channel, and alerts if any model's TTFB regresses > 25% week-over-week. You'll catch provider-side regressions before your users do.

---

## Sources of truth

- [ElevenLabs Text to Speech (capability + endpoints)](https://elevenlabs.io/docs/overview/capabilities/text-to-speech)
- [OpenAI chat completions streaming](https://platform.openai.com/docs/api-reference/chat/streaming)
- [Deepgram pre-recorded transcription](https://developers.deepgram.com/reference/listen-file)
- Playbook latency section: [`/models-and-latency`](../models-and-latency/README.md)


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*