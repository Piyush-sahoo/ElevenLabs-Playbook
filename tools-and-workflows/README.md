# Tools & Workflows

How your ElevenLabs agent **does things** beyond just talking. All of this lives in the agent's **Tools** tab in the dashboard.

ElevenLabs exposes 4 tool types ([official overview](https://elevenlabs.io/docs/eleven-agents/customization/tools)):

| Type | What it is |
|---|---|
| **System tools** | Built-in toggles that ship with every agent |
| **Server tools** | HTTPS webhooks you expose from your backend |
| **Client tools** | Functions on the browser / mobile SDK (web agents only) |
| **MCP tools** | External Model Context Protocol servers |

Plus **[Workflows](https://elevenlabs.io/docs/agents-platform/customization/agent-workflows)** for multi-step / branching conversations and **[Tool Call Sounds](https://elevenlabs.io/docs/eleven-agents/customization/tools/tool-configuration/tool-call-sounds)** for ambient audio during tool execution.

---

## System tools — built-in

Toggle on/off per agent in the Tools tab. No code.

| Tool | One-line | Docs |
|---|---|---|
| **End conversation** | Agent hangs up when done | [→](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/end-call) |
| **Detect language** | Mid-call language classification | [→](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/language-detection) |
| **Skip turn** | Agent stays silent for one turn | [→](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/skip-turn) |
| **Update state** | Write key-value data per call | [→](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools) |
| **Transfer to agent** | Hand off to another ElevenLabs agent (with context) | [→](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/agent-transfer) |
| **Transfer to number** | SIP REFER to a real phone number | [→](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/transfer-to-number) |
| **Play keypad touch tone** | DTMF for downstream IVRs | [→](https://elevenlabs.io/docs/eleven-agents/customization/tools/system-tools/play-keypad-touch-tone) |
| **Voicemail detection** | Human vs. answering machine on outbound | [→](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools/voicemail-detection) |

**Recommended defaults for a phone agent:** End conversation + Detect language (if multilingual). Everything else is opt-in.

---

## Server tools — your backend

A function you define in the agent's Tools tab. ElevenLabs calls your HTTPS endpoint when the LLM decides to invoke it.

Typical uses: CRM lookup by phone, KYC, payment status, order tracking, calendar booking, ticket creation.

**Latency budget:** keep handlers under ~500 ms. Anything longer needs a filler line ("Let me check…") in the prompt to mask the wait.

→ [Server tools docs](https://elevenlabs.io/docs/agents-platform/customization/tools/server-tools)

---

## Client tools — frontend only

Run in the browser or mobile SDK hosting the agent. DOM updates, app navigation, frontend state. **Not applicable to phone agents** — there's no frontend on a PSTN call.

→ [Client tools docs](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools)

---

## MCP tools — external surface

Bring an external Model Context Protocol server into the agent at runtime. The MCP server exposes a tool surface (potentially hundreds of tools), and the agent can call any of them.

Common picks: **Zapier MCP** (7,000+ apps via one integration), or your own custom MCP if your internal platform has many APIs.

**Approval modes:** Always Ask (recommended), Fine-grained (per-tool), No Approval (dev only).

**Compliance:** MCP is not supported in Zero Retention Mode or HIPAA deployments.

→ [MCP docs](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp)

---

## Workflows — branching the conversation

Visual graph editor for multi-step / multi-intent conversations. Each node has its own prompt, voice, tools, and LLM.

Use a workflow when:
- Multiple intents land on the same DID (support + sales + KYC)
- The prompt is becoming `IF this THEN that` spaghetti
- Different stages need different personas / voices

Use a single agent when the flow is short (< 5 turns) and single-intent.

→ [Workflows docs](https://elevenlabs.io/docs/agents-platform/customization/agent-workflows)

---

## Trust context

Agent-level setting: `low_trust` (external callers — restricted tool access, output vetting) vs. `high_trust` (internal users — full access).

**Default to `low_trust` for any customer-facing agent.** It's the guardrail against prompt injection from callers.

---

## Post-call webhook

When a call ends, ElevenLabs POSTs the full transcript + tool calls + per-leg metrics + structured state to your endpoint. Wire it into your log system on day one — it's the primary observability signal. See [`/production-best-practices`](../production-best-practices/README.md#observability).

---

## Sources of truth

- [Tools overview](https://elevenlabs.io/docs/agents-platform/customization/tools)
- [System tools](https://elevenlabs.io/docs/agents-platform/customization/tools/system-tools)
- [Server tools](https://elevenlabs.io/docs/agents-platform/customization/tools/server-tools)
- [Client tools](https://elevenlabs.io/docs/eleven-agents/customization/tools/client-tools)
- [MCP tools](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp)
- [Workflows](https://elevenlabs.io/docs/agents-platform/customization/agent-workflows)
- [Tool Call Sounds](https://elevenlabs.io/docs/eleven-agents/customization/tools/tool-configuration/tool-call-sounds)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*