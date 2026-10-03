# Shadow Block Tales — channel style guide

Read this before making any video for the channel. It is also fed to the app's "Write script with Claude" step.

## What every story delivers
1. **Long video**: 16:9 landscape, 1080p, 3–4 min (`format: landscape`), with .srt subtitles.
2. **YouTube Short** of the same story: vertical 1080×1920, **under 60 s** (`format: vertical`).
3. **Community post**: a 1080×1080 image plus the post text.
4. **Title, description and hashtags** for each, plus a **thumbnail**.
5. Everything goes on the "My Videos" page, with download buttons and copy boxes. Files under 30 MB are also sent in chat; the full 1080p file comes from the app (Make video).

## Tone and story shape
- Minecraft horror / creepypasta, told in first person as real gameplay ("I found…", "I brought it home").
- The arc is a **wholesome, cozy start**, then **slow corruption of the world**, then a **creepy climax** and a **chilling last line**.
- Never claim it's an official game feature. It's a story.

## Voice
- Narrator preset **`gamer`** (voice "A", chosen by the channel owner).
- Short, punchy lines. In Shorts, 1–2 seconds per line.
- The reveal line is shouted in CAPS with `caption_style: big`. The closing/title line is whispered (`vo_style: quiet`).

## Music and sound
- Original music only. If a script names a real song (for example C418's Sweden or Mice on Venus), use an original track with the same mood: `home` (warm piano).
- The music degrades with the story: `home` → `home_stutter` (the disc skips and cuts out) → `warped` (pitched down) → `void` (purple-noise distortion).
- Use a static burst for the scares and at the very end, then hard black.

## Story series so far
- **Glitch** (long video + Short): the faceless white entity you bring home; the world corrupts.
- **Copycats** (Short): villagers mimic you, become hollow-eyed copies of you, and swap places with you ("WHICH ONE IS ME?"). Tools: `skin: steve_hollow`, `fx.chat` (in-game chat lines), blink jump-cuts (`fx.fade` spikes plus position jumps).
- **Seer** (Short, a sequel to Copycats): a hollow-eyed villager whose trades predict your next moves, then offer your head. Tools: `skin: villager_hollow`, `gui: {type: trade, offers: [...]}` (villager trading screen; `head:` for player heads, `sold: true` for a red X), and `highlight: [[t, index], ...]` stepping through the offers.
- **Music Box** (music Short, no narration): an original creepy lullaby (`music: music_box`, 90 bpm) with beat-synced cuts to all the monsters (Glitch, the Copycats, the Seer). Every shot is exactly one bar (2.667 s), with text-only captions and a question at the end. This format recycles the monsters and promotes the other Shorts. The music is also exported as an MP3.
- **Myths** (long video + Short): "I Tested 20 Scary Minecraft Myths... 11 Are REAL". It's a fast myth-testing format with a counter (`fx.counter`), a myth banner (`fx.label`) and REAL/BUSTED stamps (`fx.stamp`); the Short cut is myth #20, "you're never alone in singleplayer".
- **Planned (from YouTube Studio suggestions):** "The Chest That Warns Me Never To Place It Down" as a long video (a forbidden rule, then worse and worse consequences, like *DON'T BREAK THE WALL*). Skip "moving shadows" (the engine can't draw real shadows).
- Next ideas from trend research (Sept 2026): a helpful thing that turns evil (the *Verity* trend), Alpha/found-footage nostalgia, testing scary seeds, "what mobs do when you log off", and "Giant Alex".

## Look (glitch-horror toolkit)
- The entity is white and faceless (`skin: glitch`, `glow: 0.8`, `float`, `still`), with head tilts. The mouth reveal uses `glitch_mouth`.
- Corruption visuals: missing-texture magenta/black blocks (`cubes`), a grey grid sky (`fx.grid`), villagers without skins (`skin: missing`), a chest full of red `null` items, and void holes (break y 58–63).
- Ending: a fall into the void, a sea of checker, then the fake desktop (`fx.desktop`) typing a message, a static burst and black.
- Lighting: torchlight for reveals (`cave_torch`), `cave_dark` for the last shot, `void` for the climax.

## Retention rules (from the channel's own analytics)
The first Glitch Short had 42.6% "stayed to watch", so more than half of viewers swiped away at the start. It also slowed down in the setup before turning dark at about 20 s. So:
- **0:00 must already be scary.** The entity (or the action) is on screen from frame 1, with an on-screen **text question** at 0:00 (for example "WOULD YOU BRING THIS HOME?"). Add a glitch flash and blip sound on frame 1. No establishing shots and no slow fade-ins.
- **The story turns dark by ~15 s.** Keep the wholesome setup to about 10 s total, with shots of 2–3.5 s each.
- **Voice runs fast** (`vo_speed` about 1.2) in the setup. Leave no silent gaps longer than about 1 s before the climax.
- **A small jolt every 3–4 s:** a glitch flash (`fx.glitch` spike) plus a `blip` sound, or a hard cut. Tease the corruption early (a blip even in the cozy shots).
- The long video follows the same rules for its first 30 s.

## Shorts formula (≤ 60 s)
1. **0 s hook:** the weird thing on screen, a text question and a glitch blip, plus a one-line claim ("I found a player with no face in my Minecraft cave.").
2. A quick wholesome bit (3–4 shots, about 10 s in total, each with a blip teaser), then "Then on day three…" by about 15 s.
3. Rapid corruption beats, 4 s each.
4. Reveal: a big shout caption and a sting.
5. Ending: the fake desktop message, a whispered title line and static, cut so it **loops** back to the hook.

## Community post
- **Image:** 1080×1080 frame from the scariest reveal shot, with a dark purple shade.
  - Pixel label "NEW VIDEO · SHADOW BLOCK TALES".
  - Big Anton title with a magenta/cyan RGB split.
  - A small red `null` tag, a magenta/black checker stripe, and a one-line warning ("DON'T BRING IT HOME.").
- **Text:** a 2–3 line eerie tease in first person, the video title, then a question to drive comments ("Would YOU have brought him home? 👇").

## Fact-checking (myth, fact and "is it real?" videos)
- Every REAL/BUSTED verdict must be true about the actual game. Minecraft fans correct mistakes in the comments fast, and a wrong "REAL" costs trust.
- Scripts from other tools often make up "real code" facts, like proximity-triggered cave sounds, seed 404 pits or 16-block sculk range. Check each claim, and replace or bust anything that isn't true.
- Keep the counter honest: count only the myths actually shown (20, not "100"), and make the final tally match the verdicts.
- Story videos (Glitch, Copycats, Seer) are fiction and can say anything. Only "is it real?" formats need this.

## Titles and descriptions (search keywords, from YouTube Studio's tips)
Most viewers find the channel through the Shorts feed. Search is the second way in, so every title and description carries the words people actually search for.
- **Title:** a curiosity hook plus a searchable keyword, with "Minecraft" near the front. Put the genre in brackets at the end: "(Minecraft Horror)", "(Minecraft Creepypasta)", "(Scary Villager Trades)". Keep it under about 70 characters, with CAPS on one key word (COPYING, NEVER). Shorts add 😨.
  - Examples: "My Minecraft Villagers Started COPYING Me… 😨 (Minecraft Horror)", "Testing 20 Scary Minecraft Myths (Herobrine, Seed 666, Far Lands) – 11 Are REAL".
- **Keywords to use naturally:** Minecraft horror, Minecraft creepypasta, scary Minecraft, Minecraft myths, Herobrine, Minecraft villager, glitch / missing texture mob, seed, Far Lands, Warden, singleplayer. Name specific mobs, mechanics and myths, because people search for those.
- **Description:** the first line is a keyword sentence (it shows in search): "Minecraft horror story: …". The second line adds related terms ("Scary Minecraft Short / Minecraft creepypasta"). End with **3 hashtags only**, since YouTube shows the first 3 above the title: #minecrafthorror #minecraft plus one topic tag (#minecraftcreepypasta, #minecraftmyths, #herobrine, #minecraftvillager…).
- Never stuff keywords, and never use a keyword the video doesn't actually deliver.
- **Hooks:** the 0:00 retention rules above (the scary thing on screen, a text question, and a glitch blip in the first 2–3 seconds) are the first thing to check on every Short, before the keywords.

## Working notes
- The owner works on Windows.
- Git commits are authored only as the owner (no co-author lines).
- YouTube links can't be opened from the build machine. When given a reference video, ask for a short description or its script.

## Retention playbook (researched Oct 2026, applies to every video)

Targets: long videos under 5 min should keep 50–70% average; 10–20 min videos 40–55%. Keep 60%+ of viewers past 0:30.
Shorts: "Viewed vs swiped away" should be 70–90%; under 60% means the first 1–3 seconds failed.

**First 30 seconds (the algorithm judges these on their own)**
- Frame 1 is the scariest image of the video, with a spoken question or claim in the first sentence. No logo, no "welcome back".
- "Previously…" recaps go AFTER the hook and stay under 4 s (one line), or are cut. Never shot 2 at 8 s again.
- State the promise by 0:20 ("by day 100 he was at my door").

**Every 5–10 seconds something changes** (long form; every 2–3 s in Shorts)
- New camera angle, a punch-in, a text pop, a glitch, a sound hit. A shot longer than ~8 s gets split into two angles.
- Engine does this automatically now: handheld sway on every shot (`camera.shake`, default 0.25; set 0 for a locked tripod shot),
  and a jolt + 12% punch-in zoom on every `sting` sound (`camera.auto_scare: false` to turn off; manual `camera.jolt` / `camera.punch: [[t, amount]]`).

**Story structure**
- Open loop in the hook ("the journal stopped at day 99"), paid off late. Max 1–2 open loops per video.
- Every reveal is followed immediately by a new question (hook → deliver → new hook). No flat pause between beats.
- Re-hook every ~60–90 s in long videos: a mid-video "but then…" turn or a new threat.

**Horror pacing**
- Slow burn: quiet holds and near-silence BEFORE a scare, then a loud sting. Silence is a tool; don't keep music on wall to wall.
- Speed up cuts during chases/montages, slow down on reveals so they land.
- Sound design over music: footsteps, door creaks, breathing, distant noises.

**Shorts**
- First frame = hook; audio or visual beat every 2–3 s; the last line should flow back into the first (loop), e.g. end on a question the opening answers.

**Diagnose with the retention graph (YouTube Studio → Analytics → video → Audience retention)**
- Big drop in first 30 s → hook/thumbnail mismatch or slow opening.
- Steady slide → pacing too slow / shots too long.
- Sudden cliff at one moment → that beat is boring or confusing; cut or move it.
- Spikes (rewatches) → do more of what's at that timestamp.

## Kids audience mode (the channel's viewers are mostly kids) — researched Oct 2026
Top kids Minecraft channels (Maizen / JJ & Mikey, Aphmau etc.) use: a sound effect roughly every 3 s, constant zooms,
fast cuts, bright saturated colours, characters with big reactions, and simple story drama (good guy vs scary thing).
Keep it spooky-fun, never gory: jump scares + funny relief, no blood, no real-world violence.

**Engine tools (use them every video)**
- `grade: vivid` at script level: bright, saturated colours (horror scenes can override per shot with `fx.grade: cold` or null).
- `fx.pop: [[t, "WHAT?! 😱", "#ffd21f"]]`: bouncy reaction text with emoji (auto "pop" sound). 1–2 per shot in Shorts, every ~5 s in long form.
- `fx.flash: [[t, "#ff2b2b"]]`: colour flash on hits/scares (pair with a `boom`).
- `fx.speed: 1` (or keys): speed lines for chases and reveals.
- Sounds (`sfx` type): boom (bass drop), pop, boing, ding, riser (with `dur`), scratch (record scratch for "wait, WHAT?"), dundun (dramatic), sparkle, plus whoosh/sting/blip/thud.
- Camera: handheld sway + automatic jolt and punch-in on every `sting`.

**Rhythm**
- Shorts: a sound or visual hit every 2–3 s; long form every 3–5 s. Never more than ~5 s of nothing new.
- Pattern per beat: riser → boom + flash + pop text → reaction line. Use scratch before a twist ("wait...").
- Voice: fast and excited (vo_speed 1.2+), short sentences, lots of questions ("Who did this?!").

**Made for kids setting**: YouTube requires an honest "made for kids" label. If it's set to Made for kids, comments and the
notification bell are turned off and ads aren't personalised. Decide using YouTube's own guidance (Studio → Settings → Channel → Advanced),
not to protect comments.
