# Multilingual

This section is opinionated. Official docs say "Multilingual v2 supports 29 languages." Production tells you **which of those 29 actually sound right on a phone call**.

---

## Language coverage at a glance

| Layer | Model | Indian languages |
|---|---|---|
| **TTS** | Multilingual v2 | Hindi, Tamil, Kannada, Bengali, others |
| **TTS (low latency)** | Flash v2.5 | 32 languages including Hindi |
| **STT (realtime)** | Scribe v2 Realtime | **11 Indian languages**: Hindi, Tamil, Telugu, Malayalam, Bengali, Gujarati, Kannada, Odia, Marathi, Punjabi, Sindhi |

For Indian-market deployments:
- **STT:** Scribe v2 Realtime — only realtime-capable model with 11 Indian languages
- **TTS:** Flash v2.5 first (latency); fall back to Multilingual v2 if prosody drifts on a specific language

---

## Quality ratings — observed

These are practitioner ratings from production listening tests, not benchmarks. They reflect **how the voice actually lands on a phone call**, accent included.

| Language | Rating | Notes |
|---|---|---|
| **Hindi** | 9 / 10 | Very natural prosody, handles formal + casual registers well |
| **Hinglish** (Hindi + English code-switch) | 8 / 10 | Strong overall; some pronunciation drift on English brand names and proper nouns |
| **Tamil** | 8.5 / 10 | Strong rhythm, good for support/sales |
| **Kannada** | 7 / 10 | Formal register sounds more natural than casual conversation |
| **Bengali** | 6.5 / 10 | Accent inconsistency between sentences — noticeable on long turns |

> If you're shipping into one of these markets and the rating is **< 8**, plan for either Multilingual v2 fallback, voice cloning with a native speaker, or shorter agent turns to mask inconsistency.

---

## Hindi STT accuracy

Per the [ElevenLabs India page](https://elevenlabs.io/india): **Hindi achieves ≤ 5% Word Error Rate** in Scribe.

That's competitive with English STT on clean audio. On phone-quality audio (8kHz µ-law), expect WER to roughly double — design your tool-call confirmation flows assuming the agent may have misheard.

---

## Code-switching — the India-critical case

Indian callers code-switch constantly:

> "Sir your KYC pending hai but Aadhaar verification done ho gaya."

| Behavior | Multilingual v2 | Flash v2.5 |
|---|---|---|
| Sentence-level switch (full Hindi → full English) | Handles well | Handles well |
| Mid-sentence switch (Hinglish) | Mostly handles | Some pronunciation drift on English nouns |
| Switching every few words | Both can drift; voice may sound "Hindi-accented English" rather than fluent mix |
| English brand/product names in Hindi sentence | Both occasionally mispronounce — pre-define phonetic spellings in the prompt if critical (e.g. "say 'ICICI' as 'I-C-I-C-I'") |

**Practical recipe for Hinglish agents:**
1. Set language to **auto-detect** in agent config
2. Use **Multilingual v2** as the TTS model (Flash v2.5 only if latency budget is tight)
3. In the system prompt, instruct the agent to mirror the caller's register — "If the user speaks Hinglish, respond in Hinglish. If they switch fully to English, switch with them."
4. For critical brand/product names, supply phonetic spellings in the prompt
5. Watch the post-call transcript for drift patterns and feed them back into the prompt

---

## When to pick which model for multilingual

| Scenario | TTS pick | Why |
|---|---|---|
| Hindi support agent, latency-critical | **Flash v2.5** | 75ms inference, Hindi quality is 9/10 |
| Bengali agent, content-heavy | **Multilingual v2** | Better prosody compensates for accent inconsistency |
| Pan-India sales (multi-language) | **Flash v2.5** | Best latency across 32 languages |
| Brand-voice IVR in Hindi | **Multilingual v2** + PVC | Prosody + brand consistency, latency is a non-issue for IVR |
| Voice notes / audio content (not realtime) | **Eleven v3** | Best emotional range, not for Agents Platform |

---

---

## Indian voice selection guide

The ElevenLabs voice library has 50+ Indian voices (premade and community-shared). They sound very different — the most common mistake is picking by name instead of by use case. Below is a curated map from the official library, grouped by what they're actually good at.

### Customer care / support / IVR

| Voice | Voice ID | Strength |
|---|---|---|
| **Vikram S** | [`SPnt7u3Gb2UpfIV1to5x`](https://elevenlabs.io/app/voice-library?voiceId=SPnt7u3Gb2UpfIV1to5x) | Calm, mature, professional. Handles banking/fintech jargon cleanly. The "trust" voice. |
| **Krishna** (sympathetic & natural) | [`XopCoWNooN3d7LfWZyX5`](https://elevenlabs.io/app/voice-library?voiceId=XopCoWNooN3d7LfWZyX5) | Courteous, professional Indian male. Reassuring — banking, telecom, ecommerce, fintech. |
| **Anika** (warm insurance renewals) | [`vmwrgeTJMqZfQXBxzjuW`](https://elevenlabs.io/app/voice-library?voiceId=vmwrgeTJMqZfQXBxzjuW) | One of the highest-volume library voices (5B+ chars). Insurance-tuned. |
| **Amit Gupta** (upbeat, clear, helpful) | [`WuePGPKIAIKI8COZpzce`](https://elevenlabs.io/app/voice-library?voiceId=WuePGPKIAIKI8COZpzce) | Bright Hindi energy, fast pace. High-traffic IVRs, app support. |
| **Ranga** (trustworthy & professional) | [`pzT3Axu7WJzqmpRAWYc5`](https://elevenlabs.io/app/voice-library?voiceId=pzT3Axu7WJzqmpRAWYc5) | Mature, calm, empathetic. BFSI escalations, senior helpdesks. |
| **Raju** (insurance agent) | [`Jf701ovNUg1ZFQugpfXU`](https://elevenlabs.io/app/voice-library?voiceId=Jf701ovNUg1ZFQugpfXU) | Conversational, natural-feeling. Battle-tested for chatbots. |
| **Riya Rao** (number-perfect support) | [`hLvRzHEBXR9scnhmrX9E`](https://elevenlabs.io/app/voice-library?voiceId=hLvRzHEBXR9scnhmrX9E) | Female counterpart to Vikram S. IVR-tuned, WhatsApp Flows, banking. |

### Sales / collections / outbound

| Voice | Voice ID | Strength |
|---|---|---|
| **Kanika** (calm & commanding) | [`K2Byg54sHB1oHegvENtI`](https://elevenlabs.io/app/voice-library?voiceId=K2Byg54sHB1oHegvENtI) | Authoritative, steady — recovery / collections specialist. EMI reminders, overdue follow-ups, fintech recovery. |
| **Shanaya** (soft collections / Hinglish) | [`tW86gkLZCsTL5jRrTBBw`](https://elevenlabs.io/app/voice-library?voiceId=tW86gkLZCsTL5jRrTBBw) | Sweet, makes feedback feel like conversation. Post-call NPS surveys, customer experience research. |
| **Sia** (confident, clear, helpful) | [`XwkIUwRxNu9PpezCu4Vg`](https://elevenlabs.io/app/voice-library?voiceId=XwkIUwRxNu9PpezCu4Vg) | Smart assistant tone, 700M+ chars. AI assistants, smart-home, virtual concierge. |
| **Bunty** (smart friendly assistant) | [`ibbx9zDYGvLgtYzRbqqG`](https://elevenlabs.io/app/voice-library?voiceId=ibbx9zDYGvLgtYzRbqqG) | Hinglish, friendly, low-friction. Task reminders, scheduling, casual AI assistants. |

### Conversational / companion / chat

| Voice | Voice ID | Strength |
|---|---|---|
| **Tara** (girlfriend, romantic) | [`RDWdsTU6N02BFftbIEAp`](https://elevenlabs.io/app/voice-library?voiceId=RDWdsTU6N02BFftbIEAp) | Sweet, flirty, romantic-companion. Girlfriend-style AI, intimate chat apps. |
| **Priyanka Sogam** (soft & romantic) | [`1zUSi8LeHs9M2mV8X6YS`](https://elevenlabs.io/app/voice-library?voiceId=1zUSi8LeHs9M2mV8X6YS) | Soft, velvety, luxury-brand tone. Romantic audiobooks, premium concierge, Replika-style apps. |
| **Vinayak** (friendly Marathi) | [`rXW8MF4nX2gHMvBmCDnr`](https://elevenlabs.io/app/voice-library?voiceId=rXW8MF4nX2gHMvBmCDnr) | Warm regional voice. Marathi customer care, regional consumer brands. |
| **Prajakta** (natural Marathi companion) | [`4QmRQP2RqsuTD7HT9MkW`](https://elevenlabs.io/app/voice-library?voiceId=4QmRQP2RqsuTD7HT9MkW) | Cultural warmth, regional emotional intelligence. Marathi companion / virtual friend apps. |

### Hindi narration / storytelling (NOT realtime — for content)

These voices are designed for audiobook / podcast / video — they typically pair with **Multilingual v2** (higher prosody, higher latency) rather than Flash v2.5. **Avoid for phone agents** unless quality is the only thing that matters.

| Voice | Voice ID | Strength |
|---|---|---|
| Krishna (energetic & expressive) | [`m5qndnI7u4OAdXhH0Mr5`](https://elevenlabs.io/app/voice-library?voiceId=m5qndnI7u4OAdXhH0Mr5) | Actor's range, 360° voice presence. Narration, audiobook. |
| Viraj (intimidating & suspenseful) | [`K24eC7JpUgk8zMtQYrpV`](https://elevenlabs.io/app/voice-library?voiceId=K24eC7JpUgk8zMtQYrpV) | Crime/suspense narrator. Thrillers, mystery, horror. |
| Taksh (calm, serious, smooth) | [`qDuRKMlYmrm8trt5QyBn`](https://elevenlabs.io/app/voice-library?voiceId=qDuRKMlYmrm8trt5QyBn) | Mythology, philosophical depth. Epic narration, Mahabharata, devotional. |
| Samisha (deep, soft, seductive) | [`vzov6y10x6nsGNFg883S`](https://elevenlabs.io/app/voice-library?voiceId=vzov6y10x6nsGNFg883S) | Late-night thriller voice. Audio thrillers, dark fiction. |
| Vayu (clear, calm, intimidating) | [`Mbwx1ZAXuMdYGtJRjvvQ`](https://elevenlabs.io/app/voice-library?voiceId=Mbwx1ZAXuMdYGtJRjvvQ) | Dramatic dubbing voice. YouTube dramas, dubbing, cinematic. |
| Monika Sogam (breathy & suspenseful) | [`VZyYADHcMi33m0wO9zD1`](https://elevenlabs.io/app/voice-library?voiceId=VZyYADHcMi33m0wO9zD1) | 900M+ chars, suspense specialist. Crime podcasts, thrillers. |

### Picking the right voice — quick rules

1. **For phone agents: pick from the "Customer care" or "Sales" group above.** Avoid narration-tuned voices — they read beautifully but feel slow / theatrical on a real call.
2. **Match register to use case.** A breathy thriller voice on a banking IVR is jarring. A clinical IVR voice on a romance-companion app feels dead. The library is huge specifically because these aren't interchangeable.
3. **Use Multilingual v2 with these voices for Hindi content** (audiobook, narration). Use **Flash v2.5** for phone agents, even if Multilingual v2's prosody is slightly better — the latency penalty makes Multilingual v2 a worse on-call experience.
4. **Listen on phone audio (8 kHz µ-law), not your laptop speakers.** A voice that sounds rich in your headphones may sound muddy after the PSTN downsampling. The recordings in [`/benchmarks/recordings`](../benchmarks/recordings/INDEX.md) are PSTN-quality — use them as the realistic preview.
5. **Track the voiceId per use case** so you can swap voices without changing other config.

To find more voices, browse [Voice Library](https://elevenlabs.io/docs/eleven-creative/voices/voice-library) — filter by language + gender + use case.

---

## Sources of truth

- [ElevenLabs India landing](https://elevenlabs.io/india)
- [Indian-accent TTS](https://elevenlabs.io/text-to-speech/indian-accent)
- [Hindi STT](https://elevenlabs.io/speech-to-text/hindi)
- [Supported languages (Help Center)](https://help.elevenlabs.io/hc/en-us/articles/13313366263441)
- [Models reference](https://elevenlabs.io/docs/overview/models)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*