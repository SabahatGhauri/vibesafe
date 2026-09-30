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

## Titles and descriptions
- **Title:** "I Adopted a 'Glitch' in Minecraft..." style (first person, ellipsis). Shorts add an emoji (😨).
- **Description:** 1–2 teaser lines, then hashtags: #minecraft #minecrafthorror #minecraftcreepypasta (+ #shorts for Shorts).

## Working notes
- The owner works on Windows.
- Git commits are authored only as the owner (no co-author lines).
- YouTube links can't be opened from the build machine. When given a reference video, ask for a short description or its script.
