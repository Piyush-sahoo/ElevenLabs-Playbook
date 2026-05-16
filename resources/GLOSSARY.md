# Glossary

One-line definitions for the acronyms and jargon used across this playbook.

## Voice AI pipeline

| Term | Stands for | One-line definition |
|---|---|---|
| **STT** | Speech-to-Text | Converts spoken audio into text. ElevenLabs uses **Scribe v2 Realtime**. |
| **TTS** | Text-to-Speech | Converts text into spoken audio. ElevenLabs offers Flash / Turbo / Multilingual / v3 model families. |
| **LLM** | Large Language Model | The "brain" that decides what to say next. GPT, Claude, Gemini, etc. |
| **VAD** | Voice Activity Detection | Detects when the user starts and stops speaking. Used for turn-taking. |
| **Endpointing** | — | The decision logic for "is the user done talking?" — combines VAD + silence timeouts. Tunable on the agent platform. |
| **Turn** | — | One round: user speaks → agent listens → agent speaks. Latency is usually measured per turn. |
| **Glass-to-glass latency** | — | Wall-clock time from "user stops speaking" to "user hears agent's first audio." The number that actually matters. |

## Latency-specific

| Term | Stands for | One-line definition |
|---|---|---|
| **TTFB** | Time To First Byte | Wall-clock time from sending a TTS request to receiving the first audio byte back. Streaming-specific. |
| **TTFA** | Time To First Audio | Same as TTFB, but framed in audio terms. The user-perceived "start of speech." |
| **TTFT** | Time To First Token | LLM-specific: time from request to first generated token. Streaming chat completions. |
| **Inference latency** | — | The model's compute time only — excludes network, queueing, streaming buffer. Vendor specs almost always quote this. |
| **P50 / P95 / P99** | percentiles | Median / 95th / 99th percentile of latency. Production targets are usually P95 budgets, not averages. |

## Voice cloning & generation

| Term | Stands for | One-line definition |
|---|---|---|
| **IVC** | Instant Voice Clone | Quick clone from ~1–2 min of audio. No model training, few-shot adaptation. |
| **PVC** | Professional Voice Clone | Studio-grade clone from 30 min – 3 hr of audio. Higher quality, higher latency per generation. |
| **Stability** | — | ElevenLabs voice setting (0.0–1.0). Low = more emotional / variable. High = more monotone / consistent. |
| **Similarity boost** | — | ElevenLabs voice setting (0.0–1.0). High = closer to source voice. Low = more model creativity. |
| **Style exaggeration** | — | Multilingual v2 / v3 setting (0.0–1.0). Amplifies emotional character; adds latency per notch. |

## Telephony

| Term | Stands for | One-line definition |
|---|---|---|
| **PSTN** | Public Switched Telephone Network | The traditional phone network (carriers, copper, mobile). Everything that's not a VoIP-native call. |
| **SIP** | Session Initiation Protocol | The signaling layer that sets up / tears down voice calls over IP. Usually port 5060. |
| **RTP** | Real-time Transport Protocol | Carries the actual audio between endpoints. UDP-based (TCP overhead would cause jitter). |
| **SRTP** | Secure RTP | Encrypted RTP. Required for production. |
| **TLS** | Transport Layer Security | Encryption for the SIP signaling layer. Pair with SRTP for end-to-end. |
| **DID** | Direct Inward Dialing number | The phone number callers dial. Bought from a trunk provider, attached to an agent. |
| **E.164** | — | International phone number format with `+` prefix and country code (e.g. `+919876543210`). |
| **SIP trunk** | — | The logical pipe between your trunk provider and ElevenLabs. Carries SIP + RTP. |
| **FQDN** | Fully Qualified Domain Name | Hostname like `sip.rtc.elevenlabs.io`. Used in SIP trunk addressing. |
| **IVR** | Interactive Voice Response | The "press 1 for billing" menu system. ElevenLabs agents can act as one, or traverse one via DTMF. |
| **DTMF** | Dual-Tone Multi-Frequency | The touch-tone signals from a phone keypad. Generated via the `play_dtmf` system tool. |
| **µ-law (mu-law)** | — | The default 8 kHz audio codec on PSTN calls. Lossy compression. Synonym: G.711 µ-law. |
| **G.711 / G.722 / Opus** | — | Audio codecs. G.711 = narrowband, G.722 = wideband, Opus = highest quality when supported. |
| **Jitter** | — | Variation in packet arrival times. Causes choppy audio. RTP receivers use a buffer to smooth it. |
| **MOS** | Mean Opinion Score | Subjective audio-quality rating, 1.0 (bad) to 5.0 (excellent). Production phone audio is usually MOS 3.5–4.2. |

## STT-specific

| Term | Stands for | One-line definition |
|---|---|---|
| **WER** | Word Error Rate | STT accuracy metric: percentage of words wrong. Lower = better. Hindi STT on ElevenLabs: ≤ 5 % WER on clean audio. |

## Other

| Term | Stands for | One-line definition |
|---|---|---|
| **MCP** | Model Context Protocol | Standard for connecting AI agents to external tools. ElevenLabs supports MCP servers as a runtime tool surface (see [`/mcp-integration`](../mcp-integration/README.md)). |
| **Webhook** | — | An HTTPS endpoint your backend exposes that an external system (ElevenLabs) calls when an event happens. Used for server tools and post-call analytics. |
| **trust_context** | — | ElevenLabs agent setting: `low_trust` (external callers, restricted tools) or `high_trust` (internal users, full access). |
| **Token (LLM)** | — | The unit LLMs count for billing. Roughly 0.75 words. A 100k-token prompt is a 5,000-line system message. |


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*