# Getting Started

The shortest path from "I have an ElevenLabs account" to "a phone is ringing my agent."

---

## What ElevenLabs Agents Platform gives you

A single dashboard where you assemble an agent end-to-end. Everything below ships with the platform — no separate orchestrator, no glue code required.

- **Voice** — pick from the library, design a new voice with a text prompt, or clone your own
- **LLM** — bring GPT, Claude, Gemini, or use the default — ElevenLabs handles the routing
- **STT** — Scribe v2 Realtime, multilingual, built-in
- **TTS** — Flash / Turbo / Multilingual / v3 — picked per agent
- **Tools** — system tools (transfer, language detect, DTMF) + server tools (webhooks to your backend) + MCP
- **Telephony** — import a phone number from any SIP trunk, attach it to an agent, done
- **Workflows** — visual graph for multi-step / multi-intent conversations
- **Post-call webhooks** — full transcript + metrics fire to your endpoint when the call ends

---

## Three steps to your first call

### 1. Create a voice (or pick one)

In the Dashboard → **Voices**. Three options:
- **Library voice** — fastest, no setup. Browse and pick.
- **Voice Design** — describe a voice in 20–1000 chars, get 3 previews, pick one.
- **Instant Voice Clone** — upload ~1–2 minutes of clean audio. Done in seconds.

For Indian-language phone agents, see [`/multilingual`](../multilingual/README.md) for a curated list of library voices by use case.

### 2. Create an agent

Dashboard → **Agents Platform** → **Create**. The defaults are sane; you only really need to set:
- **System prompt** — personality and goal. See [`/prompt-patterns`](../prompt-patterns/README.md) for ready-to-use templates.
- **First message** — what the agent says when the call connects.
- **Voice** — pick the one you made in step 1.
- **Language** — set explicitly if single-language, or use auto-detect for multilingual.

Click **Test** in the dashboard. Talk to it through your laptop mic. Iterate on the prompt until the first 30 seconds feels right.

### 3. Attach a phone number

Dashboard → **Phone Numbers** → **Import from SIP Trunk**. Enter your trunk credentials (from your provider — Vobiz / Twilio / etc.) and the DID you want to use. Click **Attach** next to the imported number → pick your agent.

Call the number from your phone. Your agent picks up.

For the full SIP trunk setup (codecs, transports, troubleshooting), see [`/telephony-and-sip`](../telephony-and-sip/README.md).

---

## What to tune next (linked deep dives)

| If you want to… | Read |
|---|---|
| Understand which TTS / LLM model to pick and why | [`/models-and-latency`](../models-and-latency/README.md) |
| Add tools (CRM lookup, transfer to human, etc.) | [`/tools-and-workflows`](../tools-and-workflows/README.md) |
| Write a production-grade system prompt | [`/prompt-patterns`](../prompt-patterns/README.md) |
| Forecast cost at your call volume | [`/cost-analysis`](../cost-analysis/README.md) |
| Ship to production without surprises | [`/production-best-practices`](../production-best-practices/README.md) |

---

## Sources of truth

- [Agents Platform quickstart](https://elevenlabs.io/docs/agents-platform/quickstart)
- [Voices capabilities](https://elevenlabs.io/docs/overview/capabilities/voices)
- [Instant Voice Cloning](https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/instant-voice-cloning)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*