# Prompt Patterns

System prompts are the personality + policy blueprint of an ElevenLabs agent. The structure of the prompt has a measurable effect on reliability — the principles below come from ElevenLabs' [official prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide); the examples in [`/prompts`](./prompts/) are original.

---

## What the system prompt does (and doesn't)

| The system prompt **controls** | The system prompt **does NOT control** |
|---|---|
| Personality, role, voice tone, response style | Turn-taking mechanics (handled by the platform's endpointing config) |
| Goals, workflow steps, escalation criteria | Which language the agent can speak (set on the agent itself) |
| Tool-use logic (when/how to call which tool) | Voice model / voice ID (set on the agent itself) |
| Guardrails — non-negotiable rules | LLM model, temperature, max tokens (set on the agent itself) |

So: structural decisions go on the agent. **Behavioral decisions go in the prompt.**

---

## The 7-section template

ElevenLabs' production prompts cluster around these sections. Use markdown headings — models pay extra attention to them, especially `# Guardrails`:

```
# Personality
Who the agent is. Role + 2–3 character traits.

# Environment
Where the conversation happens (phone, in-app, etc.) and any contextual cues
(angry caller? after-hours? returning customer?).

# Tone
Length cap, register, style of pauses, when to use fillers. Be concrete.

# Goal
Numbered workflow. Each step = one action. Mark critical steps with
"This step is important."

# Guardrails
Non-negotiable rules. Models pay extra attention to this heading.
Repeat the 1–2 most important rules.

# Tools (only if the agent has tools)
Per tool: WHEN to use, HOW to use (parameter format, ordering),
ERROR handling.

# Error handling
What to say + do when a tool fails or you don't know the answer.
Always: never guess; offer a retry or escalation.
```

---

## The 7 reliability principles (with the *why*)

1. **Separate instructions into sections** — clear boundaries prevent rules from one context bleeding into another. Models specifically prioritize `# Guardrails`.
2. **Be as concise as possible** — every unnecessary word is a potential misinterpretation. Strip filler. One action per line.
3. **Emphasize critical instructions** — append "**This step is important.**" to the 1–2 lines that absolutely cannot be missed. Repeating the same rule twice (in `# Goal` and again in `# Guardrails`) is also fine.
4. **Text normalization for TTS** — numbers and symbols cause TTS hallucinations. Write `"$1,420"` as `"one thousand four hundred and twenty rupees"`, dates as `"the twentieth of April"`. Or set the agent's `text_normalisation_type` to `elevenlabs` (slight latency cost; keeps transcripts clean).
5. **Dedicated `# Guardrails` section** — even if rules are also mentioned in `# Goal`. The heading itself signals priority to the model.
6. **Tool parameter descriptions must specify format** — STT and TTS-normalization can leave you with `"john at gmail dot com"` in context; the tool needs `"john@gmail.com"`. Always describe the expected format with an example.
7. **Explicit error handling** — never let the agent guess when a tool fails. Tell it: acknowledge → retry once → escalate.

---

## Anti-patterns (don't do these in phone-agent prompts)

- ❌ Long preambles: _"Hello! Thank you for calling. I am your AI assistant powered by…"_
- ❌ `IF this THEN that` trees in the prompt → use **Workflows** instead
- ❌ Tool-use instructions buried in paragraph 5 — put them where the LLM sees them on every turn
- ❌ Asking for the same info twice — store + reference what was already captured (use `update_state` system tool)
- ❌ Apologizing repeatedly — fillers should be neutral, not penitent
- ❌ Prompts > 2,000 tokens for a single intent — split into specialist agents via Workflows

---

## Use cases (original prompts in `/prompts`)

Each `.txt` is a complete production-ready prompt for a distinct scenario. **None are copies** of ElevenLabs example agents (Acme / CloudTech / RetailCo) — different businesses, different flows, different edge cases. Treat them as starting points, not templates to ship as-is.

| File | Scenario | Notable |
|---|---|---|
| [`prompts/customer-support-isp.txt`](./prompts/customer-support-isp.txt) | Customer support for **BrightFiber Internet** (ISP) | Diagnostics-first flow; modem-reset path |
| [`prompts/banking-kyc.txt`](./prompts/banking-kyc.txt) | **Yodha Bank** KYC verification | Identity confirm-twice; PAN normalization; fraud escalation |
| [`prompts/outbound-sales-insurance.txt`](./prompts/outbound-sales-insurance.txt) | **Tula Insurance** outbound term-life | Qualifying first; never push; 3-strike disengage |
| [`prompts/appointment-booking-clinic.txt`](./prompts/appointment-booking-clinic.txt) | **Anvaya Dental** appointment booking | Slot proposal pattern; restate-once on confirm |
| [`prompts/hinglish-grocery-support.txt`](./prompts/hinglish-grocery-support.txt) | **ApnaKirana** D2C grocery (Hinglish) | Code-switching; brand-name phonetic guide; rupee text normalization |
| [`prompts/emi-collection.txt`](./prompts/emi-collection.txt) | **Setu Capital** EMI reminder & recovery | Empathetic but firm; never threaten; compliance escalation |

---

## When to split into multiple agents

If your `# Goal` section is becoming a flowchart, split. Use **Workflows** (see [`/tools-and-workflows`](../tools-and-workflows/README.md)) and let an orchestrator route to specialists. Benefits:
- Each specialist has a smaller prompt → faster LLM TTFT (see [`/models-and-latency`](../models-and-latency/README.md))
- Easier to test, debug, version
- Per-domain metrics (billing-resolution rate, scheduling success rate, etc.)

A general-purpose "do everything" agent is harder to maintain and more likely to fail than 3 specialists with clean handoffs.

---

## Sources of truth

- [ElevenLabs prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide) — the reliability principles
- [Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow)
- [Workflows](https://elevenlabs.io/docs/agents-platform/customization/agent-workflows)
- [Guardrails docs](https://elevenlabs.io/docs/eleven-agents/best-practices/guardrails)
- [LLM configuration](https://elevenlabs.io/docs/eleven-agents/customization/llm)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*