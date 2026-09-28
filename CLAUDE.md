# VibeSafe website: notes for Claude

Static marketing and dashboard site for vibesafe.info, deployed by Vercel
straight from this repo (no build step). The scanner API lives elsewhere
(vibesafe-api.vercel.app). Preview locally with `python -m http.server 5510`.

## Session memory

Long sessions get compacted and lose detail. Hooks in `.claude/settings.json`
handle it automatically:

- **Session start and after compaction:** `.claude/memory/NOTES.md` (durable
  handoff notes), the pre-compaction snapshot of the user's recent requests,
  and the git state are loaded into context.
- **Before compaction:** the user's recent requests and git state are saved to
  `~/.claude/memory-gateway/` (outside the repo, never committed).
- **When Claude commits work without touching NOTES.md**, it is asked once to
  update the notes before finishing. `/checkpoint` does the same on demand.
- If the context after compaction doesn't answer a question, read NOTES.md and
  `git log` before asking the user. Never guess at what was agreed.

To get the same memory in every repo, see `tools/memory-gateway/README.md`
(one self-contained installer). After editing the hook or the checkpoint
skill, run `tools/memory-gateway/build.sh` then `tools/memory-gateway/test.sh`.

## Conventions

- Commit messages describe the effect for the user in plain English
  (e.g. "Let a signed-in customer change their password from the dashboard").
- Copy about pricing, trials and security coverage must be accurate. This is a
  security product, and overstating matters.
- Every file in the repo is public on the live site unless it is listed in
  `.vercelignore`.
