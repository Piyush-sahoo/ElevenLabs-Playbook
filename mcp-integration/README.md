# MCP Integration — Official ElevenLabs MCP

There are two distinct meanings of "MCP" in the ElevenLabs world. Be precise about which one you're talking about:

| Sense | What it is | Where it lives |
|---|---|---|
| **MCP servers as agent tools** | An agent at runtime calls tools exposed by an MCP server during a phone call | [ElevenLabs MCP tool docs](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp) |
| **The official ElevenLabs MCP server** | An MCP server that gives **you** (the developer) control over your ElevenLabs account from inside Claude/Cursor/Windsurf | [`github.com/elevenlabs/elevenlabs-mcp`](https://github.com/elevenlabs/elevenlabs-mcp) |

**This section is about the second one — ElevenLabs as an ops MCP for the developer.** It's the lowest-friction way to manage voices, agents, and outbound calls without leaving your editor.

For the first sense (MCP tools the agent uses at runtime), see [`/tools-and-workflows`](../tools-and-workflows/README.md).

---

## What this MCP unlocks

Once installed, you can prompt Claude Code / Cursor / Windsurf with things like:

- "Clone the voice in `/audio/sample.wav` and call it `support-v2`"
- "List my agents and which voice each uses"
- "Generate a 30-second sample of agent `agent_abc123` saying [text]"
- "Trigger an outbound call from agent `agent_abc123` to `+919876543210`"
- "What was the last conversation on agent X? Summarize the transcript."

It's everything the ElevenLabs dashboard does, available as natural language inside your editor. For voice-AI engineering workflows, this is a real productivity unlock — you stop tab-switching to the dashboard for routine ops.

---

## Install

Two paths:

```bash
# Option 1 — via PyPI
pip install elevenlabs-mcp

# Option 2 — clone the official repo
git clone https://github.com/elevenlabs/elevenlabs-mcp
```

One environment variable:

```bash
export ELEVENLABS_API_KEY=sk_...
```

Free tier gives 10k credits/month — enough to test installations and run a few clones.

---

## Wire into Claude Code

Add to your `.mcp.json` (project) or settings (user-level):

```json
{
  "mcpServers": {
    "elevenlabs": {
      "command": "uvx",
      "args": ["elevenlabs-mcp"],
      "env": {
        "ELEVENLABS_API_KEY": "sk_..."
      }
    }
  }
}
```

Restart Claude Code; the MCP tools appear automatically.

Same pattern for Cursor and Windsurf — see the [official repo](https://github.com/elevenlabs/elevenlabs-mcp) for editor-specific instructions.

---

## Useful production workflows

| Workflow | One-prompt version |
|---|---|
| Voice catalog audit | "List all my voices and which agents reference them" |
| Quick voice clone | "Clone `/audio/founder.wav` as IVC, name it `founder-clone`" |
| Sample generation for QA | "Generate a 15-second sample of `founder-clone` saying [test phrase] and save to `/qa/`" |
| Outbound test call | "Trigger an outbound call from `agent_support` to my number `+91...`" |
| Conversation review | "Get the last 10 conversations on agent `agent_support`, summarize hangup reasons" |
| Agent diff | "What changed in agent `agent_support` config in the last 7 days?" |

---

## Security & approval modes

ElevenLabs supports three approval modes for MCP tool use (configured **per agent**, not on the MCP itself):

| Mode | Behavior | Use for |
|---|---|---|
| **Always Ask** (recommended) | Agent requests permission before each tool use | Production, high-stakes |
| **Fine-grained** | Per-tool: auto-approve / require / disabled | Mixed — read-only auto, mutations require |
| **No Approval** | Agent uses any tool freely | Dev/testing only |

For the ops MCP itself, your API key is the security boundary — **don't share it, don't commit it, rotate it periodically**. Use a separate key for the MCP from the keys used by your production agents so you can revoke independently.

### Compliance constraint

MCP servers are **not supported in Zero Retention Mode or HIPAA-compliant deployments**. If your account is in either mode, the agent-runtime MCP feature is unavailable. The ops MCP described here still works (you're hitting the API as yourself), but be aware your usage is logged.

---

## Vobiz MCP — docs search

Vobiz publishes a hosted MCP server scoped to its **documentation** (not the Voice API). Point any MCP-aware editor at it and the assistant can search + fetch any page of the Vobiz docs in-context — useful when wiring up SIP trunks against the Vobiz integration steps.

| Field | Value |
|---|---|
| **Endpoint** | `https://docs.vobiz.ai/mcp` |
| **Transport** | Streamable HTTP |
| **Authentication** | None (public) |
| **Tools exposed** | `search`, `fetch` (under namespace `vobiz-docs`) |
| **Scope** | Documentation only — **not** the Vobiz REST or Partner API |

### One-liner install (auto-detects your MCP client)

```bash
npx add-mcp https://docs.vobiz.ai/mcp
```

### Per-client setup

**Claude Code** (native HTTP):
```bash
claude mcp add --transport http vobiz-docs https://docs.vobiz.ai/mcp
```

**Claude Desktop / Cursor** — add to `claude_desktop_config.json` or `~/.cursor/mcp.json`:
```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://docs.vobiz.ai/mcp"]
}
```

**VS Code 1.99+** — `.vscode/mcp.json` with type `http` and the server URL.

### Example query

> "Using the `vobiz-docs` MCP server, how do I start an audio stream from XML?"

The assistant retrieves the answer from live Vobiz docs instead of training data — so the response is always current.

### What it does NOT do

This MCP gives **docs lookup**, not control over your Vobiz account. To provision DIDs, manage trunks, or pull call records from your editor, you would still build a thin MCP wrapper around the [Vobiz Voice API](https://www.docs.vobiz.ai/).

References:
- [Vobiz MCP docs](https://docs.vobiz.ai/resources/mcp)
- [Vobiz API docs](https://www.docs.vobiz.ai/)
- [Vobiz console](https://console.vobiz.ai/)

---

## What this MCP does NOT replace

| Thing | Lives where |
|---|---|
| **Agent runtime tools** (webhook tools, system tools the agent calls during a call) | Agent config — see [`/tools-and-workflows`](../tools-and-workflows/README.md) |
| **SIP trunk configuration** | Your trunk provider's dashboard (Twilio, Vobiz) |
| **LLM provider keys** | Agent config in ElevenLabs |
| **Webhook backend** | Your own infrastructure |

The ops MCP is for you, the engineer. Don't confuse it with the tools your agent has at runtime — those are separate and configured per-agent.

---

## Sources of truth

- [Official `elevenlabs-mcp` repo](https://github.com/elevenlabs/elevenlabs-mcp)
- [ElevenLabs MCP docs](https://elevenlabs.io/docs/eleven-agents/customization/tools/mcp)
- [MCP launch blog (Claude + Cursor)](https://elevenlabs.io/blog/introducing-elevenlabs-mcp)
- [`mcp-elevenlabs` on PyPI](https://pypi.org/project/mcp-elevenlabs/)

Full index: [`/resources`](../resources/README.md).


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*