# Production Best Practices

What separates a demo from a deployed agent. Latency, reliability, observability, compliance.

---

## Latency budget

| Range | What happens |
|---|---|
| **200–500 ms** | Natural turn-taking. Users perceive this as conversational. |
| **500–1000 ms** | Tolerable. Users wait but feel friction. |
| **> 1000 ms glass-to-glass** | **Hard ceiling.** Users start interrupting because they assume the AI didn't hear them. Conversation quality collapses. |

That 1000ms ceiling is the single most important number in this playbook. Architect every component to fit under it.

A typical breakdown under budget:
- STT (Scribe v2 Realtime): ~150ms
- LLM first token: 200–500ms (depends on model + prompt size)
- TTS first chunk (Flash v2.5): ~75ms
- Telephony + network: 150–250ms
- **Total: 575–975ms** — just inside budget if everything goes right

Swap Flash v2.5 → Multilingual v2 (~1,200 ms TTS leg in measured production calls) and you blow the budget on TTS alone.

---

## Voice type for latency

```
Default voices > Synthetic > Instant Voice Clone > Professional Voice Clone
   fastest                                                 slowest
```

PVC has real per-generation overhead. **Pick IVC over PVC for phone agents** unless brand voice is non-negotiable. See [`/getting-started`](../getting-started/README.md) for the full breakdown.

---

## Streaming + persistent HTTPS

The TCP handshake to ElevenLabs takes **~375ms** on a new connection. That overhead **only hits new connections** — reuse the connection across turns in a session.

- Use HTTP/2 or HTTP/1.1 keep-alive
- Prefer the WebSocket streaming endpoint for sustained sessions
- Pool connections at your backend if you're proxying through it

---

## Geographic routing

ElevenLabs runs clusters in **USA, Netherlands, Singapore, India**. Nearest-cluster routing is automatic, but only as good as where your trunk lands.

- Indian agents → land on the India cluster (Vobiz handles this naturally; Twilio routes via US by default — measure!)
- EU agents → Netherlands
- US agents → US

A misrouted call adds 100–200ms of unnecessary round-trip per turn.

---

## Interruption + silence handling

**Interruption ON (default):** user can talk over the agent. Critical for natural conversation. The agent should detect the interruption and stop speaking within ~200ms.

**Silence handling:** define an inactivity policy in the prompt or workflow:
- Short silence (1–3s): natural pause, do nothing
- Medium silence (3–8s): "Are you still there?"
- Long silence (8–15s): "I'll end the call if I don't hear anything"
- Very long (> 15s): hang up via system tool

Also enables the **95% silence discount** for periods > 10s (see [`/cost-analysis`](../cost-analysis/README.md)).

---

## Observability — what to log

Every production agent needs three streams:

| Stream | Source | What it tells you |
|---|---|---|
| **Post-call webhooks** | ElevenLabs → your endpoint | Full transcript, tool calls, duration, cost, model used |
| **SIP/RTP metrics** | Your trunk provider's API | Jitter, packet loss, codec used, call setup time |
| **App-level metrics** | Your backend logs | Webhook RTTs, tool success rates, downstream API latencies |

**Per-call dashboards** to build:
- Glass-to-glass latency p50/p95/p99 (estimate from transcript turn timestamps)
- Tool call success rate per tool
- LLM token usage per call
- Hang-up reason (user / agent / dropped / timeout)
- Language detected vs language set
- Transfer rate (how often the agent escalates to human)

---

## Failure modes you'll hit

| Failure | Symptom | Fix |
|---|---|---|
| **Dropped RTP packets** | Audio glitches, choppy responses | Codec downgrade (G.711 over Opus), jitter buffer tuning at trunk |
| **Codec mismatch** | One side can't decode audio | Force a common codec on the trunk (G.711 µ-law is the safe default) |
| **Agent hallucinating tool args** | Webhook 400/422 errors | Tighten tool argument schema, add examples in the prompt, lower temperature |
| **LLM timeout / slow first token** | Long awkward silence | Add filler line ("Let me check…"), use faster LLM for routine intents, parallelize tool calls |
| **PSTN one-way audio** | Caller can hear agent but not vice versa (or reverse) | NAT/firewall issue on RTP ports (10000–20000 UDP), pinhole rules |
| **Misrouted region** | Higher than expected latency | Check which ElevenLabs cluster the trunk is landing on; pin or change provider |
| **Prompt injection from caller** | Agent does something unexpected ("transfer me to a manager named Bob") | Use `trust_context: low_trust`, sanitize tool args, restrict system tool access |
| **Multilingual drift mid-call** | Voice quality drops on language switch | Switch TTS model (Flash → Multilingual v2), tighten language-switch prompt instruction |

---

## Compliance

- **Zero Retention Mode** and **HIPAA-compliant deployments** do not support custom MCP servers ([source](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp))
- For PCI-scope (taking card numbers), use [`play_dtmf`](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/transfer-to-human) for keypad-only entry and route the audio out of scope
- For India: DPDP compliance handled by Vobiz at the trunk layer; your agent still needs explicit consent recording for data collection
- TLS + SRTP transport on the trunk is non-negotiable for production

---

## Pre-launch checklist

- [ ] Tested in dashboard, then on a real phone, then from 3+ networks (wifi, 4G, landline)
- [ ] Measured glass-to-glass latency on real calls, p95 < 1000ms
- [ ] Post-call webhook landing in your log system, alerts on failures
- [ ] Tool call timeouts + retries configured at your backend
- [ ] Transfer-to-human path tested end-to-end
- [ ] Silence + hangup policy defined and tested
- [ ] System prompt reviewed by 2+ people, run through eval suite
- [ ] `trust_context` set to `low_trust` for external-facing agents
- [ ] Cost forecast at expected volume (see [`/cost-analysis`](../cost-analysis/README.md))
- [ ] Recording + consent flow per local regulation
- [ ] On-call runbook for "agent is broken / loud / silent in production"

---

## Sources of truth

- [Latency optimization](https://elevenlabs.io/docs/eleven-api/guides/how-to/best-practices/latency-optimization)
- [Prompting guide](https://elevenlabs.io/docs/eleven-agents/best-practices/prompting-guide)
- [Conversation flow](https://elevenlabs.io/docs/eleven-agents/customization/conversation-flow)
- [MCP compliance constraints](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*