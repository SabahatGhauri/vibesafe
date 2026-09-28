# Game Narrator — Project Plan (upcoming)

**Status:** Planning only, nothing built yet.
**Goal:** A local system that plays a game, records the gameplay, and adds voice narration from a script, producing a finished video.

---

## 1. Inputs and outputs

- **Input:** a game (browser, desktop or emulator) plus a script file with scenes. Each scene has a goal for the agent and the lines the narrator says.
- **Output:** `final.mp4` with the gameplay, narration synced to on-screen events, subtitles, and game audio ducked under the voice.

## 2. Architecture

```
script.yaml ──► Orchestrator (Python)
                  │
     ┌────────────┼──────────────┬──────────────────┐
     ▼            ▼              ▼                  ▼
 Game Player   Recorder      Event Logger      TTS Engine
 (agent/bot)   (FFmpeg/OBS)  (timestamps)      (per-line WAV)
     └────────────┴──────┬───────┴──────────────────┘
                         ▼
                 Timeline Builder  ──►  Assembler (FFmpeg)  ──►  final.mp4 + .srt
```

## 3. Components

### A. Script format (`script.yaml`)

```yaml
game: { type: browser, url: "http://localhost:8080" }
voice: { engine: piper, model: en_US-lessac-medium }
scenes:
  - id: intro
    narration: "Welcome! Today we're taking on level one."
    cue: start                 # when to speak
  - id: first_jump
    goal: "Jump over the first gap"
    narration: "Here comes the first gap. Timing is everything."
    cue: before_action         # speak before the agent acts
  - id: win
    goal: "Reach the flag"
    narration: "And that's the level cleared!"
    cue: on_event:level_complete
```

`goal` is what the agent tries to do, `narration` is what gets spoken, `cue` says when the line plays.

### B. Game player

A shared `Player` interface (`step()`, `observe()`, `emit_event()`) with one backend per game type:

| Game type | Approach |
|---|---|
| Browser game | Playwright drives the page and takes screenshots; a vision LLM (Claude computer use or a local model) picks actions. |
| Desktop game | PyAutoGUI or `xdotool` for input, `mss` for screenshots, same vision LLM loop. |
| Retro / RL game | Gymnasium or `stable-retro` with a trained policy; `RecordVideo` gives frames for free. |
| Deterministic demo | Scripted input macros, no AI. Most reliable for polished videos. |

### C. Recorder

- **Default:** FFmpeg subprocess (`x11grab` Linux, `gdigrab` Windows, `avfoundation` macOS) at a fixed 30 fps; game audio from a loopback device to a separate track.
- **Alternative:** OBS controlled via `obs-websocket` (better quality, scenes, single-window capture).
- MCP screen recorders (e.g. `screen-recorder-mcp`) could also work but are unverified; FFmpeg/OBS directly means one less dependency.

### D. Event logger (key to sync)

- Log `t0` when recording starts.
- Every scene start, action and game event → `{t: seconds_since_t0, scene_id, event}` in `events.jsonl`.
- Narration aligns to these real timestamps, not guessed times.

### E. Voice (TTS), all local

- **Piper:** fast, CPU, good default.
- **Kokoro:** very natural, still light.
- **XTTS-v2 (Coqui):** voice cloning from ~6 s of audio; needs a GPU to be quick. Non-commercial model license.

Render one WAV per scene before gameplay and record durations, so the agent can wait if a line is longer than its action.

### F. Timeline builder

- Map each `cue` to a timestamp from `events.jsonl` (e.g. `before_action` = event time minus a small lead).
- Resolve overlaps: push lines back, or pause the agent in live mode.
- Write `.srt` subtitles from the same timeline.

### G. Assembler (FFmpeg `filter_complex`)

- Place each WAV with `adelay`, mix with `amix`.
- Duck game audio under voice with `sidechaincompress`.
- Optional: burned-in subtitles, intro/outro cards, background music.
- Export H.264/AAC MP4; optional 9:16 crop for Shorts/TikTok.

## 4. Modes

1. **Script-first (build first):** the script drives gameplay; narration pinned to agent-emitted events.
2. **Play-first commentary (later):** agent plays freely; an LLM writes narration from `events.jsonl` + keyframes; then TTS and assembly.

## 5. Build phases

| Phase | Deliverable | Done when |
|---|---|---|
| 1 | FFmpeg screen recording + event logger | MP4 and timestamped `events.jsonl` |
| 2 | TTS per script line (Piper) | WAVs and their durations |
| 3 | Timeline builder + FFmpeg assembler | Narration lands on the right moments in a test clip |
| 4 | Scripted-macro game player | Full script → video run with no AI |
| 5 | AI player (Playwright + vision LLM) | Agent completes scene goals and emits cues |
| 6 | Polish | Ducking, subtitles, music, voice cloning, vertical export |
| 7 (optional) | Wrap as MCP tools | `start_recording`, `play_scene`, `render_video` callable from Claude Desktop |

## 6. Stack and layout

- Python 3.11+, Playwright, PyAutoGUI, `mss`, FFmpeg (or OBS + `obsws-python`), Piper/Kokoro/XTTS-v2, MoviePy for prototyping, YAML + Pydantic for config.

```
game-narrator/
  script.yaml
  narrator/{orchestrator,player,recorder,events,tts,timeline,assemble}.py
  out/<run_id>/{raw.mp4, game.wav, events.jsonl, voice/*.wav, subs.srt, final.mp4}
```

## 7. Risks

- **Slow LLM agents (~1–3 s/action):** speed up idle stretches in editing or pause recording between actions; use macros/RL for real-time action games.
- **Timing drift:** one clock (`time.monotonic()`) for recorder and events; re-check against the first frame.
- **Narration longer than action:** use pre-rendered durations to hold the agent or push lines later.
- **Performance:** run TTS before gameplay; hardware encoding (`h264_nvenc` / `videotoolbox`).
- **Game ToS:** only automate games you own or that allow bots; no online multiplayer.

---

## 8. Cost estimate

**Everything except the AI player is free.** Running cost is roughly $0–10 per 10-minute video depending on the player; the only possible one-time cost is a GPU for voice cloning.

### One-time

| Item | Cost | Notes |
|---|---|---|
| FFmpeg, OBS, Playwright, PyAutoGUI, Python | $0 | Open source |
| Piper / Kokoro TTS | $0 | Kokoro is Apache 2.0; check each Piper voice's license |
| XTTS-v2 | $0 personal use | Non-commercial license; for monetized videos use Kokoro/Piper or a paid TTS |
| Hardware | $0 with an existing decent PC | Piper/Kokoro run on CPU |
| Optional GPU for fast XTTS | ~$250–400 | Used 12 GB card; rough market guess |
| Build time | Your time | ~2–4 weekends for phases 1–6 |

### Per video (AI player)

| Game player | Cost per 10-min video |
|---|---|
| Scripted macros | $0 |
| RL policy | $0 (plus training compute if self-trained) |
| Local vision model (e.g. Ollama) | $0 API; needs strong GPU, plays worse |
| Claude vision agent | ~$2–9 per run |

Claude estimate assumes ~300 steps per 10-min video; each step ≈ 1 screenshot (~1,500 tokens) + prompt/history (~3,500 tokens) in, ~500 tokens out.

| Model | Price per 1M tokens (in / out) | Per step | Per video |
|---|---|---|---|
| Haiku 4.5 | $1 / $5 | ~$0.0075 | ~$2.25 |
| Sonnet 5 | $2 / $10 | ~$0.015 | ~$4.50 |
| Opus 5.5 | $4 / $20 | ~$0.03 | ~$9 |

- Plan on 2–3 attempts per good take → realistically $5–25 per finished video on Sonnet 5.
- Prompt caching of the system prompt/instructions cuts input cost.
- Claude writing the script/commentary: under $0.10 per video.
- Prices are Anthropic list prices as of mid-2026; per-step numbers are estimates, not measurements. Re-check before budgeting.

### Setups

- **Cheapest ($0/video):** macros or RL player, Piper/Kokoro, FFmpeg, existing PC.
- **Balanced (~$5–15/video):** Sonnet 5 player, Kokoro voice, no new hardware.
- **Premium (~$300 once + $10–25/video):** Opus 5.5 player, XTTS on a GPU (personal use) or paid commercial TTS for monetized videos.

**Recommended start:** phases 1–4 with scripted input ($0, proves the pipeline), then add a Claude player on Haiku/Sonnet and measure real token use before scaling.

---

## 9. Minecraft track (first target)

The script drives the character directly through a bot, not by clicking on screenshots.

```
Script (plain English) ──► LLM turns each step into bot actions ──► Mineflayer bot acts in the world
        │                                                                  │
        └──► narration ──► TTS ──────────────► merged at the end ◄─────────┘ recorded video
```

- **Mineflayer** (Node.js, Minecraft Java Edition): joins the world as a player; walk, pathfind, mine, craft, build, fight, chat, follow, look.
- **LLM (e.g. Claude)** turns a step like "chop a tree and build a small hut" into bot calls (`goto`, `dig`, `craft`, `place`).
- **Server commands** set up scenes deterministically: `/time set night`, `/weather rain`, `/tp`, `/summon zombie`.
- Build on existing LLM + Mineflayer projects (Voyager, Mindcraft) instead of from scratch.

### Example script

```yaml
- scene: morning
  setup: ["/time set day", "/tp bot 100 64 200"]
  action: "Walk to the forest and chop 5 oak logs"
  narration: "A new day begins. First job: wood."

- scene: build
  action: "Build a 5x5 wooden hut with a door"
  narration: "Time to build a shelter before night falls."

- scene: night_attack
  setup: ["/time set night", "/summon zombie ~5 ~ ~"]
  action: "Fight the zombie with the sword"
  narration: "And here they come..."
```

### Recording

| Option | Quality | How |
|---|---|---|
| Replay Mod (best) | Cinematic | Record the session, render with smooth camera paths |
| Spectator client + OBS | Good | Your client `/spectate`s the bot; OBS records |
| prismarine-viewer | Basic | Bot's view in a browser; simplified look |

### Limits

- Good at clear tasks (go, mine, build, fight, follow, chat); complex builds are more reliable from a schematic (WorldEdit) than a vague description.
- No real "acting"; use camera angles and narration for drama.
- Steps can fail (falls, getting lost): retry the scene or re-teleport.
- Java Edition only, on your own local server/world, not public servers.
- Cost: roughly $0.50–3 per video on Sonnet 5 (estimate; no screenshots sent), $0 for scenes written as fixed commands.

### Day-one checklist

1. Minecraft Java Edition installed and a local server (Paper or vanilla) running in offline mode.
2. Node.js 18+ and Python 3.11+, FFmpeg, OBS.
3. Replay Mod installed in the client (with Fabric).
4. A first 3-scene script (like the example above).
5. First milestone: bot runs the 3 scenes from fixed commands, recorded, with Piper narration merged into one MP4.
