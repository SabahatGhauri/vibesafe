# Claude Memory Gateway (MVP)

Long Claude Code sessions get **compacted**: older conversation is summarised
to make room, and the summary drops what you asked for, what was decided and
what was half done. Claude then acts as if it has no record. The gateway puts
that back automatically.

| When | What it does |
|---|---|
| Session starts | Loads the repo's handoff notes (`.claude/memory/NOTES.md`) and git state into Claude's context |
| Just before compaction | Saves your last 15 requests and the git state to `~/.claude/memory-gateway/` (outside the repo) |
| Right after compaction | Restores those notes and requests, and tells Claude to ask rather than guess |
| Claude commits work without updating the notes | Asks Claude once to update and commit `NOTES.md` |
| You type `/checkpoint` | Claude rewrites the notes on demand |

Everything runs locally as Claude Code hooks. Nothing is sent anywhere.

## Install

It's one self-contained file, `install.sh`, and it needs `python3` and `git`.

**Your own computer** (every session, every repo):

```bash
bash tools/memory-gateway/install.sh
```

**Claude Code on the web** (every cloud session): open the environment menu in
the session title bar, choose **Edit**, and paste the whole contents of
`install.sh` into **Setup script**. No clone is needed, so it works even if
this repo is private.

**One repo only:** copy `.claude/settings.json`, `.claude/hooks/` and
`.claude/skills/checkpoint/` from this repo into the other one.

Check it, or remove it:

```bash
bash tools/memory-gateway/install.sh status
bash tools/memory-gateway/install.sh uninstall
```

The installer is safe to re-run. It keeps any hooks and settings you already
have, and it won't overwrite a `/checkpoint` skill that you wrote yourself.

## Limits (MVP)

- It restores your *requests*, not Claude's full reasoning. The notes are only
  as good as what Claude writes into them.
- `NOTES.md` is committed to the repo. Keep secrets out of it, and if the repo
  is deployed as a static site, exclude `.claude/` from the deploy.
- The commit nudge only fires on commits. Long work that is never committed
  relies on compaction snapshots and `/checkpoint`.

## Developing

The installer is generated. Edit `.claude/hooks/memory_gateway.py`,
`.claude/skills/checkpoint/SKILL.md` or `install.template.sh`, then run:

```bash
bash tools/memory-gateway/build.sh   # regenerate install.sh
bash tools/memory-gateway/test.sh    # 18 smoke tests in a throwaway HOME
```
