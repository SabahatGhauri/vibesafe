#!/usr/bin/env bash
# Install the memory gateway for EVERY Claude Code session on this machine,
# in any repo: copies the hook and the /checkpoint skill into ~/.claude and
# registers the hooks in ~/.claude/settings.json. Safe to run repeatedly.
#
#   Local machine:  bash .claude/install-global.sh
#   Cloud sessions: add the same line to the environment's setup script
#                   (see the README section in CLAUDE.md).
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$HOME/.claude"
mkdir -p "$DEST/hooks" "$DEST/skills/checkpoint"
cp "$SRC/hooks/memory_gateway.py" "$DEST/hooks/memory_gateway.py"
cp "$SRC/skills/checkpoint/SKILL.md" "$DEST/skills/checkpoint/SKILL.md"

python3 - "$DEST/settings.json" <<'PY'
import json, os, sys
path = sys.argv[1]
try:
    with open(path) as fh:
        settings = json.load(fh)
except FileNotFoundError:
    settings = {}
hooks = settings.setdefault("hooks", {})
script = os.path.expanduser("~/.claude/hooks/memory_gateway.py")
for event, mode in (("SessionStart", "restore"), ("PreCompact", "snapshot"), ("Stop", "stop")):
    command = f'python3 "{script}" {mode} --global'
    groups = hooks.setdefault(event, [])
    # Drop any earlier install of ours, then add the current one.
    for group in groups:
        group["hooks"] = [h for h in group.get("hooks", [])
                          if "memory_gateway.py" not in h.get("command", "")]
    groups[:] = [g for g in groups if g.get("hooks")]
    groups.append({"matcher": "", "hooks": [{"type": "command", "command": command}]})
with open(path, "w") as fh:
    json.dump(settings, fh, indent=2)
    fh.write("\n")
PY
echo "Memory gateway installed for all sessions (hooks in $DEST/settings.json)."
