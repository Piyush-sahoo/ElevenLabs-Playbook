# Lab call recordings

Real outbound calls to a real phone, 2026-05-16. Each call uses the **same STT + LLM + minimal "latency test" system prompt** — only the **ElevenLabs TTS model** varies. Filename encodes the full stack: `<stt>__<llm>__<tts>.wav`.

These are the audio evidence behind the latency numbers in [`/models-and-latency`](../../models-and-latency/README.md).

## English clean-prompt set

All share: Deepgram nova-3 (en) STT + gpt-4o-mini LLM + ~30-token "latency test" prompt + voiceId `NeDTo4pprKj2ZwuNJceH`.

| Recording | TTS model | TTS leg | Turn total |
|---|---|---:|---:|
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-flash-v2-5.wav` | eleven_flash_v2_5 | **290 ms** | **934 ms** ✅ |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-flash-v2.wav` | eleven_flash_v2 | 319 ms | 965 ms ✅ |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-turbo-v2-5.wav` | eleven_turbo_v2_5 | **291 ms** | **915 ms** ✅ |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-turbo-v2.wav` | eleven_turbo_v2 | 296 ms | 1,405 ms |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-multilingual-v2.wav` | eleven_multilingual_v2 | 578 ms | 1,353 ms |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-english-v1-legacy.wav` | eleven_monolingual_v1 | 969 ms | 1,582 ms ⚠️ |
| `deepgram-nova3__openai-gpt-4o-mini__elevenlabs-v3-experimental.wav` | eleven_v3 | **1,786 ms** | **2,412 ms** ❌ |

## Hindi context

| Recording | Stack | TTS leg | Turn total |
|---|---|---:|---:|
| `deepgram-nova2-hi__openai-gpt-4o-mini__elevenlabs-multilingual-v2-HINDI.wav` | nova-2 (hi) + Multilingual v2 | 684 ms | 1,662 ms |

## How to listen

The audio is mono WAV, 8 kHz µ-law (PSTN quality — exactly what your real users will hear). Open in any player. The agent's first turn says _"Hello, this is a latency test. Please say a few words back to me, then say goodbye."_ — your turn-taking delay listening to the recording is approximately the **turn total** number above.

## Recording source

All recordings are pulled from the call's `recordingUrl` field. The hosting service retains them for 90 days by default.


---

*Built by [Piyush Sahoo](https://www.linkedin.com/in/piyush-s713/) — connect on LinkedIn.*