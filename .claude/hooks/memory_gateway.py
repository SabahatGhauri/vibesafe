#!/usr/bin/env python3
"""Memory gateway for long Claude Code sessions.

When a session runs long, Claude Code compacts (summarises) the conversation
and details get lost: what the user asked for, what was decided, what is half
done. This hook puts that back.

  snapshot  (PreCompact hook)   saves the user's recent requests and the git
                                state to .claude/memory/last-snapshot.md
  restore   (SessionStart hook) prints NOTES.md, the latest snapshot and the
                                current git state; Claude Code adds whatever a
                                SessionStart hook prints to Claude's context

Always exits 0: a broken hook must never block a session.
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
MEMORY = os.path.join(ROOT, ".claude", "memory")
NOTES = os.path.join(MEMORY, "NOTES.md")
SNAPSHOT = os.path.join(MEMORY, "last-snapshot.md")

MAX_REQUESTS = 15       # recent user messages kept in a snapshot
MAX_REQUEST_CHARS = 600  # each one trimmed to this
MAX_NOTES_CHARS = 8000   # keep the injected context small


def git(*args):
    try:
        out = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                             text=True, timeout=10)
        return out.stdout.strip()
    except Exception:
        return ""


def git_state():
    status = git("status", "--short")
    return "\n".join([
        f"Branch: {git('rev-parse', '--abbrev-ref', 'HEAD') or 'unknown'}",
        "",
        "Recent commits:",
        git("log", "--oneline", "-8") or "(none)",
        "",
        "Uncommitted changes:",
        status if status else "(working tree clean)",
    ])


def user_text(entry):
    """Return the text of a real user message, or None for tool results,
    system reminders and other non-human entries."""
    if entry.get("type") != "user" or entry.get("isMeta"):
        return None
    content = (entry.get("message") or {}).get("content")
    if isinstance(content, list):
        if any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content):
            return None
        content = "\n".join(b.get("text", "") for b in content
                            if isinstance(b, dict) and b.get("type") == "text")
    if not isinstance(content, str):
        return None
    text = content.strip()
    if not text or text.startswith("<"):  # harness wrappers, reminders
        return None
    return text


def recent_requests(transcript_path):
    requests = []
    try:
        with open(transcript_path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    text = user_text(json.loads(line))
                except (ValueError, AttributeError):
                    continue
                if text:
                    requests.append(text)
    except OSError:
        return []
    trimmed = []
    for text in requests[-MAX_REQUESTS:]:
        if len(text) > MAX_REQUEST_CHARS:
            text = text[:MAX_REQUEST_CHARS] + " [...]"
        trimmed.append(text)
    return trimmed


def snapshot(hook_input):
    requests = recent_requests(hook_input.get("transcript_path") or "")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"# Auto-snapshot before compaction ({stamp})", "",
             "## The user's most recent requests (oldest first)", ""]
    lines += [f"{i}. {r}" for i, r in enumerate(requests, 1)] or ["(none found)"]
    lines += ["", "## Git state at snapshot time", "", "```", git_state(), "```", ""]
    os.makedirs(MEMORY, exist_ok=True)
    with open(SNAPSHOT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def read(path, limit):
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read().strip()
    except OSError:
        return ""
    if len(text) > limit:
        text = text[:limit] + "\n[... truncated, read the file for the rest]"
    return text


def restore(hook_input):
    source = hook_input.get("source", "startup")
    parts = ["=== MEMORY GATEWAY (injected by .claude/hooks/memory_gateway.py) ==="]
    if source == "compact":
        parts.append("The conversation was just compacted, so earlier details may be "
                     "missing from your summary. Trust the notes and snapshot below; "
                     "if something is still unclear, ask the user instead of guessing.")
    notes = read(NOTES, MAX_NOTES_CHARS)
    parts += ["", "--- .claude/memory/NOTES.md (durable handoff notes) ---",
              notes or "(empty: run /checkpoint to start keeping notes)"]
    # A snapshot only describes the session that was compacted; after a fresh
    # start it is stale, so only show it when resuming or after compaction.
    if source in ("compact", "resume"):
        snap = read(SNAPSHOT, MAX_NOTES_CHARS)
        if snap:
            parts += ["", "--- .claude/memory/last-snapshot.md ---", snap]
    parts += ["", "--- Current git state ---", git_state(),
              "=== END MEMORY GATEWAY ==="]
    print("\n".join(parts))


def main():
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}
    mode = sys.argv[1] if len(sys.argv) > 1 else "restore"
    try:
        snapshot(hook_input) if mode == "snapshot" else restore(hook_input)
    except Exception as exc:  # never break the session
        print(f"memory_gateway: {exc}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
