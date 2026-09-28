---
name: checkpoint
description: Save the current session's state to .claude/memory/NOTES.md so it survives compaction and new sessions. Use when the user says /checkpoint, "save progress", "remember this", or before a long task switches direction.
---

Update `.claude/memory/NOTES.md` so a fresh Claude with no memory of this
conversation could pick the work up correctly.

1. Read the current `.claude/memory/NOTES.md`.
2. Rewrite its sections from what happened in this session:
   - **Current focus**: what the user is working on right now, in their words.
   - **Decisions and why**: choices the user made or approved, with the reason.
     Never drop an earlier decision unless the user reversed it.
   - **Open threads / next steps**: what's unfinished, blocked, or promised.
   - **Gotchas**: things that surprised you or broke, and how they were handled.
3. Keep it under about 60 lines. Replace stale entries; don't append a log.
4. Never write secrets, API keys, passwords or customer data into it: this file
   is committed to git. If the repo deploys its files publicly (e.g. a static
   site with no build step) and `.claude` is not excluded from the deploy, add
   it to the ignore file (`.vercelignore`, `.netlifyignore`, ...) first.
5. Commit it on its own (`Update handoff notes`) and push if the session
   normally pushes, since a cloud container is thrown away when it ends.
6. Tell the user in one or two lines what you saved.
