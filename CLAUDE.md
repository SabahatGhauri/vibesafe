# VibeSafe website: notes for Claude

Static marketing and dashboard site for vibesafe.info, deployed by Vercel
straight from this repo (no build step). The scanner API lives elsewhere
(vibesafe-api.vercel.app). Preview locally with `python -m http.server 5510`.

## Session memory

Long sessions get compacted and lose detail. To stop that:

- `.claude/memory/NOTES.md` holds durable handoff notes. A SessionStart hook
  loads it into context automatically, including right after compaction.
- Run `/checkpoint` (or update NOTES.md yourself) after any decision, finished
  task or change of direction.
- Before compaction a hook saves the user's recent requests and the git state
  to `.claude/memory/last-snapshot.md` (not committed), and they come back
  after compaction.
- If the context after compaction doesn't answer a question, read NOTES.md and
  `git log` before asking the user. Never guess at what was agreed.

## Conventions

- Commit messages describe the effect for the user in plain English
  (e.g. "Let a signed-in customer change their password from the dashboard").
- Copy about pricing, trials and security coverage must be accurate. This is a
  security product, and overstating matters.
- Every file in the repo is public on the live site unless it is listed in
  `.vercelignore`.
