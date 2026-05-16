# Cost Analysis

## What does an end-to-end voice agent actually cost?

A production phone agent has three line items. Rough per-minute ranges:

| Line item | Typical range | Who bills you |
|---|---|---|
| **ElevenLabs Agents Platform** (TTS + STT + orchestration) | **$0.08 – $0.12 / min** | ElevenLabs |
| **LLM tokens** (passed through) | **$0.001 – $0.05 / min** depending on model | OpenAI / Anthropic / Google directly |
| **Telephony** (SIP trunk per-minute) | **$0.005 – $0.05 / min** depending on region and provider | Your trunk provider (Vobiz / Twilio) |
| **Total all-in** | **~$0.09 – $0.22 / min** | — |

**Typical configurations:**

| Scenario | All-in $/min | Driver |
|---|---|---|
| India inbound, Flash v2.5, gpt-4o-mini, Vobiz | **~$0.09 – $0.10** | Cheapest realistic stack |
| US inbound, Flash v2.5, gpt-4o-mini, Twilio | **~$0.10 – $0.12** | Telephony adds a bit |
| India multilingual, Multilingual v2, Claude Sonnet, Vobiz | **~$0.15 – $0.18** | Pricier TTS + LLM |
| Enterprise tier with negotiated discounts | **~$0.06 – $0.10** | Volume contract |

So: **a typical Indian-market phone agent runs around 8 to 10 cents per minute all-in.** A premium / Sonnet-driven multilingual agent runs 15 to 18 cents. Everything else is just deciding where on that band you sit.

---

## ElevenLabs has two billing models

ElevenLabs voice has **two billing models**. Pick the one that matches how you ship.

| Billing model | Use when |
|---|---|
| **TTS standalone (per-character)** | You're calling the TTS API yourself from your own backend / orchestrator |
| **ElevenLabs Agents Platform (per-minute)** | You're using ElevenLabs' end-to-end Agents Platform — STT, LLM routing, TTS, and telephony are bundled |

---

## TTS standalone — per-model character rate

The TTS API is billed in **credits per character**. Different TTS models burn credits at different rates:

| Model | Credit rate per character | Relative cost |
|---|---|---|
| **Flash v2** | 0.5 | 1× (baseline) |
| **Flash v2.5** | 0.5 | 1× |
| **Turbo v2** | 0.5 | 1× |
| **Turbo v2.5** | 0.5 | 1× |
| **Multilingual v2** | 1.0 | 2× |
| **Eleven v3** | 1.0 (alpha pricing) | 2× |

Credits convert to dollars based on your plan tier (see [official API pricing](https://elevenlabs.io/pricing/api)).

**Rough per-minute conversion** (phone-speech rate ≈ 750 characters per minute):

| Model | Characters/min | Credits/min | $/min (Creator tier, illustrative) |
|---|---|---|---|
| Flash v2.5 / Turbo v2.5 | ~750 | ~375 | ~$0.08 |
| Multilingual v2 | ~750 | ~750 | ~$0.17 |

Numbers are illustrative — confirm against your plan's per-credit rate.

---

## ElevenLabs Agents Platform — per-minute orchestration

The Agents Platform bundles TTS + STT + agent orchestration into a single per-minute price. LLM tokens are passed through (you pay your LLM provider directly). Telephony (SIP trunk) is billed by your trunk provider separately.

---

## Telephony pricing — India

For India deployments, **[Vobiz](https://www.vobiz.ai/) lands around ₹0.45 / minute (~$0.005) — or lower at scale.** That makes telephony the smallest line item in the stack; confirm exact rates with the provider for your contract size.

| Tier | Price per minute |
|---|---|
| Pay-as-you-go | **$0.10** |
| Business | **$0.08** |
| Premium | **$0.12** |

**Silence discount:** 95 % off for any silence period longer than 10 seconds (useful for IVR hold-music flows; not meaningful for normal conversation).

**Billing basis:** conversation duration, not compute time. A silent caller on hold still accrues cost (at the discounted rate after 10 s).

For current tier limits and overage rates, see the [Agents cost article](https://help.elevenlabs.io/hc/en-us/articles/29298065878929).

---

## Sources of truth

- [API pricing](https://elevenlabs.io/pricing/api)
- [Plans / pricing](https://elevenlabs.io/pricing)
- [Agents cost (Help Center)](https://help.elevenlabs.io/hc/en-us/articles/29298065878929)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*